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
from animtrain.preflight import run_preflight  # noqa: E402
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
                  (rr["ok"], f"真实渲染证据: {rr['status']} — {rr['detail'][:120]}")))
    # math_gate: 真实数学断言(真命题)
    mr = math_check("Eq(2 + 2, 4)")
    extra.append(("math_gate",
                  (mr["ok"], f"真实数学断言: {mr['status']} — {mr['detail'][:120]}")))
    # freeze_gate: 发现并校验项目内的冻结锁;无冻结评测集时如实阻断
    from animtrain.freeze import check_frozen, discover_locks  # noqa: E402
    locks = discover_locks([ROOT / "data", ROOT], max_depth=2)
    if locks:
        problems = []
        for lk in locks:
            problems += check_frozen(lk)
        extra.append(("freeze_gate",
                      (not problems,
                       f"冻结锁 {len(locks)} 个{'全过' if not problems else '未过: ' + problems[0][:120]}")))
    else:
        extra.append(("freeze_gate", (False,
                      "无冻结评测集 —— 训练就绪前必须冻结 eval/test(BR4-b)")))
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
