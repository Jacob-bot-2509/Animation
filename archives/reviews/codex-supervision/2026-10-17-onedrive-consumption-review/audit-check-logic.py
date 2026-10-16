# Review logic from the executed audit, excluding embedded receipt copies already archived separately.
from pathlib import Path
import sys,json,hashlib,importlib.util,io,contextlib,types
from fractions import Fraction
from datetime import datetime,timezone,timedelta
p=Path(r'D:\Animation-Model-Training');a=p/'archives/reviews/codex-supervision/2026-10-17-onedrive-consumption-review';o=p/'reviews/codex-supervision/2026-10-08-auto-mail';rid='run-140a171a9d1a4ab6b9cd8c5a6528aee2';r=o/'runs'/rid
assert not a.exists()
a.mkdir()
def sha(raw):return hashlib.sha256(raw).hexdigest()
def save(n,obj):
 f=a/n;f.parent.mkdir(exist_ok=True,parents=True)
 f.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
checks=[]
def ck(n,ok,detail=None):
 checks.append({'name':n,'passed':bool(ok),'detail':detail});assert ok,n
spec=importlib.util.spec_from_file_location('mw',o/'mail_watch.py');mw=importlib.util.module_from_spec(spec);spec.loader.exec_module(mw)
packet=json.loads((r/'inbox.json').read_bytes());ledger=json.loads((o/'journal.json').read_bytes())
ck('active-run-exact',packet['run_id']==ledger['active_run']['id']==rid)
ck('two-exact-source-messages',{m['id'] for m in packet['messages']}=={'msg_1792169552651_833','msg_1792169617421_834'})
for msg in packet['messages']:
 src=o/'messages'/(msg['id']+'.json')
 ck('mail-canonical-hash:'+msg['id'],mw.message_hash(json.loads(src.read_bytes()))==packet['message_hashes'][msg['id']]==ledger['items'][msg['id']]['message_sha256'])
 (a/(msg['id']+'.json')).write_bytes(src.read_bytes())
for name in ['instructions.md','inbox.json']:(a/name).write_bytes((r/name).read_bytes())
sys.path.insert(0,str(p/'tools'))
import witness_transfer_common as c
import witness_consumer as consumer
import witness_registered_adapter as adapter
config_path=p/'configs/witness_automation.local.json'
cfg=c.load_config(config_path,execute=True,role='consumer')
(a/'local-config.reviewed.json').write_bytes(config_path.read_bytes())
for rel,digest in cfg['automation_source_pins'].items():ck('automation-pin:'+rel,sha((p/rel).read_bytes())==digest)
for rel,digest in cfg['v3_source_pins'].items():
 f=p/rel if rel!='witness_receiver_v3.exe' else p/'reviews/codex-supervision/2026-10-09-witness-input-hardening/release/witness_receiver_v3.exe'
 ck('v3-pin:'+rel,sha(f.read_bytes())==digest)
