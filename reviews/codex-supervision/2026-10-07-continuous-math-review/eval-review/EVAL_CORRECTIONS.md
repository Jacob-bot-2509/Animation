# 评测稿独立复核与修订

范围：291条新提交，修订78条（正文、必要条件或场景文字）。完整评测文件300条中，前轮9条修订逐字节保留。原件及父版本均冻结归档。

数学与场景文字合格仅指本候选版本；训练评测结构隔离仍未完成，实际渲染未验证，未自动准入。

## eval-calc-003-s1

补齐题干要求的级数表示与极限相等证明

题目：证明极限 $\displaystyle\lim_{n\to\infty}\left(1+\frac{1}{n}\right)^n$ 存在（记为 $e$），并说明它与级数 $\displaystyle\sum_{k=0}^{\infty}\frac{1}{k!}$ 的联系。

过程：记 $a_n=\left(1+\dfrac{1}{n}\right)^n$。由二项式展开 $a_n=\sum_{k=0}^{n}\binom{n}{k}\dfrac{1}{n^k}=\sum_{k=0}^{n}\dfrac{1}{k!}\cdot\dfrac{n(n-1)\cdots(n-k+1)}{n^k}$。比较 $a_n$ 与 $a_{n+1}$ 的展开式，第 $k$ 项因子 $\dfrac{n(n-1)\cdots(n-k+1)}{n^k}\le\dfrac{(n+1)n\cdots(n-k+2)}{(n+1)^k}$，且 $a_{n+1}$ 还多一项，故 $a_{n+1}>a_n$，数列递增。又有 $a_n\le\sum_{k=0}^{n}\dfrac{1}{k!}\le 1+1+\dfrac{1}{2}+\dfrac{1}{4}+\cdots+\dfrac{1}{2^{n-1}}<3$，故有上界。由单调有界准则，$\lim a_n$ 存在，记为 $e$。令$E=\sum_{k=0}^{\infty}1/k!$。因$k!\ge2^{k-1}$（$k\ge1$），该正项级数收敛。二项式展开给出$a_n=\sum_{k=0}^{n}c_{k,n}/k!$，其中$c_{0,n}=c_{1,n}=1$，$c_{k,n}=\prod_{j=0}^{k-1}(1-j/n)\in[0,1]$。对固定$m$，当$n\ge m$时有$\sum_{k=0}^{m}c_{k,n}/k!\le a_n\le E$；令$n\to\infty$再令$m\to\infty$，得$\lim a_n=E$。

答案：极限存在且等于 $e=\sum_{k=0}^{\infty}\frac{1}{k!}$

修订后：数学内容及场景文字合格。

## eval-calc-003-s2

指数形式的e须与题干指定级数定义连接

题目：证明极限 $\displaystyle\lim_{n\to\infty}\left(1+\frac{1}{n}\right)^n$ 存在（记为 $e$），并说明它与级数 $\displaystyle\sum_{k=0}^{\infty}\frac{1}{k!}$ 的联系。

过程：设 $n\ln\left(1+\dfrac{1}{n}\right)=\dfrac{\ln(1+x)}{x}$，其中 $x=\dfrac{1}{n}\to 0^+$。洛必达：$\lim_{x\to 0^+}\dfrac{\ln(1+x)}{x}=\lim_{x\to 0^+}\dfrac{1}{1+x}=1$。故 $\lim n\ln(1+1/n)=1$，原极限 $=e^1$。注意此解法默认 $e$ 已由其他途径定义，适合作为验证。为连接级数定义，令$E(x)=\sum_{k=0}^{\infty}x^k/k!$；比值判别及幂级数理论保证全实轴收敛且可逐项求导，故$E^{\prime}=E$、$E(0)=1$。于是$(e^{-x}E(x))^{\prime}=0$，$E(x)=e^x$，特别地$e=\sum_{k=0}^{\infty}1/k!$。

答案：极限存在且等于 $e=\sum_{k=0}^{\infty}\frac{1}{k!}$

修订后：数学内容及场景文字合格。

## eval-calc-006-s1

补齐反函数及其值域、回代验证

题目：求函数 $y=\ln(x+\sqrt{x^2+a^2})$（$a>0$）的导数，并说明其反函数。

过程：$y'=\dfrac{1+\dfrac{x}{\sqrt{x^2+a^2}}}{x+\sqrt{x^2+a^2}}=\dfrac{\sqrt{x^2+a^2}+x}{\sqrt{x^2+a^2}\cdot(x+\sqrt{x^2+a^2})}=\dfrac{1}{\sqrt{x^2+a^2}}$。反解$e^y=x+\sqrt{x^2+a^2}$，得$x=(e^{2y}-a^2)/(2e^y)=(e^y-a^2e^{-y})/2=a\sinh(y-\ln a)$。代回时$\sqrt{x^2+a^2}=(e^y+a^2e^{-y})/2$，故没有平方引入的赘解。原函数严格递增，$x\to\pm\infty$时$y\to\pm\infty$，所以该反函数定义于$\mathbb R$。

答案：$y'=\dfrac{1}{\sqrt{x^2+a^2}}$；反函数为 $x=a\sinh(y-\ln a)=\dfrac{e^y-a^2e^{-y}}{2}$

修订后：数学内容及场景文字合格。

## eval-calc-006-s2

补齐反函数及其值域、回代验证；arsinh对应双曲线的坐标符号应与代换一致

题目：求函数 $y=\ln(x+\sqrt{x^2+a^2})$（$a>0$）的导数，并说明其反函数。

过程：令 $x=a\sinh t$，则 $x+\sqrt{x^2+a^2}=a(\sinh t+\cosh t)=a e^t$，故 $y=\ln(ae^t)=t+\ln a$，即 $y=\operatorname{arsinh}\dfrac{x}{a}+\ln a$。由反双曲函数求导公式 $(\operatorname{arsinh} u)'=\dfrac{u'}{\sqrt{1+u^2}}$，得 $y'=\dfrac{1/a}{\sqrt{1+x^2/a^2}}=\dfrac{1}{\sqrt{x^2+a^2}}$。反解$e^y=x+\sqrt{x^2+a^2}$，得$x=(e^{2y}-a^2)/(2e^y)=(e^y-a^2e^{-y})/2=a\sinh(y-\ln a)$。代回时$\sqrt{x^2+a^2}=(e^y+a^2e^{-y})/2$，故没有平方引入的赘解。原函数严格递增，$x\to\pm\infty$时$y\to\pm\infty$，所以该反函数定义于$\mathbb R$。

答案：$y'=\dfrac{1}{\sqrt{x^2+a^2}}$；反函数为 $x=a\sinh(y-\ln a)=\dfrac{e^y-a^2e^{-y}}{2}$

修订后：数学内容及场景文字合格。

## eval-calc-007-s3

包络法须真正推导二阶导，y的二阶导不是切线转角速率

题目：设星形线参数方程为 $x=a\cos^3 t$，$y=a\sin^3 t$（$a>0$，$0\le t\le 2\pi$），求 $\dfrac{dy}{dx}$ 与 $\dfrac{d^2y}{dx^2}$。

过程：星形线的切线族为$F(x,y,t)=x\sin t+y\cos t-a\sin t\cos t=0$；包络条件$F_t=0$给出$x=a\cos^3t,\ y=a\sin^3t$。在$\sin t\cos t\ne0$时，沿包络对$F=0$求导，因$F_t=0$，得$\sin t+\cos t\,y^{\prime}=0$，故$y^{\prime}=-\tan t$。再由$x^{\prime}=-3a\cos^2t\sin t$，得$y^{\prime\prime}=(-\sec^2t)/x^{\prime}=1/(3a\cos^4t\sin t)$。切线的轴截距为$a\cos t,a\sin t$，两截距点间距为$a$。尖点$t=k\pi/2$需另判：$t=k\pi$处切线水平，$t=\pi/2+k\pi$处切线竖直；尖点不套用上述二阶导公式。

答案：$\dfrac{dy}{dx}=-\tan t$；$\dfrac{d^2y}{dx^2}=\dfrac{1}{3a\cos^4 t\sin t}$（两式仅在光滑分支上成立，即 $\sin t\cos t\ne 0$；在尖点 $t=k\dfrac{\pi}{2}$ 处切线竖直或水平、二阶导不存在，需单独作单侧讨论）

修订后：数学内容及场景文字合格。

## eval-calc-011-s2

级数项对应幂函数积分，不能声称等高矩形条带面积恰等于该项

题目：用多种方法求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\cdot 2^n}$ 的和。

过程：由 $\dfrac{1}{n\cdot 2^n}=\displaystyle\int_0^{1/2}x^{n-1}\,dx$（把 $\dfrac{1}{2^n}$ 看作幂的积分），故 $S=\displaystyle\sum_{n=1}^{\infty}\int_0^{1/2}x^{n-1}dx=\int_0^{1/2}\sum_{n=1}^{\infty}x^{n-1}dx=\int_0^{1/2}\dfrac{dx}{1-x}=\left[-\ln(1-x)\right]_0^{1/2}=\ln 2$（求和与积分可交换由正项级数单调收敛保证）。

答案：$\ln 2$

修订后：数学内容及场景文字合格。

## eval-calc-012-s3

原拼接没有构造证明，改用明确的角平分线长度关系

题目：求 $\tan 15^\circ$ 的精确值。

过程：取直角三角形$ABC$，$\angle B=\pi/2$，$AB=\sqrt3,\ BC=1,\ AC=2$，则$\angle A=\pi/6$。其角平分线$AD$与$BC$交于$D$。由角平分线定理$BD/DC=AB/AC=\sqrt3/2$及$BD+DC=1$，得$BD=\sqrt3/(2+\sqrt3)$。在直角三角形$ABD$中$\angle BAD=\pi/12$，故$\tan(\pi/12)=BD/AB=1/(2+\sqrt3)=2-\sqrt3$。再由余角关系$\tan(5\pi/12)=1/\tan(\pi/12)=2+\sqrt3$。

答案：$2-\sqrt{3}$

修订后：数学内容及场景文字合格。

## eval-calc-020-s1

p=1的对数来自积分，不是b的零次幂

题目：讨论反常积分 $\displaystyle\int_1^{+\infty}\frac{dx}{x^p}$（$p>0$）的敛散性，并求其收敛时的值。

过程：当 $p\ne 1$ 时，$\displaystyle\int_1^b x^{-p}dx=\left[\dfrac{x^{1-p}}{1-p}\right]_1^b=\dfrac{b^{1-p}-1}{1-p}$。若 $p>1$，则 $1-p<0$，$b^{1-p}\to 0$，积分为 $\dfrac{0-1}{1-p}=\dfrac{1}{p-1}$，收敛；若 $0<p<1$，则 $b^{1-p}\to+\infty$，发散。当 $p=1$ 时 $\displaystyle\int_1^b\dfrac{dx}{x}=\ln b\to+\infty$，发散。综上，$p>1$ 收敛于 $\dfrac{1}{p-1}$，$0<p\le 1$ 发散。

答案：$p>1$ 时收敛于 $\dfrac{1}{p-1}$；$0<p\le 1$ 时发散

修订后：数学内容及场景文字合格。

## eval-calc-020-s2

积分判别只判敛散，补齐收敛时的精确值

题目：讨论反常积分 $\displaystyle\int_1^{+\infty}\frac{dx}{x^p}$（$p>0$）的敛散性，并求其收敛时的值。

