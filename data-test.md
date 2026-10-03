# data-test（泛化综合运用）· 审阅稿 v1

> 状态：**草稿，供用户审阅题目与解答**；未冻结、未转 JSON/JSONL。
> 规模：150 题（数学分析综合 45 / 解析几何综合 25 / 概率论综合 25 / 高等代数综合 40 / 跨学科综合 15），每题跨 ≥2 个知识点。
> 转 JSONL 的字段映射（内容定稿后执行）：
> - 标题行 `### <id>  <category> · <知识点A>×<知识点B>` → id / category / sub_category（取 × 组合）；
> - `**题目**` → problem；`**涉及知识点**` → 知识标签；`**解答**` → solution；`**答案**` → answer；
> - `**动画要点**` 为审阅辅助，scene_spec 在内容定稿后按动画要点逐条补写；
> - id 全局唯一（test-* 前缀）；与 data/v1/raw 训练集 63 条及 dataset-eval.md 题目族不同、无重叠。
> source 待用户定（建议 self-authored）；license = Internal-Research-Use-Only。
> 约定：全部题目结果为确切值或确切表达式，不收录以估算为目标的题目。

# 一、数学分析综合（45 题）

### test-calc-001 数学分析 · 极限×定积分
**题目** 求极限 $\displaystyle\lim_{n\to\infty}\frac{1}{n}\sum_{k=1}^{n}\sin\frac{k\pi}{n}$。
**涉及知识点** 黎曼和、定积分定义、正弦函数积分
**解答** 该和式为函数 $f(x)=\sin(\pi x)$ 在 $[0,1]$ 上 $n$ 等分的黎曼和（取右端点 $\dfrac{k}{n}$）：$\dfrac{1}{n}\displaystyle\sum_{k=1}^{n}\sin\dfrac{k\pi}{n}=\sum_{k=1}^{n}\sin\left(\pi\cdot\dfrac{k}{n}\right)\cdot\dfrac{1}{n}$。由定积分定义，$\lim_{n\to\infty}\dfrac{1}{n}\displaystyle\sum_{k=1}^{n}\sin\dfrac{k\pi}{n}=\int_0^1\sin(\pi x)\,dx=\left[-\dfrac{\cos\pi x}{\pi}\right]_0^1=-\dfrac{\cos\pi}{\pi}+\dfrac{\cos 0}{\pi}=\dfrac{1}{\pi}+\dfrac{1}{\pi}=\dfrac{2}{\pi}$。
**答案** $\dfrac{2}{\pi}$
**动画要点** - 单位区间 $[0,1]$ 上 $\sin(\pi x)$ 的黎曼矩形逼近 - 和式随 $n$ 增大收敛于积分值

### test-calc-002 数学分析 · 数列极限×泰勒公式
**题目** 求极限 $\displaystyle\lim_{n\to\infty}n^2\left(1-\cos\frac{1}{n}\right)$。
**涉及知识点** 数列极限、泰勒展开、无穷小阶
**解答** 由 $\cos x=1-\dfrac{x^2}{2}+o(x^2)$，取 $x=\dfrac{1}{n}\to 0$：$1-\cos\dfrac{1}{n}=\dfrac{1}{2n^2}+o\left(\dfrac{1}{n^2}\right)$。故 $n^2\left(1-\cos\dfrac{1}{n}\right)=n^2\cdot\dfrac{1}{2n^2}+n^2\cdot o\left(\dfrac{1}{n^2}\right)\to\dfrac{1}{2}$。
**答案** $\dfrac{1}{2}$
**动画要点** - $y=1-\cos x$ 与 $y=x^2/2$ 在原点附近的二阶接触 - 数列点列向 $1/2$ 收敛

### test-calc-003 数学分析 · 变限积分×导数
**题目** 设 $F(x)=\displaystyle\int_1^x\frac{\ln t}{t}\,dt$（$x>0$）。求 $F'(x)$、$F''(x)$，并给出 $F(x)$ 的显式表达式。
**涉及知识点** 微积分基本定理、对数函数、链式求导
**解答** 由微积分基本定理，$F'(x)=\dfrac{\ln x}{x}$。再求导：$F''(x)=\dfrac{\frac{1}{x}\cdot x-\ln x\cdot 1}{x^2}=\dfrac{1-\ln x}{x^2}$。显式积分：令 $u=\ln t$（$du=\dfrac{dt}{t}$），$F(x)=\displaystyle\int_0^{\ln x}u\,du=\dfrac{(\ln x)^2}{2}$（下限 $t=1$ 对应 $u=0$）。验证：$F'(x)=\dfrac{2\ln x}{2}\cdot\dfrac{1}{x}=\dfrac{\ln x}{x}$，一致。
**答案** $F'(x)=\dfrac{\ln x}{x}$；$F''(x)=\dfrac{1-\ln x}{x^2}$；$F(x)=\dfrac{(\ln x)^2}{2}$
**动画要点** - 被积函数曲线与变限积分的面积 - $F,F',F''$ 三条曲线对照

### test-calc-004 数学分析 · 微分方程×一阶线性
**题目** 求微分方程 $y'+2y=e^{-x}$ 的通解。
**涉及知识点** 一阶线性微分方程、积分因子、常数变易
**解答** 积分因子 $\mu(x)=e^{\int 2\,dx}=e^{2x}$。方程两边乘 $e^{2x}$：$e^{2x}y'+2e^{2x}y=e^{x}$，即 $(e^{2x}y)'=e^{x}$。积分得 $e^{2x}y=e^{x}+C$，故通解 $y=e^{-x}+Ce^{-2x}$。
**答案** $y=e^{-x}+Ce^{-2x}$
**动画要点** - 积分因子把左端变为乘积导数 - 通解曲线族（含特解 $e^{-x}$）

### test-calc-005 数学分析 · 级数×反常积分
**题目** 用积分判别法判断级数 $\displaystyle\sum_{n=2}^{\infty}\frac{1}{n\ln n}$ 的敛散性。
**涉及知识点** 积分判别法、对数函数积分、p 级数思想
**解答** $f(x)=\dfrac{1}{x\ln x}$ 在 $[2,+\infty)$ 上非负递减。$\displaystyle\int_2^{+\infty}\dfrac{dx}{x\ln x}=\lim_{b\to\infty}\left[\ln(\ln x)\right]_2^b=\lim_{b\to\infty}\left(\ln(\ln b)-\ln(\ln 2)\right)=+\infty$，发散。由积分判别法，级数 $\sum\dfrac{1}{n\ln n}$ 发散。
**答案** 发散
**动画要点** - $y=\dfrac{1}{x\ln x}$ 曲线下的无穷面积 - 级数柱状图嵌入曲线下方

### test-calc-006 数学分析 · 泰勒公式×递推
**题目** 求 $f(x)=\ln(1+x)$ 的麦克劳林展开式，并归纳 $f^{(n)}(0)$ 的规律。
**涉及知识点** 泰勒公式、高阶导数递推、幂级数
**解答** 逐阶求导：$f'(x)=(1+x)^{-1}$，$f''(x)=-(1+x)^{-2}$，$f'''(x)=2(1+x)^{-3}$，$f^{(4)}(x)=-6(1+x)^{-4}$。归纳得 $f^{(n)}(x)=(-1)^{n-1}(n-1)!\,(1+x)^{-n}$（$n\ge 1$），故 $f^{(n)}(0)=(-1)^{n-1}(n-1)!$。麦克劳林展开：$\ln(1+x)=\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}x^n}{n}$（$|x|<1$）。
**答案** $\ln(1+x)=\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}x^n}{n}$；$f^{(n)}(0)=(-1)^{n-1}(n-1)!$
**动画要点** - 逐阶导数系数的递推表 - 部分和多项式逐阶逼近 $\ln(1+x)$

### test-calc-007 数学分析 · 中值定理×极限
**题目** 设 $f$ 二阶可导且 $f(0)=f'(0)=0$，求 $\displaystyle\lim_{x\to 0}\frac{f(x)}{x^2}$。
**涉及知识点** 洛必达法则、二阶导数、函数极限
**解答** 由 $f(0)=0$ 与 $f'(0)=0$，$\dfrac{f(x)}{x^2}$ 为 $\dfrac{0}{0}$ 型。洛必达一次：$\lim_{x\to 0}\dfrac{f'(x)}{2x}$。不假设 $f''$ 连续，直接由二阶导数定义（$f'(0)=0$）：$\lim_{x\to 0}\dfrac{f'(x)}{2x}=\dfrac{1}{2}\lim_{x\to 0}\dfrac{f'(x)-f'(0)}{x}=\dfrac{f''(0)}{2}$。
**答案** $\dfrac{f''(0)}{2}$
**动画要点** - 洛必达两步的分子分母比值 - $f$ 在原点附近的二阶接触

### test-calc-008 数学分析 · 变限积分×极值
**题目** 求 $f(x)=\displaystyle\int_0^x(t^2-t)\,dt$ 的极值点与极值。
**涉及知识点** 微积分基本定理、极值判别、定积分计算
**解答** $f'(x)=x^2-x=x(x-1)$，驻点 $x=0,1$。$f''(x)=2x-1$：$f''(0)=-1<0$，$x=0$ 为极大值点；$f''(1)=1>0$，$x=1$ 为极小值点。计算值：$f(x)=\displaystyle\int_0^x(t^2-t)dt=\dfrac{x^3}{3}-\dfrac{x^2}{2}$。$f(0)=0$（极大值），$f(1)=\dfrac{1}{3}-\dfrac{1}{2}=-\dfrac{1}{6}$（极小值）。
**答案** 极大值 $f(0)=0$；极小值 $f(1)=-\dfrac{1}{6}$
**动画要点** - 被积函数 $t^2-t$ 与面积的正负变化 - $f$ 曲线与两个极值点

### test-calc-009 数学分析 · 参数方程×弧长
**题目** 求曲线 $x=t^2,\ y=t^3$（$0\le t\le 1$）的弧长。
**涉及知识点** 参数方程、弧长公式、换元积分
**解答** $\dfrac{dx}{dt}=2t$，$\dfrac{dy}{dt}=3t^2$。弧长 $L=\displaystyle\int_0^1\sqrt{(2t)^2+(3t^2)^2}\,dt=\int_0^1 t\sqrt{4+9t^2}\,dt$。令 $u=4+9t^2$（$du=18t\,dt$），$L=\dfrac{1}{18}\displaystyle\int_4^{13}\sqrt{u}\,du=\dfrac{1}{18}\cdot\dfrac{2}{3}\left[u^{3/2}\right]_4^{13}=\dfrac{1}{27}(13\sqrt{13}-8)$。
**答案** $\dfrac{13\sqrt{13}-8}{27}$
**动画要点** - 半立方抛物线 $x=t^2,y=t^3$ 的绘制 - 弧长微元沿曲线扫掠

### test-calc-010 数学分析 · 极坐标×面积
**题目** 求心形线 $r=1+\cos\theta$ 所围图形的面积。
**涉及知识点** 极坐标面积公式、倍角积分、对称性
**解答** 极坐标面积 $S=\dfrac{1}{2}\displaystyle\int_0^{2\pi}r^2\,d\theta=\dfrac{1}{2}\int_0^{2\pi}(1+\cos\theta)^2d\theta=\dfrac{1}{2}\int_0^{2\pi}(1+2\cos\theta+\cos^2\theta)d\theta$。其中 $\int_0^{2\pi}\cos\theta\,d\theta=0$，$\int_0^{2\pi}\cos^2\theta\,d\theta=\pi$，故 $S=\dfrac{1}{2}(2\pi+0+\pi)=\dfrac{3\pi}{2}$。
**答案** $\dfrac{3\pi}{2}$
**动画要点** - 心形线的动态绘制 - 扇形微元扫掠 - 面积结果标注

### test-calc-011 数学分析 · 旋转体×壳层法
**题目** 求由 $y=x^2$ 与 $y=4$ 围成的区域绕 $y$ 轴旋转所得旋转体的体积。
**涉及知识点** 壳层法、多项式积分、旋转体体积
**解答** 区域为 $-2\le x\le 2,\ x^2\le y\le 4$（关于 $y$ 轴对称）。绕 $y$ 轴旋转时左右两半生成同一个旋转体，只需取右半 $0\le x\le 2$。在 $x$ 处取高 $4-x^2$、厚 $dx$ 的竖直壳层，$dV=2\pi x(4-x^2)dx$。$V=\displaystyle\int_0^2 2\pi x(4-x^2)dx=2\pi\int_0^2(4x-x^3)dx=2\pi\left[2x^2-\dfrac{x^4}{4}\right]_0^2=2\pi(8-4)=8\pi$。
**答案** $8\pi$
**动画要点** - 壳层展开成薄板的扫掠动画 - 抛物线、直线与旋转轴

### test-calc-012 数学分析 · 反常积分×部分分式
**题目** 判断反常积分 $\displaystyle\int_1^{+\infty}\frac{dx}{x(1+x)}$ 的敛散性，若收敛求其值。
**涉及知识点** 反常积分、部分分式、对数函数
**解答** $\dfrac{1}{x(1+x)}=\dfrac{1}{x}-\dfrac{1}{1+x}$。$\displaystyle\int_1^b\dfrac{dx}{x(1+x)}=\left[\ln x-\ln(1+x)\right]_1^b=\ln\dfrac{b}{1+b}-\ln\dfrac{1}{2}$。令 $b\to+\infty$：$\ln\dfrac{b}{1+b}\to\ln 1=0$，故积分 $=0-\ln\dfrac{1}{2}=\ln 2$，收敛。
**答案** $\ln 2$
**动画要点** - 部分分式拆分的面积分解 - 上限 $b\to\infty$ 时面积趋于 $\ln 2$

### test-calc-013 数学分析 · 级数×裂项
**题目** 求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n(n+2)}$ 的和。
**涉及知识点** 裂项相消、部分和极限、几何级数思想
**解答** $\dfrac{1}{n(n+2)}=\dfrac{1}{2}\left(\dfrac{1}{n}-\dfrac{1}{n+2}\right)$。部分和 $S_n=\dfrac{1}{2}\displaystyle\sum_{k=1}^{n}\left(\dfrac{1}{k}-\dfrac{1}{k+2}\right)=\dfrac{1}{2}\left[\left(1+\dfrac{1}{2}+\dfrac{1}{3}+\cdots+\dfrac{1}{n}\right)-\left(\dfrac{1}{3}+\dfrac{1}{4}+\cdots+\dfrac{1}{n+2}\right)\right]=\dfrac{1}{2}\left(1+\dfrac{1}{2}-\dfrac{1}{n+1}-\dfrac{1}{n+2}\right)$。令 $n\to\infty$，$S=\dfrac{1}{2}\cdot\dfrac{3}{2}=\dfrac{3}{4}$。
**答案** $\dfrac{3}{4}$
**动画要点** - 裂项相消的逐项抵消动画 - 部分和逼近 $3/4$

### test-calc-014 数学分析 · 幂级数×微分方程
**题目** 验证幂级数 $y=\displaystyle\sum_{n=0}^{\infty}\frac{x^n}{n!}$ 满足微分方程 $y'=y$ 及初值 $y(0)=1$。
**涉及知识点** 幂级数逐项求导、微分方程、指数函数
**解答** 该级数收敛半径为 $+\infty$（比值判别法：$\dfrac{1/(n+1)!}{1/n!}=\dfrac{1}{n+1}\to 0$），可逐项求导：$y'=\displaystyle\sum_{n=1}^{\infty}\dfrac{nx^{n-1}}{n!}=\sum_{n=1}^{\infty}\dfrac{x^{n-1}}{(n-1)!}=\sum_{m=0}^{\infty}\dfrac{x^m}{m!}=y$。且 $y(0)=\dfrac{1}{0!}+\displaystyle\sum_{n=1}^{\infty}\dfrac{0^n}{n!}=1+0=1$。由解的唯一性，$y=e^x$。
**答案** $y'=y$、$y(0)=1$，故 $y=e^x$
**动画要点** - 部分和多项式随项数增长逼近 $e^x$ - 逐项求导的系数错位对应

### test-calc-015 数学分析 · 幂级数×定积分
**题目** 利用幂级数展开求 $\displaystyle\int_0^1\frac{\ln(1+x)}{x}\,dx$ 的精确值。
**涉及知识点** 幂级数逐项积分、交错级数、$\zeta(2)$
**解答** $\ln(1+x)=\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}x^n}{n}$，除以 $x$ 得 $\dfrac{\ln(1+x)}{x}=\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}x^{n-1}}{n}$（$x\ne 0$），且该级数在 $[0,1]$ 上一致收敛：余项 $\left|\displaystyle\sum_{k>N}\dfrac{(-1)^{k-1}x^{k-1}}{k}\right|\le\dfrac{x^N}{N+1}\le\dfrac{1}{N+1}\to 0$（交错级数估计，对 $x\in[0,1]$ 一致）；被积函数在 $x=0$ 处连续延拓为 $1$（$\lim_{x\to 0}\dfrac{\ln(1+x)}{x}=1$）。故可逐项积分：$\displaystyle\int_0^1\dfrac{\ln(1+x)}{x}dx=\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}}{n}\int_0^1x^{n-1}dx=\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}}{n^2}$。由交错级数与 $\zeta(2)$ 的关系：$\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}}{n^2}=\eta(2)=\left(1-2^{1-2}\right)\zeta(2)=\dfrac{1}{2}\cdot\dfrac{\pi^2}{6}=\dfrac{\pi^2}{12}$（其中 $\zeta(2)=\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{n^2}=\dfrac{\pi^2}{6}$ 为已知结果，可由 test-calc-023 的 Parseval 等式得到）。
**答案** $\dfrac{\pi^2}{12}$
**动画要点** - 级数部分和逐项逼近 - $\dfrac{\pi^2}{12}$ 与积分数值对照

### test-calc-016 数学分析 · 隐函数×高阶导数
**题目** 由方程 $x^2+y^2+xy=3$ 确定隐函数 $y=y(x)$。求 $y'(1)$ 与 $y''(1)$（已知 $(1,1)$ 满足方程）。
**涉及知识点** 隐函数求导、链式法则、高阶导数
**解答** 两边对 $x$ 求导：$2x+2yy'+y+xy'=0$。代入 $(1,1)$：$2+2y'(1)+1+y'(1)=0$，即 $3y'(1)=-3$，$y'(1)=-1$。再对 $x$ 求导：$2+2(y')^2+2yy''+y'+y'+xy''=0$，即 $2+2(y')^2+2yy''+2y'+xy''=0$。代入 $(1,1)$ 与 $y'=-1$：$2+2\cdot 1+2y''-2+y''=0$，即 $3y''=-2$，$y''(1)=-\dfrac{2}{3}$。
**答案** $y'(1)=-1$；$y''(1)=-\dfrac{2}{3}$
**动画要点** - 隐式曲线在 $(1,1)$ 处的切线与凹凸 - 逐次求导的符号推导

### test-calc-017 数学分析 · 多元函数×无条件极值
**题目** 求 $f(x,y)=x^2+y^2-xy+x+y$ 的极值点与极值。
**涉及知识点** 多元极值、驻点、Hessian 矩阵
**解答** 驻点条件：$f_x=2x-y+1=0$，$f_y=2y-x+1=0$。两式相加得 $x+y+2=0$；两式相减得 $3x-3y=0$，即 $x=y$。代入 $x+y+2=0$：$2x=-2$，$x=y=-1$。驻点 $(-1,-1)$。Hessian $H=\begin{pmatrix}2&-1\\-1&2\end{pmatrix}$，顺序主子式 $2>0$、$\det H=3>0$，正定，故 $(-1,-1)$ 为极小值点。$f(-1,-1)=1+1-1-1-1=-1$。
**答案** 极小值 $f(-1,-1)=-1$
**动画要点** - 曲面 $z=f(x,y)$ 与极小点 - 等高线向极值点收缩

### test-calc-018 数学分析 · 条件极值×拉格朗日乘数
**题目** 求 $f(x,y)=xy$ 在约束 $x+y=4$ 下的最大值。
**涉及知识点** 拉格朗日乘数法、约束优化、消元验证
**解答** 拉格朗日函数 $L=xy+\lambda(x+y-4)$。$L_x=y+\lambda=0$，$L_y=x+\lambda=0$，故 $x=y=-\lambda$。代入约束 $2x=4$，$x=y=2$，$\lambda=-2$。$f(2,2)=4$。验证（消元法）：$y=4-x$，$f=x(4-x)=4x-x^2=-(x-2)^2+4\le 4$，等号在 $x=2$ 取得，最大值 $4$。
**答案** 最大值 $4$（在 $(2,2)$ 处取得）
**动画要点** - 约束直线与等高线（双曲线族）相切 - 拉格朗日乘数的几何意义

### test-calc-019 数学分析 · 重积分×交换次序
**题目** 求 $\displaystyle I=\int_0^1\!\!\int_y^1\frac{x}{1+x^2}\,dx\,dy$。
**涉及知识点** 交换积分次序、反三角函数、二重积分
**解答** 区域 $D=\{(x,y):0\le y\le 1,\ y\le x\le 1\}=\{(x,y):0\le x\le 1,\ 0\le y\le x\}$。交换次序：$I=\displaystyle\int_0^1\!\!\int_0^x\frac{x}{1+x^2}\,dy\,dx=\int_0^1\frac{x^2}{1+x^2}\,dx=\int_0^1\left(1-\frac{1}{1+x^2}\right)dx=\left[x-\arctan x\right]_0^1=1-\dfrac{\pi}{4}$。
**答案** $1-\dfrac{\pi}{4}$
**动画要点** - 三角形区域的两种扫描方向 - 交换次序前后的对照

