# Batch 3 independent review material


## draft-c02-04

P: 设$a,b>0$。证明$\int_0^{\infty}(e^{-ax}-e^{-bx})/x\,dx$收敛并求精确值；说明交换积分的依据及为什么不能把它拆成两个广义积分之差。

S: 对$x>0$有精确恒等式$(e^{-ax}-e^{-bx})/x=\int_a^be^{-tx}\,dt$。若$a<b$，二重被积函数非负，Tonelli定理允许交换积分，得$\int_a^b\int_0^{\infty}e^{-tx}\,dx\,dt=\int_a^b1/t\,dt=\ln(b/a)<\infty$；所以原积分绝对收敛。若$a>b$，交换二参数取负；若$a=b$，被积函数恒为零。亦可直接给上界：近零绝对值不超过$|b-a|$，而$R>0$后的绝对尾积分不超过$|b-a|e^{-\min(a,b)R}/\min(a,b)$。每个单独的$e^{-ax}/x$在零点附近与$1/x$具有同阶正下界，故从零开始积分发散；原式依赖抵消，不能写成两个未定义的发散积分之差。

A: 对所有$a,b>0$均绝对收敛，积分精确等于$\ln(b/a)$。

Objects: 恒等式卡:$(e^{-ax}-e^{-bx})/x=\int_a^b e^{-tx}\,dt$ 的推导 | 板书一:内层积分 $[-\frac{e^{-tx}}t]_0^\infty=\frac1t$ 与外层 $[\ln t]_a^b$ | 高亮框:关键点——Tonelli 交换依据(非负);尾界依据 $|e^{-u}-e^{-v}|\le|u-v|$ | 参数处理卡:$a>b$ 交换取负、$a=b$ 恒零 | 结论卡:绝对收敛,值 $\ln\frac ba$;不能拆成两个发散积分之差

Steps:
第一步:精确恒等式(逐步):对 $x>0$,$\int_a^b e^{-tx}\,dt=[-\frac{e^{-tx}}x]_a^b=\frac{e^{-ax}-e^{-bx}}x$(高亮)。
第二步:$a<b$ 情形:二重被积函数 $e^{-tx}$ 非负 → Tonelli 定理允许交换积分(关键点:非负性);内层逐项:$\int_0^\infty e^{-tx}\,dx=[-\frac{e^{-tx}}t]_0^\infty=\frac1t$。
第三步:外层逐项:$\int_a^b\frac1t\,dt=[\ln t]_a^b=\ln b-\ln a=\ln\frac ba<\infty$;故原积分绝对收敛,值为 $\ln\frac ba$(高亮)。
第四步:参数处理:$a>b$ 时交换 $a,b$ 并取负(仍为 $\ln\frac ba$);$a=b$ 时被积函数恒为零。
第五步:直接上界与不可拆分(关键点):近零处 $|(e^{-ax}-e^{-bx})/x|=|\int_a^be^{-tx}dt|\le|b-a|$;尾部由 $|e^{-u}-e^{-v}|\le|u-v|$ 得 $|e^{-ax}-e^{-bx}|\le|a-b|xe^{-\min(a,b)x}$,故尾积分 $\le|b-a|\cdot\frac{e^{-\min(a,b)R}}{\min(a,b)}$;单独 $\int_0^\infty e^{-ax}/x\,dx$ 在 $0$ 附近发散,不能拆成两个积分之差(高亮)。


## draft-c07-03

P: 求四叶玫瑰线 $r=\cos 2\theta$ 所围成的总面积，并说明为什么只需计算一叶再乘 $4$。

S: 一叶对应角域 $-\frac{\pi}{4}\le\theta\le\frac{\pi}{4}$(其间 $r\ge0$ 且极径从 $0$ 出发回到 $0$)。一叶面积 $A_1=\frac12\int_{-\frac{\pi}{4}}^{\frac{\pi}{4}}\cos^2 2\theta\,d\theta$。换元 $u=2\theta$:$\int_{-\frac{\pi}{4}}^{\frac{\pi}{4}}\cos^2 2\theta\,d\theta=\frac12\int_{-\frac{\pi}{2}}^{\frac{\pi}{2}}\cos^2u\,du=\frac12\cdot\frac{\pi}{2}=\frac{\pi}{4}$。故 $A_1=\frac12\cdot\frac{\pi}{4}=\frac{\pi}{8}$。四叶互不重叠且完全对称,总面积为 $4A_1=\frac{\pi}{2}$。

