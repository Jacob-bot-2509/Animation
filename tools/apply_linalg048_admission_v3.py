"""Validate v3 review/density and publish a fresh INACTIVE proposal only.

The old render receipt and v2 entry points remain immutable. Execution evidence
and this admission validator have separate source bindings; no old hash is reset.
"""
import argparse
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/"tools"), str(ROOT/"src")]
from holdout_contract import Snapshot, json_object, required_text, raw_sha, object_sha, write_new_json
import admit_linalg048_v3 as render
from linalg048_protocol_v3 import require_density, require_manual_review, REVIEW_SCHEMA, DENSITY_SCHEMA

MANIFEST = ROOT/"data/manifest.json"
POLICY = ROOT/"configs/training_diversity_policy.json"


def load_train(snapshot, manifest):
    rows = {}
    for entry in manifest["entries"]:
        if entry.get("split") != "train":
            continue
        path = (MANIFEST.parent/required_text(entry, "path")).resolve()
        if not path.is_relative_to(MANIFEST.parent):
            raise ValueError("training path outside data")
        data = snapshot.read(path)
        if raw_sha(data) != entry.get("sha256") or len(data) != entry.get("size"):
            raise ValueError("stale training source")
        for line in data.decode("utf-8-sig").splitlines():
            if not line.strip():
                continue
            row = json_object(line.encode("utf-8"))
            pid = required_text(row, "id")
            for field in ("problem", "solution", "answer", "category"):
                required_text(row, field)
            if pid in rows or not isinstance(row.get("scene_spec"), dict):
                raise ValueError("duplicate or invalid training record")
            rows[pid] = row
    if not rows:
        raise ValueError("full active training pool required")
    return rows


def bind_references(snapshot, refs):
    for rel, digest in set(refs):
        data = snapshot.read(ROOT/rel)
        if not data or raw_sha(data) != digest:
            raise ValueError("independent review evidence binding mismatch")


def publish_proposal(out, render_path, acceptance_path, density_path):
    out = Path(out).resolve()
    if not out.is_relative_to(ROOT) or out.exists():
        raise ValueError("new project proposal path required")
    snapshot = Snapshot(ROOT)
    for rel in ("tools/apply_linalg048_admission_v3.py", "tools/linalg048_protocol_v3.py", "tools/holdout_contract.py"):
        snapshot.read(ROOT/rel)
    acceptance = json_object(snapshot.read(acceptance_path))
    if acceptance.get("schema") != REVIEW_SCHEMA or acceptance.get("independent_semantic_review_status") != "COMPLETE":
        raise ValueError("completed independent manual acceptance v3 required")
    density = json_object(snapshot.read(density_path))
    if density.get("schema") != DENSITY_SCHEMA or density.get("status") != "INDEPENDENT_VERIFIED":
        raise ValueError("independently reviewed training families required")
    manifest_bytes, policy_bytes = snapshot.read(MANIFEST), snapshot.read(POLICY)
    manifest, policy = json_object(manifest_bytes), json_object(policy_bytes)
    rows = load_train(snapshot, manifest)
    summary = require_density(density, rows, policy, raw_sha(manifest_bytes), raw_sha(policy_bytes))
    # The old verifier requires its exact execution-era 32-source set.
    # Validate it independently, then merge bytes into the admission snapshot.
    render_snapshot = Snapshot(ROOT)
    candidate, evidence = render.verify_evidence(render_snapshot, render_path)
    for path, data in render_snapshot.data.items():
        if snapshot.read(path) != data:
            raise ValueError("render/admission source snapshots disagree")
    render_snapshot.check_unchanged()
    cid = required_text(candidate, "id")
    if cid not in rows or any(rows[cid].get(k) != candidate.get(k) for k in ("problem", "solution", "answer", "scene_spec")):
        raise ValueError("candidate differs from active training mathematics")
    manual = require_manual_review(acceptance, evidence, raw_sha(snapshot.read(render_path)), summary, cid)
    if acceptance.get("density_raw_sha256") != raw_sha(snapshot.read(density_path)):
        raise ValueError("manual density binding mismatch")
    bind_references(snapshot, summary["review_references"]+manual["review_references"])
    result = {"schema": "linalg048-admission-proposal-v3",
              "status": "LOCAL_MANUAL_AND_FAMILY_REVIEW_VERIFIED_PENDING_VERSIONED_PROMOTION",
              "active_data_modified": False, "training_admitted": False,
              "global_leakage_free_certified": False, "calibration_eligible": False,
              "formal_training_readiness_certified": False,
              "candidate": candidate, "candidate_record_sha256": object_sha(candidate),
              "render_evidence_raw_sha256": raw_sha(snapshot.read(render_path)),
              "acceptance_raw_sha256": raw_sha(snapshot.read(acceptance_path)),
              "density_raw_sha256": raw_sha(snapshot.read(density_path)),
              "original_render_source_bindings": evidence["source_bindings"],
              "current_admission_source_bindings": snapshot.bindings(),
              "train_variants": manual["train_variants"],
              "family_concept_counts": summary["concept_counts"],
              "family_concept_coverage_complete": summary["concept_coverage_complete"],
              "reviewer": manual["reviewer"],
              "next_step": "Unselected proposal only. All existing training/asset/calibration/isolation gates still apply."}
    write_new_json(out, result, snapshot)
    return result


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    for flag in ("out", "render-evidence", "acceptance", "density"):
        ap.add_argument("--"+flag, required=True, type=Path)
    args = ap.parse_args(argv)
    try:
        result = publish_proposal(args.out, args.render_evidence, args.acceptance, args.density)
        print(result["status"])
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print("[FAIL]", exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
