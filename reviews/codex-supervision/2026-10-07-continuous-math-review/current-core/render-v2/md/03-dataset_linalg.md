## linalg-048

problem

已知矩阵 $A=\begin{pmatrix}1&3\\0&1\end{pmatrix}$，求该矩阵对应的线性变换对二维平面的几何影响。

solution

对任意点 $(x,y)$，$T(x,y)=A\begin{pmatrix}x\\y\end{pmatrix}=\begin{pmatrix}x+3y\\y\end{pmatrix}$，位移为 $(3y,0)$。故 $x$ 轴逐点固定，$\vec e_1=(1,0)$ 不动，$\vec e_2=(0,1)$ 映为 $(3,1)$。对于任意 $c\in\mathbb R$，$T(\mathbb R\times\{c\})=\mathbb R\times\{c\}$：整条水平直线作为点集保持不变，其上每个带标记点的横坐标增加 $3c$。有限线段 $[0,1]\times\{c\}$ 则映为 $[3c,1+3c]\times\{c\}$。竖直线 $x=c$ 的像可写为 $(X,Y)=(c+3t,t)$，$t\in\mathbb R$，即 $X-3Y=c$，斜率为 $\frac13$。沿边界次序，单位正方形顶点 $(0,0),(1,0),(1,1),(0,1)$ 依次映为 $(0,0),(1,0),(4,1),(3,1)$，得到底长 $1$、高 $1$ 的平行四边形。$\det A=1\cdot1-3\cdot0=1$，故面积与定向均保持。这是一种水平剪切；移动距离为 $3|y|$，纵坐标不变。长度一般不保持，例如 $\|(0,1)\|=1$ 而 $\|T(0,1)\|=\sqrt{10}$。

answer

水平剪切 $T(x,y)=(x+3y,y)$；$x$ 轴逐点固定，水平直线作为点集不变、带标记点的位移为 $(3y,0)$；竖直线 $x=c$ 映为 $X-3Y=c$；面积和定向保持，$\det A=1$，长度一般不保持。

scene_spec.objects[0]

带有刻度的黑色坐标轴

scene_spec.objects[1]

蓝色单位正方形，按边界次序连接 $(0,0),(1,0),(1,1),(0,1)$

scene_spec.objects[2]

橙色平行四边形，按边界次序连接 $(0,0),(1,0),(4,1),(3,1)$

scene_spec.objects[3]

青色有限线段 $[0,1]\times\{\frac12\}$ 和 $[0,1]\times\{1\}$，各自标记左端点；无限水平直线仅用作不变的参考线

scene_spec.objects[4]

白色板书 $T(x,y)=(x+3y,y)$、$\det A=1$ 与 $X-3Y=c$

scene_spec.steps[0]

第一步：绘制坐标轴与蓝色单位正方形，按边界次序标记四个顶点。

scene_spec.steps[1]

第二步：显示 $T(x,y)=(x+3y,y)$ 和 $\det A=1$，说明 $x$ 轴逐点固定。

scene_spec.steps[2]

第三步：将两条有限线段分别平移 $\frac32$ 和 $3$，终点线段为 $[\frac32,\frac52]\times\{\frac12\}$ 和 $[3,4]\times\{1\}$；闪烁带标记端点，说明整条无限水平直线作为集合不变。

scene_spec.steps[3]

第四步：按原顶点对应关系变换为橙色平行四边形，依次高亮 $(0,0),(1,0),(4,1),(3,1)$，标注底 $1$、高 $1$、面积 $1$。

scene_spec.steps[4]

第五步：展示一条竖直参考线 $x=c$ 映为 $X-3Y=c$；以 $(0,1)\mapsto(3,1)$ 说明长度由 $1$ 变为 $\sqrt{10}$，并重申面积保持。

efficiency_tags[0]

几何意义

efficiency_tags[1]

剪切变换

## linalg-050

problem

