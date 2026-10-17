"""Exact sweep-selection regressions. Main is simulated: no model, training or eval launch."""
import ast,contextlib,io,json,random,sys,tempfile,types,unittest,uuid
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'tools/hp_sweep.py'
TREE=ast.parse(SOURCE.read_text(encoding='utf-8-sig'))
DEFS=[v for v in TREE.body if isinstance(v,ast.FunctionDef) and v.name in {'_verified_rate','rank_candidates','main'}]

def metric(p=1,n=1,status='VERIFIED',rate=None):
 return {'status':status,'passed':p,'total':n,'rate':str(p) if n==1 and rate is None else (str(p)+'/'+str(n) if rate is None else rate)}

def candidate(name,e=None,r=None,m=None):
 return {'name':name,'status':'OK','metrics':{'executable':e or {'status':'UNVERIFIED','rate':None},
  'render':r or {'status':'UNVERIFIED','rate':None},'math':m or {'status':'UNVERIFIED','rate':None}}}

class SweepSelectionTests(unittest.TestCase):
 def setUp(self):
  self.ns={'argparse':__import__('argparse'),'Path':Path,'json':json,'hashlib':__import__('hashlib'),
   'datetime':datetime,'uuid':uuid,'sys':sys}
  exec(compile(ast.Module(body=DEFS,type_ignores=[]),str(SOURCE),'exec'),self.ns)
 def rank(self,rows):return self.ns['rank_candidates'](rows)
 def test_fraction_rates_sort_exactly(self):
  self.assertEqual([x['name'] for x in self.rank([candidate('low',metric(3,4)),candidate('high',metric(4,5))])],['high','low'])
 def test_near_one_does_not_round_to_tie(self):
  n=10**40
  self.assertEqual(self.rank([candidate('less',metric(n-1,n)),candidate('one',metric(n,n))])[0]['name'],'one')
 def test_all_unverified_has_no_winner(self):
  self.assertEqual(self.rank([candidate('a'),candidate('b')]),[])
 def test_unverified_claimed_high_rate_is_ignored(self):
  unknown=metric(1,1,status='UNVERIFIED')
  self.assertEqual([x['name'] for x in self.rank([candidate('unknown',unknown),candidate('known',metric(1,2))])],['known'])
 def test_math_only_cannot_select_execution_winner(self):
  self.assertEqual(self.rank([candidate('math-only',m=metric())]),[])
 def test_count_and_fraction_mismatch_rejected(self):
  with self.assertRaises(ValueError):self.rank([candidate('bad',metric(1,2,rate='1'))])
 def test_boolean_counts_rejected(self):
  with self.assertRaises(ValueError):self.rank([candidate('bad',metric(True,1,rate='1'))])
 def test_decimal_rate_is_not_accepted_as_exact_metric(self):
  for value in ['0.5',0.5,float('nan'),'1/0']:
   with self.subTest(value=value),self.assertRaises(ValueError):
    self.rank([candidate('bad',metric(1,2,rate=value))])
 def test_denominator_binds_total_questions(self):
  row=candidate('bad',metric(1,2));row['metrics']['total_questions']=3
  with self.assertRaises(ValueError):self.rank([row])
 def test_cli_refuses_winner_when_simulated_eval_is_unverified(self):
  scratch=ROOT/'reviews/witness-automation/test-work';scratch.mkdir(exist_ok=True,parents=True)
  with tempfile.TemporaryDirectory(prefix='sweep-selection-',dir=scratch) as temp:
   base=Path(temp).resolve();self.assertTrue(base.is_relative_to(scratch.resolve()))
   config=base/'sweep.json';winner=base/'winner.json'
   config.write_text(json.dumps({'candidates':[{'name':'a','hyperparameters':{},'hyperparameter_approval':{}}],
    'dataset_manifest':str(base/'manifest.json'),'model_path':str(base/'model'),'output_winner':str(winner)}))
   def evaluate(_config,work,*args):
    report={k:{'status':'UNVERIFIED','rate':None} for k in ('executable','render','math','fidelity')}
    report['total_questions']=1
    (work/'eval-report.json').write_text(json.dumps(report))
    return 0
   trained=Mock(return_value={'status':'TRAINED'})
   self.ns.update({'ROOT':base,'STOP_FILE':base/'STOP','build_subset':lambda *a:[],
    'gate_ready':Mock(return_value=(True,'simulated only')),
    'ts':types.SimpleNamespace(hyperparameter_approval_error=lambda _:None,train=trained),
    'es':types.SimpleNamespace(run=evaluate)})
   with contextlib.redirect_stdout(io.StringIO()):rc=self.ns['main'](['--config',str(config)])
   self.assertEqual(rc,2);self.assertFalse(winner.exists())
   report=next((base/'runs').glob('*/sweep-report.json'))
   self.assertIsNone(json.loads(report.read_text())['winner'])
   md=(report.parent/'sweep-report.md').read_text(encoding='utf-8')
   self.assertIn('NO_VERIFIED_WINNER',md);self.assertIn('| a |',md)
   self.assertEqual(trained.call_count,1)  # Mock only, no training executor imported/called.

if __name__=='__main__':unittest.main()
