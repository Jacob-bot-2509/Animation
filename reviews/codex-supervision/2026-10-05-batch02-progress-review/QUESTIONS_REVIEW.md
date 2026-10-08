# batch-02独立复审副本

15题核心数值通过；11题修订后可继续审题，3道级数须重写以隔离冻结评测，c51-02须增加后验任务或另归C45。未入库、未渲染验收。

## draft-c11-01

状态：ELIGIBLE_FOR_USER_REVIEW_WITH_CORRECTIONS

题目：求幂级数 $\sum_{n=1}^{\infty}\left(\frac{n}{n+1}\right)^{n^2}x^n$ 的收敛域。

答案：收敛域为 $(-e,e)$。

解答：令 $a_n=(\frac{n}{n+1})^{n^2}$。根值极限 $\lim_{n\to\infty}a_n^{1/n}=\exp(\lim_{n\to\infty}n\ln(1-\frac1{n+1}))=e^{-1}$，所以收敛半径 $R=e$。端点 $x=\pm e$ 的通项绝对值为 $\exp(n^2\ln(1-\frac1{n+1})+n)$。由 $\ln(1-v)=-v-\frac{v^2}{2}+O(v^3)$，其指数为 $n-\frac{n^2}{n+1}-\frac{n^2}{2(n+1)^2}+O(\frac1n)\to1-\frac12=\frac12$。通项绝对值趋于 $e^{1/2}\ne0$，两端点均发散。因此收敛域为 $(-e,e)$。

修订说明：根值极限补正确极限符号，端点展开给出余项O(1/n)依据

## draft-c11-02

状态：ELIGIBLE_FOR_USER_REVIEW_WITH_CORRECTIONS

题目：求幂级数 $\sum_{n=1}^{\infty}\frac{x^n}{\sqrt{n}}$ 的收敛域。

答案：收敛域为 $[-1,1)$(左端点条件收敛,右端点发散)。

解答：当 $|x|<1$ 时，$\lim_{n\to\infty}\left|\frac{x^{n+1}/\sqrt{n+1}}{x^n/\sqrt{n}}\right|=|x|\lim_{n\to\infty}\sqrt{\frac{n}{n+1}}=|x|<1$，级数绝对收敛。当 $x=1$ 时，级数为 $\sum_{n=1}^{\infty}\frac{1}{\sqrt{n}}$，是 $p=\frac12$ 的 $p$ 级数，发散。当 $x=-1$ 时，级数为 $\sum_{n=1}^{\infty}\frac{(-1)^n}{\sqrt{n}}$，$\frac{1}{\sqrt{n}}$ 单调递减趋于 $0$，由莱布尼茨判别法收敛。故收敛域为 $[-1,1)$。

修订说明：本轮未发现核心计算或表述错误。

## draft-c11-03

状态：REWRITE_REQUIRED

题目：求幂级数 $\sum_{n=1}^{\infty}\frac{x^n}{n(n+1)}$ 的收敛域与和函数，并求 $S(0)$、$S(1)$、$S(-1)$。

答案：收敛域 $[-1,1]$。对 $-1\le x<1$ 且 $x\ne0$，$S(x)=1+\frac{(1-x)\ln(1-x)}x$；另外 $S(0)=0$、$S(1)=1$，$S(-1)=1-2\ln2$。

