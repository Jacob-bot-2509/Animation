# 精确场景修订稿

以下为本轮十一题的新场景；原始题干、过程、答案与来源绑定。直角边界的题干修订另存 math-wording-c27-04.candidate.jsonl。完整视觉验收未执行。

## draft-c07-03

题目：求四叶玫瑰线 $r=\cos 2\theta$ 所围成的总面积，并说明为什么只需计算一叶再乘 $4$。

答案：总面积为 $\frac{\pi}{2}$(一叶 $\frac{\pi}{8}$ 乘 $4$)。

修订场景：

第一步:确定一叶角域(高亮):当 $-\frac{\pi}{4}\le\theta\le\frac{\pi}{4}$ 时 $2\theta\in[-\frac{\pi}{2},\frac{\pi}{2}]$,$r=\cos2\theta\ge0$ 且极径从 $0$ 出发回到 $0$,描出一叶;四叶由四段对称生成 → 总面积 $=4A_1$。

第二步:极坐标面积公式:$A_1=\frac{1}{2}\int_{-\frac{\pi}{4}}^{\frac{\pi}{4}}\cos^2(2\theta)\,d\theta$。

第三步：换元 $u=2\theta$，$d\theta=\frac{1}{2}du$；上下限分别变为 $-\frac{\pi}{2}$、$\frac{\pi}{2}$。逐项写出 $\int_{-\frac{\pi}{4}}^{\frac{\pi}{4}}\cos^2(2\theta)\,d\theta=\frac{1}{2}\int_{-\frac{\pi}{2}}^{\frac{\pi}{2}}\cos^2u\,du$；高亮两端均为定积分。

第四步:计算(逐步):半角公式 $\cos^2u=\frac{1+\cos2u}{2}$;原函数 $\frac{u}{2}+\frac{\sin2u}{4}$;代入:$[\frac{u}{2}+\frac{\sin2u}{4}]_{-\frac{\pi}{2}}^{\frac{\pi}{2}}=\frac{\pi}{4}+\frac{\pi}{4}=\frac{\pi}{2}$;故 $A_1=\frac{1}{2}\cdot\frac{1}{2}\cdot\frac{\pi}{2}=\frac{\pi}{8}$。

第五步:总面积 $A=4A_1=4\times\frac{\pi}{8}=\frac{\pi}{2}$(逐步乘法,高亮结论)。

## draft-c10-05

题目：证明莱布尼茨判别法:若 $a_n$ 单调递减趋于 $0$,则交错级数 $\sum_{n=1}^{\infty}(-1)^{n+1}a_n$ 收敛,且其和 $S$ 满足 $|S-S_N|\le a_{N+1}$。

答案：证明见解法(偶子列单调有界、奇子列同极限;余项 $|S-S_N|\le a_{N+1}$)。

修订场景：

第一步:写出条件:$a_n\ge0$ 且 $a_{n+1}\le a_n$、$a_n\to0$;部分和 $S_N=\sum_{n=1}^N(-1)^{n-1}a_n$。

第二步:单调性(逐项,高亮):$S_{2m+2}-S_{2m}=a_{2m+1}-a_{2m+2}\ge0$,偶部分和递增;$S_{2m+3}-S_{2m+1}=-a_{2m+2}+a_{2m+3}\le0$,奇部分和递减。

第三步：高亮真正的交叉序 $S_{2m}\le S_{2l+1}$，对任意 $m,l\ge0$ 成立。若 $m\le l$，由偶子列递增得 $S_{2m}\le S_{2l}\le S_{2l+1}$；若 $m>l$，由奇子列递减得 $S_{2m}\le S_{2m+1}\le S_{2l+1}$。因此 $0=S_0\le S_{2m}\le S_1$，两子列单调有界；$S_{2N+1}-S_{2N}=a_{2N+1}\to0$，故两极限相同，记为 $S$。

