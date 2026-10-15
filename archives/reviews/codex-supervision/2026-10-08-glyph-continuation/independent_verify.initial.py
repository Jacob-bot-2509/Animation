"""Verify new manual evidence bindings and exact algebra, without inventing visual verdicts."""
import pathlib,json,hashlib,datetime
from PIL import Image
import sympy as S
R=pathlib.Path(__file__).resolve().parents[3];O=pathlib.Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,v):
 with(O/n).open('xb')as f:f.write((json.dumps(v,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
def dense(d):return hashlib.sha256(json.dumps(d,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def mathsha(d):return hashlib.sha256(json.dumps({k:d.get(k)for k in ('problem','solution','answer','scene_spec')},ensure_ascii=False,sort_keys=True).encode()).hexdigest()
idx=R/'reviews/codex-supervision/2026-10-08-glyph-review-followup/DELIVERY_INDEX.jsonl'
assert sha(idx)=='07b4543d38599e1c30d2b515e0c2a8761e5611f771c46c75ee23b357c58b6331'
q=json.loads((O/'current-page-review-queue.json').read_text('utf-8'));sel=json.loads((O/'selected-review-pages.json').read_text('utf-8'))
rows={x['id']:x for x in map(json.loads,idx.read_text('utf-8').splitlines())}
bindingpath=R/'reviews/codex-supervision/2026-10-07-deep-isolation-followup/effective-core-v3/record-bindings.jsonl'
bindings={x['id']:x for x in map(json.loads,bindingpath.read_text('utf-8').splitlines())}
cache={};copies=[];fields=('id','page','path','sha256','record_sha256','math_sha256','formulas','kind','tile','tile_grid')
for p in q['pages']:
 if p['review_status']!='PASS_ACTUAL_IMAGE_REVIEW':continue
 ledger=R/p['verdict_source']
 if str(ledger)not in cache:cache[str(ledger)]=list(map(json.loads,ledger.read_text('utf-8').splitlines()))
 matches=[v for v in cache[str(ledger)]if v['status']=='PASS'and all(p[k]==v[k]for k in fields)]
 assert len(matches)==1,(p['id'],p['page'],'missing bound actual verdict')
assert sum(p['review_status']=='PASS_ACTUAL_IMAGE_REVIEW'for p in q['pages'])==209
assert len(q['pages'])==len({(p['id'],p['page'])for p in q['pages']})==633
for rid in sorted({p['id']for p in sel}):
 row=rows[rid];b=bindings[rid];src=R/b['path'];assert sha(src)==b['source_sha256']==row['source_sha256']
 rec=json.loads(src.read_text('utf-8').splitlines()[b['source_line']-1])
 assert dense(rec)==b['record_sha256']==row['record_sha256']
 assert mathsha(rec)==b['math_sha256']==row['math_sha256']
 invpath=R/row['formula_inventory_path'];assert sha(invpath)==row['formula_inventory_sha256']
 inv=json.loads(invpath.read_text('utf-8'))
 gpath=R/row['geometry_path'];assert sha(gpath)==row['geometry_sha256']
 geo=json.loads(gpath.read_text('utf-8'))
 for p in [z for z in sel if z['id']==rid]:
  gp=geo['pages'][p['page']-1];fr=row['canonical_frames'][p['page']-1]
  assert gp['page']==p['page']and gp['kind']==p['kind']and fr['path']==p['path']and fr['sha256']==p['sha256']
  assert sha(R/p['path'])==p['sha256']
  with Image.open(R/p['path'])as im:assert im.size==(3840,2160)
  for f in p['formulas']:assert inv['unique_formulas'][f['index']-1]==f['tex']
 copies.append(dict(binding=b,record=rec))
save('bound-math-records.json',copies)
# These assertions prove symbolic identities, not glyph visibility.
x,t=S.symbols('x t',real=True);n,N=S.symbols('n N',integer=True,positive=True);p=S.symbols('p',real=True)
checks=[]
def equal(name,a,b):
 assert S.simplify(a-b)==0,name
 checks.append(dict(name=name,status='PASS',difference_exact='0'))
equal('tan_pi_12_exact',S.tan(S.pi/12),2-S.sqrt(3))
equal('symmetry_g',S.sin(S.pi-x)/(1+S.cos(S.pi-x)**2),S.sin(x)/(1+S.cos(x)**2))
equal('cos_substitution_integral',S.integrate(1/(1+t**2),(t,-1,1)),S.pi/2)
equal('I_exact',S.pi/2*S.pi/2,S.pi**2/4)
equal('p_integral_primitive_derivative',S.diff(x**(1-p)/(1-p),x),x**(-p))
equal('geometric_series_second_derivative',S.diff(x/(1-x),x,2),2/(1-x)**3)
equal('sum_n_squared_generating_identity',2*x**2/(1-x)**3+x/(1-x)**2,x*(1+x)/(1-x)**3)
equal('sum_n_squared_at_half',(x*(1+x)/(1-x)**3).subs(x,S.Rational(1,2)),6)
F1=lambda z:2-(z+2)/2**z
F2=lambda z:6-(z**2+4*z+6)/2**z
equal('finite_sum_n_base',F1(1),S.Rational(1,2))
equal('finite_sum_n_induction',F1(N)-F1(N-1),N/2**N)
equal('finite_sum_n_squared_base',F2(1),S.Rational(1,2))
equal('finite_sum_n_squared_induction',F2(N)-F2(N-1),N**2/2**N)
equal('arctan_remainder_primitive_bound',S.integrate(t**(2*N+2),(t,0,x)),x**(2*N+3)/(2*N+3))
equal('arctan_finite_geometric_remainder',1/(1+t**2),(1-(-t**2)**(N+1))/(1+t**2)+(-1)**(N+1)*t**(2*N+2)/(1+t**2))
protected={'tools/hd_formula_pages.py':'2c60b0616b3be5bb87291de7e1c3c696eb05f5277804a5cc434109c4ae4d1c73',
'tools/visual_acceptance_verify_pages.py':'64c684dee38c4874a0eb4eb60fd4bf3ceee82369253c865821f16d8817a5a988'}
for name,h in protected.items():assert sha(R/name)==h
save('independent-verification.json',dict(status='PASS_BINDINGS_AND_EXACT_ALGEBRA_ONLY',selected_actual_review_pages=39,current_bound_pass_pages=209,pending_pages=424,source_records=10,source_bindings_sha256=sha(bindingpath),symbolic_checks=checks,protected_code_hashes=protected,full_glyph_visual_acceptance='NOT_ESTABLISHED',minimum_glyph_height='NOT_CERTIFIED'))
print(json.dumps(dict(status='PASS_BINDINGS_AND_EXACT_ALGEBRA_ONLY',pages=39,inherited=170,pending=424,records=10,exact_algebra_checks=len(checks))))
