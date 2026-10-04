# B5 近重复阈值校准报告 v2(pairwise 评估)

- 标注对:48(重复 11 对 / 不重复 37 对),不确定 2 对不参与
- 评估口径:每对以其自身 pairwise Jaccard 对阈值判定(修复 v1 的 query-vs-pool 自污染)
- 校准结论:**UNCALIBRATED —— 网格内无阈值同时满足 recall≥0.95 且 fpr≤0.01——对照集或方法需检查,当前阈值仍 UNCALIBRATED**

## 网格表(0.30~0.80,步长 0.05)

| 阈值 | TP | FP | FN | TN | precision | recall | fpr |
|---|---|---|---|---|---|---|---|
| 0.3 | 11 | 15 | 0 | 22 | 0.4231 | 1.0 | 0.4054 |
| 0.35 | 11 | 14 | 0 | 23 | 0.44 | 1.0 | 0.3784 |
| 0.4 | 11 | 14 | 0 | 23 | 0.44 | 1.0 | 0.3784 |
| 0.45 | 11 | 14 | 0 | 23 | 0.44 | 1.0 | 0.3784 |
| 0.5 | 9 | 3 | 2 | 34 | 0.75 | 0.8182 | 0.0811 |
| 0.55 | 3 | 2 | 8 | 35 | 0.6 | 0.2727 | 0.0541 |
| 0.6 | 2 | 0 | 9 | 37 | 1.0 | 0.1818 | 0.0 |
| 0.65 | 2 | 0 | 9 | 37 | 1.0 | 0.1818 | 0.0 |
| 0.7 | 1 | 0 | 10 | 37 | 1.0 | 0.0909 | 0.0 |
| 0.75 | 1 | 0 | 10 | 37 | 1.0 | 0.0909 | 0.0 |
| 0.8 | 0 | 0 | 11 | 37 | None | 0.0 | 0.0 |

## 交错区(0.40~0.65,升序,完整题文)

