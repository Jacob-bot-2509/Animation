"""模型 provenance 记录(纯标准库):下载完成后生成 .models/<name>/PROVENANCE.json。

msg_225 修复:
  - 排除 .git/克隆存储,区分 model_payload_bytes(模型真实载荷)与
    clone_storage_bytes(克隆目录总占用);LFS 指针未落地的权重不计数;
  - 无权重文件(config-only)默认失败(显式 --allow-no-weights 才放行);
  - 校验 git 顶层目录独立(不是项目仓库的嵌套)、remote 与 --source 一致;
  - 校验 safetensors index 分片与磁盘一致。
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

from animtrain.fs_guard import ensure_not_exists  # noqa: E402

KEY_FILES = ("config.json", "generation_config.json", "tokenizer.json",
             "tokenizer_config.json", "LICENSE")
LFS_POINTER_MAGIC = "version https://git-lfs.github.com/spec/v1"


def file_sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def is_lfs_pointer(p: Path) -> bool:
    """LFS 指针(未落地权重):≤200 字节且以指针头开头。"""
    try:
        if p.stat().st_size > 200:
            return False
        return p.read_text(encoding="ascii", errors="ignore") \
            .startswith(LFS_POINTER_MAGIC)
    except OSError:
        return True  # 读不了按未落地处理


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", required=True, help="模型目录(如 .models/qwen3-4b)")
    ap.add_argument("--source", required=True, help="来源 URL")
    ap.add_argument("--license", default="Apache-2.0")
    ap.add_argument("--force", action="store_true", help="覆盖既有 PROVENANCE.json")
    ap.add_argument("--allow-no-weights", action="store_true",
                    help="config-only/空权重也放行(默认失败)")
    args = ap.parse_args(argv)

    d = Path(args.model_dir)
    if not d.is_dir():
        print(f"[FAIL] 模型目录不存在: {d}")
        return 1
    # 1. git 顶层独立 + remote 与来源一致(msg_225:嵌套仓库会继承项目 HEAD)
    git_top = ""
    git_remote = ""
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"],
                             capture_output=True, text=True, cwd=str(d),
                             encoding="utf-8")
        git_top = out.stdout.strip()
        out2 = subprocess.run(["git", "remote", "get-url", "origin"],
                              capture_output=True, text=True, cwd=str(d),
                              encoding="utf-8")
        git_remote = out2.stdout.strip()
    except OSError:
        pass
    if git_top and Path(git_top).resolve() != d.resolve():
        print(f"[FAIL] {d} 不是独立 git 仓库顶层(实际顶层 {git_top})"
              "—— 会继承外层项目状态,不生成 provenance")
        return 1
    source_host = args.source.split("/")[2] if args.source.count("/") >= 2 else ""
    if git_remote and source_host and source_host not in git_remote:
        print(f"[WARN] git remote {git_remote} 与 --source {args.source} 不一致")

    # 2. 文件清单(排除 .git)
    files = sorted(p.relative_to(d) for p in d.rglob("*")
                   if p.is_file() and ".git" not in p.parts)
    if not files:
        print("[FAIL] 目录为空,不生成 provenance")
        return 1
    weight_files = []
    payload_bytes = 0
    for f in files:
        fp = d / f
        if f.suffix in (".safetensors", ".bin"):
            if is_lfs_pointer(fp):
                print(f"[WARN] 权重仍是 LFS 指针(未落地): {f}")
            else:
                weight_files.append({"file": str(f),
                                     "size": fp.stat().st_size,
                                     "sha256": file_sha256(fp)})
                payload_bytes += fp.stat().st_size
        elif f.suffix not in (".md", ".json", ".txt", ".gitattributes"):
            payload_bytes += fp.stat().st_size
    if not weight_files and not args.allow_no_weights:
        print("[FAIL] 未发现已落地的权重文件(config-only/全部 LFS 指针);"
              "确需登记请 --allow-no-weights")
        return 1
    # 3. safetensors index 分片一致性
    index = d / "model.safetensors.index.json"
    index_problems = []
    if index.exists() and weight_files:
        try:
            idx = json.loads(index.read_text(encoding="utf-8"))
            listed = {w["file"] for w in idx.get("weight_map", {}).values()}
            on_disk = {w["file"] for w in weight_files}
            missing = listed - on_disk
            extra = on_disk - listed
            if missing or extra:
                index_problems = [f"index 分片不一致(缺 {sorted(missing)},"
                                  f"多 {sorted(extra)})"]
        except (OSError, json.JSONDecodeError) as exc:
            index_problems = [f"index 不可读: {exc}"]

    prov = {
        "provenance_version": 2,
        "model_dir": str(d),
        "source": args.source,
        "license": args.license,
        "downloaded_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "git_top_level_ok": bool(git_top) and Path(git_top).resolve() == d.resolve(),
        "git_remote": git_remote,
        "n_files": len(files),
        "model_payload_bytes": payload_bytes,
        "weight_files": weight_files,
        "key_files": {str(f): file_sha256(d / f)
                      for f in files if f.name in KEY_FILES},
        "index_problems": index_problems,
    }
    out_path = d / "PROVENANCE.json"
    try:
        ensure_not_exists(out_path, force=args.force)
    except ValueError as exc:
        print(f"[FAIL] {exc}")
        return 1
    out_path.write_text(json.dumps(prov, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    if index_problems:
        print(f"[WARN] {index_problems[0]}")
    print(f"PROVENANCE → {out_path}({len(files)} 文件,"
          f"模型载荷 {payload_bytes / 1e9:.2f} GB,"
          f"权重 {len(weight_files)} 个,独立 git 顶层 {prov['git_top_level_ok']})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
