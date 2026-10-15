## draft-c27-01

problem

设$n\ge2$、$u,v\in\mathbb R^n$均非零，$A=I+uv^{\mathsf T}$。用$\alpha=v^{\mathsf T}u$分类其可对角化性并求最小多项式；必须处理$\alpha=0$而$uv^{\mathsf T}\ne0$的情况。

solution

记$N=uv^{\mathsf T}\ne0$，则$N^2=\alpha N$。若$\alpha\ne0$，$\ker v^{\mathsf T}$维数$n-1$，$u$不在其中，全空间分解为该超平面与$\operatorname{span}(u)$的直和；$A$分别作用为$1$和$1+\alpha$，两个不同特征值都出现，所以可对角化，最小多项式$(\lambda-1)(\lambda-1-\alpha)$。若$\alpha=0$，$N^2=0$但$N\ne0$，$A$仅有特征值$1$，最小多项式为$(\lambda-1)^2$；若可对角化只能是$I$，与$N\ne0$矛盾。因此非零向量产生的零内积边界导致不可对角化。

answer

$\alpha\ne0$可对角化，最小多项式$(\lambda-1)(\lambda-1-\alpha)$；$\alpha=0$不可，最小多项式$(\lambda-1)^2$。

scene_spec.objects[0]

设$n\ge2$、$u,v\in\mathbb R^n$均非零，$A=I+uv^{\mathsf T}$。用$\alpha=v^{\mathsf T}u$分类其可对角化性并求最小多项式；必须处理$\alpha=0$而$uv^{\mathsf T}\ne0$的情况。

scene_spec.objects[1]

$\alpha\ne0$可对角化，最小多项式$(\lambda-1)(\lambda-1-\alpha)$；$\alpha=0$不可，最小多项式$(\lambda-1)^2$。

scene_spec.steps[0]

第一步:记$N=uv^{\mathsf T}\ne0$，则$N^2=\alpha N$。

scene_spec.steps[1]

第二步:若$\alpha\ne0$，$\ker v^{\mathsf T}$维数$n-1$，$u$不在其中，全空间分解为该超平面与$\operatorname{span}(u)$的直和；$A$分别作用为$1$和$1+\alpha$，两个不同特征值都出现，所以可对角化，最小多项式$(\lambda-1)(\lambda-1-\alpha)$。

scene_spec.steps[2]

第三步:若$\alpha=0$，$N^2=0$但$N\ne0$，$A$仅有特征值$1$，最小多项式为$(\lambda-1)^2$；若可对角化只能是$I$，与$N\ne0$矛盾。

scene_spec.steps[3]

第四步:因此非零向量产生的零内积边界导致不可对角化。

## draft-c27-02

problem

求实矩阵$A=\begin{pmatrix}0&1&0\\0&0&1\\2&1&1\end{pmatrix}$在$\mathbb C$上的对角化，并判断它能否在$\mathbb R$上对角化。

solution

特征多项式为$\lambda^3-\lambda^2-\lambda-2=(\lambda-2)(\lambda^2+\lambda+1)$。三根为$2$、$\omega=(-1+i\sqrt3)/2$、$\overline\omega$，互不相同。对每一根，$v_\lambda=(1,\lambda,\lambda^2)^{\mathsf T}$满足$Av_\lambda=\lambda v_\lambda$。取$P=(v_2,v_\omega,v_{\overline\omega})$，Vandermonde行列式为$(\omega-2)(\overline\omega-2)(\overline\omega-\omega)\ne0$，故$P^{-1}AP=\operatorname{diag}(2,\omega,\overline\omega)$。若在实域可对角化，特征多项式必须分裂为实线性因子；而二次因子判别式$-3<0$，所以不能在实域对角化。数域条件不能省略。

answer

复域可对角化，$P$与$D$如上；实域不可对角化。

scene_spec.objects[0]

求实矩阵$A=\begin{pmatrix}0&1&0\\0&0&1\\2&1&1\end{pmatrix}$在$\mathbb C$上的对角化，并判断它能否在$\mathbb R$上对角化。

scene_spec.objects[1]

复域可对角化，$P$与$D$如上；实域不可对角化。

scene_spec.steps[0]

第一步:特征多项式为$\lambda^3-\lambda^2-\lambda-2=(\lambda-2)(\lambda^2+\lambda+1)$。

scene_spec.steps[1]

