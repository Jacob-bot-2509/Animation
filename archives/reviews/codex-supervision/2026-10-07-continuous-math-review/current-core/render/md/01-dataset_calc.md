## calc-derivative-001

problem

求函数 $f(x)=x^2$ 在 $x=1$ 处的切线方程。

solution

$f'(x)=2x$，所以 $f'(1)=2$。又因为 $f(1)=1$，所以切线方程为 $y-1=2(x-1)$，化简得 $y=2x-1$。

answer

$y=2x-1$

scene_spec.objects[0]

带有刻度的黑色坐标轴

scene_spec.objects[1]

蓝色抛物线 $y=x^2$

scene_spec.objects[2]

位于 $(1,1)$ 处的黄色圆点（代表切点）

scene_spec.objects[3]

橙色直线 $y=2x-1$（代表切线）

scene_spec.objects[4]

右下角白色文本 $f'(x)=2x$ 和 $y=2x-1$

scene_spec.steps[0]

第一步：动态绘制带有刻度的横纵坐标轴。

scene_spec.steps[1]

第二步：从左侧向右侧，动态绘制出蓝色抛物线 $y=x^2$。

scene_spec.steps[2]

第三步：在坐标 $(1,1)$ 的位置闪烁并显示一个黄色圆点，表示切点。

scene_spec.steps[3]

第四步：从黄色圆点处向外延伸出一条橙色直线，表示切线 $y=2x-1$。

scene_spec.steps[4]

第五步：在画面右下角，用白色字体依次显示导数公式 $f'(x)=2x$ 和切线方程 $y=2x-1$。

## calc-improper-002

problem

判断反常积分 $\int_0^{+\infty} \frac{1}{1+x^2} dx$ 是否收敛，若收敛，求其值。

solution

该积分为无穷限反常积分。根据定义，先求变上限积分：$\int_0^b \frac{1}{1+x^2} dx = [\arctan x]_0^b = \arctan b - \arctan 0 = \arctan b$。再取极限：$\lim_{b \to +\infty} \arctan b = \frac{\pi}{2}$。因为极限存在且为有限常数，故该反常积分收敛。

answer

$\frac{\pi}{2}$

scene_spec.objects[0]

带有刻度的黑色坐标轴

scene_spec.objects[1]

蓝色曲线 $y=\frac{1}{1+x^2}$

scene_spec.objects[2]

黄色半透明填充区域（代表积分面积）

scene_spec.objects[3]

向右移动的红色垂直虚线 $x=b$

scene_spec.objects[4]

右下角动态更新的公式文本 $\lim_{b \to +\infty} \arctan b = \frac{\pi}{2}$

scene_spec.steps[0]

第一步：绘制直角坐标系，用蓝色线条画出从 $x=0$ 开始向右无限延伸的对称单峰曲线 $y=\frac{1}{1+x^2}$。

scene_spec.steps[1]

第二步：从 $x=0$ 开始，在曲线下方动态填充黄色阴影区域，代表变上限积分 $\int_0^b \frac{1}{1+x^2} dx$ 的面积。

scene_spec.steps[2]

第三步：在阴影右侧添加一条红色的垂直虚线 $x=b$，并让这条虚线随着时间缓慢向右移动，代表上限 $b \to +\infty$ 的过程。

scene_spec.steps[3]

第四步：随着红线的移动，引导观众观察黄色阴影面积趋于稳定（不再无限增大），直观体现积分收敛。

scene_spec.steps[4]

第五步：画面右下角依次显示文字推导过程：$\lim_{b \to +\infty} \arctan b = \frac{\pi}{2}$，高亮最终结果。

## calc-param-improper-003

problem

求含参反常积分$I(\alpha) = \int_{0}^{+\infty} e^{-\alpha x}dx$的值（设$\alpha>0$）。

solution

$I(\alpha) = \lim_{b \to +\infty} \int_{0}^{b} e^{-\alpha x} dx = \lim_{b \to  +\infty} \left[  -\frac{1}{\alpha} e^{-\alpha x} \right]_{0}^{b} = \lim_{b \to +\infty}  \frac{1}{\alpha} (1 - e^{-\alpha b }) = \frac{1}{\alpha}$。