过程：函数 $f(x)=x^{-p}$ 在 $[1,+\infty)$ 上非负递减，由积分判别法，$\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{n^p}$ 与 $\displaystyle\int_1^{+\infty}\dfrac{dx}{x^p}$ 同敛散，故 $p>1$ 收敛、$p\le 1$ 发散——积分与级数两个世界互相印证。收敛时再直接计算：$\int_1^b x^{-p}dx=(b^{1-p}-1)/(1-p)$（$p\ne1$）；当$p>1$，$b^{1-p}\to0$，所得值为$1/(p-1)$；$p=1$时积分为$\ln b\to\infty$。

答案：$p>1$ 时收敛于 $\dfrac{1}{p-1}$；$0<p\le 1$ 时发散

修订后：数学内容及场景文字合格。

## eval-calc-020-s3

把局部数值估计替换为覆盖所有p的严格上下界

题目：讨论反常积分 $\displaystyle\int_1^{+\infty}\frac{dx}{x^p}$（$p>0$）的敛散性，并求其收敛时的值。

过程：对$k\ge0$，在$[2^k,2^{k+1}]$上单调性给出$2^{-p(k+1)}\le x^{-p}\le2^{-pk}$，故$2^{-p}2^{(1-p)k}\le\int_{2^k}^{2^{k+1}}x^{-p}dx\le2^{(1-p)k}$。当$p>1$，右侧按公比$2^{1-p}<1$构成收敛几何级数；当$0<p\le1$，各块的下界至少为$2^{-p}>0$，总面积发散。求收敛值时令$x=e^t$，则$\int_1^\infty x^{-p}dx=\int_0^\infty e^{-(p-1)t}dt=1/(p-1)$（$p>1$）。

答案：$p>1$ 时收敛于 $\dfrac{1}{p-1}$；$0<p\le 1$ 时发散

修订后：数学内容及场景文字合格。

## eval-calc-021-s1

错位相减前补齐收敛依据

题目：求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n}{2^n}$ 的和。

过程：写 $S=\dfrac{1}{2}+\dfrac{2}{4}+\dfrac{3}{8}+\dfrac{4}{16}+\cdots$，则 $\dfrac{S}{2}=\dfrac{1}{4}+\dfrac{2}{8}+\dfrac{3}{16}+\cdots$。两式相减：$S-\dfrac{S}{2}=\dfrac{1}{2}+\left(\dfrac{2}{4}-\dfrac{1}{4}\right)+\left(\dfrac{3}{8}-\dfrac{2}{8}\right)+\left(\dfrac{4}{16}-\dfrac{3}{16}\right)+\cdots=\dfrac{1}{2}+\dfrac{1}{4}+\dfrac{1}{8}+\dfrac{1}{16}+\cdots=1$（几何级数）。故 $\dfrac{S}{2}=1$，$S=2$。上述无限级数运算的依据为$a_n=n/2^n>0$且$a_{n+1}/a_n=(n+1)/(2n)\to1/2<1$，故绝对收敛；也可直接验证有限和$\sum_{n=1}^N n/2^n=2-(N+2)/2^N$后取极限。

答案：$2$

修订后：数学内容及场景文字合格。

## eval-calc-022-s1

场景把一个单项误写成求和的值，补Σ

题目：求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n^2}{2^n}$ 的和。

过程：由 $\displaystyle\sum_{n=1}^{\infty}x^n=\dfrac{x}{1-x}$ 逐项求导两次：先得 $\displaystyle\sum_{n=1}^{\infty}nx^{n-1}=\dfrac{1}{(1-x)^2}$，再得 $\displaystyle\sum_{n=1}^{\infty}n(n-1)x^{n-2}=\dfrac{2}{(1-x)^3}$。于是 $\displaystyle\sum_{n=1}^{\infty}n^2x^n=\sum_{n=1}^{\infty}n(n-1)x^n+\sum_{n=1}^{\infty}nx^n=\dfrac{2x^2}{(1-x)^3}+\dfrac{x}{(1-x)^2}=\dfrac{x(1+x)}{(1-x)^3}$。取 $x=\dfrac{1}{2}$，得 $S=\dfrac{(1/2)(3/2)}{(1/2)^3}=6$。

答案：$6$

修订后：数学内容及场景文字合格。

## eval-calc-022-s2

错位相减前补齐绝对收敛依据及有限和复验

题目：求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n^2}{2^n}$ 的和。

过程：记 $A=\displaystyle\sum_{n=1}^{\infty}\dfrac{n}{2^n}=2$（eval-calc-021）、$B=\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{2^n}=1$。$\dfrac{S}{2}=\displaystyle\sum_{n=1}^{\infty}\dfrac{n^2}{2^{n+1}}=\sum_{m=2}^{\infty}\dfrac{(m-1)^2}{2^m}$，故 $S-\dfrac{S}{2}=\displaystyle\sum_{n=1}^{\infty}\dfrac{n^2-(n-1)^2}{2^n}=\sum_{n=1}^{\infty}\dfrac{2n-1}{2^n}=2A-B=2\cdot 2-1=3$。于是 $\dfrac{S}{2}=3$，$S=6$。因$a_{n+1}/a_n=(n+1)^2/(2n^2)\to1/2<1$，原级数绝对收敛，所用移项成立。有限和恒等式为$\sum_{n=1}^N n^2/2^n=6-(N^2+4N+6)/2^N$，取极限即得$6$。

答案：$6$

修订后：数学内容及场景文字合格。

## eval-calc-024-s1

用有限几何展开余项证明端点，而非只证明开区间

题目：求 $\arctan x$ 的幂级数展开式，并由此推导莱布尼茨级数 $\dfrac{\pi}{4}=1-\dfrac{1}{3}+\dfrac{1}{5}-\dfrac{1}{7}+\cdots$。

过程：由等比级数 $\dfrac{1}{1+t}=\displaystyle\sum_{n=0}^{\infty}(-1)^nt^{n}$（$|t|<1$），以 $t=x^2$ 代入得 $\dfrac{1}{1+x^2}=\displaystyle\sum_{n=0}^{\infty}(-1)^nx^{2n}$。逐项积分：$\arctan x=\displaystyle\int_0^x\dfrac{dt}{1+t^2}=\sum_{n=0}^{\infty}(-1)^n\int_0^xt^{2n}dt=\sum_{n=0}^{\infty}\dfrac{(-1)^nx^{2n+1}}{2n+1}$（$|x|<1$）。端点也可直接处理：$\frac1{1+t^2}=\sum_{k=0}^N(-1)^kt^{2k}+(-1)^{N+1}\frac{t^{2N+2}}{1+t^2}$。从$0$积分到$x\in[-1,1]$，余项满足$|R_N(x)|\le|x|^{2N+3}/(2N+3)\le1/(2N+3)\to0$，故展开在整个闭区间成立，$x=1$给出$\pi/4=\sum_{k=0}^\infty(-1)^k/(2k+1)$。

答案：$\arctan x=\displaystyle\sum_{n=0}^{\infty}\dfrac{(-1)^n x^{2n+1}}{2n+1}$（$|x|\le 1$）；$x=1$ 时即莱布尼茨级数

修订后：数学内容及场景文字合格。

## eval-calc-024-s2

补齐Abel定理所需的开区间展开依据

题目：求 $\arctan x$ 的幂级数展开式，并由此推导莱布尼茨级数 $\dfrac{\pi}{4}=1-\dfrac{1}{3}+\dfrac{1}{5}-\dfrac{1}{7}+\cdots$。

过程：$x=1$ 处级数 $\displaystyle\sum_{n=0}^{\infty}\dfrac{(-1)^n}{2n+1}$ 为交错级数（$a_n=\dfrac{1}{2n+1}\searrow 0$），由莱布尼茨判别法收敛；由 Abel 定理，和函数在 $x=1$ 左连续，故 $\arctan 1=\dfrac{\pi}{4}=1-\dfrac{1}{3}+\dfrac{1}{5}-\dfrac{1}{7}+\cdots$。$x=-1$ 同理（或由奇偶性）。开区间的展开来自几何级数$1/(1+t^2)=\sum_{k=0}^{\infty}(-1)^kt^{2k}$，在任意紧子区间$[-r,r]$（$r<1$）一致收敛，可从$0$逐项积分得到$\arctan x$的幂级数，再结合上述端点收敛及Abel定理。

答案：$\arctan x=\displaystyle\sum_{n=0}^{\infty}\dfrac{(-1)^n x^{2n+1}}{2n+1}$（$|x|\le 1$）；$x=1$ 时即莱布尼茨级数

修订后：数学内容及场景文字合格。

## eval-calc-024-s3

给出高阶导数界的明确公式和证明

题目：求 $\arctan x$ 的幂级数展开式，并由此推导莱布尼茨级数 $\dfrac{\pi}{4}=1-\dfrac{1}{3}+\dfrac{1}{5}-\dfrac{1}{7}+\cdots$。

过程：对 $f(x)=\arctan x$ 用带拉格朗日余项的麦克劳林公式：$f^{(n)}(0)$ 由递推 $f'(x)=\dfrac{1}{1+x^2}$ 逐阶求导给出。对 $\arctan$ 可归纳证明 $|f^{(m)}(t)|\le(m-1)!$（$m\ge 1$，对一切实数 $t$），于是余项 $|R_N(x)|=\dfrac{|f^{(N+1)}(\xi)|}{(N+1)!}|x|^{N+1}\le\dfrac{N!}{(N+1)!}\cdot 1=\dfrac{1}{N+1}\to 0$，对 $|x|\le 1$ 一致成立。故展开式在 $|x|\le 1$ 成立，端点处即莱布尼茨级数。所用导数界可由部分分式严格验证：对$m\ge1$，$f^{(m)}(t)=\frac{(-1)^{m-1}(m-1)!}{2i}[(t-i)^{-m}-(t+i)^{-m}]$，于是$|f^{(m)}(t)|\le(m-1)!(1+t^2)^{-m/2}\le(m-1)!$。同时$f^{(2k+1)}(0)=(-1)^k(2k)!$，$f^{(2k)}(0)=0$；泰勒余项界$1/(N+1)$确实趋于零。

答案：$\arctan x=\displaystyle\sum_{n=0}^{\infty}\dfrac{(-1)^n x^{2n+1}}{2n+1}$（$|x|\le 1$）；$x=1$ 时即莱布尼茨级数

修订后：数学内容及场景文字合格。

## eval-calc-025-s3

删除数值量级推断，使用Abel分部求和与精确下界

题目：讨论级数 $\displaystyle\sum_{n=2}^{\infty}\frac{(-1)^n}{\ln n}$ 的敛散性，若收敛，判断是绝对收敛还是条件收敛。

过程：令$a_n=1/\ln n$（$n\ge2$），则$a_n\downarrow0$。对任意$p\ge2$，令$B_j=\sum_{n=p}^j(-1)^n$，有$|B_j|\le1$。Abel分部求和给出$\sum_{n=p}^q(-1)^na_n=B_qa_q+\sum_{j=p}^{q-1}B_j(a_j-a_{j+1})$，故其绝对值不超过$a_q+\sum_{j=p}^{q-1}(a_j-a_{j+1})=a_p\to0$，由Cauchy准则交错级数收敛。绝对级数的有限和满足$\sum_{n=2}^N1/\ln n\ge(N-1)/\ln N\to\infty$，其中$\ln N/N\to0$由洛必达法则得到。因此是条件收敛。

答案：条件收敛

修订后：数学内容及场景文字合格。

## eval-calc-029-s2

弧长微元补第一象限和绝对值条件

题目：求星形线 $x^{2/3}+y^{2/3}=a^{2/3}$（$a>0$）的周长。

