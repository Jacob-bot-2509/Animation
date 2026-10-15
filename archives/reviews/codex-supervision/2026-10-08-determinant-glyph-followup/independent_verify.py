"""Independent current-source, exact-math and actual-image binding verification."""
from pathlib import Path
from fractions import Fraction as F
import json,sys,copy,hashlib,math
from PIL import Image
import numpy as np,sympy as S,av
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'))
import core_signatures as c,native_render_pilot as native
P=R/'reviews/codex-supervision/2026-10-08-glyph-mail-744-review'
def read(p):return json.loads(p.read_text('utf-8'))
def jl(p):return list(map(json.loads,p.read_text('utf-8').splitlines()))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v):
 with(O/n).open('xb')as f:f.write(c.encoded(v))
def lines(n,vs):
 with(O/n).open('xb')as f:
  for x in vs:f.write((json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n').encode())
def rel(p):return p.relative_to(R).as_posix()
manifest=read(P/'delivery-manifest.json')
assert sha(P/'delivery-manifest.json')=='983cc586e0f3c73980dcfc96498bfb5c78428b1f24a99a150e616cd672aa0ff2'
for x in manifest['artifacts']:
 p=c.checked_path(P/x['path'],P);assert sha(p)==x['sha256']and p.stat().st_size==x['bytes']
assert len(manifest['artifacts'])==109
sources=read(O/'current-source-bindings.json');cache={}
for x in sources:
 p=c.checked_path(R/x['path'],R);assert sha(p)==x['sha256']and p.stat().st_size==x['bytes']
 cache[x['path']]=jl(p);assert len(cache[x['path']])==x['records']
assert len(sources)==24 and sum(len(x)for x in cache.values())==761
bs=jl(O/'current-record-bindings.jsonl');bm={b['id']:b for b in bs};oldbs=jl(P/'effective-record-bindings.jsonl');ob={b['id']:b for b in oldbs};records={}
assert len(bs)==len(bm)==761 and set(bm)==set(ob)
for b in bs:
 rec=cache[b['path']][b['source_line']-1];assert rec['id']==b['id']and sha(R/b['path'])==b['source_sha256']
 assert c.dense(rec)==b['record_sha256']and c.math_digest(rec)==b['math_sha256'];records[b['id']]=rec
changed=[b['id']for b in bs if b['record_sha256']!=ob[b['id']]['record_sha256']]
assert changed==['eval-linalg-002-s3','eval-linalg-004-s3']
before=jl(O/'source-before.jsonl');final=jl(O/'dataset_eval-final-candidate.jsonl')
assert len(final)==300 and [x['id']for x in before]==[x['id']for x in final]
assert [x['id']for x,y in zip(final,before)if x!=y]==changed
for rid in changed:
 old=before[ob[rid]['source_line']-1];new=records[rid]
 assert all(old[k]==new[k]for k in ('problem','answer','id'))
for rid in ['eval-calc-030-s3','eval-geom-007-s1','eval-geom-007-s2']:assert bm[rid]['record_sha256']==ob[rid]['record_sha256']
sigs=jl(O/'current-complete-signatures.jsonl');assert len(sigs)==761 and len({s['id']for s in sigs})==761
parentsigs={s['id']:s for s in jl(P/'effective-complete-signatures.jsonl')}
for s in sigs:
 b=bm[s['id']];assert all(s[k]==b[k]for k in ('record_sha256','math_sha256'))
 x=copy.deepcopy(s);x.update({k:parentsigs[s['id']][k]for k in ('record_sha256','math_sha256')});assert x==parentsigs[s['id']]
oldrows=jl(P/'CURRENT_DELIVERY_INDEX.jsonl');rows=copy.deepcopy(oldrows)
rr=read(O/'repair-render-result.json');rid=rr['id'];assert rid=='eval-linalg-004-s3'
assert c.dense(records[rid])==rr['record_binding']['record_sha256']
assert c.math_digest(records[rid])==rr['record_binding']['math_sha256']
assert sha(R/rr['record_binding']['path'])==rr['record_binding']['source_sha256']
inv=read(R/rr['formula_inventory_path']);f,l=native.formula_inventory(records[rid])
assert inv=={'unique_formulas':f,'source_occurrences':l}and len(f)==27 and len(l)==64
decoded=0
with av.open(str(R/rr['mp4_path']))as video:
 st=video.streams.video[0];assert(st.width,st.height)==(3840,2160)and F(st.average_rate)==1
 for i,fr in enumerate(video.decode(st)):
  if i%3==0:
   j=i//3;assert F(fr.pts)*F(fr.time_base)==3*j
   assert np.array_equal(np.asarray(fr.to_image().convert('RGB')),np.asarray(Image.open(R/rr['frames'][j]['path']).convert('RGB')))
   decoded+=1
 assert i+1==15 and decoded==5
assert sha(R/rr['mp4_path'])==rr['mp4_sha256']
priorq=read(P/'effective-page-review-queue.json');pq={p['ordinal']:p for p in priorq['pages']}
assert len(pq)==633 and sum(p['review_status']=='PASS_ACTUAL_IMAGE_REVIEW'for p in pq.values())==264
fields=('id','page','path','sha256','record_sha256','math_sha256','formulas','kind','tile','tile_grid')
verdictcache={}
for p in pq.values():
 if p['review_status']=='PASS_ACTUAL_IMAGE_REVIEW':
  vp=R/p['verdict_source']
  if str(vp)not in verdictcache:verdictcache[str(vp)]=jl(vp)
  assert sum(v['status']=='PASS'and all(v[k]==p[k]for k in fields)for v in verdictcache[str(vp)])==1
selected=read(O/'selected-review-pages.json');assert [p['ordinal']for p in selected]==list(range(240,272))
notes=dict(read(O/'actual-page-notes.json')['notes']);repairnotes=read(O/'actual-page-notes.json')['repair_notes']
assert len(notes)==32 and len(repairnotes)==5
oldledger=[]
for p in selected:
 assert p==pq[p['ordinal']]and p['review_status']!='PASS_ACTUAL_IMAGE_REVIEW'
 z=copy.deepcopy(p);z.update(status='FAIL_FORMULA_NOTATION'if p['ordinal']==268 else'PASS',notes=notes[p['ordinal']],review_method='ACTUAL_INDIVIDUAL_PNG_VIEW_WITH_SOURCE_TEX_COMPARISON',source_version_scope='SUPERSEDED_RECORD_HISTORY'if p['id']in changed else'CURRENT_UNCHANGED_RECORD',segment_judgment='PASS_ADJACENT_SEGMENTS_JOIN_AND_OVERLAP'if p['kind']=='FORMULA_SEGMENT'else'NOT_APPLICABLE')
 oldledger.append(z)
lines('original-page-glyph-verdicts.jsonl',oldledger)
# Full record source review archive, distinct from visual formula qualification.
selectedids=sorted({p['id']for p in selected});assert len(selectedids)==8
save('bound-current-math-records.json',[{'binding':bm[k],'record':records[k]}for k in selectedids])
qpages=[];newledger=[];metrics=[];formula_count=0;occ_count=0;inherited_frames=0
for row,oldrow in zip(rows,oldrows):
 b=bm[row['id']];rec=records[row['id']]
 assert oldrow['record_sha256']==ob[row['id']]['record_sha256']and oldrow['math_sha256']==ob[row['id']]['math_sha256']
 row['render_parent_binding']={k:oldrow[k]for k in ('record_sha256','math_sha256','source_sha256')}
 row.update({k:b[k]for k in ('record_sha256','math_sha256','source_sha256')});row.update(source_path=b['path'],source_line=b['source_line'])
 if row['id']==rid:
  row.update({k:rr[k]for k in ('geometry_path','geometry_sha256','formula_inventory_path','formula_inventory_sha256','mp4_path','mp4_sha256','page_count','video_frames','unique_formulas','source_formula_occurrences')})
  row['canonical_frames']=rr['frames'];row['repair_version_binding']=rel(O/'final-version-binding.json');row['segment_pages']=0
 elif row['id']in changed:
  row['scene_text_only_repair']=True;row['repair_version_binding']=rel(O/'final-version-binding.json')
 ip=c.checked_path(R/row['formula_inventory_path'],R);gp=c.checked_path(R/row['geometry_path'],R)
 assert sha(ip)==row['formula_inventory_sha256']and sha(gp)==row['geometry_sha256']
 inventory=read(ip);g=read(gp);ff,ll=native.formula_inventory(rec)
 assert inventory=={'unique_formulas':ff,'source_occurrences':ll}
 assert len(ff)==row['unique_formulas']and len(ll)==row['source_formula_occurrences']
 assert len(g['pages'])==len(row['canonical_frames'])==row['page_count']
 assert(g['pixel_width'],g['pixel_height'])==(3840,2160)and F(g['fps'])==1 and F(g['page_seconds'])==3
 assert sha(c.checked_path(R/row['mp4_path'],R))==row['mp4_sha256']
 formula_count+=len(ff);occ_count+=len(ll);rowmetrics=[]
 for geo,fr in zip(g['pages'],row['canonical_frames']):
  ordinal=len(qpages);path=c.checked_path(R/fr['path'],R)
  assert sha(path)==fr['sha256'];im=Image.open(path);assert im.size==(3840,2160)
  p={'ordinal':ordinal,'id':row['id'],'page':geo['page'],**{k:fr[k]for k in ('path','sha256')},**{k:b[k]for k in ('record_sha256','math_sha256')},'kind':geo['kind'],'tile':geo['tile'],'tile_grid':geo['tile_grid'],'formulas':[{'index':v['formula_index']+1,'tex':ff[v['formula_index']]}for v in geo['items']]}
  oldp=pq[ordinal];assert(p['id'],p['page'])==(oldp['id'],oldp['page'])
  if row['id']!=rid:
   assert all(p[k]==oldp[k]for k in ('path','sha256','formulas','kind','tile','tile_grid'));inherited_frames+=1
  if ordinal in notes:
   assert row['id']in selectedids
   note=repairnotes[geo['page']-1]if row['id']==rid else notes[ordinal]
   v=copy.deepcopy(p);v.update(status='PASS',notes=note,review_method='ACTUAL_INDIVIDUAL_PNG_VIEW_WITH_SOURCE_TEX_COMPARISON',math_qualification='PASS_LOCAL_COMPLETE_PROOF_REVIEW',segment_judgment='PASS_ADJACENT_SEGMENTS_JOIN_AND_OVERLAP'if p['kind']=='FORMULA_SEGMENT'else'NOT_APPLICABLE')
   if row['id']=='eval-linalg-002-s3':v.update(current_version_inheritance='IDENTICAL_TEX_OCCURRENCES_GEOMETRY_AND_PNG; THREE_TEXT_LABELS_REPAIRED',parent_record_sha256=oldp['record_sha256'])
   newledger.append(v);p.update(review_status='PASS_ACTUAL_IMAGE_REVIEW',verdict_source=rel(O/'current-batch-page-glyph-verdicts.jsonl'))
  else:
   assert all(p[k]==oldp[k]for k in fields)
   p.update({k:oldp[k]for k in ('review_status','verdict_source')if k in oldp})
  qpages.append(p)
  if geo['kind']=='FULL_FORMULAS':
   ar=np.asarray(im.convert('RGB'))[271:1889,136:3704];mask=(ar>32).any(axis=2);yy,xx=np.nonzero(mask);assert len(xx)
   height=int(yy.max()-yy.min()+1);width=int(xx.max()-xx.min()+1);items=len(geo['items'])
   m={'page':geo['page'],'bbox_height':height,'bbox_width':width,'ink_pixels':int(mask.sum()),'displayed_formula_items':items,'metric_scope':'OCCUPIED_BBOX_SLOT_PROXY_NOT_MINIMUM_GLYPH_SIZE','bbox_height_per_displayed_item_px_exact':str(F(height,items)),'slot_proxy_at_1080p_exact':str(F(height,2*items))}
   metrics.append({'id':row['id'],**m});rowmetrics.append(m)
  else:
   assert row['id']!=rid
   oldm=next(x for x in oldrow['page_metrics']if x['page']==geo['page']);rowmetrics.append(copy.deepcopy(oldm))
 row['page_metrics']=rowmetrics
assert len(rows)==165 and len(qpages)==633 and len(metrics)==552 and inherited_frames==628
assert len(newledger)==32 and sum(x['kind']=='FORMULA_SEGMENT'for x in newledger)==4
lines('CURRENT_DELIVERY_INDEX.jsonl',rows);lines('current-batch-page-glyph-verdicts.jsonl',newledger)
idxsha=sha(O/'CURRENT_DELIVERY_INDEX.jsonl')
q={'index_path':rel(O/'CURRENT_DELIVERY_INDEX.jsonl'),'index_sha256':idxsha,'pages':qpages,'parent_manifest_sha256':sha(P/'delivery-manifest.json')}
assert sum(p['review_status']=='PASS_ACTUAL_IMAGE_REVIEW'for p in qpages)==296
save('effective-page-review-queue.json',q);pending=[p for p in qpages if p['review_status']!='PASS_ACTUAL_IMAGE_REVIEW'];assert len(pending)==337
save('current-unreviewed-pages.json',pending);save('full-page-metrics.json',metrics)
slots=sorted(F(m['bbox_height_per_displayed_item_px_exact'])for m in metrics)
save('current-slot-proxy-summary.json',{'scope':'FULL_FORMULAS_OCCUPIED_BBOX_SLOT_PROXY_NOT_MINIMUM_GLYPH','full_pages':552,'segment_pages_excluded':81,'minimum_exact':str(slots[0]),'p10_nearest_rank_exact':str(slots[math.ceil(len(slots)/10)-1]),'median_exact':str((slots[275]+slots[276])/2),'minimum_at_1080p_exact':str(slots[0]/2),'minimum_glyph_height':'NOT_CERTIFIED'})
checks=[]
def eq(name,x,y):
 assert S.simplify(x-y)==0,name
 checks.append({'name':name,'status':'PASS','difference_exact':'0'})
def matrixeq(name,x,y):
 assert(x-y).applyfunc(S.simplify)==S.zeros(*x.shape),name
 checks.append({'name':name,'status':'PASS','all_component_differences_exact':'0'})
a,b=S.symbols('a b',positive=True);t=S.symbols('t',real=True)
r=S.Matrix([a*S.cos(t),a*S.sin(t),b*t]);v=r.diff(t);acc=v.diff(t);jerk=acc.diff(t);cross=v.cross(acc)
eq('helix_speed_squared',v.dot(v),a*a+b*b)
eq('helix_cross_squared',cross.dot(cross),a*a*(a*a+b*b))
eq('helix_triple_product',cross.dot(jerk),a*a*b)
eq('helix_curvature',S.sqrt(cross.dot(cross))/v.dot(v)**S.Rational(3,2),a/(a*a+b*b))
eq('helix_torsion',cross.dot(jerk)/cross.dot(cross),b/(a*a+b*b))
eq('helix_curvature_torsion_ratio',(a/(a*a+b*b))/(b/(a*a+b*b)),a/b)
u=S.Matrix([2,0]);w=S.Matrix([S.Rational(3,2),3*S.sqrt(3)/2]);summ=u+w;diff=2*u-w;diag=u-w
for name,x,y in [('norm_a',u.dot(u),4),('norm_b',w.dot(w),9),('vector_angle',u.dot(w),3),('sum_norm_squared',summ.dot(summ),19),('diff_norm_squared',diff.dot(diff),13),('diagonal_other_squared',diag.dot(diag),7),('diagonal_dot',summ.dot(diag),-5),('diagonal_cos',summ.dot(diag)/S.sqrt(summ.dot(summ)*diag.dot(diag)),-5/S.sqrt(133))]:eq(name,x,y)
u=S.Matrix([1,2,2]);w=S.Matrix([-2,1,2]);proj=(u.dot(w)/w.dot(w))*w
matrixeq('projection_components',proj,S.Matrix([S.Rational(-8,9),S.Rational(4,9),S.Rational(8,9)]))
eq('projection_orthogonal_residual',(u-proj).dot(w),0);eq('projection_length',S.sqrt(proj.dot(proj)),S.Rational(4,3));eq('projection_cos',u.dot(w)/S.sqrt(u.dot(u)*w.dot(w)),S.Rational(4,9))
pt=S.Matrix([t-4,5-2*t,t]);eq('plane_1_substitution',sum(pt),1);eq('plane_2_substitution',S.Matrix([1,2,3]).dot(pt),6)
assert S.Matrix([[1,1,1],[1,2,3]]).rank()==2;checks.append({'name':'plane_intersection_complete_rank_2','status':'PASS','parameterization':'(t-4,5-2*t,t), t real'})
A=S.ones(4)+S.diag(0,1,2,3);B=copy.deepcopy(A)
for i in range(3):B[i,:]=B[i,:]-B[3,:]
matrixeq('fourth_row_preserved',B,S.Matrix([[0,0,0,-3],[0,1,0,-3],[0,0,2,-3],[1,1,1,4]]))
C=S.Matrix([[0,0,-3],[1,0,-3],[0,2,-3]])
eq('4_by_4_determinant',A.det(),6);eq('3_by_3_minor',C.det(),-6);eq('minor_first_row_expansion',sum((-1)**j*C[0,j]*C.minor_submatrix(0,j).det()for j in range(3)),-6)
a,b=S.symbols('a b',real=True)
for n in range(1,6):
 eq('general_determinant_exact_n_'+str(n),(b*S.eye(n)+a*S.ones(n)).det(),b**(n-1)*(n*a+b))
J=S.ones(3);eq('J_characteristic_polynomial',J.charpoly().as_expr(),J.charpoly().gen**2*(J.charpoly().gen-3))
for j in range(3):
 U=S.eye(3);U[:,j]=S.ones(3,1);eq('replacement_standard_basis_column_'+str(j+1),U.det(),1)
eq('three_order_b_zero',(b*b*(3*a+b)).subs(b,0),0)
eq('one_order_all_a_b',(b*S.eye(1)+a*S.ones(1)).det(),a+b)
save('exact-symbolic-checks.json',checks)
proofs=[
{'id':'eval-geom-012-s3','proof':'For a,b>0, ds/dt=sqrt(a^2+b^2). Cross squared=a^2(a^2+b^2), triple=a^2 b. Thus kappa=a/(a^2+b^2), tau=b/(a^2+b^2), kappa:tau=a:b. Frenet signs T,N,B are consistent.','status':'PASS'},
{'id':'eval-geom-016-s3','proof':'Dot product a.b=3; (a+b)^2=19, (2a-b)^2=13, (a-b)^2=7 and (a+b).(a-b)=-5. Diagonal cosine=-5/sqrt(133).','status':'PASS'},
{'id':'eval-geom-017-s2','proof':'a.b=4, |a|=|b|=3; projection=(4/9)b=(-8/9,4/9,8/9), length=4/3, cosine=4/9.','status':'PASS'},
{'id':'eval-geom-019-s3','proof':'Subtract planes to get y+2z=5; taking z=t gives (t-4,5-2t,t). Independent normals give rank 2, so the parametrization is complete.','status':'PASS'},
{'id':'eval-linalg-002-s3','proof':'Keep row 4, subtract it from rows 1..3; expand 4x4 along column 1 with sign (-1)^5, then the displayed 3x3 along ROW 1: -[(-3)*2]=6. Three scene labels repaired; formula/source occurrence inventory identical.','status':'PASS_AFTER_SCENE_LABEL_REPAIR'},
{'id':'eval-linalg-004-s1','proof':'For n>=2, Ri<-Ri-R1 for i>=2; sum all columns into column 1. This makes column 1=(na+b,0,...,0)^T, with lower minor bI_(n-1); no division. n=1 is a+b. Includes b=0.','status':'PASS_GENERAL_PROOF'},
{'id':'eval-linalg-004-s2','proof':'R^n=span(1) direct sum {x:sum x_i=0}. J acts by n and 0 respectively, so bI+aJ acts by b+na and b. Determinant=(b+na)b^(n-1); the factors remain valid when a=0 and eigenvalues coincide.','status':'PASS_GENERAL_PROOF'},
{'id':'eval-linalg-004-s3','proof':'Expand each column be_j+a1 multilinearly. Terms with >=2 all-1 columns vanish; all b columns give b^n; exactly one all-1 column gives ab^(n-1), because det(e1,...,1,...,en)=1 (expand 1=sum e_k; only k=j survives). Sum n such terms; n=1 treated as a+b. No division, so b=0 covered. The complete 3x3 replacement determinant notation is repaired.','status':'PASS_AFTER_NOTATION_REPAIR_GENERAL_PROOF'}
]
save('complete-proof-review.json',proofs)
protected={'tools/hd_formula_pages.py':'2c60b0616b3be5bb87291de7e1c3c696eb05f5277804a5cc434109c4ae4d1c73','tools/visual_acceptance_verify_pages.py':'64c684dee38c4874a0eb4eb60fd4bf3ceee82369253c865821f16d8817a5a988'}
for path,value in protected.items():assert sha(R/path)==value
result={'status':'PASS_LOCAL_TWO_REPAIRS_EIGHT_COMPLETE_PROOFS_AND_32_CURRENT_PAGES','changed_ids':changed,'core_records_bound':761,'physical_sources':24,'render_records_bound':165,'pages_bound':633,'selected_original_pages':32,'actual_images_viewed':37,'new_current_pass_pages':32,'inherited_exact_pass_pages':264,'current_pass_pages':296,'pending_pages':337,'new_video_page_pixels_verified':5,'old_bound_pngs_inherited':628,'symbolic_checks':len(checks),'general_proof_evidence':rel(O/'complete-proof-review.json'),'current_index_path':rel(O/'CURRENT_DELIVERY_INDEX.jsonl'),'current_index_sha256':idxsha,'source_sha256':sha(O/'dataset_eval-final-candidate.jsonl'),'record_bindings_sha256':sha(O/'current-record-bindings.jsonl'),'signature_version_binding':'PASS_ALL_761_CURRENT_RECORD_VERSION_BINDINGS','signature_semantic_scope':'UNCHANGED_DESCRIPTORS; TWO_VERSION_BINDINGS_REBOUND; NO_NEW_GLOBAL_ISOLATION_CLAIM','protected_code_hashes':protected,'full_glyph_visual_acceptance':'NOT_ESTABLISHED','native_minimum_glyph_height':'NOT_CERTIFIED','semantic_isolation':'NOT_ESTABLISHED','conceptual_animation':'NOT_EVALUATED','native_sandbox':'UNVERIFIED','production':'CLOSED'}
save('final-independent-verification.json',result)
save('glyph-coverage-summary.json',{k:result[k]for k in ('selected_original_pages','actual_images_viewed','new_current_pass_pages','inherited_exact_pass_pages','current_pass_pages','pending_pages','full_glyph_visual_acceptance','current_index_path','current_index_sha256')})
print(json.dumps(result))
