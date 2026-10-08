## draft-c43-01

problem

设 $\mathbb R^2$ 的基为 $\eta_1=(1,1)$，$\eta_2=(1,-1)$。求对偶基 $f_1,f_2$，使 $f_i(\eta_j)=\delta_{ij}$。

solution

设 $f_1(x,y)=ax+by$。条件:$f_1(\eta_1)=a+b=1$,$f_1(\eta_2)=a-b=0$,解得 $a=b=\frac12$,故 $f_1(x,y)=\frac{x+y}{2}$。设 $f_2(x,y)=cx+dy$。条件:$f_2(\eta_1)=c+d=0$,$f_2(\eta_2)=c-d=1$,解得 $c=\frac12,d=-\frac12$,故 $f_2(x,y)=\frac{x-y}{2}$。验证:$f_1(\eta_1)=\frac{1+1}{2}=1$,$f_1(\eta_2)=0$;$f_2(\eta_1)=0$,$f_2(\eta_2)=1$ ✓。

answer

$f_1(x,y)=\frac{x+y}{2}$,$f_2(x,y)=\frac{x-y}{2}$。

scene_spec.objects[0]

设 $\mathbb R^2$ 的基为 $\eta_1=(1,1)$，$\eta_2=(1,-1)$。求对偶基 $f_1,f_2$，使 $f_i(\eta_j)=\delta_{ij}$。

scene_spec.objects[1]

$f_1(x,y)=\frac{x+y}{2}$,$f_2(x,y)=\frac{x-y}{2}$。

scene_spec.steps[0]

第一步:设 $f_1(x,y)=ax+by$。

scene_spec.steps[1]

第二步:条件:$f_1(\eta_1)=a+b=1$,$f_1(\eta_2)=a-b=0$,解得 $a=b=\frac12$,故 $f_1(x,y)=\frac{x+y}{2}$。

scene_spec.steps[2]

第三步:设 $f_2(x,y)=cx+dy$。

scene_spec.steps[3]

第四步:条件:$f_2(\eta_1)=c+d=0$,$f_2(\eta_2)=c-d=1$,解得 $c=\frac12,d=-\frac12$,故 $f_2(x,y)=\frac{x-y}{2}$。

scene_spec.steps[4]

第五步:验证:$f_1(\eta_1)=\frac{1+1}{2}=1$,$f_1(\eta_2)=0$;$f_2(\eta_1)=0$,$f_2(\eta_2)=1$ ✓。

## draft-c43-02

problem

求实线性泛函$f:\mathbb R^3\to\mathbb R$，满足$f(1,0,2)=2$、$f(0,2,1)=-1$、$f(1,2,3)=a$。分类存在性并给全部解，说明为何不能按三个给定值就认为唯一。

solution

第三个输入是前两个之和，所以线性性要求$a=1$，否则无解。若$a=1$，设$f(x,y,z)=\alpha x+\beta y+\gamma z$，取$\gamma=t$，前两式给$\alpha=2-2t$、$\beta=(-1-t)/2$。因此全部解$f_t=(2-2t)x-(1+t)y/2+tz$，$t\in\mathbb R$，直接代入三条件成立。两个独立输入只张成二维空间，没有组成三维基，故留下一个自由参数。

answer

$a=1$才有解；全部$f_t=(2-2t)x-(1+t)y/2+tz$；不唯一。

scene_spec.objects[0]

求实线性泛函$f:\mathbb R^3\to\mathbb R$，满足$f(1,0,2)=2$、$f(0,2,1)=-1$、$f(1,2,3)=a$。分类存在性并给全部解，说明为何不能按三个给定值就认为唯一。

scene_spec.objects[1]

$a=1$才有解；全部$f_t=(2-2t)x-(1+t)y/2+tz$；不唯一。

scene_spec.steps[0]

第一步:第三个输入是前两个之和，所以线性性要求$a=1$，否则无解。

scene_spec.steps[1]

第二步:若$a=1$，设$f(x,y,z)=\alpha x+\beta y+\gamma z$，取$\gamma=t$，前两式给$\alpha=2-2t$、$\beta=(-1-t)/2$。

scene_spec.steps[2]

第三步:因此全部解$f_t=(2-2t)x-(1+t)y/2+tz$，$t\in\mathbb R$，直接代入三条件成立。

