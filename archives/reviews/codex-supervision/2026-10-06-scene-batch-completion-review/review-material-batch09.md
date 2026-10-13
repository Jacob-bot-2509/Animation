# Batch 9 independent review material


## draft-c47-01

P: 购买两组彩票，全部彩票是否中奖相互独立：第一组$1000$张，单张中奖率$1/1000$；第二组$1000$张，单张中奖率$1/500$。求总中奖次数恰为$3$的精确概率；再将两组张数均改为$n$、中奖率改为$1/n,2/n$，求对应概率的极限。

S: 第一组$X\sim B(1000,1/1000)$，第二组$Y\sim B(1000,1/500)$且独立。卷积给精确概率$\sum_{j=0}^3\binom{1000}{j}(1/1000)^j(999/1000)^{1000-j}\binom{1000}{3-j}(1/500)^{3-j}(499/500)^{997+j}$。极限族取$n\ge3$；对固定$j$，两组点概率分别趋于$e^{-1}/j!$与$e^{-2}2^{3-j}/(3-j)!$，有限求和可交换极限。二项式定理给极限$e^{-3}\sum_{j=0}^3 2^{3-j}/[j!(3-j)!]=(9/2)e^{-3}$。有限精确概率与极限值是不同对象，不能写成等号。

A: 精确概率为四项卷积和；稀有事件族的极限$(9/2)e^{-3}$。

Objects: 题面卡:两组彩票的精确概率与稀有事件极限 | 板书一:卷积和四项的逐项对应(j=0,1,2,3 各由哪两组相乘) | 高亮框:关键点——点概率极限的依据 $(1-\frac1n)^n\to e^{-1}$ | 板书二:有限和可交换极限的四项逐项取极限 | 结论卡:极限 $\frac92e^{-3}$

Steps:
第一步:分布:$X\sim B(1000,\frac1{1000})$,$Y\sim B(1000,\frac1{500})$,且独立。
第二步:卷积和(逐项对应,高亮):$P(X+Y=3)=\sum_{j=0}^3P(X=j)P(Y=3-j)$;$j=0$:第一组 $\binom{1000}0(\frac1{1000})^0(\frac{999}{1000})^{1000}$ 与第二组 $\binom{1000}3(\frac1{500})^3(\frac{499}{500})^{997}$ 相乘;$j=1,2,3$ 同理逐项列出。
第三步:极限族:$n\ge3$,$X_n\sim B(n,\frac1n)$,$Y_n\sim B(n,\frac2n)$;固定 $j$:$P(X_n=j)=\binom nj(\frac1n)^j(1-\frac1n)^{n-j}\to\frac{e^{-1}}{j!}$。
第四步:极限依据(逐步,高亮):$\binom nj(\frac1n)^j=\frac{n(n-1)\cdots(n-j+1)}{j!\,n^j}\to\frac1{j!}$;$(1-\frac1n)^n\to e^{-1}$;$(1-\frac1n)^{-j}\to1$;同理 $P(Y_n=3-j)\to\frac{e^{-2}2^{3-j}}{(3-j)!}$。
第五步:有限和可交换极限(关键点):四项有限和逐项取极限:$P\to\sum_{j=0}^3\frac{e^{-1}}{j!}\cdot\frac{e^{-2}2^{3-j}}{(3-j)!}=e^{-3}\sum_{j=0}^3\frac{2^{3-j}}{j!(3-j)!}=e^{-3}\cdot\frac{(1+2)^3}{3!}=\frac{27}6e^{-3}=\frac92e^{-3}$(高亮结论)。


## draft-c47-02

P: 设$X\sim B(100,1/100)$。给出$P(X=0)$的精确值，严格比较它与$e^{-1}$，给指数形式的精确误差上界，不作小数计算。

