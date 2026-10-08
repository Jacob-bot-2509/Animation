"""Merge only one repaired record and verify manually reviewed pages and exact mathematics."""
from pathlib import Path
import json,sys,copy,hashlib
from fractions import Fraction
from PIL import Image
import numpy as np,sympy as S
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'))
import core_signatures as c,native_render_pilot as native,hd_formula_pages as hd
def read(p):return json.loads(p.read_text('utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v):
 with(O/n).open('xb')as f:f.write(c.encoded(v))
def jsonl(n,v):
 with(O/n).open('xb')as f:
  for x in v:f.write((json.dumps(x,ensure_ascii=False,sort_keys=True)+'\n').encode())
parent=R/'reviews/codex-supervision/2026-10-08-glyph-review-followup/DELIVERY_INDEX.jsonl'
assert sha(parent)=='07b4543d38599e1c30d2b515e0c2a8761e5611f771c46c75ee23b357c58b6331'
rows=list(map(json.loads,parent.read_text('utf-8').splitlines()));oldrow=next(x for x in rows if x['id']=='eval-calc-030-s3')
rr=read(O/'repair-render-result.json');nb=rr['record_binding'];new=read(O/'record-after.json');old=read(O/'record-before.json')
assert c.dense(new)==nb['record_sha256'] and c.math_digest(new)==nb['math_sha256']
assert sha(R/nb['path'])==nb['source_sha256']
candidate=[json.loads(x)for x in (R/nb['path']).read_text('utf-8').splitlines()]
assert candidate[nb['source_line']-1]==new
oldsource=[json.loads(x)for x in (O/'source-before.jsonl').read_text('utf-8').splitlines()]
assert len(candidate)==len(oldsource)==300
assert [r['id']for r,s in zip(candidate,oldsource)if r!=s]==[new['id']]
oldb={x['id']:x for x in c.load_record_bindings()}
bs=list(map(json.loads,(O/'current-record-bindings.jsonl').read_text('utf-8').splitlines()))
assert len(bs)==761 and len({x['id']for x in bs})==761
assert [x['id']for x in bs if x!=oldb[x['id']]]==[new['id']]
inventory=read(R/rr['formula_inventory_path']);g=read(R/rr['geometry_path'])
f,l=native.formula_inventory(new);assert inventory=={'unique_formulas':f,'source_occurrences':l}
assert len(f)==15 and len(l)==36
assert f[9].count(r'\pi^2y')==0 and r'\left[\pi^2-2\pi\int_0^1' in f[9]
# Decode independently to pixels; avoid inferring success only from renderer return code.
import av
decoded=[]
with av.open(str(R/rr['mp4_path']))as video:
 stream=video.streams.video[0];assert(stream.width,stream.height)==(3840,2160)and Fraction(stream.average_rate)==1
 for i,frame in enumerate(video.decode(stream)):
  if i%3==0:
   j=i//3;assert Fraction(frame.pts)*Fraction(frame.time_base)==j*3
   img=frame.to_image().convert('RGB');im=Image.open(R/rr['frames'][j]['path']).convert('RGB')
   assert np.array_equal(np.asarray(img),np.asarray(im));decoded.append(j)
 assert i+1==15 and len(decoded)==5
assert sha(R/rr['mp4_path'])==rr['mp4_sha256']
newrow=copy.deepcopy(oldrow)
newrow.update({k:rr[k]for k in ('geometry_path','geometry_sha256','formula_inventory_path','formula_inventory_sha256','mp4_path','mp4_sha256','page_count','video_frames','unique_formulas','source_formula_occurrences')})
newrow.update({k:nb[k]for k in ('source_sha256','record_sha256','math_sha256')})
newrow.update(canonical_frames=rr['frames'],source_path=nb['path'],source_line=nb['source_line'],repair_version_binding=(O/'repair-version-binding.json').relative_to(R).as_posix(),parent_record_sha256=oldrow['record_sha256'])
metrics=[]
for gp,fr in zip(g['pages'],rr['frames']):
 im=Image.open(R/fr['path']);assert im.size==(3840,2160)
 assert sha(R/fr['path'])==fr['sha256']
 ar=np.asarray(im.convert('RGB'))[271:1889,136:3704]
 mask=(ar>32).any(axis=2);yy,xx=np.nonzero(mask);assert len(xx)>0
 height=int(yy.max()-yy.min()+1);width=int(xx.max()-xx.min()+1);items=len(gp['items'])
 metrics.append({'page':gp['page'],'bbox_height':height,'bbox_width':width,'ink_pixels':int(mask.sum()),'displayed_formula_items':items,'metric_scope':'OCCUPIED_BBOX_SLOT_PROXY_NOT_MINIMUM_GLYPH_SIZE','bbox_height_per_displayed_item_px_exact':str(Fraction(height,items)),'slot_proxy_at_1080p_exact':str(Fraction(height,2*items))})
newrow['page_metrics']=metrics;assert sum(x['kind']=='FORMULA_SEGMENT'for x in g['pages'])==2
for i,r in enumerate(rows):
 if r['id']==new['id']:rows[i]=newrow
assert len(rows)==165 and sum(r['page_count']for r in rows)==633
jsonl('DELIVERY_INDEX.jsonl',rows)
idxhash=sha(O/'DELIVERY_INDEX.jsonl')
sel=read(O/'selected-review-pages.json');notes=dict(read(O/'actual-page-notes.json')['notes'])
priorq=read(R/'reviews/codex-supervision/2026-10-08-glyph-continuation/current-page-review-queue.json')
fields=('id','page','path','sha256','record_sha256','math_sha256','formulas','kind','tile','tile_grid')
# Verify every inherited human verdict on the same current version.
cache={}
for p in priorq['pages']:
 if p['review_status']!='PASS_ACTUAL_IMAGE_REVIEW':continue
 vp=R/p['verdict_source'];cache.setdefault(str(vp),list(map(json.loads,vp.read_text('utf-8').splitlines())))
 assert len([v for v in cache[str(vp)]if v['status']=='PASS' and all(v[k]==p[k]for k in fields)])==1
assert sum(p['review_status']=='PASS_ACTUAL_IMAGE_REVIEW'for p in priorq['pages'])==209
oldledger=[]
records=[]
for rid in sorted({p['id']for p in sel}):
 r=c.load_record(oldb,rid);row=next(x for x in map(json.loads,parent.read_text('utf-8').splitlines())if x['id']==rid)
 for k in ('source_sha256','record_sha256','math_sha256'):assert row[k]==oldb[rid][k]
 ip=R/row['formula_inventory_path'];assert sha(ip)==row['formula_inventory_sha256']
 inv=read(ip);assert inv==dict(zip(['unique_formulas','source_occurrences'],native.formula_inventory(r)))
 geo=read(R/row['geometry_path']);assert sha(R/row['geometry_path'])==row['geometry_sha256']
 for p in [z for z in sel if z['id']==rid]:
  gp=geo['pages'][p['page']-1];fr=row['canonical_frames'][p['page']-1]
  assert p['sha256']==sha(R/p['path'])==fr['sha256'] and p['path']==fr['path']
  assert gp['kind']==p['kind'] and [i['formula_index']+1 for i in gp['items']]==[v['index']for v in p['formulas']]
  assert [inv['unique_formulas'][v['index']-1]for v in p['formulas']]==[v['tex']for v in p['formulas']]
  assert Image.open(R/p['path']).size==(3840,2160)
  v=copy.deepcopy(p);v.update(status='PASS',notes=notes[p['ordinal']],review_method='ACTUAL_INDIVIDUAL_PNG_VIEW_3840x2160_DISPLAYED_2048x1152_WITH_TEX_COMPARISON',symbols_checked='See page-specific notes and formula inventory',segment_judgment='PASS_ADJACENT_SEGMENTS_JOIN_AND_OVERLAP'if p['kind']=='FORMULA_SEGMENT'else'NOT_APPLICABLE',math_qualification='SUPERSEDED_BY_REPAIR'if rid==new['id']else'PASS_LOCAL_PROOF_REVIEW')
  oldledger.append(v)
 records.append({'binding':oldb[rid],'record':r})
assert len(oldledger)==55
jsonl('page-glyph-verdicts.jsonl',oldledger);save('bound-math-records-before.json',records)
repairledger=[];repairnotes=read(O/'actual-page-notes.json')['repair_notes']
for gp,fr,note in zip(g['pages'],rr['frames'],repairnotes):
 p={'ordinal':193+gp['page'],'id':new['id'],'page':gp['page'],**{k:fr[k]for k in ('path','sha256')},**{k:nb[k]for k in ('record_sha256','math_sha256')},'kind':gp['kind'],'tile':gp['tile'],'tile_grid':gp['tile_grid'],'formulas':[{'index':i['formula_index']+1,'tex':f[i['formula_index']]}for i in gp['items']]}
 p.update(status='PASS',notes=note,review_method='ACTUAL_INDIVIDUAL_NEW_CANDIDATE_PNG_VIEW_3840x2160_DISPLAYED_2048x1152_WITH_TEX_COMPARISON',symbols_checked='See page-specific notes',segment_judgment='PASS_ADJACENT_SEGMENTS_JOIN_AND_OVERLAP'if gp['kind']=='FORMULA_SEGMENT'else'NOT_APPLICABLE',math_qualification='PASS_EXACT_INTEGRAL_AND_INDEPENDENT_SHELL_METHOD')
 repairledger.append(p)
jsonl('repair-page-glyph-verdicts.jsonl',repairledger)
q=copy.deepcopy(priorq);q.update(index_path=(O/'DELIVERY_INDEX.jsonl').relative_to(R).as_posix(),index_sha256=idxhash,parent_manifest_sha256='6f8d3d488dbb9b4e96dd6bfd4d4f797a6387b9d86defbd6986fdfd29cbc2d258')
current={v['ordinal']:v for v in oldledger if v['id']!=new['id']};current.update({v['ordinal']:v for v in repairledger})
for i,p in enumerate(q['pages']):
 if p['ordinal']in current:
  v=current[p['ordinal']];z={k:v[k]for k in p if k in v};z.update(review_status='PASS_ACTUAL_IMAGE_REVIEW',verdict_source=(O/('repair-page-glyph-verdicts.jsonl'if v['id']==new['id']else'page-glyph-verdicts.jsonl')).relative_to(R).as_posix())
  q['pages'][i]=z
assert len(q['pages'])==633 and sum(p['review_status']=='PASS_ACTUAL_IMAGE_REVIEW'for p in q['pages'])==264
assert len({(p['id'],p['page'])for p in q['pages']})==633
save('current-page-review-queue.json',q)
pending=[p for p in q['pages']if p['review_status']!='PASS_ACTUAL_IMAGE_REVIEW'];assert len(pending)==369
save('unreviewed-pages.json',pending)
save('glyph-coverage-summary.json',{'index_path':q['index_path'],'index_sha256':idxhash,'total_pages':633,'new_current_version_actual_review_pages':55,'actual_images_viewed_in_this_batch':60,'inherited_exact_version_pass_pages':209,'current_version_pass_pages':264,'pending_pages':369,'full_glyph_visual_acceptance':'NOT_ESTABLISHED','minimum_glyph_height':'NOT_CERTIFIED'})
# Exact mathematical checks; all rational constants are Rational/Integer.
checks=[]
def equal(name,a,b):
 assert S.simplify(a-b)==0,name
 checks.append(dict(name=name,status='PASS',difference_exact='0'))
x,y,t,u,v,w=S.symbols('x y t u v w',real=True);a=S.symbols('a',positive=True)
equal('arctan_derivative',S.diff(S.atan(x),x),1/(1+x*x))
equal('arctan_partial_fractions',1/(1+t*t),(1/(t-S.I)-1/(t+S.I))/(2*S.I))
for m in range(1,7):
 equal('arctan_pole_derivative_'+str(m),S.diff(S.atan(t),t,m),(-1)**(m-1)*S.factorial(m-1)/(2*S.I)*((t-S.I)**(-m)-(t+S.I)**(-m)))
equal('arctan_endpoint',S.atan(1),S.pi/4)
N=S.symbols('N',positive=True)
equal('log_N_over_N_limit',S.limit(S.log(N)/N,N,S.oo),0)
equal('x_y_partial_at_1_2',S.diff(x*x,x).subs(x,1),2)
equal('y_partial_at_x1',S.diff(S.exp(y*S.log(x)),y).subs(x,1),0)
equal('double_integral_swap',S.integrate(y*S.exp(y*y),(y,0,1)),(S.E-1)/2)
equal('astroid_first_quadrant',S.integrate(a**S.Rational(1,3)*x**S.Rational(-1,3),(x,0,a)),3*a/2)
equal('washer_square_difference',(S.pi-S.asin(y))**2-S.asin(y)**2,S.pi**2-2*S.pi*S.asin(y))
equal('arcsin_primitive',S.diff(y*S.asin(y)+S.sqrt(1-y*y),y),S.asin(y))
equal('arcsin_integral',S.integrate(S.asin(y),(y,0,1)),S.pi/2-1)
equal('washer_volume',S.pi*S.integrate(S.pi**2-2*S.pi*S.asin(y),(y,0,1)),2*S.pi**2)
equal('independent_shell_volume',2*S.pi*S.integrate(x*S.sin(x),(x,0,S.pi)),2*S.pi**2)
P=S.Matrix([1,2,-1]);Q=S.Matrix([S.Rational(19,9),S.Rational(13,9),S.Rational(1,9)]);normal=S.Matrix([2,-1,2])
equal('plane_foot',normal.dot(Q),3);equal('distance_sq',(P-Q).dot(P-Q),S.Rational(25,9))
assert(P-Q).cross(normal)==S.zeros(3,1);checks.append({'name':'normal_perpendicular_projection','status':'PASS'})
d1=S.Matrix([2,1,-1]);d2=S.Matrix([1,2,1]);delta=S.Matrix([-2,3,-2])
assert d1.cross(d2)==S.Matrix([3,-3,3])
equal('skew_line_triple_product',delta.dot(d1.cross(d2)),-21)
A=S.Matrix([[1,1,1],[1,-1,1],[2,0,2]]);AA=A.row_join(S.Matrix([1,1,2]))
assert A.rank()==AA.rank()==2;checks.append({'name':'three_planes_rank_exact','status':'PASS'})
equal('cross_term_completion',2*(x+y)**2-y*y-w*w,2*x*x+y*y+4*x*y-w*w)
equal('saddle_orthogonal_transform',((u+v)/S.sqrt(2))*((u-v)/S.sqrt(2)),(u*u-v*v)/2)
r=S.Matrix([1+t,t,t]);d=S.Matrix([1,1,1])
equal('sphere_orthogonal_decomposition',r.dot(r),S.Rational(2,3)+3*(t+S.Rational(1,3))**2)
for sign in [-1,1]:
 point=r.subs(t,(-1+sign*S.sqrt(10))/3)
 equal('sphere_intersection_'+str(sign),point.dot(point),4)
equal('sphere_chord',2*S.sqrt(10)/3*S.sqrt(3),2*S.sqrt(S.Rational(10,3)))
protected={'tools/hd_formula_pages.py':'2c60b0616b3be5bb87291de7e1c3c696eb05f5277804a5cc434109c4ae4d1c73','tools/visual_acceptance_verify_pages.py':'64c684dee38c4874a0eb4eb60fd4bf3ceee82369253c865821f16d8817a5a988'}
for name,h in protected.items():assert sha(R/name)==h
save('independent-verification.json',{'status':'PASS_LOCAL_BINDINGS_REPAIR_RENDER_AND_EXACT_MATH','selected_old_pages':55,'candidate_pages':5,'current_pass_pages':264,'pending_pages':369,'source_records_reviewed':len(records),'symbolic_checks':checks,'new_index_sha256':idxhash,'changed_source_sha256':nb['source_sha256'],'new_record_sha256':nb['record_sha256'],'new_math_sha256':nb['math_sha256'],'protected_code_hashes':protected,'semantic_isolation':'NOT_ESTABLISHED','production':'CLOSED','full_glyph_visual_acceptance':'NOT_ESTABLISHED'})
print(json.dumps({'status':'PASS_LOCAL_BINDINGS_REPAIR_RENDER_AND_EXACT_MATH','records':len(records),'checks':len(checks),'current_pass':264,'pending':369,'new_index_sha256':idxhash}))
