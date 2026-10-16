import json, io

chunk_path = r"D:\Animation-Model-Training\reviews\2026-10-06-linalg048-admission\v3-receipt-bound\review-chunks\chunk-06.json"
with open(chunk_path, encoding="utf-8") as f:
    d = json.load(f)

cand = d["candidate"]
out = io.StringIO()
w = out.write
w("########## CANDIDATE: %s ##########\n" % cand["id"])
w("category=%s | sub=%s | family=%s\n" % (cand["category"], cand["sub_category"], cand["function_family"]))
w("PROBLEM:\n%s\n" % cand["problem"])
w("SOLUTION:\n%s\n" % cand["solution"])
w("ANSWER:\n%s\n" % cand["answer"])
w("SOURCE:\n%s\n" % json.dumps(cand["source"], ensure_ascii=False))
w("SCENE_SPEC:\n%s\n" % json.dumps(cand["scene_spec"], ensure_ascii=False))
w("VISUAL_STYLE: %s\n" % json.dumps(cand["visual_style"], ensure_ascii=False))
w("EFFICIENCY_TAGS: %s\n" % json.dumps(cand["efficiency_tags"], ensure_ascii=False))

for m in d["material"]:
    if isinstance(m, dict) and m.get("id") == "eval-linalg-015":
        w("\n########## MATERIAL eval-linalg-015 ##########\n")
        w("status=%s\n" % m.get("status"))
        for r in m["source_records"]:
            w("\n----- record %s (method=%s, family=%s, sub=%s) -----\n" % (r["id"], r["method"], r["function_family"], r["sub_category"]))
            w("PROBLEM:\n%s\n" % r["problem"])
            w("SOLUTION:\n%s\n" % r["solution"])
            w("ANSWER:\n%s\n" % r["answer"])
            w("SCENE_SPEC:\n%s\n" % json.dumps(r["scene_spec"], ensure_ascii=False))

with open(r"D:\code\.bridge-poll\_tmp_pair015.txt", "w", encoding="utf-8") as f:
    f.write(out.getvalue())
print("written")
