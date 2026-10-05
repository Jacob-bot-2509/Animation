# -*- coding: utf-8 -*-
"""Extract the three target drafts from draft.jsonl as UTF-8 JSON files."""
import json
from pathlib import Path

SRC = Path(r"D:\Animation-Model-Training\reviews\2026-10-05-training-diversity-drafts\batch-11\draft.jsonl")
OUT_DIR = Path(r"D:\Animation-Model-Training\reviews\2026-10-05-training-diversity-drafts\batch-11\extracted")
OUT_DIR.mkdir(exist_ok=True)

targets = {"draft-c22-05", "draft-c23-01", "draft-c23-02"}
with SRC.open(encoding="utf-8") as f:
    for i, line in enumerate(f, 1):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        qid = d.get("id", "")
        if qid in targets:
            out = OUT_DIR / f"{qid}.json"
            out.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"wrote {qid} (line {i})")
