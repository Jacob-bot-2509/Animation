# 30 道核心范围数学正文修订

输入严格绑定冻结包的 761 条现役/入选记录；修订 30 条，保留其余 731 条的全部字段。
本稿是待准入的正文修订覆盖层。原始包、现役绑定和其他字段保持原样；场景、渲染与隔离复验另需绑定修改后的版本。
未宣称全部 761 条数学正确，也未据格式检查认定同核心隔离通过。

## calc-series-015

旧版精确数学修订仍未进入现役；本轮重新绑定原记录并核对证明。

**题目**：讨论级数 $\sum_{n=1}^{\infty} \frac{(-1)^n}{\sqrt{n}}$ 的敛散性，并指出是绝对收敛还是条件收敛。

**过程**：设 $u_n=1/\sqrt n$，则 $u_{n+1}\le u_n$ 且 $\lim_{n\to\infty}u_n=0$。由莱布尼茨判别法，$\sum_{n=1}^{\infty}(-1)^n u_n$ 收敛。若和为 $S$、前 $N$ 项和为 $S_N$，则 $|S-S_N|\le 1/\sqrt{N+1}$。绝对值级数满足 $\sum_{n=1}^{N}1/\sqrt n\ge\int_1^{N+1}x^{-1/2}\,dx=2(\sqrt{N+1}-1)\to+\infty$，即 $p=\frac{1}{2}\le1$ 的 $p$ 级数发散。因此原级数条件收敛。

**答案**：条件收敛

## calc-series-020

旧版精确数学修订仍未进入现役；本轮重新绑定原记录并核对证明。

**题目**：将函数 $f(x) = x$（$-\pi \le x \le \pi$）展开为傅立叶级数。

**过程**：$f(x)=x$ 为奇函数，故 $a_0=a_n=0$。分部积分得 $b_n=\frac{2}{\pi}\int_0^\pi x\sin(nx)\,dx=\frac{2}{\pi}[-\frac{x\cos(nx)}{n}+\frac{\sin(nx)}{n^2}]_0^\pi=\frac{2(-1)^{n+1}}{n}$。令 $S(x)=2\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n}\sin(nx)$。由傅里叶收敛定理，对 $-\pi<x<\pi$ 有 $S(x)=x$；在 $x=\pm\pi$，周期延拓的左右极限为 $\pi$ 与 $-\pi$，级数收敛到其中值 $0$，并不等于题中端点所指定的 $\pm\pi$。事实上每个有限部分和在这两个端点也恰为 $0$。

**答案**：$S(x)=2\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n}\sin(nx)$；$-\pi<x<\pi$ 时 $S(x)=x$，$x=\pm\pi$ 时 $S(x)=0$。

## linalg-050

旧版精确数学修订仍未进入现役；本轮重新绑定原记录并核对证明。

**题目**：利用几何图形解释二阶行列式 $\begin{vmatrix} a & b \\ c & d \end{vmatrix} = ad - bc$ 的几何意义。

**过程**：令 $A=\begin{pmatrix}a&b\\c&d\end{pmatrix}$，其两列为 $u=(a,c)^T$、$v=(b,d)^T$。单位正方形顶点按次序映为 $0,u,u+v,v$，所得平行四边形的有向面积为 $\det(u,v)=ad-bc$，通常面积为 $|ad-bc|$。$\det A>0$ 时保持定向，$\det A<0$ 时反转定向。若 $\det A=0$，则 $\operatorname{rank}A\le1$：秩为 $1$ 时整个平面的像为直线、单位正方形的像为线段；秩为 $0$ 时 $A=0$，两者的像均为一个点。两种退化情形的面积均为 $0$。

**答案**：有向面积为 $ad-bc$，通常面积为 $|ad-bc|$；行列式为零时像可退化为线段或点。

## linalg-070

旧版精确数学修订仍未进入现役；本轮重新绑定原记录并核对证明。

**题目**：在 $\mathbb{R}^2$ 上定义辛形式 $\omega(u,v)=u_1v_2-u_2v_1$（标准行列式形式），说明辛变换保持该形式不变的意义。

