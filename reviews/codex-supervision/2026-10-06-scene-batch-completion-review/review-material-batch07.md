# Batch 7 independent review material


## draft-c34-05

P: 记$E_{ij}(a)=I+a e_{ij}$（$i\ne j$），其中$e_{ij}$为三阶矩阵单位。证明$E_{12}(a)E_{23}(b)E_{12}(-a)E_{23}(-b)=E_{13}(ab)$，求逆矩阵，并用$a=2/3,b=3/4$精确验证。

S: 矩阵单位满足$e_{ij}e_{kl}=\delta_{jk}e_{il}$，特别是$e_{12}e_{23}=e_{13}$而$e_{23}e_{12}=0$，各相关平方为零。逐因子相乘，前三因子为$I+b e_{23}+ab e_{13}$，再乘$I-b e_{23}$得$I+ab e_{13}$。$E_{ij}(a)^{-1}=E_{ij}(-a)$，所以最终逆为$E_{13}(-ab)$。代入两分数得$ab=1/2$，复合为$\begin{pmatrix}1&0&1/2\\0&1&0\\0&0&1\end{pmatrix}$，逆将$1/2$改为$-1/2$。该交换子显示倍加变换的顺序通常不可交换。

A: 交换子$E_{13}(ab)$，逆$E_{13}(-ab)$；指定参数的非对角项$1/2$。

Objects: 题面卡:$E_{ij}(a)=I+ae_{ij}$ 的四因子复合与逆 | 板书一:乘法规则 $e_{ij}e_{kl}=\delta_{jk}e_{il}$ 与关键事实 $e_{12}e_{23}=e_{13}$、$e_{23}e_{12}=0$ | 高亮框:关键点——$e_{13}$ 项经 $e_{12}e_{23}$ 积累系数 $ab$ | 板书二:逆公式 $(I+ae_{ij})(I-ae_{ij})=I$ 的展开验证 | 验证卡:$a=\frac23,b=\frac34$ 代入得 $ab=\frac12$

Steps:
第一步:乘法规则(高亮):$e_{ij}e_{kl}=\delta_{jk}e_{il}$;关键事实:$e_{12}e_{23}=e_{13}$ 而 $e_{23}e_{12}=0$;各相关平方为零:$e_{12}^2=e_{23}^2=e_{13}^2=0$。
第二步:逐因子相乘(逐步,高亮):$(I+ae_{12})(I+be_{23})=I+ae_{12}+be_{23}+abe_{13}$;再乘 $(I-ae_{12})$:结果 $=I+ae_{12}+be_{23}+abe_{13}-ae_{12}-a^2e_{12}^2-abe_{12}e_{23}-a^2be_{13}e_{12}=I+be_{23}+abe_{13}$(用 $e_{12}^2=0$、$e_{13}e_{12}=0$ 消去)。
第三步:再乘 $(I-be_{23})$:$(I+be_{23}+abe_{13})(I-be_{23})=I+be_{23}+abe_{13}-be_{23}-b^2e_{23}^2-ab^2e_{13}e_{23}=I+abe_{13}$;故复合 $=E_{13}(ab)$(关键点:$e_{13}$ 项经 $e_{12}e_{23}=e_{13}$ 积累系数 $ab$,高亮)。
第四步:逆公式验证(逐项):$(I+ae_{ij})(I-ae_{ij})=I+ae_{ij}-ae_{ij}-a^2e_{ij}^2=I$(因 $e_{ij}^2=0$);故 $E_{ij}(a)^{-1}=E_{ij}(-a)$,最终逆为 $E_{13}(-ab)$。
第五步:代入验证(逐步):$a=\frac23,b=\frac34$:$ab=\frac23\cdot\frac34=\frac12$;复合为 $E_{13}(\frac12)=I+\frac12e_{13}$,$(1,3)$ 元为 $\frac12$(高亮结论)。


## draft-c35-02

P: 对四元二次型$f=(x_1-x_2)^2+2(x_2-x_3)^2+3(x_3-x_4)^2$，给出可逆线性替换、合同标准形及惯性；再证明将$f$限制在$V=\{x:x_4=0\}$上后成为正定型。

