"""Read-only probe: map what the confined tool layer can read/list across the workspace.

Walks the project to depth 2 and reports a per-path status. Nothing is written.
"""
import json
import os
import sys
from pathlib import Path

ROOT = Path("D:/Animation-Model-Training")
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else None
SKIP = {".git", "__pycache__", ".pytest_cache"}

report = {"root": str(ROOT), "dirs": {}, "summary": {"ok": 0, "denied": 0, "missing": 0, "other": 0}}


def probe(rel: str) -> dict:
    p = Path(rel) if os.path.isabs(rel) else ROOT / rel
    entry = {"path": str(p)}
    try:
        st = p.stat()
        entry["stat"] = "ok"
        entry["isdir"] = p.is_dir()
    except Exception as exc:
        entry["stat"] = f"{type(exc).__name__}: {exc}"
        entry["isdir"] = None
    try:
        entry["entries"] = len(list(p.iterdir())) if entry["isdir"] else None
        entry["status"] = "ok"
    except Exception as exc:
        entry["entries"] = f"{type(exc).__name__}: {exc}"
        entry["status"] = "denied" if "Permission" in type(exc).__name__ else "other"
    return entry


for child in sorted(ROOT.iterdir(), key=lambda x: x.name.lower()):
    rel = child.name
    entry = probe(rel)
    report["dirs"][rel] = entry
    report["summary"][entry.get("status", "other")] = report["summary"].get(entry.get("status", "other"), 0) + 1
    if child.is_dir() and child.name not in SKIP:
        try:
            for grand in sorted(child.iterdir(), key=lambda x: x.name.lower()):
                if grand.name in SKIP:
                    continue
                sub = probe(str(Path(rel) / grand.name))
                report["dirs"][f"{rel}/{grand.name}"] = sub
                report["summary"][sub.get("status", "other")] = report["summary"].get(sub.get("status", "other"), 0) + 1
        except Exception:
            pass

if OUT is not None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"summary": report["summary"], "written": str(OUT),
                      "denied": {k: v.get("entries") for k, v in report["dirs"].items()
                                 if v.get("status") == "denied"}}, ensure_ascii=False))
else:
    print(json.dumps(report, ensure_ascii=False, indent=2))