**过程**：设 $J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}$，则 $\omega(u,v)=u^TJv=\det(u,v)$，表示有向面积。对 $A=\begin{pmatrix}a&b\\c&d\end{pmatrix}$，有 $A^TJA=\begin{pmatrix}0&ad-bc\\bc-ad&0\end{pmatrix}=(\det A)J$，因此 $\omega(Au,Av)=(\det A)\omega(u,v)$。二维中，$A$ 是辛变换当且仅当 $\det A=1$；它同时保持有向面积、通常面积与定向。仅保持通常面积还不足以判定为辛变换：反射 $R=\operatorname{diag}(1,-1)$ 的行列式为 $-1$，它使 $\omega(Ru,Rv)=-\omega(u,v)$。

**答案**：辛变换保持有向面积与定向：$\omega(Au,Av)=\omega(u,v)$；二维中等价于 $\det A=1$。

## prob-038

旧版精确数学修订仍未进入现役；本轮重新绑定原记录并核对证明。

**题目**：已知 $P(A)=\frac{3}{5}$，$P(B)=\frac{2}{5}$，且 $P(A\cap B)=\frac{1}{5}$。求 $P(A\mid B)$ 和 $P(B\mid A)$。

**过程**：由条件概率定义，$P(A\mid B)=\frac{P(A\cap B)}{P(B)}=\frac{1/5}{2/5}=\frac{1}{5}\cdot\frac{5}{2}=\frac{1}{2}$；$P(B\mid A)=\frac{P(A\cap B)}{P(A)}=\frac{1/5}{3/5}=\frac{1}{5}\cdot\frac{5}{3}=\frac{1}{3}$。两条件事件的概率均为正，定义适用。

**答案**：$P(A\mid B)=\frac{1}{2}$，$P(B\mid A)=\frac{1}{3}$。

## prob-039

旧版精确数学修订仍未进入现役；本轮重新绑定原记录并核对证明。

**题目**：独立均匀地在正方形 $Q=[-1,1]^2$ 中选取 $n\ge1$ 个点，记落入单位圆 $D=\{(x,y):x^2+y^2\le1\}$ 的点数为 $m_n$。构造 $\widehat\pi_n=4m_n/n$，精确求其期望和方差，并证明 $\widehat\pi_n\xrightarrow{P}\pi$。说明有限样本的有理数 $4m_n/n$ 与符号常量 $\pi$ 的区别。

**过程**：令 $Q=[-1,1]^2$，$D=\{(x,y):x^2+y^2\le1\}$，独立均匀地在 $Q$ 中抽取 $n\ge1$ 个点。记 $I_i$ 为第 $i$ 点落入 $D$ 的指示变量，$m_n=\sum_{i=1}^n I_i$，则 $P(I_i=1)=\frac{\pi}{4}$。定义估计量 $\widehat\pi_n=\frac{4m_n}{n}$，这是给定计数后的精确有理数，不是有限样本下与 $\pi$ 的恒等式。$E(\widehat\pi_n)=\pi$，$\operatorname{Var}(\widehat\pi_n)=\frac{\pi(4-\pi)}{n}$。对任意 $\varepsilon>0$，切比雪夫不等式给出 $P(|\widehat\pi_n-\pi|\ge\varepsilon)\le\frac{\pi(4-\pi)}{n\varepsilon^2}\to0$，故 $\widehat\pi_n\xrightarrow{P}\pi$；强大数定律还给出几乎处处收敛。

**答案**：$\widehat\pi_n=\frac{4m_n}{n}$，$E(\widehat\pi_n)=\pi$，$\operatorname{Var}(\widehat\pi_n)=\frac{\pi(4-\pi)}{n}$，且 $\widehat\pi_n\xrightarrow{P}\pi$。

## prob-042

旧版精确数学修订仍未进入现役；本轮重新绑定原记录并核对证明。