S: $P(X=0)=(99/100)^{100}$。对$0<x<1$，积分$-\ln(1-x)=\int_0^x(1-t)^{-1}dt$，给$x<-\ln(1-x)<x/(1-x)$。代入$x=1/100$并乘$100$得$-100/99<\ln P(X=0)<-1$，所以$e^{-100/99}<P(X=0)<e^{-1}$。因此$0<e^{-1}-P(X=0)<e^{-1}(1-e^{-1/99})$。这些均为严格界，未把极限分布的点概率冒充有限样本真值。

A: $(99/100)^{100}$；$e^{-100/99}<P<e^{-1}$，误差严格小于$e^{-1}(1-e^{-1/99})$。

Objects: 题面卡:$P(X=0)=(99/100)^{100}$ 与 $e^{-1}$ 的严格比较 | 板书一:$-\ln(1-x)=\int_0^x\frac{dt}{1-t}$ 与被积函数逐点比较 | 高亮框:关键点——$x<-\ln(1-x)<\frac{x}{1-x}$ 的推导 | 板书二:$x=\frac1{100}$ 代入并乘 $100$ 的中间运算 | 结论卡:$e^{-100/99}<P<e^{-1}$,误差 $<e^{-1}(1-e^{-1/99})$

Steps:
第一步:精确值:$P(X=0)=(1-\frac1{100})^{100}=(\frac{99}{100})^{100}$。
第二步:双侧不等式(推导,高亮):对 $0<x<1$,$-\ln(1-x)=\int_0^x\frac{dt}{1-t}$;被积函数满足 $1\le\frac1{1-t}\le\frac1{1-x}$(逐点比较);积分得 $x<-\ln(1-x)<\frac{x}{1-x}$(严格,因被积函数严格)。
第三步:代入(逐步):$x=\frac1{100}$:$\frac1{100}<-\ln\frac{99}{100}<\frac{1/100}{99/100}=\frac1{99}$;乘 $100$:$100\cdot\frac1{100}=1$,$100\cdot\frac1{99}=\frac{100}{99}$;得 $1<-\ln P<\frac{100}{99}$,即 $-\frac{100}{99}<\ln P<-1$(高亮中间运算)。
第四步:取指数:$e^{-100/99}<P(X=0)<e^{-1}$。
第五步:误差界(逐步):$0<e^{-1}-P<e^{-1}-e^{-100/99}=e^{-1}(1-e^{-\frac1{99}})$(高亮结论)。


## draft-c47-03

P: 证明:当 $n\to\infty$、$p\to0$ 且 $np\to\lambda>0$ 时，对固定的 $k$，$B(n,p)$ 在 $k$ 处的概率趋于 $\frac{\lambda^k}{k!}e^{-\lambda}$。

S: 设$k\in\mathbb Z_{\ge0}$固定，$p_n\in[0,1]$且$np_n\to\lambda>0$。则$p_n\to0$，最终$0<p_n<1$。点概率写成$(np_n)^k/k!\cdot\prod_{j=0}^{k-1}(1-j/n)\cdot(1-p_n)^{n-k}$，空乘积为$1$。前两因子分别趋于$\lambda^k/k!$与$1$。由$-p_n/(1-p_n)\le\ln(1-p_n)\le-p_n$，乘$n$并夹逼得$n\ln(1-p_n)\to-\lambda$，又$k\ln(1-p_n)\to0$，故第三因子趋于$e^{-\lambda}$。因此固定$k$的极限为$e^{-\lambda}\lambda^k/k!$，这是极限恒等式，不是每个有限$n$的概率等式。

A: 证明见解法(三因子分别取极限:$\lambda^k/k!$、$1$、$e^{-\lambda}$)。

Objects: 题面卡:泊松逼近定理($np\to\lambda$ 时二项点概率趋于泊松) | 板书一:点概率改写 $\frac{(np_n)^k}{k!}\prod_{j=0}^{k-1}(1-\frac jn)(1-p_n)^{n-k}$ | 高亮框:关键点——前两因子的极限依据 | 板书二:夹逼 $-\frac{p_n}{1-p_n}\le\ln(1-p_n)\le-p_n$ 的推导 | 结论卡:$\frac{\lambda^k}{k!}e^{-\lambda}$

