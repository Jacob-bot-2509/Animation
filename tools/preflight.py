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

    extra: list[tuple[str, tuple[bool, str]]] = []
    if args.run_id:
        from animtrain.run_record import RunRecord, check_record  # noqa: E402
        rp = ROOT / "runs" / args.run_id / "run_record.json"
        if rp.exists():
            rec = RunRecord.load(rp)
            problems = check_record(rec)
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
        else:
            extra.append(("data_manifest", (False, f"manifest 不存在: {mp}")))

    if args.ready and not args.run_id:
        print("[FAIL] --ready 需要 --run-id(运行快照是 ready 必需项)")
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
