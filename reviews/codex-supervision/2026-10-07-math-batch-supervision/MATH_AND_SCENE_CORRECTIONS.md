# 本轮10条修订的完整题目、解答、答案和场景

## calc-green-005

正向圆周和半径需明确 a>0。

题目：利用格林公式计算曲线积分 $\oint_L x dy - y dx$，其中 $L$ 是正向圆周 $x^2 + y^2 = a^2$。（设 $a>0$。）

解答：设 $P(x,y) = -y$，$Q(x,y) = x$。则 $\frac{\partial Q}{\partial x} = 1$，$\frac{\partial P}{\partial y} = -1$。由格林公式，原积分 $= \iint_D \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) dxdy = \iint_D (1 - (-1)) dxdy = 2 \iint_D dxdy$。因为 $\iint_D dxdy$ 等于圆盘的面积 $\pi a^2$，所以原积分 $= 2 \pi a^2$。

答案：$2\pi a^2$

场景：

- 直角坐标系
- 红色圆周曲线 $L$，带有逆时针方向箭头
- 内部区域 $D$ 的蓝色半透明填充
- 圆内区域的向量场箭头（代表 $P$ 和 $Q$ 的分量）
- 右侧文字公式 $\oint_L P dx + Q dy = \iint_D \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) dxdy$

1. 第一步：画出直角坐标系，用红色绘制一个以原点为圆心、半径为 $a$ 的圆形路径 $L$。
2. 第二步：在圆的边界上添加逆时针方向的红色箭头，标出正向路径。
3. 第三步：用蓝色半透明颜色填充圆内部的区域 $D$，代表边界 $L$ 围成的闭区域。
4. 第四步：在圆的区域内随机绘制一些微小的向量箭头，示意在向量场中每个点的方向。
5. 第五步：画面右侧同步展示偏导数计算推导：$\frac{\partial Q}{\partial x} = 1$，$\frac{\partial P}{\partial y} = -1$。
6. 第六步：高亮显示格林公式等式，并强调左边的边界积分等价于右边区域的二重积分，最终展现结果 $2\pi a^2$。

原始记录 SHA：a732f0521056602044ad966ef416bdef289458a8bd6c53bb3b8ca2d316745c44
候选记录 SHA：6fbed8cad64ca35839f5d6df94ffbfd0f6e94d2bc4bdb9322a4952932f2c5a12

## calc-area-009

摆线一拱的标准半径参数应明确 a>0。

题目：求摆线 $x = a(t - \sin t), y = a(1 - \cos t)$ 的一拱（$0 \le t \le 2\pi$）与 $x$ 轴所围成的面积。（设 $a>0$。）

解答：摆线的一拱与 $x$ 轴围成封闭图形。面积 $S = \int_{0}^{2\pi a} y dx$。将参数方程代入，得 $S = \int_{0}^{2\pi} a(1 - \cos t) \cdot d[a(t - \sin t)] = \int_{0}^{2\pi} a(1 - \cos t) \cdot a(1 - \cos t) dt = a^2 \int_{0}^{2\pi} (1 - 2\cos t + \cos^2 t) dt$。利用三角函数积分性质，其中 $\cos t$ 在周期内积分为0，故 $S = a^2 \int_{0}^{2\pi} (1 + \frac{1+\cos 2t}{2}) dt = a^2 \cdot 3\pi = 3\pi a^2$。

答案：$3\pi a^2$

场景：

- 带有刻度的黑色直角坐标系
- 蓝色摆线一拱的轨迹
- 摆线与x轴围成的黄色半透明区域
- 参数t动态变化指示点
- 沿x轴滚动的圆

1. 第一步：绘制直角坐标系，在x轴上画一个沿着x轴滚动的圆。
2. 第二步：通过圆边缘的一个固定点，随着圆滚动，动态描绘出摆线的一拱轨迹 $x = a(t - \sin t), y = a(1 - \cos t)$。
3. 第三步：当圆滚过一个完整周期（$0 \le t \le 2\pi$）后，摆线与x轴围成了一个封闭的拱形区域，用黄色半透明填充。
4. 第四步：展示公式推导，强调变量替换过程，将 $y$ 和 $dx$ 均用参数 $t$ 的表达式替换。
5. 第五步：高亮显示最终的面积结果 $3\pi a^2$。

原始记录 SHA：15ce0d6025f6a3cf50952947ed7c3d8eb85ddfd296b20765769f119e748c949e
候选记录 SHA：cd6964e1a6da29353ef0af297b38cd891c51d3a6bcdfdd879e7de195f5f684eb

