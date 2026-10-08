import hashlib,json,tempfile,unittest
from pathlib import Path
from tools.leakage_population import ROOT,census

class PopulationTests(unittest.TestCase):
    def setUp(self):
        base=ROOT/'reviews/codex-supervision/2026-10-05-readiness-completion/test-tmp';base.mkdir(exist_ok=True)
        self.temp=tempfile.TemporaryDirectory(dir=base);self.addCleanup(self.temp.cleanup);self.base=Path(self.temp.name)
    def records(self):
        train=[{'id':'a','category':'数学','sub_category':'A','problem':'$x$'},{'id':'b','category':'数学','sub_category':'B','problem':'$x+1$'}]
        query=[{'id':'q'+str(i),'category':'数学','sub_category':'A','problem':'$x$'} for i in range(3)]
        entries=[]
        for split,rows in [('train',train),('eval',query)]:
            p=self.base/(split+'.jsonl');p.write_text('\n'.join(json.dumps(r,ensure_ascii=False) for r in rows),encoding='utf-8');entries.append({'split':split,'path':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
        mp=self.base/'manifest.json';mp.write_text(json.dumps({'entries':entries}),encoding='utf-8');return mp
    def test_multiple_solutions_do_not_multiply_problem_pairs(self):
        r=census(self.records(),self.base)
        self.assertEqual(r['candidate_pairs'],2);self.assertEqual(r['raw_record_counts']['eval'],3);self.assertEqual(r['unique_problem_counts']['eval'],1);self.assertEqual(len(r['pairs'][0]['query']['sources']),3)
    def test_different_signature_is_included_by_default(self):
        r=census(self.records(),self.base)
        self.assertEqual(sum(not p['same_signature'] for p in r['pairs']),1)
    def test_signature_only_is_explicit_and_never_auto_calibrates(self):
        r=census(self.records(),self.base,True)
        self.assertEqual(r['candidate_pairs'],1);self.assertFalse(r['calibrated']);self.assertFalse(r['automatically_labeled'])
    def test_changed_data_is_rejected(self):
        mp=self.records();(self.base/'train.jsonl').write_text('{}',encoding='utf-8')
        with self.assertRaises(ValueError):census(mp,self.base)
    def test_score_retains_exact_set_ratio(self):
        from fractions import Fraction
        r=census(self.records(),self.base)
        for p in r['pairs']:
            expected=Fraction(p['intersection'],p['union']) if p['union'] else Fraction(0)
            self.assertEqual(Fraction(p['j5']),expected);self.assertNotIn('.',p['j5'])
if __name__=='__main__':unittest.main()
