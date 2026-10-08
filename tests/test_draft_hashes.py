"""Draft hash portability must preserve content binding and immutable versions."""
import copy
import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'tools'),str(ROOT/'src')]
from tools.draft_io import NORMALIZED_HASH,RAW_HASH,fingerprint,normalized_bytes,publish_jsonl,selected_path,verify_entry
from tools import draft_audit,dataset_audit

class DraftHashTests(unittest.TestCase):
 def setUp(self):
  base=ROOT/'reviews/codex-supervision/2026-10-05-draft-hash-compatibility/test-work';base.mkdir(exist_ok=True)
  temp=tempfile.TemporaryDirectory(dir=base);self.root=Path(temp.name).resolve()
  assert self.root.is_relative_to(base.resolve())
  self.addCleanup(temp.cleanup)
  self.path=self.root/'batch-01/draft-test.jsonl';self.path.parent.mkdir()
  self.data='{"id":"q1","answer":"\\\\frac{1}{3}"}\n'.encode('utf-8')
  self.path.write_bytes(self.data)
  self.entry={'batch':'batch-01','path':'batch-01/draft-test.jsonl',**fingerprint(self.data),'count':1}
 def test_audit_similarity_is_an_exact_fraction(self):
  from fractions import Fraction
  with mock.patch.object(draft_audit,'shingles',side_effect=[{1,2},{2,3}]):
   self.assertEqual(draft_audit.jaccard_set('a','b'),Fraction(1,3))
  self.assertEqual(draft_audit.NEAR_DUP_THRESHOLD,Fraction(7,10))
 def test_exact_contract(self):
  self.assertEqual(normalized_bytes(b'\xef\xbb\xbfa\r\nb\r\n'),b'a\nb')
 def test_line_endings_bom_and_optional_terminal_newline(self):
  digest=fingerprint(self.data)['sha256']
  for data in [self.data,self.data.replace(b'\n',b'\r\n'),self.data.replace(b'\n',b'\r'),b'\xef\xbb\xbf'+self.data,self.data.rstrip(b'\n')]:
   self.path.write_bytes(data);self.assertEqual(verify_entry(self.path,self.entry,NORMALIZED_HASH)['sha256'],digest)
 def test_content_change_is_rejected(self):
  self.path.write_bytes(self.data.replace(b'{1}{3}',b'{2}{3}'))
  with self.assertRaisesRegex(ValueError,'hash mismatch'):verify_entry(self.path,self.entry,NORMALIZED_HASH)
 def test_internal_and_extra_trailing_blank_lines_remain_significant(self):
  self.assertNotEqual(fingerprint(b'a\nb\n')['sha256'],fingerprint(b'a\n\nb\n')['sha256'])
  self.assertNotEqual(fingerprint(b'a\n')['sha256'],fingerprint(b'a\n\n')['sha256'])
 def test_json_whitespace_remains_significant(self):
  self.assertNotEqual(fingerprint(b'{"a":1}\n')['sha256'],fingerprint(b'{"a": 1}\n')['sha256'])
 def test_invalid_utf8_not_replaced(self):
  with self.assertRaises(UnicodeDecodeError):fingerprint(b'\xff')
 def test_legacy_raw_hash_does_not_silently_fall_back(self):
  entry={'sha256':fingerprint(self.data)['raw_sha256']}
  self.assertEqual(verify_entry(self.path,entry)['hash_algorithm'],RAW_HASH)
  self.path.write_bytes(self.data.replace(b'\n',b'\r\n'))
  with self.assertRaises(ValueError):verify_entry(self.path,entry)
 def test_unknown_algorithm_rejected(self):
  with self.assertRaises(ValueError):verify_entry(self.path,{**self.entry,'hash_algorithm':'unknown'})
 def test_algorithm_conflict_rejected(self):
  with self.assertRaises(ValueError):verify_entry(self.path,{**self.entry,'hash_algorithm':RAW_HASH},NORMALIZED_HASH)
 def test_malformed_hash_and_missing_raw_hash_rejected(self):
  for bad in [{**self.entry,'sha256':'bad'},{k:v for k,v in self.entry.items() if k!='raw_sha256'}]:
   with self.assertRaises(ValueError):verify_entry(self.path,bad,NORMALIZED_HASH)
 def test_path_escape_and_missing_path_rejected(self):
  for path in ['../../outside.jsonl','',str(ROOT/'outside.jsonl'),'batch-02/other.jsonl']:
   with self.assertRaises(ValueError):selected_path(self.root,{**self.entry,'path':path})
 def test_writer_lf_no_bom_and_no_overwrite(self):
  p=self.root/'new.jsonl';row={'id':'q','problem':'中文题干','answer':r'\frac{1}{3}'};result=publish_jsonl(p,[row]);data=p.read_bytes()
  self.assertNotIn(b'\r',data);self.assertFalse(data.startswith(b'\xef\xbb\xbf'));self.assertTrue(data.endswith(b'\n'))
  self.assertEqual(json.loads(data),row);self.assertEqual(result,fingerprint(data)|{'count':1})
  with self.assertRaises(FileExistsError):publish_jsonl(p,[row])
  self.assertEqual(p.read_bytes(),data)
 def test_writer_validates_before_creating_file(self):
  p=self.root/'bad.jsonl'
  for rows in [[],[{'id':'x'},{'id':'x'}],[{'id':'x','value':float('nan')}]]:
   with self.assertRaises(ValueError):publish_jsonl(p,rows)
   self.assertFalse(p.exists())
 def test_coverage_ledger_rejects_tampering_but_accepts_format_equivalence(self):
  spec=importlib.util.spec_from_file_location('coverage_draft_test',ROOT/'reviews/2026-10-05-training-diversity-drafts/coverage_ledger.py')
  ledger=importlib.util.module_from_spec(spec);spec.loader.exec_module(ledger)
  selector=self.root/'draft-selection.json';selector.write_bytes(json.dumps({'schema':2,'hash_algorithm':NORMALIZED_HASH,'entries':[self.entry]}).encode())
  self.path.write_bytes(b'\xef\xbb\xbf'+self.data.replace(b'\n',b'\r\n'))
  rows,files=ledger.selected_rows(self.root);self.assertEqual(len(rows),1);self.assertFalse(files[0]['raw_bytes_match_manifest'])
  self.path.write_bytes(self.data.replace(b'{1}{3}',b'{2}{3}'))
  with self.assertRaises(ValueError):ledger.selected_rows(self.root)
 def test_bom_compatibility_does_not_change_generic_loader_default(self):
  self.path.write_bytes(b'\xef\xbb\xbf'+self.data)
  strict=dataset_audit.load_file(self.path);compatible=dataset_audit.load_file(self.path,allow_utf8_bom=True)
  self.assertTrue(any('BOM' in x for x in strict['structure_issues']))
  self.assertIsNone(strict['records'][0]['record']);self.assertIn('parse_error',strict['records'][0])
  self.assertFalse(any('解析失败' in x for x in compatible['structure_issues']))
  self.assertEqual(compatible['records'][0]['record']['id'],'q1')
 def test_actual_auditor_bom_crlf_and_forged_sha(self):
  original=(ROOT/'reviews/2026-10-05-training-diversity-drafts/batch-01/draft-codex-repair-v4-final.jsonl').read_text('utf-8').splitlines()[0]
  lf=(original+'\n').encode();self.path.write_bytes(lf);e={**self.entry,**fingerprint(lf)}
  selector=self.root/'draft-selection.json';data={'schema':2,'hash_algorithm':NORMALIZED_HASH,'draft_root':self.root.relative_to(ROOT).as_posix(),'entries':[e]}
  for label,bits,bad in [('bom-crlf',b'\xef\xbb\xbf'+lf.replace(b'\n',b'\r\n'),False),('bad-sha',lf,True)]:
   sel=copy.deepcopy(data)
   if bad:sel['entries'][0]['sha256']='0'*64
   selector.write_bytes(json.dumps(sel).encode());self.path.write_bytes(bits);out=self.root/label
   with mock.patch.object(draft_audit,'SELECTION',selector.relative_to(ROOT).as_posix()),mock.patch.object(draft_audit,'ORIG_GLOB',self.root.relative_to(ROOT).as_posix()+'/not-found*.jsonl'):
    draft_audit.main(['--drafts',self.path.relative_to(ROOT).as_posix(),'--out',out.relative_to(ROOT).as_posix()])
   summary=json.loads((out/'summary.json').read_text('utf-8'));counts=summary['issue_code_counts']
   self.assertEqual(counts.get('V007',0),int(bad));self.assertEqual(counts.get('V011',0),0)
   if not bad:self.assertEqual(summary['severity_counts'].get('hard',0),0)
 def test_retired_mutation_tools_stop_before_writing(self):
  for name in ['update_selection_sha','update_selection_v2','build_repair_v3','restore_repair_originals','fix_repair_issues','build_repair_v2']:
   module=importlib.import_module('tools.'+name)
   with self.assertRaisesRegex(ValueError,'Retired raw-hash'):module.main()

if __name__=='__main__':unittest.main()
