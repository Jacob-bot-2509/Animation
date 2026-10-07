"""Summarize frame metrics: row/formula consistency, clip flags, suspects detail."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(r"D:\Animation-Model-Training")
OUT = ROOT / "reviews/2026-10-08-visual-acceptance"

def main():
    rows = [json.loads(ln) for ln in (OUT / "frame-metrics.jsonl").read_text(encoding="utf-8").splitlines() if ln.strip()]
    suspects = ["draft-c01-03", "draft-c18-02", "prob-040"]
    detail = [{"id": r["id"], "unique_formulas": r["unique_formulas"], "ink_gt32": r["ink"],
               "bbox": r["bbox"], "rows_24px_bands": r["rows"], "clipped": r["clipped"]}
              for r in rows if r["id"] in suspects]
    clipped = [r["id"] for r in rows if r["clipped"]]
    # Row bands vs unique formulas: flag frames whose band count is oddly low relative
    # to the record's formula count (possible stacking/overlap collapse at 480p).
    low_rows = [{"id": r["id"], "unique_formulas": r["unique_formulas"], "rows": r["rows"],
                 "ink": r["ink"]} for r in rows
                if r["unique_formulas"] >= 20 and r["rows"] <= max(4, r["unique_formulas"] // 4)]
    cx = [r for r in rows if not (0.30 <= r["cx"] <= 0.70) or not (0.30 <= r["cy"] <= 0.70)]
    stats = {"total": len(rows), "clipped_edge": clipped,
             "off_center": [{"id": r["id"], "cx": round(r["cx"], 3), "cy": round(r["cy"], 3)} for r in cx],
             "low_row_bands": low_rows, "suspect_detail": detail}
    (OUT / "frame-summary.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(stats, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main())
