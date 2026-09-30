"""生成 manifest:扫描目录、算 SHA256、按子目录推断 split(纯标准库)。

用法:
  python tools/make_manifest.py --dir data --out data/manifest.json \
      --name animation-data-v1 --source "数据来源说明" --license internal-generated

生成后请人工补全 source/license(扫描只能登记,不能替人确认真实来源)。
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.manifest import Manifest  # noqa: E402


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="要登记的数据目录")
    ap.add_argument("--out", required=True, help="manifest 输出路径")
    ap.add_argument("--name", default="animation-data", help="manifest 名称")
    ap.add_argument("--source", default="", help="来源说明(建议填写)")
    ap.add_argument("--license", default="", help="默认许可证(建议填写)")
    args = ap.parse_args(argv)

    data_dir = Path(args.dir)
    if not data_dir.is_dir():
        print(f"目录不存在: {data_dir}")
        return 1
    out = Path(args.out)
    if out.parent.resolve() != data_dir.resolve():
        print("[FAIL] --out 必须位于 --dir 根目录，entry.path 相对此目录")
        return 1
    if out.exists() or out.is_symlink():
        print(f"[FAIL] 清单已存在，拒绝覆盖: {out}；请使用新版本文件名")
        return 1
    from animtrain.scan import scan_dir  # noqa: E402
    m = scan_dir(data_dir)
    if not m.entries:
        print("[FAIL] 扫描目录为空，未生成清单")
        return 1
    m.name = args.name
    m.policy = ("数据门禁:未标注许可证/source 的条目进 quarantine;"
                "评测/测试与训练精确重叠零容忍")
    for e in m.entries:
        e.source = args.source
        e.license = args.license
    try:
        with out.open("x", encoding="utf-8") as handle:
            json.dump(m.to_dict(), handle, ensure_ascii=False, indent=2)
    except OSError as exc:
        print(f"[FAIL] 无法写入清单 {out}: {exc}")
        return 1
    print(f"manifest → {out}({len(m.entries)} 条;source/license 为命令行统一值,"
          "请按实际逐条复核)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