answer

$\frac{1}{\alpha}$

scene_spec.objects[0]

带有刻度的白色坐标轴

scene_spec.objects[1]

随参数 $\alpha$ 变化的衰减曲线 $y=e^{-\alpha x}$

scene_spec.objects[2]

滑动参数$\alpha$的滑块图形

scene_spec.objects[3]

曲线下方黄色积分区域高亮

scene_spec.objects[4]

公式文本$I(\alpha) = \frac{1}{\alpha}$

scene_spec.steps[0]

第一步：绘制坐标系，先展示$\alpha =1$时的标准指数衰减曲线$y=e^{-x}$。

scene_spec.steps[1]

第二步：在屏幕上方显示一个“参数滑块”，动态演示改变$\alpha$的值。

scene_spec.steps[2]

第三步：随着参数滑块的移动，曲线随之变陡或变平，展示$\alpha$对衰减速度的影响。

scene_spec.steps[3]

第四步：在曲线下方持续保持黄色面积填充，直观展示面积随参数$\alpha$的变化情况。

scene_spec.steps[4]

第五步：画面清晰显示推导过程$\lim_{b\to +\infty} \int_{0}^{b} e^{-\alpha x}dx=\frac{1}{\alpha}$。

## calc-double-integral-004

problem

利用二重积分的几何意义，说明 $\iint_D (1 - x^2 - y^2) dxdy$ 的值，其中 $D$ 是单位圆盘 $x^2 + y^2 \le 1$。

solution

这是一个二重积分，其几何意义是以区域 $D$ 为底，曲面 $z = 1 - x^2 - y^2$ 为顶的曲顶柱体的体积。区域 $D$ 是半径为 $1$ 的圆盘，面积为 $\pi$。在柱坐标系下，该体积可以通过极坐标计算：$\iint_D (1 - x^2 - y^2) dxdy = \int_{0}^{2\pi} d\theta \int_{0}^{1} (1 - r^2) r dr = 2\pi \left[ \frac{r^2}{2} - \frac{r^4}{4} \right]_{0}^{1} = 2\pi \times \frac{1}{4} = \frac{\pi}{2}$。

answer

$\frac{\pi}{2}$

scene_spec.objects[0]

三维空间直角坐标系 $O-xyz$

scene_spec.objects[1]

三维曲面 $z=1-x^2-y^2$（蓝色半透明，位于 $xOy$ 平面上方）

scene_spec.objects[2]

底部的单位圆盘区域 $D$（黄色平面）

scene_spec.objects[3]

从底面圆盘向上垂直延伸的细密立柱阵列（代表微元分割 $dxdy$）

scene_spec.objects[4]

右侧三维悬浮公式 $V = \iint_D (1 - x^2 - y^2) dxdy = \frac{\pi}{2}$

scene_spec.steps[0]

第一步：初始化三维视角，缓慢旋转镜头，展示三维坐标系 $O-xyz$ 以及底部平面上的单位圆盘区域 $D$（黄色高亮）。

scene_spec.steps[1]

第二步：从底面区域 $D$ 开始，动态向上绘制蓝色的三维曲面 $z=1-x^2-y^2$。

scene_spec.steps[2]

第三步：在底面区域 $D$ 内，生成大量细密的垂直立柱，这些立柱的顶部均与蓝色曲面相交。

scene_spec.steps[3]

第四步：镜头缓慢拉近并旋转到侧上方视角，让观众清晰看到这些由底面积和曲面高度构成的曲顶柱体。

scene_spec.steps[4]

第五步：动态展示微元叠加过程，利用动画将所有立柱的体积凝聚成一个整体的体积概念。

scene_spec.steps[5]

第六步：画面右侧悬浮显示计算过程和最终结果 $V = \frac{\pi}{2}$。

## calc-green-005

problem

利用格林公式计算曲线积分 $\oint_L x dy - y dx$，其中 $L$ 是正向圆周 $x^2 + y^2 = a^2$。（设 $a>0$。）

solution

