## draft-c34-01

problem

设 $E=\begin{pmatrix}1&0&0\\0&1&0\\0&0&5\end{pmatrix}$。说明用 $E$ 左乘与右乘一个 $3$ 阶矩阵 $A$ 分别对 $A$ 做了什么操作。

solution

左乘 $EA$:把 $A$ 的第三行乘以 $5$(其余行不变)。右乘 $AE$:把 $A$ 的第三列乘以 $5$(其余列不变)。$E$ 是由单位矩阵把第三行(列)乘以 $5$ 得到的倍乘型初等矩阵。

answer

左乘:第三行乘 $5$;右乘:第三列乘 $5$。

scene_spec.objects[0]

设 $E=\begin{pmatrix}1&0&0\\0&1&0\\0&0&5\end{pmatrix}$。说明用 $E$ 左乘与右乘一个 $3$ 阶矩阵 $A$ 分别对 $A$ 做了什么操作。

scene_spec.objects[1]

左乘:第三行乘 $5$;右乘:第三列乘 $5$。

scene_spec.steps[0]

第一步:左乘 $EA$:把 $A$ 的第三行乘以 $5$(其余行不变)。

scene_spec.steps[1]

第二步:右乘 $AE$:把 $A$ 的第三列乘以 $5$(其余列不变)。

scene_spec.steps[2]

第三步:$E$ 是由单位矩阵把第三行(列)乘以 $5$ 得到的倍乘型初等矩阵。

## draft-c34-02

problem

构造把 $3$ 阶矩阵的第二行加到第一行的初等矩阵 $E$，并求 $E^{-1}$ 与 $E^{-1}$ 对应的操作。

solution

把第二行加到第一行的初等矩阵为 $E=\begin{pmatrix}1&1&0\\0&1&0\\0&0&1\end{pmatrix}$(左乘 $EA$ 即第一行加第二行)。其逆为把第一行减去第二行:$E^{-1}=\begin{pmatrix}1&-1&0\\0&1&0\\0&0&1\end{pmatrix}$。验证:$EE^{-1}=I$(第一行:$(1,1,0)$ 减第二行 $(0,1,0)$ 得 $(1,0,0)$)。

answer

$E=\begin{pmatrix}1&1&0\\0&1&0\\0&0&1\end{pmatrix}$;$E^{-1}=\begin{pmatrix}1&-1&0\\0&1&0\\0&0&1\end{pmatrix}$,对应「第一行减第二行」。

scene_spec.objects[0]

构造把 $3$ 阶矩阵的第二行加到第一行的初等矩阵 $E$，并求 $E^{-1}$ 与 $E^{-1}$ 对应的操作。

scene_spec.objects[1]

$E=\begin{pmatrix}1&1&0\\0&1&0\\0&0&1\end{pmatrix}$;$E^{-1}=\begin{pmatrix}1&-1&0\\0&1&0\\0&0&1\end{pmatrix}$,对应「第一行减第二行」。

scene_spec.steps[0]

第一步:把第二行加到第一行的初等矩阵为 $E=\begin{pmatrix}1&1&0\\0&1&0\\0&0&1\end{pmatrix}$(左乘 $EA$ 即第一行加第二行)。

scene_spec.steps[1]

第二步:其逆为把第一行减去第二行:$E^{-1}=\begin{pmatrix}1&-1&0\\0&1&0\\0&0&1\end{pmatrix}$。

scene_spec.steps[2]

第三步:验证:$EE^{-1}=I$(第一行:$(1,1,0)$ 减第二行 $(0,1,0)$ 得 $(1,0,0)$)。

## draft-c34-03

problem

先交换第一、二行，再将第一行乘以$2$。写出这一复合行变换的矩阵（初等矩阵的乘积），并验证作用顺序。

solution

$P_1=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}$,$P_2=\begin{pmatrix}2&0&0\\0&1&0\\0&0&1\end{pmatrix}$。先做 $P_1$ 后做 $P_2$ 对应左乘 $P_2P_1$(先作用的矩阵写在右边):$P_2P_1=\begin{pmatrix}2&0&0\\0&1&0\\0&0&1\end{pmatrix}\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}=\begin{pmatrix}0&2&0\\1&0&0\\0&0&1\end{pmatrix}$。复合矩阵把第二行换到第一行并乘以 $2$。