解答：收敛域：$|x|<1$ 时由比值法收敛；$x=\pm1$ 时 $\left|\frac{(\pm1)^n}{n(n+1)}\right|\leq\frac{1}{n(n+1)}$ 且 $\sum\frac{1}{n(n+1)}$ 收敛，故两端点绝对收敛，收敛域为 $[-1,1]$。求和(先对 $|x|<1$)：拆项 $\frac{1}{n(n+1)}=\frac{1}{n}-\frac{1}{n+1}$，记 $A(x)=\sum_{n=1}^{\infty}\frac{x^n}{n}=-\ln(1-x)$，则 $\sum_{n=1}^{\infty}\frac{x^n}{n+1}=\frac{1}{x}\sum_{n=1}^{\infty}\frac{x^{n+1}}{n+1}=\frac{A(x)-x}{x}$($x\neq0$)。故 $S(x)=A(x)-\frac{A(x)-x}{x}=1+\frac{(1-x)\ln(1-x)}{x}$。$S(0)=0$(通项为 0)；$S(1)=\sum\frac{1}{n(n+1)}=1$(裂项求和),与公式在 $x\to1^-$ 的极限一致;$S(-1)=\sum\frac{(-1)^n}{n(n+1)}=1-2\ln2$(由公式 $1+\frac{2\ln2}{-1}$)。因为在 $[-1,1]$ 上 $|x^n/(n(n+1))|\le1/(n(n+1))$，由Weierstrass判别法一致收敛，所以和函数连续，$x=-1$ 的取值可由右极限得到；$x=1$ 用裂项或左极限取值，不能直接将 $\ln0$ 代入表达式。

修订说明：公式排除x=1/0，补端点合法性并纠正“原点=端点”用语；泄漏仍须整体重写

## draft-c11-04

状态：REWRITE_REQUIRED

题目：求幂级数 $\sum_{n=1}^{\infty}\frac{nx^n}{n!}$ 的收敛域与和函数。

答案：收敛域为 $\mathbb R$;和函数 $S(x)=xe^x$。

解答：比值法：$\lim_{n\to\infty}\left|\frac{(n+1)x^{n+1}/(n+1)!}{nx^n/n!}\right|=\lim_{n\to\infty}\frac{n+1}{n}\cdot\frac{|x|}{n+1}=0$，对一切实数 $x$ 收敛，收敛域为 $\mathbb R$。求和：$\sum_{n=1}^{\infty}\frac{nx^n}{n!}=\sum_{n=1}^{\infty}\frac{x^n}{(n-1)!}=x\sum_{m=0}^{\infty}\frac{x^m}{m!}=xe^x$。逐项运算的合法性由该级数在每个紧区间上一致收敛保证(指数级数)。

修订说明：澄清只保证每个紧区间上一致收敛；结构复用仍须重写

## draft-c11-05

状态：REWRITE_REQUIRED

题目：求幂级数 $\sum_{n=1}^{\infty}\frac{(-1)^nx^n}{n}$ 的收敛域与和函数，并求 $x=1$ 处的值(说明所用定理)。

答案：收敛域 $(-1,1]$;$S(x)=-\ln(1+x)$;$S(1)=-\ln2$(由阿贝尔定理)。

解答：当 $|x|<1$ 时由比值法绝对收敛。当 $x=1$ 时，级数为 $\sum_{n=1}^{\infty}\frac{(-1)^n}{n}$，由莱布尼茨判别法($\frac1n$ 单调递减趋于 $0$)收敛；当 $x=-1$ 时，级数为 $\sum\frac{1}{n}$，发散。故收敛域为 $(-1,1]$。求和：对 $|x|<1$，$\sum_{n=1}^{\infty}(-1)^{n+1}\frac{x^n}{n}=\ln(1+x)$，故 $S(x)=-\ln(1+x)$。$x=1$ 处级数收敛，由阿贝尔定理，$S(1)=\lim_{x\to1^-}S(x)=\lim_{x\to1^-}-\ln(1+x)=-\ln2$。

修订说明：本轮未发现核心计算或表述错误。

## draft-c33-01

状态：ELIGIBLE_FOR_USER_REVIEW_WITH_CORRECTIONS

题目：用初等行变换求矩阵 $A=\begin{pmatrix}1&2&3\\0&1&2\\0&0&1\end{pmatrix}$ 的逆矩阵。

答案：$A^{-1}=\begin{pmatrix}1&-2&1\\0&1&-2\\0&0&1\end{pmatrix}$。