scene_spec.steps[3]

第四步:两个独立输入只张成二维空间，没有组成三维基，故留下一个自由参数。

## draft-c43-03

problem

在$V=\mathbb R[x]_{\le2}$中取基$1,x,x^2$。求三个多项式$g_0,g_1,g_2$，使$f_i(p)=\int_{-1}^1g_i(x)p(x)\,dx$为此基的对偶泛函，并证明九个配对值。

solution

矩阵$G_{ij}=\int_{-1}^1x^{i+j}dx$（$i,j=0,1,2$）为$\begin{pmatrix}2&0&2/3\\0&2/3&0\\2/3&0&2/5\end{pmatrix}$。若$g_i$的系数为矩阵$C$第$i$行，则配对条件为$CG=I$。独立反解或积分核验得$C=\begin{pmatrix}9/8&0&-15/8\\0&3/2&0\\-15/8&0&45/8\end{pmatrix}$，故$g_0=(9-15x^2)/8,g_1=3x/2,g_2=(-15+45x^2)/8$。利用奇次矩积分为零、$\int1=2,\int x^2=2/3,\int x^4=2/5$，相乘给九个配对$\int g_i x^j=\delta_{ij}$。真正的对偶元素是$f_i$，多项式$g_i$是相对于该积分配对的表示。

answer

$g_0=(9-15x^2)/8,g_1=3x/2,g_2=(-15+45x^2)/8$；$f_i(p)=\int_{-1}^1g_i p$组成对偶基。

scene_spec.objects[0]

在$V=\mathbb R[x]_{\le2}$中取基$1,x,x^2$。求三个多项式$g_0,g_1,g_2$，使$f_i(p)=\int_{-1}^1g_i(x)p(x)\,dx$为此基的对偶泛函，并证明九个配对值。

scene_spec.objects[1]

$g_0=(9-15x^2)/8,g_1=3x/2,g_2=(-15+45x^2)/8$；$f_i(p)=\int_{-1}^1g_i p$组成对偶基。

scene_spec.steps[0]

第一步:矩阵$G_{ij}=\int_{-1}^1x^{i+j}dx$（$i,j=0,1,2$）为$\begin{pmatrix}2&0&2/3\\0&2/3&0\\2/3&0&2/5\end{pmatrix}$。

scene_spec.steps[1]

第二步:若$g_i$的系数为矩阵$C$第$i$行，则配对条件为$CG=I$。

scene_spec.steps[2]

第三步:独立反解或积分核验得$C=\begin{pmatrix}9/8&0&-15/8\\0&3/2&0\\-15/8&0&45/8\end{pmatrix}$，故$g_0=(9-15x^2)/8,g_1=3x/2,g_2=(-15+45x^2)/8$。

scene_spec.steps[3]

第四步:利用奇次矩积分为零、$\int1=2,\int x^2=2/3,\int x^4=2/5$，相乘给九个配对$\int g_i x^j=\delta_{ij}$。

scene_spec.steps[4]

第五步:真正的对偶元素是$f_i$，多项式$g_i$是相对于该积分配对的表示。

## draft-c43-04

problem

证明对偶配对 $\langle v,f\rangle=f(v)$ 在基变换下不变:设向量 $v$ 与泛函 $f$ 在旧基下的坐标分别为 $x$ 与 $y$，在新基下的坐标分别为 $\tilde x$ 与 $\tilde y$，则 $y^{\mathsf T}x=\tilde y^{\mathsf T}\tilde x$。

solution

设新旧基的过渡矩阵为 $P$(新基向量为旧基向量的 $P$ 线性组合),则向量坐标变换为 $x=P\tilde x$(新坐标经 $P$ 得旧坐标)。对偶基的过渡矩阵为 $(P^{-1})^{\mathsf T}$,故泛函坐标变换为 $y=(P^{-1})^{\mathsf T}\tilde y$。于是 $y^{\mathsf T}x=((P^{-1})^{\mathsf T}\tilde y)^{\mathsf T}(P\tilde x)=\tilde y^{\mathsf T}P^{-1}P\tilde x=\tilde y^{\mathsf T}\tilde x$。故配对值与基的选择无关。

answer

