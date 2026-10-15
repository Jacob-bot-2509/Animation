## draft-c24-01

problem

解释剪切变换 $\begin{cases}x'=x+2y\\ y'=y\end{cases}$ 对单位正方形 $[0,1]\times[0,1]$ 的几何作用，并求像的面积。

solution

$A=\begin{pmatrix}1&2\\0&1\end{pmatrix}$给$(x,y)\mapsto(x+2y,y)$。单位正方形四顶点依次变为$(0,0),(1,0),(3,1),(2,1)$；水平边方向仍为$(1,0)$，原竖直边方向变为$(2,1)$，不再竖直。像是平行四边形，面积乘以$|\det A|=1$，故面积仍为$1$。

answer

单位正方形映为平行四边形(顶点 $(0,0),(1,0),(2,1),(3,1)$),面积为 $1$(不变)。

scene_spec.objects[0]

解释剪切变换 $\begin{cases}x'=x+2y\\ y'=y\end{cases}$ 对单位正方形 $[0,1]\times[0,1]$ 的几何作用，并求像的面积。

scene_spec.objects[1]

单位正方形映为平行四边形(顶点 $(0,0),(1,0),(2,1),(3,1)$),面积为 $1$(不变)。

scene_spec.steps[0]

第一步:$A=\begin{pmatrix}1&2\\0&1\end{pmatrix}$给$(x,y)\mapsto(x+2y,y)$。

scene_spec.steps[1]

第二步:单位正方形四顶点依次变为$(0,0),(1,0),(3,1),(2,1)$；水平边方向仍为$(1,0)$，原竖直边方向变为$(2,1)$，不再竖直。

scene_spec.steps[2]

第三步:像是平行四边形，面积乘以$|\det A|=1$，故面积仍为$1$。

## draft-c24-02

problem

仿射映射$T(x,y)=(1+x+y,-1+2x+2y)$作用于单位圆$x^2+y^2=1$。求完整像集和每个像点在圆上的原像数，说明为什么不能使用可逆仿射的椭圆结论。

solution

记$t=x+y$，由$(x-y)^2=2-t^2\ge0$，$|t|\le\sqrt2$。反过来对该区间任意$t$，取$(x,y)=((t+s)/2,(t-s)/2)$、$s=\pm\sqrt{2-t^2}$，便有$x^2+y^2=1$。故完整像为线段$\{(1+t,-1+2t):|t|\le\sqrt2\}$；内部像点有两个不同圆上原像，端点各有一个，线段外没有。线性部分秩为$1$、行列式为零，圆的二维仿射坐标不能反解为可逆椭圆。

answer

像为上述闭线段；内部两原像、端点一原像、外部零原像。

scene_spec.objects[0]

仿射映射$T(x,y)=(1+x+y,-1+2x+2y)$作用于单位圆$x^2+y^2=1$。求完整像集和每个像点在圆上的原像数，说明为什么不能使用可逆仿射的椭圆结论。

scene_spec.objects[1]

像为上述闭线段；内部两原像、端点一原像、外部零原像。

scene_spec.steps[0]

第一步:记$t=x+y$，由$(x-y)^2=2-t^2\ge0$，$|t|\le\sqrt2$。

scene_spec.steps[1]

第二步:反过来对该区间任意$t$，取$(x,y)=((t+s)/2,(t-s)/2)$、$s=\pm\sqrt{2-t^2}$，便有$x^2+y^2=1$。

scene_spec.steps[2]

第三步:故完整像为线段$\{(1+t,-1+2t):|t|\le\sqrt2\}$；内部像点有两个不同圆上原像，端点各有一个，线段外没有。

scene_spec.steps[3]

第四步:线性部分秩为$1$、行列式为零，圆的二维仿射坐标不能反解为可逆椭圆。

## draft-c24-03

problem

设$T_t(x)=A_tx+b$，$A_t=\begin{pmatrix}1&2\\t&t^2\end{pmatrix}$，$t\in\mathbb R$。求可逆参数及逆矩阵，并在每个奇异参数下给整个平面像、相容条件与全部纤维。

solution