过程：由隐函数求导（eval-calc-007）$y'=-\left(\dfrac{y}{x}\right)^{1/3}$，故弧长微元 $ds=\sqrt{1+(y')^2}\,dx=\sqrt{1+(y/x)^{2/3}}\,dx=\sqrt{\dfrac{x^{2/3}+y^{2/3}}{x^{2/3}}}\,dx$。由星形线方程 $x^{2/3}+y^{2/3}=a^{2/3}$，得 $ds=a^{1/3}x^{-1/3}dx$。第一象限部分：$L_1=\displaystyle\int_0^a a^{1/3}x^{-1/3}dx=a^{1/3}\left[\dfrac{3}{2}x^{2/3}\right]_0^a=\dfrac{3a}{2}$，故 $L=4L_1=6a$。上述$x$积分限定在第一象限$0<x\le a$，其中$ds=a^{1/3}x^{-1/3}|dx|$；从$x=0$到$a$积分可写为$a^{1/3}\int_0^a x^{-1/3}dx=3a/2$，端点按反常积分收敛处理，再由四象限对称得$6a$。

答案：$6a$

修订后：数学内容及场景文字合格。

## eval-calc-030-s3

内外半径之间是圆环截面

题目：求由 $y=\sin x$（$0\le x\le\pi$）与 $x$ 轴围成的区域绕 $y$ 轴旋转所得旋转体的体积。

过程：绕 $y$ 轴时取水平圆盘：对 $0\le y\le 1$，水平线 $y$ 与区域相交于 $x=\arcsin y$（左）与 $x=\pi-\arcsin y$（右），圆盘外半径 $R=\pi-\arcsin y$、内半径 $r=\arcsin y$。$V=\pi\displaystyle\int_0^1\left[(\pi-\arcsin y)^2-(\arcsin y)^2\right]dy=\pi\int_0^1(\pi^2-2\pi\arcsin y)\,dy=\pi\left[\pi^2y-2\pi\int_0^1\arcsin y\,dy\right]$。其中 $\displaystyle\int_0^1\arcsin y\,dy=\left[y\arcsin y+\sqrt{1-y^2}\right]_0^1=\dfrac{\pi}{2}-1$。故 $V=\pi\left[\pi^2-2\pi\left(\dfrac{\pi}{2}-1\right)\right]=\pi\left[\pi^2-\pi^2+2\pi\right]=2\pi^2$。

答案：$2\pi^2$

修订后：数学内容及场景文字合格。

## eval-geom-001-s3

Lagrange驻点需证明是全局最小距离点

题目：求点 $P(1,2,-1)$ 到平面 $\pi:2x-y+2z=3$ 的距离。

过程：求 $f(x,y,z)=(x-1)^2+(y-2)^2+(z+1)^2$ 在约束 $2x-y+2z-3=0$ 下的最小值。由 $\nabla f=\lambda\nabla(2x-y+2z-3)$：$2(x-1)=2\lambda$，$2(y-2)=-\lambda$，$2(z+1)=2\lambda$，得 $x-1=\lambda$，$y-2=-\dfrac{\lambda}{2}$，$z+1=\lambda$。代入约束：$2(1+\lambda)-\left(2-\dfrac{\lambda}{2}\right)+2(\lambda-1)=3$，即 $\dfrac{9\lambda}{2}-2=3$，解得 $\lambda=\dfrac{10}{9}$。最近距离 $d=\sqrt{\lambda^2+\dfrac{\lambda^2}{4}+\lambda^2}=\dfrac{3}{2}|\lambda|=\dfrac{5}{3}$。在约束平面内，设垂足$Q=(19/9,13/9,1/9)$；$P-Q$与平面法向量平行，故对任意平面内$X$有$(P-Q)\cdot(X-Q)=0$。因此$|P-X|^2=|P-Q|^2+|X-Q|^2=25/9+|X-Q|^2\ge25/9$，等号只在$X=Q$取到，证明此驻点是唯一全局极小点。

答案：$\dfrac{5}{3}$

修订后：数学内容及场景文字合格。

## eval-geom-002-s3

第三解不能仅引用第二解排除相交

题目：判断两条直线 $l_1:\dfrac{x-1}{2}=\dfrac{y+1}{1}=\dfrac{z-2}{-1}$ 与 $l_2:\dfrac{x+1}{1}=\dfrac{y-2}{2}=\dfrac{z}{1}$ 的位置关系。

过程：两方向$d_1=(2,1,-1)$、$d_2=(1,2,1)$满足$d_1\times d_2=(3,-3,3)\ne0$，故不平行。两基点差$\Delta=(-2,3,-2)$与叉积的内积为$-21\ne0$；若相交，则$\Delta$必在$\operatorname{span}\{d_1,d_2\}$中，内积应为零，矛盾。因此两线不相交且不平行，是异面直线。

答案：异面直线

修订后：数学内容及场景文字合格。

## eval-geom-006-s1

非齐次解集是仿射直线，不是线性解空间

题目：讨论三个平面 $\pi_1:x+y+z=1$，$\pi_2:x-y+z=1$，$\pi_3:2x+2z=2$ 的位置关系，并求其公共部分。

过程：系数矩阵与增广矩阵行变换：$\begin{pmatrix}1&1&1&1\\1&-1&1&1\\2&0&2&2\end{pmatrix}\to\begin{pmatrix}1&1&1&1\\0&-2&0&0\\0&-2&0&0\end{pmatrix}\to\begin{pmatrix}1&1&1&1\\0&1&0&0\\0&0&0&0\end{pmatrix}$。秩 $\mathrm r(A)=\mathrm r(\bar A)=2<3$，无穷多解，解集（仿射直线）一维：$y=0$，$x+z=1$，即一条直线。

答案：三平面共线，交线为 $y=0,\ x+z=1$

修订后：数学内容及场景文字合格。

## eval-geom-007-s1

补齐截面法及两组退化边界

题目：指出方程 $4x^2-y^2+z^2=1$ 表示的二次曲面类型，并用截面法说明其形状。

过程：方程化为 $\dfrac{x^2}{1/4}+\dfrac{z^2}{1}-\dfrac{y^2}{1}=1$，形如 $\dfrac{x^2}{a^2}+\dfrac{z^2}{b^2}-\dfrac{y^2}{c^2}=1$（一个负号项），是单叶双曲面，对称轴为 $y$ 轴。截面$y=k$为$4x^2+z^2=1+k^2$，始终为椭圆。截面$z=k$为$4x^2-y^2=1-k^2$：$|k|<1$沿$x$开口，$|k|>1$沿$y$开口，$|k|=1$退化为$y=\pm2x$。截面$x=k$为$z^2-y^2=1-4k^2$：$|k|<1/2$沿$z$开口，$|k|>1/2$沿$y$开口，$|k|=1/2$退化为$z=\pm y$。由一个负平方和两个正平方组成的标准式且$y=k$截面始终非空，知为绕$y$轴的单叶双曲面。

答案：单叶双曲面（以 $y$ 轴为对称轴）

修订后：数学内容及场景文字合格。

## eval-geom-007-s2

补齐截面法及两组退化边界

题目：指出方程 $4x^2-y^2+z^2=1$ 表示的二次曲面类型，并用截面法说明其形状。

过程：截面$y=k$为$4x^2+z^2=1+k^2$，始终为椭圆。截面$z=k$为$4x^2-y^2=1-k^2$：$|k|<1$沿$x$开口，$|k|>1$沿$y$开口，$|k|=1$退化为$y=\pm2x$。截面$x=k$为$z^2-y^2=1-4k^2$：$|k|<1/2$沿$z$开口，$|k|>1/2$沿$y$开口，$|k|=1/2$退化为$z=\pm y$。由一个负平方和两个正平方组成的标准式且$y=k$截面始终非空，知为绕$y$轴的单叶双曲面。

答案：单叶双曲面（以 $y$ 轴为对称轴）

修订后：数学内容及场景文字合格。

## eval-geom-007-s3

补齐截面法及两组退化边界

题目：指出方程 $4x^2-y^2+z^2=1$ 表示的二次曲面类型，并用截面法说明其形状。

过程：构造两族直线（参数 $s$）：$\begin{cases}x=\dfrac{\cos\theta+s\sin\theta}{2}\\y=s\\z=\sin\theta-s\cos\theta\end{cases}$ 与 $\begin{cases}x=\dfrac{\cos\theta-s\sin\theta}{2}\\y=s\\z=\sin\theta+s\cos\theta\end{cases}$。代入验证：$4x^2+z^2-y^2=(\cos\theta\pm s\sin\theta)^2+(\sin\theta\mp s\cos\theta)^2-s^2=\cos^2\theta+\sin^2\theta\pm 2s\sin\theta\cos\theta\mp 2s\sin\theta\cos\theta+s^2(\sin^2\theta+\cos^2\theta)-s^2=1$，整条直线都落在曲面上。直母线族的存在是单叶双曲面的特征性质（双叶双曲面无此性质）。截面$y=k$为$4x^2+z^2=1+k^2$，始终为椭圆。截面$z=k$为$4x^2-y^2=1-k^2$：$|k|<1$沿$x$开口，$|k|>1$沿$y$开口，$|k|=1$退化为$y=\pm2x$。截面$x=k$为$z^2-y^2=1-4k^2$：$|k|<1/2$沿$z$开口，$|k|>1/2$沿$y$开口，$|k|=1/2$退化为$z=\pm y$。由一个负平方和两个正平方组成的标准式且$y=k$截面始终非空，知为绕$y$轴的单叶双曲面。

答案：单叶双曲面（以 $y$ 轴为对称轴）

修订后：数学内容及场景文字合格。

## eval-geom-008-s3

仅凭几个典型截面不足以严格分类，补两连通分支表达式

题目：判断二次曲面 $2x^2+y^2-z^2+4xy=1$ 的类型。

过程：用 $z=0$ 截：$2x^2+4xy+y^2=1$，配方为 $2(x+y)^2-y^2=1$，是双曲线；用 $y=0$ 截：$2x^2-z^2=1$，是双曲线；用 $x+y=0$（即 $x=-y$）截：$-y^2-z^2=1$ 无实解——该平面与曲面不相交。三个截面说明曲面在 $z$ 方向与 $x+y$ 方向均为双曲型、且存在与曲面完全不相交的平面（双叶分离的特征）。严格分类令$u=x+y,\ v=y,\ w=z$，这是可逆线性替换。原式化为$2u^2-v^2-w^2=1$，故$u=\pm\sqrt{(1+v^2+w^2)/2}$。两个符号分支分别是定义于$\mathbb R^2$的连续图像，各自连通，且由$|u|\ge1/\sqrt2$隔开，故恰为双叶双曲面。

答案：双叶双曲面

修订后：数学内容及场景文字合格。

## eval-geom-010-s1

补题干要求的两族直母线

题目：说明曲面 $z=xy$ 的类型，并验证它是直纹面。

过程：作正交变换 $u=\dfrac{x+y}{\sqrt{2}}$、$v=\dfrac{x-y}{\sqrt{2}}$，则 $x=\dfrac{u+v}{\sqrt{2}}$、$y=\dfrac{u-v}{\sqrt{2}}$，$xy=\dfrac{u^2-v^2}{2}$。曲面方程化为 $z=\dfrac{u^2}{2}-\dfrac{v^2}{2}$，即 $2z=u^2-v^2$，是双曲抛物面（马鞍面）。两族直母线显式写成$(x,y,z)=(t,c,ct)$和$(c,t,ct)$（$c,t\in\mathbb R$）。每一点$(x_0,y_0,x_0y_0)$都同时落在$c=y_0$的第一族及$c=x_0$的第二族上。

答案：双曲抛物面（马鞍面），直纹面

修订后：数学内容及场景文字合格。

## eval-geom-010-s3

一般竖直截面并非直线，限制为两个坐标方向

题目：说明曲面 $z=xy$ 的类型，并验证它是直纹面。