**题目**：设 $X_1,X_2,\ldots$ 独立同分布，$P(X_i=1)=p$、$P(X_i=0)=1-p$，其中 $0\le p\le1$。令正面频率 $F_n=n^{-1}\sum_{i=1}^nX_i$。精确求 $E(F_n)$、$\operatorname{Var}(F_n)$，并用切比雪夫不等式证明 $F_n\xrightarrow{P}p$；说明公平硬币附加条件对应的 $p$。

**过程**：设各次投掷独立同分布，$X_i\sim\operatorname{Bernoulli}(p)$，其中 $p=P(X_i=1)$，$0\le p\le1$；题目未指定公平性，不能直接令 $p=\frac{1}{2}$。正面频率为 $F_n=\frac{1}{n}\sum_{i=1}^n X_i$。由独立性，$E(F_n)=p$，$\operatorname{Var}(F_n)=p(1-p)/n$。对任意 $\varepsilon>0$，$P(|F_n-p|\ge\varepsilon)\le\frac{p(1-p)}{n\varepsilon^2}\to0$，故 $F_n\xrightarrow{P}p$。若另有公平硬币条件，才取 $p=\frac{1}{2}$。

**答案**：$E(F_n)=p$，$\operatorname{Var}(F_n)=\frac{p(1-p)}n$，$F_n\xrightarrow{P}p$；公平硬币附加条件为 $p=\frac12$。

## prob-043

旧版精确数学修订仍未进入现役；本轮重新绑定原记录并核对证明。

**题目**：设 $X_1,X_2,\ldots$ 独立同分布，$E(X_i)=\mu$、$0<\operatorname{Var}(X_i)=\sigma^2<\infty$，$\overline X_n=n^{-1}\sum_{i=1}^nX_i$。写出标准化均值的中心极限定理，并区分其分布极限与原尺度 $\overline X_n$ 的极限；说明总体正态时有限样本的精确分布。

**过程**：设 $X_1,X_2,\ldots$ 独立同分布，$E(X_i)=\mu$、$0<\operatorname{Var}(X_i)=\sigma^2<\infty$，$\overline X_n=\frac{1}{n}\sum_{i=1}^n X_i$。中心极限定理的精确结论为 $Z_n=\frac{\sqrt n(\overline X_n-\mu)}{\sigma}\xrightarrow{d}N(0,1)$，即对每个 $t\in\mathbb R$，$\lim_{n\to\infty}P(Z_n\le t)=\Phi(t)$。未经标准化的均值有 $E(\overline X_n)=\mu$、$\operatorname{Var}(\overline X_n)=\sigma^2/n$，且 $\overline X_n\xrightarrow{P}\mu$，其极限分布为点质量 $\delta_\mu$，不能称为趋向固定的非退化正态分布。只有总体本身正态时，有限 $n$ 下才精确有 $\overline X_n\sim N(\mu,\sigma^2/n)$。

**答案**：$\frac{\sqrt n(\overline X_n-\mu)}\sigma\xrightarrow{d}N(0,1)$；$\overline X_n\xrightarrow{P}\mu$，极限分布为 $\delta_\mu$；总体为 $N(\mu,\sigma^2)$ 时，有限样本精确有 $\overline X_n\sim N(\mu,\sigma^2/n)$。

## prob-046

旧版精确数学修订仍未进入现役；本轮重新绑定原记录并核对证明。

**题目**：用几何图形直观展示可列可加性：把单位正方形分割成可列个互不相交的小矩形。

**过程**：取半开单位正方形 $\Omega=[0,1)\times[0,1)$，面积为 $1$。令 $R_k=[1-2^{-(k-1)},1-2^{-k})\times[0,1)$，$k\ge1$。这些矩形两两不交，且 $\bigcup_{k=1}^{\infty}R_k=\Omega$，$\operatorname{area}(R_k)=2^{-k}$。前 $N$ 个矩形的面积和为 $S_N=\sum_{k=1}^{N}2^{-k}=1-2^{-N}$，剩余面积为 $2^{-N}\to0$，所以由面积测度的可列可加性，$\operatorname{area}(\Omega)=\sum_{k=1}^{\infty}\operatorname{area}(R_k)=1$。若画闭单位正方形，只多出零面积边界，不改变面积等式。该例展示可列可加性，不能把单个图例当作对所有可测集合的一般证明。

