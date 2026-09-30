"""字段映射校验 CLI(只读,不重写原始数据)。

用法:
  python tools/check_fields.py --jsonl pool.jsonl \
      --required problem,solution,answer
退出码: 0 = 全部齐备;1 = 有缺失(缺失清单输出到 stdout 汇总 + 指定报告文件)。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.fields import check_jsonl  # noqa: E402
from animtrain.fs_guard import ensure_not_exists  # noqa: E402


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jsonl", required=True, help="要校验的 JSONL")
    ap.add_argument("--required", default="problem,solution,answer",
                    help="必填字段(逗号分隔)")
    ap.add_argument("--report", default="", help="缺失报告输出路径(可选)")
    ap.add_argument("--force", action="store_true", help="允许覆盖已存在报告")
    args = ap.parse_args(argv)

    required = [f.strip() for f in args.required.split(",") if f.strip()]
    if not required:
        ap.error("--required 至少需要一个字段名")
    source = Path(args.jsonl)
    report = Path(args.report) if args.report else None
    try:
        if report is not None:
            if (report.resolve() == source.resolve()
                    or (report.exists() and source.exists() and report.samefile(source))):
                print("[FAIL] 报告路径指向输入文件；--force 也不能覆盖输入")
                return 1
            ensure_not_exists(report, force=args.force)
        bad = check_jsonl(source, required)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"[FAIL] 输入或报告路径错误: {exc}")
        return 1
    print(f"必填字段 {required} | 缺失 {len(bad)} 行")
    for b in bad[:20]:
        print(f"  {b['sample_id']} (line {b['line']}): {b['reason']}")
    if len(bad) > 20:
        print(f"  …共 {len(bad)} 行,其余见报告文件")
    if report is not None:
        try:
            with report.open("w" if args.force else "x", encoding="utf-8") as handle:
                json.dump({"required": required, "bad": bad}, handle,
                          ensure_ascii=False, indent=2)
        except OSError as exc:
            print(f"[FAIL] 无法写入报告 {report}: {exc}")
            return 1
        print(f"报告 → {report}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