A: 总面积为 $\frac{\pi}{2}$(一叶 $\frac{\pi}{8}$ 乘 $4$)。

Objects: 极坐标图:四叶玫瑰线 $r=\cos2\theta$ 与一叶阴影 | 角域标注卡:一叶对应 $-\frac{\pi}4\le\theta\le\frac{\pi}4$ | 板书:$A_1=\frac12\int\cos^2(2\theta)d\theta$ 与换元 $u=2\theta$ | 原函数板:$\frac u2+\frac{\sin2u}4$ 与代入 $\frac\pi2$ | 结论卡:一叶 $\frac\pi8$,总面积 $4\times\frac\pi8=\frac\pi2$

Steps:
第一步:确定一叶角域(高亮):当 $-\frac\pi4\le\theta\le\frac\pi4$ 时 $2\theta\in[-\frac\pi2,\frac\pi2]$,$r=\cos2\theta\ge0$ 且极径从 $0$ 出发回到 $0$,描出一叶;四叶由四段对称生成 → 总面积 $=4A_1$。
第二步:极坐标面积公式:$A_1=\frac12\int_{-\frac\pi4}^{\frac\pi4}\cos^2(2\theta)\,d\theta$。
第三步:换元(逐项):$u=2\theta$,则 $du=2\,d\theta$,即 $d\theta=\frac12du$;上下限:$\theta=-\frac\pi4\to u=-\frac\pi2$,$\theta=\frac\pi4\to u=\frac\pi2$;故 $\int\cos^2(2\theta)d\theta=\frac12\int_{-\frac\pi2}^{\frac\pi2}\cos^2u\,du$。
第四步:计算(逐步):半角公式 $\cos^2u=\frac{1+\cos2u}2$;原函数 $\frac u2+\frac{\sin2u}4$;代入:$[\frac u2+\frac{\sin2u}4]_{-\frac\pi2}^{\frac\pi2}=\frac\pi4+\frac\pi4=\frac\pi2$;故 $A_1=\frac12\cdot\frac12\cdot\frac\pi2=\frac\pi8$。
第五步:总面积 $A=4A_1=4\times\frac\pi8=\frac\pi2$(逐步乘法,高亮结论)。


## draft-c07-04

P: 求圆 $r=4\cos\theta$ 内部位于圆 $r=2$ 外部的区域(月牙形)的面积。

S: 两圆交点:$4\cos\theta=2$ 得 $\cos\theta=\frac12$,即 $\theta=\pm\frac{\pi}{3}$。所求区域由 $-\frac{\pi}{3}\le\theta\le\frac{\pi}{3}$ 且 $2\le r\le4\cos\theta$ 描述。$A=\frac12\int_{-\frac{\pi}{3}}^{\frac{\pi}{3}}\left[(4\cos\theta)^2-2^2\right]d\theta=\frac12\int_{-\frac{\pi}{3}}^{\frac{\pi}{3}}(16\cos^2\theta-4)\,d\theta=\int_{-\frac{\pi}{3}}^{\frac{\pi}{3}}(8\cos^2\theta-2)\,d\theta=\int_{-\frac{\pi}{3}}^{\frac{\pi}{3}}(2+4\cos2\theta)\,d\theta=\left.2\theta+2\sin2\theta\right|_{-\frac{\pi}{3}}^{\frac{\pi}{3}}=\frac{4\pi}{3}+2\sqrt3$。

A: 面积为 $\frac{4\pi}{3}+2\sqrt3$。

Objects: 极坐标图:圆 $r=4\cos\theta$ 与圆 $r=2$,月牙区域阴影 | 交点卡:$\cos\theta=\frac12$,$\theta=\pm\frac\pi3$ | 板书:$A=\frac12\int[(4\cos\theta)^2-2^2]d\theta$ 与半角化简 | 原函数板:$\theta+\sin2\theta$ 与上下限代入 | 结论卡:$A=\frac{4\pi}3+2\sqrt3$

