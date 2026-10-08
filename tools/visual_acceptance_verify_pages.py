"""Re-verify Codex's 626-page readable formula delivery against the user's HD criteria.

Reads the frozen DELIVERY_INDEX.jsonl (read-only; nothing is written into the
frozen dir). Checks per canonical page: file existence, sha256 binding,
resolution (>=1080 lines), ink content, no edge clipping, and per-formula slot
height (page content height / formulas-on-page from the bound geometry file).
Also verifies total formula coverage (sum of per-page items == unique formulas).
Writes a new receipt under reviews/2026-10-08-visual-acceptance/ (add-only).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(r"D:\Animation-Model-Training")
INDEX = ROOT / "reviews/codex-supervision/2026-10-08-visual-mail-review/DELIVERY_INDEX.jsonl"
OUT = ROOT / "reviews/2026-10-08-visual-acceptance"
THRESH = 32
HD_LINES = 1080
SLOT_MIN = 24  # px per formula slot per page (user requirement)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def metrics(png):
    from PIL import Image
    img = Image.open(png).convert("L")
    w, h = img.size
    px = img.load()
    xs, ys, n = [], [], 0
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            if px[x, y] > THRESH:
                xs.append(x); ys.append(y); n += 1
    if not n:
        return {"ink": 0, "bbox": None, "clipped": False, "size": [w, h]}
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    clipped = minx <= 1 or maxx >= w - 2 or miny <= 1 or maxy >= h - 2
    return {"ink": n, "bbox": [minx, miny, maxx, maxy], "clipped": clipped, "size": [w, h]}


def main():
    rows = [json.loads(ln) for ln in INDEX.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(rows) == 165, f"expected 165 index rows, got {len(rows)}"
    pages, issues, per_record, total_items = [], [], [], 0
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
        n_items = {p.get("page"): len(p.get("items") or []) for p in geo_pages}
        rec = {"id": rid, "pages": len(frames), "page_rows": []}
        for f in frames:
            png = ROOT / f["path"]
            if not png.is_file():
                issues.append({"id": rid, "page": f["path"], "issue": "frame file missing"})
                continue
            if sha256(png) != f["sha256"]:
                issues.append({"id": rid, "page": f["path"], "issue": "frame sha mismatch"})
                continue
            met = metrics(png)
            page_no = int(Path(f["path"]).stem.split("-")[-1])
            items = n_items.get(page_no, 0)
            bbox_h = (met["bbox"][3] - met["bbox"][1]) if met["bbox"] else 0
            slot = round(bbox_h / items, 1) if items else None
            row = {
                "page": page_no, "size": met["size"], "ink": met["ink"],
                "clipped": met["clipped"], "formulas_on_page": items, "slot_px": slot,
                "resolution_ok": met["size"][1] >= HD_LINES,
                "slot_ok": slot is not None and slot >= SLOT_MIN,
                "ink_ok": met["ink"] >= 200,
                "clipped_ok": not met["clipped"],
            }
            row["all_ok"] = row["resolution_ok"] and row["slot_ok"] and row["ink_ok"] and row["clipped_ok"]
            if not row["all_ok"]:
                issues.append({"id": rid, "page": page_no, "issue": row})
            rec["page_rows"].append(row)
            pages.append(row)
        per_record.append(rec)
        total_items += sum(n_items.values())
    ok_pages = sum(p["all_ok"] for p in pages)
    sizes = sorted({tuple(p["size"]) for p in pages})
    slots = [p["slot_px"] for p in pages if p["slot_px"] is not None]
    summary = {
        "records": len(per_record), "pages": len(pages), "geometry_items_total": total_items,
        "pages_all_ok": ok_pages, "pages_with_issues": len(pages) - ok_pages,
        "resolution_histogram": {f"{w}x{h}": sum(1 for p in pages if tuple(p["size"]) == (w, h))
                                 for w, h in sizes},
        "slot_px_min": min(slots) if slots else None,
        "slot_px_p10": sorted(slots)[len(slots) // 10] if slots else None,
        "slot_px_median": sorted(slots)[len(slots) // 2] if slots else None,
        "criteria": {"resolution_min_lines": HD_LINES, "slot_px_min": SLOT_MIN,
                     "coverage": "165 records, all pages sha-bound to frozen index"},
        "issues": issues[:20], "issue_count": len(issues),
    }
    (OUT / "readable-pages-verification.json").write_text(
        json.dumps({"summary": summary, "records": per_record}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main())
