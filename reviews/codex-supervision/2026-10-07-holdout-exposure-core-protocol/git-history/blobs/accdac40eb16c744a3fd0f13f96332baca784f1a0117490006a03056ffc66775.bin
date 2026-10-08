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

from animtrain.fs_guard import ensure_not_exists  # noqa: E402
from animtrain.manifest import Manifest  # noqa: E402


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True, help="要登记的数据目录")
    ap.add_argument("--out", required=True, help="manifest 输出路径")
    ap.add_argument("--name", default="animation-data", help="manifest 名称")
    ap.add_argument("--source", default="", help="来源说明(建议填写)")
    ap.add_argument("--license", default="", help="默认许可证(建议填写)")
    args = ap.parse_args()

    data_dir = Path(args.dir)
    if not data_dir.is_dir():
        print(f"目录不存在: {data_dir}")
        return 1
    from animtrain.scan import scan_dir  # noqa: E402
    m = scan_dir(data_dir)
    m.name = args.name
    m.policy = ("数据门禁:未标注许可证/source 的条目进 quarantine;"
                "评测/测试与训练精确重叠零容忍")
    for e in m.entries:
        e.source = args.source
        e.license = args.license
    out = Path(args.out)
    ensure_not_exists(out, force=args.force)
    out.parent.mkdir(parents=True, exist_ok=True)
    m.save(out)
    print(f"manifest → {out}({len(m.entries)} 条;source/license 为命令行统一值,"
          "请按实际逐条复核)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