过程：用 $y=k$ 截：$z=kx$，对任意 $k$ 都是直线（上述两个坐标方向的竖直截面均为直线，直纹性的又一体现）；用 $z=k$ 截：$xy=k$，等轴双曲线（$k\ne 0$）或两坐标轴（$k=0$）；若要抛物线截面，取斜截面 $x=y$（得 $z=x^2$）与 $x=-y$（得 $z=-x^2$）。直线截面与双曲线截面正是双曲抛物面的截面特征。

答案：双曲抛物面（马鞍面），直纹面

修订后：数学内容及场景文字合格。

## eval-geom-011-s2

距离和弦长仅核对另一解，补独立推导交点

题目：求直线 $l:x=1+t,\ y=t,\ z=t$ 与球面 $x^2+y^2+z^2=4$ 的交点个数，并求出交点坐标。

过程：球心 $O(0,0,0)$ 到直线距离：直线上取点 $P_0(1,0,0)$、方向 $\vec s=(1,1,1)$，$\overrightarrow{P_0O}=(-1,0,0)$，叉积 $\overrightarrow{P_0O}\times\vec s=(0\cdot 1-0\cdot 1,\ 0\cdot 1-(-1)\cdot 1,\ (-1)\cdot 1-0\cdot 1)=(0,1,-1)$，模 $\sqrt{2}$，故 $d=\dfrac{\sqrt{2}}{\sqrt{3}}=\sqrt{\dfrac{2}{3}}<2$，直线与球面相交于两点。相交弦长 $=2\sqrt{4-\dfrac{2}{3}}=2\sqrt{\dfrac{10}{3}}$，与解法一中两参数差对应的长度 $|t_1-t_2|\cdot|\vec s|=\dfrac{2\sqrt{10}}{3}\cdot\sqrt{3}=2\sqrt{\dfrac{10}{3}}$ 一致。设直线点$r(t)=(1+t,t,t)$，沿方向$d=(1,1,1)$到球心的最近参数满足$r(t)\cdot d=1+3t=0$，故$t_0=-1/3$、垂足$Q=(2/3,-1/3,-1/3)$。由正交分解$|r(t)|^2=|Q|^2+|d|^2(t-t_0)^2=2/3+3(t+1/3)^2$。令其等于$4$，即$t=(-1\pm\sqrt{10})/3$，代入$r(t)$得到题中两个交点。

答案：两个交点：$\left(\dfrac{2+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3}\right)$ 与 $\left(\dfrac{2-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3}\right)$

修订后：数学内容及场景文字合格。

## eval-geom-012-s3

展开圆柱只能得到坡角，补Frenet框架导出曲率挠率

题目：求圆柱螺线 $x=a\cos t,\ y=a\sin t,\ z=bt$（$a,b>0$）的曲率与挠率。

过程：把圆柱面沿一条母线剪开展平，螺线变成一条直线，其与水平方向的夹角 $\alpha$ 满足 $\tan\alpha=\dfrac{b}{a}$（螺距 $2\pi b$ 与周长 $2\pi a$ 之比），故 $\cos^2\alpha=\dfrac{a^2}{a^2+b^2}$。螺线的曲率完全来自柱面弯曲：$\kappa=\dfrac{\cos^2\alpha}{a}=\dfrac{a}{a^2+b^2}$；挠率来自螺线"扭转"：$\tau=\dfrac{\sin\alpha\cos\alpha}{a}=\dfrac{b}{a^2+b^2}$。$\dfrac{\tau}{\kappa}=\dfrac{b}{a}$ 为常数，说明圆柱螺线是常曲率常挠率曲线。严格推导设$e_r=(\cos t,\sin t,0)$、$e_\theta=(-\sin t,\cos t,0)$、$e_z=(0,0,1)$，令$\tan\alpha=b/a$。单位切向量$T=\cos\alpha\,e_\theta+\sin\alpha\,e_z$，$ds/dt=a/\cos\alpha$。于是$dT/ds=-(\cos^2\alpha/a)e_r$，故$N=-e_r$、$\kappa=\cos^2\alpha/a$；$B=T\times N=\cos\alpha\,e_z-\sin\alpha\,e_\theta$，$dB/ds=(\sin\alpha\cos\alpha/a)e_r=-\tau N$，故$\tau=\sin\alpha\cos\alpha/a$。代$\cos\alpha=a/\sqrt{a^2+b^2}$、$\sin\alpha=b/\sqrt{a^2+b^2}$即得$\kappa=a/(a^2+b^2)$、$\tau=b/(a^2+b^2)$。

答案：曲率 $\kappa=\dfrac{a}{a^2+b^2}$，挠率 $\tau=\dfrac{b}{a^2+b^2}$

修订后：数学内容及场景文字合格。

## eval-geom-016-s3

把向量加法的补角和余弦定理的内角分开，避免符号误用

题目：已知 $|\vec a|=2$，$|\vec b|=3$，$\vec a$ 与 $\vec b$ 的夹角为 $60^\circ$，求 $|\vec a+\vec b|$、$|2\vec a-\vec b|$ 及 $\vec a+\vec b$ 与 $\vec a-\vec b$ 的夹角余弦。

过程：将$\vec a,\vec b$置于同一起点，夹角$\pi/3$。平行四边形对角线给出$|\vec a+\vec b|^2=4+9+2\cdot2\cdot3\cos(\pi/3)=19$。以$2\vec a,\vec b$两终点及原点构成三角形，原点内角为$\pi/3$，对边为$2\vec a-\vec b$，由余弦定理$|2\vec a-\vec b|^2=16+9-2\cdot4\cdot3\cos(\pi/3)=13$。另有$|\vec a-\vec b|^2=4+9-2\cdot2\cdot3\cos(\pi/3)=7$，两对角线的点积$(\vec a+\vec b)\cdot(\vec a-\vec b)=|\vec a|^2-|\vec b|^2=-5$，故夹角余弦为$-5/\sqrt{19\cdot7}=-5/\sqrt{133}$。

答案：$|\vec a+\vec b|=\sqrt{19}$，$|2\vec a-\vec b|=\sqrt{13}$，$\cos\theta=-\dfrac{5}{\sqrt{133}}$

修订后：数学内容及场景文字合格。

## eval-geom-017-s2

投影计算前补夹角余弦的独立求法

题目：已知 $\vec a=(1,2,2)$，$\vec b=(-2,1,2)$，求 $\vec a$ 与 $\vec b$ 的夹角余弦及 $\vec a$ 在 $\vec b$ 上的投影向量。

过程：投影长度 $|\vec a|\cos\theta=3\cdot\dfrac{4}{9}=\dfrac{4}{3}$，方向为 $\dfrac{\vec b}{|\vec b|}=\dfrac{1}{3}(-2,1,2)$，故投影向量 $=\dfrac{4}{3}\cdot\dfrac{1}{3}(-2,1,2)=\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)$。夹角也可由余弦定理独立确定：$|\vec a-\vec b|^2=|(3,1,0)|^2=10$，$|\vec a|=|\vec b|=3$，故$\cos\theta=(9+9-10)/(2\cdot3\cdot3)=4/9$。

答案：$\cos\theta=\dfrac{4}{9}$；投影向量 $\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)$

修订后：数学内容及场景文字合格。

## eval-geom-019-s3

回代只证包含，补交线描述的完备性

题目：求两平面 $\pi_1:x+y+z=1$ 与 $\pi_2:x+2y+3z=6$ 的交线方程。

过程：由解法一/二得 $(x,y,z)=(-4+t,5-2t,t)$。代入 $\pi_1$：$(-4+t)+(5-2t)+t=1$；代入 $\pi_2$：$(-4+t)+2(5-2t)+3t=-4+t+10-4t+3t=6$。两式恒成立，故确为交线。完备性：任取两平面的公共点，令$z=t$，两式相减得$y+2t=5$，所以$y=5-2t$；代回第一式得$x=t-4$。因此每个公共点都在所列参数线上，已得到完整交线。

答案：$\dfrac{x+4}{1}=\dfrac{y-5}{-2}=\dfrac{z}{1}$，即 $(x,y,z)=(-4+t,5-2t,t)$

修订后：数学内容及场景文字合格。

## eval-linalg-002-s3

消元只作用前三行，不能把末行也减成零行

题目：计算四阶行列式 $D=\begin{vmatrix}1&1&1&1\\1&2&1&1\\1&1&3&1\\1&1&1&4\end{vmatrix}$。

过程：第一、二、三行分别减第四行，第四行保持不变：$\begin{vmatrix}0&0&0&-3\\0&1&0&-3\\0&0&2&-3\\1&1&1&4\end{vmatrix}$，按第一列展开：$D=(-1)^{4+1}\cdot 1\cdot\begin{vmatrix}0&0&-3\\1&0&-3\\0&2&-3\end{vmatrix}=-\left[0-0+(-3)\begin{vmatrix}1&0\\0&2\end{vmatrix}\right]=-(-3\cdot 2)=6$。

答案：$6$

修订后：数学内容及场景文字合格。

## eval-linalg-004-s1

三阶例子没有证明题干的n阶一般情形

题目：计算 $n=3$ 时行列式 $D=\begin{vmatrix}a+b&a&a\\a&a+b&a\\a&a&a+b\end{vmatrix}$，并推广到 $n$ 阶。

过程：第二、三行分别减去第一行：$D=\begin{vmatrix}a+b&a&a\\-b&b&0\\-b&0&b\end{vmatrix}$。按第一行展开：$D=(a+b)\cdot b^2-a\cdot\begin{vmatrix}-b&0\\-b&b\end{vmatrix}+a\cdot\begin{vmatrix}-b&b\\-b&0\end{vmatrix}=(a+b)b^2-a(-b^2)+a(b^2)=b^2(a+b)+ab^2+ab^2=b^2(3a+b)$。对$n\ge2$，矩阵$M=bI+aJ$中$R_i\leftarrow R_i-R_1$（$i=2,\ldots,n$），第$i$行只在第1列有$-b$、第$i$列有$b$。再令$C_1\leftarrow C_1+C_2+\cdots+C_n$，第一列变为$(na+b,0,\ldots,0)^T$，余下主对角为$b$，所以$\det M=(na+b)b^{n-1}$。$n=1$时直接为$a+b$。全过程不除以$b$，包含$b=0$。

答案：$b^2(3a+b)$；$n$ 阶为 $b^{n-1}(na+b)$

修订后：数学内容及场景文字合格。

## eval-linalg-004-s2

场景仅标三阶谱，改为n阶谱和重数

题目：计算 $n=3$ 时行列式 $D=\begin{vmatrix}a+b&a&a\\a&a+b&a\\a&a&a+b\end{vmatrix}$，并推广到 $n$ 阶。

过程：该矩阵 $A=bI+aJ$，其中 $J$ 为全 1 矩阵。$J$ 的特征值为 $n,0,\dots,0$（$J$ 的秩为 1，且 $J(1,\dots,1)^T=n(1,\dots,1)^T$），故 $A$ 的特征值为 $b+na$（一重）与 $b$（$n-1$ 重）。行列式=特征值之积：$D=(b+3a)\cdot b\cdot b=b^2(3a+b)$（$n=3$）；一般地 $D_n=b^{n-1}(na+b)$。

答案：$b^2(3a+b)$；$n$ 阶为 $b^{n-1}(na+b)$

修订后：数学内容及场景文字合格。

## eval-linalg-004-s3

补一般n阶拆列计数

题目：计算 $n=3$ 时行列式 $D=\begin{vmatrix}a+b&a&a\\a&a+b&a\\a&a&a+b\end{vmatrix}$，并推广到 $n$ 阶。