ck('consumer-config-active-bounded',cfg['active'] is True and cfg['production']=='CLOSED' and cfg['allow_probe_emission'] is False and cfg['allow_training_start'] is False)
job=p/'reviews/witness-automation/jobs/job-e652263c33094648a5113e70dfa5adab'
job_before={str(f.relative_to(job)).replace('\\','/'):sha(f.read_bytes()) for f in job.rglob('*') if f.is_file()}
summary=consumer.verify_frozen(job)
ck('new-job-13-frozen-artifacts',len(job_before)==14 and len(json.loads((job/'delivery-manifest.json').read_bytes())['artifacts'])==13)
package_sha='7d25d860a9cffb497f99e4e016c4228eab5b7aa5144e3c9ffac631b015efca6f'
sync=Path(cfg['consumer']['sync_root']);ready_path=sync/(package_sha+'.ready.json')
ready,manifest,blobs,zip_raw=consumer.pair(ready_path,sync)
ck('actual-package-sha-and-size',sha(zip_raw)==package_sha and len(zip_raw)==4844)
ck('actual-ready-size',ready_path.stat().st_size==365)
ck('job-package-exact-sync-bytes',(job/'package.zip').read_bytes()==zip_raw)
ck('ready-original-identity',(ready['round'],ready['capture_id'])==('lan-2026-10-13-a','e605e0ee3a8b4388aa72271d56f473cd'))
capture=job/'capture'/(ready['round']+'-'+ready['capture_id'])
for name,raw in blobs.items():ck('package-five-raw-match-job:'+name,(capture/name).read_bytes()==raw)
entry=cfg['sender_registry'][0]
sender,_,sender_obj,input_bindings=adapter.binding_inputs(entry)
ck('six-original-sender-native-bindings',len(input_bindings)==6,input_bindings)
ck('job-sender-raw-exact-original',(job/'sender.json').read_bytes()==sender.read_bytes())
receipt=json.loads((job/'ADAPTER_RECEIPT.json').read_bytes())
for value,digest in receipt['input_bindings'].items():ck('receipt-input:'+str(Path(value).name),sha(Path(value).read_bytes())==digest)
ck('receipt-record-digest',sha(Path(receipt['record']['path']).read_bytes())==receipt['record']['sha256'])
inspector=adapter.load_bound(p/'tools/inspect_witness_evidence.py',c.V3_PINS['tools/inspect_witness_evidence.py'])
inspector.driver.REGISTERED_ROOT=job
precheck=inspector.inspect_capture(job/'sender.json',capture)
ck('precheck-recomputed-clean',precheck['status']=='READY_FOR_REGISTERED_RECONCILIATION' and precheck['findings']==[])
ck('precheck-exact-delivered-value',precheck==json.loads((job/'PRECHECK.json').read_bytes()))
save('precheck-independent.json',precheck)
driver=adapter.load_bound(p/'tools/sandbox_external_test_driver.py',c.V3_PINS['tools/sandbox_external_test_driver.py'])
driver.REGISTERED_ROOT=job
allowed={str(Path(x).absolute()) for x in receipt['input_bindings']}|{str((p/k).absolute()) for k in receipt['v3_source_bindings']}
def read_registered(value,must_exist=True):
 path=c.checked(value,p)
 if str(path) not in allowed and path!=capture:raise AssertionError('UNAPPROVED_RECOMPUTE_READ:'+str(path))
 if must_exist:assert path.exists()
 return path
captured=[]
def in_memory_output(path,data):
 path=Path(path)
 assert path.parent==job and path.name.startswith('reconciled-') and c.GUID.fullmatch(path.stem[len('reconciled-'):])
 captured.append(data)
 return sha(c.encoded(data))
