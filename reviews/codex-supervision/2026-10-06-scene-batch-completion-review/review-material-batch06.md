# Batch 6 independent review material


## draft-c29-05

P: 证明三次多项式的根与系数关系(韦达定理)，并构造一个以 $2$、$-1$、$\frac12$ 为根的首一三次多项式。

S: 设首一三次多项式 $f(x)=x^3+px^2+qx+r$ 的根为 $\alpha,\beta,\gamma$,则 $f(x)=(x-\alpha)(x-\beta)(x-\gamma)$。展开右边:$x^3-(\alpha+\beta+\gamma)x^2+(\alpha\beta+\beta\gamma+\gamma\alpha)x-\alpha\beta\gamma$。比较系数得韦达定理:$\alpha+\beta+\gamma=-p$,$\alpha\beta+\beta\gamma+\gamma\alpha=q$,$\alpha\beta\gamma=-r$。构造:以 $2,-1,\frac12$ 为根,则 $f(x)=(x-2)(x+1)(x-\frac12)$。展开:$(x^2-x-2)(x-\frac12)=x^3-x^2-2x-\frac12x^2+\frac12x+1=x^3-\frac32x^2-\frac32x+1$。

A: 韦达定理:根和 $=-p$,两两积和 $=q$,根积 $=-r$;构造:$f=x^3-\frac32x^2-\frac32x+1$。

Objects: 题面卡:三次韦达定理与构造题 | 板书一:逐步相乘 $(x-\alpha)(x-\beta)=x^2-(\alpha+\beta)x+\alpha\beta$ 再乘 $(x-\gamma)$ 的逐项合并 | 高亮框:关键点——两两积和项 $\alpha\beta+\beta\gamma+\gamma\alpha$ 的来源 | 板书二:系数比较 $\alpha+\beta+\gamma=-p$ 等三条 | 构造板:根 $2,-1,\frac12$ 的三项代入与验证

Steps:
第一步:设首一三次多项式 $f(x)=x^3+px^2+qx+r$ 的根为 $\alpha,\beta,\gamma$,则 $f(x)=(x-\alpha)(x-\beta)(x-\gamma)$。
第二步:逐步相乘(高亮):先 $(x-\alpha)(x-\beta)=x^2-(\alpha+\beta)x+\alpha\beta$;再乘 $(x-\gamma)$:$(x^2-(\alpha+\beta)x+\alpha\beta)(x-\gamma)=x^3-(\alpha+\beta)x^2+\alpha\beta x-\gamma x^2+\gamma(\alpha+\beta)x-\alpha\beta\gamma=x^3-(\alpha+\beta+\gamma)x^2+(\alpha\beta+\beta\gamma+\gamma\alpha)x-\alpha\beta\gamma$(关键点:$x$ 项来自 $\alpha\beta+\gamma\alpha+\gamma\beta$,即两两积和)。
第三步:比较系数:$x^2$ 项:$\alpha+\beta+\gamma=-p$;$x$ 项:$\alpha\beta+\beta\gamma+\gamma\alpha=q$;常数项:$\alpha\beta\gamma=-r$。
第四步:构造(逐步代入):根 $2,-1,\frac12$:根和 $=2-1+\frac12=\frac32$,故 $p=-\frac32$;两两积和 $=2\cdot(-1)+(-1)\cdot\frac12+\frac12\cdot2=-2-\frac12+1=-\frac32$,故 $q=-\frac32$;根积 $=2\cdot(-1)\cdot\frac12=-1$,故 $r=1$。
第五步:故 $f(x)=x^3-\frac32x^2-\frac32x+1$;验证 $x=2$:$8-6-3+1=0$ ✓(高亮结论)。


## draft-c30-01

P: 求次数不超过$5$、在$x=1$至少有三重零点、在$x=2$至少有二重零点且$f(0)=1$的全部实多项式，并写成$x-1$的幂。

S: 零点重数给$(x-1)^3(x-2)^2\mid f$。由次数上界，$f=c(x-1)^3(x-2)^2$；$f(0)=1$给$-4c=1$，即$c=-1/4$。令$u=x-1$，则$f=-u^3(u-1)^2/4=-u^5/4+u^4/2-u^3/4$。因为$c\ne0$且两个因子互素，重数分别恰为$3$与$2$。所有条件均验证，且常数被唯一确定，故解唯一。

