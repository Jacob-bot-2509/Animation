# Batch 8 independent review material


## draft-c42-03

P: 给定$u,v\in\mathbb R^3$，分类将$u$映到$v$的单个过原点平面反射。证明存在性与唯一性条件，并求将$(1,2,2)$映到$(2,1,2)$的反射矩阵。

S: 反射保持范数，故必要$\|u\|=\|v\|$。若$u\ne v$且等范数，令$n=(u-v)/\|u-v\|$；由$\|u-v\|^2=2(\|u\|^2-u\cdot v)$得$2(n\cdot u)n=u-v$，所以$H=I-2nn^{\mathsf T}$满足$Hu=v$。反过来任何满足条件的反射都有$u-v=2(n\cdot u)n$，法线必须平行$u-v$，故矩阵唯一。若$u=v\ne0$，任意单位$n\perp u$都给反射，故不唯一；若均为零，任意单位法线都可以。范数不等时无解。指定数据法线$(-1,1,0)/\sqrt2$，得到$H=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}$。

A: 等范数且不同则唯一；相同则有多种；范数不等无解。指定矩阵交换$x,y$。

Objects: 题面卡:将 $u$ 映到 $v$ 的过原点平面反射的分类 | 板书一:$\|u-v\|^2=2(\|u\|^2-u\cdot v)$ 与 $2(n\cdot u)n=u-v$ 的推导 | 高亮框:关键点——法线必平行 $u-v$ 给唯一性 | 板书二:$u-v=(-1,1,0)$、$\|u-v\|=\sqrt2$ 的代入 | 结论卡:$H=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}$(交换 $x,y$)

Steps:
第一步:必要性:反射保持范数,故 $\|u\|=\|v\|$ 是必要条件。
第二步:若 $u\ne v$ 且等范数,令 $n=\frac{u-v}{\|u-v\|}$;关键恒等式(逐步,高亮):$\|u-v\|^2=\|u\|^2+\|v\|^2-2u\cdot v=2(\|u\|^2-u\cdot v)$;而 $(u-v)\cdot u=\|u\|^2-u\cdot v=\frac{\|u-v\|^2}2$;故 $2(n\cdot u)n=2\cdot\frac{(u-v)\cdot u}{\|u-v\|^2}(u-v)=u-v$。
第三步:故 $H=I-2nn^{\mathsf T}$ 满足 $Hu=u-2(n\cdot u)n=u-(u-v)=v$。
第四步:唯一性(关键点):任何满足条件的反射都有 $u-v=2(n\cdot u)n$,法线必平行 $u-v$,故矩阵唯一;$u=v\ne0$ 时有无穷多种;$u\ne v$ 但范数不等则无解(高亮)。
第五步:具体计算(逐步,高亮):$u=(1,2,2)$,$v=(2,1,2)$:$u-v=(-1,1,0)$,$\|u-v\|=\sqrt{1+1}=\sqrt2$;$n=\frac{(-1,1,0)}{\sqrt2}$;$nn^{\mathsf T}=\frac12\begin{pmatrix}1&-1&0\\-1&1&0\\0&0&0\end{pmatrix}$;$H=I-2nn^{\mathsf T}=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}$,即交换 $x,y$。


## draft-c43-01

P: 设 $\mathbb R^2$ 的基为 $\eta_1=(1,1)$，$\eta_2=(1,-1)$。求对偶基 $f_1,f_2$，使 $f_i(\eta_j)=\delta_{ij}$。

S: 设 $f_1(x,y)=ax+by$。条件:$f_1(\eta_1)=a+b=1$,$f_1(\eta_2)=a-b=0$,解得 $a=b=\frac12$,故 $f_1(x,y)=\frac{x+y}{2}$。设 $f_2(x,y)=cx+dy$。条件:$f_2(\eta_1)=c+d=0$,$f_2(\eta_2)=c-d=1$,解得 $c=\frac12,d=-\frac12$,故 $f_2(x,y)=\frac{x-y}{2}$。验证:$f_1(\eta_1)=\frac{1+1}{2}=1$,$f_1(\eta_2)=0$;$f_2(\eta_1)=0$,$f_2(\eta_2)=1$ ✓。

A: $f_1(x,y)=\frac{x+y}{2}$,$f_2(x,y)=\frac{x-y}{2}$。

Objects: 题面卡:基 $\eta_1=(1,1)$、$\eta_2=(1,-1)$ 的对偶基 | 板书一:$f_1(\eta_1)=a+b=1$、$f_1(\eta_2)=a-b=0$ 的方程组 | 高亮框:关键点——两式相加得 $2a=1$ | 板书二:$f_2$ 的方程组与消元 | 验证板:四个配对值的代入