证明见解法(坐标变换 $x=P\tilde x$、$y=(P^{-1})^{\mathsf T}\tilde y$ 代入相消)。

scene_spec.objects[0]

证明对偶配对 $\langle v,f\rangle=f(v)$ 在基变换下不变:设向量 $v$ 与泛函 $f$ 在旧基下的坐标分别为 $x$ 与 $y$，在新基下的坐标分别为 $\tilde x$ 与 $\tilde y$，则 $y^{\mathsf T}x=\tilde y^{\mathsf T}\tilde x$。

scene_spec.objects[1]

证明见解法(坐标变换 $x=P\tilde x$、$y=(P^{-1})^{\mathsf T}\tilde y$ 代入相消)。

scene_spec.steps[0]

第一步:设新旧基的过渡矩阵为 $P$(新基向量为旧基向量的 $P$ 线性组合),则向量坐标变换为 $x=P\tilde x$(新坐标经 $P$ 得旧坐标)。

scene_spec.steps[1]

第二步:对偶基的过渡矩阵为 $(P^{-1})^{\mathsf T}$,故泛函坐标变换为 $y=(P^{-1})^{\mathsf T}\tilde y$。

scene_spec.steps[2]

第三步:于是 $y^{\mathsf T}x=((P^{-1})^{\mathsf T}\tilde y)^{\mathsf T}(P\tilde x)=\tilde y^{\mathsf T}P^{-1}P\tilde x=\tilde y^{\mathsf T}\tilde x$。

scene_spec.steps[3]

第四步:故配对值与基的选择无关。

## draft-c43-05

problem

设 $V$ 是有限维线性空间。证明 $\dim V^*=\dim V$，并构造自然同构 $\Phi:V\to V^{**}$($\Phi(v)(f)=f(v)$)。

solution

取 $V$ 的基 $e_1,\dots,e_n$ 与其对偶基 $e^1,\dots,e^n$($e^i(e_j)=\delta_{ij}$)。任何 $f\in V^*$ 由它在基上的取值唯一确定,且 $f=\sum_i f(e_i)e^i$($e^1,\dots,e^n$ 张成 $V^*$);又 $e^1,\dots,e^n$ 线性无关(若 $\sum c_ie^i=0$,作用于 $e_j$ 得 $c_j=0$)。故 $e^1,\dots,e^n$ 是 $V^*$ 的基,$\dim V^*=n=\dim V$。自然同构:定义 $\Phi(v)(f)=f(v)$。先验证 $\Phi(v)\in V^{**}$:对任意 $f,g\in V^*$ 与 $c$,$\Phi(v)(f+g)=(f+g)(v)=f(v)+g(v)=\Phi(v)(f)+\Phi(v)(g)$,$\Phi(v)(cf)=(cf)(v)=cf(v)=c\Phi(v)(f)$,故 $\Phi(v)$ 是 $V^*$ 上的线性泛函。再验证 $\Phi$ 线性:$\Phi(v_1+v_2)(f)=f(v_1+v_2)=f(v_1)+f(v_2)=\Phi(v_1)(f)+\Phi(v_2)(f)$;$\Phi(cv)(f)=f(cv)=cf(v)=c\Phi(v)(f)$。单射:若 $\Phi(v)=0$,则对一切 $f$,$f(v)=0$。若 $v\neq0$,把它延拓为基 $v=e_1,e_2,\dots,e_n$,取 $f=e^1$,则 $f(v)=1\neq0$,矛盾,故 $v=0$。于是 $\Phi$ 单射,而 $\dim V^{**}=\dim V^*=\dim V$,故 $\Phi$ 为同构。

answer

证明见解法(对偶基为基、维数相等;$\Phi$ 对 $f$ 与对 $v$ 均线性、单射,维数相同故同构)。

scene_spec.objects[0]

设 $V$ 是有限维线性空间。证明 $\dim V^*=\dim V$，并构造自然同构 $\Phi:V\to V^{**}$($\Phi(v)(f)=f(v)$)。

scene_spec.objects[1]

证明见解法(对偶基为基、维数相等;$\Phi$ 对 $f$ 与对 $v$ 均线性、单射,维数相同故同构)。

scene_spec.steps[0]

第一步:取 $V$ 的基 $e_1,\dots,e_n$ 与其对偶基 $e^1,\dots,e^n$($e^i(e_j)=\delta_{ij}$)。

