"""Build batch-5 named scene patches (10 questions) per OPERATING_GUIDE."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "reviews/2026-10-05-training-diversity-drafts"
OUT = ROOT / "reviews/2026-10-06-scene-standard-sweep/batch5-patches.json"

NEW_SCENES = {
    "draft-c06-02": {
        "objects": [
            "坐标系:$y=|x|$ 与 $y=1$ 围成区域的阴影与交点 $\\pm1$",
            "板书:$A=2\\int_0^1(1-x)dx$ 的对称性说明",
            "原函数板:$x-\\frac{x^2}2$ 与上下限代入",
            "结论卡:$A=1$",
        ],
        "steps": [
            "第一步:求交点:$|x|=1$ 得 $x=\\pm1$;区域关于 $y$ 轴对称(高亮)。",
            "第二步:右半部分:$0\\le x\\le1$,上界 $y=1$、下界 $y=|x|=x$;故 $A=2\\int_0^1(1-x)\\,dx$。",
            "第三步:逐项求原函数:$\\int(1-x)\\,dx=x-\\frac{x^2}2$。",
            "第四步:代入上下限:$[x-\\frac{x^2}2]_0^1=(1-\\frac12)-0=\\frac12$。",
            "第五步:乘对称因子:$A=2\\times\\frac12=1$(高亮结论)。",
        ],
    },
    "draft-c19-03": {
        "objects": [
            "空间图:柱面 $x^2+y^2=1$ 与平面 $z=2x$ 的截线",
            "投影卡:消去 $z$ 得 $xy$ 平面内的单位圆周",
            "正交基板:$e_1=(0,1,0)$ 与 $e_2=\\frac{(1,0,2)}{\\sqrt5}$",
            "高亮框:关键点——点积 $\\eta=\\sin t$、$\\xi=\\sqrt5\\cos t$ 的逐项计算",
            "结论卡:平面 $z=2x$ 内半轴 $\\sqrt5$ 与 $1$ 的椭圆",
        ],
        "steps": [
            "第一步:交线为方程组 $\\begin{cases}x^2+y^2=1\\\\z=2x\\end{cases}$;投影到 $xy$ 平面:消去 $z$ 得 $x^2+y^2=1$ 且 $-1\\le x\\le1$——投影是单位圆周(高亮)。",
            "第二步:交线上每点满足 $z=2x$,位于平面 $z=2x$ 内;参数化 $(\\cos t,\\sin t,2\\cos t)$。",
            "第三步:平面内取正交基:$e_1=(0,1,0)$;$e_2=\\frac{(1,0,2)}{\\sqrt5}$(模长 $\\sqrt{1+4}=\\sqrt5$,且与 $e_1$ 正交,高亮)。",
            "第四步:逐项点积(高亮):$\\eta=(\\cos t,\\sin t,2\\cos t)\\cdot e_1=\\sin t$;$\\xi=(\\cos t,\\sin t,2\\cos t)\\cdot e_2=\\frac{\\cos t+4\\cos t}{\\sqrt5}=\\sqrt5\\cos t$。",
            "第五步:代入验证:$\\eta^2+\\frac{\\xi^2}5=\\sin^2t+\\cos^2t=1$;故交线是该平面内半轴为 $\\sqrt5$ 与 $1$ 的椭圆(高亮结论)。",
        ],
    },
    "draft-c19-04": {
        "objects": [
            "四个方程卡:$x^2+y^2+z^2=0$、$x^2+y^2=0$、$x^2+y^2=1$、系统 $\\{x^2+y^2=1,2x^2+2y^2=2\\}$",
            "维数标注图:单点/直线/柱面",
            "梯度板书:$\\nabla(x^2+y^2+z^2)=(2x,2y,2z)$ 等的逐项求导",
            "高亮框:关键点——Jacobian 两行 $(2x,2y,0)$ 与 $(4x,4y,0)$ 成比例,秩 1",
            "结论卡:维数 $0,1,2,2$;满秩正则点才可用 $3-r$",
        ],
        "steps": [
            "第一步:前三式分析(逐项):$x^2+y^2+z^2=0$:非负平方和为 $0$,仅单点 $(0,0,0)$,维数 $0$;$x^2+y^2=0$:仅 $x=y=0$,是 $z$ 轴,维数 $1$;$x^2+y^2=1$:圆柱面,维数 $2$(高亮)。",
            "第二步:第四系统:$2x^2+2y^2=2$ 是第一个方程的 $2$ 倍,两方程等价;集合仍是圆柱面,维数 $2$。",
            "第三步:梯度(逐项求导,高亮):$\\nabla(x^2+y^2+z^2)=(2x,2y,2z)$,在零集单点处 $=(0,0,0)$,退化;$\\nabla(x^2+y^2)=(2x,2y,0)$,在 $z$ 轴上 $=(0,0,0)$,退化;$\\nabla(x^2+y^2-1)=(2x,2y,0)$,在圆柱面上非零,正则。",
            "第四步:Jacobian 检查(关键点):第四系统两行 $(2x,2y,0)$ 与 $(4x,4y,0)$ 成比例,秩为 $1$;只有一个独立约束(高亮)。",
            "第五步:结论(高亮):对 $r$ 个 $C^1$ 方程,只有在某解附近 Jacobian 行满秩 $r$ 时,隐函数定理才保证局部维数 $3-r$;方程个数不能替代独立性与正则性检查。",
        ],
    },
    "draft-c19-05": {
        "objects": [
            "题面卡:平移不变 ⟺ $v\\cdot\\nabla F\\equiv0$",
            "板书一:链式法则 $\\frac d{dt}F(x+tv)=\\nabla F(x+tv)\\cdot v$ 的逐项展开",
            "板书二:$h(t)=F(x+tv)$ 与 $h'(t)=0$ 的求导",
            "高亮框:关键点——零集沿 $v$ 整条直线不变(母线)",
            "反例卡:$F=x^2+y^2$、$x^2+y^2+1$、$F=0$ 三个不含 $z$ 的例子",
        ],
        "steps": [
            "第一步:必要性(链式法则逐项,高亮):$\\frac d{dt}F(x+tv)=\\partial_1F\\cdot v_1+\\partial_2F\\cdot v_2+\\partial_3F\\cdot v_3=\\nabla F(x+tv)\\cdot v$;若对一切 $t$ 平移不变,左端恒为零;令 $t=0$ 得 $v\\cdot\\nabla F(x)=0$。",
            "第二步:充分性:固定 $x$,令 $h(t)=F(x+tv)$;则 $h'(t)=v\\cdot\\nabla F(x+tv)=0$ 处处成立(高亮求导);故 $h$ 恒定,即平移不变。",
            "第三步:零集结构:零集沿 $v$ 的整条直线不变,这些直线是母线。",
            "第四步:正则柱面条件(关键点):零集非空且在零集上 $\\nabla F\\ne0$ → 隐函数定理给局部二维正则曲面,母线为上述直线(高亮)。",
            "第五步:反例(高亮):只知道不含 $z$ 不自动保证二维曲面:$F=x^2+y^2$ 的零集仅为 $z$ 轴;$F=x^2+y^2+1$ 的零集为空;$F=0$ 的零集为全空间;必须区分平移不变集合与正则二维柱面。",
        ],
    },
    "draft-c20-03": {
        "objects": [
            "题面卡:$xy+tz^2=1$($t\\in\\mathbb R$)的分类",
            "正交替换板:$u=\\frac{x+y}{\\sqrt2}$、$v=\\frac{-x+y}{\\sqrt2}$ 的单位长与正交验证",
            "代入展开板:$u^2-v^2=2xy$ 的平方展开与相减",
            "高亮框:关键点——$t=0$ 时秩由 $3$ 降为 $2$",
            "结论卡:$t>0$ 单叶、$t<0$ 双叶、$t=0$ 双曲柱面",
        ],
        "steps": [
            "第一步:正交替换验证(逐项,高亮):两列模长:$\\frac1{(\\sqrt2)^2}+\\frac1{(\\sqrt2)^2}=1$;内积:$\\frac1{\\sqrt2}\\cdot(-\\frac1{\\sqrt2})+\\frac1{\\sqrt2}\\cdot\\frac1{\\sqrt2}=0$;故 $u,v$ 是正交坐标替换。",
            "第二步:代入展开(逐项):$u^2=\\frac{x^2+2xy+y^2}2$,$v^2=\\frac{x^2-2xy+y^2}2$;相减得 $u^2-v^2=2xy$,即 $xy=\\frac{u^2-v^2}2$;方程化为 $\\frac{u^2}2-\\frac{v^2}2+tz^2=1$(高亮)。",
            "第三步:$t>0$:正平方两项($u^2,z^2$)、负平方一项($v^2$)→ 单叶双曲面。",
            "第四步:$t<0$:正平方一项、负平方两项 → 双叶双曲面。",
            "第五步:$t=0$(关键点):方程 $\\frac{u^2}2-\\frac{v^2}2=1$ 与 $z$ 无关 → 沿 $z$ 方向的双曲柱面;二次型秩由 $3$ 降为 $2$;分类依据惯性与正右端,不凭系数符号猜测(高亮)。",
        ],
    },
    "draft-c20-04": {
        "objects": [
            "空间图:椭球与平面 $x+y+z=t$ 的截面",
            "板书一:$W^{-1}n=(1,\\frac12,\\frac13)$、$n^{\\mathsf T}W^{-1}n=\\frac{11}6$ 的逐项计算",
            "板书二:$c^{\\mathsf T}Wc=\\frac{6t^2}{11}$ 的逐项代入",
            "高亮框:关键点——切向基 $e=(1,-1,0)/\\sqrt2$、$f=(1,1,-2)/\\sqrt6$ 的限制矩阵行×列计算",
            "结论卡:阈值 $|t|=\\sqrt{\\frac{11}6}$;半轴 $\\sqrt{\\frac{1-6t^2/11}{2\\mp1/\\sqrt3}}$",
        ],
        "steps": [
            "第一步:记 $W=\\operatorname{diag}(1,2,3)$、$n=(1,1,1)$;平面上二次型的最小点为 $c=\\frac{tW^{-1}n}{n^{\\mathsf T}W^{-1}n}$。",
            "第二步:逐项计算(高亮):$W^{-1}n=(1,\\frac12,\\frac13)$;$n^{\\mathsf T}W^{-1}n=1+\\frac12+\\frac13=\\frac{11}6$;故 $c=\\frac{t}{11/6}(1,\\frac12,\\frac13)=\\frac{t}{11}(6,3,2)$。",
            "第三步:逐项代入:$c^{\\mathsf T}Wc=\\frac{t^2}{121}(36+2\\cdot9+3\\cdot4)=\\frac{t^2}{121}\\cdot66=\\frac{6t^2}{11}$(高亮)。",
            "第四步:写 $x=c+h$,$n\\cdot h=0$;交叉项 $2c^{\\mathsf T}Wh=2t\\cdot n^{\\mathsf T}h=0$ 消失;截面满足 $h^{\\mathsf T}Wh=1-\\frac{6t^2}{11}$;故 $|t|>\\sqrt{\\frac{11}6}$ 为空,等号为单点,小于时为椭圆。",
            "第五步:半轴(逐分量行×列,高亮):切向正交基 $e=(1,-1,0)/\\sqrt2$、$f=(1,1,-2)/\\sqrt6$;$e^{\\mathsf T}We=\\frac{1+2}{2}=\\frac32$;$e^{\\mathsf T}Wf=\\frac{1-2+0}{\\sqrt2\\sqrt6}=-\\frac1{2\\sqrt3}$;$f^{\\mathsf T}Wf=\\frac{1+2+12}6=\\frac52$;限制矩阵特征值为 $2\\pm\\frac1{\\sqrt3}$,半轴 $\\sqrt{\\frac{1-6t^2/11}{2\\mp1/\\sqrt3}}$。",
        ],
    },
    "draft-c23-05": {
        "objects": [
            "空间图:绕平行于 $z$ 轴的直线旋转 $90^\\circ$ 复合沿轴平移",
            "分解板书:$b_\\parallel=(0,0,3)$、$b_\\perp=(1,2,0)$ 的逐项计算",
            "消元板书:方程组 $p_1+p_2=1$、$-p_1+p_2=2$ 的求解",
            "高亮框:关键点——$(I-A)p$ 第1、2行的分量乘积验证",
            "结论卡:$p=(-\\frac12,\\frac32,0)$,螺旋运动",
        ],
        "steps": [
            "第一步:旋转轴方向 $v=(0,0,1)$;分解 $b$(逐项,高亮):$b_\\parallel=(b\\cdot v)v=3\\cdot(0,0,1)=(0,0,3)$;$b_\\perp=b-b_\\parallel=(1,2,0)$。",
            "第二步:写出 $I-A=\\begin{pmatrix}1&1&0\\\\-1&1&0\\\\0&0&0\\end{pmatrix}$;在 $v^\\perp$ 上解 $(I-A)p=b_\\perp$:即 $p_1+p_2=1$,$-p_1+p_2=2$。",
            "第三步:消元(逐步,高亮):两式相加得 $2p_2=3$,故 $p_2=\\frac32$;代回第一式:$p_1=1-\\frac32=-\\frac12$;取 $p=(-\\frac12,\\frac32,0)$。",
            "第四步:验证(逐行×列,高亮):$(I-A)p$ 第1行×列:$1\\cdot(-\\frac12)+1\\cdot\\frac32+0\\cdot0=1$;第2行×列:$(-1)\\cdot(-\\frac12)+1\\cdot\\frac32+0=2$;第3行×列:$0$;得 $(1,2,0)=b_\\perp$ ✓。",
            "第五步:结论:$T$ = 绕过 $p=(-\\frac12,\\frac32,0)$ 且平行于 $z$ 轴的直线旋转 $90^\\circ$,复合沿 $z$ 轴平移 $(0,0,3)$——一个螺旋运动(高亮)。",
        ],
    },
    "draft-c27-02": {
        "objects": [
            "矩阵卡:$A=\\begin{pmatrix}0&1&0\\\\0&0&1\\\\2&1&1\\end{pmatrix}$",
            "板书一:$|\\lambda I-A|$ 按第一行展开的余子式过程",
            "高亮框:关键点——$Av_\\lambda$ 第三分量 $2+\\lambda+\\lambda^2$ 用特征方程 $\\lambda^3=\\lambda^2+\\lambda+2$ 化简",
            "特征根板:$2$、$\\omega=\\frac{-1+i\\sqrt3}2$、$\\bar\\omega$",
            "结论卡:复域可对角化;实域不可",
        ],
        "steps": [
            "第一步:特征多项式(按第一行展开,逐步):$|\\lambda I-A|=\\begin{vmatrix}\\lambda&-1&0\\\\0&\\lambda&-1\\\\-2&-1&\\lambda-1\\end{vmatrix}=\\lambda(\\lambda(\\lambda-1)-1)-(-1)(0\\cdot(\\lambda-1)-(-1)(-2))=\\lambda(\\lambda^2-\\lambda-1)-2=\\lambda^3-\\lambda^2-\\lambda-2$(高亮余子式展开)。",
            "第二步:因式分解:验证 $\\lambda=2$ 是根($8-4-2-2=0$);除以 $\\lambda-2$ 得商 $\\lambda^2+\\lambda+1$;三根为 $2$、$\\omega=\\frac{-1+i\\sqrt3}2$、$\\bar\\omega$,互不相同。",
            "第三步:特征向量验证(逐分量,高亮):取 $v_\\lambda=(1,\\lambda,\\lambda^2)^{\\mathsf T}$;$Av_\\lambda$ 第1分量 $=\\lambda$,第2分量 $=\\lambda^2$,第3分量 $=2+\\lambda+\\lambda^2$;由特征方程 $\\lambda^3=\\lambda^2+\\lambda+2$ 得第3分量 $=\\lambda^3=\\lambda\\cdot\\lambda^2$;故 $Av_\\lambda=\\lambda v_\\lambda$。",
            "第四步:取 $P=(v_2,v_\\omega,v_{\\bar\\omega})$,则 $AP=P\\operatorname{diag}(2,\\omega,\\bar\\omega)$;三根互异 → 复域可对角化。",
            "第五步:实域判定(关键点):特征多项式有非实根 $\\omega,\\bar\\omega$;实矩阵在 $\\mathbb R$ 上对角化要求特征值全实,故实域不可对角化(高亮)。",
        ],
    },
    "draft-c27-03": {
        "objects": [
            "题面卡:$A^3=A$ 的谱投影构造",
            "板书一:$P_0=I-A^2$、$P_\\pm=\\frac{A^2\\pm A}2$ 的幂等展开",
            "高亮框:关键点——$A^4=A^2$ 的推导与两两乘积零的逐项展开",
            "作用板:$AP_0=0$、$AP_+=P_+$、$AP_-=-P_-$",
            "结论卡:可对角化;奇正幂 $A$、偶正幂 $A^2$",
        ],
        "steps": [
            "第一步:定义 $P_0=I-A^2$、$P_+=\\frac{A^2+A}2$、$P_-=\\frac{A^2-A}2$;关键恒等式:$A^3=A$,且左乘 $A$ 得 $A^4=A^2$(高亮)。",
            "第二步:幂等性(逐项展开,高亮):$P_0^2=(I-A^2)^2=I-2A^2+A^4=I-2A^2+A^2=I-A^2=P_0$;$P_+^2=\\frac{A^4+2A^3+A^2}4=\\frac{A^2+2A+A^2}4=\\frac{A^2+A}2=P_+$;$P_-^2=\\frac{A^4-2A^3+A^2}4=\\frac{A^2-2A+A^2}4=\\frac{A^2-A}2=P_-$。",
            "第三步:两两乘积与和(逐项):$P_0P_+=\\frac{(I-A^2)(A^2+A)}2=\\frac{A^2+A-A^4-A^3}2=\\frac{A^2+A-A^2-A}2=0$;$P_+P_-=\\frac{(A^2+A)(A^2-A)}4=\\frac{A^4-A^2}4=0$;同理 $P_0P_-=0$;$P_0+P_++P_-=I$(高亮)。",
            "第四步:作用(逐项):$AP_0=A-A^3=A-A=0$;$AP_+=\\frac{A^3+A^2}2=\\frac{A+A^2}2=P_+$;$AP_-=\\frac{A^3-A^2}2=\\frac{A-A^2}2=-P_-$;故全空间为三个像的直和,各像取基得对角化,零维像省略。",
            "第五步:幂(逐步,高亮):由 $A^3=A$ 左乘 $A^{m-1}$ 得 $A^{m+2}=A^{m-1}A^3=A^m$($m\\ge1$);故正奇数幂为 $A$、正偶数幂为 $A^2$;这依赖多项式恒等式与简单根结构,不是数值替换。",
        ],
    },
    "draft-c27-05": {
        "objects": [
            "题面卡:$n$ 阶矩阵在数域 $\\mathbb F$ 内有 $n$ 个互异特征值",
            "板书一:施加 $A-\\lambda_mI$ 的逐向量计算",
            "高亮框:关键点 1——$(A-\\lambda_mI)v_m=0$;关键点 2——$c_mv_m=0$ 且 $v_m\\ne0$ 推出 $c_m=0$",
            "归纳图:奠基 $m=1$ 与归纳步",
            "结论卡:$AP=P\\operatorname{diag}(\\lambda_i)$,在 $\\mathbb F$ 内可对角化",
        ],
        "steps": [
            "第一步:取互异 $\\lambda_1,\\ldots,\\lambda_n\\in\\mathbb F$ 与各自的非零特征向量 $v_i$;目标:用归纳法证明 $v_1,\\ldots,v_n$ 线性无关。",
            "第二步:归纳奠基:$m=1$:单个非零向量 $v_1$ 线性无关(高亮)。",
            "第三步:归纳步(逐步,高亮):设 $\\sum_{i=1}^mc_iv_i=0$;两端施加 $A-\\lambda_mI$:对 $i<m$,$(A-\\lambda_mI)v_i=Av_i-\\lambda_mv_i=(\\lambda_i-\\lambda_m)v_i$;而 $(A-\\lambda_mI)v_m=Av_m-\\lambda_mv_m=\\lambda_mv_m-\\lambda_mv_m=0$;得 $\\sum_{i<m}c_i(\\lambda_i-\\lambda_m)v_i=0$。",
            "第四步:由归纳假设($v_1,\\ldots,v_{m-1}$ 无关)与互异性 $\\lambda_i-\\lambda_m\\ne0$,得 $c_i=0$($i<m$);代回原式得 $c_mv_m=0$;因 $v_m\\ne0$,故 $c_m=0$(关键点,高亮)。",
            "第五步:结论:$n$ 个特征向量线性无关,构成可逆矩阵 $P$,且 $AP=P\\operatorname{diag}(\\lambda_i)$;故在 $\\mathbb F$ 内可对角化;前提是数域 $\\mathbb F$ 内有全部 $n$ 个特征值(高亮)。",
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
