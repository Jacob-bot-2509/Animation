# dataset-eval（同题多解 · 思路展开）· 审阅稿 v1

> 状态：**已转 JSON/JSONL**（data/v1/eval/dataset_eval.{json,jsonl}，300 行 = 100 题×3 解法，2026-10-03 用户指示）；**已冻结**（data/{eval,test}-v1.lock.json，绑定顶层 manifest）。内容经复查整改（reviews/2026-10-03-math-review/）。
> 规模：100 题（数学分析 30 / 解析几何 20 / 概率论 15 / 高等代数 35），每题 ≥2 种解法。
> 转 JSONL 的字段映射（内容定稿后执行，契约见 EVAL_TEST_PREP.md §3.5）：
> - 标题行 `### <problem_id>  <category> · <sub_category>` → problem_id / category / sub_category；
> - `**题目**` → problem；`**答案**` → answer；
> - `**解法k（方法名）**` → 一行 JSONL：solution_id = `<problem_id>-s<k>`，method = 方法名，solution = 该解法全文；
> - `**思路展开**` / `**动画要点**` 为审阅辅助：思路展开说明多解对比与切入点；scene_spec 在内容定稿后按动画要点逐条补写。
> source 待用户定（建议 self-authored）；license = Internal-Research-Use-Only。
> 隔离约定：与 data/v1/raw 训练集 63 条题目族不同、ID 不重叠（eval-* 前缀）。

# 一、数学分析（30 题）

### eval-calc-001 数学分析 · 极限
**题目** 求极限 $\displaystyle\lim_{x\to 0}\frac{1-\cos x}{x^2}$。
**答案** $\dfrac{1}{2}$
**解法一（半角公式）** 由 $1-\cos x = 2\sin^2\dfrac{x}{2}$，得 $\dfrac{1-\cos x}{x^2}=\dfrac{2\sin^2(x/2)}{x^2}=\dfrac{1}{2}\left(\dfrac{\sin(x/2)}{x/2}\right)^2$。令 $t=x/2\to 0$，利用 $\lim_{t\to 0}\dfrac{\sin t}{t}=1$，故原式 $=\dfrac{1}{2}\cdot 1^2=\dfrac{1}{2}$。
**解法二（泰勒展开）** $\cos x = 1-\dfrac{x^2}{2}+\dfrac{x^4}{24}+o(x^4)$，故 $1-\cos x = \dfrac{x^2}{2}+o(x^2)$，原式 $=\lim_{x\to 0}\dfrac{x^2/2+o(x^2)}{x^2}=\dfrac{1}{2}$。
**解法三（洛必达法则）** 原式为 $\dfrac{0}{0}$ 型。第一次求导：$\lim_{x\to 0}\dfrac{\sin x}{2x}$；第二次求导：$\lim_{x\to 0}\dfrac{\cos x}{2}=\dfrac{1}{2}$。
**思路展开** 三种方法从三个不同视角刻画同一个极限：半角公式走三角恒等式（几何面积思想）、泰勒展开走局部多项式逼近（用 $1-x^2/2$ 在二阶接触的意义上替代 $\cos x$）、洛必达走微分算子的比值。动画切入也相应不同——半角法适合在单位圆中演示 $1-\cos x$ 与 $x^2/2$ 的面积比较，泰勒法适合放大原点附近展示 $\cos x$ 与抛物线二阶接触，洛必达法适合做分子分母比值的动态表格。对模型而言，同题三解要求输出三种不同结构的 scene_spec，考验动画规划与解法结构的绑定能力。
**解法一动画要点** - 单位圆中半角 $x/2$ 的扇形与三角形面积 - 比值 $\dfrac{\sin(x/2)}{x/2}$ 随 $x\to0$ 逼近 1 的动画 - 半角恒等式 $1-\cos x=2\sin^2(x/2)$ 的标注
**解法二动画要点** - 原点邻域放大：$y=\cos x$ 与 $y=1-x^2/2$ 二阶接触 - 泰勒多项式逐项贴合曲线
**解法三动画要点** - 分子分母比值表随两次求导收敛于 $\dfrac{1}{2}$ - 洛必达两次求导的符号推导滚动

### eval-calc-002 数学分析 · 极限
**题目** 求极限 $\displaystyle\lim_{x\to 0^+} x^x$。
**答案** $1$
**解法一（对数化+变量替换）** 令 $y=x^x$，则 $\ln y = x\ln x$。令 $t=\dfrac{1}{x}\to+\infty$，则 $x\ln x = -\dfrac{\ln t}{t}\to 0$（对数函数增长慢于幂函数）。故 $\ln y\to 0$，由指数函数连续性得 $y\to e^0=1$。
**解法二（对数化+洛必达）** 同上先取对数，$x\ln x = \dfrac{\ln x}{1/x}$ 为 $\dfrac{-\infty}{+\infty}$ 型，洛必达：$\lim_{x\to 0^+}\dfrac{1/x}{-1/x^2}=\lim_{x\to 0^+}(-x)=0$，故原极限 $=e^0=1$。
**解法三（指数代换）** 令 $x=e^{-t}$（$t\to+\infty$），则 $x^x = (e^{-t})^{e^{-t}} = e^{-t e^{-t}}$，而 $t e^{-t}\to 0$，故极限为 $e^0=1$。
**思路展开** 三种解法共享同一个本质：先把幂指函数对数化为乘积 $x\ln x$，再证明 $x\ln x\to 0$。解法一的 $t=1/x$ 代换把 $0^+$ 邻域的问题拉到 $+\infty$ 去处理，解法二留在原邻域用洛必达，解法三的 $x=e^{-t}$ 把幂指结构整体吸收进指数里。动画上，解法三最直观：可以展示 $x^x$ 在 $(0,1)$ 上的完整图像（极小值点在 $x=1/e$ 处），并放大 $x\to 0^+$ 的右端趋近 $(0,1)$ 的过程；解法一、二可配对数坐标与 $\ln x/x$ 的衰减曲线。
**解法一动画要点** - $t=\dfrac{1}{x}$ 代换把 $0^+$ 邻域拉到 $+\infty$ 的坐标动画 - $y=\dfrac{\ln t}{t}$ 随 $t\to\infty$ 衰减到 0 的曲线
**解法二动画要点** - $\dfrac{\ln x}{1/x}$ 的洛必达一次求导 - $x\ln x$ 在 $0^+$ 邻域的负值收敛曲线
**解法三动画要点** - 指数代换 $x=e^{-t}$ 的坐标压缩示意 - $y=x^x$ 全图与 $x\to0^+$ 端放大趋近 $(0,1)$

### eval-calc-003 数学分析 · 极限
**题目** 证明极限 $\displaystyle\lim_{n\to\infty}\left(1+\frac{1}{n}\right)^n$ 存在（记为 $e$），并说明它与级数 $\displaystyle\sum_{k=0}^{\infty}\frac{1}{k!}$ 的联系。
**答案** 极限存在且等于 $e=\sum_{k=0}^{\infty}\frac{1}{k!}$
**解法一（单调有界准则）** 记 $a_n=\left(1+\dfrac{1}{n}\right)^n$。由二项式展开 $a_n=\sum_{k=0}^{n}\binom{n}{k}\dfrac{1}{n^k}=\sum_{k=0}^{n}\dfrac{1}{k!}\cdot\dfrac{n(n-1)\cdots(n-k+1)}{n^k}$。比较 $a_n$ 与 $a_{n+1}$ 的展开式，第 $k$ 项因子 $\dfrac{n(n-1)\cdots(n-k+1)}{n^k}\le\dfrac{(n+1)n\cdots(n-k+2)}{(n+1)^k}$，且 $a_{n+1}$ 还多一项，故 $a_{n+1}>a_n$，数列递增。又有 $a_n\le\sum_{k=0}^{n}\dfrac{1}{k!}\le 1+1+\dfrac{1}{2}+\dfrac{1}{4}+\cdots+\dfrac{1}{2^{n-1}}<3$，故有上界。由单调有界准则，$\lim a_n$ 存在，记为 $e$。
**解法二（对数化+洛必达）** 设 $n\ln\left(1+\dfrac{1}{n}\right)=\dfrac{\ln(1+x)}{x}$，其中 $x=\dfrac{1}{n}\to 0^+$。洛必达：$\lim_{x\to 0^+}\dfrac{\ln(1+x)}{x}=\lim_{x\to 0^+}\dfrac{1}{1+x}=1$。故 $\lim n\ln(1+1/n)=1$，原极限 $=e^1$。注意此解法默认 $e$ 已由其他途径定义，适合作为验证。
**解法三（与级数定义的等价性）** 记 $c_k(n)=\left(1-\dfrac{1}{n}\right)\left(1-\dfrac{2}{n}\right)\cdots\left(1-\dfrac{k-1}{n}\right)$（约定 $c_0=c_1=1$），则 $a_n=\displaystyle\sum_{k=0}^{n}\dfrac{c_k(n)}{k!}$。每个因子都在 $(0,1]$ 内，故 $0<c_k(n)\le 1$，且对固定 $k$ 有 $c_k(n)\to 1$（$n\to\infty$）。一方面 $a_n\le\displaystyle\sum_{k=0}^{n}\dfrac{1}{k!}=:s_n$；另一方面对任意固定的 $m\le n$，$a_n\ge\displaystyle\sum_{k=0}^{m}\dfrac{c_k(n)}{k!}\to s_m$。于是 $s_m\le\liminf a_n\le\limsup a_n\le\lim s_n$，令 $m\to\infty$ 即得 $\lim a_n=\lim s_n=\displaystyle\sum_{k=0}^{\infty}\dfrac{1}{k!}$——数列极限与级数和两种构造给出同一个数 $e$。
**思路展开** 本题是"用多种工具刻画同一个数学对象"的典范：解法一在数列层面用单调有界准则证明存在性（完全初等），解法二把离散问题连续化为函数极限（快但需要 $e$ 的预定义），解法三把极限与无穷级数两种构造 $e$ 的方式打通。动画可以分屏呈现：左屏二项式展开的系数逐项长出并逼近上界 3，右屏曲线 $y=\ln(1+x)/x$ 在原点处趋于 1，底栏滚动级数 $\sum 1/k!$ 的部分和。
**解法一动画要点** - 二项展开系数柱状图逐项累加 - 数列 $a_n$ 单调递增且有上界 3 的标注 - 上界 3 的水平虚线
**解法二动画要点** - 曲线 $y=\dfrac{\ln(1+x)}{x}$ 在 $x\to0^+$ 趋于 1 - 洛必达一次求导的过程
**解法三动画要点** - 因子 $c_k(n)\to1$ 的逐项趋近动画 - 级数部分和 $s_n$ 与 $a_n$ 同框收敛于 $e$

### eval-calc-004 数学分析 · 极限
**题目** 求极限 $\displaystyle\lim_{x\to 0}\frac{\sin x-\tan x}{x^3}$。
**答案** $-\dfrac{1}{2}$
**解法一（因式分解+已知极限）** 提公因式：$\dfrac{\sin x-\tan x}{x^3}=\dfrac{\sin x\left(1-\dfrac{1}{\cos x}\right)}{x^3}=\dfrac{\sin x}{x}\cdot\dfrac{\cos x-1}{x^2}\cdot\dfrac{1}{\cos x}$。由 $\lim\dfrac{\sin x}{x}=1$、$\lim\dfrac{\cos x-1}{x^2}=-\dfrac{1}{2}$（eval-calc-001）、$\lim\dfrac{1}{\cos x}=1$，得原式 $=1\cdot\left(-\dfrac{1}{2}\right)\cdot 1=-\dfrac{1}{2}$。
**解法二（泰勒展开）** $\sin x = x-\dfrac{x^3}{6}+o(x^3)$，$\tan x = x+\dfrac{x^3}{3}+o(x^3)$，故 $\sin x-\tan x = -\dfrac{x^3}{2}+o(x^3)$，原式 $=-\dfrac{1}{2}$。
**解法三（洛必达法则）** $\dfrac{0}{0}$ 型。一阶：$\dfrac{\cos x-\sec^2 x}{3x^2}$；二阶：$\dfrac{-\sin x-2\sec^2 x\tan x}{6x}$；三阶：$\dfrac{-\cos x-2(2\sec^2 x\tan^2 x+\sec^4 x)}{6}\to \dfrac{-1-2}{6}=-\dfrac{1}{2}$。
**思路展开** 本题展示"高阶无穷小抵消"必须算到 $x^3$ 阶才能得到非零答案：$\sin x$ 与 $\tan x$ 在 $x$ 阶完全相同，一阶洛必达后分子仍为 0。解法一用因式分解把问题拆成三个已知极限的乘积（复用 eval-calc-001 的结果，体现知识复用），解法二一步到位，解法三刻意展示洛必达连求三次的繁琐——这正是"洛必达不是万能钥匙"的教学素材。动画可放大展示 $y=\sin x$、$y=\tan x$ 在原点附近几乎重合、差异是 $x^3$ 量级的细节。
**解法一动画要点** - 因式分解 $\sin x\cdot\left(1-\dfrac{1}{\cos x}\right)$ 的拆项高亮 - 三个已知极限乘积的分解式标注
**解法二动画要点** - 原点放大：$\sin x$ 与 $\tan x$ 近乎重合 - 差值曲线 $y=\sin x-\tan x$ 与 $-\dfrac{x^3}{2}$ 对比
**解法三动画要点** - 洛必达三次求导的符号推导滚动 - 分子分母比值随求导次数收敛于 $-\dfrac{1}{2}$

### eval-calc-005 数学分析 · 导数
**题目** 求函数 $y=x^x$（$x>0$）的导数。
**答案** $y'=x^x(\ln x+1)$
**解法一（对数求导法）** 两边取对数：$\ln y=x\ln x$。两边对 $x$ 求导：$\dfrac{y'}{y}=\ln x+1$。故 $y'=y(\ln x+1)=x^x(\ln x+1)$。
**解法二（隐函数求导）** 令 $F(x,y)=\ln y-x\ln x=0$。由隐函数求导公式 $y'=-\dfrac{F_x}{F_y}=-\dfrac{-(\ln x+1)}{1/y}=y(\ln x+1)=x^x(\ln x+1)$。
**解法三（指数化+链式法则）** $x^x=e^{x\ln x}$，故 $y'=e^{x\ln x}\cdot(x\ln x)'=x^x(\ln x+1)$。
**思路展开** 三种方法本质上是同一个恒等式 $x^x=e^{x\ln x}$ 的不同包装：对数求导是隐式版本，隐函数求导是形式化版本，指数化是显式版本。幂指函数 $u(x)^{v(x)}$ 求导的通法是先指数化，本例可推广到 $y=x^{\sin x}$ 之类。动画上可以画 $y=x^x$（注意其极小值点在 $x=1/e\approx 0.368$ 处，$y'=0$ 对应 $\ln x+1=0$），并展示切线斜率从负变正的过程。
**解法一动画要点** - 两边取对数 $\ln y=x\ln x$ 的变形高亮 - 乘积求导法则作用于 $\ln y$ 的过程
**解法二动画要点** - 隐函数求导公式 $y'=-\dfrac{F_x}{F_y}$ 的分量标注 - $F(x,y)=\ln y-x\ln x=0$ 的等值线
**解法三动画要点** - $y=x^x$ 曲线与极小值点 $x=\dfrac{1}{e}$ - 切线斜率随 $x$ 变化（由负转正）

### eval-calc-006 数学分析 · 导数
**题目** 求函数 $y=\ln(x+\sqrt{x^2+a^2})$（$a>0$）的导数，并说明其反函数。
**答案** $y'=\dfrac{1}{\sqrt{x^2+a^2}}$；反函数为 $x=a\sinh(y-\ln a)=\dfrac{e^y-a^2e^{-y}}{2}$
**解法一（直接链式法则）** $y'=\dfrac{1+\dfrac{x}{\sqrt{x^2+a^2}}}{x+\sqrt{x^2+a^2}}=\dfrac{\sqrt{x^2+a^2}+x}{\sqrt{x^2+a^2}\cdot(x+\sqrt{x^2+a^2})}=\dfrac{1}{\sqrt{x^2+a^2}}$。
**解法二（双曲函数观点）** 令 $x=a\sinh t$，则 $x+\sqrt{x^2+a^2}=a(\sinh t+\cosh t)=a e^t$，故 $y=\ln(ae^t)=t+\ln a$，即 $y=\operatorname{arsinh}\dfrac{x}{a}+\ln a$。由反双曲函数求导公式 $(\operatorname{arsinh} u)'=\dfrac{u'}{\sqrt{1+u^2}}$，得 $y'=\dfrac{1/a}{\sqrt{1+x^2/a^2}}=\dfrac{1}{\sqrt{x^2+a^2}}$。
**解法三（反函数求导）** 由 $y=\ln(x+\sqrt{x^2+a^2})$ 解出 $x$：$e^y=x+\sqrt{x^2+a^2}$，移项平方得 $e^{2y}-2xe^y=a^2$，故 $x=\dfrac{e^y-a^2e^{-y}}{2}=a\sinh(y-\ln a)$。于是 $\dfrac{dx}{dy}=a\cosh(y-\ln a)=\sqrt{x^2+a^2}$，故 $\dfrac{dy}{dx}=\dfrac{1}{\sqrt{x^2+a^2}}$。
**思路展开** 本题把"一个看似难算的复合函数导数"与双曲函数理论打通：$\ln(x+\sqrt{x^2+a^2})$ 正是 $\operatorname{arsinh}(x/a)$ 的对数表示。三种解法对应三个数学层次——计算（链式）、结构（双曲恒等式 $\sinh+\cosh=e^t$）、反演（解出 $x$ 再反函数求导）。动画上可以用单位双曲线 $x^2-y^2=a^2$ 的面积意义展示反双曲函数，并对照普通反三角的类似结果 $\dfrac{d}{dx}\ln(x+\sqrt{x^2-a^2})=\dfrac{1}{\sqrt{x^2-a^2}}$。
**解法一动画要点** - 链式法则逐层拆解：外层对数、内层 $x+\sqrt{x^2+a^2}$ - 分子分母同乘 $\sqrt{x^2+a^2}$ 的化简动画
**解法二动画要点** - 双曲线 $x^2-y^2=a^2$ 上 $\operatorname{arsinh}$ 的面积定义 - 恒等式 $\sinh t+\cosh t=e^t$ 的标注
**解法三动画要点** - 反函数图像关于 $y=x$ 对称 - 反解出 $x=a\sinh(y-\ln a)$ 的推导过程

### eval-calc-007 数学分析 · 导数
**题目** 设星形线参数方程为 $x=a\cos^3 t$，$y=a\sin^3 t$（$a>0$，$0\le t\le 2\pi$），求 $\dfrac{dy}{dx}$ 与 $\dfrac{d^2y}{dx^2}$。
**答案** $\dfrac{dy}{dx}=-\tan t$；$\dfrac{d^2y}{dx^2}=\dfrac{1}{3a\cos^4 t\sin t}$（两式仅在光滑分支上成立，即 $\sin t\cos t\ne 0$；在尖点 $t=k\dfrac{\pi}{2}$ 处切线竖直或水平、二阶导不存在，需单独作单侧讨论）
**解法一（参数方程求导公式）** $\dfrac{dx}{dt}=-3a\cos^2 t\sin t$，$\dfrac{dy}{dt}=3a\sin^2 t\cos t$，故 $\dfrac{dy}{dx}=\dfrac{3a\sin^2t\cos t}{-3a\cos^2t\sin t}=-\tan t$。二阶导：$\dfrac{d^2y}{dx^2}=\dfrac{d}{dt}\left(\dfrac{dy}{dx}\right)\Big/\dfrac{dx}{dt}=\dfrac{-\sec^2 t}{-3a\cos^2 t\sin t}=\dfrac{1}{3a\cos^4 t\sin t}$。
**解法二（消参后隐函数求导）** 消去参数：$x^{2/3}+y^{2/3}=a^{2/3}$。两边对 $x$ 求导：$\dfrac{2}{3}x^{-1/3}+\dfrac{2}{3}y^{-1/3}y'=0$，故 $y'=-\left(\dfrac{y}{x}\right)^{1/3}=-\tan t$。再对 $x$ 求导：$y''=-\dfrac{1}{3}\left(\dfrac{y}{x}\right)^{-2/3}\cdot\dfrac{y'x-y}{x^2}$。代入 $x=a\cos^3 t$、$y=a\sin^3 t$、$y'=-\tan t$：$\left(\dfrac{y}{x}\right)^{2/3}=\tan^2 t$，且 $y'x-y=-\tan t\cdot a\cos^3 t-a\sin^3 t=-a\sin t(\cos^2 t+\sin^2 t)=-a\sin t$。故 $y''=-\dfrac{1}{3}\cot^2 t\cdot\dfrac{-a\sin t}{a^2\cos^6 t}=\dfrac{1}{3a\cos^4 t\sin t}$，与解法一一致。
**解法三（几何切线性质）** 在参数点 $(a\cos^3 t, a\sin^3 t)$ 处，切线方程为 $y-a\sin^3 t=-\tan t\,(x-a\cos^3 t)$。令 $y=0$ 求 $x$ 截距：$\tan t\,x=a\sin^3 t+\tan t\cdot a\cos^3 t=a\sin t(\sin^2 t+\cos^2 t)=a\sin t$，故 $x=a\cos t$；令 $x=0$ 得 $y$ 截距 $y=a\sin^3 t+\tan t\cdot a\cos^3 t=a\sin t$。于是切线与两坐标轴交点间的线段长恒为 $\sqrt{a^2\cos^2 t+a^2\sin^2 t}=a$，且切线斜率恰为 $\dfrac{-a\sin t}{a\cos t}=-\tan t$，与解法一一致。二阶导 $y''$ 则描述这条定长切线随 $t$ 转动的速率（解法一已算出 $\dfrac{1}{3a\cos^4 t\sin t}$）。
**思路展开** 三种解法分别从参数公式、隐函数方程、几何性质出发。值得注意 $t=k\pi/2$ 处 $\tan t$ 无意义，对应星形线四个尖点（cusp），切线是竖直或水平的——这是参数方程求导的奇点讨论素材。动画上星形线可由"长度为 $a$ 的线段两端沿坐标轴滑动、其包络即为星形线"动态生成，导数几何意义一目了然。
**解法一动画要点** - 参数点 $(a\cos^3t,a\sin^3t)$ 沿星形线运动 - $\dfrac{dy}{dx}=\dfrac{dy/dt}{dx/dt}$ 的商式动画
**解法二动画要点** - 消参方程 $x^{2/3}+y^{2/3}=a^{2/3}$ 的隐式求导 - 二阶导 $y''$ 代入参数化简的步骤
**解法三动画要点** - 滑动线段包络生成星形线 - 四尖点处切线方向跳变标注 - 切线截距 $a\cos t$、$a\sin t$ 的实时显示

### eval-calc-008 数学分析 · 中值定理
**题目** 证明：当 $x>0$ 时，$e^x>1+x$。
**答案** 证毕（三种证法）
**解法一（单调性）** 令 $f(x)=e^x-1-x$，则 $f'(x)=e^x-1>0$（$x>0$），故 $f$ 在 $[0,+\infty)$ 上严格递增。又 $f(0)=0$，所以当 $x>0$ 时 $f(x)>f(0)=0$，即 $e^x>1+x$。
**解法二（拉格朗日中值定理）** 对 $f(x)=e^x$ 在 $[0,x]$ 上用拉格朗日中值定理：存在 $\xi\in(0,x)$ 使 $e^x-e^0=e^\xi(x-0)$。因 $\xi>0$，$e^\xi>1$，故 $e^x-1=e^\xi x>x$，即 $e^x>1+x$。
**解法三（泰勒公式带余项）** $e^x=1+x+\dfrac{x^2}{2}e^\eta$，其中 $\eta\in(0,x)$。因 $\dfrac{x^2}{2}e^\eta>0$，故 $e^x>1+x$。此证法还给出更强的估计 $e^x>1+x+\dfrac{x^2}{2}$。
**思路展开** 同一个不等式，三种证法给出三种"剩余量"的理解：解法一剩余量是 $f(x)-f(0)$ 的累积，解法二是 $e^\xi x-x$（中值点处的超额），解法三是泰勒余项 $\dfrac{x^2}{2}e^\eta$（显式的 $x^2$ 阶）。动画上最漂亮的是切线视角：$y=1+x$ 是 $y=e^x$ 在 $x=0$ 处的切线，曲线始终在切线上方（凸性），可逐点高亮差距。
**解法一动画要点** - 差值函数 $f(x)=e^x-1-x$ 的递增曲线 - $f(0)=0$ 起点的标注
**解法二动画要点** - 中值点 $\xi$ 在 $(0,x)$ 上的扫描与 $e^\xi$ 变化 - $y=e^x$ 与割线的位置关系
**解法三动画要点** - 泰勒余项曲线 $y=\dfrac{x^2}{2}e^{\eta}$ 的包络 - 强估计 $e^x>1+x+\dfrac{x^2}{2}$ 的标注

### eval-calc-009 数学分析 · 中值定理
**题目** 设 $0<a<b$，证明：$\arctan b-\arctan a<b-a$。
**答案** 证毕（三种证法）
**解法一（拉格朗日中值定理）** 对 $f(x)=\arctan x$ 在 $[a,b]$ 上用中值定理：存在 $\xi\in(a,b)$ 使 $\arctan b-\arctan a=\dfrac{1}{1+\xi^2}(b-a)$。因 $\dfrac{1}{1+\xi^2}<1$，故 $\arctan b-\arctan a<b-a$。
**解法二（单调性）** 令 $g(x)=x-\arctan x$，则 $g'(x)=1-\dfrac{1}{1+x^2}=\dfrac{x^2}{1+x^2}>0$（$x>0$），故 $g$ 在 $(0,+\infty)$ 上严格递增，$g(b)>g(a)$，即 $b-\arctan b>a-\arctan a$，移项得证。
**解法三（几何斜率比较）** 由 $(\arctan x)'=\dfrac{1}{1+x^2}<1$ 知 $y=\arctan x$ 在 $(0,+\infty)$ 上任意两点连线的斜率小于 1（割线斜率 = 某点导数值 < 1），故 $\dfrac{\arctan b-\arctan a}{b-a}<1$，得证。
**思路展开** 解法一与解法三其实共用中值定理的内核（割线斜率等于某点切线斜率），解法二则从"差值函数"角度入手。本题是"比较两个函数增长快慢"的标准模板：把不等式改写为 $f(b)-f(a)$ 与 $b-a$ 的比较。动画可展示 $y=\arctan x$ 的切线斜率 $\dfrac{1}{1+x^2}$ 随 $x$ 增大而减小、割线始终比 $y=x$ 平缓。
**解法一动画要点** - 中值点 $\xi\in(a,b)$ 的扫描 - 切线斜率 $\dfrac{1}{1+\xi^2}<1$ 的实时标注
**解法二动画要点** - 差值函数 $g(x)=x-\arctan x$ 的递增曲线 - $g(b)>g(a)$ 的区间标注
**解法三动画要点** - 割线斜率与中值点切线斜率联动 - $y=\arctan x$ 与 $y=x$ 对比

### eval-calc-010 数学分析 · 中值定理
**题目** 求极限 $\displaystyle\lim_{x\to 0}\frac{e^x-e^{\sin x}}{x-\sin x}$。
**答案** $1$
**解法一（拉格朗日中值定理）** 令 $f(t)=e^t$，对 $f$ 在 $\sin x$ 与 $x$ 之间用中值定理：$e^x-e^{\sin x}=e^\xi(x-\sin x)$，其中 $\xi$ 介于 $\sin x$ 与 $x$ 之间。当 $x\to 0$ 时 $\sin x\to 0$、$x\to 0$，故 $\xi\to 0$。原式 $=\lim_{x\to 0}e^\xi=1$。
**解法二（提取公因子+等价无穷小）** 原式 $=\lim_{x\to 0}\dfrac{e^{\sin x}\left(e^{x-\sin x}-1\right)}{x-\sin x}=\lim_{x\to 0}e^{\sin x}\cdot\lim_{x\to 0}\dfrac{e^{x-\sin x}-1}{x-\sin x}=1\cdot 1=1$。
**解法三（洛必达法则，连用三次）** 原式为 $\dfrac{0}{0}$ 型。第一次：$\lim_{x\to 0}\dfrac{e^x-e^{\sin x}\cos x}{1-\cos x}$，仍为 $\dfrac{0}{0}$ 型。第二次：分子求导得 $e^x-e^{\sin x}\cos^2 x+e^{\sin x}\sin x$，分母求导得 $\sin x$，仍为 $\dfrac{0}{0}$ 型。第三次：分子再求导为 $e^x-e^{\sin x}(\cos^3 x-2\sin x\cos x)+e^{\sin x}\cos x(\sin x+1)$，分母求导为 $\cos x$。令 $x\to 0$：分子 $\to 1-1\cdot(1-0)+1\cdot 1\cdot(0+1)=1$，分母 $\to 1$，故极限为 $\dfrac{1}{1}=1$。此路可通但三次求导冗长，恰好反衬解法一的一步到位。
**思路展开** 解法一一步到位：中值定理天然匹配"同函数在两点的差"结构，把极限转化为 $e^\xi$ 的连续性。解法二用 $e^{u}-1\sim u$ 的等价无穷小，属于标准套路。解法三刻意展示洛必达在此题的迂回——求导后分子分母结构反而复杂，说明"看到 $\dfrac{f(a)-f(b)}{a-b}$ 结构先想中值定理"。
**解法一动画要点** - $y=e^t$ 上两点 $(\sin x, e^{\sin x})$、$(x, e^x)$ 随 $x\to0$ 靠拢 - 中值点 $\xi$ 被夹逼向 0
**解法二动画要点** - 提取公因子 $e^{\sin x}$ 的变形高亮 - 等价无穷小 $\dfrac{e^u-1}{u}\to1$ 的比值动画
**解法三动画要点** - 洛必达三次求导的符号推导滚动 - 分子分母比值收敛于 1

### eval-calc-011 数学分析 · 幂级数
**题目** 用多种方法求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\cdot 2^n}$ 的和。
**答案** $\ln 2$
**解法一（代入对数展开式）** 由 $-\ln(1-x)=\displaystyle\int_0^x\dfrac{dt}{1-t}=\int_0^x\sum_{n=0}^{\infty}t^n\,dt=\sum_{n=1}^{\infty}\dfrac{x^n}{n}=x+\dfrac{x^2}{2}+\dfrac{x^3}{3}+\cdots$（$|x|<1$），取 $x=\dfrac{1}{2}$，得 $\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{n\cdot 2^n}=-\ln\left(1-\dfrac{1}{2}\right)=-\ln\dfrac{1}{2}=\ln 2$。
**解法二（积分表示求和）** 由 $\dfrac{1}{n\cdot 2^n}=\displaystyle\int_0^{1/2}x^{n-1}\,dx$（把 $\dfrac{1}{2^n}$ 看作幂的积分），故 $S=\displaystyle\sum_{n=1}^{\infty}\int_0^{1/2}x^{n-1}dx=\int_0^{1/2}\sum_{n=1}^{\infty}x^{n-1}dx=\int_0^{1/2}\dfrac{dx}{1-x}=\left[-\ln(1-x)\right]_0^{1/2}=\ln 2$（求和与积分可交换由正项级数单调收敛保证）。
**解法三（由导数重建展开式）** 设 $f(x)=\displaystyle\sum_{n=1}^{\infty}\dfrac{x^n}{n}$，逐项求导得 $f'(x)=\displaystyle\sum_{n=1}^{\infty}x^{n-1}=\dfrac{1}{1-x}$（$|x|<1$），且 $f(0)=0$，故 $f(x)=-\ln(1-x)$，取 $x=\dfrac{1}{2}$ 得 $\ln 2$。
**思路展开** 解法一直接调用已知展开式，解法二把"求和"翻译成"积分"（把分母 $2^n$ 藏进积分号里），解法三从头重建展开式——三种方法分别对应"引用结论""构造表示""推导结论"三个层次。动画可展示 $\int_0^{1/2}\dfrac{dx}{1-x}$ 的曲边梯形面积被宽为 $2^{-n}$ 的矩形条带剖分，级数各项正是这些条带的面积。
**解法一动画要点** - 展开式 $-\ln(1-x)=x+\dfrac{x^2}{2}+\cdots$ 的逐项生成 - $x=\dfrac{1}{2}$ 代入的标注
**解法二动画要点** - $y=\dfrac{1}{1-x}$ 在 $[0,1/2]$ 上的矩形条带剖分 - 每个条带面积 $\dfrac{1}{n\cdot2^n}$ 与级数项对照
**解法三动画要点** - 逐项求导得 $f'(x)=\dfrac{1}{1-x}$ 的过程 - 由 $f(0)=0$ 积分还原 $f(x)$ 的动画

### eval-calc-012 数学分析 · 三角恒等式
**题目** 求 $\tan 15^\circ$ 的精确值。
**答案** $2-\sqrt{3}$
**解法一（和角公式）** $\tan 15^\circ=\tan(45^\circ-30^\circ)=\dfrac{\tan 45^\circ-\tan 30^\circ}{1+\tan 45^\circ\tan 30^\circ}=\dfrac{1-\frac{\sqrt{3}}{3}}{1+\frac{\sqrt{3}}{3}}=\dfrac{3-\sqrt{3}}{3+\sqrt{3}}$。分子分母同乘 $3-\sqrt{3}$：$\dfrac{(3-\sqrt{3})^2}{9-3}=\dfrac{12-6\sqrt{3}}{6}=2-\sqrt{3}$。
**解法二（半角公式）** $\tan 15^\circ=\tan\dfrac{30^\circ}{2}=\dfrac{1-\cos 30^\circ}{\sin 30^\circ}=\dfrac{1-\frac{\sqrt{3}}{2}}{\frac{1}{2}}=2-\sqrt{3}$。
**解法三（几何构造）** 用 $30^\circ$-$60^\circ$-$90^\circ$ 三角形（边长 $1:\sqrt3:2$）拼出宽 $1$、长 $2+\sqrt3$ 的矩形：长边由"长直角边 $\sqrt3$ 与斜边 $2$ 首尾相接"构成，宽取短直角边 $1$。该矩形的对角线与长边的夹角 $\alpha$ 满足 $\tan\alpha=\dfrac{1}{2+\sqrt3}$。分母有理化：$\dfrac{1}{2+\sqrt3}=\dfrac{2-\sqrt3}{(2+\sqrt3)(2-\sqrt3)}=2-\sqrt3$。由解法一 $\tan 15^\circ=2-\sqrt3$，且 $0<\alpha<90^\circ$ 内正切一一对应，故 $\alpha=15^\circ$。此构造同时给出 $\tan 75^\circ=2+\sqrt3$。
**思路展开** 三种方法都给出同一精确值：和角公式走代数分解，半角公式走倍角逆向，几何构造走图形拼合。还可顺带指出 $\tan 75^\circ=2+\sqrt{3}$，两者互为倒数（$\tan 15^\circ\cdot\tan 75^\circ=1$ 来自 $15^\circ+75^\circ=90^\circ$）。动画可在单位圆中同时标出 $15^\circ$、$30^\circ$、$45^\circ$ 角，展示和角分解与半角关系的几何来源。
**解法一动画要点** - 单位圆中 $15^\circ$ 角与 $45^\circ-30^\circ$ 分解 - 和角公式 $\tan(45^\circ-30^\circ)$ 的代数代入动画
**解法二动画要点** - $30^\circ$ 角的角平分线构造 - 半角公式 $\tan\dfrac{\theta}{2}=\dfrac{1-\cos\theta}{\sin\theta}$ 的标注
**解法三动画要点** - $30^\circ$-$60^\circ$-$90^\circ$ 三角形（边 $1:\sqrt3:2$）的拼合 - $1\times(2+\sqrt3)$ 矩形对角线与 $15^\circ$ 角的对应 - 分母有理化 $1/(2+\sqrt3)=2-\sqrt3$

### eval-calc-013 数学分析 · 不定积分
**题目** 求不定积分 $\displaystyle\int x^2e^x\,dx$。
**答案** $(x^2-2x+2)e^x+C$
**解法一（分部积分两次）** 第一次：$\int x^2e^xdx=x^2e^x-2\int xe^xdx$。第二次：$\int xe^xdx=xe^x-\int e^xdx=(x-1)e^x$。故原式 $=x^2e^x-2(x-1)e^x+C=(x^2-2x+2)e^x+C$。
**解法二（待定系数法）** 因被积函数是 $x^2e^x$，设原函数为 $(ax^2+bx+c)e^x$。求导比对：$\left[(ax^2+bx+c)e^x\right]'=\left[ax^2+(2a+b)x+(b+c)\right]e^x\equiv x^2e^x$，故 $a=1$，$2a+b=0\Rightarrow b=-2$，$b+c=0\Rightarrow c=2$，得 $(x^2-2x+2)e^x$。
**解法三（递推公式）** 记 $I_n=\int x^ne^xdx$，分部得 $I_n=x^ne^x-nI_{n-1}$。$I_0=e^x$，$I_1=xe^x-I_0=(x-1)e^x$，$I_2=x^2e^x-2I_1=(x^2-2x+2)e^x$。
**思路展开** 三种方法各有定位：分部积分是通法，待定系数法把机械步骤压缩为一次求导比对（适合口算），递推公式揭示"多项式 $\times e^x$ 的原函数仍是多项式 $\times e^x$"的结构封闭性。动画可以展示分部积分法中 $u$、$dv$ 的选取与表格法（列 $x^2,x,1$ 与 $e^x$ 交错加减）。
**解法一动画要点** - 两次分部积分的逐步拆解 - 每次 $u,dv$ 选取的标注
**解法二动画要点** - 待定系数 $(ax^2+bx+c)e^x$ 的求导比对动画 - 系数 $a,b,c$ 的方程组求解
**解法三动画要点** - 递推链 $I_0\to I_1\to I_2$ 的流程图 - 递推式 $I_n=x^ne^x-nI_{n-1}$ 的标注

