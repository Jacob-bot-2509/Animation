"""Synthetic v3 guard regressions; fixtures do not certify live manual reviews."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/"tools"), str(ROOT/"src")]
from holdout_contract import object_sha, raw_sha, RULE_SHA, Snapshot
import linalg048_protocol_v3 as protocol
import apply_linalg048_admission_v3 as apply

PROOF = b"synthetic independent review evidence; not a live acceptance\n"
REF = {"path": "review.txt", "raw_sha256": raw_sha(PROOF)}
MSHA, PSHA, RSHA = "1"*64, "2"*64, "3"*64

def fixtures():
    rows = {pid: {"id": pid, "problem": "Task "+pid, "solution": "Exact 1/3",
                  "answer": "1/3", "category": "algebra", "scene_spec": {"id": pid}}
            for pid in ("candidate", "peer", "other")}
    policy = {"schema": 1, "min_reviewed_samples_per_concept": 5,
              "min_distinct_variant_kinds_per_concept": 3, "target_max_per_concept": 8,
              "concepts": [{"id": "C1", "category": "algebra"}]}
    density = {"schema": protocol.DENSITY_SCHEMA, "status": "INDEPENDENT_VERIFIED",
               "reviewer": "synthetic-reviewer", "review_evidence": copy.deepcopy(REF),
               "manifest_sha256": MSHA, "policy_sha256": PSHA,
               "record_reviews": [], "families": []}
    for pid, row in rows.items():
        density["record_reviews"].append({"id": pid, "record_sha256": object_sha(row),
            "independent_math_verified": True, "independent_core_verified": True,
            "core_family_id": "F1" if pid != "other" else "F2",
            "review_evidence": copy.deepcopy(REF)})
    for fid, members in (("F1", ["candidate", "peer"]), ("F2", ["other"])):
        density["families"].append({"id": fid, "member_ids": members, "concept_id": "C1",
            "variant_kind": "geometry" if fid == "F1" else "proof",
            "reason": "Synthetic whole-task core classification",
            "core_signature": {"object": fid+" object", "conditions": fid+" conditions",
                               "goal": fid+" goal", "solution_structure": fid+" steps"},
            "review_evidence": copy.deepcopy(REF)})
    subjects = [{"split": split, "id": pid, "problem_sha256": object_sha(pid)}
                for split, pid in (("train", "peer"), ("train", "other"), ("test", "heldout"))]
    evidence = {"candidate_raw_sha256": "4"*64, "scene": {"raw_sha256": "5"*64},
                "render_result": {"output": {"sha256": "6"*64}}, "semantic_subjects": subjects,
                "source_bindings": {"synthetic-only": {"raw_sha256": "7"*64, "bytes": 1}}}
    review = {"schema": protocol.REVIEW_SCHEMA, "independent_semantic_review_status": "COMPLETE",
              "reviewer": "synthetic-reviewer", "review_evidence": copy.deepcopy(REF),
              "render_evidence_raw_sha256": RSHA, "candidate_raw_sha256": "4"*64,
              "scene_raw_sha256": "5"*64, "media_raw_sha256": "6"*64, "labeling_rule_sha256": RULE_SHA,
              "visual": {"verdict": "ACCEPT", "reason": "Synthetic frame inspection",
                         "review_evidence": copy.deepcopy(REF)}, "semantic_pairs": []}
    for subject in subjects:
        label = {**subject, "verdict": "DIFFERENT_CORE_TASK",
                 "reason": "Synthetic full-task comparison", "review_evidence": copy.deepcopy(REF)}
        if subject["id"] == "peer":
            label.update(verdict="SAME_CORE_TRAIN_VARIANT", core_family_id="F1",
                         equivalence_mapping="Synthetic axis permutation; all four core components fixed")
        review["semantic_pairs"].append(label)
    return rows, policy, density, evidence, review

class DensityTests(unittest.TestCase):
    def setUp(self):
        self.rows, self.policy, self.density, self.evidence, self.review = fixtures()
    def check(self):
        return protocol.require_density(self.density, self.rows, self.policy, MSHA, PSHA)
    def reject(self):
        with self.assertRaises(ValueError): self.check()
    def test_family_counts_not_clone_counts(self):
        r = self.check()
        self.assertEqual(r["concept_counts"]["C1"], {"independent_tasks": 2, "distinct_forms": 2})
        self.assertFalse(r["concept_coverage_complete"])
        self.assertFalse(r["training_readiness_certified"])
    def test_pending_rejected(self):
        self.density["status"] = "PENDING"; self.reject()
    def test_wrong_schema_rejected(self):
        self.density["schema"] = "workflow-v2"; self.reject()
    def test_stale_manifest_rejected(self):
        self.density["manifest_sha256"] = "0"*64; self.reject()
    def test_stale_policy_rejected(self):
        self.density["policy_sha256"] = "0"*64; self.reject()
    def test_stale_complete_record_rejected(self):
        self.rows["peer"]["answer"] = "2/3"; self.reject()
    def test_missing_training_review_rejected(self):
        self.density["record_reviews"].pop(); self.reject()
    def test_duplicate_training_review_rejected(self):
        self.density["record_reviews"].append(copy.deepcopy(self.density["record_reviews"][0])); self.reject()
    def test_unreviewed_mathematics_rejected(self):
        self.density["record_reviews"][0]["independent_math_verified"] = False; self.reject()
    def test_unreviewed_core_rejected(self):
        self.density["record_reviews"][0]["independent_core_verified"] = False; self.reject()
    def test_self_declared_string_true_rejected(self):
        self.density["record_reviews"][0]["independent_math_verified"] = "true"; self.reject()
    def test_missing_review_proof_rejected(self):
        del self.density["record_reviews"][0]["review_evidence"]; self.reject()
    def test_invalid_proof_hash_rejected(self):
        self.density["review_evidence"]["raw_sha256"] = "not-a-hash"; self.reject()
    def test_overlapping_family_rejected(self):
        self.density["families"][1]["member_ids"].append("peer"); self.reject()
    def test_missing_member_rejected(self):
        self.density["families"][0]["member_ids"].remove("peer"); self.reject()
    def test_empty_core_signature_rejected(self):
        self.density["families"][0]["core_signature"]["goal"] = " "; self.reject()
    def test_identical_signature_cannot_inflate_count(self):
        self.density["families"][1]["core_signature"] = copy.deepcopy(self.density["families"][0]["core_signature"])
        self.reject()
    def test_category_relabel_rejected(self):
        self.rows["other"]["category"] = "calculus"
        self.density["record_reviews"][-1]["record_sha256"] = object_sha(self.rows["other"])
        self.reject()
    def test_claimed_clone_count_rejected(self):
        self.density["claimed_concept_counts"] = {"C1": {"independent_tasks": 3, "distinct_forms": 2}}
        self.reject()
    def test_claimed_complete_rejected(self):
        self.density["concept_coverage_complete"] = True; self.reject()
    def test_policy_cannot_reduce_task_minimum(self):
        self.policy["min_reviewed_samples_per_concept"] = 2; self.reject()
    def test_policy_cannot_reduce_forms_minimum(self):
        self.policy["min_distinct_variant_kinds_per_concept"] = 2; self.reject()
    def test_uncovered_concept_remains_unready(self):
        self.policy["concepts"].append({"id": "C2", "category": "algebra"})
        r = self.check()
        self.assertEqual(r["concept_counts"]["C2"]["independent_tasks"], 0)
        self.assertFalse(r["concept_coverage_complete"])
    def test_target_exceedance_requires_named_note(self):
        self.policy["min_reviewed_samples_per_concept"] = 5
        self.policy["target_max_per_concept"] = 5
        for i in range(3, 7):
            pid, fid = "extra"+str(i), "F"+str(i)
            row = {**self.rows["other"], "id": pid}
            self.rows[pid] = row
            rec = copy.deepcopy(self.density["record_reviews"][-1])
            rec.update(id=pid, record_sha256=object_sha(row), core_family_id=fid)
            self.density["record_reviews"].append(rec)
            fam = copy.deepcopy(self.density["families"][-1])
            fam.update(id=fid, member_ids=[pid])
            fam["core_signature"]["object"] = fid
            self.density["families"].append(fam)
        self.reject()
        self.density["density_notes"] = {"C1": {"reviewer": "reviewer",
            "reason": "Keep distinct tasks beyond soft target", "review_evidence": REF}}
        r = self.check()
        self.assertEqual(r["concept_counts"]["C1"]["independent_tasks"], 6)
        self.assertFalse(r["training_readiness_certified"])

class ManualTests(unittest.TestCase):
    def setUp(self):
        self.rows, self.policy, self.density, self.evidence, self.review = fixtures()
        self.summary = protocol.require_density(self.density, self.rows, self.policy, MSHA, PSHA)
    def check(self):
        return protocol.require_manual_review(self.review, self.evidence, RSHA, self.summary, "candidate")
    def reject(self):
        with self.assertRaises(ValueError): self.check()
    def test_train_variant_allowed_locally(self):
        r = self.check()
        self.assertEqual(r["train_variants"], ["peer"])
        self.assertTrue(r["accepted_for_inactive_proposal_only"])
    def test_workflow_schema_never_manual_acceptance(self):
        self.review["schema"] = "linalg048-review-workflow-v2"; self.reject()
    def test_pending_independent_review_rejected(self):
        self.review["independent_semantic_review_status"] = "PENDING"; self.reject()
    def test_wrong_media_binding_rejected(self):
        self.review["media_raw_sha256"] = "0"*64; self.reject()
    def test_wrong_rule_binding_rejected(self):
        self.review["labeling_rule_sha256"] = "0"*64; self.reject()
    def test_duplicate_pair_rejected(self):
        self.review["semantic_pairs"][-1] = copy.deepcopy(self.review["semantic_pairs"][0]); self.reject()
    def test_missing_pair_rejected(self):
        self.review["semantic_pairs"].pop(); self.reject()
    def test_stale_problem_identity_rejected(self):
        self.review["semantic_pairs"][0]["problem_sha256"] = "0"*64; self.reject()
    def test_cross_split_variant_rejected(self):
        self.review["semantic_pairs"][-1].update(verdict="SAME_CORE_TRAIN_VARIANT", core_family_id="F1")
        self.reject()
    def test_wrong_family_variant_rejected(self):
        self.review["semantic_pairs"][1].update(verdict="SAME_CORE_TRAIN_VARIANT", core_family_id="F1")
        self.reject()
    def test_disguised_same_family_difference_rejected(self):
        self.review["semantic_pairs"][0]["verdict"] = "DIFFERENT_CORE_TASK"; self.reject()
    def test_variant_family_id_required(self):
        del self.review["semantic_pairs"][0]["core_family_id"]; self.reject()
    def test_variant_mapping_required(self):
        del self.review["semantic_pairs"][0]["equivalence_mapping"]; self.reject()
    def test_leakage_rejected(self):
        self.review["semantic_pairs"][-1]["verdict"] = "SAME_CORE_CROSS_SPLIT"; self.reject()
    def test_uncertain_rejected(self):
        self.review["semantic_pairs"][-1]["verdict"] = "UNCERTAIN"; self.reject()
    def test_missing_pair_reason_rejected(self):
        self.review["semantic_pairs"][0]["reason"] = ""; self.reject()
    def test_missing_visual_review_evidence_rejected(self):
        del self.review["visual"]["review_evidence"]; self.reject()
    def test_self_comparison_receipt_rejected(self):
        self.evidence["semantic_subjects"][0]["id"] = "candidate"; self.reject()
    def test_duplicate_receipt_subject_rejected(self):
        self.evidence["semantic_subjects"].append(copy.deepcopy(self.evidence["semantic_subjects"][0])); self.reject()

class PublisherTests(unittest.TestCase):
    def setUp(self):
        base = ROOT/"reviews/codex-supervision/2026-10-06-protocol-v3-mail-followup/test-tmp"
        base.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=base)
        self.root = Path(self.temp.name).resolve()
        assert self.root.is_relative_to(base.resolve())
        self.addCleanup(self.temp.cleanup)
        self.rows, self.policy, self.density, self.evidence, self.review = fixtures()
        (self.root/"data").mkdir()
        (self.root/"configs").mkdir()
        (self.root/"tools").mkdir()
        (self.root/"review.txt").write_bytes(PROOF)
        for rel in ("apply_linalg048_admission_v3.py", "linalg048_protocol_v3.py", "holdout_contract.py"):
            (self.root/"tools"/rel).write_text("synthetic validator source", encoding="utf-8")
        def write(path, value):
            path.write_text(json.dumps(value), encoding="utf-8")
            return path.read_bytes()
        self.write = write
        train = b"".join(json.dumps(r).encode()+b"\n" for r in self.rows.values())
        (self.root/"data/train.jsonl").write_bytes(train)
        self.manifest = {"entries": [{"split": "train", "path": "train.jsonl", "sha256": raw_sha(train), "size": len(train)}]}
        mb = write(self.root/"data/manifest.json", self.manifest)
        pb = write(self.root/"configs/training_diversity_policy.json", self.policy)
        self.density.update(manifest_sha256=raw_sha(mb), policy_sha256=raw_sha(pb))
        db = write(self.root/"density.json", self.density)
        eb = write(self.root/"render.json", self.evidence)
        self.review.update(density_raw_sha256=raw_sha(db), render_evidence_raw_sha256=raw_sha(eb))
        write(self.root/"acceptance.json", self.review)
        self.out = self.root/"proposal.json"
        self.before = {p: p.read_bytes() for p in (self.root/"data").iterdir()}
        for name, value in (("ROOT", self.root), ("MANIFEST", self.root/"data/manifest.json"),
                            ("POLICY", self.root/"configs/training_diversity_policy.json")):
            patcher = patch.object(apply, name, value)
            patcher.start(); self.addCleanup(patcher.stop)
        def verifier(snapshot, render_path):
            self.assertEqual(snapshot.data, {}, "old exact-binding verifier must get a fresh snapshot")
            snapshot.read(render_path)
            return self.rows["candidate"], self.evidence
        self.mock = patch.object(apply.render, "verify_evidence", side_effect=verifier).start()
        self.addCleanup(patch.stopall)
    def publish(self):
        return apply.publish_proposal(self.out, self.root/"render.json", self.root/"acceptance.json", self.root/"density.json")
    def assert_inactive(self):
        self.assertEqual(self.before, {p:p.read_bytes() for p in (self.root/"data").iterdir()})
    def test_fresh_render_snapshot_and_separate_bindings(self):
        r = self.publish()
        self.assertEqual(r["original_render_source_bindings"], self.evidence["source_bindings"])
        self.assertIn("tools/linalg048_protocol_v3.py", r["current_admission_source_bindings"])
        for key in ("training_admitted", "active_data_modified", "global_leakage_free_certified",
                    "calibration_eligible", "formal_training_readiness_certified"):
            self.assertIs(r[key], False)
        self.assert_inactive()
    def test_existing_output_rejected_before_render(self):
        self.out.write_text("keep", encoding="utf-8")
        with self.assertRaises(ValueError): self.publish()
        self.mock.assert_not_called()
        self.assertEqual(self.out.read_text(), "keep")
    def test_external_output_rejected(self):
        self.out = self.root.parent.parent/"outside.json"
        with self.assertRaises(ValueError): self.publish()
        self.mock.assert_not_called()
    def test_workflow_rejected_before_render(self):
        self.review["schema"] = "linalg048-review-workflow-v2"
        self.write(self.root/"acceptance.json", self.review)
        with self.assertRaises(ValueError): self.publish()
        self.mock.assert_not_called(); self.assertFalse(self.out.exists()); self.assert_inactive()
    def test_stale_evidence_reference_rejected(self):
        (self.root/"review.txt").write_bytes(b"changed")
        with self.assertRaises(ValueError): self.publish()
        self.assertFalse(self.out.exists()); self.assert_inactive()
    def test_external_reference_rejected(self):
        with self.assertRaises(ValueError):
            apply.bind_references(Snapshot(self.root), [(str(ROOT/"README.md"), "0"*64)])
    def test_manual_density_hash_mismatch_rejected(self):
        self.review["density_raw_sha256"] = "0"*64
        self.write(self.root/"acceptance.json", self.review)
        with self.assertRaises(ValueError): self.publish()
        self.assertFalse(self.out.exists()); self.assert_inactive()
    def test_active_source_drift_rejected(self):
        (self.root/"data/train.jsonl").write_bytes(b"changed")
        with self.assertRaises(ValueError): self.publish()
        self.mock.assert_not_called(); self.assertFalse(self.out.exists())
    def test_active_candidate_math_mismatch_rejected(self):
        candidate = copy.deepcopy(self.rows["candidate"]); candidate["answer"] = "2/3"
        self.mock.side_effect = lambda snapshot, path: (candidate, self.evidence)
        with self.assertRaises(ValueError): self.publish()
        self.assertFalse(self.out.exists()); self.assert_inactive()
    def test_write_failure_cannot_select_active_data(self):
        with patch.object(apply, "write_new_json", side_effect=OSError("synthetic I/O failure")):
            with self.assertRaises(OSError): self.publish()
        self.assertFalse(self.out.exists()); self.assert_inactive()

if __name__ == "__main__":
    unittest.main()