A: $f=-\frac14(x-1)^3(x-2)^2=-\frac14(x-1)^5+\frac12(x-1)^4-\frac14(x-1)^3$，唯一。

Objects: 题面卡:三重零点 $x=1$、二重零点 $x=2$、$f(0)=1$ | 板书一:$f=c(x-1)^3(x-2)^2$ 的因子依据 | 高亮框:关键点——$f(0)=c(-1)^3(-2)^2=-4c=1$ 的代入 | 平移展开板:$(u-1)^2=u^2-2u+1$ 与逐项乘除 | 结论卡:$f=-\frac{u^5}4+\frac{u^4}2-\frac{u^3}4$,解唯一

Steps:
第一步:零点重数给 $(x-1)^3(x-2)^2\mid f$;由次数不超过 $5$,得 $f=c(x-1)^3(x-2)^2$。
第二步:代入(逐步,高亮):$f(0)=c(-1)^3(-2)^2=c\cdot(-1)\cdot4=-4c$;条件 $f(0)=1$ 给 $-4c=1$,即 $c=-\frac14$。
第三步:换元 $u=x-1$:则 $(x-2)^2=(u-1)^2=u^2-2u+1$(逐项展开)。
第四步:逐项相乘:$f=-\frac14u^3(u^2-2u+1)=-\frac14(u^5-2u^4+u^3)=-\frac{u^5}4+\frac{u^4}2-\frac{u^3}4$(高亮)。
第五步:唯一性(关键点):$c\ne0$ 且两个因子互素,故重数分别恰为 $3$ 与 $2$;常数被唯一确定,解唯一(高亮)。


## draft-c30-03

P: 在次数不超过$3$的实多项式空间上定义$\Delta f(x)=f(x+1)-f(x)$。证明$\Delta^4=0$但$\Delta^3\ne0$，并求满足$\Delta f=3x^2+5x+2$、$f(0)=2$的全部$f$。

S: 若$f$非恒定且次数为$m$，首项系数为$c\ne0$，二项式展开给$\Delta f$的次数恰为$m-1$，首项系数为$mc$。因此在该四维空间上$\Delta^4=0$；且$\Delta^3(x^3)=6\ne0$，指数恰为$4$。设$f=ax^3+bx^2+cx+d$，则$\Delta f=3ax^2+(3a+2b)x+(a+b+c)$。与目标比较得$a=1,b=1,c=0$，而$f(0)=2$给$d=2$。故$f=x^3+x^2+2$。若两个解存在，其差被$\Delta$消去；降阶结论说明差为常数，归一化又给常数为零，故唯一。

A: $\Delta^4=0,\Delta^3(x^3)=6$；唯一$f=x^3+x^2+2$。

Objects: 题面卡:$\Delta f(x)=f(x+1)-f(x)$ 在次数≤3空间上 | 板书一:二项式展开 $(x+1)^m=x^m+mx^{m-1}+\cdots$ 与首项抵消 | 高亮框:关键点——$x^{m-1}$ 项系数 $mc\ne0$ 来自哪一项 | 板书二:$\Delta(x^3)=3x^2+3x+1$ 等逐项差分 | 比较板:方程组 $3a=3$、$3a+2b=5$、$a+b+c=2$ 的逐步回代

Steps:
第一步:降阶证明(逐步,高亮):设 $f$ 首项 $cx^m$;二项式展开 $(x+1)^m=x^m+mx^{m-1}+\cdots$;$\Delta f$ 中 $x^m$ 项 $c-c=0$ 抵消;而 $x^{m-1}$ 项仅由 $c(x+1)^m$ 展开贡献,系数为 $mc\ne0$(关键点:只有 $(x+1)^m$ 的 $mx^{m-1}$ 项贡献 $x^{m-1}$ 系数);故 $\deg\Delta f=m-1$。
第二步:在次数≤3空间上连续四次 $\Delta$ 必降为 $0$:$\Delta^4=0$;且 $\Delta^3(x^3)=3\cdot2\cdot1=6\ne0$(三次降阶后为常数),故指数恰为 $4$(高亮)。
第三步:设 $f=ax^3+bx^2+cx+d$;逐项差分(高亮):$\Delta(x^3)=(x+1)^3-x^3=3x^2+3x+1$;$\Delta(x^2)=2x+1$;$\Delta x=1$;$\Delta1=0$;故 $\Delta f=3ax^2+(3a+2b)x+(a+b+c)$。
第四步:比较系数(逐步回代,高亮):$3a=3$ → $a=1$;$3a+2b=5$ → $3+2b=5$ → $b=1$;$a+b+c=2$ → $1+1+c=2$ → $c=0$。
第五步:$f(0)=2$ 给 $d=2$;故 $f=x^3+x^2+2$;若另有一解,差满足 $\Delta g=0$ 且 $g(0)=0$,只能 $g=0$,解唯一(高亮)。