Steps:
第一步:求交点(高亮):$4\cos\theta=2$ 得 $\cos\theta=\frac12$,即 $\theta=\pm\frac\pi3$;所求区域由 $-\frac\pi3\le\theta\le\frac\pi3$ 且 $2\le r\le4\cos\theta$ 描述。
第二步:面积公式:$A=\frac12\int_{-\frac\pi3}^{\frac\pi3}[(4\cos\theta)^2-2^2]d\theta=\frac12\int_{-\frac\pi3}^{\frac\pi3}(16\cos^2\theta-4)d\theta$。
第三步:化简(逐项):提出 $4$:$=\frac12\cdot4\int(4\cos^2\theta-1)d\theta=2\int(4\cos^2\theta-1)d\theta$;半角公式 $\cos^2\theta=\frac{1+\cos2\theta}2$:$4\cos^2\theta-1=2(1+\cos2\theta)-1=1+2\cos2\theta$(高亮)。
第四步:求原函数:$\int(1+2\cos2\theta)d\theta=\theta+\sin2\theta$;代入上下限:$[\theta+\sin2\theta]_{-\frac\pi3}^{\frac\pi3}=(\frac\pi3+\frac{\sqrt3}2)-(-\frac\pi3-\frac{\sqrt3}2)=\frac{2\pi}3+\sqrt3$。
第五步:乘系数:$A=2(\frac{2\pi}3+\sqrt3)=\frac{4\pi}3+2\sqrt3$(高亮结论)。


## draft-c10-04

P: 对$S=\sum_{n\ge1}(-1)^{n-1}/3^n$，求精确余项$R_N=S-S_N$；求使实际误差严格小于$1/2500$的最小$N$，再求只使用莱布尼茨界即可保证该条件的最小$N$。

S: 几何级数给$S=1/4$、$S_N=(1-(-1/3)^N)/4$，故$R_N=(-1)^N/(4\cdot3^N)$。实际误差条件等价于$3^N>625$；$3^5=243<625<729=3^6$，最小$N=6$。莱布尼茨界为$|R_N|\le3^{-(N+1)}$，仅依此保证严格小于$1/2500$需$3^{N+1}>2500$；$3^7=2187<2500<6561=3^8$，最小$N=7$。$S_6=182/729$、$R_6=1/2916$，均为精确分数。界给出的充分条件不能冒充实际最小项数。

A: $R_N=(-1)^N/(4\cdot3^N)$；实际最小$N=6$，仅用莱布尼茨界的最小$N=7$。

Objects: 题面卡:$S=\sum_{n\ge1}(-1)^{n-1}/3^n$ 的精确余项与最小 $N$ | 板书一:$S=\frac14$、$S_N=\frac{1-(-1/3)^N}4$、$R_N=\frac{(-1)^N}{4\cdot3^N}$ | 高亮框:关键点 1——比较链 $3^5=243<625<729=3^6$;关键点 2——比较链 $3^7=2187<2500<6561=3^8$ | 分数验证板:$S_6=\frac{182}{729}$、$R_6=\frac1{2916}$ | 结论卡:实际最小 $N=6$;仅用莱布尼茨界的最小 $N=7$

Steps:
第一步:求 $S$ 与 $S_N$(逐项):$S$ 是首项 $\frac13$、公比 $-\frac13$ 的几何级数:$S=\frac{1/3}{1-(-1/3)}=\frac{1/3}{4/3}=\frac14$;$S_N=\frac{(1/3)(1-(-1/3)^N)}{1-(-1/3)}=\frac{1-(-1/3)^N}4$。
第二步:精确余项:$R_N=S-S_N=\frac14-\frac{1-(-1/3)^N}4=\frac{(-1/3)^N}4=\frac{(-1)^N}{4\cdot3^N}$。
第三步:实际误差条件:$|R_N|=\frac1{4\cdot3^N}<\frac1{2500}$ 等价于 $3^N>625$;关键比较链(高亮):$3^5=243<625<729=3^6$,故实际最小 $N=6$。
第四步:莱布尼茨界:$|R_N|\le|u_{N+1}|=3^{-(N+1)}$;仅用此界保证 $<\frac1{2500}$ 需 $3^{N+1}>2500$;关键比较链(高亮):$3^7=2187<2500<6561=3^8$,故最小 $N=7$。
第五步:精确分数验证(逐项):$S_6=\frac{1-(-1/3)^6}4=\frac{1-\frac1{729}}4=\frac{728}{4\cdot729}=\frac{182}{729}$;$R_6=\frac1{4\cdot3^6}=\frac1{2916}$;结论:界给的充分条件不能冒充实际最小项数(高亮)。