scene_spec.steps[1]

第二步:任何 $f\in V^*$ 由它在基上的取值唯一确定,且 $f=\sum_i f(e_i)e^i$($e^1,\dots,e^n$ 张成 $V^*$);又 $e^1,\dots,e^n$ 线性无关(若 $\sum c_ie^i=0$,作用于 $e_j$ 得 $c_j=0$)。

scene_spec.steps[2]

第三步:故 $e^1,\dots,e^n$ 是 $V^*$ 的基,$\dim V^*=n=\dim V$。

scene_spec.steps[3]

第四步:自然同构:定义 $\Phi(v)(f)=f(v)$。

scene_spec.steps[4]

第五步:先验证 $\Phi(v)\in V^{**}$:对任意 $f,g\in V^*$ 与 $c$,$\Phi(v)(f+g)=(f+g)(v)=f(v)+g(v)=\Phi(v)(f)+\Phi(v)(g)$,$\Phi(v)(cf)=(cf)(v)=cf(v)=c\Phi(v)(f)$,故 $\Phi(v)$ 是 $V^*$ 上的线性泛函。

scene_spec.steps[5]

第六步:再验证 $\Phi$ 线性:$\Phi(v_1+v_2)(f)=f(v_1+v_2)=f(v_1)+f(v_2)=\Phi(v_1)(f)+\Phi(v_2)(f)$;$\Phi(cv)(f)=f(cv)=cf(v)=c\Phi(v)(f)$。

scene_spec.steps[6]

第七步:单射:若 $\Phi(v)=0$,则对一切 $f$,$f(v)=0$。

scene_spec.steps[7]

第八步:若 $v\neq0$,把它延拓为基 $v=e_1,e_2,\dots,e_n$,取 $f=e^1$,则 $f(v)=1\neq0$,矛盾,故 $v=0$。

scene_spec.steps[8]

第九步:于是 $\Phi$ 单射,而 $\dim V^{**}=\dim V^*=\dim V$,故 $\Phi$ 为同构。

## draft-c44-01

problem

在$\mathbb R^4$坐标$(p_1,p_2,q_1,q_2)$中，$J=\begin{pmatrix}0&I_2\\-I_2&0\end{pmatrix}$。分类块剪切$S_B=\begin{pmatrix}I_2&B\\0&I_2\end{pmatrix}$何时保持$\omega(u,v)=u^{\mathsf T}Jv$，并检验$B=\begin{pmatrix}1&2\\2&-1\end{pmatrix}$。

solution

矩阵乘法给$S_B^{\mathsf T}JS_B=\begin{pmatrix}0&I_2\\-I_2&B^{\mathsf T}-B\end{pmatrix}$，所以保持形式当且仅当$B^{\mathsf T}=B$。指定$B$对称，故保持。所有$S_B$的行列式均为$1$，但不对称$B$不保持形式；在四维不能以行列式$1$替代辛条件。

answer

充要条件$B$对称；指定矩阵满足，保持$\omega$。

scene_spec.objects[0]

在$\mathbb R^4$坐标$(p_1,p_2,q_1,q_2)$中，$J=\begin{pmatrix}0&I_2\\-I_2&0\end{pmatrix}$。分类块剪切$S_B=\begin{pmatrix}I_2&B\\0&I_2\end{pmatrix}$何时保持$\omega(u,v)=u^{\mathsf T}Jv$，并检验$B=\begin{pmatrix}1&2\\2&-1\end{pmatrix}$。

scene_spec.objects[1]

充要条件$B$对称；指定矩阵满足，保持$\omega$。

scene_spec.steps[0]

第一步:矩阵乘法给$S_B^{\mathsf T}JS_B=\begin{pmatrix}0&I_2\\-I_2&B^{\mathsf T}-B\end{pmatrix}$，所以保持形式当且仅当$B^{\mathsf T}=B$。

scene_spec.steps[1]

第二步:指定$B$对称，故保持。

scene_spec.steps[2]

第三步:所有$S_B$的行列式均为$1$，但不对称$B$不保持形式；在四维不能以行列式$1$替代辛条件。

## draft-c44-02

problem

