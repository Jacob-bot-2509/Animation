# Batch 4 independent review material


## draft-c07-05

P: 求双纽线 $r^2=\cos 2\theta$ 所围成的总面积，并说明角域的确定方式。

S: 需 $r^2\ge0$,即 $\cos2\theta\ge0$,故角域为 $[-\frac{\pi}{4},\frac{\pi}{4}]\cup[\frac{3\pi}{4},\frac{5\pi}{4}]$(按模 $2\pi$ 理解,等价于 $[0,\frac{\pi}{4}]\cup[\frac{3\pi}{4},\frac{5\pi}{4}]\cup[\frac{7\pi}{4},2\pi]$),两段对应两个对称的叶。右叶面积 $A_1=\frac12\int_{-\frac{\pi}{4}}^{\frac{\pi}{4}}\cos2\theta\,d\theta=\frac12\left.\frac{\sin2\theta}{2}\right|_{-\frac{\pi}{4}}^{\frac{\pi}{4}}=\frac12\times1=\frac12$。总面积 $=2A_1=1$。

A: 总面积为 $1$(每叶 $\frac12$,共两叶)。

Objects: 极坐标图:双纽线 $r^2=\cos2\theta$ 两叶 | 角域卡:$\cos2\theta\ge0$ 的区间划分 $[-\frac\pi4,\frac\pi4]\cup[\frac{3\pi}4,\frac{5\pi}4]$ | 板书:$A_1=\frac12\int_{-\frac\pi4}^{\frac\pi4}\cos2\theta\,d\theta$ 与原函数 $\frac{\sin2\theta}2$ | 高亮框:关键点——$[\frac{\sin2\theta}2]_{-\frac\pi4}^{\frac\pi4}=1$ 的上下限代入 | 结论卡:每叶 $\frac12$,总面积 $1$

Steps:
第一步:确定角域(高亮):需 $r^2=\cos2\theta\ge0$,即 $2\theta\in[-\frac\pi2,\frac\pi2]$ 模 $2\pi$;故 $\theta\in[-\frac\pi4,\frac\pi4]\cup[\frac{3\pi}4,\frac{5\pi}4]$,两段对应两个对称的叶。
第二步:右叶面积公式:$A_1=\frac12\int_{-\frac\pi4}^{\frac\pi4}r^2\,d\theta=\frac12\int_{-\frac\pi4}^{\frac\pi4}\cos2\theta\,d\theta$。
第三步:求原函数(逐项):$\int\cos2\theta\,d\theta=\frac{\sin2\theta}2$;代入上下限(高亮):$[\frac{\sin2\theta}2]_{-\frac\pi4}^{\frac\pi4}=\frac{\sin\frac\pi2}2-\frac{\sin(-\frac\pi2)}2=\frac12+\frac12=1$。
第四步:每叶面积:$A_1=\frac12\cdot1=\frac12$。
第五步:两叶全等,总面积 $A=2A_1=2\times\frac12=1$(高亮结论)。


## draft-c08-01

P: 设$a>0$，摆线一拱参数方程$x=a(t-\sin t),y=a(1-\cos t)$，$0\le t\le2\pi$。求这一拱与$x$轴围成的面积，并说明参数积分方向与封闭边界的依据。

S: $x^{\prime}=a(1-\cos t)\ge0$，在$(0,2\pi)$严格为正；$y\ge0$，两端点为$(0,0)$与$(2\pi a,0)$。因此这一拱是从左到右的单值图形，由轴上线段闭合，普通面积为$\int y\,dx=\int_0^{2\pi}a^2(1-\cos t)^2\,dt$。展开得$\int_0^{2\pi}(1-2\cos t+\cos^2t)dt=2\pi+0+\pi=3\pi$，故面积$3\pi a^2$。这里沿上拱从左到右的$\int y\,dx$给正面积；如果使用有向闭曲线公式，应同时说明此上拱方向对应顺时针闭边界，不能混用逆时针符号。轴上线段的$y\,dx$贡献为零。

A: 面积$3\pi a^2$。

Objects: 参数图:摆线一拱($0\le t\le2\pi$)与 $x$ 轴围成区域 | 方向依据卡:$x'=a(1-\cos t)\ge0$、两端点 $(0,0)$ 与 $(2\pi a,0)$ | 板书:$A=\int_0^{2\pi}a(1-\cos t)\cdot a(1-\cos t)\,dt$ 的代入 | 展开板:$(1-\cos t)^2=1-2\cos t+\cos^2t$ 与逐项积分 | 结论卡:$A=3\pi a^2$

