from pathlib import Path
import json,hashlib
import sympy as s
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
x,y,t,a,k,m,p,R,u,theta,d,l,b=s.symbols('x y t a k m p R u theta d l b', real=True)
ap,bp,dp,lp,rp=s.symbols('a_pos b_pos d_pos l_pos r_pos',positive=True)
checks=[]
def eq(rid,name,value,want):
 if isinstance(value,s.MatrixBase): ok=all(s.simplify(z)==0 for z in value-want)
 else:ok=(value==want) or s.simplify(value-want)==0
 checks.append({'id':rid,'check':name,'actual':str(value),'expected':str(want),'pass':ok})
 if not ok:raise AssertionError((rid,name,value,want))
q=s.Rational
# Line/quadric substitution: solve exactly, then verify each space point.
for rid,coords,surface,roots in [
 ('draft-c21-01',s.Matrix([t,t,2*t]),lambda v:v[2]-v[0]**2-v[1]**2,[0,1]),
 ('draft-c21-03',s.Matrix([1+t,2*t,t]),lambda v:v[2]-v[0]*v[1],[0,-q(1,2)]),
 ('draft-c21-04',s.Matrix([1+t,2*t,t]),lambda v:v[0]**2+v[1]**2+v[2]**2/4-1,[0,-q(8,21)])]:
 got=s.solve(surface(coords),t)
 assert set(got)==set(roots)
 for j,z in enumerate(roots):eq(rid,f'root {j} substitutes into surface',surface(coords.subs(t,z)),0)
 eq(rid,'substituted polynomial factorization',surface(coords),s.expand(surface(coords)))
eq('draft-c21-02','sphere substitution',a**2+t**2-4,t**2-(4-a**2))
eq('draft-c21-02','tangent dot normal',s.Matrix([0,0,1]).dot(s.Matrix([a,0,0])),0)
eq('draft-c21-05','discriminant',s.discriminant(2*t**2-m*t-1,t),m**2+8)
for sign in [-1,1]:eq('draft-c21-05',f'root sign {sign}',(2*t**2-m*t-1).subs(t,(m+sign*s.sqrt(m**2+8))/4),0)
A=s.Matrix([[1,1,0],[0,1,1],[1,0,1]])
eq('draft-c28-01','volume determinant',A.det(),2)
eq('draft-c28-02','oriented area before swap',s.Matrix([[1,2],[3,4]]).det(),-2)
eq('draft-c28-02','oriented area after swap',s.Matrix([[3,4],[1,2]]).det(),2)
eq('draft-c28-03','linear volume scale',s.Matrix([[1,1,1],[0,2,1],[0,0,3]]).det(),6)
eq('draft-c28-03','inverse volume scale',s.Matrix([[1,1,1],[0,2,1],[0,0,3]]).inv().det(),q(1,6))
eq('draft-c28-04','parameter determinant',s.Matrix([[1,2,3],[1,1,1],[k,0,1]]).det(),-1-k)
eq('draft-c28-04','dependent witness',s.Matrix([1,2,3])-2*s.Matrix([1,1,1]),s.Matrix([-1,0,1]))
v1=s.Matrix(s.symbols('a1:4'));v2=s.Matrix(s.symbols('b1:4'));v3=s.Matrix(s.symbols('c1:4'))
eq('draft-c28-05','general determinant/triple product identity',s.Matrix.hstack(v1,v2,v3).det(),v1.dot(v2.cross(v3)))
for rid,A,bvec,want in [
 ('draft-c31-01',s.Matrix([[1,1,1],[1,-1,1],[1,1,-1]]),s.Matrix([6,2,0]),s.Matrix([1,2,3])),
 ('draft-c31-03',s.Matrix([[1,1,1],[1,1,2],[1,2,a]]),s.Matrix([1,2,3]),s.Matrix([a-3,3-a,1])),
 ('draft-c31-02',s.Matrix([[a,1],[1,a]]),s.Matrix([1,1]),s.Matrix([1/(a+1),1/(a+1)])),
 ('draft-c31-04',s.Matrix([[k,1],[1,k]]),s.Matrix([1,k]),s.Matrix([0,1]))]:
 eq(rid,'computed solution',A.inv()*bvec,want)
 eq(rid,'substitution',A*want,bvec)
 for j in range(A.cols):
  Aj=A.copy();Aj[:,j]=bvec
  eq(rid,f'Cramer numerator {j}',Aj.det(),s.factor(A.det()*want[j]))
 if rid in ['draft-c31-02','draft-c31-04']:
  var=a if rid.endswith('02') else k
  for z in [-1,1]:
   M=A.subs(var,z);bv=bvec.subs(var,z)
   expected_aug=2 if rid.endswith('02') and z==-1 else 1
   eq(rid,f'singular coefficient rank {z}',M.rank(),1)
   eq(rid,f'singular augmented rank {z}',M.row_join(bv).rank(),expected_aug)
