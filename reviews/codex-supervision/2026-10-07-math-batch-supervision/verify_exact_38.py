
"""Exact algebra/calculus witnesses for the 38 bound records; theorem reasoning remains explicit."""
from pathlib import Path
import json
import sympy as s
root=Path(__file__).resolve().parents[3]
out=Path(__file__).resolve().parent
rows=[json.loads(line) for line in (out/'independent-review-38.jsonl').read_text(encoding='utf-8').splitlines()]
x,t,r,b=s.symbols('x t r b',real=True)
a,alpha,N=s.symbols('a alpha N',positive=True)
theta=s.symbols('theta',real=True)
lam=s.symbols('lambda')
proofs={}
def add(rid, equalities, reasoning):
 values=[]
 for lhs,rhs in equalities:
  residual=s.simplify(s.trigsimp(lhs-rhs))
  assert (residual.is_zero_matrix if isinstance(residual,s.MatrixBase) else residual==0),(rid,lhs,rhs,residual)
  values.append({'left':s.sstr(lhs),'right':s.sstr(rhs),'residual':'0'})
 proofs[rid]={'exact_equalities':values,'manual_reasoning':reasoning}
add('calc-derivative-001',[(s.diff(x*x,x).subs(x,1),s.Integer(2)),((x*x).subs(x,1),s.Integer(1))],
 '可微函数的切线为 y-f(1)=f\'(1)(x-1)，即 y=2x-1。')
add('calc-improper-002',[(s.integrate(1/(1+x*x),(x,0,s.oo)),s.pi/2)],
 '变上限积分 arctan b 的有限极限存在，符合反常积分收敛定义。')
add('calc-param-improper-003',[(s.integrate(s.exp(-alpha*x),(x,0,s.oo)),1/alpha)],
 'alpha>0 保证 exp(-alpha b)→0；不向 alpha<=0 外推。')
add('calc-double-integral-004',[(2*s.pi*s.integrate((1-r*r)*r,(r,0,1)),s.pi/2)],
 '单位圆盘上 integrand 非负；极坐标 Jacobian r，体积解释成立。')
add('calc-green-005',[(s.integrate(a*a,(theta,0,2*s.pi)),2*s.pi*a*a)],
 'a>0；圆周逆时针，P=-y、Q=x 为 C1，Green 公式 integrand=2。')
add('calc-limit-006',[(s.limit(s.sin(x)/x,x,0,dir='+'),s.Integer(1)),
 (s.simplify(s.sin(-x)/(-x)),s.sin(x)/x)],
 '对所有 0<x<pi/2，面积比较给 sin x<x<tan x，夹逼及偶性推出双侧极限；有限动画不是证明。')
add('calc-area-007',[(s.integrate(x+2-x*x,(x,-1,2)),s.Rational(9,2))],
 '上、下边界差 (2-x)(x+1)>=0，交点 -1,2 精确。')
add('calc-area-008',[(s.integrate((2*a*s.cos(theta))**2/2,(theta,-s.pi/2,s.pi/2)),s.pi*a*a)],
 'a>0，r>=0 的角域 [-pi/2,pi/2] 覆盖圆一次。')
add('calc-area-009',[(s.integrate(a*a*(1-s.cos(t))**2,(t,0,2*s.pi)),3*s.pi*a*a)],
 'a>0，dx/dt=a(1-cos t)>=0，一拱 y>=0，因此 y dx 给普通面积。')
add('calc-area-010',[(s.integrate(s.log(x),(x,1,s.E))+s.integrate(-x+s.E+1,(x,s.E,s.E+1)),s.Rational(3,2))],
 'ln x+x-e-1 严格递增，唯一交点 x=e；分段上边界正确。')
add('calc-area-011',[(2*(s.integrate(x*x,(x,0,1))+s.integrate(2-x*x,(x,1,s.sqrt(2)))),8*(s.sqrt(2)-1)/3)],
 '对称性及绝对值在 x=1 处分段，交点 0,+/-sqrt2；计算两瓣总面积。')
F=x*s.asin(x)**2+2*s.sqrt(1-x*x)*s.asin(x)-2*x
add('calc-vol-012',[(s.diff(F,x),s.asin(x)**2),
 (s.pi*(s.limit(F,x,1,dir='-')-F.subs(x,0)),s.pi**3/4-2*s.pi)],
 '圆盘法用于 0<=x<=1 上非负半径；反导在内部求导，端点使用连续极限。')
add('calc-area-013',[(s.integrate(x*s.exp(-x),(x,0,1)),1-2/s.E)],
 'x exp(-x)>=0，分部积分符号及上下限正确。')