def forbidden(*args,**kwargs):raise AssertionError('PROBE_OR_DISK_RESULT_WRITE_FORBIDDEN')
driver.registered=read_registered;driver.write_json=in_memory_output
driver.write_bytes=driver.collect=driver.send=driver.capture=forbidden
args=types.SimpleNamespace(reconcile=job/'sender.json',receiver_capture=capture,receiver_log=capture/'receiver.jsonl',receiver_summary=capture/'receiver.jsonl.summary.json',receiver_rc=None)
stdout=io.StringIO()
with contextlib.redirect_stdout(stdout):rc=driver.reconcile(args)
ck('registered-recompute-read-only-rc-zero',rc==0 and len(captured)==1)
delivered=json.loads(Path(receipt['record']['path']).read_bytes())
ck('entire-reconciled-result-exact-recomputed',captured[0]==delivered)
for protocol in ['tcp','udp']:ck('d9-mapping:'+protocol,delivered['cases'][protocol]['point']=='D9')
ck('certificate-and-gate-still-closed',delivered['production_gate']=='CLOSED' and delivered['certificate_written'] is False and delivered['full_surface_accepted'] is False)
save('reconciliation-independent.json',captured[0])
(a/'reconciliation-independent.stdout.txt').write_text(stdout.getvalue(),encoding='utf-8')
elapsed=sender_obj['observation']['elapsed_ns']
ck('post-attempt-exact-duration',elapsed==21000477800)
save('exact-observation.json',{'elapsed_ns':elapsed,'elapsed_seconds_exact':str(Fraction(elapsed,1000000000)),'scope':'OLD_LAN_REPLAY_NOT_NEW_EXPERIMENT'})
runtime=p/'reviews/witness-automation/runtime'
journal=json.loads((runtime/'journal.json').read_bytes());latest=json.loads((runtime/'latest.json').read_bytes())
ck('journal-matches-frozen-job',journal['jobs'][summary['logical_key']]['job']==str(job) and journal['jobs'][summary['logical_key']]['state']=='COMPLETE')
ck('runtime-latest-matches-frozen-summary',len(latest['results'])==1 and latest['results'][0]==summary)
ck('summary-adapter-exact',summary['adapter']==receipt and summary['package_sha256']==package_sha and summary['status']=='REGISTERED_RECONCILIATION_COMPLETE')
ck('summary-never-new-ipv6',summary['ipv6_D2_D8']=='GAP_DEFERRED_NONBLOCKING_PREPARATION' and summary['probe_emitted'] is False and summary['training_started'] is False)
ck('frozen-job-unchanged-by-review',job_before=={str(f.relative_to(job)).replace('\\','/'):sha(f.read_bytes()) for f in job.rglob('*') if f.is_file()})
save('job-binding.json',{'path':str(job),'manifest_sha256':sha((job/'delivery-manifest.json').read_bytes()),'artifacts':job_before,'read_only_unchanged':True})
for f in job.rglob('*'):
 if f.is_file():
  dest=a/'job-snapshot'/f.relative_to(job);dest.parent.mkdir(exist_ok=True,parents=True);dest.write_bytes(f.read_bytes())
for f in [ready_path,sync/(package_sha+'.zip')]:
 dest=a/'sync-arrival-snapshot'/f.name;dest.parent.mkdir(exist_ok=True,parents=True);dest.write_bytes(f.read_bytes())
for n in ['journal.json','latest.json']:(a/('consumer-runtime-'+n)).write_bytes((runtime/n).read_bytes())
w=p/'reviews/codex-supervision/2026-10-04-live-watch';heartbeat=json.loads((w/'latest.json').read_bytes())
save('observer-context.json',{'time':heartbeat['time'],'worker_pid':heartbeat['watcher_pid'],'process_observation':heartbeat['process_observation'],'core_drift':heartbeat['core_drift'],'source_sha256':sha((w/'watch_claude.py').read_bytes())})
ck('observer-repair-version-unchanged',sha((w/'watch_claude.py').read_bytes())=='bd29b8548f1f9318c0ebb537d68f12862f65180027b52504c7a8edbf4ca484d4')
ck('production-not-opened',json.loads((p/'reviews/codex-supervision/2026-10-07-continuous-math-review/CURRENT_STATUS.json').read_bytes())['production']=='CLOSED')
save('verification.json',{'run_id':rid,'checks':checks,'passed':len(checks),'failed':0,'local_consumption':'PASS_BOUND_JOB_AND_INPUT_BYTES','precheck':'PASS_RECOMPUTED','registered_reconciliation':'PASS_RECOMPUTED_EXACT_VALUE','cross_endpoint_origin_chain':'NEEDS_EVIDENCE_PUBLISHER_RECEIPT_CONFIG_AND_EXECUTION_OUTPUT','new_sandbox_experiment':False,'new_ipv6_evidence':False,'watch_deployment':'NOT_DEPLOYED_PER_AUTHOR_PENDING_ACTUAL_RECEIPTS','source_modified':False,'config_modified':False,'existing_28_tool_tests':'INHERITED_SAME_SOURCE_NOT_RERUN','source_package_sha256':package_sha,'config_sha256':sha(config_path.read_bytes())})
print(json.dumps({'passed':len(checks),'failed':0,'package_sha256':package_sha,'job_manifest_sha256':sha((job/'delivery-manifest.json').read_bytes()),'config_sha256':sha(config_path.read_bytes()),'actual_cross_endpoint_chain':'NEEDS_EVIDENCE','registered_recompute':'EXACT_MATCH'},indent=2))
