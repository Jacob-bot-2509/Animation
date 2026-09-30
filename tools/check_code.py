"""代码门禁 CLI(只读,不重写原始数据)。

用法:
  python tools/check_code.py --code scene.py [--whitelist configs/api_whitelist.json]
  python tools/check_code.py --dir output/ --suffix .py [--whitelist ...]
退出码: 0 = 通过;1 = 有问题。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.code_gate import check_code_all, load_whitelist  # noqa: E402


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--code", help="单个代码文件")
    mode.add_argument("--dir", help="批量目录")
    ap.add_argument("--suffix", default=".py", help="批量后缀(默认 .py)")
    ap.add_argument("--whitelist", default=str(ROOT / "configs" / "api_whitelist.json"),
                    help="API 白名单 JSON(不存在则 API 检查如实跳过)")
    args = ap.parse_args(argv)

    try:
        wl = load_whitelist(Path(args.whitelist))
    except (OSError, ValueError) as exc:
        print(f"[FAIL] 无法读取白名单: {exc}")
        return 1
    files: list[Path] = []
    if args.code:
        files = [Path(args.code)]
    elif args.dir:
        files = sorted(Path(args.dir).rglob(f"*{args.suffix}"))
    else:
        ap.print_help()
        return 2

    if not files:
        print("[FAIL] 未找到待检查代码文件；请核对目录和后缀")
        return 1
    total_bad = 0
    for f in files:
        try:
            code = f.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            print(f"  [FAIL] {f.name}: 读取失败 {exc}")
            total_bad += 1
            continue
        r = check_code_all(code, wl)
        if r.get("unverified"):
            print(f"  [UNVERIFIED] {f.name}: {', '.join(r['unverified'])}")
        if r["ok"]:
            print(f"  [PASS:STATIC] {f.name}")
        else:
            total_bad += 1
            print(f"  [FAIL] {f.name}: {len(r['problems'])} 项")
            for p in r["problems"][:8]:
                print(f"      - {p}")
    print(f"结论: {len(files)} 个文件,{total_bad} 个有问题")
    return 1 if total_bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
