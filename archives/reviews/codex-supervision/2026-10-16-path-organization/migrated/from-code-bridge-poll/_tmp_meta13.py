# -*- coding: utf-8 -*-
"""Dump pairs/definition from chunk-13.json; check acceptance/receipt for recorded verdicts"""
import json, io

path = r"D:\Animation-Model-Training\reviews\2026-10-06-linalg048-admission\v3-receipt-bound\review-chunks\chunk-13.json"
with open(path, encoding="utf-8") as f:
    d = json.load(f)

out = io.StringIO()
w = out.write
w("DEFINITION:\n%s\n\n" % json.dumps(d.get("definition"), ensure_ascii=False, indent=1))
w("PAIRS:\n%s\n" % json.dumps(d.get("pairs"), ensure_ascii=False, indent=1))

for extra in [
    r"D:\Animation-Model-Training\reviews\2026-10-06-linalg048-admission\v3-receipt-bound\manual-acceptance.json",
]:
    w("\n\n########## %s ##########\n" % extra)
    try:
        with open(extra, encoding="utf-8") as f:
            w(f.read())
    except OSError as e:
        w("ERR %s\n" % e)

with open(r"D:\code\.bridge-poll\_tmp_meta13.txt", "w", encoding="utf-8") as f:
    f.write(out.getvalue())
print("written", out.tell())
