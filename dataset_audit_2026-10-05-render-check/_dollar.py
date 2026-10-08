import json
import pathlib
import collections
import re

DATASETS = [
    ("v1 raw(63)", sorted(pathlib.Path("data/v1/raw").glob("*.jsonl"))),
    ("v2 train 池", sorted(pathlib.Path("data/v2/train/leakage-isolated-v3-2026-10-05").glob("*.jsonl"))),
    ("v2 eval", [pathlib.Path("data/v2/eval/dataset_eval.jsonl")]),
    ("v2 test", [pathlib.Path("data/v2/test/dataset_test.jsonl")]),
    ("drafts v4-final", sorted(pathlib.Path("reviews/2026-10-05-training-diversity-drafts").glob("batch-*/draft-codex-repair-v4-final.jsonl"))),
]
DOLLAR2 = "$" + "$"

print("== 双美元显示公式(##)统计 ==")
tot = 0
for name, paths in DATASETS:
    hits = []
    for p in paths:
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            rid = rec.get("id") or rec.get("problem_id")
            txts = [("problem", rec.get("problem")), ("solution", rec.get("solution")),
                    ("answer", rec.get("answer")), ("scene", json.dumps(rec.get("scene_spec"), ensure_ascii=False))]
            for fld, t in txts:
                if isinstance(t, str) and DOLLAR2 in t:
                    hits.append((rid, fld, t.count(DOLLAR2)))
    if hits:
        print(f"  {name}: {len(hits)} 处 -> {hits[:6]}")
    tot += len(hits)
print("  合计:", tot, "处")

print()
print("== eval-linalg-019-s3 的 ## 明细 ==")
for l in open("data/v2/eval/dataset_eval.jsonl", encoding="utf-8"):
    if not l.strip():
        continue
    r = json.loads(l)
    if r.get("id") == "eval-linalg-019-s3":
        sol = r["solution"]
        idx = [m.start() for m in re.finditer(re.escape(DOLLAR2), sol)]
        print("  出现位置:", idx)
        print("  单 $ 总数:", sol.count("$"), "| 双 $ 对:", len(idx) // 2)
        print("  片段:", sol[max(0, idx[0]-60):idx[0]+90].replace("\n", " "))

print()
print("== 各数据集 $ 总数与奇偶 ==")
for name, paths in DATASETS:
    n_rec = n_txt_odd = tot_dollar = 0
    for p in paths:
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            n_rec += 1
            for k in ("problem", "solution", "answer"):
                t = rec.get(k)
                if isinstance(t, str):
                    tot_dollar += t.count("$")
                    if t.count("$") % 2:
                        n_txt_odd += 1
    print(f"  {name:18s} 记录={n_rec:>4d} 文本内 $ 合计={tot_dollar:>6d} 字段级奇数 $={n_txt_odd}")