$\det A_t=t(t-2)$，故$t\ne0,2$时可逆，逆为$[t(t-2)]^{-1}\begin{pmatrix}t^2&-2\\-t&1\end{pmatrix}$。记像点为$(u,v)$，$s=u-b_1$。$t=0$时像为$b+\operatorname{span}(1,0)$，条件$v=b_2$；$t=2$时像为$b+\operatorname{span}(1,2)$，条件$v-b_2=2s$。两奇异参数下，满足条件的全部原像都是$(s-2r,r)$，$r\in\mathbb R$；不满足条件则无原像。核方向为$(-2,1)$，两种奇异像方向不同，不能只检查一个退化值。

answer

可逆$t\notin\{0,2\}$；逆如上；奇异像与全部纤维如上。

scene_spec.objects[0]

设$T_t(x)=A_tx+b$，$A_t=\begin{pmatrix}1&2\\t&t^2\end{pmatrix}$，$t\in\mathbb R$。求可逆参数及逆矩阵，并在每个奇异参数下给整个平面像、相容条件与全部纤维。

scene_spec.objects[1]

可逆$t\notin\{0,2\}$；逆如上；奇异像与全部纤维如上。

scene_spec.steps[0]

第一步:$\det A_t=t(t-2)$，故$t\ne0,2$时可逆，逆为$[t(t-2)]^{-1}\begin{pmatrix}t^2&-2\\-t&1\end{pmatrix}$。

scene_spec.steps[1]

第二步:记像点为$(u,v)$，$s=u-b_1$。

scene_spec.steps[2]

第三步:$t=0$时像为$b+\operatorname{span}(1,0)$，条件$v=b_2$；$t=2$时像为$b+\operatorname{span}(1,2)$，条件$v-b_2=2s$。

scene_spec.steps[3]

第四步:两奇异参数下，满足条件的全部原像都是$(s-2r,r)$，$r\in\mathbb R$；不满足条件则无原像。

scene_spec.steps[4]

第五步:核方向为$(-2,1)$，两种奇异像方向不同，不能只检查一个退化值。

## draft-c24-04

problem

未知仿射映射将$(0,0),(1,0),(0,1)$依次映到$(1,-1),(3,0),(0,2)$。求映射、原三角形的像面积与像重心，以及直线$x+y=1$的像方程。

solution

原点像给$b=(1,-1)$，另两像减$b$给矩阵列$(2,1)$、$(-1,3)$，故$T(x)=Ax+b$、$A=\begin{pmatrix}2&-1\\1&3\end{pmatrix}$，$\det A=7$。原三角形面积$1/2$，像面积$7/2$。仿射保平均，原重心$(1/3,1/3)$像为$(4/3,1/3)$，与三个像顶点平均一致。直线点$(t,1-t)$像为$(3t,2-2t)$，故$2u+3v=6$；反过来该方程的任意点取$t=u/3$即可得到，故像方程无额外点。

answer

$A=\begin{pmatrix}2&-1\\1&3\end{pmatrix}$、$b=(1,-1)$；面积$7/2$，重心$(4/3,1/3)$，像直线$2u+3v=6$。

scene_spec.objects[0]

未知仿射映射将$(0,0),(1,0),(0,1)$依次映到$(1,-1),(3,0),(0,2)$。求映射、原三角形的像面积与像重心，以及直线$x+y=1$的像方程。

scene_spec.objects[1]

$A=\begin{pmatrix}2&-1\\1&3\end{pmatrix}$、$b=(1,-1)$；面积$7/2$，重心$(4/3,1/3)$，像直线$2u+3v=6$。

scene_spec.steps[0]

第一步:原点像给$b=(1,-1)$，另两像减$b$给矩阵列$(2,1)$、$(-1,3)$，故$T(x)=Ax+b$、$A=\begin{pmatrix}2&-1\\1&3\end{pmatrix}$，$\det A=7$。

scene_spec.steps[1]

第二步:原三角形面积$1/2$，像面积$7/2$。

scene_spec.steps[2]

第三步:仿射保平均，原重心$(1/3,1/3)$像为$(4/3,1/3)$，与三个像顶点平均一致。

scene_spec.steps[3]

第四步:直线点$(t,1-t)$像为$(3t,2-2t)$，故$2u+3v=6$；反过来该方程的任意点取$t=u/3$即可得到，故像方程无额外点。

## draft-c24-05

problem