### eval-calc-014 数学分析 · 不定积分
**题目** 求不定积分 $\displaystyle\int\dfrac{dx}{\sin x}$，并说明不同形式答案的等价性。
**答案** $\ln\left|\tan\dfrac{x}{2}\right|+C$（等价于 $\ln|\csc x-\cot x|+C$）
**解法一（半角变形）** $\dfrac{1}{\sin x}=\dfrac{1}{2\sin\frac{x}{2}\cos\frac{x}{2}}=\dfrac{\dfrac{1}{2}\sec^2\frac{x}{2}}{\tan\frac{x}{2}}$。故 $\int\dfrac{dx}{\sin x}=\int\dfrac{d\left(\tan\frac{x}{2}\right)}{\tan\frac{x}{2}}=\ln\left|\tan\dfrac{x}{2}\right|+C$。
**解法二（万能代换）** 令 $t=\tan\dfrac{x}{2}$，则 $\sin x=\dfrac{2t}{1+t^2}$，$dx=\dfrac{2dt}{1+t^2}$。原式 $=\int\dfrac{1+t^2}{2t}\cdot\dfrac{2dt}{1+t^2}=\int\dfrac{dt}{t}=\ln|t|+C=\ln\left|\tan\dfrac{x}{2}\right|+C$。
**解法三（共轭恒等式）** 分子分母同乘 $\csc x-\cot x$：$\int\csc x\,dx=\int\dfrac{\csc x(\csc x-\cot x)}{\csc x-\cot x}dx=\int\dfrac{d(\csc x-\cot x)}{\csc x-\cot x}=\ln|\csc x-\cot x|+C$。由 $\csc x-\cot x=\dfrac{1-\cos x}{\sin x}=\tan\dfrac{x}{2}$ 知两形式完全相同。
**思路展开** 万能代换是最系统的有理化方法（任何三角有理式都可化），半角变形是它的轻量版，共轭恒等式是历史悠久的教科书技巧。三者给出同一函数的两种表面形式 $\ln|\tan(x/2)|$ 与 $\ln|\csc x-\cot x|$——"不定积分答案不唯一"的最好例证，动画可用求导验证两个形式导数都是 $\csc x$。
**解法一动画要点** - 半角恒等式 $\dfrac{1}{\sin x}=\dfrac{\sec^2(x/2)/2}{\tan(x/2)}$ 的变形动画 - 凑微分 $\dfrac{d(\tan(x/2))}{\tan(x/2)}$ 的高亮
**解法二动画要点** - 万能代换三角形（半角 $t=\tan(x/2)$ 的边长对应） - $\sin x=\dfrac{2t}{1+t^2}$、$dx=\dfrac{2dt}{1+t^2}$ 的代入
**解法三动画要点** - 共轭式 $\csc x-\cot x$ 的分子分母同乘动画 - 两形式答案同框求导验证

### eval-calc-015 数学分析 · 定积分
**题目** 求定积分 $\displaystyle I=\int_0^\pi\frac{x\sin x}{1+\cos^2 x}\,dx$。
**答案** $\dfrac{\pi^2}{4}$
**解法一（区间替换法，对称性）** 令 $t=\pi-x$，则 $I=\int_0^\pi\dfrac{(\pi-t)\sin t}{1+\cos^2 t}\,dt=\pi\int_0^\pi\dfrac{\sin t}{1+\cos^2 t}\,dt-I$，故 $2I=\pi\int_0^\pi\dfrac{\sin x}{1+\cos^2 x}\,dx$。令 $u=\cos x$（$du=-\sin x\,dx$）：$\int_0^\pi\dfrac{\sin x}{1+\cos^2x}dx=\int_{-1}^{1}\dfrac{du}{1+u^2}=\left[\arctan u\right]_{-1}^{1}=\dfrac{\pi}{2}$。于是 $2I=\pi\cdot\dfrac{\pi}{2}$，$I=\dfrac{\pi^2}{4}$。
**解法二（分部积分+回代思想）** 令 $u=x$、$dv=\dfrac{\sin x}{1+\cos^2x}dx$，则 $v=-\arctan(\cos x)$。$I=\left[-x\arctan(\cos x)\right]_0^\pi+\int_0^\pi\arctan(\cos x)dx$。代入上下限：$-\pi\arctan(-1)+0=\dfrac{\pi^2}{4}$，再结合对称性 $\int_0^\pi\arctan(\cos x)dx=0$（被积函数关于 $x=\dfrac{\pi}{2}$ 反对称），得 $I=\dfrac{\pi^2}{4}$。
**解法三（数值验证）** 用辛普森法或等距分割近似计算 $I$（如 $n=1000$ 区间），得到 $2.467401\cdots$，与 $\dfrac{\pi^2}{4}\approx2.4674011$ 吻合，作为解析结果的独立校验。
**思路展开** 解法一的区间替换是核心技巧：$\int_0^\pi xf(\sin x)dx=\dfrac{\pi}{2}\int_0^\pi f(\sin x)dx$ 把因子 $x$ "平均掉"。解法二用分部积分把 $x$ 移进 $\arctan$ 里，再用反对称性消除剩余积分，展示了完全不同的拆解路径。解法三提示数值计算在解析推导验证中的作用。
**解法一动画要点** - 区间替换 $t=\pi-x$ 的镜像动画 - 自指方程 $2I=\pi\int\dfrac{\sin x}{1+\cos^2x}dx$ 的推导高亮 - 换元 $u=\cos x$ 后 $\arctan$ 区间取值
**解法二动画要点** - 分部积分 $u=x$、$dv=\dfrac{\sin x}{1+\cos^2x}dx$ 的选取 - 反对称性 $\int_0^\pi\arctan(\cos x)dx=0$ 的面积抵消
**解法三动画要点** - 数值积分点列逼近 $\pi^2/4$ - 与解析值同框对照

### eval-calc-016 数学分析 · 不定积分
**题目** 求不定积分 $\displaystyle\int\frac{dx}{(x^2+a^2)^2}$（$a>0$）。
**答案** $\dfrac{x}{2a^2(x^2+a^2)}+\dfrac{1}{2a^3}\arctan\dfrac{x}{a}+C$
**解法一（三角换元）** 令 $x=a\tan t$，则 $dx=a\sec^2 t\,dt$，$x^2+a^2=a^2\sec^2 t$。原式 $=\displaystyle\int\dfrac{a\sec^2 t}{a^4\sec^4 t}dt=\dfrac{1}{a^3}\int\cos^2 t\,dt=\dfrac{1}{a^3}\left(\dfrac{t}{2}+\dfrac{\sin 2t}{4}\right)+C=\dfrac{1}{a^3}\left(\dfrac{t}{2}+\dfrac{\sin t\cos t}{2}\right)+C$。由直角三角形得 $\sin t=\dfrac{x}{\sqrt{x^2+a^2}}$、$\cos t=\dfrac{a}{\sqrt{x^2+a^2}}$，故原式 $=\dfrac{1}{2a^3}\arctan\dfrac{x}{a}+\dfrac{x}{2a^2(x^2+a^2)}+C$。
**解法二（递推公式）** 记 $I_n=\displaystyle\int\dfrac{dx}{(x^2+a^2)^n}$。对 $I_n$ 分部积分（取 $u=\dfrac{1}{(x^2+a^2)^n}$、$dv=dx$）：$I_n=\dfrac{x}{(x^2+a^2)^n}+2n\displaystyle\int\dfrac{x^2}{(x^2+a^2)^{n+1}}dx=\dfrac{x}{(x^2+a^2)^n}+2n\int\dfrac{(x^2+a^2)-a^2}{(x^2+a^2)^{n+1}}dx=\dfrac{x}{(x^2+a^2)^n}+2n(I_n-a^2I_{n+1})$。整理得递推式 $I_{n+1}=\dfrac{1}{2na^2}\left[\dfrac{x}{(x^2+a^2)^n}+(2n-1)I_n\right]$。取 $n=1$ 并以 $I_1=\dfrac{1}{a}\arctan\dfrac{x}{a}$ 代入：$I_2=\dfrac{1}{2a^2}\left[\dfrac{x}{x^2+a^2}+I_1\right]=\dfrac{x}{2a^2(x^2+a^2)}+\dfrac{1}{2a^3}\arctan\dfrac{x}{a}+C$。
**解法三（复数部分分式）** 在复数域 $f(z)=\dfrac{1}{(z^2+a^2)^2}=\dfrac{1}{(z-ai)^2(z+ai)^2}$，实系数保证共轭对称。求系数：$C=\lim_{z\to ai}(z-ai)^2f(z)=\dfrac{1}{(2ai)^2}=-\dfrac{1}{4a^2}$；$D=\lim_{z\to ai}\dfrac{d}{dz}\dfrac{1}{(z+ai)^2}=\dfrac{-2}{(2ai)^3}=\dfrac{1}{4a^3i}=-\dfrac{i}{4a^3}$，共轭 $\bar D=\dfrac{i}{4a^3}$。故 $\dfrac{1}{(x^2+a^2)^2}=-\dfrac{1}{4a^2}\left[\dfrac{1}{(x-ai)^2}+\dfrac{1}{(x+ai)^2}\right]-\dfrac{i}{4a^3}\cdot\dfrac{1}{x-ai}+\dfrac{i}{4a^3}\cdot\dfrac{1}{x+ai}$。逐项积分：第一组 $=\dfrac{1}{4a^2}\left[\dfrac{1}{x-ai}+\dfrac{1}{x+ai}\right]=\dfrac{x}{2a^2(x^2+a^2)}$；第二组 $=\dfrac{i}{4a^3}\left[\ln(x+ai)-\ln(x-ai)\right]=\dfrac{i}{4a^3}\ln\dfrac{x+ai}{x-ai}$。对实数 $x>0$，$|x+ai|=|x-ai|$，且 $\arg\dfrac{x+ai}{x-ai}=2\arg(x+ai)=2\left(\dfrac{\pi}{2}-\arctan\dfrac{x}{a}\right)=\pi-2\arctan\dfrac{x}{a}$，故第二组 $=\dfrac{i}{4a^3}\cdot i\left(\pi-2\arctan\dfrac{x}{a}\right)=\dfrac{1}{2a^3}\arctan\dfrac{x}{a}-\dfrac{\pi}{4a^3}$（常数并入 $C$）；当 $x<0$ 时上述辐角公式超出主值范围，需沿实轴选取连续对数分支，分支差异为常数、并入 $C$ 后不影响原函数（也可分 $x>0$ 与 $x<0$ 两区间分别计算）。合并得 $\dfrac{x}{2a^2(x^2+a^2)}+\dfrac{1}{2a^3}\arctan\dfrac{x}{a}+C$，三法一致。
**思路展开** 三角换元是几何直觉最直接的（正切替换把平方和变成 $\sec^2$），递推公式把这类积分纳入 $I_n$ 家族、适合系统化处理任意次幂，复数部分分式则展示代数封闭性——三种方法从几何、递推、复分析三个入口到达同一结果。动画可展示三角替换的直角三角形边长对应关系，以及递推链 $I_1\to I_2\to I_3$ 的传递。
**解法一动画要点** - 直角三角形替换 $x=a\tan t$ 的边长标注 - $\cos^2t$ 的倍角积分与代回
**解法二动画要点** - 递推链 $I_1\to I_2\to\cdots$ 流程图 - 分部积分导出递推式 $I_{n+1}=\dfrac{1}{2na^2}\left[\dfrac{x}{(x^2+a^2)^n}+(2n-1)I_n\right]$ 的步骤
**解法三动画要点** - 复数平面两极点 $z=\pm ai$ 示意 - 部分分式系数 $C,D$ 的极限求法 - 辐角分支与实部合并

### eval-calc-017 数学分析 · 定积分
**题目** 求定积分 $\displaystyle I=\int_0^1\frac{\ln(1+x)}{1+x^2}\,dx$。
**答案** $\dfrac{\pi}{8}\ln 2$
**解法一（换元+对称性）** 令 $x=\tan t$（$t:0\to\dfrac{\pi}{4}$），则 $I=\displaystyle\int_0^{\pi/4}\ln(1+\tan t)\,dt$。利用区间替换 $t\to\dfrac{\pi}{4}-t$：$I=\displaystyle\int_0^{\pi/4}\ln\left(1+\tan\left(\frac{\pi}{4}-t\right)\right)dt$。由和角公式 $\tan\left(\dfrac{\pi}{4}-t\right)=\dfrac{1-\tan t}{1+\tan t}$，得 $1+\tan\left(\dfrac{\pi}{4}-t\right)=\dfrac{2}{1+\tan t}$。两式相加：$2I=\displaystyle\int_0^{\pi/4}\left[\ln(1+\tan t)+\ln\dfrac{2}{1+\tan t}\right]dt=\int_0^{\pi/4}\ln 2\,dt=\dfrac{\pi}{4}\ln 2$，故 $I=\dfrac{\pi}{8}\ln 2$。
**解法二（分式替换）** 令 $x=\dfrac{1-t}{1+t}$（$t:1\to 0$），则 $dx=-\dfrac{2}{(1+t)^2}dt$，且 $1+x=\dfrac{2}{1+t}$、$1+x^2=\dfrac{2(1+t^2)}{(1+t)^2}$。代入得 $I=\displaystyle\int_1^0\dfrac{\ln\frac{2}{1+t}}{\frac{2(1+t^2)}{(1+t)^2}}\cdot\left(-\dfrac{2}{(1+t)^2}\right)dt=\int_0^1\dfrac{\ln 2-\ln(1+t)}{1+t^2}\,dt=\ln 2\int_0^1\dfrac{dt}{1+t^2}-I=\dfrac{\pi}{4}\ln 2-I$（其中 $\int_0^1\dfrac{dt}{1+t^2}=\left[\arctan t\right]_0^1=\dfrac{\pi}{4}$）。故 $2I=\dfrac{\pi}{4}\ln 2$，$I=\dfrac{\pi}{8}\ln 2$。
**解法三（分部积分+替换）** 取 $u=\ln(1+x)$、$dv=\dfrac{dx}{1+x^2}$，则 $v=\arctan x$。$I=\left[\ln(1+x)\arctan x\right]_0^1-\displaystyle\int_0^1\dfrac{\arctan x}{1+x}\,dx=\dfrac{\pi}{4}\ln 2-J$，其中 $J=\displaystyle\int_0^1\dfrac{\arctan x}{1+x}dx$。对 $J$ 作替换 $x=\dfrac{1-t}{1+t}$：$dx=-\dfrac{2}{(1+t)^2}dt$，$1+x=\dfrac{2}{1+t}$，且 $\arctan\dfrac{1-t}{1+t}=\dfrac{\pi}{4}-\arctan t$（$t\in[0,1]$，由 $\tan\left(\dfrac{\pi}{4}-\arctan t\right)=\dfrac{1-t}{1+t}$ 得）。故 $J=\displaystyle\int_1^0\left(\frac{\pi}{4}-\arctan t\right)\cdot\frac{1+t}{2}\cdot\left(-\frac{2}{(1+t)^2}\right)dt=\int_0^1\dfrac{\frac{\pi}{4}-\arctan t}{1+t}\,dt=\dfrac{\pi}{4}\ln 2-J$，得 $2J=\dfrac{\pi}{4}\ln 2$，$J=\dfrac{\pi}{8}\ln 2$。于是 $I=\dfrac{\pi}{4}\ln 2-\dfrac{\pi}{8}\ln 2=\dfrac{\pi}{8}\ln 2$。
**思路展开** 解法一的精妙之处在于 $\tan$ 替换后积分区间恰为 $\left[0,\dfrac{\pi}{4}\right]$，使 $t\to\dfrac{\pi}{4}-t$ 的对称替换可用；解法二的分式替换 $x=\dfrac{1-t}{1+t}$ 把 $1+x$ 变成 $\dfrac{2}{1+t}$，直接制造出 $I$ 的自指方程；解法三先用分部积分把 $\ln(1+x)$ 消掉、再对辅助积分 $J$ 用同一分式替换。三种方法分别代表几何、代数替换、分部+替换三条路线。
**解法一动画要点** - $x=\tan t$ 把区间映到 $\left[0,\dfrac{\pi}{4}\right]$ 的坐标动画 - $t\to\dfrac{\pi}{4}-t$ 镜像对称示意 - 两式相加得 $2I=\dfrac{\pi}{4}\ln2$ 的自指方程
**解法二动画要点** - 分式替换 $x=\dfrac{1-t}{1+t}$ 的变量对应动画 - $\ln\dfrac{2}{1+t}$ 拆分的变形高亮
**解法三动画要点** - 分部积分 $u=\ln(1+x)$、$dv=\dfrac{dx}{1+x^2}$ 的选取 - 辅助积分 $J$ 的自指方程推导

### eval-calc-018 数学分析 · 不定积分
**题目** 求不定积分 $\displaystyle\int x\arctan x\,dx$。
**答案** $\dfrac{x^2+1}{2}\arctan x-\dfrac{x}{2}+C$
**解法一（分部积分：反函数留作 $u$）** 令 $u=\arctan x$、$dv=x\,dx$，则 $du=\dfrac{dx}{1+x^2}$、$v=\dfrac{x^2}{2}$。原式 $=\dfrac{x^2}{2}\arctan x-\dfrac{1}{2}\displaystyle\int\dfrac{x^2}{1+x^2}dx=\dfrac{x^2}{2}\arctan x-\dfrac{1}{2}\int\left(1-\dfrac{1}{1+x^2}\right)dx=\dfrac{x^2}{2}\arctan x-\dfrac{x}{2}+\dfrac{1}{2}\arctan x+C=\dfrac{x^2+1}{2}\arctan x-\dfrac{x}{2}+C$。
**解法二（先换元再分部）** 令 $t=\arctan x$，则 $x=\tan t$、$dx=\sec^2 t\,dt$。原式 $=\displaystyle\int t\tan t\sec^2 t\,dt=\dfrac{1}{2}\int t\,d(\tan^2 t)=\dfrac{1}{2}t\tan^2 t-\dfrac{1}{2}\int\tan^2 t\,dt=\dfrac{1}{2}t\tan^2 t-\dfrac{1}{2}\int(\sec^2 t-1)dt=\dfrac{1}{2}t(1+\tan^2 t)-\dfrac{1}{2}\tan t+C$。代回 $t=\arctan x$、$\tan t=x$，得 $\dfrac{x^2+1}{2}\arctan x-\dfrac{x}{2}+C$。
**解法三（分部积分：整体留作 $u$）** 令 $u=x\arctan x$、$dv=dx$，则 $v=x$、$du=\left(\arctan x+\dfrac{x}{1+x^2}\right)dx$。原式 $=x^2\arctan x-\displaystyle\int x\arctan x\,dx-\int\dfrac{x^2}{1+x^2}dx$，即 $2I=x^2\arctan x-\displaystyle\int\left(1-\dfrac{1}{1+x^2}\right)dx=x^2\arctan x-x+\arctan x$，故 $I=\dfrac{x^2+1}{2}\arctan x-\dfrac{x}{2}+C$。
**思路展开** 解法一、三给出分部积分中"谁当 $u$"的两种极端：把 $\arctan x$ 当 $u$（消掉反三角）与把整个被积函数当 $u$（引出 $I$ 的自指方程）。解法二先换元把反三角"拿掉"再分部，展示了处理反三角积分的一般策略——换元消除反三角。动画可展示 $y=x\arctan x$ 的奇偶性（偶函数）与原函数曲线的形状。
**解法一动画要点** - 分部积分 $u=\arctan x$、$dv=x\,dx$ 的选取 - $\dfrac{x^2}{1+x^2}$ 拆成 $1-\dfrac{1}{1+x^2}$ 的化简
**解法二动画要点** - 换元 $t=\arctan x$ 的坐标压缩示意 - $t\tan t\sec^2t$ 的凑微分 $\dfrac{1}{2}d(\tan^2t)$
**解法三动画要点** - 整体作 $u=x\arctan x$ 的选取 - 自指方程 $2I=x^2\arctan x-x+\arctan x$ 的推导

### eval-calc-019 数学分析 · 反常积分
**题目** 求反常积分 $\displaystyle\int_0^{+\infty}xe^{-x}\,dx$。
**答案** $1$
**解法一（分部积分+极限）** 先求原函数：令 $u=x$、$dv=e^{-x}dx$，则 $du=dx$、$v=-e^{-x}$，$\displaystyle\int xe^{-x}dx=-xe^{-x}+\int e^{-x}dx=-(x+1)e^{-x}+C$。故 $\displaystyle\int_0^{b}xe^{-x}dx=\left[-(x+1)e^{-x}\right]_0^b=1-(b+1)e^{-b}$。令 $b\to+\infty$：$(b+1)e^{-b}\to 0$（指数衰减快于线性增长），得原积分 $=1$。
**解法二（Γ 函数）** 由 Γ 函数定义 $\Gamma(s)=\displaystyle\int_0^{+\infty}t^{s-1}e^{-t}dt$，原积分 $=\Gamma(2)$。递推：$\Gamma(s+1)=s\Gamma(s)$（分部积分一次即得），且 $\Gamma(1)=\displaystyle\int_0^{+\infty}e^{-t}dt=1$，故 $\Gamma(2)=1\cdot\Gamma(1)=1$。此解法把单个积分放进 Γ 函数家族，可一并处理 $\int_0^{+\infty}x^ne^{-x}dx=\Gamma(n+1)=n!$。
**解法三（概率论视角）** 若 $X\sim\operatorname{Exp}(1)$（参数 $\lambda=1$ 的指数分布），其密度为 $f(x)=e^{-x}$（$x>0$），则原积分 $=E[X]$。由指数分布期望公式 $E[X]=\dfrac{1}{\lambda}=1$；或由尾概率公式 $E[X]=\displaystyle\int_0^{+\infty}P(X>t)dt=\int_0^{+\infty}e^{-t}dt=1$ 得到同一结果。
**思路展开** 同一积分在三个语境中现身：分析（分部积分）、特殊函数（Γ 函数）、概率（指数分布期望）。解法三的尾概率公式 $E[X]=\int_0^\infty P(X>t)dt$ 本身就是一个"分层蛋糕"式面积分解，动画可以把它画成横向条带累加与纵向积分相等的直观演示。
**解法一动画要点** - 分部积分 $u=x$、$dv=e^{-x}dx$ 的选取 - $(b+1)e^{-b}\to0$ 的极限标注
**解法二动画要点** - Γ 函数递推 $\Gamma(s+1)=s\Gamma(s)$ 的示意 - $\Gamma(1)=1$ 的基线标注
**解法三动画要点** - 指数分布密度 $e^{-x}$ 的峰形曲线与面积填充 - 横向条带分解（尾概率公式 $\int P(X>t)dt$）

### eval-calc-020 数学分析 · 反常积分
**题目** 讨论反常积分 $\displaystyle\int_1^{+\infty}\frac{dx}{x^p}$（$p>0$）的敛散性，并求其收敛时的值。
**答案** $p>1$ 时收敛于 $\dfrac{1}{p-1}$；$0<p\le 1$ 时发散
**解法一（定义直接计算）** 当 $p\ne 1$ 时，$\displaystyle\int_1^b x^{-p}dx=\left[\dfrac{x^{1-p}}{1-p}\right]_1^b=\dfrac{b^{1-p}-1}{1-p}$。若 $p>1$，则 $1-p<0$，$b^{1-p}\to 0$，积分为 $\dfrac{0-1}{1-p}=\dfrac{1}{p-1}$，收敛；若 $0<p<1$，则 $b^{1-p}\to+\infty$，发散。当 $p=1$ 时 $\displaystyle\int_1^b\dfrac{dx}{x}=\ln b\to+\infty$，发散。综上，$p>1$ 收敛于 $\dfrac{1}{p-1}$，$0<p\le 1$ 发散。
**解法二（与 p 级数互证：积分判别法）** 函数 $f(x)=x^{-p}$ 在 $[1,+\infty)$ 上非负递减，由积分判别法，$\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{n^p}$ 与 $\displaystyle\int_1^{+\infty}\dfrac{dx}{x^p}$ 同敛散，故 $p>1$ 收敛、$p\le 1$ 发散——积分与级数两个世界互相印证。
**解法三（面积直觉与分块比较）** 作图比较 $y=\dfrac{1}{x}$ 与 $y=\dfrac{1}{x^2}$：把 $[1,+\infty)$ 按整数分块，$\dfrac{1}{x}$ 下第 $n$ 块面积约 $\dfrac{1}{n}$（对应调和级数各项，发散），$\dfrac{1}{x^2}$ 下第 $n$ 块面积约 $\dfrac{1}{n^2}$（对应收敛级数各项）。直观上 $p$ 越大曲线"塌得越快"，面积越有限，临界在 $p=1$。
**思路展开** 本题是"积分—级数同构"的入门范例：解法二明确指出 $p$ 级数敛散与 $p$ 积分敛散一一对应，解法三把无穷面积的分歧可视化。动画最适合画 $p$ 滑块：拖动 $p$ 从 $0.5$ 到 $2$，观察曲线下方彩色条带的总面积从"无限"变"有限"的临界（$p=1$）。
**解法一动画要点** - $b^{1-p}$ 随 $b\to\infty$ 的三种走势（收敛/发散/对数） - 分段结论 $p>1$ 收敛于 $\dfrac{1}{p-1}$ 的标注
**解法二动画要点** - 柱状图与 $y=\dfrac{1}{x^p}$ 曲线的面积夹逼 - p 级数与 p 积分的同敛散对应
**解法三动画要点** - $p$ 滑块联动曲线 $y=1/x^p$ - 整数分块条带面积与级数项对照 - 临界 $p=1$ 高亮

### eval-calc-021 数学分析 · 一般级数
**题目** 求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n}{2^n}$ 的和。
**答案** $2$
**解法一（错位相减）** 写 $S=\dfrac{1}{2}+\dfrac{2}{4}+\dfrac{3}{8}+\dfrac{4}{16}+\cdots$，则 $\dfrac{S}{2}=\dfrac{1}{4}+\dfrac{2}{8}+\dfrac{3}{16}+\cdots$。两式相减：$S-\dfrac{S}{2}=\dfrac{1}{2}+\left(\dfrac{2}{4}-\dfrac{1}{4}\right)+\left(\dfrac{3}{8}-\dfrac{2}{8}\right)+\left(\dfrac{4}{16}-\dfrac{3}{16}\right)+\cdots=\dfrac{1}{2}+\dfrac{1}{4}+\dfrac{1}{8}+\dfrac{1}{16}+\cdots=1$（几何级数）。故 $\dfrac{S}{2}=1$，$S=2$。
**解法二（幂级数求和）** 由等比级数 $\displaystyle\sum_{n=0}^{\infty}x^{n}=\dfrac{1}{1-x}$（$|x|<1$）逐项求导：$\displaystyle\sum_{n=1}^{\infty}nx^{n-1}=\dfrac{1}{(1-x)^2}$，故 $\displaystyle\sum_{n=1}^{\infty}nx^n=\dfrac{x}{(1-x)^2}$。取 $x=\dfrac{1}{2}$，得 $S=\dfrac{1/2}{(1-1/2)^2}=\dfrac{1/2}{1/4}=2$。
**解法三（概率论：几何分布期望）** 设 $X$ 服从参数 $p=\dfrac{1}{2}$ 的几何分布（抛硬币直到首次正面所需次数），则 $P(X=n)=q^{n-1}p=\left(\dfrac{1}{2}\right)^n$，$E[X]=\displaystyle\sum_{n=1}^{\infty}nq^{n-1}p=p\sum_{n=1}^{\infty}nq^{n-1}=p\cdot\dfrac{1}{(1-q)^2}=\dfrac{1}{p}=2$（其中用到 $\sum nq^{n-1}=\dfrac{1}{(1-q)^2}$）。而 $E[X]=\displaystyle\sum_{n=1}^{\infty}n\left(\dfrac{1}{2}\right)^n=S$，故 $S=2$。
**思路展开** 三个解法分属三种语言：错位相减是等差乘等比求和的经典技巧，幂级数是生成函数思想（求和转求导），几何分布则给级数一个概率语义。动画可以三屏并列：左屏数字竖式错位相减，中屏 $y=\dfrac{x}{(1-x)^2}$ 曲线在 $x=\dfrac{1}{2}$ 处的取值，右屏抛硬币试验中"首次正面次数"的频数直方图。
**解法一动画要点** - 竖式错位相减逐行对齐 - 相减后每行系数归一的抵消动画
**解法二动画要点** - 逐项求导 $\sum nx^{n-1}=\dfrac{1}{(1-x)^2}$ 的过程 - 幂级数曲线在 $x=\dfrac{1}{2}$ 处取点
**解法三动画要点** - 抛硬币"首次正面次数"的频数直方图 - 直方图均值收敛于 2

### eval-calc-022 数学分析 · 一般级数
**题目** 求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n^2}{2^n}$ 的和。
**答案** $6$
**解法一（幂级数求和）** 由 $\displaystyle\sum_{n=1}^{\infty}x^n=\dfrac{x}{1-x}$ 逐项求导两次：先得 $\displaystyle\sum_{n=1}^{\infty}nx^{n-1}=\dfrac{1}{(1-x)^2}$，再得 $\displaystyle\sum_{n=1}^{\infty}n(n-1)x^{n-2}=\dfrac{2}{(1-x)^3}$。于是 $\displaystyle\sum_{n=1}^{\infty}n^2x^n=\sum_{n=1}^{\infty}n(n-1)x^n+\sum_{n=1}^{\infty}nx^n=\dfrac{2x^2}{(1-x)^3}+\dfrac{x}{(1-x)^2}=\dfrac{x(1+x)}{(1-x)^3}$。取 $x=\dfrac{1}{2}$，得 $S=\dfrac{(1/2)(3/2)}{(1/2)^3}=6$。
**解法二（两次错位相减）** 记 $A=\displaystyle\sum_{n=1}^{\infty}\dfrac{n}{2^n}=2$（eval-calc-021）、$B=\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{2^n}=1$。$\dfrac{S}{2}=\displaystyle\sum_{n=1}^{\infty}\dfrac{n^2}{2^{n+1}}=\sum_{m=2}^{\infty}\dfrac{(m-1)^2}{2^m}$，故 $S-\dfrac{S}{2}=\displaystyle\sum_{n=1}^{\infty}\dfrac{n^2-(n-1)^2}{2^n}=\sum_{n=1}^{\infty}\dfrac{2n-1}{2^n}=2A-B=2\cdot 2-1=3$。于是 $\dfrac{S}{2}=3$，$S=6$。
**解法三（概率论：几何分布二阶矩）** 设 $X\sim\operatorname{Geom}(1/2)$（$q=p=\dfrac{1}{2}$）。先算阶乘矩：$E[X(X-1)]=\displaystyle\sum_{k=1}^{\infty}k(k-1)q^{k-1}p=pq\sum_{k=2}^{\infty}k(k-1)q^{k-2}=pq\cdot\dfrac{2}{(1-q)^3}=\dfrac{2q}{p^2}$。故 $E[X^2]=E[X(X-1)]+E[X]=\dfrac{2q}{p^2}+\dfrac{1}{p}=\dfrac{2q+p}{p^2}=\dfrac{2-p}{p^2}$。代入 $p=\dfrac{1}{2}$ 得 $E[X^2]=6$，而 $E[X^2]=\displaystyle\sum_{n=1}^{\infty}n^2\left(\dfrac{1}{2}\right)^n=S$，故 $S=6$。
**思路展开** 与 eval-calc-021 是姊妹题：一次错位/一次求导对应 $\sum n/2^n$，两次对应 $\sum n^2/2^n$。解法二刻意复用了上一题的结果，展示"把新问题降解为已知求和"的链式思想；概率视角下 $\sum n^k/2^n$ 就是几何分布的 $k$ 阶矩。
**解法一动画要点** - 两次逐项求导的系数错位动画 - $n^2x^n=\dfrac{x(1+x)}{(1-x)^3}$ 的推导
**解法二动画要点** - 两级错位相减的竖式结构 - 复用 021 的 $A=2$、$B=1$ 的链式标注
**解法三动画要点** - 阶乘矩 $E[X(X-1)]$ 的求和重整化 - $k$ 阶矩与级数逐阶对应

### eval-calc-023 数学分析 · 正项级数
**题目** 证明级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^2}$ 收敛。
**答案** 证毕（三种证法）
**解法一（积分判别法）** $f(x)=\dfrac{1}{x^2}$ 在 $[1,+\infty)$ 上非负递减，且 $\displaystyle\int_1^{+\infty}\dfrac{dx}{x^2}=1$ 收敛（eval-calc-020 的 $p=2$ 情形），由积分判别法，级数 $\sum\dfrac{1}{n^2}$ 收敛。
**解法二（裂项比较法）** 当 $n\ge 2$ 时 $\dfrac{1}{n^2}<\dfrac{1}{n(n-1)}=\dfrac{1}{n-1}-\dfrac{1}{n}$。部分和 $S_n=1+\displaystyle\sum_{k=2}^{n}\dfrac{1}{k^2}<1+\sum_{k=2}^{n}\left(\dfrac{1}{k-1}-\dfrac{1}{k}\right)=1+\left(1-\dfrac{1}{n}\right)<2$。正项级数部分和单调递增且有上界 2，故收敛。
**解法三（Cauchy 凝聚判别法）** 取 $2^k$ 项凝聚：$\displaystyle\sum_{k=1}^{\infty}2^k\cdot\dfrac{1}{(2^k)^2}=\sum_{k=1}^{\infty}\dfrac{1}{2^k}$ 收敛（几何级数），由 Cauchy 凝聚判别法，原级数收敛。
**思路展开** 三种证法给出三种上界来源：连续面积（积分判别）、裂项相消（部分和显式控制）、二分块凝聚（几何级数控制）。动画可画柱状图与 $y=1/x^2$ 曲线的面积夹逼关系，展示"离散求和被连续积分从上方罩住"。
**解法一动画要点** - 正值递减曲线 $f(x)=1/x^2$ 的三项条件 - 参数 $R$ 高亮 $[1,R]$ 面积 $1-1/R$ - $R\to\infty$ 面积趋于 1 与逐项对应 $a_n=f(n)$
**解法二动画要点** - $1/n^2<1/[n(n-1)]$ 的比较 - 裂项 $1/(n-1)-1/n$ 的逐项抵消 - 部分和上界 $2-1/N<2$ 与单调有界原则
**解法三动画要点** - $a_n$ 按 $2^k$ 标记的分块 - 凝聚项 $2^k a_{2^k}=2^{-k}$ 的建立 - 公比 $\dfrac{1}{2}$ 几何级数的映射

### eval-calc-024 数学分析 · 幂级数
**题目** 求 $\arctan x$ 的幂级数展开式，并由此推导莱布尼茨级数 $\dfrac{\pi}{4}=1-\dfrac{1}{3}+\dfrac{1}{5}-\dfrac{1}{7}+\cdots$。
**答案** $\arctan x=\displaystyle\sum_{n=0}^{\infty}\dfrac{(-1)^n x^{2n+1}}{2n+1}$（$|x|\le 1$）；$x=1$ 时即莱布尼茨级数
**解法一（逐项积分）** 由等比级数 $\dfrac{1}{1+t}=\displaystyle\sum_{n=0}^{\infty}(-1)^nt^{n}$（$|t|<1$），以 $t=x^2$ 代入得 $\dfrac{1}{1+x^2}=\displaystyle\sum_{n=0}^{\infty}(-1)^nx^{2n}$。逐项积分：$\arctan x=\displaystyle\int_0^x\dfrac{dt}{1+t^2}=\sum_{n=0}^{\infty}(-1)^n\int_0^xt^{2n}dt=\sum_{n=0}^{\infty}\dfrac{(-1)^nx^{2n+1}}{2n+1}$（$|x|<1$）。
**解法二（端点取值的 Abel 定理）** $x=1$ 处级数 $\displaystyle\sum_{n=0}^{\infty}\dfrac{(-1)^n}{2n+1}$ 为交错级数（$a_n=\dfrac{1}{2n+1}\searrow 0$），由莱布尼茨判别法收敛；由 Abel 定理，和函数在 $x=1$ 左连续，故 $\arctan 1=\dfrac{\pi}{4}=1-\dfrac{1}{3}+\dfrac{1}{5}-\dfrac{1}{7}+\cdots$。$x=-1$ 同理（或由奇偶性）。
**解法三（泰勒公式余项验证）** 对 $f(x)=\arctan x$ 用带拉格朗日余项的麦克劳林公式：$f^{(n)}(0)$ 由递推 $f'(x)=\dfrac{1}{1+x^2}$ 逐阶求导给出。对 $\arctan$ 可归纳证明 $|f^{(m)}(t)|\le(m-1)!$（$m\ge 1$，对一切实数 $t$），于是余项 $|R_N(x)|=\dfrac{|f^{(N+1)}(\xi)|}{(N+1)!}|x|^{N+1}\le\dfrac{N!}{(N+1)!}\cdot 1=\dfrac{1}{N+1}\to 0$，对 $|x|\le 1$ 一致成立。故展开式在 $|x|\le 1$ 成立，端点处即莱布尼茨级数。
**思路展开** 本题示范"先求导展开、再积分还原"的幂级数标准路线，以及级数端点取值的精细处理（$x=1$ 处需要 Abel 定理，不是简单代入）。动画可展示 $\arctan x$ 的部分和多项式在 $[-1,1]$ 上逐阶逼近，并在 $x=1$ 处展示级数项交替抵消逼近 $\pi/4$ 的过程。
**解法一动画要点** - 等比级数 $\dfrac{1}{1+x^2}=\sum(-1)^nx^{2n}$ 的逐项积分 - 部分和多项式逐阶逼近 $\arctan x$
**解法二动画要点** - $x=1$ 处交错级数逐项加减逼近 $\dfrac{\pi}{4}$ - Abel 定理左连续的标注
**解法三动画要点** - 各阶导 $|f^{(m)}(t)|\le(m-1)!$ 的界标注 - 余项 $\dfrac{1}{N+1}\to0$ 的收敛演示