answer

复合变换矩阵为$\begin{pmatrix}0&2&0\\1&0&0\\0&0&1\end{pmatrix}$，它是两个初等矩阵的乘积。

scene_spec.objects[0]

先交换第一、二行，再将第一行乘以$2$。写出这一复合行变换的矩阵（初等矩阵的乘积），并验证作用顺序。

scene_spec.objects[1]

复合变换矩阵为$\begin{pmatrix}0&2&0\\1&0&0\\0&0&1\end{pmatrix}$，它是两个初等矩阵的乘积。

scene_spec.steps[0]

第一步:$P_1=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}$,$P_2=\begin{pmatrix}2&0&0\\0&1&0\\0&0&1\end{pmatrix}$。

scene_spec.steps[1]

第二步:先做 $P_1$ 后做 $P_2$ 对应左乘 $P_2P_1$(先作用的矩阵写在右边):$P_2P_1=\begin{pmatrix}2&0&0\\0&1&0\\0&0&1\end{pmatrix}\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}=\begin{pmatrix}0&2&0\\1&0&0\\0&0&1\end{pmatrix}$。

scene_spec.steps[2]

第三步:复合矩阵把第二行换到第一行并乘以 $2$。

## draft-c34-04

problem

把矩阵 $A=\begin{pmatrix}2&2\\0&1\end{pmatrix}$ 分解为初等矩阵的乘积。

solution

对 $A$ 作行变换化单位阵:第一步第一行乘以 $\frac12$,对应初等矩阵 $E_1'=\begin{pmatrix}\frac12&0\\0&1\end{pmatrix}$,$E_1'A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$;第二步第一行减去第二行,对应 $E_2'=\begin{pmatrix}1&-1\\0&1\end{pmatrix}$,$E_2'E_1'A=I$。故 $A=E_1'^{-1}E_2'^{-1}$。求逆:$E_1'^{-1}=\begin{pmatrix}2&0\\0&1\end{pmatrix}$(第一行乘 $2$),$E_2'^{-1}=\begin{pmatrix}1&1\\0&1\end{pmatrix}$(第一行加第二行)。故 $A=\begin{pmatrix}2&0\\0&1\end{pmatrix}\begin{pmatrix}1&1\\0&1\end{pmatrix}$。验证:乘积 $=\begin{pmatrix}2&2\\0&1\end{pmatrix}=A$ ✓。

answer

$A=\begin{pmatrix}2&0\\0&1\end{pmatrix}\begin{pmatrix}1&1\\0&1\end{pmatrix}$,两个初等矩阵之积。

scene_spec.objects[0]

把矩阵 $A=\begin{pmatrix}2&2\\0&1\end{pmatrix}$ 分解为初等矩阵的乘积。

scene_spec.objects[1]

$A=\begin{pmatrix}2&0\\0&1\end{pmatrix}\begin{pmatrix}1&1\\0&1\end{pmatrix}$,两个初等矩阵之积。

scene_spec.steps[0]

第一步:对 $A$ 作行变换化单位阵:第一步第一行乘以 $\frac12$,对应初等矩阵 $E_1'=\begin{pmatrix}\frac12&0\\0&1\end{pmatrix}$,$E_1'A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$;第二步第一行减去第二行,对应 $E_2'=\begin{pmatrix}1&-1\\0&1\end{pmatrix}$,$E_2'E_1'A=I$。

scene_spec.steps[1]

第二步:故 $A=E_1'^{-1}E_2'^{-1}$。

scene_spec.steps[2]

第三步:求逆:$E_1'^{-1}=\begin{pmatrix}2&0\\0&1\end{pmatrix}$(第一行乘 $2$),$E_2'^{-1}=\begin{pmatrix}1&1\\0&1\end{pmatrix}$(第一行加第二行)。

scene_spec.steps[3]

第四步:故 $A=\begin{pmatrix}2&0\\0&1\end{pmatrix}\begin{pmatrix}1&1\\0&1\end{pmatrix}$。

scene_spec.steps[4]

第五步:验证:乘积 $=\begin{pmatrix}2&2\\0&1\end{pmatrix}=A$ ✓。

## draft-c34-05

problem

