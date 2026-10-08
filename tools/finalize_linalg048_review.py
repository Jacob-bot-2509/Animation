"""Validate complete review coverage and publish a fresh, pending review artifact.

This validates identities and evidence fields, not the truth of semantic reasons.
It never emits manual acceptance or modifies active data.
"""
from __future__ import annotations
import argparse
from collections import Counter
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "src")]
from holdout_contract import (Snapshot, json_object, required_text, raw_sha,
                              object_sha, RULE_SHA, write_new_json)

PACKET = ROOT / "reviews/codex-supervision/2026-10-06-bound-receipt-semantic-review/pending-review-packet.json"
PACKET_SHA = "eb37c77a6c2619726f2b297ae92ec12778d908140c542af5893970ab8578b401"
VALID = ("DIFFERENT_CORE_TASK", "SAME_CORE_TRAIN_VARIANT",
         "SAME_CORE_CROSS_SPLIT", "UNCERTAIN")


def subject_key(row):
    split, pid = (required_text(row, f) for f in ("split", "id"))
    if split not in ("train", "eval", "test"):
        raise ValueError("invalid subject split")
    return split, pid


def validate_packet(packet, expected_size=296):
    if packet.get("schema") != "linalg048-semantic-review-packet-v1":
        raise ValueError("pending packet schema required")
    if packet.get("labeling_rule_sha256") != RULE_SHA:
        raise ValueError("labeling rule binding mismatch")
    if (packet.get("reviewer") is not None or packet.get("accepted") is not False
            or packet.get("training_admitted") is not False):
        raise ValueError("pending packet required")
    subjects, material = packet.get("semantic_pairs"), packet.get("review_material")
    if not isinstance(subjects, list) or len(subjects) != expected_size:
        raise ValueError("packet coverage mismatch")
    expected = {}
    for s in subjects:
        key = subject_key(s)
        if key in expected or s.get("verdict") is not None:
            raise ValueError("duplicate or nonpending packet subject")
        expected[key] = required_text(s, "problem_sha256")
    if not isinstance(material, list) or len(material) != expected_size:
        raise ValueError("material coverage mismatch")
    by_key = {}
    for m in material:
        key = subject_key(m)
        if key in by_key or m.get("problem_sha256") != expected.get(key):
            raise ValueError("material identity/hash mismatch")
        rows, hashes = m.get("source_records"), m.get("source_record_sha256")
        if not isinstance(rows, list) or not rows or not isinstance(hashes, list) or len(rows) != len(hashes):
            raise ValueError("full source records and hashes required")
        for row, digest in zip(rows, hashes):
            for field in ("id", "problem", "solution", "answer"):
                required_text(row, field)
            if ((row.get("problem_id") or row["id"]) != key[1]
                    or raw_sha(row["problem"].encode("utf-8")) != expected[key]
                    or object_sha(row) != digest or not isinstance(row.get("scene_spec"), dict)):
                raise ValueError("full source record binding mismatch")
        by_key[key] = m
    if set(by_key) != set(expected):
        raise ValueError("material subject coverage mismatch")
    return expected, by_key


def read_bound_packet(snapshot):
    packet_bytes = snapshot.read(PACKET)
    if raw_sha(packet_bytes) != PACKET_SHA:
        raise ValueError("packet raw hash mismatch")
    packet = json_object(packet_bytes)
    validate_packet(packet)
    bindings = packet.get("source_bindings")
    if not isinstance(bindings, dict) or not bindings:
        raise ValueError("packet source bindings required")
    for rel, meta in bindings.items():
        if not isinstance(meta, dict):
            raise ValueError("invalid packet binding")
        data = snapshot.read(ROOT / rel)
        if raw_sha(data) != meta.get("raw_sha256") or len(data) != meta.get("bytes"):
            raise ValueError("stale packet source: " + rel)
    snapshot.read(ROOT / "tools/holdout_contract.py")
    return packet


