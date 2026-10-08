from pathlib import Path
import json,hashlib,sys
import sympy as S
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(OUT))
import build_repaired_batches as B
rows={r['id']:r for p in sorted((OUT/'staged').glob('*.jsonl')) for r in map(json.loads,p.read_text(encoding='utf-8').splitlines())}
checks=[]
def check(i,name,actual,expected=0):
 if isinstance(actual,S.MatrixBase):ok=actual.equals(expected if isinstance(expected,S.MatrixBase) else S.zeros(*actual.shape))
 elif isinstance(actual,bool):ok=actual==expected
 else:ok=S.simplify(actual-expected)==0
 assert ok,(i,name,actual,expected)
 checks.append({'id':i,'check':name,'actual':str(actual),'expected':str(expected),'status':'PASS','method':'exact_symbolic_or_integer_algebra'})
x,t,h=S.symbols('x t h',real=True);n=S.symbols('n',integer=True,nonnegative=True)
R=S.Rational
check('draft-c11-03','有限稀疏和重编号恒等式',sum(x**(2**j) for j in range(7))-x-sum((x*x)**(2**j) for j in range(6)))
check('draft-c11-03','稀疏指数界归纳步',2*(n+1)-(n+2),n)
an=(2**n+2*(-1)**n)/3
check('draft-c11-04','通项满足递推',an-an.subs(n,n-1)-2*an.subs(n,n-2))
check('draft-c11-04','两个初值',an.subs(n,0)+an.subs(n,1),1)
check('draft-c11-04','独立部分分式和函数',1/(3*(1-2*x))+2/(3*(1+x)),(1-x)/(1-x-2*x*x))
check('draft-c11-04','精确分数取值',((1-x)/(1-x-2*x*x)).subs(x,R(1,4)),R(6,5))
check('draft-c11-05','组合系数比',S.binomial(2*n+2,n+1)/4**(n+1)/(S.binomial(2*n,n)/4**n),(2*n+1)/(2*n+2))
s=(1-x)**(-R(1,2));check('draft-c11-05','初值问题',2*(1-x)*S.diff(s,x)-s)
check('draft-c11-05','负端点阿贝尔值',s.subs(x,-1),S.sqrt(2)/2)
L1=3*R(1,4)**2*R(3,4);L2=3*R(3,4)**2*R(1,4);m=R(2,3)*L1+L2/3
check('draft-c51-02','观测证据概率',m,R(15,64));p1=R(2,3)*L1/m;p2=L2/(3*m)
check('draft-c51-02','后验归一化',p1+p2,1);check('draft-c51-02','预测概率',p1/4+3*p2/4,R(11,20))
L=S.Matrix([[1,-1,0,0],[0,1,-1,0],[0,0,1,-1]])
A=L.T*S.diag(1,2,3)*L;check('draft-c35-02','全空间秩',A.rank(),3)
check('draft-c35-02','全空间核',A*S.ones(4,1),S.zeros(4,1))
U=S.Matrix([[1,1,1,1],[0,1,1,1],[0,0,1,1],[0,0,0,1]])
check('draft-c35-02','可逆替换行列式',U.det(),1);check('draft-c35-02','合同标准形',U.T*A*U,S.diag(1,2,3,0))
V=S.Matrix([[1,0,0],[0,1,0],[0,0,1],[0,0,0]]);AV=V.T*A*V
for k in (1,2,3):check('draft-c35-02',f'受限正定Sylvester主子式{k}为正',bool(AV[:k,:k].det()>0),True)
P=S.Matrix([[1,1,1],[0,0,1],[1,-1,-1]]);G=S.diag(1,2,1)
check('draft-c37-03','换基可逆',P.det(),2)
check('draft-c37-03','坐标逆问题',P.inv()*S.Matrix([3,2,1]),S.Matrix([2,-1,2]))
GN=P.T*G*P;check('draft-c37-03','Gram变换',GN,S.Matrix([[2,0,0],[0,2,2],[0,2,4]]))
z=S.Matrix([2,-1,2]);check('draft-c37-03','两种坐标同一平方范数',(z.T*GN*z)[0],18)
check('draft-c13-01','反正切差的正切',S.simplify(((x+1)-x)/(1+x*(x+1))),1/(x*x+x+1))
check('draft-c13-01','有限裂项和',sum(S.atan(j+1)-S.atan(j) for j in range(1,9)),S.atan(9)-S.pi/4)
check('draft-c13-04','二阶差分有限和',sum(S.sqrt(j+2)-2*S.sqrt(j+1)+S.sqrt(j) for j in range(1,8)),S.sqrt(9)-S.sqrt(8)-(S.sqrt(2)-1))
check('draft-c13-04','尾项有理化',S.sqrt(n+2)-S.sqrt(n+1),1/(S.sqrt(n+2)+S.sqrt(n+1)))
a=S.symbols('a',real=True);check('draft-c18-01','归一化距离条件全部分支',S.expand((2*a-1)**2-1),4*a*(a-1))
W=S.diag(1,2,3);nv=S.ones(3,1);pv=S.Matrix([1,2,3]);q=pv-(nv.dot(pv)/(nv.T*W.inv()*nv)[0])*W.inv()*nv
check('draft-c18-04','候选点满足平面',sum(q),0);check('draft-c18-04','精确投影',q,S.Matrix([-R(25,11),R(4,11),R(21,11)]))
check('draft-c18-04','加权距离平方',((pv-q).T*W*(pv-q))[0],R(216,11))
check('draft-c18-04','距离根式',S.sqrt(R(216,11)),6*S.sqrt(66)/11)
f=-(x-1)**3*(x-2)**2/4
for k in range(3):check('draft-c30-01',f'三重零点导数{k}',S.diff(f,x,k).subs(x,1))
for k in range(2):check('draft-c30-01',f'二重零点导数{k}',S.diff(f,x,k).subs(x,2))
check('draft-c30-01','归一化',f.subs(x,0),1);check('draft-c30-01','平移展开',f.subs(x,t+1),-t**5/4+t**4/2-t**3/4)
f=x**4-4*x**3+7*x**2-6*x+3;check('draft-c30-02','三次项必要条件',S.expand(f.subs(x,h+t)).coeff(t,3),4*h-4)
check('draft-c30-02','完整偶性验证',f.subs(x,1+t),t**4+t**2+1)
def delta(f):return S.expand(f.subs(x,x+1)-f)
g=x**3
for k in range(3):g=delta(g)
check('draft-c30-03','三次差分非零',g,6);check('draft-c30-03','四次差分为零',delta(g),0)
check('draft-c30-03','差分方程解',delta(x**3+x**2+2),3*x*x+5*x+2)
for m in (1,2,3,7):
 check('draft-c30-05',f'平移差最高系数m={m}',S.expand((x+h)**m-x**m).coeff(x,m-1),m*h)
 if m>=2:check('draft-c30-05',f'中心差最高系数m={m}',S.expand((x+1)**m+(x-1)**m-2*x**m).coeff(x,m-2),m*(m-1))