## draft-c31-03

P: 用克拉默法则求方程组 $\begin{cases}x+y+z=1\\ x+y+2z=2\\ x+2y+az=3\end{cases}$ 的解，并说明解与参数 $a$ 的关系。

S: 系数行列式 $D=\begin{vmatrix}1&1&1\\1&1&2\\1&2&a\end{vmatrix}=1\times(a-4)-1\times(a-2)+1\times(2-1)=-1$,与 $a$ 无关且非零,故对一切 $a$ 都有唯一解。$D_x=\begin{vmatrix}1&1&1\\2&1&2\\3&2&a\end{vmatrix}=1\times(a-4)-1\times(2a-6)+1\times(4-3)=-a+3$;$D_y=\begin{vmatrix}1&1&1\\1&2&2\\1&3&a\end{vmatrix}=1\times(2a-6)-1\times(a-2)+1\times(3-2)=a-3$;$D_z=\begin{vmatrix}1&1&1\\1&1&2\\1&2&3\end{vmatrix}=1\times(3-4)-1\times(3-2)+1\times(2-1)=-1$。故 $x=\frac{-a+3}{-1}=a-3$,$y=\frac{a-3}{-1}=3-a$,$z=\frac{-1}{-1}=1$。验证:$x+y+z=(a-3)+(3-a)+1=1$;$x+y+2z=0+2=2$;$x+2y+az=(a-3)+2(3-a)+a=3$。

A: $D=-1$ 与 $a$ 无关,对一切 $a$ 有唯一解 $x=a-3$,$y=3-a$,$z=1$。

Objects: 方程组卡:$x+y+z=1$、$x+y+2z=2$、$x+2y+az=3$ | 板书一:$D$ 按第一行展开的余子式逐项 | 板书二:$D_x,D_y,D_z$ 三个替换行列式的逐项展开 | 高亮框:关键点——$D=-1$ 与 $a$ 无关,对一切 $a$ 唯一解 | 结论卡:$x=a-3$,$y=3-a$,$z=1$

Steps:
第一步:系数行列式(按第一行展开,逐项,高亮):$D=\begin{vmatrix}1&1&1\\1&1&2\\1&2&a\end{vmatrix}=1\cdot(a-4)-1\cdot(a-2)+1\cdot(2-1)=a-4-a+2+1=-1$;与 $a$ 无关且非零 → 对一切 $a$ 有唯一解。
第二步:$D_x$(逐项展开):$\begin{vmatrix}1&1&1\\2&1&2\\3&2&a\end{vmatrix}=1\cdot(a-4)-1\cdot(2a-6)+1\cdot(4-3)=a-4-2a+6+1=-a+3$。
第三步:$D_y$(逐项展开):$\begin{vmatrix}1&1&1\\1&2&2\\1&3&a\end{vmatrix}=1\cdot(2a-6)-1\cdot(a-2)+1\cdot(3-2)=2a-6-a+2+1=a-3$。
第四步:$D_z$(逐项展开):$\begin{vmatrix}1&1&1\\1&1&2\\1&2&3\end{vmatrix}=1\cdot(3-4)-1\cdot(3-2)+1\cdot(2-1)=-1-1+1=-1$。
第五步:克拉默公式(逐步比值,高亮):$x=\frac{D_x}D=\frac{-a+3}{-1}=a-3$;$y=\frac{D_y}D=\frac{a-3}{-1}=3-a$;$z=\frac{D_z}D=\frac{-1}{-1}=1$。


## draft-c31-04

