# -*- coding: utf-8 -*-
"""Dump chunk-16 material for the pair involving test/test-x-012 to a UTF-8 text file."""
import json
import sys

CHUNK = r"d:\Animation-Model-Training\reviews\2026-10-06-linalg048-admission\v3-receipt-bound\review-chunks\chunk-16.json"
OUT = r"D:\code\.bridge-poll\_tmp_chunk16.txt"

data = json.load(open(CHUNK, encoding="utf-8"))

cand = data["candidate"]
pairs = data["pairs"]
material = data["material"]

lines = []
lines.append("=" * 80)
lines.append("CANDIDATE")
lines.append("=" * 80)
for k, v in cand.items():
    lines.append(f"\n### {k}\n{v}")

for i, (p, m) in enumerate(zip(pairs, material)):
    pid = p.get("id") or p.get("test_id") or p.get("pair_id") or str(i)
    if "test-x-012" not in str(p) and "x-012" not in str(p):
        lines.append(f"\n\n>>> SKIPPED pair index {i} (id={pid}) -- not the target; see pairs list below")
        continue
    lines.append("\n" + "=" * 80)
    lines.append(f"TARGET PAIR index {i}")
    lines.append("=" * 80)
    lines.append("\n----- PAIR ENTRY -----\n" + json.dumps(p, ensure_ascii=False, indent=2))
    lines.append("\n----- MATERIAL ENTRY -----")
    if isinstance(m, dict):
        for mk, mv in m.items():
            lines.append(f"\n### material[{mk}]\n{mv}")
    else:
        lines.append(str(m))

lines.append("\n" + "=" * 80)
lines.append("ALL PAIR IDS")
lines.append("=" * 80)
for i, p in enumerate(pairs):
    lines.append(f"{i}: {json.dumps(p, ensure_ascii=False)[:300]}")

open(OUT, "w", encoding="utf-8").write("\n".join(lines))
print("wrote", OUT)