Steps:
第一步:设 $f_1(x,y)=ax+by$;条件代入:$f_1(\eta_1)=f_1(1,1)=a+b=1$;$f_1(\eta_2)=f_1(1,-1)=a-b=0$。
第二步:消元(逐步,高亮):两式相加:$2a=1$,即 $a=\frac12$;回代:$b=1-a=\frac12$;故 $f_1(x,y)=\frac{x+y}2$。
第三步:设 $f_2(x,y)=cx+dy$;条件代入:$f_2(\eta_1)=c+d=0$;$f_2(\eta_2)=c-d=1$。
第四步:消元(逐步,高亮):相加:$2c=1$,即 $c=\frac12$;回代:$d=-c=-\frac12$;故 $f_2(x,y)=\frac{x-y}2$。
第五步:验证(逐项):$f_1(\eta_1)=\frac{1+1}2=1$,$f_1(\eta_2)=\frac{1-1}2=0$;$f_2(\eta_1)=\frac{1-1}2=0$,$f_2(\eta_2)=\frac{1-(-1)}2=1$(高亮)。


## draft-c43-02

P: 求实线性泛函$f:\mathbb R^3\to\mathbb R$，满足$f(1,0,2)=2$、$f(0,2,1)=-1$、$f(1,2,3)=a$。分类存在性并给全部解，说明为何不能按三个给定值就认为唯一。

S: 第三个输入是前两个之和，所以线性性要求$a=1$，否则无解。若$a=1$，设$f(x,y,z)=\alpha x+\beta y+\gamma z$，取$\gamma=t$，前两式给$\alpha=2-2t$、$\beta=(-1-t)/2$。因此全部解$f_t=(2-2t)x-(1+t)y/2+tz$，$t\in\mathbb R$，直接代入三条件成立。两个独立输入只张成二维空间，没有组成三维基，故留下一个自由参数。

A: $a=1$才有解；全部$f_t=(2-2t)x-(1+t)y/2+tz$；不唯一。

Objects: 题面卡:三个节点值的线性泛函分类 | 板书一:$(1,0,2)+(0,2,1)=(1,2,3)$ 的逐分量相加 | 高亮框:关键点——只有两个独立条件,解空间一维 | 板书二:$\alpha+2\gamma=2$、$2\beta+\gamma=-1$ 的移项求解 | 结论卡:$a=1$ 才有解;全部 $f_t=(2-2t)x-\frac{1+t}2y+tz$

Steps:
第一步:逐分量相加(高亮):$(1,0,2)+(0,2,1)=(1,2,3)$;线性性要求 $f(1,2,3)=f(1,0,2)+f(0,2,1)=2+(-1)=1$;故 $a\ne1$ 无解,$a=1$ 才可能有解。
第二步:设 $f(x,y,z)=\alpha x+\beta y+\gamma z$;代入条件(逐步):$f(1,0,2)=\alpha+2\gamma=2$;$f(0,2,1)=2\beta+\gamma=-1$。
第三步:只有两个独立条件,解空间一维;取 $\gamma=t$ 为自由参数(关键点,高亮);移项求解:$\alpha=2-2t$;$2\beta=-1-t$,即 $\beta=\frac{-1-t}2$。
第四步:全部解:$f_t(x,y,z)=(2-2t)x-\frac{1+t}2y+tz$,$t\in\mathbb R$。
第五步:验证(逐项代入):$f_t(1,0,2)=(2-2t)+2t=2$;$f_t(0,2,1)=2\cdot\frac{-1-t}2+t=-1$;不唯一的原因:两个独立输入只张成二维,不构成三维基(高亮)。


## draft-c43-03

P: 在$V=\mathbb R[x]_{\le2}$中取基$1,x,x^2$。求三个多项式$g_0,g_1,g_2$，使$f_i(p)=\int_{-1}^1g_i(x)p(x)\,dx$为此基的对偶泛函，并证明九个配对值。

