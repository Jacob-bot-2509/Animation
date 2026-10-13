import hashlib,json,sys
from pathlib import Path
import sympy as s
ROOT=Path(r'D:\Animation-Model-Training');OUT=Path(__file__).resolve().parent;sys.path.insert(0,str(ROOT/'tools'))
checks=[]
def eq(name,lhs,rhs):
 result=s.simplify(lhs-rhs)
 if hasattr(result,'is_zero_matrix'):passed=result.is_zero_matrix is True
 else:passed=result==0
 assert passed,(name,lhs,rhs,result)
 checks.append({'name':name,'lhs':str(lhs),'rhs':str(rhs),'passed':True})
def truth(name,test,detail):
 assert test,name;checks.append({'name':name,'passed':True,'exact_evidence':detail})
x,u,t,a,b,k,n=s.symbols('x u t a b k n',real=True);nn=s.symbols('n',integer=True,positive=True);i=s.symbols('i',integer=True,positive=True)
eq('parabolic area',s.integrate(2-2*x*x,(x,-1,1)),s.Rational(8,3))
eq('triangle area',s.integrate(1-s.Abs(x),(x,-1,1)),1)
eq('three-petal leaf',s.integrate((2*s.sin(3*t))**2/2,(t,0,s.pi/3)),s.pi/3)
eq('four-petal total',4*s.integrate(s.cos(2*t)**2/2,(t,-s.pi/4,s.pi/4)),s.pi/2)
eq('lunar polar area',s.integrate(((4*s.cos(t))**2-4)/2,(t,-s.pi/3,s.pi/3)),4*s.pi/3+2*s.sqrt(3))
eq('lemniscate',2*s.integrate(s.cos(2*t)/2,(t,-s.pi/4,s.pi/4)),1)
eq('cycloid factor',s.integrate((1-s.cos(t))**2,(t,0,2*s.pi)),3*s.pi)
eq('astroid integral',s.integrate(s.sin(t)**4*s.cos(t)**2,(t,0,s.pi/2)),s.pi/32)
eq('folium factor',s.integrate(9*t*t/(1+t**3)**2/2,(t,0,s.oo)),s.Rational(3,2))
eq('Green closing segment',s.integrate(3*t-3,(t,0,1)),-s.Rational(3,2))
eq('power series endpoint log',s.limit(nn+nn**2*s.log(nn/(nn+1)),nn,s.oo),s.Rational(1,2))
S=(1-x)/(1-x-2*x*x);eq('recurrence sum point',S.subs(x,s.Rational(1,4)),s.Rational(6,5));eq('recurrence fractions',S,1/(3*(1-2*x))+2/(3*(1+x)))
truth('exact minimal error N',s.Rational(1,4*3**5)>s.Rational(1,2500)>s.Rational(1,4*3**6),'3^5=243<625<729=3^6')
truth('Leibniz-only minimal N',s.Rational(1,3**7)>s.Rational(1,2500)>s.Rational(1,3**8),'3^7=2187<2500<6561=3^8')
truth('old arbitrary odd chain counterexample',s.Rational(5,6)>s.Rational(47,60),'a_n=1/n: S3=5/6>S5=47/60')
A=s.Matrix([[0,1,0],[-1,0,0],[0,0,1]]);bv=s.Matrix([1,2,3]);eq('affine inverse translation',-A.T*bv,s.Matrix([2,-1,-3]))
At=s.Matrix([[1,2],[t,t*t]]);eq('parameter determinant',At.det(),t*(t-2));eq('parameter inverse adjugate',At*s.Matrix([[t*t,-2],[-t,1]]),t*(t-2)*s.eye(2))
inv=s.Matrix([[1,2],[0,-1]]);eq('linear involution',inv**2,s.eye(2));eq('involution not isometry norm',((inv*s.Matrix([0,1])).T*(inv*s.Matrix([0,1])))[0],5)
Ak=s.Matrix([[1,k],[0,2]]);P=s.Matrix([[1,k],[0,1]]);eq('parameter diagonalization',Ak*P,P*s.diag(1,2))
T=s.Matrix([[0,0,1,0],[0,0,0,1],[0,0,0,0],[0,0,0,0]]);U=s.Matrix([[0,1,0,0],[0,0,1,0],[0,0,0,0],[0,0,0,0]]);truth('nilpotent ranks',[ (T**j).rank() for j in range(4)]==[4,2,0,0] and [(U**j).rank() for j in range(4)]==[4,2,1,0],'T:4,2,0;U:4,2,1,0')
w=2*i/(nn*(nn+1));v=s.summation(w*w,(i,1,nn))/12;eq('weighted variance',v,(2*nn+1)/(18*nn*(nn+1)));eq('weighted Chebyshev n100',(100*v).subs(nn,100),s.Rational(67,606))
N=s.kronecker_product(s.Matrix([[0,1],[0,0]]),s.eye(2))+s.kronecker_product(s.eye(2),s.Matrix([[0,1],[0,0]]));Q=s.Matrix([[2,0,0,0],[0,1,0,1],[0,1,0,-1],[0,0,1,0]]);J=s.diag(s.Matrix([[0,1,0],[0,0,1],[0,0,0]]),s.zeros(1));eq('tensor Jordan chain',N*Q,Q*J)
H=s.Matrix([[4,2,1],[0,4,3],[0,0,4]]);Q=s.Matrix([[6,1,0],[0,3,0],[0,0,1]]);eq('explicit Jordan chain',H*Q,Q*s.Matrix([[4,1,0],[0,4,1],[0,0,4]]))
W=s.diag(1,2,3);nv=s.ones(3,1);c=t*s.Matrix([6,3,2])/11;eq('ellipsoid center normal',W*c,6*t*nv/11);eq('ellipsoid minimum',(c.T*W*c)[0],6*t*t/11);e=s.Matrix([1,-1,0])/s.sqrt(2);f=s.Matrix([1,1,-2])/s.sqrt(6);Q=s.Matrix.hstack(e,f);B=Q.T*W*Q;lam=s.symbols('lambda');eq('ellipse characteristic',B.charpoly(lam).as_expr(),(lam-2)**2-s.Rational(1,3))
rv=s.symbols('r',positive=True);pts=[s.Matrix([0,0,1]),s.Matrix([0,0,-1]),s.Matrix([rv,rv*rv,0]),s.Matrix([-rv,rv*rv,0])];eq('nonplanar four point determinant',s.Matrix.hstack(*(p-pts[0] for p in pts[1:])).det(),-4*rv**3)
e12=s.zeros(3);e12[0,1]=1;e23=s.zeros(3);e23[1,2]=1;e13=s.zeros(3);e13[0,2]=1;I=s.eye(3);eq('noncommuting order zero',e23*e12,s.zeros(3));eq('opposite order nonzero',e12*e23,e13);eq('four-factor commutator',(I+a*e12)*(I+b*e23)*(I-a*e12)*(I-b*e23),I+a*b*e13)
D=s.Matrix([[1,1,1],[1,1,2],[1,2,a]]);eq('Cramer determinant',D.det(),-1);eq('Cramer actual solution',D*s.Matrix([a-3,3-a,1]),s.Matrix([1,2,3]))
fpoly=x**3+x*x+2;eq('finite difference',s.expand(fpoly.subs(x,x+1)-fpoly),3*x*x+5*x+2)
g=[(9-15*x*x)/8,3*x/2,(-15+45*x*x)/8]
for ii in range(3):
 for jj in range(3):eq(f'dual pairing {ii},{jj}',s.integrate(g[ii]*x**jj,(x,-1,1)),int(ii==jj))
