## draft-c20-01

problem

指出方程 $z=x^2-y^2$ 表示的二次曲面类型，并分别说明其与平面 $z=0$、$z=1$、$z=-1$ 的交线形状。

solution

类型:双曲抛物面(马鞍面)。截面 $z=0$:$x^2-y^2=0$,即 $y=\pm x$,是两条相交直线。截面 $z=1$:$x^2-y^2=1$,是双曲线(实轴沿 $x$ 方向)。截面 $z=-1$:$y^2-x^2=1$,也是双曲线(实轴沿 $y$ 方向)。

answer

双曲抛物面;$z=0$ 截面为两条相交直线 $y=\pm x$,$z=1$ 与 $z=-1$ 截面为实轴方向不同的双曲线。

scene_spec.objects[0]

指出方程 $z=x^2-y^2$ 表示的二次曲面类型，并分别说明其与平面 $z=0$、$z=1$、$z=-1$ 的交线形状。

scene_spec.objects[1]

双曲抛物面;$z=0$ 截面为两条相交直线 $y=\pm x$,$z=1$ 与 $z=-1$ 截面为实轴方向不同的双曲线。

scene_spec.steps[0]

第一步:类型:双曲抛物面(马鞍面)。

scene_spec.steps[1]

第二步:截面 $z=0$:$x^2-y^2=0$,即 $y=\pm x$,是两条相交直线。

scene_spec.steps[2]

第三步:截面 $z=1$:$x^2-y^2=1$,是双曲线(实轴沿 $x$ 方向)。

scene_spec.steps[3]

第四步:截面 $z=-1$:$y^2-x^2=1$,也是双曲线(实轴沿 $y$ 方向)。

## draft-c20-02

problem

用配方法判断方程 $x^2+y^2+z^2-2x-4y+1=0$ 表示什么曲面，并求其中心(球心)与半径。

solution

配方:$(x^2-2x)+(y^2-4y)+z^2+1=0$,即 $(x-1)^2-1+(y-2)^2-4+z^2+1=0$,整理得 $(x-1)^2+(y-2)^2+z^2=4$。这是球面,球心为 $(1,2,0)$,半径为 $2$。

answer

球面,球心 $(1,2,0)$,半径 $2$。

scene_spec.objects[0]

用配方法判断方程 $x^2+y^2+z^2-2x-4y+1=0$ 表示什么曲面，并求其中心(球心)与半径。

scene_spec.objects[1]

球面,球心 $(1,2,0)$,半径 $2$。

scene_spec.steps[0]

第一步:配方:$(x^2-2x)+(y^2-4y)+z^2+1=0$,即 $(x-1)^2-1+(y-2)^2-4+z^2+1=0$,整理得 $(x-1)^2+(y-2)^2+z^2=4$。

scene_spec.steps[1]

第二步:这是球面,球心为 $(1,2,0)$,半径为 $2$。

## draft-c20-03

problem

对曲面$xy+t z^2=1$（$t\in\mathbb R$），给出正交坐标替换并分类全部参数，特别说明$t=0$的秩退化。

solution

令$u=(x+y)/\sqrt2$、$v=(-x+y)/\sqrt2$，则$xy=(u^2-v^2)/2$，方程为$u^2/2-v^2/2+t z^2=1$。若$t>0$，正平方有两个、负平方一个，是单叶双曲面；若$t<0$，正平方一个、负平方两个，是双叶双曲面；若$t=0$，$u^2-v^2=2$与$z$无关，是沿$z$方向的双曲柱面，二次型秩由$3$降为$2$。分类依据惯性与正右端，不凭图像或系数符号猜测。

answer

$t>0$单叶，$t<0$双叶，$t=0$双曲柱面；标准坐标方程$u^2/2-v^2/2+tz^2=1$。

scene_spec.objects[0]

对曲面$xy+t z^2=1$（$t\in\mathbb R$），给出正交坐标替换并分类全部参数，特别说明$t=0$的秩退化。

scene_spec.objects[1]

$t>0$单叶，$t<0$双叶，$t=0$双曲柱面；标准坐标方程$u^2/2-v^2/2+tz^2=1$。

