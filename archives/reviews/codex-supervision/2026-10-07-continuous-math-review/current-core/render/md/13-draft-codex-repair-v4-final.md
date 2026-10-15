## draft-c10-01

problem

定义$u_{2k-1}=1/k$、$u_{2k}=-1/k+2^{-k}$（$k\ge1$）。求$\sum_{n\ge1}u_n$的和与敛散类型，并判断绝对值单调递减是否为交错级数收敛的必要条件。

solution

由$2^k>k$知偶项为负，奇项为正。精确部分和为$S_{2N}=1-2^{-N}$、$S_{2N+1}=1-2^{-N}+1/(N+1)$，均趋于$1$。而$\sum_{n=1}^{2N}|u_n|=2\sum_{k=1}^N1/k-1+2^{-N}\to\infty$，所以条件收敛。$|u_4|=1/4<|u_5|=1/3$，绝对值不单调；莱布尼茨的单调条件是充分条件，并非必要条件。

answer

条件收敛，和$1$；绝对值不单调，单调性不是必要条件。

scene_spec.objects[0]

定义$u_{2k-1}=1/k$、$u_{2k}=-1/k+2^{-k}$（$k\ge1$）。求$\sum_{n\ge1}u_n$的和与敛散类型，并判断绝对值单调递减是否为交错级数收敛的必要条件。

scene_spec.objects[1]

条件收敛，和$1$；绝对值不单调，单调性不是必要条件。

scene_spec.steps[0]

第一步:由$2^k>k$知偶项为负，奇项为正。

scene_spec.steps[1]

第二步:精确部分和为$S_{2N}=1-2^{-N}$、$S_{2N+1}=1-2^{-N}+1/(N+1)$，均趋于$1$。

scene_spec.steps[2]

第三步:而$\sum_{n=1}^{2N}|u_n|=2\sum_{k=1}^N1/k-1+2^{-N}\to\infty$，所以条件收敛。

scene_spec.steps[3]

第四步:$|u_4|=1/4<|u_5|=1/3$，绝对值不单调；莱布尼茨的单调条件是充分条件，并非必要条件。

## draft-c10-02

problem

设$b_n=1/\sqrt{n(n+1)}$，$a_n=b_n+(-1)^n/[n(n+1)]$。证明$a_n>0$、$a_n$不单调，且$\sum_{n\ge1}(-1)^na_n$条件收敛。说明绝对可和扰动为何不破坏交错级数的收敛。

solution

$b_n>1/[n(n+1)]$，故$a_n>0$。$b_n$递减趋零，$\sum(-1)^nb_n$由莱布尼茨判别法收敛。扰动项满足$\sum1/[n(n+1)]\le\sum1/n^2<\infty$，故$\sum(-1)^na_n=\sum(-1)^nb_n+\sum1/[n(n+1)]$收敛。对绝对值，$a_n\ge1/(n+1)-1/[n(n+1)]$；前一正项级数发散、后一收敛，因此绝对值级数发散。又$a_4-a_3=\sqrt5/10-\sqrt3/6+2/15>2/10-2/6+2/15=0$，故不单调。一般地，若$\sum(-1)^nb_n$收敛、$\sum|c_n|<\infty$，则$\sum(-1)^n(b_n+c_n)$是两个收敛级数之和。这里的收敛由判别法和绝对可和扰动证明，不用数值试算。

answer

正振幅不单调，但交错级数条件收敛；绝对可和扰动保持收敛。

scene_spec.objects[0]

设$b_n=1/\sqrt{n(n+1)}$，$a_n=b_n+(-1)^n/[n(n+1)]$。证明$a_n>0$、$a_n$不单调，且$\sum_{n\ge1}(-1)^na_n$条件收敛。说明绝对可和扰动为何不破坏交错级数的收敛。

scene_spec.objects[1]

正振幅不单调，但交错级数条件收敛；绝对可和扰动保持收敛。

scene_spec.steps[0]

第一步:$b_n>1/[n(n+1)]$，故$a_n>0$。

scene_spec.steps[1]

第二步:$b_n$递减趋零，$\sum(-1)^nb_n$由莱布尼茨判别法收敛。

scene_spec.steps[2]

第三步:扰动项满足$\sum1/[n(n+1)]\le\sum1/n^2<\infty$，故$\sum(-1)^na_n=\sum(-1)^nb_n+\sum1/[n(n+1)]$收敛。

