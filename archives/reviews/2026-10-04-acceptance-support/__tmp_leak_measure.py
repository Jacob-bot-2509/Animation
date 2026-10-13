"""防泄漏屏测量:train vs eval/test,考点签名一致 AND 5-gram Jaccard 分布。"""
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(r"D:\Animation-Model-Training")
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))
from animtrain.near_dup import shingles  # noqa: E402
from b5_calibrate import classify_kp  # noqa: E402


def j5(a: str, b: str) -> Fraction:
    sa, sb = shingles(a), shingles(b)
    u = sa | sb
    return Fraction(len(sa & sb), len(u)) if u else Fraction(0)


train = []
for f in ("calc", "geom", "linalg", "prob"):
    train += [json.loads(l) for l in
              (ROOT / f"data/v1/raw/dataset_{f}.jsonl").read_text(
                  encoding="utf-8").splitlines() if l.strip()]
seen = set()
ev = []
for r in [json.loads(l) for l in
          (ROOT / "data/v2/eval/dataset_eval.jsonl").read_text(
              encoding="utf-8").splitlines() if l.strip()]:
    if r["problem_id"] not in seen:
        seen.add(r["problem_id"])
        ev.append(r)
te = [json.loads(l) for l in
      (ROOT / "data/v2/test/dataset_test.jsonl").read_text(
          encoding="utf-8").splitlines() if l.strip()]


def sig(r):
    return (r.get("category", ""), classify_kp(r))


hits: list[tuple[float, str, str, str]] = []
for name, rows in (("eval", ev), ("test", te)):
    for r in rows:
        for t in train:
            if sig(r) == sig(t):
                j = j5(r["problem"], t["problem"])
                if j >= Fraction(1, 2):
                    hits.append((float(j), name, r.get("problem_id") or r.get("id"),
                                 t.get("id"), r["problem"][:50], t["problem"][:50]))
print("同考点 AND J5≥1/2 的 train-vs-eval/test 对:", len(hits))
for h in sorted(hits, reverse=True):
    print(f"  J5={h[0]:.3f} {h[1]}:{h[2]} × train:{h[3]}")
    print(f"     eval/test: {h[4]}")
    print(f"     train:     {h[5]}")
# 统计同考点对的 J5 分布(不含阈值过滤,看整体)
bins = [0] * 10
n_same = 0
for name, rows in (("eval", ev), ("test", te)):
    for r in rows:
        for t in train:
            if sig(r) == sig(t):
                n_same += 1
                j = float(j5(r["problem"], t["problem"]))
                bins[min(int(j * 10), 9)] += 1
print(f"\n同考点 train-vs-eval/test 对总数: {n_same}")
print("J5 分布(0.0-0.1, 0.1-0.2, ...):", bins)
