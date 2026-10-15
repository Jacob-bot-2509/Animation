"""Validate explicit version-bound pair decisions; never certify global isolation."""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys

if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
import deep_isolation_candidates as deep
core = deep.core

def disposed(candidate_path, expected_sha256, decisions_path, out_path):
    raw = core.checked_path(candidate_path, core.ROOT).read_bytes()
    if core.digest(raw) != expected_sha256:
        raise ValueError("Candidate submission hash mismatch")
    candidate = core.read_json(raw)
    if candidate.get("core_manifest_sha256") != core.CORE_MANIFEST_SHA256:
        raise ValueError("Candidate refers to a different current core")
    inputs = candidate["input_bindings"]
    if len(inputs) != 1:
        raise ValueError("Exactly one complete signature input required")
    sig_path = core.checked_path(core.ROOT / inputs[0]["path"], core.ROOT)
    sigs, actual_inputs, records = deep.population(sig_path)
    expected = deep.build_report(sigs, actual_inputs, records)
    generator_hash = core.digest(Path(deep.__file__).read_bytes())
    expected["generator_sha256"] = generator_hash
    if candidate != expected:
        raise ValueError("Candidate content/source/counts differ from actual recomputation")
    decision_raw = core.checked_path(decisions_path, core.ROOT).read_bytes()
    decision_doc = core.read_json(decision_raw)
    if decision_doc.get("candidate_sha256") != expected_sha256:
        raise ValueError("Decision document not bound to submitted candidate version")
    by_pair = {(c["train_id"], c["eval_id"]): c for c in candidate["candidates"]}
    seen, rows = set(), []
    for d in decision_doc["rows"]:
        key = (d["train_id"], d["eval_id"])
        if key in seen or key not in by_pair:
            raise ValueError("Duplicate/unknown decision pair")
        seen.add(key)
        c = by_pair[key]
        for f in ("train_record_sha256", "eval_record_sha256"):
            if d.get(f) != c[f]:
                raise ValueError("Decision record version mismatch")
        if d.get("verdict") not in ("SAME_CORE", "DIFFERENT_CORE", "NEEDS_REVIEW"):
            raise ValueError("Invalid decision verdict")
        reason = d.get("pairwise_reason")
        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("Nonempty independent mathematical reason required")
        rows.append({**c, "disposition": d["verdict"], "pairwise_reason": reason})
    if seen != set(by_pair):
        raise ValueError("Missing candidate pair dispositions")
    counts = Counter(r["disposition"] for r in rows)
    report = {
        "schema": "deep-candidates-disposed-v2", "core_manifest_sha256": core.CORE_MANIFEST_SHA256,
        "candidate_binding": {"path": candidate_path.relative_to(core.ROOT).as_posix(), "sha256": expected_sha256},
        "decision_binding": {"path": decisions_path.relative_to(core.ROOT).as_posix(), "sha256": core.digest(decision_raw)},
        "disposer_sha256": core.digest(Path(__file__).read_bytes()),
        "family_pairs_total": candidate["family_pairs_total"], "flagged_pairs": len(rows),
        "same_core": counts["SAME_CORE"], "different_core": counts["DIFFERENT_CORE"], "needs_review": counts["NEEDS_REVIEW"],
        "family_pairs_not_flagged": candidate["family_pairs_not_flagged"],
        "nonflagged_semantic_verdict": "NOT_REVIEWED",
        "outside_family_pairs_not_screened": candidate["outside_family_pairs_not_screened"],
        "rows": rows, "decision_packaging": "PASS_VERSION_BOUND_DECISION_PACKAGING",
        "independent_reason_correctness": "REQUIRES_SEPARATE_REVIEW_RECEIPT",
        "semantic_isolation": "NOT_ESTABLISHED", "production": "CLOSED", "PASS_CORE_SCOPE_issued": False,
    }
    core.publish(out_path, {"deep-candidates-disposed.json": core.encoded(report)})
    print(json.dumps({k: report[k] for k in ("flagged_pairs", "same_core", "different_core", "needs_review", "semantic_isolation")}, ensure_ascii=False))
    return 3 if counts["SAME_CORE"] or counts["NEEDS_REVIEW"] else 0

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--candidate-sha256", required=True)
    parser.add_argument("--decisions", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        return disposed(args.candidates.absolute(), args.candidate_sha256, args.decisions.absolute(), args.out)
    except (ValueError, KeyError, TypeError, IndexError, OSError) as exc:
        print(json.dumps({"status": "FAIL_BOUND_PAIR_DISPOSITIONS", "error": str(exc), "semantic_isolation": "NOT_ESTABLISHED", "production": "CLOSED"}, ensure_ascii=False))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
