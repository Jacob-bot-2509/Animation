"""Synthetic rejection tests; no labels are applied to real questions."""
import copy
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "src")]
import finalize_linalg048_review as final
import split_review_packet as chunks
from holdout_contract import RULE_SHA, raw_sha, object_sha, json_object


class WorkflowGuardTests(unittest.TestCase):
    def inputs(self):
        packet = {"schema": "linalg048-semantic-review-packet-v1",
                  "labeling_rule_sha256": RULE_SHA, "reviewer": None,
                  "accepted": False, "training_admitted": False,
                  "candidate": {"id": "synthetic-candidate", "problem": "T(x,y)=(x+3y,y)"},
                  "semantic_pairs": [], "review_material": []}
        subjects = [("train", "synthetic-a"), ("train", "synthetic-b"),
                    ("eval", "synthetic-c"), ("test", "synthetic-d")]
        for split, pid in subjects:
            problem = "Synthetic exact problem " + pid
            record = {"id": pid, "problem": problem, "solution": "1/3",
                      "answer": "1/3", "scene_spec": {"objects": [], "steps": []}}
            subject = {"split": split, "id": pid,
                       "problem_sha256": raw_sha(problem.encode())}
            packet["semantic_pairs"].append({**subject, "verdict": None, "reason": ""})
            packet["review_material"].append({**subject, "source_records": [record],
                                             "source_record_sha256": [object_sha(record)]})
        verdicts = ["DIFFERENT_CORE_TASK", "SAME_CORE_TRAIN_VARIANT",
                    "DIFFERENT_CORE_TASK", "UNCERTAIN"]
        rows = [{**s, "verdict": v, "reason": "Explicit synthetic comparison",
                 "evidence": "Synthetic source 1/3"}
                for s, v in zip(packet["semantic_pairs"], verdicts)]
        workflow = {"result": {"pairs": rows,
                    "counts": dict(zip(final.VALID, [2, 1, 0, 1])),
                    "trainVariants": ["train|synthetic-b"], "leakage": [],
                    "uncertain": ["test|synthetic-d"]}}
        return packet, workflow

    def validate(self, packet, wf):
        return final.validate_result(packet, wf, expected_size=4)

    def test_honest_train_variant_and_uncertain_are_retained(self):
        p, w = self.inputs()
        rows, counts, lists = self.validate(p, w)
        self.assertEqual(rows[1]["verdict"], "SAME_CORE_TRAIN_VARIANT")
        self.assertEqual(rows[3]["verdict"], "UNCERTAIN")
        self.assertEqual(counts["UNCERTAIN"], 1)
        self.assertEqual(lists["uncertain"], ["test|synthetic-d"])

    def test_duplicate_reviewer_subject_rejected(self):
        p, w = self.inputs(); w["result"]["pairs"].append(copy.deepcopy(w["result"]["pairs"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate"): self.validate(p, w)

    def test_extra_reviewer_subject_rejected(self):
        p, w = self.inputs(); w["result"]["pairs"].append(dict(w["result"]["pairs"][0], id="unreviewed-extra"))
        with self.assertRaisesRegex(ValueError, "extra"): self.validate(p, w)

    def test_missing_subject_rejected(self):
        p, w = self.inputs(); w["result"]["pairs"].pop()
        with self.assertRaisesRegex(ValueError, "missing"): self.validate(p, w)

    def test_fabricated_counts_rejected(self):
        p, w = self.inputs(); w["result"]["counts"]["DIFFERENT_CORE_TASK"] = 4
        with self.assertRaisesRegex(ValueError, "counts"): self.validate(p, w)

    def test_boolean_count_rejected(self):
        p, w = self.inputs(); w["result"]["counts"]["UNCERTAIN"] = True
        with self.assertRaisesRegex(ValueError, "counts"): self.validate(p, w)

    def test_omitted_zero_count_rejected(self):
        p, w = self.inputs(); del w["result"]["counts"]["SAME_CORE_CROSS_SPLIT"]
        with self.assertRaisesRegex(ValueError, "counts"): self.validate(p, w)

    def test_wrong_summary_list_rejected(self):
        p, w = self.inputs(); w["result"]["trainVariants"] = []
        with self.assertRaisesRegex(ValueError, "classification list"): self.validate(p, w)

    def test_duplicate_summary_id_rejected(self):
        p, w = self.inputs(); w["result"]["uncertain"] *= 2
        with self.assertRaisesRegex(ValueError, "classification list"): self.validate(p, w)

    def test_heldout_cannot_be_train_variant(self):
        p, w = self.inputs(); w["result"]["pairs"][2]["verdict"] = "SAME_CORE_TRAIN_VARIANT"
        with self.assertRaisesRegex(ValueError, "held-out"): self.validate(p, w)

    def test_train_cannot_be_cross_split_pair(self):
        p, w = self.inputs(); w["result"]["pairs"][0]["verdict"] = "SAME_CORE_CROSS_SPLIT"
        with self.assertRaisesRegex(ValueError, "training subject"): self.validate(p, w)

    def test_heldout_cross_split_label_is_retained_without_acceptance(self):
        p, w = self.inputs(); w["result"]["pairs"][2]["verdict"] = "SAME_CORE_CROSS_SPLIT"
        w["result"]["counts"] = dict(zip(final.VALID, [1, 1, 1, 1]))
        w["result"]["leakage"] = ["eval|synthetic-c"]
        rows, counts, lists = self.validate(p, w)
        self.assertEqual(counts["SAME_CORE_CROSS_SPLIT"], 1)
        self.assertEqual(lists["leakage"], ["eval|synthetic-c"])

    def test_blank_reason_or_evidence_rejected(self):
        for field in ("reason", "evidence"):
            with self.subTest(field=field):
                p, w = self.inputs(); w["result"]["pairs"][0][field] = " "
                with self.assertRaises(ValueError): self.validate(p, w)

    def test_wrong_workflow_problem_hash_rejected(self):
        p, w = self.inputs(); w["result"]["pairs"][0]["problem_sha256"] = "f" * 64
        with self.assertRaisesRegex(ValueError, "problem hash"): self.validate(p, w)

    def test_changed_solution_or_scene_hash_rejected(self):
        for field in ("solution", "scene_spec"):
            with self.subTest(field=field):
                p, _ = self.inputs(); p["review_material"][0]["source_records"][0][field] = "changed"
                with self.assertRaisesRegex(ValueError, "binding"):
                    final.validate_packet(p, expected_size=4)

    def test_duplicate_packet_subject_rejected(self):
        p, _ = self.inputs(); p["semantic_pairs"][1] = copy.deepcopy(p["semantic_pairs"][0])
        with self.assertRaisesRegex(ValueError, "duplicate"): final.validate_packet(p, 4)

    def test_chunk_material_is_joined_by_identity(self):
        p, _ = self.inputs(); p["review_material"].reverse()
        result = chunks.make_chunks(p, chunk_size=3, expected_size=4)
        self.assertEqual([len(c["pairs"]) for c in result], [3, 1])
        for chunk in result:
            for pair, material in zip(chunk["pairs"], chunk["material"]):
                self.assertEqual(final.subject_key(pair), final.subject_key(material))

    def test_chunk_invalid_size_rejected(self):
        for size in (0, -1, True):
            with self.subTest(size=size):
                with self.assertRaises(ValueError): chunks.make_chunks(self.inputs()[0], size, 4)

    def test_changed_pinned_packet_rejected(self):
        with patch.object(final.Snapshot, "read", return_value=b"{}"):
            with self.assertRaisesRegex(ValueError, "raw hash"): final.read_bound_packet(final.Snapshot(ROOT))

    def test_stale_source_binding_rejected(self):
        p, _ = self.inputs()
        p["source_bindings"] = {"synthetic.txt": {"raw_sha256": "f"*64, "bytes": 3}}
        raw = json.dumps(p).encode()
        with patch.object(final, "PACKET_SHA", raw_sha(raw)), patch.object(final, "validate_packet"), patch.object(final.Snapshot, "read", side_effect=[raw, b"old"]):
            with self.assertRaisesRegex(ValueError, "stale"): final.read_bound_packet(final.Snapshot(ROOT))

    def test_existing_or_external_output_rejected_before_reads(self):
        for target in (Path(__file__), ROOT.parent/"outside-project.json"):
            with self.subTest(target=target), patch.object(final, "read_bound_packet") as read:
                with self.assertRaisesRegex(ValueError, "fresh project"):
                    final.publish_review(ROOT/"missing.json", target)
                read.assert_not_called()

    def test_existing_chunk_directory_rejected_before_reads(self):
        with patch.object(chunks, "read_bound_packet") as read:
            with self.assertRaisesRegex(ValueError, "fresh project"):
                chunks.publish_chunks(ROOT/"tests")
            read.assert_not_called()

    def test_duplicate_json_keys_rejected(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            json_object(b'{"result":1,"result":2}')

    def test_no_args_cannot_publish_default_historical_path(self):
        for main in (final.main, chunks.main):
            with self.subTest(main=main.__module__), self.assertRaises(SystemExit) as caught:
                main([])
            self.assertEqual(caught.exception.code, 2)



    def test_workflow_outside_project_is_rejected(self):
        p, _ = self.inputs()
        with patch.object(final, "read_bound_packet", return_value=p):
            with self.assertRaisesRegex(ValueError, "source outside project"):
                final.publish_review(ROOT.parent/"unarchived.json",
                                     ROOT/"reviews/codex-supervision/2026-10-06-workflow-mail-review/not-published.json")

    def test_complete_coverage_still_cannot_be_manual_acceptance(self):
        p, w = self.inputs(); rows, counts, lists = self.validate(p, w)
        with patch.object(final, "read_bound_packet", return_value=p), patch.object(final, "Snapshot") as snapshot, patch.object(final, "validate_result", return_value=(rows, counts, lists)), patch.object(final, "write_new_json") as write:
            snapshot.return_value.read.return_value = json.dumps(w).encode()
            snapshot.return_value.bindings.return_value = {}
            artifact = final.publish_review(ROOT/"synthetic-result.json",
                ROOT/"reviews/codex-supervision/2026-10-06-workflow-mail-review/synthetic-not-written.json")
        self.assertFalse(artifact["accepted"])
        self.assertFalse(artifact["training_admitted"])
        self.assertFalse(artifact["global_leakage_free_certified"])
        import apply_linalg048_admission as apply
        with self.assertRaisesRegex(ValueError, "manual acceptance"):
            apply.require_manual_review(artifact, {}, "a"*64)
        write.assert_called_once()

if __name__ == "__main__":
    unittest.main()