S: 矩阵$G_{ij}=\int_{-1}^1x^{i+j}dx$（$i,j=0,1,2$）为$\begin{pmatrix}2&0&2/3\\0&2/3&0\\2/3&0&2/5\end{pmatrix}$。若$g_i$的系数为矩阵$C$第$i$行，则配对条件为$CG=I$。独立反解或积分核验得$C=\begin{pmatrix}9/8&0&-15/8\\0&3/2&0\\-15/8&0&45/8\end{pmatrix}$，故$g_0=(9-15x^2)/8,g_1=3x/2,g_2=(-15+45x^2)/8$。利用奇次矩积分为零、$\int1=2,\int x^2=2/3,\int x^4=2/5$，相乘给九个配对$\int g_i x^j=\delta_{ij}$。真正的对偶元素是$f_i$，多项式$g_i$是相对于该积分配对的表示。

A: $g_0=(9-15x^2)/8,g_1=3x/2,g_2=(-15+45x^2)/8$；$f_i(p)=\int_{-1}^1g_i p$组成对偶基。

Objects: 题面卡:对偶多项式 $g_0,g_1,g_2$ 与九个配对值 | 板书一:$G_{ij}=\int_{-1}^1x^{i+j}dx$ 的逐项计算 | 高亮框:关键点——$CG=I$ 的逐行×列验算 | 板书二:$g_0,g_1,g_2$ 的系数与表达式 | 验证板:九个配对值的逐项积分

Steps:
第一步:矩阵 $G_{ij}=\int_{-1}^1x^{i+j}dx$;逐项计算(高亮):$G_{00}=2$;$G_{01}=G_{10}=0$;$G_{02}=G_{20}=\frac23$;$G_{11}=\frac23$;$G_{12}=G_{21}=0$;$G_{22}=\frac25$;得 $G=\begin{pmatrix}2&0&\frac23\\0&\frac23&0\\\frac23&0&\frac25\end{pmatrix}$。
第二步:配对条件:$f_i(x^j)=\int_{-1}^1g_i(x)x^jdx=\delta_{ij}$;若 $g_i$ 的系数为矩阵 $C$ 的第 $i$ 行,则 $CG=I$。
第三步:解 $C=G^{-1}$ 并逐行×列验算 $CG=I$(高亮):第1行×第1列:$\frac98\cdot2+(-\frac{15}8)\cdot\frac23=\frac94-\frac54=1$;第1行×第3列:$\frac98\cdot\frac23-\frac{15}8\cdot\frac25=\frac34-\frac34=0$;第2行×第2列:$\frac32\cdot\frac23=1$;第3行×第1列:$-\frac{15}8\cdot2+\frac{45}8\cdot\frac23=0$;第3行×第3列:$-\frac{15}8\cdot\frac23+\frac{45}8\cdot\frac25=1$。
第四步:故 $g_0=\frac{9-15x^2}8$,$g_1=\frac{3x}2$,$g_2=\frac{-15+45x^2}8$。
第五步:九个配对值(逐项,高亮):$\int g_0\cdot1\,dx=\frac{9\cdot2-15\cdot\frac23}8=\frac{18-10}8=1$;$\int g_0x\,dx=0$;$\int g_0x^2dx=\frac{9\cdot\frac23-15\cdot\frac25}8=\frac{6-6}8=0$;其余六项同理,恰为 $\delta_{ij}$。


## draft-c44-01

P: 在$\mathbb R^4$坐标$(p_1,p_2,q_1,q_2)$中，$J=\begin{pmatrix}0&I_2\\-I_2&0\end{pmatrix}$。分类块剪切$S_B=\begin{pmatrix}I_2&B\\0&I_2\end{pmatrix}$何时保持$\omega(u,v)=u^{\mathsf T}Jv$，并检验$B=\begin{pmatrix}1&2\\2&-1\end{pmatrix}$。

S: 矩阵乘法给$S_B^{\mathsf T}JS_B=\begin{pmatrix}0&I_2\\-I_2&B^{\mathsf T}-B\end{pmatrix}$，所以保持形式当且仅当$B^{\mathsf T}=B$。指定$B$对称，故保持。所有$S_B$的行列式均为$1$，但不对称$B$不保持形式；在四维不能以行列式$1$替代辛条件。

A: 充要条件$B$对称；指定矩阵满足，保持$\omega$。

Objects: 题面卡:块剪切 $S_B=\begin{pmatrix}I_2&B\\0&I_2\end{pmatrix}$ 何时保持 $\omega$ | 板书一:$JS_B$ 与 $S_B^{\mathsf T}(JS_B)$ 的分块乘法过程 | 高亮框:关键点——右下块 $B^{\mathsf T}-B$ 的得出 | 板书二:$B$ 的转置与对称性检验 | 结论卡:充要条件 $B$ 对称;行列式 $1$ 不能替代辛条件