## draft-c10-05

P: 证明莱布尼茨判别法:若 $a_n$ 单调递减趋于 $0$,则交错级数 $\sum_{n=1}^{\infty}(-1)^{n+1}a_n$ 收敛,且其和 $S$ 满足 $|S-S_N|\le a_{N+1}$。

S: 设$a_n\ge0$、$a_{n+1}\le a_n$且$a_n\to0$，$S_N=\sum_{n=1}^N(-1)^{n-1}a_n$。偶部分和递增，奇部分和递减，且$S_{2m}\le S_{2l+1}$对一切$m,l$成立；两序列有界并有极限，差$S_{2N+1}-S_{2N}=a_{2N+1}\to0$，故极限相同，记为$S$。由夹逼，对任意$N$有$0\le(-1)^N(S-S_N)\le a_{N+1}$，所以$|S-S_N|\le a_{N+1}$。该证明只涉及有限部分和及其极限。

A: 证明见解法(偶子列单调有界、奇子列同极限;余项 $|S-S_N|\le a_{N+1}$)。

Objects: 题面卡:莱布尼茨判别法($a_n$ 递减趋于 $0$) | 板书一:$S_{2m+2}-S_{2m}=a_{2m+1}-a_{2m+2}\ge0$ 与 $S_{2m+3}-S_{2m+1}=-a_{2m+2}+a_{2m+3}\le0$ | 高亮框:关键点 1——偶部分和递增、奇部分和递减且 $S_{2m}\le S_{2l+1}$;关键点 2——$S_{2N+1}-S_{2N}=a_{2N+1}\to0$ | 夹逼板:$0\le(-1)^N(S-S_N)\le a_{N+1}$ | 结论卡:级数收敛且 $|S-S_N|\le a_{N+1}$

Steps:
第一步:写出条件:$a_n\ge0$ 且 $a_{n+1}\le a_n$、$a_n\to0$;部分和 $S_N=\sum_{n=1}^N(-1)^{n-1}a_n$。
第二步:单调性(逐项,高亮):$S_{2m+2}-S_{2m}=a_{2m+1}-a_{2m+2}\ge0$,偶部分和递增;$S_{2m+3}-S_{2m+1}=-a_{2m+2}+a_{2m+3}\le0$,奇部分和递减。
第三步:交叉序(关键点):$S_{2m}\le S_{2m+1}\le S_{2l+1}$ 对一切 $m,l$ 成立(偶部分和总不超奇部分和);两序列单调有界 → 各有极限;差 $S_{2N+1}-S_{2N}=a_{2N+1}\to0$(逐项),故两极限相同,记为 $S$。
第四步:夹逼(关键点):由 $S_{2N}\le S\le S_{2N+1}$ 得 $0\le S-S_{2N}\le a_{2N+1}$;由 $S_{2N+2}\le S\le S_{2N+1}$ 得 $0\le S_{2N+1}-S\le a_{2N+2}$;统一写成 $0\le(-1)^N(S-S_N)\le a_{N+1}$。
第五步:结论:$|S-S_N|\le a_{N+1}$,交错级数收敛且余项受下一项控制;该证明只涉及有限部分和及其极限(高亮)。


## draft-c14-02

P: 求$f(x)=x(\pi-x)$在$[0,\pi]$的半区间正弦展开，并说明周期奇延拓的端点值和收敛方式。

S: $b_n=(2/\pi)\int_0^\pi x(\pi-x)\sin(nx)dx$。两次分部积分，端点$f(0)=f(\pi)=0$且$f^{\prime\prime}=-2$，得积分$2[1-(-1)^n]/n^3$，所以$b_n=4[1-(-1)^n]/(\pi n^3)$。故$f(x)=(8/\pi)\sum_{k\ge0}\sin((2k+1)x)/(2k+1)^3$。奇延拓在$0,\pm\pi$左右极限都为零，连续、分段光滑；Dirichlet定理在每点取实际值。系数绝对可和，故周期展开全实轴一致绝对收敛。