第四步:夹逼(关键点):由 $S_{2N}\le S\le S_{2N+1}$ 得 $0\le S-S_{2N}\le a_{2N+1}$;由 $S_{2N+2}\le S\le S_{2N+1}$ 得 $0\le S_{2N+1}-S\le a_{2N+2}$;统一写成 $0\le(-1)^N(S-S_N)\le a_{N+1}$。

第五步:结论:$|S-S_N|\le a_{N+1}$,交错级数收敛且余项受下一项控制;该证明只涉及有限部分和及其极限(高亮)。

## draft-c17-04

题目：设两相交平面$f_1=x+y+z-1=0$、$f_2=x-y+2z=0$交于直线$l$。给出包含$l$的全部平面，并分类经过给定点$P$的成员；最后求经过$(1,1,1)$的成员。

答案：全部$s f_1+t f_2=0$，$(s:t)\in\mathbb{RP}^1$；$P\in l$时全部，否则唯一；指定点对应$2y-z=1$。

修订场景：

第一步:法向量 $n_1=(1,1,1)$、$n_2=(1,-1,2)$ 不成比例,线性无关;任何包含交线 $l$ 的平面,其法向量必属于 $\operatorname{span}(n_1,n_2)$(高亮)。

第二步:全部平面:$sf_1+tf_2=0$,$(s,t)\ne(0,0)$;比例 $(s:t)$ 标识同一平面;该齐次表示包含 $f_2=0$(取 $s=0,t=1$),而 $f_1+\lambda f_2$ 形式会遗漏它(关键点)。

第三步:过点条件(逐项代入):$P=(1,1,1)$:$f_1(P)=1+1+1-1=2$;$f_2(P)=1-1+2\cdot1=2$(高亮)。

第四步:解比例:$sf_1(P)+tf_2(P)=2s+2t=0$,即 $s=-t$;取 $(s:t)=(1:-1)$。

第五步:所求平面:$f_1-f_2=0$,逐项相减:$(x+y+z-1)-(x-y+2z)=2y-z-1$,即 $2y-z-1=0$(高亮结论)。

第六步：补全任意给定点 $P$ 的分类。高亮过点条件 $s f_1(P)+t f_2(P)=0$：若两值均零，则 $P\in l$，全部成员都过 $P$；否则非零解的射影比例唯一，为 $(s:t)=(f_2(P):-f_1(P))$。指定点 $(1,1,1)$ 的比例 $(2:-2)=(1:-1)$ 与前面计算一致。

## draft-c20-04

题目：椭球$x^2+2y^2+3z^2=1$与平面$x+y+z=t$相交。求截面中心、全部空集或退化情形，以及非退化截面的精确半轴长。

答案：中心$(6t,3t,2t)/11$；阈值$|t|=\sqrt{11/6}$；椭圆半轴$\sqrt{(1-6t^2/11)/(2\mp1/\sqrt3)}$。

修订场景：

第一步:记 $W=\operatorname{diag}(1,2,3)$、$n=(1,1,1)$;平面上二次型的最小点为 $c=\frac{tW^{-1}n}{n^{\mathsf T}W^{-1}n}$。

第二步:逐项计算(高亮):$W^{-1}n=(1,\frac{1}{2},\frac{1}{3})$;$n^{\mathsf T}W^{-1}n=1+\frac{1}{2}+\frac{1}{3}=\frac{11}{6}$;故 $c=\frac{t}{11/6}(1,\frac{1}{2},\frac{1}{3})=\frac{t}{11}(6,3,2)$。

第三步:逐项代入:$c^{\mathsf T}Wc=\frac{t^2}{121}(36+2\cdot9+3\cdot4)=\frac{t^2}{121}\cdot66=\frac{6t^2}{11}$(高亮)。

第四步：写 $x=c+h$，$n^{\mathsf T}h=0$。先逐分量算 $Wc=\frac{t}{11}(6,6,6)^{\mathsf T}=\frac{6t}{11}n$，于是 $2c^{\mathsf T}Wh=2(Wc)^{\mathsf T}h=\frac{12t}{11}n^{\mathsf T}h=0$。截面满足 $h^{\mathsf T}Wh=1-\frac{6t^2}{11}$；$|t|>\sqrt{\frac{11}{6}}$ 时空集，等号时仅为 $c$，严格小于时为椭圆。