解答：构造增广矩阵并作行变换:$\left(\begin{array}{ccc|ccc}1&2&3&1&0&0\\0&1&2&0&1&0\\0&0&1&0&0&1\end{array}\right)$。第三行乘 $-2$ 加到第二行、乘 $-3$ 加到第一行,得 $\left(\begin{array}{ccc|ccc}1&2&0&1&0&-3\\0&1&0&0&1&-2\\0&0&1&0&0&1\end{array}\right)$;第二行乘 $-2$ 加到第一行,得 $\left(\begin{array}{ccc|ccc}1&0&0&1&-2&1\\0&1&0&0&1&-2\\0&0&1&0&0&1\end{array}\right)$。故 $A^{-1}=\begin{pmatrix}1&-2&1\\0&1&-2\\0&0&1\end{pmatrix}$。验证:$AA^{-1}=I$(逐项相乘即得)。

修订说明：本轮未发现核心计算或表述错误。

## draft-c33-02

状态：ELIGIBLE_FOR_USER_REVIEW_WITH_CORRECTIONS

题目：求使矩阵 $A=\begin{pmatrix}1&1&a\\1&a&1\\a&1&1\end{pmatrix}$ 可逆的参数 $a$ 的取值范围；并求 $a=0$ 时的逆矩阵。

答案：可逆当且仅当 $a\neq1$ 且 $a\neq-2$;$a=0$ 时 $A^{-1}=\frac12\begin{pmatrix}1&1&-1\\1&-1&1\\-1&1&1\end{pmatrix}$。

解答：计算行列式(按第一行展开)：$\det A=1\times(a\cdot1-1\cdot1)-1\times(1\cdot1-1\cdot a)+a\times(1\cdot1-a\cdot a)=(a-1)-(1-a)+a(1-a^2)=3a-2-a^3=-(a-1)^2(a+2)$。可逆当且仅当 $\det A\neq0$，即 $a\neq1$ 且 $a\neq-2$。当 $a=0$ 时，$A=\begin{pmatrix}1&1&0\\1&0&1\\0&1&1\end{pmatrix}$。由增广矩阵消元(或直接验证)得 $A^{-1}=\frac12\begin{pmatrix}1&1&-1\\1&-1&1\\-1&1&1\end{pmatrix}$。验证:$AA^{-1}=I$。

修订说明：本轮未发现核心计算或表述错误。

## draft-c33-03

状态：ELIGIBLE_FOR_USER_REVIEW_WITH_CORRECTIONS

题目：用分块方法求矩阵 $M=\begin{pmatrix}2&1&1\\1&1&0\\0&0&2\end{pmatrix}$ 的逆矩阵。

答案：$M^{-1}=\begin{pmatrix}1&-1&-\frac12\\-1&2&\frac12\\0&0&\frac12\end{pmatrix}$。

解答：将 $M$ 分块为 $\begin{pmatrix}A&b\\0&d\end{pmatrix}$，其中 $A=\begin{pmatrix}2&1\\1&1\end{pmatrix}$，$b=\begin{pmatrix}1\\0\end{pmatrix}$，$d=2$。$A$ 可逆且 $A^{-1}=\begin{pmatrix}1&-1\\-1&2\end{pmatrix}$。由分块上三角矩阵求逆公式，$M^{-1}=\begin{pmatrix}A^{-1}&-\frac{1}{d}A^{-1}b\\0&\frac{1}{d}\end{pmatrix}$。计算 $A^{-1}b=\begin{pmatrix}1\\-1\end{pmatrix}$，故 $-\frac12A^{-1}b=\begin{pmatrix}-\frac12\\\frac12\end{pmatrix}$。于是 $M^{-1}=\begin{pmatrix}1&-1&-\frac12\\-1&2&\frac12\\0&0&\frac12\end{pmatrix}$。验证:$MM^{-1}=I$(逐行相乘核对)。

修订说明：修正真实U+0008退格转义为LaTeX\begin

## draft-c33-04

状态：ELIGIBLE_FOR_USER_REVIEW_WITH_CORRECTIONS

题目：求矩阵 $A=\begin{pmatrix}1&0\\0&1\\1&1\end{pmatrix}$ 的一个左逆与矩阵 $B=\begin{pmatrix}1&0&1\\0&1&1\end{pmatrix}$ 的一个右逆，并说明这两种单边逆的区别与不唯一性。

