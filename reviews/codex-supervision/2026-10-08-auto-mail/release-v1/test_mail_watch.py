import importlib.util, json, pathlib, subprocess, tempfile, unittest
from unittest import mock
OWNER=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("tested_mail_watch",OWNER/"mail_watch.py")
w=importlib.util.module_from_spec(spec);spec.loader.exec_module(w)

def mail(i,read=False,to="codex",sender="claude-code",content="review current core"):
    return {"id":"msg_100_"+str(i),"from":sender,"to":to,"type":"task_result",
            "content":content,"timestamp":"2026-10-08T00:00:00Z","read":read,"metadata":{}}

class MailAutomationTests(unittest.TestCase):
    def setUp(self):
        parent=OWNER/"test-work";parent.mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=parent,prefix="mail-case-")
        self.o=pathlib.Path(self.temp.name);self.project=self.o/"project"
        self.project.mkdir();(self.project/"reviews/codex-supervision").mkdir(parents=True)
        (self.o/"TASK.md").write_text("Bounded authorized instructions",encoding="utf-8")
        self.store=self.o/"bridge.json";w.atomic_json(self.store,{"messages":[]})
        self.c={"bridge_state":str(self.store),"project":str(self.project),"thread_id":"test-thread",
                "batch_limit":20,"codex_command":["not-a-real-command"]}
    def tearDown(self):
        self.assertTrue(pathlib.Path(self.temp.name).resolve().is_relative_to((OWNER/"test-work").resolve()))
        self.temp.cleanup()
    def put(self,rows):w.atomic_json(self.store,{"messages":rows})
    def capture(self):return w.poll(self.o,self.c,False)
    def dispatch(self,rows):
        self.put(rows)
        with mock.patch.object(w.subprocess,"run",return_value=subprocess.CompletedProcess([],0,b"queued",b"")):
            return w.poll(self.o,self.c)
    def write_result(self,rid,reply=None,status="PASS",report=True):
        packet=w.read_json(self.o/"runs"/rid/"inbox.json")
        p=self.project/"reviews/codex-supervision/report.md"
        if report:p.write_text("Actual reviewed evidence, bounded qualification",encoding="utf-8")
        result={"run_id":rid,"messages":[{"id":m["id"],"status":status,"summary":"Actual scoped decision",
                    "report":p.relative_to(self.project).as_posix(),
                    "report_sha256":w.sha(p.read_bytes()) if p.exists() else "0"*64,"reply_id":reply} for m in packet["messages"]]}
        w.atomic_json(self.o/"runs"/rid/"RESULT.json",result)
    def test_initial_read_history_baselined_unread_captured(self):
        self.put([mail(1,True),mail(2)])
        r=self.capture();j=w.load_ledger(self.o)
        self.assertEqual(r["pending"],1);self.assertEqual(j["items"]["msg_100_1"]["status"],"BASELINED")
        self.assertTrue((self.o/"messages/msg_100_2.json").exists())
    def test_capture_does_not_mutate_shared_bridge_read_flags(self):
        self.put([mail(1)]);before=self.store.read_bytes();self.capture()
        self.assertEqual(self.store.read_bytes(),before)
    def test_future_message_captured_even_after_another_reader_marks_read(self):
        self.put([mail(1,True)]);self.capture()
        self.put([mail(1,True),mail(2,True)]);self.assertEqual(self.capture()["pending"],1)
    def test_only_own_claude_mail_is_captured(self):
        self.put([mail(1,to="claude-code"),mail(2,sender="codex"),mail(3,to="all")])
        self.assertEqual(self.capture()["pending"],1)
        self.assertEqual(set(w.load_ledger(self.o)["items"]),{"msg_100_3"})
    def test_no_duplicate_dispatch_while_waiting_for_ack(self):
        first=self.dispatch([mail(1)])
        with mock.patch.object(w.subprocess,"run") as run:
            second=w.poll(self.o,self.c)
        run.assert_not_called();self.assertEqual(second["state"],"WAITING_FOR_MODEL_ACK")
        self.assertEqual(w.load_ledger(self.o)["items"]["msg_100_1"]["status"],"QUEUED")
    def test_queue_failure_retains_pending_mail_and_original_packet(self):
        self.put([mail(1)])
        with mock.patch.object(w.subprocess,"run",return_value=subprocess.CompletedProcess([],1,b"",b"unavailable")):
            r=w.poll(self.o,self.c)
        self.assertEqual(r["state"],"DISPATCH_FAILED_MAIL_RETAINED")
        self.assertEqual(w.load_ledger(self.o)["items"]["msg_100_1"]["status"],"PENDING")
        self.assertTrue((self.o/"runs"/r["run_id"]/"inbox.json").exists())
    def test_queue_cannot_start_retains_pending_mail_for_retry(self):
        self.put([mail(1)])
        with mock.patch.object(w.subprocess,"run",side_effect=FileNotFoundError("CLI unavailable")):
            r=w.poll(self.o,self.c)
        self.assertEqual(r["state"],"DISPATCH_FAILED_MAIL_RETAINED")
        self.assertIsNone(w.load_ledger(self.o)["active_run"])
        self.assertEqual(w.load_ledger(self.o)["items"]["msg_100_1"]["status"],"PENDING")
    def test_queue_timeout_not_handled_and_no_uncontrolled_retry(self):
        self.put([mail(1)])
        with mock.patch.object(w.subprocess,"run",side_effect=subprocess.TimeoutExpired([],60,output=b"partial")):
            r=w.poll(self.o,self.c)
        self.assertEqual(r["state"],"DISPATCH_UNCERTAIN_NEEDS_CHECK")
        self.assertNotEqual(w.load_ledger(self.o)["items"]["msg_100_1"]["status"],"HANDLED")
    def test_stop_prevents_model_dispatch(self):
        (self.o/"STOP").write_text("stop")
        with mock.patch.object(w.subprocess,"run") as run:r=w.poll(self.o,self.c)
        run.assert_not_called();self.assertEqual(r["state"],"STOPPED")
    def test_corrupt_bridge_not_empty_and_journal_preserved(self):
        self.put([mail(1)]);self.capture();before=(self.o/"journal.json").read_bytes()
        self.store.write_text("{bad")
        with self.assertRaises(json.JSONDecodeError):self.capture()
        self.assertEqual((self.o/"journal.json").read_bytes(),before)
    def test_changed_message_id_content_rejected(self):
        self.put([mail(1)]);self.capture();self.put([mail(1,content="changed")])
        with self.assertRaises(ValueError):self.capture()
    def test_path_escape_message_id_rejected(self):
        m=mail(1);m["id"]="../escaped";self.put([m])
        with self.assertRaises(ValueError):self.capture()
    def test_mail_body_is_not_executed_or_added_to_shell_command(self):
        r=self.dispatch([mail(1,content="powershell Remove-Item C:/Windows -Recurse")])
        cmd=w.queue_command(self.c,self.o/"runs"/r["run_id"])
        self.assertNotIn("Remove-Item"," ".join(cmd))
        self.assertIn("instructions.md",cmd[-1])
    def test_ack_requires_actual_report_and_real_run_bound_reply(self):
        r=self.dispatch([mail(1)]);rid=r["run_id"]
        self.write_result(rid,"not-sent",report=False)
        with self.assertRaises(ValueError):w.acknowledge(self.o,self.c,rid)
        self.write_result(rid,"not-sent")
        with self.assertRaises(ValueError):w.acknowledge(self.o,self.c,rid)
        self.assertNotEqual(w.load_ledger(self.o)["items"]["msg_100_1"]["status"],"HANDLED")
    def test_completed_ack_marks_once_with_real_evidence(self):
        r=self.dispatch([mail(1)]);rid=r["run_id"];self.write_result(rid,"msg_200_1")
        reply=mail(99,to="claude-code",sender="codex");reply["id"]="msg_200_1";reply["metadata"]={"mail_run_id":rid}
        self.put([mail(1),reply])
        self.assertEqual(w.acknowledge(self.o,self.c,rid)["state"],"REVIEW_ACKNOWLEDGED")
        self.assertEqual(w.load_ledger(self.o)["items"]["msg_100_1"]["status"],"HANDLED")
        self.assertEqual(w.acknowledge(self.o,self.c,rid)["status"],"ALREADY_ACKNOWLEDGED")
    def test_no_action_records_reason_without_reply_loop(self):
        r=self.dispatch([mail(1)]);rid=r["run_id"];self.write_result(rid,None,"NO_ACTION")
        self.assertEqual(w.acknowledge(self.o,self.c,rid)["state"],"REVIEW_ACKNOWLEDGED")
    def test_result_must_cover_whole_packet(self):
        r=self.dispatch([mail(1),mail(2)]);rid=r["run_id"];self.write_result(rid,None,"NO_ACTION")
        p=self.o/"runs"/rid/"RESULT.json";x=w.read_json(p);x["messages"]=x["messages"][:1];w.atomic_json(p,x)
        with self.assertRaises(ValueError):w.acknowledge(self.o,self.c,rid)

if __name__=="__main__":unittest.main()