scene_spec.steps[0]

第一步:令$u=(x+y)/\sqrt2$、$v=(-x+y)/\sqrt2$，则$xy=(u^2-v^2)/2$，方程为$u^2/2-v^2/2+t z^2=1$。

scene_spec.steps[1]

第二步:若$t>0$，正平方有两个、负平方一个，是单叶双曲面；若$t<0$，正平方一个、负平方两个，是双叶双曲面；若$t=0$，$u^2-v^2=2$与$z$无关，是沿$z$方向的双曲柱面，二次型秩由$3$降为$2$。

scene_spec.steps[2]

第三步:分类依据惯性与正右端，不凭图像或系数符号猜测。

## draft-c20-04

problem

椭球$x^2+2y^2+3z^2=1$与平面$x+y+z=t$相交。求截面中心、全部空集或退化情形，以及非退化截面的精确半轴长。

solution

记$W=\operatorname{diag}(1,2,3)$，$n=(1,1,1)$。在平面上二次型的最小点为$c=tW^{-1}n/(n^{\mathsf T}W^{-1}n)=(6t/11,3t/11,2t/11)$；$c^{\mathsf T}Wc=6t^2/11$。写$x=c+h$、$n\cdot h=0$，交叉项为零，截面满足$h^{\mathsf T}Wh=1-6t^2/11$。因此$|t|>\sqrt{11/6}$为空，等号为单点$c$，小于时为椭圆。在切向正交基$e=(1,-1,0)/\sqrt2$、$f=(1,1,-2)/\sqrt6$中限制矩阵为$\begin{pmatrix}3/2&-1/(2\sqrt3)\\-1/(2\sqrt3)&5/2\end{pmatrix}$，特征值$2\pm1/\sqrt3$。所以长短半轴依次为$\sqrt{(1-6t^2/11)/(2-1/\sqrt3)}$、$\sqrt{(1-6t^2/11)/(2+1/\sqrt3)}$。

answer

中心$(6t,3t,2t)/11$；阈值$|t|=\sqrt{11/6}$；椭圆半轴$\sqrt{(1-6t^2/11)/(2\mp1/\sqrt3)}$。

scene_spec.objects[0]

椭球$x^2+2y^2+3z^2=1$与平面$x+y+z=t$相交。求截面中心、全部空集或退化情形，以及非退化截面的精确半轴长。

scene_spec.objects[1]

中心$(6t,3t,2t)/11$；阈值$|t|=\sqrt{11/6}$；椭圆半轴$\sqrt{(1-6t^2/11)/(2\mp1/\sqrt3)}$。

scene_spec.steps[0]

第一步:记$W=\operatorname{diag}(1,2,3)$，$n=(1,1,1)$。

scene_spec.steps[1]

第二步:在平面上二次型的最小点为$c=tW^{-1}n/(n^{\mathsf T}W^{-1}n)=(6t/11,3t/11,2t/11)$；$c^{\mathsf T}Wc=6t^2/11$。

scene_spec.steps[2]

第三步:写$x=c+h$、$n\cdot h=0$，交叉项为零，截面满足$h^{\mathsf T}Wh=1-6t^2/11$。

scene_spec.steps[3]

第四步:因此$|t|>\sqrt{11/6}$为空，等号为单点$c$，小于时为椭圆。

scene_spec.steps[4]

第五步:在切向正交基$e=(1,-1,0)/\sqrt2$、$f=(1,1,-2)/\sqrt6$中限制矩阵为$\begin{pmatrix}3/2&-1/(2\sqrt3)\\-1/(2\sqrt3)&5/2\end{pmatrix}$，特征值$2\pm1/\sqrt3$。

scene_spec.steps[5]

第六步:所以长短半轴依次为$\sqrt{(1-6t^2/11)/(2-1/\sqrt3)}$、$\sqrt{(1-6t^2/11)/(2+1/\sqrt3)}$。

## draft-c20-05

problem

用正交变换(旋转)判断方程 $x^2+2xy+y^2+z=0$ 表示的曲面类型。