### eval-calc-025 数学分析 · 交错级数
**题目** 讨论级数 $\displaystyle\sum_{n=2}^{\infty}\frac{(-1)^n}{\ln n}$ 的敛散性，若收敛，判断是绝对收敛还是条件收敛。
**答案** 条件收敛
**解法一（莱布尼茨判别法+绝对收敛检验）** $a_n=\dfrac{1}{\ln n}$ 单调递减且 $\lim_{n\to\infty}a_n=0$，由莱布尼茨判别法，交错级数 $\displaystyle\sum_{n=2}^{\infty}(-1)^na_n$ 收敛。考察绝对级数 $\displaystyle\sum_{n=2}^{\infty}\dfrac{1}{\ln n}$：当 $n\ge 3$ 时 $\dfrac{1}{\ln n}>\dfrac{1}{n}$（因 $\ln n<n$），而调和级数 $\sum\dfrac{1}{n}$ 发散，由比较判别法绝对级数发散。因此原级数条件收敛。
**解法二（部分和分组估计）** 记 $a_n=\dfrac{1}{\ln n}$，$S_n=\displaystyle\sum_{k=2}^{n}(-1)^ka_k$。配对求和：$S_{2m+1}=\displaystyle\sum_{j=1}^{m}(a_{2j}-a_{2j+1})$，每项为正，故奇子列 $S_{2m+1}$ 随 $m$ 递增；又 $a_{2j}-a_{2j+1}<a_{2j}-a_{2j+2}$，故 $S_{2m+1}<\displaystyle\sum_{j=1}^{m}(a_{2j}-a_{2j+2})=\dfrac{1}{\ln 2}-\dfrac{1}{\ln(2m+2)}<\dfrac{1}{\ln 2}$，奇子列有上界，收敛。偶子列 $S_{2m}=S_{2m+1}+a_{2m+1}$，与奇子列之差 $a_{2m+1}\to 0$，故 $S_n$ 收敛。绝对发散仍由解法一的比较法给出。
**解法三（与调和级数对比的收敛速度观察）** 数值观察：$\displaystyle\sum_{k=2}^{n}\dfrac{1}{\ln k}$ 约为 $\dfrac{n}{\ln n}$ 量级（发散），而交错后正负相消使部分和在极限值附近振荡——用图形展示振荡收敛与无条件发散的反差。严格结论仍由解法一给出，本解法用于建立几何直觉。
**思路展开** 本题强调"收敛"与"绝对收敛"的差别：$\dfrac{1}{\ln n}$ 下降得比 $\dfrac{1}{n}$ 还慢（因为 $\ln n<n$），所以绝对级数发散，但交错结构仍能压出条件收敛。动画可并排展示原级数部分和的振荡收敛曲线与绝对级数部分和的单调发散曲线。
**解法一动画要点** - 单调递减项 $a_n=\dfrac{1}{\ln n}$ 的柱状图 - 与调和级数 $\dfrac{1}{n}$ 的比较标注
**解法二动画要点** - 奇子列 $S_{2m+1}$ 递增有上界的折线 - 偶子列 $S_{2m}$ 与奇子列之差 $a_{2m+1}\to0$ 的配对相消放大
**解法三动画要点** - 交错部分和振荡收敛折线 - 绝对级数部分和单调发散对比

### eval-calc-026 数学分析 · 多元函数微分
**题目** 设 $z=x^y$（$x>0$），求 $z$ 在点 $(1,2)$ 处的两个偏导数。
**答案** $z_x(1,2)=2$，$z_y(1,2)=0$
**解法一（直接按定义求偏导）** 把 $y$ 视为常数：$z_x=yx^{y-1}$，故 $z_x(1,2)=2\cdot 1^{2-1}=2$。把 $x$ 视为常数：$z_y=x^y\ln x$，故 $z_y(1,2)=1^2\cdot\ln 1=0$。
**解法二（全微分）** 对 $\ln z=y\ln x$ 两边求全微分：$\dfrac{dz}{z}=\dfrac{y}{x}dx+\ln x\,dy$。在 $(1,2)$ 处 $z=1$、$\dfrac{y}{x}=2$、$\ln x=0$，故 $dz=2\,dx+0\cdot dy$，即 $z_x=2$、$z_y=0$。
**解法三（数值差分验证）** 取步长 $h=10^{-4}$：$z_x\approx\dfrac{(1+h)^2-1^2}{h}=\dfrac{2h+h^2}{h}=2+h\to 2$；$z_y\approx\dfrac{1^{2+h}-1}{h}=\dfrac{0}{h}=0$。数值结果与解析一致，说明 $z_y(1,2)=0$ 反映曲面在 $y$ 方向局部水平。
**思路展开** $x^y$ 在 $x=1$ 处对 $y$ 的偏导为 0 是个易错点（$\ln 1=0$），解法三的差分验证是防错手段。全微分法把两个偏导合并为一次微分运算，在隐式结构中更省力。动画可画曲面 $z=x^y$ 在 $(1,2,1)$ 附近的局部放大，展示沿 $x$ 方向倾斜、沿 $y$ 方向水平的切平面。
**解法一动画要点** - 沿 $x$ 方向固定 $y=2$ 的截面曲线 $z=x^2$ - 沿 $y$ 方向固定 $x=1$ 的截面曲线 $z=1^y$
**解法二动画要点** - 全微分 $\dfrac{dz}{z}=\dfrac{y}{x}dx+\ln x\,dy$ 的推导 - 切平面沿 $x$ 倾斜、沿 $y$ 水平的标注
**解法三动画要点** - 差分步长 $h$ 收缩动画 - 两方向差商分别趋近 2 与 0

### eval-calc-027 数学分析 · 重积分
**题目** 求二重积分 $\displaystyle I=\int_0^1\!\!\int_x^1 e^{y^2}\,dy\,dx$。
**答案** $\dfrac{e-1}{2}$
**解法一（交换积分次序）** 积分区域为 $D=\{(x,y):0\le x\le 1,\ x\le y\le 1\}=\{(x,y):0\le y\le 1,\ 0\le x\le y\}$。交换次序：$I=\displaystyle\int_0^1\!\!\int_0^y e^{y^2}\,dx\,dy=\int_0^1 y\,e^{y^2}\,dy$。令 $u=y^2$（$du=2y\,dy$）：$I=\dfrac{1}{2}\displaystyle\int_0^1 e^u\,du=\dfrac{1}{2}(e-1)$。
**解法二（分部积分）** 记 $F(x)=\displaystyle\int_x^1e^{y^2}dy$，则 $I=\displaystyle\int_0^1F(x)dx$，且 $F(1)=0$、$F'(x)=-e^{x^2}$。分部积分：$I=\left[xF(x)\right]_0^1-\displaystyle\int_0^1xF'(x)dx=0-\int_0^1x\left(-e^{x^2}\right)dx=\int_0^1xe^{x^2}dx=\left[\dfrac{e^{x^2}}{2}\right]_0^1=\dfrac{e-1}{2}$。
**解法三（数值验证，辅助校验）** 若按原次序先积 $y$，需要 $\int e^{y^2}dy$ 的原函数，而由刘维尔定理 $e^{y^2}$ 没有初等原函数，直接路线注定失败——这正是必须交换次序（或改用解法二）的信号。作为辅助校验，用二重黎曼和（如 $1000\times 1000$ 网格）估算 $I\approx 0.85914$，与解析值 $\dfrac{e-1}{2}=0.859141\cdots$ 吻合。
**思路展开** 本题是"交换积分次序"动机的最佳素材：被积函数 $e^{y^2}$ 无初等原函数，但换序后先对 $x$ 积分把 $y$ 乘出来，立刻化为基本积分；解法二分部积分则完全绕开换序，给出第二条独立解析路径。动画可先展示区域 $D$（三角形）按竖条扫描时的受阻，再切换为横条扫描的一气呵成。
**解法一动画要点** - 积分区域 $D$ 竖条扫描受阻的演示 - 换为横条扫描后 $y\,e^{y^2}$ 的一气呵成 - 换序前后对照
**解法二动画要点** - 分部积分 $u=F(x)$、$dv=dx$ 的选取 - 边界项 $xF(x)\big|_0^1=0$ 的标注 - $F'=-e^{x^2}$ 的代入
**解法三动画要点** - 二重黎曼和网格加密 - 数值 0.85914 与 $\dfrac{e-1}{2}$ 同框对照

### eval-calc-028 数学分析 · 重积分
**题目** 求二重积分 $\displaystyle I=\iint_D(x^2+y^2)\,dA$，其中 $D=\{(x,y):x^2+y^2\le 2y\}$。
**答案** $\dfrac{3\pi}{2}$
**解法一（极坐标）** $D$ 是圆心 $(0,1)$、半径 $1$ 的圆盘，极坐标下边界 $r=2\sin\theta$（$\theta\in[0,\pi]$），且 $x^2+y^2=r^2$、$dA=r\,dr\,d\theta$。$I=\displaystyle\int_0^{\pi}\!\!\int_0^{2\sin\theta}r^2\cdot r\,dr\,d\theta=\int_0^{\pi}\left[\dfrac{r^4}{4}\right]_0^{2\sin\theta}d\theta=\int_0^{\pi}4\sin^4\theta\,d\theta$。由 $\displaystyle\int_0^{\pi}\sin^4\theta\,d\theta=\dfrac{3\pi}{8}$（倍角降次即得），故 $I=4\cdot\dfrac{3\pi}{8}=\dfrac{3\pi}{2}$。
**解法二（直角坐标）** $D:0\le y\le 2,\ -\sqrt{2y-y^2}\le x\le\sqrt{2y-y^2}$。先对 $x$ 积分：内层 $=\left[\dfrac{x^3}{3}+xy^2\right]_{-\sqrt{2y-y^2}}^{\sqrt{2y-y^2}}=2\left[\dfrac{(2y-y^2)^{3/2}}{3}+y^2\sqrt{2y-y^2}\right]=2\sqrt{2y-y^2}\left[\dfrac{2y-y^2}{3}+y^2\right]=\dfrac{4}{3}y(1+y)\sqrt{2y-y^2}$。故 $I=\dfrac{4}{3}\displaystyle\int_0^2 y(1+y)\sqrt{2y-y^2}\,dy$。令 $u=y-1$（平移至圆心），则 $y(1+y)=(1+u)(2+u)=2+3u+u^2$，$\sqrt{2y-y^2}=\sqrt{1-u^2}$，$u:-1\to 1$。$I=\dfrac{4}{3}\displaystyle\int_{-1}^{1}(2+3u+u^2)\sqrt{1-u^2}\,du=\dfrac{4}{3}\left[2\cdot\dfrac{\pi}{2}+3\cdot 0+\dfrac{\pi}{8}\right]=\dfrac{4}{3}\cdot\dfrac{9\pi}{8}=\dfrac{3\pi}{2}$（其中 $\int_{-1}^{1}\sqrt{1-u^2}du=\dfrac{\pi}{2}$ 为半圆面积，$u\sqrt{1-u^2}$ 为奇函数积分为 0，$\int_{-1}^{1}u^2\sqrt{1-u^2}du=\dfrac{\pi}{8}$ 由三角代换 $u=\sin t$ 即得）。
**解法三（平行轴定理/极惯性矩）** 被积函数 $x^2+y^2$ 是到原点的距离平方，积分即区域 $D$ 关于原点 $O$ 的极惯性矩 $J_O$。由平行轴定理 $J_O=J_C+Ad^2$，其中 $J_C$ 是圆盘关于自身圆心 $C$ 的极惯性矩 $J_C=\dfrac{\pi R^4}{2}=\dfrac{\pi}{2}$，$A=\pi$ 为面积，$d=|OC|=1$ 为圆心到原点的距离。故 $I=J_O=\dfrac{\pi}{2}+\pi\cdot 1^2=\dfrac{3\pi}{2}$。
**思路展开** 本题展示极坐标在"圆盘+径向函数"型被积函数上的统治力：$x^2+y^2=r^2$ 与 $dA=r\,dr\,d\theta$ 完美匹配。直角坐标也完全可算（平移后三个标准积分一次解决），平行轴定理则把它看成物理量（极惯性矩）一步到位。三法分别代表坐标选择、直接计算、物理模型三条路线。
**解法一动画要点** - 圆盘 $D$ 与极角 $\theta\in[0,\pi]$ 的扇形扫描 - $r^4$ 径向积分与 $\sin^4\theta$ 的倍角降次
**解法二动画要点** - 水平条带平移 $u=y-1$ 的示意 - 三个标准积分 $\dfrac{\pi}{2},0,\dfrac{\pi}{8}$ 的分解标注
**解法三动画要点** - 平行轴定理的物理示意（圆盘+偏心距 $d=1$） - $J_C=\dfrac{\pi R^4}{2}$ 与 $Ad^2$ 的叠加

### eval-calc-029 数学分析 · 定积分的应用
**题目** 求星形线 $x^{2/3}+y^{2/3}=a^{2/3}$（$a>0$）的周长。
**答案** $6a$
**解法一（参数方程弧长）** 参数化 $x=a\cos^3 t$、$y=a\sin^3 t$（$t\in[0,2\pi]$）。$x'=-3a\cos^2 t\sin t$，$y'=3a\sin^2 t\cos t$，弧长微元 $ds=\sqrt{(x')^2+(y')^2}\,dt=\sqrt{9a^2\cos^4 t\sin^2 t+9a^2\sin^4 t\cos^2 t}\,dt=3a|\sin t\cos t|\,dt$。由对称性取第一象限：$L=4\displaystyle\int_0^{\pi/2}3a\sin t\cos t\,dt=12a\left[\dfrac{\sin^2 t}{2}\right]_0^{\pi/2}=12a\cdot\dfrac{1}{2}=6a$。
**解法二（隐式方程弧长）** 由隐函数求导（eval-calc-007）$y'=-\left(\dfrac{y}{x}\right)^{1/3}$，故弧长微元 $ds=\sqrt{1+(y')^2}\,dx=\sqrt{1+(y/x)^{2/3}}\,dx=\sqrt{\dfrac{x^{2/3}+y^{2/3}}{x^{2/3}}}\,dx$。由星形线方程 $x^{2/3}+y^{2/3}=a^{2/3}$，得 $ds=a^{1/3}x^{-1/3}dx$。第一象限部分：$L_1=\displaystyle\int_0^a a^{1/3}x^{-1/3}dx=a^{1/3}\left[\dfrac{3}{2}x^{2/3}\right]_0^a=\dfrac{3a}{2}$，故 $L=4L_1=6a$。
**解法三（滑动线段包络法）** 考虑两端分别在坐标轴上、长为 $a$ 的滑动线段：端点 $E_1(t)=(a\cos t,0)$、$E_2(t)=(0,a\sin t)$。线段上参数 $v\in[0,1]$ 的点为 $P(t,v)=\big(a(1-v)\cos t,\ a v\sin t\big)$。包络条件 $\dfrac{\partial P}{\partial t}$ 与 $\dfrac{\partial P}{\partial v}$ 平行：$\left(-a(1-v)\sin t,\ av\cos t\right)$ 与 $\left(-a\cos t,\ a\sin t\right)$ 平行，叉积为零：$-a^2(1-v)\sin^2 t+a^2v\cos^2 t=0$，解得 $v=\sin^2 t$。代入得包络点 $\big(a\cos t(1-\sin^2 t),\ a\sin^3 t\big)=\big(a\cos^3 t,\ a\sin^3 t\big)$——正是星形线。于是星形线是定长滑动线段的包络，其弧长即解法一的参数曲线弧长：四分之一部分 $\displaystyle\int_0^{\pi/2}3a\sin t\cos t\,dt=\dfrac{3a}{2}$，全长 $6a$。
**思路展开** 参数方程法最顺畅（星形线天然有参数表示），隐式法展示了 $y'$ 的分数幂结构在弧长公式中的化简，包络法揭示了星形线的生成机制（滑动线段包络）并给出"切线被坐标轴截出的线段长恒为 $a$"这一几何事实。动画可用"滑动线段包络"动态生成星形线。
**解法一动画要点** - 弧长微元 $ds=3a|\sin t\cos t|dt$ 沿曲线移动 - 四分之一对称性叠加
**解法二动画要点** - 隐式导数 $y'=-(y/x)^{1/3}$ 的推导 - $ds=a^{1/3}x^{-1/3}dx$ 的化简与积分
**解法三动画要点** - 滑动线段包络生成星形线 - 包络条件叉积为零的推导 - 切点把切线分成 $a\sin^2t$ 与 $a\cos^2t$ 的标注

### eval-calc-030 数学分析 · 定积分的应用
**题目** 求由 $y=\sin x$（$0\le x\le\pi$）与 $x$ 轴围成的区域绕 $y$ 轴旋转所得旋转体的体积。
**答案** $2\pi^2$
**解法一（壳层法）** 在 $x$ 处取高度 $\sin x$、厚度 $dx$ 的竖直壳层，其体积微元 $dV=2\pi x\sin x\,dx$。$V=\displaystyle\int_0^{\pi}2\pi x\sin x\,dx$。分部积分（$u=x$、$dv=\sin x\,dx$）：$\displaystyle\int_0^{\pi}x\sin x\,dx=\left[-x\cos x\right]_0^{\pi}+\int_0^{\pi}\cos x\,dx=\pi+\left[\sin x\right]_0^{\pi}=\pi$。故 $V=2\pi\cdot\pi=2\pi^2$。
**解法二（帕普斯定理）** 区域面积 $A=\displaystyle\int_0^\pi\sin x\,dx=\left[-\cos x\right]_0^\pi=2$。质心横坐标 $\bar x=\dfrac{1}{A}\displaystyle\int_0^\pi x\sin x\,dx=\dfrac{\pi}{2}$（区域关于 $x=\dfrac{\pi}{2}$ 对称，且上式已算出积分为 $\pi$）。由帕普斯定理（绕 $y$ 轴，轴不穿过区域内部），$V=2\pi\bar x A=2\pi\cdot\dfrac{\pi}{2}\cdot 2=2\pi^2$。
**解法三（圆盘法，需分段）** 绕 $y$ 轴时取水平圆盘：对 $0\le y\le 1$，水平线 $y$ 与区域相交于 $x=\arcsin y$（左）与 $x=\pi-\arcsin y$（右），圆盘外半径 $R=\pi-\arcsin y$、内半径 $r=\arcsin y$。$V=\pi\displaystyle\int_0^1\left[(\pi-\arcsin y)^2-(\arcsin y)^2\right]dy=\pi\int_0^1(\pi^2-2\pi\arcsin y)\,dy=\pi\left[\pi^2y-2\pi\int_0^1\arcsin y\,dy\right]$。其中 $\displaystyle\int_0^1\arcsin y\,dy=\left[y\arcsin y+\sqrt{1-y^2}\right]_0^1=\dfrac{\pi}{2}-1$。故 $V=\pi\left[\pi^2-2\pi\left(\dfrac{\pi}{2}-1\right)\right]=\pi\left[\pi^2-\pi^2+2\pi\right]=2\pi^2$。
**思路展开** 绕 $y$ 轴时壳层法一次成型，圆盘法却要解出反函数 $x=\arcsin y$ 并做内外半径相减——这是"绕哪根轴选哪种方法"的经典判据。帕普斯定理把体积化为质心计算，展示了对称性红利。动画可展示壳层展开成薄板的扫掠过程，或圆盘法的环形截面。
**解法一动画要点** - 竖直壳层扫掠并展开成薄板 - 分部积分 $\int x\sin x\,dx$ 的步骤
**解法二动画要点** - 质心横坐标 $\bar x=\dfrac{\pi}{2}$ 的标注 - 帕普斯旋转示意（质心轨迹圆）
**解法三动画要点** - 水平圆盘的内外半径 $\pi-\arcsin y$ 与 $\arcsin y$ - 环形截面随 $y$ 扫掠

# 二、解析几何（20 题）

### eval-geom-001 解析几何 · 直线与平面
**题目** 求点 $P(1,2,-1)$ 到平面 $\pi:2x-y+2z=3$ 的距离。
**答案** $\dfrac{5}{3}$
**解法一（距离公式）** 平面法向量 $\vec n=(2,-1,2)$，$|\vec n|=\sqrt{4+1+4}=3$。代入点到平面距离公式：$d=\dfrac{|2\cdot 1-1\cdot 2+2\cdot(-1)-3|}{3}=\dfrac{|2-2-2-3|}{3}=\dfrac{5}{3}$。
**解法二（投影向量）** 取平面上一点 $Q(0,-3,0)$（$2\cdot 0-(-3)+2\cdot 0=3$ 满足方程），则 $\overrightarrow{QP}=(1,5,-1)$。$P$ 到平面的距离等于 $\overrightarrow{QP}$ 在法向量上的投影长度：$d=\dfrac{|\overrightarrow{QP}\cdot\vec n|}{|\vec n|}=\dfrac{|1\cdot 2+5\cdot(-1)+(-1)\cdot 2|}{3}=\dfrac{5}{3}$。垂足为 $P$ 减去投影向量 $\dfrac{\overrightarrow{QP}\cdot\vec n}{|\vec n|^2}\vec n=\dfrac{-5}{9}(2,-1,2)$，即 $\left(\dfrac{19}{9},\dfrac{13}{9},\dfrac{1}{9}\right)$。
**解法三（拉格朗日乘数法）** 求 $f(x,y,z)=(x-1)^2+(y-2)^2+(z+1)^2$ 在约束 $2x-y+2z-3=0$ 下的最小值。由 $\nabla f=\lambda\nabla(2x-y+2z-3)$：$2(x-1)=2\lambda$，$2(y-2)=-\lambda$，$2(z+1)=2\lambda$，得 $x-1=\lambda$，$y-2=-\dfrac{\lambda}{2}$，$z+1=\lambda$。代入约束：$2(1+\lambda)-\left(2-\dfrac{\lambda}{2}\right)+2(\lambda-1)=3$，即 $\dfrac{9\lambda}{2}-2=3$，解得 $\lambda=\dfrac{10}{9}$。最近距离 $d=\sqrt{\lambda^2+\dfrac{\lambda^2}{4}+\lambda^2}=\dfrac{3}{2}|\lambda|=\dfrac{5}{3}$。
**思路展开** 三种方法分别代表公式代入、几何投影、优化极值三条路线。投影法顺带给出垂足坐标，拉格朗日法把几何问题转化为约束优化——后者在"曲面到点距离"类问题中可迁移性最强。动画可在三维中画出平面、法向量与垂线段，并让垂线段旋转到任意视角都保持最短。
**解法一动画要点** - 三维平面与法向量 $\vec n=(2,-1,2)$ - 距离公式分子绝对值的标注
**解法二动画要点** - 投影向量的分解动画 - 垂足 $\left(\dfrac{19}{9},\dfrac{13}{9},\dfrac{1}{9}\right)$ 坐标标注
**解法三动画要点** - 约束平面上的等高线 - 梯度与法向量平行的最优点标注

### eval-geom-002 解析几何 · 直线与平面
**题目** 判断两条直线 $l_1:\dfrac{x-1}{2}=\dfrac{y+1}{1}=\dfrac{z-2}{-1}$ 与 $l_2:\dfrac{x+1}{1}=\dfrac{y-2}{2}=\dfrac{z}{1}$ 的位置关系。
**答案** 异面直线
**解法一（混合积判别）** $l_1$ 的方向向量 $\vec{s_1}=(2,1,-1)$，$l_2$ 的 $\vec{s_2}=(1,2,1)$。叉积 $\vec{s_1}\times\vec{s_2}=(1\cdot 1-(-1)\cdot 2,\ (-1)\cdot 1-2\cdot 1,\ 2\cdot 2-1\cdot 1)=(3,-3,3)\ne\vec 0$，故不平行。取 $P_1(1,-1,2)\in l_1$、$P_2(-1,2,0)\in l_2$，$\overrightarrow{P_1P_2}=(-2,3,-2)$。混合积 $\overrightarrow{P_1P_2}\cdot(\vec{s_1}\times\vec{s_2})=-2\cdot 3+3\cdot(-3)+(-2)\cdot 3=-21\ne 0$，故两直线不共面，即异面。
**解法二（方程组判别）** 参数化：$l_1:(1+2t,-1+t,2-t)$，$l_2:(-1+s,2+2s,s)$。若相交，需 $1+2t=-1+s$、$-1+t=2+2s$、$2-t=s$ 同时成立。由第三式 $s=2-t$ 代入第一式：$1+2t=-1+2-t$，得 $t=0$、$s=2$；代入第二式检验：$-1+0=2+4$，即 $-1=6$，矛盾。故无公共点；结合方向向量不平行，得异面。
**解法三（几何观察）** 两直线方向向量不平行（$\vec{s_1}\times\vec{s_2}\ne 0$），若相交则必共面；其公垂线方向为 $\vec{s_1}\times\vec{s_2}=(3,-3,3)$。解法二已排除相交，故两直线不平行、不相交，只能异面。
**思路展开** 空间两直线位置关系只有平行、相交、异面三种，判别的核心工具就是叉积与混合积：叉积判平行、混合积判共面。解法二是最原始的坐标法，解法三强调分类的逻辑完备性。动画可在三维中旋转视角，展示两直线"看似相交实则错开"的立体感。
**解法一动画要点** - 叉积 $\vec{s_1}\times\vec{s_2}=(3,-3,3)$ 的方向动画 - 混合积 $-21\ne0$ 的平行六面体示意
**解法二动画要点** - 参数方程三式联立的代入动画 - 矛盾式 $-1=6$ 的高亮
**解法三动画要点** - 三维两直线与方向向量箭头 - 视角旋转揭示"看似相交"

### eval-geom-003 解析几何 · 直线与平面
**题目** 求过直线 $l:\dfrac{x-1}{1}=\dfrac{y}{2}=\dfrac{z+1}{1}$ 且垂直于平面 $\pi:x+y+z=0$ 的平面方程。
**答案** $x-z=2$
**解法一（法向量叉积）** 直线方向 $\vec s=(1,2,1)$，$\pi$ 的法向量 $\vec{n_1}=(1,1,1)$。所求平面含直线 $l$ 且垂直于 $\pi$，故其法向量 $\vec n\perp\vec s$ 且 $\vec n\perp\vec{n_1}$，取 $\vec n=\vec s\times\vec{n_1}=(2\cdot 1-1\cdot 1,\ 1\cdot 1-1\cdot 1,\ 1\cdot 1-2\cdot 1)=(1,0,-1)$。过直线上一点 $P_0(1,0,-1)$：$1\cdot(x-1)+0\cdot y+(-1)\cdot(z+1)=0$，即 $x-z=2$。检验：直线上点 $(1+t,2t,-1+t)$ 满足 $(1+t)-(-1+t)=2$；$|\vec n\cdot\vec{n_1}|=|1-1|=0$ 故与 $\pi$ 垂直。
**解法二（平面束）** 把 $l$ 写成两平面交线：由 $\dfrac{x-1}{1}=\dfrac{y}{2}$ 得 $y=2x-2$，由 $\dfrac{y}{2}=\dfrac{z+1}{1}$ 得 $y=2z+2$。过 $l$ 的平面束为 $(2x-2-y)+\lambda(2z+2-y)=0$，其法向量为 $(2,-1-\lambda,2\lambda)$。与 $\pi$ 垂直要求 $2\cdot 1+(-1-\lambda)\cdot 1+2\lambda\cdot 1=0$，即 $1+\lambda=0$，$\lambda=-1$。代入：$(2x-2-y)-(2z+2-y)=0$，即 $2x-2z-4=0$，$x-z=2$。
**解法三（点+两方向向量）** 所求平面过 $P_0(1,0,-1)$ 且含方向 $\vec s=(1,2,1)$；又因垂直于 $\pi$，平面法向量必与 $\vec{n_1}$ 垂直，故 $\vec{n_1}$ 必平行于所求平面，可作为平面内第二个方向向量。平面法向量 $\vec n=\vec s\times\vec{n_1}=(1,0,-1)$（同解法一），得 $x-z=2$。
**思路展开** 本题三种方法的共同点是"找平面法向量"：解法一直接叉积，解法二用平面束参数化后解垂直条件，解法三从几何意义（$\vec n_1$ 躺在所求平面内）出发。平面束法是处理"过定直线满足某条件的平面"的通用武器。动画可先展示直线与平面 $\pi$，再旋转生成所求平面并验证垂直。
**解法一动画要点** - 法向量叉积 $\vec n=\vec s\times\vec{n_1}=(1,0,-1)$ 的方向动画 - 直线 $l$ 与平面 $\pi$ 的三维展示
**解法二动画要点** - 平面束 $(2x-2-y)+\lambda(2z+2-y)=0$ 旋转扫描到垂直位置 - 垂直条件 $1+\lambda=0$ 的求解
**解法三动画要点** - $\vec{n_1}$ 躺在所求平面内的几何标注 - 点 $P_0$ 与两方向向量张成平面的过程

### eval-geom-004 解析几何 · 直线与平面
**题目** 求两平面 $\pi_1:x-y+z=1$ 与 $\pi_2:2x+y-z=0$ 的夹角。
**答案** $\dfrac{\pi}{2}$（两平面垂直）
**解法一（法向量夹角公式）** $\vec{n_1}=(1,-1,1)$，$\vec{n_2}=(2,1,-1)$。点积 $\vec{n_1}\cdot\vec{n_2}=1\cdot 2+(-1)\cdot 1+1\cdot(-1)=0$，故 $\cos\theta=\dfrac{|\vec{n_1}\cdot\vec{n_2}|}{|\vec{n_1}||\vec{n_2}|}=0$，两平面夹角为 $\dfrac{\pi}{2}$。
**解法二（交线与截面直线）** 两平面交线方向 $\vec s=\vec{n_1}\times\vec{n_2}=((-1)(-1)-1\cdot 1,\ 1\cdot 2-1\cdot(-1),\ 1\cdot 1-(-1)\cdot 2)=(0,3,3)$，取 $\vec s=(0,1,1)$。在 $\pi_1$ 内取垂直于交线的方向 $\vec{d_1}=\vec{n_1}\times\vec s=((-1)\cdot 1-1\cdot 1,\ 1\cdot 0-1\cdot 1,\ 1\cdot 1-(-1)\cdot 0)=(-2,-1,1)$；在 $\pi_2$ 内取 $\vec{d_2}=\vec{n_2}\times\vec s=(1\cdot 1-(-1)\cdot 1,\ (-1)\cdot 0-2\cdot 1,\ 2\cdot 1-1\cdot 0)=(2,-2,2)$。两平面夹角即 $\vec{d_1}$ 与 $\vec{d_2}$ 的夹角：$\vec{d_1}\cdot\vec{d_2}=-4+2+2=0$，夹角 $\dfrac{\pi}{2}$。
**解法三（法向量共面观察）** 检验 $\pi_2$ 的法向量是否平行于 $\pi_1$ 的方向空间：$\vec{n_2}=(2,1,-1)$ 代入 $\pi_1$ 的齐次方程 $x-y+z$ 得 $2-1-1=0$，说明 $\vec{n_2}$ 是 $\pi_1$ 内的一个方向向量，即一个平面的法向量躺在另一个平面内，这正是两平面垂直的充要条件。
**思路展开** 两平面夹角本质是其法向量夹角；解法二展示"交线+截面直线"的立体几何视角（二面角的平面角），解法三给出垂直的等价刻画（法向量在对方平面内）。动画可展示两平面相交成直角，并用垂直于交线的两条截面直线标出平面角。
**解法一动画要点** - 法向量夹角联动显示 - 点积 $\vec{n_1}\cdot\vec{n_2}=0$ 的标注
**解法二动画要点** - 交线方向 $\vec s=(0,1,1)$ 的提取 - 截面直线 $\vec{d_1}$、$\vec{d_2}$ 标出平面角 $90^\circ$
**解法三动画要点** - 法向量 $\vec{n_2}$ 代入 $\pi_1$ 齐次方程得 0 的验证 - 两垂直平面的三维展示

### eval-geom-005 解析几何 · 直线与平面
**题目** 求点 $P(2,1,0)$ 到直线 $l:\dfrac{x-1}{1}=\dfrac{y}{2}=\dfrac{z+1}{1}$ 的距离。
**答案** $\dfrac{1}{\sqrt{3}}$
**解法一（叉积公式）** 取直线上点 $P_0(1,0,-1)$、方向向量 $\vec s=(1,2,1)$，$\overrightarrow{P_0P}=(1,1,1)$。叉积 $\overrightarrow{P_0P}\times\vec s=(1\cdot 1-1\cdot 2,\ 1\cdot 1-1\cdot 1,\ 1\cdot 2-1\cdot 1)=(-1,0,1)$，模 $\sqrt{2}$。距离 $d=\dfrac{|\overrightarrow{P_0P}\times\vec s|}{|\vec s|}=\dfrac{\sqrt{2}}{\sqrt{6}}=\dfrac{1}{\sqrt{3}}$。
**解法二（参数化求最小值）** 直线上点 $Q(t)=(1+t,2t,-1+t)$。$|PQ|^2=(t-1)^2+(2t-1)^2+(t-1)^2=2(t-1)^2+(2t-1)^2=6t^2-8t+3$。配方：$6\left(t-\dfrac{2}{3}\right)^2+\dfrac{1}{3}$，最小值 $\dfrac{1}{3}$ 在 $t=\dfrac{2}{3}$ 处取得，故 $d=\sqrt{\dfrac{1}{3}}=\dfrac{1}{\sqrt{3}}$。
**解法三（正交投影）** 垂足参数 $t^*=\dfrac{\overrightarrow{P_0P}\cdot\vec s}{|\vec s|^2}=\dfrac{1\cdot 1+1\cdot 2+1\cdot 1}{6}=\dfrac{2}{3}$，垂足 $Q=\left(\dfrac{5}{3},\dfrac{4}{3},-\dfrac{1}{3}\right)$。$d=|PQ|=\sqrt{\left(\dfrac{1}{3}\right)^2+\left(-\dfrac{1}{3}\right)^2+\left(\dfrac{1}{3}\right)^2}=\dfrac{1}{\sqrt{3}}$。检验垂足在直线上：$\dfrac{5/3-1}{1}=\dfrac{4/3}{2}=\dfrac{-1/3+1}{1}=\dfrac{2}{3}$。
**思路展开** 叉积公式是"面积÷底=高"的几何直译，参数化法把距离问题化为二次函数最值（纯代数），投影法给出垂足坐标。三种方法在"点到平面距离"类问题中都有对应版本，构成空间距离计算的方法体系。动画可展示三角形 $P_0QP$ 中高与底的对应关系。
**解法一动画要点** - 叉积 $\overrightarrow{P_0P}\times\vec s=(-1,0,1)$ 的平行四边形面积分解 - 面积÷底=高的标注
**解法二动画要点** - $|PQ(t)|^2=6t^2-8t+3$ 的二次函数曲线与最低点 - 参数 $t=\dfrac{2}{3}$ 的定位
**解法三动画要点** - 垂足 $Q=\left(\dfrac{5}{3},\dfrac{4}{3},-\dfrac{1}{3}\right)$ 的投影标注 - 垂线段长度 $\dfrac{1}{\sqrt3}$

### eval-geom-006 解析几何 · 直线与平面
**题目** 讨论三个平面 $\pi_1:x+y+z=1$，$\pi_2:x-y+z=1$，$\pi_3:2x+2z=2$ 的位置关系，并求其公共部分。
**答案** 三平面共线，交线为 $y=0,\ x+z=1$
**解法一（高斯消元/秩）** 系数矩阵与增广矩阵行变换：$\begin{pmatrix}1&1&1&1\\1&-1&1&1\\2&0&2&2\end{pmatrix}\to\begin{pmatrix}1&1&1&1\\0&-2&0&0\\0&-2&0&0\end{pmatrix}\to\begin{pmatrix}1&1&1&1\\0&1&0&0\\0&0&0&0\end{pmatrix}$。秩 $\mathrm r(A)=\mathrm r(\bar A)=2<3$，无穷多解，解空间一维：$y=0$，$x+z=1$，即一条直线。
**解法二（几何分析：方程相加）** 观察 $\pi_3$ 的方程恰是 $\pi_1$ 与 $\pi_2$ 方程之和，故 $\pi_3$ 必过 $\pi_1\cap\pi_2$ 的每一点。求 $\pi_1\cap\pi_2$：两式相减得 $2y=0$，$y=0$；代回得 $x+z=1$。故公共部分为直线 $\begin{cases}y=0\\x+z=1\end{cases}$，参数化 $(x,y,z)=(t,0,1-t)$。检验满足 $\pi_3$：$2t+2(1-t)=2$。
**解法三（向量法）** 三个法向量 $\vec{n_1}=(1,1,1)$、$\vec{n_2}=(1,-1,1)$、$\vec{n_3}=(2,0,2)$ 满足 $\vec{n_3}=\vec{n_1}+\vec{n_2}$，故共面。交线方向 $\vec s=\vec{n_1}\times\vec{n_2}=(1\cdot 1-1\cdot(-1),\ 1\cdot 1-1\cdot 1,\ 1\cdot(-1)-1\cdot 1)=(2,0,-2)$，取 $\vec s=(1,0,-1)$。找交线上一点：令 $y=0$，解 $x+z=1$，取 $(1,0,0)$。交线为 $(x,y,z)=(1+t,0,-t)$。
**思路展开** 三个平面共有八种位置关系（平行、相交成线、交于一点等），判别的代数工具是系数矩阵与增广矩阵的秩。本题的特殊性在于 $\pi_3$ 是 $\pi_1,\pi_2$ 的线性组合，几何上"第三个平面穿过前两个的交线"。动画可展示三张平面像书页一样共轴打开。
**解法一动画要点** - 增广矩阵行变换的逐步动画 - 秩 $2<3$ 与解空间一维的对应标注
**解法二动画要点** - 方程相加的几何含义 - 三平面共线交叠的三维视图
**解法三动画要点** - 法向量关系 $\vec{n_3}=\vec{n_1}+\vec{n_2}$ 的标注 - 交线方向 $\vec s=(1,0,-1)$ 与交点 $(1,0,0)$

