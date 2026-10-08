import json,copy,hashlib,re
from pathlib import Path
R=Path.cwd();D=R/'reviews/codex-supervision/2026-10-07-semantic-signature-supervision';OLD=R/'reviews/codex-supervision/2026-10-07-continuous-math-review/current-core';NEW=D/'effective-core-v2'
H=lambda b:hashlib.sha256(b).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
dense=lambda r:H(json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
math_hash=lambda r:H(json.dumps({k:r.get(k) for k in ['problem','solution','answer','scene_spec']},ensure_ascii=False,sort_keys=True).encode())
def write(p,obj):
 p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
assert H((OLD/'delivery-manifest.json').read_bytes())=='972bd216b713bec7c48896e8f144d999dd6385b8c0e3e00a4c0116dfd1bbca22'
old_refs=read(OLD/'current-index.json');bindings=[json.loads(x) for x in (OLD/'record-bindings.jsonl').read_text(encoding='utf8').splitlines() if x.strip()]
sources=read(OLD/'source-bindings.json');patch=read(D/'c18-revision-spec.json')
assert not NEW.exists();NEW.mkdir()
all_rows=[];new_sources=[];changed=[];old_record=None;new_record=None
for source in sources:
 oldp=R/source['path'];raw=oldp.read_bytes();assert H(raw)==source['sha256']
 local=oldp.relative_to(OLD)
 newp=NEW/local;newp.parent.mkdir(parents=True,exist_ok=True)
 lines=raw.splitlines(keepends=True)
 if source['group']=='selected_draft':
  for i,line in enumerate(lines):
   r=json.loads(line)
   if r['id']!='draft-c18-02':continue
   old_record=copy.deepcopy(r);before=dense(r)
   for field in ['problem','solution','answer','scene_spec','method','difficulty','variant_kind']:r[field]=patch[field]
   r['versioned_id']='codex-semantic-core-v2-20261007-draft-c18-02'
   r['draft_status']='CODEX-SEMANTIC-CORE-v2-NOT-ADMITTED'
   r['strict_review'].update({'math_content_sha256':math_hash(r),'math_review_evidence':(NEW/'exact-proof.json').relative_to(R).as_posix(),
      'verification_basis':'EXACT_SYMBOLIC_PROJECTION_INDUCTION_AND_REAL_DOMAIN_CASE_PROOF','core_math_verified':True,'text_math_fields_reviewed':True,
      'scene_text_reviewed':True,'render_verified':False,'admitted':False,'admission_disposition':'MATH_VALID_KNOWN_PAIR_REPAIRED_PENDING_GLOBAL_SEMANTIC_AND_ASSET_ACCEPTANCE'})
   r['revision_lineage']['current_core_v2']={'parent_record_sha256':before,'parent_math_sha256':math_hash(old_record),
      'parent_source_path':source['path'],'parent_source_sha256':source['sha256'],'historical_risk_not_reset':True,
      'reason':'Confirmed structural leakage with test-geom-024; replace static distance task with exact alternating projections; same id/count.'}
   new_record=copy.deepcopy(r);lines[i]=(json.dumps(r,ensure_ascii=False)+'\n').encode();changed.append(r['id'])
   raw=b''.join(lines)
 newp.write_bytes(raw);rel=newp.relative_to(R).as_posix()
 ns=copy.deepcopy(source);ns.update({'path':rel,'sha256':H(raw),'bytes':len(raw),'parent_source_path':source['path'],'parent_source_sha256':source['sha256']})
 new_sources.append(ns)
 records=[json.loads(l) for l in raw.splitlines() if l.strip()]
 refs=[x for x in bindings if x['path']==source['path']]
 assert len(refs)==len(records)==source['records']
 for ref,r in zip(refs,records):
  assert ref['id']==r['id']
  nr=copy.deepcopy(ref);nr.update({'path':rel,'source_sha256':H(raw),'record_sha256':dense(r),'math_sha256':math_hash(r)})
  if r['id']=='draft-c18-02':nr['patch_review']=(NEW/'exact-proof.json').relative_to(R).as_posix()
  else:assert nr['record_sha256']==ref['record_sha256'] and nr['math_sha256']==ref['math_sha256']
  all_rows.append(nr)
assert changed==['draft-c18-02'] and len(all_rows)==761 and len(new_sources)==24
(D/'c18-before.json').write_text(json.dumps(old_record,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
write(NEW/'c18-after.json',new_record)
write(NEW/'source-bindings.json',new_sources)
(NEW/'record-bindings.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in all_rows),encoding='utf8')
write(NEW/'current-index.json',{'schema':'current-core-successor-v2','records':761,'sources':24,'groups':{'train':47,'selected_draft':264,'eval':300,'test':150},
 'source_bindings_sha256':H((NEW/'source-bindings.json').read_bytes()),'record_bindings_sha256':H((NEW/'record-bindings.jsonl').read_bytes()),
 'parent_core':OLD.relative_to(R).as_posix(),'parent_manifest_sha256':H((OLD/'delivery-manifest.json').read_bytes()),'changed_ids':changed,
 'unchanged_record_bodies':760,'mathematical_review':'INHERITED_EXACT_760_PLUS_PENDING_NEW_1','semantic_isolation':'NOT_ESTABLISHED','production':'CLOSED'})
write(NEW/'inheritance-receipt.json',{'schema':'core-successor-inheritance-v1','parent_manifest_sha256':H((OLD/'delivery-manifest.json').read_bytes()),
 'id_count_preserved':761,'groups_preserved':True,'changed_record_ids':changed,'unchanged_full_record_sha256':760,
 'unchanged_math_sha256':760,'unchanged_source_files':23,'changed_source_files':1,'old_frozen_core_mutated':False,
 'known_pair':'draft-c18-02 / test-geom-024','pair_disposition':'CONFIRMED_BEFORE; REVISED_TASK_DISTINCT_FROM_PARALLEL_DISTANCE',
 'global_isolation':'NOT_ESTABLISHED','visual_and_native':'NOT_NEWLY_CERTIFIED','production':'CLOSED'})
print(json.dumps({'records':len(all_rows),'sources':len(new_sources),'changed':changed,'unchanged_bodies':760}))
