"""Lifecycle tests for consumer watch; no cloud scan, probes, or frozen job writes."""
from pathlib import Path
import contextlib,copy,io,json,sys,tempfile,unittest
from unittest import mock
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import witness_consumer as consumer
import witness_transfer_common as c

class WatchLifecycleTests(unittest.TestCase):
 def setUp(self):
  scratch=c.mkdir(ROOT/'reviews/witness-automation/test-work')
  self.temp=tempfile.TemporaryDirectory(prefix='watch-lifecycle-',dir=scratch)
  self.root=Path(self.temp.name).resolve()
  self.assertTrue(self.root.is_relative_to(scratch.resolve()))
  self.addCleanup(self.temp.cleanup)
  self.runtime=self.root/'runtime';self.runtime.mkdir()
  self.cfg={'consumer':{'runtime_root':str(self.runtime)},'retry_delays_seconds':[5,15,45,120]}
  self.args=['--config',str(self.root/'not-used.json'),'--execute','--watch']
 def run_main(self,args=None):
  with contextlib.redirect_stdout(io.StringIO()) as stream:
   rc=consumer.main(self.args if args is None else args)
  return rc,stream.getvalue()
 def stop(self,runtime=None):
  folder=runtime or self.runtime;folder.mkdir(exist_ok=True,parents=True)
  (folder/'STOP').write_text('test stop',encoding='utf-8')
 def assert_lock_released(self):
  with c.lock(self.runtime/'consumer-watch'):pass
 def test_second_watch_rejected_while_first_waits(self):
  nested=[];entered=False
  def sleep(_):
   nonlocal entered
   if not entered:
    entered=True;nested.append(self.run_main()[0]);self.stop()
   else:self.stop()
  with mock.patch.object(c,'load_config',return_value=self.cfg),mock.patch.object(consumer,'scan',return_value=[]) as scan,mock.patch.object(consumer.time,'sleep',side_effect=sleep):
   rc,_=self.run_main()
  self.assertEqual(rc,0);self.assertEqual(nested,[2]);self.assertEqual(scan.call_count,1)
  self.assert_lock_released()
 def test_scan_lock_independent_of_lifetime_lock(self):
  def scan(_):
   with c.lock(self.runtime):return []
  with mock.patch.object(c,'load_config',return_value=self.cfg),mock.patch.object(consumer,'scan',side_effect=scan),mock.patch.object(consumer.time,'sleep',side_effect=lambda _:self.stop()):
   rc,_=self.run_main()
  self.assertEqual(rc,0);self.assert_lock_released()
 def test_runtime_change_requires_restart(self):
  changed=copy.deepcopy(self.cfg);new=self.root/'runtime-two';changed['consumer']['runtime_root']=str(new)
  calls=0
  def load(*a,**kw):
   nonlocal calls
   calls+=1
   return self.cfg if calls<=2 else changed
  def sleep(_):
   if calls>=3:self.stop(new)
  with mock.patch.object(c,'load_config',side_effect=load),mock.patch.object(consumer,'scan',return_value=[]) as scan,mock.patch.object(consumer.time,'sleep',side_effect=sleep):
   rc,out=self.run_main()
  self.assertEqual(rc,2);self.assertIn('WATCH_RUNTIME_CHANGED_RESTART_REQUIRED',out)
  self.assertEqual(scan.call_count,1);self.assertFalse(new.exists());self.assert_lock_released()
 def test_scan_exception_releases_lifetime_lock(self):
  with mock.patch.object(c,'load_config',return_value=self.cfg),mock.patch.object(consumer,'scan',side_effect=ValueError('controlled-test-failure')):
   rc,_=self.run_main()
  self.assertEqual(rc,2);self.assert_lock_released()
 def test_existing_stop_does_not_start_watch(self):
  self.stop()
  with mock.patch.object(c,'load_config',return_value=self.cfg),mock.patch.object(consumer,'scan') as scan:
   rc,_=self.run_main()
  self.assertEqual(rc,0);scan.assert_not_called();self.assertFalse((self.runtime/'consumer-watch').exists())
 def test_one_shot_does_not_hold_service_lock(self):
  with mock.patch.object(c,'load_config',return_value=self.cfg),mock.patch.object(consumer,'scan',return_value=[]) as scan:
   rc,_=self.run_main(self.args[:-1])
  self.assertEqual(rc,0);self.assertEqual(scan.call_count,1);self.assertFalse((self.runtime/'consumer-watch').exists())
 def test_plan_does_not_load_config_or_create_service_lock(self):
  with mock.patch.object(c,'load_config') as load:
   rc,_=self.run_main(['--watch'])
  self.assertEqual(rc,3);load.assert_not_called();self.assertFalse((self.runtime/'consumer-watch').exists())

if __name__=='__main__':unittest.main()