Steps:
第一步:条件:$k$ 固定,$p_n\in[0,1]$ 且 $np_n\to\lambda>0$;则 $p_n\to0$,最终 $0<p_n<1$。
第二步:点概率改写(逐步,高亮):$P(X=k)=\binom nkp_n^k(1-p_n)^{n-k}$;组合数展开 $\binom nk=\frac{n(n-1)\cdots(n-k+1)}{k!}$ 得 $=\frac{(np_n)^k}{k!}\cdot\prod_{j=0}^{k-1}(1-\frac jn)\cdot(1-p_n)^{n-k}$(空乘积为 $1$)。
第三步:前两因子(依据,高亮):$(np_n)^k\to\lambda^k$(由 $np_n\to\lambda$);$\prod_{j=0}^{k-1}(1-\frac jn)\to1$(有限个因子,每个都趋于 $1$)。
第四步:第三因子(夹逼,高亮):由 $\ln(1+t)\le t$ 与 $\ln(1-t)\ge\frac{-t}{1-t}$ 得 $-\frac{p_n}{1-p_n}\le\ln(1-p_n)\le-p_n$;乘 $(n-k)$ 后两端分别趋于 $-\lambda$(因 $np_n\to\lambda$、$p_n\to0$);故 $(1-p_n)^{n-k}\to e^{-\lambda}$。
第五步:三因子相乘:$P(X=k)\to\frac{\lambda^k}{k!}e^{-\lambda}$(高亮结论)。


## draft-c47-04

P: 令$X\sim B(2,1/2)$、$Y\sim\operatorname{Pois}(1)$。精确求两离散分布的全变差距离$d_{TV}=\frac12\sum_{k\ge0}|P(X=k)-P(Y=k)|$，说明相同均值不足以保证同分布。

S: 两者均值为$1$，方差分别$1/2$与$1$。由$2<e<3$，在$k=0$有$e^{-1}>1/4$，在$k=1$有$1/2>e^{-1}$，在$k=2$有$1/4>1/(2e)$；$k\ge3$仅泊松分布有正质量。总正差等于总负差，故全变差为$[1/2-e^{-1}]+[1/4-1/(2e)]=3/4-3/(2e)>0$。$2<e<3$可由$e=\sum1/j!$与$j!\ge2^{j-1}$（$j\ge2$且部分严格）证明。均值相同不能消除分布差异；也不能把“泊松参数大”当作独立的禁用判据。

A: $d_{TV}=3/4-3/(2e)>0$；同均值但方差及分布不同。

Objects: 题面卡:$X\sim B(2,\frac12)$ 与 $Y\sim\operatorname{Pois}(1)$ 的全变差 | 板书一:均值方差对照(均值均 $1$,方差 $\frac12$ 与 $1$) | 高亮框:关键点——$2<e<3$ 导出逐点比较 | 板书二:正差项 $k=1,2$ 与负差项 $k=0,k\ge3$ 的逐项求和 | 结论卡:$d_{TV}=\frac34-\frac3{2e}>0$

Steps:
第一步:均值:两者均值均为 $1$;方差:$B(2,\frac12)$ 为 $2\cdot\frac12\cdot\frac12=\frac12$;$\operatorname{Pois}(1)$ 为 $1$。
第二步:逐点比较(推导,高亮):由 $2<e<3$:$k=0$:$e<4$ 给 $e^{-1}>\frac14$;$k=1$:$e>2$ 给 $\frac12>e^{-1}$;$k=2$:$e>2$ 给 $\frac14>\frac1{2e}$;$k\ge3$:只有泊松分布有正质量。
第三步:正差项求和(逐步):正差出现在 $k=1$:$(\frac12-e^{-1})$ 与 $k=2$:$(\frac14-\frac1{2e})$;负差出现在 $k=0$ 与 $k\ge3$。
第四步:总正差等于总负差(关键点):两分布总质量均为 $1$;故全变差 $=\frac12\sum|P_X-P_Y|=$ 正差之和 $=\frac12-e^{-1}+\frac14-\frac1{2e}=\frac34-\frac3{2e}$(逐项合并,高亮)。
第五步:结论:$d_{TV}=\frac34-\frac3{2e}>0$;相同均值不足以保证同分布(高亮)。