记$E_{ij}(a)=I+a e_{ij}$（$i\ne j$），其中$e_{ij}$为三阶矩阵单位。证明$E_{12}(a)E_{23}(b)E_{12}(-a)E_{23}(-b)=E_{13}(ab)$，求逆矩阵，并用$a=2/3,b=3/4$精确验证。

solution

矩阵单位满足$e_{ij}e_{kl}=\delta_{jk}e_{il}$，特别是$e_{12}e_{23}=e_{13}$而$e_{23}e_{12}=0$，各相关平方为零。逐因子相乘，前三因子为$I+b e_{23}+ab e_{13}$，再乘$I-b e_{23}$得$I+ab e_{13}$。$E_{ij}(a)^{-1}=E_{ij}(-a)$，所以最终逆为$E_{13}(-ab)$。代入两分数得$ab=1/2$，复合为$\begin{pmatrix}1&0&1/2\\0&1&0\\0&0&1\end{pmatrix}$，逆将$1/2$改为$-1/2$。该交换子显示倍加变换的顺序通常不可交换。

answer

交换子$E_{13}(ab)$，逆$E_{13}(-ab)$；指定参数的非对角项$1/2$。

scene_spec.objects[0]

记$E_{ij}(a)=I+a e_{ij}$（$i\ne j$），其中$e_{ij}$为三阶矩阵单位。证明$E_{12}(a)E_{23}(b)E_{12}(-a)E_{23}(-b)=E_{13}(ab)$，求逆矩阵，并用$a=2/3,b=3/4$精确验证。

scene_spec.objects[1]

交换子$E_{13}(ab)$，逆$E_{13}(-ab)$；指定参数的非对角项$1/2$。

scene_spec.steps[0]

第一步:矩阵单位满足$e_{ij}e_{kl}=\delta_{jk}e_{il}$，特别是$e_{12}e_{23}=e_{13}$而$e_{23}e_{12}=0$，各相关平方为零。

scene_spec.steps[1]

第二步:逐因子相乘，前三因子为$I+b e_{23}+ab e_{13}$，再乘$I-b e_{23}$得$I+ab e_{13}$。

scene_spec.steps[2]

第三步:$E_{ij}(a)^{-1}=E_{ij}(-a)$，所以最终逆为$E_{13}(-ab)$。

scene_spec.steps[3]

第四步:代入两分数得$ab=1/2$，复合为$\begin{pmatrix}1&0&1/2\\0&1&0\\0&0&1\end{pmatrix}$，逆将$1/2$改为$-1/2$。

scene_spec.steps[4]

第五步:该交换子显示倍加变换的顺序通常不可交换。

## draft-c38-01

problem

设$M:\mathbb R^2\to\mathbb R^2$任意线性映射，在$\mathbb R^2\times\mathbb R^2$中取$U=\{(a,Ma)\}$、$V=\{(0,b)\}$。证明全空间是$U\oplus V$，求投影到$U$沿$V$的表达式及核、像、维数。

solution

$(a,b)=(a,Ma)+(0,b-Ma)$，第一项属$U$、第二项属$V$，故和为全空间。若$(a,Ma)=(0,b)$，则$a=0,b=0$，交为零，分解唯一。投影$P(a,b)=(a,Ma)$，$P^2=P$，核$V$、像$U$，两者维数均$2$。不需要$M$可逆；图空间与竖直空间的互补来自第一坐标的唯一性。

answer

$\mathbb R^4=U\oplus V$；$P(a,b)=(a,Ma)$，核$V$、像$U$，维数均$2$。

scene_spec.objects[0]

设$M:\mathbb R^2\to\mathbb R^2$任意线性映射，在$\mathbb R^2\times\mathbb R^2$中取$U=\{(a,Ma)\}$、$V=\{(0,b)\}$。证明全空间是$U\oplus V$，求投影到$U$沿$V$的表达式及核、像、维数。

scene_spec.objects[1]

$\mathbb R^4=U\oplus V$；$P(a,b)=(a,Ma)$，核$V$、像$U$，维数均$2$。

scene_spec.steps[0]

第一步:$(a,b)=(a,Ma)+(0,b-Ma)$，第一项属$U$、第二项属$V$，故和为全空间。

scene_spec.steps[1]

第二步:若$(a,Ma)=(0,b)$，则$a=0,b=0$，交为零，分解唯一。