A: $x(\pi-x)=\frac8\pi\sum_{k\ge0}\frac{\sin((2k+1)x)}{(2k+1)^3}$；端点为零，一致绝对收敛。

Objects: 函数卡:$f(x)=x(\pi-x)$ 在 $[0,\pi]$ 与周期奇延拓示意 | 板书一:两次分部积分的逐次计算与边界项代入 | 高亮框:关键点 1——边界项 $f(0)=f(\pi)=0$;关键点 2——$|b_n|\le\frac8{\pi n^3}$ 与 $p$-级数比较 | 展开板:$\frac8\pi\sum_{k\ge0}\frac{\sin((2k+1)x)}{(2k+1)^3}$ | 结论卡:端点为零,全实轴一致绝对收敛

Steps:
第一步:正弦展开公式:$b_n=\frac2\pi\int_0^\pi x(\pi-x)\sin(nx)\,dx$;边界项:奇延拓下 $f(0)=f(\pi)=0$(高亮)。
第二步:两次分部积分(逐次):第一次($u=x(\pi-x)$,$dv=\sin(nx)dx$):边界项 $[-\frac{x(\pi-x)\cos(nx)}n]_0^\pi=0$,剩 $\frac1n\int_0^\pi(\pi-2x)\cos(nx)dx$;第二次($u=\pi-2x$,$dv=\frac{\cos(nx)}n dx$):边界项 $[\frac{(\pi-2x)\sin(nx)}{n^2}]_0^\pi=0$,剩 $\frac2{n^2}\int_0^\pi\sin(nx)dx=\frac2{n^2}\cdot\frac{1-(-1)^n}n=\frac{2[1-(-1)^n]}{n^3}$。
第三步:代入系数:$b_n=\frac2\pi\cdot\frac{2[1-(-1)^n]}{n^3}=\frac{4[1-(-1)^n]}{\pi n^3}$;$n$ 偶时 $b_n=0$;$n=2k+1$ 时 $b_{2k+1}=\frac8{\pi(2k+1)^3}$。
第四步:写出展开:$f(x)=\sum_{n\ge1}b_n\sin(nx)=\frac8\pi\sum_{k\ge0}\frac{\sin((2k+1)x)}{(2k+1)^3}$。
第五步:收敛方式(关键点):奇延拓在 $0,\pm\pi$ 处左右极限都为零,连续且分段光滑 → Dirichlet 定理每点取实际值;系数绝对可和:$|b_n|\le\frac8{\pi n^3}$ 且 $\sum\frac1{n^3}$ 收敛(高亮比较),故周期展开全实轴一致绝对收敛。


## draft-c25-04

P: 求柱面$x^2+y^2=4$与$z=x^2$的完整交线参数式，并证明交线不包含于任何平面。

S: 圆柱约束给$x=2\cos t,y=2\sin t$，另一个约束给$z=4\cos^2t$，故完整交线为$(2\cos t,2\sin t,4\cos^2t)$，$0\le t<2\pi$。若整条交线在$Ax+By+Cz=D$中，则$2A\cos t+2B\sin t+2C\cos2t+(2C-D)=0$对所有$t$成立。对$1,\cos t,\sin t,\cos2t$分别积分正交消去，得$A=B=C=D=0$，这不是平面方程，矛盾。因此是非平面闭交线。

A: 参数$(2\cos t,2\sin t,4\cos^2t)$，$0\le t<2\pi$；交线非平面。

Objects: 空间图:柱面 $x^2+y^2=4$ 与抛物柱面 $z=x^2$ 的交线 | 参数化板书:$x=2\cos t,y=2\sin t,z=4\cos^2t$ | 平面代入板:$2A\cos t+2B\sin t+2C\cos2t+(2C-D)=0$ 与半角变换 | 高亮框:关键点——正交消去:$\int\cos^2t=\pi$ 等四项积分逐项为零 | 结论卡:$A=B=C=D=0$ 矛盾,交线非平面

