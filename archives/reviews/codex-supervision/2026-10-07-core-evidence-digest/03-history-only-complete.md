# 其他已恢复历史记录

共 299 份原始内容记录，其中 298 份题目内容、1 份合成字段测试记录（id=ok，p/s/1）。原文逐字段保留，历史错误或小数也是原始证据，不代表本轮认可。每项的场景、方法、条件补充字段见 `record-variants.jsonl`；父级上下文及原始字节见 `mathematical-source-bytes.zip`。数学资格审查必须连同这些上下文进行。本轮只装配证据，不新增核心判定或答案验收。

## 1. ok（合成字段测试记录）

内容 SHA256：`00cb47280ade15d43cb4eddcc1936508b8fc87a85130bae952c9ddb16021a641`。

来源：reviews/codex-supervision/history-from-code/clone-check/reviews/2026-09-30-initial/fixtures/fields.jsonl；源 SHA256 `08c2089c972af7203e3d40faae8be855e386d25698d315a1cdcd97663986f7eb`；行 1，JSON pointer `/`。

**题干**

p

**过程**

s

**答案原文**

1

## 2. draft-c32-01

内容 SHA256：`0252ae47f10aed2a49ea119be5394779878269cb19fe49d0be517eeb5924522a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft.jsonl；源 SHA256 `e019465093b291bd83fb6ae20f3eefc40a96df3e5137a246ad8813dd03f87b34`；行 11，JSON pointer `/`。

**题干**

求齐次线性方程组 $x_1+2x_2-x_3+x_4=0$ 的基础解系。

**过程**

一个方程、四个未知量,自由未知量为 $x_2,x_3,x_4$,解出 $x_1=-2x_2+x_3-x_4$。分别令 $(x_2,x_3,x_4)=(1,0,0),(0,1,0),(0,0,1)$,得基础解系 $\xi_1=(-2,1,0,0)$,$\xi_2=(1,0,1,0)$,$\xi_3=(-1,0,0,1)$。解空间为 $\mathrm{span}\{\xi_1,\xi_2,\xi_3\}$,维数 $3$。

**答案原文**

基础解系:$\xi_1=(-2,1,0,0)$,$\xi_2=(1,0,1,0)$,$\xi_3=(-1,0,0,1)$。

## 3. draft-c28-05

内容 SHA256：`037a1c862c363876b188c77e1956af2ab816d40430dc456f53a0b9d4503f3a63`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-05/target_three.json；源 SHA256 `49dd7457ba237124b29e5478a14f1475d71b950cf91b2d437ad31f8504ed9fff`；行 —，JSON pointer `/0`。

**题干**

证明三阶行列式的绝对值等于其三个行向量张成的平行六面体的体积。

**过程**

设行向量为 $a,b,c$。向量 $b\times c$ 的模等于以 $b,c$ 为邻边的平行四边形的面积,方向垂直于该平行四边形(即平行六面体的底面)。三阶行列式等于标量三重积:$|A|=a\cdot(b\times c)$。设 $a$ 与 $b\times c$ 的夹角为 $\theta$,则 $|a\cdot(b\times c)|=|a|\,|b\times c|\,|\cos\theta|$。其中 $|b\times c|$ 是底面积,而 $|a|\,|\cos\theta|$ 恰为向量 $a$ 在底面法向 $b\times c$ 上的投影长度,即平行六面体的高。故 $|a\cdot(b\times c)|=$ 底面积 $\times$ 高 $=$ 平行六面体体积,即 $|\det A|=$ 体积。符号方面:当 $a,b,c$ 构成右手系时行列式为正,左手系时为负,对应有向体积。

**答案原文**

$|\det A|=|a\cdot(b\times c)|=$ 底面积 $\times$ 高 $=$ 平行六面体体积(证明见解法)。

## 4. draft-c04-05

内容 SHA256：`0388ad9d4694e474e99cf2303acfeaebe99a89381dc83f3808e1f961075c6201`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-07/draft.jsonl；源 SHA256 `fe3576287150709fa595d4fe033e69553cfc44acc8bd9441a4226ad815adbbd4`；行 10，JSON pointer `/`。

**题干**

由格林公式推导面积公式 $A=\frac12\oint_L x\,dy-y\,dx$，并求椭圆 $\frac{x^2}{a^2}+\frac{y^2}{b^2}=1$ 的面积。

**过程**

在格林公式 $\oint_L P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)dxdy$ 中取 $P=-y,Q=x$,得 $\oint_L x\,dy-y\,dx=\iint_D(1+1)dxdy=2A$,故 $A=\frac12\oint_L x\,dy-y\,dx$。椭圆参数化:$x=a\cos t,y=b\sin t$($t:0\to2\pi$),则 $\oint x\,dy-y\,dx=\int_0^{2\pi}\left[(a\cos t)(b\cos t)-(b\sin t)(-a\sin t)\right]dt=ab\int_0^{2\pi}(\cos^2t+\sin^2t)\,dt=2\pi ab$。故 $A=\frac12\cdot2\pi ab=\pi ab$。

**答案原文**

面积公式 $A=\frac12\oint_L x\,dy-y\,dx$;椭圆面积为 $\pi ab$。

## 5. draft-c25-04

内容 SHA256：`039519c748d2c0cec1c00b8679533874d1f205a2cc997f2643cd6c71f65afaeb`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft.jsonl；源 SHA256 `25705ed80dbac40074a2bc29ed482de0087b12bc96d3e1ec0cb9f77722fefe0e`；行 9，JSON pointer `/`。

**题干**

求球面 $x^2+y^2+z^2=1$ 与圆锥面 $z^2=x^2+y^2$ 的交线的参数方程。

**过程**

联立:$z^2=x^2+y^2$ 代入球面得 $2(x^2+y^2)=1$,即 $x^2+y^2=\frac12$,且 $z^2=\frac12$,$z=\pm\frac{1}{\sqrt2}$。交线为两个圆:平面 $z=\frac{1}{\sqrt2}$ 内的圆 $x^2+y^2=\frac12$ 与平面 $z=-\frac{1}{\sqrt2}$ 内的圆 $x^2+y^2=\frac12$。参数方程:$(\frac{1}{\sqrt2}\cos t,\frac{1}{\sqrt2}\sin t,\frac{1}{\sqrt2})$ 与 $(\frac{1}{\sqrt2}\cos t,\frac{1}{\sqrt2}\sin t,-\frac{1}{\sqrt2})$。

**答案原文**

两个圆:$x=\frac{\cos t}{\sqrt2},\ y=\frac{\sin t}{\sqrt2},\ z=\pm\frac{1}{\sqrt2}$。

## 6. draft-c21-04

内容 SHA256：`0517fac2ae16c58965f1f2d0e3f0e94ebd7c50643893e4847fb6e2541bd0a0e8`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-05.jsonl；源 SHA256 `6eabbb3d46a7d6a4b39d563a7fc339d117b2be8533dce70e0a85bf2963570f0e`；行 4，JSON pointer `/`。

**题干**

求直线 $l:(1+t,2t,t)$ 与椭球面 $x^2+y^2+\frac{z^2}{4}=1$ 的交点，并分别代入验证。

**过程**

代入:$(1+t)^2+(2t)^2+\frac{t^2}{4}=1$,即 $1+2t+t^2+4t^2+\frac{t^2}{4}=1$,整理得 $\frac{21}{4}t^2+2t=0$,即 $t(\frac{21}{4}t+2)=0$。解得 $t=0$ 或 $t=-\frac{8}{21}$。$t=0$ 对应点 $(1,0,0)$;$t=-\frac{8}{21}$ 对应点 $(1-\frac{8}{21},-\frac{16}{21},-\frac{8}{21})=(\frac{13}{21},-\frac{16}{21},-\frac{8}{21})$。验证:$t=0$ 时 $1+0+0=1$;$t=-\frac{8}{21}$ 时 $(\frac{13}{21})^2+(-\frac{16}{21})^2+\frac14(\frac{8}{21})^2=\frac{169+256+16}{441}=\frac{441}{441}=1$。

**答案原文**

两个交点:$(1,0,0)$ 与 $(\frac{13}{21},-\frac{16}{21},-\frac{8}{21})$。

## 7. prob-045

内容 SHA256：`05e65f17aa49aee788bcee3914a3e3b2f0cd9bc85483e08d0916bb5b0c1446bd`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/0b25e054de83f8b330855e402cec271d3ef98ba02f4f5998b0711d2cf2aa9222.bin；源 SHA256 `0b25e054de83f8b330855e402cec271d3ef98ba02f4f5998b0711d2cf2aa9222`；行 8，JSON pointer `/`。

**题干**

设随机变量 $X$ 服从区间 $(0, 1)$ 上的均匀分布，求 $Y = X^2$ 的概率密度函数。

**过程**

已知 $X \sim U(0,1)$，其概率密度函数为 $f_X(x) = 1$（当 $0 < x < 1$）。采用分布函数法：先求 $Y$ 的分布函数 $F_Y(y) = P(Y \le y) = P(X^2 \le y) = P(-\sqrt{y} \le X \le \sqrt{y})$。因为 $X \in (0,1)$，所以 $F_Y(y) = P(0 < X \le \sqrt{y}) = \sqrt{y}$（当 $0 < y < 1$）。对 $y$ 求导得 $f_Y(y) = F_Y'(y) = \frac{1}{2\sqrt{y}}$。

**答案原文**

$f_Y(y) = \frac{1}{2\sqrt{y}}$，其中 $0 < y < 1$

## 8. draft-c42-01

内容 SHA256：`06290e1b4572df94c787d9217846442cd9204e578c532ffeb0478646ecd04b35`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft.jsonl；源 SHA256 `58ae126d6bd255576c005783f78e6ade29c9f0bd60b1c7fa2e0971ba6cad1a00`；行 11，JSON pointer `/`。

**题干**

设 $n$ 为单位向量。证明反射矩阵 $S=I-2nn^{\mathsf T}$ 是正交矩阵，并求其特征值与行列式。

**过程**

正交性:$S^{\mathsf T}S=(I-2nn^{\mathsf T})(I-2nn^{\mathsf T})=I-4nn^{\mathsf T}+4nn^{\mathsf T}nn^{\mathsf T}=I-4nn^{\mathsf T}+4n(n^{\mathsf T}n)n^{\mathsf T}=I$(用到 $n^{\mathsf T}n=\|n\|^2=1$)。特征值:对 $n$ 本身,$Sn=n-2n=-n$,特征值 $-1$;对任意 $v\perp n$,$Sv=v$,特征值 $1$(重数 $n-1$)。故特征值为 $-1$(一重)与 $1$($n-1$ 重),行列式 $\det S=(-1)\cdot1^{n-1}=-1$。

**答案原文**

$S$ 是正交矩阵(证明见解法);特征值 $-1$(一重)、$1$($n-1$ 重),$\det S=-1$。

## 9. draft-c52-05

内容 SHA256：`06fa01e34a745fdb29254524caeb13a8a710ef4452e0a02050e9da00b552c760`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft-v2.jsonl；源 SHA256 `592604adc88816bf3bc8b9313e3b8a0dd31c2fa5d5be9bb211e057196909e596`；行 15，JSON pointer `/`。

**题干**

设连续型随机变量 $X$ 的分布函数 $F(x)$ 严格递增。证明 $Y=F(X)$ 服从区间 $(0,1)$ 上的均匀分布；并说明：给定一个服从 $U(0,1)$ 的随机数 $U$，如何构造出服从密度 $f(x)=3x^2$($0<x<1$)的随机变量，并验证你的构造。

**过程**

对 $0<y<1$，$F_Y(y)=P(F(X)\leq y)$。因 $F$ 严格递增且连续，存在反函数 $F^{-1}$，于是 $F_Y(y)=P(X\leq F^{-1}(y))=F(F^{-1}(y))=y$，即 $Y\sim U(0,1)$。构造：目标分布函数为 $F(x)=\int_0^x3t^2\,dt=x^3$($0<x<1$)，其反函数为 $F^{-1}(u)=u^{1/3}$。由概率积分变换的逆过程，令 $X=U^{1/3}$，则 $X$ 的分布函数为 $P(U^{1/3}\leq x)=P(U\leq x^3)=x^3=F(x)$($0<x<1$)，即 $X$ 服从密度 $f(x)=F'(x)=3x^2$。

**答案原文**

$Y=F(X)\sim U(0,1)$(证明见解法)；构造：$X=U^{1/3}$ 服从 $f(x)=3x^2$($0<x<1$)，验证见解法。

## 10. eval-linalg-023-s3

内容 SHA256：`074f9f4a4ac72baa892284409576f1d51ef283776ba1b5c09792363c9838ff5d`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/8ff7044a0c48f3482ab91eef3f086f7425270923de57789c0fa3801954552720.bin；源 SHA256 `8ff7044a0c48f3482ab91eef3f086f7425270923de57789c0fa3801954552720`；行 264，JSON pointer `/`。

**题干**

分别在复数域与实数域上分解 $x^8-1$。

**过程**

本题实数域分解有两种书写形式。形式一（按共轭根配对）：$x^8-1=(x-1)(x+1)(x^2-\sqrt2x+1)(x^2+1)(x^2+\sqrt2x+1)$。形式二（按平方差递推）：$x^8-1=(x-1)(x+1)(x^2+1)(x^4+1)$。两形式由恒等式 $(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)=x^4+1$ 连接，其证明是平方差：$(x^2+1)^2-(\sqrt2x)^2=x^4+2x^2+1-2x^2=x^4+1$。故两形式一致，均为完整实不可约分解。

**答案原文**

复数域：$\displaystyle\prod_{k=0}^{7}\left(x-e^{2\pi ik/8}\right)$；实数域（完整实不可约分解）：$(x-1)(x+1)(x^2+1)(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)$

## 11. eval-linalg-031-s2

内容 SHA256：`07671c4bd525c2649aa114d0dbbd82f42e6dab06232fa59bd1fe3cec58977ff7`。

来源：reviews/codex-supervision/history-from-code/recheck-68c51be/data/v2/eval/dataset_eval.json；源 SHA256 `1de2df62edd0b01403df813c80edc3a5a9dbf1791f0b223d8e0f107ccee55e6e`；行 —，JSON pointer `/286`。

**题干**

求矩阵 $A=\begin{pmatrix}2&1&0\\0&2&1\\0&0&2\end{pmatrix}$ 的最小多项式与若尔当标准形。

**过程**

$\operatorname{rank}(A-2I)=\operatorname{rank}N=2$，$\operatorname{rank}(A-2I)^2=\operatorname{rank}N^2=1$，$\operatorname{rank}(A-2I)^3=0$。特征值 $2$ 的若尔当块个数 $=3-\operatorname{rank}(A-2I)=3-2=1$，即只有一个块，大小为 3，故标准形为 $J_3(2)$，最小多项式 $(\lambda-2)^3$。

**答案原文**

最小多项式 $(\lambda-2)^3$；若尔当标准形为 $A$ 本身（单个三阶块 $J_3(2)$）

## 12. draft-c22-05

内容 SHA256：`084b1516ec2389d0be6c9467c8454a54b7c8d0ca59b55114a4b3b45fb0484276`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/extracted/draft-c22-05.json；源 SHA256 `500920d81d34cf6488472edba3dc7f126e7ae800bd783d47cd7f2f1b6ad6570a`；行 —，JSON pointer `/`。

**题干**

证明双叶双曲面 $x^2+y^2-z^2=-1$ 不是直纹面。

**过程**

反证:设存在直线 $l(t)=p+td$ 整条在曲面上,则对一切 $t$ 有 $(p_1+td_1)^2+(p_2+td_2)^2-(p_3+td_3)^2+1=0$。这是 $t$ 的二次多项式恒为零,故三个系数全为零:常数项 $p_1^2+p_2^2-p_3^2+1=0$,一次项 $p_1d_1+p_2d_2-p_3d_3=0$,二次项 $d_1^2+d_2^2-d_3^2=0$。由第三式 $|d_3|=\sqrt{d_1^2+d_2^2}$;由第一式 $p_3^2=p_1^2+p_2^2+1$,即 $|p_3|>\sqrt{p_1^2+p_2^2}$。但由第二式与柯西不等式,$|p_3d_3|=|p_1d_1+p_2d_2|\le\sqrt{p_1^2+p_2^2}\sqrt{d_1^2+d_2^2}<\sqrt{p_3^2}\sqrt{d_3^2}=|p_3d_3|$,矛盾。故不存在整条直线在双叶双曲面上,它不是直纹面。

**答案原文**

双叶双曲面不是直纹面:假设整条直线在曲面上,多项式恒零给出三个系数方程,由柯西不等式导出 $|p_3d_3|<|p_3d_3|$ 的矛盾(证明见解法)。

## 13. draft-c39-01

内容 SHA256：`088a6e13341d861827445c97981fe9bb405f775dce578206b02d79ad99661f52`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/0173d767f1eace928f815df64ba6bbcbda23c1d9e5a66938eb47f76931ca6179.bin；源 SHA256 `0173d767f1eace928f815df64ba6bbcbda23c1d9e5a66938eb47f76931ca6179`；行 11，JSON pointer `/`。

**题干**

在实$2\times2$矩阵空间中取$A=\operatorname{diag}(1,3)$，定义$T(X)=AX-XA$。求核、像、秩，并说明全空间能否分解为核与像的直和。

**过程**

对$X=\begin{pmatrix}a&b\c&d\end{pmatrix}$，$T(X)=\begin{pmatrix}0&-2b\\2c&0\end{pmatrix}$。所以核为所有对角矩阵，基$e_{11},e_{22}$；像为所有零对角矩阵，基$e_{12},e_{21}$，秩$2$。两空间交为零且每个矩阵唯一分解为对角部分与零对角部分，故是直和。$T$在像上可逆，$T^2$在像上为$4I$，与在核上为零的作用不同；非正交Jordan中心化问题未被套用。

**答案原文**

核为对角矩阵，像为零对角矩阵，秩$2$；$M_2(\mathbb R)=\ker T\oplus\operatorname{im}T$。

## 14. linalg-049

内容 SHA256：`0957f343168e962b08d3250a45a1b403ade8d1fb4362800b41dfbc243a9aef93`。

来源：reviews/codex-supervision/history-from-code/clone-check/reviews/2026-10-03-prep-recheck/results.json；源 SHA256 `078e6bbd0c76184d36494245ab5fa7c1bbb875cfa226cdcd88c09d9c47c6d3c8`；行 —，JSON pointer `/answer_record_snapshot/linalg-049`。

**题干**

求矩阵 $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ 的特征值和特征向量，并说明其几何意义。

**过程**

特征方程为 $|\lambda I - A| = (\lambda - 2)^2 - 1 = 0$，解得特征值 $\lambda_1 = 3, \lambda_2 = 1$。对于 $\lambda_1 = 3$，解方程 $(3I - A)x = 0$ 得特征向量 $(1, 1)^T$。对于 $\lambda_2 = 1$，解得特征向量 $(1, -1)^T$。几何上，整个空间在变换时，特征向量 $(1,1)$ 的方向保持不变，长度拉伸为原来的3倍；特征向量 $(1,-1)$ 的方向也保持不变，长度保持为原来的1倍。

**答案原文**

特征值 3 和 1，对应特征向量 (1,1) 和 (1,-1)；几何意义：变换保持这两个特征方向不变，$(1,1)$ 方向拉伸为原来的 3 倍，$(1,-1)$ 方向保持不变

## 15. linalg-050

内容 SHA256：`0a13795e6504f18ab622d264e2f6270fcc31316a475da901a5d0d0a8611c9443`。

来源：reviews/codex-supervision/2026-10-06-scene-repair-takeover/math-corrected-v1/dataset_linalg.jsonl；源 SHA256 `2c977c78d12f5eb107f065edf279973d344c180fde5d1c7f241b0c54bd0a0cf4`；行 2，JSON pointer `/`。

**题干**

利用几何图形解释二阶行列式 $\begin{vmatrix} a & b \\ c & d \end{vmatrix} = ad - bc$ 的几何意义。

**过程**

令 $A=\begin{pmatrix}a&b\\c&d\end{pmatrix}$，其两列为 $u=(a,c)^T$、$v=(b,d)^T$。单位正方形顶点按次序映为 $0,u,u+v,v$，所得平行四边形的有向面积为 $\det(u,v)=ad-bc$，通常面积为 $|ad-bc|$。$\det A>0$ 时保持定向，$\det A<0$ 时反转定向。若 $\det A=0$，则 $\operatorname{rank}A\le1$：秩为 $1$ 时整个平面的像为直线、单位正方形的像为线段；秩为 $0$ 时 $A=0$，两者的像均为一个点。两种退化情形的面积均为 $0$。

**答案原文**

有向面积为 $ad-bc$，通常面积为 $|ad-bc|$；行列式为零时像可退化为线段或点。

## 16. draft-c38-05

内容 SHA256：`0b2409b2952144aee4a0edc83d279151e44b7f51eac6e516e6def87103591540`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/28d2832a953c1046e1a5df5a429b1d9b5ea65c988e1936c2ec2fdeb28be2956b.bin；源 SHA256 `28d2832a953c1046e1a5df5a429b1d9b5ea65c988e1936c2ec2fdeb28be2956b`；行 —，JSON pointer `/0`。

**题干**

证明维数公式:若 $U,V$ 是有限维线性空间 $W$ 的子空间，则 $\dim(U+V)=\dim U+\dim V-\dim(U\cap V)$。

**过程**

取 $U\cap V$ 的一组基 $u_1,\dots,u_k$($k=\dim(U\cap V)$)。把它分别延拓为 $U$ 的基 $u_1,\dots,u_k,p_1,\dots,p_r$ 与 $V$ 的基 $u_1,\dots,u_k,q_1,\dots,q_s$(其中 $r=\dim U-k$,$s=\dim V-k$)。下证向量组 $u_1,\dots,u_k,p_1,\dots,p_r,q_1,\dots,q_s$ 是 $U+V$ 的一组基。张成:任意 $w\in U+V$ 可写为 $w=u+v$($u\in U,v\in V$),两者均可由上述向量组线性表出,故整个组张成 $U+V$。线性无关:设 $(\sum\alpha_iu_i+\sum\beta_jp_j)+(\sum\alpha_i'u_i+\sum\gamma_lq_l)=0$,令 $x=\sum\alpha_iu_i+\sum\beta_jp_j\in U$,则 $x=-\sum\alpha_i'u_i-\sum\gamma_lq_l\in V$,故 $x\in U\cap V$。于是 $x$ 可仅由 $u_1,\dots,u_k$ 表出,但 $x$ 作为 $U$ 中元素用 $U$ 的基表示唯一,故 $\beta_j=0$;同理 $\gamma_l=0$,回代得 $\sum(\alpha_i+\alpha_i')u_i=0$,由线性无关得 $\alpha_i+\alpha_i'=0$。于是该向量组线性无关。故 $\dim(U+V)=k+r+s=(k+r)+(k+s)-k=\dim U+\dim V-\dim(U\cap V)$。

**答案原文**

证明见解法(交的基延拓为两子空间的基,拼接组构成 $U+V$ 的基)。

## 17. linalg-048

内容 SHA256：`0cfa04bfd6ecf4fb9e813d24e6535ca20849a67511e50d6ee67f1a9c30b5385f`。

来源：reviews/codex-supervision/2026-10-05-draft-mail-reverification/training-rewrite/linalg-048-replacement.jsonl；源 SHA256 `c4d85f2c72652cc1430841de8a3631e7861e068b051713dfe81cb6ae0c3d1d23`；行 1，JSON pointer `/`。

**题干**

设线性变换$T:\mathbb R^2\to\mathbb R^2$由$T(x,y)=(x+2y,0)$给出，$D=\{(x,y):x^2+y^2\le1\}$为闭单位圆盘。求$\ker T$与$\operatorname{im}T$，确定集合$T(D)$。对每个$q=(a,b)\in\mathbb R^2$，完整描述$D\cap T^{-1}(q)$：判定何时为空、为单点或为线段；在线段情形给出精确端点与长度，并解释圆盘在该变换下的几何变化。

**过程**

$T(x,y)=0$当且仅当$x+2y=0$，故$\ker T=\operatorname{span}\{(-2,1)\}$。任意实数$a$都有$T(a,0)=(a,0)$，故$\operatorname{im}T=\mathbb R\times\{0\}$。由柯西不等式，$(x+2y)^2\le(1^2+2^2)(x^2+y^2)\le5$，所以$T(D)\subset[-\sqrt5,\sqrt5]\times\{0\}$。反之，若$|a|\le\sqrt5$，点$p_a=\frac a5(1,2)$满足$\|p_a\|^2=a^2/5\le1$且$T(p_a)=(a,0)$，故两集合相等。若$b\ne0$，原像为空。若$b=0$，方程$x+2y=a$的全部解为$p_a+t v$，其中$v=\frac1{\sqrt5}(-2,1)$、$t\in\mathbb R$；$\|v\|=1$且$p_a\cdot v=0$，所以$\|p_a+tv\|^2=a^2/5+t^2$。当$|a|>\sqrt5$时不存在属于$D$的解；当$|a|=\sqrt5$时仅$t=0$，原像为单点$p_a$；当$|a|<\sqrt5$时，$|t|\le\sqrt{1-a^2/5}$，原像为端点$p_a\pm\sqrt{1-a^2/5}\,v$之间的闭线段，长度为$2\sqrt{1-a^2/5}$。因此，变换沿核方向把每条这样的弦压缩为一个点，将整个二维圆盘压缩为横轴上的闭线段，其二维面积为$0$。

**答案原文**

$\ker T=\operatorname{span}\{(-2,1)\}$，$\operatorname{im}T=\mathbb R\times\{0\}$，$T(D)=[-\sqrt5,\sqrt5]\times\{0\}$。记$p_a=\frac a5(1,2)$、$v=\frac{(-2,1)}{\sqrt5}$。若$b\ne0$或$|a|>\sqrt5$，则$D\cap T^{-1}(a,b)=\varnothing$；若$b=0$且$|a|=\sqrt5$，原像为$\{p_a\}$；若$b=0$且$|a|<\sqrt5$，原像端点为$p_a\pm\sqrt{1-a^2/5}\,v$，长度为$2\sqrt{1-a^2/5}$。

## 18. draft-c49-02

内容 SHA256：`0d1a65a72732676d6ab265517dee61d281dcf0fe472a00c4befa5970a5f46e4d`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft.jsonl；源 SHA256 `bcd6ec3d0204b822f83440669662afcfe3ec7712fa4806d51506f98cb797b0c2`；行 12，JSON pointer `/`。

**题干**

说明依概率收敛与几乎必然收敛的区别，并说明大数定律(频率趋于概率)属于哪一种收敛。

**过程**

定义:几乎必然收敛($X_n\xrightarrow{a.s.}X$)指 $P(\{\omega:\lim X_n(\omega)=X(\omega)\})=1$,即几乎每个样本路径最终都收敛;依概率收敛($X_n\xrightarrow{P}X$)指对任意 $\varepsilon>0$,$\lim_{n}P(|X_n-X|>\varepsilon)=0$,只要求偏差大的概率趋于零,不要求逐点路径最终稳定。关系:几乎必然收敛蕴含依概率收敛,反之不成立(可构造 $X_n$ 为「越来越窄但不断游走的脉冲」序列,依概率收敛于 $0$ 但几乎必然不收敛)。大数定律:频率 $\frac{S_n}{n}$ 依概率收敛于概率 $p$(弱大数定律);加强形式(强大数定律)给出几乎必然收敛。

**答案原文**

区别与蕴含关系见解法(几乎必然⟹依概率,反之不然);(弱)大数定律给的是依概率收敛。

## 19. calc-series-020

内容 SHA256：`0de4a1af64000de8b43571b9e58c01cb8def4df7d50e3f63f0b3a41c85bbef85`。

来源：reviews/codex-supervision/2026-10-06-scene-repair-takeover/math-correction-receipt.json；源 SHA256 `33c0a0bc6bc5281f513bf17fdda3de2a178f4700b9703bdcce7465e7cbcc0ef9`；行 —，JSON pointer `/corrections/1/record`。

**题干**

将函数 $f(x) = x$（$-\pi \le x \le \pi$）展开为傅立叶级数。

**过程**

$f(x)=x$ 为奇函数，故 $a_0=a_n=0$。分部积分得 $b_n=\frac{2}{\pi}\int_0^\pi x\sin(nx)\,dx=\frac{2}{\pi}[-\frac{x\cos(nx)}{n}+\frac{\sin(nx)}{n^2}]_0^\pi=\frac{2(-1)^{n+1}}{n}$。令 $S(x)=2\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n}\sin(nx)$。由傅里叶收敛定理，对 $-\pi<x<\pi$ 有 $S(x)=x$；在 $x=\pm\pi$，周期延拓的左右极限为 $\pi$ 与 $-\pi$，级数收敛到其中值 $0$，并不等于题中端点所指定的 $\pm\pi$。事实上每个有限部分和在这两个端点也恰为 $0$。

**答案原文**

$S(x)=2\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n}\sin(nx)$；$-\pi<x<\pi$ 时 $S(x)=x$，$x=\pm\pi$ 时 $S(x)=0$。

## 20. draft-c10-03

内容 SHA256：`0e1c3e582c2dc0b1217083844eb5482aac00e07c8af6030239402ac6cb428bf0`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft.jsonl；源 SHA256 `1cc220e2699b799fb9bacc8525e1f9d82321dc39dacd33e5c1caa21c1a7d959b`；行 3，JSON pointer `/`。

**题干**

说明级数 $\sum_{n=1}^{\infty}\frac{(-1)^n(2+(-1)^n)}{n}$ 发散，并解释莱布尼茨判别法为何不能使用。

**过程**

拆项:$\frac{(-1)^n(2+(-1)^n)}{n}=\frac{2(-1)^n+1}{n}=\frac{2(-1)^n}{n}+\frac1n$。于是原级数 $=2\sum\frac{(-1)^n}{n}+\sum\frac1n$:第一项由莱布尼茨判别法收敛,第二项调和级数发散,收敛级数与发散级数之和必发散,故原级数发散。莱布尼茨判别法不能使用的原因:通项绝对值 $a_n=\frac{2+(-1)^n}{n}$ 虽趋于 $0$,但不单调($a_n$ 在 $\frac3n$ 与 $\frac1n$ 之间跳动),不满足判别法的单调条件——可见「通项趋于零」加「交错」并不足以保证收敛。

**答案原文**

级数发散(拆成 $2\sum(-1)^n/n+\sum1/n$,收敛+发散);莱布尼茨判别法因通项绝对值不单调而不可用。

## 21. draft-c02-04

内容 SHA256：`0f197f0f0e68450f679ace1e37cdd70be197044a2855af538c7f4da9c9b13e2c`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-07/draft.jsonl；源 SHA256 `fe3576287150709fa595d4fe033e69553cfc44acc8bd9441a4226ad815adbbd4`；行 4，JSON pointer `/`。

**题干**

用分部积分法计算 $\int_0^{+\infty}xe^{-x}\,dx$。

**过程**

先对有限区间分部积分:取 $u=x,dv=e^{-x}dx$,则 $\int_0^R xe^{-x}dx=\left.-xe^{-x}\right|_0^R+\int_0^R e^{-x}dx=-Re^{-R}+(1-e^{-R})$。令 $R\to+\infty$:$Re^{-R}\to0$(指数衰减快于线性增长),$e^{-R}\to0$,故 $\int_0^{+\infty}xe^{-x}dx=1$。

**答案原文**

积分值为 $1$。

## 22. draft-c50-04

内容 SHA256：`0fbfadf8029144ec44ace298b8e546875792606ceffec4a530dbbbdc259b2f24`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-18/draft.jsonl；源 SHA256 `6f921b08949f3ee7aaa95ce0363cafaff81b0ab7d0d95f10e1b5a280d697d8d1`；行 4，JSON pointer `/`。

**题干**

设 $X\sim B(100,\frac12)$。分别用不带与带连续性修正的中心极限定理近似计算 $P(X\le55)$，并与精确值比较。

**过程**

$\mu=50$,$\sigma=\sqrt{100\times\frac12\times\frac12}=5$。不带修正:$P(X\le55)\approx P(Z\le\frac{55-50}{5})=P(Z\le1)=\Phi(1)\approx0.8413$。带连续性修正:$P(X\le55)=P(X\le55.5)\approx P(Z\le\frac{55.5-50}{5})=P(Z\le1.1)=\Phi(1.1)\approx0.8643$。精确值:$\sum_{k=0}^{55}\binom{100}{k}(\frac12)^{100}\approx0.8644$。可见连续性修正显著改善了近似(不带修正误差约 $0.023$,带修正误差约 $0.0001$)。

**答案原文**

不带修正 $\approx0.841$;带修正 $\approx0.864$;精确值 $\approx0.864$。连续性修正显著改善。

## 23. draft-c28-02

内容 SHA256：`10afff4f64b623b041c364c1f3f59fdb2e37348bacd91ee60f285a548263656b`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-05/draft.jsonl；源 SHA256 `d37d937851dd65a04639ac056400cd3d508fd96a4cbec235d17dd573fb499084`；行 7，JSON pointer `/`。

**题干**

设 $a=(1,2)$，$b=(3,4)$。求以 $a,b$ 为邻边的平行四边形面积；交换两向量的顺序后，二阶行列式如何变化？并解释有向面积的含义。

**过程**

面积 $S=|\det(a,b)|=\begin{vmatrix}1&2\\3&4\end{vmatrix}$ 的绝对值 $=|1\times4-2\times3|=|4-6|=2$。交换顺序后,$\det(b,a)=\begin{vmatrix}3&4\\1&2\end{vmatrix}=3\times2-4\times1=2=-\det(a,b)$,行列式改变符号而绝对值不变,即面积仍为 $2$。有向面积:行列式的符号记录了向量组的定向;$\det(a,b)>0$ 表示 $(a,b)$ 构成逆时针(右手)定向,交换两向量后定向反转,符号变负。

**答案原文**

面积为 $2$;$\det(b,a)=-\det(a,b)$,符号反转、面积不变;符号反映定向。

## 24. draft-c41-04

内容 SHA256：`11705a5e1561f7196903c6a9e1a5038a3b2fad1c24759114f18a026037b36d95`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft.jsonl；源 SHA256 `58ae126d6bd255576c005783f78e6ade29c9f0bd60b1c7fa2e0971ba6cad1a00`；行 9，JSON pointer `/`。

**题干**

求矩阵 $A=\begin{pmatrix}2&1&0\\0&2&1\\0&0&2\end{pmatrix}$ 的若尔当标准形，并求一组广义特征向量构成的变换矩阵 $P$。

**过程**

特征值全为 $2$。令 $N=A-2I=\begin{pmatrix}0&1&0\\0&0&1\\0&0&0\end{pmatrix}$,$N^2=\begin{pmatrix}0&0&1\\0&0&0\\0&0&0\end{pmatrix}$,$N^3=0$。特征子空间 $\ker N=\mathrm{span}\{(1,0,0)\}$,维数 $1$,故只有一个块,即 $J=J_3(2)=A$ 本身。广义特征向量链:取 $v_3=(0,0,1)$(满足 $N^3v_3=0$ 且 $N^2v_3=(1,0,0)\neq0$),则 $v_2=Nv_3=(0,1,0)$,$v_1=N^2v_3=(1,0,0)$。取 $P=(v_1,v_2,v_3)=I$,则 $P^{-1}AP=A=J_3(2)$。

**答案原文**

$J=J_3(2)=A$;广义链 $v_3=(0,0,1),v_2=(0,1,0),v_1=(1,0,0)$,$P=I$。

## 25. draft-c38-04

内容 SHA256：`11a17467a40b17d3e1e9a9f419a38e2d66a359f678cc0d7719643581ab28b412`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft.jsonl；源 SHA256 `2a488597e92f7efdb6ec80074b147c9290e949fbeb4cbd114e293657e7c04776`；行 9，JSON pointer `/`。

**题干**

设 $U,V$ 是 $\mathbb R^5$ 的子空间，$\dim U=3$，$\dim V=2$。求 $\dim(U\cap V)$ 的可能取值范围，并说明每种取值对应的 $\dim(U+V)$。

**过程**

由维数公式 $\dim(U+V)=\dim U+\dim V-\dim(U\cap V)=5-\dim(U\cap V)$。而 $U+V\subseteq\mathbb R^5$,故 $\dim(U+V)\le5$,即 $\dim(U\cap V)\ge0$;又 $\dim(U\cap V)\le\min(\dim U,\dim V)=2$。故 $\dim(U\cap V)$ 的可能取值为 $0,1,2$,对应的 $\dim(U+V)$ 分别为 $5,4,3$。三种情形均可实现:直和(交为 $0$)、交一条直线、$V\subseteq U$(交为 $V$)。

**答案原文**

$\dim(U\cap V)\in\{0,1,2\}$,对应 $\dim(U+V)=5,4,3$。

## 26. calc-series-018

内容 SHA256：`136259a704756b904a6bb7599fd78462f3f2e9ac06d97185c4ec2beb134f67da`。

来源：dataset_calc.json；源 SHA256 `3c3498a772d278ee41f25e5a66d8cdeac85901bbdbc71d407952ddf9e52d929d`；行 —，JSON pointer `/16`。

**题干**

已知级数 $\sum_{n=1}^{\infty} \frac{x^n}{n}$ 在 $(-1, 1)$ 内收敛，求其和函数，并求该级数逐项求导和逐项积分后的结果。

**过程**

和函数 $S(x) = -\ln(1-x)$。逐项求导：$S'(x) = \sum_{n=1}^{\infty} x^{n-1} = \frac{1}{1-x}$。逐项积分：$\int_0^x S(t) dt = \sum_{n=1}^{\infty} \frac{x^{n+1}}{n(n+1)} = (1-x)\ln(1-x) + x$。

**答案原文**

和函数 $S(x) = -\ln(1-x)$，逐项求导得 $\frac{1}{1-x}$，逐项积分得 $(1-x)\ln(1-x) + x$

## 27. draft-c16-03

内容 SHA256：`1490ff0f96e49a7207a876d8016029b80fdb15bac0b37e10405c70dee517652d`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft.jsonl；源 SHA256 `afcd74e3e4d285e77802f29ab182f9dce80cfe5833b983feb8af34694ed15331`；行 13，JSON pointer `/`。

**题干**

求异面直线 $l_1$：$x$ 轴 与 $l_2$：过点 $(0,1,1)$、方向 $(0,1,0)$ 的公垂线方程、两个垂足与两直线间的距离。

**过程**

$l_1$ 参数化 $(t,0,0)$，$l_2$ 参数化 $(0,1+s,1)$。方向向量 $d_1=(1,0,0),d_2=(0,1,0)$，公垂线方向 $n=d_1\times d_2=(0,0,1)$。设垂足 $A=(t,0,0)$，$B=(0,1+s,1)$，则 $B-A=(-t,1+s,1)$ 应平行于 $n$，故 $-t=0$ 且 $1+s=0$，得 $t=0,s=-1$。垂足为 $A=(0,0,0)$，$B=(0,0,1)$，公垂线为 $z$ 轴：$\{(0,0,z)\}$。距离 $|AB|=1$。(亦可用公式验证:$|[d_1,d_2,P_2-P_1]|/|d_1\times d_2|$,混合积绝对值为 $1$。)

**答案原文**

公垂线为 $z$ 轴 $\{(0,0,z)\}$;垂足 $(0,0,0)$ 与 $(0,0,1)$;距离为 $1$。

## 28. draft-c09-04

内容 SHA256：`14b33caa5321cf47fe5e02580dc4004ba1e2c4ef7c962a7ffef7715e27d54db2`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft-codex-repair-v1.jsonl；源 SHA256 `66ac9042539d8a2289eb561d2f48019e4d2bbe55dc2a7900d84710f602077689`；行 14，JSON pointer `/`。

**题干**

矩形$[0,1]\times[0,2]$绕直线$y=h$旋转，$h\in\mathbb R$。求体积关于$h$的完整分段表达式及所有使体积最小的轴位置。

**过程**

纵截面与$x$无关，实体轴向长度为$1$。若$0\le h\le2$，轴穿过或触及矩形，截面为半径$\max(h,2-h)=1+|h-1|$的圆盘，体积为$\pi(1+|h-1|)^2$。若$h\le0$，为圆环，平方差$(2-h)^2-h^2=4(1-h)$；若$h\ge2$，平方差$h^2-(h-2)^2=4(h-1)$。两外侧可合写$4\pi|h-1|$；在$h=0,2$与圆盘公式同为$4\pi$。内区间公式唯一在$h=1$取最小值$\pi$，外区间体积不小于$4\pi$。因此全局唯一最优轴为$y=1$，最小体积为$\pi$。

**答案原文**

$V(h)=\begin{cases}\pi(1+|h-1|)^2,&0\le h\le2,\\4\pi|h-1|,&h<0\text{或}h>2.\end{cases}$ 唯一最小轴$y=1$，$V_{\min}=\pi$。

## 29. draft-c47-05

内容 SHA256：`14dcb36daa8e76241a603ecfec76f0c7e6e1b20d2b94a0ecd1fd82d4c7bf0aed`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft.jsonl；源 SHA256 `bcd6ec3d0204b822f83440669662afcfe3ec7712fa4806d51506f98cb797b0c2`；行 5，JSON pointer `/`。

**题干**

设 $X\sim B(50,\frac{1}{50})$。分别用精确公式与泊松近似计算 $P(X\le2)$，并比较两者。

**过程**

精确值:$P(X\le2)=p_0+p_1+p_2$,其中 $p_0=0.98^{50}\approx0.3642$;$p_1=50\times\frac{1}{50}\times0.98^{49}=0.98^{49}\approx0.3716$;$p_2=\binom{50}{2}(\frac{1}{50})^2 0.98^{48}=1225\times\frac{1}{2500}\times0.98^{48}\approx0.1858$。故精确值 $\approx0.3642+0.3716+0.1858=0.9216$。泊松近似:$\lambda=1$,$P(X\le2)\approx e^{-1}(1+1+\frac12)=2.5e^{-1}\approx2.5\times0.3679=0.9197$。两者相差约 $0.002$,相对误差约 $0.2\%$。

**答案原文**

精确值 $\approx0.922$;泊松近似 $\approx0.920$;相对误差约 $0.2\%$。

## 30. draft-c33-04

内容 SHA256：`1619d2845acf4b2cc502d92e2031ac353d6ba035291b46b7b114b0bdc932be57`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft.jsonl；源 SHA256 `71d46f404c59db6194494bf8ea2353202b77f602a15522f58c1b4599d1cbb07a`；行 9，JSON pointer `/`。

**题干**

求矩阵 $A=\begin{pmatrix}1&0\\0&1\\1&1\end{pmatrix}$ 的一个左逆与矩阵 $B=\begin{pmatrix}1&0&1\\0&1&1\end{pmatrix}$ 的一个右逆，并说明这两种单边逆的区别与不唯一性。

**过程**

$A$ 为 $3\times2$ 列满秩矩阵。取 $L=\begin{pmatrix}1&0&0\\0&1&0\end{pmatrix}$，则 $LA=\begin{pmatrix}1&0\\0&1\end{pmatrix}=I_2$，故 $L$ 是 $A$ 的一个左逆。$B$ 为 $2\times3$ 行满秩矩阵。取 $R=\begin{pmatrix}1&0\\0&1\\0&0\end{pmatrix}$，则 $BR=\begin{pmatrix}1&0\\0&1\end{pmatrix}=I_2$，故 $R$ 是 $B$ 的一个右逆。区别:列满秩的「高瘦」矩阵只可能有左逆($LA=I$),行满秩的「宽扁」矩阵只可能有右逆($BR=I$);只有方阵且可逆时才存在同时满足两侧的双边逆。不唯一性:$A$ 的左逆一般形式为 $\begin{pmatrix}1-t&-t&t\\-s&1-s&s\end{pmatrix}$($t,s$ 为任意实数),$L$ 对应 $t=s=0$,$\begin{pmatrix}0&-1&1\\1&2&-1\end{pmatrix}$ 对应 $t=1,s=-1$,也是左逆;$B$ 的右逆同理不唯一。

**答案原文**

$L=\begin{pmatrix}1&0&0\\0&1&0\end{pmatrix}$ 是 $A$ 的左逆;$R=\begin{pmatrix}1&0\\0&1\\0&0\end{pmatrix}$ 是 $B$ 的右逆;左逆只存在于列满秩高瘦矩阵,右逆只存在于行满秩宽扁矩阵,均不唯一。

## 31. draft-c30-03

内容 SHA256：`17f7946521135b82bc9a69aa5b390ba0660016cbb8ce5dd5bf3429634f591174`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft.jsonl；源 SHA256 `4a8930a557e05b01cec58257879ecd5bd9679b9c08e3e478767c363642ebe382`；行 13，JSON pointer `/`。

**题干**

用二项式定理将 $f(x)=x^4$ 按 $x-1$ 的幂展开。

**过程**

$x^4=[(x-1)+1]^4=\sum_{k=0}^{4}\binom{4}{k}(x-1)^k\cdot1^{4-k}=\binom{4}{0}+\binom{4}{1}(x-1)+\binom{4}{2}(x-1)^2+\binom{4}{3}(x-1)^3+\binom{4}{4}(x-1)^4$。二项式系数为 $1,4,6,4,1$，故 $x^4=(x-1)^4+4(x-1)^3+6(x-1)^2+4(x-1)+1$。

**答案原文**

$x^4=(x-1)^4+4(x-1)^3+6(x-1)^2+4(x-1)+1$。

## 32. draft-c53-02

内容 SHA256：`181d3c33850941915bf897768493bc1d671be69e3eb24b08802e51308daf55a9`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-18/draft.jsonl；源 SHA256 `6f921b08949f3ee7aaa95ce0363cafaff81b0ab7d0d95f10e1b5a280d697d8d1`；行 7，JSON pointer `/`。

**题干**

抛两枚均匀硬币。用互斥事件的拆分与可加性求「至少一枚正面朝上」的概率。

**过程**

样本空间 $\Omega=\{HH,HT,TH,TT\}$,四个基本事件互斥且概率各为 $\frac14$。事件 $A=$「至少一枚正面」$=\{HH,HT,TH\}$,由(有限)可加性,$P(A)=P(HH)+P(HT)+P(TH)=\frac14+\frac14+\frac14=\frac34$。

**答案原文**

$P(A)=\frac34$。

## 33. draft-c38-01

内容 SHA256：`1859984199e444ba9898931e68e7908fb54843786581a4bf033f505b73cb5d7e`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft.jsonl；源 SHA256 `2a488597e92f7efdb6ec80074b147c9290e949fbeb4cbd114e293657e7c04776`；行 6，JSON pointer `/`。

**题干**

设 $W_1=\mathrm{span}\{(1,0,0),(0,1,0)\}$，$W_2=\mathrm{span}\{(0,0,1)\}$。求 $\dim(W_1+W_2)$ 与 $\dim(W_1\cap W_2)$，并判断该和是否为直和。

**过程**

$W_1\cap W_2=\{0\}$(两子空间的生成元合在一起为 $(1,0,0),(0,1,0),(0,0,1)$,线性无关)。故 $\dim(W_1\cap W_2)=0$,$\dim(W_1+W_2)=2+1-0=3$,且 $W_1+W_2=\mathbb R^3$。由于 $W_1\cap W_2=\{0\}$,该和为直和:$W_1\oplus W_2=\mathbb R^3$。

**答案原文**

$\dim(W_1+W_2)=3$,$\dim(W_1\cap W_2)=0$,是直和。

## 34. draft-c32-04

内容 SHA256：`19a225ff4eb408c5ba1f728e051570631695b0a4d0389bf46982cb55bdd5776c`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft.jsonl；源 SHA256 `e019465093b291bd83fb6ae20f3eefc40a96df3e5137a246ad8813dd03f87b34`；行 14，JSON pointer `/`。

**题干**

讨论方程组 $\begin{cases}x+y=1\\ 2x+2y=a\end{cases}$ 的解随参数 $a$ 的变化。

**过程**

系数矩阵 $A=\begin{pmatrix}1&1\\2&2\end{pmatrix}$,秩为 $1$;增广矩阵 $\begin{pmatrix}1&1&1\\2&2&a\end{pmatrix}$。当 $a=2$ 时,两方程成比例(同一条直线),增广矩阵秩为 $1=$ 系数矩阵秩,且 $1<2$(未知量个数),方程组有无穷多解:$x+y=1$。当 $a\neq2$ 时,增广矩阵秩为 $2>$ 系数矩阵秩 $1$,方程组无解(两条平行直线)。

**答案原文**

$a=2$ 时无穷多解($x+y=1$);$a\neq2$ 时无解(平行直线)。

## 35. draft-c42-03

内容 SHA256：`1a9f9a034893f0807ca58c064290e5f94c8406c9b3c875177f76971fc4d9af1a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft.jsonl；源 SHA256 `58ae126d6bd255576c005783f78e6ade29c9f0bd60b1c7fa2e0971ba6cad1a00`；行 13，JSON pointer `/`。

**题干**

判断矩阵 $A=\frac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$ 是否为正交矩阵；若是，判断它对应的正交变换是旋转还是反射。

**过程**

$A^{\mathsf T}A=\frac12\begin{pmatrix}1&1\\1&-1\end{pmatrix}\begin{pmatrix}1&1\\1&-1\end{pmatrix}=\frac12\begin{pmatrix}2&0\\0&2\end{pmatrix}=I$,故 $A$ 是正交矩阵。$\det A=\frac12((-1)-1)=-1$,故对应的正交变换是反射(二维正交变换中,行列式为 $+1$ 的是旋转,$-1$ 的是关于过原点直线的反射)。$A$ 的特征值:$\det(A-\lambda I)=(\frac{1}{\sqrt2}-\lambda)(-\frac{1}{\sqrt2}-\lambda)-\frac12=\lambda^2-1$,特征值为 $\pm1$;反射轴为特征值 $1$ 的特征方向,解 $(A-I)v=0$ 得 $v_2=(\sqrt2-1)v_1$,即直线 $y=(\sqrt2-1)x$。

**答案原文**

$A$ 是正交矩阵;$\det A=-1$,对应关于直线 $y=(\sqrt2-1)x$ 的反射。

## 36. draft-c10-05

内容 SHA256：`1b216a5e6628b45a0bb9d4c711c0dca4893a93fd13bb5a2211154c391161f609`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft.jsonl；源 SHA256 `1cc220e2699b799fb9bacc8525e1f9d82321dc39dacd33e5c1caa21c1a7d959b`；行 5，JSON pointer `/`。

**题干**

证明莱布尼茨判别法:若 $a_n$ 单调递减趋于 $0$,则交错级数 $\sum_{n=1}^{\infty}(-1)^{n+1}a_n$ 收敛,且其和 $S$ 满足 $|S-S_N|\le a_{N+1}$。

**过程**

考察偶子列部分和:$S_{2N}=(a_1-a_2)+(a_3-a_4)+\cdots+(a_{2N-1}-a_{2N})$。因 $a_n$ 单调递减,每个括号非负,故 $S_{2N}$ 单调递增;又 $S_{2N}=a_1-(a_2-a_3)-\cdots-(a_{2N-2}-a_{2N-1})-a_{2N}\le a_1$,故 $S_{2N}$ 有上界。单调有界定理:$\lim S_{2N}=S$ 存在。奇子列 $S_{2N+1}=S_{2N}+a_{2N+1}\to S+0=S$,故两子列收敛于同一极限,原级数收敛于 $S$。余项估计:$|S-S_N|\le a_{N+1}$。证明:当 $N$ 为偶数时,$S-S_N=(a_{N+1}-a_{N+2})+(a_{N+3}-a_{N+4})+\cdots\ge0$ 且 $S-S_N\le a_{N+1}$(首个括号之后各项括号非负,逐对减去);当 $N$ 为奇数时,$|S-S_N|=S_N-S=a_{N+1}-(a_{N+2}-a_{N+3})-(a_{N+4}-a_{N+5})-\cdots\le a_{N+1}$(每个括号均非负,从 $a_{N+1}$ 起逐对减去)。故一般地 $|S-S_N|\le a_{N+1}$。

**答案原文**

证明见解法(偶子列单调有界、奇子列同极限;余项 $|S-S_N|\le a_{N+1}$)。

## 37. draft-c52-04

内容 SHA256：`1b932dbe832911ceb1b47dfb7154ba66cca3e9a73e06599e28e6b57065c4040b`。

来源：reviews/codex-supervision/2026-10-05-math-template-followup-v2/batch01-corrected-review-copy-v2.jsonl；源 SHA256 `d0c82fcc9503c4affd525ea22ba1387722b3e3d13ee215592f42e3824642bf42`；行 14，JSON pointer `/`。

**题干**

设 $X\sim U(0,2)$，$Y=\min(X,1)$。求 $Y$ 的分布函数、连续部分的密度、所有概率原子与 $E[Y]$，并说明是否存在通常意义下的概率密度函数。

**过程**

当 $y\leq0$ 时 $F_Y(y)=0$；当 $0<y<1$ 时，$F_Y(y)=P(\min(X,1)\leq y)=P(X\leq y)=\frac{y}{2}$；当 $y\geq1$ 时 $F_Y(y)=1$。故 $Y$ 在 $(0,1)$ 上有连续密度 $f_Y(y)=\frac{1}{2}$，在 $y=1$ 处有概率原子 $P(Y=1)=P(X\geq1)=\frac{1}{2}$。期望：$E[Y]=\int_0^1 y\cdot\frac{1}{2}\,dy+1\cdot\frac{1}{2}=\frac{1}{4}+\frac{1}{2}=\frac{3}{4}$。另一算法(经 $X$ 直接算)：$E[\min(X,1)]=\int_0^2\min(x,1)\cdot\frac{1}{2}\,dx=\frac{1}{2}\left(\int_0^1x\,dx+\int_1^2 1\,dx\right)=\frac{1}{2}\left(\frac{1}{2}+1\right)=\frac{3}{4}$，两法一致。由于 $P(Y=1)=\frac12>0$，整体分布不存在通常的Lebesgue概率密度；其概率测度由连续部分 $\frac12\mathbf1_{(0,1)}(y)\,dy$ 与原子部分 $\frac12\delta_1(dy)$ 构成。

**答案原文**

$F_Y(y)=0\ (y\leq0)$；$F_Y(y)=\frac{y}{2}\ (0<y<1)$；$F_Y(y)=1\ (y\geq1)$。密度:连续部分 $\frac{1}{2}$($0<y<1$)加原子质量 $\frac{1}{2}$ 于 $y=1$。$E[Y]=\frac{3}{4}$。整体没有通常的概率密度函数；分布由上述连续部分和质量 $\frac12$ 的原子组成。

## 38. draft-c19-04

内容 SHA256：`1d086e3a3af7172a58696a53ece69b9750d0265c74aeb48f5af1257b7bc4e04f`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft.jsonl；源 SHA256 `9aa29561a8f8dc1a725169c6fa9b3fb558e5c2bed5b0d43940d42e9b5ff823e3`；行 14，JSON pointer `/`。

**题干**

判断下列方程在空间直角坐标系中表示曲线还是曲面，并说明理由:(1) $x^2+y^2=1$;(2) $\begin{cases}x^2+y^2=1\\ z=0\end{cases}$;(3) $x+y+z=1$;(4) $\begin{cases}x^2+y^2=1\\ z=x\end{cases}$。

**过程**

(1) 曲面:一个方程只约束一个自由度,留下两个自由度($z$ 可任取),是母线平行 $z$ 轴的圆柱面。(2) 曲线:两个方程联立,自由度为 $3-2=1$,是 $xy$ 平面内的单位圆周。(3) 曲面:一个方程,是平面。(4) 曲线:两个独立方程联立(平面 $z=x$ 截圆柱面),是空间中的椭圆。一般地:空间维数为 $3$,一个独立方程给出一张曲面(维数 $2$),两个独立方程联立一般给出一条曲线(维数 $1$),即图形维数 $=$ $3$ $-$ 独立方程数。

**答案原文**

(1) 曲面(圆柱面);(2) 曲线(圆周);(3) 曲面(平面);(4) 曲线(椭圆);理由:方程个数与自由度(3 减方程数)。

## 39. draft-c35-04

内容 SHA256：`1d6eb54de690a9a1c4f9909924ebe4cf3141e2c3f81c1f5ce2eae97a42b9dcd8`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft.jsonl；源 SHA256 `afcd74e3e4d285e77802f29ab182f9dce80cfe5833b983feb8af34694ed15331`；行 4，JSON pointer `/`。

**题干**

用配方法将二次型 $f(x,y,z)=x^2-y^2+2xz+2yz$ 化为标准形，写出可逆线性替换，并求正负惯性指数与秩。

**过程**

先对含 $x$ 的项配方：$x^2+2xz=(x+z)^2-z^2$，于是 $f=(x+z)^2-z^2-y^2+2yz=(x+z)^2-(y^2-2yz+z^2)=(x+z)^2-(y-z)^2$。令 $u=x+z$，$v=y-z$，$w=z$，则标准形为 $u^2-v^2$($w$ 不出现，退化)；反解得线性替换 $x=u-w$，$y=v+w$，$z=w$，系数矩阵 $\begin{pmatrix}1&0&-1\\0&1&1\\0&0&1\end{pmatrix}$ 行列式为 $1$，可逆。正惯性指数 $1$，负惯性指数 $1$，秩 $2$。

**答案原文**

标准形 $u^2-v^2$;替换 $x=u-w,\ y=v+w,\ z=w$;正负惯性指数 $(1,1,0)$,秩 $2$。

## 40. draft-c25-05

内容 SHA256：`1e74cd2b63e0b174c88c659a8c618ca3d64b90f1cc6346b7b2b6d37e5f4fdd68`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft.jsonl；源 SHA256 `25705ed80dbac40074a2bc29ed482de0087b12bc96d3e1ec0cb9f77722fefe0e`；行 10，JSON pointer `/`。

**题干**

求球面 $x^2+y^2+z^2=4$ 与椭圆柱面 $\frac{x^2}{4}+y^2=1$ 的交线的参数方程，说明交线由几支组成、在何处相接，并判断每一支的形状。

**过程**

由椭圆柱面参数化:$x=2\cos t$,$y=\sin t$。代入球面:$z^2=4-x^2-y^2=4-4\cos^2t-\sin^2t=3-3\cos^2t=3\sin^2t$,故 $z=\pm\sqrt3\sin t$。交线两支:$l_1:(2\cos t,\sin t,\sqrt3\sin t)$ 与 $l_2:(2\cos t,\sin t,-\sqrt3\sin t)$。两支在 $\sin t=0$ 处相接,即点 $(2,0,0)$ 与 $(-2,0,0)$。每支的形状:$l_1$ 满足 $z=\sqrt3y$,即位于平面 $z-\sqrt3y=0$ 内;该平面内取坐标 $x=2\cos t$、$s=2\sin t$($y=\frac{s}{2},z=\frac{\sqrt3}{2}s$),满足 $\frac{x^2}{4}+\frac{s^2}{4}=1$,即 $x^2+s^2=4$,是半径为 $2$ 的圆。故每支是平面 $z=\pm\sqrt3y$ 内的圆。

**答案原文**

两支:$(2\cos t,\sin t,\pm\sqrt3\sin t)$,在 $(\pm2,0,0)$ 处相接;每支是平面 $z=\pm\sqrt3y$ 内半径为 $2$ 的圆。

## 41. draft-c35-01

内容 SHA256：`1fadc5bcca6f306c5232bb8f5805ca34f04be83d885bdeaa1c849a0e2a6f92a9`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft.jsonl；源 SHA256 `afcd74e3e4d285e77802f29ab182f9dce80cfe5833b983feb8af34694ed15331`；行 1，JSON pointer `/`。

**题干**

用配方法将二次型 $f(x,y,z)=x^2+4xy+3y^2+z^2$ 化为标准形，写出所用的可逆线性替换，并求其正负惯性指数、秩与正定性。

**过程**

先对含 $x$ 的项配方：$x^2+4xy+3y^2=(x+2y)^2-y^2$，故 $f=(x+2y)^2-y^2+z^2$。令 $u=x+2y$，$v=y$，$w=z$，则 $f=u^2-v^2+w^2$ 为标准形；线性替换为 $x=u-2v$，$y=v$，$z=w$，其系数矩阵 $\begin{pmatrix}1&-2&0\\0&1&0\\0&0&1\end{pmatrix}$ 的行列式为 $1\neq0$，可逆。正惯性指数 $2$，负惯性指数 $1$，秩 $3$。因负惯性指数非零，二次型不定(非正定)。

**答案原文**

标准形 $u^2-v^2+w^2$，替换 $x=u-2v,y=v,z=w$;正惯性指数 $2$，负惯性指数 $1$，秩 $3$，不定。

## 42. linalg-061

内容 SHA256：`2000006c7dee1ef1929e67fe2442d02f38705ce236c05709332c93dcfa4bffdf`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/0d6cf147b00b746ff542224346124229b5a6a8e21516106946a9647b8de43f36.bin；源 SHA256 `0d6cf147b00b746ff542224346124229b5a6a8e21516106946a9647b8de43f36`；行 —，JSON pointer `/13`。

**题干**

在 $\mathbb{R}^2$ 中，已知旧基 $\varepsilon_1=(1,0), \varepsilon_2=(0,1)$，新基 $\eta_1=(1,1), \eta_2=(-1,1)$。求从旧基到新基的过渡矩阵，并求向量 $\alpha=(3,1)$ 在新基下的坐标。

**过程**

过渡矩阵 $P=\begin{pmatrix} 1 & -1 \\ 1 & 1 \end{pmatrix}$。设 $\alpha$ 在新基下的坐标为 $(x_1,x_2)^T$，则 $\begin{pmatrix} 1 & -1 \\ 1 & 1 \end{pmatrix}\begin{pmatrix} x_1 \\ x_2 \end{pmatrix}=\begin{pmatrix} 3 \\ 1 \end{pmatrix}$，展开得方程组 $x_1 - x_2 = 3$，$x_1 + x_2 = 1$，两式相加得 $2x_1 = 4$，故 $x_1 = 2$，回代得 $x_2 = -1$。

**答案原文**

过渡矩阵 $P=\begin{pmatrix} 1 & -1 \\ 1 & 1 \end{pmatrix}$，新坐标 $(2,-1)^T$

## 43. draft-c15-03

内容 SHA256：`209ba4dc738969ac46770373b94af79330c58210892941b101e77ea7c58e0aa4`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft.jsonl；源 SHA256 `9aa29561a8f8dc1a725169c6fa9b3fb558e5c2bed5b0d43940d42e9b5ff823e3`；行 3，JSON pointer `/`。

**题干**

求过点 $P(1,2,3)$、法向量位于 $xz$ 平面内、且与方向为 $(1,1,0)$ 的直线成 $30^\circ$ 角的平面方程。

**过程**

设法向量 $n=(a,0,c)$($a,c$ 不同时为零)。夹角条件:$\sin30^\circ=\frac{|(a,0,c)\cdot(1,1,0)|}{|n|\cdot\sqrt2}=\frac{|a|}{\sqrt{a^2+c^2}\cdot\sqrt2}=\frac12$,平方得 $2a^2=a^2+c^2$,即 $c=\pm a$。取 $a=1$:$n=(1,0,1)$ 或 $(1,0,-1)$。过 $P(1,2,3)$:平面 $1(x-1)+0(y-2)+1(z-3)=0$ 即 $x+z=4$;或 $1(x-1)+0(y-2)-1(z-3)=0$ 即 $x-z=-2$。验证:$n=(1,0,1)$ 与 $(1,1,0)$ 的夹角余弦 $\frac{1}{\sqrt2\sqrt2}=\frac12$,直线与平面夹角确为 $30^\circ$ ✓。

**答案原文**

两个平面:$x+z=4$ 与 $x-z=-2$。

## 44. draft-c16-04

内容 SHA256：`2120992a612a64d7411f284e775acaf96bda13f04f6e79ec736db6bf33fc763d`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft.jsonl；源 SHA256 `afcd74e3e4d285e77802f29ab182f9dce80cfe5833b983feb8af34694ed15331`；行 14，JSON pointer `/`。

**题干**

求两条异面直线 $l_1:(t,t,0)$ 与 $l_2:(s,0,1-s)$ 上动点之间距离的最小值(即两直线间的距离)。

**过程**

两动点分别为 $A=(t,t,0)$ 与 $B=(s,0,1-s)$，距离平方 $|AB|^2=(s-t)^2+t^2+(1-s)^2$。对 $t,s$ 求偏导：$\frac{\partial}{\partial t}=-2(s-t)+2t=4t-2s$，$\frac{\partial}{\partial s}=2(s-t)-2(1-s)=4s-2t-2$。令两者为零，得 $s=2t$ 与 $2s-t=1$，解得 $t=\frac13,s=\frac23$。此时 $|AB|^2=(\frac13)^2+(\frac13)^2+(\frac13)^2=\frac13$，故最小距离为 $\frac{1}{\sqrt3}=\frac{\sqrt3}{3}$。交叉验证(混合积公式)：$d_1=(1,1,0),d_2=(1,0,-1)$，$P_2-P_1=(0,0,1)$，$[d_1,d_2,P_2-P_1]=-1$，$|d_1\times d_2|=\sqrt3$，距离 $\frac{1}{\sqrt3}$，一致。

**答案原文**

最小距离为 $\frac{\sqrt3}{3}$(在 $t=\frac13,s=\frac23$ 处取得)。

## 45. draft-c40-05

内容 SHA256：`213abc12fc464afd98b2b2c2bc4147fb0b101cb918b8d49a0aa546ccd3cca769`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft.jsonl；源 SHA256 `58ae126d6bd255576c005783f78e6ade29c9f0bd60b1c7fa2e0971ba6cad1a00`；行 5，JSON pointer `/`。

**题干**

用初等变换把 λ-矩阵 $A(\lambda)=\begin{pmatrix}\lambda&1\\0&\lambda\end{pmatrix}$ 化为等价标准形 $\mathrm{diag}(1,\lambda^2)$，并说明初等变换为何不改变行列式因子。

**过程**

初等变换:先交换第一、二列,得 $\begin{pmatrix}1&\lambda\\\lambda&0\end{pmatrix}$;再用第一列消去第一行的 $\lambda$(第二列减 $\lambda$ 倍第一列),得 $\begin{pmatrix}1&0\\\lambda&-\lambda^2\end{pmatrix}$;再用第一行消去第二行首项(第二行减 $\lambda$ 倍第一行),得 $\begin{pmatrix}1&0\\0&-\lambda^2\end{pmatrix}$;第二行乘 $-1$ 得 $\begin{pmatrix}1&0\\0&\lambda^2\end{pmatrix}=\mathrm{diag}(1,\lambda^2)$。不变性:三类初等变换(交换、数乘、倍加)对每个 $k$ 阶子式只产生非零常数倍或不变(倍加只把某子式变成自身与其他子式的非零倍之和),故全体 $k$ 阶子式的最大公因式(行列式因子)在等价变换下不变,从而不变因子与初等因子不变。

**答案原文**

等价标准形为 $\mathrm{diag}(1,\lambda^2)$(变换步骤见解法);行列式因子在初等变换下不变。

## 46. draft-c37-05

内容 SHA256：`225174e4349c326c4fefa6245d56c8a1cf970d06d5f8704697499dea91934b8d`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft.jsonl；源 SHA256 `afcd74e3e4d285e77802f29ab182f9dce80cfe5833b983feb8af34694ed15331`；行 10，JSON pointer `/`。

**题干**

证明 $\{1+x+x^2,\ 1-x+x^2,\ x-x^2\}$ 是次数不超过 $2$ 的多项式空间的一组基，并求 $p(x)=x^2$ 在这组基下的坐标。

**过程**

把三个多项式在基 $\{1,x,x^2\}$ 下的坐标按列排列：$M=\begin{pmatrix}1&1&0\\1&-1&1\\1&1&-1\end{pmatrix}$。计算 $\det M=1\times((-1)\times(-1)-1\times1)-1\times(1\times(-1)-1\times1)+0=0-(-2)=2\neq0$，故三个向量线性无关；空间维数为 $3$，故构成一组基。求 $p=x^2$ 的坐标即解 $M\xi=(0,0,1)^{\mathsf T}$。由伴随矩阵法(或消元)得 $M^{-1}=\begin{pmatrix}0&\frac12&\frac12\\1&-\frac12&-\frac12\\1&0&-1\end{pmatrix}$，故 $\xi=M^{-1}(0,0,1)^{\mathsf T}=(\frac12,-\frac12,-1)$。验证:$\frac12(1+x+x^2)-\frac12(1-x+x^2)-(x-x^2)=(\frac12-\frac12)+(\frac x2+\frac x2-x)+(\frac{x^2}2-\frac{x^2}2+x^2)=x^2$。

**答案原文**

三个多项式线性无关(行列式 $2\neq0$),构成一组基;$p=x^2$ 的坐标为 $(\frac12,-\frac12,-1)$。

## 47. draft-c20-04

内容 SHA256：`236e82846759048b17aa84a6ce7fd84771e10c2160336a9cb8edff293ec371e5`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft.jsonl；源 SHA256 `e0eb9bf14b1cdf0919006ede0e9523046d0edadffb69ac3a10e4941a77563756`；行 4，JSON pointer `/`。

**题干**

讨论椭球面 $\frac{x^2}{4}+\frac{y^2}{9}+z^2=1$ 与平面 $z=k$ 的交线:对不同的 $k$ 说明交线是椭圆、一个点还是空集。

**过程**

代入 $z=k$:$\frac{x^2}{4}+\frac{y^2}{9}=1-k^2$。当 $|k|<1$ 时,右端为正,交线是椭圆,半轴为 $2\sqrt{1-k^2}$ 与 $3\sqrt{1-k^2}$。当 $|k|=1$ 时,右端为 $0$,交线退化为一个点 $(0,0,\pm1)$(与椭球相切的截面)。当 $|k|>1$ 时,右端为负,无实解,交线为空集。

**答案原文**

$|k|<1$:椭圆(半轴 $2\sqrt{1-k^2}$、$3\sqrt{1-k^2}$);$|k|=1$:点 $(0,0,\pm1)$;$|k|>1$:空集。

## 48. draft-c14-04

内容 SHA256：`2480ec9da418d80c104f677936acf57b7af4be6aea2d3972a2be0194776acce0`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft.jsonl；源 SHA256 `1cc220e2699b799fb9bacc8525e1f9d82321dc39dacd33e5c1caa21c1a7d959b`；行 14，JSON pointer `/`。

**题干**

将 $f(x)=x$($0\le x<2\pi$)作周期 $2\pi$ 延拓,展开为傅立叶级数,并求级数在 $x=0$ 处的和,与狄利克雷定理核对。

**过程**

$a_0=\frac1\pi\int_0^{2\pi}x\,dx=\frac1\pi\cdot\frac{4\pi^2}{2}=2\pi$。$a_n=\frac1\pi\int_0^{2\pi}x\cos nx\,dx=\frac1\pi\left.\left(\frac{x\sin nx}{n}+\frac{\cos nx}{n^2}\right)\right|_0^{2\pi}=0$。$b_n=\frac1\pi\int_0^{2\pi}x\sin nx\,dx=\frac1\pi\left.\left(-\frac{x\cos nx}{n}+\frac{\sin nx}{n^2}\right)\right|_0^{2\pi}=\frac1\pi\left(-\frac{2\pi}{n}\right)=-\frac2n$。故 $f(x)=\pi-\sum_{n=1}^{\infty}\frac{2}{n}\sin nx$。在 $x=0$ 处,周期延拓后的函数有跳跃:$f(0^+)=0$,$f(0^-)=2\pi$,由狄利克雷定理,级数和为 $\frac{0+2\pi}{2}=\pi$;级数在该点各正弦项 $\sin(n\cdot0)=0$,级数和即常数项 $\pi$,两者一致。

**答案原文**

$f=\pi-\sum_{n=1}^{\infty}\frac{2}{n}\sin nx$;$x=0$ 处级数和为 $\pi$((0+2π)/2,与狄利克雷定理一致)。

## 49. draft-c51-01

内容 SHA256：`24e3edcc2963a4de189622a9ec835e15baf082bf91bc7ece6510a6e77d64428a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft.jsonl；源 SHA256 `71d46f404c59db6194494bf8ea2353202b77f602a15522f58c1b4599d1cbb07a`；行 11，JSON pointer `/`。

**题干**

三台机器 $M_1,M_2,M_3$ 的产量分别占总产量的 $50\%$、$30\%$、$20\%$，次品率分别为 $2\%$、$3\%$、$4\%$。随机抽取一件产品发现是次品，求它分别来自三台机器的概率，并验证三者之和为 $1$。

**过程**

记 $D$ 为抽到次品。$P(D)=\frac12\times\frac{2}{100}+\frac{3}{10}\times\frac{3}{100}+\frac15\times\frac{4}{100}=\frac{1}{100}+\frac{9}{1000}+\frac{8}{1000}=\frac{27}{1000}$。由贝叶斯公式，$P(M_1\mid D)=\frac{\frac12\times\frac{2}{100}}{\frac{27}{1000}}=\frac{10}{27}$，$P(M_2\mid D)=\frac{\frac{3}{10}\times\frac{3}{100}}{\frac{27}{1000}}=\frac{9}{27}=\frac13$，$P(M_3\mid D)=\frac{\frac15\times\frac{4}{100}}{\frac{27}{1000}}=\frac{8}{27}$。验证:$\frac{10}{27}+\frac13+\frac{8}{27}=\frac{10+9+8}{27}=1$。

**答案原文**

$P(M_1\mid D)=\frac{10}{27}$，$P(M_2\mid D)=\frac13$，$P(M_3\mid D)=\frac{8}{27}$;三者之和为 $1$。

## 50. eval-linalg-032-s2

内容 SHA256：`2526bdb37b07e690a84b31fb6bc7520fdf63b777b60eb377f35006b7ea87cb8d`。

来源：reviews/codex-supervision/history-from-code/recheck-68c51be/data/v2/eval/dataset_eval.json；源 SHA256 `1de2df62edd0b01403df813c80edc3a5a9dbf1791f0b223d8e0f107ccee55e6e`；行 —，JSON pointer `/289`。

**题干**

求 λ-矩阵 $A(\lambda)=\begin{pmatrix}\lambda-1&1\\0&\lambda-1\end{pmatrix}$ 的不变因子与初等因子。

**过程**

交换两列：$\begin{pmatrix}1&\lambda-1\\\lambda-1&0\end{pmatrix}$；第二列减第一列的 $(\lambda-1)$ 倍：$\begin{pmatrix}1&0\\\lambda-1&-(\lambda-1)^2\end{pmatrix}$；第二行减第一行的 $(\lambda-1)$ 倍：$\begin{pmatrix}1&0\\0&-(\lambda-1)^2\end{pmatrix}$。Smith 标准形为 $\operatorname{diag}(1,(\lambda-1)^2)$（$-1$ 为单位因子可吸收），不变因子即 $1,(\lambda-1)^2$。

**答案原文**

不变因子 $1,(\lambda-1)^2$；初等因子 $(\lambda-1)^2$

## 51. draft-c33-02

内容 SHA256：`255f3c584c60a7a293c1f0b7d46c73db0e0a515a06623213bbbab1237e9bc15a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft-codex-repair-v1.jsonl；源 SHA256 `24548fa6bd5a758c36b8b41480f4a46047e4aaeeaa18def93a813e72a241c454`；行 7，JSON pointer `/`。

**题干**

求使矩阵 $A=\begin{pmatrix}1&1&a\\1&a&1\a&1&1\end{pmatrix}$ 可逆的参数 $a$ 的取值范围；并求 $a=0$ 时的逆矩阵。

**过程**

计算行列式(按第一行展开)：$\det A=1\times(a\cdot1-1\cdot1)-1\times(1\cdot1-1\cdot a)+a\times(1\cdot1-a\cdot a)=(a-1)-(1-a)+a(1-a^2)=3a-2-a^3=-(a-1)^2(a+2)$。可逆当且仅当 $\det A\neq0$，即 $a\neq1$ 且 $a\neq-2$。当 $a=0$ 时，$A=\begin{pmatrix}1&1&0\\1&0&1\\0&1&1\end{pmatrix}$。由增广矩阵消元(或直接验证)得 $A^{-1}=\frac12\begin{pmatrix}1&1&-1\\1&-1&1\\-1&1&1\end{pmatrix}$。验证:$AA^{-1}=I$。

**答案原文**

可逆当且仅当 $a\neq1$ 且 $a\neq-2$;$a=0$ 时 $A^{-1}=\frac12\begin{pmatrix}1&1&-1\\1&-1&1\\-1&1&1\end{pmatrix}$。

## 52. draft-c26-03

内容 SHA256：`25fb83f186714b0f7c56acb4c0f7f7a30b73ff50de6c450f5926cfaa649f1304`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft.jsonl；源 SHA256 `25705ed80dbac40074a2bc29ed482de0087b12bc96d3e1ec0cb9f77722fefe0e`；行 13，JSON pointer `/`。

**题干**

解释矩阵 $A=\begin{pmatrix}1&-1\\-1&1\end{pmatrix}$ 对应的线性变换的几何作用，并求其核、像与秩。

**过程**

$A(x,y)=(x-y,-x+y)=(x-y)(1,-1)$。记 $v=(1,-1)$,$v\cdot v=2$,$A=vv^{\mathsf T}=2\cdot(\text{到直线 }y=-x\text{ 的正交投影})$(正交投影为 $\frac{(x,y)\cdot v}{v\cdot v}v=\frac{x-y}{2}(1,-1)$,故 $A=2$ 倍投影)。像中的每个向量都是 $(1,-1)$ 的倍数,即像为直线 $y=-x$;核满足 $x-y=0$,即直线 $y=x$。几何上,$A$ 把每个点沿核方向 $(1,1)$ 滑向像直线 $y=-x$ 并放大 $2$ 倍(投影位移 $=-\frac{x+y}{2}(1,1)$)。秩为 $1$,零度为 $1$,且 $A^2=2A\neq A$($A$ 不是幂等的投影本身,而是投影的 $2$ 倍)。

**答案原文**

$A=2$ 倍的到直线 $y=-x$ 的正交投影;核为直线 $y=x$,像为直线 $y=-x$,秩 $1$。

## 53. linalg-052

内容 SHA256：`26dc016ba967225de4e121a4b5e35e1c16769e2d7204664f206ca8d8348e545e`。

来源：reviews/codex-supervision/history-from-code/clone-check/reviews/2026-10-03-prep-recheck/results.json；源 SHA256 `078e6bbd0c76184d36494245ab5fa7c1bbb875cfa226cdcd88c09d9c47c6d3c8`；行 —，JSON pointer `/answer_record_snapshot/linalg-052`。

**题干**

将多项式 $f(x)=x^3$ 在 $x=1$ 处按泰勒公式展开，并说明展开式的意义。

**过程**

对 $f(x)=x^3$ 求导：$f(1)=1$，$f'(1)=3$，$f''(1)=6$，$f'''(1)=6$。代入泰勒公式得 $f(x)=1+3(x-1)+3(x-1)^2+(x-1)^3$。展开式的每一项系数由各阶导数在 $x=1$ 处的值决定。

**答案原文**

$1+3(x-1)+3(x-1)^2+(x-1)^3$；展开式各项系数由各阶导数在 $x=1$ 处的值决定，且三次多项式的三阶泰勒展开与原函数精确相等

## 54. linalg-048

内容 SHA256：`274d4d3e330eefab55536c612c508daafa98216657a743a21b68d5c3d4f21b99`。

来源：reviews/2026-10-06-linalg048-rewrite/linalg-048-rewrite-candidate.json；源 SHA256 `b9c797016f3e4a8d5b736f2ed7f3c0a27fa09c9b2acd6a69038144c17fa534b0`；行 —，JSON pointer `/`。

**题干**

已知矩阵 $A=\begin{pmatrix}1&3\\0&1\end{pmatrix}$，求该矩阵对应的线性变换对二维平面的几何影响。

**过程**

对任意点 $(x,y)$，有 $A\begin{pmatrix}x\\y\end{pmatrix}=\begin{pmatrix}x+3y\\y\end{pmatrix}$：横坐标增加纵坐标的 $3$ 倍，纵坐标不变。标准基向量 $\vec{e_1}=(1,0)$ 保持不变，$\vec{e_2}=(0,1)$ 映射为 $(3,1)$。水平直线 $y=c$ 上每点横坐标增加 $3c$，整体沿 $x$ 轴方向平移 $3c$，仍是水平直线；竖直直线 $x=c$ 映射为过 $(c,0)$、斜率为 $\frac{1}{3}$ 的直线（参数化为 $(c+3y,\,y)$，即 $x=c+3y$）。单位正方形 $[0,1]^2$ 映射为顶点 $(0,0)$、$(1,0)$、$(3,1)$、$(4,1)$ 的平行四边形，底边长为 $1$、高为 $1$，面积仍为 $1$。行列式 $\det A=1\times 1-3\times 0=1$，与面积不变一致。该变换称为水平剪切（shear）：$x$ 轴上每点不动，离 $x$ 轴越远的点沿 $x$ 方向平移越远。

**答案原文**

水平剪切：每个点的横坐标增加其纵坐标的 $3$ 倍、纵坐标不变；水平直线整体平移、竖直直线倾斜，面积保持不变（行列式为 $1$）。

## 55. geom-031

内容 SHA256：`27cbac9ef7fcc02799c30421ccf41f2d7b3cc3823b391eb3360d3b62acda1fd8`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/4040cba8ea52c8cbdd833485a2c2e61e48130c9cb118d9a07ab2cf8821ef9142.bin；源 SHA256 `4040cba8ea52c8cbdd833485a2c2e61e48130c9cb118d9a07ab2cf8821ef9142`；行 12，JSON pointer `/`。

**题干**

求球面 $x^2+y^2+z^2=4a^2$ 与圆柱面 $x^2+y^2=2ax$ 的交线（维维安尼曲线）的参数方程（$a>0$）。

**过程**

令 $x=a(1+\cos t)$，$y=a\sin t$，则 $x^2+y^2 = a^2(1+\cos t)^2 + a^2\sin^2 t = 2a^2(1+\cos t) = 2a\cdot a(1+\cos t) = 2ax$，圆柱面方程自动满足。代入球面方程 $x^2+y^2+z^2=4a^2$ 得 $z^2 = 4a^2 - 2a^2(1+\cos t) = 2a^2(1-\cos t) = 4a^2\sin^2\frac{t}{2}$。取连续参数分支 $z = 2a\sin\frac{t}{2}$（另一分支 $z = -2a\sin\frac{t}{2}$ 由参数平移 $2\pi$ 覆盖，不另取）。于是交线的参数方程为 $x=a(1+\cos t)$，$y=a\sin t$，$z=2a\sin\frac{t}{2}$，其中 $0 \le t \le 4\pi$ 覆盖整条曲线（$0 \le t \le 2\pi$ 仅覆盖上半部分）。

**答案原文**

维维安尼曲线，参数方程为 $x=a(1+\cos t)$，$y=a\sin t$，$z=2a\sin(t/2)$，其中 $0 \le t \le 4\pi$

## 56. draft-c45-03

内容 SHA256：`2847398eb2f2855bae8412a3a5606d0b5fd077261ae42025a0925870f8f9093e`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft-codex-repair-v1.jsonl；源 SHA256 `1210a0d4288d903b6e805927ec85df226f6ed425240f4fc99a45890c1a184b41`；行 13，JSON pointer `/`。

**题干**

独立地抛两枚公平硬币。记 $A=${第一枚正面},$B=${第二枚正面},$C=${两枚同面}。证明 $A,B,C$ 两两独立但整体不独立。

**过程**

$P(A)=P(B)=P(C)=\frac12$。$P(A\cap B)=P(\text{两枚皆正})=\frac14=P(A)P(B)$ ✓。$P(A\cap C)=P(A\cap\text{两枚同面})=P(\text{两枚皆正})=\frac14=P(A)P(C)$ ✓。$P(B\cap C)=\frac14=P(B)P(C)$ ✓。故两两独立。但 $P(A\cap B\cap C)=P(\text{两枚皆正})=\frac14\neq\frac18=P(A)P(B)P(C)$,故整体不独立。

**答案原文**

两两独立($P(A\cap B)=P(A\cap C)=P(B\cap C)=\frac14$),但 $P(A\cap B\cap C)=\frac14\neq\frac18$,整体不独立。

## 57. draft-c10-04

内容 SHA256：`2903ede9c9a5be411780accdb99c8c7cc9e900f391e4e3efd70f3aa50b5a4cd6`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft.jsonl；源 SHA256 `1cc220e2699b799fb9bacc8525e1f9d82321dc39dacd33e5c1caa21c1a7d959b`；行 4，JSON pointer `/`。

**题干**

用交错级数余项估计,求级数 $\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n}$ 的和的近似值,使误差小于 $\frac{1}{10}$。

**过程**

莱布尼茨型交错级数的余项估计:$|R_N|=|S-S_N|\le a_{N+1}=\frac{1}{N+1}$。要求 $\frac{1}{N+1}<\frac{1}{10}$,即 $N+1>10$,$N\ge10$,故取前 $10$ 项。$S_{10}=1-\frac12+\frac13-\frac14+\frac15-\frac16+\frac17-\frac18+\frac19-\frac{1}{10}$。通分(公分母 $2520$):分子 $=2520-1260+840-630+504-420+360-315+280-252=1627$,故 $S_{10}=\frac{1627}{2520}\approx0.6456$。所以 $S\approx0.646$,误差小于 $0.1$(实际 $S=\ln2\approx0.6931$,实际误差 $\approx0.05$ 满足要求)。

**答案原文**

取前 $10$ 项,$S_{10}=\frac{1627}{2520}\approx0.646$,误差小于 $\frac{1}{10}$。

## 58. draft-c44-01

内容 SHA256：`297ebfa1163aef5c5327668c2e543815cb63383f5f00d9ce421b946d3583e99e`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft.jsonl；源 SHA256 `b92648645c3b17a796e6b8938f67de934cddafd0cf192ab24ae006e5b423e27f`；行 6，JSON pointer `/`。

**题干**

设 $\mathbb R^2$ 上的辛形式为 $\omega(u,v)=u_1v_2-u_2v_1$。验证剪切矩阵 $A=\begin{pmatrix}1&2\\0&1\end{pmatrix}$ 保持 $\omega$。

**过程**

对任意 $u,v$,$\omega(Au,Av)=\det(Au,Av)$(二维情形 $\omega$ 就是行列式)。由行列式乘法性质,$\det(Au,Av)=\det A\cdot\det(u,v)=\det A\cdot\omega(u,v)$。而 $\det A=1\times1-2\times0=1$,故 $\omega(Au,Av)=\omega(u,v)$。即剪切矩阵保持辛形式——二维辛变换恰为保面积(行列式为 $1$)的线性变换。

**答案原文**

剪切矩阵保持 $\omega$(二维辛 = 保面积,$\det A=1$)。

## 59. draft-c46-04

内容 SHA256：`2a85dcffdd4d30b2b1c129f4fa7f3828b5af04cc8300dfaac8f661e9c2e6a435`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-06.jsonl；源 SHA256 `756525876eec2bd8dbc8d8f3e28afbf61ca70fd4cab235964621646009a7ae5f`；行 14，JSON pointer `/`。

**题干**

判断如下取点法是否在单位圆盘 $x^2+y^2\le1$ 内均匀分布:取独立随机变量 $U,V\sim U(0,1)$,令 $R=U$,$\Theta=2\pi V$,取点 $(R\cos\Theta,R\sin\Theta)$。若不均匀,说明原因并给出修正。

**过程**

由$U,V$独立，$R$与$\Theta$独立，角密度为$1/(2\pi)$。若$R=U$，则$f_{R,\Theta}(r,\theta)=1/(2\pi)$（$0<r<1,0<\theta<2\pi$）。面积元$dx\,dy=r\,dr\,d\theta$，故圆盘内的平面密度为$f_{X,Y}(x,y)=1/(2\pi\sqrt{x^2+y^2})$（$0<x^2+y^2<1$），并非常数。也有$P(R\le1/2)=1/2\ne1/4$，与面积比例矛盾。若改为$R=\sqrt U$，则$F_R(r)=r^2$、$f_R(r)=2r$（$0<r<1$），联合密度为$r/\pi$；除以雅可比$r$，得到$f_{X,Y}(x,y)=1/\pi$（$x^2+y^2<1$，边界与原点取值可任定），盘外为零。因此修正方案确在单位圆盘内均匀分布。

**答案原文**

不均匀(径向密度 $f_R(r)=1$ 导致中心过密,$P(R\le\frac12)=\frac12\neq\frac14$);修正:取 $R=\sqrt U$。

## 60. draft-c35-02

内容 SHA256：`2a91f8ad412765eed1d7c54adeaa1dbd31a058c66c509709a2ae037b2ef40622`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft.jsonl；源 SHA256 `afcd74e3e4d285e77802f29ab182f9dce80cfe5833b983feb8af34694ed15331`；行 2，JSON pointer `/`。

**题干**

求二次型 $f(x,y)=x^2+4xy+2y^2$ 的合同标准形与对应矩阵的相似标准形，并说明两者所记录的信息有何不同。

**过程**

合同标准形(配方)：$f=(x+2y)^2-2y^2$，令 $u=x+2y,v=y$，得 $u^2-2v^2$;再作伸缩 $\tilde u=u,\tilde v=\sqrt2v$，得合同标准形 $u^2-v^2$(规范形)，正负惯性指数为 $(1,1,0)$。相似标准形(特征值)：对应矩阵 $A=\begin{pmatrix}1&2\\2&2\end{pmatrix}$，特征方程 $|A-\lambda I|=(1-\lambda)(2-\lambda)-4=\lambda^2-3\lambda-2=0$，特征值 $\lambda=\frac{3\pm\sqrt{17}}{2}$，相似标准形为 $\begin{pmatrix}\frac{3+\sqrt{17}}{2}&0\\0&\frac{3-\sqrt{17}}{2}\end{pmatrix}$。区别:合同标准形只记录二次型的符号结构(惯性指数),相似标准形记录线性变换的全部特征值;合同变换一般改变特征值,相似变换一般改变二次型的系数。

**答案原文**

合同标准形 $u^2-v^2$,惯性指数 $(1,1,0)$;相似标准形 $\mathrm{diag}(\frac{3+\sqrt{17}}{2},\frac{3-\sqrt{17}}{2})$。合同记符号,相似记特征值,两者信息不同。

## 61. draft-c11-01

内容 SHA256：`2ca10c0bfda6e8aa4daab9373ea045620ea2c8ce9d22e874282dcba1d2672d5e`。

来源：reviews/codex-supervision/2026-10-05-batch02-progress-review/batch02-corrected-review-copy.jsonl；源 SHA256 `45bcbf3d65252c02777c6594a401b0409c2a943fd03ee597825e8d38dccb4b79`；行 1，JSON pointer `/`。

**题干**

求幂级数 $\sum_{n=1}^{\infty}\left(\frac{n}{n+1}\right)^{n^2}x^n$ 的收敛域。

**过程**

令 $a_n=(\frac{n}{n+1})^{n^2}$。根值极限 $\lim_{n\to\infty}a_n^{1/n}=\exp(\lim_{n\to\infty}n\ln(1-\frac1{n+1}))=e^{-1}$，所以收敛半径 $R=e$。端点 $x=\pm e$ 的通项绝对值为 $\exp(n^2\ln(1-\frac1{n+1})+n)$。由 $\ln(1-v)=-v-\frac{v^2}{2}+O(v^3)$，其指数为 $n-\frac{n^2}{n+1}-\frac{n^2}{2(n+1)^2}+O(\frac1n)\to1-\frac12=\frac12$。通项绝对值趋于 $e^{1/2}\ne0$，两端点均发散。因此收敛域为 $(-e,e)$。

**答案原文**

收敛域为 $(-e,e)$。

## 62. linalg-057

内容 SHA256：`2d742084bd6574532d43c3b576d6a4aaf13f895cf5bf81d2bc405caaa3fe3851`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/0d6cf147b00b746ff542224346124229b5a6a8e21516106946a9647b8de43f36.bin；源 SHA256 `0d6cf147b00b746ff542224346124229b5a6a8e21516106946a9647b8de43f36`；行 —，JSON pointer `/9`。

**题干**

已知矩阵 $A=\begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}$，求其逆矩阵，并说明可逆性的几何意义。

**过程**

计算 $\det(A)=2\times1-1\times1=1\neq0$，矩阵可逆。$A^{-1}=\frac{1}{1}\begin{pmatrix} 1 & -1 \\ -1 & 2 \end{pmatrix}=\begin{pmatrix} 1 & -1 \\ -1 & 2 \end{pmatrix}$。几何上，可逆意味着该线性变换不将空间压缩到更低维度，存在逆变换将空间恢复。

**答案原文**

$A^{-1}=\begin{pmatrix} 1 & -1 \\ -1 & 2 \end{pmatrix}$

## 63. draft-c24-04

内容 SHA256：`2e453f5ff7cfbe881e9bfbd2141d5f3abc27d562d214eca2ed426a2f1598191d`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft.jsonl；源 SHA256 `25705ed80dbac40074a2bc29ed482de0087b12bc96d3e1ec0cb9f77722fefe0e`；行 4，JSON pointer `/`。

**题干**

求单位圆 $x^2+y^2=1$ 在仿射变换 $\begin{cases}x'=2x+y\\ y'=y\end{cases}$ 下的像曲线方程，并判断其类型。

**过程**

变换矩阵 $A=\begin{pmatrix}2&1\\0&1\end{pmatrix}$,$\det A=2\neq0$,可逆,$A^{-1}=\begin{pmatrix}\frac12&-\frac12\\0&1\end{pmatrix}$。反解:$x=\frac{x'-y'}{2}$,$y=y'$。代入圆的方程:$\left(\frac{x'-y'}{2}\right)^2+y'^2=1$,即 $(x'-y')^2+4y'^2=4$,展开得 $x'^2-2x'y'+5y'^2=4$。二次型矩阵 $\begin{pmatrix}1&-1\\-1&5\end{pmatrix}$ 的顺序主子式为 $1>0$ 与 $4>0$,正定,故像曲线为椭圆。

**答案原文**

像曲线为椭圆:$x'^2-2x'y'+5y'^2=4$。

## 64. draft-c11-02

内容 SHA256：`2e8bc2c7fdd513e61a1a12268f8b0782275cd34cb29b8e24b5a9c00095026b37`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-02.jsonl；源 SHA256 `286625ebf0f88cca49b14f36be4bab4e5f3b29ecc0764226b7ebb5fb61a16527`；行 2，JSON pointer `/`。

**题干**

求幂级数 $\sum_{n=1}^{\infty}\frac{x^n}{\sqrt{n}}$ 的收敛域。

**过程**

当 $|x|<1$ 时，$\lim_{n\to\infty}\left|\frac{x^{n+1}/\sqrt{n+1}}{x^n/\sqrt{n}}\right|=|x|\lim_{n\to\infty}\sqrt{\frac{n}{n+1}}=|x|<1$，级数绝对收敛。当 $x=1$ 时，级数为 $\sum_{n=1}^{\infty}\frac{1}{\sqrt{n}}$，是 $p=\frac12$ 的 $p$ 级数，发散。当 $x=-1$ 时，级数为 $\sum_{n=1}^{\infty}\frac{(-1)^n}{\sqrt{n}}$，$\frac{1}{\sqrt{n}}$ 单调递减趋于 $0$，由莱布尼茨判别法收敛。故收敛域为 $[-1,1)$。

**答案原文**

收敛域为 $[-1,1)$(左端点条件收敛,右端点发散)。

## 65. draft-c51-05

内容 SHA256：`2f0efc77aca08d8c334f8b4cf30f625105603dce3ff1dafb6c516248a7e3d776`。

来源：reviews/codex-supervision/2026-10-05-batch02-progress-review/batch02-corrected-review-copy.jsonl；源 SHA256 `45bcbf3d65252c02777c6594a401b0409c2a943fd03ee597825e8d38dccb4b79`；行 15，JSON pointer `/`。

**题干**

设 $H$ 与 $\bar H$ 为互斥且穷尽的假设，观测 $D_1,D_2$ 在给定 $H$(及给定 $\bar H$)下条件独立。假设$0<P(H)<1$，且$P(D_i\mid H)>0$、$P(D_i\mid\bar H)>0$（$i=1,2$），以保证条件概率及有限优势比有定义。证明后验优势比可写成先验优势比与两个似然比的乘积，并说明更新顺序不影响最终后验；再用两次独立阳性检测的数据($P(H)=\frac{1}{1000}$，灵敏度与误报率均为 $\frac{99}{100}$ 与 $\frac{1}{100}$)验证所得后验为 $\frac{363}{400}$。

**过程**

由贝叶斯公式与条件独立性，$\frac{P(H\mid D_1,D_2)}{P(\bar H\mid D_1,D_2)}=\frac{P(H)}{P(\bar H)}\cdot\frac{P(D_1\mid H)}{P(D_1\mid\bar H)}\cdot\frac{P(D_2\mid H)}{P(D_2\mid\bar H)}$。乘积形式对 $D_1,D_2$ 对称，故更新顺序不影响最终后验优势比。验证:先验优势比 $\frac{P(H)}{P(\bar H)}=\frac{1}{999}$;每次阳性的似然比 $\frac{99/100}{1/100}=99$。两次阳性后，后验优势比 $=\frac{1}{999}\times99^2=\frac{9801}{999}=\frac{363}{37}$，故后验概率 $=\frac{363}{363+37}=\frac{363}{400}$，与逐次更新结果一致。

**答案原文**

证明见解法(乘积形式);验证:$P(H\mid +_1,+_2)=\frac{363}{400}$。

## 66. draft-c20-05

内容 SHA256：`2ff4bfa51b6385548a8ecc3b167a236c875a187f0c6970aa27ccc0b9b5d1bfdf`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft.jsonl；源 SHA256 `e0eb9bf14b1cdf0919006ede0e9523046d0edadffb69ac3a10e4941a77563756`；行 5，JSON pointer `/`。

**题干**

用正交变换(旋转)判断方程 $x^2+2xy+y^2+z=0$ 表示的曲面类型。

**过程**

交叉项部分 $x^2+2xy+y^2=(x+y)^2$。作正交变换 $u=\frac{x+y}{\sqrt2}$,$v=\frac{-x+y}{\sqrt2}$,$w=z$(变换矩阵 $\begin{pmatrix}\frac1{\sqrt2}&\frac1{\sqrt2}&0\\-\frac1{\sqrt2}&\frac1{\sqrt2}&0\\0&0&1\end{pmatrix}$ 为正交矩阵且行列式为 $1$,是绕 $z$ 轴的真旋转),则 $x^2+2xy+y^2=2u^2$,方程化为 $2u^2+w=0$,即 $w=-2u^2$。这是母线沿 $v$ 方向的抛物柱面。

**答案原文**

抛物柱面(旋转变换后 $w=-2u^2$,母线沿 $v=\frac{-x+y}{\sqrt2}$ 方向)。

## 67. draft-c47-01

内容 SHA256：`3089f4ec645405fbc80bde6349f119f11dbb37468c1491e18073dfa20e8c1435`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft.jsonl；源 SHA256 `bcd6ec3d0204b822f83440669662afcfe3ec7712fa4806d51506f98cb797b0c2`；行 1，JSON pointer `/`。

**题干**

某彩票单张中奖率为 $\frac{1}{1000}$。某人购买 $2000$ 张(设各张彩票是否中奖相互独立)，用泊松近似求他恰中 $3$ 次奖的概率。

**过程**

中奖次数 $X\sim B(2000,\frac{1}{1000})$,$n$ 大 $p$ 小,$\lambda=np=2000\times\frac{1}{1000}=2$。泊松近似:$P(X=3)\approx e^{-2}\frac{2^3}{3!}=e^{-2}\times\frac{8}{6}=e^{-2}\times\frac{4}{3}\approx0.1353\times\frac{4}{3}\approx0.1804$。

**答案原文**

$P(X=3)\approx e^{-2}\frac{2^3}{3!}=\frac{4}{3}e^{-2}\approx0.180$。

## 68. calc-series-015

内容 SHA256：`30a983d98d5562172958730d7e43f316e47fe8cce86a1c5b8b3844049b916fa6`。

来源：reviews/codex-supervision/2026-10-06-scene-repair-takeover/math-correction-receipt.json；源 SHA256 `33c0a0bc6bc5281f513bf17fdda3de2a178f4700b9703bdcce7465e7cbcc0ef9`；行 —，JSON pointer `/corrections/0/record`。

**题干**

讨论级数 $\sum_{n=1}^{\infty} \frac{(-1)^n}{\sqrt{n}}$ 的敛散性，并指出是绝对收敛还是条件收敛。

**过程**

设 $u_n=1/\sqrt n$，则 $u_{n+1}\le u_n$ 且 $\lim_{n\to\infty}u_n=0$。由莱布尼茨判别法，$\sum_{n=1}^{\infty}(-1)^n u_n$ 收敛。若和为 $S$、前 $N$ 项和为 $S_N$，则 $|S-S_N|\le 1/\sqrt{N+1}$。绝对值级数满足 $\sum_{n=1}^{N}1/\sqrt n\ge\int_1^{N+1}x^{-1/2}\,dx=2(\sqrt{N+1}-1)\to+\infty$，即 $p=\frac{1}{2}\le1$ 的 $p$ 级数发散。因此原级数条件收敛。

**答案原文**

条件收敛

## 69. draft-c09-01

内容 SHA256：`31d178164f3e68415ba23d6fa17478d146aaa58db13e8713a10cb5cad991a175`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft.jsonl；源 SHA256 `1d0950f73fad698178bef910eec1c19d5303cfe6bdabbcd76bddab903f05e44b`；行 11，JSON pointer `/`。

**题干**

求由曲线 $y=\sqrt{x}$、直线 $x=4$ 与 $x$ 轴围成的图形绕 $x$ 轴旋转所得旋转体的体积。

**过程**

圆盘法:旋转半径为 $R(x)=\sqrt{x}$,$0\le x\le4$。$V=\pi\int_0^4R(x)^2\,dx=\pi\int_0^4x\,dx=\pi\left.\frac{x^2}{2}\right|_0^4=8\pi$。

**答案原文**

体积为 $8\pi$。

## 70. draft-c12-05

内容 SHA256：`3595cb54d708c732a7085059b06e26051787effb42ce6a902c77e1ab00cc65ae`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft.jsonl；源 SHA256 `1cc220e2699b799fb9bacc8525e1f9d82321dc39dacd33e5c1caa21c1a7d959b`；行 10，JSON pointer `/`。

**题干**

证明函数列 $f_n(x)=n^2x(1-x^2)^n$($0\le x\le1$)逐点收敛于 $0$，但 $\int_0^1f_n(x)\,dx$ 不趋于 $0$；由此说明逐点收敛不足以保证极限与积分交换，并指出一致收敛为何是充分条件。

**过程**

逐点收敛:当 $x=0$ 时 $f_n(0)=0$;当 $0<x\le1$ 时,$f_n(x)=n^2x(1-x^2)^n$,$0\le1-x^2<1$,指数衰减快于多项式增长,故 $f_n(x)\to0$。积分:换元 $u=1-x^2$,$du=-2x\,dx$,$\int_0^1f_n(x)\,dx=\frac{n^2}{2}\int_0^1u^n\,du=\frac{n^2}{2(n+1)}\to+\infty$。而 $\int_0^1\lim f_n\,dx=0$,故极限与积分不能交换。原因:该函数列不一致收敛(若一致收敛于 $0$,则 $\sup|f_n|$ 应趋于 $0$;计算 $f_n$ 在 $x=\frac{1}{\sqrt{2n+1}}$ 处取值约为 $\frac{n^2}{\sqrt{2n+1}}e^{-\frac12}\to\infty$,故 $\sup|f_n|\to\infty$,不一致)。一致收敛是逐项积分/交换极限的充分条件:一致收敛保证 $\left|\int f_n-\int f\right|\le\int|f_n-f|\le\sup|f_n-f|\cdot(b-a)\to0$。

**答案原文**

$f_n\to0$ 逐点,但 $\int_0^1f_n=n^2/(2(n+1))\to+\infty\neq0$;该函数列不一致收敛($\sup|f_n|\to\infty$),一致收敛是交换的充分条件(证明见解法)。

## 71. syn-eval-ok / syn-train-001

内容 SHA256：`35a6ee1ba88e9d912bd4d0e2faea8cc386df3db6111c4783310d46f3c07ce1c8`。

来源：reviews/codex-supervision/history-from-code/pytest-68c51be/test_candidate_quarantine_keep0/candidate.jsonl；源 SHA256 `254eaaf3799a1f5e8dc6a71b72602979a8454a4012fcda34dc6221d5938bc754`；行 1，JSON pointer `/`。

**题干**

合成评测题目B（完全独立）：求 2×3 的值。

**过程**

2×3=6。

**答案原文**

6

## 72. draft-c20-03

内容 SHA256：`360509f42a85046eb985349f12cd1561100246608657c119db66f48542ab65df`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft.jsonl；源 SHA256 `e0eb9bf14b1cdf0919006ede0e9523046d0edadffb69ac3a10e4941a77563756`；行 3，JSON pointer `/`。

**题干**

讨论方程 $x^2+y^2-z^2=a$ 随参数 $a$ 变化所表示的曲面类型。

**过程**

当 $a>0$ 时,化为 $\frac{x^2}{a}+\frac{y^2}{a}-\frac{z^2}{a}=1$,是单叶双曲面。当 $a=0$ 时,$x^2+y^2-z^2=0$,即 $z^2=x^2+y^2$,是圆锥面(退化情形)。当 $a<0$ 时,令 $b=-a>0$,$\frac{z^2}{b}-\frac{x^2}{b}-\frac{y^2}{b}=1$,是双叶双曲面。

**答案原文**

$a>0$:单叶双曲面;$a=0$:圆锥面(退化);$a<0$:双叶双曲面。

## 73. draft-c30-05

内容 SHA256：`3772656f4783cc85115dac1d030577a7a0266def5960bb4327c107bd4f12e46e`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft.jsonl；源 SHA256 `4a8930a557e05b01cec58257879ecd5bd9679b9c08e3e478767c363642ebe382`；行 15，JSON pointer `/`。

**题干**

写出 $f(x)=\ln x$ 在 $x=1$ 处的幂级数展开的前四项，并讨论其收敛范围；再与多项式(如 $x^4$)的平移展开对照，说明两者在项数与适用范围上的区别。

**过程**

令 $u=x-1$，$\ln x=\ln(1+u)=u-\frac{u^2}{2}+\frac{u^3}{3}-\frac{u^4}{4}+\cdots$，即 $\ln x=(x-1)-\frac{(x-1)^2}{2}+\frac{(x-1)^3}{3}-\frac{(x-1)^4}{4}+\cdots$。收敛范围:该级数在 $|u|<1$ 收敛，即 $0<x<2$;$u=1$(即 $x=2$)时级数为交错调和级数，条件收敛，故 $0<x\leq2$;其余 $x$ 发散。对照:多项式 $x^4$ 的平移展开 $(x-1)^4+4(x-1)^3+\cdots$ 只有有限项,且对一切实数恒等成立;而 $\ln x$ 的展开有无穷多项,只在收敛域 $0<x\leq2$ 内成立。区别的根源:多项式展开是有限次恒等变形,超越函数展开是无穷级数,其有效性受收敛半径限制。

**答案原文**

$\ln x=(x-1)-\frac{(x-1)^2}{2}+\frac{(x-1)^3}{3}-\frac{(x-1)^4}{4}+\cdots$,收敛于 $0<x\leq2$;多项式展开有限且处处恒等,级数展开无穷且仅限收敛域。

## 74. linalg-048

内容 SHA256：`3a9c15738bca3748c426e7d2e57d6a67eb773d60f2d6f464a5a2e097ea8b375e`。

来源：reviews/codex-supervision/2026-10-06-holdout-strict-fix/old-script-reproduction/fixture-corrupt-published.json；源 SHA256 `4270a2c360779c5db5f1a7a1457b90afab5e88ae1d04a02019a4d4c0ea089553`；行 —，JSON pointer `/`。

**题干**

已知矩阵 $A=\begin{pmatrix}1&9\\0&1\end{pmatrix}$，求该矩阵对应的线性变换对二维平面的几何影响。

**过程**

对任意点 $(x,y)$，有 $A\begin{pmatrix}x\\y\end{pmatrix}=\begin{pmatrix}x+3y\\y\end{pmatrix}$：横坐标增加纵坐标的 $3$ 倍，纵坐标不变。标准基向量 $\vec{e_1}=(1,0)$ 保持不变，$\vec{e_2}=(0,1)$ 映射为 $(3,1)$。水平直线 $y=c$ 上每点横坐标增加 $3c$，整体沿 $x$ 轴方向平移 $3c$，仍是水平直线；竖直直线 $x=c$ 映射为过 $(c,0)$、斜率为 $\frac{1}{3}$ 的直线（参数化为 $(c+3y,\,y)$，即 $x=c+3y$）。单位正方形 $[0,1]^2$ 映射为顶点 $(0,0)$、$(1,0)$、$(3,1)$、$(4,1)$ 的平行四边形，底边长为 $1$、高为 $1$，面积仍为 $1$。行列式 $\det A=1\times 1-3\times 0=1$，与面积不变一致。该变换称为水平剪切（shear）：$x$ 轴上每点不动，离 $x$ 轴越远的点沿 $x$ 方向平移越远。

**答案原文**

水平剪切：每个点的横坐标增加其纵坐标的 $3$ 倍、纵坐标不变；水平直线整体平移、竖直直线倾斜，面积保持不变（行列式为 $1$）。

## 75. eval-linalg-031-s1

内容 SHA256：`3b90e2995889478ca674ef32468971178b40aab84364019c90eadca8c42cd8df`。

来源：reviews/codex-supervision/history-from-code/recheck-68c51be/data/v2/eval/dataset_eval.json；源 SHA256 `1de2df62edd0b01403df813c80edc3a5a9dbf1791f0b223d8e0f107ccee55e6e`；行 —，JSON pointer `/285`。

**题干**

求矩阵 $A=\begin{pmatrix}2&1&0\\0&2&1\\0&0&2\end{pmatrix}$ 的最小多项式与若尔当标准形。

**过程**

特征多项式 $|\lambda I-A|=(\lambda-2)^3$。$A-2I=\begin{pmatrix}0&1&0\\0&0&1\\0&0&0\end{pmatrix}=:N$，$N\ne 0$ 且 $N^2=\begin{pmatrix}0&0&1\\0&0&0\\0&0&0\end{pmatrix}\ne 0$，$N^3=0$。因 $(A-2I)\ne 0$、$(A-2I)^2\ne 0$，低次多项式 $\lambda-2$ 与 $(\lambda-2)^2$ 都不能使 $A$ 消去，故最小多项式为 $(\lambda-2)^3$。

**答案原文**

最小多项式 $(\lambda-2)^3$；若尔当标准形为 $A$ 本身（单个三阶块 $J_3(2)$）

## 76. draft-c08-05

内容 SHA256：`3c58948ee499b9b6d546f16cfc75262ee22015b686b697a0e43131a6bc50ff04`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft.jsonl；源 SHA256 `1d0950f73fad698178bef910eec1c19d5303cfe6bdabbcd76bddab903f05e44b`；行 10，JSON pointer `/`。

**题干**

推导参数曲线 $\begin{cases}x=x(t)\\ y=y(t)\end{cases}$ 的面积公式,并分别说明简单闭曲线、$y$ 变号的图线、自交曲线三种情形下绝对值应放在哪里;再举一反例说明简单闭曲线为何不能分段取绝对值。

**过程**

微元:沿曲线切片,面积微元为 $|y|\,dx=|y(t)x'(t)|\,dt$,带符号量 $y(t)x'(t)\,dt$ 的符号由曲线走向与 $y$ 的符号共同决定。情形一(简单闭曲线,不自交):两半支的带符号积分必须相加——它们的部分抵消恰好「剩出」内部面积,整圈积分后取一次绝对值即得面积:$A=\left|\int_{\alpha}^{\beta}y(t)x'(t)\,dt\right|$(格林公式:正向时 $\oint_L y\,dx=-\text{面积}$)。情形二(曲线为 $x$ 的图线且 $y$ 变号):在被积函数上取绝对值,$A=\int_{\alpha}^{\beta}\left|y(t)x'(t)\right|dt$,等价于在 $y=0$ 处分段分别取绝对值。情形三(自交曲线,如 $8$ 字形):先拆成若干简单圈,逐圈按情形一取绝对值后相加:$A=\sum_k\left|\oint_{L_k}y\,x'\,dt\right|$。反例(简单闭曲线不能分段取绝对值):圆 $x=\cos t$,$y=2+\sin t$($t\in[0,2\pi]$,圆心 $(0,2)$ 半径 $1$)。整圈积分 $\int_0^{2\pi}(2+\sin t)(-\sin t)\,dt=\int_0^{2\pi}(-2\sin t-\sin^2t)\,dt=0-\pi=-\pi$,面积 $|-\pi|=\pi$ ✓。若错误地在 $x'=0$(即 $t=0,\pi$)处拆成两段分别取绝对值:第一段 $\int_0^{\pi}y\,x'\,dt=-4-\frac{\pi}{2}$,第二段 $\int_{\pi}^{2\pi}y\,x'\,dt=4-\frac{\pi}{2}$,错误结果 $|-4-\frac{\pi}{2}|+|4-\frac{\pi}{2}|=8\neq\pi$。

**答案原文**

规则:$A=\left|\int_{\alpha}^{\beta}yx'\,dt\right|$(简单闭曲线,整圈一次绝对值);$A=\int_{\alpha}^{\beta}|yx'|\,dt$($y$ 变号图线);$A=\sum_k\left|\oint_{L_k}yx'\,dt\right|$(自交曲线逐圈)。反例:$x=\cos t,y=2+\sin t$ 的圆,分段取绝对值得 $8\neq\pi$,证明简单闭曲线不可分段取绝对值。

## 77. draft-c18-04

内容 SHA256：`3d26050d07f29bafb6bb419cc328ade9ad1ebf5a7489f5c967957dbc64b03dd9`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft.jsonl；源 SHA256 `4a8930a557e05b01cec58257879ecd5bd9679b9c08e3e478767c363642ebe382`；行 9，JSON pointer `/`。

**题干**

求点 $P(1,0,0)$ 到直线 $l:\begin{cases}x+y+z=1\\ x-y+2z=0\end{cases}$(两平面交线)的距离与垂足。

**过程**

直线方向 $d=n_1\times n_2=(1,1,1)\times(1,-1,2)=(1\times2-1\times(-1),\,1\times1-1\times2,\,1\times(-1)-1\times1)=(3,-1,-2)$。取 $z=0$ 解 $\begin{cases}x+y=1\\x-y=0\end{cases}$ 得直线上一点 $P_0=(\frac12,\frac12,0)$。设垂足 $Q=P_0+td$，由 $(Q-P)\cdot d=0$：$(-\frac12+3t,\, \frac12-t,\,-2t)\cdot(3,-1,-2)=-\frac32+9t-\frac12+t+4t=-2+14t=0$，得 $t=\frac17$。垂足 $Q=(\frac12+\frac37,\,\frac12-\frac17,\,-\frac27)=(\frac{13}{14},\frac{5}{14},-\frac27)$。距离 $|P-Q|=|(-\frac{1}{14},\frac{5}{14},-\frac{4}{14})|=\frac{\sqrt{1+25+16}}{14}=\frac{\sqrt{42}}{14}$。(交叉验证:$|(P-P_0)\times d|/|d|=\sqrt3/\sqrt{14}=\sqrt{42}/14$。)

**答案原文**

距离为 $\frac{\sqrt{42}}{14}$;垂足为 $(\frac{13}{14},\frac{5}{14},-\frac27)$。

## 78. draft-c51-02

内容 SHA256：`3d45da2bb579168af702065181c348add171e2384e31b86dda89deb6230463f7`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-02.jsonl；源 SHA256 `286625ebf0f88cca49b14f36be4bab4e5f3b29ecc0764226b7ebb5fb61a16527`；行 12，JSON pointer `/`。

**题干**

说明「独立」与「条件独立」互不蕴含：构造一个例子说明两个事件条件独立但(无条件)不独立；再构造一个例子说明两个事件独立但给定第三个事件后条件不独立。

**过程**

例一：以概率$\frac12$选择双正面或双反面硬币，令$K$为硬币种类，$A,B$分别为两次出现正面的事件。给定$K=\mathrm{HH}$时$P(A\mid K)=P(B\mid K)=P(A\cap B\mid K)=1$，给定$K=\mathrm{TT}$时均为$0$，两种条件下均有条件联合概率等于边缘概率乘积；但无条件$P(A\cap B)=\frac12\ne\frac14=P(A)P(B)$。例二：独立均匀硬币抛两次，令$A$为第二次正面，$B$为两次相同，$C$为第一次正面。无条件$P(A)=P(B)=\frac12$、$P(A\cap B)=\frac14$，故独立；给定$C$时，$P(A\cap B\mid C)=\frac12\ne\frac14=P(A\mid C)P(B\mid C)$，故不条件独立。

**答案原文**

例一:双面硬币袋中随机取一枚抛两次,$A,B$ 给定硬币条件独立但无条件不独立;例二:均匀硬币抛两次,$A$={第二次正}、$B$={两次相同}、$C$={第一次正},$A,B$ 独立但给定 $C$ 条件不独立。

## 79. draft-c17-04

内容 SHA256：`3e0e81bb72769cee035cd3725726e286438a0f6ba12f7fca214221712e391539`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft.jsonl；源 SHA256 `9aa29561a8f8dc1a725169c6fa9b3fb558e5c2bed5b0d43940d42e9b5ff823e3`；行 9，JSON pointer `/`。

**题干**

写出过直线 $l:\begin{cases}x+y+z=1\\ x-y+2z=0\end{cases}$ 的平面束方程，并求其中过点 $P(1,1,1)$ 的平面。

**过程**

过交线的平面束:$(x+y+z-1)+\lambda(x-y+2z)=0$($\lambda$ 为参数;注意 $\lambda$ 取遍实数时给出过 $l$ 的除 $x-y+2z=0$ 外的一切平面)。代入 $P(1,1,1)$:$(1+1+1-1)+\lambda(1-1+2)=0$,即 $2+2\lambda=0$,$\lambda=-1$。故所求平面为 $(x+y+z-1)-(x-y+2z)=0$,即 $2y-z-1=0$。验证:$P$ 满足 $2-1-1=0$ ✓;直线 $l$ 上点满足两原方程,故也满足其线性组合,平面过 $l$ ✓。

**答案原文**

平面束:$(x+y+z-1)+\lambda(x-y+2z)=0$;过 $P$ 的平面为 $2y-z-1=0$(对应 $\lambda=-1$)。

## 80. draft-c36-02

内容 SHA256：`3eadcff79439dc98d507525cc20e96e6085ba9e40d8a13e3fd5f75dc830e77f9`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft.jsonl；源 SHA256 `13fe6a370d3c46ae8ca6c1b16c9cd98fbedcc8648087f11a70ff046951db5479`；行 7，JSON pointer `/`。

**题干**

用特征值方法判断二次型 $f(x,y,z)=2x^2+2y^2+2z^2-2xy-2yz$ 是否正定。

**过程**

二次型对应矩阵 $A=\begin{pmatrix}2&-1&0\\-1&2&-1\\0&-1&2\end{pmatrix}$。计算特征多项式:令 $u=2-\lambda$,则 $|A-\lambda I|=u(u^2-1)-u=u(u^2-2)=(2-\lambda)\left[(2-\lambda)^2-2\right]$,故特征值为 $\lambda=2$ 与 $\lambda=2\pm\sqrt{2}$,即 $2-\sqrt{2}$、$2$、$2+\sqrt{2}$(亦可由三对角对称矩阵特征值公式 $\lambda_k=2-2\cos\frac{k\pi}{4}$ 直接得出,结果一致)。三个特征值全部为正,故二次型正定。

**答案原文**

正定(特征值为 $2-\sqrt{2}$、$2$、$2+\sqrt{2}$，全正)。

## 81. prob-042

内容 SHA256：`40bf81b9432c5868ce8aeb1f13009115113fb4eaa025e6849f353510daea69f9`。

来源：reviews/codex-supervision/2026-10-06-scene-repair-takeover/math-correction-receipt.json；源 SHA256 `33c0a0bc6bc5281f513bf17fdda3de2a178f4700b9703bdcce7465e7cbcc0ef9`；行 —，JSON pointer `/corrections/6/record`。

**题干**

设 $X_1,X_2,\ldots$ 独立同分布，$P(X_i=1)=p$、$P(X_i=0)=1-p$，其中 $0\le p\le1$。令正面频率 $F_n=n^{-1}\sum_{i=1}^nX_i$。精确求 $E(F_n)$、$\operatorname{Var}(F_n)$，并用切比雪夫不等式证明 $F_n\xrightarrow{P}p$；说明公平硬币附加条件对应的 $p$。

**过程**

设各次投掷独立同分布，$X_i\sim\operatorname{Bernoulli}(p)$，其中 $p=P(X_i=1)$，$0\le p\le1$；题目未指定公平性，不能直接令 $p=\frac{1}{2}$。正面频率为 $F_n=\frac{1}{n}\sum_{i=1}^n X_i$。由独立性，$E(F_n)=p$，$\operatorname{Var}(F_n)=p(1-p)/n$。对任意 $\varepsilon>0$，$P(|F_n-p|\ge\varepsilon)\le\frac{p(1-p)}{n\varepsilon^2}\to0$，故 $F_n\xrightarrow{P}p$。若另有公平硬币条件，才取 $p=\frac{1}{2}$。

**答案原文**

$F_n\xrightarrow{P}p$，其中 $p$ 为单次正面概率；公平硬币时 $p=\frac{1}{2}$。

## 82. draft-c12-03

内容 SHA256：`41833f5e4d700f310f6e9f9e7e054d089c07b8c5ba8daa4d624c4b05222ddb72`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft.jsonl；源 SHA256 `1cc220e2699b799fb9bacc8525e1f9d82321dc39dacd33e5c1caa21c1a7d959b`；行 8，JSON pointer `/`。

**题干**

讨论函数项级数 $\sum_{n=1}^{\infty}\frac{x^n}{n}$ 在 $[0,r]$($0<r<1$)上的一致收敛性，并说明其在 $[0,1)$ 上不一致收敛。

**过程**

在 $[0,r]$ 上,$\left|\frac{x^n}{n}\right|\le\frac{r^n}{n}\le r^n$,而 $\sum r^n$ 收敛($0<r<1$),由 $M$ 判别法一致收敛。在 $[0,1)$ 上,尾项 $\sum_{k=N+1}^{\infty}\frac{x^k}{k}$ 关于 $x$ 递增(各项系数为正),其关于 $x$ 的上确界为 $\sup_{x\in[0,1)}\sum_{k=N+1}^{\infty}\frac{x^k}{k}=\lim_{x\to1^-}\sum_{k=N+1}^{\infty}\frac{x^k}{k}=\sum_{k=N+1}^{\infty}\frac1k$(在 $[0,1)$ 内不被任何点取到,由极限给出)。调和级数尾部发散,故 $\sup$ 为 $+\infty$ 不趋于 $0$,不一致收敛。

**答案原文**

在 $[0,r]$($0<r<1$)上一致收敛;在 $[0,1)$ 上不一致收敛。

## 83. draft-c52-05

内容 SHA256：`424df8d0ad8a07b14e6af81d2131a8026b4e6fe82ec22999125723841563d3af`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft-codex-repair-v1.jsonl；源 SHA256 `5103259cb6bddac12992e1fa2076c11a2d8620040cb2501441190d2add0775eb`；行 15，JSON pointer `/`。

**题干**

设随机变量 $X$ 的分布函数 $F$ 连续，在某区间 $I$ 上严格递增，且 $P(X\in I)=1$、$F(I)=(0,1)$。证明 $Y=F(X)\sim U(0,1)$。再设目标随机变量 $Z$ 的密度为 $g(z)=\begin{cases}\frac12,&0<z<1\\ z-1,&1<z<2\\0,&\text{其余}\end{cases}$。给定 $U\sim U(0,1)$，构造 $Z=T(U)$，写出完整分布函数并验证其分布；说明为何 $T$ 必须分段。

**过程**

对 $0<y<1$，由假设，$F$ 在 $I$ 上存在反函数 $F_I^{-1}$。除零概率事件外，$F(X)\le y$ 等价于 $X\le F_I^{-1}(y)$，所以 $P(Y\le y)=F(F_I^{-1}(y))=y$；$y\le0$ 时概率为 $0$，$y\ge1$ 时为 $1$，故 $Y\sim U(0,1)$。目标密度非负，且 $\int_0^1\frac12\,dz+\int_1^2(z-1)\,dz=\frac12+\frac12=1$。积分得 $G(z)=\begin{cases}0,&z\le0\frac z2,&0<z\le1\frac12+\frac{(z-1)^2}{2},&1<z<2\\1,&z\ge2\end{cases}$，在 $z=1$ 连续，$G(1)=\frac12$。两段 CDF 的反函数分别为 $T(u)=2u$（$0<u\le\frac12$）与 $T(u)=1+\sqrt{2u-1}$（$\frac12<u<1$）。令 $Z=T(U)$。若 $0<z\le1$，事件 $T(U)\le z$ 等价于 $U\le z/2$，概率为 $z/2$；若 $1<z<2$，等价于 $U\le\frac12+\frac{(z-1)^2}{2}$，概率为该阈值。外侧概率分别为 $0$ 和 $1$，所以构造确有 CDF $G$。密度在单点 $z=1$ 的取值不影响分布；此处 CDF 无跳跃、没有原子。逆映射在 $u=\frac12$ 处分段，因为目标 CDF 的两段表达式不同，不能以一个线性或幂函数代替全部分支。

**答案原文**

$Y\sim U(0,1)$；$Z=T(U)$，其中 $T(u)=\begin{cases}2u,&0<u\le\frac12\\1+\sqrt{2u-1},&\frac12<u<1\end{cases}$。完整 CDF：$G(z)=0$（$z\le0$）、$z/2$（$0<z\le1$）、$\frac12+\frac{(z-1)^2}{2}$（$1<z<2$）、$1$（$z\ge2$）。

## 84. draft-c52-03

内容 SHA256：`43a733778615c47e32f86b8d3aab0067bdf701a7ae5cacbaf4d35f3dff8ebfbd`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft.jsonl；源 SHA256 `13fe6a370d3c46ae8ca6c1b16c9cd98fbedcc8648087f11a70ff046951db5479`；行 13，JSON pointer `/`。

**题干**

设随机变量 $X$ 服从区间 $(-1,2)$ 上的均匀分布，求 $Y=X^2$ 的概率密度函数，并指出密度分段的分界点。

**过程**

$X$ 的密度为 $\frac{1}{3}$($-1<x<2$)。$Y=X^2$ 的值域为 $(0,4)$。当 $0<y<1$ 时，$[-\sqrt{y},\sqrt{y}]\subset(-1,2)$，故 $F_Y(y)=P(X^2\leq y)=\frac{2\sqrt{y}}{3}$，$f_Y(y)=\frac{1}{3\sqrt{y}}$。当 $1\leq y<4$ 时，区间 $[-\sqrt{y},\sqrt{y}]$ 与支持集 $(-1,2)$ 的交为 $[-1,\sqrt{y}]$，故 $F_Y(y)=\frac{\sqrt{y}+1}{3}$，$f_Y(y)=\frac{1}{6\sqrt{y}}$。分界点为 $y=1$，两侧密度在该点有跳跃。验证总质量：$\int_0^1\frac{1}{3\sqrt{y}}\,dy+\int_1^4\frac{1}{6\sqrt{y}}\,dy=\frac{2}{3}+\frac{1}{3}=1$。

**答案原文**

$f_Y(y)=\frac{1}{3\sqrt{y}}$(当 $0<y<1$)；$f_Y(y)=\frac{1}{6\sqrt{y}}$(当 $1\leq y<4$)；其余为 $0$。分界点 $y=1$。

## 85. draft-c28-01

内容 SHA256：`43deededaf1fd834712df6ef9b185297151f5b39f41f58dcd25b91d3c34670b5`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-05.jsonl；源 SHA256 `6eabbb3d46a7d6a4b39d563a7fc339d117b2be8533dce70e0a85bf2963570f0e`；行 6，JSON pointer `/`。

**题干**

求由向量 $a=(1,1,0)$，$b=(0,1,1)$，$c=(1,0,1)$ 张成的平行六面体的体积。

**过程**

三向量张成的平行六面体体积等于以它们为行(或列)的三阶行列式的绝对值。$\begin{vmatrix}1&1&0\\0&1&1\\1&0&1\end{vmatrix}=1\times(1\times1-1\times0)-1\times(0\times1-1\times1)+0=1-(-1)=2$。故体积为 $|2|=2$。

**答案原文**

体积为 $2$。

## 86. draft-c37-03

内容 SHA256：`43df33a2ea068f4ca4504a6cfe91982aa6925008efeb9ce700e2835172cb591d`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-03.jsonl；源 SHA256 `ed738d83f3c59a525f3119c56735aac4bcc4b50ddf4817701a786e7b1e3c9e5d`；行 8，JSON pointer `/`。

**题干**

在 $\mathbb R^2$ 中，设从标准基到基 $\eta_1=(1,1)$，$\eta_2=(1,-1)$ 的过渡矩阵为 $P$。求 $P$；若向量 $\alpha$ 在基 $\eta$ 下的坐标为 $(2,3)$，求 $\alpha$ 在标准基下的坐标；若向量 $\beta$ 在标准基下的坐标为 $(2,3)$，求 $\beta$ 在基 $\eta$ 下的坐标。

**过程**

约定基矩阵 $B_\eta=B_\varepsilon P$，$P$的第$j$列为$[\eta_j]_\varepsilon$，故$[v]_\varepsilon=P[v]_\eta$、$[v]_\eta=P^{-1}[v]_\varepsilon$；换基改变坐标，不改变向量$v$。过渡矩阵 $P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$。由 $P^2=\begin{pmatrix}2&0\\0&2\end{pmatrix}=2I$ 得 $P^{-1}=\frac12P=\frac12\begin{pmatrix}1&1\\1&-1\end{pmatrix}$。$\alpha$ 在标准基下的坐标(基向量按新坐标组合)：$\alpha=2\eta_1+3\eta_2=2(1,1)+3(1,-1)=(5,-1)$。$\beta$ 在基 $\eta$ 下的坐标：$\xi=P^{-1}\beta=\frac12(2+3,\,2-3)=(\frac52,-\frac12)$。验证:$\frac52\eta_1-\frac12\eta_2=(\frac52-\frac12,\frac52+\frac12)=(2,3)=\beta$。注意:向量本身用 $P$ 组合,坐标换基用 $P^{-1}$,方向相反。

**答案原文**

$P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$;$\alpha$ 在标准基下为 $(5,-1)$;$\beta$ 在基 $\eta$ 下为 $(\frac52,-\frac12)$。

## 87. draft-c33-05

内容 SHA256：`44bc8638d9228a16de67a81b7ef9fa776a29cd8fa6bb71fcafb74e1a870f83d1`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-02.jsonl；源 SHA256 `286625ebf0f88cca49b14f36be4bab4e5f3b29ecc0764226b7ebb5fb61a16527`；行 10，JSON pointer `/`。

**题干**

求矩阵 $A=\begin{pmatrix}1&a&a^2\\0&1&a\\0&0&1\end{pmatrix}$ 的逆矩阵，并说明 $A$ 对一切实数 $a$ 可逆。

**过程**

令 $N=\begin{pmatrix}0&1&0\\0&0&1\\0&0&0\end{pmatrix}$，则 $N^2=\begin{pmatrix}0&0&1\\0&0&0\\0&0&0\end{pmatrix}$，$N^3=0$(幂零)，且 $A=I+aN+a^2N^2$。对幂零矩阵有 $(I+M)^{-1}=I-M+M^2-M^3+\cdots$(级数有限终止)。令 $M=aN+a^2N^2$，则 $M^2=a^2N^2$，$M^3=0$，故 $A^{-1}=I-M+M^2=I-aN-a^2N^2+a^2N^2=I-aN=\begin{pmatrix}1&-a&0\\0&1&-a\\0&0&1\end{pmatrix}$。验证:$AA^{-1}=I$。可逆性:$A$ 为上三角矩阵,$\det A=1\neq0$,与 $a$ 无关,故对一切实数 $a$ 可逆。

**答案原文**

$A^{-1}=\begin{pmatrix}1&-a&0\\0&1&-a\\0&0&1\end{pmatrix}$;$\det A=1\neq0$,对一切实数 $a$ 可逆。

## 88. linalg-060

内容 SHA256：`458e4e3531b2344006d2f9c06d28015fe274d13c3ee896ff68fe6732eb85cb25`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/0d6cf147b00b746ff542224346124229b5a6a8e21516106946a9647b8de43f36.bin；源 SHA256 `0d6cf147b00b746ff542224346124229b5a6a8e21516106946a9647b8de43f36`；行 —，JSON pointer `/12`。

**题干**

判断二次型 $f(x,y,z)=x^2+2y^2+3z^2+2xy+2xz$ 是否正定。

**过程**

写出对应的实对称矩阵 $A=\begin{pmatrix} 1 & 1 & 1 \\ 1 & 2 & 0 \\ 1 & 0 & 3 \end{pmatrix}$。顺序主子式：$1>0$，$\begin{vmatrix} 1 & 1 \\ 1 & 2 \end{vmatrix}=1>0$，$\det(A)=1(6-0)-1(3-0)+1(0-2)=6-3-2=1>0$。所有顺序主子式均为正，故二次型正定。

**答案原文**

正定

## 89. draft-c05-04

内容 SHA256：`45a6ee8573bfe60327afd5a0fe49bff4c291a4253a3e08fe313139451e0afc4b`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-06/draft.jsonl；源 SHA256 `2685493ba0765d9a8d1f8a1be3e55595e83614f9d6861bc1b87c95e2d4aad8df`；行 9，JSON pointer `/`。

**题干**

求 $\lim_{x\to+\infty}\frac{x^3}{e^x}$ 与 $\lim_{x\to+\infty}\frac{\ln x}{\sqrt{x}}$，并说明它们反映的增长等级关系。

**过程**

对 $\frac{x^3}{e^x}$ 连续三次使用洛必达法则:$\lim_{x\to+\infty}\frac{x^3}{e^x}=\lim\frac{3x^2}{e^x}=\lim\frac{6x}{e^x}=\lim\frac{6}{e^x}=0$。对 $\frac{\ln x}{\sqrt{x}}$:$\lim_{x\to+\infty}\frac{\ln x}{\sqrt{x}}=\lim\frac{1/x}{1/(2\sqrt{x})}=\lim\frac{2}{\sqrt{x}}=0$。两者均为 $0$,反映增长等级:$e^x$ 远快于多项式 $x^3$,而 $x^3$(进而 $\sqrt{x}$)远快于 $\ln x$,即 $e^x\gg x^3\gg\sqrt{x}\gg\ln x$。

**答案原文**

两者均为 $0$;反映增长等级 $e^x\gg x^3\gg\sqrt{x}\gg\ln x$。

## 90. draft-c26-02

内容 SHA256：`46c37ff21a7b604bcff9bd05a824dec38a3ffe2701b042436a2202e0d4e74946`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft.jsonl；源 SHA256 `25705ed80dbac40074a2bc29ed482de0087b12bc96d3e1ec0cb9f77722fefe0e`；行 12，JSON pointer `/`。

**题干**

解释矩阵 $A=\begin{pmatrix}1&0\\0&0\end{pmatrix}$ 对应的线性变换的几何作用，并求其核与像。

**过程**

$A(x,y)=(x,0)$:把每个点垂直投影到 $x$ 轴上(保留横坐标,丢弃纵坐标)。核为 $\{(0,y)\}$,即 $y$ 轴(投影中消失的方向);像为 $x$ 轴(投影后的整个值域)。秩为 $1$,零度为 $1$,满足秩-零度定理 $1+1=2$。

**答案原文**

向 $x$ 轴的垂直投影;核为 $y$ 轴,像为 $x$ 轴,秩 $1$。

## 91. 原记录无 id

内容 SHA256：`482e07295f3d59c8b3b9efda220c039d2d3a68bd5a14c1ac9584efcdeae10588`。

来源：reviews/codex-supervision/2026-10-06-scene-start-supervision/math-repair-proposals.pending.json；源 SHA256 `271199e7aa59032a8339fff9674eab555995e9d66a201d47b06c674d2c914d3b`；行 —，JSON pointer `/records/4/fields`。

**题干**

已知 $P(A)=\frac35$，$P(B)=\frac25$，且 $P(A\cap B)=\frac15$。求 $P(A\mid B)$ 和 $P(B\mid A)$。

**过程**

由条件概率定义，$P(A\mid B)=\frac{P(A\cap B)}{P(B)}=\frac{1/5}{2/5}=\frac15\cdot\frac52=\frac12$；$P(B\mid A)=\frac{P(A\cap B)}{P(A)}=\frac{1/5}{3/5}=\frac15\cdot\frac53=\frac13$。两条件事件的概率均为正，定义适用。

**答案原文**

$P(A\mid B)=\frac12$，$P(B\mid A)=\frac13$。

## 92. draft-c52-05

内容 SHA256：`497bb3c7f5d45324019381ea5eb8662819cf0dddc76f25ed664ec66f064736fa`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-01.jsonl；源 SHA256 `9f924a4b39b9eacb35e2efd98555567a327f9e33bc82aab515d693b3136d7f46`；行 15，JSON pointer `/`。

**题干**

设随机变量 $X$ 的分布函数 $F$ 连续，在某区间 $I$ 上严格递增，且 $P(X\in I)=1$、$F(I)=(0,1)$。证明 $Y=F(X)\sim U(0,1)$。再设目标随机变量 $Z$ 的密度为 $g(z)=\begin{cases}\frac12,&0<z<1\\ z-1,&1<z<2\\0,&\text{其余}\end{cases}$。给定 $U\sim U(0,1)$，构造 $Z=T(U)$，写出完整分布函数并验证其分布；说明为何 $T$ 必须分段。

**过程**

对 $0<y<1$，由假设，$F$ 在 $I$ 上存在反函数 $F_I^{-1}$。除零概率事件外，$F(X)\le y$ 等价于 $X\le F_I^{-1}(y)$，所以 $P(Y\le y)=F(F_I^{-1}(y))=y$；$y\le0$ 时概率为 $0$，$y\ge1$ 时为 $1$，故 $Y\sim U(0,1)$。目标密度非负，且 $\int_0^1\frac12\,dz+\int_1^2(z-1)\,dz=\frac12+\frac12=1$。积分得 $G(z)=\begin{cases}0,&z\le0\\\frac z2,&0<z\le1\\\frac12+\frac{(z-1)^2}{2},&1<z<2\\1,&z\ge2\end{cases}$，在 $z=1$ 连续，$G(1)=\frac12$。两段 CDF 的反函数分别为 $T(u)=2u$（$0<u\le\frac12$）与 $T(u)=1+\sqrt{2u-1}$（$\frac12<u<1$）。令 $Z=T(U)$。若 $0<z\le1$，事件 $T(U)\le z$ 等价于 $U\le z/2$，概率为 $z/2$；若 $1<z<2$，等价于 $U\le\frac12+\frac{(z-1)^2}{2}$，概率为该阈值。外侧概率分别为 $0$ 和 $1$，所以构造确有 CDF $G$。密度在单点 $z=1$ 的取值不影响分布；此处 CDF 无跳跃、没有原子。逆映射在 $u=\frac12$ 处分段，因为目标 CDF 的两段表达式不同，不能以一个线性或幂函数代替全部分支。

**答案原文**

$Y\sim U(0,1)$；$Z=T(U)$，其中 $T(u)=\begin{cases}2u,&0<u\le\frac12\\1+\sqrt{2u-1},&\frac12<u<1\end{cases}$。完整 CDF：$G(z)=0$（$z\le0$）、$z/2$（$0<z\le1$）、$\frac12+\frac{(z-1)^2}{2}$（$1<z<2$）、$1$（$z\ge2$）。

## 93. draft-c10-01

内容 SHA256：`49b0f1f6b3809941c8d8525bb1b77a0a8acd6a68b2b668ff847beded60cc42fc`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft.jsonl；源 SHA256 `1cc220e2699b799fb9bacc8525e1f9d82321dc39dacd33e5c1caa21c1a7d959b`；行 1，JSON pointer `/`。

**题干**

判断级数 $\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n}$ 的敛散性，并指出是绝对收敛还是条件收敛。

**过程**

绝对收敛性:$\left|\frac{(-1)^{n+1}}{n}\right|=\frac1n$,$\sum\frac1n$ 为调和级数,发散,故非绝对收敛。条件收敛性:$a_n=\frac1n$ 单调递减趋于 $0$,由莱布尼茨判别法,$\sum\frac{(-1)^{n+1}}{n}$ 收敛。故为条件收敛(其和为 $\ln2$)。

**答案原文**

条件收敛(和为 $\ln2$)。

## 94. draft-c15-01

内容 SHA256：`4b10d8863f5be88cd4eaa465cd6321e0d7b03d4e57ec4904cdf468d6e778ff51`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft.jsonl；源 SHA256 `9aa29561a8f8dc1a725169c6fa9b3fb558e5c2bed5b0d43940d42e9b5ff823e3`；行 1，JSON pointer `/`。

**题干**

求直线 $l:\frac{x-1}{1}=\frac{y+2}{0}=\frac{z}{1}$ 与平面 $\pi:x+y=1$ 的夹角。

**过程**

直线方向 $d=(1,0,1)$,平面法向量 $n=(1,1,0)$。夹角公式 $\sin\varphi=\frac{|d\cdot n|}{|d|\,|n|}=\frac{|1\times1+0\times1+1\times0|}{\sqrt{2}\times\sqrt{2}}=\frac{1}{2}$,故 $\varphi=\arcsin\frac12=\frac{\pi}{6}$,即 $30^\circ$。

**答案原文**

夹角为 $\frac{\pi}{6}$(即 $30^\circ$)。

## 95. draft-c35-02

内容 SHA256：`4fae8e1f69bfbd312004a54c78df2e10ef9ad49f295a351473bc0a7efa43bddd`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-03.jsonl；源 SHA256 `ed738d83f3c59a525f3119c56735aac4bcc4b50ddf4817701a786e7b1e3c9e5d`；行 2，JSON pointer `/`。

**题干**

对实对称矩阵 $A=\begin{pmatrix}1&2\\2&2\end{pmatrix}$，求合同规范形与相似对角形，给出相应可逆变换，并说明实对称矩阵之间的相似与合同的蕴含关系。

**过程**

对应二次型 $f=x^2+4xy+2y^2=(x+2y)^2-2y^2$。令 $u=x+2y$、$v=\sqrt2\,y$，则 $f=u^2-v^2$，旧坐标满足 $\binom xy=C\binom uv$，其中 $C=\begin{pmatrix}1&-\sqrt2\\0&1/\sqrt2\end{pmatrix}$。直接计算 $C^{\mathsf T}AC=\operatorname{diag}(1,-1)$，$\det C=1/\sqrt2\ne0$。特征多项式为 $\lambda^2-3\lambda-2$，特征值 $\lambda_\pm=\frac{3\pm\sqrt{17}}2$。令 $v_\pm=(2,\lambda_\pm-1)^{\mathsf T}$、$q_\pm=v_\pm/\sqrt{4+(\lambda_\pm-1)^2}$、$Q=(q_+,q_-)$。由 $v_+^{\mathsf T}v_-=4+(\lambda_+-1)(\lambda_--1)=0$，有 $Q^{\mathsf T}Q=I$，$Q^{-1}AQ=\operatorname{diag}(\lambda_+,\lambda_-)$。对实对称矩阵，相似保持全部特征值，因而保持惯性；由惯性定理，相似蕴含合同。反向一般不成立：$I_2$与$2I_2$合同（$C=\sqrt2 I_2$），但特征值不同，不相似。合同规范形$(1,-1)$记录惯性，相似对角形记录完整谱。

**答案原文**

合同规范形 $\operatorname{diag}(1,-1)$，$C=\begin{pmatrix}1&-\sqrt2\\0&1/\sqrt2\end{pmatrix}$；相似对角形 $\operatorname{diag}(\frac{3+\sqrt{17}}2,\frac{3-\sqrt{17}}2)$。实对称矩阵之间，相似$\Rightarrow$合同，合同$\nRightarrow$相似。

## 96. draft-c43-02

内容 SHA256：`4feb287868f2d039ba0ce3eaf9ee100dd09dbf09c36ee0e8b5073bddec5cbafd`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft.jsonl；源 SHA256 `b92648645c3b17a796e6b8938f67de934cddafd0cf192ab24ae006e5b423e27f`；行 2，JSON pointer `/`。

**题干**

求 $\mathbb R^3$ 上满足 $f(1,1,0)=2$，$f(0,1,1)=-1$，$f(1,0,1)=3$ 的线性泛函 $f(x,y,z)=ax+by+cz$。

**过程**

代入三个条件:$a+b=2$,$b+c=-1$,$a+c=3$。第一式减第二式:$a-c=3$;与第三式 $a+c=3$ 相加得 $2a=6$,$a=3$;代入第三式 $c=0$;代入第一式 $b=-1$。故 $f(x,y,z)=3x-y$。验证:$f(1,1,0)=3-1=2$ ✓;$f(0,1,1)=-1$ ✓;$f(1,0,1)=3$ ✓。

**答案原文**

$f(x,y,z)=3x-y$。

## 97. draft-c37-03

内容 SHA256：`52917a43f7e511d58d622c9e6ac1b18e2391adb7f3f3caf0df493dc88f8594dd`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft.jsonl；源 SHA256 `afcd74e3e4d285e77802f29ab182f9dce80cfe5833b983feb8af34694ed15331`；行 8，JSON pointer `/`。

**题干**

在 $\mathbb R^2$ 中，设从标准基到基 $\eta_1=(1,1)$，$\eta_2=(1,-1)$ 的过渡矩阵为 $P$。求 $P$；若向量 $\alpha$ 在基 $\eta$ 下的坐标为 $(2,3)$，求 $\alpha$ 在标准基下的坐标；若向量 $\beta$ 在标准基下的坐标为 $(2,3)$，求 $\beta$ 在基 $\eta$ 下的坐标。

**过程**

过渡矩阵 $P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$。由 $P^2=\begin{pmatrix}2&0\\0&2\end{pmatrix}=2I$ 得 $P^{-1}=\frac12P=\frac12\begin{pmatrix}1&1\\1&-1\end{pmatrix}$。$\alpha$ 在标准基下的坐标(基向量按新坐标组合)：$\alpha=2\eta_1+3\eta_2=2(1,1)+3(1,-1)=(5,-1)$。$\beta$ 在基 $\eta$ 下的坐标：$\xi=P^{-1}\beta=\frac12(2+3,\,2-3)=(\frac52,-\frac12)$。验证:$\frac52\eta_1-\frac12\eta_2=(\frac52-\frac12,\frac52+\frac12)=(2,3)=\beta$。注意:向量本身用 $P$ 组合,坐标换基用 $P^{-1}$,方向相反。

**答案原文**

$P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$;$\alpha$ 在标准基下为 $(5,-1)$;$\beta$ 在基 $\eta$ 下为 $(\frac52,-\frac12)$。

## 98. draft-c45-04

内容 SHA256：`5415c43b4d4b99b82121af62278ececb495237f8a45010de6573e13f42a1f4f2`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft.jsonl；源 SHA256 `b92648645c3b17a796e6b8938f67de934cddafd0cf192ab24ae006e5b423e27f`；行 14，JSON pointer `/`。

**题干**

说明是否存在满足 $P(A|B)=\frac{9}{10}$，$P(A|\bar B)=\frac45$，且 $P(A)=\frac{1}{10}$ 的事件 $A,B$($0<P(B)<1$)；并说明一般情形下 $P(A)$ 必须满足什么约束。

**过程**

由全概率公式,$P(A)=P(A|B)P(B)+P(A|\bar B)P(\bar B)$,是 $\frac{9}{10}$ 与 $\frac45$ 的凸组合,故必满足 $\frac45\le P(A)\le\frac{9}{10}$。题设 $P(A)=\frac{1}{10}$ 落在此区间之外,故不存在这样的事件。一般约束:给定 $P(A|B)$ 与 $P(A|\bar B)$ 时,$P(A)$ 必须是两者的凸组合,即介于两者之间;数据不满足此约束时自相矛盾,不可实现。

**答案原文**

不存在:全概率公式要求 $P(A)$ 为 $\frac45$ 与 $\frac{9}{10}$ 的凸组合(介于两者之间),而 $\frac{1}{10}$ 不在其中。

## 99. draft-c42-02

内容 SHA256：`576285c19a77dc6d588020ae9307e08b744acfbaa56455f2b59690b8028ba118`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft.jsonl；源 SHA256 `58ae126d6bd255576c005783f78e6ade29c9f0bd60b1c7fa2e0971ba6cad1a00`；行 12，JSON pointer `/`。

**题干**

设 $R(\theta)=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}$。验证 $R(\theta_1)R(\theta_2)=R(\theta_1+\theta_2)$，并说明其几何含义。

**过程**

$R(\theta_1)R(\theta_2)=\begin{pmatrix}\cos\theta_1&-\sin\theta_1\\\sin\theta_1&\cos\theta_1\end{pmatrix}\begin{pmatrix}\cos\theta_2&-\sin\theta_2\\\sin\theta_2&\cos\theta_2\end{pmatrix}$。第一行第一列:$\cos\theta_1\cos\theta_2-\sin\theta_1\sin\theta_2=\cos(\theta_1+\theta_2)$;第一行第二列:$-\cos\theta_1\sin\theta_2-\sin\theta_1\cos\theta_2=-\sin(\theta_1+\theta_2)$;第二行第一列:$\sin\theta_1\cos\theta_2+\cos\theta_1\sin\theta_2=\sin(\theta_1+\theta_2)$;第二行第二列:$-\sin\theta_1\sin\theta_2+\cos\theta_1\cos\theta_2=\cos(\theta_1+\theta_2)$。故 $R(\theta_1)R(\theta_2)=R(\theta_1+\theta_2)$。几何含义:先旋转 $\theta_2$ 再旋转 $\theta_1$ 等于一次旋转 $\theta_1+\theta_2$(旋转的合成仍是旋转,且角度相加)。

**答案原文**

验证见解法(由和角公式逐项核对);几何上旋转的合成角度相加。

## 100. draft-c53-01

内容 SHA256：`57a1bfd06c8f3e39724c3e36bf5e768e8e61c8ef3a034f1869be42b17b57d2d3`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-18/draft.jsonl；源 SHA256 `6f921b08949f3ee7aaa95ce0363cafaff81b0ab7d0d95f10e1b5a280d697d8d1`；行 6，JSON pointer `/`。

**题干**

设 $X$ 服从参数为 $p$ 的几何分布($P(X=k)=p(1-p)^{k-1}$,$k=1,2,\dots$)。用可列可加性求 $P(X\ge k)$。

**过程**

事件 $\{X\ge k\}$ 可拆分为可列个互斥事件 $\{X=i\}$($i=k,k+1,\dots$)的并。由可列可加性,$P(X\ge k)=\sum_{i=k}^{\infty}P(X=i)=\sum_{i=k}^{\infty}p(1-p)^{i-1}=p(1-p)^{k-1}\sum_{j=0}^{\infty}(1-p)^j=p(1-p)^{k-1}\cdot\frac{1}{1-(1-p)}=(1-p)^{k-1}$。

**答案原文**

$P(X\ge k)=(1-p)^{k-1}$。

## 101. draft-c30-02

内容 SHA256：`57ae8df0b0735adafc2c1c5e791fd0ad55c419508af0f25bc810123cc6fb95a0`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft.jsonl；源 SHA256 `4a8930a557e05b01cec58257879ecd5bd9679b9c08e3e478767c363642ebe382`；行 12，JSON pointer `/`。

**题干**

求 $f(x)=x^4-2x^3+3x^2-4x+5$ 在 $x=2$ 处的泰勒展开。

**过程**

逐阶求导:$f'(x)=4x^3-6x^2+6x-4$，$f''(x)=12x^2-12x+6$，$f'''(x)=24x-12$，$f^{(4)}(x)=24$。在 $x=2$ 处:$f(2)=16-16+12-8+5=9$，$f'(2)=32-24+12-4=16$，$f''(2)=48-24+6=30$，$f'''(2)=48-12=36$。泰勒公式:$f(x)=9+16(x-2)+\frac{30}{2}(x-2)^2+\frac{36}{6}(x-2)^3+\frac{24}{24}(x-2)^4=9+16(x-2)+15(x-2)^2+6(x-2)^3+(x-2)^4$。

**答案原文**

$f=(x-2)^4+6(x-2)^3+15(x-2)^2+16(x-2)+9$。

## 102. linalg-048

内容 SHA256：`57bd9e03351bd600fe4ce984ef1c1b037ab30d9f6623c7fa09d88c8c8cc77ff9`。

来源：reviews/codex-supervision/2026-10-05-math-template-followup-v2/corrected-candidates/dataset_linalg.jsonl；源 SHA256 `ba1e7680351b93504c1d8fe5518004b9107545a78761750d9d9933e8fd16ab45`；行 1，JSON pointer `/`。

**题干**

已知矩阵 $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$，分析它对应的线性变换对二维平面产生的几何影响。

**过程**

该矩阵对应的线性变换将标准基向量 $\vec{e_1} = (1,0)$ 映射为 $(2,1)$，$\vec{e_2} = (0,1)$ 映射为 $(1,2)$。该矩阵为对称矩阵，特征值为 $3$ 和 $1$，对应正交特征方向 $(1,1)$ 与 $(1,-1)$：变换是沿这两个方向的纯拉伸（无剪切），沿 $(1,1)$ 方向拉伸为原来的 3 倍，沿 $(1,-1)$ 方向保持不变。为了具体分析，可以计算其行列式 $\det(A) = 2\times2 - 1\times1 = 3$，说明变换后单位正方形的面积扩大为原来的3倍。

**答案原文**

沿 $(1,1)$ 方向拉伸为原来的3倍，沿 $(1,-1)$ 方向保持不变；无旋转或剪切，面积扩大为原来的3倍，$\det A=3$。

## 103. syn-eval-ok

内容 SHA256：`582cb762bfae156aa16d721e662b017d3789ba3faf46f98fee746c8cfd9055a7`。

来源：reviews/codex-supervision/history-from-code/pytest-68c51be/test_cross_candidate_file_ids_0/candidate/b.jsonl；源 SHA256 `8a57cc9d0649f8ec12888a090a64571a4ba35656fd566f46ffb18c818f9d4624`；行 1，JSON pointer `/`。

**题干**

A separate synthetic geometric task: classify three conic shapes.

**过程**

2×3=6。

**答案原文**

6

## 104. draft-c14-05

内容 SHA256：`58637c21d0cca1105f705c9a15ec067e589042ff290f5b5e39afa006485b215a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft.jsonl；源 SHA256 `1cc220e2699b799fb9bacc8525e1f9d82321dc39dacd33e5c1caa21c1a7d959b`；行 15，JSON pointer `/`。

**题干**

将 $f(x)=1$($0<x<\pi$)分别作正弦展开(奇延拓)与余弦展开(偶延拓),并比较两种展开在区间内部与端点处的收敛行为。

**过程**

正弦展开(奇延拓):奇延拓后为方波($-1,1$ 交替),$b_n=\frac2\pi\int_0^{\pi}\sin nx\,dx=\frac{2(1-(-1)^n)}{n\pi}$,即 $f=1=\frac{4}{\pi}\sum_{k=1}^{\infty}\frac{\sin(2k-1)x}{2k-1}$($0<x<\pi$)。在端点 $x=0,\pi$ 处,奇延拓函数跳跃($1$ 到 $-1$),级数和为左右极限平均 $\frac{1+(-1)}{2}=0$。余弦展开(偶延拓):偶延拓后 $f\equiv1$ 处处连续,$a_0=2$,$a_n=0$($n\ge1$),即 $f=1$ 恰为单项展开,在闭区间 $[0,\pi]$ 上处处成立(包括端点)。比较:同一函数在内部两种展开都收敛到 $1$,但正弦展开在端点收敛到 $0$(由奇延拓的跳跃决定),余弦展开在端点也收敛到 $1$(延拓连续)——延拓方式决定端点行为。

**答案原文**

正弦展开:$1=\frac{4}{\pi}\sum_{k=1}^{\infty}\frac{\sin(2k-1)x}{2k-1}$($0<x<\pi$),端点取 $0$;余弦展开:$1$ 的单项展开,含端点处处为 $1$。

## 105. eval-linalg-021-s2

内容 SHA256：`596c7a8f9caa4f1fef448acc5d7c4bf0a793287e9d55d20887b881d18012dcf4`。

来源：reviews/codex-supervision/history-from-code/recheck-68c51be/data/v2/eval/dataset_eval.json；源 SHA256 `1de2df62edd0b01403df813c80edc3a5a9dbf1791f0b223d8e0f107ccee55e6e`；行 —，JSON pointer `/256`。

**题干**

判断二次型 $f=x^2+2y^2+3z^2+2xy+2xz+4yz$ 是否正定。

**过程**

$f=(x+y+z)^2+(y+z)^2+z^2$。展开验证：$(x+y+z)^2=x^2+y^2+z^2+2xy+2xz+2yz$，$(y+z)^2=y^2+z^2+2yz$，三项相加得 $x^2+2y^2+3z^2+2xy+2xz+4yz$。三个平方项线性无关的变量替换（$u=x+y+z$、$v=y+z$、$w=z$，变换矩阵 $\begin{pmatrix}1&1&1\\0&1&1\\0&0&1\end{pmatrix}$ 可逆），故 $f=u^2+v^2+w^2$ 正定。

**答案原文**

正定

## 106. draft-c48-04

内容 SHA256：`5a1ac01c67c9d4481521db634667e2c809f3a6f8deeb98c8802b28e27c408754`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft.jsonl；源 SHA256 `bcd6ec3d0204b822f83440669662afcfe3ec7712fa4806d51506f98cb797b0c2`；行 9，JSON pointer `/`。

**题干**

设 $X\sim N(1,4)$ 与 $Y\sim N(2,9)$ 相互独立。求 $X+Y$ 与 $2X-Y$ 的分布，并求 $P(2X-Y>0)$。

**过程**

正态分布的可加性:$X+Y\sim N(1+2,\,4+9)=N(3,13)$。线性组合:$2X-Y\sim N(2\times1-2,\,4\times4+1\times9)=N(0,25)$。由对称性($N(0,25)$ 关于 $0$ 对称),$P(2X-Y>0)=\frac12$。

**答案原文**

$X+Y\sim N(3,13)$;$2X-Y\sim N(0,25)$;$P(2X-Y>0)=\frac12$。

## 107. draft-c11-03

内容 SHA256：`5a96eb88e476e5f5a33fa6e4da7337d46a6e9ce7f38dc013975b3ac0b651b983`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-02.jsonl；源 SHA256 `286625ebf0f88cca49b14f36be4bab4e5f3b29ecc0764226b7ebb5fb61a16527`；行 3，JSON pointer `/`。

**题干**

求幂级数 $\sum_{n=1}^{\infty}\frac{x^n}{n(n+1)}$ 的收敛域与和函数，并求 $S(0)$、$S(1)$、$S(-1)$。

**过程**

收敛域：$|x|<1$ 时由比值法收敛；$x=\pm1$ 时 $\left|\frac{(\pm1)^n}{n(n+1)}\right|\leq\frac{1}{n(n+1)}$ 且 $\sum\frac{1}{n(n+1)}$ 收敛，故两端点绝对收敛，收敛域为 $[-1,1]$。求和(先对 $|x|<1$)：拆项 $\frac{1}{n(n+1)}=\frac{1}{n}-\frac{1}{n+1}$，记 $A(x)=\sum_{n=1}^{\infty}\frac{x^n}{n}=-\ln(1-x)$，则 $\sum_{n=1}^{\infty}\frac{x^n}{n+1}=\frac{1}{x}\sum_{n=1}^{\infty}\frac{x^{n+1}}{n+1}=\frac{A(x)-x}{x}$($x\neq0$)。故 $S(x)=A(x)-\frac{A(x)-x}{x}=1+\frac{(1-x)\ln(1-x)}{x}$。$S(0)=0$(通项为 0)；$S(1)=\sum\frac{1}{n(n+1)}=1$(裂项求和),与公式在 $x\to1^-$ 的极限一致;$S(-1)=\sum\frac{(-1)^n}{n(n+1)}=1-2\ln2$(由公式 $1+\frac{2\ln2}{-1}$)。因为在 $[-1,1]$ 上 $|x^n/(n(n+1))|\le1/(n(n+1))$，由Weierstrass判别法一致收敛，所以和函数连续，$x=-1$ 的取值可由右极限得到；$x=1$ 用裂项或左极限取值，不能直接将 $\ln0$ 代入表达式。

**答案原文**

收敛域 $[-1,1]$。对 $-1\le x<1$ 且 $x\ne0$，$S(x)=1+\frac{(1-x)\ln(1-x)}x$；另外 $S(0)=0$、$S(1)=1$，$S(-1)=1-2\ln2$。

## 108. draft-c34-05

内容 SHA256：`5b5bf8746c85bac2841cb825b498fb2bd979513896fe1b4456e784e8fcd02403`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft.jsonl；源 SHA256 `2a488597e92f7efdb6ec80074b147c9290e949fbeb4cbd114e293657e7c04776`；行 5，JSON pointer `/`。

**题干**

证明三类初等矩阵都可逆，并分别求其行列式；由此说明任意可逆矩阵可以表示为初等矩阵的乘积。

**过程**

三类初等矩阵及其逆:交换型 $P_{ij}$($P_{ij}^{-1}=P_{ij}$,行列式 $-1$);倍乘型 $D_i(k)$($k\neq0$,$D_i(k)^{-1}=D_i(\frac1k)$,行列式 $k$);倍加型 $E_{ij}(k)$(第 $j$ 行乘 $k$ 加到第 $i$ 行,$E_{ij}(k)^{-1}=E_{ij}(-k)$,行列式 $1$)。均可逆。任意可逆矩阵:$A$ 可逆 ⟺ $A$ 的行阶梯形经行变换可化为单位矩阵(主元均非零),即存在初等矩阵 $E_1,\dots,E_m$ 使 $E_m\cdots E_1A=I$,故 $A=E_1^{-1}\cdots E_m^{-1}$,而初等矩阵的逆仍是初等矩阵,故 $A$ 是初等矩阵的乘积。

**答案原文**

交换型:$P_{ij}^{-1}=P_{ij}$,$\det=-1$;倍乘型:$D_i(k)^{-1}=D_i(\frac1k)$,$\det=k$;倍加型:$E_{ij}(k)^{-1}=E_{ij}(-k)$,$\det=1$;可逆矩阵可化为 $I$ 故可表为初等矩阵之积(证明见解法)。

## 109. draft-c39-04

内容 SHA256：`5be0b3b71d591f8395209045da2421df7c09ef9f2287bb2e298d11ff276332be`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft.jsonl；源 SHA256 `2a488597e92f7efdb6ec80074b147c9290e949fbeb4cbd114e293657e7c04776`；行 14，JSON pointer `/`。

**题干**

设 $T:\mathbb R^3\to\mathbb R^3$ 由 $T(x,y,z)=(x+y,\,y+z,\,0)$ 定义。求 $T^2$ 的表达式，并比较 $T$ 与 $T^2$ 的核与像。

**过程**

$T^2(x,y,z)=T(x+y,\,y+z,\,0)=((x+y)+(y+z),\,(y+z)+0,\,0)=(x+2y+z,\,y+z,\,0)$。核:$T$ 的核:$x+y=0,y+z=0$,得 $(x,-x,x)$,$\ker T=\mathrm{span}\{(1,-1,1)\}$。$T^2$ 的核:$x+2y+z=0,y+z=0$。由第二式 $z=-y$,代入第一式得 $x+2y-y=x+y=0$,故与 $\ker T$ 相同的条件,$\ker T^2=\ker T=\mathrm{span}\{(1,-1,1)\}$。像:$T$ 的像由 $T(1,0,0)=(1,0,0)$,$T(0,1,0)=(1,1,0)$,$T(0,0,1)=(0,1,0)$ 张成,即 $\{(a,b,0)\}$,维数 $2$。$T^2$ 的像由 $T^2(1,0,0)=(1,0,0)$,$T^2(0,0,1)=(1,1,0)$ 张成($T^2(0,1,0)=(2,1,0)=(1,0,0)+(1,1,0)$),也是 $\{(a,b,0)\}$,维数 $2$。故 $\ker T^2=\ker T$ 且 $\mathrm{im}\,T^2=\mathrm{im}\,T$(本例中复合映射的核与像均不变)。

**答案原文**

$T^2(x,y,z)=(x+2y+z,\\,y+z,\\,0)$;$\\ker T^2=\\ker T=\\mathrm{span}\\{(1,-1,1)\\}$,$\\mathrm{im}\\,T^2=\\mathrm{im}\\,T=\\{(a,b,0)\\}$。

## 110. draft-c51-03

内容 SHA256：`5d6fd9cd7af23eca235207c446c95bf468e30bca247a12367a86098b0bb4b6ac`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft-codex-repair-v1.jsonl；源 SHA256 `24548fa6bd5a758c36b8b41480f4a46047e4aaeeaa18def93a813e72a241c454`；行 13，JSON pointer `/`。

**题干**

某疾病患病率为 $\frac{1}{1000}$。一次检测对患病者呈阳性的概率为 $\frac{99}{100}$，对未患病者呈阳性的概率为 $\frac{1}{100}$。某人第一次检测呈阳性，随后做了一次独立(在给定患病状态下)的同类检测，仍呈阳性。求两次检测后此人患病的概率，并与第一次检测后的概率对比。

**过程**

第一次阳性后，由贝叶斯公式，$P(\text{患病}\mid+_1)=\frac{\frac{1}{1000}\times\frac{99}{100}}{\frac{1}{1000}\times\frac{99}{100}+\frac{999}{1000}\times\frac{1}{100}}=\frac{99}{99+999}=\frac{99}{1098}=\frac{11}{122}$。第二次检测在给定患病状态下与第一次独立，故将 $\frac{11}{122}$ 作为新的先验再更新：$P(\text{患病}\mid+_1,+_2)=\frac{\frac{11}{122}\times\frac{99}{100}}{\frac{11}{122}\times\frac{99}{100}+\frac{111}{122}\times\frac{1}{100}}=\frac{1089}{1089+111}=\frac{1089}{1200}=\frac{363}{400}$。对比:单次阳性后为 $\frac{11}{122}$，两次后为 $\frac{363}{400}$。

**答案原文**

第一次阳性后:$P=\frac{11}{122}$;两次阳性后:$P=\frac{363}{400}$。

## 111. draft-c19-02

内容 SHA256：`5e20453b60d32911b5158bd1b8805df7008aab54f1a1bb563fd5ff74afe512cd`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft.jsonl；源 SHA256 `9aa29561a8f8dc1a725169c6fa9b3fb558e5c2bed5b0d43940d42e9b5ff823e3`；行 12，JSON pointer `/`。

**题干**

求以 $xy$ 平面内的圆 $x^2+y^2=1$($z=0$)为准线、母线平行于直线 $l$:方向 $(1,1,1)$ 的柱面方程。

**过程**

柱面上点 $(x,y,z)$ 沿母线方向 $(1,1,1)$ 平移后可落到准线上:存在 $s$ 使 $(x-s,y-s,z-s)$ 满足 $z-s=0$ 且 $x^2+y^2$ 条件,即取 $s=z$,得 $(x-z)^2+(y-z)^2=1$。故柱面方程为 $(x-z)^2+(y-z)^2=1$。验证:准线上点 $(x_0,y_0,0)$($x_0^2+y_0^2=1$)满足 $(x_0-0)^2+(y_0-0)^2=1$ ✓;过准线上点沿 $(1,1,1)$ 的直线 $(x_0+s,y_0+s,s)$:$(x_0+s-s)^2+(y_0+s-s)^2=x_0^2+y_0^2=1$ ✓,整条母线在曲面上。

**答案原文**

柱面方程为 $(x-z)^2+(y-z)^2=1$。

## 112. draft-c11-04

内容 SHA256：`5e3f3358f90233a35efadc6468daae71ef069b248092f77d8b5122119fb9c5f6`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft.jsonl；源 SHA256 `71d46f404c59db6194494bf8ea2353202b77f602a15522f58c1b4599d1cbb07a`；行 4，JSON pointer `/`。

**题干**

求幂级数 $\sum_{n=1}^{\infty}\frac{nx^n}{n!}$ 的收敛域与和函数。

**过程**

比值法：$\lim_{n\to\infty}\left|\frac{(n+1)x^{n+1}/(n+1)!}{nx^n/n!}\right|=\lim_{n\to\infty}\frac{n+1}{n}\cdot\frac{|x|}{n+1}=0$，对一切实数 $x$ 收敛，收敛域为 $\mathbb R$。求和：$\sum_{n=1}^{\infty}\frac{nx^n}{n!}=\sum_{n=1}^{\infty}\frac{x^n}{(n-1)!}=x\sum_{m=0}^{\infty}\frac{x^m}{m!}=xe^x$。逐项运算的合法性由该级数在全实轴上一致收敛于紧区间保证(指数级数)。

**答案原文**

收敛域为 $\mathbb R$;和函数 $S(x)=xe^x$。

## 113. draft-c28-02

内容 SHA256：`6060624f2a4b9dcc57277c6f69bb7c33713733df205d74f600e702baaae36e5c`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-05.jsonl；源 SHA256 `6eabbb3d46a7d6a4b39d563a7fc339d117b2be8533dce70e0a85bf2963570f0e`；行 7，JSON pointer `/`。

**题干**

设 $a=(1,2)$，$b=(3,4)$。求以 $a,b$ 为邻边的平行四边形面积；交换两向量的顺序后，二阶行列式如何变化？并解释有向面积的含义。

**过程**

固定平面标准定向。$\det(a,b)=1\cdot4-2\cdot3=-2$，故平行四边形面积为$|-2|=2$。交换顺序后$\det(b,a)=3\cdot2-4\cdot1=2=-\det(a,b)$，面积仍为$2$。有向面积的符号记录有序向量对的定向：正值对应逆时针，负值对应顺时针。本题$(a,b)$为负定向，交换后$(b,a)$为正定向。

**答案原文**

面积为 $2$;$\det(b,a)=-\det(a,b)$,符号反转、面积不变;符号反映定向。

## 114. draft-c23-03

内容 SHA256：`608004758c1cff915d1396d281150f43fa0c69380ddef1872c769ca94f54a41e`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft.jsonl；源 SHA256 `e0eb9bf14b1cdf0919006ede0e9523046d0edadffb69ac3a10e4941a77563756`；行 13，JSON pointer `/`。

**题干**

求旋转矩阵 $A=\begin{pmatrix}0&0&1\\0&1&0\\-1&0&0\end{pmatrix}$ 的旋转轴与旋转角。

**过程**

旋转轴是特征值 $1$ 的特征向量方向:解 $(A-I)v=0$,即 $\begin{pmatrix}-1&0&1\\0&0&0\\-1&0&-1\end{pmatrix}v=0$:由第一行 $-v_1+v_3=0$ 与第三行 $-v_1-v_3=0$ 得 $v_1=v_3=0$,$v_2$ 任意,故轴为 $y$ 轴(方向 $(0,1,0)$)。旋转角:由迹公式 $\mathrm{tr}(A)=1+2\cos\theta$,这里 $\mathrm{tr}(A)=0+1+0=1$,故 $\cos\theta=0$,$\theta=\pm90^\circ$;再由 $A(1,0,0)=(0,0,-1)$,按右手定则绕 $y$ 轴正方向旋转 $90^\circ$ 恰把 $x$ 轴正方向转到 $z$ 轴负方向,故 $\theta=90^\circ$。

**答案原文**

旋转轴为 $y$ 轴(方向 $(0,1,0)$),旋转角 $90^\circ$(绕 $y$ 轴正向)。

## 115. syn-eval-leak

内容 SHA256：`61831368c4907c21215f899752bc58c1c86c244b27b877463f292ccfd8321950`。

来源：reviews/codex-supervision/history-from-code/clone-check/reviews/fixtures-eval-test/eval_leak.jsonl；源 SHA256 `c1903e06deec8e78653ea337c09b37bbf58734629d8933a5c755ee8d9aec3631`；行 1，JSON pointer `/`。

**题干**

合成训练题目A：求 1+1 的值。

**过程**

换个解法：2×1=2。

**答案原文**

2

## 116. fixture-001

内容 SHA256：`62742813b88ccdd10d4a32e52edbc50324b18925752cd0160675bc64a4e1406a`。

来源：reviews/codex-supervision/history-from-code/pytest-68c51be/test_answer_container_rejected1/train.jsonl；源 SHA256 `6d2e5313497a861fe679764dc5de2090efe37e6d1852c0a4f2e5c7b01cea35e0`；行 1，JSON pointer `/`。

**题干**

求极限 $\lim_{x \to 0} \frac{\sin x}{x}$ 的值。

**过程**

由夹逼定理, $\cos x < \frac{\sin x}{x} < 1$, 故极限为 1。

**答案原文**

{
  "value": "4"
}

## 117. draft-c07-02

内容 SHA256：`62ecb313060094e99a6189bfc31928bfc216df9d26aacbbd5ab16911145f58e5`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft.jsonl；源 SHA256 `1d0950f73fad698178bef910eec1c19d5303cfe6bdabbcd76bddab903f05e44b`；行 2，JSON pointer `/`。

**题干**

求心形线 $r=1+\cos\theta$ 所围成的面积。

**过程**

心形线在 $0\le\theta\le2\pi$ 上完整描绘一遍。$A=\frac12\int_0^{2\pi}(1+\cos\theta)^2\,d\theta=\frac12\int_0^{2\pi}(1+2\cos\theta+\cos^2\theta)\,d\theta=\frac12\left(2\pi+0+\pi\right)=\frac{3\pi}{2}$(用到 $\int_0^{2\pi}\cos\theta\,d\theta=0$ 与 $\int_0^{2\pi}\cos^2\theta\,d\theta=\pi$)。

**答案原文**

面积为 $\frac{3\pi}{2}$。

## 118. draft-c33-05

内容 SHA256：`65532de18f7953ea5ae4e20c22794f9045b6efc9f6140fafafd9670faf90c365`。

来源：reviews/codex-supervision/2026-10-05-pdf-repair-supervision/followup-2327/negative-fixtures/record-binding-tamper/batch-02/draft-codex-repair-v5.jsonl；源 SHA256 `1bb50f4fbecdca7b429e9342f7f2f579731dd9582269a0e5e7b1c639829ec91b`；行 10，JSON pointer `/`。

**题干**

令加权循环矩阵$C=\begin{pmatrix}0&2&0\\0&0&3\\1/6&0&0\end{pmatrix}$，$A_t=I-tC$，$t\in\mathbb R$。用矩阵多项式恒等式求全部可逆参数及逆矩阵。在唯一奇异参数下，求$A_tx=b$的相容条件与全部解。

**过程**

$C^3=I$，故$(I-tC)(I+tC+t^2C^2)=(1-t^3)I$，两因子均为$C$的多项式，因此逆序乘积也相同。对实数$t\ne1$，$A_t^{-1}=(I+tC+t^2C^2)/(1-t^3)=\frac1{1-t^3}\begin{pmatrix}1&2t&6t^2\t^2/2&1&3t\t/6&t^2/3&1\end{pmatrix}$。直接行列式为$1-t^3$，唯一实奇异参数$t=1$。此时方程为$x_1-2x_2=b_1,x_2-3x_3=b_2,x_3-x_1/6=b_3$，将三式分别乘$1,2,6$再相加得必要条件$b_1+2b_2+6b_3=0$。若此条件满足，任意$s\in\mathbb R$给$x=(6s+2b_2+b_1,3s+b_2,s)$，代入三式均成立；反过来任何解均由第三坐标$s$决定，故这是全部解。核为$\operatorname{span}\{(6,3,1)\}$、像为$\{b:b_1+2b_2+6b_3=0\}$、秩为$2$。

**答案原文**

$t\ne1$时$A_t^{-1}=\frac1{1-t^3}\begin{pmatrix}1&2t&6t^2\t^2/2&1&3t\t/6&t^2/3&1\end{pmatrix}$；$t=1$时相容当且仅当$b_1+2b_2+6b_3=0$，全部解$(6s+2b_2+b_1,3s+b_2,s)$，$s\in\mathbb R$。

## 119. draft-c32-03

内容 SHA256：`6619bbb446ed91b2bab1ca5a4fb01e3729413db6edcca9f3dd17ed6554e5a236`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft.jsonl；源 SHA256 `e019465093b291bd83fb6ae20f3eefc40a96df3e5137a246ad8813dd03f87b34`；行 13，JSON pointer `/`。

**题干**

求非齐次线性方程 $x_1+x_2+x_3-x_4=1$ 的通解(用特解与对应齐次方程基础解系表示)。

**过程**

特解:取 $x_2=x_3=x_4=0$,得 $\eta=(1,0,0,0)$。对应齐次方程 $x_1+x_2+x_3-x_4=0$ 的基础解系:自由未知量 $x_2,x_3,x_4$,$x_1=-x_2-x_3+x_4$,取单位赋值得 $\xi_1=(-1,1,0,0)$,$\xi_2=(-1,0,1,0)$,$\xi_3=(1,0,0,1)$。通解:$x=\eta+c_1\xi_1+c_2\xi_2+c_3\xi_3$,即 $(1-c_1-c_2+c_3,\ c_1,\ c_2,\ c_3)$。

**答案原文**

通解:$x=(1,0,0,0)+c_1(-1,1,0,0)+c_2(-1,0,1,0)+c_3(1,0,0,1)$。

## 120. draft-c16-05

内容 SHA256：`664d006c58bb7ef6f86b4b091e898dd767c535db947c4de1db9a718aee39a53d`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft.jsonl；源 SHA256 `afcd74e3e4d285e77802f29ab182f9dce80cfe5833b983feb8af34694ed15331`；行 15，JSON pointer `/`。

**题干**

证明两条异面直线有且仅有一条公垂线，并写出公垂线方向与两直线间距离的公式。

**过程**

设 $l_1:P_1+td_1$，$l_2:P_2+sd_2$ 异面，则 $d_1,d_2$ 不平行(否则共面)，故 $n=d_1\times d_2\neq0$，且 $n\perp d_1,d_2$。任何公垂线与 $l_1,l_2$ 都垂直，其方向必平行于 $n$。设公垂线连接 $A=P_1+t_1d_1$ 与 $B=P_2+t_2d_2$，则 $B-A\perp d_1,d_2$，即 $(P_2-P_1+t_2d_2-t_1d_1)\cdot d_1=0$ 且 $\cdot d_2=0$，得关于 $(t_1,t_2)$ 的线性方程组，系数矩阵 $\begin{pmatrix}-|d_1|^2&d_1\cdot d_2\\-d_1\cdot d_2&|d_2|^2\end{pmatrix}$ 的行列式为 $-|d_1|^2|d_2|^2+(d_1\cdot d_2)^2=-|d_1\times d_2|^2\neq0$，故存在唯一解 $(t_1,t_2)$，即公垂线存在且唯一。距离即两垂足间距离：$d=\frac{|(P_2-P_1)\cdot(d_1\times d_2)|}{|d_1\times d_2|}$。

**答案原文**

公垂线唯一,方向为 $n=d_1\times d_2$;距离公式 $d=\frac{|(P_2-P_1)\cdot(d_1\times d_2)|}{|d_1\times d_2|}$(证明见解法)。

## 121. draft-c24-01

内容 SHA256：`66647df82aefcecf6035c250739b75118ba59a57f139beb566eb6df36063d153`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft.jsonl；源 SHA256 `25705ed80dbac40074a2bc29ed482de0087b12bc96d3e1ec0cb9f77722fefe0e`；行 1，JSON pointer `/`。

**题干**

解释剪切变换 $\begin{cases}x'=x+2y\\ y'=y\end{cases}$ 对单位正方形 $[0,1]\times[0,1]$ 的几何作用，并求像的面积。

**过程**

剪切矩阵 $A=\begin{pmatrix}1&2\\0&1\end{pmatrix}$。单位正方形的四个顶点 $(0,0),(1,0),(0,1),(1,1)$ 分别映为 $(0,0),(1,0),(2,1),(3,1)$,像为平行四边形(左右两边仍竖直,上下两边倾斜)。面积:$\det A=1\times1-2\times0=1$,故面积不变(剪切不改变面积)。

**答案原文**

单位正方形映为平行四边形(顶点 $(0,0),(1,0),(2,1),(3,1)$),面积为 $1$(不变)。

## 122. geom-027

内容 SHA256：`67215ce39590cd2c65ab8de41f044df4282425f37ee1245ecdf646058394c4f6`。

来源：reviews/codex-supervision/2026-10-05-math-template-followup-v2/corrected-candidates/dataset_geom.jsonl；源 SHA256 `0c7b3c0833d3f4d0d43ced4108022af41ceaa78686d85664d45ef2194580e662`；行 4，JSON pointer `/`。

**题干**

判断直线 $l: \frac{x-1}{1} = \frac{y-2}{2} = \frac{z-3}{3}$ 与椭球面 $x^2 + \frac{y^2}{4} + \frac{z^2}{9} = 1$ 是否有交点，若有，求交点的个数。

**过程**

将直线参数方程 $x=1+t, y=2+2t, z=3+3t$ 代入椭球面方程：$(1+t)^2 + \frac{(2+2t)^2}{4} + \frac{(3+3t)^2}{9} = 1$，化简得 $3(1+2t+t^2) = 1$，即 $3t^2 + 6t + 2 = 0$。判别式 $\Delta = 36 - 24 = 12 > 0$，方程有两个不相等的实根，因此直线与椭球面有两个交点。

**答案原文**

有两个交点

## 123. draft-c51-04

内容 SHA256：`68d268930dbfebca978d1083de7cd2fb0ddcac333deb4e6f9731137aafb472b6`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft.jsonl；源 SHA256 `71d46f404c59db6194494bf8ea2353202b77f602a15522f58c1b4599d1cbb07a`；行 14，JSON pointer `/`。

**题干**

设一枚硬币正面朝上的概率为 $\theta$，先验取 $\theta\sim U(0,1)$。抛 $10$ 次观察到 $7$ 次正面。求 $\theta$ 的后验密度与后验均值。

**过程**

似然为 $L(\theta)=\binom{10}{7}\theta^7(1-\theta)^3\propto\theta^7(1-\theta)^3$，先验密度在 $(0,1)$ 上为常数 $1$，故后验密度 $\propto\theta^{8-1}(1-\theta)^{4-1}$，即 $\theta\mid\text{data}\sim\mathrm{Beta}(8,4)$。归一化常数 $\frac{\Gamma(12)}{\Gamma(8)\Gamma(4)}=\frac{11!}{7!\times3!}=1320$，故后验密度 $f(\theta)=1320\,\theta^7(1-\theta)^3$，$0<\theta<1$。后验均值 $\frac{8}{8+4}=\frac23$。(后验均值介于先验均值 $\frac12$ 与频率 $\frac{7}{10}$ 之间,符合共轭更新的收缩性质。)

**答案原文**

后验密度 $f(\theta)=1320\,\theta^7(1-\theta)^3$($0<\theta<1$),即 $\mathrm{Beta}(8,4)$;后验均值 $\frac23$。

## 124. linalg-064

内容 SHA256：`699bc848bb57ad337403f926abc96ffde761b200b9a2c7a7230c9c932a01735d`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/0d6cf147b00b746ff542224346124229b5a6a8e21516106946a9647b8de43f36.bin；源 SHA256 `0d6cf147b00b746ff542224346124229b5a6a8e21516106946a9647b8de43f36`；行 —，JSON pointer `/16`。

**题干**

求矩阵 $A=\begin{pmatrix} 3 & 1 \\ 0 & 2 \end{pmatrix}$ 的特征值和特征向量，并说明其几何意义。

**过程**

特征方程 $|\lambda I-A|=(\lambda-3)(\lambda-2)=0$，特征值 $\lambda_1=3, \lambda_2=2$。对应特征向量：$\lambda_1=3$ 时 $\xi_1=(1,0)^T$；$\lambda_2=2$ 时 $\xi_2=(1,-1)^T$。几何上，方向 $(1,0)$ 上的向量被拉伸 3 倍，方向 $(1,-1)$ 上的向量被拉伸 2 倍。

**答案原文**

$\lambda_1=3$ 对应 $(1,0)^T$，$\lambda_2=2$ 对应 $(1,-1)^T$

## 125. draft-c53-03

内容 SHA256：`69d27b2188714c7b0fcfb38d9acb073d96dbc84a8eb3c843367a72dfc0b326ab`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-18/draft.jsonl；源 SHA256 `6f921b08949f3ee7aaa95ce0363cafaff81b0ab7d0d95f10e1b5a280d697d8d1`；行 8，JSON pointer `/`。

**题干**

说明为什么概率公理中的可加性只要求「可列」而不要求「不可列」:以 $[0,1]$ 上的均匀分布为例。

**过程**

在 $[0,1]$ 的均匀分布下,每个单点 $\{x\}$ 的概率为 $0$。若把可加性不加限制地推广到不可列求和,则 $P([0,1])=P\left(\bigcup_{x\in[0,1]}\{x\}\right)=\sum_{x\in[0,1]}P(\{x\})=0$,与 $P([0,1])=1$ 矛盾。原因:不可列多个数(即使是零)的「和」本身没有良好的定义(不可列正数集中必有可列子集和发散),概率论只对可列并集建立求和理论。因此公理限定为可列可加性,既足以处理极限运算,又避免上述矛盾。

**答案原文**

若允许不可列可加,$[0,1]$ 的概率会是不可列多个零之和 $=0$,与 $P([0,1])=1$ 矛盾;故可加性只定义在可列并集上。

## 126. prob-046

内容 SHA256：`69f8c89128bdda3bcd6c89d13dc3e9c331d6df89fab7b2575f62e9c9d9da44e1`。

来源：reviews/codex-supervision/2026-10-06-scene-repair-takeover/math-correction-receipt.json；源 SHA256 `33c0a0bc6bc5281f513bf17fdda3de2a178f4700b9703bdcce7465e7cbcc0ef9`；行 —，JSON pointer `/corrections/8/record`。

**题干**

用几何图形直观展示可列可加性：把单位正方形分割成可列个互不相交的小矩形。

**过程**

取半开单位正方形 $\Omega=[0,1)\times[0,1)$，面积为 $1$。令 $R_k=[1-2^{-(k-1)},1-2^{-k})\times[0,1)$，$k\ge1$。这些矩形两两不交，且 $\bigcup_{k=1}^{\infty}R_k=\Omega$，$\operatorname{area}(R_k)=2^{-k}$。前 $N$ 个矩形的面积和为 $S_N=\sum_{k=1}^{N}2^{-k}=1-2^{-N}$，剩余面积为 $2^{-N}\to0$，所以由面积测度的可列可加性，$\operatorname{area}(\Omega)=\sum_{k=1}^{\infty}\operatorname{area}(R_k)=1$。若画闭单位正方形，只多出零面积边界，不改变面积等式。该例展示可列可加性，不能把单个图例当作对所有可测集合的一般证明。

**答案原文**

可列可加性成立：各矩形面积构成几何级数 $\sum_{k=1}^{\infty} \frac{1}{2^k}$，其和为 $1$，恰等于单位正方形的总面积

## 127. eval-linalg-021-s3

内容 SHA256：`6b05f162b00ca08da0ec13612228996a915e49a95fb183f67e345bc75876a319`。

来源：reviews/codex-supervision/history-from-code/recheck-68c51be/data/v2/eval/dataset_eval.json；源 SHA256 `1de2df62edd0b01403df813c80edc3a5a9dbf1791f0b223d8e0f107ccee55e6e`；行 —，JSON pointer `/257`。

**题干**

判断二次型 $f=x^2+2y^2+3z^2+2xy+2xz+4yz$ 是否正定。

**过程**

对 $A$ 做同步行列变换（合同变换）。第一步：$R_2\leftarrow R_2-R_1$、$R_3\leftarrow R_3-R_1$、$C_2\leftarrow C_2-C_1$、$C_3\leftarrow C_3-C_1$，得 $\begin{pmatrix}1&0&0\\0&1&1\\0&1&2\end{pmatrix}$；第二步：$R_3\leftarrow R_3-R_2$、$C_3\leftarrow C_3-C_2$，得 $\begin{pmatrix}1&0&0\\0&1&0\\0&0&1\end{pmatrix}=I$。即存在可逆矩阵 $C$ 使 $C^TAC=I$，故 $A$ 正定。

**答案原文**

正定

## 128. draft-c17-05

内容 SHA256：`6b204140e018336d1f5d822e6adadccb4133cd7a4c303a1206d347878babefa3`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft.jsonl；源 SHA256 `9aa29561a8f8dc1a725169c6fa9b3fb558e5c2bed5b0d43940d42e9b5ff823e3`；行 10，JSON pointer `/`。

**题干**

推导平面的截距式方程，并求过点 $P(1,2,3)$ 且在三坐标轴上的截距都相等且不为零(即平面不过原点)的平面方程。

**过程**

设平面在 $x,y,z$ 轴上的截距分别为 $a,b,c$($abc\neq0$),即平面过 $(a,0,0),(0,b,0),(0,0,c)$。三点确定平面:设一般式 $Ax+By+Cz+D=0$($D\neq0$),代入三点得 $Aa+D=0,Bb+D=0,Cc+D=0$,即 $A=-\frac Da,B=-\frac Db,C=-\frac Dc$,代入并除以 $-D$:$\frac{x}{a}+\frac{y}{b}+\frac{z}{c}=1$,即截距式。截距相等:设 $a=b=c=t\neq0$,方程为 $\frac{x+y+z}{t}=1$,即 $x+y+z=t$。过 $P(1,2,3)$:$1+2+3=t$,$t=6$。故所求平面为 $x+y+z=6$。(若允许零截距,则过原点且过 $P$ 的平面有无穷多个,条件不足以唯一确定,故本题约定截距非零。)

**答案原文**

截距式:$\frac{x}{a}+\frac{y}{b}+\frac{z}{c}=1$($abc\neq0$);$x+y+z=6$。

## 129. draft-c02-05

内容 SHA256：`6b58a68219949b95b8491fcf8dc3d2c0778aecddf679d11a8c467d7ca30001e3`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-07.jsonl；源 SHA256 `b14a41ee891c643ede8cbc2986187adaa63a4bce93c398f0cce2544a7bc123a5`；行 5，JSON pointer `/`。

**题干**

证明 $p$ 积分 $\int_1^{+\infty}\frac{1}{x^p}\,dx$ 当且仅当 $p>1$ 时收敛。

**过程**

当 $p\neq1$ 时,$\int_1^R x^{-p}dx=\left.\frac{x^{1-p}}{1-p}\right|_1^R=\frac{R^{1-p}-1}{1-p}$。若 $p>1$,则 $1-p<0$,$R^{1-p}\to0$,故极限为 $\frac{1}{p-1}$,收敛。若 $p<1$,则 $1-p>0$,$R^{1-p}\to+\infty$,发散。当 $p=1$ 时,$\int_1^R\frac{dx}{x}=\ln R\to+\infty$,发散。综上,收敛当且仅当 $p>1$(且收敛值为 $\frac{1}{p-1}$)。

**答案原文**

收敛当且仅当 $p>1$,此时值为 $\frac{1}{p-1}$;证明见解法。

## 130. prob-046

内容 SHA256：`6bbd7b93e2c5293c66fdec1818574767c3d314b2eef26bc72f674c99eeb524af`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/0b25e054de83f8b330855e402cec271d3ef98ba02f4f5998b0711d2cf2aa9222.bin；源 SHA256 `0b25e054de83f8b330855e402cec271d3ef98ba02f4f5998b0711d2cf2aa9222`；行 9，JSON pointer `/`。

**题干**

用几何图形直观展示可列可加性：把单位正方形分割成可列个互不相交的小矩形。

**过程**

将面积为 $1$ 的正方形依次分割：第一个矩形面积为 $\frac{1}{2}$，第二个为 $\frac{1}{4}$，第三个为 $\frac{1}{8}$，依此类推。随着分割次数趋向无穷，矩形面积构成几何级数 $\sum_{k=1}^{\infty} \frac{1}{2^k}$，其和为 $1$。这直观展示了可列可加性。

**答案原文**

1，即所有事件概率之和为1

## 131. draft-c01-05

内容 SHA256：`6c40db967dfb5b2d7fd83e2d9c02834d7858858cab884df650ebc2a59a196574`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft.jsonl；源 SHA256 `13fe6a370d3c46ae8ca6c1b16c9cd98fbedcc8648087f11a70ff046951db5479`；行 5，JSON pointer `/`。

**题干**

求抛物线 $y=x^2$ 与 $y=-x^2+2x+1$ 的公切线；若不存在，请说明理由。

**过程**

设公切线与 $y=x^2$ 相切于点 $(a,a^2)$，切线方程为 $y=2ax-a^2$；与 $y=-x^2+2x+1$ 相切于点 $(c,-c^2+2c+1)$，切线方程为 $y=(-2c+2)x+c^2+1$。若两直线为同一直线，则比较系数得 $2a=-2c+2$ 与 $-a^2=c^2+1$。由第一式得 $a=1-c$，代入第二式得 $-(1-c)^2=c^2+1$，即 $c^2-c+1=0$，其判别式 $\Delta=(-1)^2-4=-3<0$，无实根。故满足条件的 $c$(进而 $a$)不存在，即两抛物线没有公切线。

**答案原文**

公切线不存在(推导得 $c^2-c+1=0$，判别式 $-3<0$ 无实根)。

## 132. draft-c02-04

内容 SHA256：`6e6578e580c278c2e00131811bc116f31652e610ea97f96a2a284f099766c470`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-07.jsonl；源 SHA256 `b14a41ee891c643ede8cbc2986187adaa63a4bce93c398f0cce2544a7bc123a5`；行 4，JSON pointer `/`。

**题干**

用分部积分法计算 $\int_0^{+\infty}xe^{-x}\,dx$。

**过程**

在$[0,R]$上分部积分：$\int_0^Rxe^{-x}dx=[-xe^{-x}]_0^R+\int_0^Re^{-x}dx=1-(R+1)e^{-R}$。对$R>0$，指数级数给出$e^R\ge R^2/2$，故$0\le Re^{-R}\le2/R\to0$；且$e^{-R}\to0$。因此反常积分收敛，值为$1$。

**答案原文**

积分值为 $1$。

## 133. draft-c27-03

内容 SHA256：`6eae6942005f3d948960e2bd9f10fcfc7bf1b940274c858d14c32963393eca16`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft.jsonl；源 SHA256 `e019465093b291bd83fb6ae20f3eefc40a96df3e5137a246ad8813dd03f87b34`；行 3，JSON pointer `/`。

**题干**

用对角化计算 $A^{10}$,其中 $A=\begin{pmatrix}1&2\\0&3\end{pmatrix}$。

**过程**

$A$ 的特征值为 $1$ 与 $3$。$\lambda=1$:$(A-I)v=0$ 得 $v=(1,0)$;$\lambda=3$:$(A-3I)v=0$,即 $\begin{pmatrix}-2&2\\0&0\end{pmatrix}v=0$,得 $v=(1,1)$。取 $P=\begin{pmatrix}1&1\\0&1\end{pmatrix}$,则 $P^{-1}=\begin{pmatrix}1&-1\\0&1\end{pmatrix}$,$D=\mathrm{diag}(1,3)$,$A=PDP^{-1}$。$A^{10}=PD^{10}P^{-1}=\begin{pmatrix}1&1\\0&1\end{pmatrix}\begin{pmatrix}1&0\\0&3^{10}\end{pmatrix}\begin{pmatrix}1&-1\\0&1\end{pmatrix}=\begin{pmatrix}1&1\\0&1\end{pmatrix}\begin{pmatrix}1&-1\\0&3^{10}\end{pmatrix}=\begin{pmatrix}1&3^{10}-1\\0&3^{10}\end{pmatrix}=\begin{pmatrix}1&59048\\0&59049\end{pmatrix}$。

**答案原文**

$A^{10}=\begin{pmatrix}1&3^{10}-1\\0&3^{10}\end{pmatrix}=\begin{pmatrix}1&59048\\0&59049\end{pmatrix}$。

## 134. draft-c15-05

内容 SHA256：`6f82c4bdee88afd58f01ab0e0d9488df3087873f22b66fbb4423bd8c91a80c3a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft.jsonl；源 SHA256 `9aa29561a8f8dc1a725169c6fa9b3fb558e5c2bed5b0d43940d42e9b5ff823e3`；行 5，JSON pointer `/`。

**题干**

证明直线与平面夹角公式 $\sin\varphi=\frac{|d\cdot n|}{|d|\,|n|}$，并讨论 $d\cdot n=0$ 与 $d\times n=0$ 两个退化分支对应的位置关系及判定方法。

**过程**

记 $\psi$ 为直线方向 $d$ 与平面法向量 $n$ 的夹角(取 $[0,\frac{\pi}{2}]$ 内的值)。正交分解:$d=d'+\frac{d\cdot n}{|n|^2}n$,其中 $d'$ 位于平面的方向子空间内且 $d'\perp n$。当 $d'$ 非零时,直线与其投影线(方向 $d'$)的夹角 $\varphi$ 满足:在由 $d,d'$ 与法向分量张成的直角三角形中,$d$ 与 $d'$ 的夹角为 $\varphi$,$d$ 与 $n$ 的夹角为 $\psi$,故 $\varphi+\psi=\frac{\pi}{2}$,即 $\sin\varphi=\cos\psi=\frac{|d\cdot n|}{|d|\,|n|}$;当 $d'=0$(即 $d\parallel n$)时,直线垂直于平面,投影退化为一个点,约定夹角 $\varphi=\frac{\pi}{2}$,此时公式右端 $\frac{|d\cdot n|}{|d||n|}=1$,仍成立。退化分支一:$d\cdot n=0\iff d\perp n\iff l\parallel\pi$;此时若 $l$ 上某点在 $\pi$ 上,则 $l\subset\pi$(直线完全落在平面内),否则 $l$ 与 $\pi$ 平行无公共点——判定需代入直线上一点。退化分支二:$d\times n=0\iff d\parallel n\iff l\perp\pi$,此时直线与平面恰有一个交点(垂足)。非退化情形($d\cdot n\neq0$ 且 $d\times n\neq0$):直线与平面斜交于一点。

**答案原文**

公式由 $\varphi+\psi=\frac{\pi}{2}$ 与 $\cos\psi=\frac{|d\cdot n|}{|d||n|}$ 得;退化分支:$d\cdot n=0\iff l\parallel\pi$(再以点是否在面内区分含于面内/平行),$d\times n=0\iff l\perp\pi$(证明见解法)。

## 135. linalg-068

内容 SHA256：`6fcb39cbb56067ffb47f5722431990cefec87db47aedea59b678c5d2e890d50b`。

来源：reviews/codex-supervision/history-from-code/clone-check/reviews/2026-10-03-prep-recheck/results.json；源 SHA256 `078e6bbd0c76184d36494245ab5fa7c1bbb875cfa226cdcd88c09d9c47c6d3c8`；行 —，JSON pointer `/answer_record_snapshot/linalg-068`。

**题干**

将实对称矩阵 $A=\begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ 正交对角化。

**过程**

特征值 $\lambda_1=3$ 对应特征向量 $(1,1)^T/\sqrt{2}$，$\lambda_2=1$ 对应 $(1,-1)^T/\sqrt{2}$。两个特征向量正交。正交矩阵 $Q=\frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$，$Q^TAQ=\operatorname{diag}(3,1)$。

**答案原文**

$Q=\frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$，$Q^TAQ=\operatorname{diag}(3,1)$，即正交对角化把二次型化为对角标准形

## 136. draft-c13-04

内容 SHA256：`6fe271535172f43eef4b989e386f855e5a82ef85d671e696f212ed76a361ea84`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft.jsonl；源 SHA256 `4a8930a557e05b01cec58257879ecd5bd9679b9c08e3e478767c363642ebe382`；行 4，JSON pointer `/`。

**题干**

求级数 $\sum_{n=2}^{\infty}\frac{1}{n^2-1}$ 的和。

**过程**

部分分式：$\frac{1}{n^2-1}=\frac12\left(\frac{1}{n-1}-\frac{1}{n+1}\right)$。前 $N$ 项和 $S_N=\frac12\sum_{n=2}^{N}\left(\frac{1}{n-1}-\frac{1}{n+1}\right)=\frac12\left(1+\frac12-\frac{1}{N}-\frac{1}{N+1}\right)$(正项只留下 $n=2$ 的 $\frac11$ 与 $\frac12$，负项只留下 $\frac1N$ 与 $\frac1{N+1}$)。令 $N\to\infty$ 得 $S=\frac12\cdot\frac32=\frac34$。

**答案原文**

和为 $\frac34$。

## 137. draft-c11-04

内容 SHA256：`701dcca90396e1e5e69e2a88b46172110c752aa9420e15622bf68fbb087f4ec9`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-02.jsonl；源 SHA256 `286625ebf0f88cca49b14f36be4bab4e5f3b29ecc0764226b7ebb5fb61a16527`；行 4，JSON pointer `/`。

**题干**

求幂级数 $\sum_{n=1}^{\infty}\frac{nx^n}{n!}$ 的收敛域与和函数。

**过程**

比值法：$\lim_{n\to\infty}\left|\frac{(n+1)x^{n+1}/(n+1)!}{nx^n/n!}\right|=\lim_{n\to\infty}\frac{n+1}{n}\cdot\frac{|x|}{n+1}=0$，对一切实数 $x$ 收敛，收敛域为 $\mathbb R$。求和：$\sum_{n=1}^{\infty}\frac{nx^n}{n!}=\sum_{n=1}^{\infty}\frac{x^n}{(n-1)!}=x\sum_{m=0}^{\infty}\frac{x^m}{m!}=xe^x$。逐项运算的合法性由该级数在每个紧区间上一致收敛保证(指数级数)。

**答案原文**

收敛域为 $\mathbb R$;和函数 $S(x)=xe^x$。

## 138. geom-025

内容 SHA256：`70434d822edbb7c1fd34a4ab95a6d2579baffb14b0a01e00c34932cccbc8b5f5`。

来源：reviews/codex-supervision/2026-10-05-math-template-followup-v2/corrected-candidates/dataset_geom.jsonl；源 SHA256 `0c7b3c0833d3f4d0d43ced4108022af41ceaa78686d85664d45ef2194580e662`；行 3，JSON pointer `/`。

**题干**

指出方程 $x^2 + y^2 - z^2 = 1$ 表示的二次曲面类型，并说明其与平面 $z = k$ 的交线形状。

**过程**

该方程为单叶双曲面。用平面 $z = k$ 去截，得到 $x^2 + y^2 = 1 + k^2$，这是半径为 $\sqrt{1+k^2}$ 的圆。随着 $|k|$ 增大，截面圆的半径逐渐增大，呈现出两头大、中间细的“沙漏”形状。单叶双曲面也是一种直纹面，存在两组直线族。

**答案原文**

单叶双曲面，平行于 xOy 平面的截面为圆

## 139. draft-c33-04

内容 SHA256：`70b02dcef1df59f4dfb432256fa18147521d8549eb30a0459a08e01b7b0f6b59`。

来源：reviews/codex-supervision/2026-10-05-pdf-repair-supervision/followup-2327/negative-fixtures/record-binding-tamper/batch-02/draft-codex-repair-v5.jsonl；源 SHA256 `1bb50f4fbecdca7b429e9342f7f2f579731dd9582269a0e5e7b1c639829ec91b`；行 9，JSON pointer `/`。

**题干**

求矩阵 $A=\begin{pmatrix}1&0\\0&1\\1&1\end{pmatrix}$ 的一个左逆与矩阵 $B=\begin{pmatrix}1&0&1\\0&1&1\end{pmatrix}$ 的一个右逆，并说明这两种单边逆的区别与不唯一性。

**过程**

$A$ 为 $3\times2$ 列满秩矩阵。取 $L=\begin{pmatrix}1&0&0\\0&1&0\end{pmatrix}$，则 $LA=\begin{pmatrix}1&0\\0&1\end{pmatrix}=I_2$，故 $L$ 是 $A$ 的一个左逆。$B$ 为 $2\times3$ 行满秩矩阵。取 $R=\begin{pmatrix}1&0\\0&1\\0&0\end{pmatrix}$，则 $BR=\begin{pmatrix}1&0\\0&1\end{pmatrix}=I_2$，故 $R$ 是 $B$ 的一个右逆。区别:列满秩的「高瘦」矩阵只可能有左逆($LA=I$),行满秩的「宽扁」矩阵只可能有右逆($BR=I$);只有方阵且可逆时才存在同时满足两侧的双边逆。不唯一性:$A$ 的左逆一般形式为 $\begin{pmatrix}1-t&-t&t\\-s&1-s&s\end{pmatrix}$($t,s$ 为任意实数),$L$ 对应 $t=s=0$,$\begin{pmatrix}0&-1&1\\1&2&-1\end{pmatrix}$ 对应 $t=1,s=-1$,也是左逆;$B$ 的右逆同理不唯一。一般地，$m\times n$ 矩阵有左逆当且仅当列满秩（故$m\ge n$），有右逆当且仅当行满秩（故$m\le n$）。严格高瘦/宽扁情形的相应单边逆不唯一；可逆方阵的左右逆一致且唯一。因本题 $B=A^{\mathsf T}$，全部右逆可写成 $R(t,s)=\begin{pmatrix}1-t&-s\\-t&1-s\t&s\end{pmatrix}$，有 $BR(t,s)=I_2$。

**答案原文**

$L=\begin{pmatrix}1&0&0\\0&1&0\end{pmatrix}$ 满足 $LA=I_2$，$R=\begin{pmatrix}1&0\\0&1\\0&0\end{pmatrix}$ 满足 $BR=I_2$。一般左逆要求列满秩、$m\ge n$，右逆要求行满秩、$m\le n$；本题两种单边逆均不唯一，可逆方阵则有唯一双边逆。

## 140. draft-c31-04

内容 SHA256：`73835aa92ec92f3dcaa899809cc05bffa40a949b924bce784f57d4c9ba9772c8`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-05/draft-codex-repair-v2.jsonl；源 SHA256 `7365ad8b2df03906800f50e46c3f16fb8590eeb7cd45b5f9750f7e98d01c5e1e`；行 14，JSON pointer `/`。

**题干**

用克拉默法则解方程组 $\begin{cases}kx+y=1\\ x+ky=k\end{cases}$($k$ 为参数),并讨论奇异情形($D=0$)时的解。

**过程**

$D=k^2-1=(k-1)(k+1)$。当 $k\neq\pm1$ 时,$D_x=\begin{vmatrix}1&1\k&k\end{vmatrix}=k-k=0$,$D_y=\begin{vmatrix}k&1\\1&k\end{vmatrix}=k^2-1$,故唯一解 $x=\frac{0}{D}=0$,$y=\frac{D}{D}=1$。当 $k=1$ 时,两方程均为 $x+y=1$,无穷多解。当 $k=-1$ 时,方程为 $-x+y=1$ 与 $x-y=-1$,后者乘以 $-1$ 恰为前者,仍是同一条直线,无穷多解。注意:本题两个奇异值均落在无穷多解分支,与常见的「一个奇异值无解、另一个无穷多解」的例子不同;克拉默法则仅在 $D\neq0$ 时适用,$D=0$ 时必须改用初等变换/秩判断。

**答案原文**

$k\neq\pm1$ 时唯一解 $x=0,y=1$;$k=1$ 与 $k=-1$ 时均有无穷多解(两方程退化为同一直线)。

## 141. prob-038

内容 SHA256：`73d511336c89c5b355190e114140ad4127f555c45b511a71528208b59ea05bae`。

来源：reviews/codex-supervision/2026-10-06-scene-repair-takeover/math-correction-receipt.json；源 SHA256 `33c0a0bc6bc5281f513bf17fdda3de2a178f4700b9703bdcce7465e7cbcc0ef9`；行 —，JSON pointer `/corrections/4/record`。

**题干**

已知 $P(A)=\frac{3}{5}$，$P(B)=\frac{2}{5}$，且 $P(A\cap B)=\frac{1}{5}$。求 $P(A\mid B)$ 和 $P(B\mid A)$。

**过程**

由条件概率定义，$P(A\mid B)=\frac{P(A\cap B)}{P(B)}=\frac{1/5}{2/5}=\frac{1}{5}\cdot\frac{5}{2}=\frac{1}{2}$；$P(B\mid A)=\frac{P(A\cap B)}{P(A)}=\frac{1/5}{3/5}=\frac{1}{5}\cdot\frac{5}{3}=\frac{1}{3}$。两条件事件的概率均为正，定义适用。

**答案原文**

$P(A\mid B)=\frac{1}{2}$，$P(B\mid A)=\frac{1}{3}$。

## 142. draft-c18-01

内容 SHA256：`7424c2a88b042e0fd82993a473f6de5a6685bbb0eb733a2bd21e1440811d9174`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft.jsonl；源 SHA256 `4a8930a557e05b01cec58257879ecd5bd9679b9c08e3e478767c363642ebe382`；行 6，JSON pointer `/`。

**题干**

求点 $P(2,1,1)$ 到平面 $\pi: x+2y+2z=3$ 的距离与投影点。

**过程**

平面法向量 $n=(1,2,2)$，$|n|=3$。有向距离 $\frac{n\cdot P-3}{|n|}=\frac{2+2+2-3}{3}=1$，故距离为 $1$。投影点 $Q=P-\frac{n\cdot P-3}{|n|^2}n=(2,1,1)-\frac{3}{9}(1,2,2)=(2,1,1)-(\frac13,\frac23,\frac23)=(\frac53,\frac13,\frac13)$。验证:$Q$ 在平面上($\frac53+\frac23+\frac23=3$)且 $P-Q=(\frac13,\frac23,\frac23)\parallel n$。

**答案原文**

距离为 $1$;投影点为 $(\frac53,\frac13,\frac13)$。

## 143. eval-linalg-019-s2

内容 SHA256：`746ecd18b6fd3a56cf7646b144dd3171a8e2f177250a41e1a2815511d3924890`。

来源：reviews/codex-supervision/history-from-code/recheck-68c51be/data/v2/eval/dataset_eval.json；源 SHA256 `1de2df62edd0b01403df813c80edc3a5a9dbf1791f0b223d8e0f107ccee55e6e`；行 —，JSON pointer `/250`。

**题干**

将二次型 $f(x,y)=2x^2+2xy+3y^2$ 化为标准形，并说明其正定性。

**过程**

矩阵 $A=\begin{pmatrix}2&1\\1&3\end{pmatrix}$。特征方程 $|\lambda I-A|=(\lambda-2)(\lambda-3)-1=\lambda^2-5\lambda+5=0$，特征值 $\lambda_1=\dfrac{5+\sqrt5}{2}$、$\lambda_2=\dfrac{5-\sqrt5}{2}$（均正）。沿对应特征方向做正交变换，得标准形 $\dfrac{5+\sqrt5}{2}\xi^2+\dfrac{5-\sqrt5}{2}\eta^2$。特征值全正故正定。

**答案原文**

配方法标准形 $2u^2+\dfrac{5}{2}v^2$（$u=x+\dfrac{y}{2}$，$v=y$）；正交标准形 $\dfrac{5+\sqrt5}{2}\xi^2+\dfrac{5-\sqrt5}{2}\eta^2$；正定

## 144. draft-c01-02

内容 SHA256：`758d323e166c4c0344c16344f1d4cc3fa9ceecdebde854e7d1544998a337df45`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft.jsonl；源 SHA256 `13fe6a370d3c46ae8ca6c1b16c9cd98fbedcc8648087f11a70ff046951db5479`；行 2，JSON pointer `/`。

**题干**

求椭圆 $x^2+4y^2=8$ 在点 $(2,1)$ 处的切线方程。

**过程**

点 $(2,1)$ 满足 $2^2+4\cdot 1^2=8$，在椭圆上。对隐式方程两边关于 $x$ 求导：$2x+8y\cdot y'=0$，即 $y'=-\frac{x}{4y}$。在点 $(2,1)$ 处，$y'=-\frac{2}{4\cdot 1}=-\frac{1}{2}$。由点斜式，切线为 $y-1=-\frac{1}{2}(x-2)$，整理得 $x+2y=4$。

**答案原文**

切线方程 $x+2y=4$(即 $y=-\frac{1}{2}x+2$)。

## 145. draft-c01-03

内容 SHA256：`7695745aa797e44a6e58cdd6a2806e8984bf5fb36ad252bd2886721ea3003b64`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft.jsonl；源 SHA256 `13fe6a370d3c46ae8ca6c1b16c9cd98fbedcc8648087f11a70ff046951db5479`；行 3，JSON pointer `/`。

**题干**

已知参数曲线 $\begin{cases}x=t^2\\ y=t^3-3t\end{cases}$。求曲线在 $t=2$ 对应点处的切线方程，并求出曲线上所有水平切线与竖直切线。

**过程**

参数求导：$\frac{dx}{dt}=2t$，$\frac{dy}{dt}=3t^2-3$，故 $\frac{dy}{dx}=\frac{3t^2-3}{2t}$。当 $t=2$ 时，对应点为 $(4,2)$，斜率为 $\frac{12-3}{4}=\frac{9}{4}$，切线为 $y-2=\frac{9}{4}(x-4)$，即 $y=\frac{9}{4}x-7$。水平切线需 $\frac{dy}{dt}=0$ 且 $\frac{dx}{dt}\neq 0$：$3t^2-3=0$ 得 $t=\pm 1$，对应点 $(1,-2)$ 与 $(1,2)$，切线分别为 $y=-2$ 与 $y=2$。竖直切线需 $\frac{dx}{dt}=0$ 且 $\frac{dy}{dt}\neq 0$：$2t=0$ 得 $t=0$，此时 $\frac{dy}{dt}=-3\neq 0$，对应点 $(0,0)$，切线为 $x=0$。

**答案原文**

$t=2$ 处切线 $y=\frac{9}{4}x-7$；水平切线 $y=-2$、$y=2$；竖直切线 $x=0$。

## 146. draft-c39-02

内容 SHA256：`787ec3347f917bb211d8b35717c37f08478f6f28d7a2f3f87b87bbffc051431a`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/28d2832a953c1046e1a5df5a429b1d9b5ea65c988e1936c2ec2fdeb28be2956b.bin；源 SHA256 `28d2832a953c1046e1a5df5a429b1d9b5ea65c988e1936c2ec2fdeb28be2956b`；行 —，JSON pointer `/2`。

**题干**

设 $T:\mathbb R^2\to\mathbb R^3$ 由 $T(x,y)=(x+y,\,x-y,\,2x)$ 定义。判断 $T$ 是否单射、是否满射，并求核与像的维数。

**过程**

核:解 $x+y=0,x-y=0,2x=0$,得 $x=y=0$,故 $\ker T=\{0\}$,$\dim\ker T=0$,由秩-零度定理 $\dim\mathrm{im}\,T=2-0=2$。单射:核为 $\{0\}$ ⟺ 单射,故 $T$ 单射。满射:像的维数 $2<3$,故 $T$ 非满射(像是 $\mathbb R^3$ 中由 $T(1,0)=(1,1,2)$ 与 $T(0,1)=(1,-1,0)$ 张成的平面)。

**答案原文**

单射但非满射;$\\ker T=\\{0\\}$(维数 $0$),$\\dim\\mathrm{im}\\,T=2$。

## 147. draft-c16-02

内容 SHA256：`795e21c72261d0f5a266c24d3b6e8a3a72a3a6fd36b9d35eb33267162fe2c9a2`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft.jsonl；源 SHA256 `afcd74e3e4d285e77802f29ab182f9dce80cfe5833b983feb8af34694ed15331`；行 12，JSON pointer `/`。

**题干**

求两平行直线 $l_1$：过点 $(1,2,3)$、方向 $(1,1,1)$ 与 $l_2$：过点 $(2,3,3)$、方向 $(1,1,1)$ 之间的距离。

**过程**

两直线方向相同，且 $P_2-P_1=(1,1,0)$ 与方向 $(1,1,1)$ 不平行，故为平行不重合直线。距离公式 $d=\frac{|(P_2-P_1)\times d|}{|d|}$。计算 $(1,1,0)\times(1,1,1)=(1\times1-0\times1,\,0\times1-1\times1,\,1\times1-1\times1)=(1,-1,0)$，$|(1,-1,0)|=\sqrt2$，$|d|=\sqrt3$，故 $d=\frac{\sqrt2}{\sqrt3}=\frac{\sqrt6}{3}$。

**答案原文**

距离为 $\frac{\sqrt6}{3}$。

## 148. geom-023

内容 SHA256：`7a44e34a43bc783cafbc6fbb07952d0f5fd01d207a86e4be28ad2910f0859472`。

来源：reviews/codex-supervision/2026-10-05-math-template-followup-v2/corrected-candidates/dataset_geom.jsonl；源 SHA256 `0c7b3c0833d3f4d0d43ced4108022af41ceaa78686d85664d45ef2194580e662`；行 2，JSON pointer `/`。

**题干**

求点 $P(2, 1, 3)$ 到平面 $\pi: 2x - y + 2z + 1 = 0$ 的距离，并求点 $P$ 在平面 $\pi$ 上的投影点。

**过程**

点到平面的距离公式 $d = \frac{|Ax_0 + By_0 + Cz_0 + D|}{\sqrt{A^2 + B^2 + C^2}} = \frac{|2\times2 + (-1)\times1 + 2\times3 + 1|}{\sqrt{4 + 1 + 4}} = \frac{|4 - 1 + 6 + 1|}{3} = \frac{10}{3}$。设投影点为 $Q(x, y, z)$，则过点 $P$ 且垂直于平面的直线方程为 $\frac{x-2}{2} = \frac{y-1}{-1} = \frac{z-3}{2} = t$，即 $x = 2 + 2t, y = 1 - t, z = 3 + 2t$。代入平面方程得 $2(2+2t) - (1-t) + 2(3+2t) + 1 = 0$，解得 $t = -\frac{10}{9}$。故投影点 $Q = (2 - \frac{20}{9}, 1 + \frac{10}{9}, 3 - \frac{20}{9}) = (-\frac{2}{9}, \frac{19}{9}, \frac{7}{9})$。

**答案原文**

距离为 $\frac{10}{3}$，投影点为 $(-\frac{2}{9}, \frac{19}{9}, \frac{7}{9})$

## 149. eval-linalg-032-s1

内容 SHA256：`7a8bfe95ef4676f80f1a2d7ab5c1dc00d246318cd3f13ca0998d965724f39e07`。

来源：reviews/codex-supervision/history-from-code/recheck-68c51be/data/v2/eval/dataset_eval.json；源 SHA256 `1de2df62edd0b01403df813c80edc3a5a9dbf1791f0b223d8e0f107ccee55e6e`；行 —，JSON pointer `/288`。

**题干**

求 λ-矩阵 $A(\lambda)=\begin{pmatrix}\lambda-1&1\\0&\lambda-1\end{pmatrix}$ 的不变因子与初等因子。

**过程**

一阶行列式因子 $D_1(\lambda)=\gcd(\lambda-1,\ 1,\ 0,\ \lambda-1)=1$（含元素 1，故为 1）。二阶行列式因子 $D_2(\lambda)=\det A(\lambda)=(\lambda-1)^2$。不变因子 $d_1=D_1=1$，$d_2=\dfrac{D_2}{D_1}=(\lambda-1)^2$。初等因子为不变因子的不可约因式幂：$(\lambda-1)^2$。

**答案原文**

不变因子 $1,(\lambda-1)^2$；初等因子 $(\lambda-1)^2$

## 150. synthetic

内容 SHA256：`7a97f6f70c93c0c23296227196b788a7f982be1012e9b731cf7f8cc05a03bab1`。

来源：reviews/codex-supervision/history-from-code/pytest-68c51be/test_nonfrozen_report_force_st0/input.jsonl；源 SHA256 `099ffc970bdd55acaafe0cd44d2735b6f85a6842d5ee21a59eb2323241ed2759`；行 1，JSON pointer `/`。

**题干**

synthetic task

**过程**

synthetic explanation

**答案原文**

1

## 151. eval-linalg-014-s3

内容 SHA256：`7b602c644cd8add82ffbed658ad325116fcc6e1905f9f8b855c05c1dffd97306`。

来源：reviews/codex-supervision/history-from-code/recheck-68c51be/data/v2/eval/dataset_eval.json；源 SHA256 `1de2df62edd0b01403df813c80edc3a5a9dbf1791f0b223d8e0f107ccee55e6e`；行 —，JSON pointer `/236`。

**题干**

求矩阵 $A=\begin{pmatrix}0&1\\1&0\end{pmatrix}$ 的特征值与特征向量，并说明其几何意义。

**过程**

$A^2=I$（两次交换复原，即 $A$ 是对合矩阵）。若 $Av=\lambda v$，则 $v=A^2v=\lambda^2v$，故 $\lambda^2=1$，$\lambda=\pm 1$，与解法一一致。再由 $(A-I)$ 与 $(A+I)$ 的秩均为 1，两特征值各对应一维特征空间。

**答案原文**

特征值 $\lambda_1=1$（特征向量 $(1,1)^T$），$\lambda_2=-1$（特征向量 $(1,-1)^T$）；$A$ 是关于直线 $y=x$ 的反射

## 152. draft-c35-03

内容 SHA256：`7b9dfd1b83a49299123c0811fcdf3b99bbaf1d6191c1524d71095b5c876e0f59`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft.jsonl；源 SHA256 `afcd74e3e4d285e77802f29ab182f9dce80cfe5833b983feb8af34694ed15331`；行 3，JSON pointer `/`。

**题干**

求使二次型 $f(x,y)=x^2+2xy+ay^2$ 的秩为 $1$ 的参数 $a$ 的值；并分别求 $a=0$、$a=1$、$a=2$ 时的标准形与正负惯性指数。

**过程**

对应矩阵 $A=\begin{pmatrix}1&1\\1&a\end{pmatrix}$，$\det A=a-1$。秩为 $1$ 当且仅当所有二阶子式为零，即 $a-1=0$，故 $a=1$。$a=0$：$f=x^2+2xy=(x+y)^2-y^2$，标准形 $u^2-v^2$，惯性指数 $(1,1,0)$，秩 $2$。$a=1$：$f=x^2+2xy+y^2=(x+y)^2$，标准形 $u^2$，惯性指数 $(1,0,0)$，秩 $1$。$a=2$：$f=x^2+2xy+2y^2=(x+y)^2+y^2$，标准形 $u^2+v^2$，惯性指数 $(2,0,0)$，秩 $2$。

**答案原文**

秩为 $1$ 当且仅当 $a=1$。$a=0$:标准形 $u^2-v^2$,惯性 $(1,1,0)$;$a=1$:$u^2$,惯性 $(1,0,0)$;$a=2$:$u^2+v^2$,惯性 $(2,0,0)$。

## 153. draft-c46-05

内容 SHA256：`7c5999d88bed0ab2670af0d897b0ab99637fc53789c66cf6c9d757d4de11084c`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-06.jsonl；源 SHA256 `756525876eec2bd8dbc8d8f3e28afbf61ca70fd4cab235964621646009a7ae5f`；行 15，JSON pointer `/`。

**题干**

平面上画有间距$d>0$的平行直线族。针长满足$0<l\le d$。针中点到最近直线的距离$Y\sim U(0,d/2)$，针与直线的无向锐角$\Theta\sim U(0,\pi/2)$，并假设$Y$与$\Theta$独立。求针与至少一条直线相交的概率。

**过程**

设针中点到最近直线的距离为 $y$($0\le y\le\frac d2$,均匀),针与直线的夹角为 $\theta$($0\le\theta\le\frac\pi2$,均匀)。针与直线相交当且仅当 $y\le\frac l2\sin\theta$。由独立均匀假设，联合密度为$4/(\pi d)$；样本空间面积为 $\frac d2\times\frac\pi2$,相交区域面积为 $\int_0^{\frac\pi2}\frac l2\sin\theta\,d\theta=\frac l2$。故 $P=\frac{\frac l2}{\frac{d\pi}{4}}=\frac{2l}{\pi d}$。

**答案原文**

相交概率为 $\frac{2l}{\pi d}$。

## 154. draft-c09-05

内容 SHA256：`7d0c15d1a3a472fd2fd56d46d975f11634777e12365ff1584812dcb5a82acd10`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft.jsonl；源 SHA256 `1d0950f73fad698178bef910eec1c19d5303cfe6bdabbcd76bddab903f05e44b`；行 15，JSON pointer `/`。

**题干**

求由曲线 $y=\sin x$($0\le x\le\pi$)与 $x$ 轴围成的区域分别绕 $x$ 轴与 $y$ 轴旋转所得旋转体的体积，并说明两种情况下所用方法的适用性。

**过程**

绕 $x$ 轴(圆盘法):$V_x=\pi\int_0^{\pi}\sin^2x\,dx=\pi\cdot\frac{\pi}{2}=\frac{\pi^2}{2}$。绕 $y$ 轴(柱壳法):区域到 $y$ 轴的距离为 $x$,高为 $\sin x$,$V_y=2\pi\int_0^{\pi}x\sin x\,dx$。分部积分:$\int_0^{\pi}x\sin x\,dx=\left.\sin x-x\cos x\right|_0^{\pi}=\pi$,故 $V_y=2\pi\cdot\pi=2\pi^2$。方法适用性:绕 $x$ 轴时截面为圆盘,圆盘法直接;绕 $y$ 轴时按 $y$ 切片需要把曲线分成两支反解 $x$,柱壳法(对 $x$ 积分)更自然。

**答案原文**

绕 $x$ 轴:$\frac{\pi^2}{2}$;绕 $y$ 轴:$2\pi^2$。

## 155. draft-c15-05

内容 SHA256：`7dc0e1b7f25ef0e01be1f7b21739d02c21b6cf6649bbc22cbec65f471338e367`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft-codex-repair-v2.jsonl；源 SHA256 `1478384b361b4abdbba0adf01feaa645ede07cb61c9ca7bde6a7e0f407a6edc2`；行 5，JSON pointer `/`。

**题干**

证明直线与平面夹角公式 $\sin\varphi=\frac{|d\cdot n|}{|d|\,|n|}$，并讨论 $d\cdot n=0$ 与 $d\times n=0$ 两个退化分支对应的位置关系及判定方法。

**过程**

???$p+td$???$n\cdot x=c$?$d,n\ne0$??$d$?????$d_{\parallel}=d-(d\cdot n)n/\|n\|^2$?$d_{\perp}=(d\cdot n)n/\|n\|^2$??$d_{\parallel}\ne0$?????$\phi\in[0,\pi/2)$??????????$\sin\phi=\|d_{\perp}\|/\|d\|=|d\cdot n|/(\|d\|\|n\|)$???????$d\parallel n$???$\pi/2$?????????$d\cdot n=0$?????????$n\cdot p=c$?????????????????????$d\times n=0$????????????????????????????

**答案原文**

$\sin\phi=|d\cdot n|/(\|d\|\|n\|)$?????????????$n\cdot p=c$??????????????????

## 156. eval-linalg-031-s3

内容 SHA256：`7e2155f05250eb4823957982fa2644ac3c7cda96dc67c4490ea0e29e1eb31258`。

来源：reviews/codex-supervision/history-from-code/recheck-68c51be/data/v2/eval/dataset_eval.json；源 SHA256 `1de2df62edd0b01403df813c80edc3a5a9dbf1791f0b223d8e0f107ccee55e6e`；行 —，JSON pointer `/287`。

**题干**

求矩阵 $A=\begin{pmatrix}2&1&0\\0&2&1\\0&0&2\end{pmatrix}$ 的最小多项式与若尔当标准形。

**过程**

解 $(A-2I)^2v\ne 0$ 而 $(A-2I)^3v=0$：取 $e_1=(1,0,0)^T$，则 $(A-2I)e_1=(0,0,0)$ 不满足；取 $e_3=(0,0,1)^T$：$(A-2I)e_3=(0,1,0)^T$，$(A-2I)^2e_3=(1,0,0)^T\ne 0$，$(A-2I)^3e_3=0$。链 $e_3\to Ne_3\to N^2e_3$ 长度为 3，故若尔当块为 $J_3(2)$。

**答案原文**

最小多项式 $(\lambda-2)^3$；若尔当标准形为 $A$ 本身（单个三阶块 $J_3(2)$）

## 157. draft-c40-01

内容 SHA256：`8098f41ededbef35eccc73ea0f44c932ffff32bca0c7eee316b98d99a89991f0`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft.jsonl；源 SHA256 `58ae126d6bd255576c005783f78e6ade29c9f0bd60b1c7fa2e0971ba6cad1a00`；行 1，JSON pointer `/`。

**题干**

求 λ-矩阵 $A(\lambda)=\mathrm{diag}(\lambda-1,\,(\lambda-1)^2)$ 的行列式因子、不变因子与初等因子。

**过程**

行列式因子:$D_1(\lambda)=\gcd(\lambda-1,(\lambda-1)^2)=\lambda-1$;$D_2(\lambda)=\det A(\lambda)=(\lambda-1)^3$。不变因子:$d_1=D_1=\lambda-1$;$d_2=\frac{D_2}{D_1}=\frac{(\lambda-1)^3}{\lambda-1}=(\lambda-1)^2$。初等因子:把各不变因子分解为互不相同的不可约因式的幂:$d_1$ 给出 $(\lambda-1)$,$d_2$ 给出 $(\lambda-1)^2$。故初等因子为 $\lambda-1$ 与 $(\lambda-1)^2$。

**答案原文**

行列式因子:$D_1=\lambda-1$,$D_2=(\lambda-1)^3$;不变因子:$d_1=\lambda-1$,$d_2=(\lambda-1)^2$;初等因子:$\lambda-1$ 与 $(\lambda-1)^2$。

## 158. draft-c48-02

内容 SHA256：`80d6cde08f84a445a8e29d42932f735417fb38f6f047a8d4a1454c7105a7192a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft.jsonl；源 SHA256 `bcd6ec3d0204b822f83440669662afcfe3ec7712fa4806d51506f98cb797b0c2`；行 7，JSON pointer `/`。

**题干**

设 $X\sim N(0,1)$。求 $P(-1\le X\le1)$、$P(-2\le X\le2)$、$P(-3\le X\le3)$(即 $3\sigma$ 规则)。

**过程**

由对称性,$P(-k\le X\le k)=2\Phi(k)-1$。$k=1$:$2\Phi(1)-1\approx2\times0.8413-1=0.6826$。$k=2$:$2\Phi(2)-1\approx2\times0.9772-1=0.9544$。$k=3$:$2\Phi(3)-1\approx2\times0.9987-1=0.9974$。即正态变量落在均值附近 $1,2,3$ 个标准差内的概率分别约为 $68\%$、$95\%$、$99.7\%$。

**答案原文**

$0.6826$、$0.9544$、$0.9974$($3\sigma$ 规则)。

## 159. draft-c43-03

内容 SHA256：`82d62c39052a184c072692af2d3c8a74cb83b8bedb08081ee49767fc18b0032e`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft.jsonl；源 SHA256 `b92648645c3b17a796e6b8938f67de934cddafd0cf192ab24ae006e5b423e27f`；行 3，JSON pointer `/`。

**题干**

设 $\mathbb R^3$ 的标准基为 $\varepsilon_1,\varepsilon_2,\varepsilon_3$，新基为 $\eta_1=(1,1,0)$，$\eta_2=(0,1,1)$，$\eta_3=(1,0,1)$。求新基的对偶基 $\{f_1,f_2,f_3\}$ 在标准对偶基 $\{\varepsilon^1,\varepsilon^2,\varepsilon^3\}$ 下的坐标。

**过程**

从标准基到新基的过渡矩阵(新基向量按列)$P=\begin{pmatrix}1&0&1\\1&1&0\\0&1&1\end{pmatrix}$。设新对偶基在标准对偶基下的坐标矩阵为 $C$(第 $i$ 行是 $f_i$ 的坐标),则配对条件 $f_i(\eta_j)=\delta_{ij}$ 等价于 $CP=I$,故 $C=P^{-1}$。求 $P^{-1}$:$\det P=2$,$P^{-1}=\frac12\begin{pmatrix}1&1&-1\\-1&1&1\\1&-1&1\end{pmatrix}$。故新对偶基为 $f_1=\frac12(\varepsilon^1+\varepsilon^2-\varepsilon^3)$,$f_2=\frac12(-\varepsilon^1+\varepsilon^2+\varepsilon^3)$,$f_3=\frac12(\varepsilon^1-\varepsilon^2+\varepsilon^3)$。验证(全部九个配对值):$f_1(\eta_1)=\frac12(1+1-0)=1$,$f_1(\eta_2)=\frac12(0+1-1)=0$,$f_1(\eta_3)=\frac12(1+0-1)=0$;$f_2(\eta_1)=\frac12(-1+1+0)=0$,$f_2(\eta_2)=\frac12(0+1+1)=1$,$f_2(\eta_3)=\frac12(-1+0+1)=0$;$f_3(\eta_1)=\frac12(1-1+0)=0$,$f_3(\eta_2)=\frac12(0-1+1)=0$,$f_3(\eta_3)=\frac12(1+0+1)=1$。全部满足 $f_i(\eta_j)=\delta_{ij}$ ✓。

**答案原文**

$f_1=\frac12(\varepsilon^1+\varepsilon^2-\varepsilon^3)$,$f_2=\frac12(-\varepsilon^1+\varepsilon^2+\varepsilon^3)$,$f_3=\frac12(\varepsilon^1-\varepsilon^2+\varepsilon^3)$(坐标取 $P^{-1}$ 的行)。

## 160. draft-c19-05

内容 SHA256：`8309e0518cc510f54f3ddda501ae809b96e3e7c22bfba6cadac1cf303b8464b4`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft.jsonl；源 SHA256 `9aa29561a8f8dc1a725169c6fa9b3fb558e5c2bed5b0d43940d42e9b5ff823e3`；行 15，JSON pointer `/`。

**题干**

证明:若曲面方程 $F(x,y,z)=0$ 不含变量 $z$(即 $F(x,y)=0$),则它表示母线平行于 $z$ 轴的柱面;并说明如何识别母线沿一般方向的柱面(以 $(x-z)^2+(y-z)^2=1$ 为例)。

**过程**

设 $(x_0,y_0)$ 满足 $F(x_0,y_0)=0$。对任意 $t$,点 $(x_0,y_0,t)$ 也满足 $F(x_0,y_0)=0$($F$ 不含 $z$),故过 $(x_0,y_0,0)$ 且平行于 $z$ 轴的整条直线都在曲面上;反之曲面上任一点 $(x,y,z)$ 的 $(x,y)$ 满足 $F(x,y)=0$,其所在的沿 $z$ 方向直线由准线点 $(x,y,0)$ 给出。故曲面是母线平行于 $z$ 轴的柱面(准线为 $xy$ 平面内曲线 $F(x,y)=0$)。一般方向:对方向 $v=(v_1,v_2,v_3)$($v_3\neq0$)的柱面,作变量替换 $u=x-\frac{v_1}{v_3}z$,$w=y-\frac{v_2}{v_3}z$($u,w$ 沿母线方向不变:方向导数 $\nabla_{(v_1,v_2,v_3)}(u)=v_1-\frac{v_1}{v_3}v_3=0$),若方程可写成 $G(u,w)=0$,则是母线沿 $v$ 的柱面。例:$(x-z)^2+(y-z)^2=1$ 中 $v=(1,1,1)$,$u=x-z$,$w=y-z$,方程即 $u^2+w^2=1$,故是母线沿 $(1,1,1)$ 的圆柱面。

**答案原文**

证明见解法(沿 $z$ 方向的整条直线在曲面上);一般方向用 $u=x-\frac{v_1}{v_3}z$,$w=y-\frac{v_2}{v_3}z$ 的替换识别。

## 161. prob-043

内容 SHA256：`83acb212e92a2dbab33e54a056a04daa129cbf13773c511efe1c7fa005ebaa1c`。

来源：reviews/codex-supervision/2026-10-06-scene-repair-takeover/math-correction-receipt.json；源 SHA256 `33c0a0bc6bc5281f513bf17fdda3de2a178f4700b9703bdcce7465e7cbcc0ef9`；行 —，JSON pointer `/corrections/7/record`。

**题干**

设 $X_1,X_2,\ldots$ 独立同分布，$E(X_i)=\mu$、$0<\operatorname{Var}(X_i)=\sigma^2<\infty$，$\overline X_n=n^{-1}\sum_{i=1}^nX_i$。写出标准化均值的中心极限定理，并区分其分布极限与原尺度 $\overline X_n$ 的极限；说明总体正态时有限样本的精确分布。

**过程**

设 $X_1,X_2,\ldots$ 独立同分布，$E(X_i)=\mu$、$0<\operatorname{Var}(X_i)=\sigma^2<\infty$，$\overline X_n=\frac{1}{n}\sum_{i=1}^n X_i$。中心极限定理的精确结论为 $Z_n=\frac{\sqrt n(\overline X_n-\mu)}{\sigma}\xrightarrow{d}N(0,1)$，即对每个 $t\in\mathbb R$，$\lim_{n\to\infty}P(Z_n\le t)=\Phi(t)$。未经标准化的均值有 $E(\overline X_n)=\mu$、$\operatorname{Var}(\overline X_n)=\sigma^2/n$，且 $\overline X_n\xrightarrow{P}\mu$，其极限分布为点质量 $\delta_\mu$，不能称为趋向固定的非退化正态分布。只有总体本身正态时，有限 $n$ 下才精确有 $\overline X_n\sim N(\mu,\sigma^2/n)$。

**答案原文**

$\frac{\sqrt n(\overline X_n-\mu)}{\sigma}\xrightarrow{d}N(0,1)$；$\operatorname{Var}(\overline X_n)=\sigma^2/n$ 且 $\overline X_n\xrightarrow{P}\mu$。

## 162. draft-c39-03

内容 SHA256：`856021f96b27364fa9205ae729ecadf0878662d19378588383cb82cf8126f22f`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft.jsonl；源 SHA256 `2a488597e92f7efdb6ec80074b147c9290e949fbeb4cbd114e293657e7c04776`；行 13，JSON pointer `/`。

**题干**

在实数域上次数不超过 $2$ 的多项式空间 $V$ 上定义微分映射 $D(p)=p'$。求 $D$ 的核、像与各自的维数，并验证秩-零度定理。

**过程**

$V=\{a_0+a_1x+a_2x^2\}$,$\dim V=3$。核:$p'=0\iff p$ 为常数多项式,故 $\ker D=\mathrm{span}\{1\}$,$\dim\ker D=1$。像:$D(a_0+a_1x+a_2x^2)=a_1+2a_2x$,像为次数不超过 $1$ 的多项式全体,$\dim\mathrm{im}\,D=2$。秩-零度:$1+2=3=\dim V$ ✓。

**答案原文**

$\\ker D=\\mathrm{span}\\{1\\}$(常数多项式,维数 $1$);$\\mathrm{im}\\,D=$ 次数不超过 $1$ 的多项式全体(维数 $2$);$1+2=3$ 满足秩-零度。

## 163. draft-c04-05

内容 SHA256：`86a8d0e6f1e815d1f2ae5f02b131967488d68d5db08f0ec10417f9cbc738421f`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-07.jsonl；源 SHA256 `b14a41ee891c643ede8cbc2986187adaa63a4bce93c398f0cce2544a7bc123a5`；行 10，JSON pointer `/`。

**题干**

设$L$是分段$C^1$的简单闭曲线，以正向（逆时针）遍历一次，围成区域$D$。由格林公式推导$A=\frac12\oint_L(x\,dy-y\,dx)$，并求椭圆$x^2/a^2+y^2/b^2=1$（$a,b>0$）的面积。

**过程**

在格林公式 $\oint_L P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)dxdy$ 中取 $P=-y,Q=x$,得 $\oint_L x\,dy-y\,dx=\iint_D(1+1)dxdy=2A$,故 $A=\frac12\oint_L x\,dy-y\,dx$。椭圆参数化:$x=a\cos t,y=b\sin t$($t:0\to2\pi$),则 $\oint x\,dy-y\,dx=\int_0^{2\pi}\left[(a\cos t)(b\cos t)-(b\sin t)(-a\sin t)\right]dt=ab\int_0^{2\pi}(\cos^2t+\sin^2t)\,dt=2\pi ab$。故 $A=\frac12\cdot2\pi ab=\pi ab$。

**答案原文**

面积公式 $A=\frac12\oint_L x\,dy-y\,dx$;椭圆面积为 $\pi ab$。

## 164. draft-c27-02

内容 SHA256：`86e2b1a2be204c63e3ec524035a069d193d9316454530b1fe84d03a43e91989b`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft.jsonl；源 SHA256 `e019465093b291bd83fb6ae20f3eefc40a96df3e5137a246ad8813dd03f87b34`；行 2，JSON pointer `/`。

**题干**

判断矩阵 $A=\begin{pmatrix}1&0&1\\0&2&0\\1&0&1\end{pmatrix}$ 是否可对角化；若可对角化，写出对角矩阵 $D$ 与可逆矩阵 $P$ 使 $P^{-1}AP=D$。

**过程**

特征多项式:按第一行展开,$|A-\lambda I|=(1-\lambda)[(2-\lambda)(1-\lambda)]-0+1[0-(2-\lambda)]=(2-\lambda)[(1-\lambda)^2-1]=(2-\lambda)(\lambda^2-2\lambda)=-\lambda(\lambda-2)^2$。特征值为 $0$ 与 $2$(二重)。$\lambda=2$:解 $(A-2I)v=0$,即 $\begin{pmatrix}-1&0&1\\0&0&0\\1&0&-1\end{pmatrix}v=0$,得 $v_1=v_3$,$v_2$ 任意,特征子空间 $\mathrm{span}\{(1,0,1),(0,1,0)\}$,维数 $2=$ 代数重数。$\lambda=0$:解 $Av=0$ 得 $v_1+v_3=0,v_2=0$,特征子空间 $\mathrm{span}\{(1,0,-1)\}$,维数 $1$。故 $A$ 可对角化:$D=\mathrm{diag}(2,2,0)$,$P=\begin{pmatrix}1&0&1\\0&1&0\\1&0&-1\end{pmatrix}$(验证:$AP=PD$,各列分别为对应特征值的特征向量)。

**答案原文**

可对角化:$D=\mathrm{diag}(2,2,0)$,$P=\begin{pmatrix}1&0&1\\0&1&0\\1&0&-1\end{pmatrix}$。

## 165. calc-series-018

内容 SHA256：`87f045f20fc4a5fb1e27b07456b70c8036b734b1fff022e8bb1f84f10953c406`。

来源：reviews/codex-supervision/2026-10-05-math-template-followup-v2/corrected-candidates/dataset_calc.jsonl；源 SHA256 `ca43b838d7309352ba84965c7de3ba071fab450a3c50483e61b5fda0bb9b8180`；行 2，JSON pointer `/`。

**题干**

已知级数 $\sum_{n=1}^{\infty} \frac{x^n}{n}$ 在 $(-1, 1)$ 内收敛，求其和函数，并求该级数逐项求导和逐项积分后的结果。

**过程**

和函数 $S(x) = -\ln(1-x)$。逐项求导：$S'(x) = \sum_{n=1}^{\infty} x^{n-1} = \frac{1}{1-x}$。逐项积分：$\int_0^x S(t) dt = \sum_{n=1}^{\infty} \frac{x^{n+1}}{n(n+1)} = (1-x)\ln(1-x) + x$。逐项求导和积分在题给 $(-1,1)$ 内合法，积分下限固定为0，所以积分常数由 $I(0)=0$ 决定。

**答案原文**

和函数 $S(x) = -\ln(1-x)$，逐项求导得 $\frac{1}{1-x}$，逐项积分得 $(1-x)\ln(1-x) + x$

## 166. draft-c36-03

内容 SHA256：`885fa0f0bfa8ec549227898455ca6c972ff9988648b228b051642dfe9071cfb9`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft.jsonl；源 SHA256 `13fe6a370d3c46ae8ca6c1b16c9cd98fbedcc8648087f11a70ff046951db5479`；行 8，JSON pointer `/`。

**题干**

求使二次型 $f(x,y,z)=x^2+2xy+2y^2+az^2$ 正定的参数 $a$ 的取值范围，并讨论 $a=0$ 与 $a<0$ 时二次型的情形。

**过程**

二次型对应矩阵 $A=\begin{pmatrix}1&1&0\\1&2&0\\0&0&a\end{pmatrix}$。顺序主子式：$\Delta_1=1>0$，$\Delta_2=1\times2-1\times1=1>0$，$\Delta_3=\det A=1\times(2a-0)-1\times(a-0)+0=a$。正定当且仅当三个顺序主子式全为正，故 $a>0$。当 $a=0$ 时，$f=x^2+2xy+2y^2=(x+y)^2+y^2\geq 0$，且 $f(0,0,1)=0$，存在非零解，故半正定但非正定。当 $a<0$ 时，取 $(x,y,z)=(0,0,1)$ 得 $f(0,0,1)=a<0$，二次型不定。

**答案原文**

正定当且仅当 $a>0$；$a=0$ 时半正定非正定；$a<0$ 时不定。

## 167. draft-c52-05

内容 SHA256：`8caa793e7761b793de2a0623878ba229f13c176eabaeda85e0c91ccdc11ee774`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft.jsonl；源 SHA256 `13fe6a370d3c46ae8ca6c1b16c9cd98fbedcc8648087f11a70ff046951db5479`；行 15，JSON pointer `/`。

**题干**

设 $X$ 与 $Y$ 相互独立且均服从区间 $(0,1)$ 上的均匀分布，$Z=X+Y$。求 $Z$ 的概率密度函数，并求 $P\left(\frac{1}{2}<Z<\frac{3}{2}\right)$。

**过程**

卷积法:$Z$ 的密度为 $f_Z(z)=\int f_X(x)f_Y(z-x)\,dx$。当 $0<z<1$ 时,$0<x<z$,$f_Z(z)=\int_0^z 1\,dx=z$;当 $1\leq z<2$ 时,$z-1<x<1$,$f_Z(z)=\int_{z-1}^1 1\,dx=2-z$。故 $f_Z(z)=z$($0<z<1$)、$f_Z(z)=2-z$($1\leq z<2$)、其余为 $0$(三角密度)。所求概率:$P\left(\frac{1}{2}<Z<\frac{3}{2}\right)=\int_{\frac{1}{2}}^1z\,dz+\int_1^{\frac{3}{2}}(2-z)\,dz=\left.\frac{z^2}{2}\right|_{\frac{1}{2}}^1+\left.\left(2z-\frac{z^2}{2}\right)\right|_1^{\frac{3}{2}}=\frac{3}{8}+\frac{3}{8}=\frac{3}{4}$。(几何验证:两端各剔除一个直角边为 $\frac{1}{2}$ 的小三角形,面积各 $\frac{1}{8}$。)

**答案原文**

$f_Z(z)=z$($0<z<1$)、$f_Z(z)=2-z$($1\leq z<2$)、其余为 $0$;$P\left(\frac{1}{2}<Z<\frac{3}{2}\right)=\frac{3}{4}$。

## 168. draft-c48-03

内容 SHA256：`8de63ed4cc31d83cc94f574c69a1877bc0c2b72b7d57802b1e89352e83f1c038`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft.jsonl；源 SHA256 `bcd6ec3d0204b822f83440669662afcfe3ec7712fa4806d51506f98cb797b0c2`；行 8，JSON pointer `/`。

**题干**

设 $X\sim N(\mu,4)$。求使 $P(X\le a)=0.95$ 的 $a$(用 $\mu$ 表示)。

**过程**

标准化:$P\left(Z\le\frac{a-\mu}{2}\right)=0.95$,即 $\Phi\left(\frac{a-\mu}{2}\right)=0.95$。查表 $\Phi(1.645)\approx0.95$,故 $\frac{a-\mu}{2}=1.645$,$a=\mu+2\times1.645=\mu+3.29$。

**答案原文**

$a=\mu+3.29$(即 $\mu+2\times1.645$)。

## 169. fixture-001

内容 SHA256：`9111539fb09f383ad3589b580f0089abc3f42da3fbb4e605f560bc5b7b1b2153`。

来源：reviews/codex-supervision/history-from-code/pytest-68c51be/test_answer_container_rejected0/train.jsonl；源 SHA256 `3f8ae061c756da7e6e081938c9bafb272661b48c697899bb08724f4592814ec0`；行 1，JSON pointer `/`。

**题干**

求极限 $\lim_{x \to 0} \frac{\sin x}{x}$ 的值。

**过程**

由夹逼定理, $\cos x < \frac{\sin x}{x} < 1$, 故极限为 1。

**答案原文**

[
  "4"
]

## 170. linalg-048

内容 SHA256：`915ae5ce48774e6f2c9ef531c83fd79397a8aadd3f40d96c302fd8096f38f6f2`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/0d6cf147b00b746ff542224346124229b5a6a8e21516106946a9647b8de43f36.bin；源 SHA256 `0d6cf147b00b746ff542224346124229b5a6a8e21516106946a9647b8de43f36`；行 —，JSON pointer `/0`。

**题干**

已知矩阵 $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$，分析它对应的线性变换对二维平面产生的几何影响。

**过程**

该矩阵对应的线性变换将标准基向量 $\vec{e_1} = (1,0)$ 映射为 $(2,1)$，$\vec{e_2} = (0,1)$ 映射为 $(1,2)$。整个二维平面沿 $(1,1)$ 方向拉伸，其余方向发生剪切形变。为了具体分析，可以计算其行列式 $\det(A) = 2\times2 - 1\times1 = 3$，说明变换后单位正方形的面积扩大为原来的3倍。

**答案原文**

矩阵将平面沿 (1,1) 方向拉伸，行列式为3

## 171. draft-c21-05

内容 SHA256：`921e826a60cddfc584f50b1302067b7e37514908ddde8f2a8b7da7178dd2f8ac`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-05/draft.jsonl；源 SHA256 `d37d937851dd65a04639ac056400cd3d508fd96a4cbec235d17dd573fb499084`；行 5，JSON pointer `/`。

**题干**

设直线 $l_m$ 过点 $(0,0,1)$ 且方向向量为 $(1,1,m)$。证明无论 $m$ 取何值,$l_m$ 与旋转抛物面 $z=x^2+y^2$ 都恰有两个交点,并说明理由。

**过程**

参数化 $l_m:(t,t,1+mt)$。代入 $z=x^2+y^2$ 得 $1+mt=2t^2$,即 $2t^2-mt-1=0$。其判别式 $\Delta=m^2+8>0$ 对一切实数 $m$ 恒成立,故方程恒有两个不同实根,即直线与抛物面恒恰有两个交点。理由:点 $(0,0,1)$ 位于抛物面顶点 $(0,0,0)$ 的上方,而抛物面开口向上、沿任意水平方向无限延伸,穿过其上方的任何直线方向最终都被抛物面「追上」,必有两交(代数上体现为判别式恒正)。

**答案原文**

恒恰有两个交点:判别式 $\Delta=m^2+8>0$ 与 $m$ 无关(证明见解法)。

## 172. draft-c02-01

内容 SHA256：`93da8dc4bd374260529362ea288a26666de10ca211d1d5ff5866d54311ce44e4`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-07.jsonl；源 SHA256 `b14a41ee891c643ede8cbc2986187adaa63a4bce93c398f0cce2544a7bc123a5`；行 1，JSON pointer `/`。

**题干**

计算反常积分 $\int_1^{+\infty}\frac{1}{x^2}\,dx$。

**过程**

先算有限区间上的积分再取极限:$\int_1^R\frac{1}{x^2}\,dx=\left.-\frac1x\right|_1^R=1-\frac1R$。令 $R\to+\infty$,得 $\int_1^{+\infty}\frac{1}{x^2}\,dx=\lim_{R\to+\infty}\left(1-\frac1R\right)=1$。

**答案原文**

积分值为 $1$。

## 173. draft-c16-01

内容 SHA256：`9402adc41505aa0b27a707ad73fd16d00ac8f2884114863ad14548b72d5ba0d5`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft.jsonl；源 SHA256 `afcd74e3e4d285e77802f29ab182f9dce80cfe5833b983feb8af34694ed15331`；行 11，JSON pointer `/`。

**题干**

判断直线 $l_1$：过点 $(1,0,0)$、方向 $(1,1,0)$ 与直线 $l_2$：过点 $(0,1,0)$、方向 $(1,-1,0)$ 的位置关系；若相交，求交点与夹角。

**过程**

参数化 $l_1$:$(1,0,0)+t(1,1,0)$，$l_2$:$(0,1,0)+s(1,-1,0)$。联立 $1+t=s$，$t=1-s$，$0=0$，解得 $t=0,s=1$，交点为 $(1,0,0)$(也在 $l_2$ 上:$(0,1,0)+(1,-1,0)=(1,0,0)$)。方向向量内积 $(1,1,0)\cdot(1,-1,0)=1-1+0=0$，故两直线垂直，夹角为 $90^\circ$。

**答案原文**

相交于 $(1,0,0)$,夹角 $90^\circ$(方向向量正交)。

## 174. linalg-052

内容 SHA256：`9507593084d472a86a4ea005c87b954ac6293649ec9c46165b8b2408aa8386b5`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/0d6cf147b00b746ff542224346124229b5a6a8e21516106946a9647b8de43f36.bin；源 SHA256 `0d6cf147b00b746ff542224346124229b5a6a8e21516106946a9647b8de43f36`；行 —，JSON pointer `/4`。

**题干**

将多项式 $f(x)=x^3$ 在 $x=1$ 处按泰勒公式展开，并说明展开式的意义。

**过程**

对 $f(x)=x^3$ 求导：$f(1)=1$，$f'(1)=3$，$f''(1)=6$，$f'''(1)=6$。代入泰勒公式得 $f(x)=1+3(x-1)+3(x-1)^2+(x-1)^3$。展开式的每一项系数由各阶导数在 $x=1$ 处的值决定。

**答案原文**

$1+3(x-1)+3(x-1)^2+(x-1)^3$

## 175. draft-c49-05

内容 SHA256：`95442c8d67485b1aa0d38b5ff3cb42d901d475095694bf10d14580195f1d2411`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft.jsonl；源 SHA256 `bcd6ec3d0204b822f83440669662afcfe3ec7712fa4806d51506f98cb797b0c2`；行 15，JSON pointer `/`。

**题干**

证明(切比雪夫)大数定律:若 $X_1,X_2,\dots$ 独立同分布,均值 $\mu$ 与方差 $\sigma^2$ 均有限,则样本均值 $\bar X_n=\frac1n\sum_{i=1}^{n}X_i$ 依概率收敛于 $\mu$。

**过程**

$E\bar X_n=\mu$。由独立性,$Var(\bar X_n)=\frac{1}{n^2}\sum_{i=1}^{n}Var(X_i)=\frac{\sigma^2}{n}$。对任意 $\varepsilon>0$,由切比雪夫不等式,$P(|\bar X_n-\mu|\ge\varepsilon)\le\frac{Var(\bar X_n)}{\varepsilon^2}=\frac{\sigma^2}{n\varepsilon^2}\to0$($n\to\infty$)。这正是依概率收敛的定义,故 $\bar X_n\xrightarrow{P}\mu$。

**答案原文**

证明见解法(独立同分布使 $Var(\bar X_n)=\sigma^2/n$,切比雪夫得收敛)。

## 176. syn-train-001

内容 SHA256：`96052c4578389e14bbb067e2f24cf9400538ce2df3226c0fa28ad2ac526af434`。

来源：reviews/codex-supervision/history-from-code/clone-check/reviews/fixtures-eval-test/train_synthetic.jsonl；源 SHA256 `b5db79184069fd0303603eaec0eda6e85f562bca825b3137f33b0e6c708773b3`；行 1，JSON pointer `/`。

**题干**

合成训练题目A：求 1+1 的值。

**过程**

1+1=2。

**答案原文**

2

## 177. draft-c44-03

内容 SHA256：`9679e2808ab0f62a806e3bb7b082ae3c18e46853f04c56c6d6faa27ec18757d6`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft.jsonl；源 SHA256 `b92648645c3b17a796e6b8938f67de934cddafd0cf192ab24ae006e5b423e27f`；行 8，JSON pointer `/`。

**题干**

在 $\mathbb R^4$ 上定义标准辛形式 $\omega((p_1,p_2,q_1,q_2),(r_1,r_2,s_1,s_2))=p_1s_1+p_2s_2-q_1r_1-q_2r_2$。验证 $A=\mathrm{diag}(2,2,\frac12,\frac12)$ 保持 $\omega$。

**过程**

对任意 $x=(p_1,p_2,q_1,q_2)$,$y=(r_1,r_2,s_1,s_2)$,$Ax=(2p_1,2p_2,\frac12q_1,\frac12q_2)$,$Ay=(2r_1,2r_2,\frac12s_1,\frac12s_2)$。于是 $\omega(Ax,Ay)=(2p_1)(\frac12s_1)+(2p_2)(\frac12s_2)-(\frac12q_1)(2r_1)-(\frac12q_2)(2r_2)=p_1s_1+p_2s_2-q_1r_1-q_2r_2=\omega(x,y)$。故 $A$ 保持 $\omega$,是辛变换。

**答案原文**

$A$ 保持 $\omega$(逐项核对:p 方向放大 2 倍、q 方向收缩为 1/2,配对恰好抵消)。

## 178. draft-c27-05

内容 SHA256：`9720a0cdcd8c4493edc4d680aa0d0bf42e0e3aada7b7a56f6e463fe11c12c141`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft.jsonl；源 SHA256 `e019465093b291bd83fb6ae20f3eefc40a96df3e5137a246ad8813dd03f87b34`；行 5，JSON pointer `/`。

**题干**

证明:若 $n$ 阶矩阵 $A$ 有 $n$ 个互不相同的特征值，则 $A$ 可对角化。

**过程**

只需证明属于不同特征值的特征向量线性无关(归纳法)。$m=1$ 时显然。假设 $m-1$ 个不同特征值对应的特征向量线性无关。设 $\lambda_1,\dots,\lambda_m$ 互不相同,$v_i$ 是 $\lambda_i$ 的特征向量,若 $c_1v_1+\cdots+c_mv_m=0$,用 $A$ 作用得 $\lambda_1c_1v_1+\cdots+\lambda_mc_mv_m=0$;再用 $\lambda_m$ 乘第一式并相减,得 $c_1(\lambda_1-\lambda_m)v_1+\cdots+c_{m-1}(\lambda_{m-1}-\lambda_m)v_{m-1}=0$。由归纳假设 $v_1,\dots,v_{m-1}$ 线性无关,故 $c_i(\lambda_i-\lambda_m)=0$,而 $\lambda_i\neq\lambda_m$,得 $c_i=0$($i=1,\dots,m-1$);回代得 $c_mv_m=0$,$c_m=0$。故 $v_1,\dots,v_m$ 线性无关。于是 $A$ 的 $n$ 个不同特征值给出 $n$ 个线性无关的特征向量,构成一组基,$A$ 在该基下的矩阵为对角矩阵,即 $A$ 可对角化。

**答案原文**

证明见解法(归纳法证明不同特征值的特征向量线性无关,从而构成基)。

## 179. geom-031

内容 SHA256：`9759825563cfc1594c6ed54a3c4c893b1be1eff5b067ed9d6e8f74b38bee15a2`。

来源：reviews/codex-supervision/history-from-code/clone-check/reviews/2026-10-03-data-review-round3/results.json；源 SHA256 `59e4be16385fe16104c891fe18375fa1c990a943dc0136bace63651666f63c5e`；行 —，JSON pointer `/record_snapshot/geom-031`。

**题干**

求球面 $x^2+y^2+z^2=4a^2$ 与圆柱面 $x^2+y^2=2ax$ 的交线（维维安尼曲线）的参数方程。

**过程**

令 $x=a(1+\cos t)$，$y=a\sin t$，则 $x^2+y^2 = a^2(1+\cos t)^2 + a^2\sin^2 t = 2a^2(1+\cos t) = 2a\cdot a(1+\cos t) = 2ax$，圆柱面方程自动满足。代入球面方程 $x^2+y^2+z^2=4a^2$ 得 $z^2 = 4a^2 - 2a^2(1+\cos t) = 2a^2(1-\cos t) = 4a^2\sin^2\frac{t}{2}$，故 $z = 2a\sin\frac{t}{2}$。于是交线的参数方程为 $x=a(1+\cos t)$，$y=a\sin t$，$z=2a\sin\frac{t}{2}$。

**答案原文**

维维安尼曲线，参数方程为 $x=a(1+\cos t)$，$y=a\sin t$，$z=2a\sin(t/2)$

## 180. draft-c46-01

内容 SHA256：`9769fc5b048c6014d327c2fc330236bfbb9c8256dbe6e576394b56e9c768d833`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-06/draft.jsonl；源 SHA256 `2685493ba0765d9a8d1f8a1be3e55595e83614f9d6861bc1b87c95e2d4aad8df`；行 11，JSON pointer `/`。

**题干**

甲、乙两人约定在 $12$ 点到 $13$ 点之间随机到达某地,先到者等待 $15$ 分钟后离开。求两人能相遇的概率。

**过程**

设甲到达时刻为 $x$,乙为 $y$,均服从 $[0,1]$ 上的均匀分布($1$ 小时归一化),样本空间为单位正方形。相遇当且仅当 $|x-y|\le\frac14$。在正方形中,$|x-y|\le\frac14$ 的区域为对角线带,其面积为总面积减去两个直角边长 $\frac34$ 的等腰直角三角形:相遇概率 $P=1-2\times\frac12\times\left(\frac34\right)^2=1-\frac{9}{16}=\frac{7}{16}$。

**答案原文**

相遇概率为 $\frac{7}{16}$。

## 181. fixture-001 / original

内容 SHA256：`9822c1f8f8c13b4c20d53c5f2b8dccd963b198227ebdc4264f21ca71adf6c45d`。

来源：reviews/codex-supervision/history-from-code/pytest-68c51be/test_convert_cannot_overwrite_0/eval.jsonl；源 SHA256 `087adf4399d986c85cdef9ff19680f20cdb712cd89509e04dc2cf0ab934e8aef`；行 1，JSON pointer `/`。

**题干**

求极限 $\lim_{x \to 0} \frac{\sin x}{x}$ 的值。

**过程**

由夹逼定理, $\cos x < \frac{\sin x}{x} < 1$, 故极限为 1。

**答案原文**

1

## 182. draft-c30-01

内容 SHA256：`99b921ea6b8f641177f5201a13158e0d7f7d8ee371ba2fd510c62a66b83d6709`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft.jsonl；源 SHA256 `4a8930a557e05b01cec58257879ecd5bd9679b9c08e3e478767c363642ebe382`；行 11，JSON pointer `/`。

**题干**

将多项式 $f(x)=x^3+2x^2+x+1$ 按 $x-1$ 的幂展开。

**过程**

令 $y=x-1$，则 $x=y+1$，代入展开：$f=(y+1)^3+2(y+1)^2+(y+1)+1=(y^3+3y^2+3y+1)+(2y^2+4y+2)+(y+1)+1=y^3+5y^2+8y+5$。即 $f=(x-1)^3+5(x-1)^2+8(x-1)+5$。验证(泰勒系数):$f(1)=5$，$f'(1)=3+4+1=8$，$f''(1)/2=(6+4)/2=5$，$f'''(1)/6=6/6=1$。

**答案原文**

$f=(x-1)^3+5(x-1)^2+8(x-1)+5$。

## 183. draft-c46-03

内容 SHA256：`99dc95a78c7b0113a5d22c4cb71ab9c0e4941a657fb9de146e5922f980a0a4d5`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-06/draft.jsonl；源 SHA256 `2685493ba0765d9a8d1f8a1be3e55595e83614f9d6861bc1b87c95e2d4aad8df`；行 13，JSON pointer `/`。

**题干**

设 $X,Y$ 独立且均服从 $[0,1]$ 上的均匀分布。求 $P(|X-Y|>\frac12)$,并分别用几何面积法与二重积分法计算验证。

**过程**

几何法:样本空间为单位正方形,$|x-y|>\frac12$ 为对角线带之外的区域,即两个直角边长为 $\frac12$ 的等腰直角三角形,总面积 $2\times\frac12\times\left(\frac12\right)^2=\frac14$,故 $P=\frac14$。积分法:$P=\iint_{|x-y|>\frac12}1\,dx\,dy=2\int_0^{\frac12}\int_{y+\frac12}^{1}dx\,dy=2\int_0^{\frac12}\left(\frac12-y\right)dy=2\times\frac18=\frac14$。两法一致。

**答案原文**

概率为 $\frac14$(几何法与积分法一致)。

## 184. prob-043

内容 SHA256：`9b2d1b40505ba927a814003ba6b87e991c78639dc78f3fb04d953a7ad4bc79ea`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/34cc96ded523bca1d3cc1d49462c6fdc2af726b639050cf42c039d8c7ee6a2f5.bin；源 SHA256 `34cc96ded523bca1d3cc1d49462c6fdc2af726b639050cf42c039d8c7ee6a2f5`；行 6，JSON pointer `/`。

**题干**

解释中心极限定理的核心内容，并说明当样本量 n 增大时，样本均值的分布是如何变化的。

**过程**

设随机变量 $X_1, X_2, \dots, X_n$ 相互独立且同分布，具有有限的数学期望 $\mu$ 和方差 $\sigma^2$。中心极限定理指出，当 $n$ 充分大时，标准化样本均值 $\frac{\bar{X} - \mu}{\sigma / \sqrt{n}}$ 的分布近似于标准正态分布 $N(0, 1)$。直观来说，样本均值的方差为 $\sigma^2/n$，随着 $n$ 增大，方差减小，分布变得更加集中，直方图会变高变窄，最终趋于钟形正态分布。

**答案原文**

样本均值的标准化分布趋近于标准正态分布 $N(0,1)$，直方图变高变窄

## 185. draft-c46-03

内容 SHA256：`9b901a8c655682b601630bbbd8cc403076ca57f7e7decb48d4057a023972289d`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/24c45d1c595ffef6d37f578fb55dbffdeb2f9c1c8f626dee870dcebc41075fc9.bin；源 SHA256 `24c45d1c595ffef6d37f578fb55dbffdeb2f9c1c8f626dee870dcebc41075fc9`；行 13，JSON pointer `/`。

**题干**

从单位正方形均匀选取点$M=(X,Y)$。求$M$分别以$A=(0,0)$、$B=(1,0)$、$C=(0,1)$为三个点中唯一最近点的概率，证明平局不会改变结果。

**过程**

比较平方距离：$MA^2\le MB^2\Leftrightarrow x\le1/2$，$MA^2\le MC^2\Leftrightarrow y\le1/2$，$MB^2\le MC^2\Leftrightarrow y\le x$。所以$A$的区域为$[0,1/2]^2$，面积$1/4$；$B$的区域为$1/2\le x\le1,0\le y\le x$，面积$\int_{1/2}^1x\,dx=3/8$；$C$的区域关于$y=x$对称，面积亦为$3/8$。三面积和为$1$。平局只能位于垂直平分线$x=1/2,y=1/2,y=x$的线段上，其二维面积为零。联合分布连续且均匀，故唯一最近点的概率与非严格比较所得面积相同。

**答案原文**

$P(A\text{唯一最近})=1/4$，$P(B\text{唯一最近})=P(C\text{唯一最近})=3/8$。

## 186. draft-c36-03

内容 SHA256：`9da3ecada7c13912a904757de3d9013a0c529164e9ef9f5ba57586bc5ec36100`。

来源：reviews/codex-supervision/2026-10-05-math-template-followup-v2/batch01-corrected-review-copy-v2.jsonl；源 SHA256 `d0c82fcc9503c4affd525ea22ba1387722b3e3d13ee215592f42e3824642bf42`；行 8，JSON pointer `/`。

**题干**

求使二次型 $f(x,y,z)=x^2+2xy+2y^2+az^2$ 正定的参数 $a$ 的取值范围，并讨论 $a=0$ 与 $a<0$ 时二次型的情形。

**过程**

二次型对应矩阵 $A=\begin{pmatrix}1&1&0\\1&2&0\\0&0&a\end{pmatrix}$。顺序主子式：$\Delta_1=1>0$，$\Delta_2=1\times2-1\times1=1>0$，$\Delta_3=\det A=1\times(2a-0)-1\times(a-0)+0=a$。正定当且仅当三个顺序主子式全为正，故 $a>0$。当 $a=0$ 时，$f=x^2+2xy+2y^2=(x+y)^2+y^2\geq 0$，且 $f(0,0,1)=0$，存在非零解，故半正定但非正定。当 $a<0$ 时，取 $(x,y,z)=(0,0,1)$ 得 $f(0,0,1)=a<0$，同时取 $(1,0,0)$ 得 $f=1>0$，有正值和负值，因此二次型不定。

**答案原文**

正定当且仅当 $a>0$；$a=0$ 时半正定非正定；$a<0$ 时不定。

## 187. draft-c50-01

内容 SHA256：`9f8cd7505211ff13a119dd0c2ef441c6fe51156f4a0f701c589fdca29631dc3f`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-18/draft.jsonl；源 SHA256 `6f921b08949f3ee7aaa95ce0363cafaff81b0ab7d0d95f10e1b5a280d697d8d1`；行 1，JSON pointer `/`。

**题干**

设 $X_1,\dots,X_{100}$ 独立同分布于 $U(0,1)$，$S=\sum_{i=1}^{100}X_i$。用中心极限定理近似求 $P(S>55)$。

**过程**

$EX_i=\frac12$,$Var(X_i)=\frac{1}{12}$,故 $ES=100\times\frac12=50$,$Var(S)=100\times\frac{1}{12}=\frac{25}{3}$。由中心极限定理,$\frac{S-50}{\sqrt{25/3}}$ 近似服从 $N(0,1)$。$P(S>55)\approx P\left(Z>\frac{55-50}{\sqrt{25/3}}\right)=P\left(Z>\frac{5}{5/\sqrt3}\right)=P(Z>\sqrt3)\approx P(Z>1.732)=1-\Phi(1.732)\approx0.0416$。

**答案原文**

$P(S>55)\approx0.042$。

## 188. draft-c32-02

内容 SHA256：`a0239440adb424a61ac3163bb196cd8434aa378bca82c98c70ce206a1420be24`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft.jsonl；源 SHA256 `e019465093b291bd83fb6ae20f3eefc40a96df3e5137a246ad8813dd03f87b34`；行 12，JSON pointer `/`。

**题干**

求齐次线性方程组 $\begin{cases}x+y+z=0\\ 2x+2y+2z=0\end{cases}$ 的解空间的维数与一组基。

**过程**

两个方程成比例,实际上只有一个独立方程 $x+y+z=0$,系数矩阵秩为 $1$。未知量个数 $n=3$,故解空间维数为 $n-r=3-1=2$。自由未知量取 $y,z$,$x=-y-z$。取 $(y,z)=(1,0)$ 得 $\xi_1=(-1,1,0)$;取 $(y,z)=(0,1)$ 得 $\xi_2=(-1,0,1)$。解空间为 $\mathrm{span}\{\xi_1,\xi_2\}$。

**答案原文**

维数为 $2$;一组基:$\xi_1=(-1,1,0)$,$\xi_2=(-1,0,1)$。

## 189. draft-c38-02

内容 SHA256：`a1d0d85d4c429efbe423f5192917b1c607fc695cbc5733d49a55da2d8bca202c`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft.jsonl；源 SHA256 `2a488597e92f7efdb6ec80074b147c9290e949fbeb4cbd114e293657e7c04776`；行 7，JSON pointer `/`。

**题干**

设 $W_1=\mathrm{span}\{(1,1,0),(0,1,1)\}$，$W_2=\mathrm{span}\{(1,0,1),(0,1,1)\}$。求 $W_1\cap W_2$ 的一组基与 $\dim(W_1+W_2)$。

**过程**

设 $v\in W_1\cap W_2$:$v=a(1,1,0)+b(0,1,1)=c(1,0,1)+d(0,1,1)$。按分量比较:$a=c$,$a+b=d$,$b=c+d$。由 $a=c$ 与 $b=c+d$ 得 $b=a+d$;与 $a+b=d$ 联立得 $2a=0$,即 $a=c=0$,$b=d$。故 $v=b(0,1,1)$,$W_1\cap W_2=\mathrm{span}\{(0,1,1)\}$,$\dim=1$。维数公式:$\dim(W_1+W_2)=2+2-1=3$。

**答案原文**

$W_1\cap W_2=\mathrm{span}\{(0,1,1)\}$(维数 $1$);$\dim(W_1+W_2)=3$。

## 190. draft-c41-02

内容 SHA256：`a30f7e01ba02180fb4f43e8fe0933f28e1de7db101e7082e7eb8f31cdb598106`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft.jsonl；源 SHA256 `58ae126d6bd255576c005783f78e6ade29c9f0bd60b1c7fa2e0971ba6cad1a00`；行 7，JSON pointer `/`。

**题干**

求矩阵 $A=\begin{pmatrix}2&1\\0&2\end{pmatrix}$ 的若尔当标准形，并说明为什么它不可对角化。

**过程**

特征值为 $2$(二重)。特征子空间:解 $(A-2I)v=0$,即 $\begin{pmatrix}0&1\\0&0\end{pmatrix}v=0$,得 $v_2=0$,特征子空间 $\mathrm{span}\{(1,0)\}$,维数 $1$。几何重数 $1<$ 代数重数 $2$,不可对角化。若尔当标准形含一个二阶若尔当块:$J=\begin{pmatrix}2&1\\0&2\end{pmatrix}=J_2(2)$($A$ 本身已是若尔当标准形)。

**答案原文**

$J=J_2(2)=\begin{pmatrix}2&1\\0&2\end{pmatrix}$;特征子空间维数 $1$,不可对角化。

## 191. draft-c09-02

内容 SHA256：`a39ede9078e11388af203dd849c599692370ce007c1accec6259a849a56ef3c2`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft.jsonl；源 SHA256 `1d0950f73fad698178bef910eec1c19d5303cfe6bdabbcd76bddab903f05e44b`；行 12，JSON pointer `/`。

**题干**

用柱壳法求由曲线 $y=x^2$、直线 $x=1$ 与 $x$ 轴围成的图形绕 $y$ 轴旋转所得旋转体的体积。

**过程**

柱壳法:在 $x$ 处取厚度 $dx$ 的竖直薄片,绕 $y$ 轴旋转形成半径为 $x$、高为 $x^2$ 的柱壳,体积微元 $dV=2\pi x\cdot x^2\,dx$。$V=2\pi\int_0^1x\cdot x^2\,dx=2\pi\int_0^1x^3\,dx=2\pi\cdot\frac14=\frac{\pi}{2}$。

**答案原文**

体积为 $\frac{\pi}{2}$。

## 192. draft-c01-05

内容 SHA256：`a4badc3cc87df5335279a62971c1396d7c2980873561c79293b68ef114fbf844`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft-v2.jsonl；源 SHA256 `592604adc88816bf3bc8b9313e3b8a0dd31c2fa5d5be9bb211e057196909e596`；行 5，JSON pointer `/`。

**题干**

求抛物线 $y=x^2$ 与 $y=-x^2+2x+1$ 的公切线；若不存在，请说明理由。

**过程**

两条显式多项式曲线均无竖直切线，故可将候选切线写为 $y=mx+b$。设公切线与 $y=x^2$ 相切于点 $(a,a^2)$，切线方程为 $y=2ax-a^2$；与 $y=-x^2+2x+1$ 相切于点 $(c,-c^2+2c+1)$，切线方程为 $y=(-2c+2)x+c^2+1$。若两直线为同一直线，则比较系数得 $2a=-2c+2$ 与 $-a^2=c^2+1$。由第一式得 $a=1-c$，代入第二式得 $-(1-c)^2=c^2+1$，即 $c^2-c+1=0$，其判别式 $\Delta=(-1)^2-4=-3<0$，无实根。故满足条件的 $c$(进而 $a$)不存在，即两抛物线没有公切线。

**答案原文**

公切线不存在(推导得 $c^2-c+1=0$，判别式 $-3<0$ 无实根)。

## 193. prob-044

内容 SHA256：`a534fa906bdc4812ce34b1e3712302efa645cd4a6724d0d948e0ec066e3b7fe1`。

来源：reviews/codex-supervision/2026-10-05-math-template-followup-v2/corrected-candidates/dataset_prob.jsonl；源 SHA256 `872b850fc161b729d6338532c51de998100300f8520b0e3eef7e786c7b2ef63b`；行 1，JSON pointer `/`。

**题干**

某种疾病的患病率为 $\frac{1}{1000}$。检测对患病者判阳性的概率为 $\frac{99}{100}$，对未患病者判阴性的概率为 $\frac{99}{100}$（假阳性率 $\frac{1}{100}$）。若检测结果为阳性，求实际患病的概率。

**过程**

记 $D$ 为患病、$T$ 为阳性，则 $P(D)=\frac{1}{1000}$、$P(D^c)=\frac{999}{1000}$、$P(T\mid D)=\frac{99}{100}$、$P(T\mid D^c)=\frac{1}{100}$。由全概率公式 $P(T)=\frac{99}{100}\frac{1}{1000}+\frac{1}{100}\frac{999}{1000}=\frac{1098}{100000}=\frac{549}{50000}$。由贝叶斯公式 $P(D\mid T)=\frac{99}{1098}=\frac{11}{122}$。

**答案原文**

$\frac{11}{122}$

## 194. draft-c08-03

内容 SHA256：`a60a7143e741c1af68bd1abe1f52dac160f6470660f9d030bd4775a447377b4f`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft.jsonl；源 SHA256 `1d0950f73fad698178bef910eec1c19d5303cfe6bdabbcd76bddab903f05e44b`；行 8，JSON pointer `/`。

**题干**

求笛卡尔叶形线 $x=\frac{3t}{1+t^3}$，$y=\frac{3t^2}{1+t^3}$($t\ge0$)的环所围成的面积。

**过程**

叶形线的环对应 $t$ 从 $0$ 到 $+\infty$(曲线从原点出发,经第一象限后回到原点)。用面积公式 $A=\frac12\int_0^{+\infty}(x\,y'-y\,x')\,dt$。计算:$x'=\frac{3(1-2t^3)}{(1+t^3)^2}$,$y'=\frac{3t(2-t^3)}{(1+t^3)^2}$,故 $x\,y'-y\,x'=\frac{9t^2(2-t^3)-9t^2(1-2t^3)}{(1+t^3)^3}=\frac{9t^2(1+t^3)}{(1+t^3)^3}=\frac{9t^2}{(1+t^3)^2}$。$A=\frac12\int_0^{+\infty}\frac{9t^2}{(1+t^3)^2}\,dt=\frac12\left.\left(-\frac{3}{1+t^3}\right)\right|_0^{+\infty}=\frac12\times3=\frac32$。

**答案原文**

环的面积为 $\frac32$。

## 195. draft-c52-04

内容 SHA256：`a75d0d060b215749722e3856da18d27022a34ee92138a042045f2e08d096eec0`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft.jsonl；源 SHA256 `13fe6a370d3c46ae8ca6c1b16c9cd98fbedcc8648087f11a70ff046951db5479`；行 14，JSON pointer `/`。

**题干**

设随机变量 $X$ 服从区间 $(0,2)$ 上的均匀分布，$Y=\min(X,1)$。求 $Y$ 的分布函数，说明其密度(含可能的概率原子)，并求 $E[Y]$。

**过程**

当 $y\leq0$ 时 $F_Y(y)=0$；当 $0<y<1$ 时，$F_Y(y)=P(\min(X,1)\leq y)=P(X\leq y)=\frac{y}{2}$；当 $y\geq1$ 时 $F_Y(y)=1$。故 $Y$ 在 $(0,1)$ 上有连续密度 $f_Y(y)=\frac{1}{2}$，在 $y=1$ 处有概率原子 $P(Y=1)=P(X\geq1)=\frac{1}{2}$。期望：$E[Y]=\int_0^1 y\cdot\frac{1}{2}\,dy+1\cdot\frac{1}{2}=\frac{1}{4}+\frac{1}{2}=\frac{3}{4}$。另一算法(经 $X$ 直接算)：$E[\min(X,1)]=\int_0^2\min(x,1)\cdot\frac{1}{2}\,dx=\frac{1}{2}\left(\int_0^1x\,dx+\int_1^2 1\,dx\right)=\frac{1}{2}\left(\frac{1}{2}+1\right)=\frac{3}{4}$，两法一致。

**答案原文**

$F_Y(y)=0\ (y\leq0)$；$F_Y(y)=\frac{y}{2}\ (0<y<1)$；$F_Y(y)=1\ (y\geq1)$。密度:连续部分 $\frac{1}{2}$($0<y<1$)加原子质量 $\frac{1}{2}$ 于 $y=1$。$E[Y]=\frac{3}{4}$。

## 196. draft-c36-02

内容 SHA256：`a8d8e43e78e1be455fec0ac1da2845ba42af06d1d9ab98c2eca5fefb47c34fe8`。

来源：reviews/codex-supervision/2026-10-05-math-template-followup-v2/batch01-original.jsonl；源 SHA256 `25bcdf9bb0a1003d55e845e089a047013953ef216cac4b699485bae107174a8f`；行 7，JSON pointer `/`。

**题干**

用特征值方法判断二次型 $f(x,y,z)=2x^2+2y^2+2z^2-2xy-2yz$ 是否正定。

**过程**

二次型对应矩阵 $A=\begin{pmatrix}2&-1&0\\-1&2&-1\\0&-1&2\end{pmatrix}$。由三对角对称矩阵特征值公式(对角元均为 $2$，次对角元均为 $-1$)，$\lambda_k=2+2\cdot(-1)\cos\frac{k\pi}{4}=2-2\cos\frac{k\pi}{4}$，$k=1,2,3$，即 $\lambda_1=2-\sqrt{2}$，$\lambda_2=2$，$\lambda_3=2+\sqrt{2}$。三个特征值全部为正，故二次型正定。

**答案原文**

正定(特征值为 $2-\sqrt{2}$、$2$、$2+\sqrt{2}$，全正)。

## 197. draft-c50-05

内容 SHA256：`a9c8548788369bb6afaa24d448ebfa812ea5b86d2d50cf180af0f198d6f3ff55`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-18/draft.jsonl；源 SHA256 `6f921b08949f3ee7aaa95ce0363cafaff81b0ab7d0d95f10e1b5a280d697d8d1`；行 5，JSON pointer `/`。

**题干**

说明中心极限定理要求方差有限的条件，并用柯西分布的例子说明：若方差无限，样本均值不必近似正态。

**过程**

中心极限定理的标准条件:独立同分布、均值 $\mu$ 与方差 $\sigma^2$ 均有限;此时 $\frac{\sum X_i-n\mu}{\sigma\sqrt n}$ 依分布收敛于 $N(0,1)$。柯西分布 $Cauchy(0,1)$:均值与方差均不存在。其特征函数为 $\varphi(t)=e^{-|t|}$。若 $X_1,\dots,X_n$ 独立同分布于柯西分布,则样本均值 $\bar X_n=\frac1n\sum X_i$ 的特征函数为 $\varphi(t/n)^n=(e^{-|t|/n})^n=e^{-|t|}$,仍是 $Cauchy(0,1)$ 的特征函数!即样本均值与单个观测同分布,完全不随 $n$ 增大而向正态靠拢(也不向任何常数集中)。这从反面说明方差有限(或类似的矩条件)对 CLT 必不可少。

**答案原文**

柯西分布样本均值的特征函数 $(e^{-|t|/n})^n=e^{-|t|}$ 仍为柯西,不近似正态;说明方差有限条件是 CLT 的必要条件(论证见解法)。

## 198. draft-c26-01

内容 SHA256：`ab7fa64420e9d715a44fcf278df0b44b8f5d18903c88db1bc37ccff12c7199c1`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft.jsonl；源 SHA256 `25705ed80dbac40074a2bc29ed482de0087b12bc96d3e1ec0cb9f77722fefe0e`；行 11，JSON pointer `/`。

**题干**

解释矩阵 $A=\begin{pmatrix}1&2\\0&1\end{pmatrix}$ 对应的线性变换的几何作用。

**过程**

$A(x,y)=(x+2y,y)$:每个点的横坐标加上自身纵坐标的 $2$ 倍,纵坐标不变。这是水平剪切:水平线 $y=c$ 作为集合不变(线上每点沿水平方向平移 $2c$),竖直线 $x=c$ 被倾斜为直线 $x'-2y'=c$(斜率 $\frac12$);正方形被斜切成同面积平行四边形($\det A=1$,面积不变)。

**答案原文**

水平剪切:横坐标平移 $2y$;水平线不变、竖直线被倾斜,面积不变($\det A=1$)。

## 199. draft-c51-03

内容 SHA256：`ac0f4b1b99cad13282f76e38549a0946153665658da99ea0255a9861e87e148e`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft.jsonl；源 SHA256 `71d46f404c59db6194494bf8ea2353202b77f602a15522f58c1b4599d1cbb07a`；行 13，JSON pointer `/`。

**题干**

某疾病患病率为 $\frac{1}{1000}$。一次检测对患病者呈阳性的概率为 $\frac{99}{100}$，对未患病者呈阳性的概率为 $\frac{1}{100}$。某人第一次检测呈阳性，随后做了一次独立(在给定患病状态下)的同类检测，仍呈阳性。求两次检测后此人患病的概率，并与第一次检测后的概率对比。

**过程**

第一次阳性后，由贝叶斯公式，$P(\text{患病}\mid+_1)=\frac{\frac{1}{1000}\times\frac{99}{100}}{\frac{1}{1000}\times\frac{99}{100}+\frac{999}{1000}\times\frac{1}{100}}=\frac{99}{99+999}=\frac{99}{1098}=\frac{11}{122}$。第二次检测在给定患病状态下与第一次独立，故将 $\frac{11}{122}$ 作为新的先验再更新：$P(\text{患病}\mid+_1,+_2)=\frac{\frac{11}{122}\times\frac{99}{100}}{\frac{11}{122}\times\frac{99}{100}+\frac{111}{122}\times\frac{1}{100}}=\frac{1089}{1089+111}=\frac{1089}{1200}=\frac{363}{400}$。对比:单次阳性后为 $\frac{11}{122}\approx0.090$，两次后为 $\frac{363}{400}\approx0.908$。

**答案原文**

第一次阳性后:$P=\frac{11}{122}$;两次阳性后:$P=\frac{363}{400}$。

## 200. linalg-070

内容 SHA256：`ac1ef825ac60395d3abdbe1612688342f844cbb91895e5c5e3cd56d12671d5b9`。

来源：reviews/codex-supervision/2026-10-06-scene-repair-takeover/math-corrected-v1/dataset_linalg.jsonl；源 SHA256 `2c977c78d12f5eb107f065edf279973d344c180fde5d1c7f241b0c54bd0a0cf4`；行 16，JSON pointer `/`。

**题干**

在 $\mathbb{R}^2$ 上定义辛形式 $\omega(u,v)=u_1v_2-u_2v_1$（标准行列式形式），说明辛变换保持该形式不变的意义。

**过程**

设 $J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}$，则 $\omega(u,v)=u^TJv=\det(u,v)$，表示有向面积。对 $A=\begin{pmatrix}a&b\\c&d\end{pmatrix}$，有 $A^TJA=\begin{pmatrix}0&ad-bc\\bc-ad&0\end{pmatrix}=(\det A)J$，因此 $\omega(Au,Av)=(\det A)\omega(u,v)$。二维中，$A$ 是辛变换当且仅当 $\det A=1$；它同时保持有向面积、通常面积与定向。仅保持通常面积还不足以判定为辛变换：反射 $R=\operatorname{diag}(1,-1)$ 的行列式为 $-1$，它使 $\omega(Ru,Rv)=-\omega(u,v)$。

**答案原文**

辛变换保持有向面积与定向：$\omega(Au,Av)=\omega(u,v)$；二维中等价于 $\det A=1$。

## 201. draft-c30-05

内容 SHA256：`ae7dbff3b479fcc3eae3f5894a385ec3a661915756a3abab181895211fcc3019`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-04.jsonl；源 SHA256 `a3d74ab73cb86b41071c5be7e103aabcbbba47a54a9df746aa1cbf629bd7660f`；行 15，JSON pointer `/`。

**题干**

写出 $f(x)=\ln x$ 在 $x=1$ 处的幂级数展开的前四项，并讨论其收敛范围；再与多项式(如 $x^4$)的平移展开对照，说明两者在项数与适用范围上的区别。

**过程**

令$u=x-1$。对$|u|<1$，逐项积分等比级数得$\ln x=\sum_{n=1}^{\infty}\frac{(-1)^{n+1}u^n}{n}$。前四项为$P_4(u)=u-\frac{u^2}{2}+\frac{u^3}{3}-\frac{u^4}{4}$。精确余项为$R_4(u)=\int_0^u\frac{t^4}{1+t}\,dt$，所以$\ln(1+u)=P_4(u)+R_4(u)$（$u>-1$），不能把前四项当作精确函数值。当$u=1$时交错调和级数收敛，阿贝尔定理给出其和$\ln2$；当$u=-1$时为负调和级数，发散；当$|u|>1$时通项不趋于零，发散。故原幂级数收敛域为$0<x\le2$，在此域内等于$\ln x$。多项式平移是有限恒等式，对所有实数成立；实函数$\ln x$不是多项式，此任务不应计入C30多项式平移的五个样本。

**答案原文**

前四项为$u-\frac{u^2}{2}+\frac{u^3}{3}-\frac{u^4}{4}$（$u=x-1$），精确余项$R_4(u)=\int_0^u\frac{t^4}{1+t}\,dt$；完整级数的收敛域为$(0,2]$。

## 202. draft-c15-04

内容 SHA256：`af4b1fd8d5448040a90cd076b6200c17b05acef4a549907e9e60686dd29f8bf3`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft.jsonl；源 SHA256 `9aa29561a8f8dc1a725169c6fa9b3fb558e5c2bed5b0d43940d42e9b5ff823e3`；行 4，JSON pointer `/`。

**题干**

求直线 $l$：过原点、方向为 $(1,1,1)$ 与平面 $\pi:x+y=0$ 的夹角 $\varphi$；再求 $l$ 在 $\pi$ 上的投影直线的方向，并求 $l$ 与其投影线的夹角 $\theta$，说明 $\theta$ 与 $\varphi$ 的关系。

**过程**

平面法向量 $n=(1,1,0)$。$\sin\varphi=\frac{|(1,1,1)\cdot(1,1,0)|}{\sqrt3\cdot\sqrt2}=\frac{2}{\sqrt6}=\sqrt{\frac23}$,故 $\varphi=\arcsin\sqrt{\frac23}$。投影方向:$d'=d-\frac{d\cdot n}{|n|^2}n=(1,1,1)-\frac{2}{2}(1,1,0)=(0,0,1)$。$l$ 与投影线的夹角 $\theta$:$\cos\theta=\frac{d\cdot d'}{|d||d'|}=\frac{1}{\sqrt3\cdot1}=\frac{1}{\sqrt3}$,故 $\theta=\arccos\frac{1}{\sqrt3}$。数值核对:$\sin^2\varphi=\frac23$,而 $1-\cos^2\theta=1-\frac13=\frac23$;事实上线面夹角的定义就是直线与其投影线的夹角,故 $\theta=\varphi$(两者都等于 $90^\circ-\angle(d,n)$,即都与 $d$ 与 $n$ 的夹角互余)。

**答案原文**

$\varphi=\arcsin\sqrt{\frac23}$;投影方向 $(0,0,1)$;$\theta=\arccos\frac{1}{\sqrt3}$,且 $\theta=\varphi$(两者均为 $90^\circ-\angle(d,n)$,数值约 $54.7^\circ$)。

## 203. draft-c01-03

内容 SHA256：`af9ac0e033ddd0d9bd8d5738dfc5f32028357dfe0d503d7117d28a6b23f7d95e`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft-v2.jsonl；源 SHA256 `592604adc88816bf3bc8b9313e3b8a0dd31c2fa5d5be9bb211e057196909e596`；行 3，JSON pointer `/`。

**题干**

已知参数曲线 $\begin{cases}x=t^2\\ y=t^3-3t\end{cases}$。求曲线在 $t=2$ 对应点处的切线方程，并求出曲线上所有水平切线与竖直切线。其中参数 $t$ 取遍实数。

**过程**

参数求导：$\frac{dx}{dt}=2t$，$\frac{dy}{dt}=3t^2-3$，故 $\frac{dy}{dx}=\frac{3t^2-3}{2t}$。当 $t=2$ 时，对应点为 $(4,2)$，斜率为 $\frac{12-3}{4}=\frac{9}{4}$，切线为 $y-2=\frac{9}{4}(x-4)$，即 $y=\frac{9}{4}x-7$。水平切线需 $\frac{dy}{dt}=0$ 且 $\frac{dx}{dt}\neq 0$：$3t^2-3=0$ 得 $t=\pm 1$，对应点 $(1,-2)$ 与 $(1,2)$，切线分别为 $y=-2$ 与 $y=2$。竖直切线需 $\frac{dx}{dt}=0$ 且 $\frac{dy}{dt}\neq 0$：$2t=0$ 得 $t=0$，此时 $\frac{dy}{dt}=-3\neq 0$，对应点 $(0,0)$，切线为 $x=0$。

**答案原文**

$t=2$ 处切线 $y=\frac{9}{4}x-7$；水平切线 $y=-2$、$y=2$；竖直切线 $x=0$。

## 204. geom-026

内容 SHA256：`afc8760ff6c5dd6e6b8404e2863eaad32a81b0f13d954f58e94dfaae916aa199`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/4040cba8ea52c8cbdd833485a2c2e61e48130c9cb118d9a07ab2cf8821ef9142.bin；源 SHA256 `4040cba8ea52c8cbdd833485a2c2e61e48130c9cb118d9a07ab2cf8821ef9142`；行 7，JSON pointer `/`。

**题干**

指出方程 $z = x^2 + 2y^2$ 表示的二次曲面类型，并分析其与平面 $y = 0$ 和 $y = 1$ 的交线。

**过程**

该方程为椭圆抛物面。当 $y = 0$ 时，交线为 $z = x^2$，是 $xOz$ 平面上的抛物线。当 $y = 1$ 时，交线为 $z = x^2 + 2$，依然是一条抛物线，只是顶点向上平移了 2 个单位。因此，曲面可以看作抛物线在 $y$ 轴方向平移叠加而成。

**答案原文**

椭圆抛物面；与平面 $y=0$ 的交线为 $z=x^2$，与平面 $y=1$ 的交线为 $z=x^2+2$

## 205. draft-c11-01

内容 SHA256：`b11a78ab98ad8fb9c612cd8d6b08d4f5d96c542a0ebcf8f215a7214e7742a46b`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft.jsonl；源 SHA256 `71d46f404c59db6194494bf8ea2353202b77f602a15522f58c1b4599d1cbb07a`；行 1，JSON pointer `/`。

**题干**

求幂级数 $\sum_{n=1}^{\infty}\left(\frac{n}{n+1}\right)^{n^2}x^n$ 的收敛域。

**过程**

用根值法：$\lim_{n\to\infty}\sqrt[n]{\left(\frac{n}{n+1}\right)^{n^2}}=\lim_{n\to\infty}\left(1-\frac{1}{n+1}\right)^n=e^{n\ln(1-\frac{1}{n+1})}=e^{-1}$，故收敛半径 $R=e$。当 $|x|<e$ 时级数(绝对)收敛。检查端点 $x=\pm e$：通项的绝对值为 $\left(\frac{n}{n+1}\right)^{n^2}e^n=\exp\left(n^2\ln(1-\frac{1}{n+1})+n\right)=\exp\left(-\frac{n^2}{n+1}-\frac{n^2}{2(n+1)^2}-\cdots+n\right)\to e^{\frac12}\neq 0$，通项不趋于 $0$，故两端点均发散。收敛域为 $(-e,e)$。

**答案原文**

收敛域为 $(-e,e)$。

## 206. draft-c51-02

内容 SHA256：`b1df0960e6dbe8fcb526b2ec49054657293f43659f8cf082a2e574586a80354b`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft.jsonl；源 SHA256 `71d46f404c59db6194494bf8ea2353202b77f602a15522f58c1b4599d1cbb07a`；行 12，JSON pointer `/`。

**题干**

说明「独立」与「条件独立」互不蕴含：构造一个例子说明两个事件条件独立但(无条件)不独立；再构造一个例子说明两个事件独立但给定第三个事件后条件不独立。

**过程**

例一(条件独立但不独立)：袋中有两枚硬币，一枚两面皆正，一枚两面皆反，随机取一枚抛两次。记 $A$={第一次正面}，$B$={第二次正面}，$C$={取到双正面硬币}。无条件：$P(A)=P(B)=\frac12$，而 $P(A\cap B)=P(C)=\frac12\neq\frac14=P(A)P(B)$，故 $A,B$ 不独立。给定 $C$:$C=C_1$ 时 $P(A\mid C)=P(B\mid C)=1$ 且 $P(A\cap B\mid C)=1$;$C=C_2$ 时三者均为 $0$;故在给定硬币条件下 $A,B$ 条件独立。例二(独立但不条件独立)：一枚均匀硬币抛两次。记 $A$={第二次正面}，$B$={两次结果相同}，$C$={第一次正面}。无条件：$P(A)=\frac12$，$P(B)=\frac12$，$P(A\cap B)=P(\text{两次皆正})=\frac14=P(A)P(B)$，故 $A,B$ 独立。给定 $C$:$P(A\mid C)=\frac12$，$P(B\mid C)=P(\text{第二次正})=\frac12$，而 $P(A\cap B\mid C)=P(\text{第二次正})=\frac12\neq\frac14$，故条件不独立。

**答案原文**

例一:双面硬币袋中随机取一枚抛两次,$A,B$ 给定硬币条件独立但无条件不独立;例二:均匀硬币抛两次,$A$={第二次正}、$B$={两次相同}、$C$={第一次正},$A,B$ 独立但给定 $C$ 条件不独立。

## 207. linalg-049

内容 SHA256：`b3b7072d77dc8054628ce03d8b9fc543731a10391d7c74628898bd273d999154`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/0d6cf147b00b746ff542224346124229b5a6a8e21516106946a9647b8de43f36.bin；源 SHA256 `0d6cf147b00b746ff542224346124229b5a6a8e21516106946a9647b8de43f36`；行 —，JSON pointer `/1`。

**题干**

求矩阵 $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ 的特征值和特征向量，并说明其几何意义。

**过程**

特征方程为 $|\lambda I - A| = (\lambda - 2)^2 - 1 = 0$，解得特征值 $\lambda_1 = 3, \lambda_2 = 1$。对于 $\lambda_1 = 3$，解方程 $(3I - A)x = 0$ 得特征向量 $(1, 1)^T$。对于 $\lambda_2 = 1$，解得特征向量 $(1, -1)^T$。几何上，整个空间在变换时，特征向量 $(1,1)$ 的方向保持不变，长度拉伸为原来的3倍；特征向量 $(1,-1)$ 的方向也保持不变，长度保持为原来的1倍。

**答案原文**

特征值 3 和 1，对应特征向量 (1,1) 和 (1,-1)

## 208. eval-linalg-023-s3

内容 SHA256：`b44012aee991a840e1f1d0941d64d06d4bed52264ba39d798034995121d4ebe1`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/35d6c4b8d3003d5246cb98baf207b63cef22c86a3f15a259738ff2842ad48c9f.bin；源 SHA256 `35d6c4b8d3003d5246cb98baf207b63cef22c86a3f15a259738ff2842ad48c9f`；行 264，JSON pointer `/`。

**题干**

分别在复数域与实数域上分解 $x^8-1$。

**过程**

解法一与解法二给出实数域分解的两种形式，由 $(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)=x^4+1$（平方差：$(x^2+1)^2-(\sqrt2x)^2=x^4+2x^2+1-2x^2=x^4+1$）连接起来。两形式一致。

**答案原文**

复数域：$\displaystyle\prod_{k=0}^{7}\left(x-e^{2\pi ik/8}\right)$；实数域（完整实不可约分解）：$(x-1)(x+1)(x^2+1)(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)$

## 209. test-linalg-003

内容 SHA256：`b489dd13b4493c38a6d4cde8a9a2f4de3fff8042a6609b154f40ea36a334fbc8`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/97dfbccab4209c28590347a27399cbbb67997390b39610e258c985d588487811.bin；源 SHA256 `97dfbccab4209c28590347a27399cbbb67997390b39610e258c985d588487811`；行 —，JSON pointer `/97`。

**题干**

设 $A=\begin{pmatrix}1&2\\0&1\end{pmatrix}$，求 $A^n$（$n$ 为正整数）。

**过程**

$A=I+N$，其中 $N=\begin{pmatrix}0&2\\0&0\end{pmatrix}$ 满足 $N^2=0$。$I$ 与 $N$ 可交换，由二项式定理 $A^n=(I+N)^n=I+nN=\begin{pmatrix}1&2n\\0&1\end{pmatrix}$。

**答案原文**

$\begin{pmatrix}1&2n\\0&1\end{pmatrix}$

## 210. draft-c41-01

内容 SHA256：`b67a1b88357e8fd4959e9c921beea0924535f7673d936d1bcc2d27de9f265273`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft.jsonl；源 SHA256 `58ae126d6bd255576c005783f78e6ade29c9f0bd60b1c7fa2e0971ba6cad1a00`；行 6，JSON pointer `/`。

**题干**

求矩阵 $A=\begin{pmatrix}1&2\\0&3\end{pmatrix}$ 的若尔当标准形。

**过程**

$A$ 为上三角矩阵,特征值为 $1$ 与 $3$(互异)。特征值互异时每个特征值的几何重数等于代数重数 $1$,故若尔当标准形为对角矩阵 $J=\begin{pmatrix}1&0\\0&3\end{pmatrix}$。

**答案原文**

$J=\begin{pmatrix}1&0\\0&3\end{pmatrix}$(特征值互异,对角形)。

## 211. draft-c14-03

内容 SHA256：`b694c54259d9c01708a3f8dc1e944ca72503ee4e05105bf194c432a01b02295d`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft.jsonl；源 SHA256 `1cc220e2699b799fb9bacc8525e1f9d82321dc39dacd33e5c1caa21c1a7d959b`；行 13，JSON pointer `/`。

**题干**

将方波 $f(x)=\begin{cases}0,&-\pi<x<0\\1,&0<x<\pi\end{cases}$ 展开为傅立叶级数，并说明在间断点处级数的取值。

**过程**

$a_0=\frac1\pi\int_{-\pi}^{\pi}f(x)\,dx=\frac1\pi\int_0^{\pi}1\,dx=1$。$a_n=\frac1\pi\int_0^{\pi}\cos nx\,dx=\frac{\sin n\pi}{n\pi}=0$($n\ge1$)。$b_n=\frac1\pi\int_0^{\pi}\sin nx\,dx=\frac{1-\cos n\pi}{n\pi}=\frac{1-(-1)^n}{n\pi}$,即奇数项 $b_{2k-1}=\frac{2}{(2k-1)\pi}$,偶数项为 $0$。故 $f(x)=\frac12+\frac{2}{\pi}\sum_{k=1}^{\infty}\frac{\sin(2k-1)x}{2k-1}$。在间断点 $x=0,\pm\pi$ 处,由狄利克雷定理,级数和为左右极限的平均值 $\frac{0+1}{2}=\frac12$。

**答案原文**

$f=\frac12+\frac{2}{\pi}\sum_{k=1}^{\infty}\frac{\sin(2k-1)x}{2k-1}$;间断点处级数取 $\frac12$(左右极限平均)。

## 212. eval-linalg-032-s3

内容 SHA256：`b6f67bffd8371a988598e952418c3681885c3a509f8afc1f4bd2d1661b45f59d`。

来源：reviews/codex-supervision/history-from-code/recheck-68c51be/data/v2/eval/dataset_eval.json；源 SHA256 `1de2df62edd0b01403df813c80edc3a5a9dbf1791f0b223d8e0f107ccee55e6e`；行 —，JSON pointer `/290`。

**题干**

求 λ-矩阵 $A(\lambda)=\begin{pmatrix}\lambda-1&1\\0&\lambda-1\end{pmatrix}$ 的不变因子与初等因子。

**过程**

$A(\lambda)=\lambda I-\begin{pmatrix}1&-1\\0&1\end{pmatrix}$（因 $-\begin{pmatrix}1&-1\\0&1\end{pmatrix}=\begin{pmatrix}-1&1\\0&-1\end{pmatrix}$，而 $\lambda I-\begin{pmatrix}1&-1\\0&1\end{pmatrix}=\begin{pmatrix}\lambda-1&1\\0&\lambda-1\end{pmatrix}$）。矩阵 $\begin{pmatrix}1&-1\\0&1\end{pmatrix}$ 相似于 $J_2(1)=\begin{pmatrix}1&1\\0&1\end{pmatrix}$（相似变换：令 $P=\begin{pmatrix}1&0\\0&-1\end{pmatrix}$，$P^{-1}\begin{pmatrix}1&-1\\0&1\end{pmatrix}P=\begin{pmatrix}1&1\\0&1\end{pmatrix}$）。$J_2(1)$ 的初等因子为 $(\lambda-1)^2$，故原 λ-矩阵初等因子 $(\lambda-1)^2$。

**答案原文**

不变因子 $1,(\lambda-1)^2$；初等因子 $(\lambda-1)^2$

## 213. calc-vol-012

内容 SHA256：`b89842111834e55e9d541a220d9ae9cf1ea8fdde39e1e225dbd5f8499e35564e`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/5f36da8da087235a579b16cbaa3af8c47ceada0e45668df4a7efe70c4b14033e.bin；源 SHA256 `5f36da8da087235a579b16cbaa3af8c47ceada0e45668df4a7efe70c4b14033e`；行 12，JSON pointer `/`。

**题干**

求曲线 $y = \arcsin x$（$0 \le x \le 1$）与x轴、直线 $x=1$ 围成的图形绕x轴旋转一周所得旋转体的体积。

**过程**

使用圆盘法，体积 $V = \pi \int_0^1 (\arcsin x)^2 dx$。计算不定积分 $\int (\arcsin x)^2 dx = x(\arcsin x)^2 + 2\sqrt{1-x^2}\arcsin x - 2x$。代入上下限得 $V = \pi [1 \cdot (\frac{\pi}{2})^2 + 0 - 2] - \pi [0 + 0 - 0] = \pi(\frac{\pi^2}{4} - 2) = \frac{\pi^3}{4} - 2\pi$。

**答案原文**

$\frac{\pi^3}{4} - 2\pi$

## 214. draft-c22-04

内容 SHA256：`b8e6cb9e4e050c3edac9c3cc71641864e0b0245fe1e52c03d54b6f3e923e8f2b`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft.jsonl；源 SHA256 `e0eb9bf14b1cdf0919006ede0e9523046d0edadffb69ac3a10e4941a77563756`；行 9，JSON pointer `/`。

**题干**

判断下列曲面哪些是直纹面，并各给理由:圆柱面 $x^2+y^2=1$;圆锥面 $x^2+y^2-z^2=0$;椭球面 $\frac{x^2}{4}+\frac{y^2}{9}+z^2=1$;抛物柱面 $y=x^2$。

**过程**

圆柱面:直纹面——对每个 $(x_0,y_0)$ 在圆 $x^2+y^2=1$ 上,直线 $\{(x_0,y_0,t)\}$ 整条在曲面上(母线平行于 $z$ 轴)。圆锥面:直纹面——对每个满足 $u^2+v^2-w^2=0$ 的方向 $(u,v,w)$,过原点的直线 $\{(tu,tv,tw)\}$ 满足 $t^2(u^2+v^2-w^2)=0$,整条在曲面上(所有母线都经过顶点,互不平行)。椭球面:不是直纹面——与球面同理(有界曲面不含整条直线,任一直线与椭球面至多两交点)。抛物柱面 $y=x^2$:直纹面——对每个 $x_0$,直线 $\{(x_0,x_0^2,t)\}$ 整条在曲面上($x=x_0,y=x_0^2$ 满足 $y=x^2$,母线平行于 $z$ 轴)。

**答案原文**

圆柱面、圆锥面、抛物柱面是直纹面(圆柱面/抛物柱面含整族平行直线;圆锥面的母线均过顶点);椭球面不是直纹面(有界曲面与直线至多两交点)。

## 215. draft-c37-04

内容 SHA256：`b939d29a02e52837f8a67f58ea590d107d66f06d8736aabfb1b5d88b7c07bd2c`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-03.jsonl；源 SHA256 `ed738d83f3c59a525f3119c56735aac4bcc4b50ddf4817701a786e7b1e3c9e5d`；行 9，JSON pointer `/`。

**题干**

在 $\mathbb R^2$ 中，设从标准基 $\varepsilon$ 到基 $\eta=\{\eta_1=(1,1),\eta_2=(1,-1)\}$ 的过渡矩阵为 $P$，从 $\eta$ 到基 $\zeta=\{\zeta_1=(2,1),\zeta_2=(1,2)\}$ 的过渡矩阵为 $Q$。求 $P$、$Q$ 与从 $\varepsilon$ 到 $\zeta$ 的过渡矩阵，并验证后者等于 $PQ$；若向量 $\alpha$ 在基 $\zeta$ 下的坐标为 $(1,1)$，求 $\alpha$ 在标准基下的坐标。

**过程**

约定基矩阵 $B_\eta=B_\varepsilon P$，$P$的第$j$列为$[\eta_j]_\varepsilon$，故$[v]_\varepsilon=P[v]_\eta$、$[v]_\eta=P^{-1}[v]_\varepsilon$；换基改变坐标，不改变向量$v$。$P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$。求 $Q$：把 $\zeta_1=(2,1)$ 写成 $\eta$ 的组合，解 $(2,1)=a(1,1)+b(1,-1)$ 得 $a=\frac32,b=\frac12$;$\zeta_2=(1,2)=c(1,1)+d(1,-1)$ 得 $c=\frac32,d=-\frac12$。故 $Q=\begin{pmatrix}\frac32&\frac32\\\frac12&-\frac12\end{pmatrix}$。于是 $\varepsilon\to\zeta$ 的过渡矩阵 $R=PQ=\begin{pmatrix}1&1\\1&-1\end{pmatrix}\begin{pmatrix}\frac32&\frac32\\\frac12&-\frac12\end{pmatrix}=\begin{pmatrix}2&1\\1&2\end{pmatrix}$，恰为 $\zeta_1,\zeta_2$ 在标准基下的坐标按列排列，验证正确。$\alpha=1\cdot\zeta_1+1\cdot\zeta_2=(3,3)$。

**答案原文**

$P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$，$Q=\begin{pmatrix}\frac32&\frac32\\\frac12&-\frac12\end{pmatrix}$，$\varepsilon\to\zeta$ 的过渡矩阵为 $\begin{pmatrix}2&1\\1&2\end{pmatrix}=PQ$;$\alpha$ 在标准基下为 $(3,3)$。

## 216. draft-c47-02

内容 SHA256：`bb3a0ef6baf9247979b4cc8aedbb130e6891393e7716331fc1274646bfca7ff3`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft.jsonl；源 SHA256 `bcd6ec3d0204b822f83440669662afcfe3ec7712fa4806d51506f98cb797b0c2`；行 2，JSON pointer `/`。

**题干**

设 $X\sim B(100,\frac{1}{100})$。分别用精确公式与泊松近似计算 $P(X=0)$，并比较两者。

**过程**

精确值:$P(X=0)=(1-\frac{1}{100})^{100}=0.99^{100}\approx0.3660$。泊松近似:$\lambda=np=1$,$P(X=0)\approx e^{-1}\approx0.3679$。比较:两者相差约 $0.0018$,相对误差约 $0.5\%$。

**答案原文**

精确值 $0.99^{100}\approx0.3660$;泊松近似 $e^{-1}\approx0.3679$;相对误差约 $0.5\%$。

## 217. prob-045

内容 SHA256：`bcf345b01dab595ef789c369b2cd6f2fb7c2bbcf344c4def33d9a6ab4ef0e1e4`。

来源：reviews/codex-supervision/2026-10-05-math-template-followup-v2/corrected-candidates/dataset_prob.jsonl；源 SHA256 `872b850fc161b729d6338532c51de998100300f8520b0e3eef7e786c7b2ef63b`；行 2，JSON pointer `/`。

**题干**

设随机变量 $X$ 服从区间 $(0, 1)$ 上的均匀分布，求 $Y = X^2$ 的概率密度函数。

**过程**

已知 $X \sim U(0,1)$，其概率密度函数为 $f_X(x) = 1$（当 $0 < x < 1$）。采用分布函数法：先求 $Y$ 的分布函数 $F_Y(y) = P(Y \le y) = P(X^2 \le y) = P(-\sqrt{y} \le X \le \sqrt{y})$。因为 $X \in (0,1)$，所以 $F_Y(y) = P(0 < X \le \sqrt{y}) = \sqrt{y}$（当 $0 < y < 1$）。对 $y$ 求导得 $f_Y(y) = F_Y'(y) = \frac{1}{2\sqrt{y}}$。完整分布函数为 $F_Y(y)=0$（$y\le0$）、$\sqrt y$（$0<y<1$）、1（$y\ge1$）。故密度在 $(0,1)$ 为 $\frac{1}{2\sqrt y}$，区间外可取0，且 $\int_0^1\frac{dy}{2\sqrt y}=1$。

**答案原文**

$f_Y(y)=\frac{1}{2\sqrt y}$（$0<y<1$），区间外为0。

## 218. linalg-048

内容 SHA256：`bd342d0e2e3aaa132e2e1dedcc4913a51a095c8af87029131adbe4c70af5d2b9`。

来源：reviews/codex-supervision/2026-10-06-holdout-strict-fix/linalg048-v2/candidate.json；源 SHA256 `05fb0b57d733df7140573f77ffd627901adf18d9a82648b1f25b1affb3297150`；行 —，JSON pointer `/`。

**题干**

已知矩阵 $A=\begin{pmatrix}1&3\\0&1\end{pmatrix}$，求该矩阵对应的线性变换对二维平面的几何影响。

**过程**

对任意点 $(x,y)$，$T(x,y)=A\begin{pmatrix}x\\y\end{pmatrix}=\begin{pmatrix}x+3y\\y\end{pmatrix}$，位移为 $(3y,0)$。故 $x$ 轴逐点固定，$\vec e_1=(1,0)$ 不动，$\vec e_2=(0,1)$ 映为 $(3,1)$。对于任意 $c\in\mathbb R$，$T(\mathbb R\times\{c\})=\mathbb R\times\{c\}$：整条水平直线作为点集保持不变，其上每个带标记点的横坐标增加 $3c$。有限线段 $[0,1]\times\{c\}$ 则映为 $[3c,1+3c]\times\{c\}$。竖直线 $x=c$ 的像可写为 $(X,Y)=(c+3t,t)$，$t\in\mathbb R$，即 $X-3Y=c$，斜率为 $\frac13$。沿边界次序，单位正方形顶点 $(0,0),(1,0),(1,1),(0,1)$ 依次映为 $(0,0),(1,0),(4,1),(3,1)$，得到底长 $1$、高 $1$ 的平行四边形。$\det A=1\cdot1-3\cdot0=1$，故面积与定向均保持。这是一种水平剪切；移动距离为 $3|y|$，纵坐标不变。长度一般不保持，例如 $\|(0,1)\|=1$ 而 $\|T(0,1)\|=\sqrt{10}$。

**答案原文**

水平剪切 $T(x,y)=(x+3y,y)$；$x$ 轴逐点固定，水平直线作为点集不变、带标记点移动 $3y$；竖直线 $x=c$ 映为 $X-3Y=c$；面积和定向保持，$\det A=1$，长度一般不保持。

## 219. calc-series-016

内容 SHA256：`bd34dc3020500203a674611b47cdfd3d7bce2fb1a687498891d75b5dd97a57a6`。

来源：dataset_calc.json；源 SHA256 `3c3498a772d278ee41f25e5a66d8cdeac85901bbdbc71d407952ddf9e52d929d`；行 —，JSON pointer `/14`。

**题干**

求幂级数 $\sum_{n=1}^{\infty} \frac{x^n}{n \cdot 2^n}$ 的收敛域及和函数。

**过程**

收敛半径 $R = \lim_{n \to \infty} \left| \frac{a_n}{a_{n+1}} \right| = \lim_{n \to \infty} \frac{(n+1)2^{n+1}}{n2^n} = 2$。当 $x=2$ 时，级数为调和级数 $\sum \frac{1}{n}$，发散；当 $x=-2$ 时，级数为交错级数 $\sum \frac{(-1)^n}{n}$，收敛。故收敛域为 $[-2, 2)$。设和函数 $S(x) = \sum_{n=1}^{\infty} \frac{x^n}{n2^n}$，逐项求导得 $S'(x) = \sum_{n=1}^{\infty} \frac{x^{n-1}}{2^n} = \frac{1}{2} \cdot \frac{1}{1-x/2} = \frac{1}{2-x}$。两边从0到x积分得 $S(x) = \int_0^x \frac{1}{2-t} dt = -\ln(2-x) + \ln 2 = -\ln(1 - x/2)$。

**答案原文**

收敛域 $[-2, 2)$，和函数 $S(x) = -\ln(1 - x/2)$

## 220. draft-c23-04

内容 SHA256：`be4087c2050e20e79e0540c64e50ecbb9fe38b3ab93409c32e6f01014276813b`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft.jsonl；源 SHA256 `e0eb9bf14b1cdf0919006ede0e9523046d0edadffb69ac3a10e4941a77563756`；行 14，JSON pointer `/`。

**题干**

求关于平面 $\pi:x+y+z=0$ 的反射矩阵，并验证平面上的点不动、法向量反向。

**过程**

平面单位法向量 $n=\frac{1}{\sqrt3}(1,1,1)$。反射矩阵 $S=I-2nn^{\mathsf T}=I-\frac{2}{3}\begin{pmatrix}1&1&1\\1&1&1\\1&1&1\end{pmatrix}=\begin{pmatrix}\frac13&-\frac23&-\frac23\\-\frac23&\frac13&-\frac23\\-\frac23&-\frac23&\frac13\end{pmatrix}$。验证:对平面上点 $(x,y,z)$($x+y+z=0$),$S(x,y,z)=(x,y,z)-\frac{2}{3}(x+y+z)(1,1,1)=(x,y,z)$,不动 ✓;对法向量 $(1,1,1)$,$S(1,1,1)=(1,1,1)-\frac23\cdot3\cdot(1,1,1)=-(1,1,1)$,反向 ✓。另 $\det S=-1$,为反射的特征。

**答案原文**

$S=\begin{pmatrix}\frac13&-\frac23&-\frac23\\-\frac23&\frac13&-\frac23\\-\frac23&-\frac23&\frac13\end{pmatrix}$;平面点不动、法向量反向,已验证。

## 221. draft-c21-02

内容 SHA256：`bf30fcc239e87b2ef6c5fd0e8e5f303a0ff63e14e2bc9fb8257d088a2d5198d5`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-05/draft.jsonl；源 SHA256 `d37d937851dd65a04639ac056400cd3d508fd96a4cbec235d17dd573fb499084`；行 2，JSON pointer `/`。

**题干**

设直线 $l_a=\{(a,0,t):t\in\mathbb R\}$。求使 $l_a$ 与球面 $x^2+y^2+z^2=4$ 相交于两点、相切、无交点的 $a$ 的取值范围，并求相切时的切点。

**过程**

代入 $x=a,y=0$:$a^2+t^2=4$,即 $t^2=4-a^2$。当 $4-a^2>0$(即 $|a|<2$)时,方程有两个实根,相交于两点;当 $4-a^2=0$(即 $|a|=2$)时,只有一个根 $t=0$,相切,切点为 $(2,0,0)$ 与 $(-2,0,0)$;当 $4-a^2<0$(即 $|a|>2$)时,无实根,无交点。

**答案原文**

$|a|<2$ 时相交于两点;$|a|=2$ 时相切,切点为 $(\pm2,0,0)$;$|a|>2$ 时无交点。

## 222. draft-c11-05

内容 SHA256：`bfdaaeb44ac2d68c0e2feecfbbbe49a112ca678232a8b0cf1644f3bffe53ce8a`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-02.jsonl；源 SHA256 `286625ebf0f88cca49b14f36be4bab4e5f3b29ecc0764226b7ebb5fb61a16527`；行 5，JSON pointer `/`。

**题干**

求幂级数 $\sum_{n=1}^{\infty}\frac{(-1)^nx^n}{n}$ 的收敛域与和函数，并求 $x=1$ 处的值(说明所用定理)。

**过程**

当 $|x|<1$ 时由比值法绝对收敛。当 $x=1$ 时，级数为 $\sum_{n=1}^{\infty}\frac{(-1)^n}{n}$，由莱布尼茨判别法($\frac1n$ 单调递减趋于 $0$)收敛；当 $x=-1$ 时，级数为 $\sum\frac{1}{n}$，发散。故收敛域为 $(-1,1]$。求和：对 $|x|<1$，$\sum_{n=1}^{\infty}(-1)^{n+1}\frac{x^n}{n}=\ln(1+x)$，故 $S(x)=-\ln(1+x)$。$x=1$ 处级数收敛，由阿贝尔定理，$S(1)=\lim_{x\to1^-}S(x)=\lim_{x\to1^-}-\ln(1+x)=-\ln2$。

**答案原文**

收敛域 $(-1,1]$;$S(x)=-\ln(1+x)$;$S(1)=-\ln2$(由阿贝尔定理)。

## 223. draft-c13-05

内容 SHA256：`bfec1ccbe51240f8c5aaba1d8f67be1fd2137cac7fc42c582fbc1b5ad58e54a3`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft.jsonl；源 SHA256 `4a8930a557e05b01cec58257879ecd5bd9679b9c08e3e478767c363642ebe382`；行 5，JSON pointer `/`。

**题干**

说明级数 $\sum_{n=1}^{\infty}\frac{1}{n^2+1}$ 能否用部分分式裂项法求和，并说明理由；再用比较判别法与裂项上界证明该级数的和小于 $2$。

**过程**

不能直接裂项求和：$n^2+1$ 在实数域没有一次因式，部分分式分解不含 $\frac{1}{n-\alpha}$ 型项，无法构造相邻抵消的差分结构(对照 $n^2-1=(n-1)(n+1)$ 的情形)。上界估计：$\frac{1}{n^2+1}<\frac{1}{n^2}$，故 $S<\sum_{n=1}^{\infty}\frac{1}{n^2}$。又 $\frac{1}{n^2}<\frac{1}{n(n-1)}=\frac{1}{n-1}-\frac{1}{n}$($n\ge2$)，故 $\sum_{n=1}^{\infty}\frac{1}{n^2}=1+\sum_{n=2}^{\infty}\frac{1}{n^2}<1+\sum_{n=2}^{\infty}\left(\frac{1}{n-1}-\frac{1}{n}\right)=1+1=2$。于是 $S<2$。

**答案原文**

不能裂项求和(分母无实一次因式,无法构造差分抵消);$S<2$(比较判别+裂项上界)。

## 224. draft-c47-03

内容 SHA256：`c1d0c88ae0ce8f853cd14de05222b2cce16d173c936af903c3fc531d59f29b13`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft.jsonl；源 SHA256 `bcd6ec3d0204b822f83440669662afcfe3ec7712fa4806d51506f98cb797b0c2`；行 3，JSON pointer `/`。

**题干**

证明:当 $n\to\infty$、$p\to0$ 且 $np\to\lambda>0$ 时，对固定的 $k$，$B(n,p)$ 在 $k$ 处的概率趋于 $\frac{\lambda^k}{k!}e^{-\lambda}$。

**过程**

记 $p_n$ 满足 $np_n\to\lambda$。$P(X=k)=\binom{n}{k}p_n^k(1-p_n)^{n-k}=\frac{n(n-1)\cdots(n-k+1)}{k!}\cdot p_n^k\cdot(1-p_n)^{n-k}$。改写为 $\frac{(np_n)^k}{k!}\cdot\frac{n(n-1)\cdots(n-k+1)}{n^k}\cdot(1-p_n)^{n-k}$。第一因子 $(np_n)^k\to\lambda^k$;第二因子 $\frac{n}{n}\cdot\frac{n-1}{n}\cdots\frac{n-k+1}{n}\to1$($k$ 固定);第三因子 $(1-p_n)^{n-k}=(1-p_n)^{n}/(1-p_n)^k$,其中 $(1-p_n)^n=(1-\frac{np_n}{n})^n\to e^{-\lambda}$ 且 $(1-p_n)^k\to1$。故极限为 $\frac{\lambda^k}{k!}e^{-\lambda}$。

**答案原文**

证明见解法(三因子分别取极限:$\lambda^k/k!$、$1$、$e^{-\lambda}$)。

## 225. draft-c24-02

内容 SHA256：`c217c3a3df20ecda255ae90247c2db9b90a417734c8a22eff02984671a899a73`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft.jsonl；源 SHA256 `25705ed80dbac40074a2bc29ed482de0087b12bc96d3e1ec0cb9f77722fefe0e`；行 2，JSON pointer `/`。

**题干**

仿射变换 $\begin{cases}x'=x\\ y'=2y\end{cases}$ 把圆 $x^2+y^2=1$ 与抛物线 $y=x^2$ 分别变成什么曲线？

**过程**

对圆:反解 $x=x',y=\frac{y'}{2}$,代入得 $x'^2+\frac{y'^2}{4}=1$,即长半轴 $2$、短半轴 $1$ 的椭圆。对抛物线:代入得 $\frac{y'}{2}=x'^2$,即 $y'=2x'^2$,仍是抛物线(开口更窄)。

**答案原文**

圆变为椭圆 $x'^2+\frac{y'^2}{4}=1$;抛物线变为 $y'=2x'^2$(仍为抛物线)。

## 226. linalg-057

内容 SHA256：`c2a7e583ef8e5db17402dee0a8cb56110815518239b00a2004a49240bf185590`。

来源：reviews/codex-supervision/history-from-code/clone-check/reviews/2026-10-03-prep-recheck/results.json；源 SHA256 `078e6bbd0c76184d36494245ab5fa7c1bbb875cfa226cdcd88c09d9c47c6d3c8`；行 —，JSON pointer `/answer_record_snapshot/linalg-057`。

**题干**

已知矩阵 $A=\begin{pmatrix} 2 & 1 \\ 1 & 1 \end{pmatrix}$，求其逆矩阵，并说明可逆性的几何意义。

**过程**

计算 $\det(A)=2\times1-1\times1=1\neq0$，矩阵可逆。$A^{-1}=\frac{1}{1}\begin{pmatrix} 1 & -1 \\ -1 & 2 \end{pmatrix}=\begin{pmatrix} 1 & -1 \\ -1 & 2 \end{pmatrix}$。几何上，可逆意味着该线性变换不将空间压缩到更低维度，存在逆变换将空间恢复。

**答案原文**

$A^{-1}=\begin{pmatrix} 1 & -1 \\ -1 & 2 \end{pmatrix}$；几何意义：可逆变换不将空间压缩到更低维度，存在逆变换将空间恢复原状

## 227. draft-c52-03

内容 SHA256：`c2cf1a09eccd1d74b95d4324301c4993424747da51033799c603e546a1531f5e`。

来源：reviews/codex-supervision/2026-10-05-math-template-followup-v2/batch01-corrected-review-copy-v2.jsonl；源 SHA256 `d0c82fcc9503c4affd525ea22ba1387722b3e3d13ee215592f42e3824642bf42`；行 13，JSON pointer `/`。

**题干**

设随机变量 $X$ 服从区间 $(-1,2)$ 上的均匀分布，求 $Y=X^2$ 的概率密度函数，并指出密度分段的分界点。

**过程**

$X$ 的密度为 $\frac{1}{3}$($-1<x<2$)。$Y=X^2$ 的值域为 $[0,4)$。当 $0<y<1$ 时，$[-\sqrt{y},\sqrt{y}]\subset(-1,2)$，故 $F_Y(y)=P(X^2\leq y)=\frac{2\sqrt{y}}{3}$，$f_Y(y)=\frac{1}{3\sqrt{y}}$。当 $1\leq y<4$ 时，区间 $[-\sqrt{y},\sqrt{y}]$ 与支持集 $(-1,2)$ 的交为 $(-1,\sqrt{y}]$，故 $F_Y(y)=\frac{\sqrt{y}+1}{3}$，$f_Y(y)=\frac{1}{6\sqrt{y}}$。分界点为 $y=1$，两侧密度在该点有跳跃。验证总质量：$\int_0^1\frac{1}{3\sqrt{y}}\,dy+\int_1^4\frac{1}{6\sqrt{y}}\,dy=\frac{2}{3}+\frac{1}{3}=1$。完整CDF在 $y\le0$ 时为0，在 $y\ge4$ 时为1。$y=1$ 的CDF连续，左右导数不同；密度在这个单点可任取有限非负值，这不产生概率原子。

**答案原文**

$f_Y(y)=\frac{1}{3\sqrt{y}}$(当 $0<y<1$)；$f_Y(y)=\frac{1}{6\sqrt{y}}$(当 $1\leq y<4$)；其余为 $0$。分界点 $y=1$。

## 228. draft-c49-01

内容 SHA256：`c34064a05fe18e2c50bcab625468cf40795f0b799f5a7016e83fda9890f749bf`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft.jsonl；源 SHA256 `bcd6ec3d0204b822f83440669662afcfe3ec7712fa4806d51506f98cb797b0c2`；行 11，JSON pointer `/`。

**题干**

设随机变量 $X$ 的均值为 $5$、方差为 $1$。用切比雪夫不等式估计 $P(|X-5|\ge3)$ 的上界。

**过程**

切比雪夫不等式:$P(|X-EX|\ge\varepsilon)\le\frac{Var(X)}{\varepsilon^2}$。取 $\varepsilon=3$:$P(|X-5|\ge3)\le\frac{1}{3^2}=\frac19$。

**答案原文**

$P(|X-5|\ge3)\le\frac19$。

## 229. draft-c37-02

内容 SHA256：`c45722d48c49d232926ea307cb660a05e2c879271ec106237a3b6b6fc643ded6`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft.jsonl；源 SHA256 `afcd74e3e4d285e77802f29ab182f9dce80cfe5833b983feb8af34694ed15331`；行 7，JSON pointer `/`。

**题干**

在次数不超过 $2$ 的实系数多项式空间 $V$ 中，求从基 $\{1,x,x^2\}$ 到基 $\{1,\,x-1,\,(x-1)^2\}$ 的过渡矩阵，并求 $p(x)=2x^2+3x+4$ 在新基下的坐标。

**过程**

新基各元素在旧基 $\{1,x,x^2\}$ 下的坐标：$1=(1,0,0)$，$x-1=(-1,1,0)$，$(x-1)^2=x^2-2x+1=(1,-2,1)$。故过渡矩阵 $P=\begin{pmatrix}1&-1&1\\0&1&-2\\0&0&1\end{pmatrix}$。$p$ 在旧基下的坐标为 $(4,3,2)$。解 $P\xi=(4,3,2)^{\mathsf T}$：由回代得 $P^{-1}=\begin{pmatrix}1&1&1\\0&1&2\\0&0&1\end{pmatrix}$，故 $\xi=(4+3+2,\,3+4,\,2)=(9,7,2)$。验证:$9\cdot1+7(x-1)+2(x-1)^2=9+7x-7+2x^2-4x+2=2x^2+3x+4=p(x)$。

**答案原文**

过渡矩阵 $P=\begin{pmatrix}1&-1&1\\0&1&-2\\0&0&1\end{pmatrix}$;$p$ 在新基下的坐标为 $(9,7,2)$。

## 230. calc-series-019

内容 SHA256：`c4acdf2a6f5e823c73690fef05b61b9d16b3c5ecb698e311a9c5a1641f7a26ee`。

来源：dataset_calc.json；源 SHA256 `3c3498a772d278ee41f25e5a66d8cdeac85901bbdbc71d407952ddf9e52d929d`；行 —，JSON pointer `/17`。

**题干**

判断正项级数 $\sum_{n=1}^{\infty} \frac{1}{n^2+n}$ 的敛散性，若收敛，求其和。

**过程**

因为 $\frac{1}{n^2+n} = \frac{1}{n(n+1)} = \frac{1}{n} - \frac{1}{n+1}$。级数的部分和 $S_n = (1 - \frac{1}{2}) + (\frac{1}{2} - \frac{1}{3}) + \dots + (\frac{1}{n} - \frac{1}{n+1}) = 1 - \frac{1}{n+1}$。取极限 $\lim_{n \to \infty} S_n = 1$，故级数收敛，和为 1。

**答案原文**

1

## 231. draft-c26-04

内容 SHA256：`c4c8a43ffbea8bc3cb003502ade6e4b75bb6fdcea011e2e9a089b4754b5b6cb1`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft.jsonl；源 SHA256 `25705ed80dbac40074a2bc29ed482de0087b12bc96d3e1ec0cb9f77722fefe0e`；行 14，JSON pointer `/`。

**题干**

求矩阵 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 的特征值与特征向量，并从几何上解释为什么它不可对角化。

**过程**

特征方程 $|A-\lambda I|=(1-\lambda)^2=0$,特征值 $\lambda=1$(二重)。特征向量:解 $(A-I)v=0$,即 $\begin{pmatrix}0&1\\0&0\end{pmatrix}v=0$,得 $v_2=0$,特征子空间为 $x$ 轴,维数为 $1$,小于代数重数 $2$,故不可对角化。几何解释:$A$ 是剪切变换($A(x,y)=(x+y,y)$,横坐标平移 $y$)。它保持 $x$ 轴上的点不动(特征方向只有这一个),其余点都沿水平方向被推移而非沿某方向伸缩;剪切没有第二个特征方向,因此无法通过基变换化为对角矩阵(对角矩阵的几何作用是沿坐标轴伸缩,而剪切不是伸缩)。

**答案原文**

特征值 $1$(二重),特征子空间为 $x$ 轴(维数 $1$);剪切无第二个特征方向,不可对角化。

## 232. eval-linalg-019-s3

内容 SHA256：`c529f97781ec5b8a096c8f8cc254b9bab29a1aeeafae19d7168ddef97a545a74`。

来源：reviews/codex-supervision/history-from-code/recheck-68c51be/data/v2/eval/dataset_eval.json；源 SHA256 `1de2df62edd0b01403df813c80edc3a5a9dbf1791f0b223d8e0f107ccee55e6e`；行 —，JSON pointer `/251`。

**题干**

将二次型 $f(x,y)=2x^2+2xy+3y^2$ 化为标准形，并说明其正定性。

**过程**

$A$ 的一阶顺序主子式 $2>0$；二阶顺序主子式 $\det A=2\cdot 3-1=5>0$。由 Sylvester 判据，全部顺序主子式为正 $\iff$ 二次型正定，正惯性指数为 $2$、负惯性指数为 $0$。

**答案原文**

配方法标准形 $2u^2+\dfrac{5}{2}v^2$（$u=x+\dfrac{y}{2}$，$v=y$）；正交标准形 $\dfrac{5+\sqrt5}{2}\xi^2+\dfrac{5-\sqrt5}{2}\eta^2$；正定

## 233. draft-c14-01

内容 SHA256：`c65752c7472c0c9deaea82902364485f06486045f7b1b57deb7bd4f085cce2f5`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft.jsonl；源 SHA256 `1cc220e2699b799fb9bacc8525e1f9d82321dc39dacd33e5c1caa21c1a7d959b`；行 11，JSON pointer `/`。

**题干**

将 $f(x)=x^2$($-\pi\le x\le\pi$)展开为傅立叶级数，并由此推导 $\sum_{n=1}^{\infty}\frac{1}{n^2}=\frac{\pi^2}{6}$。

**过程**

$f$ 为偶函数,故 $b_n=0$。$a_0=\frac1\pi\int_{-\pi}^{\pi}x^2\,dx=\frac1\pi\cdot\frac{2\pi^3}{3}=\frac{2\pi^2}{3}$。$a_n=\frac1\pi\int_{-\pi}^{\pi}x^2\cos nx\,dx$。两次分部积分:$\int x^2\cos nx\,dx=\frac{x^2\sin nx}{n}+\frac{2x\cos nx}{n^2}-\frac{2\sin nx}{n^3}$,代入上下限得 $\int_{-\pi}^{\pi}x^2\cos nx\,dx=\frac{4\pi(-1)^n}{n^2}$($\sin n\pi=0$,$\cos n\pi=(-1)^n$),故 $a_n=\frac{4(-1)^n}{n^2}$。于是 $x^2=\frac{\pi^2}{3}+4\sum_{n=1}^{\infty}\frac{(-1)^n\cos nx}{n^2}$。取 $x=\pi$:$\pi^2=\frac{\pi^2}{3}+4\sum_{n=1}^{\infty}\frac{1}{n^2}$,解得 $\sum_{n=1}^{\infty}\frac{1}{n^2}=\frac{\pi^2}{6}$。

**答案原文**

$x^2=\frac{\pi^2}{3}+4\sum_{n=1}^{\infty}\frac{(-1)^n\cos nx}{n^2}$;$\sum_{n=1}^{\infty}\frac{1}{n^2}=\frac{\pi^2}{6}$。

## 234. draft-c42-04

内容 SHA256：`c8cf2c138de8e067f0d7730b4b9f7dea9ecc91fb8ddd4a4fdd6f0f5e2012ef39`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft.jsonl；源 SHA256 `58ae126d6bd255576c005783f78e6ade29c9f0bd60b1c7fa2e0971ba6cad1a00`；行 14，JSON pointer `/`。

**题干**

判断矩阵 $A=\begin{pmatrix}\frac12&\frac{\sqrt3}{2}&0\\-\frac{\sqrt3}{2}&\frac12&0\\0&0&-1\end{pmatrix}$ 是否为正交矩阵；若是，说明其对应的几何变换。

**过程**

各列(行)两两正交且模长为 $1$,故 $A^{\mathsf T}A=I$,$A$ 是正交矩阵。$\det A=\left(\frac14+\frac34\right)\times(-1)=-1$。几何结构:前两行前两列构成旋转块 $\begin{pmatrix}\frac12&\frac{\sqrt3}{2}\\-\frac{\sqrt3}{2}&\frac12\end{pmatrix}=R(-60^\circ)$($\cos60^\circ=\frac12$,$\sin(-60^\circ)=-\frac{\sqrt3}{2}$,即绕 $z$ 轴顺时针旋转 $60^\circ$),第三分量为 $-1$(关于 $xy$ 平面的反射)。特征值:旋转块的特征值为 $e^{\pm i\pi/3}=\frac12\pm i\frac{\sqrt3}{2}$,第三分量给 $-1$(特征向量 $(0,0,1)$);$A$ 没有特征值 $1$,不存在 $xy$ 平面内的旋转轴。故 $A$ 是「绕 $z$ 轴旋转 $-60^\circ$」与「关于 $xy$ 平面反射」的复合(旋转反射,二者可交换,$\det=-1$)。

**答案原文**

正交,$\det=-1$;对应绕 $z$ 轴旋转 $-60^\circ$(顺时针)与关于 $xy$ 平面反射的复合(旋转反射,可交换)。

## 235. draft-c29-01

内容 SHA256：`c9aabbcdcbc4797000d1ebfc1109d0f6039f82ed6359954e206009a5a0c3af3b`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft.jsonl；源 SHA256 `e019465093b291bd83fb6ae20f3eefc40a96df3e5137a246ad8813dd03f87b34`；行 6，JSON pointer `/`。

**题干**

用有理根定理将多项式 $f(x)=x^3-7x+6$ 在实数域上因式分解。

**过程**

有理根定理:首项系数为 $1$,有理根必为整数且是常数项 $6$ 的因子,候选为 $\pm1,\pm2,\pm3,\pm6$。试根:$f(1)=1-7+6=0$,故 $x-1$ 是因子。综合除法:$x^3-7x+6=(x-1)(x^2+x-6)=(x-1)(x-2)(x+3)$。

**答案原文**

$x^3-7x+6=(x-1)(x-2)(x+3)$。

## 236. draft-c41-05

内容 SHA256：`ca45c718d9216d02381490e839e81ae009445465d9429e95d57dd7e8a6cf0125`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft.jsonl；源 SHA256 `58ae126d6bd255576c005783f78e6ade29c9f0bd60b1c7fa2e0971ba6cad1a00`；行 10，JSON pointer `/`。

**题干**

证明:若尔当块 $J_m(\lambda)$ 的幂零部分 $N=J_m(0)$ 满足 $\dim\ker N^k=\min(k,m)$；并说明这一公式如何由核维数序列唯一确定若尔当块的个数与大小。

**过程**

$N=J_m(0)$ 是把基向量向前推一位的位移算子:$Ne_1=0$,$Ne_i=e_{i-1}$($i\ge2$)。于是 $N^k$ 把 $e_i$ 映为 $e_{i-k}$($i>k$)或 $0$($i\le k$),即 $N^k$ 的像由 $e_1,\dots,e_{m-k}$ 张成(当 $k<m$),秩为 $m-k$;当 $k\ge m$ 时 $N^k=0$,秩为 $0$。由秩-零度,$\dim\ker N^k=m-(m-k)=k$($k<m$),$\dim\ker N^k=m$($k\ge m$),即 $\min(k,m)$。块结构:对一般矩阵,设 $r_k=\dim\ker(A-\lambda I)^k$,则大小至少为 $k$ 的 $\lambda$ 块数为 $r_k-r_{k-1}$(每个 $m$ 阶块对 $r_k$ 贡献 $\min(k,m)$,相邻差即 $\min(k,m)-\min(k-1,m)$,恰好是大小为 $\ge k$ 的块数贡献的 $1$)。故核维数序列 $r_0=0,r_1,r_2,\dots$ 的差分解唯一确定各阶块数。

**答案原文**

证明见解法(位移算子的核维数 $\\min(k,m)$;块数 $=r_k-r_{k-1}$ 的差分解唯一确定块结构)。

## 237. draft-c48-01

内容 SHA256：`cb881d1359c0ae62bf87d9da92d99718a9f02765c69c9f9b7ae7032c3da196a7`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft.jsonl；源 SHA256 `bcd6ec3d0204b822f83440669662afcfe3ec7712fa4806d51506f98cb797b0c2`；行 6，JSON pointer `/`。

**题干**

设 $X\sim N(2,9)$。求 $P(X\le5)$。

**过程**

标准化:$Z=\frac{X-2}{3}\sim N(0,1)$。$P(X\le5)=P\left(Z\le\frac{5-2}{3}\right)=P(Z\le1)=\Phi(1)\approx0.8413$。

**答案原文**

$P(X\le5)=\Phi(1)\approx0.8413$。

## 238. draft-c46-01

内容 SHA256：`cbc3c5a3eb73346a0af2d367b1881328b3f2a7c60d6d0fc0129439afbea65182`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-06.jsonl；源 SHA256 `756525876eec2bd8dbc8d8f3e28afbf61ca70fd4cab235964621646009a7ae5f`；行 11，JSON pointer `/`。

**题干**

甲、乙在$12$点到$13$点之间独立到达，各自的到达时刻在该时段上均匀分布；先到者等待$15$分钟后离开。求两人相遇的概率。

**过程**

设甲到达时刻为 $x$,乙为 $y$,相互独立且均服从 $[0,1]$ 上的均匀分布($1$ 小时归一化),样本空间为单位正方形。相遇当且仅当 $|x-y|\le\frac14$。在正方形中,$|x-y|\le\frac14$ 的区域为对角线带,其面积为总面积减去两个直角边长 $\frac34$ 的等腰直角三角形:相遇概率 $P=1-2\times\frac12\times\left(\frac34\right)^2=1-\frac{9}{16}=\frac{7}{16}$。

**答案原文**

相遇概率为 $\frac{7}{16}$。

## 239. draft-c22-03

内容 SHA256：`ce0219cc29bcf8d0512efb98f5a9c6398458040ba47cccd61e19ec31aa947937`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft.jsonl；源 SHA256 `e0eb9bf14b1cdf0919006ede0e9523046d0edadffb69ac3a10e4941a77563756`；行 8，JSON pointer `/`。

**题干**

求双曲抛物面 $z=xy$ 的两族直母线，并说明过曲面上每一点恰有两条母线。

**过程**

对每个实数 $t$,直线 $\{(x,t,tx)\}$ 在曲面上(因为 $z=tx=xy$ 当 $y=t$);同样 $\{(t,y,ty)\}$ 也在曲面上(当 $x=t$)。故两族母线为 $l_1(t):\{(x,t,tx)\}$ 与 $l_2(t):\{(t,y,ty)\}$。过点 $(a,b,ab)$:取 $t=b$ 得第一族母线,取 $t=a$ 得第二族母线。完备性:设过 $(a,b,ab)$、方向为 $(u,v,w)$ 的直线在曲面上,则 $ab+tw=(a+tu)(b+tv)$ 对一切 $t$ 成立,即 $tw=(av+bu)t+uvt^2$,比较系数得 $uv=0$ 且 $w=av+bu$:$u=0$ 时是第二族($x\equiv a$),$v=0$ 时是第一族($y\equiv b$)。故过该点恰有两条母线。

**答案原文**

两族母线:$\{(x,t,tx)\}$ 与 $\{(t,y,ty)\}$($t$ 为参数);过每点恰有两条母线(完备性由比较系数 $uv=0$ 保证)。

## 240. draft-c51-05

内容 SHA256：`cedf08c5e8031a5edea9dd656293d366d1b8f0402fe5e84f4daa0f2de8a034ad`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft.jsonl；源 SHA256 `71d46f404c59db6194494bf8ea2353202b77f602a15522f58c1b4599d1cbb07a`；行 15，JSON pointer `/`。

**题干**

设 $H$ 与 $\bar H$ 为互斥且穷尽的假设，观测 $D_1,D_2$ 在给定 $H$(及给定 $\bar H$)下条件独立。证明后验优势比可写成先验优势比与两个似然比的乘积，并说明更新顺序不影响最终后验；再用两次独立阳性检测的数据($P(H)=\frac{1}{1000}$，灵敏度与误报率均为 $\frac{99}{100}$ 与 $\frac{1}{100}$)验证所得后验为 $\frac{363}{400}$。

**过程**

由贝叶斯公式与条件独立性，$\frac{P(H\mid D_1,D_2)}{P(\bar H\mid D_1,D_2)}=\frac{P(H)}{P(\bar H)}\cdot\frac{P(D_1\mid H)}{P(D_1\mid\bar H)}\cdot\frac{P(D_2\mid H)}{P(D_2\mid\bar H)}$。乘积形式对 $D_1,D_2$ 对称，故更新顺序不影响最终后验优势比。验证:先验优势比 $\frac{P(H)}{P(\bar H)}=\frac{1}{999}$;每次阳性的似然比 $\frac{99/100}{1/100}=99$。两次阳性后，后验优势比 $=\frac{1}{999}\times99^2=\frac{9801}{999}=\frac{363}{37}$，故后验概率 $=\frac{363}{363+37}=\frac{363}{400}$，与逐次更新结果一致。

**答案原文**

证明见解法(乘积形式);验证:$P(H\mid +_1,+_2)=\frac{363}{400}$。

## 241. draft-c37-01

内容 SHA256：`d017915ab079443606b311f6b80db3d58e5884b5c12c996b2af6c368ad4bf2f1`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft.jsonl；源 SHA256 `afcd74e3e4d285e77802f29ab182f9dce80cfe5833b983feb8af34694ed15331`；行 6，JSON pointer `/`。

**题干**

在 $\mathbb R^3$ 中，求从标准基 $\varepsilon_1,\varepsilon_2,\varepsilon_3$ 到基 $\eta_1=(1,1,0)$，$\eta_2=(0,1,1)$，$\eta_3=(1,0,1)$ 的过渡矩阵，并求向量 $\alpha=(1,2,3)$ 在基 $\eta_1,\eta_2,\eta_3$ 下的坐标。

**过程**

过渡矩阵以新基向量在旧基下的坐标作列：$P=\begin{pmatrix}1&0&1\\1&1&0\\0&1&1\end{pmatrix}$。求 $\alpha$ 的新坐标即解 $P\xi=\alpha$。由增广消元(或直接求逆)得 $P^{-1}=\frac12\begin{pmatrix}1&1&-1\\-1&1&1\\1&-1&1\end{pmatrix}$，故 $\xi=P^{-1}\alpha=\frac12(1+2-3,\,-1+2+3,\,1-2+3)=\frac12(0,4,2)=(0,2,1)$。验证:$0\cdot\eta_1+2\eta_2+1\cdot\eta_3=2(0,1,1)+(1,0,1)=(1,2,3)=\alpha$。

**答案原文**

过渡矩阵 $P=\begin{pmatrix}1&0&1\\1&1&0\\0&1&1\end{pmatrix}$;$\alpha$ 在新基下的坐标为 $(0,2,1)$。

## 242. draft-c36-04

内容 SHA256：`d05dd21d03020af570d16ba6f21033f7318cad0b919e2b16638d28db074d086e`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft.jsonl；源 SHA256 `13fe6a370d3c46ae8ca6c1b16c9cd98fbedcc8648087f11a70ff046951db5479`；行 9，JSON pointer `/`。

**题干**

判断二次型 $f(x,y,z)=(x-y)^2+2(y-z)^2$ 是否正定；若不正定，判断其是否半正定，并求该二次型的秩。

**过程**

由表达式可见 $f\geq 0$ 恒成立。$f=0$ 当且仅当 $x-y=0$ 且 $y-z=0$，即 $x=y=z$，存在非零解(如 $(1,1,1)$)，故半正定但非正定。展开得 $f=x^2-2xy+3y^2-4yz+2z^2$，对应矩阵 $A=\begin{pmatrix}1&-1&0\\-1&3&-2\\0&-2&2\end{pmatrix}$。计算 $\det A=1\times(3\times2-(-2)\times(-2))-(-1)\times((-1)\times2-0)+0=2-2=0$，而二阶主子式 $\det\begin{pmatrix}1&-1\\-1&3\end{pmatrix}=2\neq0$，故秩为 $2$(零度为 $3-2=1$，与零空间 $\{(t,t,t)\}$ 一致)。

**答案原文**

不正定；半正定；秩为 $2$。

## 243. draft-c25-01

内容 SHA256：`d11741b168f2859e927eeba4f53b8d6c9bda11098b4a15b60119237b9dc4900e`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft.jsonl；源 SHA256 `25705ed80dbac40074a2bc29ed482de0087b12bc96d3e1ec0cb9f77722fefe0e`；行 6，JSON pointer `/`。

**题干**

求球面 $x^2+y^2+z^2=1$ 与平面 $z=\frac12$ 的交线的参数方程，并说明其形状。

**过程**

代入 $z=\frac12$:$x^2+y^2=1-\frac14=\frac34$。交线是平面 $z=\frac12$ 内的圆,半径 $\frac{\sqrt3}{2}$,圆心 $(0,0,\frac12)$。参数方程:$x=\frac{\sqrt3}{2}\cos t$,$y=\frac{\sqrt3}{2}\sin t$,$z=\frac12$($0\le t\le2\pi$)。

**答案原文**

交线为平面 $z=\frac12$ 内的圆:$x=\frac{\sqrt3}{2}\cos t,\ y=\frac{\sqrt3}{2}\sin t,\ z=\frac12$。

## 244. draft-c34-03

内容 SHA256：`d1902a0acb04dd220f6fb21a4dda67207dac1783e2bdc09704b803d45b118e01`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft.jsonl；源 SHA256 `2a488597e92f7efdb6ec80074b147c9290e949fbeb4cbd114e293657e7c04776`；行 3，JSON pointer `/`。

**题干**

设 $P_1$ 是交换第一、二行的初等矩阵，$P_2$ 是把第一行乘以 $2$ 的初等矩阵。求先交换第一、二行、再把新第一行乘以 $2$ 的复合初等矩阵。

**过程**

$P_1=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}$,$P_2=\begin{pmatrix}2&0&0\\0&1&0\\0&0&1\end{pmatrix}$。先做 $P_1$ 后做 $P_2$ 对应左乘 $P_2P_1$(先作用的矩阵写在右边):$P_2P_1=\begin{pmatrix}2&0&0\\0&1&0\\0&0&1\end{pmatrix}\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}=\begin{pmatrix}0&2&0\\1&0&0\\0&0&1\end{pmatrix}$。复合矩阵把第二行换到第一行并乘以 $2$。

**答案原文**

复合初等矩阵为 $\begin{pmatrix}0&2&0\\1&0&0\\0&0&1\end{pmatrix}$。

## 245. draft-c28-04

内容 SHA256：`d1edacb594b3c28060afa5721411068e7b9b408329a139c40e00796f7ba1d971`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-05.jsonl；源 SHA256 `6eabbb3d46a7d6a4b39d563a7fc339d117b2be8533dce70e0a85bf2963570f0e`；行 9，JSON pointer `/`。

**题干**

求使向量 $a=(1,2,3)$，$b=(1,1,1)$，$c=(k,0,1)$ 共面的参数 $k$ 的值，并说明其几何意义。

**过程**

三向量共面当且仅当它们张成的平行六面体体积为 $0$,即行列式为零。$\begin{vmatrix}1&2&3\\1&1&1\\k&0&1\end{vmatrix}=1\times(1\times1-1\times0)-2\times(1\times1-1\times k)+3\times(1\times0-1\times k)=1-2(1-k)+3(-k)=1-2+2k-3k=-1-k$。令其为零得 $k=-1$。验证:$k=-1$ 时 $c=(-1,0,1)=a-2b$($(1,2,3)-2(1,1,1)=(-1,0,1)$),故 $c$ 确在 $a,b$ 张成的平面内。几何意义:三向量共面 ⟺ 体积为 $0$ ⟺ 行列式为零(线性相关)。

**答案原文**

$k=-1$;此时 $c=a-2b$,三向量共面,平行六面体体积为 $0$。

## 246. draft-c27-04

内容 SHA256：`d239988ef0ec67ec2b47fdd3010009d43476a278dc2e7335abbd4df03881b236`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft.jsonl；源 SHA256 `e019465093b291bd83fb6ae20f3eefc40a96df3e5137a246ad8813dd03f87b34`；行 4，JSON pointer `/`。

**题干**

求矩阵 $A=\begin{pmatrix}1&k\\0&2\end{pmatrix}$ 的特征值与特征向量，并讨论特征方向随参数 $k$ 的变化。

**过程**

$A$ 为上三角矩阵,特征值为 $1$ 与 $2$。$\lambda=1$:$(A-I)v=0$,即 $\begin{pmatrix}0&k\\0&1\end{pmatrix}v=0$,得 $v_2=0$,特征方向为 $(1,0)$,与 $k$ 无关。$\lambda=2$:$(A-2I)v=0$,即 $\begin{pmatrix}-1&k\\0&0\end{pmatrix}v=0$,得 $-v_1+kv_2=0$,特征方向为 $(k,1)$。讨论:特征值不随 $k$ 改变,但特征值 $2$ 的特征方向随 $k$ 转动($k=0$ 时为 $(0,1)$,即 $y$ 轴方向;$k\neq0$ 时倾斜);特征值 $1$ 的特征方向始终为 $x$ 轴。

**答案原文**

特征值 $1,2$;特征方向:$(1,0)$ 与 $(k,1)$;$\lambda=2$ 的特征方向随 $k$ 转动,$\lambda=1$ 的固定。

## 247. draft-c44-02

内容 SHA256：`d35b3cea38d4c3e1f83cb5e9591103ab6091898770b6294f6ac726df0fb360ad`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft.jsonl；源 SHA256 `b92648645c3b17a796e6b8938f67de934cddafd0cf192ab24ae006e5b423e27f`；行 7，JSON pointer `/`。

**题干**

验证矩阵 $A=\begin{pmatrix}2&0\\0&1\end{pmatrix}$ 不保持 $\mathbb R^2$ 上的辛形式 $\omega(u,v)=u_1v_2-u_2v_1$。

**过程**

取 $u=e_1=(1,0)$,$v=e_2=(0,1)$。$Au=2e_1=(2,0)$,$Av=e_2=(0,1)$。$\omega(Au,Av)=\det\begin{pmatrix}2&0\\0&1\end{pmatrix}=2\times1-0\times0=2$。而 $\omega(u,v)=\det\begin{pmatrix}1&0\\0&1\end{pmatrix}=1$。$2\neq1$,故 $A$ 不保持 $\omega$。(一般地,$\omega(Au,Av)=\det A\cdot\omega(u,v)$,$\det A=2\neq1$,故不保持。)

**答案原文**

不保持:$\omega(Ae_1,Ae_2)=2\neq1=\omega(e_1,e_2)$。

## 248. draft-c36-01

内容 SHA256：`d375d2ac2ce7f4bec1b103327935d87c98cac0af0303c76b404c65ae12d75337`。

来源：reviews/codex-supervision/2026-10-05-math-template-followup-v2/batch01-corrected-review-copy-v2.jsonl；源 SHA256 `d0c82fcc9503c4affd525ea22ba1387722b3e3d13ee215592f42e3824642bf42`；行 6，JSON pointer `/`。

**题干**

判断二次型 $f(x,y)=3x^2-2xy+3y^2$ 是否正定，并用配方法验证你的结论。

**过程**

二次型对应矩阵 $A=\begin{pmatrix}3&-1\\-1&3\end{pmatrix}$。顺序主子式：$\Delta_1=3>0$，$\Delta_2=\det A=3\times 3-(-1)\times(-1)=8>0$，故 $f$ 正定。配方法验证：$f=3x^2-2xy+3y^2=3\left(x-\frac{y}{3}\right)^2+\frac{8}{3}y^2$。对任意 $(x,y)\neq(0,0)$，若 $y\neq 0$ 则 $\frac{8}{3}y^2>0$；若 $y=0$ 则 $x\neq 0$，第一项 $3x^2>0$，故恒有 $f>0$，正定。

**答案原文**

正定；配方 $f=3(x-\frac y3)^2+\frac83y^2$，非零 $(x,y)$ 时严格为正。

## 249. linalg-048

内容 SHA256：`d478cf41832da611530cdc2d8a60024338026e44d123dc0da7e2380e6d0f9018`。

来源：data/v2/train/leakage-isolated-v2-2026-10-05/dataset_linalg.jsonl；源 SHA256 `19a57edceba530c9ee8471c53691104ae291f8b2db38d0b598f93b6cef8b01c4`；行 1，JSON pointer `/`。

**题干**

已知矩阵 $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$，分析它对应的线性变换对二维平面产生的几何影响。

**过程**

该矩阵对应的线性变换将标准基向量 $\vec{e_1} = (1,0)$ 映射为 $(2,1)$，$\vec{e_2} = (0,1)$ 映射为 $(1,2)$。该矩阵为对称矩阵，特征值为 $3$ 和 $1$，对应正交特征方向 $(1,1)$ 与 $(1,-1)$：变换是沿这两个方向的纯拉伸（无剪切），沿 $(1,1)$ 方向拉伸为原来的 3 倍，沿 $(1,-1)$ 方向保持不变。为了具体分析，可以计算其行列式 $\det(A) = 2\times2 - 1\times1 = 3$，说明变换后单位正方形的面积扩大为原来的3倍。

**答案原文**

矩阵将平面沿 (1,1) 方向拉伸，行列式为3

## 250. eval-linalg-021-s1

内容 SHA256：`d69f592b9298ae7f466d8ab6fc9ad823765a561d56963b6c975f89e0a8143da9`。

来源：reviews/codex-supervision/history-from-code/recheck-68c51be/data/v2/eval/dataset_eval.json；源 SHA256 `1de2df62edd0b01403df813c80edc3a5a9dbf1791f0b223d8e0f107ccee55e6e`；行 —，JSON pointer `/255`。

**题干**

判断二次型 $f=x^2+2y^2+3z^2+2xy+2xz+4yz$ 是否正定。

**过程**

矩阵 $A=\begin{pmatrix}1&1&1\\1&2&2\\1&2&3\end{pmatrix}$。顺序主子式：$\Delta_1=1>0$；$\Delta_2=\begin{vmatrix}1&1\\1&2\end{vmatrix}=1>0$；$\Delta_3=\det A=1\cdot(2\cdot 3-2\cdot 2)-1\cdot(1\cdot 3-2\cdot 1)+1\cdot(1\cdot 2-2\cdot 1)=2-1+0=1>0$。全为正，由 Sylvester 判据，$f$ 正定。

**答案原文**

正定

## 251. draft-c27-04

内容 SHA256：`d6ab823f4634a04ea6a62790b88af7fb678175b66a39ad42df1e96e275ed325d`。

来源：reviews/codex-supervision/2026-10-06-scene-batch-completion-review/math-wording-c27-04.candidate.jsonl；源 SHA256 `6040b10eaed21fceac8d5b38c6769e84eca8a1fe6c974ce80e03607ee5c9afec`；行 1，JSON pointer `/`。

**题干**

设$A_k=\begin{pmatrix}1&k\\0&2\end{pmatrix}$，$k\in\mathbb R$。求对角化并判断何时能正交对角化，给两特征线的较小夹角（包含直角情形）精确式。

**过程**

特征值为$1,2$，对应特征向量$e_1=(1,0)$与$(k,1)$。$P=\begin{pmatrix}1&k\\0&1\end{pmatrix}$可逆且$A_kP=P\operatorname{diag}(1,2)$，故所有$k$都可对角化。两特征线夹角$\alpha\in(0,\pi/2]$满足$\cos\alpha=|k|/\sqrt{k^2+1}$，所以仅$k=0$时垂直。实矩阵正交对角化为实对角阵必对称，而$A_k$对称当且仅当$k=0$；故正交对角化也当且仅当$k=0$。

**答案原文**

所有$k$可对角化；正交对角化当且仅当$k=0$；$\alpha=\arccos(|k|/\sqrt{k^2+1})$。

## 252. geom-021

内容 SHA256：`d74998759017da238a96edabef48099f09660038e6f88ee3ac77278f6431e0f2`。

来源：reviews/codex-supervision/2026-10-05-math-template-followup-v2/corrected-candidates/dataset_geom.jsonl；源 SHA256 `0c7b3c0833d3f4d0d43ced4108022af41ceaa78686d85664d45ef2194580e662`；行 1，JSON pointer `/`。

**题干**

求异面直线 $l_1: \frac{x-1}{1} = \frac{y}{-1} = \frac{z+1}{2}$ 与 $l_2: \frac{x}{2} = \frac{y+1}{1} = \frac{z-1}{1}$ 之间的距离。

**过程**

直线 $l_1$ 过点 $P_1(1,0,-1)$，方向向量 $\vec{s_1} = (1,-1,2)$。直线 $l_2$ 过点 $P_2(0,-1,1)$，方向向量 $\vec{s_2} = (2,1,1)$。两直线的公垂线方向向量 $\vec{n} = \vec{s_1} \times \vec{s_2} = \begin{vmatrix} \mathbf{i} & \mathbf{j} & \mathbf{k} \\ 1 & -1 & 2 \\ 2 & 1 & 1 \end{vmatrix} = (-3, 3, 3)$。距离 $d = \frac{|\vec{P_1 P_2} \cdot \vec{n}|}{|\vec{n}|} = \frac{|(-1, -1, 2) \cdot (-3, 3, 3)|}{\sqrt{9+9+9}} = \frac{|3 - 3 + 6|}{3\sqrt{3}} = \frac{6}{3\sqrt{3}} = \frac{2\sqrt{3}}{3}$。

**答案原文**

$\frac{2\sqrt{3}}{3}$

## 253. draft-c45-03

内容 SHA256：`d74ce88956690e2da3677380651af1a56f96018ec71272c1e1ce62a392936a56`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft.jsonl；源 SHA256 `b92648645c3b17a796e6b8938f67de934cddafd0cf192ab24ae006e5b423e27f`；行 13，JSON pointer `/`。

**题干**

抛两枚均匀硬币。记 $A=${第一枚正面},$B=${第二枚正面},$C=${两枚同面}。证明 $A,B,C$ 两两独立但整体不独立。

**过程**

$P(A)=P(B)=P(C)=\frac12$。$P(A\cap B)=P(\text{两枚皆正})=\frac14=P(A)P(B)$ ✓。$P(A\cap C)=P(A\cap\text{两枚同面})=P(\text{两枚皆正})=\frac14=P(A)P(C)$ ✓。$P(B\cap C)=\frac14=P(B)P(C)$ ✓。故两两独立。但 $P(A\cap B\cap C)=P(\text{两枚皆正})=\frac14\neq\frac18=P(A)P(B)P(C)$,故整体不独立。

**答案原文**

两两独立($P(A\cap B)=P(A\cap C)=P(B\cap C)=\frac14$),但 $P(A\cap B\cap C)=\frac14\neq\frac18$,整体不独立。

## 254. draft-c38-03

内容 SHA256：`d7ace77bfdf0a6b451885499d192ccd1e94a7de9afa59397992ff3d227450f14`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/0173d767f1eace928f815df64ba6bbcbda23c1d9e5a66938eb47f76931ca6179.bin；源 SHA256 `0173d767f1eace928f815df64ba6bbcbda23c1d9e5a66938eb47f76931ca6179`；行 8，JSON pointer `/`。

**题干**

在实$2\times2$矩阵空间中，令$U$为对称矩阵、$V$为迹为零的矩阵。给出交空间的基、两空间与和的维数，并显式证明和为全空间。

**过程**

$U$维数$3$，$V$维数$3$。交中矩阵为$\begin{pmatrix}a&b\b&-a\end{pmatrix}$，基为$\operatorname{diag}(1,-1)$与$\begin{pmatrix}0&1\\1&0\end{pmatrix}$，维数$2$。对任意$A$，分解$A=(\operatorname{tr}A/2)I+[A-(\operatorname{tr}A/2)I]$，前项对称、后项无迹，故和为全空间，维数$4$。交非零，所以分解成任意$U,V$成分不唯一，也不是直和。

**答案原文**

$\dim U=\dim V=3$，交维数$2$、基如上，和为四维全空间，非直和。

## 255. draft-c24-03

内容 SHA256：`d8c716f2dda956b8d60126874741da8cc97b2ca11c3b72558798b765bba8000b`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/074e381cf800357f5ad5a9132abc98f301d6704d9c04d7612ec224a66b09b550.bin；源 SHA256 `074e381cf800357f5ad5a9132abc98f301d6704d9c04d7612ec224a66b09b550`；行 3，JSON pointer `/`。

**题干**

设$T_t(x)=A_tx+b$，$A_t=\begin{pmatrix}1&2\t&t^2\end{pmatrix}$，$t\in\mathbb R$。求可逆参数及逆矩阵，并在每个奇异参数下给整个平面像、相容条件与全部纤维。

**过程**

$\det A_t=t(t-2)$，故$t\ne0,2$时可逆，逆为$[t(t-2)]^{-1}\begin{pmatrix}t^2&-2\\-t&1\end{pmatrix}$。记像点为$(u,v)$，$s=u-b_1$。$t=0$时像为$b+\operatorname{span}(1,0)$，条件$v=b_2$；$t=2$时像为$b+\operatorname{span}(1,2)$，条件$v-b_2=2s$。两奇异参数下，满足条件的全部原像都是$(s-2r,r)$，$r\in\mathbb R$；不满足条件则无原像。核方向为$(-2,1)$，两种奇异像方向不同，不能只检查一个退化值。

**答案原文**

可逆$t\notin\{0,2\}$；逆如上；奇异像与全部纤维如上。

## 256. linalg-054

内容 SHA256：`d8eccfddabcbfe87dbee08608a3a324c846fb0407f40d76647b2bedba2d0e889`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/0d6cf147b00b746ff542224346124229b5a6a8e21516106946a9647b8de43f36.bin；源 SHA256 `0d6cf147b00b746ff542224346124229b5a6a8e21516106946a9647b8de43f36`；行 —，JSON pointer `/6`。

**题干**

利用 Cramer 法则求解线性方程组 $\begin{cases} 2x + y = 5 \\ x - y = 1 \end{cases}$，并说明行列式为零时的几何意义。

**过程**

系数行列式 $D=\begin{vmatrix} 2 & 1 \\ 1 & -1 \end{vmatrix}=-3\neq0$，方程组有唯一解。$D_x=\begin{vmatrix} 5 & 1 \\ 1 & -1 \end{vmatrix}=-6$，$D_y=\begin{vmatrix} 2 & 5 \\ 1 & 1 \end{vmatrix}=-3$，故 $x=2, y=1$。若 $D=0$，两直线平行或重合，对应无解或无穷多解。

**答案原文**

$x=2, y=1$

## 257. draft-c13-01

内容 SHA256：`d94144b864f6efcb1711cf792cb73c06c7aa57c38b02119621277bbdd1f2aa1f`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft.jsonl；源 SHA256 `4a8930a557e05b01cec58257879ecd5bd9679b9c08e3e478767c363642ebe382`；行 1，JSON pointer `/`。

**题干**

求级数 $\sum_{n=1}^{\infty}\frac{1}{(2n-1)(2n+1)}$ 的和。

**过程**

部分分式：$\frac{1}{(2n-1)(2n+1)}=\frac12\left(\frac{1}{2n-1}-\frac{1}{2n+1}\right)$。前 $N$ 项和 $S_N=\frac12\sum_{n=1}^{N}\left(\frac{1}{2n-1}-\frac{1}{2n+1}\right)=\frac12\left(1-\frac{1}{2N+1}\right)$(中间项两两抵消)。令 $N\to\infty$ 得 $S=\frac12$。

**答案原文**

和为 $\frac12$。

## 258. draft-c50-02

内容 SHA256：`d9f7f53808afebd14e649ded344e87af955f58105c1bdee8f603a0e7e85b2205`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-18/draft.jsonl；源 SHA256 `6f921b08949f3ee7aaa95ce0363cafaff81b0ab7d0d95f10e1b5a280d697d8d1`；行 2，JSON pointer `/`。

**题干**

掷一颗均匀骰子 $36$ 次，$S$ 为点数之和。用中心极限定理近似求 $P(S>140)$。

**过程**

单次点数 $X$:$\mu=\frac{1+2+3+4+5+6}{6}=\frac72$;$\sigma^2=\frac{1^2+2^2+3^2+4^2+5^2+6^2}{6}-\left(\frac72\right)^2=\frac{91}{6}-\frac{49}{4}=\frac{35}{12}$。故 $ES=36\times\frac72=126$,$Var(S)=36\times\frac{35}{12}=105$。$P(S>140)\approx P\left(Z>\frac{140-126}{\sqrt{105}}\right)=P(Z>1.366)=1-\Phi(1.366)\approx0.086$。

**答案原文**

$P(S>140)\approx0.086$。

## 259. linalg-068

内容 SHA256：`da57924f20ea628636daef748f9105173a9814d831bfd50ca8c1d35fcc13fe93`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/0d6cf147b00b746ff542224346124229b5a6a8e21516106946a9647b8de43f36.bin；源 SHA256 `0d6cf147b00b746ff542224346124229b5a6a8e21516106946a9647b8de43f36`；行 —，JSON pointer `/20`。

**题干**

将实对称矩阵 $A=\begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ 正交对角化。

**过程**

特征值 $\lambda_1=3$ 对应特征向量 $(1,1)^T/\sqrt{2}$，$\lambda_2=1$ 对应 $(1,-1)^T/\sqrt{2}$。两个特征向量正交。正交矩阵 $Q=\frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}$，$Q^TAQ=\operatorname{diag}(3,1)$。

**答案原文**

$Q^TAQ=\operatorname{diag}(3,1)$

## 260. eval-linalg-014-s2

内容 SHA256：`daa5120ba183d08da4cd70c1f4e4984c76a9d336c27bed87f7483a9ea3814514`。

来源：reviews/codex-supervision/history-from-code/recheck-68c51be/data/v2/eval/dataset_eval.json；源 SHA256 `1de2df62edd0b01403df813c80edc3a5a9dbf1791f0b223d8e0f107ccee55e6e`；行 —，JSON pointer `/235`。

**题干**

求矩阵 $A=\begin{pmatrix}0&1\\1&0\end{pmatrix}$ 的特征值与特征向量，并说明其几何意义。

**过程**

$A$ 把 $(x,y)$ 映到 $(y,x)$，正是关于直线 $y=x$ 的镜面反射。反射轴上（$y=x$）的向量不动（特征值 1），垂直于轴的方向（$y=-x$）反向（特征值 $-1$）。

**答案原文**

特征值 $\lambda_1=1$（特征向量 $(1,1)^T$），$\lambda_2=-1$（特征向量 $(1,-1)^T$）；$A$ 是关于直线 $y=x$ 的反射

## 261. draft-c12-02

内容 SHA256：`dc2edce1c11fe69c84b784854c13ce1aede781093b3d7492cd64b1f0f9dcfdfc`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft.jsonl；源 SHA256 `1cc220e2699b799fb9bacc8525e1f9d82321dc39dacd33e5c1caa21c1a7d959b`；行 7，JSON pointer `/`。

**题干**

证明 $\sum_{n=0}^{\infty}x^n$ 在 $[-\frac12,\frac12]$ 上一致收敛，并说明在 $(-1,1)$ 上不一致收敛。

**过程**

在 $[-\frac12,\frac12]$ 上,$|x|^n\le\left(\frac12\right)^n$,而 $\sum\left(\frac12\right)^n$ 收敛,由 $M$ 判别法一致收敛。在 $(-1,1)$ 上,部分和 $S_N(x)=\frac{1-x^{N+1}}{1-x}$,和函数 $S(x)=\frac{1}{1-x}$,尾项 $|S_N(x)-S(x)|=\frac{|x|^{N+1}}{1-x}$。取 $x_N=1-\frac1N\in(-1,1)$:$\frac{x_N^{N+1}}{1-x_N}=N\left(1-\frac1N\right)^{N+1}\to\infty$(因 $\left(1-\frac1N\right)^{N+1}\to e^{-1}$),故 $\sup_{x\in(-1,1)}|S_N-S|$ 不趋于 $0$,不一致收敛。

**答案原文**

在 $[-\frac12,\frac12]$ 上一致收敛($M$ 判别法);在 $(-1,1)$ 上不一致收敛($\sup|S_N-S|$ 不趋于 $0$)。

## 262. draft-c24-03

内容 SHA256：`dd838a1b8f1b38f8ad241f434999e34469d100d5c9a8cd3cb29009c6093fb86f`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft.jsonl；源 SHA256 `25705ed80dbac40074a2bc29ed482de0087b12bc96d3e1ec0cb9f77722fefe0e`；行 3，JSON pointer `/`。

**题干**

求使仿射变换 $T(x)=Ax+b$($A=\begin{pmatrix}1&k\\k&1\end{pmatrix}$)可逆的参数 $k$ 的取值范围；并求 $k=1$ 时整个平面在 $T$ 下的像是什么图形。

**过程**

$T$ 可逆当且仅当 $\det A=1-k^2\neq0$,即 $k\neq\pm1$。当 $k=1$ 时,$A=\begin{pmatrix}1&1\\1&1\end{pmatrix}$,$T(x,y)=(x+y+b_1,\,x+y+b_2)$。令 $c=x+y$,则整个平面的像为 $\{(c+b_1,c+b_2):c\in\mathbb R\}$,即过点 $(b_1,b_2)$、方向为 $(1,1)$ 的直线,方程为 $x'-y'=b_1-b_2$($A$ 的秩为 $1$,把平面压缩到一维;仅当 $b=0$ 或 $b_1=b_2$ 时该直线才是 $y'=x'$)。每条直线 $x+y=c$ 映为点 $(c+b_1,c+b_2)$。

**答案原文**

可逆当且仅当 $k\neq\pm1$;$k=1$ 时整个平面的像是过 $(b_1,b_2)$、方向 $(1,1)$ 的直线 $x'-y'=b_1-b_2$(仅 $b_1=b_2$ 时为 $y'=x'$)。

## 263. draft-c46-04

内容 SHA256：`de05b54ef2647aaf7dbfc9cbee517312c945bb6b79bbc009ca2845e65cd92bc8`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-06/draft.jsonl；源 SHA256 `2685493ba0765d9a8d1f8a1be3e55595e83614f9d6861bc1b87c95e2d4aad8df`；行 14，JSON pointer `/`。

**题干**

判断如下取点法是否在单位圆盘 $x^2+y^2\le1$ 内均匀分布:取独立随机变量 $U,V\sim U(0,1)$,令 $R=U$,$\Theta=2\pi V$,取点 $(R\cos\Theta,R\sin\Theta)$。若不均匀,说明原因并给出修正。

**过程**

不均匀。此时 $R$ 在 $[0,1]$ 上均匀,$P(R\le r)=r$,而圆盘内半径为 $r$ 的圆面积占总面积的比例为 $r^2$。例如 $P(R\le\frac12)=\frac12$,但半径为 $\frac12$ 的圆只占总面积的 $\frac14$——点过多地集中在圆心附近(径向密度 $f_R(r)=1$,面积密度 $\propto\frac1r$)。修正:取 $R=\sqrt{U}$。此时 $P(R\le r)=P(\sqrt U\le r)=P(U\le r^2)=r^2$,恰为面积比例,故 $(R\cos\Theta,R\sin\Theta)$ 在圆盘内均匀分布。

**答案原文**

不均匀(径向密度 $f_R(r)=1$ 导致中心过密,$P(R\le\frac12)=\frac12\neq\frac14$);修正:取 $R=\sqrt U$。

## 264. draft-c14-02

内容 SHA256：`dec4ff859d8e9661de5839d97c7f4ab49d48dca8a52224d0ec7238a893b6ca8c`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft.jsonl；源 SHA256 `1cc220e2699b799fb9bacc8525e1f9d82321dc39dacd33e5c1caa21c1a7d959b`；行 12，JSON pointer `/`。

**题干**

将 $f(x)=x$($0\le x\le\pi$)展开为正弦级数(作奇延拓)。

**过程**

作奇延拓后在 $[-\pi,\pi]$ 上 $f$ 为奇函数,故 $a_n=0$。$b_n=\frac2\pi\int_0^{\pi}x\sin nx\,dx$。分部积分:$\int_0^{\pi}x\sin nx\,dx=\left.-\frac{x\cos nx}{n}\right|_0^{\pi}+\frac1n\int_0^{\pi}\cos nx\,dx=-\frac{\pi\cos n\pi}{n}+0=\frac{\pi(-1)^{n+1}}{n}$。故 $b_n=\frac{2(-1)^{n+1}}{n}$。正弦展开:$x=\sum_{n=1}^{\infty}\frac{2(-1)^{n+1}}{n}\sin nx$($0<x<\pi$;在端点 $x=0,\pi$ 处级数和为 $0$)。

**答案原文**

$x=\sum_{n=1}^{\infty}\frac{2(-1)^{n+1}}{n}\sin nx$($0<x<\pi$)。

## 265. draft-c27-01

内容 SHA256：`df3eb60d53b5846cca2b73ba2a3542c2f815ecb2e33b18c564e24ec35b978b6a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft.jsonl；源 SHA256 `e019465093b291bd83fb6ae20f3eefc40a96df3e5137a246ad8813dd03f87b34`；行 1，JSON pointer `/`。

**题干**

判断矩阵 $A=\begin{pmatrix}2&1&0\\0&2&1\\0&0&3\end{pmatrix}$ 是否可对角化，并说明理由。

**过程**

$A$ 为上三角矩阵,特征值为对角线元素:$2,2,3$(特征多项式 $(2-\lambda)^2(3-\lambda)$)。特征值 $2$ 的代数重数为 $2$,求其几何重数:解 $(A-2I)v=0$,即 $\begin{pmatrix}0&1&0\\0&0&1\\0&0&1\end{pmatrix}v=0$,得 $v_2=0,v_3=0$,特征子空间为 $\mathrm{span}\{(1,0,0)\}$,维数为 $1$。几何重数 $1<$ 代数重数 $2$,故 $A$ 不可对角化。

**答案原文**

不可对角化:特征值 $2$ 的几何重数 $1$ 小于代数重数 $2$。

## 266. draft-c33-03

内容 SHA256：`e0da4df58a4a45eac7547b392602ddf7821461f40d8739dd663037a20667e42e`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-02.jsonl；源 SHA256 `286625ebf0f88cca49b14f36be4bab4e5f3b29ecc0764226b7ebb5fb61a16527`；行 8，JSON pointer `/`。

**题干**

用分块方法求矩阵 $M=\begin{pmatrix}2&1&1\\1&1&0\\0&0&2\end{pmatrix}$ 的逆矩阵。

**过程**

将 $M$ 分块为 $\begin{pmatrix}A&b\\0&d\end{pmatrix}$，其中 $A=\begin{pmatrix}2&1\\1&1\end{pmatrix}$，$b=\begin{pmatrix}1\\0\end{pmatrix}$，$d=2$。$A$ 可逆且 $A^{-1}=\begin{pmatrix}1&-1\\-1&2\end{pmatrix}$。由分块上三角矩阵求逆公式，$M^{-1}=\begin{pmatrix}A^{-1}&-\frac{1}{d}A^{-1}b\\0&\frac{1}{d}\end{pmatrix}$。计算 $A^{-1}b=\begin{pmatrix}1\\-1\end{pmatrix}$，故 $-\frac12A^{-1}b=\begin{pmatrix}-\frac12\\\frac12\end{pmatrix}$。于是 $M^{-1}=\begin{pmatrix}1&-1&-\frac12\\-1&2&\frac12\\0&0&\frac12\end{pmatrix}$。验证:$MM^{-1}=I$(逐行相乘核对)。

**答案原文**

$M^{-1}=\begin{pmatrix}1&-1&-\frac12\\-1&2&\frac12\\0&0&\frac12\end{pmatrix}$。

## 267. draft-c52-03

内容 SHA256：`e103681bcb795b15d82e0af052e221289582ea5ed7ba527d171e0cb0438d1e35`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft-v2.jsonl；源 SHA256 `592604adc88816bf3bc8b9313e3b8a0dd31c2fa5d5be9bb211e057196909e596`；行 13，JSON pointer `/`。

**题干**

设随机变量 $X$ 服从区间 $(-1,2)$ 上的均匀分布，求 $Y=X^2$ 的概率密度函数，并指出密度分段的分界点。

**过程**

$X$ 的密度为 $\frac{1}{3}$($-1<x<2$)。$Y=X^2$ 的值域为 $[0,4)$。当 $0<y<1$ 时，$[-\sqrt{y},\sqrt{y}]\subset(-1,2)$，故 $F_Y(y)=P(X^2\leq y)=\frac{2\sqrt{y}}{3}$，$f_Y(y)=\frac{1}{3\sqrt{y}}$。当 $1\leq y<4$ 时，区间 $[-\sqrt{y},\sqrt{y}]$ 与支持集 $(-1,2)$ 的交为 $(-1,\sqrt{y}]$，故 $F_Y(y)=\frac{\sqrt{y}+1}{3}$，$f_Y(y)=\frac{1}{6\sqrt{y}}$。分界点为 $y=1$，两侧密度在该点有跳跃。验证总质量：$\int_0^1\frac{1}{3\sqrt{y}}\,dy+\int_1^4\frac{1}{6\sqrt{y}}\,dy=\frac{2}{3}+\frac{1}{3}=1$。完整 CDF 在 $y\leq0$ 时为 $0$，在 $y\geq4$ 时为 $1$；$y=1$ 处 CDF 连续但左右导数不同；密度在单个点 $y=1$ 可任取有限非负值，这不产生概率原子。

**答案原文**

$f_Y(y)=\frac{1}{3\sqrt{y}}$(当 $0<y<1$)；$f_Y(y)=\frac{1}{6\sqrt{y}}$(当 $1\leq y<4$)；其余为 $0$。分界点 $y=1$。

## 268. draft-c02-02

内容 SHA256：`e1fd713c30806c44666bec56858fe9887943ec59b1419d437a1679dedba13b83`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-07.jsonl；源 SHA256 `b14a41ee891c643ede8cbc2986187adaa63a4bce93c398f0cce2544a7bc123a5`；行 2，JSON pointer `/`。

**题干**

判断反常积分 $\int_1^{+\infty}\frac{1}{\sqrt{x}}\,dx$ 的敛散性，并说明理由。

**过程**

$\int_1^R\frac{1}{\sqrt x}\,dx=\left.2\sqrt x\right|_1^R=2\sqrt R-2$。当 $R\to+\infty$ 时,$2\sqrt R-2\to+\infty$,故积分发散。理由:这是 $p=\frac12$ 的 $p$ 积分,而 $p$ 积分 $\int_1^{+\infty}\frac1{x^p}\,dx$ 当且仅当 $p>1$ 时收敛;此处 $p=\frac12\le1$,发散。

**答案原文**

发散($p=\frac12\le1$)。

## 269. draft-c36-01

内容 SHA256：`e675e7bc645a94c7e1b8a99a0ccc98cd231913ab364c8095cbeaee66109ebf9a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft.jsonl；源 SHA256 `13fe6a370d3c46ae8ca6c1b16c9cd98fbedcc8648087f11a70ff046951db5479`；行 6，JSON pointer `/`。

**题干**

判断二次型 $f(x,y)=3x^2-2xy+3y^2$ 是否正定，并用配方法验证你的结论。

**过程**

二次型对应矩阵 $A=\begin{pmatrix}3&-1\\-1&3\end{pmatrix}$。顺序主子式：$\Delta_1=3>0$，$\Delta_2=\det A=3\times 3-(-1)\times(-1)=8>0$，故 $f$ 正定。配方法验证：$f=3x^2-2xy+3y^2=3\left(x-\frac{y}{3}\right)^2+\frac{8}{3}y^2$。对任意 $(x,y)\neq(0,0)$，若 $y\neq 0$ 则 $\frac{8}{3}y^2>0$；若 $y=0$ 则 $x\neq 0$，第一项 $3x^2>0$，故恒有 $f>0$，正定。

**答案原文**

正定。

## 270. linalg-059

内容 SHA256：`e7dbbef65c590eaeb5ad3e5809a364f2eb64ac89d952bbd897b494cd10d2f3ff`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/0d6cf147b00b746ff542224346124229b5a6a8e21516106946a9647b8de43f36.bin；源 SHA256 `0d6cf147b00b746ff542224346124229b5a6a8e21516106946a9647b8de43f36`；行 —，JSON pointer `/11`。

**题干**

将二次型 $f(x,y)=2x^2+2xy+2y^2$ 化为标准形，并确定其正负惯性指数。

**过程**

配方得 $f=2(x+\frac{y}{2})^2+\frac{3}{2}y^2$。令 $u=x+\frac{y}{2}, v=y$，标准形为 $2u^2+\frac{3}{2}v^2$。两个系数均为正，正惯性指数为 2，负惯性指数为 0，二次型正定。

**答案原文**

标准形 $2u^2+\frac{3}{2}v^2$。正惯性指数为 2，负惯性指数为 0

## 271. draft-c49-03

内容 SHA256：`e9efeb1197cdb6e1fb3548989c451c6bd17e5d15aa9e09ec0e926f27dbcea579`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft.jsonl；源 SHA256 `bcd6ec3d0204b822f83440669662afcfe3ec7712fa4806d51506f98cb797b0c2`；行 13，JSON pointer `/`。

**题干**

设 $X_1,\dots,X_{100}$ 独立同分布于 $U(0,1)$。用切比雪夫不等式估计 $P(|\bar X-\frac12|>0.1)$ 的上界。

**过程**

$E\bar X=\frac12$。$Var(X_1)=\frac{1}{12}$,$Var(\bar X)=\frac{1/12}{100}=\frac{1}{1200}$。切比雪夫:$P(|\bar X-\frac12|>0.1)\le\frac{Var(\bar X)}{0.1^2}=\frac{1/1200}{1/100}=\frac{1}{12}$。

**答案原文**

上界为 $\frac{1}{12}\approx0.083$。

## 272. draft-c22-01

内容 SHA256：`e9f615b319a585df78a2fcce722d8daf4459e8d986e65110842fd69b81bf4059`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft.jsonl；源 SHA256 `e0eb9bf14b1cdf0919006ede0e9523046d0edadffb69ac3a10e4941a77563756`；行 6，JSON pointer `/`。

**题干**

验证单叶双曲面 $x^2+y^2-z^2=1$ 是直纹面，并写出其两族直母线。

**过程**

由 $(x+z)(x-z)=(1+y)(1-y)$ 可得两族直线。第一族:$\begin{cases}x+z=\lambda(1+y)\\ \lambda(x-z)=1-y\end{cases}$($\lambda$ 取扩充实数,含 $\lambda=\infty$ 对应的极限直线 $y=-1,x=z$);第二族:$\begin{cases}x+z=\mu(1-y)\\ \mu(x-z)=1+y\end{cases}$($\mu$ 取扩充实数,含 $\mu=\infty$ 对应的极限直线 $y=1,x=z$)。验证第一族:直线上任一点满足 $(x+z)(x-z)=\lambda(1+y)\cdot\frac{1-y}{\lambda}=1-y^2$,即 $x^2-z^2=1-y^2$,故 $x^2+y^2-z^2=1$,整条直线在曲面上。第二族同理。补充极限直线后,曲面上每一点恰有每族各一条母线经过。

**答案原文**

两族母线:$\begin{cases}x+z=\lambda(1+y)\\ \lambda(x-z)=1-y\end{cases}$ 与 $\begin{cases}x+z=\mu(1-y)\\ \mu(x-z)=1+y\end{cases}$($\lambda,\mu$ 取扩充实数,含 $\infty$ 对应极限直线 $y=\mp1,x=z$);单叶双曲面是直纹面。

## 273. draft-c12-04

内容 SHA256：`eada15beafbad345bf30c6c27be7c84881a90f0d00c8cbc361517cd64f720ece`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft.jsonl；源 SHA256 `1cc220e2699b799fb9bacc8525e1f9d82321dc39dacd33e5c1caa21c1a7d959b`；行 9，JSON pointer `/`。

**题干**

设 $0<r<1$。利用 $\sum_{n=0}^{\infty}x^n$ 在 $[0,r]$ 上的一致收敛性,将 $\int_0^r\frac{1}{1-x}\,dx$ 展开为级数并验证。

**过程**

在 $[0,r]$ 上 $\sum x^n$ 一致收敛,故可逐项积分:$\int_0^r\frac{1}{1-x}\,dx=\int_0^r\sum_{n=0}^{\infty}x^n\,dx=\sum_{n=0}^{\infty}\int_0^rx^n\,dx=\sum_{n=0}^{\infty}\frac{r^{n+1}}{n+1}$。直接积分验证:$-\ln(1-r)$ 的级数展开为 $\sum_{n=0}^{\infty}\frac{r^{n+1}}{n+1}$($\ln(1-u)=-u-\frac{u^2}{2}-\frac{u^3}{3}-\cdots$,即 $-\ln(1-r)=r+\frac{r^2}{2}+\frac{r^3}{3}+\cdots$),两者一致。

**答案原文**

$\int_0^r\frac{1}{1-x}dx=\sum_{n=0}^{\infty}\frac{r^{n+1}}{n+1}=-\ln(1-r)$。

## 274. draft-c36-01

内容 SHA256：`eb33b7fc001af15e5023c859cea11febec2e4253288cbbca8ff8cfa571f8dcbf`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft-v2.jsonl；源 SHA256 `592604adc88816bf3bc8b9313e3b8a0dd31c2fa5d5be9bb211e057196909e596`；行 6，JSON pointer `/`。

**题干**

设 $A$ 为 $n$ 阶正定矩阵。证明 $A^{-1}$ 也是正定矩阵；并举出两个正定矩阵，其乘积不是正定矩阵的例子。

**过程**

由 $A$ 正定知 $A$ 为实对称矩阵且对任意非零向量 $x$ 有 $x^{\mathsf{T}}Ax>0$；其顺序主子式全正，故 $\det A>0$，$A$ 可逆。对任意 $x\neq 0$，令 $y=A^{-1}x$，则 $y\neq 0$，且 $x^{\mathsf{T}}A^{-1}x=(Ay)^{\mathsf{T}}A^{-1}(Ay)=y^{\mathsf{T}}A^{\mathsf{T}}A^{-1}Ay$。因 $A^{\mathsf{T}}=A$ 且 $A^{-1}A=I$，得 $x^{\mathsf{T}}A^{-1}x=y^{\mathsf{T}}Ay>0$。又 $(A^{-1})^{\mathsf{T}}=(A^{\mathsf{T}})^{-1}=A^{-1}$，故 $A^{-1}$ 也是实对称矩阵。于是 $A^{-1}$ 正定。反例：取 $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$(特征值为 $1$ 与 $3$，正定)与 $B=\begin{pmatrix}1&0\\0&3\end{pmatrix}$(特征值为 $1$ 与 $3$，正定)，则 $AB=\begin{pmatrix}2&3\\1&6\end{pmatrix}$ 不是对称矩阵，故不可能正定(正定矩阵必须对称)。

**答案原文**

证明见解法；反例：$A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$ 与 $B=\begin{pmatrix}1&0\\0&3\end{pmatrix}$ 均正定，而 $AB=\begin{pmatrix}2&3\\1&6\end{pmatrix}$ 不对称，不是正定矩阵。

## 275. calc-series-016

内容 SHA256：`ebcbb4b661e8f809a92fd741d23e53601b1fceffc1f621cf598ad2c35c500fe5`。

来源：reviews/codex-supervision/2026-10-05-math-template-followup-v2/corrected-candidates/dataset_calc.jsonl；源 SHA256 `ca43b838d7309352ba84965c7de3ba071fab450a3c50483e61b5fda0bb9b8180`；行 1，JSON pointer `/`。

**题干**

求幂级数 $\sum_{n=1}^{\infty} \frac{x^n}{n \cdot 2^n}$ 的收敛域及和函数。

**过程**

收敛半径 $R = \lim_{n \to \infty} \left| \frac{a_n}{a_{n+1}} \right| = \lim_{n \to \infty} \frac{(n+1)2^{n+1}}{n2^n} = 2$。当 $x=2$ 时，级数为调和级数 $\sum \frac{1}{n}$，发散；当 $x=-2$ 时，级数为交错级数 $\sum \frac{(-1)^n}{n}$，收敛。故收敛域为 $[-2, 2)$。设和函数 $S(x) = \sum_{n=1}^{\infty} \frac{x^n}{n2^n}$，逐项求导得 $S'(x) = \sum_{n=1}^{\infty} \frac{x^{n-1}}{2^n} = \frac{1}{2} \cdot \frac{1}{1-x/2} = \frac{1}{2-x}$。两边从0到x积分得 $S(x) = \int_0^x \frac{1}{2-t} dt = -\ln(2-x) + \ln 2 = -\ln(1 - x/2)$。上述逐项求导与积分在 $|x|<2$ 内成立；已知 $x=-2$ 处交错级数收敛，由Abel定理，其和等于内侧极限 $-\ln2$，因此和函数公式延伸至 $[-2,2)$。

**答案原文**

收敛域 $[-2, 2)$，和函数 $S(x) = -\ln(1 - x/2)$

## 276. draft-c38-03

内容 SHA256：`eca4fed87560022b54efb497d98af7d81e4515ad1355b543eed4277964c77432`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft.jsonl；源 SHA256 `2a488597e92f7efdb6ec80074b147c9290e949fbeb4cbd114e293657e7c04776`；行 8，JSON pointer `/`。

**题干**

设 $U=\mathrm{span}\{(1,2,3),(0,1,1)\}$，$V=\mathrm{span}\{(1,0,1),(0,1,0),(1,1,1)\}$。求 $\dim U$、$\dim V$、$\dim(U\cap V)$ 与 $\dim(U+V)$。

**过程**

$\dim U=2$($(1,2,3)$ 与 $(0,1,1)$ 线性无关)。$V$ 的生成元中 $(1,1,1)=(1,0,1)+(0,1,0)$,故 $V=\mathrm{span}\{(1,0,1),(0,1,0)\}=\{(p,q,p)\}$,$\dim V=2$。求 $U\cap V$:设 $v\in U$,$v=a(1,2,3)+b(0,1,1)=(a,2a+b,3a+b)$。$v\in V$ 当且仅当第一分量等于第三分量:$a=3a+b$,即 $2a+b=0$,$b=-2a$。此时 $v=(a,0,a)=a(1,0,1)$。故 $U\cap V=\mathrm{span}\{(1,0,1)\}$,$\dim(U\cap V)=1$。验证:$(1,0,1)=1\cdot(1,2,3)+(-2)\cdot(0,1,1)\in U$ ✓。维数公式:$\dim(U+V)=2+2-1=3$。

**答案原文**

$\dim U=2$,$\dim V=2$,$\dim(U\cap V)=1$($U\cap V=\mathrm{span}\{(1,0,1)\}$),$\dim(U+V)=3$。

## 277. draft-c08-01

内容 SHA256：`ed52a91d62b65722372cd3ccb5a0720e5874674f2d29bc4e4b9dc574dc0b9b34`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft.jsonl；源 SHA256 `1d0950f73fad698178bef910eec1c19d5303cfe6bdabbcd76bddab903f05e44b`；行 6，JSON pointer `/`。

**题干**

用参数方程求椭圆 $\begin{cases}x=a\cos t\\ y=b\sin t\end{cases}$($a,b>0$,$0\le t\le2\pi$)围成的面积。

**过程**

面积公式 $A=\left|\int_0^{2\pi}y\,x'\,dt\right|$。$x'=-a\sin t$,故 $\int_0^{2\pi}y\,x'\,dt=\int_0^{2\pi}(b\sin t)(-a\sin t)\,dt=-ab\int_0^{2\pi}\sin^2t\,dt=-ab\cdot\pi=-\pi ab$。取绝对值得 $A=\pi ab$。

**答案原文**

面积为 $\pi ab$。

## 278. draft-c52-05

内容 SHA256：`ed7048d58e89ac8353aeb285096dd1d1e3b70b79e263c54cced8b72ecdf5d9a7`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/7f56fc0aa137fd338e9959c7596a196f88e797be991499195a4ed3dc4b55badf.bin；源 SHA256 `7f56fc0aa137fd338e9959c7596a196f88e797be991499195a4ed3dc4b55badf`；行 15，JSON pointer `/`。

**题干**

设随机变量 $X$ 的分布函数 $F$ 连续，在某区间 $I$ 上严格递增，且 $P(X\in I)=1$、$F(I)=(0,1)$。证明 $Y=F(X)\sim U(0,1)$。再设目标随机变量 $Z$ 的密度为 $g(z)=\begin{cases}\frac12,&0<z<1\\ z-1,&1<z<2\\0,&\text{otherwise}\end{cases}$。给定 $U\sim U(0,1)$，构造 $Z=T(U)$，写出完整分布函数并验证其分布；说明为何 $T$ 必须分段。

**过程**

对 $0<y<1$，由假设，$F$ 在 $I$ 上存在反函数 $F_I^{-1}$。除零概率事件外，$F(X)\le y$ 等价于 $X\le F_I^{-1}(y)$，所以 $P(Y\le y)=F(F_I^{-1}(y))=y$；$y\le0$ 时概率为 $0$，$y\ge1$ 时为 $1$，故 $Y\sim U(0,1)$。目标密度非负，且 $\int_0^1\frac12\,dz+\int_1^2(z-1)\,dz=\frac12+\frac12=1$。积分得 $G(z)=\begin{cases}0,&z\le0\frac z2,&0<z\le1\frac12+\frac{(z-1)^2}{2},&1<z<2\\1,&z\ge2\end{cases}$，在 $z=1$ 连续，$G(1)=\frac12$。两段 CDF 的反函数分别为 $T(u)=2u$（$0<u\le\frac12$）与 $T(u)=1+\sqrt{2u-1}$（$\frac12<u<1$）。令 $Z=T(U)$。若 $0<z\le1$，事件 $T(U)\le z$ 等价于 $U\le z/2$，概率为 $z/2$；若 $1<z<2$，等价于 $U\le\frac12+\frac{(z-1)^2}{2}$，概率为该阈值。外侧概率分别为 $0$ 和 $1$，所以构造确有 CDF $G$。密度在单点 $z=1$ 的取值不影响分布；此处 CDF 无跳跃、没有原子。逆映射在 $u=\frac12$ 处分段，因为目标 CDF 的两段表达式不同，不能以一个线性或幂函数代替全部分支。

**答案原文**

$Y\sim U(0,1)$；$Z=T(U)$，其中 $T(u)=\begin{cases}2u,&0<u\le\frac12\\1+\sqrt{2u-1},&\frac12<u<1\end{cases}$。完整 CDF：$G(z)=0$（$z\le0$）、$z/2$（$0<z\le1$）、$\frac12+\frac{(z-1)^2}{2}$（$1<z<2$）、$1$（$z\ge2$）。

## 279. prob-044

内容 SHA256：`ed71bab1ea5c1e367d26bf8b497b56c173526178796e0dedf382a8eaeb3f99c6`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/0b25e054de83f8b330855e402cec271d3ef98ba02f4f5998b0711d2cf2aa9222.bin；源 SHA256 `0b25e054de83f8b330855e402cec271d3ef98ba02f4f5998b0711d2cf2aa9222`；行 7，JSON pointer `/`。

**题干**

某种疾病的患病率为 0.1%（即千分之一）。有一种检测方法，对于患病者检测出阳性的概率为 99%，对于未患病者检测出阴性的概率为 99%，相应地假阳性率为 1%。若某人检测结果为阳性，求他实际患病的概率。

**过程**

设事件 D 表示患病，T 表示检测为阳性。已知 $P(D) = 0.001, P(\neg D) = 0.999$。灵敏度 $P(T|D) = 0.99$，假阳性率 $P(T|\neg D) = 0.01$。根据贝叶斯公式：$P(D|T) = \frac{P(T|D)P(D)}{P(T|D)P(D) + P(T|\neg D)P(\neg D)} = \frac{0.99 \times 0.001}{0.99 \times 0.001 + 0.01 \times 0.999} = \frac{0.00099}{0.00099 + 0.00999} \approx 0.0902$。即虽然检测为阳性，实际患病的概率仅约 9.02%。

**答案原文**

约 9.02%

## 280. draft-c11-03

内容 SHA256：`ee1319e3070f4979a83f574f969eaf2e467fc96b04439862b35e3280cb9428d3`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft.jsonl；源 SHA256 `71d46f404c59db6194494bf8ea2353202b77f602a15522f58c1b4599d1cbb07a`；行 3，JSON pointer `/`。

**题干**

求幂级数 $\sum_{n=1}^{\infty}\frac{x^n}{n(n+1)}$ 的收敛域与和函数，并求 $S(0)$、$S(1)$、$S(-1)$。

**过程**

收敛域：$|x|<1$ 时由比值法收敛；$x=\pm1$ 时 $\left|\frac{(\pm1)^n}{n(n+1)}\right|\leq\frac{1}{n(n+1)}$ 且 $\sum\frac{1}{n(n+1)}$ 收敛，故两端点绝对收敛，收敛域为 $[-1,1]$。求和(先对 $|x|<1$)：拆项 $\frac{1}{n(n+1)}=\frac{1}{n}-\frac{1}{n+1}$，记 $A(x)=\sum_{n=1}^{\infty}\frac{x^n}{n}=-\ln(1-x)$，则 $\sum_{n=1}^{\infty}\frac{x^n}{n+1}=\frac{1}{x}\sum_{n=1}^{\infty}\frac{x^{n+1}}{n+1}=\frac{A(x)-x}{x}$($x\neq0$)。故 $S(x)=A(x)-\frac{A(x)-x}{x}=1+\frac{(1-x)\ln(1-x)}{x}$。$S(0)=0$(通项为 0)；$S(1)=\sum\frac{1}{n(n+1)}=1$(裂项求和),与公式在 $x\to1^-$ 的极限一致;$S(-1)=\sum\frac{(-1)^n}{n(n+1)}=1-2\ln2$(由公式 $1+\frac{2\ln2}{-1}$)。

**答案原文**

收敛域 $[-1,1]$；$S(x)=1+\frac{(1-x)\ln(1-x)}{x}$($x\neq0$)，$S(0)=0$，$S(1)=1$，$S(-1)=1-2\ln2$。

## 281. syn-train-001

内容 SHA256：`ef5cc8478782bba9c215b9a9f61417363383e708426faf0ba20b56a0e8236ea8`。

来源：reviews/codex-supervision/history-from-code/pytest-68c51be/test_reference_file_ids_must_b0/train/b.jsonl；源 SHA256 `78294e841a7fb8cd0dcbc66ee99e94439be6b1de570a240ceb23a73cc461ae71`；行 1，JSON pointer `/`。

**题干**

Synthetic calculus reference task: differentiate a cubic monomial.

**过程**

1+1=2。

**答案原文**

2

## 282. draft-c53-05

内容 SHA256：`f030d2f130f5edd33257c0994e9bb59585d7010f37156c6af5f4ccfdeef5a76a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-18/draft.jsonl；源 SHA256 `6f921b08949f3ee7aaa95ce0363cafaff81b0ab7d0d95f10e1b5a280d697d8d1`；行 10，JSON pointer `/`。

**题干**

证明:在有限可加性的前提下,可列可加性等价于下连续性(即对 $A_1\subseteq A_2\subseteq\cdots$,$P(\bigcup_nA_n)=\lim_nP(A_n)$)。

**过程**

(可列可加⟹下连续)设 $A_n\uparrow A=\bigcup_nA_n$。令 $B_1=A_1$,$B_n=A_n\setminus A_{n-1}$($n\ge2$),则 $B_n$ 两两互斥且 $A=\bigcup_nB_n$,$A_n=\bigcup_{i\le n}B_i$。由可列可加性,$P(A)=\sum_nP(B_n)=\lim_n\sum_{i\le n}P(B_i)=\lim_nP(A_n)$(最后一步用有限可加性)。(下连续⟹可列可加)设 $A_1,A_2,\dots$ 两两互斥,$A=\bigcup_nA_n$。令 $C_n=\bigcup_{i\le n}A_i$,则 $C_n\uparrow A$。由下连续性与有限可加性,$P(A)=\lim_nP(C_n)=\lim_n\sum_{i\le n}P(A_i)=\sum_nP(A_n)$。故在有限可加性下两者等价。

**答案原文**

证明见解法(可列可加⟹下连续:互斥拆分 $B_n=A_n\setminus A_{n-1}$;下连续⟹可列可加:部分并 $C_n\uparrow A$)。

## 283. draft-c47-04

内容 SHA256：`f1eca30871e47acb87bba4ea8707b28c741f237cb8f4451e383a486db5f50265`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft.jsonl；源 SHA256 `bcd6ec3d0204b822f83440669662afcfe3ec7712fa4806d51506f98cb797b0c2`；行 4，JSON pointer `/`。

**题干**

设 $X\sim B(100,\frac12)$。说明为什么不能用泊松分布近似 $X$，并用 $P(X=50)$ 的精确值与泊松近似值对比说明。

**过程**

泊松近似要求 $n$ 大、$p$ 小(稀有事件)且 $\lambda=np$ 适中;此处 $p=\frac12$ 不满足「$p$ 小」,$\lambda=50$ 过大,泊松近似失效。数值对比:精确值 $P(X=50)=\binom{100}{50}(\frac12)^{100}\approx0.0796$(直接计算 $\binom{100}{50}=100891344545564193334812497256$,除以 $2^{100}$ 得 $0.07959$);泊松近似值 $e^{-50}\frac{50^{50}}{50!}\approx0.0563$。两者相差约 $0.023$,相对误差约 $30\%$,近似不可接受。

**答案原文**

不适用:$p=\frac12$ 不小、$\lambda=50$ 过大;精确值 $\approx0.0796$ 与泊松近似 $\approx0.0563$ 相对误差约 $30\%$。

## 284. draft-c10-02

内容 SHA256：`f265e50359439859ac06885fee266b453fd7296527358abbd7763ea13beff5e9`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft.jsonl；源 SHA256 `1cc220e2699b799fb9bacc8525e1f9d82321dc39dacd33e5c1caa21c1a7d959b`；行 2，JSON pointer `/`。

**题干**

判断级数 $\sum_{n=1}^{\infty}\frac{(-1)^n n}{n^2+1}$ 的敛散性，并指出是绝对收敛还是条件收敛。

**过程**

绝对收敛性:$\frac{n}{n^2+1}\ge\frac{n}{2n^2}=\frac{1}{2n}$($n\ge1$ 时 $n^2+1\le2n^2$),而 $\sum\frac{1}{2n}$ 发散,故 $\sum\frac{n}{n^2+1}$ 发散,非绝对收敛。条件收敛性:令 $f(x)=\frac{x}{x^2+1}$,$f'(x)=\frac{1-x^2}{(x^2+1)^2}<0$($x>1$),故 $a_n=\frac{n}{n^2+1}$ 单调递减;又 $\lim_{n\to\infty}\frac{n}{n^2+1}=0$。由莱布尼茨判别法,$\sum\frac{(-1)^n n}{n^2+1}$ 收敛,故为条件收敛。

**答案原文**

条件收敛(绝对值级数发散,交错级数本身收敛)。

## 285. linalg-061

内容 SHA256：`f331704b3a1e82fc6ced2263d7da218765833e1bbd6e90dd731d2956398729b2`。

来源：reviews/codex-supervision/2026-10-05-math-template-followup-v2/corrected-candidates/dataset_linalg.jsonl；源 SHA256 `ba1e7680351b93504c1d8fe5518004b9107545a78761750d9d9933e8fd16ab45`；行 7，JSON pointer `/`。

**题干**

在 $\mathbb{R}^2$ 中，已知旧基 $\varepsilon_1=(1,0), \varepsilon_2=(0,1)$，新基 $\eta_1=(1,1), \eta_2=(-1,1)$。求从旧基到新基的过渡矩阵，并求向量 $\alpha=(3,1)$ 在新基下的坐标。约定基过渡矩阵 $P$ 满足 $(\eta_1,\eta_2)=(\varepsilon_1,\varepsilon_2)P$，并同时写出旧坐标到新坐标的变换矩阵。

**过程**

按题中约定，新基向量在旧基下的坐标作为列，故 $P=\begin{pmatrix}1&-1\\1&1\end{pmatrix}$，$[\alpha]_\varepsilon=P[\alpha]_\eta$。旧坐标到新坐标的矩阵是 $P^{-1}=\frac12\begin{pmatrix}1&1\\-1&1\end{pmatrix}$。因此 $[\alpha]_\eta=P^{-1}\begin{pmatrix}3\\1\end{pmatrix}=\begin{pmatrix}2\\-1\end{pmatrix}$；检验 $2\eta_1-\eta_2=(3,1)$。

**答案原文**

基过渡矩阵 $P=\begin{pmatrix}1&-1\\1&1\end{pmatrix}$；旧坐标到新坐标矩阵 $P^{-1}=\frac12\begin{pmatrix}1&1\\-1&1\end{pmatrix}$；新坐标 $(2,-1)^T$。

## 286. draft-c01-02

内容 SHA256：`f488252e5f1ea3d29f9d04c1d319b4418671965446f910b2c85183e45ac1bfda`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft-v2.jsonl；源 SHA256 `592604adc88816bf3bc8b9313e3b8a0dd31c2fa5d5be9bb211e057196909e596`；行 2，JSON pointer `/`。

**题干**

设 $f(x)=\begin{cases}x^2+a, & x\leq 1\\ bx+1, & x>1\end{cases}$，其中 $a,b$ 为常数。求使 $f$ 在 $x=1$ 处连续的条件；在连续前提下，求使 $f$ 在 $x=1$ 处可微(即曲线在该点处有切线)的条件，并写出此时的切线方程；再给出一组参数，使 $f$ 在 $x=1$ 处连续但不可微，并说明曲线在该点处的几何特征。

**过程**

连续性：左极限 $\lim_{x\to1^-}f(x)=1+a$，右极限 $\lim_{x\to1^+}f(x)=b+1$，连续当且仅当 $1+a=b+1$，即 $a=b$。可微性：左导数 $f'_-(1)=2x|_{x=1}=2$，右导数 $f'_+(1)=b$，可微当且仅当连续条件成立且 $b=2$，即 $a=b=2$。此时 $f(1)=1+2=3$，切线方程为 $y-3=2(x-1)$，即 $y=2x+1$。连续但不可微：取 $a=b=1$，则 $f(x)=\begin{cases}x^2+1,&x\leq1\\ x+1,&x>1\end{cases}$ 在 $x=1$ 处连续($f(1)=2$)，但左导数 $2$ 与右导数 $1$ 不相等，曲线在 $(1,2)$ 处形成角点，不存在切线。

**答案原文**

连续当且仅当 $a=b$；可微当且仅当 $a=b=2$，此时切线为 $y=2x+1$；例如 $a=b=1$ 时连续但不可微(角点 $(1,2)$，无切线)。

## 287. draft-c46-05

内容 SHA256：`f48e744f38aae2247fd8958dd5c9a31dded4803f644a40968497060059aeb47b`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-06/draft.jsonl；源 SHA256 `2685493ba0765d9a8d1f8a1be3e55595e83614f9d6861bc1b87c95e2d4aad8df`；行 15，JSON pointer `/`。

**题干**

平面上画有间距为 $d$ 的平行直线族。将一根长为 $l$($l\le d$)的针随机投掷到平面上(针中点位置与针的方向均随机)。求针与某条直线相交的概率。

**过程**

设针中点到最近直线的距离为 $y$($0\le y\le\frac d2$,均匀),针与直线的夹角为 $\theta$($0\le\theta\le\frac\pi2$,均匀)。针与直线相交当且仅当 $y\le\frac l2\sin\theta$。样本空间面积为 $\frac d2\times\frac\pi2$,相交区域面积为 $\int_0^{\frac\pi2}\frac l2\sin\theta\,d\theta=\frac l2$。故 $P=\frac{\frac l2}{\frac{d\pi}{4}}=\frac{2l}{\pi d}$。

**答案原文**

相交概率为 $\frac{2l}{\pi d}$。

## 288. draft-c37-04

内容 SHA256：`f5750fe9b89f4311b8b5747d85a299e3561b1800769004df15486658a370ae1c`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft.jsonl；源 SHA256 `afcd74e3e4d285e77802f29ab182f9dce80cfe5833b983feb8af34694ed15331`；行 9，JSON pointer `/`。

**题干**

在 $\mathbb R^2$ 中，设从标准基 $\varepsilon$ 到基 $\eta=\{\eta_1=(1,1),\eta_2=(1,-1)\}$ 的过渡矩阵为 $P$，从 $\eta$ 到基 $\zeta=\{\zeta_1=(2,1),\zeta_2=(1,2)\}$ 的过渡矩阵为 $Q$。求 $P$、$Q$ 与从 $\varepsilon$ 到 $\zeta$ 的过渡矩阵，并验证后者等于 $PQ$；若向量 $\alpha$ 在基 $\zeta$ 下的坐标为 $(1,1)$，求 $\alpha$ 在标准基下的坐标。

**过程**

$P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$。求 $Q$：把 $\zeta_1=(2,1)$ 写成 $\eta$ 的组合，解 $(2,1)=a(1,1)+b(1,-1)$ 得 $a=\frac32,b=\frac12$;$\zeta_2=(1,2)=c(1,1)+d(1,-1)$ 得 $c=\frac32,d=-\frac12$。故 $Q=\begin{pmatrix}\frac32&\frac32\\\frac12&-\frac12\end{pmatrix}$。于是 $\varepsilon\to\zeta$ 的过渡矩阵 $R=PQ=\begin{pmatrix}1&1\\1&-1\end{pmatrix}\begin{pmatrix}\frac32&\frac32\\\frac12&-\frac12\end{pmatrix}=\begin{pmatrix}2&1\\1&2\end{pmatrix}$，恰为 $\zeta_1,\zeta_2$ 在标准基下的坐标按列排列，验证正确。$\alpha=1\cdot\zeta_1+1\cdot\zeta_2=(3,3)$。

**答案原文**

$P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$，$Q=\begin{pmatrix}\frac32&\frac32\\\frac12&-\frac12\end{pmatrix}$，$\varepsilon\to\zeta$ 的过渡矩阵为 $\begin{pmatrix}2&1\\1&2\end{pmatrix}=PQ$;$\alpha$ 在标准基下为 $(3,3)$。

## 289. draft-c18-05

内容 SHA256：`f72660ff809fb58094b3f5b99221e66758ed40c4c213d3f569feac968412974e`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft.jsonl；源 SHA256 `4a8930a557e05b01cec58257879ecd5bd9679b9c08e3e478767c363642ebe382`；行 10，JSON pointer `/`。

**题干**

证明空间中任意一点到给定平面 $\pi:n\cdot x=d$($n\neq0$)的投影点存在且唯一，并推导投影公式。

**过程**

存在性:对任意点 $P$，令 $\lambda=\frac{n\cdot P-d}{|n|^2}$，$Q=P-\lambda n$。则 $n\cdot Q=n\cdot P-\lambda|n|^2=n\cdot P-(n\cdot P-d)=d$，故 $Q\in\pi$。垂直性:对任意 $X\in\pi$，$(P-Q)\cdot(X-Q)=\lambda n\cdot(X-Q)=\lambda(n\cdot X-n\cdot Q)=\lambda(d-d)=0$，故 $PQ\perp\pi$，$Q$ 是投影点。唯一性:若 $Q'$ 也是投影点，则 $Q-Q'$ 平行于 $\pi$(属于 $\pi$ 的方向子空间)，即 $n\cdot(Q-Q')=n\cdot Q-n\cdot Q'=d-d=0$;又由垂直性，$(P-Q)\cdot(Q-Q')=0$ 与 $(P-Q')\cdot(Q-Q')=0$，两式相减得 $(Q-Q')\cdot(Q-Q')=0$，故 $Q=Q'$。投影公式:$Q=P-\frac{n\cdot P-d}{|n|^2}n$，距离为 $d(P,\pi)=\frac{|n\cdot P-d|}{|n|}$。

**答案原文**

投影点唯一,公式 $Q=P-\frac{n\cdot P-d}{|n|^2}n$;距离 $d(P,\pi)=\frac{|n\cdot P-d|}{|n|}$(证明见解法)。

## 290. draft-c50-03

内容 SHA256：`f73fa89b12c6a2ed72e3d31dda36da00820aa6e9e002a5685e604b52f1373cf3`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-18/draft.jsonl；源 SHA256 `6f921b08949f3ee7aaa95ce0363cafaff81b0ab7d0d95f10e1b5a280d697d8d1`；行 3，JSON pointer `/`。

**题干**

设 $X_1,\dots,X_{100}$ 独立同分布于指数分布 $Exp(1)$，$S=\sum_{i=1}^{100}X_i$。用中心极限定理近似求 $P(S>110)$，并与精确值(伽马分布)比较。

**过程**

$Exp(1)$ 的均值为 $1$、方差为 $1$。$ES=100$,$Var(S)=100$。CLT 近似:$P(S>110)\approx P(Z>\frac{110-100}{10})=P(Z>1)=1-\Phi(1)\approx0.1587$。精确值:$S$ 服从 $\Gamma(100,1)$ 分布(形状参数 $100$)。由精确恒等式 $P(\Gamma(100,1)>110)=P(\mathrm{Pois}(110)\le99)$(伽马与泊松的互补分布关系),对泊松分布求和得 $P(S>110)\approx0.1583$。两者之差仅约 $0.0004$,说明即使总体远非正态(指数分布严重右偏),CLT 近似在 $n=100$ 时已极准确。

**答案原文**

CLT 近似 $\approx0.159$;精确值(伽马/泊松互补)$\approx0.158$;两者差约 $0.0004$,近似极佳。

## 291. draft-c09-04

内容 SHA256：`f79fecc4a366ee995bb98b4e2d3cbc588564420e9fd792883efb83c0fa551407`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft.jsonl；源 SHA256 `1d0950f73fad698178bef910eec1c19d5303cfe6bdabbcd76bddab903f05e44b`；行 14，JSON pointer `/`。

**题干**

求由曲线 $y=x^2$、$x$ 轴与直线 $x=1$ 所围成的区域绕直线 $x=-1$ 旋转所得旋转体的体积。

**过程**

旋转轴为 $x=-1$,用柱壳法:在 $x$ 处柱壳到轴的距离为 $x-(-1)=x+1$,高为 $x^2$。$V=2\pi\int_0^1(x+1)x^2\,dx=2\pi\int_0^1(x^3+x^2)\,dx=2\pi\left(\frac14+\frac13\right)=\frac{7\pi}{6}$。

**答案原文**

体积为 $\frac{7\pi}{6}$。

## 292. eval-linalg-019-s1

内容 SHA256：`f918821ce807abf40f21a130d487a43c7de1a632ae4a36c1dbb417f904cf161e`。

来源：reviews/codex-supervision/history-from-code/recheck-68c51be/data/v2/eval/dataset_eval.json；源 SHA256 `1de2df62edd0b01403df813c80edc3a5a9dbf1791f0b223d8e0f107ccee55e6e`；行 —，JSON pointer `/249`。

**题干**

将二次型 $f(x,y)=2x^2+2xy+3y^2$ 化为标准形，并说明其正定性。

**过程**

$f=2\left(x^2+xy\right)+3y^2=2\left(x+\dfrac{y}{2}\right)^2-\dfrac{y^2}{2}+3y^2=2\left(x+\dfrac{y}{2}\right)^2+\dfrac{5}{2}y^2$。令 $u=x+\dfrac{y}{2}$、$v=y$，得标准形 $2u^2+\dfrac{5}{2}v^2$，两系数均为正，正惯性指数 2，二次型正定。

**答案原文**

配方法标准形 $2u^2+\dfrac{5}{2}v^2$（$u=x+\dfrac{y}{2}$，$v=y$）；正交标准形 $\dfrac{5+\sqrt5}{2}\xi^2+\dfrac{5-\sqrt5}{2}\eta^2$；正定

## 293. draft-c18-04

内容 SHA256：`fb0879da752ef160f414757754be4886ea2a9e54eafcc721703788af14f98333`。

来源：reviews/codex-supervision/2026-10-05-batch-repair-execution/before/batch-04.jsonl；源 SHA256 `a3d74ab73cb86b41071c5be7e103aabcbbba47a54a9df746aa1cbf629bd7660f`；行 9，JSON pointer `/`。

**题干**

求点 $P(1,0,0)$ 到直线 $l:\begin{cases}x+y+z=1\\ x-y+2z=0\end{cases}$(两平面交线)的距离与垂足。

**过程**

直线方向 $d=n_1\times n_2=(1,1,1)\times(1,-1,2)=(1\times2-1\times(-1),\,1\times1-1\times2,\,1\times(-1)-1\times1)=(3,-1,-2)$。取 $z=0$ 解 $\begin{cases}x+y=1\\x-y=0\end{cases}$ 得直线上一点 $P_0=(\frac12,\frac12,0)$。设垂足 $Q=P_0+td$，由 $(Q-P)\cdot d=0$：$(-\frac12+3t,\, \frac12-t,\,-2t)\cdot(3,-1,-2)=-\frac32+9t-\frac12+t+4t=-2+14t=0$，得 $t=\frac17$。垂足 $Q=(\frac12+\frac37,\,\frac12-\frac17,\,-\frac27)=(\frac{13}{14},\frac{5}{14},-\frac27)$。距离 $\|Q-P\|=\|(-\frac{1}{14},\frac{5}{14},-\frac{4}{14})\|=\frac{\sqrt{1+25+16}}{14}=\frac{\sqrt{42}}{14}$。(交叉验证:$|(P-P_0)\times d|/|d|=\sqrt3/\sqrt{14}=\sqrt{42}/14$。)严格验证：$n_1\cdot Q=1$、$n_2\cdot Q=0$、$(P-Q)\cdot d=0$。对任意$X=Q+sd\in l$，$\|P-X\|^2=\|P-Q\|^2+s^2\|d\|^2\ge\|P-Q\|^2$，等号仅在$s=0$成立。

**答案原文**

距离为 $\frac{\sqrt{42}}{14}$;垂足为 $(\frac{13}{14},\frac{5}{14},-\frac27)$。

## 294. draft-c39-01

内容 SHA256：`fb1a8099dd23fda2ded64d50d06b9c2e9aecd65e7ad8a8aa5bed03fa6ad6aa60`。

来源：reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol/git-history/blobs/28d2832a953c1046e1a5df5a429b1d9b5ea65c988e1936c2ec2fdeb28be2956b.bin；源 SHA256 `28d2832a953c1046e1a5df5a429b1d9b5ea65c988e1936c2ec2fdeb28be2956b`；行 —，JSON pointer `/1`。

**题干**

设线性变换 $T:\mathbb R^3\to\mathbb R^3$ 由 $T(x,y,z)=(x-y,\,y-z,\,z-x)$ 定义。求 $T$ 的核、像与各自的维数。

**过程**

核:解 $x-y=0,y-z=0,z-x=0$,得 $x=y=z$,故 $\ker T=\mathrm{span}\{(1,1,1)\}$,$\dim\ker T=1$。像:由秩-零度定理 $\dim\mathrm{im}\,T=3-1=2$。像的方程:三个分量之和 $(x-y)+(y-z)+(z-x)=0$,故像包含于平面 $u+v+w=0$;两者维数均为 $2$,故 $\mathrm{im}\,T=\{u+v+w=0\}$。

**答案原文**

$\\ker T=\\mathrm{span}\\{(1,1,1)\\}$(维数 $1$);$\\mathrm{im}\\,T=\\{u+v+w=0\\}$(维数 $2$)。

## 295. prob-039

内容 SHA256：`fc8be8eec7c72dbc1df655bbd7c17d18039c6046cc972571ff40e52459f31cdd`。

来源：reviews/codex-supervision/2026-10-06-scene-repair-takeover/math-correction-receipt.json；源 SHA256 `33c0a0bc6bc5281f513bf17fdda3de2a178f4700b9703bdcce7465e7cbcc0ef9`；行 —，JSON pointer `/corrections/5/record`。

**题干**

独立均匀地在正方形 $Q=[-1,1]^2$ 中选取 $n\ge1$ 个点，记落入单位圆 $D=\{(x,y):x^2+y^2\le1\}$ 的点数为 $m_n$。构造 $\widehat\pi_n=4m_n/n$，精确求其期望和方差，并证明 $\widehat\pi_n\xrightarrow{P}\pi$。说明有限样本的有理数 $4m_n/n$ 与符号常量 $\pi$ 的区别。

**过程**

令 $Q=[-1,1]^2$，$D=\{(x,y):x^2+y^2\le1\}$，独立均匀地在 $Q$ 中抽取 $n\ge1$ 个点。记 $I_i$ 为第 $i$ 点落入 $D$ 的指示变量，$m_n=\sum_{i=1}^n I_i$，则 $P(I_i=1)=\frac{\pi}{4}$。定义估计量 $\widehat\pi_n=\frac{4m_n}{n}$，这是给定计数后的精确有理数，不是有限样本下与 $\pi$ 的恒等式。$E(\widehat\pi_n)=\pi$，$\operatorname{Var}(\widehat\pi_n)=\frac{\pi(4-\pi)}{n}$。对任意 $\varepsilon>0$，切比雪夫不等式给出 $P(|\widehat\pi_n-\pi|\ge\varepsilon)\le\frac{\pi(4-\pi)}{n\varepsilon^2}\to0$，故 $\widehat\pi_n\xrightarrow{P}\pi$；强大数定律还给出几乎处处收敛。

**答案原文**

$\widehat\pi_n=\frac{4m_n}{n}$，$E(\widehat\pi_n)=\pi$，$\operatorname{Var}(\widehat\pi_n)=\frac{\pi(4-\pi)}{n}$，且 $\widehat\pi_n\xrightarrow{P}\pi$。

## 296. draft-c44-04

内容 SHA256：`fcb79e15b02b386967c16892c027ccbc19d17b42027740c8949c29c9167b41ae`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft.jsonl；源 SHA256 `b92648645c3b17a796e6b8938f67de934cddafd0cf192ab24ae006e5b423e27f`；行 9，JSON pointer `/`。

**题干**

在 $\mathbb R^3$ 上定义 $\omega(u,v)=(u\times v)\cdot e_1$($e_1=(1,0,0)$)。验证 $\omega$ 是交替的，并说明它不是辛形式(退化)。

**过程**

交替性:$\omega(v,u)=(v\times u)\cdot e_1=-(u\times v)\cdot e_1=-\omega(u,v)$(叉积反交换),故交替。退化性:$\omega$ 的核为 $\{u:\omega(u,v)=0,\ \forall v\}$。对 $u=e_1$,$\omega(e_1,v)=(e_1\times v)\cdot e_1=0$(叉积垂直于 $e_1$),对一切 $v$ 成立,故 $e_1$ 在核中,核非零,即 $\omega$ 退化。因此 $\omega$ 只是交替双线性形式,不是辛形式(辛形式要求非退化,且只能存在于偶数维空间)。

**答案原文**

$\omega$ 交替(叉积反交换)但退化($e_1$ 在核中),不是辛形式。

## 297. draft-c29-03

内容 SHA256：`fcc507260161a4356b0b83163fce6ac236ef0562894ee5cf2b3ed5130ba5145f`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft.jsonl；源 SHA256 `e019465093b291bd83fb6ae20f3eefc40a96df3e5137a246ad8813dd03f87b34`；行 8，JSON pointer `/`。

**题干**

用 $f$ 与 $f'$ 的公因式求多项式 $f(x)=x^4-4x^3+6x^2-4x+1$ 的重根及其重数。

**过程**

$f'(x)=4x^3-12x^2+12x-4=4(x-1)^3$。若 $x_0$ 是 $f$ 的重根,则 $x_0$ 必为 $f$ 与 $f'$ 的公根;这里 $f'$ 的根只有 $x=1$,检验 $f(1)=1-4+6-4+1=0$,故 $x=1$ 是重根。重数:用辗转相除法求 $\gcd(f,f')$。$f$ 除以 $f'$:设 $f=(x-1)^4$(由二项式 $(x-1)^4=x^4-4x^3+6x^2-4x+1$ 直接看出),则 $\gcd(f,f')=(x-1)^3$,故 $x=1$ 的重数为 $3+1=4$,即四重根。(或由 $f=(x-1)^4$ 直接得四重根。)

**答案原文**

$f=(x-1)^4$,$x=1$ 是四重根。

## 298. draft-c32-05

内容 SHA256：`fd46813a1364b47dab9a57be2f5814ddc0d40465f9ed70f315456ce20cffdcb3`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft.jsonl；源 SHA256 `e019465093b291bd83fb6ae20f3eefc40a96df3e5137a246ad8813dd03f87b34`；行 15，JSON pointer `/`。

**题干**

证明:齐次线性方程组 $Ax=0$ 的解集是 $\mathbb R^n$ 的线性子空间,其维数为 $n-\mathrm{rank}(A)$;非齐次方程组 $Ax=b$($b\neq0$)的解集是 $\eta_0+\ker A$(仿射子空间)而不是线性子空间。

**过程**

子空间:若 $x_1,x_2\in\ker A$,则 $A(x_1+x_2)=0$ 且 $A(cx_1)=0$,对加法与数乘封闭;又 $0\in\ker A$,故 $\ker A$ 是线性子空间。维数:设 $\mathrm{rank}(A)=r$。把 $A$ 通过行变换化为行阶梯形,主元列有 $r$ 个,对应 $r$ 个主变量,其余 $n-r$ 个为自由变量;自由变量任意取值即唯一确定解,解空间与 $\mathbb R^{n-r}$ 同构,故维数为 $n-r$。非齐次:若 $\eta_0$ 是 $Ax=b$ 的一个特解,则 $x$ 是解 ⟺ $x-\eta_0\in\ker A$,故解集为 $\eta_0+\ker A$,是 $\ker A$ 的陪集(仿射子空间)。因 $b\neq0$ 时 $0\notin\eta_0+\ker A$(否则 $b=A0=0$),不含零向量,故不是线性子空间。

**答案原文**

证明见解法($\\ker A$ 对加法数乘封闭;维数 $n-r$;非齐次解集为陪集且不含零向量)。

## 299. eval-linalg-014-s1

内容 SHA256：`ffa29b5b754385060385d7e3efe5941642d5e6b465e41c85ddbbeaaaa697d543`。

来源：reviews/codex-supervision/history-from-code/recheck-68c51be/data/v2/eval/dataset_eval.json；源 SHA256 `1de2df62edd0b01403df813c80edc3a5a9dbf1791f0b223d8e0f107ccee55e6e`；行 —，JSON pointer `/234`。

**题干**

求矩阵 $A=\begin{pmatrix}0&1\\1&0\end{pmatrix}$ 的特征值与特征向量，并说明其几何意义。

**过程**

$|\lambda I-A|=\begin{vmatrix}\lambda&-1\\-1&\lambda\end{vmatrix}=\lambda^2-1=0$，$\lambda=\pm 1$。$\lambda=1$：解 $(I-A)v=0$，即 $\begin{pmatrix}1&-1\\-1&1\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix}=0$，得 $x=y$，特征向量 $(1,1)^T$。$\lambda=-1$：解 $(-I-A)v=0$，即 $\begin{pmatrix}-1&-1\\-1&-1\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix}=0$，得 $x=-y$，特征向量 $(1,-1)^T$。

**答案原文**

特征值 $\lambda_1=1$（特征向量 $(1,1)^T$），$\lambda_2=-1$（特征向量 $(1,-1)^T$）；$A$ 是关于直线 $y=x$ 的反射