第五步:半轴(逐分量行×列,高亮):切向正交基 $e=(1,-1,0)/\sqrt2$、$f=(1,1,-2)/\sqrt6$;$e^{\mathsf T}We=\frac{1+2}{2}=\frac{3}{2}$;$e^{\mathsf T}Wf=\frac{1-2+0}{\sqrt2\sqrt6}=-\frac{1}{2\sqrt3}$;$f^{\mathsf T}Wf=\frac{1+2+12}{6}=\frac{5}{2}$;限制矩阵特征值为 $2\pm\frac{1}{\sqrt3}$,半轴 $\sqrt{\frac{1-6t^2/11}{2\mp1/\sqrt3}}$。

第六步：高亮限制矩阵的特征方程 $\left(\lambda-\frac{3}{2}\right)\left(\lambda-\frac{5}{2}\right)-\frac{1}{12}=\lambda^2-4\lambda+\frac{11}{3}=(\lambda-2)^2-\frac{1}{3}=0$。故特征值为 $2\pm\frac{1}{\sqrt3}$；在正交特征坐标中逐轴用 $\lambda_j u_j^2=1-\frac{6t^2}{11}$ 求半轴，无小数估算。

## draft-c25-05

题目：求球$x^2+y^2+z^2=1$与抛物柱面$y=x^2$的实交线，给参数域、分支连接关系，证明交线正则且非平面。

答案：两弧$(t,t^2,\pm\sqrt{1-t^2-t^4})$，$|t|\le\sqrt{(\sqrt5-1)/2}$；连接为一条正则非平面闭曲线。

修订场景：

第一步:参数化:$x=t$,$y=t^2$,$z=\pm\sqrt{1-t^2-t^4}$;解不等式(逐步):$1-t^2-t^4\ge0$;令 $s=t^2\ge0$,得 $s^2+s-1\le0$;方程 $s^2+s-1=0$ 的根为 $\frac{-1\pm\sqrt5}{2}$,取正根 $s\le\frac{\sqrt5-1}{2}$;故 $|t|\le r=\sqrt{\frac{\sqrt5-1}{2}}$(高亮)。

第二步:分支连接(关键点):两弧在 $t=\pm r$ 处汇于 $(\pm r,r^2,0)$(此时 $z=0$);正负两弧合为一条闭曲线,不能误称两个连通分量。

第三步:正则性:$z\ne0$ 时,球面梯度 $(2t,2t^2,2z)$ 与柱面梯度 $(-2t,1,0)$ 显然线性无关(第三分量结构不同)。

第四步:$z=0$ 情形(关键点):此时 $t\ne0$;若两梯度成比例,设 $(2t,2t^2,0)=\lambda(-2t,1,0)$:第一坐标给 $\lambda=-1$,第二坐标要求 $2t^2=\lambda=-1$,但 $2t^2\ge0$,矛盾;故线性无关。

第五步:端点光滑参数(关键点):根号图形在端点不可作光滑参数;改以 $z$ 为参数:消元 $y=x^2$ 代入球面得 $x^2+x^4+z^2=1$;令 $s=x^2$,解 $s^2+s+(z^2-1)=0$ 得 $s=\frac{-1+\sqrt{5-4z^2}}{2}$(取正根),即 $x=\pm\sqrt{\frac{-1+\sqrt{5-4z^2}}{2}}$;故交线为正则非平面闭曲线(高亮)。

第六步：补全非平面证明。若整条交线在平面 $ax+by+cz=d$ 内，代入交线上的 $(0,0,1)$、$(0,0,-1)$ 得 $c=d=0$；再代入 $(r,r^2,0)$、$(-r,r^2,0)$，其中 $r>0$，得 $ar+br^2=0$、$-ar+br^2=0$，逐式相减、相加得 $a=b=0$。这与平面法向量非零矛盾。因此交线确为非平面；前五步已证明连接性与正则性。

