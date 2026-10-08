# 测试稿独立复核与修订

范围：新138条，修订28条；完整150条继承旧12条修订。数学及场景文字判定绑定当前候选版本，未通过结构隔离和实际渲染前不准入。

## test-calc-006

答案补n与展开适用域，并证明展开与端点

题目：求 $f(x)=\ln(1+x)$ 的麦克劳林展开式，并归纳 $f^{(n)}(0)$ 的规律。

过程：逐阶求导：$f'(x)=(1+x)^{-1}$，$f''(x)=-(1+x)^{-2}$，$f'''(x)=2(1+x)^{-3}$，$f^{(4)}(x)=-6(1+x)^{-4}$。归纳得 $f^{(n)}(x)=(-1)^{n-1}(n-1)!\,(1+x)^{-n}$（$n\ge 1$），故 $f^{(n)}(0)=(-1)^{n-1}(n-1)!$。麦克劳林展开：$\ln(1+x)=\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}x^n}{n}$（$|x|<1$）。展开的依据：在$|x|<1$内，几何级数$1/(1+t)=\sum_{k=0}^{\infty}(-t)^k$在从$0$到$x$的紧区间上一致收敛，逐项积分即得上述展开。$x=1$时有限几何式积分的余项绝对值不超过$1/(N+1)$，故也收敛到$\ln2$；$x=-1$时为负调和级数，发散，且原对数不定义；$|x|>1$时级数通项不趋于0。因此实展开的完整区间为$(-1,1]$。

答案：$\ln(1+x)=\sum_{n=1}^{\infty}(-1)^{n-1}x^n/n$（$-1<x\le1$）；$f^{(n)}(0)=(-1)^{n-1}(n-1)!$（整数$n\ge1$）。

修订后：数学内容与场景文字合格。

## test-calc-007

场景两次洛必达与正文一次洛必达加导数定义不一致

题目：设 $f$ 二阶可导且 $f(0)=f'(0)=0$，求 $\displaystyle\lim_{x\to 0}\frac{f(x)}{x^2}$。

过程：由 $f(0)=0$ 与 $f'(0)=0$，$\dfrac{f(x)}{x^2}$ 为 $\dfrac{0}{0}$ 型。洛必达一次：$\lim_{x\to 0}\dfrac{f'(x)}{2x}$。不假设 $f''$ 连续，直接由二阶导数定义（$f'(0)=0$）：$\lim_{x\to 0}\dfrac{f'(x)}{2x}=\dfrac{1}{2}\lim_{x\to 0}\dfrac{f'(x)-f'(0)}{x}=\dfrac{f''(0)}{2}$。

答案：$\dfrac{f''(0)}{2}$

修订后：数学内容与场景文字合格。

## test-calc-015

不以积分数值观察作为精确答案的依据

题目：利用幂级数展开求 $\displaystyle\int_0^1\frac{\ln(1+x)}{x}\,dx$ 的精确值。

过程：$\ln(1+x)=\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}x^n}{n}$，除以 $x$ 得 $\dfrac{\ln(1+x)}{x}=\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}x^{n-1}}{n}$（$x\ne 0$），且该级数在 $[0,1]$ 上一致收敛：余项 $\left|\displaystyle\sum_{k>N}\dfrac{(-1)^{k-1}x^{k-1}}{k}\right|\le\dfrac{x^N}{N+1}\le\dfrac{1}{N+1}\to 0$（交错级数估计，对 $x\in[0,1]$ 一致）；被积函数在 $x=0$ 处连续延拓为 $1$（$\lim_{x\to 0}\dfrac{\ln(1+x)}{x}=1$）。故可逐项积分：$\displaystyle\int_0^1\dfrac{\ln(1+x)}{x}dx=\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}}{n}\int_0^1x^{n-1}dx=\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}}{n^2}$。由交错级数与 $\zeta(2)$ 的关系：$\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}}{n^2}=\eta(2)=\left(1-2^{1-2}\right)\zeta(2)=\dfrac{1}{2}\cdot\dfrac{\pi^2}{6}=\dfrac{\pi^2}{12}$（其中 $\zeta(2)=\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{n^2}=\dfrac{\pi^2}{6}$ 为已知结果，可由 test-calc-023 的 Parseval 等式得到）。

答案：$\dfrac{\pi^2}{12}$

修订后：数学内容与场景文字合格。

## test-calc-017

