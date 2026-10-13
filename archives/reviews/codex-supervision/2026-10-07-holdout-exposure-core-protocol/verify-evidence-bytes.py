from pathlib import Path
import json,hashlib,datetime,subprocess,ast
R=Path(r'D:\Animation-Model-Training');O=R/'reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def rows(name):
 with (O/name).open(encoding='utf-8') as f:
  for line in f:
   if line.strip():yield json.loads(line)
checked=0;bytes_verified=0;cache={};mismatches=[]
for name in ['filesystem-inventory.jsonl','extra-filesystem-inventory.jsonl']:
 for row in rows(name):
  p=R/row['actual_bound_path']
  try:
   actual=digest(p)
   if actual!=row['sha256'] or p.stat().st_size!=row['bytes']:
    mismatches.append({'path':row['actual_bound_path'],'expected':row['sha256'],'actual':actual})
   else:
    checked+=1;bytes_verified+=row['bytes'];cache[row['actual_bound_path']]=actual
  except OSError as e:mismatches.append({'path':row['actual_bound_path'],'error':type(e).__name__})
print('all material byte rechecks',checked,'mismatches',len(mismatches),flush=True)
gitrows=list(rows('git-history-inventory.jsonl'))+read(O/'git-html-supplement.json')['rows']+list(rows('git-all-material-supplement.jsonl'))
git_checked=0
for row in gitrows:
 p=R/row['actual_bound_path'];b=p.read_bytes()
 assert hashlib.sha256(b).hexdigest()==row['sha256']
 assert hashlib.sha1(b'blob '+str(len(b)).encode('ascii')+b'\0'+b).hexdigest()==row['git_object_id']
 git_checked+=1
assert git_checked==1474
assert len(mismatches)==0,mismatches[:5]
assert checked==75739
registry=read(O/'canonicalization-registry.json')
assert len(registry['core_catalog_active_identity_checks'])==47 and all(x['identity_matches'] for x in registry['core_catalog_active_identity_checks'])
assert len(registry['selected_draft_raw_and_normalized_checks'])==18 and all(x['both_declared_hashes_match'] for x in registry['selected_draft_raw_and_normalized_checks'])
assert len(read(O/'workflow-296-row-bindings.json')['pairs'])==296
assert len(read(O/'b5-50-row-bindings.json')['pairs'])==50
assert sum(1 for _ in rows('active-497-row-bindings.jsonl'))==497
assert sum(1 for _ in rows('selected-264-row-bindings.jsonl'))==264
plan=read(O/'core-association-plan.json')
assert len(plan['families'])==46 and len(plan['candidates'])==391 and plan['decided_cells']==0
assert len({r['candidate_id'] for r in plan['candidates']})==391
defaults=read(O/'member-qualification-defaults.json')
assert len(defaults['members'])==391 and all(x['qualification']=='QUARANTINED_NOT_ELIGIBLE' and x['association_state']=='UNREVIEWED' for x in defaults['members'])
assert digest(R/'holdout-sources/extracted/kaoyan-triples.jsonl')=='39d0f1a1f16ef5ffc026ae58da887cc44ce8a8b4225bcd4f4da751e41c8e663d'
assert digest(R/'holdout-sources/extracted/kaoyan-pool-v1-manifest.json')=='a47009ab04e65b9d6a9e91dec5a2aa4bc33429f33c10572d4905e7b8f12bcb30'
older=[]
for folder,expected in [('2026-10-07-holdout-v2-review','2d5791c284cc6498e660253b622a4ba735319246addb6f6c11a5b218a8e4d4d5'),('2026-10-07-external-driver-supervision','fe360f67a071a70bc4015bd8446d7d8adbf302a1e0f52b763c277fe6d299f567')]:
 p=R/'reviews/codex-supervision'/folder/'delivery-manifest.json';assert digest(p)==expected
 m=read(p)
 for x in m['artifacts']:assert digest(R/x['path'])==x['sha256']
 older.append({'path':p.relative_to(R).as_posix(),'sha256':expected,'artifacts_match':True})
policy=read(R/'reviews/codex-supervision/2026-10-06-ipv4-joint-policy/delivery-manifest.json')
for source,expected in policy['implementation_bindings'].items():assert digest(R/source)==expected
cp=subprocess.run(['git','rev-parse','HEAD'],cwd=R,capture_output=True);assert cp.returncode==0
assert cp.stdout.decode('ascii').strip()==read(O/'git-history-scope.json')['head']
for p in O.glob('*.py'):ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
for p in O.glob('*.json'):read(p)
assert not (R/'data/execution_evidence.json').exists()
result={'schema':'holdout-evidence-verification-v1','time':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),
 'scope':'independent byte, object identity, schema and count verification only; no mathematical core adjudication',
 'material_files_verified':checked,'material_bytes_verified':bytes_verified,'git_blob_sha1_and_sha256_verified':git_checked,
 'mismatches':mismatches,'current_and_selected_counts_verified':True,'core_catalog_identity_checks':47,'old_deliveries':older,
 'current_15_implementation_bindings_unchanged':True,'candidate_pool_and_original_manifest_bytes_unchanged':True,
 'candidate_count':391,'associations_decided':0,'qualified_count':None,'historical_version_gaps':38,
 'native_experiments_started':0,'production_gate':'CLOSED','calibration_status':'UNCALIBRATED','certificate_exists':False}
with (O/'evidence-verification.json').open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False),flush=True)