| Jaccard | 标注 | 题目A(id) | 题目B(id) |
|---|---|---|---|
| 0.4615 | 不重复 | 求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n^2}{2^n}$ 的和。 (eval-calc-022) | 判断级数 $\displaystyle\sum_{n=1}^{\infty}\frac{n!}{n^n}$ 的敛散性。 (test-calc-034) |
| 0.4615 | 不重复 | 判断级数 $\displaystyle\sum_{n=1}^{\infty}\frac{n!}{n^n}$ 的敛散性。 (test-calc-034) | 证明 $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^{n-1}}{n}=\ln 2$。 (test-calc-042) |
| 0.4643 | 不重复 | 用多种方法求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\cdot 2^n}$ 的和。 (eval-calc-011) | 求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n^2}{2^n}$ 的和。 (eval-calc-022) |
| 0.4643 | 不重复 | 用多种方法求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\cdot 2^n}$ 的和。 (eval-calc-011) | 判断级数 $\displaystyle\sum_{n=1}^{\infty}\frac{n!}{n^n}$ 的敛散性。 (test-calc-034) |
| 0.4737 | 重复 | 求极限 $\displaystyle\lim_{x\to 0}\frac{1-\cos x}{x^2}$。 (eval-calc-001) | 求极限 $\displaystyle\lim_{x\to 0^+} x^x$。 (eval-calc-002) |
| 0.4792 | 不重复 | 求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n}{2^n}$ 的和。 (eval-calc-021) | 证明级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^2}$ 收敛。 (eval-calc-023) |
| 0.48 | 不重复 | 求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n}{2^n}$ 的和。 (eval-calc-021) | 判断级数 $\displaystyle\sum_{n=1}^{\infty}\frac{n!}{n^n}$ 的敛散性。 (test-calc-034) |
| 0.4808 | 不重复 | 用矩阵方法解微分方程组 $\begin{cases}x'=3x+y\\y'=x+3y\end{cases}$ 的通解。 (test-linalg-023) | 解微分方程组 $\begin{cases}x'=2x+y\\y'=2y\end{cases}$ 的通解。 (test-linalg-027) |
| 0.4815 | 不重复 | 用多种方法求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\cdot 2^n}$ 的和。 (eval-calc-011) | 求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n}{2^n}$ 的和。 (eval-calc-021) |
| 0.4889 | 重复 | 求极限 $\displaystyle\lim_{x\to 0}\frac{1-\cos x}{x^2}$。 (eval-calc-001) | 求极限 $\displaystyle\lim_{x\to 0}\frac{\sin x-\tan x}{x^3}$。 (eval-calc-004) |
| 0.4898 | 不重复 | 求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n^2}{2^n}$ 的和。 (eval-calc-022) | 求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n(n+2)}$ 的和。 (test-calc-013) |
| 0.4898 | 不重复 | 证明级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^2}$ 收敛。 (eval-calc-023) | 证明 $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^{n-1}}{n}=\ln 2$。 (test-calc-042) |
| 0.4898 | 不重复 | 求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n(n+2)}$ 的和。 (test-calc-013) | 证明 $\displaystyle\sum_{n=1}^{\infty}\frac{(-1)^{n-1}}{n}=\ln 2$。 (test-calc-042) |
| 0.5 | 重复 | 求不定积分 $\displaystyle\int x^2e^x\,dx$。 (eval-calc-013) | 求不定积分 $\displaystyle\int x\arctan x\,dx$。 (eval-calc-018) |
| 0.5106 | 重复 | 求级数 $\displaystyle S=\sum_{n=1}^{\infty}\frac{n}{2^n}$ 的和。 (eval-calc-021) | 求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n(n+2)}$ 的和。 (test-calc-013) |
| 0.5246 | 重复 | 判断反常积分 $\displaystyle\int_1^{+\infty}\frac{dx}{x(1+x)}$ 的敛散性，若收敛求其值。 (test-calc-012) | 判断 $\displaystyle\int_1^{+\infty}\frac{\ln x}{x^2}\,dx$ 的敛散性，若收敛求其值。 (test-calc-029) |
| 0.5254 | 重复 | 求矩阵 $A=\begin{pmatrix}1&2\\2&1\end{pmatrix}$ 的特征值与特征向量，并将其对角化。 (eval-linalg-015) | 求矩阵 $A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$ 的特征值与特征向量，并判断其是否可对角化。 (eval-linalg-017) |
| 0.5435 | 重复 | 求极限 $\displaystyle\lim_{x\to 0}\frac{1-\cos x}{x^2}$。 (eval-calc-001) | 求 $\displaystyle\lim_{x\to 0}\frac{1-\cos x-\frac{x^2}{2}}{x^4}$。 (test-calc-040) |
| 0.5478 | 重复 | 求 $n$ 阶三对角行列式 $D_n=\begin{vmatrix}2&1&0&\cdots&0\\1&2&1&\cdots&0\\0&1&2&\cdots&0\\\vdots&&&\ddots&\vdots\\0&0&0&\cdots&2\end{vmatrix}$ 的值（矩阵元素满足 $a_{ii}=2$，$a_{i,i+1}=a_{i+1,i}=1$，其余为 0）。 (eval-linalg-003) | 求 $n$ 阶三对角行列式 $D_n=\begin{vmatrix}1&1&0&\cdots&0\\1&1&1&\cdots&0\\0&1&1&\cdots&0\\\vdots&&&\ddots&\vdots\\0&0&\cdots&1&1\end{vmatrix}$ 的前 6 项，并发现其周期规律（矩阵元素满足 $a_{ii}=a_{i,i+1}=a_{i+1,i}=1$，其余为 0）。 (test-linalg-013) |
| 0.549 | 不重复 | 用多种方法求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\cdot 2^n}$ 的和。 (eval-calc-011) | 证明级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^2}$ 收敛。 (eval-calc-023) |
| 0.5532 | 重复 | 证明级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^2}$ 收敛。 (eval-calc-023) | 判断级数 $\displaystyle\sum_{n=1}^{\infty}\frac{n!}{n^n}$ 的敛散性。 (test-calc-034) |
| 0.5532 | 不重复 | 求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n(n+2)}$ 的和。 (test-calc-013) | 判断级数 $\displaystyle\sum_{n=1}^{\infty}\frac{n!}{n^n}$ 的敛散性。 (test-calc-034) |
| 0.58 | 不重复 | 用多种方法求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n\cdot 2^n}$ 的和。 (eval-calc-011) | 求级数 $\displaystyle\sum_{n=1}^{\infty}\frac{1}{n(n+2)}$ 的和。 (test-calc-013) |