### test-calc-020 数学分析 · 格林公式×参数方程
**题目** 用格林公式（或曲线积分）求椭圆 $\dfrac{x^2}{a^2}+\dfrac{y^2}{b^2}=1$（$a,b>0$）的面积。
**涉及知识点** 格林公式、参数方程、定积分
**解答** 参数化 $x=a\cos t$、$y=b\sin t$（$t:0\to 2\pi$）。由格林公式，面积 $S=\dfrac{1}{2}\displaystyle\oint(x\,dy-y\,dx)=\dfrac{1}{2}\int_0^{2\pi}\left[a\cos t\cdot b\cos t-b\sin t\cdot(-a\sin t)\right]dt=\dfrac{1}{2}\int_0^{2\pi}ab(\cos^2t+\sin^2t)dt=\dfrac{1}{2}ab\cdot 2\pi=\pi ab$。
**答案** $\pi ab$
**动画要点** - 椭圆参数点沿边界运动 - 面积公式与扇形微元

### test-calc-021 数学分析 · 曲线积分×路径无关
**题目** 求曲线积分 $\displaystyle\int_L(2xy\,dx+x^2\,dy)$，其中 $L$ 为从 $(0,0)$ 到 $(1,1)$ 的任意光滑曲线段，并说明结果与路径无关的原因。
**涉及知识点** 全微分、势函数、曲线积分
**解答** $d(x^2y)=2xy\,dx+x^2\,dy$，故被积表达式是全微分，势函数 $\varphi(x,y)=x^2y$。由微积分基本定理，$\displaystyle\int_L d\varphi=\varphi(1,1)-\varphi(0,0)=1-0=1$，与路径无关（本题已直接构造出 $\mathbb R^2$ 上的全局势函数，故无需再讨论充要条件；一般结论"$\dfrac{\partial P}{\partial y}=\dfrac{\partial Q}{\partial x}$ 等价于积分与路径无关"只在单连通区域上对 $C^1$ 向量场成立）。
**答案** $1$
**动画要点** - 不同路径的曲线积分同一结果 - 势函数的等高线

### test-calc-022 数学分析 · 曲面积分×高斯公式
**题目** 用高斯公式求 $\displaystyle\iint_S\vec F\cdot\vec n\,dS$，其中 $\vec F=(x,y,z)$，$S$ 为单位球面 $x^2+y^2+z^2=1$（外侧），$\vec n$ 为单位外法向量。
**涉及知识点** 高斯散度定理、球体积、散度
**解答** $\operatorname{div}\vec F=\dfrac{\partial x}{\partial x}+\dfrac{\partial y}{\partial y}+\dfrac{\partial z}{\partial z}=3$。由高斯公式，$\displaystyle\iint_S\vec F\cdot\vec n\,dS=\iiint_B\operatorname{div}\vec F\,dV=3\iiint_B dV=3\cdot\dfrac{4\pi}{3}=4\pi$（$B$ 为单位球体，体积 $\dfrac{4\pi}{3}$）。
**答案** $4\pi$
**动画要点** - 单位球面与向量场 - 高斯公式的区域积分示意

### test-calc-023 数学分析 · 傅里叶级数×Parseval 等式
**题目** 已知 $f(x)=x$（$-\pi\le x\le\pi$）的傅里叶级数为 $2\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n+1}}{n}\sin nx$。利用 Parseval 等式求 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^2}$。
**涉及知识点** 傅里叶级数、Parseval 等式、欧拉求和
**解答** Parseval 等式：$\dfrac{1}{\pi}\displaystyle\int_{-\pi}^{\pi}f(x)^2dx=\sum_{n=1}^{\infty}b_n^2$（奇函数情形，$a_n=0$），其中 $b_n=\dfrac{2(-1)^{n+1}}{n}$。左端 $\dfrac{1}{\pi}\displaystyle\int_{-\pi}^{\pi}x^2dx=\dfrac{1}{\pi}\cdot\dfrac{2\pi^3}{3}=\dfrac{2\pi^2}{3}$。右端 $\displaystyle\sum_{n=1}^{\infty}\dfrac{4}{n^2}=4\sum_{n=1}^{\infty}\dfrac{1}{n^2}$。故 $4\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{n^2}=\dfrac{2\pi^2}{3}$，$\displaystyle\sum_{n=1}^{\infty}\dfrac{1}{n^2}=\dfrac{\pi^2}{6}$。
**答案** $\dfrac{\pi^2}{6}$
**动画要点** - 锯齿波与傅里叶部分和叠加 - 能量等式两端的对照

### test-calc-024 数学分析 · 数列极限×定积分
**题目** 求 $\displaystyle\lim_{n\to\infty}\frac{\sqrt[n]{n!}}{n}$。
**涉及知识点** 对数化、黎曼和、对数积分
**解答** 记 $S_n=\dfrac{1}{n}\displaystyle\sum_{k=1}^{n}\ln\dfrac{k}{n}$，其中 $\dfrac{k}{n}$ 是小区间 $\left[\dfrac{k-1}{n},\dfrac{k}{n}\right]$ 的右端点。因 $\ln x$ 单调递增，在每个小区间上 $\ln x\le\ln\dfrac{k}{n}$，故 $\displaystyle\int_0^1\ln x\,dx=\sum_{k=1}^{n}\int_{(k-1)/n}^{k/n}\ln x\,dx\le S_n$；又对 $k\le n-1$，在 $\left[\dfrac{k}{n},\dfrac{k+1}{n}\right]$ 上 $\ln x\ge\ln\dfrac{k}{n}$，故 $S_n\le\displaystyle\sum_{k=1}^{n-1}\int_{k/n}^{(k+1)/n}\ln x\,dx+\dfrac{1}{n}\ln 1=\int_{1/n}^1\ln x\,dx$。于是 $-1=\displaystyle\int_0^1\ln x\,dx\le S_n\le\int_{1/n}^1\ln x\,dx=\left[x\ln x-x\right]_{1/n}^1=-1+\dfrac{\ln n+1}{n}$（其中 $\lim_{x\to 0^+}x\ln x=0$ 保证左端积分为 $-1$）。两端都趋于 $-1$，由夹逼准则 $S_n\to-1$。故原极限 $=\lim e^{S_n}=e^{-1}=\dfrac{1}{e}$。
**答案** $\dfrac{1}{e}$
**动画要点** - 对数函数的黎曼矩形 - 极限值 $1/e$ 的收敛示意

### test-calc-025 数学分析 · 单调有界×递推数列
**题目** 设 $a_1=1$，$a_{n+1}=1+\dfrac{a_n}{1+a_n}$。证明 $\{a_n\}$ 收敛并求其极限。
**涉及知识点** 单调有界准则、递推数列、不动点
**解答** 记 $\varphi=\dfrac{1+\sqrt5}{2}$（满足 $\varphi^2=\varphi+1$）。先证 $1\le a_n<\varphi$：$a_1=1<\varphi$；若 $a_n<\varphi$，则 $a_{n+1}=1+\dfrac{a_n}{1+a_n}<1+\dfrac{\varphi}{1+\varphi}$。由 $\varphi^2=\varphi+1$ 得 $\dfrac{\varphi}{1+\varphi}=\dfrac{1}{\varphi}$，故 $a_{n+1}<1+\dfrac{1}{\varphi}=\varphi$（$1+\dfrac{1}{\varphi}=\dfrac{\varphi+1}{\varphi}=\dfrac{\varphi^2}{\varphi}=\varphi$）。再证单调递增：$a_{n+1}-a_n=1-\dfrac{a_n^2}{1+a_n}=\dfrac{1+a_n-a_n^2}{1+a_n}>0$（因 $a_n<\varphi$ 时 $a_n^2<1+a_n$）。故 $\{a_n\}$ 单调递增有上界，收敛。设极限为 $L$，对递推式取极限：$L=1+\dfrac{L}{1+L}$，即 $L^2=L+1$，正根 $L=\varphi=\dfrac{1+\sqrt5}{2}$。
**答案** 极限为 $\dfrac{1+\sqrt5}{2}$
**动画要点** - 蛛网图（cobweb）迭代收敛 - 不动点 $\varphi$ 的标注

### test-calc-026 数学分析 · 洛必达×变限积分
**题目** 求 $\displaystyle\lim_{x\to 0}\frac{\displaystyle\int_0^x\sin(t^2)\,dt}{x^3}$。
**涉及知识点** 洛必达法则、变限积分求导、等价无穷小
**解答** $\dfrac{0}{0}$ 型。分子求导得 $\sin(x^2)$，分母求导得 $3x^2$。原式 $=\lim_{x\to 0}\dfrac{\sin(x^2)}{3x^2}$。令 $u=x^2\to 0$，$\dfrac{\sin u}{u}\to 1$，故原式 $=\dfrac{1}{3}$。
**答案** $\dfrac{1}{3}$
**动画要点** - 被积函数与面积 - 洛必达步骤的比值对照

### test-calc-027 数学分析 · 零点定理×中值定理
**题目** 证明方程 $e^x=2x+1$ 恰有两个实根，并给出两个根所在的区间。
**涉及知识点** 零点存在性、单调区间、极值分析
**解答** 令 $f(x)=e^x-2x-1$。$f(0)=1-0-1=0$，故 $x=0$ 是一个根。$f'(x)=e^x-2$，$f'=0$ 当 $x=\ln 2$。$f(\ln 2)=2-2\ln 2-1=1-2\ln 2<0$（$\ln 2\approx 0.693$）。$f(2)=e^2-5>0$，$f(-\infty)=+\infty$ 且 $f(-2)=e^{-2}+4-1>0$。在 $(-\infty,\ln 2]$ 上 $f$ 严格递减（$f'<0$），且 $f(-2)>0$、$f(\ln 2)<0$，由零点定理存在唯一根 $\xi_1\in(-2,\ln 2)$（即 $x=0$，因 $f(0)=0$ 且该区间上单调故唯一）；在 $[\ln 2,+\infty)$ 上 $f$ 严格递增，$f(\ln 2)<0$、$f(2)>0$，存在唯一根 $\xi_2\in(\ln 2,2)$。故恰有两个实根：$x=0$ 与 $\xi_2\in(\ln 2,2)$。
**答案** 恰有两个实根：$x=0$ 与 $\xi_2\in(\ln 2,2)$
**动画要点** - $y=e^x$ 与 $y=2x+1$ 的两交点 - 单调区间与零点定位

### test-calc-028 数学分析 · 定积分×奇偶对称性
**题目** 求 $\displaystyle\int_{-1}^{1}x^3\sqrt{1-x^2}\,dx$。
**涉及知识点** 奇函数对称性、定积分
**解答** 被积函数 $f(x)=x^3\sqrt{1-x^2}$ 满足 $f(-x)=(-x)^3\sqrt{1-(-x)^2}=-x^3\sqrt{1-x^2}=-f(x)$，为奇函数，积分区间关于原点对称，故 $\displaystyle\int_{-1}^{1}f(x)dx=0$。
**答案** $0$
**动画要点** - 奇函数曲线两侧面积正负抵消 - 对称性标注

### test-calc-029 数学分析 · 反常积分×分部积分
**题目** 判断 $\displaystyle\int_1^{+\infty}\frac{\ln x}{x^2}\,dx$ 的敛散性，若收敛求其值。
**涉及知识点** 反常积分、分部积分、极限
**解答** 分部积分（$u=\ln x$、$dv=x^{-2}dx$）：$\displaystyle\int\dfrac{\ln x}{x^2}dx=-\dfrac{\ln x}{x}+\int\dfrac{dx}{x^2}=-\dfrac{\ln x}{x}-\dfrac{1}{x}+C$。$\displaystyle\int_1^b=-\left[\dfrac{\ln x}{x}+\dfrac{1}{x}\right]_1^b=1-\dfrac{\ln b}{b}-\dfrac{1}{b}$。令 $b\to+\infty$：$\dfrac{\ln b}{b}\to 0$、$\dfrac{1}{b}\to 0$，故积分为 $1$，收敛。
**答案** $1$
**动画要点** - 曲线下面积趋于 1 - 分部积分的两项分解

### test-calc-030 数学分析 · 极限×积分不等式
**题目** 求 $\displaystyle\lim_{n\to\infty}\int_0^1\frac{x^n}{1+x}\,dx$。
**涉及知识点** 夹逼准则、定积分估计、极限
**解答** 当 $0\le x\le 1$ 时 $0\le\dfrac{x^n}{1+x}\le x^n$（因 $1+x\ge 1$），故 $0\le\displaystyle\int_0^1\dfrac{x^n}{1+x}dx\le\int_0^1x^ndx=\dfrac{1}{n+1}$。由夹逼准则，极限为 $0$。
**答案** $0$
**动画要点** - 被积函数随 $n$ 增大而"塌陷" - 夹逼上下界的动画

### test-calc-031 数学分析 · 导数×物理建模
**题目** 物体从高度 $20$ 米处自由下落，高度函数 $h(t)=20-5t^2$（米，$t$ 为秒）。求速度与加速度函数，及物体落地时刻与落地速度。
**涉及知识点** 导数、物理建模、二次函数
**解答** $v(t)=h'(t)=-10t$（米/秒），$a(t)=v'(t)=-10$（米/秒²，向下）。落地：$h(t)=0$，即 $20-5t^2=0$，$t=2$（秒，舍负根）。落地速度 $v(2)=-20$（米/秒，向下，大小为 $20$）。
**答案** $v=-10t$；$a=-10$；$t=2$ 秒落地，落地速度大小 $20$ 米/秒
**动画要点** - 高度抛物线、速度直线、加速度水平线三图对照 - 落地时刻标注

### test-calc-032 数学分析 · 曲率×导数
**题目** 求曲线 $y=x^2$ 在原点处的曲率，以及曲线 $y=\ln x$ 在 $(1,0)$ 处的曲率。
**涉及知识点** 曲率公式、二阶导数、反函数思想
**解答** 曲率公式 $\kappa=\dfrac{|y''|}{(1+y'^2)^{3/2}}$。对 $y=x^2$：$y'=2x$，$y''=2$，在 $(0,0)$：$\kappa=\dfrac{2}{(1+0)^{3/2}}=2$。对 $y=\ln x$：$y'=\dfrac{1}{x}$，$y''=-\dfrac{1}{x^2}$，在 $(1,0)$：$\kappa=\dfrac{1}{(1+1)^{3/2}}=\dfrac{1}{2\sqrt2}$。
**答案** $y=x^2$ 在原点处 $\kappa=2$；$y=\ln x$ 在 $(1,0)$ 处 $\kappa=\dfrac{1}{2\sqrt2}$
**动画要点** - 密切圆在两曲线处的贴合 - 曲率随位置变化

### test-calc-033 数学分析 · 泰勒公式×不等式证明
**题目** 证明：当 $x\ge 0$ 时，$e^x\ge 1+x+\dfrac{x^2}{2}$。
**涉及知识点** 泰勒公式、单调性、不等式
**解答** 令 $f(x)=e^x-1-x-\dfrac{x^2}{2}$。$f'(x)=e^x-1-x$。由 $e^x>1+x$（$x>0$，eval-calc-008）得 $f'(x)>0$（$x>0$），故 $f$ 在 $[0,+\infty)$ 上严格递增。又 $f(0)=1-1-0-0=0$，故 $x\ge 0$ 时 $f(x)\ge 0$，即 $e^x\ge 1+x+\dfrac{x^2}{2}$。亦可由泰勒公式带拉格朗日余项 $e^x=1+x+\dfrac{x^2}{2}+\dfrac{x^3}{6}e^\xi\ge 1+x+\dfrac{x^2}{2}$（$\xi\ge 0$）直接得证。
**答案** 证毕（两种证法）
**动画要点** - $y=e^x$ 与 $y=1+x+\dfrac{x^2}{2}$ 的分离 - 余项曲线的包络

### test-calc-034 数学分析 · 级数×比值判别法
**题目** 判断级数 $\displaystyle\sum_{n=1}^{\infty}\frac{n!}{n^n}$ 的敛散性。
**涉及知识点** 比值判别法、重要极限、阶乘增长
**解答** 比值：$\dfrac{a_{n+1}}{a_n}=\dfrac{(n+1)!}{(n+1)^{n+1}}\cdot\dfrac{n^n}{n!}=\dfrac{n^n}{(n+1)^n}=\left(\dfrac{n}{n+1}\right)^n=\dfrac{1}{\left(1+\frac{1}{n}\right)^n}\to\dfrac{1}{e}<1$。由比值判别法，级数收敛。
**答案** 收敛
**动画要点** - 比值 $\left(\frac{n}{n+1}\right)^n$ 趋近 $1/e$ - 级数项与几何级数比较

### test-calc-035 数学分析 · 幂级数×收敛半径
**题目** 求幂级数 $\displaystyle\sum_{n=0}^{\infty}\frac{x^n}{n!}$ 与 $\displaystyle\sum_{n=0}^{\infty}n!\,x^n$ 的收敛半径，并对比说明。
**涉及知识点** 收敛半径、比值判别法、阶乘增长
**解答** 用系数比值 $\left|\dfrac{a_{n+1}}{a_n}\right|$（$a_n$ 为幂级数系数，不含 $x$）。对 $\sum\dfrac{x^n}{n!}$：$a_n=\dfrac{1}{n!}$，$\left|\dfrac{a_{n+1}}{a_n}\right|=\dfrac{1}{n+1}\to 0$，收敛半径 $R=\dfrac{1}{0}=+\infty$。对 $\sum n!\,x^n$：$a_n=n!$，$\left|\dfrac{a_{n+1}}{a_n}\right|=n+1\to+\infty$，$R=0$；且 $x\ne 0$ 时通项 $n!x^n\not\to 0$，级数发散，与 $R=0$ 一致。
**答案** $R=+\infty$ 与 $R=0$
**动画要点** - 两系数序列的增长对比（$1/n!$ 与 $n!$） - 数轴上收敛域标注

### test-calc-036 数学分析 · 多元链式法则×拉普拉斯算子
**题目** 设 $u=f(r)$，其中 $r=\sqrt{x^2+y^2}$（$(x,y)\ne(0,0)$），$f$ 二阶可导。证明在 $\mathbb R^2\setminus\{(0,0)\}$ 上 $u_{xx}+u_{yy}=f''(r)+\dfrac{f'(r)}{r}$，并验证 $u=\ln r$ 满足 $u_{xx}+u_{yy}=0$。
**涉及知识点** 多元链式法则、拉普拉斯算子、调和函数
**解答** $r_x=\dfrac{x}{r}$，$r_y=\dfrac{y}{r}$。$u_x=f'(r)\dfrac{x}{r}$，$u_{xx}=f''(r)\dfrac{x^2}{r^2}+f'(r)\left(\dfrac{1}{r}-\dfrac{x^2}{r^3}\right)$。同理 $u_{yy}=f''(r)\dfrac{y^2}{r^2}+f'(r)\left(\dfrac{1}{r}-\dfrac{y^2}{r^3}\right)$。相加：$u_{xx}+u_{yy}=f''(r)\dfrac{x^2+y^2}{r^2}+f'(r)\left(\dfrac{2}{r}-\dfrac{x^2+y^2}{r^3}\right)=f''(r)+f'(r)\left(\dfrac{2}{r}-\dfrac{1}{r}\right)=f''(r)+\dfrac{f'(r)}{r}$。取 $f(r)=\ln r$：$f'(r)=\dfrac{1}{r}$，$f''(r)=-\dfrac{1}{r^2}$，代入得 $u_{xx}+u_{yy}=-\dfrac{1}{r^2}+\dfrac{1}{r^2}=0$，即 $\ln r$ 在去掉原点的平面上调和。
**答案** 证毕（在 $\mathbb R^2\setminus\{(0,0)\}$ 上）；$u=\ln r$ 在 $\mathbb R^2\setminus\{(0,0)\}$ 上满足 $u_{xx}+u_{yy}=0$
**动画要点** - 径向函数与极坐标拉普拉斯 - $\ln r$ 的等值线（同心圆）

### test-calc-037 数学分析 · 隐函数×导数
**题目** 由笛卡尔叶形线方程 $x^3+y^3-3xy=0$ 确定隐函数。求曲线在点 $\left(\dfrac{3}{2},\dfrac{3}{2}\right)$ 处的切线斜率。
**涉及知识点** 隐函数求导、代数曲线、切线
**解答** 两边对 $x$ 求导：$3x^2+3y^2y'-3y-3xy'=0$，即 $(y^2-x)y'=y-x^2$，$y'=\dfrac{y-x^2}{y^2-x}$。在 $\left(\dfrac{3}{2},\dfrac{3}{2}\right)$ 处：$y'=\dfrac{\frac{3}{2}-\frac{9}{4}}{\frac{9}{4}-\frac{3}{2}}=\dfrac{-\frac{3}{4}}{\frac{3}{4}}=-1$。
**答案** $-1$
**动画要点** - 叶形线的环与渐近线 - 切点 $\left(\frac32,\frac32\right)$ 处的切线

### test-calc-038 数学分析 · 凸函数×积分不等式
**题目** 证明 $\displaystyle\int_0^1 e^{x^2}\,dx\ge e^{1/3}$。
**涉及知识点** Jensen 不等式、凸函数、定积分
**解答** $e^t$ 是凸函数。区间 $[0,1]$ 上取均匀"概率测度"，由积分型 Jensen 不等式：$\displaystyle\int_0^1 e^{x^2}dx\ge e^{\int_0^1 x^2dx}=e^{1/3}$（凸函数在"平均点"的取值不大于函数值的平均）。其中 $\displaystyle\int_0^1x^2dx=\dfrac{1}{3}$。
**答案** 证毕
**动画要点** - 凸函数图像上弦与弧的位置关系 - 不等式两端的对照

### test-calc-039 数学分析 · 微分方程×应用建模
**题目** 牛顿冷却模型：物体温度 $T(t)$ 满足 $T'=-k(T-20)$（环境温度 $20^\circ$C）。已知 $T(0)=100$、$T(5)=60$，求 $T(10)$。
**涉及知识点** 可分离变量微分方程、指数衰减、参数确定
**解答** 解方程：$\dfrac{dT}{T-20}=-k\,dt$，积分得 $\ln(T-20)=-kt+C$，$T=20+Ce^{-kt}$。由 $T(0)=100$：$C=80$，$T=20+80e^{-kt}$。由 $T(5)=60$：$60=20+80e^{-5k}$，$e^{-5k}=\dfrac{1}{2}$。故 $T(10)=20+80e^{-10k}=20+80(e^{-5k})^2=20+80\cdot\dfrac{1}{4}=40$。
**答案** $T(10)=40^\circ$C
**动画要点** - 冷却曲线与 $20^\circ$C 渐近线 - 两点确定参数 $k$

### test-calc-040 数学分析 · 泰勒公式×极限
**题目** 求 $\displaystyle\lim_{x\to 0}\frac{1-\cos x-\frac{x^2}{2}}{x^4}$。
**涉及知识点** 泰勒展开、高阶无穷小、极限
**解答** $\cos x=1-\dfrac{x^2}{2}+\dfrac{x^4}{24}-\dfrac{x^6}{720}+\cdots$。故 $1-\cos x-\dfrac{x^2}{2}=-\dfrac{x^4}{24}+o(x^4)$。原式 $=\lim_{x\to 0}\dfrac{-x^4/24+o(x^4)}{x^4}=-\dfrac{1}{24}$。
**答案** $-\dfrac{1}{24}$
**动画要点** - $\cos x$ 与 $1-\dfrac{x^2}{2}$ 的四阶偏差 - 极限值标注

### test-calc-041 数学分析 · 定积分×对称性
**题目** 求 $\displaystyle\int_0^{\pi}\sin^2x\,dx$ 与 $\displaystyle\int_0^{\pi}\cos^2x\,dx$，并说明两者相等的几何原因。
**涉及知识点** 倍角公式、平移对称、定积分
**解答** $\displaystyle\int_0^{\pi}\sin^2x\,dx=\int_0^{\pi}\dfrac{1-\cos 2x}{2}dx=\left[\dfrac{x}{2}-\dfrac{\sin 2x}{4}\right]_0^{\pi}=\dfrac{\pi}{2}$。$\displaystyle\int_0^{\pi}\cos^2x\,dx=\int_0^{\pi}\dfrac{1+\cos 2x}{2}dx=\left[\dfrac{x}{2}+\dfrac{\sin 2x}{4}\right]_0^{\pi}=\dfrac{\pi}{2}$。几何原因：$\cos^2x=\sin^2\left(x+\dfrac{\pi}{2}\right)$，故 $\displaystyle\int_0^{\pi}\cos^2x\,dx=\int_0^{\pi}\sin^2\left(x+\dfrac{\pi}{2}\right)dx=\int_{\pi/2}^{3\pi/2}\sin^2u\,du$（换元 $u=x+\dfrac{\pi}{2}$）$=\displaystyle\int_0^{\pi}\sin^2u\,du$（$\sin^2$ 以 $\pi$ 为周期）。
**答案** 均为 $\dfrac{\pi}{2}$
**动画要点** - 两曲线的平移关系 - 面积相等的对照

### test-calc-042 数学分析 · 交错级数×幂级数
**题目** 证明 $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^{n-1}}{n}=\ln 2$。
**涉及知识点** 幂级数、Abel 定理、交错级数
**解答** 由 test-calc-006，$\ln(1+x)=\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}x^n}{n}$ 对 $|x|<1$ 成立。$x=1$ 处级数 $\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}}{n}$ 为交错级数（$a_n=\dfrac{1}{n}\searrow 0$），由莱布尼茨判别法收敛。由 Abel 定理，幂级数的和函数在收敛点左连续，故 $\displaystyle\sum_{n=1}^{\infty}\dfrac{(-1)^{n-1}}{n}=\lim_{x\to 1^-}\ln(1+x)=\ln 2$。另一证法（积分表示）：$\dfrac{1}{n}=\displaystyle\int_0^1x^{n-1}dx$，故 $\displaystyle\sum_{n=1}^{N}\dfrac{(-1)^{n-1}}{n}=\int_0^1\sum_{n=1}^{N}(-x)^{n-1}dx=\int_0^1\dfrac{1-(-x)^N}{1+x}dx\to\int_0^1\dfrac{dx}{1+x}=\ln 2$。
**答案** 证毕（两种证法）
**动画要点** - 交错级数部分和逼近 $\ln 2$ - $x\to 1^-$ 的和函数连续过渡