scene_spec.steps[3]

第四步:对绝对值，$a_n\ge1/(n+1)-1/[n(n+1)]$；前一正项级数发散、后一收敛，因此绝对值级数发散。

scene_spec.steps[4]

第五步:又$a_4-a_3=\sqrt5/10-\sqrt3/6+2/15>2/10-2/6+2/15=0$，故不单调。

scene_spec.steps[5]

第六步:一般地，若$\sum(-1)^nb_n$收敛、$\sum|c_n|<\infty$，则$\sum(-1)^n(b_n+c_n)$是两个收敛级数之和。

scene_spec.steps[6]

第七步:这里的收敛由判别法和绝对可和扰动证明，不用数值试算。

## draft-c10-03

problem

说明级数 $\sum_{n=1}^{\infty}\frac{(-1)^n(2+(-1)^n)}{n}$ 发散，并解释莱布尼茨判别法为何不能使用。

solution

第$2k-1$项为$-1/(2k-1)$，第$2k$项为$3/(2k)$，成对和为$(4k-3)/[2k(2k-1)]\ge1/(2k)$。所以$S_{2N}\ge\frac12\sum_{k=1}^N1/k\to+\infty$；$S_{2N+1}=S_{2N}-1/(2N+1)\to+\infty$。振幅也不递减：$1/(2k-1)<3/(2k)$。因此不能用莱布尼茨判别法，级数发散到$+\infty$。

answer

级数发散(拆成 $2\sum(-1)^n/n+\sum1/n$,收敛+发散);莱布尼茨判别法因通项绝对值不单调而不可用。

scene_spec.objects[0]

说明级数 $\sum_{n=1}^{\infty}\frac{(-1)^n(2+(-1)^n)}{n}$ 发散，并解释莱布尼茨判别法为何不能使用。

scene_spec.objects[1]

级数发散(拆成 $2\sum(-1)^n/n+\sum1/n$,收敛+发散);莱布尼茨判别法因通项绝对值不单调而不可用。

scene_spec.steps[0]

第一步:第$2k-1$项为$-1/(2k-1)$，第$2k$项为$3/(2k)$，成对和为$(4k-3)/[2k(2k-1)]\ge1/(2k)$。

scene_spec.steps[1]

第二步:所以$S_{2N}\ge\frac12\sum_{k=1}^N1/k\to+\infty$；$S_{2N+1}=S_{2N}-1/(2N+1)\to+\infty$。

scene_spec.steps[2]

第三步:振幅也不递减：$1/(2k-1)<3/(2k)$。

scene_spec.steps[3]

第四步:因此不能用莱布尼茨判别法，级数发散到$+\infty$。

## draft-c10-04

problem

对$S=\sum_{n\ge1}(-1)^{n-1}/3^n$，求精确余项$R_N=S-S_N$；求使实际误差严格小于$1/2500$的最小$N$，再求只使用莱布尼茨界即可保证该条件的最小$N$。

solution

几何级数给$S=1/4$、$S_N=(1-(-1/3)^N)/4$，故$R_N=(-1)^N/(4\cdot3^N)$。实际误差条件等价于$3^N>625$；$3^5=243<625<729=3^6$，最小$N=6$。莱布尼茨界为$|R_N|\le3^{-(N+1)}$，仅依此保证严格小于$1/2500$需$3^{N+1}>2500$；$3^7=2187<2500<6561=3^8$，最小$N=7$。$S_6=182/729$、$R_6=1/2916$，均为精确分数。界给出的充分条件不能冒充实际最小项数。

answer

$R_N=(-1)^N/(4\cdot3^N)$；实际最小$N=6$，仅用莱布尼茨界的最小$N=7$。

scene_spec.objects[0]

对$S=\sum_{n\ge1}(-1)^{n-1}/3^n$，求精确余项$R_N=S-S_N$；求使实际误差严格小于$1/2500$的最小$N$，再求只使用莱布尼茨界即可保证该条件的最小$N$。

scene_spec.objects[1]

$R_N=(-1)^N/(4\cdot3^N)$；实际最小$N=6$，仅用莱布尼茨界的最小$N=7$。

scene_spec.steps[0]

第一步:几何级数给$S=1/4$、$S_N=(1-(-1/3)^N)/4$，故$R_N=(-1)^N/(4\cdot3^N)$。

