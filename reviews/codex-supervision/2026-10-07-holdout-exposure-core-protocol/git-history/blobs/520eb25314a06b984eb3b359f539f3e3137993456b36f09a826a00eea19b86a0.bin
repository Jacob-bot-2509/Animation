"""Fill batch-6 scenes into the batch-6 builder template (dev-only)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCENES = ROOT / "reviews/2026-10-06-scene-standard-sweep/batch6-scenes.json"
TARGET = ROOT / "tools/build_batch6_scene_patches.py"


def main() -> int:
    scenes = json.loads(SCENES.read_text("utf-8"))
    text = TARGET.read_text("utf-8")
    block = "NEW_SCENES = " + json.dumps(scenes, ensure_ascii=False, indent=4) + "\n"
    text, n = re.subn(r"NEW_SCENES = \{.*?\n\}\n", block, text, count=1, flags=re.S)
    if n != 1:
        raise ValueError("replacement count: " + str(n))
    TARGET.write_text(text, encoding="utf-8", newline="\n")
    print("filled", len(scenes), "scenes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
