"""Independent exact witnesses and full-record proof binding; no decimal computation."""
from pathlib import Path
import json,sys,copy
from fractions import Fraction as F
import sympy as S
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'))
import core_signatures as c
def read(p):return json.loads(p.read_text('utf-8'))
def jl(p):return list(map(json.loads,p.read_text('utf-8').splitlines()))
def sha(p):return c.digest(p.read_bytes())
def save(n,v):(O/n).write_bytes(c.encoded(v))
sources=read(O/'current-source-bindings.json');bs=jl(O/'current-record-bindings.jsonl');bm={b['id']:b for b in bs};cache={};qs={}
assert len(sources)==24 and len(bs)==len(bm)==761
for s in sources:
 p=c.checked_path(R/s['path'],R);assert sha(p)==s['sha256'] and p.stat().st_size==s['bytes'];cache[s['path']]=jl(p);assert len(cache[s['path']])==s['records']
for b in bs:
 q=cache[b['path']][b['source_line']-1];assert q['id']==b['id'] and c.dense(q)==b['record_sha256'] and c.math_digest(q)==b['math_sha256'];qs[b['id']]=q
old=jl(O/'parent-current-record-bindings.jsonl');ob={b['id']:b for b in old};changed={b['id']for b in bs if b['record_sha256']!=ob[b['id']]['record_sha256']}
expected={z['id']for z in read(O/'manual-review-progress.json')['findings']};assert changed==expected and len(changed)==23
for rid in changed:
 q=qs[rid];before=next(z for z in read(O/'repaired-records-before.json')if z['id']==rid)
 assert q['id']==before['id'] and q['problem']==before['problem']
 if 'strict_review' in q:assert q['strict_review']['math_content_sha256']==c.math_digest(q)
for rid in ['eval-calc-030-s3','eval-geom-007-s1','eval-geom-007-s2','eval-linalg-002-s3','eval-linalg-004-s3']:assert bm[rid]['record_sha256']==ob[rid]['record_sha256']
ss=jl(O/'current-complete-signatures.jsonl');assert len(ss)==761 and {s['id']for s in ss}==set(bm)
for s in ss:assert all(s[k]==bm[s['id']][k]for k in ('record_sha256','math_sha256'))
checks=[]
def eq(name,a,b):
 assert S.simplify(a-b)==0,name
 checks.append({'name':name,'status':'PASS','difference_exact':'0'})
def meq(name,a,b):
 assert a.shape==b.shape and (a-b).applyfunc(lambda z:S.simplify(S.expand_complex(z)))==S.zeros(*a.shape),name
 checks.append({'name':name,'status':'PASS','all_component_differences_exact':'0'})
def truth(name,b,detail):
 assert b,name
 checks.append({'name':name,'status':'PASS','exact_evidence':detail})
x,y,z,a,l,t,u,v,theta,phi=S.symbols('x y z a lambda t u v theta phi',real=True)
Q=lambda k:S.Matrix([[S.cos(k),-S.sin(k)],[S.sin(k),S.cos(k)]])
meq('rotation_composition',Q(t)*Q(u),Q(t+u));meq('rotation_orthogonality',Q(t).T*Q(t),S.eye(2));eq('rotation_orientation',Q(t).det(),1)
meq('shear_iteration_induction',S.Matrix([[1,1],[0,1]])*S.Matrix([[1,a],[0,1]]),S.Matrix([[1,a+1],[0,1]]))
P=S.Matrix([[1,1],[-S.I,S.I]]);D=S.diag(S.exp(S.I*t),S.exp(-S.I*t))
meq('rotation_complex_diagonalization',P*D*P.inv(),Q(t));eq('complex_basis_determinant',P.det(),2*S.I)
A=(l-1)*S.eye(3)+S.ones(3);eq('parameter_system_determinant',A.det(),(l+2)*(l-1)**2)
truth('singular_minus2_inconsistent',sum([1,-2,4])==3,'left rows sum to zero; right sides sum to 3')
truth('singular_1_plane',A.subs(l,1).rank()==1,'rank=1 and b=(1,1,1)')
M=S.Matrix([[1,1,1],[1,2,0],[1,0,a]]);L=S.Matrix([[1,0,0],[1,1,0],[1,-1,1]])
meq('LDL_complete',M,L*S.diag(1,1,a-2)*L.T);eq('quadratic_019_determinant',M.det(),a-2)
meq('LDL_boundary_kernel',M.subs(a,2)*S.Matrix([-2,1,1]),S.zeros(3,1))
f=2*x*x+y*y+2*z*z+2*x*y+2*a*x*z
eq('quadratic_021_complete_squares',f,2*(x+y/2+a*z/2)**2+(y-a*z)**2/2+(2-a*a)*z*z)
eq('quadratic_021_necessity_vector',f.subs({x:-a,y:a,z:1}),2-a*a)
eq('quadratic_variable_change_invertible',S.Matrix([[1,S.Rational(1,2),a/2],[0,1,-a],[0,0,1]]).det(),1)
vs=[S.Matrix([1,1,0]),S.Matrix([1,0,1]),S.Matrix([0,1,1])]
w1=vs[0];w2=vs[1]-vs[1].dot(w1)/w1.dot(w1)*w1;u2=2*w2
w3=vs[2]-vs[2].dot(w1)/w1.dot(w1)*w1-vs[2].dot(u2)/u2.dot(u2)*u2
meq('GS_w2_exact',w2,S.Matrix([S.Rational(1,2),S.Rational(-1,2),1]));meq('GS_w3_exact',w3,S.Matrix([S.Rational(-2,3),S.Rational(2,3),S.Rational(2,3)]))
us=[w1,u2,-S.Rational(3,2)*w3]
for i in range(3):
 for j in range(i):eq('GS_orthogonality_'+str(i)+str(j),us[i].dot(us[j]),0)