S: 令$u_1=x_1-x_2,u_2=x_2-x_3,u_3=x_3-x_4,w=x_4$。反解为$x_4=w,x_3=u_3+w,x_2=u_2+u_3+w,x_1=u_1+u_2+u_3+w$，故替换可逆。标准形为$u_1^2+2u_2^2+3u_3^2+0w^2$；再伸缩$v_1=u_1,v_2=\sqrt2u_2,v_3=\sqrt3u_3$得规范形$v_1^2+v_2^2+v_3^2+0w^2$。全空间的秩为$3$，惯性为$(3,0,1)$，核为$\operatorname{span}\{(1,1,1,1)\}$。若$x\in V$且$f(x)=0$，三个平方均为零，故$x=c(1,1,1,1)$；第四坐标为零又给$c=0$，故$x=0$。因此$f|_V$正定；$\dim V=3$，其惯性为$(3,0,0)$。亦可在新坐标中写约束$w=0$，三个差分坐标仍独立，标准形保留三个正平方。

A: 全空间标准形$u_1^2+2u_2^2+3u_3^2+0w^2$，秩$3$、惯性$(3,0,1)$；限制在$V$上正定，惯性$(3,0,0)$。

Objects: 题面卡:$f=(x_1-x_2)^2+2(x_2-x_3)^2+3(x_3-x_4)^2$ 的替换与惯性 | 板书一:替换 $u_1=x_1-x_2$ 等与反解的逐步代入 | 高亮框:关键点——上三角反解保证替换可逆 | 板书二:标准形与伸缩 $v_2=\sqrt2u_2$、$v_3=\sqrt3u_3$ | 限制卡:$V=\{x:x_4=0\}$ 上逐项归零得正定

Steps:
第一步:作替换:$u_1=x_1-x_2$,$u_2=x_2-x_3$,$u_3=x_3-x_4$,$w=x_4$。
第二步:反解(逐步代入,高亮):$x_4=w$;$x_3=u_3+x_4=u_3+w$;$x_2=u_2+x_3=u_2+u_3+w$;$x_1=u_1+x_2=u_1+u_2+u_3+w$;上三角结构保证替换可逆。
第三步:标准形:$f=u_1^2+2u_2^2+3u_3^2+0w^2$;再伸缩(逐项):$v_1=u_1$,$v_2=\sqrt2u_2$(因 $(\sqrt2u_2)^2=2u_2^2$),$v_3=\sqrt3u_3$;得规范形 $v_1^2+v_2^2+v_3^2+0w^2$。
第四步:全空间结论:秩为 $3$,惯性为 $(3,0,1)$(3 正、0 负、1 零,高亮)。
第五步:限制在 $V=\{x:x_4=0\}$:此时 $u_3=x_3$;$f|_V=(x_1-x_2)^2+2(x_2-x_3)^2+3x_3^2$;若其为零,逐项得 $x_3=0$、$x_2=0$、$x_1=0$;故限制后为正定型(高亮)。


## draft-c35-05

P: 判断二次型 $f(x,y,z)=x^2+2y^2+3z^2+2xy$ 与 $g(x,y,z)=2x^2+3y^2+4z^2$ 是否合同，并说明理由；若合同，构造可逆矩阵 $C$ 使 $C^{\mathsf{T}}AC=B$。

S: 配方：$f=(x+y)^2+y^2+3z^2$，正惯性指数 $3$，正定；$g=2x^2+3y^2+4z^2$，正惯性指数 $3$，正定。由惯性定理，两者惯性指数相同，故合同(都与 $I_3$ 合同，由合同关系的传递性)。构造：令 $M_f=\begin{pmatrix}1&1&0\\0&1&0\\0&0&\sqrt3\end{pmatrix}$，则 $f=(M_fx)^{\mathsf{T}}(M_fx)$，即 $A=M_f^{\mathsf{T}}M_f$;令 $M_g=\mathrm{diag}(\sqrt2,\sqrt3,2)$，则 $B=M_g^{\mathsf{T}}M_g$。于是 $B=(M_f^{-1}M_g)^{\mathsf{T}}A(M_f^{-1}M_g)$，取 $C=M_f^{-1}M_g=\begin{pmatrix}1&-1&0\\0&1&0\\0&0&\frac{1}{\sqrt3}\end{pmatrix}\begin{pmatrix}\sqrt2&0&0\\0&\sqrt3&0\\0&0&2\end{pmatrix}=\begin{pmatrix}\sqrt2&-\sqrt3&0\\0&\sqrt3&0\\0&0&\frac{2}{\sqrt3}\end{pmatrix}$。验证:$C^{\mathsf{T}}AC=\mathrm{diag}(2,3,4)=B$(逐项相乘核对),且 $\det C=2\sqrt2\neq0$。