证明可逆仿射变换 $T(x)=Ax+b$ 把直线映成直线、把平行直线映成平行直线、保持共线三点的简单比，并说明圆在一般仿射变换下为何变成椭圆。

solution

直线:设直线 $l:p+td$,则像为 $T(p+td)=Ap+b+tAd$,仍是直线(方向 $Ad$,$A$ 可逆故 $Ad\neq0$)。平行线:两条平行直线有相同方向 $d$,像的方向同为 $Ad$,故仍平行。简单比:设共线三点 $A,B,C$ 满足 $C=A+\lambda(B-A)$,则 $T(C)=T(A)+\lambda(T(B)-T(A))$,分比 $\lambda$ 不变。圆→椭圆:单位圆上点 $u$ 满足 $u^{\mathsf T}u=1$;其像 $x=Au+b$ 满足 $(A^{-1}(x-b))^{\mathsf T}(A^{-1}(x-b))=1$,即 $(x-b)^{\mathsf T}(A^{-1})^{\mathsf T}A^{-1}(x-b)=1$。矩阵 $(A^{-1})^{\mathsf T}A^{-1}$ 对称正定,这是中心在 $b$ 的椭圆方程——一般仿射变换不保圆(仅当 $A$ 为正交矩阵乘常数时才保圆)。

answer

证明见解法(直线/平行/简单比均保持;圆的像为对称正定二次型 $=1$,即椭圆)。

scene_spec.objects[0]

证明可逆仿射变换 $T(x)=Ax+b$ 把直线映成直线、把平行直线映成平行直线、保持共线三点的简单比，并说明圆在一般仿射变换下为何变成椭圆。

scene_spec.objects[1]

证明见解法(直线/平行/简单比均保持;圆的像为对称正定二次型 $=1$,即椭圆)。

scene_spec.steps[0]

第一步:直线:设直线 $l:p+td$,则像为 $T(p+td)=Ap+b+tAd$,仍是直线(方向 $Ad$,$A$ 可逆故 $Ad\neq0$)。

scene_spec.steps[1]

第二步:平行线:两条平行直线有相同方向 $d$,像的方向同为 $Ad$,故仍平行。

scene_spec.steps[2]

第三步:简单比:设共线三点 $A,B,C$ 满足 $C=A+\lambda(B-A)$,则 $T(C)=T(A)+\lambda(T(B)-T(A))$,分比 $\lambda$ 不变。

scene_spec.steps[3]

第四步:圆→椭圆:单位圆上点 $u$ 满足 $u^{\mathsf T}u=1$;其像 $x=Au+b$ 满足 $(A^{-1}(x-b))^{\mathsf T}(A^{-1}(x-b))=1$,即 $(x-b)^{\mathsf T}(A^{-1})^{\mathsf T}A^{-1}(x-b)=1$。

scene_spec.steps[4]

第五步:矩阵 $(A^{-1})^{\mathsf T}A^{-1}$ 对称正定,这是中心在 $b$ 的椭圆方程——一般仿射变换不保圆(仅当 $A$ 为正交矩阵乘常数时才保圆)。

## draft-c25-01

problem

分类圆锥$x^2+y^2=z^2$与过顶点平面$z=ax$（$a\in\mathbb R$）的实交集，并给所有非单点分支的完整参数式。

solution

代入得$y^2=(a^2-1)x^2$。若$|a|<1$，两边符号迫使$x=y=z=0$，仅顶点。若$|a|=1$，$y=0,z=ax$，是一条直线$(t,0,at)$。若$|a|>1$，分解为两直线$(t,\pm\sqrt{a^2-1}t,at)$；它们不同且只在顶点相交。每个参数$t$取全部实数，代回原方程验证，分类无遗漏。

answer

$|a|<1$单点，$|a|=1$一条母线，$|a|>1$两条母线；参数式如上。

scene_spec.objects[0]

分类圆锥$x^2+y^2=z^2$与过顶点平面$z=ax$（$a\in\mathbb R$）的实交集，并给所有非单点分支的完整参数式。

scene_spec.objects[1]

$|a|<1$单点，$|a|=1$一条母线，$|a|>1$两条母线；参数式如上。

scene_spec.steps[0]

第一步:代入得$y^2=(a^2-1)x^2$。

scene_spec.steps[1]

