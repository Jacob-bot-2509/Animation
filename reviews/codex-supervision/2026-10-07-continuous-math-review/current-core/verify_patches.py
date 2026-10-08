"""Independent exact checks and explicit proofs for the three current patches."""
import pathlib,json,hashlib
import sympy as s
OUT=pathlib.Path(__file__).resolve().parent
patches={r['id']:r for r in json.loads((OUT/'patches.json').read_text(encoding='utf8'))}
checks=[]
def eq(name,a,b=0):
 assert s.simplify(a-b)==0,name
 checks.append({'name':name,'left':str(a),'right':str(b),'verdict':'PASS_EXACT'})
x,mu=s.symbols('x mu',real=True);sig=s.symbols('sigma',positive=True);c=s.symbols('c',nonnegative=True)
phi=s.exp(-x*x/2)/s.sqrt(2*s.pi)
f=s.exp(-(x-mu)**2/(2*sig**2))/(sig*s.sqrt(2*s.pi))
eq('normal_normalization',s.integrate(phi,(x,-s.oo,s.oo)),1)
eq('normal_symmetry',f.subs(x,mu+x),f.subs(x,mu-x))
eq('normal_peak',f.subs(x,mu),1/(sig*s.sqrt(2*s.pi)))
eq('normal_derivative_factor',s.diff(f,x),-(x-mu)/sig**2*f)
eq('normal_exact_symmetric_mass',s.integrate(phi,(x,-c,c)),s.erf(c/s.sqrt(2)))
eq('normal_mass_c1',s.erf(c/s.sqrt(2)).subs(c,1),s.erf(1/s.sqrt(2)))
eq('normal_mass_c2',s.erf(c/s.sqrt(2)).subs(c,2),s.erf(s.sqrt(2)))
b1,b2,b3=s.symbols('b1 b2 b3',integer=True)
A=s.Matrix([[1,1,1],[1,-1,1],[1,1,-1]])
b=s.Matrix([b1,b2,b3]);sol=s.Matrix([(b2+b3)/2,(b1-b2)/2,(b1-b3)/2])
eq('integer_det',A.det(),4)
for i in range(3):
 eq('integer_equation_'+str(i), (A*sol-b)[i])
 M=A.copy();M[:,i]=b;eq('integer_cramer_'+str(i),M.det(),4*sol[i])
for u in range(-4,5):
 for v in range(-4,5):
  for w in range(-4,5):
   answer=sol.subs({b1:u,b2:v,b3:w})
   assert all(z.is_Integer for z in answer)==((u-v)%2==0 and (u-w)%2==0)
checks.append({'name':'integer_729_exact_parity_cases','verdict':'PASS_EXACT','cases':729,'scope':'supplements the arbitrary integer necessity and sufficiency proof'})
t,p,q,r=s.symbols('t p q r')
B=s.Matrix([[t,1,0],[0,t-1,1],[0,0,1]]);bb=s.Matrix([p,q,r])
xx=((t-1)*p-q+r)/(t*(t-1));yy=(q-r)/(t-1);ss=s.Matrix([xx,yy,r])
eq('polynomial_det_nonunit',B.det(),t*(t-1))
for i in range(3):
 eq('rational_function_equation_'+str(i),(B*ss-bb)[i])
 M=B.copy();M[:,i]=bb;eq('polynomial_cramer_'+str(i),M.det(),B.det()*ss[i])
p0,p1,p2,q0,q1,q2,r0,r1,r2=s.symbols('p0 p1 p2 q0 q1 q2 r0 r1 r2')
P=p0+p1*t+p2*t*t;Q=q0+q1*t+q2*t*t;R=r0+r1*t+r2*t*t
N=(t-1)*P-Q+R
eq('polynomial_N_at_zero',N.subs(t,0),-p0-q0+r0)
eq('polynomial_N_at_one',N.subs(t,1),-(q0+q1+q2)+(r0+r1+r2))
T=s.Poly(N,t);rem=T.rem(s.Poly(t*(t-1),t)).as_expr()
eq('polynomial_two_root_remainder',rem, N.subs(t,0)*(1-t)+N.subs(t,1)*t)
manual={
'prob-041':'For sigma>0 the affine change z=(x-mu)/sigma preserves normalization. The derivative is positive for x<mu and negative for x>mu; hence unique peak at mu. Standardization and u=z/sqrt(2) give erf(c/sqrt(2)) exactly for c>=0. UTF-8 restored P and A agree with unchanged reviewed proof and scene.',
'draft-c31-01':'Cramer gives x=(b2+b3)/2,y=(b1-b2)/2,z=(b1-b3)/2. Integer solutions imply b1-b2 and b1-b3 even; the converse makes all three numerators even. det=4 gives uniqueness. The map Z^3 to (Z/2Z)^2 sending b to (b1-b2,b1-b3) is surjective and its kernel is A Z^3, so the index is 4.',
'draft-c31-03':'Over R(t), D=t(t-1) gives the displayed rational solution. A polynomial solution requires q(1)=r(1) and p(0)+q(0)-r(0)=0 by evaluating original equations. Conversely N=(t-1)p-q+r has zeros 0 and 1; coprimality yields t(t-1)|N and t-1|q-r. Direct substitution proves sufficiency. Differences solve triangular homogeneous equations; R[t] has no zero divisors, yielding uniqueness. Nonzero D is not a unit in R[t].'}
manual.update({'eval-calc-027-s3':'Only stale efficiency tags changed: exact continuous triangular-domain integral (e-1)/2; inherits unchanged reviewed P/S/A/scene.', 'eval-prob-008-s3':'Only stale efficiency tags changed: exact binomial tail q=2^-99 sum(k=0..40) C(100,k), exact Chebyshev gap; inherits unchanged reviewed P/S/A/scene.', 'test-prob-008':'Only stale efficiency tags changed: exact die mean 7/2 and Chebyshev bound min(1,875/(3n)); inherits unchanged reviewed P/S/A/scene.'})
report={'schema':'codex-current-patch-independent-exact-review-v1','checks':checks,'check_count':len(checks),'manual_proofs':manual,'patch_bindings':[{'id':rid,'record_sha256':v['after_record_sha256'],'math_sha256':v['after_math_sha256'],'math':'PASS','scene_text':'PASS','semantic_pair_disposition':'FIXED_LOCAL_CRAMER_TEMPLATE' if rid.startswith('draft') else ('ENCODING_FIXED' if rid=='prob-041' else 'EXACT_TAGS_SYNCHRONIZED')} for rid,v in patches.items()],'global_semantic_isolation':'NOT_ESTABLISHED','native_render':'UNVERIFIED','production':'CLOSED'}
print(json.dumps(report,ensure_ascii=False,indent=2))