在同一标准四维辛形式$J$下，证明保体积不必保持辛形式：检验$A=\operatorname{diag}(2,1,1,1/2)$，给具体反例向量，并解释二维与四维的差异。

solution

$\det A=2\cdot1\cdot1\cdot(1/2)=1$，所以保体积。但$\omega(e_1,e_3)=1$而$\omega(Ae_1,Ae_3)=2$，故不保持辛形式；$\omega(e_2,e_4)$也从$1$变为$1/2$。二维标准交替形式满足$A^{\mathsf T}J_2A=(\det A)J_2$，所以二维行列式$1$足够；四维需要每对配对坐标及交叉项同时满足$A^{\mathsf T}JA=J$，总体积条件不能代替这些约束。

answer

行列式$1$但非辛，反例$(e_1,e_3)$的形式值从$1$到$2$。

scene_spec.objects[0]

在同一标准四维辛形式$J$下，证明保体积不必保持辛形式：检验$A=\operatorname{diag}(2,1,1,1/2)$，给具体反例向量，并解释二维与四维的差异。

scene_spec.objects[1]

行列式$1$但非辛，反例$(e_1,e_3)$的形式值从$1$到$2$。

scene_spec.steps[0]

第一步:$\det A=2\cdot1\cdot1\cdot(1/2)=1$，所以保体积。

scene_spec.steps[1]

第二步:但$\omega(e_1,e_3)=1$而$\omega(Ae_1,Ae_3)=2$，故不保持辛形式；$\omega(e_2,e_4)$也从$1$变为$1/2$。

scene_spec.steps[2]

第三步:二维标准交替形式满足$A^{\mathsf T}J_2A=(\det A)J_2$，所以二维行列式$1$足够；四维需要每对配对坐标及交叉项同时满足$A^{\mathsf T}JA=J$，总体积条件不能代替这些约束。

## draft-c44-03

problem

在标准四维辛形式$J$下分类可逆对角矩阵$A=\operatorname{diag}(a,b,c,d)$何时为辛矩阵，并检验$(a,b,c,d)=(2,2,1/2,1/2)$。

solution

$A^{\mathsf T}JA$的两个配对系数为$ac$与$bd$，所以充要条件$ac=bd=1$，即$a,b\ne0$且$c=1/a,d=1/b$。指定数据满足两个等式，故保持辛形式。条件自动给行列式$1$，但仅行列式$1$不足以推出两配对分别为$1$。

answer

充要条件$ac=bd=1$；指定矩阵为辛矩阵。

scene_spec.objects[0]

在标准四维辛形式$J$下分类可逆对角矩阵$A=\operatorname{diag}(a,b,c,d)$何时为辛矩阵，并检验$(a,b,c,d)=(2,2,1/2,1/2)$。

scene_spec.objects[1]

充要条件$ac=bd=1$；指定矩阵为辛矩阵。

scene_spec.steps[0]

第一步:$A^{\mathsf T}JA$的两个配对系数为$ac$与$bd$，所以充要条件$ac=bd=1$，即$a,b\ne0$且$c=1/a,d=1/b$。

scene_spec.steps[1]

第二步:指定数据满足两个等式，故保持辛形式。

scene_spec.steps[2]

第三步:条件自动给行列式$1$，但仅行列式$1$不足以推出两配对分别为$1$。

## draft-c44-04

problem

在 $\mathbb R^3$ 上定义 $\omega(u,v)=(u\times v)\cdot e_1$($e_1=(1,0,0)$)。验证 $\omega$ 是交替的，并说明它不是辛形式(退化)。

solution

$\omega(u,v)=u_2v_3-u_3v_2$，显然对两变量分别线性，且$\omega(u,u)=0$，所以交替。若它对所有$v$为零，分别取$v=e_3,e_2$得$u_2=u_3=0$；反过来这些条件足够。故核恰为$\operatorname{span}(e_1)$，秩$2$，形式退化，不是辛形式。

answer

$\omega$ 交替(叉积反交换)但退化($e_1$ 在核中),不是辛形式。

scene_spec.objects[0]

在 $\mathbb R^3$ 上定义 $\omega(u,v)=(u\times v)\cdot e_1$($e_1=(1,0,0)$)。验证 $\omega$ 是交替的，并说明它不是辛形式(退化)。