scene_spec.steps[2]

第三步:投影$P(a,b)=(a,Ma)$，$P^2=P$，核$V$、像$U$，两者维数均$2$。

scene_spec.steps[3]

第四步:不需要$M$可逆；图空间与竖直空间的互补来自第一坐标的唯一性。

## draft-c38-02

problem

在$\mathbb R[x]_{\le4}$中，令$U$为偶多项式，$V$为被$(x-1)^2$整除的多项式。求$U\cap V$、$U+V$及维数，判断和是否直和。

solution

$U=\operatorname{span}(1,x^2,x^4)$，维数$3$；$V=(x-1)^2\mathbb R[x]_{\le2}$，维数$3$。若$f=a+bx^2+cx^4\in V$，须$f(1)=f^{\prime}(1)=0$，即$a+b+c=0,2b+4c=0$，得$f=c(x^2-1)^2$。故交为该一维空间。和的维数$3+3-1=5$，等于环境维数，所以和为全部$\mathbb R[x]_{\le4}$。交非零，故不是直和。

answer

交$\operatorname{span}\{(x^2-1)^2\}$，维数$1$；和为五维全空间，非直和。

scene_spec.objects[0]

在$\mathbb R[x]_{\le4}$中，令$U$为偶多项式，$V$为被$(x-1)^2$整除的多项式。求$U\cap V$、$U+V$及维数，判断和是否直和。

scene_spec.objects[1]

交$\operatorname{span}\{(x^2-1)^2\}$，维数$1$；和为五维全空间，非直和。

scene_spec.steps[0]

第一步:$U=\operatorname{span}(1,x^2,x^4)$，维数$3$；$V=(x-1)^2\mathbb R[x]_{\le2}$，维数$3$。

scene_spec.steps[1]

第二步:若$f=a+bx^2+cx^4\in V$，须$f(1)=f^{\prime}(1)=0$，即$a+b+c=0,2b+4c=0$，得$f=c(x^2-1)^2$。

scene_spec.steps[2]

第三步:故交为该一维空间。

scene_spec.steps[3]

第四步:和的维数$3+3-1=5$，等于环境维数，所以和为全部$\mathbb R[x]_{\le4}$。

scene_spec.steps[4]

第五步:交非零，故不是直和。

## draft-c38-03

problem

在实$2\times2$矩阵空间中，令$U$为对称矩阵、$V$为迹为零的矩阵。给出交空间的基、两空间与和的维数，并显式证明和为全空间。

solution

$U$维数$3$，$V$维数$3$。交中矩阵为$\begin{pmatrix}a&b\\b&-a\end{pmatrix}$，基为$\operatorname{diag}(1,-1)$与$\begin{pmatrix}0&1\\1&0\end{pmatrix}$，维数$2$。对任意$A$，分解$A=(\operatorname{tr}A/2)I+[A-(\operatorname{tr}A/2)I]$，前项对称、后项无迹，故和为全空间，维数$4$。交非零，所以分解成任意$U,V$成分不唯一，也不是直和。

answer

$\dim U=\dim V=3$，交维数$2$、基如上，和为四维全空间，非直和。

scene_spec.objects[0]

在实$2\times2$矩阵空间中，令$U$为对称矩阵、$V$为迹为零的矩阵。给出交空间的基、两空间与和的维数，并显式证明和为全空间。

scene_spec.objects[1]

$\dim U=\dim V=3$，交维数$2$、基如上，和为四维全空间，非直和。

scene_spec.steps[0]

第一步:$U$维数$3$，$V$维数$3$。

scene_spec.steps[1]

第二步:交中矩阵为$\begin{pmatrix}a&b\\b&-a\end{pmatrix}$，基为$\operatorname{diag}(1,-1)$与$\begin{pmatrix}0&1\\1&0\end{pmatrix}$，维数$2$。

scene_spec.steps[2]

第三步:对任意$A$，分解$A=(\operatorname{tr}A/2)I+[A-(\operatorname{tr}A/2)I]$，前项对称、后项无迹，故和为全空间，维数$4$。

scene_spec.steps[3]

第四步:交非零，所以分解成任意$U,V$成分不唯一，也不是直和。

## draft-c38-04

problem

