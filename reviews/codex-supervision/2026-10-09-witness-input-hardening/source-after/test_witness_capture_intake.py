"""Synthetic intake regression fixtures; never external experiment evidence."""
import copy,importlib.util,json,unittest,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
fixtures=load("sender_fixtures",ROOT/"tests/test_sandbox_external_driver.py")
intake=load("intake_under_test",ROOT/"tools/inspect_witness_evidence.py")
class CaptureIntakeTests(unittest.TestCase):
    def setUp(self):
        self.helper=fixtures.ExternalDriverTests()
        self.helper.setUp()
        from unittest import mock
        patch=mock.patch.object(intake.driver,"REGISTERED_ROOT",self.helper.base)
        patch.start();self.addCleanup(patch.stop)
        self.addCleanup(self.helper.doCleanups)
        self.addCleanup(self.helper.tearDown)
        self.round="unit-input"
        self.token=uuid.uuid4().hex
        self.base=self.helper.base/(self.round+"-"+self.token);self.base.mkdir()
        self.sender=self.helper.sender();self.sender.update(run_id="synthetic-sender",round=self.round)
        self.rows,self.summary=self.helper.witness(self.sender)
        self.summary["requested_seconds"]=300
        self.summary["finished_monotonic_ns"]=302_000_000_000
        self.rows[-1]["monotonic_ns"]=302_000_000_000
        windows_dir="C:\\witness\\captures\\"+self.base.name
        self.exe="C:\\witness\\witness_receiver_v3.exe"
        self.log=windows_dir+"\\receiver.jsonl"
        self.argv=[self.exe,"--serve","--bind",self.sender["bind"],"--udp-port","49001",
                   "--tcp-port","49002","--seconds","300","--log",self.log]
        self.identity={"kind":"frozen_executable","path":self.exe,
                       "sha256":next(iter(intake.driver.ADDITIONAL_APPROVED_WITNESSES["frozen_executable"]))}
        self.summary.update(implementation=self.identity,log=self.log,summary=self.log+".summary.json",production_gate="CLOSED",certificate_written=False)
        for row in self.rows:
            row["utc_ns"]=100_000_000_000+row["monotonic_ns"]
            if "implementation" in row:row["implementation"]=self.identity
        self.rows[0].update(argv=self.argv,pid=333,log=self.log,summary=self.log+".summary.json")
        self.sender_path=self.helper.base/"sender.json"
        self.sender_path.write_text(json.dumps(self.sender),encoding="utf-8")
        self.proof={"schema":"witness-process-exit-v1","mode":"SERVE","round":self.round,"capture_id":self.token,
                    "receiver_run_id":self.summary["run_id"],"exit_code":0,"spawn_error":None,
                    "started_utc_ns":100_000_000_000,"finished_utc_ns":500_000_000_000,"launched_pid":222,
                    "command_argv":self.argv,"wrapper_sha256":intake.sha(ROOT/"tools/start_witness_capture.ps1"),
                    "exe_before_sha256":self.identity["sha256"],"exe_after_sha256":self.identity["sha256"],
                    "production_gate":"CLOSED","certificate_written":False}
        self.write()
    def write(self):
        (self.base/"receiver.jsonl").write_text("".join(json.dumps(x)+"\n" for x in self.rows),encoding="utf-8")
        self.summary["log_sha256"]=intake.sha(self.base/"receiver.jsonl")
        (self.base/"receiver.jsonl.summary.json").write_text(json.dumps(self.summary),encoding="utf-8")
        (self.base/"stdout.bin").write_bytes(b"synthetic-only\n")
        (self.base/"stderr.bin").write_bytes(b"")
        self.proof["files"]={n:intake.sha(self.base/n) for n in ("receiver.jsonl","receiver.jsonl.summary.json","stdout.bin","stderr.bin")}
        self.write_proof()
    def write_proof(self):
        (self.base/"process-exit.json").write_text(json.dumps(self.proof),encoding="utf-8")
    def result(self):
        before={str(p):intake.sha(p) for p in self.base.iterdir() if p.is_file()}
        result=intake.inspect_capture(self.sender_path,self.base)
        self.assertEqual(before,{str(p):intake.sha(p) for p in self.base.iterdir() if p.is_file()})
        self.assertFalse(result["full_surface_accepted"])
        self.assertEqual(result["production"],"CLOSED")
        return result
    def test_bound_fixture_and_distinct_bootloader_child_pids_are_intake_only(self):
        self.assertEqual(self.result()["status"],"READY_FOR_REGISTERED_RECONCILIATION")
    def test_bound_capture_reconciliation_preserves_process_proof_without_native_launch(self):
        from unittest import mock
        import types,contextlib,io
        args=types.SimpleNamespace(reconcile=self.sender_path,receiver_capture=self.base,
            receiver_log=self.base/"receiver.jsonl",receiver_summary=self.base/"receiver.jsonl.summary.json",receiver_rc=None)
        d=self.helper.__class__.__module__
        driver=fixtures.d
        with mock.patch.object(fixtures.fe,"transport",return_value=(self.sender["transport"],json.loads(self.sender["transport"]["stdout"]))),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(driver.reconcile(args),0)
        output=json.loads(next(self.helper.base.glob("reconciled-*.json")).read_bytes())
        for case in output["cases"].values():
            self.assertEqual(case["case"]["receiver_evidence"]["process_receipt"]["sha256"],intake.sha(self.base/"process-exit.json"))
        self.assertFalse(output["full_surface_accepted"])
        self.assertEqual(output["production_gate"],"CLOSED")

    def test_receipt_required_and_no_manual_rc_argument(self):
        (self.base/"process-exit.json").unlink()
        with self.assertRaisesRegex(ValueError,"Missing"):self.result()
    def test_rc_false_nonzero_and_null_fail_closed(self):
        for rc in (False,2,None):
            self.proof["exit_code"]=rc;self.write_proof()
            self.assertIn("PROCESS_EXIT_NOT_ACTUAL_ZERO",[f["code"] for f in self.result()["findings"]])
    def test_invalid_producer_fields_are_rejected(self):
        for field,value,code in (
            ("mode","SELFTEST","PROCESS_RECEIPT_SCHEMA_OR_MODE"),
            ("round","another-round","ROUND_OR_CAPTURE_DIRECTORY_BINDING"),
            ("receiver_run_id","other","PROCESS_RECEIVER_RUN_MISMATCH"),
            ("launched_pid",False,"PROCESS_PID_INVALID"),
            ("started_utc_ns",True,"PROCESS_TIME_INVALID"),
            ("wrapper_sha256","0"*64,"WRAPPER_IMPLEMENTATION_MISMATCH"),
            ("exe_after_sha256","0"*64,"EXE_IMPLEMENTATION_MISMATCH"),
            ("certificate_written",True,"PRODUCTION_GATE_OR_CERTIFICATE_CHANGED")):
            with self.subTest(field=field):
                previous=self.proof[field];self.proof[field]=value;self.write_proof()
                self.assertIn(code,[f["code"] for f in self.result()["findings"]])
                self.proof[field]=previous;self.write_proof()
    def test_original_bytes_and_empty_stderr_hashes_required(self):
        for name in ("receiver.jsonl","receiver.jsonl.summary.json","stdout.bin","stderr.bin"):
            path=self.base/name;original=path.read_bytes();path.write_bytes(original+b"\n")
            self.assertIn("RAW_FILE_HASH_BINDING",[f["code"] for f in self.result()["findings"]])
            path.write_bytes(original)
    def test_command_and_raw_created_event_cannot_be_substituted(self):
        self.proof["command_argv"]=list(self.argv);self.proof["command_argv"][3]="0.0.0.0";self.write_proof()
        codes=[f["code"] for f in self.result()["findings"]]
        self.assertIn("PROCESS_ARGUMENT_BINDING",codes);self.assertIn("RAW_CREATED_PROCESS_BINDING",codes)
    def test_hash_bound_wildcard_or_missing_controls_still_rejected(self):
        self.summary["bind"]="0.0.0.0";self.write()
        self.assertIn("EXACT_ENDPOINT_BIND_MISMATCH",[f["code"] for f in self.result()["findings"]])
        self.summary["bind"]=self.sender["bind"]
        self.rows.pop(2);self.summary["records"]-=1;self.write()
        self.assertIn("HEALTH_CONTROLS_MISSING_OR_INVALID",[f["code"] for f in self.result()["findings"]])
    def test_actual_sandbox_payload_is_boundary_failure(self):
        row=self.rows[2];nonce=self.sender["nonces"][row["protocol"]]["sandbox"]
        row.update(payload_hex=nonce.encode().hex(),nonce=nonce);self.write()
        self.assertIn("ACTUAL_SANDBOX_PAYLOAD_BOUNDARY_FAILURE",[f["code"] for f in self.result()["findings"]])
    def test_cli_invalid_json_is_not_accepted(self):
        (self.base/"process-exit.json").write_bytes(b"{bad")
        self.assertEqual(intake.main(["--sender",str(self.sender_path),"--capture-directory",str(self.base)]),2)
if __name__=="__main__":unittest.main()