scene_spec.steps[1]

第二步:实际误差条件等价于$3^N>625$；$3^5=243<625<729=3^6$，最小$N=6$。

scene_spec.steps[2]

第三步:莱布尼茨界为$|R_N|\le3^{-(N+1)}$，仅依此保证严格小于$1/2500$需$3^{N+1}>2500$；$3^7=2187<2500<6561=3^8$，最小$N=7$。

scene_spec.steps[3]

第四步:$S_6=182/729$、$R_6=1/2916$，均为精确分数。

scene_spec.steps[4]

第五步:界给出的充分条件不能冒充实际最小项数。

## draft-c10-05

problem

证明莱布尼茨判别法:若 $a_n$ 单调递减趋于 $0$,则交错级数 $\sum_{n=1}^{\infty}(-1)^{n+1}a_n$ 收敛,且其和 $S$ 满足 $|S-S_N|\le a_{N+1}$。

solution

设$a_n\ge0$、$a_{n+1}\le a_n$且$a_n\to0$，$S_N=\sum_{n=1}^N(-1)^{n-1}a_n$。偶部分和递增，奇部分和递减，且$S_{2m}\le S_{2l+1}$对一切$m,l$成立；两序列有界并有极限，差$S_{2N+1}-S_{2N}=a_{2N+1}\to0$，故极限相同，记为$S$。由夹逼，对任意$N$有$0\le(-1)^N(S-S_N)\le a_{N+1}$，所以$|S-S_N|\le a_{N+1}$。该证明只涉及有限部分和及其极限。

answer

证明见解法(偶子列单调有界、奇子列同极限;余项 $|S-S_N|\le a_{N+1}$)。

scene_spec.objects[0]

证明莱布尼茨判别法:若 $a_n$ 单调递减趋于 $0$,则交错级数 $\sum_{n=1}^{\infty}(-1)^{n+1}a_n$ 收敛,且其和 $S$ 满足 $|S-S_N|\le a_{N+1}$。

scene_spec.objects[1]

证明见解法(偶子列单调有界、奇子列同极限;余项 $|S-S_N|\le a_{N+1}$)。

scene_spec.steps[0]

第一步:设$a_n\ge0$、$a_{n+1}\le a_n$且$a_n\to0$，$S_N=\sum_{n=1}^N(-1)^{n-1}a_n$。

scene_spec.steps[1]

第二步:偶部分和递增，奇部分和递减，且$S_{2m}\le S_{2l+1}$对一切$m,l$成立；两序列有界并有极限，差$S_{2N+1}-S_{2N}=a_{2N+1}\to0$，故极限相同，记为$S$。

scene_spec.steps[2]

第三步:由夹逼，对任意$N$有$0\le(-1)^N(S-S_N)\le a_{N+1}$，所以$|S-S_N|\le a_{N+1}$。

scene_spec.steps[3]

第四步:该证明只涉及有限部分和及其极限。

## draft-c12-01

problem

证明函数项级数 $\sum_{n=1}^{\infty}\frac{\sin nx}{n^2}$ 在 $\mathbb R$ 上一致收敛。

solution

用魏尔斯特拉斯 $M$ 判别法:对一切 $x\in\mathbb R$,$\left|\frac{\sin nx}{n^2}\right|\le\frac{1}{n^2}=M_n$,而 $\sum_{n=1}^{\infty}M_n=\sum\frac{1}{n^2}$ 收敛。故级数在 $\mathbb R$ 上一致收敛(且绝对一致收敛)。

answer

在 $\mathbb R$ 上一致收敛($M$ 判别法,$M_n=\frac{1}{n^2}$)。

scene_spec.objects[0]

证明函数项级数 $\sum_{n=1}^{\infty}\frac{\sin nx}{n^2}$ 在 $\mathbb R$ 上一致收敛。

scene_spec.objects[1]

在 $\mathbb R$ 上一致收敛($M$ 判别法,$M_n=\frac{1}{n^2}$)。

scene_spec.steps[0]

第一步:用魏尔斯特拉斯 $M$ 判别法:对一切 $x\in\mathbb R$,$\left|\frac{\sin nx}{n^2}\right|\le\frac{1}{n^2}=M_n$,而 $\sum_{n=1}^{\infty}M_n=\sum\frac{1}{n^2}$ 收敛。

scene_spec.steps[1]

