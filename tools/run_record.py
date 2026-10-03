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
from animtrain.run_record import RunRecord, check_record, verify_replay  # noqa: E402


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


# B1: 项目目录内约定目录(虚拟环境/审查证据)不计入 dirty 变更
_DIRTY_EXCLUDE = (".venv", ".git", "reviews")


def git_dirty() -> dict:
    """git dirty 状态:明确记录 clean 或变更清单(排除约定目录)。"""
    try:
        out = subprocess.run(
            ["git", "status", "--porcelain", "--untracked-files=normal"],
            capture_output=True, text=True, cwd=str(ROOT), encoding="utf-8")
    except OSError:
        return {"clean": None, "error": "git 不可用", "changed": []}
    if out.returncode != 0:
        return {"clean": None, "error": out.stderr.strip()[:200], "changed": []}
    changed = []
    for line in out.stdout.splitlines():
        path = line[3:].strip().strip('"').replace("\\", "/")
        if path.startswith(_DIRTY_EXCLUDE):
            continue
        changed.append(path)
    return {"clean": not changed, "changed": changed}


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
                  metrics=json.loads(args.metrics) if args.metrics else {},
                  seed=args.seed, dirty=git_dirty())
    out = ROOT / "runs" / args.run_id / "run_record.json"
    # 复审 R8:先校验后落盘 —— 校验未过不得占 run_id、不得留下记录
    mp = Path(args.manifest) if args.manifest else None
    problems = check_record(r, manifest_path=mp)
    if problems:
        print("!! fail-fast 校验未过(不落盘):")
        for p in problems:
            print(f"   - {p}")
        return 1
    try:
        ensure_not_exists(out)  # R1: 已存在的记录拒绝覆盖(不可篡改)
    except ValueError as exc:
        print(f"拒绝: {exc}")
        return 1
    r.save(out)
    print(f"记录 → {out.relative_to(ROOT)}(git {r.git_commit[:8]})")
    return 0


def cmd_check(args) -> int:
    if not valid_run_id(args.run_id):
        print(f"run_id 非法: {args.run_id!r}(只允许 [A-Za-z0-9_-])")
        return 1
    p = ROOT / "runs" / args.run_id / "run_record.json"
    if not p.exists():
        print(f"记录不存在: {p}")
        return 1
    r = RunRecord.load(p)
    # manifest 路径语义:显式 --manifest 优先;否则用记录内的 summary.manifest
    # (相对项目根);记录里有 hash 但既无显式路径也无记录路径 → 无法复验,报错
    if args.manifest:
        mp = Path(args.manifest)
    elif r.summary.get("manifest"):
        mp = ROOT / r.summary["manifest"]
    else:
        mp = None
        if r.manifest_hash:
            print("!! 记录 manifest_hash 非空但既无 --manifest 也无记录内路径,"
                  "无法复验")
            return 1
    problems = check_record(r, manifest_path=mp)
    if problems:
        print(f"记录 {args.run_id} 校验未过:")
        for x in problems:
            print(f"   - {x}")
        return 1
    print(f"记录 {args.run_id} 校验通过"
          f"(kind={r.kind}, git={r.git_commit[:8]}, metrics={r.metrics})")
    return 0


def cmd_verify(args) -> int:
    """B1:完整重放校验 —— git commit/dirty/config 哈希/manifest 哈希对照当前状态。"""
    if not valid_run_id(args.run_id):
        print(f"run_id 非法: {args.run_id!r}(只允许 [A-Za-z0-9_-])")
        return 1
    p = ROOT / "runs" / args.run_id / "run_record.json"
    if not p.exists():
        print(f"记录不存在: {p}")
        return 1
    r = RunRecord.load(p)
    if args.manifest:
        mp = Path(args.manifest)
    elif r.summary.get("manifest"):
        mp = ROOT / r.summary["manifest"]
    else:
        mp = None
    cp = None
    if args.config:
        cp = Path(args.config)
    elif isinstance(r.config, dict) and r.config.get("file"):
        cp = Path(r.config["file"])
    problems = verify_replay(r, manifest_path=mp,
                             git_commit_now=git_head(), dirty_now=git_dirty(),
                             config_path=cp)
    if problems:
        print(f"记录 {args.run_id} 不可重放:")
        for x in problems:
            print(f"   - {x}")
        return 1
    print(f"记录 {args.run_id} 完整可重放(git={r.git_commit[:8]},"
          f"config_hash={ (r.config or {}).get('sha256', '')[:12] if isinstance(r.config, dict) else ''}…)")
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
    p1.add_argument("--seed", type=int, default=None,
                    help="随机种子(B1:baseline/improvement 必填)")
    p1.set_defaults(fn=cmd_init)
    p2 = sub.add_parser("check")
    p2.add_argument("--run-id", required=True)
    p2.add_argument("--manifest", default="")
    p2.set_defaults(fn=cmd_check)
    p3 = sub.add_parser("verify", help="B1:完整重放校验(git/config/manifest 对照)")
    p3.add_argument("--run-id", required=True)
    p3.add_argument("--manifest", default="")
    p3.add_argument("--config", default="", help="配置文件(缺省用记录内 file)")
    p3.set_defaults(fn=cmd_verify)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