**答案**：本图例中 $R_k$ 两两不交，$\bigcup_{k=1}^\infty R_k=[0,1)^2$，且 $\sum_{k=1}^\infty\operatorname{area}(R_k)=\sum_{k=1}^\infty2^{-k}=1$。

## eval-calc-015-s3

删除数值积分估算，补齐对称换元的精确证明。

**题目**：求定积分 $\displaystyle I=\int_0^\pi\frac{x\sin x}{1+\cos^2 x}\,dx$。

**过程**：设 $g(x)=\sin x/(1+\cos^2x)$。对 $0\le x\le\pi$，有 $g(\pi-x)=g(x)$。作代换 $x=\pi-t$ 得 $I=\int_0^\pi(\pi-t)g(t)\,dt$，与原式相加得 $2I=\pi\int_0^\pi g(x)\,dx$。再令 $u=\cos x$，则 $\int_0^\pi g(x)\,dx=\int_{-1}^1(1+u^2)^{-1}\,du=\arctan1-\arctan(-1)=\pi/2$。故 $I=\pi^2/4$。

**答案**：$\frac{\pi^2}{4}$

## eval-calc-026-s3

固定步长近似替换为合法的极限定义计算。

**题目**：设 $z=x^y$（$x>0$），求 $z$ 在点 $(1,2)$ 处的两个偏导数。

**过程**：按偏导数定义，$z_x(1,2)=\lim_{h\to0}\frac{(1+h)^2-1}{h}=\lim_{h\to0}(2+h)=2$，其中 $h\ne0$ 且充分小时 $1+h>0$。另一方面，$z_y(1,2)=\lim_{h\to0}\frac{1^{2+h}-1}{h}=\lim_{h\to0}0=0$。两个结果均由极限定义精确得到。

**答案**：$z_x(1,2)=2$，$z_y(1,2)=0$。

## eval-calc-027-s3

删除黎曼和估算和不必要的非初等原函数论断，改用换序积分。

**题目**：求二重积分 $\displaystyle I=\int_0^1\!\!\int_x^1 e^{y^2}\,dy\,dx$。

**过程**：积分区域为 $D=\{(x,y):0\le x\le y\le1\}$。被积函数连续，故可交换积分次序：$I=\int_0^1\int_0^y e^{y^2}\,dx\,dy=\int_0^1 y e^{y^2}\,dy$。令 $u=y^2$，得到 $I=\frac12\int_0^1e^u\,du=\frac{e-1}{2}$。

**答案**：$\frac{e-1}{2}$

## eval-prob-007-s1

保留补事件计数，删除概率小数。

**题目**：房间里随机聚集 30 个人（假设生日在一年 365 天中等可能且相互独立）。求至少有两人生日相同的概率。

**过程**：记 $A$ 为至少两人生日相同。共有 $365^{30}$ 个等可能的有序生日序列；互不相同的序列共有 $365\cdot364\cdots336=365!/335!$ 个。因此 $P(A^c)=\frac{365!}{335!\,365^{30}}$，从而 $P(A)=1-\frac{365!}{335!\,365^{30}}$。

**答案**：$1-\frac{365!}{335!\,365^{30}}$

## eval-prob-007-s2

递推各项保持有理数，不以近似阈值代替所求概率。

**题目**：房间里随机聚集 30 个人（假设生日在一年 365 天中等可能且相互独立）。求至少有两人生日相同的概率。

**过程**：令 $q_k$ 为前 $k$ 人生日互不相同的概率。$q_1=1$；在前 $k-1$ 人生日互异的条件下，第 $k$ 人须避开 $k-1$ 天，故 $q_k=q_{k-1}\frac{366-k}{365}$。递推得 $q_{30}=\prod_{k=2}^{30}\frac{366-k}{365}=\frac{365!}{335!\,365^{30}}$，所求概率为 $1-q_{30}$。

**答案**：$1-\frac{365!}{335!\,365^{30}}$

## eval-prob-007-s3