Steps:
第一步:参数化(逐项):圆柱 $x^2+y^2=4$ 给 $x=2\cos t,y=2\sin t$;代入 $z=x^2$ 得 $z=4\cos^2t$;故完整交线为 $(2\cos t,2\sin t,4\cos^2t)$,$0\le t<2\pi$。
第二步:反设(关键点):若整条交线在平面 $Ax+By+Cz=D$ 中,代入得 $2A\cos t+2B\sin t+4C\cos^2t=D$ 对一切 $t$;半角变换 $4\cos^2t=2(1+\cos2t)$:$2A\cos t+2B\sin t+2C\cos2t+(2C-D)=0$(高亮)。
第三步:正交消去(逐项):两边乘 $\cos t$ 并在 $[0,2\pi)$ 积分:$\int_0^{2\pi}\cos^2t\,dt=\pi$,$\int\sin t\cos t\,dt=0$,$\int\cos2t\cos t\,dt=0$,$\int\cos t\,dt=0$;得 $2A\pi=0$,即 $A=0$。
第四步:同理逐项:乘 $1$ 积分得 $2\pi(2C-D)=0$;乘 $\sin t$ 得 $2B\pi=0$,即 $B=0$;乘 $\cos2t$ 得 $2C\pi=0$,即 $C=0$;再代回得 $D=0$。
第五步:结论:$A=B=C=D=0$ 不是平面方程(平面要求系数不全为零),矛盾;故交线不包含于任何平面,是非平面闭交线(高亮)。


## draft-c25-05

P: 求球$x^2+y^2+z^2=1$与抛物柱面$y=x^2$的实交线，给参数域、分支连接关系，证明交线正则且非平面。

S: 置$x=t$，则$y=t^2$、$z=\pm\sqrt{1-t^2-t^4}$。根号非负等价于$|t|\le r=\sqrt{(\sqrt5-1)/2}$。两图形弧在$t=\pm r$的点$(\pm r,r^2,0)$连接，合为一条闭曲线，不能把正负图形弧误称为两个连通分量。正则性由梯度$(2t,2t^2,2z)$与$(-2t,1,0)$线性无关证明：$z\ne0$时明显；$z=0$时$t\ne0$，若成比例，第一坐标给比例$-1$而第二要求$2t^2=-1$，不可能。根号图形在端点不能充当光滑参数，可在端点改用$z$及$x=\pm\sqrt{(-1+\sqrt{5-4z^2})/2}$作为局部参数。若整条曲线在$Ax+By+Cz=D$中，比较同$t$的正负$z$得$C=0$；继而$At+Bt^2-D$在区间恒零，得$A=B=D=0$，矛盾。

A: 两弧$(t,t^2,\pm\sqrt{1-t^2-t^4})$，$|t|\le\sqrt{(\sqrt5-1)/2}$；连接为一条正则非平面闭曲线。

Objects: 空间图:球面与抛物柱面的实交线(两弧连接) | 不等式板书:令 $s=t^2$,$s^2+s-1\le0\Rightarrow s\le\frac{\sqrt5-1}2$ | 高亮框:关键点 1——端点 $z=0$ 处两弧连接为一条闭曲线;关键点 2——梯度成比例导出的矛盾 | 端点参数板:消元解 $s=\frac{-1+\sqrt{5-4z^2}}2$ | 结论卡:正则非平面闭曲线

