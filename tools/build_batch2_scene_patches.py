"""Build batch-2 named scene patches (10 questions) per OPERATING_GUIDE.
Only scene_spec changes; math three fields byte-identical; every computation
independently re-derived from the solution."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "reviews/2026-10-05-training-diversity-drafts"
OUT = ROOT / "reviews/2026-10-06-scene-standard-sweep/batch2-patches.json"

NEW_SCENES = {
    "draft-c10-01": {
        "objects": [
            "通项卡:奇项 $u_{2k-1}=\\frac1k>0$、偶项 $u_{2k}=-\\frac1k+2^{-k}<0$",
            "部分和板书:$S_{2N}=1-2^{-N}$、$S_{2N+1}=1-2^{-N}+\\frac1{N+1}$ 逐项累加",
            "高亮框:关键点 1——成对求和化为几何级数;关键点 2——绝对值级数含 $2\\sum1/k$ 发散",
            "反例卡:$|u_4|=\\frac14<\\frac13=|u_5|$,绝对值不单调",
            "结论卡:条件收敛,和 $1$;单调性是充分条件而非必要条件",
        ],
        "steps": [
            "第一步:逐项写出:奇项 $u_{2k-1}=\\frac1k>0$;偶项 $u_{2k}=-\\frac1k+2^{-k}$;关键点:由 $2^k>k$ 得 $2^{-k}<\\frac1k$,故偶项为负,正负交错(高亮)。",
            "第二步:逐项累加部分和(关键点:奇偶成对求和):$S_{2N}=\\sum_{k=1}^N(\\frac1k-\\frac1k+2^{-k})=\\sum_{k=1}^N2^{-k}=1-2^{-N}$(几何级数);$S_{2N+1}=S_{2N}+u_{2N+1}=1-2^{-N}+\\frac1{N+1}$;两式均趋于 $1$。",
            "第三步:绝对值级数逐项对照:$\\sum_{n=1}^{2N}|u_n|=2\\sum_{k=1}^N\\frac1k-\\sum_{k=1}^N2^{-k}=2\\sum_{k=1}^N\\frac1k-1+2^{-N}$;关键点:调和级数发散、几何部分和有界,故该和趋于 $+\\infty$。",
            "第四步:结论:级数收敛但绝对值级数发散 → 条件收敛,和为 $1$(高亮)。",
            "第五步:单调性检查(关键点):$|u_4|=\\frac14<\\frac13=|u_5|$,绝对值不单调;莱布尼茨的单调条件是充分条件,不是必要条件;高亮结论。",
        ],
    },
    "draft-c10-03": {
        "objects": [
            "通项拆解卡:$n=2k-1$ 项为 $-\\frac1{2k-1}$、$n=2k$ 项为 $\\frac3{2k}$",
            "成对和板书:$\\frac{4k-3}{2k(2k-1)}\\ge\\frac1{2k}$ 的放缩依据",
            "高亮框:关键点 1——$S_{2N}\\ge\\frac12\\sum1/k\\to+\\infty$;关键点 2——振幅 $\\frac1{2k-1}<\\frac3{2k}$ 不递减",
            "莱布尼茨检查卡:单调条件不满足",
            "结论卡:级数发散到 $+\\infty$",
        ],
        "steps": [
            "第一步:逐项计算通项:$n=2k-1$ 时 $\\frac{(-1)^n(2+(-1)^n)}n=\\frac{(-1)(2-1)}{2k-1}=-\\frac1{2k-1}$;$n=2k$ 时 $=\\frac{(1)(2+1)}{2k}=\\frac3{2k}$(高亮拆解)。",
            "第二步:成对求和(逐项):第 $k$ 对和 $=\\frac3{2k}-\\frac1{2k-1}=\\frac{3(2k-1)-2k}{2k(2k-1)}=\\frac{4k-3}{2k(2k-1)}$;放缩(关键点):$4k-3\\ge2k-1$ 对 $k\\ge1$ 成立,故 $\\ge\\frac1{2k}$。",
            "第三步:部分和下界(关键点):$S_{2N}=\\sum_{k=1}^N\\frac{4k-3}{2k(2k-1)}\\ge\\sum_{k=1}^N\\frac1{2k}=\\frac12\\sum_{k=1}^N\\frac1k\\to+\\infty$。",
            "第四步:奇部分和:$S_{2N+1}=S_{2N}+u_{2N+1}=S_{2N}-\\frac1{2N+1}\\to+\\infty$;故级数发散到 $+\\infty$。",
            "第五步:莱布尼茨为何不可用(关键点):振幅不递减:$\\frac1{2k-1}<\\frac3{2k}$(因 $2k<6k-3$,即 $4k-3>0$);通项绝对值不单调,莱布尼茨前提不满足,高亮结论。",
        ],
    },
    "draft-c12-03": {
        "objects": [
            "题面卡:$\\sum\\sin(nx)/n$ 在 $[\\delta,2\\pi-\\delta]$ 一致、在 $(0,2\\pi)$ 不一致",
            "板书一:几何求和恒等式 $2\\sin\\frac x2\\sum_{n=p}^q\\sin(nx)=\\cos((p-\\frac12)x)-\\cos((q+\\frac12)x)$",
            "板书二:Abel 分部求和展开 $S_q/q+\\sum_{k=p}^{q-1}S_k(\\frac1k-\\frac1{k+1})$ 与放缩",
            "高亮框:关键点 1——界与 $x,q$ 无关→一致柯西准则;关键点 2——$x_N=\\frac{\\pi}{4N}$ 使块和为常数 $\\frac{\\sqrt2}4$",
            "结论卡:闭区间一致收敛;开区间不一致收敛",
        ],
        "steps": [
            "第一步:几何求和恒等式(逐步推导):两端乘 $2\\sin\\frac x2$ 并逐项积化和差:$2\\sin\\frac x2\\sum_{n=p}^q\\sin(nx)=\\sum_{n=p}^q[\\cos((n-\\frac12)x)-\\cos((n+\\frac12)x)]=\\cos((p-\\frac12)x)-\\cos((q+\\frac12)x)$;取绝对值 $\\le2$,故 $|\\sum_{n=p}^q\\sin(nx)|\\le\\frac1{|\\sin(x/2)|}$。",
            "第二步:在 $[\\delta,2\\pi-\\delta]$ 上(关键点):$|\\sin(x/2)|\\ge\\sin(\\delta/2)$,故任意正弦块 $\\le\\frac1{\\sin(\\delta/2)}$,与 $p,q,x$ 无关(高亮)。",
            "第三步:Abel 分部求和(逐项展开):记 $S_k=\\sum_{n=p}^k\\sin(nx)$,则 $\\sum_{n=p}^q\\frac{\\sin(nx)}n=\\frac{S_q}{q}+\\sum_{k=p}^{q-1}S_k(\\frac1k-\\frac1{k+1})$;逐项取绝对值:$\\le\\frac1{q\\sin(\\delta/2)}+\\sum_{k=p}^{q-1}\\frac1{\\sin(\\delta/2)}(\\frac1k-\\frac1{k+1})=\\frac1{p\\sin(\\delta/2)}$。",
            "第四步:该界与 $x,q$ 无关且随 $p\\to\\infty$ 收缩(关键点)→ 满足一致柯西准则;故在 $[\\delta,2\\pi-\\delta]$ 上一致收敛。",
            "第五步:反例(关键点:选取意图是让整块正弦都大):取 $x_N=\\frac{\\pi}{4N}$;对 $N+1\\le n\\le2N$,$\\frac{\\pi}4<nx_N\\le\\frac{\\pi}2$,故 $\\sin(nx_N)\\ge\\frac{\\sqrt2}2$ 且 $\\frac1n\\ge\\frac1{2N}$;该块和 $\\ge N\\cdot\\frac{\\sqrt2}2\\cdot\\frac1{2N}=\\frac{\\sqrt2}4$;块和不一致趋于零 → 在 $(0,2\\pi)$ 上不一致收敛。",
        ],
    },
    "draft-c14-01": {
        "objects": [
            "函数卡:$f(x)=|\\sin x|$ 的图像与偶函数标记",
            "板书一:$a_0=\\frac2\\pi\\int_0^\\pi\\sin x\\,dx=\\frac4\\pi$ 的逐项计算",
            "板书二:积化和差 $2\\sin x\\cos(nx)=\\sin((n+1)x)-\\sin((n-1)x)$ 与 $a_{2k}=-\\frac4{\\pi(4k^2-1)}$ 推导",
            "高亮框:关键点 1——$n=1$ 时分母为零,单独直接积分得 $0$;关键点 2——$4k^2-1\\ge3k^2$ 的 M 判别放缩",
            "结论卡:$|\\sin x|=\\frac2\\pi-\\frac4\\pi\\sum_{k\\ge1}\\frac{\\cos(2kx)}{4k^2-1}$,全实轴一致绝对收敛",
        ],
        "steps": [
            "第一步:$f$ 为偶函数,故 $b_n=0$;常数项(逐项):$a_0=\\frac2\\pi\\int_0^\\pi\\sin x\\,dx=\\frac2\\pi[-\\cos x]_0^\\pi=\\frac2\\pi(1-(-1))=\\frac4\\pi$。",
            "第二步:积化和差(逐步):$2\\sin x\\cos(nx)=\\sin((n+1)x)-\\sin((n-1)x)$;对 $n\\ne1$,$\\int_0^\\pi\\sin x\\cos(nx)dx=\\frac12[-\\frac{\\cos((n+1)x)}{n+1}+\\frac{\\cos((n-1)x)}{n-1}]_0^\\pi$;代入上下限:$n=2k$ 时得 $-\\frac2{4k^2-1}$,故 $a_{2k}=\\frac2\\pi\\cdot(-\\frac2{4k^2-1})=-\\frac4{\\pi(4k^2-1)}$;$n$ 为奇数(且 $n\\ne1$)时两端抵消得 $0$。",
            "第三步:关键点:$n=1$ 时通式分母为零,必须单独直接积分:$\\int_0^\\pi\\sin x\\cos x\\,dx=\\frac12\\int_0^\\pi\\sin(2x)dx=\\frac12[-\\frac{\\cos2x}{2}]_0^\\pi=0$(高亮:不能代入含零分母的通式)。",
            "第四步:写出展开:$f(x)=\\frac{a_0}{2}-\\frac4\\pi\\sum_{k\\ge1}\\frac{\\cos(2kx)}{4k^2-1}=\\frac2\\pi-\\frac4\\pi\\sum_{k\\ge1}\\frac{\\cos(2kx)}{4k^2-1}$。",
            "第五步:M 判别(关键点):$4k^2-1\\ge3k^2$(因 $k^2\\ge1$),故 $|\\frac{\\cos(2kx)}{4k^2-1}|\\le\\frac1{3k^2}$ 且 $\\sum\\frac1{3k^2}$ 收敛 → 全实轴一致绝对收敛;$f$ 连续且分段光滑,Dirichlet 定理给每点 Fourier 和 $=f$;端点与尖点处左右值相同,无跳跃取值问题。",
        ],
    },
    "draft-c26-04": {
        "objects": [
            "映射卡:$T(x)=(x_3,x_4,0,0)$ 与 $U(x)=(x_2,x_3,0,0)$",
            "迭代板书:$T^2=0$、$U^2\\ne0$、$U^3=0$ 的逐分量代入",
            "像维数链:卡:$4\\to2\\to0$ 与 $4\\to2\\to1\\to0$ 的柱状图对照",
            "高亮框:关键点——相似保持所有幂的秩/最小归零次数;非零幂零矩阵不可对角化",
            "结论卡:秩均 $2$;不相似;均不可对角化",
        ],
        "steps": [
            "第一步:求一次像:对 $x=(x_1,x_2,x_3,x_4)$,$T(x)=(x_3,x_4,0,0)$ 的像为后两坐标自由的平面;$U(x)=(x_2,x_3,0,0)$ 的像为前两坐标自由的平面;两者像维数均为 $2$;像维数序列起点 $4,2$(高亮)。",
            "第二步:逐分量迭代(高亮):$T^2(x)=T(x_3,x_4,0,0)=(0,0,0,0)$,故 $T^2=0$ 而 $T\\ne0$;像维数 $4\\to2\\to0$,最小归零次数为 $2$。",
            "第三步:逐分量迭代:$U^2(x)=U(x_2,x_3,0,0)=(x_3,0,0,0)\\ne0$(第三坐标残留);$U^3(x)=U(x_3,0,0,0)=(0,0,0,0)$;像维数 $4\\to2\\to1\\to0$,最小归零次数为 $3$。",
            "第四步:不相似(关键点):相似变换保持所有幂的秩,即保持最小归零次数;$T$ 二次归零、$U$ 三次归零,故不相似(高亮)。",
            "第五步:不可对角化(关键点):若非零幂零矩阵可对角化,特征值全为零,对角化结果只能为零矩阵,矛盾;故两者均不可对角化;相同一次秩不足以描述线性迭代的几何压缩。",
        ],
    },
    "draft-c27-01": {
        "objects": [
            "矩阵卡:$A=I+uv^{\\mathsf T}$,$\\alpha=v^{\\mathsf T}u$",
            "板书一:$N^2=(uv^{\\mathsf T})(uv^{\\mathsf T})=u(v^{\\mathsf T}u)v^{\\mathsf T}=\\alpha N$ 的逐项推导",
            "直和分解图:$\\mathbb R^n=\\ker v^{\\mathsf T}\\oplus\\operatorname{span}(u)$($\\alpha\\ne0$)",
            "作用计算卡:$Ax=x$(超平面)与 $Au=(1+\\alpha)u$ 的逐项代入",
            "结论卡:$\\alpha\\ne0$ 可对角化;$\\alpha=0$ 不可,最小多项式 $(\\lambda-1)^2$",
        ],
        "steps": [
            "第一步:计算 $N^2$(逐项,高亮):$N^2=(uv^{\\mathsf T})(uv^{\\mathsf T})=u(v^{\\mathsf T}u)v^{\\mathsf T}=u\\alpha v^{\\mathsf T}=\\alpha uv^{\\mathsf T}=\\alpha N$(关键点:矩阵乘法结合律,标量 $\\alpha$ 提出)。",
            "第二步:$\\alpha\\ne0$ 情形:超平面 $\\ker v^{\\mathsf T}$ 维数 $n-1$;验证 $u\\notin\\ker v^{\\mathsf T}$:因 $v^{\\mathsf T}u=\\alpha\\ne0$;故全空间分解为直和 $\\mathbb R^n=\\ker v^{\\mathsf T}\\oplus\\operatorname{span}(u)$。",
            "第三步:逐项作用(高亮):$x\\in\\ker v^{\\mathsf T}$ 时 $Ax=x+u(v^{\\mathsf T}x)=x+u\\cdot0=x$,作用为特征值 $1$;$Au=u+u(v^{\\mathsf T}u)=u+\\alpha u=(1+\\alpha)u$,作用为特征值 $1+\\alpha$。",
            "第四步:两个不同特征值 $1$ 与 $1+\\alpha$ 都出现 → 可对角化;最小多项式为 $(\\lambda-1)(\\lambda-1-\\alpha)$(高亮)。",
            "第五步:$\\alpha=0$ 情形:$N^2=0$ 但 $N\\ne0$;$A=I+N$ 特征值全为 $1$;最小多项式为 $(\\lambda-1)^2$;若可对角化只能 $A=I$,与 $N\\ne0$ 矛盾(关键点);故不可对角化。",
        ],
    },
    "draft-c41-02": {
        "objects": [
            "矩阵卡:$B=\\begin{pmatrix}1&-2\\\\2&1\\end{pmatrix}$,$A=\\begin{pmatrix}B&I_2\\\\0&B\\end{pmatrix}$",
            "板书一:特征多项式 $\\lambda^2-2\\lambda+5=0$ 与求根 $1\\pm2i$",
            "广义向量卡:$(A-\\lambda_\\pm I)w_\\pm=v_\\pm$ 的分块验证",
            "板书二:$[(\\lambda-1)^2+4]^2$ 的逐步展开",
            "结论卡:Jordan 形式 $J_2(1+2i)\\oplus J_2(1-2i)$,实最小多项式 $[(\\lambda-1)^2+4]^2$,不可对角化",
        ],
        "steps": [
            "第一步:求 $B$ 的特征值(逐步):特征多项式 $\\det(B-\\lambda I)=\\begin{vmatrix}1-\\lambda&-2\\\\2&1-\\lambda\\end{vmatrix}=(1-\\lambda)^2+4=\\lambda^2-2\\lambda+5$;解 $\\lambda^2-2\\lambda+5=0$:求根公式 $\\lambda=\\frac{2\\pm\\sqrt{4-20}}2=1\\pm2i$(高亮)。",
            "第二步:求特征向量:对 $\\lambda_+=1+2i$,解 $(B-\\lambda_+I)q=0$:即 $\\begin{pmatrix}-2i&-2\\\\2&-2i\\end{pmatrix}q=0$,$-2iq_1-2q_2=0$;取 $q_+=(1,-i)^{\\mathsf T}$;共轭得 $q_-=(1,i)^{\\mathsf T}$。",
            "第三步:构造广义特征向量(分块逐项验证):令 $v_\\pm=(q_\\pm,0)$、$w_\\pm=(0,q_\\pm)$;$(A-\\lambda_\\pm I)w_\\pm=((B-\\lambda_\\pm I)\\cdot0+I_2q_\\pm,\\,0)=(q_\\pm,0)=v_\\pm$;且 $(A-\\lambda_\\pm I)v_\\pm=((B-\\lambda_\\pm I)q_\\pm,0)=(0,0)$(高亮两级链)。",
            "第四步:$q_+,q_-$ 独立,故 $v_+,w_+,v_-,w_-$ 四向量组成复基;每个根一个二阶块 → Jordan 形式 $J_2(1+2i)\\oplus J_2(1-2i)$。",
            "第五步:复最小多项式 $=(\\lambda-1-2i)^2(\\lambda-1+2i)^2$;逐步展开:$\\lambda-1-2i$ 与 $\\lambda-1+2i$ 相乘 $=(\\lambda-1)^2+4$;故实最小多项式 $=[(\\lambda-1)^2+4]^2$;两个二阶块 → 不可对角化(高亮)。",
        ],
    },
    "draft-c42-04": {
        "objects": [
            "矩阵卡:$A=\\begin{pmatrix}\\frac12&\\frac{\\sqrt3}{2}&0\\\\-\\frac{\\sqrt3}{2}&\\frac12&0\\\\0&0&-1\\end{pmatrix}$",
            "正交验证板:三列模长与两两内积的逐项计算",
            "特征多项式板:$(\\lambda+1)(\\lambda^2-\\lambda+1)$ 的展开与求根",
            "几何解释图:$z$ 轴旋转 $-\\pi/3$ 与 $xy$ 平面反射",
            "结论卡:正交,$\\det A=-1$;复合变换;无非零逐点固定向量",
        ],
        "steps": [
            "第一步:列向量正交性验证(逐项):三列 $c_1=(\\frac12,-\\frac{\\sqrt3}2,0)$,$c_2=(\\frac{\\sqrt3}2,\\frac12,0)$,$c_3=(0,0,-1)$;模长:$\\|c_1\\|^2=\\frac14+\\frac34=1$,$\\|c_2\\|^2=\\frac34+\\frac14=1$,$\\|c_3\\|^2=1$;两两内积:$\\langle c_1,c_2\\rangle=\\frac12\\cdot\\frac{\\sqrt3}2+(-\\frac{\\sqrt3}2)\\cdot\\frac12+0=0$,$\\langle c_1,c_3\\rangle=0$,$\\langle c_2,c_3\\rangle=0$;故 $A^{\\mathsf T}A=I$,正交(高亮)。",
            "第二步:行列式:$\\det A=\\det(R(-\\pi/3))\\cdot(-1)=1\\cdot(-1)=-1$(分块:前两维是旋转块)。",
            "第三步:特征多项式(逐步):$\\det(A-\\lambda I)=[(\\frac12-\\lambda)^2+\\frac34](-1-\\lambda)=(\\lambda^2-\\lambda+1)(-1-\\lambda)$;求根:$\\lambda=-1$,以及 $\\lambda=\\frac{1\\pm\\sqrt{1-4}}2=\\frac12\\pm\\frac{\\sqrt3}2i$(高亮)。",
            "第四步:几何解释:前两维块为绕 $z$ 轴旋转 $-\\pi/3$,第三维 $-1$ 为关于 $xy$ 平面的反射;两者作用在不同坐标上,可交换 → 复合变换。",
            "第五步:关键点:特征值无 $1$,故无非零逐点固定向量;但 $z$ 轴仍是旋转因子的轴、作为集合被整个变换保持,轴上点变号;「没有逐点固定轴」不等于「复合中没有旋转轴」(高亮)。",
        ],
    },
    "draft-c07-01": {
        "objects": [
            "极坐标图:三叶玫瑰线 $r=2\\sin3\\theta$ 的一叶阴影",
            "角域标注卡:$0\\le\\theta\\le\\frac{\\pi}{3}$,叶的生成过程",
            "板书:$A=\\frac12\\int_0^{\\frac{\\pi}{3}}4\\sin^2(3\\theta)d\\theta=2\\int_0^{\\frac{\\pi}{3}}\\sin^2(3\\theta)d\\theta$",
            "换元板书:$u=3\\theta$、$du=3d\\theta$、$\\int_0^\\pi\\sin^2u\\,du=\\frac\\pi2$",
            "结论卡:$A=\\frac{\\pi}{3}$",
        ],
        "steps": [
            "第一步:确定一叶的角域(高亮):当 $\\theta$ 从 $0$ 到 $\\frac{\\pi}3$,$3\\theta$ 从 $0$ 到 $\\pi$,$r=2\\sin3\\theta$ 从 $0$ 增大到 $2$ 再回到 $0$,恰描出一叶。",
            "第二步:极坐标面积公式:$A=\\frac12\\int_0^{\\frac{\\pi}{3}}r^2\\,d\\theta=\\frac12\\int_0^{\\frac{\\pi}{3}}4\\sin^2(3\\theta)\\,d\\theta$;系数整理:$\\frac12\\times4=2$,得 $A=2\\int_0^{\\frac{\\pi}{3}}\\sin^2(3\\theta)\\,d\\theta$。",
            "第三步:换元(逐项):$u=3\\theta$,则 $du=3\\,d\\theta$,即 $d\\theta=\\frac13du$;上下限:$\\theta=0\\to u=0$,$\\theta=\\frac{\\pi}{3}\\to u=\\pi$;故 $A=\\frac23\\int_0^\\pi\\sin^2u\\,du$。",
            "第四步:计算定积分(逐步):半角公式 $\\sin^2u=\\frac{1-\\cos2u}{2}$;原函数 $\\frac{u}{2}-\\frac{\\sin2u}{4}$;代入:$[\\frac{u}{2}-\\frac{\\sin2u}{4}]_0^\\pi=\\frac{\\pi}{2}$。",
            "第五步:合起来:$A=\\frac23\\times\\frac{\\pi}{2}=\\frac{\\pi}{3}$(逐步分数乘法,高亮结论)。",
        ],
    },
    "draft-c49-03": {
        "objects": [
            "题面卡:$Y_n=\\sum_iw_{n,i}X_i$ 的 $L^2$ 收敛充要条件",
            "板书一:$EY_n=\\frac12$、$\\operatorname{Var}Y_n=\\frac1{12}\\sum_iw_{n,i}^2$ 的依据标注",
            "高亮框:关键点 1——$(\\max w)^2\\le\\sum w^2\\le\\max w$(依据 $w_i^2\\le w_i\\cdot\\max w$);关键点 2——平方和公式 $\\sum i^2=\\frac{n(n+1)(2n+1)}6$",
            "板书二:指定权代入的中间式与 Chebyshev 上界",
            "结论卡:充要条件 $\\sum_iw_{n,i}^2\\to0$;$n=100$ 上界 $\\frac{67}{606}$",
        ],
        "steps": [
            "第一步:依据标注(高亮):$EX_i=\\frac12$、$\\operatorname{Var}X_i=\\operatorname{Var}U(0,1)=\\frac1{12}$、$\\sum_iw_{n,i}=1$;故 $EY_n=\\sum_iw_{n,i}EX_i=\\frac12$;$\\operatorname{Var}Y_n=\\sum_iw_{n,i}^2\\operatorname{Var}X_i=\\frac1{12}\\sum_iw_{n,i}^2$;且 $E|Y_n-\\frac12|^2=\\operatorname{Var}Y_n$($EY_n=\\frac12$)。",
            "第二步:$L^2$ 收敛判据:$Y_n\\xrightarrow{L^2}\\frac12$ 当且仅当 $E|Y_n-\\frac12|^2\\to0$,即 $\\sum_iw_{n,i}^2\\to0$。",
            "第三步:不等式链(逐项依据,关键点):$(\\max_iw_{n,i})^2\\le\\sum_iw_{n,i}^2$(最大项小于平方和);又 $w_{n,i}^2\\le w_{n,i}\\cdot\\max_iw_{n,i}$,求和得 $\\sum_iw_{n,i}^2\\le\\max_iw_{n,i}\\sum_iw_{n,i}=\\max_iw_{n,i}$;故充要条件等价于 $\\max_iw_{n,i}\\to0$。",
            "第四步:指定权代入(逐项):$w_{n,i}=\\frac{2i}{n(n+1)}$;$\\sum_iw_{n,i}^2=\\frac4{n^2(n+1)^2}\\sum_{i=1}^ni^2=\\frac4{n^2(n+1)^2}\\cdot\\frac{n(n+1)(2n+1)}6=\\frac{2(2n+1)}{3n(n+1)}$(关键点:平方和公式);方差 $=\\frac1{12}\\cdot\\frac{2(2n+1)}{3n(n+1)}=\\frac{2n+1}{18n(n+1)}$。",
            "第五步:Chebyshev(逐步):$P(|Y_n-\\frac12|\\ge\\frac1{10})\\le\\frac{\\operatorname{Var}Y_n}{(1/10)^2}=100\\cdot\\frac{2n+1}{18n(n+1)}=\\frac{50(2n+1)}{9n(n+1)}$;与 $1$ 取小得 $\\min\\{1,\\frac{50(2n+1)}{9n(n+1)}\\}$;$n=100$ 代入:$\\frac{50\\cdot201}{9\\cdot100\\cdot101}=\\frac{10050}{90900}=\\frac{67}{606}$(逐项化简,高亮)。",
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
            old_scene = rec["scene_spec"]
            if old_scene == scene or (
                    sorted(old_scene.get("objects", [])) == sorted(scene.get("objects", []))
                    and old_scene.get("steps") == scene.get("steps")):
                raise ValueError("scene unchanged: " + cid)
            expected_record_sha256 = sorted_sha(rec)
            new_rec = dict(rec)
            new_rec["scene_spec"] = scene
            for k in ("problem", "solution", "answer"):
                if new_rec[k] != rec[k]:
                    raise ValueError("math field drift: " + cid)
            new_math = {"problem": rec["problem"], "solution": rec["solution"],
                        "answer": rec["answer"], "scene_spec": scene}
            patches.append({
                "batch": entry["batch"],
                "id": cid,
                "expected_selected_path": entry["path"],
                "expected_hash_algorithm": sel["hash_algorithm"],
                "expected_selected_sha256": entry["sha256"],
                "expected_selected_raw_sha256": entry["raw_sha256"],
                "expected_record_sha256": expected_record_sha256,
                "new_math_content_sha256": sorted_sha(new_math),
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
            print(" -", p["id"], "| batch:", p["batch"])
        return 0
    except Exception as exc:
        print("[FAIL]", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