Steps:
第一步:方向与闭边界依据(高亮):$x'=a(1-\cos t)\ge0$ 且在 $(0,2\pi)$ 严格为正;$y\ge0$,两端点为 $(0,0)$ 与 $(2\pi a,0)$;故这一拱是从左到右的单值图形,由轴上线段闭合。
第二步:面积公式(逐项代入):$A=\int y\,dx=\int_0^{2\pi}y(t)x'(t)\,dt=\int_0^{2\pi}a(1-\cos t)\cdot a(1-\cos t)\,dt=a^2\int_0^{2\pi}(1-\cos t)^2\,dt$。
第三步:展开(逐项):$(1-\cos t)^2=1-2\cos t+\cos^2t$;半角公式 $\cos^2t=\frac{1+\cos2t}2$(高亮)。
第四步:逐项积分:$\int_0^{2\pi}1\,dt=2\pi$;$\int_0^{2\pi}\cos t\,dt=0$;$\int_0^{2\pi}\cos^2t\,dt=\pi$(半角);合计 $2\pi+0+\pi=3\pi$。
第五步:结论:$A=a^2\cdot3\pi=3\pi a^2$;沿上拱从左到右的 $\int y\,dx$ 给正面积(高亮)。


## draft-c08-02

P: 求星形线 $\begin{cases}x=a\cos^3 t\\ y=a\sin^3 t\end{cases}$($a>0$)围成的面积。

S: 星形线在第一象限的部分对应 $t$ 从 $\frac{\pi}{2}$ 到 $0$。第一象限面积 $A_1=\int_{\frac{\pi}{2}}^{0}y\,x'\,dt$ 的绝对值,$x'=-3a\cos^2t\sin t$:$\int_{\frac{\pi}{2}}^{0}(a\sin^3t)(-3a\cos^2t\sin t)\,dt=3a^2\int_0^{\frac{\pi}{2}}\sin^4t\cos^2t\,dt=3a^2\cdot\frac{(3!!\cdot1!!)\pi}{6!!\cdot2}=3a^2\cdot\frac{3\pi}{96}=\frac{3\pi a^2}{32}$。总面积为 $4A_1=\frac{3\pi a^2}{8}$。

A: 面积为 $\frac{3\pi a^2}{8}$。

Objects: 参数图:星形线 $x=a\cos^3t,y=a\sin^3t$ 与第一象限部分 | 求导板书:$x'=-3a\cos^2t\sin t$ 的逐项求导 | 积分板书:$3a^2\int_0^{\frac\pi2}\sin^4t\cos^2t\,dt$ 的符号整理 | 高亮框:关键点——Wallis 公式 $\frac{(3!!\cdot1!!)\pi}{6!!\cdot2}=\frac{3\pi}{96}$ | 结论卡:第一象限 $\frac{3\pi a^2}{32}$,总面积 $\frac{3\pi a^2}8$

Steps:
第一步:第一象限部分对应 $t$ 从 $\frac\pi2$ 到 $0$;求导(逐项):$x'=\frac{d}{dt}(a\cos^3t)=3a\cos^2t\cdot(-\sin t)=-3a\cos^2t\sin t$(高亮)。
第二步:面积积分(逐项代入):$A_1=|\int_{\frac\pi2}^0y\,x'\,dt|=|\int_{\frac\pi2}^0(a\sin^3t)(-3a\cos^2t\sin t)\,dt|$;翻转上下限消去负号:$=3a^2\int_0^{\frac\pi2}\sin^4t\cos^2t\,dt$。
第三步:Wallis 公式(关键点,高亮):$\int_0^{\frac\pi2}\sin^4t\cos^2t\,dt=\frac{(3!!\cdot1!!)\pi}{6!!\cdot2}=\frac{3\pi}{96}$。
第四步:第一象限面积:$A_1=3a^2\cdot\frac{3\pi}{96}=\frac{3\pi a^2}{32}$。
第五步:星形线四象限对称,总面积 $A=4A_1=\frac{3\pi a^2}8$(高亮结论)。


## draft-c08-03

P: 求笛卡尔叶形线 $x=\frac{3t}{1+t^3}$，$y=\frac{3t^2}{1+t^3}$($t\ge0$)的环所围成的面积。