## linalg-064

给出全部非零特征向量，排除零向量。

题目：求矩阵 $A=\begin{pmatrix} 3 & 1 \\ 0 & 2 \end{pmatrix}$ 的特征值和特征向量，并说明其几何意义。

解答：$|\lambda I-A|=(\lambda-3)(\lambda-2)$。当 $\lambda=3$ 时，$(A-3I)v=0$ 等价于 $v_2=0$，故 $E_3=\operatorname{span}\{(1,0)^T\}$；全部特征向量为 $t(1,0)^T$，$t\in\mathbb R\setminus\{0\}$。当 $\lambda=2$ 时，$(A-2I)v=0$ 等价于 $v_1+v_2=0$，故 $E_2=\operatorname{span}\{(1,-1)^T\}$；全部特征向量为 $t(1,-1)^T$，$t\in\mathbb R\setminus\{0\}$。在两条特征直线上分别有 $Av=3v$ 和 $Av=2v$，所以方向保持，长度分别乘以 $3$ 和 $2$。

答案：$\lambda=3$：$E_3=\operatorname{span}\{(1,0)^T\}$，特征向量 $t(1,0)^T$，$t\ne0$；$\lambda=2$：$E_2=\operatorname{span}\{(1,-1)^T\}$，特征向量 $t(1,-1)^T$，$t\ne0$。相应方向分别拉伸 $3$ 倍和 $2$ 倍。

场景：

- 二维坐标系
- 标准网格
- 多个方向向量
- 特征向量高亮

1. 第一步：画出标准网格和几个不同方向的向量。
2. 第二步：应用矩阵变换，展示大部分向量方向发生改变。
3. 第三步：高亮特征向量 (1,0)，展示它方向不变，长度变为 3 倍。
4. 第四步：高亮特征向量 (1,-1)，展示它方向不变，长度变为 2 倍。

原始记录 SHA：1054f681c953165c301284e10ffd60b406c424a9cc8357f3449d60a467c14499
候选记录 SHA：3cf69bfaf0c138629257f163616091d3523f1d0dbed9b203c81363dbc6dc33d5

## calc-limit-006

场景中“约45度”可用精确 π/4；有限图形仅示意，证明使用对所有 0<x<π/2 的面积不等式。

题目：求极限 $\lim_{x \to 0} \frac{\sin x}{x}$ 的值。

解答：利用夹逼定理（Squeeze Theorem）进行几何证明。在单位圆中，设圆心角为 $x$（$0 < x < \frac{\pi}{2}$），比较 $\triangle OAB$、扇形 $OAB$ 和 $\triangle OAC$ 的面积。可以推导出不等式 $\sin x < x < \tan x$。同时除以 $\sin x$ 得到 $1 < \frac{x}{\sin x} < \frac{1}{\cos x}$。取倒数得 $\cos x < \frac{\sin x}{x} < 1$。由于 $\frac{\sin x}{x}$ 为偶函数，$x \to 0^-$ 时结论同样成立。当 $x \to 0$ 时，$\cos x \to 1$，由夹逼定理可得 $\lim_{x \to 0} \frac{\sin x}{x} = 1$。

答案：1

场景：

- 单位圆，$O=(0,0)$，$A=(1,0)$
- 参数点 $B=(\cos x,\sin x)$，$0<x<\frac{\pi}{2}$
- 交点 $C=(1,\tan x)$，射线 $OB$ 与 $A$ 处切线相交
- 三块区域及精确面积 $\frac12\sin x,\frac12 x,\frac12\tan x$

1. 初始角取 $x=\frac{\pi}{4}$；之后在 $0<x<\frac{\pi}{2}$ 内变化。
2. 展示 $\triangle OAB\subsetneq$ 扇形 $OAB\subsetneq\triangle OAC$，由面积得 $\sin x<x<\tan x$。
3. 由 $\sin x>0$ 得 $\cos x<\frac{\sin x}{x}<1$；显示 $\lim_{x\to0^+}\cos x=1$。
4. 以偶性 $\frac{\sin(-x)}{-x}=\frac{\sin x}{x}$ 得双侧极限 $1$。有限动画仅说明包含关系，极限结论由夹逼定理给出。

原始记录 SHA：4f07f35747328b445316aa043679b54c72add9b8ff7f29bb05b4751d497e30c9
候选记录 SHA：0577d8caa7832557dc7c0bcdc2d76260bb6b3b0942c5797f92987fb506941c0a

## linalg-053

动态测量应换成列向量叉积、精确底面积和高，避免以测量数值充当证明。