利用几何图形解释二阶行列式 $\begin{vmatrix} a & b \\ c & d \end{vmatrix} = ad - bc$ 的几何意义。

solution

令 $A=\begin{pmatrix}a&b\\c&d\end{pmatrix}$，其两列为 $u=(a,c)^T$、$v=(b,d)^T$。单位正方形顶点按次序映为 $0,u,u+v,v$，所得平行四边形的有向面积为 $\det(u,v)=ad-bc$，通常面积为 $|ad-bc|$。$\det A>0$ 时保持定向，$\det A<0$ 时反转定向。若 $\det A=0$，则 $\operatorname{rank}A\le1$：秩为 $1$ 时整个平面的像为直线、单位正方形的像为线段；秩为 $0$ 时 $A=0$，两者的像均为一个点。两种退化情形的面积均为 $0$。

answer

有向面积为 $ad-bc$，通常面积为 $|ad-bc|$；行列式为零时像可退化为线段或点。

scene_spec.objects[0]

单位正方形及列向量

scene_spec.objects[1]

有向面积与通常面积标签

scene_spec.objects[2]

秩一线段和秩零点

scene_spec.steps[0]

令 $u=(a,c)^T$、$v=(b,d)^T$，显示单位正方形的像顶点 $0,u,u+v,v$。

scene_spec.steps[1]

显示有向面积 $\det(u,v)=ad-bc$，通常面积为 $|ad-bc|$；负行列式表示定向反转。

scene_spec.steps[2]

当 $\det A=0$ 且 $\operatorname{rank}A=1$ 时，单位正方形的像为线段。

scene_spec.steps[3]

当 $\operatorname{rank}A=0$ 时，$A=0$，像为一个点；两种退化面积均为 $0$。

efficiency_tags[0]

面积计算

efficiency_tags[1]

正方形映射

## linalg-051

problem

设多项式 $f(x)=x^3-6x^2+11x-6$，将其因式分解并说明其根在复平面上的分布。

solution

由有理根定理，可能的根为 $\pm1,\pm2,\pm3,\pm6$。代入得 $f(1)=0$，故 $(x-1)$ 是因式。多项式除法得 $f(x)=(x-1)(x^2-5x+6)=(x-1)(x-2)(x-3)$。三个根均为实根，在复平面上位于实轴上。

answer

$(x-1)(x-2)(x-3)$；三个根 $1,2,3$ 均为实根，在复平面上全部位于实轴上

scene_spec.objects[0]

直角坐标系（实轴）

scene_spec.objects[1]

曲线 y=f(x)

scene_spec.objects[2]

三个实根点

scene_spec.objects[3]

因式分解公式

scene_spec.steps[0]

第一步：在坐标系中绘制三次多项式曲线 $y=x^3-6x^2+11x-6$。

scene_spec.steps[1]

第二步：在 x=1,2,3 处用黄色圆点标记曲线与 x 轴的交点，表示根的位置。

scene_spec.steps[2]

第三步：在右侧展示因式分解的代数过程，用连线将每个根与其对应的因式 $(x-1)$ 联系起来。

scene_spec.steps[3]

第四步：在数轴上展示三个根全部落在实轴上，说明该多项式无虚根。

efficiency_tags[0]

根与因式对应

efficiency_tags[1]

实根高亮

## linalg-053

problem

利用几何图形解释三阶行列式 $\begin{vmatrix} 1 & 2 & 0 \\ 0 & 1 & 3 \\ 2 & 1 & 1 \end{vmatrix}$ 的几何意义。

solution

计算行列式得 $1(1\cdot1-3\cdot1)-2(0\cdot1-3\cdot2)+0=1(-2)-2(-6)=-2+12=10$。该行列式的绝对值等于矩阵对应的线性变换将单位立方体映射成的平行六面体的体积。体积为 10。

answer

10，即该行列式的绝对值等于矩阵对应线性变换将单位立方体映射成的平行六面体的体积