solution

交叉项部分 $x^2+2xy+y^2=(x+y)^2$。作正交变换 $u=\frac{x+y}{\sqrt2}$,$v=\frac{-x+y}{\sqrt2}$,$w=z$(变换矩阵 $\begin{pmatrix}\frac1{\sqrt2}&\frac1{\sqrt2}&0\\-\frac1{\sqrt2}&\frac1{\sqrt2}&0\\0&0&1\end{pmatrix}$ 为正交矩阵且行列式为 $1$,是绕 $z$ 轴的真旋转),则 $x^2+2xy+y^2=2u^2$,方程化为 $2u^2+w=0$,即 $w=-2u^2$。这是母线沿 $v$ 方向的抛物柱面。

answer

抛物柱面；新坐标满足$w=-2u^2$，母线沿世界坐标方向$(-1,1,0)/\sqrt2$。

scene_spec.objects[0]

用正交变换(旋转)判断方程 $x^2+2xy+y^2+z=0$ 表示的曲面类型。

scene_spec.objects[1]

抛物柱面；新坐标满足$w=-2u^2$，母线沿世界坐标方向$(-1,1,0)/\sqrt2$。

scene_spec.steps[0]

第一步:交叉项部分 $x^2+2xy+y^2=(x+y)^2$。

scene_spec.steps[1]

第二步:作正交变换 $u=\frac{x+y}{\sqrt2}$,$v=\frac{-x+y}{\sqrt2}$,$w=z$(变换矩阵 $\begin{pmatrix}\frac1{\sqrt2}&\frac1{\sqrt2}&0\\-\frac1{\sqrt2}&\frac1{\sqrt2}&0\\0&0&1\end{pmatrix}$ 为正交矩阵且行列式为 $1$,是绕 $z$ 轴的真旋转),则 $x^2+2xy+y^2=2u^2$,方程化为 $2u^2+w=0$,即 $w=-2u^2$。

scene_spec.steps[2]

第三步:这是母线沿 $v$ 方向的抛物柱面。

## draft-c22-01

problem

验证单叶双曲面 $x^2+y^2-z^2=1$ 是直纹面，并写出其两族直母线。

solution

曲面$x^2+y^2-z^2=1$等价于$(x+z)(x-z)=(1+y)(1-y)$。两族直线可完整写成$t(x+z)=s(1+y),\ s(x-z)=t(1-y)$及$t(x+z)=s(1-y),\ s(x-z)=t(1+y)$，其中$(s:t)\in\mathbb{RP}^1$。若$st\ne0$，相乘消去$st$得到曲面方程；若$s=0$，两族分别给$x+z=0,y=1$与$x+z=0,y=-1$；若$t=0$，分别给$y=-1,x-z=0$与$y=1,x-z=0$，也全部位于曲面。两平面的法向量在任何非零参数对下独立，故每个成员确为直线。矩阵$\begin{pmatrix}x+z&1+y\\1-y&x-z\end{pmatrix}$在曲面上秩为$1$且不可能为零；其列空间和行空间分别唯一确定两族参数，故每点各有一条母线。

answer

两族母线:$\begin{cases}x+z=\lambda(1+y)\\ \lambda(x-z)=1-y\end{cases}$ 与 $\begin{cases}x+z=\mu(1-y)\\ \mu(x-z)=1+y\end{cases}$($\lambda,\mu$ 取扩充实数,含 $\infty$ 对应极限直线 $y=\mp1,x=z$);单叶双曲面是直纹面。

scene_spec.objects[0]

验证单叶双曲面 $x^2+y^2-z^2=1$ 是直纹面，并写出其两族直母线。

scene_spec.objects[1]

两族母线:$\begin{cases}x+z=\lambda(1+y)\\ \lambda(x-z)=1-y\end{cases}$ 与 $\begin{cases}x+z=\mu(1-y)\\ \mu(x-z)=1+y\end{cases}$($\lambda,\mu$ 取扩充实数,含 $\infty$ 对应极限直线 $y=\mp1,x=z$);单叶双曲面是直纹面。

