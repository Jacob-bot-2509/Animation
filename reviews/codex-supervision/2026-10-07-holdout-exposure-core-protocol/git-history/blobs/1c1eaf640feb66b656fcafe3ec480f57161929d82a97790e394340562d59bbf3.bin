# B5 近重复阈值校准报告 v3(本质考点规则)

- 判重依据:用户确认(2026-10-04)= 题目**本质考点**,粒度=模块+题型
- 考点签名:(category, 题型);题型由题文动词分类,结构化字段兜底
- 有效标注:48 对,其中重复 17 对、不重复 31 对;不确定 2 对排除。
- 目标:召回率≥19/20,误报率≤1/100。
- 结论:**考点网格选定阈值 1(考点签名完全一致),召回率=1,误报率=0**(TP 17,FP 0,FN 0,TN 31)
- 范围:仅评估当前标注样本;分层采样不构成总体性能保证。

## 考点网格(离散取值 0 / 1/3 / 1)

| 阈值 | TP | FP | FN | TN | 精确率 | 召回率 | 误报率 |
|---|---|---|---|---|---|---|---|
| 0 | 17 | 31 | 0 | 0 | 17/48 | 1 | 1 |
| 1/3 | 17 | 18 | 0 | 13 | 17/35 | 1 | 18/31 |
| 1 | 17 | 0 | 0 | 31 | 1 | 1 | 0 |

精确率=TP/(TP+FP),召回率=TP/(TP+FN),误报率=FP/(FP+TN)。分母为零时显示“未定义”。

## 全对证据(48 对;J5 为文字 5-gram Jaccard,仅对照)