scene_spec.objects[0]

单位立方体及列向量 $u=(1,0,2)^T,\ v=(2,1,1)^T,\ w=(0,3,1)^T$

scene_spec.objects[1]

变换后的平行六面体

scene_spec.objects[2]

精确标签 $u\times v=(-2,3,1)^T$，$B=\sqrt{14}$，$h=\frac{10}{\sqrt{14}}$

scene_spec.steps[0]

将单位立方体三条棱分别映为 $u,v,w$，保持顶点对应关系。

scene_spec.steps[1]

板书 $u\times v=(-2,3,1)^T$ 和 $(u\times v)\cdot w=10$。

scene_spec.steps[2]

标注底面积 $B=\|u\times v\|=\sqrt{14}$，垂直高 $h=\frac{|(u\times v)\cdot w|}{\|u\times v\|}=\frac{10}{\sqrt{14}}$。

scene_spec.steps[3]

由 $V=Bh=10=|\det A|$ 得体积；图形仅示意，数值标签全部使用精确式。

efficiency_tags[0]

单位立方体映射

efficiency_tags[1]

有向体积

## linalg-054

problem

利用 Cramer 法则求解线性方程组 $\begin{cases} 2x + y = 5 \\ x - y = 1 \end{cases}$，并说明行列式为零时的几何意义。

solution

系数行列式 $D=\begin{vmatrix} 2 & 1 \\ 1 & -1 \end{vmatrix}=-3\neq0$，方程组有唯一解。$D_x=\begin{vmatrix} 5 & 1 \\ 1 & -1 \end{vmatrix}=-6$，$D_y=\begin{vmatrix} 2 & 5 \\ 1 & 1 \end{vmatrix}=-3$，故 $x=2, y=1$。若 $D=0$，两直线平行或重合，对应无解或无穷多解。

answer

$x=2, y=1$；当系数行列式为零时，两直线平行或重合，对应无解或无穷多解

scene_spec.objects[0]

原题直线 $2x+y=5$ 和 $x-y=1$

scene_spec.objects[1]

交点 $(2,1)$ 与 $D=-3,\ D_x=-6,\ D_y=-3$

scene_spec.objects[2]

独立示例面板：平行不重合与重合

scene_spec.steps[0]

原题面板保持两条方程不变，以 Cramer 法则显示 $x=D_x/D=2,\ y=D_y/D=1$。

scene_spec.steps[1]

另开明确标为“系数行列式为零的示例”的面板，不把它当作原题的继续计算。

scene_spec.steps[2]

例一 $x+y=1,\ 2x+2y=3$：$D=0$，平行不重合，无解。

scene_spec.steps[3]

例二 $x+y=1,\ 2x+2y=2$：$D=0$，两直线重合，解集 $\{(t,1-t):t\in\mathbb R\}$。

efficiency_tags[0]

解的存在性条件

efficiency_tags[1]

行列式为零

## linalg-055

problem

讨论线性方程组 $\begin{cases} x + y + z = 1 \\ x - y + z = 1 \\ 2x + z = 2 \end{cases}$ 解的情况。

solution

系数矩阵的秩为 3，增广矩阵的秩也为 3，故方程组有唯一解。通过消元法：由第一式减第二式得 $2y=0 \Rightarrow y=0$。代入第一式和第三式得 $x+z=1$ 且 $2x+z=2$，相减得 $x=1, z=0$。即解为 $(1, 0, 0)$。

answer

唯一解，$(1, 0, 0)$

scene_spec.objects[0]

三维坐标系

scene_spec.objects[1]

三个平面

scene_spec.objects[2]

交点

scene_spec.steps[0]

第一步：在三维空间中画出三个平面，用不同颜色区分。

scene_spec.steps[1]

第二步：观察三个平面的位置关系，它们相交于唯一的一点。

scene_spec.steps[2]