Steps:
第一步:分块乘法(逐步,高亮):$S_B^{\mathsf T}JS_B=\begin{pmatrix}I_2&0\\B^{\mathsf T}&I_2\end{pmatrix}\begin{pmatrix}0&I_2\\-I_2&0\end{pmatrix}\begin{pmatrix}I_2&B\\0&I_2\end{pmatrix}$;先算 $JS_B=\begin{pmatrix}0&I_2\\-I_2&-B\end{pmatrix}$;再算 $S_B^{\mathsf T}(JS_B)$:左上块 $=I_2\cdot0+0\cdot(-I_2)=0$;右上块 $=I_2\cdot I_2+0\cdot(-B)=I_2$;左下块 $=B^{\mathsf T}\cdot0+I_2\cdot(-I_2)=-I_2$;右下块 $=B^{\mathsf T}\cdot I_2+I_2\cdot(-B)=B^{\mathsf T}-B$。
第二步:保持形式当且仅当 $S_B^{\mathsf T}JS_B=J$,即 $B^{\mathsf T}-B=0$,即 $B$ 对称(高亮)。
第三步:指定 $B$ 的对称性检验(逐步):$B=\begin{pmatrix}1&2\\2&-1\end{pmatrix}$,$B^{\mathsf T}=\begin{pmatrix}1&2\\2&-1\end{pmatrix}=B$;故该 $S_B$ 保持 $\omega$。
第四步:行列式:所有 $S_B$ 的 $\det S_B=1$,但不对称 $B$ 不保持形式。
第五步:结论(高亮):四维情形不能以行列式 $1$ 替代辛条件。


## draft-c44-02

P: 在同一标准四维辛形式$J$下，证明保体积不必保持辛形式：检验$A=\operatorname{diag}(2,1,1,1/2)$，给具体反例向量，并解释二维与四维的差异。

S: $\det A=2\cdot1\cdot1\cdot(1/2)=1$，所以保体积。但$\omega(e_1,e_3)=1$而$\omega(Ae_1,Ae_3)=2$，故不保持辛形式；$\omega(e_2,e_4)$也从$1$变为$1/2$。二维标准交替形式满足$A^{\mathsf T}J_2A=(\det A)J_2$，所以二维行列式$1$足够；四维需要每对配对坐标及交叉项同时满足$A^{\mathsf T}JA=J$，总体积条件不能代替这些约束。

A: 行列式$1$但非辛，反例$(e_1,e_3)$的形式值从$1$到$2$。

Objects: 题面卡:$A=\operatorname{diag}(2,1,1,\frac12)$ 保体积但不辛 | 板书一:$\det A=2\cdot1\cdot1\cdot\frac12=1$ | 高亮框:关键点——$Ae_1=2e_1$ 与双线性给 $\omega(Ae_1,Ae_3)=2$ | 板书二:$Ae_4=\frac12e_4$ 给 $\omega(e_2,Ae_4)=\frac12$ | 结论卡:二维行列式 $1$ 足够,四维不够

Steps:
第一步:行列式(逐项):$\det A=2\cdot1\cdot1\cdot\frac12=1$;故 $A$ 保体积。
第二步:形式值检验(逐步,高亮):$Ae_1=2e_1$;$\omega(Ae_1,Ae_3)=\omega(2e_1,e_3)=2\omega(e_1,e_3)=2\cdot1=2$(用双线性);而 $\omega(e_1,e_3)=1$;故 $A$ 不保持辛形式。
第三步:另一配对(逐步):$Ae_4=\frac12e_4$;$\omega(e_2,Ae_4)=\omega(e_2,\frac12e_4)=\frac12\omega(e_2,e_4)=\frac12$(从 $1$ 变到 $\frac12$,高亮)。
第四步:二维对照:标准二维交替形式满足 $A^{\mathsf T}J_2A=(\det A)J_2$,故二维行列式 $1$ 足够。
第五步:结论(高亮):四维需要每对配对坐标及交叉项同时满足 $A^{\mathsf T}JA=J$;保体积不必保持辛形式。


## draft-c44-03

P: 在标准四维辛形式$J$下分类可逆对角矩阵$A=\operatorname{diag}(a,b,c,d)$何时为辛矩阵，并检验$(a,b,c,d)=(2,2,1/2,1/2)$。

S: $A^{\mathsf T}JA$的两个配对系数为$ac$与$bd$，所以充要条件$ac=bd=1$，即$a,b\ne0$且$c=1/a,d=1/b$。指定数据满足两个等式，故保持辛形式。条件自动给行列式$1$，但仅行列式$1$不足以推出两配对分别为$1$。

