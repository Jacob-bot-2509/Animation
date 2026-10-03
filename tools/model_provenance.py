"""模型 provenance 记录(纯标准库):下载完成后生成 .models/<name>/PROVENANCE.json。

记录:来源 URL、许可证、下载时间、git 元数据、文件清单与关键文件 SHA256
(config/tokenizer/safetensors/LICENSE)。只读模型目录,不训练、不加载权重。
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


def file_sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", required=True, help="模型目录(如 .models/qwen3-4b)")
    ap.add_argument("--source", required=True, help="来源 URL")
    ap.add_argument("--license", default="Apache-2.0")
    ap.add_argument("--force", action="store_true", help="覆盖既有 PROVENANCE.json")
    args = ap.parse_args(argv)

    d = Path(args.model_dir)
    if not d.is_dir():
        print(f"[FAIL] 模型目录不存在: {d}")
        return 1
    files = sorted(p.relative_to(d) for p in d.rglob("*") if p.is_file())
    if not files:
        print("[FAIL] 目录为空,不生成 provenance")
        return 1
    git_meta = {}
    try:
        out = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True,
                             text=True, cwd=str(d), encoding="utf-8")
        git_meta["commit"] = out.stdout.strip() if out.returncode == 0 else ""
    except OSError:
        git_meta["commit"] = ""
    prov = {
        "provenance_version": 1,
        "model_dir": str(d),
        "source": args.source,
        "license": args.license,
        "downloaded_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "git_commit": git_meta.get("commit", ""),
        "n_files": len(files),
        "total_bytes": sum((d / f).stat().st_size for f in files),
        "key_files": {str(f): file_sha256(d / f)
                      for f in files if f.name in KEY_FILES},
        "weight_files": [{"file": str(f), "size": (d / f).stat().st_size,
                          "sha256": file_sha256(d / f)}
                         for f in files if f.suffix in (".safetensors", ".bin")],
    }
    out_path = d / "PROVENANCE.json"
    try:
        ensure_not_exists(out_path, force=args.force)
    except ValueError as exc:
        print(f"[FAIL] {exc}")
        return 1
    out_path.write_text(json.dumps(prov, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    print(f"PROVENANCE → {out_path}({len(files)} 文件,"
          f"{prov['total_bytes'] / 1e9:.2f} GB,权重文件 {len(prov['weight_files'])} 个)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