设 $P(x,y) = -y$，$Q(x,y) = x$。则 $\frac{\partial Q}{\partial x} = 1$，$\frac{\partial P}{\partial y} = -1$。由格林公式，原积分 $= \iint_D \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) dxdy = \iint_D (1 - (-1)) dxdy = 2 \iint_D dxdy$。因为 $\iint_D dxdy$ 等于圆盘的面积 $\pi a^2$，所以原积分 $= 2 \pi a^2$。

answer

$2\pi a^2$

scene_spec.objects[0]

直角坐标系

scene_spec.objects[1]

红色圆周曲线 $L$，带有逆时针方向箭头

scene_spec.objects[2]

内部区域 $D$ 的蓝色半透明填充

scene_spec.objects[3]

圆内区域的向量场箭头（代表 $P$ 和 $Q$ 的分量）

scene_spec.objects[4]

右侧文字公式 $\oint_L P dx + Q dy = \iint_D \left( \frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y} \right) dxdy$

scene_spec.steps[0]

第一步：画出直角坐标系，用红色绘制一个以原点为圆心、半径为 $a$ 的圆形路径 $L$。

scene_spec.steps[1]

第二步：在圆的边界上添加逆时针方向的红色箭头，标出正向路径。

scene_spec.steps[2]

第三步：用蓝色半透明颜色填充圆内部的区域 $D$，代表边界 $L$ 围成的闭区域。

scene_spec.steps[3]

第四步：在圆的区域内随机绘制一些微小的向量箭头，示意在向量场中每个点的方向。

scene_spec.steps[4]

第五步：画面右侧同步展示偏导数计算推导：$\frac{\partial Q}{\partial x} = 1$，$\frac{\partial P}{\partial y} = -1$。

scene_spec.steps[5]

第六步：高亮显示格林公式等式，并强调左边的边界积分等价于右边区域的二重积分，最终展现结果 $2\pi a^2$。

## calc-limit-006

problem

求极限 $\lim_{x \to 0} \frac{\sin x}{x}$ 的值。

solution

利用夹逼定理（Squeeze Theorem）进行几何证明。在单位圆中，设圆心角为 $x$（$0 < x < \frac{\pi}{2}$），比较 $\triangle OAB$、扇形 $OAB$ 和 $\triangle OAC$ 的面积。可以推导出不等式 $\sin x < x < \tan x$。同时除以 $\sin x$ 得到 $1 < \frac{x}{\sin x} < \frac{1}{\cos x}$。取倒数得 $\cos x < \frac{\sin x}{x} < 1$。由于 $\frac{\sin x}{x}$ 为偶函数，$x \to 0^-$ 时结论同样成立。当 $x \to 0$ 时，$\cos x \to 1$，由夹逼定理可得 $\lim_{x \to 0} \frac{\sin x}{x} = 1$。

answer

1

scene_spec.objects[0]

单位圆，$O=(0,0)$，$A=(1,0)$

scene_spec.objects[1]

参数点 $B=(\cos x,\sin x)$，$0<x<\frac{\pi}{2}$

scene_spec.objects[2]

交点 $C=(1,\tan x)$，射线 $OB$ 与 $A$ 处切线相交

scene_spec.objects[3]

三块区域及精确面积 $\frac12\sin x,\frac12 x,\frac12\tan x$

scene_spec.steps[0]

初始角取 $x=\frac{\pi}{4}$；之后在 $0<x<\frac{\pi}{2}$ 内变化。

scene_spec.steps[1]

展示 $\triangle OAB\subsetneq$ 扇形 $OAB\subsetneq\triangle OAC$，由面积得 $\sin x<x<\tan x$。

scene_spec.steps[2]

由 $\sin x>0$ 得 $\cos x<\frac{\sin x}{x}<1$；显示 $\lim_{x\to0^+}\cos x=1$。

scene_spec.steps[3]

以偶性 $\frac{\sin(-x)}{-x}=\frac{\sin x}{x}$ 得双侧极限 $1$。有限动画仅说明包含关系，极限结论由夹逼定理给出。

## calc-area-007

problem

计算由抛物线 $y=x^2$ 与直线 $y=x+2$ 所围成的封闭图形的面积。

solution

