# 当前评测 300 题与测试 150 题

共 450 份题干、过程、答案。原文逐字段保留，历史错误或小数也是原始证据，不代表本轮认可。每项的场景、方法、条件补充字段见 `record-variants.jsonl`；父级上下文及原始字节见 `mathematical-source-bytes.zip`。数学资格审查必须连同这些上下文进行。本轮只装配证据，不新增核心判定或答案验收。

## 1. eval-calc-001-s1

内容 SHA256：`88324b39ff44dfa527cedeb93c2704d1130cc42146a253d261f54ba3c7d97abd`。

来源：data/v2/eval/dataset_eval.jsonl，第 1 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求极限 $\displaystyle\lim_{x\to 0}\frac{1-\cos x}{x^2}$。

**过程**

由 $1-\cos x = 2\sin^2\dfrac{x}{2}$，得 $\dfrac{1-\cos x}{x^2}=\dfrac{2\sin^2(x/2)}{x^2}=\dfrac{1}{2}\left(\dfrac{\sin(x/2)}{x/2}\right)^2$。令 $t=x/2\to 0$，利用 $\lim_{t\to 0}\dfrac{\sin t}{t}=1$，故原式 $=\dfrac{1}{2}\cdot 1^2=\dfrac{1}{2}$。

**答案原文**

$\dfrac{1}{2}$

## 2. eval-calc-001-s2

内容 SHA256：`3ed0825e52e4bc214af520f41f90f3952a14e31c28b975bc4cd31af4cfee20cb`。

来源：data/v2/eval/dataset_eval.jsonl，第 2 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求极限 $\displaystyle\lim_{x\to 0}\frac{1-\cos x}{x^2}$。

**过程**

$\cos x = 1-\dfrac{x^2}{2}+\dfrac{x^4}{24}+o(x^4)$，故 $1-\cos x = \dfrac{x^2}{2}+o(x^2)$，原式 $=\lim_{x\to 0}\dfrac{x^2/2+o(x^2)}{x^2}=\dfrac{1}{2}$。

**答案原文**

$\dfrac{1}{2}$

## 3. eval-calc-001-s3

内容 SHA256：`efc1ac36580d968313135cbc9d4a8716caf62e307bcec2d2d0afde2e350e2d2b`。

来源：data/v2/eval/dataset_eval.jsonl，第 3 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求极限 $\displaystyle\lim_{x\to 0}\frac{1-\cos x}{x^2}$。

**过程**

原式为 $\dfrac{0}{0}$ 型。第一次求导：$\lim_{x\to 0}\dfrac{\sin x}{2x}$；第二次求导：$\lim_{x\to 0}\dfrac{\cos x}{2}=\dfrac{1}{2}$。

**答案原文**

$\dfrac{1}{2}$

## 4. eval-calc-002-s1

内容 SHA256：`129f5a9496afdf1f98baf610442a068d57fd200f5272fe5382e8f6f21cba71d6`。

来源：data/v2/eval/dataset_eval.jsonl，第 4 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求极限 $\displaystyle\lim_{x\to 0^+} x^x$。

**过程**

令 $y=x^x$，则 $\ln y = x\ln x$。令 $t=\dfrac{1}{x}\to+\infty$，则 $x\ln x = -\dfrac{\ln t}{t}\to 0$（对数函数增长慢于幂函数）。故 $\ln y\to 0$，由指数函数连续性得 $y\to e^0=1$。

**答案原文**

$1$

## 5. eval-calc-002-s2

内容 SHA256：`95d9a1f7797f203e0a8f163aff6f7b0a0cd4750532527ae5a7fa68e1a68fc56c`。

来源：data/v2/eval/dataset_eval.jsonl，第 5 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求极限 $\displaystyle\lim_{x\to 0^+} x^x$。

**过程**

同上先取对数，$x\ln x = \dfrac{\ln x}{1/x}$ 为 $\dfrac{-\infty}{+\infty}$ 型，洛必达：$\lim_{x\to 0^+}\dfrac{1/x}{-1/x^2}=\lim_{x\to 0^+}(-x)=0$，故原极限 $=e^0=1$。

**答案原文**

$1$

## 6. eval-calc-002-s3

内容 SHA256：`8e9d97e984e59bbafdb60016195a8855a08a491159f43cbd9dc7e786abf22ea0`。

来源：data/v2/eval/dataset_eval.jsonl，第 6 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求极限 $\displaystyle\lim_{x\to 0^+} x^x$。

**过程**

令 $x=e^{-t}$（$t\to+\infty$），则 $x^x = (e^{-t})^{e^{-t}} = e^{-t e^{-t}}$，而 $t e^{-t}\to 0$，故极限为 $e^0=1$。

**答案原文**

$1$

## 7. eval-calc-003-s1

内容 SHA256：`3178aa075eceecaa5a31d56a85c210c4e5144c266040eac44be87de825a557ff`。

来源：data/v2/eval/dataset_eval.jsonl，第 7 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

证明极限 $\displaystyle\lim_{n\to\infty}\left(1+\frac{1}{n}\right)^n$ 存在（记为 $e$），并说明它与级数 $\displaystyle\sum_{k=0}^{\infty}\frac{1}{k!}$ 的联系。

**过程**

记 $a_n=\left(1+\dfrac{1}{n}\right)^n$。由二项式展开 $a_n=\sum_{k=0}^{n}\binom{n}{k}\dfrac{1}{n^k}=\sum_{k=0}^{n}\dfrac{1}{k!}\cdot\dfrac{n(n-1)\cdots(n-k+1)}{n^k}$。比较 $a_n$ 与 $a_{n+1}$ 的展开式，第 $k$ 项因子 $\dfrac{n(n-1)\cdots(n-k+1)}{n^k}\le\dfrac{(n+1)n\cdots(n-k+2)}{(n+1)^k}$，且 $a_{n+1}$ 还多一项，故 $a_{n+1}>a_n$，数列递增。又有 $a_n\le\sum_{k=0}^{n}\dfrac{1}{k!}\le 1+1+\dfrac{1}{2}+\dfrac{1}{4}+\cdots+\dfrac{1}{2^{n-1}}<3$，故有上界。由单调有界准则，$\lim a_n$ 存在，记为 $e$。

**答案原文**

极限存在且等于 $e=\sum_{k=0}^{\infty}\frac{1}{k!}$

## 8. eval-calc-003-s2

内容 SHA256：`644cd17e76bd9ee1ba95a6ac3819993b6c2913576318bb3e78588ce74405fda6`。

来源：data/v2/eval/dataset_eval.jsonl，第 8 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

证明极限 $\displaystyle\lim_{n\to\infty}\left(1+\frac{1}{n}\right)^n$ 存在（记为 $e$），并说明它与级数 $\displaystyle\sum_{k=0}^{\infty}\frac{1}{k!}$ 的联系。

**过程**

设 $n\ln\left(1+\dfrac{1}{n}\right)=\dfrac{\ln(1+x)}{x}$，其中 $x=\dfrac{1}{n}\to 0^+$。洛必达：$\lim_{x\to 0^+}\dfrac{\ln(1+x)}{x}=\lim_{x\to 0^+}\dfrac{1}{1+x}=1$。故 $\lim n\ln(1+1/n)=1$，原极限 $=e^1$。注意此解法默认 $e$ 已由其他途径定义，适合作为验证。

**答案原文**

极限存在且等于 $e=\sum_{k=0}^{\infty}\frac{1}{k!}$

## 9. eval-calc-003-s3

内容 SHA256：`088c219ce2941b27baaa40b231812bd9ff913971bd384d1c0b4ef1d854387239`。

来源：data/v2/eval/dataset_eval.jsonl，第 9 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

证明极限 $\displaystyle\lim_{n\to\infty}\left(1+\frac{1}{n}\right)^n$ 存在（记为 $e$），并说明它与级数 $\displaystyle\sum_{k=0}^{\infty}\frac{1}{k!}$ 的联系。

**过程**

记 $c_k(n)=\left(1-\dfrac{1}{n}\right)\left(1-\dfrac{2}{n}\right)\cdots\left(1-\dfrac{k-1}{n}\right)$（约定 $c_0=c_1=1$），则 $a_n=\displaystyle\sum_{k=0}^{n}\dfrac{c_k(n)}{k!}$。每个因子都在 $(0,1]$ 内，故 $0<c_k(n)\le 1$，且对固定 $k$ 有 $c_k(n)\to 1$（$n\to\infty$）。一方面 $a_n\le\displaystyle\sum_{k=0}^{n}\dfrac{1}{k!}=:s_n$；另一方面对任意固定的 $m\le n$，$a_n\ge\displaystyle\sum_{k=0}^{m}\dfrac{c_k(n)}{k!}\to s_m$。于是 $s_m\le\liminf a_n\le\limsup a_n\le\lim s_n$，令 $m\to\infty$ 即得 $\lim a_n=\lim s_n=\displaystyle\sum_{k=0}^{\infty}\dfrac{1}{k!}$——数列极限与级数和两种构造给出同一个数 $e$。

**答案原文**

极限存在且等于 $e=\sum_{k=0}^{\infty}\frac{1}{k!}$

## 10. eval-calc-004-s1

内容 SHA256：`dc519bfa0977429c97074c62cf33384ebf16f4d9c2a50bd01aa1074fd10097a5`。

来源：data/v2/eval/dataset_eval.jsonl，第 10 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求极限 $\displaystyle\lim_{x\to 0}\frac{\sin x-\tan x}{x^3}$。

**过程**

提公因式：$\dfrac{\sin x-\tan x}{x^3}=\dfrac{\sin x\left(1-\dfrac{1}{\cos x}\right)}{x^3}=\dfrac{\sin x}{x}\cdot\dfrac{\cos x-1}{x^2}\cdot\dfrac{1}{\cos x}$。由 $\lim\dfrac{\sin x}{x}=1$、$\lim\dfrac{\cos x-1}{x^2}=-\dfrac{1}{2}$（eval-calc-001）、$\lim\dfrac{1}{\cos x}=1$，得原式 $=1\cdot\left(-\dfrac{1}{2}\right)\cdot 1=-\dfrac{1}{2}$。

**答案原文**

$-\dfrac{1}{2}$

## 11. eval-calc-004-s2

内容 SHA256：`594cc33168c1a8e0dd60f5a6b95e53d2125b554c444307fad053a6f50ec81ee2`。

来源：data/v2/eval/dataset_eval.jsonl，第 11 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求极限 $\displaystyle\lim_{x\to 0}\frac{\sin x-\tan x}{x^3}$。

**过程**

$\sin x = x-\dfrac{x^3}{6}+o(x^3)$，$\tan x = x+\dfrac{x^3}{3}+o(x^3)$，故 $\sin x-\tan x = -\dfrac{x^3}{2}+o(x^3)$，原式 $=-\dfrac{1}{2}$。

**答案原文**

$-\dfrac{1}{2}$

## 12. eval-calc-004-s3

内容 SHA256：`3a845249579603b5e2987d90fac09c67c5e050363faff9d8c45d78d136d4a22f`。

来源：data/v2/eval/dataset_eval.jsonl，第 12 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求极限 $\displaystyle\lim_{x\to 0}\frac{\sin x-\tan x}{x^3}$。

**过程**

$\dfrac{0}{0}$ 型。一阶：$\dfrac{\cos x-\sec^2 x}{3x^2}$；二阶：$\dfrac{-\sin x-2\sec^2 x\tan x}{6x}$；三阶：$\dfrac{-\cos x-2(2\sec^2 x\tan^2 x+\sec^4 x)}{6}\to \dfrac{-1-2}{6}=-\dfrac{1}{2}$。

**答案原文**

$-\dfrac{1}{2}$

## 13. eval-calc-005-s1

内容 SHA256：`0f5d0b75f0d597a00f069a18dfc46ec6694b55dd305a5d1d897741792d680acf`。

来源：data/v2/eval/dataset_eval.jsonl，第 13 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求函数 $y=x^x$（$x>0$）的导数。

**过程**

两边取对数：$\ln y=x\ln x$。两边对 $x$ 求导：$\dfrac{y'}{y}=\ln x+1$。故 $y'=y(\ln x+1)=x^x(\ln x+1)$。

**答案原文**

$y'=x^x(\ln x+1)$

## 14. eval-calc-005-s2

内容 SHA256：`080a074e0cf67f97f3a89ca78667be4e19247cc1daa4c421aa22ac1eabe0412c`。

来源：data/v2/eval/dataset_eval.jsonl，第 14 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求函数 $y=x^x$（$x>0$）的导数。

**过程**

令 $F(x,y)=\ln y-x\ln x=0$。由隐函数求导公式 $y'=-\dfrac{F_x}{F_y}=-\dfrac{-(\ln x+1)}{1/y}=y(\ln x+1)=x^x(\ln x+1)$。

**答案原文**

$y'=x^x(\ln x+1)$

## 15. eval-calc-005-s3

内容 SHA256：`db6b84306caf6984e5a43c2c752a1c101b0de4755eadc1a5ab0c762e4f03fe4d`。

来源：data/v2/eval/dataset_eval.jsonl，第 15 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求函数 $y=x^x$（$x>0$）的导数。

**过程**

$x^x=e^{x\ln x}$，故 $y'=e^{x\ln x}\cdot(x\ln x)'=x^x(\ln x+1)$。

**答案原文**

$y'=x^x(\ln x+1)$

## 16. eval-calc-006-s1

内容 SHA256：`80f9708f93a313f532ff98b477abd0155172bff9757f395881fa957213a7945f`。

来源：data/v2/eval/dataset_eval.jsonl，第 16 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求函数 $y=\ln(x+\sqrt{x^2+a^2})$（$a>0$）的导数，并说明其反函数。

**过程**

$y'=\dfrac{1+\dfrac{x}{\sqrt{x^2+a^2}}}{x+\sqrt{x^2+a^2}}=\dfrac{\sqrt{x^2+a^2}+x}{\sqrt{x^2+a^2}\cdot(x+\sqrt{x^2+a^2})}=\dfrac{1}{\sqrt{x^2+a^2}}$。

**答案原文**

$y'=\dfrac{1}{\sqrt{x^2+a^2}}$；反函数为 $x=a\sinh(y-\ln a)=\dfrac{e^y-a^2e^{-y}}{2}$

## 17. eval-calc-006-s2

内容 SHA256：`3829a68ad01931b633a3a47389fab8d657cbeae006bf5cf649cd88c5f1e2ed68`。

来源：data/v2/eval/dataset_eval.jsonl，第 17 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求函数 $y=\ln(x+\sqrt{x^2+a^2})$（$a>0$）的导数，并说明其反函数。

**过程**

令 $x=a\sinh t$，则 $x+\sqrt{x^2+a^2}=a(\sinh t+\cosh t)=a e^t$，故 $y=\ln(ae^t)=t+\ln a$，即 $y=\operatorname{arsinh}\dfrac{x}{a}+\ln a$。由反双曲函数求导公式 $(\operatorname{arsinh} u)'=\dfrac{u'}{\sqrt{1+u^2}}$，得 $y'=\dfrac{1/a}{\sqrt{1+x^2/a^2}}=\dfrac{1}{\sqrt{x^2+a^2}}$。

**答案原文**

$y'=\dfrac{1}{\sqrt{x^2+a^2}}$；反函数为 $x=a\sinh(y-\ln a)=\dfrac{e^y-a^2e^{-y}}{2}$

## 18. eval-calc-006-s3

内容 SHA256：`8f6010e8f01bf289d1754c5bed862a1d88b3a968da4eae7fa91005c809ef3848`。

来源：data/v2/eval/dataset_eval.jsonl，第 18 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求函数 $y=\ln(x+\sqrt{x^2+a^2})$（$a>0$）的导数，并说明其反函数。

**过程**

由 $y=\ln(x+\sqrt{x^2+a^2})$ 解出 $x$：$e^y=x+\sqrt{x^2+a^2}$，移项平方得 $e^{2y}-2xe^y=a^2$，故 $x=\dfrac{e^y-a^2e^{-y}}{2}=a\sinh(y-\ln a)$。于是 $\dfrac{dx}{dy}=a\cosh(y-\ln a)=\sqrt{x^2+a^2}$，故 $\dfrac{dy}{dx}=\dfrac{1}{\sqrt{x^2+a^2}}$。

**答案原文**

$y'=\dfrac{1}{\sqrt{x^2+a^2}}$；反函数为 $x=a\sinh(y-\ln a)=\dfrac{e^y-a^2e^{-y}}{2}$

## 19. eval-calc-007-s1

内容 SHA256：`2719db4dc9303017f4e751a4d16d948d849367cdc1d4a874b6ae9b0f569f57ad`。

来源：data/v2/eval/dataset_eval.jsonl，第 19 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设星形线参数方程为 $x=a\cos^3 t$，$y=a\sin^3 t$（$a>0$，$0\le t\le 2\pi$），求 $\dfrac{dy}{dx}$ 与 $\dfrac{d^2y}{dx^2}$。

**过程**

$\dfrac{dx}{dt}=-3a\cos^2 t\sin t$，$\dfrac{dy}{dt}=3a\sin^2 t\cos t$，故 $\dfrac{dy}{dx}=\dfrac{3a\sin^2t\cos t}{-3a\cos^2t\sin t}=-\tan t$。二阶导：$\dfrac{d^2y}{dx^2}=\dfrac{d}{dt}\left(\dfrac{dy}{dx}\right)\Big/\dfrac{dx}{dt}=\dfrac{-\sec^2 t}{-3a\cos^2 t\sin t}=\dfrac{1}{3a\cos^4 t\sin t}$。

**答案原文**

$\dfrac{dy}{dx}=-\tan t$；$\dfrac{d^2y}{dx^2}=\dfrac{1}{3a\cos^4 t\sin t}$（两式仅在光滑分支上成立，即 $\sin t\cos t\ne 0$；在尖点 $t=k\dfrac{\pi}{2}$ 处切线竖直或水平、二阶导不存在，需单独作单侧讨论）

## 20. eval-calc-007-s2

内容 SHA256：`1a5434893e4dc5e492359491d3db086042fc167e391b4ea41d9045809a3b0293`。

来源：data/v2/eval/dataset_eval.jsonl，第 20 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设星形线参数方程为 $x=a\cos^3 t$，$y=a\sin^3 t$（$a>0$，$0\le t\le 2\pi$），求 $\dfrac{dy}{dx}$ 与 $\dfrac{d^2y}{dx^2}$。

**过程**

消去参数：$x^{2/3}+y^{2/3}=a^{2/3}$。两边对 $x$ 求导：$\dfrac{2}{3}x^{-1/3}+\dfrac{2}{3}y^{-1/3}y'=0$，故 $y'=-\left(\dfrac{y}{x}\right)^{1/3}=-\tan t$。再对 $x$ 求导：$y''=-\dfrac{1}{3}\left(\dfrac{y}{x}\right)^{-2/3}\cdot\dfrac{y'x-y}{x^2}$。代入 $x=a\cos^3 t$、$y=a\sin^3 t$、$y'=-\tan t$：$\left(\dfrac{y}{x}\right)^{2/3}=\tan^2 t$，且 $y'x-y=-\tan t\cdot a\cos^3 t-a\sin^3 t=-a\sin t(\cos^2 t+\sin^2 t)=-a\sin t$。故 $y''=-\dfrac{1}{3}\cot^2 t\cdot\dfrac{-a\sin t}{a^2\cos^6 t}=\dfrac{1}{3a\cos^4 t\sin t}$，与解法一一致。

**答案原文**

$\dfrac{dy}{dx}=-\tan t$；$\dfrac{d^2y}{dx^2}=\dfrac{1}{3a\cos^4 t\sin t}$（两式仅在光滑分支上成立，即 $\sin t\cos t\ne 0$；在尖点 $t=k\dfrac{\pi}{2}$ 处切线竖直或水平、二阶导不存在，需单独作单侧讨论）

## 21. eval-calc-007-s3

内容 SHA256：`4c50163271ae0d8d082eee9eebe7ef8720e8dd03164bc3ca6b062c2197972964`。

来源：data/v2/eval/dataset_eval.jsonl，第 21 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设星形线参数方程为 $x=a\cos^3 t$，$y=a\sin^3 t$（$a>0$，$0\le t\le 2\pi$），求 $\dfrac{dy}{dx}$ 与 $\dfrac{d^2y}{dx^2}$。

**过程**

在参数点 $(a\cos^3 t, a\sin^3 t)$ 处，切线方程为 $y-a\sin^3 t=-\tan t\,(x-a\cos^3 t)$。令 $y=0$ 求 $x$ 截距：$\tan t\,x=a\sin^3 t+\tan t\cdot a\cos^3 t=a\sin t(\sin^2 t+\cos^2 t)=a\sin t$，故 $x=a\cos t$；令 $x=0$ 得 $y$ 截距 $y=a\sin^3 t+\tan t\cdot a\cos^3 t=a\sin t$。于是切线与两坐标轴交点间的线段长恒为 $\sqrt{a^2\cos^2 t+a^2\sin^2 t}=a$，且切线斜率恰为 $\dfrac{-a\sin t}{a\cos t}=-\tan t$，与解法一一致。二阶导 $y''$ 则描述这条定长切线随 $t$ 转动的速率（解法一已算出 $\dfrac{1}{3a\cos^4 t\sin t}$）。

**答案原文**

$\dfrac{dy}{dx}=-\tan t$；$\dfrac{d^2y}{dx^2}=\dfrac{1}{3a\cos^4 t\sin t}$（两式仅在光滑分支上成立，即 $\sin t\cos t\ne 0$；在尖点 $t=k\dfrac{\pi}{2}$ 处切线竖直或水平、二阶导不存在，需单独作单侧讨论）

## 22. eval-calc-008-s1

内容 SHA256：`619a2c008146141383fbd8e4d66bc6c555e9ce56f3d7d4ac5e4a8ad234ac53d3`。

来源：data/v2/eval/dataset_eval.jsonl，第 22 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

证明：当 $x>0$ 时，$e^x>1+x$。

**过程**

令 $f(x)=e^x-1-x$，则 $f'(x)=e^x-1>0$（$x>0$），故 $f$ 在 $[0,+\infty)$ 上严格递增。又 $f(0)=0$，所以当 $x>0$ 时 $f(x)>f(0)=0$，即 $e^x>1+x$。

**答案原文**

证毕（三种证法）

## 23. eval-calc-008-s2

内容 SHA256：`10fc3b63ac79540ccf7cbb3ac225bfde0ab7cd2d51d58b882529079c1cc6c4c2`。

来源：data/v2/eval/dataset_eval.jsonl，第 23 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

证明：当 $x>0$ 时，$e^x>1+x$。

**过程**

对 $f(x)=e^x$ 在 $[0,x]$ 上用拉格朗日中值定理：存在 $\xi\in(0,x)$ 使 $e^x-e^0=e^\xi(x-0)$。因 $\xi>0$，$e^\xi>1$，故 $e^x-1=e^\xi x>x$，即 $e^x>1+x$。

**答案原文**

证毕（三种证法）

## 24. eval-calc-008-s3

内容 SHA256：`33712a953ac25c3bbfde490fd7566107e1123f3b7847c0eed422f2b69d76788f`。

来源：data/v2/eval/dataset_eval.jsonl，第 24 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

证明：当 $x>0$ 时，$e^x>1+x$。

**过程**

$e^x=1+x+\dfrac{x^2}{2}e^\eta$，其中 $\eta\in(0,x)$。因 $\dfrac{x^2}{2}e^\eta>0$，故 $e^x>1+x$。此证法还给出更强的估计 $e^x>1+x+\dfrac{x^2}{2}$。

**答案原文**

证毕（三种证法）

## 25. eval-calc-009-s1

内容 SHA256：`de8c9d5cd7504371c46f4f27ba20f4fc24270d78f3998d3405a2a075b7086470`。

来源：data/v2/eval/dataset_eval.jsonl，第 25 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $0<a<b$，证明：$\arctan b-\arctan a<b-a$。

**过程**

对 $f(x)=\arctan x$ 在 $[a,b]$ 上用中值定理：存在 $\xi\in(a,b)$ 使 $\arctan b-\arctan a=\dfrac{1}{1+\xi^2}(b-a)$。因 $\dfrac{1}{1+\xi^2}<1$，故 $\arctan b-\arctan a<b-a$。

**答案原文**

证毕（三种证法）

## 26. eval-calc-009-s2

内容 SHA256：`9cd589b60c2ad2e830aa6d2362d89353d7a93b729a6c3edcb714236d8fa77476`。

来源：data/v2/eval/dataset_eval.jsonl，第 26 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $0<a<b$，证明：$\arctan b-\arctan a<b-a$。

**过程**

令 $g(x)=x-\arctan x$，则 $g'(x)=1-\dfrac{1}{1+x^2}=\dfrac{x^2}{1+x^2}>0$（$x>0$），故 $g$ 在 $(0,+\infty)$ 上严格递增，$g(b)>g(a)$，即 $b-\arctan b>a-\arctan a$，移项得证。

**答案原文**

证毕（三种证法）

## 27. eval-calc-009-s3

内容 SHA256：`38e40cb341eaa88ebd0470bc17d945761b654618b0c41759931f485e3492f372`。

来源：data/v2/eval/dataset_eval.jsonl，第 27 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $0<a<b$，证明：$\arctan b-\arctan a<b-a$。

**过程**

由 $(\arctan x)'=\dfrac{1}{1+x^2}<1$ 知 $y=\arctan x$ 在 $(0,+\infty)$ 上任意两点连线的斜率小于 1（割线斜率 = 某点导数值 < 1），故 $\dfrac{\arctan b-\arctan a}{b-a}<1$，得证。

**答案原文**

证毕（三种证法）

## 28. eval-calc-010-s1

内容 SHA256：`6e50884aa4541648b17e5b4a1127780984bd9d0f5e36b56935e6d5109da57156`。

来源：data/v2/eval/dataset_eval.jsonl，第 28 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求极限 $\displaystyle\lim_{x\to 0}\frac{e^x-e^{\sin x}}{x-\sin x}$。

**过程**

令 $f(t)=e^t$，对 $f$ 在 $\sin x$ 与 $x$ 之间用中值定理：$e^x-e^{\sin x}=e^\xi(x-\sin x)$，其中 $\xi$ 介于 $\sin x$ 与 $x$ 之间。当 $x\to 0$ 时 $\sin x\to 0$、$x\to 0$，故 $\xi\to 0$。原式 $=\lim_{x\to 0}e^\xi=1$。

**答案原文**

$1$

## 29. eval-calc-010-s2

内容 SHA256：`282616d55bca98edc1742b90ff943674cdbd45a74b5e0019bb96d014c9c58bc7`。

来源：data/v2/eval/dataset_eval.jsonl，第 29 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求极限 $\displaystyle\lim_{x\to 0}\frac{e^x-e^{\sin x}}{x-\sin x}$。

**过程**

原式 $=\lim_{x\to 0}\dfrac{e^{\sin x}\left(e^{x-\sin x}-1\right)}{x-\sin x}=\lim_{x\to 0}e^{\sin x}\cdot\lim_{x\to 0}\dfrac{e^{x-\sin x}-1}{x-\sin x}=1\cdot 1=1$。

**答案原文**

$1$

## 30. eval-calc-010-s3

内容 SHA256：`fef2ee2b19024e7a3b0e7404165efbf49fe446d16839b9026176a7a553ae0549`。

来源：data/v2/eval/dataset_eval.jsonl，第 30 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求极限 $\displaystyle\lim_{x\to 0}\frac{e^x-e^{\sin x}}{x-\sin x}$。

**过程**

原式为 $\dfrac{0}{0}$ 型。第一次：$\lim_{x\to 0}\dfrac{e^x-e^{\sin x}\cos x}{1-\cos x}$，仍为 $\dfrac{0}{0}$ 型。第二次：分子求导得 $e^x-e^{\sin x}\cos^2 x+e^{\sin x}\sin x$，分母求导得 $\sin x$，仍为 $\dfrac{0}{0}$ 型。第三次：分子再求导为 $e^x-e^{\sin x}(\cos^3 x-2\sin x\cos x)+e^{\sin x}\cos x(\sin x+1)$，分母求导为 $\cos x$。令 $x\to 0$：分子 $\to 1-1\cdot(1-0)+1\cdot 1\cdot(0+1)=1$，分母 $\to 1$，故极限为 $\dfrac{1}{1}=1$。此路可通但三次求导冗长，恰好反衬解法一的一步到位。

**答案原文**

$1$

## 31. eval-calc-011-s1

内容 SHA256：`17ac66177d857004add01ccc1d6ce3bf67a8d1ab92f6fa0e04bbda364838e07e`。

来源：data/v2/eval/dataset_eval.jsonl，第 31 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

用多种方法求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\cdot 2^n}$ 的和。

**过程**

由 $-\ln(1-x)=\displaystyle\int_0^x\dfrac{dt}{1-t}=\int_0^x\sum_{n=0}^{\infty}t^n\,dt=\sum_{n=1}^{\infty}\dfrac{x^n}{n}=x+\dfrac{x^2}{2}+\dfrac{x^3}{3}+\cdots$（$|x|<1$），取 $x=\dfrac{1}{2}$，得 $\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{n\cdot 2^n}=-\ln\left(1-\dfrac{1}{2}\right)=-\ln\dfrac{1}{2}=\ln 2$。

**答案原文**

$\ln 2$

## 32. eval-calc-011-s2

内容 SHA256：`bd18b8e41624120013aab378656982f1e99649d140a1a3e3742012e406bafe56`。

来源：data/v2/eval/dataset_eval.jsonl，第 32 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

用多种方法求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\cdot 2^n}$ 的和。

**过程**

由 $\dfrac{1}{n\cdot 2^n}=\displaystyle\int_0^{1/2}x^{n-1}\,dx$（把 $\dfrac{1}{2^n}$ 看作幂的积分），故 $S=\displaystyle\sum_{n=1}^{\infty}\int_0^{1/2}x^{n-1}dx=\int_0^{1/2}\sum_{n=1}^{\infty}x^{n-1}dx=\int_0^{1/2}\dfrac{dx}{1-x}=\left[-\ln(1-x)\right]_0^{1/2}=\ln 2$（求和与积分可交换由正项级数单调收敛保证）。

**答案原文**

$\ln 2$

## 33. eval-calc-011-s3

内容 SHA256：`63dda2ed12752db4e444446468a340f0867ed4f13ed71b4f3bbd3a4139ab818c`。

来源：data/v2/eval/dataset_eval.jsonl，第 33 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

用多种方法求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\cdot 2^n}$ 的和。

**过程**

设 $f(x)=\displaystyle\sum_{n=1}^{\infty}\dfrac{x^n}{n}$，逐项求导得 $f'(x)=\displaystyle\sum_{n=1}^{\infty}x^{n-1}=\dfrac{1}{1-x}$（$|x|<1$），且 $f(0)=0$，故 $f(x)=-\ln(1-x)$，取 $x=\dfrac{1}{2}$ 得 $\ln 2$。

**答案原文**

$\ln 2$

## 34. eval-calc-012-s1

内容 SHA256：`da60b5b2234745e21af07d9de667916da1be46d236c239ddc2064d2e0b564d09`。

来源：data/v2/eval/dataset_eval.jsonl，第 34 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求 $\tan 15^\circ$ 的精确值。

**过程**

$\tan 15^\circ=\tan(45^\circ-30^\circ)=\dfrac{\tan 45^\circ-\tan 30^\circ}{1+\tan 45^\circ\tan 30^\circ}=\dfrac{1-\frac{\sqrt{3}}{3}}{1+\frac{\sqrt{3}}{3}}=\dfrac{3-\sqrt{3}}{3+\sqrt{3}}$。分子分母同乘 $3-\sqrt{3}$：$\dfrac{(3-\sqrt{3})^2}{9-3}=\dfrac{12-6\sqrt{3}}{6}=2-\sqrt{3}$。

**答案原文**

$2-\sqrt{3}$

## 35. eval-calc-012-s2

内容 SHA256：`64a4d0c3b4473b1554b275fcf3e1bc3897be473df020ea7b1ccba339130caeff`。

来源：data/v2/eval/dataset_eval.jsonl，第 35 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求 $\tan 15^\circ$ 的精确值。

**过程**

$\tan 15^\circ=\tan\dfrac{30^\circ}{2}=\dfrac{1-\cos 30^\circ}{\sin 30^\circ}=\dfrac{1-\frac{\sqrt{3}}{2}}{\frac{1}{2}}=2-\sqrt{3}$。

**答案原文**

$2-\sqrt{3}$

## 36. eval-calc-012-s3

内容 SHA256：`a6a1bde9531e84aeb73cdd0e390a44dcc4cb69e9945bf485a5aaac7d206da19f`。

来源：data/v2/eval/dataset_eval.jsonl，第 36 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求 $\tan 15^\circ$ 的精确值。

**过程**

用 $30^\circ$-$60^\circ$-$90^\circ$ 三角形（边长 $1:\sqrt3:2$）拼出宽 $1$、长 $2+\sqrt3$ 的矩形：长边由"长直角边 $\sqrt3$ 与斜边 $2$ 首尾相接"构成，宽取短直角边 $1$。该矩形的对角线与长边的夹角 $\alpha$ 满足 $\tan\alpha=\dfrac{1}{2+\sqrt3}$。分母有理化：$\dfrac{1}{2+\sqrt3}=\dfrac{2-\sqrt3}{(2+\sqrt3)(2-\sqrt3)}=2-\sqrt3$。由解法一 $\tan 15^\circ=2-\sqrt3$，且 $0<\alpha<90^\circ$ 内正切一一对应，故 $\alpha=15^\circ$。此构造同时给出 $\tan 75^\circ=2+\sqrt3$。

**答案原文**

$2-\sqrt{3}$

## 37. eval-calc-013-s1

内容 SHA256：`7f93b13fbec4b29b07aa07f6b076432961d5445829c10ba8e83ed9d1ed62a454`。

来源：data/v2/eval/dataset_eval.jsonl，第 37 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求不定积分 $\displaystyle\int x^2e^x\,dx$。

**过程**

第一次：$\int x^2e^xdx=x^2e^x-2\int xe^xdx$。第二次：$\int xe^xdx=xe^x-\int e^xdx=(x-1)e^x$。故原式 $=x^2e^x-2(x-1)e^x+C=(x^2-2x+2)e^x+C$。

**答案原文**

$(x^2-2x+2)e^x+C$

## 38. eval-calc-013-s2

内容 SHA256：`f7b90865303d9f6b75d7f5ae70417c68a6dd8d3cfebec3da88f18f12e02ddb73`。

来源：data/v2/eval/dataset_eval.jsonl，第 38 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求不定积分 $\displaystyle\int x^2e^x\,dx$。

**过程**

因被积函数是 $x^2e^x$，设原函数为 $(ax^2+bx+c)e^x$。求导比对：$\left[(ax^2+bx+c)e^x\right]'=\left[ax^2+(2a+b)x+(b+c)\right]e^x\equiv x^2e^x$，故 $a=1$，$2a+b=0\Rightarrow b=-2$，$b+c=0\Rightarrow c=2$，得 $(x^2-2x+2)e^x$。

**答案原文**

$(x^2-2x+2)e^x+C$

## 39. eval-calc-013-s3

内容 SHA256：`af15b359050acf7835e796b04a50eebc5d519259ac6e3db5e8570f0e161d3e60`。

来源：data/v2/eval/dataset_eval.jsonl，第 39 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求不定积分 $\displaystyle\int x^2e^x\,dx$。

**过程**

记 $I_n=\int x^ne^xdx$，分部得 $I_n=x^ne^x-nI_{n-1}$。$I_0=e^x$，$I_1=xe^x-I_0=(x-1)e^x$，$I_2=x^2e^x-2I_1=(x^2-2x+2)e^x$。

**答案原文**

$(x^2-2x+2)e^x+C$

## 40. eval-calc-014-s1

内容 SHA256：`a4af239fc8b6e7522c52fd526391cc1662b54c862020a7a2b01a8783caea8d6b`。

来源：data/v2/eval/dataset_eval.jsonl，第 40 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求不定积分 $\displaystyle\int\dfrac{dx}{\sin x}$，并说明不同形式答案的等价性。

**过程**

$\dfrac{1}{\sin x}=\dfrac{1}{2\sin\frac{x}{2}\cos\frac{x}{2}}=\dfrac{\dfrac{1}{2}\sec^2\frac{x}{2}}{\tan\frac{x}{2}}$。故 $\int\dfrac{dx}{\sin x}=\int\dfrac{d\left(\tan\frac{x}{2}\right)}{\tan\frac{x}{2}}=\ln\left|\tan\dfrac{x}{2}\right|+C$。

**答案原文**

$\ln\left|\tan\dfrac{x}{2}\right|+C$（等价于 $\ln|\csc x-\cot x|+C$）

## 41. eval-calc-014-s2

内容 SHA256：`2d0da070af03e3f6c1d9378d4932ff772a621ddf9121c88a2d105b870fc06b60`。

来源：data/v2/eval/dataset_eval.jsonl，第 41 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求不定积分 $\displaystyle\int\dfrac{dx}{\sin x}$，并说明不同形式答案的等价性。

**过程**

令 $t=\tan\dfrac{x}{2}$，则 $\sin x=\dfrac{2t}{1+t^2}$，$dx=\dfrac{2dt}{1+t^2}$。原式 $=\int\dfrac{1+t^2}{2t}\cdot\dfrac{2dt}{1+t^2}=\int\dfrac{dt}{t}=\ln|t|+C=\ln\left|\tan\dfrac{x}{2}\right|+C$。

**答案原文**

$\ln\left|\tan\dfrac{x}{2}\right|+C$（等价于 $\ln|\csc x-\cot x|+C$）

## 42. eval-calc-014-s3

内容 SHA256：`46e87514fff3a98be53baf86362eaac8d407f84579b4e866c888dad288aae820`。

来源：data/v2/eval/dataset_eval.jsonl，第 42 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求不定积分 $\displaystyle\int\dfrac{dx}{\sin x}$，并说明不同形式答案的等价性。

**过程**

分子分母同乘 $\csc x-\cot x$：$\int\csc x\,dx=\int\dfrac{\csc x(\csc x-\cot x)}{\csc x-\cot x}dx=\int\dfrac{d(\csc x-\cot x)}{\csc x-\cot x}=\ln|\csc x-\cot x|+C$。由 $\csc x-\cot x=\dfrac{1-\cos x}{\sin x}=\tan\dfrac{x}{2}$ 知两形式完全相同。

**答案原文**

$\ln\left|\tan\dfrac{x}{2}\right|+C$（等价于 $\ln|\csc x-\cot x|+C$）

## 43. eval-calc-015-s1

内容 SHA256：`6fe1e9b5c4735fc4504c1e29549a137ebbeab0f446cf467d019d19223ff12427`。

来源：data/v2/eval/dataset_eval.jsonl，第 43 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求定积分 $\displaystyle I=\int_0^\pi\frac{x\sin x}{1+\cos^2 x}\,dx$。

**过程**

令 $t=\pi-x$，则 $I=\int_0^\pi\dfrac{(\pi-t)\sin t}{1+\cos^2 t}\,dt=\pi\int_0^\pi\dfrac{\sin t}{1+\cos^2 t}\,dt-I$，故 $2I=\pi\int_0^\pi\dfrac{\sin x}{1+\cos^2 x}\,dx$。令 $u=\cos x$（$du=-\sin x\,dx$）：$\int_0^\pi\dfrac{\sin x}{1+\cos^2x}dx=\int_{-1}^{1}\dfrac{du}{1+u^2}=\left[\arctan u\right]_{-1}^{1}=\dfrac{\pi}{2}$。于是 $2I=\pi\cdot\dfrac{\pi}{2}$，$I=\dfrac{\pi^2}{4}$。

**答案原文**

$\dfrac{\pi^2}{4}$

## 44. eval-calc-015-s2

内容 SHA256：`8c3bf2a0b624b5278fabbc7615d1778c18b79549f9a73ceacf5555b070c9de57`。

来源：data/v2/eval/dataset_eval.jsonl，第 44 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求定积分 $\displaystyle I=\int_0^\pi\frac{x\sin x}{1+\cos^2 x}\,dx$。

**过程**

令 $u=x$、$dv=\dfrac{\sin x}{1+\cos^2x}dx$，则 $v=-\arctan(\cos x)$。$I=\left[-x\arctan(\cos x)\right]_0^\pi+\int_0^\pi\arctan(\cos x)dx$。代入上下限：$-\pi\arctan(-1)+0=\dfrac{\pi^2}{4}$，再结合对称性 $\int_0^\pi\arctan(\cos x)dx=0$（被积函数关于 $x=\dfrac{\pi}{2}$ 反对称），得 $I=\dfrac{\pi^2}{4}$。

**答案原文**

$\dfrac{\pi^2}{4}$

## 45. eval-calc-015-s3

内容 SHA256：`7906671ec84b48fcf609fcb655390127bfdae2a1f9ff971ff5f5fb7fc1cf74e9`。

来源：data/v2/eval/dataset_eval.jsonl，第 45 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求定积分 $\displaystyle I=\int_0^\pi\frac{x\sin x}{1+\cos^2 x}\,dx$。

**过程**

用辛普森法或等距分割近似计算 $I$（如 $n=1000$ 区间），得到 $2.467401\cdots$，与 $\dfrac{\pi^2}{4}\approx2.4674011$ 吻合，作为解析结果的独立校验。

**答案原文**

$\dfrac{\pi^2}{4}$

## 46. eval-calc-016-s1

内容 SHA256：`033316474d0f9c54e66723248ed1ed6ec0aa08682af9d8dca2e239867cf79960`。

来源：data/v2/eval/dataset_eval.jsonl，第 46 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求不定积分 $\displaystyle\int\frac{dx}{(x^2+a^2)^2}$（$a>0$）。

**过程**

令 $x=a\tan t$，则 $dx=a\sec^2 t\,dt$，$x^2+a^2=a^2\sec^2 t$。原式 $=\displaystyle\int\dfrac{a\sec^2 t}{a^4\sec^4 t}dt=\dfrac{1}{a^3}\int\cos^2 t\,dt=\dfrac{1}{a^3}\left(\dfrac{t}{2}+\dfrac{\sin 2t}{4}\right)+C=\dfrac{1}{a^3}\left(\dfrac{t}{2}+\dfrac{\sin t\cos t}{2}\right)+C$。由直角三角形得 $\sin t=\dfrac{x}{\sqrt{x^2+a^2}}$、$\cos t=\dfrac{a}{\sqrt{x^2+a^2}}$，故原式 $=\dfrac{1}{2a^3}\arctan\dfrac{x}{a}+\dfrac{x}{2a^2(x^2+a^2)}+C$。

**答案原文**

$\dfrac{x}{2a^2(x^2+a^2)}+\dfrac{1}{2a^3}\arctan\dfrac{x}{a}+C$

## 47. eval-calc-016-s2

内容 SHA256：`0021cdaa64044d3a95eb6567d341007ab9fa2434b46a4ba143e110ef19217171`。

来源：data/v2/eval/dataset_eval.jsonl，第 47 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求不定积分 $\displaystyle\int\frac{dx}{(x^2+a^2)^2}$（$a>0$）。

**过程**

记 $I_n=\displaystyle\int\dfrac{dx}{(x^2+a^2)^n}$。对 $I_n$ 分部积分（取 $u=\dfrac{1}{(x^2+a^2)^n}$、$dv=dx$）：$I_n=\dfrac{x}{(x^2+a^2)^n}+2n\displaystyle\int\dfrac{x^2}{(x^2+a^2)^{n+1}}dx=\dfrac{x}{(x^2+a^2)^n}+2n\int\dfrac{(x^2+a^2)-a^2}{(x^2+a^2)^{n+1}}dx=\dfrac{x}{(x^2+a^2)^n}+2n(I_n-a^2I_{n+1})$。整理得递推式 $I_{n+1}=\dfrac{1}{2na^2}\left[\dfrac{x}{(x^2+a^2)^n}+(2n-1)I_n\right]$。取 $n=1$ 并以 $I_1=\dfrac{1}{a}\arctan\dfrac{x}{a}$ 代入：$I_2=\dfrac{1}{2a^2}\left[\dfrac{x}{x^2+a^2}+I_1\right]=\dfrac{x}{2a^2(x^2+a^2)}+\dfrac{1}{2a^3}\arctan\dfrac{x}{a}+C$。

**答案原文**

$\dfrac{x}{2a^2(x^2+a^2)}+\dfrac{1}{2a^3}\arctan\dfrac{x}{a}+C$

## 48. eval-calc-016-s3

内容 SHA256：`9efa83002572cc34b3cf4b95ab460ac0c54a61dd4c84317123df3ba8988ab017`。

来源：data/v2/eval/dataset_eval.jsonl，第 48 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求不定积分 $\displaystyle\int\frac{dx}{(x^2+a^2)^2}$（$a>0$）。

**过程**

在复数域 $f(z)=\dfrac{1}{(z^2+a^2)^2}=\dfrac{1}{(z-ai)^2(z+ai)^2}$，实系数保证共轭对称。求系数：$C=\lim_{z\to ai}(z-ai)^2f(z)=\dfrac{1}{(2ai)^2}=-\dfrac{1}{4a^2}$；$D=\lim_{z\to ai}\dfrac{d}{dz}\dfrac{1}{(z+ai)^2}=\dfrac{-2}{(2ai)^3}=\dfrac{1}{4a^3i}=-\dfrac{i}{4a^3}$，共轭 $\bar D=\dfrac{i}{4a^3}$。故 $\dfrac{1}{(x^2+a^2)^2}=-\dfrac{1}{4a^2}\left[\dfrac{1}{(x-ai)^2}+\dfrac{1}{(x+ai)^2}\right]-\dfrac{i}{4a^3}\cdot\dfrac{1}{x-ai}+\dfrac{i}{4a^3}\cdot\dfrac{1}{x+ai}$。逐项积分：第一组 $=\dfrac{1}{4a^2}\left[\dfrac{1}{x-ai}+\dfrac{1}{x+ai}\right]=\dfrac{x}{2a^2(x^2+a^2)}$；第二组 $=\dfrac{i}{4a^3}\left[\ln(x+ai)-\ln(x-ai)\right]=\dfrac{i}{4a^3}\ln\dfrac{x+ai}{x-ai}$。对实数 $x>0$，$|x+ai|=|x-ai|$，且 $\arg\dfrac{x+ai}{x-ai}=2\arg(x+ai)=2\left(\dfrac{\pi}{2}-\arctan\dfrac{x}{a}\right)=\pi-2\arctan\dfrac{x}{a}$，故第二组 $=\dfrac{i}{4a^3}\cdot i\left(\pi-2\arctan\dfrac{x}{a}\right)=\dfrac{1}{2a^3}\arctan\dfrac{x}{a}-\dfrac{\pi}{4a^3}$（常数并入 $C$）；当 $x<0$ 时上述辐角公式超出主值范围，需沿实轴选取连续对数分支，分支差异为常数、并入 $C$ 后不影响原函数（也可分 $x>0$ 与 $x<0$ 两区间分别计算）。合并得 $\dfrac{x}{2a^2(x^2+a^2)}+\dfrac{1}{2a^3}\arctan\dfrac{x}{a}+C$，三法一致。

**答案原文**

$\dfrac{x}{2a^2(x^2+a^2)}+\dfrac{1}{2a^3}\arctan\dfrac{x}{a}+C$

## 49. eval-calc-017-s1

内容 SHA256：`5066f6f120c76d3b9e5b40f980cd4eb9e9391d9ff1d9a982cc43dfbac9fb1dad`。

来源：data/v2/eval/dataset_eval.jsonl，第 49 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求定积分 $\displaystyle I=\int_0^1\frac{\ln(1+x)}{1+x^2}\,dx$。

**过程**

令 $x=\tan t$（$t:0\to\dfrac{\pi}{4}$），则 $I=\displaystyle\int_0^{\pi/4}\ln(1+\tan t)\,dt$。利用区间替换 $t\to\dfrac{\pi}{4}-t$：$I=\displaystyle\int_0^{\pi/4}\ln\left(1+\tan\left(\frac{\pi}{4}-t\right)\right)dt$。由和角公式 $\tan\left(\dfrac{\pi}{4}-t\right)=\dfrac{1-\tan t}{1+\tan t}$，得 $1+\tan\left(\dfrac{\pi}{4}-t\right)=\dfrac{2}{1+\tan t}$。两式相加：$2I=\displaystyle\int_0^{\pi/4}\left[\ln(1+\tan t)+\ln\dfrac{2}{1+\tan t}\right]dt=\int_0^{\pi/4}\ln 2\,dt=\dfrac{\pi}{4}\ln 2$，故 $I=\dfrac{\pi}{8}\ln 2$。

**答案原文**

$\dfrac{\pi}{8}\ln 2$

## 50. eval-calc-017-s2

内容 SHA256：`135c818004bb993ec0a799b7f996606f27cdeeba4a2db8c3f570b9d2fabe3429`。

来源：data/v2/eval/dataset_eval.jsonl，第 50 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求定积分 $\displaystyle I=\int_0^1\frac{\ln(1+x)}{1+x^2}\,dx$。

**过程**

令 $x=\dfrac{1-t}{1+t}$（$t:1\to 0$），则 $dx=-\dfrac{2}{(1+t)^2}dt$，且 $1+x=\dfrac{2}{1+t}$、$1+x^2=\dfrac{2(1+t^2)}{(1+t)^2}$。代入得 $I=\displaystyle\int_1^0\dfrac{\ln\frac{2}{1+t}}{\frac{2(1+t^2)}{(1+t)^2}}\cdot\left(-\dfrac{2}{(1+t)^2}\right)dt=\int_0^1\dfrac{\ln 2-\ln(1+t)}{1+t^2}\,dt=\ln 2\int_0^1\dfrac{dt}{1+t^2}-I=\dfrac{\pi}{4}\ln 2-I$（其中 $\int_0^1\dfrac{dt}{1+t^2}=\left[\arctan t\right]_0^1=\dfrac{\pi}{4}$）。故 $2I=\dfrac{\pi}{4}\ln 2$，$I=\dfrac{\pi}{8}\ln 2$。

**答案原文**

$\dfrac{\pi}{8}\ln 2$

## 51. eval-calc-017-s3

内容 SHA256：`d2ebe9ccd20774250cd501090416f060db2769efaa11650588a1bc005a23dc24`。

来源：data/v2/eval/dataset_eval.jsonl，第 51 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求定积分 $\displaystyle I=\int_0^1\frac{\ln(1+x)}{1+x^2}\,dx$。

**过程**

取 $u=\ln(1+x)$、$dv=\dfrac{dx}{1+x^2}$，则 $v=\arctan x$。$I=\left[\ln(1+x)\arctan x\right]_0^1-\displaystyle\int_0^1\dfrac{\arctan x}{1+x}\,dx=\dfrac{\pi}{4}\ln 2-J$，其中 $J=\displaystyle\int_0^1\dfrac{\arctan x}{1+x}dx$。对 $J$ 作替换 $x=\dfrac{1-t}{1+t}$：$dx=-\dfrac{2}{(1+t)^2}dt$，$1+x=\dfrac{2}{1+t}$，且 $\arctan\dfrac{1-t}{1+t}=\dfrac{\pi}{4}-\arctan t$（$t\in[0,1]$，由 $\tan\left(\dfrac{\pi}{4}-\arctan t\right)=\dfrac{1-t}{1+t}$ 得）。故 $J=\displaystyle\int_1^0\left(\frac{\pi}{4}-\arctan t\right)\cdot\frac{1+t}{2}\cdot\left(-\frac{2}{(1+t)^2}\right)dt=\int_0^1\dfrac{\frac{\pi}{4}-\arctan t}{1+t}\,dt=\dfrac{\pi}{4}\ln 2-J$，得 $2J=\dfrac{\pi}{4}\ln 2$，$J=\dfrac{\pi}{8}\ln 2$。于是 $I=\dfrac{\pi}{4}\ln 2-\dfrac{\pi}{8}\ln 2=\dfrac{\pi}{8}\ln 2$。

**答案原文**

$\dfrac{\pi}{8}\ln 2$

## 52. eval-calc-018-s1

内容 SHA256：`b4d0a85bd17e7889e8898d6403b8b1e82117debc776ac60edc193ea9852c31b1`。

来源：data/v2/eval/dataset_eval.jsonl，第 52 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求不定积分 $\displaystyle\int x\arctan x\,dx$。

**过程**

令 $u=\arctan x$、$dv=x\,dx$，则 $du=\dfrac{dx}{1+x^2}$、$v=\dfrac{x^2}{2}$。原式 $=\dfrac{x^2}{2}\arctan x-\dfrac{1}{2}\displaystyle\int\dfrac{x^2}{1+x^2}dx=\dfrac{x^2}{2}\arctan x-\dfrac{1}{2}\int\left(1-\dfrac{1}{1+x^2}\right)dx=\dfrac{x^2}{2}\arctan x-\dfrac{x}{2}+\dfrac{1}{2}\arctan x+C=\dfrac{x^2+1}{2}\arctan x-\dfrac{x}{2}+C$。

**答案原文**

$\dfrac{x^2+1}{2}\arctan x-\dfrac{x}{2}+C$

## 53. eval-calc-018-s2

内容 SHA256：`22d8cd478620dc2a23932e4a4ba2518b9169ec89073c17cdbad67101178b55c2`。

来源：data/v2/eval/dataset_eval.jsonl，第 53 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求不定积分 $\displaystyle\int x\arctan x\,dx$。

**过程**

令 $t=\arctan x$，则 $x=\tan t$、$dx=\sec^2 t\,dt$。原式 $=\displaystyle\int t\tan t\sec^2 t\,dt=\dfrac{1}{2}\int t\,d(\tan^2 t)=\dfrac{1}{2}t\tan^2 t-\dfrac{1}{2}\int\tan^2 t\,dt=\dfrac{1}{2}t\tan^2 t-\dfrac{1}{2}\int(\sec^2 t-1)dt=\dfrac{1}{2}t(1+\tan^2 t)-\dfrac{1}{2}\tan t+C$。代回 $t=\arctan x$、$\tan t=x$，得 $\dfrac{x^2+1}{2}\arctan x-\dfrac{x}{2}+C$。

**答案原文**

$\dfrac{x^2+1}{2}\arctan x-\dfrac{x}{2}+C$

## 54. eval-calc-018-s3

内容 SHA256：`83aeb8f4544ba57bba5909abdde91dcec4544bf8610f39c8967ab7bef22eabf2`。

来源：data/v2/eval/dataset_eval.jsonl，第 54 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求不定积分 $\displaystyle\int x\arctan x\,dx$。

**过程**

令 $u=x\arctan x$、$dv=dx$，则 $v=x$、$du=\left(\arctan x+\dfrac{x}{1+x^2}\right)dx$。原式 $=x^2\arctan x-\displaystyle\int x\arctan x\,dx-\int\dfrac{x^2}{1+x^2}dx$，即 $2I=x^2\arctan x-\displaystyle\int\left(1-\dfrac{1}{1+x^2}\right)dx=x^2\arctan x-x+\arctan x$，故 $I=\dfrac{x^2+1}{2}\arctan x-\dfrac{x}{2}+C$。

**答案原文**

$\dfrac{x^2+1}{2}\arctan x-\dfrac{x}{2}+C$

## 55. eval-calc-019-s1

内容 SHA256：`26a6cfd06f606d8bc37c104b8b9a44054ac5131f648f2cf131ca2ff8141925e9`。

来源：data/v2/eval/dataset_eval.jsonl，第 55 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求反常积分 $\displaystyle\int_0^{+\infty}xe^{-x}\,dx$。

**过程**

先求原函数：令 $u=x$、$dv=e^{-x}dx$，则 $du=dx$、$v=-e^{-x}$，$\displaystyle\int xe^{-x}dx=-xe^{-x}+\int e^{-x}dx=-(x+1)e^{-x}+C$。故 $\displaystyle\int_0^{b}xe^{-x}dx=\left[-(x+1)e^{-x}\right]_0^b=1-(b+1)e^{-b}$。令 $b\to+\infty$：$(b+1)e^{-b}\to 0$（指数衰减快于线性增长），得原积分 $=1$。

**答案原文**

$1$

## 56. eval-calc-019-s2

内容 SHA256：`c93871113f4fee471fe29be9f8cd703072963f165a62ab4e2f9b3722567d27d8`。

来源：data/v2/eval/dataset_eval.jsonl，第 56 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求反常积分 $\displaystyle\int_0^{+\infty}xe^{-x}\,dx$。

**过程**

由 Γ 函数定义 $\Gamma(s)=\displaystyle\int_0^{+\infty}t^{s-1}e^{-t}dt$，原积分 $=\Gamma(2)$。递推：$\Gamma(s+1)=s\Gamma(s)$（分部积分一次即得），且 $\Gamma(1)=\displaystyle\int_0^{+\infty}e^{-t}dt=1$，故 $\Gamma(2)=1\cdot\Gamma(1)=1$。此解法把单个积分放进 Γ 函数家族，可一并处理 $\int_0^{+\infty}x^ne^{-x}dx=\Gamma(n+1)=n!$。

**答案原文**

$1$

## 57. eval-calc-019-s3

内容 SHA256：`afeb9a2d0f1379f72506c1fa7c8521764a9a651e5bedb2d3bed0dd747345f99a`。

来源：data/v2/eval/dataset_eval.jsonl，第 57 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求反常积分 $\displaystyle\int_0^{+\infty}xe^{-x}\,dx$。

**过程**

若 $X\sim\operatorname{Exp}(1)$（参数 $\lambda=1$ 的指数分布），其密度为 $f(x)=e^{-x}$（$x>0$），则原积分 $=E[X]$。由指数分布期望公式 $E[X]=\dfrac{1}{\lambda}=1$；或由尾概率公式 $E[X]=\displaystyle\int_0^{+\infty}P(X>t)dt=\int_0^{+\infty}e^{-t}dt=1$ 得到同一结果。

**答案原文**

$1$

## 58. eval-calc-020-s1

内容 SHA256：`27b03e187d267133347dc128b5b4161b2fa9dc9cb158f991f093a3baef396ece`。

来源：data/v2/eval/dataset_eval.jsonl，第 58 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

讨论反常积分 $\displaystyle\int_1^{+\infty}\frac{dx}{x^p}$（$p>0$）的敛散性，并求其收敛时的值。

**过程**

当 $p\ne 1$ 时，$\displaystyle\int_1^b x^{-p}dx=\left[\dfrac{x^{1-p}}{1-p}\right]_1^b=\dfrac{b^{1-p}-1}{1-p}$。若 $p>1$，则 $1-p<0$，$b^{1-p}\to 0$，积分为 $\dfrac{0-1}{1-p}=\dfrac{1}{p-1}$，收敛；若 $0<p<1$，则 $b^{1-p}\to+\infty$，发散。当 $p=1$ 时 $\displaystyle\int_1^b\dfrac{dx}{x}=\ln b\to+\infty$，发散。综上，$p>1$ 收敛于 $\dfrac{1}{p-1}$，$0<p\le 1$ 发散。

**答案原文**

$p>1$ 时收敛于 $\dfrac{1}{p-1}$；$0<p\le 1$ 时发散

## 59. eval-calc-020-s2

内容 SHA256：`5252a640797daa5ae61005088f1a9509cd32b2324a3be72f4e5a40e747c3a059`。

来源：data/v2/eval/dataset_eval.jsonl，第 59 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

讨论反常积分 $\displaystyle\int_1^{+\infty}\frac{dx}{x^p}$（$p>0$）的敛散性，并求其收敛时的值。

**过程**

函数 $f(x)=x^{-p}$ 在 $[1,+\infty)$ 上非负递减，由积分判别法，$\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{n^p}$ 与 $\displaystyle\int_1^{+\infty}\dfrac{dx}{x^p}$ 同敛散，故 $p>1$ 收敛、$p\le 1$ 发散——积分与级数两个世界互相印证。

**答案原文**

$p>1$ 时收敛于 $\dfrac{1}{p-1}$；$0<p\le 1$ 时发散

## 60. eval-calc-020-s3

内容 SHA256：`925f062e72d633fcba51fc9b60db59686ff2f90a780ee6579f19358be286bd9b`。

来源：data/v2/eval/dataset_eval.jsonl，第 60 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

讨论反常积分 $\displaystyle\int_1^{+\infty}\frac{dx}{x^p}$（$p>0$）的敛散性，并求其收敛时的值。

**过程**

作图比较 $y=\dfrac{1}{x}$ 与 $y=\dfrac{1}{x^2}$：把 $[1,+\infty)$ 按整数分块，$\dfrac{1}{x}$ 下第 $n$ 块面积约 $\dfrac{1}{n}$（对应调和级数各项，发散），$\dfrac{1}{x^2}$ 下第 $n$ 块面积约 $\dfrac{1}{n^2}$（对应收敛级数各项）。直观上 $p$ 越大曲线"塌得越快"，面积越有限，临界在 $p=1$。

**答案原文**

$p>1$ 时收敛于 $\dfrac{1}{p-1}$；$0<p\le 1$ 时发散

## 61. eval-calc-021-s1

内容 SHA256：`970adb3f81e3e3017f014d90a9f771f5a159927f60c05f9bd7d879d6b4f52db9`。

来源：data/v2/eval/dataset_eval.jsonl，第 61 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n}{2^n}$ 的和。

**过程**

写 $S=\dfrac{1}{2}+\dfrac{2}{4}+\dfrac{3}{8}+\dfrac{4}{16}+\cdots$，则 $\dfrac{S}{2}=\dfrac{1}{4}+\dfrac{2}{8}+\dfrac{3}{16}+\cdots$。两式相减：$S-\dfrac{S}{2}=\dfrac{1}{2}+\left(\dfrac{2}{4}-\dfrac{1}{4}\right)+\left(\dfrac{3}{8}-\dfrac{2}{8}\right)+\left(\dfrac{4}{16}-\dfrac{3}{16}\right)+\cdots=\dfrac{1}{2}+\dfrac{1}{4}+\dfrac{1}{8}+\dfrac{1}{16}+\cdots=1$（几何级数）。故 $\dfrac{S}{2}=1$，$S=2$。

**答案原文**

$2$

## 62. eval-calc-021-s2

内容 SHA256：`642b37cf66f3c4a2cc4bf8722bdd32d956a4cf8827bf66fe2d959db3b34348bd`。

来源：data/v2/eval/dataset_eval.jsonl，第 62 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n}{2^n}$ 的和。

**过程**

由等比级数 $\displaystyle\sum_{n=0}^{\infty}x^{n}=\dfrac{1}{1-x}$（$|x|<1$）逐项求导：$\displaystyle\sum_{n=1}^{\infty}nx^{n-1}=\dfrac{1}{(1-x)^2}$，故 $\displaystyle\sum_{n=1}^{\infty}nx^n=\dfrac{x}{(1-x)^2}$。取 $x=\dfrac{1}{2}$，得 $S=\dfrac{1/2}{(1-1/2)^2}=\dfrac{1/2}{1/4}=2$。

**答案原文**

$2$

## 63. eval-calc-021-s3

内容 SHA256：`c9be96b1d254eef3652e64b47e3530ec490e33baa2c3abfe2e5c4d1689392ab7`。

来源：data/v2/eval/dataset_eval.jsonl，第 63 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n}{2^n}$ 的和。

**过程**

设 $X$ 服从参数 $p=\dfrac{1}{2}$ 的几何分布（抛硬币直到首次正面所需次数），则 $P(X=n)=q^{n-1}p=\left(\dfrac{1}{2}\right)^n$，$E[X]=\displaystyle\sum_{n=1}^{\infty}nq^{n-1}p=p\sum_{n=1}^{\infty}nq^{n-1}=p\cdot\dfrac{1}{(1-q)^2}=\dfrac{1}{p}=2$（其中用到 $\sum nq^{n-1}=\dfrac{1}{(1-q)^2}$）。而 $E[X]=\displaystyle\sum_{n=1}^{\infty}n\left(\dfrac{1}{2}\right)^n=S$，故 $S=2$。

**答案原文**

$2$

## 64. eval-calc-022-s1

内容 SHA256：`d90dc24c80a4d39585a1cde5b8a6079f8bf209b6f40984cf4b215e3746478dc2`。

来源：data/v2/eval/dataset_eval.jsonl，第 64 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n^2}{2^n}$ 的和。

**过程**

由 $\displaystyle\sum_{n=1}^{\infty}x^n=\dfrac{x}{1-x}$ 逐项求导两次：先得 $\displaystyle\sum_{n=1}^{\infty}nx^{n-1}=\dfrac{1}{(1-x)^2}$，再得 $\displaystyle\sum_{n=1}^{\infty}n(n-1)x^{n-2}=\dfrac{2}{(1-x)^3}$。于是 $\displaystyle\sum_{n=1}^{\infty}n^2x^n=\sum_{n=1}^{\infty}n(n-1)x^n+\sum_{n=1}^{\infty}nx^n=\dfrac{2x^2}{(1-x)^3}+\dfrac{x}{(1-x)^2}=\dfrac{x(1+x)}{(1-x)^3}$。取 $x=\dfrac{1}{2}$，得 $S=\dfrac{(1/2)(3/2)}{(1/2)^3}=6$。

**答案原文**

$6$

## 65. eval-calc-022-s2

内容 SHA256：`47ac6ef091eea690f794844ed6a67634c48233d0374e4b490bfaff5d0bbdaf43`。

来源：data/v2/eval/dataset_eval.jsonl，第 65 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n^2}{2^n}$ 的和。

**过程**

记 $A=\displaystyle\sum_{n=1}^{\infty}\dfrac{n}{2^n}=2$（eval-calc-021）、$B=\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{2^n}=1$。$\dfrac{S}{2}=\displaystyle\sum_{n=1}^{\infty}\dfrac{n^2}{2^{n+1}}=\sum_{m=2}^{\infty}\dfrac{(m-1)^2}{2^m}$，故 $S-\dfrac{S}{2}=\displaystyle\sum_{n=1}^{\infty}\dfrac{n^2-(n-1)^2}{2^n}=\sum_{n=1}^{\infty}\dfrac{2n-1}{2^n}=2A-B=2\cdot 2-1=3$。于是 $\dfrac{S}{2}=3$，$S=6$。

**答案原文**

$6$

## 66. eval-calc-022-s3

内容 SHA256：`50867999766bbbfff041ca0ecc3f496b3f56169a548d82ffecabefd8d1fe05d4`。

来源：data/v2/eval/dataset_eval.jsonl，第 66 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n^2}{2^n}$ 的和。

**过程**

设 $X\sim\operatorname{Geom}(1/2)$（$q=p=\dfrac{1}{2}$）。先算阶乘矩：$E[X(X-1)]=\displaystyle\sum_{k=1}^{\infty}k(k-1)q^{k-1}p=pq\sum_{k=2}^{\infty}k(k-1)q^{k-2}=pq\cdot\dfrac{2}{(1-q)^3}=\dfrac{2q}{p^2}$。故 $E[X^2]=E[X(X-1)]+E[X]=\dfrac{2q}{p^2}+\dfrac{1}{p}=\dfrac{2q+p}{p^2}=\dfrac{2-p}{p^2}$。代入 $p=\dfrac{1}{2}$ 得 $E[X^2]=6$，而 $E[X^2]=\displaystyle\sum_{n=1}^{\infty}n^2\left(\dfrac{1}{2}\right)^n=S$，故 $S=6$。

**答案原文**

$6$

## 67. eval-calc-023-s1

内容 SHA256：`c3e26f811cee852773964a6bf8f07de6143ef760b7daf62d2b27cad84b8f47ee`。

来源：data/v2/eval/dataset_eval.jsonl，第 67 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

证明级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^2}$ 收敛。

**过程**

$f(x)=\dfrac{1}{x^2}$ 在 $[1,+\infty)$ 上非负递减，且 $\displaystyle\int_1^{+\infty}\dfrac{dx}{x^2}=1$ 收敛（eval-calc-020 的 $p=2$ 情形），由积分判别法，级数 $\sum\dfrac{1}{n^2}$ 收敛。

**答案原文**

证毕（三种证法）

## 68. eval-calc-023-s2

内容 SHA256：`6cedd5d9a9d2d4efe40afb6609ec4f007295131092ff32af652d929f9995e0ad`。

来源：data/v2/eval/dataset_eval.jsonl，第 68 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

证明级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^2}$ 收敛。

**过程**

当 $n\ge 2$ 时 $\dfrac{1}{n^2}<\dfrac{1}{n(n-1)}=\dfrac{1}{n-1}-\dfrac{1}{n}$。部分和 $S_n=1+\displaystyle\sum_{k=2}^{n}\dfrac{1}{k^2}<1+\sum_{k=2}^{n}\left(\dfrac{1}{k-1}-\dfrac{1}{k}\right)=1+\left(1-\dfrac{1}{n}\right)<2$。正项级数部分和单调递增且有上界 2，故收敛。

**答案原文**

证毕（三种证法）

## 69. eval-calc-023-s3

内容 SHA256：`8366df5cd0e1db092399e0e17793275d6466bb250695fc07f02e8bb487184875`。

来源：data/v2/eval/dataset_eval.jsonl，第 69 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

证明级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^2}$ 收敛。

**过程**

取 $2^k$ 项凝聚：$\displaystyle\sum_{k=1}^{\infty}2^k\cdot\dfrac{1}{(2^k)^2}=\sum_{k=1}^{\infty}\dfrac{1}{2^k}$ 收敛（几何级数），由 Cauchy 凝聚判别法，原级数收敛。

**答案原文**

证毕（三种证法）

## 70. eval-calc-024-s1

内容 SHA256：`3ac7b36bbe5e3ab45b8b4c7616ef8d6db343e85c468d66209a6411593e597888`。

来源：data/v2/eval/dataset_eval.jsonl，第 70 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求 $\arctan x$ 的幂级数展开式，并由此推导莱布尼茨级数 $\dfrac{\pi}{4}=1-\dfrac{1}{3}+\dfrac{1}{5}-\dfrac{1}{7}+\cdots$。

**过程**

由等比级数 $\dfrac{1}{1+t}=\displaystyle\sum_{n=0}^{\infty}(-1)^nt^{n}$（$|t|<1$），以 $t=x^2$ 代入得 $\dfrac{1}{1+x^2}=\displaystyle\sum_{n=0}^{\infty}(-1)^nx^{2n}$。逐项积分：$\arctan x=\displaystyle\int_0^x\dfrac{dt}{1+t^2}=\sum_{n=0}^{\infty}(-1)^n\int_0^xt^{2n}dt=\sum_{n=0}^{\infty}\dfrac{(-1)^nx^{2n+1}}{2n+1}$（$|x|<1$）。

**答案原文**

$\arctan x=\displaystyle\sum_{n=0}^{\infty}\dfrac{(-1)^n x^{2n+1}}{2n+1}$（$|x|\le 1$）；$x=1$ 时即莱布尼茨级数

## 71. eval-calc-024-s2

内容 SHA256：`093109836bf55d81fa07675d720e5b851c81726eefbfe037856bc2ba48a15b18`。

来源：data/v2/eval/dataset_eval.jsonl，第 71 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求 $\arctan x$ 的幂级数展开式，并由此推导莱布尼茨级数 $\dfrac{\pi}{4}=1-\dfrac{1}{3}+\dfrac{1}{5}-\dfrac{1}{7}+\cdots$。

**过程**

$x=1$ 处级数 $\displaystyle\sum_{n=0}^{\infty}\dfrac{(-1)^n}{2n+1}$ 为交错级数（$a_n=\dfrac{1}{2n+1}\searrow 0$），由莱布尼茨判别法收敛；由 Abel 定理，和函数在 $x=1$ 左连续，故 $\arctan 1=\dfrac{\pi}{4}=1-\dfrac{1}{3}+\dfrac{1}{5}-\dfrac{1}{7}+\cdots$。$x=-1$ 同理（或由奇偶性）。

**答案原文**

$\arctan x=\displaystyle\sum_{n=0}^{\infty}\dfrac{(-1)^n x^{2n+1}}{2n+1}$（$|x|\le 1$）；$x=1$ 时即莱布尼茨级数

## 72. eval-calc-024-s3

内容 SHA256：`854facb3033f084745e91b7bf58bd743147cc577ed7de9630d97ceb6276acc50`。

来源：data/v2/eval/dataset_eval.jsonl，第 72 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求 $\arctan x$ 的幂级数展开式，并由此推导莱布尼茨级数 $\dfrac{\pi}{4}=1-\dfrac{1}{3}+\dfrac{1}{5}-\dfrac{1}{7}+\cdots$。

**过程**

对 $f(x)=\arctan x$ 用带拉格朗日余项的麦克劳林公式：$f^{(n)}(0)$ 由递推 $f'(x)=\dfrac{1}{1+x^2}$ 逐阶求导给出。对 $\arctan$ 可归纳证明 $|f^{(m)}(t)|\le(m-1)!$（$m\ge 1$，对一切实数 $t$），于是余项 $|R_N(x)|=\dfrac{|f^{(N+1)}(\xi)|}{(N+1)!}|x|^{N+1}\le\dfrac{N!}{(N+1)!}\cdot 1=\dfrac{1}{N+1}\to 0$，对 $|x|\le 1$ 一致成立。故展开式在 $|x|\le 1$ 成立，端点处即莱布尼茨级数。

**答案原文**

$\arctan x=\displaystyle\sum_{n=0}^{\infty}\dfrac{(-1)^n x^{2n+1}}{2n+1}$（$|x|\le 1$）；$x=1$ 时即莱布尼茨级数

## 73. eval-calc-025-s1

内容 SHA256：`40c5a60946a40fdcfd7a6669f42c404f2a47f704a1e18de81a14d1ffd12e16c8`。

来源：data/v2/eval/dataset_eval.jsonl，第 73 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

讨论级数 $\displaystyle\sum_{n=2}^{\infty}\frac{(-1)^n}{\ln n}$ 的敛散性，若收敛，判断是绝对收敛还是条件收敛。

**过程**

$a_n=\dfrac{1}{\ln n}$ 单调递减且 $\lim_{n\to\infty}a_n=0$，由莱布尼茨判别法，交错级数 $\displaystyle\sum_{n=2}^{\infty}(-1)^na_n$ 收敛。考察绝对级数 $\displaystyle\sum_{n=2}^{\infty}\dfrac{1}{\ln n}$：当 $n\ge 3$ 时 $\dfrac{1}{\ln n}>\dfrac{1}{n}$（因 $\ln n<n$），而调和级数 $\sum\dfrac{1}{n}$ 发散，由比较判别法绝对级数发散。因此原级数条件收敛。

**答案原文**

条件收敛

## 74. eval-calc-025-s2

内容 SHA256：`efb396bb68d4a5c5c22ce59f089f36fe41fc29c22aece7a4fbaf252eae38ccd9`。

来源：data/v2/eval/dataset_eval.jsonl，第 74 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

讨论级数 $\displaystyle\sum_{n=2}^{\infty}\frac{(-1)^n}{\ln n}$ 的敛散性，若收敛，判断是绝对收敛还是条件收敛。

**过程**

记 $a_n=\dfrac{1}{\ln n}$，$S_n=\displaystyle\sum_{k=2}^{n}(-1)^ka_k$。配对求和：$S_{2m+1}=\displaystyle\sum_{j=1}^{m}(a_{2j}-a_{2j+1})$，每项为正，故奇子列 $S_{2m+1}$ 随 $m$ 递增；又 $a_{2j}-a_{2j+1}<a_{2j}-a_{2j+2}$，故 $S_{2m+1}<\displaystyle\sum_{j=1}^{m}(a_{2j}-a_{2j+2})=\dfrac{1}{\ln 2}-\dfrac{1}{\ln(2m+2)}<\dfrac{1}{\ln 2}$，奇子列有上界，收敛。偶子列 $S_{2m}=S_{2m+1}+a_{2m+1}$，与奇子列之差 $a_{2m+1}\to 0$，故 $S_n$ 收敛。绝对发散仍由解法一的比较法给出。

**答案原文**

条件收敛

## 75. eval-calc-025-s3

内容 SHA256：`1c22fabf74c460a8c89f3a37eaa686f0da5bb2ba5bafe62c6b14d478cae37356`。

来源：data/v2/eval/dataset_eval.jsonl，第 75 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

讨论级数 $\displaystyle\sum_{n=2}^{\infty}\frac{(-1)^n}{\ln n}$ 的敛散性，若收敛，判断是绝对收敛还是条件收敛。

**过程**

数值观察：$\displaystyle\sum_{k=2}^{n}\dfrac{1}{\ln k}$ 约为 $\dfrac{n}{\ln n}$ 量级（发散），而交错后正负相消使部分和在极限值附近振荡——用图形展示振荡收敛与无条件发散的反差。严格结论仍由解法一给出，本解法用于建立几何直觉。

**答案原文**

条件收敛

## 76. eval-calc-026-s1

内容 SHA256：`70acc86b9f425462e59c777aa51b3246840c52345e61d2d865560942604b6141`。

来源：data/v2/eval/dataset_eval.jsonl，第 76 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $z=x^y$（$x>0$），求 $z$ 在点 $(1,2)$ 处的两个偏导数。

**过程**

把 $y$ 视为常数：$z_x=yx^{y-1}$，故 $z_x(1,2)=2\cdot 1^{2-1}=2$。把 $x$ 视为常数：$z_y=x^y\ln x$，故 $z_y(1,2)=1^2\cdot\ln 1=0$。

**答案原文**

$z_x(1,2)=2$，$z_y(1,2)=0$

## 77. eval-calc-026-s2

内容 SHA256：`a912f5a1a823a2aa4f1a7a3e7c66d4f1625f8dde8b4276f2f736b885d4882931`。

来源：data/v2/eval/dataset_eval.jsonl，第 77 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $z=x^y$（$x>0$），求 $z$ 在点 $(1,2)$ 处的两个偏导数。

**过程**

对 $\ln z=y\ln x$ 两边求全微分：$\dfrac{dz}{z}=\dfrac{y}{x}dx+\ln x\,dy$。在 $(1,2)$ 处 $z=1$、$\dfrac{y}{x}=2$、$\ln x=0$，故 $dz=2\,dx+0\cdot dy$，即 $z_x=2$、$z_y=0$。

**答案原文**

$z_x(1,2)=2$，$z_y(1,2)=0$

## 78. eval-calc-026-s3

内容 SHA256：`60e5e4e5c2ba0a35909e5a9a94f5fba5a79101bb2e9a5d61f2d0cf4e9a9c3494`。

来源：data/v2/eval/dataset_eval.jsonl，第 78 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $z=x^y$（$x>0$），求 $z$ 在点 $(1,2)$ 处的两个偏导数。

**过程**

取步长 $h=10^{-4}$：$z_x\approx\dfrac{(1+h)^2-1^2}{h}=\dfrac{2h+h^2}{h}=2+h\to 2$；$z_y\approx\dfrac{1^{2+h}-1}{h}=\dfrac{0}{h}=0$。数值结果与解析一致，说明 $z_y(1,2)=0$ 反映曲面在 $y$ 方向局部水平。

**答案原文**

$z_x(1,2)=2$，$z_y(1,2)=0$

## 79. eval-calc-027-s1

内容 SHA256：`599c1be044b804db5643e3425697a44344f350d702d94340dff71f808b7a7ff8`。

来源：data/v2/eval/dataset_eval.jsonl，第 79 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求二重积分 $\displaystyle I=\int_0^1\!\!\int_x^1 e^{y^2}\,dy\,dx$。

**过程**

积分区域为 $D=\{(x,y):0\le x\le 1,\ x\le y\le 1\}=\{(x,y):0\le y\le 1,\ 0\le x\le y\}$。交换次序：$I=\displaystyle\int_0^1\!\!\int_0^y e^{y^2}\,dx\,dy=\int_0^1 y\,e^{y^2}\,dy$。令 $u=y^2$（$du=2y\,dy$）：$I=\dfrac{1}{2}\displaystyle\int_0^1 e^u\,du=\dfrac{1}{2}(e-1)$。

**答案原文**

$\dfrac{e-1}{2}$

## 80. eval-calc-027-s2

内容 SHA256：`92c13770404f6825bd54e40042011a99ef4af404ecd0627c97e1c74648c640b1`。

来源：data/v2/eval/dataset_eval.jsonl，第 80 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求二重积分 $\displaystyle I=\int_0^1\!\!\int_x^1 e^{y^2}\,dy\,dx$。

**过程**

记 $F(x)=\displaystyle\int_x^1e^{y^2}dy$，则 $I=\displaystyle\int_0^1F(x)dx$，且 $F(1)=0$、$F'(x)=-e^{x^2}$。分部积分：$I=\left[xF(x)\right]_0^1-\displaystyle\int_0^1xF'(x)dx=0-\int_0^1x\left(-e^{x^2}\right)dx=\int_0^1xe^{x^2}dx=\left[\dfrac{e^{x^2}}{2}\right]_0^1=\dfrac{e-1}{2}$。

**答案原文**

$\dfrac{e-1}{2}$

## 81. eval-calc-027-s3

内容 SHA256：`a9b0725def2a89b2a245083453124191f502328c43c308b6aa301b55d3b22260`。

来源：data/v2/eval/dataset_eval.jsonl，第 81 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求二重积分 $\displaystyle I=\int_0^1\!\!\int_x^1 e^{y^2}\,dy\,dx$。

**过程**

若按原次序先积 $y$，需要 $\int e^{y^2}dy$ 的原函数，而由刘维尔定理 $e^{y^2}$ 没有初等原函数，直接路线注定失败——这正是必须交换次序（或改用解法二）的信号。作为辅助校验，用二重黎曼和（如 $1000\times 1000$ 网格）估算 $I\approx 0.85914$，与解析值 $\dfrac{e-1}{2}=0.859141\cdots$ 吻合。

**答案原文**

$\dfrac{e-1}{2}$

## 82. eval-calc-028-s1

内容 SHA256：`a5e07fdef9998eac36713ecdeff4a3b736eeea7e887c1a033b5b6e984e115bd4`。

来源：data/v2/eval/dataset_eval.jsonl，第 82 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求二重积分 $\displaystyle I=\iint_D(x^2+y^2)\,dA$，其中 $D=\{(x,y):x^2+y^2\le 2y\}$。

**过程**

$D$ 是圆心 $(0,1)$、半径 $1$ 的圆盘，极坐标下边界 $r=2\sin\theta$（$\theta\in[0,\pi]$），且 $x^2+y^2=r^2$、$dA=r\,dr\,d\theta$。$I=\displaystyle\int_0^{\pi}\!\!\int_0^{2\sin\theta}r^2\cdot r\,dr\,d\theta=\int_0^{\pi}\left[\dfrac{r^4}{4}\right]_0^{2\sin\theta}d\theta=\int_0^{\pi}4\sin^4\theta\,d\theta$。由 $\displaystyle\int_0^{\pi}\sin^4\theta\,d\theta=\dfrac{3\pi}{8}$（倍角降次即得），故 $I=4\cdot\dfrac{3\pi}{8}=\dfrac{3\pi}{2}$。

**答案原文**

$\dfrac{3\pi}{2}$

## 83. eval-calc-028-s2

内容 SHA256：`1c19d83eccd338c9c99895e5bb1660cfa2bc0b1ddc2f98fcf46986a0d680e291`。

来源：data/v2/eval/dataset_eval.jsonl，第 83 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求二重积分 $\displaystyle I=\iint_D(x^2+y^2)\,dA$，其中 $D=\{(x,y):x^2+y^2\le 2y\}$。

**过程**

$D:0\le y\le 2,\ -\sqrt{2y-y^2}\le x\le\sqrt{2y-y^2}$。先对 $x$ 积分：内层 $=\left[\dfrac{x^3}{3}+xy^2\right]_{-\sqrt{2y-y^2}}^{\sqrt{2y-y^2}}=2\left[\dfrac{(2y-y^2)^{3/2}}{3}+y^2\sqrt{2y-y^2}\right]=2\sqrt{2y-y^2}\left[\dfrac{2y-y^2}{3}+y^2\right]=\dfrac{4}{3}y(1+y)\sqrt{2y-y^2}$。故 $I=\dfrac{4}{3}\displaystyle\int_0^2 y(1+y)\sqrt{2y-y^2}\,dy$。令 $u=y-1$（平移至圆心），则 $y(1+y)=(1+u)(2+u)=2+3u+u^2$，$\sqrt{2y-y^2}=\sqrt{1-u^2}$，$u:-1\to 1$。$I=\dfrac{4}{3}\displaystyle\int_{-1}^{1}(2+3u+u^2)\sqrt{1-u^2}\,du=\dfrac{4}{3}\left[2\cdot\dfrac{\pi}{2}+3\cdot 0+\dfrac{\pi}{8}\right]=\dfrac{4}{3}\cdot\dfrac{9\pi}{8}=\dfrac{3\pi}{2}$（其中 $\int_{-1}^{1}\sqrt{1-u^2}du=\dfrac{\pi}{2}$ 为半圆面积，$u\sqrt{1-u^2}$ 为奇函数积分为 0，$\int_{-1}^{1}u^2\sqrt{1-u^2}du=\dfrac{\pi}{8}$ 由三角代换 $u=\sin t$ 即得）。

**答案原文**

$\dfrac{3\pi}{2}$

## 84. eval-calc-028-s3

内容 SHA256：`bd23ce00fbe436021e575f1df52dd28f270e92fab2c9567a0cce46c0b1d7a9c4`。

来源：data/v2/eval/dataset_eval.jsonl，第 84 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求二重积分 $\displaystyle I=\iint_D(x^2+y^2)\,dA$，其中 $D=\{(x,y):x^2+y^2\le 2y\}$。

**过程**

被积函数 $x^2+y^2$ 是到原点的距离平方，积分即区域 $D$ 关于原点 $O$ 的极惯性矩 $J_O$。由平行轴定理 $J_O=J_C+Ad^2$，其中 $J_C$ 是圆盘关于自身圆心 $C$ 的极惯性矩 $J_C=\dfrac{\pi R^4}{2}=\dfrac{\pi}{2}$，$A=\pi$ 为面积，$d=|OC|=1$ 为圆心到原点的距离。故 $I=J_O=\dfrac{\pi}{2}+\pi\cdot 1^2=\dfrac{3\pi}{2}$。

**答案原文**

$\dfrac{3\pi}{2}$

## 85. eval-calc-029-s1

内容 SHA256：`b6dc5aa6984cb4dc1f05526670ab587d6810fc4707b366941c43f1cb6f233b12`。

来源：data/v2/eval/dataset_eval.jsonl，第 85 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求星形线 $x^{2/3}+y^{2/3}=a^{2/3}$（$a>0$）的周长。

**过程**

参数化 $x=a\cos^3 t$、$y=a\sin^3 t$（$t\in[0,2\pi]$）。$x'=-3a\cos^2 t\sin t$，$y'=3a\sin^2 t\cos t$，弧长微元 $ds=\sqrt{(x')^2+(y')^2}\,dt=\sqrt{9a^2\cos^4 t\sin^2 t+9a^2\sin^4 t\cos^2 t}\,dt=3a|\sin t\cos t|\,dt$。由对称性取第一象限：$L=4\displaystyle\int_0^{\pi/2}3a\sin t\cos t\,dt=12a\left[\dfrac{\sin^2 t}{2}\right]_0^{\pi/2}=12a\cdot\dfrac{1}{2}=6a$。

**答案原文**

$6a$

## 86. eval-calc-029-s2

内容 SHA256：`8ddd3f5d2879b83efc5b04d879d30fa0b487ab1b19827c11ee6ae082fcf3a50e`。

来源：data/v2/eval/dataset_eval.jsonl，第 86 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求星形线 $x^{2/3}+y^{2/3}=a^{2/3}$（$a>0$）的周长。

**过程**

由隐函数求导（eval-calc-007）$y'=-\left(\dfrac{y}{x}\right)^{1/3}$，故弧长微元 $ds=\sqrt{1+(y')^2}\,dx=\sqrt{1+(y/x)^{2/3}}\,dx=\sqrt{\dfrac{x^{2/3}+y^{2/3}}{x^{2/3}}}\,dx$。由星形线方程 $x^{2/3}+y^{2/3}=a^{2/3}$，得 $ds=a^{1/3}x^{-1/3}dx$。第一象限部分：$L_1=\displaystyle\int_0^a a^{1/3}x^{-1/3}dx=a^{1/3}\left[\dfrac{3}{2}x^{2/3}\right]_0^a=\dfrac{3a}{2}$，故 $L=4L_1=6a$。

**答案原文**

$6a$

## 87. eval-calc-029-s3

内容 SHA256：`9b35cda2bd3ecb953c2329e4a00a5f4e7ca826a3f4f32bd01c771ddde5e4cacd`。

来源：data/v2/eval/dataset_eval.jsonl，第 87 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求星形线 $x^{2/3}+y^{2/3}=a^{2/3}$（$a>0$）的周长。

**过程**

考虑两端分别在坐标轴上、长为 $a$ 的滑动线段：端点 $E_1(t)=(a\cos t,0)$、$E_2(t)=(0,a\sin t)$。线段上参数 $v\in[0,1]$ 的点为 $P(t,v)=\big(a(1-v)\cos t,\ a v\sin t\big)$。包络条件 $\dfrac{\partial P}{\partial t}$ 与 $\dfrac{\partial P}{\partial v}$ 平行：$\left(-a(1-v)\sin t,\ av\cos t\right)$ 与 $\left(-a\cos t,\ a\sin t\right)$ 平行，叉积为零：$-a^2(1-v)\sin^2 t+a^2v\cos^2 t=0$，解得 $v=\sin^2 t$。代入得包络点 $\big(a\cos t(1-\sin^2 t),\ a\sin^3 t\big)=\big(a\cos^3 t,\ a\sin^3 t\big)$——正是星形线。于是星形线是定长滑动线段的包络，其弧长即解法一的参数曲线弧长：四分之一部分 $\displaystyle\int_0^{\pi/2}3a\sin t\cos t\,dt=\dfrac{3a}{2}$，全长 $6a$。

**答案原文**

$6a$

## 88. eval-calc-030-s1

内容 SHA256：`3ff7bd6612c299f4cdc89d43133280d6ded27c22ee1cccbc5ff29cc1531412a7`。

来源：data/v2/eval/dataset_eval.jsonl，第 88 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求由 $y=\sin x$（$0\le x\le\pi$）与 $x$ 轴围成的区域绕 $y$ 轴旋转所得旋转体的体积。

**过程**

在 $x$ 处取高度 $\sin x$、厚度 $dx$ 的竖直壳层，其体积微元 $dV=2\pi x\sin x\,dx$。$V=\displaystyle\int_0^{\pi}2\pi x\sin x\,dx$。分部积分（$u=x$、$dv=\sin x\,dx$）：$\displaystyle\int_0^{\pi}x\sin x\,dx=\left[-x\cos x\right]_0^{\pi}+\int_0^{\pi}\cos x\,dx=\pi+\left[\sin x\right]_0^{\pi}=\pi$。故 $V=2\pi\cdot\pi=2\pi^2$。

**答案原文**

$2\pi^2$

## 89. eval-calc-030-s2

内容 SHA256：`be47cadaf78991987bc2c05e949581eee5964e14634662714922f39821f6e1f1`。

来源：data/v2/eval/dataset_eval.jsonl，第 89 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求由 $y=\sin x$（$0\le x\le\pi$）与 $x$ 轴围成的区域绕 $y$ 轴旋转所得旋转体的体积。

**过程**

区域面积 $A=\displaystyle\int_0^\pi\sin x\,dx=\left[-\cos x\right]_0^\pi=2$。质心横坐标 $\bar x=\dfrac{1}{A}\displaystyle\int_0^\pi x\sin x\,dx=\dfrac{\pi}{2}$（区域关于 $x=\dfrac{\pi}{2}$ 对称，且上式已算出积分为 $\pi$）。由帕普斯定理（绕 $y$ 轴，轴不穿过区域内部），$V=2\pi\bar x A=2\pi\cdot\dfrac{\pi}{2}\cdot 2=2\pi^2$。

**答案原文**

$2\pi^2$

## 90. eval-calc-030-s3

内容 SHA256：`635df1ba473ada5b40aaf0aeee0601aa129b0e356e8ae5600dfb476dcab1bd66`。

来源：data/v2/eval/dataset_eval.jsonl，第 90 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求由 $y=\sin x$（$0\le x\le\pi$）与 $x$ 轴围成的区域绕 $y$ 轴旋转所得旋转体的体积。

**过程**

绕 $y$ 轴时取水平圆盘：对 $0\le y\le 1$，水平线 $y$ 与区域相交于 $x=\arcsin y$（左）与 $x=\pi-\arcsin y$（右），圆盘外半径 $R=\pi-\arcsin y$、内半径 $r=\arcsin y$。$V=\pi\displaystyle\int_0^1\left[(\pi-\arcsin y)^2-(\arcsin y)^2\right]dy=\pi\int_0^1(\pi^2-2\pi\arcsin y)\,dy=\pi\left[\pi^2y-2\pi\int_0^1\arcsin y\,dy\right]$。其中 $\displaystyle\int_0^1\arcsin y\,dy=\left[y\arcsin y+\sqrt{1-y^2}\right]_0^1=\dfrac{\pi}{2}-1$。故 $V=\pi\left[\pi^2-2\pi\left(\dfrac{\pi}{2}-1\right)\right]=\pi\left[\pi^2-\pi^2+2\pi\right]=2\pi^2$。

**答案原文**

$2\pi^2$

## 91. eval-geom-001-s1

内容 SHA256：`c38d38ad471ce61cabcb81f2820e3be2c3003ff44489e0f4bd78ab8b3bc4a83a`。

来源：data/v2/eval/dataset_eval.jsonl，第 91 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求点 $P(1,2,-1)$ 到平面 $\pi:2x-y+2z=3$ 的距离。

**过程**

平面法向量 $\vec n=(2,-1,2)$，$|\vec n|=\sqrt{4+1+4}=3$。代入点到平面距离公式：$d=\dfrac{|2\cdot 1-1\cdot 2+2\cdot(-1)-3|}{3}=\dfrac{|2-2-2-3|}{3}=\dfrac{5}{3}$。

**答案原文**

$\dfrac{5}{3}$

## 92. eval-geom-001-s2

内容 SHA256：`895608046b065da3de94d4a89def7a494858a6cb890595710269f6c9ad0e7de9`。

来源：data/v2/eval/dataset_eval.jsonl，第 92 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求点 $P(1,2,-1)$ 到平面 $\pi:2x-y+2z=3$ 的距离。

**过程**

取平面上一点 $Q(0,-3,0)$（$2\cdot 0-(-3)+2\cdot 0=3$ 满足方程），则 $\overrightarrow{QP}=(1,5,-1)$。$P$ 到平面的距离等于 $\overrightarrow{QP}$ 在法向量上的投影长度：$d=\dfrac{|\overrightarrow{QP}\cdot\vec n|}{|\vec n|}=\dfrac{|1\cdot 2+5\cdot(-1)+(-1)\cdot 2|}{3}=\dfrac{5}{3}$。垂足为 $P$ 减去投影向量 $\dfrac{\overrightarrow{QP}\cdot\vec n}{|\vec n|^2}\vec n=\dfrac{-5}{9}(2,-1,2)$，即 $\left(\dfrac{19}{9},\dfrac{13}{9},\dfrac{1}{9}\right)$。

**答案原文**

$\dfrac{5}{3}$

## 93. eval-geom-001-s3

内容 SHA256：`04ba1f390d53a9e730fe8b77047b49bc3f8aac33108f0e3f04603a471f0c14b3`。

来源：data/v2/eval/dataset_eval.jsonl，第 93 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求点 $P(1,2,-1)$ 到平面 $\pi:2x-y+2z=3$ 的距离。

**过程**

求 $f(x,y,z)=(x-1)^2+(y-2)^2+(z+1)^2$ 在约束 $2x-y+2z-3=0$ 下的最小值。由 $\nabla f=\lambda\nabla(2x-y+2z-3)$：$2(x-1)=2\lambda$，$2(y-2)=-\lambda$，$2(z+1)=2\lambda$，得 $x-1=\lambda$，$y-2=-\dfrac{\lambda}{2}$，$z+1=\lambda$。代入约束：$2(1+\lambda)-\left(2-\dfrac{\lambda}{2}\right)+2(\lambda-1)=3$，即 $\dfrac{9\lambda}{2}-2=3$，解得 $\lambda=\dfrac{10}{9}$。最近距离 $d=\sqrt{\lambda^2+\dfrac{\lambda^2}{4}+\lambda^2}=\dfrac{3}{2}|\lambda|=\dfrac{5}{3}$。

**答案原文**

$\dfrac{5}{3}$

## 94. eval-geom-002-s1

内容 SHA256：`2164dada940fcaf2deaaefa3a0bcce40663773c9816229fcc7647035c1ac2ce6`。

来源：data/v2/eval/dataset_eval.jsonl，第 94 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

判断两条直线 $l_1:\dfrac{x-1}{2}=\dfrac{y+1}{1}=\dfrac{z-2}{-1}$ 与 $l_2:\dfrac{x+1}{1}=\dfrac{y-2}{2}=\dfrac{z}{1}$ 的位置关系。

**过程**

$l_1$ 的方向向量 $\vec{s_1}=(2,1,-1)$，$l_2$ 的 $\vec{s_2}=(1,2,1)$。叉积 $\vec{s_1}\times\vec{s_2}=(1\cdot 1-(-1)\cdot 2,\ (-1)\cdot 1-2\cdot 1,\ 2\cdot 2-1\cdot 1)=(3,-3,3)\ne\vec 0$，故不平行。取 $P_1(1,-1,2)\in l_1$、$P_2(-1,2,0)\in l_2$，$\overrightarrow{P_1P_2}=(-2,3,-2)$。混合积 $\overrightarrow{P_1P_2}\cdot(\vec{s_1}\times\vec{s_2})=-2\cdot 3+3\cdot(-3)+(-2)\cdot 3=-21\ne 0$，故两直线不共面，即异面。

**答案原文**

异面直线

## 95. eval-geom-002-s2

内容 SHA256：`1be04e5926b3e0989157b664e4d36279dad2ecea50b9f03444f93ee3d116c3f4`。

来源：data/v2/eval/dataset_eval.jsonl，第 95 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

判断两条直线 $l_1:\dfrac{x-1}{2}=\dfrac{y+1}{1}=\dfrac{z-2}{-1}$ 与 $l_2:\dfrac{x+1}{1}=\dfrac{y-2}{2}=\dfrac{z}{1}$ 的位置关系。

**过程**

参数化：$l_1:(1+2t,-1+t,2-t)$，$l_2:(-1+s,2+2s,s)$。若相交，需 $1+2t=-1+s$、$-1+t=2+2s$、$2-t=s$ 同时成立。由第三式 $s=2-t$ 代入第一式：$1+2t=-1+2-t$，得 $t=0$、$s=2$；代入第二式检验：$-1+0=2+4$，即 $-1=6$，矛盾。故无公共点；结合方向向量不平行，得异面。

**答案原文**

异面直线

## 96. eval-geom-002-s3

内容 SHA256：`0ee27302f647667353b401d4f037fe1c8172b181dedd18bf3ce801da666dce46`。

来源：data/v2/eval/dataset_eval.jsonl，第 96 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

判断两条直线 $l_1:\dfrac{x-1}{2}=\dfrac{y+1}{1}=\dfrac{z-2}{-1}$ 与 $l_2:\dfrac{x+1}{1}=\dfrac{y-2}{2}=\dfrac{z}{1}$ 的位置关系。

**过程**

两直线方向向量不平行（$\vec{s_1}\times\vec{s_2}\ne 0$），若相交则必共面；其公垂线方向为 $\vec{s_1}\times\vec{s_2}=(3,-3,3)$。解法二已排除相交，故两直线不平行、不相交，只能异面。

**答案原文**

异面直线

## 97. eval-geom-003-s1

内容 SHA256：`084b4143ed20c792cef2d646615615d17201ffb32ef58fc9e058e8ea693a55f6`。

来源：data/v2/eval/dataset_eval.jsonl，第 97 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求过直线 $l:\dfrac{x-1}{1}=\dfrac{y}{2}=\dfrac{z+1}{1}$ 且垂直于平面 $\pi:x+y+z=0$ 的平面方程。

**过程**

直线方向 $\vec s=(1,2,1)$，$\pi$ 的法向量 $\vec{n_1}=(1,1,1)$。所求平面含直线 $l$ 且垂直于 $\pi$，故其法向量 $\vec n\perp\vec s$ 且 $\vec n\perp\vec{n_1}$，取 $\vec n=\vec s\times\vec{n_1}=(2\cdot 1-1\cdot 1,\ 1\cdot 1-1\cdot 1,\ 1\cdot 1-2\cdot 1)=(1,0,-1)$。过直线上一点 $P_0(1,0,-1)$：$1\cdot(x-1)+0\cdot y+(-1)\cdot(z+1)=0$，即 $x-z=2$。检验：直线上点 $(1+t,2t,-1+t)$ 满足 $(1+t)-(-1+t)=2$；$|\vec n\cdot\vec{n_1}|=|1-1|=0$ 故与 $\pi$ 垂直。

**答案原文**

$x-z=2$

## 98. eval-geom-003-s2

内容 SHA256：`ad7e059a57e29e89130537514130ed0e06e968c9bd983dc4744d48f498f8206b`。

来源：data/v2/eval/dataset_eval.jsonl，第 98 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求过直线 $l:\dfrac{x-1}{1}=\dfrac{y}{2}=\dfrac{z+1}{1}$ 且垂直于平面 $\pi:x+y+z=0$ 的平面方程。

**过程**

把 $l$ 写成两平面交线：由 $\dfrac{x-1}{1}=\dfrac{y}{2}$ 得 $y=2x-2$，由 $\dfrac{y}{2}=\dfrac{z+1}{1}$ 得 $y=2z+2$。过 $l$ 的平面束为 $(2x-2-y)+\lambda(2z+2-y)=0$，其法向量为 $(2,-1-\lambda,2\lambda)$。与 $\pi$ 垂直要求 $2\cdot 1+(-1-\lambda)\cdot 1+2\lambda\cdot 1=0$，即 $1+\lambda=0$，$\lambda=-1$。代入：$(2x-2-y)-(2z+2-y)=0$，即 $2x-2z-4=0$，$x-z=2$。

**答案原文**

$x-z=2$

## 99. eval-geom-003-s3

内容 SHA256：`7a31db0678938e1e4ca441899bcad2401b32ee8ba5e05ccb67f3fd55d20800ed`。

来源：data/v2/eval/dataset_eval.jsonl，第 99 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求过直线 $l:\dfrac{x-1}{1}=\dfrac{y}{2}=\dfrac{z+1}{1}$ 且垂直于平面 $\pi:x+y+z=0$ 的平面方程。

**过程**

所求平面过 $P_0(1,0,-1)$ 且含方向 $\vec s=(1,2,1)$；又因垂直于 $\pi$，平面法向量必与 $\vec{n_1}$ 垂直，故 $\vec{n_1}$ 必平行于所求平面，可作为平面内第二个方向向量。平面法向量 $\vec n=\vec s\times\vec{n_1}=(1,0,-1)$（同解法一），得 $x-z=2$。

**答案原文**

$x-z=2$

## 100. eval-geom-004-s1

内容 SHA256：`38ce7e6aee563cfa1a05dc5058af27787686194cc21abe5666815eceb321e16b`。

来源：data/v2/eval/dataset_eval.jsonl，第 100 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求两平面 $\pi_1:x-y+z=1$ 与 $\pi_2:2x+y-z=0$ 的夹角。

**过程**

$\vec{n_1}=(1,-1,1)$，$\vec{n_2}=(2,1,-1)$。点积 $\vec{n_1}\cdot\vec{n_2}=1\cdot 2+(-1)\cdot 1+1\cdot(-1)=0$，故 $\cos\theta=\dfrac{|\vec{n_1}\cdot\vec{n_2}|}{|\vec{n_1}||\vec{n_2}|}=0$，两平面夹角为 $\dfrac{\pi}{2}$。

**答案原文**

$\dfrac{\pi}{2}$（两平面垂直）

## 101. eval-geom-004-s2

内容 SHA256：`17711c937801d740b0a56e743bed6e158c8ca5c96e2753535d8e19a04b3da3d5`。

来源：data/v2/eval/dataset_eval.jsonl，第 101 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求两平面 $\pi_1:x-y+z=1$ 与 $\pi_2:2x+y-z=0$ 的夹角。

**过程**

两平面交线方向 $\vec s=\vec{n_1}\times\vec{n_2}=((-1)(-1)-1\cdot 1,\ 1\cdot 2-1\cdot(-1),\ 1\cdot 1-(-1)\cdot 2)=(0,3,3)$，取 $\vec s=(0,1,1)$。在 $\pi_1$ 内取垂直于交线的方向 $\vec{d_1}=\vec{n_1}\times\vec s=((-1)\cdot 1-1\cdot 1,\ 1\cdot 0-1\cdot 1,\ 1\cdot 1-(-1)\cdot 0)=(-2,-1,1)$；在 $\pi_2$ 内取 $\vec{d_2}=\vec{n_2}\times\vec s=(1\cdot 1-(-1)\cdot 1,\ (-1)\cdot 0-2\cdot 1,\ 2\cdot 1-1\cdot 0)=(2,-2,2)$。两平面夹角即 $\vec{d_1}$ 与 $\vec{d_2}$ 的夹角：$\vec{d_1}\cdot\vec{d_2}=-4+2+2=0$，夹角 $\dfrac{\pi}{2}$。

**答案原文**

$\dfrac{\pi}{2}$（两平面垂直）

## 102. eval-geom-004-s3

内容 SHA256：`ce17c29673ae2987ae71e393a6b8e5a93388c878f617eb17532435e54a45bde6`。

来源：data/v2/eval/dataset_eval.jsonl，第 102 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求两平面 $\pi_1:x-y+z=1$ 与 $\pi_2:2x+y-z=0$ 的夹角。

**过程**

检验 $\pi_2$ 的法向量是否平行于 $\pi_1$ 的方向空间：$\vec{n_2}=(2,1,-1)$ 代入 $\pi_1$ 的齐次方程 $x-y+z$ 得 $2-1-1=0$，说明 $\vec{n_2}$ 是 $\pi_1$ 内的一个方向向量，即一个平面的法向量躺在另一个平面内，这正是两平面垂直的充要条件。

**答案原文**

$\dfrac{\pi}{2}$（两平面垂直）

## 103. eval-geom-005-s1

内容 SHA256：`f6d1d646d979a0e4e723d50309f568fef9538c27bac1176bf7dceb317bd5eff7`。

来源：data/v2/eval/dataset_eval.jsonl，第 103 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求点 $P(2,1,0)$ 到直线 $l:\dfrac{x-1}{1}=\dfrac{y}{2}=\dfrac{z+1}{1}$ 的距离。

**过程**

取直线上点 $P_0(1,0,-1)$、方向向量 $\vec s=(1,2,1)$，$\overrightarrow{P_0P}=(1,1,1)$。叉积 $\overrightarrow{P_0P}\times\vec s=(1\cdot 1-1\cdot 2,\ 1\cdot 1-1\cdot 1,\ 1\cdot 2-1\cdot 1)=(-1,0,1)$，模 $\sqrt{2}$。距离 $d=\dfrac{|\overrightarrow{P_0P}\times\vec s|}{|\vec s|}=\dfrac{\sqrt{2}}{\sqrt{6}}=\dfrac{1}{\sqrt{3}}$。

**答案原文**

$\dfrac{1}{\sqrt{3}}$

## 104. eval-geom-005-s2

内容 SHA256：`32d94c1df6e951d7043e8351dcfd087df6a9377db7a23f8eabe1f30a410d349d`。

来源：data/v2/eval/dataset_eval.jsonl，第 104 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求点 $P(2,1,0)$ 到直线 $l:\dfrac{x-1}{1}=\dfrac{y}{2}=\dfrac{z+1}{1}$ 的距离。

**过程**

直线上点 $Q(t)=(1+t,2t,-1+t)$。$|PQ|^2=(t-1)^2+(2t-1)^2+(t-1)^2=2(t-1)^2+(2t-1)^2=6t^2-8t+3$。配方：$6\left(t-\dfrac{2}{3}\right)^2+\dfrac{1}{3}$，最小值 $\dfrac{1}{3}$ 在 $t=\dfrac{2}{3}$ 处取得，故 $d=\sqrt{\dfrac{1}{3}}=\dfrac{1}{\sqrt{3}}$。

**答案原文**

$\dfrac{1}{\sqrt{3}}$

## 105. eval-geom-005-s3

内容 SHA256：`65e0adb0b834dbad7646424a003b61dbd3c9f561bf91403435024bae71b20c51`。

来源：data/v2/eval/dataset_eval.jsonl，第 105 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求点 $P(2,1,0)$ 到直线 $l:\dfrac{x-1}{1}=\dfrac{y}{2}=\dfrac{z+1}{1}$ 的距离。

**过程**

垂足参数 $t^*=\dfrac{\overrightarrow{P_0P}\cdot\vec s}{|\vec s|^2}=\dfrac{1\cdot 1+1\cdot 2+1\cdot 1}{6}=\dfrac{2}{3}$，垂足 $Q=\left(\dfrac{5}{3},\dfrac{4}{3},-\dfrac{1}{3}\right)$。$d=|PQ|=\sqrt{\left(\dfrac{1}{3}\right)^2+\left(-\dfrac{1}{3}\right)^2+\left(\dfrac{1}{3}\right)^2}=\dfrac{1}{\sqrt{3}}$。检验垂足在直线上：$\dfrac{5/3-1}{1}=\dfrac{4/3}{2}=\dfrac{-1/3+1}{1}=\dfrac{2}{3}$。

**答案原文**

$\dfrac{1}{\sqrt{3}}$

## 106. eval-geom-006-s1

内容 SHA256：`50bd0ef7894ccda1a115d7dda0eabf2367873bc4a7429a2fee485a68cfda9ea3`。

来源：data/v2/eval/dataset_eval.jsonl，第 106 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

讨论三个平面 $\pi_1:x+y+z=1$，$\pi_2:x-y+z=1$，$\pi_3:2x+2z=2$ 的位置关系，并求其公共部分。

**过程**

系数矩阵与增广矩阵行变换：$\begin{pmatrix}1&1&1&1\\1&-1&1&1\\2&0&2&2\end{pmatrix}\to\begin{pmatrix}1&1&1&1\\0&-2&0&0\\0&-2&0&0\end{pmatrix}\to\begin{pmatrix}1&1&1&1\\0&1&0&0\\0&0&0&0\end{pmatrix}$。秩 $\mathrm r(A)=\mathrm r(\bar A)=2<3$，无穷多解，解空间一维：$y=0$，$x+z=1$，即一条直线。

**答案原文**

三平面共线，交线为 $y=0,\ x+z=1$

## 107. eval-geom-006-s2

内容 SHA256：`a0c3757049c864ce0371e86d5fb0354659879a5135ed8ee73788daf6fc58d1f4`。

来源：data/v2/eval/dataset_eval.jsonl，第 107 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

讨论三个平面 $\pi_1:x+y+z=1$，$\pi_2:x-y+z=1$，$\pi_3:2x+2z=2$ 的位置关系，并求其公共部分。

**过程**

观察 $\pi_3$ 的方程恰是 $\pi_1$ 与 $\pi_2$ 方程之和，故 $\pi_3$ 必过 $\pi_1\cap\pi_2$ 的每一点。求 $\pi_1\cap\pi_2$：两式相减得 $2y=0$，$y=0$；代回得 $x+z=1$。故公共部分为直线 $\begin{cases}y=0\\x+z=1\end{cases}$，参数化 $(x,y,z)=(t,0,1-t)$。检验满足 $\pi_3$：$2t+2(1-t)=2$。

**答案原文**

三平面共线，交线为 $y=0,\ x+z=1$

## 108. eval-geom-006-s3

内容 SHA256：`099e31fe72096b91f56a51bf8a0083263b881f41b172b9fb4f0f3d3e59e44589`。

来源：data/v2/eval/dataset_eval.jsonl，第 108 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

讨论三个平面 $\pi_1:x+y+z=1$，$\pi_2:x-y+z=1$，$\pi_3:2x+2z=2$ 的位置关系，并求其公共部分。

**过程**

三个法向量 $\vec{n_1}=(1,1,1)$、$\vec{n_2}=(1,-1,1)$、$\vec{n_3}=(2,0,2)$ 满足 $\vec{n_3}=\vec{n_1}+\vec{n_2}$，故共面。交线方向 $\vec s=\vec{n_1}\times\vec{n_2}=(1\cdot 1-1\cdot(-1),\ 1\cdot 1-1\cdot 1,\ 1\cdot(-1)-1\cdot 1)=(2,0,-2)$，取 $\vec s=(1,0,-1)$。找交线上一点：令 $y=0$，解 $x+z=1$，取 $(1,0,0)$。交线为 $(x,y,z)=(1+t,0,-t)$。

**答案原文**

三平面共线，交线为 $y=0,\ x+z=1$

## 109. eval-geom-007-s1

内容 SHA256：`e7226e09c751e7b8620374e6a23262db19d6d72f28dad8bd5c4781086655a158`。

来源：data/v2/eval/dataset_eval.jsonl，第 109 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

指出方程 $4x^2-y^2+z^2=1$ 表示的二次曲面类型，并用截面法说明其形状。

**过程**

方程化为 $\dfrac{x^2}{1/4}+\dfrac{z^2}{1}-\dfrac{y^2}{1}=1$，形如 $\dfrac{x^2}{a^2}+\dfrac{z^2}{b^2}-\dfrac{y^2}{c^2}=1$（一个负号项），是单叶双曲面，对称轴为 $y$ 轴。

**答案原文**

单叶双曲面（以 $y$ 轴为对称轴）

## 110. eval-geom-007-s2

内容 SHA256：`5fa3415c237f344bcc9ad0de810ae180cbff98de6f82c41e95e6f6f936ca319d`。

来源：data/v2/eval/dataset_eval.jsonl，第 110 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

指出方程 $4x^2-y^2+z^2=1$ 表示的二次曲面类型，并用截面法说明其形状。

**过程**

用 $y=k$ 截：$4x^2+z^2=1+k^2$，即 $\dfrac{x^2}{(1+k^2)/4}+\dfrac{z^2}{1+k^2}=1$，恒为椭圆，且随 $|k|$ 增大而变大（"中间细、两头粗"）。用 $z=k$ 截：$4x^2-y^2=1-k^2$，$|k|<1$ 时为双曲线，$|k|=1$ 时为两相交直线 $y=\pm 2x$，$|k|>1$ 时仍为双曲线（开口换向）。用 $x=k$ 截：$z^2-y^2=1-4k^2$，同为双曲线族。三类截面共同刻画单叶双曲面的"马鞍+束腰"形态。

**答案原文**

单叶双曲面（以 $y$ 轴为对称轴）

## 111. eval-geom-007-s3

内容 SHA256：`97b672208613ea80640305dbfdfc083bf8fadd409868de53cc3304ea0ae70ef8`。

来源：data/v2/eval/dataset_eval.jsonl，第 111 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

指出方程 $4x^2-y^2+z^2=1$ 表示的二次曲面类型，并用截面法说明其形状。

**过程**

构造两族直线（参数 $s$）：$\begin{cases}x=\dfrac{\cos\theta+s\sin\theta}{2}\\y=s\\z=\sin\theta-s\cos\theta\end{cases}$ 与 $\begin{cases}x=\dfrac{\cos\theta-s\sin\theta}{2}\\y=s\\z=\sin\theta+s\cos\theta\end{cases}$。代入验证：$4x^2+z^2-y^2=(\cos\theta\pm s\sin\theta)^2+(\sin\theta\mp s\cos\theta)^2-s^2=\cos^2\theta+\sin^2\theta\pm 2s\sin\theta\cos\theta\mp 2s\sin\theta\cos\theta+s^2(\sin^2\theta+\cos^2\theta)-s^2=1$，整条直线都落在曲面上。直母线族的存在是单叶双曲面的特征性质（双叶双曲面无此性质）。

**答案原文**

单叶双曲面（以 $y$ 轴为对称轴）

## 112. eval-geom-008-s1

内容 SHA256：`45f0a8c7f88e9a8d5078565d7a60c78ed7ce4de2fd4a6f418ca74e8b54586441`。

来源：data/v2/eval/dataset_eval.jsonl，第 112 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

判断二次曲面 $2x^2+y^2-z^2+4xy=1$ 的类型。

**过程**

二次项矩阵 $A=\begin{pmatrix}2&2&0\\2&1&0\\0&0&-1\end{pmatrix}$。$2\times 2$ 块 $\begin{pmatrix}2&2\\2&1\end{pmatrix}$ 的特征方程为 $(2-\lambda)(1-\lambda)-4=0$，即 $\lambda^2-3\lambda-2=0$，特征值 $\lambda_1=\dfrac{3+\sqrt{17}}{2}>0$、$\lambda_2=\dfrac{3-\sqrt{17}}{2}<0$；第三个特征值为 $-1<0$。正惯性指数 $1$、负惯性指数 $2$，对应双叶双曲面。

**答案原文**

双叶双曲面

## 113. eval-geom-008-s2

内容 SHA256：`37f2812aca177039ab86713e1a1e54a1c19d01d0ee82e43fcb6fbe0d1aff534e`。

来源：data/v2/eval/dataset_eval.jsonl，第 113 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

判断二次曲面 $2x^2+y^2-z^2+4xy=1$ 的类型。

**过程**

$2x^2+4xy+y^2=2(x+y)^2-y^2$，故曲面方程为 $2(x+y)^2-y^2-z^2=1$，正平方项 1 个、负平方项 2 个，为双叶双曲面。

**答案原文**

双叶双曲面

## 114. eval-geom-008-s3

内容 SHA256：`352dc1cc2c444c8b6806708c466e98d1089d3a295563b034c22fc804d994aef5`。

来源：data/v2/eval/dataset_eval.jsonl，第 114 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

判断二次曲面 $2x^2+y^2-z^2+4xy=1$ 的类型。

**过程**

用 $z=0$ 截：$2x^2+4xy+y^2=1$，配方为 $2(x+y)^2-y^2=1$，是双曲线；用 $y=0$ 截：$2x^2-z^2=1$，是双曲线；用 $x+y=0$（即 $x=-y$）截：$-y^2-z^2=1$ 无实解——该平面与曲面不相交。三个截面说明曲面在 $z$ 方向与 $x+y$ 方向均为双曲型、且存在与曲面完全不相交的平面（双叶分离的特征）。

**答案原文**

双叶双曲面

## 115. eval-geom-009-s1

内容 SHA256：`d64590d5554a5856995711bd48bc125c8732c29fb79b83814596d8292ad32871`。

来源：data/v2/eval/dataset_eval.jsonl，第 115 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求椭球面 $\dfrac{x^2}{4}+\dfrac{y^2}{9}+z^2=1$ 与平面 $x=1$ 的交线方程，并说明其形状。

**过程**

将 $x=1$ 代入椭球面方程：$\dfrac{1}{4}+\dfrac{y^2}{9}+z^2=1$，即 $\dfrac{y^2}{9}+z^2=\dfrac{3}{4}$。化为标准形 $\dfrac{y^2}{9\cdot\frac{3}{4}}+\dfrac{z^2}{\frac{3}{4}}=1$，即 $\dfrac{y^2}{27/4}+\dfrac{z^2}{3/4}=1$。这是平面 $x=1$ 内的椭圆，半轴分别为 $\sqrt{\dfrac{27}{4}}=\dfrac{3\sqrt{3}}{2}$ 与 $\sqrt{\dfrac{3}{4}}=\dfrac{\sqrt{3}}{2}$，中心 $(1,0,0)$。

**答案原文**

椭圆：$\dfrac{y^2}{27/4}+\dfrac{z^2}{3/4}=1$（$x=1$），半轴 $\dfrac{3\sqrt{3}}{2}$ 与 $\dfrac{\sqrt{3}}{2}$

## 116. eval-geom-009-s2

内容 SHA256：`71a31516a5ad5ffd1da8c78268ea7ec39cdab92509716cb1ee3c346983677669`。

来源：data/v2/eval/dataset_eval.jsonl，第 116 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求椭球面 $\dfrac{x^2}{4}+\dfrac{y^2}{9}+z^2=1$ 与平面 $x=1$ 的交线方程，并说明其形状。

**过程**

由标准形直接参数化：$x=1$，$y=\dfrac{3\sqrt{3}}{2}\cos t$，$z=\dfrac{\sqrt{3}}{2}\sin t$，$t\in[0,2\pi]$。代回验证：$\dfrac{1}{4}+\dfrac{27\cos^2 t}{4\cdot 9}+\dfrac{3\sin^2 t}{4}=\dfrac{1}{4}+\dfrac{3}{4}(\cos^2 t+\sin^2 t)=1$。

**答案原文**

椭圆：$\dfrac{y^2}{27/4}+\dfrac{z^2}{3/4}=1$（$x=1$），半轴 $\dfrac{3\sqrt{3}}{2}$ 与 $\dfrac{\sqrt{3}}{2}$

## 117. eval-geom-009-s3

内容 SHA256：`a9287d16007823e058b70978fd2b0201968f203f5d087496a31f6cab1f946283`。

来源：data/v2/eval/dataset_eval.jsonl，第 117 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求椭球面 $\dfrac{x^2}{4}+\dfrac{y^2}{9}+z^2=1$ 与平面 $x=1$ 的交线方程，并说明其形状。

**过程**

一般截面 $x=k$：$|k|<2$ 时为椭圆 $\dfrac{y^2}{9\left(1-\frac{k^2}{4}\right)}+\dfrac{z^2}{1-\frac{k^2}{4}}=1$，半轴 $3\sqrt{1-\dfrac{k^2}{4}}$ 与 $\sqrt{1-\dfrac{k^2}{4}}$（比值恒为 $3$，故所有截面椭圆相似）；$k=\pm 2$ 时 $1-\dfrac{k^2}{4}=0$，方程仅剩 $y=z=0$，截面退化为单点 $(\pm 2,0,0)$；$|k|>2$ 时无交点。取 $k=1$：半轴 $3\cdot\dfrac{\sqrt{3}}{2}=\dfrac{3\sqrt{3}}{2}$ 与 $\dfrac{\sqrt{3}}{2}$，与解法一一致。

**答案原文**

椭圆：$\dfrac{y^2}{27/4}+\dfrac{z^2}{3/4}=1$（$x=1$），半轴 $\dfrac{3\sqrt{3}}{2}$ 与 $\dfrac{\sqrt{3}}{2}$

## 118. eval-geom-010-s1

内容 SHA256：`aa8562a166703661cba4e9d8509873a2f93ae476b891266dfb4efb0cdf9a3f2f`。

来源：data/v2/eval/dataset_eval.jsonl，第 118 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

说明曲面 $z=xy$ 的类型，并验证它是直纹面。

**过程**

作正交变换 $u=\dfrac{x+y}{\sqrt{2}}$、$v=\dfrac{x-y}{\sqrt{2}}$，则 $x=\dfrac{u+v}{\sqrt{2}}$、$y=\dfrac{u-v}{\sqrt{2}}$，$xy=\dfrac{u^2-v^2}{2}$。曲面方程化为 $z=\dfrac{u^2}{2}-\dfrac{v^2}{2}$，即 $2z=u^2-v^2$，是双曲抛物面（马鞍面）。

**答案原文**

双曲抛物面（马鞍面），直纹面

## 119. eval-geom-010-s2

内容 SHA256：`00fe2d1268b28e1552c4a80cc2b496f553987268956bbec171af74ee289e0953`。

来源：data/v2/eval/dataset_eval.jsonl，第 119 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

说明曲面 $z=xy$ 的类型，并验证它是直纹面。

**过程**

固定 $y=c$：截面 $z=cx$ 是直线；固定 $x=c$：截面 $z=cy$ 也是直线。即曲面上存在两族平行于坐标平面的直线族 $\{z=cx,\ y=c\}$ 与 $\{z=cy,\ x=c\}$，故 $z=xy$ 是直纹面，且每一点处恰有两条直母线通过（交叉直线构成马鞍网格）。

**答案原文**

双曲抛物面（马鞍面），直纹面

## 120. eval-geom-010-s3

内容 SHA256：`442431421378c3af5327306a770982d02e227337fbf5a74430dd73ac20168634`。

来源：data/v2/eval/dataset_eval.jsonl，第 120 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

说明曲面 $z=xy$ 的类型，并验证它是直纹面。

**过程**

用 $y=k$ 截：$z=kx$，对任意 $k$ 都是直线（竖直截面均为直线，直纹性的又一体现）；用 $z=k$ 截：$xy=k$，等轴双曲线（$k\ne 0$）或两坐标轴（$k=0$）；若要抛物线截面，取斜截面 $x=y$（得 $z=x^2$）与 $x=-y$（得 $z=-x^2$）。直线截面与双曲线截面正是双曲抛物面的截面特征。

**答案原文**

双曲抛物面（马鞍面），直纹面

## 121. eval-geom-011-s1

内容 SHA256：`f4634e8a9c2ebdc770af379cfecb5df292b32561cc6205429c798f068f53f20e`。

来源：data/v2/eval/dataset_eval.jsonl，第 121 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求直线 $l:x=1+t,\ y=t,\ z=t$ 与球面 $x^2+y^2+z^2=4$ 的交点个数，并求出交点坐标。

**过程**

代入：$(1+t)^2+t^2+t^2=4$，即 $3t^2+2t-3=0$。判别式 $\Delta=4+36=40>0$，故有两个交点。解出 $t=\dfrac{-2\pm\sqrt{40}}{6}=\dfrac{-1\pm\sqrt{10}}{3}$，对应两点 $\left(1+t,t,t\right)$：$t_1=\dfrac{-1+\sqrt{10}}{3}$ 时 $\left(\dfrac{2+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3}\right)$，$t_2=\dfrac{-1-\sqrt{10}}{3}$ 时 $\left(\dfrac{2-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3}\right)$。

**答案原文**

两个交点：$\left(\dfrac{2+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3}\right)$ 与 $\left(\dfrac{2-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3}\right)$

## 122. eval-geom-011-s2

内容 SHA256：`23ef9ba884a8fb9af9fbf161da9369fd74da2113c09eb9d81929c33f947b6c12`。

来源：data/v2/eval/dataset_eval.jsonl，第 122 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求直线 $l:x=1+t,\ y=t,\ z=t$ 与球面 $x^2+y^2+z^2=4$ 的交点个数，并求出交点坐标。

**过程**

球心 $O(0,0,0)$ 到直线距离：直线上取点 $P_0(1,0,0)$、方向 $\vec s=(1,1,1)$，$\overrightarrow{P_0O}=(-1,0,0)$，叉积 $\overrightarrow{P_0O}\times\vec s=(0\cdot 1-0\cdot 1,\ 0\cdot 1-(-1)\cdot 1,\ (-1)\cdot 1-0\cdot 1)=(0,1,-1)$，模 $\sqrt{2}$，故 $d=\dfrac{\sqrt{2}}{\sqrt{3}}=\sqrt{\dfrac{2}{3}}<2$，直线与球面相交于两点。相交弦长 $=2\sqrt{4-\dfrac{2}{3}}=2\sqrt{\dfrac{10}{3}}$，与解法一中两参数差对应的长度 $|t_1-t_2|\cdot|\vec s|=\dfrac{2\sqrt{10}}{3}\cdot\sqrt{3}=2\sqrt{\dfrac{10}{3}}$ 一致。

**答案原文**

两个交点：$\left(\dfrac{2+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3}\right)$ 与 $\left(\dfrac{2-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3}\right)$

## 123. eval-geom-011-s3

内容 SHA256：`e33e27915bec20910b99b728ab8420d815892df8828d97363ff6d08b5e3d3fe1`。

来源：data/v2/eval/dataset_eval.jsonl，第 123 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求直线 $l:x=1+t,\ y=t,\ z=t$ 与球面 $x^2+y^2+z^2=4$ 的交点个数，并求出交点坐标。

**过程**

$3t^2+2t-3=3\left(t+\dfrac{1}{3}\right)^2-\dfrac{10}{3}=0$，故 $t+\dfrac{1}{3}=\pm\dfrac{\sqrt{10}}{3}$，$t=\dfrac{-1\pm\sqrt{10}}{3}$，与解法一相同。

**答案原文**

两个交点：$\left(\dfrac{2+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3}\right)$ 与 $\left(\dfrac{2-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3}\right)$

## 124. eval-geom-012-s1

内容 SHA256：`d13f0e1983942db3fcddd80f44389e739be45bd86b4360924206508e64b22cc1`。

来源：data/v2/eval/dataset_eval.jsonl，第 124 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求圆柱螺线 $x=a\cos t,\ y=a\sin t,\ z=bt$（$a,b>0$）的曲率与挠率。

**过程**

记 $c=\sqrt{a^2+b^2}$。$\vec r'=(-a\sin t,a\cos t,b)$，$|\vec r'|=c$；$\vec r''=(-a\cos t,-a\sin t,0)$；$\vec r'\times\vec r''=(ab\sin t,-ab\cos t,a^2)$，模 $\sqrt{a^2b^2+a^4}=ac$。曲率 $\kappa=\dfrac{|\vec r'\times\vec r''|}{|\vec r'|^3}=\dfrac{ac}{c^3}=\dfrac{a}{c^2}=\dfrac{a}{a^2+b^2}$。又 $\vec r'''=(a\sin t,-a\cos t,0)$，挠率 $\tau=\dfrac{(\vec r',\vec r'',\vec r''')}{|\vec r'\times\vec r''|^2}=\dfrac{a^2b\sin^2 t+a^2b\cos^2 t}{a^2c^2}=\dfrac{b}{c^2}=\dfrac{b}{a^2+b^2}$。

**答案原文**

曲率 $\kappa=\dfrac{a}{a^2+b^2}$，挠率 $\tau=\dfrac{b}{a^2+b^2}$

## 125. eval-geom-012-s2

内容 SHA256：`9ea9f22dad4244e0b99e17031ee852cbd215d78e4128a5d8ef590f78698a3678`。

来源：data/v2/eval/dataset_eval.jsonl，第 125 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求圆柱螺线 $x=a\cos t,\ y=a\sin t,\ z=bt$（$a,b>0$）的曲率与挠率。

**过程**

速度 $\vec v=\vec r'$，模 $|\vec v|=c$ 恒定，故切向加速度为 $0$；加速度 $\vec a=\vec r''=(-a\cos t,-a\sin t,0)$，模 $|\vec a|=a$。由 $|\vec a|=\kappa|\vec v|^2$ 得 $\kappa=\dfrac{a}{c^2}=\dfrac{a}{a^2+b^2}$。副法向量 $\vec B=\dfrac{\vec r'\times\vec r''}{|\vec r'\times\vec r''|}=\dfrac{1}{c}(b\sin t,-b\cos t,a)$，$\dfrac{d\vec B}{dt}=\dfrac{1}{c}(b\cos t,b\sin t,0)$，模 $\dfrac{b}{c}$。由 Frenet 公式 $\dfrac{d\vec B}{ds}=-\tau\vec N$ 核对方向（本题 $\dfrac{d\vec B}{ds}$ 与 $-\vec N$ 同向，故 $\tau>0$），且 $\left|\dfrac{d\vec B}{ds}\right|=\tau$、$\dfrac{ds}{dt}=c$，得 $\tau=\dfrac{b/c}{c}=\dfrac{b}{a^2+b^2}$。

**答案原文**

曲率 $\kappa=\dfrac{a}{a^2+b^2}$，挠率 $\tau=\dfrac{b}{a^2+b^2}$

## 126. eval-geom-012-s3

内容 SHA256：`88a85d372a5ad391306a72b14badb5d390a370834e5c2cc90d09060ae18675c4`。

来源：data/v2/eval/dataset_eval.jsonl，第 126 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求圆柱螺线 $x=a\cos t,\ y=a\sin t,\ z=bt$（$a,b>0$）的曲率与挠率。

**过程**

把圆柱面沿一条母线剪开展平，螺线变成一条直线，其与水平方向的夹角 $\alpha$ 满足 $\tan\alpha=\dfrac{b}{a}$（螺距 $2\pi b$ 与周长 $2\pi a$ 之比），故 $\cos^2\alpha=\dfrac{a^2}{a^2+b^2}$。螺线的曲率完全来自柱面弯曲：$\kappa=\dfrac{\cos^2\alpha}{a}=\dfrac{a}{a^2+b^2}$；挠率来自螺线"扭转"：$\tau=\dfrac{\sin\alpha\cos\alpha}{a}=\dfrac{b}{a^2+b^2}$。$\dfrac{\tau}{\kappa}=\dfrac{b}{a}$ 为常数，说明圆柱螺线是常曲率常挠率曲线。

**答案原文**

曲率 $\kappa=\dfrac{a}{a^2+b^2}$，挠率 $\tau=\dfrac{b}{a^2+b^2}$

## 127. eval-geom-013-s1

内容 SHA256：`53eb52ab1e842a543a5da809161a3356c36e8376c57588f92cfaf8d62d3cc8a1`。

来源：data/v2/eval/dataset_eval.jsonl，第 127 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求曲面 $z=x^2+y^2$ 在点 $(1,1,2)$ 处的切平面与法线方程。

**过程**

令 $F(x,y,z)=z-x^2-y^2$，曲面为 $F=0$。$\nabla F=(-2x,-2y,1)$，在 $(1,1,2)$ 处为 $\vec n=(-2,-2,1)$。切平面：$-2(x-1)-2(y-1)+1\cdot(z-2)=0$，即 $2x+2y-z=2$。法线：$\dfrac{x-1}{-2}=\dfrac{y-1}{-2}=\dfrac{z-2}{1}$。

**答案原文**

切平面 $2x+2y-z=2$；法线 $\dfrac{x-1}{-2}=\dfrac{y-1}{-2}=\dfrac{z-2}{1}$

## 128. eval-geom-013-s2

内容 SHA256：`05db41d5d5de3c7885ca83ea7d9df66ecfd7b67eafd30bdfd1736379a50a443c`。

来源：data/v2/eval/dataset_eval.jsonl，第 128 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求曲面 $z=x^2+y^2$ 在点 $(1,1,2)$ 处的切平面与法线方程。

**过程**

$dz=2x\,dx+2y\,dy$，在 $(1,1)$ 处 $dz=2dx+2dy$。切平面为 $z-2=2(x-1)+2(y-1)$，即 $2x+2y-z=2$。法线方向由 $(dx,dy,dz)$ 与 $(2,2,-1)$ 垂直得出：法向 $(2,2,-1)$，法线方程同上。

**答案原文**

切平面 $2x+2y-z=2$；法线 $\dfrac{x-1}{-2}=\dfrac{y-1}{-2}=\dfrac{z-2}{1}$

## 129. eval-geom-013-s3

内容 SHA256：`02cb920c982085395fb9d33344e305ae5d2596c663b5d925fa096593d70357cc`。

来源：data/v2/eval/dataset_eval.jsonl，第 129 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求曲面 $z=x^2+y^2$ 在点 $(1,1,2)$ 处的切平面与法线方程。

**过程**

参数化 $\vec r(u,v)=(u,v,u^2+v^2)$。$\vec r_u=(1,0,2u)$，$\vec r_v=(0,1,2v)$，在 $(u,v)=(1,1)$ 处为 $(1,0,2)$、$(0,1,2)$。切平面法向量 $\vec r_u\times\vec r_v=(0\cdot 2-2\cdot 1,\ 2\cdot 0-1\cdot 2,\ 1\cdot 1-0\cdot 0)=(-2,-2,1)$，与解法一一致，切平面、法线同上。

**答案原文**

切平面 $2x+2y-z=2$；法线 $\dfrac{x-1}{-2}=\dfrac{y-1}{-2}=\dfrac{z-2}{1}$

## 130. eval-geom-014-s1

内容 SHA256：`5489dda0efb1cd7f754fc04e8f96ebbadfee09409f78e5938531f71b7874e9e9`。

来源：data/v2/eval/dataset_eval.jsonl，第 130 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求椭圆 $\dfrac{x^2}{4}+\dfrac{y^2}{9}=1$ 在点 $\left(\sqrt{2},\dfrac{3}{\sqrt{2}}\right)$ 处的切线方程。

**过程**

椭圆上点 $(x_0,y_0)$ 处的切线为 $\dfrac{xx_0}{4}+\dfrac{yy_0}{9}=1$。代入 $\left(\sqrt{2},\dfrac{3}{\sqrt{2}}\right)$：$\dfrac{\sqrt{2}}{4}x+\dfrac{3}{9\sqrt{2}}y=1$，即 $\dfrac{\sqrt{2}}{4}x+\dfrac{1}{3\sqrt{2}}y=1$。两边乘 $12\sqrt{2}$：$6x+4y=12\sqrt{2}$，即 $3x+2y=6\sqrt{2}$。检验切点在切线上：$3\sqrt{2}+2\cdot\dfrac{3}{\sqrt{2}}=3\sqrt{2}+3\sqrt{2}=6\sqrt{2}$。

**答案原文**

$3x+2y=6\sqrt{2}$

## 131. eval-geom-014-s2

内容 SHA256：`0639398145ab5cc0f58f4977e231c9cd896e4dd10298339805230410e468f758`。

来源：data/v2/eval/dataset_eval.jsonl，第 131 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求椭圆 $\dfrac{x^2}{4}+\dfrac{y^2}{9}=1$ 在点 $\left(\sqrt{2},\dfrac{3}{\sqrt{2}}\right)$ 处的切线方程。

**过程**

两边对 $x$ 求导：$\dfrac{2x}{4}+\dfrac{2y}{9}y'=0$，得 $y'=-\dfrac{9x}{4y}$。在 $\left(\sqrt{2},\dfrac{3}{\sqrt{2}}\right)$ 处 $y'=-\dfrac{9\sqrt{2}}{4\cdot\frac{3}{\sqrt{2}}}=-\dfrac{9\cdot 2}{12}=-\dfrac{3}{2}$。切线：$y-\dfrac{3}{\sqrt{2}}=-\dfrac{3}{2}(x-\sqrt{2})$，整理得 $2y-\dfrac{6}{\sqrt{2}}=-3x+3\sqrt{2}$，即 $3x+2y=3\sqrt{2}+3\sqrt{2}=6\sqrt{2}$。

**答案原文**

$3x+2y=6\sqrt{2}$

## 132. eval-geom-014-s3

内容 SHA256：`365960066144c312c1dd8b5f7683ff4e249b7d85be24a9534594e0700f179d0c`。

来源：data/v2/eval/dataset_eval.jsonl，第 132 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求椭圆 $\dfrac{x^2}{4}+\dfrac{y^2}{9}=1$ 在点 $\left(\sqrt{2},\dfrac{3}{\sqrt{2}}\right)$ 处的切线方程。

**过程**

参数化 $x=2\cos t$、$y=3\sin t$。切点处 $\cos t=\dfrac{\sqrt{2}}{2}$、$\sin t=\dfrac{1}{\sqrt{2}}$，即 $t=\dfrac{\pi}{4}$。切线斜率 $\dfrac{dy}{dx}=\dfrac{3\cos t}{-2\sin t}$，在 $t=\dfrac{\pi}{4}$ 处为 $-\dfrac{3}{2}$。切线方程同解法二，即 $3x+2y=6\sqrt{2}$。

**答案原文**

$3x+2y=6\sqrt{2}$

## 133. eval-geom-015-s1

内容 SHA256：`03eaf29a4945a688b261f6aa8152d622f13f410b2416dc731c48db4fd80ed2cb`。

来源：data/v2/eval/dataset_eval.jsonl，第 133 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求两球面 $x^2+y^2+z^2=4$ 与 $x^2+(y-1)^2+z^2=4$ 的交线方程。

**过程**

两方程相减：$x^2+y^2+z^2-\left[x^2+(y-1)^2+z^2\right]=0$，即 $y^2-(y^2-2y+1)=0$，得 $2y-1=0$，$y=\dfrac{1}{2}$。代入第一式：$x^2+z^2=4-\dfrac{1}{4}=\dfrac{15}{4}$。交线为平面 $y=\dfrac{1}{2}$ 上的圆 $x^2+z^2=\dfrac{15}{4}$。

**答案原文**

圆：$y=\dfrac{1}{2}$，$x^2+z^2=\dfrac{15}{4}$（圆心 $\left(0,\dfrac{1}{2},0\right)$，半径 $\dfrac{\sqrt{15}}{2}$）

## 134. eval-geom-015-s2

内容 SHA256：`a60fe56d074b0cea62d7491fa6733edb8cde9629a4a5cda2bcb4d07405864e5c`。

来源：data/v2/eval/dataset_eval.jsonl，第 134 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求两球面 $x^2+y^2+z^2=4$ 与 $x^2+(y-1)^2+z^2=4$ 的交线方程。

**过程**

两球半径相等（均为 $2$），故交线圆所在平面是两球心连线的垂直平分面。球心 $O_1(0,0,0)$、$O_2(0,1,0)$，垂直平分面为 $y=\dfrac{1}{2}$。球心 $O_1$ 到该平面的距离为 $\dfrac{1}{2}$，故截面圆半径 $\sqrt{2^2-\left(\dfrac{1}{2}\right)^2}=\dfrac{\sqrt{15}}{2}$，圆心 $\left(0,\dfrac{1}{2},0\right)$。

**答案原文**

圆：$y=\dfrac{1}{2}$，$x^2+z^2=\dfrac{15}{4}$（圆心 $\left(0,\dfrac{1}{2},0\right)$，半径 $\dfrac{\sqrt{15}}{2}$）

## 135. eval-geom-015-s3

内容 SHA256：`c2a94f4ef12ae71e990748a21dee00d5759d88ae705cf5e19e9fa8018659949e`。

来源：data/v2/eval/dataset_eval.jsonl，第 135 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求两球面 $x^2+y^2+z^2=4$ 与 $x^2+(y-1)^2+z^2=4$ 的交线方程。

**过程**

由圆方程直接参数化：$x=\dfrac{\sqrt{15}}{2}\cos t$，$y=\dfrac{1}{2}$，$z=\dfrac{\sqrt{15}}{2}\sin t$，$t\in[0,2\pi]$。代回两球面验证：$x^2+y^2+z^2=\dfrac{15}{4}+\dfrac{1}{4}=4$；$x^2+(y-1)^2+z^2=\dfrac{15}{4}+\dfrac{1}{4}=4$。

**答案原文**

圆：$y=\dfrac{1}{2}$，$x^2+z^2=\dfrac{15}{4}$（圆心 $\left(0,\dfrac{1}{2},0\right)$，半径 $\dfrac{\sqrt{15}}{2}$）

## 136. eval-geom-016-s1

内容 SHA256：`53042c63239e3ccf1400310a7583936fb6936709e1fb15f80e7e63d9260c8a61`。

来源：data/v2/eval/dataset_eval.jsonl，第 136 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

已知 $|\vec a|=2$，$|\vec b|=3$，$\vec a$ 与 $\vec b$ 的夹角为 $60^\circ$，求 $|\vec a+\vec b|$、$|2\vec a-\vec b|$ 及 $\vec a+\vec b$ 与 $\vec a-\vec b$ 的夹角余弦。

**过程**

$|\vec a+\vec b|^2=|\vec a|^2+|\vec b|^2+2|\vec a||\vec b|\cos 60^\circ=4+9+2\cdot 2\cdot 3\cdot\dfrac{1}{2}=19$，故 $|\vec a+\vec b|=\sqrt{19}$。$|2\vec a-\vec b|^2=4|\vec a|^2+|\vec b|^2-4|\vec a||\vec b|\cos 60^\circ=16+9-12=13$，故 $|2\vec a-\vec b|=\sqrt{13}$。又 $(\vec a+\vec b)\cdot(\vec a-\vec b)=|\vec a|^2-|\vec b|^2=4-9=-5$，$|\vec a-\vec b|^2=4+9-2\cdot 2\cdot 3\cdot\dfrac{1}{2}=7$，故 $\cos\theta=\dfrac{-5}{\sqrt{19}\cdot\sqrt{7}}=-\dfrac{5}{\sqrt{133}}$。

**答案原文**

$|\vec a+\vec b|=\sqrt{19}$，$|2\vec a-\vec b|=\sqrt{13}$，$\cos\theta=-\dfrac{5}{\sqrt{133}}$

## 137. eval-geom-016-s2

内容 SHA256：`e855b10438ab6c3ce780e8741062b60a90659658cbc52bde05ee5aaf632a0778`。

来源：data/v2/eval/dataset_eval.jsonl，第 137 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

已知 $|\vec a|=2$，$|\vec b|=3$，$\vec a$ 与 $\vec b$ 的夹角为 $60^\circ$，求 $|\vec a+\vec b|$、$|2\vec a-\vec b|$ 及 $\vec a+\vec b$ 与 $\vec a-\vec b$ 的夹角余弦。

**过程**

取 $\vec a=(2,0)$，$\vec b=\left(\dfrac{3}{2},\dfrac{3\sqrt{3}}{2}\right)$。则 $\vec a+\vec b=\left(\dfrac{7}{2},\dfrac{3\sqrt{3}}{2}\right)$，$|\vec a+\vec b|^2=\dfrac{49}{4}+\dfrac{27}{4}=19$；$2\vec a-\vec b=\left(\dfrac{5}{2},-\dfrac{3\sqrt{3}}{2}\right)$，模平方 $\dfrac{25}{4}+\dfrac{27}{4}=13$；$\vec a-\vec b=\left(\dfrac{1}{2},-\dfrac{3\sqrt{3}}{2}\right)$，$(\vec a+\vec b)\cdot(\vec a-\vec b)=\dfrac{7}{4}-\dfrac{27}{4}=-5$，与解法一一致。

**答案原文**

$|\vec a+\vec b|=\sqrt{19}$，$|2\vec a-\vec b|=\sqrt{13}$，$\cos\theta=-\dfrac{5}{\sqrt{133}}$

## 138. eval-geom-016-s3

内容 SHA256：`6fc3a4568d1cd47b29fc562bed5e8b6ada61bda34cd7083ff4f23f729c2b61d8`。

来源：data/v2/eval/dataset_eval.jsonl，第 138 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

已知 $|\vec a|=2$，$|\vec b|=3$，$\vec a$ 与 $\vec b$ 的夹角为 $60^\circ$，求 $|\vec a+\vec b|$、$|2\vec a-\vec b|$ 及 $\vec a+\vec b$ 与 $\vec a-\vec b$ 的夹角余弦。

**过程**

以 $\vec a,\vec b$ 为邻边作平行四边形，对角线长为 $|\vec a+\vec b|$ 与 $|\vec a-\vec b|$。由余弦定理：$|\vec a+\vec b|^2=2^2+3^2-2\cdot 2\cdot 3\cos 120^\circ=19$（补角 $120^\circ$），$|\vec a-\vec b|^2=2^2+3^2-2\cdot 2\cdot 3\cos 60^\circ=7$。$2\vec a-\vec b$ 可用三角形法则：以 $2\vec a$ 与 $-\vec b$ 为边，$|2\vec a-\vec b|^2=16+9-2\cdot 4\cdot 3\cdot\dfrac{1}{2}=13$。夹角余弦由点积公式同解法一。

**答案原文**

$|\vec a+\vec b|=\sqrt{19}$，$|2\vec a-\vec b|=\sqrt{13}$，$\cos\theta=-\dfrac{5}{\sqrt{133}}$

## 139. eval-geom-017-s1

内容 SHA256：`14a52912b4df0e1fcc0aa53292307ce91dbbea98bd7aff76d77fda0105d8e563`。

来源：data/v2/eval/dataset_eval.jsonl，第 139 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

已知 $\vec a=(1,2,2)$，$\vec b=(-2,1,2)$，求 $\vec a$ 与 $\vec b$ 的夹角余弦及 $\vec a$ 在 $\vec b$ 上的投影向量。

**过程**

$\vec a\cdot\vec b=1\cdot(-2)+2\cdot 1+2\cdot 2=4$，$|\vec a|=\sqrt{1+4+4}=3$，$|\vec b|=\sqrt{4+1+4}=3$，故 $\cos\theta=\dfrac{4}{3\cdot 3}=\dfrac{4}{9}$。投影向量 $\mathrm{proj}_{\vec b}\vec a=\dfrac{\vec a\cdot\vec b}{|\vec b|^2}\vec b=\dfrac{4}{9}(-2,1,2)=\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)$。

**答案原文**

$\cos\theta=\dfrac{4}{9}$；投影向量 $\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)$

## 140. eval-geom-017-s2

内容 SHA256：`ae1242a3265f54def93f3a49bce9719d3675785e74a7cc4522392a21dd242eb9`。

来源：data/v2/eval/dataset_eval.jsonl，第 140 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

已知 $\vec a=(1,2,2)$，$\vec b=(-2,1,2)$，求 $\vec a$ 与 $\vec b$ 的夹角余弦及 $\vec a$ 在 $\vec b$ 上的投影向量。

**过程**

投影长度 $|\vec a|\cos\theta=3\cdot\dfrac{4}{9}=\dfrac{4}{3}$，方向为 $\dfrac{\vec b}{|\vec b|}=\dfrac{1}{3}(-2,1,2)$，故投影向量 $=\dfrac{4}{3}\cdot\dfrac{1}{3}(-2,1,2)=\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)$。

**答案原文**

$\cos\theta=\dfrac{4}{9}$；投影向量 $\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)$

## 141. eval-geom-017-s3

内容 SHA256：`52a8d2e012af4c2ab18fc9b5ce9325203070a4c196ed407c74ccd39386306004`。

来源：data/v2/eval/dataset_eval.jsonl，第 141 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

已知 $\vec a=(1,2,2)$，$\vec b=(-2,1,2)$，求 $\vec a$ 与 $\vec b$ 的夹角余弦及 $\vec a$ 在 $\vec b$ 上的投影向量。

**过程**

取单位向量 $\vec u=\dfrac{\vec b}{3}=\left(-\dfrac{2}{3},\dfrac{1}{3},\dfrac{2}{3}\right)$，则 $\vec a=\left(\vec a\cdot\vec u\right)\vec u+\vec a_\perp$，其中 $\vec a\cdot\vec u=\dfrac{4}{3}$，$\vec a_\perp=\vec a-\dfrac{4}{3}\vec u=(1,2,2)-\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)=\left(\dfrac{17}{9},\dfrac{14}{9},\dfrac{10}{9}\right)$。验证 $\vec a_\perp\cdot\vec b=\dfrac{17}{9}\cdot(-2)+\dfrac{14}{9}\cdot 1+\dfrac{10}{9}\cdot 2=\dfrac{-34+14+20}{9}=0$，正交分解成立，投影分量即 $\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)$。

**答案原文**

$\cos\theta=\dfrac{4}{9}$；投影向量 $\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)$

## 142. eval-geom-018-s1

内容 SHA256：`e3761b05f084278aa40650e8f6dc014ce53489bb237720e2ad7392843542ec99`。

来源：data/v2/eval/dataset_eval.jsonl，第 142 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求以 $O(0,0,0)$、$A(2,0,0)$、$B(0,3,0)$、$C(0,0,4)$ 为顶点的四面体体积。

**过程**

$V=\dfrac{1}{6}\left|\det(\overrightarrow{OA},\overrightarrow{OB},\overrightarrow{OC})\right|=\dfrac{1}{6}\left|\begin{vmatrix}2&0&0\\0&3&0\\0&0&4\end{vmatrix}\right|=\dfrac{24}{6}=4$。

**答案原文**

$4$

## 143. eval-geom-018-s2

内容 SHA256：`3d3644bccdac88bac60f7ce2d695823f26c76a2573c2ea31a05eb0bd7682eb6f`。

来源：data/v2/eval/dataset_eval.jsonl，第 143 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求以 $O(0,0,0)$、$A(2,0,0)$、$B(0,3,0)$、$C(0,0,4)$ 为顶点的四面体体积。

**过程**

取底面 $OAB$：面积 $S=\dfrac{1}{2}\cdot 2\cdot 3=3$。顶点 $C$ 到平面 $xOy$ 的距离即高 $h=4$。故 $V=\dfrac{1}{3}Sh=\dfrac{1}{3}\cdot 3\cdot 4=4$。

**答案原文**

$4$

## 144. eval-geom-018-s3

内容 SHA256：`acd19617682cc46f8be40ce6b52122e5db4be4b31807af3bdf489faa696a4f72`。

来源：data/v2/eval/dataset_eval.jsonl，第 144 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求以 $O(0,0,0)$、$A(2,0,0)$、$B(0,3,0)$、$C(0,0,4)$ 为顶点的四面体体积。

**过程**

四面体区域为 $\dfrac{x}{2}+\dfrac{y}{3}+\dfrac{z}{4}\le 1$、$x,y,z\ge 0$。作线性替换 $u=\dfrac{x}{2}$、$v=\dfrac{y}{3}$、$w=\dfrac{z}{4}$（雅可比行列式 $\dfrac{\partial(x,y,z)}{\partial(u,v,w)}=2\cdot 3\cdot 4=24$），区域变为 $u+v+w\le 1$、$u,v,w\ge 0$。$V=\displaystyle\iiint dx\,dy\,dz=24\iiint du\,dv\,dw=24\cdot\dfrac{1}{6}=4$（单位单纯形 $u+v+w\le 1,\ u,v,w\ge 0$ 的体积为 $\dfrac{1}{6}$）。

**答案原文**

$4$

## 145. eval-geom-019-s1

内容 SHA256：`4341b2be611ff64e175a214582b5697c44c1955ae21cae0bed2cd3663b36f2d3`。

来源：data/v2/eval/dataset_eval.jsonl，第 145 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求两平面 $\pi_1:x+y+z=1$ 与 $\pi_2:x+2y+3z=6$ 的交线方程。

**过程**

方向向量 $\vec s=\vec{n_1}\times\vec{n_2}=(1,1,1)\times(1,2,3)=(1\cdot 3-1\cdot 2,\ 1\cdot 1-1\cdot 3,\ 1\cdot 2-1\cdot 1)=(1,-2,1)$。求交线上一点：令 $z=0$，解 $\begin{cases}x+y=1\\x+2y=6\end{cases}$，两式相减得 $y=5$、$x=-4$，得点 $P_0(-4,5,0)$。交线为 $\dfrac{x+4}{1}=\dfrac{y-5}{-2}=\dfrac{z}{1}$。

**答案原文**

$\dfrac{x+4}{1}=\dfrac{y-5}{-2}=\dfrac{z}{1}$，即 $(x,y,z)=(-4+t,5-2t,t)$

## 146. eval-geom-019-s2

内容 SHA256：`a5357195d5a04c503b86db91cc4dade06635064055b3b81aad8982577117e059`。

来源：data/v2/eval/dataset_eval.jsonl，第 146 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求两平面 $\pi_1:x+y+z=1$ 与 $\pi_2:x+2y+3z=6$ 的交线方程。

**过程**

方程组 $\begin{cases}x+y+z=1\\x+2y+3z=6\end{cases}$。第二式减第一式：$y+2z=5$，即 $y=5-2z$；代回第一式：$x+5-2z+z=1$，$x=z-4$。令 $z=t$，得参数方程 $(x,y,z)=(t-4,5-2t,t)=(-4+t,5-2t,t)$。

**答案原文**

$\dfrac{x+4}{1}=\dfrac{y-5}{-2}=\dfrac{z}{1}$，即 $(x,y,z)=(-4+t,5-2t,t)$

## 147. eval-geom-019-s3

内容 SHA256：`576ed0fa52fef5de7ae0eeddccfc86e910d4689a26b0cdbf0a867f7b496d061b`。

来源：data/v2/eval/dataset_eval.jsonl，第 147 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求两平面 $\pi_1:x+y+z=1$ 与 $\pi_2:x+2y+3z=6$ 的交线方程。

**过程**

由解法一/二得 $(x,y,z)=(-4+t,5-2t,t)$。代入 $\pi_1$：$(-4+t)+(5-2t)+t=1$；代入 $\pi_2$：$(-4+t)+2(5-2t)+3t=-4+t+10-4t+3t=6$。两式恒成立，故确为交线。

**答案原文**

$\dfrac{x+4}{1}=\dfrac{y-5}{-2}=\dfrac{z}{1}$，即 $(x,y,z)=(-4+t,5-2t,t)$

## 148. eval-geom-020-s1

内容 SHA256：`5b7c23882ec60aecc0efa3c26ebd56313dc9ca4bdbe12e57385550e86db92920`。

来源：data/v2/eval/dataset_eval.jsonl，第 148 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

判断四点 $A(1,2,3)$、$B(2,3,4)$、$C(3,5,7)$、$D(2,4,6)$ 是否共面。

**过程**

$\overrightarrow{AB}=(1,1,1)$，$\overrightarrow{AC}=(2,3,4)$，$\overrightarrow{AD}=(1,2,3)$。混合积 $\det(\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD})=\begin{vmatrix}1&1&1\\2&3&4\\1&2&3\end{vmatrix}=1\cdot(9-8)-1\cdot(6-4)+1\cdot(4-3)=1-2+1=0$，故四点共面。

**答案原文**

共面

## 149. eval-geom-020-s2

内容 SHA256：`fff8f60686b3c6e873b9f5356b26c6711712ce6977f67d22be3ccfaebaf41761`。

来源：data/v2/eval/dataset_eval.jsonl，第 149 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

判断四点 $A(1,2,3)$、$B(2,3,4)$、$C(3,5,7)$、$D(2,4,6)$ 是否共面。

**过程**

过 $A,B,C$ 的平面法向量 $\vec n=\overrightarrow{AB}\times\overrightarrow{AC}=(1,1,1)\times(2,3,4)=(1\cdot 4-1\cdot 3,\ 1\cdot 2-1\cdot 4,\ 1\cdot 3-1\cdot 2)=(1,-2,1)$。平面方程：$(x-1)-2(y-2)+(z-3)=0$，即 $x-2y+z=0$。代入 $D(2,4,6)$：$2-8+6=0$，满足方程，故 $D$ 在平面 $ABC$ 上，四点共面。

**答案原文**

共面

## 150. eval-geom-020-s3

内容 SHA256：`a70b0ad41d9fd2ef786be4fb8c88ca4b384d53c78b2aaec69cc78681c1601b6c`。

来源：data/v2/eval/dataset_eval.jsonl，第 150 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

判断四点 $A(1,2,3)$、$B(2,3,4)$、$C(3,5,7)$、$D(2,4,6)$ 是否共面。

**过程**

检查 $\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}$ 是否线性相关。设 $k_1(1,1,1)+k_2(2,3,4)+k_3(1,2,3)=(0,0,0)$，即 $\begin{cases}k_1+2k_2+k_3=0\\k_1+3k_2+2k_3=0\\k_1+4k_2+3k_3=0\end{cases}$。第二式减第一式、第三式减第二式均得 $k_2+k_3=0$，取 $k_2=1$、$k_3=-1$，则 $k_1=-1$。验证 $-(1,1,1)+(2,3,4)-(1,2,3)=(0,0,0)$，存在非零解，故三向量线性相关，四点共面。

**答案原文**

共面

## 151. eval-prob-001-s1

内容 SHA256：`8a6962b797338f5c619633cd90dd9257c87ac1252802f36edc1d69469888eb72`。

来源：data/v2/eval/dataset_eval.jsonl，第 151 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

三门问题：参赛者在三扇门中选择一扇（其中一扇后有汽车，另两扇后是山羊）。主持人（知道车在哪）打开另一扇有山羊的门，给参赛者一次换门机会。问换门获胜的概率是多少？并解释原因。

**过程**

参赛者初始选中山羊的概率为 $\dfrac{2}{3}$，此时主持人必须打开另一扇山羊门（他不能开车门），剩下的未开门必然是汽车，换门必赢。初始选中汽车的概率为 $\dfrac{1}{3}$，此时换门必输。故换门获胜概率 $=\dfrac{2}{3}\times 1+\dfrac{1}{3}\times 0=\dfrac{2}{3}$。

**答案原文**

换门获胜概率为 $\dfrac{2}{3}$，不换为 $\dfrac{1}{3}$

## 152. eval-prob-001-s2

内容 SHA256：`559fdc65c9bbc228c521eea8f7a6de5b489d7656f7930dea84751c099d892c00`。

来源：data/v2/eval/dataset_eval.jsonl，第 152 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

三门问题：参赛者在三扇门中选择一扇（其中一扇后有汽车，另两扇后是山羊）。主持人（知道车在哪）打开另一扇有山羊的门，给参赛者一次换门机会。问换门获胜的概率是多少？并解释原因。

**过程**

设参赛者选 1 号门、主持人打开 2 号门，并假设主持人在有两扇羊门可选时等概率选择（其余情形由对称性同理）。记 $C_i$=车在 $i$ 号门，$H_2$=主持人开 2 号门。则 $P(H_2|C_3)=1$（车在 3 号门时主持人只能开 2 号门），$P(H_2|C_1)=\dfrac{1}{2}$（车在 1 号门时主持人可在 2、3 号门中等概率选择），$P(H_2|C_2)=0$（主持人不能开有车的门），$P(C_i)=\dfrac{1}{3}$。由贝叶斯公式：$P(C_3|H_2)=\dfrac{P(H_2|C_3)P(C_3)}{P(H_2|C_3)P(C_3)+P(H_2|C_1)P(C_1)+P(H_2|C_2)P(C_2)}=\dfrac{1\cdot\frac{1}{3}}{1\cdot\frac{1}{3}+\frac{1}{2}\cdot\frac{1}{3}+0}=\dfrac{1/3}{1/2}=\dfrac{2}{3}$。即主持人开 2 号门后，车在 3 号门（换门目标）的概率为 $\dfrac{2}{3}$。注意"总是换门"的获胜率 $\dfrac{2}{3}$ 其实不依赖主持人的等概率规则（见解法一）。

**答案原文**

换门获胜概率为 $\dfrac{2}{3}$，不换为 $\dfrac{1}{3}$

## 153. eval-prob-001-s3

内容 SHA256：`b5c4f752d5526c8e9021d23a0b8821aa2305e9863aef903c38ccd86a35329adb`。

来源：data/v2/eval/dataset_eval.jsonl，第 153 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

三门问题：参赛者在三扇门中选择一扇（其中一扇后有汽车，另两扇后是山羊）。主持人（知道车在哪）打开另一扇有山羊的门，给参赛者一次换门机会。问换门获胜的概率是多少？并解释原因。

**过程**

车的位置（3 种）×参赛者初选（3 种）=9 种等可能情形。逐项枚举：参赛者初选=车门（3 种情形），换门必输；参赛者初选=山羊门（6 种情形），换门必赢。故换门获胜概率 $=\dfrac{6}{9}=\dfrac{2}{3}$。

**答案原文**

换门获胜概率为 $\dfrac{2}{3}$，不换为 $\dfrac{1}{3}$

## 154. eval-prob-002-s1

内容 SHA256：`ede480b26a3ec9f7fc8ab2e19cdab035397b3b74763e0821129f735e2bcaf5bb`。

来源：data/v2/eval/dataset_eval.jsonl，第 154 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

三个盒子：甲盒装 2 枚金币，乙盒装 2 枚银币，丙盒装 1 金 1 银。随机选一个盒子再从中随机摸出一枚硬币，发现是金币。问：该盒子中另一枚硬币也是金币的概率是多少？

**过程**

记 $A$=摸到金币，$B_1,B_2,B_3$=分别选中甲盒（双金）、乙盒（双银）、丙盒（一金一银）。$P(B_i)=\dfrac{1}{3}$，$P(A|B_1)=1$，$P(A|B_2)=0$，$P(A|B_3)=\dfrac{1}{2}$。$P(B_1|A)=\dfrac{P(A|B_1)P(B_1)}{P(A|B_1)P(B_1)+P(A|B_2)P(B_2)+P(A|B_3)P(B_3)}=\dfrac{1\cdot\frac{1}{3}}{1\cdot\frac{1}{3}+0\cdot\frac{1}{3}+\frac{1}{2}\cdot\frac{1}{3}}=\dfrac{1/3}{1/2}=\dfrac{2}{3}$。

**答案原文**

$\dfrac{2}{3}$

## 155. eval-prob-002-s2

内容 SHA256：`29972a9b3eda037d564e6f24c22aa7f6dc91a61c2412b816b626f87c6c6b5761`。

来源：data/v2/eval/dataset_eval.jsonl，第 155 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

三个盒子：甲盒装 2 枚金币，乙盒装 2 枚银币，丙盒装 1 金 1 银。随机选一个盒子再从中随机摸出一枚硬币，发现是金币。问：该盒子中另一枚硬币也是金币的概率是多少？

**过程**

6 枚硬币等可能地被摸到。已知摸到的是金币，则它必是 3 枚金币之一，且 3 枚金币等可能。其中 2 枚来自甲盒（另一枚也是金），1 枚来自丙盒（另一枚是银）。故所求概率 $=\dfrac{2}{3}$。

**答案原文**

$\dfrac{2}{3}$

## 156. eval-prob-002-s3

内容 SHA256：`a5bdb4887ae8902aa6f10c84503484a2574d460e4b3d2ad7d5ca8d8a1549f28c`。

来源：data/v2/eval/dataset_eval.jsonl，第 156 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

三个盒子：甲盒装 2 枚金币，乙盒装 2 枚银币，丙盒装 1 金 1 银。随机选一个盒子再从中随机摸出一枚硬币，发现是金币。问：该盒子中另一枚硬币也是金币的概率是多少？

**过程**

第一层：选盒，各 $\dfrac{1}{3}$；第二层：甲盒内摸到金概率 1（路径概率 $\dfrac{1}{3}$），丙盒内摸到金概率 $\dfrac{1}{2}$（路径概率 $\dfrac{1}{6}$），乙盒为 0。摸到金的总概率 $\dfrac{1}{3}+\dfrac{1}{6}=\dfrac{1}{2}$；其中来自甲盒的占比 $\dfrac{1/3}{1/2}=\dfrac{2}{3}$。

**答案原文**

$\dfrac{2}{3}$

## 157. eval-prob-003-s1

内容 SHA256：`b29345bfc98d46938fa92dde2f2f89c2aa95f8799ef56290b57ee42da62ae18d`。

来源：data/v2/eval/dataset_eval.jsonl，第 157 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

抛一枚均匀硬币直到出现正面为止，求抛掷次数的期望（几何分布期望）。

**过程**

设 $X\sim\operatorname{Geom}\!\left(\dfrac{1}{2}\right)$，$P(X=n)=q^{n-1}p=\left(\dfrac{1}{2}\right)^n$。$E[X]=\displaystyle\sum_{n=1}^{\infty}n\left(\dfrac{1}{2}\right)^n$。由 eval-calc-021 的错位相减（或幂级数 $\sum nx^{n-1}=\dfrac{1}{(1-x)^2}$ 取 $x=\dfrac{1}{2}$），得 $E[X]=\dfrac{1/2}{(1-1/2)^2}=2$。

**答案原文**

$2$

## 158. eval-prob-003-s2

内容 SHA256：`d72a4bf7943cc0a78133aad0031a96cba5afd72dae5d276c30bfaba40014f736`。

来源：data/v2/eval/dataset_eval.jsonl，第 158 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

抛一枚均匀硬币直到出现正面为止，求抛掷次数的期望（几何分布期望）。

**过程**

记 $E$ 为首次正面所需次数的期望。第一次若为正面（概率 $\dfrac{1}{2}$），总次数为 1；若为反面（概率 $\dfrac{1}{2}$），则"回到原点"，总次数为 $1+E$。故 $E=\dfrac{1}{2}\cdot 1+\dfrac{1}{2}\cdot(1+E)=1+\dfrac{E}{2}$，解得 $E=2$。

**答案原文**

$2$

## 159. eval-prob-003-s3

内容 SHA256：`3daf034117150091f0dceadb90520dba56e7a4d451d9d3fd26e0424b5bb41799`。

来源：data/v2/eval/dataset_eval.jsonl，第 159 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

抛一枚均匀硬币直到出现正面为止，求抛掷次数的期望（几何分布期望）。

**过程**

概率母函数 $G(z)=E[z^X]=\displaystyle\sum_{n=1}^{\infty}z^nq^{n-1}p=\dfrac{pz}{1-qz}$。$G'(z)=\dfrac{p(1-qz)+pqz}{(1-qz)^2}=\dfrac{p}{(1-qz)^2}$，故 $E[X]=G'(1)=\dfrac{p}{(1-q)^2}=\dfrac{1}{p}=2$（$p=q=\dfrac{1}{2}$）。

**答案原文**

$2$

## 160. eval-prob-004-s1

内容 SHA256：`b0ae862b287d060cfdb1b578797d851f9c02d5c01a8bf9771fe6381de85be17f`。

来源：data/v2/eval/dataset_eval.jsonl，第 160 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

掷一枚均匀骰子两次，设 $X$ 为第一次点数，$Y$ 为两次点数之和。求 $P(Y\ge 8\mid X=3)$ 与 $E[Y\mid X=3]$。

**过程**

给定 $X=3$，第二次点数 $Z$ 在 $\{1,2,3,4,5,6\}$ 上等可能。$Y=3+Z\ge 8\iff Z\ge 5$，故 $P(Y\ge 8|X=3)=P(Z\in\{5,6\})=\dfrac{2}{6}=\dfrac{1}{3}$。$E[Y|X=3]=3+E[Z]=3+\dfrac{7}{2}=\dfrac{13}{2}$。

**答案原文**

$P(Y\ge 8\mid X=3)=\dfrac{1}{3}$；$E[Y\mid X=3]=\dfrac{13}{2}$

## 161. eval-prob-004-s2

内容 SHA256：`e11d9aeb329ee7caa68bc6607cb1ce6b394335a3d8e215536977cba5f05bd14a`。

来源：data/v2/eval/dataset_eval.jsonl，第 161 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

掷一枚均匀骰子两次，设 $X$ 为第一次点数，$Y$ 为两次点数之和。求 $P(Y\ge 8\mid X=3)$ 与 $E[Y\mid X=3]$。

**过程**

$P(Y\ge 8|X=3)=\dfrac{P(X=3,Y\ge 8)}{P(X=3)}$。$P(X=3)=\dfrac{1}{6}$；事件 $\{X=3,Y\ge 8\}$ 即 $\{X=3,Z\ge 5\}$，由独立性 $P=\dfrac{1}{6}\cdot\dfrac{2}{6}=\dfrac{1}{18}$。故条件概率 $=\dfrac{1/18}{1/6}=\dfrac{1}{3}$。同理 $E[Y|X=3]=\dfrac{1}{P(X=3)}\displaystyle\sum_z(3+z)P(X=3)P(Z=z)=\sum_z(3+z)\cdot\dfrac{1}{6}=\dfrac{13}{2}$。

**答案原文**

$P(Y\ge 8\mid X=3)=\dfrac{1}{3}$；$E[Y\mid X=3]=\dfrac{13}{2}$

## 162. eval-prob-004-s3

内容 SHA256：`dc7a1ed6e0723d41d5fbd8857ad4b6a9167c320e50d4ca52922bf5b00db4fb31`。

来源：data/v2/eval/dataset_eval.jsonl，第 162 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

掷一枚均匀骰子两次，设 $X$ 为第一次点数，$Y$ 为两次点数之和。求 $P(Y\ge 8\mid X=3)$ 与 $E[Y\mid X=3]$。

**过程**

第一层固定 $X=3$，第二层 $Z\in\{1,\dots,6\}$ 各 $\dfrac{1}{6}$。数出 $Z\ge 5$ 的分支两条，概率 $\dfrac{2}{6}$；所有分支的 $Y$ 值平均为 $\dfrac{4+5+6+7+8+9}{6}=\dfrac{39}{6}=\dfrac{13}{2}$。

**答案原文**

$P(Y\ge 8\mid X=3)=\dfrac{1}{3}$；$E[Y\mid X=3]=\dfrac{13}{2}$

## 163. eval-prob-005-s1

内容 SHA256：`fb4ad38768236a8014e14e462b85e084d5088490d8319ca3e0f0a50fd4de36e7`。

来源：data/v2/eval/dataset_eval.jsonl，第 163 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $X\sim U(0,1)$（区间 $(0,1)$ 上的均匀分布），求 $Y=-\ln X$ 的分布。

**过程**

$F_Y(y)=P(Y\le y)=P(-\ln X\le y)=P(X\ge e^{-y})=1-e^{-y}$（$y>0$，用到 $X$ 的分布函数 $F_X(x)=x$ 于 $(0,1)$）。对 $y$ 求导：$f_Y(y)=e^{-y}$（$y>0$），即 $Y\sim\operatorname{Exp}(1)$。

**答案原文**

$Y\sim\operatorname{Exp}(1)$，密度 $f_Y(y)=e^{-y}$（$y>0$）

## 164. eval-prob-005-s2

内容 SHA256：`72f0968ca8a9c5e8309c7da27872546c6f776d209bf205269422e1789e61331e`。

来源：data/v2/eval/dataset_eval.jsonl，第 164 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $X\sim U(0,1)$（区间 $(0,1)$ 上的均匀分布），求 $Y=-\ln X$ 的分布。

**过程**

$y=g(x)=-\ln x$ 在 $(0,1)$ 上严格递减，反函数 $x=h(y)=e^{-y}$（$y>0$），$|h'(y)|=e^{-y}$。由变换公式 $f_Y(y)=f_X(h(y))\cdot|h'(y)|=1\cdot e^{-y}=e^{-y}$（$y>0$）。

**答案原文**

$Y\sim\operatorname{Exp}(1)$，密度 $f_Y(y)=e^{-y}$（$y>0$）

## 165. eval-prob-005-s3

内容 SHA256：`1eecb044c71415a2d53ca10e022925103ae342e0b4000b4f42ae646233bef8b9`。

来源：data/v2/eval/dataset_eval.jsonl，第 165 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $X\sim U(0,1)$（区间 $(0,1)$ 上的均匀分布），求 $Y=-\ln X$ 的分布。

**过程**

指数分布 $\operatorname{Exp}(1)$ 的分布函数为 $F(y)=1-e^{-y}$，其反函数 $F^{-1}(u)=-\ln(1-u)$。由于 $1-X$ 与 $X$ 同分布，$-\ln X$ 与 $F^{-1}(X)$ 同分布，故 $Y\sim\operatorname{Exp}(1)$。这正是计算机生成指数随机数的标准方法（逆变换法）。

**答案原文**

$Y\sim\operatorname{Exp}(1)$，密度 $f_Y(y)=e^{-y}$（$y>0$）

## 166. eval-prob-006-s1

内容 SHA256：`76f842a2814fb3004934f77484f6b19dfefb278f94514a01974e52f7259f7780`。

来源：data/v2/eval/dataset_eval.jsonl，第 166 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $X\sim\operatorname{Poisson}(\lambda)$，求 $E[X^2]$，并由此求 $\operatorname{Var}(X)$。

**过程**

$E[X^2]=\displaystyle\sum_{k=0}^{\infty}k^2\cdot\dfrac{\lambda^ke^{-\lambda}}{k!}=\sum_{k=0}^{\infty}\left[k(k-1)+k\right]\dfrac{\lambda^ke^{-\lambda}}{k!}=e^{-\lambda}\left[\lambda^2\sum_{k=2}^{\infty}\dfrac{\lambda^{k-2}}{(k-2)!}+\lambda\sum_{k=1}^{\infty}\dfrac{\lambda^{k-1}}{(k-1)!}\right]=e^{-\lambda}\left[\lambda^2e^{\lambda}+\lambda e^{\lambda}\right]=\lambda^2+\lambda$。故 $\operatorname{Var}(X)=E[X^2]-(E[X])^2=\lambda^2+\lambda-\lambda^2=\lambda$。

**答案原文**

$E[X^2]=\lambda^2+\lambda$，$\operatorname{Var}(X)=\lambda$

## 167. eval-prob-006-s2

内容 SHA256：`85d197cbc336db9c3c121ad1e6b4cfa8613b92ac67d00eda7042b886581ff154`。

来源：data/v2/eval/dataset_eval.jsonl，第 167 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $X\sim\operatorname{Poisson}(\lambda)$，求 $E[X^2]$，并由此求 $\operatorname{Var}(X)$。

**过程**

$E[X(X-1)]=\displaystyle\sum_{k=2}^{\infty}k(k-1)\dfrac{\lambda^ke^{-\lambda}}{k!}=e^{-\lambda}\lambda^2\sum_{k=2}^{\infty}\dfrac{\lambda^{k-2}}{(k-2)!}=\lambda^2$。故 $E[X^2]=E[X(X-1)]+E[X]=\lambda^2+\lambda$，$\operatorname{Var}(X)=\lambda$。

**答案原文**

$E[X^2]=\lambda^2+\lambda$，$\operatorname{Var}(X)=\lambda$

## 168. eval-prob-006-s3

内容 SHA256：`45f3ceab56427cadaad3633d5ab0db10e68a06bb3544d15994b175a316391291`。

来源：data/v2/eval/dataset_eval.jsonl，第 168 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $X\sim\operatorname{Poisson}(\lambda)$，求 $E[X^2]$，并由此求 $\operatorname{Var}(X)$。

**过程**

$M(t)=E[e^{tX}]=e^{\lambda(e^t-1)}$。$M'(t)=M(t)\cdot\lambda e^t$，$M''(t)=M(t)\left[(\lambda e^t)^2+\lambda e^t\right]$。$E[X]=M'(0)=\lambda$，$E[X^2]=M''(0)=\lambda^2+\lambda$，$\operatorname{Var}(X)=M''(0)-[M'(0)]^2=\lambda$。

**答案原文**

$E[X^2]=\lambda^2+\lambda$，$\operatorname{Var}(X)=\lambda$

## 169. eval-prob-007-s1

内容 SHA256：`dbf1e3e350bbc690714bda3cd0439898a9e2c2c2a20d68823f56a0cff1bdd261`。

来源：data/v2/eval/dataset_eval.jsonl，第 169 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

房间里随机聚集 30 个人（假设生日在一年 365 天中等可能且相互独立）。求至少有两人生日相同的概率。

**过程**

记 $A$=至少两人生日相同。$\bar A$=30 人生日全不同。依次安排生日：第 1 人 $365$ 种，第 2 人 $364$ 种，$\dots$，第 30 人 $336$ 种。$P(\bar A)=\dfrac{365\cdot 364\cdots 336}{365^{30}}$。故 $P(A)=1-\dfrac{365\cdot 364\cdots 336}{365^{30}}=1-0.29368\cdots\approx 0.7063$。

**答案原文**

$1-\dfrac{365\cdot 364\cdots 336}{365^{30}}\approx 0.7063$

## 170. eval-prob-007-s2

内容 SHA256：`5357a1cfab9a5e40d33960542abd04f3bc54cac788bc337b6631affa317bb108`。

来源：data/v2/eval/dataset_eval.jsonl，第 170 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

房间里随机聚集 30 个人（假设生日在一年 365 天中等可能且相互独立）。求至少有两人生日相同的概率。

**过程**

记 $p_k$=前 $k$ 人生日全不同的概率。$p_1=1$，$p_k=p_{k-1}\cdot\dfrac{365-(k-1)}{365}$。依次计算：$p_{10}\approx 0.88305$，$p_{20}\approx 0.58856$，$p_{23}\approx 0.49270$（第 23 人时首次低于 $\dfrac{1}{2}$），$p_{30}\approx 0.29368$。故 $P(A)=1-p_{30}\approx 0.70632$。

**答案原文**

$1-\dfrac{365\cdot 364\cdots 336}{365^{30}}\approx 0.7063$

## 171. eval-prob-007-s3

内容 SHA256：`c71ea80078b89385e233680200c91144eada4e33193fc452e40afb0894957821`。

来源：data/v2/eval/dataset_eval.jsonl，第 171 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

房间里随机聚集 30 个人（假设生日在一年 365 天中等可能且相互独立）。求至少有两人生日相同的概率。

**过程**

30 人两两配对共 $C_{30}^2=435$ 对，每对生日相同的概率恰为 $\dfrac{1}{365}$，由期望线性性，"生日相同对数"的期望精确等于 $\dfrac{435}{365}=\dfrac{87}{73}\approx 1.19$。期望已大于 1，从侧面印证 $P(A)$ 较大；精确概率仍由解法一的对立事件公式给出。

**答案原文**

$1-\dfrac{365\cdot 364\cdots 336}{365^{30}}\approx 0.7063$

## 172. eval-prob-008-s1

内容 SHA256：`4355811836c02d671e8021e65fc07ff94d593bcf03db820a3ff28a08037630d0`。

来源：data/v2/eval/dataset_eval.jsonl，第 172 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $X\sim B\!\left(100,\dfrac{1}{2}\right)$。用切比雪夫不等式给出 $P(|X-50|\ge 10)$ 的上界，并与精确值比较。

**过程**

$E[X]=np=50$，$\operatorname{Var}(X)=np(1-p)=25$。由切比雪夫不等式 $P(|X-E[X]|\ge\varepsilon)\le\dfrac{\operatorname{Var}(X)}{\varepsilon^2}$，取 $\varepsilon=10$：$P(|X-50|\ge 10)\le\dfrac{25}{100}=\dfrac{1}{4}$。

**答案原文**

切比雪夫上界 $\dfrac{1}{4}$；精确值 $2\displaystyle\sum_{k=0}^{40}\binom{100}{k}\left(\frac{1}{2}\right)^{100}\approx 0.0569$

## 173. eval-prob-008-s2

内容 SHA256：`e59b6925c8dfeb4e5bc80ca22ede65eab2d0aceb280151582b3b3053053f2f79`。

来源：data/v2/eval/dataset_eval.jsonl，第 173 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $X\sim B\!\left(100,\dfrac{1}{2}\right)$。用切比雪夫不等式给出 $P(|X-50|\ge 10)$ 的上界，并与精确值比较。

**过程**

$P(|X-50|\ge 10)=P(X\le 40)+P(X\ge 60)$。由对称性（$p=\dfrac{1}{2}$），$P(X\ge 60)=P(X\le 40)$（$X$ 与 $100-X$ 同分布），故 $P=2P(X\le 40)=2\displaystyle\sum_{k=0}^{40}\binom{100}{k}\left(\dfrac{1}{2}\right)^{100}\approx 0.0569$。

**答案原文**

切比雪夫上界 $\dfrac{1}{4}$；精确值 $2\displaystyle\sum_{k=0}^{40}\binom{100}{k}\left(\frac{1}{2}\right)^{100}\approx 0.0569$

## 174. eval-prob-008-s3

内容 SHA256：`63378544b8e5013d992954d8f6edfefe368963b64a35c4e6099ecffeec65cc8b`。

来源：data/v2/eval/dataset_eval.jsonl，第 174 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $X\sim B\!\left(100,\dfrac{1}{2}\right)$。用切比雪夫不等式给出 $P(|X-50|\ge 10)$ 的上界，并与精确值比较。

**过程**

切比雪夫上界 $0.25$ 只需均值与方差、对任何同均值方差的分布都成立（通用性），但远松于精确值 $0.0569$；精确计算需要完整的二项分布信息（专用性）。两者之差 $0.193$ 体现了"分布无关界"与"分布相关值"的代价差。动画可并排展示两种结果的对比条。

**答案原文**

切比雪夫上界 $\dfrac{1}{4}$；精确值 $2\displaystyle\sum_{k=0}^{40}\binom{100}{k}\left(\frac{1}{2}\right)^{100}\approx 0.0569$

## 175. eval-prob-009-s1

内容 SHA256：`42268f90e33056a0513bbaa5ed43bec66d20bfd3a1a725792d529369742c14ec`。

来源：data/v2/eval/dataset_eval.jsonl，第 175 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $X,Y$ 相互独立且均服从 $\operatorname{Exp}(1)$，求 $Z=\min(X,Y)$ 的分布。

**过程**

$P(Z>z)=P(X>z,Y>z)=P(X>z)P(Y>z)=e^{-z}\cdot e^{-z}=e^{-2z}$（$z>0$，由独立性）。故 $F_Z(z)=1-e^{-2z}$，$f_Z(z)=2e^{-2z}$，即 $Z\sim\operatorname{Exp}(2)$。

**答案原文**

$Z\sim\operatorname{Exp}(2)$，密度 $f_Z(z)=2e^{-2z}$（$z>0$）

## 176. eval-prob-009-s2

内容 SHA256：`c8bcf6caac2e2f24786b62f789bb298a3941b0f1a8c1677513740ed0c77ac249`。

来源：data/v2/eval/dataset_eval.jsonl，第 176 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $X,Y$ 相互独立且均服从 $\operatorname{Exp}(1)$，求 $Z=\min(X,Y)$ 的分布。

**过程**

最小值的密度公式：$f_Z(z)=2f(z)[1-F(z)]$，其中 $f(z)=e^{-z}$、$F(z)=1-e^{-z}$ 为 $\operatorname{Exp}(1)$ 的密度与分布函数。故 $f_Z(z)=2e^{-z}\cdot e^{-z}=2e^{-2z}$。

**答案原文**

$Z\sim\operatorname{Exp}(2)$，密度 $f_Z(z)=2e^{-2z}$（$z>0$）

## 177. eval-prob-009-s3

内容 SHA256：`6af298328ee07d463f1ac3680fb6d5f80240e8760a36382c907e14a643937c91`。

来源：data/v2/eval/dataset_eval.jsonl，第 177 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $X,Y$ 相互独立且均服从 $\operatorname{Exp}(1)$，求 $Z=\min(X,Y)$ 的分布。

**过程**

联合密度 $f(x,y)=e^{-x-y}$（$x,y>0$）。$P(Z>z)=\displaystyle\int_z^\infty\!\!\int_z^\infty e^{-x-y}\,dx\,dy=\left(\int_z^\infty e^{-x}dx\right)\left(\int_z^\infty e^{-y}dy\right)=e^{-z}\cdot e^{-z}=e^{-2z}$，与解法一一致。

**答案原文**

$Z\sim\operatorname{Exp}(2)$，密度 $f_Z(z)=2e^{-2z}$（$z>0$）

## 178. eval-prob-010-s1

内容 SHA256：`ec51a795355ca6b20ff75528a2c1e7a17815cafa4860766a52bcaaa99a58df29`。

来源：data/v2/eval/dataset_eval.jsonl，第 178 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

$n$ 个人各带一顶帽子，帽子随机打乱后每人随机取回一顶（全排列等可能）。求取到自己帽子的人数的期望，并说明该期望不依赖 $n$ 的原因。

**过程**

设 $I_i$ 为"第 $i$ 人取到自己帽子"的指示变量。由对称性，第 $i$ 人取到自己帽子的概率 $P(I_i=1)=\dfrac{1}{n}$（$n$ 顶帽子中恰有一顶属于他，均匀排列下等可能）。总正确人数 $X=I_1+\cdots+I_n$，由期望线性性（**不要求独立性**）：$E[X]=\displaystyle\sum_{i=1}^{n}E[I_i]=\sum_{i=1}^{n}P(I_i=1)=n\cdot\dfrac{1}{n}=1$。

**答案原文**

$1$（与 $n$ 无关）

## 179. eval-prob-010-s2

内容 SHA256：`8f754f2479e650f96e3ba5fc2336e87f7af5fb4ba674df8496818a3c226371ae`。

来源：data/v2/eval/dataset_eval.jsonl，第 179 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

$n$ 个人各带一顶帽子，帽子随机打乱后每人随机取回一顶（全排列等可能）。求取到自己帽子的人数的期望，并说明该期望不依赖 $n$ 的原因。

**过程**

恰有 $k$ 人取对的概率 $P(X=k)=\dfrac{\binom{n}{k}D(n-k)}{n!}$，其中 $D(m)=m!\displaystyle\sum_{j=0}^{m}\dfrac{(-1)^j}{j!}$ 为错排数。生成函数 $G(z)=\displaystyle\sum_{k=0}^{n}\dfrac{\binom{n}{k}D(n-k)}{n!}z^k$。$E[X]=G'(1)=\dfrac{1}{n!}\displaystyle\sum_{k=1}^{n}k\binom{n}{k}D(n-k)=\dfrac{n}{n!}\sum_{k=1}^{n}\binom{n-1}{k-1}D(n-k)=\dfrac{1}{(n-1)!}\sum_{j=0}^{n-1}\binom{n-1}{j}D(n-1-j)$。而 $\displaystyle\sum_{j=0}^{n-1}\binom{n-1}{j}D(n-1-j)=(n-1)!$（对 $n-1$ 个元素的所有排列按"不动点个数 $j$"分类计数），故 $E[X]=1$。

**答案原文**

$1$（与 $n$ 无关）

## 180. eval-prob-010-s3

内容 SHA256：`6e199f7a5443e2b1c6fbd7d6f9a944a38e3110a02bac81f20b7fa03dbcfe8092`。

来源：data/v2/eval/dataset_eval.jsonl，第 180 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

$n$ 个人各带一顶帽子，帽子随机打乱后每人随机取回一顶（全排列等可能）。求取到自己帽子的人数的期望，并说明该期望不依赖 $n$ 的原因。

**过程**

对全部 $n!$ 种排列统计"拿对帽子"的总人次：对任意固定的第 $i$ 人，其帽子被自己拿到的排列数为 $(n-1)!$（其余 $n-1$ 顶帽子任意排列），故总固定点数 $=\displaystyle\sum_{i=1}^{n}(n-1)!=n\cdot(n-1)!=n!$。除以排列总数 $n!$，得期望 $=\dfrac{n!}{n!}=1$。期望不随 $n$ 变化的本质是"每顶帽子命中率恒为 $\dfrac{1}{n}$、恰好 $n$ 顶"。

**答案原文**

$1$（与 $n$ 无关）

## 181. eval-prob-011-s1

内容 SHA256：`e835a8efcdbe83a9b0b728d299343ecd30ed739eca0c247d608c2d4070a1a116`。

来源：data/v2/eval/dataset_eval.jsonl，第 181 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

抛均匀硬币直到连续出现两次正面（HH）为止，求所需抛掷次数的期望。

**过程**

设 $E_0$=当前无连续正面记录时的期望剩余次数，$E_1$=刚出现一次正面时的期望剩余次数。状态转移：$E_0=1+\dfrac{1}{2}E_0+\dfrac{1}{2}E_1$（抛一次后：反面回 $E_0$，正面进 $E_1$）；$E_1=1+\dfrac{1}{2}\cdot 0+\dfrac{1}{2}E_0$（再抛：正面完成，反面回 $E_0$）。由第二式 $E_1=1+\dfrac{E_0}{2}$，代入第一式：$E_0=1+\dfrac{E_0}{2}+\dfrac{1}{2}\left(1+\dfrac{E_0}{2}\right)=\dfrac{3}{2}+\dfrac{3E_0}{4}$，解得 $E_0=6$。

**答案原文**

$6$

## 182. eval-prob-011-s2

内容 SHA256：`ba23401daec88fc8717001f57a0c63a50b289fe7c9d28dccfaaf92f6dad07b1a`。

来源：data/v2/eval/dataset_eval.jsonl，第 182 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

抛均匀硬币直到连续出现两次正面（HH）为止，求所需抛掷次数的期望。

**过程**

状态 $\{0,1,H\}$（$H$ 为吸收态），转移矩阵 $P=\begin{pmatrix}1/2&1/2&0\\1/2&0&1/2\\0&0&1\end{pmatrix}$，瞬态子矩阵 $Q=\begin{pmatrix}1/2&1/2\\1/2&0\end{pmatrix}$。基本矩阵 $N=(I-Q)^{-1}=\begin{pmatrix}1/2&-1/2\\-1/2&1\end{pmatrix}^{-1}=4\begin{pmatrix}1&1/2\\1/2&1/2\end{pmatrix}=\begin{pmatrix}4&2\\2&2\end{pmatrix}$（$\det(I-Q)=\dfrac{1}{2}-\dfrac{1}{4}=\dfrac{1}{4}$）。从状态 0 出发的期望步数为 $N$ 第 1 行之和 $=4+2=6$。

**答案原文**

$6$

## 183. eval-prob-011-s3

内容 SHA256：`0c5c95af01fab9975ee051e214c46b6c9cbd96e2680779dc9cab0e339782c199`。

来源：data/v2/eval/dataset_eval.jsonl，第 183 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

抛均匀硬币直到连续出现两次正面（HH）为止，求所需抛掷次数的期望。

**过程**

首次出现 HH 的时刻 $T\ge 2$，其分布为 $P(T=k)=\dfrac{F_{k-1}}{2^k}$（$k\ge 2$），其中 $F_1=F_2=1$ 为斐波那契数（$k$ 次抛掷中前 $k-1$ 次无 HH 且第 $k$ 次前恰为 $\dots H$ 的计数即斐波那契递推）。概率母函数 $G(z)=\displaystyle\sum_{k=2}^{\infty}\dfrac{F_{k-1}}{2^k}z^k=\dfrac{z^2}{4-2z-z^2}$（由 $\sum_{m\ge 1}F_mx^m=\dfrac{x}{1-x-x^2}$ 代入 $x=\dfrac{z}{2}$ 得）。$E[T]=G'(1)=\left.\dfrac{2z(4-2z-z^2)+z^2(2+2z)}{(4-2z-z^2)^2}\right|_{z=1}=\dfrac{2\cdot 1+4}{1}=6$。

**答案原文**

$6$

## 184. eval-prob-012-s1

内容 SHA256：`c83686784155c92bcb637ab12e02e7be3842c6d6e3c9a34b5a0146f69ecc71f0`。

来源：data/v2/eval/dataset_eval.jsonl，第 184 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $X,Y$ 相互独立且均服从 $U(0,1)$，求 $P(X+Y\le 1)$。

**过程**

$(X,Y)$ 在单位正方形 $[0,1]^2$ 上均匀分布。事件 $\{X+Y\le 1\}$ 对应正方形中直线 $x+y=1$ 左下方的等腰直角三角形，面积 $\dfrac{1}{2}\cdot 1\cdot 1=\dfrac{1}{2}$。均匀分布下概率=面积比，故 $P=\dfrac{1}{2}$。

**答案原文**

$\dfrac{1}{2}$

## 185. eval-prob-012-s2

内容 SHA256：`e31f9d6401059c692b2d1f5c65878721644bf410153fed4ff526ad021bdb309b`。

来源：data/v2/eval/dataset_eval.jsonl，第 185 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $X,Y$ 相互独立且均服从 $U(0,1)$，求 $P(X+Y\le 1)$。

**过程**

$Z=X+Y$ 的密度为卷积：$f_Z(z)=\displaystyle\int_{-\infty}^{\infty}f_X(x)f_Y(z-x)dx=\int_0^1\mathbf 1_{[0,1]}(z-x)dx$。当 $0<z<1$：$f_Z(z)=\displaystyle\int_0^z dx=z$；当 $1<z<2$：$f_Z(z)=\displaystyle\int_{z-1}^1 dx=2-z$（三角分布）。故 $P(X+Y\le 1)=\displaystyle\int_0^1 z\,dz=\dfrac{1}{2}$。

**答案原文**

$\dfrac{1}{2}$

## 186. eval-prob-012-s3

内容 SHA256：`dffd3decd10771ac78afba5fafe86fcb2e689087e688adb04953a14624dd2348`。

来源：data/v2/eval/dataset_eval.jsonl，第 186 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $X,Y$ 相互独立且均服从 $U(0,1)$，求 $P(X+Y\le 1)$。

**过程**

$(X,Y)$ 与 $(1-X,1-Y)$ 同分布。$X+Y\le 1\iff (1-X)+(1-Y)\ge 1$，且 $P(X+Y=1)=0$。故 $P(X+Y\le 1)=P(X+Y\ge 1)=\dfrac{1}{2}$（两事件互补且等概率）。

**答案原文**

$\dfrac{1}{2}$

## 187. eval-prob-013-s1

内容 SHA256：`b7297bfff5774af295c76f6ce2fda60a7d2396246edb38556b483afd3697be00`。

来源：data/v2/eval/dataset_eval.jsonl，第 187 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $X\sim N(0,1)$（标准正态分布），求 $E|X|$。

**过程**

$E|X|=\displaystyle\int_{-\infty}^{\infty}|x|\dfrac{1}{\sqrt{2\pi}}e^{-x^2/2}dx=\dfrac{2}{\sqrt{2\pi}}\int_0^{\infty}xe^{-x^2/2}dx$。令 $u=\dfrac{x^2}{2}$（$du=x\,dx$）：$=\dfrac{2}{\sqrt{2\pi}}\displaystyle\int_0^{\infty}e^{-u}du=\dfrac{2}{\sqrt{2\pi}}\cdot 1=\sqrt{\dfrac{2}{\pi}}$。

**答案原文**

$\sqrt{\dfrac{2}{\pi}}$

## 188. eval-prob-013-s2

内容 SHA256：`a47d79c10e70743827f31ca0178446525b6f5491c1126098237e6c56df221d14`。

来源：data/v2/eval/dataset_eval.jsonl，第 188 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $X\sim N(0,1)$（标准正态分布），求 $E|X|$。

**过程**

$|X|$ 服从半正态分布，密度 $f(y)=\dfrac{2}{\sqrt{2\pi}}e^{-y^2/2}$（$y>0$，即把负半轴密度折叠到正半轴）。$E|X|=\displaystyle\int_0^\infty y\dfrac{2}{\sqrt{2\pi}}e^{-y^2/2}dy=\dfrac{2}{\sqrt{2\pi}}\left[-e^{-y^2/2}\right]_0^\infty=\dfrac{2}{\sqrt{2\pi}}=\sqrt{\dfrac{2}{\pi}}$。

**答案原文**

$\sqrt{\dfrac{2}{\pi}}$

## 189. eval-prob-013-s3

内容 SHA256：`9083312a30021cc46a6af4336ee5c9b8eedfb89de3fb6e155b58aa52a92a9574`。

来源：data/v2/eval/dataset_eval.jsonl，第 189 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $X\sim N(0,1)$（标准正态分布），求 $E|X|$。

**过程**

$Y=X^2\sim\chi^2(1)$，密度 $f_Y(y)=\dfrac{1}{\sqrt{2\pi}}y^{-1/2}e^{-y/2}$（$y>0$）。$E|X|=E[\sqrt{Y}]=\displaystyle\int_0^\infty\sqrt{y}\cdot\dfrac{1}{\sqrt{2\pi}}y^{-1/2}e^{-y/2}dy=\dfrac{1}{\sqrt{2\pi}}\int_0^\infty e^{-y/2}dy=\dfrac{1}{\sqrt{2\pi}}\cdot 2=\sqrt{\dfrac{2}{\pi}}$。

**答案原文**

$\sqrt{\dfrac{2}{\pi}}$

## 190. eval-prob-014-s1

内容 SHA256：`e1dfeffb95da1b3cc771087d8bcccd44d5cd74523a1c553b4229b5d3f078a87f`。

来源：data/v2/eval/dataset_eval.jsonl，第 190 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $X\sim\operatorname{Exp}(\lambda)$（$\lambda>0$）。证明无记忆性 $P(X>s+t\mid X>s)=P(X>t)$（$s,t>0$），并说明其含义。

**过程**

$P(X>s+t\mid X>s)=\dfrac{P(X>s+t)}{P(X>s)}=\dfrac{e^{-\lambda(s+t)}}{e^{-\lambda s}}=e^{-\lambda t}=P(X>t)$。即条件后剩余寿命的分布与全新时完全相同。

**答案原文**

证毕；无记忆性成立且是指数分布的特征性质

## 191. eval-prob-014-s2

内容 SHA256：`957b1396ae2eda81e11d6f7e22c3419b3c120098c9db491dd2218ae0472f75e5`。

来源：data/v2/eval/dataset_eval.jsonl，第 191 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $X\sim\operatorname{Exp}(\lambda)$（$\lambda>0$）。证明无记忆性 $P(X>s+t\mid X>s)=P(X>t)$（$s,t>0$），并说明其含义。

**过程**

危险率函数 $h(t)=\dfrac{f(t)}{1-F(t)}=\dfrac{\lambda e^{-\lambda t}}{e^{-\lambda t}}=\lambda$ 为常数。常数危险率意味着"每时每刻的瞬时失效倾向不随年龄变化"，这正是无记忆性的微分刻画；反之，若某分布危险率为常数 $\lambda$，解微分方程 $\dfrac{F'}{1-F}=\lambda$ 得 $F(t)=1-e^{-\lambda t}$，故常数危险率⇔指数分布。

**答案原文**

证毕；无记忆性成立且是指数分布的特征性质

## 192. eval-prob-014-s3

内容 SHA256：`e88381ac8a81f690213e860c1718bd4486c0bb55f513446be8111ac1c44c5471`。

来源：data/v2/eval/dataset_eval.jsonl，第 192 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $X\sim\operatorname{Exp}(\lambda)$（$\lambda>0$）。证明无记忆性 $P(X>s+t\mid X>s)=P(X>t)$（$s,t>0$），并说明其含义。

**过程**

在强度 $\lambda$ 的泊松过程中，相邻事件的时间间隔服从 $\operatorname{Exp}(\lambda)$。已等待 $s$ 而无事件发生，意味着 $(0,s]$ 内的事件数 $N(s)=0$；由泊松过程的独立增量性，$(s,s+t]$ 内的事件数与 $(0,s]$ 内无关，$P(N(s,s+t)=0\mid N(s)=0)=P(N(s,s+t)=0)=e^{-\lambda t}$。故剩余等待时间仍服从 $\operatorname{Exp}(\lambda)$。

**答案原文**

证毕；无记忆性成立且是指数分布的特征性质

## 193. eval-prob-015-s1

内容 SHA256：`d59237bebe2bd1e953d2015eb632075a71b4becf1fa8008b4ddfcb5c77ac324e`。

来源：data/v2/eval/dataset_eval.jsonl，第 193 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

掷一枚均匀骰子，设 $X$ 为点数。求 $E[X]$ 与 $\operatorname{Var}(X)$。

**过程**

$E[X]=\dfrac{1+2+3+4+5+6}{6}=\dfrac{21}{6}=\dfrac{7}{2}$。$E[X^2]=\dfrac{1+4+9+16+25+36}{6}=\dfrac{91}{6}$。$\operatorname{Var}(X)=E[X^2]-(E[X])^2=\dfrac{91}{6}-\dfrac{49}{4}=\dfrac{182-147}{12}=\dfrac{35}{12}$。

**答案原文**

$E[X]=\dfrac{7}{2}$，$\operatorname{Var}(X)=\dfrac{35}{12}$

## 194. eval-prob-015-s2

内容 SHA256：`f35e2d8c42015d6f9948c320bc3e80e1bbdbc6f64627cae2a14fea356e25193c`。

来源：data/v2/eval/dataset_eval.jsonl，第 194 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

掷一枚均匀骰子，设 $X$ 为点数。求 $E[X]$ 与 $\operatorname{Var}(X)$。

**过程**

$M(t)=\dfrac{e^t+e^{2t}+e^{3t}+e^{4t}+e^{5t}+e^{6t}}{6}$。$M'(0)=\dfrac{1+2+3+4+5+6}{6}=\dfrac{7}{2}$，$M''(0)=\dfrac{1+4+9+16+25+36}{6}=\dfrac{91}{6}$。故 $E[X]=\dfrac{7}{2}$，$\operatorname{Var}(X)=M''(0)-[M'(0)]^2=\dfrac{35}{12}$。

**答案原文**

$E[X]=\dfrac{7}{2}$，$\operatorname{Var}(X)=\dfrac{35}{12}$

## 195. eval-prob-015-s3

内容 SHA256：`3f053e4c6543075f3b2e50bfa07e69fac6765886084af6c6bb1520e8899ef028`。

来源：data/v2/eval/dataset_eval.jsonl，第 195 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

掷一枚均匀骰子，设 $X$ 为点数。求 $E[X]$ 与 $\operatorname{Var}(X)$。

**过程**

令 $X=1+U$，其中 $U\sim U\{0,1,\dots,5\}$。离散均匀分布 $\{0,\dots,n-1\}$ 的方差公式：$\operatorname{Var}(U)=\dfrac{n^2-1}{12}=\dfrac{36-1}{12}=\dfrac{35}{12}$。故 $E[X]=1+\dfrac{5}{2}=\dfrac{7}{2}$，$\operatorname{Var}(X)=\operatorname{Var}(U)=\dfrac{35}{12}$。

**答案原文**

$E[X]=\dfrac{7}{2}$，$\operatorname{Var}(X)=\dfrac{35}{12}$

## 196. eval-linalg-001-s1

内容 SHA256：`a656b77f97224dd11dc2f577584fbabe6d90012682873961d9a67043f7e8b49a`。

来源：data/v2/eval/dataset_eval.jsonl，第 196 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

计算范德蒙德行列式 $\begin{vmatrix}1&1&1\\a&b&c\\a^2&b^2&c^2\end{vmatrix}$，并求 $a=1,b=2,c=3$ 时的值。

**过程**

第二行减第一行的 $a$ 倍、第三行减第一行的 $a^2$ 倍：$D=\begin{vmatrix}1&1&1\\0&b-a&c-a\\0&b^2-a^2&c^2-a^2\end{vmatrix}$。按第一列展开：$D=\begin{vmatrix}b-a&c-a\\b^2-a^2&c^2-a^2\end{vmatrix}=(b-a)(c-a)\begin{vmatrix}1&1\\b+a&c+a\end{vmatrix}=(b-a)(c-a)\left[(c+a)-(b+a)\right]=(b-a)(c-a)(c-b)$。代入 $a=1,b=2,c=3$：$D=(1)(2)(1)=2$。

**答案原文**

$(b-a)(c-a)(c-b)$；取值 $2$

## 197. eval-linalg-001-s2

内容 SHA256：`9aa56ea516eff380ffdb30a2ff5e8c51a6ccb57869b9cb691b2b1f6ee9f1b193`。

来源：data/v2/eval/dataset_eval.jsonl，第 197 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

计算范德蒙德行列式 $\begin{vmatrix}1&1&1\\a&b&c\\a^2&b^2&c^2\end{vmatrix}$，并求 $a=1,b=2,c=3$ 时的值。

**过程**

把 $D$ 看成关于 $c$ 的多项式 $f(c)$。按第三列展开，$c^2$ 的系数为 $\begin{vmatrix}1&1\\a&b\end{vmatrix}=b-a$，故 $f$ 至多是二次多项式。当 $c=a$ 或 $c=b$ 时，第三列与第一列（或第二列）相同，$f=0$，故 $f(c)=k(c-a)(c-b)$。取 $k=b-a$（最高次系数），得 $D=(b-a)(c-a)(c-b)$。（$a=b$ 时 $k=0$ 且 $D=0$，公式两端均为 0，仍成立。）

**答案原文**

$(b-a)(c-a)(c-b)$；取值 $2$

## 198. eval-linalg-001-s3

内容 SHA256：`fc0483bbc179fa5d3e0d8903bc9c41262fdb1e22d6f2e31be074211163823c18`。

来源：data/v2/eval/dataset_eval.jsonl，第 198 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

计算范德蒙德行列式 $\begin{vmatrix}1&1&1\\a&b&c\\a^2&b^2&c^2\end{vmatrix}$，并求 $a=1,b=2,c=3$ 时的值。

**过程**

$n$ 阶范德蒙德行列式 $D_n=\prod_{1\le i<j\le n}(x_j-x_i)$ 可用数学归纳法证明：自下而上做行变换 $R_k\leftarrow R_k-x_1R_{k-1}$（$k=n,n-1,\dots,2$），再按第一列展开、各列提取公因子 $x_j-x_1$，即降阶为 $n-1$ 阶范德蒙德行列式，归纳即得。$n=3$ 时即 $(b-a)(c-a)(c-b)$，代入得 $2$。

**答案原文**

$(b-a)(c-a)(c-b)$；取值 $2$

## 199. eval-linalg-002-s1

内容 SHA256：`a2e305e8c03cdd0157e694fbd85000dc9e0f5b9b58cacffce4b139b58ba90ccc`。

来源：data/v2/eval/dataset_eval.jsonl，第 199 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

计算四阶行列式 $D=\begin{vmatrix}1&1&1&1\\1&2&1&1\\1&1&3&1\\1&1&1&4\end{vmatrix}$。

**过程**

第二、三、四行分别减去第一行：$D=\begin{vmatrix}1&1&1&1\\0&1&0&0\\0&0&2&0\\0&0&0&3\end{vmatrix}$。上三角行列式等于对角线元素之积：$D=1\cdot 1\cdot 2\cdot 3=6$。

**答案原文**

$6$

## 200. eval-linalg-002-s2

内容 SHA256：`419c0aff12fdeb57194eed9166dde6fac9036d9cd81059eeef4a35e15bed4429`。

来源：data/v2/eval/dataset_eval.jsonl，第 200 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

计算四阶行列式 $D=\begin{vmatrix}1&1&1&1\\1&2&1&1\\1&1&3&1\\1&1&1&4\end{vmatrix}$。

**过程**

加边升阶：$D=\begin{vmatrix}1&1&1&1&1\\0&1&1&1&1\\0&1&2&1&1\\0&1&1&3&1\\0&1&1&1&4\end{vmatrix}$（按第一列展开即原行列式）。新行列式中，第三、四、五行分别减去第二行：$=\begin{vmatrix}1&1&1&1&1\\0&1&1&1&1\\0&0&1&0&0\\0&0&0&2&0\\0&0&0&0&3\end{vmatrix}=1\cdot 1\cdot 1\cdot 2\cdot 3=6$。

**答案原文**

$6$

## 201. eval-linalg-002-s3

内容 SHA256：`df227e282c243751f1cf48bfa776398513fa7634bfc72cb19bc55cd94a673713`。

来源：data/v2/eval/dataset_eval.jsonl，第 201 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

计算四阶行列式 $D=\begin{vmatrix}1&1&1&1\\1&2&1&1\\1&1&3&1\\1&1&1&4\end{vmatrix}$。

**过程**

每行减末行：$\begin{vmatrix}0&0&0&-3\\0&1&0&-3\\0&0&2&-3\\1&1&1&4\end{vmatrix}$，按第一列展开：$D=(-1)^{4+1}\cdot 1\cdot\begin{vmatrix}0&0&-3\\1&0&-3\\0&2&-3\end{vmatrix}=-\left[0-0+(-3)\begin{vmatrix}1&0\\0&2\end{vmatrix}\right]=-(-3\cdot 2)=6$。

**答案原文**

$6$

## 202. eval-linalg-003-s1

内容 SHA256：`829cd7e3d9acc23197b67bf425ebb6d2eda89516f2d48150ae4a74ce8feae985`。

来源：data/v2/eval/dataset_eval.jsonl，第 202 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求 $n$ 阶三对角行列式 $D_n=\begin{vmatrix}2&1&0&\cdots&0\\1&2&1&\cdots&0\\0&1&2&\cdots&0\\\vdots&&&\ddots&\vdots\\0&0&0&\cdots&2\end{vmatrix}$ 的值（矩阵元素满足 $a_{ii}=2$，$a_{i,i+1}=a_{i+1,i}=1$，其余为 0）。

**过程**

按第一行展开：$D_n=2D_{n-1}-1\cdot\begin{vmatrix}1&1&0&\cdots\\0&2&1&\cdots\\\vdots&&&\ddots\end{vmatrix}=2D_{n-1}-D_{n-2}$（第二项按第一列展开后恰为 $D_{n-2}$）。初始值 $D_1=2$，$D_2=\begin{vmatrix}2&1\\1&2\end{vmatrix}=3$。由递推 $D_n-D_{n-1}=D_{n-1}-D_{n-2}=\cdots=D_2-D_1=1$，故 $D_n=D_1+(n-1)=n+1$。

**答案原文**

$D_n=n+1$

## 203. eval-linalg-003-s2

内容 SHA256：`07fb8f65f13dee05c4637bab8cf8665ff74796ffea8624bec9dfb5e7108adf10`。

来源：data/v2/eval/dataset_eval.jsonl，第 203 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求 $n$ 阶三对角行列式 $D_n=\begin{vmatrix}2&1&0&\cdots&0\\1&2&1&\cdots&0\\0&1&2&\cdots&0\\\vdots&&&\ddots&\vdots\\0&0&0&\cdots&2\end{vmatrix}$ 的值（矩阵元素满足 $a_{ii}=2$，$a_{i,i+1}=a_{i+1,i}=1$，其余为 0）。

**过程**

该矩阵 $A=2I+B$，其中 $B$ 是 $n$ 阶路的邻接矩阵，其特征值为 $2\cos\dfrac{k\pi}{n+1}$（$k=1,\dots,n$）。故 $D_n=\det(2I+B)=\displaystyle\prod_{k=1}^{n}\left(2+2\cos\dfrac{k\pi}{n+1}\right)=2^n\prod_{k=1}^{n}\left(1+\cos\dfrac{k\pi}{n+1}\right)$。利用恒等式 $\displaystyle\prod_{k=1}^{n}\left(2+2\cos\dfrac{k\pi}{n+1}\right)=n+1$，证明如下：由 $x^{2n+2}-1=(x^2-1)\displaystyle\prod_{k=1}^{n}\left(x^2-2x\cos\dfrac{k\pi}{n+1}+1\right)$，两边同除 $x^2-1$ 得 $\dfrac{x^{2n+2}-1}{x^2-1}=\displaystyle\sum_{j=0}^{n}x^{2j}=\prod_{k=1}^{n}\left(x^2-2x\cos\dfrac{k\pi}{n+1}+1\right)$；令 $x\to-1$：左端 $\to n+1$，右端 $\to\displaystyle\prod_{k=1}^{n}\left(2+2\cos\dfrac{k\pi}{n+1}\right)$。得 $D_n=n+1$。

**答案原文**

$D_n=n+1$

## 204. eval-linalg-003-s3

内容 SHA256：`4bc10a191c821b16126162d51341a1dd990f754767c383dcf8ec08fb78b8a21b`。

来源：data/v2/eval/dataset_eval.jsonl，第 204 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求 $n$ 阶三对角行列式 $D_n=\begin{vmatrix}2&1&0&\cdots&0\\1&2&1&\cdots&0\\0&1&2&\cdots&0\\\vdots&&&\ddots&\vdots\\0&0&0&\cdots&2\end{vmatrix}$ 的值（矩阵元素满足 $a_{ii}=2$，$a_{i,i+1}=a_{i+1,i}=1$，其余为 0）。

**过程**

由解法一的递推式，归纳证明 $D_n=n+1$：$n=1,2$ 已验证；设 $D_{n-1}=n$、$D_{n-2}=n-1$，则 $D_n=2D_{n-1}-D_{n-2}=2n-(n-1)=n+1$。

**答案原文**

$D_n=n+1$

## 205. eval-linalg-004-s1

内容 SHA256：`94afd35569bc97bd8a78a8de018626d844839e96baf15b43a3982ed9ab985e5c`。

来源：data/v2/eval/dataset_eval.jsonl，第 205 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

计算 $n=3$ 时行列式 $D=\begin{vmatrix}a+b&a&a\\a&a+b&a\\a&a&a+b\end{vmatrix}$，并推广到 $n$ 阶。

**过程**

第二、三行分别减去第一行：$D=\begin{vmatrix}a+b&a&a\\-b&b&0\\-b&0&b\end{vmatrix}$。按第一行展开：$D=(a+b)\cdot b^2-a\cdot\begin{vmatrix}-b&0\\-b&b\end{vmatrix}+a\cdot\begin{vmatrix}-b&b\\-b&0\end{vmatrix}=(a+b)b^2-a(-b^2)+a(b^2)=b^2(a+b)+ab^2+ab^2=b^2(3a+b)$。

**答案原文**

$b^2(3a+b)$；$n$ 阶为 $b^{n-1}(na+b)$

## 206. eval-linalg-004-s2

内容 SHA256：`86199b50d43b1e1bc86c1a3dee848d19a863be5a65a4d9405b09da55bed4bdca`。

来源：data/v2/eval/dataset_eval.jsonl，第 206 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

计算 $n=3$ 时行列式 $D=\begin{vmatrix}a+b&a&a\\a&a+b&a\\a&a&a+b\end{vmatrix}$，并推广到 $n$ 阶。

**过程**

该矩阵 $A=bI+aJ$，其中 $J$ 为全 1 矩阵。$J$ 的特征值为 $n,0,\dots,0$（$J$ 的秩为 1，且 $J(1,\dots,1)^T=n(1,\dots,1)^T$），故 $A$ 的特征值为 $b+na$（一重）与 $b$（$n-1$ 重）。行列式=特征值之积：$D=(b+3a)\cdot b\cdot b=b^2(3a+b)$（$n=3$）；一般地 $D_n=b^{n-1}(na+b)$。

**答案原文**

$b^2(3a+b)$；$n$ 阶为 $b^{n-1}(na+b)$

## 207. eval-linalg-004-s3

内容 SHA256：`c9b3243bcca5eb7827c7043becf7e1ebf6675f0450091ba21e6468aff9429236`。

来源：data/v2/eval/dataset_eval.jsonl，第 207 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

计算 $n=3$ 时行列式 $D=\begin{vmatrix}a+b&a&a\\a&a+b&a\\a&a&a+b\end{vmatrix}$，并推广到 $n$ 阶。

**过程**

把每列拆成 $(a,a,a)^T+b\,e_i$（$e_i$ 为标准基向量）。由行列式关于列的多重线性：全取 $b\,e_i$ 的项为 $b^3\det I=b^3$；恰有一列取 $(a,a,a)^T$ 的项有 3 个，每个为 $ab^2\cdot\det(e_1,e_2,e_j$ 换为 $(1,1,1)^T)=ab^2$；有两列以上取 $(a,a,a)^T$ 的项行列式为 0（两列相同）。故 $D=b^3+3ab^2=b^2(3a+b)$。

**答案原文**

$b^2(3a+b)$；$n$ 阶为 $b^{n-1}(na+b)$

## 208. eval-linalg-005-s1

内容 SHA256：`976fb4945e735551014f8e06c442b4ed049238f136377c1de95eab49260d01a1`。

来源：data/v2/eval/dataset_eval.jsonl，第 208 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求矩阵 $A=\begin{pmatrix}3&2\\4&3\end{pmatrix}$ 的逆矩阵。

**过程**

$\det A=3\cdot 3-2\cdot 4=9-8=1$。$A^*=\begin{pmatrix}3&-2\\-4&3\end{pmatrix}$（代数余子式转置：$A_{11}=3$，$A_{12}=-4$，$A_{21}=-2$，$A_{22}=3$）。$A^{-1}=\dfrac{A^*}{\det A}=\begin{pmatrix}3&-2\\-4&3\end{pmatrix}$。验证：$AA^{-1}=\begin{pmatrix}9-8&-6+6\\12-12&-8+9\end{pmatrix}=I$。

**答案原文**

$A^{-1}=\begin{pmatrix}3&-2\\-4&3\end{pmatrix}$

## 209. eval-linalg-005-s2

内容 SHA256：`a4e9a32e56ee590b6c91de2f5b7c51c38417de17594548e1caad5b141bfcee1d`。

来源：data/v2/eval/dataset_eval.jsonl，第 209 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求矩阵 $A=\begin{pmatrix}3&2\\4&3\end{pmatrix}$ 的逆矩阵。

**过程**

对增广矩阵 $(A\mid I)$ 做行变换：$\begin{pmatrix}3&2&|&1&0\\4&3&|&0&1\end{pmatrix}\xrightarrow{R_2-\frac{4}{3}R_1}\begin{pmatrix}3&2&|&1&0\\0&\frac{1}{3}&|&-\frac{4}{3}&1\end{pmatrix}\xrightarrow{R_1-6R_2}\begin{pmatrix}3&0&|&9&-6\\0&\frac{1}{3}&|&-\frac{4}{3}&1\end{pmatrix}\xrightarrow{R_1/3,\ 3R_2}\begin{pmatrix}1&0&|&3&-2\\0&1&|&-4&3\end{pmatrix}$，故 $A^{-1}=\begin{pmatrix}3&-2\\-4&3\end{pmatrix}$。

**答案原文**

$A^{-1}=\begin{pmatrix}3&-2\\-4&3\end{pmatrix}$

## 210. eval-linalg-005-s3

内容 SHA256：`8116f4ef0959f7a18023e1d59285cce0c78b0b5c129d838f3f31d25e83ab761c`。

来源：data/v2/eval/dataset_eval.jsonl，第 210 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求矩阵 $A=\begin{pmatrix}3&2\\4&3\end{pmatrix}$ 的逆矩阵。

**过程**

设 $A^{-1}$ 的第 $j$ 列为 $x^{(j)}$，解 $Ax^{(1)}=e_1$、$Ax^{(2)}=e_2$。第一组：$\begin{cases}3x+2y=1\\4x+3y=0\end{cases}$，由第二式 $y=-\dfrac{4x}{3}$ 代入第一式：$3x-\dfrac{8x}{3}=1$，$x=3$，$y=-4$。第二组：$\begin{cases}3x+2y=0\\4x+3y=1\end{cases}$，得 $x=-2$，$y=3$。故 $A^{-1}=\begin{pmatrix}3&-2\\-4&3\end{pmatrix}$。

**答案原文**

$A^{-1}=\begin{pmatrix}3&-2\\-4&3\end{pmatrix}$

## 211. eval-linalg-006-s1

内容 SHA256：`7da42b044c1de4f5b9de66ec889701dd2a3ac282537a3645371762e837540e45`。

来源：data/v2/eval/dataset_eval.jsonl，第 211 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$，求 $A^n$（$n$ 为正整数）。

**过程**

$A^1=\begin{pmatrix}1&1\\0&1\end{pmatrix}$。设 $A^k=\begin{pmatrix}1&k\\0&1\end{pmatrix}$，则 $A^{k+1}=A^kA=\begin{pmatrix}1&k\\0&1\end{pmatrix}\begin{pmatrix}1&1\\0&1\end{pmatrix}=\begin{pmatrix}1&1+k\\0&1\end{pmatrix}$。归纳得 $A^n=\begin{pmatrix}1&n\\0&1\end{pmatrix}$。

**答案原文**

$A^n=\begin{pmatrix}1&n\\0&1\end{pmatrix}$

## 212. eval-linalg-006-s2

内容 SHA256：`096f0f9a7c31240d9fed7d7a804f3257976b899e05baa31ab406a7a5500c473b`。

来源：data/v2/eval/dataset_eval.jsonl，第 212 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$，求 $A^n$（$n$ 为正整数）。

**过程**

$A=I+N$，其中 $N=\begin{pmatrix}0&1\\0&0\end{pmatrix}$，且 $N^2=0$。$I$ 与 $N$ 可交换，由二项式定理：$A^n=(I+N)^n=I^n+\binom{n}{1}I^{n-1}N+\binom{n}{2}I^{n-2}N^2+\cdots=I+nN=\begin{pmatrix}1&n\\0&1\end{pmatrix}$（$N^2$ 起全为 0）。

**答案原文**

$A^n=\begin{pmatrix}1&n\\0&1\end{pmatrix}$

## 213. eval-linalg-006-s3

内容 SHA256：`7a4d69645cb3a88494845725474cfc7bc99704bf54dda404f8307c876f88dbed`。

来源：data/v2/eval/dataset_eval.jsonl，第 213 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$，求 $A^n$（$n$ 为正整数）。

**过程**

$A$ 的特征值为 $\lambda=1$（二重），$A-I=N\ne 0$ 而 $(A-I)^2=0$，故 $A$ 的若尔当标准形为 $J=\begin{pmatrix}1&1\\0&1\end{pmatrix}=A$ 本身。$J^n$ 的计算同解法二，得 $\begin{pmatrix}1&n\\0&1\end{pmatrix}$。

**答案原文**

$A^n=\begin{pmatrix}1&n\\0&1\end{pmatrix}$

## 214. eval-linalg-007-s1

内容 SHA256：`709957297d19a539ab220959fd7046e9930104c598090f3c3f6a59652e8d96c9`。

来源：data/v2/eval/dataset_eval.jsonl，第 214 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $A=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}$，求 $A^n$。

**过程**

$n=1$ 成立。设 $A^k=\begin{pmatrix}\cos k\theta&-\sin k\theta\\\sin k\theta&\cos k\theta\end{pmatrix}$，则 $A^{k+1}=A^kA$，其 $(1,1)$ 元为 $\cos k\theta\cos\theta-\sin k\theta\sin\theta=\cos(k+1)\theta$，$(1,2)$ 元为 $-\cos k\theta\sin\theta-\sin k\theta\cos\theta=-\sin(k+1)\theta$，其余两元同理。归纳成立。

**答案原文**

$A^n=\begin{pmatrix}\cos n\theta&-\sin n\theta\\\sin n\theta&\cos n\theta\end{pmatrix}$

## 215. eval-linalg-007-s2

内容 SHA256：`efbab70ef8e5451fa4b84b1677fcf2ee4ee0e0a7875c54f13143738684e7c260`。

来源：data/v2/eval/dataset_eval.jsonl，第 215 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $A=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}$，求 $A^n$。

**过程**

特征方程 $(\cos\theta-\lambda)^2+\sin^2\theta=0$，即 $\lambda^2-2\lambda\cos\theta+1=0$，特征值 $\lambda=e^{\pm i\theta}$，对应特征向量 $(1,\mp i)^T$。取 $P=\begin{pmatrix}1&1\\-i&i\end{pmatrix}$，$P^{-1}=\dfrac{1}{2}\begin{pmatrix}1&i\\1&-i\end{pmatrix}$，则 $A=P\begin{pmatrix}e^{i\theta}&0\\0&e^{-i\theta}\end{pmatrix}P^{-1}$。故 $A^n=P\begin{pmatrix}e^{in\theta}&0\\0&e^{-in\theta}\end{pmatrix}P^{-1}=\dfrac{1}{2}\begin{pmatrix}e^{in\theta}+e^{-in\theta}&i(e^{in\theta}-e^{-in\theta})\\-i(e^{in\theta}-e^{-in\theta})&e^{in\theta}+e^{-in\theta}\end{pmatrix}=\begin{pmatrix}\cos n\theta&-\sin n\theta\\\sin n\theta&\cos n\theta\end{pmatrix}$（用欧拉公式 $e^{\pm in\theta}=\cos n\theta\pm i\sin n\theta$ 化简）。

**答案原文**

$A^n=\begin{pmatrix}\cos n\theta&-\sin n\theta\\\sin n\theta&\cos n\theta\end{pmatrix}$

## 216. eval-linalg-007-s3

内容 SHA256：`7b791bcb38cccdcfe3e01948a2fa9a1a64b262202d185e07fc185a6fdef7ea8c`。

来源：data/v2/eval/dataset_eval.jsonl，第 216 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $A=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}$，求 $A^n$。

**过程**

旋转矩阵 $A$ 与复数乘法 $z\mapsto e^{i\theta}z$ 一一对应（$(x,y)\mapsto(x\cos\theta-y\sin\theta,\ x\sin\theta+y\cos\theta)$ 正是 $e^{i\theta}(x+iy)$ 的实虚部）。旋转的复合即角度相加：$(e^{i\theta})^n=e^{in\theta}$，对应 $A^n=$ 旋转 $n\theta$ 角的矩阵。

**答案原文**

$A^n=\begin{pmatrix}\cos n\theta&-\sin n\theta\\\sin n\theta&\cos n\theta\end{pmatrix}$

## 217. eval-linalg-008-s1

内容 SHA256：`00c67f11e1505aadb2b6d3644b60756984c659c2a052a6dea26d11728df18ca4`。

来源：data/v2/eval/dataset_eval.jsonl，第 217 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$，求 $\det A$、$A$ 的秩与 $A^{-1}$。

**过程**

$\det A=1\cdot 4-2\cdot 3=-2\ne 0$，故 $A$ 可逆、秩为 $2$。$A^*=\begin{pmatrix}4&-2\\-3&1\end{pmatrix}$，$A^{-1}=\dfrac{A^*}{\det A}=\dfrac{1}{-2}\begin{pmatrix}4&-2\\-3&1\end{pmatrix}=\begin{pmatrix}-2&1\\\frac{3}{2}&-\frac{1}{2}\end{pmatrix}$。

**答案原文**

$\det A=-2$；秩为 $2$；$A^{-1}=\begin{pmatrix}-2&1\\\frac{3}{2}&-\frac{1}{2}\end{pmatrix}$

## 218. eval-linalg-008-s2

内容 SHA256：`d761d4ec2df3b634884cf6fe0a62694b15f4172e72a0967a6fd3361159259463`。

来源：data/v2/eval/dataset_eval.jsonl，第 218 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$，求 $\det A$、$A$ 的秩与 $A^{-1}$。

**过程**

$(A\mid I)=\begin{pmatrix}1&2&|&1&0\\3&4&|&0&1\end{pmatrix}\xrightarrow{R_2-3R_1}\begin{pmatrix}1&2&|&1&0\\0&-2&|&-3&1\end{pmatrix}\xrightarrow{-\frac{1}{2}R_2}\begin{pmatrix}1&2&|&1&0\\0&1&|&\frac{3}{2}&-\frac{1}{2}\end{pmatrix}\xrightarrow{R_1-2R_2}\begin{pmatrix}1&0&|&-2&1\\0&1&|&\frac{3}{2}&-\frac{1}{2}\end{pmatrix}$。故 $A^{-1}=\begin{pmatrix}-2&1\\\frac{3}{2}&-\frac{1}{2}\end{pmatrix}$。

**答案原文**

$\det A=-2$；秩为 $2$；$A^{-1}=\begin{pmatrix}-2&1\\\frac{3}{2}&-\frac{1}{2}\end{pmatrix}$

## 219. eval-linalg-008-s3

内容 SHA256：`f25ee411f5e7b749064c934b09259009713887358fb3c4c4331f2e1d72183cfb`。

来源：data/v2/eval/dataset_eval.jsonl，第 219 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$，求 $\det A$、$A$ 的秩与 $A^{-1}$。

**过程**

$\det A=-2\ne 0$ 说明两行（列）线性无关，$\operatorname{rank}A=2$。验证逆矩阵：$AA^{-1}=\begin{pmatrix}1&2\\3&4\end{pmatrix}\begin{pmatrix}-2&1\\\frac{3}{2}&-\frac{1}{2}\end{pmatrix}=\begin{pmatrix}-2+3&1-1\\-6+6&3-2\end{pmatrix}=\begin{pmatrix}1&0\\0&1\end{pmatrix}$。

**答案原文**

$\det A=-2$；秩为 $2$；$A^{-1}=\begin{pmatrix}-2&1\\\frac{3}{2}&-\frac{1}{2}\end{pmatrix}$

## 220. eval-linalg-009-s1

内容 SHA256：`7aa6f5401d9837a08ad6e9b0bb4ee3a9b80338d93d6ef7d3ce9260a36da8b22c`。

来源：data/v2/eval/dataset_eval.jsonl，第 220 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

用分块方法计算 $M=\begin{pmatrix}2&1&1\\1&2&1\\0&0&3\end{pmatrix}$ 的行列式。

**过程**

取 $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$，$B=\begin{pmatrix}1\\1\end{pmatrix}$，$C=(3)$，则 $M=\begin{pmatrix}A&B\\0&C\end{pmatrix}$。分块上三角矩阵的行列式 $\det M=\det A\cdot\det C$。$\det A=2\cdot 2-1\cdot 1=3$，$\det C=3$，故 $\det M=3\cdot 3=9$。

**答案原文**

$9$

## 221. eval-linalg-009-s2

内容 SHA256：`9dcbe8210da94d7d9ee944baeaf5966c963bc5dac5e401dee8d87f42fd950c5e`。

来源：data/v2/eval/dataset_eval.jsonl，第 221 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

用分块方法计算 $M=\begin{pmatrix}2&1&1\\1&2&1\\0&0&3\end{pmatrix}$ 的行列式。

**过程**

按第三行展开：$\det M=(-1)^{3+3}\cdot 3\cdot\begin{vmatrix}2&1\\1&2\end{vmatrix}=3\cdot 3=9$（第三行仅第 3 个元素非零）。

**答案原文**

$9$

## 222. eval-linalg-009-s3

内容 SHA256：`066952840f6a3ff5872b2040fd22e657aa2d9695726f6c00ff5dd36a07242ecc`。

来源：data/v2/eval/dataset_eval.jsonl，第 222 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

用分块方法计算 $M=\begin{pmatrix}2&1&1\\1&2&1\\0&0&3\end{pmatrix}$ 的行列式。

**过程**

第三行与第一、二行的前两列零块使 $M$ 已是分块上三角。验证：直接用一般公式展开，$\det M=2\cdot\begin{vmatrix}2&1\\0&3\end{vmatrix}-1\cdot\begin{vmatrix}1&1\\0&3\end{vmatrix}+1\cdot\begin{vmatrix}1&2\\0&0\end{vmatrix}=2\cdot 6-1\cdot 3+1\cdot 0=12-3=9$，与分块公式一致。

**答案原文**

$9$

## 223. eval-linalg-010-s1

内容 SHA256：`4851049031bf460727dbd8f4e41f69dd9ebffc4bb3f335e09c0f721439f08b14`。

来源：data/v2/eval/dataset_eval.jsonl，第 223 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求矩阵 $A=\begin{pmatrix}1&1&2\\2&1&3\\1&2&3\end{pmatrix}$ 的秩。

**过程**

$\begin{pmatrix}1&1&2\\2&1&3\\1&2&3\end{pmatrix}\xrightarrow{R_2-2R_1}\begin{pmatrix}1&1&2\\0&-1&-1\\1&2&3\end{pmatrix}\xrightarrow{R_3-R_1}\begin{pmatrix}1&1&2\\0&-1&-1\\0&1&1\end{pmatrix}\xrightarrow{R_3+R_2}\begin{pmatrix}1&1&2\\0&-1&-1\\0&0&0\end{pmatrix}$。非零行数为 2，故 $\operatorname{rank}A=2$。

**答案原文**

$2$

## 224. eval-linalg-010-s2

内容 SHA256：`608fa1b6a1ae7e8c892dec155480c780f8c79780289aea17124e11b061b01629`。

来源：data/v2/eval/dataset_eval.jsonl，第 224 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求矩阵 $A=\begin{pmatrix}1&1&2\\2&1&3\\1&2&3\end{pmatrix}$ 的秩。

**过程**

$\det A=1\cdot(1\cdot 3-3\cdot 2)-1\cdot(2\cdot 3-3\cdot 1)+2\cdot(2\cdot 2-1\cdot 1)=1\cdot(-3)-1\cdot 3+2\cdot 3=0$，秩小于 3。二阶子式 $\begin{vmatrix}1&1\\2&1\end{vmatrix}=1-2=-1\ne 0$，故秩为 2。

**答案原文**

$2$

## 225. eval-linalg-010-s3

内容 SHA256：`faa7a4d40c20b2c22eb810516484564fd9cecef846f188699346606865da62a7`。

来源：data/v2/eval/dataset_eval.jsonl，第 225 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求矩阵 $A=\begin{pmatrix}1&1&2\\2&1&3\\1&2&3\end{pmatrix}$ 的秩。

**过程**

三列 $c_1=(1,2,1)^T$、$c_2=(1,1,2)^T$、$c_3=(2,3,3)^T$ 满足 $c_3=c_1+c_2$（逐分量验证：$1+1=2$，$2+1=3$，$1+2=3$），故 $c_3$ 可由前两列线性表出；$c_1,c_2$ 不成比例，线性无关。列秩 $=2$，即 $\operatorname{rank}A=2$。

**答案原文**

$2$

## 226. eval-linalg-011-s1

内容 SHA256：`dde192611c33e50c43ed6f0860d9112869400ed5188776d88e8023997c5a6029`。

来源：data/v2/eval/dataset_eval.jsonl，第 226 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

讨论含参数线性方程组 $\begin{cases}\lambda x+y+z=1\\x+\lambda y+z=\lambda\\x+y+\lambda z=\lambda^2\end{cases}$ 的解的情况。

**过程**

系数行列式 $D=\begin{vmatrix}\lambda&1&1\\1&\lambda&1\\1&1&\lambda\end{vmatrix}$。该矩阵 $=(\lambda-1)I+J$（$J$ 全 1 矩阵），特征值为 $(\lambda-1)+3=\lambda+2$ 与 $\lambda-1$（二重），故 $D=(\lambda+2)(\lambda-1)^2$。当 $\lambda\ne 1,-2$ 时 $D\ne 0$，由 Cramer 法则有唯一解。当 $\lambda=1$：三个方程均为 $x+y+z=1$，无穷多解（解空间二维）。当 $\lambda=-2$：三式相加得 $0\cdot(x+y+z)=1+(-2)+4=3$，即 $0=3$，矛盾，无解。

**答案原文**

$\lambda\ne 1$ 且 $\lambda\ne-2$ 时唯一解；$\lambda=1$ 时无穷多解；$\lambda=-2$ 时无解

## 227. eval-linalg-011-s2

内容 SHA256：`42cbe53f661f68ed0121fd265d1a4538fb65059a96879d4b5d61dfaeb08d529a`。

来源：data/v2/eval/dataset_eval.jsonl，第 227 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

讨论含参数线性方程组 $\begin{cases}\lambda x+y+z=1\\x+\lambda y+z=\lambda\\x+y+\lambda z=\lambda^2\end{cases}$ 的解的情况。

**过程**

增广矩阵 $\begin{pmatrix}\lambda&1&1&1\\1&\lambda&1&\lambda\\1&1&\lambda&\lambda^2\end{pmatrix}$。交换第一、三行后消元：$\begin{pmatrix}1&1&\lambda&\lambda^2\\0&\lambda-1&1-\lambda&\lambda-\lambda^2\\0&1-\lambda&1-\lambda^2&1-\lambda^3\end{pmatrix}$。当 $\lambda\ne 1$：第二行除以 $\lambda-1$ 得 $\begin{pmatrix}1&1&\lambda&\lambda^2\\0&1&-1&-\lambda\\0&1-\lambda&1-\lambda^2&1-\lambda^3\end{pmatrix}$，第三行减第二行的 $(1-\lambda)$ 倍，其首项系数为 $(1-\lambda^2)+(1-\lambda)=2-\lambda-\lambda^2=(\lambda+2)(1-\lambda)\cdot\ldots$，最终当 $\lambda=-2$ 时出现 $0=3$ 型矛盾行（无解），其余 $\lambda\ne 1$ 时有唯一解；$\lambda=1$ 时三行相同，无穷多解。

**答案原文**

$\lambda\ne 1$ 且 $\lambda\ne-2$ 时唯一解；$\lambda=1$ 时无穷多解；$\lambda=-2$ 时无解

## 228. eval-linalg-011-s3

内容 SHA256：`116399e7f45e821fe162eff262a502a93e05c9d9b31c464409ebde3a8898971b`。

来源：data/v2/eval/dataset_eval.jsonl，第 228 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

讨论含参数线性方程组 $\begin{cases}\lambda x+y+z=1\\x+\lambda y+z=\lambda\\x+y+\lambda z=\lambda^2\end{cases}$ 的解的情况。

**过程**

三个方程代表三个平面。$\lambda=1$ 时三平面重合（$x+y+z=1$）；$\lambda=-2$ 时三平面两两相交但三交线平行（法向量和为零向量导致矛盾）；其余情形三平面交于一点（唯一解）。

**答案原文**

$\lambda\ne 1$ 且 $\lambda\ne-2$ 时唯一解；$\lambda=1$ 时无穷多解；$\lambda=-2$ 时无解

## 229. eval-linalg-012-s1

内容 SHA256：`1a6634561b4b4adfb6b78a2e52604d24c9182ac1b7d0fc083b7c8aaab60cbc56`。

来源：data/v2/eval/dataset_eval.jsonl，第 229 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求参数 $a$ 使齐次线性方程组 $\begin{cases}ax+y+z=0\\x+ay+z=0\\x+y+az=0\end{cases}$ 有非零解，并求各情形下的解空间。

**过程**

系数行列式 $D=\begin{vmatrix}a&1&1\\1&a&1\\1&1&a\end{vmatrix}$。矩阵 $=(a-1)I+J$，特征值 $a+2$ 与 $a-1$（二重），故 $D=(a+2)(a-1)^2$。齐次方程组有非零解 $\iff D=0\iff a=1$ 或 $a=-2$。$a=1$：三个方程均为 $x+y+z=0$，解空间为二维平面。$a=-2$：三式相加得 $-2(x+y+z)+2(x+y+z)=0$ 恒等，且 $\begin{cases}-2x+y+z=0\\x-2y+z=0\end{cases}$ 相减得 $x=y$，代回得 $z=x$，解空间为直线 $x=y=z$（一维）。

**答案原文**

$a=1$（解空间二维：$x+y+z=0$）或 $a=-2$（解空间一维：$x=y=z$）

## 230. eval-linalg-012-s2

内容 SHA256：`fc07fb59bfc2d65961101c79e00717081ec7360b87329f67ca515e08452eb042`。

来源：data/v2/eval/dataset_eval.jsonl，第 230 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求参数 $a$ 使齐次线性方程组 $\begin{cases}ax+y+z=0\\x+ay+z=0\\x+y+az=0\end{cases}$ 有非零解，并求各情形下的解空间。

**过程**

$a\ne 1,-2$ 时 $D\ne 0$，秩为 3，只有零解。$a=1$ 时矩阵为全 1 矩阵，秩 1，解空间维数 $3-1=2$。$a=-2$ 时矩阵 $\begin{pmatrix}-2&1&1\\1&-2&1\\1&1&-2\end{pmatrix}$，行变换：第二行减第一行的 $-\dfrac{1}{2}$ 倍……等价地观察任意两行相减得 $\pm 3(x-y)=0$ 型关系，秩为 2，解空间维数 $3-2=1$。

**答案原文**

$a=1$（解空间二维：$x+y+z=0$）或 $a=-2$（解空间一维：$x=y=z$）

## 231. eval-linalg-012-s3

内容 SHA256：`da994973cc326d07ed4050b24bc958e7183b331e2a24a7456f1c4de49d25842d`。

来源：data/v2/eval/dataset_eval.jsonl，第 231 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求参数 $a$ 使齐次线性方程组 $\begin{cases}ax+y+z=0\\x+ay+z=0\\x+y+az=0\end{cases}$ 有非零解，并求各情形下的解空间。

**过程**

方程组 $((a-1)I+J)v=0$ 有非零解 $\iff -(a-1)$ 是 $J$ 的特征值。$J$ 的特征值为 $3,0,0$，故 $a-1\in\{-3,0\}$，即 $a=-2$ 或 $a=1$，与解法一一致。$a=-2$ 时解为 $J$ 的特征值 $3$ 对应的特征向量方向 $(1,1,1)^T$；$a=1$ 时解为 $J$ 的零空间（$x+y+z=0$，二维）。

**答案原文**

$a=1$（解空间二维：$x+y+z=0$）或 $a=-2$（解空间一维：$x=y=z$）

## 232. eval-linalg-013-s1

内容 SHA256：`c86cd391785c66a65a81d75f14dc1bf5d4aff1264baaa1a51cd98dd18b413fe1`。

来源：data/v2/eval/dataset_eval.jsonl，第 232 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求齐次线性方程组 $x_1+x_2+x_3+x_4=0$ 的基础解系与通解。

**过程**

取 $x_2,x_3,x_4$ 为自由变量，$x_1=-x_2-x_3-x_4$。分别令 $(x_2,x_3,x_4)=(1,0,0),(0,1,0),(0,0,1)$，得基础解系 $\xi_1=(-1,1,0,0)^T$，$\xi_2=(-1,0,1,0)^T$，$\xi_3=(-1,0,0,1)^T$（取负号即 $\xi_1=(1,-1,0,0)^T$ 等形式，两者等价）。通解 $x=c_1\xi_1+c_2\xi_2+c_3\xi_3$。

**答案原文**

基础解系 $\xi_1=(1,-1,0,0)^T$，$\xi_2=(1,0,-1,0)^T$，$\xi_3=(1,0,0,-1)^T$；通解 $x=c_1\xi_1+c_2\xi_2+c_3\xi_3$

## 233. eval-linalg-013-s2

内容 SHA256：`8950c9ac0364f4283a56ae40d5930efe1e2f637fd16c57d264f7543030676971`。

来源：data/v2/eval/dataset_eval.jsonl，第 233 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求齐次线性方程组 $x_1+x_2+x_3+x_4=0$ 的基础解系与通解。

**过程**

解空间 $=(\operatorname{span}\{(1,1,1,1)^T\})^\perp$（法向量 $(1,1,1,1)$ 的正交补）。取三个线性无关且与 $(1,1,1,1)$ 正交的向量：$(1,-1,0,0)^T$、$(1,0,-1,0)^T$、$(1,0,0,-1)^T$（逐一点积为 0）。三者线性无关（前三个分量的子矩阵 $\begin{pmatrix}1&-1&0\\1&0&-1\\1&0&0\end{pmatrix}$ 行列式 $1\ne 0$），故构成基础解系。

**答案原文**

基础解系 $\xi_1=(1,-1,0,0)^T$，$\xi_2=(1,0,-1,0)^T$，$\xi_3=(1,0,0,-1)^T$；通解 $x=c_1\xi_1+c_2\xi_2+c_3\xi_3$

## 234. eval-linalg-013-s3

内容 SHA256：`3a330441d2b6ea8fa7393cf599fc441ae6dbabfe2dc5876a4049060e9ed16f62`。

来源：data/v2/eval/dataset_eval.jsonl，第 234 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求齐次线性方程组 $x_1+x_2+x_3+x_4=0$ 的基础解系与通解。

**过程**

方程 $x_1+x_2+x_3+x_4=0$ 是 $\mathbb R^4$ 中过原点的三维超平面（法向量 $(1,1,1,1)$）。基础解系即该超平面的一个基，通解是超平面上所有点。维数 $4-1=3$ 与基础解系含 3 个向量一致。

**答案原文**

基础解系 $\xi_1=(1,-1,0,0)^T$，$\xi_2=(1,0,-1,0)^T$，$\xi_3=(1,0,0,-1)^T$；通解 $x=c_1\xi_1+c_2\xi_2+c_3\xi_3$

## 235. eval-linalg-014-s1

内容 SHA256：`d764660b2b33713f10b7d6bb521c958f664f243f0e8df3e2c0ac8c11518cc9d1`。

来源：data/v2/eval/dataset_eval.jsonl，第 235 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $a\in\mathbb R\setminus\{0\}$ 为参数,求矩阵 $A=\begin{pmatrix}1&a&0\\a&1&a\\0&a&1\end{pmatrix}$ 的特征值与特征向量,并求正交矩阵 $Q$,使 $Q^TAQ$ 为对角矩阵。

**过程**

$|\lambda I-A|=\begin{vmatrix}\lambda-1&-a&0\\-a&\lambda-1&-a\\0&-a&\lambda-1\end{vmatrix}=(\lambda-1)\bigl[(\lambda-1)^2-2a^2\bigr]$,得特征值 $1,\ 1\pm\sqrt{2}a$($a\neq 0$ 时互异)。$\lambda=1$:解 $(A-I)v=0$,即 $\begin{pmatrix}0&a&0\\a&0&a\\0&a&0\end{pmatrix}v=0$,得 $y=0,\ x=-z$,取 $v_1=(1,0,-1)^T$。$\lambda=1+\sqrt{2}a$:由 $(A-(1+\sqrt{2}a)I)v=0$,第一行给 $y=\sqrt{2}x$,第二行给 $x-\sqrt{2}y+z=0$,故 $z=x$,取 $v_2=(1,\sqrt{2},1)^T$。$\lambda=1-\sqrt{2}a$:同理 $y=-\sqrt{2}x,\ z=x$,取 $v_3=(1,-\sqrt{2},1)^T$。三个特征向量两两正交,范数分别为 $\sqrt{2},\ 2,\ 2$;单位化后按列排成 $Q=\begin{pmatrix}1/\sqrt{2}&1/2&1/2\\0&\sqrt{2}/2&-\sqrt{2}/2\\-1/\sqrt{2}&1/2&1/2\end{pmatrix}$。直接验证:$AQ=Q\operatorname{diag}(1,1+\sqrt{2}a,1-\sqrt{2}a)$(逐列即 $Av_i=\lambda_i v_i$),故 $Q^TAQ=\operatorname{diag}(1,\,1+\sqrt{2}a,\,1-\sqrt{2}a)$。

**答案原文**

特征值 $1,\ 1+\sqrt{2}a,\ 1-\sqrt{2}a$;对应单位特征向量 $\dfrac{1}{\sqrt{2}}(1,0,-1)^T,\ \dfrac{1}{2}(1,\sqrt{2},1)^T,\ \dfrac{1}{2}(1,-\sqrt{2},1)^T$;$Q=\begin{pmatrix}1/\sqrt{2}&1/2&1/2\\0&\sqrt{2}/2&-\sqrt{2}/2\\-1/\sqrt{2}&1/2&1/2\end{pmatrix}$,$Q^TAQ=\operatorname{diag}(1,\,1+\sqrt{2}a,\,1-\sqrt{2}a)$

## 236. eval-linalg-014-s2

内容 SHA256：`547e117cb3dae10ff8159188ca765eeef5f7fc32cd3849493a8a9300c676221b`。

来源：data/v2/eval/dataset_eval.jsonl，第 236 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $a\in\mathbb R\setminus\{0\}$ 为参数,求矩阵 $A=\begin{pmatrix}1&a&0\\a&1&a\\0&a&1\end{pmatrix}$ 的特征值与特征向量,并求正交矩阵 $Q$,使 $Q^TAQ$ 为对角矩阵。

**过程**

先看反对称方向:$A(1,0,-1)^T=(1,0,-1)^T$,故 $v_1=(1,0,-1)^T$ 是特征值 1 的特征向量。其余特征向量在 $v_1$ 的正交补 $\operatorname{span}\{r,s\}$ 内,其中 $r=\dfrac{1}{\sqrt{2}}(1,0,1)^T,\ s=(0,1,0)^T$ 为单位正交基。计算 $A$ 在 $(r,s)$ 上的限制:$Ar=\dfrac{1}{\sqrt{2}}A(1,0,1)^T=\dfrac{1}{\sqrt{2}}(1,2a,1)^T=r+\sqrt{2}a\,s$;$As=A(0,1,0)^T=(a,1,a)^T=\sqrt{2}a\,r+s$。故限制矩阵为 $\begin{pmatrix}1&\sqrt{2}a\\\sqrt{2}a&1\end{pmatrix}$,其特征值为 $1\pm\sqrt{2}a$,对应特征向量 $r\pm s$,即 $v_2=\dfrac{1}{2}(1,\sqrt{2},1)^T$,$v_3=\dfrac{1}{2}(1,-\sqrt{2},1)^T$。三向量两两正交,单位化后按列排成 $Q=\begin{pmatrix}1/\sqrt{2}&1/2&1/2\\0&\sqrt{2}/2&-\sqrt{2}/2\\-1/\sqrt{2}&1/2&1/2\end{pmatrix}$,$Q^TAQ=\operatorname{diag}(1,\,1+\sqrt{2}a,\,1-\sqrt{2}a)$。

**答案原文**

特征值 $1,\ 1+\sqrt{2}a,\ 1-\sqrt{2}a$;对应单位特征向量 $\dfrac{1}{\sqrt{2}}(1,0,-1)^T,\ \dfrac{1}{2}(1,\sqrt{2},1)^T,\ \dfrac{1}{2}(1,-\sqrt{2},1)^T$;$Q=\begin{pmatrix}1/\sqrt{2}&1/2&1/2\\0&\sqrt{2}/2&-\sqrt{2}/2\\-1/\sqrt{2}&1/2&1/2\end{pmatrix}$,$Q^TAQ=\operatorname{diag}(1,\,1+\sqrt{2}a,\,1-\sqrt{2}a)$

## 237. eval-linalg-014-s3

内容 SHA256：`b27dae0e6dcf4b48df9e3dc1fe02cea97c23dfacd391cc9d09809cf43f932853`。

来源：data/v2/eval/dataset_eval.jsonl，第 237 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $a\in\mathbb R\setminus\{0\}$ 为参数,求矩阵 $A=\begin{pmatrix}1&a&0\\a&1&a\\0&a&1\end{pmatrix}$ 的特征值与特征向量,并求正交矩阵 $Q$,使 $Q^TAQ$ 为对角矩阵。

**过程**

二次型 $f(x,y,z)=x^2+y^2+z^2+2a(xy+yz)$。令 $u=\dfrac{x-z}{\sqrt{2}},\ p=\dfrac{x+z}{\sqrt{2}}$,则 $x^2+z^2=u^2+p^2$,$xy+yz=y(x+z)=\sqrt{2}py$,故 $f=u^2+p^2+y^2+2\sqrt{2}a\,py$。再令 $v=\dfrac{p+y}{\sqrt{2}},\ w=\dfrac{p-y}{\sqrt{2}}$,则 $p^2+y^2=v^2+w^2$,$2py=v^2-w^2$,故 $f=u^2+(1+\sqrt{2}a)v^2+(1-\sqrt{2}a)w^2$——三项系数即特征值。由 $(u,v,w)^T=P(x,y,z)^T$ 解出 $P=\begin{pmatrix}1/\sqrt{2}&0&-1/\sqrt{2}\\1/2&\sqrt{2}/2&1/2\\1/2&-\sqrt{2}/2&1/2\end{pmatrix}$,$Q=P^T$ 即为所求正交矩阵。参数分类($f=1$ 等值面):$|a|<\dfrac{\sqrt{2}}{2}$ 时三系数全正,为椭球面;$a=\pm\dfrac{\sqrt{2}}{2}$ 时一个系数为 0,退化为椭圆柱面;$|a|>\dfrac{\sqrt{2}}{2}$ 时一个系数为负,为单叶双曲面。

**答案原文**

特征值 $1,\ 1+\sqrt{2}a,\ 1-\sqrt{2}a$;对应单位特征向量 $\dfrac{1}{\sqrt{2}}(1,0,-1)^T,\ \dfrac{1}{2}(1,\sqrt{2},1)^T,\ \dfrac{1}{2}(1,-\sqrt{2},1)^T$;$Q=\begin{pmatrix}1/\sqrt{2}&1/2&1/2\\0&\sqrt{2}/2&-\sqrt{2}/2\\-1/\sqrt{2}&1/2&1/2\end{pmatrix}$,$Q^TAQ=\operatorname{diag}(1,\,1+\sqrt{2}a,\,1-\sqrt{2}a)$

## 238. eval-linalg-015-s1

内容 SHA256：`ea3aa32859a7f0d7fb54c0f40578c381b62ad3ec78b75b91e79722134a557485`。

来源：data/v2/eval/dataset_eval.jsonl，第 238 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求矩阵 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$ 的特征值与特征向量，并将其对角化。

**过程**

$|\lambda I-A|=\begin{vmatrix}\lambda-1&-2\\-2&\lambda-1\end{vmatrix}=(\lambda-1)^2-4=\lambda^2-2\lambda-3=(\lambda-3)(\lambda+1)$，$\lambda=3,-1$。$\lambda=3$：$(3I-A)v=0$，即 $\begin{pmatrix}2&-2\\-2&2\end{pmatrix}v=0$，$v=(1,1)^T$。$\lambda=-1$：$(-I-A)v=0$，即 $\begin{pmatrix}-2&-2\\-2&-2\end{pmatrix}v=0$，$v=(1,-1)^T$。

**答案原文**

特征值 $\lambda_1=3$、$\lambda_2=-1$；特征向量 $(1,1)^T$、$(1,-1)^T$；$P^{-1}AP=\begin{pmatrix}3&0\\0&-1\end{pmatrix}$，其中 $P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$

## 239. eval-linalg-015-s2

内容 SHA256：`0e4c69e79bd6ef6bf20f840decd0891f96e9825c240cca300cbfaba072caaadb`。

来源：data/v2/eval/dataset_eval.jsonl，第 239 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求矩阵 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$ 的特征值与特征向量，并将其对角化。

**过程**

$A$ 对应二次型 $x^2+4xy+y^2$。配方得 $(x+y)^2+2xy\ldots$ 沿 $y=x$ 方向（$u=\dfrac{x+y}{\sqrt2}$）：值为 $3u^2$；沿 $y=-x$ 方向（$v=\dfrac{x-y}{\sqrt2}$）：值为 $-v^2$。故主轴方向 $(1,1)$ 与 $(1,-1)$ 上二次型取值 $3u^2-v^2$，特征值为 $3,-1$。

**答案原文**

特征值 $\lambda_1=3$、$\lambda_2=-1$；特征向量 $(1,1)^T$、$(1,-1)^T$；$P^{-1}AP=\begin{pmatrix}3&0\\0&-1\end{pmatrix}$，其中 $P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$

## 240. eval-linalg-015-s3

内容 SHA256：`52f5abe9929b7602ea722a90c53344163934079753879638e2365e3423345a18`。

来源：data/v2/eval/dataset_eval.jsonl，第 240 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求矩阵 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$ 的特征值与特征向量，并将其对角化。

**过程**

归一化特征向量 $q_1=\dfrac{1}{\sqrt2}(1,1)^T$、$q_2=\dfrac{1}{\sqrt2}(1,-1)^T$（自动正交），取 $Q=\dfrac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$（$Q$ 为正交矩阵，$Q^{-1}=Q^T$）。$Q^TAQ=\begin{pmatrix}3&0\\0&-1\end{pmatrix}$，验证：$Q^TAQ=\dfrac{1}{2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}\begin{pmatrix}1&2\\2&1\end{pmatrix}\begin{pmatrix}1&1\\1&-1\end{pmatrix}=\dfrac{1}{2}\begin{pmatrix}3&3\\-1&1\end{pmatrix}\begin{pmatrix}1&1\\1&-1\end{pmatrix}=\dfrac{1}{2}\begin{pmatrix}6&0\\0&-2\end{pmatrix}$。

**答案原文**

特征值 $\lambda_1=3$、$\lambda_2=-1$；特征向量 $(1,1)^T$、$(1,-1)^T$；$P^{-1}AP=\begin{pmatrix}3&0\\0&-1\end{pmatrix}$，其中 $P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$

## 241. eval-linalg-016-s1

内容 SHA256：`83365a54487166eb0c09ebfe1d558b22db3afe02fa0dc99912b75e12d5b5f75b`。

来源：data/v2/eval/dataset_eval.jsonl，第 241 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $A$ 为二阶方阵，已知 $\operatorname{tr}A=5$、$\det A=6$。求 $A$ 的特征值，并验证 $A^2-5A+6I=0$。

**过程**

特征多项式 $|\lambda I-A|=\lambda^2-(\operatorname{tr}A)\lambda+\det A=\lambda^2-5\lambda+6=(\lambda-2)(\lambda-3)$，特征值为 $2,3$。

**答案原文**

特征值为 $2$ 与 $3$；$A^2-5A+6I=0$ 成立

## 242. eval-linalg-016-s2

内容 SHA256：`08e7515544b25824830db2c364ce5e1e80b8d35ff78dd7717d6b4bf4fe920719`。

来源：data/v2/eval/dataset_eval.jsonl，第 242 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $A$ 为二阶方阵，已知 $\operatorname{tr}A=5$、$\det A=6$。求 $A$ 的特征值，并验证 $A^2-5A+6I=0$。

**过程**

由特征多项式 $p(\lambda)=\lambda^2-5\lambda+6$，Cayley–Hamilton 定理给出 $p(A)=A^2-5A+6I=0$。验证特例 $A=\begin{pmatrix}2&1\\0&3\end{pmatrix}$（$\operatorname{tr}=5$、$\det=6$）：$A^2=\begin{pmatrix}4&5\\0&9\end{pmatrix}$，$A^2-5A+6I=\begin{pmatrix}4-10+6&5-5\\0&9-15+6\end{pmatrix}=0$。

**答案原文**

特征值为 $2$ 与 $3$；$A^2-5A+6I=0$ 成立

## 243. eval-linalg-016-s3

内容 SHA256：`a5ba55a3913a655ccfbbdc460823a91526337e375a7a922f9f53d8a8f3909417`。

来源：data/v2/eval/dataset_eval.jsonl，第 243 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $A$ 为二阶方阵，已知 $\operatorname{tr}A=5$、$\det A=6$。求 $A$ 的特征值，并验证 $A^2-5A+6I=0$。

**过程**

迹与行列式是相似不变量，特征值由迹与行列式唯一确定为 $2,3$。由两个不同特征值知 $A$ 可对角化（最小多项式 $(\lambda-2)(\lambda-3)$ 无重根），即 $A=P\operatorname{diag}(2,3)P^{-1}$。于是 $A^2-5A+6I=P\left(\operatorname{diag}(4,9)-5\operatorname{diag}(2,3)+6I\right)P^{-1}=P\cdot 0\cdot P^{-1}=0$，与解法二一致。

**答案原文**

特征值为 $2$ 与 $3$；$A^2-5A+6I=0$ 成立

## 244. eval-linalg-017-s1

内容 SHA256：`6211bcb4b078078b5862cec2dc5e99f7c9986fd3523645d70c9e036cf2cda9bc`。

来源：data/v2/eval/dataset_eval.jsonl，第 244 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求矩阵 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 的特征值与特征向量，并判断其是否可对角化。

**过程**

$|\lambda I-A|=(\lambda-1)^2=0$，$\lambda=1$（二重）。解 $(I-A)v=0$：$I-A=\begin{pmatrix}0&-1\\0&0\end{pmatrix}$，$\begin{pmatrix}0&-1\\0&0\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix}=0$ 得 $y=0$，特征空间 $\operatorname{span}\{(1,0)^T\}$ 仅一维（非零特征向量为 $t(1,0)^T$，$t\ne 0$）。特征空间维数 $1<$ 代数重数 $2$，故不可对角化。

**答案原文**

特征值 $\lambda=1$（二重），非零特征向量 $t(1,0)^T$（$t\ne 0$，特征空间连同零向量为一维）；不可对角化，若尔当标准形为 $\begin{pmatrix}1&1\\0&1\end{pmatrix}$

## 245. eval-linalg-017-s2

内容 SHA256：`b4862520830f8dc0fa13343a74d1220327616e0b1ce5c7c0e7dab8e0681b70dc`。

来源：data/v2/eval/dataset_eval.jsonl，第 245 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求矩阵 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 的特征值与特征向量，并判断其是否可对角化。

**过程**

$A$ 是水平剪切变换：$(x,y)\mapsto(x+y,y)$。所有向量的 $y$ 分量不变，仅 $(t,0)^T$（水平方向）方向不变，其余向量方向都被"推斜"。剪切没有第二个不变方向，故只有一个特征方向，不可对角化。

**答案原文**

特征值 $\lambda=1$（二重），非零特征向量 $t(1,0)^T$（$t\ne 0$，特征空间连同零向量为一维）；不可对角化，若尔当标准形为 $\begin{pmatrix}1&1\\0&1\end{pmatrix}$

## 246. eval-linalg-017-s3

内容 SHA256：`06509b3215bf25d89b4695d4d8e29a0dc3196388a5a27d33ccdc9c9b68481a73`。

来源：data/v2/eval/dataset_eval.jsonl，第 246 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求矩阵 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 的特征值与特征向量，并判断其是否可对角化。

**过程**

$A-I=\begin{pmatrix}0&1\\0&0\end{pmatrix}\ne 0$，$(A-I)^2=0$，故最小多项式为 $m(\lambda)=(\lambda-1)^2$，含有重因子 $(\lambda-1)^2$。矩阵可对角化 $\iff$ 最小多项式无重根，故 $A$ 不可对角化；其若尔当标准形为单个二阶块 $J_2(1)=\begin{pmatrix}1&1\\0&1\end{pmatrix}$。

**答案原文**

特征值 $\lambda=1$（二重），非零特征向量 $t(1,0)^T$（$t\ne 0$，特征空间连同零向量为一维）；不可对角化，若尔当标准形为 $\begin{pmatrix}1&1\\0&1\end{pmatrix}$

## 247. eval-linalg-018-s1

内容 SHA256：`000716513a8dd2cad74ffdf561f7ffa4258c21d1bb809f466ecfc4673a643ba4`。

来源：data/v2/eval/dataset_eval.jsonl，第 247 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$，求 $A^{100}$。

**过程**

特征方程 $(\lambda-2)^2-1=0$，特征值 $3,1$；对应特征向量 $(1,1)^T$、$(1,-1)^T$。取 $P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$（即 eval-linalg-015 的结论），则 $P^{-1}AP=\begin{pmatrix}3&0\\0&1\end{pmatrix}$，且 $P^{-1}=\dfrac{1}{2}P$（因 $P^2=2I$）。故 $A^{100}=P\begin{pmatrix}3^{100}&0\\0&1\end{pmatrix}P^{-1}=\dfrac{1}{2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}\begin{pmatrix}3^{100}&0\\0&1\end{pmatrix}\begin{pmatrix}1&1\\1&-1\end{pmatrix}=\dfrac{1}{2}\begin{pmatrix}3^{100}&1\\3^{100}&-1\end{pmatrix}\begin{pmatrix}1&1\\1&-1\end{pmatrix}=\dfrac{1}{2}\begin{pmatrix}3^{100}+1&3^{100}-1\\3^{100}-1&3^{100}+1\end{pmatrix}$。

**答案原文**

$A^{100}=\dfrac{1}{2}\begin{pmatrix}3^{100}+1&3^{100}-1\\3^{100}-1&3^{100}+1\end{pmatrix}$

## 248. eval-linalg-018-s2

内容 SHA256：`3b62d9abc70480cd95a22888153f3515271fe861fa7018ba2f74993d229eb70d`。

来源：data/v2/eval/dataset_eval.jsonl，第 248 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$，求 $A^{100}$。

**过程**

$A=I+B$，其中 $B=\begin{pmatrix}1&1\\1&1\end{pmatrix}$，且 $B^2=2B$（验证：$B^2=\begin{pmatrix}2&2\\2&2\end{pmatrix}=2B$）。于是 $B^k=2^{k-1}B$（$k\ge 1$）。$A^{100}=(I+B)^{100}=I+\displaystyle\sum_{k=1}^{100}\binom{100}{k}2^{k-1}B=I+\dfrac{3^{100}-1}{2}B$（其中 $\displaystyle\sum_{k=1}^{100}\binom{100}{k}2^{k}=3^{100}-1$，除以 $2$ 即得）。代入 $B$：$A^{100}=\begin{pmatrix}1+\frac{3^{100}-1}{2}&\frac{3^{100}-1}{2}\\\frac{3^{100}-1}{2}&1+\frac{3^{100}-1}{2}\end{pmatrix}=\dfrac{1}{2}\begin{pmatrix}3^{100}+1&3^{100}-1\\3^{100}-1&3^{100}+1\end{pmatrix}$。

**答案原文**

$A^{100}=\dfrac{1}{2}\begin{pmatrix}3^{100}+1&3^{100}-1\\3^{100}-1&3^{100}+1\end{pmatrix}$

## 249. eval-linalg-018-s3

内容 SHA256：`81728709e63137dce0d4f5a4ef6188826b4ef2f67197bb584f66405ced1c7248`。

来源：data/v2/eval/dataset_eval.jsonl，第 249 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$，求 $A^{100}$。

**过程**

特征多项式 $\lambda^2-4\lambda+3$，由 C–H 定理 $A^2=4A-3I$。设 $A^n=u_nA+v_nI$，则 $A^{n+1}=A^nA=(u_nA+v_nI)A=u_nA^2+v_nA=u_n(4A-3I)+v_nA=(4u_n+v_n)A-3u_nI$，故 $u_{n+1}=4u_n+v_n$、$v_{n+1}=-3u_n$，初值 $u_1=1$、$v_1=0$。由 $v_n=-3u_{n-1}$（$n\ge 2$）代入第一式得 $u_{n+1}=4u_n-3u_{n-1}$，即 $u_{n+1}-u_n=3(u_n-u_{n-1})$；又 $u_2-u_1=3$，故 $u_n-u_{n-1}=3^{n-1}$，$u_n=1+\displaystyle\sum_{k=2}^{n}3^{k-1}=1+3\cdot\dfrac{3^{n-1}-1}{2}=\dfrac{3^n-1}{2}$，$v_n=-3u_{n-1}=-\dfrac{3^n-3}{2}$。$A^{100}=\dfrac{3^{100}-1}{2}A-\dfrac{3^{100}-3}{2}I=\dfrac{1}{2}\begin{pmatrix}3^{100}+1&3^{100}-1\\3^{100}-1&3^{100}+1\end{pmatrix}$。

**答案原文**

$A^{100}=\dfrac{1}{2}\begin{pmatrix}3^{100}+1&3^{100}-1\\3^{100}-1&3^{100}+1\end{pmatrix}$

## 250. eval-linalg-019-s1

内容 SHA256：`822f84925d2f0f7fdf2d0f3fe8db422affdbb53443e6d63319dacf2970d9bc1b`。

来源：data/v2/eval/dataset_eval.jsonl，第 250 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $a\in\mathbb R$ 为参数,将二次型 $f(x,y,z)=x^2+2y^2+az^2+2xy+2xz$ 化为标准形,并讨论 $a$ 取何值时 $f$ 正定。

**过程**

先按含 $x$ 的项配方:$(x+y+z)^2=x^2+y^2+z^2+2xy+2xz+2yz$,故 $f=(x+y+z)^2+(y^2-2yz+(a-1)z^2)$。再对 $y$ 配方:$(y-z)^2=y^2-2yz+z^2$,得 $f=(x+y+z)^2+(y-z)^2+(a-2)z^2$。若 $a>2$,三项系数全正,且 $(x+y+z,y-z,z)=(0,0,0)$ 推出 $x=y=z=0$,故 $f>0$($(x,y,z)\neq(0,0,0)$)。若 $a\le 2$,取 $x+y+z=0,\ y=z$ 的非零解(如 $(x,y,z)=(-2,1,1)$),此时前两项为 0、第三项 $\le 0$,$f$ 不正定。

**答案原文**

$f=(x+y+z)^2+(y-z)^2+(a-2)z^2$;$f$ 正定当且仅当 $a>2$

## 251. eval-linalg-019-s2

内容 SHA256：`653ef1423c620a9f12ab8040af3cc5d70078745ae807f7bf5b299d36944e89b4`。

来源：data/v2/eval/dataset_eval.jsonl，第 251 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $a\in\mathbb R$ 为参数,将二次型 $f(x,y,z)=x^2+2y^2+az^2+2xy+2xz$ 化为标准形,并讨论 $a$ 取何值时 $f$ 正定。

**过程**

$f$ 的矩阵 $A=\begin{pmatrix}1&1&1\\1&2&0\\1&0&a\end{pmatrix}$。作合同变换(行列同步):第一步,第二、三行分别减去第一行,第二、三列分别减去第一列,得 $\begin{pmatrix}1&0&0\\0&1&-1\\0&-1&a-1\end{pmatrix}$;第二步,第三行加上第二行、第三列加上第二列,得 $\operatorname{diag}(1,1,a-2)$。两步对应的列变换矩阵累计为 $C=\begin{pmatrix}1&-1&-2\\0&1&1\\0&0&1\end{pmatrix}$,满足 $C^TAC=\operatorname{diag}(1,1,a-2)$。对应新变量 $u=x+y+z,\ v=y-z,\ w=z$(即 $(x,y,z)^T=C(u,v,w)^T$),标准形为 $u^2+v^2+(a-2)w^2$。合同保持正定性,故 $f$ 正定 $\iff$ 对角元全正 $\iff a>2$。

**答案原文**

$f=(x+y+z)^2+(y-z)^2+(a-2)z^2$;$f$ 正定当且仅当 $a>2$

## 252. eval-linalg-019-s3

内容 SHA256：`8c22fdd95943d2b859bb3e59a69ae0c416602098ce8416fd327b661926d97ce8`。

来源：data/v2/eval/dataset_eval.jsonl，第 252 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $a\in\mathbb R$ 为参数,将二次型 $f(x,y,z)=x^2+2y^2+az^2+2xy+2xz$ 化为标准形,并讨论 $a$ 取何值时 $f$ 正定。

**过程**

$f$ 的矩阵 $A$ 可作 $LDL^T$ 分解: $$A=L\operatorname{diag}(1,1,a-2)L^T,\qquad L=\begin{pmatrix}1&0&0\\1&1&0\\1&-1&1\end{pmatrix}.$$ (直接乘开验证:行列为 $1,2,0$ 与 $1,0,a$ 的交叉项分别由 $L$ 的第 2、3 行生成。)令 $(u,v,w)^T=L^T(x,y,z)^T$,得新变量 $u=x+y+z,\ v=y-z,\ w=z$,于是 $$f=(x,y,z)A(x,y,z)^T=(L^T(x,y,z)^T)^T\operatorname{diag}(1,1,a-2)(L^T(x,y,z)^T)=u^2+v^2+(a-2)w^2,$$ 即标准形为 $u^2+v^2+(a-2)w^2$。再由顺序主子式($\Delta_1=1,\Delta_2=1,\Delta_3=|A|=a-2$),$f$ 正定 $\iff\Delta_3>0\iff a>2$——本条解法独立完成"化标准形+判正定"两问。边界 $a=2$ 时标准形第三项系数为 0,$f=u^2+v^2$ 半正定,零空间为 $u=v=0$,即 $x+y+z=0,\ y=z$,也就是 $t(-2,1,1)$。

**答案原文**

$f=(x+y+z)^2+(y-z)^2+(a-2)z^2$;$f$ 正定当且仅当 $a>2$

## 253. eval-linalg-020-s1

内容 SHA256：`71fc158f7984d98f8dec537e4a2f215d4db799527ca118dcbef4088bb3ceb107`。

来源：data/v2/eval/dataset_eval.jsonl，第 253 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

判断二次型 $f(x,y)=x^2-4xy+4y^2$ 的类型（正定/半正定/不定/负定）。

**过程**

$f=x^2-4xy+4y^2=(x-2y)^2\ge 0$ 对一切 $(x,y)$ 成立，且 $x=2y$（如 $(2,1)$）时取到 0，故半正定。标准形为 $u^2$（$u=x-2y$），秩为 1。

**答案原文**

半正定，秩为 1，正惯性指数 1、负惯性指数 0

## 254. eval-linalg-020-s2

内容 SHA256：`80e574fe12e2dc3392cd284e1247dd1587b08a7d0068272cb8e5376286533de7`。

来源：data/v2/eval/dataset_eval.jsonl，第 254 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

判断二次型 $f(x,y)=x^2-4xy+4y^2$ 的类型（正定/半正定/不定/负定）。

**过程**

矩阵 $A=\begin{pmatrix}1&-2\\-2&4\end{pmatrix}$。特征方程 $\lambda^2-5\lambda=0$，特征值 $\lambda_1=5$、$\lambda_2=0$。特征值非负且含 0，故半正定，秩 $=$ 非零特征值个数 $=1$。

**答案原文**

半正定，秩为 1，正惯性指数 1、负惯性指数 0

## 255. eval-linalg-020-s3

内容 SHA256：`e2d9d4c7284f22481658fa8128f0088f5bff7f2a081efd9e0e0eacee029fb021`。

来源：data/v2/eval/dataset_eval.jsonl，第 255 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

判断二次型 $f(x,y)=x^2-4xy+4y^2$ 的类型（正定/半正定/不定/负定）。

**过程**

$f=0\iff x=2y$，即一条过原点的直线；$f>0$ 对其余所有点成立。等值线族 $f=k$（$k>0$）是平行直线对 $x-2y=\pm\sqrt{k}$（两条直线）。这对应"退化椭圆"的极限情形，故半正定秩 1。

**答案原文**

半正定，秩为 1，正惯性指数 1、负惯性指数 0

## 256. eval-linalg-021-s1

内容 SHA256：`c296d801d26529c049e5dd5c2b8b8d022885e5a4d92ac76d455521708a9b70c3`。

来源：data/v2/eval/dataset_eval.jsonl，第 256 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $a\in\mathbb R$ 为参数,求使二次型 $f(x,y,z)=2x^2+y^2+2z^2+2xy+2axz$ 正定的 $a$ 的取值范围。

**过程**

$f$ 的矩阵 $A=\begin{pmatrix}2&1&a\\1&1&0\\a&0&2\end{pmatrix}$。顺序主子式:$\Delta_1=2>0$,$\Delta_2=\begin{vmatrix}2&1\\1&1\end{vmatrix}=1>0$,$\Delta_3=|A|=2\cdot\begin{vmatrix}1&0\\0&2\end{vmatrix}-1\cdot\begin{vmatrix}1&0\\a&2\end{vmatrix}+a\cdot\begin{vmatrix}1&1\\a&0\end{vmatrix}=4-2-a^2=2-a^2$。$f$ 正定 $\iff\Delta_3>0\iff 2-a^2>0\iff -\sqrt{2}<a<\sqrt{2}$。

**答案原文**

$-\sqrt{2}<a<\sqrt{2}$

## 257. eval-linalg-021-s2

内容 SHA256：`d2249bdffe09f69d0483532a1f87ddb1b87934b8f4ac6b182fda32fe162eac5b`。

来源：data/v2/eval/dataset_eval.jsonl，第 257 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $a\in\mathbb R$ 为参数,求使二次型 $f(x,y,z)=2x^2+y^2+2z^2+2xy+2axz$ 正定的 $a$ 的取值范围。

**过程**

$2\left(x+\dfrac{y}{2}+\dfrac{az}{2}\right)^2=2x^2+\dfrac{y^2}{2}+\dfrac{a^2z^2}{2}+2xy+2axz+ayz$,故 $$f=2\left(x+\frac{y}{2}+\frac{az}{2}\right)^2+\left[\frac{y^2}{2}-ayz+\left(2-\frac{a^2}{2}\right)z^2\right]=2\left(x+\frac{y}{2}+\frac{az}{2}\right)^2+\frac{1}{2}(y-az)^2+(2-a^2)z^2.$$ 三项系数 $2,\ \dfrac{1}{2},\ 2-a^2$ 全正 $\iff 2-a^2>0\iff |a|<\sqrt{2}$,与解法一一致。

**答案原文**

$-\sqrt{2}<a<\sqrt{2}$

## 258. eval-linalg-021-s3

内容 SHA256：`87d50dc0d5af3f9848b3c5914738981798a604086896ae9e7bc718fffb067eb9`。

来源：data/v2/eval/dataset_eval.jsonl，第 258 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $a\in\mathbb R$ 为参数,求使二次型 $f(x,y,z)=2x^2+y^2+2z^2+2xy+2axz$ 正定的 $a$ 的取值范围。

**过程**

把 $A$ 分块为 $\begin{pmatrix}B&c\\c^T&2\end{pmatrix}$,其中 $B=\begin{pmatrix}2&1\\1&1\end{pmatrix}$,$c=(a,0)^T$。$B$ 正定($2>0$ 且 $|B|=1>0$),由 Schur 补判据,$A$ 正定 $\iff$ $B$ 正定且 $S=2-c^TB^{-1}c>0$。$B^{-1}=\begin{pmatrix}1&-1\\-1&2\end{pmatrix}$,$c^TB^{-1}c=(a,0)\begin{pmatrix}1&-1\\-1&2\end{pmatrix}\begin{pmatrix}a\\0\end{pmatrix}=a^2$,故 $S=2-a^2$。于是 $f$ 正定 $\iff 2-a^2>0\iff -\sqrt{2}<a<\sqrt{2}$,与前两法独立得到同一范围。

**答案原文**

$-\sqrt{2}<a<\sqrt{2}$

## 259. eval-linalg-022-s1

内容 SHA256：`cdaf9514ab497fad6c631c4652e679e1ce06522a1dae5608f0cbc50b2e5763f7`。

来源：data/v2/eval/dataset_eval.jsonl，第 259 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

将多项式 $f(x)=x^4+2x^3-7x^2-8x+12$ 因式分解。

**过程**

常数项 $12$ 与首项系数 $1$，可能的有理根为 $\pm1,\pm2,\pm3,\pm4,\pm6,\pm12$。逐一代入：$f(1)=1+2-7-8+12=0$；$f(2)=16+16-28-16+12=0$；$f(-2)=16-16-28+16+12=0$；$f(-3)=81-54-63+24+12=0$。四次多项式有四个根 $1,2,-2,-3$，故 $f=(x-1)(x-2)(x+2)(x+3)$。

**答案原文**

$(x-1)(x-2)(x+2)(x+3)$

## 260. eval-linalg-022-s2

内容 SHA256：`0b4e7f77a6967a793c2c66db990475a759b2812d437e627100b3ca0cdd0cb34f`。

来源：data/v2/eval/dataset_eval.jsonl，第 260 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

将多项式 $f(x)=x^4+2x^3-7x^2-8x+12$ 因式分解。

**过程**

设 $f=(x^2+ax+b)(x^2+cx+d)$，展开比对：$a+c=2$，$b+d+ac=-7$，$ad+bc=-8$，$bd=12$。试 $b=-2$、$d=-6$（$bd=12$）：则 $b+d=-8$，$ac=-7+8=1$；结合 $a+c=2$、$ac=1$ 得 $a=c=1$。检验 $ad+bc=1\cdot(-6)+1\cdot(-2)=-8$，全部吻合。故 $f=(x^2+x-2)(x^2+x-6)=(x-1)(x+2)(x-2)(x+3)$。

**答案原文**

$(x-1)(x-2)(x+2)(x+3)$

## 261. eval-linalg-022-s3

内容 SHA256：`e9513c6e5023fb9fc0f053f8daebff5f01398ee72b204e3505c85166718fa94b`。

来源：data/v2/eval/dataset_eval.jsonl，第 261 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

将多项式 $f(x)=x^4+2x^3-7x^2-8x+12$ 因式分解。

**过程**

由 $f(1)=0$，用综合除法除以 $x-1$：系数 $1,2,-7,-8,12$ 依次得商系数 $1,3,-4,-12$（即 $x^3+3x^2-4x-12$），余 0。检验 $g(2)=8+12-8-12=0$，再除以 $x-2$ 得 $x^2+5x+6$。最后 $x^2+5x+6=(x+2)(x+3)$。故 $f=(x-1)(x-2)(x+2)(x+3)$。

**答案原文**

$(x-1)(x-2)(x+2)(x+3)$

## 262. eval-linalg-023-s1

内容 SHA256：`491fef6141c8bf728b8f14e0f556d1357c44abaef301f68d8eef4f6f7ff3dd56`。

来源：data/v2/eval/dataset_eval.jsonl，第 262 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

分别在复数域与实数域上分解 $x^8-1$。

**过程**

$x^8-1=0$ 的根是 8 次单位根 $e^{2\pi ik/8}$（$k=0,1,\dots,7$），在复平面上构成正八边形的顶点。复数域上 $x^8-1=\displaystyle\prod_{k=0}^{7}\left(x-e^{2\pi ik/8}\right)$。实数域上把共轭根配对：$k=0,4$ 对应实根 $\pm 1$；$k=1,7$ 配对得 $\left(x-e^{i\pi/4}\right)\left(x-e^{-i\pi/4}\right)=x^2-2x\cos\dfrac{\pi}{4}+1=x^2-\sqrt2x+1$；$k=2,6$ 配对得 $x^2+1$；$k=3,5$ 配对得 $x^2+\sqrt2x+1$。故实数域分解为 $(x-1)(x+1)(x^2-\sqrt2x+1)(x^2+1)(x^2+\sqrt2x+1)$。

**答案原文**

复数域：$\displaystyle\prod_{k=0}^{7}\left(x-e^{2\pi ik/8}\right)$；实数域（完整实不可约分解）：$(x-1)(x+1)(x^2+1)(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)$

## 263. eval-linalg-023-s2

内容 SHA256：`63594d58430ee4b6139d911422ed9317fb2eabdcd132ba304f3bf996d194c79d`。

来源：data/v2/eval/dataset_eval.jsonl，第 263 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

分别在复数域与实数域上分解 $x^8-1$。

**过程**

$x^8-1=(x^4-1)(x^4+1)=(x^2-1)(x^2+1)(x^4+1)=(x-1)(x+1)(x^2+1)(x^4+1)$。再对 $x^4+1$ 作实分解（见解法三的恒等式）：$x^4+1=(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)$，合并得完整实不可约分解 $(x-1)(x+1)(x^2+1)(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)$。

**答案原文**

复数域：$\displaystyle\prod_{k=0}^{7}\left(x-e^{2\pi ik/8}\right)$；实数域（完整实不可约分解）：$(x-1)(x+1)(x^2+1)(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)$

## 264. eval-linalg-023-s3

内容 SHA256：`fcd4c55ca45110a49502aca83bb3f1c03805c4ea146fe8b36c0472a0f922cb82`。

来源：data/v2/eval/dataset_eval.jsonl，第 264 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

分别在复数域与实数域上分解 $x^8-1$。

**过程**

本题复数域分解为 $\displaystyle\prod_{k=0}^{7}\left(x-e^{2\pi ik/8}\right)$（8 次单位根）。实数域分解有两种书写形式。形式一（按共轭根配对，完整实不可约分解）：$x^8-1=(x-1)(x+1)(x^2-\sqrt2x+1)(x^2+1)(x^2+\sqrt2x+1)$。形式二（按平方差递推，尚未完全分解）：$x^8-1=(x-1)(x+1)(x^2+1)(x^4+1)$。两形式由恒等式 $(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)=x^4+1$ 连接，其证明是平方差：$(x^2+1)^2-(\sqrt2x)^2=x^4+2x^2+1-2x^2=x^4+1$。故形式二是形式一的合并书写，形式一才是完整实不可约分解。

**答案原文**

复数域：$\displaystyle\prod_{k=0}^{7}\left(x-e^{2\pi ik/8}\right)$；实数域（完整实不可约分解）：$(x-1)(x+1)(x^2+1)(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)$

## 265. eval-linalg-024-s1

内容 SHA256：`1563a83b0e69eb4778e23a077baafa1a45979010642f209366bd075eae36bc1c`。

来源：data/v2/eval/dataset_eval.jsonl，第 265 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

将多项式 $f(x)=x^3-7x+6$ 按 $x-1$ 的幂展开（即求 $f$ 在 $x=1$ 处的泰勒展开）。

**过程**

$f(1)=1-7+6=0$；$f'(x)=3x^2-7$，$f'(1)=-4$；$f''(x)=6x$，$f''(1)=6$；$f'''(x)=6$，$f'''(1)=6$。由泰勒公式 $f(x)=f(1)+f'(1)(x-1)+\dfrac{f''(1)}{2}(x-1)^2+\dfrac{f'''(1)}{6}(x-1)^3=0-4(x-1)+3(x-1)^2+(x-1)^3$。

**答案原文**

$f(x)=(x-1)^3+3(x-1)^2-4(x-1)$

## 266. eval-linalg-024-s2

内容 SHA256：`3b060c1aec021820addb8846b04c73d4d48c07ae056171fef791c41923aef2e2`。

来源：data/v2/eval/dataset_eval.jsonl，第 266 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

将多项式 $f(x)=x^3-7x+6$ 按 $x-1$ 的幂展开（即求 $f$ 在 $x=1$ 处的泰勒展开）。

**过程**

对系数 $1,0,-7,6$ 反复除以 $x-1$。第一次：商系数 $1,1,-6$，余 $0$；第二次：商 $1,2$，余 $-4$；第三次：商 $1$，余 $3$。由 $f=(x-1)q_1+r_1$，$q_1=(x-1)q_2+r_2$，$q_2=(x-1)q_3+r_3$，得 $f=(x-1)[(x-1)[(x-1)\cdot 1+3]-4]=(x-1)^3+3(x-1)^2-4(x-1)$。

**答案原文**

$f(x)=(x-1)^3+3(x-1)^2-4(x-1)$

## 267. eval-linalg-024-s3

内容 SHA256：`0608fdc1c322b18722c52029d6d988e5a8d43a4cb39071333332015acf7a6f1a`。

来源：data/v2/eval/dataset_eval.jsonl，第 267 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

将多项式 $f(x)=x^3-7x+6$ 按 $x-1$ 的幂展开（即求 $f$ 在 $x=1$ 处的泰勒展开）。

**过程**

令 $y=x-1$，则 $x=y+1$。$f=(y+1)^3-7(y+1)+6=y^3+3y^2+3y+1-7y-7+6=y^3+3y^2-4y$。代回 $y=x-1$ 得 $f=(x-1)^3+3(x-1)^2-4(x-1)$。

**答案原文**

$f(x)=(x-1)^3+3(x-1)^2-4(x-1)$

## 268. eval-linalg-025-s1

内容 SHA256：`e099f705335b48dd73b61b931413508f0ed85aa686c6a830528db576c38b4580`。

来源：data/v2/eval/dataset_eval.jsonl，第 268 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $f(x)=x^5+x+1$。求 $f(x)$ 除以 $x-1$ 的余式，以及除以 $x^2+1$ 的余式。

**过程**

除以 $x-1$ 的余式为 $f(1)=1+1+1=3$。除以二次式 $x^2+1$ 设余式为 $ax+b$，由 $x^2+1$ 的根 $x=i$（虚数单位）：$f(i)=i^5+i+1$，而 $i^4=1$ 故 $i^5=i$，得 $f(i)=2i+1$。余式在 $x=i$ 处的值 $ai+b$ 应等于 $f(i)$：$ai+b=2i+1$，故 $a=2$、$b=1$，余式为 $2x+1$。

**答案原文**

除以 $x-1$ 余 $3$；除以 $x^2+1$ 余 $2x+1$

## 269. eval-linalg-025-s2

内容 SHA256：`23f8e83673689a7bdca27411e74b6847ca04686e57fb8a9f6d5ea85bfe83972f`。

来源：data/v2/eval/dataset_eval.jsonl，第 269 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $f(x)=x^5+x+1$。求 $f(x)$ 除以 $x-1$ 的余式，以及除以 $x^2+1$ 的余式。

**过程**

除以 $x^2+1$：$x^5+x+1$ 中，$x^5$ 与 $x$ 各含 $x^2+1$ 的分解：$x^5=x^3(x^2+1)-x^3$，$x^3=x(x^2+1)-x$，故 $x^5+x+1=x^3(x^2+1)-x(x^2+1)+x+x+1=(x^2+1)(x^3-x)+(2x+1)$，余式 $2x+1$。除以 $x-1$：$x^5+x+1=(x-1)q+3$ 由余数定理直接得余 $3$（商 $q=x^4+x^3+x^2+x+2$，验证 $f(1)=3$）。

**答案原文**

除以 $x-1$ 余 $3$；除以 $x^2+1$ 余 $2x+1$

## 270. eval-linalg-025-s3

内容 SHA256：`51b2fbac5287d0e690cef8688b8664d8c661e727822e3bc23e79e7a5e16ba963`。

来源：data/v2/eval/dataset_eval.jsonl，第 270 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $f(x)=x^5+x+1$。求 $f(x)$ 除以 $x-1$ 的余式，以及除以 $x^2+1$ 的余式。

**过程**

设除以 $x^2+1$ 的余式为 $ax+b$，则 $f(x)=(x^2+1)q(x)+ax+b$。取 $x=i$ 与 $x=-i$：$f(i)=1+2i$（同解法一），$f(-i)=(-i)^5-i+1=-i-i+1=1-2i$。解 $\begin{cases}ai+b=1+2i\\-ai+b=1-2i\end{cases}$，相加得 $2b=2$、$b=1$；相减得 $2ai=4i$、$a=2$。余式 $2x+1$。

**答案原文**

除以 $x-1$ 余 $3$；除以 $x^2+1$ 余 $2x+1$

## 271. eval-linalg-026-s1

内容 SHA256：`84e3d01c69289c9d60e9572682d0bcc5465f229c660ad46c395e85b102b2ac0d`。

来源：data/v2/eval/dataset_eval.jsonl，第 271 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

判断向量组 $\alpha_1=(1,2,3)$，$\alpha_2=(2,3,1)$，$\alpha_3=(3,1,2)$ 是否线性相关。

**过程**

以三向量为行（或列）的行列式 $D=\begin{vmatrix}1&2&3\\2&3&1\\3&1&2\end{vmatrix}=1\cdot(3\cdot 2-1\cdot 1)-2\cdot(2\cdot 2-1\cdot 3)+3\cdot(2\cdot 1-3\cdot 3)=1\cdot 5-2\cdot 1+3\cdot(-7)=5-2-21=-18\ne 0$。行列式非零，故三向量线性无关。

**答案原文**

线性无关

## 272. eval-linalg-026-s2

内容 SHA256：`c84a0a28fb32950db98a9e04b8e0cc864f8b0ea728fb116a2a9a4c3e1a107afa`。

来源：data/v2/eval/dataset_eval.jsonl，第 272 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

判断向量组 $\alpha_1=(1,2,3)$，$\alpha_2=(2,3,1)$，$\alpha_3=(3,1,2)$ 是否线性相关。

**过程**

设 $k_1\alpha_1+k_2\alpha_2+k_3\alpha_3=0$，即 $\begin{cases}k_1+2k_2+3k_3=0\\2k_1+3k_2+k_3=0\\3k_1+k_2+2k_3=0\end{cases}$。由第一式 $k_1=-2k_2-3k_3$，代入第二式：$2(-2k_2-3k_3)+3k_2+k_3=0$，即 $-k_2-5k_3=0$，$k_2=-5k_3$；代入第三式：$3(-2k_2-3k_3)+k_2+2k_3=0$，即 $-5k_2-7k_3=0$，代入 $k_2=-5k_3$ 得 $25k_3-7k_3=18k_3=0$，$k_3=0$，进而 $k_2=0$、$k_1=0$。只有零解，线性无关。

**答案原文**

线性无关

## 273. eval-linalg-026-s3

内容 SHA256：`fcd26b674a6bbb414ce2b4a72c0e0fe9a8a1b9d61466e7dfe750654194e9399b`。

来源：data/v2/eval/dataset_eval.jsonl，第 273 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

判断向量组 $\alpha_1=(1,2,3)$，$\alpha_2=(2,3,1)$，$\alpha_3=(3,1,2)$ 是否线性相关。

**过程**

三向量张成的平行六面体体积 $|D|=18\ne 0$，即三向量不共面，故线性无关（线性相关⇔体积为 0）。

**答案原文**

线性无关

## 274. eval-linalg-027-s1

内容 SHA256：`4a67b035b08b0fa719ed8c24b82cbb7062c369b63808636e218edcaec3c268be`。

来源：data/v2/eval/dataset_eval.jsonl，第 274 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求 $\mathbb R^3$ 中子空间 $W=\operatorname{span}\{(1,1,0),(0,1,1)\}$ 的正交补 $W^\perp$。

**过程**

$W^\perp=\{(x,y,z):(x,y,z)\cdot(1,1,0)=0,\ (x,y,z)\cdot(0,1,1)=0\}$，即 $\begin{cases}x+y=0\\y+z=0\end{cases}$。由第二式 $z=-y$，第一式 $x=-y$，故 $(x,y,z)=(-y,y,-y)=y(-1,1,-1)$，取 $(1,-1,1)$ 为基，$W^\perp$ 为一维。

**答案原文**

$W^\perp=\operatorname{span}\{(1,-1,1)\}$（一维）

## 275. eval-linalg-027-s2

内容 SHA256：`32b3778505f08673c38c9162286015db147baed54e8d87b87df229afa90031d2`。

来源：data/v2/eval/dataset_eval.jsonl，第 275 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求 $\mathbb R^3$ 中子空间 $W=\operatorname{span}\{(1,1,0),(0,1,1)\}$ 的正交补 $W^\perp$。

**过程**

把 $\{(1,1,0),(0,1,1)\}$ 扩充为 $\mathbb R^3$ 的正交基：$u_1=(1,1,0)$；$u_2=(0,1,1)-\dfrac{(0,1,1)\cdot(1,1,0)}{2}(1,1,0)=(0,1,1)-\dfrac{1}{2}(1,1,0)=\left(-\dfrac{1}{2},\dfrac{1}{2},1\right)$，取 $(-1,1,2)$。再取 $e_3=(0,0,1)$ 去掉前两者的投影：$u_3=(0,0,1)-0-\dfrac{(0,0,1)\cdot(-1,1,2)}{6}(-1,1,2)=(0,0,1)-\dfrac{1}{3}(-1,1,2)=\left(\dfrac{1}{3},-\dfrac{1}{3},\dfrac{1}{3}\right)$，取 $(1,-1,1)$。它与 $u_1,u_2$ 均正交，故 $W^\perp=\operatorname{span}\{(1,-1,1)\}$。

**答案原文**

$W^\perp=\operatorname{span}\{(1,-1,1)\}$（一维）

## 276. eval-linalg-027-s3

内容 SHA256：`0b155ccdfdba5bb8c02731c1b38ec771baa9f56c219704c7e18d3c800c496aa2`。

来源：data/v2/eval/dataset_eval.jsonl，第 276 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

求 $\mathbb R^3$ 中子空间 $W=\operatorname{span}\{(1,1,0),(0,1,1)\}$ 的正交补 $W^\perp$。

**过程**

$(1,1,0)\times(0,1,1)=(1\cdot 1-0\cdot 1,\ 0\cdot 0-1\cdot 1,\ 1\cdot 1-1\cdot 0)=(1,-1,1)$，与两生成元都垂直，故 $W^\perp=\operatorname{span}\{(1,-1,1)\}$（$\dim W^\perp=3-2=1$）。

**答案原文**

$W^\perp=\operatorname{span}\{(1,-1,1)\}$（一维）

## 277. eval-linalg-028-s1

内容 SHA256：`52e8858ce578223e22fda1c77b9f9839ad3193274059071853cc01bba4f8a1af`。

来源：data/v2/eval/dataset_eval.jsonl，第 277 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

在 $\mathbb R^2$ 中，求向量 $\alpha=(2,3)$ 在基 $\beta_1=(1,2)$、$\beta_2=(1,1)$ 下的坐标。

**过程**

设 $\alpha=x_1\beta_1+x_2\beta_2$，即 $\begin{cases}x_1+x_2=2\\2x_1+x_2=3\end{cases}$。两式相减：$x_1=1$，代回得 $x_2=1$。故坐标为 $(1,1)$。

**答案原文**

$(1,1)$

## 278. eval-linalg-028-s2

内容 SHA256：`1bba6b6e24e5734d6906206c368ec10849e744d1b23f2147192176b6350ab105`。

来源：data/v2/eval/dataset_eval.jsonl，第 278 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

在 $\mathbb R^2$ 中，求向量 $\alpha=(2,3)$ 在基 $\beta_1=(1,2)$、$\beta_2=(1,1)$ 下的坐标。

**过程**

从标准基到基 $\{\beta_1,\beta_2\}$ 的过渡矩阵 $P=\begin{pmatrix}1&1\\2&1\end{pmatrix}$（列为基向量）。$\alpha=P\xi$，其中 $\xi$ 为所求坐标。$P^{-1}=\dfrac{1}{1-2}\begin{pmatrix}1&-1\\-2&1\end{pmatrix}=\begin{pmatrix}-1&1\\2&-1\end{pmatrix}$。故 $\xi=P^{-1}\alpha=\begin{pmatrix}-1&1\\2&-1\end{pmatrix}\begin{pmatrix}2\\3\end{pmatrix}=\begin{pmatrix}-2+3\\4-3\end{pmatrix}=\begin{pmatrix}1\\1\end{pmatrix}$。

**答案原文**

$(1,1)$

## 279. eval-linalg-028-s3

内容 SHA256：`59239fba5a49dd2a0035a8648a87d6093bb596a856ba0edf67a89011cc297570`。

来源：data/v2/eval/dataset_eval.jsonl，第 279 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

在 $\mathbb R^2$ 中，求向量 $\alpha=(2,3)$ 在基 $\beta_1=(1,2)$、$\beta_2=(1,1)$ 下的坐标。

**过程**

在图上作平行四边形：$\alpha=(2,3)$ 可由 $\beta_1+\beta_2=(2,3)$ 一次组合而成（$1\cdot(1,2)+1\cdot(1,1)=(2,3)$），坐标即组合系数 $(1,1)$。

**答案原文**

$(1,1)$

## 280. eval-linalg-029-s1

内容 SHA256：`1bc76c4970e05215e42b4d475ff2e0498f45a66b3efeb808ea8b35d13125d3b8`。

来源：data/v2/eval/dataset_eval.jsonl，第 280 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设线性变换 $T:\mathbb R^2\to\mathbb R^2$ 为 $T(x,y)=(x+2y,2x+y)$。求 $\ker T$ 与 $\operatorname{Im}T$，并说明其维数关系。

**过程**

$T$ 的矩阵 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$，$\det A=1-4=-3\ne 0$，故 $A$ 可逆，$T$ 为同构：$\ker T=\{0\}$（零维），$\operatorname{Im}T=\mathbb R^2$（二维），维数公式 $0+2=2$ 成立。

**答案原文**

$\ker T=\{(0,0)\}$；$\operatorname{Im}T=\mathbb R^2$；$\dim\ker T+\dim\operatorname{Im}T=2$

## 281. eval-linalg-029-s2

内容 SHA256：`8435b65443070169f2e068ecf20409c604de1eafed1dabb7ca6c9bb11d0950cc`。

来源：data/v2/eval/dataset_eval.jsonl，第 281 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设线性变换 $T:\mathbb R^2\to\mathbb R^2$ 为 $T(x,y)=(x+2y,2x+y)$。求 $\ker T$ 与 $\operatorname{Im}T$，并说明其维数关系。

**过程**

核：解 $\begin{cases}x+2y=0\\2x+y=0\end{cases}$，第一式 $x=-2y$ 代入第二式：$-4y+y=-3y=0$，$y=0$，$x=0$，故 $\ker T=\{(0,0)\}$。像：对任意 $(u,v)$，解 $\begin{cases}x+2y=u\\2x+y=v\end{cases}$，由第二式 $y=v-2x$ 代入第一式：$x+2v-4x=u$，$x=\dfrac{2v-u}{3}$，$y=v-2\cdot\dfrac{2v-u}{3}=\dfrac{2u-v}{3}$，恒有解，故 $\operatorname{Im}T=\mathbb R^2$。

**答案原文**

$\ker T=\{(0,0)\}$；$\operatorname{Im}T=\mathbb R^2$；$\dim\ker T+\dim\operatorname{Im}T=2$

## 282. eval-linalg-029-s3

内容 SHA256：`957a5f844f2763ec838dbe583cbea1634a312352dfb0a1c6173167cdf06372b4`。

来源：data/v2/eval/dataset_eval.jsonl，第 282 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设线性变换 $T:\mathbb R^2\to\mathbb R^2$ 为 $T(x,y)=(x+2y,2x+y)$。求 $\ker T$ 与 $\operatorname{Im}T$，并说明其维数关系。

**过程**

$T\circ T$ 的矩阵 $A^2=\begin{pmatrix}5&4\\4&5\end{pmatrix}$，$\det A^2=9\ne 0$，仍为同构。或由特征值观点：$A$ 的特征值为 $3,-1$（eval-linalg-015），均非零，故核为零、像为全空间。

**答案原文**

$\ker T=\{(0,0)\}$；$\operatorname{Im}T=\mathbb R^2$；$\dim\ker T+\dim\operatorname{Im}T=2$

## 283. eval-linalg-030-s1

内容 SHA256：`d4d3af0b92f3fe7f00e6f7918bf4e846a48eaba76183845fa666d9fd41d4dd8b`。

来源：data/v2/eval/dataset_eval.jsonl，第 283 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

用 Gram–Schmidt 正交化方法把向量组 $(1,1,0),(1,0,1),(0,1,1)$ 化为正交向量组。

**过程**

取 $u_1=(1,1,0)$。$u_2=(1,0,1)-\dfrac{(1,0,1)\cdot u_1}{\|u_1\|^2}u_1=(1,0,1)-\dfrac{1}{2}(1,1,0)=\left(\dfrac{1}{2},-\dfrac{1}{2},1\right)$，乘 2 取 $u_2=(1,-1,2)$。$u_3=(0,1,1)-\dfrac{(0,1,1)\cdot u_1}{\|u_1\|^2}u_1-\dfrac{(0,1,1)\cdot u_2}{\|u_2\|^2}u_2=(0,1,1)-\dfrac{1}{2}(1,1,0)-\dfrac{1}{6}(1,-1,2)=\left(-\dfrac{2}{3},\dfrac{2}{3},\dfrac{2}{3}\right)$，乘 $-\dfrac{3}{2}$ 取 $u_3=(1,-1,-1)$。验证：$u_1\cdot u_2=0$，$u_1\cdot u_3=1-1+0=0$，$u_2\cdot u_3=1+1-2=0$，两两正交。

**答案原文**

$u_1=(1,1,0)$，$u_2=(1,-1,2)$，$u_3=(1,-1,-1)$（可各乘常数）

## 284. eval-linalg-030-s2

内容 SHA256：`9189445a15159f11b2ae6ee274afc03b04f6298232204d7653db27358c48684a`。

来源：data/v2/eval/dataset_eval.jsonl，第 284 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

用 Gram–Schmidt 正交化方法把向量组 $(1,1,0),(1,0,1),(0,1,1)$ 化为正交向量组。

**过程**

三个向量关于坐标轮换对称。取和向量 $v_1=(1,1,1)$（在张成空间内，因 $v_1=\dfrac{(1,1,0)+(1,0,1)+(0,1,1)}{2}$ 验证：$\dfrac{(2,2,2)}{2}=(1,1,1)$）；取差向量 $v_2=(1,0,-1)$：$v_1\cdot v_2=0$；取 $v_3=v_1\times v_2=(1,1,1)\times(1,0,-1)=(1\cdot(-1)-1\cdot 0,\ 1\cdot 1-1\cdot(-1),\ 1\cdot 0-1\cdot 1)=(-1,2,-1)$。验证 $v_3$ 在张成空间内：$(1,1,0)-2(1,0,1)+(0,1,1)=(-1,2,-1)$；且 $v_3\cdot v_1=0$、$v_3\cdot v_2=0$。故 $\{(1,1,1),(1,0,-1),(-1,2,-1)\}$ 亦为正交基（这是利用对称性的替代正交基构造，与按原顺序做 Gram–Schmidt 的输出不必相同）。

**答案原文**

$u_1=(1,1,0)$，$u_2=(1,-1,2)$，$u_3=(1,-1,-1)$（可各乘常数）

## 285. eval-linalg-030-s3

内容 SHA256：`30b1499cd609585a09ed41b99d7732ac34efeb80dc549a049d06059dfc3cb4ab`。

来源：data/v2/eval/dataset_eval.jsonl，第 285 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

用 Gram–Schmidt 正交化方法把向量组 $(1,1,0),(1,0,1),(0,1,1)$ 化为正交向量组。

**过程**

验证解法一的三向量线性无关：行列式 $\begin{vmatrix}1&1&0\\1&-1&2\\1&-1&-1\end{vmatrix}=1\cdot(1+2)-1\cdot(-1-2)+0=3+3=6\ne 0$。且三者张成的空间与原组相同（原组行列式 $\begin{vmatrix}1&1&0\\1&0&1\\0&1&1\end{vmatrix}=-2\ne 0$，两组都张成 $\mathbb R^3$），故正交化合法。

**答案原文**

$u_1=(1,1,0)$，$u_2=(1,-1,2)$，$u_3=(1,-1,-1)$（可各乘常数）

## 286. eval-linalg-031-s1

内容 SHA256：`accda139586476694f69f165e35887093c74968e0d2c78291b1be398272cae6f`。

来源：data/v2/eval/dataset_eval.jsonl，第 286 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 4 阶矩阵 $A$ 的最小多项式为 $m_A(\lambda)=(\lambda-2)^2(\lambda-3)$,且 $\operatorname{tr}(A)=9$。求 $A$ 的所有可能若尔当标准形,并说明最小多项式如何决定各若尔当块的最大阶数。

**过程**

$m_A$ 的根为 $2,3$,故 $A$ 的谱为 $\{2,3\}$。因子 $(\lambda-2)^2$ 表明 2 对应若尔当块的最大阶数为 2(且恰有一块取到 2 阶);因子 $(\lambda-3)$ 无平方,表明 3 对应块全为 1 阶。$n=4$ 且 3 的重数至少为 1,故 2 的重数为 2 或 3。若 2 重数为 2:块为 $J_2(2)\oplus J_1(3)\oplus J_1(3)$,迹 $=2+2+3+3=10\neq 9$,排除。若 2 重数为 3:块为 $J_2(2)\oplus J_1(2)\oplus J_1(3)$,共 $2+1+1=4$ 阶,迹 $=2+2+2+3=9$,符合。故唯一。

**答案原文**

唯一:$\operatorname{diag}\!\bigl(J_2(2),\,2,\,3\bigr)=\begin{pmatrix}2&1&0&0\\0&2&0&0\\0&0&2&0\\0&0&0&3\end{pmatrix}$,其中 $J_2(2)=\begin{pmatrix}2&1\\0&2\end{pmatrix}$

## 287. eval-linalg-031-s2

内容 SHA256：`a9358f02685ca05c6e26bd9d93511ebe14a55af6347ff4d94bee93a39e0b9d9f`。

来源：data/v2/eval/dataset_eval.jsonl，第 287 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 4 阶矩阵 $A$ 的最小多项式为 $m_A(\lambda)=(\lambda-2)^2(\lambda-3)$,且 $\operatorname{tr}(A)=9$。求 $A$ 的所有可能若尔当标准形,并说明最小多项式如何决定各若尔当块的最大阶数。

**过程**

特征多项式 $f_A$ 与 $m_A$ 有相同根,$f_A=(\lambda-2)^{r_2}(\lambda-3)^{r_3}$,$r_2+r_3=4$,$r_2\ge 2$,$r_3\ge 1$,故 $(r_2,r_3)=(3,1)$ 或 $(2,2)$。迹 $=2r_2+3r_3$:$(3,1)$ 给 $6+3=9$;$(2,2)$ 给 $4+6=10$。故 $r_2=3,r_3=1$。2 的块:最大块阶为 2(由 $(\lambda-2)^2$ 整除 $m_A$)且总维数为 3,故块大小拆分为 $2+1$,即 $J_2(2)\oplus J_1(2)$;3 的块为 $J_1(3)$。故唯一:$\operatorname{diag}\!\bigl(J_2(2),2,3\bigr)$。

**答案原文**

唯一:$\operatorname{diag}\!\bigl(J_2(2),\,2,\,3\bigr)=\begin{pmatrix}2&1&0&0\\0&2&0&0\\0&0&2&0\\0&0&0&3\end{pmatrix}$,其中 $J_2(2)=\begin{pmatrix}2&1\\0&2\end{pmatrix}$

## 288. eval-linalg-031-s3

内容 SHA256：`7a3d92589f34a8429d74bd5e92a2b3f35f4bfbec029850cafebe6d6038934325`。

来源：data/v2/eval/dataset_eval.jsonl，第 288 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 4 阶矩阵 $A$ 的最小多项式为 $m_A(\lambda)=(\lambda-2)^2(\lambda-3)$,且 $\operatorname{tr}(A)=9$。求 $A$ 的所有可能若尔当标准形,并说明最小多项式如何决定各若尔当块的最大阶数。

**过程**

$m_A$ 的两个互素因子给出主分解 $V=\ker(A-2I)^2\oplus\ker(A-3I)$。$\ker(A-3I)$ 的维数等于 3 的重数 $r_3$;$\ker(A-2I)^2$ 的维数等于 2 的重数 $r_2$。由 $r_2+r_3=4$、$r_2\ge 2$、$r_3\ge 1$ 与迹 $2r_2+3r_3=9$ 得 $r_2=3,\ r_3=1$。在 $V_2=\ker(A-2I)^2$ 上,幂零部分 $N=A-2I$ 满足 $N^2=0$ 且 $N\neq 0$($N=0$ 会给 $m_A$ 带来因子 $(\lambda-2)$ 而非 $(\lambda-2)^2$),故 $N$ 的幂零指数恰为 2,$V_2$ 上的块为 $J_2(2)\oplus J_1(2)$;$V_3$ 一维,块为 $J_1(3)$。故唯一:$\operatorname{diag}\!\bigl(J_2(2),2,3\bigr)$。

**答案原文**

唯一:$\operatorname{diag}\!\bigl(J_2(2),\,2,\,3\bigr)=\begin{pmatrix}2&1&0&0\\0&2&0&0\\0&0&2&0\\0&0&0&3\end{pmatrix}$,其中 $J_2(2)=\begin{pmatrix}2&1\\0&2\end{pmatrix}$

## 289. eval-linalg-032-s1

内容 SHA256：`bf134742feef617b7a1c580377d4137a794fbc5cb8742d8c3931c01bb696bc46`。

来源：data/v2/eval/dataset_eval.jsonl，第 289 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $a\in\mathbb R$ 为参数,$\lambda$-矩阵 $A(\lambda)=\begin{pmatrix}\lambda-a&1&0\\0&\lambda-1&1\\0&0&\lambda-1\end{pmatrix}$。求 $A(\lambda)$ 的不变因子与初等因子,并讨论 $a$ 的取值如何影响初等因子(何时两个不同根的初等因子合并、重数如何变化)。

**过程**

一阶行列式因子 $D_1=1$。二阶子式中含 $\begin{vmatrix}1&0\\\lambda-1&1\end{vmatrix}=1$,故二阶行列式因子 $D_2=\gcd(\cdots,1,\cdots)=1$。三阶行列式因子 $D_3=|A(\lambda)|=(\lambda-a)(\lambda-1)^2$。不变因子 $d_1=D_1=1$,$d_2=\dfrac{D_2}{D_1}=1$,$d_3=\dfrac{D_3}{D_2}=(\lambda-a)(\lambda-1)^2$。初等因子即不变因子分解出的互异幂因子:$a\neq 1$ 时 $d_3$ 给出 $\lambda-a$ 与 $(\lambda-1)^2$ 两个初等因子;$a=1$ 时 $\lambda-a$ 与 $(\lambda-1)^2$ 的根重合,$d_3=(\lambda-1)^3$ 成为一个三重初等因子。

**答案原文**

不变因子:$1,\ 1,\ (\lambda-a)(\lambda-1)^2$;初等因子:$a\neq 1$ 时为 $\lambda-a$ 与 $(\lambda-1)^2$;$a=1$ 时为 $(\lambda-1)^3$

## 290. eval-linalg-032-s2

内容 SHA256：`c77bd8b9bbe9056a13e4df856f1056c9a4210689df6a403aaa6c71839f68de72`。

来源：data/v2/eval/dataset_eval.jsonl，第 290 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $a\in\mathbb R$ 为参数,$\lambda$-矩阵 $A(\lambda)=\begin{pmatrix}\lambda-a&1&0\\0&\lambda-1&1\\0&0&\lambda-1\end{pmatrix}$。求 $A(\lambda)$ 的不变因子与初等因子,并讨论 $a$ 的取值如何影响初等因子(何时两个不同根的初等因子合并、重数如何变化)。

**过程**

交换第 1、2 列得 $\begin{pmatrix}1&\lambda-a&0\\\lambda-1&0&1\\0&0&\lambda-1\end{pmatrix}$;第 2 行减去第 1 行的 $(\lambda-1)$ 倍、第 2 列减去第 1 列的 $(\lambda-a)$ 倍,得 $\begin{pmatrix}1&0&0\\0&-(\lambda-a)(\lambda-1)&1\\0&0&\lambda-1\end{pmatrix}$;再交换第 2、3 列,第 3 行减去第 2 行的 $(\lambda-1)$ 倍,第 3 列加回第 2 列的 $(\lambda-a)(\lambda-1)$ 倍,得标准形 $\operatorname{diag}\!\bigl(1,\,1,\,(\lambda-a)(\lambda-1)^2\bigr)$。不变因子读出 $1,\ 1,\ (\lambda-a)(\lambda-1)^2$。末项分解得初等因子:$a\neq 1$ 时为 $\lambda-a$ 与 $(\lambda-1)^2$ 两个;$a=1$ 时两者根重合,合并为 $(\lambda-1)^3$ 一个。

**答案原文**

不变因子:$1,\ 1,\ (\lambda-a)(\lambda-1)^2$;初等因子:$a\neq 1$ 时为 $\lambda-a$ 与 $(\lambda-1)^2$;$a=1$ 时为 $(\lambda-1)^3$

## 291. eval-linalg-032-s3

内容 SHA256：`1c6d0c1e0abe01072c21efed8c41c4a7e7407a4a72ddf54c9700ed52abbbdee3`。

来源：data/v2/eval/dataset_eval.jsonl，第 291 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $a\in\mathbb R$ 为参数,$\lambda$-矩阵 $A(\lambda)=\begin{pmatrix}\lambda-a&1&0\\0&\lambda-1&1\\0&0&\lambda-1\end{pmatrix}$。求 $A(\lambda)$ 的不变因子与初等因子,并讨论 $a$ 的取值如何影响初等因子(何时两个不同根的初等因子合并、重数如何变化)。

**过程**

令 $B(a)=\begin{pmatrix}a&-1&0\\0&1&-1\\0&0&1\end{pmatrix}$,则 $A(\lambda)=\lambda I-B(a)$。取 $e_3=(0,0,1)^T$,直接计算: $$(e_3,\ B e_3,\ B^2 e_3)=\begin{pmatrix}0&0&1\\0&-1&-2\\1&1&1\end{pmatrix},\qquad \det=1\neq 0,$$ 故 $\{e_3,Be_3,B^2e_3\}$ 构成基,$e_3$ 对所有 $a$ 都是 $B$ 的循环向量,因此 $m_B$ 的次数为 3,与特征多项式 $\chi_B(\lambda)=(\lambda-a)(\lambda-1)^2$ 相同,即 $m_B=\chi_B$。于是 $A(\lambda)$ 的不变因子为 $1,\ 1,\ (\lambda-a)(\lambda-1)^2$(唯一非平凡不变因子等于特征多项式)。初等因子:$a\neq 1$ 时为 $\lambda-a$ 与 $(\lambda-1)^2$,对应块 $\operatorname{diag}\!\bigl(a,\,J_2(1)\bigr)$,其中 $J_2(1)=\begin{pmatrix}1&1\\0&1\end{pmatrix}$;$a=1$ 时合并为 $(\lambda-1)^3$,对应块 $J_3(1)=\begin{pmatrix}1&1&0\\0&1&1\\0&0&1\end{pmatrix}$。**所有参数取值下均不可对角化**($a\neq 1$ 时已含 $J_2(1)$ 块);$a$ 从 $\neq 1$ 变到 1 时,变化是初等因子合并、最大若尔当块由二阶升为三阶。

**答案原文**

不变因子:$1,\ 1,\ (\lambda-a)(\lambda-1)^2$;初等因子:$a\neq 1$ 时为 $\lambda-a$ 与 $(\lambda-1)^2$;$a=1$ 时为 $(\lambda-1)^3$

## 292. eval-linalg-033-s1

内容 SHA256：`746134a6fe52edee4a240c49757c008a385bcf2e10fc46e3aaa472bc4580e991`。

来源：data/v2/eval/dataset_eval.jsonl，第 292 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $A=\begin{pmatrix}0&1\\0&0\end{pmatrix}$，求矩阵指数 $e^{tA}$（$t$ 为参数）。

**过程**

$A^2=\begin{pmatrix}0&1\\0&0\end{pmatrix}\begin{pmatrix}0&1\\0&0\end{pmatrix}=0$，故 $A^k=0$（$k\ge 2$）。$e^{tA}=I+tA+\dfrac{t^2A^2}{2!}+\cdots=I+tA=\begin{pmatrix}1&t\\0&1\end{pmatrix}$。

**答案原文**

$e^{tA}=\begin{pmatrix}1&t\\0&1\end{pmatrix}$

## 293. eval-linalg-033-s2

内容 SHA256：`80b041b073244ff66bb746474ac400ccf03ec18d22eadec63f0b6a984f5b9e72`。

来源：data/v2/eval/dataset_eval.jsonl，第 293 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $A=\begin{pmatrix}0&1\\0&0\end{pmatrix}$，求矩阵指数 $e^{tA}$（$t$ 为参数）。

**过程**

方程组 $\dfrac{d}{dt}\begin{pmatrix}x\\y\end{pmatrix}=A\begin{pmatrix}x\\y\end{pmatrix}$，即 $\begin{cases}x'=y\\y'=0\end{cases}$。解得 $y(t)=y_0$，$x(t)=x_0+y_0t$，即 $\begin{pmatrix}x\\y\end{pmatrix}=\begin{pmatrix}1&t\\0&1\end{pmatrix}\begin{pmatrix}x_0\\y_0\end{pmatrix}$。基解矩阵（满足 $\Phi(0)=I$）即 $e^{tA}=\begin{pmatrix}1&t\\0&1\end{pmatrix}$。

**答案原文**

$e^{tA}=\begin{pmatrix}1&t\\0&1\end{pmatrix}$

## 294. eval-linalg-033-s3

内容 SHA256：`b3e55284a78ae93279ac5c29a5f338e653680d3551c2c09b1021aa9c8efe5e72`。

来源：data/v2/eval/dataset_eval.jsonl，第 294 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

设 $A=\begin{pmatrix}0&1\\0&0\end{pmatrix}$，求矩阵指数 $e^{tA}$（$t$ 为参数）。

**过程**

$(sI-A)^{-1}=\begin{pmatrix}s&-1\\0&s\end{pmatrix}^{-1}=\dfrac{1}{s^2}\begin{pmatrix}s&1\\0&s\end{pmatrix}=\begin{pmatrix}1/s&1/s^2\\0&1/s\end{pmatrix}$。逐项取拉普拉斯逆变换（$\mathcal L^{-1}\{1/s\}=1$，$\mathcal L^{-1}\{1/s^2\}=t$），得 $e^{tA}=\begin{pmatrix}1&t\\0&1\end{pmatrix}$。

**答案原文**

$e^{tA}=\begin{pmatrix}1&t\\0&1\end{pmatrix}$

## 295. eval-linalg-034-s1

内容 SHA256：`8e24cb718a9194db3cb5f15d502870d0a15499d10003aa829a3945973280f9cc`。

来源：data/v2/eval/dataset_eval.jsonl，第 295 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

证明 Cauchy–Schwarz 不等式：对任意向量 $\vec a,\vec b$，$|\vec a\cdot\vec b|\le|\vec a||\vec b|$。

**过程**

若 $\vec b=\vec 0$ 不等式平凡成立。设 $\vec b\ne\vec 0$，对任意实数 $t$，$0\le|\vec a+t\vec b|^2=|\vec a|^2+2t(\vec a\cdot\vec b)+t^2|\vec b|^2$。该二次函数恒非负，故判别式 $\Delta=4(\vec a\cdot\vec b)^2-4|\vec a|^2|\vec b|^2\le 0$，即 $(\vec a\cdot\vec b)^2\le|\vec a|^2|\vec b|^2$，开方得 $|\vec a\cdot\vec b|\le|\vec a||\vec b|$。等号成立当且仅当 $\vec a+t\vec b=\vec 0$（$\vec a$ 与 $\vec b$ 线性相关）。

**答案原文**

证毕（三种证法）

## 296. eval-linalg-034-s2

内容 SHA256：`726c6cdc9a2ab9771b8cc23a82e801e038202400410de24d5371bfa0d2e12693`。

来源：data/v2/eval/dataset_eval.jsonl，第 296 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

证明 Cauchy–Schwarz 不等式：对任意向量 $\vec a,\vec b$，$|\vec a\cdot\vec b|\le|\vec a||\vec b|$。

**过程**

若 $\vec b=\vec 0$ 不等式平凡成立。以下设 $\vec b\ne\vec 0$，把 $\vec a$ 分解为 $\vec a=\vec a_\parallel+\vec a_\perp$，其中 $\vec a_\parallel=\dfrac{\vec a\cdot\vec b}{|\vec b|^2}\vec b$ 与 $\vec b$ 平行，$\vec a_\perp\perp\vec b$。由勾股定理 $|\vec a|^2=|\vec a_\parallel|^2+|\vec a_\perp|^2\ge|\vec a_\parallel|^2=\dfrac{(\vec a\cdot\vec b)^2}{|\vec b|^2}$，移项即得。等号成立当且仅当 $\vec a_\perp=\vec 0$。

**答案原文**

证毕（三种证法）

## 297. eval-linalg-034-s3

内容 SHA256：`79337367518c1eed968c6a84691df947091e6a04d3e8535e6c803d592232c4b2`。

来源：data/v2/eval/dataset_eval.jsonl，第 297 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

证明 Cauchy–Schwarz 不等式：对任意向量 $\vec a,\vec b$，$|\vec a\cdot\vec b|\le|\vec a||\vec b|$。

**过程**

对随机变量 $X,Y$ 有 $E[(tX+Y)^2]\ge 0$ 对任意 $t$，故二阶矩矩阵（当 $E[X]=E[Y]=0$ 时即协方差矩阵，一般情形称 Gram 矩阵）$\begin{pmatrix}E[X^2]&E[XY]\\E[XY]&E[Y^2]\end{pmatrix}$ 半正定，行列式 $E[X^2]E[Y^2]-(E[XY])^2\ge 0$，即 $(E[XY])^2\le E[X^2]E[Y^2]$。取有限样本空间上的随机变量与内积 $\langle X,Y\rangle=E[XY]$ 对应（必要时先中心化），即得向量形式的 Cauchy–Schwarz。

**答案原文**

证毕（三种证法）

## 298. eval-linalg-035-s1

内容 SHA256：`2c80db99f4db937c4e1e6e3d56a35eaaa613f197ae9e5dd4b341a5156ffae9db`。

来源：data/v2/eval/dataset_eval.jsonl，第 298 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

证明：$n$ 阶实方阵 $A$ 是正交矩阵（$A^TA=I$）当且仅当 $A$ 的列向量构成 $\mathbb R^n$ 的标准正交基。

**过程**

把 $A$ 按列分块 $A=(a_1,a_2,\dots,a_n)$。$A^TA$ 的 $(i,j)$ 元为 $a_i^Ta_j=a_i\cdot a_j$。$A^TA=I\iff a_i\cdot a_j=\delta_{ij}$ 对一切 $i,j$ 成立 $\iff$ 列向量两两正交且都是单位向量 $\iff$ 列向量构成标准正交基（$n$ 个两两正交的单位向量必线性无关，因若 $\sum c_ia_i=0$ 则与 $a_j$ 作内积得 $c_j=0$）。

**答案原文**

证毕（三种证法）

## 299. eval-linalg-035-s2

内容 SHA256：`92904062d70fd41d5b5cdf20046644442a1679026f4acb467a1bbde46e7ee74e`。

来源：data/v2/eval/dataset_eval.jsonl，第 299 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

证明：$n$ 阶实方阵 $A$ 是正交矩阵（$A^TA=I$）当且仅当 $A$ 的列向量构成 $\mathbb R^n$ 的标准正交基。

**过程**

$A^TA=I\iff$ 对任意 $x$，$|Ax|^2=(Ax)^T(Ax)=x^TA^TAx=x^Tx=|x|^2$，即 $A$ 保长。由极化恒等式 $(Ax,Ay)=\dfrac{|A(x+y)|^2-|Ax|^2-|Ay|^2}{2}=\dfrac{|x+y|^2-|x|^2-|y|^2}{2}=(x,y)$，保长⇒保内积。取 $x=e_i$、$y=e_j$：$(Ae_i,Ae_j)=(e_i,e_j)=\delta_{ij}$，即列向量标准正交。反之列向量标准正交⇒$A^TA=I$ 由解法一。

**答案原文**

证毕（三种证法）

## 300. eval-linalg-035-s3

内容 SHA256：`46b83753d4e415b69f6521e9fffb4cfb5cf2fa3d72b20f94a32d78467d233391`。

来源：data/v2/eval/dataset_eval.jsonl，第 300 行；源 SHA256 `187913709744c008dd8bd18a56910845156b748a3d935f3496a047e321a18866`。

**题干**

证明：$n$ 阶实方阵 $A$ 是正交矩阵（$A^TA=I$）当且仅当 $A$ 的列向量构成 $\mathbb R^n$ 的标准正交基。

**过程**

由 $A^TA=I$ 取行列式得 $(\det A)^2=1$，故正交矩阵的行列式为 $\pm 1$；又若 $Ax=\lambda x$，则 $|x|^2=|Ax|^2=|\lambda|^2|x|^2$，故特征值的模为 1。反之行列式为 $\pm 1$ 或特征值模为 1 都不足以保证正交（反例：$\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 的行列式为 1、特征值均为 1，但列向量不垂直，非正交矩阵），说明"列标准正交"才是充要条件。

**答案原文**

证毕（三种证法）

## 301. test-calc-001

内容 SHA256：`80bfc92b5954bcbbcb29467182d09bd272a1d28a83dabc250c161a843159bb84`。

来源：data/v2/test/dataset_test.jsonl，第 1 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求极限 $\displaystyle\lim_{n\to\infty}\frac{1}{n}\sum_{k=1}^{n}\sin\frac{k\pi}{n}$。

**过程**

该和式为函数 $f(x)=\sin(\pi x)$ 在 $[0,1]$ 上 $n$ 等分的黎曼和（取右端点 $\dfrac{k}{n}$）：$\dfrac{1}{n}\displaystyle\sum_{k=1}^{n}\sin\dfrac{k\pi}{n}=\sum_{k=1}^{n}\sin\left(\pi\cdot\dfrac{k}{n}\right)\cdot\dfrac{1}{n}$。由定积分定义，$\lim_{n\to\infty}\dfrac{1}{n}\displaystyle\sum_{k=1}^{n}\sin\dfrac{k\pi}{n}=\int_0^1\sin(\pi x)\,dx=\left[-\dfrac{\cos\pi x}{\pi}\right]_0^1=-\dfrac{\cos\pi}{\pi}+\dfrac{\cos 0}{\pi}=\dfrac{1}{\pi}+\dfrac{1}{\pi}=\dfrac{2}{\pi}$。

**答案原文**

$\dfrac{2}{\pi}$

## 302. test-calc-002

内容 SHA256：`c46e3de89ed0ee6cf704fd1311a810b982d6c49e45c9167f54d78b73d4f3dd2c`。

来源：data/v2/test/dataset_test.jsonl，第 2 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求极限 $\displaystyle\lim_{n\to\infty}n^2\left(1-\cos\frac{1}{n}\right)$。

**过程**

由 $\cos x=1-\dfrac{x^2}{2}+o(x^2)$，取 $x=\dfrac{1}{n}\to 0$：$1-\cos\dfrac{1}{n}=\dfrac{1}{2n^2}+o\left(\dfrac{1}{n^2}\right)$。故 $n^2\left(1-\cos\dfrac{1}{n}\right)=n^2\cdot\dfrac{1}{2n^2}+n^2\cdot o\left(\dfrac{1}{n^2}\right)\to\dfrac{1}{2}$。

**答案原文**

$\dfrac{1}{2}$

## 303. test-calc-003

内容 SHA256：`3aa21b2d34d0b9c1f117255de1860e51d75849b2a811a888c637d9f7a5fa936d`。

来源：data/v2/test/dataset_test.jsonl，第 3 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $F(x)=\displaystyle\int_1^x\frac{\ln t}{t}\,dt$（$x>0$）。求 $F'(x)$、$F''(x)$，并给出 $F(x)$ 的显式表达式。

**过程**

由微积分基本定理，$F'(x)=\dfrac{\ln x}{x}$。再求导：$F''(x)=\dfrac{\frac{1}{x}\cdot x-\ln x\cdot 1}{x^2}=\dfrac{1-\ln x}{x^2}$。显式积分：令 $u=\ln t$（$du=\dfrac{dt}{t}$），$F(x)=\displaystyle\int_0^{\ln x}u\,du=\dfrac{(\ln x)^2}{2}$（下限 $t=1$ 对应 $u=0$）。验证：$F'(x)=\dfrac{2\ln x}{2}\cdot\dfrac{1}{x}=\dfrac{\ln x}{x}$，一致。

**答案原文**

$F'(x)=\dfrac{\ln x}{x}$；$F''(x)=\dfrac{1-\ln x}{x^2}$；$F(x)=\dfrac{(\ln x)^2}{2}$

## 304. test-calc-004

内容 SHA256：`3ed75bec2f567e55b0d93213981383b62599727383082b0fb391ac5aa8ee1d05`。

来源：data/v2/test/dataset_test.jsonl，第 4 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求微分方程 $y'+2y=e^{-x}$ 的通解。

**过程**

积分因子 $\mu(x)=e^{\int 2\,dx}=e^{2x}$。方程两边乘 $e^{2x}$：$e^{2x}y'+2e^{2x}y=e^{x}$，即 $(e^{2x}y)'=e^{x}$。积分得 $e^{2x}y=e^{x}+C$，故通解 $y=e^{-x}+Ce^{-2x}$。

**答案原文**

$y=e^{-x}+Ce^{-2x}$

## 305. test-calc-005

内容 SHA256：`e6763c0cedd9d28b12382708ace8c90e76f2f63d0dc30c59234be185e17b6abe`。

来源：data/v2/test/dataset_test.jsonl，第 5 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

用积分判别法判断级数 $\displaystyle\sum_{n=2}^{\infty}\frac{1}{n\ln n}$ 的敛散性。

**过程**

$f(x)=\dfrac{1}{x\ln x}$ 在 $[2,+\infty)$ 上非负递减。$\displaystyle\int_2^{+\infty}\dfrac{dx}{x\ln x}=\lim_{b\to\infty}\left[\ln(\ln x)\right]_2^b=\lim_{b\to\infty}\left(\ln(\ln b)-\ln(\ln 2)\right)=+\infty$，发散。由积分判别法，级数 $\sum\dfrac{1}{n\ln n}$ 发散。

**答案原文**

发散

## 306. test-calc-006

内容 SHA256：`8e386689e943530f6e4ad5e418e2cb0f5bd2c15230ec2c152346a6b42c85f838`。

来源：data/v2/test/dataset_test.jsonl，第 6 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $f(x)=\ln(1+x)$ 的麦克劳林展开式，并归纳 $f^{(n)}(0)$ 的规律。

**过程**

逐阶求导：$f'(x)=(1+x)^{-1}$，$f''(x)=-(1+x)^{-2}$，$f'''(x)=2(1+x)^{-3}$，$f^{(4)}(x)=-6(1+x)^{-4}$。归纳得 $f^{(n)}(x)=(-1)^{n-1}(n-1)!\,(1+x)^{-n}$（$n\ge 1$），故 $f^{(n)}(0)=(-1)^{n-1}(n-1)!$。麦克劳林展开：$\ln(1+x)=\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}x^n}{n}$（$|x|<1$）。

**答案原文**

$\ln(1+x)=\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}x^n}{n}$；$f^{(n)}(0)=(-1)^{n-1}(n-1)!$

## 307. test-calc-007

内容 SHA256：`8f5d5acb698e721b46e44baff29df525dcf743ce6664086e5fb69bf750309acc`。

来源：data/v2/test/dataset_test.jsonl，第 7 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $f$ 二阶可导且 $f(0)=f'(0)=0$，求 $\displaystyle\lim_{x\to 0}\frac{f(x)}{x^2}$。

**过程**

由 $f(0)=0$ 与 $f'(0)=0$，$\dfrac{f(x)}{x^2}$ 为 $\dfrac{0}{0}$ 型。洛必达一次：$\lim_{x\to 0}\dfrac{f'(x)}{2x}$。不假设 $f''$ 连续，直接由二阶导数定义（$f'(0)=0$）：$\lim_{x\to 0}\dfrac{f'(x)}{2x}=\dfrac{1}{2}\lim_{x\to 0}\dfrac{f'(x)-f'(0)}{x}=\dfrac{f''(0)}{2}$。

**答案原文**

$\dfrac{f''(0)}{2}$

## 308. test-calc-008

内容 SHA256：`04f548128137491387d64febec754f728e084c10d5b183972bed8a4d2c7293b8`。

来源：data/v2/test/dataset_test.jsonl，第 8 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $f(x)=\displaystyle\int_0^x(t^2-t)\,dt$ 的极值点与极值。

**过程**

$f'(x)=x^2-x=x(x-1)$，驻点 $x=0,1$。$f''(x)=2x-1$：$f''(0)=-1<0$，$x=0$ 为极大值点；$f''(1)=1>0$，$x=1$ 为极小值点。计算值：$f(x)=\displaystyle\int_0^x(t^2-t)dt=\dfrac{x^3}{3}-\dfrac{x^2}{2}$。$f(0)=0$（极大值），$f(1)=\dfrac{1}{3}-\dfrac{1}{2}=-\dfrac{1}{6}$（极小值）。

**答案原文**

极大值 $f(0)=0$；极小值 $f(1)=-\dfrac{1}{6}$

## 309. test-calc-009

内容 SHA256：`b985a64ece4cb4af78a6c03842bd27f21b317b4688881b6e74a4bf7beca981f4`。

来源：data/v2/test/dataset_test.jsonl，第 9 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求曲线 $x=t^2,\ y=t^3$（$0\le t\le 1$）的弧长。

**过程**

$\dfrac{dx}{dt}=2t$，$\dfrac{dy}{dt}=3t^2$。弧长 $L=\displaystyle\int_0^1\sqrt{(2t)^2+(3t^2)^2}\,dt=\int_0^1 t\sqrt{4+9t^2}\,dt$。令 $u=4+9t^2$（$du=18t\,dt$），$L=\dfrac{1}{18}\displaystyle\int_4^{13}\sqrt{u}\,du=\dfrac{1}{18}\cdot\dfrac{2}{3}\left[u^{3/2}\right]_4^{13}=\dfrac{1}{27}(13\sqrt{13}-8)$。

**答案原文**

$\dfrac{13\sqrt{13}-8}{27}$

## 310. test-calc-010

内容 SHA256：`b313eec75f9beb5164af55caf8ade3975f24079c11dc6b76b2b1b6d669cdc793`。

来源：data/v2/test/dataset_test.jsonl，第 10 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求心形线 $r=1+\cos\theta$ 所围图形的面积。

**过程**

极坐标面积 $S=\dfrac{1}{2}\displaystyle\int_0^{2\pi}r^2\,d\theta=\dfrac{1}{2}\int_0^{2\pi}(1+\cos\theta)^2d\theta=\dfrac{1}{2}\int_0^{2\pi}(1+2\cos\theta+\cos^2\theta)d\theta$。其中 $\int_0^{2\pi}\cos\theta\,d\theta=0$，$\int_0^{2\pi}\cos^2\theta\,d\theta=\pi$，故 $S=\dfrac{1}{2}(2\pi+0+\pi)=\dfrac{3\pi}{2}$。

**答案原文**

$\dfrac{3\pi}{2}$

## 311. test-calc-011

内容 SHA256：`cd7f47b6f74d9dfe8b8a2dda889ad0e958607d0b55d1fb60168aed2fde4726a1`。

来源：data/v2/test/dataset_test.jsonl，第 11 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求由 $y=x^2$ 与 $y=4$ 围成的区域绕 $y$ 轴旋转所得旋转体的体积。

**过程**

区域为 $-2\le x\le 2,\ x^2\le y\le 4$（关于 $y$ 轴对称）。绕 $y$ 轴旋转时左右两半生成同一个旋转体，只需取右半 $0\le x\le 2$。在 $x$ 处取高 $4-x^2$、厚 $dx$ 的竖直壳层，$dV=2\pi x(4-x^2)dx$。$V=\displaystyle\int_0^2 2\pi x(4-x^2)dx=2\pi\int_0^2(4x-x^3)dx=2\pi\left[2x^2-\dfrac{x^4}{4}\right]_0^2=2\pi(8-4)=8\pi$。

**答案原文**

$8\pi$

## 312. test-calc-012

内容 SHA256：`3f50dc95d68cb6b7ae8d518f07a6ff35a5c50e321519c7b6e8b1c7b5dde32a2e`。

来源：data/v2/test/dataset_test.jsonl，第 12 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

判断反常积分 $\displaystyle\int_1^{+\infty}\frac{dx}{x(1+x)}$ 的敛散性，若收敛求其值。

**过程**

$\dfrac{1}{x(1+x)}=\dfrac{1}{x}-\dfrac{1}{1+x}$。$\displaystyle\int_1^b\dfrac{dx}{x(1+x)}=\left[\ln x-\ln(1+x)\right]_1^b=\ln\dfrac{b}{1+b}-\ln\dfrac{1}{2}$。令 $b\to+\infty$：$\ln\dfrac{b}{1+b}\to\ln 1=0$，故积分 $=0-\ln\dfrac{1}{2}=\ln 2$，收敛。

**答案原文**

$\ln 2$

## 313. test-calc-013

内容 SHA256：`4114ef5e18fd1d7559b17b64e7a04d266ecbf64f72958313be1588fdd3a78e3c`。

来源：data/v2/test/dataset_test.jsonl，第 13 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n(n+2)}$ 的和。

**过程**

$\dfrac{1}{n(n+2)}=\dfrac{1}{2}\left(\dfrac{1}{n}-\dfrac{1}{n+2}\right)$。部分和 $S_n=\dfrac{1}{2}\displaystyle\sum_{k=1}^{n}\left(\dfrac{1}{k}-\dfrac{1}{k+2}\right)=\dfrac{1}{2}\left[\left(1+\dfrac{1}{2}+\dfrac{1}{3}+\cdots+\dfrac{1}{n}\right)-\left(\dfrac{1}{3}+\dfrac{1}{4}+\cdots+\dfrac{1}{n+2}\right)\right]=\dfrac{1}{2}\left(1+\dfrac{1}{2}-\dfrac{1}{n+1}-\dfrac{1}{n+2}\right)$。令 $n\to\infty$，$S=\dfrac{1}{2}\cdot\dfrac{3}{2}=\dfrac{3}{4}$。

**答案原文**

$\dfrac{3}{4}$

## 314. test-calc-014

内容 SHA256：`d3b878c9074c420fca72d6b3ac9f672e3ebd1ccecb7d9be0d52300b8c5605b8e`。

来源：data/v2/test/dataset_test.jsonl，第 14 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

验证幂级数 $y=\displaystyle\sum_{n=0}^{\infty}\frac{x^n}{n!}$ 满足微分方程 $y'=y$ 及初值 $y(0)=1$。

**过程**

该级数收敛半径为 $+\infty$（比值判别法：$\dfrac{1/(n+1)!}{1/n!}=\dfrac{1}{n+1}\to 0$），可逐项求导：$y'=\displaystyle\sum_{n=1}^{\infty}\dfrac{nx^{n-1}}{n!}=\sum_{n=1}^{\infty}\dfrac{x^{n-1}}{(n-1)!}=\sum_{m=0}^{\infty}\dfrac{x^m}{m!}=y$。且 $y(0)=\dfrac{1}{0!}+\displaystyle\sum_{n=1}^{\infty}\dfrac{0^n}{n!}=1+0=1$。由解的唯一性，$y=e^x$。

**答案原文**

$y'=y$、$y(0)=1$，故 $y=e^x$

## 315. test-calc-015

内容 SHA256：`fddbb8388402000fa4403387bf6576637a4f5642230bf9ebefeb89a4bc4796d8`。

来源：data/v2/test/dataset_test.jsonl，第 15 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

利用幂级数展开求 $\displaystyle\int_0^1\frac{\ln(1+x)}{x}\,dx$ 的精确值。

**过程**

$\ln(1+x)=\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}x^n}{n}$，除以 $x$ 得 $\dfrac{\ln(1+x)}{x}=\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}x^{n-1}}{n}$（$x\ne 0$），且该级数在 $[0,1]$ 上一致收敛：余项 $\left|\displaystyle\sum_{k>N}\dfrac{(-1)^{k-1}x^{k-1}}{k}\right|\le\dfrac{x^N}{N+1}\le\dfrac{1}{N+1}\to 0$（交错级数估计，对 $x\in[0,1]$ 一致）；被积函数在 $x=0$ 处连续延拓为 $1$（$\lim_{x\to 0}\dfrac{\ln(1+x)}{x}=1$）。故可逐项积分：$\displaystyle\int_0^1\dfrac{\ln(1+x)}{x}dx=\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}}{n}\int_0^1x^{n-1}dx=\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}}{n^2}$。由交错级数与 $\zeta(2)$ 的关系：$\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}}{n^2}=\eta(2)=\left(1-2^{1-2}\right)\zeta(2)=\dfrac{1}{2}\cdot\dfrac{\pi^2}{6}=\dfrac{\pi^2}{12}$（其中 $\zeta(2)=\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{n^2}=\dfrac{\pi^2}{6}$ 为已知结果，可由 test-calc-023 的 Parseval 等式得到）。

**答案原文**

$\dfrac{\pi^2}{12}$

## 316. test-calc-016

内容 SHA256：`fe6dcfc1168f13c33a4bd613977eef12b0f540c25eb013a5362e7645b7ac8b0f`。

来源：data/v2/test/dataset_test.jsonl，第 16 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

由方程 $x^2+y^2+xy=3$ 确定隐函数 $y=y(x)$。求 $y'(1)$ 与 $y''(1)$（已知 $(1,1)$ 满足方程）。

**过程**

两边对 $x$ 求导：$2x+2yy'+y+xy'=0$。代入 $(1,1)$：$2+2y'(1)+1+y'(1)=0$，即 $3y'(1)=-3$，$y'(1)=-1$。再对 $x$ 求导：$2+2(y')^2+2yy''+y'+y'+xy''=0$，即 $2+2(y')^2+2yy''+2y'+xy''=0$。代入 $(1,1)$ 与 $y'=-1$：$2+2\cdot 1+2y''-2+y''=0$，即 $3y''=-2$，$y''(1)=-\dfrac{2}{3}$。

**答案原文**

$y'(1)=-1$；$y''(1)=-\dfrac{2}{3}$

## 317. test-calc-017

内容 SHA256：`416c1bcaa826b751063f377f9c49bceaaab79ed24155d8231a8d7da7a91d3fa3`。

来源：data/v2/test/dataset_test.jsonl，第 17 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $f(x,y)=x^2+y^2-xy+x+y$ 的极值点与极值。

**过程**

驻点条件：$f_x=2x-y+1=0$，$f_y=2y-x+1=0$。两式相加得 $x+y+2=0$；两式相减得 $3x-3y=0$，即 $x=y$。代入 $x+y+2=0$：$2x=-2$，$x=y=-1$。驻点 $(-1,-1)$。Hessian $H=\begin{pmatrix}2&-1\\-1&2\end{pmatrix}$，顺序主子式 $2>0$、$\det H=3>0$，正定，故 $(-1,-1)$ 为极小值点。$f(-1,-1)=1+1-1-1-1=-1$。

**答案原文**

极小值 $f(-1,-1)=-1$

## 318. test-calc-018

内容 SHA256：`53b02f679daa29643bbb54fdea8bf9b213bea8d068842bfb9145b851296dc539`。

来源：data/v2/test/dataset_test.jsonl，第 18 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $f(x,y)=xy$ 在约束 $x+y=4$ 下的最大值。

**过程**

拉格朗日函数 $L=xy+\lambda(x+y-4)$。$L_x=y+\lambda=0$，$L_y=x+\lambda=0$，故 $x=y=-\lambda$。代入约束 $2x=4$，$x=y=2$，$\lambda=-2$。$f(2,2)=4$。验证（消元法）：$y=4-x$，$f=x(4-x)=4x-x^2=-(x-2)^2+4\le 4$，等号在 $x=2$ 取得，最大值 $4$。

**答案原文**

最大值 $4$（在 $(2,2)$ 处取得）

## 319. test-calc-019

内容 SHA256：`36e90811db3b7adc5b05303ead2a0c893514380ead81a00b9eef639169a181b6`。

来源：data/v2/test/dataset_test.jsonl，第 19 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $\displaystyle I=\int_0^1\!\!\int_y^1\frac{x}{1+x^2}\,dx\,dy$。

**过程**

区域 $D=\{(x,y):0\le y\le 1,\ y\le x\le 1\}=\{(x,y):0\le x\le 1,\ 0\le y\le x\}$。交换次序：$I=\displaystyle\int_0^1\!\!\int_0^x\frac{x}{1+x^2}\,dy\,dx=\int_0^1\frac{x^2}{1+x^2}\,dx=\int_0^1\left(1-\frac{1}{1+x^2}\right)dx=\left[x-\arctan x\right]_0^1=1-\dfrac{\pi}{4}$。

**答案原文**

$1-\dfrac{\pi}{4}$

## 320. test-calc-020

内容 SHA256：`352c64254a5d716791cddb59c534dc1309abd9c5e69280bc371e0f00bc4c1830`。

来源：data/v2/test/dataset_test.jsonl，第 20 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

用格林公式（或曲线积分）求椭圆 $\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1$（$a,b>0$）的面积。

**过程**

参数化 $x=a\cos t$、$y=b\sin t$（$t:0\to 2\pi$）。由格林公式，面积 $S=\dfrac{1}{2}\displaystyle\oint(x\,dy-y\,dx)=\dfrac{1}{2}\int_0^{2\pi}\left[a\cos t\cdot b\cos t-b\sin t\cdot(-a\sin t)\right]dt=\dfrac{1}{2}\int_0^{2\pi}ab(\cos^2t+\sin^2t)dt=\dfrac{1}{2}ab\cdot 2\pi=\pi ab$。

**答案原文**

$\pi ab$

## 321. test-calc-021

内容 SHA256：`7c20f362c4f2ff75160e37a8339144fd4867063d1b2be0136526216fc8750411`。

来源：data/v2/test/dataset_test.jsonl，第 21 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求曲线积分 $\displaystyle\int_L(2xy\,dx+x^2\,dy)$，其中 $L$ 为从 $(0,0)$ 到 $(1,1)$ 的任意光滑曲线段，并说明结果与路径无关的原因。

**过程**

$d(x^2y)=2xy\,dx+x^2\,dy$，故被积表达式是全微分，势函数 $\varphi(x,y)=x^2y$。由微积分基本定理，$\displaystyle\int_L d\varphi=\varphi(1,1)-\varphi(0,0)=1-0=1$，与路径无关（本题已直接构造出 $\mathbb R^2$ 上的全局势函数，故无需再讨论充要条件；一般结论"$\dfrac{\partial P}{\partial y}=\dfrac{\partial Q}{\partial x}$ 等价于积分与路径无关"只在单连通区域上对 $C^1$ 向量场成立）。

**答案原文**

$1$

## 322. test-calc-022

内容 SHA256：`0b0cd2cea34985ee02dd891a1757cfc05098d3cb617de6d2ecd798d922e14aae`。

来源：data/v2/test/dataset_test.jsonl，第 22 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

用高斯公式求 $\displaystyle\iint_S\vec F\cdot\vec n\,dS$，其中 $\vec F=(x,y,z)$，$S$ 为单位球面 $x^2+y^2+z^2=1$（外侧），$\vec n$ 为单位外法向量。

**过程**

$\operatorname{div}\vec F=\dfrac{\partial x}{\partial x}+\dfrac{\partial y}{\partial y}+\dfrac{\partial z}{\partial z}=3$。由高斯公式，$\displaystyle\iint_S\vec F\cdot\vec n\,dS=\iiint_B\operatorname{div}\vec F\,dV=3\iiint_B dV=3\cdot\dfrac{4\pi}{3}=4\pi$（$B$ 为单位球体，体积 $\dfrac{4\pi}{3}$）。

**答案原文**

$4\pi$

## 323. test-calc-023

内容 SHA256：`2beeaf80c49cbb61fd8a73839ee208056424a27091551abdfd0b9bd23690999e`。

来源：data/v2/test/dataset_test.jsonl，第 23 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

已知 $f(x)=x$（$-\pi\le x\le\pi$）的傅里叶级数为 $2\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n+1}}{n}\sin nx$。利用 Parseval 等式求 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^2}$。

**过程**

Parseval 等式：$\dfrac{1}{\pi}\displaystyle\int_{-\pi}^{\pi}f(x)^2dx=\sum_{n=1}^{\infty}b_n^2$（奇函数情形，$a_n=0$），其中 $b_n=\dfrac{2(-1)^{n+1}}{n}$。左端 $\dfrac{1}{\pi}\displaystyle\int_{-\pi}^{\pi}x^2dx=\dfrac{1}{\pi}\cdot\dfrac{2\pi^3}{3}=\dfrac{2\pi^2}{3}$。右端 $\displaystyle\sum_{n=1}^{\infty}\dfrac{4}{n^2}=4\sum_{n=1}^{\infty}\dfrac{1}{n^2}$。故 $4\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{n^2}=\dfrac{2\pi^2}{3}$，$\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{n^2}=\dfrac{\pi^2}{6}$。

**答案原文**

$\dfrac{\pi^2}{6}$

## 324. test-calc-024

内容 SHA256：`4aca9ef7908b9d9eb0bbcc4ca97bd553c87667151cd79886f9ab7c674f67426c`。

来源：data/v2/test/dataset_test.jsonl，第 24 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $\displaystyle\lim_{n\to\infty}\frac{\sqrt[n]{n!}}{n}$。

**过程**

记 $S_n=\dfrac{1}{n}\displaystyle\sum_{k=1}^{n}\ln\dfrac{k}{n}$，其中 $\dfrac{k}{n}$ 是小区间 $\left[\dfrac{k-1}{n},\dfrac{k}{n}\right]$ 的右端点。因 $\ln x$ 单调递增，在每个小区间上 $\ln x\le\ln\dfrac{k}{n}$，故 $\displaystyle\int_0^1\ln x\,dx=\sum_{k=1}^{n}\int_{(k-1)/n}^{k/n}\ln x\,dx\le S_n$；又对 $k\le n-1$，在 $\left[\dfrac{k}{n},\dfrac{k+1}{n}\right]$ 上 $\ln x\ge\ln\dfrac{k}{n}$，故 $S_n\le\displaystyle\sum_{k=1}^{n-1}\int_{k/n}^{(k+1)/n}\ln x\,dx+\dfrac{1}{n}\ln 1=\int_{1/n}^1\ln x\,dx$。于是 $-1=\displaystyle\int_0^1\ln x\,dx\le S_n\le\int_{1/n}^1\ln x\,dx=\left[x\ln x-x\right]_{1/n}^1=-1+\dfrac{\ln n+1}{n}$（其中 $\lim_{x\to 0^+}x\ln x=0$ 保证左端积分为 $-1$）。两端都趋于 $-1$，由夹逼准则 $S_n\to-1$。故原极限 $=\lim e^{S_n}=e^{-1}=\dfrac{1}{e}$。

**答案原文**

$\dfrac{1}{e}$

## 325. test-calc-025

内容 SHA256：`c82090464197ef7a633f743ed4505cfc8a6bac8614b68f5842cc70a9a2dbd514`。

来源：data/v2/test/dataset_test.jsonl，第 25 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $a_1=1$，$a_{n+1}=1+\dfrac{a_n}{1+a_n}$。证明 $\{a_n\}$ 收敛并求其极限。

**过程**

记 $\varphi=\dfrac{1+\sqrt5}{2}$（满足 $\varphi^2=\varphi+1$）。先证 $1\le a_n<\varphi$：$a_1=1<\varphi$；若 $a_n<\varphi$，则 $a_{n+1}=1+\dfrac{a_n}{1+a_n}<1+\dfrac{\varphi}{1+\varphi}$。由 $\varphi^2=\varphi+1$ 得 $\dfrac{\varphi}{1+\varphi}=\dfrac{1}{\varphi}$，故 $a_{n+1}<1+\dfrac{1}{\varphi}=\varphi$（$1+\dfrac{1}{\varphi}=\dfrac{\varphi+1}{\varphi}=\dfrac{\varphi^2}{\varphi}=\varphi$）。再证单调递增：$a_{n+1}-a_n=1-\dfrac{a_n^2}{1+a_n}=\dfrac{1+a_n-a_n^2}{1+a_n}>0$（因 $a_n<\varphi$ 时 $a_n^2<1+a_n$）。故 $\{a_n\}$ 单调递增有上界，收敛。设极限为 $L$，对递推式取极限：$L=1+\dfrac{L}{1+L}$，即 $L^2=L+1$，正根 $L=\varphi=\dfrac{1+\sqrt5}{2}$。

**答案原文**

极限为 $\dfrac{1+\sqrt5}{2}$

## 326. test-calc-026

内容 SHA256：`ddafea439efeb641053d5585dd94bc428d383fbc0a6af983124b436a6240ac1e`。

来源：data/v2/test/dataset_test.jsonl，第 26 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $\displaystyle\lim_{x\to 0}\frac{\displaystyle\int_0^x\sin(t^2)\,dt}{x^3}$。

**过程**

$\dfrac{0}{0}$ 型。分子求导得 $\sin(x^2)$，分母求导得 $3x^2$。原式 $=\lim_{x\to 0}\dfrac{\sin(x^2)}{3x^2}$。令 $u=x^2\to 0$，$\dfrac{\sin u}{u}\to 1$，故原式 $=\dfrac{1}{3}$。

**答案原文**

$\dfrac{1}{3}$

## 327. test-calc-027

内容 SHA256：`d76b743b04693214d20dc5f8daf4b6fb651dc06e7ca56d0aa40cbcb7a4e12f7b`。

来源：data/v2/test/dataset_test.jsonl，第 27 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

证明方程 $e^x=2x+1$ 恰有两个实根，并给出两个根所在的区间。

**过程**

令 $f(x)=e^x-2x-1$。$f(0)=1-0-1=0$，故 $x=0$ 是一个根。$f'(x)=e^x-2$，$f'=0$ 当 $x=\ln 2$。$f(\ln 2)=2-2\ln 2-1=1-2\ln 2<0$（$\ln 2\approx 0.693$）。$f(2)=e^2-5>0$，$f(-\infty)=+\infty$ 且 $f(-2)=e^{-2}+4-1>0$。在 $(-\infty,\ln 2]$ 上 $f$ 严格递减（$f'<0$），且 $f(-2)>0$、$f(\ln 2)<0$，由零点定理存在唯一根 $\xi_1\in(-2,\ln 2)$（即 $x=0$，因 $f(0)=0$ 且该区间上单调故唯一）；在 $[\ln 2,+\infty)$ 上 $f$ 严格递增，$f(\ln 2)<0$、$f(2)>0$，存在唯一根 $\xi_2\in(\ln 2,2)$。故恰有两个实根：$x=0$ 与 $\xi_2\in(\ln 2,2)$。

**答案原文**

恰有两个实根：$x=0$ 与 $\xi_2\in(\ln 2,2)$

## 328. test-calc-028

内容 SHA256：`96c6272ac589f8d0d7f0cadaa87dff3e2a5de78048a56ef6e0f2f4c61697f3f2`。

来源：data/v2/test/dataset_test.jsonl，第 28 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $\displaystyle\int_{-1}^{1}x^3\sqrt{1-x^2}\,dx$。

**过程**

被积函数 $f(x)=x^3\sqrt{1-x^2}$ 满足 $f(-x)=(-x)^3\sqrt{1-(-x)^2}=-x^3\sqrt{1-x^2}=-f(x)$，为奇函数，积分区间关于原点对称，故 $\displaystyle\int_{-1}^{1}f(x)dx=0$。

**答案原文**

$0$

## 329. test-calc-029

内容 SHA256：`026dde16d85fe462f2ba455841c0294ae104f53359cade0c48b4893ea6ee12d7`。

来源：data/v2/test/dataset_test.jsonl，第 29 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

判断 $\displaystyle\int_1^{+\infty}\frac{\ln x}{x^2}\,dx$ 的敛散性，若收敛求其值。

**过程**

分部积分（$u=\ln x$、$dv=x^{-2}dx$）：$\displaystyle\int\dfrac{\ln x}{x^2}dx=-\dfrac{\ln x}{x}+\int\dfrac{dx}{x^2}=-\dfrac{\ln x}{x}-\dfrac{1}{x}+C$。$\displaystyle\int_1^b=-\left[\dfrac{\ln x}{x}+\dfrac{1}{x}\right]_1^b=1-\dfrac{\ln b}{b}-\dfrac{1}{b}$。令 $b\to+\infty$：$\dfrac{\ln b}{b}\to 0$、$\dfrac{1}{b}\to 0$，故积分为 $1$，收敛。

**答案原文**

$1$

## 330. test-calc-030

内容 SHA256：`6b30035d2f3dadfdf3690f6714eb13e0ae8d4f871ffc5a9dd7fbea1b668696eb`。

来源：data/v2/test/dataset_test.jsonl，第 30 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $\displaystyle\lim_{n\to\infty}\int_0^1\frac{x^n}{1+x}\,dx$。

**过程**

当 $0\le x\le 1$ 时 $0\le\dfrac{x^n}{1+x}\le x^n$（因 $1+x\ge 1$），故 $0\le\displaystyle\int_0^1\dfrac{x^n}{1+x}dx\le\int_0^1x^ndx=\dfrac{1}{n+1}$。由夹逼准则，极限为 $0$。

**答案原文**

$0$

## 331. test-calc-031

内容 SHA256：`718485c7f43348e20c14049e7e81bdf54698c33932cd8046211d357c352eb233`。

来源：data/v2/test/dataset_test.jsonl，第 31 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

物体从高度 $20$ 米处自由下落，高度函数 $h(t)=20-5t^2$（米，$t$ 为秒）。求速度与加速度函数，及物体落地时刻与落地速度。

**过程**

$v(t)=h'(t)=-10t$（米/秒），$a(t)=v'(t)=-10$（米/秒²，向下）。落地：$h(t)=0$，即 $20-5t^2=0$，$t=2$（秒，舍负根）。落地速度 $v(2)=-20$（米/秒，向下，大小为 $20$）。

**答案原文**

$v=-10t$；$a=-10$；$t=2$ 秒落地，落地速度大小 $20$ 米/秒

## 332. test-calc-032

内容 SHA256：`391f72aa3620728c0dc43aeb6c942732429284701271dfc2ed82722a2767d947`。

来源：data/v2/test/dataset_test.jsonl，第 32 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求曲线 $y=x^2$ 在原点处的曲率，以及曲线 $y=\ln x$ 在 $(1,0)$ 处的曲率。

**过程**

曲率公式 $\kappa=\dfrac{|y''|}{(1+y'^2)^{3/2}}$。对 $y=x^2$：$y'=2x$，$y''=2$，在 $(0,0)$：$\kappa=\dfrac{2}{(1+0)^{3/2}}=2$。对 $y=\ln x$：$y'=\dfrac{1}{x}$，$y''=-\dfrac{1}{x^2}$，在 $(1,0)$：$\kappa=\dfrac{1}{(1+1)^{3/2}}=\dfrac{1}{2\sqrt2}$。

**答案原文**

$y=x^2$ 在原点处 $\kappa=2$；$y=\ln x$ 在 $(1,0)$ 处 $\kappa=\dfrac{1}{2\sqrt2}$

## 333. test-calc-033

内容 SHA256：`09f3c8f4ae8e0b30c7d71a0b5253388eee0b00cd9a85bf90bc8114294081b9b8`。

来源：data/v2/test/dataset_test.jsonl，第 33 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

证明：当 $x\ge 0$ 时，$e^x\ge 1+x+\dfrac{x^2}{2}$。

**过程**

令 $f(x)=e^x-1-x-\dfrac{x^2}{2}$。$f'(x)=e^x-1-x$。由 $e^x>1+x$（$x>0$，eval-calc-008）得 $f'(x)>0$（$x>0$），故 $f$ 在 $[0,+\infty)$ 上严格递增。又 $f(0)=1-1-0-0=0$，故 $x\ge 0$ 时 $f(x)\ge 0$，即 $e^x\ge 1+x+\dfrac{x^2}{2}$。亦可由泰勒公式带拉格朗日余项 $e^x=1+x+\dfrac{x^2}{2}+\dfrac{x^3}{6}e^\xi\ge 1+x+\dfrac{x^2}{2}$（$\xi\ge 0$）直接得证。

**答案原文**

证毕（两种证法）

## 334. test-calc-034

内容 SHA256：`27e67794e8ed31b9b14931f6b95951cca8579b9da065511ceb4ce0c70eafb222`。

来源：data/v2/test/dataset_test.jsonl，第 34 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

判断级数 $\displaystyle\sum_{n=1}^{\infty}\frac{n!}{n^n}$ 的敛散性。

**过程**

比值：$\dfrac{a_{n+1}}{a_n}=\dfrac{(n+1)!}{(n+1)^{n+1}}\cdot\dfrac{n^n}{n!}=\dfrac{n^n}{(n+1)^n}=\left(\dfrac{n}{n+1}\right)^n=\dfrac{1}{\left(1+\frac{1}{n}\right)^n}\to\dfrac{1}{e}<1$。由比值判别法，级数收敛。

**答案原文**

收敛

## 335. test-calc-035

内容 SHA256：`5e1ef1bba359610c5cecd6b73ca2064a30375f2d371a071237f6f22860480a3b`。

来源：data/v2/test/dataset_test.jsonl，第 35 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求幂级数 $\displaystyle\sum_{n=0}^{\infty}\frac{x^n}{n!}$ 与 $\displaystyle\sum_{n=0}^{\infty}n!\,x^n$ 的收敛半径，并对比说明。

**过程**

用系数比值 $\left|\dfrac{a_{n+1}}{a_n}\right|$（$a_n$ 为幂级数系数，不含 $x$）。对 $\sum\dfrac{x^n}{n!}$：$a_n=\dfrac{1}{n!}$，$\left|\dfrac{a_{n+1}}{a_n}\right|=\dfrac{1}{n+1}\to 0$，收敛半径 $R=\dfrac{1}{0}=+\infty$。对 $\sum n!\,x^n$：$a_n=n!$，$\left|\dfrac{a_{n+1}}{a_n}\right|=n+1\to+\infty$，$R=0$；且 $x\ne 0$ 时通项 $n!x^n\not\to 0$，级数发散，与 $R=0$ 一致。

**答案原文**

$R=+\infty$ 与 $R=0$

## 336. test-calc-036

内容 SHA256：`a782f3aad2cb7fbdc1305cb4fe8d70b38210e9f2d7026f166d633531a3202773`。

来源：data/v2/test/dataset_test.jsonl，第 36 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $u=f(r)$，其中 $r=\sqrt{x^2+y^2}$（$(x,y)\ne(0,0)$），$f$ 二阶可导。证明在 $\mathbb R^2\setminus\{(0,0)\}$ 上 $u_{xx}+u_{yy}=f''(r)+\dfrac{f'(r)}{r}$，并验证 $u=\ln r$ 满足 $u_{xx}+u_{yy}=0$。

**过程**

$r_x=\dfrac{x}{r}$，$r_y=\dfrac{y}{r}$。$u_x=f'(r)\dfrac{x}{r}$，$u_{xx}=f''(r)\dfrac{x^2}{r^2}+f'(r)\left(\dfrac{1}{r}-\dfrac{x^2}{r^3}\right)$。同理 $u_{yy}=f''(r)\dfrac{y^2}{r^2}+f'(r)\left(\dfrac{1}{r}-\dfrac{y^2}{r^3}\right)$。相加：$u_{xx}+u_{yy}=f''(r)\dfrac{x^2+y^2}{r^2}+f'(r)\left(\dfrac{2}{r}-\dfrac{x^2+y^2}{r^3}\right)=f''(r)+f'(r)\left(\dfrac{2}{r}-\dfrac{1}{r}\right)=f''(r)+\dfrac{f'(r)}{r}$。取 $f(r)=\ln r$：$f'(r)=\dfrac{1}{r}$，$f''(r)=-\dfrac{1}{r^2}$，代入得 $u_{xx}+u_{yy}=-\dfrac{1}{r^2}+\dfrac{1}{r^2}=0$，即 $\ln r$ 在去掉原点的平面上调和。

**答案原文**

证毕（在 $\mathbb R^2\setminus\{(0,0)\}$ 上）；$u=\ln r$ 在 $\mathbb R^2\setminus\{(0,0)\}$ 上满足 $u_{xx}+u_{yy}=0$

## 337. test-calc-037

内容 SHA256：`91709c84da9b9a2b42e2d438b0fd5ea8f855b6088a256a7464fc1c9d6c314b1d`。

来源：data/v2/test/dataset_test.jsonl，第 37 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

由笛卡尔叶形线方程 $x^3+y^3-3xy=0$ 确定隐函数。求曲线在点 $\left(\dfrac{3}{2},\dfrac{3}{2}\right)$ 处的切线斜率。

**过程**

两边对 $x$ 求导：$3x^2+3y^2y'-3y-3xy'=0$，即 $(y^2-x)y'=y-x^2$，$y'=\dfrac{y-x^2}{y^2-x}$。在 $\left(\dfrac{3}{2},\dfrac{3}{2}\right)$ 处：$y'=\dfrac{\frac{3}{2}-\frac{9}{4}}{\frac{9}{4}-\frac{3}{2}}=\dfrac{-\frac{3}{4}}{\frac{3}{4}}=-1$。

**答案原文**

$-1$

## 338. test-calc-038

内容 SHA256：`7507b49b61600d7814f65e857ff682247885e5d845e57a5e2beecfe764c17081`。

来源：data/v2/test/dataset_test.jsonl，第 38 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

证明 $\displaystyle\int_0^1 e^{x^2}\,dx\ge e^{1/3}$。

**过程**

$e^t$ 是凸函数。区间 $[0,1]$ 上取均匀"概率测度"，由积分型 Jensen 不等式：$\displaystyle\int_0^1 e^{x^2}dx\ge e^{\int_0^1 x^2dx}=e^{1/3}$（凸函数在"平均点"的取值不大于函数值的平均）。其中 $\displaystyle\int_0^1x^2dx=\dfrac{1}{3}$。

**答案原文**

证毕

## 339. test-calc-039

内容 SHA256：`b17d48293925de02a80b682ef0d2ca797f503ef06f4edf6df3502a36f563d9c1`。

来源：data/v2/test/dataset_test.jsonl，第 39 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

牛顿冷却模型：物体温度 $T(t)$ 满足 $T'=-k(T-20)$（环境温度 $20^\circ$C）。已知 $T(0)=100$、$T(5)=60$，求 $T(10)$。

**过程**

解方程：$\dfrac{dT}{T-20}=-k\,dt$，积分得 $\ln(T-20)=-kt+C$，$T=20+Ce^{-kt}$。由 $T(0)=100$：$C=80$，$T=20+80e^{-kt}$。由 $T(5)=60$：$60=20+80e^{-5k}$，$e^{-5k}=\dfrac{1}{2}$。故 $T(10)=20+80e^{-10k}=20+80(e^{-5k})^2=20+80\cdot\dfrac{1}{4}=40$。

**答案原文**

$T(10)=40^\circ$C

## 340. test-calc-040

内容 SHA256：`fb0477078aaa61b7bd63490ddb6194ba998fa83557c22db19b433de8cb4cced3`。

来源：data/v2/test/dataset_test.jsonl，第 40 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $\displaystyle\lim_{x\to 0}\frac{1-\cos x-\frac{x^2}{2}}{x^4}$。

**过程**

$\cos x=1-\dfrac{x^2}{2}+\dfrac{x^4}{24}-\dfrac{x^6}{720}+\cdots$。故 $1-\cos x-\dfrac{x^2}{2}=-\dfrac{x^4}{24}+o(x^4)$。原式 $=\lim_{x\to 0}\dfrac{-x^4/24+o(x^4)}{x^4}=-\dfrac{1}{24}$。

**答案原文**

$-\dfrac{1}{24}$

## 341. test-calc-041

内容 SHA256：`6f06cef6bd09114eea6cbe682bc8930093b92b3fccc14f202706db0b400be10c`。

来源：data/v2/test/dataset_test.jsonl，第 41 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $\displaystyle\int_0^{\pi}\sin^2x\,dx$ 与 $\displaystyle\int_0^{\pi}\cos^2x\,dx$，并说明两者相等的几何原因。

**过程**

$\displaystyle\int_0^{\pi}\sin^2x\,dx=\int_0^{\pi}\dfrac{1-\cos 2x}{2}dx=\left[\dfrac{x}{2}-\dfrac{\sin 2x}{4}\right]_0^{\pi}=\dfrac{\pi}{2}$。$\displaystyle\int_0^{\pi}\cos^2x\,dx=\int_0^{\pi}\dfrac{1+\cos 2x}{2}dx=\left[\dfrac{x}{2}+\dfrac{\sin 2x}{4}\right]_0^{\pi}=\dfrac{\pi}{2}$。几何原因：$\cos^2x=\sin^2\left(x+\dfrac{\pi}{2}\right)$，故 $\displaystyle\int_0^{\pi}\cos^2x\,dx=\int_0^{\pi}\sin^2\left(x+\dfrac{\pi}{2}\right)dx=\int_{\pi/2}^{3\pi/2}\sin^2u\,du$（换元 $u=x+\dfrac{\pi}{2}$）$=\displaystyle\int_0^{\pi}\sin^2u\,du$（$\sin^2$ 以 $\pi$ 为周期）。

**答案原文**

均为 $\dfrac{\pi}{2}$

## 342. test-calc-042

内容 SHA256：`e0a185708cee8cb8d0f255a8ba92c5450e1476782b7dcbe5029b7af429d18fd4`。

来源：data/v2/test/dataset_test.jsonl，第 42 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

证明 $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^{n-1}}{n}=\ln 2$。

**过程**

由 test-calc-006，$\ln(1+x)=\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}x^n}{n}$ 对 $|x|<1$ 成立。$x=1$ 处级数 $\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}}{n}$ 为交错级数（$a_n=\dfrac{1}{n}\searrow 0$），由莱布尼茨判别法收敛。由 Abel 定理，幂级数的和函数在收敛点左连续，故 $\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}}{n}=\lim_{x\to 1^-}\ln(1+x)=\ln 2$。另一证法（积分表示）：$\dfrac{1}{n}=\displaystyle\int_0^1x^{n-1}dx$，故 $\displaystyle\sum_{n=1}^{N}\dfrac{(-1)^{n-1}}{n}=\int_0^1\sum_{n=1}^{N}(-x)^{n-1}dx=\int_0^1\dfrac{1-(-x)^N}{1+x}dx\to\int_0^1\dfrac{dx}{1+x}=\ln 2$。

**答案原文**

证毕（两种证法）

## 343. test-calc-043

内容 SHA256：`9fd34f21639399b41a82152e8818a265bd68a63ac1532a4ad21cb69d304668a4`。

来源：data/v2/test/dataset_test.jsonl，第 43 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $\displaystyle\int_0^{+\infty}e^{-x^2}\,dx$（高斯积分）。

**过程**

记 $I=\displaystyle\int_0^{+\infty}e^{-x^2}dx$。$I^2=\displaystyle\int_0^{\infty}e^{-x^2}dx\int_0^{\infty}e^{-y^2}dy=\iint_{[0,\infty)^2}e^{-(x^2+y^2)}dx\,dy$。用极坐标（第一象限）：$I^2=\displaystyle\int_0^{\pi/2}\!\!\int_0^{\infty}e^{-r^2}r\,dr\,d\theta=\int_0^{\pi/2}\left[-\dfrac{e^{-r^2}}{2}\right]_0^{\infty}d\theta=\int_0^{\pi/2}\dfrac{1}{2}\,d\theta=\dfrac{\pi}{4}$。故 $I=\dfrac{\sqrt\pi}{2}$（$I>0$）。严格化：先对有限正方形/四分之一圆取极限，用夹逼说明无穷区域上的积分等于逐次积分。

**答案原文**

$\dfrac{\sqrt\pi}{2}$

## 344. test-calc-044

内容 SHA256：`063588880cc36193ba622de5d01bdbe8fecda190c80d3a04808559add4cf0953`。

来源：data/v2/test/dataset_test.jsonl，第 44 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

用参数方程 $x=a\cos t,\ y=b\sin t$（$0\le t\le 2\pi$，$a,b>0$）求椭圆所围面积。

**过程**

$S=\left|\displaystyle\int_0^{2\pi}y\,dx\right|=\left|\int_0^{2\pi}b\sin t\cdot(-a\sin t)dt\right|=ab\displaystyle\int_0^{2\pi}\sin^2t\,dt=ab\cdot\pi=\pi ab$（$\int_0^{2\pi}\sin^2t\,dt=\pi$，与 test-calc-041 同法）。

**答案原文**

$\pi ab$

## 345. test-calc-045

内容 SHA256：`5d1bdbef08635307b135adbca7a689b43d29403019f6b8543357d1d1d1f8b7f2`。

来源：data/v2/test/dataset_test.jsonl，第 45 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $\displaystyle\lim_{x\to+\infty}x^2\left(2^{1/x}-2^{1/(x+1)}\right)$。

**过程**

对 $f(t)=2^t$ 在 $\left[\dfrac{1}{x+1},\dfrac{1}{x}\right]$ 上用拉格朗日中值定理：$2^{1/x}-2^{1/(x+1)}=f'(\xi)\left(\dfrac{1}{x}-\dfrac{1}{x+1}\right)=2^\xi\ln 2\cdot\dfrac{1}{x(x+1)}$，其中 $\dfrac{1}{x+1}<\xi<\dfrac{1}{x}$。故原式 $=\lim_{x\to\infty}x^2\cdot 2^\xi\ln 2\cdot\dfrac{1}{x(x+1)}=\lim_{x\to\infty}\dfrac{x^2}{x(x+1)}\cdot 2^\xi\ln 2$。当 $x\to+\infty$ 时 $\xi\to 0^+$，$2^\xi\to 1$，$\dfrac{x^2}{x(x+1)}\to 1$，故极限为 $\ln 2$。

**答案原文**

$\ln 2$

## 346. test-geom-001

内容 SHA256：`13d8da6f0157fe979d5e24ab163022f5911adf158dc57d50878dda974b5ddb42`。

来源：data/v2/test/dataset_test.jsonl，第 46 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求两直线 $l_1:\begin{cases}x=1+t\\y=2-t\\z=t\end{cases}$ 与 $l_2:\begin{cases}x=2+s\\y=1+2s\\z=1+s\end{cases}$ 的交点，并求过两直线的平面方程。

**过程**

求交点：$\begin{cases}1+t=2+s\\2-t=1+2s\\t=1+s\end{cases}$。由第三式 $t=1+s$，代入第一式：$1+1+s=2+s$ 恒等；代入第二式：$2-(1+s)=1+2s$，即 $1-s=1+2s$，$s=0$，$t=1$。交点为 $(2,1,1)$。两直线方向：$\vec{s_1}=(1,-1,1)$，$\vec{s_2}=(1,2,1)$。过两直线的平面法向量 $\vec n=\vec{s_1}\times\vec{s_2}=((-1)\cdot 1-1\cdot 2,\ 1\cdot 1-1\cdot 1,\ 1\cdot 2-(-1)\cdot 1)=(-3,0,3)$，取 $(1,0,-1)$。平面方程：$(x-2)-(z-1)=0$，即 $x-z=1$。

**答案原文**

交点 $(2,1,1)$；平面 $x-z=1$

## 347. test-geom-002

内容 SHA256：`1e5c030427c3f378e816ddd491c6b1a0684bca1d20c480142ab305a67c8fc447`。

来源：data/v2/test/dataset_test.jsonl，第 47 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求点 $P(1,2,3)$ 到直线 $l:x=1+t,\ y=1+2t,\ z=1+3t$ 的距离与垂足坐标。

**过程**

直线上取点 $P_0(1,1,1)$、方向 $\vec s=(1,2,3)$。$\overrightarrow{P_0P}=(0,1,2)$。叉积 $\overrightarrow{P_0P}\times\vec s=(1\cdot 3-2\cdot 2,\ 2\cdot 1-0\cdot 3,\ 0\cdot 2-1\cdot 1)=(-1,2,-1)$，模 $\sqrt{6}$；$|\vec s|=\sqrt{14}$。距离 $d=\dfrac{\sqrt6}{\sqrt{14}}=\sqrt{\dfrac{3}{7}}$。垂足参数 $t^*=\dfrac{\overrightarrow{P_0P}\cdot\vec s}{|\vec s|^2}=\dfrac{0+2+6}{14}=\dfrac{4}{7}$，垂足 $Q=\left(1+\dfrac{4}{7},1+\dfrac{8}{7},1+\dfrac{12}{7}\right)=\left(\dfrac{11}{7},\dfrac{15}{7},\dfrac{19}{7}\right)$。

**答案原文**

距离 $\sqrt{\dfrac{3}{7}}$；垂足 $\left(\dfrac{11}{7},\dfrac{15}{7},\dfrac{19}{7}\right)$

## 348. test-geom-003

内容 SHA256：`62926f95e7c386d17a36cbf31a08dda3cb5d279117bf4c3f77fea4f4a71418fe`。

来源：data/v2/test/dataset_test.jsonl，第 48 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求异面直线 $l_1:\begin{cases}x=1+t\\y=2t\\z=3+t\end{cases}$ 与 $l_2:\begin{cases}x=2s\\y=1-s\\z=2s\end{cases}$ 之间的距离。

**过程**

$\vec{s_1}=(1,2,1)$，$\vec{s_2}=(2,-1,2)$，取点 $P_1=(1,0,3)\in l_1$、$P_2=(0,1,0)\in l_2$。公垂线方向 $\vec n=\vec{s_1}\times\vec{s_2}=(2\cdot 2-1\cdot(-1),\ 1\cdot 2-1\cdot 2,\ 1\cdot(-1)-2\cdot 2)=(5,0,-5)$，取 $(1,0,-1)$。$\overrightarrow{P_1P_2}=(-1,1,-3)$。距离 $d=\dfrac{|\overrightarrow{P_1P_2}\cdot\vec n|}{|\vec n|}=\dfrac{|-1-0+3|}{\sqrt2}=\dfrac{2}{\sqrt2}=\sqrt2$。

**答案原文**

$\sqrt2$

## 349. test-geom-004

内容 SHA256：`b9a3fff6e6c1594c57aad49618210127a1613669cb75f5d9dc21ca063d94d588`。

来源：data/v2/test/dataset_test.jsonl，第 49 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

判断平面 $x+2y+2z=3$ 与球面 $x^2+y^2+z^2=1$ 的位置关系，若相切求切点。

**过程**

球心 $O(0,0,0)$ 到平面的距离 $d=\dfrac{|0+0+0-3|}{\sqrt{1+4+4}}=\dfrac{3}{3}=1$，等于球半径 $1$，故平面与球面相切。切点在球心到平面的垂线上：$\overrightarrow{OQ}$ 沿法向量 $(1,2,2)$，且 $|OQ|=1$，$Q=\dfrac{1}{3}(1,2,2)=\left(\dfrac{1}{3},\dfrac{2}{3},\dfrac{2}{3}\right)$。验证在平面上：$\dfrac{1}{3}+\dfrac{4}{3}+\dfrac{4}{3}=\dfrac{9}{3}=3$。

**答案原文**

相切，切点 $\left(\dfrac{1}{3},\dfrac{2}{3},\dfrac{2}{3}\right)$

## 350. test-geom-005

内容 SHA256：`cdc9e516efe9a240b4c11e61e3b28b583199a5d1c78465a9977572df4ef22208`。

来源：data/v2/test/dataset_test.jsonl，第 50 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求曲面 $z=\dfrac{x^2}{4}+y^2$ 在点 $(2,1,2)$ 处的切平面方程。

**过程**

$z_x=\dfrac{x}{2}$，$z_y=2y$。在 $(2,1)$ 处 $z_x=1$、$z_y=2$。切平面：$z-2=1\cdot(x-2)+2\cdot(y-1)$，即 $z=x+2y-2$。验证切点在平面上：$2=2+2-2$。

**答案原文**

$z=x+2y-2$

## 351. test-geom-006

内容 SHA256：`0c4ada68c6bf6f27e0bbb12a17595d214ae14b7a31a47ebc293a90b922fa8349`。

来源：data/v2/test/dataset_test.jsonl，第 51 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求曲线 $x=t,\ y=t^2,\ z=t^3$ 在 $t=1$ 处的切线与法平面方程。

**过程**

$\vec r'(t)=(1,2t,3t^2)$，在 $t=1$ 处切向量 $(1,2,3)$，切点 $(1,1,1)$。切线：$\dfrac{x-1}{1}=\dfrac{y-1}{2}=\dfrac{z-1}{3}$。法平面：$1\cdot(x-1)+2\cdot(y-1)+3\cdot(z-1)=0$，即 $x+2y+3z=6$。

**答案原文**

切线 $\dfrac{x-1}{1}=\dfrac{y-1}{2}=\dfrac{z-1}{3}$；法平面 $x+2y+3z=6$

## 352. test-geom-007

内容 SHA256：`b8f3bc78ad412a5ba918f587cfe72418de4076f575332b13e656a0252fac93f9`。

来源：data/v2/test/dataset_test.jsonl，第 52 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求以 $O(0,0,0)$、$A(1,2,0)$、$B(2,0,1)$、$C(0,1,2)$ 为顶点的四面体体积。

**过程**

$V=\dfrac{1}{6}\left|\det(\overrightarrow{OA},\overrightarrow{OB},\overrightarrow{OC})\right|=\dfrac{1}{6}\left|\begin{vmatrix}1&2&0\\2&0&1\\0&1&2\end{vmatrix}\right|$。行列式 $=1\cdot(0\cdot 2-1\cdot 1)-2\cdot(2\cdot 2-1\cdot 0)+0=1\cdot(-1)-2\cdot 4=-9$。$V=\dfrac{9}{6}=\dfrac{3}{2}$。

**答案原文**

$\dfrac{3}{2}$

## 353. test-geom-008

内容 SHA256：`2ce3ea4815a248eb2cd2dac180eda394b47ce906bd0c7fe28b0d269bc70ce718`。

来源：data/v2/test/dataset_test.jsonl，第 53 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求以 $A(1,0)$、$B(0,1)$、$C(2,3)$ 为顶点的三角形面积。

**过程**

平面中三角形面积 $S=\dfrac{1}{2}\left|\det(\overrightarrow{AB},\overrightarrow{AC})\right|$。$\overrightarrow{AB}=(-1,1)$，$\overrightarrow{AC}=(1,3)$。$\det=(-1)\cdot 3-1\cdot 1=-4$。$S=\dfrac{1}{2}\cdot 4=2$。

**答案原文**

$2$

## 354. test-geom-009

内容 SHA256：`9e8613a5ad56a5c633c304c6d20a24ef4740fa18407c72105faa59aa3d86880a`。

来源：data/v2/test/dataset_test.jsonl，第 54 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求点 $(2,1)$ 绕原点逆时针旋转 $90^\circ$ 后的坐标，以及向量 $(3,4)$ 在方向 $(1,1)$ 上的投影向量。

**过程**

旋转 $90^\circ$：$(x,y)\mapsto(-y,x)$，$(2,1)\mapsto(-1,2)$。投影：方向单位向量 $\vec u=\dfrac{1}{\sqrt2}(1,1)$，投影 $=((3,4)\cdot\vec u)\vec u=\dfrac{7}{\sqrt2}\cdot\dfrac{1}{\sqrt2}(1,1)=\left(\dfrac{7}{2},\dfrac{7}{2}\right)$。

**答案原文**

$(-1,2)$；$\left(\dfrac{7}{2},\dfrac{7}{2}\right)$

## 355. test-geom-010

内容 SHA256：`7153c209a02cc88839d73fe667c52f30c32a60a0cabba418bc7dedfcb096e344`。

来源：data/v2/test/dataset_test.jsonl，第 55 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求椭圆 $\dfrac{x^2}{9}+\dfrac{y^2}{16}=1$ 的面积。

**过程**

椭圆是半径为 3 的圆沿 $y$ 轴拉伸 $\dfrac{4}{3}$ 倍的像：$S=\pi\cdot 3\cdot 4=12\pi$。或用定积分：$S=4\displaystyle\int_0^3 4\sqrt{1-\dfrac{x^2}{9}}\,dx=16\int_0^3\sqrt{1-\dfrac{x^2}{9}}\,dx$。换元 $x=3\sin t$（$dx=3\cos t\,dt$，$t:0\to\dfrac{\pi}{2}$）：$S=16\cdot 3\displaystyle\int_0^{\pi/2}\cos^2t\,dt=48\cdot\dfrac{\pi}{4}=12\pi$（$\int_0^{\pi/2}\cos^2t\,dt=\dfrac{\pi}{4}$）。直接公式 $S=\pi ab=\pi\cdot 3\cdot 4=12\pi$。

**答案原文**

$12\pi$

## 356. test-geom-011

内容 SHA256：`922a020d3f0e9173fb66480df80b7b70a0102f327efbb44f8c265a77b075f406`。

来源：data/v2/test/dataset_test.jsonl，第 56 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求直线 $\dfrac{x-2}{1}=\dfrac{y+1}{2}=\dfrac{z-3}{-1}$ 与三个坐标面的交点。

**过程**

参数化 $x=2+t,\ y=-1+2t,\ z=3-t$。与 $xOy$ 面（$z=0$）：$3-t=0$，$t=3$，交点 $(5,5,0)$。与 $yOz$ 面（$x=0$）：$2+t=0$，$t=-2$，交点 $(0,-5,5)$。与 $xOz$ 面（$y=0$）：$-1+2t=0$，$t=\dfrac{1}{2}$，交点 $\left(\dfrac{5}{2},0,\dfrac{5}{2}\right)$。

**答案原文**

$(5,5,0)$；$(0,-5,5)$；$\left(\dfrac{5}{2},0,\dfrac{5}{2}\right)$

## 357. test-geom-012

内容 SHA256：`914d35685204ab7a95d995709cfcbcd818d54bbe6878ce5a58a9c6c6dea0e5d7`。

来源：data/v2/test/dataset_test.jsonl，第 57 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $\vec a=(1,0,1)$、$\vec b=(0,1,1)$、$\vec c=(1,1,0)$，求 $\vec a\cdot(\vec b\times\vec c)$ 与 $\vec a\times\vec b\cdot\vec c$，并比较。

**过程**

先算 $\vec b\times\vec c$：$\vec b=(0,1,1)$，$\vec c=(1,1,0)$，叉积 $=(1\cdot 0-1\cdot 1,\ 1\cdot 1-0\cdot 0,\ 0\cdot 1-1\cdot 1)=(-1,1,-1)$。故 $\vec a\cdot(\vec b\times\vec c)=1\cdot(-1)+0\cdot 1+1\cdot(-1)=-2$。再算 $\vec a\times\vec b$：$(0\cdot 1-1\cdot 1,\ 1\cdot 0-1\cdot 1,\ 1\cdot 1-0\cdot 0)=(-1,-1,1)$。故 $(\vec a\times\vec b)\cdot\vec c=(-1)\cdot 1+(-1)\cdot 1+1\cdot 0=-2$。两者相等，符合混合积的轮换对称性 $\vec a\cdot(\vec b\times\vec c)=\vec b\cdot(\vec c\times\vec a)=\vec c\cdot(\vec a\times\vec b)$；该值也等于行列式 $\begin{vmatrix}1&0&1\\0&1&1\\1&1&0\end{vmatrix}=1\cdot(1\cdot 0-1\cdot 1)-0\cdot(0\cdot 0-1\cdot 1)+1\cdot(0\cdot 1-1\cdot 1)=-1-1=-2$。

**答案原文**

均为 $-2$

## 358. test-geom-013

内容 SHA256：`dd8238d1dc459f743c9f46f283e75e45bf29b8c46ac0adb6bc4ed684a7a57f48`。

来源：data/v2/test/dataset_test.jsonl，第 58 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求球面 $x^2+y^2+z^2=4$ 与平面 $z=\sqrt2$ 的交线方程，并将其参数化。

**过程**

代入 $z=\sqrt2$：$x^2+y^2+2=4$，即 $x^2+y^2=2$。交线为平面 $z=\sqrt2$ 上的圆，半径 $\sqrt2$，圆心 $(0,0,\sqrt2)$。参数化：$x=\sqrt2\cos t$，$y=\sqrt2\sin t$，$z=\sqrt2$，$t\in[0,2\pi]$。

**答案原文**

$\begin{cases}x^2+y^2=2\\z=\sqrt2\end{cases}$；参数化 $(x,y,z)=(\sqrt2\cos t,\sqrt2\sin t,\sqrt2)$

## 359. test-geom-014

内容 SHA256：`65dd6ea4f9ebf4131533fa264aa66249bd274b943d0e01ba612ece144877bbb1`。

来源：data/v2/test/dataset_test.jsonl，第 59 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

证明曲面 $z=x^2-y^2$ 是直纹面，并写出其直母线族。

**过程**

$z=x^2-y^2=(x+y)(x-y)$。对任意常数 $c$，直线 $\begin{cases}x+y=c\\z=c(x-y)\end{cases}$ 上每点满足 $z=(x+y)(x-y)=c(x-y)$，故整条直线在曲面上；同理 $\begin{cases}x-y=c\\z=c(x+y)\end{cases}$ 也是直母线族。每点处恰有两条直母线通过，故 $z=x^2-y^2$ 是直纹面（双曲抛物面）。

**答案原文**

证毕；直母线族 $\begin{cases}x+y=c\\z=c(x-y)\end{cases}$ 与 $\begin{cases}x-y=c\\z=c(x+y)\end{cases}$

## 360. test-geom-015

内容 SHA256：`d95c46c35b9827e18c8f63e9f43473c74b0d040259041e8fb609dec582c14bc4`。

来源：data/v2/test/dataset_test.jsonl，第 60 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求曲面 $xyz=1$（$x,y,z>0$）上到原点距离最近的点及最短距离。

**过程**

求 $d^2=x^2+y^2+z^2$ 在 $xyz=1$ 下的最小值。由均值不等式 $x^2+y^2+z^2\ge 3\sqrt[3]{x^2y^2z^2}=3\sqrt[3]{(xyz)^2}=3$，等号当且仅当 $x^2=y^2=z^2$，即 $x=y=z=1$（$xyz=1$）。故最近点为 $(1,1,1)$，最短距离 $\sqrt3$。

**答案原文**

最近点 $(1,1,1)$，距离 $\sqrt3$

## 361. test-geom-016

内容 SHA256：`475b2d53c9ea7a3d7615e68ac47de9c216bc7d58e181e9454dd6d54e5b1b68ad`。

来源：data/v2/test/dataset_test.jsonl，第 61 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

线性变换 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 把单位圆 $x^2+y^2=1$ 变成什么曲线？并求其面积。

**过程**

$A$ 把 $(x,y)$ 映到 $(x',y')=(x+y,y)$。反解 $x=x'-y'$、$y=y'$。代入 $x^2+y^2=1$：$(x'-y')^2+y'^2=1$，即 $x'^2-2x'y'+2y'^2=1$。这是椭圆（二次型 $x'^2-2x'y'+2y'^2$ 正定，因矩阵 $\begin{pmatrix}1&-1\\-1&2\end{pmatrix}$ 顺序主子式 $1>0$、$1>0$）。面积：$\det A=1$，故椭圆面积 $=\pi\cdot|\det A|=\pi$。

**答案原文**

椭圆 $x^2-2xy+2y^2=1$，面积 $\pi$

## 362. test-geom-017

内容 SHA256：`f424c47048559d339054bd2c830622a1895c1ce643a5f78773c6319d11e3a3ce`。

来源：data/v2/test/dataset_test.jsonl，第 62 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求抛物线 $y=x^2$ 在顶点处的曲率与曲率半径，并说明顶点处曲率最大的原因。

**过程**

$\kappa(x)=\dfrac{|y''|}{(1+y'^2)^{3/2}}=\dfrac{2}{(1+4x^2)^{3/2}}$。在顶点 $x=0$：$\kappa=2$，曲率半径 $R=\dfrac{1}{2}$。$\kappa(x)$ 在 $x=0$ 处最大（分母在 $x=0$ 最小），因顶点处曲线"弯得最急"。

**答案原文**

$\kappa=2$；$R=\dfrac{1}{2}$

## 363. test-geom-018

内容 SHA256：`4eec19b22ad7dc429677df89fbbe5917b0c25a2449ac428b0c5eb953f023aed5`。

来源：data/v2/test/dataset_test.jsonl，第 63 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求过直线 $l:\begin{cases}x+y-1=0\\x+z-2=0\end{cases}$ 且过点 $(0,0,0)$ 的平面方程。

**过程**

过 $l$ 的平面束为 $(x+y-1)+\lambda(x+z-2)=0$。代入点 $(0,0,0)$：$-1-2\lambda=0$，$\lambda=-\dfrac{1}{2}$。代入：$(x+y-1)-\dfrac{1}{2}(x+z-2)=0$，即 $x+y-1-\dfrac{x}{2}-\dfrac{z}{2}+1=0$，$\dfrac{x}{2}+y-\dfrac{z}{2}=0$，$x+2y-z=0$。

**答案原文**

$x+2y-z=0$

## 364. test-geom-019

内容 SHA256：`cbf7db86482e89b09b71dc8ac95733b18547f955f4e984f40d64d08512d9386a`。

来源：data/v2/test/dataset_test.jsonl，第 64 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求椭圆 $\dfrac{x^2}{4}+y^2=1$ 上点到 $(1,0)$ 的距离的最大值与最小值。

**过程**

参数化 $(2\cos t,\sin t)$。$d^2=(2\cos t-1)^2+\sin^2t=4\cos^2t-4\cos t+1+1-\cos^2t=3\cos^2t-4\cos t+2$。令 $u=\cos t\in[-1,1]$，$g(u)=3u^2-4u+2$。$g'(u)=6u-4=0$，$u=\dfrac{2}{3}$（在 $[-1,1]$ 内）。$g\left(\dfrac{2}{3}\right)=3\cdot\dfrac{4}{9}-\dfrac{8}{3}+2=\dfrac{4}{3}-\dfrac{8}{3}+2=\dfrac{2}{3}$；端点 $g(1)=1$，$g(-1)=3+4+2=9$。故 $d_{\min}=\sqrt{\dfrac{2}{3}}$，$d_{\max}=3$。

**答案原文**

最小值 $\sqrt{\dfrac{2}{3}}$；最大值 $3$

## 365. test-geom-020

内容 SHA256：`ab0eb7ab6771e915085cd3605416e31bb23d112f876a002c44670abd89fd46b2`。

来源：data/v2/test/dataset_test.jsonl，第 65 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求点 $P(1,2,3)$ 关于平面 $x+y+z=0$ 的对称点。

**过程**

法向量 $\vec n=(1,1,1)$，$|\vec n|^2=3$。$P$ 在平面上的投影为 $Q=P-\dfrac{P\cdot\vec n}{|\vec n|^2}\vec n=(1,2,3)-\dfrac{6}{3}(1,1,1)=(1,2,3)-(2,2,2)=(-1,0,1)$。对称点 $P'=2Q-P=(-2,0,2)-(1,2,3)=(-3,-2,-1)$。验证 $Q$ 在平面上：$-1+0+1=0$。

**答案原文**

$(-3,-2,-1)$

## 366. test-geom-021

内容 SHA256：`b54ac69ea79230b4ee95a74c661842f439f7cbcc8f70abf953a10ab943d3934c`。

来源：data/v2/test/dataset_test.jsonl，第 66 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

已知向量 $\vec a,\vec b,\vec c$ 满足 $\vec a+\vec b+\vec c=\vec 0$，且 $|\vec a|=3$、$|\vec b|=4$、$|\vec c|=5$。求 $\vec a$ 与 $\vec b$ 的夹角。

**过程**

由 $\vec c=-(\vec a+\vec b)$：$|\vec c|^2=|\vec a|^2+|\vec b|^2+2\vec a\cdot\vec b$。代入：$25=9+16+2\vec a\cdot\vec b$，故 $\vec a\cdot\vec b=0$。$\cos\theta=\dfrac{\vec a\cdot\vec b}{|\vec a||\vec b|}=0$，夹角为 $\dfrac{\pi}{2}$。几何上三向量首尾相接成 $3$-$4$-$5$ 直角三角形（勾股定理逆定理）。

**答案原文**

$\dfrac{\pi}{2}$

## 367. test-geom-022

内容 SHA256：`3513e3a9a3b8d49b22717c216edc2a6d652dee5e12f29a6577dada52361ea1c0`。

来源：data/v2/test/dataset_test.jsonl，第 67 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

写出绕 $y$ 轴旋转角 $\varphi$ 的旋转矩阵 $R_y(\varphi)$，并验证它是正交矩阵。

**过程**

绕 $y$ 轴旋转：$x'=x\cos\varphi+z\sin\varphi$，$y'=y$，$z'=-x\sin\varphi+z\cos\varphi$，故 $R_y(\varphi)=\begin{pmatrix}\cos\varphi&0&\sin\varphi\\0&1&0\\-\sin\varphi&0&\cos\varphi\end{pmatrix}$。验证 $R^TR=I$：第一列与第二列点积 $0$、与第三列点积 $\cos\varphi\sin\varphi-\sin\varphi\cos\varphi=0$；各列模长 $\cos^2\varphi+\sin^2\varphi=1$、$1$、$1$。故 $R$ 正交，且 $\det R=1$（旋转保定向）。

**答案原文**

$R_y(\varphi)=\begin{pmatrix}\cos\varphi&0&\sin\varphi\\0&1&0\\-\sin\varphi&0&\cos\varphi\end{pmatrix}$；正交（证毕）

## 368. test-geom-023

内容 SHA256：`3cc9ddc35ec68107f5f8881306a07d0d611a9b7f7530614c36b53e8b2004c63c`。

来源：data/v2/test/dataset_test.jsonl，第 68 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求球面 $x^2+y^2+z^2=4$ 在点 $(1,1,\sqrt2)$ 处的单位外法向量。

**过程**

$F=x^2+y^2+z^2-4$，$\nabla F=(2x,2y,2z)$。在 $(1,1,\sqrt2)$ 处 $\nabla F=(2,2,2\sqrt2)$，模 $=\sqrt{4+4+8}=4$。单位外法向量 $\vec n=\dfrac{\nabla F}{|\nabla F|}=\left(\dfrac{1}{2},\dfrac{1}{2},\dfrac{\sqrt2}{2}\right)$（若问全部单位法向量则为 $\pm\left(\dfrac{1}{2},\dfrac{1}{2},\dfrac{\sqrt2}{2}\right)$）。

**答案原文**

$\left(\dfrac{1}{2},\dfrac{1}{2},\dfrac{\sqrt2}{2}\right)$

## 369. test-geom-024

内容 SHA256：`ac67ed16ee2f4c3fa2b8bf51af73aa05180893f14c69abfc6d33326de604e2f1`。

来源：data/v2/test/dataset_test.jsonl，第 69 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求两平行平面 $2x-y+2z=1$ 与 $2x-y+2z=7$ 之间的距离。

**过程**

在第一个平面上取点（令 $x=z=0$，则 $-y=1$，$y=-1$）$P(0,-1,0)$。$P$ 到第二个平面的距离 $d=\dfrac{|2\cdot 0-(-1)+2\cdot 0-7|}{\sqrt{4+1+4}}=\dfrac{|1-7|}{3}=\dfrac{6}{3}=2$。即两平面距离为 $2$。

**答案原文**

$2$

## 370. test-geom-025

内容 SHA256：`cbde0eb1b8cc45564df66853b0581639169a6e804a7c0ba6019219ec8e3123cb`。

来源：data/v2/test/dataset_test.jsonl，第 70 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求到两定点 $A(1,0,0)$、$B(-1,0,0)$ 距离之和等于 $4$ 的点的轨迹方程，并说明曲面类型。

**过程**

设动点 $P(x,y,z)$，记 $r_1=\sqrt{(x-1)^2+y^2+z^2}$、$r_2=\sqrt{(x+1)^2+y^2+z^2}$，条件为 $r_1+r_2=4$。由 $r_2=4-r_1$ 两边平方：$r_2^2=16-8r_1+r_1^2$。又 $r_2^2-r_1^2=\left[(x+1)^2+y^2+z^2\right]-\left[(x-1)^2+y^2+z^2\right]=(x+1)^2-(x-1)^2=4x$。代入上式：$4x=16-8r_1$，即 $2r_1=4-x$。再平方：$4\left[(x-1)^2+y^2+z^2\right]=(4-x)^2$。展开：$4(x^2-2x+1)+4y^2+4z^2=16-8x+x^2$，整理得 $3x^2+4y^2+4z^2=12$，即 $\dfrac{x^2}{4}+\dfrac{y^2+z^2}{3}=1$。反向验证：由椭球方程得 $3x^2\le 12$，即 $|x|\le 2$，于是 $r_1=\dfrac{4-x}{2}\ge 1$、$r_2=\dfrac{4+x}{2}\ge 1$ 均非负（第二次平方得到的正是 $2r_1=4-x$，故 $r_1=\dfrac{4-x}{2}$ 代入平方前的方程成立，$r_2=4-r_1=\dfrac{4+x}{2}$ 同理），且 $r_1+r_2=4$——椭球上每点都满足原距离和条件，两方程等价。该方程表示绕 $x$ 轴的旋转椭球面：两焦点 $(\pm 1,0,0)$（$c=1$）、长半轴 $a=2$、短半轴 $b=\sqrt{a^2-c^2}=\sqrt3$。

**答案原文**

$\dfrac{x^2}{4}+\dfrac{y^2+z^2}{3}=1$，旋转椭球面

## 371. test-prob-001

内容 SHA256：`587caaa6a4d3dbc856c3c7590c284742a8fb912589708a2552f1dd1238970ded`。

来源：data/v2/test/dataset_test.jsonl，第 71 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

两车间各承担总产量的 $60\%$ 与 $40\%$，次品率分别为 $2\%$ 与 $3\%$。随机抽取一件产品发现是次品，求它来自第一车间的概率。

**过程**

记 $A_1$=来自第一车间，$A_2$=来自第二车间，$B$=次品。$P(A_1)=0.6$，$P(A_2)=0.4$，$P(B|A_1)=0.02$，$P(B|A_2)=0.03$。由全概率公式 $P(B)=0.6\times 0.02+0.4\times 0.03=0.012+0.012=0.024$。由贝叶斯公式 $P(A_1|B)=\dfrac{P(B|A_1)P(A_1)}{P(B)}=\dfrac{0.012}{0.024}=\dfrac{1}{2}$。

**答案原文**

$\dfrac{1}{2}$

## 372. test-prob-002

内容 SHA256：`e265b3be116b1db390896cac585765e265c2704d03840545f2de85d1ddc162ea`。

来源：data/v2/test/dataset_test.jsonl，第 72 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $X\sim B\!\left(10,\dfrac{3}{10}\right)$。求 $P(X=3)$ 与 $P(X\le 1)$ 的精确值。

**过程**

$P(X=k)=\binom{10}{k}\left(\dfrac{3}{10}\right)^k\left(\dfrac{7}{10}\right)^{10-k}$。$P(X=3)=\binom{10}{3}\cdot 0.3^3\cdot 0.7^7=120\times 0.027\times 0.0823543=0.266827932$。$P(X\le 1)=P(X=0)+P(X=1)=0.7^{10}+10\times 0.3\times 0.7^9=0.0282475249+3\times 0.040353607=0.0282475249+0.121060821=0.1493083459=\dfrac{1493083459}{10^{10}}$。

**答案原文**

$P(X=3)=0.266827932$；$P(X\le 1)=0.1493083459$

## 373. test-prob-003

内容 SHA256：`2c18f9314c94afea6d418d15cbcb84de7b5fff35ea8fb4a4fc3e2e4dc7552451`。

来源：data/v2/test/dataset_test.jsonl，第 73 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

用指示变量法推导 $X\sim B(n,p)$ 的期望与方差。

**过程**

设 $X=\displaystyle\sum_{i=1}^{n}X_i$，其中 $X_i$ 为第 $i$ 次试验成功的指示变量（独立，$P(X_i=1)=p$）。$E[X_i]=p$，由期望线性性 $E[X]=np$。$\operatorname{Var}(X_i)=E[X_i^2]-p^2=p-p^2=p(1-p)$。由独立性 $\operatorname{Var}(X)=\displaystyle\sum_{i=1}^{n}\operatorname{Var}(X_i)=np(1-p)$（独立变量的方差可加）。

**答案原文**

$E[X]=np$；$\operatorname{Var}(X)=np(1-p)$

## 374. test-prob-004

内容 SHA256：`90c72c80f43f2ab26a2249c988d3adc960e629f755f2f6ada7389ed5c9716a10`。

来源：data/v2/test/dataset_test.jsonl，第 74 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $X$ 的密度为 $f(x)=3x^2$（$0<x<1$）。求 $X$ 的分布函数、$P\!\left(X>\dfrac{1}{2}\right)$ 与 $E[X]$。

**过程**

分布函数 $F(x)=\displaystyle\int_0^x3t^2dt=x^3$（$0<x<1$；$x\le 0$ 时为 0，$x\ge 1$ 时为 1）。$P\!\left(X>\dfrac{1}{2}\right)=1-F\!\left(\dfrac{1}{2}\right)=1-\dfrac{1}{8}=\dfrac{7}{8}$。$E[X]=\displaystyle\int_0^1x\cdot 3x^2dx=3\int_0^1x^3dx=\dfrac{3}{4}$。

**答案原文**

$F(x)=\begin{cases}0,&x\le 0\\x^3,&0<x<1\\1,&x\ge 1\end{cases}$；$P\!\left(X>\dfrac12\right)=\dfrac{7}{8}$；$E[X]=\dfrac{3}{4}$

## 375. test-prob-005

内容 SHA256：`a131138b72ed648333a3d4183a4539e3d7d7cde29e05b2755b6bf02921e54135`。

来源：data/v2/test/dataset_test.jsonl，第 75 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $X,Y$ 独立同分布于 $U(0,1)$，求 $Z=X+Y$ 的密度与 $P(Z>1.5)$。

**过程**

$f_Z(z)=\displaystyle\int_0^1 f_X(x)f_Y(z-x)dx=\int_0^1\mathbf 1_{[0,1]}(z-x)dx$。当 $0<z<1$：$f_Z(z)=\displaystyle\int_0^z dx=z$；当 $1\le z<2$：$f_Z(z)=\displaystyle\int_{z-1}^1 dx=2-z$；其余为 0（三角分布）。$P(Z>1.5)=\displaystyle\int_{1.5}^{2}(2-z)dz=\left[2z-\dfrac{z^2}{2}\right]_{1.5}^{2}=\left(4-2\right)-\left(3-\dfrac{2.25}{2}\right)=2-(3-1.125)=0.125=\dfrac{1}{8}$。

**答案原文**

$f_Z(z)=z$（$0<z<1$），$f_Z(z)=2-z$（$1\le z<2$），其余 $z$ 处为 $0$；$P(Z>1.5)=\dfrac{1}{8}$

## 376. test-prob-006

内容 SHA256：`6e0fb847aed580c9e3deb952f7372a8c83a0327335ec26b3fd0cee9d508e7a8c`。

来源：data/v2/test/dataset_test.jsonl，第 76 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $X\sim\operatorname{Poisson}(4)$。求 $P(X=2)$ 与 $P(X\ge 1)$ 的精确表达式。

**过程**

$P(X=k)=\dfrac{4^ke^{-4}}{k!}$。$P(X=2)=\dfrac{16e^{-4}}{2}=8e^{-4}$。$P(X\ge 1)=1-P(X=0)=1-e^{-4}$（$P(X=0)=\dfrac{4^0e^{-4}}{0!}=e^{-4}$）。

**答案原文**

$P(X=2)=8e^{-4}$；$P(X\ge 1)=1-e^{-4}$

## 377. test-prob-007

内容 SHA256：`c926b8ffcea84b836ae617dca077ca88f33594d47df2ba99fdc2f293afa5fd67`。

来源：data/v2/test/dataset_test.jsonl，第 77 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

某灯泡寿命 $T\sim\operatorname{Exp}\!\left(\dfrac{1}{1000}\right)$（单位：小时，参数 $\lambda=\dfrac{1}{1000}$）。求 $P(T>1500\mid T>500)$。

**过程**

指数分布无记忆性：$P(T>s+t\mid T>s)=P(T>t)=e^{-\lambda t}$。取 $s=500$、$t=1000$：$P(T>1500\mid T>500)=P(T>1000)=e^{-1000/1000}=e^{-1}$。直接验证：$P(T>1500)=e^{-1.5}$，$P(T>500)=e^{-0.5}$，比值 $=\dfrac{e^{-1.5}}{e^{-0.5}}=e^{-1}$。

**答案原文**

$e^{-1}$

## 378. test-prob-008

内容 SHA256：`b2efd22f9906d84795f667b115cd9109ac111bb1de27d91bffad164d5d3def53`。

来源：data/v2/test/dataset_test.jsonl，第 78 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

掷均匀骰子 $n$ 次，设 $\bar X_n$ 为平均点数。用切比雪夫不等式给出 $P\!\left(|\bar X_n-3.5|\ge 0.1\right)$ 的上界，并说明 $n\to\infty$ 时该概率趋于 $0$（弱大数定律）。

**过程**

单次点数 $X$：$E[X]=\dfrac{7}{2}$，$\operatorname{Var}(X)=\dfrac{35}{12}$。$\bar X_n$ 的方差 $=\dfrac{35}{12n}$。由切比雪夫不等式 $P\!\left(|\bar X_n-E[\bar X_n]|\ge\varepsilon\right)\le\dfrac{\operatorname{Var}(\bar X_n)}{\varepsilon^2}$，取 $\varepsilon=0.1$：$P\!\left(|\bar X_n-3.5|\ge 0.1\right)\le\dfrac{35/12n}{0.01}=\dfrac{35}{0.12n}=\dfrac{875}{3n}$（$\approx\dfrac{291.67}{n}$）。概率不超过 1，完整上界为 $\min\left\{1,\dfrac{875}{3n}\right\}$。当 $n\to\infty$ 时上界趋于 $0$，故概率趋于 $0$（弱大数定律：样本均值依概率收敛于期望）。

**答案原文**

上界 $\min\left\{1,\dfrac{875}{3n}\right\}$；$n\to\infty$ 时趋于 $0$

## 379. test-prob-009

内容 SHA256：`af8fa9b23b0bb53582f15c8de6a705c65e957abdd7301c366b815b8c44fd501c`。

来源：data/v2/test/dataset_test.jsonl，第 79 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $X\sim N(2,3)$（均值 2、方差 3），$Y=2X-1$。求 $Y$ 的分布与 $P(Y>3)$。

**过程**

正态分布在线性变换下仍为正态：$E[Y]=2E[X]-1=3$，$\operatorname{Var}(Y)=4\operatorname{Var}(X)=12$，故 $Y\sim N(3,12)$。标准化 $Z=\dfrac{Y-3}{\sqrt{12}}\sim N(0,1)$。$P(Y>3)=P\!\left(Z>\dfrac{3-3}{\sqrt{12}}\right)=P(Z>0)=\dfrac{1}{2}$（标准正态关于 0 对称）。

**答案原文**

$Y\sim N(3,12)$；$P(Y>3)=\dfrac{1}{2}$

## 380. test-prob-010

内容 SHA256：`337b936100153c5ec536d1c0b35175721c0c9d65b2f39efbe1928e2823bf1395`。

来源：data/v2/test/dataset_test.jsonl，第 80 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $X\sim U(0,1)$，$Y=X^2$。求 $\operatorname{Cov}(X,Y)$ 与相关系数 $\rho(X,Y)$。

**过程**

$E[X]=\dfrac{1}{2}$，$E[X^2]=\dfrac{1}{3}$，$E[X^3]=\dfrac{1}{4}$，$E[X^4]=\dfrac{1}{5}$。$\operatorname{Cov}(X,Y)=E[X^3]-E[X]E[X^2]=\dfrac{1}{4}-\dfrac{1}{2}\cdot\dfrac{1}{3}=\dfrac{1}{4}-\dfrac{1}{6}=\dfrac{1}{12}$。$\operatorname{Var}(X)=\dfrac{1}{12}$，$\operatorname{Var}(Y)=E[X^4]-(E[X^2])^2=\dfrac{1}{5}-\dfrac{1}{9}=\dfrac{4}{45}$。$\rho=\dfrac{\operatorname{Cov}}{\sqrt{\operatorname{Var}(X)\operatorname{Var}(Y)}}=\dfrac{1/12}{\sqrt{\frac{1}{12}\cdot\frac{4}{45}}}=\dfrac{1/12}{\sqrt{1/135}}=\dfrac{\sqrt{135}}{12}=\dfrac{3\sqrt{15}}{12}=\dfrac{\sqrt{15}}{4}$。

**答案原文**

$\operatorname{Cov}(X,Y)=\dfrac{1}{12}$；$\rho=\dfrac{\sqrt{15}}{4}$

## 381. test-prob-011

内容 SHA256：`f6b184ad78221156d6133afe2b7931e26351e4b71776261a49513c24dcd0cc4a`。

来源：data/v2/test/dataset_test.jsonl，第 81 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

$(X,Y)$ 在三角形 $D=\{(x,y):x\ge 0,\ y\ge 0,\ x+y\le 2\}$ 上均匀分布。求条件密度 $f_{Y|X}(y|x)$ 与 $E[Y|X=x]$，并求 $E[Y]$。

**过程**

$D$ 面积为 $\dfrac{1}{2}\cdot 2\cdot 2=2$，联合密度 $f(x,y)=\dfrac{1}{2}$（$(x,y)\in D$）。边缘密度 $f_X(x)=\displaystyle\int_0^{2-x}\dfrac{1}{2}dy=\dfrac{2-x}{2}$（$0<x<2$）。条件密度 $f_{Y|X}(y|x)=\dfrac{f(x,y)}{f_X(x)}=\dfrac{1}{2-x}$（$0<y<2-x$，即在 $(0,2-x)$ 上均匀）。$E[Y|X=x]=\dfrac{2-x}{2}$。$E[Y]=\displaystyle\int_0^2E[Y|X=x]f_X(x)dx=\int_0^2\dfrac{2-x}{2}\cdot\dfrac{2-x}{2}dx=\dfrac{1}{4}\int_0^2(2-x)^2dx=\dfrac{1}{4}\cdot\dfrac{8}{3}=\dfrac{2}{3}$。

**答案原文**

$0<x<2$ 时，$f_{Y|X}(y|x)=\dfrac{1}{2-x}$（$0<y<2-x$，其余 $y$ 处为 0）；$E[Y|X=x]=\dfrac{2-x}{2}$；$E[Y]=\dfrac{2}{3}$

## 382. test-prob-012

内容 SHA256：`f5dac81fe8375dab8debc468a0ff3f11db40e82663f15eb87cdb7da20aae33b1`。

来源：data/v2/test/dataset_test.jsonl，第 82 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

袋中有 3 个红球、2 个白球，不放回地抽取 2 个。求恰抽到一红一白的概率。

**过程**

样本空间为从 5 球中取 2 球，共 $C_5^2=10$ 种等可能结果。恰一红一白：$C_3^1\cdot C_2^1=6$ 种。故 $P=\dfrac{6}{10}=\dfrac{3}{5}$。（超几何分布公式 $P=\dfrac{\binom{3}{1}\binom{2}{1}}{\binom{5}{2}}=\dfrac{3}{5}$。）

**答案原文**

$\dfrac{3}{5}$

## 383. test-prob-013

内容 SHA256：`db00a568540ea51f225644ac641b68e1ccaac431cb7bcc2bb7f0bcbf178afb62`。

来源：data/v2/test/dataset_test.jsonl，第 83 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $X\sim\operatorname{Poisson}(\lambda)$。求矩母函数 $M(t)$，并用它求 $E[X]$ 与 $E[X^2]$。

**过程**

$M(t)=E[e^{tX}]=\displaystyle\sum_{k=0}^{\infty}e^{tk}\dfrac{\lambda^ke^{-\lambda}}{k!}=e^{-\lambda}\sum_{k=0}^{\infty}\dfrac{(\lambda e^t)^k}{k!}=e^{-\lambda}e^{\lambda e^t}=e^{\lambda(e^t-1)}$。$M'(t)=M(t)\cdot\lambda e^t$，$M'(0)=\lambda$，故 $E[X]=\lambda$。$M''(t)=M(t)\left[(\lambda e^t)^2+\lambda e^t\right]$，$M''(0)=\lambda^2+\lambda$，故 $E[X^2]=\lambda^2+\lambda$（与 eval-prob-006 一致）。

**答案原文**

$M(t)=e^{\lambda(e^t-1)}$；$E[X]=\lambda$；$E[X^2]=\lambda^2+\lambda$

## 384. test-prob-014

内容 SHA256：`3ed98e68d16f730755d2c97f40a735a3f8ef1ef97dddd9df62379dcbdb09077e`。

来源：data/v2/test/dataset_test.jsonl，第 84 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

掷均匀骰子直到出现 6 为止。求所需投掷次数的期望。

**过程**

设 $E$ 为期望次数。第一次若为 6（概率 $\dfrac{1}{6}$），总次数 1；否则（概率 $\dfrac{5}{6}$）回到初始状态，总次数 $1+E$。故 $E=\dfrac{1}{6}\cdot 1+\dfrac{5}{6}\cdot(1+E)=1+\dfrac{5E}{6}$，解得 $E=6$。（几何分布 $p=\dfrac{1}{6}$ 的期望 $\dfrac{1}{p}=6$。）

**答案原文**

$6$

## 385. test-prob-015

内容 SHA256：`77f07e01fa9c3c6600f56a0e030a3a840fe2cf8b79d4cfc96a2f303e62ac6160`。

来源：data/v2/test/dataset_test.jsonl，第 85 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

甲乙两人独立地抛硬币直到各自出现正面为止。求两人在同一时刻停止的概率。

**过程**

设两人停止时刻为 $X,Y$，独立同分布于 $\operatorname{Geom}\!\left(\dfrac{1}{2}\right)$，$P(X=k)=P(Y=k)=\left(\dfrac{1}{2}\right)^k$。$P(X=Y)=\displaystyle\sum_{k=1}^{\infty}P(X=k)P(Y=k)=\sum_{k=1}^{\infty}\left(\dfrac{1}{2}\right)^{2k}=\sum_{k=1}^{\infty}\left(\dfrac{1}{4}\right)^k=\dfrac{1/4}{1-1/4}=\dfrac{1}{3}$。

**答案原文**

$\dfrac{1}{3}$

## 386. test-prob-016

内容 SHA256：`0ce595e217fa084dc00d100346c74d81800f691d9aebc56c660d3002222509eb`。

来源：data/v2/test/dataset_test.jsonl，第 86 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

某地天气的转移矩阵为 $P=\begin{pmatrix}0.8&0.2\\0.4&0.6\end{pmatrix}$（状态 1 晴、状态 2 雨，行表示今天）。求稳态分布。

**过程**

稳态分布 $\pi=(\pi_1,\pi_2)$ 满足 $\pi=\pi P$ 且 $\pi_1+\pi_2=1$：$\pi_1=0.8\pi_1+0.4\pi_2$，即 $0.2\pi_1=0.4\pi_2$，$\pi_1=2\pi_2$。由 $\pi_1+\pi_2=1$：$3\pi_2=1$，$\pi_2=\dfrac{1}{3}$，$\pi_1=\dfrac{2}{3}$。故稳态分布 $\left(\dfrac{2}{3},\dfrac{1}{3}\right)$。

**答案原文**

$\left(\dfrac{2}{3},\dfrac{1}{3}\right)$

## 387. test-prob-017

内容 SHA256：`969a19289f5462713ffcecaabee40b5f05c2afba4330399291d53046245eaf10`。

来源：data/v2/test/dataset_test.jsonl，第 87 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $X,Y$ 独立同分布于 $U(0,1)$。求 $M=\max(X,Y)$ 的分布函数，并求 $E[M]$。

**过程**

$F_M(t)=P(\max(X,Y)\le t)=P(X\le t)P(Y\le t)=t^2$（$0<t<1$，$t\le 0$ 为 0、$t\ge 1$ 为 1）。密度 $f_M(t)=2t$（$0<t<1$）。$E[M]=\displaystyle\int_0^1t\cdot 2t\,dt=\dfrac{2}{3}$。

**答案原文**

$F_M(t)=\begin{cases}0,&t\le 0\\t^2,&0<t<1\\1,&t\ge 1\end{cases}$；$E[M]=\dfrac{2}{3}$

## 388. test-prob-018

内容 SHA256：`a5ae8230133b3ec525559ef036aacfece08f18999d5c99c80b1fc24fa0752109`。

来源：data/v2/test/dataset_test.jsonl，第 88 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $X\sim\operatorname{Exp}(\lambda)$。求 $E[e^{tX}]$ 的收敛条件与表达式。

**过程**

$M(t)=E[e^{tX}]=\displaystyle\int_0^{\infty}e^{tx}\lambda e^{-\lambda x}dx=\lambda\int_0^{\infty}e^{(t-\lambda)x}dx$。当 $t<\lambda$ 时收敛：$M(t)=\lambda\cdot\dfrac{1}{\lambda-t}=\dfrac{\lambda}{\lambda-t}$；当 $t\ge\lambda$ 时积分发散（$t=\lambda$ 时 $\int\lambda\,dx$ 发散）。收敛条件 $t<\lambda$ 恰对应"指数增长阶小于衰减率"。

**答案原文**

$M(t)=\dfrac{\lambda}{\lambda-t}$（$t<\lambda$）

## 389. test-prob-019

内容 SHA256：`b66b9b9b75d2f7887791234d2fdd208403b67207a374d69e61ed57da52153593`。

来源：data/v2/test/dataset_test.jsonl，第 89 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $X_1,\dots,X_5$ 独立同分布于 $U(0,1)$。求 $E[\min X_i]$ 与 $E[\max X_i]$。

**过程**

$P(\max\le t)=t^5$，密度 $5t^4$，$E[\max]=\displaystyle\int_0^1t\cdot 5t^4dt=\dfrac{5}{6}$。$P(\min>t)=(1-t)^5$，故 $F_{\min}(t)=1-(1-t)^5$，密度 $5(1-t)^4$，$E[\min]=\displaystyle\int_0^1t\cdot 5(1-t)^4dt$。令 $u=1-t$：$=5\displaystyle\int_0^1(1-u)u^4du=5\left(\dfrac{1}{5}-\dfrac{1}{6}\right)=1-\dfrac{5}{6}=\dfrac{1}{6}$。

**答案原文**

$E[\min]=\dfrac{1}{6}$；$E[\max]=\dfrac{5}{6}$

## 390. test-prob-020

内容 SHA256：`3c1480d89fc6694519790fae7a8b02aee65690ae1857df3dcc5bcb26674451ff`。

来源：data/v2/test/dataset_test.jsonl，第 90 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

口袋里有 10 把钥匙，其中只有 1 把能开门，逐一不放回尝试。求打开门所需尝试次数的期望。

**过程**

正确钥匙在尝试序列中的位置 $X$ 在 $\{1,2,\dots,10\}$ 上均匀（等可能排在第 $k$ 次）。$E[X]=\dfrac{1+10}{2}=\dfrac{11}{2}=5.5$。

**答案原文**

$\dfrac{11}{2}$

## 391. test-prob-021

内容 SHA256：`bbee263378fd94353da64dad79fb79d29abb45360795bc79cbb01da7915143c8`。

来源：data/v2/test/dataset_test.jsonl，第 91 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $A,B$ 独立，$P(A)=0.4$，$P(A\cup B)=0.7$。求 $P(B)$。

**过程**

加法公式：$P(A\cup B)=P(A)+P(B)-P(A\cap B)$。由独立性 $P(A\cap B)=P(A)P(B)=0.4P(B)$。代入：$0.7=0.4+P(B)-0.4P(B)=0.4+0.6P(B)$，故 $P(B)=\dfrac{0.3}{0.6}=0.5$。

**答案原文**

$0.5$

## 392. test-prob-022

内容 SHA256：`72f44580708862165848494228355b3099537f6120431600bce471d1228f5e99`。

来源：data/v2/test/dataset_test.jsonl，第 92 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

掷两枚均匀骰子，设 $X$ 为两数之和。求 $\operatorname{Var}(X)$。

**过程**

设 $X=X_1+X_2$，$X_1,X_2$ 独立同分布（单次骰子），$\operatorname{Var}(X_i)=\dfrac{35}{12}$（eval-prob-015）。由独立性 $\operatorname{Var}(X)=\operatorname{Var}(X_1)+\operatorname{Var}(X_2)=\dfrac{35}{12}+\dfrac{35}{12}=\dfrac{35}{6}$。直接验证：$E[X]=7$，$E[X^2]=\displaystyle\sum_{k=2}^{12}k^2P(X=k)=\dfrac{1974}{36}=\dfrac{329}{6}$，$\operatorname{Var}(X)=\dfrac{329}{6}-49=\dfrac{329-294}{6}=\dfrac{35}{6}$，一致。

**答案原文**

$\dfrac{35}{6}$

## 393. test-prob-023

内容 SHA256：`ccdd6f85bb2c3eaeb9e4a2b08c14c56452a632236bb4cb7bd90d10420fca04ec`。

来源：data/v2/test/dataset_test.jsonl，第 93 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

布丰投针：平面上画有间距为 $d$ 的平行线，投掷长为 $l$（$l\le d$）的针。求针与任一直线相交的概率。

**过程**

设针中点到最近平行线的距离为 $x\sim U\!\left(0,\dfrac{d}{2}\right)$，针与平行线的夹角为 $\theta\sim U\!\left(0,\dfrac{\pi}{2}\right)$，两者独立。相交条件：$x\le\dfrac{l}{2}\sin\theta$。联合密度 $f(x,\theta)=\dfrac{2}{d}\cdot\dfrac{2}{\pi}$。相交概率 $P=\dfrac{4}{\pi d}\displaystyle\int_0^{\pi/2}\!\!\int_0^{(l/2)\sin\theta}dx\,d\theta=\dfrac{4}{\pi d}\int_0^{\pi/2}\dfrac{l}{2}\sin\theta\,d\theta=\dfrac{2l}{\pi d}\left[-\cos\theta\right]_0^{\pi/2}=\dfrac{2l}{\pi d}$。

**答案原文**

$\dfrac{2l}{\pi d}$

## 394. test-prob-024

内容 SHA256：`300c47ad7dc6ababa7a9987181b737daf5c81e25e595b187444627469d5fc780`。

来源：data/v2/test/dataset_test.jsonl，第 94 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

证明泊松分布的概率质量函数归一化：$\displaystyle\sum_{k=0}^{\infty}\frac{\lambda^ke^{-\lambda}}{k!}=1$，并用阶乘矩求 $\operatorname{Var}(X)$（$X\sim\operatorname{Poisson}(\lambda)$）。

**过程**

归一化：$\displaystyle\sum_{k=0}^{\infty}\dfrac{\lambda^ke^{-\lambda}}{k!}=e^{-\lambda}\sum_{k=0}^{\infty}\dfrac{\lambda^k}{k!}=e^{-\lambda}\cdot e^{\lambda}=1$（$e^\lambda$ 的泰勒展开）。阶乘矩：$E[X(X-1)]=\displaystyle\sum_{k=2}^{\infty}k(k-1)\dfrac{\lambda^ke^{-\lambda}}{k!}=\lambda^2e^{-\lambda}\sum_{k=2}^{\infty}\dfrac{\lambda^{k-2}}{(k-2)!}=\lambda^2e^{-\lambda}e^{\lambda}=\lambda^2$。故 $E[X^2]=E[X(X-1)]+E[X]=\lambda^2+\lambda$，$\operatorname{Var}(X)=E[X^2]-\lambda^2=\lambda$。

**答案原文**

证毕；$\operatorname{Var}(X)=\lambda$

## 395. test-prob-025

内容 SHA256：`aeadd442cd9fa3c03cbddc3cd0b878f446d31ba01a9af950d6d29b523962adb3`。

来源：data/v2/test/dataset_test.jsonl，第 95 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

掷一枚均匀骰子得 $X$ 分；若 $X=6$ 则可再掷一次并将点数累加。求总得分的期望。

**过程**

设总得分为 $Y$。第一次掷出 $X$；若 $X=6$ 则加第二次的 $Z$（与 $X$ 独立同分布）。$E[Y]=E[X]+E[\mathbf 1_{\{X=6\}}Z]=E[X]+P(X=6)E[Z]=\dfrac{7}{2}+\dfrac{1}{6}\cdot\dfrac{7}{2}=\dfrac{7}{2}\left(1+\dfrac{1}{6}\right)=\dfrac{7}{2}\cdot\dfrac{7}{6}=\dfrac{49}{12}$。

**答案原文**

$\dfrac{49}{12}$

## 396. test-linalg-001

内容 SHA256：`c31486c40800085dcb48dadd5834da2e197d64462177128292e6e14b46d3dd3c`。

来源：data/v2/test/dataset_test.jsonl，第 96 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

用 Cramer 法则解方程组 $\begin{cases}2x+y-z=1\\x-y+z=2\\x+2y+z=4\end{cases}$。

**过程**

系数行列式 $D=\begin{vmatrix}2&1&-1\\1&-1&1\\1&2&1\end{vmatrix}=2\cdot(-1-2)-1\cdot(1-1)+(-1)\cdot(2+1)=-6-0-3=-9$。$D_x=\begin{vmatrix}1&1&-1\\2&-1&1\\4&2&1\end{vmatrix}=1\cdot(-1-2)-1\cdot(2-4)+(-1)\cdot(4+4)=-3+2-8=-9$，$x=\dfrac{D_x}{D}=\dfrac{-9}{-9}=1$。$D_y=\begin{vmatrix}2&1&-1\\1&2&1\\1&4&1\end{vmatrix}=2\cdot(2-4)-1\cdot(1-1)+(-1)\cdot(4-2)=-4-0-2=-6$，$y=\dfrac{-6}{-9}=\dfrac{2}{3}$。$D_z=\begin{vmatrix}2&1&1\\1&-1&2\\1&2&4\end{vmatrix}=2\cdot(-4-4)-1\cdot(4-2)+1\cdot(2+1)=-16-2+3=-15$，$z=\dfrac{-15}{-9}=\dfrac{5}{3}$。验证：$2\cdot 1+\dfrac{2}{3}-\dfrac{5}{3}=1$；$1-\dfrac{2}{3}+\dfrac{5}{3}=2$；$1+\dfrac{4}{3}+\dfrac{5}{3}=4$。

**答案原文**

$(x,y,z)=\left(1,\dfrac{2}{3},\dfrac{5}{3}\right)$

## 397. test-linalg-002

内容 SHA256：`48a592731a7ca36426b894d22b37432fa8607ac23de026fbf36057fbd84e539d`。

来源：data/v2/test/dataset_test.jsonl，第 97 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

解矩阵方程 $AX=B$，其中 $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$，$B=\begin{pmatrix}3\\3\end{pmatrix}$。

**过程**

$\det A=4-1=3$，$A^{-1}=\dfrac{1}{3}\begin{pmatrix}2&-1\\-1&2\end{pmatrix}$。$X=A^{-1}B=\dfrac{1}{3}\begin{pmatrix}2&-1\\-1&2\end{pmatrix}\begin{pmatrix}3\\3\end{pmatrix}=\dfrac{1}{3}\begin{pmatrix}6-3\\-3+6\end{pmatrix}=\begin{pmatrix}1\\1\end{pmatrix}$。验证：$AX=\begin{pmatrix}2&1\\1&2\end{pmatrix}\begin{pmatrix}1\\1\end{pmatrix}=\begin{pmatrix}3\\3\end{pmatrix}=B$。

**答案原文**

$X=\begin{pmatrix}1\\1\end{pmatrix}$

## 398. test-linalg-003

内容 SHA256：`cb256a9793933022f8a52bda4870798e6ceb70fe3a7d99f8176d5a032fe65360`。

来源：data/v2/test/dataset_test.jsonl，第 98 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求所有满足 $B^2=A$ 的二阶实矩阵 $B$，其中 $A=\begin{pmatrix}1&2\\0&1\end{pmatrix}$。

**过程**

设 $B=\begin{pmatrix}a&b\\c&d\end{pmatrix}$。由 $B^2=A$ 得 $B$ 与 $A$ 可交换（$BA=B^3=AB$）。与 $A=I+2N$（$N=\begin{pmatrix}0&1\\0&0\end{pmatrix}$，$N^2=0$）可交换的矩阵族为 $\{aI+bN\}$（解 $XA=AX$：$\begin{pmatrix}a&b\\c&d\end{pmatrix}\begin{pmatrix}1&2\\0&1\end{pmatrix}=\begin{pmatrix}a&2a+b\\c&2c+d\end{pmatrix}$，$\begin{pmatrix}1&2\\0&1\end{pmatrix}\begin{pmatrix}a&b\\c&d\end{pmatrix}=\begin{pmatrix}a+2c&b+2d\\c&d\end{pmatrix}$，逐项相等得 $c=0$、$a=d$，即 test-linalg-019 的结论）。故 $B=aI+bN$。代入 $B^2=(aI+bN)^2=a^2I+2abN$（$N^2=0$ 且 $IN=NI$），要求 $a^2I+2abN=I+2N$。比较系数：$a^2=1$、$2ab=2$。由 $a^2=1$ 得 $a=\pm 1$；代入 $2ab=2$ 得 $b=a$，故 $(a,b)=(1,1)$ 或 $(-1,-1)$。于是 $B=\pm(I+N)=\pm\begin{pmatrix}1&1\\0&1\end{pmatrix}$。验证：$\begin{pmatrix}1&1\\0&1\end{pmatrix}^2=\begin{pmatrix}1&2\\0&1\end{pmatrix}=A$；$(-B)^2=A$ 同理。

**答案原文**

$B=\pm\begin{pmatrix}1&1\\0&1\end{pmatrix}$

## 399. test-linalg-004

内容 SHA256：`76b36ce01a8d63ef8addbceaa313981441ba6b250e42e5cc95bb860c7ba489a7`。

来源：data/v2/test/dataset_test.jsonl，第 99 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设线性变换 $T:\mathbb R^4\to\mathbb R^3$ 的矩阵为 $\begin{pmatrix}1&0&1&0\\0&1&1&0\\1&1&2&0\end{pmatrix}$。求 $\operatorname{rank}T$ 与 $\dim\ker T$。

**过程**

第三行 $=$ 第一行 $+$ 第二行，且第一、二行线性无关，故 $\operatorname{rank}T=2$。由秩-零化度定理 $\dim\ker T=4-2=2$。核方程：$x_1+x_3=0$、$x_2+x_3=0$，即 $x_3$ 与 $x_4$ 自由，$\ker T=\operatorname{span}\{(-1,-1,1,0)^T,(0,0,0,1)^T\}$，维数 2。

**答案原文**

$\operatorname{rank}T=2$；$\dim\ker T=2$

## 400. test-linalg-005

内容 SHA256：`eb47a70cd927a2f521295b66aed54f78d1628f93f3a752584a48093a8beabfaf`。

来源：data/v2/test/dataset_test.jsonl，第 100 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

已知 3 阶方阵 $A$ 的特征值为 $1,2,3$。求 $\operatorname{tr}A$、$\det A$、$\operatorname{tr}(A^2)$ 及 $A^{-1}$ 的特征值。

**过程**

$\operatorname{tr}A=1+2+3=6$。$\det A=1\cdot 2\cdot 3=6$。$A^2$ 的特征值为 $1^2,2^2,3^2$，故 $\operatorname{tr}(A^2)=1+4+9=14$。$A^{-1}$ 的特征值为 $1,\dfrac{1}{2},\dfrac{1}{3}$（$A$ 可逆因特征值全非零）。

**答案原文**

$\operatorname{tr}A=6$；$\det A=6$；$\operatorname{tr}(A^2)=14$；$A^{-1}$ 的特征值 $1,\dfrac{1}{2},\dfrac{1}{3}$

## 401. test-linalg-006

内容 SHA256：`91d89767d3f41b047557f6b7824285905b41624d5691c3f9c43ef5a4cdce0d2c`。

来源：data/v2/test/dataset_test.jsonl，第 101 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $A=P\begin{pmatrix}2&0\\0&3\end{pmatrix}P^{-1}$。求 $A^{10}$ 的表达式（用 $P$ 表示）。

**过程**

$A^{10}=\left(PDP^{-1}\right)^{10}=PD^{10}P^{-1}$（中间项 $P^{-1}P=I$ 逐对抵消）。$D^{10}=\begin{pmatrix}2^{10}&0\\0&3^{10}\end{pmatrix}=\begin{pmatrix}1024&0\\0&59049\end{pmatrix}$。故 $A^{10}=P\begin{pmatrix}1024&0\\0&59049\end{pmatrix}P^{-1}$。

**答案原文**

$A^{10}=P\begin{pmatrix}1024&0\\0&59049\end{pmatrix}P^{-1}$

## 402. test-linalg-007

内容 SHA256：`7b2bfb605f5dfccc514949dece068f2a3542e1b8d9449ef3283f96026bae44b6`。

来源：data/v2/test/dataset_test.jsonl，第 102 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求二次型 $f(x,y)=x^2+4y^2$ 在单位圆 $x^2+y^2=1$ 上的最大值与最小值。

**过程**

二次型矩阵 $A=\begin{pmatrix}1&0\\0&4\end{pmatrix}$，其特征值为 $1$ 与 $4$。由瑞利商性质，$\lambda_{\min}\le\dfrac{f}{x^2+y^2}\le\lambda_{\max}$，故在单位圆上 $1\le f\le 4$。最小值 $1$ 在 $(x,y)=(\pm 1,0)$ 处取得（特征值 1 的特征向量），最大值 $4$ 在 $(0,\pm 1)$ 处取得。或直接：$f=x^2+4(1-x^2)=4-3x^2$，$x\in[-1,1]$，最小 $1$（$|x|=1$）、最大 $4$（$x=0$）。

**答案原文**

最小值 $1$；最大值 $4$

## 403. test-linalg-008

内容 SHA256：`caeee237c6f03dcc7cefa293efc97e3dbfa3d0f5443acf0376ef4d074395a537`。

来源：data/v2/test/dataset_test.jsonl，第 103 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$。利用 Cayley–Hamilton 定理求 $A^{-1}$。

**过程**

特征多项式 $\chi(\lambda)=\lambda^2-2\lambda-3$。由 C–H 定理 $A^2-2A-3I=0$，即 $A(A-2I)=3I$。故 $A^{-1}=\dfrac{1}{3}(A-2I)=\dfrac{1}{3}\begin{pmatrix}-1&2\\2&-1\end{pmatrix}=\begin{pmatrix}-\frac{1}{3}&\frac{2}{3}\\\frac{2}{3}&-\frac{1}{3}\end{pmatrix}$。验证：$AA^{-1}=\begin{pmatrix}1&2\\2&1\end{pmatrix}\cdot\dfrac{1}{3}\begin{pmatrix}-1&2\\2&-1\end{pmatrix}=\dfrac{1}{3}\begin{pmatrix}3&0\\0&3\end{pmatrix}=I$。

**答案原文**

$A^{-1}=\dfrac{1}{3}\begin{pmatrix}-1&2\\2&-1\end{pmatrix}$

## 404. test-linalg-009

内容 SHA256：`c77b70727b68d119c4cdfebfc9d80f01fb8dc3bdc5cb2e1de95e08617f0ffe5d`。

来源：data/v2/test/dataset_test.jsonl，第 104 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $\mathbb R^2$ 中沿方向 $u=(1,1)^T$ 的投影矩阵，并求 $(3,1)^T$ 的投影。

**过程**

单位方向 $\hat u=\dfrac{1}{\sqrt2}(1,1)^T$。投影矩阵 $P=\hat u\hat u^T=\dfrac{1}{2}\begin{pmatrix}1&1\\1&1\end{pmatrix}=\begin{pmatrix}\frac{1}{2}&\frac{1}{2}\\\frac{1}{2}&\frac{1}{2}\end{pmatrix}$。$P\begin{pmatrix}3\\1\end{pmatrix}=\begin{pmatrix}\frac{1}{2}&\frac{1}{2}\\\frac{1}{2}&\frac{1}{2}\end{pmatrix}\begin{pmatrix}3\\1\end{pmatrix}=\begin{pmatrix}2\\2\end{pmatrix}$。验证 $P^2=P$（幂等）且 $(3,1)^T-(2,2)^T=(1,-1)^T\perp(1,1)^T$。

**答案原文**

$P=\begin{pmatrix}\frac{1}{2}&\frac{1}{2}\\\frac{1}{2}&\frac{1}{2}\end{pmatrix}$；投影为 $(2,2)^T$

## 405. test-linalg-010

内容 SHA256：`2445511194bc8e3fc314159b6dc36198a97eb2f2813892bff808578de133b51c`。

来源：data/v2/test/dataset_test.jsonl，第 105 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $A=\begin{pmatrix}1&1\\1&0\end{pmatrix}$ 的 QR 分解。

**过程**

$a_1=(1,1)^T$：$q_1=\dfrac{a_1}{\|a_1\|}=\dfrac{1}{\sqrt2}(1,1)^T$，$r_{11}=\|a_1\|=\sqrt2$，$r_{12}=q_1^Ta_2=\dfrac{1+0}{\sqrt2}=\dfrac{1}{\sqrt2}$。$a_2-r_{12}q_1=(1,0)^T-\dfrac{1}{2}(1,1)^T=\left(\dfrac{1}{2},-\dfrac{1}{2}\right)^T$，$r_{22}=\sqrt{\dfrac{1}{4}+\dfrac{1}{4}}=\dfrac{1}{\sqrt2}$，$q_2=\left(\dfrac{1}{2},-\dfrac{1}{2}\right)^T\Big/\dfrac{1}{\sqrt2}=\dfrac{1}{\sqrt2}(1,-1)^T$。故 $A=QR$，其中 $Q=\dfrac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$，$R=\begin{pmatrix}\sqrt2&\frac{1}{\sqrt2}\\0&\frac{1}{\sqrt2}\end{pmatrix}$。验证：$QR=\dfrac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}\begin{pmatrix}\sqrt2&\frac{1}{\sqrt2}\\0&\frac{1}{\sqrt2}\end{pmatrix}=\begin{pmatrix}1&1\\1&0\end{pmatrix}$。

**答案原文**

$Q=\dfrac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$，$R=\begin{pmatrix}\sqrt2&\frac{1}{\sqrt2}\\0&\frac{1}{\sqrt2}\end{pmatrix}$

## 406. test-linalg-011

内容 SHA256：`147b3807ea4d7e9fdf53986878ccaa6ca01bd0028e6a4cde1106f5a0fa0a9bfc`。

来源：data/v2/test/dataset_test.jsonl，第 106 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

用最小二乘法拟合数据点 $(1,2),(2,4),(3,7)$ 的直线 $y=ax+b$。

**过程**

$A=\begin{pmatrix}1&1\\2&1\\3&1\end{pmatrix}$，$\vec b=(2,4,7)^T$。法方程 $A^TA\vec x=A^T\vec b$：$A^TA=\begin{pmatrix}14&6\\6&3\end{pmatrix}$，$A^T\vec b=\begin{pmatrix}31\\13\end{pmatrix}$。解 $\begin{cases}14a+6b=31\\6a+3b=13\end{cases}$：由第二式 $2a+b=\dfrac{13}{3}$，$b=\dfrac{13}{3}-2a$。代入第一式：$14a+6\left(\dfrac{13}{3}-2a\right)=31$，即 $14a+26-12a=31$，$2a=5$，$a=\dfrac{5}{2}$，$b=\dfrac{13}{3}-5=-\dfrac{2}{3}$。拟合直线 $y=\dfrac{5}{2}x-\dfrac{2}{3}$。验证：$x=1,2,3$ 时预测值 $\dfrac{11}{6},\dfrac{13}{3},\dfrac{41}{6}$，残差平方和 $\left(\dfrac{1}{6}\right)^2+\left(-\dfrac{1}{3}\right)^2+\left(\dfrac{1}{6}\right)^2=\dfrac{1}{6}$。

**答案原文**

$y=\dfrac{5}{2}x-\dfrac{2}{3}$

## 407. test-linalg-012

内容 SHA256：`39ea4a2dde731d02c48a631c99a1558b48635c7afd55f8c040590912372ada2b`。

来源：data/v2/test/dataset_test.jsonl，第 107 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

用矩阵方法求斐波那契数列 $F_1=F_2=1$，$F_{n+2}=F_{n+1}+F_n$ 中 $F_{10}$ 的值，并说明增长比趋于黄金比。

**过程**

状态矩阵 $A=\begin{pmatrix}1&1\\1&0\end{pmatrix}$ 满足 $\begin{pmatrix}F_{n+1}\\F_n\end{pmatrix}=A\begin{pmatrix}F_n\\F_{n-1}\end{pmatrix}$，故 $\begin{pmatrix}F_{n+1}\\F_n\end{pmatrix}=A^{n-1}\begin{pmatrix}F_2\\F_1\end{pmatrix}=A^{n}\begin{pmatrix}F_1\\F_0\end{pmatrix}$（$F_0=0$）。归纳得 $A^n=\begin{pmatrix}F_{n+1}&F_n\\F_n&F_{n-1}\end{pmatrix}$：$A^2=\begin{pmatrix}2&1\\1&1\end{pmatrix}=\begin{pmatrix}F_3&F_2\\F_2&F_1\end{pmatrix}$。故 $A^{10}=\begin{pmatrix}F_{11}&F_{10}\\F_{10}&F_9\end{pmatrix}$。直接递推：$1,1,2,3,5,8,13,21,34,55$，$F_{10}=55$。特征值：$\chi(\lambda)=\lambda^2-\lambda-1=0$，$\lambda_1=\dfrac{1+\sqrt5}{2}=\varphi\approx 1.618$，$\lambda_2=\dfrac{1-\sqrt5}{2}$，故 $F_n\sim\dfrac{\varphi^n}{\sqrt5}$，$\dfrac{F_{n+1}}{F_n}\to\varphi$。

**答案原文**

$F_{10}=55$；增长比趋于 $\dfrac{1+\sqrt5}{2}$

## 408. test-linalg-013

内容 SHA256：`5854b2096135a388e6aac006f607548345569973361313ae27d882b9a94feb4b`。

来源：data/v2/test/dataset_test.jsonl，第 108 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $n$ 阶三对角行列式 $D_n=\begin{vmatrix}1&1&0&\cdots&0\\1&1&1&\cdots&0\\0&1&1&\cdots&0\\\vdots&&&\ddots&\vdots\\0&0&\cdots&1&1\end{vmatrix}$ 的前 6 项，并发现其周期规律（矩阵元素满足 $a_{ii}=a_{i,i+1}=a_{i+1,i}=1$，其余为 0）。

**过程**

按第一行展开：$D_n=D_{n-1}-D_{n-2}$（第二项的符号来自展开：$1\cdot D_{n-1}-1\cdot\begin{vmatrix}1&1&0&\cdots\\0&1&1&\cdots\\\vdots\end{vmatrix}$，该子式按第一列展开为 $D_{n-2}$）。$D_1=1$，$D_2=\begin{vmatrix}1&1\\1&1\end{vmatrix}=0$。递推：$D_3=D_2-D_1=-1$，$D_4=D_3-D_2=-1$，$D_5=D_4-D_3=0$，$D_6=D_5-D_4=1$。序列 $1,0,-1,-1,0,1$ 以周期 6 循环（$D_n=D_{n-6}$，因 $D_{n+6}=D_{n+5}-D_{n+4}=\cdots=D_n$ 由递推的线性性质）。

**答案原文**

$D_1,\dots,D_6=1,0,-1,-1,0,1$，周期为 6

## 409. test-linalg-014

内容 SHA256：`980658e96cafb35d6ccb45d07caef5bde5638af318d8d3630ff92bccf821bfaa`。

来源：data/v2/test/dataset_test.jsonl，第 109 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $A=\begin{pmatrix}1&0&1\\0&2&0\\1&0&2\end{pmatrix}$ 的逆矩阵。

**过程**

$\det A=1\cdot(2\cdot 2-0\cdot 0)-0+1\cdot(0\cdot 0-2\cdot 1)=4-2=2$。代数余子式：$C_{11}=\begin{vmatrix}2&0\\0&2\end{vmatrix}=4$，$C_{12}=-\begin{vmatrix}0&0\\1&2\end{vmatrix}=0$，$C_{13}=\begin{vmatrix}0&2\\1&0\end{vmatrix}=-2$，$C_{21}=-\begin{vmatrix}0&1\\0&2\end{vmatrix}=0$，$C_{22}=\begin{vmatrix}1&1\\1&2\end{vmatrix}=1$，$C_{23}=-\begin{vmatrix}1&0\\1&0\end{vmatrix}=0$，$C_{31}=\begin{vmatrix}0&1\\2&0\end{vmatrix}=-2$，$C_{32}=-\begin{vmatrix}1&1\\0&0\end{vmatrix}=0$，$C_{33}=\begin{vmatrix}1&0\\0&2\end{vmatrix}=2$。$A^*=C^T=\begin{pmatrix}4&0&-2\\0&1&0\\-2&0&2\end{pmatrix}$。$A^{-1}=\dfrac{A^*}{2}=\begin{pmatrix}2&0&-1\\0&\frac{1}{2}&0\\-1&0&1\end{pmatrix}$。验证：$AA^{-1}=I$。

**答案原文**

$\begin{pmatrix}2&0&-1\\0&\frac{1}{2}&0\\-1&0&1\end{pmatrix}$

## 410. test-linalg-015

内容 SHA256：`95c4fed48f7f68f6534c8ca54ec1b60dc56023e1442eff94406a1a4d0daa495e`。

来源：data/v2/test/dataset_test.jsonl，第 110 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $\lambda$ 使向量组 $(1,\lambda,\lambda)$、$(\lambda,1,\lambda)$、$(\lambda,\lambda,1)$ 线性相关。

**过程**

三向量为行的行列式 $D=\begin{vmatrix}1&\lambda&\lambda\\\lambda&1&\lambda\\\lambda&\lambda&1\end{vmatrix}$。该矩阵 $=(1-\lambda)I+\lambda J$（$J$ 全 1 矩阵），特征值为 $(1-\lambda)+3\lambda=1+2\lambda$（一重）与 $1-\lambda$（二重），故 $D=(1+2\lambda)(1-\lambda)^2$。线性相关 $\iff D=0\iff\lambda=1$ 或 $\lambda=-\dfrac{1}{2}$。

**答案原文**

$\lambda=1$ 或 $\lambda=-\dfrac{1}{2}$

## 411. test-linalg-016

内容 SHA256：`f4424b7227a094f35ac68d6936b53f76f080db1140ec1a8107233b8b23c96b8f`。

来源：data/v2/test/dataset_test.jsonl，第 111 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $W_1=\{(x,y,z):x+y+z=0\}$，$W_2=\{(x,y,z):x=y=z\}$。求 $\dim(W_1\cap W_2)$ 与 $\dim(W_1+W_2)$，并判断是否为直和。

**过程**

$W_1$ 是平面（维数 2），$W_2$ 是直线（维数 1，方向 $(1,1,1)$）。$W_1\cap W_2$：$(t,t,t)\in W_1$ 需 $3t=0$，即 $t=0$，故 $W_1\cap W_2=\{0\}$，$\dim=0$。由维数公式 $\dim(W_1+W_2)=2+1-0=3$，且 $W_1\cap W_2=\{0\}$，故为直和，$W_1\oplus W_2=\mathbb R^3$。

**答案原文**

$\dim(W_1\cap W_2)=0$；$\dim(W_1+W_2)=3$；直和

## 412. test-linalg-017

内容 SHA256：`ab1a7ca44f2937b5af5e8f6d6351911da1097b8d531890f93286cb3d79884806`。

来源：data/v2/test/dataset_test.jsonl，第 112 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

验证 $\langle A,B\rangle=\operatorname{tr}(A^TB)$ 是 $2\times 2$ 实矩阵空间上的内积，并求 $A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$ 的范数。

**过程**

设 $A=(a_{ij})$、$B=(b_{ij})$，$\operatorname{tr}(A^TB)=\displaystyle\sum_{i,j}a_{ij}b_{ij}$，即把矩阵按分量展开成 4 维向量的标准点积，故满足内积公理（对称、双线性、正定性：$\langle A,A\rangle=\sum a_{ij}^2\ge 0$ 且等号仅当 $A=0$）。$\|A\|=\sqrt{\langle A,A\rangle}=\sqrt{1+4+9+16}=\sqrt{30}$。

**答案原文**

证毕；$\|A\|=\sqrt{30}$

## 413. test-linalg-018

内容 SHA256：`7387e5112872de6e77cb5c142935a47b331714845f1d36943ef6efc75732c99f`。

来源：data/v2/test/dataset_test.jsonl，第 113 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $A=\begin{pmatrix}1&0\\0&0\end{pmatrix}$。验证 $A^2=A$，求 $A$ 的特征值，并说明幂等矩阵满足 $\operatorname{rank}A=\operatorname{tr}A$。

**过程**

$A^2=\begin{pmatrix}1&0\\0&0\end{pmatrix}\begin{pmatrix}1&0\\0&0\end{pmatrix}=\begin{pmatrix}1&0\\0&0\end{pmatrix}=A$。特征值：$|\lambda I-A|=\lambda(\lambda-1)$，特征值 $1,0$。$\operatorname{rank}A=1$，$\operatorname{tr}A=1$，相等。一般地，幂等矩阵 $A^2=A$ 的特征值满足 $\lambda^2=\lambda$，即 $\lambda\in\{0,1\}$，且 $A$ 可对角化（最小多项式整除 $\lambda(\lambda-1)$，无重根；本题给定矩阵的最小多项式恰为 $\lambda(\lambda-1)$），非零特征值个数 $=$ 秩，特征值之和 $=$ 迹，故 $\operatorname{rank}A=\operatorname{tr}A$。

**答案原文**

证毕；特征值 $1,0$；$\operatorname{rank}A=\operatorname{tr}A=1$

## 414. test-linalg-019

内容 SHA256：`e7ccf036ac4c3e723520acffdf52bfd3571c8c8000c8440ea84cfd87e496986e`。

来源：data/v2/test/dataset_test.jsonl，第 114 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求所有与 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 可交换的 $2\times 2$ 实矩阵 $X$。

**过程**

设 $X=\begin{pmatrix}a&b\\c&d\end{pmatrix}$。$AX=\begin{pmatrix}a+c&b+d\\c&d\end{pmatrix}$，$XA=\begin{pmatrix}a&a+b\\c&c+d\end{pmatrix}$。可交换要求两矩阵相等：$a+c=a$（即 $c=0$），$b+d=a+b$（即 $a=d$），$d=c+d$（即 $c=0$，重复）。故 $X=\begin{pmatrix}a&b\\0&a\end{pmatrix}=aI+bN$（$N=\begin{pmatrix}0&1\\0&0\end{pmatrix}$），即与 $A$ 可交换的矩阵恰为 $A$ 的多项式 $aI+bN$。

**答案原文**

$X=\begin{pmatrix}a&b\\0&a\end{pmatrix}$（$a,b\in\mathbb R$）

## 415. test-linalg-020

内容 SHA256：`0f8e6e14f37e8c4a92cad14caba3a524509f5c21afadc3d1b60d2a5c50667da2`。

来源：data/v2/test/dataset_test.jsonl，第 115 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $f(x)=x^4-4x^2+3$ 除以 $x^2-2x$ 的余式。

**过程**

设余式为 $ax+b$（除式二次，余式次数 $<2$）：$f(x)=(x^2-2x)q(x)+ax+b$。取 $x=0$：$f(0)=3=b$。取 $x=2$：$f(2)=16-16+3=3=2a+b$，故 $2a+3=3$，$a=0$。余式为 $3$。验证（长除法）：$x^4-4x^2+3=(x^2-2x)(x^2+2x)+3$（因 $(x^2-2x)(x^2+2x)=x^4-4x^2$）。

**答案原文**

$3$

## 416. test-linalg-021

内容 SHA256：`c4f142ff169143e3d6b46097e0575265ee1187a937cd40e2c3886c3d2e1d4426`。

来源：data/v2/test/dataset_test.jsonl，第 116 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $A=\begin{pmatrix}\cos\theta&\sin\theta\\\sin\theta&-\cos\theta\end{pmatrix}$。证明 $A$ 是正交矩阵，求其特征值，并说明其几何意义。

**过程**

$A^TA=\begin{pmatrix}\cos\theta&\sin\theta\\\sin\theta&-\cos\theta\end{pmatrix}\begin{pmatrix}\cos\theta&\sin\theta\\\sin\theta&-\cos\theta\end{pmatrix}=\begin{pmatrix}\cos^2\theta+\sin^2\theta&\cos\theta\sin\theta-\sin\theta\cos\theta\\\sin\theta\cos\theta-\cos\theta\sin\theta&\sin^2\theta+\cos^2\theta\end{pmatrix}=I$，故 $A$ 正交，且 $\det A=-\cos^2\theta-\sin^2\theta=-1$。特征方程 $\lambda^2-1=0$（迹为 0），特征值 $\pm 1$。特征值 $1$ 的特征方向为 $\left(\cos\dfrac{\theta}{2},\sin\dfrac{\theta}{2}\right)$（关于此方向的直线反射），$-1$ 的特征方向与之垂直。几何上 $A$ 是关于过原点、方向为 $\left(\cos\dfrac{\theta}{2},\sin\dfrac{\theta}{2}\right)$ 的直线的镜面反射；该参数化覆盖所有轴方向，包括 $\theta=(2k+1)\pi$ 时的竖直轴 $x=0$（此时 $\tan\dfrac{\theta}{2}$ 不存在，不能用斜截式表示）。

**答案原文**

证毕；特征值 $\pm 1$；关于过原点、方向 $\left(\cos\dfrac{\theta}{2},\sin\dfrac{\theta}{2}\right)$ 的直线的反射（$\theta=(2k+1)\pi$ 时为竖直轴 $x=0$）

## 417. test-linalg-022

内容 SHA256：`f943a55140f8b4250c938c1d04efe7447a2bfd5753d107d885984ab51e81894a`。

来源：data/v2/test/dataset_test.jsonl，第 117 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求正定矩阵 $A=\begin{pmatrix}4&2\\2&3\end{pmatrix}$ 的 Cholesky 分解 $A=LL^T$（$L$ 为下三角）。

**过程**

设 $L=\begin{pmatrix}l_{11}&0\\l_{21}&l_{22}\end{pmatrix}$。$LL^T=\begin{pmatrix}l_{11}^2&l_{11}l_{21}\\l_{11}l_{21}&l_{21}^2+l_{22}^2\end{pmatrix}=\begin{pmatrix}4&2\\2&3\end{pmatrix}$。解得 $l_{11}=2$（取正），$l_{21}=\dfrac{2}{2}=1$，$l_{22}^2=3-1=2$，$l_{22}=\sqrt2$。故 $L=\begin{pmatrix}2&0\\1&\sqrt2\end{pmatrix}$。验证：$LL^T=\begin{pmatrix}4&2\\2&3\end{pmatrix}$。

**答案原文**

$L=\begin{pmatrix}2&0\\1&\sqrt2\end{pmatrix}$

## 418. test-linalg-023

内容 SHA256：`fe508ce3e17940400c64cf0805d5bd6dda1a219e8464bc0e65954e3c545084e0`。

来源：data/v2/test/dataset_test.jsonl，第 118 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

用矩阵方法解微分方程组 $\begin{cases}x'=3x+y\\y'=x+3y\end{cases}$ 的通解。

**过程**

系数矩阵 $A=\begin{pmatrix}3&1\\1&3\end{pmatrix}$。特征方程 $(\lambda-3)^2-1=0$，$\lambda=4,2$，特征向量 $(1,1)^T$、$(1,-1)^T$。通解 $\begin{pmatrix}x\\y\end{pmatrix}=c_1e^{4t}\begin{pmatrix}1\\1\end{pmatrix}+c_2e^{2t}\begin{pmatrix}1\\-1\end{pmatrix}$，即 $x=c_1e^{4t}+c_2e^{2t}$，$y=c_1e^{4t}-c_2e^{2t}$。验证：$x'=4c_1e^{4t}+2c_2e^{2t}=3x+y$，$y'=4c_1e^{4t}-2c_2e^{2t}=x+3y$。

**答案原文**

$x=c_1e^{4t}+c_2e^{2t}$；$y=c_1e^{4t}-c_2e^{2t}$

## 419. test-linalg-024

内容 SHA256：`6c44dd08e8dcf02cea5cd5fe018b6b751a4cf56ebaf57bf93a6b15649c9eae32`。

来源：data/v2/test/dataset_test.jsonl，第 119 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $t$ 使三点 $(1,2)$、$(2,4)$、$(t,6)$ 共线。

**过程**

共线条件：$\begin{vmatrix}1&2&1\\2&4&1\\t&6&1\end{vmatrix}=0$。按第一行展开：$1\cdot(4\cdot 1-1\cdot 6)-2\cdot(2\cdot 1-1\cdot t)+1\cdot(2\cdot 6-4\cdot t)=1\cdot(-2)-2\cdot(2-t)+1\cdot(12-4t)=-2-4+2t+12-4t=6-2t=0$，故 $t=3$。（或用斜率：前两点连线 $y=2x$，$(t,6)$ 在直线上需 $6=2t$，$t=3$。）

**答案原文**

$t=3$

## 420. test-linalg-025

内容 SHA256：`1fc71cc6730e4dbc79ab325f875b6d3745711a701a7838b00ccfc4f35df027dc`。

来源：data/v2/test/dataset_test.jsonl，第 120 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$ 的谱分解 $A=\lambda_1u_1u_1^T+\lambda_2u_2u_2^T$。

**过程**

特征值 $\lambda_1=3$、$\lambda_2=-1$（test-linalg-008），单位特征向量 $u_1=\dfrac{1}{\sqrt2}(1,1)^T$、$u_2=\dfrac{1}{\sqrt2}(1,-1)^T$。$u_1u_1^T=\dfrac{1}{2}\begin{pmatrix}1&1\\1&1\end{pmatrix}$，$u_2u_2^T=\dfrac{1}{2}\begin{pmatrix}1&-1\\-1&1\end{pmatrix}$。谱分解 $A=3u_1u_1^T+(-1)u_2u_2^T=\dfrac{3}{2}\begin{pmatrix}1&1\\1&1\end{pmatrix}-\dfrac{1}{2}\begin{pmatrix}1&-1\\-1&1\end{pmatrix}=\begin{pmatrix}1&2\\2&1\end{pmatrix}$。

**答案原文**

$A=3u_1u_1^T-u_2u_2^T$（$u_1=\dfrac{(1,1)^T}{\sqrt2}$，$u_2=\dfrac{(1,-1)^T}{\sqrt2}$）

## 421. test-linalg-026

内容 SHA256：`6cf4aefe64ce44fac3bfbef51506516e0037a8a4e27e3b3d230814363d668e83`。

来源：data/v2/test/dataset_test.jsonl，第 121 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

将二次型 $f=3x^2+4xy+6y^2$ 用配方法化为标准形，并写出相应的可逆线性替换。

**过程**

$f=3\left(x^2+\dfrac{4}{3}xy\right)+6y^2=3\left(x+\dfrac{2}{3}y\right)^2-\dfrac{4}{3}y^2+6y^2=3\left(x+\dfrac{2}{3}y\right)^2+\dfrac{14}{3}y^2$。令 $u=x+\dfrac{2}{3}y$、$v=y$（可逆：$x=u-\dfrac{2}{3}v$、$y=v$），标准形为 $3u^2+\dfrac{14}{3}v^2$。矩阵形式：$A=\begin{pmatrix}3&2\\2&6\end{pmatrix}$，$C=\begin{pmatrix}1&-\frac{2}{3}\\0&1\end{pmatrix}$，验证 $C^TAC=\begin{pmatrix}3&0\\0&\frac{14}{3}\end{pmatrix}$（$AC=\begin{pmatrix}3&0\\2&\frac{14}{3}\end{pmatrix}$，$C^T(AC)=\begin{pmatrix}3&0\\0&\frac{14}{3}\end{pmatrix}$）。

**答案原文**

标准形 $3u^2+\dfrac{14}{3}v^2$；替换 $\begin{cases}u=x+\frac{2}{3}y\\v=y\end{cases}$

## 422. test-linalg-027

内容 SHA256：`464169fd564bc8c1522dd0e34a24e33919ed2c121528ddb94bdae2b7708118bd`。

来源：data/v2/test/dataset_test.jsonl，第 122 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

解微分方程组 $\begin{cases}x'=2x+y\\y'=2y\end{cases}$ 的通解。

**过程**

系数矩阵 $A=\begin{pmatrix}2&1\\0&2\end{pmatrix}=J_2(2)$。先解 $y'=2y$：$y=c_2e^{2t}$。代入 $x'=2x+c_2e^{2t}$：$x=e^{2t}\left(c_1+c_2t\right)$（常数变易，或观察特解 $x_p=c_2te^{2t}$：$x_p'-2x_p=c_2e^{2t}(1+2t)-2c_2te^{2t}=c_2e^{2t}$ 恰为强迫项）。验证：$x'=2e^{2t}(c_1+c_2t)+c_2e^{2t}=2x+y$。

**答案原文**

$x=e^{2t}(c_1+c_2t)$；$y=c_2e^{2t}$

## 423. test-linalg-028

内容 SHA256：`e1141eed57d200fa142692ee34ba587f3336889a4e988e86959b44846f2e4f38`。

来源：data/v2/test/dataset_test.jsonl，第 123 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $A=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$ 的特征值，并说明它没有实特征向量的几何原因。

**过程**

$|\lambda I-A|=\begin{vmatrix}\lambda&1\\-1&\lambda\end{vmatrix}=\lambda^2+1=0$，特征值 $\lambda=\pm i$（一对共轭虚数）。几何上 $A$ 是旋转 $90^\circ$（逆时针），除零向量外任何实向量旋转后都不与原方向平行，故没有（一维的）实特征空间；只有把向量空间扩充到复数域，才有特征方向。

**答案原文**

特征值 $\pm i$；无实特征向量（旋转 $90^\circ$）

## 424. test-linalg-029

内容 SHA256：`76a223f31b67fe3b78ccb799660b26d63a1d2caa4a5c7461a813ce5cf9b63b6e`。

来源：data/v2/test/dataset_test.jsonl，第 124 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $A=\begin{pmatrix}1&1&0\\0&1&0\\0&0&1\end{pmatrix}$ 的最小多项式与若尔当标准形。

**过程**

特征多项式 $(\lambda-1)^3$。$A-I=\begin{pmatrix}0&1&0\\0&0&0\\0&0&0\end{pmatrix}=:N$，$N\ne 0$ 且 $N^2=0$，故最小多项式 $m(\lambda)=(\lambda-1)^2$。秩判块结构：$\operatorname{rank}(A-I)=1$，特征值 $1$ 的若尔当块个数 $=3-1=2$，最大块尺寸由 $m(\lambda)$ 的因子幂给出为 2，故标准形为 $\begin{pmatrix}1&1&0\\0&1&0\\0&0&1\end{pmatrix}=A$ 本身（即 $J_2(1)\oplus J_1(1)$）。

**答案原文**

最小多项式 $(\lambda-1)^2$；若尔当标准形 $\begin{pmatrix}1&1&0\\0&1&0\\0&0&1\end{pmatrix}$

## 425. test-linalg-030

内容 SHA256：`253c69731f8d0b0609efe58c24a018a639865998f19a73b6a180b57ee8357f41`。

来源：data/v2/test/dataset_test.jsonl，第 125 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $\mathbb R^3$ 上的线性泛函 $f$，使其满足 $f(1,1,1)=3$、$f(1,0,0)=1$、$f(0,1,0)=1$。

**过程**

设 $f(x,y,z)=ax+by+cz$。条件：$f(1,0,0)=a=1$；$f(0,1,0)=b=1$；$f(1,1,1)=a+b+c=3$，故 $c=3-1-1=1$。得 $f(x,y,z)=x+y+z$。

**答案原文**

$f(x,y,z)=x+y+z$

## 426. test-linalg-031

内容 SHA256：`f7ebc7985289154261479b3f7fb2f823b56c022576dd30a47faee70aa1c33936`。

来源：data/v2/test/dataset_test.jsonl，第 126 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求 $\lambda$ 使向量组 $(1,2,3)$、$(2,\lambda,1)$、$(3,1,2)$ 线性相关。

**过程**

行列式 $D=\begin{vmatrix}1&2&3\\2&\lambda&1\\3&1&2\end{vmatrix}=1\cdot(\lambda\cdot 2-1\cdot 1)-2\cdot(2\cdot 2-1\cdot 3)+3\cdot(2\cdot 1-\lambda\cdot 3)=(2\lambda-1)-2\cdot 1+3\cdot(2-3\lambda)=2\lambda-1-2+6-9\lambda=3-7\lambda$。线性相关 $\iff D=0\iff\lambda=\dfrac{3}{7}$。

**答案原文**

$\lambda=\dfrac{3}{7}$

## 427. test-linalg-032

内容 SHA256：`03cf5e26f6cfde2c14bbd846eedef7247dcdc3ad736439e9a1e6c8c61c3bc5a4`。

来源：data/v2/test/dataset_test.jsonl，第 127 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

证明 $\operatorname{rank}(A+B)\le\operatorname{rank}A+\operatorname{rank}B$，并举出等号成立的例子。

**过程**

列空间 $\operatorname{col}(A+B)\subseteq\operatorname{col}(A)+\operatorname{col}(B)$（$A+B$ 的每列都是 $A$ 与 $B$ 对应列之和，落在两列空间的和中）。故 $\operatorname{rank}(A+B)=\dim\operatorname{col}(A+B)\le\dim(\operatorname{col}(A)+\operatorname{col}(B))\le\dim\operatorname{col}(A)+\dim\operatorname{col}(B)=\operatorname{rank}A+\operatorname{rank}B$。等号例子：$A=\begin{pmatrix}1&0\\0&0\end{pmatrix}$、$B=\begin{pmatrix}0&0\\0&1\end{pmatrix}$，$\operatorname{rank}A=\operatorname{rank}B=1$，$A+B=I$，$\operatorname{rank}(A+B)=2=1+1$。

**答案原文**

证毕；等号例 $A=\begin{pmatrix}1&0\\0&0\end{pmatrix}$、$B=\begin{pmatrix}0&0\\0&1\end{pmatrix}$

## 428. test-linalg-033

内容 SHA256：`2ff9951ac7564c2d8f9c2bb82a4d48b7441ddfd4c33ade5c20d9e96a9a0ec3f3`。

来源：data/v2/test/dataset_test.jsonl，第 128 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

证明：若 $A^2=A$，则 $A$ 的特征值只能是 $0$ 或 $1$。

**过程**

设 $Av=\lambda v$（$v\ne 0$）。则 $A^2v=A(Av)=A(\lambda v)=\lambda Av=\lambda^2v$。由 $A^2=A$ 得 $\lambda^2v=\lambda v$，即 $(\lambda^2-\lambda)v=0$。因 $v\ne 0$，$\lambda^2-\lambda=0$，$\lambda\in\{0,1\}$。

**答案原文**

证毕

## 429. test-linalg-034

内容 SHA256：`0ab1264b7c40bcba2808962547ac5d87c88ae89a2ea737d5876db89d8f8129f2`。

来源：data/v2/test/dataset_test.jsonl，第 129 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

判断二次曲面 $3x^2+2xy+3y^2+z^2=1$ 的类型。

**过程**

二次项矩阵 $A=\begin{pmatrix}3&1&0\\1&3&0\\0&0&1\end{pmatrix}$。$2\times 2$ 块 $\begin{pmatrix}3&1\\1&3\end{pmatrix}$ 的特征方程 $(\lambda-3)^2-1=0$，特征值 $4,2$；第三个特征值为 $1$。全为正，故曲面为椭球面：$\dfrac{u^2}{1/4}+\dfrac{v^2}{1/2}+z^2=1$（主轴沿特征方向，半轴 $\dfrac{1}{2},\dfrac{1}{\sqrt2},1$）。

**答案原文**

椭球面（特征值 $4,2,1$ 全正）

## 430. test-linalg-035

内容 SHA256：`61925328cff4abf56a892e90467b81a276786b95fe5d7e3f943d13dc1e20b7e8`。

来源：data/v2/test/dataset_test.jsonl，第 130 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

把 $D(x)=\begin{vmatrix}1&x&x^2\\1&2&4\\1&3&9\end{vmatrix}$ 看成 $x$ 的多项式并因式分解。

**过程**

这是范德蒙德行列式（三个点的范德蒙德型），$D(x)=(2-x)(3-x)(3-2)=(2-x)(3-x)=x^2-5x+6=(x-2)(x-3)$。验证：$x=2$ 时第一、二行相同，$D=0$；$x=3$ 时第一、三行相同，$D=0$；$x=0$ 时 $D=\begin{vmatrix}1&0&0\\1&2&4\\1&3&9\end{vmatrix}=18-12=6$，与 $(0-2)(0-3)=6$ 一致。

**答案原文**

$(x-2)(x-3)$

## 431. test-linalg-036

内容 SHA256：`2ba0b13ee032f78abfd7749c9d5c011b49ec935d3e503b49749c084506f1fdbe`。

来源：data/v2/test/dataset_test.jsonl，第 131 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求三类初等矩阵的行列式：交换两行、某行乘以 $k$（$k\ne 0$）、某行加到另一行（三类变换均涉及两不同行）。

**过程**

交换两行的初等矩阵 $P_{ij}$：由单位矩阵交换两行得到，$\det P_{ij}=-1$（一次对换改变符号）。第 $i$ 行乘 $k$ 的初等矩阵 $D_i(k)$：对角线第 $i$ 元为 $k$，$\det D_i(k)=k$。第 $i$ 行加到第 $j$ 行的初等矩阵 $E_{ij}$：下（上）三角且对角线全 1，$\det E_{ij}=1$。相应地对任意方阵 $B$：$\det(P_{ij}B)=-\det B$，$\det(D_i(k)B)=k\det B$，$\det(E_{ij}B)=\det B$。

**答案原文**

$-1$；$k$；$1$

## 432. test-linalg-037

内容 SHA256：`aa33157d87a026ec4d7e17d8d97f070aac47be15b03e51aa12bc64cc51fa4a95`。

来源：data/v2/test/dataset_test.jsonl，第 132 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求微分算子 $T(f)=f'$ 在多项式空间 $P_2$（次数 $\le 2$，基 $1,x,x^2$）下的矩阵。

**过程**

对基作用：$T(1)=0=0\cdot 1+0\cdot x+0\cdot x^2$；$T(x)=1=1\cdot 1+0\cdot x+0\cdot x^2$；$T(x^2)=2x=0\cdot 1+2\cdot x+0\cdot x^2$。坐标列为 $(0,0,0)^T$、$(1,0,0)^T$、$(0,2,0)^T$，故矩阵 $\begin{pmatrix}0&1&0\\0&0&2\\0&0&0\end{pmatrix}$。验证：对 $f=a+bx+cx^2$（坐标 $(a,b,c)^T$），$Tf=b+2cx$，坐标 $(b,2c,0)^T$，矩阵乘法 $\begin{pmatrix}0&1&0\\0&0&2\\0&0&0\end{pmatrix}\begin{pmatrix}a\\b\\c\end{pmatrix}=\begin{pmatrix}b\\2c\\0\end{pmatrix}$，一致。

**答案原文**

$\begin{pmatrix}0&1&0\\0&0&2\\0&0&0\end{pmatrix}$

## 433. test-linalg-038

内容 SHA256：`3cfeac479c092d987f71f9651c816cd1185d22b6835296dee4fb8dcf45a3061e`。

来源：data/v2/test/dataset_test.jsonl，第 133 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

证明：若 $A$ 可逆，则 $\operatorname{rank}(A^2)=\operatorname{rank}A$；并举出 $A$ 不可逆时该结论不成立的例子。

**过程**

$A$ 可逆时 $A^2$ 也可逆（$\det(A^2)=(\det A)^2\ne 0$），两者秩都等于 $n$（满秩），故相等。不可逆的反例：$A=\begin{pmatrix}0&1\\0&0\end{pmatrix}$，$\operatorname{rank}A=1$，$A^2=0$，$\operatorname{rank}(A^2)=0\ne 1$。

**答案原文**

证毕；反例 $A=\begin{pmatrix}0&1\\0&0\end{pmatrix}$

## 434. test-linalg-039

内容 SHA256：`387d7ec09567bb91a28655b3d3949d4ce7de035a1dc3a359287b3aaab8148f7e`。

来源：data/v2/test/dataset_test.jsonl，第 134 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求二次型 $f=3x^2-2y^2-z^2+4xy$ 的正负惯性指数，并判断等值曲面 $f=1$ 的类型。

**过程**

矩阵 $A=\begin{pmatrix}3&2&0\\2&-2&0\\0&0&-1\end{pmatrix}$。$2\times 2$ 块 $\begin{pmatrix}3&2\\2&-2\end{pmatrix}$：迹 $1$、行列式 $-10$，特征方程 $\lambda^2-\lambda-10=0$，特征值 $\dfrac{1\pm\sqrt{41}}{2}$，即一正一负；第三个特征值 $-1$。故正惯性指数 $1$、负惯性指数 $2$（符号差 $-1$）。等值曲面 $f=1$ 为双叶双曲面（一个正方向、两个负方向）。

**答案原文**

正惯性指数 $1$、负惯性指数 $2$；$f=1$ 为双叶双曲面（$f=-1$ 为单叶双曲面，$f=0$ 为锥面）

## 435. test-linalg-040

内容 SHA256：`f0b6f9ffec690620cb09700cee2a7e56191d3ee3543b071aabf50c207c085b39`。

来源：data/v2/test/dataset_test.jsonl，第 135 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求四顶点圈 $C_4$ 的邻接矩阵及其特征值。

**过程**

$C_4$ 的邻接矩阵 $A=\begin{pmatrix}0&1&0&1\\1&0&1&0\\0&1&0&1\\1&0&1&0\end{pmatrix}$。解方程 $Av=\lambda v$：由对称性，特征向量可取 $(1,1,1,1)^T$（$A(1,1,1,1)^T=(2,2,2,2)^T=2(1,1,1,1)^T$，特征值 $2$）、$(1,-1,1,-1)^T$（验证 $A(1,-1,1,-1)^T=(-2,2,-2,2)^T=-2(1,-1,1,-1)^T$，特征值 $-2$）、$(1,0,-1,0)^T$（$A(1,0,-1,0)^T=(0,0,0,0)^T$，特征值 $0$）、$(0,1,0,-1)^T$（同样为 $0$）。故特征值为 $2,0,0,-2$（图是二部图，谱关于 0 对称）。

**答案原文**

邻接矩阵 $A=\begin{pmatrix}0&1&0&1\\1&0&1&0\\0&1&0&1\\1&0&1&0\end{pmatrix}$；特征值 $2,0,0,-2$

## 436. test-x-001

内容 SHA256：`54f5db7a7fefbaf436d973bde21afb3ee5e4004f6de350fdbf25b89bbb79621d`。

来源：data/v2/test/dataset_test.jsonl，第 136 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $X$ 服从参数 $p=\dfrac{1}{2}$ 的几何分布（抛硬币直到正面）。求 $P(X$ 为偶数$)$ 的精确值。

**过程**

$P(X=k)=\left(\dfrac{1}{2}\right)^k$。$P(X$ 为偶数$)=\displaystyle\sum_{k=1}^{\infty}P(X=2k)=\sum_{k=1}^{\infty}\left(\dfrac{1}{2}\right)^{2k}=\sum_{k=1}^{\infty}\left(\dfrac{1}{4}\right)^k=\dfrac{1/4}{1-1/4}=\dfrac{1}{3}$。

**答案原文**

$\dfrac{1}{3}$

## 437. test-x-002

内容 SHA256：`3db4f4d2274a59865742db08c8d84c528c7935571e7700cbd3753eebfde19967`。

来源：data/v2/test/dataset_test.jsonl，第 137 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $X\sim U(0,1)$，求 $Y=\sqrt{X}$ 的密度与 $E[Y]$。

**过程**

$y=\sqrt{x}$ 严格递增，反函数 $x=y^2$（$0<y<1$），$\left|\dfrac{dx}{dy}\right|=2y$。$f_Y(y)=f_X(y^2)\cdot 2y=2y$（$0<y<1$）。$E[Y]=\displaystyle\int_0^1y\cdot 2y\,dy=\dfrac{2}{3}$。验证：$E[\sqrt{X}]=\displaystyle\int_0^1\sqrt{x}\,dx=\left[\dfrac{2}{3}x^{3/2}\right]_0^1=\dfrac{2}{3}$，一致。

**答案原文**

$f_Y(y)=2y$（$0<y<1$）；$E[Y]=\dfrac{2}{3}$

## 438. test-x-003

内容 SHA256：`a097afdb57dcc51b13777605a27dce517e3a99ab30b0b874f10f2e247baa5ed6`。

来源：data/v2/test/dataset_test.jsonl，第 138 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $A$ 为常矩阵。证明 $\dfrac{d}{dt}e^{tA}=Ae^{tA}$。

**过程**

$e^{tA}=\displaystyle\sum_{k=0}^{\infty}\dfrac{t^kA^k}{k!}$（对任意 $t$ 收敛）。逐项求导：$\dfrac{d}{dt}e^{tA}=\displaystyle\sum_{k=1}^{\infty}\dfrac{kt^{k-1}A^k}{k!}=\sum_{k=1}^{\infty}\dfrac{t^{k-1}A^k}{(k-1)!}=A\sum_{m=0}^{\infty}\dfrac{t^mA^m}{m!}=Ae^{tA}$（$A$ 为常数矩阵，可提出求和号外）。故 $\dfrac{d}{dt}e^{tA}=Ae^{tA}$，即矩阵指数是矩阵微分方程 $X'=AX$、$X(0)=I$ 的解。

**答案原文**

证毕

## 439. test-x-004

内容 SHA256：`5453e577b5a619b8d35a5d3a789cd463f27ddce1cc0d1ee2f1e84358a0b42dd9`。

来源：data/v2/test/dataset_test.jsonl，第 139 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

转移矩阵为 $P$ 的马尔可夫链，稳态分布 $\pi$ 满足 $\pi=\pi P$。说明稳态分布是 $P^T$ 的特征值 $1$ 对应的特征向量，并求 $P=\begin{pmatrix}0.5&0.5\\0.25&0.75\end{pmatrix}$ 的稳态分布。

**过程**

$\pi=\pi P$ 转置得 $P^T\pi^T=\pi^T$，即稳态分布（转置后）是 $P^T$ 的特征值 $1$ 的特征向量（随机矩阵行和为 1，恒有特征值 1）。对给定 $P$：解 $\pi_1=0.5\pi_1+0.25\pi_2$（即 $0.5\pi_1=0.25\pi_2$，$\pi_1=\dfrac{\pi_2}{2}$）与 $\pi_1+\pi_2=1$，得 $\pi=\left(\dfrac{1}{3},\dfrac{2}{3}\right)$。验证：$\left(\dfrac{1}{3},\dfrac{2}{3}\right)P=\left(\dfrac{1}{3},\dfrac{2}{3}\right)$。

**答案原文**

稳态分布 $\left(\dfrac{1}{3},\dfrac{2}{3}\right)$；$\pi^T$ 是 $P^T$ 特征值 $1$ 的特征向量

## 440. test-x-005

内容 SHA256：`4e3f09001a8a70c390c75602e186996e9134909ee6e283269a28c88e69184cd3`。

来源：data/v2/test/dataset_test.jsonl，第 140 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

用长为 $l$ 的围栏围一个矩形区域（一边靠墙不需围栏），求最大面积。

**过程**

设垂直墙的边长为 $x$，则平行墙的边长为 $l-2x$（$0<x<\dfrac{l}{2}$）。面积 $A=x(l-2x)=lx-2x^2$。$A'=l-4x=0$，$x=\dfrac{l}{4}$；$A''=-4<0$，为最大值。$A_{\max}=\dfrac{l}{4}\cdot\left(l-\dfrac{l}{2}\right)=\dfrac{l^2}{8}$。

**答案原文**

$\dfrac{l^2}{8}$（$x=\dfrac{l}{4}$ 时）

## 441. test-x-006

内容 SHA256：`79f1b55b6ea4863af8a4712648e500b916cad6b9881c3fff5066e6d57e77db28`。

来源：data/v2/test/dataset_test.jsonl，第 141 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

Bertrand 悖论：在单位圆中"随机取一条弦"，求弦长大于 $\sqrt3$ 的概率，分别按三种取法计算（随机端点、随机半径中点、随机中点）。

**过程**

弦长 $>\sqrt3\iff$ 弦到圆心的距离 $<\dfrac{1}{2}$（半弦长 $\sqrt{1-d^2}>\dfrac{\sqrt3}{2}\iff d<\dfrac{1}{2}$）。（1）随机端点：两端点在圆周上均匀独立，等价于固定一端后另一端随机，另一端点对应的圆心角 $\theta\in[0,2\pi)$ 均匀。弦长为 $2\sin\dfrac{\theta}{2}$（$\theta\in[0,\pi]$ 时递增、$[\pi,2\pi]$ 时递减），故 $2\sin\dfrac{\theta}{2}>\sqrt3\iff\dfrac{\theta}{2}\in\left(\dfrac{\pi}{3},\dfrac{2\pi}{3}\right)\iff\theta\in\left(\dfrac{2\pi}{3},\dfrac{4\pi}{3}\right)$，有利角长 $\dfrac{4\pi}{3}-\dfrac{2\pi}{3}=\dfrac{2\pi}{3}$，概率 $=\dfrac{2\pi/3}{2\pi}=\dfrac{1}{3}$。（2）随机半径中点：在一条半径上均匀取中点再作垂直弦，弦到圆心距离 $<\dfrac{1}{2}$ 的概率 $=\dfrac{1}{2}$。（3）随机中点：中点在圆内均匀分布，$d<\dfrac{1}{2}$ 对应半径为 $\dfrac{1}{2}$ 的小圆，面积比 $=\dfrac{\pi/4}{\pi}=\dfrac{1}{4}$。三种取法给出三个不同答案，说明"随机"必须先明确概率空间。

**答案原文**

$\dfrac{1}{3}$、$\dfrac{1}{2}$、$\dfrac{1}{4}$（取决于取法）

## 442. test-x-007

内容 SHA256：`c11b6bcc9602ddbd597f6de0660c2074ccb599adcd8995c9a4351d9f5a9a2b95`。

来源：data/v2/test/dataset_test.jsonl，第 142 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

用特征值方法判断二次曲线 $x^2+4xy+y^2=1$ 的类型，并说明主轴方向。

**过程**

矩阵 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$。特征方程 $(\lambda-1)^2-4=0$，特征值 $\lambda_1=3$、$\lambda_2=-1$（一正一负），故曲线为双曲线。特征向量：$\lambda=3$ 对应 $(1,1)^T$（主轴），$\lambda=-1$ 对应 $(1,-1)^T$。正交变换 $u=\dfrac{x+y}{\sqrt2}$、$v=\dfrac{x-y}{\sqrt2}$ 后方程为 $3u^2-v^2=1$，即 $\dfrac{u^2}{1/3}-v^2=1$，是双曲线，实轴沿 $y=x$ 方向。

**答案原文**

双曲线；主轴沿 $y=x$ 与 $y=-x$ 方向，标准形 $3u^2-v^2=1$

## 443. test-x-008

内容 SHA256：`b9159a53438dfbe770188a5d777f71f2c952cf504c11cd728b103e24e32ab1ed`。

来源：data/v2/test/dataset_test.jsonl，第 143 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求由 $y=x^2$ 与 $y=\sqrt{x}$ 围成的区域的面积。

**过程**

交点：$x^2=\sqrt{x}$，即 $x^4=x$，$x(x^3-1)=0$，$x=0$ 或 $x=1$。在 $[0,1]$ 上 $\sqrt{x}\ge x^2$。面积 $S=\displaystyle\int_0^1(\sqrt{x}-x^2)dx=\left[\dfrac{2}{3}x^{3/2}-\dfrac{x^3}{3}\right]_0^1=\dfrac{2}{3}-\dfrac{1}{3}=\dfrac{1}{3}$。

**答案原文**

$\dfrac{1}{3}$

## 444. test-x-009

内容 SHA256：`e56b4a34c8607976f2bb78ecef358953ed26bce593594d58ee26993266adcffe`。

来源：data/v2/test/dataset_test.jsonl，第 144 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设 $X\sim\operatorname{Exp}(1)$。证明 $E[X^n]=n!$。

**过程**

设 $n\in\{0,1,2,\dots\}$。$E[X^n]=\displaystyle\int_0^{\infty}x^ne^{-x}dx$。记 $I_n=\displaystyle\int_0^{\infty}x^ne^{-x}dx$。$I_0=\displaystyle\int_0^{\infty}e^{-x}dx=1$ 单独计算；$n\ge 1$ 时用分部积分（$u=x^n$、$dv=e^{-x}dx$）：$I_n=\left[-x^ne^{-x}\right]_0^{\infty}+n\displaystyle\int_0^{\infty}x^{n-1}e^{-x}dx=nI_{n-1}$（$n\ge 1$ 时边界项 $x^ne^{-x}\big|_0^\infty$ 为 0）。递推得 $I_n=n!$，即 $E[X^n]=n!$（恰为 Γ 函数 $\Gamma(n+1)$）。

**答案原文**

证毕；$E[X^n]=n!$

## 445. test-x-010

内容 SHA256：`a118d15848e73c29bf12c32dd2de6dd093be65bc29d3436521b53661df7b2cf5`。

来源：data/v2/test/dataset_test.jsonl，第 145 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设两随机变量的方差有限且严格为正（$\sigma_1,\sigma_2>0$）。证明协方差矩阵 $\begin{pmatrix}\sigma_1^2&\rho\sigma_1\sigma_2\\\rho\sigma_1\sigma_2&\sigma_2^2\end{pmatrix}$ 正定当且仅当 $|\rho|<1$。

**过程**

顺序主子式：$\sigma_1^2>0$；行列式 $\sigma_1^2\sigma_2^2(1-\rho^2)$。矩阵正定 $\iff$ 两顺序主子式均为正 $\iff 1-\rho^2>0\iff|\rho|<1$。概率解释：相关系数 $|\rho|<1$ 恰是"两个随机变量不几乎必然线性相关"的充要条件，此时协方差矩阵非退化；若某个方差为 0，协方差矩阵必奇异，且相关系数未定义。

**答案原文**

证毕（在 $\sigma_1,\sigma_2>0$ 的前提下，正定 $\iff|\rho|<1$）

## 446. test-x-011

内容 SHA256：`2a862a58967bc46deb733869b897517c73c779d0548856f9b5f8ff0d6d97a22c`。

来源：data/v2/test/dataset_test.jsonl，第 146 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

证明：平面上关于两条过原点直线的（线性）反射的复合是旋转。以关于 $x$ 轴和关于直线 $y=x$ 的两次反射为例，求复合变换矩阵并识别其几何意义。

**过程**

关于 $x$ 轴的反射 $R_1=\begin{pmatrix}1&0\\0&-1\end{pmatrix}$，关于 $y=x$ 的反射 $R_2=\begin{pmatrix}0&1\\1&0\end{pmatrix}$。复合（先 $R_1$ 后 $R_2$）$R_2R_1=\begin{pmatrix}0&1\\1&0\end{pmatrix}\begin{pmatrix}1&0\\0&-1\end{pmatrix}=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$，这是逆时针旋转 $90^\circ$ 的矩阵（$\det=1$）。一般地，两个线性反射矩阵（正交、$\det=-1$）之积是正交矩阵且 $\det=1$，即旋转。注意：对一般的平面镜面反射，两轴相交时复合为绕交点旋转 $2\varphi$（$\varphi$ 为两轴夹角），两轴平行时复合为平移——本题限定线性反射（轴过原点）才恒得旋转。

**答案原文**

复合矩阵 $\begin{pmatrix}0&-1\\1&0\end{pmatrix}$（逆时针旋转 $90^\circ$）

## 447. test-x-012

内容 SHA256：`ffdd2e898b970bc42a5f9cf5e35d2f311c7b0e8281f25f3c37828825faee06f2`。

来源：data/v2/test/dataset_test.jsonl，第 147 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

用级数定义计算矩阵指数 $e^{A}$，其中 $A=\begin{pmatrix}0&\pi\\-\pi&0\end{pmatrix}$。

**过程**

记 $J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}$，则 $A=\pi J$，且 $J^2=\begin{pmatrix}-1&0\\0&-1\end{pmatrix}=-I$。故 $A^2=-\pi^2I$，$A^3=-\pi^3J$，$A^4=\pi^4I$，一般地 $A^{2k}=(-1)^k\pi^{2k}I$，$A^{2k+1}=(-1)^k\pi^{2k+1}J$。$e^{A}=\displaystyle\sum_{k=0}^{\infty}\left[\dfrac{(-1)^k\pi^{2k}}{(2k)!}I+\dfrac{(-1)^k\pi^{2k+1}}{(2k+1)!}J\right]=\cos\pi\cdot I+\sin\pi\cdot J=-I+0\cdot J=\begin{pmatrix}-1&0\\0&-1\end{pmatrix}$（$\cos\pi=-1$，$\sin\pi=0$）。即 $e^{A}=-I$，对应旋转 $\pi$ 角（欧拉公式的矩阵版 $e^{i\pi}=-1$）。

**答案原文**

$e^{A}=\begin{pmatrix}-1&0\\0&-1\end{pmatrix}=-I$

## 448. test-x-013

内容 SHA256：`76bd31c30810702c82fc77c882bab51ddeefe0edf26ccad83ab3968479dba989`。

来源：data/v2/test/dataset_test.jsonl，第 148 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

随机取一个正整数（在 $1$ 到 $N$ 中等可能，$N\to\infty$ 取极限），求它能被 2 或 3 整除的概率。

**过程**

在 $\{1,\dots,N\}$ 中，能被 2 整除的约有 $\dfrac{N}{2}$ 个、能被 3 整除的约 $\dfrac{N}{3}$ 个、能被 6 整除的约 $\dfrac{N}{6}$ 个。由容斥原理，能被 2 或 3 整除的个数约 $\dfrac{N}{2}+\dfrac{N}{3}-\dfrac{N}{6}=\dfrac{2N}{3}$。概率 $=\dfrac{2N/3}{N}=\dfrac{2}{3}$（令 $N\to\infty$，即自然密度）。

**答案原文**

$\dfrac{2}{3}$

## 449. test-x-014

内容 SHA256：`714a8670b0830794678acdd9fe09da28f1c6fc947b825620828df70d99246a63`。

来源：data/v2/test/dataset_test.jsonl，第 149 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

求悬链线 $y=a\cosh\dfrac{x}{a}$（$0\le x\le b$）的弧长，其中 $a,b>0$。

**过程**

$y'=\sinh\dfrac{x}{a}$。弧长 $L=\displaystyle\int_0^b\sqrt{1+\sinh^2\dfrac{x}{a}}\,dx=\int_0^b\cosh\dfrac{x}{a}\,dx=\left[a\sinh\dfrac{x}{a}\right]_0^b=a\sinh\dfrac{b}{a}$（用到 $1+\sinh^2u=\cosh^2u$）。

**答案原文**

$a\sinh\dfrac{b}{a}$

## 450. test-x-015

内容 SHA256：`8e5ef07940ac043155db96f9e2d9e291172fa8a63642712f320af5dc2cb8e608`。

来源：data/v2/test/dataset_test.jsonl，第 150 行；源 SHA256 `d4de0bb6a86ff0aeeb23cfab79a013236cce742f020d980c4db31df76c94fd2a`。

**题干**

设马尔可夫链的转移矩阵 $P=\begin{pmatrix}0.5&0.5\\0.25&0.75\end{pmatrix}$。用对角化求 $P^n$，并求 $n\to\infty$ 时的极限矩阵。

**过程**

特征方程 $|\lambda I-P|=(\lambda-0.5)(\lambda-0.75)-0.125=\lambda^2-1.25\lambda+0.25=0$，判别式 $1.5625-1=0.5625=\left(\dfrac{3}{4}\right)^2$，特征值 $\lambda=\dfrac{1.25\pm 0.75}{2}$，即 $\lambda_1=1$、$\lambda_2=\dfrac{1}{4}$。$\lambda_1=1$ 的特征向量：解 $(P-I)v=0$，即 $\begin{pmatrix}-0.5&0.5\\0.25&-0.25\end{pmatrix}v=0$，得 $v_1=(1,1)^T$。$\lambda_2=\dfrac{1}{4}$ 的特征向量：解 $\left(P-\dfrac{1}{4}I\right)v=0$，即 $\begin{pmatrix}0.25&0.5\\0.25&0.5\end{pmatrix}v=0$，得 $v_2=(2,-1)^T$（验证 $Pv_2=(0.5,-0.25)=\dfrac{1}{4}v_2$）。取 $Q=\begin{pmatrix}1&2\\1&-1\end{pmatrix}$，$\det Q=-3$，$Q^{-1}=-\dfrac{1}{3}\begin{pmatrix}-1&-2\\-1&1\end{pmatrix}=\begin{pmatrix}\frac{1}{3}&\frac{2}{3}\\\frac{1}{3}&-\frac{1}{3}\end{pmatrix}$。则 $P=Q\begin{pmatrix}1&0\\0&\frac{1}{4}\end{pmatrix}Q^{-1}$，$P^n=Q\begin{pmatrix}1&0\\0&4^{-n}\end{pmatrix}Q^{-1}$。令 $n\to\infty$：$4^{-n}\to 0$，故 $P^n\to Q\begin{pmatrix}1&0\\0&0\end{pmatrix}Q^{-1}=\begin{pmatrix}1&2\\1&-1\end{pmatrix}\begin{pmatrix}1&0\\0&0\end{pmatrix}\begin{pmatrix}\frac{1}{3}&\frac{2}{3}\\\frac{1}{3}&-\frac{1}{3}\end{pmatrix}=\begin{pmatrix}1&0\\1&0\end{pmatrix}\begin{pmatrix}\frac{1}{3}&\frac{2}{3}\\\frac{1}{3}&-\frac{1}{3}\end{pmatrix}=\begin{pmatrix}\frac{1}{3}&\frac{2}{3}\\\frac{1}{3}&\frac{2}{3}\end{pmatrix}$。极限矩阵每行均为稳态分布 $\left(\dfrac{1}{3},\dfrac{2}{3}\right)$（与 $\pi=\pi P$ 直接解 $0.5\pi_1=0.25\pi_2$ 即 $\pi_2=2\pi_1$ 的结果一致）。

**答案原文**

$P^n=\dfrac{1}{3}\begin{pmatrix}1+2\cdot4^{-n}&2-2\cdot4^{-n}\\1-4^{-n}&2+4^{-n}\end{pmatrix}$；$\lim_{n\to\infty}P^n=\begin{pmatrix}\frac{1}{3}&\frac{2}{3}\\\frac{1}{3}&\frac{2}{3}\end{pmatrix}$