scene_spec.steps[0]

第一步:曲面$x^2+y^2-z^2=1$等价于$(x+z)(x-z)=(1+y)(1-y)$。

scene_spec.steps[1]

第二步:两族直线可完整写成$t(x+z)=s(1+y),\ s(x-z)=t(1-y)$及$t(x+z)=s(1-y),\ s(x-z)=t(1+y)$，其中$(s:t)\in\mathbb{RP}^1$。

scene_spec.steps[2]

第三步:若$st\ne0$，相乘消去$st$得到曲面方程；若$s=0$，两族分别给$x+z=0,y=1$与$x+z=0,y=-1$；若$t=0$，分别给$y=-1,x-z=0$与$y=1,x-z=0$，也全部位于曲面。

scene_spec.steps[3]

第四步:两平面的法向量在任何非零参数对下独立，故每个成员确为直线。

scene_spec.steps[4]

第五步:矩阵$\begin{pmatrix}x+z&1+y\\1-y&x-z\end{pmatrix}$在曲面上秩为$1$且不可能为零；其列空间和行空间分别唯一确定两族参数，故每点各有一条母线。

## draft-c22-02

problem

证明球面 $x^2+y^2+z^2=1$ 不是直纹面。

solution

任一直线与球面至多有两个交点:设直线 $l(t)=p+td$($d\neq0$),代入球面方程得 $(p_1+td_1)^2+(p_2+td_2)^2+(p_3+td_3)^2=1$,即 $|d|^2t^2+2(p\cdot d)t+(|p|^2-1)=0$。因二次项系数 $|d|^2>0$,这是真正的二次方程,至多有两个实根;该二次多项式不可能恒为零(二次项系数非零)。故球面不含任何整条直线,即球面上不存在母线,球面不是直纹面。

answer

球面不是直纹面:任一直线与球面至多交于两点,球面不含整条直线。

scene_spec.objects[0]

证明球面 $x^2+y^2+z^2=1$ 不是直纹面。

scene_spec.objects[1]

球面不是直纹面:任一直线与球面至多交于两点,球面不含整条直线。

scene_spec.steps[0]

第一步:任一直线与球面至多有两个交点:设直线 $l(t)=p+td$($d\neq0$),代入球面方程得 $(p_1+td_1)^2+(p_2+td_2)^2+(p_3+td_3)^2=1$,即 $|d|^2t^2+2(p\cdot d)t+(|p|^2-1)=0$。

scene_spec.steps[1]

第二步:因二次项系数 $|d|^2>0$,这是真正的二次方程,至多有两个实根;该二次多项式不可能恒为零(二次项系数非零)。

scene_spec.steps[2]

第三步:故球面不含任何整条直线,即球面上不存在母线,球面不是直纹面。

## draft-c22-03

problem

求三次曲面$z=xy^2$上全部实直线，并判断每个点通过几条母线。

solution

设$p=(x_0,y_0,x_0y_0^2)$，方向$d=(a,b,c)\ne0$，将$p+td$代入。比较$t^3,t^2,t$系数得$ab^2=0$、$2ay_0b+x_0b^2=0$、$c=ay_0^2+2x_0y_0b$。若$b=0$，则$c=ay_0^2$且$a\ne0$，得到全部固定$y=v$的直线$(u,v,uv^2)$。若$b\ne0$，第一式给$a=0$，第二式给$x_0=0$，第三式给$c=0$，仅得到$y$轴$(0,u,0)$。前述直线全都满足曲面，故无遗漏。$x\ne0$的点只过一条固定$y$母线；$x=0$的曲面点同时过该母线和$y$轴，恰有两条。

answer

全部直线为$(u,v,uv^2)$（$v$固定）及$(0,u,0)$；$x\ne0$过一条，$x=0$过两条。

scene_spec.objects[0]

求三次曲面$z=xy^2$上全部实直线，并判断每个点通过几条母线。

scene_spec.objects[1]

全部直线为$(u,v,uv^2)$（$v$固定）及$(0,u,0)$；$x\ne0$过一条，$x=0$过两条。