联立方程 $y=x^2$ 与 $y=x+2$ 得交点 $(-1,1)$ 和 $(2,4)$。在区间 $[-1,2]$ 内，直线 $y=x+2$ 在抛物线 $y=x^2$ 的上方，故面积 $S = \int_{-1}^{2} [(x+2) - x^2] dx = [\frac{x^2}{2} + 2x - \frac{x^3}{3}]_{-1}^{2} = \frac{9}{2}$。

answer

$\frac{9}{2}$

scene_spec.objects[0]

带有刻度的黑色直角坐标系

scene_spec.objects[1]

蓝色抛物线 $y=x^2$

scene_spec.objects[2]

红色直线 $y=x+2$

scene_spec.objects[3]

两曲线围成的黄色半透明填充区域

scene_spec.objects[4]

沿x轴滑动的矩形面积微元

scene_spec.steps[0]

第一步：绘制直角坐标系，用蓝色绘制抛物线 $y=x^2$，用红色绘制直线 $y=x+2$。

scene_spec.steps[1]

第二步：标出两曲线的交点 $(-1,1)$ 和 $(2,4)$，并将围成的封闭区域用黄色半透明填充。

scene_spec.steps[2]

第三步：在区域内绘制从下曲线到上曲线的垂直细窄矩形条，代表微元 $dS = (y_2 - y_1) dx$。

scene_spec.steps[3]

第四步：让矩形微元从左向右扫过整个区域，展示定积分的累积过程。

scene_spec.steps[4]

第五步：展示计算过程，高亮显示面积结果 $S = \frac{9}{2}$。

## calc-area-008

problem

计算由极坐标方程 $r = 2a\cos\theta$（$a>0$）所围成的图形的面积。

solution

该方程表示圆心在 $(a,0)$、半径为 $a$ 的圆。在极坐标中，$r = 2a\cos\theta \ge 0$，因此角度 $\theta$ 的取值范围为 $[-\frac{\pi}{2}, \frac{\pi}{2}]$。面积 $S = \frac{1}{2} \int_{-\pi/2}^{\pi/2} r^2 d\theta = \frac{1}{2} \int_{-\pi/2}^{\pi/2} (2a\cos\theta)^2 d\theta = \frac{1}{2} \int_{-\pi/2}^{\pi/2} 4a^2 \cos^2\theta d\theta = 2a^2 \int_{-\pi/2}^{\pi/2} \frac{1+\cos2\theta}{2} d\theta = a^2 [\theta + \frac{1}{2}\sin2\theta]_{-\pi/2}^{\pi/2} = a^2 [\frac{\pi}{2} - (-\frac{\pi}{2})] = \pi a^2$。

answer

$\pi a^2$

scene_spec.objects[0]

极坐标系

scene_spec.objects[1]

极坐标曲线 $r = 2a\cos\theta$ 所围成的圆形

scene_spec.objects[2]

从原点出发扫过的射线

scene_spec.objects[3]

由两条射线和一个圆弧围成的扇形微元

scene_spec.steps[0]

第一步：绘制极坐标系，动态画出极坐标曲线 $r = 2a\cos\theta$，它恰好是一个过原点、圆心在 x 轴上的圆。

scene_spec.steps[1]

第二步：从原点出发，绘制一条与极轴夹角为 $\theta$ 的射线，明确标注 $\theta$ 的有效范围为 $[-\frac{\pi}{2}, \frac{\pi}{2}]$。

scene_spec.steps[2]

第三步：让射线从 $-\pi/2$ 逆时针扫过至 $\pi/2$，追踪它扫过的圆形区域。

scene_spec.steps[3]

第四步：在扫过时，标出由夹角 $d\theta$ 构成的微小扇形，展示面积微元 $\frac{1}{2} r^2 d\theta$。

scene_spec.steps[4]

第五步：显示最终的面积计算结果 $\pi a^2$。

## calc-area-009

problem

求摆线 $x = a(t - \sin t), y = a(1 - \cos t)$ 的一拱（$0 \le t \le 2\pi$）与 $x$ 轴所围成的面积。（设 $a>0$。）

solution

