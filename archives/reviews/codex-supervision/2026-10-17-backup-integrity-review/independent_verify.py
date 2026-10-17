import json,hashlib,shutil
from pathlib import Path
R=Path(r'D:\Animation-Model-Training');A=R/'archives/reviews/codex-supervision/2026-10-17-backup-integrity-review'
H=R/'reviews/data-prep/2026-10-17-submission/backup-evidence';D=Path(r'D:\backups\animtrain\2026-10-17-training-data')
sha=lambda b:hashlib.sha256(b).hexdigest()
enc=lambda x:json.dumps(x,ensure_ascii=True,sort_keys=True,separators=(',',':')).encode()
audit=json.loads((A/'current-input-audit/audit.json').read_bytes());done=json.loads((A/'current-input-audit/COMPLETE.json').read_bytes())
assert audit['status']=='PASS_CURRENT_MANIFEST_INPUTS_ONLY' and len(audit['records'])==10
raw=(A/'current-input-audit/audit.json').read_bytes();assert sha(raw)==done['artifact']['sha256'] and len(raw)==done['artifact']['bytes']
assert audit['verifier_sha256']==sha((H/'verify_training_backup.py').read_bytes())
sourcepins={}
for row in audit['records']:
 source=R/row['path'];destination=D/row['path']
 for path,key,size in [(source,'source_sha256','source_bytes'),(destination,'destination_sha256','destination_bytes')]:
  before=path.stat()
  with path.open('rb') as f:digest=hashlib.file_digest(f,'sha256').hexdigest()
  after=path.stat();assert before.st_size==after.st_size==row[size] and before.st_mtime_ns==after.st_mtime_ns
  assert digest==row[key]
 assert row['source_sha256']==row['destination_sha256'] and row['status']=='PASS'
 sourcepins[row['path']]={'sha256':row['source_sha256'],'bytes':row['source_bytes']}
manifest=json.loads((R/'data/manifest.json').read_bytes())
expected={'data/'+e['path'].replace('\\','/') for e in manifest['entries']}|{'data/manifest.json','data/asset_evidence.json','configs/training_diversity_policy.json','configs/train_loop.example.json'}
assert {x['path'] for x in audit['records']}==expected
whole=json.loads((A/'whole-backup-attempt/audit.json').read_bytes())
assert whole['status']=='ERROR' and 'inventory_budget_exceeded' in whole['error']
assert audit['original_robocopy_returncodes']is None and audit['whole_backup']=='UNVERIFIED_RESOURCE_LIMIT'
W=R/'reviews/codex-supervision/2026-10-17-auto-start/runs/start-3237566e34da41fca8d3b28ab7fbbe55'
packet=json.loads((W/'signals.json').read_bytes());ids={x['detail']['tool_id'] for x in packet['signals'] if x['kind']=='PROJECT_TOOL_USE'}
L=Path(r'C:\Users\Jacap\.claude\projects\d--code\ee005e1f-71f1-4697-a746-054f6399acd6.jsonl')
with L.open('rb') as f:f.seek(max(0,L.stat().st_size-2*1024*1024));f.readline();lines=f.readlines()
mapped=[]
for raw in lines:
 try:obj=json.loads(raw)
 except Exception:continue
 content=obj.get('message',{}).get('content',[])
 if not isinstance(content,list):continue
 for x in content:
  if isinstance(x,dict) and x.get('id') in ids:
   inp=x.get('input',{});mapped.append({'tool_id':x['id'],'name':x.get('name'),'input':inp,'input_sha256':sha(enc(inp))})
assert {x['tool_id'] for x in mapped}==ids
(A/'activity-mapping.json').write_bytes(enc({'tool_records':mapped,'process_signals':[x for x in packet['signals'] if x['kind']!='PROJECT_TOOL_USE'],'log_commands_executed_by_codex':False})+b'\n')
for name in ['verify_training_backup.py','test_backup_audit.py']:
 raw=(H/name).read_bytes();sourcepins[(H/name).relative_to(R).as_posix()]={'sha256':sha(raw),'bytes':len(raw)}
(A/'current-source-bindings.json').write_bytes(enc(sourcepins)+b'\n')
watch=json.loads((R/'reviews/codex-supervision/2026-10-04-live-watch/latest.json').read_bytes())
(A/'observer-summary.json').write_bytes(enc({k:watch.get(k) for k in ['time','head','child_jobs','core_drift']})+b'\n')
verification={'status':'PASS_CURRENT_TEN_INPUT_FILES_ONLY','files':len(audit['records']),'bytes':audit['source_bytes'],
 'alternate_hash_method':'hashlib.file_digest','checks':{'source_backup_hashes':True,'manifest_file_set_exact':True,'snapshot_metadata_stable':True,'output_integrity':True,'verifier_pin':True},
 'whole_backup':'UNVERIFIED_RESOURCE_LIMIT','holdout_sources':'NOT_AUDITED',
 'original_copy_returncodes':'NOT_RECORDED','mapped_tool_ids':len(ids),'mapped_log_records':len(mapped),
 'backup_or_source_writes_performed':False,'scope':'This verification only reads observed project backup files; does not authorize copying or altering backups.'}
(A/'independent-verification.json').write_bytes(enc(verification)+b'\n')
print(json.dumps(verification))