## draft-c47-05

P: 对$X\sim B(50,1/50)$，精确求$P(X\le2)$并证明它严格大于$P(Y\le2)$，其中$Y\sim\operatorname{Pois}(1)$。比较必须由不等式证明，不能查小数表。

S: 直接相加三项得$P(X\le2)=(49/50)^{48}[(49/50)^2+49/50+49/100]=(1519/625)(49/50)^{48}$。泊松值为$5/(2e)$。两者比值为$e(49/50)^{48}(3038/3125)$。对$0<x<1$，级数或积分给$\ln(1-x)\ge-x-x^2/[2(1-x)]$；又$\ln(1-y)>-y/(1-y)$。取$x=1/50,y=87/3125$，比值的对数严格大于$1-24/25-12/1225-87/3038=17/10850>0$。故二项概率严格较大；差的精确表达式为$(1519/625)(49/50)^{48}-5/(2e)$。

A: $P(X\le2)=(1519/625)(49/50)^{48}>5/(2e)$，差如上。

Objects: 题面卡:$B(50,\frac1{50})$ 与 $\operatorname{Pois}(1)$ 的 $\le2$ 概率比较 | 板书一:$k=0,1,2$ 三项的具体系数与提取公因子 | 高亮框:关键点——通分 $\frac{2401+2450+1225}{2500}=\frac{1519}{625}$ | 板书二:泊松三项求和 $\frac5{2e}$ 与比值表达式 | 结论卡:不等式链给比值 $>1$

Steps:
第一步:三项相加(逐步,高亮):$P(X\le2)=\sum_{k=0}^2\binom{50}k(\frac1{50})^k(\frac{49}{50})^{50-k}$;$k=0$:$(\frac{49}{50})^{50}$;$k=1$:$50\cdot\frac1{50}(\frac{49}{50})^{49}=(\frac{49}{50})^{49}$;$k=2$:$\binom{50}2(\frac1{50})^2(\frac{49}{50})^{48}=\frac{49}{100}(\frac{49}{50})^{48}$。
第二步:提取公因子并通分(逐步):$P(X\le2)=(\frac{49}{50})^{48}[(\frac{49}{50})^2+\frac{49}{50}+\frac{49}{100}]$;$(\frac{49}{50})^2=\frac{2401}{2500}$,$\frac{49}{50}=\frac{2450}{2500}$,$\frac{49}{100}=\frac{1225}{2500}$;和 $=\frac{2401+2450+1225}{2500}=\frac{6076}{2500}=\frac{1519}{625}$(高亮通分);故 $P(X\le2)=\frac{1519}{625}(\frac{49}{50})^{48}$。
第三步:泊松值(逐步):$P(Y\le2)=e^{-1}+e^{-1}+\frac{e^{-1}}2=\frac5{2e}$。
第四步:比值(逐步):$\frac{P(X\le2)}{P(Y\le2)}=\frac{\frac{1519}{625}(\frac{49}{50})^{48}}{\frac5{2e}}=e(\frac{49}{50})^{48}\cdot\frac{3038}{3125}$;取对数:$=\ln\frac{3038}{3125}+48\ln\frac{49}{50}+1$。
第五步:不等式证明(关键点,高亮):对 $0<x<1$,$\ln(1-x)\ge-x-\frac{x^2}{2(1-x)}$,且 $\ln(1-y)>-\frac y{1-y}$;取 $x=\frac1{50}$:$48\ln\frac{49}{50}\ge-\frac{24}{25}-\frac{12}{1225}$;取 $y=\frac{87}{3125}$:$\ln\frac{3038}{3125}>-\frac{87}{3038}$;合计 $>1-\frac{24}{25}-\frac{12}{1225}-\frac{87}{3038}=\frac{37}{1225}-\frac{87}{3038}>0$;故比值 $>1$,即 $P(X\le2)>P(Y\le2)$(比较由不等式证明,不查小数表)。