补唯一全局最小和无最大值的完整结论

题目：求 $f(x,y)=x^2+y^2-xy+x+y$ 的极值点与极值。

过程：驻点条件：$f_x=2x-y+1=0$，$f_y=2y-x+1=0$。两式相加得 $x+y+2=0$；两式相减得 $3x-3y=0$，即 $x=y$。代入 $x+y+2=0$：$2x=-2$，$x=y=-1$。驻点 $(-1,-1)$。Hessian $H=\begin{pmatrix}2&-1\\-1&2\end{pmatrix}$，顺序主子式 $2>0$、$\det H=3>0$，正定，故 $(-1,-1)$ 为极小值点。$f(-1,-1)=1+1-1-1-1=-1$。更直接令$u=x+1,\ v=y+1$，则$f=-1+u^2+v^2-uv=-1+\frac12[(u-v)^2+u^2+v^2]$。故$f\ge-1$，等号仅在$u=v=0$，是唯一全局最小；因只有一个驻点且该点为严格最小，不存在局部极大，且沿$y=-1,x\to\infty$无上界。

答案：唯一极小点$(-1,-1)$，极小值也是全局最小值$-1$；无极大值。

修订后：数学内容与场景文字合格。

## test-calc-023

傅里叶级数在周期端点收敛到0，不等于端点给定的±π

题目：设$f(x)=x$（$-\pi<x<\pi$）并作$2\pi$周期延拓，其傅里叶正弦系数为$b_n=2(-1)^{n+1}/n$；在开区间内级数收敛到$x$，在周期接缝$x=\pm\pi$收敛到左右极限平均值$0$。利用$L^2$意义下的Parseval等式求$\sum_{n=1}^{\infty}1/n^2$。

过程：Parseval 等式：$\dfrac{1}{\pi}\displaystyle\int_{-\pi}^{\pi}f(x)^2dx=\sum_{n=1}^{\infty}b_n^2$（奇函数情形，$a_n=0$），其中 $b_n=\dfrac{2(-1)^{n+1}}{n}$。左端 $\dfrac{1}{\pi}\displaystyle\int_{-\pi}^{\pi}x^2dx=\dfrac{1}{\pi}\cdot\dfrac{2\pi^3}{3}=\dfrac{2\pi^2}{3}$。右端 $\displaystyle\sum_{n=1}^{\infty}\dfrac{4}{n^2}=4\sum_{n=1}^{\infty}\dfrac{1}{n^2}$。故 $4\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{n^2}=\dfrac{2\pi^2}{3}$，$\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{n^2}=\dfrac{\pi^2}{6}$。端点取值不影响$L^2$积分与傅里叶系数；上述Parseval论证不需要级数在接缝处等于$\pm\pi$。

答案：$\dfrac{\pi^2}{6}$

修订后：数学内容与场景文字合格。

## test-calc-031

落地速度与速率分开表述

题目：物体从高度 $20$ 米处自由下落，高度函数 $h(t)=20-5t^2$（米，$t$ 为秒）。求速度与加速度函数，及物体落地时刻与落地速度。

过程：$v(t)=h'(t)=-10t$（米/秒），$a(t)=v'(t)=-10$（米/秒²，向下）。落地：$h(t)=0$，即 $20-5t^2=0$，$t=2$（秒，舍负根）。落地速度 $v(2)=-20$（米/秒，向下，大小为 $20$）。

答案：$v(t)=-10t$米/秒，$a(t)=-10$米/秒$^2$；$t=2$秒落地，落地速度$-20$米/秒（向下），速率$20$米/秒。

修订后：数学内容与场景文字合格。

## test-calc-035

不能将1/0写成普通除法，直接给比值判别论证

题目：求幂级数 $\displaystyle\sum_{n=0}^{\infty}\frac{x^n}{n!}$ 与 $\displaystyle\sum_{n=0}^{\infty}n!\,x^n$ 的收敛半径，并对比说明。

过程：对$\sum_{n=0}^{\infty}x^n/n!$，当$x\ne0$时相邻项绝对值比为$|x|/(n+1)\to0$，故每个实数或复数$x$都绝对收敛，收敛半径$+\infty$。对$\sum_{n=0}^{\infty}n!x^n$，任意$x\ne0$时相邻项绝对值比为$(n+1)|x|\to\infty$，通项绝对值最终至少以公比2增长，不趋于0，故发散；$x=0$时只有常数项1，收敛，收敛半径0。

