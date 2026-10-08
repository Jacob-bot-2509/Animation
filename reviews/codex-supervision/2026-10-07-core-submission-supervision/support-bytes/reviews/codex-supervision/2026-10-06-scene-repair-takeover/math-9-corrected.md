# 九题精确数学修订稿

实际新版本，未正式准入；原绑定题库不改写，动画未验收。

## calc-series-015

题目：讨论级数 $\sum_{n=1}^{\infty} \frac{(-1)^n}{\sqrt{n}}$ 的敛散性，并指出是绝对收敛还是条件收敛。

过程：设 $u_n=1/\sqrt n$，则 $u_{n+1}\le u_n$ 且 $\lim_{n\to\infty}u_n=0$。由莱布尼茨判别法，$\sum_{n=1}^{\infty}(-1)^n u_n$ 收敛。若和为 $S$、前 $N$ 项和为 $S_N$，则 $|S-S_N|\le 1/\sqrt{N+1}$。绝对值级数满足 $\sum_{n=1}^{N}1/\sqrt n\ge\int_1^{N+1}x^{-1/2}\,dx=2(\sqrt{N+1}-1)\to+\infty$，即 $p=\frac{1}{2}\le1$ 的 $p$ 级数发散。因此原级数条件收敛。

答案：条件收敛

场景步骤：

1. 第一步：列出 $u_n=1/\sqrt n$，高亮 $u_{n+1}\le u_n$ 与 $u_n\to0$ 两个收敛判别假设。
2. 第二步：展示带符号项与部分和 $S_N$，以莱布尼茨判别法得出存在有限和 $S$。
3. 第三步：标出余项区间 $S_N\pm1/\sqrt{N+1}$，逐步增加 $N$，用精确界解释区间收缩。
4. 第四步：对绝对值项显示 $\sum_{n=1}^{N}1/\sqrt n\ge\int_1^{N+1}x^{-1/2}\,dx=2(\sqrt{N+1}-1)$，高亮该下界趋于 $+\infty$。
5. 第五步：并列“原级数收敛”与“绝对值级数发散”，得出条件收敛。

## calc-series-020

题目：将函数 $f(x) = x$（$-\pi \le x \le \pi$）展开为傅立叶级数。

过程：$f(x)=x$ 为奇函数，故 $a_0=a_n=0$。分部积分得 $b_n=\frac{2}{\pi}\int_0^\pi x\sin(nx)\,dx=\frac{2}{\pi}[-\frac{x\cos(nx)}{n}+\frac{\sin(nx)}{n^2}]_0^\pi=\frac{2(-1)^{n+1}}{n}$。令 $S(x)=2\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n}\sin(nx)$。由傅里叶收敛定理，对 $-\pi<x<\pi$ 有 $S(x)=x$；在 $x=\pm\pi$，周期延拓的左右极限为 $\pi$ 与 $-\pi$，级数收敛到其中值 $0$，并不等于题中端点所指定的 $\pm\pi$。事实上每个有限部分和在这两个端点也恰为 $0$。

答案：$S(x)=2\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n}\sin(nx)$；$-\pi<x<\pi$ 时 $S(x)=x$，$x=\pm\pi$ 时 $S(x)=0$。

场景步骤：

1. 第一步：画出 $-\pi<x<\pi$ 上的直线与周期接缝，标明接缝两侧极限为 $\pi$、$-\pi$。
2. 第二步：高亮奇函数条件，写出 $a_0=a_n=0$；逐步展示 $\int x\sin(nx)\,dx$ 中 $u=x$、$dv=\sin(nx)\,dx$ 与系数 $b_n=2(-1)^{n+1}/n$。
3. 第三步：依次叠加 $2\sin x$、$-\sin2x$、$\frac{2}{3}\sin3x$，展示 $S_N$ 的精确项式。
4. 第四步：区分区间内部 $S(x)=x$ 与端点 $S(\pm\pi)=0$，注明 $\sin(n\pi)=0$ 导致所有有限部分和端点值也为 $0$。
5. 第五步：高亮跳跃点附近的吉布斯振荡，并明确振荡峰位于附近，不能把 $x=\pi$ 处画成非零峰值。

## linalg-050

题目：利用几何图形解释二阶行列式 $\begin{vmatrix} a & b \\ c & d \end{vmatrix} = ad - bc$ 的几何意义。

过程：令 $A=\begin{pmatrix}a&b\\c&d\end{pmatrix}$，其两列为 $u=(a,c)^T$、$v=(b,d)^T$。单位正方形顶点按次序映为 $0,u,u+v,v$，所得平行四边形的有向面积为 $\det(u,v)=ad-bc$，通常面积为 $|ad-bc|$。$\det A>0$ 时保持定向，$\det A<0$ 时反转定向。若 $\det A=0$，则 $\operatorname{rank}A\le1$：秩为 $1$ 时整个平面的像为直线、单位正方形的像为线段；秩为 $0$ 时 $A=0$，两者的像均为一个点。两种退化情形的面积均为 $0$。

