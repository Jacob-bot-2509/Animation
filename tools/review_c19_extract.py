# -*- coding: utf-8 -*-
"""Extract the three target questions from batch-10 draft.jsonl as UTF-8 text."""
import json

SRC = r"D:\Animation-Model-Training\reviews\2026-10-05-training-diversity-drafts\batch-10\draft.jsonl"
OUT = r"D:\Animation-Model-Training\reviews\2026-10-05-training-diversity-drafts\batch-10\c19_extract.txt"

targets = {"draft-c19-03", "draft-c19-04", "draft-c19-05"}

with open(SRC, encoding="utf-8") as f:
    lines = [ln.strip() for ln in f if ln.strip()]

out_lines = []
for i, ln in enumerate(lines, 1):
    obj = json.loads(ln)
    qid = obj.get("id") or obj.get("question_id") or ""
    if qid not in targets:
        continue
    out_lines.append("=" * 70)
    out_lines.append(f"LINE {i}  {qid}")
    out_lines.append("=" * 70)
    for key, val in obj.items():
        out_lines.append(f"[{key}]")
        if isinstance(val, (dict, list)):
            out_lines.append(json.dumps(val, ensure_ascii=False, indent=2))
        else:
            out_lines.append(str(val))
        out_lines.append("")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))

print("written:", OUT)
print("count:", sum(1 for ln in lines for t in targets if (json.loads(ln).get("id") or json.loads(ln).get("question_id") or "") == t))
