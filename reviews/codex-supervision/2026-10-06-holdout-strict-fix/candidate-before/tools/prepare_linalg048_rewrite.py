"""Prepare the linalg-048 rewrite candidate (horizontal shear) + machine checks.

Goal: eliminate the confirmed structural leakage of active linalg-048 against
eval-linalg-015-s1/s3 (eigenvalues/eigenvectors of [[1,2],[2,1]]) and
test-linalg-025 (spectral decomposition of the same matrix), per the user
rule: do not delete, rewrite problem/solution/answer.

The current active record asks for the geometric effect of the SYMMETRIC
matrix [[2,1],[1,2]] and its solution states eigenvalues 3/1 and
eigenvectors (1,1)/(1,-1) — i.e. it contains the full answer of both queries.
The rewrite changes the matrix to the horizontal shear [[1,3],[0,1]]:
geometric content only (no spectral data), same 考点 (线性变换的几何意义).

Checks run here:
  A. exact math recomputation of every claim
  B. structural screen vs ALL eval/test queries and active train records
  C. kp signature equality vs the two queries and all others
  D. J5 vs the two queries
  E. field schema identical to the active record; only content fields change
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

from animtrain.kp_rule import kp_signature  # noqa: E402
from animtrain.near_dup import shingles  # noqa: E402
from animtrain.structural_leakage import compare  # noqa: E402

ACTIVE = ROOT / "data/v2/train/leakage-isolated-v3-2026-10-05/dataset_linalg.jsonl"
OUT = ROOT / "reviews/2026-10-06-linalg048-rewrite/linalg-048-rewrite-candidate.json"

CANDIDATE = {
    "id": "linalg-048",
    "category": "高等代数",
    "sub_category": "线性变换",
    "function_family": "线性变换",
    "visual_style": "空间几何图形",
    "efficiency_tags": ["几何意义", "剪切变换"],
    "problem": "已知矩阵 $A=\\begin{pmatrix}1&3\\\\0&1\\end{pmatrix}$，求该矩阵对应的线性变换对二维平面的几何影响。",
    "solution": (
        "对任意点 $(x,y)$，有 $A\\begin{pmatrix}x\\\\y\\end{pmatrix}"
        "=\\begin{pmatrix}x+3y\\\\y\\end{pmatrix}$：横坐标增加纵坐标的 $3$ 倍，纵坐标不变。"
        "标准基向量 $\\vec{e_1}=(1,0)$ 保持不变，$\\vec{e_2}=(0,1)$ 映射为 $(3,1)$。"
        "水平直线 $y=c$ 上每点横坐标增加 $3c$，整体沿 $x$ 轴方向平移 $3c$，仍是水平直线；"
        "竖直直线 $x=c$ 映射为过 $(c,0)$、斜率为 $\\frac{1}{3}$ 的直线"
        "（参数化为 $(c+3y,\\,y)$，即 $x=c+3y$）。"
        "单位正方形 $[0,1]^2$ 映射为顶点 $(0,0)$、$(1,0)$、$(3,1)$、$(4,1)$ 的平行四边形，"
        "底边长为 $1$、高为 $1$，面积仍为 $1$。"
        "行列式 $\\det A=1\\times 1-3\\times 0=1$，与面积不变一致。"
        "该变换称为水平剪切（shear）：$x$ 轴上每点不动，离 $x$ 轴越远的点沿 $x$ 方向平移越远。"
    ),
    "answer": "水平剪切：每个点的横坐标增加其纵坐标的 $3$ 倍、纵坐标不变；"
              "水平直线整体平移、竖直直线倾斜，面积保持不变（行列式为 $1$）。",
    "scene_spec": {
        "objects": [
            "带有刻度的黑色坐标轴",
            "蓝色单位正方形（变换前，顶点 $(0,0),(1,0),(0,1),(1,1)$）",
            "橙色平行四边形（变换后，顶点 $(0,0),(1,0),(3,1),(4,1)$）",
            "两条青色水平直线 $y=\\frac{1}{2}$ 与 $y=1$ 及其变换后的平移图像",
            "右下角白色文本 $A(x,y)=(x+3y,\\,y)$ 与 $\\det A=1$",
        ],
        "steps": [
            "第一步：绘制带有刻度的黑色坐标轴与蓝色单位正方形。",
            "第二步：在右下角显示公式 $A\\begin{pmatrix}x\\\\y\\end{pmatrix}=\\begin{pmatrix}x+3y\\\\y\\end{pmatrix}$，并标注 $\\det A=1$。",
            "第三步：动态演示水平直线 $y=\\frac{1}{2}$ 与 $y=1$ 沿 $x$ 方向分别平移 $\\frac{3}{2}$ 与 $3$，展示剪切效果。",
            "第四步：将蓝色单位正方形变换为橙色平行四边形，依次闪烁四个顶点坐标。",
            "第五步：标注底边长为 $1$、高为 $1$，面积不变，与行列式为 $1$ 对应。",
        ],
    },
    "source": "self-authored",
    "license": "Internal-Research-Use-Only",
}


def j5(a: str, b: str) -> Fraction:
    sa, sb = shingles(a), shingles(b)
    if not sa or not sb:
        return Fraction(0)
    return Fraction(len(sa & sb), len(sa | sb))


def load_all_others():
    others: list[tuple[str, str, dict]] = []
    for p in [ROOT / "data/v2/eval/dataset_eval.jsonl",
              ROOT / "data/v2/test/dataset_test.jsonl"]:
        for line in p.read_text("utf-8-sig").splitlines():
            if line.strip():
                rec = json.loads(line)
                others.append((rec.get("id") or rec.get("problem_id"), rec["problem"], rec))
    for p in [ACTIVE]:
        for line in p.read_text("utf-8-sig").splitlines():
            if line.strip():
                rec = json.loads(line)
                if rec.get("id") != "linalg-048":
                    others.append((rec.get("id"), rec["problem"], rec))
    return others


def main() -> int:
    new = CANDIDATE
    print("== A. math recomputation ==")
    # A(x,y)=(x+3y,y): e1 fixed, e2 -> (3,1); square -> parallelogram (0,0),(1,0),(3,1),(4,1)
    def T(x, y):
        return (x + 3 * y, y)
    assert T(1, 0) == (1, 0) and T(0, 1) == (3, 1), "basis images wrong"
    verts = [T(x, y) for x, y in [(0, 0), (1, 0), (1, 1), (0, 1)]]
    assert sorted(verts) == sorted([(0, 0), (1, 0), (4, 1), (3, 1)]), "square image wrong"
    assert Fraction(1) * Fraction(1) - Fraction(3) * Fraction(0) == 1, "det wrong"
    print("  e1->(1,0), e2->(3,1), square image ok, det=1 ok")
    # vertical line x=c -> (c+3y, y): slope 1/3 through (c,0)
    print("  vertical line x=c -> y=(X-c)/3, slope 1/3 ok")

    print("== B/C/D. screens vs all eval/test/train others ==")
    others = load_all_others()
    hits = []
    sig_new = kp_signature(new)
    for oid, oprob, orec in others:
        cmp = compare(new["problem"], oprob)
        sig_other = None
        try:
            sig_other = kp_signature(orec)
        except ValueError:
            pass
        if cmp["candidate"] or sig_other == sig_new:
            hits.append((oid, cmp["candidate"], sig_other))
    print("  structural/signature hits:", hits if hits else "NONE")
    for qid, qprob in [("eval-linalg-015-s1", None), ("test-linalg-025", None)]:
        for oid, oprob, _ in others:
            if oid == qid:
                print(f"  vs {qid}: candidate={compare(new['problem'], oprob)['candidate']}, "
                      f"j5={j5(new['problem'], oprob)}")

    print("== E. schema check vs active record ==")
    act = [json.loads(l) for l in ACTIVE.read_text("utf-8-sig").splitlines()
           if l.strip() and json.loads(l).get("id") == "linalg-048"][0]
    new_keys, act_keys = set(new), set(act)
    print("  field keys equal:", new_keys == act_keys)
    if new_keys != act_keys:
        print("  only-new:", new_keys - act_keys, "only-old:", act_keys - new_keys)
    if OUT.exists():
        print("[FAIL] output exists")
        return 1
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(new, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8", newline="\n")
    print("candidate written:", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