### test-calc-043 数学分析 · 反常积分×极坐标
**题目** 求 $\displaystyle\int_0^{+\infty}e^{-x^2}\,dx$（高斯积分）。
**涉及知识点** 反常积分、极坐标换元、夹逼
**解答** 记 $I=\displaystyle\int_0^{+\infty}e^{-x^2}dx$。$I^2=\displaystyle\int_0^{\infty}e^{-x^2}dx\int_0^{\infty}e^{-y^2}dy=\iint_{[0,\infty)^2}e^{-(x^2+y^2)}dx\,dy$。用极坐标（第一象限）：$I^2=\displaystyle\int_0^{\pi/2}\!\!\int_0^{\infty}e^{-r^2}r\,dr\,d\theta=\int_0^{\pi/2}\left[-\dfrac{e^{-r^2}}{2}\right]_0^{\infty}d\theta=\int_0^{\pi/2}\dfrac{1}{2}\,d\theta=\dfrac{\pi}{4}$。故 $I=\dfrac{\sqrt\pi}{2}$（$I>0$）。严格化：先对有限正方形/四分之一圆取极限，用夹逼说明无穷区域上的积分等于逐次积分。
**答案** $\dfrac{\sqrt\pi}{2}$
**动画要点** - 钟形曲面与体积 - 四分之一圆的极坐标扫描

### test-calc-044 数学分析 · 参数方程×面积
**题目** 用参数方程 $x=a\cos t,\ y=b\sin t$（$0\le t\le 2\pi$，$a,b>0$）求椭圆所围面积。
**涉及知识点** 参数方程面积公式、倍角积分
**解答** $S=\left|\displaystyle\int_0^{2\pi}y\,dx\right|=\left|\int_0^{2\pi}b\sin t\cdot(-a\sin t)dt\right|=ab\displaystyle\int_0^{2\pi}\sin^2t\,dt=ab\cdot\pi=\pi ab$（$\int_0^{2\pi}\sin^2t\,dt=\pi$，与 test-calc-041 同法）。
**答案** $\pi ab$
**动画要点** - 参数点沿椭圆运动 - 面积微元的累积

### test-calc-045 数学分析 · 中值定理×极限
**题目** 求 $\displaystyle\lim_{x\to+\infty}x^2\left(2^{1/x}-2^{1/(x+1)}\right)$。
**涉及知识点** 拉格朗日中值定理、指数函数、极限
**解答** 对 $f(t)=2^t$ 在 $\left[\dfrac{1}{x+1},\dfrac{1}{x}\right]$ 上用拉格朗日中值定理：$2^{1/x}-2^{1/(x+1)}=f'(\xi)\left(\dfrac{1}{x}-\dfrac{1}{x+1}\right)=2^\xi\ln 2\cdot\dfrac{1}{x(x+1)}$，其中 $\dfrac{1}{x+1}<\xi<\dfrac{1}{x}$。故原式 $=\lim_{x\to\infty}x^2\cdot 2^\xi\ln 2\cdot\dfrac{1}{x(x+1)}=\lim_{x\to\infty}\dfrac{x^2}{x(x+1)}\cdot 2^\xi\ln 2$。当 $x\to+\infty$ 时 $\xi\to 0^+$，$2^\xi\to 1$，$\dfrac{x^2}{x(x+1)}\to 1$，故极限为 $\ln 2$。
**答案** $\ln 2$
**动画要点** - $y=2^t$ 上两点随 $x\to\infty$ 靠拢 - 中值点 $\xi\to 0$ 的标注

# 二、解析几何综合（25 题）

### test-geom-001 解析几何 · 空间直线×平面
**题目** 求两直线 $l_1:\begin{cases}x=1+t\\y=2-t\\z=t\end{cases}$ 与 $l_2:\begin{cases}x=2+s\\y=1+2s\\z=1+s\end{cases}$ 的交点，并求过两直线的平面方程。
**涉及知识点** 空间直线参数方程、叉积、平面方程
**解答** 求交点：$\begin{cases}1+t=2+s\\2-t=1+2s\\t=1+s\end{cases}$。由第三式 $t=1+s$，代入第一式：$1+1+s=2+s$ 恒等；代入第二式：$2-(1+s)=1+2s$，即 $1-s=1+2s$，$s=0$，$t=1$。交点为 $(2,1,1)$。两直线方向：$\vec{s_1}=(1,-1,1)$，$\vec{s_2}=(1,2,1)$。过两直线的平面法向量 $\vec n=\vec{s_1}\times\vec{s_2}=((-1)\cdot 1-1\cdot 2,\ 1\cdot 1-1\cdot 1,\ 1\cdot 2-(-1)\cdot 1)=(-3,0,3)$，取 $(1,0,-1)$。平面方程：$(x-2)-(z-1)=0$，即 $x-z=1$。
**答案** 交点 $(2,1,1)$；平面 $x-z=1$
**动画要点** - 两直线相交的三维视图 - 法向量叉积方向 - 平面贴合两直线

### test-geom-002 解析几何 · 点到直线×投影
**题目** 求点 $P(1,2,3)$ 到直线 $l:x=1+t,\ y=1+2t,\ z=1+3t$ 的距离与垂足坐标。
**涉及知识点** 叉积距离公式、正交投影、参数方程
**解答** 直线上取点 $P_0(1,1,1)$、方向 $\vec s=(1,2,3)$。$\overrightarrow{P_0P}=(0,1,2)$。叉积 $\overrightarrow{P_0P}\times\vec s=(1\cdot 3-2\cdot 2,\ 2\cdot 1-0\cdot 3,\ 0\cdot 2-1\cdot 1)=(-1,2,-1)$，模 $\sqrt{6}$；$|\vec s|=\sqrt{14}$。距离 $d=\dfrac{\sqrt6}{\sqrt{14}}=\sqrt{\dfrac{3}{7}}$。垂足参数 $t^*=\dfrac{\overrightarrow{P_0P}\cdot\vec s}{|\vec s|^2}=\dfrac{0+2+6}{14}=\dfrac{4}{7}$，垂足 $Q=\left(1+\dfrac{4}{7},1+\dfrac{8}{7},1+\dfrac{12}{7}\right)=\left(\dfrac{11}{7},\dfrac{15}{7},\dfrac{19}{7}\right)$。
**答案** 距离 $\sqrt{\dfrac{3}{7}}$；垂足 $\left(\dfrac{11}{7},\dfrac{15}{7},\dfrac{19}{7}\right)$
**动画要点** - 直线与垂线段 - 叉积平行四边形的面积分解

### test-geom-003 解析几何 · 异面直线×公垂线
**题目** 求异面直线 $l_1:\begin{cases}x=1+t\\y=2t\\z=3+t\end{cases}$ 与 $l_2:\begin{cases}x=2s\\y=1-s\\z=2s\end{cases}$ 之间的距离。
**涉及知识点** 混合积、叉积、公垂线方向
**解答** $\vec{s_1}=(1,2,1)$，$\vec{s_2}=(2,-1,2)$，取点 $P_1=(1,0,3)\in l_1$、$P_2=(0,1,0)\in l_2$。公垂线方向 $\vec n=\vec{s_1}\times\vec{s_2}=(2\cdot 2-1\cdot(-1),\ 1\cdot 2-1\cdot 2,\ 1\cdot(-1)-2\cdot 2)=(5,0,-5)$，取 $(1,0,-1)$。$\overrightarrow{P_1P_2}=(-1,1,-3)$。距离 $d=\dfrac{|\overrightarrow{P_1P_2}\cdot\vec n|}{|\vec n|}=\dfrac{|-1-0+3|}{\sqrt2}=\dfrac{2}{\sqrt2}=\sqrt2$。
**答案** $\sqrt2$
**动画要点** - 两异面直线与公垂线段 - 方向向量叉积

### test-geom-004 解析几何 · 平面×球面
**题目** 判断平面 $x+2y+2z=3$ 与球面 $x^2+y^2+z^2=1$ 的位置关系，若相切求切点。
**涉及知识点** 点到平面距离、球面方程、相切条件
**解答** 球心 $O(0,0,0)$ 到平面的距离 $d=\dfrac{|0+0+0-3|}{\sqrt{1+4+4}}=\dfrac{3}{3}=1$，等于球半径 $1$，故平面与球面相切。切点在球心到平面的垂线上：$\overrightarrow{OQ}$ 沿法向量 $(1,2,2)$，且 $|OQ|=1$，$Q=\dfrac{1}{3}(1,2,2)=\left(\dfrac{1}{3},\dfrac{2}{3},\dfrac{2}{3}\right)$。验证在平面上：$\dfrac{1}{3}+\dfrac{4}{3}+\dfrac{4}{3}=\dfrac{9}{3}=3$。
**答案** 相切，切点 $\left(\dfrac{1}{3},\dfrac{2}{3},\dfrac{2}{3}\right)$
**动画要点** - 球与平面相切 - 半径与切点的垂直关系

### test-geom-005 解析几何 · 曲面×切平面
**题目** 求曲面 $z=\dfrac{x^2}{4}+y^2$ 在点 $(2,1,2)$ 处的切平面方程。
**涉及知识点** 偏导数、切平面、梯度
**解答** $z_x=\dfrac{x}{2}$，$z_y=2y$。在 $(2,1)$ 处 $z_x=1$、$z_y=2$。切平面：$z-2=1\cdot(x-2)+2\cdot(y-1)$，即 $z=x+2y-2$。验证切点在平面上：$2=2+2-2$。
**答案** $z=x+2y-2$
**动画要点** - 椭圆抛物面与切平面贴合 - 两条切方向

### test-geom-006 解析几何 · 空间曲线×法平面
**题目** 求曲线 $x=t,\ y=t^2,\ z=t^3$ 在 $t=1$ 处的切线与法平面方程。
**涉及知识点** 空间曲线切向量、法平面、参数求导
**解答** $\vec r'(t)=(1,2t,3t^2)$，在 $t=1$ 处切向量 $(1,2,3)$，切点 $(1,1,1)$。切线：$\dfrac{x-1}{1}=\dfrac{y-1}{2}=\dfrac{z-1}{3}$。法平面：$1\cdot(x-1)+2\cdot(y-1)+3\cdot(z-1)=0$，即 $x+2y+3z=6$。
**答案** 切线 $\dfrac{x-1}{1}=\dfrac{y-1}{2}=\dfrac{z-1}{3}$；法平面 $x+2y+3z=6$
**动画要点** - 三次挠曲线与切线 - 法平面垂直于切线

### test-geom-007 解析几何 · 混合积×体积
**题目** 求以 $O(0,0,0)$、$A(1,2,0)$、$B(2,0,1)$、$C(0,1,2)$ 为顶点的四面体体积。
**涉及知识点** 混合积、平行六面体、行列式
**解答** $V=\dfrac{1}{6}\left|\det(\overrightarrow{OA},\overrightarrow{OB},\overrightarrow{OC})\right|=\dfrac{1}{6}\left|\begin{vmatrix}1&2&0\\2&0&1\\0&1&2\end{vmatrix}\right|$。行列式 $=1\cdot(0\cdot 2-1\cdot 1)-2\cdot(2\cdot 2-1\cdot 0)+0=1\cdot(-1)-2\cdot 4=-9$。$V=\dfrac{9}{6}=\dfrac{3}{2}$。
**答案** $\dfrac{3}{2}$
**动画要点** - 四面体与平行六面体 - 混合积的体积意义

### test-geom-008 解析几何 · 向量×三角形面积
**题目** 求以 $A(1,0)$、$B(0,1)$、$C(2,3)$ 为顶点的三角形面积。
**涉及知识点** 叉积面积公式、行列式
**解答** 平面中三角形面积 $S=\dfrac{1}{2}\left|\det(\overrightarrow{AB},\overrightarrow{AC})\right|$。$\overrightarrow{AB}=(-1,1)$，$\overrightarrow{AC}=(1,3)$。$\det=(-1)\cdot 3-1\cdot 1=-4$。$S=\dfrac{1}{2}\cdot 4=2$。
**答案** $2$
**动画要点** - 三角形与叉积平行四边形 - 面积标注

### test-geom-009 解析几何 · 旋转×投影
**题目** 求点 $(2,1)$ 绕原点逆时针旋转 $90^\circ$ 后的坐标，以及向量 $(3,4)$ 在方向 $(1,1)$ 上的投影向量。
**涉及知识点** 旋转矩阵、正交投影、点积
**解答** 旋转 $90^\circ$：$(x,y)\mapsto(-y,x)$，$(2,1)\mapsto(-1,2)$。投影：方向单位向量 $\vec u=\dfrac{1}{\sqrt2}(1,1)$，投影 $=((3,4)\cdot\vec u)\vec u=\dfrac{7}{\sqrt2}\cdot\dfrac{1}{\sqrt2}(1,1)=\left(\dfrac{7}{2},\dfrac{7}{2}\right)$。
**答案** $(-1,2)$；$\left(\dfrac{7}{2},\dfrac{7}{2}\right)$
**动画要点** - 旋转动画 - 投影垂线

### test-geom-010 解析几何 · 二次曲线×面积
**题目** 求椭圆 $\dfrac{x^2}{9}+\dfrac{y^2}{16}=1$ 的面积。
**涉及知识点** 椭圆面积公式、仿射变换、积分
**解答** 椭圆是半径为 3 的圆沿 $y$ 轴拉伸 $\dfrac{4}{3}$ 倍的像：$S=\pi\cdot 3\cdot 4=12\pi$。或用定积分：$S=4\displaystyle\int_0^3 4\sqrt{1-\dfrac{x^2}{9}}\,dx=16\int_0^3\sqrt{1-\dfrac{x^2}{9}}\,dx$。换元 $x=3\sin t$（$dx=3\cos t\,dt$，$t:0\to\dfrac{\pi}{2}$）：$S=16\cdot 3\displaystyle\int_0^{\pi/2}\cos^2t\,dt=48\cdot\dfrac{\pi}{4}=12\pi$（$\int_0^{\pi/2}\cos^2t\,dt=\dfrac{\pi}{4}$）。直接公式 $S=\pi ab=\pi\cdot 3\cdot 4=12\pi$。
**答案** $12\pi$
**动画要点** - 圆到椭圆的拉伸 - 面积公式标注

### test-geom-011 解析几何 · 空间直线×坐标面
**题目** 求直线 $\dfrac{x-2}{1}=\dfrac{y+1}{2}=\dfrac{z-3}{-1}$ 与三个坐标面的交点。
**涉及知识点** 空间直线参数方程、坐标面
**解答** 参数化 $x=2+t,\ y=-1+2t,\ z=3-t$。与 $xOy$ 面（$z=0$）：$3-t=0$，$t=3$，交点 $(5,5,0)$。与 $yOz$ 面（$x=0$）：$2+t=0$，$t=-2$，交点 $(0,-5,5)$。与 $xOz$ 面（$y=0$）：$-1+2t=0$，$t=\dfrac{1}{2}$，交点 $\left(\dfrac{5}{2},0,\dfrac{5}{2}\right)$。
**答案** $(5,5,0)$；$(0,-5,5)$；$\left(\dfrac{5}{2},0,\dfrac{5}{2}\right)$
**动画要点** - 直线穿过三个坐标面 - 交点标注

### test-geom-012 解析几何 · 三重积×混合积
**题目** 设 $\vec a=(1,0,1)$、$\vec b=(0,1,1)$、$\vec c=(1,1,0)$，求 $\vec a\cdot(\vec b\times\vec c)$ 与 $\vec a\times\vec b\cdot\vec c$，并比较。
**涉及知识点** 混合积、轮换对称性、行列式
**解答** 先算 $\vec b\times\vec c$：$\vec b=(0,1,1)$，$\vec c=(1,1,0)$，叉积 $=(1\cdot 0-1\cdot 1,\ 1\cdot 1-0\cdot 0,\ 0\cdot 1-1\cdot 1)=(-1,1,-1)$。故 $\vec a\cdot(\vec b\times\vec c)=1\cdot(-1)+0\cdot 1+1\cdot(-1)=-2$。再算 $\vec a\times\vec b$：$(0\cdot 1-1\cdot 1,\ 1\cdot 0-1\cdot 1,\ 1\cdot 1-0\cdot 0)=(-1,-1,1)$。故 $(\vec a\times\vec b)\cdot\vec c=(-1)\cdot 1+(-1)\cdot 1+1\cdot 0=-2$。两者相等，符合混合积的轮换对称性 $\vec a\cdot(\vec b\times\vec c)=\vec b\cdot(\vec c\times\vec a)=\vec c\cdot(\vec a\times\vec b)$；该值也等于行列式 $\begin{vmatrix}1&0&1\\0&1&1\\1&1&0\end{vmatrix}=1\cdot(1\cdot 0-1\cdot 1)-0\cdot(0\cdot 0-1\cdot 1)+1\cdot(0\cdot 1-1\cdot 1)=-1-1=-2$。
**答案** 均为 $-2$
**动画要点** - 三向量与平行六面体 - 混合积的轮换对称

### test-geom-013 解析几何 · 球面×截面圆
**题目** 求球面 $x^2+y^2+z^2=4$ 与平面 $z=\sqrt2$ 的交线方程，并将其参数化。
**涉及知识点** 截面圆、参数方程、圆
**解答** 代入 $z=\sqrt2$：$x^2+y^2+2=4$，即 $x^2+y^2=2$。交线为平面 $z=\sqrt2$ 上的圆，半径 $\sqrt2$，圆心 $(0,0,\sqrt2)$。参数化：$x=\sqrt2\cos t$，$y=\sqrt2\sin t$，$z=\sqrt2$，$t\in[0,2\pi]$。
**答案** $\begin{cases}x^2+y^2=2\\z=\sqrt2\end{cases}$；参数化 $(x,y,z)=(\sqrt2\cos t,\sqrt2\sin t,\sqrt2)$
**动画要点** - 平面截球的截面圆 - 参数点沿圆运动

