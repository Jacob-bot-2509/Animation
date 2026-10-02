"""候选数据集入场 CLI(msg_152):convert / check / report。

用法:
  python tools/dataset_intake.py convert dataset_calc.json data/v1/raw/dataset_calc.jsonl [--force]
  python tools/dataset_intake.py check data/v1/raw/dataset_calc.jsonl [...]
  python tools/dataset_intake.py report data/v1/raw/*.jsonl --out DATASET_REVIEW.md [--force]

退出码: 0 = 干净;1 = problems(硬伤);2 = quarantine(候选待补齐)或参数错误。

规则: 原文件只读,转换产物写新文件(默认拒绝覆盖);convert 不做任何内容清洗。
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.dataset_intake import (  # noqa: E402
    check_intake_file, convert_array_to_jsonl, intake_report)
from animtrain.fs_guard import ensure_not_exists  # noqa: E402


def cmd_convert(args) -> int:
    src, dst = Path(args.src), Path(args.dst)
    try:
        result = convert_array_to_jsonl(src, dst, force=args.force)
    except (OSError, ValueError) as exc:
        print(f"[FAIL] 转换失败: {exc}")
        return 1
    print(f"转换 {result['n_records']} 条 → {result['dst']}(原文件 {src} 未动)")
    return 0


def cmd_check(args) -> int:
    r = intake_report(args.files)
    print(f"文件 {len(args.files)} | 条目 {r['n_records']} | "
          f"problems {len(r['problems'])} | quarantine {len(r['quarantines'])}"
          f" | status={r['status']}")
    for p in r["problems"]:
        print(f"  [FAIL] {p}")
    for q in r["quarantines"][:10]:
        print(f"  [QUARANTINE] {q}")
    if len(r["quarantines"]) > 10:
        print(f"  …quarantine 共 {len(r['quarantines'])} 条,汇总见 report")
    return r["exit_code"]


def _render_report(rep: dict) -> str:
    lines = ["# 候选数据集审查报告", "",
             f"> 生成日期: {date.today().isoformat()}。工具: tools/dataset_intake.py report。",
             "",
             f"## 总览",
             "",
             f"- 样本总数: {rep['n_records']}",
             f"- 状态: **{rep['status']}**(候选数据集,**不是已验收训练集**)",
             "- 含义: candidate = 存在 quarantine 待补齐;rejected = 存在硬伤;"
             "clean = 入场检查通过(正式验收仍需全链路,见报告下一步)。",
             ""]
    if rep["categories"]:
        lines += ["## 分类统计", ""]
        for c, n in sorted(rep["categories"].items(), key=lambda kv: -kv[1]):
            lines.append(f"- {c}: {n} 条")
        lines.append("")
    if rep["problems"]:
        lines += ["## 硬伤(problems,必须修复)", ""]
        for m in rep["problems"]:  # 硬伤逐条列出,保留完整 文件:行号 可定位
            lines.append(f"- **{m}**")
        lines.append("")
    if rep["quarantines"]:
        lines += ["## 待补齐(quarantine,candidate 语义)", ""]
        for reason, (count, _samples) in rep["quarantine_groups"].items():
            lines.append(f"- {reason}(×{count})")
        lines.append("")
    if rep["problems"] or rep["quarantines"]:
        lines += ["## 仍需用户确认的项", "",
                  "1. 硬伤清单的修复方案(以报告为准)",
                  "2. quarantine 项的补齐方案(许可证证据/元数据/LaTeX 修正等)",
                  ""]
    else:
        lines += ["## 下一步", "",
                  "- 入场检查已通过;进正式验收仍需全链路:"
                  "make_manifest → data_check → split → freeze → preflight --ready。",
                  "- clean 不代表训练就绪;真实数据验收以全链路结果为准。",
                  ""]
    return "\n".join(lines)


def cmd_report(args) -> int:
    rep = intake_report(args.files)
    for f, c in sorted(rep["categories"].items()):
        print(f"  {f}: {c} 条")
    print(f"样本 {rep['n_records']} | problems {len(rep['problems'])} | "
          f"quarantine {len(rep['quarantines'])} | status={rep['status']}")
    out = Path(args.out)
    try:
        if out.resolve() in {Path(f).resolve() for f in args.files}:
            raise ValueError("拒绝报告覆盖任一输入文件，--force 不能绕过输入保护")
        ensure_not_exists(out, force=args.force)
        out.write_text(_render_report(rep), encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"[FAIL] 无法写入报告 {out}: {exc}")
        return 2
    print(f"报告 → {out}")
    return rep["exit_code"]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="候选数据集入场:convert/check/report")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pc = sub.add_parser("convert", help="JSON 数组 → JSONL(原文件只读,不覆盖已有输出)")
    pc.add_argument("src")
    pc.add_argument("dst")
    pc.add_argument("--force", action="store_true", help="允许覆盖已存在输出")
    pc.set_defaults(fn=cmd_convert)
    pk = sub.add_parser("check", help="按入场契约检查 JSONL(数组/非 JSONL 直接拒绝)")
    pk.add_argument("files", nargs="+")
    pk.set_defaults(fn=cmd_check)
    pr = sub.add_parser("report", help="多文件汇总并生成 Markdown 审查报告")
    pr.add_argument("files", nargs="+")
    pr.add_argument("--out", required=True, help="报告输出路径")
    pr.add_argument("--force", action="store_true", help="允许覆盖已存在报告")
    pr.set_defaults(fn=cmd_report)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