答案：有向面积为 $ad-bc$，通常面积为 $|ad-bc|$；行列式为零时像可退化为线段或点。

场景步骤：

1. 第一步：显示 $T(x,y)=(ax+by,cx+dy)$，标出第一行 $(a,b)$ 与列向量 $(x,y)^T$ 的点乘、第二行 $(c,d)$ 与同一列的点乘。
2. 第二步：对基向量分别计算 $Ae_1=u$、$Ae_2=v$，按 $0,u,u+v,v$ 展示单位正方形的像。
3. 第三步：展示有向面积 $\det(u,v)=ad-bc$，分别高亮乘积 $ad$、$bc$ 与相减；通常面积取绝对值。
4. 第四步：分别说明正、负行列式的定向，并用箭头顺序区分有向面积与非负面积。
5. 第五步：分两种退化显示：秩 $1$ 的像为线段；$A=0$、秩 $0$ 的像为点；二者面积均为 $0$。

## linalg-070

题目：在 $\mathbb{R}^2$ 上定义辛形式 $\omega(u,v)=u_1v_2-u_2v_1$（标准行列式形式），说明辛变换保持该形式不变的意义。

过程：设 $J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}$，则 $\omega(u,v)=u^TJv=\det(u,v)$，表示有向面积。对 $A=\begin{pmatrix}a&b\\c&d\end{pmatrix}$，有 $A^TJA=\begin{pmatrix}0&ad-bc\\bc-ad&0\end{pmatrix}=(\det A)J$，因此 $\omega(Au,Av)=(\det A)\omega(u,v)$。二维中，$A$ 是辛变换当且仅当 $\det A=1$；它同时保持有向面积、通常面积与定向。仅保持通常面积还不足以判定为辛变换：反射 $R=\operatorname{diag}(1,-1)$ 的行列式为 $-1$，它使 $\omega(Ru,Rv)=-\omega(u,v)$。

答案：辛变换保持有向面积与定向：$\omega(Au,Av)=\omega(u,v)$；二维中等价于 $\det A=1$。

场景步骤：

1. 第一步：标注 $\omega(u,v)=u_1v_2-u_2v_1$ 是有向面积，通常面积为 $|\omega(u,v)|$。
2. 第二步：逐行逐列计算 $JA=\begin{pmatrix}c&d\\-a&-b\end{pmatrix}$，标明每个元素的行与列对应关系。
3. 第三步：对 $A^T(JA)$ 的四个元素分别标出行乘列：$ac-ca=0$、$ad-cb$、$bc-da$、$bd-db=0$，得到 $(\det A)J$。
4. 第四步：在 $\det A=1$ 条件下展示变换后箭头顺序与面积均保持，并列出 $\omega(Au,Av)=\omega(u,v)$。
5. 第五步：展示反射 $R$ 作为对照：通常面积不变，但有向面积变号，故它不是辛变换。

## prob-038

题目：已知 $P(A)=\frac{3}{5}$，$P(B)=\frac{2}{5}$，且 $P(A\cap B)=\frac{1}{5}$。求 $P(A\mid B)$ 和 $P(B\mid A)$。

过程：由条件概率定义，$P(A\mid B)=\frac{P(A\cap B)}{P(B)}=\frac{1/5}{2/5}=\frac{1}{5}\cdot\frac{5}{2}=\frac{1}{2}$；$P(B\mid A)=\frac{P(A\cap B)}{P(A)}=\frac{1/5}{3/5}=\frac{1}{5}\cdot\frac{5}{3}=\frac{1}{3}$。两条件事件的概率均为正，定义适用。

答案：$P(A\mid B)=\frac{1}{2}$，$P(B\mid A)=\frac{1}{3}$。

场景步骤：

1. 第一步：画出单位样本空间，并按精确横坐标 $0,\frac{2}{5},\frac{3}{5},\frac{4}{5},1$ 划分矩形，标注 $P(A)=\frac{3}{5}$、$P(B)=\frac{2}{5}$、$P(A\cap B)=\frac{1}{5}$。
2. 第二步：高亮交集矩形，说明面积为 $\frac{3}{5}-\frac{2}{5}=\frac{1}{5}$。
3. 第三步：将 $B$ 外部置灰，列出 $\frac{1/5}{2/5}=\frac{1}{5}\cdot\frac{5}{2}=\frac{1}{2}$，逐项标明分子、分母及约分。
4. 第四步：将 $A$ 外部置灰，列出 $\frac{1/5}{3/5}=\frac{1}{5}\cdot\frac{5}{3}=\frac{1}{3}$。
5. 第五步：并列两个条件概率，注明分母均大于零。