纠正仅凭期望大于1就断言事件概率较大的推理，给出精确下界及精确概率。

**题目**：房间里随机聚集 30 个人（假设生日在一年 365 天中等可能且相互独立）。求至少有两人生日相同的概率。

**过程**：设 $N=\sum_{1\le i<j\le30}I_{ij}$，其中 $I_{ij}$ 表示第 $i,j$ 人生日相同。共有 $\binom{30}{2}=435$ 对，故 $E(N)=435/365=87/73$。不同的两对指标即使共用一人，也有联合概率 $1/365^2$；所以 $E(N^2)=435/365+435\cdot434/365^2$。由柯西不等式，$E(N)^2=E(N\mathbf1_{\{N>0\}})^2\le E(N^2)P(N>0)$，得 $P(N>0)\ge435/799>1/2$。这个下界不等于精确概率；精确值仍由补事件计数得到 $P(N>0)=1-\frac{365!}{335!\,365^{30}}$。

**答案**：$1-\frac{365!}{335!\,365^{30}}$

## eval-prob-008-s1

补足题目要求的精确值比较，删除小数概率。

**题目**：设 $X\sim B\!\left(100,\dfrac{1}{2}\right)$。用切比雪夫不等式给出 $P(|X-50|\ge 10)$ 的上界，并与精确值比较。

**过程**：$E(X)=50$，$\operatorname{Var}(X)=100\cdot\frac12\cdot\frac12=25$。切比雪夫不等式给出 $q=P(|X-50|\ge10)\le25/10^2=1/4$。由于 $X$ 为整数且分布关于 $50$ 对称，$q=P(X\le40)+P(X\ge60)=2^{-99}\sum_{k=0}^{40}\binom{100}{k}$。令 $Y=(X-50)^2$。在该事件上 $Y\ge100$，且 $P(X=0)>0$ 时 $Y>100$，故 $25=E(Y)>100q$，即 $q<1/4$。这说明上界严格大于精确值。

**答案**：上界 $\frac14$；精确值 $q=2^{-99}\sum_{k=0}^{40}\binom{100}{k}<\frac14$。

## eval-prob-008-s2

补齐切比雪夫上界与精确求和的比较。

**题目**：设 $X\sim B\!\left(100,\dfrac{1}{2}\right)$。用切比雪夫不等式给出 $P(|X-50|\ge 10)$ 的上界，并与精确值比较。

**过程**：将二项分布各项求和，利用 $\binom{100}{k}=\binom{100}{100-k}$，精确得到 $q=P(X\le40)+P(X\ge60)=\frac{2}{2^{100}}\sum_{k=0}^{40}\binom{100}{k}$。另一方面 $E(X)=50$，$\operatorname{Var}(X)=25$，故切比雪夫上界为 $1/4$。设 $S=\sum_{k=0}^{40}\binom{100}{k}$，则两者之差为 $\frac14-q=\frac{2^{97}-S}{2^{99}}$。由于 $E((X-50)^2)>100P(|X-50|\ge10)$（例如 $X=0$ 的正概率项给出严格性），该差严格为正。

**答案**：上界 $\frac14$；精确值 $\frac{1}{2^{99}}\sum_{k=0}^{40}\binom{100}{k}$，严格小于 $\frac14$。

## eval-prob-008-s3

估算差值改为精确整数求和差，并证明严格性。

**题目**：设 $X\sim B\!\left(100,\dfrac{1}{2}\right)$。用切比雪夫不等式给出 $P(|X-50|\ge 10)$ 的上界，并与精确值比较。

**过程**：记 $A=\{|X-50|\ge10\}$。由 $E((X-50)^2)=25$，有 $P(A)\le1/4$。精确概率为 $q=2^{-99}\sum_{k=0}^{40}\binom{100}{k}$。更细地，$25-100q=E(((X-50)^2-100)\mathbf1_A)+E((X-50)^2\mathbf1_{A^c})>0$；两项非负，第一项中 $X=0$ 的贡献严格为正。于是 $q<1/4$，且精确差值为 $\frac14-q=\frac{2^{97}-\sum_{k=0}^{40}\binom{100}{k}}{2^{99}}>0$。