scene_spec.objects[1]

$\omega$ 交替(叉积反交换)但退化($e_1$ 在核中),不是辛形式。

scene_spec.steps[0]

第一步:$\omega(u,v)=u_2v_3-u_3v_2$，显然对两变量分别线性，且$\omega(u,u)=0$，所以交替。

scene_spec.steps[1]

第二步:若它对所有$v$为零，分别取$v=e_3,e_2$得$u_2=u_3=0$；反过来这些条件足够。

scene_spec.steps[2]

第三步:故核恰为$\operatorname{span}(e_1)$，秩$2$，形式退化，不是辛形式。

## draft-c44-05

problem

证明:在数域(特征不为 $2$)上的奇数维线性空间中,不存在非退化的交替双线性形式。

solution

设 $V$ 为 $n$ 维空间,$\omega$ 为交替双线性形式,在取定一组基后由斜对称矩阵 $A$ 表示($A^{\mathsf T}=-A$)。$\omega$ 非退化当且仅当 $A$ 可逆。但若 $n$ 为奇数,$\det A=\det(A^{\mathsf T})=\det(-A)=(-1)^n\det A=-\det A$,故 $\det A=0$,$A$ 奇异,即 $\omega$ 必退化。故奇数维空间不存在非退化的交替双线性形式(辛形式只存在于偶数维空间)。

answer

证明见解法(斜对称矩阵:$\det A=(-1)^n\det A$,奇数维时行列式为零)。

scene_spec.objects[0]

证明:在数域(特征不为 $2$)上的奇数维线性空间中,不存在非退化的交替双线性形式。

scene_spec.objects[1]

证明见解法(斜对称矩阵:$\det A=(-1)^n\det A$,奇数维时行列式为零)。

scene_spec.steps[0]

第一步:设 $V$ 为 $n$ 维空间,$\omega$ 为交替双线性形式,在取定一组基后由斜对称矩阵 $A$ 表示($A^{\mathsf T}=-A$)。

scene_spec.steps[1]

第二步:$\omega$ 非退化当且仅当 $A$ 可逆。

scene_spec.steps[2]

第三步:但若 $n$ 为奇数,$\det A=\det(A^{\mathsf T})=\det(-A)=(-1)^n\det A=-\det A$,故 $\det A=0$,$A$ 奇异,即 $\omega$ 必退化。

scene_spec.steps[3]

第四步:故奇数维空间不存在非退化的交替双线性形式(辛形式只存在于偶数维空间)。

## draft-c45-01

problem

证明:若 $A,B$ 相互独立且 $P(A)>0,P(B)>0$，则 $A,B$ 不互斥；若 $A,B$ 互斥且概率均为正，则 $A,B$ 不独立。

solution

第一部分:独立给出 $P(A\cap B)=P(A)P(B)>0$(两正数之积),故 $A\cap B\neq\varnothing$,不互斥。第二部分:互斥给出 $P(A\cap B)=0$,而 $P(A)P(B)>0$,故 $P(A\cap B)\neq P(A)P(B)$,不独立(等价地 $P(A|B)=0\neq P(A)$)。结论:独立与互斥是两个不同的概念——独立是概率乘积关系,互斥是集合不相交关系;除退化情形(零概率事件)外两者互斥。

answer

证明见解法(独立⟹交概率为正⟹不互斥;互斥⟹交概率为零⟹不独立)。

scene_spec.objects[0]

证明:若 $A,B$ 相互独立且 $P(A)>0,P(B)>0$，则 $A,B$ 不互斥；若 $A,B$ 互斥且概率均为正，则 $A,B$ 不独立。

scene_spec.objects[1]

证明见解法(独立⟹交概率为正⟹不互斥;互斥⟹交概率为零⟹不独立)。

scene_spec.steps[0]

第一步:第一部分:独立给出 $P(A\cap B)=P(A)P(B)>0$(两正数之积),故 $A\cap B\neq\varnothing$,不互斥。

scene_spec.steps[1]

第二步:第二部分:互斥给出 $P(A\cap B)=0$,而 $P(A)P(B)>0$,故 $P(A\cap B)\neq P(A)P(B)$,不独立(等价地 $P(A|B)=0\neq P(A)$)。

scene_spec.steps[2]