答案：$L=\begin{pmatrix}1&0&0\\0&1&0\end{pmatrix}$ 满足 $LA=I_2$，$R=\begin{pmatrix}1&0\\0&1\\0&0\end{pmatrix}$ 满足 $BR=I_2$。一般左逆要求列满秩、$m\ge n$，右逆要求行满秩、$m\le n$；本题两种单边逆均不唯一，可逆方阵则有唯一双边逆。

解答：$A$ 为 $3\times2$ 列满秩矩阵。取 $L=\begin{pmatrix}1&0&0\\0&1&0\end{pmatrix}$，则 $LA=\begin{pmatrix}1&0\\0&1\end{pmatrix}=I_2$，故 $L$ 是 $A$ 的一个左逆。$B$ 为 $2\times3$ 行满秩矩阵。取 $R=\begin{pmatrix}1&0\\0&1\\0&0\end{pmatrix}$，则 $BR=\begin{pmatrix}1&0\\0&1\end{pmatrix}=I_2$，故 $R$ 是 $B$ 的一个右逆。区别:列满秩的「高瘦」矩阵只可能有左逆($LA=I$),行满秩的「宽扁」矩阵只可能有右逆($BR=I$);只有方阵且可逆时才存在同时满足两侧的双边逆。不唯一性:$A$ 的左逆一般形式为 $\begin{pmatrix}1-t&-t&t\\-s&1-s&s\end{pmatrix}$($t,s$ 为任意实数),$L$ 对应 $t=s=0$,$\begin{pmatrix}0&-1&1\\1&2&-1\end{pmatrix}$ 对应 $t=1,s=-1$,也是左逆;$B$ 的右逆同理不唯一。一般地，$m\times n$ 矩阵有左逆当且仅当列满秩（故$m\ge n$），有右逆当且仅当行满秩（故$m\le n$）。严格高瘦/宽扁情形的相应单边逆不唯一；可逆方阵的左右逆一致且唯一。因本题 $B=A^{\mathsf T}$，全部右逆可写成 $R(t,s)=\begin{pmatrix}1-t&-s\\-t&1-s\\t&s\end{pmatrix}$，有 $BR(t,s)=I_2$。

修订说明：一般结论包含可逆方阵，明确本题非方阵的不唯一性并给出全部右逆

## draft-c33-05

状态：ELIGIBLE_FOR_USER_REVIEW_WITH_CORRECTIONS

题目：求矩阵 $A=\begin{pmatrix}1&a&a^2\\0&1&a\\0&0&1\end{pmatrix}$ 的逆矩阵，并说明 $A$ 对一切实数 $a$ 可逆。

答案：$A^{-1}=\begin{pmatrix}1&-a&0\\0&1&-a\\0&0&1\end{pmatrix}$;$\det A=1\neq0$,对一切实数 $a$ 可逆。

解答：令 $N=\begin{pmatrix}0&1&0\\0&0&1\\0&0&0\end{pmatrix}$，则 $N^2=\begin{pmatrix}0&0&1\\0&0&0\\0&0&0\end{pmatrix}$，$N^3=0$(幂零)，且 $A=I+aN+a^2N^2$。对幂零矩阵有 $(I+M)^{-1}=I-M+M^2-M^3+\cdots$(级数有限终止)。令 $M=aN+a^2N^2$，则 $M^2=a^2N^2$，$M^3=0$，故 $A^{-1}=I-M+M^2=I-aN-a^2N^2+a^2N^2=I-aN=\begin{pmatrix}1&-a&0\\0&1&-a\\0&0&1\end{pmatrix}$。验证:$AA^{-1}=I$。可逆性:$A$ 为上三角矩阵,$\det A=1\neq0$,与 $a$ 无关,故对一切实数 $a$ 可逆。

修订说明：本轮未发现核心计算或表述错误。

## draft-c51-01