**答案**：上界 $\frac14$；精确值 $q=2^{-99}\sum_{k=0}^{40}\binom{100}{k}$；差 $\frac14-q=\frac{2^{97}-\sum_{k=0}^{40}\binom{100}{k}}{2^{99}}>0$。

## test-calc-027

用对数积分不等式与指数级数的严格不等式替代小数比较。

**题目**：证明方程 $e^x=2x+1$ 恰有两个实根，并给出两个根所在的区间。

**过程**：令 $f(x)=e^x-2x-1$，则 $f'(x)=e^x-2$。所以 $f$ 在 $(-\infty,\ln2)$ 严格递减，在 $(\ln2,+\infty)$ 严格递增。$f(0)=0$，且 $\ln2=\int_1^2t^{-1}\,dt>1/2$，故 $f(\ln2)=1-2\ln2<0$。由指数级数的正项可知 $e^2>1+2+2=5$，因而 $f(2)>0$。又有 $0<\ln2<1$，连续性与严格单调性说明递减区间唯一零点为 $0$，递增区间唯一零点 $\xi$ 位于 $(\ln2,2)$。故恰有两个实根。

**答案**：恰有两个实根：$0$ 与 $\xi\in(\ln2,2)$。

## test-prob-001

百分数与中间小数统一改为精确分数。

**题目**：两车间各承担总产量的 $\frac35$ 与 $\frac25$，次品率分别为 $\frac1{50}$ 与 $\frac3{100}$。随机抽取一件产品发现是次品，求它来自第一车间的概率。

**过程**：设 $A_i$ 表示产品来自第 $i$ 车间，$D$ 表示次品。$P(A_1\cap D)=\frac35\cdot\frac1{50}=\frac3{250}$，$P(A_2\cap D)=\frac25\cdot\frac3{100}=\frac3{250}$，故 $P(D)=\frac3{125}>0$。由贝叶斯公式，$P(A_1\mid D)=\frac{3/250}{3/125}=\frac12$。

**答案**：$\frac12$

## test-prob-002

精确二项概率改用既约分数，中间运算不取小数。

**题目**：设 $X\sim B\!\left(10,\dfrac{3}{10}\right)$。求 $P(X=3)$ 与 $P(X\le 1)$ 的精确值。

**过程**：由二项分布公式，$P(X=3)=\binom{10}{3}\left(\frac3{10}\right)^3\left(\frac7{10}\right)^7=\frac{120\cdot3^3\cdot7^7}{10^{10}}=\frac{66706983}{250000000}$。又 $P(X\le1)=P(X=0)+P(X=1)=\left(\frac7{10}\right)^{10}+10\cdot\frac3{10}\left(\frac7{10}\right)^9=\frac{7^{10}+30\cdot7^9}{10^{10}}=\frac{1493083459}{10000000000}$。

**答案**：$P(X=3)=\frac{66706983}{250000000}$；$P(X\le1)=\frac{1493083459}{10000000000}$。

## test-prob-005

题干阈值、积分上下限和运算统一改为分数。

**题目**：设 $X,Y$ 独立同分布于 $U(0,1)$，求 $Z=X+Y$ 的密度与 $P(Z>\frac32)$。

**过程**：由卷积，$f_Z(z)=\int_{\mathbb R}\mathbf1_{(0,1)}(x)\mathbf1_{(0,1)}(z-x)\,dx$，即两个区间的交集长度。因此 $f_Z(z)=\begin{cases}z,&0<z<1,\\2-z,&1\le z<2,\\0,&\text{其他}.\end{cases}$。所求尾概率为 $P(Z>\frac32)=\int_{3/2}^2(2-z)\,dz=[2z-z^2/2]_{3/2}^2=2-\frac{15}{8}=\frac18$。

**答案**：$f_Z(z)=\begin{cases}z,&0<z<1,\\2-z,&1\le z<2,\\0,&\text{其他}.\end{cases}$；$P(Z>\frac32)=\frac18$。