P: 用克拉默法则解方程组 $\begin{cases}kx+y=1\\ x+ky=k\end{cases}$($k$ 为参数),并讨论奇异情形($D=0$)时的解。

S: $D=k^2-1=(k-1)(k+1)$。当 $k\neq\pm1$ 时,$D_x=\begin{vmatrix}1&1\\k&k\end{vmatrix}=k-k=0$,$D_y=\begin{vmatrix}k&1\\1&k\end{vmatrix}=k^2-1$,故唯一解 $x=\frac{0}{D}=0$,$y=\frac{D}{D}=1$。当 $k=1$ 时,两方程均为 $x+y=1$,无穷多解。当 $k=-1$ 时,方程为 $-x+y=1$ 与 $x-y=-1$,后者乘以 $-1$ 恰为前者,仍是同一条直线,无穷多解。注意:本题两个奇异值均落在无穷多解分支,与常见的「一个奇异值无解、另一个无穷多解」的例子不同;克拉默法则仅在 $D\neq0$ 时适用,$D=0$ 时必须改用初等变换/秩判断。

A: $k\neq\pm1$ 时唯一解 $x=0,y=1$;$k=1$ 与 $k=-1$ 时均有无穷多解(两方程退化为同一直线)。

Objects: 方程组卡:$kx+y=1$、$x+ky=k$ | 板书一:$D=k^2-1=(k-1)(k+1)$ 的对角乘积相减 | 高亮框:关键点——$D_x=1\cdot k-k\cdot1=0$、$D_y=k^2-1$ 的分量乘积 | 比值板:$x=\frac0D=0$、$y=\frac DD=1$ | 奇异讨论卡:$k=1$ 与 $k=-1$ 的退化方程

Steps:
第一步:系数行列式(对角乘积相减,高亮):$D=\begin{vmatrix}k&1\\1&k\end{vmatrix}=k\cdot k-1\cdot1=k^2-1=(k-1)(k+1)$。
第二步:$k\ne\pm1$ 时(逐项):$D_x=\begin{vmatrix}1&1\\k&k\end{vmatrix}=1\cdot k-1\cdot k=0$;$D_y=\begin{vmatrix}k&1\\1&k\end{vmatrix}=k\cdot k-1\cdot1=k^2-1=D$(高亮)。
第三步:比值(逐步代入):$x=\frac{D_x}D=\frac0D=0$;$y=\frac{D_y}D=\frac DD=1$。
第四步:$k=1$:两方程均为 $x+y=1$,退化为同一直线,无穷多解(高亮)。
第五步:$k=-1$:方程为 $-x+y=1$ 与 $x-y=-1$;第二个是第一个的 $-1$ 倍,同一直线,无穷多解(高亮结论)。


## draft-c31-05

P: 证明:若 $n$ 阶系数矩阵 $A$ 的行列式 $D=\det A\neq0$,则线性方程组 $AX=b$ 有唯一解,且解由克拉默公式给出:$x_j=\frac{D_j}{D}$,其中 $D_j$ 是把 $A$ 的第 $j$ 列换成 $b$ 所得的行列式。

S: 记 $A_{ij}$ 为代数余子式,伴随矩阵 $\mathrm{adj}(A)=(A_{ji})$。由行列式按行展开,$(A\,\mathrm{adj}(A))_{ij}=\sum_{k=1}^{n}a_{ik}A_{jk}=\begin{cases}\det A,&i=j\\0,&i\neq j\end{cases}$(异行展开为零),即 $A\,\mathrm{adj}(A)=D\,I$。因 $D\neq0$,$A^{-1}=\frac{1}{D}\mathrm{adj}(A)$ 存在,故 $AX=b$ 有唯一解 $X=A^{-1}b=\frac{1}{D}\mathrm{adj}(A)b$。第 $j$ 个分量 $x_j=\frac{1}{D}\sum_{i=1}^{n}b_iA_{ij}$,而 $\sum_{i=1}^{n}b_iA_{ij}$ 恰是按第 $j$ 列展开的、第 $j$ 列为 $b$ 的行列式 $D_j$,故 $x_j=\frac{D_j}{D}$。