scene_spec.steps[0]

第一步:设$p=(x_0,y_0,x_0y_0^2)$，方向$d=(a,b,c)\ne0$，将$p+td$代入。

scene_spec.steps[1]

第二步:比较$t^3,t^2,t$系数得$ab^2=0$、$2ay_0b+x_0b^2=0$、$c=ay_0^2+2x_0y_0b$。

scene_spec.steps[2]

第三步:若$b=0$，则$c=ay_0^2$且$a\ne0$，得到全部固定$y=v$的直线$(u,v,uv^2)$。

scene_spec.steps[3]

第四步:若$b\ne0$，第一式给$a=0$，第二式给$x_0=0$，第三式给$c=0$，仅得到$y$轴$(0,u,0)$。

scene_spec.steps[4]

第五步:前述直线全都满足曲面，故无遗漏。

scene_spec.steps[5]

第六步:$x\ne0$的点只过一条固定$y$母线；$x=0$的曲面点同时过该母线和$y$轴，恰有两条。

## draft-c22-04

problem

设实二次曲面$F(x)=x^{\mathsf T}Ax+2b^{\mathsf T}x+c=0$，$A=A^{\mathsf T}$。证明$p+td$（$d\ne0$）整条直线在曲面上的充要条件，并据此说明正定或负定$A$为何不允许母线。

solution

精确展开$F(p+td)=F(p)+2t(Ap+b)^{\mathsf T}d+t^2d^{\mathsf T}Ad$。它对所有实$t$为零，当且仅当三个系数全为零，即$F(p)=0$、$(Ap+b)^{\mathsf T}d=0$、$d^{\mathsf T}Ad=0$。充分性由代回恒等式立即成立。若$A$正定或负定，对$d\ne0$均有$d^{\mathsf T}Ad\ne0$，故没有整条母线；半定或不定时还必须核对点与混合项条件，存在零二次值方向本身并不充分。

answer

$F(p)=0$、$(Ap+b)^{\mathsf T}d=0$、$d^{\mathsf T}Ad=0$三条件充要；定号型没有母线。

scene_spec.objects[0]

设实二次曲面$F(x)=x^{\mathsf T}Ax+2b^{\mathsf T}x+c=0$，$A=A^{\mathsf T}$。证明$p+td$（$d\ne0$）整条直线在曲面上的充要条件，并据此说明正定或负定$A$为何不允许母线。

scene_spec.objects[1]

$F(p)=0$、$(Ap+b)^{\mathsf T}d=0$、$d^{\mathsf T}Ad=0$三条件充要；定号型没有母线。

scene_spec.steps[0]

第一步:精确展开$F(p+td)=F(p)+2t(Ap+b)^{\mathsf T}d+t^2d^{\mathsf T}Ad$。

scene_spec.steps[1]

第二步:它对所有实$t$为零，当且仅当三个系数全为零，即$F(p)=0$、$(Ap+b)^{\mathsf T}d=0$、$d^{\mathsf T}Ad=0$。

scene_spec.steps[2]

第三步:充分性由代回恒等式立即成立。

scene_spec.steps[3]

第四步:若$A$正定或负定，对$d\ne0$均有$d^{\mathsf T}Ad\ne0$，故没有整条母线；半定或不定时还必须核对点与混合项条件，存在零二次值方向本身并不充分。

## draft-c22-05

problem

证明双叶双曲面 $x^2+y^2-z^2=-1$ 不是直纹面。

solution

若双叶双曲面$x^2+y^2-z^2=-1$含直线$p+td$，$d\ne0$，比较系数有$p_1^2+p_2^2=p_3^2-1$、$d_1^2+d_2^2=d_3^2$及$p_1d_1+p_2d_2=p_3d_3$。若$d_3=0$，则$d_1=d_2=0$矛盾，故$d_3^2>0$。由Cauchy不等式，$(p_3d_3)^2\le(p_3^2-1)d_3^2<p_3^2d_3^2$，矛盾。因此不存在母线。

answer