### eval-geom-007 解析几何 · 二次曲面分类
**题目** 指出方程 $4x^2-y^2+z^2=1$ 表示的二次曲面类型，并用截面法说明其形状。
**答案** 单叶双曲面（以 $y$ 轴为对称轴）
**解法一（标准型判断）** 方程化为 $\dfrac{x^2}{1/4}+\dfrac{z^2}{1}-\dfrac{y^2}{1}=1$，形如 $\dfrac{x^2}{a^2}+\dfrac{z^2}{b^2}-\dfrac{y^2}{c^2}=1$（一个负号项），是单叶双曲面，对称轴为 $y$ 轴。
**解法二（截面法）** 用 $y=k$ 截：$4x^2+z^2=1+k^2$，即 $\dfrac{x^2}{(1+k^2)/4}+\dfrac{z^2}{1+k^2}=1$，恒为椭圆，且随 $|k|$ 增大而变大（"中间细、两头粗"）。用 $z=k$ 截：$4x^2-y^2=1-k^2$，$|k|<1$ 时为双曲线，$|k|=1$ 时为两相交直线 $y=\pm 2x$，$|k|>1$ 时仍为双曲线（开口换向）。用 $x=k$ 截：$z^2-y^2=1-4k^2$，同为双曲线族。三类截面共同刻画单叶双曲面的"马鞍+束腰"形态。
**解法三（直纹性验证）** 构造两族直线（参数 $s$）：$\begin{cases}x=\dfrac{\cos\theta+s\sin\theta}{2}\\y=s\\z=\sin\theta-s\cos\theta\end{cases}$ 与 $\begin{cases}x=\dfrac{\cos\theta-s\sin\theta}{2}\\y=s\\z=\sin\theta+s\cos\theta\end{cases}$。代入验证：$4x^2+z^2-y^2=(\cos\theta\pm s\sin\theta)^2+(\sin\theta\mp s\cos\theta)^2-s^2=\cos^2\theta+\sin^2\theta\pm 2s\sin\theta\cos\theta\mp 2s\sin\theta\cos\theta+s^2(\sin^2\theta+\cos^2\theta)-s^2=1$，整条直线都落在曲面上。直母线族的存在是单叶双曲面的特征性质（双叶双曲面无此性质）。
**思路展开** 二次曲面分类的标准工具是"看标准型符号"，截面法给出几何直观，直纹性验证则展示单叶双曲面最独特的性质。动画可用水平截面 $y=k$ 扫描展示椭圆截面从小到大再变大的过程，并叠加一族直母线。
**解法一动画要点** - 标准型 $\dfrac{x^2}{1/4}+\dfrac{z^2}{1}-\dfrac{y^2}{1}=1$ 的符号标注 - 单叶双曲面束腰形态
**解法二动画要点** - 水平截面扫描与截面椭圆族 - 双曲线截面族（两族方向）
**解法三动画要点** - 参数化直线族沿曲面滑动 - 代入验证恒等式的过程

### eval-geom-008 解析几何 · 二次曲面分类
**题目** 判断二次曲面 $2x^2+y^2-z^2+4xy=1$ 的类型。
**答案** 双叶双曲面
**解法一（特征值法）** 二次项矩阵 $A=\begin{pmatrix}2&2&0\\2&1&0\\0&0&-1\end{pmatrix}$。$2\times 2$ 块 $\begin{pmatrix}2&2\\2&1\end{pmatrix}$ 的特征方程为 $(2-\lambda)(1-\lambda)-4=0$，即 $\lambda^2-3\lambda-2=0$，特征值 $\lambda_1=\dfrac{3+\sqrt{17}}{2}>0$、$\lambda_2=\dfrac{3-\sqrt{17}}{2}<0$；第三个特征值为 $-1<0$。正惯性指数 $1$、负惯性指数 $2$，对应双叶双曲面。
**解法二（配方法）** $2x^2+4xy+y^2=2(x+y)^2-y^2$，故曲面方程为 $2(x+y)^2-y^2-z^2=1$，正平方项 1 个、负平方项 2 个，为双叶双曲面。
**解法三（截面法）** 用 $z=0$ 截：$2x^2+4xy+y^2=1$，配方为 $2(x+y)^2-y^2=1$，是双曲线；用 $y=0$ 截：$2x^2-z^2=1$，是双曲线；用 $x+y=0$（即 $x=-y$）截：$-y^2-z^2=1$ 无实解——该平面与曲面不相交。三个截面说明曲面在 $z$ 方向与 $x+y$ 方向均为双曲型、且存在与曲面完全不相交的平面（双叶分离的特征）。
**思路展开** 配方与特征值分别给出"正交变换"与"合同变换"两条化为标准形的路线：特征值法的结果是标准形 $3.56\,u^2-0.56\,v^2-w^2=1$（主轴方向），配方法的结果是 $2u'^2-v'^2-z^2=1$（非正交但更简单）。截面法从图形出发印证符号差 $(1,2)$。动画可展示双叶双曲面被三个坐标平面截出的双曲线截面。
**解法一动画要点** - 特征值 $\dfrac{3\pm\sqrt{17}}{2}$ 与 $-1$ 的谱标注 - 正负惯性指数 $(1,2)$ 的标注
**解法二动画要点** - 配方 $2(x+y)^2-y^2-z^2=1$ 的逐步动画 - 双叶双曲面的三维渲染
**解法三动画要点** - 三个典型截面的双曲线 - $x+y=0$ 截面无实解的标注 - 与单叶双曲面（eval-geom-007）对照

### eval-geom-009 解析几何 · 曲面与曲线
**题目** 求椭球面 $\dfrac{x^2}{4}+\dfrac{y^2}{9}+z^2=1$ 与平面 $x=1$ 的交线方程，并说明其形状。
**答案** 椭圆：$\dfrac{y^2}{27/4}+\dfrac{z^2}{3/4}=1$（$x=1$），半轴 $\dfrac{3\sqrt{3}}{2}$ 与 $\dfrac{\sqrt{3}}{2}$
**解法一（代入法）** 将 $x=1$ 代入椭球面方程：$\dfrac{1}{4}+\dfrac{y^2}{9}+z^2=1$，即 $\dfrac{y^2}{9}+z^2=\dfrac{3}{4}$。化为标准形 $\dfrac{y^2}{9\cdot\frac{3}{4}}+\dfrac{z^2}{\frac{3}{4}}=1$，即 $\dfrac{y^2}{27/4}+\dfrac{z^2}{3/4}=1$。这是平面 $x=1$ 内的椭圆，半轴分别为 $\sqrt{\dfrac{27}{4}}=\dfrac{3\sqrt{3}}{2}$ 与 $\sqrt{\dfrac{3}{4}}=\dfrac{\sqrt{3}}{2}$，中心 $(1,0,0)$。
**解法二（参数化）** 由标准形直接参数化：$x=1$，$y=\dfrac{3\sqrt{3}}{2}\cos t$，$z=\dfrac{\sqrt{3}}{2}\sin t$，$t\in[0,2\pi]$。代回验证：$\dfrac{1}{4}+\dfrac{27\cos^2 t}{4\cdot 9}+\dfrac{3\sin^2 t}{4}=\dfrac{1}{4}+\dfrac{3}{4}(\cos^2 t+\sin^2 t)=1$。
**解法三（平行截面族）** 一般截面 $x=k$：$|k|<2$ 时为椭圆 $\dfrac{y^2}{9\left(1-\frac{k^2}{4}\right)}+\dfrac{z^2}{1-\frac{k^2}{4}}=1$，半轴 $3\sqrt{1-\dfrac{k^2}{4}}$ 与 $\sqrt{1-\dfrac{k^2}{4}}$（比值恒为 $3$，故所有截面椭圆相似）；$k=\pm 2$ 时 $1-\dfrac{k^2}{4}=0$，方程仅剩 $y=z=0$，截面退化为单点 $(\pm 2,0,0)$；$|k|>2$ 时无交点。取 $k=1$：半轴 $3\cdot\dfrac{\sqrt{3}}{2}=\dfrac{3\sqrt{3}}{2}$ 与 $\dfrac{\sqrt{3}}{2}$，与解法一一致。
**思路展开** 代入法最直接；参数化法为后续弧长、曲率计算铺路；截面族法揭示椭球面的生成机制（同心相似椭圆族随 $k$ 缩放）。动画可从 $x=-2$ 扫描到 $x=2$，展示截面椭圆从小到大再到小的连续变化。
**解法一动画要点** - 椭球面与截平面 $x=1$ 相交 - 代入后方程 $\dfrac{y^2}{27/4}+\dfrac{z^2}{3/4}=1$ 的化简
**解法二动画要点** - 参数点 $\left(1,\dfrac{3\sqrt3}{2}\cos t,\dfrac{\sqrt3}{2}\sin t\right)$ 沿椭圆运动 - 代回验证恒等式
**解法三动画要点** - 截面椭圆族扫描动画 - 半轴长度随 $k$ 变化的曲线与 $k=\pm2$ 退化点

### eval-geom-010 解析几何 · 曲面与曲线
**题目** 说明曲面 $z=xy$ 的类型，并验证它是直纹面。
**答案** 双曲抛物面（马鞍面），直纹面
**解法一（旋转化标准形）** 作正交变换 $u=\dfrac{x+y}{\sqrt{2}}$、$v=\dfrac{x-y}{\sqrt{2}}$，则 $x=\dfrac{u+v}{\sqrt{2}}$、$y=\dfrac{u-v}{\sqrt{2}}$，$xy=\dfrac{u^2-v^2}{2}$。曲面方程化为 $z=\dfrac{u^2}{2}-\dfrac{v^2}{2}$，即 $2z=u^2-v^2$，是双曲抛物面（马鞍面）。
**解法二（直母线族）** 固定 $y=c$：截面 $z=cx$ 是直线；固定 $x=c$：截面 $z=cy$ 也是直线。即曲面上存在两族平行于坐标平面的直线族 $\{z=cx,\ y=c\}$ 与 $\{z=cy,\ x=c\}$，故 $z=xy$ 是直纹面，且每一点处恰有两条直母线通过（交叉直线构成马鞍网格）。
**解法三（截面法）** 用 $y=k$ 截：$z=kx$，对任意 $k$ 都是直线（竖直截面均为直线，直纹性的又一体现）；用 $z=k$ 截：$xy=k$，等轴双曲线（$k\ne 0$）或两坐标轴（$k=0$）；若要抛物线截面，取斜截面 $x=y$（得 $z=x^2$）与 $x=-y$（得 $z=-x^2$）。直线截面与双曲线截面正是双曲抛物面的截面特征。
**思路展开** 双曲抛物面与单叶双曲面一样是直纹面，但直母线结构不同（这里两族直线都平行于坐标平面）。解法一的正交变换揭示"马鞍"的对称轴方向，解法二、三分别从直纹与截面两个角度刻画。动画可画马鞍面的网格状直母线，展示"负曲率点沿两条交叉直线方向"。
**解法一动画要点** - 马鞍面三维渲染与 $45^\circ$ 旋转变换 - $xy=\dfrac{u^2-v^2}{2}$ 的代入
**解法二动画要点** - 两族直母线 $z=cx$（$y=c$）与 $z=cy$（$x=c$）的网格动画
**解法三动画要点** - 竖直截面（直线族）与水平截面（等轴双曲线）扫描 - 斜截面 $x=\pm y$ 的抛物线

### eval-geom-011 解析几何 · 曲面与曲线
**题目** 求直线 $l:x=1+t,\ y=t,\ z=t$ 与球面 $x^2+y^2+z^2=4$ 的交点个数，并求出交点坐标。
**答案** 两个交点：$\left(\dfrac{2+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3}\right)$ 与 $\left(\dfrac{2-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3}\right)$
**解法一（判别式法）** 代入：$(1+t)^2+t^2+t^2=4$，即 $3t^2+2t-3=0$。判别式 $\Delta=4+36=40>0$，故有两个交点。解出 $t=\dfrac{-2\pm\sqrt{40}}{6}=\dfrac{-1\pm\sqrt{10}}{3}$，对应两点 $\left(1+t,t,t\right)$：$t_1=\dfrac{-1+\sqrt{10}}{3}$ 时 $\left(\dfrac{2+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3},\dfrac{-1+\sqrt{10}}{3}\right)$，$t_2=\dfrac{-1-\sqrt{10}}{3}$ 时 $\left(\dfrac{2-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3},\dfrac{-1-\sqrt{10}}{3}\right)$。
**解法二（距离法）** 球心 $O(0,0,0)$ 到直线距离：直线上取点 $P_0(1,0,0)$、方向 $\vec s=(1,1,1)$，$\overrightarrow{P_0O}=(-1,0,0)$，叉积 $\overrightarrow{P_0O}\times\vec s=(0\cdot 1-0\cdot 1,\ 0\cdot 1-(-1)\cdot 1,\ (-1)\cdot 1-0\cdot 1)=(0,1,-1)$，模 $\sqrt{2}$，故 $d=\dfrac{\sqrt{2}}{\sqrt{3}}=\sqrt{\dfrac{2}{3}}<2$，直线与球面相交于两点。相交弦长 $=2\sqrt{4-\dfrac{2}{3}}=2\sqrt{\dfrac{10}{3}}$，与解法一中两参数差对应的长度 $|t_1-t_2|\cdot|\vec s|=\dfrac{2\sqrt{10}}{3}\cdot\sqrt{3}=2\sqrt{\dfrac{10}{3}}$ 一致。
**解法三（配方直接求解）** $3t^2+2t-3=3\left(t+\dfrac{1}{3}\right)^2-\dfrac{10}{3}=0$，故 $t+\dfrac{1}{3}=\pm\dfrac{\sqrt{10}}{3}$，$t=\dfrac{-1\pm\sqrt{10}}{3}$，与解法一相同。
**思路展开** 判别式法给出交点个数与坐标，距离法先回答"几个交点"再给出弦长（几何量先行），配方法则展示二次方程的几何本质（对称轴与顶点）。动画可展示直线穿过球面，两个交点随视角旋转清晰可见。
**解法一动画要点** - 代入得 $3t^2+2t-3=0$ 的判别式动画 - 两交点高亮标注
**解法二动画要点** - 球心到直线的垂线段与距离 $\sqrt{\dfrac{2}{3}}$ - 相交弦长 $2\sqrt{\dfrac{10}{3}}$ 与两参数差的对照
**解法三动画要点** - 配方 $3\left(t+\dfrac{1}{3}\right)^2-\dfrac{10}{3}=0$ 的对称轴与顶点 - 球面与直线相交的三维视图

### eval-geom-012 解析几何 · 曲线
**题目** 求圆柱螺线 $x=a\cos t,\ y=a\sin t,\ z=bt$（$a,b>0$）的曲率与挠率。
**答案** 曲率 $\kappa=\dfrac{a}{a^2+b^2}$，挠率 $\tau=\dfrac{b}{a^2+b^2}$
**解法一（Frenet 公式直接计算）** 记 $c=\sqrt{a^2+b^2}$。$\vec r'=(-a\sin t,a\cos t,b)$，$|\vec r'|=c$；$\vec r''=(-a\cos t,-a\sin t,0)$；$\vec r'\times\vec r''=(ab\sin t,-ab\cos t,a^2)$，模 $\sqrt{a^2b^2+a^4}=ac$。曲率 $\kappa=\dfrac{|\vec r'\times\vec r''|}{|\vec r'|^3}=\dfrac{ac}{c^3}=\dfrac{a}{c^2}=\dfrac{a}{a^2+b^2}$。又 $\vec r'''=(a\sin t,-a\cos t,0)$，挠率 $\tau=\dfrac{(\vec r',\vec r'',\vec r''')}{|\vec r'\times\vec r''|^2}=\dfrac{a^2b\sin^2 t+a^2b\cos^2 t}{a^2c^2}=\dfrac{b}{c^2}=\dfrac{b}{a^2+b^2}$。
**解法二（物理分解）** 速度 $\vec v=\vec r'$，模 $|\vec v|=c$ 恒定，故切向加速度为 $0$；加速度 $\vec a=\vec r''=(-a\cos t,-a\sin t,0)$，模 $|\vec a|=a$。由 $|\vec a|=\kappa|\vec v|^2$ 得 $\kappa=\dfrac{a}{c^2}=\dfrac{a}{a^2+b^2}$。副法向量 $\vec B=\dfrac{\vec r'\times\vec r''}{|\vec r'\times\vec r''|}=\dfrac{1}{c}(b\sin t,-b\cos t,a)$，$\dfrac{d\vec B}{dt}=\dfrac{1}{c}(b\cos t,b\sin t,0)$，模 $\dfrac{b}{c}$。由 Frenet 公式 $\dfrac{d\vec B}{ds}=-\tau\vec N$ 核对方向（本题 $\dfrac{d\vec B}{ds}$ 与 $-\vec N$ 同向，故 $\tau>0$），且 $\left|\dfrac{d\vec B}{ds}\right|=\tau$、$\dfrac{ds}{dt}=c$，得 $\tau=\dfrac{b/c}{c}=\dfrac{b}{a^2+b^2}$。
**解法三（展开法）** 把圆柱面沿一条母线剪开展平，螺线变成一条直线，其与水平方向的夹角 $\alpha$ 满足 $\tan\alpha=\dfrac{b}{a}$（螺距 $2\pi b$ 与周长 $2\pi a$ 之比），故 $\cos^2\alpha=\dfrac{a^2}{a^2+b^2}$。螺线的曲率完全来自柱面弯曲：$\kappa=\dfrac{\cos^2\alpha}{a}=\dfrac{a}{a^2+b^2}$；挠率来自螺线"扭转"：$\tau=\dfrac{\sin\alpha\cos\alpha}{a}=\dfrac{b}{a^2+b^2}$。$\dfrac{\tau}{\kappa}=\dfrac{b}{a}$ 为常数，说明圆柱螺线是常曲率常挠率曲线。
**思路展开** 三种方法分别代表微分几何公式、力学分解、几何展开。展开法最具启发性：曲率与挠率分别由"柱面弯曲"与"螺旋扭转"贡献，$\kappa:\tau=a:b$ 的比值揭示了螺线的本质参数。动画可把圆柱面展开，展示螺线变成直线的瞬间。
**解法一动画要点** - 向量 $\vec r'\times\vec r''$ 与三阶混合积的计算标注 - 圆柱螺线与密切圆、副法线
**解法二动画要点** - 速度、加速度的分解动画 - 副法向量 $\vec B$ 的变化率标注
**解法三动画要点** - 圆柱展开成平面、螺线变直线 - 夹角 $\alpha$ 与 $\kappa:\tau=a:b$ 的标注

### eval-geom-013 解析几何 · 曲面与曲线
**题目** 求曲面 $z=x^2+y^2$ 在点 $(1,1,2)$ 处的切平面与法线方程。
**答案** 切平面 $2x+2y-z=2$；法线 $\dfrac{x-1}{-2}=\dfrac{y-1}{-2}=\dfrac{z-2}{1}$
**解法一（梯度法）** 令 $F(x,y,z)=z-x^2-y^2$，曲面为 $F=0$。$\nabla F=(-2x,-2y,1)$，在 $(1,1,2)$ 处为 $\vec n=(-2,-2,1)$。切平面：$-2(x-1)-2(y-1)+1\cdot(z-2)=0$，即 $2x+2y-z=2$。法线：$\dfrac{x-1}{-2}=\dfrac{y-1}{-2}=\dfrac{z-2}{1}$。
**解法二（全微分）** $dz=2x\,dx+2y\,dy$，在 $(1,1)$ 处 $dz=2dx+2dy$。切平面为 $z-2=2(x-1)+2(y-1)$，即 $2x+2y-z=2$。法线方向由 $(dx,dy,dz)$ 与 $(2,2,-1)$ 垂直得出：法向 $(2,2,-1)$，法线方程同上。
**解法三（参数化切向量）** 参数化 $\vec r(u,v)=(u,v,u^2+v^2)$。$\vec r_u=(1,0,2u)$，$\vec r_v=(0,1,2v)$，在 $(u,v)=(1,1)$ 处为 $(1,0,2)$、$(0,1,2)$。切平面法向量 $\vec r_u\times\vec r_v=(0\cdot 2-2\cdot 1,\ 2\cdot 0-1\cdot 2,\ 1\cdot 1-0\cdot 0)=(-2,-2,1)$，与解法一一致，切平面、法线同上。
**思路展开** 梯度法把曲面看成等值面，全微分法把 $z$ 看成函数，参数化法从曲面片出发——三种方法殊途同归，分别适用于隐式、显式、参数式三种曲面表示。动画可展示曲面上的切平面像"贴片"一样贴合，法线垂直于所有切方向。
**解法一动画要点** - 梯度 $\nabla F=(-2x,-2y,1)$ 在 $(1,1,2)$ 的取值 - 切平面方程标注
**解法二动画要点** - 全微分 $dz=2x\,dx+2y\,dy$ 的推导 - 切平面 $z-2=2(x-1)+2(y-1)$ 的贴合
**解法三动画要点** - 两条参数切向量 $\vec r_u=(1,0,2)$、$\vec r_v=(0,1,2)$ - 叉积得法向量 $(-2,-2,1)$

### eval-geom-014 解析几何 · 二次曲线
**题目** 求椭圆 $\dfrac{x^2}{4}+\dfrac{y^2}{9}=1$ 在点 $\left(\sqrt{2},\dfrac{3}{\sqrt{2}}\right)$ 处的切线方程。
**答案** $3x+2y=6\sqrt{2}$
**解法一（切线公式）** 椭圆上点 $(x_0,y_0)$ 处的切线为 $\dfrac{xx_0}{4}+\dfrac{yy_0}{9}=1$。代入 $\left(\sqrt{2},\dfrac{3}{\sqrt{2}}\right)$：$\dfrac{\sqrt{2}}{4}x+\dfrac{3}{9\sqrt{2}}y=1$，即 $\dfrac{\sqrt{2}}{4}x+\dfrac{1}{3\sqrt{2}}y=1$。两边乘 $12\sqrt{2}$：$6x+4y=12\sqrt{2}$，即 $3x+2y=6\sqrt{2}$。检验切点在切线上：$3\sqrt{2}+2\cdot\dfrac{3}{\sqrt{2}}=3\sqrt{2}+3\sqrt{2}=6\sqrt{2}$。
**解法二（隐函数求导）** 两边对 $x$ 求导：$\dfrac{2x}{4}+\dfrac{2y}{9}y'=0$，得 $y'=-\dfrac{9x}{4y}$。在 $\left(\sqrt{2},\dfrac{3}{\sqrt{2}}\right)$ 处 $y'=-\dfrac{9\sqrt{2}}{4\cdot\frac{3}{\sqrt{2}}}=-\dfrac{9\cdot 2}{12}=-\dfrac{3}{2}$。切线：$y-\dfrac{3}{\sqrt{2}}=-\dfrac{3}{2}(x-\sqrt{2})$，整理得 $2y-\dfrac{6}{\sqrt{2}}=-3x+3\sqrt{2}$，即 $3x+2y=3\sqrt{2}+3\sqrt{2}=6\sqrt{2}$。
**解法三（参数化求导）** 参数化 $x=2\cos t$、$y=3\sin t$。切点处 $\cos t=\dfrac{\sqrt{2}}{2}$、$\sin t=\dfrac{1}{\sqrt{2}}$，即 $t=\dfrac{\pi}{4}$。切线斜率 $\dfrac{dy}{dx}=\dfrac{3\cos t}{-2\sin t}$，在 $t=\dfrac{\pi}{4}$ 处为 $-\dfrac{3}{2}$。切线方程同解法二，即 $3x+2y=6\sqrt{2}$。
**思路展开** 切线公式是椭圆标准式的最快路径，隐函数求导是通用方法，参数化把曲线几何转化为三角函数。动画可展示切线与椭圆在切点处的"一阶接触"，并让切点沿椭圆滑动、切线随之变化。
**解法一动画要点** - 切线公式 $\dfrac{xx_0}{4}+\dfrac{yy_0}{9}=1$ 的代入 - 椭圆与切线在切点的一阶接触
**解法二动画要点** - 隐函数求导 $y'=-\dfrac{9x}{4y}$ 的过程 - 斜率 $-\dfrac{3}{2}$ 的标注
**解法三动画要点** - 参数化 $x=2\cos t$、$y=3\sin t$ 在 $t=\dfrac{\pi}{4}$ 处 - 切点沿椭圆滑动的切线族

### eval-geom-015 解析几何 · 曲面与曲线
**题目** 求两球面 $x^2+y^2+z^2=4$ 与 $x^2+(y-1)^2+z^2=4$ 的交线方程。
**答案** 圆：$y=\dfrac{1}{2}$，$x^2+z^2=\dfrac{15}{4}$（圆心 $\left(0,\dfrac{1}{2},0\right)$，半径 $\dfrac{\sqrt{15}}{2}$）
**解法一（两式相减）** 两方程相减：$x^2+y^2+z^2-\left[x^2+(y-1)^2+z^2\right]=0$，即 $y^2-(y^2-2y+1)=0$，得 $2y-1=0$，$y=\dfrac{1}{2}$。代入第一式：$x^2+z^2=4-\dfrac{1}{4}=\dfrac{15}{4}$。交线为平面 $y=\dfrac{1}{2}$ 上的圆 $x^2+z^2=\dfrac{15}{4}$。
**解法二（平面截球）** 两球半径相等（均为 $2$），故交线圆所在平面是两球心连线的垂直平分面。球心 $O_1(0,0,0)$、$O_2(0,1,0)$，垂直平分面为 $y=\dfrac{1}{2}$。球心 $O_1$ 到该平面的距离为 $\dfrac{1}{2}$，故截面圆半径 $\sqrt{2^2-\left(\dfrac{1}{2}\right)^2}=\dfrac{\sqrt{15}}{2}$，圆心 $\left(0,\dfrac{1}{2},0\right)$。
**解法三（参数化）** 由圆方程直接参数化：$x=\dfrac{\sqrt{15}}{2}\cos t$，$y=\dfrac{1}{2}$，$z=\dfrac{\sqrt{15}}{2}\sin t$，$t\in[0,2\pi]$。代回两球面验证：$x^2+y^2+z^2=\dfrac{15}{4}+\dfrac{1}{4}=4$；$x^2+(y-1)^2+z^2=\dfrac{15}{4}+\dfrac{1}{4}=4$。
**思路展开** 相减法把两个二次方程化为"平面+圆"两个一次结构，是求两曲面交线的基本操作；垂直平分面视角说明等半径两球交线圆的对称性；参数化则为后续线积分服务。动画可展示两球面相交、交线圆与所在平面。
**解法一动画要点** - 两式相减得 $y=\dfrac{1}{2}$ 的消元动画 - 代入得圆 $x^2+z^2=\dfrac{15}{4}$
**解法二动画要点** - 两相交球面的三维视图 - 球心连线的垂直平分面与截面圆
**解法三动画要点** - 参数点沿交线圆运动 - 代回两球面验证恒等式

### eval-geom-016 解析几何 · 向量
**题目** 已知 $|\vec a|=2$，$|\vec b|=3$，$\vec a$ 与 $\vec b$ 的夹角为 $60^\circ$，求 $|\vec a+\vec b|$、$|2\vec a-\vec b|$ 及 $\vec a+\vec b$ 与 $\vec a-\vec b$ 的夹角余弦。
**答案** $|\vec a+\vec b|=\sqrt{19}$，$|2\vec a-\vec b|=\sqrt{13}$，$\cos\theta=-\dfrac{5}{\sqrt{133}}$
**解法一（模长公式）** $|\vec a+\vec b|^2=|\vec a|^2+|\vec b|^2+2|\vec a||\vec b|\cos 60^\circ=4+9+2\cdot 2\cdot 3\cdot\dfrac{1}{2}=19$，故 $|\vec a+\vec b|=\sqrt{19}$。$|2\vec a-\vec b|^2=4|\vec a|^2+|\vec b|^2-4|\vec a||\vec b|\cos 60^\circ=16+9-12=13$，故 $|2\vec a-\vec b|=\sqrt{13}$。又 $(\vec a+\vec b)\cdot(\vec a-\vec b)=|\vec a|^2-|\vec b|^2=4-9=-5$，$|\vec a-\vec b|^2=4+9-2\cdot 2\cdot 3\cdot\dfrac{1}{2}=7$，故 $\cos\theta=\dfrac{-5}{\sqrt{19}\cdot\sqrt{7}}=-\dfrac{5}{\sqrt{133}}$。
**解法二（坐标法）** 取 $\vec a=(2,0)$，$\vec b=\left(\dfrac{3}{2},\dfrac{3\sqrt{3}}{2}\right)$。则 $\vec a+\vec b=\left(\dfrac{7}{2},\dfrac{3\sqrt{3}}{2}\right)$，$|\vec a+\vec b|^2=\dfrac{49}{4}+\dfrac{27}{4}=19$；$2\vec a-\vec b=\left(\dfrac{5}{2},-\dfrac{3\sqrt{3}}{2}\right)$，模平方 $\dfrac{25}{4}+\dfrac{27}{4}=13$；$\vec a-\vec b=\left(\dfrac{1}{2},-\dfrac{3\sqrt{3}}{2}\right)$，$(\vec a+\vec b)\cdot(\vec a-\vec b)=\dfrac{7}{4}-\dfrac{27}{4}=-5$，与解法一一致。
**解法三（几何法）** 以 $\vec a,\vec b$ 为邻边作平行四边形，对角线长为 $|\vec a+\vec b|$ 与 $|\vec a-\vec b|$。由余弦定理：$|\vec a+\vec b|^2=2^2+3^2-2\cdot 2\cdot 3\cos 120^\circ=19$（补角 $120^\circ$），$|\vec a-\vec b|^2=2^2+3^2-2\cdot 2\cdot 3\cos 60^\circ=7$。$2\vec a-\vec b$ 可用三角形法则：以 $2\vec a$ 与 $-\vec b$ 为边，$|2\vec a-\vec b|^2=16+9-2\cdot 4\cdot 3\cdot\dfrac{1}{2}=13$。夹角余弦由点积公式同解法一。
**思路展开** 模长公式、坐标法、几何法是向量计算的三件套：模长公式适合抽象计算，坐标法适合具体数值，几何法（平行四边形、三角形法则）给出图形直觉。动画可画平行四边形对角线随夹角变化的动态过程。
**解法一动画要点** - 模长平方公式的逐项展开 - 点积恒等式 $(\vec a+\vec b)\cdot(\vec a-\vec b)=|\vec a|^2-|\vec b|^2$ 的标注
**解法二动画要点** - 坐标化 $\vec a=(2,0)$、$\vec b=\left(\dfrac{3}{2},\dfrac{3\sqrt3}{2}\right)$ 的分量计算 - 各向量坐标标注
**解法三动画要点** - 平行四边形与两对角线 - 三角形法则拼接 $2\vec a$ 与 $-\vec b$ - 余弦定理补角 $120^\circ$ 的标注

### eval-geom-017 解析几何 · 向量
**题目** 已知 $\vec a=(1,2,2)$，$\vec b=(-2,1,2)$，求 $\vec a$ 与 $\vec b$ 的夹角余弦及 $\vec a$ 在 $\vec b$ 上的投影向量。
**答案** $\cos\theta=\dfrac{4}{9}$；投影向量 $\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)$
**解法一（点积公式）** $\vec a\cdot\vec b=1\cdot(-2)+2\cdot 1+2\cdot 2=4$，$|\vec a|=\sqrt{1+4+4}=3$，$|\vec b|=\sqrt{4+1+4}=3$，故 $\cos\theta=\dfrac{4}{3\cdot 3}=\dfrac{4}{9}$。投影向量 $\mathrm{proj}_{\vec b}\vec a=\dfrac{\vec a\cdot\vec b}{|\vec b|^2}\vec b=\dfrac{4}{9}(-2,1,2)=\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)$。
**解法二（投影几何）** 投影长度 $|\vec a|\cos\theta=3\cdot\dfrac{4}{9}=\dfrac{4}{3}$，方向为 $\dfrac{\vec b}{|\vec b|}=\dfrac{1}{3}(-2,1,2)$，故投影向量 $=\dfrac{4}{3}\cdot\dfrac{1}{3}(-2,1,2)=\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)$。
**解法三（正交分解验证）** 取单位向量 $\vec u=\dfrac{\vec b}{3}=\left(-\dfrac{2}{3},\dfrac{1}{3},\dfrac{2}{3}\right)$，则 $\vec a=\left(\vec a\cdot\vec u\right)\vec u+\vec a_\perp$，其中 $\vec a\cdot\vec u=\dfrac{4}{3}$，$\vec a_\perp=\vec a-\dfrac{4}{3}\vec u=(1,2,2)-\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)=\left(\dfrac{17}{9},\dfrac{14}{9},\dfrac{10}{9}\right)$。验证 $\vec a_\perp\cdot\vec b=\dfrac{17}{9}\cdot(-2)+\dfrac{14}{9}\cdot 1+\dfrac{10}{9}\cdot 2=\dfrac{-34+14+20}{9}=0$，正交分解成立，投影分量即 $\left(-\dfrac{8}{9},\dfrac{4}{9},\dfrac{8}{9}\right)$。
**思路展开** 投影向量的三种算法：点积公式（一步到位）、几何法（长度×单位方向）、正交分解（Gram-Schmidt 思想，验证 $a-a_\parallel\perp b$）。动画可展示 $a$ 分解为平行与垂直于 $b$ 的两个分量。
**解法一动画要点** - 点积 $\vec a\cdot\vec b=4$ 与模长 $3,3$ 的标注 - 夹角余弦 $\dfrac{4}{9}$
**解法二动画要点** - 投影长度 $\dfrac{4}{3}$ 与单位方向 $\dfrac{\vec b}{3}$ 的乘积 - 三维向量与夹角
**解法三动画要点** - $a$ 分解为平行/垂直分量 - 正交性验证 $\vec a_\perp\cdot\vec b=0$

### eval-geom-018 解析几何 · 向量
**题目** 求以 $O(0,0,0)$、$A(2,0,0)$、$B(0,3,0)$、$C(0,0,4)$ 为顶点的四面体体积。
**答案** $4$
**解法一（混合积）** $V=\dfrac{1}{6}\left|\det(\overrightarrow{OA},\overrightarrow{OB},\overrightarrow{OC})\right|=\dfrac{1}{6}\left|\begin{vmatrix}2&0&0\\0&3&0\\0&0&4\end{vmatrix}\right|=\dfrac{24}{6}=4$。
**解法二（底面积×高）** 取底面 $OAB$：面积 $S=\dfrac{1}{2}\cdot 2\cdot 3=3$。顶点 $C$ 到平面 $xOy$ 的距离即高 $h=4$。故 $V=\dfrac{1}{3}Sh=\dfrac{1}{3}\cdot 3\cdot 4=4$。
**解法三（三重积分）** 四面体区域为 $\dfrac{x}{2}+\dfrac{y}{3}+\dfrac{z}{4}\le 1$、$x,y,z\ge 0$。作线性替换 $u=\dfrac{x}{2}$、$v=\dfrac{y}{3}$、$w=\dfrac{z}{4}$（雅可比行列式 $\dfrac{\partial(x,y,z)}{\partial(u,v,w)}=2\cdot 3\cdot 4=24$），区域变为 $u+v+w\le 1$、$u,v,w\ge 0$。$V=\displaystyle\iiint dx\,dy\,dz=24\iiint du\,dv\,dw=24\cdot\dfrac{1}{6}=4$（单位单纯形 $u+v+w\le 1,\ u,v,w\ge 0$ 的体积为 $\dfrac{1}{6}$）。
**思路展开** 混合积是体积的代数表示（其绝对值=平行六面体体积），底×高是几何定义，三重积分把四面体区域化成标准单纯形（$V_{\text{simplex}}=\dfrac{1}{6}V_{\text{cube}}$，即单纯形体积为立方体体积的 $\dfrac{1}{6}$——这就是系数 $\dfrac{1}{6}$ 的来源）。动画可展示线性替换把斜四面体"拉正"为标准单纯形的过程。
**解法一动画要点** - 混合积行列式 $\begin{vmatrix}2&0&0\\0&3&0\\0&0&4\end{vmatrix}=24$ 的计算 - 四面体与对应平行六面体
**解法二动画要点** - 底面积 $\dfrac{1}{2}\cdot2\cdot3=3$ 与高 4 的标注 - 体积 $\dfrac{1}{3}Sh=4$
**解法三动画要点** - 线性替换 $u=\dfrac{x}{2}$ 等拉正为标准单纯形 - 雅可比 $24$ 与单纯形体积 $\dfrac{1}{6}$ 的标注

### eval-geom-019 解析几何 · 直线与平面
**题目** 求两平面 $\pi_1:x+y+z=1$ 与 $\pi_2:x+2y+3z=6$ 的交线方程。
**答案** $\dfrac{x+4}{1}=\dfrac{y-5}{-2}=\dfrac{z}{1}$，即 $(x,y,z)=(-4+t,5-2t,t)$
**解法一（法向量叉积）** 方向向量 $\vec s=\vec{n_1}\times\vec{n_2}=(1,1,1)\times(1,2,3)=(1\cdot 3-1\cdot 2,\ 1\cdot 1-1\cdot 3,\ 1\cdot 2-1\cdot 1)=(1,-2,1)$。求交线上一点：令 $z=0$，解 $\begin{cases}x+y=1\\x+2y=6\end{cases}$，两式相减得 $y=5$、$x=-4$，得点 $P_0(-4,5,0)$。交线为 $\dfrac{x+4}{1}=\dfrac{y-5}{-2}=\dfrac{z}{1}$。
**解法二（高斯消元）** 方程组 $\begin{cases}x+y+z=1\\x+2y+3z=6\end{cases}$。第二式减第一式：$y+2z=5$，即 $y=5-2z$；代回第一式：$x+5-2z+z=1$，$x=z-4$。令 $z=t$，得参数方程 $(x,y,z)=(t-4,5-2t,t)=(-4+t,5-2t,t)$。
**解法三（参数化验证）** 由解法一/二得 $(x,y,z)=(-4+t,5-2t,t)$。代入 $\pi_1$：$(-4+t)+(5-2t)+t=1$；代入 $\pi_2$：$(-4+t)+2(5-2t)+3t=-4+t+10-4t+3t=6$。两式恒成立，故确为交线。
**思路展开** 叉积法给出交线的标准式，消元法给出参数式，两种形式互相转化（方向向量与点）。动画可展示两平面相交、交线方向向量与两法向量都垂直。
**解法一动画要点** - 叉积 $\vec s=(1,-2,1)$ 的方向动画 - 点 $P_0(-4,5,0)$ 的定位
**解法二动画要点** - 高斯消元得 $y=5-2z$、$x=z-4$ 的步骤 - 参数方程 $(t-4,5-2t,t)$ 的生成
**解法三动画要点** - 参数点沿交线运动 - 代回两平面恒成立的验证