## draft-c26-01

题目：令$n=(1,2,-1)$、$d=(1,1,0)$，定义$P(x)=x-(n\cdot x)d/3$。求矩阵、核与像，证明其为沿$d$投影到$n\cdot x=0$的斜投影，判断是否为Euclidean正交投影。

答案：$\ker P=\operatorname{span}(1,1,0)$，$\operatorname{im}P=n^{\perp}$，$P^2=P$；斜投影而非Euclidean正交投影。

修订场景：

第一步:验证投影性质(逐项,高亮):$n\cdot d=(1,2,-1)\cdot(1,1,0)=1+2+0=3$;$Pd=d-\frac{(n\cdot d)d}{3}=d-d=0$;$n\cdot Px=n\cdot x-\frac{(n\cdot d)(n\cdot x)}{3}=n\cdot x-n\cdot x=0$。

第二步：完整证明核与像。$Px=0$ 当且仅当 $x=\frac{n\cdot x}{3}d$，即 $x\in\operatorname{span}(d)$；反向由 $Pd=0$ 及线性性成立。第一步给 $\operatorname{im}P\subset n^\perp$；若 $y\in n^\perp$，则 $Py=y$，给反向包含。因此 $\ker P=\operatorname{span}(d)$、$\operatorname{im}P=n^\perp$，且 $P^2x=P(Px)=Px$，秩为 $2$。

第三步:逐列求矩阵(逐分量,高亮):$Pe_1=e_1-\frac{(n\cdot e_1)d}{3}=(1,0,0)-\frac{(1,1,0)}{3}=(\frac{2}{3},-\frac{1}{3},0)$;$Pe_2=(0,1,0)-\frac{(2,2,0)}{3}=(-\frac{2}{3},\frac{1}{3},0)$;$Pe_3=(0,0,1)-\frac{(-1,-1,0)}{3}=(\frac{1}{3},\frac{1}{3},1)$;得 $P=\begin{pmatrix}\frac{2}{3}&-\frac{2}{3}&\frac{1}{3}\\-\frac{1}{3}&\frac{1}{3}&\frac{1}{3}\\0&0&1\end{pmatrix}$。

第四步:判定(关键点):核方向 $d=(1,1,0)$ 不平行法向量 $n=(1,2,-1)$,且矩阵不对称;故是沿 $d$ 到 $n^\perp$ 的斜投影,不是 Euclidean 正交投影(高亮)。

第五步:分解唯一性:$x=Px+\frac{(n\cdot x)d}{3}$,第一项在 $n^\perp$、第二项在核中,说明投影方向(高亮)。

## draft-c27-04

题目：设$A_k=\begin{pmatrix}1&k\\0&2\end{pmatrix}$，$k\in\mathbb R$。求对角化并判断何时能正交对角化，给两特征线的锐夹角精确式。

答案：所有$k$可对角化；正交对角化当且仅当$k=0$；$\alpha=\arccos(|k|/\sqrt{k^2+1})$。

修订场景：

第一步:求特征值:$\det(A_k-\lambda I)=\begin{vmatrix}1-\lambda&k\\0&2-\lambda\end{vmatrix}=(1-\lambda)(2-\lambda)$;特征值为 $1,2$。

第二步:求特征向量:$\lambda=1$:解 $(A_k-I)v=0$,即 $\begin{pmatrix}0&k\\0&1\end{pmatrix}v=0$,得 $v=e_1=(1,0)$;$\lambda=2$:解 $(A_k-2I)v=0$,即 $-x+ky=0$,得 $v=(k,1)$。