设 $U,V$ 是 $\mathbb R^5$ 的子空间，$\dim U=3$，$\dim V=2$。求 $\dim(U\cap V)$ 的可能取值范围，并说明每种取值对应的 $\dim(U+V)$。

solution

$\dim(U+V)=3+2-\dim(U\cap V)\le5$，交维数为$0,1,2$之一，和维数对应$5,4,3$。固定$U=\operatorname{span}(e_1,e_2,e_3)$，分别取$V=\operatorname{span}(e_4,e_5)$、$\operatorname{span}(e_1,e_4)$、$\operatorname{span}(e_1,e_2)$，便逐一达到这些可能。

answer

$\dim(U\cap V)\in\{0,1,2\}$,对应 $\dim(U+V)=5,4,3$。

scene_spec.objects[0]

设 $U,V$ 是 $\mathbb R^5$ 的子空间，$\dim U=3$，$\dim V=2$。求 $\dim(U\cap V)$ 的可能取值范围，并说明每种取值对应的 $\dim(U+V)$。

scene_spec.objects[1]

$\dim(U\cap V)\in\{0,1,2\}$,对应 $\dim(U+V)=5,4,3$。

scene_spec.steps[0]

第一步:$\dim(U+V)=3+2-\dim(U\cap V)\le5$，交维数为$0,1,2$之一，和维数对应$5,4,3$。

scene_spec.steps[1]

第二步:固定$U=\operatorname{span}(e_1,e_2,e_3)$，分别取$V=\operatorname{span}(e_4,e_5)$、$\operatorname{span}(e_1,e_4)$、$\operatorname{span}(e_1,e_2)$，便逐一达到这些可能。

## draft-c38-05

problem

证明维数公式:若 $U,V$ 是有限维线性空间 $W$ 的子空间，则 $\dim(U+V)=\dim U+\dim V-\dim(U\cap V)$。

solution

取交空间基$u_1,\ldots,u_k$，分别扩充为$U$的基$u_i,p_j$与$V$的基$u_i,q_l$。合并列表张成$U+V$。若$\sum a_iu_i+\sum b_jp_j+\sum c_lq_l=0$，则$\sum b_jp_j$同时属于$U$与$V$，属于交空间；由$U$基独立得$b_j=0$，再由$V$基得$a_i=c_l=0$。因此合并列表是基，其长度为$\dim U+\dim V-\dim(U\cap V)$，得到维数公式。

answer

证明见解法(交的基延拓为两子空间的基,拼接组构成 $U+V$ 的基)。

scene_spec.objects[0]

证明维数公式:若 $U,V$ 是有限维线性空间 $W$ 的子空间，则 $\dim(U+V)=\dim U+\dim V-\dim(U\cap V)$。

scene_spec.objects[1]

证明见解法(交的基延拓为两子空间的基,拼接组构成 $U+V$ 的基)。

scene_spec.steps[0]

第一步:取交空间基$u_1,\ldots,u_k$，分别扩充为$U$的基$u_i,p_j$与$V$的基$u_i,q_l$。

scene_spec.steps[1]

第二步:合并列表张成$U+V$。

scene_spec.steps[2]

第三步:若$\sum a_iu_i+\sum b_jp_j+\sum c_lq_l=0$，则$\sum b_jp_j$同时属于$U$与$V$，属于交空间；由$U$基独立得$b_j=0$，再由$V$基得$a_i=c_l=0$。

scene_spec.steps[3]

第四步:因此合并列表是基，其长度为$\dim U+\dim V-\dim(U\cap V)$，得到维数公式。

## draft-c39-01

problem

在实$2\times2$矩阵空间中取$A=\operatorname{diag}(1,3)$，定义$T(X)=AX-XA$。求核、像、秩，并说明全空间能否分解为核与像的直和。

solution

对$X=\begin{pmatrix}a&b\\c&d\end{pmatrix}$，$T(X)=\begin{pmatrix}0&-2b\\2c&0\end{pmatrix}$。所以核为所有对角矩阵，基$e_{11},e_{22}$；像为所有零对角矩阵，基$e_{12},e_{21}$，秩$2$。两空间交为零且每个矩阵唯一分解为对角部分与零对角部分，故是直和。$T$在像上可逆，$T^2$在像上为$4I$，与在核上为零的作用不同；非正交Jordan中心化问题未被套用。