第二步:三根为$2$、$\omega=(-1+i\sqrt3)/2$、$\overline\omega$，互不相同。

scene_spec.steps[2]

第三步:对每一根，$v_\lambda=(1,\lambda,\lambda^2)^{\mathsf T}$满足$Av_\lambda=\lambda v_\lambda$。

scene_spec.steps[3]

第四步:取$P=(v_2,v_\omega,v_{\overline\omega})$，Vandermonde行列式为$(\omega-2)(\overline\omega-2)(\overline\omega-\omega)\ne0$，故$P^{-1}AP=\operatorname{diag}(2,\omega,\overline\omega)$。

scene_spec.steps[4]

第五步:若在实域可对角化，特征多项式必须分裂为实线性因子；而二次因子判别式$-3<0$，所以不能在实域对角化。

scene_spec.steps[5]

第六步:数域条件不能省略。

## draft-c27-03

problem

设实矩阵$A$满足$A^3=A$。不用先求坐标特征向量，构造对应特征值$0,1,-1$的谱投影，证明$A$可对角化，并给所有正整数幂。

solution

定义$P_0=I-A^2$、$P_+=(A^2+A)/2$、$P_-=(A^2-A)/2$。由$A^3=A$和$A^4=A^2$，直接相乘得三投影各自幂等、两两乘积零、和为$I$，且$AP_0=0,AP_+=P_+,AP_-=-P_-$。所以全空间为三个像的直和；在各像中取基便得到对角化，零维像可省略。又$A^{m+2}=A^m$对$m\ge1$成立，故正奇数幂为$A$，正偶数幂为$A^2$。这依赖多项式恒等式及简单根结构，不是某个二阶矩阵幂的数值替换。

answer

$P_0=I-A^2,P_\pm=(A^2\pm A)/2$；$A$可对角化，奇正幂$A$、偶正幂$A^2$。

scene_spec.objects[0]

设实矩阵$A$满足$A^3=A$。不用先求坐标特征向量，构造对应特征值$0,1,-1$的谱投影，证明$A$可对角化，并给所有正整数幂。

scene_spec.objects[1]

$P_0=I-A^2,P_\pm=(A^2\pm A)/2$；$A$可对角化，奇正幂$A$、偶正幂$A^2$。

scene_spec.steps[0]

第一步:定义$P_0=I-A^2$、$P_+=(A^2+A)/2$、$P_-=(A^2-A)/2$。

scene_spec.steps[1]

第二步:由$A^3=A$和$A^4=A^2$，直接相乘得三投影各自幂等、两两乘积零、和为$I$，且$AP_0=0,AP_+=P_+,AP_-=-P_-$。

scene_spec.steps[2]

第三步:所以全空间为三个像的直和；在各像中取基便得到对角化，零维像可省略。

scene_spec.steps[3]

第四步:又$A^{m+2}=A^m$对$m\ge1$成立，故正奇数幂为$A$，正偶数幂为$A^2$。

scene_spec.steps[4]

第五步:这依赖多项式恒等式及简单根结构，不是某个二阶矩阵幂的数值替换。

## draft-c27-04

problem

设$A_k=\begin{pmatrix}1&k\\0&2\end{pmatrix}$，$k\in\mathbb R$。求对角化并判断何时能正交对角化，给两特征线夹角$\alpha\in(0,\pi/2]$的精确式，并包含垂直情形。

solution

特征值为$1,2$，对应特征向量$e_1=(1,0)$与$(k,1)$。$P=\begin{pmatrix}1&k\\0&1\end{pmatrix}$可逆且$A_kP=P\operatorname{diag}(1,2)$，故所有$k$都可对角化。两特征线夹角$\alpha\in(0,\pi/2]$满足$\cos\alpha=|k|/\sqrt{k^2+1}$，所以仅$k=0$时垂直。实矩阵正交对角化为实对角阵必对称，而$A_k$对称当且仅当$k=0$；故正交对角化也当且仅当$k=0$。

answer

所有$k$可对角化；正交对角化当且仅当$k=0$；$\alpha=\arccos(|k|/\sqrt{k^2+1})$。

scene_spec.objects[0]

设$A_k=\begin{pmatrix}1&k\\0&2\end{pmatrix}$，$k\in\mathbb R$。求对角化并判断何时能正交对角化，给两特征线夹角$\alpha\in(0,\pi/2]$的精确式，并包含垂直情形。

