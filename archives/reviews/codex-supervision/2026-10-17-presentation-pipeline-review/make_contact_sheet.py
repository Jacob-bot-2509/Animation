"""把十题试点抽样帧拼成一张联系表(2 列 × 5 行)。"""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"D:\Animation-Model-Training")
PILOT = (ROOT / "reviews/data-prep/2026-10-17-submission/asset-evidence"
         "/presentation-pipeline/runs/render-pilot")
results = json.loads((PILOT / "results.json").read_text(encoding="utf-8"))
ids = [r["sample_id"] for r in results["packs"] if r.get("ok")]

CELL_W, CELL_H = 427, 260
COLS = 2
ROWS = (len(ids) + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * CELL_W, ROWS * CELL_H), "white")
draw = ImageDraw.Draw(sheet)
font_path = r"C:\Windows\Fonts\consola.ttf"
try:
    font = ImageFont.truetype(font_path, 15)
except OSError:
    font = ImageFont.load_default()

for i, sid in enumerate(ids):
    frame_files = sorted(PILOT.glob(f"{sid}-f*.png"))
    if not frame_files:
        continue
    img = Image.open(frame_files[len(frame_files) // 2]).convert("RGB")
    img.thumbnail((CELL_W - 10, CELL_H - 32))
    x = (i % COLS) * CELL_W + (CELL_W - img.width) // 2
    y = (i // COLS) * CELL_H + 24
    sheet.paste(img, (x, y))
    draw.text(((i % COLS) * CELL_W + 6, (i // COLS) * CELL_H + 4), sid, fill="black", font=font)

out = PILOT / "contact-sheet.png"
sheet.save(out)
print(out, sheet.size)
