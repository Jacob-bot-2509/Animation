# -*- coding: utf-8 -*-
"""定位 test/test-linalg-019 所在 chunk 与 pair 材料,并核对 sha256"""
import json, hashlib, os, glob

base = r"D:\Animation-Model-Training\reviews\2026-10-06-linalg048-admission\v3-receipt-bound\review-chunks"
target_hash = "cd20a9fc184b7b88db191ee9d580c9d1a328e426f1eb18a7b3946940ef37c627"

for path in sorted(glob.glob(os.path.join(base, "chunk-*.json"))):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    cand = d.get("candidate") or {}
    cand_txt = json.dumps(cand, ensure_ascii=False)
    hit = False
    for m in d.get("material", []):
        if not isinstance(m, dict):
            continue
        for r in m.get("source_records", []):
            h = hashlib.sha256(r["problem"].encode("utf-8")).hexdigest()
            if h == target_hash or r.get("id") == "test-linalg-019":
                print(os.path.basename(path), "| material id:", m.get("id"),
                      "| record id:", r.get("id"), "| sha:", h,
                      "| hash-match:", h == target_hash)
                hit = True
    if hit:
        print("   -> candidate id:", cand.get("id"))
        print("   -> candidate problem sha256:",
              hashlib.sha256(cand.get("problem", "").encode("utf-8")).hexdigest())
print("done")
