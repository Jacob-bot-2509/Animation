# -*- coding: utf-8 -*-
"""Dump chunk-13.json fully, with sha256 per material record"""
import json, hashlib, io

path = r"D:\Animation-Model-Training\reviews\2026-10-06-linalg048-admission\v3-receipt-bound\review-chunks\chunk-13.json"
with open(path, encoding="utf-8") as f:
    d = json.load(f)

out = io.StringIO()
w = out.write
w("TOP-LEVEL KEYS: %s\n\n" % sorted(d.keys()))

cand = d.get("candidate") or {}
w("########## CANDIDATE: %s ##########\n" % cand.get("id"))
w("category=%s | sub=%s | family=%s\n" % (cand.get("category"), cand.get("sub_category"), cand.get("function_family")))
w("PROBLEM:\n%s\n\n" % cand.get("problem"))
w("SOLUTION:\n%s\n\n" % cand.get("solution"))
w("ANSWER:\n%s\n\n" % cand.get("answer"))
w("SOURCE: %s\n\n" % json.dumps(cand.get("source"), ensure_ascii=False))

for m in d.get("material", []):
    if not isinstance(m, dict):
        w("NON-DICT MATERIAL: %s\n\n" % json.dumps(m, ensure_ascii=False))
        continue
    mid = m.get("id")
    w("########## MATERIAL: %s ##########\n" % mid)
    w("keys=%s | status=%s | problem_sha256=%s\n" % (
        sorted(m.keys()), m.get("status"), m.get("problem_sha256")))
    for r in m.get("source_records", []):
        h = hashlib.sha256(r["problem"].encode("utf-8")).hexdigest()
        w("\n----- record %s (sha=%s) -----\n" % (r.get("id"), h))
        for k in ("method", "function_family", "sub_category", "category"):
            if k in r:
                w("%s=%s\n" % (k, r[k]))
        for k in ("problem", "solution", "answer"):
            w("%s:\n%s\n\n" % (k.upper(), r.get(k)))
        if "scene_spec" in r:
            w("SCENE_SPEC:\n%s\n\n" % json.dumps(r["scene_spec"], ensure_ascii=False))

with open(r"D:\code\.bridge-poll\_tmp_chunk13.txt", "w", encoding="utf-8") as f:
    f.write(out.getvalue())
print("written", out.tell(), "chars")