scene_spec.objects[1]

所有$k$可对角化；正交对角化当且仅当$k=0$；$\alpha=\arccos(|k|/\sqrt{k^2+1})$。

scene_spec.steps[0]

第一步:特征值为$1,2$，对应特征向量$e_1=(1,0)$与$(k,1)$。

scene_spec.steps[1]

第二步:$P=\begin{pmatrix}1&k\\0&1\end{pmatrix}$可逆且$A_kP=P\operatorname{diag}(1,2)$，故所有$k$都可对角化。

scene_spec.steps[2]

第三步:两特征线夹角$\alpha\in(0,\pi/2]$满足$\cos\alpha=|k|/\sqrt{k^2+1}$，所以仅$k=0$时垂直。

scene_spec.steps[3]

第四步:实矩阵正交对角化为实对角阵必对称，而$A_k$对称当且仅当$k=0$；故正交对角化也当且仅当$k=0$。

## draft-c27-05

problem

证明：若$n$阶矩阵在数域$\mathbb F$内有$n$个互异特征值，则在$\mathbb F$内可对角化。

solution

对互异$\lambda_1,\ldots,\lambda_n\in\mathbb F$取非零特征向量$v_i$。用归纳法证明独立：若$\sum_{i=1}^m c_iv_i=0$，施加$A-\lambda_mI$，得到$\sum_{i<m}c_i(\lambda_i-\lambda_m)v_i=0$；由归纳假设和互异性，$c_i=0$（$i<m$），再得$c_m=0$。故$n$个特征向量组成可逆矩阵$P$，$AP=P\operatorname{diag}(\lambda_i)$。数域内有全部特征值的条件不可省略。

answer

证明见解法(归纳法证明不同特征值的特征向量线性无关,从而构成基)。

scene_spec.objects[0]

证明：若$n$阶矩阵在数域$\mathbb F$内有$n$个互异特征值，则在$\mathbb F$内可对角化。

scene_spec.objects[1]

证明见解法(归纳法证明不同特征值的特征向量线性无关,从而构成基)。

scene_spec.steps[0]

第一步:对互异$\lambda_1,\ldots,\lambda_n\in\mathbb F$取非零特征向量$v_i$。

scene_spec.steps[1]

第二步:用归纳法证明独立：若$\sum_{i=1}^m c_iv_i=0$，施加$A-\lambda_mI$，得到$\sum_{i<m}c_i(\lambda_i-\lambda_m)v_i=0$；由归纳假设和互异性，$c_i=0$（$i<m$），再得$c_m=0$。

scene_spec.steps[2]

第三步:故$n$个特征向量组成可逆矩阵$P$，$AP=P\operatorname{diag}(\lambda_i)$。

scene_spec.steps[3]

第四步:数域内有全部特征值的条件不可省略。

## draft-c29-01

problem

用$f(x)=x^4+4$说明“没有有理根”不等于“在$\mathbb Q[x]$不可约”。给出在$\mathbb Q,\mathbb R,\mathbb C$中的不可约因子，并证明。

solution

Sophie Germain恒等式给$x^4+4=(x^2-2x+2)(x^2+2x+2)$。两个二次因子的判别式都是$-4$，在$\mathbb Q$和$\mathbb R$不可约，且实数$x$下$f(x)>0$，所以连实根都没有。复数根为$1\pm i,-1\pm i$，故复域分解为相应四个首一线性因子。无有理根只能排除一次有理因子，不能排除二次因子；四次多项式的可约性不能仅靠有理根检验决定。

answer

$\mathbb Q,\mathbb R$中分解为$x^2\mp2x+2$；$\mathbb C$中根$\pm1\pm i$；没有有理根但可约。

scene_spec.objects[0]

用$f(x)=x^4+4$说明“没有有理根”不等于“在$\mathbb Q[x]$不可约”。给出在$\mathbb Q,\mathbb R,\mathbb C$中的不可约因子，并证明。

scene_spec.objects[1]

$\mathbb Q,\mathbb R$中分解为$x^2\mp2x+2$；$\mathbb C$中根$\pm1\pm i$；没有有理根但可约。

scene_spec.steps[0]

第一步:Sophie Germain恒等式给$x^4+4=(x^2-2x+2)(x^2+2x+2)$。

scene_spec.steps[1]