## draft-c48-02

P: 设$Z\sim N(0,1)$。精确给出$P(|Z|\le k)$（$k=1,2,3$）；对任意$k>0$证明双侧尾界$2k\phi(k)/(k^2+1)<P(|Z|>k)<2\phi(k)/k$。

S: 对称性给$P(|Z|\le k)=2\Phi(k)-1$。记$I=\int_k^\infty\phi(t)dt$；因$t/k>1$，$I<(1/k)\int_k^\infty t\phi(t)dt=\phi(k)/k$。分部积分得$I=\phi(k)/k-\int_k^\infty\phi(t)/t^2dt$，后项严格小于$I/k^2$，故$I>k\phi(k)/(k^2+1)$。乘$2$即得双侧界。三个覆盖概率分别为$2\Phi(1)-1,2\Phi(2)-1,2\Phi(3)-1$，所有界均有证明，无小数覆盖率。

A: 覆盖概率$2\Phi(k)-1$；尾界$\frac{2k\phi(k)}{k^2+1}<P(|Z|>k)<\frac{2\phi(k)}k$。

Objects: 题面卡:标准正态的双侧尾界 | 板书一:$I=\int_k^\infty\phi(t)dt$ 与上界放缩 $t/k>1$ | 高亮框:关键点——分部积分 $I=\frac{\phi(k)}k-\int\frac{\phi(t)}{t^2}dt$ | 板书二:$\frac1{t^2}<\frac1{k^2}$ 与移项解出下界 | 结论卡:$\frac{2k\phi(k)}{k^2+1}<P(|Z|>k)<\frac{2\phi(k)}k$

Steps:
第一步:由对称性:$P(|Z|\le k)=2\Phi(k)-1$;记尾积分 $I=\int_k^\infty\phi(t)dt$。
第二步:上界(逐步,高亮):区间上 $t/k>1$,故 $\phi(t)<(t/k)\phi(t)$;积分得 $I<\frac1k\int_k^\infty t\phi(t)dt$;因 $\phi'(t)=-t\phi(t)$,右端 $=\frac1k[\phi(k)-\phi(\infty)]=\frac{\phi(k)}k$。
第三步:下界(分部积分逐步,高亮):由 $\frac d{dt}(-\frac{\phi(t)}t)=(1+\frac1{t^2})\phi(t)$ 得 $I=[-\frac{\phi(t)}t]_k^\infty-\int_k^\infty\frac{\phi(t)}{t^2}dt=\frac{\phi(k)}k-\int_k^\infty\frac{\phi(t)}{t^2}dt$。
第四步:放缩(关键点):区间上 $t>k$ 给 $t^2>k^2$,即 $\frac1{t^2}<\frac1{k^2}$;故 $\int_k^\infty\frac{\phi(t)}{t^2}dt<\frac{I}{k^2}$;代入得 $I>\frac{\phi(k)}k-\frac{I}{k^2}$;移项(逐步):$I(1+\frac1{k^2})>\frac{\phi(k)}k$,即 $I>\frac{k\phi(k)}{k^2+1}$(高亮移项)。
第五步:乘 $2$ 得双侧尾界:$\frac{2k\phi(k)}{k^2+1}<P(|Z|>k)<\frac{2\phi(k)}k$(高亮结论)。


## draft-c48-04

P: 设独立$X\sim N(1,4),Y\sim N(2,9)$。求$S=X+Y,T=2X-Y$的分布及协方差，判断独立性；再求使$S$与$aX-Y$独立的全部实$a$。

S: $S\sim N(3,13)$，$T\sim N(0,25)$，所以$P(T>0)=1/2$。但$\operatorname{Cov}(S,T)=2\operatorname{Var}X-\operatorname{Var}Y=8-9=-1$，故不独立。由于$(S,aX-Y)$联合正态，独立等价于协方差为零，即$4a-9=0$，唯一$a=9/4$。此时$aX-Y\sim N(1/4,117/4)$。联合正态是使用零协方差推出独立的关键，不能推广到任意分布。