第三步:验算对角化(逐行×列,高亮):$P=\begin{pmatrix}1&k\\0&1\end{pmatrix}$;$A_kP$ 第1行×第1列:$1\cdot1+k\cdot0=1$;第1行×第2列:$1\cdot k+k\cdot1=2k$;第2行×第1列:$0\cdot1+2\cdot0=0$;第2行×第2列:$0\cdot k+2\cdot1=2$;得 $A_kP=\begin{pmatrix}1&2k\\0&2\end{pmatrix}=P\operatorname{diag}(1,2)$;$\det P=1$,故所有 $k$ 可对角化。

第四步:夹角公式(逐项):两特征线方向 $e_1=(1,0)$ 与 $(k,1)$;点积 $\langle e_1,(k,1)\rangle=1\cdot k+0\cdot1=k$;模长 $\|(k,1)\|=\sqrt{k^2+1}$,$\|e_1\|=1$;故 $\cos\alpha=\frac{|k|}{1\cdot\sqrt{k^2+1}}$;仅 $k=0$ 时 $\cos\alpha=0$,垂直。

第五步:正交对角化判定:实矩阵可正交对角化为实对角阵必对称;而 $A_k^{\mathsf T}=\begin{pmatrix}1&0\\k&2\end{pmatrix}$ 与 $A_k$ 相等当且仅当 $k=0$;故正交对角化当且仅当 $k=0$,高亮结论。

第六步：角度边界须精确表述为两特征线的较小夹角 $0<\alpha\le\frac{\pi}{2}$；当 $k=0$ 时 $\alpha=\frac{\pi}{2}$，是直角；当 $k\ne0$ 时才是锐角。仍用 $\alpha=\arccos\frac{|k|}{\sqrt{k^2+1}}$，不把直角称为锐角。

## draft-c34-05

题目：记$E_{ij}(a)=I+a e_{ij}$（$i\ne j$），其中$e_{ij}$为三阶矩阵单位。证明$E_{12}(a)E_{23}(b)E_{12}(-a)E_{23}(-b)=E_{13}(ab)$，求逆矩阵，并用$a=2/3,b=3/4$精确验证。

答案：交换子$E_{13}(ab)$，逆$E_{13}(-ab)$；指定参数的非对角项$1/2$。

修订场景：

第一步:乘法规则(高亮):$e_{ij}e_{kl}=\delta_{jk}e_{il}$;关键事实:$e_{12}e_{23}=e_{13}$ 而 $e_{23}e_{12}=0$;各相关平方为零:$e_{12}^2=e_{23}^2=e_{13}^2=0$。

第二步：逐因子相乘：$(I+ae_{12})(I+be_{23})=I+ae_{12}+be_{23}+abe_{13}$。右乘 $(I-ae_{12})$ 时保持次序：$I+ae_{12}+be_{23}+abe_{13}-ae_{12}-a^2e_{12}^2-ab e_{23}e_{12}-a^2b e_{13}e_{12}=I+be_{23}+abe_{13}$。高亮 $e_{23}e_{12}=0$，不能误写为 $e_{12}e_{23}=e_{13}$。

第三步:再乘 $(I-be_{23})$:$(I+be_{23}+abe_{13})(I-be_{23})=I+be_{23}+abe_{13}-be_{23}-b^2e_{23}^2-ab^2e_{13}e_{23}=I+abe_{13}$;故复合 $=E_{13}(ab)$(关键点:$e_{13}$ 项经 $e_{12}e_{23}=e_{13}$ 积累系数 $ab$,高亮)。

第四步:逆公式验证(逐项):$(I+ae_{ij})(I-ae_{ij})=I+ae_{ij}-ae_{ij}-a^2e_{ij}^2=I$(因 $e_{ij}^2=0$);故 $E_{ij}(a)^{-1}=E_{ij}(-a)$,最终逆为 $E_{13}(-ab)$。

第五步:代入验证(逐步):$a=\frac{2}{3},b=\frac{3}{4}$:$ab=\frac{2}{3}\cdot\frac{3}{4}=\frac{1}{2}$;复合为 $E_{13}(\frac{1}{2})=I+\frac{1}{2}e_{13}$,$(1,3)$ 元为 $\frac{1}{2}$(高亮结论)。