第二步:若$|a|<1$，两边符号迫使$x=y=z=0$，仅顶点。

scene_spec.steps[2]

第三步:若$|a|=1$，$y=0,z=ax$，是一条直线$(t,0,at)$。

scene_spec.steps[3]

第四步:若$|a|>1$，分解为两直线$(t,\pm\sqrt{a^2-1}t,at)$；它们不同且只在顶点相交。

scene_spec.steps[4]

第五步:每个参数$t$取全部实数，代回原方程验证，分类无遗漏。

## draft-c25-02

problem

求两圆柱面 $x^2+y^2=1$ 与 $y^2+z^2=1$ 的交线的参数方程，并说明交线由几支组成、在何处相接。

solution

由第一个柱面取 $x=\cos t$,$y=\sin t$。代入第二个柱面:$z^2=1-y^2=1-\sin^2t=\cos^2t$,故 $z=\pm\cos t$。交线由两支组成:$l_1:(\cos t,\sin t,\cos t)$ 与 $l_2:(\cos t,\sin t,-\cos t)$。两支在 $\cos t=0$ 处相接,即点 $(0,1,0)$ 与 $(0,-1,0)$。

answer

两支:$l_1:(\cos t,\sin t,\cos t)$ 与 $l_2:(\cos t,\sin t,-\cos t)$,在 $(0,\pm1,0)$ 处相接。

scene_spec.objects[0]

求两圆柱面 $x^2+y^2=1$ 与 $y^2+z^2=1$ 的交线的参数方程，并说明交线由几支组成、在何处相接。

scene_spec.objects[1]

两支:$l_1:(\cos t,\sin t,\cos t)$ 与 $l_2:(\cos t,\sin t,-\cos t)$,在 $(0,\pm1,0)$ 处相接。

scene_spec.steps[0]

第一步:由第一个柱面取 $x=\cos t$,$y=\sin t$。

scene_spec.steps[1]

第二步:代入第二个柱面:$z^2=1-y^2=1-\sin^2t=\cos^2t$,故 $z=\pm\cos t$。

scene_spec.steps[2]

第三步:交线由两支组成:$l_1:(\cos t,\sin t,\cos t)$ 与 $l_2:(\cos t,\sin t,-\cos t)$。

scene_spec.steps[3]

第四步:两支在 $\cos t=0$ 处相接,即点 $(0,1,0)$ 与 $(0,-1,0)$。

## draft-c25-03

problem

求圆锥面 $x^2+y^2=z^2$ 与平面 $z=1+y$ 的交线的参数方程，并判断该交线是什么曲线。

solution

令 $x=t$。由 $z=1+y$ 得 $z=1+y$,代入锥面方程:$t^2+y^2=(1+y)^2$,即 $t^2=1+2y$,$y=\frac{t^2-1}{2}$,故 $z=1+\frac{t^2-1}{2}=\frac{t^2+1}{2}$。参数方程:$(t,\frac{t^2-1}{2},\frac{t^2+1}{2})$。验证:消去参数得 $x^2=2y+1$ 且 $z=1+y$,它是平面 $z=1+y$ 内的抛物线($y=\frac{x^2-1}{2}$)。

answer

交线为抛物线:$(t,\frac{t^2-1}{2},\frac{t^2+1}{2})$,即 $\begin{cases}y=\frac{x^2-1}{2}\\ z=1+y\end{cases}$。

scene_spec.objects[0]

求圆锥面 $x^2+y^2=z^2$ 与平面 $z=1+y$ 的交线的参数方程，并判断该交线是什么曲线。

scene_spec.objects[1]

交线为抛物线:$(t,\frac{t^2-1}{2},\frac{t^2+1}{2})$,即 $\begin{cases}y=\frac{x^2-1}{2}\\ z=1+y\end{cases}$。

scene_spec.steps[0]

第一步:令 $x=t$。

scene_spec.steps[1]

第二步:由 $z=1+y$ 得 $z=1+y$,代入锥面方程:$t^2+y^2=(1+y)^2$,即 $t^2=1+2y$,$y=\frac{t^2-1}{2}$,故 $z=1+\frac{t^2-1}{2}=\frac{t^2+1}{2}$。

scene_spec.steps[2]

第三步:参数方程:$(t,\frac{t^2-1}{2},\frac{t^2+1}{2})$。

