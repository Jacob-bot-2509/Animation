# Batch 10 independent review material


## draft-c50-03

P: 独立$X_i\sim\operatorname{Exp}(1)$。求$P(S_{100}>110)$的精确式，并证明它；另求固定实$a$时$P(S_n>n+a\sqrt n)$的极限。不得凭未验证小数宣称有限误差很小。

S: 卷积或归纳给$S_n$密度$e^{-s}s^{n-1}/(n-1)!$（$s>0$）。对尾积分分部积分，$T_n(t)=e^{-t}t^{n-1}/(n-1)!+T_{n-1}(t)$，$T_1(t)=e^{-t}$，所以$P(S_{100}>110)=e^{-110}\sum_{k=0}^{99}110^k/k!$。这是精确表达，也等于$P(\operatorname{Pois}(110)\le99)$。单变量均值和方差均$1$，CLT给$(S_n-n)/\sqrt n\Rightarrow N(0,1)$，故所求极限$1-\Phi(a)$。该定理本身不提供$n=100$的误差大小，不能据此断言近似“极佳”。

A: 精确尾$e^{-110}\sum_{k=0}^{99}110^k/k!$；极限$1-\Phi(a)$。

Objects: 题面卡:$\operatorname{Exp}(1)$ 和 $S_{100}>110$ 的精确式与极限 | 板书一:密度 $\frac{e^{-s}s^{n-1}}{(n-1)!}$ 与分部积分递推 | 高亮框:关键点——递推 $T_n(t)=\frac{e^{-t}t^{n-1}}{(n-1)!}+T_{n-1}(t)$ 逐次累加 | 板书二:泊松等价的分布律对照 | 结论卡:精确尾 $e^{-110}\sum_{k=0}^{99}\frac{110^k}{k!}$;极限 $1-\Phi(a)$

Steps:
第一步:密度:卷积或归纳给 $S_n$ 的密度 $f_n(s)=\frac{e^{-s}s^{n-1}}{(n-1)!}$($s>0$)。
第二步:尾积分递推(逐步,高亮):记 $T_n(t)=\int_t^\infty\frac{e^{-s}s^{n-1}}{(n-1)!}ds$;分部积分:$\int_t^\infty e^{-s}s^{n-1}ds=[-e^{-s}s^{n-1}]_t^\infty+(n-1)\int_t^\infty e^{-s}s^{n-2}ds=e^{-t}t^{n-1}+(n-1)\int_t^\infty e^{-s}s^{n-2}ds$;除以 $(n-1)!$ 得 $T_n(t)=\frac{e^{-t}t^{n-1}}{(n-1)!}+T_{n-1}(t)$;$T_1(t)=e^{-t}$。
第三步:递推展开(逐步):从 $T_1$ 逐次递推到 $T_{100}$,每步累加一项 $\frac{e^{-t}t^k}{k!}$;故 $T_{100}(110)=e^{-110}\sum_{k=0}^{99}\frac{110^k}{k!}$;即 $P(S_{100}>110)=e^{-110}\sum_{k=0}^{99}\frac{110^k}{k!}$(高亮)。
第四步:泊松等价(依据,高亮):泊松分布律 $P(\operatorname{Pois}(110)\le99)=e^{-110}\sum_{k=0}^{99}\frac{110^k}{k!}$,与上式逐项相同。
第五步:极限(逐步):$EX_i=\operatorname{Var}X_i=1$;CLT 给 $\frac{S_n-n}{\sqrt n}\Rightarrow N(0,1)$;故 $\lim P(S_n>n+a\sqrt n)=\lim P(\frac{S_n-n}{\sqrt n}>a)=1-\Phi(a)$;注意:该定理不提供 $n=100$ 的误差大小,不能凭未验证小数宣称有限误差很小(高亮)。


## draft-c50-04

P: 设$X_n\sim B(n,1/2)$。精确写出$P(X_{100}\le55)$；证明整数事件阈值移动半单位的等价性，并对$k_n=\lfloor n/2+a\sqrt n/2\rfloor$证明有无半单位移动都给同一极限。

S: 有限精确概率为$2^{-100}\sum_{j=0}^{55}\binom{100}j$。由于$X_n$取整数，对整数$k$有$\{X_n\le k\}=\{X_n\le k+1/2\}$，这只是事件等价。标准化$Z_n=(X_n-n/2)/(\sqrt n/2)$由CLT趋于标准正态。阈值$z_n=(k_n-n/2)/(\sqrt n/2)$满足$|z_n-a|\le2/\sqrt n$，移动半单位后增加$1/\sqrt n$，二者都趋于$a$。用固定$a\pm\varepsilon$夹逼和$\Phi$连续性，得概率极限$\Phi(a)$。有限事件等价不能推出其概率等于某个正态CDF；连续性修正的有限误差是否变小还需额外分析，不能由CLT单独保证。

A: 精确值$2^{-100}\sum_{j=0}^{55}\binom{100}j$；整数事件可移动半单位，两个标准化阈值均给极限$\Phi(a)$。

