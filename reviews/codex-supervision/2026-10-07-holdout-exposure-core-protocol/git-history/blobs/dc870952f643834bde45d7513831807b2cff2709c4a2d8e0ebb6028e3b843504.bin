"""运行记录 CLI:创建/校验运行记录(fail-fast,可重放)。

用法:
  python tools/run_record.py init --run-id r001 --kind dry-run \
      --config configs/x.json --manifest data/manifest.json \
      --command "python tools/data_check.py --dry-run"
  python tools/run_record.py check --run-id r001 [--manifest data/manifest.json]

init 自动捕获:git commit(HEAD)、config/manifest 文件 hash。
记录落盘 runs/<run_id>/run_record.json。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.fs_guard import ensure_not_exists, valid_run_id  # noqa: E402
from animtrain.run_record import RunRecord, check_record  # noqa: E402


def git_head() -> str:
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                             text=True, cwd=str(ROOT), encoding="utf-8")
        return out.stdout.strip() if out.returncode == 0 else "<no-git>"
    except OSError:
        return "<no-git>"


def capture_env() -> dict:
    import platform
    import sys as _sys
    env = {"python": _sys.version.split()[0], "platform": platform.platform()}
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total",
                              "--format=csv,noheader"], capture_output=True,
                             text=True, encoding="utf-8")
        env["gpu"] = out.stdout.strip() if out.returncode == 0 else "查询失败"
    except FileNotFoundError:
        env["gpu"] = "无 nvidia-smi"
    return env


def file_sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def cmd_init(args) -> int:
    if not valid_run_id(args.run_id):
        print(f"run_id 非法: {args.run_id!r}(只允许 [A-Za-z0-9_-] 1-64 字符,"
              "防路径穿越)")
        return 1
    config = {}
    if args.config:
        cp = Path(args.config)
        config = {"file": str(cp), "sha256": file_sha256(cp),
                  "content": json.loads(cp.read_text(encoding="utf-8"))}
    mhash = file_sha256(Path(args.manifest)) if args.manifest else ""
    r = RunRecord(run_id=args.run_id, kind=args.kind, config=config,
                  git_commit=git_head(), manifest_hash=mhash,
                  summary={"command": args.command,
                           "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                           "manifest": args.manifest or ""},
                  env=capture_env(),
                  metrics=json.loads(args.metrics) if args.metrics else {})
    out = ROOT / "runs" / args.run_id / "run_record.json"
    try:
        ensure_not_exists(out)  # R1: 已存在的记录拒绝覆盖(不可篡改)
    except ValueError as exc:
        print(f"拒绝: {exc}")
        return 1
    r.save(out)
    problems = check_record(r)
    print(f"记录 → {out.relative_to(ROOT)}(git {r.git_commit[:8]})")
    if problems:
        print("!! fail-fast 校验未过(请补全后重跑):")
        for p in problems:
            print(f"   - {p}")
        return 1
    return 0


def cmd_check(args) -> int:
    p = ROOT / "runs" / args.run_id / "run_record.json"
    if not p.exists():
        print(f"记录不存在: {p}")
        return 1
    r = RunRecord.load(p)
    mp = Path(args.manifest) if args.manifest else None
    problems = check_record(r, manifest_path=mp)
    if problems:
        print(f"记录 {args.run_id} 校验未过:")
        for x in problems:
            print(f"   - {x}")
        return 1
    print(f"记录 {args.run_id} 校验通过"
          f"(kind={r.kind}, git={r.git_commit[:8]}, metrics={r.metrics})")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p1 = sub.add_parser("init")
    p1.add_argument("--run-id", required=True)
    p1.add_argument("--kind", default="dry-run",
                    choices=["dry-run", "baseline", "improvement", "eval"])
    p1.add_argument("--config", default="")
    p1.add_argument("--manifest", default="")
    p1.add_argument("--command", default="", required=True)
    p1.add_argument("--metrics", default="")
    p1.set_defaults(fn=cmd_init)
    p2 = sub.add_parser("check")
    p2.add_argument("--run-id", required=True)
    p2.add_argument("--manifest", default="")
    p2.set_defaults(fn=cmd_check)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
