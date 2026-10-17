
"""Independent adversarial tests; project-owned scratch, no native experiment."""
import copy, hashlib, json, os, shutil, subprocess, sys, tempfile, unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch
import exec_native_roots as m

P=Path(r"D:\Animation-Model-Training")
SCRATCH=P/"reviews/codex-supervision/2026-10-17-real-root-handler-test-runtime"
BOUNDS={"src/example.py":"c"*64}
TOOLS={"collector_sha256":"a"*64,"verifier_sha256":"b"*64}

def raw(doc):
    return json.dumps(doc,sort_keys=True).encode()

def fixture():
    genesis={"schema":m.SCHEMA,"entries":[],"previous_registry_sha256":None}
    row={"root_id":"r001","root_path":"reviews/exec-native/run-r001","purpose":"surface",
         "cohort":{**TOOLS,"bound_files_sha256_map":copy.deepcopy(BOUNDS)},
         "bound_paths":["raw","work","media"],"status":"REGISTERED",
         "created_at":"2026-10-17T00:00:00+00:00"}
    registered={"schema":m.SCHEMA,"entries":[row],
                "previous_registry_sha256":hashlib.sha256(raw(genesis)).hexdigest()}
    active=copy.deepcopy(registered);active["entries"][0]["status"]="ACTIVE"
    active["previous_registry_sha256"]=hashlib.sha256(raw(registered)).hexdigest()
    return active,{"current_tool_hashes":copy.deepcopy(TOOLS),"history":raw(registered),
                   "existing_paths":[],"reparse_paths":[]}

