# 新版渲染包 data_v2_train_leakage-isolated-v3-2026-10-05_dataset_prob

来源: reviews/codex-supervision/2026-10-07-math-batch-supervision/candidate-sources/data/v2/train/leakage-isolated-v3-2026-10-05/dataset_prob.jsonl

raw_sha256: 53af8eee14b90b58741267e47bb1276ca5fe28c703b3fb2edc18703e16a7a807


### prob-038

**problem** 已知 $P(A)=\frac{3}{5}$，$P(B)=\frac{2}{5}$，且 $P(A\cap B)=\frac{1}{5}$。求 $P(A\mid B)$ 和 $P(B\mid A)$。

**solution** 由条件概率定义，$P(A\mid B)=\frac{P(A\cap B)}{P(B)}=\frac{1/5}{2/5}=\frac{1}{5}\cdot\frac{5}{2}=\frac{1}{2}$；$P(B\mid A)=\frac{P(A\cap B)}{P(A)}=\frac{1/5}{3/5}=\frac{1}{5}\cdot\frac{5}{3}=\frac{1}{3}$。两条件事件的概率均为正，定义适用。

**answer** $P(A\mid B)=\frac{1}{2}$，$P(B\mid A)=\frac{1}{3}$。

**objects[0]** 单位面积矩形的四个精确分区

**objects[1]** 两个条件样本空间的归一化

**steps[0]** 把 $[0,1)^2$ 沿横轴分成宽为 $2/5,1/5,1/5,1/5$ 的四条带，依次代表 $A\setminus B,A\cap B,B\setminus A,(A\cup B)^c$。

**steps[1]** 四区面积和为 $1$，显示 $P(A)=3/5$、$P(B)=2/5$、$P(A\cap B)=1/5$。

**steps[2]** 按 $B$ 归一化得到 $P(A\mid B)=(1/5)/(2/5)=1/2$；按 $A$ 归一化得到 $P(B\mid A)=(1/5)/(3/5)=1/3$。


### prob-039

**problem** 独立均匀地在正方形 $Q=[-1,1]^2$ 中选取 $n\ge1$ 个点，记落入单位圆 $D=\{(x,y):x^2+y^2\le1\}$ 的点数为 $m_n$。构造 $\widehat\pi_n=4m_n/n$，精确求其期望和方差，并证明 $\widehat\pi_n\xrightarrow{P}\pi$。说明有限样本的有理数 $4m_n/n$ 与符号常量 $\pi$ 的区别。

**solution** 令 $Q=[-1,1]^2$，$D=\{(x,y):x^2+y^2\le1\}$，独立均匀地在 $Q$ 中抽取 $n\ge1$ 个点。记 $I_i$ 为第 $i$ 点落入 $D$ 的指示变量，$m_n=\sum_{i=1}^n I_i$，则 $P(I_i=1)=\frac{\pi}{4}$。定义估计量 $\widehat\pi_n=\frac{4m_n}{n}$，这是给定计数后的精确有理数，不是有限样本下与 $\pi$ 的恒等式。$E(\widehat\pi_n)=\pi$，$\operatorname{Var}(\widehat\pi_n)=\frac{\pi(4-\pi)}{n}$。对任意 $\varepsilon>0$，切比雪夫不等式给出 $P(|\widehat\pi_n-\pi|\ge\varepsilon)\le\frac{\pi(4-\pi)}{n\varepsilon^2}\to0$，故 $\widehat\pi_n\xrightarrow{P}\pi$；强大数定律还给出几乎处处收敛。

**answer** $\widehat\pi_n=\frac{4m_n}{n}$，$E(\widehat\pi_n)=\pi$，$\operatorname{Var}(\widehat\pi_n)=\frac{\pi(4-\pi)}{n}$，且 $\widehat\pi_n\xrightarrow{P}\pi$。

**objects[0]** 边长为二的正方形和单位圆

**objects[1]** 有限样本的精确计数比

**objects[2]** 期望方差与切比雪夫界

**steps[0]** 均匀独立取点于 $[-1,1]^2$，标注单点入圆概率 $p=\pi/4$。

**steps[1]** 显示给定样本的精确有理数 $\widehat\pi_n=4m_n/n$，不将它写成与 $\pi$ 的有限样本恒等式。

**steps[2]** 显示 $E(\widehat\pi_n)=\pi$，$\operatorname{Var}(\widehat\pi_n)=\pi(4-\pi)/n$。