### test-geom-014 解析几何 · 直纹面×双曲抛物面
**题目** 证明曲面 $z=x^2-y^2$ 是直纹面，并写出其直母线族。
**涉及知识点** 直纹面、因式分解、直线族
**解答** $z=x^2-y^2=(x+y)(x-y)$。对任意常数 $c$，直线 $\begin{cases}x+y=c\\z=c(x-y)\end{cases}$ 上每点满足 $z=(x+y)(x-y)=c(x-y)$，故整条直线在曲面上；同理 $\begin{cases}x-y=c\\z=c(x+y)\end{cases}$ 也是直母线族。每点处恰有两条直母线通过，故 $z=x^2-y^2$ 是直纹面（双曲抛物面）。
**答案** 证毕；直母线族 $\begin{cases}x+y=c\\z=c(x-y)\end{cases}$ 与 $\begin{cases}x-y=c\\z=c(x+y)\end{cases}$
**动画要点** - 马鞍面上的直线网格 - 两族直母线

### test-geom-015 解析几何 · 曲面×条件极值
**题目** 求曲面 $xyz=1$（$x,y,z>0$）上到原点距离最近的点及最短距离。
**涉及知识点** 条件极值、均值不等式、距离
**解答** 求 $d^2=x^2+y^2+z^2$ 在 $xyz=1$ 下的最小值。由均值不等式 $x^2+y^2+z^2\ge 3\sqrt[3]{x^2y^2z^2}=3\sqrt[3]{(xyz)^2}=3$，等号当且仅当 $x^2=y^2=z^2$，即 $x=y=z=1$（$xyz=1$）。故最近点为 $(1,1,1)$，最短距离 $\sqrt3$。
**答案** 最近点 $(1,1,1)$，距离 $\sqrt3$
**动画要点** - 曲面 $xyz=1$ 与原点 - 最短距离线段

### test-geom-016 解析几何 · 线性变换×二次曲线
**题目** 线性变换 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 把单位圆 $x^2+y^2=1$ 变成什么曲线？并求其面积。
**涉及知识点** 线性变换、二次曲线、行列式
**解答** $A$ 把 $(x,y)$ 映到 $(x',y')=(x+y,y)$。反解 $x=x'-y'$、$y=y'$。代入 $x^2+y^2=1$：$(x'-y')^2+y'^2=1$，即 $x'^2-2x'y'+2y'^2=1$。这是椭圆（二次型 $x'^2-2x'y'+2y'^2$ 正定，因矩阵 $\begin{pmatrix}1&-1\\-1&2\end{pmatrix}$ 顺序主子式 $1>0$、$1>0$）。面积：$\det A=1$，故椭圆面积 $=\pi\cdot|\det A|=\pi$。
**答案** 椭圆 $x^2-2xy+2y^2=1$，面积 $\pi$
**动画要点** - 单位圆被剪切为椭圆 - 面积不变（$\det A=1$）