### eval-geom-020 解析几何 · 向量
**题目** 判断四点 $A(1,2,3)$、$B(2,3,4)$、$C(3,5,7)$、$D(2,4,6)$ 是否共面。
**答案** 共面
**解法一（混合积为零）** $\overrightarrow{AB}=(1,1,1)$，$\overrightarrow{AC}=(2,3,4)$，$\overrightarrow{AD}=(1,2,3)$。混合积 $\det(\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD})=\begin{vmatrix}1&1&1\\2&3&4\\1&2&3\end{vmatrix}=1\cdot(9-8)-1\cdot(6-4)+1\cdot(4-3)=1-2+1=0$，故四点共面。
**解法二（平面方程检验）** 过 $A,B,C$ 的平面法向量 $\vec n=\overrightarrow{AB}\times\overrightarrow{AC}=(1,1,1)\times(2,3,4)=(1\cdot 4-1\cdot 3,\ 1\cdot 2-1\cdot 4,\ 1\cdot 3-1\cdot 2)=(1,-2,1)$。平面方程：$(x-1)-2(y-2)+(z-3)=0$，即 $x-2y+z=0$。代入 $D(2,4,6)$：$2-8+6=0$，满足方程，故 $D$ 在平面 $ABC$ 上，四点共面。
**解法三（向量组线性相关）** 检查 $\overrightarrow{AB},\overrightarrow{AC},\overrightarrow{AD}$ 是否线性相关。设 $k_1(1,1,1)+k_2(2,3,4)+k_3(1,2,3)=(0,0,0)$，即 $\begin{cases}k_1+2k_2+k_3=0\\k_1+3k_2+2k_3=0\\k_1+4k_2+3k_3=0\end{cases}$。第二式减第一式、第三式减第二式均得 $k_2+k_3=0$，取 $k_2=1$、$k_3=-1$，则 $k_1=-1$。验证 $-(1,1,1)+(2,3,4)-(1,2,3)=(0,0,0)$，存在非零解，故三向量线性相关，四点共面。
**思路展开** 四点共面的三种判据：混合积为零（代数判据）、平面方程检验（几何判据）、向量组线性相关（线性代数判据）。三者本质相同，入口不同。动画可展示四点在同一平面上的三维视图与混合积平行六面体"压扁"的过程。
**解法一动画要点** - 混合积行列式 $\begin{vmatrix}1&1&1\\2&3&4\\1&2&3\end{vmatrix}=0$ 的计算 - 平行六面体体积为零的动画
**解法二动画要点** - 平面方程 $x-2y+z=0$ 的建立 - 代入 $D(2,4,6)$ 验证 $2-8+6=0$
**解法三动画要点** - 三个向量的线性组合 $-(1,1,1)+(2,3,4)-(1,2,3)=(0,0,0)$ 回到原点 - 四点与所在平面

# 三、概率论（15 题）

### eval-prob-001 概率论 · 条件概率
**题目** 三门问题：参赛者在三扇门中选择一扇（其中一扇后有汽车，另两扇后是山羊）。主持人（知道车在哪）打开另一扇有山羊的门，给参赛者一次换门机会。问换门获胜的概率是多少？并解释原因。
**答案** 换门获胜概率为 $\dfrac{2}{3}$，不换为 $\dfrac{1}{3}$
**解法一（树状图/直接分析）** 参赛者初始选中山羊的概率为 $\dfrac{2}{3}$，此时主持人必须打开另一扇山羊门（他不能开车门），剩下的未开门必然是汽车，换门必赢。初始选中汽车的概率为 $\dfrac{1}{3}$，此时换门必输。故换门获胜概率 $=\dfrac{2}{3}\times 1+\dfrac{1}{3}\times 0=\dfrac{2}{3}$。
**解法二（贝叶斯公式）** 设参赛者选 1 号门、主持人打开 2 号门，并假设主持人在有两扇羊门可选时等概率选择（其余情形由对称性同理）。记 $C_i$=车在 $i$ 号门，$H_2$=主持人开 2 号门。则 $P(H_2|C_3)=1$（车在 3 号门时主持人只能开 2 号门），$P(H_2|C_1)=\dfrac{1}{2}$（车在 1 号门时主持人可在 2、3 号门中等概率选择），$P(H_2|C_2)=0$（主持人不能开有车的门），$P(C_i)=\dfrac{1}{3}$。由贝叶斯公式：$P(C_3|H_2)=\dfrac{P(H_2|C_3)P(C_3)}{P(H_2|C_3)P(C_3)+P(H_2|C_1)P(C_1)+P(H_2|C_2)P(C_2)}=\dfrac{1\cdot\frac{1}{3}}{1\cdot\frac{1}{3}+\frac{1}{2}\cdot\frac{1}{3}+0}=\dfrac{1/3}{1/2}=\dfrac{2}{3}$。即主持人开 2 号门后，车在 3 号门（换门目标）的概率为 $\dfrac{2}{3}$。注意"总是换门"的获胜率 $\dfrac{2}{3}$ 其实不依赖主持人的等概率规则（见解法一）。
**解法三（枚举等可能样本点）** 车的位置（3 种）×参赛者初选（3 种）=9 种等可能情形。逐项枚举：参赛者初选=车门（3 种情形），换门必输；参赛者初选=山羊门（6 种情形），换门必赢。故换门获胜概率 $=\dfrac{6}{9}=\dfrac{2}{3}$。
**思路展开** 本题的核心是"主持人的行为携带信息"：他永远开山羊门，这一选择把 $\dfrac{2}{3}$ 的概率质量集中到未开的另一扇门上。解法一从信息角度直击本质，解法二是严格的贝叶斯形式化，解法三用枚举消除直觉误区。动画可用三扇门 + 概率条带的流动展示"主持人开门的条件作用"。
**解法一动画要点** - 三扇门与车、羊的随机放置 - 初选山羊（概率 $\dfrac{2}{3}$）与换门必赢的对应标注
**解法二动画要点** - 贝叶斯分母三项的条带分解 - 条件概率 $P(C_3|H_2)$ 的收缩动画
**解法三动画要点** - 9 种等可能情形的枚举表格 - 换门胜 6 格的计数高亮

### eval-prob-002 概率论 · 条件概率
**题目** 三个盒子：甲盒装 2 枚金币，乙盒装 2 枚银币，丙盒装 1 金 1 银。随机选一个盒子再从中随机摸出一枚硬币，发现是金币。问：该盒子中另一枚硬币也是金币的概率是多少？
**答案** $\dfrac{2}{3}$
**解法一（贝叶斯公式）** 记 $A$=摸到金币，$B_1,B_2,B_3$=分别选中甲盒（双金）、乙盒（双银）、丙盒（一金一银）。$P(B_i)=\dfrac{1}{3}$，$P(A|B_1)=1$，$P(A|B_2)=0$，$P(A|B_3)=\dfrac{1}{2}$。$P(B_1|A)=\dfrac{P(A|B_1)P(B_1)}{P(A|B_1)P(B_1)+P(A|B_2)P(B_2)+P(A|B_3)P(B_3)}=\dfrac{1\cdot\frac{1}{3}}{1\cdot\frac{1}{3}+0\cdot\frac{1}{3}+\frac{1}{2}\cdot\frac{1}{3}}=\dfrac{1/3}{1/2}=\dfrac{2}{3}$。
**解法二（枚举等可能样本点）** 6 枚硬币等可能地被摸到。已知摸到的是金币，则它必是 3 枚金币之一，且 3 枚金币等可能。其中 2 枚来自甲盒（另一枚也是金），1 枚来自丙盒（另一枚是银）。故所求概率 $=\dfrac{2}{3}$。
**解法三（树状图）** 第一层：选盒，各 $\dfrac{1}{3}$；第二层：甲盒内摸到金概率 1（路径概率 $\dfrac{1}{3}$），丙盒内摸到金概率 $\dfrac{1}{2}$（路径概率 $\dfrac{1}{6}$），乙盒为 0。摸到金的总概率 $\dfrac{1}{3}+\dfrac{1}{6}=\dfrac{1}{2}$；其中来自甲盒的占比 $\dfrac{1/3}{1/2}=\dfrac{2}{3}$。
**思路展开** 本题与 eval-prob-001 同属"条件概率反直觉"家族：直觉上"摸到金后盒内另一枚是金"看似 $\dfrac{1}{2}$，实为 $\dfrac{2}{3}$——因为双金盒"贡献金币"的能力是混盒的两倍。枚举法（解法二）把连续条件化归结为"3 枚金币等可能"，是最简明的解释。动画可画三盒六币，把摸到银币的分支"熄灭"，在剩余金币上重新归一化。
**解法一动画要点** - 贝叶斯公式分子分母的条带分解 - $P(A|B_i)$ 三值的标注
**解法二动画要点** - 三盒六币的枚举展示 - 3 枚金币等可能的归一化动画
**解法三动画要点** - 三盒六币的树状图 - 银币分支熄灭、金币重新归一化

### eval-prob-003 概率论 · 常见分布
**题目** 抛一枚均匀硬币直到出现正面为止，求抛掷次数的期望（几何分布期望）。
**答案** $2$
**解法一（级数求和）** 设 $X\sim\operatorname{Geom}\!\left(\dfrac{1}{2}\right)$，$P(X=n)=q^{n-1}p=\left(\dfrac{1}{2}\right)^n$。$E[X]=\displaystyle\sum_{n=1}^{\infty}n\left(\dfrac{1}{2}\right)^n$。由 eval-calc-021 的错位相减（或幂级数 $\sum nx^{n-1}=\dfrac{1}{(1-x)^2}$ 取 $x=\dfrac{1}{2}$），得 $E[X]=\dfrac{1/2}{(1-1/2)^2}=2$。
**解法二（无记忆性递推）** 记 $E$ 为首次正面所需次数的期望。第一次若为正面（概率 $\dfrac{1}{2}$），总次数为 1；若为反面（概率 $\dfrac{1}{2}$），则"回到原点"，总次数为 $1+E$。故 $E=\dfrac{1}{2}\cdot 1+\dfrac{1}{2}\cdot(1+E)=1+\dfrac{E}{2}$，解得 $E=2$。
**解法三（概率母函数）** 概率母函数 $G(z)=E[z^X]=\displaystyle\sum_{n=1}^{\infty}z^nq^{n-1}p=\dfrac{pz}{1-qz}$。$G'(z)=\dfrac{p(1-qz)+pqz}{(1-qz)^2}=\dfrac{p}{(1-qz)^2}$，故 $E[X]=G'(1)=\dfrac{p}{(1-q)^2}=\dfrac{1}{p}=2$（$p=q=\dfrac{1}{2}$）。
**思路展开** 本题与 eval-calc-021 是同一级数在概率语境的现身：解法一就是那个级数求和，解法二利用几何分布的无记忆性建立自指方程（最优雅），解法三用母函数把分布信息打包成生成函数。动画可展示"抛到反面就重来"的树状结构与期望的自指方程。
**解法一动画要点** - 错位相减竖式逐行对齐 - 与级数 $\sum n/2^n$ 的同构对照
**解法二动画要点** - 抛硬币树状图与"回到原点"分支 - 期望自指方程 $E=1+\dfrac{E}{2}$ 的天平示意
**解法三动画要点** - 母函数 $G(z)=\dfrac{pz}{1-qz}$ 的曲线 - $G'(1)$ 切线斜率的标注

### eval-prob-004 概率论 · 条件分布
**题目** 掷一枚均匀骰子两次，设 $X$ 为第一次点数，$Y$ 为两次点数之和。求 $P(Y\ge 8\mid X=3)$ 与 $E[Y\mid X=3]$。
**答案** $P(Y\ge 8\mid X=3)=\dfrac{1}{3}$；$E[Y\mid X=3]=\dfrac{13}{2}$
**解法一（条件分布表）** 给定 $X=3$，第二次点数 $Z$ 在 $\{1,2,3,4,5,6\}$ 上等可能。$Y=3+Z\ge 8\iff Z\ge 5$，故 $P(Y\ge 8|X=3)=P(Z\in\{5,6\})=\dfrac{2}{6}=\dfrac{1}{3}$。$E[Y|X=3]=3+E[Z]=3+\dfrac{7}{2}=\dfrac{13}{2}$。
**解法二（条件概率公式）** $P(Y\ge 8|X=3)=\dfrac{P(X=3,Y\ge 8)}{P(X=3)}$。$P(X=3)=\dfrac{1}{6}$；事件 $\{X=3,Y\ge 8\}$ 即 $\{X=3,Z\ge 5\}$，由独立性 $P=\dfrac{1}{6}\cdot\dfrac{2}{6}=\dfrac{1}{18}$。故条件概率 $=\dfrac{1/18}{1/6}=\dfrac{1}{3}$。同理 $E[Y|X=3]=\dfrac{1}{P(X=3)}\displaystyle\sum_z(3+z)P(X=3)P(Z=z)=\sum_z(3+z)\cdot\dfrac{1}{6}=\dfrac{13}{2}$。
**解法三（树状图）** 第一层固定 $X=3$，第二层 $Z\in\{1,\dots,6\}$ 各 $\dfrac{1}{6}$。数出 $Z\ge 5$ 的分支两条，概率 $\dfrac{2}{6}$；所有分支的 $Y$ 值平均为 $\dfrac{4+5+6+7+8+9}{6}=\dfrac{39}{6}=\dfrac{13}{2}$。
**思路展开** 条件分布表的要点是"条件化后样本空间收缩为 $\{Z=1,\dots,6\}$"。三种解法分别从分布表、公式、树图入手，展示条件期望的两种算法（定义式与独立性拆分）。动画可固定第一次骰子为 3 点，高亮第二次的 6 种等可能结果。
**解法一动画要点** - 条件分布表（$Z\in\{1,\dots,6\}$ 等可能） - $Z\ge5$ 的两格高亮
**解法二动画要点** - 条件概率公式 $\dfrac{P(X=3,Y\ge8)}{P(X=3)}$ 的代入 - 独立性拆分的标注
**解法三动画要点** - 两次掷骰的树状图 - 给定 $X=3$ 后第二层高亮与六值平均

### eval-prob-005 概率论 · 随机变量函数的分布
**题目** 设 $X\sim U(0,1)$（区间 $(0,1)$ 上的均匀分布），求 $Y=-\ln X$ 的分布。
**答案** $Y\sim\operatorname{Exp}(1)$，密度 $f_Y(y)=e^{-y}$（$y>0$）
**解法一（分布函数法）** $F_Y(y)=P(Y\le y)=P(-\ln X\le y)=P(X\ge e^{-y})=1-e^{-y}$（$y>0$，用到 $X$ 的分布函数 $F_X(x)=x$ 于 $(0,1)$）。对 $y$ 求导：$f_Y(y)=e^{-y}$（$y>0$），即 $Y\sim\operatorname{Exp}(1)$。
**解法二（密度变换公式）** $y=g(x)=-\ln x$ 在 $(0,1)$ 上严格递减，反函数 $x=h(y)=e^{-y}$（$y>0$），$|h'(y)|=e^{-y}$。由变换公式 $f_Y(y)=f_X(h(y))\cdot|h'(y)|=1\cdot e^{-y}=e^{-y}$（$y>0$）。
**解法三（逆变换采样原理）** 指数分布 $\operatorname{Exp}(1)$ 的分布函数为 $F(y)=1-e^{-y}$，其反函数 $F^{-1}(u)=-\ln(1-u)$。由于 $1-X$ 与 $X$ 同分布，$-\ln X$ 与 $F^{-1}(X)$ 同分布，故 $Y\sim\operatorname{Exp}(1)$。这正是计算机生成指数随机数的标准方法（逆变换法）。
**思路展开** 分布函数法是"万能法"（对所有单调/非单调变换都可用），密度变换公式适用于严格单调情形，解法三揭示本题是逆变换采样的原理原型——概率与算法在此交汇。动画可展示 $(0,1)$ 上的均匀点被 $-\ln$ 压到 $(0,\infty)$ 上、密度随之拉伸的过程。
**解法一动画要点** - 事件 $\{X\ge e^{-y}\}$ 的区间高亮 - 分布函数 $F_Y(y)=1-e^{-y}$ 的生成
**解法二动画要点** - $y=-\ln x$ 曲线与映射动画 - 反函数 $e^{-y}$ 与导数的密度变换
**解法三动画要点** - 均匀点列映射到正半轴 - 逆变换采样原理的示意