A: 证明见解法;核心:$A\,\mathrm{adj}(A)=D\,I$(按行展开+异行展开为零),$D\neq0$ 时 $X=\frac{1}{D}\mathrm{adj}(A)b$,第 $j$ 分量为 $D_j/D$。

Objects: 题面卡:克拉默公式的证明 | 板书一:$(A\,\mathrm{adj}(A))_{ij}=\sum_{k=1}^na_{ik}A_{jk}$ 的第i行×第j列书写 | 高亮框:关键点——$i=j$ 按行展开得 $D$;$i\ne j$ 异行展开为 $0$ | 板书二:$A^{-1}=\frac1D\mathrm{adj}(A)$ 与解的表达式 | 结论卡:$x_j=\frac{D_j}D$

Steps:
第一步:记 $A_{ij}$ 为代数余子式,伴随矩阵 $\mathrm{adj}(A)=(A_{ji})$(注意转置排列,高亮)。
第二步:第 $i$ 行×第 $j$ 列(高亮书写):$(A\,\mathrm{adj}(A))_{ij}=\sum_{k=1}^na_{ik}A_{jk}$。
第三步:分两种情形(关键点):$i=j$ 时是第 $i$ 行按行展开:$\sum_ka_{ik}A_{ik}=\det A=D$;$i\ne j$ 时是异行展开:$\sum_ka_{ik}A_{jk}=0$(引用按行展开公式与异行展开为零,高亮)。
第四步:故 $A\,\mathrm{adj}(A)=DI$;因 $D\ne0$,得 $A^{-1}=\frac1D\mathrm{adj}(A)$;方程组解为 $x=A^{-1}b$。
第五步:第 $j$ 个分量(逐步,高亮):$x_j=\frac1D\sum_k(\mathrm{adj}(A))_{jk}b_k=\frac1D\sum_kA_{kj}b_k=\frac{D_j}D$($D_j$ 是把第 $j$ 列换成 $b$ 后按第 $j$ 列展开的行列式)。


## draft-c32-02

P: 求$V=\{x\in\mathbb R^4:\sum_{i=0}^3x_i=0,\ \sum_{i=0}^3i x_i=0\}$的基与维数，证明给出的基张成全部解。

S: 约束行$(1,1,1,1)$与$(0,1,2,3)$不成比例，秩$2$，故维数$2$。向量$v=(1,-2,1,0)$与$w=(0,1,-2,1)$同时满足两个约束，且由首末坐标可知独立。也可对任意解先取$x_0v+x_3w$，减去后首末坐标为零，剩余两坐标满足$y_1+y_2=0,y_1+2y_2=0$，故全零，证明张成。

A: 基$(1,-2,1,0),(0,1,-2,1)$，维数$2$。

Objects: 题面卡:$V=\{x\in\mathbb R^4:\sum x_i=0,\sum ix_i=0\}$ | 板书一:约束行 $(1,1,1,1)$ 与 $(0,1,2,3)$ 的秩判断 | 高亮框:关键点——$v,w$ 代入两个约束的逐项验算 | 消元板:$y_1+y_2=0$ 与 $y_1+2y_2=0$ 的求解 | 结论卡:基 $(1,-2,1,0),(0,1,-2,1)$,维数 $2$

Steps:
第一步:约束行 $(1,1,1,1)$ 与 $(0,1,2,3)$ 不成比例,秩为 $2$;故 $\dim V=4-2=2$。
第二步:验证 $v=(1,-2,1,0)$(逐项,高亮):$\sum x_i=1-2+1+0=0$;$\sum ix_i=0\cdot1+1\cdot(-2)+2\cdot1+3\cdot0=0$;$w=(0,1,-2,1)$:$\sum x_i=0+1-2+1=0$;$\sum ix_i=0+1\cdot1+2\cdot(-2)+3\cdot1=0$。
第三步:独立性(高亮):若 $c_1v+c_2w=0$,首坐标给 $c_1=0$,末坐标给 $c_2=0$;故 $v,w$ 线性无关。
第四步:张成(逐步):任取解 $y$;作 $y-x_0v-x_3w$,其首末坐标都变为零。
第五步:剩余两坐标满足 $y_1+y_2=0$ 与 $y_1+2y_2=0$;消元(高亮):两式相减得 $y_2=0$,回代得 $y_1=0$;故差为零,即 $y=x_0v+x_3w$,$v,w$ 张成全部解。