Steps:
第一步:参数化:$x=t$,$y=t^2$,$z=\pm\sqrt{1-t^2-t^4}$;解不等式(逐步):$1-t^2-t^4\ge0$;令 $s=t^2\ge0$,得 $s^2+s-1\le0$;方程 $s^2+s-1=0$ 的根为 $\frac{-1\pm\sqrt5}2$,取正根 $s\le\frac{\sqrt5-1}2$;故 $|t|\le r=\sqrt{\frac{\sqrt5-1}2}$(高亮)。
第二步:分支连接(关键点):两弧在 $t=\pm r$ 处汇于 $(\pm r,r^2,0)$(此时 $z=0$);正负两弧合为一条闭曲线,不能误称两个连通分量。
第三步:正则性:$z\ne0$ 时,球面梯度 $(2t,2t^2,2z)$ 与柱面梯度 $(-2t,1,0)$ 显然线性无关(第三分量结构不同)。
第四步:$z=0$ 情形(关键点):此时 $t\ne0$;若两梯度成比例,设 $(2t,2t^2,0)=\lambda(-2t,1,0)$:第一坐标给 $\lambda=-1$,第二坐标要求 $2t^2=\lambda=-1$,但 $2t^2\ge0$,矛盾;故线性无关。
第五步:端点光滑参数(关键点):根号图形在端点不可作光滑参数;改以 $z$ 为参数:消元 $y=x^2$ 代入球面得 $x^2+x^4+z^2=1$;令 $s=x^2$,解 $s^2+s+(z^2-1)=0$ 得 $s=\frac{-1+\sqrt{5-4z^2}}2$(取正根),即 $x=\pm\sqrt{\frac{-1+\sqrt{5-4z^2}}2}$;故交线为正则非平面闭曲线(高亮)。


## draft-c41-01

P: 在基$e_{11},e_{12},e_{21},e_{22}$中，令$N=J_2(0)\otimes I_2+I_2\otimes J_2(0)$。从张量结构求Jordan形式，并给出实际Jordan链及换基矩阵。

S: $Ne_{11}=0,Ne_{12}=Ne_{21}=e_{11},Ne_{22}=e_{12}+e_{21}$。所以$N^2e_{22}=2e_{11}$，$N^3=0$；秩序列$4,2,1,0$。取链$v_3=e_{22},v_2=e_{12}+e_{21},v_1=2e_{11}$及$w=e_{12}-e_{21}$，有$Nv_3=v_2,Nv_2=v_1,Nv_1=Nw=0$。$P=(v_1,v_2,v_3,w)=\begin{pmatrix}2&0&0&0\\0&1&0&1\\0&1&0&-1\\0&0&1&0\end{pmatrix}$可逆，$NP=P[J_3(0)\oplus J_1(0)]$。因此Jordan形式为$J_3(0)\oplus J_1(0)$。

A: $J_3(0)\oplus J_1(0)$；链和$P$如上。

Objects: 张量作用卡:$(J_2(0)\otimes I_2)e_{ij}$ 与 $(I_2\otimes J_2(0))e_{ij}$ 的规则 | 基向量作用板:$Ne_{11}=0,Ne_{12}=Ne_{21}=e_{11},Ne_{22}=e_{12}+e_{21}$ | 迭代板:$N^2e_{22}=2e_{11}$、$N^3=0$,秩链 $4,2,1,0$ | 链验证卡:$Nv_3=v_2,Nv_2=v_1,Nv_1=Nw=0$ | 结论卡:$P$ 如上,$J_3(0)\oplus J_1(0)$

Steps:
第一步:张量作用规则(高亮):$J_2(0)$ 把 $e_2$ 送到 $e_1$、$e_1$ 送到 $0$;故 $(J_2(0)\otimes I_2)e_{ij}=e_{i-1,j}$($i=2$ 时,$i=1$ 时为零),$(I_2\otimes J_2(0))e_{ij}=e_{i,j-1}$;逐项:$Ne_{11}=0$;$Ne_{12}=e_{11}$;$Ne_{21}=e_{11}$;$Ne_{22}=e_{12}+e_{21}$。
第二步:逐次作用(逐项):$N^2e_{22}=N(e_{12}+e_{21})=e_{11}+e_{11}=2e_{11}\ne0$;$N^3e_{22}=N(2e_{11})=0$;其余基向量至多两次归零;故秩链为 $4,2,1,0$($\operatorname{Im}N=\operatorname{span}(e_{11},e_{12}+e_{21})$ 维数 $2$,$\operatorname{Im}N^2=\operatorname{span}(e_{11})$ 维数 $1$,高亮)。
第三步:构造链并逐项验证(高亮):$v_3=e_{22}$,$v_2=e_{12}+e_{21}$,$v_1=2e_{11}$,$w=e_{12}-e_{21}$;$Nv_3=v_2$;$Nv_2=e_{11}+e_{11}=2e_{11}=v_1$;$Nv_1=0$;$Nw=e_{11}-e_{11}=0$。
第四步:写出换基矩阵:按列 $(v_1,v_2,v_3,w)$:列1$=2e_{11}=(2,0,0,0)$;列2$=e_{12}+e_{21}=(0,1,1,0)$;列3$=e_{22}=(0,0,0,1)$;列4$=w=(0,1,-1,0)$;$P=\begin{pmatrix}2&0&0&0\\0&1&0&1\\0&1&0&-1\\0&0&1&0\end{pmatrix}$。
第五步:结论:长度 $3$ 的链给一个 $3$ 阶块,陪一个 $1$ 阶块,故 Jordan 形式为 $J_3(0)\oplus J_1(0)$(高亮)。