第三步：高亮显示这个交点，标注其坐标为 $(1, 0, 0)$。

scene_spec.steps[3]

第四步：说明系数矩阵的秩等于增广矩阵的秩且等于未知数个数，对应唯一解。

efficiency_tags[0]

唯一解

efficiency_tags[1]

秩的几何意义

## linalg-056

problem

求齐次线性方程组 $\begin{cases} x_1 + 2x_2 + x_3 = 0 \\ 2x_1 + 4x_2 + 2x_3 = 0 \end{cases}$ 的基础解系。

solution

系数矩阵的秩为 1，未知量个数为 3，故基础解系包含 $3-1=2$ 个线性无关的解向量。取自由变量 $x_2, x_3$，得基础解系 $\xi_1=(-2,1,0)^T, \xi_2=(-1,0,1)^T$，解空间为二维平面。

answer

$\xi_1=(-2,1,0)^T, \xi_2=(-1,0,1)^T$

scene_spec.objects[0]

三维坐标系

scene_spec.objects[1]

解空间平面

scene_spec.objects[2]

两个基向量

scene_spec.steps[0]

第一步：在三维坐标系中画出解空间平面（由两个基向量张成）。

scene_spec.steps[1]

第二步：用红色箭头标出基向量 ξ₁ 和 ξ₂，展示它们线性无关。

scene_spec.steps[2]

第三步：用动画展示平面上的任意解向量都可以由这两个基向量线性组合得到。

scene_spec.steps[3]

第四步：高亮平面的维度为 2，对应基础解系中解向量的个数。

efficiency_tags[0]

基础解系

efficiency_tags[1]

零空间可视化

## linalg-058

problem

说明初等矩阵 $E=\begin{pmatrix} 1 & 0 \\ 3 & 1 \end{pmatrix}$ 对应的线性变换的几何意义。

solution

该矩阵是将单位矩阵第二行加上第一行的 3 倍得到的初等矩阵。对应的线性变换是沿 $y$ 轴方向的剪切变换：平面上每一点的 $x$ 坐标不变，$y$ 坐标变为 $y+3x$。这是一个保持面积不变（行列式为 1）的剪切变换。

answer

$x$ 坐标不变，$y$ 坐标变为 $y+3x$，面积不变

scene_spec.objects[0]

二维坐标系

scene_spec.objects[1]

标准网格

scene_spec.objects[2]

剪切后网格

scene_spec.objects[3]

基向量变化

scene_spec.steps[0]

第一步：画出标准网格和单位正方形。

scene_spec.steps[1]

第二步：应用初等矩阵 E 的变换，展示水平网格线发生倾斜（竖直网格线保持竖直），网格被剪切。

scene_spec.steps[2]

第三步：观察单位正方形变为平行四边形（以仍竖直的边为底，底和高均为 1），面积保持为 1。

scene_spec.steps[3]

第四步：高亮显示行列式值为 1，说明剪切变换不改变面积。

efficiency_tags[0]

行变换几何效果

efficiency_tags[1]

面积保持

## linalg-062

problem

在 $\mathbb{R}^3$ 中，已知子空间 $W_1=\{(x,y,0)\}$（xOy平面）和 $W_2=\{(0,y,z)\}$（yOz平面），求 $\dim(W_1+W_2)$ 和 $\dim(W_1\cap W_2)$。

solution

$W_1$ 是 xOy 平面，维数 2；$W_2$ 是 yOz 平面，维数 2。它们的交是 y 轴，维数 1。根据维数公式，$\dim(W_1+W_2)=\dim W_1+\dim W_2-\dim(W_1\cap W_2)=2+2-1=3$。

answer

$\dim(W_1+W_2)=3$，$\dim(W_1\cap W_2)=1$

scene_spec.objects[0]

三维坐标系

scene_spec.objects[1]

xOy 平面

scene_spec.objects[2]

yOz 平面

