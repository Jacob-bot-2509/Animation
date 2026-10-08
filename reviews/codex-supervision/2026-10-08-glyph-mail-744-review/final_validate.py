"""Independent verification of the final candidate registered in this new review directory."""
from pathlib import Path
import json,hashlib,sys
import sympy as S
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'))
import core_signatures as c,native_render_pilot as native
def read(p):return json.loads(p.read_text('utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v):
 with (O/n).open('xb') as f:f.write(c.encoded(v))
def load(b):
 p=R/b['path']
 if p.is_relative_to(O):
  p=c.checked_path(p,O)
  assert sha(p)==b['source_sha256']
  r=json.loads(p.read_text('utf-8').splitlines()[b['source_line']-1])
  assert r['id']==b['id'] and c.dense(r)==b['record_sha256'] and c.math_digest(r)==b['math_sha256']
  return r
 return c.load_record({b['id']:b},b['id'])
final=list(map(json.loads,(O/'dataset_eval-final-candidate.jsonl').read_text('utf-8').splitlines()))
old=list(map(json.loads,(O/'source-before.jsonl').read_text('utf-8').splitlines()))
ids=['eval-calc-030-s3','eval-geom-007-s1','eval-geom-007-s2'];gids=ids[1:]
assert len(final)==len(old)==300 and sorted(a['id']for a,b in zip(final,old) if a!=b)==sorted(ids)
bs=list(map(json.loads,(O/'effective-record-bindings.jsonl').read_text('utf-8').splitlines()));nb={b['id']:b for b in bs}
assert len(bs)==len(nb)==761
idx=list(map(json.loads,(O/'CURRENT_DELIVERY_INDEX.jsonl').read_text('utf-8').splitlines()))
oldidx=list(map(json.loads,(R/'reviews/codex-supervision/2026-10-08-glyph-review-followup/DELIVERY_INDEX.jsonl').read_text('utf-8').splitlines()))
q=read(O/'effective-page-review-queue.json');idxhash=sha(O/'CURRENT_DELIVERY_INDEX.jsonl');sourcehash=sha(O/'dataset_eval-final-candidate.jsonl')
for a,b in zip(final,old):
 assert a['id']==b['id'] and a['problem']==b['problem'] and a['answer']==b['answer']
 if a['id'] in gids:assert native.formula_inventory(a)==native.formula_inventory(b)
assert q['index_sha256']==idxhash
# Cross-bind every current queue page to the final index, geometry, source, inventory and PNG.
byid={v['id']:v for v in idx};seen=set();full=[];sg=0;cache={};verification=[]
for b in bs:
 load(b)
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
 b=nb[row['id']];v=load(b)
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