## prob-039

题目：独立均匀地在正方形 $Q=[-1,1]^2$ 中选取 $n\ge1$ 个点，记落入单位圆 $D=\{(x,y):x^2+y^2\le1\}$ 的点数为 $m_n$。构造 $\widehat\pi_n=4m_n/n$，精确求其期望和方差，并证明 $\widehat\pi_n\xrightarrow{P}\pi$。说明有限样本的有理数 $4m_n/n$ 与符号常量 $\pi$ 的区别。

过程：令 $Q=[-1,1]^2$，$D=\{(x,y):x^2+y^2\le1\}$，独立均匀地在 $Q$ 中抽取 $n\ge1$ 个点。记 $I_i$ 为第 $i$ 点落入 $D$ 的指示变量，$m_n=\sum_{i=1}^n I_i$，则 $P(I_i=1)=\frac{\pi}{4}$。定义估计量 $\widehat\pi_n=\frac{4m_n}{n}$，这是给定计数后的精确有理数，不是有限样本下与 $\pi$ 的恒等式。$E(\widehat\pi_n)=\pi$，$\operatorname{Var}(\widehat\pi_n)=\frac{\pi(4-\pi)}{n}$。对任意 $\varepsilon>0$，切比雪夫不等式给出 $P(|\widehat\pi_n-\pi|\ge\varepsilon)\le\frac{\pi(4-\pi)}{n\varepsilon^2}\to0$，故 $\widehat\pi_n\xrightarrow{P}\pi$；强大数定律还给出几乎处处收敛。

答案：$\widehat\pi_n=\frac{4m_n}{n}$，$E(\widehat\pi_n)=\pi$，$\operatorname{Var}(\widehat\pi_n)=\frac{\pi(4-\pi)}{n}$，且 $\widehat\pi_n\xrightarrow{P}\pi$。

场景步骤：

1. 第一步：标出正方形面积 $4$、圆面积 $\pi$，推得命中概率 $\pi/4$。
2. 第二步：独立均匀投点，分别统计总点数 $n$ 与圆内点数 $m_n$，把每次估计值保留为精确分数 $4m_n/n$。
3. 第三步：注明有限样本估计量不是 $\pi$ 的精确值；展示 $E(m_n)=n\pi/4$、$\operatorname{Var}(m_n)=n(\pi/4)(1-\pi/4)$。
4. 第四步：逐步乘以尺度因子 $4/n$，得到 $E(\widehat\pi_n)=\pi$ 与方差 $\pi(4-\pi)/n$。
5. 第五步：高亮切比雪夫概率界 $\pi(4-\pi)/(n\varepsilon^2)\to0$，以该界说明一致性，不用小数圆周率或有限点云冒充证明。

## prob-042

题目：设 $X_1,X_2,\ldots$ 独立同分布，$P(X_i=1)=p$、$P(X_i=0)=1-p$，其中 $0\le p\le1$。令正面频率 $F_n=n^{-1}\sum_{i=1}^nX_i$。精确求 $E(F_n)$、$\operatorname{Var}(F_n)$，并用切比雪夫不等式证明 $F_n\xrightarrow{P}p$；说明公平硬币附加条件对应的 $p$。

过程：设各次投掷独立同分布，$X_i\sim\operatorname{Bernoulli}(p)$，其中 $p=P(X_i=1)$，$0\le p\le1$；题目未指定公平性，不能直接令 $p=\frac{1}{2}$。正面频率为 $F_n=\frac{1}{n}\sum_{i=1}^n X_i$。由独立性，$E(F_n)=p$，$\operatorname{Var}(F_n)=p(1-p)/n$。对任意 $\varepsilon>0$，$P(|F_n-p|\ge\varepsilon)\le\frac{p(1-p)}{n\varepsilon^2}\to0$，故 $F_n\xrightarrow{P}p$。若另有公平硬币条件，才取 $p=\frac{1}{2}$。

答案：$F_n\xrightarrow{P}p$，其中 $p$ 为单次正面概率；公平硬币时 $p=\frac{1}{2}$。

场景步骤：

1. 第一步：明确独立同分布假设，标出 $P(X_i=1)=p$；以 $p$ 为参数而不是预设公平性。
2. 第二步：累计正面次数并用精确分数 $F_n=(X_1+\cdots+X_n)/n$ 更新频率曲线。
3. 第三步：逐步计算 $E(F_n)=p$ 和 $\operatorname{Var}(F_n)=p(1-p)/n$，说明独立性用于方差相加。
4. 第四步：标出偏差带 $p\pm\varepsilon$，高亮切比雪夫不等式与概率界趋零，得出依概率收敛。
5. 第五步：将公平硬币作为附加示例，明确此时 $p=\frac{1}{2}$；单条有限轨迹不能代替收敛证明。

## prob-043