双叶双曲面不是直纹面:假设整条直线在曲面上,多项式恒零给出三个系数方程,由柯西不等式导出 $|p_3d_3|<|p_3d_3|$ 的矛盾(证明见解法)。

scene_spec.objects[0]

证明双叶双曲面 $x^2+y^2-z^2=-1$ 不是直纹面。

scene_spec.objects[1]

双叶双曲面不是直纹面:假设整条直线在曲面上,多项式恒零给出三个系数方程,由柯西不等式导出 $|p_3d_3|<|p_3d_3|$ 的矛盾(证明见解法)。

scene_spec.steps[0]

第一步:若双叶双曲面$x^2+y^2-z^2=-1$含直线$p+td$，$d\ne0$，比较系数有$p_1^2+p_2^2=p_3^2-1$、$d_1^2+d_2^2=d_3^2$及$p_1d_1+p_2d_2=p_3d_3$。

scene_spec.steps[1]

第二步:若$d_3=0$，则$d_1=d_2=0$矛盾，故$d_3^2>0$。

scene_spec.steps[2]

第三步:由Cauchy不等式，$(p_3d_3)^2\le(p_3^2-1)d_3^2<p_3^2d_3^2$，矛盾。

scene_spec.steps[3]

第四步:因此不存在母线。

## draft-c23-01

problem

求等距变换 $T(x)=Ax+b$ 的逆变换，其中 $A=\begin{pmatrix}0&1&0\\-1&0&0\\0&0&1\end{pmatrix}$，$b=(1,2,3)$。

solution

$A$ 为正交矩阵,逆变换为 $T^{-1}(x)=A^{\mathsf T}x-A^{\mathsf T}b$。$A^{\mathsf T}=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix}$,$A^{\mathsf T}b=(0-2,\ 1+0,\ 0+3)=(-2,1,3)$。故 $T^{-1}(x)=A^{\mathsf T}x-(-2,1,3)=A^{\mathsf T}x+(2,-1,-3)$。验证:$T(T^{-1}(x))=A(A^{\mathsf T}x-A^{\mathsf T}b)+b=x-b+b=x$ ✓。

answer

$T^{-1}(x)=A^{\mathsf T}x+(2,-1,-3)$,即 $T^{-1}(x,y,z)=(-y+2,\,x-1,\,z-3)$。

scene_spec.objects[0]

求等距变换 $T(x)=Ax+b$ 的逆变换，其中 $A=\begin{pmatrix}0&1&0\\-1&0&0\\0&0&1\end{pmatrix}$，$b=(1,2,3)$。

scene_spec.objects[1]

$T^{-1}(x)=A^{\mathsf T}x+(2,-1,-3)$,即 $T^{-1}(x,y,z)=(-y+2,\,x-1,\,z-3)$。

scene_spec.steps[0]

第一步:$A$ 为正交矩阵,逆变换为 $T^{-1}(x)=A^{\mathsf T}x-A^{\mathsf T}b$。

scene_spec.steps[1]

第二步:$A^{\mathsf T}=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix}$,$A^{\mathsf T}b=(0-2,\ 1+0,\ 0+3)=(-2,1,3)$。

scene_spec.steps[2]

第三步:故 $T^{-1}(x)=A^{\mathsf T}x-(-2,1,3)=A^{\mathsf T}x+(2,-1,-3)$。

scene_spec.steps[3]

第四步:验证:$T(T^{-1}(x))=A(A^{\mathsf T}x-A^{\mathsf T}b)+b=x-b+b=x$ ✓。

## draft-c23-02

problem

证明:若 $A$ 为正交矩阵,则等距变换 $T(x)=Ax+b$ 保持任意两点间的距离,即 $\|T(x)-T(y)\|=\|x-y\|$。

solution

$\|T(x)-T(y)\|=\|(Ax+b)-(Ay+b)\|=\|A(x-y)\|$。由正交矩阵的性质 $\|Au\|^2=(Au)^{\mathsf T}(Au)=u^{\mathsf T}A^{\mathsf T}Au=u^{\mathsf T}u=\|u\|^2$,故 $\|A(x-y)\|=\|x-y\|$,距离保持不变。