S: 叶形线的环对应 $t$ 从 $0$ 到 $+\infty$(曲线从原点出发,经第一象限后回到原点)。用面积公式 $A=\frac12\int_0^{+\infty}(x\,y'-y\,x')\,dt$。计算:$x'=\frac{3(1-2t^3)}{(1+t^3)^2}$,$y'=\frac{3t(2-t^3)}{(1+t^3)^2}$,故 $x\,y'-y\,x'=\frac{9t^2(2-t^3)-9t^2(1-2t^3)}{(1+t^3)^3}=\frac{9t^2(1+t^3)}{(1+t^3)^3}=\frac{9t^2}{(1+t^3)^2}$。$A=\frac12\int_0^{+\infty}\frac{9t^2}{(1+t^3)^2}\,dt=\frac12\left.\left(-\frac{3}{1+t^3}\right)\right|_0^{+\infty}=\frac12\times3=\frac32$。 对$t>0$有$y/x=t$，故不同有限参数对应不同非原点，曲线在此参数域无自交；$t\downarrow0$与$t\to+\infty$均趋于原点，恰描绘一个环一次。上述无穷上限须理解为有限积分再取极限，原函数给出极限$3/2$。

A: 环的面积为 $\frac32$。

Objects: 参数图:笛卡尔叶形线的环($t$ 从 $0$ 到 $+\infty$) | 求导板书:$x'=\frac{3(1-2t^3)}{(1+t^3)^2}$、$y'=\frac{3t(2-t^3)}{(1+t^3)^2}$ 的商法则 | 化简板书:$xy'-yx'=\frac{9t^2}{(1+t^3)^2}$ 的分子相减与约分 | 高亮框:关键点——换元 $u=1+t^3$,$3\int_1^\infty\frac{du}{u^2}=3$ | 结论卡:$A=\frac32$

Steps:
第一步:环对应 $t$ 从 $0$ 到 $+\infty$;面积公式 $A=\frac12\int_0^{\infty}(xy'-yx')\,dt$。
第二步:逐项求导(商法则,高亮):$x'=\frac{3(1+t^3)-3t\cdot3t^2}{(1+t^3)^2}=\frac{3(1-2t^3)}{(1+t^3)^2}$;$y'=\frac{6t(1+t^3)-3t^2\cdot3t^2}{(1+t^3)^2}=\frac{3t(2-t^3)}{(1+t^3)^2}$。
第三步:叉积化简(逐项):$xy'-yx'=\frac{3t\cdot3t(2-t^3)-3t^2\cdot3(1-2t^3)}{(1+t^3)^3}=\frac{9t^2(2-t^3-1+2t^3)}{(1+t^3)^3}=\frac{9t^2}{(1+t^3)^2}$(高亮分子相减与约分)。
第四步:广义积分(逐项,关键点):$A=\frac12\int_0^\infty\frac{9t^2}{(1+t^3)^2}dt$;换元 $u=1+t^3$,$du=3t^2\,dt$:$\int_0^\infty\frac{9t^2}{(1+t^3)^2}dt=3\int_1^\infty\frac{du}{u^2}=3[-\frac1u]_1^\infty=3(0-(-1))=3$。
第五步:结论:$A=\frac12\cdot3=\frac32$(高亮)。


## draft-c14-04

P: 设$f(x)=3+2\cos x-\sin(2x)$，$g(x)=f(x-\pi/3)$。求$g$的实Fourier系数，推导一般平移的系数变换，并证明每一频率的$a_n^2+b_n^2$不变。

S: 若平移量为$\alpha$，展开加法公式得$a_n^{\prime}=a_n\cos(n\alpha)-b_n\sin(n\alpha)$、$b_n^{\prime}=a_n\sin(n\alpha)+b_n\cos(n\alpha)$，常数项不变。这是二维正交变换，平方相加消去交叉项，得$(a_n^{\prime})^2+(b_n^{\prime})^2=a_n^2+b_n^2$。本题$a_0=6,a_1=2,b_2=-1$，其余为零，代入$\alpha=\pi/3$得到$g(x)=3+\cos x+\sqrt3\sin x+(\sqrt3/2)\cos(2x)+(1/2)\sin(2x)$，有限展开无需收敛交换。