### eval-prob-006 概率论 · 数字特征
**题目** 设 $X\sim\operatorname{Poisson}(\lambda)$，求 $E[X^2]$，并由此求 $\operatorname{Var}(X)$。
**答案** $E[X^2]=\lambda^2+\lambda$，$\operatorname{Var}(X)=\lambda$
**解法一（定义级数求和）** $E[X^2]=\displaystyle\sum_{k=0}^{\infty}k^2\cdot\dfrac{\lambda^ke^{-\lambda}}{k!}=\sum_{k=0}^{\infty}\left[k(k-1)+k\right]\dfrac{\lambda^ke^{-\lambda}}{k!}=e^{-\lambda}\left[\lambda^2\sum_{k=2}^{\infty}\dfrac{\lambda^{k-2}}{(k-2)!}+\lambda\sum_{k=1}^{\infty}\dfrac{\lambda^{k-1}}{(k-1)!}\right]=e^{-\lambda}\left[\lambda^2e^{\lambda}+\lambda e^{\lambda}\right]=\lambda^2+\lambda$。故 $\operatorname{Var}(X)=E[X^2]-(E[X])^2=\lambda^2+\lambda-\lambda^2=\lambda$。
**解法二（阶乘矩）** $E[X(X-1)]=\displaystyle\sum_{k=2}^{\infty}k(k-1)\dfrac{\lambda^ke^{-\lambda}}{k!}=e^{-\lambda}\lambda^2\sum_{k=2}^{\infty}\dfrac{\lambda^{k-2}}{(k-2)!}=\lambda^2$。故 $E[X^2]=E[X(X-1)]+E[X]=\lambda^2+\lambda$，$\operatorname{Var}(X)=\lambda$。
**解法三（矩母函数）** $M(t)=E[e^{tX}]=e^{\lambda(e^t-1)}$。$M'(t)=M(t)\cdot\lambda e^t$，$M''(t)=M(t)\left[(\lambda e^t)^2+\lambda e^t\right]$。$E[X]=M'(0)=\lambda$，$E[X^2]=M''(0)=\lambda^2+\lambda$，$\operatorname{Var}(X)=M''(0)-[M'(0)]^2=\lambda$。
**思路展开** 三种算法对应处理离散分布二阶矩的三件工具：定义级数（通法）、阶乘矩（泊松分布专属技巧，利用 $\dfrac{1}{k!}$ 与 $\lambda^k$ 的匹配）、矩母函数（一阶导数出均值、二阶出二阶矩）。泊松分布"均值=方差=$\lambda$"是其标志性特征。动画可展示 $\lambda$ 滑块下泊松柱状图与方差同步变化。
**解法一动画要点** - $k^2=k(k-1)+k$ 的拆项动画 - 两级数 $e^\lambda$ 求和的重整化
**解法二动画要点** - $E[X(X-1)]=\lambda^2$ 的阶乘矩重整化示意 - 泊松分布柱状图随 $\lambda$ 变化
**解法三动画要点** - 矩母函数 $M(t)=e^{\lambda(e^t-1)}$ 的曲线 - 二阶导 $M''(0)=\lambda^2+\lambda$ 的标注

### eval-prob-007 概率论 · 经典概型
**题目** 房间里随机聚集 30 个人（假设生日在一年 365 天中等可能且相互独立）。求至少有两人生日相同的概率。
**答案** $1-\dfrac{365\cdot 364\cdots 336}{365^{30}}\approx 0.7063$
**解法一（对立事件）** 记 $A$=至少两人生日相同。$\bar A$=30 人生日全不同。依次安排生日：第 1 人 $365$ 种，第 2 人 $364$ 种，$\dots$，第 30 人 $336$ 种。$P(\bar A)=\dfrac{365\cdot 364\cdots 336}{365^{30}}$。故 $P(A)=1-\dfrac{365\cdot 364\cdots 336}{365^{30}}=1-0.29368\cdots\approx 0.7063$。
**解法二（递推计算）** 记 $p_k$=前 $k$ 人生日全不同的概率。$p_1=1$，$p_k=p_{k-1}\cdot\dfrac{365-(k-1)}{365}$。依次计算：$p_{10}\approx 0.88305$，$p_{20}\approx 0.58856$，$p_{23}\approx 0.49270$（第 23 人时首次低于 $\dfrac{1}{2}$），$p_{30}\approx 0.29368$。故 $P(A)=1-p_{30}\approx 0.70632$。
**解法三（配对计数的精确期望视角）** 30 人两两配对共 $C_{30}^2=435$ 对，每对生日相同的概率恰为 $\dfrac{1}{365}$，由期望线性性，"生日相同对数"的期望精确等于 $\dfrac{435}{365}=\dfrac{87}{73}\approx 1.19$。期望已大于 1，从侧面印证 $P(A)$ 较大；精确概率仍由解法一的对立事件公式给出。
**思路展开** 本题展示"小概率事件的碰撞效应"：每人只需避开前人生日，$p_k$ 逐项衰减，第 23 人即跌破 $\dfrac{1}{2}$。解法二的递推表是计算途径，解法三用期望线性性给出直觉支撑（精确期望 1.19 对，不是估计）。动画可画 365 个格子被随机占位的模拟，以及 $p_k$ 随 $k$ 下降的曲线。
**解法一动画要点** - 对立事件乘积式 $\dfrac{365\cdot364\cdots336}{365^{30}}$ 的逐项生成 - 365 格生日占位动画
**解法二动画要点** - $p_k$ 下降曲线与 $k=23$ 临界点 - 递推式 $p_k=p_{k-1}\cdot\dfrac{366-k}{365}$ 的标注
**解法三动画要点** - 435 对配对的计数高亮 - 期望 $\dfrac{87}{73}\approx1.19$ 的线性性标注

### eval-prob-008 概率论 · 大数定律
**题目** 设 $X\sim B\!\left(100,\dfrac{1}{2}\right)$。用切比雪夫不等式给出 $P(|X-50|\ge 10)$ 的上界，并与精确值比较。
**答案** 切比雪夫上界 $\dfrac{1}{4}$；精确值 $2\displaystyle\sum_{k=0}^{40}\binom{100}{k}\left(\frac{1}{2}\right)^{100}\approx 0.0569$
**解法一（切比雪夫不等式）** $E[X]=np=50$，$\operatorname{Var}(X)=np(1-p)=25$。由切比雪夫不等式 $P(|X-E[X]|\ge\varepsilon)\le\dfrac{\operatorname{Var}(X)}{\varepsilon^2}$，取 $\varepsilon=10$：$P(|X-50|\ge 10)\le\dfrac{25}{100}=\dfrac{1}{4}$。
**解法二（精确二项求和）** $P(|X-50|\ge 10)=P(X\le 40)+P(X\ge 60)$。由对称性（$p=\dfrac{1}{2}$），$P(X\ge 60)=P(X\le 40)$（$X$ 与 $100-X$ 同分布），故 $P=2P(X\le 40)=2\displaystyle\sum_{k=0}^{40}\binom{100}{k}\left(\dfrac{1}{2}\right)^{100}\approx 0.0569$。
**解法三（方法对比讨论）** 切比雪夫上界 $0.25$ 只需均值与方差、对任何同均值方差的分布都成立（通用性），但远松于精确值 $0.0569$；精确计算需要完整的二项分布信息（专用性）。两者之差 $0.193$ 体现了"分布无关界"与"分布相关值"的代价差。动画可并排展示两种结果的对比条。
**解法一动画要点** - 切比雪夫不等式 $\dfrac{25}{100}=\dfrac{1}{4}$ 的代入 - 上界水平线标注
**解法二动画要点** - 二项分布柱状图与 $|X-50|<10$ 区间高亮 - 对称性 $P(X\ge60)=P(X\le40)$ 的尾部概率放大
**解法三动画要点** - 切比雪夫上界与精确值 0.0569 的对比条 - "分布无关界 vs 分布相关值"的标注

### eval-prob-009 概率论 · 多维随机变量
**题目** 设 $X,Y$ 相互独立且均服从 $\operatorname{Exp}(1)$，求 $Z=\min(X,Y)$ 的分布。
**答案** $Z\sim\operatorname{Exp}(2)$，密度 $f_Z(z)=2e^{-2z}$（$z>0$）
**解法一（生存函数法）** $P(Z>z)=P(X>z,Y>z)=P(X>z)P(Y>z)=e^{-z}\cdot e^{-z}=e^{-2z}$（$z>0$，由独立性）。故 $F_Z(z)=1-e^{-2z}$，$f_Z(z)=2e^{-2z}$，即 $Z\sim\operatorname{Exp}(2)$。
**解法二（次序统计量公式）** 最小值的密度公式：$f_Z(z)=2f(z)[1-F(z)]$，其中 $f(z)=e^{-z}$、$F(z)=1-e^{-z}$ 为 $\operatorname{Exp}(1)$ 的密度与分布函数。故 $f_Z(z)=2e^{-z}\cdot e^{-z}=2e^{-2z}$。
**解法三（几何积分）** 联合密度 $f(x,y)=e^{-x-y}$（$x,y>0$）。$P(Z>z)=\displaystyle\int_z^\infty\!\!\int_z^\infty e^{-x-y}\,dx\,dy=\left(\int_z^\infty e^{-x}dx\right)\left(\int_z^\infty e^{-y}dy\right)=e^{-z}\cdot e^{-z}=e^{-2z}$，与解法一一致。
**思路展开** 求最小值分布，"生存函数法"总是首选（$\min>z$ 等价于每个都 $>z$，事件结构简单）；次序统计量公式给出一般形式；几何法把独立性与区域积分连接起来。指数分布的"最小值仍是指数、参数相加"是可靠性理论的基石。动画可展示第一象限中 $x>z,y>z$ 的方形区域随 $z$ 收缩。
**解法一动画要点** - 生存函数 $P(Z>z)=e^{-z}e^{-z}$ 的乘积动画 - $\min>z$ 区域的收缩动画
**解法二动画要点** - 次序统计量公式 $2f(z)[1-F(z)]$ 的代入 - 密度 $2e^{-2z}$ 的生成
**解法三动画要点** - 联合密度曲面与方形区域 - 二重积分 $\int_z^\infty\int_z^\infty e^{-x-y}dxdy$ 的分解

### eval-prob-010 概率论 · 期望
**题目** $n$ 个人各带一顶帽子，帽子随机打乱后每人随机取回一顶（全排列等可能）。求取到自己帽子的人数的期望，并说明该期望不依赖 $n$ 的原因。
**答案** $1$（与 $n$ 无关）
**解法一（指示变量+期望线性性）** 设 $I_i$ 为"第 $i$ 人取到自己帽子"的指示变量。由对称性，第 $i$ 人取到自己帽子的概率 $P(I_i=1)=\dfrac{1}{n}$（$n$ 顶帽子中恰有一顶属于他，均匀排列下等可能）。总正确人数 $X=I_1+\cdots+I_n$，由期望线性性（**不要求独立性**）：$E[X]=\displaystyle\sum_{i=1}^{n}E[I_i]=\sum_{i=1}^{n}P(I_i=1)=n\cdot\dfrac{1}{n}=1$。
**解法二（分布与生成函数）** 恰有 $k$ 人取对的概率 $P(X=k)=\dfrac{\binom{n}{k}D(n-k)}{n!}$，其中 $D(m)=m!\displaystyle\sum_{j=0}^{m}\dfrac{(-1)^j}{j!}$ 为错排数。生成函数 $G(z)=\displaystyle\sum_{k=0}^{n}\dfrac{\binom{n}{k}D(n-k)}{n!}z^k$。$E[X]=G'(1)=\dfrac{1}{n!}\displaystyle\sum_{k=1}^{n}k\binom{n}{k}D(n-k)=\dfrac{n}{n!}\sum_{k=1}^{n}\binom{n-1}{k-1}D(n-k)=\dfrac{1}{(n-1)!}\sum_{j=0}^{n-1}\binom{n-1}{j}D(n-1-j)$。而 $\displaystyle\sum_{j=0}^{n-1}\binom{n-1}{j}D(n-1-j)=(n-1)!$（对 $n-1$ 个元素的所有排列按"不动点个数 $j$"分类计数），故 $E[X]=1$。
**解法三（双重计数）** 对全部 $n!$ 种排列统计"拿对帽子"的总人次：对任意固定的第 $i$ 人，其帽子被自己拿到的排列数为 $(n-1)!$（其余 $n-1$ 顶帽子任意排列），故总固定点数 $=\displaystyle\sum_{i=1}^{n}(n-1)!=n\cdot(n-1)!=n!$。除以排列总数 $n!$，得期望 $=\dfrac{n!}{n!}=1$。期望不随 $n$ 变化的本质是"每顶帽子命中率恒为 $\dfrac{1}{n}$、恰好 $n$ 顶"。
**思路展开** 本题是"期望线性性无视相关性"的经典证明题：$I_1,\dots,I_n$ 高度相关（两人可能互换帽子），但线性性照常成立。解法二走完整分布+生成函数的路线并给出严格恒等式，解法一一步到位。动画可模拟 $n$ 人交换帽子的过程并统计正确人数。
**解法一动画要点** - 指示变量 $I_i$ 的高亮 - 期望线性性 $n\cdot\dfrac{1}{n}=1$ 的标注
**解法二动画要点** - 分布柱状图 $P(X=k)=\binom{n}{k}D(n-k)/n!$ - 生成函数 $G(z)$ 与导数求和 $G'(1)$ - 按固定点个数分类的 $n-1$ 元素排列示意
**解法三动画要点** - $n$ 人帽子随机交换动画 - 总固定点数 $n!$ 的双重计数示意

### eval-prob-011 概率论 · 随机过程
**题目** 抛均匀硬币直到连续出现两次正面（HH）为止，求所需抛掷次数的期望。
**答案** $6$
**解法一（状态递推方程）** 设 $E_0$=当前无连续正面记录时的期望剩余次数，$E_1$=刚出现一次正面时的期望剩余次数。状态转移：$E_0=1+\dfrac{1}{2}E_0+\dfrac{1}{2}E_1$（抛一次后：反面回 $E_0$，正面进 $E_1$）；$E_1=1+\dfrac{1}{2}\cdot 0+\dfrac{1}{2}E_0$（再抛：正面完成，反面回 $E_0$）。由第二式 $E_1=1+\dfrac{E_0}{2}$，代入第一式：$E_0=1+\dfrac{E_0}{2}+\dfrac{1}{2}\left(1+\dfrac{E_0}{2}\right)=\dfrac{3}{2}+\dfrac{3E_0}{4}$，解得 $E_0=6$。
**解法二（吸收马尔可夫链）** 状态 $\{0,1,H\}$（$H$ 为吸收态），转移矩阵 $P=\begin{pmatrix}1/2&1/2&0\\1/2&0&1/2\\0&0&1\end{pmatrix}$，瞬态子矩阵 $Q=\begin{pmatrix}1/2&1/2\\1/2&0\end{pmatrix}$。基本矩阵 $N=(I-Q)^{-1}=\begin{pmatrix}1/2&-1/2\\-1/2&1\end{pmatrix}^{-1}=4\begin{pmatrix}1&1/2\\1/2&1/2\end{pmatrix}=\begin{pmatrix}4&2\\2&2\end{pmatrix}$（$\det(I-Q)=\dfrac{1}{2}-\dfrac{1}{4}=\dfrac{1}{4}$）。从状态 0 出发的期望步数为 $N$ 第 1 行之和 $=4+2=6$。
**解法三（首达分布与生成函数）** 首次出现 HH 的时刻 $T\ge 2$，其分布为 $P(T=k)=\dfrac{F_{k-1}}{2^k}$（$k\ge 2$），其中 $F_1=F_2=1$ 为斐波那契数（$k$ 次抛掷中前 $k-1$ 次无 HH 且第 $k$ 次前恰为 $\dots H$ 的计数即斐波那契递推）。概率母函数 $G(z)=\displaystyle\sum_{k=2}^{\infty}\dfrac{F_{k-1}}{2^k}z^k=\dfrac{z^2}{4-2z-z^2}$（由 $\sum_{m\ge 1}F_mx^m=\dfrac{x}{1-x-x^2}$ 代入 $x=\dfrac{z}{2}$ 得）。$E[T]=G'(1)=\left.\dfrac{2z(4-2z-z^2)+z^2(2+2z)}{(4-2z-z^2)^2}\right|_{z=1}=\dfrac{2\cdot 1+4}{1}=6$。
**思路展开** 首达时间的三种算法：状态递推（最直观，适合教学）、吸收马尔可夫链基本矩阵（系统性最强，可推广到任意模式）、生成函数（给出完整分布）。三种方法都用到"无记忆性"：抛硬币的历史只通过"当前连续正面数"影响未来。动画可画状态机图与递推方程的平衡示意。
**解法一动画要点** - 状态递推方程 $E_0=1+\dfrac12E_0+\dfrac12E_1$ 的平衡示意 - 代入求解 $E_0=6$ 的动画
**解法二动画要点** - 三状态转移图与概率箭头 - 基本矩阵 $N=(I-Q)^{-1}=\begin{pmatrix}4&2\\2&2\end{pmatrix}$ 的计算标注
**解法三动画要点** - 斐波那契计数 $P(T=k)=\dfrac{F_{k-1}}{2^k}$ 的生成 - 母函数 $G'(1)=6$ 的求导标注

### eval-prob-012 概率论 · 多维随机变量
**题目** 设 $X,Y$ 相互独立且均服从 $U(0,1)$，求 $P(X+Y\le 1)$。
**答案** $\dfrac{1}{2}$
**解法一（几何面积）** $(X,Y)$ 在单位正方形 $[0,1]^2$ 上均匀分布。事件 $\{X+Y\le 1\}$ 对应正方形中直线 $x+y=1$ 左下方的等腰直角三角形，面积 $\dfrac{1}{2}\cdot 1\cdot 1=\dfrac{1}{2}$。均匀分布下概率=面积比，故 $P=\dfrac{1}{2}$。
**解法二（卷积密度）** $Z=X+Y$ 的密度为卷积：$f_Z(z)=\displaystyle\int_{-\infty}^{\infty}f_X(x)f_Y(z-x)dx=\int_0^1\mathbf 1_{[0,1]}(z-x)dx$。当 $0<z<1$：$f_Z(z)=\displaystyle\int_0^z dx=z$；当 $1<z<2$：$f_Z(z)=\displaystyle\int_{z-1}^1 dx=2-z$（三角分布）。故 $P(X+Y\le 1)=\displaystyle\int_0^1 z\,dz=\dfrac{1}{2}$。
**解法三（对称性）** $(X,Y)$ 与 $(1-X,1-Y)$ 同分布。$X+Y\le 1\iff (1-X)+(1-Y)\ge 1$，且 $P(X+Y=1)=0$。故 $P(X+Y\le 1)=P(X+Y\ge 1)=\dfrac{1}{2}$（两事件互补且等概率）。
**思路展开** 几何法是均匀分布概率的天然语言；卷积法给出 $X+Y$ 的完整分布（三角分布，为后续密度问题铺路）；对称法仅用分布不变性一句话解决，展示了概率论证的简洁力量。动画可画单位正方形中直线 $x+y=1$ 的分割与随机散点。
**解法一动画要点** - 单位正方形与分割直线 $x+y=1$ - 三角形面积 $\dfrac{1}{2}$ 的高亮
**解法二动画要点** - 卷积滑动的矩形面积 - 三角密度 $f_Z(z)=z$、$2-z$ 的生成
**解法三动画要点** - 对称性 $(X,Y)\sim(1-X,1-Y)$ 的镜像动画 - 互补事件等概率的标注

### eval-prob-013 概率论 · 常见分布
**题目** 设 $X\sim N(0,1)$（标准正态分布），求 $E|X|$。
**答案** $\sqrt{\dfrac{2}{\pi}}$
**解法一（直接积分）** $E|X|=\displaystyle\int_{-\infty}^{\infty}|x|\dfrac{1}{\sqrt{2\pi}}e^{-x^2/2}dx=\dfrac{2}{\sqrt{2\pi}}\int_0^{\infty}xe^{-x^2/2}dx$。令 $u=\dfrac{x^2}{2}$（$du=x\,dx$）：$=\dfrac{2}{\sqrt{2\pi}}\displaystyle\int_0^{\infty}e^{-u}du=\dfrac{2}{\sqrt{2\pi}}\cdot 1=\sqrt{\dfrac{2}{\pi}}$。
**解法二（半正态分布）** $|X|$ 服从半正态分布，密度 $f(y)=\dfrac{2}{\sqrt{2\pi}}e^{-y^2/2}$（$y>0$，即把负半轴密度折叠到正半轴）。$E|X|=\displaystyle\int_0^\infty y\dfrac{2}{\sqrt{2\pi}}e^{-y^2/2}dy=\dfrac{2}{\sqrt{2\pi}}\left[-e^{-y^2/2}\right]_0^\infty=\dfrac{2}{\sqrt{2\pi}}=\sqrt{\dfrac{2}{\pi}}$。
**解法三（$\chi^2$ 分布观点）** $Y=X^2\sim\chi^2(1)$，密度 $f_Y(y)=\dfrac{1}{\sqrt{2\pi}}y^{-1/2}e^{-y/2}$（$y>0$）。$E|X|=E[\sqrt{Y}]=\displaystyle\int_0^\infty\sqrt{y}\cdot\dfrac{1}{\sqrt{2\pi}}y^{-1/2}e^{-y/2}dy=\dfrac{1}{\sqrt{2\pi}}\int_0^\infty e^{-y/2}dy=\dfrac{1}{\sqrt{2\pi}}\cdot 2=\sqrt{\dfrac{2}{\pi}}$。
**思路展开** 三种方法分别从偶函数积分、半正态分布、$\chi^2$ 变换入手，展示同一个 $\sqrt{2/\pi}$ 的三条路径。此值约 $0.7979$，介于 $E[X^2]^{1/2}=1$ 与 $|E[X]|=0$ 之间，符合矩的排序。动画可画正态密度折叠成半正态的过程。
**解法一动画要点** - 偶函数积分 $\dfrac{2}{\sqrt{2\pi}}\int_0^\infty xe^{-x^2/2}dx$ 的分解 - 换元 $u=\dfrac{x^2}{2}$ 的标注
**解法二动画要点** - 正态密度负半轴折叠成半正态的动画 - 折叠后积分 $\dfrac{2}{\sqrt{2\pi}}$ 的标注
**解法三动画要点** - $\chi^2(1)$ 密度 $\dfrac{1}{\sqrt{2\pi}}y^{-1/2}e^{-y/2}$ 的曲线 - $E[\sqrt{Y}]$ 的积分过程

### eval-prob-014 概率论 · 常见分布
**题目** 设 $X\sim\operatorname{Exp}(\lambda)$（$\lambda>0$）。证明无记忆性 $P(X>s+t\mid X>s)=P(X>t)$（$s,t>0$），并说明其含义。
**答案** 证毕；无记忆性成立且是指数分布的特征性质
**解法一（直接计算）** $P(X>s+t\mid X>s)=\dfrac{P(X>s+t)}{P(X>s)}=\dfrac{e^{-\lambda(s+t)}}{e^{-\lambda s}}=e^{-\lambda t}=P(X>t)$。即条件后剩余寿命的分布与全新时完全相同。
**解法二（危险率函数）** 危险率函数 $h(t)=\dfrac{f(t)}{1-F(t)}=\dfrac{\lambda e^{-\lambda t}}{e^{-\lambda t}}=\lambda$ 为常数。常数危险率意味着"每时每刻的瞬时失效倾向不随年龄变化"，这正是无记忆性的微分刻画；反之，若某分布危险率为常数 $\lambda$，解微分方程 $\dfrac{F'}{1-F}=\lambda$ 得 $F(t)=1-e^{-\lambda t}$，故常数危险率⇔指数分布。
**解法三（泊松过程视角）** 在强度 $\lambda$ 的泊松过程中，相邻事件的时间间隔服从 $\operatorname{Exp}(\lambda)$。已等待 $s$ 而无事件发生，意味着 $(0,s]$ 内的事件数 $N(s)=0$；由泊松过程的独立增量性，$(s,s+t]$ 内的事件数与 $(0,s]$ 内无关，$P(N(s,s+t)=0\mid N(s)=0)=P(N(s,s+t)=0)=e^{-\lambda t}$。故剩余等待时间仍服从 $\operatorname{Exp}(\lambda)$。
**思路展开** 无记忆性的三种视角：生存函数直接相除（计算）、危险率常数（微分方程）、泊松过程独立增量（随机过程）。解法二还证明它是特征性质——只有指数分布无记忆，这在可靠性理论与排队论中至关重要。动画可展示生存函数曲线右移后与自身重合的"自相似"结构。
**解法一动画要点** - 生存函数比值 $\dfrac{e^{-\lambda(s+t)}}{e^{-\lambda s}}$ 的相消动画 - 自相似右移的标注
**解法二动画要点** - 危险率常数 $h(t)=\lambda$ 的水平线 - 微分方程 $\dfrac{F'}{1-F}=\lambda$ 的求解
**解法三动画要点** - 泊松过程时间轴上的间隔 - 独立增量性 $P(N(s,s+t)=0|N(s)=0)$ 的标注

### eval-prob-015 概率论 · 数字特征
**题目** 掷一枚均匀骰子，设 $X$ 为点数。求 $E[X]$ 与 $\operatorname{Var}(X)$。
**答案** $E[X]=\dfrac{7}{2}$，$\operatorname{Var}(X)=\dfrac{35}{12}$
**解法一（定义计算）** $E[X]=\dfrac{1+2+3+4+5+6}{6}=\dfrac{21}{6}=\dfrac{7}{2}$。$E[X^2]=\dfrac{1+4+9+16+25+36}{6}=\dfrac{91}{6}$。$\operatorname{Var}(X)=E[X^2]-(E[X])^2=\dfrac{91}{6}-\dfrac{49}{4}=\dfrac{182-147}{12}=\dfrac{35}{12}$。
**解法二（矩母函数）** $M(t)=\dfrac{e^t+e^{2t}+e^{3t}+e^{4t}+e^{5t}+e^{6t}}{6}$。$M'(0)=\dfrac{1+2+3+4+5+6}{6}=\dfrac{7}{2}$，$M''(0)=\dfrac{1+4+9+16+25+36}{6}=\dfrac{91}{6}$。故 $E[X]=\dfrac{7}{2}$，$\operatorname{Var}(X)=M''(0)-[M'(0)]^2=\dfrac{35}{12}$。
**解法三（离散均匀公式+线性变换）** 令 $X=1+U$，其中 $U\sim U\{0,1,\dots,5\}$。离散均匀分布 $\{0,\dots,n-1\}$ 的方差公式：$\operatorname{Var}(U)=\dfrac{n^2-1}{12}=\dfrac{36-1}{12}=\dfrac{35}{12}$。故 $E[X]=1+\dfrac{5}{2}=\dfrac{7}{2}$，$\operatorname{Var}(X)=\operatorname{Var}(U)=\dfrac{35}{12}$。
**思路展开** 定义法最基础；矩母函数把两个矩统一在一次微分中；离散均匀方差公式展示"平移不变、缩放平方"的方差性质（$+1$ 平移对方差无影响）。动画可画点数柱状图与其重心、离散度的标注。
**解法一动画要点** - 均匀柱状图与重心 $3.5$ - $E[X^2]=\dfrac{91}{6}$ 的逐格求和
**解法二动画要点** - 矩母函数 $M(t)$ 的曲线 - $M'(0)=\dfrac72$、$M''(0)=\dfrac{91}{6}$ 的切线标注
**解法三动画要点** - 离散均匀方差 $\dfrac{n^2-1}{12}$ 的公式标注 - 平移 $+1$ 的方差不变性

# 四、高等代数（35 题）

### eval-linalg-001 高等代数 · 行列式
**题目** 计算范德蒙德行列式 $\begin{vmatrix}1&1&1\\a&b&c\\a^2&b^2&c^2\end{vmatrix}$，并求 $a=1,b=2,c=3$ 时的值。
**答案** $(b-a)(c-a)(c-b)$；取值 $2$
**解法一（行变换降阶）** 第二行减第一行的 $a$ 倍、第三行减第一行的 $a^2$ 倍：$D=\begin{vmatrix}1&1&1\\0&b-a&c-a\\0&b^2-a^2&c^2-a^2\end{vmatrix}$。按第一列展开：$D=\begin{vmatrix}b-a&c-a\\b^2-a^2&c^2-a^2\end{vmatrix}=(b-a)(c-a)\begin{vmatrix}1&1\\b+a&c+a\end{vmatrix}=(b-a)(c-a)\left[(c+a)-(b+a)\right]=(b-a)(c-a)(c-b)$。代入 $a=1,b=2,c=3$：$D=(1)(2)(1)=2$。
**解法二（多项式观点）** 把 $D$ 看成关于 $c$ 的多项式 $f(c)$。按第三列展开，$c^2$ 的系数为 $\begin{vmatrix}1&1\\a&b\end{vmatrix}=b-a$，故 $f$ 至多是二次多项式。当 $c=a$ 或 $c=b$ 时，第三列与第一列（或第二列）相同，$f=0$，故 $f(c)=k(c-a)(c-b)$。取 $k=b-a$（最高次系数），得 $D=(b-a)(c-a)(c-b)$。（$a=b$ 时 $k=0$ 且 $D=0$，公式两端均为 0，仍成立。）
**解法三（归纳验证）** $n$ 阶范德蒙德行列式 $D_n=\prod_{1\le i<j\le n}(x_j-x_i)$ 可用数学归纳法证明：自下而上做行变换 $R_k\leftarrow R_k-x_1R_{k-1}$（$k=n,n-1,\dots,2$），再按第一列展开、各列提取公因子 $x_j-x_1$，即降阶为 $n-1$ 阶范德蒙德行列式，归纳即得。$n=3$ 时即 $(b-a)(c-a)(c-b)$，代入得 $2$。
**思路展开** 范德蒙德行列式是行列式计算的"基本积木"，三种解法分别代表行变换、多项式插值思想、归纳降阶。解法二的多项式观点最具启发性：行列式关于某一列参数是多项式，根的定位（列相同则为零）直接给出因子分解。动画可展示列向量随 $c$ 变化时平行六面体体积的变化与零点。
**解法一动画要点** - 行变换 $R_2-aR_1$、$R_3-a^2R_1$ 的逐步动画 - 降阶二阶行列式的提取
**解法二动画要点** - 多项式 $f(c)$ 与根 $a,b$ 的标注 - 最高次系数 $b-a$ 的提取（含 $a=b$ 的零多项式情形）
**解法三动画要点** - 自下而上 $R_k\leftarrow R_k-x_1R_{k-1}$ 的归纳动画 - 各列提取公因子 $x_j-x_1$ 的降阶

### eval-linalg-002 高等代数 · 行列式
**题目** 计算四阶行列式 $D=\begin{vmatrix}1&1&1&1\\1&2&1&1\\1&1&3&1\\1&1&1&4\end{vmatrix}$。
**答案** $6$
**解法一（行变换三角化）** 第二、三、四行分别减去第一行：$D=\begin{vmatrix}1&1&1&1\\0&1&0&0\\0&0&2&0\\0&0&0&3\end{vmatrix}$。上三角行列式等于对角线元素之积：$D=1\cdot 1\cdot 2\cdot 3=6$。
**解法二（加边法）** 加边升阶：$D=\begin{vmatrix}1&1&1&1&1\\0&1&1&1&1\\0&1&2&1&1\\0&1&1&3&1\\0&1&1&1&4\end{vmatrix}$（按第一列展开即原行列式）。新行列式中，第三、四、五行分别减去第二行：$=\begin{vmatrix}1&1&1&1&1\\0&1&1&1&1\\0&0&1&0&0\\0&0&0&2&0\\0&0&0&0&3\end{vmatrix}=1\cdot 1\cdot 1\cdot 2\cdot 3=6$。
**解法三（展开降阶）** 每行减末行：$\begin{vmatrix}0&0&0&-3\\0&1&0&-3\\0&0&2&-3\\1&1&1&4\end{vmatrix}$，按第一列展开：$D=(-1)^{4+1}\cdot 1\cdot\begin{vmatrix}0&0&-3\\1&0&-3\\0&2&-3\end{vmatrix}=-\left[0-0+(-3)\begin{vmatrix}1&0\\0&2\end{vmatrix}\right]=-(-3\cdot 2)=6$。
**思路展开** 行变换（化为上三角）、加边法（升一阶后一次消元）、展开降阶（按行列展开+三阶余子式）是行列式计算的三大套路。加边法的妙处在于"增加一维换来对角化"。动画可展示矩阵元素逐步清零的消元过程。
**解法一动画要点** - 各行减首行的消元三角化动画 - 对角线 $1,1,2,3$ 之积的标注
**解法二动画要点** - 加边升阶的 $5\times5$ 结构示意 - 升阶后一次消元得对角形的过程
**解法三动画要点** - 每行减末行的展开降阶 - 三阶余子式按第一列展开的高亮

### eval-linalg-003 高等代数 · 行列式
**题目** 求 $n$ 阶三对角行列式 $D_n=\begin{vmatrix}2&1&0&\cdots&0\\1&2&1&\cdots&0\\0&1&2&\cdots&0\\\vdots&&&\ddots&\vdots\\0&0&0&\cdots&2\end{vmatrix}$ 的值（矩阵元素满足 $a_{ii}=2$，$a_{i,i+1}=a_{i+1,i}=1$，其余为 0）。
**答案** $D_n=n+1$
**解法一（递推公式）** 按第一行展开：$D_n=2D_{n-1}-1\cdot\begin{vmatrix}1&1&0&\cdots\\0&2&1&\cdots\\\vdots&&&\ddots\end{vmatrix}=2D_{n-1}-D_{n-2}$（第二项按第一列展开后恰为 $D_{n-2}$）。初始值 $D_1=2$，$D_2=\begin{vmatrix}2&1\\1&2\end{vmatrix}=3$。由递推 $D_n-D_{n-1}=D_{n-1}-D_{n-2}=\cdots=D_2-D_1=1$，故 $D_n=D_1+(n-1)=n+1$。
**解法二（特征值乘积）** 该矩阵 $A=2I+B$，其中 $B$ 是 $n$ 阶路的邻接矩阵，其特征值为 $2\cos\dfrac{k\pi}{n+1}$（$k=1,\dots,n$）。故 $D_n=\det(2I+B)=\displaystyle\prod_{k=1}^{n}\left(2+2\cos\dfrac{k\pi}{n+1}\right)=2^n\prod_{k=1}^{n}\left(1+\cos\dfrac{k\pi}{n+1}\right)$。利用恒等式 $\displaystyle\prod_{k=1}^{n}\left(2+2\cos\dfrac{k\pi}{n+1}\right)=n+1$，证明如下：由 $x^{2n+2}-1=(x^2-1)\displaystyle\prod_{k=1}^{n}\left(x^2-2x\cos\dfrac{k\pi}{n+1}+1\right)$，两边同除 $x^2-1$ 得 $\dfrac{x^{2n+2}-1}{x^2-1}=\displaystyle\sum_{j=0}^{n}x^{2j}=\prod_{k=1}^{n}\left(x^2-2x\cos\dfrac{k\pi}{n+1}+1\right)$；令 $x\to-1$：左端 $\to n+1$，右端 $\to\displaystyle\prod_{k=1}^{n}\left(2+2\cos\dfrac{k\pi}{n+1}\right)$。得 $D_n=n+1$。
**解法三（数学归纳法）** 由解法一的递推式，归纳证明 $D_n=n+1$：$n=1,2$ 已验证；设 $D_{n-1}=n$、$D_{n-2}=n-1$，则 $D_n=2D_{n-1}-D_{n-2}=2n-(n-1)=n+1$。
**思路展开** 三对角行列式是递推法的主战场（按首行展开得到二阶线性递推）；特征值法把它与图的谱联系起来（路图邻接矩阵）；归纳法给出严谨闭环。动画可展示递推链 $D_1\to D_2\to\cdots$ 的展开树。
**解法一动画要点** - 首行展开的递推树 $D_n=2D_{n-1}-D_{n-2}$ - 递推序列 $2,3,4,\dots$ 的点列
**解法二动画要点** - 邻接矩阵特征值 $2\cos\dfrac{k\pi}{n+1}$ 的单位圆标注 - 恒等式 $x^{2n+2}-1$ 除 $x^2-1$ 取极限的推导
**解法三动画要点** - 归纳递推 $2n-(n-1)=n+1$ 的代入 - 三对角矩阵结构高亮

### eval-linalg-004 高等代数 · 行列式
**题目** 计算 $n=3$ 时行列式 $D=\begin{vmatrix}a+b&a&a\\a&a+b&a\\a&a&a+b\end{vmatrix}$，并推广到 $n$ 阶。
**答案** $b^2(3a+b)$；$n$ 阶为 $b^{n-1}(na+b)$
**解法一（行变换）** 第二、三行分别减去第一行：$D=\begin{vmatrix}a+b&a&a\\-b&b&0\\-b&0&b\end{vmatrix}$。按第一行展开：$D=(a+b)\cdot b^2-a\cdot\begin{vmatrix}-b&0\\-b&b\end{vmatrix}+a\cdot\begin{vmatrix}-b&b\\-b&0\end{vmatrix}=(a+b)b^2-a(-b^2)+a(b^2)=b^2(a+b)+ab^2+ab^2=b^2(3a+b)$。
**解法二（特征值法）** 该矩阵 $A=bI+aJ$，其中 $J$ 为全 1 矩阵。$J$ 的特征值为 $n,0,\dots,0$（$J$ 的秩为 1，且 $J(1,\dots,1)^T=n(1,\dots,1)^T$），故 $A$ 的特征值为 $b+na$（一重）与 $b$（$n-1$ 重）。行列式=特征值之积：$D=(b+3a)\cdot b\cdot b=b^2(3a+b)$（$n=3$）；一般地 $D_n=b^{n-1}(na+b)$。
**解法三（拆列法，行列式线性性）** 把每列拆成 $(a,a,a)^T+b\,e_i$（$e_i$ 为标准基向量）。由行列式关于列的多重线性：全取 $b\,e_i$ 的项为 $b^3\det I=b^3$；恰有一列取 $(a,a,a)^T$ 的项有 3 个，每个为 $ab^2\cdot\det(e_1,e_2,e_j$ 换为 $(1,1,1)^T)=ab^2$；有两列以上取 $(a,a,a)^T$ 的项行列式为 0（两列相同）。故 $D=b^3+3ab^2=b^2(3a+b)$。
**思路展开** 三种方法分别代表消元、谱方法、多重线性展开。特征值法揭示了这类"循环结构矩阵"的谱结构，拆列法把行列式当成列向量的多重线性函数来用——两者都可直接推广到 $n$ 阶。动画可展示矩阵的"对角+全 1"分解与特征方向。
**解法一动画要点** - 后两行减首行的消元动画 - 按首行展开的三项计算
**解法二动画要点** - 矩阵分解 $bI+aJ$ 的色块示意 - 特征值 $b+3a,b,b$ 的谱标注
**解法三动画要点** - 拆列法的组合枚举（全 $b$ 列、恰一 $a$ 列、两 $a$ 列为零） - 多重线性的标注

### eval-linalg-005 高等代数 · 矩阵
**题目** 求矩阵 $A=\begin{pmatrix}3&2\\4&3\end{pmatrix}$ 的逆矩阵。
**答案** $A^{-1}=\begin{pmatrix}3&-2\\-4&3\end{pmatrix}$
**解法一（伴随矩阵法）** $\det A=3\cdot 3-2\cdot 4=9-8=1$。$A^*=\begin{pmatrix}3&-2\\-4&3\end{pmatrix}$（代数余子式转置：$A_{11}=3$，$A_{12}=-4$，$A_{21}=-2$，$A_{22}=3$）。$A^{-1}=\dfrac{A^*}{\det A}=\begin{pmatrix}3&-2\\-4&3\end{pmatrix}$。验证：$AA^{-1}=\begin{pmatrix}9-8&-6+6\\12-12&-8+9\end{pmatrix}=I$。
**解法二（初等行变换）** 对增广矩阵 $(A\mid I)$ 做行变换：$\begin{pmatrix}3&2&|&1&0\\4&3&|&0&1\end{pmatrix}\xrightarrow{R_2-\frac{4}{3}R_1}\begin{pmatrix}3&2&|&1&0\\0&\frac{1}{3}&|&-\frac{4}{3}&1\end{pmatrix}\xrightarrow{R_1-6R_2}\begin{pmatrix}3&0&|&9&-6\\0&\frac{1}{3}&|&-\frac{4}{3}&1\end{pmatrix}\xrightarrow{R_1/3,\ 3R_2}\begin{pmatrix}1&0&|&3&-2\\0&1&|&-4&3\end{pmatrix}$，故 $A^{-1}=\begin{pmatrix}3&-2\\-4&3\end{pmatrix}$。
**解法三（解方程组）** 设 $A^{-1}$ 的第 $j$ 列为 $x^{(j)}$，解 $Ax^{(1)}=e_1$、$Ax^{(2)}=e_2$。第一组：$\begin{cases}3x+2y=1\\4x+3y=0\end{cases}$，由第二式 $y=-\dfrac{4x}{3}$ 代入第一式：$3x-\dfrac{8x}{3}=1$，$x=3$，$y=-4$。第二组：$\begin{cases}3x+2y=0\\4x+3y=1\end{cases}$，得 $x=-2$，$y=3$。故 $A^{-1}=\begin{pmatrix}3&-2\\-4&3\end{pmatrix}$。
**思路展开** 三种求逆方法各有定位：伴随矩阵适合低阶手算，初等行变换是机器实现的通用算法，解方程组揭示"逆矩阵就是同时解 $n$ 个线性方程组"。本题 $\det A=1$ 使伴随法格外干净。动画可展示行变换把 $(A|I)$ 变成 $(I|A^{-1})$ 的过程。
**解法一动画要点** - 伴随矩阵四个代数余子式的标注 - $\det A=1$ 的标注
**解法二动画要点** - $(A|I)\to(I|A^{-1})$ 的行变换动画 - 分数消元的逐步展示
**解法三动画要点** - 解 $Ax=e_1$、$Ax=e_2$ 两组方程的过程 - $AA^{-1}=I$ 验证

### eval-linalg-006 高等代数 · 矩阵
**题目** 设 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$，求 $A^n$（$n$ 为正整数）。
**答案** $A^n=\begin{pmatrix}1&n\\0&1\end{pmatrix}$
**解法一（数学归纳法）** $A^1=\begin{pmatrix}1&1\\0&1\end{pmatrix}$。设 $A^k=\begin{pmatrix}1&k\\0&1\end{pmatrix}$，则 $A^{k+1}=A^kA=\begin{pmatrix}1&k\\0&1\end{pmatrix}\begin{pmatrix}1&1\\0&1\end{pmatrix}=\begin{pmatrix}1&1+k\\0&1\end{pmatrix}$。归纳得 $A^n=\begin{pmatrix}1&n\\0&1\end{pmatrix}$。
**解法二（二项式展开）** $A=I+N$，其中 $N=\begin{pmatrix}0&1\\0&0\end{pmatrix}$，且 $N^2=0$。$I$ 与 $N$ 可交换，由二项式定理：$A^n=(I+N)^n=I^n+\binom{n}{1}I^{n-1}N+\binom{n}{2}I^{n-2}N^2+\cdots=I+nN=\begin{pmatrix}1&n\\0&1\end{pmatrix}$（$N^2$ 起全为 0）。
**解法三（若尔当形观点）** $A$ 的特征值为 $\lambda=1$（二重），$A-I=N\ne 0$ 而 $(A-I)^2=0$，故 $A$ 的若尔当标准形为 $J=\begin{pmatrix}1&1\\0&1\end{pmatrix}=A$ 本身。$J^n$ 的计算同解法二，得 $\begin{pmatrix}1&n\\0&1\end{pmatrix}$。
**思路展开** 本题是"幂零扰动"的典范：$A=I+N$ 且 $N^2=0$，二项式展开只留两项。三种方法（归纳、二项式、若尔当）层层递进，其中二项式法最深刻——它把矩阵幂的计算化为幂零矩阵的阶数问题。动画可展示 $A$ 的剪切变换作用 $n$ 次的过程。
**解法一动画要点** - $A^{k+1}=A^kA$ 的乘法递推动画 - $A^n$ 元素随 $n$ 增长的表格
**解法二动画要点** - 二项式展开只留两项（$N^2=0$）的原因 - $I$ 与 $N$ 可交换的标注
**解法三动画要点** - 剪切变换重复作用的动画 - 若尔当形 $J=A$ 本身的标注

### eval-linalg-007 高等代数 · 矩阵
**题目** 设 $A=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}$，求 $A^n$。
**答案** $A^n=\begin{pmatrix}\cos n\theta&-\sin n\theta\\\sin n\theta&\cos n\theta\end{pmatrix}$
**解法一（数学归纳法+和角公式）** $n=1$ 成立。设 $A^k=\begin{pmatrix}\cos k\theta&-\sin k\theta\\\sin k\theta&\cos k\theta\end{pmatrix}$，则 $A^{k+1}=A^kA$，其 $(1,1)$ 元为 $\cos k\theta\cos\theta-\sin k\theta\sin\theta=\cos(k+1)\theta$，$(1,2)$ 元为 $-\cos k\theta\sin\theta-\sin k\theta\cos\theta=-\sin(k+1)\theta$，其余两元同理。归纳成立。
**解法二（特征值分解）** 特征方程 $(\cos\theta-\lambda)^2+\sin^2\theta=0$，即 $\lambda^2-2\lambda\cos\theta+1=0$，特征值 $\lambda=e^{\pm i\theta}$，对应特征向量 $(1,\mp i)^T$。取 $P=\begin{pmatrix}1&1\\-i&i\end{pmatrix}$，$P^{-1}=\dfrac{1}{2}\begin{pmatrix}1&i\\1&-i\end{pmatrix}$，则 $A=P\begin{pmatrix}e^{i\theta}&0\\0&e^{-i\theta}\end{pmatrix}P^{-1}$。故 $A^n=P\begin{pmatrix}e^{in\theta}&0\\0&e^{-in\theta}\end{pmatrix}P^{-1}=\dfrac{1}{2}\begin{pmatrix}e^{in\theta}+e^{-in\theta}&i(e^{in\theta}-e^{-in\theta})\\-i(e^{in\theta}-e^{-in\theta})&e^{in\theta}+e^{-in\theta}\end{pmatrix}=\begin{pmatrix}\cos n\theta&-\sin n\theta\\\sin n\theta&\cos n\theta\end{pmatrix}$（用欧拉公式 $e^{\pm in\theta}=\cos n\theta\pm i\sin n\theta$ 化简）。
**解法三（复数同构）** 旋转矩阵 $A$ 与复数乘法 $z\mapsto e^{i\theta}z$ 一一对应（$(x,y)\mapsto(x\cos\theta-y\sin\theta,\ x\sin\theta+y\cos\theta)$ 正是 $e^{i\theta}(x+iy)$ 的实虚部）。旋转的复合即角度相加：$(e^{i\theta})^n=e^{in\theta}$，对应 $A^n=$ 旋转 $n\theta$ 角的矩阵。
**思路展开** 旋转矩阵的幂就是角度的累加，三种方法分别从归纳（代数运算）、特征值分解（谱方法）、复数同构（结构对应）证明之。解法三最简洁：把矩阵问题翻译成复数问题。动画可展示单位向量绕原点连续旋转 $n\theta$ 的过程。
**解法一动画要点** - $A^{k+1}=A^kA$ 的和角公式动画 - 单位向量旋转 $n\theta$ 的动画
**解法二动画要点** - 特征值 $e^{\pm i\theta}$ 的单位圆标注 - 对角化三连乘的矩阵运算
**解法三动画要点** - 复平面与实平面的对应 - $e^{i\theta}$ 幂的辐角累加

### eval-linalg-008 高等代数 · 矩阵
**题目** 设 $A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$，求 $\det A$、$A$ 的秩与 $A^{-1}$。
**答案** $\det A=-2$；秩为 $2$；$A^{-1}=\begin{pmatrix}-2&1\\\frac{3}{2}&-\frac{1}{2}\end{pmatrix}$
**解法一（伴随矩阵法）** $\det A=1\cdot 4-2\cdot 3=-2\ne 0$，故 $A$ 可逆、秩为 $2$。$A^*=\begin{pmatrix}4&-2\\-3&1\end{pmatrix}$，$A^{-1}=\dfrac{A^*}{\det A}=\dfrac{1}{-2}\begin{pmatrix}4&-2\\-3&1\end{pmatrix}=\begin{pmatrix}-2&1\\\frac{3}{2}&-\frac{1}{2}\end{pmatrix}$。
**解法二（初等行变换）** $(A\mid I)=\begin{pmatrix}1&2&|&1&0\\3&4&|&0&1\end{pmatrix}\xrightarrow{R_2-3R_1}\begin{pmatrix}1&2&|&1&0\\0&-2&|&-3&1\end{pmatrix}\xrightarrow{-\frac{1}{2}R_2}\begin{pmatrix}1&2&|&1&0\\0&1&|&\frac{3}{2}&-\frac{1}{2}\end{pmatrix}\xrightarrow{R_1-2R_2}\begin{pmatrix}1&0&|&-2&1\\0&1&|&\frac{3}{2}&-\frac{1}{2}\end{pmatrix}$。故 $A^{-1}=\begin{pmatrix}-2&1\\\frac{3}{2}&-\frac{1}{2}\end{pmatrix}$。
**解法三（秩与方程组）** $\det A=-2\ne 0$ 说明两行（列）线性无关，$\operatorname{rank}A=2$。验证逆矩阵：$AA^{-1}=\begin{pmatrix}1&2\\3&4\end{pmatrix}\begin{pmatrix}-2&1\\\frac{3}{2}&-\frac{1}{2}\end{pmatrix}=\begin{pmatrix}-2+3&1-1\\-6+6&3-2\end{pmatrix}=\begin{pmatrix}1&0\\0&1\end{pmatrix}$。
**思路展开** 行列式非零⇒可逆⇒秩满，这是矩阵理论的第一连锁反应。伴随矩阵、行变换、验证法三路并进。动画可展示秩与行列式的关系（面积缩放 $-2$ 意味着定向反转且面积加倍）。
**解法一动画要点** - 伴随矩阵代数余子式标注 - 除以 $\det A=-2$ 的过程
**解法二动画要点** - $(A|I)\to(I|A^{-1})$ 的行变换动画 - 分数消元的逐步展示
**解法三动画要点** - 单位正方形映射到平行四边形的面积 $-2$（定向反转） - 逆矩阵验证乘法

### eval-linalg-009 高等代数 · 矩阵
**题目** 用分块方法计算 $M=\begin{pmatrix}2&1&1\\1&2&1\\0&0&3\end{pmatrix}$ 的行列式。
**答案** $9$
**解法一（分块行列式公式）** 取 $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$，$B=\begin{pmatrix}1\\1\end{pmatrix}$，$C=(3)$，则 $M=\begin{pmatrix}A&B\\0&C\end{pmatrix}$。分块上三角矩阵的行列式 $\det M=\det A\cdot\det C$。$\det A=2\cdot 2-1\cdot 1=3$，$\det C=3$，故 $\det M=3\cdot 3=9$。
**解法二（Laplace 按最后一行展开）** 按第三行展开：$\det M=(-1)^{3+3}\cdot 3\cdot\begin{vmatrix}2&1\\1&2\end{vmatrix}=3\cdot 3=9$（第三行仅第 3 个元素非零）。
**解法三（行变换验证）** 第三行与第一、二行的前两列零块使 $M$ 已是分块上三角。验证：直接用一般公式展开，$\det M=2\cdot\begin{vmatrix}2&1\\0&3\end{vmatrix}-1\cdot\begin{vmatrix}1&1\\0&3\end{vmatrix}+1\cdot\begin{vmatrix}1&2\\0&0\end{vmatrix}=2\cdot 6-1\cdot 3+1\cdot 0=12-3=9$，与分块公式一致。
**思路展开** 分块行列式公式 $\det\begin{pmatrix}A&B\\0&C\end{pmatrix}=\det A\cdot\det C$ 是 Laplace 展开的块版本，处理块结构矩阵时最省力。三种方法分别代表分块、Laplace、直接展开。动画可展示矩阵的分块结构高亮与"上三角块"的零块。
**解法一动画要点** - 分块结构高亮（$A,B,0,C$） - 块上三角与数值上三角的类比
**解法二动画要点** - 按第三行展开的 Laplace 余子式高亮 - $(-1)^{3+3}\cdot3$ 的符号标注
**解法三动画要点** - 按第一行直接展开的三项计算 - 与分块公式结果的对照

### eval-linalg-010 高等代数 · 矩阵
**题目** 求矩阵 $A=\begin{pmatrix}1&1&2\\2&1&3\\1&2&3\end{pmatrix}$ 的秩。
**答案** $2$
**解法一（初等行变换）** $\begin{pmatrix}1&1&2\\2&1&3\\1&2&3\end{pmatrix}\xrightarrow{R_2-2R_1}\begin{pmatrix}1&1&2\\0&-1&-1\\1&2&3\end{pmatrix}\xrightarrow{R_3-R_1}\begin{pmatrix}1&1&2\\0&-1&-1\\0&1&1\end{pmatrix}\xrightarrow{R_3+R_2}\begin{pmatrix}1&1&2\\0&-1&-1\\0&0&0\end{pmatrix}$。非零行数为 2，故 $\operatorname{rank}A=2$。
**解法二（子式法）** $\det A=1\cdot(1\cdot 3-3\cdot 2)-1\cdot(2\cdot 3-3\cdot 1)+2\cdot(2\cdot 2-1\cdot 1)=1\cdot(-3)-1\cdot 3+2\cdot 3=0$，秩小于 3。二阶子式 $\begin{vmatrix}1&1\\2&1\end{vmatrix}=1-2=-1\ne 0$，故秩为 2。
**解法三（列向量组）** 三列 $c_1=(1,2,1)^T$、$c_2=(1,1,2)^T$、$c_3=(2,3,3)^T$ 满足 $c_3=c_1+c_2$（逐分量验证：$1+1=2$，$2+1=3$，$1+2=3$），故 $c_3$ 可由前两列线性表出；$c_1,c_2$ 不成比例，线性无关。列秩 $=2$，即 $\operatorname{rank}A=2$。
**思路展开** 秩的三种算法：行变换（机器算法）、子式（定义判据）、列向量组（几何意义）。本题三列"两独立一冗余"的结构一眼可见。动画可展示三列向量共面（秩 2 意味着张成平面）的几何图像。
**解法一动画要点** - 行变换消元动画 - 非零行数 2 的标注
**解法二动画要点** - 三阶行列式为零与二阶子式 $-1\ne0$ 的高亮 - 秩 2 的判定
**解法三动画要点** - 三列向量共面的三维图 - 列相关关系 $c_3=c_1+c_2$ 的平行四边形

### eval-linalg-011 高等代数 · 线性方程组
**题目** 讨论含参数线性方程组 $\begin{cases}\lambda x+y+z=1\\x+\lambda y+z=\lambda\\x+y+\lambda z=\lambda^2\end{cases}$ 的解的情况。
**答案** $\lambda\ne 1$ 且 $\lambda\ne-2$ 时唯一解；$\lambda=1$ 时无穷多解；$\lambda=-2$ 时无解
**解法一（行列式判别法）** 系数行列式 $D=\begin{vmatrix}\lambda&1&1\\1&\lambda&1\\1&1&\lambda\end{vmatrix}$。该矩阵 $=(\lambda-1)I+J$（$J$ 全 1 矩阵），特征值为 $(\lambda-1)+3=\lambda+2$ 与 $\lambda-1$（二重），故 $D=(\lambda+2)(\lambda-1)^2$。当 $\lambda\ne 1,-2$ 时 $D\ne 0$，由 Cramer 法则有唯一解。当 $\lambda=1$：三个方程均为 $x+y+z=1$，无穷多解（解空间二维）。当 $\lambda=-2$：三式相加得 $0\cdot(x+y+z)=1+(-2)+4=3$，即 $0=3$，矛盾，无解。
**解法二（高斯消元）** 增广矩阵 $\begin{pmatrix}\lambda&1&1&1\\1&\lambda&1&\lambda\\1&1&\lambda&\lambda^2\end{pmatrix}$。交换第一、三行后消元：$\begin{pmatrix}1&1&\lambda&\lambda^2\\0&\lambda-1&1-\lambda&\lambda-\lambda^2\\0&1-\lambda&1-\lambda^2&1-\lambda^3\end{pmatrix}$。当 $\lambda\ne 1$：第二行除以 $\lambda-1$ 得 $\begin{pmatrix}1&1&\lambda&\lambda^2\\0&1&-1&-\lambda\\0&1-\lambda&1-\lambda^2&1-\lambda^3\end{pmatrix}$，第三行减第二行的 $(1-\lambda)$ 倍，其首项系数为 $(1-\lambda^2)+(1-\lambda)=2-\lambda-\lambda^2=(\lambda+2)(1-\lambda)\cdot\ldots$，最终当 $\lambda=-2$ 时出现 $0=3$ 型矛盾行（无解），其余 $\lambda\ne 1$ 时有唯一解；$\lambda=1$ 时三行相同，无穷多解。
**解法三（几何观点）** 三个方程代表三个平面。$\lambda=1$ 时三平面重合（$x+y+z=1$）；$\lambda=-2$ 时三平面两两相交但三交线平行（法向量和为零向量导致矛盾）；其余情形三平面交于一点（唯一解）。
**思路展开** 含参方程组讨论是"系数行列式、消元、几何"三件套的汇合。行列式判别法利用对称矩阵的谱结构一步写出 $D$，消元法给出普适流程，几何法提供形象对照。动画可用 $\lambda$ 滑块展示三平面从交于一点到重合、再到无公共点的连续变化。
**解法一动画要点** - 行列式 $D=(\lambda+2)(\lambda-1)^2$ 的零点标注 - 三种情形的分屏对照
**解法二动画要点** - 增广矩阵行变换的逐步动画 - 矛盾行 $0=3$ 的高亮
**解法三动画要点** - $\lambda$ 滑块下三平面的位置变化 - 重合/交于一点/无公共点的三种几何

### eval-linalg-012 高等代数 · 线性方程组
**题目** 求参数 $a$ 使齐次线性方程组 $\begin{cases}ax+y+z=0\\x+ay+z=0\\x+y+az=0\end{cases}$ 有非零解，并求各情形下的解空间。
**答案** $a=1$（解空间二维：$x+y+z=0$）或 $a=-2$（解空间一维：$x=y=z$）
**解法一（行列式为零）** 系数行列式 $D=\begin{vmatrix}a&1&1\\1&a&1\\1&1&a\end{vmatrix}$。矩阵 $=(a-1)I+J$，特征值 $a+2$ 与 $a-1$（二重），故 $D=(a+2)(a-1)^2$。齐次方程组有非零解 $\iff D=0\iff a=1$ 或 $a=-2$。$a=1$：三个方程均为 $x+y+z=0$，解空间为二维平面。$a=-2$：三式相加得 $-2(x+y+z)+2(x+y+z)=0$ 恒等，且 $\begin{cases}-2x+y+z=0\\x-2y+z=0\end{cases}$ 相减得 $x=y$，代回得 $z=x$，解空间为直线 $x=y=z$（一维）。
**解法二（秩与行变换）** $a\ne 1,-2$ 时 $D\ne 0$，秩为 3，只有零解。$a=1$ 时矩阵为全 1 矩阵，秩 1，解空间维数 $3-1=2$。$a=-2$ 时矩阵 $\begin{pmatrix}-2&1&1\\1&-2&1\\1&1&-2\end{pmatrix}$，行变换：第二行减第一行的 $-\dfrac{1}{2}$ 倍……等价地观察任意两行相减得 $\pm 3(x-y)=0$ 型关系，秩为 2，解空间维数 $3-2=1$。
**解法三（特征值观点）** 方程组 $((a-1)I+J)v=0$ 有非零解 $\iff -(a-1)$ 是 $J$ 的特征值。$J$ 的特征值为 $3,0,0$，故 $a-1\in\{-3,0\}$，即 $a=-2$ 或 $a=1$，与解法一一致。$a=-2$ 时解为 $J$ 的特征值 $3$ 对应的特征向量方向 $(1,1,1)^T$；$a=1$ 时解为 $J$ 的零空间（$x+y+z=0$，二维）。
**思路展开** 齐次方程组有非零解⇔系数矩阵降秩⇔行列式为零，三种方法从判别式、消元、谱三个角度切入。解法三把解空间的维数与特征值的重数对应起来，最富结构感。动画可展示参数 $a$ 变化时解空间从"点"到"线"再到"面"的跳变。
**解法一动画要点** - 行列式 $D=(a+2)(a-1)^2$ 的零点标注 - 非零解条件的判定
**解法二动画要点** - 秩随 $a$ 的变化标注 - 解空间维度 $3-r$ 的对应
**解法三动画要点** - 矩阵谱与 $a$ 的关系图 - 解直线/解平面的三维展示

### eval-linalg-013 高等代数 · 线性方程组
**题目** 求齐次线性方程组 $x_1+x_2+x_3+x_4=0$ 的基础解系与通解。
**答案** 基础解系 $\xi_1=(1,-1,0,0)^T$，$\xi_2=(1,0,-1,0)^T$，$\xi_3=(1,0,0,-1)^T$；通解 $x=c_1\xi_1+c_2\xi_2+c_3\xi_3$
**解法一（自由变量法）** 取 $x_2,x_3,x_4$ 为自由变量，$x_1=-x_2-x_3-x_4$。分别令 $(x_2,x_3,x_4)=(1,0,0),(0,1,0),(0,0,1)$，得基础解系 $\xi_1=(-1,1,0,0)^T$，$\xi_2=(-1,0,1,0)^T$，$\xi_3=(-1,0,0,1)^T$（取负号即 $\xi_1=(1,-1,0,0)^T$ 等形式，两者等价）。通解 $x=c_1\xi_1+c_2\xi_2+c_3\xi_3$。
**解法二（正交补观点）** 解空间 $=(\operatorname{span}\{(1,1,1,1)^T\})^\perp$（法向量 $(1,1,1,1)$ 的正交补）。取三个线性无关且与 $(1,1,1,1)$ 正交的向量：$(1,-1,0,0)^T$、$(1,0,-1,0)^T$、$(1,0,0,-1)^T$（逐一点积为 0）。三者线性无关（前三个分量的子矩阵 $\begin{pmatrix}1&-1&0\\1&0&-1\\1&0&0\end{pmatrix}$ 行列式 $1\ne 0$），故构成基础解系。
**解法三（几何观点）** 方程 $x_1+x_2+x_3+x_4=0$ 是 $\mathbb R^4$ 中过原点的三维超平面（法向量 $(1,1,1,1)$）。基础解系即该超平面的一个基，通解是超平面上所有点。维数 $4-1=3$ 与基础解系含 3 个向量一致。
**思路展开** 自由变量法是机械流程，正交补法利用"解空间=法向量正交补"的几何结构，几何法给出维数直觉（$n-r=4-1=3$）。动画可在三维投影中展示超平面与其三个基向量。
**解法一动画要点** - 自由变量 $(x_2,x_3,x_4)$ 的三组赋值 - 三个解向量的生成
**解法二动画要点** - 三个基向量与法向量 $(1,1,1,1)$ 的正交关系 - 线性无关性的行列式验证
**解法三动画要点** - 三维投影中的超平面 - 通解的线性组合扫出平面

### eval-linalg-014 高等代数 · 特征值与特征向量

**题目** 设 $a\in\mathbb R\setminus\{0\}$ 为参数,求矩阵 $A=\begin{pmatrix}1&a&0\\a&1&a\\0&a&1\end{pmatrix}$ 的特征值与特征向量,并求正交矩阵 $Q$,使 $Q^TAQ$ 为对角矩阵。
**答案** 特征值 $1,\ 1+\sqrt{2}a,\ 1-\sqrt{2}a$;对应单位特征向量 $\dfrac{1}{\sqrt{2}}(1,0,-1)^T,\ \dfrac{1}{2}(1,\sqrt{2},1)^T,\ \dfrac{1}{2}(1,-\sqrt{2},1)^T$;$Q=\begin{pmatrix}1/\sqrt{2}&1/2&1/2\\0&\sqrt{2}/2&-\sqrt{2}/2\\-1/\sqrt{2}&1/2&1/2\end{pmatrix}$,$Q^TAQ=\operatorname{diag}(1,\,1+\sqrt{2}a,\,1-\sqrt{2}a)$
**解法一（特征方程）** $|\lambda I-A|=\begin{vmatrix}\lambda-1&-a&0\\-a&\lambda-1&-a\\0&-a&\lambda-1\end{vmatrix}=(\lambda-1)\bigl[(\lambda-1)^2-2a^2\bigr]$,得特征值 $1,\ 1\pm\sqrt{2}a$($a\neq 0$ 时互异)。$\lambda=1$:解 $(A-I)v=0$,即 $\begin{pmatrix}0&a&0\\a&0&a\\0&a&0\end{pmatrix}v=0$,得 $y=0,\ x=-z$,取 $v_1=(1,0,-1)^T$。$\lambda=1+\sqrt{2}a$:由 $(A-(1+\sqrt{2}a)I)v=0$,第一行给 $y=\sqrt{2}x$,第二行给 $x-\sqrt{2}y+z=0$,故 $z=x$,取 $v_2=(1,\sqrt{2},1)^T$。$\lambda=1-\sqrt{2}a$:同理 $y=-\sqrt{2}x,\ z=x$,取 $v_3=(1,-\sqrt{2},1)^T$。三个特征向量两两正交,范数分别为 $\sqrt{2},\ 2,\ 2$;单位化后按列排成 $Q=\begin{pmatrix}1/\sqrt{2}&1/2&1/2\\0&\sqrt{2}/2&-\sqrt{2}/2\\-1/\sqrt{2}&1/2&1/2\end{pmatrix}$。直接验证:$AQ=Q\operatorname{diag}(1,1+\sqrt{2}a,1-\sqrt{2}a)$(逐列即 $Av_i=\lambda_i v_i$),故 $Q^TAQ=\operatorname{diag}(1,\,1+\sqrt{2}a,\,1-\sqrt{2}a)$。
**解法二（对称结构分解）** 先看反对称方向:$A(1,0,-1)^T=(1,0,-1)^T$,故 $v_1=(1,0,-1)^T$ 是特征值 1 的特征向量。其余特征向量在 $v_1$ 的正交补 $\operatorname{span}\{r,s\}$ 内,其中 $r=\dfrac{1}{\sqrt{2}}(1,0,1)^T,\ s=(0,1,0)^T$ 为单位正交基。计算 $A$ 在 $(r,s)$ 上的限制:$Ar=\dfrac{1}{\sqrt{2}}A(1,0,1)^T=\dfrac{1}{\sqrt{2}}(1,2a,1)^T=r+\sqrt{2}a\,s$;$As=A(0,1,0)^T=(a,1,a)^T=\sqrt{2}a\,r+s$。故限制矩阵为 $\begin{pmatrix}1&\sqrt{2}a\\\sqrt{2}a&1\end{pmatrix}$,其特征值为 $1\pm\sqrt{2}a$,对应特征向量 $r\pm s$,即 $v_2=\dfrac{1}{2}(1,\sqrt{2},1)^T$,$v_3=\dfrac{1}{2}(1,-\sqrt{2},1)^T$。三向量两两正交,单位化后按列排成 $Q=\begin{pmatrix}1/\sqrt{2}&1/2&1/2\\0&\sqrt{2}/2&-\sqrt{2}/2\\-1/\sqrt{2}&1/2&1/2\end{pmatrix}$,$Q^TAQ=\operatorname{diag}(1,\,1+\sqrt{2}a,\,1-\sqrt{2}a)$。
**解法三（直接主轴配方）** 二次型 $f(x,y,z)=x^2+y^2+z^2+2a(xy+yz)$。令 $u=\dfrac{x-z}{\sqrt{2}},\ p=\dfrac{x+z}{\sqrt{2}}$,则 $x^2+z^2=u^2+p^2$,$xy+yz=y(x+z)=\sqrt{2}py$,故 $f=u^2+p^2+y^2+2\sqrt{2}a\,py$。再令 $v=\dfrac{p+y}{\sqrt{2}},\ w=\dfrac{p-y}{\sqrt{2}}$,则 $p^2+y^2=v^2+w^2$,$2py=v^2-w^2$,故 $f=u^2+(1+\sqrt{2}a)v^2+(1-\sqrt{2}a)w^2$——三项系数即特征值。由 $(u,v,w)^T=P(x,y,z)^T$ 解出 $P=\begin{pmatrix}1/\sqrt{2}&0&-1/\sqrt{2}\\1/2&\sqrt{2}/2&1/2\\1/2&-\sqrt{2}/2&1/2\end{pmatrix}$,$Q=P^T$ 即为所求正交矩阵。参数分类($f=1$ 等值面):$|a|<\dfrac{\sqrt{2}}{2}$ 时三系数全正,为椭球面;$a=\pm\dfrac{\sqrt{2}}{2}$ 时一个系数为 0,退化为椭圆柱面;$|a|>\dfrac{\sqrt{2}}{2}$ 时一个系数为负,为单叶双曲面。
**思路展开** 按用户难度要求,本题升为**三阶含参**对称矩阵:特征多项式是一元三次式的因式分解,特征向量带 $\sqrt{2}$ 系数——难度中等偏上(二阶留给简单题)。三条解法各自独立:特征方程(代数)、对称结构分解(把 3 阶问题约化为 2 阶限制矩阵)、主轴配方(几何平方和)。$a$ 变化时三个特征值以 1 为中心对称分开,动画可做"$a$ 滑杆"驱动 $f=1$ 等值面在椭球面/椭圆柱面/单叶双曲面之间切换。
**解法一动画要点** - 三阶特征多项式按第一列展开与因式分解 - 三个特征方向上伸缩率 $1,\ 1\pm\sqrt{2}a$ 的标注
**解法二动画要点** - 反对称方向 $v_1$ 先分离、正交补 $r,s$ 上的 2 阶限制 - $r\pm s$ 生成另两个特征方向的动画
**解法三动画要点** - 两次正交替换 $u,p\to v,w$ 的配方动画 - $f=1$ 等值面随 $a$ 的类型切换(椭球/椭圆柱/单叶双曲面)

### eval-linalg-015 高等代数 · 特征值与特征向量
**题目** 求矩阵 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$ 的特征值与特征向量，并将其对角化。
**答案** 特征值 $\lambda_1=3$、$\lambda_2=-1$；特征向量 $(1,1)^T$、$(1,-1)^T$；$P^{-1}AP=\begin{pmatrix}3&0\\0&-1\end{pmatrix}$，其中 $P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$
**解法一（特征方程）** $|\lambda I-A|=\begin{vmatrix}\lambda-1&-2\\-2&\lambda-1\end{vmatrix}=(\lambda-1)^2-4=\lambda^2-2\lambda-3=(\lambda-3)(\lambda+1)$，$\lambda=3,-1$。$\lambda=3$：$(3I-A)v=0$，即 $\begin{pmatrix}2&-2\\-2&2\end{pmatrix}v=0$，$v=(1,1)^T$。$\lambda=-1$：$(-I-A)v=0$，即 $\begin{pmatrix}-2&-2\\-2&-2\end{pmatrix}v=0$，$v=(1,-1)^T$。
**解法二（二次型主轴）** $A$ 对应二次型 $x^2+4xy+y^2$。配方得 $(x+y)^2+2xy\ldots$ 沿 $y=x$ 方向（$u=\dfrac{x+y}{\sqrt2}$）：值为 $3u^2$；沿 $y=-x$ 方向（$v=\dfrac{x-y}{\sqrt2}$）：值为 $-v^2$。故主轴方向 $(1,1)$ 与 $(1,-1)$ 上二次型取值 $3u^2-v^2$，特征值为 $3,-1$。
**解法三（对称矩阵正交对角化）** 归一化特征向量 $q_1=\dfrac{1}{\sqrt2}(1,1)^T$、$q_2=\dfrac{1}{\sqrt2}(1,-1)^T$（自动正交），取 $Q=\dfrac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$（$Q$ 为正交矩阵，$Q^{-1}=Q^T$）。$Q^TAQ=\begin{pmatrix}3&0\\0&-1\end{pmatrix}$，验证：$Q^TAQ=\dfrac{1}{2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}\begin{pmatrix}1&2\\2&1\end{pmatrix}\begin{pmatrix}1&1\\1&-1\end{pmatrix}=\dfrac{1}{2}\begin{pmatrix}3&3\\-1&1\end{pmatrix}\begin{pmatrix}1&1\\1&-1\end{pmatrix}=\dfrac{1}{2}\begin{pmatrix}6&0\\0&-2\end{pmatrix}$。
**思路展开** 对称矩阵的对角化有三种语言：特征方程（代数）、二次型主轴（几何）、正交矩阵（结构）。本题与 eval-linalg-014 的反射矩阵同属"对称+两正交特征方向"家族。动画可展示二次型等值线（双曲线）与主轴方向的对应。
**解法一动画要点** - 特征方程 $(\lambda-3)(\lambda+1)=0$ 的求解 - 特征向量的拉伸（3 倍与反向）
**解法二动画要点** - 二次型 $x^2+4xy+y^2$ 的等值线与主轴 - 主轴方向取值的标注
**解法三动画要点** - 正交矩阵 $Q$ 的旋转作用 - $Q^TAQ=\operatorname{diag}(3,-1)$ 的矩阵运算

### eval-linalg-016 高等代数 · 特征值与特征向量
**题目** 设 $A$ 为二阶方阵，已知 $\operatorname{tr}A=5$、$\det A=6$。求 $A$ 的特征值，并验证 $A^2-5A+6I=0$。
**答案** 特征值为 $2$ 与 $3$；$A^2-5A+6I=0$ 成立
**解法一（迹与行列式）** 特征多项式 $|\lambda I-A|=\lambda^2-(\operatorname{tr}A)\lambda+\det A=\lambda^2-5\lambda+6=(\lambda-2)(\lambda-3)$，特征值为 $2,3$。
**解法二（Cayley–Hamilton 定理）** 由特征多项式 $p(\lambda)=\lambda^2-5\lambda+6$，Cayley–Hamilton 定理给出 $p(A)=A^2-5A+6I=0$。验证特例 $A=\begin{pmatrix}2&1\\0&3\end{pmatrix}$（$\operatorname{tr}=5$、$\det=6$）：$A^2=\begin{pmatrix}4&5\\0&9\end{pmatrix}$，$A^2-5A+6I=\begin{pmatrix}4-10+6&5-5\\0&9-15+6\end{pmatrix}=0$。
**解法三（对角化验证 C–H）** 迹与行列式是相似不变量，特征值由迹与行列式唯一确定为 $2,3$。由两个不同特征值知 $A$ 可对角化（最小多项式 $(\lambda-2)(\lambda-3)$ 无重根），即 $A=P\operatorname{diag}(2,3)P^{-1}$。于是 $A^2-5A+6I=P\left(\operatorname{diag}(4,9)-5\operatorname{diag}(2,3)+6I\right)P^{-1}=P\cdot 0\cdot P^{-1}=0$，与解法二一致。
**思路展开** 二阶方阵的特征值完全由迹与行列式决定（特征多项式系数），Cayley–Hamilton 定理进一步把"特征值满足的方程"提升为"矩阵自身满足的方程"。动画可展示 $A^2-5A+6I$ 的逐项计算归零。
**解法一动画要点** - 特征多项式 $\lambda^2-5\lambda+6$ 系数与迹、行列式的对应 - 因式分解 $(\lambda-2)(\lambda-3)$
**解法二动画要点** - Cayley–Hamilton 定理的陈述 - 特例 $\begin{pmatrix}2&1\\0&3\end{pmatrix}$ 的 $A^2-5A+6I=0$ 矩阵运算动画
**解法三动画要点** - 对角化 $P\operatorname{diag}(2,3)P^{-1}$ 代入验证 - 相似矩阵共享谱的示意

### eval-linalg-017 高等代数 · 特征值与特征向量
**题目** 求矩阵 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 的特征值与特征向量，并判断其是否可对角化。
**答案** 特征值 $\lambda=1$（二重），非零特征向量 $t(1,0)^T$（$t\ne 0$，特征空间连同零向量为一维）；不可对角化，若尔当标准形为 $\begin{pmatrix}1&1\\0&1\end{pmatrix}$
**解法一（特征方程+特征空间维数）** $|\lambda I-A|=(\lambda-1)^2=0$，$\lambda=1$（二重）。解 $(I-A)v=0$：$I-A=\begin{pmatrix}0&-1\\0&0\end{pmatrix}$，$\begin{pmatrix}0&-1\\0&0\end{pmatrix}\begin{pmatrix}x\\y\end{pmatrix}=0$ 得 $y=0$，特征空间 $\operatorname{span}\{(1,0)^T\}$ 仅一维（非零特征向量为 $t(1,0)^T$，$t\ne 0$）。特征空间维数 $1<$ 代数重数 $2$，故不可对角化。
**解法二（几何剪切）** $A$ 是水平剪切变换：$(x,y)\mapsto(x+y,y)$。所有向量的 $y$ 分量不变，仅 $(t,0)^T$（水平方向）方向不变，其余向量方向都被"推斜"。剪切没有第二个不变方向，故只有一个特征方向，不可对角化。
**解法三（最小多项式）** $A-I=\begin{pmatrix}0&1\\0&0\end{pmatrix}\ne 0$，$(A-I)^2=0$，故最小多项式为 $m(\lambda)=(\lambda-1)^2$，含有重因子 $(\lambda-1)^2$。矩阵可对角化 $\iff$ 最小多项式无重根，故 $A$ 不可对角化；其若尔当标准形为单个二阶块 $J_2(1)=\begin{pmatrix}1&1\\0&1\end{pmatrix}$。
**思路展开** 本题是"重特征值未必可对角化"的标准反例：可对角化的判据有三（特征空间维数=重数、几何剪切直觉、最小多项式无重根）。三种判据一一对应。动画可展示剪切变换下网格变形，只有水平线方向保持。
**解法一动画要点** - 特征方程 $(\lambda-1)^2=0$ 的求解 - $I-A=\begin{pmatrix}0&-1\\0&0\end{pmatrix}$ 的核空间一维标注
**解法二动画要点** - 剪切变换的网格变形 - 唯一不变方向（水平）高亮
**解法三动画要点** - 最小多项式 $(\lambda-1)^2$ 有重因子的标注 - 与对角矩阵 $\operatorname{diag}(1,1)=I$ 的对照

### eval-linalg-018 高等代数 · 特征值与特征向量
**题目** 设 $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$，求 $A^{100}$。
**答案** $A^{100}=\dfrac{1}{2}\begin{pmatrix}3^{100}+1&3^{100}-1\\3^{100}-1&3^{100}+1\end{pmatrix}$
**解法一（对角化）** 特征方程 $(\lambda-2)^2-1=0$，特征值 $3,1$；对应特征向量 $(1,1)^T$、$(1,-1)^T$。取 $P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$（即 eval-linalg-015 的结论），则 $P^{-1}AP=\begin{pmatrix}3&0\\0&1\end{pmatrix}$，且 $P^{-1}=\dfrac{1}{2}P$（因 $P^2=2I$）。故 $A^{100}=P\begin{pmatrix}3^{100}&0\\0&1\end{pmatrix}P^{-1}=\dfrac{1}{2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}\begin{pmatrix}3^{100}&0\\0&1\end{pmatrix}\begin{pmatrix}1&1\\1&-1\end{pmatrix}=\dfrac{1}{2}\begin{pmatrix}3^{100}&1\\3^{100}&-1\end{pmatrix}\begin{pmatrix}1&1\\1&-1\end{pmatrix}=\dfrac{1}{2}\begin{pmatrix}3^{100}+1&3^{100}-1\\3^{100}-1&3^{100}+1\end{pmatrix}$。
**解法二（二项式展开）** $A=I+B$，其中 $B=\begin{pmatrix}1&1\\1&1\end{pmatrix}$，且 $B^2=2B$（验证：$B^2=\begin{pmatrix}2&2\\2&2\end{pmatrix}=2B$）。于是 $B^k=2^{k-1}B$（$k\ge 1$）。$A^{100}=(I+B)^{100}=I+\displaystyle\sum_{k=1}^{100}\binom{100}{k}2^{k-1}B=I+\dfrac{3^{100}-1}{2}B$（其中 $\displaystyle\sum_{k=1}^{100}\binom{100}{k}2^{k}=3^{100}-1$，除以 $2$ 即得）。代入 $B$：$A^{100}=\begin{pmatrix}1+\frac{3^{100}-1}{2}&\frac{3^{100}-1}{2}\\\frac{3^{100}-1}{2}&1+\frac{3^{100}-1}{2}\end{pmatrix}=\dfrac{1}{2}\begin{pmatrix}3^{100}+1&3^{100}-1\\3^{100}-1&3^{100}+1\end{pmatrix}$。
**解法三（Cayley–Hamilton 递推）** 特征多项式 $\lambda^2-4\lambda+3$，由 C–H 定理 $A^2=4A-3I$。设 $A^n=u_nA+v_nI$，则 $A^{n+1}=A^nA=(u_nA+v_nI)A=u_nA^2+v_nA=u_n(4A-3I)+v_nA=(4u_n+v_n)A-3u_nI$，故 $u_{n+1}=4u_n+v_n$、$v_{n+1}=-3u_n$，初值 $u_1=1$、$v_1=0$。由 $v_n=-3u_{n-1}$（$n\ge 2$）代入第一式得 $u_{n+1}=4u_n-3u_{n-1}$，即 $u_{n+1}-u_n=3(u_n-u_{n-1})$；又 $u_2-u_1=3$，故 $u_n-u_{n-1}=3^{n-1}$，$u_n=1+\displaystyle\sum_{k=2}^{n}3^{k-1}=1+3\cdot\dfrac{3^{n-1}-1}{2}=\dfrac{3^n-1}{2}$，$v_n=-3u_{n-1}=-\dfrac{3^n-3}{2}$。$A^{100}=\dfrac{3^{100}-1}{2}A-\dfrac{3^{100}-3}{2}I=\dfrac{1}{2}\begin{pmatrix}3^{100}+1&3^{100}-1\\3^{100}-1&3^{100}+1\end{pmatrix}$。
**思路展开** 对角化法是通法；二项式法利用 $B^2=2B$ 的特殊结构把 100 次幂压缩成一次线性组合；C–H 递推把矩阵幂化为标量递推。三种方法给出同一结果，互相印证。动画可展示特征方向上拉伸 $3^{100}$ 倍与保持不变的分解。
**解法一动画要点** - 特征方向分解：$3^{100}$ 倍拉伸与 $1$ 倍保持 - 对角化三连乘的矩阵运算
**解法二动画要点** - $B^2=2B$ 的结构示意 - 二项式展开系数 $\dfrac{3^{100}-1}{2}$ 的推导
**解法三动画要点** - C–H 递推 $u_{n+1}=4u_n-3u_{n-1}$ 的点列 - 三种方法的同框结果验证

### eval-linalg-019 高等代数 · 二次型

**题目** 设 $a\in\mathbb R$ 为参数,将二次型 $f(x,y,z)=x^2+2y^2+az^2+2xy+2xz$ 化为标准形,并讨论 $a$ 取何值时 $f$ 正定。
**答案** $f=(x+y+z)^2+(y-z)^2+(a-2)z^2$;$f$ 正定当且仅当 $a>2$
**解法一（配方法）** 先按含 $x$ 的项配方:$(x+y+z)^2=x^2+y^2+z^2+2xy+2xz+2yz$,故 $f=(x+y+z)^2+(y^2-2yz+(a-1)z^2)$。再对 $y$ 配方:$(y-z)^2=y^2-2yz+z^2$,得 $f=(x+y+z)^2+(y-z)^2+(a-2)z^2$。若 $a>2$,三项系数全正,且 $(x+y+z,y-z,z)=(0,0,0)$ 推出 $x=y=z=0$,故 $f>0$($(x,y,z)\neq(0,0,0)$)。若 $a\le 2$,取 $x+y+z=0,\ y=z$ 的非零解(如 $(x,y,z)=(-2,1,1)$),此时前两项为 0、第三项 $\le 0$,$f$ 不正定。
**解法二（合同变换）** $f$ 的矩阵 $A=\begin{pmatrix}1&1&1\\1&2&0\\1&0&a\end{pmatrix}$。作合同变换(行列同步):第一步,第二、三行分别减去第一行,第二、三列分别减去第一列,得 $\begin{pmatrix}1&0&0\\0&1&-1\\0&-1&a-1\end{pmatrix}$;第二步,第三行加上第二行、第三列加上第二列,得 $\operatorname{diag}(1,1,a-2)$。两步对应的列变换矩阵累计为 $C=\begin{pmatrix}1&-1&-2\\0&1&1\\0&0&1\end{pmatrix}$,满足 $C^TAC=\operatorname{diag}(1,1,a-2)$。对应新变量 $u=x+y+z,\ v=y-z,\ w=z$(即 $(x,y,z)^T=C(u,v,w)^T$),标准形为 $u^2+v^2+(a-2)w^2$。合同保持正定性,故 $f$ 正定 $\iff$ 对角元全正 $\iff a>2$。
**解法三（LDLᵀ 分解）** $f$ 的矩阵 $A$ 可作 $LDL^T$ 分解: $$A=L\operatorname{diag}(1,1,a-2)L^T,\qquad L=\begin{pmatrix}1&0&0\\1&1&0\\1&-1&1\end{pmatrix}.$$ (直接乘开验证:行列为 $1,2,0$ 与 $1,0,a$ 的交叉项分别由 $L$ 的第 2、3 行生成。)令 $(u,v,w)^T=L^T(x,y,z)^T$,得新变量 $u=x+y+z,\ v=y-z,\ w=z$,于是 $$f=(x,y,z)A(x,y,z)^T=(L^T(x,y,z)^T)^T\operatorname{diag}(1,1,a-2)(L^T(x,y,z)^T)=u^2+v^2+(a-2)w^2,$$ 即标准形为 $u^2+v^2+(a-2)w^2$。再由顺序主子式($\Delta_1=1,\Delta_2=1,\Delta_3=|A|=a-2$),$f$ 正定 $\iff\Delta_3>0\iff a>2$——本条解法独立完成"化标准形+判正定"两问。边界 $a=2$ 时标准形第三项系数为 0,$f=u^2+v^2$ 半正定,零空间为 $u=v=0$,即 $x+y+z=0,\ y=z$,也就是 $t(-2,1,1)$。
**思路展开** 原题 019(二元二次型配标准形)与 train 仅差一个系数,本题升维为**三元含参**:参数只出现在标准形第三项系数 $a-2$,正定边界 $a=2$ 是一个清晰的教学阈值。三解法给出三种判正定的语言——配方(显式平方和)、合同(矩阵语言,含变换矩阵累计)、主子式(行列式语言);动画可展示 $a$ 滑杆下 $z^2$ 系数由负转正、$a=2$ 处 $f=1$ 等值面由双曲类退化为椭圆柱面的临界切换。
**解法一动画要点** - 配方过程逐项高亮:先 $(x+y+z)^2$ 再 $(y-z)^2$ - $a$ 滑杆下 $z^2$ 系数由负转正(a=2 为临界)
**解法二动画要点** - 合同初等变换的行列同步消去两步动画 - 变换矩阵 $C$ 的累计与 $C^TAC=\operatorname{diag}(1,1,a-2)$ 验证
**解法三动画要点** - $LDL^T$ 分解的三角因子展示 - 主子式 $\Delta_3=a-2$ 随 $a$ 的符号变化与正定/半正定/不定三区标注

### eval-linalg-020 高等代数 · 二次型
**题目** 判断二次型 $f(x,y)=x^2-4xy+4y^2$ 的类型（正定/半正定/不定/负定）。
**答案** 半正定，秩为 1，正惯性指数 1、负惯性指数 0
**解法一（配方法）** $f=x^2-4xy+4y^2=(x-2y)^2\ge 0$ 对一切 $(x,y)$ 成立，且 $x=2y$（如 $(2,1)$）时取到 0，故半正定。标准形为 $u^2$（$u=x-2y$），秩为 1。
**解法二（矩阵特征值）** 矩阵 $A=\begin{pmatrix}1&-2\\-2&4\end{pmatrix}$。特征方程 $\lambda^2-5\lambda=0$，特征值 $\lambda_1=5$、$\lambda_2=0$。特征值非负且含 0，故半正定，秩 $=$ 非零特征值个数 $=1$。
**解法三（几何观点）** $f=0\iff x=2y$，即一条过原点的直线；$f>0$ 对其余所有点成立。等值线族 $f=k$（$k>0$）是平行直线对 $x-2y=\pm\sqrt{k}$（两条直线）。这对应"退化椭圆"的极限情形，故半正定秩 1。
**思路展开** 半正定二次型的判别路径与正定相同，但需注意"取零"的方向（$x=2y$ 直线）。特征值含 0 对应矩阵降秩，几何上等值面从椭圆族退化为平行直线对。动画可展示等值线族与零方向。
**解法一动画要点** - 配方 $(x-2y)^2$ 的逐步动画 - 零方向 $x=2y$ 高亮
**解法二动画要点** - 特征值 $5,0$ 的谱标注 - 半正定的判定
**解法三动画要点** - 平行直线对等值线族 - 退化椭圆的极限示意

### eval-linalg-021 高等代数 · 二次型

**题目** 设 $a\in\mathbb R$ 为参数,求使二次型 $f(x,y,z)=2x^2+y^2+2z^2+2xy+2axz$ 正定的 $a$ 的取值范围。
**答案** $-\sqrt{2}<a<\sqrt{2}$
**解法一（顺序主子式）** $f$ 的矩阵 $A=\begin{pmatrix}2&1&a\\1&1&0\\a&0&2\end{pmatrix}$。顺序主子式:$\Delta_1=2>0$,$\Delta_2=\begin{vmatrix}2&1\\1&1\end{vmatrix}=1>0$,$\Delta_3=|A|=2\cdot\begin{vmatrix}1&0\\0&2\end{vmatrix}-1\cdot\begin{vmatrix}1&0\\a&2\end{vmatrix}+a\cdot\begin{vmatrix}1&1\\a&0\end{vmatrix}=4-2-a^2=2-a^2$。$f$ 正定 $\iff\Delta_3>0\iff 2-a^2>0\iff -\sqrt{2}<a<\sqrt{2}$。
**解法二（配方）** $2\left(x+\dfrac{y}{2}+\dfrac{az}{2}\right)^2=2x^2+\dfrac{y^2}{2}+\dfrac{a^2z^2}{2}+2xy+2axz+ayz$,故 $$f=2\left(x+\frac{y}{2}+\frac{az}{2}\right)^2+\left[\frac{y^2}{2}-ayz+\left(2-\frac{a^2}{2}\right)z^2\right]=2\left(x+\frac{y}{2}+\frac{az}{2}\right)^2+\frac{1}{2}(y-az)^2+(2-a^2)z^2.$$ 三项系数 $2,\ \dfrac{1}{2},\ 2-a^2$ 全正 $\iff 2-a^2>0\iff |a|<\sqrt{2}$,与解法一一致。
**解法三（Schur 补）** 把 $A$ 分块为 $\begin{pmatrix}B&c\\c^T&2\end{pmatrix}$,其中 $B=\begin{pmatrix}2&1\\1&1\end{pmatrix}$,$c=(a,0)^T$。$B$ 正定($2>0$ 且 $|B|=1>0$),由 Schur 补判据,$A$ 正定 $\iff$ $B$ 正定且 $S=2-c^TB^{-1}c>0$。$B^{-1}=\begin{pmatrix}1&-1\\-1&2\end{pmatrix}$,$c^TB^{-1}c=(a,0)\begin{pmatrix}1&-1\\-1&2\end{pmatrix}\begin{pmatrix}a\\0\end{pmatrix}=a^2$,故 $S=2-a^2$。于是 $f$ 正定 $\iff 2-a^2>0\iff -\sqrt{2}<a<\sqrt{2}$,与前两法独立得到同一范围。
**思路展开** 原题 021(固定系数正定判断)与 train 仅差一个 $4yz$ 项,本题整体改系数并去掉 $yz$ 交叉项,改成**参数范围问题**:答案是对称区间 $(-\sqrt{2},\sqrt{2})$,三方法(主子式、配方、Schur 补)互相独立、殊途同归。临界曲面说明:固定等值面 $f=1$,当 $|a|<\sqrt{2}$ 时为椭球面,$|a|=\sqrt{2}$ 时退化为**椭圆柱面**(沿零方向 $(-a,a,1)^T$ 不变,覆盖 $a=\pm\sqrt{2}$ 两个端点),$|a|>\sqrt{2}$ 时为单叶双曲面。端点处零方向验证:$(x,y,z)=(-a,a,1)$ 时 $y-az=a-a=0$,且 $x+\dfrac{y}{2}+\dfrac{az}{2}=-a+\dfrac{a}{2}+\dfrac{a}{2}=0$,两项同时为零;当 $a=\pm\sqrt{2}$ 时 $2-a^2=0$,故 $f=0$。
**解法一动画要点** - $\Delta_3(a)=2-a^2$ 的抛物线图与正区间 $(-\sqrt2,\sqrt2)$ 标注 - 主子式序列随 $a$ 变化
**解法二动画要点** - 含参配方逐步展开 - 系数 $2-a^2$ 的符号区间
**解法三动画要点** - $2\times2$ 块 $B$ 与 Schur 补 $S=2-a^2$ 的分块标注 - 等值面 $f=1$ 随 $a$ 的类型切换(椭球/椭圆柱/单叶双曲面)

### eval-linalg-022 高等代数 · 多项式
**题目** 将多项式 $f(x)=x^4+2x^3-7x^2-8x+12$ 因式分解。
**答案** $(x-1)(x-2)(x+2)(x+3)$
**解法一（有理根定理）** 常数项 $12$ 与首项系数 $1$，可能的有理根为 $\pm1,\pm2,\pm3,\pm4,\pm6,\pm12$。逐一代入：$f(1)=1+2-7-8+12=0$；$f(2)=16+16-28-16+12=0$；$f(-2)=16-16-28+16+12=0$；$f(-3)=81-54-63+24+12=0$。四次多项式有四个根 $1,2,-2,-3$，故 $f=(x-1)(x-2)(x+2)(x+3)$。
**解法二（待定系数法）** 设 $f=(x^2+ax+b)(x^2+cx+d)$，展开比对：$a+c=2$，$b+d+ac=-7$，$ad+bc=-8$，$bd=12$。试 $b=-2$、$d=-6$（$bd=12$）：则 $b+d=-8$，$ac=-7+8=1$；结合 $a+c=2$、$ac=1$ 得 $a=c=1$。检验 $ad+bc=1\cdot(-6)+1\cdot(-2)=-8$，全部吻合。故 $f=(x^2+x-2)(x^2+x-6)=(x-1)(x+2)(x-2)(x+3)$。
**解法三（综合除法逐步降次）** 由 $f(1)=0$，用综合除法除以 $x-1$：系数 $1,2,-7,-8,12$ 依次得商系数 $1,3,-4,-12$（即 $x^3+3x^2-4x-12$），余 0。检验 $g(2)=8+12-8-12=0$，再除以 $x-2$ 得 $x^2+5x+6$。最后 $x^2+5x+6=(x+2)(x+3)$。故 $f=(x-1)(x-2)(x+2)(x+3)$。
**思路展开** 有理根定理是整数系数多项式分解的第一工具（配合试根），待定系数法适合"分组分解"的结构，综合除法把逐步降次流程化。动画可展示多项式曲线与四个根的位置、综合除法竖式的逐步过程。
**解法一动画要点** - 有理根候选 $\pm1,\pm2,\pm3,\pm4,\pm6,\pm12$ 的逐一试根 - 曲线 $y=f(x)$ 与四个实根
**解法二动画要点** - 待定系数 $(x^2+ax+b)(x^2+cx+d)$ 展开比对 - 四元方程组的求解
**解法三动画要点** - 综合除法竖式动画 - 四次降次的过程与四个因式的连线

### eval-linalg-023 高等代数 · 多项式
**题目** 分别在复数域与实数域上分解 $x^8-1$。
**答案** 复数域：$\displaystyle\prod_{k=0}^{7}\left(x-e^{2\pi ik/8}\right)$；实数域（完整实不可约分解）：$(x-1)(x+1)(x^2+1)(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)$
**解法一（单位根）** $x^8-1=0$ 的根是 8 次单位根 $e^{2\pi ik/8}$（$k=0,1,\dots,7$），在复平面上构成正八边形的顶点。复数域上 $x^8-1=\displaystyle\prod_{k=0}^{7}\left(x-e^{2\pi ik/8}\right)$。实数域上把共轭根配对：$k=0,4$ 对应实根 $\pm 1$；$k=1,7$ 配对得 $\left(x-e^{i\pi/4}\right)\left(x-e^{-i\pi/4}\right)=x^2-2x\cos\dfrac{\pi}{4}+1=x^2-\sqrt2x+1$；$k=2,6$ 配对得 $x^2+1$；$k=3,5$ 配对得 $x^2+\sqrt2x+1$。故实数域分解为 $(x-1)(x+1)(x^2-\sqrt2x+1)(x^2+1)(x^2+\sqrt2x+1)$。
**解法二（平方差递推）** $x^8-1=(x^4-1)(x^4+1)=(x^2-1)(x^2+1)(x^4+1)=(x-1)(x+1)(x^2+1)(x^4+1)$。再对 $x^4+1$ 作实分解（见解法三的恒等式）：$x^4+1=(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)$，合并得完整实不可约分解 $(x-1)(x+1)(x^2+1)(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)$。
**解法三（两种实数分解的联系）** 本题复数域分解为 $\displaystyle\prod_{k=0}^{7}\left(x-e^{2\pi ik/8}\right)$（8 次单位根）。实数域分解有两种书写形式。形式一（按共轭根配对，完整实不可约分解）：$x^8-1=(x-1)(x+1)(x^2-\sqrt2x+1)(x^2+1)(x^2+\sqrt2x+1)$。形式二（按平方差递推，尚未完全分解）：$x^8-1=(x-1)(x+1)(x^2+1)(x^4+1)$。两形式由恒等式 $(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)=x^4+1$ 连接，其证明是平方差：$(x^2+1)^2-(\sqrt2x)^2=x^4+2x^2+1-2x^2=x^4+1$。故形式二是形式一的合并书写，形式一才是完整实不可约分解。
**思路展开** 单位根分解展示代数基本定理的几何画面（正八边形），平方差递推是初等快速路径，配对法给出"不可约实因子"的一般程序。动画可在复平面上画 8 个单位根及其共轭配对。
**解法一动画要点** - 复平面正八边形单位根 - 共轭根配对的动画
**解法二动画要点** - 平方差递推的分解树 $(x^4-1)(x^4+1)\to\cdots$ - 继续分解 $x^4+1$ 的恒等式标注
**解法三动画要点** - 恒等式 $(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)=x^4+1$ 的展开验证 - 两种实数分解的连线对照

### eval-linalg-024 高等代数 · 多项式
**题目** 将多项式 $f(x)=x^3-7x+6$ 按 $x-1$ 的幂展开（即求 $f$ 在 $x=1$ 处的泰勒展开）。
**答案** $f(x)=(x-1)^3+3(x-1)^2-4(x-1)$
**解法一（泰勒公式）** $f(1)=1-7+6=0$；$f'(x)=3x^2-7$，$f'(1)=-4$；$f''(x)=6x$，$f''(1)=6$；$f'''(x)=6$，$f'''(1)=6$。由泰勒公式 $f(x)=f(1)+f'(1)(x-1)+\dfrac{f''(1)}{2}(x-1)^2+\dfrac{f'''(1)}{6}(x-1)^3=0-4(x-1)+3(x-1)^2+(x-1)^3$。
**解法二（综合除法连除）** 对系数 $1,0,-7,6$ 反复除以 $x-1$。第一次：商系数 $1,1,-6$，余 $0$；第二次：商 $1,2$，余 $-4$；第三次：商 $1$，余 $3$。由 $f=(x-1)q_1+r_1$，$q_1=(x-1)q_2+r_2$，$q_2=(x-1)q_3+r_3$，得 $f=(x-1)[(x-1)[(x-1)\cdot 1+3]-4]=(x-1)^3+3(x-1)^2-4(x-1)$。
**解法三（换元展开）** 令 $y=x-1$，则 $x=y+1$。$f=(y+1)^3-7(y+1)+6=y^3+3y^2+3y+1-7y-7+6=y^3+3y^2-4y$。代回 $y=x-1$ 得 $f=(x-1)^3+3(x-1)^2-4(x-1)$。
**思路展开** 泰勒公式、综合除法、换元是"按 $x-a$ 展开"的三条等价路径；展开式系数 $\{0,-4,3,1\}$ 即 $f$ 在 $x=1$ 的各阶导数除以阶乘。动画可展示曲线 $y=f(x)$ 与它在 $x=1$ 处的各阶切触（注意 $f(1)=0$，展开点在 $x$ 轴上）。
**解法一动画要点** - 各阶导数值 $0,-4,6,6$ 的逐项代入 - 泰勒展开式的生成
**解法二动画要点** - 综合除法连除的三次竖式 - 余数 $0,-4,3$ 的提取
**解法三动画要点** - 换元 $y=x-1$ 的展开动画 - 曲线与展开点 $(1,0)$

