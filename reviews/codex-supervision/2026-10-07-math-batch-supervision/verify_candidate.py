"""Read-only reconstruction of the additional 10 revisions and 38 reviewed bindings."""
from pathlib import Path
import json,hashlib,sys,importlib.util
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
def sha(data):return hashlib.sha256(data).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def rows(path):return [json.loads(line) for line in path.read_text(encoding='utf-8-sig').splitlines() if line.strip()]
def check(condition,message):
 if not condition:raise ValueError(message)
def inside(relative):
 rel=Path(relative);path=(ROOT/rel).resolve()
 check(not rel.is_absolute() and '..' not in rel.parts and path.is_relative_to(ROOT),'source path escape')
 return path
def verify():
 specs=read(OUT/'correction-specs.json')
 patches=rows(OUT/'corrections-10.jsonl')
 check(len(patches)==10 and {x['id'] for x in patches}==set(specs),'revision identity set')
 by_id={p['id']:p for p in patches};bindings=read(OUT/'candidate-source-bindings.json')
 check(len(bindings)==6 and len({b['source_path'] for b in bindings})==6,'candidate source scope')
 sp=importlib.util.spec_from_file_location('batch_v3',ROOT/'tools/math_review_batch.py')
 m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
 refs={r['id']:r for r in m.load_bound_refs(ROOT)}
 prior=ROOT/'reviews/codex-supervision/2026-10-07-core-verifier-followup/admission-v2'
 check(sha((prior/'admission-manifest.json').read_bytes())==
       '56e43c79868ad5ac09b3fed874a8a2dda8290ea313b9c92534c16457e7df4a86','parent manifest differs')
 for b in read(prior/'admission-manifest.json')['items']:
  data=inside(b['path']).read_bytes()
  check(sha(data)==b['raw_sha256'] and len(data)==b['bytes'],'parent artifact differs')
 candidate={};changed=0;count=0
 for b in bindings:
  source=inside(b['source_path']).read_bytes()
  parent=inside(b['parent_candidate_path']).read_bytes()
  raw=inside(b['path']).read_bytes()
  check(sha(source)==b['source_raw_sha256'],'original source differs')
  check(sha(parent)==b['parent_raw_sha256'],'parent source differs')
  check(sha(raw)==b['raw_sha256'] and len(raw)==b['bytes'],'candidate source binding differs')
  orig=source.splitlines(keepends=True);before=parent.splitlines(keepends=True);after=raw.splitlines(keepends=True)
  check(len(orig)==len(before)==len(after)==b['records'],'source line count changed')
  positions=[]
  for i,(a,z) in enumerate(zip(before,after),1):
   old=json.loads(a.decode('utf-8-sig'));new=json.loads(z.decode('utf-8-sig'))
   check(old['id']==new['id'],'identity changed')
   candidate[new['id']]=new;count+=1
   patch=by_id.get(new['id'])
   if patch:
    check(old==json.loads(orig[i-1].decode('utf-8-sig')),'unexpected parent record before new revision')
    check(patch['source']==refs[new['id']],'revision reference differs')
    check(patch['source']['source_line']==i and patch['source']['source_path']==b['source_path'],'revision position differs')
    check(sha(canon(old))==patch['before_record_dense_sha256'],'before dense hash differs')
    check(sha(canon(new))==patch['after_record_dense_sha256'],'after dense hash differs')
    spec=specs[new['id']];expected=dict(old)
    if 'problem_append' in spec:expected['problem']+=spec['problem_append']
    for k in ('problem','solution','answer','scene_spec'):
     if k in spec:expected[k]=spec[k]
    check(new==expected==patch['corrected_record'],'candidate record differs from explicit correction')
    fields=[k for k in old if old[k]!=new[k]]
    check(fields==patch['changed_fields'],'declared changes differ')
    check(patch['before_fields']=={k:old[k] for k in fields},'before fields differ')
    check(patch['after_fields']=={k:new[k] for k in fields},'after fields differ')
    positions.append(i);changed+=1
   else:check(a==z,'unlisted source row changed')
  check(positions==b['changed_lines'],'changed line declarations differ')
 check(count==497 and changed==10,'candidate counts differ')
 for b in rows(prior/'record-bindings.jsonl'):
  check(sha(canon(candidate[b['id']]))==b['final_record_dense_sha256'],'previous 30 revision changed')
 review=rows(OUT/'independent-review-38.jsonl')
 check(len(review)==38 and len({r['id'] for r in review})==38,'independent reviewed scope differs')
 witnesses=read(OUT/'exact-math-witnesses-38.json')
 check(witnesses['reviewed']==38 and len(witnesses['witnesses'])==38,'exact witness scope differs')
 w={r['id']:r for r in witnesses['witnesses']}
 check(len(w)==38 and set(w)=={r['id'] for r in review},'witness IDs differ')
 for row in review:
  check(row['source']==refs[row['id']],'review source binding differs')
  final_sha=sha(canon(candidate[row['id']]))
  check(final_sha==row['final_record_dense_sha256']==w[row['id']]['final_record_dense_sha256'],'review/witness candidate version differs')
 check(witnesses['decimal_or_numerical_approximation_used'] is False,'numeric approximation not authorized')
 return {'status':'PASS_INDEPENDENT_SOURCE_AND_VERSION_RECONSTRUCTION','reviewed':38,
 'additional_revisions':10,'previous_revisions_preserved':30,'candidate_sources':6,'candidate_records':497,
 'semantic_isolation':'NOT_ESTABLISHED','native_render':'UNVERIFIED','active_data_admission':'PENDING','production':'CLOSED'}
if __name__=='__main__':
 try:
  print(json.dumps(verify(),ensure_ascii=False,indent=2))
 except (ValueError,OSError,KeyError,TypeError,IndexError) as e:
  print(json.dumps({'status':'FAIL','error':str(e)},ensure_ascii=False));sys.exit(1)