A: $g=3+\cos x+\sqrt3\sin x+\frac{\sqrt3}{2}\cos2x+\frac12\sin2x$；各频率系数平方和不变。

Objects: 函数卡:$f(x)=3+2\cos x-\sin(2x)$ 的系数读出 | 板书一:平移系数变换 $a_n'=a_n\cos(n\alpha)-b_n\sin(n\alpha)$、$b_n'=a_n\sin(n\alpha)+b_n\cos(n\alpha)$ 的加法公式推导 | 高亮框:关键点——平方和展开中交叉项 $\pm2a_nb_n\sin\cos$ 抵消 | 板书二:$\alpha=\frac\pi3$ 的逐项代入 | 结论卡:$g=3+\cos x+\sqrt3\sin x+\frac{\sqrt3}2\cos2x+\frac12\sin2x$

Steps:
第一步:读出 $f$ 的系数:$a_0=6$(常数项 $3$)、$a_1=2$、$b_2=-1$,其余为零(高亮)。
第二步:一般平移公式(加法公式推导,高亮):$g(x)=f(x-\alpha)$;对频率 $n$ 的项 $a_n\cos(n(x-\alpha))+b_n\sin(n(x-\alpha))$ 展开:$a_n[\cos nx\cos(n\alpha)+\sin nx\sin(n\alpha)]+b_n[\sin nx\cos(n\alpha)-\cos nx\sin(n\alpha)]$;合并得 $a_n'=a_n\cos(n\alpha)-b_n\sin(n\alpha)$,$b_n'=a_n\sin(n\alpha)+b_n\cos(n\alpha)$;常数项不变。
第三步:平方和不变(逐步):$(a_n')^2+(b_n')^2=[a_n\cos(n\alpha)-b_n\sin(n\alpha)]^2+[a_n\sin(n\alpha)+b_n\cos(n\alpha)]^2=a_n^2(\cos^2+\sin^2)+b_n^2(\sin^2+\cos^2)+2a_nb_n(\sin\cos-\sin\cos)=a_n^2+b_n^2$(关键点:交叉项抵消,高亮)。
第四步:代入 $\alpha=\frac\pi3$(逐项):$a_1'=2\cos\frac\pi3=2\cdot\frac12=1$;$b_1'=2\sin\frac\pi3=2\cdot\frac{\sqrt3}2=\sqrt3$;$a_2'=-b_2\sin\frac{2\pi}3=-(-1)\cdot\frac{\sqrt3}2=\frac{\sqrt3}2$;$b_2'=b_2\cos\frac{2\pi}3=(-1)\cdot(-\frac12)=\frac12$;常数项仍为 $3$。
第五步:写出 $g(x)=3+\cos x+\sqrt3\sin x+\frac{\sqrt3}2\cos2x+\frac12\sin2x$;各频率 $a_n^2+b_n^2$ 不变(高亮)。


## draft-c17-04

P: 设两相交平面$f_1=x+y+z-1=0$、$f_2=x-y+2z=0$交于直线$l$。给出包含$l$的全部平面，并分类经过给定点$P$的成员；最后求经过$(1,1,1)$的成员。

S: 法向量$n_1=(1,1,1)$、$n_2=(1,-1,2)$线性无关。任何包含$l$的平面法向量属于$\operatorname{span}(n_1,n_2)$，在$l$上取一点比较常数项，得全部平面$s f_1+t f_2=0$，$(s,t)\ne(0,0)$，比例$(s:t)$标识同一平面。该齐次表示包含$f_2=0$，不能用$f_1+\lambda f_2$遗漏它。经过$P$需$s f_1(P)+t f_2(P)=0$：若$P\in l$，所有成员都经过$P$；否则一条非零齐次线性约束唯一确定比例。对$P=(1,1,1)$，$f_1(P)=f_2(P)=2$，故$(s:t)=(1:-1)$，平面为$2y-z=1$。

A: 全部$s f_1+t f_2=0$，$(s:t)\in\mathbb{RP}^1$；$P\in l$时全部，否则唯一；指定点对应$2y-z=1$。

Objects: 空间图:两平面 $f_1=0$、$f_2=0$ 及其交线 $l$ | 法向量卡:$n_1=(1,1,1)$、$n_2=(1,-1,2)$ 线性无关 | 平面束板书:$sf_1+tf_2=0$,$(s,t)\ne(0,0)$,比例标识同一平面 | 高亮框:关键点——齐次表示包含 $f_2=0$,而 $f_1+\lambda f_2$ 会遗漏它 | 结论卡:过 $(1,1,1)$ 的成员为 $f_1-f_2=2y-z-1=0$