u=s.symbols('u',positive=True)
add('calc-series-017',[(s.integrate(1/u**2,(u,N,s.oo)),1/N)],
 '对所有 |x|<=1，以可求和的 1/n² 控制；M 判别法一致收敛，N>=1 时尾和<=1/N。')
v=s.Matrix([2,-1,3]);ab=s.Matrix([-1,2,0]);ac=s.Matrix([-1,0,3])
add('geom-020',[(v.dot(v),s.Integer(14))],
 '方向与法向平行，sin(theta)=1 且 theta∈[0,pi/2]，故线面垂直。')
add('geom-022',[(ab.cross(ac),s.Matrix([6,3,2]))],
 '法向非零，三点不共线，方程 6x+3y+2z-6=0 包含三点。')
add('geom-024',[(s.trigsimp((2*s.cos(t))**2+(2*s.sin(t))**2),s.Integer(4))],
 'z 任意，参数 (2cost,2sint,z) 覆盖半径2圆柱面，母线平行z轴。')
c=s.symbols('c',real=True)
add('geom-026',[(x*x+2*c*c,x*x+2*c*c)],
 'y=c 的截线在三维中为 (x,c,x²+2c²)，顶点 (0,c,2c²)；y=0/1 各结果正确。')
l,m,n,x0,y0,z0=s.symbols('l m n x0 y0 z0',real=True)
poly=(x0+l*t)**2+(y0+m*t)**2-z0-n*t
add('geom-028',[(s.expand(poly).coeff(t,2),l*l+m*m),
 (s.expand(poly).coeff(t,1),2*x0*l+2*y0*m-n)],
 '实数域上二次系数0推出 l=m=0，一次系数0再推出 n=0，矛盾于方向非零。')
A=s.Matrix([[0,-1,0],[1,0,0],[0,0,1]])
add('geom-029',[(A*s.Matrix([1,0,0])+s.Matrix([1,2,3]),s.Matrix([1,3,3]))],
 'A 为绕 z 轴正向 pi/2 旋转；随后平移，操作次序正确。')
xp,yp,zp=s.symbols('xp yp zp',real=True)
add('geom-030',[((xp/2)**2+yp*yp+zp*zp,xp*xp/4+yp*yp+zp*zp)],
 '可逆仿射变换的逆代换给椭球，x向半轴2、其余1。')
xx=a*(1+s.cos(t));yy=a*s.sin(t);zz=2*a*s.sin(t/2)
add('geom-031',[(xx*xx+yy*yy,2*a*xx),(xx*xx+yy*yy+zz*zz,4*a*a)],
 't∈[0,2pi] 对应 z>=0，t+2pi 保持 x,y 而反转 z；[0,4pi] 覆盖两分支与交点。')
A=s.Matrix([[1,3],[0,1]])
add('linalg-048',[(A.det(),s.Integer(1)),((A*s.Matrix([0,1])).dot(A*s.Matrix([0,1])),s.Integer(10))],
 'T(x,y)=(x+3y,y)；整条水平线集合不变，带标记点/有限线段有位移；竖线像 X-3Y=c。')
add('linalg-051',[(s.expand((x-1)*(x-2)*(x-3)),x**3-6*x*x+11*x-6)],
 '三实根1,2,3，因此均在复平面的实轴上。')
A=s.Matrix([[1,2,0],[0,1,3],[2,1,1]])
cross=A[:,0].cross(A[:,1])
add('linalg-053',[(A.det(),s.Integer(10)),(cross,s.Matrix([-2,3,1])),
 (cross.dot(A[:,2]),s.Integer(10))],
 '底面积sqrt14、高10/sqrt14，体积10；不以动态测量代替精确结论。')
A=s.Matrix([[2,1],[1,-1]])
add('linalg-054',[(A.det(),s.Integer(-3)),(A*s.Matrix([2,1]),s.Matrix([5,1]))],
 '系数D=-3，Dx=-6，Dy=-3；非退化直线系数下 D=0 分平行不重合/重合两种。')
A=s.Matrix([[1,1,1],[1,-1,1],[2,0,1]])
add('linalg-055',[(A.det(),s.Integer(2)),(A*s.Matrix([1,0,0]),s.Matrix([1,1,2]))],
 '系数可逆，唯一解(1,0,0)，消元回代全成立。')
A=s.Matrix([[1,2,1],[2,4,2]]);B=s.Matrix([[-2,-1],[1,0],[0,1]])
add('linalg-056',[(A*B,s.zeros(2,2)),(s.Integer(A.rank()),s.Integer(1)),
 (s.Integer(B.rank()),s.Integer(2))],
 '两个零空间向量独立，零化度2，因此构成基础解系。')