### eval-linalg-025 高等代数 · 多项式
**题目** 设 $f(x)=x^5+x+1$。求 $f(x)$ 除以 $x-1$ 的余式，以及除以 $x^2+1$ 的余式。
**答案** 除以 $x-1$ 余 $3$；除以 $x^2+1$ 余 $2x+1$
**解法一（余数定理）** 除以 $x-1$ 的余式为 $f(1)=1+1+1=3$。除以二次式 $x^2+1$ 设余式为 $ax+b$，由 $x^2+1$ 的根 $x=i$（虚数单位）：$f(i)=i^5+i+1$，而 $i^4=1$ 故 $i^5=i$，得 $f(i)=2i+1$。余式在 $x=i$ 处的值 $ai+b$ 应等于 $f(i)$：$ai+b=2i+1$，故 $a=2$、$b=1$，余式为 $2x+1$。
**解法二（长除法）** 除以 $x^2+1$：$x^5+x+1$ 中，$x^5$ 与 $x$ 各含 $x^2+1$ 的分解：$x^5=x^3(x^2+1)-x^3$，$x^3=x(x^2+1)-x$，故 $x^5+x+1=x^3(x^2+1)-x(x^2+1)+x+x+1=(x^2+1)(x^3-x)+(2x+1)$，余式 $2x+1$。除以 $x-1$：$x^5+x+1=(x-1)q+3$ 由余数定理直接得余 $3$（商 $q=x^4+x^3+x^2+x+2$，验证 $f(1)=3$）。
**解法三（待定余式验证）** 设除以 $x^2+1$ 的余式为 $ax+b$，则 $f(x)=(x^2+1)q(x)+ax+b$。取 $x=i$ 与 $x=-i$：$f(i)=1+2i$（同解法一），$f(-i)=(-i)^5-i+1=-i-i+1=1-2i$。解 $\begin{cases}ai+b=1+2i\\-ai+b=1-2i\end{cases}$，相加得 $2b=2$、$b=1$；相减得 $2ai=4i$、$a=2$。余式 $2x+1$。
**思路展开** 余数定理把"除法求余"转化为"代入求值"；复数代入法对二次因子（无实根）尤其高效。三种方法（代入、长除、待定）覆盖多项式除法的全部套路。动画可展示长除法竖式的降次过程。
**解法一动画要点** - 余数定理代入 $f(1)=3$ 的标注 - 二次余式 $ax+b$ 的设定
**解法二动画要点** - 长除法竖式动画 - 商 $x^3-x$ 与余式 $2x+1$ 的提取
**解法三动画要点** - 复平面 $x=\pm i$ 代入 - 方程组 $ai+b=1+2i$ 的求解

