import datetime as dt
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("start_watch", HERE / "start_watch.py")
w = importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)

def snapshot(rows, stamp=1000, status="OK"):
    return {"time": dt.datetime.fromtimestamp(stamp, dt.timezone.utc).isoformat(),
            "claude_tree": rows, "process_observation": {"status": status}, "head": "abc"}

def proc(pid, name="claude.exe", parent=1):
    return {"ProcessId": pid, "ParentProcessId": parent, "Name": name}

def record(path=r"D:\Animation-Model-Training\docs\a.md", kind="assistant"):
    return {"type": kind, "uuid": "row1", "timestamp": "t", "message": {"content": [
        {"type": "tool_use", "id": "tool1", "name": "Edit", "input": {
            "file_path": path, "new_string": "PRIVATE CONTENT NOT TO COPY"}}]}}

class WatchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="watch-test-", dir=HERE)
        self.home = Path(self.temp.name)
        assert self.home.resolve().is_relative_to(HERE.resolve())
    def tearDown(self):
        self.temp.cleanup()
    def put(self, name, value):
        p = self.home / name
        p.write_text(json.dumps(value)+"\n", encoding="utf-8")
        return p
    def cfg(self):
        return {"project": str(w.PROJECT), "thread_id": "existing-thread",
                "codex_command": ["node", "fixed-codex.js"], "claude_log_roots": [str(self.home)]}
    def test_baseline_does_not_claim_new_start(self):
        s=w.initial(); w.observe_processes(s,snapshot([proc(5)]),1000)
        self.assertEqual(s["pending"][0]["kind"],"CLAUDE_PRESENT_BASELINE_NOT_PROVEN_NEW_START")
    def test_same_snapshot_deduplicates(self):
        s=w.initial()
        for _ in range(3): w.observe_processes(s,snapshot([proc(5),proc(6,"conhost.exe",5)]),1000)
        self.assertEqual(len(s["pending"]),1)
    def test_child_start_detected(self):
        s=w.initial();w.observe_processes(s,snapshot([proc(5)]),1000);s["pending"]=[]
        w.observe_processes(s,snapshot([proc(5),proc(8,"powershell.exe",5)]),1000)
        self.assertEqual(s["pending"][0]["detail"]["pid"],8)
    def test_stale_future_unavailable_not_work(self):
        for snap in (snapshot([proc(5)],900),snapshot([proc(5)],1020),snapshot([proc(5)],1000,"UNAVAILABLE")):
            s=w.initial()
            with self.assertRaises(ValueError):w.observe_processes(s,snap,1000)
            self.assertEqual(s["pending"],[])
    def test_tool_signal_minimal_no_source_contents(self):
        out=w.tool_signals(record())
        self.assertEqual(len(out),1)
        self.assertNotIn("PRIVATE",json.dumps(out))
        self.assertNotIn("new_string",json.dumps(out))
    def test_outside_project_and_lookalike_refused(self):
        for p in (r"D:\code\foo.md",r"D:\Animation-Model-Training-EVIL\a.md","https://example.com/Animation-Model-Training"):
            self.assertEqual(w.tool_signals(record(p)),[])
    def test_api_request_duplicate_ignored(self):
        self.assertEqual(w.tool_signals(record(kind="api-request-blob")),[])
    def test_bash_slash_project_path(self):
        r=record();r["message"]["content"][0]["input"]={"command":"cd /d/Animation-Model-Training && git diff"}
        self.assertEqual(len(w.tool_signals(r)),1)
    def test_initial_log_history_not_replayed(self):
        p=self.put("old.jsonl",record())
        end,out,gap=w.read_log_delta(p,None)
        self.assertEqual((end,out,gap),(p.stat().st_size,[],None))
    def test_log_append_read_once(self):
        p=self.put("s.jsonl",{"type":"user"})
        end,_,_=w.read_log_delta(p,None)
        with p.open("a",encoding="utf-8") as f:f.write(json.dumps(record())+"\n")
        end,out,_=w.read_log_delta(p,end)
        self.assertEqual(len(out),1)
        self.assertEqual(w.read_log_delta(p,end)[1],[])
    def test_new_session_after_enable_not_discarded(self):
        s=w.initial();w.scan_logs(s,self.cfg())
        self.put("new.jsonl",record());w.scan_logs(s,self.cfg())
        self.assertEqual(len(s["pending"]),1)
    def test_partial_line_waits_until_complete(self):
        p=self.home/"p.jsonl";v=json.dumps(record())
        p.write_text(v[:20],encoding="utf-8")
        end,out,gap=w.read_log_delta(p,0)
        self.assertEqual((end,out,gap),(0,[],None))
        p.write_text(v+"\n",encoding="utf-8")
        self.assertEqual(len(w.read_log_delta(p,end)[1]),1)
    def test_oversize_gap_recorded_and_tail_seen(self):
        p=self.home/"big.jsonl"
        p.write_bytes(b"x"*(w.MAX_READ+20)+b"\n"+json.dumps(record()).encode()+b"\n")
        end,out,gap=w.read_log_delta(p,0)
        self.assertEqual(end,p.stat().st_size)
        self.assertEqual(gap,"LOG_DELTA_EXCEEDS_LIMIT")
        self.assertEqual(len(out),1)
    def test_oversize_single_line_advances_not_infinite_gap(self):
        p=self.home/"big.jsonl";p.write_bytes(b"x"*(w.MAX_READ+20))
        end,out,gap=w.read_log_delta(p,0)
        self.assertEqual(end,p.stat().st_size);self.assertIsNotNone(gap)
        self.assertEqual(w.read_log_delta(p,end),(end,[],None))
    def test_rotation_gap_not_silent(self):
        p=self.put("rotate.jsonl",record())
        end,out,gap=w.read_log_delta(p,p.stat().st_size+5)
        self.assertEqual(gap,"LOG_TRUNCATED");self.assertEqual(len(out),1)
    def test_overflow_is_explicit(self):
        s=w.initial()
        for i in range(300):w.push(s,"TEST",{"i":i})
        self.assertEqual(len(s["pending"]),200)
        self.assertEqual(s["pending"][0]["kind"],"SIGNAL_OVERFLOW_REQUIRES_GAP_ACCOUNTING")
        self.assertEqual(s["pending"][0]["omitted_count"],101)
    def test_reserved_before_dispatch_and_pending_kept(self):
        s=w.initial();w.push(s,"A",{})
        run=w.reserve(self.home,s,"REVIEW")
        self.assertEqual(w.read(self.home/"state.json")["active"]["status"],"DISPATCHING")
        self.assertEqual(len(w.read(run/"signals.json")["signals"]),1)
        w.push(s,"B",{})
        self.assertEqual(len(s["pending"]),1)
    def test_queue_success_not_review_and_no_permission_override(self):
        s=w.initial();run=w.reserve(self.home,s,"REVIEW");calls=[]
        def runner(cmd,**kw):
            calls.append(cmd)
            return subprocess.CompletedProcess(cmd,0,b"queued",b"")
        r=w.dispatch(self.home,self.cfg(),run,s,runner)
        self.assertEqual(r["status"],"QUEUED_NOT_YET_REVIEWED")
        self.assertEqual(calls[0][2:6],["queue","--thread","existing-thread","--message"])
        self.assertFalse(any(x in calls[0] for x in ("--model","--sandbox","--yolo","--dangerously-bypass-approvals-and-sandbox")))
        self.assertFalse((run/"ACK.json").exists())
    def test_timeout_and_nonzero_no_duplicate_retry(self):
        for mode in ("timeout","nonzero","oserror"):
            s=w.initial();run=w.reserve(self.home,s,"REVIEW")
            def runner(cmd,**kw):
                if mode=="timeout":raise subprocess.TimeoutExpired(cmd,60)
                if mode=="oserror":raise OSError("not started")
                return subprocess.CompletedProcess(cmd,1,b"",b"error")
            r=w.dispatch(self.home,self.cfg(),run,s,runner)
            self.assertEqual(r["status"],"DISPATCH_UNCERTAIN_NEEDS_CHECK")
            self.assertIsNotNone(w.read(self.home/"state.json")["active"])
    def test_selftest_receipt_requires_explicit_ack(self):
        s=w.initial();run=w.reserve(self.home,s,"SELFTEST")
        w.dispatch(self.home,self.cfg(),run,s,lambda cmd,**kw: subprocess.CompletedProcess(cmd,0,b"",b""))
        self.assertFalse((self.home/"SELFTEST_ACK.json").exists())
        receipt=w.acknowledge(self.home,self.cfg(),run.name,True)
        self.assertEqual(receipt["status"],"RECEIVED")
        self.assertIsNone(w.read(self.home/"state.json")["active"])
    def test_review_cannot_be_acked_as_selftest(self):
        s=w.initial();run=w.reserve(self.home,s,"REVIEW")
        w.dispatch(self.home,self.cfg(),run,s,lambda cmd,**kw: subprocess.CompletedProcess(cmd,0,b"",b""))
        with self.assertRaises(ValueError):w.acknowledge(self.home,self.cfg(),run.name,True)
    def test_packet_mutation_rejected(self):
        s=w.initial();run=w.reserve(self.home,s,"SELFTEST")
        w.dispatch(self.home,self.cfg(),run,s,lambda cmd,**kw: subprocess.CompletedProcess(cmd,0,b"",b""))
        w.atomic(run/"signals.json",{"tampered":True})
        with self.assertRaises(ValueError):w.acknowledge(self.home,self.cfg(),run.name,True)
    def test_crash_after_ack_before_state_update_recovers(self):
        s=w.initial();run=w.reserve(self.home,s,"SELFTEST")
        w.dispatch(self.home,self.cfg(),run,s,lambda cmd,**kw: subprocess.CompletedProcess(cmd,0,b"",b""))
        w.atomic(run/"ACK.json",{"run_id":run.name,"status":"RECEIVED","time":"actual"})
        result=w.acknowledge(self.home,self.cfg(),run.name,True)
        self.assertIsNone(w.read(self.home/"state.json")["active"])
        self.assertEqual(result["time"],"actual")
        self.assertEqual(len(w.read(self.home/"state.json")["history"]),1)
        w.acknowledge(self.home,self.cfg(),run.name,True)
        self.assertEqual(len(w.read(self.home/"state.json")["history"]),1)
    def test_report_must_be_frozen_with_actual_reply(self):
        # Test a temporary fake project, never touch a real frozen archive.
        project=self.home/"project";folder=project/"archives/reviews/codex-supervision/x";folder.mkdir(parents=True)
        report=folder/"REPORT.md";report.write_text("review",encoding="utf-8")
        manifest={"actual_reply_id":"real","artifacts":[{"path":"REPORT.md","sha256":w.digest(report),"bytes":6}]}
        w.atomic(folder/"delivery-manifest.json",manifest)
        with patch.object(w,"PROJECT",project):
            with self.assertRaises(ValueError):w.validate_review(report,"real",{"messages":[]})
            out=w.validate_review(report,"real",{"messages":[{"id":"real","from":"codex","to":"claude-code"}]})
            self.assertEqual(out["reply_id"],"real")
            report.write_text("changed",encoding="utf-8")
            with self.assertRaises(ValueError):w.validate_review(report,"real",{"messages":[{"id":"real","from":"codex","to":"claude-code"}]})
    def test_parent_traversal_refused(self):
        with self.assertRaises(ValueError):w.no_reparse(self.home/".."/"elsewhere.md")
    def test_fallback_query_failure_not_empty_work(self):
        with patch.object(w,"OBSERVER",self.home/"missing.json"):
            with self.assertRaises(ValueError):
                w.process_snapshot(lambda cmd,**kw:subprocess.CompletedProcess(cmd,1,b"",b"denied"))
    def test_fallback_query_success_is_labeled(self):
        with patch.object(w,"OBSERVER",self.home/"missing.json"):
            snap,source=w.process_snapshot(lambda cmd,**kw:subprocess.CompletedProcess(cmd,0,json.dumps(proc(5)).encode(),b""))
        self.assertEqual(source,"READ_ONLY_CIM_FALLBACK")
        self.assertEqual(snap["claude_tree"],[proc(5)])
    def test_active_run_does_not_requeue_and_new_signals_stay_pending(self):
        s=w.initial();run=w.reserve(self.home,s,"SELFTEST")
        w.dispatch(self.home,self.cfg(),run,s,lambda cmd,**kw: subprocess.CompletedProcess(cmd,0,b"",b""))
        with patch.object(w,"OBSERVER",self.put("observer.json",snapshot([proc(5)],stamp=__import__("time").time()))):
            with patch.object(w,"dispatch",side_effect=AssertionError("duplicate")):
                w.tick(self.home,self.cfg())
        state=w.read(self.home/"state.json")
        self.assertEqual(state["active"]["run_id"],run.name)
        self.assertGreater(len(state["pending"]),0)

if __name__ == "__main__":
    unittest.main(verbosity=2)
