# -*- coding: utf-8 -*-
"""Build batch-8 named scene patches (10 questions) per OPERATING_GUIDE.
Only scene_spec changes; math three fields byte-identical; every computation
independently re-derived. Scenes are inline raw strings."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "reviews/2026-10-05-training-diversity-drafts"
OUT = ROOT / "reviews/2026-10-06-scene-standard-sweep/batch8-patches.json"

NEW_SCENES = {
    "draft-c42-03": {
        "objects": [
            r"题面卡:将 $u$ 映到 $v$ 的过原点平面反射的分类",
            r"板书一:$\|u-v\|^2=2(\|u\|^2-u\cdot v)$ 与 $2(n\cdot u)n=u-v$ 的推导",
            r"高亮框:关键点——法线必平行 $u-v$ 给唯一性",
            r"板书二:$u-v=(-1,1,0)$、$\|u-v\|=\sqrt2$ 的代入",
            r"结论卡:$H=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}$(交换 $x,y$)",
        ],
        "steps": [
            r"第一步:必要性:反射保持范数,故 $\|u\|=\|v\|$ 是必要条件。",
            r"第二步:若 $u\ne v$ 且等范数,令 $n=\frac{u-v}{\|u-v\|}$;关键恒等式(逐步,高亮):$\|u-v\|^2=\|u\|^2+\|v\|^2-2u\cdot v=2(\|u\|^2-u\cdot v)$;而 $(u-v)\cdot u=\|u\|^2-u\cdot v=\frac{\|u-v\|^2}2$;故 $2(n\cdot u)n=2\cdot\frac{(u-v)\cdot u}{\|u-v\|^2}(u-v)=u-v$。",
            r"第三步:故 $H=I-2nn^{\mathsf T}$ 满足 $Hu=u-2(n\cdot u)n=u-(u-v)=v$。",
            r"第四步:唯一性(关键点):任何满足条件的反射都有 $u-v=2(n\cdot u)n$,法线必平行 $u-v$,故矩阵唯一;$u=v\ne0$ 时有无穷多种;$u\ne v$ 但范数不等则无解(高亮)。",
            r"第五步:具体计算(逐步,高亮):$u=(1,2,2)$,$v=(2,1,2)$:$u-v=(-1,1,0)$,$\|u-v\|=\sqrt{1+1}=\sqrt2$;$n=\frac{(-1,1,0)}{\sqrt2}$;$nn^{\mathsf T}=\frac12\begin{pmatrix}1&-1&0\\-1&1&0\\0&0&0\end{pmatrix}$;$H=I-2nn^{\mathsf T}=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}$,即交换 $x,y$。",
        ],
    },
    "draft-c43-01": {
        "objects": [
            r"题面卡:基 $\eta_1=(1,1)$、$\eta_2=(1,-1)$ 的对偶基",
            r"板书一:$f_1(\eta_1)=a+b=1$、$f_1(\eta_2)=a-b=0$ 的方程组",
            r"高亮框:关键点——两式相加得 $2a=1$",
            r"板书二:$f_2$ 的方程组与消元",
            r"验证板:四个配对值的代入",
        ],
        "steps": [
            r"第一步:设 $f_1(x,y)=ax+by$;条件代入:$f_1(\eta_1)=f_1(1,1)=a+b=1$;$f_1(\eta_2)=f_1(1,-1)=a-b=0$。",
            r"第二步:消元(逐步,高亮):两式相加:$2a=1$,即 $a=\frac12$;回代:$b=1-a=\frac12$;故 $f_1(x,y)=\frac{x+y}2$。",
            r"第三步:设 $f_2(x,y)=cx+dy$;条件代入:$f_2(\eta_1)=c+d=0$;$f_2(\eta_2)=c-d=1$。",
            r"第四步:消元(逐步,高亮):相加:$2c=1$,即 $c=\frac12$;回代:$d=-c=-\frac12$;故 $f_2(x,y)=\frac{x-y}2$。",
            r"第五步:验证(逐项):$f_1(\eta_1)=\frac{1+1}2=1$,$f_1(\eta_2)=\frac{1-1}2=0$;$f_2(\eta_1)=\frac{1-1}2=0$,$f_2(\eta_2)=\frac{1-(-1)}2=1$(高亮)。",
        ],
    },
    "draft-c43-02": {
        "objects": [
            r"题面卡:三个节点值的线性泛函分类",
            r"板书一:$(1,0,2)+(0,2,1)=(1,2,3)$ 的逐分量相加",
            r"高亮框:关键点——只有两个独立条件,解空间一维",
            r"板书二:$\alpha+2\gamma=2$、$2\beta+\gamma=-1$ 的移项求解",
            r"结论卡:$a=1$ 才有解;全部 $f_t=(2-2t)x-\frac{1+t}2y+tz$",
        ],
        "steps": [
            r"第一步:逐分量相加(高亮):$(1,0,2)+(0,2,1)=(1,2,3)$;线性性要求 $f(1,2,3)=f(1,0,2)+f(0,2,1)=2+(-1)=1$;故 $a\ne1$ 无解,$a=1$ 才可能有解。",
            r"第二步:设 $f(x,y,z)=\alpha x+\beta y+\gamma z$;代入条件(逐步):$f(1,0,2)=\alpha+2\gamma=2$;$f(0,2,1)=2\beta+\gamma=-1$。",
            r"第三步:只有两个独立条件,解空间一维;取 $\gamma=t$ 为自由参数(关键点,高亮);移项求解:$\alpha=2-2t$;$2\beta=-1-t$,即 $\beta=\frac{-1-t}2$。",
            r"第四步:全部解:$f_t(x,y,z)=(2-2t)x-\frac{1+t}2y+tz$,$t\in\mathbb R$。",
            r"第五步:验证(逐项代入):$f_t(1,0,2)=(2-2t)+2t=2$;$f_t(0,2,1)=2\cdot\frac{-1-t}2+t=-1$;不唯一的原因:两个独立输入只张成二维,不构成三维基(高亮)。",
        ],
    },
    "draft-c43-03": {
        "objects": [
            r"题面卡:对偶多项式 $g_0,g_1,g_2$ 与九个配对值",
            r"板书一:$G_{ij}=\int_{-1}^1x^{i+j}dx$ 的逐项计算",
            r"高亮框:关键点——$CG=I$ 的逐行×列验算",
            r"板书二:$g_0,g_1,g_2$ 的系数与表达式",
            r"验证板:九个配对值的逐项积分",
        ],
        "steps": [
            r"第一步:矩阵 $G_{ij}=\int_{-1}^1x^{i+j}dx$;逐项计算(高亮):$G_{00}=2$;$G_{01}=G_{10}=0$;$G_{02}=G_{20}=\frac23$;$G_{11}=\frac23$;$G_{12}=G_{21}=0$;$G_{22}=\frac25$;得 $G=\begin{pmatrix}2&0&\frac23\\0&\frac23&0\\\frac23&0&\frac25\end{pmatrix}$。",
            r"第二步:配对条件:$f_i(x^j)=\int_{-1}^1g_i(x)x^jdx=\delta_{ij}$;若 $g_i$ 的系数为矩阵 $C$ 的第 $i$ 行,则 $CG=I$。",
            r"第三步:解 $C=G^{-1}$ 并逐行×列验算 $CG=I$(高亮):第1行×第1列:$\frac98\cdot2+(-\frac{15}8)\cdot\frac23=\frac94-\frac54=1$;第1行×第3列:$\frac98\cdot\frac23-\frac{15}8\cdot\frac25=\frac34-\frac34=0$;第2行×第2列:$\frac32\cdot\frac23=1$;第3行×第1列:$-\frac{15}8\cdot2+\frac{45}8\cdot\frac23=0$;第3行×第3列:$-\frac{15}8\cdot\frac23+\frac{45}8\cdot\frac25=1$。",
            r"第四步:故 $g_0=\frac{9-15x^2}8$,$g_1=\frac{3x}2$,$g_2=\frac{-15+45x^2}8$。",
            r"第五步:九个配对值(逐项,高亮):$\int g_0\cdot1\,dx=\frac{9\cdot2-15\cdot\frac23}8=\frac{18-10}8=1$;$\int g_0x\,dx=0$;$\int g_0x^2dx=\frac{9\cdot\frac23-15\cdot\frac25}8=\frac{6-6}8=0$;其余六项同理,恰为 $\delta_{ij}$。",
        ],
    },
    "draft-c44-01": {
        "objects": [
            r"题面卡:块剪切 $S_B=\begin{pmatrix}I_2&B\\0&I_2\end{pmatrix}$ 何时保持 $\omega$",
            r"板书一:$JS_B$ 与 $S_B^{\mathsf T}(JS_B)$ 的分块乘法过程",
            r"高亮框:关键点——右下块 $B^{\mathsf T}-B$ 的得出",
            r"板书二:$B$ 的转置与对称性检验",
            r"结论卡:充要条件 $B$ 对称;行列式 $1$ 不能替代辛条件",
        ],
        "steps": [
            r"第一步:分块乘法(逐步,高亮):$S_B^{\mathsf T}JS_B=\begin{pmatrix}I_2&0\\B^{\mathsf T}&I_2\end{pmatrix}\begin{pmatrix}0&I_2\\-I_2&0\end{pmatrix}\begin{pmatrix}I_2&B\\0&I_2\end{pmatrix}$;先算 $JS_B=\begin{pmatrix}0&I_2\\-I_2&-B\end{pmatrix}$;再算 $S_B^{\mathsf T}(JS_B)$:左上块 $=I_2\cdot0+0\cdot(-I_2)=0$;右上块 $=I_2\cdot I_2+0\cdot(-B)=I_2$;左下块 $=B^{\mathsf T}\cdot0+I_2\cdot(-I_2)=-I_2$;右下块 $=B^{\mathsf T}\cdot I_2+I_2\cdot(-B)=B^{\mathsf T}-B$。",
            r"第二步:保持形式当且仅当 $S_B^{\mathsf T}JS_B=J$,即 $B^{\mathsf T}-B=0$,即 $B$ 对称(高亮)。",
            r"第三步:指定 $B$ 的对称性检验(逐步):$B=\begin{pmatrix}1&2\\2&-1\end{pmatrix}$,$B^{\mathsf T}=\begin{pmatrix}1&2\\2&-1\end{pmatrix}=B$;故该 $S_B$ 保持 $\omega$。",
            r"第四步:行列式:所有 $S_B$ 的 $\det S_B=1$,但不对称 $B$ 不保持形式。",
            r"第五步:结论(高亮):四维情形不能以行列式 $1$ 替代辛条件。",
        ],
    },
    "draft-c44-02": {
        "objects": [
            r"题面卡:$A=\operatorname{diag}(2,1,1,\frac12)$ 保体积但不辛",
            r"板书一:$\det A=2\cdot1\cdot1\cdot\frac12=1$",
            r"高亮框:关键点——$Ae_1=2e_1$ 与双线性给 $\omega(Ae_1,Ae_3)=2$",
            r"板书二:$Ae_4=\frac12e_4$ 给 $\omega(e_2,Ae_4)=\frac12$",
            r"结论卡:二维行列式 $1$ 足够,四维不够",
        ],
        "steps": [
            r"第一步:行列式(逐项):$\det A=2\cdot1\cdot1\cdot\frac12=1$;故 $A$ 保体积。",
            r"第二步:形式值检验(逐步,高亮):$Ae_1=2e_1$;$\omega(Ae_1,Ae_3)=\omega(2e_1,e_3)=2\omega(e_1,e_3)=2\cdot1=2$(用双线性);而 $\omega(e_1,e_3)=1$;故 $A$ 不保持辛形式。",
            r"第三步:另一配对(逐步):$Ae_4=\frac12e_4$;$\omega(e_2,Ae_4)=\omega(e_2,\frac12e_4)=\frac12\omega(e_2,e_4)=\frac12$(从 $1$ 变到 $\frac12$,高亮)。",
            r"第四步:二维对照:标准二维交替形式满足 $A^{\mathsf T}J_2A=(\det A)J_2$,故二维行列式 $1$ 足够。",
            r"第五步:结论(高亮):四维需要每对配对坐标及交叉项同时满足 $A^{\mathsf T}JA=J$;保体积不必保持辛形式。",
        ],
    },
    "draft-c44-03": {
        "objects": [
            r"题面卡:对角矩阵 $A=\operatorname{diag}(a,b,c,d)$ 的辛分类",
            r"板书一:$(A^{\mathsf T}JA)_{13}=ac$、$(A^{\mathsf T}JA)_{24}=bd$ 的分量乘法",
            r"高亮框:关键点——充要条件 $ac=bd=1$",
            r"检验板:$2\cdot\frac12=1$ 与 $2\cdot\frac12=1$",
            r"结论卡:指定矩阵为辛矩阵;仅行列式 $1$ 不足",
        ],
        "steps": [
            r"第一步:计算 $A^{\mathsf T}JA$(逐分量,高亮):$(A^{\mathsf T}JA)_{13}=a\cdot1\cdot c=ac$;$(A^{\mathsf T}JA)_{31}=-ac$;$(A^{\mathsf T}JA)_{24}=b\cdot1\cdot d=bd$;$(A^{\mathsf T}JA)_{42}=-bd$;其余为零。",
            r"第二步:保持形式当且仅当 $ac=1$ 且 $bd=1$,即 $a,b\ne0$ 且 $c=\frac1a,d=\frac1b$(高亮)。",
            r"第三步:检验指定数据(逐项):$ac=2\cdot\frac12=1$;$bd=2\cdot\frac12=1$;故该 $A$ 为辛矩阵。",
            r"第四步:行列式:条件自动给 $\det A=ac\cdot bd=1$;但仅 $\det A=1$ 不足——例如配对系数分别为 $2$ 与 $\frac12$ 时行列式仍为 $1$ 却不是辛矩阵。",
            r"第五步:结论(高亮):辛条件要求两个配对各自为 $1$,不是只看行列式。",
        ],
    },
    "draft-c44-04": {
        "objects": [
            r"题面卡:$\omega(u,v)=(u\times v)\cdot e_1$ 的交替性与退化",
            r"板书一:叉积三分量展开与点乘 $e_1$ 取第一分量",
            r"高亮框:关键点——$\omega(u,u)=u_2u_3-u_3u_2=0$",
            r"板书二:取 $v=e_3,e_2$ 解核的代入",
            r"结论卡:核 $\operatorname{span}(e_1)$,秩 $2$,退化",
        ],
        "steps": [
            r"第一步:叉积展开(逐步,高亮):$u\times v=(u_2v_3-u_3v_2,\,u_3v_1-u_1v_3,\,u_1v_2-u_2v_1)$;点乘 $e_1=(1,0,0)$ 只取第一分量:$\omega(u,v)=u_2v_3-u_3v_2$。",
            r"第二步:交替性:表达式对两变量分别线性(行列式形式);且 $\omega(u,u)=u_2u_3-u_3u_2=0$,故交替(高亮)。",
            r"第三步:核(逐步):若 $\omega(u,v)=0$ 对所有 $v$:取 $v=e_3$:$\omega(u,e_3)=u_2\cdot1-u_3\cdot0=u_2$,得 $u_2=0$;取 $v=e_2$:$\omega(u,e_2)=u_2\cdot0-u_3\cdot1=-u_3$,得 $u_3=0$。",
            r"第四步:反过来 $u_2=u_3=0$ 时对所有 $v$ 有 $\omega(u,v)=0$;故核 $=\operatorname{span}(e_1)$,秩为 $2$。",
            r"第五步:结论(高亮):形式退化,不是辛形式。",
        ],
    },
    "draft-c45-04": {
        "objects": [
            r"题面卡:条件概率存在性分类",
            r"板书一:全概率公式 $P(A)=qu+(1-q)v$",
            r"高亮框:关键点——$qu+(1-q)v$ 是 $u,v$ 的凸组合",
            r"板书二:$q=\frac{p-v}{u-v}$ 的移项求解与 $q\in(0,1)$ 验证",
            r"结论卡:指定数据不可能;区间内任意值可实现",
        ],
        "steps": [
            r"第一步:记 $u=P(A\mid B)$,$v=P(A\mid B^c)$,$q=P(B)\in(0,1)$;全概率公式:$P(A)=qu+(1-q)v$。",
            r"第二步:凸组合(关键点,高亮):$qu+(1-q)v$ 是 $u,v$ 的凸组合,权重 $q,1-q$ 均在 $(0,1)$;若 $u\ne v$,则 $P(A)$ 严格位于 $\min(u,v)$ 与 $\max(u,v)$ 之间;若 $u=v$,等于共同值。",
            r"第三步:指定数据检验:$u=\frac9{10}$,$v=\frac45$,可行区间为 $(\frac45,\frac9{10})$;而 $P(A)=\frac1{10}$ 不在其中 → 不可能。",
            r"第四步:可实现性(逐步,高亮):任何严格介于两者之间的 $p$,由 $p=qu+(1-q)v$ 移项:$q(u-v)=p-v$,即 $q=\frac{p-v}{u-v}$;验证 $q\in(0,1)$:由 $v<p<u$ 得 $p-v>0$ 且 $p-v<u-v$。",
            r"第五步:构造:取四原子概率 $qu,q(1-u),(1-q)v,(1-q)(1-v)$ 即得所需事件(高亮)。",
        ],
    },
    "draft-c46-04": {
        "objects": [
            r"题面卡:$f(x,y)=x+y$ 在单位正方形上的概率",
            r"板书一:归一化积分的逐项计算",
            r"高亮框:关键点——$P(X\le\frac12)=\int_0^{\frac12}(x+\frac12)dx=\frac38$",
            r"对照板:普通面积比 $\frac12$ 与密度加权结果 $\frac38$",
            r"结论卡:非均匀分布用密度加权面积",
        ],
        "steps": [
            r"第一步:归一化(逐项,高亮):$f\ge0$;$\int_0^1\int_0^1(x+y)\,dy\,dx=\int_0^1[xy+\frac{y^2}2]_0^1dx=\int_0^1(x+\frac12)dx=[\frac{x^2}2+\frac x2]_0^1=1$;故密度有效。",
            r"第二步:所求概率(逐项):$P(X\le\frac12)=\int_0^{\frac12}\int_0^1(x+y)\,dy\,dx=\int_0^{\frac12}(x+\frac12)\,dx$。",
            r"第三步:求值(逐步):$[\frac{x^2}2+\frac x2]_0^{\frac12}=\frac18+\frac14=\frac38$(高亮)。",
            r"第四步:对照:事件区域 $\{x\le\frac12\}$ 的普通面积为 $\frac12$,但该分布不是均匀分布,面积比 $\frac12\ne\frac38$。",
            r"第五步:结论(高亮):正确的几何表示是密度加权面积,不能直接用区域与正方形的普通面积之比。",
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