## test-prob-007

指数中的有限小数改为分数，保持精确指数常量。

**题目**：某灯泡寿命 $T\sim\operatorname{Exp}\!\left(\dfrac{1}{1000}\right)$（单位：小时，参数 $\lambda=\dfrac{1}{1000}$）。求 $P(T>1500\mid T>500)$。

**过程**：指数分布的生存函数为 $P(T>t)=e^{-t/1000}$（$t\ge0$）。由于 $\{T>1500\}\subseteq\{T>500\}$，$P(T>1500\mid T>500)=\frac{e^{-1500/1000}}{e^{-500/1000}}=\frac{e^{-3/2}}{e^{-1/2}}=e^{-1}$。

**答案**：$e^{-1}$

## test-prob-008

补明独立条件，均值、阈值、方差和上界全部精确表示。

**题目**：独立投掷均匀骰子 $n$ 次，设 $\bar X_n$ 为平均点数。用切比雪夫不等式给出 $P(|\bar X_n-\frac72|\ge\frac1{10})$ 的上界，并说明 $n\to\infty$ 时该概率趋于 $0$。

**过程**：每次点数 $X_i$ 在 $1,\ldots,6$ 上等可能，故 $E(X_i)=\frac16\sum_{k=1}^6k=\frac72$，$E(X_i^2)=\frac16\sum_{k=1}^6k^2=\frac{91}{6}$，$\operatorname{Var}(X_i)=\frac{91}{6}-\frac{49}{4}=\frac{35}{12}$。独立性给出 $E(\bar X_n)=\frac72$，$\operatorname{Var}(\bar X_n)=\frac{35}{12n}$。因此 $P(|\bar X_n-\frac72|\ge\frac1{10})\le\min\{1,\frac{35}{12n}\cdot100\}=\min\{1,\frac{875}{3n}\}$。该非负上界趋于 $0$，由夹逼定理所求概率也趋于 $0$。

**答案**：上界 $\min\{1,\frac{875}{3n}\}$；当 $n\to\infty$ 时概率趋于 $0$。

## test-prob-016

转移矩阵及稳态方程中的小数全部替换为分数。

**题目**：某地天气的转移矩阵为 $P=\begin{pmatrix}\frac45&\frac15\\\frac25&\frac35\end{pmatrix}$（状态 $1$ 晴、状态 $2$ 雨，行表示今天）。求稳态分布。

**过程**：令 $\pi=(a,b)$，其中 $a+b=1$ 且 $a,b\ge0$。由 $\pi P=\pi$ 得 $a=\frac45a+\frac25b$，即 $a=2b$。联立归一化条件，得到 $a=\frac23$、$b=\frac13$。代回可核验 $(\frac23,\frac13)P=(\frac23,\frac13)$。

**答案**：$\pi=(\frac23,\frac13)$。

## test-prob-020

明确随机次序的必要条件，删除期望的小数改写。

**题目**：口袋里有 $10$ 把钥匙，其中只有 $1$ 把能开门，以均匀随机顺序逐一不放回尝试。求打开门所需尝试次数的期望。

**过程**：正确钥匙在均匀随机排列中的位置 $K$ 等可能为 $1,\ldots,10$，即 $P(K=k)=1/10$。因此 $E(K)=\frac1{10}\sum_{k=1}^{10}k=\frac{10\cdot11}{2\cdot10}=\frac{11}{2}$。

**答案**：$\frac{11}{2}$

## test-prob-021

题干、过程及答案中的小数改为分数。

**题目**：设 $A,B$ 独立，$P(A)=\frac25$，$P(A\cup B)=\frac7{10}$。求 $P(B)$。

**过程**：令 $p=P(B)$。独立性给出 $P(A\cap B)=\frac25p$。由容斥公式，$\frac7{10}=\frac25+p-\frac25p=\frac25+\frac35p$，所以 $\frac35p=\frac3{10}$，得 $p=\frac12$。

**答案**：$\frac12$

## test-linalg-012

黄金比保持根式，增长比用精确比值及极限证明。

