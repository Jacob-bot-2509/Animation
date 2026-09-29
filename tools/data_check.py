"""数据检查 CLI(dry-run 数据校验,不训练)。

用法:
  python tools/data_check.py --manifest data/manifest.json   # 校验指定 manifest
  python tools/data_check.py --scan data                      # 扫描目录临时登记并校验
  python tools/data_check.py --dry-run                        # 骨架自检(无数据时)

退出码: 0 = 通过(或仅 quarantine);1 = 有问题。

独立项目:纯标准库,不依赖 D:\\code 任何内容。
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.manifest import Entry, Manifest, sha256_text  # noqa: E402
from animtrain.scan import scan_dir  # noqa: E402
from animtrain.validate import validate_manifest  # noqa: E402





def dry_run() -> dict:
    """骨架自检:无数据时验证代码路径可用,打印 schema 说明。"""
    return {"dry_run": True, "skeleton": "ok",
            "schema": "manifest v1: name/version/generated_at/policy/entries[];"
                      "entry: path/sha256/size/source/license/split/notes",
            "checks": ["文件存在", "SHA256 一致", "许可证白名单(空=quarantine)",
                       "split 合法性", "评测/测试与训练精确重叠(零容忍)"],
            "note": "尚无数据,自检通过 = 骨架就绪;数据就位后先 make_manifest 再 data_check"}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", help="校验指定 manifest 文件")
    ap.add_argument("--scan", help="扫描目录并临时登记校验(目录路径)")
    ap.add_argument("--dry-run", action="store_true", help="骨架自检")
    args = ap.parse_args(argv)

    if args.dry_run:
        print(dry_run()["skeleton"], "|", dry_run()["schema"])
        for c in dry_run()["checks"]:
            print("  -", c)
        return 0

    if args.scan:
        d = Path(args.scan)
        m = scan_dir(d)
        report = validate_manifest(m, d)
        return _print_report(report)

    if args.manifest:
        mp = Path(args.manifest)
        m = Manifest.load(mp)
        report = validate_manifest(m, mp.parent)
        return _print_report(report)

    ap.print_help()
    return 2


def _print_report(report: dict) -> int:
    print(f"条目 {report['n_entries']} | "
          f"问题 {len(report['problems'])} | quarantine {len(report['quarantines'])}")
    for p in report["problems"]:
        print(f"  [FAIL] {p}")
    for q in report["quarantines"]:
        print(f"  [QUARANTINE] {q}")
    print("结论:", "通过" if report["ok"] else "**不通过**")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