## draft-c41-04

P: 对$A=\begin{pmatrix}4&2&1\\0&4&3\\0&0&4\end{pmatrix}$，构造实际广义特征向量链和$P$，验证$P^{-1}AP$，而非直接读出现成Jordan块。

S: 令$N=A-4I$，取$v_3=e_3$，$v_2=Nv_3=(1,3,0)^{\mathsf T}$，$v_1=Nv_2=(6,0,0)^{\mathsf T}$，则$Nv_1=0$。$P=(v_1,v_2,v_3)=\begin{pmatrix}6&1&0\\0&3&0\\0&0&1\end{pmatrix}$，行列式$18\ne0$。链给$AP=P\begin{pmatrix}4&1&0\\0&4&1\\0&0&4\end{pmatrix}$，所以Jordan形式为$J_3(4)$，最小多项式$(\lambda-4)^3$；$N^2\ne0,N^3=0$确保不能误分成较短链。

A: $P=\begin{pmatrix}6&1&0\\0&3&0\\0&0&1\end{pmatrix}$，$P^{-1}AP=J_3(4)$。

Objects: 矩阵卡:$A=\begin{pmatrix}4&2&1\\0&4&3\\0&0&4\end{pmatrix}$ 与 $N=A-4I$ | 行×列计算卡:$v_2=Nv_3$ 与 $v_1=Nv_2$ 的分量乘积 | 行列式卡:$\det P=6\cdot3\cdot1=18$(对角元乘积) | 链验证板:$AP$ 各列与 $J_3(4)$ 的列对应 | 结论卡:$J_3(4)$,最小多项式 $(\lambda-4)^3$

Steps:
第一步:令 $N=A-4I=\begin{pmatrix}0&2&1\\0&0&3\\0&0&0\end{pmatrix}$;取 $v_3=e_3$;计算 $v_2=Nv_3$(逐行×列,高亮):第1行×列:$0\cdot0+2\cdot0+1\cdot1=1$;第2行×列:$0\cdot0+0\cdot0+3\cdot1=3$;第3行×列:$0$;得 $v_2=(1,3,0)^{\mathsf T}$。
第二步:计算 $v_1=Nv_2$(逐行×列,高亮):第1行×列:$0\cdot1+2\cdot3+1\cdot0=6$;第2行×列:$0$;第3行×列:$0$;得 $v_1=(6,0,0)^{\mathsf T}$;且 $Nv_1=0$(第一列全零,逐项验证)。
第三步:构造 $P=(v_1,v_2,v_3)=\begin{pmatrix}6&1&0\\0&3&0\\0&0&1\end{pmatrix}$;$P$ 为上三角,行列式 $=6\cdot3\cdot1=18\ne0$(对角元乘积,高亮),故可逆。
第四步:链关系验证(逐列,高亮):$AP$ 的第1列 $=Av_1=Nv_1+4v_1=4v_1$;第2列 $=Av_2=Nv_2+4v_2=v_1+4v_2$;第3列 $=Av_3=Nv_3+4v_3=v_2+4v_3$;故 $AP=P\begin{pmatrix}4&1&0\\0&4&1\\0&0&4\end{pmatrix}$,即 $P^{-1}AP=J_3(4)$。
第五步:结论:Jordan 形式 $J_3(4)$;最小多项式 $(\lambda-4)^3$;验证 $N^2\ne0$(如 $N^2v_3=v_1\ne0$)且 $N^3=0$;全部由链构造得出,不是直接读现成块(高亮)。
