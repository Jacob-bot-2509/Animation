# -*- coding: utf-8 -*-
"""Build batch-7 named scene patches (10 questions) per OPERATING_GUIDE.
Only scene_spec changes; math three fields byte-identical; every computation
independently re-derived. Scenes are inline raw strings."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "reviews/2026-10-05-training-diversity-drafts"
OUT = ROOT / "reviews/2026-10-06-scene-standard-sweep/batch7-patches.json"

NEW_SCENES = {
    "draft-c34-05": {
        "objects": [
            r"题面卡:$E_{ij}(a)=I+ae_{ij}$ 的四因子复合与逆",
            r"板书一:乘法规则 $e_{ij}e_{kl}=\delta_{jk}e_{il}$ 与关键事实 $e_{12}e_{23}=e_{13}$、$e_{23}e_{12}=0$",
            r"高亮框:关键点——$e_{13}$ 项经 $e_{12}e_{23}$ 积累系数 $ab$",
            r"板书二:逆公式 $(I+ae_{ij})(I-ae_{ij})=I$ 的展开验证",
            r"验证卡:$a=\frac23,b=\frac34$ 代入得 $ab=\frac12$",
        ],
        "steps": [
            r"第一步:乘法规则(高亮):$e_{ij}e_{kl}=\delta_{jk}e_{il}$;关键事实:$e_{12}e_{23}=e_{13}$ 而 $e_{23}e_{12}=0$;各相关平方为零:$e_{12}^2=e_{23}^2=e_{13}^2=0$。",
            r"第二步:逐因子相乘(逐步,高亮):$(I+ae_{12})(I+be_{23})=I+ae_{12}+be_{23}+abe_{13}$;再乘 $(I-ae_{12})$:结果 $=I+ae_{12}+be_{23}+abe_{13}-ae_{12}-a^2e_{12}^2-abe_{12}e_{23}-a^2be_{13}e_{12}=I+be_{23}+abe_{13}$(用 $e_{12}^2=0$、$e_{13}e_{12}=0$ 消去)。",
            r"第三步:再乘 $(I-be_{23})$:$(I+be_{23}+abe_{13})(I-be_{23})=I+be_{23}+abe_{13}-be_{23}-b^2e_{23}^2-ab^2e_{13}e_{23}=I+abe_{13}$;故复合 $=E_{13}(ab)$(关键点:$e_{13}$ 项经 $e_{12}e_{23}=e_{13}$ 积累系数 $ab$,高亮)。",
            r"第四步:逆公式验证(逐项):$(I+ae_{ij})(I-ae_{ij})=I+ae_{ij}-ae_{ij}-a^2e_{ij}^2=I$(因 $e_{ij}^2=0$);故 $E_{ij}(a)^{-1}=E_{ij}(-a)$,最终逆为 $E_{13}(-ab)$。",
            r"第五步:代入验证(逐步):$a=\frac23,b=\frac34$:$ab=\frac23\cdot\frac34=\frac12$;复合为 $E_{13}(\frac12)=I+\frac12e_{13}$,$(1,3)$ 元为 $\frac12$(高亮结论)。",
        ],
    },
    "draft-c35-02": {
        "objects": [
            r"题面卡:$f=(x_1-x_2)^2+2(x_2-x_3)^2+3(x_3-x_4)^2$ 的替换与惯性",
            r"板书一:替换 $u_1=x_1-x_2$ 等与反解的逐步代入",
            r"高亮框:关键点——上三角反解保证替换可逆",
            r"板书二:标准形与伸缩 $v_2=\sqrt2u_2$、$v_3=\sqrt3u_3$",
            r"限制卡:$V=\{x:x_4=0\}$ 上逐项归零得正定",
        ],
        "steps": [
            r"第一步:作替换:$u_1=x_1-x_2$,$u_2=x_2-x_3$,$u_3=x_3-x_4$,$w=x_4$。",
            r"第二步:反解(逐步代入,高亮):$x_4=w$;$x_3=u_3+x_4=u_3+w$;$x_2=u_2+x_3=u_2+u_3+w$;$x_1=u_1+x_2=u_1+u_2+u_3+w$;上三角结构保证替换可逆。",
            r"第三步:标准形:$f=u_1^2+2u_2^2+3u_3^2+0w^2$;再伸缩(逐项):$v_1=u_1$,$v_2=\sqrt2u_2$(因 $(\sqrt2u_2)^2=2u_2^2$),$v_3=\sqrt3u_3$;得规范形 $v_1^2+v_2^2+v_3^2+0w^2$。",
            r"第四步:全空间结论:秩为 $3$,惯性为 $(3,0,1)$(3 正、0 负、1 零,高亮)。",
            r"第五步:限制在 $V=\{x:x_4=0\}$:此时 $u_3=x_3$;$f|_V=(x_1-x_2)^2+2(x_2-x_3)^2+3x_3^2$;若其为零,逐项得 $x_3=0$、$x_2=0$、$x_1=0$;故限制后为正定型(高亮)。",
        ],
    },
    "draft-c35-05": {
        "objects": [
            r"题面卡:$f=x^2+2y^2+3z^2+2xy$ 与 $g=2x^2+3y^2+4z^2$ 的合同判定",
            r"板书一:配方 $f=(x+y)^2+y^2+3z^2$ 与 $g=(\sqrt2x)^2+(\sqrt3y)^2+(2z)^2$",
            r"高亮框:关键点——惯性指数同为 $(3,0,0)$,由惯性定理合同",
            r"行×列计算板:$C=M_f^{-1}M_g$ 与 $C^{\mathsf T}AC=B$ 的逐项验证",
            r"结论卡:$C=\begin{pmatrix}\sqrt2&-\sqrt3&0\\0&\sqrt3&0\\0&0&\frac2{\sqrt3}\end{pmatrix}$",
        ],
        "steps": [
            r"第一步:配方(逐步,高亮):$f=x^2+2xy+2y^2+3z^2=(x+y)^2+y^2+3z^2$,正惯性指数 $3$,正定;$g=(\sqrt2x)^2+(\sqrt3y)^2+(2z)^2$,正惯性指数 $3$,正定。",
            r"第二步:由惯性定理,两者惯性指数同为 $(3,0,0)$,故合同(都与 $I_3$ 合同,由合同关系的传递性,高亮)。",
            r"第三步:构造(逐项):由配方取 $M_f=\begin{pmatrix}1&1&0\\0&1&0\\0&0&\sqrt3\end{pmatrix}$($M_fx=(x+y,y,\sqrt3z)$),则 $A=M_f^{\mathsf T}M_f$;$M_g=\operatorname{diag}(\sqrt2,\sqrt3,2)$,则 $B=M_g^{\mathsf T}M_g$。",
            r"第四步:计算 $C=M_f^{-1}M_g$(逐行×列,高亮):$M_f^{-1}=\begin{pmatrix}1&-1&0\\0&1&0\\0&0&\frac1{\sqrt3}\end{pmatrix}$;第1行×第1列:$1\cdot\sqrt2+(-1)\cdot0+0=\sqrt2$;第1行×第2列:$1\cdot0+(-1)\cdot\sqrt3+0=-\sqrt3$;第1行×第3列:$0$;第2行:$0,\sqrt3,0$;第3行:$0,0,\frac2{\sqrt3}$。",
            r"第五步:验证 $C^{\mathsf T}AC=B$(逐项行×列,高亮):先算 $AC$:第1行×第1列 $=\sqrt2$、第1行×第2列 $=0$、第2行×第2列 $=-\sqrt3+2\sqrt3=\sqrt3$、第3行×第3列 $=3\cdot\frac2{\sqrt3}=2\sqrt3$;再算 $C^{\mathsf T}(AC)$:对角依次为 $\sqrt2\cdot\sqrt2=2$、$\sqrt3\cdot\sqrt3=3$、$\frac2{\sqrt3}\cdot2\sqrt3=4$,非对角为零;得 $\operatorname{diag}(2,3,4)=B$ ✓。",
        ],
    },
    "draft-c38-01": {
        "objects": [
            r"题面卡:$U=\{(a,Ma)\}$、$V=\{(0,b)\}$ 的直和与投影",
            r"板书一:分解 $(a,b)=(a,Ma)+(0,b-Ma)$ 的逐项验证",
            r"高亮框:关键点——交为零来自第一坐标唯一性",
            r"板书二:$P^2=P$ 的两次作用代入与核像求解",
            r"结论卡:$\mathbb R^4=U\oplus V$,核 $V$、像 $U$,维数均 $2$",
        ],
        "steps": [
            r"第一步:和为全空间(逐项,高亮):任意 $(a,b)=(a,Ma)+(0,b-Ma)$;第一项 $(a,Ma)$ 属 $U$,第二项 $(0,b-Ma)$ 属 $V$。",
            r"第二步:交为零:若 $(a,Ma)=(0,b)$,第一坐标给 $a=0$,于是 $Ma=0$,再由第二坐标给 $b=0$;故交为 $\{0\}$,分解唯一。",
            r"第三步:投影 $P(a,b)=(a,Ma)$;两次作用(逐步,高亮):$P(P(a,b))=P(a,Ma)=(a,Ma)=P(a,b)$,故 $P^2=P$。",
            r"第四步:核(逐步):$P(a,b)=(0,0)$ 当且仅当 $a=0$(第一坐标),$b$ 任意;故 $\ker P=V$;像:$P$ 的值域即 $\{(a,Ma)\}=U$。",
            r"第五步:维数:$\dim U=\dim V=2$;不需要 $M$ 可逆——图空间与竖直空间互补来自第一坐标的唯一性(高亮)。",
        ],
    },
    "draft-c38-02": {
        "objects": [
            r"题面卡:$U$ 偶多项式与 $V$ 被 $(x-1)^2$ 整除的空间",
            r"板书一:$f(1)=a+b+c=0$ 与 $f'(1)=2b+4c=0$ 的代入",
            r"高亮框:关键点——求导代入 $f'=2bx+4cx^3$ 在 $x=1$",
            r"消元板:$b=-2c$、$a=c$ 与展开 $c(x^2-1)^2$",
            r"结论卡:交维数 $1$,和 $=$ 全空间,非直和",
        ],
        "steps": [
            r"第一步:基底:$U=\operatorname{span}(1,x^2,x^4)$,维数 $3$;$V=(x-1)^2\mathbb R[x]_{\le2}$,维数 $3$。",
            r"第二步:交的方程:设 $f=a+bx^2+cx^4\in V$;须 $f(1)=0$:$a+b+c=0$;且 $f'(1)=0$(逐步求导,高亮):$f'=2bx+4cx^3$,代入 $x=1$ 得 $2b+4c=0$。",
            r"第三步:消元(逐步,高亮):$2b+4c=0$ 给 $b=-2c$;代入 $a+b+c=0$:$a-2c+c=0$ 给 $a=c$;故 $f=c-2cx^2+cx^4=c(1-2x^2+x^4)=c(x^2-1)^2$。",
            r"第四步:故 $U\cap V=\operatorname{span}((x^2-1)^2)$,维数 $1$。",
            r"第五步:和:$3+3-1=5$,等于环境维数,故 $U+V=\mathbb R[x]_{\le4}$;交非零 → 不是直和(高亮)。",
        ],
    },
    "draft-c39-01": {
        "objects": [
            r"题面卡:$T(X)=AX-XA$,$A=\operatorname{diag}(1,3)$",
            r"板书一:$AX$ 与 $XA$ 的逐项乘法与相减",
            r"高亮框:关键点——$T(X)=\begin{pmatrix}0&-2b\\2c&0\end{pmatrix}$ 的得出",
            r"板书二:$T^2$ 在像上的逐项计算",
            r"结论卡:核=对角矩阵、像=零对角矩阵,直和,非正交投影",
        ],
        "steps": [
            r"第一步:逐项乘法(高亮):$AX=\operatorname{diag}(1,3)X=\begin{pmatrix}a&b\\3c&3d\end{pmatrix}$;$XA=\begin{pmatrix}a&3b\\c&3d\end{pmatrix}$;相减得 $T(X)=\begin{pmatrix}0&-2b\\2c&0\end{pmatrix}$。",
            r"第二步:核:$T(X)=0$ 当且仅当 $b=c=0$,即 $X$ 为对角矩阵;基 $e_{11},e_{22}$,维数 $2$。",
            r"第三步:像:零对角矩阵全体,基 $e_{12},e_{21}$,维数 $2$,故秩 $2$。",
            r"第四步:直和:每个矩阵唯一分解为对角部分加零对角部分,交为零;故 $M_2(\mathbb R)=\ker T\oplus\operatorname{im}T$(高亮)。",
            r"第五步:$T^2$ 在像上(逐步,高亮):$T(\begin{pmatrix}0&-2b\\2c&0\end{pmatrix})=\begin{pmatrix}0&2\cdot2b\\2\cdot2c&0\end{pmatrix}=\begin{pmatrix}0&4b\\4c&0\end{pmatrix}$;即 $T^2|_{\operatorname{im}T}=4I$;而在核上 $T=0$;分解非正交,不能把 $T$ 说成正交投影。",
        ],
    },
    "draft-c39-03": {
        "objects": [
            r"题面卡:$T:\mathbb R[x]_{\le3}\to\mathbb R^3$,$Tf=(f(0),f(1),f(-1))$",
            r"板书一:因子定理——三节点为零 $\Rightarrow$ 被 $x(x-1)(x+1)$ 整除",
            r"高亮框:关键点——右逆 $R$ 的逐点代入验证",
            r"验证板:$x=0,1,-1$ 三处取值 $a,b,c$",
            r"结论卡:核 $\operatorname{span}(x^3-x)$,像 $\mathbb R^3$,秩 $3$",
        ],
        "steps": [
            r"第一步:核(关键点:因子定理,高亮):$f\in\ker T$ 当且仅当 $f$ 在 $0,1,-1$ 三点为零;由因子定理 $f$ 被 $x(x-1)(x+1)$ 整除;次数≤3 → $f=c\,x(x-1)(x+1)=c(x^3-x)$;故 $\ker T=\operatorname{span}(x^3-x)$,维数 $1$。",
            r"第二步:构造右逆:$R(a,b,c)=a(1-x^2)+b\frac{x(x+1)}2+c\frac{x(x-1)}2$。",
            r"第三步:逐点代入验证(高亮):$x=0$:$R=a(1-0)+0+0=a$;$x=1$:$R=0+b\cdot\frac{1\cdot2}2+0=b$;$x=-1$:$R=0+0+c\cdot\frac{(-1)(-2)}2=c$。",
            r"第四步:故 $TR=I_{\mathbb R^3}$,像为全部 $\mathbb R^3$,秩 $3$;与核维数 $4-3=1$ 一致。",
            r"第五步:结论:显式右逆证明满射,不依赖仅报维数(高亮)。",
        ],
    },
    "draft-c40-01": {
        "objects": [
            r"题面卡:$A(\lambda)=\operatorname{diag}(f,f^2)$ 与 $B(\lambda)=\operatorname{diag}(1,f^3)$,$f=\lambda-1$",
            r"板书一:一阶子式集合 $\{f,f^2\}$ 与 $\{1,f^3\}$ 的首一 gcd",
            r"高亮框:关键点——不变因子 $(f,f^2)$ 与 $(1,f^3)$ 不同,不等价",
            r"板书二:$a\ne1$ 与 $a=1$ 代入的秩核对照",
            r"结论卡:$a=1$ 时秩分别 $0,1$;行列式相同不足以确定核",
        ],
        "steps": [
            r"第一步:一阶子式(逐项,高亮):$A$ 的一阶子式集合为 $\{f,f^2\}$,首一 gcd $=f$;$B$ 的一阶子式集合为 $\{1,f^3\}$,首一 gcd $=1$。",
            r"第二步:不变因子:$A$:$d_1=f$,$d_2=f^3/f=f^2$,即 $(f,f^2)$;$B$:$d_1=1$,$d_2=f^3$,即 $(1,f^3)$;不同 → 不多项式可逆等价(行列式同为 $f^3$ 但不变因子不同,高亮)。",
            r"第三步:有理函数域 $\mathbb R(\lambda)$:$f=\lambda-1\ne0$ 是可逆元,两矩阵秩 $2$、核零;多项式环中核也零(环无零因子)。",
            r"第四步:代入(逐项):$a\ne1$ 时两者仍秩 $2$、核零;$a=1$ 时 $A(1)=\operatorname{diag}(0,0)=0$,秩 $0$、核 $\mathbb R^2$;$B(1)=\operatorname{diag}(1,0)$;解 $B(1)v=0$:第一分量 $v_1=0$、$v_2$ 自由,故 $\ker B(1)=\operatorname{span}(e_2)$,秩 $1$(高亮)。",
            r"第五步:结论:行列式相同不足以确定特殊参数下的核与秩(高亮)。",
        ],
    },
    "draft-c40-04": {
        "objects": [
            r"题面卡:$A(\lambda)=\operatorname{diag}(\lambda+1,\lambda(\lambda+1),(\lambda+1)^2(\lambda-2))$ 的因子",
            r"板书一:$D_1$ 取最小指数的逐项 gcd",
            r"板书二:二阶子式(两两乘积)与 $D_2$ 的取最小指数",
            r"高亮框:关键点——$D_3$ 的对角元连乘展开",
            r"结论卡:$D_1=\lambda+1$,$D_2=(\lambda+1)^2$,$D_3=\lambda(\lambda+1)^4(\lambda-2)$",
        ],
        "steps": [
            r"第一步:一阶行列式因子(逐项 gcd,高亮):各对角元 $\lambda+1$、$\lambda(\lambda+1)$、$(\lambda+1)^2(\lambda-2)$;对每个根取最小指数:$D_1=\lambda+1$。",
            r"第二步:二阶子式(对角情形即两两乘积):$\lambda(\lambda+1)^2$、$(\lambda+1)^3(\lambda-2)$、$\lambda(\lambda+1)^3(\lambda-2)$;逐项取最小指数:$D_2=(\lambda+1)^2$(高亮)。",
            r"第三步:三阶:$D_3=\det A=(\lambda+1)\cdot\lambda(\lambda+1)\cdot(\lambda+1)^2(\lambda-2)=\lambda(\lambda+1)^4(\lambda-2)$(逐步连乘,高亮)。",
            r"第四步:不变因子(逐步比值):$d_1=D_1=\lambda+1$;$d_2=D_2/D_1=\lambda+1$;$d_3=D_3/D_2=\lambda(\lambda+1)^2(\lambda-2)$。",
            r"第五步:初等因子:把各不变因子分解为互异根幂:$\lambda+1$、$\lambda+1$、$\lambda$、$(\lambda+1)^2$、$\lambda-2$(高亮结论)。",
        ],
    },
    "draft-c42-02": {
        "objects": [
            r"矩阵卡:$R_x=\begin{pmatrix}1&0&0\\0&0&-1\\0&1&0\end{pmatrix}$、$R_y=\begin{pmatrix}0&0&1\\0&1&0\\-1&0&0\end{pmatrix}$",
            r"行×列计算板:$R_xR_y$ 与 $R_yR_x$ 的九项分量乘积",
            r"高亮框:关键点——迹 $0$ 与 $\operatorname{tr}R=1+2\cos\theta$ 给 $\theta=\frac{2\pi}3$",
            r"固定向量板:解 $(R-I)x=0$ 得轴方向",
            r"结论卡:两乘积不同,轴 $(1,1,1)$ 与 $(1,1,-1)$,角均 $\frac{2\pi}3$",
        ],
        "steps": [
            r"第一步:计算 $R_xR_y$(逐行×列,高亮):第1行×第1列:$1\cdot0+0\cdot0+0\cdot(-1)=0$;第1行×第2列:$0$;第1行×第3列:$1\cdot1=1$;第2行×第1列:$0+0+(-1)(-1)=1$;第2行×第2列:$0$;第2行×第3列:$0$;第3行×第1列:$0$;第3行×第2列:$1\cdot1=1$;第3行×第3列:$0$;得 $R_xR_y=\begin{pmatrix}0&0&1\\1&0&0\\0&1&0\end{pmatrix}$。",
            r"第二步:计算 $R_yR_x$(逐行×列,高亮):第1行×第1列:$0$;第1行×第2列:$1\cdot1=1$;第1行×第3列:$0$;第2行×第1列:$0$;第2行×第2列:$0$;第2行×第3列:$1\cdot(-1)=-1$;第3行×第1列:$(-1)\cdot1=-1$;第3行×第2列:$0$;第3行×第3列:$0$;得 $R_yR_x=\begin{pmatrix}0&1&0\\0&0&-1\\-1&0&0\end{pmatrix}$。",
            r"第三步:两乘积不同(高亮);两者均正交、行列式 $1$、迹 $0$;由 $\operatorname{tr}R=1+2\cos\theta$:$\cos\theta=-\frac12$,即 $\theta=\frac{2\pi}3$。",
            r"第四步:求固定向量(逐步,高亮):解 $(R_xR_y-I)x=0$:$\begin{pmatrix}-1&0&1\\1&-1&0\\0&1&-1\end{pmatrix}x=0$ 给 $x_1=x_3,x_2=x_3$,固定向量方向 $(1,1,1)$;同理 $(R_yR_x-I)x=0$ 给 $(1,1,-1)$。",
            r"第五步:结论:轴分别为 $(1,1,1)/\sqrt3$ 与 $(1,1,-1)/\sqrt3$,右手角均为 $\frac{2\pi}3$;三维不同轴旋转不交换(高亮)。",
        ],
    },
}


def sorted_sha(obj) -> str:
    return hashlib.sha256(
        json.dumps(obj, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def main() -> int:
    try:
        control = set(chr(c) for c in range(0, 32)) - {"\t"}
        for cid, scene in NEW_SCENES.items():
            for s in scene["objects"] + scene["steps"]:
                if any(ch in control for ch in s):
                    raise ValueError("control char in " + cid)
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