状态：ELIGIBLE_FOR_USER_REVIEW_WITH_CORRECTIONS

题目：三台机器 $M_1,M_2,M_3$ 的产量分别占总产量的 $\frac12$、$\frac3{10}$、$\frac15$，次品率分别为 $\frac1{50}$、$\frac3{100}$、$\frac1{25}$。随机抽取一件产品发现是次品，求它分别来自三台机器的概率，并验证三者之和为 $1$。

答案：$P(M_1\mid D)=\frac{10}{27}$，$P(M_2\mid D)=\frac13$，$P(M_3\mid D)=\frac{8}{27}$;三者之和为 $1$。

解答：记 $D$ 为抽到次品。$P(D)=\frac12\times\frac{2}{100}+\frac{3}{10}\times\frac{3}{100}+\frac15\times\frac{4}{100}=\frac{1}{100}+\frac{9}{1000}+\frac{8}{1000}=\frac{27}{1000}$。由贝叶斯公式，$P(M_1\mid D)=\frac{\frac12\times\frac{2}{100}}{\frac{27}{1000}}=\frac{10}{27}$，$P(M_2\mid D)=\frac{\frac{3}{10}\times\frac{3}{100}}{\frac{27}{1000}}=\frac{9}{27}=\frac13$，$P(M_3\mid D)=\frac{\frac15\times\frac{4}{100}}{\frac{27}{1000}}=\frac{8}{27}$。验证:$\frac{10}{27}+\frac13+\frac{8}{27}=\frac{10+9+8}{27}=1$。

修订说明：百分比占比统一改分数，核心值不变

## draft-c51-02

状态：REWRITE_REQUIRED

题目：说明「独立」与「条件独立」互不蕴含：构造一个例子说明两个事件条件独立但(无条件)不独立；再构造一个例子说明两个事件独立但给定第三个事件后条件不独立。

答案：例一:双面硬币袋中随机取一枚抛两次,$A,B$ 给定硬币条件独立但无条件不独立;例二:均匀硬币抛两次,$A$={第二次正}、$B$={两次相同}、$C$={第一次正},$A,B$ 独立但给定 $C$ 条件不独立。

解答：例一：以概率$\frac12$选择双正面或双反面硬币，令$K$为硬币种类，$A,B$分别为两次出现正面的事件。给定$K=\mathrm{HH}$时$P(A\mid K)=P(B\mid K)=P(A\cap B\mid K)=1$，给定$K=\mathrm{TT}$时均为$0$，两种条件下均有条件联合概率等于边缘概率乘积；但无条件$P(A\cap B)=\frac12\ne\frac14=P(A)P(B)$。例二：独立均匀硬币抛两次，令$A$为第二次正面，$B$为两次相同，$C$为第一次正面。无条件$P(A)=P(B)=\frac12$、$P(A\cap B)=\frac14$，故独立；给定$C$时，$P(A\cap B\mid C)=\frac12\ne\frac14=P(A\mid C)P(B\mid C)$，故不条件独立。

修订说明：明确条件随机变量K避免C=C1错误；按现有题目归C45，仍需新增C51后验任务才能计入本批目标

## draft-c51-03

状态：ELIGIBLE_FOR_USER_REVIEW_WITH_CORRECTIONS

题目：某疾病患病率为 $\frac{1}{1000}$。一次检测对患病者呈阳性的概率为 $\frac{99}{100}$，对未患病者呈阳性的概率为 $\frac{1}{100}$。某人第一次检测呈阳性，随后做了一次独立(在给定患病状态下)的同类检测，仍呈阳性。求两次检测后此人患病的概率，并与第一次检测后的概率对比。

答案：第一次阳性后:$P=\frac{11}{122}$;两次阳性后:$P=\frac{363}{400}$。