第二步:故级数在 $\mathbb R$ 上一致收敛(且绝对一致收敛)。

## draft-c12-02

problem

证明 $\sum_{n=0}^{\infty}x^n$ 在 $[-\frac12,\frac12]$ 上一致收敛，并说明在 $(-1,1)$ 上不一致收敛。

solution

在$[-1/2,1/2]$上，$|x^n|\le2^{-n}$，由M判别法一致收敛。在$(-1,1)$上点态和为$1/(1-x)$；从$n=0$到$N$的部分和尾项为$x^{N+1}/(1-x)$。对每个固定$N$，令$x\to1^{-}$，尾项趋于$+\infty$，其上确界为$+\infty$，故不一致收敛。

answer

在 $[-\frac12,\frac12]$ 上一致收敛($M$ 判别法);在 $(-1,1)$ 上不一致收敛($\sup|S_N-S|$ 不趋于 $0$)。

scene_spec.objects[0]

证明 $\sum_{n=0}^{\infty}x^n$ 在 $[-\frac12,\frac12]$ 上一致收敛，并说明在 $(-1,1)$ 上不一致收敛。

scene_spec.objects[1]

在 $[-\frac12,\frac12]$ 上一致收敛($M$ 判别法);在 $(-1,1)$ 上不一致收敛($\sup|S_N-S|$ 不趋于 $0$)。

scene_spec.steps[0]

第一步:在$[-1/2,1/2]$上，$|x^n|\le2^{-n}$，由M判别法一致收敛。

scene_spec.steps[1]

第二步:在$(-1,1)$上点态和为$1/(1-x)$；从$n=0$到$N$的部分和尾项为$x^{N+1}/(1-x)$。

scene_spec.steps[2]

第三步:对每个固定$N$，令$x\to1^{-}$，尾项趋于$+\infty$，其上确界为$+\infty$，故不一致收敛。

## draft-c12-03

problem

证明$\sum_{n\ge1}\sin(nx)/n$在$[\delta,2\pi-\delta]$（$0<\delta<\pi$）上一致收敛，而在$(0,2\pi)$上不一致收敛。不得用其和函数的图像代替证明。

solution

几何求和给任意正弦块$|\sum_{n=p}^q\sin(nx)|\le1/|\sin(x/2)|\le1/\sin(\delta/2)$。对权$1/n$作分部求和，得到$|\sum_{n=p}^q\sin(nx)/n|\le1/[p\sin(\delta/2)]$；此界与$x,q$无关，满足一致柯西准则。反之，取$x_N=\pi/(4N)$，对$N+1\le n\le2N$，$\pi/4<nx_N\le\pi/2$，故$\sin(nx_N)\ge\sqrt2/2$且$1/n\ge1/(2N)$，于是该块和不小于$\sqrt2/4$。块和不能一致趋于零，因此在整个开区间不一致收敛。

answer

远离周期端点的闭区间上一致收敛；在$(0,2\pi)$上不一致收敛。

scene_spec.objects[0]

证明$\sum_{n\ge1}\sin(nx)/n$在$[\delta,2\pi-\delta]$（$0<\delta<\pi$）上一致收敛，而在$(0,2\pi)$上不一致收敛。不得用其和函数的图像代替证明。

scene_spec.objects[1]

远离周期端点的闭区间上一致收敛；在$(0,2\pi)$上不一致收敛。

scene_spec.steps[0]

第一步:几何求和给任意正弦块$|\sum_{n=p}^q\sin(nx)|\le1/|\sin(x/2)|\le1/\sin(\delta/2)$。

scene_spec.steps[1]

第二步:对权$1/n$作分部求和，得到$|\sum_{n=p}^q\sin(nx)/n|\le1/[p\sin(\delta/2)]$；此界与$x,q$无关，满足一致柯西准则。

scene_spec.steps[2]

第三步:反之，取$x_N=\pi/(4N)$，对$N+1\le n\le2N$，$\pi/4<nx_N\le\pi/2$，故$\sin(nx_N)\ge\sqrt2/2$且$1/n\ge1/(2N)$，于是该块和不小于$\sqrt2/4$。

scene_spec.steps[3]

第四步:块和不能一致趋于零，因此在整个开区间不一致收敛。

## draft-c12-04

problem

