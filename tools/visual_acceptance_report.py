"""Emit the visual acceptance report from manifest + metrics.

Honest scope: this is author-side STRUCTURAL acceptance (content present, centered,
not clipped). Human visual review of glyphs is PENDING and explicitly not claimed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(r"D:\Animation-Model-Training")
OUT = ROOT / "reviews/2026-10-08-visual-acceptance"
TINY = {"draft-c01-03", "draft-c18-02", "prob-040"}

def main():
    manifest = [json.loads(ln) for ln in (OUT / "frames-manifest.jsonl").read_text(encoding="utf-8").splitlines() if ln.strip()]
    metrics = {r["id"]: r for r in (json.loads(ln) for ln in (OUT / "frame-metrics.jsonl").read_text(encoding="utf-8").splitlines() if ln.strip())}
    assert set(metrics) == {m["id"] for m in manifest} == {m["id"] for m in manifest} and len(manifest) == 165

    rows = []
    for m in manifest:
        met = metrics[m["id"]]
        ok = met["ink"] >= 200 and not met["clipped"] and met["rows"] >= 1
        note = "tiny_scale_zoom_recommended" if m["id"] in TINY else None
        rows.append({
            "id": m["id"], "unique_formulas": m["unique_formulas"],
            "frame_sha256": m["frame_sha256"], "mp4_sha256_verified": m["mp4_sha256_verified"],
            "frame_path": m["frame_path"], "ink_pixels_gt32": met["ink"],
            "content_bbox": met["bbox"], "row_bands_24px": met["rows"],
            "edge_clipped": met["clipped"], "review_note": note,
            "structural_verdict": "PASS_STRUCTURAL_LAYOUT" if ok else "FAIL_STRUCTURAL_LAYOUT",
        })
    passed = sum(r["structural_verdict"] == "PASS_STRUCTURAL_LAYOUT" for r in rows)
    report = {
        "schema": "visual-acceptance-author-structural-v1",
        "source_of_truth": "reviews/codex-supervision/2026-10-08-real-formula-followup/qualified-records.jsonl",
        "frames_manifest_sha256": None,  # filled below
        "method": {
            "frame_extraction": "first frame of each qualified mp4 (static scene from t=0)",
            "ink_threshold": 32, "metrics": ["ink_pixels", "content_bbox", "24px_row_bands",
                                             "edge_clip", "centroid"],
            "limitations": [
                "No image-capable reviewer in this environment; glyph-level checks are NOT claimed.",
                "Small text (dominant wide formula) reduces readability at 480p for 3 records.",
                "Author-side evidence only; independent human visual review still PENDING.",
            ],
        },
        "summary": {"total": len(rows), "structural_pass": passed,
                    "structural_fail": len(rows) - passed,
                    "tiny_scale_flags": sorted(TINY),
                    "human_visual_review": "PENDING"},
        "records": rows,
    }
    import hashlib
    raw = (OUT / "frames-manifest.jsonl").read_bytes()
    report["frames_manifest_sha256"] = hashlib.sha256(raw).hexdigest()
    (OUT / "visual-acceptance-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report["summary"], ensure_ascii=False))
    return 0 if passed == len(rows) else 3

if __name__ == "__main__":
    sys.exit(main())