A: 合同(两者均正定,惯性指数 $(3,0,0)$);$C=\begin{pmatrix}\sqrt2&-\sqrt3&0\\0&\sqrt3&0\\0&0&\frac{2}{\sqrt3}\end{pmatrix}$。

Objects: 题面卡:$f=x^2+2y^2+3z^2+2xy$ 与 $g=2x^2+3y^2+4z^2$ 的合同判定 | 板书一:配方 $f=(x+y)^2+y^2+3z^2$ 与 $g=(\sqrt2x)^2+(\sqrt3y)^2+(2z)^2$ | 高亮框:关键点——惯性指数同为 $(3,0,0)$,由惯性定理合同 | 行×列计算板:$C=M_f^{-1}M_g$ 与 $C^{\mathsf T}AC=B$ 的逐项验证 | 结论卡:$C=\begin{pmatrix}\sqrt2&-\sqrt3&0\\0&\sqrt3&0\\0&0&\frac2{\sqrt3}\end{pmatrix}$

Steps:
第一步:配方(逐步,高亮):$f=x^2+2xy+2y^2+3z^2=(x+y)^2+y^2+3z^2$,正惯性指数 $3$,正定;$g=(\sqrt2x)^2+(\sqrt3y)^2+(2z)^2$,正惯性指数 $3$,正定。
第二步:由惯性定理,两者惯性指数同为 $(3,0,0)$,故合同(都与 $I_3$ 合同,由合同关系的传递性,高亮)。
第三步:构造(逐项):由配方取 $M_f=\begin{pmatrix}1&1&0\\0&1&0\\0&0&\sqrt3\end{pmatrix}$($M_fx=(x+y,y,\sqrt3z)$),则 $A=M_f^{\mathsf T}M_f$;$M_g=\operatorname{diag}(\sqrt2,\sqrt3,2)$,则 $B=M_g^{\mathsf T}M_g$。
第四步:计算 $C=M_f^{-1}M_g$(逐行×列,高亮):$M_f^{-1}=\begin{pmatrix}1&-1&0\\0&1&0\\0&0&\frac1{\sqrt3}\end{pmatrix}$;第1行×第1列:$1\cdot\sqrt2+(-1)\cdot0+0=\sqrt2$;第1行×第2列:$1\cdot0+(-1)\cdot\sqrt3+0=-\sqrt3$;第1行×第3列:$0$;第2行:$0,\sqrt3,0$;第3行:$0,0,\frac2{\sqrt3}$。
第五步:验证 $C^{\mathsf T}AC=B$(逐项行×列,高亮):先算 $AC$:第1行×第1列 $=\sqrt2$、第1行×第2列 $=0$、第2行×第2列 $=-\sqrt3+2\sqrt3=\sqrt3$、第3行×第3列 $=3\cdot\frac2{\sqrt3}=2\sqrt3$;再算 $C^{\mathsf T}(AC)$:对角依次为 $\sqrt2\cdot\sqrt2=2$、$\sqrt3\cdot\sqrt3=3$、$\frac2{\sqrt3}\cdot2\sqrt3=4$,非对角为零;得 $\operatorname{diag}(2,3,4)=B$ ✓。


## draft-c38-01

P: 设$M:\mathbb R^2\to\mathbb R^2$任意线性映射，在$\mathbb R^2\times\mathbb R^2$中取$U=\{(a,Ma)\}$、$V=\{(0,b)\}$。证明全空间是$U\oplus V$，求投影到$U$沿$V$的表达式及核、像、维数。