| J5(文字) | 标注 | 题目A(考点) | 题目B(考点) |
|---|---|---|---|
| 16/21 | 重复 | 求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n}{2^n}$ 的和。 (eval-calc-021;考点:数学分析 级数求和) | 求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n^2}{2^n}$ 的和。 (eval-calc-022;考点:数学分析 级数求和) |
| 2/3 | 不重复 | 证明级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^2}$ 收敛。 (eval-calc-023;考点:数学分析 级数敛散) | 求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n(n+2)}$ 的和。 (test-calc-013;考点:数学分析 级数求和) |
| 29/50 | 重复 | 用多种方法求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\cdot 2^n}$ 的和。 (eval-calc-011;考点:数学分析 级数求和) | 求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n(n+2)}$ 的和。 (test-calc-013;考点:数学分析 级数求和) |
| 26/47 | 重复 | 证明级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^2}$ 收敛。 (eval-calc-023;考点:数学分析 级数敛散) | 判断级数 $\displaystyle\sum_{n=1}^{\infty}\frac{n!}{n^n}$ 的敛散性。 (test-calc-034;考点:数学分析 级数敛散) |
| 26/47 | 不重复 | 求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n(n+2)}$ 的和。 (test-calc-013;考点:数学分析 级数求和) | 判断级数 $\displaystyle\sum_{n=1}^{\infty}\frac{n!}{n^n}$ 的敛散性。 (test-calc-034;考点:数学分析 级数敛散) |
| 28/51 | 不重复 | 用多种方法求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\cdot 2^n}$ 的和。 (eval-calc-011;考点:数学分析 级数求和) | 证明级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^2}$ 收敛。 (eval-calc-023;考点:数学分析 级数敛散) |
| 86/157 | 重复 | 求 $n$ 阶三对角行列式 $D_n=\begin{vmatrix}2&1&0&\cdots&0\\1&2&1&\cdots&0\\0&1&2&\cdots&0\\\vdots&&&\ddots&\vdots\\0&0&0&\cdots&2\end{vmatrix}$ 的值（矩阵元素满足 $a_{ii}=2$，$a_{i,i+1}=a_{i+1,i}=1$，其余为 0）。 (eval-linalg-003;考点:高等代数 三对角行列式) | 求 $n$ 阶三对角行列式 $D_n=\begin{vmatrix}1&1&0&\cdots&0\\1&1&1&\cdots&0\\0&1&1&\cdots&0\\\vdots&&&\ddots&\vdots\\0&0&\cdots&1&1\end{vmatrix}$ 的前 6 项，并发现其周期规律（矩阵元素满足 $a_{ii}=a_{i,i+1}=a_{i+1,i}=1$，其余为 0）。 (test-linalg-013;考点:高等代数 三对角行列式) |
| 25/46 | 重复 | 求极限 $\displaystyle\lim_{x\to 0}\frac{1-\cos x}{x^2}$。 (eval-calc-001;考点:数学分析 极限计算) | 求 $\displaystyle\lim_{x\to 0}\frac{1-\cos x-\frac{x^2}{2}}{x^4}$。 (test-calc-040;考点:数学分析 极限计算) |
| 31/59 | 重复 | 求矩阵 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$ 的特征值与特征向量，并将其对角化。 (eval-linalg-015;考点:高等代数 特征值对角化) | 求矩阵 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 的特征值与特征向量，并判断其是否可对角化。 (eval-linalg-017;考点:高等代数 特征值对角化) |
| 32/61 | 重复 | 判断反常积分 $\displaystyle\int_1^{+\infty}\frac{dx}{x(1+x)}$ 的敛散性，若收敛求其值。 (test-calc-012;考点:数学分析 反常积分) | 判断 $\displaystyle\int_1^{+\infty}\frac{\ln x}{x^2}\,dx$ 的敛散性，若收敛求其值。 (test-calc-029;考点:数学分析 反常积分) |
| 24/47 | 重复 | 求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n}{2^n}$ 的和。 (eval-calc-021;考点:数学分析 级数求和) | 求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n(n+2)}$ 的和。 (test-calc-013;考点:数学分析 级数求和) |
| 1/2 | 重复 | 求不定积分 $\displaystyle\int x^2e^x\,dx$。 (eval-calc-013;考点:数学分析 不定积分) | 求不定积分 $\displaystyle\int x\arctan x\,dx$。 (eval-calc-018;考点:数学分析 不定积分) |
| 24/49 | 重复 | 求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n^2}{2^n}$ 的和。 (eval-calc-022;考点:数学分析 级数求和) | 求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n(n+2)}$ 的和。 (test-calc-013;考点:数学分析 级数求和) |
| 24/49 | 不重复 | 证明级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^2}$ 收敛。 (eval-calc-023;考点:数学分析 级数敛散) | 证明 $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^{n-1}}{n}=\ln 2$。 (test-calc-042;考点:数学分析 级数求和) |
| 24/49 | 重复 | 求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n(n+2)}$ 的和。 (test-calc-013;考点:数学分析 级数求和) | 证明 $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^{n-1}}{n}=\ln 2$。 (test-calc-042;考点:数学分析 级数求和) |
| 22/45 | 重复 | 求极限 $\displaystyle\lim_{x\to 0}\frac{1-\cos x}{x^2}$。 (eval-calc-001;考点:数学分析 极限计算) | 求极限 $\displaystyle\lim_{x\to 0}\frac{\sin x-\tan x}{x^3}$。 (eval-calc-004;考点:数学分析 极限计算) |
| 13/27 | 重复 | 用多种方法求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\cdot 2^n}$ 的和。 (eval-calc-011;考点:数学分析 级数求和) | 求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n}{2^n}$ 的和。 (eval-calc-021;考点:数学分析 级数求和) |
| 25/52 | 重复 | 用矩阵方法解微分方程组 $\begin{cases}x'=3x+y\\y'=x+3y\end{cases}$ 的通解。 (test-linalg-023;考点:高等代数 微分方程组) | 解微分方程组 $\begin{cases}x'=2x+y\\y'=2y\end{cases}$ 的通解。 (test-linalg-027;考点:高等代数 微分方程组) |
| 12/25 | 不重复 | 求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n}{2^n}$ 的和。 (eval-calc-021;考点:数学分析 级数求和) | 判断级数 $\displaystyle\sum_{n=1}^{\infty}\frac{n!}{n^n}$ 的敛散性。 (test-calc-034;考点:数学分析 级数敛散) |
| 23/48 | 不重复 | 求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n}{2^n}$ 的和。 (eval-calc-021;考点:数学分析 级数求和) | 证明级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^2}$ 收敛。 (eval-calc-023;考点:数学分析 级数敛散) |
| 9/19 | 重复 | 求极限 $\displaystyle\lim_{x\to 0}\frac{1-\cos x}{x^2}$。 (eval-calc-001;考点:数学分析 极限计算) | 求极限 $\displaystyle\lim_{x\to 0^+} x^x$。 (eval-calc-002;考点:数学分析 极限计算) |
| 13/28 | 重复 | 用多种方法求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\cdot 2^n}$ 的和。 (eval-calc-011;考点:数学分析 级数求和) | 求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n^2}{2^n}$ 的和。 (eval-calc-022;考点:数学分析 级数求和) |
| 13/28 | 不重复 | 用多种方法求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\cdot 2^n}$ 的和。 (eval-calc-011;考点:数学分析 级数求和) | 判断级数 $\displaystyle\sum_{n=1}^{\infty}\frac{n!}{n^n}$ 的敛散性。 (test-calc-034;考点:数学分析 级数敛散) |
| 6/13 | 不重复 | 求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n^2}{2^n}$ 的和。 (eval-calc-022;考点:数学分析 级数求和) | 判断级数 $\displaystyle\sum_{n=1}^{\infty}\frac{n!}{n^n}$ 的敛散性。 (test-calc-034;考点:数学分析 级数敛散) |
| 6/13 | 不重复 | 判断级数 $\displaystyle\sum_{n=1}^{\infty}\frac{n!}{n^n}$ 的敛散性。 (test-calc-034;考点:数学分析 级数敛散) | 证明 $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^{n-1}}{n}=\ln 2$。 (test-calc-042;考点:数学分析 级数求和) |
| 13/76 | 不重复 | 讨论反常积分 $\displaystyle\int_1^{+\infty}\frac{dx}{x^p}$（$p>0$）的敛散性，并求其收敛时的值。 (eval-calc-020;考点:数学分析 反常积分) | 求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n}{2^n}$ 的和。 (eval-calc-021;考点:数学分析 级数求和) |
| 19/62 | 重复 | 求极限 $\displaystyle\lim_{x\to 0}\frac{e^x-e^{\sin x}}{x-\sin x}$。 (eval-calc-010;考点:数学分析 极限计算) | 设 $f$ 二阶可导且 $f(0)=f'(0)=0$，求 $\displaystyle\lim_{x\to 0}\frac{f(x)}{x^2}$。 (test-calc-007;考点:数学分析 极限计算) |
| 13/80 | 不重复 | 设 $A=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}$，求 $A^n$。 (eval-linalg-007;考点:高等代数 其他[矩阵]) | 用级数定义计算矩阵指数 $e^{A}$，其中 $A=\begin{pmatrix}0&\pi\\-\pi&0\end{pmatrix}$。 (test-x-012;考点:跨学科 级数求和) |
| 14/71 | 不重复 | 设 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$，求 $A^n$（$n$ 为正整数）。 (eval-linalg-006;考点:高等代数 其他[矩阵]) | 解矩阵方程 $AX=B$，其中 $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$，$B=\begin{pmatrix}3\\3\end{pmatrix}$。 (test-linalg-002;考点:高等代数 其他[矩阵方程×逆矩阵]) |
| 13/67 | 不重复 | 判断反常积分 $\displaystyle\int_1^{+\infty}\frac{dx}{x(1+x)}$ 的敛散性，若收敛求其值。 (test-calc-012;考点:数学分析 反常积分) | 求 $\displaystyle\lim_{n\to\infty}\frac{\sqrt[n]{n!}}{n}$。 (test-calc-024;考点:数学分析 极限计算) |
| 13/69 | 不重复 | 求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n}{2^n}$ 的和。 (eval-calc-021;考点:数学分析 级数求和) | 判断 $\displaystyle\int_1^{+\infty}\frac{\ln x}{x^2}\,dx$ 的敛散性，若收敛求其值。 (test-calc-029;考点:数学分析 反常积分) |
| 15/88 | 不重复 | 求 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$ 的谱分解 $A=\lambda_1u_1u_1^T+\lambda_2u_2u_2^T$。 (test-linalg-025;考点:高等代数 其他[谱分解×对称矩阵]) | 求 $A=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$ 的特征值，并说明它没有实特征向量的几何原因。 (test-linalg-028;考点:高等代数 特征值对角化) |
| 11/72 | 不重复 | 求不定积分 $\displaystyle\int\frac{dx}{(x^2+a^2)^2}$（$a>0$）。 (eval-calc-016;考点:数学分析 不定积分) | 判断 $\displaystyle\int_1^{+\infty}\frac{\ln x}{x^2}\,dx$ 的敛散性，若收敛求其值。 (test-calc-029;考点:数学分析 反常积分) |
| 0 | 不重复 | 求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n}{2^n}$ 的和。 (eval-calc-021;考点:数学分析 级数求和) | 求 $A=\begin{pmatrix}1&1&0\\0&1&0\\0&0&1\end{pmatrix}$ 的最小多项式与若尔当标准形。 (test-linalg-029;考点:高等代数 其他[最小多项式×若尔当形]) |
| 0 | 不重复 | 讨论含参数线性方程组 $\begin{cases}\lambda x+y+z=1\\x+\lambda y+z=\lambda\\x+y+\lambda z=\lambda^2\end{cases}$ 的解的情况。 (eval-linalg-011;考点:高等代数 其他[线性方程组]) | 证明：若 $A^2=A$，则 $A$ 的特征值只能是 $0$ 或 $1$。 (test-linalg-033;考点:高等代数 特征值对角化) |
| 1/10 | 不重复 | 求极限 $\displaystyle\lim_{n\to\infty}n^2\left(1-\cos\frac{1}{n}\right)$。 (test-calc-002;考点:数学分析 极限计算) | 求 $\displaystyle I=\int_0^1\!\!\int_y^1\frac{x}{1+x^2}\,dx\,dy$。 (test-calc-019;考点:数学分析 其他[重积分×交换次序]) |
| 0 | 不重复 | 求矩阵 $A=\begin{pmatrix}3&2\\4&3\end{pmatrix}$ 的逆矩阵。 (eval-linalg-005;考点:高等代数 其他[矩阵]) | 验证幂级数 $y=\displaystyle\sum_{n=0}^{\infty}\frac{x^n}{n!}$ 满足微分方程 $y'=y$ 及初值 $y(0)=1$。 (test-calc-014;考点:数学分析 微分方程组) |
| 0 | 不重复 | 求点 $P(1,2,-1)$ 到平面 $\pi:2x-y+2z=3$ 的距离。 (eval-geom-001;考点:解析几何 其他[直线与平面]) | 求矩阵 $A=\begin{pmatrix}2&1&0\\0&2&1\\0&0&2\end{pmatrix}$ 的最小多项式与若尔当标准形。 (eval-linalg-031;考点:高等代数 其他[λ-矩阵]) |
| 0 | 不重复 | 判断两条直线 $l_1:\dfrac{x-1}{2}=\dfrac{y+1}{1}=\dfrac{z-2}{-1}$ 与 $l_2:\dfrac{x+1}{1}=\dfrac{y-2}{2}=\dfrac{z}{1}$ 的位置关系。 (eval-geom-002;考点:解析几何 其他[直线与平面]) | 设 $A=\begin{pmatrix}\cos\theta&-\sin\theta\\\sin\theta&\cos\theta\end{pmatrix}$，求 $A^n$。 (eval-linalg-007;考点:高等代数 其他[矩阵]) |
| 0 | 不重复 | 求不定积分 $\displaystyle\int\dfrac{dx}{\sin x}$，并说明不同形式答案的等价性。 (eval-calc-014;考点:数学分析 不定积分) | 判断二次型 $f=x^2+2y^2+3z^2+2xy+2xz+4yz$ 是否正定。 (eval-linalg-021;考点:高等代数 其他[二次型]) |
| 0 | 不重复 | 指出方程 $4x^2-y^2+z^2=1$ 表示的二次曲面类型，并用截面法说明其形状。 (eval-geom-007;考点:解析几何 其他[二次曲面分类]) | 证明方程 $e^x=2x+1$ 恰有两个实根，并给出两个根所在的区间。 (test-calc-027;考点:数学分析 其他[零点定理×中值定理]) |
| 0 | 不重复 | 设 $z=x^y$（$x>0$），求 $z$ 在点 $(1,2)$ 处的两个偏导数。 (eval-calc-026;考点:数学分析 其他[多元函数微分]) | 掷一枚均匀骰子得 $X$ 分；若 $X=6$ 则可再掷一次并将点数累加。求总得分的期望。 (test-prob-025;考点:概率论 其他[期望×博弈模型]) |
| 0 | 不重复 | 说明曲面 $z=xy$ 的类型，并验证它是直纹面。 (eval-geom-010;考点:解析几何 其他[曲面与曲线]) | 设 $X\sim B\!\left(100,\dfrac{1}{2}\right)$。用切比雪夫不等式给出 $P(\|X-50\|\ge 10)$ 的上界，并与精确值比较。 (eval-prob-008;考点:概率论 其他[大数定律]) |
| 0 | 不重复 | 求参数 $a$ 使齐次线性方程组 $\begin{cases}ax+y+z=0\\x+ay+z=0\\x+y+az=0\end{cases}$ 有非零解，并求各情形下的解空间。 (eval-linalg-012;考点:高等代数 其他[线性方程组]) | 求点 $P(1,2,3)$ 到直线 $l:x=1+t,\ y=1+2t,\ z=1+3t$ 的距离与垂足坐标。 (test-geom-002;考点:解析几何 其他[点到直线×投影]) |
| 0 | 不重复 | 求椭球面 $\dfrac{x^2}{4}+\dfrac{y^2}{9}+z^2=1$ 与平面 $x=1$ 的交线方程，并说明其形状。 (eval-geom-009;考点:解析几何 其他[曲面与曲线]) | 求极限 $\displaystyle\lim_{n\to\infty}n^2\left(1-\cos\frac{1}{n}\right)$。 (test-calc-002;考点:数学分析 极限计算) |
| 0 | 不重复 | 求二重积分 $\displaystyle I=\iint_D(x^2+y^2)\,dA$，其中 $D=\{(x,y):x^2+y^2\le 2y\}$。 (eval-calc-028;考点:数学分析 其他[重积分]) | 求曲线 $y=x^2$ 在原点处的曲率，以及曲线 $y=\ln x$ 在 $(1,0)$ 处的曲率。 (test-calc-032;考点:数学分析 其他[曲率×导数]) |
| 1/91 | 不重复 | 证明级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^2}$ 收敛。 (eval-calc-023;考点:数学分析 级数敛散) | 设 $X\sim B\!\left(100,\dfrac{1}{2}\right)$。用切比雪夫不等式给出 $P(\|X-50\|\ge 10)$ 的上界，并与精确值比较。 (eval-prob-008;考点:概率论 其他[大数定律]) |
| 0 | 不重复 | 判断反常积分 $\displaystyle\int_1^{+\infty}\frac{dx}{x(1+x)}$ 的敛散性，若收敛求其值。 (test-calc-012;考点:数学分析 反常积分) | 求所有与 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 可交换的 $2\times 2$ 实矩阵 $X$。 (test-linalg-019;考点:高等代数 其他[矩阵交换×待定系数]) |