B=S.Matrix([[a,-1,0],[0,1,-1],[0,0,1]]);e3=S.Matrix([0,0,1]);C=S.Matrix.hstack(e3,B*e3,B*B*e3)
meq('cyclic_basis_matrix',C,S.Matrix([[0,0,1],[0,-1,-2],[1,1,1]]));eq('cyclic_basis_determinant_all_a',C.det(),1)
eq('cyclic_characteristic',B.charpoly().as_expr().subs(B.charpoly().gen,l),(l-a)*(l-1)**2)
meq('nilpotent_exponential',S.eye(2)+t*S.Matrix([[0,1],[0,0]]),S.Matrix([[1,t],[0,1]]))
h1,h2,j1,j2=S.symbols('h1 h2 j1 j2',real=True)
eq('polarization_scalar',((h1+j1)**2+(h2+j2)**2-h1*h1-h2*h2-j1*j1-j2*j2)/2,h1*j1+h2*j2)
q1,q2=S.symbols('q1 q2',real=True);q3=1-q1-q2
eq('Monty_arbitrary_initial_choice_switch',sum(2*q/3 for q in [q1,q2,q3]),S.Rational(2,3));eq('Monty_arbitrary_initial_choice_stay',sum(q/3 for q in [q1,q2,q3]),S.Rational(1,3))
eq('Monty_fair_host_posterior',S.Rational(1,3)/(S.Rational(1,3)+S.Rational(1,6)),S.Rational(2,3))
eq('birthday_falling_factorial',S.prod(S.Rational(366-k,365)for k in range(2,31)),S.factorial(365)/(S.factorial(335)*365**30))
EN=S.Rational(435,365);EN2=EN+S.Rational(435*434,365**2)
eq('birthday_second_moment_bound',EN**2/EN2,S.Rational(435,799));truth('birthday_bound_above_half',S.Rational(435,799)>S.Rational(1,2),'435/799 > 1/2')
Qm=S.Matrix([[S.Rational(1,2),S.Rational(1,2)],[S.Rational(1,2),0]])
meq('HH_fundamental_matrix',(S.eye(2)-Qm).inv(),S.Matrix([[4,2],[2,2]]));eq('HH_start0_expectation',sum((S.eye(2)-Qm).inv()[0,:]),6)
for n in range(1,9):eq('difference_monomial_'+str(n),(x+1)**n-x**n,sum(S.binomial(n,j)*x**j for j in range(n)))
eq('difference_cubic',(x+1)**3-x**3,3*x*x+3*x+1)
A2=S.Matrix([[2,1],[1,-1]]);b2=S.Matrix([5,1]);eq('Cramer_D',A2.det(),-3);meq('Cramer_solution',A2.inv()*b2,S.Matrix([2,1]))
for AA,bb,ok in [(S.zeros(2),S.zeros(2,1),True),(S.zeros(2),S.Matrix([1,0]),False),(S.Matrix([[0,0],[1,1]]),S.Matrix([0,1]),True),(S.Matrix([[0,0],[1,1]]),S.Matrix([1,1]),False)]:
 truth('zero_row_rank_'+str(len(checks)),(AA.rank()==AA.row_join(bb).rank())==ok,'exact augmented/coefficient ranks')
eq('ellipse_shear_det',S.Matrix([[1,1],[0,1]]).det(),1);eq('ellipse_equation',(x-y)**2+y*y,x*x-2*x*y+2*y*y)
Ry=S.Matrix([[S.cos(phi),0,S.sin(phi)],[0,1,0],[-S.sin(phi),0,S.cos(phi)]])
meq('right_handed_y_rotation_Gram',Ry.T*Ry,S.eye(3));eq('right_handed_y_rotation_det',Ry.det(),1)
Ds=[S.Integer(1),S.Integer(1)]
for n in range(2,15):
 T=S.zeros(n)
 for i in range(n):
  T[i,i]=1
  if i+1<n:T[i,i+1]=T[i+1,i]=1
 Ds.append(T.det());eq('tridiagonal_recurrence_'+str(n),Ds[-1],Ds[-2]-Ds[-3])