固定$0<r<1$。证明$F_r(x)=\sum_{n=0}^{\infty}r^n\cos(nx)$在实轴上一致绝对收敛，求其和函数，并严格求$\int_0^\pi F_r(x)\,dx$。

solution

$|r^n\cos(nx)|\le r^n$，几何级数可和，故在实轴上一致绝对收敛。取$\sum r^ne^{inx}=1/(1-re^{ix})$的实部，得$F_r(x)=(1-r\cos x)/(1-2r\cos x+r^2)$；分母为$|1-re^{ix}|^2\ge(1-r)^2>0$。一致收敛允许在$[0,\pi]$逐项积分，常数项贡献$\pi$，每个$n\ge1$的积分$r^n[\sin(nx)/n]_0^\pi=0$，故积分为$\pi$。

answer

$F_r(x)=\frac{1-r\cos x}{1-2r\cos x+r^2}$，一致绝对收敛，积分$\pi$。

scene_spec.objects[0]

固定$0<r<1$。证明$F_r(x)=\sum_{n=0}^{\infty}r^n\cos(nx)$在实轴上一致绝对收敛，求其和函数，并严格求$\int_0^\pi F_r(x)\,dx$。

scene_spec.objects[1]

$F_r(x)=\frac{1-r\cos x}{1-2r\cos x+r^2}$，一致绝对收敛，积分$\pi$。

scene_spec.steps[0]

第一步:$|r^n\cos(nx)|\le r^n$，几何级数可和，故在实轴上一致绝对收敛。

scene_spec.steps[1]

第二步:取$\sum r^ne^{inx}=1/(1-re^{ix})$的实部，得$F_r(x)=(1-r\cos x)/(1-2r\cos x+r^2)$；分母为$|1-re^{ix}|^2\ge(1-r)^2>0$。

scene_spec.steps[2]

第三步:一致收敛允许在$[0,\pi]$逐项积分，常数项贡献$\pi$，每个$n\ge1$的积分$r^n[\sin(nx)/n]_0^\pi=0$，故积分为$\pi$。

## draft-c12-05

problem

证明函数列 $f_n(x)=n^2x(1-x^2)^n$($0\le x\le1$)逐点收敛于 $0$，但 $\int_0^1f_n(x)\,dx$ 不趋于 $0$；由此说明逐点收敛不足以保证极限与积分交换，并指出一致收敛为何是充分条件。

solution

$f_n(x)=n^2x(1-x^2)^n$在$[0,1]$逐点趋于零：端点直接为零，对$0<x<1$令$q=1-x^2<1$，$n^2q^n$的相邻比趋于$q<1$，故趋零。换元$u=1-x^2$给$\int_0^1f_n(x)dx=n^2/[2(n+1)]\ge n/4\to\infty$。由于$f_n\ge0$且区间长度为$1$，$\sup f_n\ge\int f_n\ge n/4$，所以不可能一致趋零，也不能交换极限与积分。在有限区间$[a,b]$上，若可积函数$g_n$一致收敛于$g$，则$g$可积且$\left|\int_a^b g_n(x)\,dx-\int_a^b g(x)\,dx\right|\le(b-a)\sup_{x\in[a,b]}|g_n(x)-g(x)|\to0$，所以一致收敛是交换积分与极限的充分条件；本题的连续函数列满足可积性，但不满足一致收敛。

answer

逐点极限$0$，非一致收敛；$\int_0^1f_n=n^2/[2(n+1)]\to+\infty$，不能交换极限与积分。一致收敛的充分性由积分差不超过区间长度乘一致误差证明。

scene_spec.objects[0]

证明函数列 $f_n(x)=n^2x(1-x^2)^n$($0\le x\le1$)逐点收敛于 $0$，但 $\int_0^1f_n(x)\,dx$ 不趋于 $0$；由此说明逐点收敛不足以保证极限与积分交换，并指出一致收敛为何是充分条件。

scene_spec.objects[1]

逐点极限$0$，非一致收敛；$\int_0^1f_n=n^2/[2(n+1)]\to+\infty$，不能交换极限与积分。一致收敛的充分性由积分差不超过区间长度乘一致误差证明。

scene_spec.steps[0]

第一步:$f_n(x)=n^2x(1-x^2)^n$在$[0,1]$逐点趋于零：端点直接为零，对$0<x<1$令$q=1-x^2<1$，$n^2q^n$的相邻比趋于$q<1$，故趋零。

scene_spec.steps[1]

