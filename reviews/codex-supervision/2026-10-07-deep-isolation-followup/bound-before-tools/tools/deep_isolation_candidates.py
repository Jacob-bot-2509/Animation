"""Version-bound family candidate screen. Non-hit is never semantic exclusion."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import json
from pathlib import Path
import sys

if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
import core_signatures as core

DEFAULT_INPUT = core.ROOT / "reviews/codex-supervision/2026-10-07-semantic-signature-supervision/revised-complete-signatures-v2.jsonl"
GOAL_SYNONYMS = (
    ("求两平面交线", "求平面交线参数方程"),
    ("求点面距离", "求点到平面距离"),
    ("求点到直线距离", "求点线距离"),
    ("求两平行平面距离", "求平行平面距离"),
    ("克拉默法则解方程组", "用克拉默法则求解方程组", "克拉默法则求解"),
    ("求矩阵逆", "求逆矩阵", "求矩阵的逆"),
    ("求特征值与特征向量", "求特征值特征向量", "求特征值和特征向量"),
    ("求两曲线围成面积", "计算两曲线围成面积", "求围成图形的面积", "计算封闭图形面积"),
    ("求旋转体体积", "计算旋转体体积"),
    ("判断级数敛散", "讨论级数敛散性", "判断级数收敛性"),
    ("求幂级数收敛域", "求级数收敛域"),
    ("求傅里叶展开", "傅里叶级数展开", "求傅里叶级数"),
    ("求直线与平面夹角", "求线面夹角"),
    ("求过三点平面方程", "求过三点平面"),
)
# Same goal labels can nominate pairs; they never certify task equivalence.
def canon(text):
    return text.strip().rstrip("。；; ")

def synonym_group(goal):
    goal = canon(goal)
    for group in GOAL_SYNONYMS:
        values = frozenset(map(canon, group))
        if goal in values:
            return values
    return frozenset((goal,))

def jaccard(left, right):
    a, b = set(map(canon, left)), set(map(canon, right))
    return Fraction(len(a & b), len(a | b)) if a | b else Fraction(1)

def population(input_path):
    bindings = core.load_record_bindings()
    by_id = {b["id"]: b for b in bindings}
    sigs, inputs = core.read_signature_inputs([input_path], by_id)
    if {s["id"] for s in sigs} != set(by_id):
        raise ValueError("Complete current-core signature coverage required")
    records = {rid: core.load_record(by_id, rid) for rid in by_id}
    for record in records.values():
        for name in ("category", "sub_category"):
            if not isinstance(record.get(name), str) or not record[name].strip():
                raise ValueError("Nonempty actual family metadata required")
    return sigs, inputs, records

def build_report(sigs, inputs, records):
    groups = dict(Counter(s["group"] for s in sigs))
    if groups != core.EXPECTED_GROUPS or len({s["id"] for s in sigs}) != len(sigs):
        raise ValueError("Population/group mismatch")
    train = [s for s in sigs if s["group"] in ("train", "selected_draft")]
    evaluation = [s for s in sigs if s["group"] in ("eval", "test")]
    family = defaultdict(lambda: {"train": [], "eval": []})
    for side, signatures in (("train", train), ("eval", evaluation)):
        for sig in signatures:
            record = records[sig["id"]]
            family[(record["category"], record["sub_category"])][side].append(sig)
    candidates, family_counts = [], []
    for (cat, sub), sides in sorted(family.items()):
        nt, ne = len(sides["train"]), len(sides["eval"])
        if nt * ne:
            family_counts.append({"category": cat, "sub_category": sub, "train_side": nt, "eval_side": ne, "pairs": nt * ne})
        for t in sides["train"]:
            for e in sides["eval"]:
                same = synonym_group(t["goal"]) == synonym_group(e["goal"])
                score = jaccard(t["decisive_steps"], e["decisive_steps"])
                if not same and score < Fraction(1, 4):
                    continue
                candidates.append({
                    "train_id": t["id"], "eval_id": e["id"], "eval_group": e["group"],
                    "category": cat, "sub_category": sub, "same_goal_group": same,
                    "steps_jaccard": str(score),
                    **{"train_" + key: t[key] for key in ("goal", "domain", "record_sha256", "math_sha256")},
                    **{"eval_" + key: e[key] for key in ("goal", "domain", "record_sha256", "math_sha256")},
                    "train_conditions": t["key_conditions"], "eval_conditions": e["key_conditions"],
                    "train_steps": t["decisive_steps"], "eval_steps": e["decisive_steps"],
                    "disposition": "UNREVIEWED",
                })
    candidates.sort(key=lambda c: (c["train_id"], c["eval_id"]))
    family_total = sum(f["pairs"] for f in family_counts)
    all_pairs = len(train) * len(evaluation)
    return {
        "schema": "deep-semantic-candidates-v2",
        "core_manifest_sha256": core.CORE_MANIFEST_SHA256,
        "input_bindings": inputs, "actual_sources_and_records_verified": True,
        "signature_coverage": "COMPLETE", "covered_groups": groups,
        "train_side": len(train), "eval_side": len(evaluation),
        "all_record_pairs": all_pairs, "family_pairs_total": family_total,
        "outside_family_pairs_not_screened": all_pairs - family_total,
        "family_pair_counts": family_counts,
        "filter": {"same_goal_label_group": True, "steps_jaccard_minimum": "1/4", "family_required": True},
        "candidate_count": len(candidates), "candidates": candidates,
        "family_pairs_not_flagged": family_total - len(candidates),
        "nonflagged_semantic_verdict": "NOT_REVIEWED",
        "candidate_generation_exhaustive": False,
        "semantic_isolation": "NOT_ESTABLISHED", "production": "CLOSED", "PASS_CORE_SCOPE_issued": False,
        "limitations": [
            "Only identical actual category/sub_category families are screened.",
            "Finite goal aliases and literal step sets miss synonymous or reformulated cores.",
            "Unflagged pairs are not semantically excluded; zero candidates cannot certify isolation.",
            "Extra training subquestions do not remove leakage of an embedded evaluation task.",
        ],
    }

def generate(input_path, out_path):
    sigs, inputs, records = population(input_path)
    report = build_report(sigs, inputs, records)
    report["generator_sha256"] = core.digest(Path(__file__).read_bytes())
    core.publish(out_path, {"deep-candidates.json": core.encoded(report)})
    print(json.dumps({k: report[k] for k in ("candidate_count", "family_pairs_total", "family_pairs_not_flagged", "semantic_isolation")}, ensure_ascii=False))
    return 0

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        return generate(args.input, args.out)
    except (ValueError, KeyError, TypeError, IndexError, OSError) as exc:
        print(json.dumps({"status": "FAIL_BOUND_CANDIDATE_SCREEN", "error": str(exc), "semantic_isolation": "NOT_ESTABLISHED", "production": "CLOSED"}, ensure_ascii=False))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