scene_spec.objects[3]

交线（y 轴）

scene_spec.steps[0]

第一步：在三维空间中画出 xOy 平面（蓝色半透明）和 yOz 平面（红色半透明）。

scene_spec.steps[1]

第二步：高亮两个平面的交线——y 轴，用黄色粗线表示。

scene_spec.steps[2]

第三步：动态展示两个平面合并张成的空间，即整个三维空间。

scene_spec.steps[3]

第四步：标注维数：W₁ 维数 2，W₂ 维数 2，交维数 1，和空间维数 3。

efficiency_tags[0]

维数公式

efficiency_tags[1]

直和条件

## linalg-063

problem

设线性变换 $T:\mathbb{R}^3\to\mathbb{R}^2$ 由 $T(x,y,z)=(x+y, y+z)$ 定义，求 $T$ 的核和值域的维数。

solution

核 $\ker T=\{(x,y,z): x+y=0, y+z=0\}=\{(-y,y,-y)\}$，维数为 1。由秩-零化度定理，$\dim(\operatorname{Im}T)=3-1=2$，值域为整个 $\mathbb{R}^2$。

answer

$\dim(\ker T)=1$，$\dim(\operatorname{Im}T)=2$

scene_spec.objects[0]

三维坐标系

scene_spec.objects[1]

核空间直线

scene_spec.objects[2]

值域平面

scene_spec.objects[3]

映射箭头

scene_spec.steps[0]

第一步：在三维空间中画出核空间——一条过原点的直线，用红色高亮。

scene_spec.steps[1]

第二步：用箭头表示线性变换 T 将三维空间映射到二维平面。

scene_spec.steps[2]

第三步：展示三维空间中的向量被映射后，核空间中的向量被压缩到原点。

scene_spec.steps[3]

第四步：高亮值域平面（二维），标注维数为 2，验证维数定理。

efficiency_tags[0]

核空间可视化

efficiency_tags[1]

维数定理

## linalg-064

problem

求矩阵 $A=\begin{pmatrix} 3 & 1 \\ 0 & 2 \end{pmatrix}$ 的特征值和特征向量，并说明其几何意义。

solution

$|\lambda I-A|=(\lambda-3)(\lambda-2)$。当 $\lambda=3$ 时，$(A-3I)v=0$ 等价于 $v_2=0$，故 $E_3=\operatorname{span}\{(1,0)^T\}$；全部特征向量为 $t(1,0)^T$，$t\in\mathbb R\setminus\{0\}$。当 $\lambda=2$ 时，$(A-2I)v=0$ 等价于 $v_1+v_2=0$，故 $E_2=\operatorname{span}\{(1,-1)^T\}$；全部特征向量为 $t(1,-1)^T$，$t\in\mathbb R\setminus\{0\}$。在两条特征直线上分别有 $Av=3v$ 和 $Av=2v$，所以方向保持，长度分别乘以 $3$ 和 $2$。

answer

$\lambda=3$：$E_3=\operatorname{span}\{(1,0)^T\}$，特征向量 $t(1,0)^T$，$t\ne0$；$\lambda=2$：$E_2=\operatorname{span}\{(1,-1)^T\}$，特征向量 $t(1,-1)^T$，$t\ne0$。相应方向分别拉伸 $3$ 倍和 $2$ 倍。

scene_spec.objects[0]

二维坐标系

scene_spec.objects[1]

标准网格

scene_spec.objects[2]

多个方向向量

scene_spec.objects[3]

特征向量高亮

scene_spec.steps[0]

第一步：画出标准网格和几个不同方向的向量。

scene_spec.steps[1]

第二步：应用矩阵变换，展示大部分向量方向发生改变。

scene_spec.steps[2]

第三步：高亮特征向量 (1,0)，展示它方向不变，长度变为 3 倍。

scene_spec.steps[3]

第四步：高亮特征向量 (1,-1)，展示它方向不变，长度变为 2 倍。