def validate_result(packet, workflow, expected_size=296):
    expected, _ = validate_packet(packet, expected_size)
    result = workflow.get("result")
    if not isinstance(result, dict) or not isinstance(result.get("pairs"), list):
        raise ValueError("workflow result/pairs required")
    labels = {}
    for row in result["pairs"]:
        key = subject_key(row)
        if key in labels or key not in expected:
            raise ValueError("duplicate or extra workflow subject")
        verdict = required_text(row, "verdict")
        if verdict not in VALID:
            raise ValueError("invalid verdict")
        if verdict == "SAME_CORE_TRAIN_VARIANT" and key[0] != "train":
            raise ValueError("train variant on a held-out subject")
        if verdict == "SAME_CORE_CROSS_SPLIT" and key[0] not in ("eval", "test"):
            raise ValueError("cross-split label on training subject")
        if "problem_sha256" in row and row["problem_sha256"] != expected[key]:
            raise ValueError("workflow problem hash mismatch")
        labels[key] = {**row, "problem_sha256": expected[key],
                       "reason": required_text(row, "reason"),
                       "evidence": required_text(row, "evidence")}
    if set(labels) != set(expected):
        raise ValueError("missing workflow subject")
    rows = [labels[subject_key(s)] for s in packet["semantic_pairs"]]
    counter = Counter(x["verdict"] for x in rows)
    counts = {v: counter[v] for v in VALID}
    claimed = result.get("counts")
    if (not isinstance(claimed, dict) or set(claimed) != set(VALID)
            or any(type(claimed[v]) is not int or claimed[v] != counts[v] for v in VALID)):
        raise ValueError("workflow counts mismatch")
    lists = {}
    for name, verdict in (("trainVariants", "SAME_CORE_TRAIN_VARIANT"),
                           ("leakage", "SAME_CORE_CROSS_SPLIT"), ("uncertain", "UNCERTAIN")):
        computed = ["|".join(subject_key(x)) for x in rows if x["verdict"] == verdict]
        claim = result.get(name)
        if (not isinstance(claim, list) or any(not isinstance(x, str) for x in claim)
                or len(claim) != len(set(claim)) or set(claim) != set(computed)):
            raise ValueError("workflow classification list mismatch: " + name)
        lists[name] = computed
    return rows, counts, lists


def publish_review(workflow_path, out, journal_path=None):
    out = Path(out).resolve()
    if not out.is_relative_to(ROOT) or out.exists():
        raise ValueError("fresh project output required")
    snapshot = Snapshot(ROOT)
    packet = read_bound_packet(snapshot)
    workflow_bytes = snapshot.read(workflow_path)
    workflow = json_object(workflow_bytes)
    rows, counts, lists = validate_result(packet, workflow)
    workflow_meta = {"result_raw_sha256": raw_sha(workflow_bytes),
                     "reported_agents": workflow.get("agentCount"),
                     "reported_subagent_tokens": workflow.get("totalTokens")}
    if journal_path is not None:
        journal = snapshot.read(journal_path)
        workflow_meta["journal_raw_sha256"] = raw_sha(journal)
    snapshot.read(ROOT / "tools/finalize_linalg048_review.py")
    artifact = {
        "schema": "linalg048-semantic-review-workflow-v2",
        "status": "COVERAGE_VERIFIED_PENDING_PROTOCOL_AND_INDEPENDENT_REVIEW",
        "reviewer": "claude-code workflow; provenance retained, semantic truth requires review",
        "accepted": False, "training_admitted": False, "global_leakage_free_certified": False,
        "bindings": {"packet_raw_sha256": PACKET_SHA, **{key: packet.get(value) for key, value in (
            ("rule_sha256", "labeling_rule_sha256"),
            ("candidate_raw_sha256", "candidate_raw_sha256"),
            ("scene_raw_sha256", "scene_raw_sha256"), ("media_raw_sha256", "media_raw_sha256"),
            ("render_evidence_raw_sha256", "render_evidence_raw_sha256"))}},
        "workflow": workflow_meta, "counts": counts,
        "same_core_train_variant": lists["trainVariants"],
        "same_core_cross_split": lists["leakage"], "uncertain": lists["uncertain"],
        "pairs": rows, "source_bindings": snapshot.bindings(),
        "note": "Coverage and fields are validated; counts do not prove semantic acceptance. "
                "Same-training-split variants require a separate density review; "
                "held-out same-core pairs and unresolved pairs cannot be admitted.",
    }
    write_new_json(out, artifact, snapshot)
    return artifact


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--workflow-result", required=True, type=Path,
                    help="Archived workflow result inside the project")
    ap.add_argument("--journal", type=Path, help="Archived original journal inside the project")
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args(argv)
    try:
        result = publish_review(args.workflow_result, args.out, args.journal)
        print(result["status"], result["counts"])
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print("[FAIL]", exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