答案：$R=+\infty$ 与 $R=0$

修订后：数学内容与场景文字合格。

## test-calc-042

第二证法的积分极限补明确余项上界

题目：证明 $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^{n-1}}{n}=\ln 2$。

过程：由 test-calc-006，$\ln(1+x)=\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}x^n}{n}$ 对 $|x|<1$ 成立。$x=1$ 处级数 $\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}}{n}$ 为交错级数（$a_n=\dfrac{1}{n}\searrow 0$），由莱布尼茨判别法收敛。由 Abel 定理，幂级数的和函数在收敛点左连续，故 $\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}}{n}=\lim_{x\to 1^-}\ln(1+x)=\ln 2$。另一证法（积分表示）：$\dfrac{1}{n}=\displaystyle\int_0^1x^{n-1}dx$，故 $\displaystyle\sum_{n=1}^{N}\dfrac{(-1)^{n-1}}{n}=\int_0^1\sum_{n=1}^{N}(-x)^{n-1}dx=\int_0^1\dfrac{1-(-x)^N}{1+x}dx\to\int_0^1\dfrac{dx}{1+x}=\ln 2$。第二证法的极限由精确界保证：$\left|\int_0^1\frac{(-x)^N}{1+x}dx\right|\le\int_0^1x^Ndx=1/(N+1)\to0$。

答案：证毕（两种证法）

修订后：数学内容与场景文字合格。

## test-calc-043

将有限区域夹逼写全，避免未证可积时的形式平方

题目：求 $\displaystyle\int_0^{+\infty}e^{-x^2}\,dx$（高斯积分）。

过程：令$I_R=\int_0^R e^{-x^2}dx$。有限矩形上的Fubini定理给$I_R^2=\iint_{[0,R]^2}e^{-(x^2+y^2)}dxdy$。第一象限半径$R$的四分之一圆包含于此正方形，而正方形包含于半径$\sqrt2R$的四分之一圆。正被积函数积分保持包含序。极坐标计算半径$r$的四分之一圆积分为$J_r=\int_0^{\pi/2}\int_0^r e^{-u^2}u\,du\,d\theta=\frac{\pi}{4}(1-e^{-r^2})$。因此$\frac{\pi}{4}(1-e^{-R^2})\le I_R^2\le\frac{\pi}{4}(1-e^{-2R^2})$。$I_R>0$单调有上界，且两端趋于$\pi/4$，故$\int_0^\infty e^{-x^2}dx=\sqrt\pi/2$。

答案：$\dfrac{\sqrt\pi}{2}$

修订后：数学内容与场景文字合格。

## test-geom-016

场景TeX的det命令多了一个反斜杠

题目：线性变换 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 把单位圆 $x^2+y^2=1$ 变成什么曲线？并求其面积。

过程：$A$ 把 $(x,y)$ 映到 $(x',y')=(x+y,y)$。反解 $x=x'-y'$、$y=y'$。代入 $x^2+y^2=1$：$(x'-y')^2+y'^2=1$，即 $x'^2-2x'y'+2y'^2=1$。这是椭圆（二次型 $x'^2-2x'y'+2y'^2$ 正定，因矩阵 $\begin{pmatrix}1&-1\\-1&2\end{pmatrix}$ 顺序主子式 $1>0$、$1>0$）。面积：$\det A=1$，故椭圆面积 $=\pi\cdot|\det A|=\pi$。

答案：椭圆 $x^2-2xy+2y^2=1$，面积 $\pi$

修订后：数学内容与场景文字合格。

## test-geom-017

曲率不是对全部实x单调，改为关于绝对值的单调性

题目：求抛物线 $y=x^2$ 在顶点处的曲率与曲率半径，并说明顶点处曲率最大的原因。

