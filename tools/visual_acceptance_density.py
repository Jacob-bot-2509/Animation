"""Quantitative readability/density check for all 165 render frames.

For the forced vertical-stack layout, glyph size per formula is bounded by
content_bbox_height / unique_formulas (px per formula slot). Below ~12px slots
glyphs degrade to mush at 480p. Also flags records that waste horizontal space
(very narrow bbox) where a side-by-side layout would help most.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(r"D:\Animation-Model-Training")
OUT = ROOT / "reviews/2026-10-08-visual-acceptance"

def main():
    rows = [json.loads(ln) for ln in (OUT / "frame-metrics.jsonl").read_text(encoding="utf-8").splitlines() if ln.strip()]
    report = []
    for r in rows:
        bbox = r["bbox"]
        bw, bh = (bbox[2] - bbox[0]), (bbox[3] - bbox[1])
        slots = r["unique_formulas"] or 1
        report.append({
            "id": r["id"], "unique_formulas": r["unique_formulas"],
            "bbox_w": bw, "bbox_h": bh,
            "px_per_formula_slot": round(bh / slots, 1),
            "frame_width_usage": round(bw / 854, 3),
            "ink": r["ink"],
        })
    tiny = [x for x in report if x["px_per_formula_slot"] < 12]
    small = [x for x in report if 12 <= x["px_per_formula_slot"] < 20]
    ok = [x for x in report if x["px_per_formula_slot"] >= 20]
    # Narrow content = vertical stack of short formulas; side-by-side would help.
    narrow = [x for x in report if x["frame_width_usage"] < 0.5 and x["unique_formulas"] >= 10]
    summary = {
        "total": len(report),
        "readable_ok": len(ok),
        "small_12_20px": len(small),
        "tiny_under_12px": len(tiny),
        "tiny_list": sorted(x["id"] for x in tiny),
        "small_list": sorted(x["id"] for x in small),
        "narrow_waste_width": sorted(x["id"] for x in narrow),
        "ids_containing_020": sorted(x["id"] for x in report if "020" in x["id"]),
    }
    (OUT / "density-report.json").write_text(
        json.dumps({"summary": summary, "rows": report}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main())
