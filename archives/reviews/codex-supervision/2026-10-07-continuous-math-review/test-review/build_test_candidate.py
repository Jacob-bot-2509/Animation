"""Versioned test corrections, preserve submitted and previous twelve revisions."""
from pathlib import Path
import json,hashlib,copy,re,sys
ROOT=Path(__file__).resolve().parents[4];OUT=Path(__file__).resolve().parent;QUEUE=OUT.parent
PARENT=ROOT/'reviews/codex-supervision/2026-10-07-math-batch-supervision'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists() and p.read_bytes()!=b:
  if '--replace-unfrozen' not in sys.argv or (OUT/'test-delivery-manifest.json').exists() or str(p.relative_to(OUT)).startswith(('original-submission','parent-candidate')):raise ValueError('frozen artifact: '+str(p))
 p.write_bytes(b)
def emit(p,x):write(p,(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def rows(p):return [json.loads(s) for s in p.read_text(encoding='utf-8-sig').splitlines() if s.strip()]
bound={}
for n in (20,21,22):
 for q in rows(next((QUEUE/'bound-records').glob('batch'+str(n)+'-*'))/'records.jsonl'):bound[q['record']['id']]=q
assert len(bound)==138
specs={}
def patch(rid,reason,solution=None,append=None,problem=None,answer=None,objects=None,replacements=None):
 old=bound[rid]['record'];r=copy.deepcopy(old)
 if rid in specs:r.update(copy.deepcopy(specs[rid]['fields']))
 if solution is not None:r['solution']=solution
 if append is not None:r['solution']+=append
 if problem is not None:r['problem']=problem
 if answer is not None:r['answer']=answer
 scene=copy.deepcopy(r['scene_spec'])
 if objects is not None:scene['objects']=objects
 if replacements:scene['objects']=[x.replace(a,b) for x in scene['objects'] for a,b in []] if False else scene['objects']
 if replacements:
  for a,b in replacements:scene['objects']=[x.replace(a,b) for x in scene['objects']]
 scene['steps']=['呈现题干及条件：'+r['problem']]+['依次呈现：'+x for x in scene['objects']]+['核对完整证明：'+r['solution'],'高亮答案：'+r['answer']]
 r['scene_spec']=scene;r['efficiency_tags']=copy.deepcopy(scene['objects'])
 specs[rid]={'reason':(specs[rid]['reason']+'；' if rid in specs else '')+reason,'fields':{k:r[k] for k in ('problem','solution','answer','scene_spec','efficiency_tags') if r[k]!=old[k]}}
patch('test-calc-006','答案补n与展开适用域，并证明展开与端点',append=r'展开的依据：在$|x|<1$内，几何级数$1/(1+t)=\sum_{k=0}^{\infty}(-t)^k$在从$0$到$x$的紧区间上一致收敛，逐项积分即得上述展开。$x=1$时有限几何式积分的余项绝对值不超过$1/(N+1)$，故也收敛到$\ln2$；$x=-1$时为负调和级数，发散，且原对数不定义；$|x|>1$时级数通项不趋于0。因此实展开的完整区间为$(-1,1]$。',answer=r'$\ln(1+x)=\sum_{n=1}^{\infty}(-1)^{n-1}x^n/n$（$-1<x\le1$）；$f^{(n)}(0)=(-1)^{n-1}(n-1)!$（整数$n\ge1$）。')
patch('test-calc-007','场景两次洛必达与正文一次洛必达加导数定义不一致',replacements=[('洛必达两步的分子分母比值','一次洛必达，再由二阶导数定义取极限')])
patch('test-calc-015','不以积分数值观察作为精确答案的依据',replacements=[('与积分数值对照','与幂级数积分恒等式对照')])
patch('test-calc-017','补唯一全局最小和无最大值的完整结论',append=r'更直接令$u=x+1,\ v=y+1$，则$f=-1+u^2+v^2-uv=-1+\frac12[(u-v)^2+u^2+v^2]$。故$f\ge-1$，等号仅在$u=v=0$，是唯一全局最小；因只有一个驻点且该点为严格最小，不存在局部极大，且沿$y=-1,x\to\infty$无上界。',answer=r'唯一极小点$(-1,-1)$，极小值也是全局最小值$-1$；无极大值。')
patch('test-calc-023','傅里叶级数在周期端点收敛到0，不等于端点给定的±π',problem=r'设$f(x)=x$（$-\pi<x<\pi$）并作$2\pi$周期延拓，其傅里叶正弦系数为$b_n=2(-1)^{n+1}/n$；在开区间内级数收敛到$x$，在周期接缝$x=\pm\pi$收敛到左右极限平均值$0$。利用$L^2$意义下的Parseval等式求$\sum_{n=1}^{\infty}1/n^2$。',append=r'端点取值不影响$L^2$积分与傅里叶系数；上述Parseval论证不需要级数在接缝处等于$\pm\pi$。')
patch('test-calc-031','落地速度与速率分开表述',answer=r'$v(t)=-10t$米/秒，$a(t)=-10$米/秒$^2$；$t=2$秒落地，落地速度$-20$米/秒（向下），速率$20$米/秒。')
patch('test-calc-035','不能将1/0写成普通除法，直接给比值判别论证',solution=r'对$\sum_{n=0}^{\infty}x^n/n!$，当$x\ne0$时相邻项绝对值比为$|x|/(n+1)\to0$，故每个实数或复数$x$都绝对收敛，收敛半径$+\infty$。对$\sum_{n=0}^{\infty}n!x^n$，任意$x\ne0$时相邻项绝对值比为$(n+1)|x|\to\infty$，通项绝对值最终至少以公比2增长，不趋于0，故发散；$x=0$时只有常数项1，收敛，收敛半径0。')
patch('test-calc-042','第二证法的积分极限补明确余项上界',append=r'第二证法的极限由精确界保证：$\left|\int_0^1\frac{(-x)^N}{1+x}dx\right|\le\int_0^1x^Ndx=1/(N+1)\to0$。')
patch('test-calc-043','将有限区域夹逼写全，避免未证可积时的形式平方',solution=r'令$I_R=\int_0^R e^{-x^2}dx$。有限矩形上的Fubini定理给$I_R^2=\iint_{[0,R]^2}e^{-(x^2+y^2)}dxdy$。第一象限半径$R$的四分之一圆包含于此正方形，而正方形包含于半径$\sqrt2R$的四分之一圆。正被积函数积分保持包含序。极坐标计算半径$r$的四分之一圆积分为$J_r=\int_0^{\pi/2}\int_0^r e^{-u^2}u\,du\,d\theta=\frac{\pi}{4}(1-e^{-r^2})$。因此$\frac{\pi}{4}(1-e^{-R^2})\le I_R^2\le\frac{\pi}{4}(1-e^{-2R^2})$。$I_R>0$单调有上界，且两端趋于$\pi/4$，故$\int_0^\infty e^{-x^2}dx=\sqrt\pi/2$。')
patch('test-geom-016','场景TeX的det命令多了一个反斜杠',replacements=[(r'\\det',r'\det')])
patch('test-geom-017','曲率不是对全部实x单调，改为关于绝对值的单调性',replacements=[('曲率随 $x$ 减小','曲率随$|x|$增大严格减小，顶点$x=0$最大')])
patch('test-geom-022','明确空间旋转矩阵采用右手正角约定',problem=bound['test-geom-022']['record']['problem']+r'取右手直角坐标系，正角遵循绕正$y$轴的右手定则。')
patch('test-prob-014','期望递推先证明有限性并说明独立重复',problem=r'独立重复掷一枚均匀骰子，直到首次出现6为止。求所需投掷次数的期望。',append=r'有限性也可直接由尾和给出：$P(T>k)=(5/6)^k$，因此$E[T]=\sum_{k=0}^\infty P(T>k)=\sum_{k=0}^\infty(5/6)^k=6<\infty$，所以递推式移项合法。')
patch('test-prob-015','同一时刻及硬币公平性需明确概率模型',problem=r'甲乙每个回合同步各抛一枚公平硬币；所有抛掷相互独立，两人各自遇到首次正面即停止。求他们在同一个回合停止的概率。')
patch('test-prob-018','答案补参数范围和发散分支',problem=bound['test-prob-018']['record']['problem']+r'其中$\lambda>0,\ t\in\mathbb R$。',answer=r'$E[e^{tX}]=\lambda/(\lambda-t)$（$t<\lambda$）；$t\ge\lambda$时为$+\infty$。')
patch('test-prob-022','均匀边缘分布不能代替两骰独立条件',problem=r'独立掷两枚均匀骰子，设$X$为两数之和。求$\operatorname{Var}(X)$。')
patch('test-prob-023','投针分布及正长度假设应在题干明确，而非推导中默加',problem=r'布丰投针：平行线间距$d>0$，针长$0<l\le d$。针中点到最近平行线的距离$X$在$[0,d/2]$均匀，针与平行线的无向锐夹角$\Theta$在$[0,\pi/2]$均匀，且两者独立。求针与任一直线相交的概率。')
patch('test-prob-025','最多两次和第二次不追加机会需明确，以匹配49/12',problem=r'掷一枚均匀骰子得$X$分；若第一次得6分，则再独立掷一次并累加点数，第二次无论得几分都停止；否则第一次后停止。最多掷两次。求总得分期望。')
patch('test-linalg-009','明确所求是到指定直线的正交投影',problem=r'求$\mathbb R^2$中到$\operatorname{span}\{(1,1)^T\}$的正交投影矩阵，并求$(3,1)^T$的正交投影。')
patch('test-linalg-011','补法方程解是唯一全局最小的验证',append=r'设求得系数向量$c_*=(5/2,-2/3)^T$，残差$r=b-Ac_*=(1/6,-1/3,1/6)^T$，满足$A^Tr=0$。任意$c=c_*+\delta$有$\|b-Ac\|^2=\|r\|^2+\|A\delta\|^2\ge1/6$。$A$列满秩（$\det(A^TA)=6>0$），故等号仅当$\delta=0$，证明拟合唯一最优。')
patch('test-linalg-013','周期不能仅从六项观察，写出严格递推恒等式',append=r'严格周期证明：由$D_{n+2}=D_{n+1}-D_n$，得到$D_{n+3}=D_{n+2}-D_{n+1}=-D_n$，再得$D_{n+6}=-D_{n+3}=D_n$。前六个相邻有序对$(1,0),(0,-1),(-1,-1),(-1,0),(0,1),(1,1)$互不相同，所以最小正周期确为6。')
patch('test-linalg-021','反射轴覆盖全部过原点方向，不只斜轴',replacements=[('关于斜直线的反射','关于任意过原点直线的反射（含水平轴、竖直轴）')])
patch('test-linalg-026','配方法的合同替换是斜坐标，不等于正交主轴旋转',replacements=[('椭圆主轴与坐标变换','可逆斜坐标合同替换；此替换不是正交主轴旋转')])
patch('test-linalg-036','倍乘操作只有一行，不能说三类均涉及两不同行',problem=r'求三类初等矩阵的行列式：交换两不同行；将单行乘以$k$（$k\ne0$）；将一行加到另一不同行。')
patch('test-x-003','矩阵级数逐项求导补紧区间一致收敛的依据',append=r'严格依据：任取$R>0$和次乘性矩阵范数，在$|t|\le R$上，原项范数不超过$R^k\|A\|^k/k!$，导数项范数不超过$R^{k-1}\|A\|^k/(k-1)!$（$k\ge1$）。两个数值级数分别求和为$e^{R\|A\|}$和$\|A\|e^{R\|A\|}$，均有限。由Weierstrass判别法及逐项求导定理，运算在任意紧区间有效，故对所有实$t$成立。')
patch('test-x-009','阶乘矩的n明确为非负整数',problem=bound['test-x-009']['record']['problem']+r'其中$n\in\mathbb Z_{\ge0}$。')
patch('test-x-010','相关系数绝对值1对应中心化线性相关，原变量为仿射关系',solution=bound['test-x-010']['record']['solution'].replace('"两个随机变量不几乎必然线性相关"','中心化变量$X-E[X]$与$Y-E[Y]$不几乎必然线性相关（即不存在非平凡常数$a,b$使$aX+bY$几乎必然为常数）'))
patch('test-x-013','删除所有约数估算，写出取整容斥及误差界',solution=r'在$\{1,\ldots,N\}$均匀选取整数。能被2、3、6整除的个数分别恰为$\lfloor N/2\rfloor,\lfloor N/3\rfloor,\lfloor N/6\rfloor$，故所求概率$p_N=[\lfloor N/2\rfloor+\lfloor N/3\rfloor-\lfloor N/6\rfloor]/N$。因$|\lfloor u\rfloor-u|<1$，有$|p_N-(1/2+1/3-1/6)|<3/N\to0$。所以极限自然密度为$2/3$；这不是在所有正整数上定义等概率分布。',objects=[r'精确计数$\lfloor N/2\rfloor+\lfloor N/3\rfloor-\lfloor N/6\rfloor$',r'容斥与严格误差$|p_N-2/3|<3/N$'])

def note_table(text):
 return {int(line.split(' ',1)[0]):line.split(' ',1)[1] for line in text.strip().splitlines()}
tables={
'calc':note_table(r"""
1 连续sin(πx)右端点Riemann和，积分2/π。
2 二阶Peano展开n²(1-cos(1/n))→1/2。
3 FTC加换元，F=(ln x)²/2，导数lnx/x，二阶(1-lnx)/x²，x>0。
4 integrating factor exp2x，通解e^-x+Ce^-2x，回代成立。
5 x≥2连续正递减1/(xlnx)，积分loglog发散。
6 高阶导(-1)^(n-1)(n-1)!，修订几何积分证明，闭端点x1及全区间(-1,1]。
7 无需f″连续，一次LHopital后用f′导数定义，极限f″(0)/2，修订场景。
8 f=x³/3-x²/2，stationary0,1，二阶符号localmax0/min-1/6。
9 t∈[0,1]speed=t√(4+9t²)，弧长(13√13-8)/27。
10 cardioid polararea half∫(1+cosθ)²=3π/2。
11 y-axis旋转左右不重复，右半shell integral8π。
12 partialfractions finite primitive，b/(1+b)→1，值ln2。
13 finite telescopinghalf[1+1/2-1/(N+1)-1/(N+2)]，和3/4。
14 power radius∞，逐项导数indexshift及initial1，ODEuniqueness给expx。
15 alternating remainderuniform≤1/(N+1)，逐项积分eta2=halfzeta2=π²/12。
16 F_y(1,1)=3，IFTvalid，implicit y′=-1,y″=-2/3。
17 唯一驻点(-1,-1)，Hpositive；修订精确中心平方式globalmin-1，无max。
18 x+y4，Lagrangepoint(2,2)，配方4-(x-2)²证明全局max4。
19 triangle换序得到∫0¹x²/(1+x²)=1-π/4。
20 a,bpositiveGreen正向椭圆参数∫half(xdy-ydx)=πab。
21 globalpotential x²y，任意曲线路径无关，值1；simplyconnected条件原文已区分。
22 div(x,y,z)=3，unitballvol4π/3，outwardflux4π。
23 Parseval L²，2π²/3=4Σ1/n²，修端点点值问题不影响积分。
24 logmonotonesum有限不等式-1≤Sn≤-1+(lnn+1)/n，极限exp-1。
25 递推1+a/(1+a)在[1,φ)保持，上界φ、差(1+a-a²)/(1+a)>0，极限φ。
26 FTC后LHopital sin(x²)/(3x²)→1/3。
28 奇函数连续对称区间积分0。
29 分部积分finite1-(lnb+1)/b→1，收敛。
30 exact0≤integral≤1/(n+1)，极限0。
31 h20-5t²,v-10t,a-10，t2,落地signedv-20，修答案速率区分。
32 graphcurvatureformula，parabola原点2,lnx点1值1/(2√2)。
33 差函数monotone及positiveLagrangecubicremainder，x≥0不等式成立。
34 ratio(n/(n+1))^n→1/e<1，正项级数收敛。
35 修订实际项比证明两个幂级数半径∞和0，避免1/0记号。
36 r>0chain Laplacian f″+f′/r，lnr给0，仅去原点。
37 foliumpoint3/2,3/2满足方程，Fy≠0，implicit slope-1。
38 integralJensen unitinterval expconvex，∫x²1/3，lowerexp1/3。
39 separableNewtoncool T20+80e^-kt，e^-5k1/2，T10=40。
40 fourthPeano cos limit-1/24。
41 doubleangle积分均π/2，sin²periodπ平移解释。
42 Abel+Leibniz或finitegeom积分，修订余项≤1/(N+1)，和ln2。
43 修订finite squaresandwich byquarterdiskR与√2R，boundπ/4(1-exp(-R²))与π/4(1-exp(-2R²))，sqrtπ/2。
44 orientedlineintegralabs givesellipseπab，a,bpositive。
45 exponentialMVT ξbetween1/(x+1)和1/x→0，x²difference→ln2。
"""),
'geom':note_table(r"""
1 参数联立s0t1，交点2,1,1，cross(-3,0,3)，plane x-z1。
2 pointlineprojectiont4/7，foot11/7,15/7,19/7，distance²3/7。
3 skewdirectionscross5,0,-5，delta-1,1,-3projectiondistance√2，nonzero混合积证异面。
4 unit球与normal1,2,2常数3平面distance1相切，Q1/3,2/3,2/3。
5 paraboloid点2,1,2，partials1,2，tangent z=x+2y-2。
6 r=(t,t²,t³) t1切向1,2,3，normalplane x+2y+3z6。
7 tetra determinant-9绝对/6，volume3/2。
8 AB(-1,1),AC(1,3)，det-4/2，area2。
9 90degCCW(2,1)→(-1,2)，投影(3,4)onto1,1=(7/2,7/2)。
10 ellipse axes3,4 area12π，affinescale或trigexactintegral。
11 lineplane z0t3→5,5,0;x0t-2→0,-5,5;y0t1/2→5/2,0,5/2。
12 cyclictriplevalue-2，两种cross和det一致。
13 sphereR2cutz√2圆x²+y²2，fullcircleparamt0..2π。
14 z=(x+y)(x-y)，固定一因子两族直线，每点两族完整覆盖。
15 xyz1positive，AMGMdistance²≥3等号1,1,1，globalmin√3。
16 shear Aunitcircleinverse=>x′²-2x′y′+2y′²1，SPDminor1,1，areaπ；sceneTeXfix。
17 κ2/(1+4x²)^(3/2)，maxat0,R1/2；scene对|x|的monotonicityfix。
18 pencilλ-1/2→plane x+2y-z0，missingpencilplane x+z2不throughorigin。
19 ucos t[-1,1] g3u²-4u2，minu2/3g2/3，maxu-1g9，distance√2/3,3。
20 n1,1,1，foot(-1,0,1)，mirror(-3,-2,-1)。
21 vectorssum0 lengths3,4,5，dot0θπ/2。
22 right-handedyrotationcolumnsorthonormalanddet1，修正角度约定。
23 radialnormal sphereR2 point1,1,√2，outwardunit(1/2,1/2,√2/2)。
24 parallelplanesconstantdifference6/norm3=>2。
25 twofocidistancesum4等价x²/4+(y²+z²)/3=1，|x|≤2正根回代无赘解，旋转椭球。
"""),
'prob':note_table(r"""
3 iidBernoulliindicator EXnp,varnp(1-p)，非独立variance不能直接加，原文已明确。
4 density3x²(0,1)，CDFx³，tailat1/2=7/8，mean3/4。
6 Poisson4 P2=8exp-4，P≥1=1-exp-4。
9 N(mean2,var3) affine2X-1→N(3,12)，tailaboveownmean1/2。
10 uniformmomentk=1/(k+1)，cov1/12,vars1/12,4/45，rho√15/4。
11 triangleleg2 area2，conditionaluniform0..2-x,mean(2-x)/2，marginal(2-x)/2，EY2/3。
12 hypergeom3red2white draw2，6/10=3/5。
13 PoissonMGFexpλ(expt-1)，derivativesmeanλ,rawsecondλ²λ。
14 independentfairdie until6，tail(5/6)^k exactsum6先证finite，递推成立。
15 修订independentfaircoin同步rounds，sameGeometricstop概率Σ4^-k=1/3。
17 iiduniformmaxCDFt²[0,1]density2t，mean2/3。
18 λ>0real t，exp integralconvergesiff t<λ valueλ/(λ-t)，diverges∞ otherwise。
19 5uniform min/max density5(1-t)^4和5t4，expect1/6,5/6。
22 两fairdice修订independence，var35/6；rawsecond329/6,moment校核正确。
23 修订Buffonmodel independentuniformdistanceandangle0<l≤d，区域概率2l/(πd)。
24 Poissonnormalization expseries1，factorialmomentλ²,varλ。
25 修订最多两次always追加oneiff初次6，无递归机会，EX7/2+EZ7/12=49/12。
"""),
'linalg':note_table(r"""
1 Cramer D-9,Dx-9,Dy-6,Dz-15，solution1,2/3,5/3回代全部成立。
2 Ainverse third[[2,-1],[-1,2]]乘B3,3得X1,1。
3 B²=A⇒BAAB，centralizeraI+bN，a²1,ab1⇒B±(I+N)，完备。
4 3×4matrixrow3=row1+row2，rank2，nullity2，twoexplicitkernelbasis。
5 eigen1,2,3⇒tr6,det6,trA²14,inverses1,1/2,1/3。
6 similardiagonalpower exp10,2^10=1024,3^10=59049。
7 Rayleigh/unitcircle f4-3x²，min1 at±1,0 max4at0,±1。
8 CHλ²-2λ-3，A(A-2I)=3I，inverse1/3[[-1,2],[2,-1]]。
9 修订正交projection P=halfones2，P²P，(3,1)→2,2，residual1,-1orthogonal。
10 GScolumnsa1(1,1),a2(1,0)，Q[[1,1],[1,-1]]/√2,R[[√2,1/√2],[0,1/√2]]。
11 leastsquaresA^TAmat14,6;6,3det6，coef5/2,-2/3，SSE1/6，修订globalminimumorthresidual。
13 tri diag/off1 recDn=Dn-1-Dn-2，first1,0,-1,-1,0,1；修Dn+3=-Dn所以leastperiod6。
14 matrix[[1,0,1],[0,2,0],[1,0,2]]det2 inverse[[2,0,-1],[0,1/2,0],[-1,0,1]]，ninecofactors正确。
15 (1-λ)I+λJ det(1+2λ)(1-λ)²，dependentiff1or-1/2。
16 planeW1sum0dim2,lineW2equalcoordsdim1，intersection0，directsumR³。
17 FrobeniusinnertraceATB=sumij aijbij满足axioms，normA√30。
18 idempotentdiag1,0，eigen1,0，generalminimaldividesλ(λ-1)⇒diagonalizable，ranktrace。
19 centralizerJordanones X[[a,b],[0,a]]，N=A-I，确为A多项式。
20 polynomial x4-4x²3 modx²-2x余3，exactquotientx²2x。
21 orthogonalreflection θhalfangledirection eigen±1，verticalaxes亦covered；scenefix。
22 Choleskypositive lowerdiag2,√2，L[[2,0],[1,√2]],LLTgiven。
23 A[[3,1],[1,3]] eigen4,2，generalx c1e4t+c2e2t,yc1e4t-c2e2t，independentbasis完整。
24 3pointcollineardet6-2t，t3。
25 spectrum3,-1unitvectors(1,±1)/√2，sum3project1-project2givenA。
26 congruence C[[1,-2/3],[0,1]] givesdiag3,14/3，替换可逆但非orth主轴rotation，scenefix。
27 Jordan2(2) ODEy c2e2t,x e2t(c1+c2t)，triangularintegration完整。
28 90degrotationcharλ²1，eigen±i，无非零realeigenvector。
29 A-Irank1nonzeroN²0，minimal(λ-1)²，JordanJ2(1)⊕1。
30 linearfunctional coeff1,1,1 determinedbasisconditions，f=x+y+z。
31 determinant3-7λ，dependentiffλ3/7。
32 col(A+B)subsetcolA+colB dimensionalinequality，orthdiagrank1examplesgiveequality2。
33 idempotenteigenλ²=λfromnonnullv⇒0or1，未误断言两值一定都出现。
34 SPDblockeigen4,2,1，ellipsoidaxes1/2,1/√2,1。
35 Vandermonde(x,2,3)det(2-x)(3-x)=(x-2)(x-3)。
36 swapdet-1,scale k,adddet1，修premise只有swap和add涉及两行。
37 derivativebasis1,x,x²列0,e1,2e2，matrix[[0,1,0],[0,0,2],[0,0,0]]。
38 invertibleAsquarefullrank；counterexamplenilpotent2rankdrops1to0。
39 quadraticblocktrace1,det-10,eigen(1±√41)/2及-1，inertia1,2，f1two-sheet。
40 cycleC4 adjacency specified，fourindependentmodes2,-2,0,0。
"""),
'x':note_table(r"""
1 geometricp1/2 supportpositive，evenΣ4^-k=1/3。
2 Y√Xtransformdensity2yfor0<y<1zeroelse，mean2/3。
3 matrixexpentire seriesderivative，修normcompact Mtest为逐项求导依据，initialI。
5 positivefencel，rectdomain0<x<l/2 quadraticlx-2x²maxl²/8。
6 Bertrandthreefullyspecifiedmodels enduniform1/3,radiusdistanceuniform1/2,midpointareauniform1/4。
7 symmetricmatrix[[1,2],[2,1]] inertia1,1，hyperbola3u²-v²1，realaxis y=x。
8 x≥0intersections0,1，sqrtx≥x²，area1/3。
9 Exp1 nnonnegativeinteger，I0=1,finitepartsrecnIprev andzeroendboundary，momentn!。
10 covariancevarspositive principalminors iff|rho|<1，修解释centeredlinearrelation或原变量affine而非raw线性。
11 twooriginlinearreflections determinant+1⇒rotation，exampleR2R1CCWπ/2，orderexplicit。
12 AπJ,J²-I，evenoddabsoluteconvergentexpseriescosπI+sinπJ=-I。
13 修精确floor容斥与error<3/N，naturaldensity2/3，非正整数全集uniformlaw。
14 a,bpositivecatenaryspeedcosh(x/a)>0，integral a sinh(b/a)。
""")}
notes={}
for rid,q in bound.items():
 m=re.fullmatch(r'test-(calc|geom|prob|linalg|x)-(\d+)',rid);assert m
 notes[rid]={'manual_proof_and_scene_review':tables[m[1]][int(m[2])],
 'method':q['record'].get('method'), 'repair_reason':specs.get(rid,{}).get('reason')}
assert len(notes)==138
emit(OUT/'test-review-notes.json',notes);emit(OUT/'test-correction-specs.json',specs)
source='data/v2/test/dataset_test.jsonl';parent_path=PARENT/'candidate-sources'/source
parent=parent_path.read_bytes();original=(ROOT/source).read_bytes()
pb=next(x for x in json.loads((PARENT/'candidate-source-bindings.json').read_text(encoding='utf-8')) if x['source_path']==source)
assert sha(parent)==pb['raw_sha256'] and sha(original)==pb['source_raw_sha256']
write(OUT/'original-submission'/source,original);write(OUT/'parent-candidate'/source,parent)
original_rows={x['id']:x for x in rows(ROOT/source)}
version='codex-continuous-test-v1-20261007';candidate=[];patches=[];reviews=[];changed=[];preserved=[]
for pos,line in enumerate(parent.splitlines(keepends=True),1):
 old=json.loads(line.decode('utf-8-sig'));rid=old['id'];r=copy.deepcopy(old)
 if rid not in bound:candidate.append(line);preserved.append(rid);continue
 q=bound[rid];assert original_rows[rid]==q['record']==old
 assert sha(canon(old))==q['source']['record_version_sha256']
 if rid in specs:
  r.update(copy.deepcopy(specs[rid]['fields']))
  r.setdefault('revision_lineage',{}).update(version=version,continuous_correction_reason=specs[rid]['reason'],
   continuous_review_parent={'submitted_ref':q['source'],'parent_candidate_path':parent_path.relative_to(ROOT).as_posix(),'parent_raw_sha256':sha(parent),'parent_record_sha256':sha(canon(old))})
  r['versioned_id']=version+'-'+rid
  r['strict_review']={'math_content_sha256':sha(json.dumps({k:r[k] for k in ('problem','solution','answer','scene_spec')},ensure_ascii=False,sort_keys=True).encode()),
   'math_review_evidence':(OUT/'independent-test-review-138.jsonl').relative_to(ROOT).as_posix(),
   'core_math_verified':True,'scene_text_reviewed':True,'render_verified':False,'admitted':False,
   'verification_basis':'INDEPENDENT_PROOF_AND_EXACT_EXPRESSION_REVIEW_WITH_EXACT_WITNESSES'}
  fields=[k for k in set(old)|set(r) if old.get(k)!=r.get(k)]
  patches.append({'id':rid,'source':q['source'],'reason':specs[rid]['reason'],'before_record_sha256':sha(canon(old)),'after_record_sha256':sha(canon(r)),
   'changed_fields':sorted(fields),'before_fields':{k:old.get(k) for k in fields},'after_fields':{k:r.get(k) for k in fields},'corrected_record':r})
  changed.append(pos);candidate.append(canon(r)+b'\n')
 else:candidate.append(line)
 reviews.append({'id':rid,'source':q['source'],'candidate_record_sha256':sha(canon(r)),
  'before_math':'ISSUE' if any(k in specs.get(rid,{}).get('fields',{}) for k in ('problem','solution','answer')) else 'PASS',
  'before_scene_text':'ISSUE_OR_SYNC_REQUIRED' if rid in specs else 'PASS',
  'post_repair_math':'PASS','post_repair_scene_text':'PASS','exact_expression_policy':'PASS','independent_basis':notes[rid],
  'semantic_isolation':'NOT_ESTABLISHED','native_render':'UNVERIFIED','admitted':False})
assert len(candidate)==150 and len(reviews)==138 and len(preserved)==12
dest=OUT/'candidate-sources'/source;cb=b''.join(candidate);write(dest,cb)
emit(OUT/'test-candidate-source-bindings.json',{'source_path':source,'source_raw_sha256':sha(original),'source_bytes':len(original),
 'parent_candidate_path':parent_path.relative_to(ROOT).as_posix(),'parent_raw_sha256':sha(parent),
 'path':dest.relative_to(ROOT).as_posix(),'raw_sha256':sha(cb),'bytes':len(cb),'records':150,
 'reviewed_records':138,'changed_lines':changed,'previous_12_preserved':preserved})
write(OUT/'test-corrections.jsonl',b''.join(canon(x)+b'\n' for x in sorted(patches,key=lambda x:x['id'])))
write(OUT/'independent-test-review-138.jsonl',b''.join(canon(x)+b'\n' for x in sorted(reviews,key=lambda x:x['id'])))
md=['# 测试稿独立复核与修订','',f'范围：新138条，修订{len(patches)}条；完整150条继承旧12条修订。数学及场景文字判定绑定当前候选版本，未通过结构隔离和实际渲染前不准入。','']
for q in sorted(patches,key=lambda x:x['id']):
 r=q['corrected_record'];md+=['## '+r['id'],'',q['reason'],'','题目：'+r['problem'],'','过程：'+r['solution'],'','答案：'+r['answer'],'','修订后：数学内容与场景文字合格。','']
write(OUT/'TEST_CORRECTIONS.md',('\n'.join(md)+'\n').encode())
print(json.dumps({'independent_review':138,'repaired':len(patches),'candidate':150,'prior_12_preserved':True},indent=2))