**题目**：用矩阵方法求斐波那契数列 $F_1=F_2=1$，$F_{n+2}=F_{n+1}+F_n$ 中 $F_{10}$ 的值，并说明增长比趋于黄金比。

**过程**：补记 $F_0=0$，则 $\binom{F_{n+1}}{F_n}=A^n\binom10$，其中 $A=\begin{pmatrix}1&1\\1&0\end{pmatrix}$。令 $\phi=(1+\sqrt5)/2$、$\psi=(1-\sqrt5)/2$，则 $Q=\begin{pmatrix}\phi&\psi\\1&1\end{pmatrix}$ 满足 $A=Q\operatorname{diag}(\phi,\psi)Q^{-1}$，且 $\det Q=\sqrt5\ne0$。由此得到精确公式 $F_n=(\phi^n-\psi^n)/\sqrt5$。递推或代入公式均得 $F_{10}=55$。令 $r=\psi/\phi$，则 $|r|<1$，并且对 $n\ge1$ 有 $\frac{F_{n+1}}{F_n}=\phi\frac{1-r^{n+1}}{1-r^n}\to\phi=\frac{1+\sqrt5}{2}$。

**答案**：$F_{10}=55$；$\lim_{n\to\infty}\frac{F_{n+1}}{F_n}=\frac{1+\sqrt5}{2}$。

## test-x-004

矩阵数据改为分数，明确转置后列向量才是所述特征向量。

**题目**：转移矩阵为 $P$ 的马尔可夫链，稳态分布 $\pi$ 满足 $\pi=\pi P$。说明稳态分布对应于 $P^T$ 的特征值 $1$ 的特征向量，并求 $P=\begin{pmatrix}\frac12&\frac12\\\frac14&\frac34\end{pmatrix}$ 的稳态分布。

**过程**：将行向量等式 $\pi P=\pi$ 转置，得 $P^T\pi^T=\pi^T$。因 $\pi$ 的分量非负且和为 $1$，$\pi^T\ne0$，所以它是 $P^T$ 对应于特征值 $1$ 的特征向量。对题中矩阵，设 $\pi=(a,b)$，则 $a+b=1$ 且 $a=\frac12a+\frac14b$，于是 $b=2a$，得 $\pi=(\frac13,\frac23)$，代回确实满足稳态方程。

**答案**：$\pi=(\frac13,\frac23)$；$P^T\pi^T=\pi^T$。

## test-x-015

删除矩阵、特征值及中间运算的全部小数。

**题目**：设马尔可夫链的转移矩阵 $P=\begin{pmatrix}\frac12&\frac12\\\frac14&\frac34\end{pmatrix}$。用对角化求 $P^n$（$n$ 为非负整数），并求 $n\to\infty$ 时的极限矩阵。

**过程**：特征多项式为 $\lambda^2-\frac54\lambda+\frac14=(\lambda-1)(\lambda-\frac14)$，对应特征向量可取 $(1,1)^T$、$(2,-1)^T$。令 $Q=\begin{pmatrix}1&2\\1&-1\end{pmatrix}$，则 $Q^{-1}=\begin{pmatrix}\frac13&\frac23\\\frac13&-\frac13\end{pmatrix}$，且 $P=Q\operatorname{diag}(1,\frac14)Q^{-1}$。所以 $P^n=Q\operatorname{diag}(1,4^{-n})Q^{-1}=\frac13\begin{pmatrix}1+2\cdot4^{-n}&2-2\cdot4^{-n}\\1-4^{-n}&2+4^{-n}\end{pmatrix}$。由 $4^{-n}\to0$，得到 $\lim_{n\to\infty}P^n=\begin{pmatrix}\frac13&\frac23\\\frac13&\frac23\end{pmatrix}$。

**答案**：$P^n=\frac13\begin{pmatrix}1+2\cdot4^{-n}&2-2\cdot4^{-n}\\1-4^{-n}&2+4^{-n}\end{pmatrix}$；$\lim_{n\to\infty}P^n=\begin{pmatrix}\frac13&\frac23\\\frac13&\frac23\end{pmatrix}$。