answer

核为对角矩阵，像为零对角矩阵，秩$2$；$M_2(\mathbb R)=\ker T\oplus\operatorname{im}T$。

scene_spec.objects[0]

在实$2\times2$矩阵空间中取$A=\operatorname{diag}(1,3)$，定义$T(X)=AX-XA$。求核、像、秩，并说明全空间能否分解为核与像的直和。

scene_spec.objects[1]

核为对角矩阵，像为零对角矩阵，秩$2$；$M_2(\mathbb R)=\ker T\oplus\operatorname{im}T$。

scene_spec.steps[0]

第一步:对$X=\begin{pmatrix}a&b\\c&d\end{pmatrix}$，$T(X)=\begin{pmatrix}0&-2b\\2c&0\end{pmatrix}$。

scene_spec.steps[1]

第二步:所以核为所有对角矩阵，基$e_{11},e_{22}$；像为所有零对角矩阵，基$e_{12},e_{21}$，秩$2$。

scene_spec.steps[2]

第三步:两空间交为零且每个矩阵唯一分解为对角部分与零对角部分，故是直和。

scene_spec.steps[3]

第四步:$T$在像上可逆，$T^2$在像上为$4I$，与在核上为零的作用不同；非正交Jordan中心化问题未被套用。

## draft-c39-02

problem

设 $T:\mathbb R^2\to\mathbb R^3$ 由 $T(x,y)=(x+y,\,x-y,\,2x)$ 定义。判断 $T$ 是否单射、是否满射，并求核与像的维数。

solution

核:解 $x+y=0,x-y=0,2x=0$,得 $x=y=0$,故 $\ker T=\{0\}$,$\dim\ker T=0$,由秩-零度定理 $\dim\mathrm{im}\,T=2-0=2$。单射:核为 $\{0\}$ ⟺ 单射,故 $T$ 单射。满射:像的维数 $2<3$,故 $T$ 非满射(像是 $\mathbb R^3$ 中由 $T(1,0)=(1,1,2)$ 与 $T(0,1)=(1,-1,0)$ 张成的平面)。

answer

单射但非满射;$\ker T=\{0\}$(维数 $0$),$\dim\mathrm{im}\,T=2$。

scene_spec.objects[0]

设 $T:\mathbb R^2\to\mathbb R^3$ 由 $T(x,y)=(x+y,\,x-y,\,2x)$ 定义。判断 $T$ 是否单射、是否满射，并求核与像的维数。

scene_spec.objects[1]

单射但非满射;$\ker T=\{0\}$(维数 $0$),$\dim\mathrm{im}\,T=2$。

scene_spec.steps[0]

第一步:核:解 $x+y=0,x-y=0,2x=0$,得 $x=y=0$,故 $\ker T=\{0\}$,$\dim\ker T=0$,由秩-零度定理 $\dim\mathrm{im}\,T=2-0=2$。

scene_spec.steps[1]

第二步:单射:核为 $\{0\}$ ⟺ 单射,故 $T$ 单射。

scene_spec.steps[2]

第三步:满射:像的维数 $2<3$,故 $T$ 非满射(像是 $\mathbb R^3$ 中由 $T(1,0)=(1,1,2)$ 与 $T(0,1)=(1,-1,0)$ 张成的平面)。

## draft-c39-03

problem

定义$T:\mathbb R[x]_{\le3}\to\mathbb R^3$，$Tf=(f(0),f(1),f(-1))$。求核、像与秩，给出证明满射的显式右逆。

solution

核中$f$在$0,1,-1$三个不同节点为零，因此被$x(x-1)(x+1)$整除；度数最多$3$，故核$\operatorname{span}(x^3-x)$。对$(a,b,c)\in\mathbb R^3$，定义$R(a,b,c)=a(1-x^2)+b x(x+1)/2+c x(x-1)/2$，三个节点的值依次为$a,b,c$，所以$TR=I$。故像为全部$\mathbb R^3$，秩$3$、核维数$1$，右逆证明满射不依赖仅报维数。

answer

核$\operatorname{span}(x^3-x)$；像$\mathbb R^3$、秩$3$；右逆$R(a,b,c)=a(1-x^2)+\frac b2x(x+1)+\frac c2x(x-1)$。

scene_spec.objects[0]

