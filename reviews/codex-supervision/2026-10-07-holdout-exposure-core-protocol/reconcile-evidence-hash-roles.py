from pathlib import Path
import json,hashlib,collections,stat,subprocess
R=Path(r'D:\Animation-Model-Training');O=R/'reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1<<20),b''):h.update(chunk)
 return h.hexdigest()
def digest(b):return hashlib.sha256(b).hexdigest()
def write(name,obj):
 with (O/name).open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def dense(obj):return digest(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8'))
fs=[json.loads(x) for x in (O/'filesystem-inventory.jsonl').read_text(encoding='utf-8').splitlines()]
git=[json.loads(x) for x in (O/'git-history-inventory.jsonl').read_text(encoding='utf-8').splitlines()]
by_sha=collections.defaultdict(set)
for x in fs+git:by_sha[x['sha256']].add(x['actual_bound_path'])

for x in read(O/'git-html-supplement.json')['rows']:by_sha[x['sha256']].add(x['actual_bound_path'])
# Prefer actual archival-byte fields over normalized-content hash fields.
anchor=read(O/'anchor-bindings.json')
sources=sorted(set(anchor['supervision_manifest_paths']+[x['path'] for x in anchor['anchors']]))
refs=[];new_material=[]
migration=read(R/'reviews/codex-supervision/2026-10-04-artifact-migration/path-mapping.json')
old_prefix=migration['old_prefix'];new_prefix=migration['new_prefix']
def references(obj,parent_algorithm=None,location='$'):
 if isinstance(obj,dict):
  alg=obj.get('hash_algorithm',parent_algorithm)
  for k,v in obj.items():
   if isinstance(v,str) and (k=='path' or k.endswith('_path')):
    stem='' if k=='path' else k[:-5]
    raw_key='raw_sha256' if not stem else stem+'_raw_sha256'
    general_key='sha256' if not stem else stem+'_sha256'
    key=raw_key if isinstance(obj.get(raw_key),str) else general_key
    val=obj.get(key)
    if isinstance(val,str) and len(val)==64 and all(c in '0123456789abcdef' for c in val):
     algorithm=obj.get((stem+'_hash_algorithm') if stem else 'hash_algorithm',alg)
     yield location+'.'+k,v,val,'RAW_BYTES' if key==raw_key else 'DECLARED_GENERIC',algorithm
   if isinstance(v,(dict,list)):yield from references(v,alg,location+'.'+k)
 elif isinstance(obj,list):
  for i,v in enumerate(obj):yield from references(v,parent_algorithm,location+'['+str(i)+']')
def candidate_paths(logical,referrer):
 text=logical
 if text.lower().startswith(old_prefix.lower()):text=new_prefix+text[len(old_prefix):]
 p=Path(text)
 base=[p] if p.is_absolute() else [R/p,(R/referrer).parent/p,R/'reviews/2026-10-05-training-diversity-drafts'/p,R/'data'/p]
 result=[]
 for x in base:
  try:
   z=x.resolve()
   if not z.is_relative_to(R.resolve()) or not z.is_file():continue
   if any(bool(a.stat(follow_symlinks=False).st_file_attributes&stat.FILE_ATTRIBUTE_REPARSE_POINT) for a in [z,*list(z.parents)[:len(z.relative_to(R).parts)-1]]):continue
   if z not in result:result.append(z)
  except (OSError,ValueError):pass
 return result
for source in sources:
 p=R/source
 if p.suffix!='.json':continue
 obj=read(p)
 for pointer,logical,expected,role,algorithm in references(obj):
  matches=sorted(by_sha.get(expected,set()))
  actual=[];normalized=[]
  # Explicit file references outside the general inventory are bound without broadening it.
  for target in candidate_paths(logical,source):
   if target.suffix=='.safetensors':
    actual.append({'path':target.relative_to(R).as_posix(),'status':'MODEL_WEIGHT_REFERENCE_OUTSIDE_QUESTION_MATERIAL_SCOPE'})
    continue
   checksum=sha(target)
   actual.append({'path':target.relative_to(R).as_posix(),'raw_sha256':checksum})
   if checksum==expected:
    matches.append(target.relative_to(R).as_posix());by_sha[checksum].add(target.relative_to(R).as_posix())
    new_material.append({'path':target.relative_to(R).as_posix(),'actual_bound_path':target.relative_to(R).as_posix(),'sha256':checksum,'bytes':target.stat().st_size})
   elif role=='DECLARED_GENERIC' and algorithm=='sha256-utf8-sig-splitlines-lf-v1':
    text=target.read_text(encoding='utf-8-sig')
    b='\n'.join(text.splitlines()).encode('utf-8')
    if digest(b)==expected:
     normalized.append({'path':target.relative_to(R).as_posix(),'normalization_algorithm':algorithm,'normalized_sha256':expected,'raw_sha256':checksum})
  state='EXACT_RAW_BYTES_AVAILABLE' if matches else 'NORMALIZED_CONTENT_BOUND_RAW_SEPARATE' if normalized else 'MODEL_WEIGHT_REFERENCE_OUTSIDE_QUESTION_MATERIAL_SCOPE' if logical.endswith('.safetensors') else 'EXPECTED_HASH_UNRESOLVED'
  refs.append({'referring_path':source,'json_pointer_label':pointer,'claimed_path':logical,'expected_sha256':expected,'expected_hash_role':role,
       'declared_algorithm':algorithm,'actual_matching_raw_paths':sorted(set(matches)),'normalized_bindings':normalized,'actual_current_paths':actual,'status':state})
with (O/'reference-closure-final.jsonl').open('x',encoding='utf-8',newline='\n') as f:
 for row in refs:f.write(json.dumps(row,ensure_ascii=False,separators=(',',':'))+'\n')
# Current source identity check using verified, distinct canonicalization.
core=read(R/'reviews/2026-10-06-core-families/core-families.corrected-v2.json')
packet=read(R/core['source_packet_path'])
active=read(R/'data/manifest.json');records={}
for entry in active['entries']:
 if entry['split']=='train':
  for x in (R/'data'/entry['path']).read_text(encoding='utf-8-sig').splitlines():
   record=json.loads(x);records[record['id']]=record
checks=[]
for row in core['record_core_reviews']:
 current=records[row['id']]
 checks.append({'id':row['id'],'core_catalog_record_sha256':row['record_canonical_sha256'],'current_dense_record_sha256':dense(current),'identity_matches':dense(current)==row['record_canonical_sha256'],'mathematical_association_judged':False})
assert len(checks)==47 and all(x['identity_matches'] for x in checks)
selector=read(R/'reviews/2026-10-05-training-diversity-drafts/draft-selection.json')
normalchecks=[]
for row in selector['entries']:
 p=R/row['root_path']
 checksum=sha(p)
 normalized=digest('\n'.join(p.read_text(encoding='utf-8-sig').splitlines()).encode('utf-8'))
 assert checksum==row['raw_sha256'] and normalized==row['sha256']
 normalchecks.append({'path':row['root_path'],'raw_sha256':checksum,'normalized_sha256':normalized,'both_declared_hashes_match':True})
write('canonicalization-registry.json',{'schema':'evidence-hash-roles-v1',
 'pool_and_new_inventory_record_canonical':'json.dumps(ensure_ascii=False,sort_keys=True); default separators; UTF-8',
 'core_catalog_and_source_packet_record_canonical':'holdout_contract.object_sha: sorted keys, ensure_ascii=False, separators=(comma,colon); UTF-8',
 'core_packet_raw_line_sha256':packet['hash_algorithms']['raw_line_sha256'],
 'new_row_raw_line_with_terminator_sha256':'exact original line bytes including its original line terminator',
 'selector_content_hash':'sha256-utf8-sig-splitlines-lf-v1: decode utf-8-sig, splitlines, join LF, without adding a final LF, encode UTF-8',
 'selector_raw_hash':'sha256 of original file bytes; never replace with normalized hash',
 'core_catalog_active_identity_checks':checks,'selected_draft_raw_and_normalized_checks':normalchecks,
 'identity_comparison_is_not_core_association':True})
workflow=read(R/'reviews/2026-10-06-linalg048-admission/v3-receipt-bound/semantic-review-workflow-v1.json')
assert len(workflow['pairs'])==296
write('workflow-296-row-bindings.json',{'schema':'historical-workflow-pair-bindings-v1','source_path':'reviews/2026-10-06-linalg048-admission/v3-receipt-bound/semantic-review-workflow-v1.json',
 'source_raw_sha256':sha(R/'reviews/2026-10-06-linalg048-admission/v3-receipt-bound/semantic-review-workflow-v1.json'),
 'bound_reviewer_claim':workflow.get('reviewer'),'pairs':[{'index':i,'id':p.get('id'),'split':p.get('split'),'problem_sha256_claim':p.get('problem_sha256'),'complete_pair_canonical_sha256':dense(p),'historical_verdict':p.get('verdict')} for i,p in enumerate(workflow['pairs'])],
 'new_associations_decided':0,'qualification_proof':False})
b5=read(R/'data/b5-annotation-set/b5-annotation-set.json')
write('b5-50-row-bindings.json',{'source_path':'data/b5-annotation-set/b5-annotation-set.json','source_raw_sha256':sha(R/'data/b5-annotation-set/b5-annotation-set.json'),
 'pairs':[{'index':i,'a':p['a'],'b':p['b'],'complete_pair_canonical_sha256':dense(p),'historical_label':p.get('label')} for i,p in enumerate(b5['pairs'])],
 'source_rows':len(b5['pairs']),'new_associations_decided':0,'note':'raw historical B5 row count; not the count of adjudicable calibration pairs'})
write('additional-explicit-file-bindings.json',{'rows':list({x['path']:x for x in new_material}.values())})
counts=dict(collections.Counter(x['status'] for x in refs))
unresolved=[x for x in refs if x['status']=='EXPECTED_HASH_UNRESOLVED']
write('reference-resolution-summary.json',{'schema':'reference-resolution-summary-v2','first_pass_correction':'Prefer archival raw_sha256 to normalized content sha256; preserve initial first-pass output.',
 'reference_count':len(refs),'states':counts,'unresolved':unresolved,'all_current_selector_source_raw_bindings_verified':True,
 'all_47_core_catalog_current_record_identities_verified':True,'mathematical_core_associations_decided':0,
 'declared_material_scope_bound':True,'all_historical_exposure_proven':False,'qualified_count':None})
# New final builder archive with corrected extraction, preserving initial source.
initial=R/'reviews/codex-supervision/2026-10-07-holdout-v2-review/build-evidence-inventory.staging.py'
source=initial.read_text(encoding='utf-8')
(O/'build-evidence-inventory.initial.py').write_bytes(initial.read_bytes())
fixed=source.replace('"watcher.lock"}','"watcher.lock","watch.lock"}').replace('["sha256","raw_sha256"]','["raw_sha256","sha256"]')
with (O/'build-evidence-inventory.py').open('x',encoding='utf-8',newline='\n') as f:f.write(fixed)
print(json.dumps({'references_v2':len(refs),'states':counts,'core_catalog_identity_checks':47,'selector_double_hash_checks':18,'workflow_rows':296,'b5_raw_rows':len(b5['pairs']),'html_versions_bound':len(read(O/'git-html-supplement.json')['rows']),'unresolved_question_material_references':len(unresolved)},ensure_ascii=False))