第二步:两个二次因子的判别式都是$-4$，在$\mathbb Q$和$\mathbb R$不可约，且实数$x$下$f(x)>0$，所以连实根都没有。

scene_spec.steps[2]

第三步:复数根为$1\pm i,-1\pm i$，故复域分解为相应四个首一线性因子。

scene_spec.steps[3]

第四步:无有理根只能排除一次有理因子，不能排除二次因子；四次多项式的可约性不能仅靠有理根检验决定。

## draft-c29-02

problem

已知 $2+i$ 是实系数多项式 $f(x)=x^3-7x^2+17x-15$ 的一个根，求 $f$ 的全部根。

solution

实系数多项式的非实根成对出现:$2-i$ 也是根,故 $f$ 含因子 $(x-(2+i))(x-(2-i))=x^2-4x+5$。用韦达定理或综合除法:设第三根为 $r$,三根之和为 $7$,故 $r=7-(2+i)-(2-i)=3$。验证:$f=(x-3)(x^2-4x+5)$,展开核对:$x^3-4x^2+5x-3x^2+12x-15=x^3-7x^2+17x-15$ ✓。全部根:$3$,$2+i$,$2-i$。

answer

全部根:$3$,$2+i$,$2-i$。

scene_spec.objects[0]

已知 $2+i$ 是实系数多项式 $f(x)=x^3-7x^2+17x-15$ 的一个根，求 $f$ 的全部根。

scene_spec.objects[1]

全部根:$3$,$2+i$,$2-i$。

scene_spec.steps[0]

第一步:实系数多项式的非实根成对出现:$2-i$ 也是根,故 $f$ 含因子 $(x-(2+i))(x-(2-i))=x^2-4x+5$。

scene_spec.steps[1]

第二步:用韦达定理或综合除法:设第三根为 $r$,三根之和为 $7$,故 $r=7-(2+i)-(2-i)=3$。

scene_spec.steps[2]

第三步:验证:$f=(x-3)(x^2-4x+5)$,展开核对:$x^3-4x^2+5x-3x^2+12x-15=x^3-7x^2+17x-15$ ✓。

scene_spec.steps[3]

第四步:全部根:$3$,$2+i$,$2-i$。

## draft-c29-03

problem

用 $f$ 与 $f'$ 的公因式求多项式 $f(x)=x^4-4x^3+6x^2-4x+1$ 的重根及其重数。

solution

$f=x^4-4x^3+6x^2-4x+1=(x-1)^4$，$f^{\prime}=4(x-1)^3$。欧几里得步骤$f-(x-1)f^{\prime}/4=0$，故首一最大公因子为$(x-1)^3$。$f/f_{\mathrm{gcd}}=x-1$给唯一不同根$1$；$f^{(j)}(1)=0$（$j=0,1,2,3$）、$f^{(4)}(1)=24\ne0$，证明重数恰为$4$。

answer

$f=(x-1)^4$,$x=1$ 是四重根。

scene_spec.objects[0]

用 $f$ 与 $f'$ 的公因式求多项式 $f(x)=x^4-4x^3+6x^2-4x+1$ 的重根及其重数。

scene_spec.objects[1]

$f=(x-1)^4$,$x=1$ 是四重根。

scene_spec.steps[0]

第一步:$f=x^4-4x^3+6x^2-4x+1=(x-1)^4$，$f^{\prime}=4(x-1)^3$。

scene_spec.steps[1]

第二步:欧几里得步骤$f-(x-1)f^{\prime}/4=0$，故首一最大公因子为$(x-1)^3$。

scene_spec.steps[2]

第三步:$f/f_{\mathrm{gcd}}=x-1$给唯一不同根$1$；$f^{(j)}(1)=0$（$j=0,1,2,3$）、$f^{(4)}(1)=24\ne0$，证明重数恰为$4$。

## draft-c29-04

problem

求使多项式 $f(x)=x^3-3x+a$ 有重根的参数 $a$ 的值。

solution

$f$ 有重根当且仅当 $f$ 与 $f'$ 有公共根。$f'(x)=3x^2-3=3(x-1)(x+1)$,可能的公根为 $x=1$ 或 $x=-1$。$x=1$ 是公根 ⟺ $f(1)=0$,即 $1-3+a=0$,$a=2$;$x=-1$ 是公根 ⟺ $f(-1)=0$,即 $-1+3+a=0$,$a=-2$。故 $a=2$ 或 $a=-2$。验证:$a=2$ 时 $f=x^3-3x+2=(x-1)^2(x+2)$;$a=-2$ 时 $f=x^3-3x-2=(x+1)^2(x-2)$。

