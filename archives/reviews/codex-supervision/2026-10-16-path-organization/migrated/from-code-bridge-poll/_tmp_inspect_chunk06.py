# -*- coding: utf-8 -*-
"""临时:验证 eval-linalg-014 problem_sha256 绑定,并扫描 chunk 中其他与剪切相关的对"""
import hashlib
import json

CHUNK = r"D:\Animation-Model-Training\reviews\2026-10-06-linalg048-admission\v3-receipt-bound\review-chunks\chunk-06.json"

with open(CHUNK, "r", encoding="utf-8") as f:
    data = json.load(f)

# 1) sha256 验证
target = None
for item in data["material"]:
    if item.get("id") == "eval-linalg-014":
        target = item
        break
prob = target["source_records"][0]["problem"]
print("sha256(problem) =", hashlib.sha256(prob.encode("utf-8")).hexdigest())
print("recorded        =", target["problem_sha256"])
print("match:", hashlib.sha256(prob.encode("utf-8")).hexdigest() == target["problem_sha256"])
print()

# 2) 其他对是否有剪切族/几何矩阵题(防止审错了对)
for item in data["material"]:
    ids = item.get("id")
    cats = {r.get("function_family") for r in item.get("source_records", [])}
    subs = {r.get("sub_category") for r in item.get("source_records", [])}
    print(ids, "|", subs, "|", cats)

# 3) candidate 中是否含任何谱分解词
cand_text = json.dumps(data["candidate"], ensure_ascii=False)
for kw in ["特征值", "特征向量", "对角", "正交矩阵", "谱", "Q^T", "lambda"]:
    print(f"candidate contains '{kw}':", kw in cand_text)
