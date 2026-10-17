"""Independent project-owned metadata fixtures; no approvals or native execution."""
import copy,hashlib,json,shutil,tempfile,unittest,uuid
from pathlib import Path
from unittest.mock import patch
import build_diversity_bindings as m
SCRATCH=m.ROOT/"reviews/codex-supervision/2026-10-17-template-diversity-test-runtime"

class DiversityTests(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(exist_ok=True);self.root=Path(tempfile.mkdtemp(dir=SCRATCH,prefix="binding-"))
        (self.root/"data/v2/train").mkdir(parents=True);(self.root/"configs").mkdir();(self.root/"out").mkdir()
        self.file=self.root/"data/v2/train/examples.jsonl"
        self.file.write_bytes(b'{"id":"first","answer":"1/3"}\r\n\n{"id":"second","answer":"2/3"}\n')
        self.policy={"concepts":[{"id":"C01"}]};(self.root/"configs/training_diversity_policy.json").write_text(json.dumps(self.policy))
        self.manifest={"entries":[{"split":"train","path":r"v2\train\examples.jsonl",
            "sha256":m.sha_bytes(self.file.read_bytes()),"size":self.file.stat().st_size}]}
        self.save()

    def save(self):
        (self.root/"data/manifest.json").write_text(json.dumps(self.manifest))
    def collect(self):return m.collect(self.root)
    def out(self):return self.root/"out"/("generation-"+uuid.uuid4().hex)
    def write(self,out,files,cap):return m.write_generation(out,files,cap,project=self.root,approved_parent=self.root/"out")
    def tearDown(self):
        assert self.root.resolve().is_relative_to(SCRATCH.resolve()) and self.root!=SCRATCH
        shutil.rmtree(self.root)

    def test_raw_lines_and_source_file_bound(self):
        files,_=self.collect();rows=[json.loads(x) for x in files["row-bindings.jsonl"].splitlines()]
        raw=self.file.read_bytes().splitlines(keepends=True)
        self.assertEqual([r["line_no"] for r in rows],[1,3])
        self.assertEqual(rows[0]["raw_line_sha256"],m.sha_bytes(raw[0]))
        self.assertEqual(rows[0]["source_file_sha256"],m.sha_bytes(self.file.read_bytes()))
        self.assertEqual(rows[0]["project_source_path"],"data/v2/train/examples.jsonl")

    def test_no_review_approval_fabricated(self):
        files,_=self.collect();t=json.loads(files["template.json"])
        self.assertEqual(t["actual_train_ids_total"],2)
        for r in t["record_reviews"]:
            for k in ("concept_id","variant_kind","user_review","math_review","diversity_review","leakage_review"):
                self.assertIsNone(r[k])
            self.assertEqual(r["review_state"],"PENDING")

    def test_stale_source_sha_rejected(self):
        self.manifest["entries"][0]["sha256"]="f"*64;self.save()
        with self.assertRaises(ValueError):self.collect()

    def test_wrong_size_and_bool_rejected(self):
        for n in (0,True):
            self.manifest["entries"][0]["size"]=n;self.save()
            with self.assertRaises(ValueError):self.collect()

    def test_duplicate_ids_fail_even_with_correct_file_sha(self):
        raw=b'{"id":"same"}\n{"id":"same"}\n';self.file.write_bytes(raw)
        self.manifest["entries"][0].update(sha256=m.sha_bytes(raw),size=len(raw));self.save()
        with self.assertRaises(ValueError):self.collect()

    def test_missing_or_conflicting_ids_fail(self):
        for raw in (b'{"answer":"1"}\n',b'{"id":"one","sample_id":"two"}\n',b'[]\n'):
            self.file.write_bytes(raw);self.manifest["entries"][0].update(sha256=m.sha_bytes(raw),size=len(raw));self.save()
            with self.assertRaises(ValueError):self.collect()

    def test_parse_error_not_success_with_pending_subset(self):
        raw=b'{"id":"one"}\nBAD\n';self.file.write_bytes(raw)
        self.manifest["entries"][0].update(sha256=m.sha_bytes(raw),size=len(raw));self.save()
        with self.assertRaises(ValueError):self.collect()

    def test_duplicate_json_keys_fail(self):
        raw=b'{"id":"first","id":"second"}\n';self.file.write_bytes(raw)
        self.manifest["entries"][0].update(sha256=m.sha_bytes(raw),size=len(raw));self.save()
        with self.assertRaises(ValueError):self.collect()

    def test_manifest_traversal_ads_and_wrong_split_path(self):
        for path in ("../outside.jsonl","v2/train/../x.jsonl","v2/train/x:ads",
                     "v2/test/examples.jsonl",r"v2\train/examples.jsonl"):
            self.manifest["entries"][0]["path"]=path;self.save()
            with self.assertRaises(ValueError):self.collect()

    def test_duplicate_paths_fail(self):
        self.manifest["entries"].append(copy.deepcopy(self.manifest["entries"][0]));self.save()
        with self.assertRaises(ValueError):self.collect()

    def test_empty_training_set_fail(self):
        self.manifest["entries"][0]["split"]="eval";self.save()
        with self.assertRaises(ValueError):self.collect()

    def test_policy_duplicate_ids_fail(self):
        self.policy["concepts"].append({"id":"C01"})
        (self.root/"configs/training_diversity_policy.json").write_text(json.dumps(self.policy))
        with self.assertRaises(ValueError):self.collect()

    def test_exclusive_generation_with_complete_last(self):
        files,cap=self.collect();out=self.out();receipt=self.write(out,files,cap)
        self.assertTrue((out/"COMPLETE.json").exists())
        for row in receipt["artifacts"]:
            self.assertEqual(m.sha_bytes((out/row["path"]).read_bytes()),row["sha256"])
        original=(out/"COMPLETE.json").read_bytes()
        with self.assertRaises(FileExistsError):self.write(out,files,cap)
        self.assertEqual((out/"COMPLETE.json").read_bytes(),original)

    def test_input_change_before_write_no_output(self):
        files,cap=self.collect();self.file.write_bytes(self.file.read_bytes()+b" ");out=self.out()
        with self.assertRaises(ValueError):self.write(out,files,cap)
        self.assertFalse(out.exists())

    def test_partial_io_failure_no_complete_marker(self):
        files,cap=self.collect();out=self.out()
        with patch.object(m.os,"fsync",side_effect=OSError("simulated I/O failure")):
            with self.assertRaises(OSError):self.write(out,files,cap)
        self.assertTrue(out.exists());self.assertFalse((out/"COMPLETE.json").exists())

    def test_frozen_and_outside_output_rejected(self):
        files,cap=self.collect()
        frozen=m.ROOT/"archives/reviews/codex-supervision/2026-10-17-progress-recheck"
        with self.assertRaises(ValueError):m.write_generation(frozen/("generation-"+uuid.uuid4().hex),files,cap,project=m.ROOT,approved_parent=frozen)
        with self.assertRaises(ValueError):self.write(Path(r"D:\code")/("generation-"+uuid.uuid4().hex),files,cap)

    def test_frozen_ancestor_above_supplied_subproject_rejected(self):
        frozen=m.ROOT/"archives/reviews/codex-supervision/2026-10-17-progress-recheck"
        subproject=frozen/"not-created-subproject"
        with self.assertRaises(ValueError):m.project_path(subproject/"out/new",subproject,writing=True)

    def test_reparse_paths_fail(self):
        with patch.object(Path,"is_symlink",return_value=True):
            with self.assertRaises(ValueError):self.collect()

if __name__=="__main__":unittest.main(verbosity=2)