class PolicyTests(unittest.TestCase):
    def setUp(self):
        self.reg,self.ctx=fixture()
        self.digest=m.sha_object(self.reg["entries"][0]["cohort"])

    def write(self,path="raw/proof.json",**kw):
        return m.check_write(self.reg,"r001",path,self.digest,current_bound_map=BOUNDS,
                             **self.ctx,**kw)[0]

    def test_valid_context_and_parent_write(self):
        self.assertEqual(m.check_registry(self.reg,BOUNDS,**self.ctx),[])
        self.assertTrue(self.write())

    def test_no_trusted_pins_or_history(self):
        for field in ("current_tool_hashes","history"):
            ctx=dict(self.ctx);ctx.pop(field)
            self.assertTrue(m.check_registry(self.reg,BOUNDS,**ctx))

    def test_empty_or_missing_full_cohort(self):
        for d in ("",None,"b"*64,"a"*64+"\n",[],{}):
            with self.subTest(d=d):
                self.assertFalse(m.check_write(self.reg,"r001","raw/x",d,
                                   current_bound_map=BOUNDS,**self.ctx)[0])

    def test_child_cannot_write_parent_raw(self):
        self.assertFalse(self.write(writer="child"))
        self.assertTrue(self.write("work/stdout.txt",writer="child"))

    def test_directory_alone_and_outside_closed_paths(self):
        for p in ("raw","media","logs/x","RAW/x"):
            self.assertFalse(self.write(p))

    def test_windows_path_adversaries(self):
        for p in ("../x","raw/../x","raw/./x","raw//x","/raw/x","C:/x",
                  r"raw\x/y",r"\\server\share\x","raw/COM1.txt","raw/LPT9.log",
                  "raw/CON.json","raw/NUL","raw/x.","raw/x ","raw/x:ads",
                  'raw/x"y',"raw/a|b","raw/a<b","raw/a>b","raw/*","raw/x\n"):
            with self.subTest(p=p):
                self.assertFalse(self.write(p))

    def test_newline_id_and_sha(self):
        self.assertFalse(m.valid_root_id("r001\n"))
        self.assertFalse(m.is_hex64("a"*64+"\n"))

    def test_malformed_json_types_fail_closed(self):
        for key in m.ENTRY_KEYS:
            for value in ([],{},None,1,True):
                reg=copy.deepcopy(self.reg);reg["entries"][0][key]=value
                with self.subTest(key=key,value=value):
                    self.assertTrue(m.check_registry(reg,BOUNDS,**self.ctx))

    def test_bound_map_case_alias_and_unsafe(self):
        for bm in ({"src/A":"c"*64,"src/a":"d"*64},{"../x":"a"*64},
                   {"src/x":"a"*64+"\n"},{}):
            reg=copy.deepcopy(self.reg);reg["entries"][0]["cohort"]["bound_files_sha256_map"]=bm
            self.assertTrue(m.check_registry(reg,bm,**self.ctx))

    def test_current_tool_pin_changes_rejected(self):
        for key in TOOLS:
            ctx=copy.deepcopy(self.ctx);ctx["current_tool_hashes"][key]="f"*64
            self.assertTrue(m.check_registry(self.reg,BOUNDS,**ctx))

    def test_duplicate_ids_and_paths(self):
        reg=copy.deepcopy(self.reg);reg["entries"].append(copy.deepcopy(reg["entries"][0]))
        self.assertTrue(m.check_registry(reg,BOUNDS,**self.ctx))

    def test_full_registry_schema_and_created_at(self):
        for key,val in (("schema","bad"),("entries",[]),("previous_registry_sha256",[])):
            reg=copy.deepcopy(self.reg);reg[key]=val
            self.assertTrue(m.check_registry(reg,BOUNDS,**self.ctx))
        reg=copy.deepcopy(self.reg);reg["entries"][0]["created_at"]="2026-10-17"
        self.assertTrue(m.check_registry(reg,BOUNDS,**self.ctx))

    def test_existing_new_target_case_and_descendant(self):
        genesis={"schema":m.SCHEMA,"entries":[],"previous_registry_sha256":None}
        reg=json.loads(self.ctx["history"])
        for p in ("REVIEWS/EXEC-NATIVE/RUN-R001","reviews/exec-native/run-r001/raw/old"):
            ctx=copy.deepcopy(self.ctx);ctx["history"]=raw(genesis);ctx["existing_paths"]=[p]
            self.assertTrue(m.check_registry(reg,BOUNDS,**ctx))

    def test_existing_container_allowed(self):
        genesis={"schema":m.SCHEMA,"entries":[],"previous_registry_sha256":None}
        reg=json.loads(self.ctx["history"]);ctx=dict(self.ctx,history=raw(genesis),
                                                  existing_paths=["reviews/exec-native"])
        self.assertEqual(m.check_registry(reg,BOUNDS,**ctx),[])

    def test_reparse_case_ancestor_or_actual_write(self):
        for rp in ("REVIEWS/EXEC-NATIVE","reviews/exec-native/run-r001/raw"):
            ctx=dict(self.ctx,reparse_paths=[rp])
            self.assertFalse(m.check_write(self.reg,"r001","raw/x",self.digest,
                                          current_bound_map=BOUNDS,**ctx)[0])

    def test_frozen_not_writable_or_current_receipt(self):
        reg=copy.deepcopy(self.reg);reg["entries"][0]["status"]="FROZEN"
        self.assertFalse(m.check_write(reg,"r001","raw/x",self.digest,
                                      current_bound_map=BOUNDS,**self.ctx)[0])

    def test_frozen_historical_pins_preserved(self):
        previous=copy.deepcopy(self.reg)
        current=copy.deepcopy(previous);current["entries"][0]["status"]="FROZEN"
        current["previous_registry_sha256"]=hashlib.sha256(raw(previous)).hexdigest()
        ctx=dict(self.ctx,history=raw(previous),
                 current_tool_hashes={k:"f"*64 for k in TOOLS})
        self.assertEqual(m.check_registry(current,{"src/new":"e"*64},**ctx),[])

    def test_actual_receipt_exact_identity(self):
        run="1"*32;receipt={"root_id":"r001","root_path":"reviews/exec-native/run-r001",
                              "run_id":run,"cohort_sha256":self.digest}
        def check(r=receipt,expected=run):
            return m.check_receipt_root(self.reg,"r001",expected,self.digest,receipt=r,
                                       current_bound_map=BOUNDS,**self.ctx)[0]
        self.assertTrue(check())
        self.assertFalse(check(None))
        self.assertFalse(check(expected="arbitrary"))
        for key in receipt:
            r=dict(receipt);r[key]="old-or-other"
            self.assertFalse(check(r))
        self.assertFalse(check(dict(receipt,extra=True)))

    def test_new_entry_must_registered(self):
        previous={"schema":m.SCHEMA,"entries":[],"previous_registry_sha256":None}
        reg=copy.deepcopy(self.reg);reg["previous_registry_sha256"]=hashlib.sha256(raw(previous)).hexdigest()
        self.assertFalse(m.HistoryChain(raw(previous)).verify_against(reg)[0])

    def test_deleted_history_and_field_changes(self):
        for key in m.ENTRY_KEYS-{"status"}:
            reg=copy.deepcopy(self.reg)
            if key=="bound_paths":reg["entries"][0][key]=["work"]
            elif key=="cohort":reg["entries"][0][key]["collector_sha256"]="f"*64
            else:reg["entries"][0][key]="changed"
            self.assertFalse(m.HistoryChain(self.ctx["history"]).verify_against(reg)[0])
        reg=copy.deepcopy(self.reg);reg["entries"]=[]
        self.assertFalse(m.HistoryChain(self.ctx["history"]).verify_against(reg)[0])

    def test_frozen_rollback_and_status_skip(self):
        previous=copy.deepcopy(self.reg);previous["entries"][0]["status"]="FROZEN"
        reg=copy.deepcopy(self.reg);reg["previous_registry_sha256"]=hashlib.sha256(raw(previous)).hexdigest()
        self.assertFalse(m.HistoryChain(raw(previous)).verify_against(reg)[0])
        reg=copy.deepcopy(self.reg);reg["entries"][0]["status"]="FROZEN"
        self.assertFalse(m.HistoryChain(self.ctx["history"]).verify_against(reg)[0])

    def test_history_exact_bytes_not_reserialized(self):
        old=self.ctx["history"];alternate=json.dumps(json.loads(old),indent=2).encode()
        self.assertFalse(m.HistoryChain(alternate).verify_against(self.reg)[0])
        self.assertTrue(m.HistoryChain(old).verify_against(self.reg)[0])

    def test_history_duplicates_malformed_and_wrong_schema(self):
        for b in (b'{"schema":1,"schema":2}',b'[]',b'{}',b'\xff',None):
            self.assertFalse(m.HistoryChain(b).verify_against(self.reg)[0])

    def test_next_registry_no_alias(self):
        chain=m.HistoryChain(self.ctx["history"])
        entries=copy.deepcopy(self.reg["entries"]);doc=chain.next_registry(entries)
        entries[0]["status"]="FROZEN"
        self.assertEqual(doc["entries"][0]["status"],"ACTIVE")

