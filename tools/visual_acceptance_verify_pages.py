"""Quantitative re-verification of the merged 633-page 4K delivery (v2).

v2 fixes the v1 flaws Codex named (msg_734):
- pages are paired to geometry entries BY ORDER, never by filename number;
- FORMULA_SEGMENT pages (partial viewport slices) are reported separately and
  excluded from slot statistics -- bbox height there is viewport framing, not
  formula size;
- every page row records its path + sha256 + the pairing rule;
- slot_px remains a LAYOUT OCCUPANCY PROXY and is explicitly not glyph
  certification (per-symbol review is Codex's lane).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(r"D:\Animation-Model-Training")
INDEX = ROOT / "reviews/codex-supervision/2026-10-08-glyph-review-followup/DELIVERY_INDEX.jsonl"
OUT = ROOT / "reviews/2026-10-08-visual-acceptance"
THRESH = 32
HD_SIZE = [3840, 2160]  # true 4K per delivery contract
SLOT_MIN = 24  # px per formula slot, FULL pages only (layout occupancy proxy)
ANALYSIS_SCALE = 2  # analyze at half resolution, scale bbox back by this factor


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def metrics(png):
    from PIL import Image
    src = Image.open(png).convert("L")
    w, h = src.size
    half = src.resize((w // ANALYSIS_SCALE, h // ANALYSIS_SCALE))
    pw, ph = half.size
    px = half.load()
    xs, ys, n = [], [], 0
    for y in range(ph):
        for x in range(pw):
            if px[x, y] > THRESH:
                xs.append(x); ys.append(y); n += 1
    if not n:
        return {"ink": 0, "bbox": None, "clipped": False, "size": [w, h]}
    minx, maxx, miny, maxy = (min(xs) * ANALYSIS_SCALE, max(xs) * ANALYSIS_SCALE,
                              min(ys) * ANALYSIS_SCALE, max(ys) * ANALYSIS_SCALE)
    clipped = minx <= 2 or maxx >= w - 3 or miny <= 2 or maxy >= h - 3
    return {"ink": n, "bbox": [minx, miny, maxx, maxy], "clipped": clipped, "size": [w, h]}


def main():
    rows = [json.loads(ln) for ln in INDEX.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(rows) == 165, f"expected 165 index rows, got {len(rows)}"
    pages, full_pages, seg_pages, issues, per_record, total_items = [], [], [], [], [], 0
    for r in rows:
        rid = r.get("id")
        frames = r.get("canonical_frames") or []
        geo_path = ROOT / r["geometry_path"]
        if not geo_path.is_file():
            issues.append({"id": rid, "issue": "geometry file missing"})
            continue
        if sha256(geo_path) != r["geometry_sha256"]:
            issues.append({"id": rid, "issue": "geometry sha mismatch"})
            continue
        geo = json.loads(geo_path.read_text(encoding="utf-8"))
        geo_pages = geo.get("pages") or []
        if len(geo_pages) != len(frames):
            issues.append({"id": rid, "issue": f"pages {len(geo_pages)} != frames {len(frames)}"})
            continue
        rec = {"id": rid, "pages": len(frames), "page_rows": []}
        for i, (geo_page, f) in enumerate(zip(geo_pages, frames)):
            png = ROOT / f["path"]
            if not png.is_file():
                issues.append({"id": rid, "page_index": i, "issue": "frame file missing"})
                continue
            if sha256(png) != f["sha256"]:
                issues.append({"id": rid, "page_index": i, "issue": "frame sha mismatch"})
                continue
            met = metrics(png)
            items = len(geo_page.get("items") or [])
            kind = geo_page.get("kind")
            bbox_h = (met["bbox"][3] - met["bbox"][1]) if met["bbox"] else 0
            slot = round(bbox_h / items, 1) if (kind == "FULL_FORMULAS" and items) else None
            row = {
                "page_order_index": i, "kind": kind, "path": f["path"],
                "frame_sha256": f["sha256"], "size": met["size"], "ink": met["ink"],
                "clipped": met["clipped"], "formulas_on_page": items, "slot_px_proxy": slot,
                "resolution_ok": met["size"] == HD_SIZE,
                "ink_ok": met["ink"] >= 200,
                "clipped_ok": not met["clipped"],
            }
            row["slot_ok"] = slot is None or slot >= SLOT_MIN
            row["all_ok"] = row["resolution_ok"] and row["slot_ok"] and row["ink_ok"] and row["clipped_ok"]
            if not row["all_ok"]:
                issues.append({"id": rid, "page_order_index": i, "issue": row})
            rec["page_rows"].append(row)
            (full_pages if kind == "FULL_FORMULAS" else seg_pages).append(row)
            pages.append(row)
        per_record.append(rec)
        total_items += sum(len(p.get("items") or []) for p in geo_pages)
    ok_pages = sum(p["all_ok"] for p in pages)
    sizes = sorted({tuple(p["size"]) for p in pages})
    slots = [p["slot_px_proxy"] for p in full_pages if p["slot_px_proxy"] is not None]
    summary = {
        "schema_version": 2,
        "records": len(per_record), "pages": len(pages),
        "full_pages": len(full_pages), "segment_pages": len(seg_pages),
        "geometry_items_total": total_items,
        "pages_all_ok": ok_pages, "pages_with_issues": len(pages) - ok_pages,
        "resolution_histogram": {f"{w}x{h}": sum(1 for p in pages if tuple(p["size"]) == (w, h))
                                 for w, h in sizes},
        "full_page_slot_proxy_min": min(slots) if slots else None,
        "full_page_slot_proxy_p10": sorted(slots)[len(slots) // 10] if slots else None,
        "full_page_slot_proxy_median": sorted(slots)[len(slots) // 2] if slots else None,
        "pairing_rule": "canonical_frames[i] <-> geometry pages[i], by order (never by filename)",
        "segment_pages_note": "FORMULA_SEGMENT pages are partial viewport slices; bbox is framing, not formula size -- excluded from slot stats",
        "slot_proxy_disclaimer": "slot_px_proxy is layout occupancy, NOT glyph-size certification; per-symbol review is separate (Codex lane)",
        "criteria": {"resolution_target": f"{HD_SIZE[0]}x{HD_SIZE[1]} (true 4K)", "slot_px_min": SLOT_MIN,
                     "coverage": "165 records, all pages sha-bound to frozen merged index (glyph-review-followup)"},
        "issues": issues[:20], "issue_count": len(issues),
    }
    (OUT / "readable-pages-verification-4k-v2.json").write_text(
        json.dumps({"summary": summary, "records": per_record}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main())
