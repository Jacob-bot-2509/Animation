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


def split(pool: Path, plan: Path, out: Path, dry_run: bool) -> dict:
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

    summary = {"pool": str(pool), "plan": str(plan),
               "pool_n": len(by_id), "assigned": len(assigned),
               "rejected": len(rejects),
               "counts": {k: len(v) for k, v in split_rows.items()},
               "dry_run": dry_run,
               "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")}

    if dry_run:
        return {"dry_run": True, **summary}

    out.mkdir(parents=True, exist_ok=True)
    for split_name, lines in split_rows.items():
        (out / f"{split_name}.jsonl").write_text(
            "\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    rejects.sort(key=lambda x: str(x.get("sample_id")))
    (out / "rejected.jsonl").write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in rejects) + "\n",
        encoding="utf-8")
    # split manifest:输出清单含每个文件 sha256(可重放的依据)
    manifest = {"split_manifest_version": 1, **summary, "files": {}}
    for f in ("train.jsonl", "eval.jsonl", "test.jsonl", "rejected.jsonl"):
        p = out / f
        manifest["files"][f] = {
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            "size": p.stat().st_size}
    (out / "split_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return manifest


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--pool", required=True, help="池子 JSONL(只读)")
    ap.add_argument("--plan", required=True, help="ID 清单 JSON")
    ap.add_argument("--out", required=True, help="输出目录")
    ap.add_argument("--dry-run", action="store_true", help="只算分配不写文件")
    args = ap.parse_args(argv)
    r = split(Path(args.pool), Path(args.plan), Path(args.out), args.dry_run)
    if r.get("dry_run"):
        print("dry-run:", json.dumps({k: v for k, v in r.items() if k != "dry_run"},
                                     ensure_ascii=False))
    else:
        print(json.dumps({"counts": r["counts"], "rejected": r["rejected"],
                          "files": list(r["files"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