Steps:
第一步:法向量 $n_1=(1,1,1)$、$n_2=(1,-1,2)$ 不成比例,线性无关;任何包含交线 $l$ 的平面,其法向量必属于 $\operatorname{span}(n_1,n_2)$(高亮)。
第二步:全部平面:$sf_1+tf_2=0$,$(s,t)\ne(0,0)$;比例 $(s:t)$ 标识同一平面;该齐次表示包含 $f_2=0$(取 $s=0,t=1$),而 $f_1+\lambda f_2$ 形式会遗漏它(关键点)。
第三步:过点条件(逐项代入):$P=(1,1,1)$:$f_1(P)=1+1+1-1=2$;$f_2(P)=1-1+2\cdot1=2$(高亮)。
第四步:解比例:$sf_1(P)+tf_2(P)=2s+2t=0$,即 $s=-t$;取 $(s:t)=(1:-1)$。
第五步:所求平面:$f_1-f_2=0$,逐项相减:$(x+y+z-1)-(x-y+2z)=2y-z-1$,即 $2y-z-1=0$(高亮结论)。


## draft-c26-01

P: 令$n=(1,2,-1)$、$d=(1,1,0)$，定义$P(x)=x-(n\cdot x)d/3$。求矩阵、核与像，证明其为沿$d$投影到$n\cdot x=0$的斜投影，判断是否为Euclidean正交投影。

S: $n\cdot d=3$，所以$Pd=0$且$n\cdot Px=0$；对$n\cdot x=0$的向量有$Px=x$。因此像为$n^{\perp}$，核为$\operatorname{span}(d)$，$P^2=P$，秩$2$。矩阵为$\begin{pmatrix}2/3&-2/3&1/3\\-1/3&1/3&1/3\\0&0&1\end{pmatrix}$。核方向$d$不平行法向量$n$，矩阵也不对称，故不是Euclidean正交投影；分解$x=Px+(n\cdot x)d/3$唯一，说明投影方向。

A: $\ker P=\operatorname{span}(1,1,0)$，$\operatorname{im}P=n^{\perp}$，$P^2=P$；斜投影而非Euclidean正交投影。

Objects: 空间图:平面 $n\cdot x=0$、方向 $d$ 与斜投影示意 | 验证卡:$n\cdot d=3$、$Pd=0$、$n\cdot Px=0$ 的逐项计算 | 矩阵推导板:$Pe_1,Pe_2,Pe_3$ 三列逐分量计算 | 高亮框:关键点——核方向 $d$ 不平行 $n$ 且矩阵不对称 → 斜投影 | 结论卡:$P=\begin{pmatrix}\frac23&-\frac23&\frac13\\-\frac13&\frac13&\frac13\\0&0&1\end{pmatrix}$,分解 $x=Px+\frac{(n\cdot x)d}3$

Steps:
第一步:验证投影性质(逐项,高亮):$n\cdot d=(1,2,-1)\cdot(1,1,0)=1+2+0=3$;$Pd=d-\frac{(n\cdot d)d}3=d-d=0$;$n\cdot Px=n\cdot x-\frac{(n\cdot d)(n\cdot x)}3=n\cdot x-n\cdot x=0$。
第二步:核与像:当 $n\cdot x=0$ 时 $Px=x$;当 $x\parallel d$ 时 $Px=0$;故 $\ker P=\operatorname{span}(d)$,$\operatorname{im}P=n^\perp$;$P^2=P$,秩 $2$。
第三步:逐列求矩阵(逐分量,高亮):$Pe_1=e_1-\frac{(n\cdot e_1)d}3=(1,0,0)-\frac{(1,1,0)}3=(\frac23,-\frac13,0)$;$Pe_2=(0,1,0)-\frac{(2,2,0)}3=(-\frac23,\frac13,0)$;$Pe_3=(0,0,1)-\frac{(-1,-1,0)}3=(\frac13,\frac13,1)$;得 $P=\begin{pmatrix}\frac23&-\frac23&\frac13\\-\frac13&\frac13&\frac13\\0&0&1\end{pmatrix}$。
第四步:判定(关键点):核方向 $d=(1,1,0)$ 不平行法向量 $n=(1,2,-1)$,且矩阵不对称;故是沿 $d$ 到 $n^\perp$ 的斜投影,不是 Euclidean 正交投影(高亮)。
第五步:分解唯一性:$x=Px+\frac{(n\cdot x)d}3$,第一项在 $n^\perp$、第二项在核中,说明投影方向(高亮)。