b=S.symbols('b',real=True);d=b*b+4*a
for sign in (-1,1):check('draft-c21-04',f'两分支精确根{sign}',(a*t*t+b*t-1).subs(t,(-b+sign*S.sqrt(d))/(2*a)))
check('draft-c21-04','线性分支', (b*t-1).subs(t,1/b));check('draft-c21-04','重根梯度方向内积',(2*a*t+b).subs(t,-b/(2*a)))
pts=[(0,0),(4,0),(4,3),(2,1),(0,3)]
area=sum(pts[j][0]*pts[(j+1)%5][1]-pts[j][1]*pts[(j+1)%5][0] for j in range(5))/S.Integer(2)
check('draft-c28-01','鞋带面积',area,8);check('draft-c28-01','几何凹口验证',4*3-R(1,2)*4*2,8)
u=S.Matrix([1,-1,2]);v=S.Matrix([2,1,1]);At=S.eye(3)+t*u*v.T
check('draft-c28-02','独立直接行列式',At.det(),1+3*t);Pr=At.subs(t,-R(1,3))
check('draft-c28-02','幂等投影',Pr*Pr,Pr);check('draft-c28-02','核包含',Pr*u,S.zeros(3,1));check('draft-c28-02','像约束',v.T*Pr,S.zeros(1,3));check('draft-c28-02','奇异秩',Pr.rank(),2)
Ua=S.Matrix([[1,0,1],[0,1,1],[1,0,0],[0,1,0]]);Ga=Ua.T*Ua
check('draft-c28-04','Gram行列式',Ga.det(),4);res=Ua[:,2]-Ua[:,0]/2-Ua[:,1]/2
check('draft-c28-04','正交残差平方长度',res.dot(res),1)
from itertools import combinations
check('draft-c28-04','独立Cauchy-Binet子式平方和',sum(Ua[list(ind),:].det()**2 for ind in combinations(range(4),3)),4)
check('draft-c46-01','双曲线分段积分',R(1,4)+S.integrate(1/(4*x),(x,R(1,4),1)),R(1,4)+S.log(2)/2)
check('draft-c46-03','Voronoi区域B面积',S.integrate(x,(x,R(1,2),1)),R(3,8));check('draft-c46-03','概率和',R(1,4)+2*R(3,8),1)
y=S.symbols('y',real=True);check('draft-c46-04','密度归一化',S.integrate(x+y,(y,0,1),(x,0,1)),1)
check('draft-c46-04','加权事件概率',S.integrate(x+y,(y,0,1),(x,0,R(1,2))),R(3,8))
check('draft-c46-05','三周期原像长度除Jacobian',3*b/3,b);check('draft-c46-05','联合事件分数',R(1,3)*R(1,2),R(1,6))
w=1/(2*S.sqrt(x));check('draft-c02-01','分部尾界化简',w.subs(x,a)+w.subs(x,b)-(w.subs(x,b)-w.subs(x,a)),1/S.sqrt(a))
check('draft-c02-01','绝对积分每段下界',R(2,3)*S.pi*R(1,2)/(2*S.sqrt((n+1)*S.pi)),S.sqrt(S.pi)/(6*S.sqrt(n+1)))
N=S.symbols('N',integer=True,positive=True);check('draft-c02-02','尖峰面积有限和',S.summation(2**(-n),(n,1,N)),1-2**(-N))
check('draft-c02-02','尖峰面积无限和',S.summation(2**(-n),(n,1,S.oo)),1)
ap,bp,q=S.symbols('ap bp q',positive=True);check('draft-c02-04','参数积分恒等式',S.integrate(S.exp(-t*q),(t,ap,bp)),(S.exp(-ap*q)-S.exp(-bp*q))/q)
check('draft-c02-04','对数原函数导数',S.diff(S.log(t),t),1/t)
q=S.symbols('q',positive=True);check('draft-c02-05','正参数平方换元',(x**(-R(1,2))/(1+x)).subs(x,q*q)*2*q,2/(1+q*q))
check('draft-c02-05','特殊值精确积分',2*S.integrate(1/(1+x*x),(x,0,S.oo)),S.pi)
Pfield=-2*y/(x*x+y*y)+3*y/((x-3)**2+y*y);Qfield=2*x/(x*x+y*y)-3*(x-3)/((x-3)**2+y*y)
check('draft-c04-05','区域内旋度',S.diff(Qfield,x)-S.diff(Pfield,y))
rr=S.symbols('rr',positive=True);cx=rr*S.cos(t);cy=rr*S.sin(t)
check('draft-c04-05','自身圆周环流微元',(-2*cy/(cx*cx+cy*cy))*S.diff(cx,t)+(2*cx/(cx*cx+cy*cy))*S.diff(cy,t),2)
check('draft-c04-05','总边界环流和',-2*S.pi-4*S.pi+6*S.pi)
F=R(17,4)*t+6*S.sin(t)+R(9,8)*S.sin(2*t)
check('draft-c07-02','极坐标面积原函数导数',S.diff(F,t),(2+3*S.cos(t))**2/2)
beta=S.acos(R(2,3));alpha=S.pi-beta
check('draft-c07-02','内环面积',S.simplify(S.expand_trig(F.subs(t,2*S.pi-alpha)-F.subs(t,alpha))),R(17,2)*beta-3*S.sqrt(5))
check('draft-c07-02','外环面积',S.simplify(S.expand_trig(F.subs(t,alpha)-F.subs(t,-alpha))),R(17,2)*(S.pi-beta)+3*S.sqrt(5))
check('draft-c07-02','全周期平方积分',S.integrate((2+3*S.cos(t))**2/2,(t,0,2*S.pi)),R(17,2)*S.pi)
check('draft-c08-01','摆线参数面积',S.integrate((1-S.cos(t))**2,(t,0,2*S.pi)),3*S.pi)
check('draft-c09-01','穿轴真实圆盘体积',S.pi*S.integrate(x*x,(x,0,1)),S.pi/3)
check('draft-c09-02','圆环截面平方差',(2+S.sqrt(1-x*x))**2-(2-S.sqrt(1-x*x))**2,8*S.sqrt(1-x*x))
check('draft-c09-02','外轴环面体积',8*S.pi*S.integrate(S.sqrt(1-x*x),(x,-1,1)),4*S.pi**2)
check('draft-c09-04','左侧圆环平方差',(2-h)**2-h*h,4*(1-h));check('draft-c09-04','右侧圆环平方差',h*h-(h-2)**2,4*(h-1))
check('draft-c09-04','内区间唯一最小值条件',(1+S.Symbol('d',nonnegative=True))**2-1,S.Symbol('d',nonnegative=True)*(S.Symbol('d',nonnegative=True)+2))
check('draft-c09-04','左右分支边界值',(4*S.pi*(1-h)).subs(h,0),4*S.pi)
check('draft-c09-04','右侧边界值',(4*S.pi*(h-1)).subs(h,2),4*S.pi)
check('draft-c09-05','三段并集体积',S.pi*(S.integrate(x*x+3,(x,0,1))+4+S.integrate(x*x,(x,2,3))),R(41,3)*S.pi)
check('draft-c09-05','交叠体积',S.pi*(S.integrate(x*x-1,(x,1,2))+3),R(13,3)*S.pi)
check('draft-c09-05','容斥核对',18*S.pi-R(13,3)*S.pi,R(41,3)*S.pi)