## draft-c43-03

题目：在$V=\mathbb R[x]_{\le2}$中取基$1,x,x^2$。求三个多项式$g_0,g_1,g_2$，使$f_i(p)=\int_{-1}^1g_i(x)p(x)\,dx$为此基的对偶泛函，并证明九个配对值。

答案：$g_0=(9-15x^2)/8,g_1=3x/2,g_2=(-15+45x^2)/8$；$f_i(p)=\int_{-1}^1g_i p$组成对偶基。

修订场景：

第一步:矩阵 $G_{ij}=\int_{-1}^1x^{i+j}dx$;逐项计算(高亮):$G_{00}=2$;$G_{01}=G_{10}=0$;$G_{02}=G_{20}=\frac{2}{3}$;$G_{11}=\frac{2}{3}$;$G_{12}=G_{21}=0$;$G_{22}=\frac{2}{5}$;得 $G=\begin{pmatrix}2&0&\frac{2}{3}\\0&\frac{2}{3}&0\\\frac{2}{3}&0&\frac{2}{5}\end{pmatrix}$。

第二步:配对条件:$f_i(x^j)=\int_{-1}^1g_i(x)x^jdx=\delta_{ij}$;若 $g_i$ 的系数为矩阵 $C$ 的第 $i$ 行,则 $CG=I$。

第三步:解 $C=G^{-1}$ 并逐行×列验算 $CG=I$(高亮):第1行×第1列:$\frac{9}{8}\cdot2+(-\frac{15}{8})\cdot\frac{2}{3}=\frac{9}{4}-\frac{5}{4}=1$;第1行×第3列:$\frac{9}{8}\cdot\frac{2}{3}-\frac{15}{8}\cdot\frac{2}{5}=\frac{3}{4}-\frac{3}{4}=0$;第2行×第2列:$\frac{3}{2}\cdot\frac{2}{3}=1$;第3行×第1列:$-\frac{15}{8}\cdot2+\frac{45}{8}\cdot\frac{2}{3}=0$;第3行×第3列:$-\frac{15}{8}\cdot\frac{2}{3}+\frac{45}{8}\cdot\frac{2}{5}=1$。

第四步:故 $g_0=\frac{9-15x^2}{8}$,$g_1=\frac{3x}{2}$,$g_2=\frac{-15+45x^2}{8}$。

第五步：九个配对值逐项展示，所有积分均在 $[-1,1]$。第一行：$\int g_0=\frac{18-10}{8}=1$，$\int g_0x=0$，$\int g_0x^2=\frac{6-6}{8}=0$。第二行：$\int g_1=0$，$\int g_1x=\frac{3}{2}\cdot\frac{2}{3}=1$，$\int g_1x^2=0$。第三行：$\int g_2=\frac{-30+30}{8}=0$，$\int g_2x=0$，$\int g_2x^2=\frac{-10+18}{8}=1$。四个零项由奇函数在对称区间的积分为零得到；高亮完整配对矩阵为 $I_3$。

## draft-c48-04

题目：设独立$X\sim N(1,4),Y\sim N(2,9)$。求$S=X+Y,T=2X-Y$的分布及协方差，判断独立性；再求使$S$与$aX-Y$独立的全部实$a$。

答案：$S\sim N(3,13),T\sim N(0,25)$，协方差$-1$，不独立；唯一$a=9/4$。

修订场景：

第一步:均值方差(逐项,高亮):$ES=EX+EY=1+2=3$;$\operatorname{Var}S=4+9=13$(独立,无交叉项);$ET=2EX-EY=2-2=0$;$\operatorname{Var}T=4\cdot4+9=25$;故 $S\sim N(3,13)$,$T\sim N(0,25)$,从而 $P(T>0)=\frac{1}{2}$。