## 标注裁决(规则冲突对,用户逐项确认按规则改判)

| 对 | 原标注 | 改判 | 理由 |
|---|---|---|---|
| eval-calc-023 × test-calc-013 | 重复 | 不重复 | 敛散判别×级数求和,规则→不重复 |
| eval-calc-011 × test-calc-013 | 不重复 | 重复 | 级数求和×级数求和,规则→重复 |
| eval-calc-022 × test-calc-013 | 不重复 | 重复 | 级数求和×级数求和,规则→重复 |
| test-calc-013 × test-calc-042 | 不重复 | 重复 | 级数求和×级数求和(求值),规则→重复 |
| eval-calc-011 × eval-calc-021 | 不重复 | 重复 | 级数求和×级数求和,规则→重复 |
| eval-calc-011 × eval-calc-022 | 不重复 | 重复 | 级数求和×级数求和,规则→重复 |
| test-linalg-023 × test-linalg-027 | 不重复 | 重复 | 微分方程组×微分方程组,规则→重复 |
| eval-calc-010 × test-calc-007 | 不重复 | 重复 | 极限计算×极限计算,规则→重复 |

## 5-gram 对照网格(3/10 至 4/5,步长 1/20)

v2 已证文字 5-gram 区分不了标注(应 msg_376 独立复验一致),此处仅作对照,不参与校准结论。

