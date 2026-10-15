"""Adversarial binding/coverage checks; signature descriptors do not prove semantics."""
import contextlib,copy,hashlib,importlib.util,io,json,tempfile,unittest
from pathlib import Path
from unittest import mock
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("core_signatures_tested",ROOT/"tools/core_signatures.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class CoreSignaturesTests(unittest.TestCase):
    def setUp(self):
        self.owner=ROOT/"reviews/codex-supervision/2026-10-07-semantic-signature-supervision"
        self.temp=tempfile.TemporaryDirectory(prefix="signature-test-",dir=self.owner)
        self.root=Path(self.temp.name).resolve();self.assertTrue(self.root.is_relative_to(self.owner.resolve()))
        self.core=self.root/"reviews/current-core";self.sigdir=self.root/"reviews/signatures"
        self.core.mkdir(parents=True);self.sigdir.mkdir()
        self.patches=[mock.patch.object(m,"ROOT",self.root),mock.patch.object(m,"CORE",self.core),mock.patch.object(m,"SIG_DIR",self.sigdir)]
        for p in self.patches:p.start()
        self.refs=[];self.sources=[]
        for group,nparts in (("train",4),("selected_draft",18),("eval",1),("test",1)):
            size=m.EXPECTED_GROUPS[group];offset=0
            for part in range(nparts):
                count=size//nparts+(part<size%nparts)
                records=[{"id":group+"-"+str(offset+i),"problem":"A bound test task","solution":"Exact proof","answer":"1","scene_spec":{"objects":[],"steps":[]}} for i in range(count)]
                offset+=count
                path=self.core/"candidate-sources"/group/(str(part)+".jsonl");path.parent.mkdir(parents=True,exist_ok=True)
                raw=("".join(json.dumps(r)+"\n" for r in records)).encode();path.write_bytes(raw)
                relative=path.relative_to(self.root).as_posix()
                self.sources.append({"path":relative,"sha256":m.digest(raw),"bytes":len(raw),"records":count,"group":group})
                for line,r in enumerate(records,1):
                    self.refs.append({"id":r["id"],"group":group,"path":relative,"source_line":line,"source_sha256":m.digest(raw),"record_sha256":m.dense(r),"math_sha256":m.math_digest(r)})
        self.seal()
    def tearDown(self):
        for p in reversed(self.patches):p.stop()
        self.assertTrue(self.root.is_relative_to(self.owner.resolve()));self.temp.cleanup()
    def seal(self):
        raw=("".join(json.dumps(r)+"\n" for r in self.refs)).encode()
        source_raw=json.dumps(self.sources).encode()
        (self.core/"record-bindings.jsonl").write_bytes(raw);(self.core/"source-bindings.json").write_bytes(source_raw)
        (self.core/"current-index.json").write_text(json.dumps({"record_bindings_sha256":m.digest(raw),"source_bindings_sha256":m.digest(source_raw),"groups":m.EXPECTED_GROUPS}),encoding="utf8")
        artifacts=[]
        for p in sorted(self.core.rglob("*")):
            if p.is_file() and p.name!="delivery-manifest.json":
                b=p.read_bytes();artifacts.append({"path":p.relative_to(self.core).as_posix(),"sha256":m.digest(b),"bytes":len(b)})
        manifest=json.dumps({"artifacts":artifacts}).encode();(self.core/"delivery-manifest.json").write_bytes(manifest)
        m.CORE_MANIFEST_SHA256=m.digest(manifest)
    def signature(self,rid):
        ref=next(r for r in self.refs if r["id"]==rid)
        return {k:ref[k] for k in ("id","group","record_sha256","math_sha256")}|{"goal":"solve "+rid,"domain":"real variables","key_conditions":["defined domain"],"decisive_steps":["derive relation","exact solution"]}
    def input(self,name,rows):
        p=self.sigdir/(name+"-signatures.jsonl");p.write_text("".join(json.dumps(r)+"\n" for r in rows),encoding="utf8");return p
    def run_bundle(self,rows):
        p=self.input("unit",rows)
        with contextlib.redirect_stdout(io.StringIO()):return m.bundle("unit",p,self.sigdir/"out")
    def test_actual_761_records_and_24_sources_are_checked(self):
        rows=m.load_record_bindings();self.assertEqual(len(rows),761);self.assertEqual(len(self.sources),24)
    def test_bundle_valid_subset_is_packaging_only(self):
        self.assertEqual(self.run_bundle([self.signature("train-0")]),0)
        r=json.loads((self.sigdir/"out/receipt.json").read_text())
        self.assertEqual(r["semantic_content"],"PENDING_INDEPENDENT_REVIEW")
        self.assertEqual(r["semantic_isolation"],"NOT_ESTABLISHED");self.assertFalse(r["PASS_CORE_SCOPE_issued"])
    def test_stale_actual_source_rejects_even_unselected_row(self):
        p=self.root/self.refs[0]["path"];lines=p.read_bytes().splitlines(keepends=True)
        r=json.loads(lines[-1]);r["answer"]="2";lines[-1]=(json.dumps(r)+"\n").encode();p.write_bytes(b"".join(lines))
        with self.assertRaises(ValueError):self.run_bundle([self.signature("train-0")])
    def test_frozen_record_binding_file_tampering_rejected(self):
        p=self.core/"record-bindings.jsonl";p.write_bytes(p.read_bytes()+b"\n")
        with self.assertRaises(ValueError):m.load_record_bindings()
    def test_frozen_manifest_tampering_rejected(self):
        p=self.core/"delivery-manifest.json";p.write_bytes(p.read_bytes()+b"\n")
        with self.assertRaises(ValueError):m.load_record_bindings()
    def test_mathematical_hash_is_recomputed_not_trusted(self):
        self.refs[0]["math_sha256"]="0"*64;self.seal()
        with self.assertRaises(ValueError):m.load_record_bindings()
    def test_record_hash_is_recomputed_not_trusted(self):
        self.refs[0]["record_sha256"]="0"*64;self.seal()
        with self.assertRaises(ValueError):m.load_record_bindings()
    def test_boolean_or_zero_line_rejected(self):
        for value in (True,0):
            self.refs[0]["source_line"]=value;self.seal()
            with self.subTest(value=value),self.assertRaises(ValueError):m.load_record_bindings()
    def test_duplicate_core_ids_rejected(self):
        self.refs[1]["id"]=self.refs[0]["id"];self.seal()
        with self.assertRaises(ValueError):m.load_record_bindings()
    def test_core_population_760_rejected(self):
        self.refs.pop();self.seal()
        with self.assertRaises(ValueError):m.load_record_bindings()
    def test_empty_input_rejected_before_output(self):
        with self.assertRaises(ValueError):self.run_bundle([])
        self.assertFalse((self.sigdir/"out").exists())
    def test_goal_and_domain_must_be_nonempty_strings(self):
        for field in ("goal","domain"):
            for value in ([],["not a string"],"   "):
                r=self.signature("train-0");r[field]=value
                with self.subTest(field=field,value=value),self.assertRaises(ValueError):
                    m.validate_signature(r,{x["id"]:x for x in self.refs})
    def test_step_and_condition_strings_cannot_be_sorted_as_characters(self):
        for field in ("decisive_steps","key_conditions"):
            for value in ("characters",[],[" "],[1],[{}]):
                r=self.signature("train-0");r[field]=value
                with self.subTest(field=field,value=value),self.assertRaises(ValueError):
                    m.validate_signature(r,{x["id"]:x for x in self.refs})
    def test_stale_signature_hashes_rejected(self):
        for field in ("record_sha256","math_sha256"):
            r=self.signature("train-0");r[field]="0"*64
            with self.subTest(field=field),self.assertRaises(ValueError):self.run_bundle([r])
    def test_signature_group_mismatch_rejected(self):
        r=self.signature("train-0");r["group"]="eval"
        with self.assertRaises(ValueError):self.run_bundle([r])
    def test_unknown_signature_identity_rejected(self):
        r=self.signature("train-0");r["id"]="unknown"
        with self.assertRaises(ValueError):self.run_bundle([r])
    def test_duplicate_ids_across_inputs_rejected(self):
        r=self.signature("train-0");p=self.input("a",[r]);q=self.input("b",[r])
        with self.assertRaises(ValueError):m.cross_match([p,q],self.sigdir/"match",True)
    def test_incomplete_default_never_returns_zero_candidate_success(self):
        p=self.input("partial",[self.signature("train-0")])
        with self.assertRaises(ValueError):m.cross_match([p],self.sigdir/"match")
        self.assertFalse((self.sigdir/"match").exists())
    def test_explicit_partial_records_missing_ids_and_nonzero_exit(self):
        a=self.signature("train-0");b=self.signature("eval-0");b["goal"]=a["goal"]
        p=self.input("partial",[a,b])
        with contextlib.redirect_stdout(io.StringIO()):rc=m.cross_match([p],self.sigdir/"match",True)
        r=json.loads((self.sigdir/"match/cross-candidates.json").read_text())
        self.assertEqual(rc,3);self.assertEqual(r["signature_coverage"],"INCOMPLETE")
        self.assertEqual(len(r["missing_ids"]),759);self.assertEqual(len(r["candidates"]),1)
        self.assertEqual(r["candidates"][0]["disposition"],"UNREVIEWED")
        self.assertFalse(r["candidate_generation_exhaustive"])
    def test_complete_761_only_generates_unreviewed_candidates(self):
        sigs=[self.signature(r["id"]) for r in self.refs];sigs[0]["goal"]="shared";sigs[311]["goal"]="shared"
        p=self.input("complete",sigs)
        with contextlib.redirect_stdout(io.StringIO()):rc=m.cross_match([p],self.sigdir/"match")
        r=json.loads((self.sigdir/"match/cross-candidates.json").read_text())
        self.assertEqual(rc,0);self.assertEqual(r["train_side"],311);self.assertEqual(r["eval_side"],450)
        self.assertEqual(r["signature_coverage"],"COMPLETE");self.assertEqual(len(r["candidates"]),1)
        self.assertEqual(r["semantic_isolation"],"NOT_ESTABLISHED");self.assertFalse(r["PASS_CORE_SCOPE_issued"])
    def test_zero_literal_candidates_never_certifies_semantics(self):
        sigs=[self.signature(r["id"]) for r in self.refs];p=self.input("complete",sigs)
        with contextlib.redirect_stdout(io.StringIO()):m.cross_match([p],self.sigdir/"match")
        r=json.loads((self.sigdir/"match/cross-candidates.json").read_text())
        self.assertEqual(r["candidates"],[]);self.assertEqual(r["semantic_isolation"],"NOT_ESTABLISHED")
    def test_existing_bundle_is_never_overwritten(self):
        p=self.input("a",[self.signature("train-0")])
        with contextlib.redirect_stdout(io.StringIO()):m.bundle("a",p,self.sigdir/"out")
        before=(self.sigdir/"out/receipt.json").read_bytes()
        with self.assertRaises(FileExistsError):m.bundle("a",p,self.sigdir/"out")
        self.assertEqual(before,(self.sigdir/"out/receipt.json").read_bytes())
    def test_output_cannot_write_into_frozen_core(self):
        p=self.input("a",[self.signature("train-0")])
        with self.assertRaises(ValueError):m.bundle("a",p,self.core/"new")
    def test_output_cannot_escape_project_reviews(self):
        p=self.input("a",[self.signature("train-0")])
        with self.assertRaises(ValueError):m.bundle("a",p,self.root/"tools")
    def test_partial_cli_reports_failure_or_explicit_incomplete(self):
        p=self.input("partial",[self.signature("train-0")])
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(m.main(["cross-match","--input",str(p),"--out",str(self.sigdir/"out")]),2)
            self.assertEqual(m.main(["cross-match","--input",str(p),"--out",str(self.sigdir/"out"),"--allow-partial"]),3)
    def test_input_paths_with_traversal_are_rejected(self):
        with self.assertRaises(ValueError):m.checked_path(self.root/"reviews/../escape",self.root)
if __name__=="__main__":unittest.main()
