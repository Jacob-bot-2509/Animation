"""Independent adversarial checks. No root registry is installed and no native cases run."""
import contextlib, copy, hashlib, importlib.util, io, json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("candidate_model",HERE/"mock_root_boundary_checker.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.reg,self.bounds,self.ctx=m.fixture(True)
    def reject(self,reg=None,**kw):
        self.assertTrue(m.check_registry(self.reg if reg is None else reg,self.bounds,**{**self.ctx,**kw}))
    def write(self,path,**kw):
        return m.check_write(self.reg,"n001",path,current_bound_map=self.bounds,**{**self.ctx,**kw})
    def test_valid_baseline(self):
        self.assertEqual(m.check_registry(self.reg,self.bounds,**self.ctx),[])
        self.assertTrue(self.write("raw/output.json"))
    def test_empty_missing_or_wrong_entries_rejected(self):
        for rows in ([],None,{},True):
            bad=copy.deepcopy(self.reg);bad["entries"]=rows;self.reject(bad)
        bad=copy.deepcopy(self.reg);del bad["entries"];self.reject(bad)
    def test_malformed_nested_objects_fail_closed(self):
        for row in (None,True,[],{"root_id":"n001"}):
            bad=copy.deepcopy(self.reg);bad["entries"]=[row];self.reject(bad)
        for field,value in (("purpose",[]),("status",[]),("cohort",None),("bound_paths",True),("created_at",0)):
            bad=copy.deepcopy(self.reg);bad["entries"][0][field]=value;self.reject(bad)
    def test_root_escape_and_absolute_variants_rejected(self):
        for path in ("reviews/exec-native/../../old","reviews/exec-native/run-n001/../x",
                     "reviews/exec-native/./run-n001","C:/x","/reviews/exec-native/run-n001",
                     r"reviews\exec-native\run-n001","reviews/exec-nativeevil/run-n001",
                     "reviews/exec-native/run-n001.","reviews/exec-native/run-n001:ads"):
            bad=copy.deepcopy(self.reg);bad["entries"][0]["root_path"]=path;self.reject(bad)
    def test_closed_bound_paths(self):
        for bp in ([],["*"],[".."],["C:/evil"],[r"C:\evil"],["raw/child"],["raw","raw"],["raw",True],["other"]):
            bad=copy.deepcopy(self.reg);bad["entries"][0]["bound_paths"]=bp;self.reject(bad)
    def test_invalid_sha_and_changed_tool_pin_rejected(self):
        for name in ("collector_sha256","verifier_sha256"):
            for value in ("invalid","A"*64,True,"d"*64):
                bad=copy.deepcopy(self.reg);bad["entries"][0]["cohort"][name]=value;self.reject(bad)
    def test_binding_map_exact_and_well_typed(self):
        for value in ({},{"src/mock.py":"v"},{"src/mock.py":True},{"src/mock.py":"d"*64},
                      {"src/mock.py":"c"*64,"SRC/MOCK.PY":"c"*64},{"../x":"c"*64}):
            bad=copy.deepcopy(self.reg);bad["entries"][0]["cohort"]["bound_files_sha256_map"]=value;self.reject(bad)
    def test_context_is_required(self):
        self.assertTrue(m.check_registry(self.reg,self.bounds))
        self.reject(history=None);self.reject(current_tool_hashes=None)
    def test_registry_self_declared_pin_cannot_change_trusted_context(self):
        bad=copy.deepcopy(self.reg);bad["entries"][0]["cohort"]["bound_files_sha256_map"]={"src/fake.py":"f"*64}
        self.reject(bad)
    def test_unregistered_id_and_unregistered_receipt_root(self):
        self.assertFalse(m.check_write(self.reg,"missing","raw/x",current_bound_map=self.bounds,**self.ctx))
        receipt=self.receipt()
        self.assertFalse(m.check_old_receipt_as_new(self.reg,"reviews/exec-native/never-registered",
            root_id="n001",expected_run_id="1"*32,receipt=receipt,current_bound_map=self.bounds,**self.ctx))
    def receipt(self):
        e=self.reg["entries"][0]
        return {"root_id":"n001","root_path":e["root_path"],"run_id":"1"*32,"cohort_sha256":m.sha_object(e["cohort"])}
    def test_receipt_root_run_and_cohort_binding(self):
        good=self.receipt()
        def accepts(p,r):return m.check_old_receipt_as_new(self.reg,p,root_id="n001",expected_run_id="1"*32,receipt=r,current_bound_map=self.bounds,**self.ctx)
        self.assertTrue(accepts(good["root_path"],good))
        for key,value in (("root_id","n999"),("run_id","2"*32),("cohort_sha256","0"*64),("root_path","reviews/elsewhere")):
            bad=dict(good);bad[key]=value;self.assertFalse(accepts(good["root_path"],bad))
        self.assertFalse(accepts(next(iter(m.OLD_ROOTS)),good))
    def test_write_rejects_windows_escape_aliases(self):
        paths=("../evil","raw/../evil","/evil","C:/evil",r"raw\..\evil","raw/x:ads",
               "raw/NUL.txt","raw/CON","raw/x.","raw/x ","raw//x","raw/./x","raw/*","raw",
               r"\\server\share","//server/share/x")
        for p in paths:self.assertFalse(self.write(p),p)
    def test_parent_and_child_evidence_separation(self):
        self.assertFalse(self.write("raw/proof.json",writer="child"))
        self.assertTrue(self.write("work/output.txt",writer="child"))
        self.assertFalse(self.write("raw/x",writer="unknown"))
    def test_registered_and_frozen_roots_cannot_write(self):
        reg,bounds,ctx=m.fixture()
        self.assertFalse(m.check_write(reg,"n001","raw/x",current_bound_map=bounds,**ctx))
        history=copy.deepcopy(self.reg);frozen=copy.deepcopy(history)
        frozen["previous_registry_sha256"]=m.sha_object(history);frozen["entries"][0]["status"]="FROZEN"
        fctx={**self.ctx,"history":history}
        self.assertEqual(m.check_registry(frozen,self.bounds,**fctx),[])
        self.assertFalse(m.check_write(frozen,"n001","raw/x",current_bound_map=self.bounds,**fctx))
    def test_existing_directory_conflict_and_container(self):
        reg,bounds,ctx=m.fixture()
        for p in ("reviews/exec-native/run-n001","REVIEWS/EXEC-NATIVE/RUN-N001","reviews/exec-native/run-n001/child"):
            self.assertTrue(m.check_registry(reg,bounds,**{**ctx,"existing_paths":(p,)}))
        self.assertEqual(m.check_registry(reg,bounds,**{**ctx,"existing_paths":("reviews","reviews/exec-native")}),[])
    def test_mock_reparse_facts_enforced_for_root_and_child(self):
        for p in ("reviews","reviews/exec-native","reviews/exec-native/run-n001"):
            self.reject(reparse_paths=(p,))
        self.assertFalse(self.write("work/link/file",reparse_paths=("reviews/exec-native/run-n001/work/link",)))
    def test_duplicate_ids_or_same_path_rejected(self):
        for rid in ("n001","n002"):
            bad=copy.deepcopy(self.reg);e=copy.deepcopy(bad["entries"][0]);e["root_id"]=rid;bad["entries"].append(e);self.reject(bad)
    def test_history_deletion_detected(self):
        history=copy.deepcopy(self.ctx["history"]);e=copy.deepcopy(history["entries"][0])
        e["root_id"]="n002";e["root_path"]="reviews/exec-native/run-n002";history["entries"].append(e)
        bad=copy.deepcopy(self.reg);bad["previous_registry_sha256"]=m.sha_object(history)
        self.reject(bad,history=history)
    def test_history_changes_rejected(self):
        for field,value in (("purpose","joint"),("created_at","2026-02-01T00:00:00+00:00"),("bound_paths",["raw"])):
            bad=copy.deepcopy(self.reg);bad["entries"][0][field]=value;self.reject(bad)
    def test_history_hash_mismatch_and_status_rollback(self):
        bad=copy.deepcopy(self.reg);bad["previous_registry_sha256"]="0"*64;self.reject(bad)
        history=copy.deepcopy(self.reg);history["entries"][0]["status"]="FROZEN"
        bad=copy.deepcopy(self.reg);bad["previous_registry_sha256"]=m.sha_object(history)
        self.reject(bad,history=history)
    def test_new_active_root_not_self_approved(self):
        reg,bounds,ctx=m.fixture();reg["entries"][0]["status"]="ACTIVE"
        self.assertTrue(m.check_registry(reg,bounds,**ctx))
    def test_frozen_old_cohort_retained_without_resigning(self):
        history=copy.deepcopy(self.reg);history["entries"][0]["status"]="FROZEN"
        new=copy.deepcopy(history);new["previous_registry_sha256"]=m.sha_object(history)
        row=copy.deepcopy(new["entries"][0]);row.update(root_id="n002",root_path="reviews/exec-native/run-n002",status="REGISTERED")
        newbounds={"src/new.py":"d"*64};row["cohort"]["bound_files_sha256_map"]=newbounds;new["entries"].append(row)
        self.assertEqual(m.check_registry(new,newbounds,**{**self.ctx,"history":history}),[])
        self.assertEqual(new["entries"][0]["cohort"]["bound_files_sha256_map"],self.bounds)
    def test_job_reuse_is_per_job_not_per_cohort(self):
        used=set();cohort="a"*64
        self.assertTrue(m.check_reuse(used,cohort,"1"*32))
        self.assertFalse(m.check_reuse(used,cohort,"1"*32))
        self.assertTrue(m.check_reuse(used,cohort,"2"*32))
        self.assertEqual(len(used),2)
    def test_invalid_job_reservations_fail_closed(self):
        for cohort,job in (("bad","1"*32),("a"*64,None),("a"*64,True),("a"*64,"bad")):
            used=set();self.assertFalse(m.check_reuse(used,cohort,job));self.assertEqual(used,set())
    def test_corrupt_reservation_set_not_reused(self):
        used={"corrupt"};self.assertFalse(m.check_reuse(used,"a"*64,"1"*32));self.assertEqual(used,{"corrupt"})
    def test_cli_ads_output_rejected(self):
        p=HERE/"forbidden.json:stream"
        with patch("sys.argv",["mock","--receipt",str(p)]),self.assertRaises(ValueError),contextlib.redirect_stdout(io.StringIO()):
            m.main()
        self.assertFalse(p.exists())
    def test_cli_failure_returns_nonzero_without_native_work(self):
        with patch.object(m,"fixture_matrix",return_value=[{"name":"forced-failure","ok":False}]),patch("sys.argv",["mock"]),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(m.main(),1)
    def test_receipt_no_overwrite_and_frozen_output_rejected(self):
        tmp=tempfile.TemporaryDirectory(prefix="model-test-",dir=HERE);p=Path(tmp.name)
        assert p.resolve().is_relative_to(HERE.resolve())
        try:
            receipt=p/"receipt.json"
            with patch("sys.argv",["mock","--receipt",str(receipt)]),contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(m.main(),0)
            prior=receipt.read_bytes()
            with patch("sys.argv",["mock","--receipt",str(receipt)]),self.assertRaises(FileExistsError),contextlib.redirect_stdout(io.StringIO()):
                m.main()
            self.assertEqual(receipt.read_bytes(),prior)
            (p/"delivery-manifest.json").write_text("{}",encoding="utf-8")
            with patch("sys.argv",["mock","--receipt",str(p/"new.json")]),self.assertRaises(ValueError),contextlib.redirect_stdout(io.StringIO()):
                m.main()
        finally:
            assert p.resolve().is_relative_to(HERE.resolve());tmp.cleanup()

if __name__=="__main__":unittest.main(verbosity=2)