answer

$a=2$ 或 $a=-2$;对应分解 $(x-1)^2(x+2)$ 与 $(x+1)^2(x-2)$。

scene_spec.objects[0]

求使多项式 $f(x)=x^3-3x+a$ 有重根的参数 $a$ 的值。

scene_spec.objects[1]

$a=2$ 或 $a=-2$;对应分解 $(x-1)^2(x+2)$ 与 $(x+1)^2(x-2)$。

scene_spec.steps[0]

第一步:$f$ 有重根当且仅当 $f$ 与 $f'$ 有公共根。

scene_spec.steps[1]

第二步:$f'(x)=3x^2-3=3(x-1)(x+1)$,可能的公根为 $x=1$ 或 $x=-1$。

scene_spec.steps[2]

第三步:$x=1$ 是公根 ⟺ $f(1)=0$,即 $1-3+a=0$,$a=2$;$x=-1$ 是公根 ⟺ $f(-1)=0$,即 $-1+3+a=0$,$a=-2$。

scene_spec.steps[3]

第四步:故 $a=2$ 或 $a=-2$。

scene_spec.steps[4]

第五步:验证:$a=2$ 时 $f=x^3-3x+2=(x-1)^2(x+2)$;$a=-2$ 时 $f=x^3-3x-2=(x+1)^2(x-2)$。

## draft-c29-05

problem

证明三次多项式的根与系数关系(韦达定理)，并构造一个以 $2$、$-1$、$\frac12$ 为根的首一三次多项式。

solution

设首一三次多项式 $f(x)=x^3+px^2+qx+r$ 的根为 $\alpha,\beta,\gamma$,则 $f(x)=(x-\alpha)(x-\beta)(x-\gamma)$。展开右边:$x^3-(\alpha+\beta+\gamma)x^2+(\alpha\beta+\beta\gamma+\gamma\alpha)x-\alpha\beta\gamma$。比较系数得韦达定理:$\alpha+\beta+\gamma=-p$,$\alpha\beta+\beta\gamma+\gamma\alpha=q$,$\alpha\beta\gamma=-r$。构造:以 $2,-1,\frac12$ 为根,则 $f(x)=(x-2)(x+1)(x-\frac12)$。展开:$(x^2-x-2)(x-\frac12)=x^3-x^2-2x-\frac12x^2+\frac12x+1=x^3-\frac32x^2-\frac32x+1$。

answer

韦达定理:根和 $=-p$,两两积和 $=q$,根积 $=-r$;构造:$f=x^3-\frac32x^2-\frac32x+1$。

scene_spec.objects[0]

证明三次多项式的根与系数关系(韦达定理)，并构造一个以 $2$、$-1$、$\frac12$ 为根的首一三次多项式。

scene_spec.objects[1]

韦达定理:根和 $=-p$,两两积和 $=q$,根积 $=-r$;构造:$f=x^3-\frac32x^2-\frac32x+1$。

scene_spec.steps[0]

第一步:设首一三次多项式 $f(x)=x^3+px^2+qx+r$ 的根为 $\alpha,\beta,\gamma$,则 $f(x)=(x-\alpha)(x-\beta)(x-\gamma)$。

scene_spec.steps[1]

第二步:展开右边:$x^3-(\alpha+\beta+\gamma)x^2+(\alpha\beta+\beta\gamma+\gamma\alpha)x-\alpha\beta\gamma$。

scene_spec.steps[2]

第三步:比较系数得韦达定理:$\alpha+\beta+\gamma=-p$,$\alpha\beta+\beta\gamma+\gamma\alpha=q$,$\alpha\beta\gamma=-r$。

scene_spec.steps[3]

第四步:构造:以 $2,-1,\frac12$ 为根,则 $f(x)=(x-2)(x+1)(x-\frac12)$。

scene_spec.steps[4]

第五步:展开:$(x^2-x-2)(x-\frac12)=x^3-x^2-2x-\frac12x^2+\frac12x+1=x^3-\frac32x^2-\frac32x+1$。

## draft-c32-01

problem

