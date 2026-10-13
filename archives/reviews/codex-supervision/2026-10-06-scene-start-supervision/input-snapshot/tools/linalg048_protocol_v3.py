"""Source-bound v3 review validation. This checks attestations, not semantic truth."""
from holdout_contract import required_text, object_sha, RULE_SHA

REVIEW_SCHEMA = "linalg048-manual-acceptance-v3"
DENSITY_SCHEMA = "linalg048-train-variant-density-v1"


def reference(record):
    ref = record.get("review_evidence")
    if not isinstance(ref, dict):
        raise ValueError("bound independent review evidence required")
    path, digest = (required_text(ref, k) for k in ("path", "raw_sha256"))
    if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
        raise ValueError("invalid review evidence hash")
    return path, digest


def require_density(density, rows, policy, manifest_sha, policy_sha):
    if density.get("schema") != DENSITY_SCHEMA or density.get("status") != "INDEPENDENT_VERIFIED":
        raise ValueError("independently reviewed full training family ledger required")
    required_text(density, "reviewer")
    refs = [reference(density)]
    if density.get("manifest_sha256") != manifest_sha or density.get("policy_sha256") != policy_sha:
        raise ValueError("density manifest/policy binding mismatch")
    definitions = policy.get("concepts")
    if not isinstance(definitions, list) or not definitions:
        raise ValueError("concept definitions required")
    concepts = {required_text(c, "id"): c for c in definitions}
    minimum, forms_min = policy.get("min_reviewed_samples_per_concept"), policy.get("min_distinct_variant_kinds_per_concept")
    if (len(concepts) != len(definitions) or policy.get("schema") != 1
            or type(minimum) is not int or minimum < 5
            or type(forms_min) is not int or forms_min < 3):
        raise ValueError("density policy cannot downgrade 5 tasks / 3 forms")
    reviews, families = density.get("record_reviews"), density.get("families")
    if not isinstance(reviews, list) or not isinstance(families, list) or not families:
        raise ValueError("full training reviews and families required")
    assignments = {}
    for rec in reviews:
        pid = required_text(rec, "id")
        if pid in assignments or pid not in rows or rec.get("record_sha256") != object_sha(rows[pid]):
            raise ValueError("duplicate, unknown or stale training review")
        if rec.get("independent_math_verified") is not True or rec.get("independent_core_verified") is not True:
            raise ValueError("training core/math review pending")
        refs.append(reference(rec))
        assignments[pid] = required_text(rec, "core_family_id")
    if set(assignments) != set(rows):
        raise ValueError("full active training review coverage required")
    seen_families, seen_members, seen_signatures = set(), set(), set()
    counts = {cid: 0 for cid in concepts}
    forms = {cid: set() for cid in concepts}
    normalized = []
    for family in families:
        fid = required_text(family, "id")
        cid, kind = (required_text(family, k) for k in ("concept_id", "variant_kind"))
        members = family.get("member_ids")
        if (fid in seen_families or cid not in concepts or not isinstance(members, list)
                or not members or any(not isinstance(x, str) for x in members)
                or len(members) != len(set(members))):
            raise ValueError("duplicate or invalid core family")
        signature = family.get("core_signature")
        for key in ("object", "conditions", "goal", "solution_structure"):
            required_text(signature, key)
        signature_hash = object_sha({k: signature[k].strip() for k in ("object", "conditions", "goal", "solution_structure")})
        if signature_hash in seen_signatures:
            raise ValueError("identical core signature split across families")
        seen_signatures.add(signature_hash)
        required_text(family, "reason")
        refs.append(reference(family))
        for pid in members:
            if pid in seen_members or assignments.get(pid) != fid:
                raise ValueError("overlapping or inconsistent core family members")
            if rows[pid].get("category") != concepts[cid].get("category"):
                raise ValueError("family concept/category mismatch")
            seen_members.add(pid)
        seen_families.add(fid)
        counts[cid] += 1  # one independent task per core family, never per clone
        forms[cid].add(kind)
        normalized.append({"id": fid, "concept_id": cid, "variant_kind": kind,
                           "member_ids": members, "independent_task_count": 1})
    if seen_members != set(rows) or set(assignments.values()) != seen_families:
        raise ValueError("family coverage mismatch")
    summary = {cid: {"independent_tasks": counts[cid], "distinct_forms": len(forms[cid])}
               for cid in concepts}
    complete = all(counts[c] >= minimum and len(forms[c]) >= forms_min for c in concepts)
    target = policy.get("target_max_per_concept")
    if type(target) is not int or target < minimum:
        raise ValueError("invalid policy target")
    notes = density.get("density_notes", {})
    if not isinstance(notes, dict):
        raise ValueError("density notes must be an object")
    for cid in concepts:
        if counts[cid] > target:
            note = notes.get(cid)
            required_text(note, "reviewer")
            required_text(note, "reason")
            refs.append(reference(note))
    if "claimed_concept_counts" in density and density["claimed_concept_counts"] != summary:
        raise ValueError("density claimed counts mismatch")
    if "concept_coverage_complete" in density and density["concept_coverage_complete"] is not complete:
        raise ValueError("density claimed completion mismatch")
    return {"assignments": assignments, "families": normalized, "concept_counts": summary,
            "concept_coverage_complete": complete, "training_readiness_certified": False,
            "target_max_per_concept": policy.get("target_max_per_concept"),
            "review_references": refs}