S: $(a,b)=(a,Ma)+(0,b-Ma)$，第一项属$U$、第二项属$V$，故和为全空间。若$(a,Ma)=(0,b)$，则$a=0,b=0$，交为零，分解唯一。投影$P(a,b)=(a,Ma)$，$P^2=P$，核$V$、像$U$，两者维数均$2$。不需要$M$可逆；图空间与竖直空间的互补来自第一坐标的唯一性。

A: $\mathbb R^4=U\oplus V$；$P(a,b)=(a,Ma)$，核$V$、像$U$，维数均$2$。

Objects: 题面卡:$U=\{(a,Ma)\}$、$V=\{(0,b)\}$ 的直和与投影 | 板书一:分解 $(a,b)=(a,Ma)+(0,b-Ma)$ 的逐项验证 | 高亮框:关键点——交为零来自第一坐标唯一性 | 板书二:$P^2=P$ 的两次作用代入与核像求解 | 结论卡:$\mathbb R^4=U\oplus V$,核 $V$、像 $U$,维数均 $2$

Steps:
第一步:和为全空间(逐项,高亮):任意 $(a,b)=(a,Ma)+(0,b-Ma)$;第一项 $(a,Ma)$ 属 $U$,第二项 $(0,b-Ma)$ 属 $V$。
第二步:交为零:若 $(a,Ma)=(0,b)$,第一坐标给 $a=0$,于是 $Ma=0$,再由第二坐标给 $b=0$;故交为 $\{0\}$,分解唯一。
第三步:投影 $P(a,b)=(a,Ma)$;两次作用(逐步,高亮):$P(P(a,b))=P(a,Ma)=(a,Ma)=P(a,b)$,故 $P^2=P$。
第四步:核(逐步):$P(a,b)=(0,0)$ 当且仅当 $a=0$(第一坐标),$b$ 任意;故 $\ker P=V$;像:$P$ 的值域即 $\{(a,Ma)\}=U$。
第五步:维数:$\dim U=\dim V=2$;不需要 $M$ 可逆——图空间与竖直空间互补来自第一坐标的唯一性(高亮)。


## draft-c38-02

P: 在$\mathbb R[x]_{\le4}$中，令$U$为偶多项式，$V$为被$(x-1)^2$整除的多项式。求$U\cap V$、$U+V$及维数，判断和是否直和。

S: $U=\operatorname{span}(1,x^2,x^4)$，维数$3$；$V=(x-1)^2\mathbb R[x]_{\le2}$，维数$3$。若$f=a+bx^2+cx^4\in V$，须$f(1)=f^{\prime}(1)=0$，即$a+b+c=0,2b+4c=0$，得$f=c(x^2-1)^2$。故交为该一维空间。和的维数$3+3-1=5$，等于环境维数，所以和为全部$\mathbb R[x]_{\le4}$。交非零，故不是直和。

A: 交$\operatorname{span}(x^2-1)^2$，维数$1$；和为五维全空间，非直和。

Objects: 题面卡:$U$ 偶多项式与 $V$ 被 $(x-1)^2$ 整除的空间 | 板书一:$f(1)=a+b+c=0$ 与 $f'(1)=2b+4c=0$ 的代入 | 高亮框:关键点——求导代入 $f'=2bx+4cx^3$ 在 $x=1$ | 消元板:$b=-2c$、$a=c$ 与展开 $c(x^2-1)^2$ | 结论卡:交维数 $1$,和 $=$ 全空间,非直和

