"""split 工具:按 ID 清单从池子筛分 train/eval/test(确定性,可重放)。

msg_101-2/3:
- split 可重新筛分:plan 是显式 ID 清单,同一 pool+plan 重复运行输出字节一致
- 失败保留原始 sample_id 与原因:
  池里有但 plan 未分配 → rejected(reason=未分配);
  plan 里有但池中缺失 → rejected(reason=池中缺失);
  池中重复 ID → rejected(reason=池中重复)
- 不重写原始数据:只读 pool,输出到新目录

用法:
  python tools/split_data.py --pool pool.jsonl --plan plan.json --out data \
      [--dry-run]
plan.json 格式: {"train": ["id1", ...], "eval": [...], "test": [...]}
输出: train.jsonl / eval.jsonl / test.jsonl / rejected.jsonl / split_manifest.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.fs_guard import ensure_not_exists  # noqa: E402


def load_pool(pool: Path) -> tuple[dict[str, str], list[dict]]:
    """返回 (id → 原始行, 重复/坏行记录)。"""
    by_id: dict[str, str] = {}
    bad: list[dict] = []
    for i, line in enumerate(pool.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            bad.append({"sample_id": f"<line-{i}>", "line": i,
                        "reason": f"JSON 解析失败:{sys.exc_info()[1] if False else ''}"})
            continue
        sid = obj.get("id") or obj.get("sample_id")
        if not sid:
            bad.append({"sample_id": f"<line-{i}>", "line": i, "reason": "无 id/sample_id 字段"})
            continue
        if sid in by_id:
            bad.append({"sample_id": sid, "line": i, "reason": "池中重复 ID"})
            continue
        by_id[sid] = line.strip()
    return by_id, bad


def split(pool: Path, plan: Path, out: Path, dry_run: bool,
          force: bool = False, license_: str = "",
          frozen_locks: list[Path] | None = None,
          allow_empty: bool = False) -> dict:
    by_id, bad = load_pool(pool)
    plan_obj = json.loads(plan.read_text(encoding="utf-8"))
    rejects = list(bad)

    split_rows: dict[str, list[str]] = {"train": [], "eval": [], "test": []}
    assigned: set[str] = set()
    for split_name in ("train", "eval", "test"):
        for sid in plan_obj.get(split_name, []):
            if sid in by_id and sid not in assigned:
                split_rows[split_name].append(by_id[sid])
                assigned.add(sid)
            elif sid in assigned:
                rejects.append({"sample_id": sid, "reason": "计划中重复分配(按先到先得,后者拒绝)"})
            else:
                rejects.append({"sample_id": sid, "reason": "池中缺失"})

    for sid, line in by_id.items():
        if sid not in assigned:
            rejects.append({"sample_id": sid, "reason": "未分配"})

    # C2:空 split 默认拒绝 —— 不写空文件、不伪造样本;确需空集合显式 --allow-empty
    for name in ("train", "eval", "test"):
        if not split_rows[name] and not allow_empty:
            raise SystemExit(f"拒绝:{name} split 为空 —— 不写空文件也不伪造样本"
                             "(C2);确需空集合请显式 --allow-empty")

    summary = {"pool": str(pool), "plan": str(plan),
               "pool_n": len(by_id), "assigned": len(assigned),
               "rejected": len(rejects),
               "counts": {k: len(v) for k, v in split_rows.items()},
               "dry_run": dry_run,
               "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")}

    if dry_run:
        return {"dry_run": True, **summary}

    # R1 写保护:输出目录不得与池子同目录(会原地覆盖 pool),已有输出默认拒绝;
    # 复审 R1:--force 也不得覆盖任何输入文件 —— 每个输出路径与 pool/plan
    # 的 resolve 比对,相同即拒绝(输入文件永远只读)
    out_res = out.resolve()
    inputs = {pool.resolve(), plan.resolve()}
    if out_res == pool.resolve().parent:
        raise SystemExit(f"拒绝:--out 与 pool 同目录({out}),会原地覆盖池子")
    from animtrain.freeze import (  # noqa: PLC0415 局部导入避免环
        check_frozen, discover_locks, frozen_paths)
    # BR5 复验(omitted_lock):自动发现冻结锁 —— 漏传 --frozen-lock
    # 也必须在写入前发现冻结标记;显式传入的锁用于跨目录场景
    valid, suspicious = discover_locks([out, pool, plan])
    # fail closed:发现无法识别的 *.lock.json(坏 JSON 等)必须拒绝写入,
    # 不得忽略(omitted_corrupt 反例)
    for sp in suspicious:
        if sp not in [lk.resolve() for lk in (frozen_locks or [])]:
            raise SystemExit(f"拒绝:发现无法识别的锁标记 {sp} —— 可能是损坏的"
                             "冻结锁,必须 fail closed(BR5)")
    all_locks = list(frozen_locks or [])
    all_locks += [lk for lk in valid if lk not in all_locks]
    frozen: set[str] = set()
    for lk in all_locks:
        # fail closed:锁不存在/损坏时不得静默放行
        if not lk.exists():
            raise SystemExit(f"拒绝:冻结锁不存在 {lk}(fail closed)")
        problems = check_frozen(lk)
        if problems:
            raise SystemExit(f"拒绝:冻结锁校验未过 {lk}: {problems[0]}"
                             "(fail closed)")
        frozen |= frozen_paths(lk)
    for f in ("train.jsonl", "eval.jsonl", "test.jsonl", "rejected.jsonl",
              "split_manifest.json"):
        target = (out / f).resolve()
        if target in inputs:
            raise SystemExit(f"拒绝:{target} 是输入文件(pool/plan),"
                             "无论是否 --force 都不得覆盖")
        if str(target) in frozen:
            raise SystemExit(f"拒绝:{target} 属于冻结数据集,"
                             "无论是否 --force 都不得写入(BR5)")
        ensure_not_exists(out / f, force=force)
    from animtrain.atomic_write import atomic_write_text  # noqa: PLC0415
    out.mkdir(parents=True, exist_ok=True)
    for split_name, lines in split_rows.items():
        atomic_write_text(out / f"{split_name}.jsonl",
                          "\n".join(lines) + ("\n" if lines else ""))
    rejects.sort(key=lambda x: str(x.get("sample_id")))
    atomic_write_text(out / "rejected.jsonl",
                      "\n".join(json.dumps(x, ensure_ascii=False) for x in rejects) + "\n")
    # R2: split manifest 用标准 Manifest v1 格式 —— Manifest.load 可直接读,
    # data_check 可直接校验;entries 登记输出文件并标正确 split。
    entries = []
    for f in ("train.jsonl", "eval.jsonl", "test.jsonl", "rejected.jsonl"):
        fp = out / f
        if not fp.exists():
            continue
        entries.append({"path": f,
                        "sha256": hashlib.sha256(fp.read_bytes()).hexdigest(),
                        "size": fp.stat().st_size,
                        "source": f"split:pool={pool} plan={plan}",
                        "license": license_,
                        "split": f.removesuffix(".jsonl") if f != "rejected.jsonl" else "raw",
                        "notes": f"由 split_data 生成: {f}"})
    manifest = {"name": f"split-{out.name}", "version": 1,
                "generated_at": summary["generated_at"],
                "policy": "split 产物清单;train/eval/test 与 rejected 分离;"
                          "输入 pool/plan 见各 entry.notes",
                "entries": entries}
    atomic_write_text(out / "split_manifest.json",
                      json.dumps(manifest, ensure_ascii=False, indent=2))
    return {**summary, "split_manifest": "标准 Manifest v1 格式" }


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", required=True, help="池子 JSONL(只读)")
    ap.add_argument("--plan", required=True, help="ID 清单 JSON")
    ap.add_argument("--out", required=True, help="输出目录")
    ap.add_argument("--dry-run", action="store_true", help="只算分配不写文件")
    ap.add_argument("--force", action="store_true", help="允许覆盖已存在输出(默认拒绝)")
    ap.add_argument("--license", default="",
                    help="输出数据许可证(未提供则留空 → 校验报 quarantine,不硬写)")
    ap.add_argument("--frozen-lock", action="append", default=[],
                    help="冻结锁(可多次);输出命中冻结文件一律拒绝,force 也不绕过")
    ap.add_argument("--allow-empty", action="store_true",
                    help="允许空 split 写出空文件(C2 默认拒绝空集合)")
    args = ap.parse_args(argv)
    r = split(Path(args.pool), Path(args.plan), Path(args.out), args.dry_run,
              force=args.force, license_=args.license,
              frozen_locks=[Path(f) for f in args.frozen_lock],
              allow_empty=args.allow_empty)
    if r.get("dry_run"):
        print("dry-run:", json.dumps({k: v for k, v in r.items() if k != "dry_run"},
                                     ensure_ascii=False))
    else:
        print(json.dumps({"counts": r["counts"], "rejected": r["rejected"],
                          "split_manifest": r["split_manifest"]},
                         ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
