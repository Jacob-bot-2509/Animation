from pathlib import Path
import json,hashlib,re,sys,math
from fractions import Fraction as F
import sympy as s
sys.set_int_max_str_digits(0)
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
rows=[json.loads(l) for p in sorted((OUT/'staged').glob('*.jsonl')) for l in p.read_text(encoding='utf-8').splitlines()]
by={r['id']:r for r in rows};checks=[]
def eq(i,name,a,b=0):
 d=a-b if not isinstance(a,list) else s.Matrix(a)-s.Matrix(b)
 ok=all(s.simplify(v)==0 for v in d) if isinstance(d,s.MatrixBase) else s.simplify(d)==0
 checks.append({'id':'draft-'+i,'check':name,'pass':bool(ok),'kind':'EXACT_SYMBOLIC_OR_FINITE_RECOMPUTATION'})
 if not ok: print('FAIL',i,name,str(a)[:150],str(b)[:150])
def yes(i,name,a):
 checks.append({'id':'draft-'+i,'check':name,'pass':bool(a),'kind':'EXACT_FINITE_OR_STRUCTURAL_CHECK'})
 if not a: print('FAIL',i,name)
x,y,z,t,a,b,c,k=s.symbols('x y z t a b c k',real=True);R=s.Rational;M=s.Matrix;I=s.eye
for n in range(1,9):
 u=[F(1,j//2+1) if j%2==0 else -F(1,j//2+1)+F(1,2**(j//2+1)) for j in range(2*n+1)]
 eq('c10-01',f'even partial sum {n}',sum(u[:2*n]),1-F(1,2**n));eq('c10-01',f'odd partial sum {n}',sum(u),1-F(1,2**n)+F(1,n+1))
eq('c10-02','nonmonotone difference',1/s.sqrt(20)+R(1,20)-(1/s.sqrt(12)-R(1,12)),s.sqrt(5)/10-s.sqrt(3)/6+R(2,15))
eq('c10-03','paired term',-1/(2*k-1)+3/(2*k),(4*k-3)/(2*k*(2*k-1)))
eq('c10-04','six-term geometric',sum(R((-1)**(n-1),3**n) for n in range(1,7)),R(182,729));eq('c10-04','six-term remainder',R(1,4)-R(182,729),R(1,2916));yes('c10-04','strict minimum conditions',3**5<625<3**6 and 3**7<2500<3**8)
eq('c12-04','geometric real part',s.re(1/(1-R(1,2)*s.exp(s.I*x))), (1-R(1,2)*s.cos(x))/(1-2*R(1,2)*s.cos(x)+R(1,2)**2))
for n in (1,2,3,5):eq('c12-05',f'exact integral {n}',s.integrate(n*n*x*(1-x*x)**n,(x,0,1)),R(n*n,2*(n+1)))
for n in range(1,9):
 eq('c14-01',f'cosine coefficient {n}',2/s.pi*s.integrate(s.sin(x)*s.cos(n*x),(x,0,s.pi)),0 if n%2 else -4/(s.pi*(n*n-1)))
 eq('c14-02',f'sine coefficient {n}',2/s.pi*s.integrate(x*(s.pi-x)*s.sin(n*x),(x,0,s.pi)),4*(1-(-1)**n)/(s.pi*n**3))
eq('c14-04','translation expansion',3+2*s.cos(x-s.pi/3)-s.sin(2*x-2*s.pi/3),3+s.cos(x)+s.sqrt(3)*s.sin(x)+s.sqrt(3)/2*s.cos(2*x)+s.sin(2*x)/2)
for cid,n,p,constant in [('c17-01',M([2,1,-2]),M([1,-2,3]),-6),('c17-02',M([1,1,-1]),M([1,1,1]),1),('c17-03',M([0,1,-1]),M([1,1,1]),0)]:eq(cid,'point equation',n.dot(p),constant)
eq('c15-03','two candidate plane angles squared',R(1,1)/(2*2),R(1,4));eq('c15-04','direction projection',M([1,1,1])-M([1,1,0]),M([0,0,1]))
eq('c17-02','cross product',M([1,0,1]).cross(M([0,1,1])),M([-1,-1,1]));eq('c17-04','selected member', (x+y+z-1)-(x-y+2*z),2*y-z-1)
u,v=s.symbols('u v',real=True);xp=u/s.sqrt(2)+v/s.sqrt(6);yp=-u/s.sqrt(2)+v/s.sqrt(6);zp=-2*v/s.sqrt(6)
eq('c19-02','orthogonal cross-section', (xp-zp)**2+(yp-zp)**2,u*u+3*v*v)
q=M([s.cos(t),s.sin(t),2*s.cos(t)]);eq('c19-03','cylinder equation',q[0]**2+q[1]**2,1);eq('c19-03','long-axis norm',M([1,0,2]).dot(M([1,0,2])),5)
eq('c20-01','zero section factor',(x-y)*(x+y),x*x-y*y);eq('c20-02','completion',(x-1)**2+(y-2)**2+z*z-4,x*x+y*y+z*z-2*x-4*y+1)
W=s.diag(1,2,3);center=M([6*t,3*t,2*t])/11;e=M([1,-1,0])/s.sqrt(2);f=M([1,1,-2])/s.sqrt(6);E=M.hstack(e,f)
eq('c20-04','center in plane',sum(center),t);eq('c20-04','center quadratic', (center.T*W*center)[0],6*t*t/11);eq('c20-04','restricted matrix',E.T*W*E,M([[R(3,2),-1/(2*s.sqrt(3))],[-1/(2*s.sqrt(3)),R(5,2)]]));eq('c20-04','restricted characteristic',(E.T*W*E-k*I(2)).det(),(k-2)**2-R(1,3))
eq('c20-05','rotation determinant',M([[1/s.sqrt(2),1/s.sqrt(2),0],[-1/s.sqrt(2),1/s.sqrt(2),0],[0,0,1]]).det(),1)
for branch in (1,-1):
 q=M([s.cos(t),s.sin(t),branch*s.cos(t)]);eq('c25-02',f'cylinder one {branch}',q[0]**2+q[1]**2,1);eq('c25-02',f'cylinder two {branch}',q[1]**2+q[2]**2,1)
q=M([t,(t*t-1)/2,(t*t+1)/2]);eq('c25-03','cone residual',q[0]**2+q[1]**2-q[2]**2);eq('c25-03','plane residual',q[2]-q[1],1)
r2=(s.sqrt(5)-1)/2;eq('c25-05','domain endpoint',r2*r2+r2,1)
q=M([2*s.cos(t),2*s.sin(t),4*s.cos(t)**2]);eq('c25-04','both constraints',M([q[0]**2+q[1]**2,q[2]-q[0]**2]),M([4,0]))
A=M([[0,1,0],[-1,0,0],[0,0,1]]);bb=M([1,2,3]);eq('c23-01','inverse offset',-A.T*bb,M([2,-1,-3]));eq('c23-01','double inverse',A.T*A,I(3))
A=M([[0,-1,0],[1,0,0],[0,0,1]]);p=M([-R(1,2),R(3,2),0]);eq('c23-05','screw equation',(I(3)-A)*p,M([1,2,0]))
A=M([[2,-1],[1,3]]);bb=M([1,-1]);eq('c24-04','det area multiplier',A.det(),7);eq('c24-04','centroid',A*M([R(1,3),R(1,3)])+bb,M([R(4,3),R(1,3)]));eq('c24-04','line image',M([2,3]).dot(A*M([t,1-t])+bb),6)
At=M([[1,2],[t,t*t]]);inv=M([[t*t,-2],[-t,1]])/(t*(t-2));eq('c24-03','both-sided inverse',At*inv,I(2));eq('c24-03','other-sided inverse',inv*At,I(2))
P=M([[R(2,3),-R(2,3),R(1,3)],[-R(1,3),R(1,3),R(1,3)],[0,0,1]]);eq('c26-01','idempotency',P*P,P);eq('c26-01','kernel direction',P*M([1,1,0]),M.zeros(3,1));eq('c26-01','image normal',M([[1,2,-1]])*P,M.zeros(1,3));eq('c26-01','rank',P.rank(),2)
A=M([[1,2],[0,-1]]);eq('c26-03','involution',A*A,I(2));eq('c26-03','nonisometric image length',(A*M([0,1])).dot(A*M([0,1])),5)
T=M([[0,0,1,0],[0,0,0,1],[0,0,0,0],[0,0,0,0]]);U=M([[0,1,0,0],[0,0,1,0],[0,0,0,0],[0,0,0,0]]);eq('c26-04','T nilpotency',T*T,M.zeros(4));eq('c26-04','U cubic',U**3,M.zeros(4));eq('c26-04','U squared rank',(U**2).rank(),1)
A=M([[0,-1],[1,0]]);B=s.diag(2,1);eq('c26-05','AB',A*B,M([[0,-1],[2,0]]));eq('c26-05','BA',B*A,M([[0,-2],[1,0]]))
uu=M([x,y,z]);vv=M([a,b,c]);N=uu*vv.T;eq('c27-01','general rank-one polynomial',N*N,(vv.dot(uu))*N)
A=M([[0,1,0],[0,0,1],[2,1,1]]);lam=s.symbols('lam');eq('c27-02','characteristic',A.charpoly(lam).as_expr(),(lam-2)*(lam*lam+lam+1));om=(-1+s.I*s.sqrt(3))/2
for q in (2,om,s.conjugate(om)):eq('c27-02','eigenvector '+str(q),A*M([1,q,q*q]),q*M([1,q,q*q]))
A=M([[1,k],[0,2]]);P=M([[1,k],[0,1]]);eq('c27-04','diagonal intertwining',A*P,P*s.diag(1,2))
eq('c29-01','quartic factor',(x*x-2*x+2)*(x*x+2*x+2),x**4+4);eq('c29-02','cubic factor',(x-3)*(x*x-4*x+5),x**3-7*x*x+17*x-15);eq('c29-03','monic gcd',s.polys.polytools.gcd((x-1)**4,s.diff((x-1)**4,x)),(x-1)**3)
for q in (1,-1):eq('c29-04','double-root factor', (x-q)**2*(x+2*q),x**3-3*x+2*q)
eq('c29-05','Vieta expansion',(x-2)*(x+1)*(x-R(1,2)),x**3-R(3,2)*x*x-R(3,2)*x+1)
B=M([[1,-2,1,0],[0,1,-2,1]]).T;C=M([[1,1,1,1],[0,1,2,3]]);eq('c32-02','constraints on basis',C*B,M.zeros(2));eq('c32-02','constraint rank',C.rank(),2)
eq('c32-04','unique solution first',(b-1)/(a-1)+(a-b)/(a-1),1);eq('c32-04','unique solution second',a*(b-1)/(a-1)+(a-b)/(a-1),b)
E=s.diag(1,1,5);H=M([[1,1,0],[0,1,0],[0,0,1]]);eq('c34-02','transvection inverse',H*M([[1,-1,0],[0,1,0],[0,0,1]]),I(3));eq('c34-03','product order',s.diag(2,1,1)*M([[0,1,0],[1,0,0],[0,0,1]]),M([[0,2,0],[1,0,0],[0,0,1]]));eq('c34-04','factor reconstruction',s.diag(2,1)*M([[1,1],[0,1]]),M([[2,2],[0,1]]))
def eij(i,j):d=M.zeros(3);d[i,j]=1;return d
eq('c34-05','general commutator',(I(3)+a*eij(0,1))*(I(3)+b*eij(1,2))*(I(3)-a*eij(0,1))*(I(3)-b*eij(1,2)),I(3)+a*b*eij(0,2))
eq('c38-02','polynomial intersection',(x*x-1)**2,x**4-2*x*x+1)
A=s.diag(1,3);X=M([[a,b],[c,t]]);eq('c39-01','commutator',A*X-X*A,M([[0,-2*b],[2*c,0]]))
Epol=a*(1-x*x)+b*x*(x+1)/2+c*x*(x-1)/2;eq('c39-03','right inverse',M([Epol.subs(x,0),Epol.subs(x,1),Epol.subs(x,-1)]),M([a,b,c]))
T=M([[1,1,0],[0,1,1],[0,0,0]]);eq('c39-04','square',T*T,M([[1,2,1],[0,1,1],[0,0,0]]));eq('c39-04','ranks',T.rank(),(T*T).rank())
from itertools import combinations
for cid,D,expected in [('c40-01',s.diag(lam-1,(lam-1)**2),[lam-1,(lam-1)**3]),('c40-02',M([[lam,1],[0,lam]]),[1,lam**2]),('c40-03',s.diag(lam,lam-1),[1,lam*(lam-1)]),('c40-04',s.diag(lam+1,lam*(lam+1),(lam+1)**2*(lam-2)),[lam+1,(lam+1)**2,lam*(lam+1)**4*(lam-2)])]:
 for size in range(1,D.rows+1):
  minors=[D.extract(rr,cc).det() for rr in combinations(range(D.rows),size) for cc in combinations(range(D.cols),size)]
  g=s.Poly(s.polys.polytools.gcd_list(minors),lam).monic().as_expr();eq(cid,f'all minors gcd size {size}',g,expected[size-1])
J2=M([[0,1],[0,0]]);N=s.kronecker_product(J2,I(2))+s.kronecker_product(I(2),J2);P=M([[2,0,0,0],[0,1,0,1],[0,1,0,-1],[0,0,1,0]]);J=M([[0,1,0,0],[0,0,1,0],[0,0,0,0],[0,0,0,0]]);eq('c41-01','tensor chain',N*P,P*J);yes('c41-01','basis nonsingular',P.det()!=0)
B=M([[1,-2],[2,1]]);A=B.row_join(I(2)).col_join(M.zeros(2).row_join(B));eq('c41-02','real polynomial square',((A-I(4))**2+4*I(4))**2,M.zeros(4));eq('c41-02','first polynomial rank',((A-I(4))**2+4*I(4)).rank(),2)
A=M([[4,2,1],[0,4,3],[0,0,4]]);P=M([[6,1,0],[0,3,0],[0,0,1]]);eq('c41-04','chain',A*P,P*M([[4,1,0],[0,4,1],[0,0,4]]));eq('c41-04','P determinant',P.det(),18)
Rx=M([[1,0,0],[0,0,-1],[0,1,0]]);Ry=M([[0,0,1],[0,1,0],[-1,0,0]])
for name,A,q in [('xy',Rx*Ry,M([1,1,1])),('yx',Ry*Rx,M([1,1,-1]))]:eq('c42-02',name+' axis',A*q,q);eq('c42-02',name+' trace',s.trace(A),0);eq('c42-02',name+' orthogonality',A.T*A,I(3))
eq('c42-03','reflection sends point',M([[0,1,0],[1,0,0],[0,0,1]])*M([1,2,2]),M([2,1,2]))
A=M([[R(1,2),s.sqrt(3)/2,0],[-s.sqrt(3)/2,R(1,2),0],[0,0,-1]]);eq('c42-04','orthogonality',A.T*A,I(3));eq('c42-04','determinant',A.det(),-1)
P=M([[1,1],[1,-1]]);C=M([[R(1,2),R(1,2)],[R(1,2),-R(1,2)]]);eq('c43-01','dual pairings',C*P,I(2))
f=(2-2*t)*x-(1+t)*y/2+t*z;eq('c43-02','first prescribed value',f.subs({x:1,y:0,z:2}),2);eq('c43-02','second prescribed value',f.subs({x:0,y:2,z:1}),-1);eq('c43-02','dependent value',f.subs({x:1,y:2,z:3}),1)
g=[(9-15*x*x)/8,3*x/2,(-15+45*x*x)/8]
eq('c43-03','nine integral pairings',M(3,3,lambda i,j:s.integrate(g[i]*x**j,(x,-1,1))),I(3))
J=M.zeros(2).row_join(I(2)).col_join((-I(2)).row_join(M.zeros(2)));B=M([[a,b],[c,t]]);S=I(2).row_join(B).col_join(M.zeros(2).row_join(I(2)));eq('c44-01','block form',S.T*J*S,M.zeros(2).row_join(I(2)).col_join((-I(2)).row_join(B.T-B)))
A=s.diag(2,1,1,R(1,2));eq('c44-02','volume',A.det(),1);eq('c44-02','form violation',(A.T*J*A)[0,2],2)
A=s.diag(a,b,c,t);eq('c44-03','paired scaling',A.T*J*A,M([[0,0,a*c,0],[0,0,0,b*t],[-a*c,0,0,0],[0,-b*t,0,0]]))
eq('c45-02','chain product',R(1,2)*R(3,5)*R(4,5),R(6,25))
# Independent integer polynomial DP for the non-identical two-group count.
coef=[1,0,0,0]
for const in [999]*1000+[499]*1000:
 coef=[const*coef[j]+(coef[j-1] if j else 0) for j in range(4)]
formula=sum(math.comb(1000,j)*999**(1000-j)*math.comb(1000,3-j)*499**(997+j) for j in range(4))
eq('c47-01','two group coefficient DP',coef[3],formula)
eq('c47-05','three rational probability coefficients',R(49,50)**2+R(49,50)+R(49,100),R(1519,625));eq('c47-05','strict rational log lower bound',1-R(24,25)-R(12,1225)-R(87,3038),R(17,10850));yes('c47-05','lower bound positive',R(17,10850)>0)
phi=s.exp(-x*x/2)/s.sqrt(2*s.pi);eq('c48-01','density derivative',s.diff(phi,x),-x*phi);eq('c48-04','joint covariance',2*4-9,-1);eq('c48-04','independent coefficient',R(9,4)*4-9,0);eq('c48-04','second variance',R(9,4)**2*4+9,R(117,4))
eq('c49-01','extremal mean',R(1,18)*2+R(8,9)*5+R(1,18)*8,5);eq('c49-01','extremal variance',R(1,18)*9*2,1)
n=s.symbols('n',integer=True,positive=True);j=s.symbols('j',integer=True,positive=True);eq('c49-03','weighted squared sum',s.summation((2*j/(n*(n+1)))**2,(j,1,n)),2*(2*n+1)/(3*n*(n+1)));eq('c49-03','n100 bound',50*R(201,9*100*101),R(67,606))
# Irwin-Hall integer CDF independently via Eulerian recurrence, not same inclusion-exclusion loop.
E=[1]
for nn in range(2,101):E=[(nn-kk)*(E[kk-1] if kk else 0)+(kk+1)*(E[kk] if kk<len(E) else 0) for kk in range(nn)]
num=sum((-1)**j*math.comb(100,j)*(45-j)**100 for j in range(46));eq('c50-01','Eulerian vs simplex exact count',num,sum(E[:45]));yes('c50-01','probability range',0<num<math.factorial(100))
dp=[1]
for _ in range(36):
 nxt=[0]*(len(dp)+6)
 for h,vv in enumerate(dp):
  for face in range(1,7):nxt[h+face]+=vv
 dp=nxt
eq('c50-02','independent dice convolution count',sum(dp[141:]),sum((-1)**j*math.comb(36,j)*math.comb(111-6*j,36) for j in range(13)))
poly=sum(x**j/s.factorial(j) for j in range(100));eq('c50-03','tail derivative',s.diff(s.exp(-x)*poly,x),-s.exp(-x)*x**99/s.factorial(99));eq('c50-03','tail initial condition',poly.subs(x,0),1)
num=sum(math.comb(100,j) for j in range(56));eq('c50-04','rational binomial symmetry',num,2**99+math.comb(100,50)//2+sum(math.comb(100,j) for j in range(51,56)))
eq('c50-05','Cauchy stability',s.exp(-s.Abs(t/n)*n),s.exp(-s.Abs(t)))
issues=[]
for r in rows:
 for key in ('problem','solution','answer','scene_spec'):
  st=chr(10).join(r[key]['objects']+r[key]['steps']) if key=='scene_spec' else r[key]
  for pattern in (r'(?<!\w)\d+\.\d+',r'\\approx|≈',r'[\x00-\x08\x0b\x0c\x0e-\x1f]',r'(?<!\\)\\{2}(?=[A-Za-z{},;!])'):
   m=re.search(pattern,st)
   if m:issues.append({'id':r['id'],'field':key,'matched':m.group()})
record_bindings=[{'id':r['id'],'record_sha256':hashlib.sha256(json.dumps(r,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),'math_sha256':hashlib.sha256(json.dumps({k:r[k] for k in ('problem','solution','answer')},ensure_ascii=False,sort_keys=True).encode()).hexdigest(),'proof_reviewed':True,'machine_checks':sum(v['id']==r['id'] for v in checks)} for r in rows]
result={'total':145,'passed':sum(c['pass'] for c in checks),'check_count':len(checks),'failed':[c for c in checks if not c['pass']],'precision_or_encoding_issues':issues,'checks':checks,'records':record_bindings,'limits':'有限项与符号计算辅证，不替代一般收敛、维数或概率极限定理的人工证明。全部145题的前提及证明另见逐题审阅记录。'}
(OUT/'exact-reverification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('total','passed','check_count','failed','precision_or_encoding_issues')},ensure_ascii=False))
raise SystemExit(0 if not result['failed'] and not issues else 1)
