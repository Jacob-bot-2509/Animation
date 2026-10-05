"""batch-01 v2 生成器:在 v1(draft.jsonl)基础上,吸收 Codex msg_442-444
复审修正,并重写 3 道与冻结评测模板重合的题。v1 原字节保留。

重写(c01-02/c36-01/c52-05)方向按 Codex 指定:
  切线/可微的分段边界、正定保持性证明与反例、概率积分变换+逆向构造。
"""
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
V1 = HERE / "draft.jsonl"
OUT = HERE / "draft-v2.jsonl"

# ---- 三题重写(整体替换) ----
REWRITES = [
{
 "id": "draft-c01-02", "category": "数学分析", "sub_category": "导数",
 "concept": "导数与切线", "concept_id": "C01",
 "parent_training_ids": ["calc-derivative-001"],
 "problem": r"设 $f(x)=\begin{cases}x^2+a, & x\leq 1\\ bx+1, & x>1\end{cases}$，其中 $a,b$ 为常数。求使 $f$ 在 $x=1$ 处连续的条件；在连续前提下，求使 $f$ 在 $x=1$ 处可微(即曲线在该点处有切线)的条件，并写出此时的切线方程；再给出一组参数，使 $f$ 在 $x=1$ 处连续但不可微，并说明曲线在该点处的几何特征。",
 "solution": r"连续性：左极限 $\lim_{x\to1^-}f(x)=1+a$，右极限 $\lim_{x\to1^+}f(x)=b+1$，连续当且仅当 $1+a=b+1$，即 $a=b$。可微性：左导数 $f'_-(1)=2x|_{x=1}=2$，右导数 $f'_+(1)=b$，可微当且仅当连续条件成立且 $b=2$，即 $a=b=2$。此时 $f(1)=1+2=3$，切线方程为 $y-3=2(x-1)$，即 $y=2x+1$。连续但不可微：取 $a=b=1$，则 $f(x)=\begin{cases}x^2+1,&x\leq1\\ x+1,&x>1\end{cases}$ 在 $x=1$ 处连续($f(1)=2$)，但左导数 $2$ 与右导数 $1$ 不相等，曲线在 $(1,2)$ 处形成角点，不存在切线。",
 "answer": r"连续当且仅当 $a=b$；可微当且仅当 $a=b=2$，此时切线为 $y=2x+1$；例如 $a=b=1$ 时连续但不可微(角点 $(1,2)$，无切线)。",
 "method": "左右极限与左右导数(可微性边界)",
 "difficulty": "基础",
 "variant_kind": "任务形式变化:隐函数切线改为分段函数可微性边界(连续→可微→切线存在三层条件+连续不可微反例)",
 "scene_spec": {
  "objects": [
   "板书:分段函数 $f(x)=\\begin{cases}x^2+a,&x\\leq1\\\\bx+1,&x>1\\end{cases}$",
   "左右极限对照:左极限 $1+a$ 与右极限 $b+1$(连续条件 $a=b$)",
   "左右导数箭头:左斜率 $2$ 与右斜率 $b$(可微条件 $b=2$)",
   "蓝色分段拼接曲线与橙色切线 $y=2x+1$(当 $a=b=2$)",
   "红色角点标记 $(1,2)$(当 $a=b=1$,左右斜率不同,无切线)"
  ],
  "steps": [
   "第一步:在黑板上写出分段函数,标出分界点 $x=1$。",
   "第二步:显示左右极限 $1+a$ 与 $b+1$,得到连续条件 $a=b$。",
   "第三步:显示左右导数 $2$ 与 $b$,在连续前提下得到可微条件 $a=b=2$。",
   "第四步:取 $a=b=2$:两段曲线在 $(1,3)$ 处光滑拼接,闪烁切点并画出橙色切线 $y=2x+1$。",
   "第五步:切换为 $a=b=1$:两段曲线在 $(1,2)$ 处形成角点,红色标记,说明左右斜率 $2$ 与 $1$ 不等,该点无切线。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v2-重写-待用户审阅",
},
{
 "id": "draft-c36-01", "category": "高等代数", "sub_category": "二次型",
 "concept": "二次型正定性", "concept_id": "C36",
 "parent_training_ids": ["linalg-060"],
 "problem": r"设 $A$ 为 $n$ 阶正定矩阵。证明 $A^{-1}$ 也是正定矩阵；并举出两个正定矩阵，其乘积不是正定矩阵的例子。",
 "solution": r"由 $A$ 正定知 $A$ 为实对称矩阵且对任意非零向量 $x$ 有 $x^{\mathsf{T}}Ax>0$；其顺序主子式全正，故 $\det A>0$，$A$ 可逆。对任意 $x\neq 0$，令 $y=A^{-1}x$，则 $y\neq 0$，且 $x^{\mathsf{T}}A^{-1}x=(Ay)^{\mathsf{T}}A^{-1}(Ay)=y^{\mathsf{T}}A^{\mathsf{T}}A^{-1}Ay$。因 $A^{\mathsf{T}}=A$ 且 $A^{-1}A=I$，得 $x^{\mathsf{T}}A^{-1}x=y^{\mathsf{T}}Ay>0$。又 $(A^{-1})^{\mathsf{T}}=(A^{\mathsf{T}})^{-1}=A^{-1}$，故 $A^{-1}$ 也是实对称矩阵。于是 $A^{-1}$ 正定。反例：取 $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$(特征值为 $1$ 与 $3$，正定)与 $B=\begin{pmatrix}1&0\\0&3\end{pmatrix}$(特征值为 $1$ 与 $3$，正定)，则 $AB=\begin{pmatrix}2&3\\1&6\end{pmatrix}$ 不是对称矩阵，故不可能正定(正定矩阵必须对称)。",
 "answer": r"证明见解法；反例：$A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$ 与 $B=\begin{pmatrix}1&0\\0&3\end{pmatrix}$ 均正定，而 $AB=\begin{pmatrix}2&3\\1&6\end{pmatrix}$ 不对称，不是正定矩阵。",
 "method": "定义法证明(正定性保持)+反例构造",
 "difficulty": "中等",
 "variant_kind": "任务升级:计算型判正定改为正定保持性证明(逆矩阵)+乘积反例(说明正定对乘法不封闭)",
 "scene_spec": {
  "objects": [
   "板书:正定的定义——实对称且 $x^{\\mathsf{T}}Ax>0$(对任意 $x\\neq0$)",
   "板书:证明链 $x^{\\mathsf{T}}A^{-1}x=y^{\\mathsf{T}}Ay>0$,其中 $y=A^{-1}x$",
   "板书:$(A^{-1})^{\\mathsf{T}}=(A^{\\mathsf{T}})^{-1}=A^{-1}$(对称性保持)",
   "绿色对勾与文本「$A^{-1}$ 正定」",
   "反例板书:$A=\\begin{pmatrix}2&1\\\\1&2\\end{pmatrix}$、$B=\\begin{pmatrix}1&0\\\\0&3\\end{pmatrix}$ 与乘积 $AB=\\begin{pmatrix}2&3\\\\1&6\\end{pmatrix}$(不对称,红色高亮)"
  ],
  "steps": [
   "第一步:写出正定的定义:实对称且对任意非零向量二次型恒正。",
   "第二步:说明 $A$ 可逆(顺序主子式全正蕴含 $\\det A>0$),令 $y=A^{-1}x$。",
   "第三步:展示证明链 $x^{\\mathsf{T}}A^{-1}x=y^{\\mathsf{T}}Ay>0$,并说明 $A^{-1}$ 实对称。",
   "第四步:绿色对勾标注结论「$A^{-1}$ 正定」。",
   "第五步:展示反例:$A$、$B$ 均正定,乘积 $AB$ 不对称,红色高亮「不对称⟹非正定」,说明正定性对乘法不封闭。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v2-重写-待用户审阅",
},
{
 "id": "draft-c52-05", "category": "概率论", "sub_category": "随机变量函数分布",
 "concept": "随机变量函数的分布", "concept_id": "C52",
 "parent_training_ids": ["prob-045"],
 "problem": r"设连续型随机变量 $X$ 的分布函数 $F(x)$ 严格递增。证明 $Y=F(X)$ 服从区间 $(0,1)$ 上的均匀分布；并说明：给定一个服从 $U(0,1)$ 的随机数 $U$，如何构造出服从密度 $f(x)=3x^2$($0<x<1$)的随机变量，并验证你的构造。",
 "solution": r"对 $0<y<1$，$F_Y(y)=P(F(X)\leq y)$。因 $F$ 严格递增且连续，存在反函数 $F^{-1}$，于是 $F_Y(y)=P(X\leq F^{-1}(y))=F(F^{-1}(y))=y$，即 $Y\sim U(0,1)$。构造：目标分布函数为 $F(x)=\int_0^x3t^2\,dt=x^3$($0<x<1$)，其反函数为 $F^{-1}(u)=u^{1/3}$。由概率积分变换的逆过程，令 $X=U^{1/3}$，则 $X$ 的分布函数为 $P(U^{1/3}\leq x)=P(U\leq x^3)=x^3=F(x)$($0<x<1$)，即 $X$ 服从密度 $f(x)=F'(x)=3x^2$。",
 "answer": r"$Y=F(X)\sim U(0,1)$(证明见解法)；构造：$X=U^{1/3}$ 服从 $f(x)=3x^2$($0<x<1$)，验证见解法。",
 "method": "概率积分变换+逆变换法",
 "difficulty": "进阶",
 "variant_kind": "结构升级:卷积改为概率积分变换定理证明与目标分布逆向构造(逆向任务)",
 "scene_spec": {
  "objects": [
   "板书:分布函数 $F$ 的图形与映射 $Y=F(X)$(值域 $(0,1)$)",
   "板书:推导 $F_Y(y)=P(F(X)\\leq y)=y$($0<y<1$)",
   "蓝色曲线 $F(x)=x^3$($0<x<1$)与其反函数 $u^{1/3}$ 的镜像示意",
   "验证链板书:$P(U^{1/3}\\leq x)=P(U\\leq x^3)=x^3$",
   "坐标图:橙色密度 $f(x)=3x^2$ 在 $(0,1)$(总面积为 $1$)"
  ],
  "steps": [
   "第一步:画出分布函数 $F$ 的图形,展示映射 $X\\mapsto F(X)$ 的值域 $(0,1)$。",
   "第二步:推导 $F_Y(y)=F(F^{-1}(y))=y$,得 $Y\\sim U(0,1)$。",
   "第三步:目标分布 $F(x)=\\int_0^x3t^2\\,dt=x^3$,展示其反函数 $u^{1/3}$。",
   "第四步:由逆变换法构造 $X=U^{1/3}$,展示验证链 $P(U^{1/3}\\leq x)=P(U\\leq x^3)=x^3$。",
   "第五步:画出橙色密度 $f(x)=3x^2$,标注积分等于 $1$,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v2-重写-待用户审阅",
},
]

# ---- 吸收修正的逐字段补丁(其余 12 题) ----
PATCHES = {
 "draft-c01-03": {
  "problem": r"已知参数曲线 $\begin{cases}x=t^2\\ y=t^3-3t\end{cases}$。求曲线在 $t=2$ 对应点处的切线方程，并求出曲线上所有水平切线与竖直切线。其中参数 $t$ 取遍实数。",
  "scene_spec": {
   "objects": [
    "带有刻度的黑色坐标轴",
    "蓝色参数曲线 $x=t^2,\\ y=t^3-3t$，自交点为 $(3,0)$",
    "黄色圆点 $(4,2)$(代表 $t=2$ 对应切点)",
    "橙色直线 $y=\\frac{9}{4}x-7$(代表切线)",
    "两条绿色水平虚线 $y=2$、$y=-2$ 与一条绿色竖直虚线 $x=0$",
    "右下角白色文本 $\\frac{dy}{dx}=\\frac{3t^2-3}{2t}$"
   ],
   "steps": [
    "第一步:动态绘制带有刻度的横纵坐标轴。",
    "第二步:绘制蓝色参数曲线,并高亮自交点 $(3,0)$(由 $t=\\pm\\sqrt{3}$ 两个参数给出)。",
    "第三步:在右下角显示参数求导公式 $\\frac{dy}{dx}=\\frac{3t^2-3}{2t}$。",
    "第四步:代入 $t=2$ 得切点 $(4,2)$ 与斜率 $\\frac{9}{4}$,闪烁黄色圆点并延伸橙色切线。",
    "第五步:依次显示水平切线($t=\\pm 1$,即 $y=\\pm 2$)与竖直切线($t=0$,即 $x=0$),用绿色虚线标注。"
   ]
  },
 },
 "draft-c01-05": {
  "solution": r"两条显式多项式曲线均无竖直切线，故可将候选切线写为 $y=mx+b$。设公切线与 $y=x^2$ 相切于点 $(a,a^2)$，切线方程为 $y=2ax-a^2$；与 $y=-x^2+2x+1$ 相切于点 $(c,-c^2+2c+1)$，切线方程为 $y=(-2c+2)x+c^2+1$。若两直线为同一直线，则比较系数得 $2a=-2c+2$ 与 $-a^2=c^2+1$。由第一式得 $a=1-c$，代入第二式得 $-(1-c)^2=c^2+1$，即 $c^2-c+1=0$，其判别式 $\Delta=(-1)^2-4=-3<0$，无实根。故满足条件的 $c$(进而 $a$)不存在，即两抛物线没有公切线。",
 },
 "draft-c36-03": {
  "solution": r"二次型对应矩阵 $A=\begin{pmatrix}1&1&0\\1&2&0\\0&0&a\end{pmatrix}$。顺序主子式：$\Delta_1=1>0$，$\Delta_2=1\times2-1\times1=1>0$，$\Delta_3=\det A=1\times(2a-0)-1\times(a-0)+0=a$。正定当且仅当三个顺序主子式全为正，故 $a>0$。当 $a=0$ 时，$f=x^2+2xy+2y^2=(x+y)^2+y^2\geq 0$，且 $f(0,0,1)=0$，存在非零解，故半正定但非正定。当 $a<0$ 时，取 $(x,y,z)=(0,0,1)$ 得 $f(0,0,1)=a<0$，同时取 $(1,0,0)$ 得 $f(1,0,0)=1>0$，既有正值又有负值，故二次型不定。",
  "scene_spec": {
   "objects": [
    "板书:二次型 $f=x^2+2xy+2y^2+az^2$ 与其矩阵 $A=\\begin{pmatrix}1&1&0\\\\1&2&0\\\\0&0&a\\end{pmatrix}$",
    "三个高亮框:顺序主子式 $\\Delta_1=1$、$\\Delta_2=1$、$\\Delta_3=a$",
    "数轴:原点处边界点 $a=0$,三个区间标注「正定」「半正定」「不定」",
    "板书:$a=0$ 时配方 $(x+y)^2+y^2$ 与零解 $(0,0,1)$",
    "板书:$a<0$ 时代入 $(0,0,1)$ 与 $(1,0,0)$ 得负值 $a$ 与正值 $1$"
   ],
   "steps": [
    "第一步:写出二次型对应的矩阵 $A$。",
    "第二步:依次计算顺序主子式 $\\Delta_1=1$、$\\Delta_2=1$、$\\Delta_3=a$,高亮显示。",
    "第三步:由全正条件得 $a>0$,在数轴上标出正定区间。",
    "第四步:讨论边界 $a=0$:配方得 $(x+y)^2+y^2\\geq0$,且 $(0,0,1)$ 为非零零解,半正定非正定。",
    "第五步:$a<0$ 时分别代入 $(0,0,1)$ 与 $(1,0,0)$ 得负值 $a$ 与正值 $1$,确认不定;汇总各分支。"
   ]
  },
 },
 "draft-c52-01": {
  "method": "单调变换密度公式+归一化验证",
 },
 "draft-c52-03": {
  "solution": r"$X$ 的密度为 $\frac{1}{3}$($-1<x<2$)。$Y=X^2$ 的值域为 $[0,4)$。当 $0<y<1$ 时，$[-\sqrt{y},\sqrt{y}]\subset(-1,2)$，故 $F_Y(y)=P(X^2\leq y)=\frac{2\sqrt{y}}{3}$，$f_Y(y)=\frac{1}{3\sqrt{y}}$。当 $1\leq y<4$ 时，区间 $[-\sqrt{y},\sqrt{y}]$ 与支持集 $(-1,2)$ 的交为 $(-1,\sqrt{y}]$，故 $F_Y(y)=\frac{\sqrt{y}+1}{3}$，$f_Y(y)=\frac{1}{6\sqrt{y}}$。分界点为 $y=1$，两侧密度在该点有跳跃。验证总质量：$\int_0^1\frac{1}{3\sqrt{y}}\,dy+\int_1^4\frac{1}{6\sqrt{y}}\,dy=\frac{2}{3}+\frac{1}{3}=1$。完整 CDF 在 $y\leq0$ 时为 $0$，在 $y\geq4$ 时为 $1$；$y=1$ 处 CDF 连续但左右导数不同；密度在单个点 $y=1$ 可任取有限非负值，这不产生概率原子。",
  "scene_spec": {
   "objects": [
    "坐标图:蓝色矩形密度 $f_X(x)=\\frac{1}{3}$ 在 $(-1,2)$",
    "动画:区间 $[-\\sqrt{y},\\sqrt{y}]$ 随 $y$ 增长,左端越过 $-1$ 的时刻高亮",
    "坐标图:橙色分段密度曲线,在 $y=1$ 处显示跳跃",
    "板书:两段公式 $\\frac{1}{3\\sqrt{y}}$ 与 $\\frac{1}{6\\sqrt{y}}$",
    "板书:总质量验证 $\\frac{2}{3}+\\frac{1}{3}=1$"
   ],
   "steps": [
    "第一步:绘制蓝色矩形密度 $f_X(x)=\\frac{1}{3}$,$x\\in(-1,2)$。",
    "第二步:当 $0<y<1$ 时,展示 $[-\\sqrt{y},\\sqrt{y}]$ 完全落入支持集,$F_Y=\\frac{2\\sqrt{y}}{3}$,求导得 $f_Y=\\frac{1}{3\\sqrt{y}}$。",
    "第三步:$1\\leq y<4$ 时,交区间为 $(-1,\\sqrt{y}]$,其长度为 $\\sqrt{y}+1$,故 $F_Y(y)=\\frac{\\sqrt{y}+1}{3}$。",
    "第四步:在 $1<y<4$ 内求导得第二段密度;展示 $y=1$ 两侧密度变化与 CDF 连续,标出 $P(Y=1)=0$。",
    "第五步:展示总质量验证 $\\frac{2}{3}+\\frac{1}{3}=1$,并汇总分段结果。"
   ]
  },
 },
 "draft-c52-04": {
  "answer": r"$F_Y(y)=0\ (y\leq0)$；$F_Y(y)=\frac{y}{2}\ (0<y<1)$；$F_Y(y)=1\ (y\geq1)$。密度:连续部分 $\frac{1}{2}$($0<y<1$)加原子质量 $\frac{1}{2}$ 于 $y=1$。$E[Y]=\frac{3}{4}$。整体没有通常的概率密度函数；分布由上述连续部分和质量 $\frac12$ 的原子组成。",
  "scene_spec": {
   "objects": [
    "坐标图:蓝色矩形密度 $f_X(x)=\\frac{1}{2}$ 在 $(0,2)$ 与函数 $\\min(x,1)$ 的折线图",
    "连续密度图:$(0,1)$ 内高度 $\\frac12$;另用独立红色质量箭头标出 $P(Y=1)=\\frac12$",
    "板书:期望计算 $\\int_0^1\\frac{y}{2}\\,dy+1\\cdot\\frac{1}{2}=\\frac{3}{4}$",
    "板书:第二算法 $\\frac{1}{2}(\\frac{1}{2}+1)=\\frac{3}{4}$",
    "右下角标签「连续+原子混合」"
   ],
   "steps": [
    "第一步:绘制 $X$ 的均匀密度与 $\\min(x,1)$ 的折线图。",
    "第二步:分段求分布函数:$F_Y(y)=\\frac{y}{2}$($0<y<1$)、$F_Y(y)=1$($y\\geq1$)。",
    "第三步:标出连续部分密度,并单独用质量箭头展示 CDF 在 $1$ 处跳跃 $\\frac12$,说明整体为混合分布。",
    "第四步:展示期望计算 $\\frac{1}{4}+\\frac{1}{2}=\\frac{3}{4}$。",
    "第五步:展示经 $X$ 直接积分的第二算法,两法结果一致,汇总结论。"
   ]
  },
 },
}

def apply_patch(row: dict, patch: dict) -> dict:
    out = dict(row)
    for k, v in patch.items():
        if k == "scene_spec":
            spec = dict(row["scene_spec"])
            for sk, sv in v.items():
                spec[sk] = sv
            out["scene_spec"] = spec
        else:
            out[k] = v
    return out


def main() -> int:
    v1 = [json.loads(l) for l in V1.read_text(encoding="utf-8").splitlines()
          if l.strip()]
    by_id = {r["id"]: r for r in v1}
    for rw in REWRITES:
        assert rw["id"] in by_id, f"重写 id 不在 v1: {rw['id']}"
        by_id[rw["id"]] = rw
    for pid, patch in PATCHES.items():
        assert pid in by_id, f"补丁 id 不在 v1: {pid}"
        by_id[pid] = apply_patch(by_id[pid], patch)
    rows = [by_id[r["id"]] for r in v1]  # 保持 v1 顺序
    OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False,
                                        separators=(",", ":")) for r in rows)
                   + "\n", encoding="utf-8", newline="\n")
    print(f"写入 {len(rows)} 行 -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