answer

证明见解法(核心:$\|Au\|^2=u^{\mathsf T}A^{\mathsf T}Au=u^{\mathsf T}u$)。

scene_spec.objects[0]

证明:若 $A$ 为正交矩阵,则等距变换 $T(x)=Ax+b$ 保持任意两点间的距离,即 $\|T(x)-T(y)\|=\|x-y\|$。

scene_spec.objects[1]

证明见解法(核心:$\|Au\|^2=u^{\mathsf T}A^{\mathsf T}Au=u^{\mathsf T}u$)。

scene_spec.steps[0]

第一步:$\|T(x)-T(y)\|=\|(Ax+b)-(Ay+b)\|=\|A(x-y)\|$。

scene_spec.steps[1]

第二步:由正交矩阵的性质 $\|Au\|^2=(Au)^{\mathsf T}(Au)=u^{\mathsf T}A^{\mathsf T}Au=u^{\mathsf T}u=\|u\|^2$,故 $\|A(x-y)\|=\|x-y\|$,距离保持不变。

## draft-c23-03

problem

分析等距变换$T(x,y,z)=(x+2,4-y,z)$：说明其几何类型，求固定点集合、逆变换及$T^2$，并证明它保持距离。

solution

线性部分$A=\operatorname{diag}(1,-1,1)$满足$A^{\mathsf T}A=I$，故两点之差的长度保持。$T$是关于$y=2$的反射，再沿该平面平移$(2,0,0)$，为滑移反射。固定点需$x+2=x$，不可能，故固定点集合为空。反解得$T^{-1}(u,v,w)=(u-2,4-v,w)$，复合得$T^2(x,y,z)=(x+4,y,z)$。它虽反转定向，却不是具有固定平面的单纯反射。

answer

滑移反射，无固定点；$T^{-1}=(x-2,4-y,z)$，$T^2=(x+4,y,z)$，保持距离。

scene_spec.objects[0]

分析等距变换$T(x,y,z)=(x+2,4-y,z)$：说明其几何类型，求固定点集合、逆变换及$T^2$，并证明它保持距离。

scene_spec.objects[1]

滑移反射，无固定点；$T^{-1}=(x-2,4-y,z)$，$T^2=(x+4,y,z)$，保持距离。

scene_spec.steps[0]

第一步:线性部分$A=\operatorname{diag}(1,-1,1)$满足$A^{\mathsf T}A=I$，故两点之差的长度保持。

scene_spec.steps[1]

第二步:$T$是关于$y=2$的反射，再沿该平面平移$(2,0,0)$，为滑移反射。

scene_spec.steps[2]

第三步:固定点需$x+2=x$，不可能，故固定点集合为空。

scene_spec.steps[3]

第四步:反解得$T^{-1}(u,v,w)=(u-2,4-v,w)$，复合得$T^2(x,y,z)=(x+4,y,z)$。

scene_spec.steps[4]

第五步:它虽反转定向，却不是具有固定平面的单纯反射。

## draft-c23-04

problem

取单位法向量$n=(2,-1,2)/3$，两平面$n\cdot x=1$、$n\cdot x=5/2$。求先关于前者、再关于后者反射的复合，说明逆序、固定点和两平面间距。

solution

记$R_a(x)=x-2(n\cdot x-a)n$，因$\|n\|=1$，$n\cdot R_a(x)=2a-n\cdot x$。所以$R_bR_a(x)=x+2(b-a)n$。代入$a=1,b=5/2$，复合为$x+(2,-1,2)$，是非零平移，故没有固定点；逆序为$x-(2,-1,2)$，正是逆变换。单位法向量使平面距离等于$|b-a|=3/2$，平移距离为$3$。

answer

复合$x\mapsto x+(2,-1,2)$；逆序反向平移，无固定点，平面间距$3/2$。

scene_spec.objects[0]

取单位法向量$n=(2,-1,2)/3$，两平面$n\cdot x=1$、$n\cdot x=5/2$。求先关于前者、再关于后者反射的复合，说明逆序、固定点和两平面间距。

scene_spec.objects[1]