Steps:
第一步:基底:$U=\operatorname{span}(1,x^2,x^4)$,维数 $3$;$V=(x-1)^2\mathbb R[x]_{\le2}$,维数 $3$。
第二步:交的方程:设 $f=a+bx^2+cx^4\in V$;须 $f(1)=0$:$a+b+c=0$;且 $f'(1)=0$(逐步求导,高亮):$f'=2bx+4cx^3$,代入 $x=1$ 得 $2b+4c=0$。
第三步:消元(逐步,高亮):$2b+4c=0$ 给 $b=-2c$;代入 $a+b+c=0$:$a-2c+c=0$ 给 $a=c$;故 $f=c-2cx^2+cx^4=c(1-2x^2+x^4)=c(x^2-1)^2$。
第四步:故 $U\cap V=\operatorname{span}((x^2-1)^2)$,维数 $1$。
第五步:和:$3+3-1=5$,等于环境维数,故 $U+V=\mathbb R[x]_{\le4}$;交非零 → 不是直和(高亮)。


## draft-c39-01

P: 在实$2\times2$矩阵空间中取$A=\operatorname{diag}(1,3)$，定义$T(X)=AX-XA$。求核、像、秩，并说明全空间能否分解为核与像的直和。

S: 对$X=\begin{pmatrix}a&b\\c&d\end{pmatrix}$，$T(X)=\begin{pmatrix}0&-2b\\2c&0\end{pmatrix}$。所以核为所有对角矩阵，基$e_{11},e_{22}$；像为所有零对角矩阵，基$e_{12},e_{21}$，秩$2$。两空间交为零且每个矩阵唯一分解为对角部分与零对角部分，故是直和。$T$在像上可逆，$T^2$在像上为$4I$，与在核上为零的作用不同；非正交Jordan中心化问题未被套用。

A: 核为对角矩阵，像为零对角矩阵，秩$2$；$M_2(\mathbb R)=\ker T\oplus\operatorname{im}T$。

Objects: 题面卡:$T(X)=AX-XA$,$A=\operatorname{diag}(1,3)$ | 板书一:$AX$ 与 $XA$ 的逐项乘法与相减 | 高亮框:关键点——$T(X)=\begin{pmatrix}0&-2b\\2c&0\end{pmatrix}$ 的得出 | 板书二:$T^2$ 在像上的逐项计算 | 结论卡:核=对角矩阵、像=零对角矩阵,直和,非正交投影

Steps:
第一步:逐项乘法(高亮):$AX=\operatorname{diag}(1,3)X=\begin{pmatrix}a&b\\3c&3d\end{pmatrix}$;$XA=\begin{pmatrix}a&3b\\c&3d\end{pmatrix}$;相减得 $T(X)=\begin{pmatrix}0&-2b\\2c&0\end{pmatrix}$。
第二步:核:$T(X)=0$ 当且仅当 $b=c=0$,即 $X$ 为对角矩阵;基 $e_{11},e_{22}$,维数 $2$。
第三步:像:零对角矩阵全体,基 $e_{12},e_{21}$,维数 $2$,故秩 $2$。
第四步:直和:每个矩阵唯一分解为对角部分加零对角部分,交为零;故 $M_2(\mathbb R)=\ker T\oplus\operatorname{im}T$(高亮)。
第五步:$T^2$ 在像上(逐步,高亮):$T(\begin{pmatrix}0&-2b\\2c&0\end{pmatrix})=\begin{pmatrix}0&2\cdot2b\\2\cdot2c&0\end{pmatrix}=\begin{pmatrix}0&4b\\4c&0\end{pmatrix}$;即 $T^2|_{\operatorname{im}T}=4I$;而在核上 $T=0$;分解非正交,不能把 $T$ 说成正交投影。


## draft-c39-03

P: 定义$T:\mathbb R[x]_{\le3}\to\mathbb R^3$，$Tf=(f(0),f(1),f(-1))$。求核、像与秩，给出证明满射的显式右逆。

S: 核中$f$在$0,1,-1$三个不同节点为零，因此被$x(x-1)(x+1)$整除；度数最多$3$，故核$\operatorname{span}(x^3-x)$。对$(a,b,c)\in\mathbb R^3$，定义$R(a,b,c)=a(1-x^2)+b x(x+1)/2+c x(x-1)/2$，三个节点的值依次为$a,b,c$，所以$TR=I$。故像为全部$\mathbb R^3$，秩$3$、核维数$1$，右逆证明满射不依赖仅报维数。