**steps[3]** 对 $\varepsilon>0$ 显示 $P(|\widehat\pi_n-\pi|\ge\varepsilon)\le\pi(4-\pi)/(n\varepsilon^2)\to0$。

**steps[4]** 结论为 $\widehat\pi_n\xrightarrow{P}\pi$；圆周率保持符号 $\pi$，不使用小数逼近。


### prob-040

**problem** 设 $p_n\in[0,1]$，$np_n\to\lambda\in[0,+\infty)$，$X_n\sim B(n,p_n)$。证明对每个固定 $k\in\mathbb Z_{\ge0}$，$P(X_n=k)$ 的极限为参数 $\lambda$ 的泊松概率质量，并给出 $\lambda=0$ 的退化情形。

**solution** 先设 $\lambda>0$。因为 $np_n\to\lambda$，有 $p_n\to0$。对固定 $k\ge0$，当 $n\ge k$ 且充分大时，
$P(X_n=k)=\frac{(np_n)^k}{k!}\prod_{j=0}^{k-1}(1-\frac jn)(1-p_n)^n(1-p_n)^{-k}$，其中 $k=0$ 时空乘积为 $1$。
对 $0\le u<1$，$-\frac{u}{1-u}\le\log(1-u)\le-u$，故
$-\frac{np_n}{1-p_n}\le n\log(1-p_n)\le-np_n$，夹逼得 $n\log(1-p_n)\to-\lambda$，从而 $(1-p_n)^n\to e^{-\lambda}$。其余三个因子分别趋于 $\lambda^k/k!$、$1$、$1$，所以 $P(X_n=k)\to e^{-\lambda}\lambda^k/k!$。
若 $\lambda=0$，由 Markov 不等式 $P(X_n\ge1)\le E X_n=np_n\to0$，故 $P(X_n=0)\to1$，且对 $k\ge1$ 有 $P(X_n=k)\to0$。

**answer** 若 $\lambda>0$，则对每个固定 $k\in\mathbb Z_{\ge0}$，$\displaystyle\lim_{n\to\infty}P(X_n=k)=\frac{e^{-\lambda}\lambda^k}{k!}$；若 $\lambda=0$，则极限为 $k=0$ 时的 $1$ 和 $k\ge1$ 时的 $0$。

**objects[0]** 离散横坐标 $k\in\mathbb Z_{\ge0}$ 和二项概率质量柱

**objects[1]** 泊松质量点 $q_k=e^{-5}5^k/k!$，不绘为连续概率密度

**objects[2]** 受约束参数 $n\in\mathbb Z,\ n\ge5,\ p_n=5/n$

**steps[0]** 取 $n=10$，$p_n=\frac12$，显示二项概率质量的精确公式 $\binom nk(5/n)^k(1-5/n)^{n-k}$。

**steps[1]** 令整数 $n$ 增大，始终保持 $p_n=5/n$；标注 $EX_n=5$ 与 $\operatorname{Var}(X_n)=5-\frac{25}{n}$，$n=10$ 时方差为 $\frac52$。

**steps[2]** 在整数 $k$ 处叠加泊松质量点 $q_k$，若截断显示只标示有限窗口，其外概率仍按分布公式定义。

**steps[3]** 板书固定 $k$ 的严格极限推导；有限柱图仅示意。有限 $n$ 时不声称二项分布与泊松分布相等。


### prob-041

**problem** ? $\mu\in\mathbb R$?$\sigma>0$?$X\sim N(\mu,\sigma^2)$??????????????? $\mu$ ? $\sigma$ ?????????

**solution** 密度为 $f_{\mu,\sigma}(x)=\frac{1}{\sigma\sqrt{2\pi}}\exp(-\frac{(x-\mu)^2}{2\sigma^2})$，其中 $\sigma>0$。
令 $\phi(z)=\frac{1}{\sqrt{2\pi}}e^{-z^2/2}$，则 $f_{\mu,\sigma}(x)=\sigma^{-1}\phi((x-\mu)/\sigma)$：改变 $\mu$ 只平移对称轴 $x=\mu$；增大 $\sigma$ 时横向按比例展宽，峰高 $f_{\mu,\sigma}(\mu)=1/(\sigma\sqrt{2\pi})$ 降低，总积分仍为 $1$。
由 $Z=(X-\mu)/\sigma\sim N(0,1)$，对任意 $c\ge0$，
$P(|X-\mu|\le c\sigma)=\frac{1}{\sqrt{2\pi}}\int_{-c}^{c}e^{-z^2/2}\,dz=\operatorname{erf}(c/\sqrt2)$。
这里 $\operatorname{erf}(u)=\frac2{\sqrt\pi}\int_0^u e^{-t^2}\,dt$，所以 $c=1,2$ 时分别为 $\operatorname{erf}(1/\sqrt2)$、$\operatorname{erf}(\sqrt2)$。

