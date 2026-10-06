"""Build batch-1 named scene patches (10 questions from the 90 remaining
REVISE list) per the OPERATING_GUIDE contract. Only scene_spec changes;
math three fields byte-identical. Every computation in the new scenes was
independently re-derived from the solution (see inline notes)."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "reviews/2026-10-05-training-diversity-drafts"
OUT = ROOT / "reviews/2026-10-06-scene-standard-sweep/batch1-patches.json"

# 新场景(逐题独立复算过;5 步,第N步: 风格,公式 $...$)
NEW_SCENES = {
    "draft-c02-01": {
        "objects": [
            "题面卡:证明 $\\int_1^{\\infty}\\sin(x^2)\\,dx$ 收敛但不绝对收敛",
            "板书一:换元 $u=x^2$ 得 $\\int_{R^2}^{T^2}\\frac{\\sin u}{2\\sqrt u}\\,du$,权重 $w(u)=\\frac{1}{2\\sqrt u}$",
            "板书二:分部积分 $[-w\\cos u]_{R^2}^{T^2}+\\int w'\\cos u\\,du$ 与放缩链",
            "高亮框:关键点 1——$w$ 正且递减,$\\int|w'|=w(R^2)-w(T^2)$;关键点 2——$[n\\pi+\\frac{\\pi}{6},n\\pi+\\frac{5\\pi}{6}]$ 上 $|\\sin u|\\ge\\frac12$",
            "结论卡:$|\\int_R^T\\sin(x^2)dx|\\le\\frac1R$,条件收敛",
        ],
        "steps": [
            "第一步:换元 $u=x^2$:尾积分化为 $\\int_{R^2}^{T^2}\\frac{\\sin u}{2\\sqrt u}\\,du$;标注振荡项 $\\sin u$ 与递减权重 $w(u)=\\frac{1}{2\\sqrt u}$。",
            "第二步:分部积分:逐项写出 $\\int w\\sin u\\,du=[-w\\cos u]_{R^2}^{T^2}+\\int_{R^2}^{T^2}w'(u)\\cos u\\,du$;绝对值 $\\le w(R^2)+w(T^2)+\\int|w'|$;关键点:因 $w$ 递减,$\\int|w'|=w(R^2)-w(T^2)$,故总界 $=2w(R^2)=\\frac1R$(高亮逐项放缩)。",
            "第三步:用柯西准则(关键点):对任意 $T'>T\\ge R\\ge1$,$|\\int_T^{T'}\\sin(x^2)dx|\\le\\frac1T\\to0$,与 $T'$ 无关且随 $T$ 收缩;故广义积分收敛。",
            "第四步:绝对值积分换元为 $\\int_1^{\\infty}\\frac{|\\sin u|}{2\\sqrt u}\\,du$;关键点:在每个 $[n\\pi+\\frac{\\pi}{6},n\\pi+\\frac{5\\pi}{6}]$ 上 $|\\sin u|\\ge\\frac12$(高亮区间选取)。",
            "第五步:每段贡献 $\\ge\\frac12\\cdot\\frac{1}{2\\sqrt{(n+1)\\pi}}\\cdot\\frac{2\\pi}{3}=\\frac{\\sqrt\\pi}{6\\sqrt{n+1}}$;从 $n=N$ 到 $2N-1$ 共 $N$ 段,和 $\\ge\\frac{\\sqrt\\pi}{6}\\cdot\\frac{N}{\\sqrt{2N}}=\\frac{\\sqrt\\pi}{6}\\sqrt{\\frac N2}\\to\\infty$;结论:不绝对收敛,条件收敛,尾界 $\\frac1R$。",
        ],
    },
    "draft-c04-04": {
        "objects": [
            "坐标系:抛物线弧 $L$($y=x^2$,从 $(0,0)$ 到 $(1,1)$)与虚线补边 $L'$",
            "板书一:$\\frac{\\partial Q}{\\partial x}=\\frac{\\partial(x)}{\\partial x}=1$,$\\frac{\\partial P}{\\partial y}=\\frac{\\partial(x+y)}{\\partial y}=1$",
            "板书二:参数化 $x=y=1-t$,$dx=dy=-dt$,代入得 $\\int_0^1(3t-3)dt$",
            "板书三:原函数 $\\frac{3t^2}{2}-3t$ 与上下限代入 $-\\frac32$",
            "结论卡:$\\int_L=\\frac32$",
        ],
        "steps": [
            "第一步:画出抛物线弧 $L$:从 $(0,0)$ 沿 $y=x^2$ 到 $(1,1)$;虚线补直线段 $L'$:从 $(1,1)$ 沿直线回到 $(0,0)$,构成闭合回路 $L+L'$。",
            "第二步:逐项求偏导(高亮):$\\frac{\\partial Q}{\\partial x}=\\frac{\\partial(x)}{\\partial x}=1$;$\\frac{\\partial P}{\\partial y}=\\frac{\\partial(x+y)}{\\partial y}=1$;故 $\\frac{\\partial Q}{\\partial x}-\\frac{\\partial P}{\\partial y}=1-1=0$。",
            "第三步:由格林公式:$\\oint_{L+L'}=\\iint_D 0\\,dxdy=0$,故 $\\int_L=-\\int_{L'}$。",
            "第四步:参数化补边:$x=y=1-t$,$t:0\\to1$,则 $dx=dy=-dt$;逐项代入:$P=x+y=2-2t$,$Q=x=1-t$;得 $\\int_{L'}=\\int_0^1[(2-2t)(-1)+(1-t)(-1)]dt=\\int_0^1(3t-3)dt$。",
            "第五步:求原函数 $\\int(3t-3)dt=\\frac{3t^2}{2}-3t$;代入上下限:$[\\frac{3t^2}{2}-3t]_0^1=\\frac32-3=-\\frac32$;取负得 $\\int_L=-(-\\frac32)=\\frac32$,高亮结论。",
        ],
    },
    "draft-c06-01": {
        "objects": [
            "坐标系:抛物线 $y=x^2$ 与 $y=2-x^2$,交点 $x=\\pm1$ 高亮",
            "阴影区域与上下曲线标注($2-x^2\\ge x^2$)",
            "板书:$A=2\\int_0^1(2-2x^2)dx$(对称性)",
            "板书:原函数 $2x-\\frac{2x^3}{3}$ 与上下限代入",
            "结论卡:$A=\\frac83$",
        ],
        "steps": [
            "第一步:画出 $y=x^2$ 与 $y=2-x^2$;解交点:$x^2=2-x^2$ 得 $x^2=1$,$x=\\pm1$,高亮两交点。",
            "第二步:阴影标出围成区域;标注区间内上曲线为 $2-x^2$、下曲线为 $x^2$,被积函数取差。",
            "第三步:写出积分 $A=\\int_{-1}^{1}[(2-x^2)-x^2]dx$;被积函数 $2-2x^2$ 为偶函数,对称性得 $A=2\\int_0^1(2-2x^2)dx$。",
            "第四步:逐项求原函数:$\\int 2\\,dx=2x$,$\\int 2x^2\\,dx=\\frac{2x^3}{3}$;故原函数为 $2x-\\frac{2x^3}{3}$。",
            "第五步:代入上下限:$[2x-\\frac{2x^3}{3}]_0^1=(2-\\frac23)-0=\\frac43$;乘对称因子:$A=2\\times\\frac43=\\frac83$,高亮结论。",
        ],
    },
    "draft-c11-01": {
        "objects": [
            "题面卡:$\\sum_{n=1}^{\\infty}(\\frac{n}{n+1})^{n^2}x^n$ 的收敛域",
            "板书一:关键不等式 $u\\le-\\ln(1-u)\\le\\frac{u}{1-u}$ 及其积分来源",
            "板书二:夹逼链 $\\frac{n}{n+1}\\le-n\\ln(1-u_n)\\le1$ 与 $\\sqrt[n]{a_n}\\to e^{-1}$",
            "数轴:收敛区间 $(-e,e)$ 与端点检查",
            "结论卡:收敛域 $(-e,e)$,端点通项 $|a_ne^n|\\to e^{1/2}\\ne0$",
        ],
        "steps": [
            "第一步:写出通项 $a_n=(\\frac{n}{n+1})^{n^2}$,说明用根值法;设 $u_n=\\frac1{n+1}$,则 $a_n=(1-u_n)^{n^2}$。",
            "第二步:展示关键不等式(高亮):对 $0<u<1$,$u\\le-\\ln(1-u)\\le\\frac{u}{1-u}$(来源:$-\\ln(1-u)=\\int_0^u\\frac{dt}{1-t}$,被积函数介于 $1$ 与 $\\frac1{1-u}$ 之间);取 $u=u_n$ 得夹逼链 $\\frac{n}{n+1}\\le-n\\ln(1-u_n)\\le1$。",
            "第三步:于是 $n\\ln(1-u_n)\\to-1$,即 $\\sqrt[n]{a_n}=(1-\\frac1{n+1})^n\\to e^{-1}$;收敛半径 $R=e$;数轴画出 $(-e,e)$。",
            "第四步:端点检查(关键点):展开 $-\\ln(1-u)=u+\\frac{u^2}{2}+r(u)$,余项估计 $0\\le r(u)=\\sum_{k\\ge3}\\frac{u^k}{k}\\le\\frac{u^3}{3(1-u)}$;取 $u=u_n$ 得 $n^2r(u_n)\\to0$。",
            "第五步:逐项代入 $x=\\pm e$:$n+n^2\\ln(1-u_n)=n-\\frac{n^2}{n+1}-\\frac{n^2}{2(n+1)^2}-n^2r(u_n)\\to1-\\frac12=\\frac12$;故 $|a_ne^n|\\to e^{1/2}\\ne0$,通项不趋于零,两端点发散;收敛域为 $(-e,e)$。",
        ],
    },
    "draft-c11-04": {
        "objects": [
            "板书一:特征方程 $\\lambda^2=\\lambda+2$ 与根 $2,-1$",
            "板书二:初值代入 $a_0=1,a_1=0$ 得 $a_n=\\frac{2^n+2(-1)^n}{3}$",
            "板书三:拆和 $S(x)=\\frac1{3(1-2x)}+\\frac2{3(1+x)}=\\frac{1-x}{1-x-2x^2}$",
            "端点检查卡:$x=\\pm\\frac12$ 通项趋于 $\\frac13\\ne0$",
            "结论卡:收敛域 $(-\\frac12,\\frac12)$,$S(\\frac14)=\\frac65$",
        ],
        "steps": [
            "第一步:解递推(逐步):设 $a_n=\\lambda^n$ 代入得 $\\lambda^n=\\lambda^{n-1}+2\\lambda^{n-2}$,即特征方程 $\\lambda^2=\\lambda+2$;因式分解 $\\lambda^2-\\lambda-2=(\\lambda-2)(\\lambda+1)=0$,根为 $2,-1$。",
            "第二步:通解 $a_n=c_1 2^n+c_2(-1)^n$;初值代入:$a_0=c_1+c_2=1$,$a_1=2c_1-c_2=0$;解得 $c_1=\\frac13,c_2=\\frac23$,故 $a_n=\\frac{2^n+2(-1)^n}{3}$;验证 $n=2$:$a_2=a_1+2a_0=2$ 与公式 $\\frac{4+2}{3}=2$ 一致(高亮)。",
            "第三步:拆成两个几何级数:$S(x)=\\frac13\\sum(2x)^n+\\frac23\\sum(-x)^n$;收敛条件 $|2x|<1$ 且 $|x|<1$,即 $|x|<\\frac12$;通分求和:$\\frac{1}{3(1-2x)}+\\frac{2}{3(1+x)}=\\frac{(1+x)+2(1-2x)}{3(1-2x)(1+x)}=\\frac{3-3x}{3(1-x-2x^2)}=\\frac{1-x}{1-x-2x^2}$。",
            "第四步:端点检查(逐项):$x=\\frac12$ 时 $a_n(\\frac12)^n=\\frac{2^n+2(-1)^n}{3\\cdot2^n}=\\frac13+\\frac{2(-1)^n}{3\\cdot2^n}\\to\\frac13\\ne0$;$x=-\\frac12$ 时 $|a_n(-\\frac12)^n|=|\\frac{(-1)^n+2(\\frac12)^n}{3}|\\to\\frac13\\ne0$;两端通项均不趋于零,发散。",
            "第五步:收敛域为 $(-\\frac12,\\frac12)$;计算 $S(\\frac14)$:代入和函数 $\\frac{1-\\frac14}{1-\\frac14-2\\cdot\\frac1{16}}=\\frac{3/4}{5/8}=\\frac34\\times\\frac85=\\frac65$(逐步分数运算,高亮)。",
        ],
    },
    "draft-c12-01": {
        "objects": [
            "题面卡:证 $\\sum_{n=1}^{\\infty}\\frac{\\sin nx}{n^2}$ 在 $\\mathbb R$ 上一致收敛",
            "板书一:逐项核对 $|\\frac{\\sin nx}{n^2}|\\le\\frac1{n^2}=M_n$",
            "高亮框:关键点 1——放缩依据 $|\\sin nx|\\le1$ 对一切 $x$ 成立;关键点 2——$\\sum\\frac1{n^2}$ 为 $p=2>1$ 的 $p$-级数,收敛",
            "板书二:$M$ 判别法结论与绝对一致收敛说明",
            "总结卡:对一切 $x$ 有 $|f_n(x)|\\le M_n$ 且 $\\sum M_n<\\infty$ $\\Rightarrow$ 一致收敛",
        ],
        "steps": [
            "第一步:写出目标:证明 $\\sum\\frac{\\sin nx}{n^2}$ 在 $\\mathbb R$ 上一致收敛;采用魏尔斯特拉斯 $M$ 判别法。",
            "第二步:逐项放缩(高亮关键点 1):对一切 $x\\in\\mathbb R$,$|\\sin nx|\\le1$,故 $|\\frac{\\sin nx}{n^2}|=\\frac{|\\sin nx|}{n^2}\\le\\frac1{n^2}=:M_n$;板书逐项核对 $|f_n(x)|\\le M_n$。",
            "第三步:验证 $\\sum M_n$(高亮关键点 2):$\\sum_{n=1}^{\\infty}\\frac1{n^2}$ 是 $p=2>1$ 的 $p$-级数,收敛。",
            "第四步:由 $M$ 判别法,级数在 $\\mathbb R$ 上一致收敛;且 $\\sum|f_n|$ 亦一致收敛,故绝对一致收敛。",
            "第五步:总结板书:条件「对一切 $x$ 有 $|f_n(x)|\\le M_n$」+「$\\sum M_n<\\infty$」两栏打勾,推出一致收敛,高亮结论。",
        ],
    },
    "draft-c23-01": {
        "objects": [
            "矩阵卡:$A=\\begin{pmatrix}0&1&0\\\\-1&0&0\\\\0&0&1\\end{pmatrix}$ 与 $A^{\\mathsf T}=\\begin{pmatrix}0&-1&0\\\\1&0&0\\\\0&0&1\\end{pmatrix}$",
            "行×列计算卡:$A^{\\mathsf T}b$ 三行分量逐项乘积",
            "板书:$T^{-1}(x)=A^{\\mathsf T}x+(2,-1,-3)$",
            "验证卡:$T(T^{-1}(x))=x$",
            "结论卡:$T^{-1}(x,y,z)=(-y+2,\\,x-1,\\,z-3)$",
        ],
        "steps": [
            "第一步:$A$ 为正交矩阵(行向量单位正交),等距变换的逆为 $T^{-1}(x)=A^{\\mathsf T}x-A^{\\mathsf T}b$;写出 $A^{\\mathsf T}=\\begin{pmatrix}0&-1&0\\\\1&0&0\\\\0&0&1\\end{pmatrix}$。",
            "第二步:逐行×列计算 $A^{\\mathsf T}b$(高亮分量乘积):第1行×列:$0\\cdot1+(-1)\\cdot2+0\\cdot3=-2$;第2行×列:$1\\cdot1+0\\cdot2+0\\cdot3=1$;第3行×列:$0\\cdot1+0\\cdot2+1\\cdot3=3$;得 $A^{\\mathsf T}b=(-2,1,3)$。",
            "第三步:代入公式:$T^{-1}(x)=A^{\\mathsf T}x-(-2,1,3)=A^{\\mathsf T}x+(2,-1,-3)$。",
            "第四步:验证:$T(T^{-1}(x))=A(A^{\\mathsf T}x-A^{\\mathsf T}b)+b=AA^{\\mathsf T}x-AA^{\\mathsf T}b+b=x-b+b=x$ ✓(用正交性 $AA^{\\mathsf T}=I$)。",
            "第五步:写分量形式:$T^{-1}(x,y,z)=(-y+2,\\,x-1,\\,z-3)$,高亮结论。",
        ],
    },
    "draft-c24-03": {
        "objects": [
            "矩阵卡:$A_t=\\begin{pmatrix}1&2\\\\t&t^2\\end{pmatrix}$,参数 $t$ 数轴标出 $0,2$",
            "板书一:$\\det A_t=1\\cdot t^2-2\\cdot t=t(t-2)$",
            "板书二:逆矩阵 $\\frac{1}{t(t-2)}\\begin{pmatrix}t^2&-2\\\\-t&1\\end{pmatrix}$ 与余子式来源",
            "奇异分析卡:$t=0$ 与 $t=2$ 的像集、相容条件、纤维",
            "结论卡:核方向 $(-2,1)$,两种奇异像方向不同",
        ],
        "steps": [
            "第一步:逐分量计算行列式:$\\det A_t=\\begin{vmatrix}1&2\\\\t&t^2\\end{vmatrix}=1\\cdot t^2-2\\cdot t=t(t-2)$;可逆当且仅当 $t\\ne0,2$(高亮)。",
            "第二步:伴随矩阵法求逆:余子式 $M_{11}=t^2,M_{12}=t,M_{21}=2,M_{22}=1$;代数余子式转置得 $\\begin{pmatrix}t^2&-2\\\\-t&1\\end{pmatrix}$;故 $A_t^{-1}=\\frac{1}{t(t-2)}\\begin{pmatrix}t^2&-2\\\\-t&1\\end{pmatrix}$。",
            "第三步:$t=0$ 代入:$A_0=\\begin{pmatrix}1&2\\\\0&0\\end{pmatrix}$,$T_0(x,y)=b+(x+2y,0)$;像集为 $b+\\operatorname{span}(1,0)$;相容条件 $v=b_2$;满足条件的原像由 $x+2y=s$ 解得 $x=s-2y$,纤维为 $(s-2r,r)$,$r\\in\\mathbb R$。",
            "第四步:$t=2$ 代入:$A_2=\\begin{pmatrix}1&2\\\\2&4\\end{pmatrix}$,$T_2(x,y)=b+(x+2y,2x+4y)=b+(x+2y)(1,2)$;像集为 $b+\\operatorname{span}(1,2)$;相容条件 $v-b_2=2s$($s=u-b_1$)。",
            "第五步:核方向:解齐次方程 $x+2y=0$ 得核 $=\\operatorname{span}(-2,1)$;两种奇异像方向不同,必须分别检查两个退化值,高亮结论。",
        ],
    },
    "draft-c26-03": {
        "objects": [
            "矩阵卡:$A=\\begin{pmatrix}1&2\\\\0&-1\\end{pmatrix}$",
            "逐分量代入卡:$A(A(x,y))=(x,y)$ 的完整计算",
            "固定线/变号线板:$x$ 轴与 $\\operatorname{span}(-1,1)$,斜分解示意",
            "范数卡:$\\|Ae_2\\|^2=2^2+(-1)^2=5\\ne1$",
            "结论卡:线性对合但不是 Euclidean 反射",
        ],
        "steps": [
            "第一步:证明 $A^2=I$(逐分量,高亮):$A(x,y)=(x+2y,-y)$;再作用一次:$A(A(x,y))=A(x+2y,-y)=((x+2y)+2(-y),-(-y))=(x,y)$;故 $A^2=I$。",
            "第二步:求固定线:解 $A(x,y)=(x,y)$ 得方程组 $\\begin{cases}x+2y=x\\\\-y=y\\end{cases}$,即 $y=0$;固定线为 $x$ 轴。",
            "第三步:求变号线:解 $A(x,y)=-(x,y)$ 得 $\\begin{cases}x+2y=-x\\\\-y=-y\\end{cases}$,即 $x=-y$;变号线为 $\\operatorname{span}(-1,1)$;两方向向量 $(1,0)$ 与 $(-1,1)$ 点积为 $-1\\ne0$,不垂直(高亮)。",
            "第四步:验证不等距:取 $e_2=(0,1)$,$\\|Ae_2\\|^2=\\|(2,-1)\\|^2=2^2+(-1)^2=5\\ne1=\\|e_2\\|^2$;故不保距离,不是 Euclidean 平面反射。",
            "第五步:任意向量唯一分解为两线分量之和,$A$ 固定第一分量、将第二分量变号 → 斜分解下的线性对合;结论:线性对合不一定是等距变换。",
        ],
    },
    "draft-c27-04": {
        "objects": [
            "矩阵卡:$A_k=\\begin{pmatrix}1&k\\\\0&2\\end{pmatrix}$",
            "特征值板:$\\det(A_k-\\lambda I)=(1-\\lambda)(2-\\lambda)$,特征值 $1,2$",
            "行×列验算卡:$A_kP$ 与 $P\\operatorname{diag}(1,2)$ 的四项分量乘积",
            "夹角推导板:$\\langle e_1,(k,1)\\rangle=k$,$\\cos\\alpha=\\frac{|k|}{\\sqrt{k^2+1}}$",
            "结论卡:所有 $k$ 可对角化;正交对角化当且仅当 $k=0$",
        ],
        "steps": [
            "第一步:求特征值:$\\det(A_k-\\lambda I)=\\begin{vmatrix}1-\\lambda&k\\\\0&2-\\lambda\\end{vmatrix}=(1-\\lambda)(2-\\lambda)$;特征值为 $1,2$。",
            "第二步:求特征向量:$\\lambda=1$:解 $(A_k-I)v=0$,即 $\\begin{pmatrix}0&k\\\\0&1\\end{pmatrix}v=0$,得 $v=e_1=(1,0)$;$\\lambda=2$:解 $(A_k-2I)v=0$,即 $-x+ky=0$,得 $v=(k,1)$。",
            "第三步:验算对角化(逐行×列,高亮):$P=\\begin{pmatrix}1&k\\\\0&1\\end{pmatrix}$;$A_kP$ 第1行×第1列:$1\\cdot1+k\\cdot0=1$;第1行×第2列:$1\\cdot k+k\\cdot1=2k$;第2行×第1列:$0\\cdot1+2\\cdot0=0$;第2行×第2列:$0\\cdot k+2\\cdot1=2$;得 $A_kP=\\begin{pmatrix}1&2k\\\\0&2\\end{pmatrix}=P\\operatorname{diag}(1,2)$;$\\det P=1$,故所有 $k$ 可对角化。",
            "第四步:夹角公式(逐项):两特征线方向 $e_1=(1,0)$ 与 $(k,1)$;点积 $\\langle e_1,(k,1)\\rangle=1\\cdot k+0\\cdot1=k$;模长 $\\|(k,1)\\|=\\sqrt{k^2+1}$,$\\|e_1\\|=1$;故 $\\cos\\alpha=\\frac{|k|}{1\\cdot\\sqrt{k^2+1}}$;仅 $k=0$ 时 $\\cos\\alpha=0$,垂直。",
            "第五步:正交对角化判定:实矩阵可正交对角化为实对角阵必对称;而 $A_k^{\\mathsf T}=\\begin{pmatrix}1&0\\\\k&2\\end{pmatrix}$ 与 $A_k$ 相等当且仅当 $k=0$;故正交对角化当且仅当 $k=0$,高亮结论。",
        ],
    },
}


def sorted_sha(obj) -> str:
    return hashlib.sha256(
        json.dumps(obj, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def main() -> int:
    try:
        sel_path = DRAFTS / "draft-selection.json"
        sel = json.loads(sel_path.read_text("utf-8-sig"))
        if sel.get("schema") != 2:
            raise ValueError("schema2 selector required")
        # id -> (batch entry, original record from selected file)
        found = {}
        for entry in sel["entries"]:
            path = DRAFTS / entry["path"]
            for line in path.read_text("utf-8-sig").splitlines():
                if not line.strip():
                    continue
                rec = json.loads(line)
                if rec["id"] in NEW_SCENES and rec["id"] not in found:
                    found[rec["id"]] = (entry, rec)
        if len(found) != len(NEW_SCENES):
            raise ValueError("missing records: " + str(set(NEW_SCENES) - set(found)))
        patches = []
        for cid, scene in NEW_SCENES.items():
            entry, rec = found[cid]
            old_math = {"problem": rec["problem"], "solution": rec["solution"],
                        "answer": rec["answer"], "scene_spec": rec["scene_spec"]}
            expected_record_sha256 = sorted_sha(rec)
            new_rec = dict(rec)
            new_rec["scene_spec"] = scene
            new_math = {"problem": rec["problem"], "solution": rec["solution"],
                        "answer": rec["answer"], "scene_spec": scene}
            new_math_content_sha256 = sorted_sha(new_math)
            # 数学三字段不变性自检
            for k in ("problem", "solution", "answer"):
                if new_rec[k] != rec[k]:
                    raise ValueError("math field drift: " + cid)
            # 独立复算自检:新旧 record 仅 scene_spec 之差
            if old_math["scene_spec"] == scene:
                raise ValueError("scene unchanged: " + cid)
            if sorted(old_math["scene_spec"].get("objects", [])) == sorted(scene.get("objects", [])) \
                    and old_math["scene_spec"].get("steps") == scene.get("steps"):
                raise ValueError("scene unchanged: " + cid)
            patches.append({
                "batch": entry["batch"],
                "id": cid,
                "expected_selected_path": entry["path"],
                "expected_hash_algorithm": sel["hash_algorithm"],
                "expected_selected_sha256": entry["sha256"],
                "expected_selected_raw_sha256": entry["raw_sha256"],
                "expected_record_sha256": expected_record_sha256,
                "new_math_content_sha256": new_math_content_sha256,
                "fields": {"scene_spec": scene},
            })
        out = {
            "schema": "scene-patches-batch-v1",
            "status": "PENDING_CODEX_REVIEW",
            "normalization": "sorted-json-default-separators",
            "records": patches,
        }
        if OUT.exists():
            raise ValueError("output exists")
        with OUT.open("x", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
        print("patches:", len(patches))
        for p in patches:
            print(" -", p["id"], "| batch:", p["batch"], "| rec_sha:", p["expected_record_sha256"][:12])
        return 0
    except Exception as exc:
        print("[FAIL]", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
