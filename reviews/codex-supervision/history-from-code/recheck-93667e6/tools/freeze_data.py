"""冻结数据 CLI(B3):把 eval/test 数据集冻结进锁,之后不可修改。

用法:
  python tools/freeze_data.py --files eval/eval.jsonl test/test.jsonl \\
      --lock data/v1/frozen.lock.json --name eval-test-v1
  python tools/freeze_data.py --check data/v1/frozen.lock.json

退出码: 0 = 冻结完好;1 = 有变化/错误。
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.freeze import check_frozen, freeze_set  # noqa: E402


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--files", nargs="+", help="要冻结的数据文件(空格分隔)")
    ap.add_argument("--lock", help="锁文件路径")
    ap.add_argument("--name", default="", help="冻结集名称")
    ap.add_argument("--manifest", default="",
                    help="绑定当前 manifest(BR4-b:manifest sha256 写入锁 meta)")
    ap.add_argument("--check", help="校验指定锁文件")
    args = ap.parse_args(argv)

    if args.check:
        problems = check_frozen(Path(args.check))
        if not problems and args.manifest:
            # msg_253:--check 增加 manifest 绑定校验(此前只核验样本数据)
            import hashlib as _h2  # noqa: PLC0415
            import json as _j2  # noqa: PLC0415
            mp = Path(args.manifest)
            if mp.exists():
                actual = _h2.sha256(mp.read_bytes()).hexdigest()
                bound = None
                try:
                    bound = (_j2.loads(Path(args.check).read_text(encoding="utf-8"))
                             .get("meta", {}).get("manifest_sha256"))
                except (OSError, ValueError):
                    bound = None
                if bound != actual:
                    problems.append(
                        f"manifest 绑定不一致:锁绑定 {str(bound)[:12]}…,"
                        f"当前 manifest {actual[:12]}…")
        if problems:
            print(f"冻结校验未过({len(problems)} 项):")
            for p in problems:
                print(f"  - {p}")
            return 1
        print("冻结完好")
        return 0

    if not args.files or not args.lock:
        ap.error("--files 与 --lock 必填(或使用 --check)")
    import hashlib as _h  # noqa: PLC0415
    meta = {"name": args.name}
    if args.manifest:
        mp = Path(args.manifest)
        meta["manifest_sha256"] = _h.sha256(mp.read_bytes()).hexdigest()
    try:
        lock = freeze_set([Path(f) for f in args.files], Path(args.lock),
                          meta=meta)
    except ValueError as exc:
        print(f"[FAIL] {exc}")
        return 1
    print(f"已冻结 {lock['n_files']} 个文件 → {args.lock}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