A: 充要条件$ac=bd=1$；指定矩阵为辛矩阵。

Objects: 题面卡:对角矩阵 $A=\operatorname{diag}(a,b,c,d)$ 的辛分类 | 板书一:$(A^{\mathsf T}JA)_{13}=ac$、$(A^{\mathsf T}JA)_{24}=bd$ 的分量乘法 | 高亮框:关键点——充要条件 $ac=bd=1$ | 检验板:$2\cdot\frac12=1$ 与 $2\cdot\frac12=1$ | 结论卡:指定矩阵为辛矩阵;仅行列式 $1$ 不足

Steps:
第一步:计算 $A^{\mathsf T}JA$(逐分量,高亮):$(A^{\mathsf T}JA)_{13}=a\cdot1\cdot c=ac$;$(A^{\mathsf T}JA)_{31}=-ac$;$(A^{\mathsf T}JA)_{24}=b\cdot1\cdot d=bd$;$(A^{\mathsf T}JA)_{42}=-bd$;其余为零。
第二步:保持形式当且仅当 $ac=1$ 且 $bd=1$,即 $a,b\ne0$ 且 $c=\frac1a,d=\frac1b$(高亮)。
第三步:检验指定数据(逐项):$ac=2\cdot\frac12=1$;$bd=2\cdot\frac12=1$;故该 $A$ 为辛矩阵。
第四步:行列式:条件自动给 $\det A=ac\cdot bd=1$;但仅 $\det A=1$ 不足——例如配对系数分别为 $2$ 与 $\frac12$ 时行列式仍为 $1$ 却不是辛矩阵。
第五步:结论(高亮):辛条件要求两个配对各自为 $1$,不是只看行列式。


## draft-c44-04

P: 在 $\mathbb R^3$ 上定义 $\omega(u,v)=(u\times v)\cdot e_1$($e_1=(1,0,0)$)。验证 $\omega$ 是交替的，并说明它不是辛形式(退化)。

S: $\omega(u,v)=u_2v_3-u_3v_2$，显然对两变量分别线性，且$\omega(u,u)=0$，所以交替。若它对所有$v$为零，分别取$v=e_3,e_2$得$u_2=u_3=0$；反过来这些条件足够。故核恰为$\operatorname{span}(e_1)$，秩$2$，形式退化，不是辛形式。

A: $\omega$ 交替(叉积反交换)但退化($e_1$ 在核中),不是辛形式。

Objects: 题面卡:$\omega(u,v)=(u\times v)\cdot e_1$ 的交替性与退化 | 板书一:叉积三分量展开与点乘 $e_1$ 取第一分量 | 高亮框:关键点——$\omega(u,u)=u_2u_3-u_3u_2=0$ | 板书二:取 $v=e_3,e_2$ 解核的代入 | 结论卡:核 $\operatorname{span}(e_1)$,秩 $2$,退化

Steps:
第一步:叉积展开(逐步,高亮):$u\times v=(u_2v_3-u_3v_2,\,u_3v_1-u_1v_3,\,u_1v_2-u_2v_1)$;点乘 $e_1=(1,0,0)$ 只取第一分量:$\omega(u,v)=u_2v_3-u_3v_2$。
第二步:交替性:表达式对两变量分别线性(行列式形式);且 $\omega(u,u)=u_2u_3-u_3u_2=0$,故交替(高亮)。
第三步:核(逐步):若 $\omega(u,v)=0$ 对所有 $v$:取 $v=e_3$:$\omega(u,e_3)=u_2\cdot1-u_3\cdot0=u_2$,得 $u_2=0$;取 $v=e_2$:$\omega(u,e_2)=u_2\cdot0-u_3\cdot1=-u_3$,得 $u_3=0$。
第四步:反过来 $u_2=u_3=0$ 时对所有 $v$ 有 $\omega(u,v)=0$;故核 $=\operatorname{span}(e_1)$,秩为 $2$。
第五步:结论(高亮):形式退化,不是辛形式。


## draft-c45-04

P: 说明是否存在满足 $P(A|B)=\frac{9}{10}$，$P(A|\bar B)=\frac45$，且 $P(A)=\frac{1}{10}$ 的事件 $A,B$($0<P(B)<1$)；并说明一般情形下 $P(A)$ 必须满足什么约束。

