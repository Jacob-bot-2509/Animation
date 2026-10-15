"""Versioned independent eval review, exact symbolic proofs, no submitted-source mutation."""
from pathlib import Path
import json,hashlib,copy,re,sys
ROOT=Path(__file__).resolve().parents[4]
OUT=Path(__file__).resolve().parent
QUEUE=OUT.parent
PARENT=ROOT/'reviews/codex-supervision/2026-10-07-math-batch-supervision'
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def write(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 if p.exists() and p.read_bytes()!=b:
  if '--replace-unfrozen' not in sys.argv or (OUT/'eval-delivery-manifest.json').exists() or str(p.relative_to(OUT)).startswith(('original-submission','parent-candidate')):raise ValueError('immutable artifact already exists: '+str(p))
 p.write_bytes(b)
def emit(p,x):write(p,(json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode())
def rows(p):return [json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
bound={}
for n in range(13,20):
 for q in rows(next((QUEUE/'bound-records').glob('batch'+str(n)+'-*'))/'records.jsonl'):bound[q['record']['id']]=q
assert len(bound)==291
specs={}
def patch(rid,reason,solution=None,append=None,problem=None,answer=None,objects=None,scene_replacements=None):
 old=bound[rid]['record'];r=copy.deepcopy(old)
 if rid in specs:r.update(copy.deepcopy(specs[rid]['fields']))
 if solution is not None:r['solution']=solution
 if append is not None:r['solution']+=append
 if problem is not None:r['problem']=problem
 if answer is not None:r['answer']=answer
 scene=copy.deepcopy(r['scene_spec'])
 if objects is not None:scene['objects']=objects
 if scene_replacements:
  for a,b in scene_replacements:
   scene['objects']=[x.replace(a,b) for x in scene['objects']]
 # Preserve the reviewed graphical objects, add exact proof and domain to synchronized steps.
 scene['steps']=['呈现题干及适用条件：'+r['problem']]+['依次呈现：'+x for x in scene['objects']]+['核对完整证明：'+r['solution'],'高亮结果：'+r['answer']]
 r['scene_spec']=scene
 fields={k:r[k] for k in ('problem','solution','answer','scene_spec') if old[k]!=r[k]}
 specs[rid]={'reason':(specs[rid]['reason']+'；' if rid in specs else '')+reason,'fields':fields}

seriesbridge=r'令$E=\sum_{k=0}^{\infty}1/k!$。因$k!\ge2^{k-1}$（$k\ge1$），该正项级数收敛。二项式展开给出$a_n=\sum_{k=0}^{n}c_{k,n}/k!$，其中$c_{0,n}=c_{1,n}=1$，$c_{k,n}=\prod_{j=0}^{k-1}(1-j/n)\in[0,1]$。对固定$m$，当$n\ge m$时有$\sum_{k=0}^{m}c_{k,n}/k!\le a_n\le E$；令$n\to\infty$再令$m\to\infty$，得$\lim a_n=E$。'
patch('eval-calc-003-s1','补齐题干要求的级数表示与极限相等证明',append=seriesbridge)
patch('eval-calc-003-s2','指数形式的e须与题干指定级数定义连接',append=r'为连接级数定义，令$E(x)=\sum_{k=0}^{\infty}x^k/k!$；比值判别及幂级数理论保证全实轴收敛且可逐项求导，故$E^{\prime}=E$、$E(0)=1$。于是$(e^{-x}E(x))^{\prime}=0$，$E(x)=e^x$，特别地$e=\sum_{k=0}^{\infty}1/k!$。')
inverse=r'反解$e^y=x+\sqrt{x^2+a^2}$，得$x=(e^{2y}-a^2)/(2e^y)=(e^y-a^2e^{-y})/2=a\sinh(y-\ln a)$。代回时$\sqrt{x^2+a^2}=(e^y+a^2e^{-y})/2$，故没有平方引入的赘解。原函数严格递增，$x\to\pm\infty$时$y\to\pm\infty$，所以该反函数定义于$\mathbb R$。'
for s in (1,2):patch(f'eval-calc-006-s{s}','补齐反函数及其值域、回代验证',append=inverse)
patch('eval-calc-006-s2','arsinh对应双曲线的坐标符号应与代换一致',objects=[r'双曲线$Y^2-X^2=a^2$的上支：$X=a\sinh t,\ Y=a\cosh t$',r'恒等式$\sinh t+\cosh t=e^t$；反函数$x=a\sinh(y-\ln a)$'])
patch('eval-calc-007-s3','包络法须真正推导二阶导，y的二阶导不是切线转角速率',solution=r'星形线的切线族为$F(x,y,t)=x\sin t+y\cos t-a\sin t\cos t=0$；包络条件$F_t=0$给出$x=a\cos^3t,\ y=a\sin^3t$。在$\sin t\cos t\ne0$时，沿包络对$F=0$求导，因$F_t=0$，得$\sin t+\cos t\,y^{\prime}=0$，故$y^{\prime}=-\tan t$。再由$x^{\prime}=-3a\cos^2t\sin t$，得$y^{\prime\prime}=(-\sec^2t)/x^{\prime}=1/(3a\cos^4t\sin t)$。切线的轴截距为$a\cos t,a\sin t$，两截距点间距为$a$。尖点$t=k\pi/2$需另判：$t=k\pi$处切线水平，$t=\pi/2+k\pi$处切线竖直；尖点不套用上述二阶导公式。',objects=[r'滑动长度$a$的线段与包络$F=F_t=0$',r'四尖点处参数速度为零；切线分别水平或竖直，切线本身不发生无向角跳变',r'切线截距$a\cos t,a\sin t$及正则点的$y^{\prime\prime}$公式'])
patch('eval-calc-011-s2','级数项对应幂函数积分，不能声称等高矩形条带面积恰等于该项',objects=[r'在$[0,1/2]$叠加幂函数$x^{n-1}$的面积',r'$\int_0^{1/2}x^{n-1}dx=1/(n2^n)$；非负项用单调收敛交换求和与积分'])
patch('eval-calc-012-s3','原拼接没有构造证明，改用明确的角平分线长度关系',solution=r'取直角三角形$ABC$，$\angle B=\pi/2$，$AB=\sqrt3,\ BC=1,\ AC=2$，则$\angle A=\pi/6$。其角平分线$AD$与$BC$交于$D$。由角平分线定理$BD/DC=AB/AC=\sqrt3/2$及$BD+DC=1$，得$BD=\sqrt3/(2+\sqrt3)$。在直角三角形$ABD$中$\angle BAD=\pi/12$，故$\tan(\pi/12)=BD/AB=1/(2+\sqrt3)=2-\sqrt3$。再由余角关系$\tan(5\pi/12)=1/\tan(\pi/12)=2+\sqrt3$。',objects=[r'直角三角形$AB=\sqrt3,\ BC=1,\ AC=2$及角平分线$AD$',r'$BD/DC=\sqrt3/2$，$BD=\sqrt3/(2+\sqrt3)$',r'$\tan(\pi/12)=BD/AB=2-\sqrt3$'])
patch('eval-calc-020-s2','积分判别只判敛散，补齐收敛时的精确值',append=r'收敛时再直接计算：$\int_1^b x^{-p}dx=(b^{1-p}-1)/(1-p)$（$p\ne1$）；当$p>1$，$b^{1-p}\to0$，所得值为$1/(p-1)$；$p=1$时积分为$\ln b\to\infty$。')
patch('eval-calc-020-s3','把局部数值估计替换为覆盖所有p的严格上下界',solution=r'对$k\ge0$，在$[2^k,2^{k+1}]$上单调性给出$2^{-p(k+1)}\le x^{-p}\le2^{-pk}$，故$2^{-p}2^{(1-p)k}\le\int_{2^k}^{2^{k+1}}x^{-p}dx\le2^{(1-p)k}$。当$p>1$，右侧按公比$2^{1-p}<1$构成收敛几何级数；当$0<p\le1$，各块的下界至少为$2^{-p}>0$，总面积发散。求收敛值时令$x=e^t$，则$\int_1^\infty x^{-p}dx=\int_0^\infty e^{-(p-1)t}dt=1/(p-1)$（$p>1$）。',objects=[r'二进分块$[2^k,2^{k+1}]$及严格上下界',r'$2^{-p}2^{(1-p)k}\le A_k\le2^{(1-p)k}$',r'临界$p=1$；收敛值$1/(p-1)$'])
patch('eval-calc-020-s1','p=1的对数来自积分，不是b的零次幂',objects=[r'有限积分：$p\ne1$时$(b^{1-p}-1)/(1-p)$；$p=1$时$\ln b$',r'$p>1$收敛于$1/(p-1)$；$0<p\le1$发散'])
patch('eval-calc-021-s1','错位相减前补齐收敛依据',append=r'上述无限级数运算的依据为$a_n=n/2^n>0$且$a_{n+1}/a_n=(n+1)/(2n)\to1/2<1$，故绝对收敛；也可直接验证有限和$\sum_{n=1}^N n/2^n=2-(N+2)/2^N$后取极限。')
patch('eval-calc-022-s2','错位相减前补齐绝对收敛依据及有限和复验',append=r'因$a_{n+1}/a_n=(n+1)^2/(2n^2)\to1/2<1$，原级数绝对收敛，所用移项成立。有限和恒等式为$\sum_{n=1}^N n^2/2^n=6-(N^2+4N+6)/2^N$，取极限即得$6$。')
patch('eval-calc-022-s1','场景把一个单项误写成求和的值，补Σ',scene_replacements=[(r'$n^2x^n=\dfrac{x(1+x)}{(1-x)^3}$',r'$\sum_{n=1}^{\infty}n^2x^n=\dfrac{x(1+x)}{(1-x)^3}\quad(|x|<1)$')])
patch('eval-calc-024-s1','用有限几何展开余项证明端点，而非只证明开区间',append=r'端点也可直接处理：$\frac1{1+t^2}=\sum_{k=0}^N(-1)^kt^{2k}+(-1)^{N+1}\frac{t^{2N+2}}{1+t^2}$。从$0$积分到$x\in[-1,1]$，余项满足$|R_N(x)|\le|x|^{2N+3}/(2N+3)\le1/(2N+3)\to0$，故展开在整个闭区间成立，$x=1$给出$\pi/4=\sum_{k=0}^\infty(-1)^k/(2k+1)$。')
patch('eval-calc-024-s2','补齐Abel定理所需的开区间展开依据',append=r'开区间的展开来自几何级数$1/(1+t^2)=\sum_{k=0}^{\infty}(-1)^kt^{2k}$，在任意紧子区间$[-r,r]$（$r<1$）一致收敛，可从$0$逐项积分得到$\arctan x$的幂级数，再结合上述端点收敛及Abel定理。')
patch('eval-calc-024-s3','给出高阶导数界的明确公式和证明',append=r'所用导数界可由部分分式严格验证：对$m\ge1$，$f^{(m)}(t)=\frac{(-1)^{m-1}(m-1)!}{2i}[(t-i)^{-m}-(t+i)^{-m}]$，于是$|f^{(m)}(t)|\le(m-1)!(1+t^2)^{-m/2}\le(m-1)!$。同时$f^{(2k+1)}(0)=(-1)^k(2k)!$，$f^{(2k)}(0)=0$；泰勒余项界$1/(N+1)$确实趋于零。')
patch('eval-calc-025-s3','删除数值量级推断，使用Abel分部求和与精确下界',solution=r'令$a_n=1/\ln n$（$n\ge2$），则$a_n\downarrow0$。对任意$p\ge2$，令$B_j=\sum_{n=p}^j(-1)^n$，有$|B_j|\le1$。Abel分部求和给出$\sum_{n=p}^q(-1)^na_n=B_qa_q+\sum_{j=p}^{q-1}B_j(a_j-a_{j+1})$，故其绝对值不超过$a_q+\sum_{j=p}^{q-1}(a_j-a_{j+1})=a_p\to0$，由Cauchy准则交错级数收敛。绝对级数的有限和满足$\sum_{n=2}^N1/\ln n\ge(N-1)/\ln N\to\infty$，其中$\ln N/N\to0$由洛必达法则得到。因此是条件收敛。')
patch('eval-calc-029-s2','弧长微元补第一象限和绝对值条件',append=r'上述$x$积分限定在第一象限$0<x\le a$，其中$ds=a^{1/3}x^{-1/3}|dx|$；从$x=0$到$a$积分可写为$a^{1/3}\int_0^a x^{-1/3}dx=3a/2$，端点按反常积分收敛处理，再由四象限对称得$6a$。',scene_replacements=[(r'$ds=a^{1/3}x^{-1/3}dx$',r'$ds=a^{1/3}x^{-1/3}|dx|\quad(0<x\le a)$')])
patch('eval-calc-030-s3','内外半径之间是圆环截面',scene_replacements=[('水平圆盘的内外半径','水平圆环的外、内半径')])
patch('eval-geom-001-s3','Lagrange驻点需证明是全局最小距离点',append=r'在约束平面内，设垂足$Q=(19/9,13/9,1/9)$；$P-Q$与平面法向量平行，故对任意平面内$X$有$(P-Q)\cdot(X-Q)=0$。因此$|P-X|^2=|P-Q|^2+|X-Q|^2=25/9+|X-Q|^2\ge25/9$，等号只在$X=Q$取到，证明此驻点是唯一全局极小点。')
patch('eval-geom-002-s3','第三解不能仅引用第二解排除相交',solution=r'两方向$d_1=(2,1,-1)$、$d_2=(1,2,1)$满足$d_1\times d_2=(3,-3,3)\ne0$，故不平行。两基点差$\Delta=(-2,3,-2)$与叉积的内积为$-21\ne0$；若相交，则$\Delta$必在$\operatorname{span}\{d_1,d_2\}$中，内积应为零，矛盾。因此两线不相交且不平行，是异面直线。')
patch('eval-geom-006-s1','非齐次解集是仿射直线，不是线性解空间',solution=bound['eval-geom-006-s1']['record']['solution'].replace('解空间','解集（仿射直线）'),scene_replacements=[('解空间一维','仿射解集维数一')])
sections=r'截面$y=k$为$4x^2+z^2=1+k^2$，始终为椭圆。截面$z=k$为$4x^2-y^2=1-k^2$：$|k|<1$沿$x$开口，$|k|>1$沿$y$开口，$|k|=1$退化为$y=\pm2x$。截面$x=k$为$z^2-y^2=1-4k^2$：$|k|<1/2$沿$z$开口，$|k|>1/2$沿$y$开口，$|k|=1/2$退化为$z=\pm y$。由一个负平方和两个正平方组成的标准式且$y=k$截面始终非空，知为绕$y$轴的单叶双曲面。'
for s in (1,2,3):
 patch(f'eval-geom-007-s{s}','补齐截面法及两组退化边界',solution=(bound[f'eval-geom-007-s{s}']['record']['solution']+sections if s!=2 else sections),objects=[r'$y=k$的椭圆截面$4x^2+z^2=1+k^2$',r'$z=k$在$k=\pm1$退化为两相交直线',r'$x=k$在$k=\pm1/2$退化为两相交直线',r'绕$y$轴的单叶双曲面'])
patch('eval-geom-008-s3','仅凭几个典型截面不足以严格分类，补两连通分支表达式',append=r'严格分类令$u=x+y,\ v=y,\ w=z$，这是可逆线性替换。原式化为$2u^2-v^2-w^2=1$，故$u=\pm\sqrt{(1+v^2+w^2)/2}$。两个符号分支分别是定义于$\mathbb R^2$的连续图像，各自连通，且由$|u|\ge1/\sqrt2$隔开，故恰为双叶双曲面。')
patch('eval-geom-010-s1','补题干要求的两族直母线',append=r'两族直母线显式写成$(x,y,z)=(t,c,ct)$和$(c,t,ct)$（$c,t\in\mathbb R$）。每一点$(x_0,y_0,x_0y_0)$都同时落在$c=y_0$的第一族及$c=x_0$的第二族上。')
patch('eval-geom-010-s3','一般竖直截面并非直线，限制为两个坐标方向',solution=bound['eval-geom-010-s3']['record']['solution'].replace('竖直截面均为直线','上述两个坐标方向的竖直截面均为直线'),scene_replacements=[('竖直截面（直线族）','坐标方向竖直截面（直线族）'),('水平截面（等轴双曲线）','水平截面（非零高度为等轴双曲线，零高度为两相交直线）')])
patch('eval-geom-011-s2','距离和弦长仅核对另一解，补独立推导交点',append=r'设直线点$r(t)=(1+t,t,t)$，沿方向$d=(1,1,1)$到球心的最近参数满足$r(t)\cdot d=1+3t=0$，故$t_0=-1/3$、垂足$Q=(2/3,-1/3,-1/3)$。由正交分解$|r(t)|^2=|Q|^2+|d|^2(t-t_0)^2=2/3+3(t+1/3)^2$。令其等于$4$，即$t=(-1\pm\sqrt{10})/3$，代入$r(t)$得到题中两个交点。')
patch('eval-geom-012-s3','展开圆柱只能得到坡角，补Frenet框架导出曲率挠率',append=r'严格推导设$e_r=(\cos t,\sin t,0)$、$e_\theta=(-\sin t,\cos t,0)$、$e_z=(0,0,1)$，令$\tan\alpha=b/a$。单位切向量$T=\cos\alpha\,e_\theta+\sin\alpha\,e_z$，$ds/dt=a/\cos\alpha$。于是$dT/ds=-(\cos^2\alpha/a)e_r$，故$N=-e_r$、$\kappa=\cos^2\alpha/a$；$B=T\times N=\cos\alpha\,e_z-\sin\alpha\,e_\theta$，$dB/ds=(\sin\alpha\cos\alpha/a)e_r=-\tau N$，故$\tau=\sin\alpha\cos\alpha/a$。代$\cos\alpha=a/\sqrt{a^2+b^2}$、$\sin\alpha=b/\sqrt{a^2+b^2}$即得$\kappa=a/(a^2+b^2)$、$\tau=b/(a^2+b^2)$。')
patch('eval-geom-016-s3','把向量加法的补角和余弦定理的内角分开，避免符号误用',solution=r'将$\vec a,\vec b$置于同一起点，夹角$\pi/3$。平行四边形对角线给出$|\vec a+\vec b|^2=4+9+2\cdot2\cdot3\cos(\pi/3)=19$。以$2\vec a,\vec b$两终点及原点构成三角形，原点内角为$\pi/3$，对边为$2\vec a-\vec b$，由余弦定理$|2\vec a-\vec b|^2=16+9-2\cdot4\cdot3\cos(\pi/3)=13$。另有$|\vec a-\vec b|^2=4+9-2\cdot2\cdot3\cos(\pi/3)=7$，两对角线的点积$(\vec a+\vec b)\cdot(\vec a-\vec b)=|\vec a|^2-|\vec b|^2=-5$，故夹角余弦为$-5/\sqrt{19\cdot7}=-5/\sqrt{133}$。',objects=[r'平行四边形的和、差向量',r'三角形的两边为$2\vec a,\vec b$，内角$\pi/3$，对边为$2\vec a-\vec b$',r'余弦定理$16+9-24\cos(\pi/3)=13$'])
patch('eval-geom-017-s2','投影计算前补夹角余弦的独立求法',append=r'夹角也可由余弦定理独立确定：$|\vec a-\vec b|^2=|(3,1,0)|^2=10$，$|\vec a|=|\vec b|=3$，故$\cos\theta=(9+9-10)/(2\cdot3\cdot3)=4/9$。')
patch('eval-geom-019-s3','回代只证包含，补交线描述的完备性',append=r'完备性：任取两平面的公共点，令$z=t$，两式相减得$y+2t=5$，所以$y=5-2t$；代回第一式得$x=t-4$。因此每个公共点都在所列参数线上，已得到完整交线。')
monty=r'三扇门中车的位置等概率，初选与车的位置独立。主持人知道车的位置，总从未选的门中打开一扇有羊的门，并总给出换门机会。求坚持初选和换至唯一剩余未开的门各自获车概率。'
for s in (1,2,3):patch(f'eval-prob-001-s{s}','明确等概率、独立初选及主持人始终开羊门和提供换门条件',problem=monty)
patch('eval-prob-003-s2','期望递推需先排除无穷期望',append=r'递推中的期望有限：首次正面等待$X$满足$P(X>2k)=4^{-k}$，尾和公式给出$E[X]\le2\sum_{k=0}^{\infty}4^{-k}=8/3<\infty$，故可对递推式作有限数的移项，得到$E[X]=2$。')
for s in (1,2):
 patch(f'eval-prob-011-s{s}','等待时间递推和基本矩阵须先证明瞬态且期望有限',append=r'有限性：把抛掷分成互不重叠的两次一块，每块为HH的概率$1/4$，各块独立。因此首次连续HH时间$T$满足$P(T>2k)\le(3/4)^k$，尾和公式给出$E[T]\le2\sum_{k=0}^{\infty}(3/4)^k=8<\infty$。吸收概率为1，期望有限，所以递推及基本矩阵的期望运算有效。')
patch('eval-prob-012-s3','边界交集为零概率，不应将两个闭事件称为集合互补',solution=bound['eval-prob-012-s3']['record']['solution'].replace('互补','覆盖全空间且交集为零概率边界'),scene_replacements=[('互补事件等概率','两侧事件等概率且交集边界概率为零')])
patch('eval-prob-014-s2','补危险率微分方程的初值、适用条件及条件概率',append=r'上述常危险率刻画限定于非负、绝对连续且$F(0)=0$、生存函数正的分布。令$S=1-F$，则$S^{\prime}=-\lambda S$、$S(0)=1$，故$S(t)=e^{-\lambda t}$。所以$P(X>s+t\mid X>s)=S(s+t)/S(s)=e^{-\lambda t}=P(X>t)$，完成无记忆性证明。')
patch('eval-prob-015-s1','场景均值3.5改为精确分数7/2',scene_replacements=[('$3.5$',r'$\dfrac72$')])
patch('eval-linalg-002-s3','消元只作用前三行，不能把末行也减成零行',solution=bound['eval-linalg-002-s3']['record']['solution'].replace('每行减末行','第一、二、三行分别减第四行，第四行保持不变'),scene_replacements=[('每行减末行','前三行分别减第四行（第四行保持不变）')])
generalrow=r'对$n\ge2$，矩阵$M=bI+aJ$中$R_i\leftarrow R_i-R_1$（$i=2,\ldots,n$），第$i$行只在第1列有$-b$、第$i$列有$b$。再令$C_1\leftarrow C_1+C_2+\cdots+C_n$，第一列变为$(na+b,0,\ldots,0)^T$，余下主对角为$b$，所以$\det M=(na+b)b^{n-1}$。$n=1$时直接为$a+b$。全过程不除以$b$，包含$b=0$。'
patch('eval-linalg-004-s1','三阶例子没有证明题干的n阶一般情形',append=generalrow,objects=[r'$R_i\leftarrow R_i-R_1$（$2\le i\le n$）',r'$C_1\leftarrow\sum_{j=1}^nC_j$后第一列为$(na+b,0,\ldots,0)^T$',r'$\det M=(na+b)b^{n-1}$；$n=1$另作$a+b$'])
patch('eval-linalg-004-s2','场景仅标三阶谱，改为n阶谱和重数',scene_replacements=[(r'特征值 $b+3a,b,b$',r'特征值$b+na$（沿全1向量）、$b$（其正交补，重数$n-1$）')])
patch('eval-linalg-004-s3','补一般n阶拆列计数',append=r'一般$n\ge2$同理：每列为$be_j+a\mathbf1$。多重线性展开中，选择两个及以上$a\mathbf1$列的项因重复列为零；全选$be_j$给$b^n$；恰选一个$a\mathbf1$列有$n$项，每项为$ab^{n-1}$（把该列的$\mathbf1=\sum_j e_j$展开，只有原列位置的$e_j$能留下非零行列式）。故总和为$b^n+nab^{n-1}=(na+b)b^{n-1}$。$n=1$直接为$a+b$。')
patch('eval-linalg-006-s3','第三解不能只引用第二解，补独立坐标迭代',solution=r'该矩阵作用为$(x,y)\mapsto(x+y,y)$。归纳可得迭代$n\ge0$次为$(x+ny,y)$（$n=0$为恒等；再作用一次把$x+ny$变为$x+(n+1)y$）。因此$A^n=\begin{pmatrix}1&n\\0&1\end{pmatrix}$。')
for s in (1,2,3):patch(f'eval-linalg-007-s{s}','明确整数次幂的n适用域',problem=bound[f'eval-linalg-007-s{s}']['record']['problem']+r'其中$n\in\mathbb Z_{\ge0}$；$n=0$时按$A^0=I$。')
patch('eval-linalg-008-s3','面积非负，负号表示定向而非面积',scene_replacements=[('面积 $-2$（定向反转）','面积$2$，有向面积为$-2$（定向反转）')])
patch('eval-linalg-009-s2','Laplace展开与题干指定的分块方法建立对应',append=r'这正是分块上三角公式：取左上$2\times2$块$B=\begin{pmatrix}2&1\\1&2\end{pmatrix}$、右下块$C=(3)$，左下为零块，则$\det M=\det B\det C=3\cdot3=9$。')
patch('eval-linalg-011-s1','非齐次解集应为二维仿射平面',solution=bound['eval-linalg-011-s1']['record']['solution'].replace('解空间二维','解集为二维仿射平面'))
patch('eval-linalg-011-s2','去掉消元省略号，补精确最终行和分支条件',solution=r'交换第一、三行并消元得$\begin{pmatrix}1&1&\lambda&\lambda^2\\0&\lambda-1&1-\lambda&\lambda-\lambda^2\\0&1-\lambda&1-\lambda^2&1-\lambda^3\end{pmatrix}$。当$\lambda\ne1$，第二行除以$\lambda-1$为$(0,1,-1,-\lambda)$；第三行减去$(1-\lambda)$倍第二行，得到$(0,0,(1-\lambda)(\lambda+2),(1-\lambda)(\lambda+1)^2)$。因此$\lambda\ne1,-2$时三主元均非零，唯一解；$\lambda=-2$时末行为$0=3$，无解。$\lambda=1$时原三式均为$x+y+z=1$，解集为二维仿射平面，有无穷多解。')
patch('eval-linalg-011-s3','几何断言补行列式和常数项相容性验证',append=r'代数依据：法向量矩阵为$(\lambda-1)I+J$，行列式$(\lambda-1)^2(\lambda+2)$，在$\lambda\ne1,-2$可逆，所以三平面唯一公共点；$\lambda=-2$时三式相加左侧为0、右侧为$1-2+4=3$，故无公共点，各法向量两两不成比例且叉积均沿$(1,1,1)$，三条两两交线平行；$\lambda=1$时代入即为同一个平面。')
patch('eval-linalg-012-s2','行变换省略号改成完整秩与核空间证明',solution=r'矩阵$(a-1)I+J$的行列式为$(a-1)^2(a+2)$，$a\ne1,-2$时秩3，只有零解。$a=1$时全1矩阵秩1，核为$x+y+z=0$，维数2。$a=-2$时每行和为0，秩不超过2；左上二阶子式为$4-1=3\ne0$，故秩恰2。第一式减第二式为$-3x+3y=0$，再代回得$z=x$，故核为$\operatorname{span}\{(1,1,1)^T\}$，维数1。')
patch('eval-linalg-013-s3','超平面的维数不能代替所求基础解系构造',append=r'具体取$\xi_1=(1,-1,0,0)^T,\xi_2=(1,0,-1,0)^T,\xi_3=(1,0,0,-1)^T$；它们都满足方程，且后三个分量直接保证线性无关。任意解$x$满足$x_1=-x_2-x_3-x_4$，所以$x=-x_2\xi_1-x_3\xi_2-x_4\xi_3$，给出完整通解。')
patch('eval-linalg-015-s1','补题干要求的对角化运算',append=r'取$P=((1,1)^T,(1,-1)^T)=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$，$\det P=-2\ne0$，逐列有$AP=P\operatorname{diag}(3,-1)$，故$P^{-1}AP=\operatorname{diag}(3,-1)$。')
patch('eval-linalg-015-s2','用明确正交替换替代省略的配方并给出对角化',solution=r'令$u=(x+y)/\sqrt2,\ v=(x-y)/\sqrt2$，逆变换$x=(u+v)/\sqrt2,\ y=(u-v)/\sqrt2$。则$x^2+y^2=u^2+v^2$、$4xy=2u^2-2v^2$，所以$f=3u^2-v^2$。对应正交矩阵$Q=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$满足$Q^TAQ=\operatorname{diag}(3,-1)$，列向量分别是特征值$3,-1$的单位特征向量。等价地取$P=\sqrt2Q$，有$P^{-1}AP=\operatorname{diag}(3,-1)$。')
patch('eval-linalg-015-s3','Q行列式为负，不应称其为平面旋转',scene_replacements=[('正交矩阵 $Q$ 的旋转作用','正交矩阵$Q$的基变换（$\\det Q=-1$，包含反射）')])
patch('eval-linalg-016-s1','特征值已求但漏验题干中的矩阵恒等式',append=r'一般二阶矩阵满足Cayley–Hamilton定理，将$p(\lambda)=\lambda^2-5\lambda+6$代入即得$p(A)=A^2-5A+6I=0$；这对所有满足给定迹与行列式的矩阵成立。')
patch('eval-linalg-017-s3','最小多项式判不可对角化之外须给出所求特征向量',append=r'求特征向量时，$Av=v$等价于$(A-I)(x,y)^T=(y,0)^T=0$，故所有非零特征向量为$t(1,0)^T$（$t\ne0$），仅一个特征方向。')
patch('eval-linalg-020-s3','避免把非紧的平行直线对称为退化椭圆',solution=r'$f=(x-2y)^2\ge0$，当且仅当$x=2y$时取0，并存在非零零向量$(2,1)$；故半正定而非正定。平方中的线性形式非零，矩阵为$(1,-2)^T(1,-2)$，秩1，正、负惯性指数分别为1、0。$f=k>0$的等值集恰为平行直线对$x-2y=\pm\sqrt k$，$k=0$为一条直线。',objects=[r'正高度等值集$x-2y=\pm\sqrt k$（$k>0$）',r'零方向$x=2y$与非零零向量$(2,1)$'])
patch('eval-linalg-021-s2','系数判正定补可逆变量替换及反向必要性',append=r'变量替换$u=x+y/2+az/2,\ v=y-az,\ w=z$的矩阵为上三角且行列式1，故可逆。若$2-a^2\le0$，取非零向量$(x,y,z)=(-a,a,1)$，前两平方为零且$f=2-a^2\le0$，因此上述条件也是必要条件。')
patch('eval-linalg-023-s2','补题干所问复数域的完整分解',append=r'复数域中$e^{2\pi ik/8}$（$k=0,\ldots,7$）是八个互异根，首项系数1，故$x^8-1=\prod_{k=0}^7(x-e^{2\pi ik/8})$。三个实二次因子的判别式分别为$-4,-2,-2$，均负，所以所列实分解确为实不可约分解。')
patch('eval-linalg-025-s3','漏了除以x-1的余式这一问',append=r'除以$x-1$时由余数定理，余式为$f(1)=1+1+1=3$。')
patch('eval-linalg-026-s3','体积数值应独立计算，不能未推导就引用另一解的18',append=r'具体计算$\alpha_2\times\alpha_3=(5,-1,-7)$，$\alpha_1\cdot(\alpha_2\times\alpha_3)=5-2-21=-18$，所以体积为18，结论由本解独立获得。')
patch('eval-linalg-028-s2','列为beta的P将beta坐标送至标准坐标，明确方向',solution=bound['eval-linalg-028-s2']['record']['solution'].replace('从标准基到基 $\\{\\beta_1,\\beta_2\\}$ 的过渡矩阵','把基$\\{\\beta_1,\\beta_2\\}$坐标映到标准坐标的矩阵'))
gs=r'按原顺序令$v_1=(1,1,0),v_2=(1,0,1),v_3=(0,1,1)$。首先$w_1=v_1$，$w_2=v_2-\frac{\langle v_2,w_1\rangle}{\langle w_1,w_1\rangle}w_1=(1/2,-1/2,1)$，可取非零倍数$u_2=(1,-1,2)$。随后$w_3=v_3-\frac12w_1-\frac16u_2=(-2/3,2/3,2/3)$，取$u_3=(-3/2)w_3=(1,-1,-1)$。三者非零且两两内积为0，故按题干指定的Gram–Schmidt得到$u_1=(1,1,0),u_2=(1,-1,2),u_3=(1,-1,-1)$。允许每个结果乘非零常数。'
patch('eval-linalg-030-s2','题干指定GS，原解仅构造另一正交基且与答案不对应',solution=gs,objects=[r'按输入原顺序投影：$w_2=v_2-\frac12v_1$',r'$w_3=v_3-\frac12v_1-\frac16(1,-1,2)$',r'非零倍数得到$(1,1,0),(1,-1,2),(1,-1,-1)$'])
patch('eval-linalg-030-s3','只验张成和行列式不等于执行GS，补投影过程和非零条件',append=gs,answer=r'$u_1=(1,1,0),\ u_2=(1,-1,2),\ u_3=(1,-1,-1)$；各自只允许乘非零常数。')
patch('eval-linalg-030-s1','可乘常数必须非零，否则不是正交化所得的基',answer=r'$u_1=(1,1,0),\ u_2=(1,-1,2),\ u_3=(1,-1,-1)$；各自只允许乘非零常数。')
patch('eval-linalg-033-s3','单边Laplace直接给非负t，补推广到全部实t',append=r'单边Laplace逆变换先给$t\ge0$的结果。候选$\Phi(t)=I+tA$对全部实$t$满足$\Phi^{\prime}=A\Phi$、$\Phi(0)=I$，由线性常微分方程初值问题唯一性，$\Phi(t)=e^{tA}$对全部实$t$成立。')
patch('eval-linalg-034-s3','向量证明不能任意中心化，直接构造有限均匀样本并保留原内积',solution=r'设$\vec a,\vec b\in\mathbb R^n$，取均匀样本空间$\{1,\ldots,n\}$，定义$X(i)=a_i,\ Y(i)=b_i$。于是$E[X^2]=|\vec a|^2/n$、$E[Y^2]=|\vec b|^2/n$、$E[XY]=(\vec a\cdot\vec b)/n$，不作中心化。若$E[Y^2]=0$，则$\vec b=0$，不等式成立。否则由$E[(X-tY)^2]\ge0$，在$t=E[XY]/E[Y^2]$处得$E[X^2]-(E[XY])^2/E[Y^2]\ge0$，代回并开方即得$|\vec a\cdot\vec b|\le|\vec a||\vec b|$。等号当且仅当$X=tY$在每个样本点成立，或$\vec b=0$，也就是两向量线性相关。')
for s in (1,2,3):patch(f'eval-linalg-034-s{s}','答案明确该条证明结论，不引用三种解法作为答案',answer=r'$|\vec a\cdot\vec b|\le|\vec a||\vec b|$；等号当且仅当两向量线性相关（包括零向量）。')
patch('eval-linalg-035-s3','必要条件与反例不证明题干充要性，补两方向严格推导',solution=r'记标准基为$e_1,\ldots,e_n$，$A$的列为$a_i=Ae_i$。若$A^TA=I$，则$a_i\cdot a_j=e_i^TA^TAe_j=\delta_{ij}$；若$\sum_i c_i a_i=0$，分别与$a_j$取内积得$c_j=0$，所以这$n$个单位正交向量是$\mathbb R^n$的基。反过来，若列向量构成标准正交基，则$(A^TA)_{ij}=a_i\cdot a_j=\delta_{ij}$，故$A^TA=I$。行列式为$\pm1$本身不充分，例如剪切矩阵$\begin{pmatrix}1&1\\0&1\end{pmatrix}$的两列不正交；这个反例只是补充，不替代上述充要性证明。',objects=[r'$a_i=Ae_i$，$a_i\cdot a_j=e_i^TA^TAe_j$',r'$a_i\cdot a_j=\delta_{ij}$的双向等价及线性无关性证明',r'剪切反例说明仅凭行列式条件不充分'])
for s in (1,2,3):patch(f'eval-linalg-035-s{s}','答案明确两方向充要关系',answer=r'$A^TA=I\iff$列向量构成$\mathbb R^n$的标准正交基。')

# Independent reviewer notes: all three submitted variants were read, not inferred from author verdicts.
notes_by_topic={
'calc':{
1:r'半角恒等式、二阶Taylor、两次LHopital均给1/2；分母在去心邻域非零。',
2:r'x^x=exp(x ln x)，三种代换/求导均严格证明x ln x趋于0，极限1。',
3:r'二项式有限积、ln极限、有限头尾夹逼。修订补E(x)级数与指数的连接，极限Σ1/k!。',
4:r'因式分解、三阶Taylor、三次LHopital一致给-1/2；三阶导极限-3而分母为6。',
5:r'x>0，log、隐式、指数复合求导均为x^x(ln x+1)。',
6:r'a>0保证对数正和严格单调，导数1/√(x²+a²)；修订补反函数值域和无赘解回代。',
7:r'a>0正则点sin t cos t≠0，y′=-tan t,y″=1/(3a cos⁴t sin t)；包络解补真实导数，尖点另判。',
8:r'x>0分别用差函数、MVT和正Lagrange余项，得到e^x>1+x，Taylor还给更强严格界。',
9:r'0<a<b，arctan导数1/(1+x²)<1，MVT、差函数、割线证明一致。',
10:r'e^x割线或提取e^sinx、三次LHopital，夹逼中值点至0，极限1。',
11:r'|x|<1幂级数、非负项积分、逐项求导给Σ1/(n2^n)=ln2；场景改成幂函数面积。',
12:r'差角/半角公式给2-√3，第三解修为明确30度三角形角平分线；余角得2+√3。',
13:r'分部积分两次、待定系数、递推均给(x²-2x+2)e^x+C，导数为x²e^x。',
14:r'sin x≠0的每个连通区间，半角凑微分、万能代换、共轭式给ln|tan(x/2)|+C。',
15:r'已审s1/s2以x↦π-x对称或分部积分得到π²/4；旧s3修订保留，不在新291条内。',
16:r'a>0，trig替换/递推/复部分分式系数符号及连续log分支给相同精确原函数。',
17:r'tan替换及反射、Moebius替换、分部积分辅助积分，均得到πln2/8。',
18:r'分部积分、tan替换、自指递推给((x²+1)arctan x-x)/2+C。',
19:r'有限分部积分极限、Γ递推、非负尾积分给1，(b+1)e^-b严格趋于0。',
20:r'p>0；有限原函数、积分判别和修订的二进块精确界，p>1值1/(p-1)，其余发散。',
21:r'比值判别保证错位移项，有限和2-(N+2)/2^N；幂级数/几何分布期望给2。',
22:r'二次幂级数求导、绝对收敛下错位相减、阶乘矩均给6；补有限和并修场景Σ。',
23:r'积分判别、1/[n(n-1)]裂项比较、Cauchy凝聚均证Σ1/n²收敛，未误称积分值为级数值。',
24:r'修订有限几何余项覆盖[-1,1]；Leibniz+Abel及明确高阶导界也证明端点，π/4交错展开。',
25:r'项1/ln n递减到0；交错/子列/修订Abel尾界均证收敛，绝对和精确下界趋∞，条件收敛。',
26:r'x>0直接偏导与log全微分给(1,2)处(2,0)，旧s3修订不覆盖。',
27:r'交换三角形积分顺序或F积分分部均给(e-1)/2，旧s3保留。',
28:r'圆盘(0,1),R=1；原点极坐标、水平截面、平行轴定理均给3π/2。',
29:r'a>0弧长；参数速度绝对值、第一象限x反常积分、滑杆包络均给6a。',
30:r'壳层、轴不穿区域内部的Pappus、水平圆环截面均得2π²，内外半径次序正确。'},
'geom':{
1:r'点(1,2,-1)，法向量(2,-1,2)，距离5/3；垂足(19/9,13/9,1/9)；Lagrange解补Pythag全局最小。',
2:r'方向叉积(3,-3,3)，基点差与叉积混合积-21；参数联立矛盾-1=6，第三解补独立不交证明。',
3:r'法向量(1,0,-1)，点(1,0,-1)给x-z=2；叉积、平面束λ=-1、包含两方向三法一致。',
4:r'法向量内积0、垂直交线截面方向内积0、另一法向量躺在方向平面，均为π/2。',
5:r'叉积面积、二次式配方、正交投影给距离1/√3，垂足(5/3,4/3,-1/3)。',
6:r'三式中第三为前两之和，秩2；y=0,x+z=1，解集是仿射直线非线性空间。',
7:r'标准式4x²+z²-y²=1单叶，修订三解补全部截面边界z=±1,x=±1/2为相交直线。',
8:r'实对称谱(3±√17)/2,-1；配方2(x+y)²-y²-z²=1；第三解补两连续图像证明双叶。',
9:r'x=1时y²/(27/4)+z²/(3/4)=1；参数化完整，x=k时|k|=2单点,>2空。',
10:r'45度旋转给z=(u²-v²)/2，双曲抛物面；补两直母线，竖直一般截面并非直线。',
11:r'球线交代入3t²+2t-3=0；配方或垂足与半弦导出t=(-1±√10)/3，三个解均完整。',
12:r'a,b>0 helix；cross/triple、Frenet及修订坡角frame均给κ=a/(a²+b²),τ=b/(a²+b²)。',
13:r'梯度、全微分、参数切向量叉积同法向量(-2,-2,1)，切平面2x+2y-z=2。',
14:r'椭圆点(√2,3/√2)，切线公式、隐导y′=-3/2、t=π/4参数导数均给3x+2y=6√2。',
15:r'两球相减得y=1/2，圆x²+z²=15/4；垂直平分面和参数回代一致。',
16:r'|a|2|b|3角π/3，和√19,2a-b模√13；和差夹角cos=-5/√133；第三解修正内角说明。',
17:r'a=(1,2,2),b=(-2,1,2)，norm3,dot4，cos4/9；投影4b/9，残差与b正交；第二解补cos求法。',
18:r'轴截距2,3,4四面体，det24/6、底3高4/3、Jac24单纯形1/6均体积4。',
19:r'独立平面法向量叉积(1,-2,1)，基点(-4,5,0)；第三解补任意公共点反推参数，完备交线。',
20:r'AB=(1,1,1),AC=(2,3,4),AD=(1,2,3)，AC=AB+AD；triple0,plane x-2y+z=0均证共面。'},
'prob':{
1:r'修订明确uniform独立初选及总开羊门/总换门机会，unconditional stay1/3/switch2/3；Bayes条件解另明公平开门。',
2:r'盒均匀、盒内币均匀；Bayes/六币枚举/树给另一金2/3。',
3:r'公平coin首次H；级数/修订有限性后递推/PGF均EX2，尾界排除无穷期望。',
4:r'两公平die独立，给X=3，则Z均匀1..6，P(Y≥8|X3)=1/3，E[Y|X3]=13/2。',
5:r'Xuniform(0,1),Y=-lnX；CDF/Jac/反变换均给Exp1，负半轴密度0。',
6:r'Poisson λ；直接二阶矩、factorial、MGF均EX²=λ²+λ,varλ，λ0按集中0可连续延拓。',
9:r'独立Exp1最小值；生存乘积、orderstat、joint矩形积分均Exp2，z≥0。',
10:r'n≥1uniform permutation固定点数；indicator不需独立、错排分类GF、双计数均期望1。',
11:r'公平coinHH等待；修订独立二块tail≤(3/4)^k，期望有限；states/basicmatrix/Fibonacci PGF均6。',
12:r'independentuniformsum；trianglearea、convolution、reflection双闭事件交界概率0，概率1/2。',
13:r'标准normal绝对值；symint/halfnormal/χ²(1)后√moment均√(2/π)。',
14:r'λ>0生存比、补初值后的hazardODE、Poisson独立增量均证s,t>0无记忆性。',
15:r'fairdie1..6；直接矩/MGF/uniformformula均均值7/2,方差35/12；场景小数修分数。'},
'linalg':{
1:r'Vandermonde行消元、多项式根和n归纳均prod差值；a=b分支已处理，1,2,3值2。',
2:r'4阶diag1,2,3,4 off1；减首行、border升5阶、修订前三行减末行均det6。',
3:r'三对角diag2 off1；D0=1,D1=2 recurrence、path谱乘积、归纳均n+1。',
4:r'n≥1 diag a+b offa；修订n阶row/col消元、rankone谱、多重线性选择0/1列均b^(n-1)(na+b)，n1另列。',
5:r'A[[3,2],[4,3]],det1，adjugate/GaussJordan/columns solve均inverse[[3,-2],[-4,3]]。',
6:r'Jordan2ones，n≥0，induction/binomial nilpotence/修订坐标迭代给[[1,n],[0,1]]。',
7:r'旋转矩阵整数n≥0；和角归纳、复P对角化、复乘法均rotation nθ，θkπ亦成立。',
8:r'A[[1,2],[3,4]],det-2 rank2 inverse[[-2,1],[3/2,-1/2]]，adj/Gauss/AAinv与场景有向面积区分。',
9:r'blockuppertri diagblocks[[2,1],[1,2]]和3，det9；Laplace补指定分块，直接展开一致。',
10:r'Acols c3=c1+c2独立c1/c2；rowechelon2,det0且minor-1三法均rank2。',
11:r'参数det(λ+2)(λ-1)²；修订完整消元，λ1仿射解平面,λ-2矛盾0=3,其余unique。',
12:r'homogeneousparameter a；a1kernelplane维2,a-2span(1,1,1)维1，其余0；谱、修订minor秩、J谱一致。',
13:r'4元和0；3basis(1,-1,0,0),(1,0,-1,0),(1,0,0,-1)，rank1nullity3；第三解补生成完备性。',
14:r'a非零real，symmetric tri eigen1,1±√2a；orthbasis(1,0,-1)/√2,(1,±√2,1)/2；限制/配方一致，boundarycylinder。',
15:r'A[[1,2],[2,1]] eigen3,-1，P[[1,1],[1,-1]] det-2；补s1 diagonalization及s2完整正交替换，s3Q含反射。',
16:r'2阶tr5 det6,char(λ2)(λ3)；s1补CH恒等式，s2CH加例，s3distincteigen diagonalization均成立。',
17:r'Jordan2(1)，eigen1double,kernelspan(1,0)，geomdim1所以nondiag；s3补全部非零eigenvectors。',
18:r'A[[2,1],[1,2]]，diag3,1/binomialJ²2J/CHrecurrence给half[[3^100+1,3^100-1],[3^100-1,3^100+1]]。',
19:r'form x²+2y²+az²+2xy+2xz；square/congruenceC/LDL均diag1,1,a-2，positiveiffa>2;nulla2span(-2,1,1)。',
20:r'(x-2y)² rank1semiPOS,positiveindex1negative0；eigen5,0；修订等值线解释。',
21:r'principalminors2,1,2-a²；square可逆且见证(-a,a,1)、SchurB^-1[[1,-1],[-1,2]]，iff|a|<√2。',
22:r'quarticroots1,2,-2,-3，rationaltest/quadraticcoefficients/synthetic除法给四线性因子。',
23:r'8次单位根全部互异；共轭配对/平方差/恒等式，完整实不可约三个quadratic判别式负。',
24:r'x3-7x6在1中心Taylor、连synthetic除法、换元均(x-1)³+3(x-1)²-4(x-1)。',
25:r'x5+x1除x1余3，除x²1余2x1；复杂根系数real、长除法、±i二式，s3补第一问。',
26:r'rows(1,2,3),(2,3,1),(3,1,2)det-18，唯一零解、补体积独立算cross，线性无关。',
27:r'Wspan(1,1,0),(0,1,1)，linearorth、GSextension、cross均perp span(1,-1,1)。',
28:r'βcolumnsP[[1,1],[2,1]],det-1，coordinatesP^-1(2,3)=(1,1)，修正P方向；线性组合和方程均同。',
29:r'T[[1,2],[2,1]],det-3，kernel0imageR²，逆解x=(2v-u)/3,y=(2u-v)/3，谱非零及A²可逆同证。',
30:r'原顺序GS w2=(1/2,-1/2,1),w3=(-2/3,2/3,2/3)，仅乘非零常数得三正交基；替代basis解改实际GS。',
31:r'minimal(λ2)²(λ3),dim4,tr9=>multiplicities3,1；maxblock2和1，唯一J2(2)⊕2⊕3，primarydecomp一致。',
32:r'polymatrixminor1⇒D1=D2=1,D3=(λa)(λ1)²；Smith交换消去及cyclic e3 determinant1均证invariant，a1合并3次。',
33:r'nilpotentA²0，exp=I+tA；series、IVPode、resolvent+修订全实t延拓一致。',
34:r'realvectors；discriminant/projection/修订uniformfinite sample直接Gram，零向量分支及等号iffdependent。',
35:r'iffA^TAI与columnsorthnormalbasis；entryinnerproducts/保长polarization/修订第三解双向完整证明。'}
}
notes={}
for rid,q in bound.items():
 m=re.fullmatch(r'eval-(calc|geom|prob|linalg)-(\d+)-s([123])',rid);assert m
 notes[rid]={'scope':'MANUAL_PROBLEM_ALL_SUBMITTED_PROOF_AND_ANSWER_PLUS_SCENE_TEXT',
 'topic_verification':notes_by_topic[m[1]][int(m[2])],
 'reviewed_variant':m[3],'method':q['record']['method'],
 'repair_reason':specs.get(rid,{}).get('reason')}
# Clarify the same nonzero multiplier condition in GS s2.
patch('eval-linalg-030-s2','正交化基只允许非零倍数',answer=r'$u_1=(1,1,0),\ u_2=(1,-1,2),\ u_3=(1,-1,-1)$；各自只允许乘非零常数。')
# Correct prime notation in a scene string; keep proof derivative unambiguous.
specs['eval-calc-007-s3']['fields']['scene_spec']['objects'][-1]=r'切线截距$a\cos t,a\sin t$；正则点二阶导数$\frac{d^2y}{dx^2}$'
notes['eval-linalg-030-s2']['repair_reason']=specs['eval-linalg-030-s2']['reason']
methods={'eval-calc-012-s3':'几何构造：角平分线定理','eval-calc-020-s3':'二进分块精确比较与指数换元','eval-calc-025-s3':'Abel分部求和与精确下界','eval-linalg-006-s3':'剪切变换的坐标迭代','eval-linalg-030-s2':'Gram–Schmidt逐次投影','eval-linalg-035-s3':'标准基像与列内积的双向证明'}
for rid,sp in specs.items():
 sp['fields']['efficiency_tags']=copy.deepcopy(sp['fields']['scene_spec']['objects'])
 if rid in methods:sp['fields']['method']=methods[rid]

emit(OUT/'eval-correction-specs.json',specs);emit(OUT/'eval-review-notes.json',notes)
source='data/v2/eval/dataset_eval.jsonl'
parent_path=PARENT/'candidate-sources'/source
parent=parent_path.read_bytes()
pb=next(x for x in json.loads((PARENT/'candidate-source-bindings.json').read_text(encoding='utf-8')) if x['source_path']==source)
assert sha(parent)==pb['raw_sha256']
original=(ROOT/source).read_bytes()
assert sha(original)==next(iter(bound.values()))['source']['source_raw_sha256']
write(OUT/'original-submission'/source,original)
write(OUT/'parent-candidate'/source,parent)
origrows={r['id']:r for r in rows(ROOT/source)}
version='codex-continuous-eval-v1-20261007'
candidate=[];patches=[];reviews=[];changed=[];preserved_previous=[]
for line_no,line in enumerate(parent.splitlines(keepends=True),1):
 old=json.loads(line.decode('utf-8-sig'));rid=old['id'];r=copy.deepcopy(old)
 if rid not in bound:preserved_previous.append(rid);candidate.append(line);continue
 q=bound[rid]
 assert origrows[rid]==q['record'] and sha(canon(q['record']))==q['source']['record_version_sha256']
 assert old==q['record'],'unreviewed parent differs for '+rid
 if rid in specs:
  r.update(copy.deepcopy(specs[rid]['fields']))
  lineage=r.setdefault('revision_lineage',{})
  lineage['continuous_review_parent']={'submitted_ref':q['source'],'parent_candidate_path':str(parent_path.relative_to(ROOT)).replace('\\','/'),'parent_raw_sha256':sha(parent),'parent_record_sha256':sha(canon(old))}
  lineage['version']=version;lineage['continuous_correction_reason']=specs[rid]['reason']
  r['versioned_id']=version+'-'+rid
  r['strict_review']={'math_content_sha256':sha(json.dumps({k:r[k] for k in ('problem','solution','answer','scene_spec')},ensure_ascii=False,sort_keys=True).encode()),
  'math_review_evidence':str((OUT/'independent-eval-review-291.jsonl').relative_to(ROOT)).replace('\\','/'),
  'core_math_verified':True,'scene_text_reviewed':True,'render_verified':False,'admitted':False,
  'verification_basis':'INDEPENDENT_ALL_PROOFS_AND_EXACT_WITNESSES'}
  fields=[k for k in set(old)|set(r) if old.get(k)!=r.get(k)]
  patches.append({'id':rid,'source':q['source'],'reason':specs[rid]['reason'],'before_record_sha256':sha(canon(old)),'after_record_sha256':sha(canon(r)),
  'changed_fields':sorted(fields),'before_fields':{k:old.get(k) for k in fields},'after_fields':{k:r.get(k) for k in fields},'corrected_record':r})
  changed.append(line_no);candidate.append(canon(r)+b'\n')
 else:candidate.append(line)
 reviews.append({'id':rid,'source':q['source'],'candidate_record_sha256':sha(canon(r)),
 'before_math':'ISSUE' if any(k in specs.get(rid,{}).get('fields',{}) for k in ('problem','solution','answer')) else 'PASS',
 'before_scene_text':'ISSUE_OR_SYNC_REQUIRED' if rid in specs else 'PASS',
 'post_repair_math':'PASS','post_repair_scene_text':'PASS','exact_expression_policy':'PASS','independent_basis':notes[rid],
 'semantic_isolation':'NOT_ESTABLISHED','native_render':'UNVERIFIED','admitted':False})
assert len(candidate)==300 and len(reviews)==291 and len(preserved_previous)==9
dest=OUT/'candidate-sources'/source;cbytes=b''.join(candidate);write(dest,cbytes)
emit(OUT/'eval-candidate-source-bindings.json',{'source_path':source,'source_raw_sha256':sha(original),'source_bytes':len(original),
 'parent_candidate_path':str(parent_path.relative_to(ROOT)).replace('\\','/'),'parent_raw_sha256':sha(parent),
 'path':str(dest.relative_to(ROOT)).replace('\\','/'),'raw_sha256':sha(cbytes),'bytes':len(cbytes),'records':300,
 'reviewed_records':291,'changed_lines':changed,'previous_9_preserved':preserved_previous})
write(OUT/'eval-corrections.jsonl',b''.join(canon(x)+b'\n' for x in sorted(patches,key=lambda x:x['id'])))
write(OUT/'independent-eval-review-291.jsonl',b''.join(canon(x)+b'\n' for x in sorted(reviews,key=lambda x:x['id'])))
md=['# 评测稿独立复核与修订','',f'范围：291条新提交，修订{len(patches)}条（正文、必要条件或场景文字）。完整评测文件300条中，前轮9条修订逐字节保留。原件及父版本均冻结归档。','',
'数学与场景文字合格仅指本候选版本；训练评测结构隔离仍未完成，实际渲染未验证，未自动准入。','']
for p in sorted(patches,key=lambda x:x['id']):
 r=p['corrected_record'];md+=['## '+p['id'],'',p['reason'],'','题目：'+r['problem'],'','过程：'+r['solution'],'','答案：'+r['answer'],'','修订后：数学内容及场景文字合格。','']
write(OUT/'EVAL_CORRECTIONS.md',('\n'.join(md)+'\n').encode())
print(json.dumps({'reviewed':291,'repaired':len(patches),'full_candidate':300,'prior_preserved':9},indent=2))