def require_manual_review(review, evidence, evidence_sha, density_summary, candidate_id):
    if review.get("schema") != REVIEW_SCHEMA or review.get("independent_semantic_review_status") != "COMPLETE":
        raise ValueError("completed independent manual acceptance v3 required")
    required_text(review, "reviewer")
    refs = [reference(review)]
    expected = {"render_evidence_raw_sha256": evidence_sha,
                "candidate_raw_sha256": evidence["candidate_raw_sha256"],
                "scene_raw_sha256": evidence["scene"]["raw_sha256"],
                "media_raw_sha256": evidence["render_result"]["output"]["sha256"],
                "labeling_rule_sha256": RULE_SHA}
    if any(review.get(k) != v for k, v in expected.items()):
        raise ValueError("manual v3 subject/rule binding mismatch")
    if candidate_id not in density_summary["assignments"]:
        raise ValueError("candidate missing from full training family ledger")
    candidate_family = density_summary["assignments"][candidate_id]
    visual = review.get("visual")
    if not isinstance(visual, dict) or visual.get("verdict") != "ACCEPT":
        raise ValueError("actual visual acceptance required")
    required_text(visual, "reason")
    refs.append(reference(visual))
    subjects = evidence["semantic_subjects"]
    expected_keys = set()
    for item in subjects:
        key = tuple(required_text(item, k) for k in ("split", "id", "problem_sha256"))
        if key[0] not in ("train", "eval", "test") or key in expected_keys or (key[0] == "train" and key[1] == candidate_id):
            raise ValueError("duplicate or invalid receipt subject")
        expected_keys.add(key)
    labels = review.get("semantic_pairs")
    if not isinstance(labels, list) or len(labels) != len(subjects):
        raise ValueError("full manual review coverage required")
    seen, variants = set(), []
    for label in labels:
        key = tuple(required_text(label, k) for k in ("split", "id", "problem_sha256"))
        if key not in expected_keys or key in seen:
            raise ValueError("duplicate or wrong manual review subject")
        seen.add(key)
        required_text(label, "reason")
        refs.append(reference(label))
        verdict = label.get("verdict")
        if verdict not in ("DIFFERENT_CORE_TASK", "SAME_CORE_TRAIN_VARIANT"):
            raise ValueError("cross-split leakage or uncertainty requires revision")
        same_family = False
        if key[0] == "train":
            if key[1] not in density_summary["assignments"]:
                raise ValueError("training subject absent from density ledger")
            same_family = density_summary["assignments"][key[1]] == candidate_family
        if verdict == "SAME_CORE_TRAIN_VARIANT":
            if key[0] != "train" or not same_family or label.get("core_family_id") != candidate_family:
                raise ValueError("held-out or inconsistent train variant")
            required_text(label, "equivalence_mapping")
            variants.append(key[1])
        elif same_family:
            raise ValueError("same family cannot be labeled DIFFERENT")
    return {"reviewer": review["reviewer"], "train_variants": variants,
            "review_references": refs, "accepted_for_inactive_proposal_only": True}