摆线的一拱与 $x$ 轴围成封闭图形。面积 $S = \int_{0}^{2\pi a} y dx$。将参数方程代入，得 $S = \int_{0}^{2\pi} a(1 - \cos t) \cdot d[a(t - \sin t)] = \int_{0}^{2\pi} a(1 - \cos t) \cdot a(1 - \cos t) dt = a^2 \int_{0}^{2\pi} (1 - 2\cos t + \cos^2 t) dt$。利用三角函数积分性质，其中 $\cos t$ 在周期内积分为0，故 $S = a^2 \int_{0}^{2\pi} (1 + \frac{1+\cos 2t}{2}) dt = a^2 \cdot 3\pi = 3\pi a^2$。

answer

$3\pi a^2$

scene_spec.objects[0]

带有刻度的黑色直角坐标系

scene_spec.objects[1]

蓝色摆线一拱的轨迹

scene_spec.objects[2]

摆线与x轴围成的黄色半透明区域

scene_spec.objects[3]

参数t动态变化指示点

scene_spec.objects[4]

沿x轴滚动的圆

scene_spec.steps[0]

第一步：绘制直角坐标系，在x轴上画一个沿着x轴滚动的圆。

scene_spec.steps[1]

第二步：通过圆边缘的一个固定点，随着圆滚动，动态描绘出摆线的一拱轨迹 $x = a(t - \sin t), y = a(1 - \cos t)$。

scene_spec.steps[2]

第三步：当圆滚过一个完整周期（$0 \le t \le 2\pi$）后，摆线与x轴围成了一个封闭的拱形区域，用黄色半透明填充。

scene_spec.steps[3]

第四步：展示公式推导，强调变量替换过程，将 $y$ 和 $dx$ 均用参数 $t$ 的表达式替换。

scene_spec.steps[4]

第五步：高亮显示最终的面积结果 $3\pi a^2$。

## calc-area-010

problem

计算由曲线 $y=\ln x$、直线 $y=-x+e+1$ 以及 $x$ 轴围成的封闭图形的面积。

solution

联立 $y=\ln x$ 与 $y=-x+e+1$ 得交点为 $(e, 1)$。该封闭图形以 $x$ 轴为下边界，由两部分组成：在 $[1, e]$ 上，上边界为曲线 $y=\ln x$；在 $[e, e+1]$ 上，上边界为直线 $y=-x+e+1$。面积 $S = \int_1^e \ln x dx + \int_e^{e+1} (-x+e+1) dx$。第一项：$\int_1^e \ln x dx = [x\ln x - x]_1^e = (e - e) - (0 - 1) = 1$。第二项：$\int_e^{e+1} (-x+e+1) dx = [-\frac{1}{2}x^2 + (e+1)x]_e^{e+1} = \frac{1}{2}$。总面积 $S = 1 + \frac{1}{2} = \frac{3}{2}$。

answer

$\frac{3}{2}$

scene_spec.objects[0]

带有刻度的直角坐标系

scene_spec.objects[1]

蓝色对数曲线 $y=\ln x$

scene_spec.objects[2]

红色直线 $y=-x+e+1$

scene_spec.objects[3]

由两条曲线和 x 轴围成的封闭区域（黄色填充）

scene_spec.objects[4]

区分 $[1,e]$ 与 $[e,e+1]$ 的分段垂直虚线

scene_spec.objects[5]

垂直微元矩形

scene_spec.steps[0]

第一步：绘制直角坐标系，用蓝色画出对数曲线 $y=\ln x$，用红色画出直线 $y=-x+e+1$。

scene_spec.steps[1]

第二步：标出交点 $(e, 1)$，以及曲线与 x 轴的交点 $(1, 0)$ 和直线与 x 轴的交点 $(e+1, 0)$。

scene_spec.steps[2]

第三步：用黄色半透明填充由曲线、直线和 x 轴围成的封闭区域，并用垂直虚线将区域分为 $[1, e]$ 和 $[e, e+1]$ 两部分。

scene_spec.steps[3]

第四步：在区域中动态绘制垂直微元，分别展示两部分面积积分 $S_1$ 和 $S_2$。

scene_spec.steps[4]