复合$x\mapsto x+(2,-1,2)$；逆序反向平移，无固定点，平面间距$3/2$。

scene_spec.steps[0]

第一步:记$R_a(x)=x-2(n\cdot x-a)n$，因$\|n\|=1$，$n\cdot R_a(x)=2a-n\cdot x$。

scene_spec.steps[1]

第二步:所以$R_bR_a(x)=x+2(b-a)n$。

scene_spec.steps[2]

第三步:代入$a=1,b=5/2$，复合为$x+(2,-1,2)$，是非零平移，故没有固定点；逆序为$x-(2,-1,2)$，正是逆变换。

scene_spec.steps[3]

第四步:单位法向量使平面距离等于$|b-a|=3/2$，平移距离为$3$。

## draft-c23-05

problem

把等距变换 $T(x)=Ax+b$ 分解为绕某轴的旋转与沿该轴平移的复合(螺旋运动),其中 $A=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix}$(绕 $z$ 轴旋转 $90^\circ$),$b=(1,2,3)$。

solution

旋转轴方向 $v=(0,0,1)$。把 $b$ 分解为沿轴分量与垂直分量:$b_\parallel=(b\cdot v)v=(0,0,3)$,$b_\perp=b-b_\parallel=(1,2,0)$。在 $v^\perp$ 上解 $(I-A)p=b_\perp$:$I-A=\begin{pmatrix}1&1&0\\-1&1&0\\0&0&0\end{pmatrix}$,方程 $p_1+p_2=1$,$-p_1+p_2=2$,解得 $p_1=-\frac12,p_2=\frac32$;取 $p=(-\frac12,\frac32,0)$。则 $T(x)=A(x-p)+p+b_\parallel$:验证右端 $=Ax+(I-A)p+(0,0,3)=Ax+(1,2,0)+(0,0,3)=Ax+b=T(x)$ ✓。故 $T$ 是「绕过点 $p$、平行于 $z$ 轴的直线旋转 $90^\circ$」与「沿 $z$ 轴平移 $(0,0,3)$」的复合(螺旋运动)。

answer

$T=$ 绕过 $p=(-\frac12,\frac32,0)$ 且平行于 $z$ 轴的直线旋转 $90^\circ$,复合沿 $z$ 轴平移 $(0,0,3)$。

scene_spec.objects[0]

把等距变换 $T(x)=Ax+b$ 分解为绕某轴的旋转与沿该轴平移的复合(螺旋运动),其中 $A=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix}$(绕 $z$ 轴旋转 $90^\circ$),$b=(1,2,3)$。

scene_spec.objects[1]

$T=$ 绕过 $p=(-\frac12,\frac32,0)$ 且平行于 $z$ 轴的直线旋转 $90^\circ$,复合沿 $z$ 轴平移 $(0,0,3)$。

scene_spec.steps[0]

第一步:旋转轴方向 $v=(0,0,1)$。

scene_spec.steps[1]

第二步:把 $b$ 分解为沿轴分量与垂直分量:$b_\parallel=(b\cdot v)v=(0,0,3)$,$b_\perp=b-b_\parallel=(1,2,0)$。

scene_spec.steps[2]

第三步:在 $v^\perp$ 上解 $(I-A)p=b_\perp$:$I-A=\begin{pmatrix}1&1&0\\-1&1&0\\0&0&0\end{pmatrix}$,方程 $p_1+p_2=1$,$-p_1+p_2=2$,解得 $p_1=-\frac12,p_2=\frac32$;取 $p=(-\frac12,\frac32,0)$。

scene_spec.steps[3]

第四步:则 $T(x)=A(x-p)+p+b_\parallel$:验证右端 $=Ax+(I-A)p+(0,0,3)=Ax+(1,2,0)+(0,0,3)=Ax+b=T(x)$ ✓。

scene_spec.steps[4]

第五步:故 $T$ 是「绕过点 $p$、平行于 $z$ 轴的直线旋转 $90^\circ$」与「沿 $z$ 轴平移 $(0,0,3)$」的复合(螺旋运动)。
