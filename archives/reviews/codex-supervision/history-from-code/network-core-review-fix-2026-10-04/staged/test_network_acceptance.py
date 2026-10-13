"""Failure injection at acceptance entry points, without altering OS policy."""
from __future__ import annotations
import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("network_acceptance_review",ROOT/"tools/network_acceptance.py")
tool=importlib.util.module_from_spec(spec)
spec.loader.exec_module(tool)


def attempts(verdict="PASS_LOCAL_LOOPBACK"):
    return [dict(transport=t,host=h,judgment=dict(verdict=verdict)) for t,h in tool.CASES]


class TestAcceptanceEntry(unittest.TestCase):
    def invoke(self, directory, baseline, execute=None):
        args=["--baseline-evidence",str(baseline),"--output",str(directory)]
        with contextlib.redirect_stdout(io.StringIO()):
            if execute is None: status=tool.main(args)
            else:
                with mock.patch.object(tool,"execute",side_effect=execute): status=tool.main(args)
        files=list(directory.glob("loopback-*.json"));self.assertEqual(len(files),1)
        return status,json.loads(files[0].read_text(encoding="utf-8"))
    def test_preflight_missing_or_invalid_baseline_writes_full_unknown_evidence(self):
        for mode in ("missing","json","schema"):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as temp:
                base=Path(temp)/"baseline.json";out=Path(temp)/"out"
                if mode=="json": base.write_text("{",encoding="utf-8")
                if mode=="schema": base.write_text("{}",encoding="utf-8")
                status,result=self.invoke(out,base)
                self.assertEqual(status,2);self.assertEqual(result["overall"],"UNVERIFIED")
                self.assertEqual(result["state"],"ERROR");self.assertEqual(result["attempts"],[])
                self.assertIn("error",result);self.assertIn("traceback",result)
                self.assertEqual(result["production_gate"],"CLOSED");self.assertEqual(result["external_network"],"UNVERIFIED")
                self.assertEqual(result["schema"],2);self.assertEqual(result["contract"],tool.net.LOCAL_LOOPBACK_CONTRACT)
    def test_unexpected_midrun_error_preserves_partial_attempts_and_unknown_exit(self):
        with tempfile.TemporaryDirectory() as temp:
            def fault(args,result,target):
                result["attempts"].extend(attempts()[:1]);raise TypeError("native API wiring")
            status,result=self.invoke(Path(temp)/"out",Path(temp)/"missing.json",fault)
            self.assertEqual(status,2);self.assertEqual(result["state"],"ERROR")
            self.assertEqual(result["overall"],"UNVERIFIED");self.assertEqual(len(result["attempts"]),1)
            self.assertIn("TypeError",result["error"])
    def test_delivery_failure_survives_later_rig_error_and_returns_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            def fault(args,result,target):
                result["attempts"].extend(attempts("FAIL")[:1]);raise RuntimeError("after delivery")
            status,result=self.invoke(Path(temp)/"out",Path(temp)/"missing.json",fault)
            self.assertEqual(status,1);self.assertEqual(result["overall"],"FAIL")
            self.assertEqual(result["state"],"ERROR")
    def test_incomplete_or_wrong_cases_never_aggregate_to_pass(self):
        for mode in ("empty","partial","duplicate","state","runtime","malformed","judgment"):
            result=dict(state="COMPLETE",runtime_unchanged=True,attempts=attempts())
            if mode=="empty":result["attempts"]=[]
            if mode=="partial":result["attempts"].pop()
            if mode=="duplicate":result["attempts"][-1]=result["attempts"][0]
            if mode=="state":result["state"]="RUNNING"
            if mode=="runtime":result["runtime_unchanged"]=None
            if mode=="malformed":result["attempts"]=[None]
            if mode=="judgment":result["attempts"][0]["judgment"]=None
            with self.subTest(mode=mode):self.assertEqual(tool.overall_verdict(result),"UNVERIFIED")
    def test_only_complete_four_cases_can_exit_zero(self):
        with tempfile.TemporaryDirectory() as temp:
            def complete(args,result,target):
                result.update(state="COMPLETE",runtime_unchanged=True,attempts=attempts())
            status,result=self.invoke(Path(temp)/"out",Path(temp)/"missing.json",complete)
            self.assertEqual(status,0);self.assertEqual(result["overall"],"PASS_LOCAL_LOOPBACK")
    def test_output_failure_has_explicit_unknown_exit(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/"file";path.write_text("occupied",encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()) as errors, contextlib.redirect_stdout(io.StringIO()):
                status=tool.main(["--baseline-evidence",str(Path(temp)/"missing"),"--output",str(path)])
            self.assertEqual(status,2);self.assertIn("Evidence write failed",errors.getvalue())
    def test_running_snapshots_include_overall_unknown(self):
        with tempfile.TemporaryDirectory() as temp:
            def inspect_snapshot(args,result,target):
                snapshot=json.loads(target.read_text(encoding="utf-8"))
                self.assertEqual(snapshot["state"],"RUNNING")
                self.assertEqual(snapshot["overall"],"UNVERIFIED")
                result["state"]="COMPLETE"
            status,result=self.invoke(Path(temp)/"out",Path(temp)/"missing.json",inspect_snapshot)
            self.assertEqual(status,2)
            self.assertFalse(list((Path(temp)/"out").glob("*.tmp")))


class TestCaseCleanup(unittest.TestCase):
    def test_policy_query_type_error_returns_case_unknown(self):
        with mock.patch.object(tool.net,"read_loopback_exemptions",side_effect=TypeError("policy wiring")), mock.patch.object(tool.net,"LoopbackReceiver") as receiver:
            result=tool.run_case("udp","127.0.0.1",Path("missing.exe"),Path("client"),Path("work"),{},"S-1-15-2-123",{},"sha",20)
        receiver.assert_not_called()
        self.assertEqual(result["judgment"]["verdict"],"UNVERIFIED")
        self.assertIn("TypeError",result["server_errors"][0])
        self.assertIn("error",result["policy_after"])
    def test_client_or_post_policy_error_closes_receiver_and_is_unknown(self):
        for phase in ("client","post_policy","close"):
            receiver=mock.MagicMock();receiver.port=12345;receiver.started=0;receiver.closed=30
            receiver.thread.is_alive.return_value=False;receiver.snapshot.return_value=[];receiver.errors=[]
            if phase=="close":receiver.close.side_effect=TypeError("close wiring")
            policy=dict(api_ok=True,return_code=0,cleanup_ok=True,sids=[])
            policy_effect=[policy,TypeError("post query")] if phase=="post_policy" else [policy,policy]
            with mock.patch.object(tool.net,"LoopbackReceiver",return_value=receiver), mock.patch.object(tool.net,"read_loopback_exemptions",side_effect=policy_effect), mock.patch.object(tool,"run_client",side_effect=TypeError("client wiring")), contextlib.redirect_stdout(io.StringIO()):
                result=tool.run_case("udp","127.0.0.1",Path("missing.exe"),Path("client"),Path("work"),{},"S-1-15-2-123",{},"sha",20)
            receiver.close.assert_called_once()
            self.assertEqual(result["judgment"]["verdict"],"UNVERIFIED")
            if phase=="post_policy":self.assertIn("error",result["policy_after"])
            if phase=="close":self.assertFalse(result["server_complete"])


if __name__=="__main__":unittest.main()