第五步：高亮显示面积计算结果 $S = \frac{3}{2}$。

## calc-area-011

problem

计算由曲线 $y = |x^2 - 1|$ 与直线 $y = 1$ 所围成的封闭图形的面积。

solution

曲线 $y = |x^2 - 1|$ 与直线 $y = 1$ 的交点为 $x = 0$ 和 $x = \pm\sqrt{2}$。因为图形关于y轴对称，可以计算右半部分 $[0, \sqrt{2}]$ 的面积再乘以2。当 $0 \le x \le 1$ 时，$y = 1 - x^2$，当 $1 \le x \le \sqrt{2}$ 时，$y = x^2 - 1$。面积 $S = 2 \left( \int_0^1 (1 - (1-x^2)) dx + \int_1^{\sqrt{2}} (1 - (x^2-1)) dx \right) = 2 \left( \int_0^1 x^2 dx + \int_1^{\sqrt{2}} (2 - x^2) dx \right) = 2 \left( \frac{1}{3} + (2x - \frac{x^3}{3})|_1^{\sqrt{2}} \right) = 2 \left( \frac{1}{3} + (2\sqrt{2} - \frac{2\sqrt{2}}{3}) - (2 - \frac{1}{3}) \right) = 2 \left( \frac{1}{3} + \frac{4\sqrt{2}}{3} - \frac{5}{3} \right) = \frac{8(\sqrt{2}-1)}{3}$。

answer

$\frac{8(\sqrt{2}-1)}{3}$

scene_spec.objects[0]

带有刻度的黑色直角坐标系

scene_spec.objects[1]

红色绝对值曲线 $y=|x^2-1|$

scene_spec.objects[2]

蓝色水平直线 $y=1$

scene_spec.objects[3]

两曲线围成的黄色半透明填充区域

scene_spec.objects[4]

沿着x轴滑动的微元矩形

scene_spec.steps[0]

第一步：绘制直角坐标系，用蓝色画出直线 $y=1$。

scene_spec.steps[1]

第二步：先画出抛物线 $y=x^2-1$，然后将x轴下方的部分向上翻折，形成红色的绝对值曲线 $y=|x^2-1|$。

scene_spec.steps[2]

第三步：标出交点 $x=0, \pm\sqrt{2}$，并用黄色半透明填充直线与绝对值曲线围成的区域。

scene_spec.steps[3]

第四步：在区域中划分两个部分：$[0,1]$ 和 $[1, \sqrt{2}]$，分别用垂直细条扫过，展示分段积分的微元。

scene_spec.steps[4]

第五步：右侧展示对称性，乘以2，并显示最终结果 $\frac{8(\sqrt{2}-1)}{3}$。

## calc-vol-012

problem

求曲线 $y = \arcsin x$（$0 \le x \le 1$）与x轴、直线 $x=1$ 围成的图形绕x轴旋转一周所得旋转体的体积。

solution

使用圆盘法，体积 $V = \pi \int_0^1 (\arcsin x)^2 dx$。用分部积分法计算不定积分：令 $u=(\arcsin x)^2$，$dv=dx$，则 $du=\frac{2\arcsin x}{\sqrt{1-x^2}}dx$，$v=x$，于是 $\int (\arcsin x)^2 dx = x(\arcsin x)^2 - \int \frac{2x\arcsin x}{\sqrt{1-x^2}} dx = x(\arcsin x)^2 + 2\sqrt{1-x^2}\arcsin x - 2x$。代入上下限得 $V = \pi [1 \cdot (\frac{\pi}{2})^2 + 0 - 2] - \pi [0 + 0 - 0] = \pi(\frac{\pi^2}{4} - 2) = \frac{\pi^3}{4} - 2\pi$。

answer

$\frac{\pi^3}{4} - 2\pi$

scene_spec.objects[0]

二维直角坐标系

scene_spec.objects[1]

蓝色反三角函数曲线 $y=\arcsin x$

scene_spec.objects[2]

曲线与x轴、直线 $x=1$ 围成的平面图形

scene_spec.objects[3]

三维空间

scene_spec.objects[4]

绕x轴旋转生成的三维立体

scene_spec.objects[5]