定义$T:\mathbb R[x]_{\le3}\to\mathbb R^3$，$Tf=(f(0),f(1),f(-1))$。求核、像与秩，给出证明满射的显式右逆。

scene_spec.objects[1]

核$\operatorname{span}(x^3-x)$；像$\mathbb R^3$、秩$3$；右逆$R(a,b,c)=a(1-x^2)+\frac b2x(x+1)+\frac c2x(x-1)$。

scene_spec.steps[0]

第一步:核中$f$在$0,1,-1$三个不同节点为零，因此被$x(x-1)(x+1)$整除；度数最多$3$，故核$\operatorname{span}(x^3-x)$。

scene_spec.steps[1]

第二步:对$(a,b,c)\in\mathbb R^3$，定义$R(a,b,c)=a(1-x^2)+b x(x+1)/2+c x(x-1)/2$，三个节点的值依次为$a,b,c$，所以$TR=I$。

scene_spec.steps[2]

第三步:故像为全部$\mathbb R^3$，秩$3$、核维数$1$，右逆证明满射不依赖仅报维数。

## draft-c39-04

problem

设 $T:\mathbb R^3\to\mathbb R^3$ 由 $T(x,y,z)=(x+y,\,y+z,\,0)$ 定义。求 $T^2$ 的表达式，并比较 $T$ 与 $T^2$ 的核与像。

solution

$T^2(x,y,z)=T(x+y,\,y+z,\,0)=((x+y)+(y+z),\,(y+z)+0,\,0)=(x+2y+z,\,y+z,\,0)$。核:$T$ 的核:$x+y=0,y+z=0$,得 $(x,-x,x)$,$\ker T=\mathrm{span}\{(1,-1,1)\}$。$T^2$ 的核:$x+2y+z=0,y+z=0$。由第二式 $z=-y$,代入第一式得 $x+2y-y=x+y=0$,故与 $\ker T$ 相同的条件,$\ker T^2=\ker T=\mathrm{span}\{(1,-1,1)\}$。像:$T$ 的像由 $T(1,0,0)=(1,0,0)$,$T(0,1,0)=(1,1,0)$,$T(0,0,1)=(0,1,0)$ 张成,即 $\{(a,b,0)\}$,维数 $2$。$T^2$ 的像由 $T^2(1,0,0)=(1,0,0)$,$T^2(0,0,1)=(1,1,0)$ 张成($T^2(0,1,0)=(2,1,0)=(1,0,0)+(1,1,0)$),也是 $\{(a,b,0)\}$,维数 $2$。故 $\ker T^2=\ker T$ 且 $\mathrm{im}\,T^2=\mathrm{im}\,T$(本例中复合映射的核与像均不变)。

answer

$T^2(x,y,z)=(x+2y+z,\,y+z,\,0)$;$\ker T^2=\ker T=\mathrm{span}\{(1,-1,1)\}$,$\mathrm{im}\,T^2=\mathrm{im}\,T=\{(a,b,0)\}$。

scene_spec.objects[0]

设 $T:\mathbb R^3\to\mathbb R^3$ 由 $T(x,y,z)=(x+y,\,y+z,\,0)$ 定义。求 $T^2$ 的表达式，并比较 $T$ 与 $T^2$ 的核与像。

scene_spec.objects[1]

$T^2(x,y,z)=(x+2y+z,\,y+z,\,0)$;$\ker T^2=\ker T=\mathrm{span}\{(1,-1,1)\}$,$\mathrm{im}\,T^2=\mathrm{im}\,T=\{(a,b,0)\}$。

scene_spec.steps[0]

第一步:$T^2(x,y,z)=T(x+y,\,y+z,\,0)=((x+y)+(y+z),\,(y+z)+0,\,0)=(x+2y+z,\,y+z,\,0)$。

scene_spec.steps[1]

第二步:核:$T$ 的核:$x+y=0,y+z=0$,得 $(x,-x,x)$,$\ker T=\mathrm{span}\{(1,-1,1)\}$。

scene_spec.steps[2]

第三步:$T^2$ 的核:$x+2y+z=0,y+z=0$。

scene_spec.steps[3]

第四步:由第二式 $z=-y$,代入第一式得 $x+2y-y=x+y=0$,故与 $\ker T$ 相同的条件,$\ker T^2=\ker T=\mathrm{span}\{(1,-1,1)\}$。

