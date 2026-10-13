# Run archive; output paths are exclusive and must not be rerun into this frozen directory.

from pathlib import Path
from datetime import datetime,timezone
import json,subprocess,hashlib,importlib.util,collections
R=Path(r'D:\Animation-Model-Training')
O=R/'reviews/codex-supervision/2026-10-07-historical-gap-mail-review'
H=R/'reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol'
def put(name,value):
 with (O/name).open('x',encoding='utf-8',newline='\n') as f: f.write(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
cmd=[str(R/'.venv/Scripts/python.exe'),'-X','utf8','-B','-m','unittest','discover','-s','tests','-p','test_holdout_recyclebin_scan.py','-v']
p=subprocess.run(cmd,cwd=R,capture_output=True)
(O/'tests.stdout.txt').write_bytes(p.stdout);(O/'tests.stderr.txt').write_bytes(p.stderr)
put('tests-receipt.json',{'command':cmd,'cwd':str(R),'returncode':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest(),'test_scope':'metadata parsing and simulated I/O; no sandbox experiment'})
print('TEST',p.returncode,p.stderr.decode('utf-8','replace'))
assert p.returncode==0
cmd=[str(R/'.venv/Scripts/python.exe'),'-X','utf8','-B',str(R/'tools/holdout_recyclebin_scan.py'),'--root','D:/$Recycle.Bin','--target',str(R),'--target',r'D:\code']
p=subprocess.run(cmd,cwd=R,capture_output=True)
with (O/'recycle-current-snapshot.json').open('xb') as f:f.write(p.stdout)
(O/'recycle-current-snapshot.stderr.txt').write_bytes(p.stderr)
report=json.loads(p.stdout)
put('recycle-current-receipt.json',{'command':cmd,'returncode':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest(),'read_only_metadata':True,'status':report['status'],'metadata_files_seen':report['metadata_files_seen'],'parsed_records':report['parsed_records'],'matched_records':report['matched_records'],'error_count':len(report['errors']),'historical_non_deletion_proved':False})
print('SCAN',json.dumps({k:report[k] for k in ['status','metadata_files_seen','parsed_records','matched_records','errors']},ensure_ascii=False))
g=json.loads((H/'EXPECTED_VERSION_GAPS.json').read_text(encoding='utf-8-sig'))
c=json.loads((R/'reviews/2026-10-03-model-screening/screening-cleanup-manifest.json').read_text(encoding='utf-8-sig'))
cleanup={x['sha256']:x['path'] for x in c['files']}
rows=[json.loads(line) for line in (H/'reference-closure-complete-scope.jsonl').read_text(encoding='utf-8-sig').splitlines() if line]
overlay=[];counts=collections.Counter()
for v in g['versions']:
 digest=v['expected_sha256']
 if digest in cleanup:cat='SCREENING_REMOVAL_MANIFEST_REFERENCE'
 elif any('draft-selection' in s for s in v['claimed_paths']):cat='SELECTOR_VERSION_DRIFT_REFERENCE'
 elif any(s.startswith('batch-') for s in v['claimed_paths']):cat='BATCH_VERSION_DRIFT_REFERENCE'
 else:cat='LEGACY_RAW_MIGRATION_REFERENCE'
 refs=[r for r in rows if r.get('expected_sha256')==digest]
 currents={a['path']:a for r in refs for a in r.get('actual_current_paths',[])}
 actual=[]
 for rel,a in sorted(currents.items()):
  path=R/rel
  actual.append({'path':rel,'raw_sha256':hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None,'original_version_recovered':False})
 overlay.append({**v,'use_category':cat,'documentary_use_scope':'PARTIALLY_CORROBORATED_BY_PATH_AND_BOUND_MANIFEST','cleanup_manifest_path':'reviews/2026-10-03-model-screening/screening-cleanup-manifest.json' if digest in cleanup else None,'cleanup_entry_relative_path':cleanup.get(digest),'cleanup_time_declared':c['deleted_at'] if digest in cleanup else None,'current_alternate_versions':actual,'byte_recovery_status':'MATCHING_ORIGINAL_BYTES_NOT_FOUND','exposure_status':'UNKNOWN','historical_no_overlap_status':'NOT_ESTABLISHED','delete_actor':'UNKNOWN','closure_decision':'NOT_CLOSED_BY_IMPORT_CHRONOLOGY','needed_evidence': ['Original bytes with this exact SHA256, or independently bound lossless predecessor/input history sufficient to reconstruct the full mathematical task exposure scope','Per-role access/use record and same-core exclusion covering historical input and output content']})
 counts[cat]+=1
put('EXPECTED_VERSION_GAPS.followup.json',{'schema':'historical-gap-mail-followup-v1','base_path':str(H/'EXPECTED_VERSION_GAPS.json'),'base_raw_sha256':hashlib.sha256((H/'EXPECTED_VERSION_GAPS.json').read_bytes()).hexdigest(),'versions':overlay,'unique_versions':len(overlay),'categories':dict(counts),'original_version_recoveries_in_mail':0,'closures':0,'prior_file_untouched':True,'user_non_deletion_statement':{'provenance':'Claude Code relay in message616','text':'user says they have never deleted files','does_not_identify_another_actor':True}})
bindings=[]
for rel in ['tools/holdout_recyclebin_scan.py','tests/test_holdout_recyclebin_scan.py','MODEL_SHOOTOUT_PLAN.md','tools/screening_probe.py','tools/screening_qlora_probe.py','reviews/2026-10-03-model-screening/screening-cleanup-manifest.json','holdout-sources/SOURCES.md','holdout-sources/extracted/kaoyan-pool-v1-manifest.json']:
 f=R/rel
 bindings.append({'path':rel,'raw_sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
put('documentary-source-bindings.json',bindings)
for args,name in [(['log','--all','--diff-filter=A','--format=%H %aI %cI %s','--','holdout-sources/SOURCES.md','holdout-sources/extracted/kaoyan-pool-v1-manifest.json'],'source-first-commit.txt'),(['show','--format=fuller','--stat','521471419769f0d58dca28c18b7d24d939ecd46e'],'claude-latest-commit.txt')]:
 p=subprocess.run(['git','-C',str(R),*args],capture_output=True)
 (O/name).write_bytes(p.stdout)
 assert p.returncode==0
put('CURRENT_STATUS.json',{'time':datetime.now(timezone.utc).isoformat(),'mail616':'REVIEWED_WITH_CORRECTIONS','version_gaps':38,'version_gaps_closed':0,'purpose_evidence':'PARTIAL_DOCUMENTARY_CORROBORATION','historical_full_exposure_proof':'PENDING','qualified_count':None,'candidate_count':391,'core_judgments':0,'new_questions':0,'labels':0,'sandbox_experiments':0,'production_gate':'CLOSED','calibration_status':'UNCALIBRATED','recycle_snapshot_status':report['status'],'no_delete_actor_attribution':True})
print('OVERLAY',dict(counts))
