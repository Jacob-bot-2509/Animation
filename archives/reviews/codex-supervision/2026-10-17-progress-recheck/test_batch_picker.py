
"""Independent selection/binding checks; only project-owned temporary data."""
import copy,hashlib,importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
P=Path(r"D:\Animation-Model-Training")
FILE=P/"reviews/data-prep/2026-10-17-submission/asset-evidence/pick_first_batch_10.py"
s=importlib.util.spec_from_file_location("picker",FILE);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
SCRATCH=P/"reviews/codex-supervision/2026-10-17-batch-selection-test-runtime"

class BindingTests(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(exist_ok=True);self.root=Path(tempfile.mkdtemp(dir=SCRATCH,prefix="binding-"))
        (self.root/"data").mkdir();self.file=self.root/"data/examples.jsonl"
        self.record={"id":"example-s1","problem_id":"example","problem":"x","answer":"1/3"}
        self.file.write_bytes(json.dumps(self.record).encode()+b"\r\n")
        self.ev={"source":{"path":str(self.file),"line":1,"sha256":m.sha(self.file.read_bytes())},
                 "input_sha256":"a"*64,"errors":[m.LABELS["A"]],"warnings":[m.LABELS["E"]]}

    def tearDown(self):
        assert self.root.resolve().is_relative_to(SCRATCH.resolve()) and self.root!=SCRATCH
        shutil.rmtree(self.root)

    def bind(self,sid="example-s1",ev=None):
        return m.bind_record(sid,self.ev if ev is None else ev,root=self.root)

    def test_exact_raw_line_binding_and_pending_status(self):
        row=self.bind()
        self.assertEqual(row["source"]["raw_line_sha256"],m.sha(self.file.read_bytes()))
        self.assertEqual(row["source"]["canonical_record_sha256"],m.sha(m.encoded(self.record)))
        self.assertEqual(row["family_key"],"example")
        for k in ("math_review","semantic_review","render_review"):self.assertEqual(row[k],"PENDING")

    def test_explicit_problem_id_precedes_suffix(self):
        self.record["problem_id"]="real-family";self.file.write_bytes(json.dumps(self.record).encode()+b"\n")
        self.ev["source"]["sha256"]=m.sha(self.file.read_bytes())
        self.assertEqual(self.bind()["family_key"],"real-family")

    def test_suffix_rule_really_removes_number(self):
        self.record.pop("problem_id");self.file.write_bytes(json.dumps(self.record).encode()+b"\n")
        self.ev["source"]["sha256"]=m.sha(self.file.read_bytes())
        self.assertEqual(self.bind()["family_key"],"example")

    def test_source_file_change_rejected(self):
        self.file.write_bytes(self.file.read_bytes()+b" ")
        with self.assertRaises(ValueError):self.bind()

    def test_wrong_source_record_id_rejected(self):
        with self.assertRaises(ValueError):self.bind("different")

    def test_line_index_bool_zero_and_missing_rejected(self):
        for x in (True,0,-1,2,None,"1"):
            ev=copy.deepcopy(self.ev);ev["source"]["line"]=x
            with self.subTest(x=x):
                with self.assertRaises(ValueError):self.bind(ev=ev)

    def test_path_traversal_ads_outside_and_non_dataset_rejected(self):
        for path in (str(self.file)+":ads",str(self.root)+r"\data\..\outside.jsonl",
                     r"D:\code\example.jsonl",str(self.root/"other.jsonl")):
            ev=copy.deepcopy(self.ev);ev["source"]["path"]=path
            with self.subTest(path=path):
                with self.assertRaises(ValueError):self.bind(ev=ev)

    def test_stale_unrelated_rows_quarantined_not_rebound(self):
        stale=copy.deepcopy(self.ev);stale["source"]["sha256"]="f"*64
        rows,rejected,cache=m.bind_candidates({"example-s1":self.ev,"stale-s1":stale},root=self.root)
        self.assertEqual([r["sample_id"] for r in rows],["example-s1"])
        self.assertEqual(rejected,[{"sample_id":"stale-s1","reason":"source_file_sha_mismatch","status":"QUARANTINED_NOT_ELIGIBLE"}])

    def test_malformed_label_and_claim_rejected(self):
        for field,value in (("errors","A"),("warnings",[{}]),("input_sha256","a"*64+"\n")):
            ev=copy.deepcopy(self.ev);ev[field]=value
            with self.assertRaises(ValueError):self.bind(ev=ev)

class SelectionTests(unittest.TestCase):
    def rows(self):
        rows=[]
        for i in range(12):
            rows.append({"sample_id":"p"+str(i),"family_key":"family"+str(i),
                         "tags":["A"] if i else sorted(m.REQUIRED),"errors":[]})
        return rows

    def test_exact_size_full_coverage_deterministic(self):
        a,c=m.choose(self.rows());b,d=m.choose(list(reversed(self.rows())))
        self.assertEqual(len(a),10);self.assertEqual(c,sorted(m.REQUIRED));self.assertEqual(a,b)

    def test_same_family_variants_take_one_slot(self):
        rows=self.rows();clone=copy.deepcopy(rows[0]);clone["sample_id"]="p0-s2";rows.append(clone)
        chosen,_=m.choose(rows)
        self.assertEqual(len({r["family_key"] for r in chosen}),10)

    def test_coverage_phase_also_obeys_family_uniqueness(self):
        rows=[{"sample_id":"p-s1","family_key":"p","tags":list("ABEFG"),"errors":[]},
              {"sample_id":"p-s2","family_key":"p","tags":list("ACDG"),"errors":[]},
              {"sample_id":"q","family_key":"q","tags":list("CDEG"),"errors":[]}]
        rows += [{"sample_id":"other-"+str(i),"family_key":"other-"+str(i),"tags":["A"],"errors":[]} for i in range(12)]
        selected,covered=m.choose(rows)
        self.assertEqual(len({r["family_key"] for r in selected}),10)
        self.assertEqual(covered,sorted(m.REQUIRED))

    def test_coverage_recomputed_after_fill(self):
        chosen,covered=m.choose(self.rows())
        self.assertEqual(covered,sorted(set().union(*(set(r["tags"]) for r in chosen))))

    def test_uncovered_tag_rejected_even_with_ten_rows(self):
        rows=self.rows()
        for r in rows:r["tags"]=["A"]
        with self.assertRaises(ValueError):m.choose(rows)

    def test_insufficient_families_rejected(self):
        rows=self.rows()
        for r in rows:r["family_key"]="same"
        with self.assertRaises(ValueError):m.choose(rows)

    def test_duplicate_ids_and_invalid_count_rejected(self):
        rows=self.rows();rows.append(copy.deepcopy(rows[0]))
        with self.assertRaises(ValueError):m.choose(rows)
        for n in (True,0,"10"):
            with self.assertRaises(ValueError):m.choose(self.rows(),n)

    def test_unknown_tags_rejected(self):
        rows=self.rows();rows[0]["tags"].append("UNKNOWN")
        with self.assertRaises(ValueError):m.choose(rows)

if __name__=="__main__":unittest.main(verbosity=2)
