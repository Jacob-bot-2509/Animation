"""Extract final frames from the 165 qualified render videos for visual acceptance.

Reads the frozen qualified-records.jsonl (source of truth), verifies each mp4 SHA,
extracts the last frame, and records a brightness self-check (blank-frame guard).
Never writes into the frozen followup directory.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
import sys

ROOT = Path(r"D:\Animation-Model-Training")
FFMPEG = Path(r"D:\Settings\ffmpeg\bin\ffmpeg.exe")
QUALIFIED = ROOT / "reviews/codex-supervision/2026-10-08-real-formula-followup/qualified-records.jsonl"
OUT = ROOT / "reviews/2026-10-08-visual-acceptance"
FRAMES = OUT / "frames"
EXPECTED = 165


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def bright_fraction(png):
    from PIL import Image
    img = Image.open(png).convert("L")
    w, h = img.size
    px = img.load()
    bright = sum(1 for y in range(0, h, 2) for x in range(0, w, 2) if px[x, y] > 128)
    sampled = ((h + 1) // 2) * ((w + 1) // 2)
    return round(bright / sampled, 6)


def main():
    FRAMES.mkdir(parents=True, exist_ok=False)
    lines = [ln for ln in QUALIFIED.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if len(lines) != EXPECTED:
        raise SystemExit(f"expected {EXPECTED} rows, got {len(lines)}")
    rows = [json.loads(ln) for ln in lines]
    if len({r["id"] for r in rows}) != EXPECTED:
        raise SystemExit("duplicate record ids in qualified-records.jsonl")
    manifest = []
    for i, r in enumerate(rows, 1):
        mp4 = ROOT / r["mp4_path"]
        if not mp4.is_file():
            raise SystemExit(f"missing mp4: {r['id']} {mp4}")
        if sha256(mp4) != r["mp4_sha256"]:
            raise SystemExit(f"mp4 hash mismatch: {r['id']}")
        png = FRAMES / (r["id"] + ".png")
        # Scenes are static from t=0 (self.add then wait), so frame 1 shows the final layout.
        proc = subprocess.run(
            [str(FFMPEG), "-y", "-i", str(mp4), "-frames:v", "1", str(png)],
            capture_output=True)
        if proc.returncode != 0 or not png.is_file():
            raise SystemExit(f"ffmpeg failed {r['id']}: {proc.stderr[-400:]!r}")
        manifest.append({
            "id": r["id"], "unique_formulas": r["unique_formulas"],
            "mp4_sha256_verified": r["mp4_sha256"],
            "frame_path": png.relative_to(ROOT).as_posix(),
            "frame_sha256": sha256(png),
            "bright_fraction": bright_fraction(png),
        })
        if i % 20 == 0:
            print(json.dumps({"extracted": i}, ensure_ascii=False), flush=True)
    out = OUT / "frames-manifest.jsonl"
    out.write_text("\n".join(json.dumps(m, ensure_ascii=False) for m in manifest) + "\n", encoding="utf-8")
    blank = [m["id"] for m in manifest if m["bright_fraction"] < 0.001]
    print(json.dumps({"extracted": len(manifest), "near_blank": blank,
                      "manifest": out.relative_to(ROOT).as_posix()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