## draft-c26-05

P: 设 $A=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$(旋转 $90^\circ$),$B=\begin{pmatrix}2&0\\0&1\end{pmatrix}$(沿 $x$ 方向伸缩)。计算 $AB$ 与 $BA$，并用单位正方形的像说明两者对应的几何作用不同。

S: $AB=\begin{pmatrix}0&-1\\1&0\end{pmatrix}\begin{pmatrix}2&0\\0&1\end{pmatrix}=\begin{pmatrix}0&-1\\2&0\end{pmatrix}$;$BA=\begin{pmatrix}2&0\\0&1\end{pmatrix}\begin{pmatrix}0&-1\\1&0\end{pmatrix}=\begin{pmatrix}0&-2\\1&0\end{pmatrix}$。$AB\neq BA$。几何:单位正方形在 $AB$(先伸缩、后旋转)下:伸缩把顶点映为 $(0,0),(2,0),(2,1),(0,1)$(水平长条),再旋转 $90^\circ$ 得 $(0,0),(0,2),(-1,2),(-1,0)$(竖直长条)。在 $BA$(先旋转、后伸缩)下:旋转得 $(0,0),(0,1),(-1,1),(-1,0)$,再沿 $x$ 方向伸缩得 $(0,0),(0,1),(-2,1),(-2,0)$(水平长条)。两像不同($AB$ 的像为竖直 $1\times2$ 长条,$BA$ 的像为水平 $2\times1$ 长条),故矩阵乘法顺序不可交换,几何上对应「先伸缩后旋转」与「先旋转后伸缩」的不同。

A: $AB=\begin{pmatrix}0&-1\\2&0\end{pmatrix}$,$BA=\begin{pmatrix}0&-2\\1&0\end{pmatrix}$,两者不同;$AB$ 的像为竖直长条,$BA$ 的像为水平长条,几何上为「先伸缩后旋转」与「先旋转后伸缩」的差异。

Objects: 矩阵卡:$A=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$(旋转 $90^\circ$)、$B=\begin{pmatrix}2&0\\0&1\end{pmatrix}$(伸缩) | 行×列计算卡:$AB$ 与 $BA$ 各四项分量乘积 | 单位正方形像对照图:$AB$ 的像与 $BA$ 的像 | 高亮框:关键点——$(1,2)$ 位置 $-1\ne-2$、$(2,1)$ 位置 $2\ne1$ | 结论卡:$AB\ne BA$,几何作用不同

Steps:
第一步:计算 $AB$(逐行×列,高亮):第1行×第1列:$0\cdot2+(-1)\cdot0=0$;第1行×第2列:$0\cdot0+(-1)\cdot1=-1$;第2行×第1列:$1\cdot2+0\cdot0=2$;第2行×第2列:$1\cdot0+0\cdot1=0$;得 $AB=\begin{pmatrix}0&-1\\2&0\end{pmatrix}$。
第二步:计算 $BA$(逐行×列,高亮):第1行×第1列:$2\cdot0+0\cdot1=0$;第1行×第2列:$2\cdot(-1)+0\cdot0=-2$;第2行×第1列:$0\cdot0+1\cdot1=1$;第2行×第2列:$0\cdot(-1)+1\cdot0=0$;得 $BA=\begin{pmatrix}0&-2\\1&0\end{pmatrix}$。
第三步:$AB\ne BA$:比较 $(1,2)$ 位置 $-1\ne-2$、$(2,1)$ 位置 $2\ne1$(高亮)。
第四步:$AB$ 的几何作用(先伸缩后旋转):单位正方形顶点像为 $(0,0),(0,2),(-1,2),(-1,0)$,横向放置的矩形(逐顶点标注)。
第五步:$BA$ 的几何作用(先旋转后伸缩):像为 $(0,0),(0,1),(-2,1),(-2,0)$,竖向放置的矩形;两种作用次序的像不同(高亮结论)。


## draft-c29-02

P: 已知 $2+i$ 是实系数多项式 $f(x)=x^3-7x^2+17x-15$ 的一个根，求 $f$ 的全部根。