### eval-linalg-026 高等代数 · 线性空间
**题目** 判断向量组 $\alpha_1=(1,2,3)$，$\alpha_2=(2,3,1)$，$\alpha_3=(3,1,2)$ 是否线性相关。
**答案** 线性无关
**解法一（行列式）** 以三向量为行（或列）的行列式 $D=\begin{vmatrix}1&2&3\\2&3&1\\3&1&2\end{vmatrix}=1\cdot(3\cdot 2-1\cdot 1)-2\cdot(2\cdot 2-1\cdot 3)+3\cdot(2\cdot 1-3\cdot 3)=1\cdot 5-2\cdot 1+3\cdot(-7)=5-2-21=-18\ne 0$。行列式非零，故三向量线性无关。
**解法二（定义解方程组）** 设 $k_1\alpha_1+k_2\alpha_2+k_3\alpha_3=0$，即 $\begin{cases}k_1+2k_2+3k_3=0\\2k_1+3k_2+k_3=0\\3k_1+k_2+2k_3=0\end{cases}$。由第一式 $k_1=-2k_2-3k_3$，代入第二式：$2(-2k_2-3k_3)+3k_2+k_3=0$，即 $-k_2-5k_3=0$，$k_2=-5k_3$；代入第三式：$3(-2k_2-3k_3)+k_2+2k_3=0$，即 $-5k_2-7k_3=0$，代入 $k_2=-5k_3$ 得 $25k_3-7k_3=18k_3=0$，$k_3=0$，进而 $k_2=0$、$k_1=0$。只有零解，线性无关。
**解法三（几何）** 三向量张成的平行六面体体积 $|D|=18\ne 0$，即三向量不共面，故线性无关（线性相关⇔体积为 0）。
**思路展开** 线性相关的三种判据：行列式（体积）、定义（齐次方程组）、几何（共面）。本题三向量"循环轮换"的结构使行列式呈现轮换对称性。动画可展示三向量张成的平行六面体与体积。
**解法一动画要点** - 三阶行列式 $-18$ 的展开计算 - 体积 $|D|=18$ 的标注
**解法二动画要点** - 齐次方程组的逐步代入消元 - 零解唯一性的标注
**解法三动画要点** - 三向量与平行六面体 - 不共面的几何展示

### eval-linalg-027 高等代数 · 线性空间
**题目** 求 $\mathbb R^3$ 中子空间 $W=\operatorname{span}\{(1,1,0),(0,1,1)\}$ 的正交补 $W^\perp$。
**答案** $W^\perp=\operatorname{span}\{(1,-1,1)\}$（一维）
**解法一（解方程组）** $W^\perp=\{(x,y,z):(x,y,z)\cdot(1,1,0)=0,\ (x,y,z)\cdot(0,1,1)=0\}$，即 $\begin{cases}x+y=0\\y+z=0\end{cases}$。由第二式 $z=-y$，第一式 $x=-y$，故 $(x,y,z)=(-y,y,-y)=y(-1,1,-1)$，取 $(1,-1,1)$ 为基，$W^\perp$ 为一维。
**解法二（Gram–Schmidt 扩充）** 把 $\{(1,1,0),(0,1,1)\}$ 扩充为 $\mathbb R^3$ 的正交基：$u_1=(1,1,0)$；$u_2=(0,1,1)-\dfrac{(0,1,1)\cdot(1,1,0)}{2}(1,1,0)=(0,1,1)-\dfrac{1}{2}(1,1,0)=\left(-\dfrac{1}{2},\dfrac{1}{2},1\right)$，取 $(-1,1,2)$。再取 $e_3=(0,0,1)$ 去掉前两者的投影：$u_3=(0,0,1)-0-\dfrac{(0,0,1)\cdot(-1,1,2)}{6}(-1,1,2)=(0,0,1)-\dfrac{1}{3}(-1,1,2)=\left(\dfrac{1}{3},-\dfrac{1}{3},\dfrac{1}{3}\right)$，取 $(1,-1,1)$。它与 $u_1,u_2$ 均正交，故 $W^\perp=\operatorname{span}\{(1,-1,1)\}$。
**解法三（叉积）** $(1,1,0)\times(0,1,1)=(1\cdot 1-0\cdot 1,\ 0\cdot 0-1\cdot 1,\ 1\cdot 1-1\cdot 0)=(1,-1,1)$，与两生成元都垂直，故 $W^\perp=\operatorname{span}\{(1,-1,1)\}$（$\dim W^\perp=3-2=1$）。
**思路展开** 正交补的三种求法：直接解垂直方程组、Gram–Schmidt 扩充、叉积（三维特供）。维数公式 $\dim W+\dim W^\perp=3$ 始终在背后。动画可展示平面 $W$ 与其法线方向 $(1,-1,1)$。
**解法一动画要点** - 垂直方程组 $\begin{cases}x+y=0\\y+z=0\end{cases}$ 的求解 - 解方向 $(-y,y,-y)$ 的标注
**解法二动画要点** - Gram–Schmidt 扩充的投影步骤 - 第三个正交向量 $(1,-1,1)$ 的提取
**解法三动画要点** - 叉积 $(1,1,0)\times(0,1,1)$ 的右手定则 - 平面 $W$ 与法线 $(1,-1,1)$

### eval-linalg-028 高等代数 · 线性空间
**题目** 在 $\mathbb R^2$ 中，求向量 $\alpha=(2,3)$ 在基 $\beta_1=(1,2)$、$\beta_2=(1,1)$ 下的坐标。
**答案** $(1,1)$
**解法一（解方程组）** 设 $\alpha=x_1\beta_1+x_2\beta_2$，即 $\begin{cases}x_1+x_2=2\\2x_1+x_2=3\end{cases}$。两式相减：$x_1=1$，代回得 $x_2=1$。故坐标为 $(1,1)$。
**解法二（过渡矩阵）** 从标准基到基 $\{\beta_1,\beta_2\}$ 的过渡矩阵 $P=\begin{pmatrix}1&1\\2&1\end{pmatrix}$（列为基向量）。$\alpha=P\xi$，其中 $\xi$ 为所求坐标。$P^{-1}=\dfrac{1}{1-2}\begin{pmatrix}1&-1\\-2&1\end{pmatrix}=\begin{pmatrix}-1&1\\2&-1\end{pmatrix}$。故 $\xi=P^{-1}\alpha=\begin{pmatrix}-1&1\\2&-1\end{pmatrix}\begin{pmatrix}2\\3\end{pmatrix}=\begin{pmatrix}-2+3\\4-3\end{pmatrix}=\begin{pmatrix}1\\1\end{pmatrix}$。
**解法三（几何分解）** 在图上作平行四边形：$\alpha=(2,3)$ 可由 $\beta_1+\beta_2=(2,3)$ 一次组合而成（$1\cdot(1,2)+1\cdot(1,1)=(2,3)$），坐标即组合系数 $(1,1)$。
**思路展开** 基变换坐标的三种算法：解方程（定义）、过渡矩阵求逆（机械化）、平行四边形分解（几何）。动画可展示平行四边形分解与坐标网格的斜切。
**解法一动画要点** - 方程组 $\begin{cases}x_1+x_2=2\\2x_1+x_2=3\end{cases}$ 的消元 - 坐标 $(1,1)$ 的标注
**解法二动画要点** - 过渡矩阵 $P=\begin{pmatrix}1&1\\2&1\end{pmatrix}$ 与 $P^{-1}$ 的作用 - 矩阵乘法动画
**解法三动画要点** - 斜基网格与平行四边形分解 - $\beta_1+\beta_2=(2,3)$ 的几何展示

### eval-linalg-029 高等代数 · 线性变换
**题目** 设线性变换 $T:\mathbb R^2\to\mathbb R^2$ 为 $T(x,y)=(x+2y,2x+y)$。求 $\ker T$ 与 $\operatorname{Im}T$，并说明其维数关系。
**答案** $\ker T=\{(0,0)\}$；$\operatorname{Im}T=\mathbb R^2$；$\dim\ker T+\dim\operatorname{Im}T=2$
**解法一（矩阵行列式）** $T$ 的矩阵 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$，$\det A=1-4=-3\ne 0$，故 $A$ 可逆，$T$ 为同构：$\ker T=\{0\}$（零维），$\operatorname{Im}T=\mathbb R^2$（二维），维数公式 $0+2=2$ 成立。
**解法二（直接求解）** 核：解 $\begin{cases}x+2y=0\\2x+y=0\end{cases}$，第一式 $x=-2y$ 代入第二式：$-4y+y=-3y=0$，$y=0$，$x=0$，故 $\ker T=\{(0,0)\}$。像：对任意 $(u,v)$，解 $\begin{cases}x+2y=u\\2x+y=v\end{cases}$，由第二式 $y=v-2x$ 代入第一式：$x+2v-4x=u$，$x=\dfrac{2v-u}{3}$，$y=v-2\cdot\dfrac{2v-u}{3}=\dfrac{2u-v}{3}$，恒有解，故 $\operatorname{Im}T=\mathbb R^2$。
**解法三（复合变换）** $T\circ T$ 的矩阵 $A^2=\begin{pmatrix}5&4\\4&5\end{pmatrix}$，$\det A^2=9\ne 0$，仍为同构。或由特征值观点：$A$ 的特征值为 $3,-1$（eval-linalg-015），均非零，故核为零、像为全空间。
**思路展开** 核与像的维数由秩-零化度定理约束：$\dim\ker+\dim\operatorname{Im}=\dim\mathbb R^2$。可逆性（行列式非零）是核为零的快捷判据。动画可展示网格在 $T$ 下的变换（沿 $(1,1)$ 拉伸 3 倍、沿 $(1,-1)$ 反向）。
**解法一动画要点** - 行列式 $\det A=-3\ne0$ 的可逆判定 - 核为零、像为全空间的标注
**解法二动画要点** - 齐次方程组只有零解的消元 - 对任意 $(u,v)$ 解的存在性验证
**解法三动画要点** - 网格在 $T$ 下的形变 - 特征方向拉伸（3 倍/反向）与复合 $T\circ T$ 的可逆性

### eval-linalg-030 高等代数 · 线性空间
**题目** 用 Gram–Schmidt 正交化方法把向量组 $(1,1,0),(1,0,1),(0,1,1)$ 化为正交向量组。
**答案** $u_1=(1,1,0)$，$u_2=(1,-1,2)$，$u_3=(1,-1,-1)$（可各乘常数）
**解法一（标准 Gram–Schmidt 过程）** 取 $u_1=(1,1,0)$。$u_2=(1,0,1)-\dfrac{(1,0,1)\cdot u_1}{\|u_1\|^2}u_1=(1,0,1)-\dfrac{1}{2}(1,1,0)=\left(\dfrac{1}{2},-\dfrac{1}{2},1\right)$，乘 2 取 $u_2=(1,-1,2)$。$u_3=(0,1,1)-\dfrac{(0,1,1)\cdot u_1}{\|u_1\|^2}u_1-\dfrac{(0,1,1)\cdot u_2}{\|u_2\|^2}u_2=(0,1,1)-\dfrac{1}{2}(1,1,0)-\dfrac{1}{6}(1,-1,2)=\left(-\dfrac{2}{3},\dfrac{2}{3},\dfrac{2}{3}\right)$，乘 $-\dfrac{3}{2}$ 取 $u_3=(1,-1,-1)$。验证：$u_1\cdot u_2=0$，$u_1\cdot u_3=1-1+0=0$，$u_2\cdot u_3=1+1-2=0$，两两正交。
**解法二（对称性构造）** 三个向量关于坐标轮换对称。取和向量 $v_1=(1,1,1)$（在张成空间内，因 $v_1=\dfrac{(1,1,0)+(1,0,1)+(0,1,1)}{2}$ 验证：$\dfrac{(2,2,2)}{2}=(1,1,1)$）；取差向量 $v_2=(1,0,-1)$：$v_1\cdot v_2=0$；取 $v_3=v_1\times v_2=(1,1,1)\times(1,0,-1)=(1\cdot(-1)-1\cdot 0,\ 1\cdot 1-1\cdot(-1),\ 1\cdot 0-1\cdot 1)=(-1,2,-1)$。验证 $v_3$ 在张成空间内：$(1,1,0)-2(1,0,1)+(0,1,1)=(-1,2,-1)$；且 $v_3\cdot v_1=0$、$v_3\cdot v_2=0$。故 $\{(1,1,1),(1,0,-1),(-1,2,-1)\}$ 亦为正交基（这是利用对称性的替代正交基构造，与按原顺序做 Gram–Schmidt 的输出不必相同）。
**解法三（验算还原）** 验证解法一的三向量线性无关：行列式 $\begin{vmatrix}1&1&0\\1&-1&2\\1&-1&-1\end{vmatrix}=1\cdot(1+2)-1\cdot(-1-2)+0=3+3=6\ne 0$。且三者张成的空间与原组相同（原组行列式 $\begin{vmatrix}1&1&0\\1&0&1\\0&1&1\end{vmatrix}=-2\ne 0$，两组都张成 $\mathbb R^3$），故正交化合法。
**思路展开** Gram–Schmidt 是"逐步减去投影"的机械过程；对称性构造利用轮换结构一步到位；验算法保证结果的正确性。动画可展示投影减去的几何步骤（每次减掉已得方向上的分量）。
**解法一动画要点** - 投影减去的逐步动画 - $u_2=(1,-1,2)$、$u_3=(1,-1,-1)$ 的生成
**解法二动画要点** - 和向量/差向量/叉积的轮换对称构造 - 替代正交基的标注
**解法三动画要点** - 两两垂直的验证标注 - 行列式 $6\ne0$ 的线性无关验证

### eval-linalg-031 高等代数 · λ-矩阵

**题目** 设 4 阶矩阵 $A$ 的最小多项式为 $m_A(\lambda)=(\lambda-2)^2(\lambda-3)$,且 $\operatorname{tr}(A)=9$。求 $A$ 的所有可能若尔当标准形,并说明最小多项式如何决定各若尔当块的最大阶数。
**答案** 唯一:$\operatorname{diag}\!\bigl(J_2(2),\,2,\,3\bigr)=\begin{pmatrix}2&1&0&0\\0&2&0&0\\0&0&2&0\\0&0&0&3\end{pmatrix}$,其中 $J_2(2)=\begin{pmatrix}2&1\\0&2\end{pmatrix}$
**解法一（最小多项式定最大块阶）** $m_A$ 的根为 $2,3$,故 $A$ 的谱为 $\{2,3\}$。因子 $(\lambda-2)^2$ 表明 2 对应若尔当块的最大阶数为 2(且恰有一块取到 2 阶);因子 $(\lambda-3)$ 无平方,表明 3 对应块全为 1 阶。$n=4$ 且 3 的重数至少为 1,故 2 的重数为 2 或 3。若 2 重数为 2:块为 $J_2(2)\oplus J_1(3)\oplus J_1(3)$,迹 $=2+2+3+3=10\neq 9$,排除。若 2 重数为 3:块为 $J_2(2)\oplus J_1(2)\oplus J_1(3)$,共 $2+1+1=4$ 阶,迹 $=2+2+2+3=9$,符合。故唯一。
**解法二（特征多项式与迹联立）** 特征多项式 $f_A$ 与 $m_A$ 有相同根,$f_A=(\lambda-2)^{r_2}(\lambda-3)^{r_3}$,$r_2+r_3=4$,$r_2\ge 2$,$r_3\ge 1$,故 $(r_2,r_3)=(3,1)$ 或 $(2,2)$。迹 $=2r_2+3r_3$:$(3,1)$ 给 $6+3=9$;$(2,2)$ 给 $4+6=10$。故 $r_2=3,r_3=1$。2 的块:最大块阶为 2(由 $(\lambda-2)^2$ 整除 $m_A$)且总维数为 3,故块大小拆分为 $2+1$,即 $J_2(2)\oplus J_1(2)$;3 的块为 $J_1(3)$。故唯一:$\operatorname{diag}\!\bigl(J_2(2),2,3\bigr)$。
**解法三（主分解）** $m_A$ 的两个互素因子给出主分解 $V=\ker(A-2I)^2\oplus\ker(A-3I)$。$\ker(A-3I)$ 的维数等于 3 的重数 $r_3$;$\ker(A-2I)^2$ 的维数等于 2 的重数 $r_2$。由 $r_2+r_3=4$、$r_2\ge 2$、$r_3\ge 1$ 与迹 $2r_2+3r_3=9$ 得 $r_2=3,\ r_3=1$。在 $V_2=\ker(A-2I)^2$ 上,幂零部分 $N=A-2I$ 满足 $N^2=0$ 且 $N\neq 0$($N=0$ 会给 $m_A$ 带来因子 $(\lambda-2)$ 而非 $(\lambda-2)^2$),故 $N$ 的幂零指数恰为 2,$V_2$ 上的块为 $J_2(2)\oplus J_1(2)$;$V_3$ 一维,块为 $J_1(3)$。故唯一:$\operatorname{diag}\!\bigl(J_2(2),2,3\bigr)$。
**思路展开** 原题 031(给定矩阵求最小多项式与若尔当形)与 train 仅差一个矩阵元,本题**反其道而行**:从最小多项式与迹反推若尔当形——训练"结构信息如何唯一确定标准形"的逆向思维。三解法分别用最小多项式(块阶上界)、特征多项式+迹(重数分配)、主分解+幂零指数(子空间结构)三条独立路径;动画可展示"块拼图":$2\times2$ 块与 $1\times1$ 块的组合如何在迹约束下唯一化。
**解法一动画要点** - 若尔当块按 $(\lambda-2)^2$、$(\lambda-3)$ 的阶数约束拼图 - 迹 9 排除 $10$ 的组合
**解法二动画要点** - 重数分配 $(3,1)$ 与 $(2,2)$ 的分支图 - 迹公式 $2r_2+3r_3$ 的对照表
**解法三动画要点** - 主分解 $V_2\oplus V_3$ 的子空间示意 - 幂零指数 2(块阶上限)与维数 3 定出 $2+1$ 拆分

### eval-linalg-032 高等代数 · λ-矩阵

**题目** 设 $a\in\mathbb R$ 为参数,$\lambda$-矩阵 $A(\lambda)=\begin{pmatrix}\lambda-a&1&0\\0&\lambda-1&1\\0&0&\lambda-1\end{pmatrix}$。求 $A(\lambda)$ 的不变因子与初等因子,并讨论 $a$ 的取值如何影响初等因子(何时两个不同根的初等因子合并、重数如何变化)。
**答案** 不变因子:$1,\ 1,\ (\lambda-a)(\lambda-1)^2$;初等因子:$a\neq 1$ 时为 $\lambda-a$ 与 $(\lambda-1)^2$;$a=1$ 时为 $(\lambda-1)^3$
**解法一（行列式因子）** 一阶行列式因子 $D_1=1$。二阶子式中含 $\begin{vmatrix}1&0\\\lambda-1&1\end{vmatrix}=1$,故二阶行列式因子 $D_2=\gcd(\cdots,1,\cdots)=1$。三阶行列式因子 $D_3=|A(\lambda)|=(\lambda-a)(\lambda-1)^2$。不变因子 $d_1=D_1=1$,$d_2=\dfrac{D_2}{D_1}=1$,$d_3=\dfrac{D_3}{D_2}=(\lambda-a)(\lambda-1)^2$。初等因子即不变因子分解出的互异幂因子:$a\neq 1$ 时 $d_3$ 给出 $\lambda-a$ 与 $(\lambda-1)^2$ 两个初等因子;$a=1$ 时 $\lambda-a$ 与 $(\lambda-1)^2$ 的根重合,$d_3=(\lambda-1)^3$ 成为一个三重初等因子。
**解法二（初等变换化标准形）** 交换第 1、2 列得 $\begin{pmatrix}1&\lambda-a&0\\\lambda-1&0&1\\0&0&\lambda-1\end{pmatrix}$;第 2 行减去第 1 行的 $(\lambda-1)$ 倍、第 2 列减去第 1 列的 $(\lambda-a)$ 倍,得 $\begin{pmatrix}1&0&0\\0&-(\lambda-a)(\lambda-1)&1\\0&0&\lambda-1\end{pmatrix}$;再交换第 2、3 列,第 3 行减去第 2 行的 $(\lambda-1)$ 倍,第 3 列加回第 2 列的 $(\lambda-a)(\lambda-1)$ 倍,得标准形 $\operatorname{diag}\!\bigl(1,\,1,\,(\lambda-a)(\lambda-1)^2\bigr)$。不变因子读出 $1,\ 1,\ (\lambda-a)(\lambda-1)^2$。末项分解得初等因子:$a\neq 1$ 时为 $\lambda-a$ 与 $(\lambda-1)^2$ 两个;$a=1$ 时两者根重合,合并为 $(\lambda-1)^3$ 一个。
**解法三（循环向量独立推导）** 令 $B(a)=\begin{pmatrix}a&-1&0\\0&1&-1\\0&0&1\end{pmatrix}$,则 $A(\lambda)=\lambda I-B(a)$。取 $e_3=(0,0,1)^T$,直接计算: $$(e_3,\ B e_3,\ B^2 e_3)=\begin{pmatrix}0&0&1\\0&-1&-2\\1&1&1\end{pmatrix},\qquad \det=1\neq 0,$$ 故 $\{e_3,Be_3,B^2e_3\}$ 构成基,$e_3$ 对所有 $a$ 都是 $B$ 的循环向量,因此 $m_B$ 的次数为 3,与特征多项式 $\chi_B(\lambda)=(\lambda-a)(\lambda-1)^2$ 相同,即 $m_B=\chi_B$。于是 $A(\lambda)$ 的不变因子为 $1,\ 1,\ (\lambda-a)(\lambda-1)^2$(唯一非平凡不变因子等于特征多项式)。初等因子:$a\neq 1$ 时为 $\lambda-a$ 与 $(\lambda-1)^2$,对应块 $\operatorname{diag}\!\bigl(a,\,J_2(1)\bigr)$,其中 $J_2(1)=\begin{pmatrix}1&1\\0&1\end{pmatrix}$;$a=1$ 时合并为 $(\lambda-1)^3$,对应块 $J_3(1)=\begin{pmatrix}1&1&0\\0&1&1\\0&0&1\end{pmatrix}$。**所有参数取值下均不可对角化**($a\neq 1$ 时已含 $J_2(1)$ 块);$a$ 从 $\neq 1$ 变到 1 时,变化是初等因子合并、最大若尔当块由二阶升为三阶。
**思路展开** 按用户难度要求升为**三阶**含参 λ-矩阵:不变因子链 $1\mid 1\mid(\lambda-a)(\lambda-1)^2$ 展示"中间不变因子为 1"的典型情形;$(\lambda-1)^2$ 对所有 $a$ 都是重因子,参数退化 $a=1$ 使 $\lambda-a$ 与它合并为 $(\lambda-1)^3$,块结构 $J_1(a)\oplus J_2(1)$ 突变为 $J_3(1)$。三解法分别用行列式因子(定义)、初等变换(算法)、循环向量(结构)三视角。
**解法一动画要点** - 全部二阶子式 $\gcd=1$ 的逐一检验 - $a$ 滑杆下 $(\lambda-a)$ 与 $(\lambda-1)$ 的根逐渐重合
**解法二动画要点** - 行、列初等变换分别逐步动画(Smith 形) - 标准形 $\operatorname{diag}(1,1,(\lambda-a)(\lambda-1)^2)$ 的生成
**解法三动画要点** - 在原参数矩阵上展示特征值合并、特征方向趋于重合 - 块结构 $J_1(a)\oplus J_2(1)$ 向 $J_3(1)$ 的突变(全程不可对角化)
### eval-linalg-033 高等代数 · 矩阵函数
**题目** 设 $A=\begin{pmatrix}0&1\\0&0\end{pmatrix}$，求矩阵指数 $e^{tA}$（$t$ 为参数）。
**答案** $e^{tA}=\begin{pmatrix}1&t\\0&1\end{pmatrix}$
**解法一（级数定义）** $A^2=\begin{pmatrix}0&1\\0&0\end{pmatrix}\begin{pmatrix}0&1\\0&0\end{pmatrix}=0$，故 $A^k=0$（$k\ge 2$）。$e^{tA}=I+tA+\dfrac{t^2A^2}{2!}+\cdots=I+tA=\begin{pmatrix}1&t\\0&1\end{pmatrix}$。
**解法二（解微分方程组）** 方程组 $\dfrac{d}{dt}\begin{pmatrix}x\\y\end{pmatrix}=A\begin{pmatrix}x\\y\end{pmatrix}$，即 $\begin{cases}x'=y\\y'=0\end{cases}$。解得 $y(t)=y_0$，$x(t)=x_0+y_0t$，即 $\begin{pmatrix}x\\y\end{pmatrix}=\begin{pmatrix}1&t\\0&1\end{pmatrix}\begin{pmatrix}x_0\\y_0\end{pmatrix}$。基解矩阵（满足 $\Phi(0)=I$）即 $e^{tA}=\begin{pmatrix}1&t\\0&1\end{pmatrix}$。
**解法三（拉普拉斯变换）** $(sI-A)^{-1}=\begin{pmatrix}s&-1\\0&s\end{pmatrix}^{-1}=\dfrac{1}{s^2}\begin{pmatrix}s&1\\0&s\end{pmatrix}=\begin{pmatrix}1/s&1/s^2\\0&1/s\end{pmatrix}$。逐项取拉普拉斯逆变换（$\mathcal L^{-1}\{1/s\}=1$，$\mathcal L^{-1}\{1/s^2\}=t$），得 $e^{tA}=\begin{pmatrix}1&t\\0&1\end{pmatrix}$。
**思路展开** 矩阵指数在三个语境中出现：级数定义（幂零矩阵只留两项）、微分方程组（基解矩阵）、拉普拉斯变换（预解式逆变换）。幂零性 $A^2=0$ 是本题所有捷径的共同来源。动画可展示 $e^{tA}$ 作用下的相图（沿水平方向匀速漂移的剪切流）。
**解法一动画要点** - 级数展开只留两项（$A^2=0$）的标注 - $e^{tA}=I+tA$ 的生成
**解法二动画要点** - 方程组 $x'=y$、$y'=0$ 的求解 - 基解矩阵的生成
**解法三动画要点** - 预解式 $(sI-A)^{-1}=\begin{pmatrix}1/s&1/s^2\\0&1/s\end{pmatrix}$ 的逆变换 - 相图：剪切流轨道

### eval-linalg-034 高等代数 · 欧几里得空间
**题目** 证明 Cauchy–Schwarz 不等式：对任意向量 $\vec a,\vec b$，$|\vec a\cdot\vec b|\le|\vec a||\vec b|$。
**答案** 证毕（三种证法）
**解法一（判别式法）** 若 $\vec b=\vec 0$ 不等式平凡成立。设 $\vec b\ne\vec 0$，对任意实数 $t$，$0\le|\vec a+t\vec b|^2=|\vec a|^2+2t(\vec a\cdot\vec b)+t^2|\vec b|^2$。该二次函数恒非负，故判别式 $\Delta=4(\vec a\cdot\vec b)^2-4|\vec a|^2|\vec b|^2\le 0$，即 $(\vec a\cdot\vec b)^2\le|\vec a|^2|\vec b|^2$，开方得 $|\vec a\cdot\vec b|\le|\vec a||\vec b|$。等号成立当且仅当 $\vec a+t\vec b=\vec 0$（$\vec a$ 与 $\vec b$ 线性相关）。
**解法二（正交投影）** 若 $\vec b=\vec 0$ 不等式平凡成立。以下设 $\vec b\ne\vec 0$，把 $\vec a$ 分解为 $\vec a=\vec a_\parallel+\vec a_\perp$，其中 $\vec a_\parallel=\dfrac{\vec a\cdot\vec b}{|\vec b|^2}\vec b$ 与 $\vec b$ 平行，$\vec a_\perp\perp\vec b$。由勾股定理 $|\vec a|^2=|\vec a_\parallel|^2+|\vec a_\perp|^2\ge|\vec a_\parallel|^2=\dfrac{(\vec a\cdot\vec b)^2}{|\vec b|^2}$，移项即得。等号成立当且仅当 $\vec a_\perp=\vec 0$。
**解法三（Gram 矩阵半正定）** 对随机变量 $X,Y$ 有 $E[(tX+Y)^2]\ge 0$ 对任意 $t$，故二阶矩矩阵（当 $E[X]=E[Y]=0$ 时即协方差矩阵，一般情形称 Gram 矩阵）$\begin{pmatrix}E[X^2]&E[XY]\\E[XY]&E[Y^2]\end{pmatrix}$ 半正定，行列式 $E[X^2]E[Y^2]-(E[XY])^2\ge 0$，即 $(E[XY])^2\le E[X^2]E[Y^2]$。取有限样本空间上的随机变量与内积 $\langle X,Y\rangle=E[XY]$ 对应（必要时先中心化），即得向量形式的 Cauchy–Schwarz。
**思路展开** 三种证法分别来自二次函数判别式（代换 $t$）、正交分解（勾股定理）、协方差矩阵半正定（概率内积）。它们共同展示"内积空间公理 ⇒ 不等式"的推理链。动画可展示投影分解与判别式抛物线的非负性。
**解法一动画要点** - 判别式 $\Delta\le0$ 的推导 - 二次函数恒非负的抛物线
**解法二动画要点** - 正交投影分解动画 - 勾股定理 $|\vec a|^2\ge|\vec a_\parallel|^2$ 的标注
**解法三动画要点** - 二阶矩矩阵半正定的标注 - 等号条件（共线/退化）的标注

### eval-linalg-035 高等代数 · 欧几里得空间
**题目** 证明：$n$ 阶实方阵 $A$ 是正交矩阵（$A^TA=I$）当且仅当 $A$ 的列向量构成 $\mathbb R^n$ 的标准正交基。
**答案** 证毕（三种证法）
**解法一（分块矩阵）** 把 $A$ 按列分块 $A=(a_1,a_2,\dots,a_n)$。$A^TA$ 的 $(i,j)$ 元为 $a_i^Ta_j=a_i\cdot a_j$。$A^TA=I\iff a_i\cdot a_j=\delta_{ij}$ 对一切 $i,j$ 成立 $\iff$ 列向量两两正交且都是单位向量 $\iff$ 列向量构成标准正交基（$n$ 个两两正交的单位向量必线性无关，因若 $\sum c_ia_i=0$ 则与 $a_j$ 作内积得 $c_j=0$）。
**解法二（保长⇔保内积）** $A^TA=I\iff$ 对任意 $x$，$|Ax|^2=(Ax)^T(Ax)=x^TA^TAx=x^Tx=|x|^2$，即 $A$ 保长。由极化恒等式 $(Ax,Ay)=\dfrac{|A(x+y)|^2-|Ax|^2-|Ay|^2}{2}=\dfrac{|x+y|^2-|x|^2-|y|^2}{2}=(x,y)$，保长⇒保内积。取 $x=e_i$、$y=e_j$：$(Ae_i,Ae_j)=(e_i,e_j)=\delta_{ij}$，即列向量标准正交。反之列向量标准正交⇒$A^TA=I$ 由解法一。
**解法三（必要条件与反例说明）** 由 $A^TA=I$ 取行列式得 $(\det A)^2=1$，故正交矩阵的行列式为 $\pm 1$；又若 $Ax=\lambda x$，则 $|x|^2=|Ax|^2=|\lambda|^2|x|^2$，故特征值的模为 1。反之行列式为 $\pm 1$ 或特征值模为 1 都不足以保证正交（反例：$\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 的行列式为 1、特征值均为 1，但列向量不垂直，非正交矩阵），说明"列标准正交"才是充要条件。
**思路展开** 本题是"矩阵方程⇔几何性质"的典型证明题：$A^TA=I$ 的代数结构、保长保内积的几何性质、列标准正交基的向量组性质三者等价。解法三刻意给出两个"似是而非"的必要条件及其反例，划清充要条件的边界。动画可展示正交变换的保长性质与列向量旋转。
**解法一动画要点** - 分块 $A^TA$ 的 $(i,j)$ 元 $a_i\cdot a_j$ 标注 - 线性无关性的验证
**解法二动画要点** - 保长性质的演示 - 极化恒等式的推导
**解法三动画要点** - 行列式 $\pm1$ 与特征值模 1 的必要条件 - 反例矩阵（剪切）的对照