过程：把每列拆成 $(a,a,a)^T+b\,e_i$（$e_i$ 为标准基向量）。由行列式关于列的多重线性：全取 $b\,e_i$ 的项为 $b^3\det I=b^3$；恰有一列取 $(a,a,a)^T$ 的项有 3 个，每个为 $ab^2\cdot\det(e_1,e_2,e_j$ 换为 $(1,1,1)^T)=ab^2$；有两列以上取 $(a,a,a)^T$ 的项行列式为 0（两列相同）。故 $D=b^3+3ab^2=b^2(3a+b)$。一般$n\ge2$同理：每列为$be_j+a\mathbf1$。多重线性展开中，选择两个及以上$a\mathbf1$列的项因重复列为零；全选$be_j$给$b^n$；恰选一个$a\mathbf1$列有$n$项，每项为$ab^{n-1}$（把该列的$\mathbf1=\sum_j e_j$展开，只有原列位置的$e_j$能留下非零行列式）。故总和为$b^n+nab^{n-1}=(na+b)b^{n-1}$。$n=1$直接为$a+b$。

答案：$b^2(3a+b)$；$n$ 阶为 $b^{n-1}(na+b)$

修订后：数学内容及场景文字合格。

## eval-linalg-006-s3

第三解不能只引用第二解，补独立坐标迭代

题目：设 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$，求 $A^n$（$n$ 为正整数）。

过程：该矩阵作用为$(x,y)\mapsto(x+y,y)$。归纳可得迭代$n\ge0$次为$(x+ny,y)$（$n=0$为恒等；再作用一次把$x+ny$变为$x+(n+1)y$）。因此$A^n=\begin{pmatrix}1&n\\0&1\end{pmatrix}$。

答案：$A^n=\begin{pmatrix}1&n\\0&1\end{pmatrix}$

修订后：数学内容及场景文字合格。

## eval-linalg-007-s1

明确整数次幂的n适用域

题目：设 $A=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}$，求 $A^n$。其中$n\in\mathbb Z_{\ge0}$；$n=0$时按$A^0=I$。

过程：$n=1$ 成立。设 $A^k=\begin{pmatrix}\cos k\theta&-\sin k\theta\\\sin k\theta&\cos k\theta\end{pmatrix}$，则 $A^{k+1}=A^kA$，其 $(1,1)$ 元为 $\cos k\theta\cos\theta-\sin k\theta\sin\theta=\cos(k+1)\theta$，$(1,2)$ 元为 $-\cos k\theta\sin\theta-\sin k\theta\cos\theta=-\sin(k+1)\theta$，其余两元同理。归纳成立。

答案：$A^n=\begin{pmatrix}\cos n\theta&-\sin n\theta\\\sin n\theta&\cos n\theta\end{pmatrix}$

修订后：数学内容及场景文字合格。

## eval-linalg-007-s2

明确整数次幂的n适用域

题目：设 $A=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}$，求 $A^n$。其中$n\in\mathbb Z_{\ge0}$；$n=0$时按$A^0=I$。

过程：特征方程 $(\cos\theta-\lambda)^2+\sin^2\theta=0$，即 $\lambda^2-2\lambda\cos\theta+1=0$，特征值 $\lambda=e^{\pm i\theta}$，对应特征向量 $(1,\mp i)^T$。取 $P=\begin{pmatrix}1&1\\-i&i\end{pmatrix}$，$P^{-1}=\dfrac{1}{2}\begin{pmatrix}1&i\\1&-i\end{pmatrix}$，则 $A=P\begin{pmatrix}e^{i\theta}&0\\0&e^{-i\theta}\end{pmatrix}P^{-1}$。故 $A^n=P\begin{pmatrix}e^{in\theta}&0\\0&e^{-in\theta}\end{pmatrix}P^{-1}=\dfrac{1}{2}\begin{pmatrix}e^{in\theta}+e^{-in\theta}&i(e^{in\theta}-e^{-in\theta})\\-i(e^{in\theta}-e^{-in\theta})&e^{in\theta}+e^{-in\theta}\end{pmatrix}=\begin{pmatrix}\cos n\theta&-\sin n\theta\\\sin n\theta&\cos n\theta\end{pmatrix}$（用欧拉公式 $e^{\pm in\theta}=\cos n\theta\pm i\sin n\theta$ 化简）。

答案：$A^n=\begin{pmatrix}\cos n\theta&-\sin n\theta\\\sin n\theta&\cos n\theta\end{pmatrix}$

修订后：数学内容及场景文字合格。

## eval-linalg-007-s3

明确整数次幂的n适用域

题目：设 $A=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}$，求 $A^n$。其中$n\in\mathbb Z_{\ge0}$；$n=0$时按$A^0=I$。

过程：旋转矩阵 $A$ 与复数乘法 $z\mapsto e^{i\theta}z$ 一一对应（$(x,y)\mapsto(x\cos\theta-y\sin\theta,\ x\sin\theta+y\cos\theta)$ 正是 $e^{i\theta}(x+iy)$ 的实虚部）。旋转的复合即角度相加：$(e^{i\theta})^n=e^{in\theta}$，对应 $A^n=$ 旋转 $n\theta$ 角的矩阵。

答案：$A^n=\begin{pmatrix}\cos n\theta&-\sin n\theta\\\sin n\theta&\cos n\theta\end{pmatrix}$

修订后：数学内容及场景文字合格。

## eval-linalg-008-s3

面积非负，负号表示定向而非面积

题目：设 $A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$，求 $\det A$、$A$ 的秩与 $A^{-1}$。

过程：$\det A=-2\ne 0$ 说明两行（列）线性无关，$\operatorname{rank}A=2$。验证逆矩阵：$AA^{-1}=\begin{pmatrix}1&2\\3&4\end{pmatrix}\begin{pmatrix}-2&1\\\frac{3}{2}&-\frac{1}{2}\end{pmatrix}=\begin{pmatrix}-2+3&1-1\\-6+6&3-2\end{pmatrix}=\begin{pmatrix}1&0\\0&1\end{pmatrix}$。

答案：$\det A=-2$；秩为 $2$；$A^{-1}=\begin{pmatrix}-2&1\\\frac{3}{2}&-\frac{1}{2}\end{pmatrix}$

修订后：数学内容及场景文字合格。

## eval-linalg-009-s2

Laplace展开与题干指定的分块方法建立对应

题目：用分块方法计算 $M=\begin{pmatrix}2&1&1\\1&2&1\\0&0&3\end{pmatrix}$ 的行列式。

过程：按第三行展开：$\det M=(-1)^{3+3}\cdot 3\cdot\begin{vmatrix}2&1\\1&2\end{vmatrix}=3\cdot 3=9$（第三行仅第 3 个元素非零）。这正是分块上三角公式：取左上$2\times2$块$B=\begin{pmatrix}2&1\\1&2\end{pmatrix}$、右下块$C=(3)$，左下为零块，则$\det M=\det B\det C=3\cdot3=9$。

答案：$9$

修订后：数学内容及场景文字合格。

## eval-linalg-011-s1

非齐次解集应为二维仿射平面

题目：讨论含参数线性方程组 $\begin{cases}\lambda x+y+z=1\\x+\lambda y+z=\lambda\\x+y+\lambda z=\lambda^2\end{cases}$ 的解的情况。

过程：系数行列式 $D=\begin{vmatrix}\lambda&1&1\\1&\lambda&1\\1&1&\lambda\end{vmatrix}$。该矩阵 $=(\lambda-1)I+J$（$J$ 全 1 矩阵），特征值为 $(\lambda-1)+3=\lambda+2$ 与 $\lambda-1$（二重），故 $D=(\lambda+2)(\lambda-1)^2$。当 $\lambda\ne 1,-2$ 时 $D\ne 0$，由 Cramer 法则有唯一解。当 $\lambda=1$：三个方程均为 $x+y+z=1$，无穷多解（解集为二维仿射平面）。当 $\lambda=-2$：三式相加得 $0\cdot(x+y+z)=1+(-2)+4=3$，即 $0=3$，矛盾，无解。

答案：$\lambda\ne 1$ 且 $\lambda\ne-2$ 时唯一解；$\lambda=1$ 时无穷多解；$\lambda=-2$ 时无解

修订后：数学内容及场景文字合格。

## eval-linalg-011-s2

去掉消元省略号，补精确最终行和分支条件

题目：讨论含参数线性方程组 $\begin{cases}\lambda x+y+z=1\\x+\lambda y+z=\lambda\\x+y+\lambda z=\lambda^2\end{cases}$ 的解的情况。

过程：交换第一、三行并消元得$\begin{pmatrix}1&1&\lambda&\lambda^2\\0&\lambda-1&1-\lambda&\lambda-\lambda^2\\0&1-\lambda&1-\lambda^2&1-\lambda^3\end{pmatrix}$。当$\lambda\ne1$，第二行除以$\lambda-1$为$(0,1,-1,-\lambda)$；第三行减去$(1-\lambda)$倍第二行，得到$(0,0,(1-\lambda)(\lambda+2),(1-\lambda)(\lambda+1)^2)$。因此$\lambda\ne1,-2$时三主元均非零，唯一解；$\lambda=-2$时末行为$0=3$，无解。$\lambda=1$时原三式均为$x+y+z=1$，解集为二维仿射平面，有无穷多解。

答案：$\lambda\ne 1$ 且 $\lambda\ne-2$ 时唯一解；$\lambda=1$ 时无穷多解；$\lambda=-2$ 时无解

修订后：数学内容及场景文字合格。

## eval-linalg-011-s3

几何断言补行列式和常数项相容性验证

题目：讨论含参数线性方程组 $\begin{cases}\lambda x+y+z=1\\x+\lambda y+z=\lambda\\x+y+\lambda z=\lambda^2\end{cases}$ 的解的情况。

过程：三个方程代表三个平面。$\lambda=1$ 时三平面重合（$x+y+z=1$）；$\lambda=-2$ 时三平面两两相交但三交线平行（法向量和为零向量导致矛盾）；其余情形三平面交于一点（唯一解）。代数依据：法向量矩阵为$(\lambda-1)I+J$，行列式$(\lambda-1)^2(\lambda+2)$，在$\lambda\ne1,-2$可逆，所以三平面唯一公共点；$\lambda=-2$时三式相加左侧为0、右侧为$1-2+4=3$，故无公共点，各法向量两两不成比例且叉积均沿$(1,1,1)$，三条两两交线平行；$\lambda=1$时代入即为同一个平面。

答案：$\lambda\ne 1$ 且 $\lambda\ne-2$ 时唯一解；$\lambda=1$ 时无穷多解；$\lambda=-2$ 时无解

修订后：数学内容及场景文字合格。

## eval-linalg-012-s2

行变换省略号改成完整秩与核空间证明

题目：求参数 $a$ 使齐次线性方程组 $\begin{cases}ax+y+z=0\\x+ay+z=0\\x+y+az=0\end{cases}$ 有非零解，并求各情形下的解空间。

过程：矩阵$(a-1)I+J$的行列式为$(a-1)^2(a+2)$，$a\ne1,-2$时秩3，只有零解。$a=1$时全1矩阵秩1，核为$x+y+z=0$，维数2。$a=-2$时每行和为0，秩不超过2；左上二阶子式为$4-1=3\ne0$，故秩恰2。第一式减第二式为$-3x+3y=0$，再代回得$z=x$，故核为$\operatorname{span}\{(1,1,1)^T\}$，维数1。

答案：$a=1$（解空间二维：$x+y+z=0$）或 $a=-2$（解空间一维：$x=y=z$）

修订后：数学内容及场景文字合格。

## eval-linalg-013-s3

超平面的维数不能代替所求基础解系构造

题目：求齐次线性方程组 $x_1+x_2+x_3+x_4=0$ 的基础解系与通解。