eq('nonuniform density event',s.integrate(x+s.Rational(1,2),(x,0,s.Rational(1,2))),s.Rational(3,8))
eq('Poisson comparison coefficient',s.Rational(49,50)**2+s.Rational(49,50)+s.Rational(49,100),s.Rational(1519,625));truth('log comparison exact positive',s.Rational(37,1225)-s.Rational(87,3038)>0,str(s.Rational(37,1225)-s.Rational(87,3038)))
eq('normal coefficient square',s.Rational(9,4)**2,s.Rational(81,16));eq('normal repaired variance',s.Rational(9,4)**2*4+9,s.Rational(117,4));eq('normal independence covariance',4*s.Rational(9,4)-9,0)
mu,eps,M,tau=s.symbols('mu epsilon M tau',positive=True);eq('truncated mean Chebyshev threshold',M*M/(nn*(eps/3)**2),9*M*M/(nn*eps**2));eq('averaged tail Markov threshold',tau/(eps/3),3*tau/eps);eq('Cauchy density interval bound',(1/s.pi)*(2*s.pi/8),s.Rational(1,4))
# Bind claims to the exact corrected patch bytes; these checks are scoped, not all-scene acceptance.
p=OUT/'scene-candidates-corrected-v5.json';result={'checks':checks,'passed':len(checks),'patches_raw_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'scope':'named exact formulas/counterexamples; model scene review distinct from visual acceptance','visual_verified':False,'training_admitted':False};(OUT/'exact-math-checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps({'exact_checks':len(checks),'passed':True}))