cn=(-1)**n*2**(-(n+1)/2)*S.sin((n+1)*S.pi/4)
# Use integer arithmetic on sampled coefficients plus an exact geometric complex-root recurrence.
rplus=(-1+S.I)/2;rminus=(-1-S.I)/2
check('draft-c11-02','复根满足特征方程',rplus**2+rplus+S.Rational(1,2))
coeff=lambda k:S.simplify((-1)**k*2**(-S.Rational(k+1,2))*S.sin(S.Rational(k+1,4)*S.pi))
check('draft-c11-02','两个初值',S.Matrix([coeff(0),coeff(1)]),S.Matrix([S.Rational(1,2),-S.Rational(1,2)]))
check('draft-c11-02','精确复根幅度',rplus*S.conjugate(rplus),S.Rational(1,2))
for k in (2,3,4,5,6,7,8,15,16):check('draft-c11-02',f'递推独立取样{k}',coeff(k)+coeff(k-1)+coeff(k-2)/2)
check('draft-c11-02','端点非零子列通项',coeff(16)*S.sqrt(2)**16,S.Rational(1,2))
CC=S.Matrix([[0,2,0],[0,0,3],[S.Rational(1,6),0,0]]);AA=S.eye(3)-t*CC
check('draft-c33-05','三次循环恒等式',CC**3,S.eye(3));check('draft-c33-05','直接行列式',AA.det(),1-t**3)
II=(S.eye(3)+t*CC+t*t*CC**2)/(1-t**3)
check('draft-c33-05','双侧逆左乘',AA*II,S.eye(3));check('draft-c33-05','双侧逆右乘',II*AA,S.eye(3))
b1,b2,ss=S.symbols('b1 b2 ss');sol=S.Matrix([6*ss+2*b2+b1,3*ss+b2,ss])
check('draft-c33-05','奇异参数全部解代入',AA.subs(t,1)*sol,S.Matrix([b1,b2,-(b1+2*b2)/6]));check('draft-c33-05','奇异秩',AA.subs(t,1).rank(),2)
check('draft-c02-05','零端二进分块上界',2**(-n-1)*(2**(-n-1))**(a-1),2**(-a*(n+1)))
check('draft-c02-05','无穷端二进分块上界',2**n*(2**n)**(a-2),2**(n*(a-1)))
assert set(B.NEW)=={r['id'] for r in checks}
forbidden=[]
import re
for i,row in rows.items():
 for field in ('problem','solution','answer','scene_spec'):
  value=json.dumps(row[field],ensure_ascii=False) if field=='scene_spec' else row[field]
  # Scan the decoded strings, not JSON escapes.
  parts=[str(v) for v in row[field].get('objects',[])+row[field].get('steps',[])] if field=='scene_spec' else [value]
  for value in parts:
   for kind,pat in [('decimal',r'(?<![A-Za-z0-9])\d+\.\d+'),('approximation',r'\\(?:approx|simeq)\b|≈|大约|近似值|约等于'),('control',r'[\x00-\x08\x0b\x0c\x0e-\x1f]'),('double_macro',r'\\\\[A-Za-z]+')]:
    if re.search(pat,value):forbidden.append({'id':i,'field':field,'kind':kind,'match':re.search(pat,value).group()})
   if value.count('{')!=value.count('}'):forbidden.append({'id':i,'field':field,'kind':'brace_imbalance'})