题目：利用几何图形解释三阶行列式 $\begin{vmatrix} 1 & 2 & 0 \\ 0 & 1 & 3 \\ 2 & 1 & 1 \end{vmatrix}$ 的几何意义。

解答：计算行列式得 $1(1\cdot1-3\cdot1)-2(0\cdot1-3\cdot2)+0=1(-2)-2(-6)=-2+12=10$。该行列式的绝对值等于矩阵对应的线性变换将单位立方体映射成的平行六面体的体积。体积为 10。

答案：10，即该行列式的绝对值等于矩阵对应线性变换将单位立方体映射成的平行六面体的体积

场景：

- 单位立方体及列向量 $u=(1,0,2)^T,\ v=(2,1,1)^T,\ w=(0,3,1)^T$
- 变换后的平行六面体
- 精确标签 $u\times v=(-2,3,1)^T$，$B=\sqrt{14}$，$h=\frac{10}{\sqrt{14}}$

1. 将单位立方体三条棱分别映为 $u,v,w$，保持顶点对应关系。
2. 板书 $u\times v=(-2,3,1)^T$ 和 $(u\times v)\cdot w=10$。
3. 标注底面积 $B=\|u\times v\|=\sqrt{14}$，垂直高 $h=\frac{|(u\times v)\cdot w|}{\|u\times v\|}=\frac{10}{\sqrt{14}}$。
4. 由 $V=Bh=10=|\det A|$ 得体积；图形仅示意，数值标签全部使用精确式。

原始记录 SHA：f257e2425409858699514e0beac6859df86eaa86f04a0995124e4b94e2a53ec5
候选记录 SHA：432b996caf30a744445fc41c9b14e97b80e2070267af39279299a8e4d65027b1

## linalg-054

D=0 必须覆盖平行不重合和重合两种情形；固定题面不能暗示拖动斜率后仍是原方程组。

题目：利用 Cramer 法则求解线性方程组 $\begin{cases} 2x + y = 5 \\ x - y = 1 \end{cases}$，并说明行列式为零时的几何意义。

解答：系数行列式 $D=\begin{vmatrix} 2 & 1 \\ 1 & -1 \end{vmatrix}=-3\neq0$，方程组有唯一解。$D_x=\begin{vmatrix} 5 & 1 \\ 1 & -1 \end{vmatrix}=-6$，$D_y=\begin{vmatrix} 2 & 5 \\ 1 & 1 \end{vmatrix}=-3$，故 $x=2, y=1$。若 $D=0$，两直线平行或重合，对应无解或无穷多解。

答案：$x=2, y=1$；当系数行列式为零时，两直线平行或重合，对应无解或无穷多解

场景：

- 原题直线 $2x+y=5$ 和 $x-y=1$
- 交点 $(2,1)$ 与 $D=-3,\ D_x=-6,\ D_y=-3$
- 独立示例面板：平行不重合与重合

1. 原题面板保持两条方程不变，以 Cramer 法则显示 $x=D_x/D=2,\ y=D_y/D=1$。
2. 另开明确标为“系数行列式为零的示例”的面板，不把它当作原题的继续计算。
3. 例一 $x+y=1,\ 2x+2y=3$：$D=0$，平行不重合，无解。
4. 例二 $x+y=1,\ 2x+2y=2$：$D=0$，两直线重合，解集 $\{(t,1-t):t\in\mathbb R\}$。

原始记录 SHA：da8cdcee83888931a391155143b894ddf1cf7977f59da628e02b9ac430c56dba
候选记录 SHA：f3b22b400485ff50782724cb134c5df7e40e1468795ff70a5703f980b4c9cdbf

## linalg-067

有限图形的动态测量不证明任意向量的保距性，补上 A^TA=I 的精确恒等式。

题目：验证矩阵 $A=\begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$ 是正交矩阵，并说明其对应的正交变换。

解答：$A^TA=\begin{pmatrix} \cos\theta & \sin\theta \\ -\sin\theta & \cos\theta \end{pmatrix}\begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}=I$，故 A 是正交矩阵。它对应的变换是平面上的旋转 θ 角。

答案：A 是正交矩阵，对应旋转 θ 角

场景：

- 旋转矩阵 $A=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}$
- 三角形及其像，所有边长标签保持符号 $\|u-v\|$
- 板书 $A^TA=I$ 和 $\langle Au,Av\rangle=\langle u,v\rangle$