第二步:换元$u=1-x^2$给$\int_0^1f_n(x)dx=n^2/[2(n+1)]\ge n/4\to\infty$。

scene_spec.steps[2]

第三步:由于$f_n\ge0$且区间长度为$1$，$\sup f_n\ge\int f_n\ge n/4$，所以不可能一致趋零，也不能交换极限与积分。

scene_spec.steps[3]

第四步:在有限区间$[a,b]$上，若可积函数$g_n$一致收敛于$g$，则$g$可积且$\left|\int_a^b g_n(x)\,dx-\int_a^b g(x)\,dx\right|\le(b-a)\sup_{x\in[a,b]}|g_n(x)-g(x)|\to0$，所以一致收敛是交换积分与极限的充分条件；本题的连续函数列满足可积性，但不满足一致收敛。

## draft-c14-01

problem

求$2\pi$周期函数$f(x)=|\sin x|$的实Fourier展开，证明展开在实轴上一致绝对收敛并确实等于$f$。

solution

$f$为偶函数，故$b_n=0$。$a_0=(2/\pi)\int_0^\pi\sin x\,dx=4/\pi$。用积化和差积分可得$a_n=0$（$n$奇），$a_{2k}=-4/[\pi(4k^2-1)]$（$k\ge1$）；在$n=1$时直接积分也为零，不能在含零分母的通式中代入。故展开为$2/\pi-(4/\pi)\sum_{k\ge1}\cos(2kx)/(4k^2-1)$。因$4k^2-1\ge3k^2$，系数绝对可和，由M判别法一致绝对收敛。$f$连续且分段光滑，Dirichlet定理给每点Fourier和等于$f$；端点及尖点的左右值相同，所以也无跳跃取值问题。

answer

$|\sin x|=\frac2\pi-\frac4\pi\sum_{k\ge1}\frac{\cos(2kx)}{4k^2-1}$，全实轴一致绝对收敛。

scene_spec.objects[0]

求$2\pi$周期函数$f(x)=|\sin x|$的实Fourier展开，证明展开在实轴上一致绝对收敛并确实等于$f$。

scene_spec.objects[1]

$|\sin x|=\frac2\pi-\frac4\pi\sum_{k\ge1}\frac{\cos(2kx)}{4k^2-1}$，全实轴一致绝对收敛。

scene_spec.steps[0]

第一步:$f$为偶函数，故$b_n=0$。

scene_spec.steps[1]

第二步:$a_0=(2/\pi)\int_0^\pi\sin x\,dx=4/\pi$。

scene_spec.steps[2]

第三步:用积化和差积分可得$a_n=0$（$n$奇），$a_{2k}=-4/[\pi(4k^2-1)]$（$k\ge1$）；在$n=1$时直接积分也为零，不能在含零分母的通式中代入。

scene_spec.steps[3]

第四步:故展开为$2/\pi-(4/\pi)\sum_{k\ge1}\cos(2kx)/(4k^2-1)$。

scene_spec.steps[4]

第五步:因$4k^2-1\ge3k^2$，系数绝对可和，由M判别法一致绝对收敛。

scene_spec.steps[5]

第六步:$f$连续且分段光滑，Dirichlet定理给每点Fourier和等于$f$；端点及尖点的左右值相同，所以也无跳跃取值问题。

## draft-c14-02

problem

求$f(x)=x(\pi-x)$在$[0,\pi]$的半区间正弦展开，并说明周期奇延拓的端点值和收敛方式。

solution

$b_n=(2/\pi)\int_0^\pi x(\pi-x)\sin(nx)dx$。两次分部积分，端点$f(0)=f(\pi)=0$且$f^{\prime\prime}=-2$，得积分$2[1-(-1)^n]/n^3$，所以$b_n=4[1-(-1)^n]/(\pi n^3)$。故$f(x)=(8/\pi)\sum_{k\ge0}\sin((2k+1)x)/(2k+1)^3$。奇延拓在$0,\pm\pi$左右极限都为零，连续、分段光滑；Dirichlet定理在每点取实际值。系数绝对可和，故周期展开全实轴一致绝对收敛。

answer

$x(\pi-x)=\frac8\pi\sum_{k\ge0}\frac{\sin((2k+1)x)}{(2k+1)^3}$；端点为零，一致绝对收敛。

scene_spec.objects[0]

