# -*- coding: utf-8 -*-
"""提取 chunk-04.json 中 idx=48 / id=draft-c13-04 的记录,写入 UTF-8 文件供 Read 查看。"""
import json, io, sys

CHUNK = r'D:/Animation-Model-Training/reviews/2026-10-06-scene-standard-sweep/chunks/chunk-04.json'
OUT = r'D:/Animation-Model-Training/tools/_tmp_c13_04_record.json'

with open(CHUNK, encoding='utf-8') as f:
    data = json.load(f)

recs = data.get('records', [])
hits = [r for r in recs if isinstance(r, dict) and (r.get('idx') == 48 or r.get('id') == 'draft-c13-04')]
print('total records:', len(recs))
print('hits:', len(hits))
for h in hits:
    print('idx=', h.get('idx'), 'id=', h.get('id'))

with open(OUT, 'w', encoding='utf-8') as f:
    json.dump({'standard': data.get('standard'), 'hits': hits}, f, ensure_ascii=False, indent=2)
print('written:', OUT)