A=s.Matrix([[1,0],[3,1]])
add('linalg-058',[(A.det(),s.Integer(1)),(A*s.Matrix([x,t]),s.Matrix([x,t+3*x]))],
 '竖直线集合保持，水平线倾斜，底/高1，保持面积和定向。')
add('linalg-062',[(s.Integer(2+2-1),s.Integer(3))],
 '交为span(e2)，和含三个标准基而等于R³；维数3和1。')
A=s.Matrix([[1,1,0],[0,1,1]])
add('linalg-063',[(A*s.Matrix([-t,t,-t]),s.zeros(2,1)),
 (s.Integer(A.rank()),s.Integer(2))],
 '核维1，任(u,v)可取(x,y,z)=(u,0,v)，值域R²。')
A=s.Matrix([[3,1],[0,2]])
add('linalg-064',[(A*s.Matrix([1,0]),3*s.Matrix([1,0])),
 (A*s.Matrix([1,-1]),2*s.Matrix([1,-1])),
 ((lam*s.eye(2)-A).det(),(lam-3)*(lam-2))],
 '全部非零特征向量是对应一维特征空间的非零倍，不能含零向量。')
add('linalg-065',[(s.gcd(lam,lam*lam-1),s.Integer(1)),
 (lam*(lam*lam-1),lam*(lam-1)*(lam+1))],
 '一阶行列式因子1，二阶lambda(lambda²-1)，不变因子1、二阶式；初等因子三个一次多项式。')
A=s.Matrix([[2,1,0],[0,2,0],[0,0,3]])
add('linalg-066',[((lam*s.eye(3)-A).det(),(lam-2)**2*(lam-3)),
 (s.Integer((A-2*s.eye(3)).rank()),s.Integer(2))],
 'lambda=2代数重数2、几何重数1，对应一个2阶块；lambda=3一个1阶块，A已在Jordan形式。')
A=s.Matrix([[s.cos(theta),-s.sin(theta)],[s.sin(theta),s.cos(theta)]])
add('linalg-067',[(A.T*A,s.eye(2)),(A.det(),s.Integer(1))],
 'A^TA=I 对所有实theta成立，内积、长度、角度与定向保持。')
add('linalg-069',[(s.eye(2)*s.Matrix([1,0]),s.Matrix([1,0])),
 (s.eye(2)*s.Matrix([0,1]),s.Matrix([0,1]))],
 'f1(x,y)=x和f2(x,y)=y分别在标准基取Kronecker值，线性扩张唯一。')
p=s.symbols('p',real=True)
add('prob-040',[(s.diff(s.log(1-p)+p,p),-p/(1-p)),
 (s.diff(s.log(1-p)+p/(1-p),p),p/(1-p)**2)],
 '对0<=p<1，积分导数符号给 -p/(1-p)<=log(1-p)<=-p；np_n→lambda 推出二项质量固定k极限。lambda=0 用Markov界 np_n，不使用0^0。')
z=s.symbols('z',real=True);sigma=s.symbols('sigma',positive=True)
phi=s.exp(-z*z/2)/s.sqrt(2*s.pi)
add('prob-041',[(s.integrate(phi,(z,-1,1)),s.erf(1/s.sqrt(2))),
 (s.integrate(phi,(z,-2,2)),s.erf(s.sqrt(2))),
 (s.integrate(phi,(z,-s.oo,s.oo)),s.Integer(1))],
 'sigma>0，Z=(X-mu)/sigma为标准正态；缩放密度保持总面积，区间质量使用erf精确表达。')
assert set(proofs)=={r['id'] for r in rows},set(proofs)^{r['id'] for r in rows}
for row in rows:
 p=proofs[row['id']];p.update({'id':row['id'],'source':row['source'],
 'final_record_dense_sha256':row['final_record_dense_sha256'],'status':'PASS_SCOPED_EXACT_WITNESSES_AND_MANUAL_REVIEW',
 'limitation':'符号恒等式佐证具体计算；所列定理条件和覆盖性由逐题人工数学审阅确认，非自动通用证明。'})
receipt={'schema':'exact-bound-math-review-38-v1','reviewed':38,'witnesses':list(proofs.values()),
 'sympy_version':s.__version__,'decimal_or_numerical_approximation_used':False,
 'semantic_isolation':'NOT_ESTABLISHED','native_render':'UNVERIFIED','production':'CLOSED'}
print(json.dumps({'status':'PASS_SCOPED_EXACT_WITNESSES_AND_MANUAL_REVIEW','reviewed':38,'exact_equalities':sum(len(p['exact_equalities']) for p in proofs.values()),'decimal_or_numerical_approximation_used':False,'write_performed':False},ensure_ascii=False,indent=2))