垂直于x轴的红色圆盘微元

scene_spec.objects[6]

右侧分部积分推导公式

scene_spec.steps[0]

第一步：在二维坐标系中绘制曲线 $y = \arcsin x$，用黄色填充它与 $x=1$ 及x轴围成的区域。

scene_spec.steps[1]

第二步：将场景切换至三维视角，展示该平面区域绕x轴旋转一周的动态过程。

scene_spec.steps[2]

第三步：旋转完成后，生成一个连续的三维旋转体。

scene_spec.steps[3]

第四步：在x轴上从0到1滑动，展示垂直于x轴的红色圆盘微元，演示 $dV = \pi y^2 dx$。

scene_spec.steps[4]

第五步：展示定积分的分部积分计算过程，高亮最终结果 $\frac{\pi^3}{4} - 2\pi$。

scene_spec.steps[5]

第六步：配合右侧公式推导，展示圆盘微元积分过程。

## calc-area-013

problem

计算由曲线 $y = x e^{-x}$、直线 $x = 1$ 以及x轴围成的封闭图形的面积。

solution

面积 $S = \int_0^1 x e^{-x} dx$。使用分部积分法，令 $u = x$，$dv = e^{-x} dx$，则 $du = dx$，$v = -e^{-x}$。$S = [-x e^{-x}]_0^1 - \int_0^1 (-e^{-x}) dx = -1 \cdot e^{-1} - 0 + [-e^{-x}]_0^1 = -e^{-1} - (e^{-1} - 1) = 1 - \frac{2}{e}$。

answer

$1 - \frac{2}{e}$

scene_spec.objects[0]

带有刻度的黑色直角坐标系

scene_spec.objects[1]

蓝色复合曲线 $y=x e^{-x}$

scene_spec.objects[2]

x轴和直线 $x=1$

scene_spec.objects[3]

黄色半透明填充区域

scene_spec.objects[4]

沿x轴滑动的微元矩形

scene_spec.steps[0]

第一步：绘制直角坐标系，用蓝色动态描绘复合函数曲线 $y = x e^{-x}$。

scene_spec.steps[1]

第二步：标记出区间 $[0, 1]$，并用黄色半透明填充曲线、直线 $x=1$ 和x轴围成的区域。

scene_spec.steps[2]

第三步：从0到1动态画出垂直细窄矩形，展示微元面积 $dS = y dx$。

scene_spec.steps[3]

第四步：画面展示分部积分的推导过程，明确 $u$ 和 $dv$ 的选择。

scene_spec.steps[4]

第五步：高亮显示最终面积结果 $1 - \frac{2}{e}$。

## calc-series-015

problem

讨论级数 $\sum_{n=1}^{\infty} \frac{(-1)^n}{\sqrt{n}}$ 的敛散性，并指出是绝对收敛还是条件收敛。

solution

设 $u_n=1/\sqrt n$，则 $u_{n+1}\le u_n$ 且 $\lim_{n\to\infty}u_n=0$。由莱布尼茨判别法，$\sum_{n=1}^{\infty}(-1)^n u_n$ 收敛。若和为 $S$、前 $N$ 项和为 $S_N$，则 $|S-S_N|\le 1/\sqrt{N+1}$。绝对值级数满足 $\sum_{n=1}^{N}1/\sqrt n\ge\int_1^{N+1}x^{-1/2}\,dx=2(\sqrt{N+1}-1)\to+\infty$，即 $p=\frac{1}{2}\le1$ 的 $p$ 级数发散。因此原级数条件收敛。

answer

条件收敛

scene_spec.objects[0]

交错项与部分和

scene_spec.objects[1]

精确余项界

scene_spec.objects[2]

绝对值部分和的积分下界

scene_spec.steps[0]

令 $u_n=1/\sqrt n$，标注 $u_n\downarrow0$，由莱布尼茨判别法得到交错级数收敛。

scene_spec.steps[1]

部分和图用于示意，并显示精确界 $|S-S_N|\le1/\sqrt{N+1}$。

scene_spec.steps[2]