1. 演示任意角 $\theta$ 的旋转，图形仅用于示意。
2. 由 $\cos^2\theta+\sin^2\theta=1$ 逐项计算 $A^TA=I$。
3. 对任意 $u,v$，$\|Au-Av\|^2=(u-v)^TA^TA(u-v)=\|u-v\|^2$；对非零向量，内积和长度保持，因此夹角保持。
4. 高亮 $\det A=1$，说明它是定向保持的平面旋转。

原始记录 SHA：308ae4734dad5650788d5605531f4ce593ab67bfaab45ee9b769190388c3ff9f
候选记录 SHA：3f70cb26aa7f187055812d0c9b3ca0a4aa1aa22037234711f2ac61a1e12de261

## geom-028

l=m=0 尚不能推出直线退化，必须再由一次项系数得到 n=0。

题目：判断椭圆抛物面 $z = x^2 + y^2$ 是否为直纹面，并说明理由。

解答：不是直纹面。假设它是直纹面，则曲面上存在直线。设直线过点 $(x_0, y_0, z_0)$，方向向量为 $(l, m, n)$，参数方程为 $(x_0+lt, y_0+mt, z_0+nt)$。代入曲面方程 $z=x^2+y^2$ 并整理得 $t^2(l^2+m^2)+t(2x_0l+2y_0m-n)+(x_0^2+y_0^2-z_0)=0$。若该方程对任意 $t$ 成立，则各次项系数全为零：由 $l^2+m^2=0$ 得 $l=m=0$；再由一次项系数 $2x_0l+2y_0m-n=0$ 得 $n=0$。于是方向向量为零向量，直线退化为一个点，矛盾。因此，椭圆抛物面上不存在直线，它不是直纹面。

答案：不是直纹面

场景：

- 实曲面 $z=x^2+y^2$
- 候选直线 $(x,y,z)=(x_0+lt,y_0+mt,z_0+nt)$
- 方向条件 $(l,m,n)\ne(0,0,0)$

1. 图示候选直线只作示意；显示代入恒等式 $t^2(l^2+m^2)+t(2x_0l+2y_0m-n)+(x_0^2+y_0^2-z_0)=0$。
2. 若整条直线在曲面上，该多项式对所有 $t\in\mathbb R$ 为零，故每个系数为零。
3. 二次项给出 $l^2+m^2=0$，在实数域上得 $l=m=0$；一次项再给出 $-n=0$。
4. 于是 $(l,m,n)=(0,0,0)$，与直线方向非零矛盾；因此曲面不含直线，也不是直纹面。

原始记录 SHA：0d057d9c18189ad4032f1d8b7025e53a6a8e9938c7282f9f8e6713f4d85a446e
候选记录 SHA：ef3561df932f82a7976e9759819538b6b171f464119b660d8cd8ab5eccb96808

## prob-040

把笼统“很大/很小/近似”改为 pn 序列的精确极限；补固定 k、λ=0 分支、离散质量图和方差精确式。

题目：设 $p_n\in[0,1]$，$np_n\to\lambda\in[0,+\infty)$，$X_n\sim B(n,p_n)$。证明对每个固定 $k\in\mathbb Z_{\ge0}$，$P(X_n=k)$ 的极限为参数 $\lambda$ 的泊松概率质量，并给出 $\lambda=0$ 的退化情形。

解答：先设 $\lambda>0$。因为 $np_n\to\lambda$，有 $p_n\to0$。对固定 $k\ge0$，当 $n\ge k$ 且充分大时，
$P(X_n=k)=\frac{(np_n)^k}{k!}\prod_{j=0}^{k-1}(1-\frac jn)(1-p_n)^n(1-p_n)^{-k}$，其中 $k=0$ 时空乘积为 $1$。
对 $0\le u<1$，$-\frac{u}{1-u}\le\log(1-u)\le-u$，故
$-\frac{np_n}{1-p_n}\le n\log(1-p_n)\le-np_n$，夹逼得 $n\log(1-p_n)\to-\lambda$，从而 $(1-p_n)^n\to e^{-\lambda}$。其余三个因子分别趋于 $\lambda^k/k!$、$1$、$1$，所以 $P(X_n=k)\to e^{-\lambda}\lambda^k/k!$。
若 $\lambda=0$，由 Markov 不等式 $P(X_n\ge1)\le E X_n=np_n\to0$，故 $P(X_n=0)\to1$，且对 $k\ge1$ 有 $P(X_n=k)\to0$。

答案：若 $\lambda>0$，则对每个固定 $k\in\mathbb Z_{\ge0}$，$\displaystyle\lim_{n\to\infty}P(X_n=k)=\frac{e^{-\lambda}\lambda^k}{k!}$；若 $\lambda=0$，则极限为 $k=0$ 时的 $1$ 和 $k\ge1$ 时的 $0$。

