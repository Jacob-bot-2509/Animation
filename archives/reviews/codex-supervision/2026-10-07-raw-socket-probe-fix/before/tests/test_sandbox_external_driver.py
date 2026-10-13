"""Simulated remote evidence and local I/O tests; never external native acceptance."""
import contextlib,copy,importlib.util,io,json,socket,subprocess,sys,tempfile,types,unittest,uuid
from pathlib import Path
from unittest import mock
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/"src"))
spec=importlib.util.spec_from_file_location("external_driver_under_test",ROOT/"tools/sandbox_external_test_driver.py")
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
from animtrain import sandbox_execution as se,full_surface_evidence as fe

class ExternalDriverTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix="external-driver-test-",dir=d.REGISTERED_ROOT)
        self.base=Path(self.temp.name).resolve()
        self.assertTrue(self.base.is_relative_to(d.REGISTERED_ROOT.resolve()))
    def tearDown(self):
        self.assertTrue(self.base.is_relative_to(d.REGISTERED_ROOT.resolve()))
        self.temp.cleanup()
    def run_main(self,args):
        stream=io.StringIO()
        with contextlib.redirect_stdout(stream):code=d.main(args)
        return code,stream.getvalue()
    def interfaces(self):
        path=self.base/"interfaces.json";err=self.base/"interfaces.err"
        if not path.exists():d.write_bytes(path,b'[{"IPAddress":"192.0.2.1","PrefixLength":24}]\r\n')
        if not err.exists():d.write_bytes(err,b"")
        return {"path":str(path),"sha256":d.digest(path),"rc":0,"stderr":"",
            "stderr_path":str(err),"stderr_sha256":d.digest(err)}
    def sender(self):
        nonces={p:{phase:uuid.uuid4().hex for phase in ("before","sandbox","after")} for p in ("tcp","udp")}
        bindings={n:se.digest(ROOT/n) for n in se.BOUND_FILES}
        states={"tcp":{"outcome":"os_denied","winerror":10013},"udp":{"outcome":"sent"}}
        raw={"schema":d.SCHEMA,"complete":True,"implementation_unchanged":True,
            "driver_source_path":str(Path(d.__file__).resolve()),"driver_before_sha256":d.digest(d.__file__),
            "driver_after_sha256":d.digest(d.__file__),"implementation_before":bindings,
            "implementation_after":bindings,"source":"SIMULATED FIXTURE, NOT A NATIVE PROBE",
            "transport":{"rc":0,"stdout":json.dumps(states)+"\n","stderr":""},
            "sender_identity":{"hostname":"sender-test"},"scope":"lan","bind":"192.0.2.10",
            "ports":{"tcp":49002,"udp":49001},"protocols":["tcp","udp"],"nonces":nonces,
            "sender_interfaces":self.interfaces(),"sandbox_started_monotonic_ns":3_000_000_000,
            "sandbox_finished_monotonic_ns":4_000_000_000,
            "observation":{"started_monotonic_ns":5_000_000_000,"finished_monotonic_ns":26_000_000_000,"elapsed_ns":21_000_000_000},
            "phases":{}}
        for p in raw["protocols"]:
            raw["phases"]["before_"+p]={"started_monotonic_ns":1_000_000_000,
                "finished_monotonic_ns":2_000_000_000,"result":{"outcome":"completed" if p=="tcp" else "sent"}}
            raw["phases"]["after_"+p]={"started_monotonic_ns":25_000_000_000,
                "finished_monotonic_ns":25_500_000_000,"result":{"outcome":"completed" if p=="tcp" else "sent"}}
        return raw
    def witness(self,sender):
        run=uuid.uuid4().hex;identity={"kind":"python_source","path":"approved-source.py",
            "sha256":d.APPROVED_WITNESSES["python_source"]}
        endpoints={p:[sender["bind"],sender["ports"][p]] for p in ("tcp","udp")}
        rows=[]
        def add(kind,mono,**fields):
            rows.append({"schema":d.WITNESS_SCHEMA,"run_id":run,"seq":len(rows)+1,
                "monotonic_ns":mono,"utc_ns":mono,"kind":kind,**fields})
        add("created",1_000_000_000,bind=sender["bind"],host="witness-test",implementation=identity)
        add("listening",2_000_000_000,endpoints=endpoints,implementation=identity)
        for phase,offset in (("before",3_000_000_000),("after",27_000_000_000)):
            for i,p in enumerate(("tcp","udp")):
                nonce=sender["nonces"][p][phase]
                add("payload",offset+i*100_000_000,protocol=p,endpoint=endpoints[p],peer=["192.0.2.1",50001],
                    payload_hex=nonce.encode().hex(),bytes=32,capture_complete=True,exact_nonce=True,nonce=nonce)
        add("closed",32_000_000_000,listeners_closed=True,deadline_reached=True,receiver_complete=True)
        summary={"schema":d.WITNESS_SCHEMA,"run_id":run,"bind":sender["bind"],"address_family":4,
            "implementation":identity,"receiver_complete":True,"implementation_unchanged":True,
            "deadline_reached":True,"listeners_closed":True,"errors":[],"interrupted":False,
            "started_monotonic_ns":2_000_000_000,"finished_monotonic_ns":32_000_000_000,
            "requested_seconds":30,"records":4,"endpoints":endpoints}
        return rows,summary
    def store_witness(self,rows,summary):
        token=uuid.uuid4().hex;log=self.base/(token+".jsonl");path=self.base/(token+".summary.json")
        d.write_bytes(log,("".join(json.dumps(r)+"\n" for r in rows)).encode())
        summary=copy.deepcopy(summary);summary["log_sha256"]=d.digest(log);d.write_json(path,summary)
        return log,path
    def verify(self,sender,rows=None,summary=None,rc=0):
        if rows is None:rows,summary=self.witness(sender)
        log,path=self.store_witness(rows,summary)
        return d.receiver_packets(sender,log,path,rc)
    def test_default_is_plan_without_any_launch_or_socket(self):
        with mock.patch.object(d.socket,"socket") as connect,mock.patch.object(d.subprocess,"run") as launch:
            rc,out=self.run_main([])
        self.assertEqual(rc,3);self.assertEqual(json.loads(out)["status"],"PLAN")
        connect.assert_not_called();launch.assert_not_called()
    def test_input_rejects_hostnames_loopback_multicast_and_round_escape(self):
        for addr,round_name in (("example.com","r"),("127.0.0.1","r"),("224.0.0.1","r"),("192.0.2.10","../escape")):
            with self.subTest(addr=addr,round_name=round_name),self.assertRaises(ValueError):
                d.validate(addr,49001,49002,round_name,21,"lan")
    def test_native_requires_literal_bind_and_named_round(self):
        rc,out=self.run_main(["--execute-native"])
        self.assertEqual(rc,2);self.assertEqual(json.loads(out)["status"],"PARTIAL")
    def test_registered_scope_rejects_project_external_and_parent_traversal(self):
        for p in (ROOT/"tools/file.json",d.REGISTERED_ROOT/"../escape.json"):
            with self.subTest(path=p),self.assertRaises(ValueError):d.registered(p,False)
    def test_file_digest_covers_exact_written_bytes_and_never_overwrites(self):
        p=self.base/"proof";payload=b"\xff\x00line\r\n\n"
        checksum=d.write_bytes(p,payload)
        self.assertEqual(checksum,d.digest(p));self.assertEqual(p.read_bytes(),payload)
        with self.assertRaises(FileExistsError):d.write_bytes(p,b"replacement")
        self.assertEqual(p.read_bytes(),payload)
    def test_json_digest_includes_its_actual_newline(self):
        p=self.base/"proof.json";checksum=d.write_json(p,{"test":True})
        self.assertTrue(p.read_bytes().endswith(b"\n"));self.assertEqual(checksum,d.digest(p))
    def test_subprocess_binary_outputs_are_complete_and_bound(self):
        cp=subprocess.CompletedProcess(["cmd"],0,b"\xff\xfeRAW\r\n",b"E"*5000)
        with mock.patch.object(d.subprocess,"run",return_value=cp):
            result=d.capture(["cmd"],self.base,"binary",30)
        self.assertEqual(Path(result["path"]).read_bytes(),cp.stdout)
        self.assertEqual(Path(result["stderr_path"]).read_bytes(),cp.stderr)
        self.assertEqual(result["sha256"],d.digest(result["path"]))
        self.assertEqual(result["stderr_sha256"],d.digest(result["stderr_path"]))
        self.assertEqual(len(result["stderr"]),5000)
    def test_subprocess_timeout_keeps_partial_original_streams(self):
        exc=subprocess.TimeoutExpired(["cmd"],30,output=b"PARTIAL\xff",stderr=b"ERR")
        with mock.patch.object(d.subprocess,"run",side_effect=exc):
            result=d.capture(["cmd"],self.base,"timeout",30)
        self.assertIsNone(result["rc"]);self.assertTrue(result["timed_out"])
        self.assertEqual(Path(result["path"]).read_bytes(),exc.stdout)
    def execute_probe(self,error):
        sockets=[]
        for _ in range(2):
            s=mock.MagicMock();s.__enter__.return_value=s;s.sendto.side_effect=error;s.connect.side_effect=error;sockets.append(s)
        fake=types.SimpleNamespace(AF_INET=2,AF_INET6=23,SOCK_DGRAM=2,SOCK_STREAM=1,
            socket=mock.Mock(side_effect=sockets))
        output=io.StringIO()
        with mock.patch.dict(sys.modules,{"_socket":fake}),contextlib.redirect_stdout(output):
            exec(d.probe_source("192.0.2.10",{"tcp":49002,"udp":49001},
                {p:{"sandbox":uuid.uuid4().hex} for p in ("tcp","udp")},["udp","tcp"]),{})
        return json.loads(output.getvalue())
    def test_probe_classifies_only_actual_10013_as_os_denied(self):
        error=PermissionError("denied");error.winerror=10013
        data=self.execute_probe(error)
        self.assertTrue(all(v["outcome"]=="os_denied" and v["winerror"]==10013 for v in data.values()))
    def test_probe_typed_timeout_and_unknown_error_are_distinct(self):
        for error,outcome in ((TimeoutError("deadline"),"timeout"),(OSError("network failed"),"error")):
            data=self.execute_probe(error)
            with self.subTest(outcome=outcome):self.assertTrue(all(v["outcome"]==outcome and type(v["elapsed_ns"]) is int for v in data.values()))
    def test_healthy_sender_does_not_claim_receiver_delivery(self):
        s=mock.MagicMock();s.__enter__.return_value=s
        with mock.patch.object(d.socket,"socket",return_value=s):
            result=d.send(("192.0.2.10",49002),b"A"*32,socket.AF_INET,"tcp")
        self.assertEqual(result["outcome"],"completed");self.assertFalse(result["receiver_delivery_verified"])
        s.shutdown.assert_called_once_with(socket.SHUT_WR)
    def test_same_host_and_same_64_cannot_be_external(self):
        p=self.base/"v6.json";err=self.base/"v6.err"
        d.write_bytes(p,b'[{"IPAddress":"2001:4860:1000::1","PrefixLength":64}]');d.write_bytes(err,b"")
        proof={"path":str(p),"sha256":d.digest(p),"rc":0,"stderr":"","stderr_path":str(err),"stderr_sha256":d.digest(err)}
        for address in ("2001:4860:1000::1","2001:4860:1000::abcd"):
            with self.subTest(address=address),self.assertRaises(ValueError):
                d.check_scope(__import__("ipaddress").ip_address(address),"external",proof)
    def test_full_witness_recognizes_exact_healthy_controls(self):
        sender=self.sender();packets,receipt=self.verify(sender)
        self.assertEqual(set(packets),{"tcp","udp"});self.assertEqual(receipt["rc"],0)
        self.assertTrue(all(len(v)==2 for v in packets.values()))
    def test_actual_sandbox_nonce_fails_even_when_capture_marked_incomplete(self):
        sender=self.sender();rows,summary=self.witness(sender)
        row=rows[2];nonce=sender["nonces"][row["protocol"]]["sandbox"]
        row.update(payload_hex=(nonce+"EXTRA").encode().hex(),nonce=None,capture_complete=False,exact_nonce=False,bytes=37)
        with self.assertRaises(fe.BoundaryFailure):self.verify(sender,rows,summary)
    def test_missing_duplicate_and_out_of_order_receiver_controls_rejected(self):
        for mode in ("missing","duplicate","reverse"):
            sender=self.sender();rows,summary=self.witness(sender)
            if mode=="missing":rows.pop(4);summary["records"]-=1
            elif mode=="duplicate":rows[4].update({k:rows[2][k] for k in ("payload_hex","nonce")})
            else:
                rows[2].update({k:rows[4][k] for k in ("payload_hex","nonce")})
                rows[4].update(payload_hex=sender["nonces"]["tcp"]["before"].encode().hex(),nonce=sender["nonces"]["tcp"]["before"])
            for i,r in enumerate(rows,1):r["seq"]=i
            with self.subTest(mode=mode),self.assertRaises(ValueError):self.verify(sender,rows,summary)
    def test_wrong_endpoint_unknown_payload_and_other_protocol_rejected(self):
        for mode in ("endpoint","unknown","protocol"):
            sender=self.sender();rows,summary=self.witness(sender)
            if mode=="endpoint":rows[2]["endpoint"]=["192.0.2.11",49002]
            elif mode=="protocol":rows[2]["protocol"]="icmp"
            else:rows[2].update(payload_hex=("B"*32).encode().hex(),nonce="B"*32)
            with self.subTest(mode=mode),self.assertRaises(ValueError):self.verify(sender,rows,summary)
    def test_receiver_rc_boolean_is_not_native_zero(self):
        sender=self.sender()
        for rc in (False,2,None):
            with self.subTest(rc=rc),self.assertRaises(ValueError):self.verify(sender,rc=rc)
    def test_receiver_lifecycle_duration_version_identity_and_count_are_required(self):
        for field,value in (("receiver_complete",False),("errors",[{}]),("interrupted",True),
            ("finished_monotonic_ns",31_999_999_999),("records",3)):
            sender=self.sender();rows,summary=self.witness(sender);summary[field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):self.verify(sender,rows,summary)
        sender=self.sender();rows,summary=self.witness(sender);summary["implementation"]["sha256"]="0"*64
        with self.assertRaises(ValueError):self.verify(sender,rows,summary)
    def test_sender_and_receiver_must_be_distinct_hosts(self):
        sender=self.sender();rows,summary=self.witness(sender);rows[0]["host"]="SENDER-TEST"
        with self.assertRaises(ValueError):self.verify(sender,rows,summary)
    def test_log_hash_sequence_and_closed_record_corruption_fail(self):
        sender=self.sender();rows,summary=self.witness(sender);log,path=self.store_witness(rows,summary)
        with log.open("ab") as f:f.write(b"\n")
        with self.assertRaisesRegex(ValueError,"hash"):d.receiver_packets(sender,log,path,0)
        rows[2]["seq"]=100
        with self.assertRaises(ValueError):self.verify(sender,rows,summary)
        rows,summary=self.witness(sender);rows.pop()
        with self.assertRaises(ValueError):self.verify(sender,rows,summary)
    def reconcile_args(self,sender):
        p=self.base/("sender-"+uuid.uuid4().hex+".json");d.write_json(p,sender)
        rows,summary=self.witness(sender);log,path=self.store_witness(rows,summary)
        return types.SimpleNamespace(reconcile=p,receiver_log=log,receiver_summary=path,receiver_rc=0)
    def test_reconciliation_keeps_original_sender_and_only_exports_scoped_cases(self):
        sender=self.sender();args=self.reconcile_args(sender);original=args.reconcile.read_bytes()
        def transport(row):return row["transport"],json.loads(row["transport"]["stdout"])
        with mock.patch.object(fe,"transport",side_effect=transport),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(d.reconcile(args),0)
        self.assertEqual(args.reconcile.read_bytes(),original)
        outputs=list(self.base.glob("reconciled-*.json"));self.assertEqual(len(outputs),1)
        result=json.loads(outputs[0].read_bytes())
        self.assertFalse(result["full_surface_accepted"]);self.assertEqual(result["production_gate"],"CLOSED")
        self.assertTrue(all(r["point"]=="D9" for r in result["cases"].values()))
    def test_reconciliation_never_trusts_legacy_pass_labels(self):
        args=self.reconcile_args(self.sender())
        args.reconcile.write_text(json.dumps({"status":"GREEN","complete":True}),encoding="utf-8")
        with self.assertRaisesRegex(ValueError,"unsupported"):d.reconcile(args)
    def test_reconciliation_rejects_after_outside_window_or_early(self):
        for offset in (24_999_999_999,26_000_000_001):
            sender=self.sender();sender["phases"]["after_tcp"]["started_monotonic_ns"]=offset
            args=self.reconcile_args(sender)
            with mock.patch.object(fe,"transport",return_value=(sender["transport"],json.loads(sender["transport"]["stdout"]))):
                with self.assertRaises(ValueError):d.reconcile(args)
    def test_reconciliation_source_and_nonce_bindings_cannot_be_bypassed(self):
        for mode in ("source","nonce"):
            sender=self.sender()
            if mode=="source":sender["driver_before_sha256"]=sender["driver_after_sha256"]="0"*64
            else:sender["nonces"]["udp"]["before"]=sender["nonces"]["tcp"]["before"]
            with self.subTest(mode=mode),self.assertRaises(ValueError):d.reconcile(self.reconcile_args(sender))
    def test_boolean_or_unordered_native_timestamps_cannot_pass(self):
        for field in ("sandbox_started_monotonic_ns","sandbox_finished_monotonic_ns"):
            sender=self.sender();sender[field]=True;args=self.reconcile_args(sender)
            with mock.patch.object(fe,"transport",return_value=(sender["transport"],json.loads(sender["transport"]["stdout"]))):
                with self.assertRaises(ValueError):d.reconcile(args)
        sender=self.sender();sender["phases"]["before_tcp"]["started_monotonic_ns"]=True
        with mock.patch.object(fe,"transport",return_value=(sender["transport"],json.loads(sender["transport"]["stdout"]))):
            with self.assertRaises(ValueError):d.reconcile(self.reconcile_args(sender))
    def test_collection_preserves_full_transport_and_records_measured_window(self):
        clock=types.SimpleNamespace(value=100_000_000_000)
        def now():clock.value+=100_000;return clock.value
        def wait(deadline):clock.value=max(clock.value,deadline)
        cp={"rc":0,"stdout":"\n"+json.dumps({"tcp":{"outcome":"os_denied","winerror":10013},"udp":{"outcome":"sent"}})+"\n",
            "stderr":"FULL UNTRUNCATED STDERR\n"*500,"work":"SIMULATED ONLY","source_sha256":"test"}
        args=types.SimpleNamespace(bind="192.0.2.10",udp_port=49001,tcp_port=49002,
            round="unit-collect",observe_seconds=21,scope="lan",out=self.base,protocol="both")
        def capture(command,directory,tag,timeout):
            stdout=directory/(tag+".stdout.bin");stderr=directory/(tag+".stderr.bin")
            body=b"TRACE" if tag=="route" else b'[{"IPAddress":"192.0.2.1","PrefixLength":24}]'
            d.write_bytes(stdout,body);d.write_bytes(stderr,b"")
            return {"path":str(stdout),"sha256":d.digest(stdout),"stderr_path":str(stderr),
                "stderr_sha256":d.digest(stderr),"rc":0,"stderr":""}
        with (mock.patch.object(d,"capture",side_effect=capture),mock.patch.object(d,"send",return_value={"outcome":"sent"}),
            mock.patch.object(d.time,"monotonic_ns",side_effect=now),mock.patch.object(d,"wait_until",side_effect=wait),
            mock.patch.object(se,"run_code",return_value=cp),contextlib.redirect_stdout(io.StringIO())):
            self.assertEqual(d.collect(args),0)
        sender=json.loads(next(self.base.glob("remote-*/sender.json")).read_bytes())
        self.assertEqual(sender["transport"],cp);self.assertEqual(sender["verification_status"],"UNVERIFIED")
        obs=sender["observation"];self.assertGreaterEqual(obs["elapsed_ns"],21_000_000_000)
        for p in ("tcp","udp"):
            self.assertGreaterEqual(sender["phases"]["after_"+p]["started_monotonic_ns"],obs["started_monotonic_ns"]+20_000_000_000)

if __name__=="__main__":unittest.main()