scene_spec.steps[3]

第四步:验证:消去参数得 $x^2=2y+1$ 且 $z=1+y$,它是平面 $z=1+y$ 内的抛物线($y=\frac{x^2-1}{2}$)。

## draft-c25-04

problem

求柱面$x^2+y^2=4$与$z=x^2$的完整交线参数式，并证明交线不包含于任何平面。

solution

圆柱约束给$x=2\cos t,y=2\sin t$，另一个约束给$z=4\cos^2t$，故完整交线为$(2\cos t,2\sin t,4\cos^2t)$，$0\le t<2\pi$。若整条交线在$Ax+By+Cz=D$中，则$2A\cos t+2B\sin t+2C\cos2t+(2C-D)=0$对所有$t$成立。对$1,\cos t,\sin t,\cos2t$分别积分正交消去，得$A=B=C=D=0$，这不是平面方程，矛盾。因此是非平面闭交线。

answer

参数$(2\cos t,2\sin t,4\cos^2t)$，$0\le t<2\pi$；交线非平面。

scene_spec.objects[0]

求柱面$x^2+y^2=4$与$z=x^2$的完整交线参数式，并证明交线不包含于任何平面。

scene_spec.objects[1]

参数$(2\cos t,2\sin t,4\cos^2t)$，$0\le t<2\pi$；交线非平面。

scene_spec.steps[0]

第一步:圆柱约束给$x=2\cos t,y=2\sin t$，另一个约束给$z=4\cos^2t$，故完整交线为$(2\cos t,2\sin t,4\cos^2t)$，$0\le t<2\pi$。

scene_spec.steps[1]

第二步:若整条交线在$Ax+By+Cz=D$中，则$2A\cos t+2B\sin t+2C\cos2t+(2C-D)=0$对所有$t$成立。

scene_spec.steps[2]

第三步:对$1,\cos t,\sin t,\cos2t$分别积分正交消去，得$A=B=C=D=0$，这不是平面方程，矛盾。

scene_spec.steps[3]

第四步:因此是非平面闭交线。

## draft-c25-05

problem

求球$x^2+y^2+z^2=1$与抛物柱面$y=x^2$的实交线，给参数域、分支连接关系，证明交线正则且非平面。

solution

置$x=t$，则$y=t^2$、$z=\pm\sqrt{1-t^2-t^4}$。根号非负等价于$|t|\le r=\sqrt{(\sqrt5-1)/2}$。两图形弧在$t=\pm r$的点$(\pm r,r^2,0)$连接，合为一条闭曲线，不能把正负图形弧误称为两个连通分量。正则性由梯度$(2t,2t^2,2z)$与$(-2t,1,0)$线性无关证明：$z\ne0$时明显；$z=0$时$t\ne0$，若成比例，第一坐标给比例$-1$而第二要求$2t^2=-1$，不可能。根号图形在端点不能充当光滑参数，可在端点改用$z$及$x=\pm\sqrt{(-1+\sqrt{5-4z^2})/2}$作为局部参数。若整条曲线在$Ax+By+Cz=D$中，比较同$t$的正负$z$得$C=0$；继而$At+Bt^2-D$在区间恒零，得$A=B=D=0$，矛盾。

answer

两弧$(t,t^2,\pm\sqrt{1-t^2-t^4})$，$|t|\le\sqrt{(\sqrt5-1)/2}$；连接为一条正则非平面闭曲线。

scene_spec.objects[0]

求球$x^2+y^2+z^2=1$与抛物柱面$y=x^2$的实交线，给参数域、分支连接关系，证明交线正则且非平面。

scene_spec.objects[1]

两弧$(t,t^2,\pm\sqrt{1-t^2-t^4})$，$|t|\le\sqrt{(\sqrt5-1)/2}$；连接为一条正则非平面闭曲线。

scene_spec.steps[0]

第一步:置$x=t$，则$y=t^2$、$z=\pm\sqrt{1-t^2-t^4}$。

scene_spec.steps[1]

第二步:根号非负等价于$|t|\le r=\sqrt{(\sqrt5-1)/2}$。

scene_spec.steps[2]

第三步:两图形弧在$t=\pm r$的点$(\pm r,r^2,0)$连接，合为一条闭曲线，不能把正负图形弧误称为两个连通分量。