求$f(x)=x(\pi-x)$在$[0,\pi]$的半区间正弦展开，并说明周期奇延拓的端点值和收敛方式。

scene_spec.objects[1]

$x(\pi-x)=\frac8\pi\sum_{k\ge0}\frac{\sin((2k+1)x)}{(2k+1)^3}$；端点为零，一致绝对收敛。

scene_spec.steps[0]

第一步:$b_n=(2/\pi)\int_0^\pi x(\pi-x)\sin(nx)dx$。

scene_spec.steps[1]

第二步:两次分部积分，端点$f(0)=f(\pi)=0$且$f^{\prime\prime}=-2$，得积分$2[1-(-1)^n]/n^3$，所以$b_n=4[1-(-1)^n]/(\pi n^3)$。

scene_spec.steps[2]

第三步:故$f(x)=(8/\pi)\sum_{k\ge0}\sin((2k+1)x)/(2k+1)^3$。

scene_spec.steps[3]

第四步:奇延拓在$0,\pm\pi$左右极限都为零，连续、分段光滑；Dirichlet定理在每点取实际值。

scene_spec.steps[4]

第五步:系数绝对可和，故周期展开全实轴一致绝对收敛。

## draft-c14-03

problem

将$2\pi$周期方波$f(x)=0$（$-\pi<x<0$）、$f(x)=1$（$0<x<\pi$）展开为Fourier级数；跳点$x\in\pi\mathbb Z$处定义$f(x)=0$。说明非跳点及跳点的级数取值。

solution

$a_0=\frac1\pi\int_{-\pi}^{\pi}f(x)\,dx=\frac1\pi\int_0^{\pi}1\,dx=1$。$a_n=\frac1\pi\int_0^{\pi}\cos nx\,dx=\frac{\sin n\pi}{n\pi}=0$($n\ge1$)。$b_n=\frac1\pi\int_0^{\pi}\sin nx\,dx=\frac{1-\cos n\pi}{n\pi}=\frac{1-(-1)^n}{n\pi}$,即奇数项 $b_{2k-1}=\frac{2}{(2k-1)\pi}$,偶数项为 $0$。故在非跳点 $f(x)=\frac12+\frac{2}{\pi}\sum_{k=1}^{\infty}\frac{\sin(2k-1)x}{2k-1}$。在间断点 $x=0,\pm\pi$ 处,由狄利克雷定理,级数和为左右极限的平均值 $\frac{0+1}{2}=\frac12$。

answer

非跳点上$f(x)=\frac12+\frac2\pi\sum_{k\ge0}\frac{\sin((2k+1)x)}{2k+1}$；在$x\in\pi\mathbb Z$，级数和为$1/2$，与任意指定单点值无关。

scene_spec.objects[0]

将$2\pi$周期方波$f(x)=0$（$-\pi<x<0$）、$f(x)=1$（$0<x<\pi$）展开为Fourier级数；跳点$x\in\pi\mathbb Z$处定义$f(x)=0$。说明非跳点及跳点的级数取值。

scene_spec.objects[1]

非跳点上$f(x)=\frac12+\frac2\pi\sum_{k\ge0}\frac{\sin((2k+1)x)}{2k+1}$；在$x\in\pi\mathbb Z$，级数和为$1/2$，与任意指定单点值无关。

scene_spec.steps[0]

第一步:$a_0=\frac1\pi\int_{-\pi}^{\pi}f(x)\,dx=\frac1\pi\int_0^{\pi}1\,dx=1$。

scene_spec.steps[1]

第二步:$a_n=\frac1\pi\int_0^{\pi}\cos nx\,dx=\frac{\sin n\pi}{n\pi}=0$($n\ge1$)。

scene_spec.steps[2]

第三步:$b_n=\frac1\pi\int_0^{\pi}\sin nx\,dx=\frac{1-\cos n\pi}{n\pi}=\frac{1-(-1)^n}{n\pi}$,即奇数项 $b_{2k-1}=\frac{2}{(2k-1)\pi}$,偶数项为 $0$。

scene_spec.steps[3]

第四步:故在非跳点 $f(x)=\frac12+\frac{2}{\pi}\sum_{k=1}^{\infty}\frac{\sin(2k-1)x}{2k-1}$。

scene_spec.steps[4]

第五步:在间断点 $x=0,\pm\pi$ 处,由狄利克雷定理,级数和为左右极限的平均值 $\frac{0+1}{2}=\frac12$。

