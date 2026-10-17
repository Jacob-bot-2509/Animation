import importlib.util,json,shutil,tempfile,unittest
from pathlib import Path
from unittest import mock
HERE=Path(__file__).absolute().parent
s=importlib.util.spec_from_file_location("backup_audit",HERE/"verify_training_backup.py");m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
SCRATCH=m.ROOT/"reviews/codex-supervision/2026-10-17-backup-audit-tests";SCRATCH.mkdir(exist_ok=True)
class Tests(unittest.TestCase):
 def setUp(self):
  self.base=Path(tempfile.mkdtemp(prefix="case-",dir=SCRATCH));self.src=self.base/"source";self.dst=self.base/"copy"
  for root in [self.src,self.dst]:
   for part in m.PARTS:(root/part).mkdir(parents=True)
   (root/"data/one.bin").write_bytes(b"data\x00")
   (root/"configs/settings.json").write_bytes(b'{"a":1}')
 def tearDown(self):
  p=self.base.resolve();assert p.is_relative_to(SCRATCH.resolve()) and p!=SCRATCH.resolve();shutil.rmtree(p)
 def test_equal_and_no_writes(self):
  before={p:p.stat().st_mtime_ns for root in [self.src,self.dst] for p in root.rglob("*")}
  x=m.audit(self.src,self.dst);self.assertEqual(x["status"],"PASS_CURRENT_CONTENT_EQUALITY_ONLY");self.assertEqual(x["matched_files"],2)
  self.assertEqual(before,{p:p.stat().st_mtime_ns for root in [self.src,self.dst] for p in root.rglob("*")})
  self.assertIsNone(x["original_robocopy_returncodes"])
 def test_same_count_same_size_wrong_content(self):
  (self.dst/"data/one.bin").write_bytes(b"FAIL\x00");x=m.audit(self.src,self.dst)
  self.assertEqual(x["status"],"FAIL");self.assertEqual(x["mismatched_files"],["data/one.bin"])
 def test_missing_file(self):
  (self.dst/"data/one.bin").unlink();self.assertEqual(m.audit(self.src,self.dst)["missing_files"],["data/one.bin"])
 def test_extra_file(self):
  (self.dst/"data/stale.txt").write_bytes(b"old");self.assertEqual(m.audit(self.src,self.dst)["extra_files"],["data/stale.txt"])
 def test_extra_empty_directory(self):
  (self.dst/"data/stale").mkdir();self.assertEqual(m.audit(self.src,self.dst)["extra_directories"],["data/stale"])
 def test_missing_required_directory(self):
  (self.dst/"holdout-sources").rmdir()
  with self.assertRaises(OSError):m.audit(self.src,self.dst)
 def test_overlap_rejected(self):
  with self.assertRaisesRegex(ValueError,"overlapping_roots"):m.audit(self.src,self.src)
 def test_nested_root_rejected(self):
  with self.assertRaisesRegex(ValueError,"overlapping_roots"):m.audit(self.src,self.src/"nested")
 def test_inventory_budget(self):
  with self.assertRaisesRegex(ValueError,"inventory_budget"):m.inventory(self.src,max_files=1)
 def test_file_change_rejected(self):
  p=self.src/"data/one.bin";pin=m.fingerprint(p.stat());p.write_bytes(b"new")
  with self.assertRaisesRegex(ValueError,"file_changed_before_hash"):m.hash_file(p,pin)
 def test_tree_change_rejected(self):
  original=m.hash_file;changed=False
  def change(*a,**k):
   nonlocal changed
   result=original(*a,**k)
   if not changed:(self.src/"data/new.txt").write_bytes(b"drift");changed=True
   return result
  with mock.patch.object(m,"hash_file",side_effect=change):
   with self.assertRaisesRegex(ValueError,"tree_changed"):m.audit(self.src,self.dst)
 def test_reparse_flag_rejected(self):
  original=Path.lstat
  def flagged(p,*a,**k):
   st=original(p,*a,**k)
   if p==self.src:
    return type("S",(),{"st_file_attributes":0x400,"st_mode":st.st_mode})()
   return st
  with mock.patch.object(Path,"lstat",flagged):
   with self.assertRaisesRegex(ValueError,"reparse"):m.inventory(self.src)
 def test_frozen_output_rejected(self):
  (self.base/"delivery-manifest.json").write_bytes(b"{}")
  with self.assertRaisesRegex(ValueError,"frozen"):m.write_report({"status":"TEST"},self.src)
 def test_outside_output_rejected(self):
  with self.assertRaisesRegex(ValueError,"output_outside"):m.write_report({"status":"TEST"},m.ROOT.parent)
 def test_new_report_only(self):
  result={"status":"TEST"};a=m.write_report(result,self.base);b=m.write_report(result,self.base);self.assertNotEqual(a,b)
  c=json.loads((a/"COMPLETE.json").read_bytes());raw=(a/"audit.json").read_bytes();self.assertEqual(c["artifact"]["sha256"],m.sha(raw))

 def current_fixture(self):
  raw=b'{"id":"current"}\n';manifest={"entries":[{"path":"items.jsonl","sha256":m.sha(raw),"size":len(raw)}]}
  for root in [self.src,self.dst]:
   (root/"data/items.jsonl").write_bytes(raw)
   (root/"data/manifest.json").write_bytes(m.enc(manifest))
   (root/"data/asset_evidence.json").write_bytes(b"{}")
   (root/"configs/training_diversity_policy.json").write_bytes(b"{}")
   (root/"configs/train_loop.example.json").write_bytes(b"{}")
 def test_current_inputs_scope(self):
  self.current_fixture();x=m.audit_current_inputs(self.src,self.dst)
  self.assertEqual(x["status"],"PASS_CURRENT_MANIFEST_INPUTS_ONLY");self.assertEqual(len(x["records"]),5)
  self.assertEqual(x["whole_backup"],"UNVERIFIED_RESOURCE_LIMIT")
 def test_current_input_mismatch(self):
  self.current_fixture();(self.dst/"data/items.jsonl").write_bytes(b"wrong")
  self.assertEqual(m.audit_current_inputs(self.src,self.dst)["status"],"FAIL")
 def test_current_input_missing(self):
  self.current_fixture();(self.dst/"configs/train_loop.example.json").unlink()
  self.assertEqual(m.audit_current_inputs(self.src,self.dst)["status"],"FAIL")
 def test_current_manifest_path_escape(self):
  self.current_fixture();p=self.src/"data/manifest.json";x=json.loads(p.read_bytes());x["entries"][0]["path"]="../outside";p.write_bytes(m.enc(x))
  with self.assertRaisesRegex(ValueError,"manifest_path_alias"):m.audit_current_inputs(self.src,self.dst)
 def test_current_manifest_size_mismatch(self):
  self.current_fixture();p=self.src/"data/manifest.json";x=json.loads(p.read_bytes());x["entries"][0]["size"]=999;p.write_bytes(m.enc(x))
  with self.assertRaisesRegex(ValueError,"manifest_input_size"):m.audit_current_inputs(self.src,self.dst)
 def test_shared_file_identity_not_backup(self):
  import os
  (self.dst/"data/one.bin").unlink();os.link(self.src/"data/one.bin",self.dst/"data/one.bin")
  self.assertEqual(m.audit(self.src,self.dst)["shared_file_identity"],["data/one.bin"])

if __name__=="__main__":unittest.main(verbosity=2)