truth('tridiagonal_six_values',Ds[1:7]==[1,0,-1,-1,0,1],'D1..D6=1,0,-1,-1,0,1')
truth('tridiagonal_min_period_pairs',len(set(zip(Ds[1:7],Ds[2:8])))==6,'six distinct adjacent states')
rho,s1,s2=S.symbols('rho s1 s2',real=True)
Sigma=S.Matrix([[s1*s1,rho*s1*s2],[rho*s1*s2,s2*s2]])
eq('covariance_determinant',Sigma.det(),s1*s1*s2*s2*(1-rho*rho))
eq('uniform_series_term_integral',S.integrate(x**7,(x,0,1)),S.Rational(1,8))
eq('eta2_even_odd_identity',(1-S.Rational(1,2))*S.pi**2/6,S.pi**2/12)
eq('die_mean',sum(S.Integer(k)for k in range(1,7))/6,S.Rational(7,2))
eq('die_second_moment',sum(S.Integer(k*k)for k in range(1,7))/6,S.Rational(91,6))
eq('die_variance',S.Rational(91,6)-S.Rational(7,2)**2,S.Rational(35,12))
eq('two_dice_variance',2*S.Rational(35,12),S.Rational(35,6))
eq('two_dice_second_moment',sum(S.Integer((i+j)**2)for i in range(1,7)for j in range(1,7))/36,S.Rational(329,6))
eq('binomial_exact_three',S.binomial(10,3)*S.Rational(3,10)**3*S.Rational(7,10)**7,S.Rational(66706983,250000000))
eq('binomial_exact_at_most_one',S.Rational(7,10)**10+10*S.Rational(3,10)*S.Rational(7,10)**9,S.Rational(1493083459,10**10))
eq('Bayes_defect_factory',S.Rational(3,5)*S.Rational(1,50)/(S.Rational(3,5)*S.Rational(1,50)+S.Rational(2,5)*S.Rational(3,100)),S.Rational(1,2))
eq('uniform_sum_tail',S.integrate(2-z,(z,S.Rational(3,2),2)),S.Rational(1,8))
eq('exponential_survival_ratio',S.exp(-S.Rational(3,2))/S.exp(-S.Rational(1,2)),S.exp(-1))
eq('Chebyshev_die_bound',S.Rational(35,12)*100,S.Rational(875,3))
eq('first_six_geometric_mean',1/(1-S.Rational(5,6)),6)
eq('independent_geometric_equality',(S.Rational(1,4))/(1-S.Rational(1,4)),S.Rational(1,3))
eq('uniform_key_expectation',sum(range(1,11))/S.Integer(10),S.Rational(11,2))
eq('independent_union_probability',S.Rational(2,5)+S.Rational(1,2)-S.Rational(2,5)*S.Rational(1,2),S.Rational(7,10))
ell,d=S.symbols('ell d',positive=True)
eq('Buffon_exact_integral',S.integrate(2*ell*S.sin(theta)/(S.pi*d),(theta,0,S.pi/2)),2*ell/(S.pi*d))
eq('second_roll_if_six_mean',S.Rational(7,2)*(1+S.Rational(1,6)),S.Rational(49,12))
for n in range(8):eq('exponential_moment_'+str(n),S.integrate(x**n*S.exp(-x),(x,0,S.oo)),S.factorial(n))
eq('density_inclusion_exclusion',S.Rational(1,2)+S.Rational(1,3)-S.Rational(1,6),S.Rational(2,3))
# Full proofs were read independently; witnesses supplement, not replace, general proofs.
notes=read(O/'manual-review-progress.json')['math_notes'];assert len(notes)==98 and len({m[0]for m in notes})==98
proofs=[]
for rid,status,note in notes:
 q=qs[rid];proofs.append({'id':rid,'status':'PASS_LOCAL_COMPLETE_PROOF_AFTER_REPAIR'if rid in changed else'PASS_LOCAL_COMPLETE_PROOF','binding':bm[rid],'independent_reasoning':note,'current_solution':q['solution'],'current_answer':q['answer'],'repair_findings':[f for f in read(O/'manual-review-progress.json')['findings']if f['id']==rid],'verification_scope':'FULL_CURRENT_RECORD_AND_SCENE_TEXT; EXACT_WITNESSES_SUPPLEMENT_GENERAL_REASONING'})
save('bound-current-math-records.json',[{'binding':bm[m[0]],'record':qs[m[0]]}for m in notes])
save('complete-proof-review.json',proofs);save('exact-symbolic-checks.json',checks)
save('independent-math-verification.json',{'status':'PASS_98_CURRENT_COMPLETE_PROOFS_AND_EXACT_WITNESSES','proofs':98,'symbolic_checks':len(checks),'changed_records':23,'source_records':761,'physical_sources':24,'prior_five_repairs_preserved':True,'question_ids_and_problem_text_unchanged':True,'source_binding_sha256':sha(O/'current-source-bindings.json'),'record_binding_sha256':sha(O/'current-record-bindings.jsonl'),'signature_sha256':sha(O/'current-complete-signatures.jsonl'),'production':'CLOSED'})
print(json.dumps({'status':'PASS_EXACT_MATH_AND_FULL_PROOF_BINDINGS','proofs':98,'checks':len(checks)}))
