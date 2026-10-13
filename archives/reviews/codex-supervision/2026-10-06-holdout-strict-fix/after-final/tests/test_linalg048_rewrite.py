"""Exact shear and publication regressions; no production activation."""
import copy,json,os,subprocess,sys,tempfile,unittest
from pathlib import Path
from unittest import mock
ROOT=Path(__file__).resolve().parents[1];sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'src')]
import prepare_linalg048_rewrite as rewrite
from holdout_contract import Snapshot,object_sha

class RewriteTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.d=Path(self.tmp.name);self.addCleanup(self.tmp.cleanup)
        self.active,self.others,self.aliases,self.population=rewrite.load_population(Snapshot())
    def test_math_geometry_exact_and_line_set_distinguished(self):
        result=rewrite.math_checks(rewrite.CANDIDATE)
        self.assertEqual(result['oriented_area'],'1');self.assertEqual(result['vertical_image_slope'],'1/3')
        self.assertEqual(result['horizontal_segment_shifts'],['3/2','3']);self.assertEqual(result['e2_image_norm'],'sqrt(10)')
        self.assertIn('作为点集保持不变',rewrite.CANDIDATE['solution']);self.assertIn('有限线段',rewrite.CANDIDATE['scene_spec']['objects'][3])
    def test_wrong_matrix_or_math_text_rejected(self):
        for field in ('problem','answer'):
            row=copy.deepcopy(rewrite.CANDIDATE);row[field]+=' incorrect'
            with self.subTest(field=field),self.assertRaises(ValueError):rewrite.math_checks(row)
    def test_missing_schema_field_rejected(self):
        row=copy.deepcopy(rewrite.CANDIDATE);del row['license']
        with self.assertRaises(ValueError):rewrite.check_candidate(row,self.active,self.others,self.aliases)
    def test_active_identity_and_license_preserved(self):
        row=copy.deepcopy(rewrite.CANDIDATE);row['license']='different'
        with self.assertRaises(ValueError):rewrite.check_candidate(row,self.active,self.others,self.aliases)
    def test_all_manifest_train_files_included(self):
        manifest=json.loads(rewrite.MANIFEST.read_text('utf-8'));paths={(ROOT/'data'/e['path']).resolve() for e in manifest['entries'] if e['split']=='train'}
        self.assertEqual(paths,{(ROOT/p).resolve() for p in self.population['active_train_files']});self.assertEqual(len(paths),4)
        self.assertEqual(self.population['active_train_records'],47);self.assertEqual(len(self.others),46+250)
    def test_combined_candidate_hit_blocks_publication(self):
        with self.assertRaises(ValueError):rewrite.check_candidate(rewrite.CANDIDATE,self.active,[('train','cloned',dict(rewrite.CANDIDATE,id='cloned'))],self.aliases)
    def test_structural_candidate_hit_blocks_publication(self):
        with mock.patch.object(rewrite,'compare',return_value={'candidate':True,'coverage':'CANDIDATE'}):
            with self.assertRaises(ValueError):rewrite.check_candidate(rewrite.CANDIDATE,self.active,self.others,self.aliases)
    def test_named_semantic_review_is_hash_bound(self):
        aliases=copy.deepcopy(self.aliases);aliases['eval-linalg-015-s1']['problem']='another question'
        with self.assertRaises(ValueError):rewrite.check_candidate(rewrite.CANDIDATE,self.active,self.others,aliases)
    def test_math_guard_still_runs_under_python_optimization(self):
        code="import sys;sys.path[:0]=[r'D:/Animation-Model-Training/tools',r'D:/Animation-Model-Training/src'];import prepare_linalg048_rewrite as r;import copy;c=copy.deepcopy(r.CANDIDATE);c['problem']+='bad';r.math_checks(c)"
        cp=subprocess.run([str(ROOT/'.venv/Scripts/python.exe'),'-B','-O','-c',code],capture_output=True,encoding='utf-8')
        self.assertNotEqual(cp.returncode,0);self.assertIn('ValueError',cp.stderr)
    def test_valid_candidate_is_new_unadmitted_and_bound(self):
        p=self.d/'candidate.json';q=self.d/'receipt.json'
        before=rewrite.MANIFEST.read_bytes();self.assertEqual(rewrite.main(['--out',str(p),'--checks',str(q)]),0)
        report=json.loads(q.read_text('utf-8'));self.assertFalse(report['admitted']);self.assertFalse(report['global_leakage_free_certified'])
        self.assertEqual(report['candidate_record_sha256'],object_sha(json.loads(p.read_text('utf-8'))));self.assertEqual(before,rewrite.MANIFEST.read_bytes())
    def test_existing_outputs_and_colliding_paths_preserved(self):
        p=self.d/'candidate.json';p.write_bytes(b'OLD')
        self.assertEqual(rewrite.main(['--out',str(p)]),2);self.assertEqual(p.read_bytes(),b'OLD')
        p=self.d/'new.json';self.assertEqual(rewrite.main(['--out',str(p),'--checks',str(p)]),2);self.assertFalse(p.exists())
    def test_source_drift_before_publication_creates_nothing(self):
        p=self.d/'new.json'
        with mock.patch.object(rewrite.Snapshot,'check_unchanged',side_effect=ValueError('source changed')):
            self.assertEqual(rewrite.main(['--out',str(p)]),2)
        self.assertFalse(p.exists())
    def test_existing_receipt_blocks_candidate_creation(self):
        p=self.d/'new.json';q=self.d/'receipt.json';q.write_bytes(b'OLD')
        self.assertEqual(rewrite.main(['--out',str(p),'--checks',str(q)]),2);self.assertFalse(p.exists());self.assertEqual(q.read_bytes(),b'OLD')

if __name__=='__main__':unittest.main()