A: 核$\operatorname{span}(x^3-x)$；像$\mathbb R^3$、秩$3$；右逆$R(a,b,c)=a(1-x^2)+\frac b2x(x+1)+\frac c2x(x-1)$。

Objects: 题面卡:$T:\mathbb R[x]_{\le3}\to\mathbb R^3$,$Tf=(f(0),f(1),f(-1))$ | 板书一:因子定理——三节点为零 $\Rightarrow$ 被 $x(x-1)(x+1)$ 整除 | 高亮框:关键点——右逆 $R$ 的逐点代入验证 | 验证板:$x=0,1,-1$ 三处取值 $a,b,c$ | 结论卡:核 $\operatorname{span}(x^3-x)$,像 $\mathbb R^3$,秩 $3$

Steps:
第一步:核(关键点:因子定理,高亮):$f\in\ker T$ 当且仅当 $f$ 在 $0,1,-1$ 三点为零;由因子定理 $f$ 被 $x(x-1)(x+1)$ 整除;次数≤3 → $f=c\,x(x-1)(x+1)=c(x^3-x)$;故 $\ker T=\operatorname{span}(x^3-x)$,维数 $1$。
第二步:构造右逆:$R(a,b,c)=a(1-x^2)+b\frac{x(x+1)}2+c\frac{x(x-1)}2$。
第三步:逐点代入验证(高亮):$x=0$:$R=a(1-0)+0+0=a$;$x=1$:$R=0+b\cdot\frac{1\cdot2}2+0=b$;$x=-1$:$R=0+0+c\cdot\frac{(-1)(-2)}2=c$。
第四步:故 $TR=I_{\mathbb R^3}$,像为全部 $\mathbb R^3$,秩 $3$;与核维数 $4-3=1$ 一致。
第五步:结论:显式右逆证明满射,不依赖仅报维数(高亮)。


## draft-c40-01

P: 令$f=\lambda-1$，$A(\lambda)=\operatorname{diag}(f,f^2)$、$B(\lambda)=\operatorname{diag}(1,f^3)$。两矩阵行列式相同，判断是否多项式可逆等价；比较在有理函数域与代入实参数后的秩、核，说明行列式为何不足。

S: 两者行列式都为$f^3$，但一阶子式首一gcd分别为$f$与$1$，不变因子分别$f,f^2$与$1,f^3$，所以不unimodular等价。在有理函数域$\mathbb R(\lambda)$，$f$是可逆非零元素，两矩阵秩都为$2$、核都为零；在多项式环中核也都为零，因为环无零因子。在实数$a\ne1$代入时两者仍秩$2$、核零。代入$a=1$，$A(1)=0$，秩$0$、核$\mathbb R^2$；$B(1)=\operatorname{diag}(1,0)$，秩$1$、核$\operatorname{span}(e_2)$。同一行列式零点及其阶数不能确定特殊参数的核维数，通用域的核也不能直接代入当作特殊核。

A: 不等价；一般域及$a\ne1$均秩$2$，$a=1$时秩分别$0,1$；行列式相同不足以确定特殊核。

Objects: 题面卡:$A(\lambda)=\operatorname{diag}(f,f^2)$ 与 $B(\lambda)=\operatorname{diag}(1,f^3)$,$f=\lambda-1$ | 板书一:一阶子式集合 $\{f,f^2\}$ 与 $\{1,f^3\}$ 的首一 gcd | 高亮框:关键点——不变因子 $(f,f^2)$ 与 $(1,f^3)$ 不同,不等价 | 板书二:$a\ne1$ 与 $a=1$ 代入的秩核对照 | 结论卡:$a=1$ 时秩分别 $0,1$;行列式相同不足以确定核