过程：$\kappa(x)=\dfrac{|y''|}{(1+y'^2)^{3/2}}=\dfrac{2}{(1+4x^2)^{3/2}}$。在顶点 $x=0$：$\kappa=2$，曲率半径 $R=\dfrac{1}{2}$。$\kappa(x)$ 在 $x=0$ 处最大（分母在 $x=0$ 最小），因顶点处曲线"弯得最急"。

答案：$\kappa=2$；$R=\dfrac{1}{2}$

修订后：数学内容与场景文字合格。

## test-geom-022

明确空间旋转矩阵采用右手正角约定

题目：写出绕 $y$ 轴旋转角 $\varphi$ 的旋转矩阵 $R_y(\varphi)$，并验证它是正交矩阵。取右手直角坐标系，正角遵循绕正$y$轴的右手定则。

过程：绕 $y$ 轴旋转：$x'=x\cos\varphi+z\sin\varphi$，$y'=y$，$z'=-x\sin\varphi+z\cos\varphi$，故 $R_y(\varphi)=\begin{pmatrix}\cos\varphi&0&\sin\varphi\\0&1&0\\-\sin\varphi&0&\cos\varphi\end{pmatrix}$。验证 $R^TR=I$：第一列与第二列点积 $0$、与第三列点积 $\cos\varphi\sin\varphi-\sin\varphi\cos\varphi=0$；各列模长 $\cos^2\varphi+\sin^2\varphi=1$、$1$、$1$。故 $R$ 正交，且 $\det R=1$（旋转保定向）。

答案：$R_y(\varphi)=\begin{pmatrix}\cos\varphi&0&\sin\varphi\\0&1&0\\-\sin\varphi&0&\cos\varphi\end{pmatrix}$；正交（证毕）

修订后：数学内容与场景文字合格。

## test-linalg-009

明确所求是到指定直线的正交投影

题目：求$\mathbb R^2$中到$\operatorname{span}\{(1,1)^T\}$的正交投影矩阵，并求$(3,1)^T$的正交投影。

过程：单位方向 $\hat u=\dfrac{1}{\sqrt2}(1,1)^T$。投影矩阵 $P=\hat u\hat u^T=\dfrac{1}{2}\begin{pmatrix}1&1\\1&1\end{pmatrix}=\begin{pmatrix}\frac{1}{2}&\frac{1}{2}\\\frac{1}{2}&\frac{1}{2}\end{pmatrix}$。$P\begin{pmatrix}3\\1\end{pmatrix}=\begin{pmatrix}\frac{1}{2}&\frac{1}{2}\\\frac{1}{2}&\frac{1}{2}\end{pmatrix}\begin{pmatrix}3\\1\end{pmatrix}=\begin{pmatrix}2\\2\end{pmatrix}$。验证 $P^2=P$（幂等）且 $(3,1)^T-(2,2)^T=(1,-1)^T\perp(1,1)^T$。

答案：$P=\begin{pmatrix}\frac{1}{2}&\frac{1}{2}\\\frac{1}{2}&\frac{1}{2}\end{pmatrix}$；投影为 $(2,2)^T$

修订后：数学内容与场景文字合格。

## test-linalg-011

补法方程解是唯一全局最小的验证

题目：用最小二乘法拟合数据点 $(1,2),(2,4),(3,7)$ 的直线 $y=ax+b$。

过程：$A=\begin{pmatrix}1&1\\2&1\\3&1\end{pmatrix}$，$\vec b=(2,4,7)^T$。法方程 $A^TA\vec x=A^T\vec b$：$A^TA=\begin{pmatrix}14&6\\6&3\end{pmatrix}$，$A^T\vec b=\begin{pmatrix}31\\13\end{pmatrix}$。解 $\begin{cases}14a+6b=31\\6a+3b=13\end{cases}$：由第二式 $2a+b=\dfrac{13}{3}$，$b=\dfrac{13}{3}-2a$。代入第一式：$14a+6\left(\dfrac{13}{3}-2a\right)=31$，即 $14a+26-12a=31$，$2a=5$，$a=\dfrac{5}{2}$，$b=\dfrac{13}{3}-5=-\dfrac{2}{3}$。拟合直线 $y=\dfrac{5}{2}x-\dfrac{2}{3}$。验证：$x=1,2,3$ 时预测值 $\dfrac{11}{6},\dfrac{13}{3},\dfrac{41}{6}$，残差平方和 $\left(\dfrac{1}{6}\right)^2+\left(-\dfrac{1}{3}\right)^2+\left(\dfrac{1}{6}\right)^2=\dfrac{1}{6}$。设求得系数向量$c_*=(5/2,-2/3)^T$，残差$r=b-Ac_*=(1/6,-1/3,1/6)^T$，满足$A^Tr=0$。任意$c=c_*+\delta$有$\|b-Ac\|^2=\|r\|^2+\|A\delta\|^2\ge1/6$。$A$列满秩（$\det(A^TA)=6>0$），故等号仅当$\delta=0$，证明拟合唯一最优。

答案：$y=\dfrac{5}{2}x-\dfrac{2}{3}$

修订后：数学内容与场景文字合格。

## test-linalg-013

周期不能仅从六项观察，写出严格递推恒等式

题目：求 $n$ 阶三对角行列式 $D_n=\begin{vmatrix}1&1&0&\cdots&0\\1&1&1&\cdots&0\\0&1&1&\cdots&0\\\vdots&&&\ddots&\vdots\\0&0&\cdots&1&1\end{vmatrix}$ 的前 6 项，并发现其周期规律（矩阵元素满足 $a_{ii}=a_{i,i+1}=a_{i+1,i}=1$，其余为 0）。

过程：按第一行展开：$D_n=D_{n-1}-D_{n-2}$（第二项的符号来自展开：$1\cdot D_{n-1}-1\cdot\begin{vmatrix}1&1&0&\cdots\\0&1&1&\cdots\\\vdots\end{vmatrix}$，该子式按第一列展开为 $D_{n-2}$）。$D_1=1$，$D_2=\begin{vmatrix}1&1\\1&1\end{vmatrix}=0$。递推：$D_3=D_2-D_1=-1$，$D_4=D_3-D_2=-1$，$D_5=D_4-D_3=0$，$D_6=D_5-D_4=1$。序列 $1,0,-1,-1,0,1$ 以周期 6 循环（$D_n=D_{n-6}$，因 $D_{n+6}=D_{n+5}-D_{n+4}=\cdots=D_n$ 由递推的线性性质）。严格周期证明：由$D_{n+2}=D_{n+1}-D_n$，得到$D_{n+3}=D_{n+2}-D_{n+1}=-D_n$，再得$D_{n+6}=-D_{n+3}=D_n$。前六个相邻有序对$(1,0),(0,-1),(-1,-1),(-1,0),(0,1),(1,1)$互不相同，所以最小正周期确为6。

答案：$D_1,\dots,D_6=1,0,-1,-1,0,1$，周期为 6

修订后：数学内容与场景文字合格。

## test-linalg-021

反射轴覆盖全部过原点方向，不只斜轴

题目：设 $A=\begin{pmatrix}\cos\theta&\sin\theta\\\sin\theta&-\cos\theta\end{pmatrix}$。证明 $A$ 是正交矩阵，求其特征值，并说明其几何意义。

过程：$A^TA=\begin{pmatrix}\cos\theta&\sin\theta\\\sin\theta&-\cos\theta\end{pmatrix}\begin{pmatrix}\cos\theta&\sin\theta\\\sin\theta&-\cos\theta\end{pmatrix}=\begin{pmatrix}\cos^2\theta+\sin^2\theta&\cos\theta\sin\theta-\sin\theta\cos\theta\\\sin\theta\cos\theta-\cos\theta\sin\theta&\sin^2\theta+\cos^2\theta\end{pmatrix}=I$，故 $A$ 正交，且 $\det A=-\cos^2\theta-\sin^2\theta=-1$。特征方程 $\lambda^2-1=0$（迹为 0），特征值 $\pm 1$。特征值 $1$ 的特征方向为 $\left(\cos\dfrac{\theta}{2},\sin\dfrac{\theta}{2}\right)$（关于此方向的直线反射），$-1$ 的特征方向与之垂直。几何上 $A$ 是关于过原点、方向为 $\left(\cos\dfrac{\theta}{2},\sin\dfrac{\theta}{2}\right)$ 的直线的镜面反射；该参数化覆盖所有轴方向，包括 $\theta=(2k+1)\pi$ 时的竖直轴 $x=0$（此时 $\tan\dfrac{\theta}{2}$ 不存在，不能用斜截式表示）。

答案：证毕；特征值 $\pm 1$；关于过原点、方向 $\left(\cos\dfrac{\theta}{2},\sin\dfrac{\theta}{2}\right)$ 的直线的反射（$\theta=(2k+1)\pi$ 时为竖直轴 $x=0$）

修订后：数学内容与场景文字合格。

## test-linalg-026

配方法的合同替换是斜坐标，不等于正交主轴旋转

题目：将二次型 $f=3x^2+4xy+6y^2$ 用配方法化为标准形，并写出相应的可逆线性替换。

过程：$f=3\left(x^2+\dfrac{4}{3}xy\right)+6y^2=3\left(x+\dfrac{2}{3}y\right)^2-\dfrac{4}{3}y^2+6y^2=3\left(x+\dfrac{2}{3}y\right)^2+\dfrac{14}{3}y^2$。令 $u=x+\dfrac{2}{3}y$、$v=y$（可逆：$x=u-\dfrac{2}{3}v$、$y=v$），标准形为 $3u^2+\dfrac{14}{3}v^2$。矩阵形式：$A=\begin{pmatrix}3&2\\2&6\end{pmatrix}$，$C=\begin{pmatrix}1&-\frac{2}{3}\\0&1\end{pmatrix}$，验证 $C^TAC=\begin{pmatrix}3&0\\0&\frac{14}{3}\end{pmatrix}$（$AC=\begin{pmatrix}3&0\\2&\frac{14}{3}\end{pmatrix}$，$C^T(AC)=\begin{pmatrix}3&0\\0&\frac{14}{3}\end{pmatrix}$）。

答案：标准形 $3u^2+\dfrac{14}{3}v^2$；替换 $\begin{cases}u=x+\frac{2}{3}y\\v=y\end{cases}$

修订后：数学内容与场景文字合格。

## test-linalg-036

倍乘操作只有一行，不能说三类均涉及两不同行

题目：求三类初等矩阵的行列式：交换两不同行；将单行乘以$k$（$k\ne0$）；将一行加到另一不同行。

过程：交换两行的初等矩阵 $P_{ij}$：由单位矩阵交换两行得到，$\det P_{ij}=-1$（一次对换改变符号）。第 $i$ 行乘 $k$ 的初等矩阵 $D_i(k)$：对角线第 $i$ 元为 $k$，$\det D_i(k)=k$。第 $i$ 行加到第 $j$ 行的初等矩阵 $E_{ij}$：下（上）三角且对角线全 1，$\det E_{ij}=1$。相应地对任意方阵 $B$：$\det(P_{ij}B)=-\det B$，$\det(D_i(k)B)=k\det B$，$\det(E_{ij}B)=\det B$。

答案：$-1$；$k$；$1$

修订后：数学内容与场景文字合格。

## test-prob-014

期望递推先证明有限性并说明独立重复

题目：独立重复掷一枚均匀骰子，直到首次出现6为止。求所需投掷次数的期望。

过程：设 $E$ 为期望次数。第一次若为 6（概率 $\dfrac{1}{6}$），总次数 1；否则（概率 $\dfrac{5}{6}$）回到初始状态，总次数 $1+E$。故 $E=\dfrac{1}{6}\cdot 1+\dfrac{5}{6}\cdot(1+E)=1+\dfrac{5E}{6}$，解得 $E=6$。（几何分布 $p=\dfrac{1}{6}$ 的期望 $\dfrac{1}{p}=6$。）有限性也可直接由尾和给出：$P(T>k)=(5/6)^k$，因此$E[T]=\sum_{k=0}^\infty P(T>k)=\sum_{k=0}^\infty(5/6)^k=6<\infty$，所以递推式移项合法。

答案：$6$

修订后：数学内容与场景文字合格。

## test-prob-015

同一时刻及硬币公平性需明确概率模型

题目：甲乙每个回合同步各抛一枚公平硬币；所有抛掷相互独立，两人各自遇到首次正面即停止。求他们在同一个回合停止的概率。

过程：设两人停止时刻为 $X,Y$，独立同分布于 $\operatorname{Geom}\!\left(\dfrac{1}{2}\right)$，$P(X=k)=P(Y=k)=\left(\dfrac{1}{2}\right)^k$。$P(X=Y)=\displaystyle\sum_{k=1}^{\infty}P(X=k)P(Y=k)=\sum_{k=1}^{\infty}\left(\dfrac{1}{2}\right)^{2k}=\sum_{k=1}^{\infty}\left(\dfrac{1}{4}\right)^k=\dfrac{1/4}{1-1/4}=\dfrac{1}{3}$。

答案：$\dfrac{1}{3}$

修订后：数学内容与场景文字合格。

## test-prob-018

答案补参数范围和发散分支

题目：设 $X\sim\operatorname{Exp}(\lambda)$。求 $E[e^{tX}]$ 的收敛条件与表达式。其中$\lambda>0,\ t\in\mathbb R$。

过程：$M(t)=E[e^{tX}]=\displaystyle\int_0^{\infty}e^{tx}\lambda e^{-\lambda x}dx=\lambda\int_0^{\infty}e^{(t-\lambda)x}dx$。当 $t<\lambda$ 时收敛：$M(t)=\lambda\cdot\dfrac{1}{\lambda-t}=\dfrac{\lambda}{\lambda-t}$；当 $t\ge\lambda$ 时积分发散（$t=\lambda$ 时 $\int\lambda\,dx$ 发散）。收敛条件 $t<\lambda$ 恰对应"指数增长阶小于衰减率"。

答案：$E[e^{tX}]=\lambda/(\lambda-t)$（$t<\lambda$）；$t\ge\lambda$时为$+\infty$。

修订后：数学内容与场景文字合格。

## test-prob-022

均匀边缘分布不能代替两骰独立条件

题目：独立掷两枚均匀骰子，设$X$为两数之和。求$\operatorname{Var}(X)$。

过程：设 $X=X_1+X_2$，$X_1,X_2$ 独立同分布（单次骰子），$\operatorname{Var}(X_i)=\dfrac{35}{12}$（eval-prob-015）。由独立性 $\operatorname{Var}(X)=\operatorname{Var}(X_1)+\operatorname{Var}(X_2)=\dfrac{35}{12}+\dfrac{35}{12}=\dfrac{35}{6}$。直接验证：$E[X]=7$，$E[X^2]=\displaystyle\sum_{k=2}^{12}k^2P(X=k)=\dfrac{1974}{36}=\dfrac{329}{6}$，$\operatorname{Var}(X)=\dfrac{329}{6}-49=\dfrac{329-294}{6}=\dfrac{35}{6}$，一致。

答案：$\dfrac{35}{6}$

修订后：数学内容与场景文字合格。

## test-prob-023

投针分布及正长度假设应在题干明确，而非推导中默加

题目：布丰投针：平行线间距$d>0$，针长$0<l\le d$。针中点到最近平行线的距离$X$在$[0,d/2]$均匀，针与平行线的无向锐夹角$\Theta$在$[0,\pi/2]$均匀，且两者独立。求针与任一直线相交的概率。

过程：设针中点到最近平行线的距离为 $x\sim U\!\left(0,\dfrac{d}{2}\right)$，针与平行线的夹角为 $\theta\sim U\!\left(0,\dfrac{\pi}{2}\right)$，两者独立。相交条件：$x\le\dfrac{l}{2}\sin\theta$。联合密度 $f(x,\theta)=\dfrac{2}{d}\cdot\dfrac{2}{\pi}$。相交概率 $P=\dfrac{4}{\pi d}\displaystyle\int_0^{\pi/2}\!\!\int_0^{(l/2)\sin\theta}dx\,d\theta=\dfrac{4}{\pi d}\int_0^{\pi/2}\dfrac{l}{2}\sin\theta\,d\theta=\dfrac{2l}{\pi d}\left[-\cos\theta\right]_0^{\pi/2}=\dfrac{2l}{\pi d}$。

答案：$\dfrac{2l}{\pi d}$

修订后：数学内容与场景文字合格。

## test-prob-025

最多两次和第二次不追加机会需明确，以匹配49/12

题目：掷一枚均匀骰子得$X$分；若第一次得6分，则再独立掷一次并累加点数，第二次无论得几分都停止；否则第一次后停止。最多掷两次。求总得分期望。

过程：设总得分为 $Y$。第一次掷出 $X$；若 $X=6$ 则加第二次的 $Z$（与 $X$ 独立同分布）。$E[Y]=E[X]+E[\mathbf 1_{\{X=6\}}Z]=E[X]+P(X=6)E[Z]=\dfrac{7}{2}+\dfrac{1}{6}\cdot\dfrac{7}{2}=\dfrac{7}{2}\left(1+\dfrac{1}{6}\right)=\dfrac{7}{2}\cdot\dfrac{7}{6}=\dfrac{49}{12}$。

答案：$\dfrac{49}{12}$

修订后：数学内容与场景文字合格。

## test-x-003

矩阵级数逐项求导补紧区间一致收敛的依据

题目：设 $A$ 为常矩阵。证明 $\dfrac{d}{dt}e^{tA}=Ae^{tA}$。

过程：$e^{tA}=\displaystyle\sum_{k=0}^{\infty}\dfrac{t^kA^k}{k!}$（对任意 $t$ 收敛）。逐项求导：$\dfrac{d}{dt}e^{tA}=\displaystyle\sum_{k=1}^{\infty}\dfrac{kt^{k-1}A^k}{k!}=\sum_{k=1}^{\infty}\dfrac{t^{k-1}A^k}{(k-1)!}=A\sum_{m=0}^{\infty}\dfrac{t^mA^m}{m!}=Ae^{tA}$（$A$ 为常数矩阵，可提出求和号外）。故 $\dfrac{d}{dt}e^{tA}=Ae^{tA}$，即矩阵指数是矩阵微分方程 $X'=AX$、$X(0)=I$ 的解。严格依据：任取$R>0$和次乘性矩阵范数，在$|t|\le R$上，原项范数不超过$R^k\|A\|^k/k!$，导数项范数不超过$R^{k-1}\|A\|^k/(k-1)!$（$k\ge1$）。两个数值级数分别求和为$e^{R\|A\|}$和$\|A\|e^{R\|A\|}$，均有限。由Weierstrass判别法及逐项求导定理，运算在任意紧区间有效，故对所有实$t$成立。

答案：证毕

修订后：数学内容与场景文字合格。

## test-x-009

阶乘矩的n明确为非负整数

题目：设 $X\sim\operatorname{Exp}(1)$。证明 $E[X^n]=n!$。其中$n\in\mathbb Z_{\ge0}$。

过程：设 $n\in\{0,1,2,\dots\}$。$E[X^n]=\displaystyle\int_0^{\infty}x^ne^{-x}dx$。记 $I_n=\displaystyle\int_0^{\infty}x^ne^{-x}dx$。$I_0=\displaystyle\int_0^{\infty}e^{-x}dx=1$ 单独计算；$n\ge 1$ 时用分部积分（$u=x^n$、$dv=e^{-x}dx$）：$I_n=\left[-x^ne^{-x}\right]_0^{\infty}+n\displaystyle\int_0^{\infty}x^{n-1}e^{-x}dx=nI_{n-1}$（$n\ge 1$ 时边界项 $x^ne^{-x}\big|_0^\infty$ 为 0）。递推得 $I_n=n!$，即 $E[X^n]=n!$（恰为 Γ 函数 $\Gamma(n+1)$）。

答案：证毕；$E[X^n]=n!$

修订后：数学内容与场景文字合格。

## test-x-010

相关系数绝对值1对应中心化线性相关，原变量为仿射关系

题目：设两随机变量的方差有限且严格为正（$\sigma_1,\sigma_2>0$）。证明协方差矩阵 $\begin{pmatrix}\sigma_1^2&\rho\sigma_1\sigma_2\\\rho\sigma_1\sigma_2&\sigma_2^2\end{pmatrix}$ 正定当且仅当 $|\rho|<1$。

过程：顺序主子式：$\sigma_1^2>0$；行列式 $\sigma_1^2\sigma_2^2(1-\rho^2)$。矩阵正定 $\iff$ 两顺序主子式均为正 $\iff 1-\rho^2>0\iff|\rho|<1$。概率解释：相关系数 $|\rho|<1$ 恰是中心化变量$X-E[X]$与$Y-E[Y]$不几乎必然线性相关（即不存在非平凡常数$a,b$使$aX+bY$几乎必然为常数）的充要条件，此时协方差矩阵非退化；若某个方差为 0，协方差矩阵必奇异，且相关系数未定义。

答案：证毕（在 $\sigma_1,\sigma_2>0$ 的前提下，正定 $\iff|\rho|<1$）

修订后：数学内容与场景文字合格。

## test-x-013

删除所有约数估算，写出取整容斥及误差界

题目：随机取一个正整数（在 $1$ 到 $N$ 中等可能，$N\to\infty$ 取极限），求它能被 2 或 3 整除的概率。

过程：在$\{1,\ldots,N\}$均匀选取整数。能被2、3、6整除的个数分别恰为$\lfloor N/2\rfloor,\lfloor N/3\rfloor,\lfloor N/6\rfloor$，故所求概率$p_N=[\lfloor N/2\rfloor+\lfloor N/3\rfloor-\lfloor N/6\rfloor]/N$。因$|\lfloor u\rfloor-u|<1$，有$|p_N-(1/2+1/3-1/6)|<3/N\to0$。所以极限自然密度为$2/3$；这不是在所有正整数上定义等概率分布。

答案：$\dfrac{2}{3}$

修订后：数学内容与场景文字合格。

