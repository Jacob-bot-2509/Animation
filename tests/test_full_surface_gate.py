"""Adversarial rejection tests for all-43 gate, source binding and fixed fixture hook."""
import json,sys,tempfile,unittest
from pathlib import Path
from unittest import mock
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"src"))
from animtrain import sandbox_execution as se,full_surface_evidence as fe
class SurfaceGateTests(unittest.TestCase):
    def test_exact_43_points(self):
        self.assertEqual(len(fe.POINTS),43);self.assertEqual(len(set(fe.POINTS)),43)
    def test_green_labels_without_evidence_do_not_pass(self):
        raw={"schema":"sandbox-surface-native-v1","initial_bindings":{n:se.digest(ROOT/n) for n in se.BOUND_FILES},"status":"GREEN","cases":{},"results":{p:{"status":"GREEN"} for p in fe.POINTS}}
        self.assertTrue(all(v["status"]=="GAP" for v in fe.recompute(raw).values()))
    def test_copied_denial_without_parent_source_and_controls_is_not_green(self):
        raw={"schema":"sandbox-surface-native-v1","initial_bindings":{n:se.digest(ROOT/n) for n in se.BOUND_FILES},"cases":{p:{"status":"GREEN","outcome":"os_denied","winerror":5} for p in fe.POINTS}}
        self.assertTrue(all(v["status"]!="GREEN" for v in fe.recompute(raw).values()))
    def test_unknown_schema_rejected(self):
        with self.assertRaises(ValueError):fe.recompute({"schema":"legacy","cases":{}})
    def test_review_path_cannot_escape(self):
        with self.assertRaises(ValueError):fe.bound_path(ROOT/"data/execution_evidence.json",fe.REVIEW_ROOT)
    def test_old_16_certificate_rejected_even_with_current_hashes(self):
        with tempfile.TemporaryDirectory(dir=fe.REVIEW_ROOT) as d:
            p=Path(d)/"old.json";p.write_text(json.dumps({"schema":"production-appcontainer-v1","fs_isolation":"private_per_run","implementation_sha256":{n:se.digest(ROOT/n) for n in se.BOUND_FILES}}),encoding="utf-8")
            self.assertFalse(se.check_certificate(p)[0])
    def test_16_passes_cannot_open_new_certificate_without_surface(self):
        with tempfile.TemporaryDirectory(dir=se.WORK_ROOT) as d:
            work=Path(d);bind={n:se.digest(ROOT/n) for n in se.BOUND_FILES}
            raw=work/"raw.json";raw.write_text(json.dumps({"implementation_sha256":bind}),encoding="utf-8")
            cert=work/"cert.json";cert.write_text(json.dumps({"schema":"production-appcontainer-v2","fs_isolation":"private_per_run","implementation_sha256":bind,"raw_path":str(raw),"raw_sha256":se.digest(raw)}),encoding="utf-8")
            with mock.patch("animtrain.isolation_evidence.judge",return_value={n:"PASS" for n in se.REQUIRED_CASES}):
                self.assertFalse(se.check_certificate(cert)[0])
    def test_fixture_hook_not_allowed_for_generated_render(self):
        hook=mock.Mock()
        with self.assertRaisesRegex(ValueError,"fixed probes"):se.run_code("print(1)",mode="render",prepare_probe=hook)
        hook.assert_not_called()
    def test_fixture_hook_must_be_callable(self):
        with self.assertRaises(ValueError):se.run_code("print(1)",mode="probe",prepare_probe="unsafe")
    def test_production_bootstrap_installs_actual_shim(self):
        from animtrain.net_guard import NETWORK_SHIM
        self.assertTrue(se.TEX_BOOTSTRAP.startswith(NETWORK_SHIM))
    def test_runtime_has_exact_dead_proxies_and_ignores_inherited_host_values(self):
        env=se.runtime_env(ROOT/"reviews/codex-supervision/fixture-only")
        for k in ("HTTP_PROXY","HTTPS_PROXY","ALL_PROXY","http_proxy","https_proxy","all_proxy"):self.assertEqual(env[k],"http://127.0.0.1:9")
        self.assertEqual(env["NO_PROXY"],"");self.assertEqual(env["no_proxy"],"")
    def test_bool_exit_is_not_native_exit(self):
        with self.assertRaisesRegex(ValueError,"integer"):
            fe.transport({"transport":{"rc":False}})
if __name__=="__main__":unittest.main()
