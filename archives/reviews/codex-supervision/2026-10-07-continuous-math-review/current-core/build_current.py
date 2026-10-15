"""Compose current reviewed candidates; never overwrite a different existing artifact."""
import json,hashlib,pathlib,copy,re,sys
REPLACE="--replace-unfrozen" in sys.argv
ROOT=pathlib.Path(__file__).resolve().parents[4]
OUT=pathlib.Path(__file__).resolve().parent
BASE=OUT.parent
PRIOR=ROOT/'reviews/codex-supervision/2026-10-07-math-batch-supervision'
def sha(b): return hashlib.sha256(b).hexdigest()
def dense(o): return sha(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def mathsha(o): return sha(json.dumps({k:o.get(k) for k in ('problem','solution','answer','scene_spec')},ensure_ascii=False,sort_keys=True).encode())
def save(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists() and p.read_bytes()!=b and not (REPLACE and not (OUT/'delivery-manifest.json').exists()): raise ValueError('Refuse overwrite: '+str(p))
 if not p.exists() or (REPLACE and not (OUT/"delivery-manifest.json").exists()): p.write_bytes(b)
def dump(p,o): save(p,(json.dumps(o,ensure_ascii=False,indent=2)+'\n').encode())
def rel(p): return p.relative_to(ROOT).as_posix()
pins=[
(PRIOR/'delivery-manifest.json','f3bb6661de2c026938a21bb712c99926b521941c1faad20da82dd0b3d6fa8f13'),
(BASE/'draft-delivery-manifest.json','df1826e6cf927ee3983c4596d5556bbf674db1e56a32e48618085b305a9197fd'),
(BASE/'eval-review/eval-delivery-manifest.json','8e28eefc8353c1b4009159a3d153f545e13b104b5a3dd96eb4d1919f2f11c166'),
(BASE/'test-review/test-delivery-manifest.json','00213933fd4db9f79d90d39553153cbf7ba87dd31b2ec5da030ee46a871af55d')]
parent_manifests=[]
for p,h in pins:
 assert sha(p.read_bytes())==h,rel(p)
 j=json.loads(p.read_text(encoding='utf-8-sig'))
 for item in j['artifacts']:
  f=p.parent/item['path'];b=f.read_bytes()
  assert sha(b)==item.get('sha256',item.get('raw_sha256')) and len(b)==item['bytes'],str(f)
 parent_manifests.append({'path':rel(p),'sha256':h,'artifacts_verified':len(j['artifacts'])})
reviews={}
reviewpaths=[PRIOR/'independent-review-38.jsonl',ROOT/'reviews/codex-supervision/2026-10-07-core-verifier-followup/admission-v2/record-bindings.jsonl',BASE/'independent-draft-review-264.jsonl',BASE/'eval-review/independent-eval-review-291.jsonl',BASE/'test-review/independent-test-review-138.jsonl']
for p in reviewpaths:
 for i,l in enumerate(p.read_text(encoding='utf8').splitlines(),1):
  r=json.loads(l);assert r['id'] not in reviews
  reviews[r['id']]={'path':rel(p),'line':i,'sha256':sha(p.read_bytes()),'record_sha256':r.get('candidate_record_sha256',r.get('final_record_dense_sha256'))}
assert len(reviews)==761
roots=[(PRIOR/'candidate-sources/data/v2/train','train'),(BASE/'candidate-sources','selected_draft'),(BASE/'eval-review/candidate-sources','eval'),(BASE/'test-review/candidate-sources','test')]
specs={r['id']:r for r in json.loads((OUT/'patch-specifications.json').read_text(encoding='utf8'))}
sources=[];records=[];patches=[];seen=set()
for source_root,group in roots:
 for p in sorted(source_root.rglob('*.jsonl')):
  if group=='train': target='data/v2/train/'+p.relative_to(source_root).as_posix()
  else: target=p.relative_to(source_root).as_posix()
  raw=p.read_bytes();outlines=[]
  for i,line in enumerate(raw.splitlines(keepends=True),1):
   r=json.loads(line);rid=r['id'];assert rid not in seen;seen.add(rid)
   assert dense(r)==reviews[rid]['record_sha256'],rid
   before=copy.deepcopy(r)
   if rid in specs:
    r.update(copy.deepcopy(specs[rid]['fields']))
    r['versioned_id']='codex-current-core-v1-20261007-'+rid
    r['admitted']=False;r['animation_render_verified']=False
    r['review_status']='CODEX_MATH_AND_SCENE_TEXT_REVIEWED_PENDING_GLOBAL_ISOLATION'
    sr=r.setdefault('strict_review',{})
    sr.update({'core_math_verified':True,'text_math_fields_reviewed':True,'scene_text_reviewed':True,'math_content_sha256':mathsha(r),'math_review_evidence':rel(OUT/'patch-review.json'),'render_verified':False,'admitted':False,'verification_basis':'CURRENT_EXACT_PATCH_PROOF_AND_SCENE_TEXT_REVIEW'})
    r['current_revision_lineage']={'parent_path':rel(p),'parent_raw_sha256':sha(raw),'parent_record_sha256':dense(before),'reason':specs[rid]['reason'],'native_render':'UNVERIFIED','semantic_isolation':'NOT_ESTABLISHED'}
    if 'draft_status' in r:r['draft_status']='CODEX-CURRENT-CORE-v1-NOT-ADMITTED'
    line=(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n').encode()
    patches.append({'id':rid,'reason':specs[rid]['reason'],'before':before,'after':r,'before_record_sha256':dense(before),'after_record_sha256':dense(r),'after_math_sha256':mathsha(r)})
   outlines.append(line)
   records.append({'id':rid,'group':group,'path':rel(OUT/'candidate-sources'/target),'source_line':i,'record_sha256':dense(r),'math_sha256':mathsha(r),'parent_review':reviews[rid],'patch_review':rel(OUT/'patch-review.json') if rid in specs else None})
  out=OUT/'candidate-sources'/target;data=b''.join(outlines);save(out,data)
  sources.append({'path':rel(out),'sha256':sha(data),'bytes':len(data),'records':len(outlines),'group':group,'parent_path':rel(p),'parent_sha256':sha(raw),'parent_bytes':len(raw),'patched_ids':[json.loads(l)['id'] for l in outlines if json.loads(l)['id'] in specs]})
assert len(sources)==24 and len(records)==761 and len(patches)==6
for r in records:r['source_sha256']=next(s['sha256'] for s in sources if s['path']==r['path'])
dump(OUT/'source-bindings.json',sources)
save(OUT/'record-bindings.jsonl',b''.join((json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n').encode() for r in records))
dump(OUT/'patches.json',patches)
dump(OUT/'current-index.json',{'schema':'codex-current-reviewed-core-v1','records':761,'sources':24,'groups':{'train':47,'selected_draft':264,'eval':300,'test':150},'parent_manifests':parent_manifests,'source_bindings_sha256':sha((OUT/'source-bindings.json').read_bytes()),'record_bindings_sha256':sha((OUT/'record-bindings.jsonl').read_bytes()),'patched_records':len(patches),'parent_byte_preserved_records':761-len(patches),'math':'PASS_VERSION_BOUND_CANDIDATE_FIELDS','semantic_isolation':'NOT_ESTABLISHED','browser_render':'LOCAL_TYPESETTING_ONLY','visual_layout':'NOT_INDEPENDENTLY_REVIEWED','native_render':'UNVERIFIED','production':'CLOSED','PASS_CORE_SCOPE_issued':False})
print(json.dumps({'records':len(records),'sources':len(sources),'patches':len(patches),'parent_artifacts_verified':sum(x['artifacts_verified'] for x in parent_manifests)}))
