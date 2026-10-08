# -*- coding: utf-8 -*-
"""对抗验证: 读取 chunk-07 中 eval-linalg-033 的完整 material 并输出。"""
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")

CHUNK = r"D:\Animation-Model-Training\reviews\2026-10-06-linalg048-admission\v3-receipt-bound\review-chunks\chunk-07.json"

data = json.load(open(CHUNK, encoding="utf-8"))

print("=== candidate id ===")
print(data["candidate"]["id"])

mat = data.get("material", {})
print("=== material type ===")
print(type(mat))
if isinstance(mat, list):
    print("=== material len ===")
    print(len(mat))
    # find the entry whose id is eval-linalg-033
    target = None
    for m in mat:
        mid = None
        if isinstance(m, dict):
            mid = m.get("id") or m.get("problem_id") or m.get("item_id")
        if mid and "033" in str(mid):
            target = m
            break
    if target is None:
        # dump first entry keys and id-like fields of all entries
        if mat:
            print("=== first entry keys ===")
            print(list(mat[0].keys()) if isinstance(mat[0], dict) else type(mat[0]))
            print("=== all id-like fields ===")
            for m in mat:
                if isinstance(m, dict):
                    print(m.get("id") or m.get("problem_id") or m.get("item_id") or list(m.keys()))
    else:
        print("=== FULL MATERIAL eval-linalg-033 ===")
        print(json.dumps(target, ensure_ascii=False, indent=2))
