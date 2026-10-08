"""preflight CLI:训练前检查清单(msg_101-6)。任何 FAIL → 禁止后续动作。

用法:
  python tools/preflight.py                    # 只查 GPU
  python tools/preflight.py --model .models/xxx   # GPU + 模型文件
  python tools/preflight.py --manifest data/manifest.json   # 附带数据门禁

不下载模型、不启动训练;数据门禁用 data_check 同款校验(只读)。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.manifest import Manifest  # noqa: E402
from animtrain.preflight import check_asset_evidence, run_preflight  # noqa: E402
from animtrain.validate import validate_manifest  # noqa: E402


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="", help="模型目录(存在性+关键文件)")
    ap.add_argument("--manifest", default="", help="数据 manifest(附带数据门禁)")
    ap.add_argument("--strict", action="store_true",
                    help="严格模式:模型/数据门禁必填,缺失即 FAIL(训练前用)")
    ap.add_argument("--ready", action="store_true",
                    help="B2 训练就绪聚合:gpu/model_dir/data_manifest/run_snapshot"
                         " 全部通过且无 UNVERIFIED 才 ready")
    ap.add_argument("--run-id", default="",
                    help="--ready 时必填:运行快照 run_id(校验 runs/<id>/run_record.json)")
    args = ap.parse_args(argv)

    from animtrain.fs_guard import valid_run_id  # noqa: E402
    extra: list[tuple[str, tuple[bool, str]]] = []
    mp: Path | None = None
    if args.run_id:
        # BR4: 先验证 run_id 再拼路径(与 run_record CLI 输入边界一致)
        if not valid_run_id(args.run_id):
            print(f"[FAIL] run_id 非法: {args.run_id!r}")
            return 1
        from animtrain.run_record import RunRecord, check_record  # noqa: E402
        rp = ROOT / "runs" / args.run_id / "run_record.json"
        if rp.exists():
            rec = RunRecord.load(rp)
            # BR4 复验:manifest 路径先确定,快照校验必须绑定它
            # (否则 record_hash 与实际文件不符仍能 READY)
            mp_here = None
            if args.manifest:
                mp_here = Path(args.manifest)
            elif rec.summary.get("manifest"):
                mp_here = ROOT / rec.summary["manifest"]
            problems = check_record(rec, manifest_path=mp_here)
            extra.append(("run_snapshot",
                          (not problems,
                           f"run {args.run_id} 快照{'通过' if not problems else '未过: ' + '; '.join(problems[:3])}")))
        else:
            extra.append(("run_snapshot", (False, f"快照不存在: {rp}")))
    if args.manifest:
        mp = Path(args.manifest)
        if mp.exists():
            m = Manifest.load(mp)
            rep = validate_manifest(m, mp.parent)
            extra.append(("data_manifest", (rep["ok"], f"{rep['n_entries']} 条目,"
                           f"问题 {len(rep['problems'])},quarantine {len(rep['quarantines'])}")))
            # BR4: near_dup_calibrated 必须传播 —— UNCALIBRATED 的阈值
            # 在 ready 模式下明确阻止(数据隔离验收未完成)
            if not rep.get("near_dup_calibrated", False):
                extra.append(("near_dup_calibrated", (False,
                              "近重复阈值 UNCALIBRATED(真实数据对照实验未完成)"
                              "—— ready 模式必须阻断")))
        else:
            extra.append(("data_manifest", (False, f"manifest 不存在: {mp}")))
    # BR4-b 复验:门禁必须提供**真实执行证据**,不能只查依赖存在。
    # render_gate: 真实渲染项目内可信模板(trusted=True,已审查样例)
    from animtrain.render_gate import render_check, math_check  # noqa: E402
    _RENDER_SMOKE = (
        "from manim import *\n\n\n"
        "class ConceptScene(Scene):\n"
        "    def construct(self):\n"
        "        eq = MathTex(r\"x^2\")\n"
        "        self.add(eq)\n"
        "        self.wait(0.2)\n")
    rr = render_check(_RENDER_SMOKE, trusted=True)
    extra.append(("render_gate",
                  (rr["ok"], f"环境诊断(固定可信 smoke,**非资产验收证据**): "
                             f"{rr['status']} — {rr['detail'][:100]}")))
    # math_gate: 真实数学断言(真命题)
    mr = math_check("Eq(2 + 2, 4)")
    extra.append(("math_gate",
                  (mr["ok"], f"环境诊断(固定数学 smoke,**非资产验收证据**): "
                             f"{mr['status']} — {mr['detail'][:100]}")))
    # freeze_gate(BR4-b 复验):冻结证据必须绑定当前 manifest 的 eval/test
    # 集合 —— 无锁/部分覆盖/无关锁/坏锁/锁与 manifest hash 不一致均 NOT READY
    from animtrain.freeze import check_frozen, discover_locks, frozen_paths  # noqa: E402
    import hashlib as _hashlib  # noqa: E402
    import json as _json  # noqa: E402
    eval_test_files: set[str] = set()
    manifest_sha = ""
    if mp is not None and mp.exists():
        manifest_sha = _hashlib.sha256(mp.read_bytes()).hexdigest()
        m2 = Manifest.load(mp)
        for e in m2.entries:
            if e.split in ("eval", "test"):
                eval_test_files.add(str((mp.parent / e.path).resolve()))
    f_problems: list[str] = []
    f_ok = False
    if not eval_test_files:
        f_problems.append("当前 manifest 无 eval/test 条目 —— 无法验收冻结证据")
    else:
        valid, suspicious = discover_locks([ROOT / "data", ROOT], max_depth=2)
        if suspicious:
            f_problems.append(f"发现无法识别的锁标记 {len(suspicious)} 个: {suspicious[0]}")
        if not valid:
            f_problems.append("无冻结锁 —— eval/test 必须先冻结(BR4-b)")
        else:
            for lk in valid:
                f_problems += check_frozen(lk)
            frozen_all: set[str] = set()
            manifest_bound: list[tuple[str, str]] = []
            for lk in valid:
                frozen_all |= frozen_paths(lk)
                try:
                    meta = _json.loads(lk.read_text(encoding="utf-8")).get("meta", {})
                except Exception:
                    meta = {}
                bound_sha = meta.get("manifest_sha256") if isinstance(meta, dict) else None
                if not isinstance(bound_sha, str) or not bound_sha:
                    f_problems.append(f"锁 {lk} 缺少有效 manifest_sha256 绑定，不能作为冻结证据")
                else:
                    manifest_bound.append((str(lk), bound_sha))
            uncovered = eval_test_files - frozen_all
            if uncovered:
                f_problems.append(f"eval/test 部分未冻结({len(uncovered)} 个文件未被任何锁覆盖)")
            for lk_name, bound_sha in manifest_bound:
                if bound_sha != manifest_sha:
                    f_problems.append(f"锁 {lk_name} 绑定 manifest {bound_sha[:12]}…"
                                      f" 与当前 {manifest_sha[:12]}… 不一致")
            if not f_problems:
                f_ok = True
    extra.append(("freeze_gate", (f_ok, ("冻结证据绑定当前 manifest, eval/test 全量覆盖"
                  if f_ok else "; ".join(f_problems)[:200]))))
    # B2(BR4-b 剩余):资产验收证据——固定 smoke 只证明环境能运行,不能替代
    # 当前资产验收;证据必须绑定当前 manifest 且全量覆盖,缺失即 UNVERIFIED 阻断
    if mp is not None and mp.exists():
        ae_ok, ae_detail = check_asset_evidence(mp)
        extra.append(("asset_evidence", (ae_ok, ae_detail)))
    if args.ready and not args.run_id:
        print("[FAIL] --ready 需要 --run-id(运行快照是 ready 必需项)")
        return 1
    if args.ready and not args.manifest:
        print("[FAIL] --ready 需要 --manifest(数据门禁与哈希绑定是 ready 必需项)")
        return 1
    r = run_preflight(Path(args.model) if args.model else None, extra_checks=extra,
                      strict=args.strict, ready=args.ready)
    for c in r["checks"]:
        print(f"[{'PASS' if c['ok'] else 'FAIL'}] {c['check']}: {c['detail']}")
    if args.ready:
        print("结论:", "READY: 可生成可执行训练计划" if r["ready"]
              else "**NOT READY —— 禁止生成训练计划,先定位缺失项**")
    else:
        print("结论:", "全部通过,可以进入后续动作" if r["ok"]
              else "**存在 FAIL —— 禁止后续动作(训练/评测一律停止),先定位修复**")
    return r["exit_code"]


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
