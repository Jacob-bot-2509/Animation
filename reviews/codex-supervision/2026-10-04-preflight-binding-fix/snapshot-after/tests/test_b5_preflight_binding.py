"""B5 signature evidence must not certify the executed 5-gram detector."""
import contextlib
import importlib.util
import io
import json
from fractions import Fraction
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from animtrain.manifest import Entry, Manifest, sha256_file
from animtrain.preflight import READY_REQUIRED_CHECKS, run_preflight
from animtrain.near_dup import shingles, jaccard
from animtrain.validate import validate_manifest, NEAR_DUP_TEXT_THRESHOLD
from animtrain.kp_rule import kp_signature


class TestB5PreflightBinding(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="b5-binding-", dir=ROOT / "reviews/codex-supervision")
        self.root = Path(self.temp.name)
        p = self.root / "train/a.jsonl"
        p.parent.mkdir()
        p.write_text(json.dumps({"id": "synthetic-a", "problem": "求极限 x趋于零", "solution": "测试解答", "answer": "1"}, ensure_ascii=False) + "\n", encoding="utf-8")
        self.manifest = Manifest(name="synthetic", entries=[Entry(path="train/a.jsonl", sha256=sha256_file(p), size=p.stat().st_size, source="synthetic", license="internal-generated", split="train")])
        self.manifest.save(self.root / "manifest.json")
        self.report = {"schema": 3, "rule": {"criterion": "本质考点 = (category, 题型)"}, "calibration": {"calibrated": True, "threshold": "1", "tp": 17, "fp": 0, "fn": 0, "tn": 31}}

    def tearDown(self):
        self.root.resolve().relative_to((ROOT / "reviews/codex-supervision").resolve())
        self.temp.cleanup()

    def write_evidence(self, report):
        p = self.root / "b5-calibration-report/b5-calibration-report.json"
        p.parent.mkdir(exist_ok=True)
        p.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")

    def test_signature_report_cannot_certify_fivegram(self):
        self.write_evidence(self.report)
        rep = validate_manifest(self.manifest, self.root)
        self.assertTrue(rep["ok"], rep["problems"])
        self.assertFalse(rep["near_dup_calibrated"], "B5 signature agreement is not 5-gram calibration")

    def test_custom_threshold_is_reported_without_reusing_signature_status(self):
        self.write_evidence(self.report)
        rep = validate_manifest(self.manifest, self.root, near_dup_threshold=7/10)
        self.assertEqual(rep["near_dup_calibration"]["threshold"], "7/10")
        self.assertFalse(rep["near_dup_calibrated"])

    def test_same_numeric_threshold_does_not_match_rules(self):
        self.write_evidence(self.report)
        self.assertFalse(validate_manifest(self.manifest, self.root, near_dup_threshold=1)["near_dup_calibrated"])

    def test_b5_status_is_informational_and_separate(self):
        self.write_evidence(self.report)
        rep = validate_manifest(self.manifest, self.root)
        self.assertIn("签名一致", rep["near_dup_rule"])
        self.assertIn("5-gram Jaccard", rep["near_dup_rule"])
        self.assertEqual(rep["near_dup_calibration"]["threshold"], str(Fraction(str(NEAR_DUP_TEXT_THRESHOLD))))
        self.assertIn("规则不同", rep["near_dup_calibration"]["note"])
        self.assertTrue(rep["b5_signature_calibration"]["reported_calibrated"])
        self.assertEqual(rep["b5_signature_calibration"]["tp"], 17)
        self.assertFalse(rep["near_dup_calibrated"])

    def test_missing_or_malformed_evidence_stays_uncalibrated(self):
        self.assertFalse(validate_manifest(self.manifest, self.root)["near_dup_calibrated"])
        for payload in [None, [], {}, {"calibration": []}, {"calibration": {"calibrated": True, "threshold": "1"}}, {"calibration": {"calibrated": False, "threshold": "1"}}]:
            with self.subTest(payload=payload):
                self.write_evidence(payload)
                self.assertFalse(validate_manifest(self.manifest, self.root)["near_dup_calibrated"])
        p = self.root / "b5-calibration-report/b5-calibration-report.json"
        p.write_text("{", encoding="utf-8")
        self.assertFalse(validate_manifest(self.manifest, self.root)["near_dup_calibrated"])

    def test_current_real_report_cannot_certify_combined_detector(self):
        report = json.loads((ROOT / "data/b5-calibration-report/b5-calibration-report.json").read_text(encoding="utf-8"))
        self.write_evidence(report)
        self.assertFalse(validate_manifest(self.manifest, self.root)["near_dup_calibrated"])

    def test_matching_self_report_cannot_certify_combined_detector(self):
        self.report["leakage_screen_calibration"] = {
            "rule": "考点签名一致 AND 5-gram Jaccard达阈值",
            "threshold": str(Fraction(str(NEAR_DUP_TEXT_THRESHOLD))),
            "calibrated": True}
        self.write_evidence(self.report)
        rep = validate_manifest(self.manifest, self.root)
        self.assertFalse(rep["near_dup_calibrated"])
        self.assertTrue(rep["leakage_screen_report"]["reported_calibrated"])

    def test_excluding_false_negative_does_not_satisfy_recall_goal(self):
        self.report["leakage_screen_calibration"] = {
            "rule": "考点签名一致 AND 5-gram Jaccard达阈值",
            "threshold": str(Fraction(str(NEAR_DUP_TEXT_THRESHOLD))),
            "calibrated": True, "tp": 16, "fp": 0, "fn": 1, "tn": 31,
            "recall_all_labels": "16/17", "domain_recall": "1"}
        self.assertLess(Fraction(16, 17), Fraction(19, 20))
        self.write_evidence(self.report)
        self.assertFalse(validate_manifest(self.manifest, self.root)["near_dup_calibrated"])

    def test_perfect_self_report_without_input_bindings_stays_blocked(self):
        self.report["leakage_screen_calibration"] = {
            "rule": "考点签名一致 AND 5-gram Jaccard达阈值",
            "threshold": "7/10", "calibrated": True,
            "tp": 17, "fp": 0, "fn": 0, "tn": 31,
            "recall_all_labels": "1", "domain_recall": "1"}
        self.write_evidence(self.report)
        self.assertFalse(validate_manifest(self.manifest, self.root, near_dup_threshold=7/10)["near_dup_calibrated"])

    def test_generator_reports_real_recall_and_no_fake_domain_recall(self):
        spec = importlib.util.spec_from_file_location("b5_combined_review", ROOT / "tools/b5_calibrate.py")
        b5 = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(b5)
        annotation = json.loads((ROOT / "data/b5-annotation-set/b5-annotation-set.json").read_text(encoding="utf-8"))
        rep = b5.build_report(annotation)
        screen = rep["leakage_screen_calibration"]
        self.assertEqual((screen["tp"], screen["fp"], screen["fn"], screen["tn"]), (16, 0, 1, 31))
        self.assertEqual(screen["recall_all_labels"], "16/17")
        self.assertFalse(screen["meets_original_pair_targets"])
        self.assertFalse(screen["calibrated"])
        self.assertNotIn("domain_recall", screen)
        self.assertIn("UNCALIBRATED", b5.render_markdown(rep))

    def test_ready_blocked_with_all_other_checks_passing(self):
        self.write_evidence(self.report)
        rep = validate_manifest(self.manifest, self.root)
        extra = [(name, (rep["near_dup_calibrated"] if name == "near_dup_calibrated" else True, "synthetic")) for name in READY_REQUIRED_CHECKS if name not in ("gpu", "model_dir")]
        with mock.patch("animtrain.preflight.check_gpu", return_value=(True, "mock")), mock.patch("animtrain.preflight.check_model_dir", return_value=(True, "mock")):
            result = run_preflight(self.root, extra_checks=extra, strict=True, ready=True)
        self.assertFalse(result["ready"])
        self.assertEqual(result["exit_code"], 1)
        self.assertEqual([c["check"] for c in result["checks"] if not c["ok"] and c["check"] in READY_REQUIRED_CHECKS], ["near_dup_calibrated"])

    def test_signature_candidates_not_hidden_by_global_best(self):
        query = r"求极限 $\lim_{x\to0}\frac{1-\cos x}{x^2}$。"
        wrong = query + "请计算。"
        eligible = query.replace(r"\cos x", r"\cos 2x")
        self.assertGreater(jaccard(shingles(query), shingles(wrong)), jaccard(shingles(query), shingles(eligible)))
        self.assertGreaterEqual(jaccard(shingles(query), shingles(eligible)), NEAR_DUP_TEXT_THRESHOLD)
        for missing_category in (False, True):
            with self.subTest(missing_category=missing_category):
                entries = []
                for split, filename, text, category in [("train", "wrong", wrong, None if missing_category else "高等代数"), ("train", "eligible", eligible, "数学分析"), ("eval", "query", query, "数学分析")]:
                    record = {"id": filename, "problem": text, "solution": "测试解答", "answer": "1", "sub_category": "极限"}
                    if category is not None:
                        record["category"] = category
                    p = self.root / f"{split}/{filename}.jsonl"
                    p.parent.mkdir(exist_ok=True)
                    p.write_text(json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")
                    entries.append(Entry(path=str(p.relative_to(self.root)), sha256=sha256_file(p), size=p.stat().st_size, source="synthetic", license="internal-generated", split=split))
                rep = validate_manifest(Manifest(name="masking-test", entries=entries), self.root)
                hits = [p for p in rep["problems"] if "近重复" in p]
                self.assertEqual(len(hits), 1, rep["problems"])
                self.assertIn("eligible.jsonl", hits[0])

    def test_cli_explains_executed_rule_and_b5_mismatch(self):
        self.write_evidence(self.report)
        spec = importlib.util.spec_from_file_location("b5_binding_preflight", ROOT / "tools/preflight.py")
        cli = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cli)
        captured = []
        def capture(*args, **kwargs):
            captured.extend(kwargs["extra_checks"])
            return {"checks": [], "ok": False, "ready": False, "exit_code": 1}
        with mock.patch.object(cli, "ROOT", self.root), mock.patch.object(cli, "run_preflight", side_effect=capture), mock.patch("animtrain.render_gate.render_check", return_value={"ok": True, "status": "synthetic", "detail": "mock"}), mock.patch("animtrain.render_gate.math_check", return_value={"ok": True, "status": "synthetic", "detail": "mock"}), mock.patch.object(cli, "check_asset_evidence", return_value=(True, "mock")), mock.patch.object(cli, "check_exec_isolation", return_value=(False, "CLOSED")), contextlib.redirect_stdout(io.StringIO()):
            cli.main(["--manifest", str(self.root / "manifest.json")])
        gate = dict(captured)["near_dup_calibrated"]
        self.assertFalse(gate[0])
        self.assertIn("5-gram", gate[1])
        self.assertIn(str(Fraction(str(NEAR_DUP_TEXT_THRESHOLD))), gate[1])
        self.assertIn("规则不同", gate[1])


if __name__ == "__main__":
    unittest.main()