efficiency_tags[0]

特定方向高亮

efficiency_tags[1]

缩放因子

## linalg-065

problem

求 λ-矩阵 $A(\lambda)=\begin{pmatrix} \lambda & 0 \\ 0 & \lambda^2-1 \end{pmatrix}$ 的不变因子和初等因子。

solution

该矩阵已是对角形。一阶行列式因子 $D_1=\gcd(\lambda, \lambda^2-1)=1$，二阶 $D_2=\lambda(\lambda^2-1)$。不变因子 $d_1=D_1=1$，$d_2=D_2/D_1=\lambda(\lambda^2-1)$，即不变因子为 $1, \lambda(\lambda^2-1)$；再将 $\lambda(\lambda^2-1)$ 分解为 $\lambda(\lambda-1)(\lambda+1)$，得初等因子为 $\lambda, \lambda-1, \lambda+1$。

answer

不变因子 $1, \lambda(\lambda^2-1)$；初等因子 $\lambda, \lambda-1, \lambda+1$

scene_spec.objects[0]

矩阵元素展示

scene_spec.objects[1]

行列式因子计算

scene_spec.objects[2]

初等因子分解动画

scene_spec.steps[0]

第一步：展示 λ-矩阵，用不同颜色标出对角线元素。

scene_spec.steps[1]

第二步：计算一阶行列式因子 D₁=1，用动画展示最大公因式的提取过程。

scene_spec.steps[2]

第三步：计算二阶行列式因子 D₂=λ(λ²-1)。

scene_spec.steps[3]

第四步：展示不变因子和初等因子的分解结果，用颜色块区分不同的因子。

efficiency_tags[0]

对角线元素

efficiency_tags[1]

初等因子分解

## linalg-066

problem

求矩阵 $A=\begin{pmatrix} 2 & 1 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 3 \end{pmatrix}$ 的若尔当标准形。

solution

A 已经是分块对角形式。主对角线上有一个 2×2 的若尔当块 $J_1(2)=\begin{pmatrix} 2 & 1 \\ 0 & 2 \end{pmatrix}$ 和一个 1×1 的若尔当块 $J_2(3)=(3)$。故若尔当标准形为 $\operatorname{diag}(J_1(2), J_2(3))$。

answer

$\begin{pmatrix} 2 & 1 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 3 \end{pmatrix}$

scene_spec.objects[0]

矩阵可视化

scene_spec.objects[1]

若尔当块高亮

scene_spec.steps[0]

第一步：展示矩阵 A，用不同颜色标出两个若尔当块。

scene_spec.steps[1]

第二步：用动画高亮矩阵的分块结构，直观展示两个若尔当块。

scene_spec.steps[2]

第三步：高亮 2×2 的若尔当块，展示其主对角线为 2、超对角线上的 1 表示该块不可对角化。

scene_spec.steps[3]

第四步：标注 1×1 的若尔当块对应特征值 3，可以单独对角化。

efficiency_tags[0]

若尔当块

efficiency_tags[1]

分块高亮

## linalg-067

problem

验证矩阵 $A=\begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$ 是正交矩阵，并说明其对应的正交变换。

solution

$A^TA=\begin{pmatrix} \cos\theta & \sin\theta \\ -\sin\theta & \cos\theta \end{pmatrix}\begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}=I$，故 A 是正交矩阵。它对应的变换是平面上的旋转 θ 角。

answer

A 是正交矩阵，对应旋转 θ 角

scene_spec.objects[0]

旋转矩阵 $A=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}$

scene_spec.objects[1]

三角形及其像，所有边长标签保持符号 $\|u-v\|$

scene_spec.objects[2]

板书 $A^TA=I$ 和 $\langle Au,Av\rangle=\langle u,v\rangle$

scene_spec.steps[0]

演示任意角 $\theta$ 的旋转，图形仅用于示意。

