# linalg-051 精确修订候选

在实多项式空间 $\mathbb R[x]$ 上定义前向差分算子 $\Delta p(x)=p(x+1)-p(x)$。证明 $\ker\Delta$ 恰为常数多项式空间，且 $\Delta:\mathbb R[x]\to\mathbb R[x]$ 为满射；求满足 $\Delta p(x)=3x^2+3x+1$、$p(0)=0$ 的全部多项式。

## 证明与过程

$\Delta$ 是线性算子。若 $p(x)=a_nx^n+\cdots$、$n\ge1$、$a_n\ne0$，二项式恒等式给出 $\Delta p(x)=na_nx^{n-1}+\cdots\ne0$；常数多项式的差分为零，故 $\ker\Delta=\mathbb R\cdot1$。证明满射：零多项式已有原像。若目标多项式 $g$ 的次数为 $m\ge0$、首项为 $c_mx^m$，则 $\Delta(\frac{c_m}{m+1}x^{m+1})$ 的首项恰为 $c_mx^m$。两者之差次数小于 $m$；对次数归纳（常数 $c$ 的原像为 $cx$）即可构造 $g$ 的原像。最后 $(x+1)^3-x^3=3x^2+3x+1$，故任意解与 $x^3$ 之差属于 $\ker\Delta$，即 $p=x^3+C$。由 $p(0)=0$ 得 $C=0$，所以解唯一。

## 答案

$\ker\Delta=\mathbb R\cdot1$，$\operatorname{im}\Delta=\mathbb R[x]$；唯一解 $p(x)=x^3$。

## 场景文字

先用二项式恒等式证明非零非常数多项式不在核中。

逐次消去目标的最高次项，证明满射。

验证 $x^3$ 的差分；由核得到全体解 $x^3+C$。

代入 $p(0)=0$ 确定 $C=0$。