class FilesystemTests(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(exist_ok=True)
        self.base=Path(tempfile.mkdtemp(prefix="metadata-",dir=SCRATCH))
        self.store=m.JobReservation(self.base);self.c="a"*64;self.j="1"*32

    def tearDown(self):
        assert self.base.resolve().is_relative_to(SCRATCH.resolve()) and self.base!=SCRATCH
        shutil.rmtree(self.base)

    def test_reserve_duplicate_and_finalize(self):
        self.assertTrue(self.store.reserve(self.c,self.j)[0])
        self.assertEqual(self.store.inspect(self.c,self.j),"RESERVED")
        self.assertFalse(self.store.reserve(self.c,self.j)[0])
        self.assertTrue(self.store.finalize(self.c,self.j)[0])
        self.assertEqual(self.store.inspect(self.c,self.j),"FINALIZED")
        self.assertFalse(self.store.finalize(self.c,self.j)[0])
        self.assertEqual(self.store.inspect(self.c,self.j),"FINALIZED")
        self.assertFalse(self.store.reserve(self.c,self.j)[0])

    def test_pair_identity_not_global_job_name(self):
        for c,j in ((self.c,self.j),(self.c,"2"*32),("b"*64,self.j)):
            self.assertTrue(self.store.reserve(c,j)[0])

    def test_invalid_ids_no_mutation(self):
        for c,j in (("../x",self.j),(self.c,"../../escape"),(self.c,"x:ads"),("",self.j),
                    (self.c,self.j+"\n"),("a"*64+"\n",self.j)):
            self.assertFalse(self.store.reserve(c,j)[0])
            self.assertFalse(self.store.finalize(c,j)[0])
        self.assertEqual(list(self.base.iterdir()),[])

    def test_outside_relative_and_frozen_base(self):
        for p in (Path(r"D:\code"),"relative",str(self.base)+r"\..\outside",
                  P/"archives/reviews/codex-supervision/2026-10-17-root-boundary-mock-review"):
            with self.subTest(p=str(p)):
                with self.assertRaises(ValueError):m.JobReservation(p)

    def test_missing_base_not_implicitly_created(self):
        with self.assertRaises(ValueError):m.JobReservation(self.base/"missing")

    def test_crash_after_mkdir_retains_reservation(self):
        place=self.store._place(self.c,self.j);place.parent.mkdir();place.mkdir()
        self.assertEqual(self.store.inspect(self.c,self.j),"UNCERTAIN")
        self.assertFalse(self.store.reserve(self.c,self.j)[0])
        self.assertFalse(self.store.finalize(self.c,self.j)[0])

    def test_reservation_io_failure_never_retries(self):
        with patch.object(m,"write_new_json",side_effect=OSError("simulated")):
            self.assertFalse(self.store.reserve(self.c,self.j)[0])
        self.assertEqual(self.store.inspect(self.c,self.j),"UNCERTAIN")
        self.assertFalse(self.store.reserve(self.c,self.j)[0])

    def test_corrupt_and_wrong_identity_intent_rejected(self):
        self.assertTrue(self.store.reserve(self.c,self.j)[0])
        path=self.store._place(self.c,self.j)/"intent.json"
        path.write_text('{"state":"RESERVED"}')
        self.assertEqual(self.store.inspect(self.c,self.j),"UNCERTAIN")
        self.assertFalse(self.store.finalize(self.c,self.j)[0])
        self.assertEqual(path.read_text(),'{"state":"RESERVED"}')
        self.assertEqual(self.store.inspect(self.c,self.j),"UNCERTAIN")

    def test_pending_lock_no_auto_recovery(self):
        self.store.reserve(self.c,self.j)
        place=self.store._place(self.c,self.j);(place/".busy").write_text("crashed")
        self.assertEqual(self.store.inspect(self.c,self.j),"UNCERTAIN")
        self.assertFalse(self.store.finalize(self.c,self.j)[0])
        self.assertEqual((place/".busy").read_text(),"crashed")

    def test_replace_failure_preserves_uncertainty(self):
        self.store.reserve(self.c,self.j)
        with patch.object(m.os,"replace",side_effect=OSError("simulated crash")):
            self.assertFalse(self.store.finalize(self.c,self.j)[0])
        self.assertEqual(self.store.inspect(self.c,self.j),"UNCERTAIN")
        self.assertFalse(self.store.reserve(self.c,self.j)[0])

    def test_exclusive_receipt_no_overwrite(self):
        f=self.base/"receipt.json";m.write_new_json(f,{"x":1})
        original=f.read_bytes()
        with self.assertRaises(FileExistsError):m.write_new_json(f,{"x":2})
        self.assertEqual(f.read_bytes(),original)

    def test_reparse_fact_rejected_locally(self):
        original=Path.lstat
        def fake(p,*args,**kw):
            st=original(p,*args,**kw)
            if p==self.base:
                from types import SimpleNamespace
                return SimpleNamespace(st_file_attributes=0x400,st_mode=st.st_mode)
            return st
        with patch.object(Path,"lstat",fake):
            with self.assertRaises(ValueError):m.JobReservation(self.base)

    def test_same_pair_concurrent_threads_one_winner(self):
        with ThreadPoolExecutor(max_workers=8) as pool:
            results=list(pool.map(lambda _:self.store.reserve(self.c,self.j)[0],range(16)))
        self.assertEqual(sum(results),1)

    def test_same_pair_concurrent_processes_one_winner(self):
        commands=[[sys.executable,"-X","utf8","-B",str(Path(__file__).absolute()),
                   "--reserve-worker",str(self.base),self.c,self.j] for _ in range(6)]
        children=[subprocess.Popen(c,stdout=subprocess.PIPE,stderr=subprocess.PIPE) for c in commands]
        outputs=[p.communicate(timeout=30) for p in children]
        self.assertEqual(sorted(p.returncode for p in children),[0,2,2,2,2,2],
                         [(p.returncode,o) for p,o in zip(children,outputs)])
        self.assertEqual(self.store.inspect(self.c,self.j),"RESERVED")

    def test_finalize_concurrency_only_one_transition(self):
        self.store.reserve(self.c,self.j)
        with ThreadPoolExecutor(max_workers=4) as pool:
            results=list(pool.map(lambda _:self.store.finalize(self.c,self.j)[0],range(4)))
        self.assertEqual(sum(results),1)
        self.assertIn(self.store.inspect(self.c,self.j),("FINALIZED","UNCERTAIN"))

if __name__=="__main__":
    if len(sys.argv)>1 and sys.argv[1]=="--reserve-worker":
        sys.exit(0 if m.JobReservation(Path(sys.argv[2])).reserve(sys.argv[3],sys.argv[4])[0] else 2)
    unittest.main(verbosity=2)