S: 记$u=P(A\mid B),v=P(A\mid B^c),q=P(B)\in(0,1)$。全概率公式给$P(A)=qu+(1-q)v$。若$u\ne v$，概率严格位于$\min(u,v)$与$\max(u,v)$之间；若$u=v$，等于共同值。反过来，任何严格介于两者之间的$p$都可取$q=(p-v)/(u-v)\in(0,1)$，用四原子概率$qu,q(1-u),(1-q)v,(1-q)(1-v)$实现。指定$u=9/10,v=4/5$时必有$4/5<P(A)<9/10$，与$P(A)=1/10$矛盾，因此数据不可能。

A: 指定数据不可能；一般$u\ne v$时$\min(u,v)<P(A)<\max(u,v)$，且区间内任意值可实现。

Objects: 题面卡:条件概率存在性分类 | 板书一:全概率公式 $P(A)=qu+(1-q)v$ | 高亮框:关键点——$qu+(1-q)v$ 是 $u,v$ 的凸组合 | 板书二:$q=\frac{p-v}{u-v}$ 的移项求解与 $q\in(0,1)$ 验证 | 结论卡:指定数据不可能;区间内任意值可实现

Steps:
第一步:记 $u=P(A\mid B)$,$v=P(A\mid B^c)$,$q=P(B)\in(0,1)$;全概率公式:$P(A)=qu+(1-q)v$。
第二步:凸组合(关键点,高亮):$qu+(1-q)v$ 是 $u,v$ 的凸组合,权重 $q,1-q$ 均在 $(0,1)$;若 $u\ne v$,则 $P(A)$ 严格位于 $\min(u,v)$ 与 $\max(u,v)$ 之间;若 $u=v$,等于共同值。
第三步:指定数据检验:$u=\frac9{10}$,$v=\frac45$,可行区间为 $(\frac45,\frac9{10})$;而 $P(A)=\frac1{10}$ 不在其中 → 不可能。
第四步:可实现性(逐步,高亮):任何严格介于两者之间的 $p$,由 $p=qu+(1-q)v$ 移项:$q(u-v)=p-v$,即 $q=\frac{p-v}{u-v}$;验证 $q\in(0,1)$:由 $v<p<u$ 得 $p-v>0$ 且 $p-v<u-v$。
第五步:构造:取四原子概率 $qu,q(1-u),(1-q)v,(1-q)(1-v)$ 即得所需事件(高亮)。


## draft-c46-04

P: 在单位正方形上取联合密度$f(x,y)=x+y$，其余地方为零。验证这是概率密度，求$P(X\le1/2)$，并解释为什么此时不能直接用事件区域与正方形的普通面积之比。

S: $f\ge0$且$\int_0^1\int_0^1(x+y)\,dy\,dx=\int_0^1(x+1/2)\,dx=1$，故密度有效。所求概率为$\int_0^{1/2}\int_0^1(x+y)\,dy\,dx=\int_0^{1/2}(x+1/2)\,dx=1/8+1/4=3/8$。事件区域的普通面积为$1/2$，但该分布不是均匀分布，所以普通面积比不是概率；正确几何表示是密度加权面积。边界线$x=1/2$零测，不影响结果。

A: 密度归一化积分为$1$；$P(X\le1/2)=3/8$，普通面积比$1/2$不适用。

Objects: 题面卡:$f(x,y)=x+y$ 在单位正方形上的概率 | 板书一:归一化积分的逐项计算 | 高亮框:关键点——$P(X\le\frac12)=\int_0^{\frac12}(x+\frac12)dx=\frac38$ | 对照板:普通面积比 $\frac12$ 与密度加权结果 $\frac38$ | 结论卡:非均匀分布用密度加权面积

Steps:
第一步:归一化(逐项,高亮):$f\ge0$;$\int_0^1\int_0^1(x+y)\,dy\,dx=\int_0^1[xy+\frac{y^2}2]_0^1dx=\int_0^1(x+\frac12)dx=[\frac{x^2}2+\frac x2]_0^1=1$;故密度有效。
第二步:所求概率(逐项):$P(X\le\frac12)=\int_0^{\frac12}\int_0^1(x+y)\,dy\,dx=\int_0^{\frac12}(x+\frac12)\,dx$。
第三步:求值(逐步):$[\frac{x^2}2+\frac x2]_0^{\frac12}=\frac18+\frac14=\frac38$(高亮)。
第四步:对照:事件区域 $\{x\le\frac12\}$ 的普通面积为 $\frac12$,但该分布不是均匀分布,面积比 $\frac12\ne\frac38$。
第五步:结论(高亮):正确的几何表示是密度加权面积,不能直接用区域与正方形的普通面积之比。