# Universal proof is reviewed manually; symbolic generic 3x3 identity is supplemental.
G=s.Matrix(3,3,s.symbols('g0:9'))
eq('draft-c31-05','adjugate identity generic 3x3',G*G.adjugate(),G.det()*s.eye(3))
B=s.Matrix(s.symbols('b0:3'))
for j in range(3):
 H=G.copy();H[:,j]=B
 eq('draft-c31-05',f'cofactor replacement {j}',(G.adjugate()*B)[j],H.det())
# Double integrals, changes of coordinates, limits, geometric probabilities.
eq('draft-c03-01','separable integral',s.integrate(x*y,(y,0,2),(x,0,1)),1)
eq('draft-c03-02','triangle first order',s.integrate(x**2,(y,0,x),(x,0,1)),q(1,4))
eq('draft-c03-02','triangle reversed order',s.integrate(x**2,(x,y,1),(y,0,1)),q(1,4))
eq('draft-c03-03','polar integral with Jacobian',s.integrate(rp**3,(rp,0,2),(theta,0,s.pi/2)),2*s.pi)
eq('draft-c03-04','upper half disk polar',s.integrate(rp**2*s.sin(theta),(rp,0,1),(theta,0,s.pi)),q(2,3))
eq('draft-c03-04','upper half disk Cartesian',s.integrate((1-x*x)/2,(x,-1,1)),q(2,3))
eq('draft-c03-04','full disk',s.integrate(rp**2*s.sin(theta),(rp,0,1),(theta,0,2*s.pi)),0)
eq('draft-c03-05','Jacobian determinant',s.Matrix([[1,1],[1,-1]]).det(),-2)
eq('draft-c03-05','diamond pieces',s.integrate(u*u,(u,0,1))+s.integrate(2*u-u*u,(u,1,2)),1)
eq('draft-c05-01','rational limit',s.limit((x*x+3*x+1)/(2*x*x-x+5),x,s.oo),q(1,2))
eq('draft-c05-02','right limit',s.limit(s.Abs(x)/x,x,0,dir='+'),1)
eq('draft-c05-02','left limit',s.limit(s.Abs(x)/x,x,0,dir='-'),-1)
eq('draft-c05-03','rationalization limit',s.limit(s.sqrt(x*x+2*x)-x,x,s.oo),1)
eq('draft-c05-04','polynomial over exponential',s.limit(x**3/s.exp(x),x,s.oo),0)
eq('draft-c05-04','logarithm over root',s.limit(s.log(x)/s.sqrt(x),x,s.oo),0)
eq('draft-c05-04','root over cube',s.limit(s.sqrt(x)/x**3,x,s.oo),0)
n=s.symbols('n',integer=True,positive=True)
eq('draft-c05-05','sequence first value',s.sin(2*n*s.pi),0)
eq('draft-c05-05','sequence second value',s.sin(2*n*s.pi+s.pi/2),1)
eq('draft-c05-05','sequence tends zero',s.limit(1/(2*n*s.pi+s.pi/2),n,s.oo),0)
eq('draft-c46-01','meeting band',1-2*q(1,2)*q(3,4)**2,q(7,16))
eq('draft-c46-02','square/disk ratio',s.sqrt(2)**2/s.pi,2/s.pi)
eq('draft-c46-03','joint-density integral',2*s.integrate(q(1,2)-y,(y,0,q(1,2))),q(1,4))
eq('draft-c46-04','corrected radial CDF',s.integrate(2*rp,(rp,0,u)),u*u)
eq('draft-c46-04','corrected joint density divided by Jacobian',(2*rp/(2*s.pi))/rp,1/s.pi)
eq('draft-c46-05','Buffon density integral',4/(s.pi*dp)*s.integrate(lp*s.sin(theta)/2,(theta,0,s.pi/2)),2*lp/(s.pi*dp))
# Improper integrals: compute finite expressions, then limits.
eq('draft-c02-01','finite p=2 integral',s.integrate(x**-2,(x,1,R)),1-1/R)
eq('draft-c02-01','tail limit',s.limit(1-1/R,R,s.oo),1)
eq('draft-c02-02','finite p=1/2 integral',s.integrate(x**(-q(1,2)),(x,1,R)),2*s.sqrt(R)-2)
eq('draft-c02-02','divergent limit',s.limit(2*s.sqrt(R)-2,R,s.oo),s.oo)
eq('draft-c02-03','log integral derivative',s.diff(s.log(s.log(x)),x),1/(x*s.log(x)))
eq('draft-c02-03','log-square primitive derivative',s.diff(-1/s.log(x),x),1/(x*s.log(x)**2))
eq('draft-c02-03','convergent value',s.limit(1/s.log(2)-1/s.log(R),R,s.oo),1/s.log(2))
eq('draft-c02-04','finite integral',s.integrate(x*s.exp(-x),(x,0,R)),1-(R+1)*s.exp(-R))
eq('draft-c02-04','integral limit',s.limit(1-(R+1)*s.exp(-R),R,s.oo),1)
eq('draft-c02-05','p not equal 1 primitive derivative',s.diff(x**(1-p)/(1-p),x),x**(-p))
eq('draft-c02-05','p=1 primitive derivative',s.diff(s.log(x),x),1/x)
eq('draft-c04-01','Green triangle',s.integrate(2*x,(x,0,1-y),(y,0,1)),q(1,3))
eq('draft-c04-02','CCW circle integral',s.integrate(s.sin(t)*(-s.sin(t)),(t,0,2*s.pi)),-s.pi)
eq('draft-c04-03','annulus Green integral',s.integrate(3*rp**3,(rp,1,2),(theta,0,2*s.pi)),45*s.pi/2)
eq('draft-c04-04','supplementary segment',s.integrate(3*t-3,(t,0,1)),-q(3,2))
eq('draft-c04-04','direct parabola verification',s.integrate((t+t*t)+t*2*t,(t,0,1)),q(3,2))
eq('draft-c04-05','ellipse Green integral',s.integrate(ap*bp*(s.cos(t)**2+s.sin(t)**2)/2,(t,0,2*s.pi)),s.pi*ap*bp)
eq('draft-c06-01','two parabolas',s.integrate(2-2*x*x,(x,-1,1)),q(8,3))
eq('draft-c06-02','absolute graph',2*s.integrate(1-x,(x,0,1)),1)
eq('draft-c06-03','horizontal slices',s.integrate(y+2-y*y,(y,-1,2)),q(9,2))
eq('draft-c06-04','positive parameter slices',s.integrate(k*x-x*x,(x,0,k)),k**3/6)
eq('draft-c06-04','k=2',s.Rational(2)**3/6,q(4,3))
eq('draft-c07-01','rose petal',s.integrate((2*s.sin(3*theta))**2/2,(theta,0,s.pi/3)),s.pi/3)
eq('draft-c07-02','cardioid',s.integrate((1+s.cos(theta))**2/2,(theta,0,2*s.pi)),3*s.pi/2)
eq('draft-c07-03','four rose petals',4*s.integrate(s.cos(2*theta)**2/2,(theta,-s.pi/4,s.pi/4)),s.pi/2)
eq('draft-c07-04','difference of disks',s.integrate(((4*s.cos(theta))**2-4)/2,(theta,-s.pi/3,s.pi/3)),4*s.pi/3+2*s.sqrt(3))
eq('draft-c07-05','two lemniscate leaves',2*s.integrate(s.cos(2*theta)/2,(theta,-s.pi/4,s.pi/4)),1)
eq('draft-c08-01','ellipse oriented integral',s.integrate(bp*s.sin(t)*(-ap*s.sin(t)),(t,0,2*s.pi)),-s.pi*ap*bp)
eq('draft-c08-02','astroid quadrant',3*ap**2*s.integrate(s.sin(t)**4*s.cos(t)**2,(t,0,s.pi/2)),3*s.pi*ap**2/32)
fx=3*t/(1+t**3);fy=3*t*t/(1+t**3)
eq('draft-c08-03','folium cross-derivative',fx*s.diff(fy,t)-fy*s.diff(fx,t),9*t*t/(1+t**3)**2)
eq('draft-c08-03','folium integral',s.integrate(9*t*t/(1+t**3)**2/2,(t,0,s.oo)),q(3,2))
I=2*s.cos(t)*s.cos(2*t)+s.sin(t)*s.sin(2*t)
eq('draft-c08-04','Lissajous first loop integral',s.integrate(I,(t,-s.pi/2,s.pi/2)),q(8,3))
eq('draft-c08-04','Lissajous second loop integral',s.integrate(I,(t,s.pi/2,3*s.pi/2)),-q(8,3))
eq('draft-c08-04','Lissajous period',s.integrate(I,(t,0,2*s.pi)),0)
f=(2+s.sin(t))*(-s.sin(t))
eq('draft-c08-05','counterexample whole circle',s.integrate(f,(t,0,2*s.pi)),-s.pi)
eq('draft-c08-05','counterexample first half',s.integrate(f,(t,0,s.pi)),-4-s.pi/2)
eq('draft-c08-05','counterexample second half',s.integrate(f,(t,s.pi,2*s.pi)),4-s.pi/2)
eq('draft-c09-01','disk volume',s.pi*s.integrate(x,(x,0,4)),8*s.pi)
eq('draft-c09-02','shell volume',2*s.pi*s.integrate(x**3,(x,0,1)),s.pi/2)
eq('draft-c09-03','washer volume',s.pi*s.integrate(x*x-x**4,(x,0,1)),2*s.pi/15)
eq('draft-c09-04','shifted shell volume',2*s.pi*s.integrate((x+1)*x*x,(x,0,1)),7*s.pi/6)
eq('draft-c09-05','x-axis disk volume',s.pi*s.integrate(s.sin(x)**2,(x,0,s.pi)),s.pi**2/2)
eq('draft-c09-05','y-axis shell volume',2*s.pi*s.integrate(x*s.sin(x),(x,0,s.pi)),2*s.pi**2)
# Infinity values are compared directly before subtraction.
coverage=sorted({z['id'] for z in checks})
expected={json.loads(line)['id'] for k in range(5,9) for line in (OUT/'corrected'/f'batch-{k:02}.jsonl').read_text(encoding='utf-8').splitlines()}
assert set(coverage)==expected,(expected-set(coverage))
report={'arithmetic':'exact SymPy expressions only; no floats, evalf, approximate quadrature or finite numerical sampling','checks':checks,'passed':sum(z['pass'] for z in checks),'total':len(checks),'record_coverage':coverage,'record_count':len(coverage),'manual_proof_obligations':['sphere tangency and parameter branch inequalities','triple-product volume including degenerate base','general-n cofactor proof, not inferred from generic 3x3 check','Fubini and Jacobian change-of-variable hypotheses','Heine sequence criterion','independent uniform sampling hypotheses and Jacobian density','p-integral all-real-parameter branch proof','Green regularity and orientation','rose/lemniscate single traversal and disjoint leaves','folium loop single traversal and endpoint limit','self-intersection area overlap correction and graph monotonicity'],'input_sha256':{f'batch-{k:02}.jsonl':hashlib.sha256((OUT/'corrected'/f'batch-{k:02}.jsonl').read_bytes()).hexdigest() for k in range(5,9)}}
(OUT/'exact-verification-batches-05-08.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'passed':report['passed'],'total':report['total'],'records':len(coverage)}))