第三步:结论:独立与互斥是两个不同的概念——独立是概率乘积关系,互斥是集合不相交关系;除退化情形(零概率事件)外两者互斥。

## draft-c45-02

problem

用乘法公式(链式法则)求 $P(A\cap B\cap C)$，其中 $P(A)=\frac12$，$P(B|A)=\frac35$，$P(C|A\cap B)=\frac45$。

solution

链式法则:$P(A\cap B\cap C)=P(A)\cdot P(B|A)\cdot P(C|A\cap B)=\frac12\times\frac35\times\frac45=\frac{6}{25}$。

answer

$P(A\cap B\cap C)=\frac{6}{25}$。

scene_spec.objects[0]

用乘法公式(链式法则)求 $P(A\cap B\cap C)$，其中 $P(A)=\frac12$，$P(B|A)=\frac35$，$P(C|A\cap B)=\frac45$。

scene_spec.objects[1]

$P(A\cap B\cap C)=\frac{6}{25}$。

scene_spec.steps[0]

第一步:链式法则:$P(A\cap B\cap C)=P(A)\cdot P(B|A)\cdot P(C|A\cap B)=\frac12\times\frac35\times\frac45=\frac{6}{25}$。

## draft-c45-03

problem

独立地抛两枚公平硬币。记 $A=${第一枚正面},$B=${第二枚正面},$C=${两枚同面}。证明 $A,B,C$ 两两独立但整体不独立。

solution

$P(A)=P(B)=P(C)=\frac12$。$P(A\cap B)=P(\text{both heads})=\frac14=P(A)P(B)$ ✓。$P(A\cap C)=P(A\cap\text{same face})=P(\text{both heads})=\frac14=P(A)P(C)$ ✓。$P(B\cap C)=\frac14=P(B)P(C)$ ✓。故两两独立。但 $P(A\cap B\cap C)=P(\text{both heads})=\frac14\neq\frac18=P(A)P(B)P(C)$,故整体不独立。

answer

两两独立($P(A\cap B)=P(A\cap C)=P(B\cap C)=\frac14$),但 $P(A\cap B\cap C)=\frac14\neq\frac18$,整体不独立。

scene_spec.objects[0]

独立地抛两枚公平硬币。记 $A=${第一枚正面},$B=${第二枚正面},$C=${两枚同面}。证明 $A,B,C$ 两两独立但整体不独立。

scene_spec.objects[1]

两两独立($P(A\cap B)=P(A\cap C)=P(B\cap C)=\frac14$),但 $P(A\cap B\cap C)=\frac14\neq\frac18$,整体不独立。

scene_spec.steps[0]

第一步:$P(A)=P(B)=P(C)=\frac12$。

scene_spec.steps[1]

第二步:$P(A\cap B)=P(\text{both heads})=\frac14=P(A)P(B)$ ✓。

scene_spec.steps[2]

第三步:$P(A\cap C)=P(A\cap\text{same face})=P(\text{both heads})=\frac14=P(A)P(C)$ ✓。

scene_spec.steps[3]

第四步:$P(B\cap C)=\frac14=P(B)P(C)$ ✓。

scene_spec.steps[4]

第五步:故两两独立。

scene_spec.steps[5]

第六步:但 $P(A\cap B\cap C)=P(\text{both heads})=\frac14\neq\frac18=P(A)P(B)P(C)$,故整体不独立。

## draft-c45-04

problem

说明是否存在满足 $P(A|B)=\frac{9}{10}$，$P(A|\bar B)=\frac45$，且 $P(A)=\frac{1}{10}$ 的事件 $A,B$($0<P(B)<1$)；并说明一般情形下 $P(A)$ 必须满足什么约束。

solution

记$u=P(A\mid B),v=P(A\mid B^c),q=P(B)\in(0,1)$。全概率公式给$P(A)=qu+(1-q)v$。若$u\ne v$，概率严格位于$\min(u,v)$与$\max(u,v)$之间；若$u=v$，等于共同值。反过来，任何严格介于两者之间的$p$都可取$q=(p-v)/(u-v)\in(0,1)$，用四原子概率$qu,q(1-u),(1-q)v,(1-q)(1-v)$实现。指定$u=9/10,v=4/5$时必有$4/5<P(A)<9/10$，与$P(A)=1/10$矛盾，因此数据不可能。

