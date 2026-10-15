"""全局语义隔离深层通道:同(category,sub_category)族跨集配对 + 签名相似度分级候选."""
from __future__ import annotations
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUP = ROOT / "reviews/codex-supervision/2026-10-07-semantic-signature-supervision"
OUT = ROOT / "reviews/2026-10-07-semantic-core-lists"

# 目标同义组:同一数学目标的不同表述(几何↔代数等)
GOAL_SYNONYMS = [
    {"求直线与平面交点", "求直线与曲面交点", "求参数方程交点", "求方程组交点"},
    {"求两平面交线", "求平面交线参数方程"},
    {"求点面距离", "求点到平面距离"},
    {"求点到直线距离", "求点线距离"},
    {"求两平行平面距离", "求平行平面距离"},
    {"克拉默法则解方程组", "用克拉默法则求解方程组", "克拉默法则求解"},
    {"求矩阵逆", "求逆矩阵", "求矩阵的逆"},
    {"求特征值与特征向量", "求特征值特征向量", "求特征值和特征向量"},
    {"求条件概率", "求后验概率"},
    {"求二项尾概率", "求尾概率上界"},
    {"求极限", "计算极限", "求数列极限"},
    {"求两曲线围成面积", "计算两曲线围成面积", "求围成图形的面积", "计算封闭图形面积"},
    {"求旋转体体积", "计算旋转体体积"},
    {"判断级数敛散", "讨论级数敛散性", "判断级数收敛性"},
    {"求幂级数收敛域", "求级数收敛域"},
    {"求傅里叶展开", "傅里叶级数展开", "求傅里叶级数"},
    {"判断二次曲面类型", "指出二次曲面类型", "说明二次曲面类型"},
    {"求曲面切平面", "求切平面方程"},
    {"求直线与平面夹角", "求线面夹角"},
    {"求过三点平面方程", "求过三点平面"},
    {"求正态尾概率", "求正态分布概率"},
    {"求指数分布无记忆性", "证明无记忆性"},
    {"求几何分布期望", "求首次成功期望"},
]


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canon(t: str) -> str:
    return t.strip().rstrip("。；; ")


def synonym_group(goal: str) -> frozenset:
    g = canon(goal)
    for group in GOAL_SYNONYMS:
        if g in group:
            return frozenset(canon(x) for x in group)
    return frozenset({g})


def jaccard(a: list, b: list) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / len(sa | sb)


def load_records() -> dict:
    """从 effective-core-v2 绑定加载记录元数据(category/sub_category)."""
    core = SUP / "effective-core-v2"
    man = json.loads((core / "delivery-manifest.json").read_text(encoding="utf-8-sig"))
    expected = "78017f740969cd251f6c263bdcb14ef1bb5bd63de939df394fa24e33e57df4b5"
    if digest((core / "delivery-manifest.json").read_bytes()) != expected:
        raise ValueError("effective-core-v2 manifest changed")
    rb = [json.loads(l) for l in (core / "record-bindings.jsonl").read_text(encoding="utf-8-sig").splitlines()
          if l.strip()]
    if len(rb) != 761:
        raise ValueError("record bindings incomplete")
    cache = {}
    meta = {}
    for b in rb:
        src = b["path"]
        if src not in cache:
            data = (ROOT / src).read_bytes()
            if digest(data) != b["source_sha256"]:
                raise ValueError("source changed: " + src)
            cache[src] = data.splitlines(keepends=True)
        rec = json.loads(cache[src][b["source_line"] - 1].decode("utf-8-sig"))
        meta[b["id"]] = {"category": rec.get("category", ""),
                         "sub_category": rec.get("sub_category", ""),
                         "group": b["group"]}
    return meta


def main() -> int:
    sigs = [json.loads(l) for l in (SUP / "revised-complete-signatures-v2.jsonl")
            .read_text(encoding="utf-8-sig").splitlines() if l.strip()]
    by_id = {s["id"]: s for s in sigs}
    if len(by_id) != 761:
        raise ValueError("signature count != 761")
    meta = load_records()
    train_side = [s for s in sigs if s["group"] in ("train", "selected_draft")]
    eval_side = [s for s in sigs if s["group"] in ("eval", "test")]

    # 1) 同族跨集配对计数
    family = defaultdict(lambda: {"train": [], "eval": []})
    for s in train_side:
        m = meta[s["id"]]
        family[(m["category"], m["sub_category"])]["train"].append(s)
    for s in eval_side:
        m = meta[s["id"]]
        family[(m["category"], m["sub_category"])]["eval"].append(s)
    total_pairs = 0
    fam_lines = []
    for (cat, sub), sides in sorted(family.items()):
        pairs = len(sides["train"]) * len(sides["eval"])
        total_pairs += pairs
        if pairs:
            fam_lines.append((pairs, cat, sub, len(sides["train"]), len(sides["eval"])))
    print(f"同族跨集配对总数: {total_pairs}")
    print("前 12 大族:")
    for pairs, cat, sub, nt, ne in sorted(fam_lines, reverse=True)[:12]:
        print(f"  {pairs:>5} 对  {cat}/{sub}  (train侧{nt} × eval侧{ne})")

    # 2) 候选过滤:同族 且 (目标同义组相同 或 步骤Jaccard≥0.25)
    candidates = []
    for (cat, sub), sides in family.items():
        for t in sides["train"]:
            for e in sides["eval"]:
                same_goal = synonym_group(t["goal"]) == synonym_group(e["goal"])
                jac = jaccard(t["decisive_steps"], e["decisive_steps"])
                if same_goal or jac >= 0.25:
                    candidates.append({
                        "train_id": t["id"], "eval_id": e["id"],
                        "eval_group": e["group"], "category": cat, "sub_category": sub,
                        "same_goal_group": same_goal,
                        "steps_jaccard": round(jac, 3),
                        "train_goal": t["goal"], "eval_goal": e["goal"],
                        "train_domain": t["domain"], "eval_domain": e["domain"],
                        "train_conditions": t["key_conditions"], "eval_conditions": e["key_conditions"],
                        "train_steps": t["decisive_steps"], "eval_steps": e["decisive_steps"],
                        "train_record_sha256": t["record_sha256"],
                        "eval_record_sha256": e["record_sha256"],
                        "disposition": "UNREVIEWED",
                    })
    out = OUT / "deep-candidates-v1.json"
    with out.open("w", encoding="utf-8", newline="\n") as f:
        json.dump({"schema": "deep-semantic-candidates-v1",
                   "family_pairs_total": total_pairs,
                   "candidate_count": len(candidates),
                   "candidates": candidates}, f, ensure_ascii=False, indent=2)
        f.write("\n")
    b = out.read_bytes()
    print(f"\n候选过滤后: {len(candidates)} 对 -> {out.relative_to(ROOT)}")
    print(f"sha256={digest(b)}  bytes={len(b)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