## draft-c34-01

P: 设 $E=\begin{pmatrix}1&0&0\\0&1&0\\0&0&5\end{pmatrix}$。说明用 $E$ 左乘与右乘一个 $3$ 阶矩阵 $A$ 分别对 $A$ 做了什么操作。

S: 左乘 $EA$:把 $A$ 的第三行乘以 $5$(其余行不变)。右乘 $AE$:把 $A$ 的第三列乘以 $5$(其余列不变)。$E$ 是由单位矩阵把第三行(列)乘以 $5$ 得到的倍乘型初等矩阵。

A: 左乘:第三行乘 $5$;右乘:第三列乘 $5$。

Objects: 矩阵卡:$E=\begin{pmatrix}1&0&0\\0&1&0\\0&0&5\end{pmatrix}$ 与符号元矩阵 $A=(a_{ij})$ | 板书一:$(EA)_{ij}=\sum_kE_{ik}A_{kj}$ 的行×列机制 | 高亮框:关键点——$E$ 仅对角元非零,故 $(EA)_{3j}=5A_{3j}$、$(AE)_{i3}=5A_{i3}$ | 演示板:左乘后第三行乘 5、右乘后第三列乘 5 的逐元素对照 | 结论卡:倍乘型初等矩阵;左乘行操作、右乘列操作

Steps:
第一步:行×列机制(高亮):$(EA)_{ij}=\sum_kE_{ik}A_{kj}$;因 $E$ 仅对角元非零($E_{11}=E_{22}=1,E_{33}=5$)。
第二步:左乘逐项:$i\ne3$ 时 $(EA)_{ij}=1\cdot A_{ij}=A_{ij}$,其余行不变;$i=3$ 时 $(EA)_{3j}=5\cdot A_{3j}$,第三行乘以 $5$(高亮)。
第三步:右乘逐项:$(AE)_{ij}=\sum_kA_{ik}E_{kj}$;$j\ne3$ 时 $(AE)_{ij}=A_{ij}$;$j=3$ 时 $(AE)_{i3}=5\cdot A_{i3}$,第三列乘以 $5$(高亮)。
第四步:符号元演示(逐元素):左乘后 $EA=\begin{pmatrix}a_{11}&a_{12}&a_{13}\\a_{21}&a_{22}&a_{23}\\5a_{31}&5a_{32}&5a_{33}\end{pmatrix}$;右乘后 $AE=\begin{pmatrix}a_{11}&a_{12}&5a_{13}\\a_{21}&a_{22}&5a_{23}\\a_{31}&a_{32}&5a_{33}\end{pmatrix}$(逐格对照)。
第五步:结论:$E$ 是单位矩阵把第三行(列)乘以 $5$ 得到的倍乘型初等矩阵;左乘作用于行、右乘作用于列(高亮)。


## draft-c34-02

P: 构造把 $3$ 阶矩阵的第二行加到第一行的初等矩阵 $E$，并求 $E^{-1}$ 与 $E^{-1}$ 对应的操作。

S: 把第二行加到第一行的初等矩阵为 $E=\begin{pmatrix}1&1&0\\0&1&0\\0&0&1\end{pmatrix}$(左乘 $EA$ 即第一行加第二行)。其逆为把第一行减去第二行:$E^{-1}=\begin{pmatrix}1&-1&0\\0&1&0\\0&0&1\end{pmatrix}$。验证:$EE^{-1}=I$(第一行:$(1,1,0)$ 减第二行 $(0,1,0)$ 得 $(1,0,0)$)。

A: $E=\begin{pmatrix}1&1&0\\0&1&0\\0&0&1\end{pmatrix}$;$E^{-1}=\begin{pmatrix}1&-1&0\\0&1&0\\0&0&1\end{pmatrix}$,对应「第一行减第二行」。

Objects: 构造卡:把第二行加到第一行的初等矩阵 $E$ | 板书一:$EA$ 第1行 $=1\cdot A_{1j}+1\cdot A_{2j}$ 的行×列机制 | 高亮框:关键点——$E^{-1}$ 对应第一行减去第二行 | 验证板:$EE^{-1}=I$ 的九项分量乘积 | 结论卡:$E$ 与 $E^{-1}$ 的矩阵