answer

指定数据不可能；一般$u\ne v$时$\min(u,v)<P(A)<\max(u,v)$，且区间内任意值可实现。

scene_spec.objects[0]

说明是否存在满足 $P(A|B)=\frac{9}{10}$，$P(A|\bar B)=\frac45$，且 $P(A)=\frac{1}{10}$ 的事件 $A,B$($0<P(B)<1$)；并说明一般情形下 $P(A)$ 必须满足什么约束。

scene_spec.objects[1]

指定数据不可能；一般$u\ne v$时$\min(u,v)<P(A)<\max(u,v)$，且区间内任意值可实现。

scene_spec.steps[0]

第一步:记$u=P(A\mid B),v=P(A\mid B^c),q=P(B)\in(0,1)$。

scene_spec.steps[1]

第二步:全概率公式给$P(A)=qu+(1-q)v$。

scene_spec.steps[2]

第三步:若$u\ne v$，概率严格位于$\min(u,v)$与$\max(u,v)$之间；若$u=v$，等于共同值。

scene_spec.steps[3]

第四步:反过来，任何严格介于两者之间的$p$都可取$q=(p-v)/(u-v)\in(0,1)$，用四原子概率$qu,q(1-u),(1-q)v,(1-q)(1-v)$实现。

scene_spec.steps[4]

第五步:指定$u=9/10,v=4/5$时必有$4/5<P(A)<9/10$，与$P(A)=1/10$矛盾，因此数据不可能。

## draft-c45-05

problem

证明:给定事件 $B$($P(B)>0$)，条件概率 $P(\cdot|B)$ 是样本空间上的概率测度，并推导全概率公式。

solution

验证概率公理:非负性:对任意 $A$,$P(A|B)=\frac{P(A\cap B)}{P(B)}\ge0$。归一性:$P(\Omega|B)=\frac{P(\Omega\cap B)}{P(B)}=\frac{P(B)}{P(B)}=1$。可列可加性:设 $A_1,A_2,\dots$ 两两互斥,则 $P\left(\bigcup_i A_i\,\middle|\,B\right)=\frac{P(\bigcup_i(A_i\cap B))}{P(B)}=\frac{\sum_i P(A_i\cap B)}{P(B)}=\sum_i P(A_i|B)$(用到 $P$ 的可列可加性)。故 $P(\cdot|B)$ 是概率测度。全概率公式:设 $B_1,\dots,B_n$ 构成完备事件组(两两互斥且并为 $\Omega$,$P(B_i)>0$),则 $P(A)=\sum_i P(A\cap B_i)=\sum_i P(A|B_i)P(B_i)$。

answer

证明见解法(非负/归一/可列可加三公理验证;全概率公式由完备事件组分解得)。

scene_spec.objects[0]

证明:给定事件 $B$($P(B)>0$)，条件概率 $P(\cdot|B)$ 是样本空间上的概率测度，并推导全概率公式。

scene_spec.objects[1]

证明见解法(非负/归一/可列可加三公理验证;全概率公式由完备事件组分解得)。

scene_spec.steps[0]

第一步:验证概率公理:非负性:对任意 $A$,$P(A|B)=\frac{P(A\cap B)}{P(B)}\ge0$。

scene_spec.steps[1]

第二步:归一性:$P(\Omega|B)=\frac{P(\Omega\cap B)}{P(B)}=\frac{P(B)}{P(B)}=1$。

scene_spec.steps[2]

第三步:可列可加性:设 $A_1,A_2,\dots$ 两两互斥,则 $P\left(\bigcup_i A_i\,\middle|\,B\right)=\frac{P(\bigcup_i(A_i\cap B))}{P(B)}=\frac{\sum_i P(A_i\cap B)}{P(B)}=\sum_i P(A_i|B)$(用到 $P$ 的可列可加性)。

scene_spec.steps[3]

第四步:故 $P(\cdot|B)$ 是概率测度。

scene_spec.steps[4]

第五步:全概率公式:设 $B_1,\dots,B_n$ 构成完备事件组(两两互斥且并为 $\Omega$,$P(B_i)>0$),则 $P(A)=\sum_i P(A\cap B_i)=\sum_i P(A|B_i)P(B_i)$。