Steps:
第一步:一阶子式(逐项,高亮):$A$ 的一阶子式集合为 $\{f,f^2\}$,首一 gcd $=f$;$B$ 的一阶子式集合为 $\{1,f^3\}$,首一 gcd $=1$。
第二步:不变因子:$A$:$d_1=f$,$d_2=f^3/f=f^2$,即 $(f,f^2)$;$B$:$d_1=1$,$d_2=f^3$,即 $(1,f^3)$;不同 → 不多项式可逆等价(行列式同为 $f^3$ 但不变因子不同,高亮)。
第三步:有理函数域 $\mathbb R(\lambda)$:$f=\lambda-1\ne0$ 是可逆元,两矩阵秩 $2$、核零;多项式环中核也零(环无零因子)。
第四步:代入(逐项):$a\ne1$ 时两者仍秩 $2$、核零;$a=1$ 时 $A(1)=\operatorname{diag}(0,0)=0$,秩 $0$、核 $\mathbb R^2$;$B(1)=\operatorname{diag}(1,0)$;解 $B(1)v=0$:第一分量 $v_1=0$、$v_2$ 自由,故 $\ker B(1)=\operatorname{span}(e_2)$,秩 $1$(高亮)。
第五步:结论:行列式相同不足以确定特殊参数下的核与秩(高亮)。


## draft-c40-04

P: 求 λ-矩阵 $A(\lambda)=\mathrm{diag}(\lambda+1,\,\lambda(\lambda+1),\,(\lambda+1)^2(\lambda-2))$ 的行列式因子、不变因子与初等因子。

S: 一阶行列式因子:$D_1=\gcd(\lambda+1,\lambda(\lambda+1),(\lambda+1)^2(\lambda-2))=\lambda+1$。二阶行列式因子:各二阶子式(对角情形即两两乘积)为 $\lambda(\lambda+1)^2$、$(\lambda+1)^3(\lambda-2)$、$\lambda(\lambda+1)^3(\lambda-2)$,最大公因式 $D_2=(\lambda+1)^2$。$D_3=\det=\lambda(\lambda+1)^4(\lambda-2)$。不变因子:$d_1=D_1=\lambda+1$;$d_2=\frac{D_2}{D_1}=\lambda+1$;$d_3=\frac{D_3}{D_2}=\lambda(\lambda+1)^2(\lambda-2)$。初等因子:$\lambda+1$、$\lambda+1$、$\lambda$、$(\lambda+1)^2$、$\lambda-2$。

A: $D_1=\lambda+1$,$D_2=(\lambda+1)^2$,$D_3=\lambda(\lambda+1)^4(\lambda-2)$;不变因子 $\lambda+1,\lambda+1,\lambda(\lambda+1)^2(\lambda-2)$;初等因子 $\lambda+1,\lambda+1,\lambda,(\lambda+1)^2,\lambda-2$。

Objects: 题面卡:$A(\lambda)=\operatorname{diag}(\lambda+1,\lambda(\lambda+1),(\lambda+1)^2(\lambda-2))$ 的因子 | 板书一:$D_1$ 取最小指数的逐项 gcd | 板书二:二阶子式(两两乘积)与 $D_2$ 的取最小指数 | 高亮框:关键点——$D_3$ 的对角元连乘展开 | 结论卡:$D_1=\lambda+1$,$D_2=(\lambda+1)^2$,$D_3=\lambda(\lambda+1)^4(\lambda-2)$

Steps:
第一步:一阶行列式因子(逐项 gcd,高亮):各对角元 $\lambda+1$、$\lambda(\lambda+1)$、$(\lambda+1)^2(\lambda-2)$;对每个根取最小指数:$D_1=\lambda+1$。
第二步:二阶子式(对角情形即两两乘积):$\lambda(\lambda+1)^2$、$(\lambda+1)^3(\lambda-2)$、$\lambda(\lambda+1)^3(\lambda-2)$;逐项取最小指数:$D_2=(\lambda+1)^2$(高亮)。
第三步:三阶:$D_3=\det A=(\lambda+1)\cdot\lambda(\lambda+1)\cdot(\lambda+1)^2(\lambda-2)=\lambda(\lambda+1)^4(\lambda-2)$(逐步连乘,高亮)。
第四步:不变因子(逐步比值):$d_1=D_1=\lambda+1$;$d_2=D_2/D_1=\lambda+1$;$d_3=D_3/D_2=\lambda(\lambda+1)^2(\lambda-2)$。
第五步:初等因子:把各不变因子分解为互异根幂:$\lambda+1$、$\lambda+1$、$\lambda$、$(\lambda+1)^2$、$\lambda-2$(高亮结论)。