显示 $\sum_{n=1}^Nn^{-1/2}\ge\int_1^{N+1}x^{-1/2}\,dx=2(\sqrt{N+1}-1)\to+\infty$。

scene_spec.steps[3]

用以上证明判定条件收敛；有限动画不能代替无穷极限证明。

## calc-series-017

problem

讨论函数项级数 $\sum_{n=1}^{\infty} \frac{x^n}{n^2}$ 在区间 $[-1, 1]$ 上是否一致收敛。

solution

对任意 $x \in [-1, 1]$，有 $|x| \le 1$，因此 $\left| \frac{x^n}{n^2} \right| \le \frac{1}{n^2}$。由于正项级数 $\sum_{n=1}^{\infty} \frac{1}{n^2}$ 收敛（p 级数，p=2>1），根据魏尔斯特拉斯判别法（M-判别法），原函数项级数在 $[-1, 1]$ 上一致收敛。

answer

一致收敛

scene_spec.objects[0]

坐标轴

scene_spec.objects[1]

上下界直线

scene_spec.objects[2]

部分和曲线族

scene_spec.objects[3]

高项数部分和参考曲线（$N=200$）

scene_spec.steps[0]

第一步：绘制直角坐标系，用浅灰色画出两条上下对称的界直线 $y = \pm \sum_{n=1}^{\infty} \frac{1}{n^2} = \pm \frac{\pi^2}{6}$。

scene_spec.steps[1]

第二步：依次绘制前1项、前3项、前5项、前20项的部分和曲线，用不同颜色区分。

scene_spec.steps[2]

第三步：展示随着项数 $N$ 增大，部分和曲线的“波动”完全被限制在上下界直线之间。

scene_spec.steps[3]

第四步：高亮展示随着 $N$ 增大，部分和曲线在区间 $[-1,1]$ 上一致逼近极限函数（以高项数部分和 $N=200$ 作为极限函数的近似参考曲线）。

scene_spec.steps[4]

第五步：右侧展示 M-判别法的数学推导过程，强调 $\frac{1}{n^2}$ 起到的“控制”作用。

## calc-series-020

problem

将函数 $f(x) = x$（$-\pi \le x \le \pi$）展开为傅立叶级数。

solution

$f(x)=x$ 为奇函数，故 $a_0=a_n=0$。分部积分得 $b_n=\frac{2}{\pi}\int_0^\pi x\sin(nx)\,dx=\frac{2}{\pi}[-\frac{x\cos(nx)}{n}+\frac{\sin(nx)}{n^2}]_0^\pi=\frac{2(-1)^{n+1}}{n}$。令 $S(x)=2\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n}\sin(nx)$。由傅里叶收敛定理，对 $-\pi<x<\pi$ 有 $S(x)=x$；在 $x=\pm\pi$，周期延拓的左右极限为 $\pi$ 与 $-\pi$，级数收敛到其中值 $0$，并不等于题中端点所指定的 $\pm\pi$。事实上每个有限部分和在这两个端点也恰为 $0$。

answer

$S(x)=2\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n}\sin(nx)$；$-\pi<x<\pi$ 时 $S(x)=x$，$x=\pm\pi$ 时 $S(x)=0$。

scene_spec.objects[0]

正弦部分和与内部直线

scene_spec.objects[1]

端点和函数值的分开标注

scene_spec.objects[2]

跳跃附近的局部放大

scene_spec.steps[0]

显示 $b_n=2(-1)^{n+1}/n$，定义 $S_N(x)=2\sum_{n=1}^N(-1)^{n+1}\sin(nx)/n$。

scene_spec.steps[1]

对 $-\pi<x<\pi$，标注 $\lim_{N\to\infty}S_N(x)=x$；有限部分和仅作为示意。

scene_spec.steps[2]

在 $x=\pm\pi$ 单独标注每个 $S_N(\pm\pi)=0$，以及跳跃左右极限中值 $(\pi-\pi)/2=0$。

scene_spec.steps[3]

明确端点的级数和为 $0$，与题中函数的端点值 $\pm\pi$ 区分。

scene_spec.steps[4]

吉布斯振荡发生在跳跃点附近，不把峰放在端点本身；端点的部分和仍为 $0$。