Objects: 题面卡:$B(n,\frac12)$ 的整数阈值与半单位移动 | 板书一:精确概率 $2^{-100}\sum_{j=0}^{55}\binom{100}j$ | 高亮框:关键点——事件等价 $\{X_n\le k\}=\{X_n\le k+\frac12\}$ | 板书二:$|z_n-a|\le\frac2{\sqrt n}$ 与半单位移动增 $\frac1{\sqrt n}$ 的推导 | 结论卡:两个标准化阈值均给极限 $\Phi(a)$

Steps:
第一步:精确概率:$P(X_{100}\le55)=2^{-100}\sum_{j=0}^{55}\binom{100}j$。
第二步:半单位移动(事件等价,高亮):$X_n$ 只取整数,故对整数 $k$:$\{X_n\le k\}=\{X_n\le k+\frac12\}$,只是事件等价,不改变概率。
第三步:标准化:$Z_n=\frac{X_n-n/2}{\sqrt n/2}$,CLT 给 $Z_n\Rightarrow N(0,1)$;对 $k_n=\lfloor n/2+a\sqrt n/2\rfloor$,记阈值 $z_n=\frac{k_n-n/2}{\sqrt n/2}$。
第四步:阈值估计(推导,高亮):$|z_n-a|=\frac{|k_n-(n/2+a\sqrt n/2)|}{\sqrt n/2}\le\frac1{\sqrt n/2}=\frac2{\sqrt n}$(取整误差不超过 $1$);移动半单位后阈值增加 $\frac{1/2}{\sqrt n/2}=\frac1{\sqrt n}$;二者都趋于 $a$。
第五步:夹逼(逐步,高亮):对固定 $\varepsilon>0$,最终 $z_n\in(a-\varepsilon,a+\varepsilon)$;于是 $P(Z_n\le a-\varepsilon)\le P(X_n\le k_n)\le P(Z_n\le a+\varepsilon)$;两边取极限得 $\Phi(a-\varepsilon)\le\liminf\le\limsup\le\Phi(a+\varepsilon)$;由 $\Phi$ 的连续性令 $\varepsilon\to0$,得极限 $\Phi(a)$;有限事件等价不能推出其概率等于正态 CDF,连续性论证才是极限依据。


## draft-c50-05

P: 说明经典独立同分布中心极限定理的充分矩条件，并以标准柯西分布证明：去掉这些条件后，样本均值不保证集中到常数或趋于正态。明确反例证明的逻辑范围。

S: 经典独立同分布CLT的充分条件为$EX=\mu$、$0<\operatorname{Var}X=\sigma^2<\infty$，标准化为$(\sum X_i-n\mu)/(\sigma\sqrt n)$；零方差是退化情形。对标准柯西变量，$E|X|$及$EX^2$发散，均值不存在；特征函数$e^{-|t|}$。独立柯西样本均值的特征函数为$(e^{-|t|/n})^n=e^{-|t|}$，所以仍为标准柯西，且$P(|\overline X_n|\le1)=1/2$对所有$n$成立，不集中到零。密度不超过$1/\pi$，故对任何常数$c$，$P(|\overline X_n-c|\le\pi/8)\le1/4$，也不集中到任何常数。这说明删去矩条件后结论不能普遍保证；它没有证明有限方差是所有正态吸引域或其他规范化极限定理的必要条件。

A: 柯西样本均值仍为柯西，不集中到常数；有限正方差是经典$\sqrt n$规范化CLT的充分假设，不能由该反例推断所有CLT的必要条件。

Objects: 题面卡:柯西反例——去掉矩条件后样本均值不集中 | 板书一:经典 CLT 的充分矩条件与标准化 | 高亮框:关键点——特征函数 $(e^{-|t|/n})^n=e^{-|t|}$,样本均值仍为标准柯西 | 板书二:$P(|\overline X_n|\le1)=\frac12$ 与 $P(|\overline X_n-c|\le\frac\pi8)\le\frac14$ | 结论卡:反例只说明充分性,不能推断所有 CLT 的必要条件

Steps:
第一步:经典条件(高亮):$EX=\mu$、$0<\operatorname{Var}X=\sigma^2<\infty$,标准化为 $\frac{\sum X_i-n\mu}{\sigma\sqrt n}$;零方差是退化情形。
第二步:柯西的矩:标准柯西的 $E|X|$ 与 $EX^2$ 发散,均值不存在;特征函数(逐步):$\phi(t)=\frac1\pi\int_{-\infty}^{\infty}\frac{e^{itx}}{1+x^2}dx=e^{-|t|}$。
第三步:样本均值特征函数(逐步,高亮):独立和的特征函数相乘:$\phi_{\overline X_n}(t)=(\phi(t/n))^n=(e^{-|t|/n})^n=e^{-|t|}$;故 $\overline X_n$ 仍为标准柯西(高亮核心结论)。
第四步:不集中到零(逐步):$P(|\overline X_n|\le1)=P(|X|\le1)=\frac2\pi\int_0^1\frac{dx}{1+x^2}=\frac2\pi\cdot\frac\pi4=\frac12$,对所有 $n$ 成立。
第五步:不集中到任何常数(逐步):密度 $f\le\frac1\pi$,故 $P(|\overline X_n-c|\le\frac\pi8)\le\frac1\pi\cdot\frac{2\pi}8=\frac14$;反例的逻辑范围:只说明有限正方差是经典 $\sqrt n$ 规范化 CLT 的充分假设,不能由该反例推断所有 CLT 形式的必要条件(高亮)。