## draft-c42-02

P: 令$R_x=\begin{pmatrix}1&0&0\\0&0&-1\\0&1&0\end{pmatrix}$、$R_y=\begin{pmatrix}0&0&1\\0&1&0\\-1&0&0\end{pmatrix}$。求两个乘积并说明三维不同轴旋转为何不交换，给两乘积的轴与精确角。

S: $R_xR_y=\begin{pmatrix}0&0&1\\1&0&0\\0&1&0\end{pmatrix}$，$R_yR_x=\begin{pmatrix}0&1&0\\0&0&-1\\-1&0&0\end{pmatrix}$，不同。两者均正交、行列式$1$、迹$0$，由$\operatorname{tr}R=1+2\cos\theta$得$\theta=2\pi/3$。固定向量分别为$(1,1,1)$、$(1,1,-1)$；反对称部分的轴向量分别正比于这两个向量，因$\sin(2\pi/3)>0$，取对应单位向量即给右手角$2\pi/3$。不同轴使作用顺序改变结果，不能把平面旋转角相加律直接用于三维。

A: 两个乘积不同，轴分别$(1,1,1)/\sqrt3$与$(1,1,-1)/\sqrt3$，右手角均$2\pi/3$。

Objects: 矩阵卡:$R_x=\begin{pmatrix}1&0&0\\0&0&-1\\0&1&0\end{pmatrix}$、$R_y=\begin{pmatrix}0&0&1\\0&1&0\\-1&0&0\end{pmatrix}$ | 行×列计算板:$R_xR_y$ 与 $R_yR_x$ 的九项分量乘积 | 高亮框:关键点——迹 $0$ 与 $\operatorname{tr}R=1+2\cos\theta$ 给 $\theta=\frac{2\pi}3$ | 固定向量板:解 $(R-I)x=0$ 得轴方向 | 结论卡:两乘积不同,轴 $(1,1,1)$ 与 $(1,1,-1)$,角均 $\frac{2\pi}3$

Steps:
第一步:计算 $R_xR_y$(逐行×列,高亮):第1行×第1列:$1\cdot0+0\cdot0+0\cdot(-1)=0$;第1行×第2列:$0$;第1行×第3列:$1\cdot1=1$;第2行×第1列:$0+0+(-1)(-1)=1$;第2行×第2列:$0$;第2行×第3列:$0$;第3行×第1列:$0$;第3行×第2列:$1\cdot1=1$;第3行×第3列:$0$;得 $R_xR_y=\begin{pmatrix}0&0&1\\1&0&0\\0&1&0\end{pmatrix}$。
第二步:计算 $R_yR_x$(逐行×列,高亮):第1行×第1列:$0$;第1行×第2列:$1\cdot1=1$;第1行×第3列:$0$;第2行×第1列:$0$;第2行×第2列:$0$;第2行×第3列:$1\cdot(-1)=-1$;第3行×第1列:$(-1)\cdot1=-1$;第3行×第2列:$0$;第3行×第3列:$0$;得 $R_yR_x=\begin{pmatrix}0&1&0\\0&0&-1\\-1&0&0\end{pmatrix}$。
第三步:两乘积不同(高亮);两者均正交、行列式 $1$、迹 $0$;由 $\operatorname{tr}R=1+2\cos\theta$:$\cos\theta=-\frac12$,即 $\theta=\frac{2\pi}3$。
第四步:求固定向量(逐步,高亮):解 $(R_xR_y-I)x=0$:$\begin{pmatrix}-1&0&1\\1&-1&0\\0&1&-1\end{pmatrix}x=0$ 给 $x_1=x_3,x_2=x_3$,固定向量方向 $(1,1,1)$;同理 $(R_yR_x-I)x=0$ 给 $(1,1,-1)$。
第五步:结论:轴分别为 $(1,1,1)/\sqrt3$ 与 $(1,1,-1)/\sqrt3$,右手角均为 $\frac{2\pi}3$;三维不同轴旋转不交换(高亮)。