scene_spec.steps[4]

第五步:像:$T$ 的像由 $T(1,0,0)=(1,0,0)$,$T(0,1,0)=(1,1,0)$,$T(0,0,1)=(0,1,0)$ 张成,即 $\{(a,b,0)\}$,维数 $2$。

scene_spec.steps[5]

第六步:$T^2$ 的像由 $T^2(1,0,0)=(1,0,0)$,$T^2(0,0,1)=(1,1,0)$ 张成($T^2(0,1,0)=(2,1,0)=(1,0,0)+(1,1,0)$),也是 $\{(a,b,0)\}$,维数 $2$。

scene_spec.steps[6]

第七步:故 $\ker T^2=\ker T$ 且 $\mathrm{im}\,T^2=\mathrm{im}\,T$(本例中复合映射的核与像均不变)。

## draft-c39-05

problem

证明秩-零度定理:若 $T:V\to W$ 是有限维线性空间之间的线性映射，则 $\dim V=\dim\ker T+\dim\mathrm{im}\,T$。

solution

取 $\ker T$ 的一组基 $v_1,\dots,v_k$,延拓为 $V$ 的基 $v_1,\dots,v_k,v_{k+1},\dots,v_n$(故 $\dim V=n$)。下证 $T(v_{k+1}),\dots,T(v_n)$ 是 $\mathrm{im}\,T$ 的一组基。张成:任意 $y\in\mathrm{im}\,T$,存在 $x=\sum_{i=1}^{n}c_iv_i$ 使 $y=T(x)=\sum_{i=1}^{n}c_iT(v_i)=\sum_{i=k+1}^{n}c_iT(v_i)$(前 $k$ 项为零,因 $v_i\in\ker T$)。线性无关:若 $\sum_{i=k+1}^{n}d_iT(v_i)=0$,则 $T\left(\sum_{i=k+1}^{n}d_iv_i\right)=0$,即 $\sum_{i=k+1}^{n}d_iv_i\in\ker T$,它可仅由 $v_1,\dots,v_k$ 表出;但 $V$ 的基表示唯一,故 $d_{k+1}=\cdots=d_n=0$。于是 $\dim\mathrm{im}\,T=n-k$,即 $\dim V=n=k+(n-k)=\dim\ker T+\dim\mathrm{im}\,T$。

answer

证明见解法(核的基延拓到全空间,核外基向量的像构成像的基)。

scene_spec.objects[0]

证明秩-零度定理:若 $T:V\to W$ 是有限维线性空间之间的线性映射，则 $\dim V=\dim\ker T+\dim\mathrm{im}\,T$。

scene_spec.objects[1]

证明见解法(核的基延拓到全空间,核外基向量的像构成像的基)。

scene_spec.steps[0]

第一步:取 $\ker T$ 的一组基 $v_1,\dots,v_k$,延拓为 $V$ 的基 $v_1,\dots,v_k,v_{k+1},\dots,v_n$(故 $\dim V=n$)。

scene_spec.steps[1]

第二步:下证 $T(v_{k+1}),\dots,T(v_n)$ 是 $\mathrm{im}\,T$ 的一组基。

scene_spec.steps[2]

第三步:张成:任意 $y\in\mathrm{im}\,T$,存在 $x=\sum_{i=1}^{n}c_iv_i$ 使 $y=T(x)=\sum_{i=1}^{n}c_iT(v_i)=\sum_{i=k+1}^{n}c_iT(v_i)$(前 $k$ 项为零,因 $v_i\in\ker T$)。

scene_spec.steps[3]

第四步:线性无关:若 $\sum_{i=k+1}^{n}d_iT(v_i)=0$,则 $T\left(\sum_{i=k+1}^{n}d_iv_i\right)=0$,即 $\sum_{i=k+1}^{n}d_iv_i\in\ker T$,它可仅由 $v_1,\dots,v_k$ 表出;但 $V$ 的基表示唯一,故 $d_{k+1}=\cdots=d_n=0$。

scene_spec.steps[4]

第五步:于是 $\dim\mathrm{im}\,T=n-k$,即 $\dim V=n=k+(n-k)=\dim\ker T+\dim\mathrm{im}\,T$。