求$\mathbb R^5$中满足$x_{i+2}-2x_{i+1}+x_i=0$（$i=1,2,3$）的子空间的基与维数，并证明解的表达式完整。

solution

二阶差分为零等价于相邻一阶差相同。令$a=x_1,b=x_2-x_1$，递推唯一给$x_i=a+(i-1)b$，$i=1,\ldots,5$。反过来任何该形式均满足三约束。故解空间为$\operatorname{span}\{(1,1,1,1,1),(0,1,2,3,4)\}$。两向量由前两坐标可知独立，维数$2$；三个耦合约束独立，秩$3$。

answer

基$(1,1,1,1,1),(0,1,2,3,4)$，维数$2$。

scene_spec.objects[0]

求$\mathbb R^5$中满足$x_{i+2}-2x_{i+1}+x_i=0$（$i=1,2,3$）的子空间的基与维数，并证明解的表达式完整。

scene_spec.objects[1]

基$(1,1,1,1,1),(0,1,2,3,4)$，维数$2$。

scene_spec.steps[0]

第一步:二阶差分为零等价于相邻一阶差相同。

scene_spec.steps[1]

第二步:令$a=x_1,b=x_2-x_1$，递推唯一给$x_i=a+(i-1)b$，$i=1,\ldots,5$。

scene_spec.steps[2]

第三步:反过来任何该形式均满足三约束。

scene_spec.steps[3]

第四步:故解空间为$\operatorname{span}\{(1,1,1,1,1),(0,1,2,3,4)\}$。

scene_spec.steps[4]

第五步:两向量由前两坐标可知独立，维数$2$；三个耦合约束独立，秩$3$。

## draft-c32-02

problem

求$V=\{x\in\mathbb R^4:\sum_{i=0}^3x_i=0,\ \sum_{i=0}^3i x_i=0\}$的基与维数，证明给出的基张成全部解。

solution

约束行$(1,1,1,1)$与$(0,1,2,3)$不成比例，秩$2$，故维数$2$。向量$v=(1,-2,1,0)$与$w=(0,1,-2,1)$同时满足两个约束，且由首末坐标可知独立。也可对任意解先取$x_0v+x_3w$，减去后首末坐标为零，剩余两坐标满足$y_1+y_2=0,y_1+2y_2=0$，故全零，证明张成。

answer

基$(1,-2,1,0),(0,1,-2,1)$，维数$2$。

scene_spec.objects[0]

求$V=\{x\in\mathbb R^4:\sum_{i=0}^3x_i=0,\ \sum_{i=0}^3i x_i=0\}$的基与维数，证明给出的基张成全部解。

scene_spec.objects[1]

基$(1,-2,1,0),(0,1,-2,1)$，维数$2$。

scene_spec.steps[0]

第一步:约束行$(1,1,1,1)$与$(0,1,2,3)$不成比例，秩$2$，故维数$2$。

scene_spec.steps[1]

第二步:向量$v=(1,-2,1,0)$与$w=(0,1,-2,1)$同时满足两个约束，且由首末坐标可知独立。

scene_spec.steps[2]

第三步:也可对任意解先取$x_0v+x_3w$，减去后首末坐标为零，剩余两坐标满足$y_1+y_2=0,y_1+2y_2=0$，故全零，证明张成。

## draft-c32-03

problem

一个菱形流网络的四边流量$(u,v,w,z)$满足$u+v=1,w+z=1,u=w,v=z$。求实线性方程的全部解；再加入各流量非负，求可行集并判断两者是否为线性子空间。

solution

由守恒得$w=u,z=v=1-u$，所以全部解为$(t,1-t,t,1-t)$，$t\in\mathbb R$，是一条仿射直线。它等于$(0,1,0,1)+t(1,-1,1,-1)$，但不含零向量，因此不是线性子空间。非负性等价于$0\le t\le1$，可行集为该直线上的闭线段；线段也不含零且不封闭于任意标量乘法。四条等式有冗余，不能按方程条数直接减维数。

answer

全部实解$t\in\mathbb R$；非负解$t\in[0,1]$；两者都不是线性子空间。

scene_spec.objects[0]

一个菱形流网络的四边流量$(u,v,w,z)$满足$u+v=1,w+z=1,u=w,v=z$。求实线性方程的全部解；再加入各流量非负，求可行集并判断两者是否为线性子空间。

scene_spec.objects[1]

