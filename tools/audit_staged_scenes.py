"""Audit all staged scene outputs for control-char corruption (read-only)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SWEEP = ROOT / "reviews/2026-10-06-scene-standard-sweep"
CONTROL = set(chr(c) for c in range(0, 32)) - {"\t"}


def main() -> int:
    total_bad = 0
    for d in sorted(SWEEP.glob("batch*-staged-v1")):
        sel = d / "draft-selection.candidate.json"
        if not sel.exists():
            continue
        data = json.loads(sel.read_text("utf-8"))
        bad = []
        # staged selection 的 entries 指向各 batch 新文件;直接扫 candidate 目录里的 jsonl
        for f in sorted(d.glob("batch-*/*.jsonl")):
            for i, line in enumerate(f.read_text("utf-8").splitlines(), 1):
                if not line.strip():
                    continue
                rec = json.loads(line)
                scene = rec.get("scene_spec", {})
                for s in scene.get("objects", []) + scene.get("steps", []):
                    hits = [ch for ch in s if ch in CONTROL]
                    if hits:
                        bad.append((rec["id"], f.name, i, [repr(h) for h in hits[:3]]))
        print(d.name, "->", "CORRUPT " + str(len(bad)) if bad else "clean")
        for b in bad[:6]:
            print("   ", b)
        total_bad += len(bad)
    print("total corrupt entries:", total_bad)
    return 1 if total_bad else 0


if __name__ == "__main__":
    sys.exit(main())
