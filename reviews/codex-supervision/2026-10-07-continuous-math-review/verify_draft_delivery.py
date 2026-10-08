"""Read-only reconstruction and version checks for the reviewed draft candidate."""
from pathlib import Path
import json,hashlib,sys,re
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def rows(p):return [json.loads(l) for l in p.read_text(encoding='utf-8-sig').splitlines() if l.strip()]
def check(x,msg):
 if not x:raise ValueError(msg)
def inside(base,relative):
 rel=Path(relative);p=(base/rel).resolve()
 check(not rel.is_absolute() and '..' not in rel.parts and p.is_relative_to(base.resolve()),'unsafe path')
 return p
def verify():
 specs=read(OUT/'draft-correction-specs.json');patches=rows(OUT/'draft-corrections-10.jsonl')
 check(len(specs)==len(patches)==10 and set(specs)=={p['id'] for p in patches},'correction set')
 patchmap={p['id']:p for p in patches};notes=read(OUT/'draft-review-notes.json')
 bindings=read(OUT/'draft-candidate-source-bindings.json')
 final={};changed=0
 for b in bindings:
  live=inside(ROOT,b['source_path']).read_bytes()
  orig=inside(OUT,'source-originals/'+b['source_path']).read_bytes()
  after=inside(ROOT,b['path']).read_bytes()
  check(live==orig and sha(orig)==b['source_raw_sha256'] and len(orig)==b['source_bytes'],'original version changed')
  check(sha(after)==b['raw_sha256'] and len(after)==b['bytes'],'candidate bytes changed')
  before_lines=orig.splitlines(keepends=True);after_lines=after.splitlines(keepends=True)
  check(len(before_lines)==len(after_lines)==b['records'],'count changed')
  positions=[]
  for i,(lb,la) in enumerate(zip(before_lines,after_lines),1):
   old=json.loads(lb.decode('utf-8-sig'));new=json.loads(la.decode('utf-8-sig'));rid=new['id']
   check(rid==old['id'] and rid not in final,'identity/duplicate')
   final[rid]=new
   if rid in patchmap:
    p=patchmap[rid];spec=specs[rid]
    check(p['source']['source_path']==b['source_path'] and p['source']['source_line']==i,'source position')
    check(sha(canon(old))==p['before_record_sha256']==p['source']['record_version_sha256'],'original row version')
    check(new==p['corrected_record'] and sha(canon(new))==p['after_record_sha256'],'candidate row version')
    fields=[k for k in old if old[k]!=new[k]]
    check(fields==p['changed_fields'],'field list differs')
    check({k:old[k] for k in fields}==p['before_fields'] and {k:new[k] for k in fields}==p['after_fields'],'field snapshots differ')
    for f in ('problem','solution','answer','scene_spec'):
     check(new[f]==spec['fields'].get(f,old[f]),'explicit mathematical correction differs')
    check(set(fields)<=set(spec['fields'])|{'revision_lineage','versioned_id','draft_status','strict_review'},'unexpected field changed')
    parent=new['revision_lineage']['continuous_review_parent']
    check(parent['strict_review']==old['strict_review'] and parent['record_version_sha256']==sha(canon(old)),'historical review not retained')
    check(new['versioned_id']=='codex-continuous-draft-v1-20261007-'+rid,'revision name')
    positions.append(i);changed+=1
   else:check(lb==la,'unlisted row changed')
   mathsha=sha(json.dumps({k:new[k] for k in ('problem','solution','answer','scene_spec')},ensure_ascii=False,sort_keys=True).encode())
   check(new['strict_review']['math_content_sha256']==mathsha,'stale mathematical fingerprint')
   check(new['admitted'] is False and new['animation_render_verified'] is False,'admission/render claim changed')
  check(positions==b['changed_lines'],'line deltas')
 check(len(final)==264 and changed==10 and len(bindings)==18,'scope counts')
 review=rows(OUT/'independent-draft-review-264.jsonl')
 check(len(review)==264 and set(final)==set(notes)=={r['id'] for r in review},'review coverage')
 for q in review:
  rid=q['id']
  check(q['candidate_record_sha256']==sha(canon(final[rid])),'receipt candidate differs')
  check(q['independent_basis']==notes[rid] and notes[rid],'proof note missing')
  check(q['post_repair_math']==q['post_repair_scene_text']==q['exact_expression_policy']=='PASS','post-repair verdict')
  check(q['native_render']=='UNVERIFIED' and q['semantic_isolation']=='NOT_ESTABLISHED' and q['admitted'] is False,'scope inflation')
 # Explicit dimensions prevent silently interpreting a missing TeX row separator as multiplication.
 for rid,field,rows_expected,cols_expected in [('draft-c33-03','solution',2,1),('draft-c37-04','answer',2,2)]:
  text=final[rid][field]
  target=(r'\begin{pmatrix}-\frac12\\\frac12\end{pmatrix}' if rid.endswith('33-03')
          else r'\begin{pmatrix}\frac32&\frac32\\\frac12&-\frac12\end{pmatrix}')
  check(target in text,'corrected matrix string missing')
  body=target.split(r'\begin{pmatrix}')[1].split(r'\end{pmatrix}')[0]
  cells=[row.split('&') for row in body.split(r'\\')]
  check(len(cells)==rows_expected and all(len(row)==cols_expected for row in cells),'matrix dimensions')
 witnesses=read(OUT/'draft-exact-witnesses.json')
 check(witnesses['status']=='PASS_EXACT_SYMBOLIC_WITNESSES' and witnesses['approximation_used'] is False,'witness receipt')
 check(witnesses['proof_review_binding']==sha((OUT/'independent-draft-review-264.jsonl').read_bytes()),'proof witness binding')
 check(witnesses['checks']==len(witnesses['witnesses']) and witnesses['checks']>=100,'witness count')
 for w in witnesses['witnesses']:
  check(w['status']=='PASS' and w['candidate_record_sha256']==sha(canon(final[w['id']])),'witness row binding')
 manifest=OUT/'draft-delivery-manifest.json'
 if manifest.exists():
  m=read(manifest)
  for b in m['artifacts']:
   data=inside(OUT,b['path']).read_bytes()
   check(sha(data)==b['raw_sha256'] and len(data)==b['bytes'],'archive manifest mismatch '+b['path'])
 return {'status':'PASS_DRAFT_SOURCE_AND_REPAIR_RECONSTRUCTION','drafts_reviewed':264,'repaired_records':changed,
  'unchanged_record_bytes_preserved':254,'candidate_sources':18,'exact_symbolic_checks':witnesses['checks'],
  'symbolically_checked_record_count':witnesses['distinct_records_with_symbolic_witnesses'],
  'post_repair_math':'PASS','scene_text':'PASS','semantic_isolation':'NOT_ESTABLISHED','native_render':'UNVERIFIED',
  'active_admission':'PENDING','production':'CLOSED'}
if __name__=='__main__':
 try:print(json.dumps(verify(),ensure_ascii=False,indent=2))
 except (ValueError,OSError,KeyError,IndexError,TypeError) as e:
  print(json.dumps({'status':'FAIL','error':str(e)},ensure_ascii=False));sys.exit(1)