**answer** $\mu$ ????????$\sigma>0$ ????????? $\sigma$ ???????? $\frac1{\sigma\sqrt{2\pi}}$ ???????? $1$?

**objects[0]** 密度 $f_{\mu,\sigma}(x)$，参数 $\mu\in\mathbb R,\ \sigma>0$

**objects[1]** 对称轴 $x=\mu$，峰高标签 $\frac1{\sigma\sqrt{2\pi}}$

**objects[2]** 精确阴影标签 $\operatorname{erf}(1/\sqrt2)$ 和 $\operatorname{erf}(\sqrt2)$

**steps[0]** 初始展示 $N(0,1)$，板书 $\int_{\mathbb R}\phi(z)\,dz=1$。

**steps[1]** 改变 $\mu$ 仅平移曲线；改变 $\sigma$ 时始终限制为正数，显示缩放公式 $f_{\mu,\sigma}(x)=\sigma^{-1}\phi((x-\mu)/\sigma)$。

**steps[2]** 对区间 $[\mu-\sigma,\mu+\sigma]$ 和 $[\mu-2\sigma,\mu+2\sigma]$ 填充阴影，只使用精确概率 $\operatorname{erf}(1/\sqrt2)$ 和 $\operatorname{erf}(\sqrt2)$。

**steps[3]** 展示变量代换 $z=(x-\mu)/\sigma$；面积结论来自精确积分，视觉阴影只作示意。


### prob-042

**problem** 设 $X_1,X_2,\ldots$ 独立同分布，$P(X_i=1)=p$、$P(X_i=0)=1-p$，其中 $0\le p\le1$。令正面频率 $F_n=n^{-1}\sum_{i=1}^nX_i$。精确求 $E(F_n)$、$\operatorname{Var}(F_n)$，并用切比雪夫不等式证明 $F_n\xrightarrow{P}p$；说明公平硬币附加条件对应的 $p$。

**solution** 设各次投掷独立同分布，$X_i\sim\operatorname{Bernoulli}(p)$，其中 $p=P(X_i=1)$，$0\le p\le1$；题目未指定公平性，不能直接令 $p=\frac{1}{2}$。正面频率为 $F_n=\frac{1}{n}\sum_{i=1}^n X_i$。由独立性，$E(F_n)=p$，$\operatorname{Var}(F_n)=p(1-p)/n$。对任意 $\varepsilon>0$，$P(|F_n-p|\ge\varepsilon)\le\frac{p(1-p)}{n\varepsilon^2}\to0$，故 $F_n\xrightarrow{P}p$。若另有公平硬币条件，才取 $p=\frac{1}{2}$。

**answer** $E(F_n)=p$，$\operatorname{Var}(F_n)=\frac{p(1-p)}n$，$F_n\xrightarrow{P}p$；公平硬币附加条件为 $p=\frac12$。

**objects[0]** 一般参数的频率图

**objects[1]** 期望方差标签

**objects[2]** 概率上界

**steps[0]** 标明各次为独立同分布 Bernoulli$(p)$，其中 $0\le p\le1$；水平参考线为 $y=p$。

**steps[1]** 显示 $F_n=n^{-1}\sum_{i=1}^nX_i$、$E(F_n)=p$、$\operatorname{Var}(F_n)=p(1-p)/n$。

**steps[2]** 显示 $P(|F_n-p|\ge\varepsilon)\le\min\{1,p(1-p)/(n\varepsilon^2)\}\to0$。

**steps[3]** 只在附加公平条件时取 $p=1/2$；频率图为示意，结论由上述不等式给出。


### prob-043

**problem** 设 $X_1,X_2,\ldots$ 独立同分布，$E(X_i)=\mu$、$0<\operatorname{Var}(X_i)=\sigma^2<\infty$，$\overline X_n=n^{-1}\sum_{i=1}^nX_i$。写出标准化均值的中心极限定理，并区分其分布极限与原尺度 $\overline X_n$ 的极限；说明总体正态时有限样本的精确分布。

