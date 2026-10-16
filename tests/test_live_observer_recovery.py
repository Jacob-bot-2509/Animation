"""Regression tests for the read-only observer; never import its worker entry point."""
import ast
import json
from pathlib import Path
import subprocess
import tempfile
import types
import unittest
from unittest.mock import Mock

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'reviews/codex-supervision/2026-10-04-live-watch/watch_claude.py'
TREE=ast.parse(SOURCE.read_text(encoding='utf-8'))
functions=[n for n in TREE.body if isinstance(n,ast.FunctionDef) and n.name in
           {'sample_processes','process_transition_events','discover_subtree_files'}]
NS={'subprocess':subprocess,'json':json,'Path':Path,'os':__import__('os'),'PS':'READ_ONLY_QUERY',
    'math_receipt_scopes':set(),'automation_receipt_scopes':{'reviews/witness-automation/jobs'}}
exec(compile(ast.Module(body=functions,type_ignores=[]),str(SOURCE),'exec'),NS)
row=lambda pid:{'ProcessId':pid,'ParentProcessId':1,'Name':'claude.exe'}
state=lambda status,rows:{'process_observation':{'status':status,'error':None},'claude_tree':rows}

class ProcessObservationTests(unittest.TestCase):
 def setUp(self):
  target=ROOT/'reviews/witness-automation/test-work'
  target.mkdir(exist_ok=True,parents=True)
  self.temp=tempfile.TemporaryDirectory(prefix='live-observer-',dir=target)
  self.root=Path(self.temp.name)
  self.addCleanup(self.temp.cleanup)
 def sample(self,data=None,rc=0,stderr=b'',error=None):
  run=Mock(side_effect=error) if error else Mock(return_value=types.SimpleNamespace(
      returncode=rc,stdout=json.dumps(data).encode() if data is not None else b'',stderr=stderr))
  return NS['sample_processes'](run)
 def test_single_process_object(self):
  actual=self.sample(row(7));self.assertEqual(actual['status'],'OK');self.assertEqual(actual['processes'],[row(7)])
 def test_empty_success_is_available(self):
  self.assertEqual(self.sample(),{'status':'OK','processes':[],'error':None})
 def test_cim_error_is_unavailable(self):
  actual=self.sample(rc=1,stderr=b'CIM unavailable')
  self.assertEqual(actual['status'],'UNAVAILABLE');self.assertIn('CIM unavailable',actual['error'])
 def test_timeout_is_unavailable(self):
  self.assertEqual(self.sample(error=subprocess.TimeoutExpired('powershell',15))['status'],'UNAVAILABLE')
 def test_invalid_json_is_unavailable(self):
  run=lambda *a,**kw:types.SimpleNamespace(returncode=0,stdout=b'invalid',stderr=b'')
  self.assertEqual(NS['sample_processes'](run)['status'],'UNAVAILABLE')
 def test_invalid_row_and_duplicate_identity(self):
  for rows in [[row(True)],[row(7),row(7)],[dict(row(7),CommandLine='must not be accepted')]]:
   self.assertEqual(self.sample(rows)['status'],'UNAVAILABLE')
 def test_failure_does_not_emit_false_process_exit(self):
  events=NS['process_transition_events'](state('OK',[row(7)]),state('UNAVAILABLE',[]))
  self.assertEqual([kind for kind,_ in events],['process_observation_unavailable'])
 def test_recovery_does_not_infer_start_or_exit_across_gap(self):
  events=NS['process_transition_events'](state('UNAVAILABLE',[]),state('OK',[row(9)]))
  self.assertEqual([kind for kind,_ in events],['process_baseline_restored'])
 def test_continuous_success_detects_actual_set_delta(self):
  events=NS['process_transition_events'](state('OK',[row(7)]),state('OK',[row(9)]))
  self.assertEqual([(kind,data['ProcessId']) for kind,data in events],[('process_started',9),('process_ended',7)])
 def test_repeated_unavailability_does_not_flood_event_log(self):
  self.assertEqual(NS['process_transition_events'](state('UNAVAILABLE',[]),state('UNAVAILABLE',[])),[])
 def test_failed_process_query_still_writes_file_heartbeat(self):
  loop=next(n for n in TREE.body if isinstance(n,ast.While))
  writes={};events=[]
  class EndIteration(Exception):pass
  def sleep(_):raise EndIteration()
  ns=dict(NS)
  ns.update({'OUT':self.root,
   'ROOT':ROOT,'prior':None,'watched':['configs/witness_automation.local.json'],
   'observed_subtrees':(),'manifest':{},'now':lambda:'TEST_TIME','os':__import__('os'),
   'hashlib':__import__('hashlib'),'time':types.SimpleNamespace(sleep=sleep),
   'subprocess':types.SimpleNamespace(run=lambda *a,**kw:types.SimpleNamespace(returncode=0,stdout='head')),
   'sample_processes':lambda:{'status':'UNAVAILABLE','processes':[],'error':'CIM unavailable'},
   'discover_subtree_files':lambda *a:(set(),[]),
   'write':lambda name,value:writes.__setitem__(name,value),'event':lambda kind,data:events.append((kind,data))})
  with self.assertRaises(EndIteration):
   exec(compile(ast.Module(body=[loop],type_ignores=[]),str(SOURCE),'exec'),ns)
  self.assertEqual(writes['latest.json']['process_observation']['status'],'UNAVAILABLE')
  self.assertIsNotNone(writes['latest.json']['hashes']['configs/witness_automation.local.json'])
  self.assertFalse(any(kind=='process_ended' for kind,_ in events))
 def test_receipt_discovery_excludes_package_bytes(self):
  root=self.root;job=root/'reviews/witness-automation/jobs/job-example';job.mkdir(parents=True)
  (job/'SUMMARY.json').write_text('{}');(job/'package.zip').write_bytes(b'not-executed')
  found,skipped=NS['discover_subtree_files'](root,('reviews/witness-automation/jobs',))
  self.assertEqual(found,{'reviews/witness-automation/jobs/job-example/SUMMARY.json'})
  self.assertEqual(skipped,[])

if __name__=='__main__':unittest.main()