解答：第一次阳性后，由贝叶斯公式，$P(\text{患病}\mid+_1)=\frac{\frac{1}{1000}\times\frac{99}{100}}{\frac{1}{1000}\times\frac{99}{100}+\frac{999}{1000}\times\frac{1}{100}}=\frac{99}{99+999}=\frac{99}{1098}=\frac{11}{122}$。第二次检测在给定患病状态下与第一次独立，故将 $\frac{11}{122}$ 作为新的先验再更新：$P(\text{患病}\mid+_1,+_2)=\frac{\frac{11}{122}\times\frac{99}{100}}{\frac{11}{122}\times\frac{99}{100}+\frac{111}{122}\times\frac{1}{100}}=\frac{1089}{1089+111}=\frac{1089}{1200}=\frac{363}{400}$。对比:单次阳性后为 $\frac{11}{122}$，两次后为 $\frac{363}{400}$。

修订说明：删除解答/场景所有小数，用精确分数比较

## draft-c51-04

状态：ELIGIBLE_FOR_USER_REVIEW_WITH_CORRECTIONS

题目：设一枚硬币正面朝上的概率为 $\theta$，先验取 $\theta\sim U(0,1)$。抛 $10$ 次观察到 $7$ 次正面。求 $\theta$ 的后验密度与后验均值。

答案：后验密度 $f(\theta)=1320\,\theta^7(1-\theta)^3$($0<\theta<1$),即 $\mathrm{Beta}(8,4)$;后验均值 $\frac23$。 支撑区间外密度为$0$。

解答：似然为 $L(\theta)=\binom{10}{7}\theta^7(1-\theta)^3\propto\theta^7(1-\theta)^3$，先验密度在 $(0,1)$ 上为常数 $1$，故后验密度 $\propto\theta^{8-1}(1-\theta)^{4-1}$，即 $\theta\mid\text{data}\sim\mathrm{Beta}(8,4)$。归一化常数 $\frac{\Gamma(12)}{\Gamma(8)\Gamma(4)}=\frac{11!}{7!\times3!}=1320$，故后验密度 $f(\theta)=1320\,\theta^7(1-\theta)^3$，$0<\theta<1$。后验均值 $\frac{8}{8+4}=\frac23$。(后验均值介于先验均值 $\frac12$ 与频率 $\frac{7}{10}$ 之间,符合共轭更新的收缩性质。)

修订说明：补后验密度支撑区间外为0

## draft-c51-05

状态：ELIGIBLE_FOR_USER_REVIEW_WITH_CORRECTIONS

题目：设 $H$ 与 $\bar H$ 为互斥且穷尽的假设，观测 $D_1,D_2$ 在给定 $H$(及给定 $\bar H$)下条件独立。假设$0<P(H)<1$，且$P(D_i\mid H)>0$、$P(D_i\mid\bar H)>0$（$i=1,2$），以保证条件概率及有限优势比有定义。证明后验优势比可写成先验优势比与两个似然比的乘积，并说明更新顺序不影响最终后验；再用两次独立阳性检测的数据($P(H)=\frac{1}{1000}$，灵敏度与误报率均为 $\frac{99}{100}$ 与 $\frac{1}{100}$)验证所得后验为 $\frac{363}{400}$。

答案：证明见解法(乘积形式);验证:$P(H\mid +_1,+_2)=\frac{363}{400}$。

解答：由贝叶斯公式与条件独立性，$\frac{P(H\mid D_1,D_2)}{P(\bar H\mid D_1,D_2)}=\frac{P(H)}{P(\bar H)}\cdot\frac{P(D_1\mid H)}{P(D_1\mid\bar H)}\cdot\frac{P(D_2\mid H)}{P(D_2\mid\bar H)}$。乘积形式对 $D_1,D_2$ 对称，故更新顺序不影响最终后验优势比。验证:先验优势比 $\frac{P(H)}{P(\bar H)}=\frac{1}{999}$;每次阳性的似然比 $\frac{99/100}{1/100}=99$。两次阳性后，后验优势比 $=\frac{1}{999}\times99^2=\frac{9801}{999}=\frac{363}{37}$，故后验概率 $=\frac{363}{363+37}=\frac{363}{400}$，与逐次更新结果一致。

修订说明：补非退化先验及正似然条件，避免除零或未定义条件概率