A: $S\sim N(3,13),T\sim N(0,25)$，协方差$-1$，不独立；唯一$a=9/4$。

Objects: 题面卡:$S=X+Y$、$T=2X-Y$ 的分布与独立性 | 板书一:均值方差的逐项计算 | 高亮框:关键点——协方差双线性展开 $2\operatorname{Var}X-\operatorname{Var}Y=8-9=-1$ | 板书二:联合正态下独立 ⟺ 协方差为零 | 结论卡:$S\sim N(3,13)$,$T\sim N(0,25)$,不独立;唯一 $a=\frac94$

Steps:
第一步:均值方差(逐项,高亮):$ES=EX+EY=1+2=3$;$\operatorname{Var}S=4+9=13$(独立,无交叉项);$ET=2EX-EY=2-2=0$;$\operatorname{Var}T=4\cdot4+9=25$;故 $S\sim N(3,13)$,$T\sim N(0,25)$,从而 $P(T>0)=\frac12$。
第二步:协方差(双线性展开,高亮):$\operatorname{Cov}(S,T)=\operatorname{Cov}(X+Y,2X-Y)=2\operatorname{Cov}(X,X)-\operatorname{Cov}(X,Y)+2\operatorname{Cov}(Y,X)-\operatorname{Cov}(Y,Y)$;独立性给 $\operatorname{Cov}(X,Y)=0$;故 $=2\operatorname{Var}X-\operatorname{Var}Y=8-9=-1\ne0$,不独立。
第三步:判定方法:$(S,aX-Y)$ 是 $(X,Y)$ 的线性变换,联合正态;联合正态下独立等价于协方差为零(高亮)。
第四步:求 $a$:$\operatorname{Cov}(X+Y,aX-Y)=a\operatorname{Var}X-\operatorname{Var}Y=4a-9$;令 $4a-9=0$,得唯一 $a=\frac94$。
第五步:验证(逐步):$a=\frac94$ 时 $aX-Y\sim N(\frac94-2,\frac{81}4\cdot4+9)=N(\frac14,\frac{117}4)$;其余 $a$ 协方差非零,不独立(高亮结论)。


## draft-c49-04

P: 证明切比雪夫大数定律:若随机变量序列 $X_1,X_2,\dots$ 两两不相关，且存在常数 $C$ 使 $Var(X_i)\le C$ 对一切 $i$ 成立，则 $\frac{1}{n}\sum_{i=1}^{n}(X_i-EX_i)\xrightarrow{P}0$。

S: 令 $S_n=\frac1n\sum_{i=1}^{n}(X_i-EX_i)$。$ES_n=0$。由两两不相关,$Var(S_n)=\frac{1}{n^2}\sum_{i=1}^{n}Var(X_i)\le\frac{nC}{n^2}=\frac{C}{n}$(协方差项全为零)。由切比雪夫不等式,对任意 $\varepsilon>0$,$P(|S_n|\ge\varepsilon)\le\frac{Var(S_n)}{\varepsilon^2}\le\frac{C}{n\varepsilon^2}\to0$。故 $S_n\xrightarrow{P}0$。

A: 证明见解法(两两不相关使方差无交叉项:$Var(S_n)\le C/n\to0$,切比雪夫得依概率收敛)。

Objects: 题面卡:切比雪夫大数定律(两两不相关+方差一致有界) | 板书一:方差展开 $\frac1{n^2}\sum_i\operatorname{Var}X_i+\frac1{n^2}\sum_{i\ne j}\operatorname{Cov}(X_i,X_j)$ | 高亮框:关键点——交叉项因两两不相关逐项消失 | 板书二:切比雪夫代入与 $\frac C{n\varepsilon^2}$ | 结论卡:$\frac1n\sum(X_i-EX_i)\xrightarrow P0$