过程：方程 $x_1+x_2+x_3+x_4=0$ 是 $\mathbb R^4$ 中过原点的三维超平面（法向量 $(1,1,1,1)$）。基础解系即该超平面的一个基，通解是超平面上所有点。维数 $4-1=3$ 与基础解系含 3 个向量一致。具体取$\xi_1=(1,-1,0,0)^T,\xi_2=(1,0,-1,0)^T,\xi_3=(1,0,0,-1)^T$；它们都满足方程，且后三个分量直接保证线性无关。任意解$x$满足$x_1=-x_2-x_3-x_4$，所以$x=-x_2\xi_1-x_3\xi_2-x_4\xi_3$，给出完整通解。

答案：基础解系 $\xi_1=(1,-1,0,0)^T$，$\xi_2=(1,0,-1,0)^T$，$\xi_3=(1,0,0,-1)^T$；通解 $x=c_1\xi_1+c_2\xi_2+c_3\xi_3$

修订后：数学内容及场景文字合格。

## eval-linalg-015-s1

补题干要求的对角化运算

题目：求矩阵 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$ 的特征值与特征向量，并将其对角化。

过程：$|\lambda I-A|=\begin{vmatrix}\lambda-1&-2\\-2&\lambda-1\end{vmatrix}=(\lambda-1)^2-4=\lambda^2-2\lambda-3=(\lambda-3)(\lambda+1)$，$\lambda=3,-1$。$\lambda=3$：$(3I-A)v=0$，即 $\begin{pmatrix}2&-2\\-2&2\end{pmatrix}v=0$，$v=(1,1)^T$。$\lambda=-1$：$(-I-A)v=0$，即 $\begin{pmatrix}-2&-2\\-2&-2\end{pmatrix}v=0$，$v=(1,-1)^T$。取$P=((1,1)^T,(1,-1)^T)=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$，$\det P=-2\ne0$，逐列有$AP=P\operatorname{diag}(3,-1)$，故$P^{-1}AP=\operatorname{diag}(3,-1)$。

答案：特征值 $\lambda_1=3$、$\lambda_2=-1$；特征向量 $(1,1)^T$、$(1,-1)^T$；$P^{-1}AP=\begin{pmatrix}3&0\\0&-1\end{pmatrix}$，其中 $P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$

修订后：数学内容及场景文字合格。

## eval-linalg-015-s2

用明确正交替换替代省略的配方并给出对角化

题目：求矩阵 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$ 的特征值与特征向量，并将其对角化。

过程：令$u=(x+y)/\sqrt2,\ v=(x-y)/\sqrt2$，逆变换$x=(u+v)/\sqrt2,\ y=(u-v)/\sqrt2$。则$x^2+y^2=u^2+v^2$、$4xy=2u^2-2v^2$，所以$f=3u^2-v^2$。对应正交矩阵$Q=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$满足$Q^TAQ=\operatorname{diag}(3,-1)$，列向量分别是特征值$3,-1$的单位特征向量。等价地取$P=\sqrt2Q$，有$P^{-1}AP=\operatorname{diag}(3,-1)$。

答案：特征值 $\lambda_1=3$、$\lambda_2=-1$；特征向量 $(1,1)^T$、$(1,-1)^T$；$P^{-1}AP=\begin{pmatrix}3&0\\0&-1\end{pmatrix}$，其中 $P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$

修订后：数学内容及场景文字合格。

## eval-linalg-015-s3

Q行列式为负，不应称其为平面旋转

题目：求矩阵 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$ 的特征值与特征向量，并将其对角化。

过程：归一化特征向量 $q_1=\dfrac{1}{\sqrt2}(1,1)^T$、$q_2=\dfrac{1}{\sqrt2}(1,-1)^T$（自动正交），取 $Q=\dfrac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$（$Q$ 为正交矩阵，$Q^{-1}=Q^T$）。$Q^TAQ=\begin{pmatrix}3&0\\0&-1\end{pmatrix}$，验证：$Q^TAQ=\dfrac{1}{2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}\begin{pmatrix}1&2\\2&1\end{pmatrix}\begin{pmatrix}1&1\\1&-1\end{pmatrix}=\dfrac{1}{2}\begin{pmatrix}3&3\\-1&1\end{pmatrix}\begin{pmatrix}1&1\\1&-1\end{pmatrix}=\dfrac{1}{2}\begin{pmatrix}6&0\\0&-2\end{pmatrix}$。

答案：特征值 $\lambda_1=3$、$\lambda_2=-1$；特征向量 $(1,1)^T$、$(1,-1)^T$；$P^{-1}AP=\begin{pmatrix}3&0\\0&-1\end{pmatrix}$，其中 $P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$

修订后：数学内容及场景文字合格。

## eval-linalg-016-s1

特征值已求但漏验题干中的矩阵恒等式

题目：设 $A$ 为二阶方阵，已知 $\operatorname{tr}A=5$、$\det A=6$。求 $A$ 的特征值，并验证 $A^2-5A+6I=0$。

过程：特征多项式 $|\lambda I-A|=\lambda^2-(\operatorname{tr}A)\lambda+\det A=\lambda^2-5\lambda+6=(\lambda-2)(\lambda-3)$，特征值为 $2,3$。一般二阶矩阵满足Cayley–Hamilton定理，将$p(\lambda)=\lambda^2-5\lambda+6$代入即得$p(A)=A^2-5A+6I=0$；这对所有满足给定迹与行列式的矩阵成立。

答案：特征值为 $2$ 与 $3$；$A^2-5A+6I=0$ 成立

修订后：数学内容及场景文字合格。

## eval-linalg-017-s3

最小多项式判不可对角化之外须给出所求特征向量

题目：求矩阵 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 的特征值与特征向量，并判断其是否可对角化。

过程：$A-I=\begin{pmatrix}0&1\\0&0\end{pmatrix}\ne 0$，$(A-I)^2=0$，故最小多项式为 $m(\lambda)=(\lambda-1)^2$，含有重因子 $(\lambda-1)^2$。矩阵可对角化 $\iff$ 最小多项式无重根，故 $A$ 不可对角化；其若尔当标准形为单个二阶块 $J_2(1)=\begin{pmatrix}1&1\\0&1\end{pmatrix}$。求特征向量时，$Av=v$等价于$(A-I)(x,y)^T=(y,0)^T=0$，故所有非零特征向量为$t(1,0)^T$（$t\ne0$），仅一个特征方向。

答案：特征值 $\lambda=1$（二重），非零特征向量 $t(1,0)^T$（$t\ne 0$，特征空间连同零向量为一维）；不可对角化，若尔当标准形为 $\begin{pmatrix}1&1\\0&1\end{pmatrix}$

修订后：数学内容及场景文字合格。

## eval-linalg-020-s3

避免把非紧的平行直线对称为退化椭圆

题目：判断二次型 $f(x,y)=x^2-4xy+4y^2$ 的类型（正定/半正定/不定/负定）。

过程：$f=(x-2y)^2\ge0$，当且仅当$x=2y$时取0，并存在非零零向量$(2,1)$；故半正定而非正定。平方中的线性形式非零，矩阵为$(1,-2)^T(1,-2)$，秩1，正、负惯性指数分别为1、0。$f=k>0$的等值集恰为平行直线对$x-2y=\pm\sqrt k$，$k=0$为一条直线。

答案：半正定，秩为 1，正惯性指数 1、负惯性指数 0

修订后：数学内容及场景文字合格。

## eval-linalg-021-s2

系数判正定补可逆变量替换及反向必要性

题目：设 $a\in\mathbb R$ 为参数,求使二次型 $f(x,y,z)=2x^2+y^2+2z^2+2xy+2axz$ 正定的 $a$ 的取值范围。

过程：$2\left(x+\dfrac{y}{2}+\dfrac{az}{2}\right)^2=2x^2+\dfrac{y^2}{2}+\dfrac{a^2z^2}{2}+2xy+2axz+ayz$,故 $$f=2\left(x+\frac{y}{2}+\frac{az}{2}\right)^2+\left[\frac{y^2}{2}-ayz+\left(2-\frac{a^2}{2}\right)z^2\right]=2\left(x+\frac{y}{2}+\frac{az}{2}\right)^2+\frac{1}{2}(y-az)^2+(2-a^2)z^2.$$ 三项系数 $2,\ \dfrac{1}{2},\ 2-a^2$ 全正 $\iff 2-a^2>0\iff |a|<\sqrt{2}$,与解法一一致。变量替换$u=x+y/2+az/2,\ v=y-az,\ w=z$的矩阵为上三角且行列式1，故可逆。若$2-a^2\le0$，取非零向量$(x,y,z)=(-a,a,1)$，前两平方为零且$f=2-a^2\le0$，因此上述条件也是必要条件。

答案：$-\sqrt{2}<a<\sqrt{2}$

修订后：数学内容及场景文字合格。

## eval-linalg-023-s2

补题干所问复数域的完整分解

题目：分别在复数域与实数域上分解 $x^8-1$。

过程：$x^8-1=(x^4-1)(x^4+1)=(x^2-1)(x^2+1)(x^4+1)=(x-1)(x+1)(x^2+1)(x^4+1)$。再对 $x^4+1$ 作实分解（见解法三的恒等式）：$x^4+1=(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)$，合并得完整实不可约分解 $(x-1)(x+1)(x^2+1)(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)$。复数域中$e^{2\pi ik/8}$（$k=0,\ldots,7$）是八个互异根，首项系数1，故$x^8-1=\prod_{k=0}^7(x-e^{2\pi ik/8})$。三个实二次因子的判别式分别为$-4,-2,-2$，均负，所以所列实分解确为实不可约分解。

答案：复数域：$\displaystyle\prod_{k=0}^{7}\left(x-e^{2\pi ik/8}\right)$；实数域（完整实不可约分解）：$(x-1)(x+1)(x^2+1)(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)$

修订后：数学内容及场景文字合格。

## eval-linalg-025-s3

漏了除以x-1的余式这一问

题目：设 $f(x)=x^5+x+1$。求 $f(x)$ 除以 $x-1$ 的余式，以及除以 $x^2+1$ 的余式。

过程：设除以 $x^2+1$ 的余式为 $ax+b$，则 $f(x)=(x^2+1)q(x)+ax+b$。取 $x=i$ 与 $x=-i$：$f(i)=1+2i$（同解法一），$f(-i)=(-i)^5-i+1=-i-i+1=1-2i$。解 $\begin{cases}ai+b=1+2i\\-ai+b=1-2i\end{cases}$，相加得 $2b=2$、$b=1$；相减得 $2ai=4i$、$a=2$。余式 $2x+1$。除以$x-1$时由余数定理，余式为$f(1)=1+1+1=3$。

答案：除以 $x-1$ 余 $3$；除以 $x^2+1$ 余 $2x+1$

修订后：数学内容及场景文字合格。

## eval-linalg-026-s3

体积数值应独立计算，不能未推导就引用另一解的18

题目：判断向量组 $\alpha_1=(1,2,3)$，$\alpha_2=(2,3,1)$，$\alpha_3=(3,1,2)$ 是否线性相关。

过程：三向量张成的平行六面体体积 $|D|=18\ne 0$，即三向量不共面，故线性无关（线性相关⇔体积为 0）。具体计算$\alpha_2\times\alpha_3=(5,-1,-7)$，$\alpha_1\cdot(\alpha_2\times\alpha_3)=5-2-21=-18$，所以体积为18，结论由本解独立获得。

答案：线性无关

修订后：数学内容及场景文字合格。

## eval-linalg-028-s2

列为beta的P将beta坐标送至标准坐标，明确方向

题目：在 $\mathbb R^2$ 中，求向量 $\alpha=(2,3)$ 在基 $\beta_1=(1,2)$、$\beta_2=(1,1)$ 下的坐标。