scene_spec.steps[3]

第四步:正则性由梯度$(2t,2t^2,2z)$与$(-2t,1,0)$线性无关证明：$z\ne0$时明显；$z=0$时$t\ne0$，若成比例，第一坐标给比例$-1$而第二要求$2t^2=-1$，不可能。

scene_spec.steps[4]

第五步:根号图形在端点不能充当光滑参数，可在端点改用$z$及$x=\pm\sqrt{(-1+\sqrt{5-4z^2})/2}$作为局部参数。

scene_spec.steps[5]

第六步:若整条曲线在$Ax+By+Cz=D$中，比较同$t$的正负$z$得$C=0$；继而$At+Bt^2-D$在区间恒零，得$A=B=D=0$，矛盾。

## draft-c26-01

problem

令$n=(1,2,-1)$、$d=(1,1,0)$，定义$P(x)=x-(n\cdot x)d/3$。求矩阵、核与像，证明其为沿$d$投影到$n\cdot x=0$的斜投影，判断是否为Euclidean正交投影。

solution

$n\cdot d=3$，所以$Pd=0$且$n\cdot Px=0$；对$n\cdot x=0$的向量有$Px=x$。因此像为$n^{\perp}$，核为$\operatorname{span}(d)$，$P^2=P$，秩$2$。矩阵为$\begin{pmatrix}2/3&-2/3&1/3\\-1/3&1/3&1/3\\0&0&1\end{pmatrix}$。核方向$d$不平行法向量$n$，矩阵也不对称，故不是Euclidean正交投影；分解$x=Px+(n\cdot x)d/3$唯一，说明投影方向。

answer

$\ker P=\operatorname{span}(1,1,0)$，$\operatorname{im}P=n^{\perp}$，$P^2=P$；斜投影而非Euclidean正交投影。

scene_spec.objects[0]

令$n=(1,2,-1)$、$d=(1,1,0)$，定义$P(x)=x-(n\cdot x)d/3$。求矩阵、核与像，证明其为沿$d$投影到$n\cdot x=0$的斜投影，判断是否为Euclidean正交投影。

scene_spec.objects[1]

$\ker P=\operatorname{span}(1,1,0)$，$\operatorname{im}P=n^{\perp}$，$P^2=P$；斜投影而非Euclidean正交投影。

scene_spec.steps[0]

第一步:$n\cdot d=3$，所以$Pd=0$且$n\cdot Px=0$；对$n\cdot x=0$的向量有$Px=x$。

scene_spec.steps[1]

第二步:因此像为$n^{\perp}$，核为$\operatorname{span}(d)$，$P^2=P$，秩$2$。

scene_spec.steps[2]

第三步:矩阵为$\begin{pmatrix}2/3&-2/3&1/3\\-1/3&1/3&1/3\\0&0&1\end{pmatrix}$。

scene_spec.steps[3]

第四步:核方向$d$不平行法向量$n$，矩阵也不对称，故不是Euclidean正交投影；分解$x=Px+(n\cdot x)d/3$唯一，说明投影方向。

## draft-c26-02

problem

分类所有保持两条坐标轴各自不变、并将单位圆映到自身的实线性映射$A:\mathbb R^2\to\mathbb R^2$。分别给其固定点集合与定向。

solution

两轴各自不变使矩阵为$\operatorname{diag}(a,b)$。单位基向量在圆上，其像也必须在圆上，所以$|a|=|b|=1$；反之这四个对角矩阵均保持整个单位圆。$A=I$固定全平面且保定向；$A=-I$仅固定原点且保定向；$\operatorname{diag}(1,-1)$固定$x$轴并反定向；$\operatorname{diag}(-1,1)$固定$y$轴并反定向。

answer

仅四个$\operatorname{diag}(\pm1,\pm1)$；固定集合和定向如上。

scene_spec.objects[0]

分类所有保持两条坐标轴各自不变、并将单位圆映到自身的实线性映射$A:\mathbb R^2\to\mathbb R^2$。分别给其固定点集合与定向。

scene_spec.objects[1]

仅四个$\operatorname{diag}(\pm1,\pm1)$；固定集合和定向如上。

scene_spec.steps[0]