## draft-c14-04

problem

设$f(x)=3+2\cos x-\sin(2x)$，$g(x)=f(x-\pi/3)$。求$g$的实Fourier系数，推导一般平移的系数变换，并证明每一频率的$a_n^2+b_n^2$不变。

solution

若平移量为$\alpha$，展开加法公式得$a_n^{\prime}=a_n\cos(n\alpha)-b_n\sin(n\alpha)$、$b_n^{\prime}=a_n\sin(n\alpha)+b_n\cos(n\alpha)$，常数项不变。这是二维正交变换，平方相加消去交叉项，得$(a_n^{\prime})^2+(b_n^{\prime})^2=a_n^2+b_n^2$。本题$a_0=6,a_1=2,b_2=-1$，其余为零，代入$\alpha=\pi/3$得到$g(x)=3+\cos x+\sqrt3\sin x+(\sqrt3/2)\cos(2x)+(1/2)\sin(2x)$，有限展开无需收敛交换。

answer

$g=3+\cos x+\sqrt3\sin x+\frac{\sqrt3}{2}\cos2x+\frac12\sin2x$；各频率系数平方和不变。

scene_spec.objects[0]

设$f(x)=3+2\cos x-\sin(2x)$，$g(x)=f(x-\pi/3)$。求$g$的实Fourier系数，推导一般平移的系数变换，并证明每一频率的$a_n^2+b_n^2$不变。

scene_spec.objects[1]

$g=3+\cos x+\sqrt3\sin x+\frac{\sqrt3}{2}\cos2x+\frac12\sin2x$；各频率系数平方和不变。

scene_spec.steps[0]

第一步:若平移量为$\alpha$，展开加法公式得$a_n^{\prime}=a_n\cos(n\alpha)-b_n\sin(n\alpha)$、$b_n^{\prime}=a_n\sin(n\alpha)+b_n\cos(n\alpha)$，常数项不变。

scene_spec.steps[1]

第二步:这是二维正交变换，平方相加消去交叉项，得$(a_n^{\prime})^2+(b_n^{\prime})^2=a_n^2+b_n^2$。

scene_spec.steps[2]

第三步:本题$a_0=6,a_1=2,b_2=-1$，其余为零，代入$\alpha=\pi/3$得到$g(x)=3+\cos x+\sqrt3\sin x+(\sqrt3/2)\cos(2x)+(1/2)\sin(2x)$，有限展开无需收敛交换。

## draft-c14-05

problem

令$f(x)=\cos x$，$g(x)=\cos x$（$x\notin2\pi\mathbb Z$），而$g(x)=5$（$x\in2\pi\mathbb Z$）。比较两者的Fourier系数与在$x=0$处的级数和。为什么系数相同不保证处处相同？

solution

在一个周期内，两函数只在有限点不同，这些点对积分无贡献，所以Fourier系数完全相同：$a_1=1$，其他系数为零，两者级数均为$\cos x$。在$0$处级数和为$1$，等于左右极限平均值，而$g(0)=5$。Fourier积分无法辨识零测集上的取值；在此例两函数几乎处处相等，却不处处相等。没有连续性等附加条件，不能从系数相同推出逐点相同。

answer

系数相同，级数均为$\cos x$；在$0$处和$1\ne g(0)=5$。

scene_spec.objects[0]

令$f(x)=\cos x$，$g(x)=\cos x$（$x\notin2\pi\mathbb Z$），而$g(x)=5$（$x\in2\pi\mathbb Z$）。比较两者的Fourier系数与在$x=0$处的级数和。为什么系数相同不保证处处相同？

scene_spec.objects[1]

系数相同，级数均为$\cos x$；在$0$处和$1\ne g(0)=5$。

scene_spec.steps[0]

第一步:在一个周期内，两函数只在有限点不同，这些点对积分无贡献，所以Fourier系数完全相同：$a_1=1$，其他系数为零，两者级数均为$\cos x$。

scene_spec.steps[1]

第二步:在$0$处级数和为$1$，等于左右极限平均值，而$g(0)=5$。

scene_spec.steps[2]

第三步:Fourier积分无法辨识零测集上的取值；在此例两函数几乎处处相等，却不处处相等。

scene_spec.steps[3]

第四步:没有连续性等附加条件，不能从系数相同推出逐点相同。