Steps:
第一步:构造机制(高亮):要求 $(EA)_{1j}=\sum_kE_{1k}A_{kj}=1\cdot A_{1j}+1\cdot A_{2j}=$ 第1行+第2行;故 $E=\begin{pmatrix}1&1&0\\0&1&0\\0&0&1\end{pmatrix}$。
第二步:逆操作:把第一行减去第二行,即 $E^{-1}=\begin{pmatrix}1&-1&0\\0&1&0\\0&0&1\end{pmatrix}$。
第三步:验证第1行(逐行×列,高亮):第1行×第1列:$1\cdot1+1\cdot0+0\cdot0=1$;第1行×第2列:$1\cdot(-1)+1\cdot1+0\cdot0=0$;第1行×第3列:$0$。
第四步:验证第2、3行(逐项):第2行×各列:$0\cdot1+1\cdot0+0=0$、$0\cdot(-1)+1\cdot1+0=1$、$0$;第3行×各列:$0,0,1\cdot1$;得 $EE^{-1}=I$(高亮)。
第五步:结论:$E^{-1}$ 对应的操作是「把第一行减去第二行」(高亮)。


## draft-c34-03

P: 先交换第一、二行，再将第一行乘以$2$。写出这一复合行变换的矩阵（初等矩阵的乘积），并验证作用顺序。

S: $P_1=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}$,$P_2=\begin{pmatrix}2&0&0\\0&1&0\\0&0&1\end{pmatrix}$。先做 $P_1$ 后做 $P_2$ 对应左乘 $P_2P_1$(先作用的矩阵写在右边):$P_2P_1=\begin{pmatrix}2&0&0\\0&1&0\\0&0&1\end{pmatrix}\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}=\begin{pmatrix}0&2&0\\1&0&0\\0&0&1\end{pmatrix}$。复合矩阵把第二行换到第一行并乘以 $2$。

A: 复合变换矩阵为$\begin{pmatrix}0&2&0\\1&0&0\\0&0&1\end{pmatrix}$，它是两个初等矩阵的乘积。

Objects: 操作卡:先交换第一、二行,再将(新的)第一行乘以 $2$ | 矩阵卡:$P_1=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}$、$P_2=\begin{pmatrix}2&0&0\\0&1&0\\0&0&1\end{pmatrix}$ | 高亮框:关键点——先作用的矩阵写在右边:复合为 $P_2P_1$ | 行×列计算板:$P_2P_1$ 的九项分量乘积 | 作用演示板:对符号元矩阵逐步做两次行变换并对照

Steps:
第一步:写出 $P_1=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}$(交换1、2行),$P_2=\begin{pmatrix}2&0&0\\0&1&0\\0&0&1\end{pmatrix}$(第1行乘2)。
第二步:顺序(关键点,高亮):先做 $P_1$ 后做 $P_2$,对应左乘 $P_2P_1$——先作用的矩阵写在右边。
第三步:乘法(逐行×列,高亮):第1行 $(2,0,0)$:×第1列 $(0,1,0)^{\mathsf T}=2\cdot0+0\cdot1+0\cdot0=0$;×第2列 $(1,0,0)^{\mathsf T}=2\cdot1=2$;×第3列 $=0$;第2行 $(0,1,0)$:×第1列 $=1$、×第2列 $=0$、×第3列 $=0$;第3行:×第3列 $=1$;得 $P_2P_1=\begin{pmatrix}0&2&0\\1&0&0\\0&0&1\end{pmatrix}$。
第四步:作用验证(逐步):对 $A=\begin{pmatrix}a&b&c\\d&e&f\\g&h&i\end{pmatrix}$:先 $P_1A=\begin{pmatrix}d&e&f\\a&b&c\\g&h&i\end{pmatrix}$(交换1、2行);再 $P_2(P_1A)=\begin{pmatrix}2d&2e&2f\\a&b&c\\g&h&i\end{pmatrix}$(第1行乘2);与 $(P_2P_1)A$ 一致(高亮)。
第五步:结论:复合行变换矩阵为 $P_2P_1=\begin{pmatrix}0&2&0\\1&0&0\\0&0&1\end{pmatrix}$,先交换第一、二行,再把新的第一行乘以 $2$(高亮)。