第一步:两轴各自不变使矩阵为$\operatorname{diag}(a,b)$。

scene_spec.steps[1]

第二步:单位基向量在圆上，其像也必须在圆上，所以$|a|=|b|=1$；反之这四个对角矩阵均保持整个单位圆。

scene_spec.steps[2]

第三步:$A=I$固定全平面且保定向；$A=-I$仅固定原点且保定向；$\operatorname{diag}(1,-1)$固定$x$轴并反定向；$\operatorname{diag}(-1,1)$固定$y$轴并反定向。

## draft-c26-03

problem

对$A=\begin{pmatrix}1&2\\0&-1\end{pmatrix}$，证明$A^2=I$，求固定线与变号线，判断是否为Euclidean反射。说明线性对合为何不一定是等距变换。

solution

$A(x,y)=(x+2y,-y)$，直接再作用给$(x,y)$，所以$A^2=I$。固定向量满足$y=0$，固定线为$x$轴；变号向量满足$x=-y$，变号线为$\operatorname{span}(-1,1)$，两者独立但不垂直。$\|Ae_2\|^2=\|(2,-1)\|^2=5\ne1$，因此不保距离，不是Euclidean平面反射。任意向量唯一分解为这两条线的向量，$A$保持第一分量并将第二变号，是斜分解下的线性对合。

answer

线性对合，固定线$x$轴、变号线$y=-x$；不等距，不是Euclidean反射。

scene_spec.objects[0]

对$A=\begin{pmatrix}1&2\\0&-1\end{pmatrix}$，证明$A^2=I$，求固定线与变号线，判断是否为Euclidean反射。说明线性对合为何不一定是等距变换。

scene_spec.objects[1]

线性对合，固定线$x$轴、变号线$y=-x$；不等距，不是Euclidean反射。

scene_spec.steps[0]

第一步:$A(x,y)=(x+2y,-y)$，直接再作用给$(x,y)$，所以$A^2=I$。

scene_spec.steps[1]

第二步:固定向量满足$y=0$，固定线为$x$轴；变号向量满足$x=-y$，变号线为$\operatorname{span}(-1,1)$，两者独立但不垂直。

scene_spec.steps[2]

第三步:$\|Ae_2\|^2=\|(2,-1)\|^2=5\ne1$，因此不保距离，不是Euclidean平面反射。

scene_spec.steps[3]

第四步:任意向量唯一分解为这两条线的向量，$A$保持第一分量并将第二变号，是斜分解下的线性对合。

## draft-c26-04

problem

在$\mathbb R^4$中比较$T(x)=(x_3,x_4,0,0)$与$U(x)=(x_2,x_3,0,0)$。求迭代像维数与最小归零次数，证明它们虽秩相同却不相似，并判断可否对角化。

solution

两者像维数均为$2$。$T^2=0$且$T\ne0$，像维数序列为$4,2,0$；$U^2(x)=(x_3,0,0,0)\ne0$、$U^3=0$，像维数为$4,2,1,0$。相似会保持所有幂的秩或最小归零次数，故两者不相似。若一个非零幂零实或复矩阵可对角化，其对角特征值全为零，矩阵只能为零，矛盾。因此两者均不可对角化。相同一次秩不足以描述线性迭代的几何压缩。

answer

秩均$2$；$T$二次归零，$U$三次归零，不相似，均不可对角化。

scene_spec.objects[0]

在$\mathbb R^4$中比较$T(x)=(x_3,x_4,0,0)$与$U(x)=(x_2,x_3,0,0)$。求迭代像维数与最小归零次数，证明它们虽秩相同却不相似，并判断可否对角化。

scene_spec.objects[1]

秩均$2$；$T$二次归零，$U$三次归零，不相似，均不可对角化。

scene_spec.steps[0]

第一步:两者像维数均为$2$。

scene_spec.steps[1]

第二步:$T^2=0$且$T\ne0$，像维数序列为$4,2,0$；$U^2(x)=(x_3,0,0,0)\ne0$、$U^3=0$，像维数为$4,2,1,0$。

scene_spec.steps[2]

第三步:相似会保持所有幂的秩或最小归零次数，故两者不相似。

scene_spec.steps[3]

第四步:若一个非零幂零实或复矩阵可对角化，其对角特征值全为零，矩阵只能为零，矛盾。