scene_spec.steps[1]

由 $\cos^2\theta+\sin^2\theta=1$ 逐项计算 $A^TA=I$。

scene_spec.steps[2]

对任意 $u,v$，$\|Au-Av\|^2=(u-v)^TA^TA(u-v)=\|u-v\|^2$；对非零向量，内积和长度保持，因此夹角保持。

scene_spec.steps[3]

高亮 $\det A=1$，说明它是定向保持的平面旋转。

efficiency_tags[0]

长度不变

efficiency_tags[1]

夹角不变

## linalg-069

problem

设 $V=\mathbb{R}^2$，$\varepsilon_1=(1,0), \varepsilon_2=(0,1)$ 是标准基。求对偶基 $f_1, f_2$，使得 $f_i(\varepsilon_j)=\delta_{ij}$。

solution

对偶空间 $V^*$ 中的线性函数 $f$ 由其在基向量上的值唯一确定。对偶基满足 $f_1(\varepsilon_1)=1, f_1(\varepsilon_2)=0$；$f_2(\varepsilon_1)=0, f_2(\varepsilon_2)=1$。即 $f_1(x,y)=x, f_2(x,y)=y$。

answer

$f_1(x,y)=x, f_2(x,y)=y$

scene_spec.objects[0]

二维坐标系

scene_spec.objects[1]

基向量

scene_spec.objects[2]

对偶基线性函数等值线

scene_spec.steps[0]

第一步：在二维空间中画出标准基向量 ε₁ 和 ε₂。

scene_spec.steps[1]

第二步：画出线性函数 f₁(x,y)=x 的等值线（竖直线），展示它在 ε₁ 上值为 1，在 ε₂ 上值为 0。

scene_spec.steps[2]

第三步：画出 f₂(x,y)=y 的等值线（水平线），展示其对偶性质。

scene_spec.steps[3]

第四步：高亮对偶基的克罗内克 δ 性质。

efficiency_tags[0]

对偶基可视化

efficiency_tags[1]

线性泛函

## linalg-070

problem

在 $\mathbb{R}^2$ 上定义辛形式 $\omega(u,v)=u_1v_2-u_2v_1$（标准行列式形式），说明辛变换保持该形式不变的意义。

solution

设 $J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}$，则 $\omega(u,v)=u^TJv=\det(u,v)$，表示有向面积。对 $A=\begin{pmatrix}a&b\\c&d\end{pmatrix}$，有 $A^TJA=\begin{pmatrix}0&ad-bc\\bc-ad&0\end{pmatrix}=(\det A)J$，因此 $\omega(Au,Av)=(\det A)\omega(u,v)$。二维中，$A$ 是辛变换当且仅当 $\det A=1$；它同时保持有向面积、通常面积与定向。仅保持通常面积还不足以判定为辛变换：反射 $R=\operatorname{diag}(1,-1)$ 的行列式为 $-1$，它使 $\omega(Ru,Rv)=-\omega(u,v)$。

answer

辛变换保持有向面积与定向：$\omega(Au,Av)=\omega(u,v)$；二维中等价于 $\det A=1$。

scene_spec.objects[0]

带定向箭头的平行四边形

scene_spec.objects[1]

辛形式矩阵恒等式

scene_spec.objects[2]

反射对照

scene_spec.steps[0]

显示 $\omega(u,v)=u^TJv=\det(u,v)$，标签为有向面积。

scene_spec.steps[1]

逐式显示 $A^TJA=(\det A)J$，故二维中辛条件等价于 $\det A=1$。

scene_spec.steps[2]

辛变换保持有向面积、通常面积和定向。

scene_spec.steps[3]

用 $R=\operatorname{diag}(1,-1)$ 对照：通常面积不变，但 $\omega(Ru,Rv)=-\omega(u,v)$。

efficiency_tags[0]

辛形式

efficiency_tags[1]

面积守恒