题目：设 $X_1,X_2,\ldots$ 独立同分布，$E(X_i)=\mu$、$0<\operatorname{Var}(X_i)=\sigma^2<\infty$，$\overline X_n=n^{-1}\sum_{i=1}^nX_i$。写出标准化均值的中心极限定理，并区分其分布极限与原尺度 $\overline X_n$ 的极限；说明总体正态时有限样本的精确分布。

过程：设 $X_1,X_2,\ldots$ 独立同分布，$E(X_i)=\mu$、$0<\operatorname{Var}(X_i)=\sigma^2<\infty$，$\overline X_n=\frac{1}{n}\sum_{i=1}^n X_i$。中心极限定理的精确结论为 $Z_n=\frac{\sqrt n(\overline X_n-\mu)}{\sigma}\xrightarrow{d}N(0,1)$，即对每个 $t\in\mathbb R$，$\lim_{n\to\infty}P(Z_n\le t)=\Phi(t)$。未经标准化的均值有 $E(\overline X_n)=\mu$、$\operatorname{Var}(\overline X_n)=\sigma^2/n$，且 $\overline X_n\xrightarrow{P}\mu$，其极限分布为点质量 $\delta_\mu$，不能称为趋向固定的非退化正态分布。只有总体本身正态时，有限 $n$ 下才精确有 $\overline X_n\sim N(\mu,\sigma^2/n)$。

答案：$\frac{\sqrt n(\overline X_n-\mu)}{\sigma}\xrightarrow{d}N(0,1)$；$\operatorname{Var}(\overline X_n)=\sigma^2/n$ 且 $\overline X_n\xrightarrow{P}\mu$。

场景步骤：

1. 第一步：高亮独立同分布、有限正方差两项条件，列出 $E(X_i)=\mu$ 和 $\operatorname{Var}(X_i)=\sigma^2$。
2. 第二步：逐项求均值与方差，得到 $E(\overline X_n)=\mu$、$\operatorname{Var}(\overline X_n)=\sigma^2/n$。
3. 第三步：展示减去 $\mu$ 再除以 $\sigma/\sqrt n$ 的标准化操作，得到 $Z_n$。
4. 第四步：在固定尺度上对照 $Z_n$ 与 $N(0,1)$，展示分布函数极限 $P(Z_n\le t)\to\Phi(t)$；有限 $n$ 的图形不标为完全一致。
5. 第五步：另屏展示原尺度均值集中到 $\mu$，用 $P(|\overline X_n-\mu|\ge\varepsilon)\le\sigma^2/(n\varepsilon^2)$ 区分大数定律与中心极限定理。
6. 第六步：说明总体正态时 $\overline X_n\sim N(\mu,\sigma^2/n)$ 对有限 $n$ 精确成立；一般总体不能用某个固定样本量保证精确正态。

## prob-046

题目：用几何图形直观展示可列可加性：把单位正方形分割成可列个互不相交的小矩形。

过程：取半开单位正方形 $\Omega=[0,1)\times[0,1)$，面积为 $1$。令 $R_k=[1-2^{-(k-1)},1-2^{-k})\times[0,1)$，$k\ge1$。这些矩形两两不交，且 $\bigcup_{k=1}^{\infty}R_k=\Omega$，$\operatorname{area}(R_k)=2^{-k}$。前 $N$ 个矩形的面积和为 $S_N=\sum_{k=1}^{N}2^{-k}=1-2^{-N}$，剩余面积为 $2^{-N}\to0$，所以由面积测度的可列可加性，$\operatorname{area}(\Omega)=\sum_{k=1}^{\infty}\operatorname{area}(R_k)=1$。若画闭单位正方形，只多出零面积边界，不改变面积等式。该例展示可列可加性，不能把单个图例当作对所有可测集合的一般证明。

答案：可列可加性成立：各矩形面积构成几何级数 $\sum_{k=1}^{\infty} \frac{1}{2^k}$，其和为 $1$，恰等于单位正方形的总面积

场景步骤：

1. 第一步：说明边界采用半开约定，保证相邻矩形作为集合不重叠；若画完整边框，标明附加边界面积为零。
2. 第二步：依次划出 $R_1=[0,\frac{1}{2})\times[0,1)$、$R_2=[\frac{1}{2},\frac{3}{4})\times[0,1)$、$R_3=[\frac{3}{4},\frac{7}{8})\times[0,1)$。
3. 第三步：列出一般矩形端点并相减，得到宽度 $2^{-k}$，高度为 $1$，面积为 $2^{-k}$。
4. 第四步：逐项显示几何级数部分和 $S_N=1-2^{-N}$，高亮剩余面积恰为 $2^{-N}$。
5. 第五步：用 $2^{-N}\to0$ 与两两不交、完整覆盖条件得出总面积为 $1$，标注这是可列可加性的具体例子。
