from pathlib import Path
import json, hashlib, subprocess, sys, importlib.util
from datetime import datetime, timezone, timedelta
p=Path(r'D:\Animation-Model-Training')
a=p/'archives/reviews/codex-supervision/2026-10-16-onedrive-config-review'
assert not a.exists()
a.mkdir()
def sha(raw): return hashlib.sha256(raw).hexdigest()
def save(name,obj): (a/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
save('ownership-receipt.json',json.loads("{\"request\":{\"from\":\"codex\",\"to\":\"claude-code\",\"type\":\"review\",\"metadata\":{\"mail_run_id\":\"run-1a69298c8f5d4c99b554c07bbd1ce78f\"},\"content\":\"\u63a5\u624b msg_1792149832314_825 \u7684\u63a5\u5165\u51c6\u5907\u590d\u6838\u3002\u53d1\u73b0 configs/witness_automation.local.json \u5f53\u524d\u672a\u88ab Git \u5ffd\u7565\uff1bCodex \u5c06\u4ec5\u4fee\u6539 .gitignore \u589e\u52a0\u8be5\u5177\u540d\u672c\u5730\u914d\u7f6e\u6392\u9664\u9879\uff0c\u4fdd\u7559 example \u548c\u4f60\u7684 local \u914d\u7f6e\u5b57\u8282\u4e0d\u52a8\uff0c\u5e76\u6838\u9a8c registry \u539f\u59cb SHA/PLAN \u884c\u4e3a\u3002\u8bf7\u6682\u4e0d\u5e76\u6539 .gitignore\u3002PLAN/rc3 \u5165\u53e3\u4e0d\u52a0\u8f7d\u914d\u7f6e\uff0c\u4e0d\u80fd\u636e\u6b64\u8ba4\u5b9a\u914d\u7f6e\u53ef\u6267\u884c\u6216 OneDrive \u540c\u6b65\u5df2\u9a8c\u8bc1\uff1b\u4e09\u5b9e\u9645\u8def\u5f84\u53ca\u5171\u4eab\u6743\u9650\u4ecd\u5f85\u660e\u786e\u3002\u4e0d\u4f1a\u542f\u52a8\u91c7\u96c6\u3001\u63a2\u9488\u6216\u540e\u53f0\u540c\u6b65\u3002\"},\"response\":{\"content\":[{\"type\":\"text\",\"text\":\"{\\n  \\\"status\\\": \\\"sent\\\",\\n  \\\"message\\\": {\\n    \\\"id\\\": \\\"msg_1792150284658_826\\\",\\n    \\\"from\\\": \\\"codex\\\",\\n    \\\"to\\\": \\\"claude-code\\\",\\n    \\\"type\\\": \\\"review\\\",\\n    \\\"content\\\": \\\"\u63a5\u624b msg_1792149832314_825 \u7684\u63a5\u5165\u51c6\u5907\u590d\u6838\u3002\u53d1\u73b0 configs/witness_automation.local.json \u5f53\u524d\u672a\u88ab Git \u5ffd\u7565\uff1bCodex \u5c06\u4ec5\u4fee\u6539 .gitignore \u589e\u52a0\u8be5\u5177\u540d\u672c\u5730\u914d\u7f6e\u6392\u9664\u9879\uff0c\u4fdd\u7559 example \u548c\u4f60\u7684 local \u914d\u7f6e\u5b57\u8282\u4e0d\u52a8\uff0c\u5e76\u6838\u9a8c registry \u539f\u59cb SHA/PLAN \u884c\u4e3a\u3002\u8bf7\u6682\u4e0d\u5e76\u6539 .gitignore\u3002PLAN/rc3 \u5165\u53e3\u4e0d\u52a0\u8f7d\u914d\u7f6e\uff0c\u4e0d\u80fd\u636e\u6b64\u8ba4\u5b9a\u914d\u7f6e\u53ef\u6267\u884c\u6216 OneDrive \u540c\u6b65\u5df2\u9a8c\u8bc1\uff1b\u4e09\u5b9e\u9645\u8def\u5f84\u53ca\u5171\u4eab\u6743\u9650\u4ecd\u5f85\u660e\u786e\u3002\u4e0d\u4f1a\u542f\u52a8\u91c7\u96c6\u3001\u63a2\u9488\u6216\u540e\u53f0\u540c\u6b65\u3002\\\",\\n    \\\"metadata\\\": {\\n      \\\"mail_run_id\\\": \\\"run-1a69298c8f5d4c99b554c07bbd1ce78f\\\"\\n    },\\n    \\\"timestamp\\\": \\\"2026-10-16T11:31:24.658Z\\\",\\n    \\\"read\\\": false\\n  }\\n}\"}]}}"))
ignore=p/'.gitignore'; local=p/'configs/witness_automation.local.json'; example=p/'configs/witness_automation.example.json'
original=ignore.read_bytes(); config_raw=local.read_bytes(); example_raw=example.read_bytes()
(a/'gitignore.before').write_bytes(original)
(a/'local-config.reviewed.json').write_bytes(config_raw)
checks=[]
def ck(name,condition,detail=None):
 checks.append({'name':name,'passed':bool(condition),'detail':detail})
 assert condition,name
for path in [ignore,local]:
 ck('mutable-no-frozen-ancestor:'+path.name,not any((x/'delivery-manifest.json').is_file() for x in [path.parent,*path.parents] if x.is_relative_to(p)))
 ck('ordinary-file:'+path.name,not any(x.exists() and x.lstat().st_file_attributes & 1024 for x in [path,*path.parents]))
rule=b'/configs/witness_automation.local.json'
ck('local-rule-not-already-present',rule not in original.splitlines())
eol=b'\r\n' if b'\r\n' in original else b'\n'
after=original+(b'' if original.endswith(b'\n') else eol)+eol+b'# Machine-local witness paths and sender approval bindings'+eol+rule+eol
ck('gitignore-before-write-unchanged',ignore.read_bytes()==original)
ignore.write_bytes(after)
(a/'gitignore.after').write_bytes(after)
cfg=json.loads(config_raw); ex=json.loads(example_raw)
without=dict(cfg); without['sender_registry']=[]
ck('only-registry-differs-from-example',without==ex)
ck('inactive-and-forbidden-actions',cfg['active'] is False and all(cfg[k] is False for k in ['allow_probe_emission','allow_training_start','allow_frozen_archive_writes']) and cfg['production']=='CLOSED')
ck('three-unapproved-paths-stay-null',cfg['consumer']['sync_root'] is cfg['witness']['capture_root'] is cfg['witness']['sync_root'] is None)
sys.path.insert(0,str(p/'tools'))
import witness_transfer_common as c
import witness_registered_adapter as adapter
ck('config-read-schema',c.load_config(local)==cfg)
for role in ['consumer','witness']:
 try:
  c.load_config(local,execute=True,role=role)
 except c.TransferError as err:
  ck('inactive-refused-before-io:'+role,err.code=='CONFIG_INACTIVE',str(err))
 else: ck('inactive-refused-before-io:'+role,False)
for group in ['automation_source_pins','v3_source_pins']:
 for rel,digest in cfg[group].items():
  f=p/rel if rel!='witness_receiver_v3.exe' else p/'reviews/codex-supervision/2026-10-09-witness-input-hardening/release/witness_receiver_v3.exe'
  ck('source-pin:'+rel,sha(f.read_bytes())==digest,{'sha256':digest,'bytes':f.stat().st_size})
ck('registry-exactly-one',len(cfg['sender_registry'])==1)
entry=cfg['sender_registry'][0]
sender,raw_bytes,raw,bindings=adapter.binding_inputs(entry)
ck('registry-validator-accepts-six-original-inputs',len(bindings)==6,bindings)
proof_path=sender.parent/'captures'/(entry['round']+'-'+entry['receiver_capture_id'])/'process-exit.json'
proof=json.loads(proof_path.read_bytes())
ck('original-capture-identity', (proof['round'],proof['capture_id'],proof['receiver_run_id'])==(entry['round'],entry['receiver_capture_id'],entry['expected_receiver_run_id']))
ck('old-replay-not-new-experiment',entry['round']=='lan-2026-10-13-a')
def runtime_snapshot():
 roots=[p/'reviews/witness-automation',p/'tools',p/'configs']
 rows={}
 for root in roots:
  if root.exists():
   for f in root.rglob('*'):
    if f.is_file() and not f.lstat().st_file_attributes & 1024:
     rows[str(f.relative_to(p))]={'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())}
 return rows
before=runtime_snapshot()
plan=[]
for tool in ['witness_pack.py','witness_consumer.py']:
 for config_path,kind in [(local,'local'),(p/'configs/__codex_nonexistent_plan_only__.json','absent-negative-control')]:
  result=subprocess.run([sys.executable,'-X','utf8','-B',str(p/'tools'/tool),'--config',str(config_path)],cwd=p,capture_output=True)
  row={'tool':tool,'config_kind':kind,'returncode':result.returncode,'stdout':result.stdout.decode('utf-8'),'stderr':result.stderr.decode('utf-8')}
  plan.append(row)
  out=json.loads(result.stdout)
  ck('plan-contract:'+tool+':'+kind,result.returncode==3 and out['status']=='PLAN' and out['probe_emitted'] is False and out['cloud_write'] is False and not result.stderr)
ck('plan-no-artifact-or-source-byte-changes',runtime_snapshot()==before)
ck('local-config-unchanged',local.read_bytes()==config_raw,sha(config_raw))
ck('example-config-unchanged',example.read_bytes()==example_raw,sha(example_raw))
res=subprocess.run(['git','check-ignore','-v','--','configs/witness_automation.local.json'],cwd=p,capture_output=True)
save('git-check-ignore.json',{'returncode':res.returncode,'stdout':res.stdout.decode('utf-8'),'stderr':res.stderr.decode('utf-8')})
ck('local-config-now-ignored',res.returncode==0 and rule.decode() in res.stdout.decode('utf-8'))
res=subprocess.run(['git','diff','--check','--','.gitignore'],cwd=p,capture_output=True)
ck('git-diff-check',res.returncode==0)
(a/'gitignore.diff').write_bytes(subprocess.run(['git','diff','--','.gitignore'],cwd=p,capture_output=True).stdout)
save('plan-smoke.json',plan)
save('runtime-before.json',before)
save('runtime-after.json',runtime_snapshot())
o=p/'reviews/codex-supervision/2026-10-04-live-watch'
heartbeat=json.loads((o/'latest.json').read_bytes())
save('context-status.json',{'observed_at':datetime.now(timezone(timedelta(hours=8))).isoformat(),'observer_time':heartbeat.get('time'),'observer_pid':heartbeat.get('watcher_pid'),'observer_head':heartbeat.get('head'),'observer_current_live_status':'NOT_ESTABLISHED_STALE_HEARTBEAT','event_tail':[json.loads(s) for s in (o/'events.jsonl').read_text(encoding='utf-8-sig').splitlines()[-3:]],'math_status_sha256':sha((p/'reviews/codex-supervision/2026-10-07-continuous-math-review/CURRENT_STATUS.json').read_bytes()),'production':'CLOSED','semantic_isolation':'NOT_ESTABLISHED','native_sandbox':'UNVERIFIED'})
save('verification.json',{'schema':'onedrive-local-config-review-v1','checks':checks,'passed':len(checks),'failed':0,'source_changed':False,'local_config_sha256':sha(config_raw),'example_config_sha256':sha(example_raw),'gitignore_before_sha256':sha(original),'gitignore_after_sha256':sha(after),'qualification':'PASS_LOCAL_INACTIVE_CONFIG_AND_IGNORE_REPAIR_ONLY','actual_onedrive_sync':'NEEDS_EVIDENCE','prior_28_tool_tests':'INHERITED_UNCHANGED_NAMED_SOURCE_PINS_NOT_RERUN'})
print(json.dumps({'archive':str(a),'passed':len(checks),'config_sha256':sha(config_raw),'gitignore_sha256':sha(after)},indent=2))