scene_spec.steps[4]

第五步:因此两者均不可对角化。

scene_spec.steps[5]

第六步:相同一次秩不足以描述线性迭代的几何压缩。

## draft-c26-05

problem

设 $A=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$(旋转 $90^\circ$),$B=\begin{pmatrix}2&0\\0&1\end{pmatrix}$(沿 $x$ 方向伸缩)。计算 $AB$ 与 $BA$，并用单位正方形的像说明两者对应的几何作用不同。

solution

$AB=\begin{pmatrix}0&-1\\1&0\end{pmatrix}\begin{pmatrix}2&0\\0&1\end{pmatrix}=\begin{pmatrix}0&-1\\2&0\end{pmatrix}$;$BA=\begin{pmatrix}2&0\\0&1\end{pmatrix}\begin{pmatrix}0&-1\\1&0\end{pmatrix}=\begin{pmatrix}0&-2\\1&0\end{pmatrix}$。$AB\neq BA$。几何:单位正方形在 $AB$(先伸缩、后旋转)下:伸缩把顶点映为 $(0,0),(2,0),(2,1),(0,1)$(水平长条),再旋转 $90^\circ$ 得 $(0,0),(0,2),(-1,2),(-1,0)$(竖直长条)。在 $BA$(先旋转、后伸缩)下:旋转得 $(0,0),(0,1),(-1,1),(-1,0)$,再沿 $x$ 方向伸缩得 $(0,0),(0,1),(-2,1),(-2,0)$(水平长条)。两像不同($AB$ 的像为竖直 $1\times2$ 长条,$BA$ 的像为水平 $2\times1$ 长条),故矩阵乘法顺序不可交换,几何上对应「先伸缩后旋转」与「先旋转后伸缩」的不同。

answer

$AB=\begin{pmatrix}0&-1\\2&0\end{pmatrix}$,$BA=\begin{pmatrix}0&-2\\1&0\end{pmatrix}$,两者不同;$AB$ 的像为竖直长条,$BA$ 的像为水平长条,几何上为「先伸缩后旋转」与「先旋转后伸缩」的差异。

scene_spec.objects[0]

设 $A=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$(旋转 $90^\circ$),$B=\begin{pmatrix}2&0\\0&1\end{pmatrix}$(沿 $x$ 方向伸缩)。计算 $AB$ 与 $BA$，并用单位正方形的像说明两者对应的几何作用不同。

scene_spec.objects[1]

$AB=\begin{pmatrix}0&-1\\2&0\end{pmatrix}$,$BA=\begin{pmatrix}0&-2\\1&0\end{pmatrix}$,两者不同;$AB$ 的像为竖直长条,$BA$ 的像为水平长条,几何上为「先伸缩后旋转」与「先旋转后伸缩」的差异。

scene_spec.steps[0]

第一步:$AB=\begin{pmatrix}0&-1\\1&0\end{pmatrix}\begin{pmatrix}2&0\\0&1\end{pmatrix}=\begin{pmatrix}0&-1\\2&0\end{pmatrix}$;$BA=\begin{pmatrix}2&0\\0&1\end{pmatrix}\begin{pmatrix}0&-1\\1&0\end{pmatrix}=\begin{pmatrix}0&-2\\1&0\end{pmatrix}$。

scene_spec.steps[1]

第二步:$AB\neq BA$。

scene_spec.steps[2]

第三步:几何:单位正方形在 $AB$(先伸缩、后旋转)下:伸缩把顶点映为 $(0,0),(2,0),(2,1),(0,1)$(水平长条),再旋转 $90^\circ$ 得 $(0,0),(0,2),(-1,2),(-1,0)$(竖直长条)。

scene_spec.steps[3]

第四步:在 $BA$(先旋转、后伸缩)下:旋转得 $(0,0),(0,1),(-1,1),(-1,0)$,再沿 $x$ 方向伸缩得 $(0,0),(0,1),(-2,1),(-2,0)$(水平长条)。

scene_spec.steps[4]

第五步:两像不同($AB$ 的像为竖直 $1\times2$ 长条,$BA$ 的像为水平 $2\times1$ 长条),故矩阵乘法顺序不可交换,几何上对应「先伸缩后旋转」与「先旋转后伸缩」的不同。
