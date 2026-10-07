"""Structural/layout analysis of extracted frames + diagnosis of near-blank suspects.

No human vision available in this environment, so visual acceptance is decomposed into:
- per-frame content metrics (ink, bounding box, row profile, edge-clip check)
- per-video frame-by-frame profiling for suspects (is frame 1 black but later frames lit?)
- contact sheets for the human reviewer to eyeball locally.
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
import sys

ROOT = Path(r"D:\Animation-Model-Training")
FFMPEG = Path(r"D:\Settings\ffmpeg\bin\ffmpeg.exe")
OUT = ROOT / "reviews/2026-10-08-visual-acceptance"
FRAMES = OUT / "frames"
MANIFEST = OUT / "frames-manifest.jsonl"
THRESH = 32


def metrics(png):
    from PIL import Image
    img = Image.open(png).convert("L")
    w, h = img.size
    px = img.load()
    xs, ys, n = [], [], 0
    for y in range(h):
        for x in range(w):
            if px[x, y] > THRESH:
                xs.append(x); ys.append(y); n += 1
    if not n:
        return {"ink": 0, "bbox": None, "rows": 0, "clipped": False, "cx": None, "cy": None}
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    bands = {}
    for y in ys:
        bands[y // 24] = bands.get(y // 24, 0) + 1
    rows = sum(1 for c in bands.values() if c >= 20)
    clipped = minx <= 1 or maxx >= w - 2 or miny <= 1 or maxy >= h - 2
    return {"ink": n, "bbox": [minx, miny, maxx, maxy], "rows": rows,
            "clipped": clipped, "cx": (minx + maxx) / 2 / w, "cy": (miny + maxy) / 2 / h}


def main():
    manifest = [json.loads(ln) for ln in MANIFEST.read_text(encoding="utf-8").splitlines() if ln.strip()]
    by_id = {m["id"]: m for m in manifest}

    # 1. Per-frame metrics for all 165.
    rows = []
    for m in manifest:
        png = ROOT / m["frame_path"]
        met = metrics(png)
        rows.append({"id": m["id"], "unique_formulas": m["unique_formulas"], **met})
    (OUT / "frame-metrics.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")

    suspects = [r for r in rows if r["ink"] < 200]
    print(json.dumps({"analyzed": len(rows),
                      "low_ink": [{"id": r["id"], "ink": r["ink"], "rows": r["rows"]} for r in suspects]},
                     ensure_ascii=False))

    # 2. Frame-by-frame profile for the suspects' videos.
    for r in suspects:
        mp4 = ROOT / by_id[r["id"]]["mp4_path"]
        work = OUT / "suspect" / r["id"]
        work.mkdir(parents=True, exist_ok=True)
        proc = subprocess.run([str(FFMPEG), "-y", "-i", str(mp4), str(work / "f%02d.png")],
                              capture_output=True)
        frames = sorted(work.glob("f*.png"))
        prof = [{"frame": p.name, "metrics": metrics(p)} for p in frames]
        print(json.dumps({"id": r["id"], "frames": len(frames), "profile": prof}, ensure_ascii=False))

    # 3. Contact sheets (4x3, labeled) for human review.
    sheets = OUT / "contact-sheets"
    sheets.mkdir(exist_ok=True)
    from PIL import Image, ImageDraw
    cell_w, cell_h, cols, per = 854, 480, 4, 12
    for page in range((len(manifest) + per - 1) // per):
        canvas = Image.new("RGB", (cols * cell_w, (per // cols) * cell_h), (8, 8, 8))
        draw = ImageDraw.Draw(canvas)
        for slot in range(per):
            idx = page * per + slot
            if idx >= len(manifest):
                break
            m = manifest[idx]
            img = Image.open(ROOT / m["frame_path"]).convert("RGB")
            canvas.paste(img, ((slot % cols) * cell_w, (slot // cols) * cell_h))
            draw.rectangle([(slot % cols) * cell_w, (slot // cols) * cell_h,
                            (slot % cols) * cell_w + cell_w - 1, (slot // cols) * cell_h + cell_h - 1],
                           outline=(200, 200, 0), width=2)
            draw.text(((slot % cols) * cell_w + 4, (slot // cols) * cell_h + 2),
                      m["id"], fill=(0, 255, 0))
        canvas.save(sheets / f"sheet-{page + 1:02d}.png")
    print(json.dumps({"contact_sheets": len(list(sheets.glob("*.png")))}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