| 阈值 | TP | FP | FN | TN | 精确率 | 召回率 | 误报率 |
|---|---|---|---|---|---|---|---|
| 3/10 | 17 | 9 | 0 | 22 | 17/26 | 1 | 9/31 |
| 7/20 | 16 | 9 | 1 | 22 | 16/25 | 16/17 | 9/31 |
| 2/5 | 16 | 9 | 1 | 22 | 16/25 | 16/17 | 9/31 |
| 9/20 | 16 | 9 | 1 | 22 | 16/25 | 16/17 | 9/31 |
| 1/2 | 9 | 3 | 8 | 28 | 3/4 | 9/17 | 3/31 |
| 11/20 | 3 | 2 | 14 | 29 | 3/5 | 3/17 | 2/31 |
| 3/5 | 1 | 1 | 16 | 30 | 1/2 | 1/17 | 1/31 |
| 13/20 | 1 | 1 | 16 | 30 | 1/2 | 1/17 | 1/31 |
| 7/10 | 1 | 0 | 16 | 31 | 1 | 1/17 | 0 |
| 3/4 | 1 | 0 | 16 | 31 | 1 | 1/17 | 0 |
| 4/5 | 0 | 0 | 17 | 31 | 未定义 | 0 | 0 |

## 不确定对(不参与校准,仅规则预测)

| 题目A(考点) | 题目B(考点) | 规则预测 |
|---|---|---|
| 求矩阵 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$ 的特征值与特征向量，并将其对角化。 (eval-linalg-015;考点:高等代数 特征值对角化) | 求所有与 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 可交换的 $2\times 2$ 实矩阵 $X$。 (test-linalg-019;考点:高等代数 其他[矩阵交换×待定系数]) | 不重复 |
| 设 $X\sim\operatorname{Poisson}(\lambda)$，求 $E[X^2]$，并由此求 $\operatorname{Var}(X)$。 (eval-prob-006;考点:概率论 其他[数字特征]) | 设 $X\sim\operatorname{Exp}(1)$。证明 $E[X^n]=n!$。 (test-x-009;考点:跨学科 其他[概率论×微积分]) | 不重复 |