过程：把基$\{\beta_1,\beta_2\}$坐标映到标准坐标的矩阵 $P=\begin{pmatrix}1&1\\2&1\end{pmatrix}$（列为基向量）。$\alpha=P\xi$，其中 $\xi$ 为所求坐标。$P^{-1}=\dfrac{1}{1-2}\begin{pmatrix}1&-1\\-2&1\end{pmatrix}=\begin{pmatrix}-1&1\\2&-1\end{pmatrix}$。故 $\xi=P^{-1}\alpha=\begin{pmatrix}-1&1\\2&-1\end{pmatrix}\begin{pmatrix}2\\3\end{pmatrix}=\begin{pmatrix}-2+3\\4-3\end{pmatrix}=\begin{pmatrix}1\\1\end{pmatrix}$。

答案：$(1,1)$

修订后：数学内容及场景文字合格。

## eval-linalg-030-s1

可乘常数必须非零，否则不是正交化所得的基

题目：用 Gram–Schmidt 正交化方法把向量组 $(1,1,0),(1,0,1),(0,1,1)$ 化为正交向量组。

过程：取 $u_1=(1,1,0)$。$u_2=(1,0,1)-\dfrac{(1,0,1)\cdot u_1}{\|u_1\|^2}u_1=(1,0,1)-\dfrac{1}{2}(1,1,0)=\left(\dfrac{1}{2},-\dfrac{1}{2},1\right)$，乘 2 取 $u_2=(1,-1,2)$。$u_3=(0,1,1)-\dfrac{(0,1,1)\cdot u_1}{\|u_1\|^2}u_1-\dfrac{(0,1,1)\cdot u_2}{\|u_2\|^2}u_2=(0,1,1)-\dfrac{1}{2}(1,1,0)-\dfrac{1}{6}(1,-1,2)=\left(-\dfrac{2}{3},\dfrac{2}{3},\dfrac{2}{3}\right)$，乘 $-\dfrac{3}{2}$ 取 $u_3=(1,-1,-1)$。验证：$u_1\cdot u_2=0$，$u_1\cdot u_3=1-1+0=0$，$u_2\cdot u_3=1+1-2=0$，两两正交。

答案：$u_1=(1,1,0),\ u_2=(1,-1,2),\ u_3=(1,-1,-1)$；各自只允许乘非零常数。

修订后：数学内容及场景文字合格。

## eval-linalg-030-s2

题干指定GS，原解仅构造另一正交基且与答案不对应；正交化基只允许非零倍数

题目：用 Gram–Schmidt 正交化方法把向量组 $(1,1,0),(1,0,1),(0,1,1)$ 化为正交向量组。

过程：按原顺序令$v_1=(1,1,0),v_2=(1,0,1),v_3=(0,1,1)$。首先$w_1=v_1$，$w_2=v_2-\frac{\langle v_2,w_1\rangle}{\langle w_1,w_1\rangle}w_1=(1/2,-1/2,1)$，可取非零倍数$u_2=(1,-1,2)$。随后$w_3=v_3-\frac12w_1-\frac16u_2=(-2/3,2/3,2/3)$，取$u_3=(-3/2)w_3=(1,-1,-1)$。三者非零且两两内积为0，故按题干指定的Gram–Schmidt得到$u_1=(1,1,0),u_2=(1,-1,2),u_3=(1,-1,-1)$。允许每个结果乘非零常数。

答案：$u_1=(1,1,0),\ u_2=(1,-1,2),\ u_3=(1,-1,-1)$；各自只允许乘非零常数。

修订后：数学内容及场景文字合格。

## eval-linalg-030-s3

只验张成和行列式不等于执行GS，补投影过程和非零条件

题目：用 Gram–Schmidt 正交化方法把向量组 $(1,1,0),(1,0,1),(0,1,1)$ 化为正交向量组。

过程：验证解法一的三向量线性无关：行列式 $\begin{vmatrix}1&1&0\\1&-1&2\\1&-1&-1\end{vmatrix}=1\cdot(1+2)-1\cdot(-1-2)+0=3+3=6\ne 0$。且三者张成的空间与原组相同（原组行列式 $\begin{vmatrix}1&1&0\\1&0&1\\0&1&1\end{vmatrix}=-2\ne 0$，两组都张成 $\mathbb R^3$），故正交化合法。按原顺序令$v_1=(1,1,0),v_2=(1,0,1),v_3=(0,1,1)$。首先$w_1=v_1$，$w_2=v_2-\frac{\langle v_2,w_1\rangle}{\langle w_1,w_1\rangle}w_1=(1/2,-1/2,1)$，可取非零倍数$u_2=(1,-1,2)$。随后$w_3=v_3-\frac12w_1-\frac16u_2=(-2/3,2/3,2/3)$，取$u_3=(-3/2)w_3=(1,-1,-1)$。三者非零且两两内积为0，故按题干指定的Gram–Schmidt得到$u_1=(1,1,0),u_2=(1,-1,2),u_3=(1,-1,-1)$。允许每个结果乘非零常数。

答案：$u_1=(1,1,0),\ u_2=(1,-1,2),\ u_3=(1,-1,-1)$；各自只允许乘非零常数。

修订后：数学内容及场景文字合格。

## eval-linalg-033-s3

单边Laplace直接给非负t，补推广到全部实t

题目：设 $A=\begin{pmatrix}0&1\\0&0\end{pmatrix}$，求矩阵指数 $e^{tA}$（$t$ 为参数）。

过程：$(sI-A)^{-1}=\begin{pmatrix}s&-1\\0&s\end{pmatrix}^{-1}=\dfrac{1}{s^2}\begin{pmatrix}s&1\\0&s\end{pmatrix}=\begin{pmatrix}1/s&1/s^2\\0&1/s\end{pmatrix}$。逐项取拉普拉斯逆变换（$\mathcal L^{-1}\{1/s\}=1$，$\mathcal L^{-1}\{1/s^2\}=t$），得 $e^{tA}=\begin{pmatrix}1&t\\0&1\end{pmatrix}$。单边Laplace逆变换先给$t\ge0$的结果。候选$\Phi(t)=I+tA$对全部实$t$满足$\Phi^{\prime}=A\Phi$、$\Phi(0)=I$，由线性常微分方程初值问题唯一性，$\Phi(t)=e^{tA}$对全部实$t$成立。

答案：$e^{tA}=\begin{pmatrix}1&t\\0&1\end{pmatrix}$

修订后：数学内容及场景文字合格。

## eval-linalg-034-s1

答案明确该条证明结论，不引用三种解法作为答案

题目：证明 Cauchy–Schwarz 不等式：对任意向量 $\vec a,\vec b$，$|\vec a\cdot\vec b|\le|\vec a||\vec b|$。

过程：若 $\vec b=\vec 0$ 不等式平凡成立。设 $\vec b\ne\vec 0$，对任意实数 $t$，$0\le|\vec a+t\vec b|^2=|\vec a|^2+2t(\vec a\cdot\vec b)+t^2|\vec b|^2$。该二次函数恒非负，故判别式 $\Delta=4(\vec a\cdot\vec b)^2-4|\vec a|^2|\vec b|^2\le 0$，即 $(\vec a\cdot\vec b)^2\le|\vec a|^2|\vec b|^2$，开方得 $|\vec a\cdot\vec b|\le|\vec a||\vec b|$。等号成立当且仅当 $\vec a+t\vec b=\vec 0$（$\vec a$ 与 $\vec b$ 线性相关）。

答案：$|\vec a\cdot\vec b|\le|\vec a||\vec b|$；等号当且仅当两向量线性相关（包括零向量）。

修订后：数学内容及场景文字合格。

## eval-linalg-034-s2

答案明确该条证明结论，不引用三种解法作为答案

题目：证明 Cauchy–Schwarz 不等式：对任意向量 $\vec a,\vec b$，$|\vec a\cdot\vec b|\le|\vec a||\vec b|$。

过程：若 $\vec b=\vec 0$ 不等式平凡成立。以下设 $\vec b\ne\vec 0$，把 $\vec a$ 分解为 $\vec a=\vec a_\parallel+\vec a_\perp$，其中 $\vec a_\parallel=\dfrac{\vec a\cdot\vec b}{|\vec b|^2}\vec b$ 与 $\vec b$ 平行，$\vec a_\perp\perp\vec b$。由勾股定理 $|\vec a|^2=|\vec a_\parallel|^2+|\vec a_\perp|^2\ge|\vec a_\parallel|^2=\dfrac{(\vec a\cdot\vec b)^2}{|\vec b|^2}$，移项即得。等号成立当且仅当 $\vec a_\perp=\vec 0$。

答案：$|\vec a\cdot\vec b|\le|\vec a||\vec b|$；等号当且仅当两向量线性相关（包括零向量）。

修订后：数学内容及场景文字合格。

## eval-linalg-034-s3

向量证明不能任意中心化，直接构造有限均匀样本并保留原内积；答案明确该条证明结论，不引用三种解法作为答案

题目：证明 Cauchy–Schwarz 不等式：对任意向量 $\vec a,\vec b$，$|\vec a\cdot\vec b|\le|\vec a||\vec b|$。

过程：设$\vec a,\vec b\in\mathbb R^n$，取均匀样本空间$\{1,\ldots,n\}$，定义$X(i)=a_i,\ Y(i)=b_i$。于是$E[X^2]=|\vec a|^2/n$、$E[Y^2]=|\vec b|^2/n$、$E[XY]=(\vec a\cdot\vec b)/n$，不作中心化。若$E[Y^2]=0$，则$\vec b=0$，不等式成立。否则由$E[(X-tY)^2]\ge0$，在$t=E[XY]/E[Y^2]$处得$E[X^2]-(E[XY])^2/E[Y^2]\ge0$，代回并开方即得$|\vec a\cdot\vec b|\le|\vec a||\vec b|$。等号当且仅当$X=tY$在每个样本点成立，或$\vec b=0$，也就是两向量线性相关。

答案：$|\vec a\cdot\vec b|\le|\vec a||\vec b|$；等号当且仅当两向量线性相关（包括零向量）。

修订后：数学内容及场景文字合格。

## eval-linalg-035-s1

答案明确两方向充要关系

题目：证明：$n$ 阶实方阵 $A$ 是正交矩阵（$A^TA=I$）当且仅当 $A$ 的列向量构成 $\mathbb R^n$ 的标准正交基。

过程：把 $A$ 按列分块 $A=(a_1,a_2,\dots,a_n)$。$A^TA$ 的 $(i,j)$ 元为 $a_i^Ta_j=a_i\cdot a_j$。$A^TA=I\iff a_i\cdot a_j=\delta_{ij}$ 对一切 $i,j$ 成立 $\iff$ 列向量两两正交且都是单位向量 $\iff$ 列向量构成标准正交基（$n$ 个两两正交的单位向量必线性无关，因若 $\sum c_ia_i=0$ 则与 $a_j$ 作内积得 $c_j=0$）。

答案：$A^TA=I\iff$列向量构成$\mathbb R^n$的标准正交基。

修订后：数学内容及场景文字合格。

## eval-linalg-035-s2

答案明确两方向充要关系

题目：证明：$n$ 阶实方阵 $A$ 是正交矩阵（$A^TA=I$）当且仅当 $A$ 的列向量构成 $\mathbb R^n$ 的标准正交基。

