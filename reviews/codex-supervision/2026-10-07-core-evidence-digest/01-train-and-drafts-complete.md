# 当前训练 47 题与选中草稿 264 题

共 311 份题干、过程、答案。原文逐字段保留，历史错误或小数也是原始证据，不代表本轮认可。每项的场景、方法、条件补充字段见 `record-variants.jsonl`；父级上下文及原始字节见 `mathematical-source-bytes.zip`。数学资格审查必须连同这些上下文进行。本轮只装配证据，不新增核心判定或答案验收。

## 1. calc-derivative-001

内容 SHA256：`dec6095ba849a50559497acef17681f09c958dba06fd482a0b8c1eee2a9efe1b`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_calc.jsonl，第 1 行；源 SHA256 `cb2416f493f769d84e036f1f6d178fe2b1036c22bb83991d4a8fec1de76ab9e1`。

**题干**

求函数 $f(x)=x^2$ 在 $x=1$ 处的切线方程。

**过程**

$f'(x)=2x$，所以 $f'(1)=2$。又因为 $f(1)=1$，所以切线方程为 $y-1=2(x-1)$，化简得 $y=2x-1$。

**答案原文**

$y=2x-1$

## 2. calc-improper-002

内容 SHA256：`ef87b1cae997b8b477f6422cf6fc4fc624d2b3bae4d3ffff68696f850d801a40`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_calc.jsonl，第 2 行；源 SHA256 `cb2416f493f769d84e036f1f6d178fe2b1036c22bb83991d4a8fec1de76ab9e1`。

**题干**

判断反常积分 $\int_0^{+\infty} \frac{1}{1+x^2} dx$ 是否收敛，若收敛，求其值。

**过程**

该积分为无穷限反常积分。根据定义，先求变上限积分：$\int_0^b \frac{1}{1+x^2} dx = [\arctan x]_0^b = \arctan b - \arctan 0 = \arctan b$。再取极限：$\lim_{b \to +\infty} \arctan b = \frac{\pi}{2}$。因为极限存在且为有限常数，故该反常积分收敛。

**答案原文**

$\frac{\pi}{2}$

## 3. calc-param-improper-003

内容 SHA256：`fbd2d0871812a2032d3279d12588d529d1fca826942697656c1ab48504342a50`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_calc.jsonl，第 3 行；源 SHA256 `cb2416f493f769d84e036f1f6d178fe2b1036c22bb83991d4a8fec1de76ab9e1`。

**题干**

求含参反常积分$I(\alpha) = \int_{0}^{+\infty} e^{-\alpha x}dx$的值（设$\alpha>0$）。

**过程**

$I(\alpha) = \lim_{b \to +\infty} \int_{0}^{b} e^{-\alpha x} dx = \lim_{b \to  +\infty} \left[  -\frac{1}{\alpha} e^{-\alpha x} \right]_{0}^{b} = \lim_{b \to +\infty}  \frac{1}{\alpha} (1 - e^{-\alpha b }) = \frac{1}{\alpha}$。

**答案原文**

$\frac{1}{\alpha}$

## 4. calc-double-integral-004

内容 SHA256：`2a341d577d6739cf7e753db6588fceda658a85ef09c951772e768fb733272c94`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_calc.jsonl，第 4 行；源 SHA256 `cb2416f493f769d84e036f1f6d178fe2b1036c22bb83991d4a8fec1de76ab9e1`。

**题干**

利用二重积分的几何意义，说明 $\iint_D (1 - x^2 - y^2) dxdy$ 的值，其中 $D$ 是单位圆盘 $x^2 + y^2 \le 1$。

**过程**

这是一个二重积分，其几何意义是以区域 $D$ 为底，曲面 $z = 1 - x^2 - y^2$ 为顶的曲顶柱体的体积。区域 $D$ 是半径为 $1$ 的圆盘，面积为 $\pi$。在柱坐标系下，该体积可以通过极坐标计算：$\iint_D (1 - x^2 - y^2) dxdy = \int_{0}^{2\pi} d\theta \int_{0}^{1} (1 - r^2) r dr = 2\pi \left[ \frac{r^2}{2} - \frac{r^4}{4} \right]_{0}^{1} = 2\pi \times \frac{1}{4} = \frac{\pi}{2}$。

**答案原文**

$\frac{\pi}{2}$

## 5. calc-green-005

内容 SHA256：`bd2ff67645bddc2b82be5d2192756bac15bbed11bae2a1e15052484ff4534e6b`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_calc.jsonl，第 5 行；源 SHA256 `cb2416f493f769d84e036f1f6d178fe2b1036c22bb83991d4a8fec1de76ab9e1`。

**题干**

利用格林公式计算曲线积分 $\oint_L x dy - y dx$，其中 $L$ 是正向圆周 $x^2 + y^2 = a^2$。

**过程**

设 $P(x,y) = -y$，$Q(x,y) = x$。则 $\frac{\partial Q}{\partial x} = 1$，$\frac{\partial P}{\partial y} = -1$。由格林公式，原积分 $= \iint_D \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) dxdy = \iint_D (1 - (-1)) dxdy = 2 \iint_D dxdy$。因为 $\iint_D dxdy$ 等于圆盘的面积 $\pi a^2$，所以原积分 $= 2 \pi a^2$。

**答案原文**

$2\pi a^2$

## 6. calc-limit-006

内容 SHA256：`35d61a793d1102abaf166bbfd293c23e69cab57aa2699659ed89438bbfac7d6e`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_calc.jsonl，第 6 行；源 SHA256 `cb2416f493f769d84e036f1f6d178fe2b1036c22bb83991d4a8fec1de76ab9e1`。

**题干**

求极限 $\lim_{x \to 0} \frac{\sin x}{x}$ 的值。

**过程**

利用夹逼定理（Squeeze Theorem）进行几何证明。在单位圆中，设圆心角为 $x$（$0 < x < \frac{\pi}{2}$），比较 $\triangle OAB$、扇形 $OAB$ 和 $\triangle OAC$ 的面积。可以推导出不等式 $\sin x < x < \tan x$。同时除以 $\sin x$ 得到 $1 < \frac{x}{\sin x} < \frac{1}{\cos x}$。取倒数得 $\cos x < \frac{\sin x}{x} < 1$。由于 $\frac{\sin x}{x}$ 为偶函数，$x \to 0^-$ 时结论同样成立。当 $x \to 0$ 时，$\cos x \to 1$，由夹逼定理可得 $\lim_{x \to 0} \frac{\sin x}{x} = 1$。

**答案原文**

1

## 7. calc-area-007

内容 SHA256：`4224598f4b3eddfec0f52be5ca9a474c080167b4bd8f460bcdcd67f627f300a9`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_calc.jsonl，第 7 行；源 SHA256 `cb2416f493f769d84e036f1f6d178fe2b1036c22bb83991d4a8fec1de76ab9e1`。

**题干**

计算由抛物线 $y=x^2$ 与直线 $y=x+2$ 所围成的封闭图形的面积。

**过程**

联立方程 $y=x^2$ 与 $y=x+2$ 得交点 $(-1,1)$ 和 $(2,4)$。在区间 $[-1,2]$ 内，直线 $y=x+2$ 在抛物线 $y=x^2$ 的上方，故面积 $S = \int_{-1}^{2} [(x+2) - x^2] dx = [\frac{x^2}{2} + 2x - \frac{x^3}{3}]_{-1}^{2} = \frac{9}{2}$。

**答案原文**

$\frac{9}{2}$

## 8. calc-area-008

内容 SHA256：`525f4bf08ebfc671be099f5a8cfc2f03c05fa33ea474a8224f6b1791850c71db`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_calc.jsonl，第 8 行；源 SHA256 `cb2416f493f769d84e036f1f6d178fe2b1036c22bb83991d4a8fec1de76ab9e1`。

**题干**

计算由极坐标方程 $r = 2a\cos\theta$（$a>0$）所围成的图形的面积。

**过程**

该方程表示圆心在 $(a,0)$、半径为 $a$ 的圆。在极坐标中，$r = 2a\cos\theta \ge 0$，因此角度 $\theta$ 的取值范围为 $[-\frac{\pi}{2}, \frac{\pi}{2}]$。面积 $S = \frac{1}{2} \int_{-\pi/2}^{\pi/2} r^2 d\theta = \frac{1}{2} \int_{-\pi/2}^{\pi/2} (2a\cos\theta)^2 d\theta = \frac{1}{2} \int_{-\pi/2}^{\pi/2} 4a^2 \cos^2\theta d\theta = 2a^2 \int_{-\pi/2}^{\pi/2} \frac{1+\cos2\theta}{2} d\theta = a^2 [\theta + \frac{1}{2}\sin2\theta]_{-\pi/2}^{\pi/2} = a^2 [\frac{\pi}{2} - (-\frac{\pi}{2})] = \pi a^2$。

**答案原文**

$\pi a^2$

## 9. calc-area-009

内容 SHA256：`066a714c5b92da9e9a1b8d41ced49e89ecd6a18e2ce8b7907b26f13a9d2710b3`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_calc.jsonl，第 9 行；源 SHA256 `cb2416f493f769d84e036f1f6d178fe2b1036c22bb83991d4a8fec1de76ab9e1`。

**题干**

求摆线 $x = a(t - \sin t), y = a(1 - \cos t)$ 的一拱（$0 \le t \le 2\pi$）与 $x$ 轴所围成的面积。

**过程**

摆线的一拱与 $x$ 轴围成封闭图形。面积 $S = \int_{0}^{2\pi a} y dx$。将参数方程代入，得 $S = \int_{0}^{2\pi} a(1 - \cos t) \cdot d[a(t - \sin t)] = \int_{0}^{2\pi} a(1 - \cos t) \cdot a(1 - \cos t) dt = a^2 \int_{0}^{2\pi} (1 - 2\cos t + \cos^2 t) dt$。利用三角函数积分性质，其中 $\cos t$ 在周期内积分为0，故 $S = a^2 \int_{0}^{2\pi} (1 + \frac{1+\cos 2t}{2}) dt = a^2 \cdot 3\pi = 3\pi a^2$。

**答案原文**

$3\pi a^2$

## 10. calc-area-010

内容 SHA256：`4117293d1867e058f14f9b37412f7f21779117ff81b5fceda5f7fa097ebc28b5`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_calc.jsonl，第 10 行；源 SHA256 `cb2416f493f769d84e036f1f6d178fe2b1036c22bb83991d4a8fec1de76ab9e1`。

**题干**

计算由曲线 $y=\ln x$、直线 $y=-x+e+1$ 以及 $x$ 轴围成的封闭图形的面积。

**过程**

联立 $y=\ln x$ 与 $y=-x+e+1$ 得交点为 $(e, 1)$。该封闭图形以 $x$ 轴为下边界，由两部分组成：在 $[1, e]$ 上，上边界为曲线 $y=\ln x$；在 $[e, e+1]$ 上，上边界为直线 $y=-x+e+1$。面积 $S = \int_1^e \ln x dx + \int_e^{e+1} (-x+e+1) dx$。第一项：$\int_1^e \ln x dx = [x\ln x - x]_1^e = (e - e) - (0 - 1) = 1$。第二项：$\int_e^{e+1} (-x+e+1) dx = [-\frac{1}{2}x^2 + (e+1)x]_e^{e+1} = \frac{1}{2}$。总面积 $S = 1 + \frac{1}{2} = \frac{3}{2}$。

**答案原文**

$\frac{3}{2}$

## 11. calc-area-011

内容 SHA256：`c935181829e09d4c0064e45dd5120681ceaf1943f97a0b5ca0a38023e1d394f3`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_calc.jsonl，第 11 行；源 SHA256 `cb2416f493f769d84e036f1f6d178fe2b1036c22bb83991d4a8fec1de76ab9e1`。

**题干**

计算由曲线 $y = |x^2 - 1|$ 与直线 $y = 1$ 所围成的封闭图形的面积。

**过程**

曲线 $y = |x^2 - 1|$ 与直线 $y = 1$ 的交点为 $x = 0$ 和 $x = \pm\sqrt{2}$。因为图形关于y轴对称，可以计算右半部分 $[0, \sqrt{2}]$ 的面积再乘以2。当 $0 \le x \le 1$ 时，$y = 1 - x^2$，当 $1 \le x \le \sqrt{2}$ 时，$y = x^2 - 1$。面积 $S = 2 \left( \int_0^1 (1 - (1-x^2)) dx + \int_1^{\sqrt{2}} (1 - (x^2-1)) dx \right) = 2 \left( \int_0^1 x^2 dx + \int_1^{\sqrt{2}} (2 - x^2) dx \right) = 2 \left( \frac{1}{3} + (2x - \frac{x^3}{3})|_1^{\sqrt{2}} \right) = 2 \left( \frac{1}{3} + (2\sqrt{2} - \frac{2\sqrt{2}}{3}) - (2 - \frac{1}{3}) \right) = 2 \left( \frac{1}{3} + \frac{4\sqrt{2}}{3} - \frac{5}{3} \right) = \frac{8(\sqrt{2}-1)}{3}$。

**答案原文**

$\frac{8(\sqrt{2}-1)}{3}$

## 12. calc-vol-012

内容 SHA256：`dea0e26452eb4d18f39391bfe2f17cd7ec57bf8e6b36ef8425f2c3fa120e3f3f`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_calc.jsonl，第 12 行；源 SHA256 `cb2416f493f769d84e036f1f6d178fe2b1036c22bb83991d4a8fec1de76ab9e1`。

**题干**

求曲线 $y = \arcsin x$（$0 \le x \le 1$）与x轴、直线 $x=1$ 围成的图形绕x轴旋转一周所得旋转体的体积。

**过程**

使用圆盘法，体积 $V = \pi \int_0^1 (\arcsin x)^2 dx$。用分部积分法计算不定积分：令 $u=(\arcsin x)^2$，$dv=dx$，则 $du=\frac{2\arcsin x}{\sqrt{1-x^2}}dx$，$v=x$，于是 $\int (\arcsin x)^2 dx = x(\arcsin x)^2 - \int \frac{2x\arcsin x}{\sqrt{1-x^2}} dx = x(\arcsin x)^2 + 2\sqrt{1-x^2}\arcsin x - 2x$。代入上下限得 $V = \pi [1 \cdot (\frac{\pi}{2})^2 + 0 - 2] - \pi [0 + 0 - 0] = \pi(\frac{\pi^2}{4} - 2) = \frac{\pi^3}{4} - 2\pi$。

**答案原文**

$\frac{\pi^3}{4} - 2\pi$

## 13. calc-area-013

内容 SHA256：`a2eef58143fb4f962ad56682658bd56f8bdae6861116a3e3a540da4786e33d3f`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_calc.jsonl，第 13 行；源 SHA256 `cb2416f493f769d84e036f1f6d178fe2b1036c22bb83991d4a8fec1de76ab9e1`。

**题干**

计算由曲线 $y = x e^{-x}$、直线 $x = 1$ 以及x轴围成的封闭图形的面积。

**过程**

面积 $S = \int_0^1 x e^{-x} dx$。使用分部积分法，令 $u = x$，$dv = e^{-x} dx$，则 $du = dx$，$v = -e^{-x}$。$S = [-x e^{-x}]_0^1 - \int_0^1 (-e^{-x}) dx = -1 \cdot e^{-1} - 0 + [-e^{-x}]_0^1 = -e^{-1} - (e^{-1} - 1) = 1 - \frac{2}{e}$。

**答案原文**

$1 - \frac{2}{e}$

## 14. calc-series-015

内容 SHA256：`2e4ec22f1ef339c22cef7d2dc3667d652f56c8340db90d54aba5e89658a33449`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_calc.jsonl，第 14 行；源 SHA256 `cb2416f493f769d84e036f1f6d178fe2b1036c22bb83991d4a8fec1de76ab9e1`。

**题干**

讨论级数 $\sum_{n=1}^{\infty} \frac{(-1)^n}{\sqrt{n}}$ 的敛散性，并指出是绝对收敛还是条件收敛。

**过程**

该级数为交错级数，满足 $u_n = \frac{1}{\sqrt{n}}$ 单调递减且 $\lim_{n \to \infty} u_n = 0$，由莱布尼茨判别法知级数本身收敛。考察绝对值级数 $\sum_{n=1}^{\infty} \frac{1}{\sqrt{n}}$，这是一个 $p = 0.5 \le 1$ 的 p 级数，发散。因此，该级数为条件收敛。

**答案原文**

条件收敛

## 15. calc-series-017

内容 SHA256：`7e60fa1339ca7d1c1635ed502c2a8ce95c8479924ea668e30e968ee6f0f8292b`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_calc.jsonl，第 15 行；源 SHA256 `cb2416f493f769d84e036f1f6d178fe2b1036c22bb83991d4a8fec1de76ab9e1`。

**题干**

讨论函数项级数 $\sum_{n=1}^{\infty} \frac{x^n}{n^2}$ 在区间 $[-1, 1]$ 上是否一致收敛。

**过程**

对任意 $x \in [-1, 1]$，有 $|x| \le 1$，因此 $\left| \frac{x^n}{n^2} \right| \le \frac{1}{n^2}$。由于正项级数 $\sum_{n=1}^{\infty} \frac{1}{n^2}$ 收敛（p 级数，p=2>1），根据魏尔斯特拉斯判别法（M-判别法），原函数项级数在 $[-1, 1]$ 上一致收敛。

**答案原文**

一致收敛

## 16. calc-series-020

内容 SHA256：`6c6e80cd52ac19665697cd0a482ed0ef99c5c8528912cf0fef9c38f084fa03a0`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_calc.jsonl，第 16 行；源 SHA256 `cb2416f493f769d84e036f1f6d178fe2b1036c22bb83991d4a8fec1de76ab9e1`。

**题干**

将函数 $f(x) = x$（$-\pi \le x \le \pi$）展开为傅立叶级数。

**过程**

由于 $f(x)$ 是奇函数，傅立叶系数 $a_0 = 0$，$a_n = 0$。计算正弦项系数 $b_n = \frac{2}{\pi} \int_0^\pi x \sin(nx) dx = \frac{2(-1)^{n+1}}{n}$。故傅立叶级数为 $f(x) \sim 2\sum_{n=1}^{\infty} \frac{(-1)^{n+1}}{n} \sin(nx)$。

**答案原文**

$2\sum_{n=1}^{\infty} \frac{(-1)^{n+1}}{n} \sin(nx)$

## 17. geom-020

内容 SHA256：`152c37ca829483c9777e212980a53c1c00a9f101754a17a366fdce31128530da`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_geom.jsonl，第 1 行；源 SHA256 `8f163bbb5a5199af4dbcd56a15c6010ca085abe92b8034aeae26d57917b400b3`。

**题干**

求直线 $l: \frac{x-1}{2} = \frac{y+1}{-1} = \frac{z}{3}$ 与平面 $\pi: 2x - y + 3z = 5$ 的夹角。

**过程**

直线的方向向量为 $\vec{s} = (2, -1, 3)$，平面的法向量为 $\vec{n} = (2, -1, 3)$。计算两向量的点积 $\vec{s} \cdot \vec{n} = 2\times2 + (-1)\times(-1) + 3\times3 = 4 + 1 + 9 = 14$。两者的模长为 $|\vec{s}| = \sqrt{4+1+9} = \sqrt{14}$，$|\vec{n}| = \sqrt{14}$。设直线与平面的夹角为 $\theta$，则 $\sin\theta = \frac{|\vec{s} \cdot \vec{n}|}{|\vec{s}||\vec{n}|} = \frac{14}{\sqrt{14}\sqrt{14}} = \frac{14}{14} = 1$，故 $\theta = \frac{\pi}{2}$，即直线与平面垂直。

**答案原文**

$\frac{\pi}{2}$

## 18. geom-022

内容 SHA256：`87838be596d6fefccf52d51fa5947c3ecbcfee38a5d3aad14bf14489cb744ff5`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_geom.jsonl，第 2 行；源 SHA256 `8f163bbb5a5199af4dbcd56a15c6010ca085abe92b8034aeae26d57917b400b3`。

**题干**

求过三点 $A(1,0,0)$、$B(0,2,0)$、$C(0,0,3)$ 的平面方程。

**过程**

求向量 $\vec{AB} = (-1, 2, 0)$ 和 $\vec{AC} = (-1, 0, 3)$。平面的法向量 $\vec{n} = \vec{AB} \times \vec{AC} = \begin{vmatrix} \mathbf{i} & \mathbf{j} & \mathbf{k} \\ -1 & 2 & 0 \\ -1 & 0 & 3 \end{vmatrix} = (6, 3, 2)$。由点法式方程得 $6(x-1) + 3y + 2z = 0$，化简为 $6x + 3y + 2z - 6 = 0$。

**答案原文**

$6x + 3y + 2z - 6 = 0$

## 19. geom-024

内容 SHA256：`a6549ad9527543daf1f7a4e13903e54d2f2f456d44513c23aa16e420dcb7edd0`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_geom.jsonl，第 3 行；源 SHA256 `8f163bbb5a5199af4dbcd56a15c6010ca085abe92b8034aeae26d57917b400b3`。

**题干**

说明方程 $x^2 + y^2 = 4$ 在空间直角坐标系中表示什么曲面，并画出其图形。

**过程**

在平面直角坐标系中，方程 $x^2 + y^2 = 4$ 表示半径为 2 的圆。在空间直角坐标系中，由于方程缺少变量 $z$，说明对于任意 $z$ 值，$xOy$ 平面上的截面都是同样的圆。因此，该方程表示一个圆柱面，其母线平行于 $z$ 轴，准线为 $xOy$ 平面上的圆 $x^2 + y^2 = 4$。

**答案原文**

圆柱面，母线平行于 z 轴，准线为 xOy 平面上的圆

## 20. geom-026

内容 SHA256：`315bef8a9ce368b4001c6eb901433b7dca6f07bcf8c3c92cfa72969591b9bf6d`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_geom.jsonl，第 4 行；源 SHA256 `8f163bbb5a5199af4dbcd56a15c6010ca085abe92b8034aeae26d57917b400b3`。

**题干**

指出方程 $z = x^2 + 2y^2$ 表示的二次曲面类型，并分析其与平面 $y = 0$ 和 $y = 1$ 的交线。

**过程**

该方程为椭圆抛物面。当 $y = 0$ 时，交线为 $z = x^2$，是 $xOz$ 平面上的抛物线。当 $y = 1$ 时，交线为 $z = x^2 + 2$，依然是一条抛物线，只是顶点向上平移了 2 个单位。一般地，截面 $y=c$ 给出交线 $z=x^2+2c^2$：顶点在 $z$ 方向抬高 $2c^2$。因此，曲面可以看作截面抛物线随 $c$ 变化（顶点沿 $z$ 方向抬高 $2c^2$）叠加而成。

**答案原文**

椭圆抛物面；与平面 $y=0$ 的交线为 $z=x^2$，与平面 $y=1$ 的交线为 $z=x^2+2$

## 21. geom-028

内容 SHA256：`97997e313f5b4e985248e73040f96f69107d482cae360de83957070f0d930e57`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_geom.jsonl，第 5 行；源 SHA256 `8f163bbb5a5199af4dbcd56a15c6010ca085abe92b8034aeae26d57917b400b3`。

**题干**

判断椭圆抛物面 $z = x^2 + y^2$ 是否为直纹面，并说明理由。

**过程**

不是直纹面。假设它是直纹面，则曲面上存在直线。设直线过点 $(x_0, y_0, z_0)$，方向向量为 $(l, m, n)$，参数方程为 $(x_0+lt, y_0+mt, z_0+nt)$。代入曲面方程 $z=x^2+y^2$ 并整理得 $t^2(l^2+m^2)+t(2x_0l+2y_0m-n)+(x_0^2+y_0^2-z_0)=0$。若该方程对任意 $t$ 成立，则各次项系数全为零：由 $l^2+m^2=0$ 得 $l=m=0$；再由一次项系数 $2x_0l+2y_0m-n=0$ 得 $n=0$。于是方向向量为零向量，直线退化为一个点，矛盾。因此，椭圆抛物面上不存在直线，它不是直纹面。

**答案原文**

不是直纹面

## 22. geom-029

内容 SHA256：`5beb89b1d2fa9257b56bb5d0710ac5eb90c769fd63b21a8a0345be6f06a3b18d`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_geom.jsonl，第 6 行；源 SHA256 `8f163bbb5a5199af4dbcd56a15c6010ca085abe92b8034aeae26d57917b400b3`。

**题干**

已知空间中的等距变换由正交矩阵 $A = \begin{pmatrix} 0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1 \end{pmatrix}$ 和平移向量 $\vec{b} = (1, 2, 3)$ 定义。求点 $P(1, 0, 0)$ 变换后的坐标。

**过程**

根据等距变换公式 $P' = AP + \vec{b}$。先计算矩阵乘法：$AP = \begin{pmatrix} 0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1 \end{pmatrix} \begin{pmatrix} 1 \\ 0 \\ 0 \end{pmatrix} = \begin{pmatrix} 0 \\ 1 \\ 0 \end{pmatrix}$。然后加上平移向量：$P' = (0, 1, 0) + (1, 2, 3) = (1, 3, 3)$。该变换实际上是将点绕 $z$ 轴旋转 $90^\circ$，再平移。

**答案原文**

$(1, 3, 3)$

## 23. geom-030

内容 SHA256：`b7bee074aea1b62950cb65a7d6f75adb002b14ee8d57223c22fd1fc76f25c544`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_geom.jsonl，第 7 行；源 SHA256 `8f163bbb5a5199af4dbcd56a15c6010ca085abe92b8034aeae26d57917b400b3`。

**题干**

说明仿射变换 $x' = 2x, y' = y, z' = z$ 将球面 $x^2 + y^2 + z^2 = 1$ 变成了什么图形。

**过程**

将 $x = x'/2, y = y', z = z'$ 代入球面方程，得 $(x'/2)^2 + y'^2 + z'^2 = 1$，即 $\frac{x'^2}{4} + y'^2 + z'^2 = 1$。这是一个椭球面，它在 $x$ 轴方向被拉伸了 2 倍，而在 $y$ 和 $z$ 轴方向保持不变。

**答案原文**

椭球面 $\frac{x'^2}{4} + y'^2 + z'^2 = 1$

## 24. geom-031

内容 SHA256：`761ac8ee56e17ecbd1063308250c3268bb6aa71aa2349525ab2f035b8e997b77`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_geom.jsonl，第 8 行；源 SHA256 `8f163bbb5a5199af4dbcd56a15c6010ca085abe92b8034aeae26d57917b400b3`。

**题干**

求球面 $x^2+y^2+z^2=4a^2$ 与圆柱面 $x^2+y^2=2ax$ 的交线（维维安尼曲线）的参数方程（$a>0$）。

**过程**

令 $x=a(1+\cos t)$，$y=a\sin t$，则 $x^2+y^2 = a^2(1+\cos t)^2 + a^2\sin^2 t = 2a^2(1+\cos t) = 2a\cdot a(1+\cos t) = 2ax$，圆柱面方程自动满足。代入球面方程 $x^2+y^2+z^2=4a^2$ 得 $z^2 = 4a^2 - 2a^2(1+\cos t) = 2a^2(1-\cos t) = 4a^2\sin^2\frac{t}{2}$。取连续参数分支 $z = 2a\sin\frac{t}{2}$（另一分支 $z = -2a\sin\frac{t}{2}$ 由参数平移 $2\pi$ 覆盖，不另取）。于是交线的参数方程为 $x=a(1+\cos t)$，$y=a\sin t$，$z=2a\sin\frac{t}{2}$，其中 $0 \le t \le 4\pi$ 覆盖整条曲线（$0 \le t \le 2\pi$ 仅覆盖上半部分）。

**答案原文**

维维安尼曲线，参数方程为 $x=a(1+\cos t)$，$y=a\sin t$，$z=2a\sin\frac{t}{2}$，其中 $0 \le t \le 4\pi$

## 25. linalg-048

内容 SHA256：`9d85642ac8c608c5dd22aadc77c31f72c96800dbf8f180da4aa412811ea40b64`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_linalg.jsonl，第 1 行；源 SHA256 `c2e36b7f45ffb461f1d909e51410155ffc07ad2badd5cd198bdb61e03413b39f`。

**题干**

已知矩阵 $A=\begin{pmatrix}1&3\\0&1\end{pmatrix}$，求该矩阵对应的线性变换对二维平面的几何影响。

**过程**

对任意点 $(x,y)$，$T(x,y)=A\begin{pmatrix}x\\y\end{pmatrix}=\begin{pmatrix}x+3y\\y\end{pmatrix}$，位移为 $(3y,0)$。故 $x$ 轴逐点固定，$\vec e_1=(1,0)$ 不动，$\vec e_2=(0,1)$ 映为 $(3,1)$。对于任意 $c\in\mathbb R$，$T(\mathbb R\times\{c\})=\mathbb R\times\{c\}$：整条水平直线作为点集保持不变，其上每个带标记点的横坐标增加 $3c$。有限线段 $[0,1]\times\{c\}$ 则映为 $[3c,1+3c]\times\{c\}$。竖直线 $x=c$ 的像可写为 $(X,Y)=(c+3t,t)$，$t\in\mathbb R$，即 $X-3Y=c$，斜率为 $\frac13$。沿边界次序，单位正方形顶点 $(0,0),(1,0),(1,1),(0,1)$ 依次映为 $(0,0),(1,0),(4,1),(3,1)$，得到底长 $1$、高 $1$ 的平行四边形。$\det A=1\cdot1-3\cdot0=1$，故面积与定向均保持。这是一种水平剪切；移动距离为 $3|y|$，纵坐标不变。长度一般不保持，例如 $\|(0,1)\|=1$ 而 $\|T(0,1)\|=\sqrt{10}$。

**答案原文**

水平剪切 $T(x,y)=(x+3y,y)$；$x$ 轴逐点固定，水平直线作为点集不变、带标记点的位移为 $(3y,0)$；竖直线 $x=c$ 映为 $X-3Y=c$；面积和定向保持，$\det A=1$，长度一般不保持。

## 26. linalg-050

内容 SHA256：`22b11a0d204a892593635bba8f2d222d9ab6f80d3da92cd2e284a0f6649d1ac4`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_linalg.jsonl，第 2 行；源 SHA256 `c2e36b7f45ffb461f1d909e51410155ffc07ad2badd5cd198bdb61e03413b39f`。

**题干**

利用几何图形解释二阶行列式 $\begin{vmatrix} a & b \\ c & d \end{vmatrix} = ad - bc$ 的几何意义。

**过程**

二阶行列式 $ad - bc$ 的绝对值等于矩阵 $\begin{pmatrix} a & b \\ c & d \end{pmatrix}$ 对应的线性变换将单位正方形映射成的平行四边形的面积。若行列式为正，表示空间保持定向；若为负，表示空间发生了翻折（定向反转）；若为0，表示空间被压缩到一条直线上，面积消失。

**答案原文**

行列式绝对值等于变换后平行四边形的面积

## 27. linalg-051

内容 SHA256：`2b4a65cd47016ad6386e9927089c8dfb9ef3de6008c838fa20255ad0716fe80a`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_linalg.jsonl，第 3 行；源 SHA256 `c2e36b7f45ffb461f1d909e51410155ffc07ad2badd5cd198bdb61e03413b39f`。

**题干**

设多项式 $f(x)=x^3-6x^2+11x-6$，将其因式分解并说明其根在复平面上的分布。

**过程**

由有理根定理，可能的根为 $\pm1,\pm2,\pm3,\pm6$。代入得 $f(1)=0$，故 $(x-1)$ 是因式。多项式除法得 $f(x)=(x-1)(x^2-5x+6)=(x-1)(x-2)(x-3)$。三个根均为实根，在复平面上位于实轴上。

**答案原文**

$(x-1)(x-2)(x-3)$；三个根 $1,2,3$ 均为实根，在复平面上全部位于实轴上

## 28. linalg-053

内容 SHA256：`928a19e71a273237b103c3b3e7c66f4947ea55a5aeedd9808a8d5346d037cb7b`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_linalg.jsonl，第 4 行；源 SHA256 `c2e36b7f45ffb461f1d909e51410155ffc07ad2badd5cd198bdb61e03413b39f`。

**题干**

利用几何图形解释三阶行列式 $\begin{vmatrix} 1 & 2 & 0 \\ 0 & 1 & 3 \\ 2 & 1 & 1 \end{vmatrix}$ 的几何意义。

**过程**

计算行列式得 $1(1\cdot1-3\cdot1)-2(0\cdot1-3\cdot2)+0=1(-2)-2(-6)=-2+12=10$。该行列式的绝对值等于矩阵对应的线性变换将单位立方体映射成的平行六面体的体积。体积为 10。

**答案原文**

10，即该行列式的绝对值等于矩阵对应线性变换将单位立方体映射成的平行六面体的体积

## 29. linalg-054

内容 SHA256：`d4056b1a65a6e6806a6dfde1c09f9bf1a58db16cd26bcebac6a6c18a6719a541`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_linalg.jsonl，第 5 行；源 SHA256 `c2e36b7f45ffb461f1d909e51410155ffc07ad2badd5cd198bdb61e03413b39f`。

**题干**

利用 Cramer 法则求解线性方程组 $\begin{cases} 2x + y = 5 \\ x - y = 1 \end{cases}$，并说明行列式为零时的几何意义。

**过程**

系数行列式 $D=\begin{vmatrix} 2 & 1 \\ 1 & -1 \end{vmatrix}=-3\neq0$，方程组有唯一解。$D_x=\begin{vmatrix} 5 & 1 \\ 1 & -1 \end{vmatrix}=-6$，$D_y=\begin{vmatrix} 2 & 5 \\ 1 & 1 \end{vmatrix}=-3$，故 $x=2, y=1$。若 $D=0$，两直线平行或重合，对应无解或无穷多解。

**答案原文**

$x=2, y=1$；当系数行列式为零时，两直线平行或重合，对应无解或无穷多解

## 30. linalg-055

内容 SHA256：`995ab568881bee4456f807b2b4fb0508e1c60fe80abde478af52878b9133a3bc`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_linalg.jsonl，第 6 行；源 SHA256 `c2e36b7f45ffb461f1d909e51410155ffc07ad2badd5cd198bdb61e03413b39f`。

**题干**

讨论线性方程组 $\begin{cases} x + y + z = 1 \\ x - y + z = 1 \\ 2x + z = 2 \end{cases}$ 解的情况。

**过程**

系数矩阵的秩为 3，增广矩阵的秩也为 3，故方程组有唯一解。通过消元法：由第一式减第二式得 $2y=0 \Rightarrow y=0$。代入第一式和第三式得 $x+z=1$ 且 $2x+z=2$，相减得 $x=1, z=0$。即解为 $(1, 0, 0)$。

**答案原文**

唯一解，$(1, 0, 0)$

## 31. linalg-056

内容 SHA256：`b19c8e90ba0407656b0480f72b748faa314ba492f66a5d02e9591d75f0d28788`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_linalg.jsonl，第 7 行；源 SHA256 `c2e36b7f45ffb461f1d909e51410155ffc07ad2badd5cd198bdb61e03413b39f`。

**题干**

求齐次线性方程组 $\begin{cases} x_1 + 2x_2 + x_3 = 0 \\ 2x_1 + 4x_2 + 2x_3 = 0 \end{cases}$ 的基础解系。

**过程**

系数矩阵的秩为 1，未知量个数为 3，故基础解系包含 $3-1=2$ 个线性无关的解向量。取自由变量 $x_2, x_3$，得基础解系 $\xi_1=(-2,1,0)^T, \xi_2=(-1,0,1)^T$，解空间为二维平面。

**答案原文**

$\xi_1=(-2,1,0)^T, \xi_2=(-1,0,1)^T$

## 32. linalg-058

内容 SHA256：`59a8fc6d548e4a8a125f80163f888935822dda9f3e09bb096f0a0dbdf85541a7`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_linalg.jsonl，第 8 行；源 SHA256 `c2e36b7f45ffb461f1d909e51410155ffc07ad2badd5cd198bdb61e03413b39f`。

**题干**

说明初等矩阵 $E=\begin{pmatrix} 1 & 0 \\ 3 & 1 \end{pmatrix}$ 对应的线性变换的几何意义。

**过程**

该矩阵是将单位矩阵第二行加上第一行的 3 倍得到的初等矩阵。对应的线性变换是沿 $y$ 轴方向的剪切变换：平面上每一点的 $x$ 坐标不变，$y$ 坐标变为 $y+3x$。这是一个保持面积不变（行列式为 1）的剪切变换。

**答案原文**

$x$ 坐标不变，$y$ 坐标变为 $y+3x$，面积不变

## 33. linalg-062

内容 SHA256：`13f1b76ec974ac442cc71506481fe0d7598a87ef6dd99f6759714b15661e0f2b`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_linalg.jsonl，第 9 行；源 SHA256 `c2e36b7f45ffb461f1d909e51410155ffc07ad2badd5cd198bdb61e03413b39f`。

**题干**

在 $\mathbb{R}^3$ 中，已知子空间 $W_1=\{(x,y,0)\}$（xOy平面）和 $W_2=\{(0,y,z)\}$（yOz平面），求 $\dim(W_1+W_2)$ 和 $\dim(W_1\cap W_2)$。

**过程**

$W_1$ 是 xOy 平面，维数 2；$W_2$ 是 yOz 平面，维数 2。它们的交是 y 轴，维数 1。根据维数公式，$\dim(W_1+W_2)=\dim W_1+\dim W_2-\dim(W_1\cap W_2)=2+2-1=3$。

**答案原文**

$\dim(W_1+W_2)=3$，$\dim(W_1\cap W_2)=1$

## 34. linalg-063

内容 SHA256：`916e2b590b2f296a7f155db9dcc2003bd4aaf6fd29ee633a24df5ef476d0ecea`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_linalg.jsonl，第 10 行；源 SHA256 `c2e36b7f45ffb461f1d909e51410155ffc07ad2badd5cd198bdb61e03413b39f`。

**题干**

设线性变换 $T:\mathbb{R}^3\to\mathbb{R}^2$ 由 $T(x,y,z)=(x+y, y+z)$ 定义，求 $T$ 的核和值域的维数。

**过程**

核 $\ker T=\{(x,y,z): x+y=0, y+z=0\}=\{(-y,y,-y)\}$，维数为 1。由秩-零化度定理，$\dim(\operatorname{Im}T)=3-1=2$，值域为整个 $\mathbb{R}^2$。

**答案原文**

$\dim(\ker T)=1$，$\dim(\operatorname{Im}T)=2$

## 35. linalg-064

内容 SHA256：`db81e327b152b66d2ed1b2cd83a0bca5078bb307c5d07745464689d73ba4c684`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_linalg.jsonl，第 11 行；源 SHA256 `c2e36b7f45ffb461f1d909e51410155ffc07ad2badd5cd198bdb61e03413b39f`。

**题干**

求矩阵 $A=\begin{pmatrix} 3 & 1 \\ 0 & 2 \end{pmatrix}$ 的特征值和特征向量，并说明其几何意义。

**过程**

特征方程 $|\lambda I-A|=(\lambda-3)(\lambda-2)=0$，特征值 $\lambda_1=3, \lambda_2=2$。对应特征向量：$\lambda_1=3$ 时 $\xi_1=(1,0)^T$；$\lambda_2=2$ 时 $\xi_2=(1,-1)^T$。几何上，方向 $(1,0)$ 上的向量被拉伸 3 倍，方向 $(1,-1)$ 上的向量被拉伸 2 倍。

**答案原文**

$\lambda_1=3$ 对应特征向量 $(1,0)^T$，$\lambda_2=2$ 对应 $(1,-1)^T$；几何意义：变换保持这两个方向不变，分别拉伸为原来的 3 倍和 2 倍

## 36. linalg-065

内容 SHA256：`7db9a65d67b8f7166c52502c658806fbe38f57c29adfbaf5ee66e21fdfb5b856`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_linalg.jsonl，第 12 行；源 SHA256 `c2e36b7f45ffb461f1d909e51410155ffc07ad2badd5cd198bdb61e03413b39f`。

**题干**

求 λ-矩阵 $A(\lambda)=\begin{pmatrix} \lambda & 0 \\ 0 & \lambda^2-1 \end{pmatrix}$ 的不变因子和初等因子。

**过程**

该矩阵已是对角形。一阶行列式因子 $D_1=\gcd(\lambda, \lambda^2-1)=1$，二阶 $D_2=\lambda(\lambda^2-1)$。不变因子 $d_1=D_1=1$，$d_2=D_2/D_1=\lambda(\lambda^2-1)$，即不变因子为 $1, \lambda(\lambda^2-1)$；再将 $\lambda(\lambda^2-1)$ 分解为 $\lambda(\lambda-1)(\lambda+1)$，得初等因子为 $\lambda, \lambda-1, \lambda+1$。

**答案原文**

不变因子 $1, \lambda(\lambda^2-1)$；初等因子 $\lambda, \lambda-1, \lambda+1$

## 37. linalg-066

内容 SHA256：`b7e54509a59691270c01406e6c9d762a779af8cdc63fec94fb766659a6e747eb`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_linalg.jsonl，第 13 行；源 SHA256 `c2e36b7f45ffb461f1d909e51410155ffc07ad2badd5cd198bdb61e03413b39f`。

**题干**

求矩阵 $A=\begin{pmatrix} 2 & 1 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 3 \end{pmatrix}$ 的若尔当标准形。

**过程**

A 已经是分块对角形式。主对角线上有一个 2×2 的若尔当块 $J_1(2)=\begin{pmatrix} 2 & 1 \\ 0 & 2 \end{pmatrix}$ 和一个 1×1 的若尔当块 $J_2(3)=(3)$。故若尔当标准形为 $\operatorname{diag}(J_1(2), J_2(3))$。

**答案原文**

$\begin{pmatrix} 2 & 1 & 0 \\ 0 & 2 & 0 \\ 0 & 0 & 3 \end{pmatrix}$

## 38. linalg-067

内容 SHA256：`cbf7fa2c2560f28645b2917654fbefe5a10887a2e2144dc763f1ad08f29764cb`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_linalg.jsonl，第 14 行；源 SHA256 `c2e36b7f45ffb461f1d909e51410155ffc07ad2badd5cd198bdb61e03413b39f`。

**题干**

验证矩阵 $A=\begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$ 是正交矩阵，并说明其对应的正交变换。

**过程**

$A^TA=\begin{pmatrix} \cos\theta & \sin\theta \\ -\sin\theta & \cos\theta \end{pmatrix}\begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}=I$，故 A 是正交矩阵。它对应的变换是平面上的旋转 θ 角。

**答案原文**

A 是正交矩阵，对应旋转 θ 角

## 39. linalg-069

内容 SHA256：`951a4bb8417f55a111947a424c87771774c93497d466d470560eb4021a3c2228`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_linalg.jsonl，第 15 行；源 SHA256 `c2e36b7f45ffb461f1d909e51410155ffc07ad2badd5cd198bdb61e03413b39f`。

**题干**

设 $V=\mathbb{R}^2$，$\varepsilon_1=(1,0), \varepsilon_2=(0,1)$ 是标准基。求对偶基 $f_1, f_2$，使得 $f_i(\varepsilon_j)=\delta_{ij}$。

**过程**

对偶空间 $V^*$ 中的线性函数 $f$ 由其在基向量上的值唯一确定。对偶基满足 $f_1(\varepsilon_1)=1, f_1(\varepsilon_2)=0$；$f_2(\varepsilon_1)=0, f_2(\varepsilon_2)=1$。即 $f_1(x,y)=x, f_2(x,y)=y$。

**答案原文**

$f_1(x,y)=x, f_2(x,y)=y$

## 40. linalg-070

内容 SHA256：`27c88e070bfe5c01e955e01eb3d5c7e54344e21c2c9950b81f4ab89811f20789`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_linalg.jsonl，第 16 行；源 SHA256 `c2e36b7f45ffb461f1d909e51410155ffc07ad2badd5cd198bdb61e03413b39f`。

**题干**

在 $\mathbb{R}^2$ 上定义辛形式 $\omega(u,v)=u_1v_2-u_2v_1$（标准行列式形式），说明辛变换保持该形式不变的意义。

**过程**

标准辛形式即二维向量的行列式。辛变换是保持 $\omega$ 不变的线性变换，即保持任意两个向量张成的平行四边形面积不变。在二维情形下，辛变换就是行列式为 1 的线性变换。

**答案原文**

辛变换保持面积不变

## 41. prob-038

内容 SHA256：`3f126e0160543d387c893e427a38fed2db91c7f5f3cd5bf1bf804c581350d08d`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_prob.jsonl，第 1 行；源 SHA256 `8c91bd17227db6f25018939d4a995cd056a5123fb2eee2754681b9a41b363fd0`。

**题干**

已知事件 $A$ 与 $B$ 的概率分别为 $P(A) = 0.6$，$P(B) = 0.4$，且 $P(A \cap B) = 0.2$。求条件概率 $P(A|B)$ 和 $P(B|A)$。

**过程**

根据条件概率公式，$P(A|B) = \frac{P(A \cap B)}{P(B)} = \frac{0.2}{0.4} = 0.5$。$P(B|A) = \frac{P(A \cap B)}{P(A)} = \frac{0.2}{0.6} = \frac{1}{3}$。可以直观理解为在缩减的样本空间 $B$ 或 $A$ 中，交集部分所占的比例。

**答案原文**

$P(A|B) = 0.5$，$P(B|A) = \frac{1}{3}$

## 42. prob-039

内容 SHA256：`88f4fbf0c8b55dd3a18a98303f69908cbb6b12b2572c44dd91aca4035134a1f9`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_prob.jsonl，第 2 行；源 SHA256 `8c91bd17227db6f25018939d4a995cd056a5123fb2eee2754681b9a41b363fd0`。

**题干**

利用几何概型的思想，说明如何通过随机投点估算圆周率 $\pi$ 的值。

**过程**

考虑边长为2的正方形内切一个半径为1的圆。正方形的面积为4，圆的面积为 $\pi$。如果向正方形内随机投掷 $n$ 个点，点落在圆内的概率为 $P = \frac{\pi}{4}$。随着投掷次数 $n$ 增大，落入圆内的点频数 $m$ 与 $n$ 的比值 $\frac{m}{n}$ 会趋近于 $\frac{\pi}{4}$，从而可以估算 $\pi \approx \frac{4m}{n}$。

**答案原文**

$\pi \approx \frac{4m}{n}$

## 43. prob-040

内容 SHA256：`7e77395971e5529ab01d76e8d70a15fd7a32ddf9175be7f2243e9447bc41c1e4`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_prob.jsonl，第 3 行；源 SHA256 `8c91bd17227db6f25018939d4a995cd056a5123fb2eee2754681b9a41b363fd0`。

**题干**

说明当 $n$ 很大，$p$ 很小时，二项分布 $B(n, p)$ 可以近似为泊松分布 $P(\lambda)$，其中 $\lambda = np$。

**过程**

二项分布的概率质量函数为 $P(X=k) = \binom{n}{k} p^k (1-p)^{n-k}$。当 $n \to \infty$，$p \to 0$ 且 $np \to \lambda$ 时，利用极限 $\lim_{n \to \infty} (1 - \frac{\lambda}{n})^n = e^{-\lambda}$，可以推导出 $P(X=k) \to \frac{\lambda^k e^{-\lambda}}{k!}$，这正是泊松分布的概率质量函数。

**答案原文**

当 $n \to \infty$、$p \to 0$ 且 $np \to \lambda$ 时，$B(n,p)$ 的概率质量函数趋近于泊松分布 $P(\lambda)$ 的概率质量函数 $\frac{\lambda^k e^{-\lambda}}{k!}$

## 44. prob-041

内容 SHA256：`cdaf4e933c8b49d1df650ae3ec0804877a42f36a43a95f85a37cf87ec34ba3c4`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_prob.jsonl，第 4 行；源 SHA256 `8c91bd17227db6f25018939d4a995cd056a5123fb2eee2754681b9a41b363fd0`。

**题干**

分析正态分布 $X \sim N(\mu, \sigma^2)$ 的概率密度函数，说明参数 $\mu$ 和 $\sigma$ 对曲线形状的影响。

**过程**

正态分布的概率密度函数为 $f(x) = \frac{1}{\sqrt{2\pi}\sigma} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$。参数 $\mu$ 是位置参数，决定曲线的对称轴位置；参数 $\sigma$ 是尺度参数，决定曲线的陡峭程度（$\sigma$ 越大，曲线越矮胖；$\sigma$ 越小，曲线越高瘦）。

**答案原文**

$\mu$ 决定位置，$\sigma$ 决定形状的陡峭程度

## 45. prob-042

内容 SHA256：`eb53315d0b7b792d07aa88cdff4b8994a326989c15b923315731f2b0edbf764b`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_prob.jsonl，第 5 行；源 SHA256 `8c91bd17227db6f25018939d4a995cd056a5123fb2eee2754681b9a41b363fd0`。

**题干**

利用伯努利大数定律，说明抛硬币试验中正面出现的频率是如何随试验次数增加而趋于其概率的。

**过程**

设 $X_i$ 为第 $i$ 次抛硬币的指示变量（正面为1，反面为0），$P(X_i=1) = p = 0.5$。伯努利大数定律指出，对于任意 $\epsilon > 0$，有 $\lim_{n \to \infty} P\left( \left| \frac{1}{n} \sum_{i=1}^n X_i - p \right| < \epsilon \right) = 1$。即当试验次数 $n$ 趋近于无穷大时，正面出现的频率依概率收敛于其理论概率 $0.5$。

**答案原文**

频率依概率收敛于 $0.5$

## 46. prob-043

内容 SHA256：`cd33183487ca205dcd97ccae6a2a7d611538f39cd46ca967b159136cddd149c6`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_prob.jsonl，第 6 行；源 SHA256 `8c91bd17227db6f25018939d4a995cd056a5123fb2eee2754681b9a41b363fd0`。

**题干**

解释中心极限定理的核心内容，并说明当样本量 n 增大时，样本均值的分布是如何变化的。

**过程**

设随机变量 $X_1, X_2, \dots, X_n$ 相互独立且同分布，具有有限的数学期望 $\mu$ 和方差 $\sigma^2$。中心极限定理指出，当 $n$ 充分大时，标准化样本均值 $\frac{\bar{X} - \mu}{\sigma / \sqrt{n}}$ 的分布近似于标准正态分布 $N(0, 1)$。直观来说，样本均值的方差为 $\sigma^2/n$，随着 $n$ 增大，方差减小，分布变得更加集中，直方图会变高变窄，最终趋于钟形正态分布。

**答案原文**

样本均值 $\bar{X}$ 的分布趋近于正态分布 $N(\mu, \sigma^2/n)$：随着 $n$ 增大，分布变高变窄、中心不变。

## 47. prob-046

内容 SHA256：`d038b21944287a5ba07b5a291d614d3855adf1dd41d0c68acca345d5e64a668a`。

来源：data/v2/train/leakage-isolated-v3-2026-10-05/dataset_prob.jsonl，第 7 行；源 SHA256 `8c91bd17227db6f25018939d4a995cd056a5123fb2eee2754681b9a41b363fd0`。

**题干**

用几何图形直观展示可列可加性：把单位正方形分割成可列个互不相交的小矩形。

**过程**

将面积为 $1$ 的正方形依次分割：第一个矩形面积为 $\frac{1}{2}$，第二个为 $\frac{1}{4}$，第三个为 $\frac{1}{8}$，依此类推。随着分割次数趋向无穷，矩形面积构成几何级数 $\sum_{k=1}^{\infty} \frac{1}{2^k}$，其和为 $1$。这直观展示了可列可加性。

**答案原文**

可列可加性成立：各矩形面积构成几何级数 $\sum_{k=1}^{\infty} \frac{1}{2^k}$，其和为 $1$，恰等于单位正方形的总面积

## 48. draft-c01-01

内容 SHA256：`4e544b50bfa456adf21215b92c5d7d4a1ecf02ae13deda6d1392d572fefd3b08`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft-codex-repair-v4-final.jsonl，第 1 行；源 SHA256 `e52c6ac7de59e7cec9f2c56ced7e6ff399d66dbf9811ec6bac2d574c7fe7d259`。

**题干**

求曲线 $y=x^3-3x^2+2$ 上切线平行于 $x$ 轴的所有点，并写出各点处的切线方程。

**过程**

先求导：$f'(x)=3x^2-6x=3x(x-2)$。切线平行于 $x$ 轴等价于 $f'(x)=0$，即 $3x(x-2)=0$，解得 $x=0$ 或 $x=2$。当 $x=0$ 时，$f(0)=2$，切点为 $(0,2)$，切线为 $y=2$；当 $x=2$ 时，$f(2)=8-12+2=-2$，切点为 $(2,-2)$，切线为 $y=-2$。两处切点处的切线均为水平直线。

**答案原文**

切点 $(0,2)$，切线 $y=2$；切点 $(2,-2)$，切线 $y=-2$。

## 49. draft-c01-02

内容 SHA256：`a92d921a4f25488f475f1678e6fcfb8f2f619e7ad4c740f6b6e59e355d22bbbd`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft-codex-repair-v4-final.jsonl，第 2 行；源 SHA256 `e52c6ac7de59e7cec9f2c56ced7e6ff399d66dbf9811ec6bac2d574c7fe7d259`。

**题干**

设 $f(x)=\begin{cases}x^2+a, & x\leq 1\\ bx+1, & x>1\end{cases}$，其中 $a,b$ 为常数。求使 $f$ 在 $x=1$ 处连续的条件；在连续前提下，求使 $f$ 在 $x=1$ 处可微（具有有限斜率的切线）的条件，并写出此时的切线方程；再给出一组参数，使 $f$ 在 $x=1$ 处连续但不可微，并说明曲线在该点处的几何特征。

**过程**

连续性：左极限 $\lim_{x\to1^-}f(x)=1+a$，右极限 $\lim_{x\to1^+}f(x)=b+1$，连续当且仅当 $1+a=b+1$，即 $a=b$。可微性：左导数 $f'_-(1)=2x|_{x=1}=2$，右导数 $f'_+(1)=b$，可微当且仅当连续条件成立且 $b=2$，即 $a=b=2$。此时 $f(1)=1+2=3$，切线方程为 $y-3=2(x-1)$，即 $y=2x+1$。连续但不可微：取 $a=b=1$，则 $f(x)=\begin{cases}x^2+1,&x\leq1\\ x+1,&x>1\end{cases}$ 在 $x=1$ 处连续($f(1)=2$)，但左导数 $2$ 与右导数 $1$ 不相等，曲线在 $(1,2)$ 处形成角点，不存在切线。

**答案原文**

连续当且仅当 $a=b$；可微当且仅当 $a=b=2$，此时切线为 $y=2x+1$；例如 $a=b=1$ 时连续但不可微(角点 $(1,2)$，无切线)。

## 50. draft-c01-03

内容 SHA256：`1fe5f75df0026faed88bee600e2ad6c3aa0d166d7bf92e4a52db69737dabd8c4`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft-codex-repair-v4-final.jsonl，第 3 行；源 SHA256 `e52c6ac7de59e7cec9f2c56ced7e6ff399d66dbf9811ec6bac2d574c7fe7d259`。

**题干**

已知参数曲线 $\begin{cases}x=t^2\\ y=t^3-3t\end{cases}$。求曲线在 $t=2$ 对应点处的切线方程，并求出曲线上所有水平切线与竖直切线。其中参数 $t$ 取遍实数。

**过程**

参数求导：$\frac{dx}{dt}=2t$，$\frac{dy}{dt}=3t^2-3$，故 $\frac{dy}{dx}=\frac{3t^2-3}{2t}$。当 $t=2$ 时，对应点为 $(4,2)$，斜率为 $\frac{12-3}{4}=\frac{9}{4}$，切线为 $y-2=\frac{9}{4}(x-4)$，即 $y=\frac{9}{4}x-7$。水平切线需 $\frac{dy}{dt}=0$ 且 $\frac{dx}{dt}\neq 0$：$3t^2-3=0$ 得 $t=\pm 1$，对应点 $(1,-2)$ 与 $(1,2)$，切线分别为 $y=-2$ 与 $y=2$。竖直切线需 $\frac{dx}{dt}=0$ 且 $\frac{dy}{dt}\neq 0$：$2t=0$ 得 $t=0$，此时 $\frac{dy}{dt}=-3\neq 0$，对应点 $(0,0)$，切线为 $x=0$。切向量为 $(2t,3t^2-3)$，两分量不同时为零，因此曲线正则。水平切线要求 $3t^2-3=0$ 且 $2t\ne0$，即 $t=\pm1$；竖直切线要求 $2t=0$ 且 $3t^2-3\ne0$，即 $t=0$。自交点来自不同参数 $t,-t$ 满足 $t^3-3t=-(t^3-3t)$，故 $t=\pm\sqrt3$，交点为 $(3,0)$。

**答案原文**

$t=2$ 处切线 $y=\frac{9}{4}x-7$；水平切线 $y=-2$、$y=2$；竖直切线 $x=0$。

## 51. draft-c01-04

内容 SHA256：`e31489a6e1e7ee0e7f0437b9c21cc8aa66bcc77f0b0964b35eb410a860744b37`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft-codex-repair-v4-final.jsonl，第 4 行；源 SHA256 `e52c6ac7de59e7cec9f2c56ced7e6ff399d66dbf9811ec6bac2d574c7fe7d259`。

**题干**

求过点 $P(1,-2)$ 且与抛物线 $y=x^2-2x$ 相切的所有直线的方程，并写出各切点坐标。

**过程**

点 $P(1,-2)$ 不在曲线上($y(1)=1-2=-1\neq-2$)。设切点为 $(a,a^2-2a)$，切线斜率为 $2a-2$，切线方程为 $y-(a^2-2a)=(2a-2)(x-a)$。切线过 $P(1,-2)$，代入得 $-2-(a^2-2a)=(2a-2)(1-a)$，即 $-a^2+2a-2=-2a^2+4a-2$，整理得 $a^2-2a=0$，解得 $a=0$ 或 $a=2$。当 $a=0$ 时，切点为 $(0,0)$，切线为 $y=-2x$；当 $a=2$ 时，切点为 $(2,0)$，切线为 $y=2(x-2)=2x-4$。

**答案原文**

两条：切点 $(0,0)$，切线 $y=-2x$；切点 $(2,0)$，切线 $y=2x-4$。

## 52. draft-c01-05

内容 SHA256：`a94cd0232a0a31c5df6b51098d4b7640dbcc50a7fdbf05a7d8f5bd52bf141644`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft-codex-repair-v4-final.jsonl，第 5 行；源 SHA256 `e52c6ac7de59e7cec9f2c56ced7e6ff399d66dbf9811ec6bac2d574c7fe7d259`。

**题干**

求抛物线 $y=x^2$ 与 $y=-x^2+2x+1$ 的公切线；若不存在，请说明理由。

**过程**

两条曲线均是显式多项式函数的图像，切线斜率有限，不存在竖直切线。设分别在 $x=a$、$x=c$ 相切，则切线为 $y=2ax-a^2$ 与 $y=(2-2c)x+c^2+1$。两直线相同要求 $a=1-c$ 且 $-a^2=c^2+1$，从而 $c^2-c+1=(c-\frac12)^2+\frac34=0$，与左侧恒正矛盾。故无公切线。

**答案原文**

公切线不存在(推导得 $c^2-c+1=0$，判别式 $-3<0$ 无实根)。

## 53. draft-c36-01

内容 SHA256：`83b0515abfde5714e1bf3cfa0615d4f957c92a88065f4e24cf6fd5d8a2b8b796`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft-codex-repair-v4-final.jsonl，第 6 行；源 SHA256 `e52c6ac7de59e7cec9f2c56ced7e6ff399d66dbf9811ec6bac2d574c7fe7d259`。

**题干**

本题正定矩阵指实对称且二次型对所有非零实向量为正的矩阵。设 $A$ 为 $n$ 阶正定矩阵。证明 $A^{-1}$ 也是正定矩阵；并举出两个正定矩阵，其乘积不是正定矩阵的例子。

**过程**

由 $A$ 正定知 $A$ 为实对称矩阵且对任意非零向量 $x$ 有 $x^{\mathsf{T}}Ax>0$；其顺序主子式全正，故 $\det A>0$，$A$ 可逆。对任意 $x\neq 0$，令 $y=A^{-1}x$，则 $y\neq 0$，且 $x^{\mathsf{T}}A^{-1}x=(Ay)^{\mathsf{T}}A^{-1}(Ay)=y^{\mathsf{T}}A^{\mathsf{T}}A^{-1}Ay$。因 $A^{\mathsf{T}}=A$ 且 $A^{-1}A=I$，得 $x^{\mathsf{T}}A^{-1}x=y^{\mathsf{T}}Ay>0$。又 $(A^{-1})^{\mathsf{T}}=(A^{\mathsf{T}})^{-1}=A^{-1}$，故 $A^{-1}$ 也是实对称矩阵。于是 $A^{-1}$ 正定。反例：取 $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$(特征值为 $1$ 与 $3$，正定)与 $B=\begin{pmatrix}1&0\\0&3\end{pmatrix}$(特征值为 $1$ 与 $3$，正定)，则 $AB=\begin{pmatrix}2&3\\1&6\end{pmatrix}$ 不是对称矩阵，故不可能正定(正定矩阵必须对称)。

**答案原文**

证明见解法；反例：$A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$ 与 $B=\begin{pmatrix}1&0\\0&3\end{pmatrix}$ 均正定，而 $AB=\begin{pmatrix}2&3\\1&6\end{pmatrix}$ 不对称，不是正定矩阵。

## 54. draft-c36-02

内容 SHA256：`1ec88b2f40c4bec3617a6ae6cda605d1367645ce597d96a282cd94caf4ee3544`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft-codex-repair-v4-final.jsonl，第 7 行；源 SHA256 `e52c6ac7de59e7cec9f2c56ced7e6ff399d66dbf9811ec6bac2d574c7fe7d259`。

**题干**

用特征值方法判断二次型 $f(x,y,z)=2x^2+2y^2+2z^2-2xy-2yz$ 是否正定。

**过程**

二次型对应矩阵 $A=\begin{pmatrix}2&-1&0\\-1&2&-1\\0&-1&2\end{pmatrix}$。计算特征多项式:令 $u=2-\lambda$,则 $|A-\lambda I|=u(u^2-1)-u=u(u^2-2)=(2-\lambda)\left[(2-\lambda)^2-2\right]$,故特征值为 $\lambda=2$ 与 $\lambda=2\pm\sqrt{2}$,即 $2-\sqrt{2}$、$2$、$2+\sqrt{2}$(亦可由三对角对称矩阵特征值公式 $\lambda_k=2-2\cos\frac{k\pi}{4}$ 直接得出,结果一致)。三个特征值全部为正,故二次型正定。由 $\sqrt2<2$（等价于$2<4$），最小特征值 $2-\sqrt2>0$，故无需数值近似即可断定正定。

**答案原文**

正定(特征值为 $2-\sqrt{2}$、$2$、$2+\sqrt{2}$，全正)。

## 55. draft-c36-03

内容 SHA256：`4a6cb04702678790b566b39d39fa2ae2f39b4684ccd9d90a1c0085cef0c6af6f`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft-codex-repair-v4-final.jsonl，第 8 行；源 SHA256 `e52c6ac7de59e7cec9f2c56ced7e6ff399d66dbf9811ec6bac2d574c7fe7d259`。

**题干**

求使二次型 $f(x,y,z)=x^2+2xy+2y^2+az^2$ 正定的参数 $a$ 的取值范围，并讨论 $a=0$ 与 $a<0$ 时二次型的情形。

**过程**

二次型对应矩阵 $A=\begin{pmatrix}1&1&0\\1&2&0\\0&0&a\end{pmatrix}$。顺序主子式：$\Delta_1=1>0$，$\Delta_2=1\times2-1\times1=1>0$，$\Delta_3=\det A=1\times(2a-0)-1\times(a-0)+0=a$。正定当且仅当三个顺序主子式全为正，故 $a>0$。当 $a=0$ 时，$f=x^2+2xy+2y^2=(x+y)^2+y^2\geq 0$，且 $f(0,0,1)=0$，存在非零解，故半正定但非正定。当 $a<0$ 时，取 $(x,y,z)=(0,0,1)$ 得 $f(0,0,1)=a<0$，同时取 $(1,0,0)$ 得 $f(1,0,0)=1>0$，既有正值又有负值，故二次型不定。

**答案原文**

正定当且仅当 $a>0$；$a=0$ 时半正定非正定；$a<0$ 时不定。

## 56. draft-c36-04

内容 SHA256：`4173aabe33b3a0c5934cddc03e803e777d627072cb4e88273a21099d914df04e`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft-codex-repair-v4-final.jsonl，第 9 行；源 SHA256 `e52c6ac7de59e7cec9f2c56ced7e6ff399d66dbf9811ec6bac2d574c7fe7d259`。

**题干**

判断二次型 $f(x,y,z)=(x-y)^2+2(y-z)^2$ 是否正定；若不正定，判断其是否半正定，并求该二次型的秩。

**过程**

由表达式可见 $f\geq 0$ 恒成立。$f=0$ 当且仅当 $x-y=0$ 且 $y-z=0$，即 $x=y=z$，存在非零解(如 $(1,1,1)$)，故半正定但非正定。展开得 $f=x^2-2xy+3y^2-4yz+2z^2$，对应矩阵 $A=\begin{pmatrix}1&-1&0\\-1&3&-2\\0&-2&2\end{pmatrix}$。计算 $\det A=1\times(3\times2-(-2)\times(-2))-(-1)\times((-1)\times2-0)+0=2-2=0$，而二阶主子式 $\det\begin{pmatrix}1&-1\\-1&3\end{pmatrix}=2\neq0$，故秩为 $2$(零度为 $3-2=1$，与零空间 $\{(t,t,t)\}$ 一致)。令 $T=\begin{pmatrix}1&-1&0\\0&1&-1\end{pmatrix}$、$D=\operatorname{diag}(1,2)$，则 $A=T^{\mathsf T}DT$。$\ker A=\ker T=\operatorname{span}\{(1,1,1)^{\mathsf T}\}$，故 $\operatorname{rank}A=2$，惯性三元组为 $(n_+,n_-,n_0)=(2,0,1)$。

**答案原文**

不正定；半正定；秩为 $2$。

## 57. draft-c36-05

内容 SHA256：`dd324356e110a94fd7831b5a7285df52ac15c0d28851f2b5e0f01c037f02f2f3`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft-codex-repair-v4-final.jsonl，第 10 行；源 SHA256 `e52c6ac7de59e7cec9f2c56ced7e6ff399d66dbf9811ec6bac2d574c7fe7d259`。

**题干**

构造一个三阶实对称矩阵 $A$，使其所有顺序主子式均非负，但 $A$ 不是半正定的，并给出验证。

**过程**

取 $A=\begin{pmatrix}0&0&1\\0&0&1\\1&1&0\end{pmatrix}$。顺序主子式：$\Delta_1=0$，$\Delta_2=\det\begin{pmatrix}0&0\\0&0\end{pmatrix}=0$，$\Delta_3=\det A=0\times(0\times0-1\times1)-0+1\times(0\times1-0\times1)=0$，全部非负。但取 $x=(1,0,-1)^{\mathsf{T}}$，则 $x^{\mathsf{T}}Ax=2x_1x_3+2x_2x_3=2\times1\times(-1)+0=-2<0$，故 $A$ 非半正定。特征值验证：$|A-\lambda I|=-\lambda(\lambda^2-2)$，特征值为 $0$、$-\sqrt{2}$、$\sqrt{2}$，含负特征值 $-\sqrt{2}$，与结论一致。要点：顺序主子式非负不是半正定的充分条件，半正定要求所有主子式非负(如本例二、三行二、三列主子式为 $\det\begin{pmatrix}0&1\\1&0\end{pmatrix}=-1<0$)。

**答案原文**

$A=\begin{pmatrix}0&0&1\\0&0&1\\1&1&0\end{pmatrix}$；顺序主子式全为 $0$(非负)，但 $x=(1,0,-1)^{\mathsf{T}}$ 使 $x^{\mathsf{T}}Ax=-2<0$，且特征值含 $-\sqrt{2}$，故非半正定。

## 58. draft-c52-01

内容 SHA256：`2701ac5a92f036d116d60e0c5bb6549682af0ae5cbdc278e7a3e835608058bc1`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft-codex-repair-v4-final.jsonl，第 11 行；源 SHA256 `e52c6ac7de59e7cec9f2c56ced7e6ff399d66dbf9811ec6bac2d574c7fe7d259`。

**题干**

设随机变量 $X$ 的概率密度为 $f_X(x)=2x\ (0<x<1)$，其余为 $0$。求 $Y=3X+1$ 的概率密度函数。

**过程**

变换 $y=3x+1$ 在 $(0,1)$ 上严格单调递增，值域为 $(1,4)$。反解 $x=\frac{y-1}{3}$，$\left|\frac{dx}{dy}\right|=\frac{1}{3}$。由单调变换密度公式，$f_Y(y)=f_X\left(\frac{y-1}{3}\right)\cdot\frac{1}{3}=2\cdot\frac{y-1}{3}\cdot\frac{1}{3}=\frac{2(y-1)}{9}$，$1<y<4$，其余为 $0$。验证：$\int_1^4\frac{2(y-1)}{9}\,dy=\left.\frac{(y-1)^2}{9}\right|_1^4=1$。

**答案原文**

$f_Y(y)=\frac{2(y-1)}{9}$，$1<y<4$；其余为 $0$。

## 59. draft-c52-02

内容 SHA256：`66f5bdcb93f6a8266bac6654ebe5e42ec5d5467ede2ced1907200e78c845610d`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft-codex-repair-v4-final.jsonl，第 12 行；源 SHA256 `e52c6ac7de59e7cec9f2c56ced7e6ff399d66dbf9811ec6bac2d574c7fe7d259`。

**题干**

设随机变量 $X\sim N(0,1)$，求 $Y=X^2$ 的概率密度函数。

**过程**

当 $y>0$ 时，$F_Y(y)=P(X^2\leq y)=P(-\sqrt{y}\leq X\leq\sqrt{y})=\Phi(\sqrt{y})-\Phi(-\sqrt{y})=2\Phi(\sqrt{y})-1$，其中 $\Phi$ 与 $\varphi$ 分别为标准正态的分布函数与密度函数。对 $y$ 求导，$f_Y(y)=2\varphi(\sqrt{y})\cdot\frac{1}{2\sqrt{y}}=\frac{\varphi(\sqrt{y})}{\sqrt{y}}=\frac{1}{\sqrt{2\pi}}y^{-\frac{1}{2}}e^{-\frac{y}{2}}$，$y>0$；$y\leq0$ 时 $f_Y(y)=0$。即 $Y$ 服从自由度为 $1$ 的 $\chi^2$ 分布。

**答案原文**

$f_Y(y)=\frac{1}{\sqrt{2\pi}}y^{-\frac{1}{2}}e^{-\frac{y}{2}}$，$y>0$；$y\leq0$ 时 $f_Y(y)=0$。

## 60. draft-c52-03

内容 SHA256：`6049d73f6e007954e040f50b1abcd1efd1b46607ad28a05a3bec2ee0bc69dfdb`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft-codex-repair-v4-final.jsonl，第 13 行；源 SHA256 `e52c6ac7de59e7cec9f2c56ced7e6ff399d66dbf9811ec6bac2d574c7fe7d259`。

**题干**

设随机变量 $X$ 服从区间 $(-1,2)$ 上的均匀分布，求 $Y=X^2$ 的概率密度函数，并指出密度分段的分界点。

**过程**

$X$ 的密度为 $\frac{1}{3}$($-1<x<2$)。$Y=X^2$ 的值域为 $[0,4)$。当 $0<y<1$ 时，$[-\sqrt{y},\sqrt{y}]\subset(-1,2)$，故 $F_Y(y)=P(X^2\leq y)=\frac{2\sqrt{y}}{3}$，$f_Y(y)=\frac{1}{3\sqrt{y}}$。当 $1\leq y<4$ 时，区间 $[-\sqrt{y},\sqrt{y}]$ 与密度非零区间 $(-1,2)$ 的交为 $(-1,\sqrt{y}]$，故 $F_Y(y)=\frac{\sqrt{y}+1}{3}$，$f_Y(y)=\frac{1}{6\sqrt{y}}$。分界点为 $y=1$，两侧密度在该点有跳跃。验证总质量：$\int_0^1\frac{1}{3\sqrt{y}}\,dy+\int_1^4\frac{1}{6\sqrt{y}}\,dy=\frac{2}{3}+\frac{1}{3}=1$。完整 CDF 在 $y\leq0$ 时为 $0$，在 $y\geq4$ 时为 $1$；$y=1$ 处 CDF 连续但左右导数不同；密度在单个点 $y=1$ 可任取有限非负值，这不产生概率原子。这里把 $X\in(-1,2)$ 的代表取值映射为 $[0,4)$；概率律的闭支撑则为 $[0,4]$。端点的零概率与闭支撑概念不同。

**答案原文**

$f_Y(y)=\frac{1}{3\sqrt{y}}$(当 $0<y<1$)；$f_Y(y)=\frac{1}{6\sqrt{y}}$(当 $1\leq y<4$)；其余为 $0$。分界点 $y=1$。

## 61. draft-c52-04

内容 SHA256：`a94c0fb1ed26e93162a3790570423eccf67c536d57954feead6b79071af3e756`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft-codex-repair-v4-final.jsonl，第 14 行；源 SHA256 `e52c6ac7de59e7cec9f2c56ced7e6ff399d66dbf9811ec6bac2d574c7fe7d259`。

**题干**

设随机变量 $X$ 服从区间 $(0,2)$ 上的均匀分布，$Y=\min(X,1)$。求 $Y$ 的分布函数，说明其密度(含可能的概率原子)，并求 $E[Y]$。

**过程**

当 $y\leq0$ 时 $F_Y(y)=0$；当 $0<y<1$ 时，$F_Y(y)=P(\min(X,1)\leq y)=P(X\leq y)=\frac{y}{2}$；当 $y\geq1$ 时 $F_Y(y)=1$。故 $Y$ 在 $(0,1)$ 上有连续密度 $f_Y(y)=\frac{1}{2}$，在 $y=1$ 处有概率原子 $P(Y=1)=P(X\geq1)=\frac{1}{2}$。期望：$E[Y]=\int_0^1 y\cdot\frac{1}{2}\,dy+1\cdot\frac{1}{2}=\frac{1}{4}+\frac{1}{2}=\frac{3}{4}$。另一算法(经 $X$ 直接算)：$E[\min(X,1)]=\int_0^2\min(x,1)\cdot\frac{1}{2}\,dx=\frac{1}{2}\left(\int_0^1x\,dx+\int_1^2 1\,dx\right)=\frac{1}{2}\left(\frac{1}{2}+1\right)=\frac{3}{4}$，两法一致。

**答案原文**

$F_Y(y)=0\ (y\leq0)$；$F_Y(y)=\frac{y}{2}\ (0<y<1)$；$F_Y(y)=1\ (y\geq1)$。密度:连续部分 $\frac{1}{2}$($0<y<1$)加原子质量 $\frac{1}{2}$ 于 $y=1$。$E[Y]=\frac{3}{4}$。整体没有通常的概率密度函数；分布由上述连续部分和质量 $\frac12$ 的原子组成。

## 62. draft-c52-05

内容 SHA256：`0d935f041a3ab2f08ceb3906272389589f1b2bfdcdd9f3b5d772801b58dbcf08`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-01/draft-codex-repair-v4-final.jsonl，第 15 行；源 SHA256 `e52c6ac7de59e7cec9f2c56ced7e6ff399d66dbf9811ec6bac2d574c7fe7d259`。

**题干**

设随机变量 $X$ 的分布函数 $F$ 连续，在某区间 $I$ 上严格递增，且 $P(X\in I)=1$、$F(I)=(0,1)$。证明 $Y=F(X)\sim U(0,1)$。再设目标随机变量 $Z$ 的密度为 $g(z)=\begin{cases}\frac12,&0<z<1\\ z-1,&1<z<2\\0,&\text{otherwise}\end{cases}$。给定 $U\sim U(0,1)$，构造 $Z=T(U)$，写出完整分布函数并验证其分布；说明为何 $T$ 必须分段。

**过程**

对 $0<y<1$，由假设，$F$ 在 $I$ 上存在反函数 $F_I^{-1}$。除零概率事件外，$F(X)\le y$ 等价于 $X\le F_I^{-1}(y)$，所以 $P(Y\le y)=F(F_I^{-1}(y))=y$；$y\le0$ 时概率为 $0$，$y\ge1$ 时为 $1$，故 $Y\sim U(0,1)$。目标密度非负，且 $\int_0^1\frac12\,dz+\int_1^2(z-1)\,dz=\frac12+\frac12=1$。积分得 $G(z)=\begin{cases}0,&z\le0\\\frac z2,&0<z\le1\\\frac12+\frac{(z-1)^2}{2},&1<z<2\\1,&z\ge2\end{cases}$，在 $z=1$ 连续，$G(1)=\frac12$。两段 CDF 的反函数分别为 $T(u)=2u$（$0<u\le\frac12$）与 $T(u)=1+\sqrt{2u-1}$（$\frac12<u<1$）。令 $Z=T(U)$。若 $0<z\le1$，事件 $T(U)\le z$ 等价于 $U\le z/2$，概率为 $z/2$；若 $1<z<2$，等价于 $U\le\frac12+\frac{(z-1)^2}{2}$，概率为该阈值。外侧概率分别为 $0$ 和 $1$，所以构造确有 CDF $G$。密度在单点 $z=1$ 的取值不影响分布；此处 CDF 无跳跃、没有原子。逆映射在 $u=\frac12$ 处分段，因为目标 CDF 的两段表达式不同，不能以一个线性或幂函数代替全部分支。

**答案原文**

$Y\sim U(0,1)$；$Z=T(U)$，其中 $T(u)=\begin{cases}2u,&0<u\le\frac12\\1+\sqrt{2u-1},&\frac12<u<1\end{cases}$。完整 CDF：$G(z)=0$（$z\le0$）、$z/2$（$0<z\le1$）、$\frac12+\frac{(z-1)^2}{2}$（$1<z<2$）、$1$（$z\ge2$）。

## 63. draft-c11-01

内容 SHA256：`bf3d3283593637f568bd1c043e700797e4988b2e9c4a664c06e4df0e26b78203`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft-codex-repair-v6.jsonl，第 1 行；源 SHA256 `fc452babbd4d0e70583703759186527f6fc2631f1b875e4b49e13c5a3ba4168f`。

**题干**

求幂级数 $\sum_{n=1}^{\infty}\left(\frac{n}{n+1}\right)^{n^2}x^n$ 的收敛域。

**过程**

设 $u_n=\frac1{n+1}$、$a_n=(1-u_n)^{n^2}$。由 $u\le-\ln(1-u)\le\frac{u}{1-u}$，有 $\frac{n}{n+1}\le-n\ln(1-u_n)\le1$，故 $\lim a_n^{1/n}=e^{-1}$，收敛半径 $R=e$。为判端点，写 $-\ln(1-u)=u+\frac{u^2}{2}+r(u)$，其中 $0\le r(u)=\sum_{k=3}^{\infty}\frac{u^k}{k}\le\frac{u^3}{3(1-u)}$。于是 $0\le n^2r(u_n)\le\frac{n}{3(n+1)^2}\to0$，且 $n+n^2\ln(1-u_n)=\frac{n}{n+1}-\frac{n^2}{2(n+1)^2}-n^2r(u_n)\to\frac12$。当 $x=\pm e$ 时，通项绝对值趋于 $e^{1/2}\ne0$，故两端点发散。收敛域为 $(-e,e)$。

**答案原文**

收敛域为 $(-e,e)$。

## 64. draft-c11-02

内容 SHA256：`aa7bf3d19ab677f88f9fd3dc9c4f2483b09ac7cccb7184252c111b121ff04ccf`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft-codex-repair-v6.jsonl，第 2 行；源 SHA256 `fc452babbd4d0e70583703759186527f6fc2631f1b875e4b49e13c5a3ba4168f`。

**题干**

把$f(x)=1/(1+x^2)$在$x=1$处展开为$\sum_{n=0}^{\infty}c_n(x-1)^n$。求系数的显式式、收敛半径和实收敛域，严格检查两个端点，并解释为什么相邻系数比值法不适用。

**过程**

令$h=x-1$。由$(2+2h+h^2)\sum c_nh^n=1$，得$c_0=1/2,c_1=-1/2$及$c_n=-c_{n-1}-c_{n-2}/2$（$n\ge2$）。递推根为$(-1\pm i)/2$，初值给$c_n=(-1)^n2^{-(n+1)/2}\sin((n+1)\pi/4)$，可代回验证。于是$|c_n|\le2^{-(n+1)/2}$，而$n=8k$时$|c_n|=2^{-(n+2)/2}$，故$\limsup|c_n|^{1/n}=1/\sqrt2$，半径$R=\sqrt2$。在$|h|<\sqrt2$绝对收敛，乘以$2+2h+h^2$验证其和确为$f(1+h)$。在$h=\pm\sqrt2$，沿$n=8k$子列通项绝对值恒为$1/2$，故两个端点均发散；区间外同一子列绝对值为$(|h|/\sqrt2)^{8k}/2$，不趋于零。因此实收敛域为$(1-\sqrt2,1+\sqrt2)$。$c_{4k+3}=0$但相邻其他系数非零，普通相邻系数比值极限不存在，不能据此错误断定半径；必须用根值上极限或复根幅度。

**答案原文**

$c_n=(-1)^n2^{-(n+1)/2}\sin((n+1)\pi/4)$；$R=\sqrt2$，实收敛域$(1-\sqrt2,1+\sqrt2)$，两端均发散。

## 65. draft-c11-03

内容 SHA256：`203ba703ba0e89fcd0d6aa1fd08a46a18acfc2fd012a30b40fabb0f826ea493a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft-codex-repair-v6.jsonl，第 3 行；源 SHA256 `fc452babbd4d0e70583703759186527f6fc2631f1b875e4b49e13c5a3ba4168f`。

**题干**

设$S(x)=\sum_{n=0}^{\infty}x^{2^n}$。求其收敛域，证明$S(x)=x+S(x^2)$；并证明在$(-1,1)$上，满足该方程、在$0$处连续且$S(0)=0$的函数唯一。

**过程**

若$|x|=r<1$，由$2^n\ge n+1$有$\sum|x|^{2^n}\le\sum r^{n+1}=r/(1-r)$，故绝对收敛，并在每个$[-r,r]$上一致收敛。当$x=1$时通项为$1$；当$x=-1$时从$n=1$起通项为$1$；当$|x|>1$时通项不趋于$0$。收敛域为$(-1,1)$。绝对收敛允许重编号：$S(x^2)=\sum_{n=1}^{\infty}x^{2^n}$，故$S(x)=x+S(x^2)$，且$S(0)=0$。若$F,G$满足条件，令$D=F-G$，则$D(x)=D(x^2)=D(x^{2^m})$；因$|x|<1$，$x^{2^m}\to0$，由$0$处连续得$D(x)=D(0)=0$。故唯一。有限展开也有精确尾项恒等式$S(x)=\sum_{j=0}^{m-1}x^{2^j}+S(x^{2^m})$，不是数值拟合。

**答案原文**

收敛域$(-1,1)$；唯一满足条件的函数为$S(x)=\sum_{n=0}^{\infty}x^{2^n}$，且$S(x)=x+S(x^2)$。

## 66. draft-c11-04

内容 SHA256：`985229417c4a22e385c1d5ac9b1f98d8be9a4bb6471892b7bd8baf808e23bc2a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft-codex-repair-v6.jsonl，第 4 行；源 SHA256 `fc452babbd4d0e70583703759186527f6fc2631f1b875e4b49e13c5a3ba4168f`。

**题干**

设$a_0=1,a_1=0$，$a_n=a_{n-1}+2a_{n-2}$（$n\ge2$）。求幂级数$S(x)=\sum_{n=0}^{\infty}a_nx^n$的收敛域与和函数，并求$S(1/4)$。

**过程**

递推特征根为$2,-1$，由初值得$a_n=(2^n+2(-1)^n)/3$，可直接代回验证。于是$S(x)=\frac13\sum(2x)^n+\frac23\sum(-x)^n$，在$|x|<1/2$绝对收敛，其和为$\frac1{3(1-2x)}+\frac2{3(1+x)}=\frac{1-x}{1-x-2x^2}$。若$|x|>1/2$，$|a_nx^n|\ge((2|x|)^n-2|x|^n)/3$最终不趋于零。当$x=1/2$时通项趋于$1/3$；当$x=-1/2$时通项为$((-1)^n+2(1/2)^n)/3$，其绝对值趋于$1/3$。两端均发散，故收敛域为$(-1/2,1/2)$。亦可由递推在收敛域内得到$(1-x-2x^2)S(x)=1-x$。代入$x=1/4$得$S(1/4)=(3/4)/(5/8)=6/5$。

**答案原文**

$S(x)=\frac{1-x}{1-x-2x^2}$，收敛域$(-1/2,1/2)$；$S(1/4)=6/5$。

## 67. draft-c11-05

内容 SHA256：`6d107667df41214436621a32a4c690c39508c44956ea6c5f07a507673d441033`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft-codex-repair-v6.jsonl，第 5 行；源 SHA256 `fc452babbd4d0e70583703759186527f6fc2631f1b875e4b49e13c5a3ba4168f`。

**题干**

设$a_n=\binom{2n}{n}/4^n$，$S(x)=\sum_{n=0}^{\infty}a_nx^n$。由系数递推推导$S$满足的微分方程，求和函数与实收敛域，并严格处理两个端点。

**过程**

$a_0=1$，$a_{n+1}/a_n=(2n+1)/(2n+2)$，比值法给半径$1$。在$|x|<1$可逐项求导，由$2(n+1)a_{n+1}=(2n+1)a_n$得$2(1-x)S^{\prime}=S$、$S(0)=1$，故$S(x)=(1-x)^{-1/2}$。在$x=1$，因$\binom{2n}{n}$是第$2n$行最大的二项式系数，而该行总和为$4^n$，有$a_n\ge1/(2n+1)\ge1/(2n+2)$，故级数发散。在$x=-1$，$a_n$严格递减且$a_n\to0$：对$n\ge1$，$a_n=\prod_{k=1}^n(1-1/(2k))$，由$\ln(1-u)\le-u$得$0<a_n\le\exp(-\sum_{k=1}^n1/(2k))\to0$。莱布尼茨判别法给交错端点收敛，绝对值级数已证明发散。由阿贝尔定理，该端点和为$S(-1)=1/\sqrt2=\sqrt2/2$。因此实收敛域为$[-1,1)$，和函数为$1/\sqrt{1-x}$，包含$x=-1$。

**答案原文**

$2(1-x)S^{\prime}=S$，$S(0)=1$；$S(x)=1/\sqrt{1-x}$，收敛域$[-1,1)$，$S(-1)=\sqrt2/2$。

## 68. draft-c33-01

内容 SHA256：`d4cb3411213189a458ef1dec1f1b1339591095207da4c4b6c66c45c8c55425f1`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft-codex-repair-v6.jsonl，第 6 行；源 SHA256 `fc452babbd4d0e70583703759186527f6fc2631f1b875e4b49e13c5a3ba4168f`。

**题干**

用初等行变换求矩阵 $A=\begin{pmatrix}1&2&3\\0&1&2\\0&0&1\end{pmatrix}$ 的逆矩阵。

**过程**

构造增广矩阵并作行变换:$\left(\begin{array}{ccc|ccc}1&2&3&1&0&0\\0&1&2&0&1&0\\0&0&1&0&0&1\end{array}\right)$。第三行乘 $-2$ 加到第二行、乘 $-3$ 加到第一行,得 $\left(\begin{array}{ccc|ccc}1&2&0&1&0&-3\\0&1&0&0&1&-2\\0&0&1&0&0&1\end{array}\right)$;第二行乘 $-2$ 加到第一行,得 $\left(\begin{array}{ccc|ccc}1&0&0&1&-2&1\\0&1&0&0&1&-2\\0&0&1&0&0&1\end{array}\right)$。故 $A^{-1}=\begin{pmatrix}1&-2&1\\0&1&-2\\0&0&1\end{pmatrix}$。验证:$AA^{-1}=I$(逐项相乘即得)。

**答案原文**

$A^{-1}=\begin{pmatrix}1&-2&1\\0&1&-2\\0&0&1\end{pmatrix}$。

## 69. draft-c33-02

内容 SHA256：`8efda667da901ddbe9277505e78b753a6d798daf061bc40047cd40cc5543019f`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft-codex-repair-v6.jsonl，第 7 行；源 SHA256 `fc452babbd4d0e70583703759186527f6fc2631f1b875e4b49e13c5a3ba4168f`。

**题干**

求使矩阵 $A=\begin{pmatrix}1&1&a\\1&a&1\\a&1&1\end{pmatrix}$ 可逆的参数 $a$ 的取值范围；并求 $a=0$ 时的逆矩阵。

**过程**

计算行列式(按第一行展开)：$\det A=1\times(a\cdot1-1\cdot1)-1\times(1\cdot1-1\cdot a)+a\times(1\cdot1-a\cdot a)=(a-1)-(1-a)+a(1-a^2)=3a-2-a^3=-(a-1)^2(a+2)$。可逆当且仅当 $\det A\neq0$，即 $a\neq1$ 且 $a\neq-2$。当 $a=0$ 时，$A=\begin{pmatrix}1&1&0\\1&0&1\\0&1&1\end{pmatrix}$。由增广矩阵消元(或直接验证)得 $A^{-1}=\frac12\begin{pmatrix}1&1&-1\\1&-1&1\\-1&1&1\end{pmatrix}$。验证:$AA^{-1}=I$。

**答案原文**

可逆当且仅当 $a\neq1$ 且 $a\neq-2$;$a=0$ 时 $A^{-1}=\frac12\begin{pmatrix}1&1&-1\\1&-1&1\\-1&1&1\end{pmatrix}$。

## 70. draft-c33-03

内容 SHA256：`a3a0c2e3998f003e7e59cb6b70742c6d6f4e2dc54950c40bbcb92fac577211a8`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft-codex-repair-v6.jsonl，第 8 行；源 SHA256 `fc452babbd4d0e70583703759186527f6fc2631f1b875e4b49e13c5a3ba4168f`。

**题干**

用分块方法求矩阵 $M=\begin{pmatrix}2&1&1\\1&1&0\\0&0&2\end{pmatrix}$ 的逆矩阵。

**过程**

将 $M$ 分块为 $\begin{pmatrix}A&b\\0&d\end{pmatrix}$，其中 $A=\begin{pmatrix}2&1\\1&1\end{pmatrix}$，$b=\begin{pmatrix}1\\0\end{pmatrix}$，$d=2$。$A$ 可逆且 $A^{-1}=\begin{pmatrix}1&-1\\-1&2\end{pmatrix}$。由分块上三角矩阵求逆公式，$M^{-1}=\begin{pmatrix}A^{-1}&-\frac{1}{d}A^{-1}b\\0&\frac{1}{d}\end{pmatrix}$。计算 $A^{-1}b=\begin{pmatrix}1\\-1\end{pmatrix}$，故 $-\frac12A^{-1}b=\begin{pmatrix}-\frac12\frac12\end{pmatrix}$。于是 $M^{-1}=\begin{pmatrix}1&-1&-\frac12\\-1&2&\frac12\\0&0&\frac12\end{pmatrix}$。验证:$MM^{-1}=I$(逐行相乘核对)。

**答案原文**

$M^{-1}=\begin{pmatrix}1&-1&-\frac12\\-1&2&\frac12\\0&0&\frac12\end{pmatrix}$。

## 71. draft-c33-04

内容 SHA256：`50a054a386bc25e63a0909750cc2b5ddd0777c33588e1b812d68e18d9f3157e0`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft-codex-repair-v6.jsonl，第 9 行；源 SHA256 `fc452babbd4d0e70583703759186527f6fc2631f1b875e4b49e13c5a3ba4168f`。

**题干**

求矩阵 $A=\begin{pmatrix}1&0\\0&1\\1&1\end{pmatrix}$ 的一个左逆与矩阵 $B=\begin{pmatrix}1&0&1\\0&1&1\end{pmatrix}$ 的一个右逆，并说明这两种单边逆的区别与不唯一性。

**过程**

$A$ 为 $3\times2$ 列满秩矩阵。取 $L=\begin{pmatrix}1&0&0\\0&1&0\end{pmatrix}$，则 $LA=\begin{pmatrix}1&0\\0&1\end{pmatrix}=I_2$，故 $L$ 是 $A$ 的一个左逆。$B$ 为 $2\times3$ 行满秩矩阵。取 $R=\begin{pmatrix}1&0\\0&1\\0&0\end{pmatrix}$，则 $BR=\begin{pmatrix}1&0\\0&1\end{pmatrix}=I_2$，故 $R$ 是 $B$ 的一个右逆。区别:列满秩的「高瘦」矩阵只可能有左逆($LA=I$),行满秩的「宽扁」矩阵只可能有右逆($BR=I$);只有方阵且可逆时才存在同时满足两侧的双边逆。不唯一性:$A$ 的左逆一般形式为 $\begin{pmatrix}1-t&-t&t\\-s&1-s&s\end{pmatrix}$($t,s$ 为任意实数),$L$ 对应 $t=s=0$,$\begin{pmatrix}0&-1&1\\1&2&-1\end{pmatrix}$ 对应 $t=1,s=-1$,也是左逆;$B$ 的右逆同理不唯一。一般地，$m\times n$ 矩阵有左逆当且仅当列满秩（故$m\ge n$），有右逆当且仅当行满秩（故$m\le n$）。严格高瘦/宽扁情形的相应单边逆不唯一；可逆方阵的左右逆一致且唯一。因本题 $B=A^{\mathsf T}$，全部右逆可写成 $R(t,s)=\begin{pmatrix}1-t&-s\\-t&1-s\\t&s\end{pmatrix}$，有 $BR(t,s)=I_2$。

**答案原文**

$L=\begin{pmatrix}1&0&0\\0&1&0\end{pmatrix}$ 满足 $LA=I_2$，$R=\begin{pmatrix}1&0\\0&1\\0&0\end{pmatrix}$ 满足 $BR=I_2$。一般左逆要求列满秩、$m\ge n$，右逆要求行满秩、$m\le n$；本题两种单边逆均不唯一，可逆方阵则有唯一双边逆。

## 72. draft-c33-05

内容 SHA256：`f164a181a465d7a6a44bfabd3d543c76145b80f467422c9c91f83aa7c71e658d`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft-codex-repair-v6.jsonl，第 10 行；源 SHA256 `fc452babbd4d0e70583703759186527f6fc2631f1b875e4b49e13c5a3ba4168f`。

**题干**

令加权循环矩阵$C=\begin{pmatrix}0&2&0\\0&0&3\\1/6&0&0\end{pmatrix}$，$A_t=I-tC$，$t\in\mathbb R$。用矩阵多项式恒等式求全部可逆参数及逆矩阵。在唯一奇异参数下，求$A_tx=b$的相容条件与全部解。

**过程**

$C^3=I$，故$(I-tC)(I+tC+t^2C^2)=(1-t^3)I$，两因子均为$C$的多项式，因此逆序乘积也相同。对实数$t\ne1$，$A_t^{-1}=(I+tC+t^2C^2)/(1-t^3)=\frac1{1-t^3}\begin{pmatrix}1&2t&6t^2\\t^2/2&1&3t\\t/6&t^2/3&1\end{pmatrix}$。直接行列式为$1-t^3$，唯一实奇异参数$t=1$。此时方程为$x_1-2x_2=b_1,x_2-3x_3=b_2,x_3-x_1/6=b_3$，将三式分别乘$1,2,6$再相加得必要条件$b_1+2b_2+6b_3=0$。若此条件满足，任意$s\in\mathbb R$给$x=(6s+2b_2+b_1,3s+b_2,s)$，代入三式均成立；反过来任何解均由第三坐标$s$决定，故这是全部解。核为$\operatorname{span}\{(6,3,1)\}$、像为$\{b:b_1+2b_2+6b_3=0\}$、秩为$2$。

**答案原文**

$t\ne1$时$A_t^{-1}=\frac1{1-t^3}\begin{pmatrix}1&2t&6t^2\\t^2/2&1&3t\\t/6&t^2/3&1\end{pmatrix}$；$t=1$时相容当且仅当$b_1+2b_2+6b_3=0$，全部解$(6s+2b_2+b_1,3s+b_2,s)$，$s\in\mathbb R$。

## 73. draft-c51-01

内容 SHA256：`ff55d50a543c4f6efc8fdff632ae8e0a416bf9813cececb703e3ecfac067131f`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft-codex-repair-v6.jsonl，第 11 行；源 SHA256 `fc452babbd4d0e70583703759186527f6fc2631f1b875e4b49e13c5a3ba4168f`。

**题干**

三台机器 $M_1,M_2,M_3$ 的产量分别占总产量的 $\frac12$、$\frac3{10}$、$\frac15$，次品率分别为 $\frac1{50}$、$\frac3{100}$、$\frac1{25}$。随机抽取一件产品发现是次品，求它分别来自三台机器的概率，并验证三者之和为 $1$。

**过程**

记 $D$ 为抽到次品。$P(D)=\frac12\times\frac{2}{100}+\frac{3}{10}\times\frac{3}{100}+\frac15\times\frac{4}{100}=\frac{1}{100}+\frac{9}{1000}+\frac{8}{1000}=\frac{27}{1000}$。由贝叶斯公式，$P(M_1\mid D)=\frac{\frac12\times\frac{2}{100}}{\frac{27}{1000}}=\frac{10}{27}$，$P(M_2\mid D)=\frac{\frac{3}{10}\times\frac{3}{100}}{\frac{27}{1000}}=\frac{9}{27}=\frac13$，$P(M_3\mid D)=\frac{\frac15\times\frac{4}{100}}{\frac{27}{1000}}=\frac{8}{27}$。验证:$\frac{10}{27}+\frac13+\frac{8}{27}=\frac{10+9+8}{27}=1$。

**答案原文**

$P(M_1\mid D)=\frac{10}{27}$，$P(M_2\mid D)=\frac13$，$P(M_3\mid D)=\frac{8}{27}$;三者之和为 $1$。

## 74. draft-c51-02

内容 SHA256：`80fbfcf5880a886aac23ff67b1cffcb1c780d0546c4015e53e5d0fe760dc32d0`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft-codex-repair-v6.jsonl，第 12 行；源 SHA256 `fc452babbd4d0e70583703759186527f6fc2631f1b875e4b49e13c5a3ba4168f`。

**题干**

先随机选择硬币参数$\Theta$：$P(\Theta=1/4)=2/3$，$P(\Theta=3/4)=1/3$。给定$\Theta$后各次抛掷独立，正面概率为$\Theta$。观测前三次恰有两次正面，求$\Theta$的后验分布及第四次为正面的预测概率。

**过程**

令$K$为前三次正面数。条件似然为$P(K=2\mid\Theta=1/4)=\binom32(1/4)^2(3/4)=9/64$，$P(K=2\mid\Theta=3/4)=27/64$。边缘概率$P(K=2)=(2/3)(9/64)+(1/3)(27/64)=15/64>0$。贝叶斯公式给$P(\Theta=3/4\mid K=2)=(9/64)/(15/64)=3/5$，另一个后验概率为$2/5$。给定参数时第四次与前三次独立，故预测概率为$(2/5)(1/4)+(3/5)(3/4)=11/20$。这里计算的是参数后验及后验预测，不以独立性辨析代替后验任务。

**答案原文**

后验$P(\Theta=1/4\mid K=2)=2/5$、$P(\Theta=3/4\mid K=2)=3/5$；第四次正面概率$11/20$。

## 75. draft-c51-03

内容 SHA256：`cc37c7138b5ad744a5eed900e6009ee715c175bafa270517ef2f85331d9cddf1`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft-codex-repair-v6.jsonl，第 13 行；源 SHA256 `fc452babbd4d0e70583703759186527f6fc2631f1b875e4b49e13c5a3ba4168f`。

**题干**

某疾病患病率为 $\frac{1}{1000}$。一次检测对患病者呈阳性的概率为 $\frac{99}{100}$，对未患病者呈阳性的概率为 $\frac{1}{100}$。某人第一次检测呈阳性，随后做了一次独立(在给定患病状态下)的同类检测，仍呈阳性。求两次检测后此人患病的概率，并与第一次检测后的概率对比。

**过程**

第一次阳性后，由贝叶斯公式，$P(\text{diseased}\mid+_1)=\frac{\frac{1}{1000}\times\frac{99}{100}}{\frac{1}{1000}\times\frac{99}{100}+\frac{999}{1000}\times\frac{1}{100}}=\frac{99}{99+999}=\frac{99}{1098}=\frac{11}{122}$。第二次检测在给定患病状态下与第一次独立，故将 $\frac{11}{122}$ 作为新的先验再更新：$P(\text{diseased}\mid+_1,+_2)=\frac{\frac{11}{122}\times\frac{99}{100}}{\frac{11}{122}\times\frac{99}{100}+\frac{111}{122}\times\frac{1}{100}}=\frac{1089}{1089+111}=\frac{1089}{1200}=\frac{363}{400}$。对比:单次阳性后为 $\frac{11}{122}$，两次后为 $\frac{363}{400}$。

**答案原文**

第一次阳性后:$P=\frac{11}{122}$;两次阳性后:$P=\frac{363}{400}$。

## 76. draft-c51-04

内容 SHA256：`82883f0a0c11924a768c2aa0f9ba363f2382a08bd35bd7b051ce5090b9bdbd47`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft-codex-repair-v6.jsonl，第 14 行；源 SHA256 `fc452babbd4d0e70583703759186527f6fc2631f1b875e4b49e13c5a3ba4168f`。

**题干**

设一枚硬币正面朝上的概率为 $\theta$，先验取 $\theta\sim U(0,1)$。抛 $10$ 次观察到 $7$ 次正面。求 $\theta$ 的后验密度与后验均值。

**过程**

似然为 $L(\theta)=\binom{10}{7}\theta^7(1-\theta)^3\propto\theta^7(1-\theta)^3$，先验密度在 $(0,1)$ 上为常数 $1$，故后验密度 $\propto\theta^{8-1}(1-\theta)^{4-1}$，即 $\theta\mid\text{data}\sim\mathrm{Beta}(8,4)$。归一化常数 $\frac{\Gamma(12)}{\Gamma(8)\Gamma(4)}=\frac{11!}{7!\times3!}=1320$，故后验密度 $f(\theta)=1320\,\theta^7(1-\theta)^3$，$0<\theta<1$。后验均值 $\frac{8}{8+4}=\frac23$。(后验均值介于先验均值 $\frac12$ 与频率 $\frac{7}{10}$ 之间,符合共轭更新的收缩性质。)

**答案原文**

后验密度 $f(\theta)=1320\,\theta^7(1-\theta)^3$($0<\theta<1$),即 $\mathrm{Beta}(8,4)$;后验均值 $\frac23$。 支撑区间外密度为$0$。

## 77. draft-c51-05

内容 SHA256：`9ff68b8697613dae262a6d7504d1a3e4c2acecb5495c4f3696937518894e0df4`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-02/draft-codex-repair-v6.jsonl，第 15 行；源 SHA256 `fc452babbd4d0e70583703759186527f6fc2631f1b875e4b49e13c5a3ba4168f`。

**题干**

设 $H$ 与 $\bar H$ 为互斥且穷尽的假设，观测 $D_1,D_2$ 在给定 $H$(及给定 $\bar H$)下条件独立。假设$0<P(H)<1$，且$P(D_i\mid H)>0$、$P(D_i\mid\bar H)>0$（$i=1,2$），以保证条件概率及有限优势比有定义。证明后验优势比可写成先验优势比与两个似然比的乘积，并说明更新顺序不影响最终后验；再用两次独立阳性检测的数据($P(H)=\frac{1}{1000}$，灵敏度与误报率分别为 $\frac{99}{100}$ 与 $\frac{1}{100}$)验证所得后验为 $\frac{363}{400}$。

**过程**

由贝叶斯公式与条件独立性，$\frac{P(H\mid D_1,D_2)}{P(\bar H\mid D_1,D_2)}=\frac{P(H)}{P(\bar H)}\cdot\frac{P(D_1\mid H)}{P(D_1\mid\bar H)}\cdot\frac{P(D_2\mid H)}{P(D_2\mid\bar H)}$。乘积形式对 $D_1,D_2$ 对称，故更新顺序不影响最终后验优势比。验证:先验优势比 $\frac{P(H)}{P(\bar H)}=\frac{1}{999}$;每次阳性的似然比 $\frac{99/100}{1/100}=99$。两次阳性后，后验优势比 $=\frac{1}{999}\times99^2=\frac{9801}{999}=\frac{363}{37}$，故后验概率 $=\frac{363}{363+37}=\frac{363}{400}$，与逐次更新结果一致。

**答案原文**

证明见解法(乘积形式);验证:$P(H\mid +_1,+_2)=\frac{363}{400}$。

## 78. draft-c35-01

内容 SHA256：`c596f50814224df159b522f89c0e41ac01033902a0fe7bd33e5369483ce5e289`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft-codex-repair-v4-final.jsonl，第 1 行；源 SHA256 `cf876d0a55020e12a3585a04513f0247b94ce192e738835d0cb31e1f22d0feac`。

**题干**

用配方法将二次型 $f(x,y,z)=x^2+4xy+3y^2+z^2$ 化为标准形，写出所用的可逆线性替换，并求其正负惯性指数、秩与正定性。

**过程**

先对含 $x$ 的项配方：$x^2+4xy+3y^2=(x+2y)^2-y^2$，故 $f=(x+2y)^2-y^2+z^2$。令 $u=x+2y$，$v=y$，$w=z$，则 $f=u^2-v^2+w^2$ 为标准形；线性替换为 $x=u-2v$，$y=v$，$z=w$，其系数矩阵 $\begin{pmatrix}1&-2&0\\0&1&0\\0&0&1\end{pmatrix}$ 的行列式为 $1\neq0$，可逆。正惯性指数 $2$，负惯性指数 $1$，秩 $3$。因负惯性指数非零，二次型不定(非正定)。令 $C=\begin{pmatrix}1&-2&0\\0&1&0\\0&0&1\end{pmatrix}$，有 $C^{\mathsf T}AC=\operatorname{diag}(1,-1,1)$。$\det C=1$，$(n_+,n_-,n_0)=(2,1,0)$。既有正方向又有负方向才推出不定：$f(1,0,0)=1>0$、$f(-2,1,0)=-1<0$。

**答案原文**

标准形 $u^2-v^2+w^2$，替换 $x=u-2v,y=v,z=w$;正惯性指数 $2$，负惯性指数 $1$，秩 $3$，不定。

## 79. draft-c35-02

内容 SHA256：`40b53c03ebff1e0706f316ca001d54812a706d920dc0e385e50dc9a2181189e4`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft-codex-repair-v4-final.jsonl，第 2 行；源 SHA256 `cf876d0a55020e12a3585a04513f0247b94ce192e738835d0cb31e1f22d0feac`。

**题干**

对四元二次型$f=(x_1-x_2)^2+2(x_2-x_3)^2+3(x_3-x_4)^2$，给出可逆线性替换、合同标准形及惯性；再证明将$f$限制在$V=\{x:x_4=0\}$上后成为正定型。

**过程**

令$u_1=x_1-x_2,u_2=x_2-x_3,u_3=x_3-x_4,w=x_4$。反解为$x_4=w,x_3=u_3+w,x_2=u_2+u_3+w,x_1=u_1+u_2+u_3+w$，故替换可逆。标准形为$u_1^2+2u_2^2+3u_3^2+0w^2$；再伸缩$v_1=u_1,v_2=\sqrt2u_2,v_3=\sqrt3u_3$得规范形$v_1^2+v_2^2+v_3^2+0w^2$。全空间的秩为$3$，惯性为$(3,0,1)$，核为$\operatorname{span}\{(1,1,1,1)\}$。若$x\in V$且$f(x)=0$，三个平方均为零，故$x=c(1,1,1,1)$；第四坐标为零又给$c=0$，故$x=0$。因此$f|_V$正定；$\dim V=3$，其惯性为$(3,0,0)$。亦可在新坐标中写约束$w=0$，三个差分坐标仍独立，标准形保留三个正平方。

**答案原文**

全空间标准形$u_1^2+2u_2^2+3u_3^2+0w^2$，秩$3$、惯性$(3,0,1)$；限制在$V$上正定，惯性$(3,0,0)$。

## 80. draft-c35-03

内容 SHA256：`054429ee64ab0a77311a70957ee6937e2fda2468da06a0081200818b8d70ebb1`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft-codex-repair-v4-final.jsonl，第 3 行；源 SHA256 `cf876d0a55020e12a3585a04513f0247b94ce192e738835d0cb31e1f22d0feac`。

**题干**

求使二次型 $f(x,y)=x^2+2xy+ay^2$ 的秩为 $1$ 的参数 $a$ 的值；并分别求 $a=0$、$a=1$、$a=2$ 时的标准形与正负惯性指数。

**过程**

令 $u=x+y,v=y$，则 $f=u^2+(a-1)v^2$，对应 $C=\begin{pmatrix}1&-1\\0&1\end{pmatrix}$ 满足 $C^{\mathsf T}AC=\operatorname{diag}(1,a-1)$，$\det C=1$。因 $A_{11}=1\ne0$，$\operatorname{rank}A\ge1$；$\det A=a-1$，故秩为$1$当且仅当$a=1$。$a=0$时标准形$u^2-v^2$、惯性三元组$(1,1,0)$、秩$2$；$a=1$时$u^2+0v^2$、惯性三元组$(1,0,1)$、秩$1$；$a=2$时$u^2+v^2$、惯性三元组$(2,0,0)$、秩$2$。

**答案原文**

$a=1\iff\operatorname{rank}A=1$。$a=0,1,2$的标准形分别为$u^2-v^2,u^2+0v^2,u^2+v^2$；惯性三元组$(n_+,n_-,n_0)$分别为$(1,1,0),(1,0,1),(2,0,0)$。

## 81. draft-c35-04

内容 SHA256：`c3f4a9686cc9b36121dbdd05c3c9507554e48648df19fe2b45e2cae07cf2726f`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft-codex-repair-v4-final.jsonl，第 4 行；源 SHA256 `cf876d0a55020e12a3585a04513f0247b94ce192e738835d0cb31e1f22d0feac`。

**题干**

用配方法将二次型 $f(x,y,z)=x^2-y^2+2xz+2yz$ 化为标准形，写出可逆线性替换，并求正负惯性指数与秩。

**过程**

先对含 $x$ 的项配方：$x^2+2xz=(x+z)^2-z^2$，于是 $f=(x+z)^2-z^2-y^2+2yz=(x+z)^2-(y^2-2yz+z^2)=(x+z)^2-(y-z)^2$。令 $u=x+z$，$v=y-z$，$w=z$，则标准形为 $u^2-v^2$($w$ 不出现，退化)；反解得线性替换 $x=u-w$，$y=v+w$，$z=w$，系数矩阵 $\begin{pmatrix}1&0&-1\\0&1&1\\0&0&1\end{pmatrix}$ 行列式为 $1$，可逆。正惯性指数 $1$，负惯性指数 $1$，秩 $2$。对应 $C^{\mathsf T}AC=\operatorname{diag}(1,-1,0)$，故惯性三元组为 $(1,1,1)$。不出现的第三变量是一个零方向，不能把零惯性指数写成$0$。

**答案原文**

标准形 $u^2-v^2+0w^2$；$x=u-w,y=v+w,z=w$；$(n_+,n_-,n_0)=(1,1,1)$，秩$2$。

## 82. draft-c35-05

内容 SHA256：`bc9a262bed34edcee1e0c4a5dea0bb3c0b355115bba00061fa0b5b8ef88f1722`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft-codex-repair-v4-final.jsonl，第 5 行；源 SHA256 `cf876d0a55020e12a3585a04513f0247b94ce192e738835d0cb31e1f22d0feac`。

**题干**

判断二次型 $f(x,y,z)=x^2+2y^2+3z^2+2xy$ 与 $g(x,y,z)=2x^2+3y^2+4z^2$ 是否合同，并说明理由；若合同，构造可逆矩阵 $C$ 使 $C^{\mathsf{T}}AC=B$。

**过程**

配方：$f=(x+y)^2+y^2+3z^2$，正惯性指数 $3$，正定；$g=2x^2+3y^2+4z^2$，正惯性指数 $3$，正定。由惯性定理，两者惯性指数相同，故合同(都与 $I_3$ 合同，由合同关系的传递性)。构造：令 $M_f=\begin{pmatrix}1&1&0\\0&1&0\\0&0&\sqrt3\end{pmatrix}$，则 $f=(M_fx)^{\mathsf{T}}(M_fx)$，即 $A=M_f^{\mathsf{T}}M_f$;令 $M_g=\mathrm{diag}(\sqrt2,\sqrt3,2)$，则 $B=M_g^{\mathsf{T}}M_g$。于是 $B=(M_f^{-1}M_g)^{\mathsf{T}}A(M_f^{-1}M_g)$，取 $C=M_f^{-1}M_g=\begin{pmatrix}1&-1&0\\0&1&0\\0&0&\frac{1}{\sqrt3}\end{pmatrix}\begin{pmatrix}\sqrt2&0&0\\0&\sqrt3&0\\0&0&2\end{pmatrix}=\begin{pmatrix}\sqrt2&-\sqrt3&0\\0&\sqrt3&0\\0&0&\frac{2}{\sqrt3}\end{pmatrix}$。验证:$C^{\mathsf{T}}AC=\mathrm{diag}(2,3,4)=B$(逐项相乘核对),且 $\det C=2\sqrt2\neq0$。

**答案原文**

合同(两者均正定,惯性指数 $(3,0,0)$);$C=\begin{pmatrix}\sqrt2&-\sqrt3&0\\0&\sqrt3&0\\0&0&\frac{2}{\sqrt3}\end{pmatrix}$。

## 83. draft-c37-01

内容 SHA256：`de0ef4f41b2615974a5264a7b8013649f76682780588d7b11f6870e5c8b4829d`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft-codex-repair-v4-final.jsonl，第 6 行；源 SHA256 `cf876d0a55020e12a3585a04513f0247b94ce192e738835d0cb31e1f22d0feac`。

**题干**

在 $\mathbb R^3$ 中，求从标准基 $\varepsilon_1,\varepsilon_2,\varepsilon_3$ 到基 $\eta_1=(1,1,0)$，$\eta_2=(0,1,1)$，$\eta_3=(1,0,1)$ 的过渡矩阵，并求向量 $\alpha=(1,2,3)$ 在基 $\eta_1,\eta_2,\eta_3$ 下的坐标。

**过程**

约定基矩阵 $B_\eta=B_\varepsilon P$，$P$的第$j$列为$[\eta_j]_\varepsilon$，故$[v]_\varepsilon=P[v]_\eta$、$[v]_\eta=P^{-1}[v]_\varepsilon$；换基改变坐标，不改变向量$v$。过渡矩阵以新基向量在旧基下的坐标作列：$P=\begin{pmatrix}1&0&1\\1&1&0\\0&1&1\end{pmatrix}$。求 $\alpha$ 的新坐标即解 $P\xi=\alpha$。由增广消元(或直接求逆)得 $P^{-1}=\frac12\begin{pmatrix}1&1&-1\\-1&1&1\\1&-1&1\end{pmatrix}$，故 $\xi=P^{-1}\alpha=\frac12(1+2-3,\,-1+2+3,\,1-2+3)=\frac12(0,4,2)=(0,2,1)$。验证:$0\cdot\eta_1+2\eta_2+1\cdot\eta_3=2(0,1,1)+(1,0,1)=(1,2,3)=\alpha$。

**答案原文**

过渡矩阵 $P=\begin{pmatrix}1&0&1\\1&1&0\\0&1&1\end{pmatrix}$;$\alpha$ 在新基下的坐标为 $(0,2,1)$。

## 84. draft-c37-02

内容 SHA256：`1bcf82e10525eb1df3f25a87a1ef486d791ff07963197111f29b4963d1f3563c`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft-codex-repair-v4-final.jsonl，第 7 行；源 SHA256 `cf876d0a55020e12a3585a04513f0247b94ce192e738835d0cb31e1f22d0feac`。

**题干**

在次数不超过 $2$ 的实系数多项式空间 $V$ 中，求从基 $\{1,x,x^2\}$ 到基 $\{1,\,x-1,\,(x-1)^2\}$ 的过渡矩阵，并求 $p(x)=2x^2+3x+4$ 在新基下的坐标。

**过程**

约定基矩阵 $B_\eta=B_\varepsilon P$，$P$的第$j$列为$[\eta_j]_\varepsilon$，故$[v]_\varepsilon=P[v]_\eta$、$[v]_\eta=P^{-1}[v]_\varepsilon$；换基改变坐标，不改变向量$v$。新基各元素在旧基 $\{1,x,x^2\}$ 下的坐标：$1=(1,0,0)$，$x-1=(-1,1,0)$，$(x-1)^2=x^2-2x+1=(1,-2,1)$。故过渡矩阵 $P=\begin{pmatrix}1&-1&1\\0&1&-2\\0&0&1\end{pmatrix}$。$p$ 在旧基下的坐标为 $(4,3,2)$。解 $P\xi=(4,3,2)^{\mathsf T}$：由回代得 $P^{-1}=\begin{pmatrix}1&1&1\\0&1&2\\0&0&1\end{pmatrix}$，故 $\xi=(4+3+2,\,3+4,\,2)=(9,7,2)$。验证:$9\cdot1+7(x-1)+2(x-1)^2=9+7x-7+2x^2-4x+2=2x^2+3x+4=p(x)$。

**答案原文**

过渡矩阵 $P=\begin{pmatrix}1&-1&1\\0&1&-2\\0&0&1\end{pmatrix}$;$p$ 在新基下的坐标为 $(9,7,2)$。

## 85. draft-c37-03

内容 SHA256：`560e0b6b1964c382f870c248e48a68a68cd4993246160c0883c00b260a3fd47d`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft-codex-repair-v4-final.jsonl，第 8 行；源 SHA256 `cf876d0a55020e12a3585a04513f0247b94ce192e738835d0cb31e1f22d0feac`。

**题干**

在实对称$2\times2$矩阵空间中，取旧基$E_1=\begin{pmatrix}1&0\\0&0\end{pmatrix},E_2=\begin{pmatrix}0&1\\1&0\end{pmatrix},E_3=\begin{pmatrix}0&0\\0&1\end{pmatrix}$；新基$\eta_1=I_2,\eta_2=\operatorname{diag}(1,-1),\eta_3=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$。求过渡矩阵、$T=\begin{pmatrix}3&2\\2&1\end{pmatrix}$的新坐标，并在内积$\langle U,V\rangle=\operatorname{tr}(UV)$下求新基Gram矩阵，核对$\|T\|^2$。

**过程**

约定$B_\eta=B_EP$，即$P$的列是新基在旧基下的坐标。于是$P=\begin{pmatrix}1&1&1\\0&0&1\\1&-1&-1\end{pmatrix}$，$\det P=2\ne0$。旧坐标为$(3,2,1)^{\mathsf T}$，解$P\xi=(3,2,1)^{\mathsf T}$得$\xi=(2,-1,2)^{\mathsf T}$；代回$2\eta_1-\eta_2+2\eta_3=T$。旧基Gram矩阵$G_E=\operatorname{diag}(1,2,1)$，故$G_\eta=P^{\mathsf T}G_EP=\begin{pmatrix}2&0&0\\0&2&2\\0&2&4\end{pmatrix}$。新坐标不能直接用欧氏坐标平方和；实际$\xi^{\mathsf T}G_\eta\xi=8+2-8+16=18$，与$\operatorname{tr}(T^2)=3^2+2\cdot2^2+1^2=18$一致。

**答案原文**

$P=\begin{pmatrix}1&1&1\\0&0&1\\1&-1&-1\end{pmatrix}$，$[T]_\eta=(2,-1,2)^{\mathsf T}$；$G_\eta=\begin{pmatrix}2&0&0\\0&2&2\\0&2&4\end{pmatrix}$，$\|T\|^2=18$。

## 86. draft-c37-04

内容 SHA256：`365b21d7251c400333f9410fc921133b9d82c643113def1c5adaa588111486fc`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft-codex-repair-v4-final.jsonl，第 9 行；源 SHA256 `cf876d0a55020e12a3585a04513f0247b94ce192e738835d0cb31e1f22d0feac`。

**题干**

在 $\mathbb R^2$ 中，设从标准基 $\varepsilon$ 到基 $\eta=\{\eta_1=(1,1),\eta_2=(1,-1)\}$ 的过渡矩阵为 $P$，从 $\eta$ 到基 $\zeta=\{\zeta_1=(2,1),\zeta_2=(1,2)\}$ 的过渡矩阵为 $Q$。求 $P$、$Q$ 与从 $\varepsilon$ 到 $\zeta$ 的过渡矩阵，并验证后者等于 $PQ$；若向量 $\alpha$ 在基 $\zeta$ 下的坐标为 $(1,1)$，求 $\alpha$ 在标准基下的坐标。

**过程**

约定基矩阵 $B_\eta=B_\varepsilon P$，$P$的第$j$列为$[\eta_j]_\varepsilon$，故$[v]_\varepsilon=P[v]_\eta$、$[v]_\eta=P^{-1}[v]_\varepsilon$；换基改变坐标，不改变向量$v$。$P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$。求 $Q$：把 $\zeta_1=(2,1)$ 写成 $\eta$ 的组合，解 $(2,1)=a(1,1)+b(1,-1)$ 得 $a=\frac32,b=\frac12$;$\zeta_2=(1,2)=c(1,1)+d(1,-1)$ 得 $c=\frac32,d=-\frac12$。故 $Q=\begin{pmatrix}\frac32&\frac32\frac12&-\frac12\end{pmatrix}$。于是 $\varepsilon\to\zeta$ 的过渡矩阵 $R=PQ=\begin{pmatrix}1&1\\1&-1\end{pmatrix}\begin{pmatrix}\frac32&\frac32\frac12&-\frac12\end{pmatrix}=\begin{pmatrix}2&1\\1&2\end{pmatrix}$，恰为 $\zeta_1,\zeta_2$ 在标准基下的坐标按列排列，验证正确。$\alpha=1\cdot\zeta_1+1\cdot\zeta_2=(3,3)$。

**答案原文**

$P=\begin{pmatrix}1&1\\1&-1\end{pmatrix}$，$Q=\begin{pmatrix}\frac32&\frac32\frac12&-\frac12\end{pmatrix}$，$\varepsilon\to\zeta$ 的过渡矩阵为 $\begin{pmatrix}2&1\\1&2\end{pmatrix}=PQ$;$\alpha$ 在标准基下为 $(3,3)$。

## 87. draft-c37-05

内容 SHA256：`431d3d2b30fdbacb7e20cac3f38d66c507fd02285a37ffd1bf92723cc73c0fc3`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft-codex-repair-v4-final.jsonl，第 10 行；源 SHA256 `cf876d0a55020e12a3585a04513f0247b94ce192e738835d0cb31e1f22d0feac`。

**题干**

证明 $\{1+x+x^2,\ 1-x+x^2,\ x-x^2\}$ 是次数不超过 $2$ 的多项式空间的一组基，并求 $p(x)=x^2$ 在这组基下的坐标。

**过程**

约定基矩阵 $B_\eta=B_\varepsilon P$，$P$的第$j$列为$[\eta_j]_\varepsilon$，故$[v]_\varepsilon=P[v]_\eta$、$[v]_\eta=P^{-1}[v]_\varepsilon$；换基改变坐标，不改变向量$v$。把三个多项式在基 $\{1,x,x^2\}$ 下的坐标按列排列：$M=\begin{pmatrix}1&1&0\\1&-1&1\\1&1&-1\end{pmatrix}$。计算 $\det M=1\times((-1)\times(-1)-1\times1)-1\times(1\times(-1)-1\times1)+0=0-(-2)=2\neq0$，故三个向量线性无关；空间维数为 $3$，故构成一组基。求 $p=x^2$ 的坐标即解 $M\xi=(0,0,1)^{\mathsf T}$。由伴随矩阵法(或消元)得 $M^{-1}=\begin{pmatrix}0&\frac12&\frac12\\1&-\frac12&-\frac12\\1&0&-1\end{pmatrix}$，故 $\xi=M^{-1}(0,0,1)^{\mathsf T}=(\frac12,-\frac12,-1)$。验证:$\frac12(1+x+x^2)-\frac12(1-x+x^2)-(x-x^2)=(\frac12-\frac12)+(\frac x2+\frac x2-x)+(\frac{x^2}2-\frac{x^2}2+x^2)=x^2$。

**答案原文**

三个多项式线性无关(行列式 $2\neq0$),构成一组基;$p=x^2$ 的坐标为 $(\frac12,-\frac12,-1)$。

## 88. draft-c16-01

内容 SHA256：`cdda6b8e26e3d2190c58638e01fa52484509e90d941bbf978cdc99e90422defc`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft-codex-repair-v4-final.jsonl，第 11 行；源 SHA256 `cf876d0a55020e12a3585a04513f0247b94ce192e738835d0cb31e1f22d0feac`。

**题干**

判断直线 $l_1$：过点 $(1,0,0)$、方向 $(1,1,0)$ 与直线 $l_2$：过点 $(0,1,0)$、方向 $(1,-1,0)$ 的位置关系；若相交，求交点与夹角。

**过程**

参数化 $l_1$:$(1,0,0)+t(1,1,0)$，$l_2$:$(0,1,0)+s(1,-1,0)$。联立 $1+t=s$，$t=1-s$，$0=0$，解得 $t=0,s=1$，交点为 $(1,0,0)$(也在 $l_2$ 上:$(0,1,0)+(1,-1,0)=(1,0,0)$)。方向向量内积 $(1,1,0)\cdot(1,-1,0)=1-1+0=0$，故两直线垂直，夹角为 $\frac\pi2$。

**答案原文**

相交于 $(1,0,0)$,夹角 $\frac\pi2$(方向向量正交)。

## 89. draft-c16-02

内容 SHA256：`f71554dd8b37279af7032825a670e0ea4483e0dbfc43d1d9e02c5c6fb1ed473a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft-codex-repair-v4-final.jsonl，第 12 行；源 SHA256 `cf876d0a55020e12a3585a04513f0247b94ce192e738835d0cb31e1f22d0feac`。

**题干**

求两平行直线 $l_1$：过点 $(1,2,3)$、方向 $(1,1,1)$ 与 $l_2$：过点 $(2,3,3)$、方向 $(1,1,1)$ 之间的距离。

**过程**

记 $v=(1,1,1)$、$\Delta=P_2-P_1=(1,1,0)$。$\Delta\notin\operatorname{span}\{v\}$，两线平行不重合。连接向量写为 $\Delta+\tau v$，距离平方 $\|\Delta+\tau v\|^2=\|v\|^2(\tau+\frac{\Delta\cdot v}{\|v\|^2})^2+\|\Delta\|^2-\frac{(\Delta\cdot v)^2}{\|v\|^2}=3(\tau+\frac23)^2+\frac23$。故$d^2=\frac23$、$d=\frac{\sqrt6}3$。与叉积恒等式 $\|\Delta\times v\|^2=\|\Delta\|^2\|v\|^2-(\Delta\cdot v)^2=2$ 一致。

**答案原文**

距离为 $\frac{\sqrt6}{3}$。

## 90. draft-c16-03

内容 SHA256：`efdace877ccb19173fb1460574ac67b70bbe488ac3e7dc683e35c3df63f2bb97`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft-codex-repair-v4-final.jsonl，第 13 行；源 SHA256 `cf876d0a55020e12a3585a04513f0247b94ce192e738835d0cb31e1f22d0feac`。

**题干**

求异面直线 $l_1$：$x$ 轴 与 $l_2$：过点 $(0,1,1)$、方向 $(0,1,0)$ 的公垂线方程、两个垂足与两直线间的距离。

**过程**

两线点为 $A=(t,0,0)$、$B=(0,1+s,1)$，连接向量 $B-A=(-t,1+s,1)$。公垂线方向与两个方向向量均正交，故平行于 $(0,0,1)$；于是 $t=0,s=-1$，垂足为 $(0,0,0)$、$(0,0,1)$，公垂线为 $\{(0,0,z):z\in\mathbb R\}$。对任意$t,s$，$\|B-A\|^2=t^2+(1+s)^2+1\ge1$，且等号仅在$t=0,s=-1$成立，因此最短距离精确为$1$。

**答案原文**

公垂线为 $z$ 轴 $\{(0,0,z)\}$;垂足 $(0,0,0)$ 与 $(0,0,1)$;距离为 $1$。

## 91. draft-c16-04

内容 SHA256：`f40d7c5b6e1b2a96462b9ee84dcac3ff13803c66a423dfa5740006b07f774c3f`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft-codex-repair-v4-final.jsonl，第 14 行；源 SHA256 `cf876d0a55020e12a3585a04513f0247b94ce192e738835d0cb31e1f22d0feac`。

**题干**

求两条异面直线 $l_1:(t,t,0)$ 与 $l_2:(s,0,1-s)$ 上动点之间距离的最小值(即两直线间的距离)。

**过程**

令 $F(t,s)=(s-t)^2+t^2+(1-s)^2=2t^2-2ts+2s^2-2s+1$。驻点条件 $\partial_tF=4t-2s=0$、$\partial_sF=4s-2t-2=0$ 给出 $(t,s)=(\frac13,\frac23)$。令 $u=t-\frac13,v=s-\frac23$，则 $F=\frac13+2u^2-2uv+2v^2=\frac13+u^2+v^2+(u-v)^2\ge\frac13$；等号当且仅当$u=v=0$。因此唯一全局最小距离为$\sqrt{\frac13}=\frac{\sqrt3}{3}$，在给定参数对处取得。

**答案原文**

最小距离为 $\frac{\sqrt3}{3}$(在 $t=\frac13,s=\frac23$ 处取得)。

## 92. draft-c16-05

内容 SHA256：`494a4083456809ccd0c943ee816f60cb63c58da6d4b47b763e432dd2f54a35d0`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-03/draft-codex-repair-v4-final.jsonl，第 15 行；源 SHA256 `cf876d0a55020e12a3585a04513f0247b94ce192e738835d0cb31e1f22d0feac`。

**题干**

证明两条异面直线有且仅有一条公垂线，并写出公垂线方向与两直线间距离的公式。

**过程**

设 $l_1:P_1+td_1$，$l_2:P_2+sd_2$ 异面，则 $d_1,d_2$ 不平行(否则共面)，故 $n=d_1\times d_2\neq0$，且 $n\perp d_1,d_2$。任何公垂线与 $l_1,l_2$ 都垂直，其方向必平行于 $n$。设公垂线连接 $A=P_1+t_1d_1$ 与 $B=P_2+t_2d_2$，则 $B-A\perp d_1,d_2$，即 $(P_2-P_1+t_2d_2-t_1d_1)\cdot d_1=0$ 且 $\cdot d_2=0$，得关于 $(t_1,t_2)$ 的线性方程组，系数矩阵 $\begin{pmatrix}-|d_1|^2&d_1\cdot d_2\\-d_1\cdot d_2&|d_2|^2\end{pmatrix}$ 的行列式为 $-|d_1|^2|d_2|^2+(d_1\cdot d_2)^2=-|d_1\times d_2|^2\neq0$，故存在唯一解 $(t_1,t_2)$，即公垂线存在且唯一。距离即两垂足间距离：$d=\frac{|(P_2-P_1)\cdot(d_1\times d_2)|}{|d_1\times d_2|}$。令 $r=B-A$。由$r\perp d_1,d_2$知$r=\lambda n$，又$r\cdot n=(P_2-P_1)\cdot n$，故$\|r\|=\frac{|(P_2-P_1)\cdot n|}{\|n\|}$。任意其他点对的连接向量为$r+sd_2-td_1$，且两项正交，因此$\|r+sd_2-td_1\|^2=\|r\|^2+\|sd_2-td_1\|^2\ge\|r\|^2$。$d_1,d_2$线性无关，等号只在$s=t=0$成立，故该连接段确为唯一最短段。

**答案原文**

公垂线唯一,方向为 $n=d_1\times d_2$;距离公式 $d=\frac{|(P_2-P_1)\cdot(d_1\times d_2)|}{|d_1\times d_2|}$(证明见解法)。

## 93. draft-c13-01

内容 SHA256：`8688471fc3cdced5c98527928459fdb333133dd8be4657dd8e59726b38ab5047`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft-codex-repair-v4-final.jsonl，第 1 行；源 SHA256 `49218ed2ea4db10545e5e9796224f589ed2de433dd7a0193aa814ef3645dba0a`。

**题干**

求$\sum_{n=1}^{\infty}\arctan\frac1{n^2+n+1}$的精确和，并给出前$N$项后的精确余项。

**过程**

令$\delta_n=\arctan(n+1)-\arctan n$，有$0<\delta_n<\pi/2$，且$\tan\delta_n=((n+1)-n)/(1+n(n+1))=1/(n^2+n+1)$。由主值范围得$\delta_n=\arctan(1/(n^2+n+1))$，不能只由正切相等而忽略整周差。故$S_N=\arctan(N+1)-\pi/4$；取极限得$S=\pi/4$。余项$R_N=S-S_N=\pi/2-\arctan(N+1)=\arctan(1/(N+1))$，后一等式同样用正数主值范围确定。

**答案原文**

$S=\pi/4$，$R_N=\arctan(1/(N+1))$。

## 94. draft-c13-02

内容 SHA256：`159b399a14fc92ba8fdd9aac3ac1b2f70ab471096f554af079e78caa731102d4`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft-codex-repair-v4-final.jsonl，第 2 行；源 SHA256 `49218ed2ea4db10545e5e9796224f589ed2de433dd7a0193aa814ef3645dba0a`。

**题干**

求级数 $\sum_{n=1}^{\infty}\frac{1}{n(n+1)(n+2)}$ 的和。

**过程**

重组分解：$\frac{1}{n(n+1)(n+2)}=\frac12\left(\frac{1}{n(n+1)}-\frac{1}{(n+1)(n+2)}\right)$(通分核对:分子差为 $(n+2)-n=2$)。前 $N$ 项和 $S_N=\frac12\sum_{n=1}^{N}\left(\frac{1}{n(n+1)}-\frac{1}{(n+1)(n+2)}\right)=\frac12\left(\frac12-\frac{1}{(N+1)(N+2)}\right)$。令 $N\to\infty$ 得 $S=\frac12\cdot\frac12=\frac14$。

**答案原文**

和为 $\frac14$。

## 95. draft-c13-03

内容 SHA256：`243e14ad4b2a93822340ac06c8a9196ec050162f7eed7089ff68841c1ced9ec3`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft-codex-repair-v4-final.jsonl，第 3 行；源 SHA256 `49218ed2ea4db10545e5e9796224f589ed2de433dd7a0193aa814ef3645dba0a`。

**题干**

求级数 $\sum_{n=1}^{\infty}\frac{n}{(n+1)!}$ 的和。

**过程**

重组：$\frac{n}{(n+1)!}=\frac{n+1-1}{(n+1)!}=\frac{1}{n!}-\frac{1}{(n+1)!}$。前 $N$ 项和 $S_N=\sum_{n=1}^{N}\left(\frac{1}{n!}-\frac{1}{(n+1)!}\right)=\frac{1}{1!}-\frac{1}{(N+1)!}=1-\frac{1}{(N+1)!}$。令 $N\to\infty$ 得 $S=1$。

**答案原文**

和为 $1$。

## 96. draft-c13-04

内容 SHA256：`698bc5d64a6ad0190250d67c8a6a903972eda4f40b01f619436c90729028ff0b`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft-codex-repair-v4-final.jsonl，第 4 行；源 SHA256 `49218ed2ea4db10545e5e9796224f589ed2de433dd7a0193aa814ef3645dba0a`。

**题干**

求$\sum_{n=1}^{\infty}(\sqrt{n+2}-2\sqrt{n+1}+\sqrt n)$的和，证明绝对收敛，并给精确余项。

**过程**

令$d_n=\sqrt{n+1}-\sqrt n=1/(\sqrt{n+1}+\sqrt n)$。$d_n>0$且严格递减趋于零，通项为$d_{n+1}-d_n<0$。有限和$S_N=d_{N+1}-d_1=1-\sqrt2+1/(\sqrt{N+2}+\sqrt{N+1})$。因此$S=1-\sqrt2$，且$\sum|d_{n+1}-d_n|=d_1=\sqrt2-1$，绝对收敛。精确尾项$R_N=S-S_N=-1/(\sqrt{N+2}+\sqrt{N+1})$；其绝对值就是对应正分数，未用渐近截断。

**答案原文**

$S=1-\sqrt2$，绝对值级数和$\sqrt2-1$；$R_N=-1/(\sqrt{N+2}+\sqrt{N+1})$。

## 97. draft-c13-05

内容 SHA256：`7f7e667966164f617999c2c7aae691e3e578c406cfc7377baa3bc187fd3c6ef7`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft-codex-repair-v4-final.jsonl，第 5 行；源 SHA256 `49218ed2ea4db10545e5e9796224f589ed2de433dd7a0193aa814ef3645dba0a`。

**题干**

证明不存在有理函数 $R\in\mathbb R(t)$ 使 $\frac1{t^2+1}=R(t)-R(t+1)$。由此说明该级数不能用这类有理函数裂项直接求和。再用精确不等式证明 $S=\sum_{n=1}^{\infty}\frac1{n^2+1}<2$。

**过程**

若存在这样的$R$，把等式视为复有理函数恒等式。把$R$的有限极点按等价关系$a\sim b\iff a-b\in\mathbb Z$分组。在任一等价类内，$R(t)$的留数之和与$R(t+1)$的留数之和相同，因为极点平移$a\mapsto a-1$不改变该类且不改变留数。因此$R(t)-R(t+1)$在每个类中的留数总和必须为$0$。但$1/(t^2+1)$在$t=i,-i$的留数分别为$1/(2i),-1/(2i)$，且$2i\notin\mathbb Z$，两极点属于不同类，各类留数总和均非零，矛盾。故不存在这样的实有理函数$R$。这不排除超出有理函数有限差分框架的其他方法。对于级数，$0<\frac1{n^2+1}<\frac1{n(n-1)}$（$n\ge2$），而$\sum_{n=2}^N\frac1{n(n-1)}=1-\frac1N$。比较判别得收敛，且至少$n=2$的差为$\frac12-\frac15=\frac3{10}>0$，从而$S=\frac12+\sum_{n=2}^{\infty}\frac1{n^2+1}<\frac12+1=\frac32<2$。此外，其和有精确表达式。取$f(x)=\cosh x$在$[-\pi,\pi]$上的周期延拓，其余弦系数为$a_0=\frac{2\sinh\pi}{\pi}$，$a_n=\frac2\pi\int_0^\pi\cosh x\cos(nx)\,dx=\frac{2(-1)^n\sinh\pi}{\pi(1+n^2)}$（$n\ge1$）。周期延拓连续且分段光滑，由傅里叶级数收敛定理，在$x=\pi$有$\cosh\pi=\frac{\sinh\pi}{\pi}+\frac{2\sinh\pi}{\pi}\sum_{n=1}^{\infty}\frac1{1+n^2}$。因此$S=\frac{\pi\coth\pi-1}{2}$，其中$\coth\pi=\cosh\pi/\sinh\pi$。

**答案原文**

不存在上述实有理函数有限差分裂项。精确和为$S=\frac{\pi\coth\pi-1}{2}$，且$0<S<\frac32<2$。

## 98. draft-c18-01

内容 SHA256：`dedb9b6455bc71e99a5bde11147b5faf8f8c8e035dbea7268771cf190bfb31b6`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft-codex-repair-v4-final.jsonl，第 6 行；源 SHA256 `49218ed2ea4db10545e5e9796224f589ed2de433dd7a0193aa814ef3645dba0a`。

**题干**

求空间中到$P=(0,0,0)$与$Q=(2,0,0)$的距离都恰为$1$的全部平面，并给出两点在这些平面上的投影。

**过程**

到原点距离为$1$的任意平面可唯一选朝向写成$ax+by+cz=1$，其中$a^2+b^2+c^2=1$。到$Q$的距离条件为$|2a-1|=1$，故$a=0$或$a=1$。若$a=1$，单位条件给$b=c=0$，平面为$x=1$，两投影均为$(1,0,0)$。若$a=0$，全部平面为$by+cz=1$、$b^2+c^2=1$；法向$n=(0,b,c)$为单位向量，两投影分别为$P+n=(0,b,c)$与$Q+n=(2,b,c)$。逐一验证法向长度与平面方程，距离均为$1$。这两类穷尽上述归一化条件的全部解。

**答案原文**

$x=1$，两投影同为$(1,0,0)$；或$by+cz=1,b^2+c^2=1$，投影分别$(0,b,c)$、$(2,b,c)$。

## 99. draft-c18-02

内容 SHA256：`bb4beaff0b63eb1c8ae03f754d86cdd1ad6840f94b6c29406b7b1094f6af4d06`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft-codex-repair-v4-final.jsonl，第 7 行；源 SHA256 `49218ed2ea4db10545e5e9796224f589ed2de433dd7a0193aa814ef3645dba0a`。

**题干**

求两平行平面 $\pi_1:2x-y+2z=1$ 与 $\pi_2:2x-y+2z=5$ 之间的距离。

**过程**

两平面法向量相同，为平行平面。取 $\pi_1$ 上一点(如 $P_1=(0,-1,0)$:代入 $0-(-1)+0=1$)，点 $P_1$ 到 $\pi_2$ 的有向距离为 $\frac{2\times0-(-1)+2\times0-5}{\sqrt{4+1+4}}=\frac{-4}{3}$，绝对值 $\frac43$ 即两平面间距离。(亦可用公式 $\frac{|d_1-d_2|}{\sqrt{a^2+b^2+c^2}}=\frac{|1-5|}{3}=\frac43$。)

**答案原文**

距离为 $\frac43$。

## 100. draft-c18-03

内容 SHA256：`2fae1159a910f5e288b210768932a75dcc6556f866ea3fb4507cac9e7e550b34`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft-codex-repair-v4-final.jsonl，第 8 行；源 SHA256 `49218ed2ea4db10545e5e9796224f589ed2de433dd7a0193aa814ef3645dba0a`。

**题干**

求过点 $P(1,2,3)$ 且垂直于方向 $v=(2,1,-1)$ 的平面方程；并求该平面与过原点、方向为 $v$ 的直线的交点。

**过程**

以 $v=(2,1,-1)$ 为法向量、过 $P(1,2,3)$ 的平面为 $2(x-1)+(y-2)-(z-3)=0$，即 $2x+y-z-1=0$。直线参数化 $(2t,t,-t)$，代入平面方程：$4t+t+t-1=0$，得 $6t-1=0$，$t=\frac16$，交点为 $(\frac13,\frac16,-\frac16)$。验证:该点满足 $2x+y-z-1=\frac23+\frac16+\frac16-1=0$。

**答案原文**

平面 $2x+y-z-1=0$;交点为 $(\frac13,\frac16,-\frac16)$。

## 101. draft-c18-04

内容 SHA256：`aa7957e5c86e1d22714abf87e16bfdabd70d0a4f342859b0ba579dde6b4a04a0`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft-codex-repair-v4-final.jsonl，第 9 行；源 SHA256 `49218ed2ea4db10545e5e9796224f589ed2de433dd7a0193aa814ef3645dba0a`。

**题干**

设$P=(1,2,3)$，平面$\pi:x+y+z=0$。在加权距离$d_W(P,X)^2=(X-P)^{\mathsf T}W(X-P)$、$W=\operatorname{diag}(1,2,3)$下求唯一最近点与距离，并证明全局唯一性。

**过程**

令$n=(1,1,1)^{\mathsf T}$，$n^{\mathsf T}W^{-1}n=1+1/2+1/3=11/6$。置$\lambda=(n\cdot P)/(n^{\mathsf T}W^{-1}n)=36/11$，$Q=P-\lambda W^{-1}n=(-25/11,4/11,21/11)$，其坐标和为零。对任意$X\in\pi$，$(P-Q)^{\mathsf T}W(X-Q)=\lambda n\cdot(X-Q)=0$。所以$d_W(P,X)^2=d_W(P,Q)^2+(X-Q)^{\mathsf T}W(X-Q)$；$W$正定，等号当且仅当$X=Q$。这证明全局最近性与唯一性。最小平方距离为$(n\cdot P)^2/(n^{\mathsf T}W^{-1}n)=216/11$，距离为$\sqrt{216/11}=6\sqrt{66}/11$。加权法向是$W^{-1}n$，不能错误套用欧氏投影移动方向$n$。

**答案原文**

$Q=(-25/11,4/11,21/11)$，$d_W(P,\pi)^2=216/11$，$d_W(P,\pi)=6\sqrt{66}/11$。

## 102. draft-c18-05

内容 SHA256：`3d26985b017e3abfe479f75f9403981449b60d41a6c3cdca8c3bc4428641bbab`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft-codex-repair-v4-final.jsonl，第 10 行；源 SHA256 `49218ed2ea4db10545e5e9796224f589ed2de433dd7a0193aa814ef3645dba0a`。

**题干**

证明空间中任意一点$P$到平面$\pi=\{X:n\cdot X=c\}$（$n\ne0$）的最近点存在且唯一，并推导正交投影及距离公式。

**过程**

设$\pi=\{X:n\cdot X=c\}$、$n\ne0$。定义 $\lambda=\frac{n\cdot P-c}{\|n\|^2}$、$Q=P-\lambda n$。则$n\cdot Q=c$，故$Q\in\pi$。对任意$X\in\pi$，$n\cdot(X-Q)=0$，即$X-Q\in\ker(n^{\mathsf T})$；且$(P-Q)\cdot(X-Q)=\lambda n\cdot(X-Q)=0$。因此$\|P-X\|^2=\|P-Q\|^2+\|X-Q\|^2\ge\|P-Q\|^2$，等号当且仅当$X=Q$。这同时证明存在、垂直性、最近性和唯一性。投影公式 $Q=P-\frac{n\cdot P-c}{\|n\|^2}n$，距离 $d(P,\pi)=\frac{|n\cdot P-c|}{\|n\|}$。两个平面上点的差向量属于线性空间$\ker(n^{\mathsf T})$，不能说属于一般仿射平面$\pi$。

**答案原文**

$Q=P-\frac{n\cdot P-c}{\|n\|^2}n$是唯一最近点；$d(P,\pi)=\frac{|n\cdot P-c|}{\|n\|}$。

## 103. draft-c30-01

内容 SHA256：`1e0fa22d095efa7082661887f563ad09c012999faacff92685a2550fa0306fa6`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft-codex-repair-v4-final.jsonl，第 11 行；源 SHA256 `49218ed2ea4db10545e5e9796224f589ed2de433dd7a0193aa814ef3645dba0a`。

**题干**

求次数不超过$5$、在$x=1$至少有三重零点、在$x=2$至少有二重零点且$f(0)=1$的全部实多项式，并写成$x-1$的幂。

**过程**

零点重数给$(x-1)^3(x-2)^2\mid f$。由次数上界，$f=c(x-1)^3(x-2)^2$；$f(0)=1$给$-4c=1$，即$c=-1/4$。令$u=x-1$，则$f=-u^3(u-1)^2/4=-u^5/4+u^4/2-u^3/4$。因为$c\ne0$且两个因子互素，重数分别恰为$3$与$2$。所有条件均验证，且常数被唯一确定，故解唯一。

**答案原文**

$f=-\frac14(x-1)^3(x-2)^2=-\frac14(x-1)^5+\frac12(x-1)^4-\frac14(x-1)^3$，唯一。

## 104. draft-c30-02

内容 SHA256：`5248a776f902ca3020713a2f2e933b98ba9b69181057b07997efa37b26c235b8`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft-codex-repair-v4-final.jsonl，第 12 行；源 SHA256 `49218ed2ea4db10545e5e9796224f589ed2de433dd7a0193aa814ef3645dba0a`。

**题干**

对$f(x)=x^4-4x^3+7x^2-6x+3$，求所有使$f(h+t)=f(h-t)$对每个实数$t$成立的实数$h$，并给关于该中心的展开。

**过程**

$f(h+t)$的三次项系数为$4h-4$。若关于$t$为偶函数，该系数必为零，故$h=1$是唯一可能值。直接展开$f(1+t)=t^4+t^2+1$，所有奇次项为零，确满足$f(1+t)=f(1-t)$。因此唯一中心为$1$，平移展开$f(x)=(x-1)^4+(x-1)^2+1$。必要条件与代入验证共同给全体解，不能只检查局部导数为零而漏掉其他奇次项。

**答案原文**

唯一中心$h=1$；$f(x)=(x-1)^4+(x-1)^2+1$。

## 105. draft-c30-03

内容 SHA256：`2f03e9adb82b6128fd9df305d0f5527bfd3d6e2601287ed3c6ea4a179bd53b34`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft-codex-repair-v4-final.jsonl，第 13 行；源 SHA256 `49218ed2ea4db10545e5e9796224f589ed2de433dd7a0193aa814ef3645dba0a`。

**题干**

在次数不超过$3$的实多项式空间上定义$\Delta f(x)=f(x+1)-f(x)$。证明$\Delta^4=0$但$\Delta^3\ne0$，并求满足$\Delta f=3x^2+5x+2$、$f(0)=2$的全部$f$。

**过程**

若$f$非恒定且次数为$m$，首项系数为$c\ne0$，二项式展开给$\Delta f$的次数恰为$m-1$，首项系数为$mc$。因此在该四维空间上$\Delta^4=0$；且$\Delta^3(x^3)=6\ne0$，指数恰为$4$。设$f=ax^3+bx^2+cx+d$，则$\Delta f=3ax^2+(3a+2b)x+(a+b+c)$。与目标比较得$a=1,b=1,c=0$，而$f(0)=2$给$d=2$。故$f=x^3+x^2+2$。若两个解存在，其差被$\Delta$消去；降阶结论说明差为常数，归一化又给常数为零，故唯一。

**答案原文**

$\Delta^4=0,\Delta^3(x^3)=6$；唯一$f=x^3+x^2+2$。

## 106. draft-c30-04

内容 SHA256：`8f584ac40afedab8ccc8389a710ca836ea66e78b021854c0a64f40aec4701e63`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft-codex-repair-v4-final.jsonl，第 14 行；源 SHA256 `49218ed2ea4db10545e5e9796224f589ed2de433dd7a0193aa814ef3645dba0a`。

**题干**

已知多项式 $f$ 在 $x=1$ 处的展开为 $f=2+3(x-1)+(x-1)^2-(x-1)^3$。求 $f$ 按 $x$ 的幂展开的标准形式，并求 $f(1)$、$f'(1)$、$f''(1)$。

**过程**

令 $y=x-1$，$f=2+3y+y^2-y^3$，回代 $y=x-1$ 并展开:$2+3(x-1)+(x-1)^2-(x-1)^3=2+3x-3+(x^2-2x+1)-(x^3-3x^2+3x-1)=-x^3+4x^2-2x+1$。由展开式直接读系数:$f(1)=2$，$f'(1)=3$，$f''(1)/2!=1$ 即 $f''(1)=2$。验证:对标准形式求导 $f'(x)=-3x^2+8x-2$，$f'(1)=3$;$f''(x)=-6x+8$，$f''(1)=2$，一致。

**答案原文**

$f=-x^3+4x^2-2x+1$;$f(1)=2$，$f'(1)=3$，$f''(1)=2$。

## 107. draft-c30-05

内容 SHA256：`ef1e349580dc5d6477b43772edc0ef14014558e85b70d02c79dbc34120ae4e4e`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-04/draft-codex-repair-v4-final.jsonl，第 15 行；源 SHA256 `49218ed2ea4db10545e5e9796224f589ed2de433dd7a0193aa814ef3645dba0a`。

**题干**

证明非恒定实多项式没有非零实周期。再求全部满足$f(x+1)+f(x-1)=2f(x)$对所有实数$x$成立的实多项式。

**过程**

设非恒定$f$次数为$m\ge1$、首项系数$c\ne0$。若$h\ne0$，有限展开给$f(x+h)-f(x)$的$x^{m-1}$系数为$cmh\ne0$，故该差不可能为零多项式，非零周期不存在。对第二个恒等式，若$m\ge2$，$f(x+1)+f(x-1)-2f(x)$的次数恰为$m-2$，首项系数为$cm(m-1)\ne0$，故不可能恒为零。次数至多$1$的多项式$f(x)=ax+b$直接代入均满足。因而全体解为任意实$a,b$的仿射多项式，包含常数与零多项式。以上比较的是有限多项式系数，不使用渐近近似。

**答案原文**

非恒定实多项式无非零实周期；第二个方程的全部解为$f(x)=ax+b$（$a,b\in\mathbb R$）。

## 108. draft-c21-01

内容 SHA256：`c7500b918062a82efd3cbb00faf3a3247b74b92abebc154259fad7fa17ffce5f`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-05/draft-codex-repair-v6.jsonl，第 1 行；源 SHA256 `fe34e9cd7dc872f85037666d1ec5a7530f9fd2f2721814a2ee34b048b1a49063`。

**题干**

求直线 $l:(t,t,2t)$ 与旋转抛物面 $z=x^2+y^2$ 的交点。

**过程**

把参数式代入曲面方程:$2t=t^2+t^2=2t^2$,即 $t(t-1)=0$,解得 $t=0$ 或 $t=1$。$t=0$ 对应点 $(0,0,0)$;$t=1$ 对应点 $(1,1,2)$。验证:$(0,0,0)$ 满足 $0=0$;$(1,1,2)$ 满足 $2=1+1$。

**答案原文**

两个交点:$(0,0,0)$ 与 $(1,1,2)$。

## 109. draft-c21-02

内容 SHA256：`78c7616e3ddec28303444a96446e5c0ee65023b40fbc9bb7fe6fc8b7831ee729`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-05/draft-codex-repair-v6.jsonl，第 2 行；源 SHA256 `fe34e9cd7dc872f85037666d1ec5a7530f9fd2f2721814a2ee34b048b1a49063`。

**题干**

设直线 $l_a=\{(a,0,t):t\in\mathbb R\}$。求使 $l_a$ 与球面 $x^2+y^2+z^2=4$ 相交于两点、相切、无交点的 $a$ 的取值范围，并求相切时的切点。

**过程**

代入$x=a,y=0$得$t^2=4-a^2$。若$|a|<2$，两交点为$(a,0,\sqrt{4-a^2})$与$(a,0,-\sqrt{4-a^2})$。若$a=2$，仅有切点$(2,0,0)$；若$a=-2$，仅有切点$(-2,0,0)$。两种相切情形分别对应不同直线，每一条相切直线只有一个切点。此时直线方向$(0,0,1)$与球面法向$(a,0,0)$正交，确为相切。若$|a|>2$，无实根，故无交点。

**答案原文**

$|a|<2$时有两个交点$(a,0,\pm\sqrt{4-a^2})$；$a=2$时切点$(2,0,0)$，$a=-2$时切点$(-2,0,0)$；$|a|>2$时无交点。

## 110. draft-c21-03

内容 SHA256：`ecf6e0f3fb1c9b1909b6c0e1711ee7afd26a44a61bfbe3b1c13a70f0defabbfe`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-05/draft-codex-repair-v6.jsonl，第 3 行；源 SHA256 `fe34e9cd7dc872f85037666d1ec5a7530f9fd2f2721814a2ee34b048b1a49063`。

**题干**

求直线 $l:(1+t,2t,t)$ 与双曲抛物面 $z=xy$ 的交点。

**过程**

代入:$z=t$,而 $xy=(1+t)\cdot2t=2t+2t^2$,故 $t=2t+2t^2$,即 $t(2t+1)=0$,解得 $t=0$ 或 $t=-\frac12$。$t=0$ 对应点 $(1,0,0)$;$t=-\frac12$ 对应点 $(\frac12,-1,-\frac12)$。验证:$t=0$ 时 $z=0=1\cdot0$;$t=-\frac12$ 时 $z=-\frac12=\frac12\times(-1)$。

**答案原文**

两个交点:$(1,0,0)$ 与 $(\frac12,-1,-\frac12)$。

## 111. draft-c21-04

内容 SHA256：`23f631c1d9e81d5f99fbc021c2db367176b7c500bb2059ec68c2fbadcac934a7`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-05/draft-codex-repair-v6.jsonl，第 4 行；源 SHA256 `fe34e9cd7dc872f85037666d1ec5a7530f9fd2f2721814a2ee34b048b1a49063`。

**题干**

在曲面$xy=1$上，讨论直线$l_{a,b}(t)=(t,at+b,t)$（$a,b\in\mathbb R$）的全部交点情况。区分无交点、一个或两个交点；在二次方程重根时证明直线与曲面相切。

**过程**

代入曲面得到$at^2+bt-1=0$。若$a=0,b=0$，方程无解；若$a=0,b\ne0$，唯一$t=1/b$，交点为$(1/b,b,1/b)$。若$a\ne0$，令$\Delta=b^2+4a$：当$\Delta>0$时有两个参数$t_{\pm}=(-b\pm\sqrt\Delta)/(2a)$；当$\Delta<0$时无实交点；当$\Delta=0$时唯一$t_0=-b/(2a)$。各点均为$(t,at+b,t)$。曲面梯度为$(y,x,0)$，在$xy=1$上永不为零。在重根交点，梯度与方向$(1,a,1)$内积为$2at_0+b=0$，故方向位于切平面；直线不是曲面上的整条直线，因为代入所得多项式常数项为$-1$。因此重根情形确为相切。直线参数由第一坐标唯一确定，故不同参数给不同交点，以上分类穷尽。

**答案原文**

$a=b=0$无交点；$a=0,b\ne0$一个交点$(1/b,b,1/b)$；$a\ne0$按$\Delta=b^2+4a$的正、零、负分别为两个交点、一个切点、无交点，参数$t_{\pm}=(-b\pm\sqrt\Delta)/(2a)$。

## 112. draft-c21-05

内容 SHA256：`96d874df5c19af08cb076acebf945ef5e69adf4288d11aebfc247f207ea809c1`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-05/draft-codex-repair-v6.jsonl，第 5 行；源 SHA256 `fe34e9cd7dc872f85037666d1ec5a7530f9fd2f2721814a2ee34b048b1a49063`。

**题干**

设直线 $l_m$ 过点 $(0,0,1)$ 且方向向量为 $(1,1,m)$。证明无论 $m$ 取何值,$l_m$ 与旋转抛物面 $z=x^2+y^2$ 都恰有两个交点,并说明理由。

**过程**

参数化$l_m:(t,t,1+mt)$，其中$m\in\mathbb R$。代入曲面得$2t^2-mt-1=0$。判别式$\Delta(m)=m^2+8\ge8>0$，因此有两个不同实根$t_\pm=(m\pm\sqrt{m^2+8})/4$，交点为$(t_\pm,t_\pm,1+mt_\pm)$。参数化的第一坐标为$t$，故不同参数对应不同空间点，恰有两个交点。也可令$F_m(t)=2t^2-mt-1$，则$F_m(0)=-1<0$、$F_m(t)\to+\infty$（$t\to\pm\infty$），说明两侧各有一交点。判别式的数值依赖$m$；独立于$m$的是其恒正性和交点个数。该结论仅针对给定方向$(1,1,m)$，不能推广到过该点的任意方向，例如竖直线仅与抛物面相交一次。

**答案原文**

对所有$m\in\mathbb R$，恰有两个交点$(t_\pm,t_\pm,1+mt_\pm)$，其中$t_\pm=\frac{m\pm\sqrt{m^2+8}}4$；原因是$\Delta(m)=m^2+8\ge8>0$。

## 113. draft-c28-01

内容 SHA256：`fd391c361a94c8927b61ea19a387c3abf99a1af0a25f887237c0f168958bd0dd`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-05/draft-codex-repair-v6.jsonl，第 6 行；源 SHA256 `fe34e9cd7dc872f85037666d1ec5a7530f9fd2f2721814a2ee34b048b1a49063`。

**题干**

按顺序连接$A=(0,0),B=(4,0),C=(4,3),D=(2,1),E=(0,3)$形成简单多边形。用行列式计算其有向面积和普通面积，并说明以$A$为顶点的三角形扇分解为什么必须保留符号。

**过程**

各边只在相邻顶点相交；在凹顶点$D$有$\det(D-C,E-D)=-8<0$，其余非平角顶点转向为正。鞋带公式的连续行列式为$0,12,-2,6,0$，和为$16$，故有向面积$8>0$、普通面积为$8$，边界方向为逆时针。扇分解$ABC,ACD,ADE$的有向面积分别为$6,-1,3$，相加为$8$；若取每项绝对值，则得到$10$，错误地把凹口重叠区域算入。独立检验：外矩形面积为$4\cdot3=12$，上方被挖去的三角形$CDE$底为$4$、高为$2$、面积$4$，所以多边形面积为$12-4=8$。负号是凹多边形扇分解的抵消项。

**答案原文**

有向面积与普通面积均为$8$；有向三角形扇面积为$6,-1,3$，其和$8$，绝对值逐项相加所得$10$不正确。

## 114. draft-c28-02

内容 SHA256：`0c40099a728b33a4eeafc9123ed5f1b81fd83d78170ec1ac5a5ca074d36118c9`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-05/draft-codex-repair-v6.jsonl，第 7 行；源 SHA256 `fe34e9cd7dc872f85037666d1ec5a7530f9fd2f2721814a2ee34b048b1a49063`。

**题干**

设$u=(1,-1,2)^{\mathsf T}$、$v=(2,1,1)^{\mathsf T}$，$A_t=I+tuv^{\mathsf T}$。求该变换对单位立方体的体积及取向的影响。对奇异参数，证明$A_t$是投影，并求其核与像。

**过程**

由行列式对列的多线性，$I+tuv^{\mathsf T}$展开中选两列以上来自$u$的项均为零；只选第$j$列的项为$tv_ju_j$。故$\det A_t=1+t\sum_jv_ju_j=1+3t$。普通体积为$|1+3t|$；$t>-1/3$保取向、$t<-1/3$反取向。当$t=-1/3$时$P=I-uv^{\mathsf T}/3$，因为$v^{\mathsf T}u=3$，有$P^2=I-2uv^{\mathsf T}/3+u(v^{\mathsf T}u)v^{\mathsf T}/9=P$。由$Pu=0$及$Px=0\Rightarrow x=u(v^{\mathsf T}x)/3$得$\ker P=\operatorname{span}\{u\}$。又$v^{\mathsf T}P=0$，而若$v^{\mathsf T}x=0$则$Px=x$，故$\operatorname{im}P=\{(x,y,z):2x+y+z=0\}$，秩为$2$。立方体在该参数下压入一个平面，三维体积为零。

**答案原文**

$\det A_t=1+3t$，体积$|1+3t|$；奇异参数$t=-1/3$，此时$P^2=P$、$\ker P=\operatorname{span}\{(1,-1,2)\}$、$\operatorname{im}P=\{2x+y+z=0\}$、秩$2$。

## 115. draft-c28-03

内容 SHA256：`0567f0f972861ed2e109ae04e3167f0e0ab356ac9eba504fc6766e114e9c1e10`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-05/draft-codex-repair-v6.jsonl，第 8 行；源 SHA256 `fe34e9cd7dc872f85037666d1ec5a7530f9fd2f2721814a2ee34b048b1a49063`。

**题干**

线性变换 $T(x)=Ax$，其中 $A=\begin{pmatrix}1&1&1\\0&2&1\\0&0&3\end{pmatrix}$。求单位立方体在 $T$ 下的像(一个平行六面体)的体积；并求 $T^{-1}$ 对应的体积缩放因子。

**过程**

线性变换把体积放大 $|\det A|$ 倍。$A$ 为上三角矩阵,$\det A=1\times2\times3=6$,故像的体积为 $1\times6=6$。$T^{-1}$ 的矩阵为 $A^{-1}$,$\det(A^{-1})=\frac{1}{\det A}=\frac16$,故其体积缩放因子为 $\frac16$。

**答案原文**

像的体积为 $6$;$T^{-1}$ 的体积缩放因子为 $\frac16$。

## 116. draft-c28-04

内容 SHA256：`2175d35c259696d51d5fcc73b934f80b6b469f93a26ec75b1635815c72e8f8ee`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-05/draft-codex-repair-v6.jsonl，第 9 行；源 SHA256 `fe34e9cd7dc872f85037666d1ec5a7530f9fd2f2721814a2ee34b048b1a49063`。

**题干**

在$\mathbb R^4$中，$a=(1,0,1,0)$、$b=(0,1,0,1)$、$c=(1,1,0,0)$生成三维平行多面体。用Gram行列式求其三维体积，并用正交分解独立验证；说明为什么不能把四维坐标直接拼成三阶方阵取行列式。

**过程**

令$U$为以$a,b,c$为列的$4\times3$矩阵。Gram矩阵$G=U^{\mathsf T}U=\begin{pmatrix}2&0&1\\0&2&1\\1&1&2\end{pmatrix}$，$\det G=4$，体积$V=\sqrt{\det G}=2$。公式来源：满列秩时作薄QR分解$U=QR$、$Q^{\mathsf T}Q=I$，则$G=R^{\mathsf T}R$；各正交高度乘积为$|\det R|=\sqrt{\det G}$。列相关时体积与Gram行列式均为零。独立检验：$a\perp b$且两长度均为$\sqrt2$；$c_{\perp}=c-a/2-b/2=(1/2,1/2,-1/2,-1/2)$与$a,b$正交且长度为$1$。底面积$2$、高$1$，故体积为$2$。原坐标矩阵是矩形，不能直接取其行列式；任意丢弃一维会改变度量与体积。

**答案原文**

$G=\begin{pmatrix}2&0&1\\0&2&1\\1&1&2\end{pmatrix}$，$\det G=4$，三维体积$V=2$；正交高度为$1$，底面积为$2$。

## 117. draft-c28-05

内容 SHA256：`044bef1c5d24d6acd9fd6b8119e014c6ec9fbee800196b6ac6c71d235814ffd2`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-05/draft-codex-repair-v6.jsonl，第 10 行；源 SHA256 `fe34e9cd7dc872f85037666d1ec5a7530f9fd2f2721814a2ee34b048b1a49063`。

**题干**

证明三阶行列式的绝对值等于其三个行向量张成的平行六面体的体积。

**过程**

设矩阵$A$的行向量为$a,b,c\in\mathbb R^3$。直接按坐标展开得$\det A=a\cdot(b\times c)$。若$b\times c=0$，底面积为零，平行六面体退化，体积与行列式均为零。若$b\times c\ne0$，底面积为$B=\|b\times c\|$，单位法向为$\nu=(b\times c)/B$，两平行底面之间的距离为$h=|a\cdot\nu|$，包括$a=0$或共面时$h=0$。因此$V=Bh=\|b\times c\|\,|a\cdot\nu|=|a\cdot(b\times c)|=|\det A|$。非退化时，$\det A>0$对应右手定向，$\det A<0$对应左手定向；退化时不定义右手或左手三维基定向。

**答案原文**

$|\det A|=|a\cdot(b\times c)|=$ 底面积 $\times$ 高 $=$ 平行六面体体积(证明见解法)。

## 118. draft-c31-01

内容 SHA256：`501379ecfb770c63905e99de8b4aed0c257102d93b37334ddf8c15adf69f824b`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-05/draft-codex-repair-v6.jsonl，第 11 行；源 SHA256 `fe34e9cd7dc872f85037666d1ec5a7530f9fd2f2721814a2ee34b048b1a49063`。

**题干**

用克拉默法则解线性方程组 $\begin{cases}x+y+z=6\\ x-y+z=2\\ x+y-z=0\end{cases}$。

**过程**

系数行列式 $D=\begin{vmatrix}1&1&1\\1&-1&1\\1&1&-1\end{vmatrix}=1\times((-1)\times(-1)-1\times1)-1\times(1\times(-1)-1\times1)+1\times(1\times1-(-1)\times1)=0+2+2=4$。$D_x=\begin{vmatrix}6&1&1\\2&-1&1\\0&1&-1\end{vmatrix}=6\times0-1\times(-2)+1\times2=4$,$x=\frac{D_x}{D}=1$。$D_y=\begin{vmatrix}1&6&1\\1&2&1\\1&0&-1\end{vmatrix}=1\times(-2)-6\times(-2)+1\times(-2)=8$,$y=\frac{D_y}{D}=2$。$D_z=\begin{vmatrix}1&1&6\\1&-1&2\\1&1&0\end{vmatrix}=1\times(-2)-1\times(-2)+6\times2=12$,$z=\frac{D_z}{D}=3$。验证:$1+2+3=6$,$1-2+3=2$,$1+2-3=0$。

**答案原文**

$x=1$,$y=2$,$z=3$。

## 119. draft-c31-02

内容 SHA256：`83a46473f53e5cf79830d37b03dcb27fbd4f74f899aa8e873c5a67bfa64c593e`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-05/draft-codex-repair-v6.jsonl，第 12 行；源 SHA256 `fe34e9cd7dc872f85037666d1ec5a7530f9fd2f2721814a2ee34b048b1a49063`。

**题干**

用克拉默法则讨论方程组 $\begin{cases}ax+y=1\\ x+ay=1\end{cases}$ 的解随参数 $a$ 的变化;唯一解时给出解,奇异时说明无解或无穷多解。

**过程**

系数行列式 $D=a^2-1=(a-1)(a+1)$。当 $a\neq\pm1$ 时,$D_x=\begin{vmatrix}1&1\\1&a\end{vmatrix}=a-1$,$D_y=\begin{vmatrix}a&1\\1&1\end{vmatrix}=a-1$,故唯一解 $x=y=\frac{a-1}{a^2-1}=\frac{1}{a+1}$。当 $a=1$ 时,两个方程都化为 $x+y=1$,同一条直线,无穷多解。当 $a=-1$ 时,方程为 $-x+y=1$ 与 $x-y=1$,两者相加得 $0=2$,矛盾,无解。

**答案原文**

$a\neq\pm1$ 时唯一解 $x=y=\frac{1}{a+1}$;$a=1$ 时无穷多解($x+y=1$);$a=-1$ 时无解。

## 120. draft-c31-03

内容 SHA256：`42f7d7ef7a10891825719f741c4f60b8b594434a1a10f57d086925288fbebf77`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-05/draft-codex-repair-v6.jsonl，第 13 行；源 SHA256 `fe34e9cd7dc872f85037666d1ec5a7530f9fd2f2721814a2ee34b048b1a49063`。

**题干**

用克拉默法则求方程组 $\begin{cases}x+y+z=1\\ x+y+2z=2\\ x+2y+az=3\end{cases}$ 的解，并说明解与参数 $a$ 的关系。

**过程**

系数行列式 $D=\begin{vmatrix}1&1&1\\1&1&2\\1&2&a\end{vmatrix}=1\times(a-4)-1\times(a-2)+1\times(2-1)=-1$,与 $a$ 无关且非零,故对一切 $a$ 都有唯一解。$D_x=\begin{vmatrix}1&1&1\\2&1&2\\3&2&a\end{vmatrix}=1\times(a-4)-1\times(2a-6)+1\times(4-3)=-a+3$;$D_y=\begin{vmatrix}1&1&1\\1&2&2\\1&3&a\end{vmatrix}=1\times(2a-6)-1\times(a-2)+1\times(3-2)=a-3$;$D_z=\begin{vmatrix}1&1&1\\1&1&2\\1&2&3\end{vmatrix}=1\times(3-4)-1\times(3-2)+1\times(2-1)=-1$。故 $x=\frac{-a+3}{-1}=a-3$,$y=\frac{a-3}{-1}=3-a$,$z=\frac{-1}{-1}=1$。验证:$x+y+z=(a-3)+(3-a)+1=1$;$x+y+2z=0+2=2$;$x+2y+az=(a-3)+2(3-a)+a=3$。

**答案原文**

$D=-1$ 与 $a$ 无关,对一切 $a$ 有唯一解 $x=a-3$,$y=3-a$,$z=1$。

## 121. draft-c31-04

内容 SHA256：`a94194a0c9f5a8366c1a7a5359083b2eff6fafe232a8341f28a02b53fca1c0ff`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-05/draft-codex-repair-v6.jsonl，第 14 行；源 SHA256 `fe34e9cd7dc872f85037666d1ec5a7530f9fd2f2721814a2ee34b048b1a49063`。

**题干**

用克拉默法则解方程组 $\begin{cases}kx+y=1\\ x+ky=k\end{cases}$($k$ 为参数),并讨论奇异情形($D=0$)时的解。

**过程**

$D=k^2-1=(k-1)(k+1)$。当 $k\neq\pm1$ 时,$D_x=\begin{vmatrix}1&1\\k&k\end{vmatrix}=k-k=0$,$D_y=\begin{vmatrix}k&1\\1&k\end{vmatrix}=k^2-1$,故唯一解 $x=\frac{0}{D}=0$,$y=\frac{D}{D}=1$。当 $k=1$ 时,两方程均为 $x+y=1$,无穷多解。当 $k=-1$ 时,方程为 $-x+y=1$ 与 $x-y=-1$,后者乘以 $-1$ 恰为前者,仍是同一条直线,无穷多解。注意:本题两个奇异值均落在无穷多解分支,与常见的「一个奇异值无解、另一个无穷多解」的例子不同;克拉默法则仅在 $D\neq0$ 时适用,$D=0$ 时必须改用初等变换/秩判断。

**答案原文**

$k\neq\pm1$ 时唯一解 $x=0,y=1$;$k=1$ 与 $k=-1$ 时均有无穷多解(两方程退化为同一直线)。

## 122. draft-c31-05

内容 SHA256：`9683dcbdcf0ba72157e7dcdfb0d355c1285b5520b9cbe4f37c35122b18719ddb`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-05/draft-codex-repair-v6.jsonl，第 15 行；源 SHA256 `fe34e9cd7dc872f85037666d1ec5a7530f9fd2f2721814a2ee34b048b1a49063`。

**题干**

证明:若 $n$ 阶系数矩阵 $A$ 的行列式 $D=\det A\neq0$,则线性方程组 $AX=b$ 有唯一解,且解由克拉默公式给出:$x_j=\frac{D_j}{D}$,其中 $D_j$ 是把 $A$ 的第 $j$ 列换成 $b$ 所得的行列式。

**过程**

记 $A_{ij}$ 为代数余子式,伴随矩阵 $\mathrm{adj}(A)=(A_{ji})$。由行列式按行展开,$(A\,\mathrm{adj}(A))_{ij}=\sum_{k=1}^{n}a_{ik}A_{jk}=\begin{cases}\det A,&i=j\\0,&i\neq j\end{cases}$(异行展开为零),即 $A\,\mathrm{adj}(A)=D\,I$。因 $D\neq0$,$A^{-1}=\frac{1}{D}\mathrm{adj}(A)$ 存在,故 $AX=b$ 有唯一解 $X=A^{-1}b=\frac{1}{D}\mathrm{adj}(A)b$。第 $j$ 个分量 $x_j=\frac{1}{D}\sum_{i=1}^{n}b_iA_{ij}$,而 $\sum_{i=1}^{n}b_iA_{ij}$ 恰是按第 $j$ 列展开的、第 $j$ 列为 $b$ 的行列式 $D_j$,故 $x_j=\frac{D_j}{D}$。

**答案原文**

证明见解法;核心:$A\,\mathrm{adj}(A)=D\,I$(按行展开+异行展开为零),$D\neq0$ 时 $X=\frac{1}{D}\mathrm{adj}(A)b$,第 $j$ 分量为 $D_j/D$。

## 123. draft-c03-01

内容 SHA256：`1674a0569d8152ac99341791d3a26d01977797ceeef145fdaacbffea8611c90e`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-06/draft-codex-repair-v4-final.jsonl，第 1 行；源 SHA256 `a1e5cdea755498453a9ff3081cb4eb5fc557816c9ab36434f214afc2be6bd04c`。

**题干**

求二重积分 $\iint_D xy\,dxdy$，其中 $D=[0,1]\times[0,2]$。

**过程**

矩形区域上被积函数可分离：$\iint_D xy\,dxdy=\left(\int_0^1x\,dx\right)\left(\int_0^2y\,dy\right)=\frac12\times\frac{2^2}{2}=\frac12\times2=1$。

**答案原文**

积分值为 $1$。

## 124. draft-c03-02

内容 SHA256：`849becdea1691788599c324f67372ae06517e02b9eab0460b2d9c31a0336b5e3`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-06/draft-codex-repair-v4-final.jsonl，第 2 行；源 SHA256 `a1e5cdea755498453a9ff3081cb4eb5fc557816c9ab36434f214afc2be6bd04c`。

**题干**

求二重积分 $\iint_D x^2\,dxdy$，其中 $D$ 由 $y=x$、$y=0$、$x=1$ 围成；并换一种积分次序重算验证。

**过程**

先对 $y$ 积分：$\iint_D x^2\,dxdy=\int_0^1\int_0^x x^2\,dy\,dx=\int_0^1 x^3\,dx=\frac14$。换序(先对 $x$)：区域改写为 $0\le y\le1$，$y\le x\le1$，故 $\iint_D x^2\,dxdy=\int_0^1\int_y^1 x^2\,dx\,dy=\int_0^1\frac{1-y^3}{3}\,dy=\frac{1-\frac14}{3}=\frac14$。两种次序结果一致。

**答案原文**

积分值为 $\frac14$(两种积分次序结果一致)。

## 125. draft-c03-03

内容 SHA256：`297452fbd9a7ef7b7abae0008f6c42bb94d9e4bf1584fe7e68cd78a16985b7ea`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-06/draft-codex-repair-v4-final.jsonl，第 3 行；源 SHA256 `a1e5cdea755498453a9ff3081cb4eb5fc557816c9ab36434f214afc2be6bd04c`。

**题干**

用极坐标求二重积分 $\iint_D (x^2+y^2)\,dxdy$，其中 $D$ 为圆盘 $x^2+y^2\le4$ 在第一象限的部分。

**过程**

极坐标:$x=r\cos\theta,y=r\sin\theta$,雅可比为 $r$。区域:$0\le r\le2$,$0\le\theta\le\frac{\pi}{2}$。$\iint_D (x^2+y^2)\,dxdy=\int_0^{\frac{\pi}{2}}\int_0^2 r^2\cdot r\,dr\,d\theta=\int_0^{\frac{\pi}{2}}d\theta\cdot\int_0^2 r^3\,dr=\frac{\pi}{2}\times\frac{2^4}{4}=\frac{\pi}{2}\times4=2\pi$。

**答案原文**

积分值为 $2\pi$。

## 126. draft-c03-04

内容 SHA256：`0d1dcd61f1a3f403ace0ab6e8ce17eb4c3b14d0ac23b8597fef8a52fe3ad3231`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-06/draft-codex-repair-v4-final.jsonl，第 4 行；源 SHA256 `a1e5cdea755498453a9ff3081cb4eb5fc557816c9ab36434f214afc2be6bd04c`。

**题干**

求二重积分 $\iint_D y\,dxdy$，其中 $D$ 为上半圆盘 $x^2+y^2\le1$，$y\ge0$；并说明在全圆盘上的积分值及其理由。

**过程**

极坐标:$0\le r\le1$,$0\le\theta\le\pi$。$\iint_D y\,dxdy=\int_0^{\pi}\int_0^1 (r\sin\theta)\,r\,dr\,d\theta=\int_0^{\pi}\sin\theta\,d\theta\cdot\int_0^1 r^2\,dr=2\times\frac13=\frac23$。(直角坐标验证:$\int_{-1}^{1}\int_0^{\sqrt{1-x^2}}y\,dy\,dx=\int_{-1}^{1}\frac{1-x^2}{2}\,dx=\frac23$。)全圆盘上被积函数 $y$ 关于 $x$ 轴为奇函数,区域关于 $x$ 轴对称,故积分为 $0$。

**答案原文**

上半圆盘上积分为 $\frac23$;全圆盘上积分为 $0$(奇对称性)。

## 127. draft-c03-05

内容 SHA256：`d7852874cd15ca3c77d833a6d5528f7d8014567bf78e877df767e344eaae7cae`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-06/draft-codex-repair-v4-final.jsonl，第 5 行；源 SHA256 `a1e5cdea755498453a9ff3081cb4eb5fc557816c9ab36434f214afc2be6bd04c`。

**题干**

用变量替换 $u=x+y$，$v=x-y$ 求二重积分 $\iint_D (x+y)\,dxdy$，其中 $D=[0,1]\times[0,1]$。

**过程**

雅可比:$\frac{\partial(u,v)}{\partial(x,y)}=\begin{vmatrix}1&1\\1&-1\end{vmatrix}=-2$,故 $dxdy=\frac12\,du\,dv$。区域变换:由 $x=\frac{u+v}{2},y=\frac{u-v}{2}$ 与 $0\le x,y\le1$ 得 $0\le u\le2$,且当 $0\le u\le1$ 时 $-u\le v\le u$;当 $1\le u\le2$ 时 $u-2\le v\le2-u$(菱形)。于是 $\iint_D(x+y)\,dxdy=\int_0^1\int_{-u}^{u}\frac{u}{2}\,dv\,du+\int_1^2\int_{u-2}^{2-u}\frac{u}{2}\,dv\,du=\int_0^1u^2\,du+\int_1^2(2u-u^2)\,du=\frac13+\left(\left.u^2-\frac{u^3}{3}\right|_1^2\right)=\frac13+\left[(4-\frac83)-(1-\frac13)\right]=\frac13+\frac23=1$。直角坐标直算验证:$\int_0^1\int_0^1(x+y)\,dx\,dy=\int_0^1(\frac12+y)\,dy=1$。

**答案原文**

积分值为 $1$(雅可比 $\frac12$,菱形区域分两段)。

## 128. draft-c05-01

内容 SHA256：`af7fd2d1c196dedc852b907ef00c0c30264a5bf5818b23e3276a8751b4eae382`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-06/draft-codex-repair-v4-final.jsonl，第 6 行；源 SHA256 `a1e5cdea755498453a9ff3081cb4eb5fc557816c9ab36434f214afc2be6bd04c`。

**题干**

求极限 $\lim_{x\to\infty}\frac{x^2+3x+1}{2x^2-x+5}$。

**过程**

分子分母同除以最高次项 $x^2$:$\frac{x^2+3x+1}{2x^2-x+5}=\frac{1+\frac3x+\frac1{x^2}}{2-\frac1x+\frac5{x^2}}$。当 $x\to\infty$ 时,$\frac3x,\frac1x,\frac1{x^2},\frac5{x^2}$ 均趋于 $0$,故极限为 $\frac{1}{2}$。

**答案原文**

极限为 $\frac12$。

## 129. draft-c05-02

内容 SHA256：`c13eb787ab999d33005b3921be0c7717bb2e5f26e212da048672627951aac56c`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-06/draft-codex-repair-v4-final.jsonl，第 7 行；源 SHA256 `a1e5cdea755498453a9ff3081cb4eb5fc557816c9ab36434f214afc2be6bd04c`。

**题干**

求 $\lim_{x\to0^+}\frac{|x|}{x}$ 与 $\lim_{x\to0^-}\frac{|x|}{x}$，并判断 $\lim_{x\to0}\frac{|x|}{x}$ 是否存在。

**过程**

当 $x>0$ 时,$|x|=x$,故 $\frac{|x|}{x}=1$,右极限为 $1$。当 $x<0$ 时,$|x|=-x$,故 $\frac{|x|}{x}=-1$,左极限为 $-1$。左右极限不相等,故 $\lim_{x\to0}\frac{|x|}{x}$ 不存在。

**答案原文**

右极限 $1$,左极限 $-1$;$\lim_{x\to0}\frac{|x|}{x}$ 不存在。

## 130. draft-c05-03

内容 SHA256：`21eaa04878364c7c5c32e501f6e34b7a5d61184dee0e78769b803f4347ac578a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-06/draft-codex-repair-v4-final.jsonl，第 8 行；源 SHA256 `a1e5cdea755498453a9ff3081cb4eb5fc557816c9ab36434f214afc2be6bd04c`。

**题干**

求极限 $\lim_{x\to+\infty}\left(\sqrt{x^2+2x}-x\right)$。

**过程**

分子有理化(当 $x>0$ 时):$\sqrt{x^2+2x}-x=\frac{(x^2+2x)-x^2}{\sqrt{x^2+2x}+x}=\frac{2x}{\sqrt{x^2+2x}+x}=\frac{2}{\sqrt{1+\frac2x}+1}$(分子分母同除以 $x$,$x>0$ 时 $\sqrt{x^2+2x}=x\sqrt{1+\frac2x}$)。当 $x\to+\infty$ 时,$\frac2x\to0$,极限为 $\frac{2}{\sqrt1+1}=1$。

**答案原文**

极限为 $1$。

## 131. draft-c05-04

内容 SHA256：`9c1f487573eb3bd95cfbc7fdefff085eab0bbb8c1ee4a5b43884e8a38f75f4f1`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-06/draft-codex-repair-v4-final.jsonl，第 9 行；源 SHA256 `a1e5cdea755498453a9ff3081cb4eb5fc557816c9ab36434f214afc2be6bd04c`。

**题干**

求 $\lim_{x\to+\infty}\frac{x^3}{e^x}$ 与 $\lim_{x\to+\infty}\frac{\ln x}{\sqrt{x}}$，并说明它们反映的增长等级关系。

**过程**

对$x\to+\infty$，三个指数比值均为$\infty/\infty$型，各阶段分母导数$e^x>0$，洛必达法则给出$\lim x^3/e^x=\lim3x^2/e^x=\lim6x/e^x=\lim6/e^x=0$。同理$\ln x/\sqrt x$为$\infty/\infty$型，$\lim\ln x/\sqrt x=\lim(1/x)/(1/(2\sqrt x))=\lim2/\sqrt x=0$。另有$\lim\sqrt x/x^3=\lim x^{-5/2}=0$。所以增长次序用严格比值极限表示为$\lim x^3/e^x=\lim\sqrt x/x^3=\lim\ln x/\sqrt x=0$，以上极限均为$x\to+\infty$。

**答案原文**

两个极限均为$0$；严格增长关系为$\lim_{x\to+\infty}\frac{x^3}{e^x}=\lim_{x\to+\infty}\frac{\sqrt x}{x^3}=\lim_{x\to+\infty}\frac{\ln x}{\sqrt x}=0$。

## 132. draft-c05-05

内容 SHA256：`5c32e870fc960e8be75fc5c0a9690af4122309fee1f8c9db63d59ebb351494ef`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-06/draft-codex-repair-v4-final.jsonl，第 10 行；源 SHA256 `a1e5cdea755498453a9ff3081cb4eb5fc557816c9ab36434f214afc2be6bd04c`。

**题干**

证明 $\lim_{x\to0}\sin\frac{1}{x}$ 不存在。

**过程**

取两个趋于 $0$ 的数列:$x_n=\frac{1}{2n\pi}$,则 $x_n\to0$ 且 $\sin\frac{1}{x_n}=\sin(2n\pi)=0\to0$。再取 $y_n=\frac{1}{2n\pi+\frac{\pi}{2}}$,则 $y_n\to0$ 且 $\sin\frac{1}{y_n}=\sin(2n\pi+\frac{\pi}{2})=1\to1$。两个数列都趋于 $0$,但函数值分别趋于 $0$ 与 $1$。由海涅定理(归结原则),若 $\lim_{x\to0}\sin\frac1x$ 存在,则沿任何趋于 $0$ 的数列函数值应收敛到同一极限,矛盾。故极限不存在。

**答案原文**

极限不存在(取 $x_n=\frac{1}{2n\pi}$ 与 $y_n=\frac{1}{2n\pi+\frac\pi2}$ 两列,函数值分别趋于 $0$ 与 $1$,由海涅定理得矛盾)。

## 133. draft-c46-01

内容 SHA256：`77c35c63856b1411f6e85036833a498be2305f8f59a366973e97c6bb0c28acf7`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-06/draft-codex-repair-v4-final.jsonl，第 11 行；源 SHA256 `a1e5cdea755498453a9ff3081cb4eb5fc557816c9ab36434f214afc2be6bd04c`。

**题干**

$X,Y$相互独立且均匀分布于$[0,1]$。用单位正方形中的面积计算$P(XY\le1/4)$，并说明积分区间的分段依据。

**过程**

联合密度为单位正方形上的$1$，事件概率等于区域面积。当$0\le x\le1/4$，所有$0\le y\le1$满足$xy\le1/4$；当$1/4<x\le1$，须$0\le y\le1/(4x)$。边界面积为零，故$P=\int_0^{1/4}1\,dx+\int_{1/4}^{1}\frac1{4x}\,dx=1/4+(\ln4)/4=1/4+(\ln2)/2$。分段点来自双曲线与上边界$y=1$的交点$x=1/4$；若全区间都用$1/(4x)$会超出样本空间且产生伪发散。

**答案原文**

$P(XY\le1/4)=\frac14+\frac12\ln2$。

## 134. draft-c46-02

内容 SHA256：`9e996cbfafd108e4dfb70bcbfe840e0564b672a4b2ddce1e9dcfb4e2642db6c4`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-06/draft-codex-repair-v4-final.jsonl，第 12 行；源 SHA256 `a1e5cdea755498453a9ff3081cb4eb5fc557816c9ab36434f214afc2be6bd04c`。

**题干**

在单位圆盘 $x^2+y^2\le1$ 内随机取一点(均匀分布),求该点落入内接正方形 $|x|\le\frac{1}{\sqrt2}$，$|y|\le\frac{1}{\sqrt2}$ 的概率。

**过程**

均匀分布下,概率等于面积比。内接正方形的边长为 $\sqrt2$($\frac{1}{\sqrt2}\times2$),面积为 $(\sqrt2)^2=2$。单位圆盘面积为 $\pi$。故所求概率为 $\frac{2}{\pi}$。

**答案原文**

概率为 $\frac{2}{\pi}$。

## 135. draft-c46-03

内容 SHA256：`f1c55a1dc3c5eee2990dfc9cb8a57def556f16fbb2231330d1d169ef33c4dbe9`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-06/draft-codex-repair-v4-final.jsonl，第 13 行；源 SHA256 `a1e5cdea755498453a9ff3081cb4eb5fc557816c9ab36434f214afc2be6bd04c`。

**题干**

从单位正方形均匀选取点$M=(X,Y)$。求$M$分别以$A=(0,0)$、$B=(1,0)$、$C=(0,1)$为三个点中唯一最近点的概率，证明平局不会改变结果。

**过程**

比较平方距离：$MA^2\le MB^2\Leftrightarrow x\le1/2$，$MA^2\le MC^2\Leftrightarrow y\le1/2$，$MB^2\le MC^2\Leftrightarrow y\le x$。所以$A$的区域为$[0,1/2]^2$，面积$1/4$；$B$的区域为$1/2\le x\le1,0\le y\le x$，面积$\int_{1/2}^1x\,dx=3/8$；$C$的区域关于$y=x$对称，面积亦为$3/8$。三面积和为$1$。平局只能位于垂直平分线$x=1/2,y=1/2,y=x$的线段上，其二维面积为零。联合分布连续且均匀，故唯一最近点的概率与非严格比较所得面积相同。

**答案原文**

$P(A\text{ uniquely nearest})=1/4$，$P(B\text{ uniquely nearest})=P(C\text{ uniquely nearest})=3/8$。

## 136. draft-c46-04

内容 SHA256：`1c1dc770b8799b7d2583736481527509a61aa9af2fbef901e79bd0b34228152a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-06/draft-codex-repair-v4-final.jsonl，第 14 行；源 SHA256 `a1e5cdea755498453a9ff3081cb4eb5fc557816c9ab36434f214afc2be6bd04c`。

**题干**

在单位正方形上取联合密度$f(x,y)=x+y$，其余地方为零。验证这是概率密度，求$P(X\le1/2)$，并解释为什么此时不能直接用事件区域与正方形的普通面积之比。

**过程**

$f\ge0$且$\int_0^1\int_0^1(x+y)\,dy\,dx=\int_0^1(x+1/2)\,dx=1$，故密度有效。所求概率为$\int_0^{1/2}\int_0^1(x+y)\,dy\,dx=\int_0^{1/2}(x+1/2)\,dx=1/8+1/4=3/8$。事件区域的普通面积为$1/2$，但该分布不是均匀分布，所以普通面积比不是概率；正确几何表示是密度加权面积。边界线$x=1/2$零测，不影响结果。

**答案原文**

密度归一化积分为$1$；$P(X\le1/2)=3/8$，普通面积比$1/2$不适用。

## 137. draft-c46-05

内容 SHA256：`3317db7f1e2488025f37ac84b8889b62643c24900740d349c631d343f5ba497a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-06/draft-codex-repair-v4-final.jsonl，第 15 行；源 SHA256 `a1e5cdea755498453a9ff3081cb4eb5fc557816c9ab36434f214afc2be6bd04c`。

**题干**

$X,Y$相互独立且均匀分布于$[0,1]$。令$Z=\{2X+3Y\}$为小数部分，即$Z=2X+3Y-\lfloor2X+3Y\rfloor$。用单位正方形的原像面积证明$X,Z$相互独立且$Z$均匀分布于$[0,1]$，并求$P(X\le1/3,Z\le1/2)$。

**过程**

对固定$x$和$0\le b\le1$，置$t=2x+3y$，则$dy=dt/3$，$t$扫过长度为$3$的区间$[2x,2x+3]$。函数$\mathbf1_{\{\{t\}\le b\}}$以$1$为周期，每周期积分为$b$，因而任意长度为$3$的区间积分为$3b$。故$\int_0^1\mathbf1_{\{\{2x+3y\}\le b\}}\,dy=b$。再积分$x$，对$0\le a,b\le1$有$P(X\le a,Z\le b)=\int_0^a b\,dx=ab$。取$a=1$得$Z$的均匀分布，乘积联合分布函数证明独立性。所求为$(1/3)(1/2)=1/6$。整数边界只有有限条直线，面积零；此结论来自精确的周期原像面积，不是抽样估计。

**答案原文**

$P(X\le a,Z\le b)=ab$（$0\le a,b\le1$），故$X,Z$独立且均匀；$P(X\le1/3,Z\le1/2)=1/6$。

## 138. draft-c02-01

内容 SHA256：`eb4278ebccd740074ca7d9f583da3e56f6746b965f7d80294cad4b4129530c61`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-07/draft-codex-repair-v4-final.jsonl，第 1 行；源 SHA256 `abf8c360311f485f3422b04cf43a60a64b166b9a65e9c6e24d79fafcd9978894`。

**题干**

证明广义积分$\int_1^{\infty}\sin(x^2)\,dx$收敛但不绝对收敛，并给出对任意$T>R\ge1$均成立的精确尾积分上界。无需计算积分的具体值。

**过程**

令$u=x^2$，尾积分为$\int_{R^2}^{T^2}\sin u/(2\sqrt u)\,du$。置$w(u)=1/(2\sqrt u)$，分部积分得$[-w(u)\cos u]_{R^2}^{T^2}+\int_{R^2}^{T^2}w^{\prime}(u)\cos u\,du$。因$w$正且递减，其绝对值不超过$w(R^2)+w(T^2)+\int_{R^2}^{T^2}|w^{\prime}|=2w(R^2)=1/R$。由柯西准则，广义积分收敛。绝对值积分换元为$\int_1^{\infty}|\sin u|/(2\sqrt u)\,du$。对$n\ge1$，在$[n\pi+\pi/6,n\pi+5\pi/6]$上$|\sin u|\ge1/2$，故每段贡献至少$\sqrt\pi/(6\sqrt{n+1})$。从$n=N$到$2N-1$的贡献至少$(\sqrt\pi/6)N/\sqrt{2N}=(\sqrt\pi/6)\sqrt{N/2}$，无界，因而不绝对收敛。

**答案原文**

条件收敛；$\left|\int_R^T\sin(x^2)\,dx\right|\le1/R$（$T>R\ge1$）。

## 139. draft-c02-02

内容 SHA256：`1d54536a4e9328ee8bfcafe9cccc8ad193a32d3c1aec728fe3802d2d6fb10f40`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-07/draft-codex-repair-v4-final.jsonl，第 2 行；源 SHA256 `abf8c360311f485f3422b04cf43a60a64b166b9a65e9c6e24d79fafcd9978894`。

**题干**

在$[1,\infty)$上定义$g(x)=n$，当$x\in[n,n+2^{-n}/n]$、$n\in\mathbb N^+$时；其余点令$g(x)=0$。证明$g$局部黎曼可积且广义积分收敛，求精确积分值，并判断$\lim_{x\to\infty}g(x)$是否存在。

**过程**

每个尖峰宽度为$2^{-n}/n\le1/2$，支撑区间互不重叠；在任意有界区间上只有有限个跳跃点，函数有界，故黎曼可积。一个完整尖峰面积为$n\cdot2^{-n}/n=2^{-n}$，因此$\int_1^{N+1}g=\sum_{n=1}^N2^{-n}=1-2^{-N}$（$x=N+1$处单点值不影响积分）。由于$g\ge0$，任意上限$R$可夹在相邻整数上限之间，积分极限存在且等于$1$。取$t_n=n+2^{-n-1}/n$，有$g(t_n)=n\to\infty$；取$s_n=n+3/4$，有$g(s_n)=0$。两列都趋于无穷，故函数没有有限极限，也不趋于正无穷。此例证明非负可积函数不必趋于零，也不必全局有界。

**答案原文**

$\int_1^{\infty}g(x)\,dx=1$；$\lim_{x\to\infty}g(x)$不存在，且$g$不趋于零。

## 140. draft-c02-03

内容 SHA256：`d6ae9cf2fbb6a2bb111f9e6020c851377e7486ed3f52c2d60105046061957431`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-07/draft-codex-repair-v4-final.jsonl，第 3 行；源 SHA256 `abf8c360311f485f3422b04cf43a60a64b166b9a65e9c6e24d79fafcd9978894`。

**题干**

判断 $\int_2^{+\infty}\frac{1}{x\ln x}\,dx$ 与 $\int_2^{+\infty}\frac{1}{x\ln^2 x}\,dx$ 的敛散性，并求收敛者的值。

**过程**

换元 $u=\ln x$,$du=\frac{dx}{x}$。第一个:$\int_2^R\frac{1}{x\ln x}dx=\int_{\ln2}^{\ln R}\frac{du}{u}=\ln(\ln R)-\ln(\ln2)\to+\infty$,发散。第二个:$\int_2^R\frac{1}{x\ln^2x}dx=\int_{\ln2}^{\ln R}\frac{du}{u^2}=\frac{1}{\ln2}-\frac{1}{\ln R}\to\frac{1}{\ln2}$,收敛且值为 $\frac{1}{\ln2}$。

**答案原文**

$\int_2^{+\infty}\frac{1}{x\ln x}dx$ 发散;$\int_2^{+\infty}\frac{1}{x\ln^2x}dx$ 收敛,值为 $\frac{1}{\ln2}$。

## 141. draft-c02-04

内容 SHA256：`cee141451c1ae9dbf9524d9a3112d21755ec4b12b7e49a84405fe2bb2d535ece`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-07/draft-codex-repair-v4-final.jsonl，第 4 行；源 SHA256 `abf8c360311f485f3422b04cf43a60a64b166b9a65e9c6e24d79fafcd9978894`。

**题干**

设$a,b>0$。证明$\int_0^{\infty}(e^{-ax}-e^{-bx})/x\,dx$收敛并求精确值；说明交换积分的依据及为什么不能把它拆成两个广义积分之差。

**过程**

对$x>0$有精确恒等式$(e^{-ax}-e^{-bx})/x=\int_a^be^{-tx}\,dt$。若$a<b$，二重被积函数非负，Tonelli定理允许交换积分，得$\int_a^b\int_0^{\infty}e^{-tx}\,dx\,dt=\int_a^b1/t\,dt=\ln(b/a)<\infty$；所以原积分绝对收敛。若$a>b$，交换二参数取负；若$a=b$，被积函数恒为零。亦可直接给上界：近零绝对值不超过$|b-a|$，而$R>0$后的绝对尾积分不超过$|b-a|e^{-\min(a,b)R}/\min(a,b)$。每个单独的$e^{-ax}/x$在零点附近与$1/x$具有同阶正下界，故从零开始积分发散；原式依赖抵消，不能写成两个未定义的发散积分之差。

**答案原文**

对所有$a,b>0$均绝对收敛，积分精确等于$\ln(b/a)$。

## 142. draft-c02-05

内容 SHA256：`51d9faea52ca212ffcf83f7bafadedf9632725abb16d48b8a43b4fc7c22c85d8`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-07/draft-codex-repair-v4-final.jsonl，第 5 行；源 SHA256 `abf8c360311f485f3422b04cf43a60a64b166b9a65e9c6e24d79fafcd9978894`。

**题干**

对实参数$a$，讨论$\int_0^{\infty}x^{a-1}/(1+x)\,dx$的收敛性，必须同时处理零点与无穷远。并在$a=1/2$时求精确值。

**过程**

在$0<x\le1$，被积函数介于$x^{a-1}/2$与$x^{a-1}$之间；在$x\ge1$，介于$x^{a-2}/2$与$x^{a-2}$之间。若$0<a<1$，在零端二进分块$[2^{-n-1},2^{-n}]$（$n\ge0$）上积分不超过$2^{-a(n+1)}$；在无穷端分块$[2^n,2^{n+1}]$上积分不超过$2^{n(a-1)}$。前后两个精确几何级数的公比分别为$2^{-a}<1$、$2^{a-1}<1$，故两个端点均收敛。若$a\le0$，在$(0,1]$被积函数不小于$1/(2x)$，零端发散；若$a\ge1$，在$[1,\infty)$被积函数不小于$1/(2x)$，无穷端发散。这穷尽所有实参数。$a=1/2$时令$x=t^2$，积分为$2\int_0^{\infty}1/(1+t^2)\,dt=2[\arctan t]_0^{\infty}=\pi$。两端分别取极限，不能只检查无穷远而忽略零端。

**答案原文**

收敛当且仅当$0<a<1$；当$a=1/2$时积分等于$\pi$。

## 143. draft-c04-01

内容 SHA256：`7f740f8251109b8a0c7254accfa7e7f84ddbd75a1ac56992bad93dfba7cebb21`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-07/draft-codex-repair-v4-final.jsonl，第 6 行；源 SHA256 `abf8c360311f485f3422b04cf43a60a64b166b9a65e9c6e24d79fafcd9978894`。

**题干**

用格林公式求 $\oint_L x^2\,dy$，其中 $L$ 为以 $(0,0),(1,0),(0,1)$ 为顶点的三角形正向边界，并直接计算验证。

**过程**

格林公式:$\oint_L x^2\,dy=\iint_D 2x\,dxdy$。区域 $D$:$0\le y\le1$,$0\le x\le1-y$。$\iint_D 2x\,dxdy=\int_0^1\int_0^{1-y}2x\,dx\,dy=\int_0^1(1-y)^2\,dy=\frac13$。直接验证:底边 $y=0$ 上 $dy=0$ 贡献为 $0$;竖边 $x=0$ 上 $x^2=0$ 贡献为 $0$;斜边 $x=1-y$($y$ 从 $0$ 到 $1$):$\int_0^1(1-y)^2\,dy=\frac13$。两法一致。

**答案原文**

积分值为 $\frac13$(格林公式与直接计算一致)。

## 144. draft-c04-02

内容 SHA256：`308edd8a5c26ff8e161ba9752e622966f3c198eb03b959b81a2654371ddc7fa5`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-07/draft-codex-repair-v4-final.jsonl，第 7 行；源 SHA256 `abf8c360311f485f3422b04cf43a60a64b166b9a65e9c6e24d79fafcd9978894`。

**题干**

求 $\oint_L y\,dx$，其中 $L$ 为逆时针单位圆周；并说明若沿顺时针方向积分，结果如何变化。

**过程**

格林公式:$\oint_L y\,dx=\iint_D(0-1)\,dxdy=-\iint_D 1\,dxdy=-A$,其中 $A$ 为区域面积。单位圆面积 $A=\pi$,故逆时针积分为 $-\pi$。若改为顺时针,格林公式需取负号(或等价地区域定向反转),结果为 $+\pi$。

**答案原文**

逆时针为 $-\pi$;顺时针为 $+\pi$(符号随定向反转)。

## 145. draft-c04-03

内容 SHA256：`0cf425e37b85120077672b81ff6ee8907a0c14208be2a7aa4a5212ce7c121ab6`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-07/draft-codex-repair-v4-final.jsonl，第 8 行；源 SHA256 `abf8c360311f485f3422b04cf43a60a64b166b9a65e9c6e24d79fafcd9978894`。

**题干**

用格林公式求 $\oint_L -y^3\,dx+x^3\,dy$，其中 $L$ 为圆环 $1\le x^2+y^2\le4$ 的边界(外圆逆时针、内圆顺时针)，并说明内外圆方向相反的原因。

**过程**

格林公式(区域 $D$ 为圆环):$\oint_L -y^3dx+x^3dy=\iint_D\left(\frac{\partial}{\partial x}x^3-\frac{\partial}{\partial y}(-y^3)\right)dxdy=\iint_D(3x^2+3y^2)\,dxdy=3\iint_D r^2\cdot r\,dr\,d\theta=3\int_0^{2\pi}d\theta\int_1^2r^3\,dr=3\times2\pi\times\frac{2^4-1^4}{4}=\frac{45\pi}{2}$。方向:为使区域 $D$ 总在边界的左侧(正向),外边界须逆时针、内边界须顺时针。

**答案原文**

积分值为 $\frac{45\pi}{2}$;外逆内顺保证区域在边界左侧(正向)。

## 146. draft-c04-04

内容 SHA256：`f6d1057c7dd9202d60371db9c4f4f59a30558a9f9759ff958a00fc444fe5547a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-07/draft-codex-repair-v4-final.jsonl，第 9 行；源 SHA256 `abf8c360311f485f3422b04cf43a60a64b166b9a65e9c6e24d79fafcd9978894`。

**题干**

用格林公式(补边闭合)计算曲线积分 $\int_L (x+y)\,dx+x\,dy$，其中 $L$ 为抛物线 $y=x^2$ 上从 $(0,0)$ 到 $(1,1)$ 的弧段。

**过程**

补直线段 $L'$:从 $(1,1)$ 沿直线回到 $(0,0)$,$L+L'$ 为闭合曲线。区域 $D$ 内,$\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}=\frac{\partial x}{\partial x}-\frac{\partial(x+y)}{\partial y}=1-1=0$,故 $\oint_{L+L'}=0$,于是 $\int_L=-\int_{L'}$。参数化 $L'$:$(1-t,1-t)$,$t\in[0,1]$,$dx=dy=-dt$:$\int_{L'}(x+y)dx+x\,dy=\int_0^1\left[(2-2t)(-1)+(1-t)(-1)\right]dt=\int_0^1(3t-3)\,dt=-\frac32$。故 $\int_L=\frac32$。

**答案原文**

积分值为 $\frac32$(补边闭合,格林公式得闭合积分为零)。

## 147. draft-c04-05

内容 SHA256：`b9cfb03652e61bb2f5f67856198e3f07bb393a9a6563e17371be3bd1412b9a42`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-07/draft-codex-repair-v4-final.jsonl，第 10 行；源 SHA256 `abf8c360311f485f3422b04cf43a60a64b166b9a65e9c6e24d79fafcd9978894`。

**题干**

设$P=-2y/(x^2+y^2)+3y/((x-3)^2+y^2)$，$Q=2x/(x^2+y^2)-3(x-3)/((x-3)^2+y^2)$。取圆盘$(x-3/2)^2+y^2\le16$，挖去以$(0,0)$、$(3,0)$为中心、半径$1/2$的两个开圆盘，得区域$D$。分别求外圆逆时针及两个内圆顺时针的积分$\oint P\,dx+Q\,dy$，并验证正向总边界的Green公式。

**过程**

两小圆盘互不相交且严格在大圆盘内。$P,Q$在$\overline D$的某邻域中连续可微，直接求导得$Q_x-P_y=0$。以原点为中心的场$(-ky/r^2,kx/r^2)$沿逆时针圆的积分为$2\pi k$，由$x=r\cos t,y=r\sin t$可直接得到被积表达式$k\,dt$；顺时针则取负。第一孔中心场权重$2$，给顺时针积分$-4\pi$；第二孔中心场权重$-3$，给顺时针积分$6\pi$。对每个孔，另一中心的场在该孔闭圆盘附近光滑且旋度零，Green公式给其圆周积分为零。对带两孔区域正确应用Green公式，外圆积分$I_{\rm out}$加两个顺时针内圆积分等于$0$，故$I_{\rm out}-4\pi+6\pi=0$，即$I_{\rm out}=-2\pi$。总正向边界积分为零。不能把外圆所围实心圆盘直接用于Green公式，因为该实心盘包含两个奇点。

**答案原文**

外圆逆时针$-2\pi$；原点孔顺时针$-4\pi$；$(3,0)$孔顺时针$6\pi$；正向总边界积分为$0$。

## 148. draft-c06-01

内容 SHA256：`99f7ffe5c190c2bd296f110f9e0e684472b0771600dd6931c469ad1e76138240`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-07/draft-codex-repair-v4-final.jsonl，第 11 行；源 SHA256 `abf8c360311f485f3422b04cf43a60a64b166b9a65e9c6e24d79fafcd9978894`。

**题干**

求由抛物线 $y=x^2$ 与 $y=2-x^2$ 围成的封闭图形的面积。

**过程**

交点:$x^2=2-x^2$ 得 $x=\pm1$。利用对称性,$A=\int_{-1}^{1}\left[(2-x^2)-x^2\right]dx=2\int_0^1(2-2x^2)\,dx=2\left.\left(2x-\frac{2x^3}{3}\right)\right|_0^1=2\times\frac43=\frac83$。

**答案原文**

面积为 $\frac83$。

## 149. draft-c06-02

内容 SHA256：`219e3934dc5e9fe422506c77b03d9ce4e4563c64459ffcaf5e5ff679343fe76a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-07/draft-codex-repair-v4-final.jsonl，第 12 行；源 SHA256 `abf8c360311f485f3422b04cf43a60a64b166b9a65e9c6e24d79fafcd9978894`。

**题干**

求由 $y=|x|$ 与 $y=1$ 围成的封闭图形的面积。

**过程**

交点:$|x|=1$ 得 $x=\pm1$。区域关于 $y$ 轴对称,右半部分为 $0\le x\le1$,$|x|\le y\le1$。$A=2\int_0^1(1-x)\,dx=2\left.\left(x-\frac{x^2}{2}\right)\right|_0^1=2\times\frac12=1$。

**答案原文**

面积为 $1$。

## 150. draft-c06-03

内容 SHA256：`8154458b4729d95ba804174567373832715576838600ecae5c267c7798cd7627`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-07/draft-codex-repair-v4-final.jsonl，第 13 行；源 SHA256 `abf8c360311f485f3422b04cf43a60a64b166b9a65e9c6e24d79fafcd9978894`。

**题干**

求由抛物线 $x=y^2$ 与直线 $y=x-2$ 围成的封闭图形的面积(按 $y$ 积分)。

**过程**

交点:$y^2=y+2$,即 $y^2-y-2=0$,得 $y=-1$ 与 $y=2$。区域在 $y$ 方向的范围为 $[-1,2]$,右边界为直线 $x=y+2$,左边界为抛物线 $x=y^2$。$A=\int_{-1}^{2}\left[(y+2)-y^2\right]dy=\left.\left(\frac{y^2}{2}+2y-\frac{y^3}{3}\right)\right|_{-1}^{2}=\left(2+4-\frac83\right)-\left(\frac12-2+\frac13\right)=\frac{10}{3}+\frac76=\frac92$。

**答案原文**

面积为 $\frac92$。

## 151. draft-c06-04

内容 SHA256：`9c4d13e22cedd5eb0f5b46205d69fb45f1f1170b1761637a49e7bf89d03cf4af`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-07/draft-codex-repair-v4-final.jsonl，第 14 行；源 SHA256 `abf8c360311f485f3422b04cf43a60a64b166b9a65e9c6e24d79fafcd9978894`。

**题干**

求由抛物线 $y=x^2$ 与直线 $y=kx$($k>0$)围成的封闭图形的面积(用 $k$ 表示)，并求 $k=2$ 时的面积。

**过程**

交点:$x^2=kx$ 得 $x=0$ 与 $x=k$。在 $[0,k]$ 上,$kx\ge x^2$。$A(k)=\int_0^k(kx-x^2)\,dx=\left.\left(\frac{kx^2}{2}-\frac{x^3}{3}\right)\right|_0^k=\frac{k^3}{2}-\frac{k^3}{3}=\frac{k^3}{6}$。当 $k=2$ 时,$A=\frac{2^3}{6}=\frac43$。

**答案原文**

$A(k)=\frac{k^3}{6}$;$k=2$ 时面积为 $\frac43$。

## 152. draft-c07-01

内容 SHA256：`2310a3bdbd8a26c9250d90bb383dfd027987a43514dd056d5b47255e283b6905`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft-codex-repair-v4-final.jsonl，第 1 行；源 SHA256 `7309fa42140db57b43b38b4223b922fd04c8fa90d53138b79036bc8d15778e2f`。

**题干**

求三叶玫瑰线 $r=2\sin 3\theta$ 的一叶所围成的面积。

**过程**

一叶对应角域 $0\le\theta\le\frac{\pi}{3}$(当 $\theta$ 从 $0$ 到 $\frac{\pi}{3}$ 时,$r$ 从 $0$ 增大到 $2$ 再回到 $0$)。面积 $A=\frac12\int_0^{\frac{\pi}{3}}r^2\,d\theta=\frac12\int_0^{\frac{\pi}{3}}4\sin^2 3\theta\,d\theta=2\int_0^{\frac{\pi}{3}}\sin^2 3\theta\,d\theta$。换元 $u=3\theta$:$\int_0^{\frac{\pi}{3}}\sin^2 3\theta\,d\theta=\frac13\int_0^{\pi}\sin^2u\,du=\frac13\cdot\frac{\pi}{2}=\frac{\pi}{6}$。故 $A=2\times\frac{\pi}{6}=\frac{\pi}{3}$。

**答案原文**

一叶面积为 $\frac{\pi}{3}$。

## 153. draft-c07-02

内容 SHA256：`9c6f19ff89c92b17c2c5a93caeb9793096b2a19afdf32c97fdb1067570e57a90`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft-codex-repair-v4-final.jsonl，第 2 行；源 SHA256 `7309fa42140db57b43b38b4223b922fd04c8fa90d53138b79036bc8d15778e2f`。

**题干**

极坐标曲线$r=2+3\cos\theta$具有内环。分别求内环面积、外环所围面积和两环内部区域并集的面积，说明为什么全周期的$\frac12\int r^2d\theta$不等于并集面积。

**过程**

令$\beta=\arccos(2/3)\in(0,\pi/2)$、$\alpha=\pi-\beta$。$r\ge0$的外环对应$-\alpha\le\theta\le\alpha$，$r\le0$的内环对应$\alpha\le\theta\le2\pi-\alpha$。$r^2/2$的原函数为$F(\theta)=17\theta/4+6\sin\theta+(9/8)\sin2\theta$。由$\sin\beta=\sqrt5/3$、$\sin2\beta=4\sqrt5/9$，内环面积为$F(2\pi-\alpha)-F(\alpha)=17\beta/2-3\sqrt5$；外环面积为$F(\alpha)-F(-\alpha)=17(\pi-\beta)/2+3\sqrt5$。在内环的实际方向$\phi\in[-\beta,\beta]$上，负半径转换给内环径向边界$\rho_{\rm in}=3\cos\phi-2$，外环对应$\rho_{\rm out}=2+3\cos\phi$，相差$4$；该方向区间也属于外环区间。因此内环内部包含于外环内部，并集面积就是外环面积。全周期积分为$17\pi/2$，等于两环面积之和，把内环内部重复计算一次。

**答案原文**

令$\beta=\arccos(2/3)$。内环$17\beta/2-3\sqrt5$；外环及并集面积均为$17(\pi-\beta)/2+3\sqrt5$；全周期平方积分为$17\pi/2$。

## 154. draft-c07-03

内容 SHA256：`ffe9919aa068263772a663fdf5c90883e29932717710d9b651e287469ec197fb`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft-codex-repair-v4-final.jsonl，第 3 行；源 SHA256 `7309fa42140db57b43b38b4223b922fd04c8fa90d53138b79036bc8d15778e2f`。

**题干**

求四叶玫瑰线 $r=\cos 2\theta$ 所围成的总面积，并说明为什么只需计算一叶再乘 $4$。

**过程**

一叶对应角域 $-\frac{\pi}{4}\le\theta\le\frac{\pi}{4}$(其间 $r\ge0$ 且极径从 $0$ 出发回到 $0$)。一叶面积 $A_1=\frac12\int_{-\frac{\pi}{4}}^{\frac{\pi}{4}}\cos^2 2\theta\,d\theta$。换元 $u=2\theta$:$\int_{-\frac{\pi}{4}}^{\frac{\pi}{4}}\cos^2 2\theta\,d\theta=\frac12\int_{-\frac{\pi}{2}}^{\frac{\pi}{2}}\cos^2u\,du=\frac12\cdot\frac{\pi}{2}=\frac{\pi}{4}$。故 $A_1=\frac12\cdot\frac{\pi}{4}=\frac{\pi}{8}$。四叶互不重叠且完全对称,总面积为 $4A_1=\frac{\pi}{2}$。

**答案原文**

总面积为 $\frac{\pi}{2}$(一叶 $\frac{\pi}{8}$ 乘 $4$)。

## 155. draft-c07-04

内容 SHA256：`67dad708c43ac80859e988bda34962b026eb20703d7d7dd93b19a90b2ec9282e`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft-codex-repair-v4-final.jsonl，第 4 行；源 SHA256 `7309fa42140db57b43b38b4223b922fd04c8fa90d53138b79036bc8d15778e2f`。

**题干**

求圆 $r=4\cos\theta$ 内部位于圆 $r=2$ 外部的区域(月牙形)的面积。

**过程**

两圆交点:$4\cos\theta=2$ 得 $\cos\theta=\frac12$,即 $\theta=\pm\frac{\pi}{3}$。所求区域由 $-\frac{\pi}{3}\le\theta\le\frac{\pi}{3}$ 且 $2\le r\le4\cos\theta$ 描述。$A=\frac12\int_{-\frac{\pi}{3}}^{\frac{\pi}{3}}\left[(4\cos\theta)^2-2^2\right]d\theta=\frac12\int_{-\frac{\pi}{3}}^{\frac{\pi}{3}}(16\cos^2\theta-4)\,d\theta=\int_{-\frac{\pi}{3}}^{\frac{\pi}{3}}(8\cos^2\theta-2)\,d\theta=\int_{-\frac{\pi}{3}}^{\frac{\pi}{3}}(2+4\cos2\theta)\,d\theta=\left.2\theta+2\sin2\theta\right|_{-\frac{\pi}{3}}^{\frac{\pi}{3}}=\frac{4\pi}{3}+2\sqrt3$。

**答案原文**

面积为 $\frac{4\pi}{3}+2\sqrt3$。

## 156. draft-c07-05

内容 SHA256：`0ff7456cfb276ec5b5f3eb14bb4b7668494212d01d8c88aed5c1c68156155b48`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft-codex-repair-v4-final.jsonl，第 5 行；源 SHA256 `7309fa42140db57b43b38b4223b922fd04c8fa90d53138b79036bc8d15778e2f`。

**题干**

求双纽线 $r^2=\cos 2\theta$ 所围成的总面积，并说明角域的确定方式。

**过程**

需 $r^2\ge0$,即 $\cos2\theta\ge0$,故角域为 $[-\frac{\pi}{4},\frac{\pi}{4}]\cup[\frac{3\pi}{4},\frac{5\pi}{4}]$(按模 $2\pi$ 理解,等价于 $[0,\frac{\pi}{4}]\cup[\frac{3\pi}{4},\frac{5\pi}{4}]\cup[\frac{7\pi}{4},2\pi]$),两段对应两个对称的叶。右叶面积 $A_1=\frac12\int_{-\frac{\pi}{4}}^{\frac{\pi}{4}}\cos2\theta\,d\theta=\frac12\left.\frac{\sin2\theta}{2}\right|_{-\frac{\pi}{4}}^{\frac{\pi}{4}}=\frac12\times1=\frac12$。总面积 $=2A_1=1$。

**答案原文**

总面积为 $1$(每叶 $\frac12$,共两叶)。

## 157. draft-c08-01

内容 SHA256：`b8c3fcc4fed26a0f4c1b9dcab6d72d60aec60525e16217393e70f5b7bde1dde1`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft-codex-repair-v4-final.jsonl，第 6 行；源 SHA256 `7309fa42140db57b43b38b4223b922fd04c8fa90d53138b79036bc8d15778e2f`。

**题干**

设$a>0$，摆线一拱参数方程$x=a(t-\sin t),y=a(1-\cos t)$，$0\le t\le2\pi$。求这一拱与$x$轴围成的面积，并说明参数积分方向与封闭边界的依据。

**过程**

$x^{\prime}=a(1-\cos t)\ge0$，在$(0,2\pi)$严格为正；$y\ge0$，两端点为$(0,0)$与$(2\pi a,0)$。因此这一拱是从左到右的单值图形，由轴上线段闭合，普通面积为$\int y\,dx=\int_0^{2\pi}a^2(1-\cos t)^2\,dt$。展开得$\int_0^{2\pi}(1-2\cos t+\cos^2t)dt=2\pi+0+\pi=3\pi$，故面积$3\pi a^2$。这里沿上拱从左到右的$\int y\,dx$给正面积；如果使用有向闭曲线公式，应同时说明此上拱方向对应顺时针闭边界，不能混用逆时针符号。轴上线段的$y\,dx$贡献为零。

**答案原文**

面积$3\pi a^2$。

## 158. draft-c08-02

内容 SHA256：`8dcee93cf6872a785246fbd559f9a64c2926609bfa6e9ec48ba44a7f621e1870`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft-codex-repair-v4-final.jsonl，第 7 行；源 SHA256 `7309fa42140db57b43b38b4223b922fd04c8fa90d53138b79036bc8d15778e2f`。

**题干**

求星形线 $\begin{cases}x=a\cos^3 t\\ y=a\sin^3 t\end{cases}$($a>0$)围成的面积。

**过程**

星形线在第一象限的部分对应 $t$ 从 $\frac{\pi}{2}$ 到 $0$。第一象限面积 $A_1=\int_{\frac{\pi}{2}}^{0}y\,x'\,dt$ 的绝对值,$x'=-3a\cos^2t\sin t$:$\int_{\frac{\pi}{2}}^{0}(a\sin^3t)(-3a\cos^2t\sin t)\,dt=3a^2\int_0^{\frac{\pi}{2}}\sin^4t\cos^2t\,dt=3a^2\cdot\frac{(3!!\cdot1!!)\pi}{6!!\cdot2}=3a^2\cdot\frac{3\pi}{96}=\frac{3\pi a^2}{32}$。总面积为 $4A_1=\frac{3\pi a^2}{8}$。

**答案原文**

面积为 $\frac{3\pi a^2}{8}$。

## 159. draft-c08-03

内容 SHA256：`e38c639fb51f5b386cb43e1b7518aa3d3649b6c6773cd5f01847a9b1102bd89f`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft-codex-repair-v4-final.jsonl，第 8 行；源 SHA256 `7309fa42140db57b43b38b4223b922fd04c8fa90d53138b79036bc8d15778e2f`。

**题干**

求笛卡尔叶形线 $x=\frac{3t}{1+t^3}$，$y=\frac{3t^2}{1+t^3}$($t\ge0$)的环所围成的面积。

**过程**

叶形线的环对应 $t$ 从 $0$ 到 $+\infty$(曲线从原点出发,经第一象限后回到原点)。用面积公式 $A=\frac12\int_0^{+\infty}(x\,y'-y\,x')\,dt$。计算:$x'=\frac{3(1-2t^3)}{(1+t^3)^2}$,$y'=\frac{3t(2-t^3)}{(1+t^3)^2}$,故 $x\,y'-y\,x'=\frac{9t^2(2-t^3)-9t^2(1-2t^3)}{(1+t^3)^3}=\frac{9t^2(1+t^3)}{(1+t^3)^3}=\frac{9t^2}{(1+t^3)^2}$。$A=\frac12\int_0^{+\infty}\frac{9t^2}{(1+t^3)^2}\,dt=\frac12\left.\left(-\frac{3}{1+t^3}\right)\right|_0^{+\infty}=\frac12\times3=\frac32$。 对$t>0$有$y/x=t$，故不同有限参数对应不同非原点，曲线在此参数域无自交；$t\downarrow0$与$t\to+\infty$均趋于原点，恰描绘一个环一次。上述无穷上限须理解为有限积分再取极限，原函数给出极限$3/2$。

**答案原文**

环的面积为 $\frac32$。

## 160. draft-c08-04

内容 SHA256：`ce1be38d92779edfb535bfe9c5c4f786da8a5abff06ffd80d803a4543270f902`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft-codex-repair-v4-final.jsonl，第 9 行；源 SHA256 `7309fa42140db57b43b38b4223b922fd04c8fa90d53138b79036bc8d15778e2f`。

**题干**

求李萨如曲线 $\begin{cases}x=\cos t\\ y=\sin 2t\end{cases}$ 的两个环各自的面积与总面积，并说明沿全周期 $[0,2\pi]$ 的有向积分为何为零。

**过程**

曲线在 $t=\frac{\pi}{2}$ 与 $t=\frac{3\pi}{2}$ 处经过原点;在 $t=0$ 与 $t=\pi$ 处分别经过两环的顶点 $(1,0)$ 与 $(-1,0)$。两个环分别对应 $t\in[-\frac{\pi}{2},\frac{\pi}{2}]$ 与 $t\in[\frac{\pi}{2},\frac{3\pi}{2}]$。$x\,y'-y\,x'=\cos t\cdot2\cos2t-\sin2t\cdot(-\sin t)=2\cos t\cos2t+\sin t\sin2t$。第一环:$\int_{-\frac{\pi}{2}}^{\frac{\pi}{2}}(2\cos t\cos2t+\sin t\sin2t)\,dt=\int_{-\frac{\pi}{2}}^{\frac{\pi}{2}}\left(\frac32\cos t+\frac12\cos3t\right)dt=\left.\frac32\sin t+\frac16\sin3t\right|_{-\frac{\pi}{2}}^{\frac{\pi}{2}}=3-\frac13=\frac83$,故第一环面积 $\frac12\cdot\frac83=\frac43$。由对称性第二环面积也是 $\frac43$,总面积 $\frac83$。全周期有向积分:$\int_0^{2\pi}\cos t\cos2t\,dt=0$ 且 $\int_0^{2\pi}\sin t\sin2t\,dt=0$(正交性),两个环定向相反、有向值相消,故为零——有向面积为零而实际面积为 $\frac83$。

**答案原文**

每环面积 $\frac43$,总面积 $\frac83$;全周期有向积分为 $0$(两环定向相反,相互抵消)。

## 161. draft-c08-05

内容 SHA256：`3c9f4c174eae96490eecdef71ec7d8ee608ba5c8a7ce4ff567572daeba81e317`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft-codex-repair-v4-final.jsonl，第 10 行；源 SHA256 `7309fa42140db57b43b38b4223b922fd04c8fa90d53138b79036bc8d15778e2f`。

**题干**

对分段$C^1$参数曲线推导面积公式，明确：简单闭曲线单次遍历；曲线为$x$的图像且沿$x$单调遍历一次；自交曲线可拆成有限个简单圈。在第三种情形区分各圈内部两两不交与存在重叠。分别说明绝对值及重叠计数的处理，并用圆$x=\cos t,y=2+\sin t$说明简单闭曲线不能一般性地分段取绝对值。

**过程**

一、若$L$是简单闭曲线，单次遍历且正向，由格林公式$\oint_L y\,dx=-\operatorname{area}(D)$；反向符号反转。因此$A=|\int_\alpha^\beta y(t)x^{\prime}(t)dt|$，须整圈积分后取绝对值。一般闭曲线不能把$|y|\,dx$当作非负面积元。二、若曲线是$y=f(x)$的图像且$x(t)$单调、单次遍历$x$区间，图线与$x$轴之间的面积为$A=\int|f(x)|\,|dx|=\int_\alpha^\beta|y(t)x^{\prime}(t)|dt$，可按$y=0$分段求和；单调性防止重复计数。三、若自交曲线拆成简单圈$L_k$，各圈均单次遍历且内部$D_k$两两不交，则实际总面积为$\sum_k|\oint_{L_k}y\,dx|$。若内部有重叠，此和计重，不能当作并集面积；对有限个圈须用$\operatorname{area}(\bigcup_kD_k)=\sum_{\varnothing\ne I\subseteq\{1,\ldots,m\}}(-1)^{|I|+1}\operatorname{area}(\bigcap_{i\in I}D_i)$或拆成互不重叠的面域后求和。全曲线的带符号积分记录绕数加权的有向面积，不能用一次绝对值消除反向抵消或重复遍历。反例：$x=\cos t,y=2+\sin t$（$0\le t\le2\pi$），$\int_0^{2\pi}yx^{\prime} dt=-\pi$，故圆面积为$\pi$。按$t=\pi$分段，两积分为$-4-\pi/2$和$4-\pi/2$；因$0<\pi<4$，分别取绝对值得$8\ne\pi$，不等于圆面积。

**答案原文**

简单闭曲线单次遍历：$A=|\oint y\,dx|$。单调遍历图线：$A=\int|yx^{\prime}|dt$。有限简单圈且内部两两不交：$A=\sum_k|\oint_{L_k}y\,dx|$；有重叠则须去重，不能直接相加。反例圆：整圈面积$\pi$，分段绝对值之和$8\ne\pi$。

## 162. draft-c09-01

内容 SHA256：`74b678433635bce07caed03a59dbcf572c698b9f19991077fb72f6420475a96f`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft-codex-repair-v4-final.jsonl，第 11 行；源 SHA256 `7309fa42140db57b43b38b4223b922fd04c8fa90d53138b79036bc8d15778e2f`。

**题干**

区域$D=\{(x,y):0\le x\le1,-x\le y\le x^2\}$绕$x$轴旋转。求体积，并说明为什么不能把上下边界的平方直接相减。

**过程**

固定$x\in[0,1]$，纵截面跨越旋转轴。下半段$[-x,0]$旋转填满半径$x$的圆盘，上半段$[0,x^2]$填满半径$x^2$的圆盘。因为$x\ge x^2$，两圆盘并集为半径$x$的圆盘，截面积为$\pi x^2$，不是圆环。故$V=\pi\int_0^1x^2dx=\pi/3$。若错用$\pi\int_0^1(x^2-x^4)dx$，会得$2\pi/15$；这是把轴两侧互相重叠的旋转像错误地相减，漏掉已被填满的内部。

**答案原文**

$V=\pi/3$，截面为半径$x$的圆盘。

## 163. draft-c09-02

内容 SHA256：`91c2d8e43634ea60a9d0c13704a68d7060c8593f1e7749f0285da12909c0f3b6`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft-codex-repair-v4-final.jsonl，第 12 行；源 SHA256 `7309fa42140db57b43b38b4223b922fd04c8fa90d53138b79036bc8d15778e2f`。

**题干**

单位圆盘$x^2+y^2\le1$绕外部直线$y=2$旋转。用截面圆环法求体积，并用质心定理独立验证，明确该定理适用的轴位置条件。

**过程**

对$-1\le x\le1$，置$h=\sqrt{1-x^2}$。截面到轴的距离范围为$[2-h,2+h]$，两端均正，圆环截面积$\pi[(2+h)^2-(2-h)^2]=8\pi\sqrt{1-x^2}$。因此$V=8\pi\int_{-1}^1\sqrt{1-x^2}dx=8\pi(\pi/2)=4\pi^2$，其中积分是单位圆的上半圆面积，亦可用$x=\sin t$在$[-\pi/2,\pi/2]$精确积分验证。独立地，圆盘面积为$\pi$、质心为原点，外部轴到质心距离为$2$；轴与圆盘不相交，满足Pappus质心定理条件，故$V=\pi\cdot2\pi\cdot2=4\pi^2$。此实体是主半径$2$、管半径$1$的环面。

**答案原文**

$V=4\pi^2$；截面圆环法与Pappus质心定理结果相同。

## 164. draft-c09-03

内容 SHA256：`8d62f3fb3d2bb637e39ed6477df96e390eef3d5230d35d9a4e179fb5b7658b06`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft-codex-repair-v4-final.jsonl，第 13 行；源 SHA256 `7309fa42140db57b43b38b4223b922fd04c8fa90d53138b79036bc8d15778e2f`。

**题干**

求由曲线 $y=x$ 与 $y=x^2$ 围成的区域绕 $x$ 轴旋转所得旋转体的体积。

**过程**

两曲线交点:$x=0,1$。区域绕 $x$ 轴旋转形成中空的旋转体,用垫圈法:外半径 $R(x)=x$,内半径 $r(x)=x^2$。$V=\pi\int_0^1\left[R(x)^2-r(x)^2\right]dx=\pi\int_0^1(x^2-x^4)\,dx=\pi\left(\frac13-\frac15\right)=\frac{2\pi}{15}$。

**答案原文**

体积为 $\frac{2\pi}{15}$。

## 165. draft-c09-04

内容 SHA256：`33f62a9df55f8b176b747e181a316b6661188551470e2c5a316395402b3444c7`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft-codex-repair-v4-final.jsonl，第 14 行；源 SHA256 `7309fa42140db57b43b38b4223b922fd04c8fa90d53138b79036bc8d15778e2f`。

**题干**

矩形$[0,1]\times[0,2]$绕直线$y=h$旋转，$h\in\mathbb R$。求体积关于$h$的完整分段表达式及所有使体积最小的轴位置。

**过程**

纵截面与$x$无关，实体轴向长度为$1$。若$0\le h\le2$，轴穿过或触及矩形，截面为半径$\max(h,2-h)=1+|h-1|$的圆盘，体积为$\pi(1+|h-1|)^2$。若$h\le0$，为圆环，平方差$(2-h)^2-h^2=4(1-h)$；若$h\ge2$，平方差$h^2-(h-2)^2=4(h-1)$。两外侧可合写$4\pi|h-1|$；在$h=0,2$与圆盘公式同为$4\pi$。内区间公式唯一在$h=1$取最小值$\pi$，外区间体积不小于$4\pi$。因此全局唯一最优轴为$y=1$，最小体积为$\pi$。

**答案原文**

$V(h)=\begin{cases}\pi(1+|h-1|)^2,&0\le h\le2,\\4\pi|h-1|,&h<0\text{ or }h>2.\end{cases}$ 唯一最小轴$y=1$，$V_{\min}=\pi$。

## 166. draft-c09-05

内容 SHA256：`5452d2ce83c126528ed44e293b6557448190cda861dcdb372fb5e6e904567ad3`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-08/draft-codex-repair-v4-final.jsonl，第 15 行；源 SHA256 `7309fa42140db57b43b38b4223b922fd04c8fa90d53138b79036bc8d15778e2f`。

**题干**

区域$D=\{(x,y):0\le x\le3,\ y\in[1,2]\cup[-x,0]\}$绕$x$轴旋转。求其旋转像并集的体积，说明两部分分别旋转后的体积为什么不能直接相加。

**过程**

固定$x$，上部旋转像为半径区间$[1,2]$的圆环，下部为半径区间$[0,x]$的圆盘。若$0\le x\le1$，除边界外不重叠，截面积为$\pi(x^2+3)$；若$1\le x\le2$，并集填满半径$2$的圆盘，面积$4\pi$；若$2\le x\le3$，并集为半径$x$的圆盘，面积$\pi x^2$。所以$V=\pi\int_0^1(x^2+3)dx+4\pi\int_1^2dx+\pi\int_2^3x^2dx=\pi(10/3+4+19/3)=41\pi/3$。独立用容斥验证：上部体积$9\pi$、下部体积$9\pi$；交叠体积$\pi\int_1^2(x^2-1)dx+3\pi\int_2^3dx=13\pi/3$，故并集为$18\pi-13\pi/3=41\pi/3$。直接相加会重复计算交叠旋转像。

**答案原文**

$V=41\pi/3$；两旋转像交叠体积$13\pi/3$，不能直接将$9\pi$与$9\pi$相加。

## 167. draft-c10-01

内容 SHA256：`51ee0e4aea9713f79c8b3b4c99f2c306b075c0adba2ed2bb6d6de9d1ebffb5a3`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft-codex-repair-v4-final.jsonl，第 1 行；源 SHA256 `9142001c7dce29061273bbf49596001de7f74defa40e7eb26aa3d262ced6f003`。

**题干**

定义$u_{2k-1}=1/k$、$u_{2k}=-1/k+2^{-k}$（$k\ge1$）。求$\sum_{n\ge1}u_n$的和与敛散类型，并判断绝对值单调递减是否为交错级数收敛的必要条件。

**过程**

由$2^k>k$知偶项为负，奇项为正。精确部分和为$S_{2N}=1-2^{-N}$、$S_{2N+1}=1-2^{-N}+1/(N+1)$，均趋于$1$。而$\sum_{n=1}^{2N}|u_n|=2\sum_{k=1}^N1/k-1+2^{-N}\to\infty$，所以条件收敛。$|u_4|=1/4<|u_5|=1/3$，绝对值不单调；莱布尼茨的单调条件是充分条件，并非必要条件。

**答案原文**

条件收敛，和$1$；绝对值不单调，单调性不是必要条件。

## 168. draft-c10-02

内容 SHA256：`75db880e4c03608a18daf8258b9a3484dd0ed7af76fe30712e880b48ba6e4729`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft-codex-repair-v4-final.jsonl，第 2 行；源 SHA256 `9142001c7dce29061273bbf49596001de7f74defa40e7eb26aa3d262ced6f003`。

**题干**

设$b_n=1/\sqrt{n(n+1)}$，$a_n=b_n+(-1)^n/[n(n+1)]$。证明$a_n>0$、$a_n$不单调，且$\sum_{n\ge1}(-1)^na_n$条件收敛。说明绝对可和扰动为何不破坏交错级数的收敛。

**过程**

$b_n>1/[n(n+1)]$，故$a_n>0$。$b_n$递减趋零，$\sum(-1)^nb_n$由莱布尼茨判别法收敛。扰动项满足$\sum1/[n(n+1)]\le\sum1/n^2<\infty$，故$\sum(-1)^na_n=\sum(-1)^nb_n+\sum1/[n(n+1)]$收敛。对绝对值，$a_n\ge1/(n+1)-1/[n(n+1)]$；前一正项级数发散、后一收敛，因此绝对值级数发散。又$a_4-a_3=\sqrt5/10-\sqrt3/6+2/15>2/10-2/6+2/15=0$，故不单调。一般地，若$\sum(-1)^nb_n$收敛、$\sum|c_n|<\infty$，则$\sum(-1)^n(b_n+c_n)$是两个收敛级数之和。这里的收敛由判别法和绝对可和扰动证明，不用数值试算。

**答案原文**

正振幅不单调，但交错级数条件收敛；绝对可和扰动保持收敛。

## 169. draft-c10-03

内容 SHA256：`e89c63bf297a26bcc8faff976134dfe19b66de72157e08ad6264ade2a0ec3c27`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft-codex-repair-v4-final.jsonl，第 3 行；源 SHA256 `9142001c7dce29061273bbf49596001de7f74defa40e7eb26aa3d262ced6f003`。

**题干**

说明级数 $\sum_{n=1}^{\infty}\frac{(-1)^n(2+(-1)^n)}{n}$ 发散，并解释莱布尼茨判别法为何不能使用。

**过程**

第$2k-1$项为$-1/(2k-1)$，第$2k$项为$3/(2k)$，成对和为$(4k-3)/[2k(2k-1)]\ge1/(2k)$。所以$S_{2N}\ge\frac12\sum_{k=1}^N1/k\to+\infty$；$S_{2N+1}=S_{2N}-1/(2N+1)\to+\infty$。振幅也不递减：$1/(2k-1)<3/(2k)$。因此不能用莱布尼茨判别法，级数发散到$+\infty$。

**答案原文**

级数发散(拆成 $2\sum(-1)^n/n+\sum1/n$,收敛+发散);莱布尼茨判别法因通项绝对值不单调而不可用。

## 170. draft-c10-04

内容 SHA256：`4371134a9cef673197db2062cf67dc4d17ef2914df476e18e2095ebc9d5b49e7`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft-codex-repair-v4-final.jsonl，第 4 行；源 SHA256 `9142001c7dce29061273bbf49596001de7f74defa40e7eb26aa3d262ced6f003`。

**题干**

对$S=\sum_{n\ge1}(-1)^{n-1}/3^n$，求精确余项$R_N=S-S_N$；求使实际误差严格小于$1/2500$的最小$N$，再求只使用莱布尼茨界即可保证该条件的最小$N$。

**过程**

几何级数给$S=1/4$、$S_N=(1-(-1/3)^N)/4$，故$R_N=(-1)^N/(4\cdot3^N)$。实际误差条件等价于$3^N>625$；$3^5=243<625<729=3^6$，最小$N=6$。莱布尼茨界为$|R_N|\le3^{-(N+1)}$，仅依此保证严格小于$1/2500$需$3^{N+1}>2500$；$3^7=2187<2500<6561=3^8$，最小$N=7$。$S_6=182/729$、$R_6=1/2916$，均为精确分数。界给出的充分条件不能冒充实际最小项数。

**答案原文**

$R_N=(-1)^N/(4\cdot3^N)$；实际最小$N=6$，仅用莱布尼茨界的最小$N=7$。

## 171. draft-c10-05

内容 SHA256：`a06b8979c14befe790b6611384b177a14f2729442bd61aa8785b59a6f69afe36`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft-codex-repair-v4-final.jsonl，第 5 行；源 SHA256 `9142001c7dce29061273bbf49596001de7f74defa40e7eb26aa3d262ced6f003`。

**题干**

证明莱布尼茨判别法:若 $a_n$ 单调递减趋于 $0$,则交错级数 $\sum_{n=1}^{\infty}(-1)^{n+1}a_n$ 收敛,且其和 $S$ 满足 $|S-S_N|\le a_{N+1}$。

**过程**

设$a_n\ge0$、$a_{n+1}\le a_n$且$a_n\to0$，$S_N=\sum_{n=1}^N(-1)^{n-1}a_n$。偶部分和递增，奇部分和递减，且$S_{2m}\le S_{2l+1}$对一切$m,l$成立；两序列有界并有极限，差$S_{2N+1}-S_{2N}=a_{2N+1}\to0$，故极限相同，记为$S$。由夹逼，对任意$N$有$0\le(-1)^N(S-S_N)\le a_{N+1}$，所以$|S-S_N|\le a_{N+1}$。该证明只涉及有限部分和及其极限。

**答案原文**

证明见解法(偶子列单调有界、奇子列同极限;余项 $|S-S_N|\le a_{N+1}$)。

## 172. draft-c12-01

内容 SHA256：`7e12e50d46b4d5f4e76678d3a2b933e6e0295afe0f93af01f12e3f2386fafc77`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft-codex-repair-v4-final.jsonl，第 6 行；源 SHA256 `9142001c7dce29061273bbf49596001de7f74defa40e7eb26aa3d262ced6f003`。

**题干**

证明函数项级数 $\sum_{n=1}^{\infty}\frac{\sin nx}{n^2}$ 在 $\mathbb R$ 上一致收敛。

**过程**

用魏尔斯特拉斯 $M$ 判别法:对一切 $x\in\mathbb R$,$\left|\frac{\sin nx}{n^2}\right|\le\frac{1}{n^2}=M_n$,而 $\sum_{n=1}^{\infty}M_n=\sum\frac{1}{n^2}$ 收敛。故级数在 $\mathbb R$ 上一致收敛(且绝对一致收敛)。

**答案原文**

在 $\mathbb R$ 上一致收敛($M$ 判别法,$M_n=\frac{1}{n^2}$)。

## 173. draft-c12-02

内容 SHA256：`bdeeabc55112b409353a22d97a41fb29381b403212148bb6ae16dda1ae906921`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft-codex-repair-v4-final.jsonl，第 7 行；源 SHA256 `9142001c7dce29061273bbf49596001de7f74defa40e7eb26aa3d262ced6f003`。

**题干**

证明 $\sum_{n=0}^{\infty}x^n$ 在 $[-\frac12,\frac12]$ 上一致收敛，并说明在 $(-1,1)$ 上不一致收敛。

**过程**

在$[-1/2,1/2]$上，$|x^n|\le2^{-n}$，由M判别法一致收敛。在$(-1,1)$上点态和为$1/(1-x)$；从$n=0$到$N$的部分和尾项为$x^{N+1}/(1-x)$。对每个固定$N$，令$x\to1^{-}$，尾项趋于$+\infty$，其上确界为$+\infty$，故不一致收敛。

**答案原文**

在 $[-\frac12,\frac12]$ 上一致收敛($M$ 判别法);在 $(-1,1)$ 上不一致收敛($\sup|S_N-S|$ 不趋于 $0$)。

## 174. draft-c12-03

内容 SHA256：`1fcfeaef7fa472f6e96bc983d5b9f478b4d5403b677e692235d723714bf055a6`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft-codex-repair-v4-final.jsonl，第 8 行；源 SHA256 `9142001c7dce29061273bbf49596001de7f74defa40e7eb26aa3d262ced6f003`。

**题干**

证明$\sum_{n\ge1}\sin(nx)/n$在$[\delta,2\pi-\delta]$（$0<\delta<\pi$）上一致收敛，而在$(0,2\pi)$上不一致收敛。不得用其和函数的图像代替证明。

**过程**

几何求和给任意正弦块$|\sum_{n=p}^q\sin(nx)|\le1/|\sin(x/2)|\le1/\sin(\delta/2)$。对权$1/n$作分部求和，得到$|\sum_{n=p}^q\sin(nx)/n|\le1/[p\sin(\delta/2)]$；此界与$x,q$无关，满足一致柯西准则。反之，取$x_N=\pi/(4N)$，对$N+1\le n\le2N$，$\pi/4<nx_N\le\pi/2$，故$\sin(nx_N)\ge\sqrt2/2$且$1/n\ge1/(2N)$，于是该块和不小于$\sqrt2/4$。块和不能一致趋于零，因此在整个开区间不一致收敛。

**答案原文**

远离周期端点的闭区间上一致收敛；在$(0,2\pi)$上不一致收敛。

## 175. draft-c12-04

内容 SHA256：`d4fc043d7787af8d6790ebe0a8147d6afd466693d6f1f23fe4d3f48dfb9aafcf`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft-codex-repair-v4-final.jsonl，第 9 行；源 SHA256 `9142001c7dce29061273bbf49596001de7f74defa40e7eb26aa3d262ced6f003`。

**题干**

固定$0<r<1$。证明$F_r(x)=\sum_{n=0}^{\infty}r^n\cos(nx)$在实轴上一致绝对收敛，求其和函数，并严格求$\int_0^\pi F_r(x)\,dx$。

**过程**

$|r^n\cos(nx)|\le r^n$，几何级数可和，故在实轴上一致绝对收敛。取$\sum r^ne^{inx}=1/(1-re^{ix})$的实部，得$F_r(x)=(1-r\cos x)/(1-2r\cos x+r^2)$；分母为$|1-re^{ix}|^2\ge(1-r)^2>0$。一致收敛允许在$[0,\pi]$逐项积分，常数项贡献$\pi$，每个$n\ge1$的积分$r^n[\sin(nx)/n]_0^\pi=0$，故积分为$\pi$。

**答案原文**

$F_r(x)=\frac{1-r\cos x}{1-2r\cos x+r^2}$，一致绝对收敛，积分$\pi$。

## 176. draft-c12-05

内容 SHA256：`dbeeca3b65f7ddf4ea5e8e96675253e18592b853312687135e41a9d86d297537`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft-codex-repair-v4-final.jsonl，第 10 行；源 SHA256 `9142001c7dce29061273bbf49596001de7f74defa40e7eb26aa3d262ced6f003`。

**题干**

证明函数列 $f_n(x)=n^2x(1-x^2)^n$($0\le x\le1$)逐点收敛于 $0$，但 $\int_0^1f_n(x)\,dx$ 不趋于 $0$；由此说明逐点收敛不足以保证极限与积分交换，并指出一致收敛为何是充分条件。

**过程**

$f_n(x)=n^2x(1-x^2)^n$在$[0,1]$逐点趋于零：端点直接为零，对$0<x<1$令$q=1-x^2<1$，$n^2q^n$的相邻比趋于$q<1$，故趋零。换元$u=1-x^2$给$\int_0^1f_n(x)dx=n^2/[2(n+1)]\ge n/4\to\infty$。由于$f_n\ge0$且区间长度为$1$，$\sup f_n\ge\int f_n\ge n/4$，所以不可能一致趋零，也不能交换极限与积分。

**答案原文**

逐点极限$0$，非一致收敛；$\int_0^1f_n=n^2/[2(n+1)]\to+\infty$，不能交换极限与积分。

## 177. draft-c14-01

内容 SHA256：`c53632e21978c28d6ab22ada5ed0ff1dd12ec1143cc2a70c854506025d26ef4a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft-codex-repair-v4-final.jsonl，第 11 行；源 SHA256 `9142001c7dce29061273bbf49596001de7f74defa40e7eb26aa3d262ced6f003`。

**题干**

求$2\pi$周期函数$f(x)=|\sin x|$的实Fourier展开，证明展开在实轴上一致绝对收敛并确实等于$f$。

**过程**

$f$为偶函数，故$b_n=0$。$a_0=(2/\pi)\int_0^\pi\sin x\,dx=4/\pi$。用积化和差积分可得$a_n=0$（$n$奇），$a_{2k}=-4/[\pi(4k^2-1)]$（$k\ge1$）；在$n=1$时直接积分也为零，不能在含零分母的通式中代入。故展开为$2/\pi-(4/\pi)\sum_{k\ge1}\cos(2kx)/(4k^2-1)$。因$4k^2-1\ge3k^2$，系数绝对可和，由M判别法一致绝对收敛。$f$连续且分段光滑，Dirichlet定理给每点Fourier和等于$f$；端点及尖点的左右值相同，所以也无跳跃取值问题。

**答案原文**

$|\sin x|=\frac2\pi-\frac4\pi\sum_{k\ge1}\frac{\cos(2kx)}{4k^2-1}$，全实轴一致绝对收敛。

## 178. draft-c14-02

内容 SHA256：`d6c4cd4c00418d4302dce4ece567e48b0793870b89dbf574ee948892bf5b8c96`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft-codex-repair-v4-final.jsonl，第 12 行；源 SHA256 `9142001c7dce29061273bbf49596001de7f74defa40e7eb26aa3d262ced6f003`。

**题干**

求$f(x)=x(\pi-x)$在$[0,\pi]$的半区间正弦展开，并说明周期奇延拓的端点值和收敛方式。

**过程**

$b_n=(2/\pi)\int_0^\pi x(\pi-x)\sin(nx)dx$。两次分部积分，端点$f(0)=f(\pi)=0$且$f^{\prime\prime}=-2$，得积分$2[1-(-1)^n]/n^3$，所以$b_n=4[1-(-1)^n]/(\pi n^3)$。故$f(x)=(8/\pi)\sum_{k\ge0}\sin((2k+1)x)/(2k+1)^3$。奇延拓在$0,\pm\pi$左右极限都为零，连续、分段光滑；Dirichlet定理在每点取实际值。系数绝对可和，故周期展开全实轴一致绝对收敛。

**答案原文**

$x(\pi-x)=\frac8\pi\sum_{k\ge0}\frac{\sin((2k+1)x)}{(2k+1)^3}$；端点为零，一致绝对收敛。

## 179. draft-c14-03

内容 SHA256：`d55a0429e604e0f939005cfcf1c4a437a473b6e186ad2b4adffc9fd45a479703`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft-codex-repair-v4-final.jsonl，第 13 行；源 SHA256 `9142001c7dce29061273bbf49596001de7f74defa40e7eb26aa3d262ced6f003`。

**题干**

将$2\pi$周期方波$f(x)=0$（$-\pi<x<0$）、$f(x)=1$（$0<x<\pi$）展开为Fourier级数；跳点$x\in\pi\mathbb Z$处定义$f(x)=0$。说明非跳点及跳点的级数取值。

**过程**

$a_0=\frac1\pi\int_{-\pi}^{\pi}f(x)\,dx=\frac1\pi\int_0^{\pi}1\,dx=1$。$a_n=\frac1\pi\int_0^{\pi}\cos nx\,dx=\frac{\sin n\pi}{n\pi}=0$($n\ge1$)。$b_n=\frac1\pi\int_0^{\pi}\sin nx\,dx=\frac{1-\cos n\pi}{n\pi}=\frac{1-(-1)^n}{n\pi}$,即奇数项 $b_{2k-1}=\frac{2}{(2k-1)\pi}$,偶数项为 $0$。故在非跳点 $f(x)=\frac12+\frac{2}{\pi}\sum_{k=1}^{\infty}\frac{\sin(2k-1)x}{2k-1}$。在间断点 $x=0,\pm\pi$ 处,由狄利克雷定理,级数和为左右极限的平均值 $\frac{0+1}{2}=\frac12$。

**答案原文**

非跳点上$f(x)=\frac12+\frac2\pi\sum_{k\ge0}\frac{\sin((2k+1)x)}{2k+1}$；在$x\in\pi\mathbb Z$，级数和为$1/2$，与任意指定单点值无关。

## 180. draft-c14-04

内容 SHA256：`6b024f39c1d67f557691b7a7ab5c197b3e9e316839cc4c82dd07ac1547c4452b`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft-codex-repair-v4-final.jsonl，第 14 行；源 SHA256 `9142001c7dce29061273bbf49596001de7f74defa40e7eb26aa3d262ced6f003`。

**题干**

设$f(x)=3+2\cos x-\sin(2x)$，$g(x)=f(x-\pi/3)$。求$g$的实Fourier系数，推导一般平移的系数变换，并证明每一频率的$a_n^2+b_n^2$不变。

**过程**

若平移量为$\alpha$，展开加法公式得$a_n^{\prime}=a_n\cos(n\alpha)-b_n\sin(n\alpha)$、$b_n^{\prime}=a_n\sin(n\alpha)+b_n\cos(n\alpha)$，常数项不变。这是二维正交变换，平方相加消去交叉项，得$(a_n^{\prime})^2+(b_n^{\prime})^2=a_n^2+b_n^2$。本题$a_0=6,a_1=2,b_2=-1$，其余为零，代入$\alpha=\pi/3$得到$g(x)=3+\cos x+\sqrt3\sin x+(\sqrt3/2)\cos(2x)+(1/2)\sin(2x)$，有限展开无需收敛交换。

**答案原文**

$g=3+\cos x+\sqrt3\sin x+\frac{\sqrt3}{2}\cos2x+\frac12\sin2x$；各频率系数平方和不变。

## 181. draft-c14-05

内容 SHA256：`f715b7cc32312f5448484a02e07f739beda23ce75e70e6249bc99475f42f40eb`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-09/draft-codex-repair-v4-final.jsonl，第 15 行；源 SHA256 `9142001c7dce29061273bbf49596001de7f74defa40e7eb26aa3d262ced6f003`。

**题干**

令$f(x)=\cos x$，$g(x)=\cos x$（$x\notin2\pi\mathbb Z$），而$g(x)=5$（$x\in2\pi\mathbb Z$）。比较两者的Fourier系数与在$x=0$处的级数和。为什么系数相同不保证处处相同？

**过程**

在一个周期内，两函数只在有限点不同，这些点对积分无贡献，所以Fourier系数完全相同：$a_1=1$，其他系数为零，两者级数均为$\cos x$。在$0$处级数和为$1$，等于左右极限平均值，而$g(0)=5$。Fourier积分无法辨识零测集上的取值；在此例两函数几乎处处相等，却不处处相等。没有连续性等附加条件，不能从系数相同推出逐点相同。

**答案原文**

系数相同，级数均为$\cos x$；在$0$处和$1\ne g(0)=5$。

## 182. draft-c15-01

内容 SHA256：`a914e58188eadd52261102411ca902340ad74e945f647bf1765e104fae500ad2`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft-codex-repair-v4-final.jsonl，第 1 行；源 SHA256 `dc13b53c4401342a342854938bae6a2ffeaa64ea79dab92c4bbb8aaff601976e`。

**题干**

直线$l:(x,y,z)=(1,-2,0)+t(1,0,1)$，$t\in\mathbb R$，平面$\pi:x+y=1$。求直线与平面的锐夹角。

**过程**

直线方向 $d=(1,0,1)$,平面法向量 $n=(1,1,0)$。夹角公式 $\sin\varphi=\frac{|d\cdot n|}{|d|\,|n|}=\frac{|1\times1+0\times1+1\times0|}{\sqrt{2}\times\sqrt{2}}=\frac{1}{2}$,故 $\varphi=\arcsin\frac12=\frac{\pi}{6}$,即 $30^\circ$。

**答案原文**

夹角为 $\frac{\pi}{6}$(即 $30^\circ$)。

## 183. draft-c15-02

内容 SHA256：`9692ac6ecd53ba2c802388c8ed531733d08cd36862c3cb9e9164321b9747053a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft-codex-repair-v4-final.jsonl，第 2 行；源 SHA256 `dc13b53c4401342a342854938bae6a2ffeaa64ea79dab92c4bbb8aaff601976e`。

**题干**

判断直线 $l:\frac{x-1}{1}=\frac{y-2}{2}=\frac{z-3}{-1}$ 与平面 $\pi:x+2y-z=0$ 的位置关系；再判断过点 $(1,1,2)$、方向为 $(1,-1,1)$ 的直线 $l'$ 与平面 $\pi':x+y=0$ 的位置关系。

**过程**

$l$ 的方向 $d=(1,2,-1)$ 与 $\pi$ 的法向量 $n=(1,2,-1)$ 平行($d=n$),故 $l\perp\pi$(直线垂直于平面)。$l'$ 的方向 $d'=(1,-1,1)$ 与 $\pi'$ 的法向量 $n'=(1,1,0)$ 的内积为 $1-1+0=0$,故 $d'\perp n'$,即 $l'\parallel\pi'$;又点 $(1,1,2)$ 代入 $x+y=2\neq0$,不在平面内,故 $l'$ 与 $\pi'$ 平行且不重合。

**答案原文**

$l\perp\pi$(方向平行于法向);$l'\parallel\pi'$ 且不重合($d'\perp n'$ 且所过点不在平面内)。

## 184. draft-c15-03

内容 SHA256：`3d722aa0315f811fbc3503d988c12dd49ef0a9725fd6de2ac9bd91e7e3dfe349`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft-codex-repair-v4-final.jsonl，第 3 行；源 SHA256 `dc13b53c4401342a342854938bae6a2ffeaa64ea79dab92c4bbb8aaff601976e`。

**题干**

求过点 $P(1,2,3)$、法向量位于 $xz$ 平面内、且与方向为 $(1,1,0)$ 的直线成 $30^\circ$ 角的平面方程。

**过程**

法向量为$(a,0,c)\ne0$，直线方向为$(1,1,0)$。线面角为$\pi/6$，所以$|a|/[\sqrt2\sqrt{a^2+c^2}]=1/2$，平方得$a^2=c^2$；若$a=0$则$c=0$矛盾，故可取$a=1$，$c=\pm1$。过$P=(1,2,3)$的两个平面分别为$x+z=4$、$x-z=-2$。两者法向量均使角正弦为$1/2$，故线面锐角均为$\pi/6$。

**答案原文**

两个平面:$x+z=4$ 与 $x-z=-2$。

## 185. draft-c15-04

内容 SHA256：`fd8faabbe2e38bd4bcb1e5e3fcf759674eb796899c3eecc8983b80398f55f89e`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft-codex-repair-v4-final.jsonl，第 4 行；源 SHA256 `dc13b53c4401342a342854938bae6a2ffeaa64ea79dab92c4bbb8aaff601976e`。

**题干**

求直线 $l$：过原点、方向为 $(1,1,1)$ 与平面 $\pi:x+y=0$ 的夹角 $\varphi$；再求 $l$ 在 $\pi$ 上的投影直线的方向，并求 $l$ 与其投影线的夹角 $\theta$，说明 $\theta$ 与 $\varphi$ 的关系。

**过程**

直线方向$d=(1,1,1)$，平面法向量$n=(1,1,0)$。正交投影方向$d_{\parallel}=d-(d\cdot n)/(n\cdot n)n=(0,0,1)$。线面角$\phi\in[0,\pi/2]$满足$\sin\phi=|d\cdot n|/(\|d\|\|n\|)=\sqrt{2/3}$；直线与其非零投影的锐角$\theta$满足$\cos\theta=(d\cdot d_{\parallel})/(\|d\|\|d_{\parallel}\|)=1/\sqrt3$。两角范围相同且$\cos\phi=1/\sqrt3$，故$\phi=\theta$。

**答案原文**

$\phi=\arcsin\sqrt{2/3}$，$\theta=\arccos(1/\sqrt3)$；$\phi=\theta$，方向投影为$(0,0,1)$。

## 186. draft-c15-05

内容 SHA256：`49021b89d96e838620b2ee11dd138461814c163e101893509be7dcd03ff886b1`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft-codex-repair-v4-final.jsonl，第 5 行；源 SHA256 `dc13b53c4401342a342854938bae6a2ffeaa64ea79dab92c4bbb8aaff601976e`。

**题干**

证明直线与平面夹角公式 $\sin\varphi=\frac{|d\cdot n|}{|d|\,|n|}$，并讨论 $d\cdot n=0$ 与 $d\times n=0$ 两个退化分支对应的位置关系及判定方法。

**过程**

设直线为$l=p+td$，平面为$\Pi=\{x:n\cdot x=c\}$，其中$d,n\ne0$。将方向向量正交分解为$d=d_{\parallel}+d_{\perp}$，其中$d_{\perp}=\frac{d\cdot n}{\|n\|^2}n$，$d_{\parallel}=d-\frac{d\cdot n}{\|n\|^2}n$，故$n\cdot d_{\parallel}=0$、$d_{\parallel}\cdot d_{\perp}=0$。若$d_{\parallel}\ne0$，直线与平面的夹角$\varphi\in[0,\pi/2)$为$d$与其平面投影方向的锐角或零角，由直角三角形得$\sin\varphi=\frac{\|d_{\perp}\|}{\|d\|}=\frac{|d\cdot n|}{\|d\|\,\|n\|}$。若$d_{\parallel}=0$，则$d\parallel n$，直线垂直于平面，$\varphi=\pi/2$，上述公式右端为$1$，仍然成立。若$d\cdot n=0$，则$\varphi=0$，且所有$t$都有$n\cdot(p+td)=n\cdot p$；因此$n\cdot p=c$时$l\subset\Pi$，$n\cdot p\ne c$时$l\cap\Pi=\varnothing$且直线与平面平行。若$d\times n=0$，由$d,n\ne0$知$d\cdot n\ne0$；直线垂直于平面，并在唯一参数$t=\frac{c-n\cdot p}{n\cdot d}$处与平面相交。

**答案原文**

$\sin\varphi=\frac{|d\cdot n|}{\|d\|\,\|n\|}$，$\varphi\in[0,\pi/2]$。若$d\cdot n=0$，则$\varphi=0$：$n\cdot p=c$时$l\subset\Pi$，否则$l\cap\Pi=\varnothing$且$l\parallel\Pi$。若$d\times n=0$，则$\varphi=\pi/2$且$l\perp\Pi$，交点为$p+\frac{c-n\cdot p}{n\cdot d}d$。

## 187. draft-c17-01

内容 SHA256：`fcc7e9a6460c2a7f203e3f419c0fb211b2b05dcdff0cc7667c3f379cd18d9ad4`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft-codex-repair-v4-final.jsonl，第 6 行；源 SHA256 `dc13b53c4401342a342854938bae6a2ffeaa64ea79dab92c4bbb8aaff601976e`。

**题干**

求过点 $P(1,-2,3)$ 且以 $n=(2,1,-2)$ 为法向量的平面方程。

**过程**

点法式:$2(x-1)+1(y+2)-2(z-3)=0$,展开得 $2x+y-2z+6=0$。验证:代入 $P$:$2-2-6+6=0$ ✓。

**答案原文**

平面方程为 $2x+y-2z+6=0$。

## 188. draft-c17-02

内容 SHA256：`e6cb092cb13280fa2cb9a221d23c63898e4854dd59b4a1352ef244ea54ecad85`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft-codex-repair-v4-final.jsonl，第 7 行；源 SHA256 `dc13b53c4401342a342854938bae6a2ffeaa64ea79dab92c4bbb8aaff601976e`。

**题干**

求过点 $P(1,1,1)$ 且平行于向量 $a=(1,0,1)$ 与 $b=(0,1,1)$ 的平面方程。

**过程**

平面的法向量可取 $n=a\times b=(1,0,1)\times(0,1,1)=(0\times1-1\times1,\,1\times0-1\times1,\,1\times1-0\times0)=(-1,-1,1)$。由点法式:$-(x-1)-(y-1)+(z-1)=0$,即 $x+y-z=1$。验证:$P$ 满足 $1+1-1=1$ ✓;$a\cdot n=-1+0+1=0$,$b\cdot n=0-1+1=0$,两个方向均在平面内 ✓。

**答案原文**

平面方程为 $x+y-z=1$。

## 189. draft-c17-03

内容 SHA256：`eb927b7c35c47a6c270578afe7253bd870fcf5d600e87403e554985071a85a10`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft-codex-repair-v4-final.jsonl，第 8 行；源 SHA256 `dc13b53c4401342a342854938bae6a2ffeaa64ea79dab92c4bbb8aaff601976e`。

**题干**

求过 $A(1,1,1)$、$B(2,2,2)$ 且平行于 $x$ 轴的平面方程，并说明为什么只用两个共线的点不能确定平面。

**过程**

$\overrightarrow{AB}=(1,1,1)$,$x$ 轴方向 $e=(1,0,0)$。$AB$ 与 $e$ 不平行,两者张成所求平面的方向子空间,法向量 $n=\overrightarrow{AB}\times e=(1,1,1)\times(1,0,0)=(1\times0-1\times0,\,1\times1-1\times0,\,1\times0-1\times1)=(0,1,-1)$。点法式:$0(x-1)+(y-1)-(z-1)=0$,即 $y=z$。验证:$A,B$ 均满足 $y=z$ ✓;方向 $e$ 与 $n$ 正交 ✓。说明:$A,B$ 共线时,两个点只给出一个方向,而空间中过一条定直线的平面有无穷多个(绕该直线旋转),必须再给一个与 $AB$ 不共线的方向或条件才能唯一确定平面。

**答案原文**

平面方程为 $y=z$;共线两点只确定一个方向,过该直线的平面有无穷多个,故不能唯一确定平面。

## 190. draft-c17-04

内容 SHA256：`a0a909ead00acb7fb011f71a0dd333f73921d777b4bc937621d3c666b2f33abc`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft-codex-repair-v4-final.jsonl，第 9 行；源 SHA256 `dc13b53c4401342a342854938bae6a2ffeaa64ea79dab92c4bbb8aaff601976e`。

**题干**

设两相交平面$f_1=x+y+z-1=0$、$f_2=x-y+2z=0$交于直线$l$。给出包含$l$的全部平面，并分类经过给定点$P$的成员；最后求经过$(1,1,1)$的成员。

**过程**

法向量$n_1=(1,1,1)$、$n_2=(1,-1,2)$线性无关。任何包含$l$的平面法向量属于$\operatorname{span}(n_1,n_2)$，在$l$上取一点比较常数项，得全部平面$s f_1+t f_2=0$，$(s,t)\ne(0,0)$，比例$(s:t)$标识同一平面。该齐次表示包含$f_2=0$，不能用$f_1+\lambda f_2$遗漏它。经过$P$需$s f_1(P)+t f_2(P)=0$：若$P\in l$，所有成员都经过$P$；否则一条非零齐次线性约束唯一确定比例。对$P=(1,1,1)$，$f_1(P)=f_2(P)=2$，故$(s:t)=(1:-1)$，平面为$2y-z=1$。

**答案原文**

全部$s f_1+t f_2=0$，$(s:t)\in\mathbb{RP}^1$；$P\in l$时全部，否则唯一；指定点对应$2y-z=1$。

## 191. draft-c17-05

内容 SHA256：`6a58d9a12604facf640fc0bece2f0c96e73d54fa322daae3f0db696a00afe766`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft-codex-repair-v4-final.jsonl，第 10 行；源 SHA256 `dc13b53c4401342a342854938bae6a2ffeaa64ea79dab92c4bbb8aaff601976e`。

**题干**

推导平面的截距式方程，并求过点 $P(1,2,3)$ 且在三坐标轴上的截距都相等且不为零(即平面不过原点)的平面方程。

**过程**

若平面与三轴分别交于$(a,0,0),(0,b,0),(0,0,c)$，其中$abc\ne0$，代入$Ax+By+Cz=D$得$Aa=Bb=Cc=D$。这三个截距点不共线，且其平面不经过原点，故$D\ne0$，除以$D$得到$x/a+y/b+z/c=1$。过$(1,2,3)$且三截距相等为$h\ne0$时，$(1+2+3)/h=1$，得$h=6$，平面$x+y+z=6$。若坐标轴包含于平面或不相交，不能使用三个非零有限截距的假设。

**答案原文**

截距式:$\frac{x}{a}+\frac{y}{b}+\frac{z}{c}=1$($abc\neq0$);$x+y+z=6$。

## 192. draft-c19-01

内容 SHA256：`dec6ac9a126215676e25d46979b5f924b35a05353f3e69af1626d4454ab145e0`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft-codex-repair-v4-final.jsonl，第 11 行；源 SHA256 `dc13b53c4401342a342854938bae6a2ffeaa64ea79dab92c4bbb8aaff601976e`。

**题干**

说明方程 $y^2=2x$ 在空间直角坐标系中表示什么曲面，并指出它与 $xy$ 平面内的曲线 $y^2=2x$ 的区别。

**过程**

方程不含 $z$:若 $(x,y,z)$ 满足 $y^2=2x$,则对任意 $z'$,$(x,y,z')$ 也满足。故该方程表示母线平行于 $z$ 轴的抛物柱面——准线是 $xy$ 平面内的抛物线 $y^2=2x$,过准线上每一点作平行于 $z$ 轴的直线,这些直线的并集即曲面。区别:平面内方程 $y^2=2x$ 表示一条曲线(一维),空间同一方程表示一张曲面(二维,沿 $z$ 方向无限延伸)。

**答案原文**

母线平行于 $z$ 轴的抛物柱面(准线 $y^2=2x$);平面内同方程为曲线,空间中为曲面。

## 193. draft-c19-02

内容 SHA256：`1d4bfa462b9f8047d2c82ec7745f5879b7994c404aa314e840d8da55b1fdd8f4`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft-codex-repair-v4-final.jsonl，第 12 行；源 SHA256 `dc13b53c4401342a342854938bae6a2ffeaa64ea79dab92c4bbb8aaff601976e`。

**题干**

求以 $xy$ 平面内的圆 $x^2+y^2=1$($z=0$)为准线、母线平行于直线 $l$:方向 $(1,1,1)$ 的柱面方程。

**过程**

母线方向$(1,1,1)$，点可写为$(\cos\theta+t,\sin\theta+t,t)$，消去$t$得$(x-z)^2+(y-z)^2=1$；反过来取$t=z$即可恢复基圆与母线，故方程完整。基圆位于$z=0$，母线不垂直基圆平面，是斜圆柱。若在$x+y+z=0$中截取，令正交坐标$u=(x-y)/\sqrt2$、$v=(x+y-2z)/\sqrt6$，则$(x-z)^2+(y-z)^2=u^2+3v^2$，截面为椭圆$u^2+3v^2=1$，半轴$1,1/\sqrt3$，不能称所有正截面均为圆。

**答案原文**

柱面方程为 $(x-z)^2+(y-z)^2=1$。

## 194. draft-c19-03

内容 SHA256：`11e65d1195fc266d388d4581cd459f0de59c9a6a3f1dc43c4e8ed3e6f058c084`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft-codex-repair-v4-final.jsonl，第 13 行；源 SHA256 `dc13b53c4401342a342854938bae6a2ffeaa64ea79dab92c4bbb8aaff601976e`。

**题干**

求柱面 $x^2+y^2=1$ 与平面 $z=2x$ 的交线方程及其在 $xy$ 平面上的投影，并说明该交线是什么曲线。

**过程**

交线为方程组 $\begin{cases}x^2+y^2=1\\ z=2x\end{cases}$。投影到 $xy$ 平面:消去 $z$ 得 $x^2+y^2=1$ 且 $-1\le x\le1$——投影是 $xy$ 平面内的单位圆周。交线本身是圆柱面 $x^2+y^2=1$ 被平面 $z=2x$ 截出的截线,位于该平面内,是椭圆。轴长分析:参数化 $(\cos t,\sin t,2\cos t)$,在平面 $z=2x$ 内取正交基 $e_1=(0,1,0)$ 与 $e_2=\frac{(1,0,2)}{\sqrt5}$(均垂直于法向 $(2,0,-1)$ 且互相正交),则交线坐标为 $(\sin t,\sqrt5\cos t)$,即 $\eta^2+\frac{\xi^2}{5}=1$:沿 $y$ 方向($e_1$)为短轴,半轴长 $1$,全长 $2$;沿 $(1,0,2)$ 方向($e_2$)为长轴,半轴长 $\sqrt5$,全长 $2\sqrt5$。

**答案原文**

交线:$\begin{cases}x^2+y^2=1\\ z=2x\end{cases}$;$xy$ 平面投影为单位圆周;交线为平面 $z=2x$ 内的椭圆(短半轴 $1$ 沿 $y$ 方向,长半轴 $\sqrt5$ 沿 $(1,0,2)$ 方向)。

## 195. draft-c19-04

内容 SHA256：`4902f451e22a13103456aba615f1c39620a11ffd11b5606e0791df32d26212ed`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft-codex-repair-v4-final.jsonl，第 14 行；源 SHA256 `dc13b53c4401342a342854938bae6a2ffeaa64ea79dab92c4bbb8aaff601976e`。

**题干**

分析下列实集合的几何维数，并说明“维数等于三减方程数”需要什么局部条件：$x^2+y^2+z^2=0$；$x^2+y^2=0$；$x^2+y^2=1$；系统$x^2+y^2=1,\ 2x^2+2y^2=2$。

**过程**

前两式由非负平方之和为零，分别给单点$(0,0,0)$（维数$0$）与$z$轴（维数$1$）；第三式给圆柱面（维数$2$）。最后两个方程等价，其集合仍是圆柱面（维数$2$）。单个方程在前三者的零集上梯度分别为零、零、非零；最后系统只有一个独立约束。在$\mathbb R^3$中，对$r$个$C^1$方程，只有在某解附近Jacobian行满秩$r$时，隐函数定理才保证局部维数$3-r$。方程个数不能替代独立性与正则性检查。

**答案原文**

维数依次$0,1,2,2$；满秩正则点才可用$3-r$。

## 196. draft-c19-05

内容 SHA256：`0304a5b5a2362a7b415350852b975ea9d5f7578629ee07ab4fbe746f1526b95a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-10/draft-codex-repair-v4-final.jsonl，第 15 行；源 SHA256 `dc13b53c4401342a342854938bae6a2ffeaa64ea79dab92c4bbb8aaff601976e`。

**题干**

设$F\in C^1(\mathbb R^3)$，$v\ne0$。证明$F(x+tv)=F(x)$对所有$x,t$成立，当且仅当$v\cdot\nabla F(x)=0$处处成立。说明零集何时为正则柱面，为什么“不含某变量”并不自动保证二维曲面。

**过程**

若平移不变，对$t$求导并令$t=0$，得$v\cdot\nabla F(x)=0$。反之，固定$x$，函数$h(t)=F(x+tv)$的导数处处为零，所以$h$恒定。故零集沿$v$的整条直线不变；若零集非空且在零集上$\nabla F\ne0$，则由隐函数定理局部为二维正则曲面，母线为这些直线。若只知道不含$z$，例$F=x^2+y^2$的零集仅为$z$轴，$F=x^2+y^2+1$的零集为空，$F=0$的零集为全空间。必须区分平移不变集合与正则二维柱面。

**答案原文**

平移不变等价于$v\cdot\nabla F\equiv0$；非空且零集上梯度非零时为正则柱面。

## 197. draft-c20-01

内容 SHA256：`234060b45de4c841a21d76184d5ea2fecba5c20697af883e59dbdfad53a2520b`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft-codex-repair-v4-final.jsonl，第 1 行；源 SHA256 `34447f85bb99aa20aaa84d8756a977d97ca51253c62bd82366d6374e9b953dea`。

**题干**

指出方程 $z=x^2-y^2$ 表示的二次曲面类型，并分别说明其与平面 $z=0$、$z=1$、$z=-1$ 的交线形状。

**过程**

类型:双曲抛物面(马鞍面)。截面 $z=0$:$x^2-y^2=0$,即 $y=\pm x$,是两条相交直线。截面 $z=1$:$x^2-y^2=1$,是双曲线(实轴沿 $x$ 方向)。截面 $z=-1$:$y^2-x^2=1$,也是双曲线(实轴沿 $y$ 方向)。

**答案原文**

双曲抛物面;$z=0$ 截面为两条相交直线 $y=\pm x$,$z=1$ 与 $z=-1$ 截面为实轴方向不同的双曲线。

## 198. draft-c20-02

内容 SHA256：`e7c9856c23b7c57d619c4f39f8f715ea81cf41a3a756634d6617dba04e2c325c`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft-codex-repair-v4-final.jsonl，第 2 行；源 SHA256 `34447f85bb99aa20aaa84d8756a977d97ca51253c62bd82366d6374e9b953dea`。

**题干**

用配方法判断方程 $x^2+y^2+z^2-2x-4y+1=0$ 表示什么曲面，并求其中心(球心)与半径。

**过程**

配方:$(x^2-2x)+(y^2-4y)+z^2+1=0$,即 $(x-1)^2-1+(y-2)^2-4+z^2+1=0$,整理得 $(x-1)^2+(y-2)^2+z^2=4$。这是球面,球心为 $(1,2,0)$,半径为 $2$。

**答案原文**

球面,球心 $(1,2,0)$,半径 $2$。

## 199. draft-c20-03

内容 SHA256：`2c3e241d17167111510e12eedfe8be47f74ce9d65f46ba8c3d873d5e5c5cfffe`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft-codex-repair-v4-final.jsonl，第 3 行；源 SHA256 `34447f85bb99aa20aaa84d8756a977d97ca51253c62bd82366d6374e9b953dea`。

**题干**

对曲面$xy+t z^2=1$（$t\in\mathbb R$），给出正交坐标替换并分类全部参数，特别说明$t=0$的秩退化。

**过程**

令$u=(x+y)/\sqrt2$、$v=(-x+y)/\sqrt2$，则$xy=(u^2-v^2)/2$，方程为$u^2/2-v^2/2+t z^2=1$。若$t>0$，正平方有两个、负平方一个，是单叶双曲面；若$t<0$，正平方一个、负平方两个，是双叶双曲面；若$t=0$，$u^2-v^2=2$与$z$无关，是沿$z$方向的双曲柱面，二次型秩由$3$降为$2$。分类依据惯性与正右端，不凭图像或系数符号猜测。

**答案原文**

$t>0$单叶，$t<0$双叶，$t=0$双曲柱面；标准坐标方程$u^2/2-v^2/2+tz^2=1$。

## 200. draft-c20-04

内容 SHA256：`bbf9d1f60969110277caf52611361150b2bccd15ce634b55fcba39070de08c14`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft-codex-repair-v4-final.jsonl，第 4 行；源 SHA256 `34447f85bb99aa20aaa84d8756a977d97ca51253c62bd82366d6374e9b953dea`。

**题干**

椭球$x^2+2y^2+3z^2=1$与平面$x+y+z=t$相交。求截面中心、全部空集或退化情形，以及非退化截面的精确半轴长。

**过程**

记$W=\operatorname{diag}(1,2,3)$，$n=(1,1,1)$。在平面上二次型的最小点为$c=tW^{-1}n/(n^{\mathsf T}W^{-1}n)=(6t/11,3t/11,2t/11)$；$c^{\mathsf T}Wc=6t^2/11$。写$x=c+h$、$n\cdot h=0$，交叉项为零，截面满足$h^{\mathsf T}Wh=1-6t^2/11$。因此$|t|>\sqrt{11/6}$为空，等号为单点$c$，小于时为椭圆。在切向正交基$e=(1,-1,0)/\sqrt2$、$f=(1,1,-2)/\sqrt6$中限制矩阵为$\begin{pmatrix}3/2&-1/(2\sqrt3)\\-1/(2\sqrt3)&5/2\end{pmatrix}$，特征值$2\pm1/\sqrt3$。所以长短半轴依次为$\sqrt{(1-6t^2/11)/(2-1/\sqrt3)}$、$\sqrt{(1-6t^2/11)/(2+1/\sqrt3)}$。

**答案原文**

中心$(6t,3t,2t)/11$；阈值$|t|=\sqrt{11/6}$；椭圆半轴$\sqrt{(1-6t^2/11)/(2\mp1/\sqrt3)}$。

## 201. draft-c20-05

内容 SHA256：`2351d53a8476932d9b5f05794686140ec530f344554215f7c15d594a15261840`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft-codex-repair-v4-final.jsonl，第 5 行；源 SHA256 `34447f85bb99aa20aaa84d8756a977d97ca51253c62bd82366d6374e9b953dea`。

**题干**

用正交变换(旋转)判断方程 $x^2+2xy+y^2+z=0$ 表示的曲面类型。

**过程**

交叉项部分 $x^2+2xy+y^2=(x+y)^2$。作正交变换 $u=\frac{x+y}{\sqrt2}$,$v=\frac{-x+y}{\sqrt2}$,$w=z$(变换矩阵 $\begin{pmatrix}\frac1{\sqrt2}&\frac1{\sqrt2}&0\\-\frac1{\sqrt2}&\frac1{\sqrt2}&0\\0&0&1\end{pmatrix}$ 为正交矩阵且行列式为 $1$,是绕 $z$ 轴的真旋转),则 $x^2+2xy+y^2=2u^2$,方程化为 $2u^2+w=0$,即 $w=-2u^2$。这是母线沿 $v$ 方向的抛物柱面。

**答案原文**

抛物柱面；新坐标满足$w=-2u^2$，母线沿世界坐标方向$(-1,1,0)/\sqrt2$。

## 202. draft-c22-01

内容 SHA256：`8dc82d6278aa1a7a9b1bab4ce521fc870430c74143cc96d7c2b2c2f3acf900c2`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft-codex-repair-v4-final.jsonl，第 6 行；源 SHA256 `34447f85bb99aa20aaa84d8756a977d97ca51253c62bd82366d6374e9b953dea`。

**题干**

验证单叶双曲面 $x^2+y^2-z^2=1$ 是直纹面，并写出其两族直母线。

**过程**

曲面$x^2+y^2-z^2=1$等价于$(x+z)(x-z)=(1+y)(1-y)$。两族直线可完整写成$t(x+z)=s(1+y),\ s(x-z)=t(1-y)$及$t(x+z)=s(1-y),\ s(x-z)=t(1+y)$，其中$(s:t)\in\mathbb{RP}^1$。若$st\ne0$，相乘消去$st$得到曲面方程；若$s=0$，两族分别给$x+z=0,y=1$与$x+z=0,y=-1$；若$t=0$，分别给$y=-1,x-z=0$与$y=1,x-z=0$，也全部位于曲面。两平面的法向量在任何非零参数对下独立，故每个成员确为直线。矩阵$\begin{pmatrix}x+z&1+y\\1-y&x-z\end{pmatrix}$在曲面上秩为$1$且不可能为零；其列空间和行空间分别唯一确定两族参数，故每点各有一条母线。

**答案原文**

两族母线:$\begin{cases}x+z=\lambda(1+y)\\ \lambda(x-z)=1-y\end{cases}$ 与 $\begin{cases}x+z=\mu(1-y)\\ \mu(x-z)=1+y\end{cases}$($\lambda,\mu$ 取扩充实数,含 $\infty$ 对应极限直线 $y=\mp1,x=z$);单叶双曲面是直纹面。

## 203. draft-c22-02

内容 SHA256：`da607350c3eed839a70a407bf4af638f5d5dc0b9741316b3034559c2fef039a3`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft-codex-repair-v4-final.jsonl，第 7 行；源 SHA256 `34447f85bb99aa20aaa84d8756a977d97ca51253c62bd82366d6374e9b953dea`。

**题干**

证明球面 $x^2+y^2+z^2=1$ 不是直纹面。

**过程**

任一直线与球面至多有两个交点:设直线 $l(t)=p+td$($d\neq0$),代入球面方程得 $(p_1+td_1)^2+(p_2+td_2)^2+(p_3+td_3)^2=1$,即 $|d|^2t^2+2(p\cdot d)t+(|p|^2-1)=0$。因二次项系数 $|d|^2>0$,这是真正的二次方程,至多有两个实根;该二次多项式不可能恒为零(二次项系数非零)。故球面不含任何整条直线,即球面上不存在母线,球面不是直纹面。

**答案原文**

球面不是直纹面:任一直线与球面至多交于两点,球面不含整条直线。

## 204. draft-c22-03

内容 SHA256：`6bba76a4748e883a752e3b0e8701e8c4e15cafe83a21a94ce5799f73d6ebdcdb`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft-codex-repair-v4-final.jsonl，第 8 行；源 SHA256 `34447f85bb99aa20aaa84d8756a977d97ca51253c62bd82366d6374e9b953dea`。

**题干**

求三次曲面$z=xy^2$上全部实直线，并判断每个点通过几条母线。

**过程**

设$p=(x_0,y_0,x_0y_0^2)$，方向$d=(a,b,c)\ne0$，将$p+td$代入。比较$t^3,t^2,t$系数得$ab^2=0$、$2ay_0b+x_0b^2=0$、$c=ay_0^2+2x_0y_0b$。若$b=0$，则$c=ay_0^2$且$a\ne0$，得到全部固定$y=v$的直线$(u,v,uv^2)$。若$b\ne0$，第一式给$a=0$，第二式给$x_0=0$，第三式给$c=0$，仅得到$y$轴$(0,u,0)$。前述直线全都满足曲面，故无遗漏。$x\ne0$的点只过一条固定$y$母线；$x=0$的曲面点同时过该母线和$y$轴，恰有两条。

**答案原文**

全部直线为$(u,v,uv^2)$（$v$固定）及$(0,u,0)$；$x\ne0$过一条，$x=0$过两条。

## 205. draft-c22-04

内容 SHA256：`5fc4465ecaac28271c740665357a2ceb160234b40fcfc2edc916205c37ed76b1`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft-codex-repair-v4-final.jsonl，第 9 行；源 SHA256 `34447f85bb99aa20aaa84d8756a977d97ca51253c62bd82366d6374e9b953dea`。

**题干**

设实二次曲面$F(x)=x^{\mathsf T}Ax+2b^{\mathsf T}x+c=0$，$A=A^{\mathsf T}$。证明$p+td$（$d\ne0$）整条直线在曲面上的充要条件，并据此说明正定或负定$A$为何不允许母线。

**过程**

精确展开$F(p+td)=F(p)+2t(Ap+b)^{\mathsf T}d+t^2d^{\mathsf T}Ad$。它对所有实$t$为零，当且仅当三个系数全为零，即$F(p)=0$、$(Ap+b)^{\mathsf T}d=0$、$d^{\mathsf T}Ad=0$。充分性由代回恒等式立即成立。若$A$正定或负定，对$d\ne0$均有$d^{\mathsf T}Ad\ne0$，故没有整条母线；半定或不定时还必须核对点与混合项条件，存在零二次值方向本身并不充分。

**答案原文**

$F(p)=0$、$(Ap+b)^{\mathsf T}d=0$、$d^{\mathsf T}Ad=0$三条件充要；定号型没有母线。

## 206. draft-c22-05

内容 SHA256：`32b0b63244c7b38b1e548f316174d7b0ac85c9226af8f8e1bef76997a8bf83ea`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft-codex-repair-v4-final.jsonl，第 10 行；源 SHA256 `34447f85bb99aa20aaa84d8756a977d97ca51253c62bd82366d6374e9b953dea`。

**题干**

证明双叶双曲面 $x^2+y^2-z^2=-1$ 不是直纹面。

**过程**

若双叶双曲面$x^2+y^2-z^2=-1$含直线$p+td$，$d\ne0$，比较系数有$p_1^2+p_2^2=p_3^2-1$、$d_1^2+d_2^2=d_3^2$及$p_1d_1+p_2d_2=p_3d_3$。若$d_3=0$，则$d_1=d_2=0$矛盾，故$d_3^2>0$。由Cauchy不等式，$(p_3d_3)^2\le(p_3^2-1)d_3^2<p_3^2d_3^2$，矛盾。因此不存在母线。

**答案原文**

双叶双曲面不是直纹面:假设整条直线在曲面上,多项式恒零给出三个系数方程,由柯西不等式导出 $|p_3d_3|<|p_3d_3|$ 的矛盾(证明见解法)。

## 207. draft-c23-01

内容 SHA256：`bf4616e78e3f96301cee84242ffd95dbd6565475052f5880e025a691de9b1b6c`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft-codex-repair-v4-final.jsonl，第 11 行；源 SHA256 `34447f85bb99aa20aaa84d8756a977d97ca51253c62bd82366d6374e9b953dea`。

**题干**

求等距变换 $T(x)=Ax+b$ 的逆变换，其中 $A=\begin{pmatrix}0&1&0\\-1&0&0\\0&0&1\end{pmatrix}$，$b=(1,2,3)$。

**过程**

$A$ 为正交矩阵,逆变换为 $T^{-1}(x)=A^{\mathsf T}x-A^{\mathsf T}b$。$A^{\mathsf T}=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix}$,$A^{\mathsf T}b=(0-2,\ 1+0,\ 0+3)=(-2,1,3)$。故 $T^{-1}(x)=A^{\mathsf T}x-(-2,1,3)=A^{\mathsf T}x+(2,-1,-3)$。验证:$T(T^{-1}(x))=A(A^{\mathsf T}x-A^{\mathsf T}b)+b=x-b+b=x$ ✓。

**答案原文**

$T^{-1}(x)=A^{\mathsf T}x+(2,-1,-3)$,即 $T^{-1}(x,y,z)=(-y+2,\,x-1,\,z-3)$。

## 208. draft-c23-02

内容 SHA256：`0f5680db032e359c7c85e94a9b90528b9b20956acec90a1c64df9cd641ee9a2c`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft-codex-repair-v4-final.jsonl，第 12 行；源 SHA256 `34447f85bb99aa20aaa84d8756a977d97ca51253c62bd82366d6374e9b953dea`。

**题干**

证明:若 $A$ 为正交矩阵,则等距变换 $T(x)=Ax+b$ 保持任意两点间的距离,即 $\|T(x)-T(y)\|=\|x-y\|$。

**过程**

$\|T(x)-T(y)\|=\|(Ax+b)-(Ay+b)\|=\|A(x-y)\|$。由正交矩阵的性质 $\|Au\|^2=(Au)^{\mathsf T}(Au)=u^{\mathsf T}A^{\mathsf T}Au=u^{\mathsf T}u=\|u\|^2$,故 $\|A(x-y)\|=\|x-y\|$,距离保持不变。

**答案原文**

证明见解法(核心:$\|Au\|^2=u^{\mathsf T}A^{\mathsf T}Au=u^{\mathsf T}u$)。

## 209. draft-c23-03

内容 SHA256：`0667d29d2cc3903388fbd8e86fc87a0caac4d2648a247419c5ae86abdbcfe9aa`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft-codex-repair-v4-final.jsonl，第 13 行；源 SHA256 `34447f85bb99aa20aaa84d8756a977d97ca51253c62bd82366d6374e9b953dea`。

**题干**

分析等距变换$T(x,y,z)=(x+2,4-y,z)$：说明其几何类型，求固定点集合、逆变换及$T^2$，并证明它保持距离。

**过程**

线性部分$A=\operatorname{diag}(1,-1,1)$满足$A^{\mathsf T}A=I$，故两点之差的长度保持。$T$是关于$y=2$的反射，再沿该平面平移$(2,0,0)$，为滑移反射。固定点需$x+2=x$，不可能，故固定点集合为空。反解得$T^{-1}(u,v,w)=(u-2,4-v,w)$，复合得$T^2(x,y,z)=(x+4,y,z)$。它虽反转定向，却不是具有固定平面的单纯反射。

**答案原文**

滑移反射，无固定点；$T^{-1}=(x-2,4-y,z)$，$T^2=(x+4,y,z)$，保持距离。

## 210. draft-c23-04

内容 SHA256：`326ed0d88b06f18e493f3c26fa65249ea41c5b00b1accaee25e9ba824e01fe0d`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft-codex-repair-v4-final.jsonl，第 14 行；源 SHA256 `34447f85bb99aa20aaa84d8756a977d97ca51253c62bd82366d6374e9b953dea`。

**题干**

取单位法向量$n=(2,-1,2)/3$，两平面$n\cdot x=1$、$n\cdot x=5/2$。求先关于前者、再关于后者反射的复合，说明逆序、固定点和两平面间距。

**过程**

记$R_a(x)=x-2(n\cdot x-a)n$，因$\|n\|=1$，$n\cdot R_a(x)=2a-n\cdot x$。所以$R_bR_a(x)=x+2(b-a)n$。代入$a=1,b=5/2$，复合为$x+(2,-1,2)$，是非零平移，故没有固定点；逆序为$x-(2,-1,2)$，正是逆变换。单位法向量使平面距离等于$|b-a|=3/2$，平移距离为$3$。

**答案原文**

复合$x\mapsto x+(2,-1,2)$；逆序反向平移，无固定点，平面间距$3/2$。

## 211. draft-c23-05

内容 SHA256：`a87897a5368b33f21c125bfa1da4b979dfff5e8e7449ba786ab43a630e10d5f2`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-11/draft-codex-repair-v4-final.jsonl，第 15 行；源 SHA256 `34447f85bb99aa20aaa84d8756a977d97ca51253c62bd82366d6374e9b953dea`。

**题干**

把等距变换 $T(x)=Ax+b$ 分解为绕某轴的旋转与沿该轴平移的复合(螺旋运动),其中 $A=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix}$(绕 $z$ 轴旋转 $90^\circ$),$b=(1,2,3)$。

**过程**

旋转轴方向 $v=(0,0,1)$。把 $b$ 分解为沿轴分量与垂直分量:$b_\parallel=(b\cdot v)v=(0,0,3)$,$b_\perp=b-b_\parallel=(1,2,0)$。在 $v^\perp$ 上解 $(I-A)p=b_\perp$:$I-A=\begin{pmatrix}1&1&0\\-1&1&0\\0&0&0\end{pmatrix}$,方程 $p_1+p_2=1$,$-p_1+p_2=2$,解得 $p_1=-\frac12,p_2=\frac32$;取 $p=(-\frac12,\frac32,0)$。则 $T(x)=A(x-p)+p+b_\parallel$:验证右端 $=Ax+(I-A)p+(0,0,3)=Ax+(1,2,0)+(0,0,3)=Ax+b=T(x)$ ✓。故 $T$ 是「绕过点 $p$、平行于 $z$ 轴的直线旋转 $90^\circ$」与「沿 $z$ 轴平移 $(0,0,3)$」的复合(螺旋运动)。

**答案原文**

$T=$ 绕过 $p=(-\frac12,\frac32,0)$ 且平行于 $z$ 轴的直线旋转 $90^\circ$,复合沿 $z$ 轴平移 $(0,0,3)$。

## 212. draft-c24-01

内容 SHA256：`a67734ab13f1b7de7657660ad1cbf140ec20e96e2ca6c0d2158b44b8eae8f169`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft-codex-repair-v6.jsonl，第 1 行；源 SHA256 `acc81053013232ca4b5653b7326696832530cde1a4d620588ddd2dd6da329e89`。

**题干**

解释剪切变换 $\begin{cases}x'=x+2y\\ y'=y\end{cases}$ 对单位正方形 $[0,1]\times[0,1]$ 的几何作用，并求像的面积。

**过程**

$A=\begin{pmatrix}1&2\\0&1\end{pmatrix}$给$(x,y)\mapsto(x+2y,y)$。单位正方形四顶点依次变为$(0,0),(1,0),(3,1),(2,1)$；水平边方向仍为$(1,0)$，原竖直边方向变为$(2,1)$，不再竖直。像是平行四边形，面积乘以$|\det A|=1$，故面积仍为$1$。

**答案原文**

单位正方形映为平行四边形(顶点 $(0,0),(1,0),(2,1),(3,1)$),面积为 $1$(不变)。

## 213. draft-c24-02

内容 SHA256：`b9594c513d9ae4eb8f44c3fa6699980ab8c872b09e384fa84a0aabc8009e1fdd`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft-codex-repair-v6.jsonl，第 2 行；源 SHA256 `acc81053013232ca4b5653b7326696832530cde1a4d620588ddd2dd6da329e89`。

**题干**

仿射映射$T(x,y)=(1+x+y,-1+2x+2y)$作用于单位圆$x^2+y^2=1$。求完整像集和每个像点在圆上的原像数，说明为什么不能使用可逆仿射的椭圆结论。

**过程**

记$t=x+y$，由$(x-y)^2=2-t^2\ge0$，$|t|\le\sqrt2$。反过来对该区间任意$t$，取$(x,y)=((t+s)/2,(t-s)/2)$、$s=\pm\sqrt{2-t^2}$，便有$x^2+y^2=1$。故完整像为线段$\{(1+t,-1+2t):|t|\le\sqrt2\}$；内部像点有两个不同圆上原像，端点各有一个，线段外没有。线性部分秩为$1$、行列式为零，圆的二维仿射坐标不能反解为可逆椭圆。

**答案原文**

像为上述闭线段；内部两原像、端点一原像、外部零原像。

## 214. draft-c24-03

内容 SHA256：`c8d30cc0513aa488f87b90b528ac46dbd936957a4b0d84bfece1dbaa6971e22a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft-codex-repair-v6.jsonl，第 3 行；源 SHA256 `acc81053013232ca4b5653b7326696832530cde1a4d620588ddd2dd6da329e89`。

**题干**

设$T_t(x)=A_tx+b$，$A_t=\begin{pmatrix}1&2\\t&t^2\end{pmatrix}$，$t\in\mathbb R$。求可逆参数及逆矩阵，并在每个奇异参数下给整个平面像、相容条件与全部纤维。

**过程**

$\det A_t=t(t-2)$，故$t\ne0,2$时可逆，逆为$[t(t-2)]^{-1}\begin{pmatrix}t^2&-2\\-t&1\end{pmatrix}$。记像点为$(u,v)$，$s=u-b_1$。$t=0$时像为$b+\operatorname{span}(1,0)$，条件$v=b_2$；$t=2$时像为$b+\operatorname{span}(1,2)$，条件$v-b_2=2s$。两奇异参数下，满足条件的全部原像都是$(s-2r,r)$，$r\in\mathbb R$；不满足条件则无原像。核方向为$(-2,1)$，两种奇异像方向不同，不能只检查一个退化值。

**答案原文**

可逆$t\notin\{0,2\}$；逆如上；奇异像与全部纤维如上。

## 215. draft-c24-04

内容 SHA256：`c70ae57c4f97be3c5200dd9fbde8e47db499d0e030f4c72471f2880a7958d822`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft-codex-repair-v6.jsonl，第 4 行；源 SHA256 `acc81053013232ca4b5653b7326696832530cde1a4d620588ddd2dd6da329e89`。

**题干**

未知仿射映射将$(0,0),(1,0),(0,1)$依次映到$(1,-1),(3,0),(0,2)$。求映射、原三角形的像面积与像重心，以及直线$x+y=1$的像方程。

**过程**

原点像给$b=(1,-1)$，另两像减$b$给矩阵列$(2,1)$、$(-1,3)$，故$T(x)=Ax+b$、$A=\begin{pmatrix}2&-1\\1&3\end{pmatrix}$，$\det A=7$。原三角形面积$1/2$，像面积$7/2$。仿射保平均，原重心$(1/3,1/3)$像为$(4/3,1/3)$，与三个像顶点平均一致。直线点$(t,1-t)$像为$(3t,2-2t)$，故$2u+3v=6$；反过来该方程的任意点取$t=u/3$即可得到，故像方程无额外点。

**答案原文**

$A=\begin{pmatrix}2&-1\\1&3\end{pmatrix}$、$b=(1,-1)$；面积$7/2$，重心$(4/3,1/3)$，像直线$2u+3v=6$。

## 216. draft-c24-05

内容 SHA256：`26c5ba31f6af192d69dda30ae759f84d5b5e1f935a48cf0bd15a7eb61f758aed`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft-codex-repair-v6.jsonl，第 5 行；源 SHA256 `acc81053013232ca4b5653b7326696832530cde1a4d620588ddd2dd6da329e89`。

**题干**

证明可逆仿射变换 $T(x)=Ax+b$ 把直线映成直线、把平行直线映成平行直线、保持共线三点的简单比，并说明圆在一般仿射变换下为何变成椭圆。

**过程**

直线:设直线 $l:p+td$,则像为 $T(p+td)=Ap+b+tAd$,仍是直线(方向 $Ad$,$A$ 可逆故 $Ad\neq0$)。平行线:两条平行直线有相同方向 $d$,像的方向同为 $Ad$,故仍平行。简单比:设共线三点 $A,B,C$ 满足 $C=A+\lambda(B-A)$,则 $T(C)=T(A)+\lambda(T(B)-T(A))$,分比 $\lambda$ 不变。圆→椭圆:单位圆上点 $u$ 满足 $u^{\mathsf T}u=1$;其像 $x=Au+b$ 满足 $(A^{-1}(x-b))^{\mathsf T}(A^{-1}(x-b))=1$,即 $(x-b)^{\mathsf T}(A^{-1})^{\mathsf T}A^{-1}(x-b)=1$。矩阵 $(A^{-1})^{\mathsf T}A^{-1}$ 对称正定,这是中心在 $b$ 的椭圆方程——一般仿射变换不保圆(仅当 $A$ 为正交矩阵乘常数时才保圆)。

**答案原文**

证明见解法(直线/平行/简单比均保持;圆的像为对称正定二次型 $=1$,即椭圆)。

## 217. draft-c25-01

内容 SHA256：`952a499ee435c943d0a021c926830e4ed1d4b3cef3c24bdfead33e9160ea43cd`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft-codex-repair-v6.jsonl，第 6 行；源 SHA256 `acc81053013232ca4b5653b7326696832530cde1a4d620588ddd2dd6da329e89`。

**题干**

分类圆锥$x^2+y^2=z^2$与过顶点平面$z=ax$（$a\in\mathbb R$）的实交集，并给所有非单点分支的完整参数式。

**过程**

代入得$y^2=(a^2-1)x^2$。若$|a|<1$，两边符号迫使$x=y=z=0$，仅顶点。若$|a|=1$，$y=0,z=ax$，是一条直线$(t,0,at)$。若$|a|>1$，分解为两直线$(t,\pm\sqrt{a^2-1}t,at)$；它们不同且只在顶点相交。每个参数$t$取全部实数，代回原方程验证，分类无遗漏。

**答案原文**

$|a|<1$单点，$|a|=1$一条母线，$|a|>1$两条母线；参数式如上。

## 218. draft-c25-02

内容 SHA256：`6855d9fabc118bdedba3a9d76c9f6e0f085f5e2a2aa44972a05cdcf632b84adb`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft-codex-repair-v6.jsonl，第 7 行；源 SHA256 `acc81053013232ca4b5653b7326696832530cde1a4d620588ddd2dd6da329e89`。

**题干**

求两圆柱面 $x^2+y^2=1$ 与 $y^2+z^2=1$ 的交线的参数方程，并说明交线由几支组成、在何处相接。

**过程**

由第一个柱面取 $x=\cos t$,$y=\sin t$。代入第二个柱面:$z^2=1-y^2=1-\sin^2t=\cos^2t$,故 $z=\pm\cos t$。交线由两支组成:$l_1:(\cos t,\sin t,\cos t)$ 与 $l_2:(\cos t,\sin t,-\cos t)$。两支在 $\cos t=0$ 处相接,即点 $(0,1,0)$ 与 $(0,-1,0)$。

**答案原文**

两支:$l_1:(\cos t,\sin t,\cos t)$ 与 $l_2:(\cos t,\sin t,-\cos t)$,在 $(0,\pm1,0)$ 处相接。

## 219. draft-c25-03

内容 SHA256：`ba525e8e8711b9d3f2d54162ca1bb04c4dd1874752f6be77bf9b7fff9c73629e`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft-codex-repair-v6.jsonl，第 8 行；源 SHA256 `acc81053013232ca4b5653b7326696832530cde1a4d620588ddd2dd6da329e89`。

**题干**

求圆锥面 $x^2+y^2=z^2$ 与平面 $z=1+y$ 的交线的参数方程，并判断该交线是什么曲线。

**过程**

令 $x=t$。由 $z=1+y$ 得 $z=1+y$,代入锥面方程:$t^2+y^2=(1+y)^2$,即 $t^2=1+2y$,$y=\frac{t^2-1}{2}$,故 $z=1+\frac{t^2-1}{2}=\frac{t^2+1}{2}$。参数方程:$(t,\frac{t^2-1}{2},\frac{t^2+1}{2})$。验证:消去参数得 $x^2=2y+1$ 且 $z=1+y$,它是平面 $z=1+y$ 内的抛物线($y=\frac{x^2-1}{2}$)。

**答案原文**

交线为抛物线:$(t,\frac{t^2-1}{2},\frac{t^2+1}{2})$,即 $\begin{cases}y=\frac{x^2-1}{2}\\ z=1+y\end{cases}$。

## 220. draft-c25-04

内容 SHA256：`13dbf148ee41e5ee07437c7ed662dd0783e54fce865bfa47e0353e5a6f3d05fd`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft-codex-repair-v6.jsonl，第 9 行；源 SHA256 `acc81053013232ca4b5653b7326696832530cde1a4d620588ddd2dd6da329e89`。

**题干**

求柱面$x^2+y^2=4$与$z=x^2$的完整交线参数式，并证明交线不包含于任何平面。

**过程**

圆柱约束给$x=2\cos t,y=2\sin t$，另一个约束给$z=4\cos^2t$，故完整交线为$(2\cos t,2\sin t,4\cos^2t)$，$0\le t<2\pi$。若整条交线在$Ax+By+Cz=D$中，则$2A\cos t+2B\sin t+2C\cos2t+(2C-D)=0$对所有$t$成立。对$1,\cos t,\sin t,\cos2t$分别积分正交消去，得$A=B=C=D=0$，这不是平面方程，矛盾。因此是非平面闭交线。

**答案原文**

参数$(2\cos t,2\sin t,4\cos^2t)$，$0\le t<2\pi$；交线非平面。

## 221. draft-c25-05

内容 SHA256：`98c4fb5f7e49698dcdc983118a419a211996814b9904a54525a47c78a2536456`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft-codex-repair-v6.jsonl，第 10 行；源 SHA256 `acc81053013232ca4b5653b7326696832530cde1a4d620588ddd2dd6da329e89`。

**题干**

求球$x^2+y^2+z^2=1$与抛物柱面$y=x^2$的实交线，给参数域、分支连接关系，证明交线正则且非平面。

**过程**

置$x=t$，则$y=t^2$、$z=\pm\sqrt{1-t^2-t^4}$。根号非负等价于$|t|\le r=\sqrt{(\sqrt5-1)/2}$。两图形弧在$t=\pm r$的点$(\pm r,r^2,0)$连接，合为一条闭曲线，不能把正负图形弧误称为两个连通分量。正则性由梯度$(2t,2t^2,2z)$与$(-2t,1,0)$线性无关证明：$z\ne0$时明显；$z=0$时$t\ne0$，若成比例，第一坐标给比例$-1$而第二要求$2t^2=-1$，不可能。根号图形在端点不能充当光滑参数，可在端点改用$z$及$x=\pm\sqrt{(-1+\sqrt{5-4z^2})/2}$作为局部参数。若整条曲线在$Ax+By+Cz=D$中，比较同$t$的正负$z$得$C=0$；继而$At+Bt^2-D$在区间恒零，得$A=B=D=0$，矛盾。

**答案原文**

两弧$(t,t^2,\pm\sqrt{1-t^2-t^4})$，$|t|\le\sqrt{(\sqrt5-1)/2}$；连接为一条正则非平面闭曲线。

## 222. draft-c26-01

内容 SHA256：`47ceec5eb77e58baf845743ab79cd61f13271ed22073a7ecb05fbb14dd318bd8`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft-codex-repair-v6.jsonl，第 11 行；源 SHA256 `acc81053013232ca4b5653b7326696832530cde1a4d620588ddd2dd6da329e89`。

**题干**

令$n=(1,2,-1)$、$d=(1,1,0)$，定义$P(x)=x-(n\cdot x)d/3$。求矩阵、核与像，证明其为沿$d$投影到$n\cdot x=0$的斜投影，判断是否为Euclidean正交投影。

**过程**

$n\cdot d=3$，所以$Pd=0$且$n\cdot Px=0$；对$n\cdot x=0$的向量有$Px=x$。因此像为$n^{\perp}$，核为$\operatorname{span}(d)$，$P^2=P$，秩$2$。矩阵为$\begin{pmatrix}2/3&-2/3&1/3\\-1/3&1/3&1/3\\0&0&1\end{pmatrix}$。核方向$d$不平行法向量$n$，矩阵也不对称，故不是Euclidean正交投影；分解$x=Px+(n\cdot x)d/3$唯一，说明投影方向。

**答案原文**

$\ker P=\operatorname{span}(1,1,0)$，$\operatorname{im}P=n^{\perp}$，$P^2=P$；斜投影而非Euclidean正交投影。

## 223. draft-c26-02

内容 SHA256：`5643915c1ebb53d2adadc52ea61c0926c14765e904ea101c5df0908f46f88c00`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft-codex-repair-v6.jsonl，第 12 行；源 SHA256 `acc81053013232ca4b5653b7326696832530cde1a4d620588ddd2dd6da329e89`。

**题干**

分类所有保持两条坐标轴各自不变、并将单位圆映到自身的实线性映射$A:\mathbb R^2\to\mathbb R^2$。分别给其固定点集合与定向。

**过程**

两轴各自不变使矩阵为$\operatorname{diag}(a,b)$。单位基向量在圆上，其像也必须在圆上，所以$|a|=|b|=1$；反之这四个对角矩阵均保持整个单位圆。$A=I$固定全平面且保定向；$A=-I$仅固定原点且保定向；$\operatorname{diag}(1,-1)$固定$x$轴并反定向；$\operatorname{diag}(-1,1)$固定$y$轴并反定向。

**答案原文**

仅四个$\operatorname{diag}(\pm1,\pm1)$；固定集合和定向如上。

## 224. draft-c26-03

内容 SHA256：`7c398a4ddec8b816b3e41c624763f1ae5acb5f539102b7296ec3cfc627343b32`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft-codex-repair-v6.jsonl，第 13 行；源 SHA256 `acc81053013232ca4b5653b7326696832530cde1a4d620588ddd2dd6da329e89`。

**题干**

对$A=\begin{pmatrix}1&2\\0&-1\end{pmatrix}$，证明$A^2=I$，求固定线与变号线，判断是否为Euclidean反射。说明线性对合为何不一定是等距变换。

**过程**

$A(x,y)=(x+2y,-y)$，直接再作用给$(x,y)$，所以$A^2=I$。固定向量满足$y=0$，固定线为$x$轴；变号向量满足$x=-y$，变号线为$\operatorname{span}(-1,1)$，两者独立但不垂直。$\|Ae_2\|^2=\|(2,-1)\|^2=5\ne1$，因此不保距离，不是Euclidean平面反射。任意向量唯一分解为这两条线的向量，$A$保持第一分量并将第二变号，是斜分解下的线性对合。

**答案原文**

线性对合，固定线$x$轴、变号线$y=-x$；不等距，不是Euclidean反射。

## 225. draft-c26-04

内容 SHA256：`00b12bcb744f93e439220dbec35d933ce07ab1f7ccb31259e6c8fe935af58ab9`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft-codex-repair-v6.jsonl，第 14 行；源 SHA256 `acc81053013232ca4b5653b7326696832530cde1a4d620588ddd2dd6da329e89`。

**题干**

在$\mathbb R^4$中比较$T(x)=(x_3,x_4,0,0)$与$U(x)=(x_2,x_3,0,0)$。求迭代像维数与最小归零次数，证明它们虽秩相同却不相似，并判断可否对角化。

**过程**

两者像维数均为$2$。$T^2=0$且$T\ne0$，像维数序列为$4,2,0$；$U^2(x)=(x_3,0,0,0)\ne0$、$U^3=0$，像维数为$4,2,1,0$。相似会保持所有幂的秩或最小归零次数，故两者不相似。若一个非零幂零实或复矩阵可对角化，其对角特征值全为零，矩阵只能为零，矛盾。因此两者均不可对角化。相同一次秩不足以描述线性迭代的几何压缩。

**答案原文**

秩均$2$；$T$二次归零，$U$三次归零，不相似，均不可对角化。

## 226. draft-c26-05

内容 SHA256：`5353b82bdeca73f304808a3c9223f02f77a9f4d20ad85d852f832d4351dae1a1`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-12/draft-codex-repair-v6.jsonl，第 15 行；源 SHA256 `acc81053013232ca4b5653b7326696832530cde1a4d620588ddd2dd6da329e89`。

**题干**

设 $A=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$(旋转 $90^\circ$),$B=\begin{pmatrix}2&0\\0&1\end{pmatrix}$(沿 $x$ 方向伸缩)。计算 $AB$ 与 $BA$，并用单位正方形的像说明两者对应的几何作用不同。

**过程**

$AB=\begin{pmatrix}0&-1\\1&0\end{pmatrix}\begin{pmatrix}2&0\\0&1\end{pmatrix}=\begin{pmatrix}0&-1\\2&0\end{pmatrix}$;$BA=\begin{pmatrix}2&0\\0&1\end{pmatrix}\begin{pmatrix}0&-1\\1&0\end{pmatrix}=\begin{pmatrix}0&-2\\1&0\end{pmatrix}$。$AB\neq BA$。几何:单位正方形在 $AB$(先伸缩、后旋转)下:伸缩把顶点映为 $(0,0),(2,0),(2,1),(0,1)$(水平长条),再旋转 $90^\circ$ 得 $(0,0),(0,2),(-1,2),(-1,0)$(竖直长条)。在 $BA$(先旋转、后伸缩)下:旋转得 $(0,0),(0,1),(-1,1),(-1,0)$,再沿 $x$ 方向伸缩得 $(0,0),(0,1),(-2,1),(-2,0)$(水平长条)。两像不同($AB$ 的像为竖直 $1\times2$ 长条,$BA$ 的像为水平 $2\times1$ 长条),故矩阵乘法顺序不可交换,几何上对应「先伸缩后旋转」与「先旋转后伸缩」的不同。

**答案原文**

$AB=\begin{pmatrix}0&-1\\2&0\end{pmatrix}$,$BA=\begin{pmatrix}0&-2\\1&0\end{pmatrix}$,两者不同;$AB$ 的像为竖直长条,$BA$ 的像为水平长条,几何上为「先伸缩后旋转」与「先旋转后伸缩」的差异。

## 227. draft-c27-01

内容 SHA256：`d5efaf81663f659e9fa9ffcffd55ec32ba48c9d46b9ff80c1955b6f85be1078b`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft-codex-repair-v4-final.jsonl，第 1 行；源 SHA256 `37ad744d2e28133f1449fa961a00606ef7982b32aa4969f2b360192fca2090f6`。

**题干**

设$n\ge2$、$u,v\in\mathbb R^n$均非零，$A=I+uv^{\mathsf T}$。用$\alpha=v^{\mathsf T}u$分类其可对角化性并求最小多项式；必须处理$\alpha=0$而$uv^{\mathsf T}\ne0$的情况。

**过程**

记$N=uv^{\mathsf T}\ne0$，则$N^2=\alpha N$。若$\alpha\ne0$，$\ker v^{\mathsf T}$维数$n-1$，$u$不在其中，全空间分解为该超平面与$\operatorname{span}(u)$的直和；$A$分别作用为$1$和$1+\alpha$，两个不同特征值都出现，所以可对角化，最小多项式$(\lambda-1)(\lambda-1-\alpha)$。若$\alpha=0$，$N^2=0$但$N\ne0$，$A$仅有特征值$1$，最小多项式为$(\lambda-1)^2$；若可对角化只能是$I$，与$N\ne0$矛盾。因此非零向量产生的零内积边界导致不可对角化。

**答案原文**

$\alpha\ne0$可对角化，最小多项式$(\lambda-1)(\lambda-1-\alpha)$；$\alpha=0$不可，最小多项式$(\lambda-1)^2$。

## 228. draft-c27-02

内容 SHA256：`81423386740955d424887336d1bb1157ec5c977afc864ef7b047f8a5a56049e4`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft-codex-repair-v4-final.jsonl，第 2 行；源 SHA256 `37ad744d2e28133f1449fa961a00606ef7982b32aa4969f2b360192fca2090f6`。

**题干**

求实矩阵$A=\begin{pmatrix}0&1&0\\0&0&1\\2&1&1\end{pmatrix}$在$\mathbb C$上的对角化，并判断它能否在$\mathbb R$上对角化。

**过程**

特征多项式为$\lambda^3-\lambda^2-\lambda-2=(\lambda-2)(\lambda^2+\lambda+1)$。三根为$2$、$\omega=(-1+i\sqrt3)/2$、$\overline\omega$，互不相同。对每一根，$v_\lambda=(1,\lambda,\lambda^2)^{\mathsf T}$满足$Av_\lambda=\lambda v_\lambda$。取$P=(v_2,v_\omega,v_{\overline\omega})$，Vandermonde行列式为$(\omega-2)(\overline\omega-2)(\overline\omega-\omega)\ne0$，故$P^{-1}AP=\operatorname{diag}(2,\omega,\overline\omega)$。若在实域可对角化，特征多项式必须分裂为实线性因子；而二次因子判别式$-3<0$，所以不能在实域对角化。数域条件不能省略。

**答案原文**

复域可对角化，$P$与$D$如上；实域不可对角化。

## 229. draft-c27-03

内容 SHA256：`693ebf1a679b05d0d44f902f82da2950eadfa6dfe9da151a2c6ae12166925f0f`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft-codex-repair-v4-final.jsonl，第 3 行；源 SHA256 `37ad744d2e28133f1449fa961a00606ef7982b32aa4969f2b360192fca2090f6`。

**题干**

设实矩阵$A$满足$A^3=A$。不用先求坐标特征向量，构造对应特征值$0,1,-1$的谱投影，证明$A$可对角化，并给所有正整数幂。

**过程**

定义$P_0=I-A^2$、$P_+=(A^2+A)/2$、$P_-=(A^2-A)/2$。由$A^3=A$和$A^4=A^2$，直接相乘得三投影各自幂等、两两乘积零、和为$I$，且$AP_0=0,AP_+=P_+,AP_-=-P_-$。所以全空间为三个像的直和；在各像中取基便得到对角化，零维像可省略。又$A^{m+2}=A^m$对$m\ge1$成立，故正奇数幂为$A$，正偶数幂为$A^2$。这依赖多项式恒等式及简单根结构，不是某个二阶矩阵幂的数值替换。

**答案原文**

$P_0=I-A^2,P_\pm=(A^2\pm A)/2$；$A$可对角化，奇正幂$A$、偶正幂$A^2$。

## 230. draft-c27-04

内容 SHA256：`586b15d3d199cefc3c965cce67f8b7afa664cb0abe2cc4d81dafe89e4af28b7b`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft-codex-repair-v4-final.jsonl，第 4 行；源 SHA256 `37ad744d2e28133f1449fa961a00606ef7982b32aa4969f2b360192fca2090f6`。

**题干**

设$A_k=\begin{pmatrix}1&k\\0&2\end{pmatrix}$，$k\in\mathbb R$。求对角化并判断何时能正交对角化，给两特征线的锐夹角精确式。

**过程**

特征值为$1,2$，对应特征向量$e_1=(1,0)$与$(k,1)$。$P=\begin{pmatrix}1&k\\0&1\end{pmatrix}$可逆且$A_kP=P\operatorname{diag}(1,2)$，故所有$k$都可对角化。两特征线夹角$\alpha\in(0,\pi/2]$满足$\cos\alpha=|k|/\sqrt{k^2+1}$，所以仅$k=0$时垂直。实矩阵正交对角化为实对角阵必对称，而$A_k$对称当且仅当$k=0$；故正交对角化也当且仅当$k=0$。

**答案原文**

所有$k$可对角化；正交对角化当且仅当$k=0$；$\alpha=\arccos(|k|/\sqrt{k^2+1})$。

## 231. draft-c27-05

内容 SHA256：`8531504c6de44ff96c4b4a5d12f13d0a3f6782f92fd42b88e06b8336f360cec7`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft-codex-repair-v4-final.jsonl，第 5 行；源 SHA256 `37ad744d2e28133f1449fa961a00606ef7982b32aa4969f2b360192fca2090f6`。

**题干**

证明：若$n$阶矩阵在数域$\mathbb F$内有$n$个互异特征值，则在$\mathbb F$内可对角化。

**过程**

对互异$\lambda_1,\ldots,\lambda_n\in\mathbb F$取非零特征向量$v_i$。用归纳法证明独立：若$\sum_{i=1}^m c_iv_i=0$，施加$A-\lambda_mI$，得到$\sum_{i<m}c_i(\lambda_i-\lambda_m)v_i=0$；由归纳假设和互异性，$c_i=0$（$i<m$），再得$c_m=0$。故$n$个特征向量组成可逆矩阵$P$，$AP=P\operatorname{diag}(\lambda_i)$。数域内有全部特征值的条件不可省略。

**答案原文**

证明见解法(归纳法证明不同特征值的特征向量线性无关,从而构成基)。

## 232. draft-c29-01

内容 SHA256：`c2de91098af0215d7ef7adb19ffa8452449f5f79f91faba22b012d3ace242c0a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft-codex-repair-v4-final.jsonl，第 6 行；源 SHA256 `37ad744d2e28133f1449fa961a00606ef7982b32aa4969f2b360192fca2090f6`。

**题干**

用$f(x)=x^4+4$说明“没有有理根”不等于“在$\mathbb Q[x]$不可约”。给出在$\mathbb Q,\mathbb R,\mathbb C$中的不可约因子，并证明。

**过程**

Sophie Germain恒等式给$x^4+4=(x^2-2x+2)(x^2+2x+2)$。两个二次因子的判别式都是$-4$，在$\mathbb Q$和$\mathbb R$不可约，且实数$x$下$f(x)>0$，所以连实根都没有。复数根为$1\pm i,-1\pm i$，故复域分解为相应四个首一线性因子。无有理根只能排除一次有理因子，不能排除二次因子；四次多项式的可约性不能仅靠有理根检验决定。

**答案原文**

$\mathbb Q,\mathbb R$中分解为$x^2\mp2x+2$；$\mathbb C$中根$\pm1\pm i$；没有有理根但可约。

## 233. draft-c29-02

内容 SHA256：`35cf2318fe7fb15cac4ac94fdb11dea00bf54c57cd79bcd2b86b58321669739b`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft-codex-repair-v4-final.jsonl，第 7 行；源 SHA256 `37ad744d2e28133f1449fa961a00606ef7982b32aa4969f2b360192fca2090f6`。

**题干**

已知 $2+i$ 是实系数多项式 $f(x)=x^3-7x^2+17x-15$ 的一个根，求 $f$ 的全部根。

**过程**

实系数多项式的非实根成对出现:$2-i$ 也是根,故 $f$ 含因子 $(x-(2+i))(x-(2-i))=x^2-4x+5$。用韦达定理或综合除法:设第三根为 $r$,三根之和为 $7$,故 $r=7-(2+i)-(2-i)=3$。验证:$f=(x-3)(x^2-4x+5)$,展开核对:$x^3-4x^2+5x-3x^2+12x-15=x^3-7x^2+17x-15$ ✓。全部根:$3$,$2+i$,$2-i$。

**答案原文**

全部根:$3$,$2+i$,$2-i$。

## 234. draft-c29-03

内容 SHA256：`09eff888f30f2e9335fae1890cfc7c2773f0088c9187385ae36d9f57daee6f69`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft-codex-repair-v4-final.jsonl，第 8 行；源 SHA256 `37ad744d2e28133f1449fa961a00606ef7982b32aa4969f2b360192fca2090f6`。

**题干**

用 $f$ 与 $f'$ 的公因式求多项式 $f(x)=x^4-4x^3+6x^2-4x+1$ 的重根及其重数。

**过程**

$f=x^4-4x^3+6x^2-4x+1=(x-1)^4$，$f^{\prime}=4(x-1)^3$。欧几里得步骤$f-(x-1)f^{\prime}/4=0$，故首一最大公因子为$(x-1)^3$。$f/f_{\mathrm{gcd}}=x-1$给唯一不同根$1$；$f^{(j)}(1)=0$（$j=0,1,2,3$）、$f^{(4)}(1)=24\ne0$，证明重数恰为$4$。

**答案原文**

$f=(x-1)^4$,$x=1$ 是四重根。

## 235. draft-c29-04

内容 SHA256：`4c7e2c5978bc17ff03f971435c2a679244deb62f9f95a52c7fe91eb24229583f`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft-codex-repair-v4-final.jsonl，第 9 行；源 SHA256 `37ad744d2e28133f1449fa961a00606ef7982b32aa4969f2b360192fca2090f6`。

**题干**

求使多项式 $f(x)=x^3-3x+a$ 有重根的参数 $a$ 的值。

**过程**

$f$ 有重根当且仅当 $f$ 与 $f'$ 有公共根。$f'(x)=3x^2-3=3(x-1)(x+1)$,可能的公根为 $x=1$ 或 $x=-1$。$x=1$ 是公根 ⟺ $f(1)=0$,即 $1-3+a=0$,$a=2$;$x=-1$ 是公根 ⟺ $f(-1)=0$,即 $-1+3+a=0$,$a=-2$。故 $a=2$ 或 $a=-2$。验证:$a=2$ 时 $f=x^3-3x+2=(x-1)^2(x+2)$;$a=-2$ 时 $f=x^3-3x-2=(x+1)^2(x-2)$。

**答案原文**

$a=2$ 或 $a=-2$;对应分解 $(x-1)^2(x+2)$ 与 $(x+1)^2(x-2)$。

## 236. draft-c29-05

内容 SHA256：`7bd31b702af3eeb15316aa1ba3d689266673eda118a69b5c7d76622cf22e0ed7`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft-codex-repair-v4-final.jsonl，第 10 行；源 SHA256 `37ad744d2e28133f1449fa961a00606ef7982b32aa4969f2b360192fca2090f6`。

**题干**

证明三次多项式的根与系数关系(韦达定理)，并构造一个以 $2$、$-1$、$\frac12$ 为根的首一三次多项式。

**过程**

设首一三次多项式 $f(x)=x^3+px^2+qx+r$ 的根为 $\alpha,\beta,\gamma$,则 $f(x)=(x-\alpha)(x-\beta)(x-\gamma)$。展开右边:$x^3-(\alpha+\beta+\gamma)x^2+(\alpha\beta+\beta\gamma+\gamma\alpha)x-\alpha\beta\gamma$。比较系数得韦达定理:$\alpha+\beta+\gamma=-p$,$\alpha\beta+\beta\gamma+\gamma\alpha=q$,$\alpha\beta\gamma=-r$。构造:以 $2,-1,\frac12$ 为根,则 $f(x)=(x-2)(x+1)(x-\frac12)$。展开:$(x^2-x-2)(x-\frac12)=x^3-x^2-2x-\frac12x^2+\frac12x+1=x^3-\frac32x^2-\frac32x+1$。

**答案原文**

韦达定理:根和 $=-p$,两两积和 $=q$,根积 $=-r$;构造:$f=x^3-\frac32x^2-\frac32x+1$。

## 237. draft-c32-01

内容 SHA256：`e8ed0f784dade8d46d5d4705248478fb2b13d2e040be02d87de670a45105434e`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft-codex-repair-v4-final.jsonl，第 11 行；源 SHA256 `37ad744d2e28133f1449fa961a00606ef7982b32aa4969f2b360192fca2090f6`。

**题干**

求$\mathbb R^5$中满足$x_{i+2}-2x_{i+1}+x_i=0$（$i=1,2,3$）的子空间的基与维数，并证明解的表达式完整。

**过程**

二阶差分为零等价于相邻一阶差相同。令$a=x_1,b=x_2-x_1$，递推唯一给$x_i=a+(i-1)b$，$i=1,\ldots,5$。反过来任何该形式均满足三约束。故解空间为$\operatorname{span}\{(1,1,1,1,1),(0,1,2,3,4)\}$。两向量由前两坐标可知独立，维数$2$；三个耦合约束独立，秩$3$。

**答案原文**

基$(1,1,1,1,1),(0,1,2,3,4)$，维数$2$。

## 238. draft-c32-02

内容 SHA256：`149c75bc40dc551b2f716901382def34275920315c60a5c0b99967fee934baf8`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft-codex-repair-v4-final.jsonl，第 12 行；源 SHA256 `37ad744d2e28133f1449fa961a00606ef7982b32aa4969f2b360192fca2090f6`。

**题干**

求$V=\{x\in\mathbb R^4:\sum_{i=0}^3x_i=0,\ \sum_{i=0}^3i x_i=0\}$的基与维数，证明给出的基张成全部解。

**过程**

约束行$(1,1,1,1)$与$(0,1,2,3)$不成比例，秩$2$，故维数$2$。向量$v=(1,-2,1,0)$与$w=(0,1,-2,1)$同时满足两个约束，且由首末坐标可知独立。也可对任意解先取$x_0v+x_3w$，减去后首末坐标为零，剩余两坐标满足$y_1+y_2=0,y_1+2y_2=0$，故全零，证明张成。

**答案原文**

基$(1,-2,1,0),(0,1,-2,1)$，维数$2$。

## 239. draft-c32-03

内容 SHA256：`ed25fae6c8377151659af656862ad9a43acdefaa3ba2a2fe34d7d6720a48fbc0`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft-codex-repair-v4-final.jsonl，第 13 行；源 SHA256 `37ad744d2e28133f1449fa961a00606ef7982b32aa4969f2b360192fca2090f6`。

**题干**

一个菱形流网络的四边流量$(u,v,w,z)$满足$u+v=1,w+z=1,u=w,v=z$。求实线性方程的全部解；再加入各流量非负，求可行集并判断两者是否为线性子空间。

**过程**

由守恒得$w=u,z=v=1-u$，所以全部解为$(t,1-t,t,1-t)$，$t\in\mathbb R$，是一条仿射直线。它等于$(0,1,0,1)+t(1,-1,1,-1)$，但不含零向量，因此不是线性子空间。非负性等价于$0\le t\le1$，可行集为该直线上的闭线段；线段也不含零且不封闭于任意标量乘法。四条等式有冗余，不能按方程条数直接减维数。

**答案原文**

全部实解$t\in\mathbb R$；非负解$t\in[0,1]$；两者都不是线性子空间。

## 240. draft-c32-04

内容 SHA256：`7c4736af28e00f7be5b450cc20f7f35b27261c99de237ecdeb4f62f40c501470`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft-codex-repair-v4-final.jsonl，第 14 行；源 SHA256 `37ad744d2e28133f1449fa961a00606ef7982b32aa4969f2b360192fca2090f6`。

**题干**

对实参数$a,b$，分类系统$x+y=1,\ ax+y=b$的全部解，并写出每种解集的维数或为空。

**过程**

相减得$(a-1)x=b-1$。若$a\ne1$，唯一解$x=(b-1)/(a-1),y=(a-b)/(a-1)$，解集为一个点，仿射维数$0$。若$a=1,b=1$，两式相同，解集$(t,1-t)$为仿射直线，维数$1$。若$a=1,b\ne1$，相减为$0=b-1\ne0$，无解；空集不作为含基点的仿射子空间讨论维数。

**答案原文**

$a\ne1$唯一；$a=b=1$一维仿射直线；$a=1,b\ne1$无解。

## 241. draft-c32-05

内容 SHA256：`047c80a54ef0b5476576bcd916c510c41c0cc0199664b475ad333ae947c4a570`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-13/draft-codex-repair-v4-final.jsonl，第 15 行；源 SHA256 `37ad744d2e28133f1449fa961a00606ef7982b32aa4969f2b360192fca2090f6`。

**题干**

证明:齐次线性方程组 $Ax=0$ 的解集是 $\mathbb R^n$ 的线性子空间,其维数为 $n-\mathrm{rank}(A)$;非齐次方程组 $Ax=b$($b\neq0$)的解集是 $\eta_0+\ker A$(仿射子空间)而不是线性子空间。

**过程**

齐次解集$\ker A$含零并对线性组合封闭，维数$n-\operatorname{rank}A$。非齐次系统$Ax=b$若不相容，解集为空；若相容，选一个特解$x_0$，则$Ax=b$等价于$A(x-x_0)=0$，所以解集恰为$x_0+\ker A$，仿射维数$n-\operatorname{rank}A$。若$b\ne0$，零向量不在该解集中，因而不是线性子空间；若$b=0$，回到齐次情形。

**答案原文**

齐次解集$\ker A$；相容非齐次解集$x_0+\ker A$；不相容则为空。

## 242. draft-c34-01

内容 SHA256：`1adc29dca0d4a9fe615d3dff959e0053a65dd320d06e231aee6932c2c936b538`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft-codex-repair-v6.jsonl，第 1 行；源 SHA256 `509ada826f1f061a3d5f51557202038197b530851e638cb3cee4ba5c1b48a9eb`。

**题干**

设 $E=\begin{pmatrix}1&0&0\\0&1&0\\0&0&5\end{pmatrix}$。说明用 $E$ 左乘与右乘一个 $3$ 阶矩阵 $A$ 分别对 $A$ 做了什么操作。

**过程**

左乘 $EA$:把 $A$ 的第三行乘以 $5$(其余行不变)。右乘 $AE$:把 $A$ 的第三列乘以 $5$(其余列不变)。$E$ 是由单位矩阵把第三行(列)乘以 $5$ 得到的倍乘型初等矩阵。

**答案原文**

左乘:第三行乘 $5$;右乘:第三列乘 $5$。

## 243. draft-c34-02

内容 SHA256：`3f2b5adcf91846fd3c92146ef9c83ee603e5f15457ff63f1d5bb77eb03224782`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft-codex-repair-v6.jsonl，第 2 行；源 SHA256 `509ada826f1f061a3d5f51557202038197b530851e638cb3cee4ba5c1b48a9eb`。

**题干**

构造把 $3$ 阶矩阵的第二行加到第一行的初等矩阵 $E$，并求 $E^{-1}$ 与 $E^{-1}$ 对应的操作。

**过程**

把第二行加到第一行的初等矩阵为 $E=\begin{pmatrix}1&1&0\\0&1&0\\0&0&1\end{pmatrix}$(左乘 $EA$ 即第一行加第二行)。其逆为把第一行减去第二行:$E^{-1}=\begin{pmatrix}1&-1&0\\0&1&0\\0&0&1\end{pmatrix}$。验证:$EE^{-1}=I$(第一行:$(1,1,0)$ 减第二行 $(0,1,0)$ 得 $(1,0,0)$)。

**答案原文**

$E=\begin{pmatrix}1&1&0\\0&1&0\\0&0&1\end{pmatrix}$;$E^{-1}=\begin{pmatrix}1&-1&0\\0&1&0\\0&0&1\end{pmatrix}$,对应「第一行减第二行」。

## 244. draft-c34-03

内容 SHA256：`524c10bf51c0120a7b1e1fe2ff43a962057255a9570c7cb8b26dedcf85e18cfd`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft-codex-repair-v6.jsonl，第 3 行；源 SHA256 `509ada826f1f061a3d5f51557202038197b530851e638cb3cee4ba5c1b48a9eb`。

**题干**

先交换第一、二行，再将第一行乘以$2$。写出这一复合行变换的矩阵（初等矩阵的乘积），并验证作用顺序。

**过程**

$P_1=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}$,$P_2=\begin{pmatrix}2&0&0\\0&1&0\\0&0&1\end{pmatrix}$。先做 $P_1$ 后做 $P_2$ 对应左乘 $P_2P_1$(先作用的矩阵写在右边):$P_2P_1=\begin{pmatrix}2&0&0\\0&1&0\\0&0&1\end{pmatrix}\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}=\begin{pmatrix}0&2&0\\1&0&0\\0&0&1\end{pmatrix}$。复合矩阵把第二行换到第一行并乘以 $2$。

**答案原文**

复合变换矩阵为$\begin{pmatrix}0&2&0\\1&0&0\\0&0&1\end{pmatrix}$，它是两个初等矩阵的乘积。

## 245. draft-c34-04

内容 SHA256：`cc8053c19b4d47f171006007448db58404862d80ab32891f434511cbe253300c`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft-codex-repair-v6.jsonl，第 4 行；源 SHA256 `509ada826f1f061a3d5f51557202038197b530851e638cb3cee4ba5c1b48a9eb`。

**题干**

把矩阵 $A=\begin{pmatrix}2&2\\0&1\end{pmatrix}$ 分解为初等矩阵的乘积。

**过程**

对 $A$ 作行变换化单位阵:第一步第一行乘以 $\frac12$,对应初等矩阵 $E_1'=\begin{pmatrix}\frac12&0\\0&1\end{pmatrix}$,$E_1'A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$;第二步第一行减去第二行,对应 $E_2'=\begin{pmatrix}1&-1\\0&1\end{pmatrix}$,$E_2'E_1'A=I$。故 $A=E_1'^{-1}E_2'^{-1}$。求逆:$E_1'^{-1}=\begin{pmatrix}2&0\\0&1\end{pmatrix}$(第一行乘 $2$),$E_2'^{-1}=\begin{pmatrix}1&1\\0&1\end{pmatrix}$(第一行加第二行)。故 $A=\begin{pmatrix}2&0\\0&1\end{pmatrix}\begin{pmatrix}1&1\\0&1\end{pmatrix}$。验证:乘积 $=\begin{pmatrix}2&2\\0&1\end{pmatrix}=A$ ✓。

**答案原文**

$A=\begin{pmatrix}2&0\\0&1\end{pmatrix}\begin{pmatrix}1&1\\0&1\end{pmatrix}$,两个初等矩阵之积。

## 246. draft-c34-05

内容 SHA256：`f55246daa45c55bedd74eac121b5067f525728226d8ac86a506d6352aa9acf67`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft-codex-repair-v6.jsonl，第 5 行；源 SHA256 `509ada826f1f061a3d5f51557202038197b530851e638cb3cee4ba5c1b48a9eb`。

**题干**

记$E_{ij}(a)=I+a e_{ij}$（$i\ne j$），其中$e_{ij}$为三阶矩阵单位。证明$E_{12}(a)E_{23}(b)E_{12}(-a)E_{23}(-b)=E_{13}(ab)$，求逆矩阵，并用$a=2/3,b=3/4$精确验证。

**过程**

矩阵单位满足$e_{ij}e_{kl}=\delta_{jk}e_{il}$，特别是$e_{12}e_{23}=e_{13}$而$e_{23}e_{12}=0$，各相关平方为零。逐因子相乘，前三因子为$I+b e_{23}+ab e_{13}$，再乘$I-b e_{23}$得$I+ab e_{13}$。$E_{ij}(a)^{-1}=E_{ij}(-a)$，所以最终逆为$E_{13}(-ab)$。代入两分数得$ab=1/2$，复合为$\begin{pmatrix}1&0&1/2\\0&1&0\\0&0&1\end{pmatrix}$，逆将$1/2$改为$-1/2$。该交换子显示倍加变换的顺序通常不可交换。

**答案原文**

交换子$E_{13}(ab)$，逆$E_{13}(-ab)$；指定参数的非对角项$1/2$。

## 247. draft-c38-01

内容 SHA256：`2606f69e5f272062cca7d09fdd89258964f1bf1b7bf14c613227b1f788dcc8e9`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft-codex-repair-v6.jsonl，第 6 行；源 SHA256 `509ada826f1f061a3d5f51557202038197b530851e638cb3cee4ba5c1b48a9eb`。

**题干**

设$M:\mathbb R^2\to\mathbb R^2$任意线性映射，在$\mathbb R^2\times\mathbb R^2$中取$U=\{(a,Ma)\}$、$V=\{(0,b)\}$。证明全空间是$U\oplus V$，求投影到$U$沿$V$的表达式及核、像、维数。

**过程**

$(a,b)=(a,Ma)+(0,b-Ma)$，第一项属$U$、第二项属$V$，故和为全空间。若$(a,Ma)=(0,b)$，则$a=0,b=0$，交为零，分解唯一。投影$P(a,b)=(a,Ma)$，$P^2=P$，核$V$、像$U$，两者维数均$2$。不需要$M$可逆；图空间与竖直空间的互补来自第一坐标的唯一性。

**答案原文**

$\mathbb R^4=U\oplus V$；$P(a,b)=(a,Ma)$，核$V$、像$U$，维数均$2$。

## 248. draft-c38-02

内容 SHA256：`a2295bdd12102a741a1a504b77b465b20f0609ad4f9375057b94cdfa7c00e6fa`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft-codex-repair-v6.jsonl，第 7 行；源 SHA256 `509ada826f1f061a3d5f51557202038197b530851e638cb3cee4ba5c1b48a9eb`。

**题干**

在$\mathbb R[x]_{\le4}$中，令$U$为偶多项式，$V$为被$(x-1)^2$整除的多项式。求$U\cap V$、$U+V$及维数，判断和是否直和。

**过程**

$U=\operatorname{span}(1,x^2,x^4)$，维数$3$；$V=(x-1)^2\mathbb R[x]_{\le2}$，维数$3$。若$f=a+bx^2+cx^4\in V$，须$f(1)=f^{\prime}(1)=0$，即$a+b+c=0,2b+4c=0$，得$f=c(x^2-1)^2$。故交为该一维空间。和的维数$3+3-1=5$，等于环境维数，所以和为全部$\mathbb R[x]_{\le4}$。交非零，故不是直和。

**答案原文**

交$\operatorname{span}(x^2-1)^2$，维数$1$；和为五维全空间，非直和。

## 249. draft-c38-03

内容 SHA256：`33ac67a30408313df6373a05339cad46dcc68258913e943bb0040ca05ccb0142`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft-codex-repair-v6.jsonl，第 8 行；源 SHA256 `509ada826f1f061a3d5f51557202038197b530851e638cb3cee4ba5c1b48a9eb`。

**题干**

在实$2\times2$矩阵空间中，令$U$为对称矩阵、$V$为迹为零的矩阵。给出交空间的基、两空间与和的维数，并显式证明和为全空间。

**过程**

$U$维数$3$，$V$维数$3$。交中矩阵为$\begin{pmatrix}a&b\\b&-a\end{pmatrix}$，基为$\operatorname{diag}(1,-1)$与$\begin{pmatrix}0&1\\1&0\end{pmatrix}$，维数$2$。对任意$A$，分解$A=(\operatorname{tr}A/2)I+[A-(\operatorname{tr}A/2)I]$，前项对称、后项无迹，故和为全空间，维数$4$。交非零，所以分解成任意$U,V$成分不唯一，也不是直和。

**答案原文**

$\dim U=\dim V=3$，交维数$2$、基如上，和为四维全空间，非直和。

## 250. draft-c38-04

内容 SHA256：`5c4dad2d2f4b2c3eab8eab8499e3879ab421533bf9ba899c4b92c92f018500e1`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft-codex-repair-v6.jsonl，第 9 行；源 SHA256 `509ada826f1f061a3d5f51557202038197b530851e638cb3cee4ba5c1b48a9eb`。

**题干**

设 $U,V$ 是 $\mathbb R^5$ 的子空间，$\dim U=3$，$\dim V=2$。求 $\dim(U\cap V)$ 的可能取值范围，并说明每种取值对应的 $\dim(U+V)$。

**过程**

$\dim(U+V)=3+2-\dim(U\cap V)\le5$，交维数为$0,1,2$之一，和维数对应$5,4,3$。固定$U=\operatorname{span}(e_1,e_2,e_3)$，分别取$V=\operatorname{span}(e_4,e_5)$、$\operatorname{span}(e_1,e_4)$、$\operatorname{span}(e_1,e_2)$，便逐一达到这些可能。

**答案原文**

$\dim(U\cap V)\in\{0,1,2\}$,对应 $\dim(U+V)=5,4,3$。

## 251. draft-c38-05

内容 SHA256：`eec178fb8196df119401d4f2d490f06c0ba248ce0f34f7a79c009fac10f3e1ec`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft-codex-repair-v6.jsonl，第 10 行；源 SHA256 `509ada826f1f061a3d5f51557202038197b530851e638cb3cee4ba5c1b48a9eb`。

**题干**

证明维数公式:若 $U,V$ 是有限维线性空间 $W$ 的子空间，则 $\dim(U+V)=\dim U+\dim V-\dim(U\cap V)$。

**过程**

取交空间基$u_1,\ldots,u_k$，分别扩充为$U$的基$u_i,p_j$与$V$的基$u_i,q_l$。合并列表张成$U+V$。若$\sum a_iu_i+\sum b_jp_j+\sum c_lq_l=0$，则$\sum b_jp_j$同时属于$U$与$V$，属于交空间；由$U$基独立得$b_j=0$，再由$V$基得$a_i=c_l=0$。因此合并列表是基，其长度为$\dim U+\dim V-\dim(U\cap V)$，得到维数公式。

**答案原文**

证明见解法(交的基延拓为两子空间的基,拼接组构成 $U+V$ 的基)。

## 252. draft-c39-01

内容 SHA256：`9a8418cdda2f5b24da99c43d676cf16fc338b110fb36b74d364bb7b449541871`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft-codex-repair-v6.jsonl，第 11 行；源 SHA256 `509ada826f1f061a3d5f51557202038197b530851e638cb3cee4ba5c1b48a9eb`。

**题干**

在实$2\times2$矩阵空间中取$A=\operatorname{diag}(1,3)$，定义$T(X)=AX-XA$。求核、像、秩，并说明全空间能否分解为核与像的直和。

**过程**

对$X=\begin{pmatrix}a&b\\c&d\end{pmatrix}$，$T(X)=\begin{pmatrix}0&-2b\\2c&0\end{pmatrix}$。所以核为所有对角矩阵，基$e_{11},e_{22}$；像为所有零对角矩阵，基$e_{12},e_{21}$，秩$2$。两空间交为零且每个矩阵唯一分解为对角部分与零对角部分，故是直和。$T$在像上可逆，$T^2$在像上为$4I$，与在核上为零的作用不同；非正交Jordan中心化问题未被套用。

**答案原文**

核为对角矩阵，像为零对角矩阵，秩$2$；$M_2(\mathbb R)=\ker T\oplus\operatorname{im}T$。

## 253. draft-c39-02

内容 SHA256：`2ee8a9157e04520c57a06ed99084d417bb6cea33c31e9696afd8d4bb806a8d71`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft-codex-repair-v6.jsonl，第 12 行；源 SHA256 `509ada826f1f061a3d5f51557202038197b530851e638cb3cee4ba5c1b48a9eb`。

**题干**

设 $T:\mathbb R^2\to\mathbb R^3$ 由 $T(x,y)=(x+y,\,x-y,\,2x)$ 定义。判断 $T$ 是否单射、是否满射，并求核与像的维数。

**过程**

核:解 $x+y=0,x-y=0,2x=0$,得 $x=y=0$,故 $\ker T=\{0\}$,$\dim\ker T=0$,由秩-零度定理 $\dim\mathrm{im}\,T=2-0=2$。单射:核为 $\{0\}$ ⟺ 单射,故 $T$ 单射。满射:像的维数 $2<3$,故 $T$ 非满射(像是 $\mathbb R^3$ 中由 $T(1,0)=(1,1,2)$ 与 $T(0,1)=(1,-1,0)$ 张成的平面)。

**答案原文**

单射但非满射;$\ker T=\{0\}$(维数 $0$),$\dim\mathrm{im}\,T=2$。

## 254. draft-c39-03

内容 SHA256：`35aba93ce2b694602694d55923e51fa48c2a92c8d1abc162ed8fd308a7903806`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft-codex-repair-v6.jsonl，第 13 行；源 SHA256 `509ada826f1f061a3d5f51557202038197b530851e638cb3cee4ba5c1b48a9eb`。

**题干**

定义$T:\mathbb R[x]_{\le3}\to\mathbb R^3$，$Tf=(f(0),f(1),f(-1))$。求核、像与秩，给出证明满射的显式右逆。

**过程**

核中$f$在$0,1,-1$三个不同节点为零，因此被$x(x-1)(x+1)$整除；度数最多$3$，故核$\operatorname{span}(x^3-x)$。对$(a,b,c)\in\mathbb R^3$，定义$R(a,b,c)=a(1-x^2)+b x(x+1)/2+c x(x-1)/2$，三个节点的值依次为$a,b,c$，所以$TR=I$。故像为全部$\mathbb R^3$，秩$3$、核维数$1$，右逆证明满射不依赖仅报维数。

**答案原文**

核$\operatorname{span}(x^3-x)$；像$\mathbb R^3$、秩$3$；右逆$R(a,b,c)=a(1-x^2)+\frac b2x(x+1)+\frac c2x(x-1)$。

## 255. draft-c39-04

内容 SHA256：`95e5165e64d190047ac35f0c641738676a967d36c0a1d42703bb278f60d7718a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft-codex-repair-v6.jsonl，第 14 行；源 SHA256 `509ada826f1f061a3d5f51557202038197b530851e638cb3cee4ba5c1b48a9eb`。

**题干**

设 $T:\mathbb R^3\to\mathbb R^3$ 由 $T(x,y,z)=(x+y,\,y+z,\,0)$ 定义。求 $T^2$ 的表达式，并比较 $T$ 与 $T^2$ 的核与像。

**过程**

$T^2(x,y,z)=T(x+y,\,y+z,\,0)=((x+y)+(y+z),\,(y+z)+0,\,0)=(x+2y+z,\,y+z,\,0)$。核:$T$ 的核:$x+y=0,y+z=0$,得 $(x,-x,x)$,$\ker T=\mathrm{span}\{(1,-1,1)\}$。$T^2$ 的核:$x+2y+z=0,y+z=0$。由第二式 $z=-y$,代入第一式得 $x+2y-y=x+y=0$,故与 $\ker T$ 相同的条件,$\ker T^2=\ker T=\mathrm{span}\{(1,-1,1)\}$。像:$T$ 的像由 $T(1,0,0)=(1,0,0)$,$T(0,1,0)=(1,1,0)$,$T(0,0,1)=(0,1,0)$ 张成,即 $\{(a,b,0)\}$,维数 $2$。$T^2$ 的像由 $T^2(1,0,0)=(1,0,0)$,$T^2(0,0,1)=(1,1,0)$ 张成($T^2(0,1,0)=(2,1,0)=(1,0,0)+(1,1,0)$),也是 $\{(a,b,0)\}$,维数 $2$。故 $\ker T^2=\ker T$ 且 $\mathrm{im}\,T^2=\mathrm{im}\,T$(本例中复合映射的核与像均不变)。

**答案原文**

$T^2(x,y,z)=(x+2y+z,\,y+z,\,0)$;$\ker T^2=\ker T=\mathrm{span}\{(1,-1,1)\}$,$\mathrm{im}\,T^2=\mathrm{im}\,T=\{(a,b,0)\}$。

## 256. draft-c39-05

内容 SHA256：`d17c47c0f5123d7414c33db3a72e9ea76875f74d1569c1c6e13391044f4b68cc`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-14/draft-codex-repair-v6.jsonl，第 15 行；源 SHA256 `509ada826f1f061a3d5f51557202038197b530851e638cb3cee4ba5c1b48a9eb`。

**题干**

证明秩-零度定理:若 $T:V\to W$ 是有限维线性空间之间的线性映射，则 $\dim V=\dim\ker T+\dim\mathrm{im}\,T$。

**过程**

取 $\ker T$ 的一组基 $v_1,\dots,v_k$,延拓为 $V$ 的基 $v_1,\dots,v_k,v_{k+1},\dots,v_n$(故 $\dim V=n$)。下证 $T(v_{k+1}),\dots,T(v_n)$ 是 $\mathrm{im}\,T$ 的一组基。张成:任意 $y\in\mathrm{im}\,T$,存在 $x=\sum_{i=1}^{n}c_iv_i$ 使 $y=T(x)=\sum_{i=1}^{n}c_iT(v_i)=\sum_{i=k+1}^{n}c_iT(v_i)$(前 $k$ 项为零,因 $v_i\in\ker T$)。线性无关:若 $\sum_{i=k+1}^{n}d_iT(v_i)=0$,则 $T\left(\sum_{i=k+1}^{n}d_iv_i\right)=0$,即 $\sum_{i=k+1}^{n}d_iv_i\in\ker T$,它可仅由 $v_1,\dots,v_k$ 表出;但 $V$ 的基表示唯一,故 $d_{k+1}=\cdots=d_n=0$。于是 $\dim\mathrm{im}\,T=n-k$,即 $\dim V=n=k+(n-k)=\dim\ker T+\dim\mathrm{im}\,T$。

**答案原文**

证明见解法(核的基延拓到全空间,核外基向量的像构成像的基)。

## 257. draft-c40-01

内容 SHA256：`70b1a195519e5548d9eb56cc3808ff33ac15436089989e1a531213ce613d8787`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft-codex-repair-v4-final.jsonl，第 1 行；源 SHA256 `1b30dc88733b7cf641716e24d00836d421d9b364628fdd5dea63d6b4f987ba1a`。

**题干**

令$f=\lambda-1$，$A(\lambda)=\operatorname{diag}(f,f^2)$、$B(\lambda)=\operatorname{diag}(1,f^3)$。两矩阵行列式相同，判断是否多项式可逆等价；比较在有理函数域与代入实参数后的秩、核，说明行列式为何不足。

**过程**

两者行列式都为$f^3$，但一阶子式首一gcd分别为$f$与$1$，不变因子分别$f,f^2$与$1,f^3$，所以不unimodular等价。在有理函数域$\mathbb R(\lambda)$，$f$是可逆非零元素，两矩阵秩都为$2$、核都为零；在多项式环中核也都为零，因为环无零因子。在实数$a\ne1$代入时两者仍秩$2$、核零。代入$a=1$，$A(1)=0$，秩$0$、核$\mathbb R^2$；$B(1)=\operatorname{diag}(1,0)$，秩$1$、核$\operatorname{span}(e_2)$。同一行列式零点及其阶数不能确定特殊参数的核维数，通用域的核也不能直接代入当作特殊核。

**答案原文**

不等价；一般域及$a\ne1$均秩$2$，$a=1$时秩分别$0,1$；行列式相同不足以确定特殊核。

## 258. draft-c40-02

内容 SHA256：`b8894e726c0684300215ac7f27dc1cbae2d8fa101171bdbb4b315b934892b725`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft-codex-repair-v4-final.jsonl，第 2 行；源 SHA256 `1b30dc88733b7cf641716e24d00836d421d9b364628fdd5dea63d6b4f987ba1a`。

**题干**

求 λ-矩阵 $A(\lambda)=\begin{pmatrix}\lambda&1\\0&\lambda\end{pmatrix}$ 的行列式因子、不变因子与初等因子。

**过程**

$A(\lambda)$ 的全部一阶子式为 $\lambda,1,0,\lambda$,其最大公因式 $D_1(\lambda)=1$。二阶行列式因子 $D_2(\lambda)=\det A(\lambda)=\lambda^2$。不变因子:$d_1=D_1=1$,$d_2=\frac{D_2}{D_1}=\lambda^2$。初等因子:$\lambda^2$(由 $d_2$ 给出)。

**答案原文**

$D_1=1$,$D_2=\lambda^2$;不变因子 $d_1=1$,$d_2=\lambda^2$;初等因子 $\lambda^2$。

## 259. draft-c40-03

内容 SHA256：`1426737efb5e1e422a8714d69ceb61c211dac1dfa4d63e2e329c38398a946423`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft-codex-repair-v4-final.jsonl，第 3 行；源 SHA256 `1b30dc88733b7cf641716e24d00836d421d9b364628fdd5dea63d6b4f987ba1a`。

**题干**

分别求 $A(\lambda)=\mathrm{diag}(\lambda,\lambda-1)$ 与 $B(\lambda)=\mathrm{diag}(\lambda,\lambda)$ 的不变因子与初等因子，并说明两者结构差异的原因。

**过程**

$A(\lambda)$:$D_1=\gcd(\lambda,\lambda-1)=1$,$D_2=\lambda(\lambda-1)$;不变因子 $d_1=1$,$d_2=\lambda(\lambda-1)$;初等因子 $\lambda$ 与 $\lambda-1$(均由 $d_2$ 分解得到)。$B(\lambda)$:$D_1=\lambda$,$D_2=\lambda^2$;不变因子 $d_1=\lambda$,$d_2=\lambda$;初等因子 $\lambda$ 与 $\lambda$($\lambda$ 出现两次)。差异原因:不变因子满足整除链 $d_1\mid d_2$。$A$ 的两个对角元互素,公因子为 $1$,$d_2$ 必须吞下全部两个因子;而 $B$ 的两个对角元有公因子 $\lambda$,可分摊到 $d_1$ 与 $d_2$。

**答案原文**

$A$:不变因子 $1,\lambda(\lambda-1)$,初等因子 $\lambda,\lambda-1$;$B$:不变因子 $\lambda,\lambda$,初等因子 $\lambda,\lambda$。差异源于互素与否影响整除链分配。

## 260. draft-c40-04

内容 SHA256：`14e22dbdbd10f7ff26f8f8456b3a86f5cbf4a6c65d2fccd0826c0ab3ca29571a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft-codex-repair-v4-final.jsonl，第 4 行；源 SHA256 `1b30dc88733b7cf641716e24d00836d421d9b364628fdd5dea63d6b4f987ba1a`。

**题干**

求 λ-矩阵 $A(\lambda)=\mathrm{diag}(\lambda+1,\,\lambda(\lambda+1),\,(\lambda+1)^2(\lambda-2))$ 的行列式因子、不变因子与初等因子。

**过程**

一阶行列式因子:$D_1=\gcd(\lambda+1,\lambda(\lambda+1),(\lambda+1)^2(\lambda-2))=\lambda+1$。二阶行列式因子:各二阶子式(对角情形即两两乘积)为 $\lambda(\lambda+1)^2$、$(\lambda+1)^3(\lambda-2)$、$\lambda(\lambda+1)^3(\lambda-2)$,最大公因式 $D_2=(\lambda+1)^2$。$D_3=\det=\lambda(\lambda+1)^4(\lambda-2)$。不变因子:$d_1=D_1=\lambda+1$;$d_2=\frac{D_2}{D_1}=\lambda+1$;$d_3=\frac{D_3}{D_2}=\lambda(\lambda+1)^2(\lambda-2)$。初等因子:$\lambda+1$、$\lambda+1$、$\lambda$、$(\lambda+1)^2$、$\lambda-2$。

**答案原文**

$D_1=\lambda+1$,$D_2=(\lambda+1)^2$,$D_3=\lambda(\lambda+1)^4(\lambda-2)$;不变因子 $\lambda+1,\lambda+1,\lambda(\lambda+1)^2(\lambda-2)$;初等因子 $\lambda+1,\lambda+1,\lambda,(\lambda+1)^2,\lambda-2$。

## 261. draft-c40-05

内容 SHA256：`191936a47436c6e9d444ae31a63d7861576943c1e7120d5b1d66d5808bd63cba`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft-codex-repair-v4-final.jsonl，第 5 行；源 SHA256 `1b30dc88733b7cf641716e24d00836d421d9b364628fdd5dea63d6b4f987ba1a`。

**题干**

在$\mathbb R[\lambda]$中，证明多项式矩阵的各阶首一行列式因子在左右乘可逆多项式矩阵时不变。说明允许的行缩放是什么，并以一个非可逆多项式行缩放说明限制必要。

**过程**

环中的单位是非零实常数。可逆多项式矩阵的行列式是单位，逆仍为多项式矩阵。由Cauchy–Binet公式，$UA$的每个$k$阶子式是$A$的$k$阶子式的多项式线性组合，所以旧子式的首一最大公因子整除新子式的首一最大公因子；再乘$U^{-1}$得反向整除，因此两者相同。右乘同理，恒为零的子式族也保持。初等行缩放只能乘非零常数，行倍加可乘任意多项式。反例$A=\operatorname{diag}(\lambda,\lambda+1)$，将第一行乘$\lambda$得$B=\operatorname{diag}(\lambda^2,\lambda+1)$；二阶因子由$\lambda(\lambda+1)$变为$\lambda^2(\lambda+1)$，不保持，因为缩放矩阵行列式$\lambda$不是单位。

**答案原文**

左右unimodular等价保持全部首一行列式因子；行缩放限非零常数，非单位缩放可改变因子。

## 262. draft-c41-01

内容 SHA256：`0338164658db8578af802e9fa7b362fa74c8dae63425e4521095e9d09127d2c3`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft-codex-repair-v4-final.jsonl，第 6 行；源 SHA256 `1b30dc88733b7cf641716e24d00836d421d9b364628fdd5dea63d6b4f987ba1a`。

**题干**

在基$e_{11},e_{12},e_{21},e_{22}$中，令$N=J_2(0)\otimes I_2+I_2\otimes J_2(0)$。从张量结构求Jordan形式，并给出实际Jordan链及换基矩阵。

**过程**

$Ne_{11}=0,Ne_{12}=Ne_{21}=e_{11},Ne_{22}=e_{12}+e_{21}$。所以$N^2e_{22}=2e_{11}$，$N^3=0$；秩序列$4,2,1,0$。取链$v_3=e_{22},v_2=e_{12}+e_{21},v_1=2e_{11}$及$w=e_{12}-e_{21}$，有$Nv_3=v_2,Nv_2=v_1,Nv_1=Nw=0$。$P=(v_1,v_2,v_3,w)=\begin{pmatrix}2&0&0&0\\0&1&0&1\\0&1&0&-1\\0&0&1&0\end{pmatrix}$可逆，$NP=P[J_3(0)\oplus J_1(0)]$。因此Jordan形式为$J_3(0)\oplus J_1(0)$。

**答案原文**

$J_3(0)\oplus J_1(0)$；链和$P$如上。

## 263. draft-c41-02

内容 SHA256：`c0f65f25b055d3cf44466a05eeb35a831fcb838c62b124a65d167838f2e2c9d8`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft-codex-repair-v4-final.jsonl，第 7 行；源 SHA256 `1b30dc88733b7cf641716e24d00836d421d9b364628fdd5dea63d6b4f987ba1a`。

**题干**

设$B=\begin{pmatrix}1&-2\\2&1\end{pmatrix}$、$A=\begin{pmatrix}B&I_2\\0&B\end{pmatrix}$。求复域Jordan形式和实最小多项式，说明实域是否可以写成实对角阵。

**过程**

$B$有不同复根$\lambda_\pm=1\pm2i$，特征向量$q_+=(1,-i)^{\mathsf T},q_-=(1,i)^{\mathsf T}$。对各根令$v_\pm=(q_\pm,0)$、$w_\pm=(0,q_\pm)$，则$(A-\lambda_\pm I)w_\pm=v_\pm$、$(A-\lambda_\pm I)v_\pm=0$。因$q_+,q_-$独立，四向量组成复基，所以Jordan形式$J_2(1+2i)\oplus J_2(1-2i)$。两个二阶块使复最小多项式为$(\lambda-1-2i)^2(\lambda-1+2i)^2=[(\lambda-1)^2+4]^2$，它也是实最小多项式。非实特征值且存在二阶块，不能写成实对角阵，也不能在复域对角化。

**答案原文**

复Jordan形式$J_2(1+2i)\oplus J_2(1-2i)$；实最小多项式$[(\lambda-1)^2+4]^2$；不可对角化。

## 264. draft-c41-03

内容 SHA256：`30d2de746bf004b26ac7b6d1e391a8cd6facd194b0469b99170afdae2e7e47d5`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft-codex-repair-v4-final.jsonl，第 8 行；源 SHA256 `1b30dc88733b7cf641716e24d00836d421d9b364628fdd5dea63d6b4f987ba1a`。

**题干**

设四阶矩阵 $A$ 的特征值全为 $2$，且 $\dim\ker(A-2I)=2$，$\dim\ker(A-2I)^2=3$，$\dim\ker(A-2I)^3=4$。求 $A$ 的若尔当标准形。

**过程**

若尔当块数 $=$ 特征子空间维数 $=\dim\ker(A-2I)=2$。各阶块数由核维数差给出:大小至少为 $2$ 的块数 $=\dim\ker(A-2I)^2-\dim\ker(A-2I)=3-2=1$;大小至少为 $3$ 的块数 $=\dim\ker(A-2I)^3-\dim\ker(A-2I)^2=4-3=1$。故块为:一个三阶块与一个一阶块($3+1=4$)。若尔当标准形为 $J_3(2)\oplus J_1(2)=\begin{pmatrix}2&1&0&0\\0&2&1&0\\0&0&2&0\\0&0&0&2\end{pmatrix}$。

**答案原文**

$J=J_3(2)\oplus J_1(2)$,即一个三阶块与一个一阶块。

## 265. draft-c41-04

内容 SHA256：`cf122b7a2b4d3b01abd9f19d3323515943fff72b2ed6466dc6ceb611db889855`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft-codex-repair-v4-final.jsonl，第 9 行；源 SHA256 `1b30dc88733b7cf641716e24d00836d421d9b364628fdd5dea63d6b4f987ba1a`。

**题干**

对$A=\begin{pmatrix}4&2&1\\0&4&3\\0&0&4\end{pmatrix}$，构造实际广义特征向量链和$P$，验证$P^{-1}AP$，而非直接读出现成Jordan块。

**过程**

令$N=A-4I$，取$v_3=e_3$，$v_2=Nv_3=(1,3,0)^{\mathsf T}$，$v_1=Nv_2=(6,0,0)^{\mathsf T}$，则$Nv_1=0$。$P=(v_1,v_2,v_3)=\begin{pmatrix}6&1&0\\0&3&0\\0&0&1\end{pmatrix}$，行列式$18\ne0$。链给$AP=P\begin{pmatrix}4&1&0\\0&4&1\\0&0&4\end{pmatrix}$，所以Jordan形式为$J_3(4)$，最小多项式$(\lambda-4)^3$；$N^2\ne0,N^3=0$确保不能误分成较短链。

**答案原文**

$P=\begin{pmatrix}6&1&0\\0&3&0\\0&0&1\end{pmatrix}$，$P^{-1}AP=J_3(4)$。

## 266. draft-c41-05

内容 SHA256：`20546b1e52f58e601553c027ea8b54930ef6440c8f6fea4c145818ec3f76002e`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft-codex-repair-v4-final.jsonl，第 10 行；源 SHA256 `1b30dc88733b7cf641716e24d00836d421d9b364628fdd5dea63d6b4f987ba1a`。

**题干**

证明:若尔当块 $J_m(\lambda)$ 的幂零部分 $N=J_m(0)$ 满足 $\dim\ker N^k=\min(k,m)$；并说明这一公式如何由核维数序列唯一确定若尔当块的个数与大小。

**过程**

$N=J_m(0)$ 是把基向量向前推一位的位移算子:$Ne_1=0$,$Ne_i=e_{i-1}$($i\ge2$)。于是 $N^k$ 把 $e_i$ 映为 $e_{i-k}$($i>k$)或 $0$($i\le k$),即 $N^k$ 的像由 $e_1,\dots,e_{m-k}$ 张成(当 $k<m$),秩为 $m-k$;当 $k\ge m$ 时 $N^k=0$,秩为 $0$。由秩-零度,$\dim\ker N^k=m-(m-k)=k$($k<m$),$\dim\ker N^k=m$($k\ge m$),即 $\min(k,m)$。块结构:对一般矩阵,设 $r_k=\dim\ker(A-\lambda I)^k$,则大小至少为 $k$ 的 $\lambda$ 块数为 $r_k-r_{k-1}$(每个 $m$ 阶块对 $r_k$ 贡献 $\min(k,m)$,相邻差即 $\min(k,m)-\min(k-1,m)$,恰好是大小为 $\ge k$ 的块数贡献的 $1$)。故核维数序列 $r_0=0,r_1,r_2,\dots$ 的差分解唯一确定各阶块数。

**答案原文**

证明见解法(位移算子的核维数 $\min(k,m)$;块数 $=r_k-r_{k-1}$ 的差分解唯一确定块结构)。

## 267. draft-c42-01

内容 SHA256：`7f859c6952043f2d866e51b4b74397b84fcea20c429daa0c86805aa6b298674d`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft-codex-repair-v4-final.jsonl，第 11 行；源 SHA256 `1b30dc88733b7cf641716e24d00836d421d9b364628fdd5dea63d6b4f987ba1a`。

**题干**

设$u\in\mathbb R^m$为单位向量，$m\ge1$。证明$H=I-2uu^{\mathsf T}$是正交矩阵，求几何意义、行列式与特征空间。

**过程**

$H^{\mathsf T}=H$，且$H^2=I-4uu^{\mathsf T}+4u(u^{\mathsf T}u)u^{\mathsf T}=I$。$Hu=-u$；若$v\perp u$，$Hv=v$。由直和$\mathbb R^m=\operatorname{span}(u)\oplus u^{\perp}$，这是关于超平面$u^{\perp}$的反射；特征值$-1$空间为$\operatorname{span}(u)$，特征值$1$空间为$u^{\perp}$，维数分别$1,m-1$，行列式$-1$。

**答案原文**

$H$为超平面反射，$\det H=-1$；两特征空间$\operatorname{span}(u)$与$u^{\perp}$。

## 268. draft-c42-02

内容 SHA256：`f1e0c1c5ee8703d2c3cb1d64d9ea9243a168c10c5bf5a652c49034bd5c90b022`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft-codex-repair-v4-final.jsonl，第 12 行；源 SHA256 `1b30dc88733b7cf641716e24d00836d421d9b364628fdd5dea63d6b4f987ba1a`。

**题干**

令$R_x=\begin{pmatrix}1&0&0\\0&0&-1\\0&1&0\end{pmatrix}$、$R_y=\begin{pmatrix}0&0&1\\0&1&0\\-1&0&0\end{pmatrix}$。求两个乘积并说明三维不同轴旋转为何不交换，给两乘积的轴与精确角。

**过程**

$R_xR_y=\begin{pmatrix}0&0&1\\1&0&0\\0&1&0\end{pmatrix}$，$R_yR_x=\begin{pmatrix}0&1&0\\0&0&-1\\-1&0&0\end{pmatrix}$，不同。两者均正交、行列式$1$、迹$0$，由$\operatorname{tr}R=1+2\cos\theta$得$\theta=2\pi/3$。固定向量分别为$(1,1,1)$、$(1,1,-1)$；反对称部分的轴向量分别正比于这两个向量，因$\sin(2\pi/3)>0$，取对应单位向量即给右手角$2\pi/3$。不同轴使作用顺序改变结果，不能把平面旋转角相加律直接用于三维。

**答案原文**

两个乘积不同，轴分别$(1,1,1)/\sqrt3$与$(1,1,-1)/\sqrt3$，右手角均$2\pi/3$。

## 269. draft-c42-03

内容 SHA256：`11115d7f8b3c9ba8d0f7392cf351d95beea10a8a9fb8b93472cd46e42b17158a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft-codex-repair-v4-final.jsonl，第 13 行；源 SHA256 `1b30dc88733b7cf641716e24d00836d421d9b364628fdd5dea63d6b4f987ba1a`。

**题干**

给定$u,v\in\mathbb R^3$，分类将$u$映到$v$的单个过原点平面反射。证明存在性与唯一性条件，并求将$(1,2,2)$映到$(2,1,2)$的反射矩阵。

**过程**

反射保持范数，故必要$\|u\|=\|v\|$。若$u\ne v$且等范数，令$n=(u-v)/\|u-v\|$；由$\|u-v\|^2=2(\|u\|^2-u\cdot v)$得$2(n\cdot u)n=u-v$，所以$H=I-2nn^{\mathsf T}$满足$Hu=v$。反过来任何满足条件的反射都有$u-v=2(n\cdot u)n$，法线必须平行$u-v$，故矩阵唯一。若$u=v\ne0$，任意单位$n\perp u$都给反射，故不唯一；若均为零，任意单位法线都可以。范数不等时无解。指定数据法线$(-1,1,0)/\sqrt2$，得到$H=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}$。

**答案原文**

等范数且不同则唯一；相同则有多种；范数不等无解。指定矩阵交换$x,y$。

## 270. draft-c42-04

内容 SHA256：`4b42892585c87b4565edf51c399cdc163e2e49972610782f16b93e994f1bb66c`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft-codex-repair-v4-final.jsonl，第 14 行；源 SHA256 `1b30dc88733b7cf641716e24d00836d421d9b364628fdd5dea63d6b4f987ba1a`。

**题干**

判断矩阵 $A=\begin{pmatrix}\frac12&\frac{\sqrt3}{2}&0\\-\frac{\sqrt3}{2}&\frac12&0\\0&0&-1\end{pmatrix}$ 是否为正交矩阵；若是，说明其对应的几何变换。

**过程**

前两维块为$R(-\pi/3)$，第三维为$-1$，故$A^{\mathsf T}A=I$、$\det A=-1$。它是绕$z$轴旋转$-\pi/3$与关于$xy$平面反射的可交换复合。特征值为$1/2\pm i\sqrt3/2,-1$，没有$1$，所以没有非零逐点固定向量；$z$轴仍是旋转因子的轴并被整个变换作为集合保持，轴上点变号。不能把“没有逐点固定轴”误说为复合中没有旋转轴。

**答案原文**

正交、行列式$-1$；绕$z$轴旋转$-\pi/3$与$xy$平面反射的复合，无非零固定点。

## 271. draft-c42-05

内容 SHA256：`437401583d9c2f2cd1586b52b381e835b15181a54db013c97cdc62e8a4bcb813`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-15/draft-codex-repair-v4-final.jsonl，第 15 行；源 SHA256 `1b30dc88733b7cf641716e24d00836d421d9b364628fdd5dea63d6b4f987ba1a`。

**题干**

证明:实正交矩阵的特征值的模长为 $1$(实特征值只能为 $\pm1$),且 $\det A=\pm1$;由此说明三维正交变换的分类:行列式为 $+1$ 时是旋转(绕特征值 $1$ 的轴),行列式为 $-1$ 时是旋转与反射的复合。

**过程**

模长:设 $Av=\lambda v$($v$ 为复特征向量)。取共轭转置:$v^{\mathsf H}A^{\mathsf T}Av=\bar\lambda\lambda v^{\mathsf H}v$,而 $A^{\mathsf T}A=I$,故 $v^{\mathsf H}v=|\lambda|^2v^{\mathsf H}v$,得 $|\lambda|=1$。实特征值只能为 $\pm1$。行列式:特征值之积,每个模长为 $1$,而 $\det A$ 为实数,故 $\det A=\pm1$(实矩阵的复特征值共轭成对,乘积为正实数)。三维分类:奇数维实矩阵至少有一个实特征值(实系数特征多项式次数为 $3$,必有实根),即 $\pm1$。若 $\det A=1$:特征值组合(计重数)为 $(1,1,1)$、$(1,-1,-1)$ 或 $(1,e^{i\theta},e^{-i\theta})$,特征值 $1$ 必出现;其对应的特征方向为不动轴,$A$ 在其正交补平面上的限制是行列式为 $+1$ 的二维正交矩阵,即旋转(含 $-I$,即 $180^\circ$ 旋转的情形),故 $A$ 是绕该轴的旋转。若 $\det A=-1$:特征值 $-1$ 必出现(类似枚举),设其单位特征向量为 $v$;在 $v^\perp$ 上,$\det(A|_{v^\perp})=\det A/(-1)=+1$,故 $A|_{v^\perp}$ 是旋转。于是 $A$ 是关于平面 $v^\perp$ 的反射与绕轴 $v$ 旋转的复合。

**答案原文**

证明见解法(模长 $1$ 由 $A^{\mathsf T}A=I$ 得;分类由实特征值存在性与行列式符号得)。

## 272. draft-c43-01

内容 SHA256：`06abddee79423d1800e9350f5dd2a2fa9f576e9ca38e5b06add31bd489fee5c0`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft-codex-repair-v4-final.jsonl，第 1 行；源 SHA256 `ffa0d6f7e9670b2daf11546c5bee6dfb2d0dd84188bb04544bc29541fbc8d60a`。

**题干**

设 $\mathbb R^2$ 的基为 $\eta_1=(1,1)$，$\eta_2=(1,-1)$。求对偶基 $f_1,f_2$，使 $f_i(\eta_j)=\delta_{ij}$。

**过程**

设 $f_1(x,y)=ax+by$。条件:$f_1(\eta_1)=a+b=1$,$f_1(\eta_2)=a-b=0$,解得 $a=b=\frac12$,故 $f_1(x,y)=\frac{x+y}{2}$。设 $f_2(x,y)=cx+dy$。条件:$f_2(\eta_1)=c+d=0$,$f_2(\eta_2)=c-d=1$,解得 $c=\frac12,d=-\frac12$,故 $f_2(x,y)=\frac{x-y}{2}$。验证:$f_1(\eta_1)=\frac{1+1}{2}=1$,$f_1(\eta_2)=0$;$f_2(\eta_1)=0$,$f_2(\eta_2)=1$ ✓。

**答案原文**

$f_1(x,y)=\frac{x+y}{2}$,$f_2(x,y)=\frac{x-y}{2}$。

## 273. draft-c43-02

内容 SHA256：`07e3b61c18b91a397d7d6b60c237d2c016f02be2e7833bf333c8023716f15f6f`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft-codex-repair-v4-final.jsonl，第 2 行；源 SHA256 `ffa0d6f7e9670b2daf11546c5bee6dfb2d0dd84188bb04544bc29541fbc8d60a`。

**题干**

求实线性泛函$f:\mathbb R^3\to\mathbb R$，满足$f(1,0,2)=2$、$f(0,2,1)=-1$、$f(1,2,3)=a$。分类存在性并给全部解，说明为何不能按三个给定值就认为唯一。

**过程**

第三个输入是前两个之和，所以线性性要求$a=1$，否则无解。若$a=1$，设$f(x,y,z)=\alpha x+\beta y+\gamma z$，取$\gamma=t$，前两式给$\alpha=2-2t$、$\beta=(-1-t)/2$。因此全部解$f_t=(2-2t)x-(1+t)y/2+tz$，$t\in\mathbb R$，直接代入三条件成立。两个独立输入只张成二维空间，没有组成三维基，故留下一个自由参数。

**答案原文**

$a=1$才有解；全部$f_t=(2-2t)x-(1+t)y/2+tz$；不唯一。

## 274. draft-c43-03

内容 SHA256：`7e625de562e6cee652f235c705f2c92566186d92a17feb79d4f2d630b1698d77`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft-codex-repair-v4-final.jsonl，第 3 行；源 SHA256 `ffa0d6f7e9670b2daf11546c5bee6dfb2d0dd84188bb04544bc29541fbc8d60a`。

**题干**

在$V=\mathbb R[x]_{\le2}$中取基$1,x,x^2$。求三个多项式$g_0,g_1,g_2$，使$f_i(p)=\int_{-1}^1g_i(x)p(x)\,dx$为此基的对偶泛函，并证明九个配对值。

**过程**

矩阵$G_{ij}=\int_{-1}^1x^{i+j}dx$（$i,j=0,1,2$）为$\begin{pmatrix}2&0&2/3\\0&2/3&0\\2/3&0&2/5\end{pmatrix}$。若$g_i$的系数为矩阵$C$第$i$行，则配对条件为$CG=I$。独立反解或积分核验得$C=\begin{pmatrix}9/8&0&-15/8\\0&3/2&0\\-15/8&0&45/8\end{pmatrix}$，故$g_0=(9-15x^2)/8,g_1=3x/2,g_2=(-15+45x^2)/8$。利用奇次矩积分为零、$\int1=2,\int x^2=2/3,\int x^4=2/5$，相乘给九个配对$\int g_i x^j=\delta_{ij}$。真正的对偶元素是$f_i$，多项式$g_i$是相对于该积分配对的表示。

**答案原文**

$g_0=(9-15x^2)/8,g_1=3x/2,g_2=(-15+45x^2)/8$；$f_i(p)=\int_{-1}^1g_i p$组成对偶基。

## 275. draft-c43-04

内容 SHA256：`1baa057147043a7fe0fa522830a68364138e2fb696e678603eee4a6e96a782ee`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft-codex-repair-v4-final.jsonl，第 4 行；源 SHA256 `ffa0d6f7e9670b2daf11546c5bee6dfb2d0dd84188bb04544bc29541fbc8d60a`。

**题干**

证明对偶配对 $\langle v,f\rangle=f(v)$ 在基变换下不变:设向量 $v$ 与泛函 $f$ 在旧基下的坐标分别为 $x$ 与 $y$，在新基下的坐标分别为 $\tilde x$ 与 $\tilde y$，则 $y^{\mathsf T}x=\tilde y^{\mathsf T}\tilde x$。

**过程**

设新旧基的过渡矩阵为 $P$(新基向量为旧基向量的 $P$ 线性组合),则向量坐标变换为 $x=P\tilde x$(新坐标经 $P$ 得旧坐标)。对偶基的过渡矩阵为 $(P^{-1})^{\mathsf T}$,故泛函坐标变换为 $y=(P^{-1})^{\mathsf T}\tilde y$。于是 $y^{\mathsf T}x=((P^{-1})^{\mathsf T}\tilde y)^{\mathsf T}(P\tilde x)=\tilde y^{\mathsf T}P^{-1}P\tilde x=\tilde y^{\mathsf T}\tilde x$。故配对值与基的选择无关。

**答案原文**

证明见解法(坐标变换 $x=P\tilde x$、$y=(P^{-1})^{\mathsf T}\tilde y$ 代入相消)。

## 276. draft-c43-05

内容 SHA256：`b5375a2c7629c0886d96759b3d49bcebe2e23733005a3d5f7f115587b4e8907e`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft-codex-repair-v4-final.jsonl，第 5 行；源 SHA256 `ffa0d6f7e9670b2daf11546c5bee6dfb2d0dd84188bb04544bc29541fbc8d60a`。

**题干**

设 $V$ 是有限维线性空间。证明 $\dim V^*=\dim V$，并构造自然同构 $\Phi:V\to V^{**}$($\Phi(v)(f)=f(v)$)。

**过程**

取 $V$ 的基 $e_1,\dots,e_n$ 与其对偶基 $e^1,\dots,e^n$($e^i(e_j)=\delta_{ij}$)。任何 $f\in V^*$ 由它在基上的取值唯一确定,且 $f=\sum_i f(e_i)e^i$($e^1,\dots,e^n$ 张成 $V^*$);又 $e^1,\dots,e^n$ 线性无关(若 $\sum c_ie^i=0$,作用于 $e_j$ 得 $c_j=0$)。故 $e^1,\dots,e^n$ 是 $V^*$ 的基,$\dim V^*=n=\dim V$。自然同构:定义 $\Phi(v)(f)=f(v)$。先验证 $\Phi(v)\in V^{**}$:对任意 $f,g\in V^*$ 与 $c$,$\Phi(v)(f+g)=(f+g)(v)=f(v)+g(v)=\Phi(v)(f)+\Phi(v)(g)$,$\Phi(v)(cf)=(cf)(v)=cf(v)=c\Phi(v)(f)$,故 $\Phi(v)$ 是 $V^*$ 上的线性泛函。再验证 $\Phi$ 线性:$\Phi(v_1+v_2)(f)=f(v_1+v_2)=f(v_1)+f(v_2)=\Phi(v_1)(f)+\Phi(v_2)(f)$;$\Phi(cv)(f)=f(cv)=cf(v)=c\Phi(v)(f)$。单射:若 $\Phi(v)=0$,则对一切 $f$,$f(v)=0$。若 $v\neq0$,把它延拓为基 $v=e_1,e_2,\dots,e_n$,取 $f=e^1$,则 $f(v)=1\neq0$,矛盾,故 $v=0$。于是 $\Phi$ 单射,而 $\dim V^{**}=\dim V^*=\dim V$,故 $\Phi$ 为同构。

**答案原文**

证明见解法(对偶基为基、维数相等;$\Phi$ 对 $f$ 与对 $v$ 均线性、单射,维数相同故同构)。

## 277. draft-c44-01

内容 SHA256：`d05e48e1e551497ee72428b5727fa60689055c92feeff0e71f58f91f4c194f10`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft-codex-repair-v4-final.jsonl，第 6 行；源 SHA256 `ffa0d6f7e9670b2daf11546c5bee6dfb2d0dd84188bb04544bc29541fbc8d60a`。

**题干**

在$\mathbb R^4$坐标$(p_1,p_2,q_1,q_2)$中，$J=\begin{pmatrix}0&I_2\\-I_2&0\end{pmatrix}$。分类块剪切$S_B=\begin{pmatrix}I_2&B\\0&I_2\end{pmatrix}$何时保持$\omega(u,v)=u^{\mathsf T}Jv$，并检验$B=\begin{pmatrix}1&2\\2&-1\end{pmatrix}$。

**过程**

矩阵乘法给$S_B^{\mathsf T}JS_B=\begin{pmatrix}0&I_2\\-I_2&B^{\mathsf T}-B\end{pmatrix}$，所以保持形式当且仅当$B^{\mathsf T}=B$。指定$B$对称，故保持。所有$S_B$的行列式均为$1$，但不对称$B$不保持形式；在四维不能以行列式$1$替代辛条件。

**答案原文**

充要条件$B$对称；指定矩阵满足，保持$\omega$。

## 278. draft-c44-02

内容 SHA256：`bf7941050b4048aab7f2540912d1bead5c1dd3d25ae53ed220cfa80bea51a992`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft-codex-repair-v4-final.jsonl，第 7 行；源 SHA256 `ffa0d6f7e9670b2daf11546c5bee6dfb2d0dd84188bb04544bc29541fbc8d60a`。

**题干**

在同一标准四维辛形式$J$下，证明保体积不必保持辛形式：检验$A=\operatorname{diag}(2,1,1,1/2)$，给具体反例向量，并解释二维与四维的差异。

**过程**

$\det A=2\cdot1\cdot1\cdot(1/2)=1$，所以保体积。但$\omega(e_1,e_3)=1$而$\omega(Ae_1,Ae_3)=2$，故不保持辛形式；$\omega(e_2,e_4)$也从$1$变为$1/2$。二维标准交替形式满足$A^{\mathsf T}J_2A=(\det A)J_2$，所以二维行列式$1$足够；四维需要每对配对坐标及交叉项同时满足$A^{\mathsf T}JA=J$，总体积条件不能代替这些约束。

**答案原文**

行列式$1$但非辛，反例$(e_1,e_3)$的形式值从$1$到$2$。

## 279. draft-c44-03

内容 SHA256：`acc12f2fc409be3d54ff58942c9ae967778d4f63b8799282c137bebcbac1d4b7`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft-codex-repair-v4-final.jsonl，第 8 行；源 SHA256 `ffa0d6f7e9670b2daf11546c5bee6dfb2d0dd84188bb04544bc29541fbc8d60a`。

**题干**

在标准四维辛形式$J$下分类可逆对角矩阵$A=\operatorname{diag}(a,b,c,d)$何时为辛矩阵，并检验$(a,b,c,d)=(2,2,1/2,1/2)$。

**过程**

$A^{\mathsf T}JA$的两个配对系数为$ac$与$bd$，所以充要条件$ac=bd=1$，即$a,b\ne0$且$c=1/a,d=1/b$。指定数据满足两个等式，故保持辛形式。条件自动给行列式$1$，但仅行列式$1$不足以推出两配对分别为$1$。

**答案原文**

充要条件$ac=bd=1$；指定矩阵为辛矩阵。

## 280. draft-c44-04

内容 SHA256：`99c8ce694b4373138c1b2bf3fe50edcdbf73318b6d2700372041e2352c241796`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft-codex-repair-v4-final.jsonl，第 9 行；源 SHA256 `ffa0d6f7e9670b2daf11546c5bee6dfb2d0dd84188bb04544bc29541fbc8d60a`。

**题干**

在 $\mathbb R^3$ 上定义 $\omega(u,v)=(u\times v)\cdot e_1$($e_1=(1,0,0)$)。验证 $\omega$ 是交替的，并说明它不是辛形式(退化)。

**过程**

$\omega(u,v)=u_2v_3-u_3v_2$，显然对两变量分别线性，且$\omega(u,u)=0$，所以交替。若它对所有$v$为零，分别取$v=e_3,e_2$得$u_2=u_3=0$；反过来这些条件足够。故核恰为$\operatorname{span}(e_1)$，秩$2$，形式退化，不是辛形式。

**答案原文**

$\omega$ 交替(叉积反交换)但退化($e_1$ 在核中),不是辛形式。

## 281. draft-c44-05

内容 SHA256：`6e323488587a3e4080c05fb2c3814a219f3bb640708f7ddf9e03435ad80289b9`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft-codex-repair-v4-final.jsonl，第 10 行；源 SHA256 `ffa0d6f7e9670b2daf11546c5bee6dfb2d0dd84188bb04544bc29541fbc8d60a`。

**题干**

证明:在数域(特征不为 $2$)上的奇数维线性空间中,不存在非退化的交替双线性形式。

**过程**

设 $V$ 为 $n$ 维空间,$\omega$ 为交替双线性形式,在取定一组基后由斜对称矩阵 $A$ 表示($A^{\mathsf T}=-A$)。$\omega$ 非退化当且仅当 $A$ 可逆。但若 $n$ 为奇数,$\det A=\det(A^{\mathsf T})=\det(-A)=(-1)^n\det A=-\det A$,故 $\det A=0$,$A$ 奇异,即 $\omega$ 必退化。故奇数维空间不存在非退化的交替双线性形式(辛形式只存在于偶数维空间)。

**答案原文**

证明见解法(斜对称矩阵:$\det A=(-1)^n\det A$,奇数维时行列式为零)。

## 282. draft-c45-01

内容 SHA256：`9d5771a05daf342a0d3f4cfbd3f3a1236bf76ceb95920acff7457444af32b511`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft-codex-repair-v4-final.jsonl，第 11 行；源 SHA256 `ffa0d6f7e9670b2daf11546c5bee6dfb2d0dd84188bb04544bc29541fbc8d60a`。

**题干**

证明:若 $A,B$ 相互独立且 $P(A)>0,P(B)>0$，则 $A,B$ 不互斥；若 $A,B$ 互斥且概率均为正，则 $A,B$ 不独立。

**过程**

第一部分:独立给出 $P(A\cap B)=P(A)P(B)>0$(两正数之积),故 $A\cap B\neq\varnothing$,不互斥。第二部分:互斥给出 $P(A\cap B)=0$,而 $P(A)P(B)>0$,故 $P(A\cap B)\neq P(A)P(B)$,不独立(等价地 $P(A|B)=0\neq P(A)$)。结论:独立与互斥是两个不同的概念——独立是概率乘积关系,互斥是集合不相交关系;除退化情形(零概率事件)外两者互斥。

**答案原文**

证明见解法(独立⟹交概率为正⟹不互斥;互斥⟹交概率为零⟹不独立)。

## 283. draft-c45-02

内容 SHA256：`7430f703fde20771796fcbe5482e32e1366aac0c41c36db873f9149fd3202cd2`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft-codex-repair-v4-final.jsonl，第 12 行；源 SHA256 `ffa0d6f7e9670b2daf11546c5bee6dfb2d0dd84188bb04544bc29541fbc8d60a`。

**题干**

用乘法公式(链式法则)求 $P(A\cap B\cap C)$，其中 $P(A)=\frac12$，$P(B|A)=\frac35$，$P(C|A\cap B)=\frac45$。

**过程**

链式法则:$P(A\cap B\cap C)=P(A)\cdot P(B|A)\cdot P(C|A\cap B)=\frac12\times\frac35\times\frac45=\frac{6}{25}$。

**答案原文**

$P(A\cap B\cap C)=\frac{6}{25}$。

## 284. draft-c45-03

内容 SHA256：`0ed5e1469077687cfcfcb40e66c03b00123b2ba78679b3d6b0a43b8881c1c2cb`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft-codex-repair-v4-final.jsonl，第 13 行；源 SHA256 `ffa0d6f7e9670b2daf11546c5bee6dfb2d0dd84188bb04544bc29541fbc8d60a`。

**题干**

独立地抛两枚公平硬币。记 $A=${第一枚正面},$B=${第二枚正面},$C=${两枚同面}。证明 $A,B,C$ 两两独立但整体不独立。

**过程**

$P(A)=P(B)=P(C)=\frac12$。$P(A\cap B)=P(\text{both heads})=\frac14=P(A)P(B)$ ✓。$P(A\cap C)=P(A\cap\text{same face})=P(\text{both heads})=\frac14=P(A)P(C)$ ✓。$P(B\cap C)=\frac14=P(B)P(C)$ ✓。故两两独立。但 $P(A\cap B\cap C)=P(\text{both heads})=\frac14\neq\frac18=P(A)P(B)P(C)$,故整体不独立。

**答案原文**

两两独立($P(A\cap B)=P(A\cap C)=P(B\cap C)=\frac14$),但 $P(A\cap B\cap C)=\frac14\neq\frac18$,整体不独立。

## 285. draft-c45-04

内容 SHA256：`de9ef38d333231c285ecb5a433f4cdbf6f55f90c56a24988da0a813457ea822b`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft-codex-repair-v4-final.jsonl，第 14 行；源 SHA256 `ffa0d6f7e9670b2daf11546c5bee6dfb2d0dd84188bb04544bc29541fbc8d60a`。

**题干**

说明是否存在满足 $P(A|B)=\frac{9}{10}$，$P(A|\bar B)=\frac45$，且 $P(A)=\frac{1}{10}$ 的事件 $A,B$($0<P(B)<1$)；并说明一般情形下 $P(A)$ 必须满足什么约束。

**过程**

记$u=P(A\mid B),v=P(A\mid B^c),q=P(B)\in(0,1)$。全概率公式给$P(A)=qu+(1-q)v$。若$u\ne v$，概率严格位于$\min(u,v)$与$\max(u,v)$之间；若$u=v$，等于共同值。反过来，任何严格介于两者之间的$p$都可取$q=(p-v)/(u-v)\in(0,1)$，用四原子概率$qu,q(1-u),(1-q)v,(1-q)(1-v)$实现。指定$u=9/10,v=4/5$时必有$4/5<P(A)<9/10$，与$P(A)=1/10$矛盾，因此数据不可能。

**答案原文**

指定数据不可能；一般$u\ne v$时$\min(u,v)<P(A)<\max(u,v)$，且区间内任意值可实现。

## 286. draft-c45-05

内容 SHA256：`56483d9eaaea183405a44bc641fb74d600422bd5fcff4c24637428189af218d4`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-16/draft-codex-repair-v4-final.jsonl，第 15 行；源 SHA256 `ffa0d6f7e9670b2daf11546c5bee6dfb2d0dd84188bb04544bc29541fbc8d60a`。

**题干**

证明:给定事件 $B$($P(B)>0$)，条件概率 $P(\cdot|B)$ 是样本空间上的概率测度，并推导全概率公式。

**过程**

验证概率公理:非负性:对任意 $A$,$P(A|B)=\frac{P(A\cap B)}{P(B)}\ge0$。归一性:$P(\Omega|B)=\frac{P(\Omega\cap B)}{P(B)}=\frac{P(B)}{P(B)}=1$。可列可加性:设 $A_1,A_2,\dots$ 两两互斥,则 $P\left(\bigcup_i A_i\,\middle|\,B\right)=\frac{P(\bigcup_i(A_i\cap B))}{P(B)}=\frac{\sum_i P(A_i\cap B)}{P(B)}=\sum_i P(A_i|B)$(用到 $P$ 的可列可加性)。故 $P(\cdot|B)$ 是概率测度。全概率公式:设 $B_1,\dots,B_n$ 构成完备事件组(两两互斥且并为 $\Omega$,$P(B_i)>0$),则 $P(A)=\sum_i P(A\cap B_i)=\sum_i P(A|B_i)P(B_i)$。

**答案原文**

证明见解法(非负/归一/可列可加三公理验证;全概率公式由完备事件组分解得)。

## 287. draft-c47-01

内容 SHA256：`6fe7783b352d549bcc4481f59637213e32b4656dd6f4de0204203d6138a4ee2a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft-codex-repair-v4-final.jsonl，第 1 行；源 SHA256 `231cb8909d898bb52a9d8261eceaec30081c0017c13460bce3496a7148f0d07d`。

**题干**

购买两组彩票，全部彩票是否中奖相互独立：第一组$1000$张，单张中奖率$1/1000$；第二组$1000$张，单张中奖率$1/500$。求总中奖次数恰为$3$的精确概率；再将两组张数均改为$n$、中奖率改为$1/n,2/n$，求对应概率的极限。

**过程**

第一组$X\sim B(1000,1/1000)$，第二组$Y\sim B(1000,1/500)$且独立。卷积给精确概率$\sum_{j=0}^3\binom{1000}{j}(1/1000)^j(999/1000)^{1000-j}\binom{1000}{3-j}(1/500)^{3-j}(499/500)^{997+j}$。极限族取$n\ge3$；对固定$j$，两组点概率分别趋于$e^{-1}/j!$与$e^{-2}2^{3-j}/(3-j)!$，有限求和可交换极限。二项式定理给极限$e^{-3}\sum_{j=0}^3 2^{3-j}/[j!(3-j)!]=(9/2)e^{-3}$。有限精确概率与极限值是不同对象，不能写成等号。

**答案原文**

精确概率为四项卷积和；稀有事件族的极限$(9/2)e^{-3}$。

## 288. draft-c47-02

内容 SHA256：`1641a233d232542444ca5457207bfcaaefcb8af2e2532876d4c42da54ca4ce95`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft-codex-repair-v4-final.jsonl，第 2 行；源 SHA256 `231cb8909d898bb52a9d8261eceaec30081c0017c13460bce3496a7148f0d07d`。

**题干**

设$X\sim B(100,1/100)$。给出$P(X=0)$的精确值，严格比较它与$e^{-1}$，给指数形式的精确误差上界，不作小数计算。

**过程**

$P(X=0)=(99/100)^{100}$。对$0<x<1$，积分$-\ln(1-x)=\int_0^x(1-t)^{-1}dt$，给$x<-\ln(1-x)<x/(1-x)$。代入$x=1/100$并乘$100$得$-100/99<\ln P(X=0)<-1$，所以$e^{-100/99}<P(X=0)<e^{-1}$。因此$0<e^{-1}-P(X=0)<e^{-1}(1-e^{-1/99})$。这些均为严格界，未把极限分布的点概率冒充有限样本真值。

**答案原文**

$(99/100)^{100}$；$e^{-100/99}<P<e^{-1}$，误差严格小于$e^{-1}(1-e^{-1/99})$。

## 289. draft-c47-03

内容 SHA256：`c3b496aa7b13f407973cc45f1d90002fc24ceab2c6a3bb59e6014c9277c2f899`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft-codex-repair-v4-final.jsonl，第 3 行；源 SHA256 `231cb8909d898bb52a9d8261eceaec30081c0017c13460bce3496a7148f0d07d`。

**题干**

证明:当 $n\to\infty$、$p\to0$ 且 $np\to\lambda>0$ 时，对固定的 $k$，$B(n,p)$ 在 $k$ 处的概率趋于 $\frac{\lambda^k}{k!}e^{-\lambda}$。

**过程**

设$k\in\mathbb Z_{\ge0}$固定，$p_n\in[0,1]$且$np_n\to\lambda>0$。则$p_n\to0$，最终$0<p_n<1$。点概率写成$(np_n)^k/k!\cdot\prod_{j=0}^{k-1}(1-j/n)\cdot(1-p_n)^{n-k}$，空乘积为$1$。前两因子分别趋于$\lambda^k/k!$与$1$。由$-p_n/(1-p_n)\le\ln(1-p_n)\le-p_n$，乘$n$并夹逼得$n\ln(1-p_n)\to-\lambda$，又$k\ln(1-p_n)\to0$，故第三因子趋于$e^{-\lambda}$。因此固定$k$的极限为$e^{-\lambda}\lambda^k/k!$，这是极限恒等式，不是每个有限$n$的概率等式。

**答案原文**

证明见解法(三因子分别取极限:$\lambda^k/k!$、$1$、$e^{-\lambda}$)。

## 290. draft-c47-04

内容 SHA256：`6b215157a16458acdd8a21cab41e410864629f0af373b7b3d8f8ff73b27830c4`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft-codex-repair-v4-final.jsonl，第 4 行；源 SHA256 `231cb8909d898bb52a9d8261eceaec30081c0017c13460bce3496a7148f0d07d`。

**题干**

令$X\sim B(2,1/2)$、$Y\sim\operatorname{Pois}(1)$。精确求两离散分布的全变差距离$d_{TV}=\frac12\sum_{k\ge0}|P(X=k)-P(Y=k)|$，说明相同均值不足以保证同分布。

**过程**

两者均值为$1$，方差分别$1/2$与$1$。由$2<e<3$，在$k=0$有$e^{-1}>1/4$，在$k=1$有$1/2>e^{-1}$，在$k=2$有$1/4>1/(2e)$；$k\ge3$仅泊松分布有正质量。总正差等于总负差，故全变差为$[1/2-e^{-1}]+[1/4-1/(2e)]=3/4-3/(2e)>0$。$2<e<3$可由$e=\sum1/j!$与$j!\ge2^{j-1}$（$j\ge2$且部分严格）证明。均值相同不能消除分布差异；也不能把“泊松参数大”当作独立的禁用判据。

**答案原文**

$d_{TV}=3/4-3/(2e)>0$；同均值但方差及分布不同。

## 291. draft-c47-05

内容 SHA256：`02473adb1563b68763e7313b1315c18b792c6288c47d2721fbc7dd062c7d39a2`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft-codex-repair-v4-final.jsonl，第 5 行；源 SHA256 `231cb8909d898bb52a9d8261eceaec30081c0017c13460bce3496a7148f0d07d`。

**题干**

对$X\sim B(50,1/50)$，精确求$P(X\le2)$并证明它严格大于$P(Y\le2)$，其中$Y\sim\operatorname{Pois}(1)$。比较必须由不等式证明，不能查小数表。

**过程**

直接相加三项得$P(X\le2)=(49/50)^{48}[(49/50)^2+49/50+49/100]=(1519/625)(49/50)^{48}$。泊松值为$5/(2e)$。两者比值为$e(49/50)^{48}(3038/3125)$。对$0<x<1$，级数或积分给$\ln(1-x)\ge-x-x^2/[2(1-x)]$；又$\ln(1-y)>-y/(1-y)$。取$x=1/50,y=87/3125$，比值的对数严格大于$1-24/25-12/1225-87/3038=17/10850>0$。故二项概率严格较大；差的精确表达式为$(1519/625)(49/50)^{48}-5/(2e)$。

**答案原文**

$P(X\le2)=(1519/625)(49/50)^{48}>5/(2e)$，差如上。

## 292. draft-c48-01

内容 SHA256：`1784617e7825a0ad59093e41a8eafd5b6bd571b681dbba7645d93866fd089465`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft-codex-repair-v4-final.jsonl，第 6 行；源 SHA256 `231cb8909d898bb52a9d8261eceaec30081c0017c13460bce3496a7148f0d07d`。

**题干**

约定$N(\mu,\sigma^2)$第二参数为方差。设$X\sim N(2,9)$，精确求$P(X>5)$与$E[X\mid X>5]$。记$\phi(t)=e^{-t^2/2}/\sqrt{2\pi}$、$\Phi(t)=\int_{-\infty}^t\phi(s)ds$。

**过程**

标准化$Z=(X-2)/3$给$P(X>5)=1-\Phi(1)>0$。因$\phi^{\prime}(z)=-z\phi(z)$，$E[Z\mathbf1_{Z>1}]=\int_1^\infty z\phi(z)dz=\phi(1)$，边界$\phi(\infty)=0$。所以条件期望为$2+3\phi(1)/(1-\Phi(1))$。这是精确函数表达，不能用查表小数代替。

**答案原文**

$P(X>5)=1-\Phi(1)$；条件期望$2+3\phi(1)/(1-\Phi(1))$。

## 293. draft-c48-02

内容 SHA256：`a4dd1ae3d532f0c96ab62d3769602dc59d24d4a6a6bdd36c000d2566d36ba6be`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft-codex-repair-v4-final.jsonl，第 7 行；源 SHA256 `231cb8909d898bb52a9d8261eceaec30081c0017c13460bce3496a7148f0d07d`。

**题干**

设$Z\sim N(0,1)$。精确给出$P(|Z|\le k)$（$k=1,2,3$）；对任意$k>0$证明双侧尾界$2k\phi(k)/(k^2+1)<P(|Z|>k)<2\phi(k)/k$。

**过程**

对称性给$P(|Z|\le k)=2\Phi(k)-1$。记$I=\int_k^\infty\phi(t)dt$；因$t/k>1$，$I<(1/k)\int_k^\infty t\phi(t)dt=\phi(k)/k$。分部积分得$I=\phi(k)/k-\int_k^\infty\phi(t)/t^2dt$，后项严格小于$I/k^2$，故$I>k\phi(k)/(k^2+1)$。乘$2$即得双侧界。三个覆盖概率分别为$2\Phi(1)-1,2\Phi(2)-1,2\Phi(3)-1$，所有界均有证明，无小数覆盖率。

**答案原文**

覆盖概率$2\Phi(k)-1$；尾界$\frac{2k\phi(k)}{k^2+1}<P(|Z|>k)<\frac{2\phi(k)}k$。

## 294. draft-c48-03

内容 SHA256：`2fb0d4174d2178cc800c7a3d773e2eef62b8d96e909cf520ca40bb150280d344`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft-codex-repair-v4-final.jsonl，第 8 行；源 SHA256 `231cb8909d898bb52a9d8261eceaec30081c0017c13460bce3496a7148f0d07d`。

**题干**

设$X\sim N(\mu,4)$（第二参数为方差）。求使$P(X\le a)=19/20$的唯一$a$，只用精确符号。

**过程**

$\Phi$连续严格递增，取值范围$(0,1)$，所以存在唯一$z=\Phi^{-1}(19/20)$。标准化给$\Phi((a-\mu)/2)=19/20$，故$a=\mu+2\Phi^{-1}(19/20)$；查表的有限小数不能作为该分位数的精确值。

**答案原文**

$a=\mu+2\Phi^{-1}(19/20)$。

## 295. draft-c48-04

内容 SHA256：`1fc31763e8897aa9f868b7be46517d42e50dc0c613e5302e1a214bd740be442a`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft-codex-repair-v4-final.jsonl，第 9 行；源 SHA256 `231cb8909d898bb52a9d8261eceaec30081c0017c13460bce3496a7148f0d07d`。

**题干**

设独立$X\sim N(1,4),Y\sim N(2,9)$。求$S=X+Y,T=2X-Y$的分布及协方差，判断独立性；再求使$S$与$aX-Y$独立的全部实$a$。

**过程**

$S\sim N(3,13)$，$T\sim N(0,25)$，所以$P(T>0)=1/2$。但$\operatorname{Cov}(S,T)=2\operatorname{Var}X-\operatorname{Var}Y=8-9=-1$，故不独立。由于$(S,aX-Y)$联合正态，独立等价于协方差为零，即$4a-9=0$，唯一$a=9/4$。此时$aX-Y\sim N(1/4,117/4)$。联合正态是使用零协方差推出独立的关键，不能推广到任意分布。

**答案原文**

$S\sim N(3,13),T\sim N(0,25)$，协方差$-1$，不独立；唯一$a=9/4$。

## 296. draft-c48-05

内容 SHA256：`7bd86c8ae27c5208d58550e10e1026ee438e5b5c10dbe300109e0660be99997c`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft-codex-repair-v4-final.jsonl，第 10 行；源 SHA256 `231cb8909d898bb52a9d8261eceaec30081c0017c13460bce3496a7148f0d07d`。

**题干**

用特征函数证明:若 $X\sim N(\mu_1,\sigma_1^2)$ 与 $Y\sim N(\mu_2,\sigma_2^2)$ 相互独立，则 $X+Y\sim N(\mu_1+\mu_2,\sigma_1^2+\sigma_2^2)$。

**过程**

正态分布的特征函数为 $\varphi_X(t)=e^{i\mu_1t-\frac{\sigma_1^2t^2}{2}}$。由独立性,和的特征函数为乘积:$\varphi_{X+Y}(t)=\varphi_X(t)\varphi_Y(t)=e^{i\mu_1t-\frac{\sigma_1^2t^2}{2}}\cdot e^{i\mu_2t-\frac{\sigma_2^2t^2}{2}}=e^{i(\mu_1+\mu_2)t-\frac{(\sigma_1^2+\sigma_2^2)t^2}{2}}$。这正是 $N(\mu_1+\mu_2,\sigma_1^2+\sigma_2^2)$ 的特征函数,而特征函数唯一决定分布,故 $X+Y\sim N(\mu_1+\mu_2,\sigma_1^2+\sigma_2^2)$。

**答案原文**

证明见解法(特征函数乘积:$e^{i(\mu_1+\mu_2)t-(\sigma_1^2+\sigma_2^2)t^2/2}$)。

## 297. draft-c49-01

内容 SHA256：`aef1e615084a1eeb3ad1663f6c78a0cf630b44e525650a156533bef508a9ef90`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft-codex-repair-v4-final.jsonl，第 11 行；源 SHA256 `231cb8909d898bb52a9d8261eceaec30081c0017c13460bce3496a7148f0d07d`。

**题干**

设$EX=5,\operatorname{Var}X=1$。求$P(|X-5|\ge3)$的最大可能值，构造达到该值的分布并证明其唯一性。

**过程**

点态有$(X-5)^2\ge9\mathbf1_{|X-5|\ge3}$，取期望给概率不超过$1/9$。等号要求该非负差几乎处处为零，因此$X$只能取$5,2,8$。设后两个概率为$q_-,q_+$，方差要求$9(q_-+q_+)=1$，均值要求$-3q_-+3q_+=0$，故$q_-=q_+=1/18$，$P(X=5)=8/9$。该分布确实达到$1/9$，且上述等号条件证明唯一。

**答案原文**

最大值$1/9$；唯一极值分布在$2,5,8$取概率$1/18,8/9,1/18$。

## 298. draft-c49-02

内容 SHA256：`930e4fb9c86fcfd34a4d360b072c926b7ae5596b71ed26b02f8404d7653865a6`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft-codex-repair-v4-final.jsonl，第 12 行；源 SHA256 `231cb8909d898bb52a9d8261eceaec30081c0017c13460bce3496a7148f0d07d`。

**题干**

说明依概率收敛与几乎必然收敛的区别，并说明大数定律(频率趋于概率)属于哪一种收敛。

**过程**

几乎必然收敛指样本路径极限在概率一集合上成立；依概率收敛指每个$\varepsilon>0$有$P(|X_n-X|>\varepsilon)\to0$。前者使偏差指标逐点趋零，由有界收敛定理推出后者。反例取$\Omega=[0,1)$均匀测度，按$n=2^m+j$（$0\le j<2^m$）定义$X_n=\mathbf1_{[j/2^m,(j+1)/2^m)}$。对$0<\varepsilon<1$，偏差概率$2^{-m}\to0$；但每个样本点在每一层恰有一次取$1$，并在大层有其他取$0$，所以路径不收敛。独立同分布Bernoulli频率的弱大数定律给依概率收敛，强大数定律给几乎必然收敛，必须指明所用版本与假设。

**答案原文**

区别与蕴含关系见解法(几乎必然⟹依概率,反之不然);(弱)大数定律给的是依概率收敛。

## 299. draft-c49-03

内容 SHA256：`a0e8631755f6016f27451723debf400d6e0c1990ebe53f9e5ad59aa9182f0bcf`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft-codex-repair-v4-final.jsonl，第 13 行；源 SHA256 `231cb8909d898bb52a9d8261eceaec30081c0017c13460bce3496a7148f0d07d`。

**题干**

设$X_i$独立同分布于$U(0,1)$，非负权$w_{n,i}$满足$\sum_{i=1}^nw_{n,i}=1$。证明$Y_n=\sum_iw_{n,i}X_i$在$L^2$收敛到$1/2$的充要条件，并对$w_{n,i}=2i/[n(n+1)]$求精确方差及$P(|Y_n-1/2|\ge1/10)$的上界。

**过程**

$EY_n=1/2$，$E|Y_n-1/2|^2=\operatorname{Var}Y_n=\sum_iw_{n,i}^2/12$，故$L^2$收敛当且仅当该平方和趋零。又$(\max_iw_{n,i})^2\le\sum_iw_{n,i}^2\le\max_iw_{n,i}$，所以也等价于最大权趋零。指定权用$\sum i^2=n(n+1)(2n+1)/6$得平方和$2(2n+1)/[3n(n+1)]$，方差$(2n+1)/[18n(n+1)]$。Chebyshev给上界$\min\{1,50(2n+1)/[9n(n+1)]\}$；$n=100$时为$67/606$。

**答案原文**

充要条件$\sum_iw_{n,i}^2\to0$，等价于最大权趋零；方差$(2n+1)/[18n(n+1)]$，上界如上。

## 300. draft-c49-04

内容 SHA256：`5e67c1d6b5460d7a96055ee14874f7fd79d58d36a4d4208f37e6aba277accfe1`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft-codex-repair-v4-final.jsonl，第 14 行；源 SHA256 `231cb8909d898bb52a9d8261eceaec30081c0017c13460bce3496a7148f0d07d`。

**题干**

证明切比雪夫大数定律:若随机变量序列 $X_1,X_2,\dots$ 两两不相关，且存在常数 $C$ 使 $Var(X_i)\le C$ 对一切 $i$ 成立，则 $\frac{1}{n}\sum_{i=1}^{n}(X_i-EX_i)\xrightarrow{P}0$。

**过程**

令 $S_n=\frac1n\sum_{i=1}^{n}(X_i-EX_i)$。$ES_n=0$。由两两不相关,$Var(S_n)=\frac{1}{n^2}\sum_{i=1}^{n}Var(X_i)\le\frac{nC}{n^2}=\frac{C}{n}$(协方差项全为零)。由切比雪夫不等式,对任意 $\varepsilon>0$,$P(|S_n|\ge\varepsilon)\le\frac{Var(S_n)}{\varepsilon^2}\le\frac{C}{n\varepsilon^2}\to0$。故 $S_n\xrightarrow{P}0$。

**答案原文**

证明见解法(两两不相关使方差无交叉项:$Var(S_n)\le C/n\to0$,切比雪夫得依概率收敛)。

## 301. draft-c49-05

内容 SHA256：`5f408dee9a7ba150aa42be2c6cbad9c537d072d379b6d316dadd7d5fb91145b0`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-17/draft-codex-repair-v4-final.jsonl，第 15 行；源 SHA256 `231cb8909d898bb52a9d8261eceaec30081c0017c13460bce3496a7148f0d07d`。

**题干**

证明独立同分布且$E|X_1|<\infty$时样本均值依概率收敛到$\mu=EX_1$，无需有限方差。证明必须说明截断偏差和尾部概率怎样分别控制。

**过程**

令$Y_i^{(M)}=X_i\mathbf1_{|X_i|\le M}$，$\tau_M=E[|X_1|\mathbf1_{|X_1|>M}]\to0$。有$|EY_1^{(M)}-\mu|\le\tau_M$，$E|\overline X_n-\overline Y_n^{(M)}|\le\tau_M$，且独立性给$\operatorname{Var}(\overline Y_n^{(M)})\le M^2/n$。固定$\varepsilon>0$并取$M$使$\tau_M<\varepsilon/3$，三角不等式、Markov与Chebyshev得$P(|\overline X_n-\mu|>\varepsilon)\le3\tau_M/\varepsilon+9M^2/(n\varepsilon^2)$。先对固定$M$令$n\to\infty$，再令$M\to\infty$，上极限为零。该次序避免把随$n$变化的截断界误当一致方差界。

**答案原文**

$E|X_1|<\infty$的独立同分布样本满足$\overline X_n\xrightarrow P\mu$，不需要有限方差。

## 302. draft-c50-01

内容 SHA256：`5f2c9d1c64bd49f69c99a95b6818b0454248b3a4753a7b7ff60c29f3978bf2b3`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-18/draft-codex-repair-v4-final.jsonl，第 1 行；源 SHA256 `1e11739f849a86beae6e173320bb8e62c153af2d88f9f6338bb591da18166aa4`。

**题干**

设独立$X_i\sim U(0,1)$，$S_n=\sum_{i=1}^nX_i$。精确求$P(S_{100}>55)$；另对固定实$a$求$\lim_{n\to\infty}P(S_n>n/2+a\sqrt{n/12})$。

**过程**

连续均匀立方体中，$\sum x_i\le s$的非负单纯形体积为$s^n/n!$；用容斥扣除坐标超过$1$的区域，得到$P(S_n\le s)=\frac1{n!}\sum_{k=0}^{\lfloor s\rfloor}(-1)^k\binom nk(s-k)^n$（$0\le s\le n$）。$S_{100}$与$100-S_{100}$同分布且无原子，所以目标概率为$P(S_{100}<45)=\frac1{100!}\sum_{k=0}^{45}(-1)^k\binom{100}k(45-k)^{100}$，是精确有理数。因单变量均值$1/2$、方差$1/12$，经典CLT给标准化和依分布收敛到$N(0,1)$；正态CDF连续，故极限为$1-\Phi(a)$。CLT的极限不等于固定样本的概率。

**答案原文**

有限概率$\frac1{100!}\sum_{k=0}^{45}(-1)^k\binom{100}k(45-k)^{100}$；极限$1-\Phi(a)$。

## 303. draft-c50-02

内容 SHA256：`494117ec7dbd2c499ad39e6ece19e5380b9089c8de35e2f30c39343c2d046661`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-18/draft-codex-repair-v4-final.jsonl，第 2 行；源 SHA256 `1e11739f849a86beae6e173320bb8e62c153af2d88f9f6338bb591da18166aa4`。

**题干**

公平六面骰独立掷$36$次，点数和$S$。用有限计数精确求$P(S>140)$；再给任意$n$次的中心极限标准化及固定阈值$a$的极限。

**过程**

单次均值$7/2$、方差$35/12$。利用$X\mapsto7-X$，$S$与$252-S$同分布，故$P(S>140)=P(S\le111)$。令$Y_i=X_i-1\in\{0,\ldots,5\}$，需$\sum Y_i\le75$。加一个非负松弛变量，stars-and-bars计数为$\binom{111}{36}$；对超过上界的坐标作容斥，平移每个选中坐标$6$，得到精确概率$6^{-36}\sum_{k=0}^{12}(-1)^k\binom{36}k\binom{111-6k}{36}$。全部样本等可能，故分母$6^{36}$。任意$n$的标准化$(S_n-7n/2)/\sqrt{35n/12}$依分布趋于标准正态，所以$P(S_n>7n/2+a\sqrt{35n/12})\to1-\Phi(a)$，不将有限离散尾写为正态小数。

**答案原文**

$P(S>140)=6^{-36}\sum_{k=0}^{12}(-1)^k\binom{36}k\binom{111-6k}{36}$；标准化极限如上。

## 304. draft-c50-03

内容 SHA256：`94c20666a9dfdc1fa9edae65dd347c8c5e72f496e6b59ddb729506e0c551d886`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-18/draft-codex-repair-v4-final.jsonl，第 3 行；源 SHA256 `1e11739f849a86beae6e173320bb8e62c153af2d88f9f6338bb591da18166aa4`。

**题干**

独立$X_i\sim\operatorname{Exp}(1)$。求$P(S_{100}>110)$的精确式，并证明它；另求固定实$a$时$P(S_n>n+a\sqrt n)$的极限。不得凭未验证小数宣称有限误差很小。

**过程**

卷积或归纳给$S_n$密度$e^{-s}s^{n-1}/(n-1)!$（$s>0$）。对尾积分分部积分，$T_n(t)=e^{-t}t^{n-1}/(n-1)!+T_{n-1}(t)$，$T_1(t)=e^{-t}$，所以$P(S_{100}>110)=e^{-110}\sum_{k=0}^{99}110^k/k!$。这是精确表达，也等于$P(\operatorname{Pois}(110)\le99)$。单变量均值和方差均$1$，CLT给$(S_n-n)/\sqrt n\Rightarrow N(0,1)$，故所求极限$1-\Phi(a)$。该定理本身不提供$n=100$的误差大小，不能据此断言近似“极佳”。

**答案原文**

精确尾$e^{-110}\sum_{k=0}^{99}110^k/k!$；极限$1-\Phi(a)$。

## 305. draft-c50-04

内容 SHA256：`16e8bfdee261639170305b2b451ad1fa41869a9d1357e71be99cbc0127984356`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-18/draft-codex-repair-v4-final.jsonl，第 4 行；源 SHA256 `1e11739f849a86beae6e173320bb8e62c153af2d88f9f6338bb591da18166aa4`。

**题干**

设$X_n\sim B(n,1/2)$。精确写出$P(X_{100}\le55)$；证明整数事件阈值移动半单位的等价性，并对$k_n=\lfloor n/2+a\sqrt n/2\rfloor$证明有无半单位移动都给同一极限。

**过程**

有限精确概率为$2^{-100}\sum_{j=0}^{55}\binom{100}j$。由于$X_n$取整数，对整数$k$有$\{X_n\le k\}=\{X_n\le k+1/2\}$，这只是事件等价。标准化$Z_n=(X_n-n/2)/(\sqrt n/2)$由CLT趋于标准正态。阈值$z_n=(k_n-n/2)/(\sqrt n/2)$满足$|z_n-a|\le2/\sqrt n$，移动半单位后增加$1/\sqrt n$，二者都趋于$a$。用固定$a\pm\varepsilon$夹逼和$\Phi$连续性，得概率极限$\Phi(a)$。有限事件等价不能推出其概率等于某个正态CDF；连续性修正的有限误差是否变小还需额外分析，不能由CLT单独保证。

**答案原文**

精确值$2^{-100}\sum_{j=0}^{55}\binom{100}j$；整数事件可移动半单位，两个标准化阈值均给极限$\Phi(a)$。

## 306. draft-c50-05

内容 SHA256：`766fdb34e1c0eda573ced35d5b6d1d9844f7f395b6d53c54bbec58293e78eca1`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-18/draft-codex-repair-v4-final.jsonl，第 5 行；源 SHA256 `1e11739f849a86beae6e173320bb8e62c153af2d88f9f6338bb591da18166aa4`。

**题干**

说明经典独立同分布中心极限定理的充分矩条件，并以标准柯西分布证明：去掉这些条件后，样本均值不保证集中到常数或趋于正态。明确反例证明的逻辑范围。

**过程**

经典独立同分布CLT的充分条件为$EX=\mu$、$0<\operatorname{Var}X=\sigma^2<\infty$，标准化为$(\sum X_i-n\mu)/(\sigma\sqrt n)$；零方差是退化情形。对标准柯西变量，$E|X|$及$EX^2$发散，均值不存在；特征函数$e^{-|t|}$。独立柯西样本均值的特征函数为$(e^{-|t|/n})^n=e^{-|t|}$，所以仍为标准柯西，且$P(|\overline X_n|\le1)=1/2$对所有$n$成立，不集中到零。密度不超过$1/\pi$，故对任何常数$c$，$P(|\overline X_n-c|\le\pi/8)\le1/4$，也不集中到任何常数。这说明删去矩条件后结论不能普遍保证；它没有证明有限方差是所有正态吸引域或其他规范化极限定理的必要条件。

**答案原文**

柯西样本均值仍为柯西，不集中到常数；有限正方差是经典$\sqrt n$规范化CLT的充分假设，不能由该反例推断所有CLT的必要条件。

## 307. draft-c53-01

内容 SHA256：`5b045db758593b574c7f62a529b256b3f36ab39250035e4dc9faf0e1259b62eb`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-18/draft-codex-repair-v4-final.jsonl，第 6 行；源 SHA256 `1e11739f849a86beae6e173320bb8e62c153af2d88f9f6338bb591da18166aa4`。

**题干**

设$0<p<1$，$P(X=j)=p(1-p)^{j-1}$（$j\ge1$整数）。用可列可加性求$P(X\ge k)$（$k\ge1$整数），并单独说明$p=1$的退化情形。

**过程**

互斥可列分解给$P(X\ge k)=\sum_{j=k}^{\infty}p(1-p)^{j-1}=p(1-p)^{k-1}/[1-(1-p)]=(1-p)^{k-1}$。若$p=1$，直接由$X=1$几乎必然得到$k=1$概率$1$、$k\ge2$概率$0$，无需使用$0^0$。

**答案原文**

$0<p<1$时$P(X\ge k)=(1-p)^{k-1}$；$p=1$时$X=1$几乎必然，$k=1$概率$1$、$k\ge2$概率$0$。

## 308. draft-c53-02

内容 SHA256：`217adb364b75d590e1b9d12d03870ee6a5647984ebc2ccab4b4812baf99c53c7`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-18/draft-codex-repair-v4-final.jsonl，第 7 行；源 SHA256 `1e11739f849a86beae6e173320bb8e62c153af2d88f9f6338bb591da18166aa4`。

**题干**

独立地抛两枚公平硬币。用互斥事件的拆分与可加性求「至少一枚正面朝上」的概率。

**过程**

样本空间 $\Omega=\{HH,HT,TH,TT\}$,四个基本事件互斥且概率各为 $\frac14$。事件 $A=$「至少一枚正面」$=\{HH,HT,TH\}$,由(有限)可加性,$P(A)=P(HH)+P(HT)+P(TH)=\frac14+\frac14+\frac14=\frac34$。

**答案原文**

$P(A)=\frac34$。

## 309. draft-c53-03

内容 SHA256：`0bcd68d4b5bbbcc9eed3fbac85268e2c5b06a30b47295ffcdf637e976225b1db`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-18/draft-codex-repair-v4-final.jsonl，第 8 行；源 SHA256 `1e11739f849a86beae6e173320bb8e62c153af2d88f9f6338bb591da18166aa4`。

**题干**

说明为什么概率公理中的可加性只要求「可列」而不要求「不可列」:以 $[0,1]$ 上的均匀分布为例。

**过程**

非负数族的不可列和可以定义为有限子和的上确界，值属于$[0,+\infty]$；全零族的该和确为零，不能说没有定义。在均匀$[0,1]$测度下，每个单点概率零，全部单点的并为可测全集，概率为$1$，与不可列和$0$不同。因此该概率测度不满足不可列可加性。另一个障碍是σ代数只保证可列并可测，任意不可列并未必可测。概率公理要求可列可加性；失败的是不可列可加等式，不是非负不可列和的定义。

**答案原文**

不可列非负和有定义，但单点零质量的不可列并可有概率$1$；不可列可加性不成立，且任意不可列并未必可测。

## 310. draft-c53-04

内容 SHA256：`bbdeb4e9dd023c20d10909e5b5040ff81cb54aa0a7d72d9042561c365be322a0`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-18/draft-codex-repair-v4-final.jsonl，第 9 行；源 SHA256 `1e11739f849a86beae6e173320bb8e62c153af2d88f9f6338bb591da18166aa4`。

**题干**

设 $X\sim U(0,1)$，$A_n=\{X\ge\frac1n\}$。求 $P(A_n)$ 与 $P\left(\bigcup_{n=1}^{\infty}A_n\right)$，并说明与概率的单调连续性(下连续性)的关系。

**过程**

$P(A_n)=P(X\ge\frac1n)=1-\frac1n$。$\bigcup_{n=1}^{\infty}A_n=\{X>0\}$(对 $X\in(0,1)$ 的样本点,存在 $n$ 使 $X\ge\frac1n$),故 $P\left(\bigcup_nA_n\right)=P(X>0)=1$。另一方面 $A_n$ 单调递增($A_1\subseteq A_2\subseteq\cdots$),由下连续性(可由可列可加性导出),$P(\bigcup_nA_n)=\lim_{n}P(A_n)=\lim(1-\frac1n)=1$。两者一致。

**答案原文**

$P(A_n)=1-\frac1n$;$P(\bigcup_n A_n)=1=\lim P(A_n)$(下连续性,与可列可加性一致)。

## 311. draft-c53-05

内容 SHA256：`bdebee5d42df4f365799380afa043f5ac4e870d8eade3271c527315253643582`。

来源：reviews/2026-10-05-training-diversity-drafts/batch-18/draft-codex-repair-v4-final.jsonl，第 10 行；源 SHA256 `1e11739f849a86beae6e173320bb8e62c153af2d88f9f6338bb591da18166aa4`。

**题干**

设$P$为σ代数上的非负、规范化、有限可加函数。证明可列可加性与下连续性等价。

**过程**

(可列可加⟹下连续)设 $A_n\uparrow A=\bigcup_nA_n$。令 $B_1=A_1$,$B_n=A_n\setminus A_{n-1}$($n\ge2$),则 $B_n$ 两两互斥且 $A=\bigcup_nB_n$,$A_n=\bigcup_{i\le n}B_i$。由可列可加性,$P(A)=\sum_nP(B_n)=\lim_n\sum_{i\le n}P(B_i)=\lim_nP(A_n)$(最后一步用有限可加性)。(下连续⟹可列可加)设 $A_1,A_2,\dots$ 两两互斥,$A=\bigcup_nA_n$。令 $C_n=\bigcup_{i\le n}A_i$,则 $C_n\uparrow A$。由下连续性与有限可加性,$P(A)=\lim_nP(C_n)=\lim_n\sum_{i\le n}P(A_i)=\sum_nP(A_n)$。故在有限可加性下两者等价。

**答案原文**

证明见解法(可列可加⟹下连续:互斥拆分 $B_n=A_n\setminus A_{n-1}$;下连续⟹可列可加:部分并 $C_n\uparrow A$)。
