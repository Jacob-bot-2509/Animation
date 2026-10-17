"""Independent adversarial checks for fixed-fixture diagnostics."""
import copy, hashlib, json, os, sys, types, unittest, uuid
from pathlib import Path
from unittest.mock import patch
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import eval_protocol as p
import run_fixtures as f
import fixture_executor as child

class ProtocolTests(unittest.TestCase):
    def setUp(self):
        f.RUNS = p.FIXTURE_ROOT / ("regression-" + uuid.uuid4().hex)
        self.cfg, self.work = f.build_cfg("01-valid-all", f.make_questions())
        self.req = p.build_request(self.cfg)
        self.specs = {p._identity({k: x[k] for k in p.IDENTITY_KEYS}): [x["spec"]]
                      for x in json.loads((self.work/"generated-specs.json").read_text(encoding="utf-8"))}

    def rows(self):
        child.emit(self.req, self.work, {})
        return [json.loads(x) for x in (self.work/"response-index.jsonl").read_text(encoding="utf-8").splitlines()]

    def metrics(self, rows, timed_out=False):
        return p.aggregate(self.req, p.verify_response(self.req, self.work, rows, 0, timed_out), self.specs)

    def test_mock_success_never_becomes_actual_metric(self):
        report = self.metrics(self.rows())
        for name in p.METRICS:
            self.assertEqual(report[name]["status"], "UNVERIFIED")
            self.assertIsNone(report[name]["rate"])
            self.assertEqual(report["fixture_diagnostics"][name]["status"], "FIXTURE_CHECKED")

    def test_missing_render_and_execution_remain_unknown(self):
        rows = self.rows()
        for x in rows:
            x.pop("render"); x.pop("executable")
        d = self.metrics(rows)["fixture_diagnostics"]
        self.assertIsNone(d["render"]["rate"]); self.assertIsNone(d["executable"]["rate"])

    def test_input_record_forgery_rejected(self):
        rows = self.rows()
        for x in rows:
            x["input_bindings"]["input_record_sha256"] = "f"*64
        d = self.metrics(rows)["fixture_diagnostics"]
        self.assertIsNone(d["render"]["rate"]); self.assertEqual(d["render"]["unknown"], 6)

    def test_pass_claim_with_false_assertion_is_diagnostic_failure(self):
        rows = self.rows()
        rows[0]["math"]["assertions"][0]["verdict"] = False
        d = self.metrics(rows)["fixture_diagnostics"]
        self.assertEqual(d["math"]["rate"], "5/6")

    def test_pass_claim_with_missing_fidelity_list_is_unknown(self):
        rows = self.rows()
        for x in rows:
            x["fidelity"]["checklist"] = []
        self.assertIsNone(self.metrics(rows)["fixture_diagnostics"]["fidelity"]["rate"])

    def test_extra_identity_refuses_whole_response(self):
        rows = self.rows()
        ghost = copy.deepcopy(rows[0]); ghost["identity"]["problem_id"] = "ghost"
        rows.append(ghost)
        report = self.metrics(rows)
        self.assertEqual(report["status"], "REFUSED")
        self.assertIsNone(report["fixture_diagnostics"]["render"]["rate"])

    def test_timeout_cannot_reuse_existing_success_rows(self):
        report = self.metrics(self.rows(), timed_out=True)
        self.assertEqual(report["status"], "REFUSED")
        self.assertIsNone(report["fixture_diagnostics"]["render"]["rate"])

    def test_request_hash_is_not_executor_approval(self):
        path = self.work/"fixture_executor.py"; path.write_text("raise SystemExit(0)", encoding="utf-8")
        self.req["evaluator_sources"]["render_executor"]["sha256"] = p._sha(path)
        with patch.object(p.subprocess, "run") as launch:
            with self.assertRaises(ValueError):
                p.run_executor(self.req, self.work, "render_executor")
            launch.assert_not_called()

    def test_executor_absolute_or_escaped_path_refused_before_launch(self):
        self.req["evaluator_sources"]["render_executor"]["path"] = "../fixture_executor.py"
        with patch.object(p.subprocess, "run") as launch:
            with self.assertRaises(ValueError):
                p.run_executor(self.req, self.work, "render_executor")
            launch.assert_not_called()

    def test_scope_cannot_be_upgraded_by_request(self):
        self.req["scope"] = "production"
        with patch.object(p.subprocess, "run") as launch:
            with self.assertRaises(ValueError):
                p.run_executor(self.req, self.work, "render_executor")
            launch.assert_not_called()

    def test_duplicate_fixed_identity_rejected(self):
        self.req["fixed_questions"].append(copy.deepcopy(self.req["fixed_questions"][0]))
        self.assertFalse(p.verify_bindings(self.req, self.work)[0])

    def test_boolean_row_index_is_not_an_identity_integer(self):
        self.req["fixed_questions"][0]["identity"]["row_index"] = False
        self.assertFalse(p.verify_bindings(self.req, self.work)[0])

    def test_spec_file_hash_does_not_hide_per_sample_content_drift(self):
        path = self.work/"generated-specs.json"; rows = json.loads(path.read_text(encoding="utf-8"))
        rows[0]["spec"]["objects"] = ["substituted"]
        path.write_text(json.dumps(rows,ensure_ascii=False),encoding="utf-8")
        self.req["bindings"]["generated_specs_sha256"] = p._sha(path)
        self.assertEqual(p.verify_bindings(self.req, self.work), (False, "SPEC_CONTENT_DRIFT"))

    def test_generated_identity_coverage_required(self):
        path = self.work/"generated-specs.json"; rows = json.loads(path.read_text(encoding="utf-8")); rows.pop()
        path.write_text(json.dumps(rows),encoding="utf-8")
        self.req["bindings"]["generated_specs_sha256"] = p._sha(path)
        self.assertEqual(p.verify_bindings(self.req, self.work), (False, "GENERATED_IDENTITY_COVERAGE"))

    def test_stale_receipt_is_not_reused_or_overwritten(self):
        stale = self.work/"response-index.jsonl"; stale.write_bytes(b"stale")
        with patch.object(p.subprocess, "run") as launch:
            report = p.run_harness(self.cfg,self.work)
            self.assertEqual(report["status"],"REFUSED"); launch.assert_not_called()
        self.assertEqual(stale.read_bytes(),b"stale")

    def test_output_root_is_fixed_fixture_root(self):
        outside = HERE/("not-an-approved-work-"+uuid.uuid4().hex)
        report = p.run_harness(self.cfg,outside)
        self.assertEqual(report["reason"],"FIXTURE_WORK_ROOT_ONLY")
        self.assertFalse(outside.exists())

    def test_reparse_component_rejected_even_with_in_root_target(self):
        real = p.os.lstat
        target = self.work/"redirect"
        def fake(path):
            info = real(path)
            if Path(path)==target:
                return types.SimpleNamespace(st_mode=info.st_mode,st_file_attributes=1024)
            return info
        target.mkdir()
        with patch.object(p.os,"lstat",side_effect=fake):
            self.assertIsNone(p._safe_artifact(self.work,"redirect/a.png"))

    def test_unsupported_media_is_unknown_not_success(self):
        path = self.work/"not-a-real.mp4"; path.write_bytes(b"anything")
        self.assertEqual(p._decode_media(path),(None,"UNSUPPORTED_MEDIA"))

if __name__ == "__main__":
    unittest.main(verbosity=2)
