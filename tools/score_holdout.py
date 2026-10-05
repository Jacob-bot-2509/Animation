"""Score the independent holdout: production screens vs independent labels.

Inputs:
  reviews/2026-10-06-independent-holdout/holdout-pairs.json   (blind pairs)
  reviews/2026-10-06-independent-holdout/holdout-labels.json  (Codex labels)
Strata are rebuilt deterministically from the pairs (same seed/algorithm as
build_holdout_pairs; nothing on disk can reveal them to the labeler).

Screens measured (exactly what production runs):
  A. combined rule   = 考点签名一致 AND 5-gram Jaccard >= 2/5  (validate.py)
  B. structural screen = structure_keys overlap -> candidate   (structural_leakage.compare)
  C. union (operational gate) = A OR B

Targets (B5 strict): recall >= 19/20 AND fpr <= 1/100 -> CALIBRATED, else
UNCALIBRATED with exact fractions reported honestly.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

from animtrain.near_dup import shingles  # noqa: E402
from animtrain.kp_rule import kp_signature  # noqa: E402
from animtrain.structural_leakage import compare, implementation_sha256  # noqa: E402
from build_holdout_pairs import (SEED, load_drafts, load_queries,  # noqa: E402
                                 build_pairs, EVAL, TEST)

OUT_DIR = ROOT / "reviews/2026-10-06-independent-holdout"
MIN_RECALL = Fraction(19, 20)
MAX_FPR = Fraction(1, 100)
J5_THRESHOLD = Fraction(2, 5)


def load_labels(path: Path) -> dict[str, dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "holdout-labels-v1":
        raise ValueError("labels schema mismatch")
    out = {}
    for lab in data["labels"]:
        if lab["pair_id"] in out:
            raise ValueError("duplicate label: " + lab["pair_id"])
        out[lab["pair_id"]] = lab
    return out


def sig_of(rec: dict):
    """考点签名;无法归类且无 sub_category 时按规则拒绝签名(不得当共同考点)。"""
    try:
        return kp_signature(rec)
    except ValueError:
        return None


def j5_fraction(a: str, b: str) -> Fraction:
    sa, sb = shingles(a), shingles(b)
    if not sa or not sb:
        return Fraction(0)
    return Fraction(len(sa & sb), len(sa | sb))


def score(pairs, strata, labels, query_lookup, draft_lookup):
    rows = []
    cm = {"combined": Counter(), "structural": Counter(), "union": Counter()}
    per_stratum: dict[str, dict[str, Counter]] = defaultdict(lambda: {k: Counter() for k in cm})
    for p in pairs:
        pid = p["pair_id"]
        lab = labels.get(pid)
        if lab is None:
            raise ValueError("missing label for pair: " + pid)
        label = lab["label"]
        if label not in ("泄漏", "不泄漏"):
            raise ValueError("bad label value for " + pid)
        q_rec = query_lookup[p["query"]["id"]]
        t_rec = draft_lookup[p["train"]["id"]]
        sq, st = sig_of(q_rec), sig_of(t_rec)
        sig_equal = sq is not None and sq == st
        j5 = j5_fraction(p["query"]["problem"], p["train"]["problem"])
        combined = sig_equal and j5 >= J5_THRESHOLD
        structural = bool(compare(p["query"]["problem"], p["train"]["problem"])["candidate"])
        preds = {"combined": combined, "structural": structural,
                 "union": combined or structural}
        truth = label == "泄漏"
        for screen, pred in preds.items():
            key = ("tp" if pred else "fn") if truth else ("fp" if pred else "tn")
            cm[screen][key] += 1
            per_stratum[strata[pid]][screen][key] += 1
        rows.append({"pair_id": pid, "label": label, "sig_equal": sig_equal,
                     "j5": str(j5), "combined": combined,
                     "structural": structural, "union": preds["union"],
                     "reason": lab.get("reason", "")[:160]})

    def metrics(c: Counter) -> dict:
        tp, fp, fn, tn = c["tp"], c["fp"], c["fn"], c["tn"]
        recall = Fraction(tp, tp + fn) if tp + fn else None
        fpr = Fraction(fp, fp + tn) if fp + tn else None
        calibrated = (recall is not None and fpr is not None
                      and recall >= MIN_RECALL and fpr <= MAX_FPR)
        return {"tp": tp, "fp": fp, "fn": fn, "tn": tn,
                "recall": str(recall) if recall is not None else None,
                "fpr": str(fpr) if fpr is not None else None,
                "calibrated": calibrated}

    report = {
        "schema": "holdout-score-v1",
        "targets": {"min_recall": str(MIN_RECALL), "max_fpr": str(MAX_FPR),
                    "j5_threshold": str(J5_THRESHOLD)},
        "screens": {k: metrics(c) for k, c in cm.items()},
        "per_stratum": {s: {k: metrics(c) for k, c in sc.items()}
                        for s, sc in sorted(per_stratum.items())},
        "rows": rows,
    }
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--pairs", type=Path, default=OUT_DIR / "holdout-pairs.json")
    ap.add_argument("--labels", type=Path, default=OUT_DIR / "holdout-labels.json")
    ap.add_argument("--out", type=Path, default=OUT_DIR / "holdout-score.json")
    args = ap.parse_args(argv)
    try:
        pairs_data = json.loads(args.pairs.read_text(encoding="utf-8"))
        pairs = pairs_data["pairs"]
        labels = load_labels(args.labels)
        if set(labels) != {p["pair_id"] for p in pairs}:
            raise ValueError("labels do not cover the pairs 1:1")
        drafts = load_drafts()
        recs, by_pid = load_queries()
        rng = random.Random(SEED)
        _, strata = build_pairs(drafts, recs, by_pid, rng)
        if set(strata) != {p["pair_id"] for p in pairs}:
            raise ValueError("strata rebuild mismatch (data changed since building)")
        query_lookup = {q.get("problem_id") or q.get("id"): q for q in recs}
        draft_lookup = {d["id"]: d for d in drafts}
        report = score(pairs, strata, labels, query_lookup, draft_lookup)
        report["bindings"] = {
            "pairs_sha256": hashlib.sha256(args.pairs.read_bytes()).hexdigest(),
            "labels_sha256": hashlib.sha256(args.labels.read_bytes()).hexdigest(),
            "structural_implementation_sha256": implementation_sha256(),
            "kp_rule_sha256": hashlib.sha256(
                (ROOT / "src/animtrain/kp_rule.py").read_bytes()).hexdigest(),
            "near_dup_sha256": hashlib.sha256(
                (ROOT / "src/animtrain/near_dup.py").read_bytes()).hexdigest(),
            "seed": SEED,
        }
        if args.out.exists():
            raise ValueError("output exists: use a new path")
        with args.out.open("x", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        print(json.dumps({"screens": report["screens"], "strata": {
            s: {k: v["calibrated"] for k, v in sc.items()}
            for s, sc in report["per_stratum"].items()}}, ensure_ascii=False, indent=1))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("[FAIL]", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
