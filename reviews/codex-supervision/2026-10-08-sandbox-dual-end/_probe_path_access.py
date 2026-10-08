"""Read-only probe: report which workspace paths the confined tool layer can read/list.

Nothing is created, modified, or deleted. Safe to re-run at any time.
"""
import json
from pathlib import Path

ROOT = Path("D:/Animation-Model-Training")
TARGETS = [
    None, ".venv", ".venv/Scripts", ".venv/Scripts/python.exe",
    ".tools", ".models", "src", "tests", "tools", "reviews", "data",
    ".git", ".sandbox-runtime", ".render-tmp", ".render-pilot",
    "configs", "outputs", "runs", "holdout-sources", "docs",
]

out = {}
for t in TARGETS:
    p = ROOT / t if t else ROOT
    entry = {"path": str(p)}
    try:
        entry["exists"] = p.exists()
    except Exception as exc:
        entry["exists"] = f"ERR {type(exc).__name__}: {exc}"
    try:
        entry["is_dir"] = p.is_dir()
    except Exception as exc:
        entry["is_dir"] = f"ERR {type(exc).__name__}: {exc}"
    try:
        entry["listdir"] = len(list(p.iterdir())) if p.is_dir() else None
    except Exception as exc:
        entry["listdir"] = f"ERR {type(exc).__name__}: {exc}"
    try:
        entry["stat_bytes"] = p.stat().st_size if p.is_file() else None
    except Exception as exc:
        entry["stat_bytes"] = f"ERR {type(exc).__name__}: {exc}"
    out[t or "<root>"] = entry

print(json.dumps(out, ensure_ascii=False, indent=2))
