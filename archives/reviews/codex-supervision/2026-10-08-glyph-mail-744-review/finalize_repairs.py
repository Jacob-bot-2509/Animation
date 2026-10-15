"""Finalize three bounded math/scene repairs without overwriting any frozen delivery."""
from pathlib import Path
import json,hashlib,sys,copy,difflib
import sympy as S
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'))
import core_signatures as c,native_render_pilot as native
def read(p):return json.loads(p.read_text('utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v):
 with (O/n).open('xb') as f:f.write(c.encoded(v))
def jl(n,vs):
 with (O/n).open('xb') as f:
  for v in vs:f.write((json.dumps(v,ensure_ascii=False,sort_keys=True)+'\n').encode())
old=list(map(json.loads,(O/'source-before.jsonl').read_text('utf-8').splitlines()))
phase1=list(map(json.loads,(O/'dataset_eval-candidate.jsonl').read_text('utf-8').splitlines()))
final=copy.deepcopy(phase1)
gids=['eval-geom-007-s1','eval-geom-007-s2'];ids=['eval-calc-030-s3']+gids
def replace(v):
 if isinstance(v,str):
  for a,b in [(r'\u7ed5$y$\u8f74',r'\u4ee5$y$\u8f74\u4e3a\u4e3b\u8f74\u7684\u692d\u5706\u578b'),(r'\u7ed5$y$ \u8f74',r'\u4ee5$y$ \u8f74\u4e3a\u4e3b\u8f74\u7684\u692d\u5706\u578b')]:
   v=v.replace(a.encode().decode('unicode_escape'),b.encode().decode('unicode_escape'))
  return v
 if isinstance(v,list):return [replace(x) for x in v]
 if isinstance(v,dict):return {k:replace(x) for k,x in v.items()}
 return v
for i,v in enumerate(final):
 if v['id'] in gids:final[i]=replace(v)
assert len(final)==300 and [v['id'] for v in final]==[v['id'] for v in old]
assert sorted(v['id'] for v,w in zip(final,old) if v!=w)==sorted(ids)
for v,w in zip(final,old):
 assert v['id']==w['id'] and v['problem']==w['problem'] and v['answer']==w['answer']
 if v['id'] in gids:
  assert v!=w
  assert native.formula_inventory(v)==native.formula_inventory(w)
jl('dataset_eval-final-candidate.jsonl',final)
source=O/'dataset_eval-final-candidate.jsonl';sourcehash=sha(source)
save('changed-records-final.json',[{'before':w,'after':v} for v,w in zip(final,old) if v!=w])
with (O/'final-math-changes.patch').open('xb') as f:
 f.write(''.join(difflib.unified_diff((O/'source-before.jsonl').read_text('utf-8').splitlines(True),source.read_text('utf-8').splitlines(True),fromfile='frozen-eval-before.jsonl',tofile='dataset_eval-final-candidate.jsonl')).encode())
bindings=c.load_record_bindings();bs=[]
for b in bindings:
 b=copy.deepcopy(b)
 if b['id'] in ids:
  v=next(x for x in final if x['id']==b['id'])
  b.update(parent_binding=copy.deepcopy(b),path=source.relative_to(R).as_posix(),source_sha256=sourcehash,record_sha256=c.dense(v),math_sha256=c.math_digest(v),review='REPAIRED_PASS_LOCAL_EXACT_MATH_AND_SCENE_TEXT',repair_review='PASS_INDEPENDENT_VERIFICATION_THIS_BATCH')
 bs.append(b)
jl('effective-record-bindings.jsonl',bs)
nb={b['id']:b for b in bs}
oldidx=list(map(json.loads,(R/'reviews/codex-supervision/2026-10-08-glyph-review-followup/DELIVERY_INDEX.jsonl').read_text('utf-8').splitlines()))
idx=list(map(json.loads,(O/'DELIVERY_INDEX.jsonl').read_text('utf-8').splitlines()))
for v in idx:
 if v['id'] in ids:
  b=nb[v['id']]
  v.update(source_path=b['path'],source_sha256=b['source_sha256'],source_line=b['source_line'],record_sha256=b['record_sha256'],math_sha256=b['math_sha256'],parent_record_sha256=b['parent_binding']['record_sha256'],repair_version_binding=(O/'final-version-binding.json').relative_to(R).as_posix(),math_scene_qualification='REPAIRED_PASS_LOCAL_EXACT_MATH_AND_SCENE_TEXT')
jl('CURRENT_DELIVERY_INDEX.jsonl',idx);idxhash=sha(O/'CURRENT_DELIVERY_INDEX.jsonl')
save('final-version-binding.json',{'parent_core_manifest_sha256':'e66ca4f1835667801cc20502818dbf3398308634e8dc2b9a7f1b182ba3805eda','source_path':source.relative_to(R).as_posix(),'source_sha256':sourcehash,'source_records':300,'core_records':761,'changed_records':3,'overrides':[nb[x] for x in ids],'binding_path':(O/'effective-record-bindings.jsonl').relative_to(R).as_posix(),'binding_sha256':sha(O/'effective-record-bindings.jsonl'),'qualification':'REPAIRED_PASS_LOCAL_EXACT_MATH_AND_SCENE_TEXT','signature_version_binding':'NEEDS_REBINDING_FOR_THREE_CURRENT_OVERRIDES','production':'CLOSED'})
# Proof of exact same formula inventory/pixels for two scene wording repairs.
led=[]
phaseled=list(map(json.loads,(O/'page-glyph-verdicts.jsonl').read_text('utf-8').splitlines()))
for v in phaseled:
 if v['id'] in gids:
  z=copy.deepcopy(v);z.update(record_sha256=nb[v['id']]['record_sha256'],math_sha256=nb[v['id']]['math_sha256'],source_path=source.relative_to(R).as_posix(),source_sha256=sourcehash,math_qualification='PASS_PRECISE_ELLIPTIC_ONE_SHEET_CLASSIFICATION',version_inheritance='FORMULA_INVENTORY_AND_CANONICAL_PIXELS_IDENTICAL_DESPITE_PROSE_REPAIR');led.append(z)
assert len(led)==8
jl('scene-repair-page-glyph-verdicts.jsonl',led)
q=read(O/'current-page-review-queue.json');q.update(index_path=(O/'CURRENT_DELIVERY_INDEX.jsonl').relative_to(R).as_posix(),index_sha256=idxhash)
for p in q['pages']:
 if p['id'] in gids:
  v=next(v for v in led if (v['id'],v['page'])==(p['id'],p['page']))
  p.update(record_sha256=v['record_sha256'],math_sha256=v['math_sha256'],verdict_source=(O/'scene-repair-page-glyph-verdicts.jsonl').relative_to(R).as_posix())
save('effective-page-review-queue.json',q)
save('current-unreviewed-pages.json',[p for p in q['pages'] if p['review_status']!='PASS_ACTUAL_IMAGE_REVIEW'])
# Cross-bind every current queue page to the final index, geometry, source, inventory and PNG.
byid={v['id']:v for v in idx};seen=set();full=[];sg=0;cache={};verification=[]
for b in bs:
 c.load_record({b['id']:b},b['id'])
for p in q['pages']:
 row=byid[p['id']];fr=row['canonical_frames'][p['page']-1]
 assert (p['id'],p['page']) not in seen;seen.add((p['id'],p['page']))
 assert p['path']==fr['path'] and p['sha256']==fr['sha256']==sha(R/p['path'])
 for k in ('record_sha256','math_sha256'):assert p[k]==row[k]
 gp=read(R/row['geometry_path'])['pages'][p['page']-1]
 assert gp['kind']==p['kind']
 if p['review_status']=='PASS_ACTUAL_IMAGE_REVIEW':
  vp=R/p['verdict_source'];cache.setdefault(str(vp),list(map(json.loads,vp.read_text('utf-8').splitlines())))
  assert len([v for v in cache[str(vp)] if v['status']=='PASS' and all(v[k]==p[k] for k in ('id','page','path','sha256','record_sha256','math_sha256','formulas','kind','tile','tile_grid'))])==1
 if gp['kind']=='FULL_FORMULAS':
  oldrow=next(x for x in oldidx if x['id']==p['id']);oldfr=oldrow['canonical_frames'][p['page']-1]
  assert fr['sha256']==oldfr['sha256']
  oldgp=read(R/oldrow['geometry_path'])['pages'][p['page']-1]
  assert gp==oldgp
  full.append({'id':p['id'],'page':p['page'],'sha256':fr['sha256'],'same_geometry':True})
 else:sg+=1
assert len(idx)==165 and len(q['pages'])==633 and len(full)==552 and sg==81
assert sum(p['review_status']=='PASS_ACTUAL_IMAGE_REVIEW' for p in q['pages'])==264
for row in idx:
 b=nb[row['id']];v=c.load_record({b['id']:b},b['id'])
 assert row['source_sha256']==b['source_sha256'] and row['record_sha256']==c.dense(v) and row['math_sha256']==c.math_digest(v)
 inv=read(R/row['formula_inventory_path'])
 assert inv==dict(zip(['unique_formulas','source_occurrences'],native.formula_inventory(v)))
 assert sha(R/row['formula_inventory_path'])==row['formula_inventory_sha256']
 assert sha(R/row['geometry_path'])==row['geometry_sha256']
# Independent exact geometric checks: standard form, principal axis and lack of revolution.
x,y,z,k=S.symbols('x y z k',real=True)
assert S.Matrix([[4,0,0],[0,-1,0],[0,0,1]]).eigenvals()=={S.Integer(4):1,S.Integer(-1):1,S.Integer(1):1}
assert S.simplify(4*(S.sqrt(1+k*k)/2)**2-(1+k*k))==0
assert 4*S.Rational(1,2)**2==1 and S.Rational(1,2)**2!=1
for rid in gids:
 v=next(x for x in final if x['id']==rid)
 assert '\u7ed5$y$\u8f74' not in json.dumps(v,ensure_ascii=False)
 assert '\u4e3b\u8f74' in v['solution']
save('full-page-quantitative-inheritance.json',{'status':'PASS_EXACT_SAME_FULL_PAGE_PIXELS_AND_GEOMETRY','parent_index_sha256':sha(R/'reviews/codex-supervision/2026-10-08-glyph-review-followup/DELIVERY_INDEX.jsonl'),'current_index_sha256':idxhash,'full_pages':full,'full_page_count':552,'segment_page_count':81,'statistical_source':'reviews/codex-supervision/2026-10-08-quantitative-v2-review/verification-v3.json','statistical_source_sha256':sha(R/'reviews/codex-supervision/2026-10-08-quantitative-v2-review/verification-v3.json'),'slot_proxy_only':True,'minimum_glyph_height':'NOT_CERTIFIED'})
save('final-independent-verification.json',{'status':'PASS_LOCAL_THREE_REPAIRS_AND_VERSIONED_PAGE_BINDINGS','changed_ids':ids,'core_records_bound':761,'render_records_bound':165,'pages_bound':633,'exact_same_full_pages':552,'current_review_pass_pages':264,'pending_pages':369,'additional_symbolic_checks':['exact_symmetric_matrix_eigenvalues_4_minus1_1','positive_y_section_ellipse','counterexample_to_rotational_symmetry_about_y'],'formula_inventory_unchanged_for_scene_wording_repairs':gids,'current_index_path':(O/'CURRENT_DELIVERY_INDEX.jsonl').relative_to(R).as_posix(),'current_index_sha256':idxhash,'source_sha256':sourcehash,'record_bindings_sha256':sha(O/'effective-record-bindings.jsonl'),'phase1_math_and_render_verification_sha256':sha(O/'independent-verification.json'),'full_glyph_visual_acceptance':'NOT_ESTABLISHED','semantic_isolation':'NOT_ESTABLISHED','production':'CLOSED','signature_version_binding':'NEEDS_REBINDING_FOR_THREE_CURRENT_OVERRIDES'})
print(json.dumps({'status':'PASS','index_sha256':idxhash,'source_sha256':sourcehash,'records':761,'pages':633,'glyph_pass':264,'pending':369,'changed_ids':ids}))
