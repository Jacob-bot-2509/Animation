from pathlib import Path
import importlib.util,json,tempfile,unittest,hashlib
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('ledger',P/'coverage_ledger.repaired.py');L=importlib.util.module_from_spec(spec);spec.loader.exec_module(L)
class Tests(unittest.TestCase):
 def fixture(self):
  d=tempfile.TemporaryDirectory(dir=P);self.addCleanup(d.cleanup);root=Path(d.name);b=root/'batch-01';b.mkdir()
  for name,text in [('draft.jsonl','旧'),('draft-v3.jsonl','新')]:
   (b/name).write_text(json.dumps({'id':'q','concept_id':'C01','problem':text},ensure_ascii=False)+'\n',encoding='utf-8')
  return root,b
 def test_latest_numbered_version(self):
  root,b=self.fixture();self.assertEqual(L.selected_rows(root)[0][0]['problem'],'新')
 def test_exact_threshold_fraction(self):
  from fractions import Fraction
  self.assertEqual(L.THRESHOLD,Fraction(2,5));self.assertIsInstance(L.j5('abcdefghi','defghijkl'),Fraction)
 def test_hash_mismatch_stops(self):
  root,b=self.fixture();(root/'draft-selection.json').write_text(json.dumps({'entries':[{'batch':'batch-01','path':'batch-01/draft-v3.jsonl','sha256':'0'*64}]}),encoding='utf-8')
  with self.assertRaises(ValueError):L.selected_rows(root)
 def test_explicit_version_prevents_fallback(self):
  root,b=self.fixture();old=b/'draft.jsonl';(root/'draft-selection.json').write_text(json.dumps({'entries':[{'batch':'batch-01','path':'batch-01/draft.jsonl','sha256':L.digest(old)}]}),encoding='utf-8')
  self.assertEqual(L.selected_rows(root)[0][0]['problem'],'旧')
 def test_duplicate_ids_stop(self):
  root,b=self.fixture();(root/'batch-02').mkdir();(root/'batch-02/draft.jsonl').write_bytes((b/'draft.jsonl').read_bytes())
  with self.assertRaises(ValueError):L.selected_rows(root)
 def test_drafts_cannot_certify_density(self):
  drafts=[{'id':str(i),'concept_id':'C01','admitted':True,'strict_review':{'core_math_verified':True}} for i in range(8)]
  c,u=L.planning_counts([{'id':'C01','name':'概念'}],[],drafts,{})
  self.assertEqual(c[0]['math_reviewed_drafts'],8);self.assertEqual(c[0]['newly_admitted'],0);self.assertFalse(c[0]['formal_density_pass'])
 def test_path_escape_stops(self):
  root,b=self.fixture();(root/'draft-selection.json').write_text(json.dumps({'entries':[{'batch':'batch-01','path':'../outside.jsonl','sha256':'0'*64}]}),encoding='utf-8')
  with self.assertRaises(ValueError):L.selected_files(root)
if __name__=='__main__':unittest.main()