**solution** 设 $X_1,X_2,\ldots$ 独立同分布，$E(X_i)=\mu$、$0<\operatorname{Var}(X_i)=\sigma^2<\infty$，$\overline X_n=\frac{1}{n}\sum_{i=1}^n X_i$。中心极限定理的精确结论为 $Z_n=\frac{\sqrt n(\overline X_n-\mu)}{\sigma}\xrightarrow{d}N(0,1)$，即对每个 $t\in\mathbb R$，$\lim_{n\to\infty}P(Z_n\le t)=\Phi(t)$。未经标准化的均值有 $E(\overline X_n)=\mu$、$\operatorname{Var}(\overline X_n)=\sigma^2/n$，且 $\overline X_n\xrightarrow{P}\mu$，其极限分布为点质量 $\delta_\mu$，不能称为趋向固定的非退化正态分布。只有总体本身正态时，有限 $n$ 下才精确有 $\overline X_n\sim N(\mu,\sigma^2/n)$。

**answer** $\frac{\sqrt n(\overline X_n-\mu)}\sigma\xrightarrow{d}N(0,1)$；$\overline X_n\xrightarrow{P}\mu$，极限分布为 $\delta_\mu$；总体为 $N(\mu,\sigma^2)$ 时，有限样本精确有 $\overline X_n\sim N(\mu,\sigma^2/n)$。

**objects[0]** 标准化均值的分布视图

**objects[1]** 原尺度均值的退化极限视图

**objects[2]** 总体正态时的精确有限样本结论

**steps[0]** 标注独立同分布及 $E(X_i)=\mu$、$0<\operatorname{Var}(X_i)=\sigma^2<\infty$。

**steps[1]** 定义 $Z_n=\sqrt n(\overline X_n-\mu)/\sigma$，显示 $Z_n\xrightarrow{d}N(0,1)$ 和 $P(Z_n\le t)\to\Phi(t)$。

**steps[2]** 原尺度另显示 $\operatorname{Var}(\overline X_n)=\sigma^2/n\to0$、$\overline X_n\xrightarrow{P}\mu$，极限分布为 $\delta_\mu$。

**steps[3]** 只有总体为 $N(\mu,\sigma^2)$ 时，有限样本才精确有 $\overline X_n\sim N(\mu,\sigma^2/n)$。

**steps[4]** 图形仅示意定理结论，不宣称非正态总体在某一固定样本量已有精确正态均值分布。


### prob-046

**problem** 用几何图形直观展示可列可加性：把单位正方形分割成可列个互不相交的小矩形。

**solution** 取半开单位正方形 $\Omega=[0,1)\times[0,1)$，面积为 $1$。令 $R_k=[1-2^{-(k-1)},1-2^{-k})\times[0,1)$，$k\ge1$。这些矩形两两不交，且 $\bigcup_{k=1}^{\infty}R_k=\Omega$，$\operatorname{area}(R_k)=2^{-k}$。前 $N$ 个矩形的面积和为 $S_N=\sum_{k=1}^{N}2^{-k}=1-2^{-N}$，剩余面积为 $2^{-N}\to0$，所以由面积测度的可列可加性，$\operatorname{area}(\Omega)=\sum_{k=1}^{\infty}\operatorname{area}(R_k)=1$。若画闭单位正方形，只多出零面积边界，不改变面积等式。该例展示可列可加性，不能把单个图例当作对所有可测集合的一般证明。

**answer** 本图例中 $R_k$ 两两不交，$\bigcup_{k=1}^\infty R_k=[0,1)^2$，且 $\sum_{k=1}^\infty\operatorname{area}(R_k)=\sum_{k=1}^\infty2^{-k}=1$。

**objects[0]** 半开单位正方形

**objects[1]** 相邻半开矩形条

**objects[2]** 精确面积和及剩余面积

**steps[0]** 明确区域 $\Omega=[0,1)^2$，第 $k$ 条为 $R_k=[1-2^{-(k-1)},1-2^{-k})\times[0,1)$。

**steps[1]** 标注各条两两不交、并集为 $\Omega$，每条面积为 $2^{-k}$。

**steps[2]** 显示 $S_N=\sum_{k=1}^N2^{-k}=1-2^{-N}$，剩余面积为 $2^{-N}\to0$。

**steps[3]** 显示 $\sum_{k=1}^\infty\operatorname{area}(R_k)=1$；本图例展示可列可加性，不作为一般可测集合的完整证明。
