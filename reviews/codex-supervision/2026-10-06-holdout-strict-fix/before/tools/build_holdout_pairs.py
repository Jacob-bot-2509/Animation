"""Build the independent leakage-holdout pair set (2026-10-06).

Independence contract:
- Train side = the 264 new draft records (selected versions per
  draft-selection.json). These did not exist while the structural screen and
  kp rules were developed, so no detector score or rule was ever influenced
  by them.
- Query side = frozen eval (300) + test (150) records.
- Sampling is stratified by 考点 metadata (category / sub_category / concept
  / parent lineage), NOT by any similarity score, so text-similar and
  text-different structural clones (the calc-series-018 failure mode) are
  both represented fairly.

Strata (kept OUT of the labeling file to keep labels blind):
  S1a parent-derived : drafts whose parent_training_ids were involved in the
       17 dev-positive leakage labels or the 5 quarantined pairs, paired with
       that same query. Tests whether the rules generalize to NEW instances
       (reworded drafts) of known-leaking structures.
  S1b same-sub      : exact sub_category matches (concept-stratified sample).
  S2  same-cat      : same category, different sub_category.
  S3  cross-cat     : different category.

Outputs:
  reviews/2026-10-06-independent-holdout/holdout-pairs.json  (BLIND: no stratum,
      no detector scores, no parent ids -> for the independent labeler)
  Strata are NOT written to disk: score_holdout.py rebuilds them
  deterministically (same seed, same algorithm) so the labeler cannot see them.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from draft_io import selected_path, verify_entry  # noqa: E402

DRAFTS = ROOT / "reviews/2026-10-05-training-diversity-drafts"
EVAL = ROOT / "data/v2/eval/dataset_eval.jsonl"
TEST = ROOT / "data/v2/test/dataset_test.jsonl"
DEV_LABELS = (ROOT / "reviews/codex-supervision/2026-10-05-readiness-completion"
              / "independent-leakage-labels-v2.json")
DEV_POP = (ROOT / "reviews/codex-supervision/2026-10-05-readiness-completion"
           / "leakage-population.json")
QUARANTINE = (ROOT / "reviews/codex-supervision/2026-10-05-math-template-followup-v2"
              / "new-overlap-before-fix.json")
OUT_DIR = ROOT / "reviews/2026-10-06-independent-holdout"

SEED = 20261006
S1A_MAX_DRAFTS_PER_PAIR = 3
S1B_PER_CONCEPT = 2
S2_PER_CATEGORY = 12
S3_TOTAL = 32


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _pair_id(q_problem: str, t_problem: str) -> str:
    return hashlib.sha256((_sha(q_problem) + _sha(t_problem)).encode()).hexdigest()[:20]


def load_drafts() -> list[dict]:
    sel_path = DRAFTS / "draft-selection.json"
    sel_bytes = sel_path.read_bytes()
    sel = json.loads(sel_bytes.decode("utf-8-sig"))
    if sel.get("schema") != 2:
        raise ValueError("schema2 selector required")
    rows: list[dict] = []
    for entry in sel["entries"]:
        path = selected_path(DRAFTS, entry)
        verify_entry(path, entry, hash_algorithm=sel["hash_algorithm"])
        for line in path.read_text("utf-8-sig").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    if sel_path.read_bytes() != sel_bytes:
        raise ValueError("selection changed during load")
    return rows


def load_queries() -> tuple[list[dict], dict[str, dict]]:
    """All eval/test records + by-problem_id lookup (first record wins)."""
    recs: list[dict] = []
    by_pid: dict[str, dict] = {}
    for path in (EVAL, TEST):
        for line in path.read_text("utf-8-sig").splitlines():
            if line.strip():
                rec = json.loads(line)
                rec["_source"] = str(path.relative_to(ROOT))
                recs.append(rec)
                pid = rec.get("problem_id") or rec.get("id")
                by_pid.setdefault(pid, rec)
    return recs, by_pid


def parent_positive_queries() -> list[tuple[str, str]]:
    """(parent_train_id, query_problem_id) from dev labels + quarantine."""
    out: list[tuple[str, str]] = []
    labels = json.loads(DEV_LABELS.read_text(encoding="utf-8"))
    pop = json.loads(DEV_POP.read_text(encoding="utf-8"))
    h2ids: dict[str, list[str]] = {}
    for p in pop["pairs"]:
        for side in ("query", "train"):
            h2ids[p[side]["hash"]] = [s["id"] for s in p[side]["sources"]]
    for a in labels["annotations"]:
        if a["label"] != "泄漏":
            continue
        tids = h2ids.get(a["train_hash"], [])
        qids = h2ids.get(a["query_hash"], [])
        if tids and qids:
            out.append((tids[0], qids[0].rsplit("-s", 1)[0] if "-s" in qids[0] else qids[0]))
    quar = json.loads(QUARANTINE.read_text(encoding="utf-8"))
    for p in quar.get("new_pairs", []):
        out.append((p["train_id"], p["query_id"].rsplit("-s", 1)[0] if "-s" in p["query_id"] else p["query_id"]))
    # dedupe, keep order
    seen, dedup = set(), []
    for t, q in out:
        if (t, q) not in seen:
            seen.add((t, q))
            dedup.append((t, q))
    return dedup


def build_pairs(drafts, recs, by_pid, rng) -> tuple[list[dict], dict[str, str]]:
    strata: dict[str, str] = {}
    pairs: list[dict] = []
    by_id = {d["id"]: d for d in drafts}

    def add(train: dict, query: dict, stratum: str) -> None:
        pid = _pair_id(query["problem"], train["problem"])
        if pid in strata:
            return
        strata[pid] = stratum
        pairs.append({
            "pair_id": pid,
            "query": {"id": query.get("problem_id") or query.get("id"),
                      "problem": query["problem"], "category": query["category"]},
            "train": {"id": train["id"], "problem": train["problem"],
                      "category": train["category"]},
        })

    # S1a: parent-derived. Drafts whose parents leaked a query, re-paired with it.
    for parent_tid, query_pid in parent_positive_queries():
        q = by_pid.get(query_pid) or by_pid.get(query_pid + "-s1")
        if q is None:
            continue
        kids = [d for d in drafts if parent_tid in d.get("parent_training_ids", [])]
        rng.shuffle(kids)
        for d in kids[:S1A_MAX_DRAFTS_PER_PAIR]:
            add(d, q, "S1a_parent_derived")

    # S1b: exact same-sub, per concept
    by_sub: dict[str, list[dict]] = defaultdict(list)
    for q in recs:
        by_sub[(q["category"], q.get("sub_category", ""))].append(q)
    per_concept: dict[str, list[dict]] = defaultdict(list)
    for d in drafts:
        for q in by_sub[(d["category"], d["sub_category"])]:
            per_concept[d["concept_id"]].append((d, q))
    for concept in sorted(per_concept):
        pool = per_concept[concept]
        rng.shuffle(pool)
        taken = 0
        for d, q in pool:
            if taken >= S1B_PER_CONCEPT:
                break
            if _pair_id(q["problem"], d["problem"]) in strata:
                continue
            add(d, q, "S1b_same_sub")
            taken += 1

    # S2: same category, different sub
    by_cat_q: dict[str, list[dict]] = defaultdict(list)
    for q in recs:
        by_cat_q[q["category"]].append(q)
    for cat in sorted({d["category"] for d in drafts}):
        pool = [(d, q) for d in drafts if d["category"] == cat
                for q in by_cat_q[cat] if q.get("sub_category") != d["sub_category"]]
        rng.shuffle(pool)
        n = 0
        for d, q in pool:
            if n >= S2_PER_CATEGORY:
                break
            add(d, q, "S2_same_cat_diff_sub")
            n += 1

    # S3: cross-category
    cats = sorted({d["category"] for d in drafts})
    cross = [(d, q) for d in drafts for cat in cats if cat != d["category"]
             for q in by_cat_q[cat]]
    rng.shuffle(cross)
    n = 0
    for d, q in cross:
        if n >= S3_TOTAL:
            break
        add(d, q, "S3_cross_cat")
        n += 1
    return pairs, strata


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-dir", type=Path, default=OUT_DIR)
    args = ap.parse_args(argv)
    try:
        drafts = load_drafts()
        recs, by_pid = load_queries()
        rng = random.Random(SEED)
        pairs, strata = build_pairs(drafts, recs, by_pid, rng)
        args.out_dir.mkdir(parents=True, exist_ok=True)
        pairs_path = args.out_dir / "holdout-pairs.json"
        if pairs_path.exists():
            raise ValueError("output exists: use a new directory")
        blind = {
            "schema": "holdout-pairs-v1",
            "created": "2026-10-06",
            "seed": SEED,
            "sampling": "metadata-stratified; NO similarity scores; strata hidden from labeler",
            "labeling_rule": "独立标注:本质考点+数学对象/题型/目标及求解结构均不变的文本变体=泄漏;共享知识点本身不算泄漏",
            "labeler": "codex-independent; conflicts -> user adjudication",
            "pairs": pairs,
        }
        with pairs_path.open("x", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(blind, ensure_ascii=False, indent=2) + "\n")
        from collections import Counter
        print(json.dumps({"pairs": len(pairs), "strata": dict(Counter(strata.values())),
                          "out": str(pairs_path)}, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("[FAIL]", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