全部实解$t\in\mathbb R$；非负解$t\in[0,1]$；两者都不是线性子空间。

scene_spec.steps[0]

第一步:由守恒得$w=u,z=v=1-u$，所以全部解为$(t,1-t,t,1-t)$，$t\in\mathbb R$，是一条仿射直线。

scene_spec.steps[1]

第二步:它等于$(0,1,0,1)+t(1,-1,1,-1)$，但不含零向量，因此不是线性子空间。

scene_spec.steps[2]

第三步:非负性等价于$0\le t\le1$，可行集为该直线上的闭线段；线段也不含零且不封闭于任意标量乘法。

scene_spec.steps[3]

第四步:四条等式有冗余，不能按方程条数直接减维数。

## draft-c32-04

problem

对实参数$a,b$，分类系统$x+y=1,\ ax+y=b$的全部解，并写出每种解集的维数或为空。

solution

相减得$(a-1)x=b-1$。若$a\ne1$，唯一解$x=(b-1)/(a-1),y=(a-b)/(a-1)$，解集为一个点，仿射维数$0$。若$a=1,b=1$，两式相同，解集$(t,1-t)$为仿射直线，维数$1$。若$a=1,b\ne1$，相减为$0=b-1\ne0$，无解；空集不作为含基点的仿射子空间讨论维数。

answer

$a\ne1$唯一；$a=b=1$一维仿射直线；$a=1,b\ne1$无解。

scene_spec.objects[0]

对实参数$a,b$，分类系统$x+y=1,\ ax+y=b$的全部解，并写出每种解集的维数或为空。

scene_spec.objects[1]

$a\ne1$唯一；$a=b=1$一维仿射直线；$a=1,b\ne1$无解。

scene_spec.steps[0]

第一步:相减得$(a-1)x=b-1$。

scene_spec.steps[1]

第二步:若$a\ne1$，唯一解$x=(b-1)/(a-1),y=(a-b)/(a-1)$，解集为一个点，仿射维数$0$。

scene_spec.steps[2]

第三步:若$a=1,b=1$，两式相同，解集$(t,1-t)$为仿射直线，维数$1$。

scene_spec.steps[3]

第四步:若$a=1,b\ne1$，相减为$0=b-1\ne0$，无解；空集不作为含基点的仿射子空间讨论维数。

## draft-c32-05

problem

证明:齐次线性方程组 $Ax=0$ 的解集是 $\mathbb R^n$ 的线性子空间,其维数为 $n-\mathrm{rank}(A)$;相容的非齐次方程组 $Ax=b$($b\neq0$)的解集是 $\eta_0+\ker A$(仿射子空间)而不是线性子空间。同时说明不相容时的解集。

solution

齐次解集$\ker A$含零并对线性组合封闭，维数$n-\operatorname{rank}A$。非齐次系统$Ax=b$若不相容，解集为空；若相容，选一个特解$x_0$，则$Ax=b$等价于$A(x-x_0)=0$，所以解集恰为$x_0+\ker A$，仿射维数$n-\operatorname{rank}A$。若$b\ne0$，零向量不在该解集中，因而不是线性子空间；若$b=0$，回到齐次情形。

answer

齐次解集$\ker A$；相容非齐次解集$x_0+\ker A$；不相容则为空。

scene_spec.objects[0]

证明:齐次线性方程组 $Ax=0$ 的解集是 $\mathbb R^n$ 的线性子空间,其维数为 $n-\mathrm{rank}(A)$;相容的非齐次方程组 $Ax=b$($b\neq0$)的解集是 $\eta_0+\ker A$(仿射子空间)而不是线性子空间。同时说明不相容时的解集。

scene_spec.objects[1]

齐次解集$\ker A$；相容非齐次解集$x_0+\ker A$；不相容则为空。

scene_spec.steps[0]

第一步:齐次解集$\ker A$含零并对线性组合封闭，维数$n-\operatorname{rank}A$。

scene_spec.steps[1]

第二步:非齐次系统$Ax=b$若不相容，解集为空；若相容，选一个特解$x_0$，则$Ax=b$等价于$A(x-x_0)=0$，所以解集恰为$x_0+\ker A$，仿射维数$n-\operatorname{rank}A$。

scene_spec.steps[2]

第三步:若$b\ne0$，零向量不在该解集中，因而不是线性子空间；若$b=0$，回到齐次情形。