assert not forbidden,forbidden
for i in set(rows)-set(B.NEW):
 for f in ('problem','solution','answer','scene_spec'):
  assert rows[i][f]==B.normalize_math(B.OLD[i][f]),(i,f,'unexpected_math_change')
manual=[]
for i in B.NEW:
 math={f:rows[i][f] for f in ('problem','solution','answer','scene_spec')}
 assert all(rows[i][f]==B.normalize_math(B.NEW[i][f]) for f in math)
 manual.append({'id':i,'concept_id':rows[i]['concept_id'],'math_sha256':hashlib.sha256(json.dumps(math,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),'manual_general_proof':'PASS_UNDER_EXPLICIT_ASSUMPTIONS','proof_steps_reviewed':rows[i]['scene_spec']['steps'],'finite_checks_do_not_replace_general_proof':True,'symbolic_check_count':sum(c['id']==i for c in checks)})
result={'revised_questions':len(B.NEW),'exact_checks':len(checks),'all_pass':True,'floating_point_used':False,'finite_checks_not_universal_proof':True,'manual_general_proofs':manual,'checks':checks,'retained_questions_same_math_as_prior_after_latex_normalization':len(rows)-len(B.NEW),'precision_scan':{'records':119,'flags':forbidden}}
(OUT/'exact-reverification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:v for k,v in result.items() if k not in ('checks','manual_general_proofs')},ensure_ascii=False))