Steps:
第一步:令 $S_n=\frac1n\sum_{i=1}^n(X_i-EX_i)$;则 $ES_n=0$。
第二步:方差展开(逐项,高亮):$\operatorname{Var}S_n=\frac1{n^2}\sum_i\operatorname{Var}X_i+\frac1{n^2}\sum_{i\ne j}\operatorname{Cov}(X_i,X_j)$;两两不相关给 $\operatorname{Cov}(X_i,X_j)=0$($i\ne j$),交叉项逐项消失(高亮演示)。
第三步:界:$\operatorname{Var}S_n=\frac1{n^2}\sum_{i=1}^n\operatorname{Var}X_i\le\frac{nC}{n^2}=\frac Cn$。
第四步:切比雪夫:对任意 $\varepsilon>0$,$P(|S_n|\ge\varepsilon)\le\frac{\operatorname{Var}S_n}{\varepsilon^2}\le\frac C{n\varepsilon^2}$。
第五步:收敛(关键点,高亮):$\varepsilon$ 任意固定,$n\to\infty$ 时 $\frac C{n\varepsilon^2}\to0$,概率界收缩;故 $S_n\xrightarrow P0$。


## draft-c49-05

P: 证明独立同分布且$E|X_1|<\infty$时样本均值依概率收敛到$\mu=EX_1$，无需有限方差。证明必须说明截断偏差和尾部概率怎样分别控制。

S: 令$Y_i^{(M)}=X_i\mathbf1_{|X_i|\le M}$，$\tau_M=E[|X_1|\mathbf1_{|X_1|>M}]\to0$。有$|EY_1^{(M)}-\mu|\le\tau_M$，$E|\overline X_n-\overline Y_n^{(M)}|\le\tau_M$，且独立性给$\operatorname{Var}(\overline Y_n^{(M)})\le M^2/n$。固定$\varepsilon>0$并取$M$使$\tau_M<\varepsilon/3$，三角不等式、Markov与Chebyshev得$P(|\overline X_n-\mu|>\varepsilon)\le3\tau_M/\varepsilon+9M^2/(n\varepsilon^2)$。先对固定$M$令$n\to\infty$，再令$M\to\infty$，上极限为零。该次序避免把随$n$变化的截断界误当一致方差界。

A: $E|X_1|<\infty$的独立同分布样本满足$\overline X_n\xrightarrow P\mu$，不需要有限方差。

Objects: 题面卡:无有限方差的样本均值依概率收敛 | 板书一:截断 $Y_i^{(M)}=X_i\mathbf1_{|X_i|\le M}$ 与 $\tau_M\to0$ | 高亮框:关键点——三项控制:尾部概率(Markov)、截断偏差、切比雪夫 | 板书二:三项放缩依据逐项标注 | 结论卡:先 $n\to\infty$ 后 $M\to\infty$,$\overline X_n\xrightarrow P\mu$

Steps:
第一步:截断:$Y_i^{(M)}=X_i\mathbf1_{|X_i|\le M}$;$\tau_M=E[|X_1|\mathbf1_{|X_1|>M}]\to0$(由 $E|X_1|<\infty$,高亮)。
第二步:截断偏差(逐步,高亮):$|EY_1^{(M)}-\mu|=|E[X_1\mathbf1_{|X_1|>M}]|\le\tau_M$;$E|\overline X_n-\overline Y_n^{(M)}|\le\frac1n\sum_iE|X_i-Y_i^{(M)}|=\tau_M$。
第三步:截断方差(依据):独立性给 $\operatorname{Var}(\overline Y_n^{(M)})=\frac1{n^2}\sum_i\operatorname{Var}Y_i^{(M)}\le\frac{M^2}n$(因 $|Y|\le M$ 给 $\operatorname{Var}Y\le EY^2\le M^2$)。
第四步:三项控制(关键点,高亮):(i) 尾部概率(Markov):$P(\exists i:|X_i|>M)\le nP(|X_1|>M)\le\frac{n\tau_M}M$;(ii) 截断偏差 $|E\overline X_n-E\overline Y_n^{(M)}|\le\tau_M$;(iii) 切比雪夫:$P(|\overline Y_n^{(M)}-E\overline Y_n^{(M)}|\ge\varepsilon)\le\frac{M^2}{n\varepsilon^2}$。
第五步:取极限次序(关键点,高亮):先令 $n\to\infty$(切比雪夫项与尾部项趋于零),再令 $M\to\infty$($\tau_M\to0$);次序不可交换;结论:$E|X_1|<\infty$ 的独立同分布样本满足 $\overline X_n\xrightarrow P\mu$,无需有限方差。


