# -*- coding: utf-8 -*-
"""Extract idx=226 draft-c43-03 from chunk-17.json, write to file."""
import json
import io

SRC = r"D:/Animation-Model-Training/reviews/2026-10-06-scene-standard-sweep/chunks/chunk-17.json"
OUT = r"D:/code/.bridge-poll/record_226.json"

with io.open(SRC, encoding="utf-8") as f:
    data = json.load(f)

rec = None
for r in data["records"]:
    if r.get("idx") == 226 and r.get("id") == "draft-c43-03":
        rec = r
        break

assert rec is not None, "record not found"

with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(rec, f, ensure_ascii=False, indent=2)

print("written:", OUT)
print("keys:", sorted(rec.keys()))