过程：$A^TA=I\iff$ 对任意 $x$，$|Ax|^2=(Ax)^T(Ax)=x^TA^TAx=x^Tx=|x|^2$，即 $A$ 保长。由极化恒等式 $(Ax,Ay)=\dfrac{|A(x+y)|^2-|Ax|^2-|Ay|^2}{2}=\dfrac{|x+y|^2-|x|^2-|y|^2}{2}=(x,y)$，保长⇒保内积。取 $x=e_i$、$y=e_j$：$(Ae_i,Ae_j)=(e_i,e_j)=\delta_{ij}$，即列向量标准正交。反之列向量标准正交⇒$A^TA=I$ 由解法一。

答案：$A^TA=I\iff$列向量构成$\mathbb R^n$的标准正交基。

修订后：数学内容及场景文字合格。

## eval-linalg-035-s3

必要条件与反例不证明题干充要性，补两方向严格推导；答案明确两方向充要关系

题目：证明：$n$ 阶实方阵 $A$ 是正交矩阵（$A^TA=I$）当且仅当 $A$ 的列向量构成 $\mathbb R^n$ 的标准正交基。

过程：记标准基为$e_1,\ldots,e_n$，$A$的列为$a_i=Ae_i$。若$A^TA=I$，则$a_i\cdot a_j=e_i^TA^TAe_j=\delta_{ij}$；若$\sum_i c_i a_i=0$，分别与$a_j$取内积得$c_j=0$，所以这$n$个单位正交向量是$\mathbb R^n$的基。反过来，若列向量构成标准正交基，则$(A^TA)_{ij}=a_i\cdot a_j=\delta_{ij}$，故$A^TA=I$。行列式为$\pm1$本身不充分，例如剪切矩阵$\begin{pmatrix}1&1\\0&1\end{pmatrix}$的两列不正交；这个反例只是补充，不替代上述充要性证明。

答案：$A^TA=I\iff$列向量构成$\mathbb R^n$的标准正交基。

修订后：数学内容及场景文字合格。

## eval-prob-001-s1

明确等概率、独立初选及主持人始终开羊门和提供换门条件

题目：三扇门中车的位置等概率，初选与车的位置独立。主持人知道车的位置，总从未选的门中打开一扇有羊的门，并总给出换门机会。求坚持初选和换至唯一剩余未开的门各自获车概率。

过程：参赛者初始选中山羊的概率为 $\dfrac{2}{3}$，此时主持人必须打开另一扇山羊门（他不能开车门），剩下的未开门必然是汽车，换门必赢。初始选中汽车的概率为 $\dfrac{1}{3}$，此时换门必输。故换门获胜概率 $=\dfrac{2}{3}\times 1+\dfrac{1}{3}\times 0=\dfrac{2}{3}$。

答案：换门获胜概率为 $\dfrac{2}{3}$，不换为 $\dfrac{1}{3}$

修订后：数学内容及场景文字合格。

## eval-prob-001-s2

明确等概率、独立初选及主持人始终开羊门和提供换门条件

题目：三扇门中车的位置等概率，初选与车的位置独立。主持人知道车的位置，总从未选的门中打开一扇有羊的门，并总给出换门机会。求坚持初选和换至唯一剩余未开的门各自获车概率。

过程：设参赛者选 1 号门、主持人打开 2 号门，并假设主持人在有两扇羊门可选时等概率选择（其余情形由对称性同理）。记 $C_i$=车在 $i$ 号门，$H_2$=主持人开 2 号门。则 $P(H_2|C_3)=1$（车在 3 号门时主持人只能开 2 号门），$P(H_2|C_1)=\dfrac{1}{2}$（车在 1 号门时主持人可在 2、3 号门中等概率选择），$P(H_2|C_2)=0$（主持人不能开有车的门），$P(C_i)=\dfrac{1}{3}$。由贝叶斯公式：$P(C_3|H_2)=\dfrac{P(H_2|C_3)P(C_3)}{P(H_2|C_3)P(C_3)+P(H_2|C_1)P(C_1)+P(H_2|C_2)P(C_2)}=\dfrac{1\cdot\frac{1}{3}}{1\cdot\frac{1}{3}+\frac{1}{2}\cdot\frac{1}{3}+0}=\dfrac{1/3}{1/2}=\dfrac{2}{3}$。即主持人开 2 号门后，车在 3 号门（换门目标）的概率为 $\dfrac{2}{3}$。注意"总是换门"的获胜率 $\dfrac{2}{3}$ 其实不依赖主持人的等概率规则（见解法一）。

答案：换门获胜概率为 $\dfrac{2}{3}$，不换为 $\dfrac{1}{3}$

修订后：数学内容及场景文字合格。

## eval-prob-001-s3

明确等概率、独立初选及主持人始终开羊门和提供换门条件

题目：三扇门中车的位置等概率，初选与车的位置独立。主持人知道车的位置，总从未选的门中打开一扇有羊的门，并总给出换门机会。求坚持初选和换至唯一剩余未开的门各自获车概率。

过程：车的位置（3 种）×参赛者初选（3 种）=9 种等可能情形。逐项枚举：参赛者初选=车门（3 种情形），换门必输；参赛者初选=山羊门（6 种情形），换门必赢。故换门获胜概率 $=\dfrac{6}{9}=\dfrac{2}{3}$。

答案：换门获胜概率为 $\dfrac{2}{3}$，不换为 $\dfrac{1}{3}$

修订后：数学内容及场景文字合格。

## eval-prob-003-s2

期望递推需先排除无穷期望

题目：抛一枚均匀硬币直到出现正面为止，求抛掷次数的期望（几何分布期望）。

过程：记 $E$ 为首次正面所需次数的期望。第一次若为正面（概率 $\dfrac{1}{2}$），总次数为 1；若为反面（概率 $\dfrac{1}{2}$），则"回到原点"，总次数为 $1+E$。故 $E=\dfrac{1}{2}\cdot 1+\dfrac{1}{2}\cdot(1+E)=1+\dfrac{E}{2}$，解得 $E=2$。递推中的期望有限：首次正面等待$X$满足$P(X>2k)=4^{-k}$，尾和公式给出$E[X]\le2\sum_{k=0}^{\infty}4^{-k}=8/3<\infty$，故可对递推式作有限数的移项，得到$E[X]=2$。

答案：$2$

修订后：数学内容及场景文字合格。

## eval-prob-011-s1

等待时间递推和基本矩阵须先证明瞬态且期望有限

题目：抛均匀硬币直到连续出现两次正面（HH）为止，求所需抛掷次数的期望。

过程：设 $E_0$=当前无连续正面记录时的期望剩余次数，$E_1$=刚出现一次正面时的期望剩余次数。状态转移：$E_0=1+\dfrac{1}{2}E_0+\dfrac{1}{2}E_1$（抛一次后：反面回 $E_0$，正面进 $E_1$）；$E_1=1+\dfrac{1}{2}\cdot 0+\dfrac{1}{2}E_0$（再抛：正面完成，反面回 $E_0$）。由第二式 $E_1=1+\dfrac{E_0}{2}$，代入第一式：$E_0=1+\dfrac{E_0}{2}+\dfrac{1}{2}\left(1+\dfrac{E_0}{2}\right)=\dfrac{3}{2}+\dfrac{3E_0}{4}$，解得 $E_0=6$。有限性：把抛掷分成互不重叠的两次一块，每块为HH的概率$1/4$，各块独立。因此首次连续HH时间$T$满足$P(T>2k)\le(3/4)^k$，尾和公式给出$E[T]\le2\sum_{k=0}^{\infty}(3/4)^k=8<\infty$。吸收概率为1，期望有限，所以递推及基本矩阵的期望运算有效。

答案：$6$

修订后：数学内容及场景文字合格。

## eval-prob-011-s2

等待时间递推和基本矩阵须先证明瞬态且期望有限

题目：抛均匀硬币直到连续出现两次正面（HH）为止，求所需抛掷次数的期望。

过程：状态 $\{0,1,H\}$（$H$ 为吸收态），转移矩阵 $P=\begin{pmatrix}1/2&1/2&0\\1/2&0&1/2\\0&0&1\end{pmatrix}$，瞬态子矩阵 $Q=\begin{pmatrix}1/2&1/2\\1/2&0\end{pmatrix}$。基本矩阵 $N=(I-Q)^{-1}=\begin{pmatrix}1/2&-1/2\\-1/2&1\end{pmatrix}^{-1}=4\begin{pmatrix}1&1/2\\1/2&1/2\end{pmatrix}=\begin{pmatrix}4&2\\2&2\end{pmatrix}$（$\det(I-Q)=\dfrac{1}{2}-\dfrac{1}{4}=\dfrac{1}{4}$）。从状态 0 出发的期望步数为 $N$ 第 1 行之和 $=4+2=6$。有限性：把抛掷分成互不重叠的两次一块，每块为HH的概率$1/4$，各块独立。因此首次连续HH时间$T$满足$P(T>2k)\le(3/4)^k$，尾和公式给出$E[T]\le2\sum_{k=0}^{\infty}(3/4)^k=8<\infty$。吸收概率为1，期望有限，所以递推及基本矩阵的期望运算有效。

答案：$6$

修订后：数学内容及场景文字合格。

## eval-prob-012-s3

边界交集为零概率，不应将两个闭事件称为集合互补

题目：设 $X,Y$ 相互独立且均服从 $U(0,1)$，求 $P(X+Y\le 1)$。

过程：$(X,Y)$ 与 $(1-X,1-Y)$ 同分布。$X+Y\le 1\iff (1-X)+(1-Y)\ge 1$，且 $P(X+Y=1)=0$。故 $P(X+Y\le 1)=P(X+Y\ge 1)=\dfrac{1}{2}$（两事件覆盖全空间且交集为零概率边界且等概率）。

答案：$\dfrac{1}{2}$

修订后：数学内容及场景文字合格。

## eval-prob-014-s2

补危险率微分方程的初值、适用条件及条件概率

题目：设 $X\sim\operatorname{Exp}(\lambda)$（$\lambda>0$）。证明无记忆性 $P(X>s+t\mid X>s)=P(X>t)$（$s,t>0$），并说明其含义。

过程：危险率函数 $h(t)=\dfrac{f(t)}{1-F(t)}=\dfrac{\lambda e^{-\lambda t}}{e^{-\lambda t}}=\lambda$ 为常数。常数危险率意味着"每时每刻的瞬时失效倾向不随年龄变化"，这正是无记忆性的微分刻画；反之，若某分布危险率为常数 $\lambda$，解微分方程 $\dfrac{F'}{1-F}=\lambda$ 得 $F(t)=1-e^{-\lambda t}$，故常数危险率⇔指数分布。上述常危险率刻画限定于非负、绝对连续且$F(0)=0$、生存函数正的分布。令$S=1-F$，则$S^{\prime}=-\lambda S$、$S(0)=1$，故$S(t)=e^{-\lambda t}$。所以$P(X>s+t\mid X>s)=S(s+t)/S(s)=e^{-\lambda t}=P(X>t)$，完成无记忆性证明。

答案：证毕；无记忆性成立且是指数分布的特征性质

修订后：数学内容及场景文字合格。

## eval-prob-015-s1

场景均值3.5改为精确分数7/2

题目：掷一枚均匀骰子，设 $X$ 为点数。求 $E[X]$ 与 $\operatorname{Var}(X)$。

过程：$E[X]=\dfrac{1+2+3+4+5+6}{6}=\dfrac{21}{6}=\dfrac{7}{2}$。$E[X^2]=\dfrac{1+4+9+16+25+36}{6}=\dfrac{91}{6}$。$\operatorname{Var}(X)=E[X^2]-(E[X])^2=\dfrac{91}{6}-\dfrac{49}{4}=\dfrac{182-147}{12}=\dfrac{35}{12}$。

答案：$E[X]=\dfrac{7}{2}$，$\operatorname{Var}(X)=\dfrac{35}{12}$

修订后：数学内容及场景文字合格。