S: 实系数多项式的非实根成对出现:$2-i$ 也是根,故 $f$ 含因子 $(x-(2+i))(x-(2-i))=x^2-4x+5$。用韦达定理或综合除法:设第三根为 $r$,三根之和为 $7$,故 $r=7-(2+i)-(2-i)=3$。验证:$f=(x-3)(x^2-4x+5)$,展开核对:$x^3-4x^2+5x-3x^2+12x-15=x^3-7x^2+17x-15$ ✓。全部根:$3$,$2+i$,$2-i$。

A: 全部根:$3$,$2+i$,$2-i$。

Objects: 题面卡:$f(x)=x^3-7x^2+17x-15$ 与已知根 $2+i$ | 板书一:共轭根成对与因子展开 $((x-2)-i)((x-2)+i)$ | 高亮框:关键点——$i^2=-1$ 使常数项 $+1$ | 板书二:韦达定理 $r=7-(2+i)-(2-i)=3$ | 验证板:$(x-3)(x^2-4x+5)$ 展开逐项核对

Steps:
第一步:共轭成对(关键点,高亮):实系数多项式的非实根成对出现,故 $2-i$ 也是根。
第二步:因子展开(逐步):$(x-(2+i))(x-(2-i))=((x-2)-i)((x-2)+i)=(x-2)^2-i^2=x^2-4x+4+1=x^2-4x+5$(关键点:$i^2=-1$ 使常数项为 $+1$,高亮)。
第三步:韦达定理:三次根之和 $=7$;设第三根为 $r$,则 $r=7-(2+i)-(2-i)=7-4=3$。
第四步:验证展开(逐项):$(x-3)(x^2-4x+5)=x^3-4x^2+5x-3x^2+12x-15=x^3-7x^2+17x-15=f(x)$ ✓。
第五步:全部根:$3,2+i,2-i$(高亮结论)。


## draft-c29-03

P: 用 $f$ 与 $f'$ 的公因式求多项式 $f(x)=x^4-4x^3+6x^2-4x+1$ 的重根及其重数。

S: $f=x^4-4x^3+6x^2-4x+1=(x-1)^4$，$f^{\prime}=4(x-1)^3$。欧几里得步骤$f-(x-1)f^{\prime}/4=0$，故首一最大公因子为$(x-1)^3$。$f/f_{\mathrm{gcd}}=x-1$给唯一不同根$1$；$f^{(j)}(1)=0$（$j=0,1,2,3$）、$f^{(4)}(1)=24\ne0$，证明重数恰为$4$。

A: $f=(x-1)^4$,$x=1$ 是四重根。

Objects: 题面卡:$f=x^4-4x^3+6x^2-4x+1$ 与二项式系数对照 | 长除法板书:$f'$ 除 $f$ 得商 $\frac{x-1}4$、余 $0$ 的逐步演算 | 高亮框:关键点——$\gcd(f,f')=(x-1)^3$,商 $x-1$ 给唯一不同根 | 导数代入板:$f^{(j)}(1)=0$($j=0,1,2,3$)、$f^{(4)}(1)=24$ | 结论卡:$x=1$ 是四重根

Steps:
第一步:识别(逐项对照):系数 $1,-4,6,-4,1$ 恰为 $(x-1)^4$ 的二项式展开;故 $f=(x-1)^4$,$f'=4(x-1)^3$(高亮)。
第二步:欧几里得长除法(逐步):用 $f'=4x^3-12x^2+12x-4$ 除 $f$:商为 $\frac{x-1}4$;验算:$(x-1)\cdot\frac{f'}4=(x-1)(x^3-3x^2+3x-1)=x^4-4x^3+6x^2-4x+1=f$,余数为 $0$;故首一最大公因子 $\gcd(f,f')=(x-1)^3$(高亮演算)。
第三步:商:$f/\gcd=x-1$,唯一不同根为 $x=1$。
第四步:逐阶导数代入(高亮):$f'(1)=4\cdot0^3=0$;$f''(x)=12(x-1)^2$,故 $f''(1)=0$;$f'''(x)=24(x-1)$,故 $f'''(1)=0$;$f^{(4)}(x)=24$,故 $f^{(4)}(1)=24\ne0$。
第五步:结论:$x=1$ 的重数恰为 $4$(高亮)。