### test-geom-017 解析几何 · 曲率×曲率半径
**题目** 求抛物线 $y=x^2$ 在顶点处的曲率与曲率半径，并说明顶点处曲率最大的原因。
**涉及知识点** 曲率公式、极值、抛物线
**解答** $\kappa(x)=\dfrac{|y''|}{(1+y'^2)^{3/2}}=\dfrac{2}{(1+4x^2)^{3/2}}$。在顶点 $x=0$：$\kappa=2$，曲率半径 $R=\dfrac{1}{2}$。$\kappa(x)$ 在 $x=0$ 处最大（分母在 $x=0$ 最小），因顶点处曲线"弯得最急"。
**答案** $\kappa=2$；$R=\dfrac{1}{2}$
**动画要点** - 密切圆在顶点处贴合 - 曲率随 $x$ 减小

### test-geom-018 解析几何 · 平面束×定点
**题目** 求过直线 $l:\begin{cases}x+y-1=0\\x+z-2=0\end{cases}$ 且过点 $(0,0,0)$ 的平面方程。
**涉及知识点** 平面束、参数代入、平面方程
**解答** 过 $l$ 的平面束为 $(x+y-1)+\lambda(x+z-2)=0$。代入点 $(0,0,0)$：$-1-2\lambda=0$，$\lambda=-\dfrac{1}{2}$。代入：$(x+y-1)-\dfrac{1}{2}(x+z-2)=0$，即 $x+y-1-\dfrac{x}{2}-\dfrac{z}{2}+1=0$，$\dfrac{x}{2}+y-\dfrac{z}{2}=0$，$x+2y-z=0$。
**答案** $x+2y-z=0$
**动画要点** - 平面束绕直线旋转 - 扫过定点

### test-geom-019 解析几何 · 椭圆×距离最值
**题目** 求椭圆 $\dfrac{x^2}{4}+y^2=1$ 上点到 $(1,0)$ 的距离的最大值与最小值。
**涉及知识点** 参数方程、距离最值、二次函数
**解答** 参数化 $(2\cos t,\sin t)$。$d^2=(2\cos t-1)^2+\sin^2t=4\cos^2t-4\cos t+1+1-\cos^2t=3\cos^2t-4\cos t+2$。令 $u=\cos t\in[-1,1]$，$g(u)=3u^2-4u+2$。$g'(u)=6u-4=0$，$u=\dfrac{2}{3}$（在 $[-1,1]$ 内）。$g\left(\dfrac{2}{3}\right)=3\cdot\dfrac{4}{9}-\dfrac{8}{3}+2=\dfrac{4}{3}-\dfrac{8}{3}+2=\dfrac{2}{3}$；端点 $g(1)=1$，$g(-1)=3+4+2=9$。故 $d_{\min}=\sqrt{\dfrac{2}{3}}$，$d_{\max}=3$。
**答案** 最小值 $\sqrt{\dfrac{2}{3}}$；最大值 $3$
**动画要点** - 椭圆上动点到 $(1,0)$ 的距离变化 - 最值点标注

### test-geom-020 解析几何 · 对称点×平面
**题目** 求点 $P(1,2,3)$ 关于平面 $x+y+z=0$ 的对称点。
**涉及知识点** 投影、对称、法向量
**解答** 法向量 $\vec n=(1,1,1)$，$|\vec n|^2=3$。$P$ 在平面上的投影为 $Q=P-\dfrac{P\cdot\vec n}{|\vec n|^2}\vec n=(1,2,3)-\dfrac{6}{3}(1,1,1)=(1,2,3)-(2,2,2)=(-1,0,1)$。对称点 $P'=2Q-P=(-2,0,2)-(1,2,3)=(-3,-2,-1)$。验证 $Q$ 在平面上：$-1+0+1=0$。
**答案** $(-3,-2,-1)$
**动画要点** - 点、投影、对称点共线 - 平面镜面反射

### test-geom-021 解析几何 · 向量×三角形边角
**题目** 已知向量 $\vec a,\vec b,\vec c$ 满足 $\vec a+\vec b+\vec c=\vec 0$，且 $|\vec a|=3$、$|\vec b|=4$、$|\vec c|=5$。求 $\vec a$ 与 $\vec b$ 的夹角。
**涉及知识点** 向量模长、内积、三角形
**解答** 由 $\vec c=-(\vec a+\vec b)$：$|\vec c|^2=|\vec a|^2+|\vec b|^2+2\vec a\cdot\vec b$。代入：$25=9+16+2\vec a\cdot\vec b$，故 $\vec a\cdot\vec b=0$。$\cos\theta=\dfrac{\vec a\cdot\vec b}{|\vec a||\vec b|}=0$，夹角为 $\dfrac{\pi}{2}$。几何上三向量首尾相接成 $3$-$4$-$5$ 直角三角形（勾股定理逆定理）。
**答案** $\dfrac{\pi}{2}$
**动画要点** - 三向量首尾相接成三角形 - 直角标注

### test-geom-022 解析几何 · 旋转矩阵×正交验证
**题目** 写出绕 $y$ 轴旋转角 $\varphi$ 的旋转矩阵 $R_y(\varphi)$，并验证它是正交矩阵。
**涉及知识点** 旋转矩阵、正交矩阵、行列式
**解答** 绕 $y$ 轴旋转：$x'=x\cos\varphi+z\sin\varphi$，$y'=y$，$z'=-x\sin\varphi+z\cos\varphi$，故 $R_y(\varphi)=\begin{pmatrix}\cos\varphi&0&\sin\varphi\\0&1&0\\-\sin\varphi&0&\cos\varphi\end{pmatrix}$。验证 $R^TR=I$：第一列与第二列点积 $0$、与第三列点积 $\cos\varphi\sin\varphi-\sin\varphi\cos\varphi=0$；各列模长 $\cos^2\varphi+\sin^2\varphi=1$、$1$、$1$。故 $R$ 正交，且 $\det R=1$（旋转保定向）。
**答案** $R_y(\varphi)=\begin{pmatrix}\cos\varphi&0&\sin\varphi\\0&1&0\\-\sin\varphi&0&\cos\varphi\end{pmatrix}$；正交（证毕）
**动画要点** - 绕 $y$ 轴旋转动画 - 列向量标准正交标注

### test-geom-023 解析几何 · 曲面×单位法向量
**题目** 求球面 $x^2+y^2+z^2=4$ 在点 $(1,1,\sqrt2)$ 处的单位外法向量。
**涉及知识点** 梯度、法向量、球面
**解答** $F=x^2+y^2+z^2-4$，$\nabla F=(2x,2y,2z)$。在 $(1,1,\sqrt2)$ 处 $\nabla F=(2,2,2\sqrt2)$，模 $=\sqrt{4+4+8}=4$。单位外法向量 $\vec n=\dfrac{\nabla F}{|\nabla F|}=\left(\dfrac{1}{2},\dfrac{1}{2},\dfrac{\sqrt2}{2}\right)$（若问全部单位法向量则为 $\pm\left(\dfrac{1}{2},\dfrac{1}{2},\dfrac{\sqrt2}{2}\right)$）。
**答案** $\left(\dfrac{1}{2},\dfrac{1}{2},\dfrac{\sqrt2}{2}\right)$
**动画要点** - 球面与径向法向量 - 梯度方向标注

### test-geom-024 解析几何 · 平行平面×距离
**题目** 求两平行平面 $2x-y+2z=1$ 与 $2x-y+2z=7$ 之间的距离。
**涉及知识点** 平行平面距离、点面距离公式
**解答** 在第一个平面上取点（令 $x=z=0$，则 $-y=1$，$y=-1$）$P(0,-1,0)$。$P$ 到第二个平面的距离 $d=\dfrac{|2\cdot 0-(-1)+2\cdot 0-7|}{\sqrt{4+1+4}}=\dfrac{|1-7|}{3}=\dfrac{6}{3}=2$。即两平面距离为 $2$。
**答案** $2$
**动画要点** - 两平行平面与公垂线段 - 距离标注

### test-geom-025 解析几何 · 轨迹×二次曲面
**题目** 求到两定点 $A(1,0,0)$、$B(-1,0,0)$ 距离之和等于 $4$ 的点的轨迹方程，并说明曲面类型。
**涉及知识点** 距离公式、椭球面、轨迹
**解答** 设动点 $P(x,y,z)$，记 $r_1=\sqrt{(x-1)^2+y^2+z^2}$、$r_2=\sqrt{(x+1)^2+y^2+z^2}$，条件为 $r_1+r_2=4$。由 $r_2=4-r_1$ 两边平方：$r_2^2=16-8r_1+r_1^2$。又 $r_2^2-r_1^2=\left[(x+1)^2+y^2+z^2\right]-\left[(x-1)^2+y^2+z^2\right]=(x+1)^2-(x-1)^2=4x$。代入上式：$4x=16-8r_1$，即 $2r_1=4-x$。再平方：$4\left[(x-1)^2+y^2+z^2\right]=(4-x)^2$。展开：$4(x^2-2x+1)+4y^2+4z^2=16-8x+x^2$，整理得 $3x^2+4y^2+4z^2=12$，即 $\dfrac{x^2}{4}+\dfrac{y^2+z^2}{3}=1$。反向验证：由椭球方程得 $3x^2\le 12$，即 $|x|\le 2$，于是 $r_1=\dfrac{4-x}{2}\ge 1$、$r_2=\dfrac{4+x}{2}\ge 1$ 均非负（第二次平方得到的正是 $2r_1=4-x$，故 $r_1=\dfrac{4-x}{2}$ 代入平方前的方程成立，$r_2=4-r_1=\dfrac{4+x}{2}$ 同理），且 $r_1+r_2=4$——椭球上每点都满足原距离和条件，两方程等价。该方程表示绕 $x$ 轴的旋转椭球面：两焦点 $(\pm 1,0,0)$（$c=1$）、长半轴 $a=2$、短半轴 $b=\sqrt{a^2-c^2}=\sqrt3$。
**答案** $\dfrac{x^2}{4}+\dfrac{y^2+z^2}{3}=1$，旋转椭球面
**动画要点** - 两定点与"绳长固定"的椭球生成 - 截面椭圆族

# 三、概率论综合（25 题）

### test-prob-001 概率论 · 全概率公式×贝叶斯公式
**题目** 两车间各承担总产量的 $60\%$ 与 $40\%$，次品率分别为 $2\%$ 与 $3\%$。随机抽取一件产品发现是次品，求它来自第一车间的概率。
**涉及知识点** 全概率公式、贝叶斯公式、条件概率
**解答** 记 $A_1$=来自第一车间，$A_2$=来自第二车间，$B$=次品。$P(A_1)=0.6$，$P(A_2)=0.4$，$P(B|A_1)=0.02$，$P(B|A_2)=0.03$。由全概率公式 $P(B)=0.6\times 0.02+0.4\times 0.03=0.012+0.012=0.024$。由贝叶斯公式 $P(A_1|B)=\dfrac{P(B|A_1)P(A_1)}{P(B)}=\dfrac{0.012}{0.024}=\dfrac{1}{2}$。
**答案** $\dfrac{1}{2}$
**动画要点** - 两车间分支的面积图 - 次品分支的重新归一化

### test-prob-002 概率论 · 二项分布×组合计数
**题目** 设 $X\sim B\!\left(10,\dfrac{3}{10}\right)$。求 $P(X=3)$ 与 $P(X\le 1)$ 的精确值。
**涉及知识点** 二项分布、组合数、概率质量函数
**解答** $P(X=k)=\binom{10}{k}\left(\dfrac{3}{10}\right)^k\left(\dfrac{7}{10}\right)^{10-k}$。$P(X=3)=\binom{10}{3}\cdot 0.3^3\cdot 0.7^7=120\times 0.027\times 0.0823543=0.266827932$。$P(X\le 1)=P(X=0)+P(X=1)=0.7^{10}+10\times 0.3\times 0.7^9=0.0282475249+3\times 0.040353607=0.0282475249+0.121060821=0.1493083459=\dfrac{1493083459}{10^{10}}$。
**答案** $P(X=3)=0.266827932$；$P(X\le 1)=0.1493083459$
**动画要点** - 二项分布柱状图 - 目标柱高亮

### test-prob-003 概率论 · 期望×方差×指示变量
**题目** 用指示变量法推导 $X\sim B(n,p)$ 的期望与方差。
**涉及知识点** 指示变量、期望线性性、方差、独立性
**解答** 设 $X=\displaystyle\sum_{i=1}^{n}X_i$，其中 $X_i$ 为第 $i$ 次试验成功的指示变量（独立，$P(X_i=1)=p$）。$E[X_i]=p$，由期望线性性 $E[X]=np$。$\operatorname{Var}(X_i)=E[X_i^2]-p^2=p-p^2=p(1-p)$。由独立性 $\operatorname{Var}(X)=\displaystyle\sum_{i=1}^{n}\operatorname{Var}(X_i)=np(1-p)$（独立变量的方差可加）。
**答案** $E[X]=np$；$\operatorname{Var}(X)=np(1-p)$
**动画要点** - 指示变量拆解动画 - 方差可加性的示意

### test-prob-004 概率论 · 连续分布×分布函数
**题目** 设 $X$ 的密度为 $f(x)=3x^2$（$0<x<1$）。求 $X$ 的分布函数、$P\!\left(X>\dfrac{1}{2}\right)$ 与 $E[X]$。
**涉及知识点** 连续型随机变量、分布函数、分段函数积分
**解答** 分布函数 $F(x)=\displaystyle\int_0^x3t^2dt=x^3$（$0<x<1$；$x\le 0$ 时为 0，$x\ge 1$ 时为 1）。$P\!\left(X>\dfrac{1}{2}\right)=1-F\!\left(\dfrac{1}{2}\right)=1-\dfrac{1}{8}=\dfrac{7}{8}$。$E[X]=\displaystyle\int_0^1x\cdot 3x^2dx=3\int_0^1x^3dx=\dfrac{3}{4}$。
**答案** $F(x)=\begin{cases}0,&x\le 0\\x^3,&0<x<1\\1,&x\ge 1\end{cases}$；$P\!\left(X>\dfrac12\right)=\dfrac{7}{8}$；$E[X]=\dfrac{3}{4}$
**动画要点** - 密度与分布函数曲线对照 - 概率面积高亮

### test-prob-005 概率论 · 卷积×三角分布
**题目** 设 $X,Y$ 独立同分布于 $U(0,1)$，求 $Z=X+Y$ 的密度与 $P(Z>1.5)$。
**涉及知识点** 卷积、三角分布、分段积分
**解答** $f_Z(z)=\displaystyle\int_0^1 f_X(x)f_Y(z-x)dx=\int_0^1\mathbf 1_{[0,1]}(z-x)dx$。当 $0<z<1$：$f_Z(z)=\displaystyle\int_0^z dx=z$；当 $1\le z<2$：$f_Z(z)=\displaystyle\int_{z-1}^1 dx=2-z$；其余为 0（三角分布）。$P(Z>1.5)=\displaystyle\int_{1.5}^{2}(2-z)dz=\left[2z-\dfrac{z^2}{2}\right]_{1.5}^{2}=\left(4-2\right)-\left(3-\dfrac{2.25}{2}\right)=2-(3-1.125)=0.125=\dfrac{1}{8}$。
**答案** $f_Z(z)=z$（$0<z<1$），$f_Z(z)=2-z$（$1\le z<2$），其余 $z$ 处为 $0$；$P(Z>1.5)=\dfrac{1}{8}$
**动画要点** - 卷积滑动的矩形面积 - 三角密度与尾部高亮

### test-prob-006 概率论 · 泊松分布×级数
**题目** 设 $X\sim\operatorname{Poisson}(4)$。求 $P(X=2)$ 与 $P(X\ge 1)$ 的精确表达式。
**涉及知识点** 泊松分布、对立事件、指数级数
**解答** $P(X=k)=\dfrac{4^ke^{-4}}{k!}$。$P(X=2)=\dfrac{16e^{-4}}{2}=8e^{-4}$。$P(X\ge 1)=1-P(X=0)=1-e^{-4}$（$P(X=0)=\dfrac{4^0e^{-4}}{0!}=e^{-4}$）。
**答案** $P(X=2)=8e^{-4}$；$P(X\ge 1)=1-e^{-4}$
**动画要点** - 泊松柱状图 - 尾部概率高亮

### test-prob-007 概率论 · 指数分布×无记忆性
**题目** 某灯泡寿命 $T\sim\operatorname{Exp}\!\left(\dfrac{1}{1000}\right)$（单位：小时，参数 $\lambda=\dfrac{1}{1000}$）。求 $P(T>1500\mid T>500)$。
**涉及知识点** 指数分布、无记忆性、条件概率
**解答** 指数分布无记忆性：$P(T>s+t\mid T>s)=P(T>t)=e^{-\lambda t}$。取 $s=500$、$t=1000$：$P(T>1500\mid T>500)=P(T>1000)=e^{-1000/1000}=e^{-1}$。直接验证：$P(T>1500)=e^{-1.5}$，$P(T>500)=e^{-0.5}$，比值 $=\dfrac{e^{-1.5}}{e^{-0.5}}=e^{-1}$。
**答案** $e^{-1}$
**动画要点** - 生存函数曲线右移重合 - 条件概率的面积比

### test-prob-008 概率论 · 切比雪夫×大数定律
**题目** 掷均匀骰子 $n$ 次，设 $\bar X_n$ 为平均点数。用切比雪夫不等式给出 $P\!\left(|\bar X_n-3.5|\ge 0.1\right)$ 的上界，并说明 $n\to\infty$ 时该概率趋于 $0$（弱大数定律）。
**涉及知识点** 切比雪夫不等式、弱大数定律、均匀分布数字特征
**解答** 单次点数 $X$：$E[X]=\dfrac{7}{2}$，$\operatorname{Var}(X)=\dfrac{35}{12}$。$\bar X_n$ 的方差 $=\dfrac{35}{12n}$。由切比雪夫不等式 $P\!\left(|\bar X_n-E[\bar X_n]|\ge\varepsilon\right)\le\dfrac{\operatorname{Var}(\bar X_n)}{\varepsilon^2}$，取 $\varepsilon=0.1$：$P\!\left(|\bar X_n-3.5|\ge 0.1\right)\le\dfrac{35/12n}{0.01}=\dfrac{35}{0.12n}=\dfrac{875}{3n}$（$\approx\dfrac{291.67}{n}$）。概率不超过 1，完整上界为 $\min\left\{1,\dfrac{875}{3n}\right\}$。当 $n\to\infty$ 时上界趋于 $0$，故概率趋于 $0$（弱大数定律：样本均值依概率收敛于期望）。
**答案** 上界 $\min\left\{1,\dfrac{875}{3n}\right\}$；$n\to\infty$ 时趋于 $0$
**动画要点** - 样本均值轨迹收敛于 3.5 - 上界随 $n$ 衰减曲线

### test-prob-009 概率论 · 正态分布×线性变换
**题目** 设 $X\sim N(2,3)$（均值 2、方差 3），$Y=2X-1$。求 $Y$ 的分布与 $P(Y>3)$。
**涉及知识点** 正态分布线性变换、标准化、分布函数
**解答** 正态分布在线性变换下仍为正态：$E[Y]=2E[X]-1=3$，$\operatorname{Var}(Y)=4\operatorname{Var}(X)=12$，故 $Y\sim N(3,12)$。标准化 $Z=\dfrac{Y-3}{\sqrt{12}}\sim N(0,1)$。$P(Y>3)=P\!\left(Z>\dfrac{3-3}{\sqrt{12}}\right)=P(Z>0)=\dfrac{1}{2}$（标准正态关于 0 对称）。
**答案** $Y\sim N(3,12)$；$P(Y>3)=\dfrac{1}{2}$
**动画要点** - 线性变换前后密度曲线 - 对称性与 $1/2$ 面积

### test-prob-010 概率论 · 协方差×相关系数
**题目** 设 $X\sim U(0,1)$，$Y=X^2$。求 $\operatorname{Cov}(X,Y)$ 与相关系数 $\rho(X,Y)$。
**涉及知识点** 协方差、相关系数、均匀分布
**解答** $E[X]=\dfrac{1}{2}$，$E[X^2]=\dfrac{1}{3}$，$E[X^3]=\dfrac{1}{4}$，$E[X^4]=\dfrac{1}{5}$。$\operatorname{Cov}(X,Y)=E[X^3]-E[X]E[X^2]=\dfrac{1}{4}-\dfrac{1}{2}\cdot\dfrac{1}{3}=\dfrac{1}{4}-\dfrac{1}{6}=\dfrac{1}{12}$。$\operatorname{Var}(X)=\dfrac{1}{12}$，$\operatorname{Var}(Y)=E[X^4]-(E[X^2])^2=\dfrac{1}{5}-\dfrac{1}{9}=\dfrac{4}{45}$。$\rho=\dfrac{\operatorname{Cov}}{\sqrt{\operatorname{Var}(X)\operatorname{Var}(Y)}}=\dfrac{1/12}{\sqrt{\frac{1}{12}\cdot\frac{4}{45}}}=\dfrac{1/12}{\sqrt{1/135}}=\dfrac{\sqrt{135}}{12}=\dfrac{3\sqrt{15}}{12}=\dfrac{\sqrt{15}}{4}$。
**答案** $\operatorname{Cov}(X,Y)=\dfrac{1}{12}$；$\rho=\dfrac{\sqrt{15}}{4}$
**动画要点** - $y=x^2$ 上的散点 - 正相关的可视化

### test-prob-011 概率论 · 条件期望×二维均匀
**题目** $(X,Y)$ 在三角形 $D=\{(x,y):x\ge 0,\ y\ge 0,\ x+y\le 2\}$ 上均匀分布。求条件密度 $f_{Y|X}(y|x)$ 与 $E[Y|X=x]$，并求 $E[Y]$。
**涉及知识点** 二维均匀、条件分布、条件期望
**解答** $D$ 面积为 $\dfrac{1}{2}\cdot 2\cdot 2=2$，联合密度 $f(x,y)=\dfrac{1}{2}$（$(x,y)\in D$）。边缘密度 $f_X(x)=\displaystyle\int_0^{2-x}\dfrac{1}{2}dy=\dfrac{2-x}{2}$（$0<x<2$）。条件密度 $f_{Y|X}(y|x)=\dfrac{f(x,y)}{f_X(x)}=\dfrac{1}{2-x}$（$0<y<2-x$，即在 $(0,2-x)$ 上均匀）。$E[Y|X=x]=\dfrac{2-x}{2}$。$E[Y]=\displaystyle\int_0^2E[Y|X=x]f_X(x)dx=\int_0^2\dfrac{2-x}{2}\cdot\dfrac{2-x}{2}dx=\dfrac{1}{4}\int_0^2(2-x)^2dx=\dfrac{1}{4}\cdot\dfrac{8}{3}=\dfrac{2}{3}$。
**答案** $0<x<2$ 时，$f_{Y|X}(y|x)=\dfrac{1}{2-x}$（$0<y<2-x$，其余 $y$ 处为 0）；$E[Y|X=x]=\dfrac{2-x}{2}$；$E[Y]=\dfrac{2}{3}$
**动画要点** - 三角形区域与条件切片 - 条件期望随 $x$ 变化的直线

### test-prob-012 概率论 · 超几何分布×组合
**题目** 袋中有 3 个红球、2 个白球，不放回地抽取 2 个。求恰抽到一红一白的概率。
**涉及知识点** 超几何分布、组合计数、对称性
**解答** 样本空间为从 5 球中取 2 球，共 $C_5^2=10$ 种等可能结果。恰一红一白：$C_3^1\cdot C_2^1=6$ 种。故 $P=\dfrac{6}{10}=\dfrac{3}{5}$。（超几何分布公式 $P=\dfrac{\binom{3}{1}\binom{2}{1}}{\binom{5}{2}}=\dfrac{3}{5}$。）
**答案** $\dfrac{3}{5}$
**动画要点** - 抽取过程的树状图 - 有利分支高亮

### test-prob-013 概率论 · 矩母函数×数字特征
**题目** 设 $X\sim\operatorname{Poisson}(\lambda)$。求矩母函数 $M(t)$，并用它求 $E[X]$ 与 $E[X^2]$。
**涉及知识点** 矩母函数、指数级数、矩的计算
**解答** $M(t)=E[e^{tX}]=\displaystyle\sum_{k=0}^{\infty}e^{tk}\dfrac{\lambda^ke^{-\lambda}}{k!}=e^{-\lambda}\sum_{k=0}^{\infty}\dfrac{(\lambda e^t)^k}{k!}=e^{-\lambda}e^{\lambda e^t}=e^{\lambda(e^t-1)}$。$M'(t)=M(t)\cdot\lambda e^t$，$M'(0)=\lambda$，故 $E[X]=\lambda$。$M''(t)=M(t)\left[(\lambda e^t)^2+\lambda e^t\right]$，$M''(0)=\lambda^2+\lambda$，故 $E[X^2]=\lambda^2+\lambda$（与 eval-prob-006 一致）。
**答案** $M(t)=e^{\lambda(e^t-1)}$；$E[X]=\lambda$；$E[X^2]=\lambda^2+\lambda$
**动画要点** - 矩母函数曲线 - 导数与矩的对应

### test-prob-014 概率论 · 几何分布×期望递推
**题目** 掷均匀骰子直到出现 6 为止。求所需投掷次数的期望。
**涉及知识点** 几何分布、期望递推、无记忆性
**解答** 设 $E$ 为期望次数。第一次若为 6（概率 $\dfrac{1}{6}$），总次数 1；否则（概率 $\dfrac{5}{6}$）回到初始状态，总次数 $1+E$。故 $E=\dfrac{1}{6}\cdot 1+\dfrac{5}{6}\cdot(1+E)=1+\dfrac{5E}{6}$，解得 $E=6$。（几何分布 $p=\dfrac{1}{6}$ 的期望 $\dfrac{1}{p}=6$。）
**答案** $6$
**动画要点** - 树状图与"回到原点"分支 - 期望自指方程

### test-prob-015 概率论 · 独立事件×几何分布
**题目** 甲乙两人独立地抛硬币直到各自出现正面为止。求两人在同一时刻停止的概率。
**涉及知识点** 几何分布、独立性、几何级数
**解答** 设两人停止时刻为 $X,Y$，独立同分布于 $\operatorname{Geom}\!\left(\dfrac{1}{2}\right)$，$P(X=k)=P(Y=k)=\left(\dfrac{1}{2}\right)^k$。$P(X=Y)=\displaystyle\sum_{k=1}^{\infty}P(X=k)P(Y=k)=\sum_{k=1}^{\infty}\left(\dfrac{1}{2}\right)^{2k}=\sum_{k=1}^{\infty}\left(\dfrac{1}{4}\right)^k=\dfrac{1/4}{1-1/4}=\dfrac{1}{3}$。
**答案** $\dfrac{1}{3}$
**动画要点** - 两人抛硬币过程同步 - 同时停止的计数

### test-prob-016 概率论 · 马尔可夫链×稳态分布
**题目** 某地天气的转移矩阵为 $P=\begin{pmatrix}0.8&0.2\\0.4&0.6\end{pmatrix}$（状态 1 晴、状态 2 雨，行表示今天）。求稳态分布。
**涉及知识点** 马尔可夫链、稳态分布、特征向量
**解答** 稳态分布 $\pi=(\pi_1,\pi_2)$ 满足 $\pi=\pi P$ 且 $\pi_1+\pi_2=1$：$\pi_1=0.8\pi_1+0.4\pi_2$，即 $0.2\pi_1=0.4\pi_2$，$\pi_1=2\pi_2$。由 $\pi_1+\pi_2=1$：$3\pi_2=1$，$\pi_2=\dfrac{1}{3}$，$\pi_1=\dfrac{2}{3}$。故稳态分布 $\left(\dfrac{2}{3},\dfrac{1}{3}\right)$。
**答案** $\left(\dfrac{2}{3},\dfrac{1}{3}\right)$
**动画要点** - 状态转移图 - 分布向稳态收敛

### test-prob-017 概率论 · 二维均匀×次序统计量
**题目** 设 $X,Y$ 独立同分布于 $U(0,1)$。求 $M=\max(X,Y)$ 的分布函数，并求 $E[M]$。
**涉及知识点** 次序统计量、二维均匀、分布函数
**解答** $F_M(t)=P(\max(X,Y)\le t)=P(X\le t)P(Y\le t)=t^2$（$0<t<1$，$t\le 0$ 为 0、$t\ge 1$ 为 1）。密度 $f_M(t)=2t$（$0<t<1$）。$E[M]=\displaystyle\int_0^1t\cdot 2t\,dt=\dfrac{2}{3}$。
**答案** $F_M(t)=\begin{cases}0,&t\le 0\\t^2,&0<t<1\\1,&t\ge 1\end{cases}$；$E[M]=\dfrac{2}{3}$
**动画要点** - 单位正方形中 $\max\le t$ 的小正方形 - 密度 $2t$ 曲线

### test-prob-018 概率论 · 矩母函数×反常积分
**题目** 设 $X\sim\operatorname{Exp}(\lambda)$。求 $E[e^{tX}]$ 的收敛条件与表达式。
**涉及知识点** 矩母函数、反常积分、指数函数
**解答** $M(t)=E[e^{tX}]=\displaystyle\int_0^{\infty}e^{tx}\lambda e^{-\lambda x}dx=\lambda\int_0^{\infty}e^{(t-\lambda)x}dx$。当 $t<\lambda$ 时收敛：$M(t)=\lambda\cdot\dfrac{1}{\lambda-t}=\dfrac{\lambda}{\lambda-t}$；当 $t\ge\lambda$ 时积分发散（$t=\lambda$ 时 $\int\lambda\,dx$ 发散）。收敛条件 $t<\lambda$ 恰对应"指数增长阶小于衰减率"。
**答案** $M(t)=\dfrac{\lambda}{\lambda-t}$（$t<\lambda$）
**动画要点** - 被积函数随 $t$ 逼近 $\lambda$ 的变化 - 收敛域标注

### test-prob-019 概率论 · 均匀分布×次序统计量
**题目** 设 $X_1,\dots,X_5$ 独立同分布于 $U(0,1)$。求 $E[\min X_i]$ 与 $E[\max X_i]$。
**涉及知识点** 次序统计量、均匀分布、期望
**解答** $P(\max\le t)=t^5$，密度 $5t^4$，$E[\max]=\displaystyle\int_0^1t\cdot 5t^4dt=\dfrac{5}{6}$。$P(\min>t)=(1-t)^5$，故 $F_{\min}(t)=1-(1-t)^5$，密度 $5(1-t)^4$，$E[\min]=\displaystyle\int_0^1t\cdot 5(1-t)^4dt$。令 $u=1-t$：$=5\displaystyle\int_0^1(1-u)u^4du=5\left(\dfrac{1}{5}-\dfrac{1}{6}\right)=1-\dfrac{5}{6}=\dfrac{1}{6}$。
**答案** $E[\min]=\dfrac{1}{6}$；$E[\max]=\dfrac{5}{6}$
**动画要点** - 五个样本点的最值标注 - 对称性 $1/6$ 与 $5/6$

### test-prob-020 概率论 · 组合×期望
**题目** 口袋里有 10 把钥匙，其中只有 1 把能开门，逐一不放回尝试。求打开门所需尝试次数的期望。
**涉及知识点** 对称性、期望、均匀分布
**解答** 正确钥匙在尝试序列中的位置 $X$ 在 $\{1,2,\dots,10\}$ 上均匀（等可能排在第 $k$ 次）。$E[X]=\dfrac{1+10}{2}=\dfrac{11}{2}=5.5$。
**答案** $\dfrac{11}{2}$
**动画要点** - 逐一尝试的动画 - 位置均匀性示意

### test-prob-021 概率论 · 独立性×概率运算
**题目** 设 $A,B$ 独立，$P(A)=0.4$，$P(A\cup B)=0.7$。求 $P(B)$。
**涉及知识点** 独立性、加法公式、解方程
**解答** 加法公式：$P(A\cup B)=P(A)+P(B)-P(A\cap B)$。由独立性 $P(A\cap B)=P(A)P(B)=0.4P(B)$。代入：$0.7=0.4+P(B)-0.4P(B)=0.4+0.6P(B)$，故 $P(B)=\dfrac{0.3}{0.6}=0.5$。
**答案** $0.5$
**动画要点** - 韦恩图与面积方程 - 独立性约束

### test-prob-022 概率论 · 方差×协方差
**题目** 掷两枚均匀骰子，设 $X$ 为两数之和。求 $\operatorname{Var}(X)$。
**涉及知识点** 方差、独立性、均匀分布
**解答** 设 $X=X_1+X_2$，$X_1,X_2$ 独立同分布（单次骰子），$\operatorname{Var}(X_i)=\dfrac{35}{12}$（eval-prob-015）。由独立性 $\operatorname{Var}(X)=\operatorname{Var}(X_1)+\operatorname{Var}(X_2)=\dfrac{35}{12}+\dfrac{35}{12}=\dfrac{35}{6}$。直接验证：$E[X]=7$，$E[X^2]=\displaystyle\sum_{k=2}^{12}k^2P(X=k)=\dfrac{1974}{36}=\dfrac{329}{6}$，$\operatorname{Var}(X)=\dfrac{329}{6}-49=\dfrac{329-294}{6}=\dfrac{35}{6}$，一致。
**答案** $\dfrac{35}{6}$
**动画要点** - 两骰子和的分布柱状图 - 方差叠加示意

### test-prob-023 概率论 · 几何概型×积分
**题目** 布丰投针：平面上画有间距为 $d$ 的平行线，投掷长为 $l$（$l\le d$）的针。求针与任一直线相交的概率。
**涉及知识点** 几何概型、二元均匀、三角积分
**解答** 设针中点到最近平行线的距离为 $x\sim U\!\left(0,\dfrac{d}{2}\right)$，针与平行线的夹角为 $\theta\sim U\!\left(0,\dfrac{\pi}{2}\right)$，两者独立。相交条件：$x\le\dfrac{l}{2}\sin\theta$。联合密度 $f(x,\theta)=\dfrac{2}{d}\cdot\dfrac{2}{\pi}$。相交概率 $P=\dfrac{4}{\pi d}\displaystyle\int_0^{\pi/2}\!\!\int_0^{(l/2)\sin\theta}dx\,d\theta=\dfrac{4}{\pi d}\int_0^{\pi/2}\dfrac{l}{2}\sin\theta\,d\theta=\dfrac{2l}{\pi d}\left[-\cos\theta\right]_0^{\pi/2}=\dfrac{2l}{\pi d}$。
**答案** $\dfrac{2l}{\pi d}$
**动画要点** - 随机投针动画 - 相交区域的面积

### test-prob-024 概率论 · 泊松分布×泰勒展开
**题目** 证明泊松分布的概率质量函数归一化：$\displaystyle\sum_{k=0}^{\infty}\frac{\lambda^ke^{-\lambda}}{k!}=1$，并用阶乘矩求 $\operatorname{Var}(X)$（$X\sim\operatorname{Poisson}(\lambda)$）。
**涉及知识点** 泊松分布、指数级数、阶乘矩
**解答** 归一化：$\displaystyle\sum_{k=0}^{\infty}\dfrac{\lambda^ke^{-\lambda}}{k!}=e^{-\lambda}\sum_{k=0}^{\infty}\dfrac{\lambda^k}{k!}=e^{-\lambda}\cdot e^{\lambda}=1$（$e^\lambda$ 的泰勒展开）。阶乘矩：$E[X(X-1)]=\displaystyle\sum_{k=2}^{\infty}k(k-1)\dfrac{\lambda^ke^{-\lambda}}{k!}=\lambda^2e^{-\lambda}\sum_{k=2}^{\infty}\dfrac{\lambda^{k-2}}{(k-2)!}=\lambda^2e^{-\lambda}e^{\lambda}=\lambda^2$。故 $E[X^2]=E[X(X-1)]+E[X]=\lambda^2+\lambda$，$\operatorname{Var}(X)=E[X^2]-\lambda^2=\lambda$。
**答案** 证毕；$\operatorname{Var}(X)=\lambda$
**动画要点** - 泊松柱状图归一 - 阶乘矩求和的重整化

### test-prob-025 概率论 · 期望×博弈模型
**题目** 掷一枚均匀骰子得 $X$ 分；若 $X=6$ 则可再掷一次并将点数累加。求总得分的期望。
**涉及知识点** 条件期望、期望线性性、全期望公式
**解答** 设总得分为 $Y$。第一次掷出 $X$；若 $X=6$ 则加第二次的 $Z$（与 $X$ 独立同分布）。$E[Y]=E[X]+E[\mathbf 1_{\{X=6\}}Z]=E[X]+P(X=6)E[Z]=\dfrac{7}{2}+\dfrac{1}{6}\cdot\dfrac{7}{2}=\dfrac{7}{2}\left(1+\dfrac{1}{6}\right)=\dfrac{7}{2}\cdot\dfrac{7}{6}=\dfrac{49}{12}$。
**答案** $\dfrac{49}{12}$
**动画要点** - 掷骰分支的树状图 - 期望拆分示意

# 四、高等代数综合（40 题）

### test-linalg-001 高等代数 · 行列式×线性方程组
**题目** 用 Cramer 法则解方程组 $\begin{cases}2x+y-z=1\\x-y+z=2\\x+2y+z=4\end{cases}$。
**涉及知识点** Cramer 法则、三阶行列式、方程组
**解答** 系数行列式 $D=\begin{vmatrix}2&1&-1\\1&-1&1\\1&2&1\end{vmatrix}=2\cdot(-1-2)-1\cdot(1-1)+(-1)\cdot(2+1)=-6-0-3=-9$。$D_x=\begin{vmatrix}1&1&-1\\2&-1&1\\4&2&1\end{vmatrix}=1\cdot(-1-2)-1\cdot(2-4)+(-1)\cdot(4+4)=-3+2-8=-9$，$x=\dfrac{D_x}{D}=\dfrac{-9}{-9}=1$。$D_y=\begin{vmatrix}2&1&-1\\1&2&1\\1&4&1\end{vmatrix}=2\cdot(2-4)-1\cdot(1-1)+(-1)\cdot(4-2)=-4-0-2=-6$，$y=\dfrac{-6}{-9}=\dfrac{2}{3}$。$D_z=\begin{vmatrix}2&1&1\\1&-1&2\\1&2&4\end{vmatrix}=2\cdot(-4-4)-1\cdot(4-2)+1\cdot(2+1)=-16-2+3=-15$，$z=\dfrac{-15}{-9}=\dfrac{5}{3}$。验证：$2\cdot 1+\dfrac{2}{3}-\dfrac{5}{3}=1$；$1-\dfrac{2}{3}+\dfrac{5}{3}=2$；$1+\dfrac{4}{3}+\dfrac{5}{3}=4$。
**答案** $(x,y,z)=\left(1,\dfrac{2}{3},\dfrac{5}{3}\right)$
**动画要点** - 三个行列式的并行计算 - 解的三平面交点

### test-linalg-002 高等代数 · 矩阵方程×逆矩阵
**题目** 解矩阵方程 $AX=B$，其中 $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$，$B=\begin{pmatrix}3\\3\end{pmatrix}$。
**涉及知识点** 矩阵方程、逆矩阵、矩阵乘法
**解答** $\det A=4-1=3$，$A^{-1}=\dfrac{1}{3}\begin{pmatrix}2&-1\\-1&2\end{pmatrix}$。$X=A^{-1}B=\dfrac{1}{3}\begin{pmatrix}2&-1\\-1&2\end{pmatrix}\begin{pmatrix}3\\3\end{pmatrix}=\dfrac{1}{3}\begin{pmatrix}6-3\\-3+6\end{pmatrix}=\begin{pmatrix}1\\1\end{pmatrix}$。验证：$AX=\begin{pmatrix}2&1\\1&2\end{pmatrix}\begin{pmatrix}1\\1\end{pmatrix}=\begin{pmatrix}3\\3\end{pmatrix}=B$。
**答案** $X=\begin{pmatrix}1\\1\end{pmatrix}$
**动画要点** - 矩阵乘法的行列运算 - 验证回代

### test-linalg-003 高等代数 · 分块结构×矩阵幂
**题目** 设 $A=\begin{pmatrix}1&2\\0&1\end{pmatrix}$，求 $A^n$（$n$ 为正整数）。
**涉及知识点** 幂零矩阵、二项式定理、矩阵幂
**解答** $A=I+N$，其中 $N=\begin{pmatrix}0&2\\0&0\end{pmatrix}$ 满足 $N^2=0$。$I$ 与 $N$ 可交换，由二项式定理 $A^n=(I+N)^n=I+nN=\begin{pmatrix}1&2n\\0&1\end{pmatrix}$。
**答案** $\begin{pmatrix}1&2n\\0&1\end{pmatrix}$
**动画要点** - 剪切变换重复作用 - 二项式展开只留两项

### test-linalg-004 高等代数 · 秩×零度
**题目** 设线性变换 $T:\mathbb R^4\to\mathbb R^3$ 的矩阵为 $\begin{pmatrix}1&0&1&0\\0&1&1&0\\1&1&2&0\end{pmatrix}$。求 $\operatorname{rank}T$ 与 $\dim\ker T$。
**涉及知识点** 矩阵的秩、秩-零化度定理、行变换
**解答** 第三行 $=$ 第一行 $+$ 第二行，且第一、二行线性无关，故 $\operatorname{rank}T=2$。由秩-零化度定理 $\dim\ker T=4-2=2$。核方程：$x_1+x_3=0$、$x_2+x_3=0$，即 $x_3$ 与 $x_4$ 自由，$\ker T=\operatorname{span}\{(-1,-1,1,0)^T,(0,0,0,1)^T\}$，维数 2。
**答案** $\operatorname{rank}T=2$；$\dim\ker T=2$
**动画要点** - 行变换消元 - 核空间与像空间的维数对应

### test-linalg-005 高等代数 · 特征值×迹与行列式
**题目** 已知 3 阶方阵 $A$ 的特征值为 $1,2,3$。求 $\operatorname{tr}A$、$\det A$、$\operatorname{tr}(A^2)$ 及 $A^{-1}$ 的特征值。
**涉及知识点** 特征值性质、迹、行列式、逆矩阵
**解答** $\operatorname{tr}A=1+2+3=6$。$\det A=1\cdot 2\cdot 3=6$。$A^2$ 的特征值为 $1^2,2^2,3^2$，故 $\operatorname{tr}(A^2)=1+4+9=14$。$A^{-1}$ 的特征值为 $1,\dfrac{1}{2},\dfrac{1}{3}$（$A$ 可逆因特征值全非零）。
**答案** $\operatorname{tr}A=6$；$\det A=6$；$\operatorname{tr}(A^2)=14$；$A^{-1}$ 的特征值 $1,\dfrac{1}{2},\dfrac{1}{3}$
**动画要点** - 特征值在数轴上的位置 - 谱与不变量对照

### test-linalg-006 高等代数 · 相似对角化×矩阵幂
**题目** 设 $A=P\begin{pmatrix}2&0\\0&3\end{pmatrix}P^{-1}$。求 $A^{10}$ 的表达式（用 $P$ 表示）。
**涉及知识点** 相似对角化、矩阵幂、分块
**解答** $A^{10}=\left(PDP^{-1}\right)^{10}=PD^{10}P^{-1}$（中间项 $P^{-1}P=I$ 逐对抵消）。$D^{10}=\begin{pmatrix}2^{10}&0\\0&3^{10}\end{pmatrix}=\begin{pmatrix}1024&0\\0&59049\end{pmatrix}$。故 $A^{10}=P\begin{pmatrix}1024&0\\0&59049\end{pmatrix}P^{-1}$。
**答案** $A^{10}=P\begin{pmatrix}1024&0\\0&59049\end{pmatrix}P^{-1}$
**动画要点** - $PDP^{-1}$ 连乘的抵消动画 - 对角元逐次幂

### test-linalg-007 高等代数 · 二次型×特征值×最值
**题目** 求二次型 $f(x,y)=x^2+4y^2$ 在单位圆 $x^2+y^2=1$ 上的最大值与最小值。
**涉及知识点** 瑞利商、特征值、条件极值
**解答** 二次型矩阵 $A=\begin{pmatrix}1&0\\0&4\end{pmatrix}$，其特征值为 $1$ 与 $4$。由瑞利商性质，$\lambda_{\min}\le\dfrac{f}{x^2+y^2}\le\lambda_{\max}$，故在单位圆上 $1\le f\le 4$。最小值 $1$ 在 $(x,y)=(\pm 1,0)$ 处取得（特征值 1 的特征向量），最大值 $4$ 在 $(0,\pm 1)$ 处取得。或直接：$f=x^2+4(1-x^2)=4-3x^2$，$x\in[-1,1]$，最小 $1$（$|x|=1$）、最大 $4$（$x=0$）。
**答案** 最小值 $1$；最大值 $4$
**动画要点** - 单位圆上的 $f$ 值色彩映射 - 极值点标注

### test-linalg-008 高等代数 · Cayley–Hamilton×逆矩阵
**题目** 设 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$。利用 Cayley–Hamilton 定理求 $A^{-1}$。
**涉及知识点** Cayley–Hamilton 定理、特征多项式、逆矩阵
**解答** 特征多项式 $\chi(\lambda)=\lambda^2-2\lambda-3$。由 C–H 定理 $A^2-2A-3I=0$，即 $A(A-2I)=3I$。故 $A^{-1}=\dfrac{1}{3}(A-2I)=\dfrac{1}{3}\begin{pmatrix}-1&2\\2&-1\end{pmatrix}=\begin{pmatrix}-\frac{1}{3}&\frac{2}{3}\\\frac{2}{3}&-\frac{1}{3}\end{pmatrix}$。验证：$AA^{-1}=\begin{pmatrix}1&2\\2&1\end{pmatrix}\cdot\dfrac{1}{3}\begin{pmatrix}-1&2\\2&-1\end{pmatrix}=\dfrac{1}{3}\begin{pmatrix}3&0\\0&3\end{pmatrix}=I$。
**答案** $A^{-1}=\dfrac{1}{3}\begin{pmatrix}-1&2\\2&-1\end{pmatrix}$
**动画要点** - $A^2-2A-3I=0$ 的代入过程 - 从多项式恒等式提取逆矩阵

### test-linalg-009 高等代数 · 正交投影×投影矩阵
**题目** 求 $\mathbb R^2$ 中沿方向 $u=(1,1)^T$ 的投影矩阵，并求 $(3,1)^T$ 的投影。
**涉及知识点** 投影矩阵、外积、单位向量
**解答** 单位方向 $\hat u=\dfrac{1}{\sqrt2}(1,1)^T$。投影矩阵 $P=\hat u\hat u^T=\dfrac{1}{2}\begin{pmatrix}1&1\\1&1\end{pmatrix}=\begin{pmatrix}\frac{1}{2}&\frac{1}{2}\\\frac{1}{2}&\frac{1}{2}\end{pmatrix}$。$P\begin{pmatrix}3\\1\end{pmatrix}=\begin{pmatrix}\frac{1}{2}&\frac{1}{2}\\\frac{1}{2}&\frac{1}{2}\end{pmatrix}\begin{pmatrix}3\\1\end{pmatrix}=\begin{pmatrix}2\\2\end{pmatrix}$。验证 $P^2=P$（幂等）且 $(3,1)^T-(2,2)^T=(1,-1)^T\perp(1,1)^T$。
**答案** $P=\begin{pmatrix}\frac{1}{2}&\frac{1}{2}\\\frac{1}{2}&\frac{1}{2}\end{pmatrix}$；投影为 $(2,2)^T$
**动画要点** - 向量沿 $y=x$ 方向的投影 - 垂足与正交分解

### test-linalg-010 高等代数 · QR 分解×Gram–Schmidt
**题目** 求 $A=\begin{pmatrix}1&1\\1&0\end{pmatrix}$ 的 QR 分解。
**涉及知识点** Gram–Schmidt 正交化、QR 分解
**解答** $a_1=(1,1)^T$：$q_1=\dfrac{a_1}{\|a_1\|}=\dfrac{1}{\sqrt2}(1,1)^T$，$r_{11}=\|a_1\|=\sqrt2$，$r_{12}=q_1^Ta_2=\dfrac{1+0}{\sqrt2}=\dfrac{1}{\sqrt2}$。$a_2-r_{12}q_1=(1,0)^T-\dfrac{1}{2}(1,1)^T=\left(\dfrac{1}{2},-\dfrac{1}{2}\right)^T$，$r_{22}=\sqrt{\dfrac{1}{4}+\dfrac{1}{4}}=\dfrac{1}{\sqrt2}$，$q_2=\left(\dfrac{1}{2},-\dfrac{1}{2}\right)^T\Big/\dfrac{1}{\sqrt2}=\dfrac{1}{\sqrt2}(1,-1)^T$。故 $A=QR$，其中 $Q=\dfrac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$，$R=\begin{pmatrix}\sqrt2&\frac{1}{\sqrt2}\\0&\frac{1}{\sqrt2}\end{pmatrix}$。验证：$QR=\dfrac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}\begin{pmatrix}\sqrt2&\frac{1}{\sqrt2}\\0&\frac{1}{\sqrt2}\end{pmatrix}=\begin{pmatrix}1&1\\1&0\end{pmatrix}$。
**答案** $Q=\dfrac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$，$R=\begin{pmatrix}\sqrt2&\frac{1}{\sqrt2}\\0&\frac{1}{\sqrt2}\end{pmatrix}$
**动画要点** - 两列的 Gram–Schmidt 步骤 - $Q$ 正交、$R$ 上三角的标注

### test-linalg-011 高等代数 · 最小二乘×法方程
**题目** 用最小二乘法拟合数据点 $(1,2),(2,4),(3,7)$ 的直线 $y=ax+b$。
**涉及知识点** 最小二乘、法方程、矩阵
**解答** $A=\begin{pmatrix}1&1\\2&1\\3&1\end{pmatrix}$，$\vec b=(2,4,7)^T$。法方程 $A^TA\vec x=A^T\vec b$：$A^TA=\begin{pmatrix}14&6\\6&3\end{pmatrix}$，$A^T\vec b=\begin{pmatrix}31\\13\end{pmatrix}$。解 $\begin{cases}14a+6b=31\\6a+3b=13\end{cases}$：由第二式 $2a+b=\dfrac{13}{3}$，$b=\dfrac{13}{3}-2a$。代入第一式：$14a+6\left(\dfrac{13}{3}-2a\right)=31$，即 $14a+26-12a=31$，$2a=5$，$a=\dfrac{5}{2}$，$b=\dfrac{13}{3}-5=-\dfrac{2}{3}$。拟合直线 $y=\dfrac{5}{2}x-\dfrac{2}{3}$。验证：$x=1,2,3$ 时预测值 $\dfrac{11}{6},\dfrac{13}{3},\dfrac{41}{6}$，残差平方和 $\left(\dfrac{1}{6}\right)^2+\left(-\dfrac{1}{3}\right)^2+\left(\dfrac{1}{6}\right)^2=\dfrac{1}{6}$。
**答案** $y=\dfrac{5}{2}x-\dfrac{2}{3}$
**动画要点** - 数据点与拟合直线 - 残差线段最小化

### test-linalg-012 高等代数 · 特征值×递推数列
**题目** 用矩阵方法求斐波那契数列 $F_1=F_2=1$，$F_{n+2}=F_{n+1}+F_n$ 中 $F_{10}$ 的值，并说明增长比趋于黄金比。
**涉及知识点** 矩阵幂、特征值、斐波那契数列
**解答** 状态矩阵 $A=\begin{pmatrix}1&1\\1&0\end{pmatrix}$ 满足 $\begin{pmatrix}F_{n+1}\\F_n\end{pmatrix}=A\begin{pmatrix}F_n\\F_{n-1}\end{pmatrix}$，故 $\begin{pmatrix}F_{n+1}\\F_n\end{pmatrix}=A^{n-1}\begin{pmatrix}F_2\\F_1\end{pmatrix}=A^{n}\begin{pmatrix}F_1\\F_0\end{pmatrix}$（$F_0=0$）。归纳得 $A^n=\begin{pmatrix}F_{n+1}&F_n\\F_n&F_{n-1}\end{pmatrix}$：$A^2=\begin{pmatrix}2&1\\1&1\end{pmatrix}=\begin{pmatrix}F_3&F_2\\F_2&F_1\end{pmatrix}$。故 $A^{10}=\begin{pmatrix}F_{11}&F_{10}\\F_{10}&F_9\end{pmatrix}$。直接递推：$1,1,2,3,5,8,13,21,34,55$，$F_{10}=55$。特征值：$\chi(\lambda)=\lambda^2-\lambda-1=0$，$\lambda_1=\dfrac{1+\sqrt5}{2}=\varphi\approx 1.618$，$\lambda_2=\dfrac{1-\sqrt5}{2}$，故 $F_n\sim\dfrac{\varphi^n}{\sqrt5}$，$\dfrac{F_{n+1}}{F_n}\to\varphi$。
**答案** $F_{10}=55$；增长比趋于 $\dfrac{1+\sqrt5}{2}$
**动画要点** - 斐波那契递推与矩阵幂 - 比值逼近黄金比

### test-linalg-013 高等代数 · 三对角行列式×周期性
**题目** 求 $n$ 阶三对角行列式 $D_n=\begin{vmatrix}1&1&0&\cdots&0\\1&1&1&\cdots&0\\0&1&1&\cdots&0\\\vdots&&&\ddots&\vdots\\0&0&\cdots&1&1\end{vmatrix}$ 的前 6 项，并发现其周期规律（矩阵元素满足 $a_{ii}=a_{i,i+1}=a_{i+1,i}=1$，其余为 0）。
**涉及知识点** 三对角行列式、递推、周期性
**解答** 按第一行展开：$D_n=D_{n-1}-D_{n-2}$（第二项的符号来自展开：$1\cdot D_{n-1}-1\cdot\begin{vmatrix}1&1&0&\cdots\\0&1&1&\cdots\\\vdots\end{vmatrix}$，该子式按第一列展开为 $D_{n-2}$）。$D_1=1$，$D_2=\begin{vmatrix}1&1\\1&1\end{vmatrix}=0$。递推：$D_3=D_2-D_1=-1$，$D_4=D_3-D_2=-1$，$D_5=D_4-D_3=0$，$D_6=D_5-D_4=1$。序列 $1,0,-1,-1,0,1$ 以周期 6 循环（$D_n=D_{n-6}$，因 $D_{n+6}=D_{n+5}-D_{n+4}=\cdots=D_n$ 由递推的线性性质）。
**答案** $D_1,\dots,D_6=1,0,-1,-1,0,1$，周期为 6
**动画要点** - 三对角矩阵结构 - 递推序列的循环折线

### test-linalg-014 高等代数 · 逆矩阵×伴随矩阵
**题目** 求 $A=\begin{pmatrix}1&0&1\\0&2&0\\1&0&2\end{pmatrix}$ 的逆矩阵。
**涉及知识点** 伴随矩阵、代数余子式、三阶逆矩阵
**解答** $\det A=1\cdot(2\cdot 2-0\cdot 0)-0+1\cdot(0\cdot 0-2\cdot 1)=4-2=2$。代数余子式：$C_{11}=\begin{vmatrix}2&0\\0&2\end{vmatrix}=4$，$C_{12}=-\begin{vmatrix}0&0\\1&2\end{vmatrix}=0$，$C_{13}=\begin{vmatrix}0&2\\1&0\end{vmatrix}=-2$，$C_{21}=-\begin{vmatrix}0&1\\0&2\end{vmatrix}=0$，$C_{22}=\begin{vmatrix}1&1\\1&2\end{vmatrix}=1$，$C_{23}=-\begin{vmatrix}1&0\\1&0\end{vmatrix}=0$，$C_{31}=\begin{vmatrix}0&1\\2&0\end{vmatrix}=-2$，$C_{32}=-\begin{vmatrix}1&1\\0&0\end{vmatrix}=0$，$C_{33}=\begin{vmatrix}1&0\\0&2\end{vmatrix}=2$。$A^*=C^T=\begin{pmatrix}4&0&-2\\0&1&0\\-2&0&2\end{pmatrix}$。$A^{-1}=\dfrac{A^*}{2}=\begin{pmatrix}2&0&-1\\0&\frac{1}{2}&0\\-1&0&1\end{pmatrix}$。验证：$AA^{-1}=I$。
**答案** $\begin{pmatrix}2&0&-1\\0&\frac{1}{2}&0\\-1&0&1\end{pmatrix}$
**动画要点** - 9 个代数余子式的高亮计算 - 伴随矩阵转置

### test-linalg-015 高等代数 · 行列式×线性相关
**题目** 求 $\lambda$ 使向量组 $(1,\lambda,\lambda)$、$(\lambda,1,\lambda)$、$(\lambda,\lambda,1)$ 线性相关。
**涉及知识点** 行列式判据、特征值、参数讨论
**解答** 三向量为行的行列式 $D=\begin{vmatrix}1&\lambda&\lambda\\\lambda&1&\lambda\\\lambda&\lambda&1\end{vmatrix}$。该矩阵 $=(1-\lambda)I+\lambda J$（$J$ 全 1 矩阵），特征值为 $(1-\lambda)+3\lambda=1+2\lambda$（一重）与 $1-\lambda$（二重），故 $D=(1+2\lambda)(1-\lambda)^2$。线性相关 $\iff D=0\iff\lambda=1$ 或 $\lambda=-\dfrac{1}{2}$。
**答案** $\lambda=1$ 或 $\lambda=-\dfrac{1}{2}$
**动画要点** - 行列式随 $\lambda$ 变化的曲线 - 零点标注

### test-linalg-016 高等代数 · 子空间×维数公式
**题目** 设 $W_1=\{(x,y,z):x+y+z=0\}$，$W_2=\{(x,y,z):x=y=z\}$。求 $\dim(W_1\cap W_2)$ 与 $\dim(W_1+W_2)$，并判断是否为直和。
**涉及知识点** 子空间、维数公式、直和
**解答** $W_1$ 是平面（维数 2），$W_2$ 是直线（维数 1，方向 $(1,1,1)$）。$W_1\cap W_2$：$(t,t,t)\in W_1$ 需 $3t=0$，即 $t=0$，故 $W_1\cap W_2=\{0\}$，$\dim=0$。由维数公式 $\dim(W_1+W_2)=2+1-0=3$，且 $W_1\cap W_2=\{0\}$，故为直和，$W_1\oplus W_2=\mathbb R^3$。
**答案** $\dim(W_1\cap W_2)=0$；$\dim(W_1+W_2)=3$；直和
**动画要点** - 平面与直线只交于原点 - 直和分解示意

### test-linalg-017 高等代数 · 内积×矩阵
**题目** 验证 $\langle A,B\rangle=\operatorname{tr}(A^TB)$ 是 $2\times 2$ 实矩阵空间上的内积，并求 $A=\begin{pmatrix}1&2\\3&4\end{pmatrix}$ 的范数。
**涉及知识点** 内积公理、矩阵迹、范数
**解答** 设 $A=(a_{ij})$、$B=(b_{ij})$，$\operatorname{tr}(A^TB)=\displaystyle\sum_{i,j}a_{ij}b_{ij}$，即把矩阵按分量展开成 4 维向量的标准点积，故满足内积公理（对称、双线性、正定性：$\langle A,A\rangle=\sum a_{ij}^2\ge 0$ 且等号仅当 $A=0$）。$\|A\|=\sqrt{\langle A,A\rangle}=\sqrt{1+4+9+16}=\sqrt{30}$。
**答案** 证毕；$\|A\|=\sqrt{30}$
**动画要点** - 矩阵展开为 4 维向量 - 分量平方和

### test-linalg-018 高等代数 · 幂等矩阵×秩与迹
**题目** 设 $A=\begin{pmatrix}1&0\\0&0\end{pmatrix}$。验证 $A^2=A$，求 $A$ 的特征值，并说明幂等矩阵满足 $\operatorname{rank}A=\operatorname{tr}A$。
**涉及知识点** 幂等矩阵、特征值、秩与迹
**解答** $A^2=\begin{pmatrix}1&0\\0&0\end{pmatrix}\begin{pmatrix}1&0\\0&0\end{pmatrix}=\begin{pmatrix}1&0\\0&0\end{pmatrix}=A$。特征值：$|\lambda I-A|=\lambda(\lambda-1)$，特征值 $1,0$。$\operatorname{rank}A=1$，$\operatorname{tr}A=1$，相等。一般地，幂等矩阵 $A^2=A$ 的特征值满足 $\lambda^2=\lambda$，即 $\lambda\in\{0,1\}$，且 $A$ 可对角化（最小多项式整除 $\lambda(\lambda-1)$，无重根；本题给定矩阵的最小多项式恰为 $\lambda(\lambda-1)$），非零特征值个数 $=$ 秩，特征值之和 $=$ 迹，故 $\operatorname{rank}A=\operatorname{tr}A$。
**答案** 证毕；特征值 $1,0$；$\operatorname{rank}A=\operatorname{tr}A=1$
**动画要点** - 投影变换的几何 - 特征值 $\{0,1\}$ 标注

### test-linalg-019 高等代数 · 矩阵交换×待定系数
**题目** 求所有与 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 可交换的 $2\times 2$ 实矩阵 $X$。
**涉及知识点** 矩阵乘法、可交换性、待定系数
**解答** 设 $X=\begin{pmatrix}a&b\\c&d\end{pmatrix}$。$AX=\begin{pmatrix}a+c&b+d\\c&d\end{pmatrix}$，$XA=\begin{pmatrix}a&a+b\\c&c+d\end{pmatrix}$。可交换要求两矩阵相等：$a+c=a$（即 $c=0$），$b+d=a+b$（即 $a=d$），$d=c+d$（即 $c=0$，重复）。故 $X=\begin{pmatrix}a&b\\0&a\end{pmatrix}=aI+bN$（$N=\begin{pmatrix}0&1\\0&0\end{pmatrix}$），即与 $A$ 可交换的矩阵恰为 $A$ 的多项式 $aI+bN$。
**答案** $X=\begin{pmatrix}a&b\\0&a\end{pmatrix}$（$a,b\in\mathbb R$）
**动画要点** - 矩阵乘法比对 - 参数空间示意

### test-linalg-020 高等代数 · 多项式除法×余数定理
**题目** 求 $f(x)=x^4-4x^2+3$ 除以 $x^2-2x$ 的余式。
**涉及知识点** 多项式除法、余式定理、代入法
**解答** 设余式为 $ax+b$（除式二次，余式次数 $<2$）：$f(x)=(x^2-2x)q(x)+ax+b$。取 $x=0$：$f(0)=3=b$。取 $x=2$：$f(2)=16-16+3=3=2a+b$，故 $2a+3=3$，$a=0$。余式为 $3$。验证（长除法）：$x^4-4x^2+3=(x^2-2x)(x^2+2x)+3$（因 $(x^2-2x)(x^2+2x)=x^4-4x^2$）。
**答案** $3$
**动画要点** - 长除法竖式 - 代入 $x=0,2$ 的快速路径

### test-linalg-021 高等代数 · 正交矩阵×反射
**题目** 设 $A=\begin{pmatrix}\cos\theta&\sin\theta\\\sin\theta&-\cos\theta\end{pmatrix}$。证明 $A$ 是正交矩阵，求其特征值，并说明其几何意义。
**涉及知识点** 正交矩阵、反射、特征值
**解答** $A^TA=\begin{pmatrix}\cos\theta&\sin\theta\\\sin\theta&-\cos\theta\end{pmatrix}\begin{pmatrix}\cos\theta&\sin\theta\\\sin\theta&-\cos\theta\end{pmatrix}=\begin{pmatrix}\cos^2\theta+\sin^2\theta&\cos\theta\sin\theta-\sin\theta\cos\theta\\\sin\theta\cos\theta-\cos\theta\sin\theta&\sin^2\theta+\cos^2\theta\end{pmatrix}=I$，故 $A$ 正交，且 $\det A=-\cos^2\theta-\sin^2\theta=-1$。特征方程 $\lambda^2-1=0$（迹为 0），特征值 $\pm 1$。特征值 $1$ 的特征方向为 $\left(\cos\dfrac{\theta}{2},\sin\dfrac{\theta}{2}\right)$（关于此方向的直线反射），$-1$ 的特征方向与之垂直。几何上 $A$ 是关于过原点、方向为 $\left(\cos\dfrac{\theta}{2},\sin\dfrac{\theta}{2}\right)$ 的直线的镜面反射；该参数化覆盖所有轴方向，包括 $\theta=(2k+1)\pi$ 时的竖直轴 $x=0$（此时 $\tan\dfrac{\theta}{2}$ 不存在，不能用斜截式表示）。
**答案** 证毕；特征值 $\pm 1$；关于过原点、方向 $\left(\cos\dfrac{\theta}{2},\sin\dfrac{\theta}{2}\right)$ 的直线的反射（$\theta=(2k+1)\pi$ 时为竖直轴 $x=0$）
**动画要点** - 关于斜直线的反射 - 两个特征方向（不动/反向）

### test-linalg-022 高等代数 · Cholesky 分解×正定矩阵
**题目** 求正定矩阵 $A=\begin{pmatrix}4&2\\2&3\end{pmatrix}$ 的 Cholesky 分解 $A=LL^T$（$L$ 为下三角）。
**涉及知识点** Cholesky 分解、正定矩阵、三角矩阵
**解答** 设 $L=\begin{pmatrix}l_{11}&0\\l_{21}&l_{22}\end{pmatrix}$。$LL^T=\begin{pmatrix}l_{11}^2&l_{11}l_{21}\\l_{11}l_{21}&l_{21}^2+l_{22}^2\end{pmatrix}=\begin{pmatrix}4&2\\2&3\end{pmatrix}$。解得 $l_{11}=2$（取正），$l_{21}=\dfrac{2}{2}=1$，$l_{22}^2=3-1=2$，$l_{22}=\sqrt2$。故 $L=\begin{pmatrix}2&0\\1&\sqrt2\end{pmatrix}$。验证：$LL^T=\begin{pmatrix}4&2\\2&3\end{pmatrix}$。
**答案** $L=\begin{pmatrix}2&0\\1&\sqrt2\end{pmatrix}$
**动画要点** - 下三角矩阵的逐列计算 - 平方和分解示意

### test-linalg-023 高等代数 · 特征值×微分方程组
**题目** 用矩阵方法解微分方程组 $\begin{cases}x'=3x+y\\y'=x+3y\end{cases}$ 的通解。
**涉及知识点** 特征值分解、线性微分方程组、矩阵指数
**解答** 系数矩阵 $A=\begin{pmatrix}3&1\\1&3\end{pmatrix}$。特征方程 $(\lambda-3)^2-1=0$，$\lambda=4,2$，特征向量 $(1,1)^T$、$(1,-1)^T$。通解 $\begin{pmatrix}x\\y\end{pmatrix}=c_1e^{4t}\begin{pmatrix}1\\1\end{pmatrix}+c_2e^{2t}\begin{pmatrix}1\\-1\end{pmatrix}$，即 $x=c_1e^{4t}+c_2e^{2t}$，$y=c_1e^{4t}-c_2e^{2t}$。验证：$x'=4c_1e^{4t}+2c_2e^{2t}=3x+y$，$y'=4c_1e^{4t}-2c_2e^{2t}=x+3y$。
**答案** $x=c_1e^{4t}+c_2e^{2t}$；$y=c_1e^{4t}-c_2e^{2t}$
**动画要点** - 相图与特征方向 - 解的轨道

### test-linalg-024 高等代数 · 行列式×共线条件
**题目** 求 $t$ 使三点 $(1,2)$、$(2,4)$、$(t,6)$ 共线。
**涉及知识点** 三点共线、行列式、斜率
**解答** 共线条件：$\begin{vmatrix}1&2&1\\2&4&1\\t&6&1\end{vmatrix}=0$。按第一行展开：$1\cdot(4\cdot 1-1\cdot 6)-2\cdot(2\cdot 1-1\cdot t)+1\cdot(2\cdot 6-4\cdot t)=1\cdot(-2)-2\cdot(2-t)+1\cdot(12-4t)=-2-4+2t+12-4t=6-2t=0$，故 $t=3$。（或用斜率：前两点连线 $y=2x$，$(t,6)$ 在直线上需 $6=2t$，$t=3$。）
**答案** $t=3$
**动画要点** - 三点与直线 - 行列式为零的几何意义

### test-linalg-025 高等代数 · 谱分解×对称矩阵
**题目** 求 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$ 的谱分解 $A=\lambda_1u_1u_1^T+\lambda_2u_2u_2^T$。
**涉及知识点** 谱分解、特征值、正交投影
**解答** 特征值 $\lambda_1=3$、$\lambda_2=-1$（test-linalg-008），单位特征向量 $u_1=\dfrac{1}{\sqrt2}(1,1)^T$、$u_2=\dfrac{1}{\sqrt2}(1,-1)^T$。$u_1u_1^T=\dfrac{1}{2}\begin{pmatrix}1&1\\1&1\end{pmatrix}$，$u_2u_2^T=\dfrac{1}{2}\begin{pmatrix}1&-1\\-1&1\end{pmatrix}$。谱分解 $A=3u_1u_1^T+(-1)u_2u_2^T=\dfrac{3}{2}\begin{pmatrix}1&1\\1&1\end{pmatrix}-\dfrac{1}{2}\begin{pmatrix}1&-1\\-1&1\end{pmatrix}=\begin{pmatrix}1&2\\2&1\end{pmatrix}$。
**答案** $A=3u_1u_1^T-u_2u_2^T$（$u_1=\dfrac{(1,1)^T}{\sqrt2}$，$u_2=\dfrac{(1,-1)^T}{\sqrt2}$）
**动画要点** - 两个投影的叠加 - 特征方向的分解

### test-linalg-026 高等代数 · 二次型×合同变换
**题目** 将二次型 $f=3x^2+4xy+6y^2$ 用配方法化为标准形，并写出相应的可逆线性替换。
**涉及知识点** 配方法、合同变换、二次型
**解答** $f=3\left(x^2+\dfrac{4}{3}xy\right)+6y^2=3\left(x+\dfrac{2}{3}y\right)^2-\dfrac{4}{3}y^2+6y^2=3\left(x+\dfrac{2}{3}y\right)^2+\dfrac{14}{3}y^2$。令 $u=x+\dfrac{2}{3}y$、$v=y$（可逆：$x=u-\dfrac{2}{3}v$、$y=v$），标准形为 $3u^2+\dfrac{14}{3}v^2$。矩阵形式：$A=\begin{pmatrix}3&2\\2&6\end{pmatrix}$，$C=\begin{pmatrix}1&-\frac{2}{3}\\0&1\end{pmatrix}$，验证 $C^TAC=\begin{pmatrix}3&0\\0&\frac{14}{3}\end{pmatrix}$（$AC=\begin{pmatrix}3&0\\2&\frac{14}{3}\end{pmatrix}$，$C^T(AC)=\begin{pmatrix}3&0\\0&\frac{14}{3}\end{pmatrix}$）。
**答案** 标准形 $3u^2+\dfrac{14}{3}v^2$；替换 $\begin{cases}u=x+\frac{2}{3}y\\v=y\end{cases}$
**动画要点** - 配方步骤的代数动画 - 椭圆主轴与坐标变换

### test-linalg-027 高等代数 · 若尔当形×微分方程组
**题目** 解微分方程组 $\begin{cases}x'=2x+y\\y'=2y\end{cases}$ 的通解。
**涉及知识点** 若尔当块、广义特征向量、线性微分方程
**解答** 系数矩阵 $A=\begin{pmatrix}2&1\\0&2\end{pmatrix}=J_2(2)$。先解 $y'=2y$：$y=c_2e^{2t}$。代入 $x'=2x+c_2e^{2t}$：$x=e^{2t}\left(c_1+c_2t\right)$（常数变易，或观察特解 $x_p=c_2te^{2t}$：$x_p'-2x_p=c_2e^{2t}(1+2t)-2c_2te^{2t}=c_2e^{2t}$ 恰为强迫项）。验证：$x'=2e^{2t}(c_1+c_2t)+c_2e^{2t}=2x+y$。
**答案** $x=e^{2t}(c_1+c_2t)$；$y=c_2e^{2t}$
**动画要点** - 相图的退化结点 - 广义特征方向

### test-linalg-028 高等代数 · 复特征值×旋转
**题目** 求 $A=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$ 的特征值，并说明它没有实特征向量的几何原因。
**涉及知识点** 复特征值、旋转、特征向量
**解答** $|\lambda I-A|=\begin{vmatrix}\lambda&1\\-1&\lambda\end{vmatrix}=\lambda^2+1=0$，特征值 $\lambda=\pm i$（一对共轭虚数）。几何上 $A$ 是旋转 $90^\circ$（逆时针），除零向量外任何实向量旋转后都不与原方向平行，故没有（一维的）实特征空间；只有把向量空间扩充到复数域，才有特征方向。
**答案** 特征值 $\pm i$；无实特征向量（旋转 $90^\circ$）
**动画要点** - 向量旋转 $90^\circ$ - 无不变方向的演示

### test-linalg-029 高等代数 · 最小多项式×若尔当形
**题目** 求 $A=\begin{pmatrix}1&1&0\\0&1&0\\0&0&1\end{pmatrix}$ 的最小多项式与若尔当标准形。
**涉及知识点** 最小多项式、若尔当块、秩序列
**解答** 特征多项式 $(\lambda-1)^3$。$A-I=\begin{pmatrix}0&1&0\\0&0&0\\0&0&0\end{pmatrix}=:N$，$N\ne 0$ 且 $N^2=0$，故最小多项式 $m(\lambda)=(\lambda-1)^2$。秩判块结构：$\operatorname{rank}(A-I)=1$，特征值 $1$ 的若尔当块个数 $=3-1=2$，最大块尺寸由 $m(\lambda)$ 的因子幂给出为 2，故标准形为 $\begin{pmatrix}1&1&0\\0&1&0\\0&0&1\end{pmatrix}=A$ 本身（即 $J_2(1)\oplus J_1(1)$）。
**答案** 最小多项式 $(\lambda-1)^2$；若尔当标准形 $\begin{pmatrix}1&1&0\\0&1&0\\0&0&1\end{pmatrix}$
**动画要点** - 两个若尔当块的分块高亮 - 幂零链长度

### test-linalg-030 高等代数 · 线性泛函×对偶
**题目** 求 $\mathbb R^3$ 上的线性泛函 $f$，使其满足 $f(1,1,1)=3$、$f(1,0,0)=1$、$f(0,1,0)=1$。
**涉及知识点** 线性泛函、对偶空间、待定系数
**解答** 设 $f(x,y,z)=ax+by+cz$。条件：$f(1,0,0)=a=1$；$f(0,1,0)=b=1$；$f(1,1,1)=a+b+c=3$，故 $c=3-1-1=1$。得 $f(x,y,z)=x+y+z$。
**答案** $f(x,y,z)=x+y+z$
**动画要点** - 等值面（平面族） - 基向量上的取值

### test-linalg-031 高等代数 · 行列式×线性相关
**题目** 求 $\lambda$ 使向量组 $(1,2,3)$、$(2,\lambda,1)$、$(3,1,2)$ 线性相关。
**涉及知识点** 三阶行列式、线性相关、参数
**解答** 行列式 $D=\begin{vmatrix}1&2&3\\2&\lambda&1\\3&1&2\end{vmatrix}=1\cdot(\lambda\cdot 2-1\cdot 1)-2\cdot(2\cdot 2-1\cdot 3)+3\cdot(2\cdot 1-\lambda\cdot 3)=(2\lambda-1)-2\cdot 1+3\cdot(2-3\lambda)=2\lambda-1-2+6-9\lambda=3-7\lambda$。线性相关 $\iff D=0\iff\lambda=\dfrac{3}{7}$。
**答案** $\lambda=\dfrac{3}{7}$
**动画要点** - 三向量随 $\lambda$ 共面的瞬间 - 行列式零点

### test-linalg-032 高等代数 · 秩不等式×证明
**题目** 证明 $\operatorname{rank}(A+B)\le\operatorname{rank}A+\operatorname{rank}B$，并举出等号成立的例子。
**涉及知识点** 秩不等式、子空间、列空间
**解答** 列空间 $\operatorname{col}(A+B)\subseteq\operatorname{col}(A)+\operatorname{col}(B)$（$A+B$ 的每列都是 $A$ 与 $B$ 对应列之和，落在两列空间的和中）。故 $\operatorname{rank}(A+B)=\dim\operatorname{col}(A+B)\le\dim(\operatorname{col}(A)+\operatorname{col}(B))\le\dim\operatorname{col}(A)+\dim\operatorname{col}(B)=\operatorname{rank}A+\operatorname{rank}B$。等号例子：$A=\begin{pmatrix}1&0\\0&0\end{pmatrix}$、$B=\begin{pmatrix}0&0\\0&1\end{pmatrix}$，$\operatorname{rank}A=\operatorname{rank}B=1$，$A+B=I$，$\operatorname{rank}(A+B)=2=1+1$。
**答案** 证毕；等号例 $A=\begin{pmatrix}1&0\\0&0\end{pmatrix}$、$B=\begin{pmatrix}0&0\\0&1\end{pmatrix}$
**动画要点** - 列空间包含关系 - 等号例的对照

### test-linalg-033 高等代数 · 幂等矩阵×特征值证明
**题目** 证明：若 $A^2=A$，则 $A$ 的特征值只能是 $0$ 或 $1$。
**涉及知识点** 幂等矩阵、特征值、证明
**解答** 设 $Av=\lambda v$（$v\ne 0$）。则 $A^2v=A(Av)=A(\lambda v)=\lambda Av=\lambda^2v$。由 $A^2=A$ 得 $\lambda^2v=\lambda v$，即 $(\lambda^2-\lambda)v=0$。因 $v\ne 0$，$\lambda^2-\lambda=0$，$\lambda\in\{0,1\}$。
**答案** 证毕
**动画要点** - 投影的"两次作用=一次" - 特征值 $\{0,1\}$

### test-linalg-034 高等代数 · 正交对角化×二次曲面分类
**题目** 判断二次曲面 $3x^2+2xy+3y^2+z^2=1$ 的类型。
**涉及知识点** 正交对角化、特征值、二次曲面分类
**解答** 二次项矩阵 $A=\begin{pmatrix}3&1&0\\1&3&0\\0&0&1\end{pmatrix}$。$2\times 2$ 块 $\begin{pmatrix}3&1\\1&3\end{pmatrix}$ 的特征方程 $(\lambda-3)^2-1=0$，特征值 $4,2$；第三个特征值为 $1$。全为正，故曲面为椭球面：$\dfrac{u^2}{1/4}+\dfrac{v^2}{1/2}+z^2=1$（主轴沿特征方向，半轴 $\dfrac{1}{2},\dfrac{1}{\sqrt2},1$）。
**答案** 椭球面（特征值 $4,2,1$ 全正）
**动画要点** - 椭球面与三个主轴 - 特征方向旋转到主轴

### test-linalg-035 高等代数 · 行列式×多项式
**题目** 把 $D(x)=\begin{vmatrix}1&x&x^2\\1&2&4\\1&3&9\end{vmatrix}$ 看成 $x$ 的多项式并因式分解。
**涉及知识点** 范德蒙德行列式、多项式、因式分解
**解答** 这是范德蒙德行列式（三个点的范德蒙德型），$D(x)=(2-x)(3-x)(3-2)=(2-x)(3-x)=x^2-5x+6=(x-2)(x-3)$。验证：$x=2$ 时第一、二行相同，$D=0$；$x=3$ 时第一、三行相同，$D=0$；$x=0$ 时 $D=\begin{vmatrix}1&0&0\\1&2&4\\1&3&9\end{vmatrix}=18-12=6$，与 $(0-2)(0-3)=6$ 一致。
**答案** $(x-2)(x-3)$
**动画要点** - 行列式随 $x$ 变化的曲线 - 两个零点

### test-linalg-036 高等代数 · 初等矩阵×行列式
**题目** 求三类初等矩阵的行列式：交换两行、某行乘以 $k$（$k\ne 0$）、某行加到另一行（三类变换均涉及两不同行）。
**涉及知识点** 初等矩阵、行列式性质
**解答** 交换两行的初等矩阵 $P_{ij}$：由单位矩阵交换两行得到，$\det P_{ij}=-1$（一次对换改变符号）。第 $i$ 行乘 $k$ 的初等矩阵 $D_i(k)$：对角线第 $i$ 元为 $k$，$\det D_i(k)=k$。第 $i$ 行加到第 $j$ 行的初等矩阵 $E_{ij}$：下（上）三角且对角线全 1，$\det E_{ij}=1$。相应地对任意方阵 $B$：$\det(P_{ij}B)=-\det B$，$\det(D_i(k)B)=k\det B$，$\det(E_{ij}B)=\det B$。
**答案** $-1$；$k$；$1$
**动画要点** - 三类行变换对行列式的影响 - 单位矩阵的变形

### test-linalg-037 高等代数 · 线性变换×矩阵表示
**题目** 求微分算子 $T(f)=f'$ 在多项式空间 $P_2$（次数 $\le 2$，基 $1,x,x^2$）下的矩阵。
**涉及知识点** 线性变换的矩阵、微分、基
**解答** 对基作用：$T(1)=0=0\cdot 1+0\cdot x+0\cdot x^2$；$T(x)=1=1\cdot 1+0\cdot x+0\cdot x^2$；$T(x^2)=2x=0\cdot 1+2\cdot x+0\cdot x^2$。坐标列为 $(0,0,0)^T$、$(1,0,0)^T$、$(0,2,0)^T$，故矩阵 $\begin{pmatrix}0&1&0\\0&0&2\\0&0&0\end{pmatrix}$。验证：对 $f=a+bx+cx^2$（坐标 $(a,b,c)^T$），$Tf=b+2cx$，坐标 $(b,2c,0)^T$，矩阵乘法 $\begin{pmatrix}0&1&0\\0&0&2\\0&0&0\end{pmatrix}\begin{pmatrix}a\\b\\c\end{pmatrix}=\begin{pmatrix}b\\2c\\0\end{pmatrix}$，一致。
**答案** $\begin{pmatrix}0&1&0\\0&0&2\\0&0&0\end{pmatrix}$
**动画要点** - 基向量被微分的映射 - 矩阵-坐标乘法验证

### test-linalg-038 高等代数 · 秩×可逆性
**题目** 证明：若 $A$ 可逆，则 $\operatorname{rank}(A^2)=\operatorname{rank}A$；并举出 $A$ 不可逆时该结论不成立的例子。
**涉及知识点** 秩、可逆性、反例
**解答** $A$ 可逆时 $A^2$ 也可逆（$\det(A^2)=(\det A)^2\ne 0$），两者秩都等于 $n$（满秩），故相等。不可逆的反例：$A=\begin{pmatrix}0&1\\0&0\end{pmatrix}$，$\operatorname{rank}A=1$，$A^2=0$，$\operatorname{rank}(A^2)=0\ne 1$。
**答案** 证毕；反例 $A=\begin{pmatrix}0&1\\0&0\end{pmatrix}$
**动画要点** - 幂零变换的逐步退化 - 秩的变化链

### test-linalg-039 高等代数 · 二次型×惯性指数
**题目** 求二次型 $f=3x^2-2y^2-z^2+4xy$ 的正负惯性指数，并判断等值曲面 $f=1$ 的类型。
**涉及知识点** 惯性指数、特征值、二次曲面分类
**解答** 矩阵 $A=\begin{pmatrix}3&2&0\\2&-2&0\\0&0&-1\end{pmatrix}$。$2\times 2$ 块 $\begin{pmatrix}3&2\\2&-2\end{pmatrix}$：迹 $1$、行列式 $-10$，特征方程 $\lambda^2-\lambda-10=0$，特征值 $\dfrac{1\pm\sqrt{41}}{2}$，即一正一负；第三个特征值 $-1$。故正惯性指数 $1$、负惯性指数 $2$（符号差 $-1$）。等值曲面 $f=1$ 为双叶双曲面（一个正方向、两个负方向）。
**答案** 正惯性指数 $1$、负惯性指数 $2$；$f=1$ 为双叶双曲面（$f=-1$ 为单叶双曲面，$f=0$ 为锥面）
**动画要点** - 双叶双曲面的三维图 - 惯性指数标注

### test-linalg-040 高等代数 · 图论×特征值
**题目** 求四顶点圈 $C_4$ 的邻接矩阵及其特征值。
**涉及知识点** 邻接矩阵、图的谱、对称矩阵
**解答** $C_4$ 的邻接矩阵 $A=\begin{pmatrix}0&1&0&1\\1&0&1&0\\0&1&0&1\\1&0&1&0\end{pmatrix}$。解方程 $Av=\lambda v$：由对称性，特征向量可取 $(1,1,1,1)^T$（$A(1,1,1,1)^T=(2,2,2,2)^T=2(1,1,1,1)^T$，特征值 $2$）、$(1,-1,1,-1)^T$（验证 $A(1,-1,1,-1)^T=(-2,2,-2,2)^T=-2(1,-1,1,-1)^T$，特征值 $-2$）、$(1,0,-1,0)^T$（$A(1,0,-1,0)^T=(0,0,0,0)^T$，特征值 $0$）、$(0,1,0,-1)^T$（同样为 $0$）。故特征值为 $2,0,0,-2$（图是二部图，谱关于 0 对称）。
**答案** 邻接矩阵 $A=\begin{pmatrix}0&1&0&1\\1&0&1&0\\0&1&0&1\\1&0&1&0\end{pmatrix}$；特征值 $2,0,0,-2$
**动画要点** - 圈图与邻接矩阵 - 四个特征向量的模式

# 五、跨学科综合（15 题）

### test-x-001 跨学科 · 概率论×级数
**题目** 设 $X$ 服从参数 $p=\dfrac{1}{2}$ 的几何分布（抛硬币直到正面）。求 $P(X$ 为偶数$)$ 的精确值。
**涉及知识点** 几何分布、几何级数、奇偶分类
**解答** $P(X=k)=\left(\dfrac{1}{2}\right)^k$。$P(X$ 为偶数$)=\displaystyle\sum_{k=1}^{\infty}P(X=2k)=\sum_{k=1}^{\infty}\left(\dfrac{1}{2}\right)^{2k}=\sum_{k=1}^{\infty}\left(\dfrac{1}{4}\right)^k=\dfrac{1/4}{1-1/4}=\dfrac{1}{3}$。
**答案** $\dfrac{1}{3}$
**动画要点** - 奇偶分支的概率条 - 几何级数求和示意

### test-x-002 跨学科 · 概率论×微积分
**题目** 设 $X\sim U(0,1)$，求 $Y=\sqrt{X}$ 的密度与 $E[Y]$。
**涉及知识点** 密度变换、均匀分布、定积分
**解答** $y=\sqrt{x}$ 严格递增，反函数 $x=y^2$（$0<y<1$），$\left|\dfrac{dx}{dy}\right|=2y$。$f_Y(y)=f_X(y^2)\cdot 2y=2y$（$0<y<1$）。$E[Y]=\displaystyle\int_0^1y\cdot 2y\,dy=\dfrac{2}{3}$。验证：$E[\sqrt{X}]=\displaystyle\int_0^1\sqrt{x}\,dx=\left[\dfrac{2}{3}x^{3/2}\right]_0^1=\dfrac{2}{3}$，一致。
**答案** $f_Y(y)=2y$（$0<y<1$）；$E[Y]=\dfrac{2}{3}$
**动画要点** - $y=\sqrt{x}$ 的映射 - 密度曲线 $2y$

### test-x-003 跨学科 · 线性代数×微积分
**题目** 设 $A$ 为常矩阵。证明 $\dfrac{d}{dt}e^{tA}=Ae^{tA}$。
**涉及知识点** 矩阵指数、级数逐项求导、矩阵运算
**解答** $e^{tA}=\displaystyle\sum_{k=0}^{\infty}\dfrac{t^kA^k}{k!}$（对任意 $t$ 收敛）。逐项求导：$\dfrac{d}{dt}e^{tA}=\displaystyle\sum_{k=1}^{\infty}\dfrac{kt^{k-1}A^k}{k!}=\sum_{k=1}^{\infty}\dfrac{t^{k-1}A^k}{(k-1)!}=A\sum_{m=0}^{\infty}\dfrac{t^mA^m}{m!}=Ae^{tA}$（$A$ 为常数矩阵，可提出求和号外）。故 $\dfrac{d}{dt}e^{tA}=Ae^{tA}$，即矩阵指数是矩阵微分方程 $X'=AX$、$X(0)=I$ 的解。
**答案** 证毕
**动画要点** - 级数逐项求导 - 与标量情形的类比

### test-x-004 跨学科 · 概率论×线性代数
**题目** 转移矩阵为 $P$ 的马尔可夫链，稳态分布 $\pi$ 满足 $\pi=\pi P$。说明稳态分布是 $P^T$ 的特征值 $1$ 对应的特征向量，并求 $P=\begin{pmatrix}0.5&0.5\\0.25&0.75\end{pmatrix}$ 的稳态分布。
**涉及知识点** 马尔可夫链、特征向量、随机矩阵
**解答** $\pi=\pi P$ 转置得 $P^T\pi^T=\pi^T$，即稳态分布（转置后）是 $P^T$ 的特征值 $1$ 的特征向量（随机矩阵行和为 1，恒有特征值 1）。对给定 $P$：解 $\pi_1=0.5\pi_1+0.25\pi_2$（即 $0.5\pi_1=0.25\pi_2$，$\pi_1=\dfrac{\pi_2}{2}$）与 $\pi_1+\pi_2=1$，得 $\pi=\left(\dfrac{1}{3},\dfrac{2}{3}\right)$。验证：$\left(\dfrac{1}{3},\dfrac{2}{3}\right)P=\left(\dfrac{1}{3},\dfrac{2}{3}\right)$。
**答案** 稳态分布 $\left(\dfrac{1}{3},\dfrac{2}{3}\right)$；$\pi^T$ 是 $P^T$ 特征值 $1$ 的特征向量
**动画要点** - 状态转移图 - 特征值 1 与稳态的对应

### test-x-005 跨学科 · 解析几何×微积分
**题目** 用长为 $l$ 的围栏围一个矩形区域（一边靠墙不需围栏），求最大面积。
**涉及知识点** 二次函数最值、几何建模、导数
**解答** 设垂直墙的边长为 $x$，则平行墙的边长为 $l-2x$（$0<x<\dfrac{l}{2}$）。面积 $A=x(l-2x)=lx-2x^2$。$A'=l-4x=0$，$x=\dfrac{l}{4}$；$A''=-4<0$，为最大值。$A_{\max}=\dfrac{l}{4}\cdot\left(l-\dfrac{l}{2}\right)=\dfrac{l^2}{8}$。
**答案** $\dfrac{l^2}{8}$（$x=\dfrac{l}{4}$ 时）
**动画要点** - 矩形随 $x$ 变形 - 面积抛物线与顶点

### test-x-006 跨学科 · 概率论×解析几何
**题目** Bertrand 悖论：在单位圆中"随机取一条弦"，求弦长大于 $\sqrt3$ 的概率，分别按三种取法计算（随机端点、随机半径中点、随机中点）。
**涉及知识点** 几何概型、概率空间定义、建模
**解答** 弦长 $>\sqrt3\iff$ 弦到圆心的距离 $<\dfrac{1}{2}$（半弦长 $\sqrt{1-d^2}>\dfrac{\sqrt3}{2}\iff d<\dfrac{1}{2}$）。（1）随机端点：两端点在圆周上均匀独立，等价于固定一端后另一端随机，另一端点对应的圆心角 $\theta\in[0,2\pi)$ 均匀。弦长为 $2\sin\dfrac{\theta}{2}$（$\theta\in[0,\pi]$ 时递增、$[\pi,2\pi]$ 时递减），故 $2\sin\dfrac{\theta}{2}>\sqrt3\iff\dfrac{\theta}{2}\in\left(\dfrac{\pi}{3},\dfrac{2\pi}{3}\right)\iff\theta\in\left(\dfrac{2\pi}{3},\dfrac{4\pi}{3}\right)$，有利角长 $\dfrac{4\pi}{3}-\dfrac{2\pi}{3}=\dfrac{2\pi}{3}$，概率 $=\dfrac{2\pi/3}{2\pi}=\dfrac{1}{3}$。（2）随机半径中点：在一条半径上均匀取中点再作垂直弦，弦到圆心距离 $<\dfrac{1}{2}$ 的概率 $=\dfrac{1}{2}$。（3）随机中点：中点在圆内均匀分布，$d<\dfrac{1}{2}$ 对应半径为 $\dfrac{1}{2}$ 的小圆，面积比 $=\dfrac{\pi/4}{\pi}=\dfrac{1}{4}$。三种取法给出三个不同答案，说明"随机"必须先明确概率空间。
**答案** $\dfrac{1}{3}$、$\dfrac{1}{2}$、$\dfrac{1}{4}$（取决于取法）
**动画要点** - 三种取弦方式并排演示 - 有利区域高亮

### test-x-007 跨学科 · 线性代数×解析几何
**题目** 用特征值方法判断二次曲线 $x^2+4xy+y^2=1$ 的类型，并说明主轴方向。
**涉及知识点** 二次曲线分类、特征值、主轴
**解答** 矩阵 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$。特征方程 $(\lambda-1)^2-4=0$，特征值 $\lambda_1=3$、$\lambda_2=-1$（一正一负），故曲线为双曲线。特征向量：$\lambda=3$ 对应 $(1,1)^T$（主轴），$\lambda=-1$ 对应 $(1,-1)^T$。正交变换 $u=\dfrac{x+y}{\sqrt2}$、$v=\dfrac{x-y}{\sqrt2}$ 后方程为 $3u^2-v^2=1$，即 $\dfrac{u^2}{1/3}-v^2=1$，是双曲线，实轴沿 $y=x$ 方向。
**答案** 双曲线；主轴沿 $y=x$ 与 $y=-x$ 方向，标准形 $3u^2-v^2=1$
**动画要点** - 双曲线与两主轴 - 旋转到标准位置

### test-x-008 跨学科 · 解析几何×微积分
**题目** 求由 $y=x^2$ 与 $y=\sqrt{x}$ 围成的区域的面积。
**涉及知识点** 定积分、曲线交点、面积
**解答** 交点：$x^2=\sqrt{x}$，即 $x^4=x$，$x(x^3-1)=0$，$x=0$ 或 $x=1$。在 $[0,1]$ 上 $\sqrt{x}\ge x^2$。面积 $S=\displaystyle\int_0^1(\sqrt{x}-x^2)dx=\left[\dfrac{2}{3}x^{3/2}-\dfrac{x^3}{3}\right]_0^1=\dfrac{2}{3}-\dfrac{1}{3}=\dfrac{1}{3}$。
**答案** $\dfrac{1}{3}$
**动画要点** - 两曲线围成的叶片形区域 - 微元扫掠

### test-x-009 跨学科 · 概率论×微积分
**题目** 设 $X\sim\operatorname{Exp}(1)$。证明 $E[X^n]=n!$。
**涉及知识点** 指数分布、Γ 函数、分部积分
**解答** 设 $n\in\{0,1,2,\dots\}$。$E[X^n]=\displaystyle\int_0^{\infty}x^ne^{-x}dx$。记 $I_n=\displaystyle\int_0^{\infty}x^ne^{-x}dx$。$I_0=\displaystyle\int_0^{\infty}e^{-x}dx=1$ 单独计算；$n\ge 1$ 时用分部积分（$u=x^n$、$dv=e^{-x}dx$）：$I_n=\left[-x^ne^{-x}\right]_0^{\infty}+n\displaystyle\int_0^{\infty}x^{n-1}e^{-x}dx=nI_{n-1}$（$n\ge 1$ 时边界项 $x^ne^{-x}\big|_0^\infty$ 为 0）。递推得 $I_n=n!$，即 $E[X^n]=n!$（恰为 Γ 函数 $\Gamma(n+1)$）。
**答案** 证毕；$E[X^n]=n!$
**动画要点** - 分部积分的递推链 - 矩的阶乘增长

### test-x-010 跨学科 · 线性代数×概率论
**题目** 设两随机变量的方差有限且严格为正（$\sigma_1,\sigma_2>0$）。证明协方差矩阵 $\begin{pmatrix}\sigma_1^2&\rho\sigma_1\sigma_2\\\rho\sigma_1\sigma_2&\sigma_2^2\end{pmatrix}$ 正定当且仅当 $|\rho|<1$。
**涉及知识点** 协方差矩阵、正定性、行列式
**解答** 顺序主子式：$\sigma_1^2>0$；行列式 $\sigma_1^2\sigma_2^2(1-\rho^2)$。矩阵正定 $\iff$ 两顺序主子式均为正 $\iff 1-\rho^2>0\iff|\rho|<1$。概率解释：相关系数 $|\rho|<1$ 恰是"两个随机变量不几乎必然线性相关"的充要条件，此时协方差矩阵非退化；若某个方差为 0，协方差矩阵必奇异，且相关系数未定义。
**答案** 证毕（在 $\sigma_1,\sigma_2>0$ 的前提下，正定 $\iff|\rho|<1$）
**动画要点** - 相关系数滑块与散布图 - 退化情形 $\rho=\pm 1$

### test-x-011 跨学科 · 解析几何×线性代数
**题目** 证明：平面上关于两条过原点直线的（线性）反射的复合是旋转。以关于 $x$ 轴和关于直线 $y=x$ 的两次反射为例，求复合变换矩阵并识别其几何意义。
**涉及知识点** 反射矩阵、矩阵乘法、旋转
**解答** 关于 $x$ 轴的反射 $R_1=\begin{pmatrix}1&0\\0&-1\end{pmatrix}$，关于 $y=x$ 的反射 $R_2=\begin{pmatrix}0&1\\1&0\end{pmatrix}$。复合（先 $R_1$ 后 $R_2$）$R_2R_1=\begin{pmatrix}0&1\\1&0\end{pmatrix}\begin{pmatrix}1&0\\0&-1\end{pmatrix}=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$，这是逆时针旋转 $90^\circ$ 的矩阵（$\det=1$）。一般地，两个线性反射矩阵（正交、$\det=-1$）之积是正交矩阵且 $\det=1$，即旋转。注意：对一般的平面镜面反射，两轴相交时复合为绕交点旋转 $2\varphi$（$\varphi$ 为两轴夹角），两轴平行时复合为平移——本题限定线性反射（轴过原点）才恒得旋转。
**答案** 复合矩阵 $\begin{pmatrix}0&-1\\1&0\end{pmatrix}$（逆时针旋转 $90^\circ$）
**动画要点** - 两次反射的连续动画 - 合成出旋转

### test-x-012 跨学科 · 线性代数×微积分
**题目** 用级数定义计算矩阵指数 $e^{A}$，其中 $A=\begin{pmatrix}0&\pi\\-\pi&0\end{pmatrix}$。
**涉及知识点** 矩阵指数、级数、旋转矩阵
**解答** 记 $J=\begin{pmatrix}0&1\\-1&0\end{pmatrix}$，则 $A=\pi J$，且 $J^2=\begin{pmatrix}-1&0\\0&-1\end{pmatrix}=-I$。故 $A^2=-\pi^2I$，$A^3=-\pi^3J$，$A^4=\pi^4I$，一般地 $A^{2k}=(-1)^k\pi^{2k}I$，$A^{2k+1}=(-1)^k\pi^{2k+1}J$。$e^{A}=\displaystyle\sum_{k=0}^{\infty}\left[\dfrac{(-1)^k\pi^{2k}}{(2k)!}I+\dfrac{(-1)^k\pi^{2k+1}}{(2k+1)!}J\right]=\cos\pi\cdot I+\sin\pi\cdot J=-I+0\cdot J=\begin{pmatrix}-1&0\\0&-1\end{pmatrix}$（$\cos\pi=-1$，$\sin\pi=0$）。即 $e^{A}=-I$，对应旋转 $\pi$ 角（欧拉公式的矩阵版 $e^{i\pi}=-1$）。
**答案** $e^{A}=\begin{pmatrix}-1&0\\0&-1\end{pmatrix}=-I$
**动画要点** - 旋转 $\pi$ 的动画 - 矩阵版欧拉公式

### test-x-013 跨学科 · 概率论×数论
**题目** 随机取一个正整数（在 $1$ 到 $N$ 中等可能，$N\to\infty$ 取极限），求它能被 2 或 3 整除的概率。
**涉及知识点** 容斥原理、整除性、极限
**解答** 在 $\{1,\dots,N\}$ 中，能被 2 整除的约有 $\dfrac{N}{2}$ 个、能被 3 整除的约 $\dfrac{N}{3}$ 个、能被 6 整除的约 $\dfrac{N}{6}$ 个。由容斥原理，能被 2 或 3 整除的个数约 $\dfrac{N}{2}+\dfrac{N}{3}-\dfrac{N}{6}=\dfrac{2N}{3}$。概率 $=\dfrac{2N/3}{N}=\dfrac{2}{3}$（令 $N\to\infty$，即自然密度）。
**答案** $\dfrac{2}{3}$
**动画要点** - 数轴上 2、3 的倍数标记 - 容斥的双色重叠

### test-x-014 跨学科 · 解析几何×微积分
**题目** 求悬链线 $y=a\cosh\dfrac{x}{a}$（$0\le x\le b$）的弧长，其中 $a,b>0$。
**涉及知识点** 双曲函数、弧长公式、导数
**解答** $y'=\sinh\dfrac{x}{a}$。弧长 $L=\displaystyle\int_0^b\sqrt{1+\sinh^2\dfrac{x}{a}}\,dx=\int_0^b\cosh\dfrac{x}{a}\,dx=\left[a\sinh\dfrac{x}{a}\right]_0^b=a\sinh\dfrac{b}{a}$（用到 $1+\sinh^2u=\cosh^2u$）。
**答案** $a\sinh\dfrac{b}{a}$
**动画要点** - 悬链线与其弧长 - $\cosh$ 与 $\sinh$ 的关系

### test-x-015 跨学科 · 概率论×线性代数×级数
**题目** 设马尔可夫链的转移矩阵 $P=\begin{pmatrix}0.5&0.5\\0.25&0.75\end{pmatrix}$。用对角化求 $P^n$，并求 $n\to\infty$ 时的极限矩阵。
**涉及知识点** 对角化、矩阵极限、稳态分布
**解答** 特征方程 $|\lambda I-P|=(\lambda-0.5)(\lambda-0.75)-0.125=\lambda^2-1.25\lambda+0.25=0$，判别式 $1.5625-1=0.5625=\left(\dfrac{3}{4}\right)^2$，特征值 $\lambda=\dfrac{1.25\pm 0.75}{2}$，即 $\lambda_1=1$、$\lambda_2=\dfrac{1}{4}$。$\lambda_1=1$ 的特征向量：解 $(P-I)v=0$，即 $\begin{pmatrix}-0.5&0.5\\0.25&-0.25\end{pmatrix}v=0$，得 $v_1=(1,1)^T$。$\lambda_2=\dfrac{1}{4}$ 的特征向量：解 $\left(P-\dfrac{1}{4}I\right)v=0$，即 $\begin{pmatrix}0.25&0.5\\0.25&0.5\end{pmatrix}v=0$，得 $v_2=(2,-1)^T$（验证 $Pv_2=(0.5,-0.25)=\dfrac{1}{4}v_2$）。取 $Q=\begin{pmatrix}1&2\\1&-1\end{pmatrix}$，$\det Q=-3$，$Q^{-1}=-\dfrac{1}{3}\begin{pmatrix}-1&-2\\-1&1\end{pmatrix}=\begin{pmatrix}\frac{1}{3}&\frac{2}{3}\\\frac{1}{3}&-\frac{1}{3}\end{pmatrix}$。则 $P=Q\begin{pmatrix}1&0\\0&\frac{1}{4}\end{pmatrix}Q^{-1}$，$P^n=Q\begin{pmatrix}1&0\\0&4^{-n}\end{pmatrix}Q^{-1}$。令 $n\to\infty$：$4^{-n}\to 0$，故 $P^n\to Q\begin{pmatrix}1&0\\0&0\end{pmatrix}Q^{-1}=\begin{pmatrix}1&2\\1&-1\end{pmatrix}\begin{pmatrix}1&0\\0&0\end{pmatrix}\begin{pmatrix}\frac{1}{3}&\frac{2}{3}\\\frac{1}{3}&-\frac{1}{3}\end{pmatrix}=\begin{pmatrix}1&0\\1&0\end{pmatrix}\begin{pmatrix}\frac{1}{3}&\frac{2}{3}\\\frac{1}{3}&-\frac{1}{3}\end{pmatrix}=\begin{pmatrix}\frac{1}{3}&\frac{2}{3}\\\frac{1}{3}&\frac{2}{3}\end{pmatrix}$。极限矩阵每行均为稳态分布 $\left(\dfrac{1}{3},\dfrac{2}{3}\right)$（与 $\pi=\pi P$ 直接解 $0.5\pi_1=0.25\pi_2$ 即 $\pi_2=2\pi_1$ 的结果一致）。
**答案** $P^n=\dfrac{1}{3}\begin{pmatrix}1+2\cdot4^{-n}&2-2\cdot4^{-n}\\1-4^{-n}&2+4^{-n}\end{pmatrix}$；$\lim_{n\to\infty}P^n=\begin{pmatrix}\frac{1}{3}&\frac{2}{3}\\\frac{1}{3}&\frac{2}{3}\end{pmatrix}$
**动画要点** - $P^n$ 随 $n$ 收敛的动画 - 稳态分布行重复结构
