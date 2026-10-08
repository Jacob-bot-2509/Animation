"""Exact, version-bound local formula-page layout evidence; never glyph certification."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np
from PIL import Image
import core_signatures as core

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "reviews/codex-supervision/2026-10-08-glyph-review-followup/DELIVERY_INDEX.jsonl"
INDEX_SHA = "07b4543d38599e1c30d2b515e0c2a8761e5611f771c46c75ee23b357c58b6331"
HD_SIZE = (3840, 2160)
THRESH = 32
SLOT_MIN = 24
FORMULA_INK_MIN = 200
VIEWPORT = (271, 1889, 136, 3704)
METHOD = {
    "pixels": "Native RGB; no resizing or grayscale conversion.",
    "formula_region_zero_based_half_open": {"rows": [271, 1889], "columns": [136, 3704]},
    "ink": "Any RGB channel >32; formula ink is counted only inside the formula region.",
    "bbox": "Inclusive occupied formula-region bbox height: max_y-min_y+1.",
    "slot": "FULL_FORMULAS only: exact fraction bbox_height/displayed_item_count.",
    "segments": "FORMULA_SEGMENT occupancy recorded separately; slot statistics NOT_APPLICABLE.",
    "p10": "Nearest rank: sorted exact slots[ceil(N/10)-1].",
    "median": "Middle value if odd; exact arithmetic mean of middle two if even.",
    "canvas_edge": "Any native RGB ink in the outer 3 pixel rows or columns is a structural edge flag.",
    "limits": "Formula occupancy and canvas-edge flags do not certify glyph size, symbols, or segment completeness."
}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def valid_sha(value):
    require(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value), "Invalid SHA256")

def input_path(root, relative):
    require(isinstance(relative, str) and relative and not Path(relative).is_absolute(), "Invalid relative input path")
    return core.checked_path(root / relative, root)

def metrics(png):
    with Image.open(png) as src:
        size = src.size
        require(size == HD_SIZE, "Wrong actual PNG resolution")
        pixels = np.asarray(src.convert("RGB"))
    y0, y1, x0, x1 = VIEWPORT
    mask = np.any(pixels[y0:y1, x0:x1] > THRESH, axis=2)
    yy, xx = np.nonzero(mask)
    count = len(xx)
    h = int(yy.max()-yy.min()+1) if count else 0
    w = int(xx.max()-xx.min()+1) if count else 0
    border = (
        np.any(pixels[:3] > THRESH) or np.any(pixels[-3:] > THRESH)
        or np.any(pixels[:, :3] > THRESH) or np.any(pixels[:, -3:] > THRESH)
    )
    return {"size": list(size), "formula_ink": int(count), "bbox_height": h,
            "bbox_width": w, "canvas_edge_ink": bool(border)}

def exact_stats(slots):
    slots = sorted(slots)
    if not slots:
        return {"min": None, "p10_nearest_rank": None, "median": None}
    n = len(slots)
    middle = slots[n//2] if n % 2 else (slots[n//2-1]+slots[n//2])/2
    return {"min": str(slots[0]), "p10_nearest_rank": str(slots[(n+9)//10-1]),
            "median": str(middle)}

def verify(root, index, expected_index_sha256, expected_records=165, expected_pages=633):
    root = core.checked_path(root, root)
    index = core.checked_path(index, root)
    valid_sha(expected_index_sha256)
    require(sha256(index) == expected_index_sha256, "Index SHA mismatch")
    require(type(expected_records) is int and expected_records > 0 and type(expected_pages) is int and expected_pages > 0, "Invalid expected population")
    rows = [json.loads(line) for line in index.read_text("utf-8-sig").splitlines() if line.strip()]
    require(len(rows) == expected_records, "Wrong index record count")
    ids, seen_paths, records, full, segments, issues = set(), set(), [], [], [], []
    for row in rows:
        rid = row.get("id")
        require(isinstance(rid, str) and rid.strip() and rid not in ids, "Missing or duplicate record ID")
        ids.add(rid)
        for key in ("record_sha256", "math_sha256", "source_sha256", "geometry_sha256"):
            valid_sha(row.get(key))
        geometry_path = input_path(root, row["geometry_path"])
        require(sha256(geometry_path) == row["geometry_sha256"], "Geometry SHA mismatch")
        geo = json.loads(geometry_path.read_text("utf-8-sig"))
        require(geo.get("id") == rid, "Geometry record identity mismatch")
        gp, frames = geo.get("pages"), row.get("canonical_frames")
        require(isinstance(gp, list) and isinstance(frames, list) and gp, "Empty or invalid page coverage")
        require(len(gp) == len(frames) == row.get("page_count"), "Page coverage mismatch")
        record = {k: row[k] for k in ("id", "record_sha256", "math_sha256", "source_sha256")}
        record.update(geometry_path=row["geometry_path"], geometry_sha256=row["geometry_sha256"], pages=len(gp), page_rows=[])
        for i, (page, frame) in enumerate(zip(gp, frames)):
            require(type(page.get("page")) is int and page["page"] == i+1, "Geometry page order mismatch")
            kind, items = page.get("kind"), page.get("items")
            require(kind in ("FULL_FORMULAS", "FORMULA_SEGMENT"), "Unknown page kind")
            require(isinstance(items, list) and items and all(isinstance(x, dict) for x in items), "Empty or invalid formula items")
            path = input_path(root, frame["path"])
            require(path not in seen_paths, "Duplicate frame path")
            seen_paths.add(path)
            valid_sha(frame.get("sha256"))
            require(sha256(path) == frame["sha256"], "Frame SHA mismatch")
            require(page.get("frame") == path.name, "Ordered frame/geometry mismatch")
            met = metrics(path)
            n = len(items)
            slot = Fraction(met["bbox_height"], n) if kind == "FULL_FORMULAS" else None
            item = {"page_order_index": i, "page": page["page"], "kind": kind,
                    "path": frame["path"], "frame_sha256": frame["sha256"],
                    **met, "formulas_on_page": n,
                    "slot_px_proxy_exact": str(slot) if slot is not None else None,
                    "slot_proxy_at_1080p_exact": str(slot/2) if slot is not None else None,
                    "slot_status": "APPLICABLE_LAYOUT_PROXY_ONLY" if slot is not None else "NOT_APPLICABLE_SEGMENT",
                    "resolution_ok": True, "formula_ink_ok": met["formula_ink"] >= FORMULA_INK_MIN,
                    "canvas_edge_ok": not met["canvas_edge_ink"],
                    "slot_ok": slot is None or slot >= SLOT_MIN}
            item["all_structural_checks_ok"] = item["formula_ink_ok"] and item["canvas_edge_ok"] and item["slot_ok"]
            if not item["all_structural_checks_ok"]:
                issues.append({"id": rid, "page": page["page"], "path": frame["path"], "formula_ink_ok": item["formula_ink_ok"], "canvas_edge_ok": item["canvas_edge_ok"], "slot_ok": item["slot_ok"]})
            (full if kind == "FULL_FORMULAS" else segments).append(item)
            record["page_rows"].append(item)
        records.append(record)
    require(len(full)+len(segments) == expected_pages, "Wrong total page count")
    slots = [Fraction(p["slot_px_proxy_exact"]) for p in full]
    summary = {"schema_version": 3, "records": len(records), "pages": expected_pages,
               "full_pages": len(full), "segment_pages": len(segments),
               "geometry_items_total": sum(p["formulas_on_page"] for r in records for p in r["page_rows"]),
               "full_page_slot_proxy_exact": exact_stats(slots),
               "all_rational_metrics": "EXACT_FRACTIONS", "issue_count": len(issues), "issues": issues,
               "status": "PASS_BOUND_LAYOUT_PROXY_ONLY" if not issues else "FAIL_STRUCTURAL_CHECKS",
               "full_glyph_visual_acceptance": "NOT_ESTABLISHED",
               "minimum_glyph_size": "NOT_CERTIFIED_BY_SLOT_PROXY"}
    return {"summary": summary, "records": records, "algorithm": METHOD,
            "index_path": index.relative_to(root).as_posix(), "index_sha256": expected_index_sha256,
            "verifier_sha256": sha256(Path(__file__))}

def checked_output(root, output):
    base = root / "reviews/codex-supervision"
    output = core.checked_path(output, base)
    require(not output.exists(), "Refuse to overwrite existing evidence")
    current = output.parent
    while True:
        require(not (current / "delivery-manifest.json").exists(), "Refuse to add evidence inside frozen archive")
        if current == root:
            break
        current = current.parent
    return output

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, default=INDEX)
    parser.add_argument("--expected-index-sha256", default=INDEX_SHA)
    parser.add_argument("--expected-records", type=int, default=165)
    parser.add_argument("--expected-pages", type=int, default=633)
    parser.add_argument("--output", type=Path, required=True, help="Fresh project reviews/codex-supervision JSON path; never overwrite historical evidence")
    args = parser.parse_args(argv)
    try:
        root = ROOT.absolute()
        output = checked_output(root, args.output.absolute())
        evidence = verify(root, args.index.absolute(), args.expected_index_sha256, args.expected_records, args.expected_pages)
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open("xb") as target:
            target.write((json.dumps(evidence, ensure_ascii=False, indent=2)+"\n").encode("utf-8"))
        print(json.dumps(evidence["summary"], ensure_ascii=False))
        return 1 if evidence["summary"]["issue_count"] else 0
    except (OSError, ValueError, TypeError, KeyError) as error:
        print(json.dumps({"status": "FAILED", "error": str(error)}, ensure_ascii=False), file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