## draft-c50-01

P: 设独立$X_i\sim U(0,1)$，$S_n=\sum_{i=1}^nX_i$。精确求$P(S_{100}>55)$；另对固定实$a$求$\lim_{n\to\infty}P(S_n>n/2+a\sqrt{n/12})$。

S: 连续均匀立方体中，$\sum x_i\le s$的非负单纯形体积为$s^n/n!$；用容斥扣除坐标超过$1$的区域，得到$P(S_n\le s)=\frac1{n!}\sum_{k=0}^{\lfloor s\rfloor}(-1)^k\binom nk(s-k)^n$（$0\le s\le n$）。$S_{100}$与$100-S_{100}$同分布且无原子，所以目标概率为$P(S_{100}<45)=\frac1{100!}\sum_{k=0}^{45}(-1)^k\binom{100}k(45-k)^{100}$，是精确有理数。因单变量均值$1/2$、方差$1/12$，经典CLT给标准化和依分布收敛到$N(0,1)$；正态CDF连续，故极限为$1-\Phi(a)$。CLT的极限不等于固定样本的概率。

A: 有限概率$\frac1{100!}\sum_{k=0}^{45}(-1)^k\binom{100}k(45-k)^{100}$；极限$1-\Phi(a)$。

Objects: 题面卡:均匀和 $S_{100}>55$ 的精确概率与 CLT 极限 | 板书一:单纯形体积与容斥展开的 k=0,1,2 各项 | 高亮框:关键点——$S_{100}$ 与 $100-S_{100}$ 同分布且无原子 | 板书二:代入 $n=100,s=45$ 的求和式 | 结论卡:极限 $1-\Phi(a)$

Steps:
第一步:单纯形体积(逐步,高亮):$0\le s\le1$ 时 $P(S_n\le s)$ 为非负单纯形体积 $\frac{s^n}{n!}$;对一般 $s$ 用容斥扣除坐标超过 $1$ 的区域。
第二步:容斥展开(逐项):$k=0$:单纯形体积 $\frac{s^n}{n!}$;$k=1$:扣除一个坐标超 $1$ 的区域(平移后仍为单纯形,体积 $\frac{(s-1)^n}{n!}$),共 $\binom n1$ 个;$k=2$:加回两个坐标同时超 $1$ 的交,依此类推;得 $P(S_n\le s)=\frac1{n!}\sum_{k=0}^{\lfloor s\rfloor}(-1)^k\binom nk(s-k)^n$($0\le s\le n$,高亮)。
第三步:对称性(推导,高亮):每个 $X_i$ 与 $1-X_i$ 同分布,故 $S_{100}$ 与 $100-S_{100}$ 同分布,且连续分布无原子;于是 $P(S_{100}>55)=P(100-S_{100}<45)=P(S_{100}<45)=P(S_{100}\le45)$。
第四步:代入 $n=100$,$s=45$($\lfloor45\rfloor=45$):$P(S_{100}\le45)=\frac1{100!}\sum_{k=0}^{45}(-1)^k\binom{100}k(45-k)^{100}$。
第五步:极限(逐步,高亮):$EX_i=\frac12$,$\operatorname{Var}X_i=\frac1{12}$;中心极限定理给 $\frac{S_n-n/2}{\sqrt{n/12}}\Rightarrow N(0,1)$;故 $\lim_{n\to\infty}P(S_n>n/2+a\sqrt{n/12})=P(Z>a)=1-\Phi(a)$。
