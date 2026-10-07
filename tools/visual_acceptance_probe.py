"""Probe extracted frame PNG formats and normalize them to plain RGB if needed."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(r"D:\Animation-Model-Training")
OUT = ROOT / "reviews/2026-10-08-visual-acceptance"

def main():
    from PIL import Image
    frames = OUT / "frames"
    report = []
    for png in sorted(frames.glob("*.png")):
        with Image.open(png) as img:
            report.append({"id": png.stem, "mode": img.mode, "size": list(img.size),
                           "bytes": png.stat().st_size})
    odd = [r for r in report if r["mode"] not in ("RGB", "RGBA") or tuple(r["size"]) != (854, 480)]
    print(json.dumps({"total": len(report), "odd": odd,
                      "sample": report[:3]}, ensure_ascii=False))
    # Normalize every frame to 8-bit RGB JPEG companion (safe for any viewer).
    norm = OUT / "frames-jpg"
    norm.mkdir(exist_ok=True)
    n = 0
    for r in report:
        with Image.open(frames / (r["id"] + ".png")) as img:
            img.convert("RGB").save(norm / (r["id"] + ".jpg"), "JPEG", quality=92)
        n += 1
    print(json.dumps({"normalized_jpg": n}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main())
