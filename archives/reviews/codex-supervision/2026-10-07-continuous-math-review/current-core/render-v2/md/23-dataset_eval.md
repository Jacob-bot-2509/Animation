## eval-calc-001-s1

problem

求极限 $\displaystyle\lim_{x\to 0}\frac{1-\cos x}{x^2}$。

solution

由 $1-\cos x = 2\sin^2\dfrac{x}{2}$，得 $\dfrac{1-\cos x}{x^2}=\dfrac{2\sin^2(x/2)}{x^2}=\dfrac{1}{2}\left(\dfrac{\sin(x/2)}{x/2}\right)^2$。令 $t=x/2\to 0$，利用 $\lim_{t\to 0}\dfrac{\sin t}{t}=1$，故原式 $=\dfrac{1}{2}\cdot 1^2=\dfrac{1}{2}$。

answer

$\dfrac{1}{2}$

scene_spec.objects[0]

单位圆中半角 $x/2$ 的扇形与三角形面积

scene_spec.objects[1]

比值 $\dfrac{\sin(x/2)}{x/2}$ 随 $x\to0$ 逼近 1 的动画

scene_spec.objects[2]

半角恒等式 $1-\cos x=2\sin^2(x/2)$ 的标注

scene_spec.steps[0]

第一步：以半角公式为主线，建立数学分析·极限场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：单位圆中半角 $x/2$ 的扇形与三角形面积。

scene_spec.steps[2]

第三步：比值 $\dfrac{\sin(x/2)}{x/2}$ 随 $x\to0$ 逼近 1 的动画。

scene_spec.steps[3]

第四步：半角恒等式 $1-\cos x=2\sin^2(x/2)$ 的标注。

scene_spec.steps[4]

第五步：高亮最终结果与答案。

efficiency_tags[0]

单位圆中半角 $x/2$ 的扇形与三角形面积

efficiency_tags[1]

比值 $\dfrac{\sin(x/2)}{x/2}$ 随 $x\to0$ 逼近 1 的动画

efficiency_tags[2]

半角恒等式 $1-\cos x=2\sin^2(x/2)$ 的标注

## eval-calc-001-s2

problem

求极限 $\displaystyle\lim_{x\to 0}\frac{1-\cos x}{x^2}$。

solution

$\cos x = 1-\dfrac{x^2}{2}+\dfrac{x^4}{24}+o(x^4)$，故 $1-\cos x = \dfrac{x^2}{2}+o(x^2)$，原式 $=\lim_{x\to 0}\dfrac{x^2/2+o(x^2)}{x^2}=\dfrac{1}{2}$。

answer

$\dfrac{1}{2}$

scene_spec.objects[0]

原点邻域放大：$y=\cos x$ 与 $y=1-x^2/2$ 二阶接触

scene_spec.objects[1]

泰勒多项式逐项贴合曲线

scene_spec.steps[0]

第一步：以泰勒展开为主线，建立数学分析·极限场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：原点邻域放大：$y=\cos x$ 与 $y=1-x^2/2$ 二阶接触。

scene_spec.steps[2]

第三步：泰勒多项式逐项贴合曲线。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

原点邻域放大：$y=\cos x$ 与 $y=1-x^2/2$ 二阶接触

efficiency_tags[1]

泰勒多项式逐项贴合曲线

## eval-calc-001-s3

problem

求极限 $\displaystyle\lim_{x\to 0}\frac{1-\cos x}{x^2}$。

solution

原式为 $\dfrac{0}{0}$ 型。第一次求导：$\lim_{x\to 0}\dfrac{\sin x}{2x}$；第二次求导：$\lim_{x\to 0}\dfrac{\cos x}{2}=\dfrac{1}{2}$。

answer

$\dfrac{1}{2}$

scene_spec.objects[0]

分子分母比值表随两次求导收敛于 $\dfrac{1}{2}$

scene_spec.objects[1]

洛必达两次求导的符号推导滚动

scene_spec.steps[0]

第一步：以洛必达法则为主线，建立数学分析·极限场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：分子分母比值表随两次求导收敛于 $\dfrac{1}{2}$。

scene_spec.steps[2]

第三步：洛必达两次求导的符号推导滚动。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

分子分母比值表随两次求导收敛于 $\dfrac{1}{2}$

efficiency_tags[1]

洛必达两次求导的符号推导滚动

## eval-calc-002-s1

problem

求极限 $\displaystyle\lim_{x\to 0^+} x^x$。

solution

令 $y=x^x$，则 $\ln y = x\ln x$。令 $t=\dfrac{1}{x}\to+\infty$，则 $x\ln x = -\dfrac{\ln t}{t}\to 0$（对数函数增长慢于幂函数）。故 $\ln y\to 0$，由指数函数连续性得 $y\to e^0=1$。

answer

$1$

scene_spec.objects[0]

$t=\dfrac{1}{x}$ 代换把 $0^+$ 邻域拉到 $+\infty$ 的坐标动画

scene_spec.objects[1]

$y=\dfrac{\ln t}{t}$ 随 $t\to\infty$ 衰减到 0 的曲线

scene_spec.steps[0]

第一步：以对数化+变量替换为主线，建立数学分析·极限场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：$t=\dfrac{1}{x}$ 代换把 $0^+$ 邻域拉到 $+\infty$ 的坐标动画。

scene_spec.steps[2]

第三步：$y=\dfrac{\ln t}{t}$ 随 $t\to\infty$ 衰减到 0 的曲线。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

$t=\dfrac{1}{x}$ 代换把 $0^+$ 邻域拉到 $+\infty$ 的坐标动画

efficiency_tags[1]

$y=\dfrac{\ln t}{t}$ 随 $t\to\infty$ 衰减到 0 的曲线

## eval-calc-002-s2

problem

求极限 $\displaystyle\lim_{x\to 0^+} x^x$。

solution

同上先取对数，$x\ln x = \dfrac{\ln x}{1/x}$ 为 $\dfrac{-\infty}{+\infty}$ 型，洛必达：$\lim_{x\to 0^+}\dfrac{1/x}{-1/x^2}=\lim_{x\to 0^+}(-x)=0$，故原极限 $=e^0=1$。

answer

$1$

scene_spec.objects[0]

$\dfrac{\ln x}{1/x}$ 的洛必达一次求导

scene_spec.objects[1]

$x\ln x$ 在 $0^+$ 邻域的负值收敛曲线

scene_spec.steps[0]

第一步：以对数化+洛必达为主线，建立数学分析·极限场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：$\dfrac{\ln x}{1/x}$ 的洛必达一次求导。

scene_spec.steps[2]

第三步：$x\ln x$ 在 $0^+$ 邻域的负值收敛曲线。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

$\dfrac{\ln x}{1/x}$ 的洛必达一次求导

efficiency_tags[1]

$x\ln x$ 在 $0^+$ 邻域的负值收敛曲线

## eval-calc-002-s3

problem

求极限 $\displaystyle\lim_{x\to 0^+} x^x$。

solution

令 $x=e^{-t}$（$t\to+\infty$），则 $x^x = (e^{-t})^{e^{-t}} = e^{-t e^{-t}}$，而 $t e^{-t}\to 0$，故极限为 $e^0=1$。

answer

$1$

scene_spec.objects[0]

指数代换 $x=e^{-t}$ 的坐标压缩示意

scene_spec.objects[1]

$y=x^x$ 全图与 $x\to0^+$ 端放大趋近 $(0,1)$

scene_spec.steps[0]

第一步：以指数代换为主线，建立数学分析·极限场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：指数代换 $x=e^{-t}$ 的坐标压缩示意。

scene_spec.steps[2]

第三步：$y=x^x$ 全图与 $x\to0^+$ 端放大趋近 $(0,1)$。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

指数代换 $x=e^{-t}$ 的坐标压缩示意

efficiency_tags[1]

$y=x^x$ 全图与 $x\to0^+$ 端放大趋近 $(0,1)$

## eval-calc-003-s1

problem

证明极限 $\displaystyle\lim_{n\to\infty}\left(1+\frac{1}{n}\right)^n$ 存在（记为 $e$），并说明它与级数 $\displaystyle\sum_{k=0}^{\infty}\frac{1}{k!}$ 的联系。

solution

记 $a_n=\left(1+\dfrac{1}{n}\right)^n$。由二项式展开 $a_n=\sum_{k=0}^{n}\binom{n}{k}\dfrac{1}{n^k}=\sum_{k=0}^{n}\dfrac{1}{k!}\cdot\dfrac{n(n-1)\cdots(n-k+1)}{n^k}$。比较 $a_n$ 与 $a_{n+1}$ 的展开式，第 $k$ 项因子 $\dfrac{n(n-1)\cdots(n-k+1)}{n^k}\le\dfrac{(n+1)n\cdots(n-k+2)}{(n+1)^k}$，且 $a_{n+1}$ 还多一项，故 $a_{n+1}>a_n$，数列递增。又有 $a_n\le\sum_{k=0}^{n}\dfrac{1}{k!}\le 1+1+\dfrac{1}{2}+\dfrac{1}{4}+\cdots+\dfrac{1}{2^{n-1}}<3$，故有上界。由单调有界准则，$\lim a_n$ 存在，记为 $e$。令$E=\sum_{k=0}^{\infty}1/k!$。因$k!\ge2^{k-1}$（$k\ge1$），该正项级数收敛。二项式展开给出$a_n=\sum_{k=0}^{n}c_{k,n}/k!$，其中$c_{0,n}=c_{1,n}=1$，$c_{k,n}=\prod_{j=0}^{k-1}(1-j/n)\in[0,1]$。对固定$m$，当$n\ge m$时有$\sum_{k=0}^{m}c_{k,n}/k!\le a_n\le E$；令$n\to\infty$再令$m\to\infty$，得$\lim a_n=E$。

answer

极限存在且等于 $e=\sum_{k=0}^{\infty}\frac{1}{k!}$

scene_spec.objects[0]

二项展开系数柱状图逐项累加

scene_spec.objects[1]

数列 $a_n$ 单调递增且有上界 3 的标注

scene_spec.objects[2]

上界 3 的水平虚线

scene_spec.steps[0]

呈现题干及适用条件：证明极限 $\displaystyle\lim_{n\to\infty}\left(1+\frac{1}{n}\right)^n$ 存在（记为 $e$），并说明它与级数 $\displaystyle\sum_{k=0}^{\infty}\frac{1}{k!}$ 的联系。

scene_spec.steps[1]

依次呈现：二项展开系数柱状图逐项累加

scene_spec.steps[2]

依次呈现：数列 $a_n$ 单调递增且有上界 3 的标注

scene_spec.steps[3]

依次呈现：上界 3 的水平虚线

scene_spec.steps[4]

核对完整证明：记 $a_n=\left(1+\dfrac{1}{n}\right)^n$。由二项式展开 $a_n=\sum_{k=0}^{n}\binom{n}{k}\dfrac{1}{n^k}=\sum_{k=0}^{n}\dfrac{1}{k!}\cdot\dfrac{n(n-1)\cdots(n-k+1)}{n^k}$。比较 $a_n$ 与 $a_{n+1}$ 的展开式，第 $k$ 项因子 $\dfrac{n(n-1)\cdots(n-k+1)}{n^k}\le\dfrac{(n+1)n\cdots(n-k+2)}{(n+1)^k}$，且 $a_{n+1}$ 还多一项，故 $a_{n+1}>a_n$，数列递增。又有 $a_n\le\sum_{k=0}^{n}\dfrac{1}{k!}\le 1+1+\dfrac{1}{2}+\dfrac{1}{4}+\cdots+\dfrac{1}{2^{n-1}}<3$，故有上界。由单调有界准则，$\lim a_n$ 存在，记为 $e$。令$E=\sum_{k=0}^{\infty}1/k!$。因$k!\ge2^{k-1}$（$k\ge1$），该正项级数收敛。二项式展开给出$a_n=\sum_{k=0}^{n}c_{k,n}/k!$，其中$c_{0,n}=c_{1,n}=1$，$c_{k,n}=\prod_{j=0}^{k-1}(1-j/n)\in[0,1]$。对固定$m$，当$n\ge m$时有$\sum_{k=0}^{m}c_{k,n}/k!\le a_n\le E$；令$n\to\infty$再令$m\to\infty$，得$\lim a_n=E$。

scene_spec.steps[5]

高亮结果：极限存在且等于 $e=\sum_{k=0}^{\infty}\frac{1}{k!}$

efficiency_tags[0]

二项展开系数柱状图逐项累加

efficiency_tags[1]

数列 $a_n$ 单调递增且有上界 3 的标注

efficiency_tags[2]

上界 3 的水平虚线

## eval-calc-003-s2

problem

证明极限 $\displaystyle\lim_{n\to\infty}\left(1+\frac{1}{n}\right)^n$ 存在（记为 $e$），并说明它与级数 $\displaystyle\sum_{k=0}^{\infty}\frac{1}{k!}$ 的联系。

solution

设 $n\ln\left(1+\dfrac{1}{n}\right)=\dfrac{\ln(1+x)}{x}$，其中 $x=\dfrac{1}{n}\to 0^+$。洛必达：$\lim_{x\to 0^+}\dfrac{\ln(1+x)}{x}=\lim_{x\to 0^+}\dfrac{1}{1+x}=1$。故 $\lim n\ln(1+1/n)=1$，原极限 $=e^1$。注意此解法默认 $e$ 已由其他途径定义，适合作为验证。为连接级数定义，令$E(x)=\sum_{k=0}^{\infty}x^k/k!$；比值判别及幂级数理论保证全实轴收敛且可逐项求导，故$E^{\prime}=E$、$E(0)=1$。于是$(e^{-x}E(x))^{\prime}=0$，$E(x)=e^x$，特别地$e=\sum_{k=0}^{\infty}1/k!$。

answer

极限存在且等于 $e=\sum_{k=0}^{\infty}\frac{1}{k!}$

scene_spec.objects[0]

曲线 $y=\dfrac{\ln(1+x)}{x}$ 在 $x\to0^+$ 趋于 1

scene_spec.objects[1]

洛必达一次求导的过程

scene_spec.steps[0]

呈现题干及适用条件：证明极限 $\displaystyle\lim_{n\to\infty}\left(1+\frac{1}{n}\right)^n$ 存在（记为 $e$），并说明它与级数 $\displaystyle\sum_{k=0}^{\infty}\frac{1}{k!}$ 的联系。

scene_spec.steps[1]

依次呈现：曲线 $y=\dfrac{\ln(1+x)}{x}$ 在 $x\to0^+$ 趋于 1

scene_spec.steps[2]

依次呈现：洛必达一次求导的过程

scene_spec.steps[3]

核对完整证明：设 $n\ln\left(1+\dfrac{1}{n}\right)=\dfrac{\ln(1+x)}{x}$，其中 $x=\dfrac{1}{n}\to 0^+$。洛必达：$\lim_{x\to 0^+}\dfrac{\ln(1+x)}{x}=\lim_{x\to 0^+}\dfrac{1}{1+x}=1$。故 $\lim n\ln(1+1/n)=1$，原极限 $=e^1$。注意此解法默认 $e$ 已由其他途径定义，适合作为验证。为连接级数定义，令$E(x)=\sum_{k=0}^{\infty}x^k/k!$；比值判别及幂级数理论保证全实轴收敛且可逐项求导，故$E^{\prime}=E$、$E(0)=1$。于是$(e^{-x}E(x))^{\prime}=0$，$E(x)=e^x$，特别地$e=\sum_{k=0}^{\infty}1/k!$。

scene_spec.steps[4]

高亮结果：极限存在且等于 $e=\sum_{k=0}^{\infty}\frac{1}{k!}$

efficiency_tags[0]

曲线 $y=\dfrac{\ln(1+x)}{x}$ 在 $x\to0^+$ 趋于 1

efficiency_tags[1]

洛必达一次求导的过程

## eval-calc-003-s3

problem

证明极限 $\displaystyle\lim_{n\to\infty}\left(1+\frac{1}{n}\right)^n$ 存在（记为 $e$），并说明它与级数 $\displaystyle\sum_{k=0}^{\infty}\frac{1}{k!}$ 的联系。

solution

记 $c_k(n)=\left(1-\dfrac{1}{n}\right)\left(1-\dfrac{2}{n}\right)\cdots\left(1-\dfrac{k-1}{n}\right)$（约定 $c_0=c_1=1$），则 $a_n=\displaystyle\sum_{k=0}^{n}\dfrac{c_k(n)}{k!}$。每个因子都在 $(0,1]$ 内，故 $0<c_k(n)\le 1$，且对固定 $k$ 有 $c_k(n)\to 1$（$n\to\infty$）。一方面 $a_n\le\displaystyle\sum_{k=0}^{n}\dfrac{1}{k!}=:s_n$；另一方面对任意固定的 $m\le n$，$a_n\ge\displaystyle\sum_{k=0}^{m}\dfrac{c_k(n)}{k!}\to s_m$。于是 $s_m\le\liminf a_n\le\limsup a_n\le\lim s_n$，令 $m\to\infty$ 即得 $\lim a_n=\lim s_n=\displaystyle\sum_{k=0}^{\infty}\dfrac{1}{k!}$——数列极限与级数和两种构造给出同一个数 $e$。

answer

极限存在且等于 $e=\sum_{k=0}^{\infty}\frac{1}{k!}$

scene_spec.objects[0]

因子 $c_k(n)\to1$ 的逐项趋近动画

scene_spec.objects[1]

级数部分和 $s_n$ 与 $a_n$ 同框收敛于 $e$

scene_spec.steps[0]

第一步：以与级数定义的等价性为主线，建立数学分析·极限场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：因子 $c_k(n)\to1$ 的逐项趋近动画。

scene_spec.steps[2]

第三步：级数部分和 $s_n$ 与 $a_n$ 同框收敛于 $e$。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

因子 $c_k(n)\to1$ 的逐项趋近动画

efficiency_tags[1]

级数部分和 $s_n$ 与 $a_n$ 同框收敛于 $e$

## eval-calc-004-s1

problem

求极限 $\displaystyle\lim_{x\to 0}\frac{\sin x-\tan x}{x^3}$。

solution

提公因式：$\dfrac{\sin x-\tan x}{x^3}=\dfrac{\sin x\left(1-\dfrac{1}{\cos x}\right)}{x^3}=\dfrac{\sin x}{x}\cdot\dfrac{\cos x-1}{x^2}\cdot\dfrac{1}{\cos x}$。由 $\lim\dfrac{\sin x}{x}=1$、$\lim\dfrac{\cos x-1}{x^2}=-\dfrac{1}{2}$（eval-calc-001）、$\lim\dfrac{1}{\cos x}=1$，得原式 $=1\cdot\left(-\dfrac{1}{2}\right)\cdot 1=-\dfrac{1}{2}$。

answer

$-\dfrac{1}{2}$

scene_spec.objects[0]

因式分解 $\sin x\cdot\left(1-\dfrac{1}{\cos x}\right)$ 的拆项高亮

scene_spec.objects[1]

三个已知极限乘积的分解式标注

scene_spec.steps[0]

第一步：以因式分解+已知极限为主线，建立数学分析·极限场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：因式分解 $\sin x\cdot\left(1-\dfrac{1}{\cos x}\right)$ 的拆项高亮。

scene_spec.steps[2]

第三步：三个已知极限乘积的分解式标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

因式分解 $\sin x\cdot\left(1-\dfrac{1}{\cos x}\right)$ 的拆项高亮

efficiency_tags[1]

三个已知极限乘积的分解式标注

## eval-calc-004-s2

problem

求极限 $\displaystyle\lim_{x\to 0}\frac{\sin x-\tan x}{x^3}$。

solution

$\sin x = x-\dfrac{x^3}{6}+o(x^3)$，$\tan x = x+\dfrac{x^3}{3}+o(x^3)$，故 $\sin x-\tan x = -\dfrac{x^3}{2}+o(x^3)$，原式 $=-\dfrac{1}{2}$。

answer

$-\dfrac{1}{2}$

scene_spec.objects[0]

原点放大：$\sin x$ 与 $\tan x$ 近乎重合

scene_spec.objects[1]

差值曲线 $y=\sin x-\tan x$ 与 $-\dfrac{x^3}{2}$ 对比

scene_spec.steps[0]

第一步：以泰勒展开为主线，建立数学分析·极限场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：原点放大：$\sin x$ 与 $\tan x$ 近乎重合。

scene_spec.steps[2]

第三步：差值曲线 $y=\sin x-\tan x$ 与 $-\dfrac{x^3}{2}$ 对比。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

原点放大：$\sin x$ 与 $\tan x$ 近乎重合

efficiency_tags[1]

差值曲线 $y=\sin x-\tan x$ 与 $-\dfrac{x^3}{2}$ 对比

## eval-calc-004-s3

problem

求极限 $\displaystyle\lim_{x\to 0}\frac{\sin x-\tan x}{x^3}$。

solution

$\dfrac{0}{0}$ 型。一阶：$\dfrac{\cos x-\sec^2 x}{3x^2}$；二阶：$\dfrac{-\sin x-2\sec^2 x\tan x}{6x}$；三阶：$\dfrac{-\cos x-2(2\sec^2 x\tan^2 x+\sec^4 x)}{6}\to \dfrac{-1-2}{6}=-\dfrac{1}{2}$。

answer

$-\dfrac{1}{2}$

scene_spec.objects[0]

洛必达三次求导的符号推导滚动

scene_spec.objects[1]

分子分母比值随求导次数收敛于 $-\dfrac{1}{2}$

scene_spec.steps[0]

第一步：以洛必达法则为主线，建立数学分析·极限场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：洛必达三次求导的符号推导滚动。

scene_spec.steps[2]

第三步：分子分母比值随求导次数收敛于 $-\dfrac{1}{2}$。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

洛必达三次求导的符号推导滚动

efficiency_tags[1]

分子分母比值随求导次数收敛于 $-\dfrac{1}{2}$

## eval-calc-005-s1

problem

求函数 $y=x^x$（$x>0$）的导数。

solution

两边取对数：$\ln y=x\ln x$。两边对 $x$ 求导：$\dfrac{y'}{y}=\ln x+1$。故 $y'=y(\ln x+1)=x^x(\ln x+1)$。

answer

$y'=x^x(\ln x+1)$

scene_spec.objects[0]

两边取对数 $\ln y=x\ln x$ 的变形高亮

scene_spec.objects[1]

乘积求导法则作用于 $\ln y$ 的过程

scene_spec.steps[0]

第一步：以对数求导法为主线，建立数学分析·导数场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：两边取对数 $\ln y=x\ln x$ 的变形高亮。

scene_spec.steps[2]

第三步：乘积求导法则作用于 $\ln y$ 的过程。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

两边取对数 $\ln y=x\ln x$ 的变形高亮

efficiency_tags[1]

乘积求导法则作用于 $\ln y$ 的过程

## eval-calc-005-s2

problem

求函数 $y=x^x$（$x>0$）的导数。

solution

令 $F(x,y)=\ln y-x\ln x=0$。由隐函数求导公式 $y'=-\dfrac{F_x}{F_y}=-\dfrac{-(\ln x+1)}{1/y}=y(\ln x+1)=x^x(\ln x+1)$。

answer

$y'=x^x(\ln x+1)$

scene_spec.objects[0]

隐函数求导公式 $y'=-\dfrac{F_x}{F_y}$ 的分量标注

scene_spec.objects[1]

$F(x,y)=\ln y-x\ln x=0$ 的等值线

scene_spec.steps[0]

第一步：以隐函数求导为主线，建立数学分析·导数场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：隐函数求导公式 $y'=-\dfrac{F_x}{F_y}$ 的分量标注。

scene_spec.steps[2]

第三步：$F(x,y)=\ln y-x\ln x=0$ 的等值线。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

隐函数求导公式 $y'=-\dfrac{F_x}{F_y}$ 的分量标注

efficiency_tags[1]

$F(x,y)=\ln y-x\ln x=0$ 的等值线

## eval-calc-005-s3

problem

求函数 $y=x^x$（$x>0$）的导数。

solution

$x^x=e^{x\ln x}$，故 $y'=e^{x\ln x}\cdot(x\ln x)'=x^x(\ln x+1)$。

answer

$y'=x^x(\ln x+1)$

scene_spec.objects[0]

$y=x^x$ 曲线与极小值点 $x=\dfrac{1}{e}$

scene_spec.objects[1]

切线斜率随 $x$ 变化（由负转正）

scene_spec.steps[0]

第一步：以指数化+链式法则为主线，建立数学分析·导数场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：$y=x^x$ 曲线与极小值点 $x=\dfrac{1}{e}$。

scene_spec.steps[2]

第三步：切线斜率随 $x$ 变化（由负转正）。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

$y=x^x$ 曲线与极小值点 $x=\dfrac{1}{e}$

efficiency_tags[1]

切线斜率随 $x$ 变化（由负转正）

## eval-calc-006-s1

problem

求函数 $y=\ln(x+\sqrt{x^2+a^2})$（$a>0$）的导数，并说明其反函数。

solution

$y'=\dfrac{1+\dfrac{x}{\sqrt{x^2+a^2}}}{x+\sqrt{x^2+a^2}}=\dfrac{\sqrt{x^2+a^2}+x}{\sqrt{x^2+a^2}\cdot(x+\sqrt{x^2+a^2})}=\dfrac{1}{\sqrt{x^2+a^2}}$。反解$e^y=x+\sqrt{x^2+a^2}$，得$x=(e^{2y}-a^2)/(2e^y)=(e^y-a^2e^{-y})/2=a\sinh(y-\ln a)$。代回时$\sqrt{x^2+a^2}=(e^y+a^2e^{-y})/2$，故没有平方引入的赘解。原函数严格递增，$x\to\pm\infty$时$y\to\pm\infty$，所以该反函数定义于$\mathbb R$。

answer

$y'=\dfrac{1}{\sqrt{x^2+a^2}}$；反函数为 $x=a\sinh(y-\ln a)=\dfrac{e^y-a^2e^{-y}}{2}$

scene_spec.objects[0]

链式法则逐层拆解：外层对数、内层 $x+\sqrt{x^2+a^2}$

scene_spec.objects[1]

分子分母同乘 $\sqrt{x^2+a^2}$ 的化简动画

scene_spec.steps[0]

呈现题干及适用条件：求函数 $y=\ln(x+\sqrt{x^2+a^2})$（$a>0$）的导数，并说明其反函数。

scene_spec.steps[1]

依次呈现：链式法则逐层拆解：外层对数、内层 $x+\sqrt{x^2+a^2}$

scene_spec.steps[2]

依次呈现：分子分母同乘 $\sqrt{x^2+a^2}$ 的化简动画

scene_spec.steps[3]

核对完整证明：$y'=\dfrac{1+\dfrac{x}{\sqrt{x^2+a^2}}}{x+\sqrt{x^2+a^2}}=\dfrac{\sqrt{x^2+a^2}+x}{\sqrt{x^2+a^2}\cdot(x+\sqrt{x^2+a^2})}=\dfrac{1}{\sqrt{x^2+a^2}}$。反解$e^y=x+\sqrt{x^2+a^2}$，得$x=(e^{2y}-a^2)/(2e^y)=(e^y-a^2e^{-y})/2=a\sinh(y-\ln a)$。代回时$\sqrt{x^2+a^2}=(e^y+a^2e^{-y})/2$，故没有平方引入的赘解。原函数严格递增，$x\to\pm\infty$时$y\to\pm\infty$，所以该反函数定义于$\mathbb R$。

scene_spec.steps[4]

高亮结果：$y'=\dfrac{1}{\sqrt{x^2+a^2}}$；反函数为 $x=a\sinh(y-\ln a)=\dfrac{e^y-a^2e^{-y}}{2}$

efficiency_tags[0]

链式法则逐层拆解：外层对数、内层 $x+\sqrt{x^2+a^2}$

efficiency_tags[1]

分子分母同乘 $\sqrt{x^2+a^2}$ 的化简动画

## eval-calc-006-s2

problem

求函数 $y=\ln(x+\sqrt{x^2+a^2})$（$a>0$）的导数，并说明其反函数。

solution

令 $x=a\sinh t$，则 $x+\sqrt{x^2+a^2}=a(\sinh t+\cosh t)=a e^t$，故 $y=\ln(ae^t)=t+\ln a$，即 $y=\operatorname{arsinh}\dfrac{x}{a}+\ln a$。由反双曲函数求导公式 $(\operatorname{arsinh} u)'=\dfrac{u'}{\sqrt{1+u^2}}$，得 $y'=\dfrac{1/a}{\sqrt{1+x^2/a^2}}=\dfrac{1}{\sqrt{x^2+a^2}}$。反解$e^y=x+\sqrt{x^2+a^2}$，得$x=(e^{2y}-a^2)/(2e^y)=(e^y-a^2e^{-y})/2=a\sinh(y-\ln a)$。代回时$\sqrt{x^2+a^2}=(e^y+a^2e^{-y})/2$，故没有平方引入的赘解。原函数严格递增，$x\to\pm\infty$时$y\to\pm\infty$，所以该反函数定义于$\mathbb R$。

answer

$y'=\dfrac{1}{\sqrt{x^2+a^2}}$；反函数为 $x=a\sinh(y-\ln a)=\dfrac{e^y-a^2e^{-y}}{2}$

scene_spec.objects[0]

双曲线$Y^2-X^2=a^2$的上支：$X=a\sinh t,\ Y=a\cosh t$

scene_spec.objects[1]

恒等式$\sinh t+\cosh t=e^t$；反函数$x=a\sinh(y-\ln a)$

scene_spec.steps[0]

呈现题干及适用条件：求函数 $y=\ln(x+\sqrt{x^2+a^2})$（$a>0$）的导数，并说明其反函数。

scene_spec.steps[1]

依次呈现：双曲线$Y^2-X^2=a^2$的上支：$X=a\sinh t,\ Y=a\cosh t$

scene_spec.steps[2]

依次呈现：恒等式$\sinh t+\cosh t=e^t$；反函数$x=a\sinh(y-\ln a)$

scene_spec.steps[3]

核对完整证明：令 $x=a\sinh t$，则 $x+\sqrt{x^2+a^2}=a(\sinh t+\cosh t)=a e^t$，故 $y=\ln(ae^t)=t+\ln a$，即 $y=\operatorname{arsinh}\dfrac{x}{a}+\ln a$。由反双曲函数求导公式 $(\operatorname{arsinh} u)'=\dfrac{u'}{\sqrt{1+u^2}}$，得 $y'=\dfrac{1/a}{\sqrt{1+x^2/a^2}}=\dfrac{1}{\sqrt{x^2+a^2}}$。反解$e^y=x+\sqrt{x^2+a^2}$，得$x=(e^{2y}-a^2)/(2e^y)=(e^y-a^2e^{-y})/2=a\sinh(y-\ln a)$。代回时$\sqrt{x^2+a^2}=(e^y+a^2e^{-y})/2$，故没有平方引入的赘解。原函数严格递增，$x\to\pm\infty$时$y\to\pm\infty$，所以该反函数定义于$\mathbb R$。

scene_spec.steps[4]

高亮结果：$y'=\dfrac{1}{\sqrt{x^2+a^2}}$；反函数为 $x=a\sinh(y-\ln a)=\dfrac{e^y-a^2e^{-y}}{2}$

efficiency_tags[0]

双曲线$Y^2-X^2=a^2$的上支：$X=a\sinh t,\ Y=a\cosh t$

efficiency_tags[1]

恒等式$\sinh t+\cosh t=e^t$；反函数$x=a\sinh(y-\ln a)$

## eval-calc-006-s3

problem

求函数 $y=\ln(x+\sqrt{x^2+a^2})$（$a>0$）的导数，并说明其反函数。

solution

由 $y=\ln(x+\sqrt{x^2+a^2})$ 解出 $x$：$e^y=x+\sqrt{x^2+a^2}$，移项平方得 $e^{2y}-2xe^y=a^2$，故 $x=\dfrac{e^y-a^2e^{-y}}{2}=a\sinh(y-\ln a)$。于是 $\dfrac{dx}{dy}=a\cosh(y-\ln a)=\sqrt{x^2+a^2}$，故 $\dfrac{dy}{dx}=\dfrac{1}{\sqrt{x^2+a^2}}$。

answer

$y'=\dfrac{1}{\sqrt{x^2+a^2}}$；反函数为 $x=a\sinh(y-\ln a)=\dfrac{e^y-a^2e^{-y}}{2}$

scene_spec.objects[0]

反函数图像关于 $y=x$ 对称

scene_spec.objects[1]

反解出 $x=a\sinh(y-\ln a)$ 的推导过程

scene_spec.steps[0]

第一步：以反函数求导为主线，建立数学分析·导数场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：反函数图像关于 $y=x$ 对称。

scene_spec.steps[2]

第三步：反解出 $x=a\sinh(y-\ln a)$ 的推导过程。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

反函数图像关于 $y=x$ 对称

efficiency_tags[1]

反解出 $x=a\sinh(y-\ln a)$ 的推导过程

## eval-calc-007-s1

problem

设星形线参数方程为 $x=a\cos^3 t$，$y=a\sin^3 t$（$a>0$，$0\le t\le 2\pi$），求 $\dfrac{dy}{dx}$ 与 $\dfrac{d^2y}{dx^2}$。

solution

$\dfrac{dx}{dt}=-3a\cos^2 t\sin t$，$\dfrac{dy}{dt}=3a\sin^2 t\cos t$，故 $\dfrac{dy}{dx}=\dfrac{3a\sin^2t\cos t}{-3a\cos^2t\sin t}=-\tan t$。二阶导：$\dfrac{d^2y}{dx^2}=\dfrac{d}{dt}\left(\dfrac{dy}{dx}\right)\Big/\dfrac{dx}{dt}=\dfrac{-\sec^2 t}{-3a\cos^2 t\sin t}=\dfrac{1}{3a\cos^4 t\sin t}$。

answer

$\dfrac{dy}{dx}=-\tan t$；$\dfrac{d^2y}{dx^2}=\dfrac{1}{3a\cos^4 t\sin t}$（两式仅在光滑分支上成立，即 $\sin t\cos t\ne 0$；在尖点 $t=k\dfrac{\pi}{2}$ 处切线竖直或水平、二阶导不存在，需单独作单侧讨论）

scene_spec.objects[0]

参数点 $(a\cos^3t,a\sin^3t)$ 沿星形线运动

scene_spec.objects[1]

$\dfrac{dy}{dx}=\dfrac{dy/dt}{dx/dt}$ 的商式动画

scene_spec.steps[0]

第一步：以参数方程求导公式为主线，建立数学分析·导数场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：参数点 $(a\cos^3t,a\sin^3t)$ 沿星形线运动。

scene_spec.steps[2]

第三步：$\dfrac{dy}{dx}=\dfrac{dy/dt}{dx/dt}$ 的商式动画。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

参数点 $(a\cos^3t,a\sin^3t)$ 沿星形线运动

efficiency_tags[1]

$\dfrac{dy}{dx}=\dfrac{dy/dt}{dx/dt}$ 的商式动画

## eval-calc-007-s2

problem

设星形线参数方程为 $x=a\cos^3 t$，$y=a\sin^3 t$（$a>0$，$0\le t\le 2\pi$），求 $\dfrac{dy}{dx}$ 与 $\dfrac{d^2y}{dx^2}$。

solution

消去参数：$x^{2/3}+y^{2/3}=a^{2/3}$。两边对 $x$ 求导：$\dfrac{2}{3}x^{-1/3}+\dfrac{2}{3}y^{-1/3}y'=0$，故 $y'=-\left(\dfrac{y}{x}\right)^{1/3}=-\tan t$。再对 $x$ 求导：$y''=-\dfrac{1}{3}\left(\dfrac{y}{x}\right)^{-2/3}\cdot\dfrac{y'x-y}{x^2}$。代入 $x=a\cos^3 t$、$y=a\sin^3 t$、$y'=-\tan t$：$\left(\dfrac{y}{x}\right)^{2/3}=\tan^2 t$，且 $y'x-y=-\tan t\cdot a\cos^3 t-a\sin^3 t=-a\sin t(\cos^2 t+\sin^2 t)=-a\sin t$。故 $y''=-\dfrac{1}{3}\cot^2 t\cdot\dfrac{-a\sin t}{a^2\cos^6 t}=\dfrac{1}{3a\cos^4 t\sin t}$，与解法一一致。

answer

$\dfrac{dy}{dx}=-\tan t$；$\dfrac{d^2y}{dx^2}=\dfrac{1}{3a\cos^4 t\sin t}$（两式仅在光滑分支上成立，即 $\sin t\cos t\ne 0$；在尖点 $t=k\dfrac{\pi}{2}$ 处切线竖直或水平、二阶导不存在，需单独作单侧讨论）

scene_spec.objects[0]

消参方程 $x^{2/3}+y^{2/3}=a^{2/3}$ 的隐式求导

scene_spec.objects[1]

二阶导 $y''$ 代入参数化简的步骤

scene_spec.steps[0]

第一步：以消参后隐函数求导为主线，建立数学分析·导数场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：消参方程 $x^{2/3}+y^{2/3}=a^{2/3}$ 的隐式求导。

scene_spec.steps[2]

第三步：二阶导 $y''$ 代入参数化简的步骤。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

消参方程 $x^{2/3}+y^{2/3}=a^{2/3}$ 的隐式求导

efficiency_tags[1]

二阶导 $y''$ 代入参数化简的步骤

## eval-calc-007-s3

problem

设星形线参数方程为 $x=a\cos^3 t$，$y=a\sin^3 t$（$a>0$，$0\le t\le 2\pi$），求 $\dfrac{dy}{dx}$ 与 $\dfrac{d^2y}{dx^2}$。

solution

星形线的切线族为$F(x,y,t)=x\sin t+y\cos t-a\sin t\cos t=0$；包络条件$F_t=0$给出$x=a\cos^3t,\ y=a\sin^3t$。在$\sin t\cos t\ne0$时，沿包络对$F=0$求导，因$F_t=0$，得$\sin t+\cos t\,y^{\prime}=0$，故$y^{\prime}=-\tan t$。再由$x^{\prime}=-3a\cos^2t\sin t$，得$y^{\prime\prime}=(-\sec^2t)/x^{\prime}=1/(3a\cos^4t\sin t)$。切线的轴截距为$a\cos t,a\sin t$，两截距点间距为$a$。尖点$t=k\pi/2$需另判：$t=k\pi$处切线水平，$t=\pi/2+k\pi$处切线竖直；尖点不套用上述二阶导公式。

answer

$\dfrac{dy}{dx}=-\tan t$；$\dfrac{d^2y}{dx^2}=\dfrac{1}{3a\cos^4 t\sin t}$（两式仅在光滑分支上成立，即 $\sin t\cos t\ne 0$；在尖点 $t=k\dfrac{\pi}{2}$ 处切线竖直或水平、二阶导不存在，需单独作单侧讨论）

scene_spec.objects[0]

滑动长度$a$的线段与包络$F=F_t=0$

scene_spec.objects[1]

四尖点处参数速度为零；切线分别水平或竖直，切线本身不发生无向角跳变

scene_spec.objects[2]

切线截距$a\cos t,a\sin t$；正则点二阶导数$\frac{d^2y}{dx^2}$

scene_spec.steps[0]

呈现题干及适用条件：设星形线参数方程为 $x=a\cos^3 t$，$y=a\sin^3 t$（$a>0$，$0\le t\le 2\pi$），求 $\dfrac{dy}{dx}$ 与 $\dfrac{d^2y}{dx^2}$。

scene_spec.steps[1]

依次呈现：滑动长度$a$的线段与包络$F=F_t=0$

scene_spec.steps[2]

依次呈现：四尖点处参数速度为零；切线分别水平或竖直，切线本身不发生无向角跳变

scene_spec.steps[3]

依次呈现：切线截距$a\cos t,a\sin t$及正则点的$y^{\prime\prime}$公式

scene_spec.steps[4]

核对完整证明：星形线的切线族为$F(x,y,t)=x\sin t+y\cos t-a\sin t\cos t=0$；包络条件$F_t=0$给出$x=a\cos^3t,\ y=a\sin^3t$。在$\sin t\cos t\ne0$时，沿包络对$F=0$求导，因$F_t=0$，得$\sin t+\cos t\,y^{\prime}=0$，故$y^{\prime}=-\tan t$。再由$x^{\prime}=-3a\cos^2t\sin t$，得$y^{\prime\prime}=(-\sec^2t)/x^{\prime}=1/(3a\cos^4t\sin t)$。切线的轴截距为$a\cos t,a\sin t$，两截距点间距为$a$。尖点$t=k\pi/2$需另判：$t=k\pi$处切线水平，$t=\pi/2+k\pi$处切线竖直；尖点不套用上述二阶导公式。

scene_spec.steps[5]

高亮结果：$\dfrac{dy}{dx}=-\tan t$；$\dfrac{d^2y}{dx^2}=\dfrac{1}{3a\cos^4 t\sin t}$（两式仅在光滑分支上成立，即 $\sin t\cos t\ne 0$；在尖点 $t=k\dfrac{\pi}{2}$ 处切线竖直或水平、二阶导不存在，需单独作单侧讨论）

efficiency_tags[0]

滑动长度$a$的线段与包络$F=F_t=0$

efficiency_tags[1]

四尖点处参数速度为零；切线分别水平或竖直，切线本身不发生无向角跳变

efficiency_tags[2]

切线截距$a\cos t,a\sin t$；正则点二阶导数$\frac{d^2y}{dx^2}$

## eval-calc-008-s1

problem

证明：当 $x>0$ 时，$e^x>1+x$。

solution

令 $f(x)=e^x-1-x$，则 $f'(x)=e^x-1>0$（$x>0$），故 $f$ 在 $[0,+\infty)$ 上严格递增。又 $f(0)=0$，所以当 $x>0$ 时 $f(x)>f(0)=0$，即 $e^x>1+x$。

answer

证毕（三种证法）

scene_spec.objects[0]

差值函数 $f(x)=e^x-1-x$ 的递增曲线

scene_spec.objects[1]

$f(0)=0$ 起点的标注

scene_spec.steps[0]

第一步：以单调性为主线，建立数学分析·中值定理场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：差值函数 $f(x)=e^x-1-x$ 的递增曲线。

scene_spec.steps[2]

第三步：$f(0)=0$ 起点的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

差值函数 $f(x)=e^x-1-x$ 的递增曲线

efficiency_tags[1]

$f(0)=0$ 起点的标注

## eval-calc-008-s2

problem

证明：当 $x>0$ 时，$e^x>1+x$。

solution

对 $f(x)=e^x$ 在 $[0,x]$ 上用拉格朗日中值定理：存在 $\xi\in(0,x)$ 使 $e^x-e^0=e^\xi(x-0)$。因 $\xi>0$，$e^\xi>1$，故 $e^x-1=e^\xi x>x$，即 $e^x>1+x$。

answer

证毕（三种证法）

scene_spec.objects[0]

中值点 $\xi$ 在 $(0,x)$ 上的扫描与 $e^\xi$ 变化

scene_spec.objects[1]

$y=e^x$ 与割线的位置关系

scene_spec.steps[0]

第一步：以拉格朗日中值定理为主线，建立数学分析·中值定理场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：中值点 $\xi$ 在 $(0,x)$ 上的扫描与 $e^\xi$ 变化。

scene_spec.steps[2]

第三步：$y=e^x$ 与割线的位置关系。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

中值点 $\xi$ 在 $(0,x)$ 上的扫描与 $e^\xi$ 变化

efficiency_tags[1]

$y=e^x$ 与割线的位置关系

## eval-calc-008-s3

problem

证明：当 $x>0$ 时，$e^x>1+x$。

solution

$e^x=1+x+\dfrac{x^2}{2}e^\eta$，其中 $\eta\in(0,x)$。因 $\dfrac{x^2}{2}e^\eta>0$，故 $e^x>1+x$。此证法还给出更强的估计 $e^x>1+x+\dfrac{x^2}{2}$。

answer

证毕（三种证法）

scene_spec.objects[0]

泰勒余项曲线 $y=\dfrac{x^2}{2}e^{\eta}$ 的包络

scene_spec.objects[1]

强估计 $e^x>1+x+\dfrac{x^2}{2}$ 的标注

scene_spec.steps[0]

第一步：以泰勒公式带余项为主线，建立数学分析·中值定理场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：泰勒余项曲线 $y=\dfrac{x^2}{2}e^{\eta}$ 的包络。

scene_spec.steps[2]

第三步：强估计 $e^x>1+x+\dfrac{x^2}{2}$ 的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

泰勒余项曲线 $y=\dfrac{x^2}{2}e^{\eta}$ 的包络

efficiency_tags[1]

强估计 $e^x>1+x+\dfrac{x^2}{2}$ 的标注

## eval-calc-009-s1

problem

设 $0<a<b$，证明：$\arctan b-\arctan a<b-a$。

solution

对 $f(x)=\arctan x$ 在 $[a,b]$ 上用中值定理：存在 $\xi\in(a,b)$ 使 $\arctan b-\arctan a=\dfrac{1}{1+\xi^2}(b-a)$。因 $\dfrac{1}{1+\xi^2}<1$，故 $\arctan b-\arctan a<b-a$。

answer

证毕（三种证法）

scene_spec.objects[0]

中值点 $\xi\in(a,b)$ 的扫描

scene_spec.objects[1]

切线斜率 $\dfrac{1}{1+\xi^2}<1$ 的实时标注

scene_spec.steps[0]

第一步：以拉格朗日中值定理为主线，建立数学分析·中值定理场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：中值点 $\xi\in(a,b)$ 的扫描。

scene_spec.steps[2]

第三步：切线斜率 $\dfrac{1}{1+\xi^2}<1$ 的实时标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

中值点 $\xi\in(a,b)$ 的扫描

efficiency_tags[1]

切线斜率 $\dfrac{1}{1+\xi^2}<1$ 的实时标注

## eval-calc-009-s2

problem

设 $0<a<b$，证明：$\arctan b-\arctan a<b-a$。

solution

令 $g(x)=x-\arctan x$，则 $g'(x)=1-\dfrac{1}{1+x^2}=\dfrac{x^2}{1+x^2}>0$（$x>0$），故 $g$ 在 $(0,+\infty)$ 上严格递增，$g(b)>g(a)$，即 $b-\arctan b>a-\arctan a$，移项得证。

answer

证毕（三种证法）

scene_spec.objects[0]

差值函数 $g(x)=x-\arctan x$ 的递增曲线

scene_spec.objects[1]

$g(b)>g(a)$ 的区间标注

scene_spec.steps[0]

第一步：以单调性为主线，建立数学分析·中值定理场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：差值函数 $g(x)=x-\arctan x$ 的递增曲线。

scene_spec.steps[2]

第三步：$g(b)>g(a)$ 的区间标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

差值函数 $g(x)=x-\arctan x$ 的递增曲线

efficiency_tags[1]

$g(b)>g(a)$ 的区间标注

## eval-calc-009-s3

problem

设 $0<a<b$，证明：$\arctan b-\arctan a<b-a$。

solution

由 $(\arctan x)'=\dfrac{1}{1+x^2}<1$ 知 $y=\arctan x$ 在 $(0,+\infty)$ 上任意两点连线的斜率小于 1（割线斜率 = 某点导数值 < 1），故 $\dfrac{\arctan b-\arctan a}{b-a}<1$，得证。

answer

证毕（三种证法）

scene_spec.objects[0]

割线斜率与中值点切线斜率联动

scene_spec.objects[1]

$y=\arctan x$ 与 $y=x$ 对比

scene_spec.steps[0]

第一步：以几何斜率比较为主线，建立数学分析·中值定理场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：割线斜率与中值点切线斜率联动。

scene_spec.steps[2]

第三步：$y=\arctan x$ 与 $y=x$ 对比。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

割线斜率与中值点切线斜率联动

efficiency_tags[1]

$y=\arctan x$ 与 $y=x$ 对比

## eval-calc-010-s1

problem

求极限 $\displaystyle\lim_{x\to 0}\frac{e^x-e^{\sin x}}{x-\sin x}$。

solution

令 $f(t)=e^t$，对 $f$ 在 $\sin x$ 与 $x$ 之间用中值定理：$e^x-e^{\sin x}=e^\xi(x-\sin x)$，其中 $\xi$ 介于 $\sin x$ 与 $x$ 之间。当 $x\to 0$ 时 $\sin x\to 0$、$x\to 0$，故 $\xi\to 0$。原式 $=\lim_{x\to 0}e^\xi=1$。

answer

$1$

scene_spec.objects[0]

$y=e^t$ 上两点 $(\sin x, e^{\sin x})$、$(x, e^x)$ 随 $x\to0$ 靠拢

scene_spec.objects[1]

中值点 $\xi$ 被夹逼向 0

scene_spec.steps[0]

第一步：以拉格朗日中值定理为主线，建立数学分析·中值定理场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：$y=e^t$ 上两点 $(\sin x, e^{\sin x})$、$(x, e^x)$ 随 $x\to0$ 靠拢。

scene_spec.steps[2]

第三步：中值点 $\xi$ 被夹逼向 0。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

$y=e^t$ 上两点 $(\sin x, e^{\sin x})$、$(x, e^x)$ 随 $x\to0$ 靠拢

efficiency_tags[1]

中值点 $\xi$ 被夹逼向 0

## eval-calc-010-s2

problem

求极限 $\displaystyle\lim_{x\to 0}\frac{e^x-e^{\sin x}}{x-\sin x}$。

solution

原式 $=\lim_{x\to 0}\dfrac{e^{\sin x}\left(e^{x-\sin x}-1\right)}{x-\sin x}=\lim_{x\to 0}e^{\sin x}\cdot\lim_{x\to 0}\dfrac{e^{x-\sin x}-1}{x-\sin x}=1\cdot 1=1$。

answer

$1$

scene_spec.objects[0]

提取公因子 $e^{\sin x}$ 的变形高亮

scene_spec.objects[1]

等价无穷小 $\dfrac{e^u-1}{u}\to1$ 的比值动画

scene_spec.steps[0]

第一步：以提取公因子+等价无穷小为主线，建立数学分析·中值定理场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：提取公因子 $e^{\sin x}$ 的变形高亮。

scene_spec.steps[2]

第三步：等价无穷小 $\dfrac{e^u-1}{u}\to1$ 的比值动画。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

提取公因子 $e^{\sin x}$ 的变形高亮

efficiency_tags[1]

等价无穷小 $\dfrac{e^u-1}{u}\to1$ 的比值动画

## eval-calc-010-s3

problem

求极限 $\displaystyle\lim_{x\to 0}\frac{e^x-e^{\sin x}}{x-\sin x}$。

solution

原式为 $\dfrac{0}{0}$ 型。第一次：$\lim_{x\to 0}\dfrac{e^x-e^{\sin x}\cos x}{1-\cos x}$，仍为 $\dfrac{0}{0}$ 型。第二次：分子求导得 $e^x-e^{\sin x}\cos^2 x+e^{\sin x}\sin x$，分母求导得 $\sin x$，仍为 $\dfrac{0}{0}$ 型。第三次：分子再求导为 $e^x-e^{\sin x}(\cos^3 x-2\sin x\cos x)+e^{\sin x}\cos x(\sin x+1)$，分母求导为 $\cos x$。令 $x\to 0$：分子 $\to 1-1\cdot(1-0)+1\cdot 1\cdot(0+1)=1$，分母 $\to 1$，故极限为 $\dfrac{1}{1}=1$。此路可通但三次求导冗长，恰好反衬解法一的一步到位。

answer

$1$

scene_spec.objects[0]

洛必达三次求导的符号推导滚动

scene_spec.objects[1]

分子分母比值收敛于 1

scene_spec.steps[0]

第一步：以洛必达法则，连用三次为主线，建立数学分析·中值定理场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：洛必达三次求导的符号推导滚动。

scene_spec.steps[2]

第三步：分子分母比值收敛于 1。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

洛必达三次求导的符号推导滚动

efficiency_tags[1]

分子分母比值收敛于 1

## eval-calc-011-s1

problem

用多种方法求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\cdot 2^n}$ 的和。

solution

由 $-\ln(1-x)=\displaystyle\int_0^x\dfrac{dt}{1-t}=\int_0^x\sum_{n=0}^{\infty}t^n\,dt=\sum_{n=1}^{\infty}\dfrac{x^n}{n}=x+\dfrac{x^2}{2}+\dfrac{x^3}{3}+\cdots$（$|x|<1$），取 $x=\dfrac{1}{2}$，得 $\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{n\cdot 2^n}=-\ln\left(1-\dfrac{1}{2}\right)=-\ln\dfrac{1}{2}=\ln 2$。

answer

$\ln 2$

scene_spec.objects[0]

展开式 $-\ln(1-x)=x+\dfrac{x^2}{2}+\cdots$ 的逐项生成

scene_spec.objects[1]

$x=\dfrac{1}{2}$ 代入的标注

scene_spec.steps[0]

第一步：以代入对数展开式为主线，建立数学分析·幂级数场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：展开式 $-\ln(1-x)=x+\dfrac{x^2}{2}+\cdots$ 的逐项生成。

scene_spec.steps[2]

第三步：$x=\dfrac{1}{2}$ 代入的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

展开式 $-\ln(1-x)=x+\dfrac{x^2}{2}+\cdots$ 的逐项生成

efficiency_tags[1]

$x=\dfrac{1}{2}$ 代入的标注

## eval-calc-011-s2

problem

用多种方法求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\cdot 2^n}$ 的和。

solution

由 $\dfrac{1}{n\cdot 2^n}=\displaystyle\int_0^{1/2}x^{n-1}\,dx$（把 $\dfrac{1}{2^n}$ 看作幂的积分），故 $S=\displaystyle\sum_{n=1}^{\infty}\int_0^{1/2}x^{n-1}dx=\int_0^{1/2}\sum_{n=1}^{\infty}x^{n-1}dx=\int_0^{1/2}\dfrac{dx}{1-x}=\left[-\ln(1-x)\right]_0^{1/2}=\ln 2$（求和与积分可交换由正项级数单调收敛保证）。

answer

$\ln 2$

scene_spec.objects[0]

在$[0,1/2]$叠加幂函数$x^{n-1}$的面积

scene_spec.objects[1]

$\int_0^{1/2}x^{n-1}dx=1/(n2^n)$；非负项用单调收敛交换求和与积分

scene_spec.steps[0]

呈现题干及适用条件：用多种方法求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\cdot 2^n}$ 的和。

scene_spec.steps[1]

依次呈现：在$[0,1/2]$叠加幂函数$x^{n-1}$的面积

scene_spec.steps[2]

依次呈现：$\int_0^{1/2}x^{n-1}dx=1/(n2^n)$；非负项用单调收敛交换求和与积分

scene_spec.steps[3]

核对完整证明：由 $\dfrac{1}{n\cdot 2^n}=\displaystyle\int_0^{1/2}x^{n-1}\,dx$（把 $\dfrac{1}{2^n}$ 看作幂的积分），故 $S=\displaystyle\sum_{n=1}^{\infty}\int_0^{1/2}x^{n-1}dx=\int_0^{1/2}\sum_{n=1}^{\infty}x^{n-1}dx=\int_0^{1/2}\dfrac{dx}{1-x}=\left[-\ln(1-x)\right]_0^{1/2}=\ln 2$（求和与积分可交换由正项级数单调收敛保证）。

scene_spec.steps[4]

高亮结果：$\ln 2$

efficiency_tags[0]

在$[0,1/2]$叠加幂函数$x^{n-1}$的面积

efficiency_tags[1]

$\int_0^{1/2}x^{n-1}dx=1/(n2^n)$；非负项用单调收敛交换求和与积分

## eval-calc-011-s3

problem

用多种方法求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\cdot 2^n}$ 的和。

solution

设 $f(x)=\displaystyle\sum_{n=1}^{\infty}\dfrac{x^n}{n}$，逐项求导得 $f'(x)=\displaystyle\sum_{n=1}^{\infty}x^{n-1}=\dfrac{1}{1-x}$（$|x|<1$），且 $f(0)=0$，故 $f(x)=-\ln(1-x)$，取 $x=\dfrac{1}{2}$ 得 $\ln 2$。

answer

$\ln 2$

scene_spec.objects[0]

逐项求导得 $f'(x)=\dfrac{1}{1-x}$ 的过程

scene_spec.objects[1]

由 $f(0)=0$ 积分还原 $f(x)$ 的动画

scene_spec.steps[0]

第一步：以由导数重建展开式为主线，建立数学分析·幂级数场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：逐项求导得 $f'(x)=\dfrac{1}{1-x}$ 的过程。

scene_spec.steps[2]

第三步：由 $f(0)=0$ 积分还原 $f(x)$ 的动画。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

逐项求导得 $f'(x)=\dfrac{1}{1-x}$ 的过程

efficiency_tags[1]

由 $f(0)=0$ 积分还原 $f(x)$ 的动画

## eval-calc-012-s1

problem

求 $\tan 15^\circ$ 的精确值。

solution

$\tan 15^\circ=\tan(45^\circ-30^\circ)=\dfrac{\tan 45^\circ-\tan 30^\circ}{1+\tan 45^\circ\tan 30^\circ}=\dfrac{1-\frac{\sqrt{3}}{3}}{1+\frac{\sqrt{3}}{3}}=\dfrac{3-\sqrt{3}}{3+\sqrt{3}}$。分子分母同乘 $3-\sqrt{3}$：$\dfrac{(3-\sqrt{3})^2}{9-3}=\dfrac{12-6\sqrt{3}}{6}=2-\sqrt{3}$。

answer

$2-\sqrt{3}$

scene_spec.objects[0]

单位圆中 $15^\circ$ 角与 $45^\circ-30^\circ$ 分解

scene_spec.objects[1]

和角公式 $\tan(45^\circ-30^\circ)$ 的代数代入动画

scene_spec.steps[0]

第一步：以和角公式为主线，建立数学分析·三角恒等式场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：单位圆中 $15^\circ$ 角与 $45^\circ-30^\circ$ 分解。

scene_spec.steps[2]

第三步：和角公式 $\tan(45^\circ-30^\circ)$ 的代数代入动画。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

单位圆中 $15^\circ$ 角与 $45^\circ-30^\circ$ 分解

efficiency_tags[1]

和角公式 $\tan(45^\circ-30^\circ)$ 的代数代入动画

## eval-calc-012-s2

problem

求 $\tan 15^\circ$ 的精确值。

solution

$\tan 15^\circ=\tan\dfrac{30^\circ}{2}=\dfrac{1-\cos 30^\circ}{\sin 30^\circ}=\dfrac{1-\frac{\sqrt{3}}{2}}{\frac{1}{2}}=2-\sqrt{3}$。

answer

$2-\sqrt{3}$

scene_spec.objects[0]

$30^\circ$ 角的角平分线构造

scene_spec.objects[1]

半角公式 $\tan\dfrac{\theta}{2}=\dfrac{1-\cos\theta}{\sin\theta}$ 的标注

scene_spec.steps[0]

第一步：以半角公式为主线，建立数学分析·三角恒等式场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：$30^\circ$ 角的角平分线构造。

scene_spec.steps[2]

第三步：半角公式 $\tan\dfrac{\theta}{2}=\dfrac{1-\cos\theta}{\sin\theta}$ 的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

$30^\circ$ 角的角平分线构造

efficiency_tags[1]

半角公式 $\tan\dfrac{\theta}{2}=\dfrac{1-\cos\theta}{\sin\theta}$ 的标注

## eval-calc-012-s3

problem

求 $\tan 15^\circ$ 的精确值。

solution

取直角三角形$ABC$，$\angle B=\pi/2$，$AB=\sqrt3,\ BC=1,\ AC=2$，则$\angle A=\pi/6$。其角平分线$AD$与$BC$交于$D$。由角平分线定理$BD/DC=AB/AC=\sqrt3/2$及$BD+DC=1$，得$BD=\sqrt3/(2+\sqrt3)$。在直角三角形$ABD$中$\angle BAD=\pi/12$，故$\tan(\pi/12)=BD/AB=1/(2+\sqrt3)=2-\sqrt3$。再由余角关系$\tan(5\pi/12)=1/\tan(\pi/12)=2+\sqrt3$。

answer

$2-\sqrt{3}$

scene_spec.objects[0]

直角三角形$AB=\sqrt3,\ BC=1,\ AC=2$及角平分线$AD$

scene_spec.objects[1]

$BD/DC=\sqrt3/2$，$BD=\sqrt3/(2+\sqrt3)$

scene_spec.objects[2]

$\tan(\pi/12)=BD/AB=2-\sqrt3$

scene_spec.steps[0]

呈现题干及适用条件：求 $\tan 15^\circ$ 的精确值。

scene_spec.steps[1]

依次呈现：直角三角形$AB=\sqrt3,\ BC=1,\ AC=2$及角平分线$AD$

scene_spec.steps[2]

依次呈现：$BD/DC=\sqrt3/2$，$BD=\sqrt3/(2+\sqrt3)$

scene_spec.steps[3]

依次呈现：$\tan(\pi/12)=BD/AB=2-\sqrt3$

scene_spec.steps[4]

核对完整证明：取直角三角形$ABC$，$\angle B=\pi/2$，$AB=\sqrt3,\ BC=1,\ AC=2$，则$\angle A=\pi/6$。其角平分线$AD$与$BC$交于$D$。由角平分线定理$BD/DC=AB/AC=\sqrt3/2$及$BD+DC=1$，得$BD=\sqrt3/(2+\sqrt3)$。在直角三角形$ABD$中$\angle BAD=\pi/12$，故$\tan(\pi/12)=BD/AB=1/(2+\sqrt3)=2-\sqrt3$。再由余角关系$\tan(5\pi/12)=1/\tan(\pi/12)=2+\sqrt3$。

scene_spec.steps[5]

高亮结果：$2-\sqrt{3}$

efficiency_tags[0]

直角三角形$AB=\sqrt3,\ BC=1,\ AC=2$及角平分线$AD$

efficiency_tags[1]

$BD/DC=\sqrt3/2$，$BD=\sqrt3/(2+\sqrt3)$

efficiency_tags[2]

$\tan(\pi/12)=BD/AB=2-\sqrt3$

## eval-calc-013-s1

problem

求不定积分 $\displaystyle\int x^2e^x\,dx$。

solution

第一次：$\int x^2e^xdx=x^2e^x-2\int xe^xdx$。第二次：$\int xe^xdx=xe^x-\int e^xdx=(x-1)e^x$。故原式 $=x^2e^x-2(x-1)e^x+C=(x^2-2x+2)e^x+C$。

answer

$(x^2-2x+2)e^x+C$

scene_spec.objects[0]

两次分部积分的逐步拆解

scene_spec.objects[1]

每次 $u,dv$ 选取的标注

scene_spec.steps[0]

第一步：以分部积分两次为主线，建立数学分析·不定积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：两次分部积分的逐步拆解。

scene_spec.steps[2]

第三步：每次 $u,dv$ 选取的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

两次分部积分的逐步拆解

efficiency_tags[1]

每次 $u,dv$ 选取的标注

## eval-calc-013-s2

problem

求不定积分 $\displaystyle\int x^2e^x\,dx$。

solution

因被积函数是 $x^2e^x$，设原函数为 $(ax^2+bx+c)e^x$。求导比对：$\left[(ax^2+bx+c)e^x\right]'=\left[ax^2+(2a+b)x+(b+c)\right]e^x\equiv x^2e^x$，故 $a=1$，$2a+b=0\Rightarrow b=-2$，$b+c=0\Rightarrow c=2$，得 $(x^2-2x+2)e^x$。

answer

$(x^2-2x+2)e^x+C$

scene_spec.objects[0]

待定系数 $(ax^2+bx+c)e^x$ 的求导比对动画

scene_spec.objects[1]

系数 $a,b,c$ 的方程组求解

scene_spec.steps[0]

第一步：以待定系数法为主线，建立数学分析·不定积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：待定系数 $(ax^2+bx+c)e^x$ 的求导比对动画。

scene_spec.steps[2]

第三步：系数 $a,b,c$ 的方程组求解。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

待定系数 $(ax^2+bx+c)e^x$ 的求导比对动画

efficiency_tags[1]

系数 $a,b,c$ 的方程组求解

## eval-calc-013-s3

problem

求不定积分 $\displaystyle\int x^2e^x\,dx$。

solution

记 $I_n=\int x^ne^xdx$，分部得 $I_n=x^ne^x-nI_{n-1}$。$I_0=e^x$，$I_1=xe^x-I_0=(x-1)e^x$，$I_2=x^2e^x-2I_1=(x^2-2x+2)e^x$。

answer

$(x^2-2x+2)e^x+C$

scene_spec.objects[0]

递推链 $I_0\to I_1\to I_2$ 的流程图

scene_spec.objects[1]

递推式 $I_n=x^ne^x-nI_{n-1}$ 的标注

scene_spec.steps[0]

第一步：以递推公式为主线，建立数学分析·不定积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：递推链 $I_0\to I_1\to I_2$ 的流程图。

scene_spec.steps[2]

第三步：递推式 $I_n=x^ne^x-nI_{n-1}$ 的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

递推链 $I_0\to I_1\to I_2$ 的流程图

efficiency_tags[1]

递推式 $I_n=x^ne^x-nI_{n-1}$ 的标注

## eval-calc-014-s1

problem

求不定积分 $\displaystyle\int\dfrac{dx}{\sin x}$，并说明不同形式答案的等价性。

solution

$\dfrac{1}{\sin x}=\dfrac{1}{2\sin\frac{x}{2}\cos\frac{x}{2}}=\dfrac{\dfrac{1}{2}\sec^2\frac{x}{2}}{\tan\frac{x}{2}}$。故 $\int\dfrac{dx}{\sin x}=\int\dfrac{d\left(\tan\frac{x}{2}\right)}{\tan\frac{x}{2}}=\ln\left|\tan\dfrac{x}{2}\right|+C$。

answer

$\ln\left|\tan\dfrac{x}{2}\right|+C$（等价于 $\ln|\csc x-\cot x|+C$）

scene_spec.objects[0]

半角恒等式 $\dfrac{1}{\sin x}=\dfrac{\sec^2(x/2)/2}{\tan(x/2)}$ 的变形动画

scene_spec.objects[1]

凑微分 $\dfrac{d(\tan(x/2))}{\tan(x/2)}$ 的高亮

scene_spec.steps[0]

第一步：以半角变形为主线，建立数学分析·不定积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：半角恒等式 $\dfrac{1}{\sin x}=\dfrac{\sec^2(x/2)/2}{\tan(x/2)}$ 的变形动画。

scene_spec.steps[2]

第三步：凑微分 $\dfrac{d(\tan(x/2))}{\tan(x/2)}$ 的高亮。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

半角恒等式 $\dfrac{1}{\sin x}=\dfrac{\sec^2(x/2)/2}{\tan(x/2)}$ 的变形动画

efficiency_tags[1]

凑微分 $\dfrac{d(\tan(x/2))}{\tan(x/2)}$ 的高亮

## eval-calc-014-s2

problem

求不定积分 $\displaystyle\int\dfrac{dx}{\sin x}$，并说明不同形式答案的等价性。

solution

令 $t=\tan\dfrac{x}{2}$，则 $\sin x=\dfrac{2t}{1+t^2}$，$dx=\dfrac{2dt}{1+t^2}$。原式 $=\int\dfrac{1+t^2}{2t}\cdot\dfrac{2dt}{1+t^2}=\int\dfrac{dt}{t}=\ln|t|+C=\ln\left|\tan\dfrac{x}{2}\right|+C$。

answer

$\ln\left|\tan\dfrac{x}{2}\right|+C$（等价于 $\ln|\csc x-\cot x|+C$）

scene_spec.objects[0]

万能代换三角形（半角 $t=\tan(x/2)$ 的边长对应）

scene_spec.objects[1]

$\sin x=\dfrac{2t}{1+t^2}$、$dx=\dfrac{2dt}{1+t^2}$ 的代入

scene_spec.steps[0]

第一步：以万能代换为主线，建立数学分析·不定积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：万能代换三角形（半角 $t=\tan(x/2)$ 的边长对应）。

scene_spec.steps[2]

第三步：$\sin x=\dfrac{2t}{1+t^2}$、$dx=\dfrac{2dt}{1+t^2}$ 的代入。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

万能代换三角形（半角 $t=\tan(x/2)$ 的边长对应）

efficiency_tags[1]

$\sin x=\dfrac{2t}{1+t^2}$、$dx=\dfrac{2dt}{1+t^2}$ 的代入

## eval-calc-014-s3

problem

求不定积分 $\displaystyle\int\dfrac{dx}{\sin x}$，并说明不同形式答案的等价性。

solution

分子分母同乘 $\csc x-\cot x$：$\int\csc x\,dx=\int\dfrac{\csc x(\csc x-\cot x)}{\csc x-\cot x}dx=\int\dfrac{d(\csc x-\cot x)}{\csc x-\cot x}=\ln|\csc x-\cot x|+C$。由 $\csc x-\cot x=\dfrac{1-\cos x}{\sin x}=\tan\dfrac{x}{2}$ 知两形式完全相同。

answer

$\ln\left|\tan\dfrac{x}{2}\right|+C$（等价于 $\ln|\csc x-\cot x|+C$）

scene_spec.objects[0]

共轭式 $\csc x-\cot x$ 的分子分母同乘动画

scene_spec.objects[1]

两形式答案同框求导验证

scene_spec.steps[0]

第一步：以共轭恒等式为主线，建立数学分析·不定积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：共轭式 $\csc x-\cot x$ 的分子分母同乘动画。

scene_spec.steps[2]

第三步：两形式答案同框求导验证。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

共轭式 $\csc x-\cot x$ 的分子分母同乘动画

efficiency_tags[1]

两形式答案同框求导验证

## eval-calc-015-s1

problem

求定积分 $\displaystyle I=\int_0^\pi\frac{x\sin x}{1+\cos^2 x}\,dx$。

solution

令 $t=\pi-x$，则 $I=\int_0^\pi\dfrac{(\pi-t)\sin t}{1+\cos^2 t}\,dt=\pi\int_0^\pi\dfrac{\sin t}{1+\cos^2 t}\,dt-I$，故 $2I=\pi\int_0^\pi\dfrac{\sin x}{1+\cos^2 x}\,dx$。令 $u=\cos x$（$du=-\sin x\,dx$）：$\int_0^\pi\dfrac{\sin x}{1+\cos^2x}dx=\int_{-1}^{1}\dfrac{du}{1+u^2}=\left[\arctan u\right]_{-1}^{1}=\dfrac{\pi}{2}$。于是 $2I=\pi\cdot\dfrac{\pi}{2}$，$I=\dfrac{\pi^2}{4}$。

answer

$\dfrac{\pi^2}{4}$

scene_spec.objects[0]

区间替换 $t=\pi-x$ 的镜像动画

scene_spec.objects[1]

自指方程 $2I=\pi\int\dfrac{\sin x}{1+\cos^2x}dx$ 的推导高亮

scene_spec.objects[2]

换元 $u=\cos x$ 后 $\arctan$ 区间取值

scene_spec.steps[0]

第一步：以区间替换法，对称性为主线，建立数学分析·定积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：区间替换 $t=\pi-x$ 的镜像动画。

scene_spec.steps[2]

第三步：自指方程 $2I=\pi\int\dfrac{\sin x}{1+\cos^2x}dx$ 的推导高亮。

scene_spec.steps[3]

第四步：换元 $u=\cos x$ 后 $\arctan$ 区间取值。

scene_spec.steps[4]

第五步：高亮最终结果与答案。

efficiency_tags[0]

区间替换 $t=\pi-x$ 的镜像动画

efficiency_tags[1]

自指方程 $2I=\pi\int\dfrac{\sin x}{1+\cos^2x}dx$ 的推导高亮

efficiency_tags[2]

换元 $u=\cos x$ 后 $\arctan$ 区间取值

## eval-calc-015-s2

problem

求定积分 $\displaystyle I=\int_0^\pi\frac{x\sin x}{1+\cos^2 x}\,dx$。

solution

令 $u=x$、$dv=\dfrac{\sin x}{1+\cos^2x}dx$，则 $v=-\arctan(\cos x)$。$I=\left[-x\arctan(\cos x)\right]_0^\pi+\int_0^\pi\arctan(\cos x)dx$。代入上下限：$-\pi\arctan(-1)+0=\dfrac{\pi^2}{4}$，再结合对称性 $\int_0^\pi\arctan(\cos x)dx=0$（被积函数关于 $x=\dfrac{\pi}{2}$ 反对称），得 $I=\dfrac{\pi^2}{4}$。

answer

$\dfrac{\pi^2}{4}$

scene_spec.objects[0]

分部积分 $u=x$、$dv=\dfrac{\sin x}{1+\cos^2x}dx$ 的选取

scene_spec.objects[1]

反对称性 $\int_0^\pi\arctan(\cos x)dx=0$ 的面积抵消

scene_spec.steps[0]

第一步：以分部积分+回代思想为主线，建立数学分析·定积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：分部积分 $u=x$、$dv=\dfrac{\sin x}{1+\cos^2x}dx$ 的选取。

scene_spec.steps[2]

第三步：反对称性 $\int_0^\pi\arctan(\cos x)dx=0$ 的面积抵消。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

分部积分 $u=x$、$dv=\dfrac{\sin x}{1+\cos^2x}dx$ 的选取

efficiency_tags[1]

反对称性 $\int_0^\pi\arctan(\cos x)dx=0$ 的面积抵消

## eval-calc-015-s3

problem

求定积分 $\displaystyle I=\int_0^\pi\frac{x\sin x}{1+\cos^2 x}\,dx$。

solution

设 $g(x)=\sin x/(1+\cos^2x)$。对 $0\le x\le\pi$，有 $g(\pi-x)=g(x)$。作代换 $x=\pi-t$ 得 $I=\int_0^\pi(\pi-t)g(t)\,dt$，与原式相加得 $2I=\pi\int_0^\pi g(x)\,dx$。再令 $u=\cos x$，则 $\int_0^\pi g(x)\,dx=\int_{-1}^1(1+u^2)^{-1}\,du=\arctan1-\arctan(-1)=\pi/2$。故 $I=\pi^2/4$。

answer

$\frac{\pi^2}{4}$

scene_spec.objects[0]

关于区间中点的镜像配对

scene_spec.objects[1]

换元后的精确积分

scene_spec.steps[0]

定义 $g(x)=\sin x/(1+\cos^2x)$，标注 $g(\pi-x)=g(x)$。

scene_spec.steps[1]

镜像配对显示 $2I=\pi\int_0^\pi g(x)\,dx$。

scene_spec.steps[2]

令 $u=\cos x$，得到 $\int_0^\pi g(x)\,dx=\int_{-1}^1(1+u^2)^{-1}\,du=\pi/2$。

scene_spec.steps[3]

显示精确结论 $I=\pi^2/4$，不采用数值积分点列作为证明。

efficiency_tags[0]

数值积分点列逼近 $\pi^2/4$

efficiency_tags[1]

与解析值同框对照

## eval-calc-016-s1

problem

求不定积分 $\displaystyle\int\frac{dx}{(x^2+a^2)^2}$（$a>0$）。

solution

令 $x=a\tan t$，则 $dx=a\sec^2 t\,dt$，$x^2+a^2=a^2\sec^2 t$。原式 $=\displaystyle\int\dfrac{a\sec^2 t}{a^4\sec^4 t}dt=\dfrac{1}{a^3}\int\cos^2 t\,dt=\dfrac{1}{a^3}\left(\dfrac{t}{2}+\dfrac{\sin 2t}{4}\right)+C=\dfrac{1}{a^3}\left(\dfrac{t}{2}+\dfrac{\sin t\cos t}{2}\right)+C$。由直角三角形得 $\sin t=\dfrac{x}{\sqrt{x^2+a^2}}$、$\cos t=\dfrac{a}{\sqrt{x^2+a^2}}$，故原式 $=\dfrac{1}{2a^3}\arctan\dfrac{x}{a}+\dfrac{x}{2a^2(x^2+a^2)}+C$。

answer

$\dfrac{x}{2a^2(x^2+a^2)}+\dfrac{1}{2a^3}\arctan\dfrac{x}{a}+C$

scene_spec.objects[0]

直角三角形替换 $x=a\tan t$ 的边长标注

scene_spec.objects[1]

$\cos^2t$ 的倍角积分与代回

scene_spec.steps[0]

第一步：以三角换元为主线，建立数学分析·不定积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：直角三角形替换 $x=a\tan t$ 的边长标注。

scene_spec.steps[2]

第三步：$\cos^2t$ 的倍角积分与代回。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

直角三角形替换 $x=a\tan t$ 的边长标注

efficiency_tags[1]

$\cos^2t$ 的倍角积分与代回

## eval-calc-016-s2

problem

求不定积分 $\displaystyle\int\frac{dx}{(x^2+a^2)^2}$（$a>0$）。

solution

记 $I_n=\displaystyle\int\dfrac{dx}{(x^2+a^2)^n}$。对 $I_n$ 分部积分（取 $u=\dfrac{1}{(x^2+a^2)^n}$、$dv=dx$）：$I_n=\dfrac{x}{(x^2+a^2)^n}+2n\displaystyle\int\dfrac{x^2}{(x^2+a^2)^{n+1}}dx=\dfrac{x}{(x^2+a^2)^n}+2n\int\dfrac{(x^2+a^2)-a^2}{(x^2+a^2)^{n+1}}dx=\dfrac{x}{(x^2+a^2)^n}+2n(I_n-a^2I_{n+1})$。整理得递推式 $I_{n+1}=\dfrac{1}{2na^2}\left[\dfrac{x}{(x^2+a^2)^n}+(2n-1)I_n\right]$。取 $n=1$ 并以 $I_1=\dfrac{1}{a}\arctan\dfrac{x}{a}$ 代入：$I_2=\dfrac{1}{2a^2}\left[\dfrac{x}{x^2+a^2}+I_1\right]=\dfrac{x}{2a^2(x^2+a^2)}+\dfrac{1}{2a^3}\arctan\dfrac{x}{a}+C$。

answer

$\dfrac{x}{2a^2(x^2+a^2)}+\dfrac{1}{2a^3}\arctan\dfrac{x}{a}+C$

scene_spec.objects[0]

递推链 $I_1\to I_2\to\cdots$ 流程图

scene_spec.objects[1]

分部积分导出递推式 $I_{n+1}=\dfrac{1}{2na^2}\left[\dfrac{x}{(x^2+a^2)^n}+(2n-1)I_n\right]$ 的步骤

scene_spec.steps[0]

第一步：以递推公式为主线，建立数学分析·不定积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：递推链 $I_1\to I_2\to\cdots$ 流程图。

scene_spec.steps[2]

第三步：分部积分导出递推式 $I_{n+1}=\dfrac{1}{2na^2}\left[\dfrac{x}{(x^2+a^2)^n}+(2n-1)I_n\right]$ 的步骤。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

递推链 $I_1\to I_2\to\cdots$ 流程图

efficiency_tags[1]

分部积分导出递推式 $I_{n+1}=\dfrac{1}{2na^2}\left[\dfrac{x}{(x^2+a^2)^n}+(2n-1)I_n\right]$ 的步骤

## eval-calc-016-s3

problem

求不定积分 $\displaystyle\int\frac{dx}{(x^2+a^2)^2}$（$a>0$）。

solution

在复数域 $f(z)=\dfrac{1}{(z^2+a^2)^2}=\dfrac{1}{(z-ai)^2(z+ai)^2}$，实系数保证共轭对称。求系数：$C=\lim_{z\to ai}(z-ai)^2f(z)=\dfrac{1}{(2ai)^2}=-\dfrac{1}{4a^2}$；$D=\lim_{z\to ai}\dfrac{d}{dz}\dfrac{1}{(z+ai)^2}=\dfrac{-2}{(2ai)^3}=\dfrac{1}{4a^3i}=-\dfrac{i}{4a^3}$，共轭 $\bar D=\dfrac{i}{4a^3}$。故 $\dfrac{1}{(x^2+a^2)^2}=-\dfrac{1}{4a^2}\left[\dfrac{1}{(x-ai)^2}+\dfrac{1}{(x+ai)^2}\right]-\dfrac{i}{4a^3}\cdot\dfrac{1}{x-ai}+\dfrac{i}{4a^3}\cdot\dfrac{1}{x+ai}$。逐项积分：第一组 $=\dfrac{1}{4a^2}\left[\dfrac{1}{x-ai}+\dfrac{1}{x+ai}\right]=\dfrac{x}{2a^2(x^2+a^2)}$；第二组 $=\dfrac{i}{4a^3}\left[\ln(x+ai)-\ln(x-ai)\right]=\dfrac{i}{4a^3}\ln\dfrac{x+ai}{x-ai}$。对实数 $x>0$，$|x+ai|=|x-ai|$，且 $\arg\dfrac{x+ai}{x-ai}=2\arg(x+ai)=2\left(\dfrac{\pi}{2}-\arctan\dfrac{x}{a}\right)=\pi-2\arctan\dfrac{x}{a}$，故第二组 $=\dfrac{i}{4a^3}\cdot i\left(\pi-2\arctan\dfrac{x}{a}\right)=\dfrac{1}{2a^3}\arctan\dfrac{x}{a}-\dfrac{\pi}{4a^3}$（常数并入 $C$）；当 $x<0$ 时上述辐角公式超出主值范围，需沿实轴选取连续对数分支，分支差异为常数、并入 $C$ 后不影响原函数（也可分 $x>0$ 与 $x<0$ 两区间分别计算）。合并得 $\dfrac{x}{2a^2(x^2+a^2)}+\dfrac{1}{2a^3}\arctan\dfrac{x}{a}+C$，三法一致。

answer

$\dfrac{x}{2a^2(x^2+a^2)}+\dfrac{1}{2a^3}\arctan\dfrac{x}{a}+C$

scene_spec.objects[0]

复数平面两极点 $z=\pm ai$ 示意

scene_spec.objects[1]

部分分式系数 $C,D$ 的极限求法

scene_spec.objects[2]

辐角分支与实部合并

scene_spec.steps[0]

第一步：以复数部分分式为主线，建立数学分析·不定积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：复数平面两极点 $z=\pm ai$ 示意。

scene_spec.steps[2]

第三步：部分分式系数 $C,D$ 的极限求法。

scene_spec.steps[3]

第四步：辐角分支与实部合并。

scene_spec.steps[4]

第五步：高亮最终结果与答案。

efficiency_tags[0]

复数平面两极点 $z=\pm ai$ 示意

efficiency_tags[1]

部分分式系数 $C,D$ 的极限求法

efficiency_tags[2]

辐角分支与实部合并

## eval-calc-017-s1

problem

求定积分 $\displaystyle I=\int_0^1\frac{\ln(1+x)}{1+x^2}\,dx$。

solution

令 $x=\tan t$（$t:0\to\dfrac{\pi}{4}$），则 $I=\displaystyle\int_0^{\pi/4}\ln(1+\tan t)\,dt$。利用区间替换 $t\to\dfrac{\pi}{4}-t$：$I=\displaystyle\int_0^{\pi/4}\ln\left(1+\tan\left(\frac{\pi}{4}-t\right)\right)dt$。由和角公式 $\tan\left(\dfrac{\pi}{4}-t\right)=\dfrac{1-\tan t}{1+\tan t}$，得 $1+\tan\left(\dfrac{\pi}{4}-t\right)=\dfrac{2}{1+\tan t}$。两式相加：$2I=\displaystyle\int_0^{\pi/4}\left[\ln(1+\tan t)+\ln\dfrac{2}{1+\tan t}\right]dt=\int_0^{\pi/4}\ln 2\,dt=\dfrac{\pi}{4}\ln 2$，故 $I=\dfrac{\pi}{8}\ln 2$。

answer

$\dfrac{\pi}{8}\ln 2$

scene_spec.objects[0]

$x=\tan t$ 把区间映到 $\left[0,\dfrac{\pi}{4}\right]$ 的坐标动画

scene_spec.objects[1]

$t\to\dfrac{\pi}{4}-t$ 镜像对称示意

scene_spec.objects[2]

两式相加得 $2I=\dfrac{\pi}{4}\ln2$ 的自指方程

scene_spec.steps[0]

第一步：以换元+对称性为主线，建立数学分析·定积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：$x=\tan t$ 把区间映到 $\left[0,\dfrac{\pi}{4}\right]$ 的坐标动画。

scene_spec.steps[2]

第三步：$t\to\dfrac{\pi}{4}-t$ 镜像对称示意。

scene_spec.steps[3]

第四步：两式相加得 $2I=\dfrac{\pi}{4}\ln2$ 的自指方程。

scene_spec.steps[4]

第五步：高亮最终结果与答案。

efficiency_tags[0]

$x=\tan t$ 把区间映到 $\left[0,\dfrac{\pi}{4}\right]$ 的坐标动画

efficiency_tags[1]

$t\to\dfrac{\pi}{4}-t$ 镜像对称示意

efficiency_tags[2]

两式相加得 $2I=\dfrac{\pi}{4}\ln2$ 的自指方程

## eval-calc-017-s2

problem

求定积分 $\displaystyle I=\int_0^1\frac{\ln(1+x)}{1+x^2}\,dx$。

solution

令 $x=\dfrac{1-t}{1+t}$（$t:1\to 0$），则 $dx=-\dfrac{2}{(1+t)^2}dt$，且 $1+x=\dfrac{2}{1+t}$、$1+x^2=\dfrac{2(1+t^2)}{(1+t)^2}$。代入得 $I=\displaystyle\int_1^0\dfrac{\ln\frac{2}{1+t}}{\frac{2(1+t^2)}{(1+t)^2}}\cdot\left(-\dfrac{2}{(1+t)^2}\right)dt=\int_0^1\dfrac{\ln 2-\ln(1+t)}{1+t^2}\,dt=\ln 2\int_0^1\dfrac{dt}{1+t^2}-I=\dfrac{\pi}{4}\ln 2-I$（其中 $\int_0^1\dfrac{dt}{1+t^2}=\left[\arctan t\right]_0^1=\dfrac{\pi}{4}$）。故 $2I=\dfrac{\pi}{4}\ln 2$，$I=\dfrac{\pi}{8}\ln 2$。

answer

$\dfrac{\pi}{8}\ln 2$

scene_spec.objects[0]

分式替换 $x=\dfrac{1-t}{1+t}$ 的变量对应动画

scene_spec.objects[1]

$\ln\dfrac{2}{1+t}$ 拆分的变形高亮

scene_spec.steps[0]

第一步：以分式替换为主线，建立数学分析·定积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：分式替换 $x=\dfrac{1-t}{1+t}$ 的变量对应动画。

scene_spec.steps[2]

第三步：$\ln\dfrac{2}{1+t}$ 拆分的变形高亮。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

分式替换 $x=\dfrac{1-t}{1+t}$ 的变量对应动画

efficiency_tags[1]

$\ln\dfrac{2}{1+t}$ 拆分的变形高亮

## eval-calc-017-s3

problem

求定积分 $\displaystyle I=\int_0^1\frac{\ln(1+x)}{1+x^2}\,dx$。

solution

取 $u=\ln(1+x)$、$dv=\dfrac{dx}{1+x^2}$，则 $v=\arctan x$。$I=\left[\ln(1+x)\arctan x\right]_0^1-\displaystyle\int_0^1\dfrac{\arctan x}{1+x}\,dx=\dfrac{\pi}{4}\ln 2-J$，其中 $J=\displaystyle\int_0^1\dfrac{\arctan x}{1+x}dx$。对 $J$ 作替换 $x=\dfrac{1-t}{1+t}$：$dx=-\dfrac{2}{(1+t)^2}dt$，$1+x=\dfrac{2}{1+t}$，且 $\arctan\dfrac{1-t}{1+t}=\dfrac{\pi}{4}-\arctan t$（$t\in[0,1]$，由 $\tan\left(\dfrac{\pi}{4}-\arctan t\right)=\dfrac{1-t}{1+t}$ 得）。故 $J=\displaystyle\int_1^0\left(\frac{\pi}{4}-\arctan t\right)\cdot\frac{1+t}{2}\cdot\left(-\frac{2}{(1+t)^2}\right)dt=\int_0^1\dfrac{\frac{\pi}{4}-\arctan t}{1+t}\,dt=\dfrac{\pi}{4}\ln 2-J$，得 $2J=\dfrac{\pi}{4}\ln 2$，$J=\dfrac{\pi}{8}\ln 2$。于是 $I=\dfrac{\pi}{4}\ln 2-\dfrac{\pi}{8}\ln 2=\dfrac{\pi}{8}\ln 2$。

answer

$\dfrac{\pi}{8}\ln 2$

scene_spec.objects[0]

分部积分 $u=\ln(1+x)$、$dv=\dfrac{dx}{1+x^2}$ 的选取

scene_spec.objects[1]

辅助积分 $J$ 的自指方程推导

scene_spec.steps[0]

第一步：以分部积分+替换为主线，建立数学分析·定积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：分部积分 $u=\ln(1+x)$、$dv=\dfrac{dx}{1+x^2}$ 的选取。

scene_spec.steps[2]

第三步：辅助积分 $J$ 的自指方程推导。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

分部积分 $u=\ln(1+x)$、$dv=\dfrac{dx}{1+x^2}$ 的选取

efficiency_tags[1]

辅助积分 $J$ 的自指方程推导

## eval-calc-018-s1

problem

求不定积分 $\displaystyle\int x\arctan x\,dx$。

solution

令 $u=\arctan x$、$dv=x\,dx$，则 $du=\dfrac{dx}{1+x^2}$、$v=\dfrac{x^2}{2}$。原式 $=\dfrac{x^2}{2}\arctan x-\dfrac{1}{2}\displaystyle\int\dfrac{x^2}{1+x^2}dx=\dfrac{x^2}{2}\arctan x-\dfrac{1}{2}\int\left(1-\dfrac{1}{1+x^2}\right)dx=\dfrac{x^2}{2}\arctan x-\dfrac{x}{2}+\dfrac{1}{2}\arctan x+C=\dfrac{x^2+1}{2}\arctan x-\dfrac{x}{2}+C$。

answer

$\dfrac{x^2+1}{2}\arctan x-\dfrac{x}{2}+C$

scene_spec.objects[0]

分部积分 $u=\arctan x$、$dv=x\,dx$ 的选取

scene_spec.objects[1]

$\dfrac{x^2}{1+x^2}$ 拆成 $1-\dfrac{1}{1+x^2}$ 的化简

scene_spec.steps[0]

第一步：以分部积分：反函数留作 $u$为主线，建立数学分析·不定积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：分部积分 $u=\arctan x$、$dv=x\,dx$ 的选取。

scene_spec.steps[2]

第三步：$\dfrac{x^2}{1+x^2}$ 拆成 $1-\dfrac{1}{1+x^2}$ 的化简。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

分部积分 $u=\arctan x$、$dv=x\,dx$ 的选取

efficiency_tags[1]

$\dfrac{x^2}{1+x^2}$ 拆成 $1-\dfrac{1}{1+x^2}$ 的化简

## eval-calc-018-s2

problem

求不定积分 $\displaystyle\int x\arctan x\,dx$。

solution

令 $t=\arctan x$，则 $x=\tan t$、$dx=\sec^2 t\,dt$。原式 $=\displaystyle\int t\tan t\sec^2 t\,dt=\dfrac{1}{2}\int t\,d(\tan^2 t)=\dfrac{1}{2}t\tan^2 t-\dfrac{1}{2}\int\tan^2 t\,dt=\dfrac{1}{2}t\tan^2 t-\dfrac{1}{2}\int(\sec^2 t-1)dt=\dfrac{1}{2}t(1+\tan^2 t)-\dfrac{1}{2}\tan t+C$。代回 $t=\arctan x$、$\tan t=x$，得 $\dfrac{x^2+1}{2}\arctan x-\dfrac{x}{2}+C$。

answer

$\dfrac{x^2+1}{2}\arctan x-\dfrac{x}{2}+C$

scene_spec.objects[0]

换元 $t=\arctan x$ 的坐标压缩示意

scene_spec.objects[1]

$t\tan t\sec^2t$ 的凑微分 $\dfrac{1}{2}d(\tan^2t)$

scene_spec.steps[0]

第一步：以先换元再分部为主线，建立数学分析·不定积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：换元 $t=\arctan x$ 的坐标压缩示意。

scene_spec.steps[2]

第三步：$t\tan t\sec^2t$ 的凑微分 $\dfrac{1}{2}d(\tan^2t)$。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

换元 $t=\arctan x$ 的坐标压缩示意

efficiency_tags[1]

$t\tan t\sec^2t$ 的凑微分 $\dfrac{1}{2}d(\tan^2t)$

## eval-calc-018-s3

problem

求不定积分 $\displaystyle\int x\arctan x\,dx$。

solution

令 $u=x\arctan x$、$dv=dx$，则 $v=x$、$du=\left(\arctan x+\dfrac{x}{1+x^2}\right)dx$。原式 $=x^2\arctan x-\displaystyle\int x\arctan x\,dx-\int\dfrac{x^2}{1+x^2}dx$，即 $2I=x^2\arctan x-\displaystyle\int\left(1-\dfrac{1}{1+x^2}\right)dx=x^2\arctan x-x+\arctan x$，故 $I=\dfrac{x^2+1}{2}\arctan x-\dfrac{x}{2}+C$。

answer

$\dfrac{x^2+1}{2}\arctan x-\dfrac{x}{2}+C$

scene_spec.objects[0]

整体作 $u=x\arctan x$ 的选取

scene_spec.objects[1]

自指方程 $2I=x^2\arctan x-x+\arctan x$ 的推导

scene_spec.steps[0]

第一步：以分部积分：整体留作 $u$为主线，建立数学分析·不定积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：整体作 $u=x\arctan x$ 的选取。

scene_spec.steps[2]

第三步：自指方程 $2I=x^2\arctan x-x+\arctan x$ 的推导。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

整体作 $u=x\arctan x$ 的选取

efficiency_tags[1]

自指方程 $2I=x^2\arctan x-x+\arctan x$ 的推导

## eval-calc-019-s1

problem

求反常积分 $\displaystyle\int_0^{+\infty}xe^{-x}\,dx$。

solution

先求原函数：令 $u=x$、$dv=e^{-x}dx$，则 $du=dx$、$v=-e^{-x}$，$\displaystyle\int xe^{-x}dx=-xe^{-x}+\int e^{-x}dx=-(x+1)e^{-x}+C$。故 $\displaystyle\int_0^{b}xe^{-x}dx=\left[-(x+1)e^{-x}\right]_0^b=1-(b+1)e^{-b}$。令 $b\to+\infty$：$(b+1)e^{-b}\to 0$（指数衰减快于线性增长），得原积分 $=1$。

answer

$1$

scene_spec.objects[0]

分部积分 $u=x$、$dv=e^{-x}dx$ 的选取

scene_spec.objects[1]

$(b+1)e^{-b}\to0$ 的极限标注

scene_spec.steps[0]

第一步：以分部积分+极限为主线，建立数学分析·反常积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：分部积分 $u=x$、$dv=e^{-x}dx$ 的选取。

scene_spec.steps[2]

第三步：$(b+1)e^{-b}\to0$ 的极限标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

分部积分 $u=x$、$dv=e^{-x}dx$ 的选取

efficiency_tags[1]

$(b+1)e^{-b}\to0$ 的极限标注

## eval-calc-019-s2

problem

求反常积分 $\displaystyle\int_0^{+\infty}xe^{-x}\,dx$。

solution

由 Γ 函数定义 $\Gamma(s)=\displaystyle\int_0^{+\infty}t^{s-1}e^{-t}dt$，原积分 $=\Gamma(2)$。递推：$\Gamma(s+1)=s\Gamma(s)$（分部积分一次即得），且 $\Gamma(1)=\displaystyle\int_0^{+\infty}e^{-t}dt=1$，故 $\Gamma(2)=1\cdot\Gamma(1)=1$。此解法把单个积分放进 Γ 函数家族，可一并处理 $\int_0^{+\infty}x^ne^{-x}dx=\Gamma(n+1)=n!$。

answer

$1$

scene_spec.objects[0]

Γ 函数递推 $\Gamma(s+1)=s\Gamma(s)$ 的示意

scene_spec.objects[1]

$\Gamma(1)=1$ 的基线标注

scene_spec.steps[0]

第一步：以Γ 函数为主线，建立数学分析·反常积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：Γ 函数递推 $\Gamma(s+1)=s\Gamma(s)$ 的示意。

scene_spec.steps[2]

第三步：$\Gamma(1)=1$ 的基线标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

Γ 函数递推 $\Gamma(s+1)=s\Gamma(s)$ 的示意

efficiency_tags[1]

$\Gamma(1)=1$ 的基线标注

## eval-calc-019-s3

problem

求反常积分 $\displaystyle\int_0^{+\infty}xe^{-x}\,dx$。

solution

若 $X\sim\operatorname{Exp}(1)$（参数 $\lambda=1$ 的指数分布），其密度为 $f(x)=e^{-x}$（$x>0$），则原积分 $=E[X]$。由指数分布期望公式 $E[X]=\dfrac{1}{\lambda}=1$；或由尾概率公式 $E[X]=\displaystyle\int_0^{+\infty}P(X>t)dt=\int_0^{+\infty}e^{-t}dt=1$ 得到同一结果。

answer

$1$

scene_spec.objects[0]

指数分布密度 $e^{-x}$ 的峰形曲线与面积填充

scene_spec.objects[1]

横向条带分解（尾概率公式 $\int P(X>t)dt$）

scene_spec.steps[0]

第一步：以概率论视角为主线，建立数学分析·反常积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：指数分布密度 $e^{-x}$ 的峰形曲线与面积填充。

scene_spec.steps[2]

第三步：横向条带分解（尾概率公式 $\int P(X>t)dt$）。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

指数分布密度 $e^{-x}$ 的峰形曲线与面积填充

efficiency_tags[1]

横向条带分解（尾概率公式 $\int P(X>t)dt$）

## eval-calc-020-s1

problem

讨论反常积分 $\displaystyle\int_1^{+\infty}\frac{dx}{x^p}$（$p>0$）的敛散性，并求其收敛时的值。

solution

当 $p\ne 1$ 时，$\displaystyle\int_1^b x^{-p}dx=\left[\dfrac{x^{1-p}}{1-p}\right]_1^b=\dfrac{b^{1-p}-1}{1-p}$。若 $p>1$，则 $1-p<0$，$b^{1-p}\to 0$，积分为 $\dfrac{0-1}{1-p}=\dfrac{1}{p-1}$，收敛；若 $0<p<1$，则 $b^{1-p}\to+\infty$，发散。当 $p=1$ 时 $\displaystyle\int_1^b\dfrac{dx}{x}=\ln b\to+\infty$，发散。综上，$p>1$ 收敛于 $\dfrac{1}{p-1}$，$0<p\le 1$ 发散。

answer

$p>1$ 时收敛于 $\dfrac{1}{p-1}$；$0<p\le 1$ 时发散

scene_spec.objects[0]

有限积分：$p\ne1$时$(b^{1-p}-1)/(1-p)$；$p=1$时$\ln b$

scene_spec.objects[1]

$p>1$收敛于$1/(p-1)$；$0<p\le1$发散

scene_spec.steps[0]

呈现题干及适用条件：讨论反常积分 $\displaystyle\int_1^{+\infty}\frac{dx}{x^p}$（$p>0$）的敛散性，并求其收敛时的值。

scene_spec.steps[1]

依次呈现：有限积分：$p\ne1$时$(b^{1-p}-1)/(1-p)$；$p=1$时$\ln b$

scene_spec.steps[2]

依次呈现：$p>1$收敛于$1/(p-1)$；$0<p\le1$发散

scene_spec.steps[3]

核对完整证明：当 $p\ne 1$ 时，$\displaystyle\int_1^b x^{-p}dx=\left[\dfrac{x^{1-p}}{1-p}\right]_1^b=\dfrac{b^{1-p}-1}{1-p}$。若 $p>1$，则 $1-p<0$，$b^{1-p}\to 0$，积分为 $\dfrac{0-1}{1-p}=\dfrac{1}{p-1}$，收敛；若 $0<p<1$，则 $b^{1-p}\to+\infty$，发散。当 $p=1$ 时 $\displaystyle\int_1^b\dfrac{dx}{x}=\ln b\to+\infty$，发散。综上，$p>1$ 收敛于 $\dfrac{1}{p-1}$，$0<p\le 1$ 发散。

scene_spec.steps[4]

高亮结果：$p>1$ 时收敛于 $\dfrac{1}{p-1}$；$0<p\le 1$ 时发散

efficiency_tags[0]

有限积分：$p\ne1$时$(b^{1-p}-1)/(1-p)$；$p=1$时$\ln b$

efficiency_tags[1]

$p>1$收敛于$1/(p-1)$；$0<p\le1$发散

## eval-calc-020-s2

problem

讨论反常积分 $\displaystyle\int_1^{+\infty}\frac{dx}{x^p}$（$p>0$）的敛散性，并求其收敛时的值。

solution

函数 $f(x)=x^{-p}$ 在 $[1,+\infty)$ 上非负递减，由积分判别法，$\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{n^p}$ 与 $\displaystyle\int_1^{+\infty}\dfrac{dx}{x^p}$ 同敛散，故 $p>1$ 收敛、$p\le 1$ 发散——积分与级数两个世界互相印证。收敛时再直接计算：$\int_1^b x^{-p}dx=(b^{1-p}-1)/(1-p)$（$p\ne1$）；当$p>1$，$b^{1-p}\to0$，所得值为$1/(p-1)$；$p=1$时积分为$\ln b\to\infty$。

answer

$p>1$ 时收敛于 $\dfrac{1}{p-1}$；$0<p\le 1$ 时发散

scene_spec.objects[0]

柱状图与 $y=\dfrac{1}{x^p}$ 曲线的面积夹逼

scene_spec.objects[1]

p 级数与 p 积分的同敛散对应

scene_spec.steps[0]

呈现题干及适用条件：讨论反常积分 $\displaystyle\int_1^{+\infty}\frac{dx}{x^p}$（$p>0$）的敛散性，并求其收敛时的值。

scene_spec.steps[1]

依次呈现：柱状图与 $y=\dfrac{1}{x^p}$ 曲线的面积夹逼

scene_spec.steps[2]

依次呈现：p 级数与 p 积分的同敛散对应

scene_spec.steps[3]

核对完整证明：函数 $f(x)=x^{-p}$ 在 $[1,+\infty)$ 上非负递减，由积分判别法，$\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{n^p}$ 与 $\displaystyle\int_1^{+\infty}\dfrac{dx}{x^p}$ 同敛散，故 $p>1$ 收敛、$p\le 1$ 发散——积分与级数两个世界互相印证。收敛时再直接计算：$\int_1^b x^{-p}dx=(b^{1-p}-1)/(1-p)$（$p\ne1$）；当$p>1$，$b^{1-p}\to0$，所得值为$1/(p-1)$；$p=1$时积分为$\ln b\to\infty$。

scene_spec.steps[4]

高亮结果：$p>1$ 时收敛于 $\dfrac{1}{p-1}$；$0<p\le 1$ 时发散

efficiency_tags[0]

柱状图与 $y=\dfrac{1}{x^p}$ 曲线的面积夹逼

efficiency_tags[1]

p 级数与 p 积分的同敛散对应

## eval-calc-020-s3

problem

讨论反常积分 $\displaystyle\int_1^{+\infty}\frac{dx}{x^p}$（$p>0$）的敛散性，并求其收敛时的值。

solution

对$k\ge0$，在$[2^k,2^{k+1}]$上单调性给出$2^{-p(k+1)}\le x^{-p}\le2^{-pk}$，故$2^{-p}2^{(1-p)k}\le\int_{2^k}^{2^{k+1}}x^{-p}dx\le2^{(1-p)k}$。当$p>1$，右侧按公比$2^{1-p}<1$构成收敛几何级数；当$0<p\le1$，各块的下界至少为$2^{-p}>0$，总面积发散。求收敛值时令$x=e^t$，则$\int_1^\infty x^{-p}dx=\int_0^\infty e^{-(p-1)t}dt=1/(p-1)$（$p>1$）。

answer

$p>1$ 时收敛于 $\dfrac{1}{p-1}$；$0<p\le 1$ 时发散

scene_spec.objects[0]

二进分块$[2^k,2^{k+1}]$及严格上下界

scene_spec.objects[1]

$2^{-p}2^{(1-p)k}\le A_k\le2^{(1-p)k}$

scene_spec.objects[2]

临界$p=1$；收敛值$1/(p-1)$

scene_spec.steps[0]

呈现题干及适用条件：讨论反常积分 $\displaystyle\int_1^{+\infty}\frac{dx}{x^p}$（$p>0$）的敛散性，并求其收敛时的值。

scene_spec.steps[1]

依次呈现：二进分块$[2^k,2^{k+1}]$及严格上下界

scene_spec.steps[2]

依次呈现：$2^{-p}2^{(1-p)k}\le A_k\le2^{(1-p)k}$

scene_spec.steps[3]

依次呈现：临界$p=1$；收敛值$1/(p-1)$

scene_spec.steps[4]

核对完整证明：对$k\ge0$，在$[2^k,2^{k+1}]$上单调性给出$2^{-p(k+1)}\le x^{-p}\le2^{-pk}$，故$2^{-p}2^{(1-p)k}\le\int_{2^k}^{2^{k+1}}x^{-p}dx\le2^{(1-p)k}$。当$p>1$，右侧按公比$2^{1-p}<1$构成收敛几何级数；当$0<p\le1$，各块的下界至少为$2^{-p}>0$，总面积发散。求收敛值时令$x=e^t$，则$\int_1^\infty x^{-p}dx=\int_0^\infty e^{-(p-1)t}dt=1/(p-1)$（$p>1$）。

scene_spec.steps[5]

高亮结果：$p>1$ 时收敛于 $\dfrac{1}{p-1}$；$0<p\le 1$ 时发散

efficiency_tags[0]

二进分块$[2^k,2^{k+1}]$及严格上下界

efficiency_tags[1]

$2^{-p}2^{(1-p)k}\le A_k\le2^{(1-p)k}$

efficiency_tags[2]

临界$p=1$；收敛值$1/(p-1)$

## eval-calc-021-s1

problem

求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n}{2^n}$ 的和。

solution

写 $S=\dfrac{1}{2}+\dfrac{2}{4}+\dfrac{3}{8}+\dfrac{4}{16}+\cdots$，则 $\dfrac{S}{2}=\dfrac{1}{4}+\dfrac{2}{8}+\dfrac{3}{16}+\cdots$。两式相减：$S-\dfrac{S}{2}=\dfrac{1}{2}+\left(\dfrac{2}{4}-\dfrac{1}{4}\right)+\left(\dfrac{3}{8}-\dfrac{2}{8}\right)+\left(\dfrac{4}{16}-\dfrac{3}{16}\right)+\cdots=\dfrac{1}{2}+\dfrac{1}{4}+\dfrac{1}{8}+\dfrac{1}{16}+\cdots=1$（几何级数）。故 $\dfrac{S}{2}=1$，$S=2$。上述无限级数运算的依据为$a_n=n/2^n>0$且$a_{n+1}/a_n=(n+1)/(2n)\to1/2<1$，故绝对收敛；也可直接验证有限和$\sum_{n=1}^N n/2^n=2-(N+2)/2^N$后取极限。

answer

$2$

scene_spec.objects[0]

竖式错位相减逐行对齐

scene_spec.objects[1]

相减后每行系数归一的抵消动画

scene_spec.steps[0]

呈现题干及适用条件：求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n}{2^n}$ 的和。

scene_spec.steps[1]

依次呈现：竖式错位相减逐行对齐

scene_spec.steps[2]

依次呈现：相减后每行系数归一的抵消动画

scene_spec.steps[3]

核对完整证明：写 $S=\dfrac{1}{2}+\dfrac{2}{4}+\dfrac{3}{8}+\dfrac{4}{16}+\cdots$，则 $\dfrac{S}{2}=\dfrac{1}{4}+\dfrac{2}{8}+\dfrac{3}{16}+\cdots$。两式相减：$S-\dfrac{S}{2}=\dfrac{1}{2}+\left(\dfrac{2}{4}-\dfrac{1}{4}\right)+\left(\dfrac{3}{8}-\dfrac{2}{8}\right)+\left(\dfrac{4}{16}-\dfrac{3}{16}\right)+\cdots=\dfrac{1}{2}+\dfrac{1}{4}+\dfrac{1}{8}+\dfrac{1}{16}+\cdots=1$（几何级数）。故 $\dfrac{S}{2}=1$，$S=2$。上述无限级数运算的依据为$a_n=n/2^n>0$且$a_{n+1}/a_n=(n+1)/(2n)\to1/2<1$，故绝对收敛；也可直接验证有限和$\sum_{n=1}^N n/2^n=2-(N+2)/2^N$后取极限。

scene_spec.steps[4]

高亮结果：$2$

efficiency_tags[0]

竖式错位相减逐行对齐

efficiency_tags[1]

相减后每行系数归一的抵消动画

## eval-calc-021-s2

problem

求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n}{2^n}$ 的和。

solution

由等比级数 $\displaystyle\sum_{n=0}^{\infty}x^{n}=\dfrac{1}{1-x}$（$|x|<1$）逐项求导：$\displaystyle\sum_{n=1}^{\infty}nx^{n-1}=\dfrac{1}{(1-x)^2}$，故 $\displaystyle\sum_{n=1}^{\infty}nx^n=\dfrac{x}{(1-x)^2}$。取 $x=\dfrac{1}{2}$，得 $S=\dfrac{1/2}{(1-1/2)^2}=\dfrac{1/2}{1/4}=2$。

answer

$2$

scene_spec.objects[0]

逐项求导 $\sum nx^{n-1}=\dfrac{1}{(1-x)^2}$ 的过程

scene_spec.objects[1]

幂级数曲线在 $x=\dfrac{1}{2}$ 处取点

scene_spec.steps[0]

第一步：以幂级数求和为主线，建立数学分析·一般级数场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：逐项求导 $\sum nx^{n-1}=\dfrac{1}{(1-x)^2}$ 的过程。

scene_spec.steps[2]

第三步：幂级数曲线在 $x=\dfrac{1}{2}$ 处取点。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

逐项求导 $\sum nx^{n-1}=\dfrac{1}{(1-x)^2}$ 的过程

efficiency_tags[1]

幂级数曲线在 $x=\dfrac{1}{2}$ 处取点

## eval-calc-021-s3

problem

求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n}{2^n}$ 的和。

solution

设 $X$ 服从参数 $p=\dfrac{1}{2}$ 的几何分布（抛硬币直到首次正面所需次数），则 $P(X=n)=q^{n-1}p=\left(\dfrac{1}{2}\right)^n$，$E[X]=\displaystyle\sum_{n=1}^{\infty}nq^{n-1}p=p\sum_{n=1}^{\infty}nq^{n-1}=p\cdot\dfrac{1}{(1-q)^2}=\dfrac{1}{p}=2$（其中用到 $\sum nq^{n-1}=\dfrac{1}{(1-q)^2}$）。而 $E[X]=\displaystyle\sum_{n=1}^{\infty}n\left(\dfrac{1}{2}\right)^n=S$，故 $S=2$。

answer

$2$

scene_spec.objects[0]

抛硬币"首次正面次数"的频数直方图

scene_spec.objects[1]

直方图均值收敛于 2

scene_spec.steps[0]

第一步：以概率论：几何分布期望为主线，建立数学分析·一般级数场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：抛硬币"首次正面次数"的频数直方图。

scene_spec.steps[2]

第三步：直方图均值收敛于 2。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

抛硬币"首次正面次数"的频数直方图

efficiency_tags[1]

直方图均值收敛于 2

## eval-calc-022-s1

problem

求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n^2}{2^n}$ 的和。

solution

由 $\displaystyle\sum_{n=1}^{\infty}x^n=\dfrac{x}{1-x}$ 逐项求导两次：先得 $\displaystyle\sum_{n=1}^{\infty}nx^{n-1}=\dfrac{1}{(1-x)^2}$，再得 $\displaystyle\sum_{n=1}^{\infty}n(n-1)x^{n-2}=\dfrac{2}{(1-x)^3}$。于是 $\displaystyle\sum_{n=1}^{\infty}n^2x^n=\sum_{n=1}^{\infty}n(n-1)x^n+\sum_{n=1}^{\infty}nx^n=\dfrac{2x^2}{(1-x)^3}+\dfrac{x}{(1-x)^2}=\dfrac{x(1+x)}{(1-x)^3}$。取 $x=\dfrac{1}{2}$，得 $S=\dfrac{(1/2)(3/2)}{(1/2)^3}=6$。

answer

$6$

scene_spec.objects[0]

两次逐项求导的系数错位动画

scene_spec.objects[1]

$\sum_{n=1}^{\infty}n^2x^n=\dfrac{x(1+x)}{(1-x)^3}\quad(|x|<1)$ 的推导

scene_spec.steps[0]

呈现题干及适用条件：求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n^2}{2^n}$ 的和。

scene_spec.steps[1]

依次呈现：两次逐项求导的系数错位动画

scene_spec.steps[2]

依次呈现：$\sum_{n=1}^{\infty}n^2x^n=\dfrac{x(1+x)}{(1-x)^3}\quad(|x|<1)$ 的推导

scene_spec.steps[3]

核对完整证明：由 $\displaystyle\sum_{n=1}^{\infty}x^n=\dfrac{x}{1-x}$ 逐项求导两次：先得 $\displaystyle\sum_{n=1}^{\infty}nx^{n-1}=\dfrac{1}{(1-x)^2}$，再得 $\displaystyle\sum_{n=1}^{\infty}n(n-1)x^{n-2}=\dfrac{2}{(1-x)^3}$。于是 $\displaystyle\sum_{n=1}^{\infty}n^2x^n=\sum_{n=1}^{\infty}n(n-1)x^n+\sum_{n=1}^{\infty}nx^n=\dfrac{2x^2}{(1-x)^3}+\dfrac{x}{(1-x)^2}=\dfrac{x(1+x)}{(1-x)^3}$。取 $x=\dfrac{1}{2}$，得 $S=\dfrac{(1/2)(3/2)}{(1/2)^3}=6$。

scene_spec.steps[4]

高亮结果：$6$

efficiency_tags[0]

两次逐项求导的系数错位动画

efficiency_tags[1]

$\sum_{n=1}^{\infty}n^2x^n=\dfrac{x(1+x)}{(1-x)^3}\quad(|x|<1)$ 的推导

## eval-calc-022-s2

problem

求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n^2}{2^n}$ 的和。

solution

记 $A=\displaystyle\sum_{n=1}^{\infty}\dfrac{n}{2^n}=2$（eval-calc-021）、$B=\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{2^n}=1$。$\dfrac{S}{2}=\displaystyle\sum_{n=1}^{\infty}\dfrac{n^2}{2^{n+1}}=\sum_{m=2}^{\infty}\dfrac{(m-1)^2}{2^m}$，故 $S-\dfrac{S}{2}=\displaystyle\sum_{n=1}^{\infty}\dfrac{n^2-(n-1)^2}{2^n}=\sum_{n=1}^{\infty}\dfrac{2n-1}{2^n}=2A-B=2\cdot 2-1=3$。于是 $\dfrac{S}{2}=3$，$S=6$。因$a_{n+1}/a_n=(n+1)^2/(2n^2)\to1/2<1$，原级数绝对收敛，所用移项成立。有限和恒等式为$\sum_{n=1}^N n^2/2^n=6-(N^2+4N+6)/2^N$，取极限即得$6$。

answer

$6$

scene_spec.objects[0]

两级错位相减的竖式结构

scene_spec.objects[1]

复用 021 的 $A=2$、$B=1$ 的链式标注

scene_spec.steps[0]

呈现题干及适用条件：求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n^2}{2^n}$ 的和。

scene_spec.steps[1]

依次呈现：两级错位相减的竖式结构

scene_spec.steps[2]

依次呈现：复用 021 的 $A=2$、$B=1$ 的链式标注

scene_spec.steps[3]

核对完整证明：记 $A=\displaystyle\sum_{n=1}^{\infty}\dfrac{n}{2^n}=2$（eval-calc-021）、$B=\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{2^n}=1$。$\dfrac{S}{2}=\displaystyle\sum_{n=1}^{\infty}\dfrac{n^2}{2^{n+1}}=\sum_{m=2}^{\infty}\dfrac{(m-1)^2}{2^m}$，故 $S-\dfrac{S}{2}=\displaystyle\sum_{n=1}^{\infty}\dfrac{n^2-(n-1)^2}{2^n}=\sum_{n=1}^{\infty}\dfrac{2n-1}{2^n}=2A-B=2\cdot 2-1=3$。于是 $\dfrac{S}{2}=3$，$S=6$。因$a_{n+1}/a_n=(n+1)^2/(2n^2)\to1/2<1$，原级数绝对收敛，所用移项成立。有限和恒等式为$\sum_{n=1}^N n^2/2^n=6-(N^2+4N+6)/2^N$，取极限即得$6$。

scene_spec.steps[4]

高亮结果：$6$

efficiency_tags[0]

两级错位相减的竖式结构

efficiency_tags[1]

复用 021 的 $A=2$、$B=1$ 的链式标注

## eval-calc-022-s3

problem

求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n^2}{2^n}$ 的和。

solution

设 $X\sim\operatorname{Geom}(1/2)$（$q=p=\dfrac{1}{2}$）。先算阶乘矩：$E[X(X-1)]=\displaystyle\sum_{k=1}^{\infty}k(k-1)q^{k-1}p=pq\sum_{k=2}^{\infty}k(k-1)q^{k-2}=pq\cdot\dfrac{2}{(1-q)^3}=\dfrac{2q}{p^2}$。故 $E[X^2]=E[X(X-1)]+E[X]=\dfrac{2q}{p^2}+\dfrac{1}{p}=\dfrac{2q+p}{p^2}=\dfrac{2-p}{p^2}$。代入 $p=\dfrac{1}{2}$ 得 $E[X^2]=6$，而 $E[X^2]=\displaystyle\sum_{n=1}^{\infty}n^2\left(\dfrac{1}{2}\right)^n=S$，故 $S=6$。

answer

$6$

scene_spec.objects[0]

阶乘矩 $E[X(X-1)]$ 的求和重整化

scene_spec.objects[1]

$k$ 阶矩与级数逐阶对应

scene_spec.steps[0]

第一步：以概率论：几何分布二阶矩为主线，建立数学分析·一般级数场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：阶乘矩 $E[X(X-1)]$ 的求和重整化。

scene_spec.steps[2]

第三步：$k$ 阶矩与级数逐阶对应。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

阶乘矩 $E[X(X-1)]$ 的求和重整化

efficiency_tags[1]

$k$ 阶矩与级数逐阶对应

## eval-calc-023-s1

problem

证明级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^2}$ 收敛。

solution

$f(x)=\dfrac{1}{x^2}$ 在 $[1,+\infty)$ 上非负递减，且 $\displaystyle\int_1^{+\infty}\dfrac{dx}{x^2}=1$ 收敛（eval-calc-020 的 $p=2$ 情形），由积分判别法，级数 $\sum\dfrac{1}{n^2}$ 收敛。

answer

证毕（三种证法）

scene_spec.objects[0]

坐标系与曲线 $f(x)=1/x^2$（$x\ge1$）

scene_spec.objects[1]

积分区域 $1\le x\le R$ 及面积 $1-1/R$

scene_spec.objects[2]

正项级数 $\sum_{n=1}^{\infty}1/n^2$ 与积分判别法条件

scene_spec.steps[0]

画出正值递减曲线 $f(x)=1/x^2$，明确连续、非负、递减三项条件。

scene_spec.steps[1]

用参数 $R>1$ 高亮曲线下从 $1$ 到 $R$ 的区域，展示 $\int_1^R x^{-2}\,dx=1-1/R$。

scene_spec.steps[2]

令 $R\to\infty$，面积趋于 $1$，说明反常积分收敛。

scene_spec.steps[3]

逐项对应 $a_n=f(n)$，应用积分判别法得到 $\sum1/n^2$ 收敛

efficiency_tags[0]

正值递减曲线 $f(x)=1/x^2$ 的三项条件

efficiency_tags[1]

参数 $R$ 高亮 $[1,R]$ 面积 $1-1/R$

efficiency_tags[2]

$R\to\infty$ 面积趋于 1 与逐项对应 $a_n=f(n)$

## eval-calc-023-s2

problem

证明级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^2}$ 收敛。

solution

当 $n\ge 2$ 时 $\dfrac{1}{n^2}<\dfrac{1}{n(n-1)}=\dfrac{1}{n-1}-\dfrac{1}{n}$。部分和 $S_n=1+\displaystyle\sum_{k=2}^{n}\dfrac{1}{k^2}<1+\sum_{k=2}^{n}\left(\dfrac{1}{k-1}-\dfrac{1}{k}\right)=1+\left(1-\dfrac{1}{n}\right)<2$。正项级数部分和单调递增且有上界 2，故收敛。

answer

证毕（三种证法）

scene_spec.objects[0]

项 $1/n^2$ 与比较项 $1/[n(n-1)]$（$n\ge2$）

scene_spec.objects[1]

裂项恒等式 $1/[n(n-1)]=1/(n-1)-1/n$

scene_spec.objects[2]

部分和 $S_N$ 与上界 $2-1/N$

scene_spec.steps[0]

从 $n\ge2$ 开始，展示 $1/n^2<1/[n(n-1)]$；首项 $1$ 单独保留。

scene_spec.steps[1]

把比较项拆成 $1/(n-1)-1/n$，按相邻项逐项抵消。

scene_spec.steps[2]

给出 $S_N<1+\sum_{n=2}^{N}(1/(n-1)-1/n)=2-1/N<2$（$N\ge2$）。

scene_spec.steps[3]

展示 $S_N$ 递增且有上界，应用单调有界原则证明收敛

efficiency_tags[0]

$1/n^2<1/[n(n-1)]$ 的比较

efficiency_tags[1]

裂项 $1/(n-1)-1/n$ 的逐项抵消

efficiency_tags[2]

部分和上界 $2-1/N<2$ 与单调有界原则

## eval-calc-023-s3

problem

证明级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^2}$ 收敛。

solution

取 $2^k$ 项凝聚：$\displaystyle\sum_{k=1}^{\infty}2^k\cdot\dfrac{1}{(2^k)^2}=\sum_{k=1}^{\infty}\dfrac{1}{2^k}$ 收敛（几何级数），由 Cauchy 凝聚判别法，原级数收敛。

answer

证毕（三种证法）

scene_spec.objects[0]

数列 $a_n=1/n^2$ 及按 $2^k$ 标记的分块

scene_spec.objects[1]

凝聚项 $2^k a_{2^k}=2^{-k}$

scene_spec.objects[2]

几何级数 $\sum_{k=1}^{\infty}2^{-k}$

scene_spec.steps[0]

确认 $a_n$ 正且递减，说明 Cauchy 凝聚判别法的适用条件。

scene_spec.steps[1]

高亮 $2^k$ 对应的样本位置和权重，建立 $2^k/(2^k)^2=2^{-k}$。

scene_spec.steps[2]

把凝聚级数映射到公比 $1/2$ 的几何级数，其和为 $1$；有限初始项不影响收敛性。

scene_spec.steps[3]

应用凝聚判别法回到原级数，结论是收敛

efficiency_tags[0]

$a_n$ 按 $2^k$ 标记的分块

efficiency_tags[1]

凝聚项 $2^k a_{2^k}=2^{-k}$ 的建立

efficiency_tags[2]

公比 $\dfrac{1}{2}$ 几何级数的映射

## eval-calc-024-s1

problem

求 $\arctan x$ 的幂级数展开式，并由此推导莱布尼茨级数 $\dfrac{\pi}{4}=1-\dfrac{1}{3}+\dfrac{1}{5}-\dfrac{1}{7}+\cdots$。

solution

由等比级数 $\dfrac{1}{1+t}=\displaystyle\sum_{n=0}^{\infty}(-1)^nt^{n}$（$|t|<1$），以 $t=x^2$ 代入得 $\dfrac{1}{1+x^2}=\displaystyle\sum_{n=0}^{\infty}(-1)^nx^{2n}$。逐项积分：$\arctan x=\displaystyle\int_0^x\dfrac{dt}{1+t^2}=\sum_{n=0}^{\infty}(-1)^n\int_0^xt^{2n}dt=\sum_{n=0}^{\infty}\dfrac{(-1)^nx^{2n+1}}{2n+1}$（$|x|<1$）。端点也可直接处理：$\frac1{1+t^2}=\sum_{k=0}^N(-1)^kt^{2k}+(-1)^{N+1}\frac{t^{2N+2}}{1+t^2}$。从$0$积分到$x\in[-1,1]$，余项满足$|R_N(x)|\le|x|^{2N+3}/(2N+3)\le1/(2N+3)\to0$，故展开在整个闭区间成立，$x=1$给出$\pi/4=\sum_{k=0}^\infty(-1)^k/(2k+1)$。

answer

$\arctan x=\displaystyle\sum_{n=0}^{\infty}\dfrac{(-1)^n x^{2n+1}}{2n+1}$（$|x|\le 1$）；$x=1$ 时即莱布尼茨级数

scene_spec.objects[0]

等比级数 $\dfrac{1}{1+x^2}=\sum(-1)^nx^{2n}$ 的逐项积分

scene_spec.objects[1]

部分和多项式逐阶逼近 $\arctan x$

scene_spec.steps[0]

呈现题干及适用条件：求 $\arctan x$ 的幂级数展开式，并由此推导莱布尼茨级数 $\dfrac{\pi}{4}=1-\dfrac{1}{3}+\dfrac{1}{5}-\dfrac{1}{7}+\cdots$。

scene_spec.steps[1]

依次呈现：等比级数 $\dfrac{1}{1+x^2}=\sum(-1)^nx^{2n}$ 的逐项积分

scene_spec.steps[2]

依次呈现：部分和多项式逐阶逼近 $\arctan x$

scene_spec.steps[3]

核对完整证明：由等比级数 $\dfrac{1}{1+t}=\displaystyle\sum_{n=0}^{\infty}(-1)^nt^{n}$（$|t|<1$），以 $t=x^2$ 代入得 $\dfrac{1}{1+x^2}=\displaystyle\sum_{n=0}^{\infty}(-1)^nx^{2n}$。逐项积分：$\arctan x=\displaystyle\int_0^x\dfrac{dt}{1+t^2}=\sum_{n=0}^{\infty}(-1)^n\int_0^xt^{2n}dt=\sum_{n=0}^{\infty}\dfrac{(-1)^nx^{2n+1}}{2n+1}$（$|x|<1$）。端点也可直接处理：$\frac1{1+t^2}=\sum_{k=0}^N(-1)^kt^{2k}+(-1)^{N+1}\frac{t^{2N+2}}{1+t^2}$。从$0$积分到$x\in[-1,1]$，余项满足$|R_N(x)|\le|x|^{2N+3}/(2N+3)\le1/(2N+3)\to0$，故展开在整个闭区间成立，$x=1$给出$\pi/4=\sum_{k=0}^\infty(-1)^k/(2k+1)$。

scene_spec.steps[4]

高亮结果：$\arctan x=\displaystyle\sum_{n=0}^{\infty}\dfrac{(-1)^n x^{2n+1}}{2n+1}$（$|x|\le 1$）；$x=1$ 时即莱布尼茨级数

efficiency_tags[0]

等比级数 $\dfrac{1}{1+x^2}=\sum(-1)^nx^{2n}$ 的逐项积分

efficiency_tags[1]

部分和多项式逐阶逼近 $\arctan x$

## eval-calc-024-s2

problem

求 $\arctan x$ 的幂级数展开式，并由此推导莱布尼茨级数 $\dfrac{\pi}{4}=1-\dfrac{1}{3}+\dfrac{1}{5}-\dfrac{1}{7}+\cdots$。

solution

$x=1$ 处级数 $\displaystyle\sum_{n=0}^{\infty}\dfrac{(-1)^n}{2n+1}$ 为交错级数（$a_n=\dfrac{1}{2n+1}\searrow 0$），由莱布尼茨判别法收敛；由 Abel 定理，和函数在 $x=1$ 左连续，故 $\arctan 1=\dfrac{\pi}{4}=1-\dfrac{1}{3}+\dfrac{1}{5}-\dfrac{1}{7}+\cdots$。$x=-1$ 同理（或由奇偶性）。开区间的展开来自几何级数$1/(1+t^2)=\sum_{k=0}^{\infty}(-1)^kt^{2k}$，在任意紧子区间$[-r,r]$（$r<1$）一致收敛，可从$0$逐项积分得到$\arctan x$的幂级数，再结合上述端点收敛及Abel定理。

answer

$\arctan x=\displaystyle\sum_{n=0}^{\infty}\dfrac{(-1)^n x^{2n+1}}{2n+1}$（$|x|\le 1$）；$x=1$ 时即莱布尼茨级数

scene_spec.objects[0]

$x=1$ 处交错级数逐项加减逼近 $\dfrac{\pi}{4}$

scene_spec.objects[1]

Abel 定理左连续的标注

scene_spec.steps[0]

呈现题干及适用条件：求 $\arctan x$ 的幂级数展开式，并由此推导莱布尼茨级数 $\dfrac{\pi}{4}=1-\dfrac{1}{3}+\dfrac{1}{5}-\dfrac{1}{7}+\cdots$。

scene_spec.steps[1]

依次呈现：$x=1$ 处交错级数逐项加减逼近 $\dfrac{\pi}{4}$

scene_spec.steps[2]

依次呈现：Abel 定理左连续的标注

scene_spec.steps[3]

核对完整证明：$x=1$ 处级数 $\displaystyle\sum_{n=0}^{\infty}\dfrac{(-1)^n}{2n+1}$ 为交错级数（$a_n=\dfrac{1}{2n+1}\searrow 0$），由莱布尼茨判别法收敛；由 Abel 定理，和函数在 $x=1$ 左连续，故 $\arctan 1=\dfrac{\pi}{4}=1-\dfrac{1}{3}+\dfrac{1}{5}-\dfrac{1}{7}+\cdots$。$x=-1$ 同理（或由奇偶性）。开区间的展开来自几何级数$1/(1+t^2)=\sum_{k=0}^{\infty}(-1)^kt^{2k}$，在任意紧子区间$[-r,r]$（$r<1$）一致收敛，可从$0$逐项积分得到$\arctan x$的幂级数，再结合上述端点收敛及Abel定理。

scene_spec.steps[4]

高亮结果：$\arctan x=\displaystyle\sum_{n=0}^{\infty}\dfrac{(-1)^n x^{2n+1}}{2n+1}$（$|x|\le 1$）；$x=1$ 时即莱布尼茨级数

efficiency_tags[0]

$x=1$ 处交错级数逐项加减逼近 $\dfrac{\pi}{4}$

efficiency_tags[1]

Abel 定理左连续的标注

## eval-calc-024-s3

problem

求 $\arctan x$ 的幂级数展开式，并由此推导莱布尼茨级数 $\dfrac{\pi}{4}=1-\dfrac{1}{3}+\dfrac{1}{5}-\dfrac{1}{7}+\cdots$。

solution

对 $f(x)=\arctan x$ 用带拉格朗日余项的麦克劳林公式：$f^{(n)}(0)$ 由递推 $f'(x)=\dfrac{1}{1+x^2}$ 逐阶求导给出。对 $\arctan$ 可归纳证明 $|f^{(m)}(t)|\le(m-1)!$（$m\ge 1$，对一切实数 $t$），于是余项 $|R_N(x)|=\dfrac{|f^{(N+1)}(\xi)|}{(N+1)!}|x|^{N+1}\le\dfrac{N!}{(N+1)!}\cdot 1=\dfrac{1}{N+1}\to 0$，对 $|x|\le 1$ 一致成立。故展开式在 $|x|\le 1$ 成立，端点处即莱布尼茨级数。所用导数界可由部分分式严格验证：对$m\ge1$，$f^{(m)}(t)=\frac{(-1)^{m-1}(m-1)!}{2i}[(t-i)^{-m}-(t+i)^{-m}]$，于是$|f^{(m)}(t)|\le(m-1)!(1+t^2)^{-m/2}\le(m-1)!$。同时$f^{(2k+1)}(0)=(-1)^k(2k)!$，$f^{(2k)}(0)=0$；泰勒余项界$1/(N+1)$确实趋于零。

answer

$\arctan x=\displaystyle\sum_{n=0}^{\infty}\dfrac{(-1)^n x^{2n+1}}{2n+1}$（$|x|\le 1$）；$x=1$ 时即莱布尼茨级数

scene_spec.objects[0]

各阶导 $|f^{(m)}(t)|\le(m-1)!$ 的界标注

scene_spec.objects[1]

余项 $\dfrac{1}{N+1}\to0$ 的收敛演示

scene_spec.steps[0]

呈现题干及适用条件：求 $\arctan x$ 的幂级数展开式，并由此推导莱布尼茨级数 $\dfrac{\pi}{4}=1-\dfrac{1}{3}+\dfrac{1}{5}-\dfrac{1}{7}+\cdots$。

scene_spec.steps[1]

依次呈现：各阶导 $|f^{(m)}(t)|\le(m-1)!$ 的界标注

scene_spec.steps[2]

依次呈现：余项 $\dfrac{1}{N+1}\to0$ 的收敛演示

scene_spec.steps[3]

核对完整证明：对 $f(x)=\arctan x$ 用带拉格朗日余项的麦克劳林公式：$f^{(n)}(0)$ 由递推 $f'(x)=\dfrac{1}{1+x^2}$ 逐阶求导给出。对 $\arctan$ 可归纳证明 $|f^{(m)}(t)|\le(m-1)!$（$m\ge 1$，对一切实数 $t$），于是余项 $|R_N(x)|=\dfrac{|f^{(N+1)}(\xi)|}{(N+1)!}|x|^{N+1}\le\dfrac{N!}{(N+1)!}\cdot 1=\dfrac{1}{N+1}\to 0$，对 $|x|\le 1$ 一致成立。故展开式在 $|x|\le 1$ 成立，端点处即莱布尼茨级数。所用导数界可由部分分式严格验证：对$m\ge1$，$f^{(m)}(t)=\frac{(-1)^{m-1}(m-1)!}{2i}[(t-i)^{-m}-(t+i)^{-m}]$，于是$|f^{(m)}(t)|\le(m-1)!(1+t^2)^{-m/2}\le(m-1)!$。同时$f^{(2k+1)}(0)=(-1)^k(2k)!$，$f^{(2k)}(0)=0$；泰勒余项界$1/(N+1)$确实趋于零。

scene_spec.steps[4]

高亮结果：$\arctan x=\displaystyle\sum_{n=0}^{\infty}\dfrac{(-1)^n x^{2n+1}}{2n+1}$（$|x|\le 1$）；$x=1$ 时即莱布尼茨级数

efficiency_tags[0]

各阶导 $|f^{(m)}(t)|\le(m-1)!$ 的界标注

efficiency_tags[1]

余项 $\dfrac{1}{N+1}\to0$ 的收敛演示

## eval-calc-025-s1

problem

讨论级数 $\displaystyle\sum_{n=2}^{\infty}\frac{(-1)^n}{\ln n}$ 的敛散性，若收敛，判断是绝对收敛还是条件收敛。

solution

$a_n=\dfrac{1}{\ln n}$ 单调递减且 $\lim_{n\to\infty}a_n=0$，由莱布尼茨判别法，交错级数 $\displaystyle\sum_{n=2}^{\infty}(-1)^na_n$ 收敛。考察绝对级数 $\displaystyle\sum_{n=2}^{\infty}\dfrac{1}{\ln n}$：当 $n\ge 3$ 时 $\dfrac{1}{\ln n}>\dfrac{1}{n}$（因 $\ln n<n$），而调和级数 $\sum\dfrac{1}{n}$ 发散，由比较判别法绝对级数发散。因此原级数条件收敛。

answer

条件收敛

scene_spec.objects[0]

单调递减项 $a_n=\dfrac{1}{\ln n}$ 的柱状图

scene_spec.objects[1]

与调和级数 $\dfrac{1}{n}$ 的比较标注

scene_spec.steps[0]

第一步：以莱布尼茨判别法+绝对收敛检验为主线，建立数学分析·交错级数场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：单调递减项 $a_n=\dfrac{1}{\ln n}$ 的柱状图。

scene_spec.steps[2]

第三步：与调和级数 $\dfrac{1}{n}$ 的比较标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

单调递减项 $a_n=\dfrac{1}{\ln n}$ 的柱状图

efficiency_tags[1]

与调和级数 $\dfrac{1}{n}$ 的比较标注

## eval-calc-025-s2

problem

讨论级数 $\displaystyle\sum_{n=2}^{\infty}\frac{(-1)^n}{\ln n}$ 的敛散性，若收敛，判断是绝对收敛还是条件收敛。

solution

记 $a_n=\dfrac{1}{\ln n}$，$S_n=\displaystyle\sum_{k=2}^{n}(-1)^ka_k$。配对求和：$S_{2m+1}=\displaystyle\sum_{j=1}^{m}(a_{2j}-a_{2j+1})$，每项为正，故奇子列 $S_{2m+1}$ 随 $m$ 递增；又 $a_{2j}-a_{2j+1}<a_{2j}-a_{2j+2}$，故 $S_{2m+1}<\displaystyle\sum_{j=1}^{m}(a_{2j}-a_{2j+2})=\dfrac{1}{\ln 2}-\dfrac{1}{\ln(2m+2)}<\dfrac{1}{\ln 2}$，奇子列有上界，收敛。偶子列 $S_{2m}=S_{2m+1}+a_{2m+1}$，与奇子列之差 $a_{2m+1}\to 0$，故 $S_n$ 收敛。绝对发散仍由解法一的比较法给出。

answer

条件收敛

scene_spec.objects[0]

奇子列 $S_{2m+1}$ 递增有上界的折线

scene_spec.objects[1]

偶子列 $S_{2m}$ 与奇子列之差 $a_{2m+1}\to0$ 的配对相消放大

scene_spec.steps[0]

第一步：以部分和分组估计为主线，建立数学分析·交错级数场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：奇子列 $S_{2m+1}$ 递增有上界的折线。

scene_spec.steps[2]

第三步：偶子列 $S_{2m}$ 与奇子列之差 $a_{2m+1}\to0$ 的配对相消放大。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

奇子列 $S_{2m+1}$ 递增有上界的折线

efficiency_tags[1]

偶子列 $S_{2m}$ 与奇子列之差 $a_{2m+1}\to0$ 的配对相消放大

## eval-calc-025-s3

problem

讨论级数 $\displaystyle\sum_{n=2}^{\infty}\frac{(-1)^n}{\ln n}$ 的敛散性，若收敛，判断是绝对收敛还是条件收敛。

solution

令$a_n=1/\ln n$（$n\ge2$），则$a_n\downarrow0$。对任意$p\ge2$，令$B_j=\sum_{n=p}^j(-1)^n$，有$|B_j|\le1$。Abel分部求和给出$\sum_{n=p}^q(-1)^na_n=B_qa_q+\sum_{j=p}^{q-1}B_j(a_j-a_{j+1})$，故其绝对值不超过$a_q+\sum_{j=p}^{q-1}(a_j-a_{j+1})=a_p\to0$，由Cauchy准则交错级数收敛。绝对级数的有限和满足$\sum_{n=2}^N1/\ln n\ge(N-1)/\ln N\to\infty$，其中$\ln N/N\to0$由洛必达法则得到。因此是条件收敛。

answer

条件收敛

scene_spec.objects[0]

交错部分和振荡收敛折线

scene_spec.objects[1]

绝对级数部分和单调发散对比

scene_spec.steps[0]

呈现题干及适用条件：讨论级数 $\displaystyle\sum_{n=2}^{\infty}\frac{(-1)^n}{\ln n}$ 的敛散性，若收敛，判断是绝对收敛还是条件收敛。

scene_spec.steps[1]

依次呈现：交错部分和振荡收敛折线

scene_spec.steps[2]

依次呈现：绝对级数部分和单调发散对比

scene_spec.steps[3]

核对完整证明：令$a_n=1/\ln n$（$n\ge2$），则$a_n\downarrow0$。对任意$p\ge2$，令$B_j=\sum_{n=p}^j(-1)^n$，有$|B_j|\le1$。Abel分部求和给出$\sum_{n=p}^q(-1)^na_n=B_qa_q+\sum_{j=p}^{q-1}B_j(a_j-a_{j+1})$，故其绝对值不超过$a_q+\sum_{j=p}^{q-1}(a_j-a_{j+1})=a_p\to0$，由Cauchy准则交错级数收敛。绝对级数的有限和满足$\sum_{n=2}^N1/\ln n\ge(N-1)/\ln N\to\infty$，其中$\ln N/N\to0$由洛必达法则得到。因此是条件收敛。

scene_spec.steps[4]

高亮结果：条件收敛

efficiency_tags[0]

交错部分和振荡收敛折线

efficiency_tags[1]

绝对级数部分和单调发散对比

## eval-calc-026-s1

problem

设 $z=x^y$（$x>0$），求 $z$ 在点 $(1,2)$ 处的两个偏导数。

solution

把 $y$ 视为常数：$z_x=yx^{y-1}$，故 $z_x(1,2)=2\cdot 1^{2-1}=2$。把 $x$ 视为常数：$z_y=x^y\ln x$，故 $z_y(1,2)=1^2\cdot\ln 1=0$。

answer

$z_x(1,2)=2$，$z_y(1,2)=0$

scene_spec.objects[0]

沿 $x$ 方向固定 $y=2$ 的截面曲线 $z=x^2$

scene_spec.objects[1]

沿 $y$ 方向固定 $x=1$ 的截面曲线 $z=1^y$

scene_spec.steps[0]

第一步：以直接按定义求偏导为主线，建立数学分析·多元函数微分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：沿 $x$ 方向固定 $y=2$ 的截面曲线 $z=x^2$。

scene_spec.steps[2]

第三步：沿 $y$ 方向固定 $x=1$ 的截面曲线 $z=1^y$。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

沿 $x$ 方向固定 $y=2$ 的截面曲线 $z=x^2$

efficiency_tags[1]

沿 $y$ 方向固定 $x=1$ 的截面曲线 $z=1^y$

## eval-calc-026-s2

problem

设 $z=x^y$（$x>0$），求 $z$ 在点 $(1,2)$ 处的两个偏导数。

solution

对 $\ln z=y\ln x$ 两边求全微分：$\dfrac{dz}{z}=\dfrac{y}{x}dx+\ln x\,dy$。在 $(1,2)$ 处 $z=1$、$\dfrac{y}{x}=2$、$\ln x=0$，故 $dz=2\,dx+0\cdot dy$，即 $z_x=2$、$z_y=0$。

answer

$z_x(1,2)=2$，$z_y(1,2)=0$

scene_spec.objects[0]

全微分 $\dfrac{dz}{z}=\dfrac{y}{x}dx+\ln x\,dy$ 的推导

scene_spec.objects[1]

切平面沿 $x$ 倾斜、沿 $y$ 水平的标注

scene_spec.steps[0]

第一步：以全微分为主线，建立数学分析·多元函数微分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：全微分 $\dfrac{dz}{z}=\dfrac{y}{x}dx+\ln x\,dy$ 的推导。

scene_spec.steps[2]

第三步：切平面沿 $x$ 倾斜、沿 $y$ 水平的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

全微分 $\dfrac{dz}{z}=\dfrac{y}{x}dx+\ln x\,dy$ 的推导

efficiency_tags[1]

切平面沿 $x$ 倾斜、沿 $y$ 水平的标注

## eval-calc-026-s3

problem

设 $z=x^y$（$x>0$），求 $z$ 在点 $(1,2)$ 处的两个偏导数。

solution

按偏导数定义，$z_x(1,2)=\lim_{h\to0}\frac{(1+h)^2-1}{h}=\lim_{h\to0}(2+h)=2$，其中 $h\ne0$ 且充分小时 $1+h>0$。另一方面，$z_y(1,2)=\lim_{h\to0}\frac{1^{2+h}-1}{h}=\lim_{h\to0}0=0$。两个结果均由极限定义精确得到。

answer

$z_x(1,2)=2$，$z_y(1,2)=0$。

scene_spec.objects[0]

两个方向的差商

scene_spec.objects[1]

精确极限等式

scene_spec.steps[0]

沿 $x$ 方向显示差商 $((1+h)^2-1)/h=2+h$，其中 $h\ne0$ 且 $1+h>0$。

scene_spec.steps[1]

令 $h\to0$ 得 $z_x(1,2)=2$。

scene_spec.steps[2]

沿 $y$ 方向显示 $(1^{2+h}-1)/h=0$，所以 $z_y(1,2)=0$。

scene_spec.steps[3]

步长收缩图示精确极限定义，不用固定步长数值差分替代偏导数。

efficiency_tags[0]

差分步长 $h$ 收缩动画

efficiency_tags[1]

两方向差商分别趋近 2 与 0

## eval-calc-027-s1

problem

求二重积分 $\displaystyle I=\int_0^1\!\!\int_x^1 e^{y^2}\,dy\,dx$。

solution

积分区域为 $D=\{(x,y):0\le x\le 1,\ x\le y\le 1\}=\{(x,y):0\le y\le 1,\ 0\le x\le y\}$。交换次序：$I=\displaystyle\int_0^1\!\!\int_0^y e^{y^2}\,dx\,dy=\int_0^1 y\,e^{y^2}\,dy$。令 $u=y^2$（$du=2y\,dy$）：$I=\dfrac{1}{2}\displaystyle\int_0^1 e^u\,du=\dfrac{1}{2}(e-1)$。

answer

$\dfrac{e-1}{2}$

scene_spec.objects[0]

积分区域 $D$ 竖条扫描受阻的演示

scene_spec.objects[1]

换为横条扫描后 $y\,e^{y^2}$ 的一气呵成

scene_spec.objects[2]

换序前后对照

scene_spec.steps[0]

第一步：以交换积分次序为主线，建立数学分析·重积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：积分区域 $D$ 竖条扫描受阻的演示。

scene_spec.steps[2]

第三步：换为横条扫描后 $y\,e^{y^2}$ 的一气呵成。

scene_spec.steps[3]

第四步：换序前后对照。

scene_spec.steps[4]

第五步：高亮最终结果与答案。

efficiency_tags[0]

积分区域 $D$ 竖条扫描受阻的演示

efficiency_tags[1]

换为横条扫描后 $y\,e^{y^2}$ 的一气呵成

efficiency_tags[2]

换序前后对照

## eval-calc-027-s2

problem

求二重积分 $\displaystyle I=\int_0^1\!\!\int_x^1 e^{y^2}\,dy\,dx$。

solution

记 $F(x)=\displaystyle\int_x^1e^{y^2}dy$，则 $I=\displaystyle\int_0^1F(x)dx$，且 $F(1)=0$、$F'(x)=-e^{x^2}$。分部积分：$I=\left[xF(x)\right]_0^1-\displaystyle\int_0^1xF'(x)dx=0-\int_0^1x\left(-e^{x^2}\right)dx=\int_0^1xe^{x^2}dx=\left[\dfrac{e^{x^2}}{2}\right]_0^1=\dfrac{e-1}{2}$。

answer

$\dfrac{e-1}{2}$

scene_spec.objects[0]

分部积分 $u=F(x)$、$dv=dx$ 的选取

scene_spec.objects[1]

边界项 $xF(x)\big|_0^1=0$ 的标注

scene_spec.objects[2]

$F'=-e^{x^2}$ 的代入

scene_spec.steps[0]

第一步：以分部积分为主线，建立数学分析·重积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：分部积分 $u=F(x)$、$dv=dx$ 的选取。

scene_spec.steps[2]

第三步：边界项 $xF(x)\big|_0^1=0$ 的标注。

scene_spec.steps[3]

第四步：$F'=-e^{x^2}$ 的代入。

scene_spec.steps[4]

第五步：高亮最终结果与答案。

efficiency_tags[0]

分部积分 $u=F(x)$、$dv=dx$ 的选取

efficiency_tags[1]

边界项 $xF(x)\big|_0^1=0$ 的标注

efficiency_tags[2]

$F'=-e^{x^2}$ 的代入

## eval-calc-027-s3

problem

求二重积分 $\displaystyle I=\int_0^1\!\!\int_x^1 e^{y^2}\,dy\,dx$。

solution

积分区域为 $D=\{(x,y):0\le x\le y\le1\}$。被积函数连续，故可交换积分次序：$I=\int_0^1\int_0^y e^{y^2}\,dx\,dy=\int_0^1 y e^{y^2}\,dy$。令 $u=y^2$，得到 $I=\frac12\int_0^1e^u\,du=\frac{e-1}{2}$。

answer

$\frac{e-1}{2}$

scene_spec.objects[0]

$D=\{(x,y):0\le x\le y\le1\}$

scene_spec.objects[1]

积分换序与代换

scene_spec.steps[0]

画出三角形 $D$ 并标注被积函数连续，可以交换次序。

scene_spec.steps[1]

显示 $I=\int_0^1\int_0^y e^{y^2}\,dx\,dy=\int_0^1y e^{y^2}\,dy$。

scene_spec.steps[2]

令 $u=y^2$，得 $I=\frac12\int_0^1e^u\,du=(e-1)/2$。

efficiency_tags[0]

三角域 $D=\{(x,y):0\le x\le y\le1\}$ 与积分换序

efficiency_tags[1]

精确积分 $I=\frac12\int_0^1e^u\,du=\frac{e-1}{2}$

## eval-calc-028-s1

problem

求二重积分 $\displaystyle I=\iint_D(x^2+y^2)\,dA$，其中 $D=\{(x,y):x^2+y^2\le 2y\}$。

solution

$D$ 是圆心 $(0,1)$、半径 $1$ 的圆盘，极坐标下边界 $r=2\sin\theta$（$\theta\in[0,\pi]$），且 $x^2+y^2=r^2$、$dA=r\,dr\,d\theta$。$I=\displaystyle\int_0^{\pi}\!\!\int_0^{2\sin\theta}r^2\cdot r\,dr\,d\theta=\int_0^{\pi}\left[\dfrac{r^4}{4}\right]_0^{2\sin\theta}d\theta=\int_0^{\pi}4\sin^4\theta\,d\theta$。由 $\displaystyle\int_0^{\pi}\sin^4\theta\,d\theta=\dfrac{3\pi}{8}$（倍角降次即得），故 $I=4\cdot\dfrac{3\pi}{8}=\dfrac{3\pi}{2}$。

answer

$\dfrac{3\pi}{2}$

scene_spec.objects[0]

圆盘 $D$ 与极角 $\theta\in[0,\pi]$ 的扇形扫描

scene_spec.objects[1]

$r^4$ 径向积分与 $\sin^4\theta$ 的倍角降次

scene_spec.steps[0]

第一步：以极坐标为主线，建立数学分析·重积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：圆盘 $D$ 与极角 $\theta\in[0,\pi]$ 的扇形扫描。

scene_spec.steps[2]

第三步：$r^4$ 径向积分与 $\sin^4\theta$ 的倍角降次。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

圆盘 $D$ 与极角 $\theta\in[0,\pi]$ 的扇形扫描

efficiency_tags[1]

$r^4$ 径向积分与 $\sin^4\theta$ 的倍角降次

## eval-calc-028-s2

problem

求二重积分 $\displaystyle I=\iint_D(x^2+y^2)\,dA$，其中 $D=\{(x,y):x^2+y^2\le 2y\}$。

solution

$D:0\le y\le 2,\ -\sqrt{2y-y^2}\le x\le\sqrt{2y-y^2}$。先对 $x$ 积分：内层 $=\left[\dfrac{x^3}{3}+xy^2\right]_{-\sqrt{2y-y^2}}^{\sqrt{2y-y^2}}=2\left[\dfrac{(2y-y^2)^{3/2}}{3}+y^2\sqrt{2y-y^2}\right]=2\sqrt{2y-y^2}\left[\dfrac{2y-y^2}{3}+y^2\right]=\dfrac{4}{3}y(1+y)\sqrt{2y-y^2}$。故 $I=\dfrac{4}{3}\displaystyle\int_0^2 y(1+y)\sqrt{2y-y^2}\,dy$。令 $u=y-1$（平移至圆心），则 $y(1+y)=(1+u)(2+u)=2+3u+u^2$，$\sqrt{2y-y^2}=\sqrt{1-u^2}$，$u:-1\to 1$。$I=\dfrac{4}{3}\displaystyle\int_{-1}^{1}(2+3u+u^2)\sqrt{1-u^2}\,du=\dfrac{4}{3}\left[2\cdot\dfrac{\pi}{2}+3\cdot 0+\dfrac{\pi}{8}\right]=\dfrac{4}{3}\cdot\dfrac{9\pi}{8}=\dfrac{3\pi}{2}$（其中 $\int_{-1}^{1}\sqrt{1-u^2}du=\dfrac{\pi}{2}$ 为半圆面积，$u\sqrt{1-u^2}$ 为奇函数积分为 0，$\int_{-1}^{1}u^2\sqrt{1-u^2}du=\dfrac{\pi}{8}$ 由三角代换 $u=\sin t$ 即得）。

answer

$\dfrac{3\pi}{2}$

scene_spec.objects[0]

水平条带平移 $u=y-1$ 的示意

scene_spec.objects[1]

三个标准积分 $\dfrac{\pi}{2},0,\dfrac{\pi}{8}$ 的分解标注

scene_spec.steps[0]

第一步：以直角坐标为主线，建立数学分析·重积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：水平条带平移 $u=y-1$ 的示意。

scene_spec.steps[2]

第三步：三个标准积分 $\dfrac{\pi}{2},0,\dfrac{\pi}{8}$ 的分解标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

水平条带平移 $u=y-1$ 的示意

efficiency_tags[1]

三个标准积分 $\dfrac{\pi}{2},0,\dfrac{\pi}{8}$ 的分解标注

## eval-calc-028-s3

problem

求二重积分 $\displaystyle I=\iint_D(x^2+y^2)\,dA$，其中 $D=\{(x,y):x^2+y^2\le 2y\}$。

solution

被积函数 $x^2+y^2$ 是到原点的距离平方，积分即区域 $D$ 关于原点 $O$ 的极惯性矩 $J_O$。由平行轴定理 $J_O=J_C+Ad^2$，其中 $J_C$ 是圆盘关于自身圆心 $C$ 的极惯性矩 $J_C=\dfrac{\pi R^4}{2}=\dfrac{\pi}{2}$，$A=\pi$ 为面积，$d=|OC|=1$ 为圆心到原点的距离。故 $I=J_O=\dfrac{\pi}{2}+\pi\cdot 1^2=\dfrac{3\pi}{2}$。

answer

$\dfrac{3\pi}{2}$

scene_spec.objects[0]

平行轴定理的物理示意（圆盘+偏心距 $d=1$）

scene_spec.objects[1]

$J_C=\dfrac{\pi R^4}{2}$ 与 $Ad^2$ 的叠加

scene_spec.steps[0]

第一步：以平行轴定理/极惯性矩为主线，建立数学分析·重积分场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：平行轴定理的物理示意（圆盘+偏心距 $d=1$）。

scene_spec.steps[2]

第三步：$J_C=\dfrac{\pi R^4}{2}$ 与 $Ad^2$ 的叠加。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

平行轴定理的物理示意（圆盘+偏心距 $d=1$）

efficiency_tags[1]

$J_C=\dfrac{\pi R^4}{2}$ 与 $Ad^2$ 的叠加

## eval-calc-029-s1

problem

求星形线 $x^{2/3}+y^{2/3}=a^{2/3}$（$a>0$）的周长。

solution

参数化 $x=a\cos^3 t$、$y=a\sin^3 t$（$t\in[0,2\pi]$）。$x'=-3a\cos^2 t\sin t$，$y'=3a\sin^2 t\cos t$，弧长微元 $ds=\sqrt{(x')^2+(y')^2}\,dt=\sqrt{9a^2\cos^4 t\sin^2 t+9a^2\sin^4 t\cos^2 t}\,dt=3a|\sin t\cos t|\,dt$。由对称性取第一象限：$L=4\displaystyle\int_0^{\pi/2}3a\sin t\cos t\,dt=12a\left[\dfrac{\sin^2 t}{2}\right]_0^{\pi/2}=12a\cdot\dfrac{1}{2}=6a$。

answer

$6a$

scene_spec.objects[0]

弧长微元 $ds=3a|\sin t\cos t|dt$ 沿曲线移动

scene_spec.objects[1]

四分之一对称性叠加

scene_spec.steps[0]

第一步：以参数方程弧长为主线，建立数学分析·定积分的应用场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：弧长微元 $ds=3a|\sin t\cos t|dt$ 沿曲线移动。

scene_spec.steps[2]

第三步：四分之一对称性叠加。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

弧长微元 $ds=3a|\sin t\cos t|dt$ 沿曲线移动

efficiency_tags[1]

四分之一对称性叠加

## eval-calc-029-s2

problem

求星形线 $x^{2/3}+y^{2/3}=a^{2/3}$（$a>0$）的周长。

solution

由隐函数求导（eval-calc-007）$y'=-\left(\dfrac{y}{x}\right)^{1/3}$，故弧长微元 $ds=\sqrt{1+(y')^2}\,dx=\sqrt{1+(y/x)^{2/3}}\,dx=\sqrt{\dfrac{x^{2/3}+y^{2/3}}{x^{2/3}}}\,dx$。由星形线方程 $x^{2/3}+y^{2/3}=a^{2/3}$，得 $ds=a^{1/3}x^{-1/3}dx$。第一象限部分：$L_1=\displaystyle\int_0^a a^{1/3}x^{-1/3}dx=a^{1/3}\left[\dfrac{3}{2}x^{2/3}\right]_0^a=\dfrac{3a}{2}$，故 $L=4L_1=6a$。上述$x$积分限定在第一象限$0<x\le a$，其中$ds=a^{1/3}x^{-1/3}|dx|$；从$x=0$到$a$积分可写为$a^{1/3}\int_0^a x^{-1/3}dx=3a/2$，端点按反常积分收敛处理，再由四象限对称得$6a$。

answer

$6a$

scene_spec.objects[0]

隐式导数 $y'=-(y/x)^{1/3}$ 的推导

scene_spec.objects[1]

$ds=a^{1/3}x^{-1/3}|dx|\quad(0<x\le a)$ 的化简与积分

scene_spec.steps[0]

呈现题干及适用条件：求星形线 $x^{2/3}+y^{2/3}=a^{2/3}$（$a>0$）的周长。

scene_spec.steps[1]

依次呈现：隐式导数 $y'=-(y/x)^{1/3}$ 的推导

scene_spec.steps[2]

依次呈现：$ds=a^{1/3}x^{-1/3}|dx|\quad(0<x\le a)$ 的化简与积分

scene_spec.steps[3]

核对完整证明：由隐函数求导（eval-calc-007）$y'=-\left(\dfrac{y}{x}\right)^{1/3}$，故弧长微元 $ds=\sqrt{1+(y')^2}\,dx=\sqrt{1+(y/x)^{2/3}}\,dx=\sqrt{\dfrac{x^{2/3}+y^{2/3}}{x^{2/3}}}\,dx$。由星形线方程 $x^{2/3}+y^{2/3}=a^{2/3}$，得 $ds=a^{1/3}x^{-1/3}dx$。第一象限部分：$L_1=\displaystyle\int_0^a a^{1/3}x^{-1/3}dx=a^{1/3}\left[\dfrac{3}{2}x^{2/3}\right]_0^a=\dfrac{3a}{2}$，故 $L=4L_1=6a$。上述$x$积分限定在第一象限$0<x\le a$，其中$ds=a^{1/3}x^{-1/3}|dx|$；从$x=0$到$a$积分可写为$a^{1/3}\int_0^a x^{-1/3}dx=3a/2$，端点按反常积分收敛处理，再由四象限对称得$6a$。

scene_spec.steps[4]

高亮结果：$6a$

efficiency_tags[0]

隐式导数 $y'=-(y/x)^{1/3}$ 的推导

efficiency_tags[1]

$ds=a^{1/3}x^{-1/3}|dx|\quad(0<x\le a)$ 的化简与积分

## eval-calc-029-s3

problem

求星形线 $x^{2/3}+y^{2/3}=a^{2/3}$（$a>0$）的周长。

solution

考虑两端分别在坐标轴上、长为 $a$ 的滑动线段：端点 $E_1(t)=(a\cos t,0)$、$E_2(t)=(0,a\sin t)$。线段上参数 $v\in[0,1]$ 的点为 $P(t,v)=\big(a(1-v)\cos t,\ a v\sin t\big)$。包络条件 $\dfrac{\partial P}{\partial t}$ 与 $\dfrac{\partial P}{\partial v}$ 平行：$\left(-a(1-v)\sin t,\ av\cos t\right)$ 与 $\left(-a\cos t,\ a\sin t\right)$ 平行，叉积为零：$-a^2(1-v)\sin^2 t+a^2v\cos^2 t=0$，解得 $v=\sin^2 t$。代入得包络点 $\big(a\cos t(1-\sin^2 t),\ a\sin^3 t\big)=\big(a\cos^3 t,\ a\sin^3 t\big)$——正是星形线。于是星形线是定长滑动线段的包络，其弧长即解法一的参数曲线弧长：四分之一部分 $\displaystyle\int_0^{\pi/2}3a\sin t\cos t\,dt=\dfrac{3a}{2}$，全长 $6a$。

answer

$6a$

scene_spec.objects[0]

滑动线段包络生成星形线

scene_spec.objects[1]

包络条件叉积为零的推导

scene_spec.objects[2]

切点把切线分成 $a\sin^2t$ 与 $a\cos^2t$ 的标注

scene_spec.steps[0]

第一步：以滑动线段包络法为主线，建立数学分析·定积分的应用场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：滑动线段包络生成星形线。

scene_spec.steps[2]

第三步：包络条件叉积为零的推导。

scene_spec.steps[3]

第四步：切点把切线分成 $a\sin^2t$ 与 $a\cos^2t$ 的标注。

scene_spec.steps[4]

第五步：高亮最终结果与答案。

efficiency_tags[0]

滑动线段包络生成星形线

efficiency_tags[1]

包络条件叉积为零的推导

efficiency_tags[2]

切点把切线分成 $a\sin^2t$ 与 $a\cos^2t$ 的标注

## eval-calc-030-s1

problem

求由 $y=\sin x$（$0\le x\le\pi$）与 $x$ 轴围成的区域绕 $y$ 轴旋转所得旋转体的体积。

solution

在 $x$ 处取高度 $\sin x$、厚度 $dx$ 的竖直壳层，其体积微元 $dV=2\pi x\sin x\,dx$。$V=\displaystyle\int_0^{\pi}2\pi x\sin x\,dx$。分部积分（$u=x$、$dv=\sin x\,dx$）：$\displaystyle\int_0^{\pi}x\sin x\,dx=\left[-x\cos x\right]_0^{\pi}+\int_0^{\pi}\cos x\,dx=\pi+\left[\sin x\right]_0^{\pi}=\pi$。故 $V=2\pi\cdot\pi=2\pi^2$。

answer

$2\pi^2$

scene_spec.objects[0]

竖直壳层扫掠并展开成薄板

scene_spec.objects[1]

分部积分 $\int x\sin x\,dx$ 的步骤

scene_spec.steps[0]

第一步：以壳层法为主线，建立数学分析·定积分的应用场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：竖直壳层扫掠并展开成薄板。

scene_spec.steps[2]

第三步：分部积分 $\int x\sin x\,dx$ 的步骤。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

竖直壳层扫掠并展开成薄板

efficiency_tags[1]

分部积分 $\int x\sin x\,dx$ 的步骤

## eval-calc-030-s2

problem

求由 $y=\sin x$（$0\le x\le\pi$）与 $x$ 轴围成的区域绕 $y$ 轴旋转所得旋转体的体积。

solution

区域面积 $A=\displaystyle\int_0^\pi\sin x\,dx=\left[-\cos x\right]_0^\pi=2$。质心横坐标 $\bar x=\dfrac{1}{A}\displaystyle\int_0^\pi x\sin x\,dx=\dfrac{\pi}{2}$（区域关于 $x=\dfrac{\pi}{2}$ 对称，且上式已算出积分为 $\pi$）。由帕普斯定理（绕 $y$ 轴，轴不穿过区域内部），$V=2\pi\bar x A=2\pi\cdot\dfrac{\pi}{2}\cdot 2=2\pi^2$。

answer

$2\pi^2$

scene_spec.objects[0]

质心横坐标 $\bar x=\dfrac{\pi}{2}$ 的标注

scene_spec.objects[1]

帕普斯旋转示意（质心轨迹圆）

scene_spec.steps[0]

第一步：以帕普斯定理为主线，建立数学分析·定积分的应用场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：质心横坐标 $\bar x=\dfrac{\pi}{2}$ 的标注。

scene_spec.steps[2]

第三步：帕普斯旋转示意（质心轨迹圆）。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

质心横坐标 $\bar x=\dfrac{\pi}{2}$ 的标注

efficiency_tags[1]

帕普斯旋转示意（质心轨迹圆）

## eval-calc-030-s3

problem

求由 $y=\sin x$（$0\le x\le\pi$）与 $x$ 轴围成的区域绕 $y$ 轴旋转所得旋转体的体积。

solution

绕 $y$ 轴时取水平圆盘：对 $0\le y\le 1$，水平线 $y$ 与区域相交于 $x=\arcsin y$（左）与 $x=\pi-\arcsin y$（右），圆盘外半径 $R=\pi-\arcsin y$、内半径 $r=\arcsin y$。$V=\pi\displaystyle\int_0^1\left[(\pi-\arcsin y)^2-(\arcsin y)^2\right]dy=\pi\int_0^1(\pi^2-2\pi\arcsin y)\,dy=\pi\left[\pi^2y-2\pi\int_0^1\arcsin y\,dy\right]$。其中 $\displaystyle\int_0^1\arcsin y\,dy=\left[y\arcsin y+\sqrt{1-y^2}\right]_0^1=\dfrac{\pi}{2}-1$。故 $V=\pi\left[\pi^2-2\pi\left(\dfrac{\pi}{2}-1\right)\right]=\pi\left[\pi^2-\pi^2+2\pi\right]=2\pi^2$。

answer

$2\pi^2$

scene_spec.objects[0]

水平圆环的外、内半径 $\pi-\arcsin y$ 与 $\arcsin y$

scene_spec.objects[1]

环形截面随 $y$ 扫掠

scene_spec.steps[0]

呈现题干及适用条件：求由 $y=\sin x$（$0\le x\le\pi$）与 $x$ 轴围成的区域绕 $y$ 轴旋转所得旋转体的体积。

scene_spec.steps[1]

依次呈现：水平圆环的外、内半径 $\pi-\arcsin y$ 与 $\arcsin y$

scene_spec.steps[2]

依次呈现：环形截面随 $y$ 扫掠

scene_spec.steps[3]

核对完整证明：绕 $y$ 轴时取水平圆盘：对 $0\le y\le 1$，水平线 $y$ 与区域相交于 $x=\arcsin y$（左）与 $x=\pi-\arcsin y$（右），圆盘外半径 $R=\pi-\arcsin y$、内半径 $r=\arcsin y$。$V=\pi\displaystyle\int_0^1\left[(\pi-\arcsin y)^2-(\arcsin y)^2\right]dy=\pi\int_0^1(\pi^2-2\pi\arcsin y)\,dy=\pi\left[\pi^2y-2\pi\int_0^1\arcsin y\,dy\right]$。其中 $\displaystyle\int_0^1\arcsin y\,dy=\left[y\arcsin y+\sqrt{1-y^2}\right]_0^1=\dfrac{\pi}{2}-1$。故 $V=\pi\left[\pi^2-2\pi\left(\dfrac{\pi}{2}-1\right)\right]=\pi\left[\pi^2-\pi^2+2\pi\right]=2\pi^2$。

scene_spec.steps[4]

高亮结果：$2\pi^2$

efficiency_tags[0]

水平圆环的外、内半径 $\pi-\arcsin y$ 与 $\arcsin y$

efficiency_tags[1]

环形截面随 $y$ 扫掠

## eval-geom-001-s1

problem

求点 $P(1,2,-1)$ 到平面 $\pi:2x-y+2z=3$ 的距离。

solution

平面法向量 $\vec n=(2,-1,2)$，$|\vec n|=\sqrt{4+1+4}=3$。代入点到平面距离公式：$d=\dfrac{|2\cdot 1-1\cdot 2+2\cdot(-1)-3|}{3}=\dfrac{|2-2-2-3|}{3}=\dfrac{5}{3}$。

answer

$\dfrac{5}{3}$

scene_spec.objects[0]

三维平面与法向量 $\vec n=(2,-1,2)$

scene_spec.objects[1]

距离公式分子绝对值的标注

scene_spec.steps[0]

第一步：以距离公式为主线，建立解析几何·直线与平面场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：三维平面与法向量 $\vec n=(2,-1,2)$。

scene_spec.steps[2]

第三步：距离公式分子绝对值的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

三维平面与法向量 $\vec n=(2,-1,2)$

efficiency_tags[1]

距离公式分子绝对值的标注

## eval-geom-001-s2

problem

求点 $P(1,2,-1)$ 到平面 $\pi:2x-y+2z=3$ 的距离。

solution

取平面上一点 $Q(0,-3,0)$（$2\cdot 0-(-3)+2\cdot 0=3$ 满足方程），则 $\overrightarrow{QP}=(1,5,-1)$。$P$ 到平面的距离等于 $\overrightarrow{QP}$ 在法向量上的投影长度：$d=\dfrac{|\overrightarrow{QP}\cdot\vec n|}{|\vec n|}=\dfrac{|1\cdot 2+5\cdot(-1)+(-1)\cdot 2|}{3}=\dfrac{5}{3}$。垂足为 $P$ 减去投影向量 $\dfrac{\overrightarrow{QP}\cdot\vec n}{|\vec n|^2}\vec n=\dfrac{-5}{9}(2,-1,2)$，即 $\left(\dfrac{19}{9},\dfrac{13}{9},\dfrac{1}{9}\right)$。

answer

$\dfrac{5}{3}$

scene_spec.objects[0]

投影向量的分解动画

scene_spec.objects[1]

垂足 $\left(\dfrac{19}{9},\dfrac{13}{9},\dfrac{1}{9}\right)$ 坐标标注

scene_spec.steps[0]

第一步：以投影向量为主线，建立解析几何·直线与平面场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：投影向量的分解动画。

scene_spec.steps[2]

第三步：垂足 $\left(\dfrac{19}{9},\dfrac{13}{9},\dfrac{1}{9}\right)$ 坐标标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

投影向量的分解动画

efficiency_tags[1]

垂足 $\left(\dfrac{19}{9},\dfrac{13}{9},\dfrac{1}{9}\right)$ 坐标标注

## eval-geom-001-s3

problem

求点 $P(1,2,-1)$ 到平面 $\pi:2x-y+2z=3$ 的距离。

solution

求 $f(x,y,z)=(x-1)^2+(y-2)^2+(z+1)^2$ 在约束 $2x-y+2z-3=0$ 下的最小值。由 $\nabla f=\lambda\nabla(2x-y+2z-3)$：$2(x-1)=2\lambda$，$2(y-2)=-\lambda$，$2(z+1)=2\lambda$，得 $x-1=\lambda$，$y-2=-\dfrac{\lambda}{2}$，$z+1=\lambda$。代入约束：$2(1+\lambda)-\left(2-\dfrac{\lambda}{2}\right)+2(\lambda-1)=3$，即 $\dfrac{9\lambda}{2}-2=3$，解得 $\lambda=\dfrac{10}{9}$。最近距离 $d=\sqrt{\lambda^2+\dfrac{\lambda^2}{4}+\lambda^2}=\dfrac{3}{2}|\lambda|=\dfrac{5}{3}$。在约束平面内，设垂足$Q=(19/9,13/9,1/9)$；$P-Q$与平面法向量平行，故对任意平面内$X$有$(P-Q)\cdot(X-Q)=0$。因此$|P-X|^2=|P-Q|^2+|X-Q|^2=25/9+|X-Q|^2\ge25/9$，等号只在$X=Q$取到，证明此驻点是唯一全局极小点。

answer

$\dfrac{5}{3}$

scene_spec.objects[0]

约束平面上的等高线

scene_spec.objects[1]

梯度与法向量平行的最优点标注

scene_spec.steps[0]

呈现题干及适用条件：求点 $P(1,2,-1)$ 到平面 $\pi:2x-y+2z=3$ 的距离。

scene_spec.steps[1]

依次呈现：约束平面上的等高线

scene_spec.steps[2]

依次呈现：梯度与法向量平行的最优点标注

scene_spec.steps[3]

核对完整证明：求 $f(x,y,z)=(x-1)^2+(y-2)^2+(z+1)^2$ 在约束 $2x-y+2z-3=0$ 下的最小值。由 $\nabla f=\lambda\nabla(2x-y+2z-3)$：$2(x-1)=2\lambda$，$2(y-2)=-\lambda$，$2(z+1)=2\lambda$，得 $x-1=\lambda$，$y-2=-\dfrac{\lambda}{2}$，$z+1=\lambda$。代入约束：$2(1+\lambda)-\left(2-\dfrac{\lambda}{2}\right)+2(\lambda-1)=3$，即 $\dfrac{9\lambda}{2}-2=3$，解得 $\lambda=\dfrac{10}{9}$。最近距离 $d=\sqrt{\lambda^2+\dfrac{\lambda^2}{4}+\lambda^2}=\dfrac{3}{2}|\lambda|=\dfrac{5}{3}$。在约束平面内，设垂足$Q=(19/9,13/9,1/9)$；$P-Q$与平面法向量平行，故对任意平面内$X$有$(P-Q)\cdot(X-Q)=0$。因此$|P-X|^2=|P-Q|^2+|X-Q|^2=25/9+|X-Q|^2\ge25/9$，等号只在$X=Q$取到，证明此驻点是唯一全局极小点。

scene_spec.steps[4]

高亮结果：$\dfrac{5}{3}$

efficiency_tags[0]

约束平面上的等高线

efficiency_tags[1]

梯度与法向量平行的最优点标注

## eval-geom-002-s1

problem

判断两条直线 $l_1:\dfrac{x-1}{2}=\dfrac{y+1}{1}=\dfrac{z-2}{-1}$ 与 $l_2:\dfrac{x+1}{1}=\dfrac{y-2}{2}=\dfrac{z}{1}$ 的位置关系。

solution

$l_1$ 的方向向量 $\vec{s_1}=(2,1,-1)$，$l_2$ 的 $\vec{s_2}=(1,2,1)$。叉积 $\vec{s_1}\times\vec{s_2}=(1\cdot 1-(-1)\cdot 2,\ (-1)\cdot 1-2\cdot 1,\ 2\cdot 2-1\cdot 1)=(3,-3,3)\ne\vec 0$，故不平行。取 $P_1(1,-1,2)\in l_1$、$P_2(-1,2,0)\in l_2$，$\overrightarrow{P_1P_2}=(-2,3,-2)$。混合积 $\overrightarrow{P_1P_2}\cdot(\vec{s_1}\times\vec{s_2})=-2\cdot 3+3\cdot(-3)+(-2)\cdot 3=-21\ne 0$，故两直线不共面，即异面。

answer

异面直线

scene_spec.objects[0]

叉积 $\vec{s_1}\times\vec{s_2}=(3,-3,3)$ 的方向动画

scene_spec.objects[1]

混合积 $-21\ne0$ 的平行六面体示意

scene_spec.steps[0]

第一步：以混合积判别为主线，建立解析几何·直线与平面场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：叉积 $\vec{s_1}\times\vec{s_2}=(3,-3,3)$ 的方向动画。

scene_spec.steps[2]

第三步：混合积 $-21\ne0$ 的平行六面体示意。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

叉积 $\vec{s_1}\times\vec{s_2}=(3,-3,3)$ 的方向动画

efficiency_tags[1]

混合积 $-21\ne0$ 的平行六面体示意

## eval-geom-002-s2

problem

判断两条直线 $l_1:\dfrac{x-1}{2}=\dfrac{y+1}{1}=\dfrac{z-2}{-1}$ 与 $l_2:\dfrac{x+1}{1}=\dfrac{y-2}{2}=\dfrac{z}{1}$ 的位置关系。

solution

参数化：$l_1:(1+2t,-1+t,2-t)$，$l_2:(-1+s,2+2s,s)$。若相交，需 $1+2t=-1+s$、$-1+t=2+2s$、$2-t=s$ 同时成立。由第三式 $s=2-t$ 代入第一式：$1+2t=-1+2-t$，得 $t=0$、$s=2$；代入第二式检验：$-1+0=2+4$，即 $-1=6$，矛盾。故无公共点；结合方向向量不平行，得异面。

answer

异面直线

scene_spec.objects[0]

参数方程三式联立的代入动画

scene_spec.objects[1]

矛盾式 $-1=6$ 的高亮

scene_spec.steps[0]

第一步：以方程组判别为主线，建立解析几何·直线与平面场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：参数方程三式联立的代入动画。

scene_spec.steps[2]

第三步：矛盾式 $-1=6$ 的高亮。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

参数方程三式联立的代入动画

efficiency_tags[1]

矛盾式 $-1=6$ 的高亮

## eval-geom-002-s3

problem

判断两条直线 $l_1:\dfrac{x-1}{2}=\dfrac{y+1}{1}=\dfrac{z-2}{-1}$ 与 $l_2:\dfrac{x+1}{1}=\dfrac{y-2}{2}=\dfrac{z}{1}$ 的位置关系。

solution

两方向$d_1=(2,1,-1)$、$d_2=(1,2,1)$满足$d_1\times d_2=(3,-3,3)\ne0$，故不平行。两基点差$\Delta=(-2,3,-2)$与叉积的内积为$-21\ne0$；若相交，则$\Delta$必在$\operatorname{span}\{d_1,d_2\}$中，内积应为零，矛盾。因此两线不相交且不平行，是异面直线。

answer

异面直线

scene_spec.objects[0]

三维两直线与方向向量箭头

scene_spec.objects[1]

视角旋转揭示"看似相交"

scene_spec.steps[0]

呈现题干及适用条件：判断两条直线 $l_1:\dfrac{x-1}{2}=\dfrac{y+1}{1}=\dfrac{z-2}{-1}$ 与 $l_2:\dfrac{x+1}{1}=\dfrac{y-2}{2}=\dfrac{z}{1}$ 的位置关系。

scene_spec.steps[1]

依次呈现：三维两直线与方向向量箭头

scene_spec.steps[2]

依次呈现：视角旋转揭示"看似相交"

scene_spec.steps[3]

核对完整证明：两方向$d_1=(2,1,-1)$、$d_2=(1,2,1)$满足$d_1\times d_2=(3,-3,3)\ne0$，故不平行。两基点差$\Delta=(-2,3,-2)$与叉积的内积为$-21\ne0$；若相交，则$\Delta$必在$\operatorname{span}\{d_1,d_2\}$中，内积应为零，矛盾。因此两线不相交且不平行，是异面直线。

scene_spec.steps[4]

高亮结果：异面直线

efficiency_tags[0]

三维两直线与方向向量箭头

efficiency_tags[1]

视角旋转揭示"看似相交"

## eval-geom-003-s1

problem

求过直线 $l:\dfrac{x-1}{1}=\dfrac{y}{2}=\dfrac{z+1}{1}$ 且垂直于平面 $\pi:x+y+z=0$ 的平面方程。

solution

直线方向 $\vec s=(1,2,1)$，$\pi$ 的法向量 $\vec{n_1}=(1,1,1)$。所求平面含直线 $l$ 且垂直于 $\pi$，故其法向量 $\vec n\perp\vec s$ 且 $\vec n\perp\vec{n_1}$，取 $\vec n=\vec s\times\vec{n_1}=(2\cdot 1-1\cdot 1,\ 1\cdot 1-1\cdot 1,\ 1\cdot 1-2\cdot 1)=(1,0,-1)$。过直线上一点 $P_0(1,0,-1)$：$1\cdot(x-1)+0\cdot y+(-1)\cdot(z+1)=0$，即 $x-z=2$。检验：直线上点 $(1+t,2t,-1+t)$ 满足 $(1+t)-(-1+t)=2$；$|\vec n\cdot\vec{n_1}|=|1-1|=0$ 故与 $\pi$ 垂直。

answer

$x-z=2$

scene_spec.objects[0]

法向量叉积 $\vec n=\vec s\times\vec{n_1}=(1,0,-1)$ 的方向动画

scene_spec.objects[1]

直线 $l$ 与平面 $\pi$ 的三维展示

scene_spec.steps[0]

第一步：以法向量叉积为主线，建立解析几何·直线与平面场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：法向量叉积 $\vec n=\vec s\times\vec{n_1}=(1,0,-1)$ 的方向动画。

scene_spec.steps[2]

第三步：直线 $l$ 与平面 $\pi$ 的三维展示。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

法向量叉积 $\vec n=\vec s\times\vec{n_1}=(1,0,-1)$ 的方向动画

efficiency_tags[1]

直线 $l$ 与平面 $\pi$ 的三维展示

## eval-geom-003-s2

problem

求过直线 $l:\dfrac{x-1}{1}=\dfrac{y}{2}=\dfrac{z+1}{1}$ 且垂直于平面 $\pi:x+y+z=0$ 的平面方程。

solution

把 $l$ 写成两平面交线：由 $\dfrac{x-1}{1}=\dfrac{y}{2}$ 得 $y=2x-2$，由 $\dfrac{y}{2}=\dfrac{z+1}{1}$ 得 $y=2z+2$。过 $l$ 的平面束为 $(2x-2-y)+\lambda(2z+2-y)=0$，其法向量为 $(2,-1-\lambda,2\lambda)$。与 $\pi$ 垂直要求 $2\cdot 1+(-1-\lambda)\cdot 1+2\lambda\cdot 1=0$，即 $1+\lambda=0$，$\lambda=-1$。代入：$(2x-2-y)-(2z+2-y)=0$，即 $2x-2z-4=0$，$x-z=2$。

answer

$x-z=2$

scene_spec.objects[0]

平面束 $(2x-2-y)+\lambda(2z+2-y)=0$ 旋转扫描到垂直位置

scene_spec.objects[1]

垂直条件 $1+\lambda=0$ 的求解

scene_spec.steps[0]

第一步：以平面束为主线，建立解析几何·直线与平面场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：平面束 $(2x-2-y)+\lambda(2z+2-y)=0$ 旋转扫描到垂直位置。

scene_spec.steps[2]

第三步：垂直条件 $1+\lambda=0$ 的求解。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

平面束 $(2x-2-y)+\lambda(2z+2-y)=0$ 旋转扫描到垂直位置

efficiency_tags[1]

垂直条件 $1+\lambda=0$ 的求解

## eval-geom-003-s3

problem

求过直线 $l:\dfrac{x-1}{1}=\dfrac{y}{2}=\dfrac{z+1}{1}$ 且垂直于平面 $\pi:x+y+z=0$ 的平面方程。

solution

所求平面过 $P_0(1,0,-1)$ 且含方向 $\vec s=(1,2,1)$；又因垂直于 $\pi$，平面法向量必与 $\vec{n_1}$ 垂直，故 $\vec{n_1}$ 必平行于所求平面，可作为平面内第二个方向向量。平面法向量 $\vec n=\vec s\times\vec{n_1}=(1,0,-1)$（同解法一），得 $x-z=2$。

answer

$x-z=2$

scene_spec.objects[0]

$\vec{n_1}$ 躺在所求平面内的几何标注

scene_spec.objects[1]

点 $P_0$ 与两方向向量张成平面的过程

scene_spec.steps[0]

第一步：以点+两方向向量为主线，建立解析几何·直线与平面场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：$\vec{n_1}$ 躺在所求平面内的几何标注。

scene_spec.steps[2]

第三步：点 $P_0$ 与两方向向量张成平面的过程。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

$\vec{n_1}$ 躺在所求平面内的几何标注

efficiency_tags[1]

点 $P_0$ 与两方向向量张成平面的过程

## eval-geom-004-s1

problem

求两平面 $\pi_1:x-y+z=1$ 与 $\pi_2:2x+y-z=0$ 的夹角。

solution

$\vec{n_1}=(1,-1,1)$，$\vec{n_2}=(2,1,-1)$。点积 $\vec{n_1}\cdot\vec{n_2}=1\cdot 2+(-1)\cdot 1+1\cdot(-1)=0$，故 $\cos\theta=\dfrac{|\vec{n_1}\cdot\vec{n_2}|}{|\vec{n_1}||\vec{n_2}|}=0$，两平面夹角为 $\dfrac{\pi}{2}$。

answer

$\dfrac{\pi}{2}$（两平面垂直）

scene_spec.objects[0]

法向量夹角联动显示

scene_spec.objects[1]

点积 $\vec{n_1}\cdot\vec{n_2}=0$ 的标注

scene_spec.steps[0]

第一步：以法向量夹角公式为主线，建立解析几何·直线与平面场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：法向量夹角联动显示。

scene_spec.steps[2]

第三步：点积 $\vec{n_1}\cdot\vec{n_2}=0$ 的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

法向量夹角联动显示

efficiency_tags[1]

点积 $\vec{n_1}\cdot\vec{n_2}=0$ 的标注

## eval-geom-004-s2

problem

求两平面 $\pi_1:x-y+z=1$ 与 $\pi_2:2x+y-z=0$ 的夹角。

solution

两平面交线方向 $\vec s=\vec{n_1}\times\vec{n_2}=((-1)(-1)-1\cdot 1,\ 1\cdot 2-1\cdot(-1),\ 1\cdot 1-(-1)\cdot 2)=(0,3,3)$，取 $\vec s=(0,1,1)$。在 $\pi_1$ 内取垂直于交线的方向 $\vec{d_1}=\vec{n_1}\times\vec s=((-1)\cdot 1-1\cdot 1,\ 1\cdot 0-1\cdot 1,\ 1\cdot 1-(-1)\cdot 0)=(-2,-1,1)$；在 $\pi_2$ 内取 $\vec{d_2}=\vec{n_2}\times\vec s=(1\cdot 1-(-1)\cdot 1,\ (-1)\cdot 0-2\cdot 1,\ 2\cdot 1-1\cdot 0)=(2,-2,2)$。两平面夹角即 $\vec{d_1}$ 与 $\vec{d_2}$ 的夹角：$\vec{d_1}\cdot\vec{d_2}=-4+2+2=0$，夹角 $\dfrac{\pi}{2}$。

answer

$\dfrac{\pi}{2}$（两平面垂直）

scene_spec.objects[0]

交线方向 $\vec s=(0,1,1)$ 的提取

scene_spec.objects[1]

截面直线 $\vec{d_1}$、$\vec{d_2}$ 标出平面角 $90^\circ$

scene_spec.steps[0]

第一步：以交线与截面直线为主线，建立解析几何·直线与平面场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：交线方向 $\vec s=(0,1,1)$ 的提取。

scene_spec.steps[2]

第三步：截面直线 $\vec{d_1}$、$\vec{d_2}$ 标出平面角 $90^\circ$。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

交线方向 $\vec s=(0,1,1)$ 的提取

efficiency_tags[1]

截面直线 $\vec{d_1}$、$\vec{d_2}$ 标出平面角 $90^\circ$

## eval-geom-004-s3

problem

求两平面 $\pi_1:x-y+z=1$ 与 $\pi_2:2x+y-z=0$ 的夹角。

solution

检验 $\pi_2$ 的法向量是否平行于 $\pi_1$ 的方向空间：$\vec{n_2}=(2,1,-1)$ 代入 $\pi_1$ 的齐次方程 $x-y+z$ 得 $2-1-1=0$，说明 $\vec{n_2}$ 是 $\pi_1$ 内的一个方向向量，即一个平面的法向量躺在另一个平面内，这正是两平面垂直的充要条件。

answer

$\dfrac{\pi}{2}$（两平面垂直）

scene_spec.objects[0]

法向量 $\vec{n_2}$ 代入 $\pi_1$ 齐次方程得 0 的验证

scene_spec.objects[1]

两垂直平面的三维展示

scene_spec.steps[0]

第一步：以法向量共面观察为主线，建立解析几何·直线与平面场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：法向量 $\vec{n_2}$ 代入 $\pi_1$ 齐次方程得 0 的验证。

scene_spec.steps[2]

第三步：两垂直平面的三维展示。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

法向量 $\vec{n_2}$ 代入 $\pi_1$ 齐次方程得 0 的验证

efficiency_tags[1]

两垂直平面的三维展示

## eval-geom-005-s1

problem

求点 $P(2,1,0)$ 到直线 $l:\dfrac{x-1}{1}=\dfrac{y}{2}=\dfrac{z+1}{1}$ 的距离。

solution

取直线上点 $P_0(1,0,-1)$、方向向量 $\vec s=(1,2,1)$，$\overrightarrow{P_0P}=(1,1,1)$。叉积 $\overrightarrow{P_0P}\times\vec s=(1\cdot 1-1\cdot 2,\ 1\cdot 1-1\cdot 1,\ 1\cdot 2-1\cdot 1)=(-1,0,1)$，模 $\sqrt{2}$。距离 $d=\dfrac{|\overrightarrow{P_0P}\times\vec s|}{|\vec s|}=\dfrac{\sqrt{2}}{\sqrt{6}}=\dfrac{1}{\sqrt{3}}$。

answer

$\dfrac{1}{\sqrt{3}}$

scene_spec.objects[0]

叉积 $\overrightarrow{P_0P}\times\vec s=(-1,0,1)$ 的平行四边形面积分解

scene_spec.objects[1]

面积÷底=高的标注

scene_spec.steps[0]

第一步：以叉积公式为主线，建立解析几何·直线与平面场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：叉积 $\overrightarrow{P_0P}\times\vec s=(-1,0,1)$ 的平行四边形面积分解。

scene_spec.steps[2]

第三步：面积÷底=高的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

叉积 $\overrightarrow{P_0P}\times\vec s=(-1,0,1)$ 的平行四边形面积分解

efficiency_tags[1]

面积÷底=高的标注

## eval-geom-005-s2

problem

求点 $P(2,1,0)$ 到直线 $l:\dfrac{x-1}{1}=\dfrac{y}{2}=\dfrac{z+1}{1}$ 的距离。

solution

直线上点 $Q(t)=(1+t,2t,-1+t)$。$|PQ|^2=(t-1)^2+(2t-1)^2+(t-1)^2=2(t-1)^2+(2t-1)^2=6t^2-8t+3$。配方：$6\left(t-\dfrac{2}{3}\right)^2+\dfrac{1}{3}$，最小值 $\dfrac{1}{3}$ 在 $t=\dfrac{2}{3}$ 处取得，故 $d=\sqrt{\dfrac{1}{3}}=\dfrac{1}{\sqrt{3}}$。

answer

$\dfrac{1}{\sqrt{3}}$

scene_spec.objects[0]

$|PQ(t)|^2=6t^2-8t+3$ 的二次函数曲线与最低点

scene_spec.objects[1]

参数 $t=\dfrac{2}{3}$ 的定位

scene_spec.steps[0]

第一步：以参数化求最小值为主线，建立解析几何·直线与平面场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：$|PQ(t)|^2=6t^2-8t+3$ 的二次函数曲线与最低点。

scene_spec.steps[2]

第三步：参数 $t=\dfrac{2}{3}$ 的定位。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

$|PQ(t)|^2=6t^2-8t+3$ 的二次函数曲线与最低点

efficiency_tags[1]

参数 $t=\dfrac{2}{3}$ 的定位

## eval-geom-005-s3

problem

求点 $P(2,1,0)$ 到直线 $l:\dfrac{x-1}{1}=\dfrac{y}{2}=\dfrac{z+1}{1}$ 的距离。

solution

垂足参数 $t^*=\dfrac{\overrightarrow{P_0P}\cdot\vec s}{|\vec s|^2}=\dfrac{1\cdot 1+1\cdot 2+1\cdot 1}{6}=\dfrac{2}{3}$，垂足 $Q=\left(\dfrac{5}{3},\dfrac{4}{3},-\dfrac{1}{3}\right)$。$d=|PQ|=\sqrt{\left(\dfrac{1}{3}\right)^2+\left(-\dfrac{1}{3}\right)^2+\left(\dfrac{1}{3}\right)^2}=\dfrac{1}{\sqrt{3}}$。检验垂足在直线上：$\dfrac{5/3-1}{1}=\dfrac{4/3}{2}=\dfrac{-1/3+1}{1}=\dfrac{2}{3}$。

answer

$\dfrac{1}{\sqrt{3}}$

scene_spec.objects[0]

垂足 $Q=\left(\dfrac{5}{3},\dfrac{4}{3},-\dfrac{1}{3}\right)$ 的投影标注

scene_spec.objects[1]

垂线段长度 $\dfrac{1}{\sqrt3}$

scene_spec.steps[0]

第一步：以正交投影为主线，建立解析几何·直线与平面场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：垂足 $Q=\left(\dfrac{5}{3},\dfrac{4}{3},-\dfrac{1}{3}\right)$ 的投影标注。

scene_spec.steps[2]

第三步：垂线段长度 $\dfrac{1}{\sqrt3}$。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

垂足 $Q=\left(\dfrac{5}{3},\dfrac{4}{3},-\dfrac{1}{3}\right)$ 的投影标注

efficiency_tags[1]

垂线段长度 $\dfrac{1}{\sqrt3}$

## eval-geom-006-s1

problem

讨论三个平面 $\pi_1:x+y+z=1$，$\pi_2:x-y+z=1$，$\pi_3:2x+2z=2$ 的位置关系，并求其公共部分。

solution

系数矩阵与增广矩阵行变换：$\begin{pmatrix}1&1&1&1\\1&-1&1&1\\2&0&2&2\end{pmatrix}\to\begin{pmatrix}1&1&1&1\\0&-2&0&0\\0&-2&0&0\end{pmatrix}\to\begin{pmatrix}1&1&1&1\\0&1&0&0\\0&0&0&0\end{pmatrix}$。秩 $\mathrm r(A)=\mathrm r(\bar A)=2<3$，无穷多解，解集（仿射直线）一维：$y=0$，$x+z=1$，即一条直线。

answer

三平面共线，交线为 $y=0,\ x+z=1$

scene_spec.objects[0]

增广矩阵行变换的逐步动画

scene_spec.objects[1]

秩 $2<3$ 与仿射解集维数一的对应标注

scene_spec.steps[0]

呈现题干及适用条件：讨论三个平面 $\pi_1:x+y+z=1$，$\pi_2:x-y+z=1$，$\pi_3:2x+2z=2$ 的位置关系，并求其公共部分。

scene_spec.steps[1]

依次呈现：增广矩阵行变换的逐步动画

scene_spec.steps[2]

依次呈现：秩 $2<3$ 与仿射解集维数一的对应标注

scene_spec.steps[3]

核对完整证明：系数矩阵与增广矩阵行变换：$\begin{pmatrix}1&1&1&1\\1&-1&1&1\\2&0&2&2\end{pmatrix}\to\begin{pmatrix}1&1&1&1\\0&-2&0&0\\0&-2&0&0\end{pmatrix}\to\begin{pmatrix}1&1&1&1\\0&1&0&0\\0&0&0&0\end{pmatrix}$。秩 $\mathrm r(A)=\mathrm r(\bar A)=2<3$，无穷多解，解集（仿射直线）一维：$y=0$，$x+z=1$，即一条直线。

scene_spec.steps[4]

高亮结果：三平面共线，交线为 $y=0,\ x+z=1$

efficiency_tags[0]

增广矩阵行变换的逐步动画

efficiency_tags[1]

秩 $2<3$ 与仿射解集维数一的对应标注

## eval-geom-006-s2

problem

讨论三个平面 $\pi_1:x+y+z=1$，$\pi_2:x-y+z=1$，$\pi_3:2x+2z=2$ 的位置关系，并求其公共部分。

solution

观察 $\pi_3$ 的方程恰是 $\pi_1$ 与 $\pi_2$ 方程之和，故 $\pi_3$ 必过 $\pi_1\cap\pi_2$ 的每一点。求 $\pi_1\cap\pi_2$：两式相减得 $2y=0$，$y=0$；代回得 $x+z=1$。故公共部分为直线 $\begin{cases}y=0\\x+z=1\end{cases}$，参数化 $(x,y,z)=(t,0,1-t)$。检验满足 $\pi_3$：$2t+2(1-t)=2$。

answer

三平面共线，交线为 $y=0,\ x+z=1$

scene_spec.objects[0]

方程相加的几何含义

scene_spec.objects[1]

三平面共线交叠的三维视图

scene_spec.steps[0]

第一步：以几何分析：方程相加为主线，建立解析几何·直线与平面场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：方程相加的几何含义。

scene_spec.steps[2]

第三步：三平面共线交叠的三维视图。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

方程相加的几何含义

efficiency_tags[1]

三平面共线交叠的三维视图

## eval-geom-006-s3

problem

讨论三个平面 $\pi_1:x+y+z=1$，$\pi_2:x-y+z=1$，$\pi_3:2x+2z=2$ 的位置关系，并求其公共部分。

solution

三个法向量 $\vec{n_1}=(1,1,1)$、$\vec{n_2}=(1,-1,1)$、$\vec{n_3}=(2,0,2)$ 满足 $\vec{n_3}=\vec{n_1}+\vec{n_2}$，故共面。交线方向 $\vec s=\vec{n_1}\times\vec{n_2}=(1\cdot 1-1\cdot(-1),\ 1\cdot 1-1\cdot 1,\ 1\cdot(-1)-1\cdot 1)=(2,0,-2)$，取 $\vec s=(1,0,-1)$。找交线上一点：令 $y=0$，解 $x+z=1$，取 $(1,0,0)$。交线为 $(x,y,z)=(1+t,0,-t)$。

answer

三平面共线，交线为 $y=0,\ x+z=1$

scene_spec.objects[0]

法向量关系 $\vec{n_3}=\vec{n_1}+\vec{n_2}$ 的标注

scene_spec.objects[1]

交线方向 $\vec s=(1,0,-1)$ 与交点 $(1,0,0)$

scene_spec.steps[0]

第一步：以向量法为主线，建立解析几何·直线与平面场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：法向量关系 $\vec{n_3}=\vec{n_1}+\vec{n_2}$ 的标注。

scene_spec.steps[2]

第三步：交线方向 $\vec s=(1,0,-1)$ 与交点 $(1,0,0)$。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

法向量关系 $\vec{n_3}=\vec{n_1}+\vec{n_2}$ 的标注

efficiency_tags[1]

交线方向 $\vec s=(1,0,-1)$ 与交点 $(1,0,0)$

## eval-geom-007-s1

problem

指出方程 $4x^2-y^2+z^2=1$ 表示的二次曲面类型，并用截面法说明其形状。

solution

方程化为 $\dfrac{x^2}{1/4}+\dfrac{z^2}{1}-\dfrac{y^2}{1}=1$，形如 $\dfrac{x^2}{a^2}+\dfrac{z^2}{b^2}-\dfrac{y^2}{c^2}=1$（一个负号项），是单叶双曲面，对称轴为 $y$ 轴。截面$y=k$为$4x^2+z^2=1+k^2$，始终为椭圆。截面$z=k$为$4x^2-y^2=1-k^2$：$|k|<1$沿$x$开口，$|k|>1$沿$y$开口，$|k|=1$退化为$y=\pm2x$。截面$x=k$为$z^2-y^2=1-4k^2$：$|k|<1/2$沿$z$开口，$|k|>1/2$沿$y$开口，$|k|=1/2$退化为$z=\pm y$。由一个负平方和两个正平方组成的标准式且$y=k$截面始终非空，知为绕$y$轴的单叶双曲面。

answer

单叶双曲面（以 $y$ 轴为对称轴）

scene_spec.objects[0]

$y=k$的椭圆截面$4x^2+z^2=1+k^2$

scene_spec.objects[1]

$z=k$在$k=\pm1$退化为两相交直线

scene_spec.objects[2]

$x=k$在$k=\pm1/2$退化为两相交直线

scene_spec.objects[3]

绕$y$轴的单叶双曲面

scene_spec.steps[0]

呈现题干及适用条件：指出方程 $4x^2-y^2+z^2=1$ 表示的二次曲面类型，并用截面法说明其形状。

scene_spec.steps[1]

依次呈现：$y=k$的椭圆截面$4x^2+z^2=1+k^2$

scene_spec.steps[2]

依次呈现：$z=k$在$k=\pm1$退化为两相交直线

scene_spec.steps[3]

依次呈现：$x=k$在$k=\pm1/2$退化为两相交直线

scene_spec.steps[4]

依次呈现：绕$y$轴的单叶双曲面

scene_spec.steps[5]

核对完整证明：方程化为 $\dfrac{x^2}{1/4}+\dfrac{z^2}{1}-\dfrac{y^2}{1}=1$，形如 $\dfrac{x^2}{a^2}+\dfrac{z^2}{b^2}-\dfrac{y^2}{c^2}=1$（一个负号项），是单叶双曲面，对称轴为 $y$ 轴。截面$y=k$为$4x^2+z^2=1+k^2$，始终为椭圆。截面$z=k$为$4x^2-y^2=1-k^2$：$|k|<1$沿$x$开口，$|k|>1$沿$y$开口，$|k|=1$退化为$y=\pm2x$。截面$x=k$为$z^2-y^2=1-4k^2$：$|k|<1/2$沿$z$开口，$|k|>1/2$沿$y$开口，$|k|=1/2$退化为$z=\pm y$。由一个负平方和两个正平方组成的标准式且$y=k$截面始终非空，知为绕$y$轴的单叶双曲面。

scene_spec.steps[6]

高亮结果：单叶双曲面（以 $y$ 轴为对称轴）

efficiency_tags[0]

$y=k$的椭圆截面$4x^2+z^2=1+k^2$

efficiency_tags[1]

$z=k$在$k=\pm1$退化为两相交直线

efficiency_tags[2]

$x=k$在$k=\pm1/2$退化为两相交直线

efficiency_tags[3]

绕$y$轴的单叶双曲面

## eval-geom-007-s2

problem

指出方程 $4x^2-y^2+z^2=1$ 表示的二次曲面类型，并用截面法说明其形状。

solution

截面$y=k$为$4x^2+z^2=1+k^2$，始终为椭圆。截面$z=k$为$4x^2-y^2=1-k^2$：$|k|<1$沿$x$开口，$|k|>1$沿$y$开口，$|k|=1$退化为$y=\pm2x$。截面$x=k$为$z^2-y^2=1-4k^2$：$|k|<1/2$沿$z$开口，$|k|>1/2$沿$y$开口，$|k|=1/2$退化为$z=\pm y$。由一个负平方和两个正平方组成的标准式且$y=k$截面始终非空，知为绕$y$轴的单叶双曲面。

answer

单叶双曲面（以 $y$ 轴为对称轴）

scene_spec.objects[0]

$y=k$的椭圆截面$4x^2+z^2=1+k^2$

scene_spec.objects[1]

$z=k$在$k=\pm1$退化为两相交直线

scene_spec.objects[2]

$x=k$在$k=\pm1/2$退化为两相交直线

scene_spec.objects[3]

绕$y$轴的单叶双曲面

scene_spec.steps[0]

呈现题干及适用条件：指出方程 $4x^2-y^2+z^2=1$ 表示的二次曲面类型，并用截面法说明其形状。

scene_spec.steps[1]

依次呈现：$y=k$的椭圆截面$4x^2+z^2=1+k^2$

scene_spec.steps[2]

依次呈现：$z=k$在$k=\pm1$退化为两相交直线

scene_spec.steps[3]

依次呈现：$x=k$在$k=\pm1/2$退化为两相交直线

scene_spec.steps[4]

依次呈现：绕$y$轴的单叶双曲面

scene_spec.steps[5]

核对完整证明：截面$y=k$为$4x^2+z^2=1+k^2$，始终为椭圆。截面$z=k$为$4x^2-y^2=1-k^2$：$|k|<1$沿$x$开口，$|k|>1$沿$y$开口，$|k|=1$退化为$y=\pm2x$。截面$x=k$为$z^2-y^2=1-4k^2$：$|k|<1/2$沿$z$开口，$|k|>1/2$沿$y$开口，$|k|=1/2$退化为$z=\pm y$。由一个负平方和两个正平方组成的标准式且$y=k$截面始终非空，知为绕$y$轴的单叶双曲面。

scene_spec.steps[6]

高亮结果：单叶双曲面（以 $y$ 轴为对称轴）

efficiency_tags[0]

$y=k$的椭圆截面$4x^2+z^2=1+k^2$

efficiency_tags[1]

$z=k$在$k=\pm1$退化为两相交直线

efficiency_tags[2]

$x=k$在$k=\pm1/2$退化为两相交直线

efficiency_tags[3]

绕$y$轴的单叶双曲面

## eval-geom-007-s3

problem

指出方程 $4x^2-y^2+z^2=1$ 表示的二次曲面类型，并用截面法说明其形状。

solution

构造两族直线（参数 $s$）：$\begin{cases}x=\dfrac{\cos\theta+s\sin\theta}{2}\\y=s\\z=\sin\theta-s\cos\theta\end{cases}$ 与 $\begin{cases}x=\dfrac{\cos\theta-s\sin\theta}{2}\\y=s\\z=\sin\theta+s\cos\theta\end{cases}$。代入验证：$4x^2+z^2-y^2=(\cos\theta\pm s\sin\theta)^2+(\sin\theta\mp s\cos\theta)^2-s^2=\cos^2\theta+\sin^2\theta\pm 2s\sin\theta\cos\theta\mp 2s\sin\theta\cos\theta+s^2(\sin^2\theta+\cos^2\theta)-s^2=1$，整条直线都落在曲面上。直母线族的存在是单叶双曲面的特征性质（双叶双曲面无此性质）。截面$y=k$为$4x^2+z^2=1+k^2$，始终为椭圆。截面$z=k$为$4x^2-y^2=1-k^2$：$|k|<1$沿$x$开口，$|k|>1$沿$y$开口，$|k|=1$退化为$y=\pm2x$。截面$x=k$为$z^2-y^2=1-4k^2$：$|k|<1/2$沿$z$开口，$|k|>1/2$沿$y$开口，$|k|=1/2$退化为$z=\pm y$。由一个负平方和两个正平方组成的标准式且$y=k$截面始终非空，知为绕$y$轴的单叶双曲面。

answer

单叶双曲面（以 $y$ 轴为对称轴）

scene_spec.objects[0]

$y=k$的椭圆截面$4x^2+z^2=1+k^2$

scene_spec.objects[1]

$z=k$在$k=\pm1$退化为两相交直线

scene_spec.objects[2]

$x=k$在$k=\pm1/2$退化为两相交直线

scene_spec.objects[3]

绕$y$轴的单叶双曲面

scene_spec.steps[0]

呈现题干及适用条件：指出方程 $4x^2-y^2+z^2=1$ 表示的二次曲面类型，并用截面法说明其形状。

scene_spec.steps[1]

依次呈现：$y=k$的椭圆截面$4x^2+z^2=1+k^2$

scene_spec.steps[2]

依次呈现：$z=k$在$k=\pm1$退化为两相交直线

scene_spec.steps[3]

依次呈现：$x=k$在$k=\pm1/2$退化为两相交直线

scene_spec.steps[4]

依次呈现：绕$y$轴的单叶双曲面

scene_spec.steps[5]

核对完整证明：构造两族直线（参数 $s$）：$\begin{cases}x=\dfrac{\cos\theta+s\sin\theta}{2}\\y=s\\z=\sin\theta-s\cos\theta\end{cases}$ 与 $\begin{cases}x=\dfrac{\cos\theta-s\sin\theta}{2}\\y=s\\z=\sin\theta+s\cos\theta\end{cases}$。代入验证：$4x^2+z^2-y^2=(\cos\theta\pm s\sin\theta)^2+(\sin\theta\mp s\cos\theta)^2-s^2=\cos^2\theta+\sin^2\theta\pm 2s\sin\theta\cos\theta\mp 2s\sin\theta\cos\theta+s^2(\sin^2\theta+\cos^2\theta)-s^2=1$，整条直线都落在曲面上。直母线族的存在是单叶双曲面的特征性质（双叶双曲面无此性质）。截面$y=k$为$4x^2+z^2=1+k^2$，始终为椭圆。截面$z=k$为$4x^2-y^2=1-k^2$：$|k|<1$沿$x$开口，$|k|>1$沿$y$开口，$|k|=1$退化为$y=\pm2x$。截面$x=k$为$z^2-y^2=1-4k^2$：$|k|<1/2$沿$z$开口，$|k|>1/2$沿$y$开口，$|k|=1/2$退化为$z=\pm y$。由一个负平方和两个正平方组成的标准式且$y=k$截面始终非空，知为绕$y$轴的单叶双曲面。

scene_spec.steps[6]

高亮结果：单叶双曲面（以 $y$ 轴为对称轴）

efficiency_tags[0]

$y=k$的椭圆截面$4x^2+z^2=1+k^2$

efficiency_tags[1]

$z=k$在$k=\pm1$退化为两相交直线

efficiency_tags[2]

$x=k$在$k=\pm1/2$退化为两相交直线

efficiency_tags[3]

绕$y$轴的单叶双曲面

## eval-geom-008-s1

problem

判断二次曲面 $2x^2+y^2-z^2+4xy=1$ 的类型。

solution

二次项矩阵 $A=\begin{pmatrix}2&2&0\\2&1&0\\0&0&-1\end{pmatrix}$。$2\times 2$ 块 $\begin{pmatrix}2&2\\2&1\end{pmatrix}$ 的特征方程为 $(2-\lambda)(1-\lambda)-4=0$，即 $\lambda^2-3\lambda-2=0$，特征值 $\lambda_1=\dfrac{3+\sqrt{17}}{2}>0$、$\lambda_2=\dfrac{3-\sqrt{17}}{2}<0$；第三个特征值为 $-1<0$。正惯性指数 $1$、负惯性指数 $2$，对应双叶双曲面。

answer

双叶双曲面

scene_spec.objects[0]

特征值 $\dfrac{3\pm\sqrt{17}}{2}$ 与 $-1$ 的谱标注

scene_spec.objects[1]

正负惯性指数 $(1,2)$ 的标注

scene_spec.steps[0]

第一步：以特征值法为主线，建立解析几何·二次曲面分类场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：特征值 $\dfrac{3\pm\sqrt{17}}{2}$ 与 $-1$ 的谱标注。

scene_spec.steps[2]

第三步：正负惯性指数 $(1,2)$ 的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

特征值 $\dfrac{3\pm\sqrt{17}}{2}$ 与 $-1$ 的谱标注

efficiency_tags[1]

正负惯性指数 $(1,2)$ 的标注

## eval-geom-008-s2

problem

判断二次曲面 $2x^2+y^2-z^2+4xy=1$ 的类型。

solution

$2x^2+4xy+y^2=2(x+y)^2-y^2$，故曲面方程为 $2(x+y)^2-y^2-z^2=1$，正平方项 1 个、负平方项 2 个，为双叶双曲面。

answer

双叶双曲面

scene_spec.objects[0]

配方 $2(x+y)^2-y^2-z^2=1$ 的逐步动画

scene_spec.objects[1]

双叶双曲面的三维渲染

scene_spec.steps[0]

第一步：以配方法为主线，建立解析几何·二次曲面分类场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：配方 $2(x+y)^2-y^2-z^2=1$ 的逐步动画。

scene_spec.steps[2]

第三步：双叶双曲面的三维渲染。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

配方 $2(x+y)^2-y^2-z^2=1$ 的逐步动画

efficiency_tags[1]

双叶双曲面的三维渲染

## eval-geom-008-s3

problem

判断二次曲面 $2x^2+y^2-z^2+4xy=1$ 的类型。

solution

用 $z=0$ 截：$2x^2+4xy+y^2=1$，配方为 $2(x+y)^2-y^2=1$，是双曲线；用 $y=0$ 截：$2x^2-z^2=1$，是双曲线；用 $x+y=0$（即 $x=-y$）截：$-y^2-z^2=1$ 无实解——该平面与曲面不相交。三个截面说明曲面在 $z$ 方向与 $x+y$ 方向均为双曲型、且存在与曲面完全不相交的平面（双叶分离的特征）。严格分类令$u=x+y,\ v=y,\ w=z$，这是可逆线性替换。原式化为$2u^2-v^2-w^2=1$，故$u=\pm\sqrt{(1+v^2+w^2)/2}$。两个符号分支分别是定义于$\mathbb R^2$的连续图像，各自连通，且由$|u|\ge1/\sqrt2$隔开，故恰为双叶双曲面。

answer

双叶双曲面

scene_spec.objects[0]

三个典型截面的双曲线

scene_spec.objects[1]

$x+y=0$ 截面无实解的标注

scene_spec.objects[2]

与单叶双曲面（eval-geom-007）对照

scene_spec.steps[0]

呈现题干及适用条件：判断二次曲面 $2x^2+y^2-z^2+4xy=1$ 的类型。

scene_spec.steps[1]

依次呈现：三个典型截面的双曲线

scene_spec.steps[2]

依次呈现：$x+y=0$ 截面无实解的标注

scene_spec.steps[3]

依次呈现：与单叶双曲面（eval-geom-007）对照

scene_spec.steps[4]

核对完整证明：用 $z=0$ 截：$2x^2+4xy+y^2=1$，配方为 $2(x+y)^2-y^2=1$，是双曲线；用 $y=0$ 截：$2x^2-z^2=1$，是双曲线；用 $x+y=0$（即 $x=-y$）截：$-y^2-z^2=1$ 无实解——该平面与曲面不相交。三个截面说明曲面在 $z$ 方向与 $x+y$ 方向均为双曲型、且存在与曲面完全不相交的平面（双叶分离的特征）。严格分类令$u=x+y,\ v=y,\ w=z$，这是可逆线性替换。原式化为$2u^2-v^2-w^2=1$，故$u=\pm\sqrt{(1+v^2+w^2)/2}$。两个符号分支分别是定义于$\mathbb R^2$的连续图像，各自连通，且由$|u|\ge1/\sqrt2$隔开，故恰为双叶双曲面。

scene_spec.steps[5]

高亮结果：双叶双曲面

efficiency_tags[0]

三个典型截面的双曲线

efficiency_tags[1]

$x+y=0$ 截面无实解的标注

efficiency_tags[2]

与单叶双曲面（eval-geom-007）对照

## eval-geom-009-s1

problem

求椭球面 $\dfrac{x^2}{4}+\dfrac{y^2}{9}+z^2=1$ 与平面 $x=1$ 的交线方程，并说明其形状。

solution

将 $x=1$ 代入椭球面方程：$\dfrac{1}{4}+\dfrac{y^2}{9}+z^2=1$，即 $\dfrac{y^2}{9}+z^2=\dfrac{3}{4}$。化为标准形 $\dfrac{y^2}{9\cdot\frac{3}{4}}+\dfrac{z^2}{\frac{3}{4}}=1$，即 $\dfrac{y^2}{27/4}+\dfrac{z^2}{3/4}=1$。这是平面 $x=1$ 内的椭圆，半轴分别为 $\sqrt{\dfrac{27}{4}}=\dfrac{3\sqrt{3}}{2}$ 与 $\sqrt{\dfrac{3}{4}}=\dfrac{\sqrt{3}}{2}$，中心 $(1,0,0)$。

answer

椭圆：$\dfrac{y^2}{27/4}+\dfrac{z^2}{3/4}=1$（$x=1$），半轴 $\dfrac{3\sqrt{3}}{2}$ 与 $\dfrac{\sqrt{3}}{2}$

scene_spec.objects[0]

椭球面与截平面 $x=1$ 相交

scene_spec.objects[1]

代入后方程 $\dfrac{y^2}{27/4}+\dfrac{z^2}{3/4}=1$ 的化简

scene_spec.steps[0]

第一步：以代入法为主线，建立解析几何·曲面与曲线场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：椭球面与截平面 $x=1$ 相交。

scene_spec.steps[2]

第三步：代入后方程 $\dfrac{y^2}{27/4}+\dfrac{z^2}{3/4}=1$ 的化简。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

椭球面与截平面 $x=1$ 相交

efficiency_tags[1]

代入后方程 $\dfrac{y^2}{27/4}+\dfrac{z^2}{3/4}=1$ 的化简

## eval-geom-009-s2

problem

求椭球面 $\dfrac{x^2}{4}+\dfrac{y^2}{9}+z^2=1$ 与平面 $x=1$ 的交线方程，并说明其形状。

solution

由标准形直接参数化：$x=1$，$y=\dfrac{3\sqrt{3}}{2}\cos t$，$z=\dfrac{\sqrt{3}}{2}\sin t$，$t\in[0,2\pi]$。代回验证：$\dfrac{1}{4}+\dfrac{27\cos^2 t}{4\cdot 9}+\dfrac{3\sin^2 t}{4}=\dfrac{1}{4}+\dfrac{3}{4}(\cos^2 t+\sin^2 t)=1$。

answer

椭圆：$\dfrac{y^2}{27/4}+\dfrac{z^2}{3/4}=1$（$x=1$），半轴 $\dfrac{3\sqrt{3}}{2}$ 与 $\dfrac{\sqrt{3}}{2}$

scene_spec.objects[0]

参数点 $\left(1,\dfrac{3\sqrt3}{2}\cos t,\dfrac{\sqrt3}{2}\sin t\right)$ 沿椭圆运动

scene_spec.objects[1]

代回验证恒等式

scene_spec.steps[0]

第一步：以参数化为主线，建立解析几何·曲面与曲线场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：参数点 $\left(1,\dfrac{3\sqrt3}{2}\cos t,\dfrac{\sqrt3}{2}\sin t\right)$ 沿椭圆运动。

scene_spec.steps[2]

第三步：代回验证恒等式。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

参数点 $\left(1,\dfrac{3\sqrt3}{2}\cos t,\dfrac{\sqrt3}{2}\sin t\right)$ 沿椭圆运动

efficiency_tags[1]

代回验证恒等式

## eval-geom-009-s3

problem

求椭球面 $\dfrac{x^2}{4}+\dfrac{y^2}{9}+z^2=1$ 与平面 $x=1$ 的交线方程，并说明其形状。

solution

一般截面 $x=k$：$|k|<2$ 时为椭圆 $\dfrac{y^2}{9\left(1-\frac{k^2}{4}\right)}+\dfrac{z^2}{1-\frac{k^2}{4}}=1$，半轴 $3\sqrt{1-\dfrac{k^2}{4}}$ 与 $\sqrt{1-\dfrac{k^2}{4}}$（比值恒为 $3$，故所有截面椭圆相似）；$k=\pm 2$ 时 $1-\dfrac{k^2}{4}=0$，方程仅剩 $y=z=0$，截面退化为单点 $(\pm 2,0,0)$；$|k|>2$ 时无交点。取 $k=1$：半轴 $3\cdot\dfrac{\sqrt{3}}{2}=\dfrac{3\sqrt{3}}{2}$ 与 $\dfrac{\sqrt{3}}{2}$，与解法一一致。

answer

椭圆：$\dfrac{y^2}{27/4}+\dfrac{z^2}{3/4}=1$（$x=1$），半轴 $\dfrac{3\sqrt{3}}{2}$ 与 $\dfrac{\sqrt{3}}{2}$

scene_spec.objects[0]

截面椭圆族扫描动画

scene_spec.objects[1]

半轴长度随 $k$ 变化的曲线与 $k=\pm2$ 退化点

scene_spec.steps[0]

第一步：以平行截面族为主线，建立解析几何·曲面与曲线场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：截面椭圆族扫描动画。

scene_spec.steps[2]

第三步：半轴长度随 $k$ 变化的曲线与 $k=\pm2$ 退化点。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

截面椭圆族扫描动画

efficiency_tags[1]

半轴长度随 $k$ 变化的曲线与 $k=\pm2$ 退化点

## eval-geom-010-s1

problem

说明曲面 $z=xy$ 的类型，并验证它是直纹面。

solution

作正交变换 $u=\dfrac{x+y}{\sqrt{2}}$、$v=\dfrac{x-y}{\sqrt{2}}$，则 $x=\dfrac{u+v}{\sqrt{2}}$、$y=\dfrac{u-v}{\sqrt{2}}$，$xy=\dfrac{u^2-v^2}{2}$。曲面方程化为 $z=\dfrac{u^2}{2}-\dfrac{v^2}{2}$，即 $2z=u^2-v^2$，是双曲抛物面（马鞍面）。两族直母线显式写成$(x,y,z)=(t,c,ct)$和$(c,t,ct)$（$c,t\in\mathbb R$）。每一点$(x_0,y_0,x_0y_0)$都同时落在$c=y_0$的第一族及$c=x_0$的第二族上。

answer

双曲抛物面（马鞍面），直纹面

scene_spec.objects[0]

马鞍面三维渲染与 $45^\circ$ 旋转变换

scene_spec.objects[1]

$xy=\dfrac{u^2-v^2}{2}$ 的代入

scene_spec.steps[0]

呈现题干及适用条件：说明曲面 $z=xy$ 的类型，并验证它是直纹面。

scene_spec.steps[1]

依次呈现：马鞍面三维渲染与 $45^\circ$ 旋转变换

scene_spec.steps[2]

依次呈现：$xy=\dfrac{u^2-v^2}{2}$ 的代入

scene_spec.steps[3]

核对完整证明：作正交变换 $u=\dfrac{x+y}{\sqrt{2}}$、$v=\dfrac{x-y}{\sqrt{2}}$，则 $x=\dfrac{u+v}{\sqrt{2}}$、$y=\dfrac{u-v}{\sqrt{2}}$，$xy=\dfrac{u^2-v^2}{2}$。曲面方程化为 $z=\dfrac{u^2}{2}-\dfrac{v^2}{2}$，即 $2z=u^2-v^2$，是双曲抛物面（马鞍面）。两族直母线显式写成$(x,y,z)=(t,c,ct)$和$(c,t,ct)$（$c,t\in\mathbb R$）。每一点$(x_0,y_0,x_0y_0)$都同时落在$c=y_0$的第一族及$c=x_0$的第二族上。

scene_spec.steps[4]

高亮结果：双曲抛物面（马鞍面），直纹面

efficiency_tags[0]

马鞍面三维渲染与 $45^\circ$ 旋转变换

efficiency_tags[1]

$xy=\dfrac{u^2-v^2}{2}$ 的代入

## eval-geom-010-s2

problem

说明曲面 $z=xy$ 的类型，并验证它是直纹面。

solution

固定 $y=c$：截面 $z=cx$ 是直线；固定 $x=c$：截面 $z=cy$ 也是直线。即曲面上存在两族平行于坐标平面的直线族 $\{z=cx,\ y=c\}$ 与 $\{z=cy,\ x=c\}$，故 $z=xy$ 是直纹面，且每一点处恰有两条直母线通过（交叉直线构成马鞍网格）。

answer

双曲抛物面（马鞍面），直纹面

scene_spec.objects[0]

两族直母线 $z=cx$（$y=c$）与 $z=cy$（$x=c$）的网格动画

scene_spec.steps[0]

第一步：以直母线族为主线，建立解析几何·曲面与曲线场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：两族直母线 $z=cx$（$y=c$）与 $z=cy$（$x=c$）的网格动画。

scene_spec.steps[2]

第三步：高亮最终结果与答案。

efficiency_tags[0]

两族直母线 $z=cx$（$y=c$）与 $z=cy$（$x=c$）的网格动画

## eval-geom-010-s3

problem

说明曲面 $z=xy$ 的类型，并验证它是直纹面。

solution

用 $y=k$ 截：$z=kx$，对任意 $k$ 都是直线（上述两个坐标方向的竖直截面均为直线，直纹性的又一体现）；用 $z=k$ 截：$xy=k$，等轴双曲线（$k\ne 0$）或两坐标轴（$k=0$）；若要抛物线截面，取斜截面 $x=y$（得 $z=x^2$）与 $x=-y$（得 $z=-x^2$）。直线截面与双曲线截面正是双曲抛物面的截面特征。

answer

双曲抛物面（马鞍面），直纹面

scene_spec.objects[0]

坐标方向竖直截面（直线族）与水平截面（非零高度为等轴双曲线，零高度为两相交直线）扫描

scene_spec.objects[1]

斜截面 $x=\pm y$ 的抛物线

scene_spec.steps[0]

呈现题干及适用条件：说明曲面 $z=xy$ 的类型，并验证它是直纹面。

scene_spec.steps[1]

依次呈现：坐标方向竖直截面（直线族）与水平截面（非零高度为等轴双曲线，零高度为两相交直线）扫描

scene_spec.steps[2]

依次呈现：斜截面 $x=\pm y$ 的抛物线

scene_spec.steps[3]

核对完整证明：用 $y=k$ 截：$z=kx$，对任意 $k$ 都是直线（上述两个坐标方向的竖直截面均为直线，直纹性的又一体现）；用 $z=k$ 截：$xy=k$，等轴双曲线（$k\ne 0$）或两坐标轴（$k=0$）；若要抛物线截面，取斜截面 $x=y$（得 $z=x^2$）与 $x=-y$（得 $z=-x^2$）。直线截面与双曲线截面正是双曲抛物面的截面特征。

scene_spec.steps[4]

高亮结果：双曲抛物面（马鞍面），直纹面

efficiency_tags[0]

坐标方向竖直截面（直线族）与水平截面（非零高度为等轴双曲线，零高度为两相交直线）扫描

efficiency_tags[1]

斜截面 $x=\pm y$ 的抛物线

## eval-geom-011-s1

problem

求直线 $l:x=1+t,\ y=t,\ z=t$ 与球面 $x^2+y^2+z^2=4$ 的交点个数，并求出交点坐标。

solution

代入：$(1+t)^2+t^2+t^2=4$，即 $3t^2+2t-3=0$。判别式 $\Delta=4+36=40>0$，故有两个交点。解出 $t=\dfrac{-2\pm\sqrt{40}}{6}=\dfrac{-1\pm\sqrt{10}}{3}$，对应两点 $\left(1+t,t,t\right)$：$t_1=\dfrac{-1+\sqrt{10}}{3}$ 时 $\left(\dfrac{2+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3}\right)$，$t_2=\dfrac{-1-\sqrt{10}}{3}$ 时 $\left(\dfrac{2-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3}\right)$。

answer

两个交点：$\left(\dfrac{2+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3}\right)$ 与 $\left(\dfrac{2-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3}\right)$

scene_spec.objects[0]

代入得 $3t^2+2t-3=0$ 的判别式动画

scene_spec.objects[1]

两交点高亮标注

scene_spec.steps[0]

第一步：以判别式法为主线，建立解析几何·曲面与曲线场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：代入得 $3t^2+2t-3=0$ 的判别式动画。

scene_spec.steps[2]

第三步：两交点高亮标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

代入得 $3t^2+2t-3=0$ 的判别式动画

efficiency_tags[1]

两交点高亮标注

## eval-geom-011-s2

problem

求直线 $l:x=1+t,\ y=t,\ z=t$ 与球面 $x^2+y^2+z^2=4$ 的交点个数，并求出交点坐标。

solution

球心 $O(0,0,0)$ 到直线距离：直线上取点 $P_0(1,0,0)$、方向 $\vec s=(1,1,1)$，$\overrightarrow{P_0O}=(-1,0,0)$，叉积 $\overrightarrow{P_0O}\times\vec s=(0\cdot 1-0\cdot 1,\ 0\cdot 1-(-1)\cdot 1,\ (-1)\cdot 1-0\cdot 1)=(0,1,-1)$，模 $\sqrt{2}$，故 $d=\dfrac{\sqrt{2}}{\sqrt{3}}=\sqrt{\dfrac{2}{3}}<2$，直线与球面相交于两点。相交弦长 $=2\sqrt{4-\dfrac{2}{3}}=2\sqrt{\dfrac{10}{3}}$，与解法一中两参数差对应的长度 $|t_1-t_2|\cdot|\vec s|=\dfrac{2\sqrt{10}}{3}\cdot\sqrt{3}=2\sqrt{\dfrac{10}{3}}$ 一致。设直线点$r(t)=(1+t,t,t)$，沿方向$d=(1,1,1)$到球心的最近参数满足$r(t)\cdot d=1+3t=0$，故$t_0=-1/3$、垂足$Q=(2/3,-1/3,-1/3)$。由正交分解$|r(t)|^2=|Q|^2+|d|^2(t-t_0)^2=2/3+3(t+1/3)^2$。令其等于$4$，即$t=(-1\pm\sqrt{10})/3$，代入$r(t)$得到题中两个交点。

answer

两个交点：$\left(\dfrac{2+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3}\right)$ 与 $\left(\dfrac{2-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3}\right)$

scene_spec.objects[0]

球心到直线的垂线段与距离 $\sqrt{\dfrac{2}{3}}$

scene_spec.objects[1]

相交弦长 $2\sqrt{\dfrac{10}{3}}$ 与两参数差的对照

scene_spec.steps[0]

呈现题干及适用条件：求直线 $l:x=1+t,\ y=t,\ z=t$ 与球面 $x^2+y^2+z^2=4$ 的交点个数，并求出交点坐标。

scene_spec.steps[1]

依次呈现：球心到直线的垂线段与距离 $\sqrt{\dfrac{2}{3}}$

scene_spec.steps[2]

依次呈现：相交弦长 $2\sqrt{\dfrac{10}{3}}$ 与两参数差的对照

scene_spec.steps[3]

核对完整证明：球心 $O(0,0,0)$ 到直线距离：直线上取点 $P_0(1,0,0)$、方向 $\vec s=(1,1,1)$，$\overrightarrow{P_0O}=(-1,0,0)$，叉积 $\overrightarrow{P_0O}\times\vec s=(0\cdot 1-0\cdot 1,\ 0\cdot 1-(-1)\cdot 1,\ (-1)\cdot 1-0\cdot 1)=(0,1,-1)$，模 $\sqrt{2}$，故 $d=\dfrac{\sqrt{2}}{\sqrt{3}}=\sqrt{\dfrac{2}{3}}<2$，直线与球面相交于两点。相交弦长 $=2\sqrt{4-\dfrac{2}{3}}=2\sqrt{\dfrac{10}{3}}$，与解法一中两参数差对应的长度 $|t_1-t_2|\cdot|\vec s|=\dfrac{2\sqrt{10}}{3}\cdot\sqrt{3}=2\sqrt{\dfrac{10}{3}}$ 一致。设直线点$r(t)=(1+t,t,t)$，沿方向$d=(1,1,1)$到球心的最近参数满足$r(t)\cdot d=1+3t=0$，故$t_0=-1/3$、垂足$Q=(2/3,-1/3,-1/3)$。由正交分解$|r(t)|^2=|Q|^2+|d|^2(t-t_0)^2=2/3+3(t+1/3)^2$。令其等于$4$，即$t=(-1\pm\sqrt{10})/3$，代入$r(t)$得到题中两个交点。

scene_spec.steps[4]

高亮结果：两个交点：$\left(\dfrac{2+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3}\right)$ 与 $\left(\dfrac{2-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3}\right)$

efficiency_tags[0]

球心到直线的垂线段与距离 $\sqrt{\dfrac{2}{3}}$

efficiency_tags[1]

相交弦长 $2\sqrt{\dfrac{10}{3}}$ 与两参数差的对照

## eval-geom-011-s3

problem

求直线 $l:x=1+t,\ y=t,\ z=t$ 与球面 $x^2+y^2+z^2=4$ 的交点个数，并求出交点坐标。

solution

$3t^2+2t-3=3\left(t+\dfrac{1}{3}\right)^2-\dfrac{10}{3}=0$，故 $t+\dfrac{1}{3}=\pm\dfrac{\sqrt{10}}{3}$，$t=\dfrac{-1\pm\sqrt{10}}{3}$，与解法一相同。

answer

两个交点：$\left(\dfrac{2+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3}\right)$ 与 $\left(\dfrac{2-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3}\right)$

scene_spec.objects[0]

配方 $3\left(t+\dfrac{1}{3}\right)^2-\dfrac{10}{3}=0$ 的对称轴与顶点

scene_spec.objects[1]

球面与直线相交的三维视图

scene_spec.steps[0]

第一步：以配方直接求解为主线，建立解析几何·曲面与曲线场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：配方 $3\left(t+\dfrac{1}{3}\right)^2-\dfrac{10}{3}=0$ 的对称轴与顶点。

scene_spec.steps[2]

第三步：球面与直线相交的三维视图。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

配方 $3\left(t+\dfrac{1}{3}\right)^2-\dfrac{10}{3}=0$ 的对称轴与顶点

efficiency_tags[1]

球面与直线相交的三维视图

## eval-geom-012-s1

problem

求圆柱螺线 $x=a\cos t,\ y=a\sin t,\ z=bt$（$a,b>0$）的曲率与挠率。

solution

记 $c=\sqrt{a^2+b^2}$。$\vec r'=(-a\sin t,a\cos t,b)$，$|\vec r'|=c$；$\vec r''=(-a\cos t,-a\sin t,0)$；$\vec r'\times\vec r''=(ab\sin t,-ab\cos t,a^2)$，模 $\sqrt{a^2b^2+a^4}=ac$。曲率 $\kappa=\dfrac{|\vec r'\times\vec r''|}{|\vec r'|^3}=\dfrac{ac}{c^3}=\dfrac{a}{c^2}=\dfrac{a}{a^2+b^2}$。又 $\vec r'''=(a\sin t,-a\cos t,0)$，挠率 $\tau=\dfrac{(\vec r',\vec r'',\vec r''')}{|\vec r'\times\vec r''|^2}=\dfrac{a^2b\sin^2 t+a^2b\cos^2 t}{a^2c^2}=\dfrac{b}{c^2}=\dfrac{b}{a^2+b^2}$。

answer

曲率 $\kappa=\dfrac{a}{a^2+b^2}$，挠率 $\tau=\dfrac{b}{a^2+b^2}$

scene_spec.objects[0]

向量 $\vec r'\times\vec r''$ 与三阶混合积的计算标注

scene_spec.objects[1]

圆柱螺线与密切圆、副法线

scene_spec.steps[0]

第一步：以Frenet 公式直接计算为主线，建立解析几何·曲线场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：向量 $\vec r'\times\vec r''$ 与三阶混合积的计算标注。

scene_spec.steps[2]

第三步：圆柱螺线与密切圆、副法线。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

向量 $\vec r'\times\vec r''$ 与三阶混合积的计算标注

efficiency_tags[1]

圆柱螺线与密切圆、副法线

## eval-geom-012-s2

problem

求圆柱螺线 $x=a\cos t,\ y=a\sin t,\ z=bt$（$a,b>0$）的曲率与挠率。

solution

速度 $\vec v=\vec r'$，模 $|\vec v|=c$ 恒定，故切向加速度为 $0$；加速度 $\vec a=\vec r''=(-a\cos t,-a\sin t,0)$，模 $|\vec a|=a$。由 $|\vec a|=\kappa|\vec v|^2$ 得 $\kappa=\dfrac{a}{c^2}=\dfrac{a}{a^2+b^2}$。副法向量 $\vec B=\dfrac{\vec r'\times\vec r''}{|\vec r'\times\vec r''|}=\dfrac{1}{c}(b\sin t,-b\cos t,a)$，$\dfrac{d\vec B}{dt}=\dfrac{1}{c}(b\cos t,b\sin t,0)$，模 $\dfrac{b}{c}$。由 Frenet 公式 $\dfrac{d\vec B}{ds}=-\tau\vec N$ 核对方向（本题 $\dfrac{d\vec B}{ds}$ 与 $-\vec N$ 同向，故 $\tau>0$），且 $\left|\dfrac{d\vec B}{ds}\right|=\tau$、$\dfrac{ds}{dt}=c$，得 $\tau=\dfrac{b/c}{c}=\dfrac{b}{a^2+b^2}$。

answer

曲率 $\kappa=\dfrac{a}{a^2+b^2}$，挠率 $\tau=\dfrac{b}{a^2+b^2}$

scene_spec.objects[0]

速度、加速度的分解动画

scene_spec.objects[1]

副法向量 $\vec B$ 的变化率标注

scene_spec.steps[0]

第一步：以物理分解为主线，建立解析几何·曲线场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：速度、加速度的分解动画。

scene_spec.steps[2]

第三步：副法向量 $\vec B$ 的变化率标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

速度、加速度的分解动画

efficiency_tags[1]

副法向量 $\vec B$ 的变化率标注

## eval-geom-012-s3

problem

求圆柱螺线 $x=a\cos t,\ y=a\sin t,\ z=bt$（$a,b>0$）的曲率与挠率。

solution

把圆柱面沿一条母线剪开展平，螺线变成一条直线，其与水平方向的夹角 $\alpha$ 满足 $\tan\alpha=\dfrac{b}{a}$（螺距 $2\pi b$ 与周长 $2\pi a$ 之比），故 $\cos^2\alpha=\dfrac{a^2}{a^2+b^2}$。螺线的曲率完全来自柱面弯曲：$\kappa=\dfrac{\cos^2\alpha}{a}=\dfrac{a}{a^2+b^2}$；挠率来自螺线"扭转"：$\tau=\dfrac{\sin\alpha\cos\alpha}{a}=\dfrac{b}{a^2+b^2}$。$\dfrac{\tau}{\kappa}=\dfrac{b}{a}$ 为常数，说明圆柱螺线是常曲率常挠率曲线。严格推导设$e_r=(\cos t,\sin t,0)$、$e_\theta=(-\sin t,\cos t,0)$、$e_z=(0,0,1)$，令$\tan\alpha=b/a$。单位切向量$T=\cos\alpha\,e_\theta+\sin\alpha\,e_z$，$ds/dt=a/\cos\alpha$。于是$dT/ds=-(\cos^2\alpha/a)e_r$，故$N=-e_r$、$\kappa=\cos^2\alpha/a$；$B=T\times N=\cos\alpha\,e_z-\sin\alpha\,e_\theta$，$dB/ds=(\sin\alpha\cos\alpha/a)e_r=-\tau N$，故$\tau=\sin\alpha\cos\alpha/a$。代$\cos\alpha=a/\sqrt{a^2+b^2}$、$\sin\alpha=b/\sqrt{a^2+b^2}$即得$\kappa=a/(a^2+b^2)$、$\tau=b/(a^2+b^2)$。

answer

曲率 $\kappa=\dfrac{a}{a^2+b^2}$，挠率 $\tau=\dfrac{b}{a^2+b^2}$

scene_spec.objects[0]

圆柱展开成平面、螺线变直线

scene_spec.objects[1]

夹角 $\alpha$ 与 $\kappa:\tau=a:b$ 的标注

scene_spec.steps[0]

呈现题干及适用条件：求圆柱螺线 $x=a\cos t,\ y=a\sin t,\ z=bt$（$a,b>0$）的曲率与挠率。

scene_spec.steps[1]

依次呈现：圆柱展开成平面、螺线变直线

scene_spec.steps[2]

依次呈现：夹角 $\alpha$ 与 $\kappa:\tau=a:b$ 的标注

scene_spec.steps[3]

核对完整证明：把圆柱面沿一条母线剪开展平，螺线变成一条直线，其与水平方向的夹角 $\alpha$ 满足 $\tan\alpha=\dfrac{b}{a}$（螺距 $2\pi b$ 与周长 $2\pi a$ 之比），故 $\cos^2\alpha=\dfrac{a^2}{a^2+b^2}$。螺线的曲率完全来自柱面弯曲：$\kappa=\dfrac{\cos^2\alpha}{a}=\dfrac{a}{a^2+b^2}$；挠率来自螺线"扭转"：$\tau=\dfrac{\sin\alpha\cos\alpha}{a}=\dfrac{b}{a^2+b^2}$。$\dfrac{\tau}{\kappa}=\dfrac{b}{a}$ 为常数，说明圆柱螺线是常曲率常挠率曲线。严格推导设$e_r=(\cos t,\sin t,0)$、$e_\theta=(-\sin t,\cos t,0)$、$e_z=(0,0,1)$，令$\tan\alpha=b/a$。单位切向量$T=\cos\alpha\,e_\theta+\sin\alpha\,e_z$，$ds/dt=a/\cos\alpha$。于是$dT/ds=-(\cos^2\alpha/a)e_r$，故$N=-e_r$、$\kappa=\cos^2\alpha/a$；$B=T\times N=\cos\alpha\,e_z-\sin\alpha\,e_\theta$，$dB/ds=(\sin\alpha\cos\alpha/a)e_r=-\tau N$，故$\tau=\sin\alpha\cos\alpha/a$。代$\cos\alpha=a/\sqrt{a^2+b^2}$、$\sin\alpha=b/\sqrt{a^2+b^2}$即得$\kappa=a/(a^2+b^2)$、$\tau=b/(a^2+b^2)$。

scene_spec.steps[4]

高亮结果：曲率 $\kappa=\dfrac{a}{a^2+b^2}$，挠率 $\tau=\dfrac{b}{a^2+b^2}$

efficiency_tags[0]

圆柱展开成平面、螺线变直线

efficiency_tags[1]

夹角 $\alpha$ 与 $\kappa:\tau=a:b$ 的标注

## eval-geom-013-s1

problem

求曲面 $z=x^2+y^2$ 在点 $(1,1,2)$ 处的切平面与法线方程。

solution

令 $F(x,y,z)=z-x^2-y^2$，曲面为 $F=0$。$\nabla F=(-2x,-2y,1)$，在 $(1,1,2)$ 处为 $\vec n=(-2,-2,1)$。切平面：$-2(x-1)-2(y-1)+1\cdot(z-2)=0$，即 $2x+2y-z=2$。法线：$\dfrac{x-1}{-2}=\dfrac{y-1}{-2}=\dfrac{z-2}{1}$。

answer

切平面 $2x+2y-z=2$；法线 $\dfrac{x-1}{-2}=\dfrac{y-1}{-2}=\dfrac{z-2}{1}$

scene_spec.objects[0]

梯度 $\nabla F=(-2x,-2y,1)$ 在 $(1,1,2)$ 的取值

scene_spec.objects[1]

切平面方程标注

scene_spec.steps[0]

第一步：以梯度法为主线，建立解析几何·曲面与曲线场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：梯度 $\nabla F=(-2x,-2y,1)$ 在 $(1,1,2)$ 的取值。

scene_spec.steps[2]

第三步：切平面方程标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

梯度 $\nabla F=(-2x,-2y,1)$ 在 $(1,1,2)$ 的取值

efficiency_tags[1]

切平面方程标注

## eval-geom-013-s2

problem

求曲面 $z=x^2+y^2$ 在点 $(1,1,2)$ 处的切平面与法线方程。

solution

$dz=2x\,dx+2y\,dy$，在 $(1,1)$ 处 $dz=2dx+2dy$。切平面为 $z-2=2(x-1)+2(y-1)$，即 $2x+2y-z=2$。法线方向由 $(dx,dy,dz)$ 与 $(2,2,-1)$ 垂直得出：法向 $(2,2,-1)$，法线方程同上。

answer

切平面 $2x+2y-z=2$；法线 $\dfrac{x-1}{-2}=\dfrac{y-1}{-2}=\dfrac{z-2}{1}$

scene_spec.objects[0]

全微分 $dz=2x\,dx+2y\,dy$ 的推导

scene_spec.objects[1]

切平面 $z-2=2(x-1)+2(y-1)$ 的贴合

scene_spec.steps[0]

第一步：以全微分为主线，建立解析几何·曲面与曲线场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：全微分 $dz=2x\,dx+2y\,dy$ 的推导。

scene_spec.steps[2]

第三步：切平面 $z-2=2(x-1)+2(y-1)$ 的贴合。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

全微分 $dz=2x\,dx+2y\,dy$ 的推导

efficiency_tags[1]

切平面 $z-2=2(x-1)+2(y-1)$ 的贴合

## eval-geom-013-s3

problem

求曲面 $z=x^2+y^2$ 在点 $(1,1,2)$ 处的切平面与法线方程。

solution

参数化 $\vec r(u,v)=(u,v,u^2+v^2)$。$\vec r_u=(1,0,2u)$，$\vec r_v=(0,1,2v)$，在 $(u,v)=(1,1)$ 处为 $(1,0,2)$、$(0,1,2)$。切平面法向量 $\vec r_u\times\vec r_v=(0\cdot 2-2\cdot 1,\ 2\cdot 0-1\cdot 2,\ 1\cdot 1-0\cdot 0)=(-2,-2,1)$，与解法一一致，切平面、法线同上。

answer

切平面 $2x+2y-z=2$；法线 $\dfrac{x-1}{-2}=\dfrac{y-1}{-2}=\dfrac{z-2}{1}$

scene_spec.objects[0]

两条参数切向量 $\vec r_u=(1,0,2)$、$\vec r_v=(0,1,2)$

scene_spec.objects[1]

叉积得法向量 $(-2,-2,1)$

scene_spec.steps[0]

第一步：以参数化切向量为主线，建立解析几何·曲面与曲线场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：两条参数切向量 $\vec r_u=(1,0,2)$、$\vec r_v=(0,1,2)$。

scene_spec.steps[2]

第三步：叉积得法向量 $(-2,-2,1)$。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

两条参数切向量 $\vec r_u=(1,0,2)$、$\vec r_v=(0,1,2)$

efficiency_tags[1]

叉积得法向量 $(-2,-2,1)$

## eval-geom-014-s1

problem

求椭圆 $\dfrac{x^2}{4}+\dfrac{y^2}{9}=1$ 在点 $\left(\sqrt{2},\dfrac{3}{\sqrt{2}}\right)$ 处的切线方程。

solution

椭圆上点 $(x_0,y_0)$ 处的切线为 $\dfrac{xx_0}{4}+\dfrac{yy_0}{9}=1$。代入 $\left(\sqrt{2},\dfrac{3}{\sqrt{2}}\right)$：$\dfrac{\sqrt{2}}{4}x+\dfrac{3}{9\sqrt{2}}y=1$，即 $\dfrac{\sqrt{2}}{4}x+\dfrac{1}{3\sqrt{2}}y=1$。两边乘 $12\sqrt{2}$：$6x+4y=12\sqrt{2}$，即 $3x+2y=6\sqrt{2}$。检验切点在切线上：$3\sqrt{2}+2\cdot\dfrac{3}{\sqrt{2}}=3\sqrt{2}+3\sqrt{2}=6\sqrt{2}$。

answer

$3x+2y=6\sqrt{2}$

scene_spec.objects[0]

切线公式 $\dfrac{xx_0}{4}+\dfrac{yy_0}{9}=1$ 的代入

scene_spec.objects[1]

椭圆与切线在切点的一阶接触

scene_spec.steps[0]

第一步：以切线公式为主线，建立解析几何·二次曲线场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：切线公式 $\dfrac{xx_0}{4}+\dfrac{yy_0}{9}=1$ 的代入。

scene_spec.steps[2]

第三步：椭圆与切线在切点的一阶接触。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

切线公式 $\dfrac{xx_0}{4}+\dfrac{yy_0}{9}=1$ 的代入

efficiency_tags[1]

椭圆与切线在切点的一阶接触

## eval-geom-014-s2

problem

求椭圆 $\dfrac{x^2}{4}+\dfrac{y^2}{9}=1$ 在点 $\left(\sqrt{2},\dfrac{3}{\sqrt{2}}\right)$ 处的切线方程。

solution

两边对 $x$ 求导：$\dfrac{2x}{4}+\dfrac{2y}{9}y'=0$，得 $y'=-\dfrac{9x}{4y}$。在 $\left(\sqrt{2},\dfrac{3}{\sqrt{2}}\right)$ 处 $y'=-\dfrac{9\sqrt{2}}{4\cdot\frac{3}{\sqrt{2}}}=-\dfrac{9\cdot 2}{12}=-\dfrac{3}{2}$。切线：$y-\dfrac{3}{\sqrt{2}}=-\dfrac{3}{2}(x-\sqrt{2})$，整理得 $2y-\dfrac{6}{\sqrt{2}}=-3x+3\sqrt{2}$，即 $3x+2y=3\sqrt{2}+3\sqrt{2}=6\sqrt{2}$。

answer

$3x+2y=6\sqrt{2}$

scene_spec.objects[0]

隐函数求导 $y'=-\dfrac{9x}{4y}$ 的过程

scene_spec.objects[1]

斜率 $-\dfrac{3}{2}$ 的标注

scene_spec.steps[0]

第一步：以隐函数求导为主线，建立解析几何·二次曲线场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：隐函数求导 $y'=-\dfrac{9x}{4y}$ 的过程。

scene_spec.steps[2]

第三步：斜率 $-\dfrac{3}{2}$ 的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

隐函数求导 $y'=-\dfrac{9x}{4y}$ 的过程

efficiency_tags[1]

斜率 $-\dfrac{3}{2}$ 的标注

## eval-geom-014-s3

problem

求椭圆 $\dfrac{x^2}{4}+\dfrac{y^2}{9}=1$ 在点 $\left(\sqrt{2},\dfrac{3}{\sqrt{2}}\right)$ 处的切线方程。

solution

参数化 $x=2\cos t$、$y=3\sin t$。切点处 $\cos t=\dfrac{\sqrt{2}}{2}$、$\sin t=\dfrac{1}{\sqrt{2}}$，即 $t=\dfrac{\pi}{4}$。切线斜率 $\dfrac{dy}{dx}=\dfrac{3\cos t}{-2\sin t}$，在 $t=\dfrac{\pi}{4}$ 处为 $-\dfrac{3}{2}$。切线方程同解法二，即 $3x+2y=6\sqrt{2}$。

answer

$3x+2y=6\sqrt{2}$

scene_spec.objects[0]

参数化 $x=2\cos t$、$y=3\sin t$ 在 $t=\dfrac{\pi}{4}$ 处

scene_spec.objects[1]

切点沿椭圆滑动的切线族

scene_spec.steps[0]

第一步：以参数化求导为主线，建立解析几何·二次曲线场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：参数化 $x=2\cos t$、$y=3\sin t$ 在 $t=\dfrac{\pi}{4}$ 处。

scene_spec.steps[2]

第三步：切点沿椭圆滑动的切线族。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

参数化 $x=2\cos t$、$y=3\sin t$ 在 $t=\dfrac{\pi}{4}$ 处

efficiency_tags[1]

切点沿椭圆滑动的切线族

## eval-geom-015-s1

problem

求两球面 $x^2+y^2+z^2=4$ 与 $x^2+(y-1)^2+z^2=4$ 的交线方程。

solution

两方程相减：$x^2+y^2+z^2-\left[x^2+(y-1)^2+z^2\right]=0$，即 $y^2-(y^2-2y+1)=0$，得 $2y-1=0$，$y=\dfrac{1}{2}$。代入第一式：$x^2+z^2=4-\dfrac{1}{4}=\dfrac{15}{4}$。交线为平面 $y=\dfrac{1}{2}$ 上的圆 $x^2+z^2=\dfrac{15}{4}$。

answer

圆：$y=\dfrac{1}{2}$，$x^2+z^2=\dfrac{15}{4}$（圆心 $\left(0,\dfrac{1}{2},0\right)$，半径 $\dfrac{\sqrt{15}}{2}$）

scene_spec.objects[0]

两式相减得 $y=\dfrac{1}{2}$ 的消元动画

scene_spec.objects[1]

代入得圆 $x^2+z^2=\dfrac{15}{4}$

scene_spec.steps[0]

第一步：以两式相减为主线，建立解析几何·曲面与曲线场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：两式相减得 $y=\dfrac{1}{2}$ 的消元动画。

scene_spec.steps[2]

第三步：代入得圆 $x^2+z^2=\dfrac{15}{4}$。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

两式相减得 $y=\dfrac{1}{2}$ 的消元动画

efficiency_tags[1]

代入得圆 $x^2+z^2=\dfrac{15}{4}$

## eval-geom-015-s2

problem

求两球面 $x^2+y^2+z^2=4$ 与 $x^2+(y-1)^2+z^2=4$ 的交线方程。

solution

两球半径相等（均为 $2$），故交线圆所在平面是两球心连线的垂直平分面。球心 $O_1(0,0,0)$、$O_2(0,1,0)$，垂直平分面为 $y=\dfrac{1}{2}$。球心 $O_1$ 到该平面的距离为 $\dfrac{1}{2}$，故截面圆半径 $\sqrt{2^2-\left(\dfrac{1}{2}\right)^2}=\dfrac{\sqrt{15}}{2}$，圆心 $\left(0,\dfrac{1}{2},0\right)$。

answer

圆：$y=\dfrac{1}{2}$，$x^2+z^2=\dfrac{15}{4}$（圆心 $\left(0,\dfrac{1}{2},0\right)$，半径 $\dfrac{\sqrt{15}}{2}$）

scene_spec.objects[0]

两相交球面的三维视图

scene_spec.objects[1]

球心连线的垂直平分面与截面圆

scene_spec.steps[0]

第一步：以平面截球为主线，建立解析几何·曲面与曲线场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：两相交球面的三维视图。

scene_spec.steps[2]

第三步：球心连线的垂直平分面与截面圆。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

两相交球面的三维视图

efficiency_tags[1]

球心连线的垂直平分面与截面圆

## eval-geom-015-s3

problem

求两球面 $x^2+y^2+z^2=4$ 与 $x^2+(y-1)^2+z^2=4$ 的交线方程。

solution

由圆方程直接参数化：$x=\dfrac{\sqrt{15}}{2}\cos t$，$y=\dfrac{1}{2}$，$z=\dfrac{\sqrt{15}}{2}\sin t$，$t\in[0,2\pi]$。代回两球面验证：$x^2+y^2+z^2=\dfrac{15}{4}+\dfrac{1}{4}=4$；$x^2+(y-1)^2+z^2=\dfrac{15}{4}+\dfrac{1}{4}=4$。

answer

圆：$y=\dfrac{1}{2}$，$x^2+z^2=\dfrac{15}{4}$（圆心 $\left(0,\dfrac{1}{2},0\right)$，半径 $\dfrac{\sqrt{15}}{2}$）

scene_spec.objects[0]

参数点沿交线圆运动

scene_spec.objects[1]

代回两球面验证恒等式

scene_spec.steps[0]

第一步：以参数化为主线，建立解析几何·曲面与曲线场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：参数点沿交线圆运动。

scene_spec.steps[2]

第三步：代回两球面验证恒等式。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

参数点沿交线圆运动

efficiency_tags[1]

代回两球面验证恒等式

## eval-geom-016-s1

problem

已知 $|\vec a|=2$，$|\vec b|=3$，$\vec a$ 与 $\vec b$ 的夹角为 $60^\circ$，求 $|\vec a+\vec b|$、$|2\vec a-\vec b|$ 及 $\vec a+\vec b$ 与 $\vec a-\vec b$ 的夹角余弦。

solution

$|\vec a+\vec b|^2=|\vec a|^2+|\vec b|^2+2|\vec a||\vec b|\cos 60^\circ=4+9+2\cdot 2\cdot 3\cdot\dfrac{1}{2}=19$，故 $|\vec a+\vec b|=\sqrt{19}$。$|2\vec a-\vec b|^2=4|\vec a|^2+|\vec b|^2-4|\vec a||\vec b|\cos 60^\circ=16+9-12=13$，故 $|2\vec a-\vec b|=\sqrt{13}$。又 $(\vec a+\vec b)\cdot(\vec a-\vec b)=|\vec a|^2-|\vec b|^2=4-9=-5$，$|\vec a-\vec b|^2=4+9-2\cdot 2\cdot 3\cdot\dfrac{1}{2}=7$，故 $\cos\theta=\dfrac{-5}{\sqrt{19}\cdot\sqrt{7}}=-\dfrac{5}{\sqrt{133}}$。

answer

$|\vec a+\vec b|=\sqrt{19}$，$|2\vec a-\vec b|=\sqrt{13}$，$\cos\theta=-\dfrac{5}{\sqrt{133}}$

scene_spec.objects[0]

模长平方公式的逐项展开

scene_spec.objects[1]

点积恒等式 $(\vec a+\vec b)\cdot(\vec a-\vec b)=|\vec a|^2-|\vec b|^2$ 的标注

scene_spec.steps[0]

第一步：以模长公式为主线，建立解析几何·向量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：模长平方公式的逐项展开。

scene_spec.steps[2]

第三步：点积恒等式 $(\vec a+\vec b)\cdot(\vec a-\vec b)=|\vec a|^2-|\vec b|^2$ 的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

模长平方公式的逐项展开

efficiency_tags[1]

点积恒等式 $(\vec a+\vec b)\cdot(\vec a-\vec b)=|\vec a|^2-|\vec b|^2$ 的标注

## eval-geom-016-s2

problem

已知 $|\vec a|=2$，$|\vec b|=3$，$\vec a$ 与 $\vec b$ 的夹角为 $60^\circ$，求 $|\vec a+\vec b|$、$|2\vec a-\vec b|$ 及 $\vec a+\vec b$ 与 $\vec a-\vec b$ 的夹角余弦。

solution

取 $\vec a=(2,0)$，$\vec b=\left(\dfrac{3}{2},\dfrac{3\sqrt{3}}{2}\right)$。则 $\vec a+\vec b=\left(\dfrac{7}{2},\dfrac{3\sqrt{3}}{2}\right)$，$|\vec a+\vec b|^2=\dfrac{49}{4}+\dfrac{27}{4}=19$；$2\vec a-\vec b=\left(\dfrac{5}{2},-\dfrac{3\sqrt{3}}{2}\right)$，模平方 $\dfrac{25}{4}+\dfrac{27}{4}=13$；$\vec a-\vec b=\left(\dfrac{1}{2},-\dfrac{3\sqrt{3}}{2}\right)$，$(\vec a+\vec b)\cdot(\vec a-\vec b)=\dfrac{7}{4}-\dfrac{27}{4}=-5$，与解法一一致。

answer

$|\vec a+\vec b|=\sqrt{19}$，$|2\vec a-\vec b|=\sqrt{13}$，$\cos\theta=-\dfrac{5}{\sqrt{133}}$

scene_spec.objects[0]

坐标化 $\vec a=(2,0)$、$\vec b=\left(\dfrac{3}{2},\dfrac{3\sqrt3}{2}\right)$ 的分量计算

scene_spec.objects[1]

各向量坐标标注

scene_spec.steps[0]

第一步：以坐标法为主线，建立解析几何·向量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：坐标化 $\vec a=(2,0)$、$\vec b=\left(\dfrac{3}{2},\dfrac{3\sqrt3}{2}\right)$ 的分量计算。

scene_spec.steps[2]

第三步：各向量坐标标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

坐标化 $\vec a=(2,0)$、$\vec b=\left(\dfrac{3}{2},\dfrac{3\sqrt3}{2}\right)$ 的分量计算

efficiency_tags[1]

各向量坐标标注

## eval-geom-016-s3

problem

已知 $|\vec a|=2$，$|\vec b|=3$，$\vec a$ 与 $\vec b$ 的夹角为 $60^\circ$，求 $|\vec a+\vec b|$、$|2\vec a-\vec b|$ 及 $\vec a+\vec b$ 与 $\vec a-\vec b$ 的夹角余弦。

solution

将$\vec a,\vec b$置于同一起点，夹角$\pi/3$。平行四边形对角线给出$|\vec a+\vec b|^2=4+9+2\cdot2\cdot3\cos(\pi/3)=19$。以$2\vec a,\vec b$两终点及原点构成三角形，原点内角为$\pi/3$，对边为$2\vec a-\vec b$，由余弦定理$|2\vec a-\vec b|^2=16+9-2\cdot4\cdot3\cos(\pi/3)=13$。另有$|\vec a-\vec b|^2=4+9-2\cdot2\cdot3\cos(\pi/3)=7$，两对角线的点积$(\vec a+\vec b)\cdot(\vec a-\vec b)=|\vec a|^2-|\vec b|^2=-5$，故夹角余弦为$-5/\sqrt{19\cdot7}=-5/\sqrt{133}$。

answer

$|\vec a+\vec b|=\sqrt{19}$，$|2\vec a-\vec b|=\sqrt{13}$，$\cos\theta=-\dfrac{5}{\sqrt{133}}$

scene_spec.objects[0]

平行四边形的和、差向量

scene_spec.objects[1]

三角形的两边为$2\vec a,\vec b$，内角$\pi/3$，对边为$2\vec a-\vec b$

scene_spec.objects[2]

余弦定理$16+9-24\cos(\pi/3)=13$

scene_spec.steps[0]

呈现题干及适用条件：已知 $|\vec a|=2$，$|\vec b|=3$，$\vec a$ 与 $\vec b$ 的夹角为 $60^\circ$，求 $|\vec a+\vec b|$、$|2\vec a-\vec b|$ 及 $\vec a+\vec b$ 与 $\vec a-\vec b$ 的夹角余弦。

scene_spec.steps[1]

依次呈现：平行四边形的和、差向量

scene_spec.steps[2]

依次呈现：三角形的两边为$2\vec a,\vec b$，内角$\pi/3$，对边为$2\vec a-\vec b$

scene_spec.steps[3]

依次呈现：余弦定理$16+9-24\cos(\pi/3)=13$

scene_spec.steps[4]

核对完整证明：将$\vec a,\vec b$置于同一起点，夹角$\pi/3$。平行四边形对角线给出$|\vec a+\vec b|^2=4+9+2\cdot2\cdot3\cos(\pi/3)=19$。以$2\vec a,\vec b$两终点及原点构成三角形，原点内角为$\pi/3$，对边为$2\vec a-\vec b$，由余弦定理$|2\vec a-\vec b|^2=16+9-2\cdot4\cdot3\cos(\pi/3)=13$。另有$|\vec a-\vec b|^2=4+9-2\cdot2\cdot3\cos(\pi/3)=7$，两对角线的点积$(\vec a+\vec b)\cdot(\vec a-\vec b)=|\vec a|^2-|\vec b|^2=-5$，故夹角余弦为$-5/\sqrt{19\cdot7}=-5/\sqrt{133}$。

scene_spec.steps[5]

高亮结果：$|\vec a+\vec b|=\sqrt{19}$，$|2\vec a-\vec b|=\sqrt{13}$，$\cos\theta=-\dfrac{5}{\sqrt{133}}$

efficiency_tags[0]

平行四边形的和、差向量

efficiency_tags[1]

三角形的两边为$2\vec a,\vec b$，内角$\pi/3$，对边为$2\vec a-\vec b$

efficiency_tags[2]

余弦定理$16+9-24\cos(\pi/3)=13$

## eval-geom-017-s1

problem

已知 $\vec a=(1,2,2)$，$\vec b=(-2,1,2)$，求 $\vec a$ 与 $\vec b$ 的夹角余弦及 $\vec a$ 在 $\vec b$ 上的投影向量。

solution

$\vec a\cdot\vec b=1\cdot(-2)+2\cdot 1+2\cdot 2=4$，$|\vec a|=\sqrt{1+4+4}=3$，$|\vec b|=\sqrt{4+1+4}=3$，故 $\cos\theta=\dfrac{4}{3\cdot 3}=\dfrac{4}{9}$。投影向量 $\mathrm{proj}_{\vec b}\vec a=\dfrac{\vec a\cdot\vec b}{|\vec b|^2}\vec b=\dfrac{4}{9}(-2,1,2)=\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)$。

answer

$\cos\theta=\dfrac{4}{9}$；投影向量 $\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)$

scene_spec.objects[0]

点积 $\vec a\cdot\vec b=4$ 与模长 $3,3$ 的标注

scene_spec.objects[1]

夹角余弦 $\dfrac{4}{9}$

scene_spec.steps[0]

第一步：以点积公式为主线，建立解析几何·向量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：点积 $\vec a\cdot\vec b=4$ 与模长 $3,3$ 的标注。

scene_spec.steps[2]

第三步：夹角余弦 $\dfrac{4}{9}$。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

点积 $\vec a\cdot\vec b=4$ 与模长 $3,3$ 的标注

efficiency_tags[1]

夹角余弦 $\dfrac{4}{9}$

## eval-geom-017-s2

problem

已知 $\vec a=(1,2,2)$，$\vec b=(-2,1,2)$，求 $\vec a$ 与 $\vec b$ 的夹角余弦及 $\vec a$ 在 $\vec b$ 上的投影向量。

solution

投影长度 $|\vec a|\cos\theta=3\cdot\dfrac{4}{9}=\dfrac{4}{3}$，方向为 $\dfrac{\vec b}{|\vec b|}=\dfrac{1}{3}(-2,1,2)$，故投影向量 $=\dfrac{4}{3}\cdot\dfrac{1}{3}(-2,1,2)=\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)$。夹角也可由余弦定理独立确定：$|\vec a-\vec b|^2=|(3,1,0)|^2=10$，$|\vec a|=|\vec b|=3$，故$\cos\theta=(9+9-10)/(2\cdot3\cdot3)=4/9$。

answer

$\cos\theta=\dfrac{4}{9}$；投影向量 $\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)$

scene_spec.objects[0]

投影长度 $\dfrac{4}{3}$ 与单位方向 $\dfrac{\vec b}{3}$ 的乘积

scene_spec.objects[1]

三维向量与夹角

scene_spec.steps[0]

呈现题干及适用条件：已知 $\vec a=(1,2,2)$，$\vec b=(-2,1,2)$，求 $\vec a$ 与 $\vec b$ 的夹角余弦及 $\vec a$ 在 $\vec b$ 上的投影向量。

scene_spec.steps[1]

依次呈现：投影长度 $\dfrac{4}{3}$ 与单位方向 $\dfrac{\vec b}{3}$ 的乘积

scene_spec.steps[2]

依次呈现：三维向量与夹角

scene_spec.steps[3]

核对完整证明：投影长度 $|\vec a|\cos\theta=3\cdot\dfrac{4}{9}=\dfrac{4}{3}$，方向为 $\dfrac{\vec b}{|\vec b|}=\dfrac{1}{3}(-2,1,2)$，故投影向量 $=\dfrac{4}{3}\cdot\dfrac{1}{3}(-2,1,2)=\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)$。夹角也可由余弦定理独立确定：$|\vec a-\vec b|^2=|(3,1,0)|^2=10$，$|\vec a|=|\vec b|=3$，故$\cos\theta=(9+9-10)/(2\cdot3\cdot3)=4/9$。

scene_spec.steps[4]

高亮结果：$\cos\theta=\dfrac{4}{9}$；投影向量 $\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)$

efficiency_tags[0]

投影长度 $\dfrac{4}{3}$ 与单位方向 $\dfrac{\vec b}{3}$ 的乘积

efficiency_tags[1]

三维向量与夹角

## eval-geom-017-s3

problem

已知 $\vec a=(1,2,2)$，$\vec b=(-2,1,2)$，求 $\vec a$ 与 $\vec b$ 的夹角余弦及 $\vec a$ 在 $\vec b$ 上的投影向量。

solution

取单位向量 $\vec u=\dfrac{\vec b}{3}=\left(-\dfrac{2}{3},\dfrac{1}{3},\dfrac{2}{3}\right)$，则 $\vec a=\left(\vec a\cdot\vec u\right)\vec u+\vec a_\perp$，其中 $\vec a\cdot\vec u=\dfrac{4}{3}$，$\vec a_\perp=\vec a-\dfrac{4}{3}\vec u=(1,2,2)-\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)=\left(\dfrac{17}{9},\dfrac{14}{9},\dfrac{10}{9}\right)$。验证 $\vec a_\perp\cdot\vec b=\dfrac{17}{9}\cdot(-2)+\dfrac{14}{9}\cdot 1+\dfrac{10}{9}\cdot 2=\dfrac{-34+14+20}{9}=0$，正交分解成立，投影分量即 $\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)$。

answer

$\cos\theta=\dfrac{4}{9}$；投影向量 $\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)$

scene_spec.objects[0]

$a$ 分解为平行/垂直分量

scene_spec.objects[1]

正交性验证 $\vec a_\perp\cdot\vec b=0$

scene_spec.steps[0]

第一步：以正交分解验证为主线，建立解析几何·向量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：$a$ 分解为平行/垂直分量。

scene_spec.steps[2]

第三步：正交性验证 $\vec a_\perp\cdot\vec b=0$。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

$a$ 分解为平行/垂直分量

efficiency_tags[1]

正交性验证 $\vec a_\perp\cdot\vec b=0$

## eval-geom-018-s1

problem

求以 $O(0,0,0)$、$A(2,0,0)$、$B(0,3,0)$、$C(0,0,4)$ 为顶点的四面体体积。

solution

$V=\dfrac{1}{6}\left|\det(\overrightarrow{OA},\overrightarrow{OB},\overrightarrow{OC})\right|=\dfrac{1}{6}\left|\begin{vmatrix}2&0&0\\0&3&0\\0&0&4\end{vmatrix}\right|=\dfrac{24}{6}=4$。

answer

$4$

scene_spec.objects[0]

混合积行列式 $\begin{vmatrix}2&0&0\\0&3&0\\0&0&4\end{vmatrix}=24$ 的计算

scene_spec.objects[1]

四面体与对应平行六面体

scene_spec.steps[0]

第一步：以混合积为主线，建立解析几何·向量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：混合积行列式 $\begin{vmatrix}2&0&0\\0&3&0\\0&0&4\end{vmatrix}=24$ 的计算。

scene_spec.steps[2]

第三步：四面体与对应平行六面体。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

混合积行列式 $\begin{vmatrix}2&0&0\\0&3&0\\0&0&4\end{vmatrix}=24$ 的计算

efficiency_tags[1]

四面体与对应平行六面体

## eval-geom-018-s2

problem

求以 $O(0,0,0)$、$A(2,0,0)$、$B(0,3,0)$、$C(0,0,4)$ 为顶点的四面体体积。

solution

取底面 $OAB$：面积 $S=\dfrac{1}{2}\cdot 2\cdot 3=3$。顶点 $C$ 到平面 $xOy$ 的距离即高 $h=4$。故 $V=\dfrac{1}{3}Sh=\dfrac{1}{3}\cdot 3\cdot 4=4$。

answer

$4$

scene_spec.objects[0]

底面积 $\dfrac{1}{2}\cdot2\cdot3=3$ 与高 4 的标注

scene_spec.objects[1]

体积 $\dfrac{1}{3}Sh=4$

scene_spec.steps[0]

第一步：以底面积×高为主线，建立解析几何·向量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：底面积 $\dfrac{1}{2}\cdot2\cdot3=3$ 与高 4 的标注。

scene_spec.steps[2]

第三步：体积 $\dfrac{1}{3}Sh=4$。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

底面积 $\dfrac{1}{2}\cdot2\cdot3=3$ 与高 4 的标注

efficiency_tags[1]

体积 $\dfrac{1}{3}Sh=4$

## eval-geom-018-s3

problem

求以 $O(0,0,0)$、$A(2,0,0)$、$B(0,3,0)$、$C(0,0,4)$ 为顶点的四面体体积。

solution

四面体区域为 $\dfrac{x}{2}+\dfrac{y}{3}+\dfrac{z}{4}\le 1$、$x,y,z\ge 0$。作线性替换 $u=\dfrac{x}{2}$、$v=\dfrac{y}{3}$、$w=\dfrac{z}{4}$（雅可比行列式 $\dfrac{\partial(x,y,z)}{\partial(u,v,w)}=2\cdot 3\cdot 4=24$），区域变为 $u+v+w\le 1$、$u,v,w\ge 0$。$V=\displaystyle\iiint dx\,dy\,dz=24\iiint du\,dv\,dw=24\cdot\dfrac{1}{6}=4$（单位单纯形 $u+v+w\le 1,\ u,v,w\ge 0$ 的体积为 $\dfrac{1}{6}$）。

answer

$4$

scene_spec.objects[0]

线性替换 $u=\dfrac{x}{2}$ 等拉正为标准单纯形

scene_spec.objects[1]

雅可比 $24$ 与单纯形体积 $\dfrac{1}{6}$ 的标注

scene_spec.steps[0]

第一步：以三重积分为主线，建立解析几何·向量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：线性替换 $u=\dfrac{x}{2}$ 等拉正为标准单纯形。

scene_spec.steps[2]

第三步：雅可比 $24$ 与单纯形体积 $\dfrac{1}{6}$ 的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

线性替换 $u=\dfrac{x}{2}$ 等拉正为标准单纯形

efficiency_tags[1]

雅可比 $24$ 与单纯形体积 $\dfrac{1}{6}$ 的标注

## eval-geom-019-s1

problem

求两平面 $\pi_1:x+y+z=1$ 与 $\pi_2:x+2y+3z=6$ 的交线方程。

solution

方向向量 $\vec s=\vec{n_1}\times\vec{n_2}=(1,1,1)\times(1,2,3)=(1\cdot 3-1\cdot 2,\ 1\cdot 1-1\cdot 3,\ 1\cdot 2-1\cdot 1)=(1,-2,1)$。求交线上一点：令 $z=0$，解 $\begin{cases}x+y=1\\x+2y=6\end{cases}$，两式相减得 $y=5$、$x=-4$，得点 $P_0(-4,5,0)$。交线为 $\dfrac{x+4}{1}=\dfrac{y-5}{-2}=\dfrac{z}{1}$。

answer

$\dfrac{x+4}{1}=\dfrac{y-5}{-2}=\dfrac{z}{1}$，即 $(x,y,z)=(-4+t,5-2t,t)$

scene_spec.objects[0]

叉积 $\vec s=(1,-2,1)$ 的方向动画

scene_spec.objects[1]

点 $P_0(-4,5,0)$ 的定位

scene_spec.steps[0]

第一步：以法向量叉积为主线，建立解析几何·直线与平面场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：叉积 $\vec s=(1,-2,1)$ 的方向动画。

scene_spec.steps[2]

第三步：点 $P_0(-4,5,0)$ 的定位。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

叉积 $\vec s=(1,-2,1)$ 的方向动画

efficiency_tags[1]

点 $P_0(-4,5,0)$ 的定位

## eval-geom-019-s2

problem

求两平面 $\pi_1:x+y+z=1$ 与 $\pi_2:x+2y+3z=6$ 的交线方程。

solution

方程组 $\begin{cases}x+y+z=1\\x+2y+3z=6\end{cases}$。第二式减第一式：$y+2z=5$，即 $y=5-2z$；代回第一式：$x+5-2z+z=1$，$x=z-4$。令 $z=t$，得参数方程 $(x,y,z)=(t-4,5-2t,t)=(-4+t,5-2t,t)$。

answer

$\dfrac{x+4}{1}=\dfrac{y-5}{-2}=\dfrac{z}{1}$，即 $(x,y,z)=(-4+t,5-2t,t)$

scene_spec.objects[0]

高斯消元得 $y=5-2z$、$x=z-4$ 的步骤

scene_spec.objects[1]

参数方程 $(t-4,5-2t,t)$ 的生成

scene_spec.steps[0]

第一步：以高斯消元为主线，建立解析几何·直线与平面场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：高斯消元得 $y=5-2z$、$x=z-4$ 的步骤。

scene_spec.steps[2]

第三步：参数方程 $(t-4,5-2t,t)$ 的生成。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

高斯消元得 $y=5-2z$、$x=z-4$ 的步骤

efficiency_tags[1]

参数方程 $(t-4,5-2t,t)$ 的生成

## eval-geom-019-s3

problem

求两平面 $\pi_1:x+y+z=1$ 与 $\pi_2:x+2y+3z=6$ 的交线方程。

solution

由解法一/二得 $(x,y,z)=(-4+t,5-2t,t)$。代入 $\pi_1$：$(-4+t)+(5-2t)+t=1$；代入 $\pi_2$：$(-4+t)+2(5-2t)+3t=-4+t+10-4t+3t=6$。两式恒成立，故确为交线。完备性：任取两平面的公共点，令$z=t$，两式相减得$y+2t=5$，所以$y=5-2t$；代回第一式得$x=t-4$。因此每个公共点都在所列参数线上，已得到完整交线。

answer

$\dfrac{x+4}{1}=\dfrac{y-5}{-2}=\dfrac{z}{1}$，即 $(x,y,z)=(-4+t,5-2t,t)$

scene_spec.objects[0]

参数点沿交线运动

scene_spec.objects[1]

代回两平面恒成立的验证

scene_spec.steps[0]

呈现题干及适用条件：求两平面 $\pi_1:x+y+z=1$ 与 $\pi_2:x+2y+3z=6$ 的交线方程。

scene_spec.steps[1]

依次呈现：参数点沿交线运动

scene_spec.steps[2]

依次呈现：代回两平面恒成立的验证

scene_spec.steps[3]

核对完整证明：由解法一/二得 $(x,y,z)=(-4+t,5-2t,t)$。代入 $\pi_1$：$(-4+t)+(5-2t)+t=1$；代入 $\pi_2$：$(-4+t)+2(5-2t)+3t=-4+t+10-4t+3t=6$。两式恒成立，故确为交线。完备性：任取两平面的公共点，令$z=t$，两式相减得$y+2t=5$，所以$y=5-2t$；代回第一式得$x=t-4$。因此每个公共点都在所列参数线上，已得到完整交线。

scene_spec.steps[4]

高亮结果：$\dfrac{x+4}{1}=\dfrac{y-5}{-2}=\dfrac{z}{1}$，即 $(x,y,z)=(-4+t,5-2t,t)$

efficiency_tags[0]

参数点沿交线运动

efficiency_tags[1]

代回两平面恒成立的验证

## eval-geom-020-s1

problem

判断四点 $A(1,2,3)$、$B(2,3,4)$、$C(3,5,7)$、$D(2,4,6)$ 是否共面。

solution

$\overrightarrow{AB}=(1,1,1)$，$\overrightarrow{AC}=(2,3,4)$，$\overrightarrow{AD}=(1,2,3)$。混合积 $\det(\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD})=\begin{vmatrix}1&1&1\\2&3&4\\1&2&3\end{vmatrix}=1\cdot(9-8)-1\cdot(6-4)+1\cdot(4-3)=1-2+1=0$，故四点共面。

answer

共面

scene_spec.objects[0]

混合积行列式 $\begin{vmatrix}1&1&1\\2&3&4\\1&2&3\end{vmatrix}=0$ 的计算

scene_spec.objects[1]

平行六面体体积为零的动画

scene_spec.steps[0]

第一步：以混合积为零为主线，建立解析几何·向量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：混合积行列式 $\begin{vmatrix}1&1&1\\2&3&4\\1&2&3\end{vmatrix}=0$ 的计算。

scene_spec.steps[2]

第三步：平行六面体体积为零的动画。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

混合积行列式 $\begin{vmatrix}1&1&1\\2&3&4\\1&2&3\end{vmatrix}=0$ 的计算

efficiency_tags[1]

平行六面体体积为零的动画

## eval-geom-020-s2

problem

判断四点 $A(1,2,3)$、$B(2,3,4)$、$C(3,5,7)$、$D(2,4,6)$ 是否共面。

solution

过 $A,B,C$ 的平面法向量 $\vec n=\overrightarrow{AB}\times\overrightarrow{AC}=(1,1,1)\times(2,3,4)=(1\cdot 4-1\cdot 3,\ 1\cdot 2-1\cdot 4,\ 1\cdot 3-1\cdot 2)=(1,-2,1)$。平面方程：$(x-1)-2(y-2)+(z-3)=0$，即 $x-2y+z=0$。代入 $D(2,4,6)$：$2-8+6=0$，满足方程，故 $D$ 在平面 $ABC$ 上，四点共面。

answer

共面

scene_spec.objects[0]

平面方程 $x-2y+z=0$ 的建立

scene_spec.objects[1]

代入 $D(2,4,6)$ 验证 $2-8+6=0$

scene_spec.steps[0]

第一步：以平面方程检验为主线，建立解析几何·向量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：平面方程 $x-2y+z=0$ 的建立。

scene_spec.steps[2]

第三步：代入 $D(2,4,6)$ 验证 $2-8+6=0$。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

平面方程 $x-2y+z=0$ 的建立

efficiency_tags[1]

代入 $D(2,4,6)$ 验证 $2-8+6=0$

## eval-geom-020-s3

problem

判断四点 $A(1,2,3)$、$B(2,3,4)$、$C(3,5,7)$、$D(2,4,6)$ 是否共面。

solution

检查 $\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}$ 是否线性相关。设 $k_1(1,1,1)+k_2(2,3,4)+k_3(1,2,3)=(0,0,0)$，即 $\begin{cases}k_1+2k_2+k_3=0\\k_1+3k_2+2k_3=0\\k_1+4k_2+3k_3=0\end{cases}$。第二式减第一式、第三式减第二式均得 $k_2+k_3=0$，取 $k_2=1$、$k_3=-1$，则 $k_1=-1$。验证 $-(1,1,1)+(2,3,4)-(1,2,3)=(0,0,0)$，存在非零解，故三向量线性相关，四点共面。

answer

共面

scene_spec.objects[0]

三个向量的线性组合 $-(1,1,1)+(2,3,4)-(1,2,3)=(0,0,0)$ 回到原点

scene_spec.objects[1]

四点与所在平面

scene_spec.steps[0]

第一步：以向量组线性相关为主线，建立解析几何·向量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：三个向量的线性组合 $-(1,1,1)+(2,3,4)-(1,2,3)=(0,0,0)$ 回到原点。

scene_spec.steps[2]

第三步：四点与所在平面。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

三个向量的线性组合 $-(1,1,1)+(2,3,4)-(1,2,3)=(0,0,0)$ 回到原点

efficiency_tags[1]

四点与所在平面

## eval-prob-001-s1

problem

三扇门中车的位置等概率，初选与车的位置独立。主持人知道车的位置，总从未选的门中打开一扇有羊的门，并总给出换门机会。求坚持初选和换至唯一剩余未开的门各自获车概率。

solution

参赛者初始选中山羊的概率为 $\dfrac{2}{3}$，此时主持人必须打开另一扇山羊门（他不能开车门），剩下的未开门必然是汽车，换门必赢。初始选中汽车的概率为 $\dfrac{1}{3}$，此时换门必输。故换门获胜概率 $=\dfrac{2}{3}\times 1+\dfrac{1}{3}\times 0=\dfrac{2}{3}$。

answer

换门获胜概率为 $\dfrac{2}{3}$，不换为 $\dfrac{1}{3}$

scene_spec.objects[0]

三扇门与车、羊的随机放置

scene_spec.objects[1]

初选山羊（概率 $\dfrac{2}{3}$）与换门必赢的对应标注

scene_spec.steps[0]

呈现题干及适用条件：三扇门中车的位置等概率，初选与车的位置独立。主持人知道车的位置，总从未选的门中打开一扇有羊的门，并总给出换门机会。求坚持初选和换至唯一剩余未开的门各自获车概率。

scene_spec.steps[1]

依次呈现：三扇门与车、羊的随机放置

scene_spec.steps[2]

依次呈现：初选山羊（概率 $\dfrac{2}{3}$）与换门必赢的对应标注

scene_spec.steps[3]

核对完整证明：参赛者初始选中山羊的概率为 $\dfrac{2}{3}$，此时主持人必须打开另一扇山羊门（他不能开车门），剩下的未开门必然是汽车，换门必赢。初始选中汽车的概率为 $\dfrac{1}{3}$，此时换门必输。故换门获胜概率 $=\dfrac{2}{3}\times 1+\dfrac{1}{3}\times 0=\dfrac{2}{3}$。

scene_spec.steps[4]

高亮结果：换门获胜概率为 $\dfrac{2}{3}$，不换为 $\dfrac{1}{3}$

efficiency_tags[0]

三扇门与车、羊的随机放置

efficiency_tags[1]

初选山羊（概率 $\dfrac{2}{3}$）与换门必赢的对应标注

## eval-prob-001-s2

problem

三扇门中车的位置等概率，初选与车的位置独立。主持人知道车的位置，总从未选的门中打开一扇有羊的门，并总给出换门机会。求坚持初选和换至唯一剩余未开的门各自获车概率。

solution

设参赛者选 1 号门、主持人打开 2 号门，并假设主持人在有两扇羊门可选时等概率选择（其余情形由对称性同理）。记 $C_i$=车在 $i$ 号门，$H_2$=主持人开 2 号门。则 $P(H_2|C_3)=1$（车在 3 号门时主持人只能开 2 号门），$P(H_2|C_1)=\dfrac{1}{2}$（车在 1 号门时主持人可在 2、3 号门中等概率选择），$P(H_2|C_2)=0$（主持人不能开有车的门），$P(C_i)=\dfrac{1}{3}$。由贝叶斯公式：$P(C_3|H_2)=\dfrac{P(H_2|C_3)P(C_3)}{P(H_2|C_3)P(C_3)+P(H_2|C_1)P(C_1)+P(H_2|C_2)P(C_2)}=\dfrac{1\cdot\frac{1}{3}}{1\cdot\frac{1}{3}+\frac{1}{2}\cdot\frac{1}{3}+0}=\dfrac{1/3}{1/2}=\dfrac{2}{3}$。即主持人开 2 号门后，车在 3 号门（换门目标）的概率为 $\dfrac{2}{3}$。注意"总是换门"的获胜率 $\dfrac{2}{3}$ 其实不依赖主持人的等概率规则（见解法一）。

answer

换门获胜概率为 $\dfrac{2}{3}$，不换为 $\dfrac{1}{3}$

scene_spec.objects[0]

贝叶斯分母三项的条带分解

scene_spec.objects[1]

条件概率 $P(C_3|H_2)$ 的收缩动画

scene_spec.steps[0]

呈现题干及适用条件：三扇门中车的位置等概率，初选与车的位置独立。主持人知道车的位置，总从未选的门中打开一扇有羊的门，并总给出换门机会。求坚持初选和换至唯一剩余未开的门各自获车概率。

scene_spec.steps[1]

依次呈现：贝叶斯分母三项的条带分解

scene_spec.steps[2]

依次呈现：条件概率 $P(C_3|H_2)$ 的收缩动画

scene_spec.steps[3]

核对完整证明：设参赛者选 1 号门、主持人打开 2 号门，并假设主持人在有两扇羊门可选时等概率选择（其余情形由对称性同理）。记 $C_i$=车在 $i$ 号门，$H_2$=主持人开 2 号门。则 $P(H_2|C_3)=1$（车在 3 号门时主持人只能开 2 号门），$P(H_2|C_1)=\dfrac{1}{2}$（车在 1 号门时主持人可在 2、3 号门中等概率选择），$P(H_2|C_2)=0$（主持人不能开有车的门），$P(C_i)=\dfrac{1}{3}$。由贝叶斯公式：$P(C_3|H_2)=\dfrac{P(H_2|C_3)P(C_3)}{P(H_2|C_3)P(C_3)+P(H_2|C_1)P(C_1)+P(H_2|C_2)P(C_2)}=\dfrac{1\cdot\frac{1}{3}}{1\cdot\frac{1}{3}+\frac{1}{2}\cdot\frac{1}{3}+0}=\dfrac{1/3}{1/2}=\dfrac{2}{3}$。即主持人开 2 号门后，车在 3 号门（换门目标）的概率为 $\dfrac{2}{3}$。注意"总是换门"的获胜率 $\dfrac{2}{3}$ 其实不依赖主持人的等概率规则（见解法一）。

scene_spec.steps[4]

高亮结果：换门获胜概率为 $\dfrac{2}{3}$，不换为 $\dfrac{1}{3}$

efficiency_tags[0]

贝叶斯分母三项的条带分解

efficiency_tags[1]

条件概率 $P(C_3|H_2)$ 的收缩动画

## eval-prob-001-s3

problem

三扇门中车的位置等概率，初选与车的位置独立。主持人知道车的位置，总从未选的门中打开一扇有羊的门，并总给出换门机会。求坚持初选和换至唯一剩余未开的门各自获车概率。

solution

车的位置（3 种）×参赛者初选（3 种）=9 种等可能情形。逐项枚举：参赛者初选=车门（3 种情形），换门必输；参赛者初选=山羊门（6 种情形），换门必赢。故换门获胜概率 $=\dfrac{6}{9}=\dfrac{2}{3}$。

answer

换门获胜概率为 $\dfrac{2}{3}$，不换为 $\dfrac{1}{3}$

scene_spec.objects[0]

9 种等可能情形的枚举表格

scene_spec.objects[1]

换门胜 6 格的计数高亮

scene_spec.steps[0]

呈现题干及适用条件：三扇门中车的位置等概率，初选与车的位置独立。主持人知道车的位置，总从未选的门中打开一扇有羊的门，并总给出换门机会。求坚持初选和换至唯一剩余未开的门各自获车概率。

scene_spec.steps[1]

依次呈现：9 种等可能情形的枚举表格

scene_spec.steps[2]

依次呈现：换门胜 6 格的计数高亮

scene_spec.steps[3]

核对完整证明：车的位置（3 种）×参赛者初选（3 种）=9 种等可能情形。逐项枚举：参赛者初选=车门（3 种情形），换门必输；参赛者初选=山羊门（6 种情形），换门必赢。故换门获胜概率 $=\dfrac{6}{9}=\dfrac{2}{3}$。

scene_spec.steps[4]

高亮结果：换门获胜概率为 $\dfrac{2}{3}$，不换为 $\dfrac{1}{3}$

efficiency_tags[0]

9 种等可能情形的枚举表格

efficiency_tags[1]

换门胜 6 格的计数高亮

## eval-prob-002-s1

problem

三个盒子：甲盒装 2 枚金币，乙盒装 2 枚银币，丙盒装 1 金 1 银。随机选一个盒子再从中随机摸出一枚硬币，发现是金币。问：该盒子中另一枚硬币也是金币的概率是多少？

solution

记 $A$=摸到金币，$B_1,B_2,B_3$=分别选中甲盒（双金）、乙盒（双银）、丙盒（一金一银）。$P(B_i)=\dfrac{1}{3}$，$P(A|B_1)=1$，$P(A|B_2)=0$，$P(A|B_3)=\dfrac{1}{2}$。$P(B_1|A)=\dfrac{P(A|B_1)P(B_1)}{P(A|B_1)P(B_1)+P(A|B_2)P(B_2)+P(A|B_3)P(B_3)}=\dfrac{1\cdot\frac{1}{3}}{1\cdot\frac{1}{3}+0\cdot\frac{1}{3}+\frac{1}{2}\cdot\frac{1}{3}}=\dfrac{1/3}{1/2}=\dfrac{2}{3}$。

answer

$\dfrac{2}{3}$

scene_spec.objects[0]

贝叶斯公式分子分母的条带分解

scene_spec.objects[1]

$P(A|B_i)$ 三值的标注

scene_spec.steps[0]

第一步：以贝叶斯公式为主线，建立概率论·条件概率场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：贝叶斯公式分子分母的条带分解。

scene_spec.steps[2]

第三步：$P(A|B_i)$ 三值的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

贝叶斯公式分子分母的条带分解

efficiency_tags[1]

$P(A|B_i)$ 三值的标注

## eval-prob-002-s2

problem

三个盒子：甲盒装 2 枚金币，乙盒装 2 枚银币，丙盒装 1 金 1 银。随机选一个盒子再从中随机摸出一枚硬币，发现是金币。问：该盒子中另一枚硬币也是金币的概率是多少？

solution

6 枚硬币等可能地被摸到。已知摸到的是金币，则它必是 3 枚金币之一，且 3 枚金币等可能。其中 2 枚来自甲盒（另一枚也是金），1 枚来自丙盒（另一枚是银）。故所求概率 $=\dfrac{2}{3}$。

answer

$\dfrac{2}{3}$

scene_spec.objects[0]

三盒六币的枚举展示

scene_spec.objects[1]

3 枚金币等可能的归一化动画

scene_spec.steps[0]

第一步：以枚举等可能样本点为主线，建立概率论·条件概率场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：三盒六币的枚举展示。

scene_spec.steps[2]

第三步：3 枚金币等可能的归一化动画。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

三盒六币的枚举展示

efficiency_tags[1]

3 枚金币等可能的归一化动画

## eval-prob-002-s3

problem

三个盒子：甲盒装 2 枚金币，乙盒装 2 枚银币，丙盒装 1 金 1 银。随机选一个盒子再从中随机摸出一枚硬币，发现是金币。问：该盒子中另一枚硬币也是金币的概率是多少？

solution

第一层：选盒，各 $\dfrac{1}{3}$；第二层：甲盒内摸到金概率 1（路径概率 $\dfrac{1}{3}$），丙盒内摸到金概率 $\dfrac{1}{2}$（路径概率 $\dfrac{1}{6}$），乙盒为 0。摸到金的总概率 $\dfrac{1}{3}+\dfrac{1}{6}=\dfrac{1}{2}$；其中来自甲盒的占比 $\dfrac{1/3}{1/2}=\dfrac{2}{3}$。

answer

$\dfrac{2}{3}$

scene_spec.objects[0]

三盒六币的树状图

scene_spec.objects[1]

银币分支熄灭、金币重新归一化

scene_spec.steps[0]

第一步：以树状图为主线，建立概率论·条件概率场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：三盒六币的树状图。

scene_spec.steps[2]

第三步：银币分支熄灭、金币重新归一化。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

三盒六币的树状图

efficiency_tags[1]

银币分支熄灭、金币重新归一化

## eval-prob-003-s1

problem

抛一枚均匀硬币直到出现正面为止，求抛掷次数的期望（几何分布期望）。

solution

设 $X\sim\operatorname{Geom}\!\left(\dfrac{1}{2}\right)$，$P(X=n)=q^{n-1}p=\left(\dfrac{1}{2}\right)^n$。$E[X]=\displaystyle\sum_{n=1}^{\infty}n\left(\dfrac{1}{2}\right)^n$。由 eval-calc-021 的错位相减（或幂级数 $\sum nx^{n-1}=\dfrac{1}{(1-x)^2}$ 取 $x=\dfrac{1}{2}$），得 $E[X]=\dfrac{1/2}{(1-1/2)^2}=2$。

answer

$2$

scene_spec.objects[0]

错位相减竖式逐行对齐

scene_spec.objects[1]

与级数 $\sum n/2^n$ 的同构对照

scene_spec.steps[0]

第一步：以级数求和为主线，建立概率论·常见分布场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：错位相减竖式逐行对齐。

scene_spec.steps[2]

第三步：与级数 $\sum n/2^n$ 的同构对照。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

错位相减竖式逐行对齐

efficiency_tags[1]

与级数 $\sum n/2^n$ 的同构对照

## eval-prob-003-s2

problem

抛一枚均匀硬币直到出现正面为止，求抛掷次数的期望（几何分布期望）。

solution

记 $E$ 为首次正面所需次数的期望。第一次若为正面（概率 $\dfrac{1}{2}$），总次数为 1；若为反面（概率 $\dfrac{1}{2}$），则"回到原点"，总次数为 $1+E$。故 $E=\dfrac{1}{2}\cdot 1+\dfrac{1}{2}\cdot(1+E)=1+\dfrac{E}{2}$，解得 $E=2$。递推中的期望有限：首次正面等待$X$满足$P(X>2k)=4^{-k}$，尾和公式给出$E[X]\le2\sum_{k=0}^{\infty}4^{-k}=8/3<\infty$，故可对递推式作有限数的移项，得到$E[X]=2$。

answer

$2$

scene_spec.objects[0]

抛硬币树状图与"回到原点"分支

scene_spec.objects[1]

期望自指方程 $E=1+\dfrac{E}{2}$ 的天平示意

scene_spec.steps[0]

呈现题干及适用条件：抛一枚均匀硬币直到出现正面为止，求抛掷次数的期望（几何分布期望）。

scene_spec.steps[1]

依次呈现：抛硬币树状图与"回到原点"分支

scene_spec.steps[2]

依次呈现：期望自指方程 $E=1+\dfrac{E}{2}$ 的天平示意

scene_spec.steps[3]

核对完整证明：记 $E$ 为首次正面所需次数的期望。第一次若为正面（概率 $\dfrac{1}{2}$），总次数为 1；若为反面（概率 $\dfrac{1}{2}$），则"回到原点"，总次数为 $1+E$。故 $E=\dfrac{1}{2}\cdot 1+\dfrac{1}{2}\cdot(1+E)=1+\dfrac{E}{2}$，解得 $E=2$。递推中的期望有限：首次正面等待$X$满足$P(X>2k)=4^{-k}$，尾和公式给出$E[X]\le2\sum_{k=0}^{\infty}4^{-k}=8/3<\infty$，故可对递推式作有限数的移项，得到$E[X]=2$。

scene_spec.steps[4]

高亮结果：$2$

efficiency_tags[0]

抛硬币树状图与"回到原点"分支

efficiency_tags[1]

期望自指方程 $E=1+\dfrac{E}{2}$ 的天平示意

## eval-prob-003-s3

problem

抛一枚均匀硬币直到出现正面为止，求抛掷次数的期望（几何分布期望）。

solution

概率母函数 $G(z)=E[z^X]=\displaystyle\sum_{n=1}^{\infty}z^nq^{n-1}p=\dfrac{pz}{1-qz}$。$G'(z)=\dfrac{p(1-qz)+pqz}{(1-qz)^2}=\dfrac{p}{(1-qz)^2}$，故 $E[X]=G'(1)=\dfrac{p}{(1-q)^2}=\dfrac{1}{p}=2$（$p=q=\dfrac{1}{2}$）。

answer

$2$

scene_spec.objects[0]

母函数 $G(z)=\dfrac{pz}{1-qz}$ 的曲线

scene_spec.objects[1]

$G'(1)$ 切线斜率的标注

scene_spec.steps[0]

第一步：以概率母函数为主线，建立概率论·常见分布场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：母函数 $G(z)=\dfrac{pz}{1-qz}$ 的曲线。

scene_spec.steps[2]

第三步：$G'(1)$ 切线斜率的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

母函数 $G(z)=\dfrac{pz}{1-qz}$ 的曲线

efficiency_tags[1]

$G'(1)$ 切线斜率的标注

## eval-prob-004-s1

problem

掷一枚均匀骰子两次，设 $X$ 为第一次点数，$Y$ 为两次点数之和。求 $P(Y\ge 8\mid X=3)$ 与 $E[Y\mid X=3]$。

solution

给定 $X=3$，第二次点数 $Z$ 在 $\{1,2,3,4,5,6\}$ 上等可能。$Y=3+Z\ge 8\iff Z\ge 5$，故 $P(Y\ge 8|X=3)=P(Z\in\{5,6\})=\dfrac{2}{6}=\dfrac{1}{3}$。$E[Y|X=3]=3+E[Z]=3+\dfrac{7}{2}=\dfrac{13}{2}$。

answer

$P(Y\ge 8\mid X=3)=\dfrac{1}{3}$；$E[Y\mid X=3]=\dfrac{13}{2}$

scene_spec.objects[0]

条件分布表（$Z\in\{1,\dots,6\}$ 等可能）

scene_spec.objects[1]

$Z\ge5$ 的两格高亮

scene_spec.steps[0]

第一步：以条件分布表为主线，建立概率论·条件分布场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：条件分布表（$Z\in\{1,\dots,6\}$ 等可能）。

scene_spec.steps[2]

第三步：$Z\ge5$ 的两格高亮。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

条件分布表（$Z\in\{1,\dots,6\}$ 等可能）

efficiency_tags[1]

$Z\ge5$ 的两格高亮

## eval-prob-004-s2

problem

掷一枚均匀骰子两次，设 $X$ 为第一次点数，$Y$ 为两次点数之和。求 $P(Y\ge 8\mid X=3)$ 与 $E[Y\mid X=3]$。

solution

$P(Y\ge 8|X=3)=\dfrac{P(X=3,Y\ge 8)}{P(X=3)}$。$P(X=3)=\dfrac{1}{6}$；事件 $\{X=3,Y\ge 8\}$ 即 $\{X=3,Z\ge 5\}$，由独立性 $P=\dfrac{1}{6}\cdot\dfrac{2}{6}=\dfrac{1}{18}$。故条件概率 $=\dfrac{1/18}{1/6}=\dfrac{1}{3}$。同理 $E[Y|X=3]=\dfrac{1}{P(X=3)}\displaystyle\sum_z(3+z)P(X=3)P(Z=z)=\sum_z(3+z)\cdot\dfrac{1}{6}=\dfrac{13}{2}$。

answer

$P(Y\ge 8\mid X=3)=\dfrac{1}{3}$；$E[Y\mid X=3]=\dfrac{13}{2}$

scene_spec.objects[0]

条件概率公式 $\dfrac{P(X=3,Y\ge8)}{P(X=3)}$ 的代入

scene_spec.objects[1]

独立性拆分的标注

scene_spec.steps[0]

第一步：以条件概率公式为主线，建立概率论·条件分布场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：条件概率公式 $\dfrac{P(X=3,Y\ge8)}{P(X=3)}$ 的代入。

scene_spec.steps[2]

第三步：独立性拆分的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

条件概率公式 $\dfrac{P(X=3,Y\ge8)}{P(X=3)}$ 的代入

efficiency_tags[1]

独立性拆分的标注

## eval-prob-004-s3

problem

掷一枚均匀骰子两次，设 $X$ 为第一次点数，$Y$ 为两次点数之和。求 $P(Y\ge 8\mid X=3)$ 与 $E[Y\mid X=3]$。

solution

第一层固定 $X=3$，第二层 $Z\in\{1,\dots,6\}$ 各 $\dfrac{1}{6}$。数出 $Z\ge 5$ 的分支两条，概率 $\dfrac{2}{6}$；所有分支的 $Y$ 值平均为 $\dfrac{4+5+6+7+8+9}{6}=\dfrac{39}{6}=\dfrac{13}{2}$。

answer

$P(Y\ge 8\mid X=3)=\dfrac{1}{3}$；$E[Y\mid X=3]=\dfrac{13}{2}$

scene_spec.objects[0]

两次掷骰的树状图

scene_spec.objects[1]

给定 $X=3$ 后第二层高亮与六值平均

scene_spec.steps[0]

第一步：以树状图为主线，建立概率论·条件分布场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：两次掷骰的树状图。

scene_spec.steps[2]

第三步：给定 $X=3$ 后第二层高亮与六值平均。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

两次掷骰的树状图

efficiency_tags[1]

给定 $X=3$ 后第二层高亮与六值平均

## eval-prob-005-s1

problem

设 $X\sim U(0,1)$（区间 $(0,1)$ 上的均匀分布），求 $Y=-\ln X$ 的分布。

solution

$F_Y(y)=P(Y\le y)=P(-\ln X\le y)=P(X\ge e^{-y})=1-e^{-y}$（$y>0$，用到 $X$ 的分布函数 $F_X(x)=x$ 于 $(0,1)$）。对 $y$ 求导：$f_Y(y)=e^{-y}$（$y>0$），即 $Y\sim\operatorname{Exp}(1)$。

answer

$Y\sim\operatorname{Exp}(1)$，密度 $f_Y(y)=e^{-y}$（$y>0$）

scene_spec.objects[0]

事件 $\{X\ge e^{-y}\}$ 的区间高亮

scene_spec.objects[1]

分布函数 $F_Y(y)=1-e^{-y}$ 的生成

scene_spec.steps[0]

第一步：以分布函数法为主线，建立概率论·随机变量函数的分布场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：事件 $\{X\ge e^{-y}\}$ 的区间高亮。

scene_spec.steps[2]

第三步：分布函数 $F_Y(y)=1-e^{-y}$ 的生成。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

事件 $\{X\ge e^{-y}\}$ 的区间高亮

efficiency_tags[1]

分布函数 $F_Y(y)=1-e^{-y}$ 的生成

## eval-prob-005-s2

problem

设 $X\sim U(0,1)$（区间 $(0,1)$ 上的均匀分布），求 $Y=-\ln X$ 的分布。

solution

$y=g(x)=-\ln x$ 在 $(0,1)$ 上严格递减，反函数 $x=h(y)=e^{-y}$（$y>0$），$|h'(y)|=e^{-y}$。由变换公式 $f_Y(y)=f_X(h(y))\cdot|h'(y)|=1\cdot e^{-y}=e^{-y}$（$y>0$）。

answer

$Y\sim\operatorname{Exp}(1)$，密度 $f_Y(y)=e^{-y}$（$y>0$）

scene_spec.objects[0]

$y=-\ln x$ 曲线与映射动画

scene_spec.objects[1]

反函数 $e^{-y}$ 与导数的密度变换

scene_spec.steps[0]

第一步：以密度变换公式为主线，建立概率论·随机变量函数的分布场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：$y=-\ln x$ 曲线与映射动画。

scene_spec.steps[2]

第三步：反函数 $e^{-y}$ 与导数的密度变换。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

$y=-\ln x$ 曲线与映射动画

efficiency_tags[1]

反函数 $e^{-y}$ 与导数的密度变换

## eval-prob-005-s3

problem

设 $X\sim U(0,1)$（区间 $(0,1)$ 上的均匀分布），求 $Y=-\ln X$ 的分布。

solution

指数分布 $\operatorname{Exp}(1)$ 的分布函数为 $F(y)=1-e^{-y}$，其反函数 $F^{-1}(u)=-\ln(1-u)$。由于 $1-X$ 与 $X$ 同分布，$-\ln X$ 与 $F^{-1}(X)$ 同分布，故 $Y\sim\operatorname{Exp}(1)$。这正是计算机生成指数随机数的标准方法（逆变换法）。

answer

$Y\sim\operatorname{Exp}(1)$，密度 $f_Y(y)=e^{-y}$（$y>0$）

scene_spec.objects[0]

均匀点列映射到正半轴

scene_spec.objects[1]

逆变换采样原理的示意

scene_spec.steps[0]

第一步：以逆变换采样原理为主线，建立概率论·随机变量函数的分布场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：均匀点列映射到正半轴。

scene_spec.steps[2]

第三步：逆变换采样原理的示意。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

均匀点列映射到正半轴

efficiency_tags[1]

逆变换采样原理的示意

## eval-prob-006-s1

problem

设 $X\sim\operatorname{Poisson}(\lambda)$，求 $E[X^2]$，并由此求 $\operatorname{Var}(X)$。

solution

$E[X^2]=\displaystyle\sum_{k=0}^{\infty}k^2\cdot\dfrac{\lambda^ke^{-\lambda}}{k!}=\sum_{k=0}^{\infty}\left[k(k-1)+k\right]\dfrac{\lambda^ke^{-\lambda}}{k!}=e^{-\lambda}\left[\lambda^2\sum_{k=2}^{\infty}\dfrac{\lambda^{k-2}}{(k-2)!}+\lambda\sum_{k=1}^{\infty}\dfrac{\lambda^{k-1}}{(k-1)!}\right]=e^{-\lambda}\left[\lambda^2e^{\lambda}+\lambda e^{\lambda}\right]=\lambda^2+\lambda$。故 $\operatorname{Var}(X)=E[X^2]-(E[X])^2=\lambda^2+\lambda-\lambda^2=\lambda$。

answer

$E[X^2]=\lambda^2+\lambda$，$\operatorname{Var}(X)=\lambda$

scene_spec.objects[0]

$k^2=k(k-1)+k$ 的拆项动画

scene_spec.objects[1]

两级数 $e^\lambda$ 求和的重整化

scene_spec.steps[0]

第一步：以定义级数求和为主线，建立概率论·数字特征场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：$k^2=k(k-1)+k$ 的拆项动画。

scene_spec.steps[2]

第三步：两级数 $e^\lambda$ 求和的重整化。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

$k^2=k(k-1)+k$ 的拆项动画

efficiency_tags[1]

两级数 $e^\lambda$ 求和的重整化

## eval-prob-006-s2

problem

设 $X\sim\operatorname{Poisson}(\lambda)$，求 $E[X^2]$，并由此求 $\operatorname{Var}(X)$。

solution

$E[X(X-1)]=\displaystyle\sum_{k=2}^{\infty}k(k-1)\dfrac{\lambda^ke^{-\lambda}}{k!}=e^{-\lambda}\lambda^2\sum_{k=2}^{\infty}\dfrac{\lambda^{k-2}}{(k-2)!}=\lambda^2$。故 $E[X^2]=E[X(X-1)]+E[X]=\lambda^2+\lambda$，$\operatorname{Var}(X)=\lambda$。

answer

$E[X^2]=\lambda^2+\lambda$，$\operatorname{Var}(X)=\lambda$

scene_spec.objects[0]

$E[X(X-1)]=\lambda^2$ 的阶乘矩重整化示意

scene_spec.objects[1]

泊松分布柱状图随 $\lambda$ 变化

scene_spec.steps[0]

第一步：以阶乘矩为主线，建立概率论·数字特征场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：$E[X(X-1)]=\lambda^2$ 的阶乘矩重整化示意。

scene_spec.steps[2]

第三步：泊松分布柱状图随 $\lambda$ 变化。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

$E[X(X-1)]=\lambda^2$ 的阶乘矩重整化示意

efficiency_tags[1]

泊松分布柱状图随 $\lambda$ 变化

## eval-prob-006-s3

problem

设 $X\sim\operatorname{Poisson}(\lambda)$，求 $E[X^2]$，并由此求 $\operatorname{Var}(X)$。

solution

$M(t)=E[e^{tX}]=e^{\lambda(e^t-1)}$。$M'(t)=M(t)\cdot\lambda e^t$，$M''(t)=M(t)\left[(\lambda e^t)^2+\lambda e^t\right]$。$E[X]=M'(0)=\lambda$，$E[X^2]=M''(0)=\lambda^2+\lambda$，$\operatorname{Var}(X)=M''(0)-[M'(0)]^2=\lambda$。

answer

$E[X^2]=\lambda^2+\lambda$，$\operatorname{Var}(X)=\lambda$

scene_spec.objects[0]

矩母函数 $M(t)=e^{\lambda(e^t-1)}$ 的曲线

scene_spec.objects[1]

二阶导 $M''(0)=\lambda^2+\lambda$ 的标注

scene_spec.steps[0]

第一步：以矩母函数为主线，建立概率论·数字特征场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：矩母函数 $M(t)=e^{\lambda(e^t-1)}$ 的曲线。

scene_spec.steps[2]

第三步：二阶导 $M''(0)=\lambda^2+\lambda$ 的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

矩母函数 $M(t)=e^{\lambda(e^t-1)}$ 的曲线

efficiency_tags[1]

二阶导 $M''(0)=\lambda^2+\lambda$ 的标注

## eval-prob-007-s1

problem

房间里随机聚集 30 个人（假设生日在一年 365 天中等可能且相互独立）。求至少有两人生日相同的概率。

solution

记 $A$ 为至少两人生日相同。共有 $365^{30}$ 个等可能的有序生日序列；互不相同的序列共有 $365\cdot364\cdots336=365!/335!$ 个。因此 $P(A^c)=\frac{365!}{335!\,365^{30}}$，从而 $P(A)=1-\frac{365!}{335!\,365^{30}}$。

answer

$1-\frac{365!}{335!\,365^{30}}$

scene_spec.objects[0]

对立事件乘积式 $\dfrac{365\cdot364\cdots336}{365^{30}}$ 的逐项生成

scene_spec.objects[1]

365 格生日占位动画

scene_spec.steps[0]

第一步：以对立事件为主线，建立概率论·经典概型场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：对立事件乘积式 $\dfrac{365\cdot364\cdots336}{365^{30}}$ 的逐项生成。

scene_spec.steps[2]

第三步：365 格生日占位动画。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

对立事件乘积式 $\dfrac{365\cdot364\cdots336}{365^{30}}$ 的逐项生成

efficiency_tags[1]

365 格生日占位动画

## eval-prob-007-s2

problem

房间里随机聚集 30 个人（假设生日在一年 365 天中等可能且相互独立）。求至少有两人生日相同的概率。

solution

令 $q_k$ 为前 $k$ 人生日互不相同的概率。$q_1=1$；在前 $k-1$ 人生日互异的条件下，第 $k$ 人须避开 $k-1$ 天，故 $q_k=q_{k-1}\frac{366-k}{365}$。递推得 $q_{30}=\prod_{k=2}^{30}\frac{366-k}{365}=\frac{365!}{335!\,365^{30}}$，所求概率为 $1-q_{30}$。

answer

$1-\frac{365!}{335!\,365^{30}}$

scene_spec.objects[0]

生日占位与递推乘积

scene_spec.steps[0]

令 $q_k$ 表示前 $k$ 人生日互不相同，$q_1=1$。

scene_spec.steps[1]

给定前 $k-1$ 人互异，第 $k$ 人可选 $366-k$ 天；显示 $q_k=q_{k-1}(366-k)/365$。

scene_spec.steps[2]

显示 $q_{30}=\prod_{k=2}^{30}(366-k)/365=365!/(335!\,365^{30})$。

scene_spec.steps[3]

最终概率为 $1-q_{30}$，保持阶乘和分数。

efficiency_tags[0]

$p_k$ 下降曲线与 $k=23$ 临界点

efficiency_tags[1]

递推式 $p_k=p_{k-1}\cdot\dfrac{366-k}{365}$ 的标注

## eval-prob-007-s3

problem

房间里随机聚集 30 个人（假设生日在一年 365 天中等可能且相互独立）。求至少有两人生日相同的概率。

solution

设 $N=\sum_{1\le i<j\le30}I_{ij}$，其中 $I_{ij}$ 表示第 $i,j$ 人生日相同。共有 $\binom{30}{2}=435$ 对，故 $E(N)=435/365=87/73$。不同的两对指标即使共用一人，也有联合概率 $1/365^2$；所以 $E(N^2)=435/365+435\cdot434/365^2$。由柯西不等式，$E(N)^2=E(N\mathbf1_{\{N>0\}})^2\le E(N^2)P(N>0)$，得 $P(N>0)\ge435/799>1/2$。这个下界不等于精确概率；精确值仍由补事件计数得到 $P(N>0)=1-\frac{365!}{335!\,365^{30}}$。

answer

$1-\frac{365!}{335!\,365^{30}}$

scene_spec.objects[0]

配对计数

scene_spec.objects[1]

精确二阶矩下界

scene_spec.objects[2]

补事件精确概率

scene_spec.steps[0]

定义 $N=\sum_{i<j}I_{ij}$，有 $435$ 对，$E(N)=435/365=87/73$。

scene_spec.steps[1]

不同两对联合成功概率为 $1/365^2$，包括共享一人的情况；显示 $E(N^2)=435/365+435\cdot434/365^2$。

scene_spec.steps[2]

由柯西不等式显示 $P(N>0)\ge E(N)^2/E(N^2)=435/799>1/2$。

scene_spec.steps[3]

区分下界和精确值；用生日互异的序列数得 $P(N>0)=1-365!/(335!\,365^{30})$。

efficiency_tags[0]

435 对配对的计数高亮

efficiency_tags[1]

期望 $\dfrac{87}{73}\approx1.19$ 的线性性标注

## eval-prob-008-s1

problem

设 $X\sim B\!\left(100,\dfrac{1}{2}\right)$。用切比雪夫不等式给出 $P(|X-50|\ge 10)$ 的上界，并与精确值比较。

solution

$E(X)=50$，$\operatorname{Var}(X)=100\cdot\frac12\cdot\frac12=25$。切比雪夫不等式给出 $q=P(|X-50|\ge10)\le25/10^2=1/4$。由于 $X$ 为整数且分布关于 $50$ 对称，$q=P(X\le40)+P(X\ge60)=2^{-99}\sum_{k=0}^{40}\binom{100}{k}$。令 $Y=(X-50)^2$。在该事件上 $Y\ge100$，且 $P(X=0)>0$ 时 $Y>100$，故 $25=E(Y)>100q$，即 $q<1/4$。这说明上界严格大于精确值。

answer

上界 $\frac14$；精确值 $q=2^{-99}\sum_{k=0}^{40}\binom{100}{k}<\frac14$。

scene_spec.objects[0]

切比雪夫不等式 $\dfrac{25}{100}=\dfrac{1}{4}$ 的代入

scene_spec.objects[1]

上界水平线标注

scene_spec.steps[0]

第一步：以切比雪夫不等式为主线，建立概率论·大数定律场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：切比雪夫不等式 $\dfrac{25}{100}=\dfrac{1}{4}$ 的代入。

scene_spec.steps[2]

第三步：上界水平线标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

切比雪夫不等式 $\dfrac{25}{100}=\dfrac{1}{4}$ 的代入

efficiency_tags[1]

上界水平线标注

## eval-prob-008-s2

problem

设 $X\sim B\!\left(100,\dfrac{1}{2}\right)$。用切比雪夫不等式给出 $P(|X-50|\ge 10)$ 的上界，并与精确值比较。

solution

将二项分布各项求和，利用 $\binom{100}{k}=\binom{100}{100-k}$，精确得到 $q=P(X\le40)+P(X\ge60)=\frac{2}{2^{100}}\sum_{k=0}^{40}\binom{100}{k}$。另一方面 $E(X)=50$，$\operatorname{Var}(X)=25$，故切比雪夫上界为 $1/4$。设 $S=\sum_{k=0}^{40}\binom{100}{k}$，则两者之差为 $\frac14-q=\frac{2^{97}-S}{2^{99}}$。由于 $E((X-50)^2)>100P(|X-50|\ge10)$（例如 $X=0$ 的正概率项给出严格性），该差严格为正。

answer

上界 $\frac14$；精确值 $\frac{1}{2^{99}}\sum_{k=0}^{40}\binom{100}{k}$，严格小于 $\frac14$。

scene_spec.objects[0]

二项分布柱状图与 $|X-50|<10$ 区间高亮

scene_spec.objects[1]

对称性 $P(X\ge60)=P(X\le40)$ 的尾部概率放大

scene_spec.steps[0]

第一步：以精确二项求和为主线，建立概率论·大数定律场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：二项分布柱状图与 $|X-50|<10$ 区间高亮。

scene_spec.steps[2]

第三步：对称性 $P(X\ge60)=P(X\le40)$ 的尾部概率放大。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

二项分布柱状图与 $|X-50|<10$ 区间高亮

efficiency_tags[1]

对称性 $P(X\ge60)=P(X\le40)$ 的尾部概率放大

## eval-prob-008-s3

problem

设 $X\sim B\!\left(100,\dfrac{1}{2}\right)$。用切比雪夫不等式给出 $P(|X-50|\ge 10)$ 的上界，并与精确值比较。

solution

记 $A=\{|X-50|\ge10\}$。由 $E((X-50)^2)=25$，有 $P(A)\le1/4$。精确概率为 $q=2^{-99}\sum_{k=0}^{40}\binom{100}{k}$。更细地，$25-100q=E(((X-50)^2-100)\mathbf1_A)+E((X-50)^2\mathbf1_{A^c})>0$；两项非负，第一项中 $X=0$ 的贡献严格为正。于是 $q<1/4$，且精确差值为 $\frac14-q=\frac{2^{97}-\sum_{k=0}^{40}\binom{100}{k}}{2^{99}}>0$。

answer

上界 $\frac14$；精确值 $q=2^{-99}\sum_{k=0}^{40}\binom{100}{k}$；差 $\frac14-q=\frac{2^{97}-\sum_{k=0}^{40}\binom{100}{k}}{2^{99}}>0$。

scene_spec.objects[0]

切比雪夫上界

scene_spec.objects[1]

精确尾概率和差值

scene_spec.steps[0]

显示 $E(X)=50$、$\operatorname{Var}(X)=25$，从而 $P(|X-50|\ge10)\le1/4$。

scene_spec.steps[1]

由对称性显示 $q=2^{-99}\sum_{k=0}^{40}\binom{100}{k}$。

scene_spec.steps[2]

显示精确差值 $1/4-q=(2^{97}-\sum_{k=0}^{40}\binom{100}{k})/2^{99}>0$。

scene_spec.steps[3]

严格性来自正概率的 $X=0$ 项使平方偏差严格大于阈值 $100$。

efficiency_tags[0]

切比雪夫上界 $\frac14$ 与精确尾概率 $q=2^{-99}\sum_{k=0}^{40}\binom{100}{k}$

efficiency_tags[1]

精确正差值 $\frac14-q=\frac{2^{97}-\sum_{k=0}^{40}\binom{100}{k}}{2^{99}}>0$

## eval-prob-009-s1

problem

设 $X,Y$ 相互独立且均服从 $\operatorname{Exp}(1)$，求 $Z=\min(X,Y)$ 的分布。

solution

$P(Z>z)=P(X>z,Y>z)=P(X>z)P(Y>z)=e^{-z}\cdot e^{-z}=e^{-2z}$（$z>0$，由独立性）。故 $F_Z(z)=1-e^{-2z}$，$f_Z(z)=2e^{-2z}$，即 $Z\sim\operatorname{Exp}(2)$。

answer

$Z\sim\operatorname{Exp}(2)$，密度 $f_Z(z)=2e^{-2z}$（$z>0$）

scene_spec.objects[0]

生存函数 $P(Z>z)=e^{-z}e^{-z}$ 的乘积动画

scene_spec.objects[1]

$\min>z$ 区域的收缩动画

scene_spec.steps[0]

第一步：以生存函数法为主线，建立概率论·多维随机变量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：生存函数 $P(Z>z)=e^{-z}e^{-z}$ 的乘积动画。

scene_spec.steps[2]

第三步：$\min>z$ 区域的收缩动画。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

生存函数 $P(Z>z)=e^{-z}e^{-z}$ 的乘积动画

efficiency_tags[1]

$\min>z$ 区域的收缩动画

## eval-prob-009-s2

problem

设 $X,Y$ 相互独立且均服从 $\operatorname{Exp}(1)$，求 $Z=\min(X,Y)$ 的分布。

solution

最小值的密度公式：$f_Z(z)=2f(z)[1-F(z)]$，其中 $f(z)=e^{-z}$、$F(z)=1-e^{-z}$ 为 $\operatorname{Exp}(1)$ 的密度与分布函数。故 $f_Z(z)=2e^{-z}\cdot e^{-z}=2e^{-2z}$。

answer

$Z\sim\operatorname{Exp}(2)$，密度 $f_Z(z)=2e^{-2z}$（$z>0$）

scene_spec.objects[0]

次序统计量公式 $2f(z)[1-F(z)]$ 的代入

scene_spec.objects[1]

密度 $2e^{-2z}$ 的生成

scene_spec.steps[0]

第一步：以次序统计量公式为主线，建立概率论·多维随机变量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：次序统计量公式 $2f(z)[1-F(z)]$ 的代入。

scene_spec.steps[2]

第三步：密度 $2e^{-2z}$ 的生成。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

次序统计量公式 $2f(z)[1-F(z)]$ 的代入

efficiency_tags[1]

密度 $2e^{-2z}$ 的生成

## eval-prob-009-s3

problem

设 $X,Y$ 相互独立且均服从 $\operatorname{Exp}(1)$，求 $Z=\min(X,Y)$ 的分布。

solution

联合密度 $f(x,y)=e^{-x-y}$（$x,y>0$）。$P(Z>z)=\displaystyle\int_z^\infty\!\!\int_z^\infty e^{-x-y}\,dx\,dy=\left(\int_z^\infty e^{-x}dx\right)\left(\int_z^\infty e^{-y}dy\right)=e^{-z}\cdot e^{-z}=e^{-2z}$，与解法一一致。

answer

$Z\sim\operatorname{Exp}(2)$，密度 $f_Z(z)=2e^{-2z}$（$z>0$）

scene_spec.objects[0]

联合密度曲面与方形区域

scene_spec.objects[1]

二重积分 $\int_z^\infty\int_z^\infty e^{-x-y}dxdy$ 的分解

scene_spec.steps[0]

第一步：以几何积分为主线，建立概率论·多维随机变量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：联合密度曲面与方形区域。

scene_spec.steps[2]

第三步：二重积分 $\int_z^\infty\int_z^\infty e^{-x-y}dxdy$ 的分解。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

联合密度曲面与方形区域

efficiency_tags[1]

二重积分 $\int_z^\infty\int_z^\infty e^{-x-y}dxdy$ 的分解

## eval-prob-010-s1

problem

$n$ 个人各带一顶帽子，帽子随机打乱后每人随机取回一顶（全排列等可能）。求取到自己帽子的人数的期望，并说明该期望不依赖 $n$ 的原因。

solution

设 $I_i$ 为"第 $i$ 人取到自己帽子"的指示变量。由对称性，第 $i$ 人取到自己帽子的概率 $P(I_i=1)=\dfrac{1}{n}$（$n$ 顶帽子中恰有一顶属于他，均匀排列下等可能）。总正确人数 $X=I_1+\cdots+I_n$，由期望线性性（**不要求独立性**）：$E[X]=\displaystyle\sum_{i=1}^{n}E[I_i]=\sum_{i=1}^{n}P(I_i=1)=n\cdot\dfrac{1}{n}=1$。

answer

$1$（与 $n$ 无关）

scene_spec.objects[0]

指示变量 $I_i$ 的高亮

scene_spec.objects[1]

期望线性性 $n\cdot\dfrac{1}{n}=1$ 的标注

scene_spec.steps[0]

第一步：以指示变量+期望线性性为主线，建立概率论·期望场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：指示变量 $I_i$ 的高亮。

scene_spec.steps[2]

第三步：期望线性性 $n\cdot\dfrac{1}{n}=1$ 的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

指示变量 $I_i$ 的高亮

efficiency_tags[1]

期望线性性 $n\cdot\dfrac{1}{n}=1$ 的标注

## eval-prob-010-s2

problem

$n$ 个人各带一顶帽子，帽子随机打乱后每人随机取回一顶（全排列等可能）。求取到自己帽子的人数的期望，并说明该期望不依赖 $n$ 的原因。

solution

恰有 $k$ 人取对的概率 $P(X=k)=\dfrac{\binom{n}{k}D(n-k)}{n!}$，其中 $D(m)=m!\displaystyle\sum_{j=0}^{m}\dfrac{(-1)^j}{j!}$ 为错排数。生成函数 $G(z)=\displaystyle\sum_{k=0}^{n}\dfrac{\binom{n}{k}D(n-k)}{n!}z^k$。$E[X]=G'(1)=\dfrac{1}{n!}\displaystyle\sum_{k=1}^{n}k\binom{n}{k}D(n-k)=\dfrac{n}{n!}\sum_{k=1}^{n}\binom{n-1}{k-1}D(n-k)=\dfrac{1}{(n-1)!}\sum_{j=0}^{n-1}\binom{n-1}{j}D(n-1-j)$。而 $\displaystyle\sum_{j=0}^{n-1}\binom{n-1}{j}D(n-1-j)=(n-1)!$（对 $n-1$ 个元素的所有排列按"不动点个数 $j$"分类计数），故 $E[X]=1$。

answer

$1$（与 $n$ 无关）

scene_spec.objects[0]

固定点人数 $X$ 的分布柱状图 $P(X=k)=\binom{n}{k}D(n-k)/n!$

scene_spec.objects[1]

错排数 $D(m)$ 与生成函数 $G(z)=\sum_{k=0}^{n}P(X=k)z^k$

scene_spec.objects[2]

导数求和 $G^{\prime}(1)=\sum_{k=1}^{n}kP(X=k)$

scene_spec.objects[3]

按固定点个数分类的 $n-1$ 元素排列示意

scene_spec.steps[0]

固定 $n$，按 $k$ 展示分布柱状图与组合表达式。

scene_spec.steps[1]

写出生成函数 $G(z)$ 并逐项求导得 $G^{\prime}(1)$ 的求和式。

scene_spec.steps[2]

用 $k\binom{n}{k}=n\binom{n-1}{k-1}$ 把求和化为按固定点分类计数。

scene_spec.steps[3]

由 $\sum_j\binom{n-1}{j}D(n-1-j)=(n-1)!$ 得 $E[X]=1$

efficiency_tags[0]

分布柱状图 $P(X=k)=\binom{n}{k}D(n-k)/n!$

efficiency_tags[1]

生成函数 $G(z)$ 与导数求和 $G'(1)$

efficiency_tags[2]

按固定点个数分类的 $n-1$ 元素排列示意

## eval-prob-010-s3

problem

$n$ 个人各带一顶帽子，帽子随机打乱后每人随机取回一顶（全排列等可能）。求取到自己帽子的人数的期望，并说明该期望不依赖 $n$ 的原因。

solution

对全部 $n!$ 种排列统计"拿对帽子"的总人次：对任意固定的第 $i$ 人，其帽子被自己拿到的排列数为 $(n-1)!$（其余 $n-1$ 顶帽子任意排列），故总固定点数 $=\displaystyle\sum_{i=1}^{n}(n-1)!=n\cdot(n-1)!=n!$。除以排列总数 $n!$，得期望 $=\dfrac{n!}{n!}=1$。期望不随 $n$ 变化的本质是"每顶帽子命中率恒为 $\dfrac{1}{n}$、恰好 $n$ 顶"。

answer

$1$（与 $n$ 无关）

scene_spec.objects[0]

$n$ 人帽子随机交换动画

scene_spec.objects[1]

总固定点数 $n!$ 的双重计数示意

scene_spec.steps[0]

第一步：以双重计数为主线，建立概率论·期望场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：$n$ 人帽子随机交换动画。

scene_spec.steps[2]

第三步：总固定点数 $n!$ 的双重计数示意。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

$n$ 人帽子随机交换动画

efficiency_tags[1]

总固定点数 $n!$ 的双重计数示意

## eval-prob-011-s1

problem

抛均匀硬币直到连续出现两次正面（HH）为止，求所需抛掷次数的期望。

solution

设 $E_0$=当前无连续正面记录时的期望剩余次数，$E_1$=刚出现一次正面时的期望剩余次数。状态转移：$E_0=1+\dfrac{1}{2}E_0+\dfrac{1}{2}E_1$（抛一次后：反面回 $E_0$，正面进 $E_1$）；$E_1=1+\dfrac{1}{2}\cdot 0+\dfrac{1}{2}E_0$（再抛：正面完成，反面回 $E_0$）。由第二式 $E_1=1+\dfrac{E_0}{2}$，代入第一式：$E_0=1+\dfrac{E_0}{2}+\dfrac{1}{2}\left(1+\dfrac{E_0}{2}\right)=\dfrac{3}{2}+\dfrac{3E_0}{4}$，解得 $E_0=6$。有限性：把抛掷分成互不重叠的两次一块，每块为HH的概率$1/4$，各块独立。因此首次连续HH时间$T$满足$P(T>2k)\le(3/4)^k$，尾和公式给出$E[T]\le2\sum_{k=0}^{\infty}(3/4)^k=8<\infty$。吸收概率为1，期望有限，所以递推及基本矩阵的期望运算有效。

answer

$6$

scene_spec.objects[0]

状态递推方程 $E_0=1+\dfrac12E_0+\dfrac12E_1$ 的平衡示意

scene_spec.objects[1]

代入求解 $E_0=6$ 的动画

scene_spec.steps[0]

呈现题干及适用条件：抛均匀硬币直到连续出现两次正面（HH）为止，求所需抛掷次数的期望。

scene_spec.steps[1]

依次呈现：状态递推方程 $E_0=1+\dfrac12E_0+\dfrac12E_1$ 的平衡示意

scene_spec.steps[2]

依次呈现：代入求解 $E_0=6$ 的动画

scene_spec.steps[3]

核对完整证明：设 $E_0$=当前无连续正面记录时的期望剩余次数，$E_1$=刚出现一次正面时的期望剩余次数。状态转移：$E_0=1+\dfrac{1}{2}E_0+\dfrac{1}{2}E_1$（抛一次后：反面回 $E_0$，正面进 $E_1$）；$E_1=1+\dfrac{1}{2}\cdot 0+\dfrac{1}{2}E_0$（再抛：正面完成，反面回 $E_0$）。由第二式 $E_1=1+\dfrac{E_0}{2}$，代入第一式：$E_0=1+\dfrac{E_0}{2}+\dfrac{1}{2}\left(1+\dfrac{E_0}{2}\right)=\dfrac{3}{2}+\dfrac{3E_0}{4}$，解得 $E_0=6$。有限性：把抛掷分成互不重叠的两次一块，每块为HH的概率$1/4$，各块独立。因此首次连续HH时间$T$满足$P(T>2k)\le(3/4)^k$，尾和公式给出$E[T]\le2\sum_{k=0}^{\infty}(3/4)^k=8<\infty$。吸收概率为1，期望有限，所以递推及基本矩阵的期望运算有效。

scene_spec.steps[4]

高亮结果：$6$

efficiency_tags[0]

状态递推方程 $E_0=1+\dfrac12E_0+\dfrac12E_1$ 的平衡示意

efficiency_tags[1]

代入求解 $E_0=6$ 的动画

## eval-prob-011-s2

problem

抛均匀硬币直到连续出现两次正面（HH）为止，求所需抛掷次数的期望。

solution

状态 $\{0,1,H\}$（$H$ 为吸收态），转移矩阵 $P=\begin{pmatrix}1/2&1/2&0\\1/2&0&1/2\\0&0&1\end{pmatrix}$，瞬态子矩阵 $Q=\begin{pmatrix}1/2&1/2\\1/2&0\end{pmatrix}$。基本矩阵 $N=(I-Q)^{-1}=\begin{pmatrix}1/2&-1/2\\-1/2&1\end{pmatrix}^{-1}=4\begin{pmatrix}1&1/2\\1/2&1/2\end{pmatrix}=\begin{pmatrix}4&2\\2&2\end{pmatrix}$（$\det(I-Q)=\dfrac{1}{2}-\dfrac{1}{4}=\dfrac{1}{4}$）。从状态 0 出发的期望步数为 $N$ 第 1 行之和 $=4+2=6$。有限性：把抛掷分成互不重叠的两次一块，每块为HH的概率$1/4$，各块独立。因此首次连续HH时间$T$满足$P(T>2k)\le(3/4)^k$，尾和公式给出$E[T]\le2\sum_{k=0}^{\infty}(3/4)^k=8<\infty$。吸收概率为1，期望有限，所以递推及基本矩阵的期望运算有效。

answer

$6$

scene_spec.objects[0]

三状态转移图与概率箭头

scene_spec.objects[1]

基本矩阵 $N=(I-Q)^{-1}=\begin{pmatrix}4&2\\2&2\end{pmatrix}$ 的计算标注

scene_spec.steps[0]

呈现题干及适用条件：抛均匀硬币直到连续出现两次正面（HH）为止，求所需抛掷次数的期望。

scene_spec.steps[1]

依次呈现：三状态转移图与概率箭头

scene_spec.steps[2]

依次呈现：基本矩阵 $N=(I-Q)^{-1}=\begin{pmatrix}4&2\\2&2\end{pmatrix}$ 的计算标注

scene_spec.steps[3]

核对完整证明：状态 $\{0,1,H\}$（$H$ 为吸收态），转移矩阵 $P=\begin{pmatrix}1/2&1/2&0\\1/2&0&1/2\\0&0&1\end{pmatrix}$，瞬态子矩阵 $Q=\begin{pmatrix}1/2&1/2\\1/2&0\end{pmatrix}$。基本矩阵 $N=(I-Q)^{-1}=\begin{pmatrix}1/2&-1/2\\-1/2&1\end{pmatrix}^{-1}=4\begin{pmatrix}1&1/2\\1/2&1/2\end{pmatrix}=\begin{pmatrix}4&2\\2&2\end{pmatrix}$（$\det(I-Q)=\dfrac{1}{2}-\dfrac{1}{4}=\dfrac{1}{4}$）。从状态 0 出发的期望步数为 $N$ 第 1 行之和 $=4+2=6$。有限性：把抛掷分成互不重叠的两次一块，每块为HH的概率$1/4$，各块独立。因此首次连续HH时间$T$满足$P(T>2k)\le(3/4)^k$，尾和公式给出$E[T]\le2\sum_{k=0}^{\infty}(3/4)^k=8<\infty$。吸收概率为1，期望有限，所以递推及基本矩阵的期望运算有效。

scene_spec.steps[4]

高亮结果：$6$

efficiency_tags[0]

三状态转移图与概率箭头

efficiency_tags[1]

基本矩阵 $N=(I-Q)^{-1}=\begin{pmatrix}4&2\\2&2\end{pmatrix}$ 的计算标注

## eval-prob-011-s3

problem

抛均匀硬币直到连续出现两次正面（HH）为止，求所需抛掷次数的期望。

solution

首次出现 HH 的时刻 $T\ge 2$，其分布为 $P(T=k)=\dfrac{F_{k-1}}{2^k}$（$k\ge 2$），其中 $F_1=F_2=1$ 为斐波那契数（$k$ 次抛掷中前 $k-1$ 次无 HH 且第 $k$ 次前恰为 $\dots H$ 的计数即斐波那契递推）。概率母函数 $G(z)=\displaystyle\sum_{k=2}^{\infty}\dfrac{F_{k-1}}{2^k}z^k=\dfrac{z^2}{4-2z-z^2}$（由 $\sum_{m\ge 1}F_mx^m=\dfrac{x}{1-x-x^2}$ 代入 $x=\dfrac{z}{2}$ 得）。$E[T]=G'(1)=\left.\dfrac{2z(4-2z-z^2)+z^2(2+2z)}{(4-2z-z^2)^2}\right|_{z=1}=\dfrac{2\cdot 1+4}{1}=6$。

answer

$6$

scene_spec.objects[0]

斐波那契计数 $P(T=k)=\dfrac{F_{k-1}}{2^k}$ 的生成

scene_spec.objects[1]

母函数 $G'(1)=6$ 的求导标注

scene_spec.steps[0]

第一步：以首达分布与生成函数为主线，建立概率论·随机过程场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：斐波那契计数 $P(T=k)=\dfrac{F_{k-1}}{2^k}$ 的生成。

scene_spec.steps[2]

第三步：母函数 $G'(1)=6$ 的求导标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

斐波那契计数 $P(T=k)=\dfrac{F_{k-1}}{2^k}$ 的生成

efficiency_tags[1]

母函数 $G'(1)=6$ 的求导标注

## eval-prob-012-s1

problem

设 $X,Y$ 相互独立且均服从 $U(0,1)$，求 $P(X+Y\le 1)$。

solution

$(X,Y)$ 在单位正方形 $[0,1]^2$ 上均匀分布。事件 $\{X+Y\le 1\}$ 对应正方形中直线 $x+y=1$ 左下方的等腰直角三角形，面积 $\dfrac{1}{2}\cdot 1\cdot 1=\dfrac{1}{2}$。均匀分布下概率=面积比，故 $P=\dfrac{1}{2}$。

answer

$\dfrac{1}{2}$

scene_spec.objects[0]

单位正方形与分割直线 $x+y=1$

scene_spec.objects[1]

三角形面积 $\dfrac{1}{2}$ 的高亮

scene_spec.steps[0]

第一步：以几何面积为主线，建立概率论·多维随机变量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：单位正方形与分割直线 $x+y=1$。

scene_spec.steps[2]

第三步：三角形面积 $\dfrac{1}{2}$ 的高亮。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

单位正方形与分割直线 $x+y=1$

efficiency_tags[1]

三角形面积 $\dfrac{1}{2}$ 的高亮

## eval-prob-012-s2

problem

设 $X,Y$ 相互独立且均服从 $U(0,1)$，求 $P(X+Y\le 1)$。

solution

$Z=X+Y$ 的密度为卷积：$f_Z(z)=\displaystyle\int_{-\infty}^{\infty}f_X(x)f_Y(z-x)dx=\int_0^1\mathbf 1_{[0,1]}(z-x)dx$。当 $0<z<1$：$f_Z(z)=\displaystyle\int_0^z dx=z$；当 $1<z<2$：$f_Z(z)=\displaystyle\int_{z-1}^1 dx=2-z$（三角分布）。故 $P(X+Y\le 1)=\displaystyle\int_0^1 z\,dz=\dfrac{1}{2}$。

answer

$\dfrac{1}{2}$

scene_spec.objects[0]

卷积滑动的矩形面积

scene_spec.objects[1]

三角密度 $f_Z(z)=z$、$2-z$ 的生成

scene_spec.steps[0]

第一步：以卷积密度为主线，建立概率论·多维随机变量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：卷积滑动的矩形面积。

scene_spec.steps[2]

第三步：三角密度 $f_Z(z)=z$、$2-z$ 的生成。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

卷积滑动的矩形面积

efficiency_tags[1]

三角密度 $f_Z(z)=z$、$2-z$ 的生成

## eval-prob-012-s3

problem

设 $X,Y$ 相互独立且均服从 $U(0,1)$，求 $P(X+Y\le 1)$。

solution

$(X,Y)$ 与 $(1-X,1-Y)$ 同分布。$X+Y\le 1\iff (1-X)+(1-Y)\ge 1$，且 $P(X+Y=1)=0$。故 $P(X+Y\le 1)=P(X+Y\ge 1)=\dfrac{1}{2}$（两事件覆盖全空间且交集为零概率边界且等概率）。

answer

$\dfrac{1}{2}$

scene_spec.objects[0]

对称性 $(X,Y)\sim(1-X,1-Y)$ 的镜像动画

scene_spec.objects[1]

两侧事件等概率且交集边界概率为零的标注

scene_spec.steps[0]

呈现题干及适用条件：设 $X,Y$ 相互独立且均服从 $U(0,1)$，求 $P(X+Y\le 1)$。

scene_spec.steps[1]

依次呈现：对称性 $(X,Y)\sim(1-X,1-Y)$ 的镜像动画

scene_spec.steps[2]

依次呈现：两侧事件等概率且交集边界概率为零的标注

scene_spec.steps[3]

核对完整证明：$(X,Y)$ 与 $(1-X,1-Y)$ 同分布。$X+Y\le 1\iff (1-X)+(1-Y)\ge 1$，且 $P(X+Y=1)=0$。故 $P(X+Y\le 1)=P(X+Y\ge 1)=\dfrac{1}{2}$（两事件覆盖全空间且交集为零概率边界且等概率）。

scene_spec.steps[4]

高亮结果：$\dfrac{1}{2}$

efficiency_tags[0]

对称性 $(X,Y)\sim(1-X,1-Y)$ 的镜像动画

efficiency_tags[1]

两侧事件等概率且交集边界概率为零的标注

## eval-prob-013-s1

problem

设 $X\sim N(0,1)$（标准正态分布），求 $E|X|$。

solution

$E|X|=\displaystyle\int_{-\infty}^{\infty}|x|\dfrac{1}{\sqrt{2\pi}}e^{-x^2/2}dx=\dfrac{2}{\sqrt{2\pi}}\int_0^{\infty}xe^{-x^2/2}dx$。令 $u=\dfrac{x^2}{2}$（$du=x\,dx$）：$=\dfrac{2}{\sqrt{2\pi}}\displaystyle\int_0^{\infty}e^{-u}du=\dfrac{2}{\sqrt{2\pi}}\cdot 1=\sqrt{\dfrac{2}{\pi}}$。

answer

$\sqrt{\dfrac{2}{\pi}}$

scene_spec.objects[0]

偶函数积分 $\dfrac{2}{\sqrt{2\pi}}\int_0^\infty xe^{-x^2/2}dx$ 的分解

scene_spec.objects[1]

换元 $u=\dfrac{x^2}{2}$ 的标注

scene_spec.steps[0]

第一步：以直接积分为主线，建立概率论·常见分布场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：偶函数积分 $\dfrac{2}{\sqrt{2\pi}}\int_0^\infty xe^{-x^2/2}dx$ 的分解。

scene_spec.steps[2]

第三步：换元 $u=\dfrac{x^2}{2}$ 的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

偶函数积分 $\dfrac{2}{\sqrt{2\pi}}\int_0^\infty xe^{-x^2/2}dx$ 的分解

efficiency_tags[1]

换元 $u=\dfrac{x^2}{2}$ 的标注

## eval-prob-013-s2

problem

设 $X\sim N(0,1)$（标准正态分布），求 $E|X|$。

solution

$|X|$ 服从半正态分布，密度 $f(y)=\dfrac{2}{\sqrt{2\pi}}e^{-y^2/2}$（$y>0$，即把负半轴密度折叠到正半轴）。$E|X|=\displaystyle\int_0^\infty y\dfrac{2}{\sqrt{2\pi}}e^{-y^2/2}dy=\dfrac{2}{\sqrt{2\pi}}\left[-e^{-y^2/2}\right]_0^\infty=\dfrac{2}{\sqrt{2\pi}}=\sqrt{\dfrac{2}{\pi}}$。

answer

$\sqrt{\dfrac{2}{\pi}}$

scene_spec.objects[0]

正态密度负半轴折叠成半正态的动画

scene_spec.objects[1]

折叠后积分 $\dfrac{2}{\sqrt{2\pi}}$ 的标注

scene_spec.steps[0]

第一步：以半正态分布为主线，建立概率论·常见分布场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：正态密度负半轴折叠成半正态的动画。

scene_spec.steps[2]

第三步：折叠后积分 $\dfrac{2}{\sqrt{2\pi}}$ 的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

正态密度负半轴折叠成半正态的动画

efficiency_tags[1]

折叠后积分 $\dfrac{2}{\sqrt{2\pi}}$ 的标注

## eval-prob-013-s3

problem

设 $X\sim N(0,1)$（标准正态分布），求 $E|X|$。

solution

$Y=X^2\sim\chi^2(1)$，密度 $f_Y(y)=\dfrac{1}{\sqrt{2\pi}}y^{-1/2}e^{-y/2}$（$y>0$）。$E|X|=E[\sqrt{Y}]=\displaystyle\int_0^\infty\sqrt{y}\cdot\dfrac{1}{\sqrt{2\pi}}y^{-1/2}e^{-y/2}dy=\dfrac{1}{\sqrt{2\pi}}\int_0^\infty e^{-y/2}dy=\dfrac{1}{\sqrt{2\pi}}\cdot 2=\sqrt{\dfrac{2}{\pi}}$。

answer

$\sqrt{\dfrac{2}{\pi}}$

scene_spec.objects[0]

$\chi^2(1)$ 密度 $\dfrac{1}{\sqrt{2\pi}}y^{-1/2}e^{-y/2}$ 的曲线

scene_spec.objects[1]

$E[\sqrt{Y}]$ 的积分过程

scene_spec.steps[0]

第一步：以$\chi^2$ 分布观点为主线，建立概率论·常见分布场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：$\chi^2(1)$ 密度 $\dfrac{1}{\sqrt{2\pi}}y^{-1/2}e^{-y/2}$ 的曲线。

scene_spec.steps[2]

第三步：$E[\sqrt{Y}]$ 的积分过程。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

$\chi^2(1)$ 密度 $\dfrac{1}{\sqrt{2\pi}}y^{-1/2}e^{-y/2}$ 的曲线

efficiency_tags[1]

$E[\sqrt{Y}]$ 的积分过程

## eval-prob-014-s1

problem

设 $X\sim\operatorname{Exp}(\lambda)$（$\lambda>0$）。证明无记忆性 $P(X>s+t\mid X>s)=P(X>t)$（$s,t>0$），并说明其含义。

solution

$P(X>s+t\mid X>s)=\dfrac{P(X>s+t)}{P(X>s)}=\dfrac{e^{-\lambda(s+t)}}{e^{-\lambda s}}=e^{-\lambda t}=P(X>t)$。即条件后剩余寿命的分布与全新时完全相同。

answer

证毕；无记忆性成立且是指数分布的特征性质

scene_spec.objects[0]

生存函数比值 $\dfrac{e^{-\lambda(s+t)}}{e^{-\lambda s}}$ 的相消动画

scene_spec.objects[1]

自相似右移的标注

scene_spec.steps[0]

第一步：以直接计算为主线，建立概率论·常见分布场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：生存函数比值 $\dfrac{e^{-\lambda(s+t)}}{e^{-\lambda s}}$ 的相消动画。

scene_spec.steps[2]

第三步：自相似右移的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

生存函数比值 $\dfrac{e^{-\lambda(s+t)}}{e^{-\lambda s}}$ 的相消动画

efficiency_tags[1]

自相似右移的标注

## eval-prob-014-s2

problem

设 $X\sim\operatorname{Exp}(\lambda)$（$\lambda>0$）。证明无记忆性 $P(X>s+t\mid X>s)=P(X>t)$（$s,t>0$），并说明其含义。

solution

危险率函数 $h(t)=\dfrac{f(t)}{1-F(t)}=\dfrac{\lambda e^{-\lambda t}}{e^{-\lambda t}}=\lambda$ 为常数。常数危险率意味着"每时每刻的瞬时失效倾向不随年龄变化"，这正是无记忆性的微分刻画；反之，若某分布危险率为常数 $\lambda$，解微分方程 $\dfrac{F'}{1-F}=\lambda$ 得 $F(t)=1-e^{-\lambda t}$，故常数危险率⇔指数分布。上述常危险率刻画限定于非负、绝对连续且$F(0)=0$、生存函数正的分布。令$S=1-F$，则$S^{\prime}=-\lambda S$、$S(0)=1$，故$S(t)=e^{-\lambda t}$。所以$P(X>s+t\mid X>s)=S(s+t)/S(s)=e^{-\lambda t}=P(X>t)$，完成无记忆性证明。

answer

证毕；无记忆性成立且是指数分布的特征性质

scene_spec.objects[0]

危险率常数 $h(t)=\lambda$ 的水平线

scene_spec.objects[1]

微分方程 $\dfrac{F'}{1-F}=\lambda$ 的求解

scene_spec.steps[0]

呈现题干及适用条件：设 $X\sim\operatorname{Exp}(\lambda)$（$\lambda>0$）。证明无记忆性 $P(X>s+t\mid X>s)=P(X>t)$（$s,t>0$），并说明其含义。

scene_spec.steps[1]

依次呈现：危险率常数 $h(t)=\lambda$ 的水平线

scene_spec.steps[2]

依次呈现：微分方程 $\dfrac{F'}{1-F}=\lambda$ 的求解

scene_spec.steps[3]

核对完整证明：危险率函数 $h(t)=\dfrac{f(t)}{1-F(t)}=\dfrac{\lambda e^{-\lambda t}}{e^{-\lambda t}}=\lambda$ 为常数。常数危险率意味着"每时每刻的瞬时失效倾向不随年龄变化"，这正是无记忆性的微分刻画；反之，若某分布危险率为常数 $\lambda$，解微分方程 $\dfrac{F'}{1-F}=\lambda$ 得 $F(t)=1-e^{-\lambda t}$，故常数危险率⇔指数分布。上述常危险率刻画限定于非负、绝对连续且$F(0)=0$、生存函数正的分布。令$S=1-F$，则$S^{\prime}=-\lambda S$、$S(0)=1$，故$S(t)=e^{-\lambda t}$。所以$P(X>s+t\mid X>s)=S(s+t)/S(s)=e^{-\lambda t}=P(X>t)$，完成无记忆性证明。

scene_spec.steps[4]

高亮结果：证毕；无记忆性成立且是指数分布的特征性质

efficiency_tags[0]

危险率常数 $h(t)=\lambda$ 的水平线

efficiency_tags[1]

微分方程 $\dfrac{F'}{1-F}=\lambda$ 的求解

## eval-prob-014-s3

problem

设 $X\sim\operatorname{Exp}(\lambda)$（$\lambda>0$）。证明无记忆性 $P(X>s+t\mid X>s)=P(X>t)$（$s,t>0$），并说明其含义。

solution

在强度 $\lambda$ 的泊松过程中，相邻事件的时间间隔服从 $\operatorname{Exp}(\lambda)$。已等待 $s$ 而无事件发生，意味着 $(0,s]$ 内的事件数 $N(s)=0$；由泊松过程的独立增量性，$(s,s+t]$ 内的事件数与 $(0,s]$ 内无关，$P(N(s,s+t)=0\mid N(s)=0)=P(N(s,s+t)=0)=e^{-\lambda t}$。故剩余等待时间仍服从 $\operatorname{Exp}(\lambda)$。

answer

证毕；无记忆性成立且是指数分布的特征性质

scene_spec.objects[0]

泊松过程时间轴上的间隔

scene_spec.objects[1]

独立增量性 $P(N(s,s+t)=0|N(s)=0)$ 的标注

scene_spec.steps[0]

第一步：以泊松过程视角为主线，建立概率论·常见分布场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：泊松过程时间轴上的间隔。

scene_spec.steps[2]

第三步：独立增量性 $P(N(s,s+t)=0|N(s)=0)$ 的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

泊松过程时间轴上的间隔

efficiency_tags[1]

独立增量性 $P(N(s,s+t)=0|N(s)=0)$ 的标注

## eval-prob-015-s1

problem

掷一枚均匀骰子，设 $X$ 为点数。求 $E[X]$ 与 $\operatorname{Var}(X)$。

solution

$E[X]=\dfrac{1+2+3+4+5+6}{6}=\dfrac{21}{6}=\dfrac{7}{2}$。$E[X^2]=\dfrac{1+4+9+16+25+36}{6}=\dfrac{91}{6}$。$\operatorname{Var}(X)=E[X^2]-(E[X])^2=\dfrac{91}{6}-\dfrac{49}{4}=\dfrac{182-147}{12}=\dfrac{35}{12}$。

answer

$E[X]=\dfrac{7}{2}$，$\operatorname{Var}(X)=\dfrac{35}{12}$

scene_spec.objects[0]

均匀柱状图与重心 $\dfrac72$

scene_spec.objects[1]

$E[X^2]=\dfrac{91}{6}$ 的逐格求和

scene_spec.steps[0]

呈现题干及适用条件：掷一枚均匀骰子，设 $X$ 为点数。求 $E[X]$ 与 $\operatorname{Var}(X)$。

scene_spec.steps[1]

依次呈现：均匀柱状图与重心 $\dfrac72$

scene_spec.steps[2]

依次呈现：$E[X^2]=\dfrac{91}{6}$ 的逐格求和

scene_spec.steps[3]

核对完整证明：$E[X]=\dfrac{1+2+3+4+5+6}{6}=\dfrac{21}{6}=\dfrac{7}{2}$。$E[X^2]=\dfrac{1+4+9+16+25+36}{6}=\dfrac{91}{6}$。$\operatorname{Var}(X)=E[X^2]-(E[X])^2=\dfrac{91}{6}-\dfrac{49}{4}=\dfrac{182-147}{12}=\dfrac{35}{12}$。

scene_spec.steps[4]

高亮结果：$E[X]=\dfrac{7}{2}$，$\operatorname{Var}(X)=\dfrac{35}{12}$

efficiency_tags[0]

均匀柱状图与重心 $\dfrac72$

efficiency_tags[1]

$E[X^2]=\dfrac{91}{6}$ 的逐格求和

## eval-prob-015-s2

problem

掷一枚均匀骰子，设 $X$ 为点数。求 $E[X]$ 与 $\operatorname{Var}(X)$。

solution

$M(t)=\dfrac{e^t+e^{2t}+e^{3t}+e^{4t}+e^{5t}+e^{6t}}{6}$。$M'(0)=\dfrac{1+2+3+4+5+6}{6}=\dfrac{7}{2}$，$M''(0)=\dfrac{1+4+9+16+25+36}{6}=\dfrac{91}{6}$。故 $E[X]=\dfrac{7}{2}$，$\operatorname{Var}(X)=M''(0)-[M'(0)]^2=\dfrac{35}{12}$。

answer

$E[X]=\dfrac{7}{2}$，$\operatorname{Var}(X)=\dfrac{35}{12}$

scene_spec.objects[0]

矩母函数 $M(t)$ 的曲线

scene_spec.objects[1]

$M'(0)=\dfrac72$、$M''(0)=\dfrac{91}{6}$ 的切线标注

scene_spec.steps[0]

第一步：以矩母函数为主线，建立概率论·数字特征场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：矩母函数 $M(t)$ 的曲线。

scene_spec.steps[2]

第三步：$M'(0)=\dfrac72$、$M''(0)=\dfrac{91}{6}$ 的切线标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

矩母函数 $M(t)$ 的曲线

efficiency_tags[1]

$M'(0)=\dfrac72$、$M''(0)=\dfrac{91}{6}$ 的切线标注

## eval-prob-015-s3

problem

掷一枚均匀骰子，设 $X$ 为点数。求 $E[X]$ 与 $\operatorname{Var}(X)$。

solution

令 $X=1+U$，其中 $U\sim U\{0,1,\dots,5\}$。离散均匀分布 $\{0,\dots,n-1\}$ 的方差公式：$\operatorname{Var}(U)=\dfrac{n^2-1}{12}=\dfrac{36-1}{12}=\dfrac{35}{12}$。故 $E[X]=1+\dfrac{5}{2}=\dfrac{7}{2}$，$\operatorname{Var}(X)=\operatorname{Var}(U)=\dfrac{35}{12}$。

answer

$E[X]=\dfrac{7}{2}$，$\operatorname{Var}(X)=\dfrac{35}{12}$

scene_spec.objects[0]

离散均匀方差 $\dfrac{n^2-1}{12}$ 的公式标注

scene_spec.objects[1]

平移 $+1$ 的方差不变性

scene_spec.steps[0]

第一步：以离散均匀公式+线性变换为主线，建立概率论·数字特征场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：离散均匀方差 $\dfrac{n^2-1}{12}$ 的公式标注。

scene_spec.steps[2]

第三步：平移 $+1$ 的方差不变性。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

离散均匀方差 $\dfrac{n^2-1}{12}$ 的公式标注

efficiency_tags[1]

平移 $+1$ 的方差不变性

## eval-linalg-001-s1

problem

计算范德蒙德行列式 $\begin{vmatrix}1&1&1\\a&b&c\\a^2&b^2&c^2\end{vmatrix}$，并求 $a=1,b=2,c=3$ 时的值。

solution

第二行减第一行的 $a$ 倍、第三行减第一行的 $a^2$ 倍：$D=\begin{vmatrix}1&1&1\\0&b-a&c-a\\0&b^2-a^2&c^2-a^2\end{vmatrix}$。按第一列展开：$D=\begin{vmatrix}b-a&c-a\\b^2-a^2&c^2-a^2\end{vmatrix}=(b-a)(c-a)\begin{vmatrix}1&1\\b+a&c+a\end{vmatrix}=(b-a)(c-a)\left[(c+a)-(b+a)\right]=(b-a)(c-a)(c-b)$。代入 $a=1,b=2,c=3$：$D=(1)(2)(1)=2$。

answer

$(b-a)(c-a)(c-b)$；取值 $2$

scene_spec.objects[0]

行变换 $R_2-aR_1$、$R_3-a^2R_1$ 的逐步动画

scene_spec.objects[1]

降阶二阶行列式的提取

scene_spec.steps[0]

第一步：以行变换降阶为主线，建立高等代数·行列式场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：行变换 $R_2-aR_1$、$R_3-a^2R_1$ 的逐步动画。

scene_spec.steps[2]

第三步：降阶二阶行列式的提取。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

行变换 $R_2-aR_1$、$R_3-a^2R_1$ 的逐步动画

efficiency_tags[1]

降阶二阶行列式的提取

## eval-linalg-001-s2

problem

计算范德蒙德行列式 $\begin{vmatrix}1&1&1\\a&b&c\\a^2&b^2&c^2\end{vmatrix}$，并求 $a=1,b=2,c=3$ 时的值。

solution

把 $D$ 看成关于 $c$ 的多项式 $f(c)$。按第三列展开，$c^2$ 的系数为 $\begin{vmatrix}1&1\\a&b\end{vmatrix}=b-a$，故 $f$ 至多是二次多项式。当 $c=a$ 或 $c=b$ 时，第三列与第一列（或第二列）相同，$f=0$，故 $f(c)=k(c-a)(c-b)$。取 $k=b-a$（最高次系数），得 $D=(b-a)(c-a)(c-b)$。（$a=b$ 时 $k=0$ 且 $D=0$，公式两端均为 0，仍成立。）

answer

$(b-a)(c-a)(c-b)$；取值 $2$

scene_spec.objects[0]

多项式 $f(c)$ 与根 $a,b$ 的标注

scene_spec.objects[1]

最高次系数 $b-a$ 的提取（含 $a=b$ 的零多项式情形）

scene_spec.steps[0]

第一步：以多项式观点为主线，建立高等代数·行列式场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：多项式 $f(c)$ 与根 $a,b$ 的标注。

scene_spec.steps[2]

第三步：最高次系数 $b-a$ 的提取（含 $a=b$ 的零多项式情形）。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

多项式 $f(c)$ 与根 $a,b$ 的标注

efficiency_tags[1]

最高次系数 $b-a$ 的提取（含 $a=b$ 的零多项式情形）

## eval-linalg-001-s3

problem

计算范德蒙德行列式 $\begin{vmatrix}1&1&1\\a&b&c\\a^2&b^2&c^2\end{vmatrix}$，并求 $a=1,b=2,c=3$ 时的值。

solution

$n$ 阶范德蒙德行列式 $D_n=\prod_{1\le i<j\le n}(x_j-x_i)$ 可用数学归纳法证明：自下而上做行变换 $R_k\leftarrow R_k-x_1R_{k-1}$（$k=n,n-1,\dots,2$），再按第一列展开、各列提取公因子 $x_j-x_1$，即降阶为 $n-1$ 阶范德蒙德行列式，归纳即得。$n=3$ 时即 $(b-a)(c-a)(c-b)$，代入得 $2$。

answer

$(b-a)(c-a)(c-b)$；取值 $2$

scene_spec.objects[0]

自下而上 $R_k\leftarrow R_k-x_1R_{k-1}$ 的归纳动画

scene_spec.objects[1]

各列提取公因子 $x_j-x_1$ 的降阶

scene_spec.steps[0]

第一步：以归纳验证为主线，建立高等代数·行列式场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：自下而上 $R_k\leftarrow R_k-x_1R_{k-1}$ 的归纳动画。

scene_spec.steps[2]

第三步：各列提取公因子 $x_j-x_1$ 的降阶。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

自下而上 $R_k\leftarrow R_k-x_1R_{k-1}$ 的归纳动画

efficiency_tags[1]

各列提取公因子 $x_j-x_1$ 的降阶

## eval-linalg-002-s1

problem

计算四阶行列式 $D=\begin{vmatrix}1&1&1&1\\1&2&1&1\\1&1&3&1\\1&1&1&4\end{vmatrix}$。

solution

第二、三、四行分别减去第一行：$D=\begin{vmatrix}1&1&1&1\\0&1&0&0\\0&0&2&0\\0&0&0&3\end{vmatrix}$。上三角行列式等于对角线元素之积：$D=1\cdot 1\cdot 2\cdot 3=6$。

answer

$6$

scene_spec.objects[0]

各行减首行的消元三角化动画

scene_spec.objects[1]

对角线 $1,1,2,3$ 之积的标注

scene_spec.steps[0]

第一步：以行变换三角化为主线，建立高等代数·行列式场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：各行减首行的消元三角化动画。

scene_spec.steps[2]

第三步：对角线 $1,1,2,3$ 之积的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

各行减首行的消元三角化动画

efficiency_tags[1]

对角线 $1,1,2,3$ 之积的标注

## eval-linalg-002-s2

problem

计算四阶行列式 $D=\begin{vmatrix}1&1&1&1\\1&2&1&1\\1&1&3&1\\1&1&1&4\end{vmatrix}$。

solution

加边升阶：$D=\begin{vmatrix}1&1&1&1&1\\0&1&1&1&1\\0&1&2&1&1\\0&1&1&3&1\\0&1&1&1&4\end{vmatrix}$（按第一列展开即原行列式）。新行列式中，第三、四、五行分别减去第二行：$=\begin{vmatrix}1&1&1&1&1\\0&1&1&1&1\\0&0&1&0&0\\0&0&0&2&0\\0&0&0&0&3\end{vmatrix}=1\cdot 1\cdot 1\cdot 2\cdot 3=6$。

answer

$6$

scene_spec.objects[0]

加边升阶的 $5\times5$ 结构示意

scene_spec.objects[1]

升阶后一次消元得对角形的过程

scene_spec.steps[0]

第一步：以加边法为主线，建立高等代数·行列式场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：加边升阶的 $5\times5$ 结构示意。

scene_spec.steps[2]

第三步：升阶后一次消元得对角形的过程。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

加边升阶的 $5\times5$ 结构示意

efficiency_tags[1]

升阶后一次消元得对角形的过程

## eval-linalg-002-s3

problem

计算四阶行列式 $D=\begin{vmatrix}1&1&1&1\\1&2&1&1\\1&1&3&1\\1&1&1&4\end{vmatrix}$。

solution

第一、二、三行分别减第四行，第四行保持不变：$\begin{vmatrix}0&0&0&-3\\0&1&0&-3\\0&0&2&-3\\1&1&1&4\end{vmatrix}$，按第一列展开：$D=(-1)^{4+1}\cdot 1\cdot\begin{vmatrix}0&0&-3\\1&0&-3\\0&2&-3\end{vmatrix}=-\left[0-0+(-3)\begin{vmatrix}1&0\\0&2\end{vmatrix}\right]=-(-3\cdot 2)=6$。

answer

$6$

scene_spec.objects[0]

前三行分别减第四行（第四行保持不变）的展开降阶

scene_spec.objects[1]

三阶余子式按第一列展开的高亮

scene_spec.steps[0]

呈现题干及适用条件：计算四阶行列式 $D=\begin{vmatrix}1&1&1&1\\1&2&1&1\\1&1&3&1\\1&1&1&4\end{vmatrix}$。

scene_spec.steps[1]

依次呈现：前三行分别减第四行（第四行保持不变）的展开降阶

scene_spec.steps[2]

依次呈现：三阶余子式按第一列展开的高亮

scene_spec.steps[3]

核对完整证明：第一、二、三行分别减第四行，第四行保持不变：$\begin{vmatrix}0&0&0&-3\\0&1&0&-3\\0&0&2&-3\\1&1&1&4\end{vmatrix}$，按第一列展开：$D=(-1)^{4+1}\cdot 1\cdot\begin{vmatrix}0&0&-3\\1&0&-3\\0&2&-3\end{vmatrix}=-\left[0-0+(-3)\begin{vmatrix}1&0\\0&2\end{vmatrix}\right]=-(-3\cdot 2)=6$。

scene_spec.steps[4]

高亮结果：$6$

efficiency_tags[0]

前三行分别减第四行（第四行保持不变）的展开降阶

efficiency_tags[1]

三阶余子式按第一列展开的高亮

## eval-linalg-003-s1

problem

求 $n$ 阶三对角行列式 $D_n=\begin{vmatrix}2&1&0&\cdots&0\\1&2&1&\cdots&0\\0&1&2&\cdots&0\\\vdots&&&\ddots&\vdots\\0&0&0&\cdots&2\end{vmatrix}$ 的值（矩阵元素满足 $a_{ii}=2$，$a_{i,i+1}=a_{i+1,i}=1$，其余为 0）。

solution

按第一行展开：$D_n=2D_{n-1}-1\cdot\begin{vmatrix}1&1&0&\cdots\\0&2&1&\cdots\\\vdots&&&\ddots\end{vmatrix}=2D_{n-1}-D_{n-2}$（第二项按第一列展开后恰为 $D_{n-2}$）。初始值 $D_1=2$，$D_2=\begin{vmatrix}2&1\\1&2\end{vmatrix}=3$。由递推 $D_n-D_{n-1}=D_{n-1}-D_{n-2}=\cdots=D_2-D_1=1$，故 $D_n=D_1+(n-1)=n+1$。

answer

$D_n=n+1$

scene_spec.objects[0]

首行展开的递推树 $D_n=2D_{n-1}-D_{n-2}$

scene_spec.objects[1]

递推序列 $2,3,4,\dots$ 的点列

scene_spec.steps[0]

第一步：以递推公式为主线，建立高等代数·行列式场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：首行展开的递推树 $D_n=2D_{n-1}-D_{n-2}$。

scene_spec.steps[2]

第三步：递推序列 $2,3,4,\dots$ 的点列。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

首行展开的递推树 $D_n=2D_{n-1}-D_{n-2}$

efficiency_tags[1]

递推序列 $2,3,4,\dots$ 的点列

## eval-linalg-003-s2

problem

求 $n$ 阶三对角行列式 $D_n=\begin{vmatrix}2&1&0&\cdots&0\\1&2&1&\cdots&0\\0&1&2&\cdots&0\\\vdots&&&\ddots&\vdots\\0&0&0&\cdots&2\end{vmatrix}$ 的值（矩阵元素满足 $a_{ii}=2$，$a_{i,i+1}=a_{i+1,i}=1$，其余为 0）。

solution

该矩阵 $A=2I+B$，其中 $B$ 是 $n$ 阶路的邻接矩阵，其特征值为 $2\cos\dfrac{k\pi}{n+1}$（$k=1,\dots,n$）。故 $D_n=\det(2I+B)=\displaystyle\prod_{k=1}^{n}\left(2+2\cos\dfrac{k\pi}{n+1}\right)=2^n\prod_{k=1}^{n}\left(1+\cos\dfrac{k\pi}{n+1}\right)$。利用恒等式 $\displaystyle\prod_{k=1}^{n}\left(2+2\cos\dfrac{k\pi}{n+1}\right)=n+1$，证明如下：由 $x^{2n+2}-1=(x^2-1)\displaystyle\prod_{k=1}^{n}\left(x^2-2x\cos\dfrac{k\pi}{n+1}+1\right)$，两边同除 $x^2-1$ 得 $\dfrac{x^{2n+2}-1}{x^2-1}=\displaystyle\sum_{j=0}^{n}x^{2j}=\prod_{k=1}^{n}\left(x^2-2x\cos\dfrac{k\pi}{n+1}+1\right)$；令 $x\to-1$：左端 $\to n+1$，右端 $\to\displaystyle\prod_{k=1}^{n}\left(2+2\cos\dfrac{k\pi}{n+1}\right)$。得 $D_n=n+1$。

answer

$D_n=n+1$

scene_spec.objects[0]

邻接矩阵特征值 $2\cos\dfrac{k\pi}{n+1}$ 的单位圆标注

scene_spec.objects[1]

恒等式 $x^{2n+2}-1$ 除 $x^2-1$ 取极限的推导

scene_spec.steps[0]

第一步：以特征值乘积为主线，建立高等代数·行列式场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：邻接矩阵特征值 $2\cos\dfrac{k\pi}{n+1}$ 的单位圆标注。

scene_spec.steps[2]

第三步：恒等式 $x^{2n+2}-1$ 除 $x^2-1$ 取极限的推导。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

邻接矩阵特征值 $2\cos\dfrac{k\pi}{n+1}$ 的单位圆标注

efficiency_tags[1]

恒等式 $x^{2n+2}-1$ 除 $x^2-1$ 取极限的推导

## eval-linalg-003-s3

problem

求 $n$ 阶三对角行列式 $D_n=\begin{vmatrix}2&1&0&\cdots&0\\1&2&1&\cdots&0\\0&1&2&\cdots&0\\\vdots&&&\ddots&\vdots\\0&0&0&\cdots&2\end{vmatrix}$ 的值（矩阵元素满足 $a_{ii}=2$，$a_{i,i+1}=a_{i+1,i}=1$，其余为 0）。

solution

由解法一的递推式，归纳证明 $D_n=n+1$：$n=1,2$ 已验证；设 $D_{n-1}=n$、$D_{n-2}=n-1$，则 $D_n=2D_{n-1}-D_{n-2}=2n-(n-1)=n+1$。

answer

$D_n=n+1$

scene_spec.objects[0]

归纳递推 $2n-(n-1)=n+1$ 的代入

scene_spec.objects[1]

三对角矩阵结构高亮

scene_spec.steps[0]

第一步：以数学归纳法为主线，建立高等代数·行列式场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：归纳递推 $2n-(n-1)=n+1$ 的代入。

scene_spec.steps[2]

第三步：三对角矩阵结构高亮。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

归纳递推 $2n-(n-1)=n+1$ 的代入

efficiency_tags[1]

三对角矩阵结构高亮

## eval-linalg-004-s1

problem

计算 $n=3$ 时行列式 $D=\begin{vmatrix}a+b&a&a\\a&a+b&a\\a&a&a+b\end{vmatrix}$，并推广到 $n$ 阶。

solution

第二、三行分别减去第一行：$D=\begin{vmatrix}a+b&a&a\\-b&b&0\\-b&0&b\end{vmatrix}$。按第一行展开：$D=(a+b)\cdot b^2-a\cdot\begin{vmatrix}-b&0\\-b&b\end{vmatrix}+a\cdot\begin{vmatrix}-b&b\\-b&0\end{vmatrix}=(a+b)b^2-a(-b^2)+a(b^2)=b^2(a+b)+ab^2+ab^2=b^2(3a+b)$。对$n\ge2$，矩阵$M=bI+aJ$中$R_i\leftarrow R_i-R_1$（$i=2,\ldots,n$），第$i$行只在第1列有$-b$、第$i$列有$b$。再令$C_1\leftarrow C_1+C_2+\cdots+C_n$，第一列变为$(na+b,0,\ldots,0)^T$，余下主对角为$b$，所以$\det M=(na+b)b^{n-1}$。$n=1$时直接为$a+b$。全过程不除以$b$，包含$b=0$。

answer

$b^2(3a+b)$；$n$ 阶为 $b^{n-1}(na+b)$

scene_spec.objects[0]

$R_i\leftarrow R_i-R_1$（$2\le i\le n$）

scene_spec.objects[1]

$C_1\leftarrow\sum_{j=1}^nC_j$后第一列为$(na+b,0,\ldots,0)^T$

scene_spec.objects[2]

$\det M=(na+b)b^{n-1}$；$n=1$另作$a+b$

scene_spec.steps[0]

呈现题干及适用条件：计算 $n=3$ 时行列式 $D=\begin{vmatrix}a+b&a&a\\a&a+b&a\\a&a&a+b\end{vmatrix}$，并推广到 $n$ 阶。

scene_spec.steps[1]

依次呈现：$R_i\leftarrow R_i-R_1$（$2\le i\le n$）

scene_spec.steps[2]

依次呈现：$C_1\leftarrow\sum_{j=1}^nC_j$后第一列为$(na+b,0,\ldots,0)^T$

scene_spec.steps[3]

依次呈现：$\det M=(na+b)b^{n-1}$；$n=1$另作$a+b$

scene_spec.steps[4]

核对完整证明：第二、三行分别减去第一行：$D=\begin{vmatrix}a+b&a&a\\-b&b&0\\-b&0&b\end{vmatrix}$。按第一行展开：$D=(a+b)\cdot b^2-a\cdot\begin{vmatrix}-b&0\\-b&b\end{vmatrix}+a\cdot\begin{vmatrix}-b&b\\-b&0\end{vmatrix}=(a+b)b^2-a(-b^2)+a(b^2)=b^2(a+b)+ab^2+ab^2=b^2(3a+b)$。对$n\ge2$，矩阵$M=bI+aJ$中$R_i\leftarrow R_i-R_1$（$i=2,\ldots,n$），第$i$行只在第1列有$-b$、第$i$列有$b$。再令$C_1\leftarrow C_1+C_2+\cdots+C_n$，第一列变为$(na+b,0,\ldots,0)^T$，余下主对角为$b$，所以$\det M=(na+b)b^{n-1}$。$n=1$时直接为$a+b$。全过程不除以$b$，包含$b=0$。

scene_spec.steps[5]

高亮结果：$b^2(3a+b)$；$n$ 阶为 $b^{n-1}(na+b)$

efficiency_tags[0]

$R_i\leftarrow R_i-R_1$（$2\le i\le n$）

efficiency_tags[1]

$C_1\leftarrow\sum_{j=1}^nC_j$后第一列为$(na+b,0,\ldots,0)^T$

efficiency_tags[2]

$\det M=(na+b)b^{n-1}$；$n=1$另作$a+b$

## eval-linalg-004-s2

problem

计算 $n=3$ 时行列式 $D=\begin{vmatrix}a+b&a&a\\a&a+b&a\\a&a&a+b\end{vmatrix}$，并推广到 $n$ 阶。

solution

该矩阵 $A=bI+aJ$，其中 $J$ 为全 1 矩阵。$J$ 的特征值为 $n,0,\dots,0$（$J$ 的秩为 1，且 $J(1,\dots,1)^T=n(1,\dots,1)^T$），故 $A$ 的特征值为 $b+na$（一重）与 $b$（$n-1$ 重）。行列式=特征值之积：$D=(b+3a)\cdot b\cdot b=b^2(3a+b)$（$n=3$）；一般地 $D_n=b^{n-1}(na+b)$。

answer

$b^2(3a+b)$；$n$ 阶为 $b^{n-1}(na+b)$

scene_spec.objects[0]

矩阵分解 $bI+aJ$ 的色块示意

scene_spec.objects[1]

特征值$b+na$（沿全1向量）、$b$（其正交补，重数$n-1$） 的谱标注

scene_spec.steps[0]

呈现题干及适用条件：计算 $n=3$ 时行列式 $D=\begin{vmatrix}a+b&a&a\\a&a+b&a\\a&a&a+b\end{vmatrix}$，并推广到 $n$ 阶。

scene_spec.steps[1]

依次呈现：矩阵分解 $bI+aJ$ 的色块示意

scene_spec.steps[2]

依次呈现：特征值$b+na$（沿全1向量）、$b$（其正交补，重数$n-1$） 的谱标注

scene_spec.steps[3]

核对完整证明：该矩阵 $A=bI+aJ$，其中 $J$ 为全 1 矩阵。$J$ 的特征值为 $n,0,\dots,0$（$J$ 的秩为 1，且 $J(1,\dots,1)^T=n(1,\dots,1)^T$），故 $A$ 的特征值为 $b+na$（一重）与 $b$（$n-1$ 重）。行列式=特征值之积：$D=(b+3a)\cdot b\cdot b=b^2(3a+b)$（$n=3$）；一般地 $D_n=b^{n-1}(na+b)$。

scene_spec.steps[4]

高亮结果：$b^2(3a+b)$；$n$ 阶为 $b^{n-1}(na+b)$

efficiency_tags[0]

矩阵分解 $bI+aJ$ 的色块示意

efficiency_tags[1]

特征值$b+na$（沿全1向量）、$b$（其正交补，重数$n-1$） 的谱标注

## eval-linalg-004-s3

problem

计算 $n=3$ 时行列式 $D=\begin{vmatrix}a+b&a&a\\a&a+b&a\\a&a&a+b\end{vmatrix}$，并推广到 $n$ 阶。

solution

把每列拆成 $(a,a,a)^T+b\,e_i$（$e_i$ 为标准基向量）。由行列式关于列的多重线性：全取 $b\,e_i$ 的项为 $b^3\det I=b^3$；恰有一列取 $(a,a,a)^T$ 的项有 3 个，每个为 $ab^2\cdot\det(e_1,e_2,e_j$ 换为 $(1,1,1)^T)=ab^2$；有两列以上取 $(a,a,a)^T$ 的项行列式为 0（两列相同）。故 $D=b^3+3ab^2=b^2(3a+b)$。一般$n\ge2$同理：每列为$be_j+a\mathbf1$。多重线性展开中，选择两个及以上$a\mathbf1$列的项因重复列为零；全选$be_j$给$b^n$；恰选一个$a\mathbf1$列有$n$项，每项为$ab^{n-1}$（把该列的$\mathbf1=\sum_j e_j$展开，只有原列位置的$e_j$能留下非零行列式）。故总和为$b^n+nab^{n-1}=(na+b)b^{n-1}$。$n=1$直接为$a+b$。

answer

$b^2(3a+b)$；$n$ 阶为 $b^{n-1}(na+b)$

scene_spec.objects[0]

拆列法的组合枚举（全 $b$ 列、恰一 $a$ 列、两 $a$ 列为零）

scene_spec.objects[1]

多重线性的标注

scene_spec.steps[0]

呈现题干及适用条件：计算 $n=3$ 时行列式 $D=\begin{vmatrix}a+b&a&a\\a&a+b&a\\a&a&a+b\end{vmatrix}$，并推广到 $n$ 阶。

scene_spec.steps[1]

依次呈现：拆列法的组合枚举（全 $b$ 列、恰一 $a$ 列、两 $a$ 列为零）

scene_spec.steps[2]

依次呈现：多重线性的标注

scene_spec.steps[3]

核对完整证明：把每列拆成 $(a,a,a)^T+b\,e_i$（$e_i$ 为标准基向量）。由行列式关于列的多重线性：全取 $b\,e_i$ 的项为 $b^3\det I=b^3$；恰有一列取 $(a,a,a)^T$ 的项有 3 个，每个为 $ab^2\cdot\det(e_1,e_2,e_j$ 换为 $(1,1,1)^T)=ab^2$；有两列以上取 $(a,a,a)^T$ 的项行列式为 0（两列相同）。故 $D=b^3+3ab^2=b^2(3a+b)$。一般$n\ge2$同理：每列为$be_j+a\mathbf1$。多重线性展开中，选择两个及以上$a\mathbf1$列的项因重复列为零；全选$be_j$给$b^n$；恰选一个$a\mathbf1$列有$n$项，每项为$ab^{n-1}$（把该列的$\mathbf1=\sum_j e_j$展开，只有原列位置的$e_j$能留下非零行列式）。故总和为$b^n+nab^{n-1}=(na+b)b^{n-1}$。$n=1$直接为$a+b$。

scene_spec.steps[4]

高亮结果：$b^2(3a+b)$；$n$ 阶为 $b^{n-1}(na+b)$

efficiency_tags[0]

拆列法的组合枚举（全 $b$ 列、恰一 $a$ 列、两 $a$ 列为零）

efficiency_tags[1]

多重线性的标注

## eval-linalg-005-s1

problem

求矩阵 $A=\begin{pmatrix}3&2\\4&3\end{pmatrix}$ 的逆矩阵。

solution

$\det A=3\cdot 3-2\cdot 4=9-8=1$。$A^*=\begin{pmatrix}3&-2\\-4&3\end{pmatrix}$（代数余子式转置：$A_{11}=3$，$A_{12}=-4$，$A_{21}=-2$，$A_{22}=3$）。$A^{-1}=\dfrac{A^*}{\det A}=\begin{pmatrix}3&-2\\-4&3\end{pmatrix}$。验证：$AA^{-1}=\begin{pmatrix}9-8&-6+6\\12-12&-8+9\end{pmatrix}=I$。

answer

$A^{-1}=\begin{pmatrix}3&-2\\-4&3\end{pmatrix}$

scene_spec.objects[0]

伴随矩阵四个代数余子式的标注

scene_spec.objects[1]

$\det A=1$ 的标注

scene_spec.steps[0]

第一步：以伴随矩阵法为主线，建立高等代数·矩阵场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：伴随矩阵四个代数余子式的标注。

scene_spec.steps[2]

第三步：$\det A=1$ 的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

伴随矩阵四个代数余子式的标注

efficiency_tags[1]

$\det A=1$ 的标注

## eval-linalg-005-s2

problem

求矩阵 $A=\begin{pmatrix}3&2\\4&3\end{pmatrix}$ 的逆矩阵。

solution

对增广矩阵 $(A\mid I)$ 做行变换：$\begin{pmatrix}3&2&|&1&0\\4&3&|&0&1\end{pmatrix}\xrightarrow{R_2-\frac{4}{3}R_1}\begin{pmatrix}3&2&|&1&0\\0&\frac{1}{3}&|&-\frac{4}{3}&1\end{pmatrix}\xrightarrow{R_1-6R_2}\begin{pmatrix}3&0&|&9&-6\\0&\frac{1}{3}&|&-\frac{4}{3}&1\end{pmatrix}\xrightarrow{R_1/3,\ 3R_2}\begin{pmatrix}1&0&|&3&-2\\0&1&|&-4&3\end{pmatrix}$，故 $A^{-1}=\begin{pmatrix}3&-2\\-4&3\end{pmatrix}$。

answer

$A^{-1}=\begin{pmatrix}3&-2\\-4&3\end{pmatrix}$

scene_spec.objects[0]

$(A|I)\to(I|A^{-1})$ 的行变换动画

scene_spec.objects[1]

分数消元的逐步展示

scene_spec.steps[0]

第一步：以初等行变换为主线，建立高等代数·矩阵场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：$(A|I)\to(I|A^{-1})$ 的行变换动画。

scene_spec.steps[2]

第三步：分数消元的逐步展示。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

$(A|I)\to(I|A^{-1})$ 的行变换动画

efficiency_tags[1]

分数消元的逐步展示

## eval-linalg-005-s3

problem

求矩阵 $A=\begin{pmatrix}3&2\\4&3\end{pmatrix}$ 的逆矩阵。

solution

设 $A^{-1}$ 的第 $j$ 列为 $x^{(j)}$，解 $Ax^{(1)}=e_1$、$Ax^{(2)}=e_2$。第一组：$\begin{cases}3x+2y=1\\4x+3y=0\end{cases}$，由第二式 $y=-\dfrac{4x}{3}$ 代入第一式：$3x-\dfrac{8x}{3}=1$，$x=3$，$y=-4$。第二组：$\begin{cases}3x+2y=0\\4x+3y=1\end{cases}$，得 $x=-2$，$y=3$。故 $A^{-1}=\begin{pmatrix}3&-2\\-4&3\end{pmatrix}$。

answer

$A^{-1}=\begin{pmatrix}3&-2\\-4&3\end{pmatrix}$

scene_spec.objects[0]

解 $Ax=e_1$、$Ax=e_2$ 两组方程的过程

scene_spec.objects[1]

$AA^{-1}=I$ 验证

scene_spec.steps[0]

第一步：以解方程组为主线，建立高等代数·矩阵场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：解 $Ax=e_1$、$Ax=e_2$ 两组方程的过程。

scene_spec.steps[2]

第三步：$AA^{-1}=I$ 验证。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

解 $Ax=e_1$、$Ax=e_2$ 两组方程的过程

efficiency_tags[1]

$AA^{-1}=I$ 验证

## eval-linalg-006-s1

problem

设 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$，求 $A^n$（$n$ 为正整数）。

solution

$A^1=\begin{pmatrix}1&1\\0&1\end{pmatrix}$。设 $A^k=\begin{pmatrix}1&k\\0&1\end{pmatrix}$，则 $A^{k+1}=A^kA=\begin{pmatrix}1&k\\0&1\end{pmatrix}\begin{pmatrix}1&1\\0&1\end{pmatrix}=\begin{pmatrix}1&1+k\\0&1\end{pmatrix}$。归纳得 $A^n=\begin{pmatrix}1&n\\0&1\end{pmatrix}$。

answer

$A^n=\begin{pmatrix}1&n\\0&1\end{pmatrix}$

scene_spec.objects[0]

$A^{k+1}=A^kA$ 的乘法递推动画

scene_spec.objects[1]

$A^n$ 元素随 $n$ 增长的表格

scene_spec.steps[0]

第一步：以数学归纳法为主线，建立高等代数·矩阵场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：$A^{k+1}=A^kA$ 的乘法递推动画。

scene_spec.steps[2]

第三步：$A^n$ 元素随 $n$ 增长的表格。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

$A^{k+1}=A^kA$ 的乘法递推动画

efficiency_tags[1]

$A^n$ 元素随 $n$ 增长的表格

## eval-linalg-006-s2

problem

设 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$，求 $A^n$（$n$ 为正整数）。

solution

$A=I+N$，其中 $N=\begin{pmatrix}0&1\\0&0\end{pmatrix}$，且 $N^2=0$。$I$ 与 $N$ 可交换，由二项式定理：$A^n=(I+N)^n=I^n+\binom{n}{1}I^{n-1}N+\binom{n}{2}I^{n-2}N^2+\cdots=I+nN=\begin{pmatrix}1&n\\0&1\end{pmatrix}$（$N^2$ 起全为 0）。

answer

$A^n=\begin{pmatrix}1&n\\0&1\end{pmatrix}$

scene_spec.objects[0]

二项式展开只留两项（$N^2=0$）的原因

scene_spec.objects[1]

$I$ 与 $N$ 可交换的标注

scene_spec.steps[0]

第一步：以二项式展开为主线，建立高等代数·矩阵场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：二项式展开只留两项（$N^2=0$）的原因。

scene_spec.steps[2]

第三步：$I$ 与 $N$ 可交换的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

二项式展开只留两项（$N^2=0$）的原因

efficiency_tags[1]

$I$ 与 $N$ 可交换的标注

## eval-linalg-006-s3

problem

设 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$，求 $A^n$（$n$ 为正整数）。

solution

该矩阵作用为$(x,y)\mapsto(x+y,y)$。归纳可得迭代$n\ge0$次为$(x+ny,y)$（$n=0$为恒等；再作用一次把$x+ny$变为$x+(n+1)y$）。因此$A^n=\begin{pmatrix}1&n\\0&1\end{pmatrix}$。

answer

$A^n=\begin{pmatrix}1&n\\0&1\end{pmatrix}$

scene_spec.objects[0]

剪切变换重复作用的动画

scene_spec.objects[1]

若尔当形 $J=A$ 本身的标注

scene_spec.steps[0]

呈现题干及适用条件：设 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$，求 $A^n$（$n$ 为正整数）。

scene_spec.steps[1]

依次呈现：剪切变换重复作用的动画

scene_spec.steps[2]

依次呈现：若尔当形 $J=A$ 本身的标注

scene_spec.steps[3]

核对完整证明：该矩阵作用为$(x,y)\mapsto(x+y,y)$。归纳可得迭代$n\ge0$次为$(x+ny,y)$（$n=0$为恒等；再作用一次把$x+ny$变为$x+(n+1)y$）。因此$A^n=\begin{pmatrix}1&n\\0&1\end{pmatrix}$。

scene_spec.steps[4]

高亮结果：$A^n=\begin{pmatrix}1&n\\0&1\end{pmatrix}$

efficiency_tags[0]

剪切变换重复作用的动画

efficiency_tags[1]

若尔当形 $J=A$ 本身的标注

## eval-linalg-007-s1

problem

设 $A=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}$，求 $A^n$。其中$n\in\mathbb Z_{\ge0}$；$n=0$时按$A^0=I$。

solution

$n=1$ 成立。设 $A^k=\begin{pmatrix}\cos k\theta&-\sin k\theta\\\sin k\theta&\cos k\theta\end{pmatrix}$，则 $A^{k+1}=A^kA$，其 $(1,1)$ 元为 $\cos k\theta\cos\theta-\sin k\theta\sin\theta=\cos(k+1)\theta$，$(1,2)$ 元为 $-\cos k\theta\sin\theta-\sin k\theta\cos\theta=-\sin(k+1)\theta$，其余两元同理。归纳成立。

answer

$A^n=\begin{pmatrix}\cos n\theta&-\sin n\theta\\\sin n\theta&\cos n\theta\end{pmatrix}$

scene_spec.objects[0]

$A^{k+1}=A^kA$ 的和角公式动画

scene_spec.objects[1]

单位向量旋转 $n\theta$ 的动画

scene_spec.steps[0]

呈现题干及适用条件：设 $A=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}$，求 $A^n$。其中$n\in\mathbb Z_{\ge0}$；$n=0$时按$A^0=I$。

scene_spec.steps[1]

依次呈现：$A^{k+1}=A^kA$ 的和角公式动画

scene_spec.steps[2]

依次呈现：单位向量旋转 $n\theta$ 的动画

scene_spec.steps[3]

核对完整证明：$n=1$ 成立。设 $A^k=\begin{pmatrix}\cos k\theta&-\sin k\theta\\\sin k\theta&\cos k\theta\end{pmatrix}$，则 $A^{k+1}=A^kA$，其 $(1,1)$ 元为 $\cos k\theta\cos\theta-\sin k\theta\sin\theta=\cos(k+1)\theta$，$(1,2)$ 元为 $-\cos k\theta\sin\theta-\sin k\theta\cos\theta=-\sin(k+1)\theta$，其余两元同理。归纳成立。

scene_spec.steps[4]

高亮结果：$A^n=\begin{pmatrix}\cos n\theta&-\sin n\theta\\\sin n\theta&\cos n\theta\end{pmatrix}$

efficiency_tags[0]

$A^{k+1}=A^kA$ 的和角公式动画

efficiency_tags[1]

单位向量旋转 $n\theta$ 的动画

## eval-linalg-007-s2

problem

设 $A=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}$，求 $A^n$。其中$n\in\mathbb Z_{\ge0}$；$n=0$时按$A^0=I$。

solution

特征方程 $(\cos\theta-\lambda)^2+\sin^2\theta=0$，即 $\lambda^2-2\lambda\cos\theta+1=0$，特征值 $\lambda=e^{\pm i\theta}$，对应特征向量 $(1,\mp i)^T$。取 $P=\begin{pmatrix}1&1\\-i&i\end{pmatrix}$，$P^{-1}=\dfrac{1}{2}\begin{pmatrix}1&i\\1&-i\end{pmatrix}$，则 $A=P\begin{pmatrix}e^{i\theta}&0\\0&e^{-i\theta}\end{pmatrix}P^{-1}$。故 $A^n=P\begin{pmatrix}e^{in\theta}&0\\0&e^{-in\theta}\end{pmatrix}P^{-1}=\dfrac{1}{2}\begin{pmatrix}e^{in\theta}+e^{-in\theta}&i(e^{in\theta}-e^{-in\theta})\\-i(e^{in\theta}-e^{-in\theta})&e^{in\theta}+e^{-in\theta}\end{pmatrix}=\begin{pmatrix}\cos n\theta&-\sin n\theta\\\sin n\theta&\cos n\theta\end{pmatrix}$（用欧拉公式 $e^{\pm in\theta}=\cos n\theta\pm i\sin n\theta$ 化简）。

answer

$A^n=\begin{pmatrix}\cos n\theta&-\sin n\theta\\\sin n\theta&\cos n\theta\end{pmatrix}$

scene_spec.objects[0]

特征值 $e^{\pm i\theta}$ 的单位圆标注

scene_spec.objects[1]

对角化三连乘的矩阵运算

scene_spec.steps[0]

呈现题干及适用条件：设 $A=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}$，求 $A^n$。其中$n\in\mathbb Z_{\ge0}$；$n=0$时按$A^0=I$。

scene_spec.steps[1]

依次呈现：特征值 $e^{\pm i\theta}$ 的单位圆标注

scene_spec.steps[2]

依次呈现：对角化三连乘的矩阵运算

scene_spec.steps[3]

核对完整证明：特征方程 $(\cos\theta-\lambda)^2+\sin^2\theta=0$，即 $\lambda^2-2\lambda\cos\theta+1=0$，特征值 $\lambda=e^{\pm i\theta}$，对应特征向量 $(1,\mp i)^T$。取 $P=\begin{pmatrix}1&1\\-i&i\end{pmatrix}$，$P^{-1}=\dfrac{1}{2}\begin{pmatrix}1&i\\1&-i\end{pmatrix}$，则 $A=P\begin{pmatrix}e^{i\theta}&0\\0&e^{-i\theta}\end{pmatrix}P^{-1}$。故 $A^n=P\begin{pmatrix}e^{in\theta}&0\\0&e^{-in\theta}\end{pmatrix}P^{-1}=\dfrac{1}{2}\begin{pmatrix}e^{in\theta}+e^{-in\theta}&i(e^{in\theta}-e^{-in\theta})\\-i(e^{in\theta}-e^{-in\theta})&e^{in\theta}+e^{-in\theta}\end{pmatrix}=\begin{pmatrix}\cos n\theta&-\sin n\theta\\\sin n\theta&\cos n\theta\end{pmatrix}$（用欧拉公式 $e^{\pm in\theta}=\cos n\theta\pm i\sin n\theta$ 化简）。

scene_spec.steps[4]

高亮结果：$A^n=\begin{pmatrix}\cos n\theta&-\sin n\theta\\\sin n\theta&\cos n\theta\end{pmatrix}$

efficiency_tags[0]

特征值 $e^{\pm i\theta}$ 的单位圆标注

efficiency_tags[1]

对角化三连乘的矩阵运算

## eval-linalg-007-s3

problem

设 $A=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}$，求 $A^n$。其中$n\in\mathbb Z_{\ge0}$；$n=0$时按$A^0=I$。

solution

旋转矩阵 $A$ 与复数乘法 $z\mapsto e^{i\theta}z$ 一一对应（$(x,y)\mapsto(x\cos\theta-y\sin\theta,\ x\sin\theta+y\cos\theta)$ 正是 $e^{i\theta}(x+iy)$ 的实虚部）。旋转的复合即角度相加：$(e^{i\theta})^n=e^{in\theta}$，对应 $A^n=$ 旋转 $n\theta$ 角的矩阵。

answer

$A^n=\begin{pmatrix}\cos n\theta&-\sin n\theta\\\sin n\theta&\cos n\theta\end{pmatrix}$

scene_spec.objects[0]

复平面与实平面的对应

scene_spec.objects[1]

$e^{i\theta}$ 幂的辐角累加

scene_spec.steps[0]

呈现题干及适用条件：设 $A=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}$，求 $A^n$。其中$n\in\mathbb Z_{\ge0}$；$n=0$时按$A^0=I$。

scene_spec.steps[1]

依次呈现：复平面与实平面的对应

scene_spec.steps[2]

依次呈现：$e^{i\theta}$ 幂的辐角累加

scene_spec.steps[3]

核对完整证明：旋转矩阵 $A$ 与复数乘法 $z\mapsto e^{i\theta}z$ 一一对应（$(x,y)\mapsto(x\cos\theta-y\sin\theta,\ x\sin\theta+y\cos\theta)$ 正是 $e^{i\theta}(x+iy)$ 的实虚部）。旋转的复合即角度相加：$(e^{i\theta})^n=e^{in\theta}$，对应 $A^n=$ 旋转 $n\theta$ 角的矩阵。

scene_spec.steps[4]

高亮结果：$A^n=\begin{pmatrix}\cos n\theta&-\sin n\theta\\\sin n\theta&\cos n\theta\end{pmatrix}$

efficiency_tags[0]

复平面与实平面的对应

efficiency_tags[1]

$e^{i\theta}$ 幂的辐角累加

## eval-linalg-008-s1

problem

设 $A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$，求 $\det A$、$A$ 的秩与 $A^{-1}$。

solution

$\det A=1\cdot 4-2\cdot 3=-2\ne 0$，故 $A$ 可逆、秩为 $2$。$A^*=\begin{pmatrix}4&-2\\-3&1\end{pmatrix}$，$A^{-1}=\dfrac{A^*}{\det A}=\dfrac{1}{-2}\begin{pmatrix}4&-2\\-3&1\end{pmatrix}=\begin{pmatrix}-2&1\\\frac{3}{2}&-\frac{1}{2}\end{pmatrix}$。

answer

$\det A=-2$；秩为 $2$；$A^{-1}=\begin{pmatrix}-2&1\\\frac{3}{2}&-\frac{1}{2}\end{pmatrix}$

scene_spec.objects[0]

伴随矩阵代数余子式标注

scene_spec.objects[1]

除以 $\det A=-2$ 的过程

scene_spec.steps[0]

第一步：以伴随矩阵法为主线，建立高等代数·矩阵场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：伴随矩阵代数余子式标注。

scene_spec.steps[2]

第三步：除以 $\det A=-2$ 的过程。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

伴随矩阵代数余子式标注

efficiency_tags[1]

除以 $\det A=-2$ 的过程

## eval-linalg-008-s2

problem

设 $A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$，求 $\det A$、$A$ 的秩与 $A^{-1}$。

solution

$(A\mid I)=\begin{pmatrix}1&2&|&1&0\\3&4&|&0&1\end{pmatrix}\xrightarrow{R_2-3R_1}\begin{pmatrix}1&2&|&1&0\\0&-2&|&-3&1\end{pmatrix}\xrightarrow{-\frac{1}{2}R_2}\begin{pmatrix}1&2&|&1&0\\0&1&|&\frac{3}{2}&-\frac{1}{2}\end{pmatrix}\xrightarrow{R_1-2R_2}\begin{pmatrix}1&0&|&-2&1\\0&1&|&\frac{3}{2}&-\frac{1}{2}\end{pmatrix}$。故 $A^{-1}=\begin{pmatrix}-2&1\\\frac{3}{2}&-\frac{1}{2}\end{pmatrix}$。

answer

$\det A=-2$；秩为 $2$；$A^{-1}=\begin{pmatrix}-2&1\\\frac{3}{2}&-\frac{1}{2}\end{pmatrix}$

scene_spec.objects[0]

$(A|I)\to(I|A^{-1})$ 的行变换动画

scene_spec.objects[1]

分数消元的逐步展示

scene_spec.steps[0]

第一步：以初等行变换为主线，建立高等代数·矩阵场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：$(A|I)\to(I|A^{-1})$ 的行变换动画。

scene_spec.steps[2]

第三步：分数消元的逐步展示。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

$(A|I)\to(I|A^{-1})$ 的行变换动画

efficiency_tags[1]

分数消元的逐步展示

## eval-linalg-008-s3

problem

设 $A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$，求 $\det A$、$A$ 的秩与 $A^{-1}$。

solution

$\det A=-2\ne 0$ 说明两行（列）线性无关，$\operatorname{rank}A=2$。验证逆矩阵：$AA^{-1}=\begin{pmatrix}1&2\\3&4\end{pmatrix}\begin{pmatrix}-2&1\\\frac{3}{2}&-\frac{1}{2}\end{pmatrix}=\begin{pmatrix}-2+3&1-1\\-6+6&3-2\end{pmatrix}=\begin{pmatrix}1&0\\0&1\end{pmatrix}$。

answer

$\det A=-2$；秩为 $2$；$A^{-1}=\begin{pmatrix}-2&1\\\frac{3}{2}&-\frac{1}{2}\end{pmatrix}$

scene_spec.objects[0]

单位正方形映射到平行四边形的面积$2$，有向面积为$-2$（定向反转）

scene_spec.objects[1]

逆矩阵验证乘法

scene_spec.steps[0]

呈现题干及适用条件：设 $A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$，求 $\det A$、$A$ 的秩与 $A^{-1}$。

scene_spec.steps[1]

依次呈现：单位正方形映射到平行四边形的面积$2$，有向面积为$-2$（定向反转）

scene_spec.steps[2]

依次呈现：逆矩阵验证乘法

scene_spec.steps[3]

核对完整证明：$\det A=-2\ne 0$ 说明两行（列）线性无关，$\operatorname{rank}A=2$。验证逆矩阵：$AA^{-1}=\begin{pmatrix}1&2\\3&4\end{pmatrix}\begin{pmatrix}-2&1\\\frac{3}{2}&-\frac{1}{2}\end{pmatrix}=\begin{pmatrix}-2+3&1-1\\-6+6&3-2\end{pmatrix}=\begin{pmatrix}1&0\\0&1\end{pmatrix}$。

scene_spec.steps[4]

高亮结果：$\det A=-2$；秩为 $2$；$A^{-1}=\begin{pmatrix}-2&1\\\frac{3}{2}&-\frac{1}{2}\end{pmatrix}$

efficiency_tags[0]

单位正方形映射到平行四边形的面积$2$，有向面积为$-2$（定向反转）

efficiency_tags[1]

逆矩阵验证乘法

## eval-linalg-009-s1

problem

用分块方法计算 $M=\begin{pmatrix}2&1&1\\1&2&1\\0&0&3\end{pmatrix}$ 的行列式。

solution

取 $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$，$B=\begin{pmatrix}1\\1\end{pmatrix}$，$C=(3)$，则 $M=\begin{pmatrix}A&B\\0&C\end{pmatrix}$。分块上三角矩阵的行列式 $\det M=\det A\cdot\det C$。$\det A=2\cdot 2-1\cdot 1=3$，$\det C=3$，故 $\det M=3\cdot 3=9$。

answer

$9$

scene_spec.objects[0]

分块结构高亮（$A,B,0,C$）

scene_spec.objects[1]

块上三角与数值上三角的类比

scene_spec.steps[0]

第一步：以分块行列式公式为主线，建立高等代数·矩阵场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：分块结构高亮（$A,B,0,C$）。

scene_spec.steps[2]

第三步：块上三角与数值上三角的类比。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

分块结构高亮（$A,B,0,C$）

efficiency_tags[1]

块上三角与数值上三角的类比

## eval-linalg-009-s2

problem

用分块方法计算 $M=\begin{pmatrix}2&1&1\\1&2&1\\0&0&3\end{pmatrix}$ 的行列式。

solution

按第三行展开：$\det M=(-1)^{3+3}\cdot 3\cdot\begin{vmatrix}2&1\\1&2\end{vmatrix}=3\cdot 3=9$（第三行仅第 3 个元素非零）。这正是分块上三角公式：取左上$2\times2$块$B=\begin{pmatrix}2&1\\1&2\end{pmatrix}$、右下块$C=(3)$，左下为零块，则$\det M=\det B\det C=3\cdot3=9$。

answer

$9$

scene_spec.objects[0]

按第三行展开的 Laplace 余子式高亮

scene_spec.objects[1]

$(-1)^{3+3}\cdot3$ 的符号标注

scene_spec.steps[0]

呈现题干及适用条件：用分块方法计算 $M=\begin{pmatrix}2&1&1\\1&2&1\\0&0&3\end{pmatrix}$ 的行列式。

scene_spec.steps[1]

依次呈现：按第三行展开的 Laplace 余子式高亮

scene_spec.steps[2]

依次呈现：$(-1)^{3+3}\cdot3$ 的符号标注

scene_spec.steps[3]

核对完整证明：按第三行展开：$\det M=(-1)^{3+3}\cdot 3\cdot\begin{vmatrix}2&1\\1&2\end{vmatrix}=3\cdot 3=9$（第三行仅第 3 个元素非零）。这正是分块上三角公式：取左上$2\times2$块$B=\begin{pmatrix}2&1\\1&2\end{pmatrix}$、右下块$C=(3)$，左下为零块，则$\det M=\det B\det C=3\cdot3=9$。

scene_spec.steps[4]

高亮结果：$9$

efficiency_tags[0]

按第三行展开的 Laplace 余子式高亮

efficiency_tags[1]

$(-1)^{3+3}\cdot3$ 的符号标注

## eval-linalg-009-s3

problem

用分块方法计算 $M=\begin{pmatrix}2&1&1\\1&2&1\\0&0&3\end{pmatrix}$ 的行列式。

solution

第三行与第一、二行的前两列零块使 $M$ 已是分块上三角。验证：直接用一般公式展开，$\det M=2\cdot\begin{vmatrix}2&1\\0&3\end{vmatrix}-1\cdot\begin{vmatrix}1&1\\0&3\end{vmatrix}+1\cdot\begin{vmatrix}1&2\\0&0\end{vmatrix}=2\cdot 6-1\cdot 3+1\cdot 0=12-3=9$，与分块公式一致。

answer

$9$

scene_spec.objects[0]

按第一行直接展开的三项计算

scene_spec.objects[1]

与分块公式结果的对照

scene_spec.steps[0]

第一步：以行变换验证为主线，建立高等代数·矩阵场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：按第一行直接展开的三项计算。

scene_spec.steps[2]

第三步：与分块公式结果的对照。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

按第一行直接展开的三项计算

efficiency_tags[1]

与分块公式结果的对照

## eval-linalg-010-s1

problem

求矩阵 $A=\begin{pmatrix}1&1&2\\2&1&3\\1&2&3\end{pmatrix}$ 的秩。

solution

$\begin{pmatrix}1&1&2\\2&1&3\\1&2&3\end{pmatrix}\xrightarrow{R_2-2R_1}\begin{pmatrix}1&1&2\\0&-1&-1\\1&2&3\end{pmatrix}\xrightarrow{R_3-R_1}\begin{pmatrix}1&1&2\\0&-1&-1\\0&1&1\end{pmatrix}\xrightarrow{R_3+R_2}\begin{pmatrix}1&1&2\\0&-1&-1\\0&0&0\end{pmatrix}$。非零行数为 2，故 $\operatorname{rank}A=2$。

answer

$2$

scene_spec.objects[0]

行变换消元动画

scene_spec.objects[1]

非零行数 2 的标注

scene_spec.steps[0]

第一步：以初等行变换为主线，建立高等代数·矩阵场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：行变换消元动画。

scene_spec.steps[2]

第三步：非零行数 2 的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

行变换消元动画

efficiency_tags[1]

非零行数 2 的标注

## eval-linalg-010-s2

problem

求矩阵 $A=\begin{pmatrix}1&1&2\\2&1&3\\1&2&3\end{pmatrix}$ 的秩。

solution

$\det A=1\cdot(1\cdot 3-3\cdot 2)-1\cdot(2\cdot 3-3\cdot 1)+2\cdot(2\cdot 2-1\cdot 1)=1\cdot(-3)-1\cdot 3+2\cdot 3=0$，秩小于 3。二阶子式 $\begin{vmatrix}1&1\\2&1\end{vmatrix}=1-2=-1\ne 0$，故秩为 2。

answer

$2$

scene_spec.objects[0]

三阶行列式为零与二阶子式 $-1\ne0$ 的高亮

scene_spec.objects[1]

秩 2 的判定

scene_spec.steps[0]

第一步：以子式法为主线，建立高等代数·矩阵场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：三阶行列式为零与二阶子式 $-1\ne0$ 的高亮。

scene_spec.steps[2]

第三步：秩 2 的判定。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

三阶行列式为零与二阶子式 $-1\ne0$ 的高亮

efficiency_tags[1]

秩 2 的判定

## eval-linalg-010-s3

problem

求矩阵 $A=\begin{pmatrix}1&1&2\\2&1&3\\1&2&3\end{pmatrix}$ 的秩。

solution

三列 $c_1=(1,2,1)^T$、$c_2=(1,1,2)^T$、$c_3=(2,3,3)^T$ 满足 $c_3=c_1+c_2$（逐分量验证：$1+1=2$，$2+1=3$，$1+2=3$），故 $c_3$ 可由前两列线性表出；$c_1,c_2$ 不成比例，线性无关。列秩 $=2$，即 $\operatorname{rank}A=2$。

answer

$2$

scene_spec.objects[0]

三列向量共面的三维图

scene_spec.objects[1]

列相关关系 $c_3=c_1+c_2$ 的平行四边形

scene_spec.steps[0]

第一步：以列向量组为主线，建立高等代数·矩阵场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：三列向量共面的三维图。

scene_spec.steps[2]

第三步：列相关关系 $c_3=c_1+c_2$ 的平行四边形。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

三列向量共面的三维图

efficiency_tags[1]

列相关关系 $c_3=c_1+c_2$ 的平行四边形

## eval-linalg-011-s1

problem

讨论含参数线性方程组 $\begin{cases}\lambda x+y+z=1\\x+\lambda y+z=\lambda\\x+y+\lambda z=\lambda^2\end{cases}$ 的解的情况。

solution

系数行列式 $D=\begin{vmatrix}\lambda&1&1\\1&\lambda&1\\1&1&\lambda\end{vmatrix}$。该矩阵 $=(\lambda-1)I+J$（$J$ 全 1 矩阵），特征值为 $(\lambda-1)+3=\lambda+2$ 与 $\lambda-1$（二重），故 $D=(\lambda+2)(\lambda-1)^2$。当 $\lambda\ne 1,-2$ 时 $D\ne 0$，由 Cramer 法则有唯一解。当 $\lambda=1$：三个方程均为 $x+y+z=1$，无穷多解（解集为二维仿射平面）。当 $\lambda=-2$：三式相加得 $0\cdot(x+y+z)=1+(-2)+4=3$，即 $0=3$，矛盾，无解。

answer

$\lambda\ne 1$ 且 $\lambda\ne-2$ 时唯一解；$\lambda=1$ 时无穷多解；$\lambda=-2$ 时无解

scene_spec.objects[0]

行列式 $D=(\lambda+2)(\lambda-1)^2$ 的零点标注

scene_spec.objects[1]

三种情形的分屏对照

scene_spec.steps[0]

呈现题干及适用条件：讨论含参数线性方程组 $\begin{cases}\lambda x+y+z=1\\x+\lambda y+z=\lambda\\x+y+\lambda z=\lambda^2\end{cases}$ 的解的情况。

scene_spec.steps[1]

依次呈现：行列式 $D=(\lambda+2)(\lambda-1)^2$ 的零点标注

scene_spec.steps[2]

依次呈现：三种情形的分屏对照

scene_spec.steps[3]

核对完整证明：系数行列式 $D=\begin{vmatrix}\lambda&1&1\\1&\lambda&1\\1&1&\lambda\end{vmatrix}$。该矩阵 $=(\lambda-1)I+J$（$J$ 全 1 矩阵），特征值为 $(\lambda-1)+3=\lambda+2$ 与 $\lambda-1$（二重），故 $D=(\lambda+2)(\lambda-1)^2$。当 $\lambda\ne 1,-2$ 时 $D\ne 0$，由 Cramer 法则有唯一解。当 $\lambda=1$：三个方程均为 $x+y+z=1$，无穷多解（解集为二维仿射平面）。当 $\lambda=-2$：三式相加得 $0\cdot(x+y+z)=1+(-2)+4=3$，即 $0=3$，矛盾，无解。

scene_spec.steps[4]

高亮结果：$\lambda\ne 1$ 且 $\lambda\ne-2$ 时唯一解；$\lambda=1$ 时无穷多解；$\lambda=-2$ 时无解

efficiency_tags[0]

行列式 $D=(\lambda+2)(\lambda-1)^2$ 的零点标注

efficiency_tags[1]

三种情形的分屏对照

## eval-linalg-011-s2

problem

讨论含参数线性方程组 $\begin{cases}\lambda x+y+z=1\\x+\lambda y+z=\lambda\\x+y+\lambda z=\lambda^2\end{cases}$ 的解的情况。

solution

交换第一、三行并消元得$\begin{pmatrix}1&1&\lambda&\lambda^2\\0&\lambda-1&1-\lambda&\lambda-\lambda^2\\0&1-\lambda&1-\lambda^2&1-\lambda^3\end{pmatrix}$。当$\lambda\ne1$，第二行除以$\lambda-1$为$(0,1,-1,-\lambda)$；第三行减去$(1-\lambda)$倍第二行，得到$(0,0,(1-\lambda)(\lambda+2),(1-\lambda)(\lambda+1)^2)$。因此$\lambda\ne1,-2$时三主元均非零，唯一解；$\lambda=-2$时末行为$0=3$，无解。$\lambda=1$时原三式均为$x+y+z=1$，解集为二维仿射平面，有无穷多解。

answer

$\lambda\ne 1$ 且 $\lambda\ne-2$ 时唯一解；$\lambda=1$ 时无穷多解；$\lambda=-2$ 时无解

scene_spec.objects[0]

增广矩阵行变换的逐步动画

scene_spec.objects[1]

矛盾行 $0=3$ 的高亮

scene_spec.steps[0]

呈现题干及适用条件：讨论含参数线性方程组 $\begin{cases}\lambda x+y+z=1\\x+\lambda y+z=\lambda\\x+y+\lambda z=\lambda^2\end{cases}$ 的解的情况。

scene_spec.steps[1]

依次呈现：增广矩阵行变换的逐步动画

scene_spec.steps[2]

依次呈现：矛盾行 $0=3$ 的高亮

scene_spec.steps[3]

核对完整证明：交换第一、三行并消元得$\begin{pmatrix}1&1&\lambda&\lambda^2\\0&\lambda-1&1-\lambda&\lambda-\lambda^2\\0&1-\lambda&1-\lambda^2&1-\lambda^3\end{pmatrix}$。当$\lambda\ne1$，第二行除以$\lambda-1$为$(0,1,-1,-\lambda)$；第三行减去$(1-\lambda)$倍第二行，得到$(0,0,(1-\lambda)(\lambda+2),(1-\lambda)(\lambda+1)^2)$。因此$\lambda\ne1,-2$时三主元均非零，唯一解；$\lambda=-2$时末行为$0=3$，无解。$\lambda=1$时原三式均为$x+y+z=1$，解集为二维仿射平面，有无穷多解。

scene_spec.steps[4]

高亮结果：$\lambda\ne 1$ 且 $\lambda\ne-2$ 时唯一解；$\lambda=1$ 时无穷多解；$\lambda=-2$ 时无解

efficiency_tags[0]

增广矩阵行变换的逐步动画

efficiency_tags[1]

矛盾行 $0=3$ 的高亮

## eval-linalg-011-s3

problem

讨论含参数线性方程组 $\begin{cases}\lambda x+y+z=1\\x+\lambda y+z=\lambda\\x+y+\lambda z=\lambda^2\end{cases}$ 的解的情况。

solution

三个方程代表三个平面。$\lambda=1$ 时三平面重合（$x+y+z=1$）；$\lambda=-2$ 时三平面两两相交但三交线平行（法向量和为零向量导致矛盾）；其余情形三平面交于一点（唯一解）。代数依据：法向量矩阵为$(\lambda-1)I+J$，行列式$(\lambda-1)^2(\lambda+2)$，在$\lambda\ne1,-2$可逆，所以三平面唯一公共点；$\lambda=-2$时三式相加左侧为0、右侧为$1-2+4=3$，故无公共点，各法向量两两不成比例且叉积均沿$(1,1,1)$，三条两两交线平行；$\lambda=1$时代入即为同一个平面。

answer

$\lambda\ne 1$ 且 $\lambda\ne-2$ 时唯一解；$\lambda=1$ 时无穷多解；$\lambda=-2$ 时无解

scene_spec.objects[0]

$\lambda$ 滑块下三平面的位置变化

scene_spec.objects[1]

重合/交于一点/无公共点的三种几何

scene_spec.steps[0]

呈现题干及适用条件：讨论含参数线性方程组 $\begin{cases}\lambda x+y+z=1\\x+\lambda y+z=\lambda\\x+y+\lambda z=\lambda^2\end{cases}$ 的解的情况。

scene_spec.steps[1]

依次呈现：$\lambda$ 滑块下三平面的位置变化

scene_spec.steps[2]

依次呈现：重合/交于一点/无公共点的三种几何

scene_spec.steps[3]

核对完整证明：三个方程代表三个平面。$\lambda=1$ 时三平面重合（$x+y+z=1$）；$\lambda=-2$ 时三平面两两相交但三交线平行（法向量和为零向量导致矛盾）；其余情形三平面交于一点（唯一解）。代数依据：法向量矩阵为$(\lambda-1)I+J$，行列式$(\lambda-1)^2(\lambda+2)$，在$\lambda\ne1,-2$可逆，所以三平面唯一公共点；$\lambda=-2$时三式相加左侧为0、右侧为$1-2+4=3$，故无公共点，各法向量两两不成比例且叉积均沿$(1,1,1)$，三条两两交线平行；$\lambda=1$时代入即为同一个平面。

scene_spec.steps[4]

高亮结果：$\lambda\ne 1$ 且 $\lambda\ne-2$ 时唯一解；$\lambda=1$ 时无穷多解；$\lambda=-2$ 时无解

efficiency_tags[0]

$\lambda$ 滑块下三平面的位置变化

efficiency_tags[1]

重合/交于一点/无公共点的三种几何

## eval-linalg-012-s1

problem

求参数 $a$ 使齐次线性方程组 $\begin{cases}ax+y+z=0\\x+ay+z=0\\x+y+az=0\end{cases}$ 有非零解，并求各情形下的解空间。

solution

系数行列式 $D=\begin{vmatrix}a&1&1\\1&a&1\\1&1&a\end{vmatrix}$。矩阵 $=(a-1)I+J$，特征值 $a+2$ 与 $a-1$（二重），故 $D=(a+2)(a-1)^2$。齐次方程组有非零解 $\iff D=0\iff a=1$ 或 $a=-2$。$a=1$：三个方程均为 $x+y+z=0$，解空间为二维平面。$a=-2$：三式相加得 $-2(x+y+z)+2(x+y+z)=0$ 恒等，且 $\begin{cases}-2x+y+z=0\\x-2y+z=0\end{cases}$ 相减得 $x=y$，代回得 $z=x$，解空间为直线 $x=y=z$（一维）。

answer

$a=1$（解空间二维：$x+y+z=0$）或 $a=-2$（解空间一维：$x=y=z$）

scene_spec.objects[0]

行列式 $D=(a+2)(a-1)^2$ 的零点标注

scene_spec.objects[1]

非零解条件的判定

scene_spec.steps[0]

第一步：以行列式为零为主线，建立高等代数·线性方程组场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：行列式 $D=(a+2)(a-1)^2$ 的零点标注。

scene_spec.steps[2]

第三步：非零解条件的判定。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

行列式 $D=(a+2)(a-1)^2$ 的零点标注

efficiency_tags[1]

非零解条件的判定

## eval-linalg-012-s2

problem

求参数 $a$ 使齐次线性方程组 $\begin{cases}ax+y+z=0\\x+ay+z=0\\x+y+az=0\end{cases}$ 有非零解，并求各情形下的解空间。

solution

矩阵$(a-1)I+J$的行列式为$(a-1)^2(a+2)$，$a\ne1,-2$时秩3，只有零解。$a=1$时全1矩阵秩1，核为$x+y+z=0$，维数2。$a=-2$时每行和为0，秩不超过2；左上二阶子式为$4-1=3\ne0$，故秩恰2。第一式减第二式为$-3x+3y=0$，再代回得$z=x$，故核为$\operatorname{span}\{(1,1,1)^T\}$，维数1。

answer

$a=1$（解空间二维：$x+y+z=0$）或 $a=-2$（解空间一维：$x=y=z$）

scene_spec.objects[0]

秩随 $a$ 的变化标注

scene_spec.objects[1]

解空间维度 $3-r$ 的对应

scene_spec.steps[0]

呈现题干及适用条件：求参数 $a$ 使齐次线性方程组 $\begin{cases}ax+y+z=0\\x+ay+z=0\\x+y+az=0\end{cases}$ 有非零解，并求各情形下的解空间。

scene_spec.steps[1]

依次呈现：秩随 $a$ 的变化标注

scene_spec.steps[2]

依次呈现：解空间维度 $3-r$ 的对应

scene_spec.steps[3]

核对完整证明：矩阵$(a-1)I+J$的行列式为$(a-1)^2(a+2)$，$a\ne1,-2$时秩3，只有零解。$a=1$时全1矩阵秩1，核为$x+y+z=0$，维数2。$a=-2$时每行和为0，秩不超过2；左上二阶子式为$4-1=3\ne0$，故秩恰2。第一式减第二式为$-3x+3y=0$，再代回得$z=x$，故核为$\operatorname{span}\{(1,1,1)^T\}$，维数1。

scene_spec.steps[4]

高亮结果：$a=1$（解空间二维：$x+y+z=0$）或 $a=-2$（解空间一维：$x=y=z$）

efficiency_tags[0]

秩随 $a$ 的变化标注

efficiency_tags[1]

解空间维度 $3-r$ 的对应

## eval-linalg-012-s3

problem

求参数 $a$ 使齐次线性方程组 $\begin{cases}ax+y+z=0\\x+ay+z=0\\x+y+az=0\end{cases}$ 有非零解，并求各情形下的解空间。

solution

方程组 $((a-1)I+J)v=0$ 有非零解 $\iff -(a-1)$ 是 $J$ 的特征值。$J$ 的特征值为 $3,0,0$，故 $a-1\in\{-3,0\}$，即 $a=-2$ 或 $a=1$，与解法一一致。$a=-2$ 时解为 $J$ 的特征值 $3$ 对应的特征向量方向 $(1,1,1)^T$；$a=1$ 时解为 $J$ 的零空间（$x+y+z=0$，二维）。

answer

$a=1$（解空间二维：$x+y+z=0$）或 $a=-2$（解空间一维：$x=y=z$）

scene_spec.objects[0]

矩阵谱与 $a$ 的关系图

scene_spec.objects[1]

解直线/解平面的三维展示

scene_spec.steps[0]

第一步：以特征值观点为主线，建立高等代数·线性方程组场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：矩阵谱与 $a$ 的关系图。

scene_spec.steps[2]

第三步：解直线/解平面的三维展示。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

矩阵谱与 $a$ 的关系图

efficiency_tags[1]

解直线/解平面的三维展示

## eval-linalg-013-s1

problem

求齐次线性方程组 $x_1+x_2+x_3+x_4=0$ 的基础解系与通解。

solution

取 $x_2,x_3,x_4$ 为自由变量，$x_1=-x_2-x_3-x_4$。分别令 $(x_2,x_3,x_4)=(1,0,0),(0,1,0),(0,0,1)$，得基础解系 $\xi_1=(-1,1,0,0)^T$，$\xi_2=(-1,0,1,0)^T$，$\xi_3=(-1,0,0,1)^T$（取负号即 $\xi_1=(1,-1,0,0)^T$ 等形式，两者等价）。通解 $x=c_1\xi_1+c_2\xi_2+c_3\xi_3$。

answer

基础解系 $\xi_1=(1,-1,0,0)^T$，$\xi_2=(1,0,-1,0)^T$，$\xi_3=(1,0,0,-1)^T$；通解 $x=c_1\xi_1+c_2\xi_2+c_3\xi_3$

scene_spec.objects[0]

自由变量 $(x_2,x_3,x_4)$ 的三组赋值

scene_spec.objects[1]

三个解向量的生成

scene_spec.steps[0]

第一步：以自由变量法为主线，建立高等代数·线性方程组场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：自由变量 $(x_2,x_3,x_4)$ 的三组赋值。

scene_spec.steps[2]

第三步：三个解向量的生成。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

自由变量 $(x_2,x_3,x_4)$ 的三组赋值

efficiency_tags[1]

三个解向量的生成

## eval-linalg-013-s2

problem

求齐次线性方程组 $x_1+x_2+x_3+x_4=0$ 的基础解系与通解。

solution

解空间 $=(\operatorname{span}\{(1,1,1,1)^T\})^\perp$（法向量 $(1,1,1,1)$ 的正交补）。取三个线性无关且与 $(1,1,1,1)$ 正交的向量：$(1,-1,0,0)^T$、$(1,0,-1,0)^T$、$(1,0,0,-1)^T$（逐一点积为 0）。三者线性无关（前三个分量的子矩阵 $\begin{pmatrix}1&-1&0\\1&0&-1\\1&0&0\end{pmatrix}$ 行列式 $1\ne 0$），故构成基础解系。

answer

基础解系 $\xi_1=(1,-1,0,0)^T$，$\xi_2=(1,0,-1,0)^T$，$\xi_3=(1,0,0,-1)^T$；通解 $x=c_1\xi_1+c_2\xi_2+c_3\xi_3$

scene_spec.objects[0]

三个基向量与法向量 $(1,1,1,1)$ 的正交关系

scene_spec.objects[1]

线性无关性的行列式验证

scene_spec.steps[0]

第一步：以正交补观点为主线，建立高等代数·线性方程组场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：三个基向量与法向量 $(1,1,1,1)$ 的正交关系。

scene_spec.steps[2]

第三步：线性无关性的行列式验证。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

三个基向量与法向量 $(1,1,1,1)$ 的正交关系

efficiency_tags[1]

线性无关性的行列式验证

## eval-linalg-013-s3

problem

求齐次线性方程组 $x_1+x_2+x_3+x_4=0$ 的基础解系与通解。

solution

方程 $x_1+x_2+x_3+x_4=0$ 是 $\mathbb R^4$ 中过原点的三维超平面（法向量 $(1,1,1,1)$）。基础解系即该超平面的一个基，通解是超平面上所有点。维数 $4-1=3$ 与基础解系含 3 个向量一致。具体取$\xi_1=(1,-1,0,0)^T,\xi_2=(1,0,-1,0)^T,\xi_3=(1,0,0,-1)^T$；它们都满足方程，且后三个分量直接保证线性无关。任意解$x$满足$x_1=-x_2-x_3-x_4$，所以$x=-x_2\xi_1-x_3\xi_2-x_4\xi_3$，给出完整通解。

answer

基础解系 $\xi_1=(1,-1,0,0)^T$，$\xi_2=(1,0,-1,0)^T$，$\xi_3=(1,0,0,-1)^T$；通解 $x=c_1\xi_1+c_2\xi_2+c_3\xi_3$

scene_spec.objects[0]

三维投影中的超平面

scene_spec.objects[1]

通解的线性组合扫出平面

scene_spec.steps[0]

呈现题干及适用条件：求齐次线性方程组 $x_1+x_2+x_3+x_4=0$ 的基础解系与通解。

scene_spec.steps[1]

依次呈现：三维投影中的超平面

scene_spec.steps[2]

依次呈现：通解的线性组合扫出平面

scene_spec.steps[3]

核对完整证明：方程 $x_1+x_2+x_3+x_4=0$ 是 $\mathbb R^4$ 中过原点的三维超平面（法向量 $(1,1,1,1)$）。基础解系即该超平面的一个基，通解是超平面上所有点。维数 $4-1=3$ 与基础解系含 3 个向量一致。具体取$\xi_1=(1,-1,0,0)^T,\xi_2=(1,0,-1,0)^T,\xi_3=(1,0,0,-1)^T$；它们都满足方程，且后三个分量直接保证线性无关。任意解$x$满足$x_1=-x_2-x_3-x_4$，所以$x=-x_2\xi_1-x_3\xi_2-x_4\xi_3$，给出完整通解。

scene_spec.steps[4]

高亮结果：基础解系 $\xi_1=(1,-1,0,0)^T$，$\xi_2=(1,0,-1,0)^T$，$\xi_3=(1,0,0,-1)^T$；通解 $x=c_1\xi_1+c_2\xi_2+c_3\xi_3$

efficiency_tags[0]

三维投影中的超平面

efficiency_tags[1]

通解的线性组合扫出平面

## eval-linalg-014-s1

problem

设 $a\in\mathbb R\setminus\{0\}$ 为参数,求矩阵 $A=\begin{pmatrix}1&a&0\\a&1&a\\0&a&1\end{pmatrix}$ 的特征值与特征向量,并求正交矩阵 $Q$,使 $Q^TAQ$ 为对角矩阵。

solution

$|\lambda I-A|=\begin{vmatrix}\lambda-1&-a&0\\-a&\lambda-1&-a\\0&-a&\lambda-1\end{vmatrix}=(\lambda-1)\bigl[(\lambda-1)^2-2a^2\bigr]$,得特征值 $1,\ 1\pm\sqrt{2}a$($a\neq 0$ 时互异)。$\lambda=1$:解 $(A-I)v=0$,即 $\begin{pmatrix}0&a&0\\a&0&a\\0&a&0\end{pmatrix}v=0$,得 $y=0,\ x=-z$,取 $v_1=(1,0,-1)^T$。$\lambda=1+\sqrt{2}a$:由 $(A-(1+\sqrt{2}a)I)v=0$,第一行给 $y=\sqrt{2}x$,第二行给 $x-\sqrt{2}y+z=0$,故 $z=x$,取 $v_2=(1,\sqrt{2},1)^T$。$\lambda=1-\sqrt{2}a$:同理 $y=-\sqrt{2}x,\ z=x$,取 $v_3=(1,-\sqrt{2},1)^T$。三个特征向量两两正交,范数分别为 $\sqrt{2},\ 2,\ 2$;单位化后按列排成 $Q=\begin{pmatrix}1/\sqrt{2}&1/2&1/2\\0&\sqrt{2}/2&-\sqrt{2}/2\\-1/\sqrt{2}&1/2&1/2\end{pmatrix}$。直接验证:$AQ=Q\operatorname{diag}(1,1+\sqrt{2}a,1-\sqrt{2}a)$(逐列即 $Av_i=\lambda_i v_i$),故 $Q^TAQ=\operatorname{diag}(1,\,1+\sqrt{2}a,\,1-\sqrt{2}a)$。

answer

特征值 $1,\ 1+\sqrt{2}a,\ 1-\sqrt{2}a$;对应单位特征向量 $\dfrac{1}{\sqrt{2}}(1,0,-1)^T,\ \dfrac{1}{2}(1,\sqrt{2},1)^T,\ \dfrac{1}{2}(1,-\sqrt{2},1)^T$;$Q=\begin{pmatrix}1/\sqrt{2}&1/2&1/2\\0&\sqrt{2}/2&-\sqrt{2}/2\\-1/\sqrt{2}&1/2&1/2\end{pmatrix}$,$Q^TAQ=\operatorname{diag}(1,\,1+\sqrt{2}a,\,1-\sqrt{2}a)$

scene_spec.objects[0]

三阶特征多项式按第一列展开与因式分解

scene_spec.objects[1]

三个特征方向上伸缩率 $1,\ 1\pm\sqrt{2}a$ 的标注

scene_spec.steps[0]

第一步：以特征方程为主线，建立高等代数·特征值与特征向量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：三阶特征多项式按第一列展开与因式分解。

scene_spec.steps[2]

第三步：三个特征方向上伸缩率 $1,\ 1\pm\sqrt{2}a$ 的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

三阶特征多项式按第一列展开与因式分解

efficiency_tags[1]

三个特征方向上伸缩率 $1,\ 1\pm\sqrt{2}a$ 的标注

## eval-linalg-014-s2

problem

设 $a\in\mathbb R\setminus\{0\}$ 为参数,求矩阵 $A=\begin{pmatrix}1&a&0\\a&1&a\\0&a&1\end{pmatrix}$ 的特征值与特征向量,并求正交矩阵 $Q$,使 $Q^TAQ$ 为对角矩阵。

solution

先看反对称方向:$A(1,0,-1)^T=(1,0,-1)^T$,故 $v_1=(1,0,-1)^T$ 是特征值 1 的特征向量。其余特征向量在 $v_1$ 的正交补 $\operatorname{span}\{r,s\}$ 内,其中 $r=\dfrac{1}{\sqrt{2}}(1,0,1)^T,\ s=(0,1,0)^T$ 为单位正交基。计算 $A$ 在 $(r,s)$ 上的限制:$Ar=\dfrac{1}{\sqrt{2}}A(1,0,1)^T=\dfrac{1}{\sqrt{2}}(1,2a,1)^T=r+\sqrt{2}a\,s$;$As=A(0,1,0)^T=(a,1,a)^T=\sqrt{2}a\,r+s$。故限制矩阵为 $\begin{pmatrix}1&\sqrt{2}a\\\sqrt{2}a&1\end{pmatrix}$,其特征值为 $1\pm\sqrt{2}a$,对应特征向量 $r\pm s$,即 $v_2=\dfrac{1}{2}(1,\sqrt{2},1)^T$,$v_3=\dfrac{1}{2}(1,-\sqrt{2},1)^T$。三向量两两正交,单位化后按列排成 $Q=\begin{pmatrix}1/\sqrt{2}&1/2&1/2\\0&\sqrt{2}/2&-\sqrt{2}/2\\-1/\sqrt{2}&1/2&1/2\end{pmatrix}$,$Q^TAQ=\operatorname{diag}(1,\,1+\sqrt{2}a,\,1-\sqrt{2}a)$。

answer

特征值 $1,\ 1+\sqrt{2}a,\ 1-\sqrt{2}a$;对应单位特征向量 $\dfrac{1}{\sqrt{2}}(1,0,-1)^T,\ \dfrac{1}{2}(1,\sqrt{2},1)^T,\ \dfrac{1}{2}(1,-\sqrt{2},1)^T$;$Q=\begin{pmatrix}1/\sqrt{2}&1/2&1/2\\0&\sqrt{2}/2&-\sqrt{2}/2\\-1/\sqrt{2}&1/2&1/2\end{pmatrix}$,$Q^TAQ=\operatorname{diag}(1,\,1+\sqrt{2}a,\,1-\sqrt{2}a)$

scene_spec.objects[0]

反对称方向 $v_1$ 先分离、正交补 $r,s$ 上的 2 阶限制

scene_spec.objects[1]

$r\pm s$ 生成另两个特征方向的动画

scene_spec.steps[0]

第一步：以对称结构分解为主线，建立高等代数·特征值与特征向量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：反对称方向 $v_1$ 先分离、正交补 $r,s$ 上的 2 阶限制。

scene_spec.steps[2]

第三步：$r\pm s$ 生成另两个特征方向的动画。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

反对称方向 $v_1$ 先分离、正交补 $r,s$ 上的 2 阶限制

efficiency_tags[1]

$r\pm s$ 生成另两个特征方向的动画

## eval-linalg-014-s3

problem

设 $a\in\mathbb R\setminus\{0\}$ 为参数,求矩阵 $A=\begin{pmatrix}1&a&0\\a&1&a\\0&a&1\end{pmatrix}$ 的特征值与特征向量,并求正交矩阵 $Q$,使 $Q^TAQ$ 为对角矩阵。

solution

二次型 $f(x,y,z)=x^2+y^2+z^2+2a(xy+yz)$。令 $u=\dfrac{x-z}{\sqrt{2}},\ p=\dfrac{x+z}{\sqrt{2}}$,则 $x^2+z^2=u^2+p^2$,$xy+yz=y(x+z)=\sqrt{2}py$,故 $f=u^2+p^2+y^2+2\sqrt{2}a\,py$。再令 $v=\dfrac{p+y}{\sqrt{2}},\ w=\dfrac{p-y}{\sqrt{2}}$,则 $p^2+y^2=v^2+w^2$,$2py=v^2-w^2$,故 $f=u^2+(1+\sqrt{2}a)v^2+(1-\sqrt{2}a)w^2$——三项系数即特征值。由 $(u,v,w)^T=P(x,y,z)^T$ 解出 $P=\begin{pmatrix}1/\sqrt{2}&0&-1/\sqrt{2}\\1/2&\sqrt{2}/2&1/2\\1/2&-\sqrt{2}/2&1/2\end{pmatrix}$,$Q=P^T$ 即为所求正交矩阵。参数分类($f=1$ 等值面):$|a|<\dfrac{\sqrt{2}}{2}$ 时三系数全正,为椭球面;$a=\pm\dfrac{\sqrt{2}}{2}$ 时一个系数为 0,退化为椭圆柱面;$|a|>\dfrac{\sqrt{2}}{2}$ 时一个系数为负,为单叶双曲面。

answer

特征值 $1,\ 1+\sqrt{2}a,\ 1-\sqrt{2}a$;对应单位特征向量 $\dfrac{1}{\sqrt{2}}(1,0,-1)^T,\ \dfrac{1}{2}(1,\sqrt{2},1)^T,\ \dfrac{1}{2}(1,-\sqrt{2},1)^T$;$Q=\begin{pmatrix}1/\sqrt{2}&1/2&1/2\\0&\sqrt{2}/2&-\sqrt{2}/2\\-1/\sqrt{2}&1/2&1/2\end{pmatrix}$,$Q^TAQ=\operatorname{diag}(1,\,1+\sqrt{2}a,\,1-\sqrt{2}a)$

scene_spec.objects[0]

两次正交替换 $u,p\to v,w$ 的配方动画

scene_spec.objects[1]

$f=1$ 等值面随 $a$ 的类型切换(椭球/椭圆柱/单叶双曲面)

scene_spec.steps[0]

第一步：以直接主轴配方为主线，建立高等代数·特征值与特征向量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：两次正交替换 $u,p\to v,w$ 的配方动画。

scene_spec.steps[2]

第三步：$f=1$ 等值面随 $a$ 的类型切换(椭球/椭圆柱/单叶双曲面)。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

两次正交替换 $u,p\to v,w$ 的配方动画

efficiency_tags[1]

$f=1$ 等值面随 $a$ 的类型切换(椭球/椭圆柱/单叶双曲面)

## eval-linalg-015-s1

problem

求矩阵 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$ 的特征值与特征向量，并将其对角化。

solution

$|\lambda I-A|=\begin{vmatrix}\lambda-1&-2\\-2&\lambda-1\end{vmatrix}=(\lambda-1)^2-4=\lambda^2-2\lambda-3=(\lambda-3)(\lambda+1)$，$\lambda=3,-1$。$\lambda=3$：$(3I-A)v=0$，即 $\begin{pmatrix}2&-2\\-2&2\end{pmatrix}v=0$，$v=(1,1)^T$。$\lambda=-1$：$(-I-A)v=0$，即 $\begin{pmatrix}-2&-2\\-2&-2\end{pmatrix}v=0$，$v=(1,-1)^T$。取$P=((1,1)^T,(1,-1)^T)=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$，$\det P=-2\ne0$，逐列有$AP=P\operatorname{diag}(3,-1)$，故$P^{-1}AP=\operatorname{diag}(3,-1)$。

answer

特征值 $\lambda_1=3$、$\lambda_2=-1$；特征向量 $(1,1)^T$、$(1,-1)^T$；$P^{-1}AP=\begin{pmatrix}3&0\\0&-1\end{pmatrix}$，其中 $P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$

scene_spec.objects[0]

特征方程 $(\lambda-3)(\lambda+1)=0$ 的求解

scene_spec.objects[1]

特征向量的拉伸（3 倍与反向）

scene_spec.steps[0]

呈现题干及适用条件：求矩阵 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$ 的特征值与特征向量，并将其对角化。

scene_spec.steps[1]

依次呈现：特征方程 $(\lambda-3)(\lambda+1)=0$ 的求解

scene_spec.steps[2]

依次呈现：特征向量的拉伸（3 倍与反向）

scene_spec.steps[3]

核对完整证明：$|\lambda I-A|=\begin{vmatrix}\lambda-1&-2\\-2&\lambda-1\end{vmatrix}=(\lambda-1)^2-4=\lambda^2-2\lambda-3=(\lambda-3)(\lambda+1)$，$\lambda=3,-1$。$\lambda=3$：$(3I-A)v=0$，即 $\begin{pmatrix}2&-2\\-2&2\end{pmatrix}v=0$，$v=(1,1)^T$。$\lambda=-1$：$(-I-A)v=0$，即 $\begin{pmatrix}-2&-2\\-2&-2\end{pmatrix}v=0$，$v=(1,-1)^T$。取$P=((1,1)^T,(1,-1)^T)=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$，$\det P=-2\ne0$，逐列有$AP=P\operatorname{diag}(3,-1)$，故$P^{-1}AP=\operatorname{diag}(3,-1)$。

scene_spec.steps[4]

高亮结果：特征值 $\lambda_1=3$、$\lambda_2=-1$；特征向量 $(1,1)^T$、$(1,-1)^T$；$P^{-1}AP=\begin{pmatrix}3&0\\0&-1\end{pmatrix}$，其中 $P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$

efficiency_tags[0]

特征方程 $(\lambda-3)(\lambda+1)=0$ 的求解

efficiency_tags[1]

特征向量的拉伸（3 倍与反向）

## eval-linalg-015-s2

problem

求矩阵 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$ 的特征值与特征向量，并将其对角化。

solution

令$u=(x+y)/\sqrt2,\ v=(x-y)/\sqrt2$，逆变换$x=(u+v)/\sqrt2,\ y=(u-v)/\sqrt2$。则$x^2+y^2=u^2+v^2$、$4xy=2u^2-2v^2$，所以$f=3u^2-v^2$。对应正交矩阵$Q=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$满足$Q^TAQ=\operatorname{diag}(3,-1)$，列向量分别是特征值$3,-1$的单位特征向量。等价地取$P=\sqrt2Q$，有$P^{-1}AP=\operatorname{diag}(3,-1)$。

answer

特征值 $\lambda_1=3$、$\lambda_2=-1$；特征向量 $(1,1)^T$、$(1,-1)^T$；$P^{-1}AP=\begin{pmatrix}3&0\\0&-1\end{pmatrix}$，其中 $P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$

scene_spec.objects[0]

二次型 $x^2+4xy+y^2$ 的等值线与主轴

scene_spec.objects[1]

主轴方向取值的标注

scene_spec.steps[0]

呈现题干及适用条件：求矩阵 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$ 的特征值与特征向量，并将其对角化。

scene_spec.steps[1]

依次呈现：二次型 $x^2+4xy+y^2$ 的等值线与主轴

scene_spec.steps[2]

依次呈现：主轴方向取值的标注

scene_spec.steps[3]

核对完整证明：令$u=(x+y)/\sqrt2,\ v=(x-y)/\sqrt2$，逆变换$x=(u+v)/\sqrt2,\ y=(u-v)/\sqrt2$。则$x^2+y^2=u^2+v^2$、$4xy=2u^2-2v^2$，所以$f=3u^2-v^2$。对应正交矩阵$Q=\frac1{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$满足$Q^TAQ=\operatorname{diag}(3,-1)$，列向量分别是特征值$3,-1$的单位特征向量。等价地取$P=\sqrt2Q$，有$P^{-1}AP=\operatorname{diag}(3,-1)$。

scene_spec.steps[4]

高亮结果：特征值 $\lambda_1=3$、$\lambda_2=-1$；特征向量 $(1,1)^T$、$(1,-1)^T$；$P^{-1}AP=\begin{pmatrix}3&0\\0&-1\end{pmatrix}$，其中 $P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$

efficiency_tags[0]

二次型 $x^2+4xy+y^2$ 的等值线与主轴

efficiency_tags[1]

主轴方向取值的标注

## eval-linalg-015-s3

problem

求矩阵 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$ 的特征值与特征向量，并将其对角化。

solution

归一化特征向量 $q_1=\dfrac{1}{\sqrt2}(1,1)^T$、$q_2=\dfrac{1}{\sqrt2}(1,-1)^T$（自动正交），取 $Q=\dfrac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$（$Q$ 为正交矩阵，$Q^{-1}=Q^T$）。$Q^TAQ=\begin{pmatrix}3&0\\0&-1\end{pmatrix}$，验证：$Q^TAQ=\dfrac{1}{2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}\begin{pmatrix}1&2\\2&1\end{pmatrix}\begin{pmatrix}1&1\\1&-1\end{pmatrix}=\dfrac{1}{2}\begin{pmatrix}3&3\\-1&1\end{pmatrix}\begin{pmatrix}1&1\\1&-1\end{pmatrix}=\dfrac{1}{2}\begin{pmatrix}6&0\\0&-2\end{pmatrix}$。

answer

特征值 $\lambda_1=3$、$\lambda_2=-1$；特征向量 $(1,1)^T$、$(1,-1)^T$；$P^{-1}AP=\begin{pmatrix}3&0\\0&-1\end{pmatrix}$，其中 $P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$

scene_spec.objects[0]

正交矩阵$Q$的基变换（$\det Q=-1$，包含反射）

scene_spec.objects[1]

$Q^TAQ=\operatorname{diag}(3,-1)$ 的矩阵运算

scene_spec.steps[0]

呈现题干及适用条件：求矩阵 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$ 的特征值与特征向量，并将其对角化。

scene_spec.steps[1]

依次呈现：正交矩阵$Q$的基变换（$\det Q=-1$，包含反射）

scene_spec.steps[2]

依次呈现：$Q^TAQ=\operatorname{diag}(3,-1)$ 的矩阵运算

scene_spec.steps[3]

核对完整证明：归一化特征向量 $q_1=\dfrac{1}{\sqrt2}(1,1)^T$、$q_2=\dfrac{1}{\sqrt2}(1,-1)^T$（自动正交），取 $Q=\dfrac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$（$Q$ 为正交矩阵，$Q^{-1}=Q^T$）。$Q^TAQ=\begin{pmatrix}3&0\\0&-1\end{pmatrix}$，验证：$Q^TAQ=\dfrac{1}{2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}\begin{pmatrix}1&2\\2&1\end{pmatrix}\begin{pmatrix}1&1\\1&-1\end{pmatrix}=\dfrac{1}{2}\begin{pmatrix}3&3\\-1&1\end{pmatrix}\begin{pmatrix}1&1\\1&-1\end{pmatrix}=\dfrac{1}{2}\begin{pmatrix}6&0\\0&-2\end{pmatrix}$。

scene_spec.steps[4]

高亮结果：特征值 $\lambda_1=3$、$\lambda_2=-1$；特征向量 $(1,1)^T$、$(1,-1)^T$；$P^{-1}AP=\begin{pmatrix}3&0\\0&-1\end{pmatrix}$，其中 $P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$

efficiency_tags[0]

正交矩阵$Q$的基变换（$\det Q=-1$，包含反射）

efficiency_tags[1]

$Q^TAQ=\operatorname{diag}(3,-1)$ 的矩阵运算

## eval-linalg-016-s1

problem

设 $A$ 为二阶方阵，已知 $\operatorname{tr}A=5$、$\det A=6$。求 $A$ 的特征值，并验证 $A^2-5A+6I=0$。

solution

特征多项式 $|\lambda I-A|=\lambda^2-(\operatorname{tr}A)\lambda+\det A=\lambda^2-5\lambda+6=(\lambda-2)(\lambda-3)$，特征值为 $2,3$。一般二阶矩阵满足Cayley–Hamilton定理，将$p(\lambda)=\lambda^2-5\lambda+6$代入即得$p(A)=A^2-5A+6I=0$；这对所有满足给定迹与行列式的矩阵成立。

answer

特征值为 $2$ 与 $3$；$A^2-5A+6I=0$ 成立

scene_spec.objects[0]

特征多项式 $\lambda^2-5\lambda+6$ 系数与迹、行列式的对应

scene_spec.objects[1]

因式分解 $(\lambda-2)(\lambda-3)$

scene_spec.steps[0]

呈现题干及适用条件：设 $A$ 为二阶方阵，已知 $\operatorname{tr}A=5$、$\det A=6$。求 $A$ 的特征值，并验证 $A^2-5A+6I=0$。

scene_spec.steps[1]

依次呈现：特征多项式 $\lambda^2-5\lambda+6$ 系数与迹、行列式的对应

scene_spec.steps[2]

依次呈现：因式分解 $(\lambda-2)(\lambda-3)$

scene_spec.steps[3]

核对完整证明：特征多项式 $|\lambda I-A|=\lambda^2-(\operatorname{tr}A)\lambda+\det A=\lambda^2-5\lambda+6=(\lambda-2)(\lambda-3)$，特征值为 $2,3$。一般二阶矩阵满足Cayley–Hamilton定理，将$p(\lambda)=\lambda^2-5\lambda+6$代入即得$p(A)=A^2-5A+6I=0$；这对所有满足给定迹与行列式的矩阵成立。

scene_spec.steps[4]

高亮结果：特征值为 $2$ 与 $3$；$A^2-5A+6I=0$ 成立

efficiency_tags[0]

特征多项式 $\lambda^2-5\lambda+6$ 系数与迹、行列式的对应

efficiency_tags[1]

因式分解 $(\lambda-2)(\lambda-3)$

## eval-linalg-016-s2

problem

设 $A$ 为二阶方阵，已知 $\operatorname{tr}A=5$、$\det A=6$。求 $A$ 的特征值，并验证 $A^2-5A+6I=0$。

solution

由特征多项式 $p(\lambda)=\lambda^2-5\lambda+6$，Cayley–Hamilton 定理给出 $p(A)=A^2-5A+6I=0$。验证特例 $A=\begin{pmatrix}2&1\\0&3\end{pmatrix}$（$\operatorname{tr}=5$、$\det=6$）：$A^2=\begin{pmatrix}4&5\\0&9\end{pmatrix}$，$A^2-5A+6I=\begin{pmatrix}4-10+6&5-5\\0&9-15+6\end{pmatrix}=0$。

answer

特征值为 $2$ 与 $3$；$A^2-5A+6I=0$ 成立

scene_spec.objects[0]

Cayley–Hamilton 定理的陈述

scene_spec.objects[1]

特例 $\begin{pmatrix}2&1\\0&3\end{pmatrix}$ 的 $A^2-5A+6I=0$ 矩阵运算动画

scene_spec.steps[0]

第一步：以Cayley–Hamilton 定理为主线，建立高等代数·特征值与特征向量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：Cayley–Hamilton 定理的陈述。

scene_spec.steps[2]

第三步：特例 $\begin{pmatrix}2&1\\0&3\end{pmatrix}$ 的 $A^2-5A+6I=0$ 矩阵运算动画。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

Cayley–Hamilton 定理的陈述

efficiency_tags[1]

特例 $\begin{pmatrix}2&1\\0&3\end{pmatrix}$ 的 $A^2-5A+6I=0$ 矩阵运算动画

## eval-linalg-016-s3

problem

设 $A$ 为二阶方阵，已知 $\operatorname{tr}A=5$、$\det A=6$。求 $A$ 的特征值，并验证 $A^2-5A+6I=0$。

solution

迹与行列式是相似不变量，特征值由迹与行列式唯一确定为 $2,3$。由两个不同特征值知 $A$ 可对角化（最小多项式 $(\lambda-2)(\lambda-3)$ 无重根），即 $A=P\operatorname{diag}(2,3)P^{-1}$。于是 $A^2-5A+6I=P\left(\operatorname{diag}(4,9)-5\operatorname{diag}(2,3)+6I\right)P^{-1}=P\cdot 0\cdot P^{-1}=0$，与解法二一致。

answer

特征值为 $2$ 与 $3$；$A^2-5A+6I=0$ 成立

scene_spec.objects[0]

对角化 $P\operatorname{diag}(2,3)P^{-1}$ 代入验证

scene_spec.objects[1]

相似矩阵共享谱的示意

scene_spec.steps[0]

第一步：以对角化验证 C–H为主线，建立高等代数·特征值与特征向量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：对角化 $P\operatorname{diag}(2,3)P^{-1}$ 代入验证。

scene_spec.steps[2]

第三步：相似矩阵共享谱的示意。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

对角化 $P\operatorname{diag}(2,3)P^{-1}$ 代入验证

efficiency_tags[1]

相似矩阵共享谱的示意

## eval-linalg-017-s1

problem

求矩阵 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 的特征值与特征向量，并判断其是否可对角化。

solution

$|\lambda I-A|=(\lambda-1)^2=0$，$\lambda=1$（二重）。解 $(I-A)v=0$：$I-A=\begin{pmatrix}0&-1\\0&0\end{pmatrix}$，$\begin{pmatrix}0&-1\\0&0\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix}=0$ 得 $y=0$，特征空间 $\operatorname{span}\{(1,0)^T\}$ 仅一维（非零特征向量为 $t(1,0)^T$，$t\ne 0$）。特征空间维数 $1<$ 代数重数 $2$，故不可对角化。

answer

特征值 $\lambda=1$（二重），非零特征向量 $t(1,0)^T$（$t\ne 0$，特征空间连同零向量为一维）；不可对角化，若尔当标准形为 $\begin{pmatrix}1&1\\0&1\end{pmatrix}$

scene_spec.objects[0]

特征方程 $(\lambda-1)^2=0$ 的求解

scene_spec.objects[1]

$I-A=\begin{pmatrix}0&-1\\0&0\end{pmatrix}$ 的核空间一维标注

scene_spec.steps[0]

第一步：以特征方程+特征空间维数为主线，建立高等代数·特征值与特征向量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：特征方程 $(\lambda-1)^2=0$ 的求解。

scene_spec.steps[2]

第三步：$I-A=\begin{pmatrix}0&-1\\0&0\end{pmatrix}$ 的核空间一维标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

特征方程 $(\lambda-1)^2=0$ 的求解

efficiency_tags[1]

$I-A=\begin{pmatrix}0&-1\\0&0\end{pmatrix}$ 的核空间一维标注

## eval-linalg-017-s2

problem

求矩阵 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 的特征值与特征向量，并判断其是否可对角化。

solution

$A$ 是水平剪切变换：$(x,y)\mapsto(x+y,y)$。所有向量的 $y$ 分量不变，仅 $(t,0)^T$（水平方向）方向不变，其余向量方向都被"推斜"。剪切没有第二个不变方向，故只有一个特征方向，不可对角化。

answer

特征值 $\lambda=1$（二重），非零特征向量 $t(1,0)^T$（$t\ne 0$，特征空间连同零向量为一维）；不可对角化，若尔当标准形为 $\begin{pmatrix}1&1\\0&1\end{pmatrix}$

scene_spec.objects[0]

剪切变换的网格变形

scene_spec.objects[1]

唯一不变方向（水平）高亮

scene_spec.steps[0]

第一步：以几何剪切为主线，建立高等代数·特征值与特征向量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：剪切变换的网格变形。

scene_spec.steps[2]

第三步：唯一不变方向（水平）高亮。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

剪切变换的网格变形

efficiency_tags[1]

唯一不变方向（水平）高亮

## eval-linalg-017-s3

problem

求矩阵 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 的特征值与特征向量，并判断其是否可对角化。

solution

$A-I=\begin{pmatrix}0&1\\0&0\end{pmatrix}\ne 0$，$(A-I)^2=0$，故最小多项式为 $m(\lambda)=(\lambda-1)^2$，含有重因子 $(\lambda-1)^2$。矩阵可对角化 $\iff$ 最小多项式无重根，故 $A$ 不可对角化；其若尔当标准形为单个二阶块 $J_2(1)=\begin{pmatrix}1&1\\0&1\end{pmatrix}$。求特征向量时，$Av=v$等价于$(A-I)(x,y)^T=(y,0)^T=0$，故所有非零特征向量为$t(1,0)^T$（$t\ne0$），仅一个特征方向。

answer

特征值 $\lambda=1$（二重），非零特征向量 $t(1,0)^T$（$t\ne 0$，特征空间连同零向量为一维）；不可对角化，若尔当标准形为 $\begin{pmatrix}1&1\\0&1\end{pmatrix}$

scene_spec.objects[0]

最小多项式 $(\lambda-1)^2$ 有重因子的标注

scene_spec.objects[1]

与对角矩阵 $\operatorname{diag}(1,1)=I$ 的对照

scene_spec.steps[0]

呈现题干及适用条件：求矩阵 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 的特征值与特征向量，并判断其是否可对角化。

scene_spec.steps[1]

依次呈现：最小多项式 $(\lambda-1)^2$ 有重因子的标注

scene_spec.steps[2]

依次呈现：与对角矩阵 $\operatorname{diag}(1,1)=I$ 的对照

scene_spec.steps[3]

核对完整证明：$A-I=\begin{pmatrix}0&1\\0&0\end{pmatrix}\ne 0$，$(A-I)^2=0$，故最小多项式为 $m(\lambda)=(\lambda-1)^2$，含有重因子 $(\lambda-1)^2$。矩阵可对角化 $\iff$ 最小多项式无重根，故 $A$ 不可对角化；其若尔当标准形为单个二阶块 $J_2(1)=\begin{pmatrix}1&1\\0&1\end{pmatrix}$。求特征向量时，$Av=v$等价于$(A-I)(x,y)^T=(y,0)^T=0$，故所有非零特征向量为$t(1,0)^T$（$t\ne0$），仅一个特征方向。

scene_spec.steps[4]

高亮结果：特征值 $\lambda=1$（二重），非零特征向量 $t(1,0)^T$（$t\ne 0$，特征空间连同零向量为一维）；不可对角化，若尔当标准形为 $\begin{pmatrix}1&1\\0&1\end{pmatrix}$

efficiency_tags[0]

最小多项式 $(\lambda-1)^2$ 有重因子的标注

efficiency_tags[1]

与对角矩阵 $\operatorname{diag}(1,1)=I$ 的对照

## eval-linalg-018-s1

problem

设 $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$，求 $A^{100}$。

solution

特征方程 $(\lambda-2)^2-1=0$，特征值 $3,1$；对应特征向量 $(1,1)^T$、$(1,-1)^T$。取 $P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$（即 eval-linalg-015 的结论），则 $P^{-1}AP=\begin{pmatrix}3&0\\0&1\end{pmatrix}$，且 $P^{-1}=\dfrac{1}{2}P$（因 $P^2=2I$）。故 $A^{100}=P\begin{pmatrix}3^{100}&0\\0&1\end{pmatrix}P^{-1}=\dfrac{1}{2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}\begin{pmatrix}3^{100}&0\\0&1\end{pmatrix}\begin{pmatrix}1&1\\1&-1\end{pmatrix}=\dfrac{1}{2}\begin{pmatrix}3^{100}&1\\3^{100}&-1\end{pmatrix}\begin{pmatrix}1&1\\1&-1\end{pmatrix}=\dfrac{1}{2}\begin{pmatrix}3^{100}+1&3^{100}-1\\3^{100}-1&3^{100}+1\end{pmatrix}$。

answer

$A^{100}=\dfrac{1}{2}\begin{pmatrix}3^{100}+1&3^{100}-1\\3^{100}-1&3^{100}+1\end{pmatrix}$

scene_spec.objects[0]

特征方向分解：$3^{100}$ 倍拉伸与 $1$ 倍保持

scene_spec.objects[1]

对角化三连乘的矩阵运算

scene_spec.steps[0]

第一步：以对角化为主线，建立高等代数·特征值与特征向量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：特征方向分解：$3^{100}$ 倍拉伸与 $1$ 倍保持。

scene_spec.steps[2]

第三步：对角化三连乘的矩阵运算。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

特征方向分解：$3^{100}$ 倍拉伸与 $1$ 倍保持

efficiency_tags[1]

对角化三连乘的矩阵运算

## eval-linalg-018-s2

problem

设 $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$，求 $A^{100}$。

solution

$A=I+B$，其中 $B=\begin{pmatrix}1&1\\1&1\end{pmatrix}$，且 $B^2=2B$（验证：$B^2=\begin{pmatrix}2&2\\2&2\end{pmatrix}=2B$）。于是 $B^k=2^{k-1}B$（$k\ge 1$）。$A^{100}=(I+B)^{100}=I+\displaystyle\sum_{k=1}^{100}\binom{100}{k}2^{k-1}B=I+\dfrac{3^{100}-1}{2}B$（其中 $\displaystyle\sum_{k=1}^{100}\binom{100}{k}2^{k}=3^{100}-1$，除以 $2$ 即得）。代入 $B$：$A^{100}=\begin{pmatrix}1+\frac{3^{100}-1}{2}&\frac{3^{100}-1}{2}\\\frac{3^{100}-1}{2}&1+\frac{3^{100}-1}{2}\end{pmatrix}=\dfrac{1}{2}\begin{pmatrix}3^{100}+1&3^{100}-1\\3^{100}-1&3^{100}+1\end{pmatrix}$。

answer

$A^{100}=\dfrac{1}{2}\begin{pmatrix}3^{100}+1&3^{100}-1\\3^{100}-1&3^{100}+1\end{pmatrix}$

scene_spec.objects[0]

$B^2=2B$ 的结构示意

scene_spec.objects[1]

二项式展开系数 $\dfrac{3^{100}-1}{2}$ 的推导

scene_spec.steps[0]

第一步：以二项式展开为主线，建立高等代数·特征值与特征向量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：$B^2=2B$ 的结构示意。

scene_spec.steps[2]

第三步：二项式展开系数 $\dfrac{3^{100}-1}{2}$ 的推导。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

$B^2=2B$ 的结构示意

efficiency_tags[1]

二项式展开系数 $\dfrac{3^{100}-1}{2}$ 的推导

## eval-linalg-018-s3

problem

设 $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$，求 $A^{100}$。

solution

特征多项式 $\lambda^2-4\lambda+3$，由 C–H 定理 $A^2=4A-3I$。设 $A^n=u_nA+v_nI$，则 $A^{n+1}=A^nA=(u_nA+v_nI)A=u_nA^2+v_nA=u_n(4A-3I)+v_nA=(4u_n+v_n)A-3u_nI$，故 $u_{n+1}=4u_n+v_n$、$v_{n+1}=-3u_n$，初值 $u_1=1$、$v_1=0$。由 $v_n=-3u_{n-1}$（$n\ge 2$）代入第一式得 $u_{n+1}=4u_n-3u_{n-1}$，即 $u_{n+1}-u_n=3(u_n-u_{n-1})$；又 $u_2-u_1=3$，故 $u_n-u_{n-1}=3^{n-1}$，$u_n=1+\displaystyle\sum_{k=2}^{n}3^{k-1}=1+3\cdot\dfrac{3^{n-1}-1}{2}=\dfrac{3^n-1}{2}$，$v_n=-3u_{n-1}=-\dfrac{3^n-3}{2}$。$A^{100}=\dfrac{3^{100}-1}{2}A-\dfrac{3^{100}-3}{2}I=\dfrac{1}{2}\begin{pmatrix}3^{100}+1&3^{100}-1\\3^{100}-1&3^{100}+1\end{pmatrix}$。

answer

$A^{100}=\dfrac{1}{2}\begin{pmatrix}3^{100}+1&3^{100}-1\\3^{100}-1&3^{100}+1\end{pmatrix}$

scene_spec.objects[0]

C–H 递推 $u_{n+1}=4u_n-3u_{n-1}$ 的点列

scene_spec.objects[1]

三种方法的同框结果验证

scene_spec.steps[0]

第一步：以Cayley–Hamilton 递推为主线，建立高等代数·特征值与特征向量场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：C–H 递推 $u_{n+1}=4u_n-3u_{n-1}$ 的点列。

scene_spec.steps[2]

第三步：三种方法的同框结果验证。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

C–H 递推 $u_{n+1}=4u_n-3u_{n-1}$ 的点列

efficiency_tags[1]

三种方法的同框结果验证

## eval-linalg-019-s1

problem

设 $a\in\mathbb R$ 为参数,将二次型 $f(x,y,z)=x^2+2y^2+az^2+2xy+2xz$ 化为标准形,并讨论 $a$ 取何值时 $f$ 正定。

solution

先按含 $x$ 的项配方:$(x+y+z)^2=x^2+y^2+z^2+2xy+2xz+2yz$,故 $f=(x+y+z)^2+(y^2-2yz+(a-1)z^2)$。再对 $y$ 配方:$(y-z)^2=y^2-2yz+z^2$,得 $f=(x+y+z)^2+(y-z)^2+(a-2)z^2$。若 $a>2$,三项系数全正,且 $(x+y+z,y-z,z)=(0,0,0)$ 推出 $x=y=z=0$,故 $f>0$($(x,y,z)\neq(0,0,0)$)。若 $a\le 2$,取 $x+y+z=0,\ y=z$ 的非零解(如 $(x,y,z)=(-2,1,1)$),此时前两项为 0、第三项 $\le 0$,$f$ 不正定。

answer

$f=(x+y+z)^2+(y-z)^2+(a-2)z^2$;$f$ 正定当且仅当 $a>2$

scene_spec.objects[0]

配方过程逐项高亮:先 $(x+y+z)^2$ 再 $(y-z)^2$

scene_spec.objects[1]

$a$ 滑杆下 $z^2$ 系数由负转正(a=2 为临界)

scene_spec.steps[0]

第一步：以配方法为主线，建立高等代数·二次型场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：配方过程逐项高亮:先 $(x+y+z)^2$ 再 $(y-z)^2$。

scene_spec.steps[2]

第三步：$a$ 滑杆下 $z^2$ 系数由负转正(a=2 为临界)。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

配方过程逐项高亮:先 $(x+y+z)^2$ 再 $(y-z)^2$

efficiency_tags[1]

$a$ 滑杆下 $z^2$ 系数由负转正(a=2 为临界)

## eval-linalg-019-s2

problem

设 $a\in\mathbb R$ 为参数,将二次型 $f(x,y,z)=x^2+2y^2+az^2+2xy+2xz$ 化为标准形,并讨论 $a$ 取何值时 $f$ 正定。

solution

$f$ 的矩阵 $A=\begin{pmatrix}1&1&1\\1&2&0\\1&0&a\end{pmatrix}$。作合同变换(行列同步):第一步,第二、三行分别减去第一行,第二、三列分别减去第一列,得 $\begin{pmatrix}1&0&0\\0&1&-1\\0&-1&a-1\end{pmatrix}$;第二步,第三行加上第二行、第三列加上第二列,得 $\operatorname{diag}(1,1,a-2)$。两步对应的列变换矩阵累计为 $C=\begin{pmatrix}1&-1&-2\\0&1&1\\0&0&1\end{pmatrix}$,满足 $C^TAC=\operatorname{diag}(1,1,a-2)$。对应新变量 $u=x+y+z,\ v=y-z,\ w=z$(即 $(x,y,z)^T=C(u,v,w)^T$),标准形为 $u^2+v^2+(a-2)w^2$。合同保持正定性,故 $f$ 正定 $\iff$ 对角元全正 $\iff a>2$。

answer

$f=(x+y+z)^2+(y-z)^2+(a-2)z^2$;$f$ 正定当且仅当 $a>2$

scene_spec.objects[0]

合同初等变换的行列同步消去两步动画

scene_spec.objects[1]

变换矩阵 $C$ 的累计与 $C^TAC=\operatorname{diag}(1,1,a-2)$ 验证

scene_spec.steps[0]

第一步：以合同变换为主线，建立高等代数·二次型场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：合同初等变换的行列同步消去两步动画。

scene_spec.steps[2]

第三步：变换矩阵 $C$ 的累计与 $C^TAC=\operatorname{diag}(1,1,a-2)$ 验证。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

合同初等变换的行列同步消去两步动画

efficiency_tags[1]

变换矩阵 $C$ 的累计与 $C^TAC=\operatorname{diag}(1,1,a-2)$ 验证

## eval-linalg-019-s3

problem

设 $a\in\mathbb R$ 为参数,将二次型 $f(x,y,z)=x^2+2y^2+az^2+2xy+2xz$ 化为标准形,并讨论 $a$ 取何值时 $f$ 正定。

solution

$f$ 的矩阵 $A$ 可作 $LDL^T$ 分解: $$A=L\operatorname{diag}(1,1,a-2)L^T,\qquad L=\begin{pmatrix}1&0&0\\1&1&0\\1&-1&1\end{pmatrix}.$$ (直接乘开验证:行列为 $1,2,0$ 与 $1,0,a$ 的交叉项分别由 $L$ 的第 2、3 行生成。)令 $(u,v,w)^T=L^T(x,y,z)^T$,得新变量 $u=x+y+z,\ v=y-z,\ w=z$,于是 $$f=(x,y,z)A(x,y,z)^T=(L^T(x,y,z)^T)^T\operatorname{diag}(1,1,a-2)(L^T(x,y,z)^T)=u^2+v^2+(a-2)w^2,$$ 即标准形为 $u^2+v^2+(a-2)w^2$。再由顺序主子式($\Delta_1=1,\Delta_2=1,\Delta_3=|A|=a-2$),$f$ 正定 $\iff\Delta_3>0\iff a>2$——本条解法独立完成"化标准形+判正定"两问。边界 $a=2$ 时标准形第三项系数为 0,$f=u^2+v^2$ 半正定,零空间为 $u=v=0$,即 $x+y+z=0,\ y=z$,也就是 $t(-2,1,1)$。

answer

$f=(x+y+z)^2+(y-z)^2+(a-2)z^2$;$f$ 正定当且仅当 $a>2$

scene_spec.objects[0]

$LDL^T$ 分解的三角因子展示

scene_spec.objects[1]

主子式 $\Delta_3=a-2$ 随 $a$ 的符号变化与正定/半正定/不定三区标注

scene_spec.steps[0]

第一步：以LDLᵀ 分解为主线，建立高等代数·二次型场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：$LDL^T$ 分解的三角因子展示。

scene_spec.steps[2]

第三步：主子式 $\Delta_3=a-2$ 随 $a$ 的符号变化与正定/半正定/不定三区标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

$LDL^T$ 分解的三角因子展示

efficiency_tags[1]

主子式 $\Delta_3=a-2$ 随 $a$ 的符号变化与正定/半正定/不定三区标注

## eval-linalg-020-s1

problem

判断二次型 $f(x,y)=x^2-4xy+4y^2$ 的类型（正定/半正定/不定/负定）。

solution

$f=x^2-4xy+4y^2=(x-2y)^2\ge 0$ 对一切 $(x,y)$ 成立，且 $x=2y$（如 $(2,1)$）时取到 0，故半正定。标准形为 $u^2$（$u=x-2y$），秩为 1。

answer

半正定，秩为 1，正惯性指数 1、负惯性指数 0

scene_spec.objects[0]

配方 $(x-2y)^2$ 的逐步动画

scene_spec.objects[1]

零方向 $x=2y$ 高亮

scene_spec.steps[0]

第一步：以配方法为主线，建立高等代数·二次型场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：配方 $(x-2y)^2$ 的逐步动画。

scene_spec.steps[2]

第三步：零方向 $x=2y$ 高亮。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

配方 $(x-2y)^2$ 的逐步动画

efficiency_tags[1]

零方向 $x=2y$ 高亮

## eval-linalg-020-s2

problem

判断二次型 $f(x,y)=x^2-4xy+4y^2$ 的类型（正定/半正定/不定/负定）。

solution

矩阵 $A=\begin{pmatrix}1&-2\\-2&4\end{pmatrix}$。特征方程 $\lambda^2-5\lambda=0$，特征值 $\lambda_1=5$、$\lambda_2=0$。特征值非负且含 0，故半正定，秩 $=$ 非零特征值个数 $=1$。

answer

半正定，秩为 1，正惯性指数 1、负惯性指数 0

scene_spec.objects[0]

特征值 $5,0$ 的谱标注

scene_spec.objects[1]

半正定的判定

scene_spec.steps[0]

第一步：以矩阵特征值为主线，建立高等代数·二次型场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：特征值 $5,0$ 的谱标注。

scene_spec.steps[2]

第三步：半正定的判定。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

特征值 $5,0$ 的谱标注

efficiency_tags[1]

半正定的判定

## eval-linalg-020-s3

problem

判断二次型 $f(x,y)=x^2-4xy+4y^2$ 的类型（正定/半正定/不定/负定）。

solution

$f=(x-2y)^2\ge0$，当且仅当$x=2y$时取0，并存在非零零向量$(2,1)$；故半正定而非正定。平方中的线性形式非零，矩阵为$(1,-2)^T(1,-2)$，秩1，正、负惯性指数分别为1、0。$f=k>0$的等值集恰为平行直线对$x-2y=\pm\sqrt k$，$k=0$为一条直线。

answer

半正定，秩为 1，正惯性指数 1、负惯性指数 0

scene_spec.objects[0]

正高度等值集$x-2y=\pm\sqrt k$（$k>0$）

scene_spec.objects[1]

零方向$x=2y$与非零零向量$(2,1)$

scene_spec.steps[0]

呈现题干及适用条件：判断二次型 $f(x,y)=x^2-4xy+4y^2$ 的类型（正定/半正定/不定/负定）。

scene_spec.steps[1]

依次呈现：正高度等值集$x-2y=\pm\sqrt k$（$k>0$）

scene_spec.steps[2]

依次呈现：零方向$x=2y$与非零零向量$(2,1)$

scene_spec.steps[3]

核对完整证明：$f=(x-2y)^2\ge0$，当且仅当$x=2y$时取0，并存在非零零向量$(2,1)$；故半正定而非正定。平方中的线性形式非零，矩阵为$(1,-2)^T(1,-2)$，秩1，正、负惯性指数分别为1、0。$f=k>0$的等值集恰为平行直线对$x-2y=\pm\sqrt k$，$k=0$为一条直线。

scene_spec.steps[4]

高亮结果：半正定，秩为 1，正惯性指数 1、负惯性指数 0

efficiency_tags[0]

正高度等值集$x-2y=\pm\sqrt k$（$k>0$）

efficiency_tags[1]

零方向$x=2y$与非零零向量$(2,1)$

## eval-linalg-021-s1

problem

设 $a\in\mathbb R$ 为参数,求使二次型 $f(x,y,z)=2x^2+y^2+2z^2+2xy+2axz$ 正定的 $a$ 的取值范围。

solution

$f$ 的矩阵 $A=\begin{pmatrix}2&1&a\\1&1&0\\a&0&2\end{pmatrix}$。顺序主子式:$\Delta_1=2>0$,$\Delta_2=\begin{vmatrix}2&1\\1&1\end{vmatrix}=1>0$,$\Delta_3=|A|=2\cdot\begin{vmatrix}1&0\\0&2\end{vmatrix}-1\cdot\begin{vmatrix}1&0\\a&2\end{vmatrix}+a\cdot\begin{vmatrix}1&1\\a&0\end{vmatrix}=4-2-a^2=2-a^2$。$f$ 正定 $\iff\Delta_3>0\iff 2-a^2>0\iff -\sqrt{2}<a<\sqrt{2}$。

answer

$-\sqrt{2}<a<\sqrt{2}$

scene_spec.objects[0]

$\Delta_3(a)=2-a^2$ 的抛物线图与正区间 $(-\sqrt2,\sqrt2)$ 标注

scene_spec.objects[1]

主子式序列随 $a$ 变化

scene_spec.steps[0]

第一步：以顺序主子式为主线，建立高等代数·二次型场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：$\Delta_3(a)=2-a^2$ 的抛物线图与正区间 $(-\sqrt2,\sqrt2)$ 标注。

scene_spec.steps[2]

第三步：主子式序列随 $a$ 变化。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

$\Delta_3(a)=2-a^2$ 的抛物线图与正区间 $(-\sqrt2,\sqrt2)$ 标注

efficiency_tags[1]

主子式序列随 $a$ 变化

## eval-linalg-021-s2

problem

设 $a\in\mathbb R$ 为参数,求使二次型 $f(x,y,z)=2x^2+y^2+2z^2+2xy+2axz$ 正定的 $a$ 的取值范围。

solution

$2\left(x+\dfrac{y}{2}+\dfrac{az}{2}\right)^2=2x^2+\dfrac{y^2}{2}+\dfrac{a^2z^2}{2}+2xy+2axz+ayz$,故 $$f=2\left(x+\frac{y}{2}+\frac{az}{2}\right)^2+\left[\frac{y^2}{2}-ayz+\left(2-\frac{a^2}{2}\right)z^2\right]=2\left(x+\frac{y}{2}+\frac{az}{2}\right)^2+\frac{1}{2}(y-az)^2+(2-a^2)z^2.$$ 三项系数 $2,\ \dfrac{1}{2},\ 2-a^2$ 全正 $\iff 2-a^2>0\iff |a|<\sqrt{2}$,与解法一一致。变量替换$u=x+y/2+az/2,\ v=y-az,\ w=z$的矩阵为上三角且行列式1，故可逆。若$2-a^2\le0$，取非零向量$(x,y,z)=(-a,a,1)$，前两平方为零且$f=2-a^2\le0$，因此上述条件也是必要条件。

answer

$-\sqrt{2}<a<\sqrt{2}$

scene_spec.objects[0]

含参配方逐步展开

scene_spec.objects[1]

系数 $2-a^2$ 的符号区间

scene_spec.steps[0]

呈现题干及适用条件：设 $a\in\mathbb R$ 为参数,求使二次型 $f(x,y,z)=2x^2+y^2+2z^2+2xy+2axz$ 正定的 $a$ 的取值范围。

scene_spec.steps[1]

依次呈现：含参配方逐步展开

scene_spec.steps[2]

依次呈现：系数 $2-a^2$ 的符号区间

scene_spec.steps[3]

核对完整证明：$2\left(x+\dfrac{y}{2}+\dfrac{az}{2}\right)^2=2x^2+\dfrac{y^2}{2}+\dfrac{a^2z^2}{2}+2xy+2axz+ayz$,故 $$f=2\left(x+\frac{y}{2}+\frac{az}{2}\right)^2+\left[\frac{y^2}{2}-ayz+\left(2-\frac{a^2}{2}\right)z^2\right]=2\left(x+\frac{y}{2}+\frac{az}{2}\right)^2+\frac{1}{2}(y-az)^2+(2-a^2)z^2.$$ 三项系数 $2,\ \dfrac{1}{2},\ 2-a^2$ 全正 $\iff 2-a^2>0\iff |a|<\sqrt{2}$,与解法一一致。变量替换$u=x+y/2+az/2,\ v=y-az,\ w=z$的矩阵为上三角且行列式1，故可逆。若$2-a^2\le0$，取非零向量$(x,y,z)=(-a,a,1)$，前两平方为零且$f=2-a^2\le0$，因此上述条件也是必要条件。

scene_spec.steps[4]

高亮结果：$-\sqrt{2}<a<\sqrt{2}$

efficiency_tags[0]

含参配方逐步展开

efficiency_tags[1]

系数 $2-a^2$ 的符号区间

## eval-linalg-021-s3

problem

设 $a\in\mathbb R$ 为参数,求使二次型 $f(x,y,z)=2x^2+y^2+2z^2+2xy+2axz$ 正定的 $a$ 的取值范围。

solution

把 $A$ 分块为 $\begin{pmatrix}B&c\\c^T&2\end{pmatrix}$,其中 $B=\begin{pmatrix}2&1\\1&1\end{pmatrix}$,$c=(a,0)^T$。$B$ 正定($2>0$ 且 $|B|=1>0$),由 Schur 补判据,$A$ 正定 $\iff$ $B$ 正定且 $S=2-c^TB^{-1}c>0$。$B^{-1}=\begin{pmatrix}1&-1\\-1&2\end{pmatrix}$,$c^TB^{-1}c=(a,0)\begin{pmatrix}1&-1\\-1&2\end{pmatrix}\begin{pmatrix}a\\0\end{pmatrix}=a^2$,故 $S=2-a^2$。于是 $f$ 正定 $\iff 2-a^2>0\iff -\sqrt{2}<a<\sqrt{2}$,与前两法独立得到同一范围。

answer

$-\sqrt{2}<a<\sqrt{2}$

scene_spec.objects[0]

$2\times2$ 块 $B$ 与 Schur 补 $S=2-a^2$ 的分块标注

scene_spec.objects[1]

等值面 $f=1$ 随 $a$ 的类型切换(椭球/椭圆柱/单叶双曲面)

scene_spec.steps[0]

第一步：以Schur 补为主线，建立高等代数·二次型场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：$2\times2$ 块 $B$ 与 Schur 补 $S=2-a^2$ 的分块标注。

scene_spec.steps[2]

第三步：等值面 $f=1$ 随 $a$ 的类型切换(椭球/椭圆柱/单叶双曲面)。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

$2\times2$ 块 $B$ 与 Schur 补 $S=2-a^2$ 的分块标注

efficiency_tags[1]

等值面 $f=1$ 随 $a$ 的类型切换(椭球/椭圆柱/单叶双曲面)

## eval-linalg-022-s1

problem

将多项式 $f(x)=x^4+2x^3-7x^2-8x+12$ 因式分解。

solution

常数项 $12$ 与首项系数 $1$，可能的有理根为 $\pm1,\pm2,\pm3,\pm4,\pm6,\pm12$。逐一代入：$f(1)=1+2-7-8+12=0$；$f(2)=16+16-28-16+12=0$；$f(-2)=16-16-28+16+12=0$；$f(-3)=81-54-63+24+12=0$。四次多项式有四个根 $1,2,-2,-3$，故 $f=(x-1)(x-2)(x+2)(x+3)$。

answer

$(x-1)(x-2)(x+2)(x+3)$

scene_spec.objects[0]

有理根候选 $\pm1,\pm2,\pm3,\pm4,\pm6,\pm12$ 的逐一试根

scene_spec.objects[1]

曲线 $y=f(x)$ 与四个实根

scene_spec.steps[0]

第一步：以有理根定理为主线，建立高等代数·多项式场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：有理根候选 $\pm1,\pm2,\pm3,\pm4,\pm6,\pm12$ 的逐一试根。

scene_spec.steps[2]

第三步：曲线 $y=f(x)$ 与四个实根。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

有理根候选 $\pm1,\pm2,\pm3,\pm4,\pm6,\pm12$ 的逐一试根

efficiency_tags[1]

曲线 $y=f(x)$ 与四个实根

## eval-linalg-022-s2

problem

将多项式 $f(x)=x^4+2x^3-7x^2-8x+12$ 因式分解。

solution

设 $f=(x^2+ax+b)(x^2+cx+d)$，展开比对：$a+c=2$，$b+d+ac=-7$，$ad+bc=-8$，$bd=12$。试 $b=-2$、$d=-6$（$bd=12$）：则 $b+d=-8$，$ac=-7+8=1$；结合 $a+c=2$、$ac=1$ 得 $a=c=1$。检验 $ad+bc=1\cdot(-6)+1\cdot(-2)=-8$，全部吻合。故 $f=(x^2+x-2)(x^2+x-6)=(x-1)(x+2)(x-2)(x+3)$。

answer

$(x-1)(x-2)(x+2)(x+3)$

scene_spec.objects[0]

待定系数 $(x^2+ax+b)(x^2+cx+d)$ 展开比对

scene_spec.objects[1]

四元方程组的求解

scene_spec.steps[0]

第一步：以待定系数法为主线，建立高等代数·多项式场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：待定系数 $(x^2+ax+b)(x^2+cx+d)$ 展开比对。

scene_spec.steps[2]

第三步：四元方程组的求解。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

待定系数 $(x^2+ax+b)(x^2+cx+d)$ 展开比对

efficiency_tags[1]

四元方程组的求解

## eval-linalg-022-s3

problem

将多项式 $f(x)=x^4+2x^3-7x^2-8x+12$ 因式分解。

solution

由 $f(1)=0$，用综合除法除以 $x-1$：系数 $1,2,-7,-8,12$ 依次得商系数 $1,3,-4,-12$（即 $x^3+3x^2-4x-12$），余 0。检验 $g(2)=8+12-8-12=0$，再除以 $x-2$ 得 $x^2+5x+6$。最后 $x^2+5x+6=(x+2)(x+3)$。故 $f=(x-1)(x-2)(x+2)(x+3)$。

answer

$(x-1)(x-2)(x+2)(x+3)$

scene_spec.objects[0]

综合除法竖式动画

scene_spec.objects[1]

四次降次的过程与四个因式的连线

scene_spec.steps[0]

第一步：以综合除法逐步降次为主线，建立高等代数·多项式场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：综合除法竖式动画。

scene_spec.steps[2]

第三步：四次降次的过程与四个因式的连线。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

综合除法竖式动画

efficiency_tags[1]

四次降次的过程与四个因式的连线

## eval-linalg-023-s1

problem

分别在复数域与实数域上分解 $x^8-1$。

solution

$x^8-1=0$ 的根是 8 次单位根 $e^{2\pi ik/8}$（$k=0,1,\dots,7$），在复平面上构成正八边形的顶点。复数域上 $x^8-1=\displaystyle\prod_{k=0}^{7}\left(x-e^{2\pi ik/8}\right)$。实数域上把共轭根配对：$k=0,4$ 对应实根 $\pm 1$；$k=1,7$ 配对得 $\left(x-e^{i\pi/4}\right)\left(x-e^{-i\pi/4}\right)=x^2-2x\cos\dfrac{\pi}{4}+1=x^2-\sqrt2x+1$；$k=2,6$ 配对得 $x^2+1$；$k=3,5$ 配对得 $x^2+\sqrt2x+1$。故实数域分解为 $(x-1)(x+1)(x^2-\sqrt2x+1)(x^2+1)(x^2+\sqrt2x+1)$。

answer

复数域：$\displaystyle\prod_{k=0}^{7}\left(x-e^{2\pi ik/8}\right)$；实数域（完整实不可约分解）：$(x-1)(x+1)(x^2+1)(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)$

scene_spec.objects[0]

复平面正八边形单位根

scene_spec.objects[1]

共轭根配对的动画

scene_spec.steps[0]

第一步：以单位根为主线，建立高等代数·多项式场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：复平面正八边形单位根。

scene_spec.steps[2]

第三步：共轭根配对的动画。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

复平面正八边形单位根

efficiency_tags[1]

共轭根配对的动画

## eval-linalg-023-s2

problem

分别在复数域与实数域上分解 $x^8-1$。

solution

$x^8-1=(x^4-1)(x^4+1)=(x^2-1)(x^2+1)(x^4+1)=(x-1)(x+1)(x^2+1)(x^4+1)$。再对 $x^4+1$ 作实分解（见解法三的恒等式）：$x^4+1=(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)$，合并得完整实不可约分解 $(x-1)(x+1)(x^2+1)(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)$。复数域中$e^{2\pi ik/8}$（$k=0,\ldots,7$）是八个互异根，首项系数1，故$x^8-1=\prod_{k=0}^7(x-e^{2\pi ik/8})$。三个实二次因子的判别式分别为$-4,-2,-2$，均负，所以所列实分解确为实不可约分解。

answer

复数域：$\displaystyle\prod_{k=0}^{7}\left(x-e^{2\pi ik/8}\right)$；实数域（完整实不可约分解）：$(x-1)(x+1)(x^2+1)(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)$

scene_spec.objects[0]

平方差递推的分解树 $(x^4-1)(x^4+1)\to\cdots$

scene_spec.objects[1]

继续分解 $x^4+1$ 的恒等式标注

scene_spec.steps[0]

呈现题干及适用条件：分别在复数域与实数域上分解 $x^8-1$。

scene_spec.steps[1]

依次呈现：平方差递推的分解树 $(x^4-1)(x^4+1)\to\cdots$

scene_spec.steps[2]

依次呈现：继续分解 $x^4+1$ 的恒等式标注

scene_spec.steps[3]

核对完整证明：$x^8-1=(x^4-1)(x^4+1)=(x^2-1)(x^2+1)(x^4+1)=(x-1)(x+1)(x^2+1)(x^4+1)$。再对 $x^4+1$ 作实分解（见解法三的恒等式）：$x^4+1=(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)$，合并得完整实不可约分解 $(x-1)(x+1)(x^2+1)(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)$。复数域中$e^{2\pi ik/8}$（$k=0,\ldots,7$）是八个互异根，首项系数1，故$x^8-1=\prod_{k=0}^7(x-e^{2\pi ik/8})$。三个实二次因子的判别式分别为$-4,-2,-2$，均负，所以所列实分解确为实不可约分解。

scene_spec.steps[4]

高亮结果：复数域：$\displaystyle\prod_{k=0}^{7}\left(x-e^{2\pi ik/8}\right)$；实数域（完整实不可约分解）：$(x-1)(x+1)(x^2+1)(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)$

efficiency_tags[0]

平方差递推的分解树 $(x^4-1)(x^4+1)\to\cdots$

efficiency_tags[1]

继续分解 $x^4+1$ 的恒等式标注

## eval-linalg-023-s3

problem

分别在复数域与实数域上分解 $x^8-1$。

solution

本题复数域分解为 $\displaystyle\prod_{k=0}^{7}\left(x-e^{2\pi ik/8}\right)$（8 次单位根）。实数域分解有两种书写形式。形式一（按共轭根配对，完整实不可约分解）：$x^8-1=(x-1)(x+1)(x^2-\sqrt2x+1)(x^2+1)(x^2+\sqrt2x+1)$。形式二（按平方差递推，尚未完全分解）：$x^8-1=(x-1)(x+1)(x^2+1)(x^4+1)$。两形式由恒等式 $(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)=x^4+1$ 连接，其证明是平方差：$(x^2+1)^2-(\sqrt2x)^2=x^4+2x^2+1-2x^2=x^4+1$。故形式二是形式一的合并书写，形式一才是完整实不可约分解。

answer

复数域：$\displaystyle\prod_{k=0}^{7}\left(x-e^{2\pi ik/8}\right)$；实数域（完整实不可约分解）：$(x-1)(x+1)(x^2+1)(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)$

scene_spec.objects[0]

恒等式 $(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)=x^4+1$ 的展开验证

scene_spec.objects[1]

两种实数分解的连线对照

scene_spec.steps[0]

第一步：以两种实数分解的联系为主线，建立高等代数·多项式场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：恒等式 $(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)=x^4+1$ 的展开验证。

scene_spec.steps[2]

第三步：两种实数分解的连线对照。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

恒等式 $(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)=x^4+1$ 的展开验证

efficiency_tags[1]

两种实数分解的连线对照

## eval-linalg-024-s1

problem

将多项式 $f(x)=x^3-7x+6$ 按 $x-1$ 的幂展开（即求 $f$ 在 $x=1$ 处的泰勒展开）。

solution

$f(1)=1-7+6=0$；$f'(x)=3x^2-7$，$f'(1)=-4$；$f''(x)=6x$，$f''(1)=6$；$f'''(x)=6$，$f'''(1)=6$。由泰勒公式 $f(x)=f(1)+f'(1)(x-1)+\dfrac{f''(1)}{2}(x-1)^2+\dfrac{f'''(1)}{6}(x-1)^3=0-4(x-1)+3(x-1)^2+(x-1)^3$。

answer

$f(x)=(x-1)^3+3(x-1)^2-4(x-1)$

scene_spec.objects[0]

各阶导数值 $0,-4,6,6$ 的逐项代入

scene_spec.objects[1]

泰勒展开式的生成

scene_spec.steps[0]

第一步：以泰勒公式为主线，建立高等代数·多项式场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：各阶导数值 $0,-4,6,6$ 的逐项代入。

scene_spec.steps[2]

第三步：泰勒展开式的生成。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

各阶导数值 $0,-4,6,6$ 的逐项代入

efficiency_tags[1]

泰勒展开式的生成

## eval-linalg-024-s2

problem

将多项式 $f(x)=x^3-7x+6$ 按 $x-1$ 的幂展开（即求 $f$ 在 $x=1$ 处的泰勒展开）。

solution

对系数 $1,0,-7,6$ 反复除以 $x-1$。第一次：商系数 $1,1,-6$，余 $0$；第二次：商 $1,2$，余 $-4$；第三次：商 $1$，余 $3$。由 $f=(x-1)q_1+r_1$，$q_1=(x-1)q_2+r_2$，$q_2=(x-1)q_3+r_3$，得 $f=(x-1)[(x-1)[(x-1)\cdot 1+3]-4]=(x-1)^3+3(x-1)^2-4(x-1)$。

answer

$f(x)=(x-1)^3+3(x-1)^2-4(x-1)$

scene_spec.objects[0]

综合除法连除的三次竖式

scene_spec.objects[1]

余数 $0,-4,3$ 的提取

scene_spec.steps[0]

第一步：以综合除法连除为主线，建立高等代数·多项式场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：综合除法连除的三次竖式。

scene_spec.steps[2]

第三步：余数 $0,-4,3$ 的提取。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

综合除法连除的三次竖式

efficiency_tags[1]

余数 $0,-4,3$ 的提取

## eval-linalg-024-s3

problem

将多项式 $f(x)=x^3-7x+6$ 按 $x-1$ 的幂展开（即求 $f$ 在 $x=1$ 处的泰勒展开）。

solution

令 $y=x-1$，则 $x=y+1$。$f=(y+1)^3-7(y+1)+6=y^3+3y^2+3y+1-7y-7+6=y^3+3y^2-4y$。代回 $y=x-1$ 得 $f=(x-1)^3+3(x-1)^2-4(x-1)$。

answer

$f(x)=(x-1)^3+3(x-1)^2-4(x-1)$

scene_spec.objects[0]

换元 $y=x-1$ 的展开动画

scene_spec.objects[1]

曲线与展开点 $(1,0)$

scene_spec.steps[0]

第一步：以换元展开为主线，建立高等代数·多项式场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：换元 $y=x-1$ 的展开动画。

scene_spec.steps[2]

第三步：曲线与展开点 $(1,0)$。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

换元 $y=x-1$ 的展开动画

efficiency_tags[1]

曲线与展开点 $(1,0)$

## eval-linalg-025-s1

problem

设 $f(x)=x^5+x+1$。求 $f(x)$ 除以 $x-1$ 的余式，以及除以 $x^2+1$ 的余式。

solution

除以 $x-1$ 的余式为 $f(1)=1+1+1=3$。除以二次式 $x^2+1$ 设余式为 $ax+b$，由 $x^2+1$ 的根 $x=i$（虚数单位）：$f(i)=i^5+i+1$，而 $i^4=1$ 故 $i^5=i$，得 $f(i)=2i+1$。余式在 $x=i$ 处的值 $ai+b$ 应等于 $f(i)$：$ai+b=2i+1$，故 $a=2$、$b=1$，余式为 $2x+1$。

answer

除以 $x-1$ 余 $3$；除以 $x^2+1$ 余 $2x+1$

scene_spec.objects[0]

余数定理代入 $f(1)=3$ 的标注

scene_spec.objects[1]

二次余式 $ax+b$ 的设定

scene_spec.steps[0]

第一步：以余数定理为主线，建立高等代数·多项式场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：余数定理代入 $f(1)=3$ 的标注。

scene_spec.steps[2]

第三步：二次余式 $ax+b$ 的设定。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

余数定理代入 $f(1)=3$ 的标注

efficiency_tags[1]

二次余式 $ax+b$ 的设定

## eval-linalg-025-s2

problem

设 $f(x)=x^5+x+1$。求 $f(x)$ 除以 $x-1$ 的余式，以及除以 $x^2+1$ 的余式。

solution

除以 $x^2+1$：$x^5+x+1$ 中，$x^5$ 与 $x$ 各含 $x^2+1$ 的分解：$x^5=x^3(x^2+1)-x^3$，$x^3=x(x^2+1)-x$，故 $x^5+x+1=x^3(x^2+1)-x(x^2+1)+x+x+1=(x^2+1)(x^3-x)+(2x+1)$，余式 $2x+1$。除以 $x-1$：$x^5+x+1=(x-1)q+3$ 由余数定理直接得余 $3$（商 $q=x^4+x^3+x^2+x+2$，验证 $f(1)=3$）。

answer

除以 $x-1$ 余 $3$；除以 $x^2+1$ 余 $2x+1$

scene_spec.objects[0]

长除法竖式动画

scene_spec.objects[1]

商 $x^3-x$ 与余式 $2x+1$ 的提取

scene_spec.steps[0]

第一步：以长除法为主线，建立高等代数·多项式场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：长除法竖式动画。

scene_spec.steps[2]

第三步：商 $x^3-x$ 与余式 $2x+1$ 的提取。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

长除法竖式动画

efficiency_tags[1]

商 $x^3-x$ 与余式 $2x+1$ 的提取

## eval-linalg-025-s3

problem

设 $f(x)=x^5+x+1$。求 $f(x)$ 除以 $x-1$ 的余式，以及除以 $x^2+1$ 的余式。

solution

设除以 $x^2+1$ 的余式为 $ax+b$，则 $f(x)=(x^2+1)q(x)+ax+b$。取 $x=i$ 与 $x=-i$：$f(i)=1+2i$（同解法一），$f(-i)=(-i)^5-i+1=-i-i+1=1-2i$。解 $\begin{cases}ai+b=1+2i\\-ai+b=1-2i\end{cases}$，相加得 $2b=2$、$b=1$；相减得 $2ai=4i$、$a=2$。余式 $2x+1$。除以$x-1$时由余数定理，余式为$f(1)=1+1+1=3$。

answer

除以 $x-1$ 余 $3$；除以 $x^2+1$ 余 $2x+1$

scene_spec.objects[0]

复平面 $x=\pm i$ 代入

scene_spec.objects[1]

方程组 $ai+b=1+2i$ 的求解

scene_spec.steps[0]

呈现题干及适用条件：设 $f(x)=x^5+x+1$。求 $f(x)$ 除以 $x-1$ 的余式，以及除以 $x^2+1$ 的余式。

scene_spec.steps[1]

依次呈现：复平面 $x=\pm i$ 代入

scene_spec.steps[2]

依次呈现：方程组 $ai+b=1+2i$ 的求解

scene_spec.steps[3]

核对完整证明：设除以 $x^2+1$ 的余式为 $ax+b$，则 $f(x)=(x^2+1)q(x)+ax+b$。取 $x=i$ 与 $x=-i$：$f(i)=1+2i$（同解法一），$f(-i)=(-i)^5-i+1=-i-i+1=1-2i$。解 $\begin{cases}ai+b=1+2i\\-ai+b=1-2i\end{cases}$，相加得 $2b=2$、$b=1$；相减得 $2ai=4i$、$a=2$。余式 $2x+1$。除以$x-1$时由余数定理，余式为$f(1)=1+1+1=3$。

scene_spec.steps[4]

高亮结果：除以 $x-1$ 余 $3$；除以 $x^2+1$ 余 $2x+1$

efficiency_tags[0]

复平面 $x=\pm i$ 代入

efficiency_tags[1]

方程组 $ai+b=1+2i$ 的求解

## eval-linalg-026-s1

problem

判断向量组 $\alpha_1=(1,2,3)$，$\alpha_2=(2,3,1)$，$\alpha_3=(3,1,2)$ 是否线性相关。

solution

以三向量为行（或列）的行列式 $D=\begin{vmatrix}1&2&3\\2&3&1\\3&1&2\end{vmatrix}=1\cdot(3\cdot 2-1\cdot 1)-2\cdot(2\cdot 2-1\cdot 3)+3\cdot(2\cdot 1-3\cdot 3)=1\cdot 5-2\cdot 1+3\cdot(-7)=5-2-21=-18\ne 0$。行列式非零，故三向量线性无关。

answer

线性无关

scene_spec.objects[0]

三阶行列式 $-18$ 的展开计算

scene_spec.objects[1]

体积 $|D|=18$ 的标注

scene_spec.steps[0]

第一步：以行列式为主线，建立高等代数·线性空间场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：三阶行列式 $-18$ 的展开计算。

scene_spec.steps[2]

第三步：体积 $|D|=18$ 的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

三阶行列式 $-18$ 的展开计算

efficiency_tags[1]

体积 $|D|=18$ 的标注

## eval-linalg-026-s2

problem

判断向量组 $\alpha_1=(1,2,3)$，$\alpha_2=(2,3,1)$，$\alpha_3=(3,1,2)$ 是否线性相关。

solution

设 $k_1\alpha_1+k_2\alpha_2+k_3\alpha_3=0$，即 $\begin{cases}k_1+2k_2+3k_3=0\\2k_1+3k_2+k_3=0\\3k_1+k_2+2k_3=0\end{cases}$。由第一式 $k_1=-2k_2-3k_3$，代入第二式：$2(-2k_2-3k_3)+3k_2+k_3=0$，即 $-k_2-5k_3=0$，$k_2=-5k_3$；代入第三式：$3(-2k_2-3k_3)+k_2+2k_3=0$，即 $-5k_2-7k_3=0$，代入 $k_2=-5k_3$ 得 $25k_3-7k_3=18k_3=0$，$k_3=0$，进而 $k_2=0$、$k_1=0$。只有零解，线性无关。

answer

线性无关

scene_spec.objects[0]

齐次方程组的逐步代入消元

scene_spec.objects[1]

零解唯一性的标注

scene_spec.steps[0]

第一步：以定义解方程组为主线，建立高等代数·线性空间场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：齐次方程组的逐步代入消元。

scene_spec.steps[2]

第三步：零解唯一性的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

齐次方程组的逐步代入消元

efficiency_tags[1]

零解唯一性的标注

## eval-linalg-026-s3

problem

判断向量组 $\alpha_1=(1,2,3)$，$\alpha_2=(2,3,1)$，$\alpha_3=(3,1,2)$ 是否线性相关。

solution

三向量张成的平行六面体体积 $|D|=18\ne 0$，即三向量不共面，故线性无关（线性相关⇔体积为 0）。具体计算$\alpha_2\times\alpha_3=(5,-1,-7)$，$\alpha_1\cdot(\alpha_2\times\alpha_3)=5-2-21=-18$，所以体积为18，结论由本解独立获得。

answer

线性无关

scene_spec.objects[0]

三向量与平行六面体

scene_spec.objects[1]

不共面的几何展示

scene_spec.steps[0]

呈现题干及适用条件：判断向量组 $\alpha_1=(1,2,3)$，$\alpha_2=(2,3,1)$，$\alpha_3=(3,1,2)$ 是否线性相关。

scene_spec.steps[1]

依次呈现：三向量与平行六面体

scene_spec.steps[2]

依次呈现：不共面的几何展示

scene_spec.steps[3]

核对完整证明：三向量张成的平行六面体体积 $|D|=18\ne 0$，即三向量不共面，故线性无关（线性相关⇔体积为 0）。具体计算$\alpha_2\times\alpha_3=(5,-1,-7)$，$\alpha_1\cdot(\alpha_2\times\alpha_3)=5-2-21=-18$，所以体积为18，结论由本解独立获得。

scene_spec.steps[4]

高亮结果：线性无关

efficiency_tags[0]

三向量与平行六面体

efficiency_tags[1]

不共面的几何展示

## eval-linalg-027-s1

problem

求 $\mathbb R^3$ 中子空间 $W=\operatorname{span}\{(1,1,0),(0,1,1)\}$ 的正交补 $W^\perp$。

solution

$W^\perp=\{(x,y,z):(x,y,z)\cdot(1,1,0)=0,\ (x,y,z)\cdot(0,1,1)=0\}$，即 $\begin{cases}x+y=0\\y+z=0\end{cases}$。由第二式 $z=-y$，第一式 $x=-y$，故 $(x,y,z)=(-y,y,-y)=y(-1,1,-1)$，取 $(1,-1,1)$ 为基，$W^\perp$ 为一维。

answer

$W^\perp=\operatorname{span}\{(1,-1,1)\}$（一维）

scene_spec.objects[0]

垂直方程组 $\begin{cases}x+y=0\\y+z=0\end{cases}$ 的求解

scene_spec.objects[1]

解方向 $(-y,y,-y)$ 的标注

scene_spec.steps[0]

第一步：以解方程组为主线，建立高等代数·线性空间场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：垂直方程组 $\begin{cases}x+y=0\\y+z=0\end{cases}$ 的求解。

scene_spec.steps[2]

第三步：解方向 $(-y,y,-y)$ 的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

垂直方程组 $\begin{cases}x+y=0\\y+z=0\end{cases}$ 的求解

efficiency_tags[1]

解方向 $(-y,y,-y)$ 的标注

## eval-linalg-027-s2

problem

求 $\mathbb R^3$ 中子空间 $W=\operatorname{span}\{(1,1,0),(0,1,1)\}$ 的正交补 $W^\perp$。

solution

把 $\{(1,1,0),(0,1,1)\}$ 扩充为 $\mathbb R^3$ 的正交基：$u_1=(1,1,0)$；$u_2=(0,1,1)-\dfrac{(0,1,1)\cdot(1,1,0)}{2}(1,1,0)=(0,1,1)-\dfrac{1}{2}(1,1,0)=\left(-\dfrac{1}{2},\dfrac{1}{2},1\right)$，取 $(-1,1,2)$。再取 $e_3=(0,0,1)$ 去掉前两者的投影：$u_3=(0,0,1)-0-\dfrac{(0,0,1)\cdot(-1,1,2)}{6}(-1,1,2)=(0,0,1)-\dfrac{1}{3}(-1,1,2)=\left(\dfrac{1}{3},-\dfrac{1}{3},\dfrac{1}{3}\right)$，取 $(1,-1,1)$。它与 $u_1,u_2$ 均正交，故 $W^\perp=\operatorname{span}\{(1,-1,1)\}$。

answer

$W^\perp=\operatorname{span}\{(1,-1,1)\}$（一维）

scene_spec.objects[0]

Gram–Schmidt 扩充的投影步骤

scene_spec.objects[1]

第三个正交向量 $(1,-1,1)$ 的提取

scene_spec.steps[0]

第一步：以Gram–Schmidt 扩充为主线，建立高等代数·线性空间场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：Gram–Schmidt 扩充的投影步骤。

scene_spec.steps[2]

第三步：第三个正交向量 $(1,-1,1)$ 的提取。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

Gram–Schmidt 扩充的投影步骤

efficiency_tags[1]

第三个正交向量 $(1,-1,1)$ 的提取

## eval-linalg-027-s3

problem

求 $\mathbb R^3$ 中子空间 $W=\operatorname{span}\{(1,1,0),(0,1,1)\}$ 的正交补 $W^\perp$。

solution

$(1,1,0)\times(0,1,1)=(1\cdot 1-0\cdot 1,\ 0\cdot 0-1\cdot 1,\ 1\cdot 1-1\cdot 0)=(1,-1,1)$，与两生成元都垂直，故 $W^\perp=\operatorname{span}\{(1,-1,1)\}$（$\dim W^\perp=3-2=1$）。

answer

$W^\perp=\operatorname{span}\{(1,-1,1)\}$（一维）

scene_spec.objects[0]

叉积 $(1,1,0)\times(0,1,1)$ 的右手定则

scene_spec.objects[1]

平面 $W$ 与法线 $(1,-1,1)$

scene_spec.steps[0]

第一步：以叉积为主线，建立高等代数·线性空间场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：叉积 $(1,1,0)\times(0,1,1)$ 的右手定则。

scene_spec.steps[2]

第三步：平面 $W$ 与法线 $(1,-1,1)$。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

叉积 $(1,1,0)\times(0,1,1)$ 的右手定则

efficiency_tags[1]

平面 $W$ 与法线 $(1,-1,1)$

## eval-linalg-028-s1

problem

在 $\mathbb R^2$ 中，求向量 $\alpha=(2,3)$ 在基 $\beta_1=(1,2)$、$\beta_2=(1,1)$ 下的坐标。

solution

设 $\alpha=x_1\beta_1+x_2\beta_2$，即 $\begin{cases}x_1+x_2=2\\2x_1+x_2=3\end{cases}$。两式相减：$x_1=1$，代回得 $x_2=1$。故坐标为 $(1,1)$。

answer

$(1,1)$

scene_spec.objects[0]

方程组 $\begin{cases}x_1+x_2=2\\2x_1+x_2=3\end{cases}$ 的消元

scene_spec.objects[1]

坐标 $(1,1)$ 的标注

scene_spec.steps[0]

第一步：以解方程组为主线，建立高等代数·线性空间场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：方程组 $\begin{cases}x_1+x_2=2\\2x_1+x_2=3\end{cases}$ 的消元。

scene_spec.steps[2]

第三步：坐标 $(1,1)$ 的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

方程组 $\begin{cases}x_1+x_2=2\\2x_1+x_2=3\end{cases}$ 的消元

efficiency_tags[1]

坐标 $(1,1)$ 的标注

## eval-linalg-028-s2

problem

在 $\mathbb R^2$ 中，求向量 $\alpha=(2,3)$ 在基 $\beta_1=(1,2)$、$\beta_2=(1,1)$ 下的坐标。

solution

把基$\{\beta_1,\beta_2\}$坐标映到标准坐标的矩阵 $P=\begin{pmatrix}1&1\\2&1\end{pmatrix}$（列为基向量）。$\alpha=P\xi$，其中 $\xi$ 为所求坐标。$P^{-1}=\dfrac{1}{1-2}\begin{pmatrix}1&-1\\-2&1\end{pmatrix}=\begin{pmatrix}-1&1\\2&-1\end{pmatrix}$。故 $\xi=P^{-1}\alpha=\begin{pmatrix}-1&1\\2&-1\end{pmatrix}\begin{pmatrix}2\\3\end{pmatrix}=\begin{pmatrix}-2+3\\4-3\end{pmatrix}=\begin{pmatrix}1\\1\end{pmatrix}$。

answer

$(1,1)$

scene_spec.objects[0]

过渡矩阵 $P=\begin{pmatrix}1&1\\2&1\end{pmatrix}$ 与 $P^{-1}$ 的作用

scene_spec.objects[1]

矩阵乘法动画

scene_spec.steps[0]

呈现题干及适用条件：在 $\mathbb R^2$ 中，求向量 $\alpha=(2,3)$ 在基 $\beta_1=(1,2)$、$\beta_2=(1,1)$ 下的坐标。

scene_spec.steps[1]

依次呈现：过渡矩阵 $P=\begin{pmatrix}1&1\\2&1\end{pmatrix}$ 与 $P^{-1}$ 的作用

scene_spec.steps[2]

依次呈现：矩阵乘法动画

scene_spec.steps[3]

核对完整证明：把基$\{\beta_1,\beta_2\}$坐标映到标准坐标的矩阵 $P=\begin{pmatrix}1&1\\2&1\end{pmatrix}$（列为基向量）。$\alpha=P\xi$，其中 $\xi$ 为所求坐标。$P^{-1}=\dfrac{1}{1-2}\begin{pmatrix}1&-1\\-2&1\end{pmatrix}=\begin{pmatrix}-1&1\\2&-1\end{pmatrix}$。故 $\xi=P^{-1}\alpha=\begin{pmatrix}-1&1\\2&-1\end{pmatrix}\begin{pmatrix}2\\3\end{pmatrix}=\begin{pmatrix}-2+3\\4-3\end{pmatrix}=\begin{pmatrix}1\\1\end{pmatrix}$。

scene_spec.steps[4]

高亮结果：$(1,1)$

efficiency_tags[0]

过渡矩阵 $P=\begin{pmatrix}1&1\\2&1\end{pmatrix}$ 与 $P^{-1}$ 的作用

efficiency_tags[1]

矩阵乘法动画

## eval-linalg-028-s3

problem

在 $\mathbb R^2$ 中，求向量 $\alpha=(2,3)$ 在基 $\beta_1=(1,2)$、$\beta_2=(1,1)$ 下的坐标。

solution

在图上作平行四边形：$\alpha=(2,3)$ 可由 $\beta_1+\beta_2=(2,3)$ 一次组合而成（$1\cdot(1,2)+1\cdot(1,1)=(2,3)$），坐标即组合系数 $(1,1)$。

answer

$(1,1)$

scene_spec.objects[0]

斜基网格与平行四边形分解

scene_spec.objects[1]

$\beta_1+\beta_2=(2,3)$ 的几何展示

scene_spec.steps[0]

第一步：以几何分解为主线，建立高等代数·线性空间场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：斜基网格与平行四边形分解。

scene_spec.steps[2]

第三步：$\beta_1+\beta_2=(2,3)$ 的几何展示。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

斜基网格与平行四边形分解

efficiency_tags[1]

$\beta_1+\beta_2=(2,3)$ 的几何展示

## eval-linalg-029-s1

problem

设线性变换 $T:\mathbb R^2\to\mathbb R^2$ 为 $T(x,y)=(x+2y,2x+y)$。求 $\ker T$ 与 $\operatorname{Im}T$，并说明其维数关系。

solution

$T$ 的矩阵 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$，$\det A=1-4=-3\ne 0$，故 $A$ 可逆，$T$ 为同构：$\ker T=\{0\}$（零维），$\operatorname{Im}T=\mathbb R^2$（二维），维数公式 $0+2=2$ 成立。

answer

$\ker T=\{(0,0)\}$；$\operatorname{Im}T=\mathbb R^2$；$\dim\ker T+\dim\operatorname{Im}T=2$

scene_spec.objects[0]

行列式 $\det A=-3\ne0$ 的可逆判定

scene_spec.objects[1]

核为零、像为全空间的标注

scene_spec.steps[0]

第一步：以矩阵行列式为主线，建立高等代数·线性变换场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：行列式 $\det A=-3\ne0$ 的可逆判定。

scene_spec.steps[2]

第三步：核为零、像为全空间的标注。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

行列式 $\det A=-3\ne0$ 的可逆判定

efficiency_tags[1]

核为零、像为全空间的标注

## eval-linalg-029-s2

problem

设线性变换 $T:\mathbb R^2\to\mathbb R^2$ 为 $T(x,y)=(x+2y,2x+y)$。求 $\ker T$ 与 $\operatorname{Im}T$，并说明其维数关系。

solution

核：解 $\begin{cases}x+2y=0\\2x+y=0\end{cases}$，第一式 $x=-2y$ 代入第二式：$-4y+y=-3y=0$，$y=0$，$x=0$，故 $\ker T=\{(0,0)\}$。像：对任意 $(u,v)$，解 $\begin{cases}x+2y=u\\2x+y=v\end{cases}$，由第二式 $y=v-2x$ 代入第一式：$x+2v-4x=u$，$x=\dfrac{2v-u}{3}$，$y=v-2\cdot\dfrac{2v-u}{3}=\dfrac{2u-v}{3}$，恒有解，故 $\operatorname{Im}T=\mathbb R^2$。

answer

$\ker T=\{(0,0)\}$；$\operatorname{Im}T=\mathbb R^2$；$\dim\ker T+\dim\operatorname{Im}T=2$

scene_spec.objects[0]

齐次方程组只有零解的消元

scene_spec.objects[1]

对任意 $(u,v)$ 解的存在性验证

scene_spec.steps[0]

第一步：以直接求解为主线，建立高等代数·线性变换场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：齐次方程组只有零解的消元。

scene_spec.steps[2]

第三步：对任意 $(u,v)$ 解的存在性验证。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

齐次方程组只有零解的消元

efficiency_tags[1]

对任意 $(u,v)$ 解的存在性验证

## eval-linalg-029-s3

problem

设线性变换 $T:\mathbb R^2\to\mathbb R^2$ 为 $T(x,y)=(x+2y,2x+y)$。求 $\ker T$ 与 $\operatorname{Im}T$，并说明其维数关系。

solution

$T\circ T$ 的矩阵 $A^2=\begin{pmatrix}5&4\\4&5\end{pmatrix}$，$\det A^2=9\ne 0$，仍为同构。或由特征值观点：$A$ 的特征值为 $3,-1$（eval-linalg-015），均非零，故核为零、像为全空间。

answer

$\ker T=\{(0,0)\}$；$\operatorname{Im}T=\mathbb R^2$；$\dim\ker T+\dim\operatorname{Im}T=2$

scene_spec.objects[0]

网格在 $T$ 下的形变

scene_spec.objects[1]

特征方向拉伸（3 倍/反向）与复合 $T\circ T$ 的可逆性

scene_spec.steps[0]

第一步：以复合变换为主线，建立高等代数·线性变换场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：网格在 $T$ 下的形变。

scene_spec.steps[2]

第三步：特征方向拉伸（3 倍/反向）与复合 $T\circ T$ 的可逆性。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

网格在 $T$ 下的形变

efficiency_tags[1]

特征方向拉伸（3 倍/反向）与复合 $T\circ T$ 的可逆性

## eval-linalg-030-s1

problem

用 Gram–Schmidt 正交化方法把向量组 $(1,1,0),(1,0,1),(0,1,1)$ 化为正交向量组。

solution

取 $u_1=(1,1,0)$。$u_2=(1,0,1)-\dfrac{(1,0,1)\cdot u_1}{\|u_1\|^2}u_1=(1,0,1)-\dfrac{1}{2}(1,1,0)=\left(\dfrac{1}{2},-\dfrac{1}{2},1\right)$，乘 2 取 $u_2=(1,-1,2)$。$u_3=(0,1,1)-\dfrac{(0,1,1)\cdot u_1}{\|u_1\|^2}u_1-\dfrac{(0,1,1)\cdot u_2}{\|u_2\|^2}u_2=(0,1,1)-\dfrac{1}{2}(1,1,0)-\dfrac{1}{6}(1,-1,2)=\left(-\dfrac{2}{3},\dfrac{2}{3},\dfrac{2}{3}\right)$，乘 $-\dfrac{3}{2}$ 取 $u_3=(1,-1,-1)$。验证：$u_1\cdot u_2=0$，$u_1\cdot u_3=1-1+0=0$，$u_2\cdot u_3=1+1-2=0$，两两正交。

answer

$u_1=(1,1,0),\ u_2=(1,-1,2),\ u_3=(1,-1,-1)$；各自只允许乘非零常数。

scene_spec.objects[0]

投影减去的逐步动画

scene_spec.objects[1]

$u_2=(1,-1,2)$、$u_3=(1,-1,-1)$ 的生成

scene_spec.steps[0]

呈现题干及适用条件：用 Gram–Schmidt 正交化方法把向量组 $(1,1,0),(1,0,1),(0,1,1)$ 化为正交向量组。

scene_spec.steps[1]

依次呈现：投影减去的逐步动画

scene_spec.steps[2]

依次呈现：$u_2=(1,-1,2)$、$u_3=(1,-1,-1)$ 的生成

scene_spec.steps[3]

核对完整证明：取 $u_1=(1,1,0)$。$u_2=(1,0,1)-\dfrac{(1,0,1)\cdot u_1}{\|u_1\|^2}u_1=(1,0,1)-\dfrac{1}{2}(1,1,0)=\left(\dfrac{1}{2},-\dfrac{1}{2},1\right)$，乘 2 取 $u_2=(1,-1,2)$。$u_3=(0,1,1)-\dfrac{(0,1,1)\cdot u_1}{\|u_1\|^2}u_1-\dfrac{(0,1,1)\cdot u_2}{\|u_2\|^2}u_2=(0,1,1)-\dfrac{1}{2}(1,1,0)-\dfrac{1}{6}(1,-1,2)=\left(-\dfrac{2}{3},\dfrac{2}{3},\dfrac{2}{3}\right)$，乘 $-\dfrac{3}{2}$ 取 $u_3=(1,-1,-1)$。验证：$u_1\cdot u_2=0$，$u_1\cdot u_3=1-1+0=0$，$u_2\cdot u_3=1+1-2=0$，两两正交。

scene_spec.steps[4]

高亮结果：$u_1=(1,1,0),\ u_2=(1,-1,2),\ u_3=(1,-1,-1)$；各自只允许乘非零常数。

efficiency_tags[0]

投影减去的逐步动画

efficiency_tags[1]

$u_2=(1,-1,2)$、$u_3=(1,-1,-1)$ 的生成

## eval-linalg-030-s2

problem

用 Gram–Schmidt 正交化方法把向量组 $(1,1,0),(1,0,1),(0,1,1)$ 化为正交向量组。

solution

按原顺序令$v_1=(1,1,0),v_2=(1,0,1),v_3=(0,1,1)$。首先$w_1=v_1$，$w_2=v_2-\frac{\langle v_2,w_1\rangle}{\langle w_1,w_1\rangle}w_1=(1/2,-1/2,1)$，可取非零倍数$u_2=(1,-1,2)$。随后$w_3=v_3-\frac12w_1-\frac16u_2=(-2/3,2/3,2/3)$，取$u_3=(-3/2)w_3=(1,-1,-1)$。三者非零且两两内积为0，故按题干指定的Gram–Schmidt得到$u_1=(1,1,0),u_2=(1,-1,2),u_3=(1,-1,-1)$。允许每个结果乘非零常数。

answer

$u_1=(1,1,0),\ u_2=(1,-1,2),\ u_3=(1,-1,-1)$；各自只允许乘非零常数。

scene_spec.objects[0]

按输入原顺序投影：$w_2=v_2-\frac12v_1$

scene_spec.objects[1]

$w_3=v_3-\frac12v_1-\frac16(1,-1,2)$

scene_spec.objects[2]

非零倍数得到$(1,1,0),(1,-1,2),(1,-1,-1)$

scene_spec.steps[0]

呈现题干及适用条件：用 Gram–Schmidt 正交化方法把向量组 $(1,1,0),(1,0,1),(0,1,1)$ 化为正交向量组。

scene_spec.steps[1]

依次呈现：按输入原顺序投影：$w_2=v_2-\frac12v_1$

scene_spec.steps[2]

依次呈现：$w_3=v_3-\frac12v_1-\frac16(1,-1,2)$

scene_spec.steps[3]

依次呈现：非零倍数得到$(1,1,0),(1,-1,2),(1,-1,-1)$

scene_spec.steps[4]

核对完整证明：按原顺序令$v_1=(1,1,0),v_2=(1,0,1),v_3=(0,1,1)$。首先$w_1=v_1$，$w_2=v_2-\frac{\langle v_2,w_1\rangle}{\langle w_1,w_1\rangle}w_1=(1/2,-1/2,1)$，可取非零倍数$u_2=(1,-1,2)$。随后$w_3=v_3-\frac12w_1-\frac16u_2=(-2/3,2/3,2/3)$，取$u_3=(-3/2)w_3=(1,-1,-1)$。三者非零且两两内积为0，故按题干指定的Gram–Schmidt得到$u_1=(1,1,0),u_2=(1,-1,2),u_3=(1,-1,-1)$。允许每个结果乘非零常数。

scene_spec.steps[5]

高亮结果：$u_1=(1,1,0),\ u_2=(1,-1,2),\ u_3=(1,-1,-1)$；各自只允许乘非零常数。

efficiency_tags[0]

按输入原顺序投影：$w_2=v_2-\frac12v_1$

efficiency_tags[1]

$w_3=v_3-\frac12v_1-\frac16(1,-1,2)$

efficiency_tags[2]

非零倍数得到$(1,1,0),(1,-1,2),(1,-1,-1)$

## eval-linalg-030-s3

problem

用 Gram–Schmidt 正交化方法把向量组 $(1,1,0),(1,0,1),(0,1,1)$ 化为正交向量组。

solution

验证解法一的三向量线性无关：行列式 $\begin{vmatrix}1&1&0\\1&-1&2\\1&-1&-1\end{vmatrix}=1\cdot(1+2)-1\cdot(-1-2)+0=3+3=6\ne 0$。且三者张成的空间与原组相同（原组行列式 $\begin{vmatrix}1&1&0\\1&0&1\\0&1&1\end{vmatrix}=-2\ne 0$，两组都张成 $\mathbb R^3$），故正交化合法。按原顺序令$v_1=(1,1,0),v_2=(1,0,1),v_3=(0,1,1)$。首先$w_1=v_1$，$w_2=v_2-\frac{\langle v_2,w_1\rangle}{\langle w_1,w_1\rangle}w_1=(1/2,-1/2,1)$，可取非零倍数$u_2=(1,-1,2)$。随后$w_3=v_3-\frac12w_1-\frac16u_2=(-2/3,2/3,2/3)$，取$u_3=(-3/2)w_3=(1,-1,-1)$。三者非零且两两内积为0，故按题干指定的Gram–Schmidt得到$u_1=(1,1,0),u_2=(1,-1,2),u_3=(1,-1,-1)$。允许每个结果乘非零常数。

answer

$u_1=(1,1,0),\ u_2=(1,-1,2),\ u_3=(1,-1,-1)$；各自只允许乘非零常数。

scene_spec.objects[0]

两两垂直的验证标注

scene_spec.objects[1]

行列式 $6\ne0$ 的线性无关验证

scene_spec.steps[0]

呈现题干及适用条件：用 Gram–Schmidt 正交化方法把向量组 $(1,1,0),(1,0,1),(0,1,1)$ 化为正交向量组。

scene_spec.steps[1]

依次呈现：两两垂直的验证标注

scene_spec.steps[2]

依次呈现：行列式 $6\ne0$ 的线性无关验证

scene_spec.steps[3]

核对完整证明：验证解法一的三向量线性无关：行列式 $\begin{vmatrix}1&1&0\\1&-1&2\\1&-1&-1\end{vmatrix}=1\cdot(1+2)-1\cdot(-1-2)+0=3+3=6\ne 0$。且三者张成的空间与原组相同（原组行列式 $\begin{vmatrix}1&1&0\\1&0&1\\0&1&1\end{vmatrix}=-2\ne 0$，两组都张成 $\mathbb R^3$），故正交化合法。按原顺序令$v_1=(1,1,0),v_2=(1,0,1),v_3=(0,1,1)$。首先$w_1=v_1$，$w_2=v_2-\frac{\langle v_2,w_1\rangle}{\langle w_1,w_1\rangle}w_1=(1/2,-1/2,1)$，可取非零倍数$u_2=(1,-1,2)$。随后$w_3=v_3-\frac12w_1-\frac16u_2=(-2/3,2/3,2/3)$，取$u_3=(-3/2)w_3=(1,-1,-1)$。三者非零且两两内积为0，故按题干指定的Gram–Schmidt得到$u_1=(1,1,0),u_2=(1,-1,2),u_3=(1,-1,-1)$。允许每个结果乘非零常数。

scene_spec.steps[4]

高亮结果：$u_1=(1,1,0),\ u_2=(1,-1,2),\ u_3=(1,-1,-1)$；各自只允许乘非零常数。

efficiency_tags[0]

两两垂直的验证标注

efficiency_tags[1]

行列式 $6\ne0$ 的线性无关验证

## eval-linalg-031-s1

problem

设 4 阶矩阵 $A$ 的最小多项式为 $m_A(\lambda)=(\lambda-2)^2(\lambda-3)$,且 $\operatorname{tr}(A)=9$。求 $A$ 的所有可能若尔当标准形,并说明最小多项式如何决定各若尔当块的最大阶数。

solution

$m_A$ 的根为 $2,3$,故 $A$ 的谱为 $\{2,3\}$。因子 $(\lambda-2)^2$ 表明 2 对应若尔当块的最大阶数为 2(且恰有一块取到 2 阶);因子 $(\lambda-3)$ 无平方,表明 3 对应块全为 1 阶。$n=4$ 且 3 的重数至少为 1,故 2 的重数为 2 或 3。若 2 重数为 2:块为 $J_2(2)\oplus J_1(3)\oplus J_1(3)$,迹 $=2+2+3+3=10\neq 9$,排除。若 2 重数为 3:块为 $J_2(2)\oplus J_1(2)\oplus J_1(3)$,共 $2+1+1=4$ 阶,迹 $=2+2+2+3=9$,符合。故唯一。

answer

唯一:$\operatorname{diag}\!\bigl(J_2(2),\,2,\,3\bigr)=\begin{pmatrix}2&1&0&0\\0&2&0&0\\0&0&2&0\\0&0&0&3\end{pmatrix}$,其中 $J_2(2)=\begin{pmatrix}2&1\\0&2\end{pmatrix}$

scene_spec.objects[0]

若尔当块按 $(\lambda-2)^2$、$(\lambda-3)$ 的阶数约束拼图

scene_spec.objects[1]

迹 9 排除 $10$ 的组合

scene_spec.steps[0]

第一步：以最小多项式定最大块阶为主线，建立高等代数·λ-矩阵场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：若尔当块按 $(\lambda-2)^2$、$(\lambda-3)$ 的阶数约束拼图。

scene_spec.steps[2]

第三步：迹 9 排除 $10$ 的组合。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

若尔当块按 $(\lambda-2)^2$、$(\lambda-3)$ 的阶数约束拼图

efficiency_tags[1]

迹 9 排除 $10$ 的组合

## eval-linalg-031-s2

problem

设 4 阶矩阵 $A$ 的最小多项式为 $m_A(\lambda)=(\lambda-2)^2(\lambda-3)$,且 $\operatorname{tr}(A)=9$。求 $A$ 的所有可能若尔当标准形,并说明最小多项式如何决定各若尔当块的最大阶数。

solution

特征多项式 $f_A$ 与 $m_A$ 有相同根,$f_A=(\lambda-2)^{r_2}(\lambda-3)^{r_3}$,$r_2+r_3=4$,$r_2\ge 2$,$r_3\ge 1$,故 $(r_2,r_3)=(3,1)$ 或 $(2,2)$。迹 $=2r_2+3r_3$:$(3,1)$ 给 $6+3=9$;$(2,2)$ 给 $4+6=10$。故 $r_2=3,r_3=1$。2 的块:最大块阶为 2(由 $(\lambda-2)^2$ 整除 $m_A$)且总维数为 3,故块大小拆分为 $2+1$,即 $J_2(2)\oplus J_1(2)$;3 的块为 $J_1(3)$。故唯一:$\operatorname{diag}\!\bigl(J_2(2),2,3\bigr)$。

answer

唯一:$\operatorname{diag}\!\bigl(J_2(2),\,2,\,3\bigr)=\begin{pmatrix}2&1&0&0\\0&2&0&0\\0&0&2&0\\0&0&0&3\end{pmatrix}$,其中 $J_2(2)=\begin{pmatrix}2&1\\0&2\end{pmatrix}$

scene_spec.objects[0]

重数分配 $(3,1)$ 与 $(2,2)$ 的分支图

scene_spec.objects[1]

迹公式 $2r_2+3r_3$ 的对照表

scene_spec.steps[0]

第一步：以特征多项式与迹联立为主线，建立高等代数·λ-矩阵场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：重数分配 $(3,1)$ 与 $(2,2)$ 的分支图。

scene_spec.steps[2]

第三步：迹公式 $2r_2+3r_3$ 的对照表。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

重数分配 $(3,1)$ 与 $(2,2)$ 的分支图

efficiency_tags[1]

迹公式 $2r_2+3r_3$ 的对照表

## eval-linalg-031-s3

problem

设 4 阶矩阵 $A$ 的最小多项式为 $m_A(\lambda)=(\lambda-2)^2(\lambda-3)$,且 $\operatorname{tr}(A)=9$。求 $A$ 的所有可能若尔当标准形,并说明最小多项式如何决定各若尔当块的最大阶数。

solution

$m_A$ 的两个互素因子给出主分解 $V=\ker(A-2I)^2\oplus\ker(A-3I)$。$\ker(A-3I)$ 的维数等于 3 的重数 $r_3$;$\ker(A-2I)^2$ 的维数等于 2 的重数 $r_2$。由 $r_2+r_3=4$、$r_2\ge 2$、$r_3\ge 1$ 与迹 $2r_2+3r_3=9$ 得 $r_2=3,\ r_3=1$。在 $V_2=\ker(A-2I)^2$ 上,幂零部分 $N=A-2I$ 满足 $N^2=0$ 且 $N\neq 0$($N=0$ 会给 $m_A$ 带来因子 $(\lambda-2)$ 而非 $(\lambda-2)^2$),故 $N$ 的幂零指数恰为 2,$V_2$ 上的块为 $J_2(2)\oplus J_1(2)$;$V_3$ 一维,块为 $J_1(3)$。故唯一:$\operatorname{diag}\!\bigl(J_2(2),2,3\bigr)$。

answer

唯一:$\operatorname{diag}\!\bigl(J_2(2),\,2,\,3\bigr)=\begin{pmatrix}2&1&0&0\\0&2&0&0\\0&0&2&0\\0&0&0&3\end{pmatrix}$,其中 $J_2(2)=\begin{pmatrix}2&1\\0&2\end{pmatrix}$

scene_spec.objects[0]

主分解 $V_2\oplus V_3$ 的子空间示意

scene_spec.objects[1]

幂零指数 2(块阶上限)与维数 3 定出 $2+1$ 拆分

scene_spec.steps[0]

第一步：以主分解为主线，建立高等代数·λ-矩阵场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：主分解 $V_2\oplus V_3$ 的子空间示意。

scene_spec.steps[2]

第三步：幂零指数 2(块阶上限)与维数 3 定出 $2+1$ 拆分。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

主分解 $V_2\oplus V_3$ 的子空间示意

efficiency_tags[1]

幂零指数 2(块阶上限)与维数 3 定出 $2+1$ 拆分

## eval-linalg-032-s1

problem

设 $a\in\mathbb R$ 为参数,$\lambda$-矩阵 $A(\lambda)=\begin{pmatrix}\lambda-a&1&0\\0&\lambda-1&1\\0&0&\lambda-1\end{pmatrix}$。求 $A(\lambda)$ 的不变因子与初等因子,并讨论 $a$ 的取值如何影响初等因子(何时两个不同根的初等因子合并、重数如何变化)。

solution

一阶行列式因子 $D_1=1$。二阶子式中含 $\begin{vmatrix}1&0\\\lambda-1&1\end{vmatrix}=1$,故二阶行列式因子 $D_2=\gcd(\cdots,1,\cdots)=1$。三阶行列式因子 $D_3=|A(\lambda)|=(\lambda-a)(\lambda-1)^2$。不变因子 $d_1=D_1=1$,$d_2=\dfrac{D_2}{D_1}=1$,$d_3=\dfrac{D_3}{D_2}=(\lambda-a)(\lambda-1)^2$。初等因子即不变因子分解出的互异幂因子:$a\neq 1$ 时 $d_3$ 给出 $\lambda-a$ 与 $(\lambda-1)^2$ 两个初等因子;$a=1$ 时 $\lambda-a$ 与 $(\lambda-1)^2$ 的根重合,$d_3=(\lambda-1)^3$ 成为一个三重初等因子。

answer

不变因子:$1,\ 1,\ (\lambda-a)(\lambda-1)^2$;初等因子:$a\neq 1$ 时为 $\lambda-a$ 与 $(\lambda-1)^2$;$a=1$ 时为 $(\lambda-1)^3$

scene_spec.objects[0]

全部二阶子式 $\gcd=1$ 的逐一检验

scene_spec.objects[1]

$a$ 滑杆下 $(\lambda-a)$ 与 $(\lambda-1)$ 的根逐渐重合

scene_spec.steps[0]

第一步：以行列式因子为主线，建立高等代数·λ-矩阵场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：全部二阶子式 $\gcd=1$ 的逐一检验。

scene_spec.steps[2]

第三步：$a$ 滑杆下 $(\lambda-a)$ 与 $(\lambda-1)$ 的根逐渐重合。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

全部二阶子式 $\gcd=1$ 的逐一检验

efficiency_tags[1]

$a$ 滑杆下 $(\lambda-a)$ 与 $(\lambda-1)$ 的根逐渐重合

## eval-linalg-032-s2

problem

设 $a\in\mathbb R$ 为参数,$\lambda$-矩阵 $A(\lambda)=\begin{pmatrix}\lambda-a&1&0\\0&\lambda-1&1\\0&0&\lambda-1\end{pmatrix}$。求 $A(\lambda)$ 的不变因子与初等因子,并讨论 $a$ 的取值如何影响初等因子(何时两个不同根的初等因子合并、重数如何变化)。

solution

交换第 1、2 列得 $\begin{pmatrix}1&\lambda-a&0\\\lambda-1&0&1\\0&0&\lambda-1\end{pmatrix}$;第 2 行减去第 1 行的 $(\lambda-1)$ 倍、第 2 列减去第 1 列的 $(\lambda-a)$ 倍,得 $\begin{pmatrix}1&0&0\\0&-(\lambda-a)(\lambda-1)&1\\0&0&\lambda-1\end{pmatrix}$;再交换第 2、3 列,第 3 行减去第 2 行的 $(\lambda-1)$ 倍,第 3 列加回第 2 列的 $(\lambda-a)(\lambda-1)$ 倍,得标准形 $\operatorname{diag}\!\bigl(1,\,1,\,(\lambda-a)(\lambda-1)^2\bigr)$。不变因子读出 $1,\ 1,\ (\lambda-a)(\lambda-1)^2$。末项分解得初等因子:$a\neq 1$ 时为 $\lambda-a$ 与 $(\lambda-1)^2$ 两个;$a=1$ 时两者根重合,合并为 $(\lambda-1)^3$ 一个。

answer

不变因子:$1,\ 1,\ (\lambda-a)(\lambda-1)^2$;初等因子:$a\neq 1$ 时为 $\lambda-a$ 与 $(\lambda-1)^2$;$a=1$ 时为 $(\lambda-1)^3$

scene_spec.objects[0]

行、列初等变换分别逐步动画(Smith 形)

scene_spec.objects[1]

标准形 $\operatorname{diag}(1,1,(\lambda-a)(\lambda-1)^2)$ 的生成

scene_spec.steps[0]

第一步：以初等变换化标准形为主线，建立高等代数·λ-矩阵场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：行、列初等变换分别逐步动画(Smith 形)。

scene_spec.steps[2]

第三步：标准形 $\operatorname{diag}(1,1,(\lambda-a)(\lambda-1)^2)$ 的生成。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

行、列初等变换分别逐步动画(Smith 形)

efficiency_tags[1]

标准形 $\operatorname{diag}(1,1,(\lambda-a)(\lambda-1)^2)$ 的生成

## eval-linalg-032-s3

problem

设 $a\in\mathbb R$ 为参数,$\lambda$-矩阵 $A(\lambda)=\begin{pmatrix}\lambda-a&1&0\\0&\lambda-1&1\\0&0&\lambda-1\end{pmatrix}$。求 $A(\lambda)$ 的不变因子与初等因子,并讨论 $a$ 的取值如何影响初等因子(何时两个不同根的初等因子合并、重数如何变化)。

solution

令 $B(a)=\begin{pmatrix}a&-1&0\\0&1&-1\\0&0&1\end{pmatrix}$,则 $A(\lambda)=\lambda I-B(a)$。取 $e_3=(0,0,1)^T$,直接计算: $$(e_3,\ B e_3,\ B^2 e_3)=\begin{pmatrix}0&0&1\\0&-1&-2\\1&1&1\end{pmatrix},\qquad \det=1\neq 0,$$ 故 $\{e_3,Be_3,B^2e_3\}$ 构成基,$e_3$ 对所有 $a$ 都是 $B$ 的循环向量,因此 $m_B$ 的次数为 3,与特征多项式 $\chi_B(\lambda)=(\lambda-a)(\lambda-1)^2$ 相同,即 $m_B=\chi_B$。于是 $A(\lambda)$ 的不变因子为 $1,\ 1,\ (\lambda-a)(\lambda-1)^2$(唯一非平凡不变因子等于特征多项式)。初等因子:$a\neq 1$ 时为 $\lambda-a$ 与 $(\lambda-1)^2$,对应块 $\operatorname{diag}\!\bigl(a,\,J_2(1)\bigr)$,其中 $J_2(1)=\begin{pmatrix}1&1\\0&1\end{pmatrix}$;$a=1$ 时合并为 $(\lambda-1)^3$,对应块 $J_3(1)=\begin{pmatrix}1&1&0\\0&1&1\\0&0&1\end{pmatrix}$。**所有参数取值下均不可对角化**($a\neq 1$ 时已含 $J_2(1)$ 块);$a$ 从 $\neq 1$ 变到 1 时,变化是初等因子合并、最大若尔当块由二阶升为三阶。

answer

不变因子:$1,\ 1,\ (\lambda-a)(\lambda-1)^2$;初等因子:$a\neq 1$ 时为 $\lambda-a$ 与 $(\lambda-1)^2$;$a=1$ 时为 $(\lambda-1)^3$

scene_spec.objects[0]

在原参数矩阵上展示特征值合并、特征方向趋于重合

scene_spec.objects[1]

块结构 $J_1(a)\oplus J_2(1)$ 向 $J_3(1)$ 的突变(全程不可对角化)

scene_spec.steps[0]

第一步：以循环向量独立推导为主线，建立高等代数·λ-矩阵场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：在原参数矩阵上展示特征值合并、特征方向趋于重合。

scene_spec.steps[2]

第三步：块结构 $J_1(a)\oplus J_2(1)$ 向 $J_3(1)$ 的突变(全程不可对角化)。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

在原参数矩阵上展示特征值合并、特征方向趋于重合

efficiency_tags[1]

块结构 $J_1(a)\oplus J_2(1)$ 向 $J_3(1)$ 的突变(全程不可对角化)

## eval-linalg-033-s1

problem

设 $A=\begin{pmatrix}0&1\\0&0\end{pmatrix}$，求矩阵指数 $e^{tA}$（$t$ 为参数）。

solution

$A^2=\begin{pmatrix}0&1\\0&0\end{pmatrix}\begin{pmatrix}0&1\\0&0\end{pmatrix}=0$，故 $A^k=0$（$k\ge 2$）。$e^{tA}=I+tA+\dfrac{t^2A^2}{2!}+\cdots=I+tA=\begin{pmatrix}1&t\\0&1\end{pmatrix}$。

answer

$e^{tA}=\begin{pmatrix}1&t\\0&1\end{pmatrix}$

scene_spec.objects[0]

级数展开只留两项（$A^2=0$）的标注

scene_spec.objects[1]

$e^{tA}=I+tA$ 的生成

scene_spec.steps[0]

第一步：以级数定义为主线，建立高等代数·矩阵函数场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：级数展开只留两项（$A^2=0$）的标注。

scene_spec.steps[2]

第三步：$e^{tA}=I+tA$ 的生成。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

级数展开只留两项（$A^2=0$）的标注

efficiency_tags[1]

$e^{tA}=I+tA$ 的生成

## eval-linalg-033-s2

problem

设 $A=\begin{pmatrix}0&1\\0&0\end{pmatrix}$，求矩阵指数 $e^{tA}$（$t$ 为参数）。

solution

方程组 $\dfrac{d}{dt}\begin{pmatrix}x\\y\end{pmatrix}=A\begin{pmatrix}x\\y\end{pmatrix}$，即 $\begin{cases}x'=y\\y'=0\end{cases}$。解得 $y(t)=y_0$，$x(t)=x_0+y_0t$，即 $\begin{pmatrix}x\\y\end{pmatrix}=\begin{pmatrix}1&t\\0&1\end{pmatrix}\begin{pmatrix}x_0\\y_0\end{pmatrix}$。基解矩阵（满足 $\Phi(0)=I$）即 $e^{tA}=\begin{pmatrix}1&t\\0&1\end{pmatrix}$。

answer

$e^{tA}=\begin{pmatrix}1&t\\0&1\end{pmatrix}$

scene_spec.objects[0]

方程组 $x'=y$、$y'=0$ 的求解

scene_spec.objects[1]

基解矩阵的生成

scene_spec.steps[0]

第一步：以解微分方程组为主线，建立高等代数·矩阵函数场景并呈现该解法的关键图形。

scene_spec.steps[1]

第二步：方程组 $x'=y$、$y'=0$ 的求解。

scene_spec.steps[2]

第三步：基解矩阵的生成。

scene_spec.steps[3]

第四步：高亮最终结果与答案。

efficiency_tags[0]

方程组 $x'=y$、$y'=0$ 的求解

efficiency_tags[1]

基解矩阵的生成

## eval-linalg-033-s3

problem

设 $A=\begin{pmatrix}0&1\\0&0\end{pmatrix}$，求矩阵指数 $e^{tA}$（$t$ 为参数）。

solution

$(sI-A)^{-1}=\begin{pmatrix}s&-1\\0&s\end{pmatrix}^{-1}=\dfrac{1}{s^2}\begin{pmatrix}s&1\\0&s\end{pmatrix}=\begin{pmatrix}1/s&1/s^2\\0&1/s\end{pmatrix}$。逐项取拉普拉斯逆变换（$\mathcal L^{-1}\{1/s\}=1$，$\mathcal L^{-1}\{1/s^2\}=t$），得 $e^{tA}=\begin{pmatrix}1&t\\0&1\end{pmatrix}$。单边Laplace逆变换先给$t\ge0$的结果。候选$\Phi(t)=I+tA$对全部实$t$满足$\Phi^{\prime}=A\Phi$、$\Phi(0)=I$，由线性常微分方程初值问题唯一性，$\Phi(t)=e^{tA}$对全部实$t$成立。

answer

$e^{tA}=\begin{pmatrix}1&t\\0&1\end{pmatrix}$

scene_spec.objects[0]

预解式 $(sI-A)^{-1}=\begin{pmatrix}1/s&1/s^2\\0&1/s\end{pmatrix}$ 的逆变换

scene_spec.objects[1]

相图：剪切流轨道

scene_spec.steps[0]

呈现题干及适用条件：设 $A=\begin{pmatrix}0&1\\0&0\end{pmatrix}$，求矩阵指数 $e^{tA}$（$t$ 为参数）。

scene_spec.steps[1]

依次呈现：预解式 $(sI-A)^{-1}=\begin{pmatrix}1/s&1/s^2\\0&1/s\end{pmatrix}$ 的逆变换

scene_spec.steps[2]

依次呈现：相图：剪切流轨道

scene_spec.steps[3]

核对完整证明：$(sI-A)^{-1}=\begin{pmatrix}s&-1\\0&s\end{pmatrix}^{-1}=\dfrac{1}{s^2}\begin{pmatrix}s&1\\0&s\end{pmatrix}=\begin{pmatrix}1/s&1/s^2\\0&1/s\end{pmatrix}$。逐项取拉普拉斯逆变换（$\mathcal L^{-1}\{1/s\}=1$，$\mathcal L^{-1}\{1/s^2\}=t$），得 $e^{tA}=\begin{pmatrix}1&t\\0&1\end{pmatrix}$。单边Laplace逆变换先给$t\ge0$的结果。候选$\Phi(t)=I+tA$对全部实$t$满足$\Phi^{\prime}=A\Phi$、$\Phi(0)=I$，由线性常微分方程初值问题唯一性，$\Phi(t)=e^{tA}$对全部实$t$成立。

scene_spec.steps[4]

高亮结果：$e^{tA}=\begin{pmatrix}1&t\\0&1\end{pmatrix}$

efficiency_tags[0]

预解式 $(sI-A)^{-1}=\begin{pmatrix}1/s&1/s^2\\0&1/s\end{pmatrix}$ 的逆变换

efficiency_tags[1]

相图：剪切流轨道

## eval-linalg-034-s1

problem

证明 Cauchy–Schwarz 不等式：对任意向量 $\vec a,\vec b$，$|\vec a\cdot\vec b|\le|\vec a||\vec b|$。

solution

若 $\vec b=\vec 0$ 不等式平凡成立。设 $\vec b\ne\vec 0$，对任意实数 $t$，$0\le|\vec a+t\vec b|^2=|\vec a|^2+2t(\vec a\cdot\vec b)+t^2|\vec b|^2$。该二次函数恒非负，故判别式 $\Delta=4(\vec a\cdot\vec b)^2-4|\vec a|^2|\vec b|^2\le 0$，即 $(\vec a\cdot\vec b)^2\le|\vec a|^2|\vec b|^2$，开方得 $|\vec a\cdot\vec b|\le|\vec a||\vec b|$。等号成立当且仅当 $\vec a+t\vec b=\vec 0$（$\vec a$ 与 $\vec b$ 线性相关）。

answer

$|\vec a\cdot\vec b|\le|\vec a||\vec b|$；等号当且仅当两向量线性相关（包括零向量）。

scene_spec.objects[0]

判别式 $\Delta\le0$ 的推导

scene_spec.objects[1]

二次函数恒非负的抛物线

scene_spec.steps[0]

呈现题干及适用条件：证明 Cauchy–Schwarz 不等式：对任意向量 $\vec a,\vec b$，$|\vec a\cdot\vec b|\le|\vec a||\vec b|$。

scene_spec.steps[1]

依次呈现：判别式 $\Delta\le0$ 的推导

scene_spec.steps[2]

依次呈现：二次函数恒非负的抛物线

scene_spec.steps[3]

核对完整证明：若 $\vec b=\vec 0$ 不等式平凡成立。设 $\vec b\ne\vec 0$，对任意实数 $t$，$0\le|\vec a+t\vec b|^2=|\vec a|^2+2t(\vec a\cdot\vec b)+t^2|\vec b|^2$。该二次函数恒非负，故判别式 $\Delta=4(\vec a\cdot\vec b)^2-4|\vec a|^2|\vec b|^2\le 0$，即 $(\vec a\cdot\vec b)^2\le|\vec a|^2|\vec b|^2$，开方得 $|\vec a\cdot\vec b|\le|\vec a||\vec b|$。等号成立当且仅当 $\vec a+t\vec b=\vec 0$（$\vec a$ 与 $\vec b$ 线性相关）。

scene_spec.steps[4]

高亮结果：$|\vec a\cdot\vec b|\le|\vec a||\vec b|$；等号当且仅当两向量线性相关（包括零向量）。

efficiency_tags[0]

判别式 $\Delta\le0$ 的推导

efficiency_tags[1]

二次函数恒非负的抛物线

## eval-linalg-034-s2

problem

证明 Cauchy–Schwarz 不等式：对任意向量 $\vec a,\vec b$，$|\vec a\cdot\vec b|\le|\vec a||\vec b|$。

solution

若 $\vec b=\vec 0$ 不等式平凡成立。以下设 $\vec b\ne\vec 0$，把 $\vec a$ 分解为 $\vec a=\vec a_\parallel+\vec a_\perp$，其中 $\vec a_\parallel=\dfrac{\vec a\cdot\vec b}{|\vec b|^2}\vec b$ 与 $\vec b$ 平行，$\vec a_\perp\perp\vec b$。由勾股定理 $|\vec a|^2=|\vec a_\parallel|^2+|\vec a_\perp|^2\ge|\vec a_\parallel|^2=\dfrac{(\vec a\cdot\vec b)^2}{|\vec b|^2}$，移项即得。等号成立当且仅当 $\vec a_\perp=\vec 0$。

answer

$|\vec a\cdot\vec b|\le|\vec a||\vec b|$；等号当且仅当两向量线性相关（包括零向量）。

scene_spec.objects[0]

正交投影分解动画

scene_spec.objects[1]

勾股定理 $|\vec a|^2\ge|\vec a_\parallel|^2$ 的标注

scene_spec.steps[0]

呈现题干及适用条件：证明 Cauchy–Schwarz 不等式：对任意向量 $\vec a,\vec b$，$|\vec a\cdot\vec b|\le|\vec a||\vec b|$。

scene_spec.steps[1]

依次呈现：正交投影分解动画

scene_spec.steps[2]

依次呈现：勾股定理 $|\vec a|^2\ge|\vec a_\parallel|^2$ 的标注

scene_spec.steps[3]

核对完整证明：若 $\vec b=\vec 0$ 不等式平凡成立。以下设 $\vec b\ne\vec 0$，把 $\vec a$ 分解为 $\vec a=\vec a_\parallel+\vec a_\perp$，其中 $\vec a_\parallel=\dfrac{\vec a\cdot\vec b}{|\vec b|^2}\vec b$ 与 $\vec b$ 平行，$\vec a_\perp\perp\vec b$。由勾股定理 $|\vec a|^2=|\vec a_\parallel|^2+|\vec a_\perp|^2\ge|\vec a_\parallel|^2=\dfrac{(\vec a\cdot\vec b)^2}{|\vec b|^2}$，移项即得。等号成立当且仅当 $\vec a_\perp=\vec 0$。

scene_spec.steps[4]

高亮结果：$|\vec a\cdot\vec b|\le|\vec a||\vec b|$；等号当且仅当两向量线性相关（包括零向量）。

efficiency_tags[0]

正交投影分解动画

efficiency_tags[1]

勾股定理 $|\vec a|^2\ge|\vec a_\parallel|^2$ 的标注

## eval-linalg-034-s3

problem

证明 Cauchy–Schwarz 不等式：对任意向量 $\vec a,\vec b$，$|\vec a\cdot\vec b|\le|\vec a||\vec b|$。

solution

设$\vec a,\vec b\in\mathbb R^n$，取均匀样本空间$\{1,\ldots,n\}$，定义$X(i)=a_i,\ Y(i)=b_i$。于是$E[X^2]=|\vec a|^2/n$、$E[Y^2]=|\vec b|^2/n$、$E[XY]=(\vec a\cdot\vec b)/n$，不作中心化。若$E[Y^2]=0$，则$\vec b=0$，不等式成立。否则由$E[(X-tY)^2]\ge0$，在$t=E[XY]/E[Y^2]$处得$E[X^2]-(E[XY])^2/E[Y^2]\ge0$，代回并开方即得$|\vec a\cdot\vec b|\le|\vec a||\vec b|$。等号当且仅当$X=tY$在每个样本点成立，或$\vec b=0$，也就是两向量线性相关。

answer

$|\vec a\cdot\vec b|\le|\vec a||\vec b|$；等号当且仅当两向量线性相关（包括零向量）。

scene_spec.objects[0]

二阶矩矩阵半正定的标注

scene_spec.objects[1]

等号条件（共线/退化）的标注

scene_spec.steps[0]

呈现题干及适用条件：证明 Cauchy–Schwarz 不等式：对任意向量 $\vec a,\vec b$，$|\vec a\cdot\vec b|\le|\vec a||\vec b|$。

scene_spec.steps[1]

依次呈现：二阶矩矩阵半正定的标注

scene_spec.steps[2]

依次呈现：等号条件（共线/退化）的标注

scene_spec.steps[3]

核对完整证明：设$\vec a,\vec b\in\mathbb R^n$，取均匀样本空间$\{1,\ldots,n\}$，定义$X(i)=a_i,\ Y(i)=b_i$。于是$E[X^2]=|\vec a|^2/n$、$E[Y^2]=|\vec b|^2/n$、$E[XY]=(\vec a\cdot\vec b)/n$，不作中心化。若$E[Y^2]=0$，则$\vec b=0$，不等式成立。否则由$E[(X-tY)^2]\ge0$，在$t=E[XY]/E[Y^2]$处得$E[X^2]-(E[XY])^2/E[Y^2]\ge0$，代回并开方即得$|\vec a\cdot\vec b|\le|\vec a||\vec b|$。等号当且仅当$X=tY$在每个样本点成立，或$\vec b=0$，也就是两向量线性相关。

scene_spec.steps[4]

高亮结果：$|\vec a\cdot\vec b|\le|\vec a||\vec b|$；等号当且仅当两向量线性相关（包括零向量）。

efficiency_tags[0]

二阶矩矩阵半正定的标注

efficiency_tags[1]

等号条件（共线/退化）的标注

## eval-linalg-035-s1

problem

证明：$n$ 阶实方阵 $A$ 是正交矩阵（$A^TA=I$）当且仅当 $A$ 的列向量构成 $\mathbb R^n$ 的标准正交基。

solution

把 $A$ 按列分块 $A=(a_1,a_2,\dots,a_n)$。$A^TA$ 的 $(i,j)$ 元为 $a_i^Ta_j=a_i\cdot a_j$。$A^TA=I\iff a_i\cdot a_j=\delta_{ij}$ 对一切 $i,j$ 成立 $\iff$ 列向量两两正交且都是单位向量 $\iff$ 列向量构成标准正交基（$n$ 个两两正交的单位向量必线性无关，因若 $\sum c_ia_i=0$ 则与 $a_j$ 作内积得 $c_j=0$）。

answer

$A^TA=I\iff$列向量构成$\mathbb R^n$的标准正交基。

scene_spec.objects[0]

分块 $A^TA$ 的 $(i,j)$ 元 $a_i\cdot a_j$ 标注

scene_spec.objects[1]

线性无关性的验证

scene_spec.steps[0]

呈现题干及适用条件：证明：$n$ 阶实方阵 $A$ 是正交矩阵（$A^TA=I$）当且仅当 $A$ 的列向量构成 $\mathbb R^n$ 的标准正交基。

scene_spec.steps[1]

依次呈现：分块 $A^TA$ 的 $(i,j)$ 元 $a_i\cdot a_j$ 标注

scene_spec.steps[2]

依次呈现：线性无关性的验证

scene_spec.steps[3]

核对完整证明：把 $A$ 按列分块 $A=(a_1,a_2,\dots,a_n)$。$A^TA$ 的 $(i,j)$ 元为 $a_i^Ta_j=a_i\cdot a_j$。$A^TA=I\iff a_i\cdot a_j=\delta_{ij}$ 对一切 $i,j$ 成立 $\iff$ 列向量两两正交且都是单位向量 $\iff$ 列向量构成标准正交基（$n$ 个两两正交的单位向量必线性无关，因若 $\sum c_ia_i=0$ 则与 $a_j$ 作内积得 $c_j=0$）。

scene_spec.steps[4]

高亮结果：$A^TA=I\iff$列向量构成$\mathbb R^n$的标准正交基。

efficiency_tags[0]

分块 $A^TA$ 的 $(i,j)$ 元 $a_i\cdot a_j$ 标注

efficiency_tags[1]

线性无关性的验证

## eval-linalg-035-s2

problem

证明：$n$ 阶实方阵 $A$ 是正交矩阵（$A^TA=I$）当且仅当 $A$ 的列向量构成 $\mathbb R^n$ 的标准正交基。

solution

$A^TA=I\iff$ 对任意 $x$，$|Ax|^2=(Ax)^T(Ax)=x^TA^TAx=x^Tx=|x|^2$，即 $A$ 保长。由极化恒等式 $(Ax,Ay)=\dfrac{|A(x+y)|^2-|Ax|^2-|Ay|^2}{2}=\dfrac{|x+y|^2-|x|^2-|y|^2}{2}=(x,y)$，保长⇒保内积。取 $x=e_i$、$y=e_j$：$(Ae_i,Ae_j)=(e_i,e_j)=\delta_{ij}$，即列向量标准正交。反之列向量标准正交⇒$A^TA=I$ 由解法一。

answer

$A^TA=I\iff$列向量构成$\mathbb R^n$的标准正交基。

scene_spec.objects[0]

保长性质的演示

scene_spec.objects[1]

极化恒等式的推导

scene_spec.steps[0]

呈现题干及适用条件：证明：$n$ 阶实方阵 $A$ 是正交矩阵（$A^TA=I$）当且仅当 $A$ 的列向量构成 $\mathbb R^n$ 的标准正交基。

scene_spec.steps[1]

依次呈现：保长性质的演示

scene_spec.steps[2]

依次呈现：极化恒等式的推导

scene_spec.steps[3]

核对完整证明：$A^TA=I\iff$ 对任意 $x$，$|Ax|^2=(Ax)^T(Ax)=x^TA^TAx=x^Tx=|x|^2$，即 $A$ 保长。由极化恒等式 $(Ax,Ay)=\dfrac{|A(x+y)|^2-|Ax|^2-|Ay|^2}{2}=\dfrac{|x+y|^2-|x|^2-|y|^2}{2}=(x,y)$，保长⇒保内积。取 $x=e_i$、$y=e_j$：$(Ae_i,Ae_j)=(e_i,e_j)=\delta_{ij}$，即列向量标准正交。反之列向量标准正交⇒$A^TA=I$ 由解法一。

scene_spec.steps[4]

高亮结果：$A^TA=I\iff$列向量构成$\mathbb R^n$的标准正交基。

efficiency_tags[0]

保长性质的演示

efficiency_tags[1]

极化恒等式的推导

## eval-linalg-035-s3

problem

证明：$n$ 阶实方阵 $A$ 是正交矩阵（$A^TA=I$）当且仅当 $A$ 的列向量构成 $\mathbb R^n$ 的标准正交基。

solution

记标准基为$e_1,\ldots,e_n$，$A$的列为$a_i=Ae_i$。若$A^TA=I$，则$a_i\cdot a_j=e_i^TA^TAe_j=\delta_{ij}$；若$\sum_i c_i a_i=0$，分别与$a_j$取内积得$c_j=0$，所以这$n$个单位正交向量是$\mathbb R^n$的基。反过来，若列向量构成标准正交基，则$(A^TA)_{ij}=a_i\cdot a_j=\delta_{ij}$，故$A^TA=I$。行列式为$\pm1$本身不充分，例如剪切矩阵$\begin{pmatrix}1&1\\0&1\end{pmatrix}$的两列不正交；这个反例只是补充，不替代上述充要性证明。

answer

$A^TA=I\iff$列向量构成$\mathbb R^n$的标准正交基。

scene_spec.objects[0]

$a_i=Ae_i$，$a_i\cdot a_j=e_i^TA^TAe_j$

scene_spec.objects[1]

$a_i\cdot a_j=\delta_{ij}$的双向等价及线性无关性证明

scene_spec.objects[2]

剪切反例说明仅凭行列式条件不充分

scene_spec.steps[0]

呈现题干及适用条件：证明：$n$ 阶实方阵 $A$ 是正交矩阵（$A^TA=I$）当且仅当 $A$ 的列向量构成 $\mathbb R^n$ 的标准正交基。

scene_spec.steps[1]

依次呈现：$a_i=Ae_i$，$a_i\cdot a_j=e_i^TA^TAe_j$

scene_spec.steps[2]

依次呈现：$a_i\cdot a_j=\delta_{ij}$的双向等价及线性无关性证明

scene_spec.steps[3]

依次呈现：剪切反例说明仅凭行列式条件不充分

scene_spec.steps[4]

核对完整证明：记标准基为$e_1,\ldots,e_n$，$A$的列为$a_i=Ae_i$。若$A^TA=I$，则$a_i\cdot a_j=e_i^TA^TAe_j=\delta_{ij}$；若$\sum_i c_i a_i=0$，分别与$a_j$取内积得$c_j=0$，所以这$n$个单位正交向量是$\mathbb R^n$的基。反过来，若列向量构成标准正交基，则$(A^TA)_{ij}=a_i\cdot a_j=\delta_{ij}$，故$A^TA=I$。行列式为$\pm1$本身不充分，例如剪切矩阵$\begin{pmatrix}1&1\\0&1\end{pmatrix}$的两列不正交；这个反例只是补充，不替代上述充要性证明。

scene_spec.steps[5]

高亮结果：$A^TA=I\iff$列向量构成$\mathbb R^n$的标准正交基。

efficiency_tags[0]

$a_i=Ae_i$，$a_i\cdot a_j=e_i^TA^TAe_j$

efficiency_tags[1]

$a_i\cdot a_j=\delta_{ij}$的双向等价及线性无关性证明

efficiency_tags[2]

剪切反例说明仅凭行列式条件不充分