场景：

- 离散横坐标 $k\in\mathbb Z_{\ge0}$ 和二项概率质量柱
- 泊松质量点 $q_k=e^{-5}5^k/k!$，不绘为连续概率密度
- 受约束参数 $n\in\mathbb Z,\ n\ge5,\ p_n=5/n$

1. 取 $n=10$，$p_n=\frac12$，显示二项概率质量的精确公式 $\binom nk(5/n)^k(1-5/n)^{n-k}$。
2. 令整数 $n$ 增大，始终保持 $p_n=5/n$；标注 $EX_n=5$ 与 $\operatorname{Var}(X_n)=5-\frac{25}{n}$，$n=10$ 时方差为 $\frac52$。
3. 在整数 $k$ 处叠加泊松质量点 $q_k$，若截断显示只标示有限窗口，其外概率仍按分布公式定义。
4. 板书固定 $k$ 的严格极限推导；有限柱图仅示意。有限 $n$ 时不声称二项分布与泊松分布相等。

原始记录 SHA：8603c675ce665f2e3cda9c651e7ff29123390af943ae42c0dfb34ed87ee222c8
候选记录 SHA：8ac6000bc9cf96a828d535fc5e6d2df42972fa367ee264626831fb2f2b0c7014

## prob-041

明确 σ>0；正态区间概率用 erf 或积分精确式替换0.6827和0.9545。

题目：? $\mu\in\mathbb R$?$\sigma>0$?$X\sim N(\mu,\sigma^2)$??????????????? $\mu$ ? $\sigma$ ?????????

解答：密度为 $f_{\mu,\sigma}(x)=\frac{1}{\sigma\sqrt{2\pi}}\exp(-\frac{(x-\mu)^2}{2\sigma^2})$，其中 $\sigma>0$。
令 $\phi(z)=\frac{1}{\sqrt{2\pi}}e^{-z^2/2}$，则 $f_{\mu,\sigma}(x)=\sigma^{-1}\phi((x-\mu)/\sigma)$：改变 $\mu$ 只平移对称轴 $x=\mu$；增大 $\sigma$ 时横向按比例展宽，峰高 $f_{\mu,\sigma}(\mu)=1/(\sigma\sqrt{2\pi})$ 降低，总积分仍为 $1$。
由 $Z=(X-\mu)/\sigma\sim N(0,1)$，对任意 $c\ge0$，
$P(|X-\mu|\le c\sigma)=\frac{1}{\sqrt{2\pi}}\int_{-c}^{c}e^{-z^2/2}\,dz=\operatorname{erf}(c/\sqrt2)$。
这里 $\operatorname{erf}(u)=\frac2{\sqrt\pi}\int_0^u e^{-t^2}\,dt$，所以 $c=1,2$ 时分别为 $\operatorname{erf}(1/\sqrt2)$、$\operatorname{erf}(\sqrt2)$。

答案：$\mu$ ????????$\sigma>0$ ????????? $\sigma$ ???????? $\frac1{\sigma\sqrt{2\pi}}$ ???????? $1$?

场景：

- 密度 $f_{\mu,\sigma}(x)$，参数 $\mu\in\mathbb R,\ \sigma>0$
- 对称轴 $x=\mu$，峰高标签 $\frac1{\sigma\sqrt{2\pi}}$
- 精确阴影标签 $\operatorname{erf}(1/\sqrt2)$ 和 $\operatorname{erf}(\sqrt2)$

1. 初始展示 $N(0,1)$，板书 $\int_{\mathbb R}\phi(z)\,dz=1$。
2. 改变 $\mu$ 仅平移曲线；改变 $\sigma$ 时始终限制为正数，显示缩放公式 $f_{\mu,\sigma}(x)=\sigma^{-1}\phi((x-\mu)/\sigma)$。
3. 对区间 $[\mu-\sigma,\mu+\sigma]$ 和 $[\mu-2\sigma,\mu+2\sigma]$ 填充阴影，只使用精确概率 $\operatorname{erf}(1/\sqrt2)$ 和 $\operatorname{erf}(\sqrt2)$。
4. 展示变量代换 $z=(x-\mu)/\sigma$；面积结论来自精确积分，视觉阴影只作示意。

原始记录 SHA：eae914133e0447d5ba8da272170e4397878aaa3aafeb77f0833e5525ec03174f
候选记录 SHA：709f96f3e19cf35bbcb14582527248bfe3c357efe8cf9118020992e2efde06c3