第二步:协方差(双线性展开,高亮):$\operatorname{Cov}(S,T)=\operatorname{Cov}(X+Y,2X-Y)=2\operatorname{Cov}(X,X)-\operatorname{Cov}(X,Y)+2\operatorname{Cov}(Y,X)-\operatorname{Cov}(Y,Y)$;独立性给 $\operatorname{Cov}(X,Y)=0$;故 $=2\operatorname{Var}X-\operatorname{Var}Y=8-9=-1\ne0$,不独立。

第三步:判定方法:$(S,aX-Y)$ 是 $(X,Y)$ 的线性变换,联合正态;联合正态下独立等价于协方差为零(高亮)。

第四步:求 $a$:$\operatorname{Cov}(X+Y,aX-Y)=a\operatorname{Var}X-\operatorname{Var}Y=4a-9$;令 $4a-9=0$,得唯一 $a=\frac{9}{4}$。

第五步：$a=\frac{9}{4}$ 时先高亮平方 $a^2=\frac{81}{16}$；均值为 $aEX-EY=\frac{9}{4}-2=\frac{1}{4}$，方差为 $a^2\operatorname{Var}X+\operatorname{Var}Y=\frac{81}{16}\cdot4+9=\frac{81}{4}+\frac{36}{4}=\frac{117}{4}$。故 $aX-Y\sim N\left(\frac{1}{4},\frac{117}{4}\right)$；与 $S$ 联合正态且协方差为零，因而独立。其余 $a$ 的协方差非零，不独立。

## draft-c49-05

题目：证明独立同分布且$E|X_1|<\infty$时样本均值依概率收敛到$\mu=EX_1$，无需有限方差。证明必须说明截断偏差和尾部概率怎样分别控制。

答案：$E|X_1|<\infty$的独立同分布样本满足$\overline X_n\xrightarrow P\mu$，不需要有限方差。

修订场景：

第一步:截断:$Y_i^{(M)}=X_i\mathbf1_{|X_i|\le M}$;$\tau_M=E[|X_1|\mathbf1_{|X_1|>M}]\to0$(由 $E|X_1|<\infty$,高亮)。

第二步:截断偏差(逐步,高亮):$|EY_1^{(M)}-\mu|=|E[X_1\mathbf1_{|X_1|>M}]|\le\tau_M$;$E|\overline X_n-\overline Y_n^{(M)}|\le\frac{1}{n}\sum_iE|X_i-Y_i^{(M)}|=\tau_M$。

第三步:截断方差(依据):独立性给 $\operatorname{Var}(\overline Y_n^{(M)})=\frac{1}{n^2}\sum_i\operatorname{Var}Y_i^{(M)}\le\frac{M^2}{n}$(因 $|Y|\le M$ 给 $\operatorname{Var}Y\le EY^2\le M^2$)。

第四步：对任意 $\varepsilon>0$，先选足够大的固定 $M$ 使 $\tau_M<\frac{\varepsilon}{3}$。三角不等式把误差分为平均尾部、截断均值波动、确定性偏差；后者小于 $\frac{\varepsilon}{3}$。对平均尾部用 Markov：$P\left(|\overline X_n-\overline Y_n^{(M)}|\ge\frac{\varepsilon}{3}\right)\le\frac{3\tau_M}{\varepsilon}$。对截断均值用切比雪夫：$P\left(|\overline Y_n^{(M)}-EY_1^{(M)}|\ge\frac{\varepsilon}{3}\right)\le\frac{9M^2}{n\varepsilon^2}$。故 $P(|\overline X_n-\mu|\ge\varepsilon)\le\frac{3\tau_M}{\varepsilon}+\frac{9M^2}{n\varepsilon^2}$。

第五步：高亮极限次序。对每个满足偏差条件的固定 $M$，先令 $n\to\infty$ 得 $\limsup_{n\to\infty}P(|\overline X_n-\mu|\ge\varepsilon)\le\frac{3\tau_M}{\varepsilon}$；再令 $M\to\infty$，由 $\tau_M\to0$ 得上界为零。于是 $\overline X_n\xrightarrow{P}\mu$；全程仅用 $E|X_1|<\infty$，没有假设原变量方差有限。
