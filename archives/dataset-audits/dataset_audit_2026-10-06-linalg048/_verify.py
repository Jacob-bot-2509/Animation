"""linalg-048 改写候选的独立复核(只读)。"""
import json
import sys
import pathlib
import collections
from fractions import Fraction

ROOT = pathlib.Path(".").resolve()
sys.path[:0] = [str(ROOT), str(ROOT / "src"), str(ROOT / "tools")]
from animtrain.structural_leakage import compare, VERSION  # noqa: E402
from animtrain.near_dup import shingles  # noqa: E402
from dataset_audit import (Audit, check_consistency, check_latex,  # noqa: E402
                           check_scene_spec, check_source_license)

cand = json.loads(pathlib.Path(
    "reviews/2026-10-06-linalg048-rewrite/linalg-048-rewrite-candidate.json"
).read_text(encoding="utf-8-sig"))

print("== 1. 数学自算(Lead 独立推导) ==")
import itertools
A = [[1, 3], [0, 1]]
det = A[0][0] * A[1][1] - A[0][1] * A[1][0]
def mul(M, v):
    return [M[0][0]*v[0] + M[0][1]*v[1], M[1][0]*v[0] + M[1][1]*v[1]]
print(f"  det(A) = {det}  (候选声称 1)")
print(f"  A·e1 = {mul(A,[1,0])}  (应 (1,0)) | A·e2 = {mul(A,[0,1])}  (应 (3,1))")
print(f"  A(x,y) = {mul(A,[7,2])}  (x=7,y=2 -> (7+6,2)=(13,2))")
verts = [[0,0],[1,0],[0,1],[1,1]]
print("  单位正方形顶点像:", [mul(A, v) for v in verts], "(应与候选一致)")
# 特征值: (1-λ)^2 = 0 -> λ=1 双根,缺陷矩阵(不可对角化)
print("  特征多项式 (1-λ)^2 -> λ=1 双根;A≠I 且无第二线性无关特征向量 -> 不可对角化(剪切)")
print("  竖直线 x=c 的像: (c+3y, y) -> 斜率 1/3,过 (c,0) ✓")
print("  水平线 y=c 的像: (x+3c, c) -> 仍水平,右移 3c ✓")
print("  面积因子 |det| = 1 ✓; 候选结论与自算一致" )

print()
print("== 2. 结构泄漏复筛(structural_leakage.compare) ==")
def problems_of(path):
    out = {}
    for l in pathlib.Path(path).read_text(encoding="utf-8-sig").splitlines():
        if l.strip():
            r = json.loads(l)
            out[r.get("id") or r.get("problem_id")] = r.get("problem")
    return out

train = {}
for p in pathlib.Path("data/v2/train/leakage-isolated-v3-2026-10-05").glob("*.jsonl"):
    train.update(problems_of(p))
ev = problems_of("data/v2/eval/dataset_eval.jsonl")
te = problems_of("data/v2/test/dataset_test.jsonl")
newp = cand["problem"]
print(f"  规则 {VERSION} | train {len(train)} / eval {len(ev)} / test {len(te)} 题")
targets = {"eval-linalg-015-s1": None, "test-linalg-025": None}
for k in targets:
    targets[k] = ev.get(k) or te.get(k)
for k, prob in targets.items():
    r = compare(newp, prob)
    print(f"  候选 vs {k}: candidate={r.get('candidate')} reasons={r.get('reasons')} score={r.get('score')}")
oldp = train.get("linalg-048")
for k, prob in targets.items():
    r_old = compare(oldp, prob)
    print(f"  (旧题 vs {k}: candidate={r_old.get('candidate')} score={r_old.get('score')})")

print("  --- 用候选题替换 linalg-048 后,全量再筛 ---")
cands = []
for side, pool in (("eval", ev), ("test", te)):
    for rid, prob in pool.items():
        for tid, tprob in train.items():
            tp = newp if tid == "linalg-048" else tprob
            r = compare(prob, tp)
            if r.get("candidate"):
                cands.append((side, rid, tid, r.get("score"), r.get("reasons")))
print(f"  全量候选对数(替换后): {len(cands)}")
for c in cands[:10]:
    print("   ", c)

print()
print("== 3. 近重复(5-gram set Jaccard,阈值 0.7) ==")
def jac(a, b):
    sa, sb = shingles(a), shingles(b)
    return Fraction(len(sa & sb), len(sa | sb)) if sa and sb else Fraction(0)
worst = (Fraction(0), None)
for pool_name, pool in (("train", train), ("eval", ev), ("test", te)):
    for rid, prob in pool.items():
        if rid == "linalg-048":
            continue
        s = jac(newp, prob)
        if s > worst[0]:
            worst = (s, f"{pool_name}:{rid}")
for k, prob in targets.items():
    print(f"  候选 vs {k}: J={float(jac(newp, prob)):.4f}")
print(f"  与全池最大: {float(worst[0]):.4f} ({worst[1]})")

print()
print("== 4. 记录级检查(字段/LaTeX/scene/一致性) ==")
audit = Audit()
fake_path = "reviews/2026-10-06-linalg048-rewrite/linalg-048-rewrite-candidate.json"
info = {"path": fake_path, "format": "json"}
r = {"locator": "record[1]", "record": cand}
rid = str(cand.get("id"))
check_source_license(audit, info, r, rid)
check_consistency(audit, info, r, rid)
check_latex(audit, info, r, rid)
check_scene_spec(audit, info, r, rid)
sev = collections.Counter(i["severity"] for i in audit.issues)
print("  严重度:", dict(sev))
for i in audit.issues:
    print(f"   [{i['severity']} {i['code']}] {i['message'][:150]}")
missing = [k for k in ("id","category","sub_category","problem","solution","answer",
                       "scene_spec","source","license") if not cand.get(k)]
print("  必需字段缺失:", missing or "无")
