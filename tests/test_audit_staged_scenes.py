import copy,json,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'tools'))
from audit_staged_scenes import audit_staged
from draft_io import publish_jsonl
from holdout_contract import raw_sha
class StagedAuditTests(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.directory=self.root/'candidate';self.directory.mkdir();self.source=self.root/'source.json';self.source.write_bytes(b'{}')
  self.row={'id':'example','scene_spec':{'objects':[r'$\theta$'],'steps':[r'$\frac{1}{2}$']},'admitted':False,'training_admitted':False,'render_verified':False,'animation_verified':False}
  self.sel={'schema':2,'status':'UNSELECTED_NOT_ADMITTED','entries':[]};self.rec={'schema':'scene-staging-receipt-v2','status':'STAGED_UNSELECTED_NOT_ADMITTED','record_count':1,'production_selector_updated':False,'training_admitted':False,'visual_verified':False,'source_bindings':{'source.json':{'raw_sha256':raw_sha(b'{}'),'bytes':2}}};self.write()
 def tearDown(self): self.temp.cleanup()
 def write(self):
  path=self.directory/'batch-01/draft-new.jsonl';path.parent.mkdir(exist_ok=True);data=(json.dumps(self.row,ensure_ascii=True)+'\n').encode('utf-8');path.write_bytes(data)
  from draft_io import fingerprint
  self.sel['entries']=[{'batch':'batch-01','path':'batch-01/draft-new.jsonl','count':1,**fingerprint(data)}];self.save()
 def save(self):
  (self.directory/'draft-selection.candidate.json').write_text(json.dumps(self.sel),encoding='utf-8');(self.directory/'stage-receipt.json').write_text(json.dumps(self.rec),encoding='utf-8')
 def audit(self):return audit_staged(self.directory,root=self.root)
 def test_valid_is_integrity_only(self):
  v=self.audit();self.assertTrue(v['passed']);self.assertFalse(v['math_verified']);self.assertFalse(v['visual_verified'])
 def test_tab_corrupted_theta_is_rejected(self):
  self.row['scene_spec']['steps']=['$\theta$'];self.write();self.assertFalse(self.audit()['passed'])
 def test_other_control_and_replacement_are_rejected(self):
  for ch in ('\r','\b','\x7f','\x85','\ufffd'):
   with self.subTest(ch=repr(ch)):
    self.row['scene_spec']['steps']=['bad'+ch];self.write();self.assertFalse(self.audit()['passed'])
 def test_missing_candidate_is_error(self):
  with self.assertRaises(OSError):audit_staged(self.root/'missing',root=self.root)
 def test_empty_entries_fail(self):
  self.sel['entries']=[];self.save()
  with self.assertRaises(ValueError):self.audit()
 def test_missing_record_file_fails(self):
  (self.directory/'batch-01/draft-new.jsonl').unlink()
  with self.assertRaises(OSError):self.audit()
 def test_forged_hash_fails(self):
  self.sel['entries'][0]['raw_sha256']='0'*64;self.save()
  with self.assertRaises(ValueError):self.audit()
 def test_source_drift_fails(self):
  self.source.write_bytes(b'{"changed":true}')
  with self.assertRaises(ValueError):self.audit()
 def test_coverage_mismatch_fails(self):
  self.rec['record_count']=2;self.save()
  with self.assertRaises(ValueError):self.audit()
 def test_duplicate_batch_fails(self):
  self.sel['entries']*=2;self.save()
  with self.assertRaises(ValueError):self.audit()
 def test_unknown_scene_shape_fails(self):
  self.row['scene_spec']['steps']=[42];self.write()
  with self.assertRaises(ValueError):self.audit()
 def test_admission_flag_fails(self):
  self.row['admitted']=True;self.write()
  with self.assertRaises(ValueError):self.audit()
 def test_path_escape_fails(self):
  self.sel['entries'][0]['path']='../source.json';self.save()
  with self.assertRaises(ValueError):self.audit()
 def test_receipt_drift_during_audit_fails(self):
  from unittest.mock import patch
  import audit_staged_scenes as module
  original=module.jsonl
  def drift(data):
   rows=original(data);self.rec['concurrent_change']=True;self.save();return rows
  with patch.object(module,'jsonl',side_effect=drift):
   with self.assertRaises(ValueError):self.audit()
 def test_prose_substep_newlines_are_valid(self):
  self.row['scene_spec']['steps']=['first substep\nsecond substep'];self.write();self.assertTrue(self.audit()['passed'])
 def test_newline_inside_formula_is_rejected(self):
  self.row['scene_spec']['steps']=['$a\nabla b$'];self.write();self.assertFalse(self.audit()['passed'])
if __name__=='__main__':unittest.main()