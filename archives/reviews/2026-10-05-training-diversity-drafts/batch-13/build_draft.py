"""batch-13 生成器:三个单条考点各 5 题
(C27 谱分解与对角化 / C29 多项式因式分解与根 / C32 线性方程组解空间)。
全部数学结论由作者逐题手工验算(见 DRAFT_REPORT.md 核算说明);
起草过程未读 eval/test 题文或答案作提示;凡有理数一律分数。
注:C27 父题 linalg-049/068 属已知谱分解风险区([[u,v],[v,u]] 模板),
本组刻意避开对称 2x2 谱分解,走 3x3 与非对称路径。
"""
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "draft.jsonl"

DATA = [
# ===================== C27 谱分解与对角化 =====================
{
 "id": "draft-c27-01", "category": "高等代数", "sub_category": "矩阵对角化",
 "concept": "谱分解与对角化", "concept_id": "C27",
 "parent_training_ids": ["linalg-049", "linalg-064", "linalg-068"],
 "problem": r"判断矩阵 $A=\begin{pmatrix}2&1&0\\0&2&1\\0&0&3\end{pmatrix}$ 是否可对角化，并说明理由。",
 "solution": r"$A$ 为上三角矩阵,特征值为对角线元素:$2,2,3$(特征多项式 $(2-\lambda)^2(3-\lambda)$)。特征值 $2$ 的代数重数为 $2$,求其几何重数:解 $(A-2I)v=0$,即 $\begin{pmatrix}0&1&0\\0&0&1\\0&0&1\end{pmatrix}v=0$,得 $v_2=0,v_3=0$,特征子空间为 $\mathrm{span}\{(1,0,0)\}$,维数为 $1$。几何重数 $1<$ 代数重数 $2$,故 $A$ 不可对角化。",
 "answer": r"不可对角化:特征值 $2$ 的几何重数 $1$ 小于代数重数 $2$。",
 "method": "代数重数与几何重数比较",
 "difficulty": "基础",
 "variant_kind": "重根不可对角化:三重三角矩阵的重根几何重数判定",
 "scene_spec": {
  "objects": [
   "板书:矩阵 $A$ 与特征多项式 $(2-\\lambda)^2(3-\\lambda)$",
   "板书:$(A-2I)v=0$ 的求解与特征子空间",
   "高亮框:「几何重数 1 < 代数重数 2」",
   "红色标签「不可对角化」",
   "标签「上三角矩阵特征值即对角元」"
  ],
  "steps": [
   "第一步:读出特征值与代数重数。",
   "第二步:解特征方程组求特征子空间。",
   "第三步:高亮几何重数与代数重数的比较。",
   "第四步:判定不可对角化。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c27-02", "category": "高等代数", "sub_category": "矩阵对角化",
 "concept": "谱分解与对角化", "concept_id": "C27",
 "parent_training_ids": ["linalg-049", "linalg-064", "linalg-068"],
 "problem": r"判断矩阵 $A=\begin{pmatrix}1&0&1\\0&2&0\\1&0&1\end{pmatrix}$ 是否可对角化；若可对角化，写出对角矩阵 $D$ 与可逆矩阵 $P$ 使 $P^{-1}AP=D$。",
 "solution": r"特征多项式:按第一行展开,$|A-\lambda I|=(1-\lambda)[(2-\lambda)(1-\lambda)]-0+1[0-(2-\lambda)]=(2-\lambda)[(1-\lambda)^2-1]=(2-\lambda)(\lambda^2-2\lambda)=-\lambda(\lambda-2)^2$。特征值为 $0$ 与 $2$(二重)。$\lambda=2$:解 $(A-2I)v=0$,即 $\begin{pmatrix}-1&0&1\\0&0&0\\1&0&-1\end{pmatrix}v=0$,得 $v_1=v_3$,$v_2$ 任意,特征子空间 $\mathrm{span}\{(1,0,1),(0,1,0)\}$,维数 $2=$ 代数重数。$\lambda=0$:解 $Av=0$ 得 $v_1+v_3=0,v_2=0$,特征子空间 $\mathrm{span}\{(1,0,-1)\}$,维数 $1$。故 $A$ 可对角化:$D=\mathrm{diag}(2,2,0)$,$P=\begin{pmatrix}1&0&1\\0&1&0\\1&0&-1\end{pmatrix}$(验证:$AP=PD$,各列分别为对应特征值的特征向量)。",
 "answer": r"可对角化:$D=\mathrm{diag}(2,2,0)$,$P=\begin{pmatrix}1&0&1\\0&1&0\\1&0&-1\end{pmatrix}$。",
 "method": "特征子空间基构造对角化",
 "difficulty": "基础",
 "variant_kind": "可对角化:3x3 矩阵特征子空间基的构造与验证",
 "scene_spec": {
  "objects": [
   "板书:$A$ 与特征多项式的展开",
   "板书:两个特征子空间的求解",
   "高亮框:$D=\\mathrm{diag}(2,2,0)$ 与 $P$",
   "验证板书:$AP=PD$",
   "绿色标签「可对角化」"
  ],
  "steps": [
   "第一步:计算特征多项式与特征值。",
   "第二步:求二重特征值的特征子空间,核对维数。",
   "第三步:求零特征值的特征子空间。",
   "第四步:拼出 $D$ 与 $P$,高亮显示。",
   "第五步:验证 $AP=PD$,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c27-03", "category": "高等代数", "sub_category": "矩阵对角化",
 "concept": "谱分解与对角化", "concept_id": "C27",
 "parent_training_ids": ["linalg-049", "linalg-064", "linalg-068"],
 "problem": r"用对角化计算 $A^{10}$,其中 $A=\begin{pmatrix}1&2\\0&3\end{pmatrix}$。",
 "solution": r"$A$ 的特征值为 $1$ 与 $3$。$\lambda=1$:$(A-I)v=0$ 得 $v=(1,0)$;$\lambda=3$:$(A-3I)v=0$,即 $\begin{pmatrix}-2&2\\0&0\end{pmatrix}v=0$,得 $v=(1,1)$。取 $P=\begin{pmatrix}1&1\\0&1\end{pmatrix}$,则 $P^{-1}=\begin{pmatrix}1&-1\\0&1\end{pmatrix}$,$D=\mathrm{diag}(1,3)$,$A=PDP^{-1}$。$A^{10}=PD^{10}P^{-1}=\begin{pmatrix}1&1\\0&1\end{pmatrix}\begin{pmatrix}1&0\\0&3^{10}\end{pmatrix}\begin{pmatrix}1&-1\\0&1\end{pmatrix}=\begin{pmatrix}1&1\\0&1\end{pmatrix}\begin{pmatrix}1&-1\\0&3^{10}\end{pmatrix}=\begin{pmatrix}1&3^{10}-1\\0&3^{10}\end{pmatrix}=\begin{pmatrix}1&59048\\0&59049\end{pmatrix}$。",
 "answer": r"$A^{10}=\begin{pmatrix}1&3^{10}-1\\0&3^{10}\end{pmatrix}=\begin{pmatrix}1&59048\\0&59049\end{pmatrix}$。",
 "method": "对角化的幂(PD^kP^{-1})",
 "difficulty": "中等",
 "variant_kind": "对角化应用:高次幂的快速计算(非对称矩阵,避开谱分解模板)",
 "scene_spec": {
  "objects": [
   "板书:特征值特征向量与 $P,P^{-1},D$",
   "板书:$A^{10}=PD^{10}P^{-1}$ 的代入",
   "板书:矩阵乘法过程与 $3^{10}=59049$",
   "高亮框:$A^{10}=\\begin{pmatrix}1&59048\\\\0&59049\\end{pmatrix}$",
   "标签「对角化加速幂运算」"
  ],
  "steps": [
   "第一步:求特征值与特征向量,构造 $P$ 与 $D$。",
   "第二步:写出 $A=PD P^{-1}$。",
   "第三步:代入 $A^{10}=PD^{10}P^{-1}$。",
   "第四步:完成矩阵乘法,得结果。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c27-04", "category": "高等代数", "sub_category": "矩阵对角化",
 "concept": "谱分解与对角化", "concept_id": "C27",
 "parent_training_ids": ["linalg-049", "linalg-064", "linalg-068"],
 "problem": r"求矩阵 $A=\begin{pmatrix}1&k\\0&2\end{pmatrix}$ 的特征值与特征向量，并讨论特征方向随参数 $k$ 的变化。",
 "solution": r"$A$ 为上三角矩阵,特征值为 $1$ 与 $2$。$\lambda=1$:$(A-I)v=0$,即 $\begin{pmatrix}0&k\\0&1\end{pmatrix}v=0$,得 $v_2=0$,特征方向为 $(1,0)$,与 $k$ 无关。$\lambda=2$:$(A-2I)v=0$,即 $\begin{pmatrix}-1&k\\0&0\end{pmatrix}v=0$,得 $-v_1+kv_2=0$,特征方向为 $(k,1)$。讨论:特征值不随 $k$ 改变,但特征值 $2$ 的特征方向随 $k$ 转动($k=0$ 时为 $(0,1)$,即 $y$ 轴方向;$k\neq0$ 时倾斜);特征值 $1$ 的特征方向始终为 $x$ 轴。",
 "answer": r"特征值 $1,2$;特征方向:$(1,0)$ 与 $(k,1)$;$\lambda=2$ 的特征方向随 $k$ 转动,$\lambda=1$ 的固定。",
 "method": "含参特征方向分析",
 "difficulty": "中等",
 "variant_kind": "特征方向随参数改变:含参矩阵的特征方向转动分析",
 "scene_spec": {
  "objects": [
   "平面坐标系:特征方向向量动画($k$ 滑动)",
   "板书:两个特征方程组的求解",
   "高亮框:特征方向 $(1,0)$(固定)与 $(k,1)$(转动)",
   "标签「特征值不随参数变,方向随参数转」"
  ],
  "steps": [
   "第一步:读出特征值。",
   "第二步:解两个特征方程组。",
   "第三步:动画滑动 $k$,展示 $(k,1)$ 方向转动。",
   "第四步:说明 $(1,0)$ 方向固定。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c27-05", "category": "高等代数", "sub_category": "矩阵对角化",
 "concept": "谱分解与对角化", "concept_id": "C27",
 "parent_training_ids": ["linalg-049", "linalg-064", "linalg-068"],
 "problem": r"证明:若 $n$ 阶矩阵 $A$ 有 $n$ 个互不相同的特征值，则 $A$ 可对角化。",
 "solution": r"只需证明属于不同特征值的特征向量线性无关(归纳法)。$m=1$ 时显然。假设 $m-1$ 个不同特征值对应的特征向量线性无关。设 $\lambda_1,\dots,\lambda_m$ 互不相同,$v_i$ 是 $\lambda_i$ 的特征向量,若 $c_1v_1+\cdots+c_mv_m=0$,用 $A$ 作用得 $\lambda_1c_1v_1+\cdots+\lambda_mc_mv_m=0$;再用 $\lambda_m$ 乘第一式并相减,得 $c_1(\lambda_1-\lambda_m)v_1+\cdots+c_{m-1}(\lambda_{m-1}-\lambda_m)v_{m-1}=0$。由归纳假设 $v_1,\dots,v_{m-1}$ 线性无关,故 $c_i(\lambda_i-\lambda_m)=0$,而 $\lambda_i\neq\lambda_m$,得 $c_i=0$($i=1,\dots,m-1$);回代得 $c_mv_m=0$,$c_m=0$。故 $v_1,\dots,v_m$ 线性无关。于是 $A$ 的 $n$ 个不同特征值给出 $n$ 个线性无关的特征向量,构成一组基,$A$ 在该基下的矩阵为对角矩阵,即 $A$ 可对角化。",
 "answer": r"证明见解法(归纳法证明不同特征值的特征向量线性无关,从而构成基)。",
 "method": "充分条件证明(归纳法)",
 "difficulty": "进阶",
 "variant_kind": "证明型:不同特征值充分条件的严格证明(特征向量线性无关归纳)",
 "scene_spec": {
  "objects": [
   "板书:归纳假设与线性组合为零的等式",
   "板书:用 $A$ 作用与乘以 $\\lambda_m$ 相减的运算",
   "板书:逐项系数为零的推导",
   "高亮框:线性无关 → 构成基 → 可对角化",
   "标签「充分条件」"
  ],
  "steps": [
   "第一步:写出归纳假设。",
   "第二步:对线性组合等式两边用 $A$ 作用并相减。",
   "第三步:由归纳假设得各系数为零。",
   "第四步:说明 $n$ 个特征向量构成基。",
   "第五步:高亮结论,完成证明。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
# ===================== C29 多项式因式分解与根 =====================
{
 "id": "draft-c29-01", "category": "高等代数", "sub_category": "多项式",
 "concept": "多项式因式分解与根", "concept_id": "C29",
 "parent_training_ids": ["linalg-051"],
 "problem": r"用有理根定理将多项式 $f(x)=x^3-7x+6$ 在实数域上因式分解。",
 "solution": r"有理根定理:首项系数为 $1$,有理根必为整数且是常数项 $6$ 的因子,候选为 $\pm1,\pm2,\pm3,\pm6$。试根:$f(1)=1-7+6=0$,故 $x-1$ 是因子。综合除法:$x^3-7x+6=(x-1)(x^2+x-6)=(x-1)(x-2)(x+3)$。",
 "answer": r"$x^3-7x+6=(x-1)(x-2)(x+3)$。",
 "method": "有理根定理+综合除法",
 "difficulty": "基础",
 "variant_kind": "数值结构变化:有理根试根的三次分解(与父题不同多项式)",
 "scene_spec": {
  "objects": [
   "板书:$f(x)=x^3-7x+6$ 与常数项因子候选",
   "板书:试根 $f(1)=0$ 与综合除法过程",
   "板书:二次因子 $x^2+x-6$ 的再分解",
   "高亮框:$(x-1)(x-2)(x+3)$",
   "标签「有理根定理」"
  ],
  "steps": [
   "第一步:列出常数项因子的候选根。",
   "第二步:试根得 $x=1$,综合除法降次。",
   "第三步:分解二次因子。",
   "第四步:高亮完全分解。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c29-02", "category": "高等代数", "sub_category": "多项式",
 "concept": "多项式因式分解与根", "concept_id": "C29",
 "parent_training_ids": ["linalg-051"],
 "problem": r"已知 $2+i$ 是实系数多项式 $f(x)=x^3-7x^2+17x-15$ 的一个根，求 $f$ 的全部根。",
 "solution": r"实系数多项式的非实根成对出现:$2-i$ 也是根,故 $f$ 含因子 $(x-(2+i))(x-(2-i))=x^2-4x+5$。用韦达定理或综合除法:设第三根为 $r$,三根之和为 $7$,故 $r=7-(2+i)-(2-i)=3$。验证:$f=(x-3)(x^2-4x+5)$,展开核对:$x^3-4x^2+5x-3x^2+12x-15=x^3-7x^2+17x-15$ ✓。全部根:$3$,$2+i$,$2-i$。",
 "answer": r"全部根:$3$,$2+i$,$2-i$。",
 "method": "复根共轭配对+韦达定理",
 "difficulty": "基础",
 "variant_kind": "复根配对:已知复根求全部根(共轭+韦达)",
 "scene_spec": {
  "objects": [
   "复平面:根 $2+i$ 与 $2-i$ 的共轭对称标注,实根 $3$ 在实轴上",
   "板书:共轭配对与二次因子 $x^2-4x+5$",
   "板书:韦达定理求第三根",
   "高亮框:三个根",
   "验证板书:$(x-3)(x^2-4x+5)$ 展开核对"
  ],
  "steps": [
   "第一步:由实系数性质得共轭根。",
   "第二步:在复平面上标出共轭对。",
   "第三步:构造二次因子并用韦达求第三根。",
   "第四步:展开验证。",
   "第五步:高亮全部根。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c29-03", "category": "高等代数", "sub_category": "多项式",
 "concept": "多项式因式分解与根", "concept_id": "C29",
 "parent_training_ids": ["linalg-051"],
 "problem": r"用 $f$ 与 $f'$ 的公因式求多项式 $f(x)=x^4-4x^3+6x^2-4x+1$ 的重根及其重数。",
 "solution": r"$f'(x)=4x^3-12x^2+12x-4=4(x-1)^3$。若 $x_0$ 是 $f$ 的重根,则 $x_0$ 必为 $f$ 与 $f'$ 的公根;这里 $f'$ 的根只有 $x=1$,检验 $f(1)=1-4+6-4+1=0$,故 $x=1$ 是重根。重数:用辗转相除法求 $\gcd(f,f')$。$f$ 除以 $f'$:设 $f=(x-1)^4$(由二项式 $(x-1)^4=x^4-4x^3+6x^2-4x+1$ 直接看出),则 $\gcd(f,f')=(x-1)^3$,故 $x=1$ 的重数为 $3+1=4$,即四重根。(或由 $f=(x-1)^4$ 直接得四重根。)",
 "answer": r"$f=(x-1)^4$,$x=1$ 是四重根。",
 "method": "导数公因式判重根",
 "difficulty": "中等",
 "variant_kind": "重根判定:公因式方法与二项式识别的双路径",
 "scene_spec": {
  "objects": [
   "板书:$f$ 与 $f'=4(x-1)^3$",
   "板书:二项式展开 $(x-1)^4$ 的对照",
   "板书:$\\gcd(f,f')=(x-1)^3$ 与重数 $=3+1=4$",
   "高亮框:四重根 $x=1$",
   "标签「重根 ⟺ f 与 f' 公根」"
  ],
  "steps": [
   "第一步:求导并因式分解。",
   "第二步:识别 $f=(x-1)^4$ 的二项式结构。",
   "第三步:求公因式 $(x-1)^3$。",
   "第四步:由公因式次数加一得重数。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c29-04", "category": "高等代数", "sub_category": "多项式",
 "concept": "多项式因式分解与根", "concept_id": "C29",
 "parent_training_ids": ["linalg-051"],
 "problem": r"求使多项式 $f(x)=x^3-3x+a$ 有重根的参数 $a$ 的值。",
 "solution": r"$f$ 有重根当且仅当 $f$ 与 $f'$ 有公共根。$f'(x)=3x^2-3=3(x-1)(x+1)$,可能的公根为 $x=1$ 或 $x=-1$。$x=1$ 是公根 ⟺ $f(1)=0$,即 $1-3+a=0$,$a=2$;$x=-1$ 是公根 ⟺ $f(-1)=0$,即 $-1+3+a=0$,$a=-2$。故 $a=2$ 或 $a=-2$。验证:$a=2$ 时 $f=x^3-3x+2=(x-1)^2(x+2)$;$a=-2$ 时 $f=x^3-3x-2=(x+1)^2(x-2)$。",
 "answer": r"$a=2$ 或 $a=-2$;对应分解 $(x-1)^2(x+2)$ 与 $(x+1)^2(x-2)$。",
 "method": "判别式思想(公根条件)",
 "difficulty": "中等",
 "variant_kind": "含参根分类:参数取临界值时出现重根的条件",
 "scene_spec": {
  "objects": [
   "数轴:参数 $a$ 的两个临界值 $a=\\pm2$",
   "动画:$a$ 滑动时曲线 $f$ 与 $x$ 轴的交点变化(重根处相切)",
   "板书:$f'=3(x-1)(x+1)$ 与公根条件",
   "高亮框:$a=2$(重根 $1$)与 $a=-2$(重根 $-1$)"
  ],
  "steps": [
   "第一步:求导并找出可能的公根。",
   "第二步:代入得两个临界参数值。",
   "第三步:动画展示曲线与 $x$ 轴相切的重根情形。",
   "第四步:验证两个分解式。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c29-05", "category": "高等代数", "sub_category": "多项式",
 "concept": "多项式因式分解与根", "concept_id": "C29",
 "parent_training_ids": ["linalg-051"],
 "problem": r"证明三次多项式的根与系数关系(韦达定理)，并构造一个以 $2$、$-1$、$\frac12$ 为根的首一三次多项式。",
 "solution": r"设首一三次多项式 $f(x)=x^3+px^2+qx+r$ 的根为 $\alpha,\beta,\gamma$,则 $f(x)=(x-\alpha)(x-\beta)(x-\gamma)$。展开右边:$x^3-(\alpha+\beta+\gamma)x^2+(\alpha\beta+\beta\gamma+\gamma\alpha)x-\alpha\beta\gamma$。比较系数得韦达定理:$\alpha+\beta+\gamma=-p$,$\alpha\beta+\beta\gamma+\gamma\alpha=q$,$\alpha\beta\gamma=-r$。构造:以 $2,-1,\frac12$ 为根,则 $f(x)=(x-2)(x+1)(x-\frac12)$。展开:$(x^2-x-2)(x-\frac12)=x^3-x^2-2x-\frac12x^2+\frac12x+1=x^3-\frac32x^2-\frac32x+1$。",
 "answer": r"韦达定理:根和 $=-p$,两两积和 $=q$,根积 $=-r$;构造:$f=x^3-\frac32x^2-\frac32x+1$。",
 "method": "展开比较系数(韦达定理证明)+构造",
 "difficulty": "进阶",
 "variant_kind": "证明+构造:韦达定理的推导与给定根的多项式构造",
 "scene_spec": {
  "objects": [
   "板书:$(x-\\alpha)(x-\\beta)(x-\\gamma)$ 的展开",
   "板书:逐项比较系数的对照表",
   "高亮框:韦达定理三式",
   "板书:给定三根的乘积展开",
   "高亮框:$x^3-\\frac32x^2-\\frac32x+1$"
  ],
  "steps": [
   "第一步:写出因式分解形式并展开。",
   "第二步:逐项比较系数得韦达定理。",
   "第三步:高亮三个关系式。",
   "第四步:代入给定三根展开构造。",
   "第五步:高亮构造结果,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
# ===================== C32 线性方程组解空间 =====================
{
 "id": "draft-c32-01", "category": "高等代数", "sub_category": "线性方程组",
 "concept": "线性方程组解空间", "concept_id": "C32",
 "parent_training_ids": ["linalg-055", "linalg-056"],
 "problem": r"求齐次线性方程组 $x_1+2x_2-x_3+x_4=0$ 的基础解系。",
 "solution": r"一个方程、四个未知量,自由未知量为 $x_2,x_3,x_4$,解出 $x_1=-2x_2+x_3-x_4$。分别令 $(x_2,x_3,x_4)=(1,0,0),(0,1,0),(0,0,1)$,得基础解系 $\xi_1=(-2,1,0,0)$,$\xi_2=(1,0,1,0)$,$\xi_3=(-1,0,0,1)$。解空间为 $\mathrm{span}\{\xi_1,\xi_2,\xi_3\}$,维数 $3$。",
 "answer": r"基础解系:$\xi_1=(-2,1,0,0)$,$\xi_2=(1,0,1,0)$,$\xi_3=(-1,0,0,1)$。",
 "method": "自由未知量赋值法",
 "difficulty": "基础",
 "variant_kind": "维数变化:四变量单方程的基础解系(与父题二方程不同)",
 "scene_spec": {
  "objects": [
   "板书:方程 $x_1+2x_2-x_3+x_4=0$ 与自由未知量标注",
   "板书:三个自由变量依次取单位值的赋值过程",
   "高亮框:三个基础解系向量",
   "标签「解空间维数 3」"
  ],
  "steps": [
   "第一步:标出自由未知量并解出主变量。",
   "第二步:依次给自由变量赋值 $(1,0,0)$ 等。",
   "第三步:写出三个基础解系向量。",
   "第四步:高亮显示。",
   "第五步:说明解空间维数为 $3$,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c32-02", "category": "高等代数", "sub_category": "线性方程组",
 "concept": "线性方程组解空间", "concept_id": "C32",
 "parent_training_ids": ["linalg-055", "linalg-056"],
 "problem": r"求齐次线性方程组 $\begin{cases}x+y+z=0\\ 2x+2y+2z=0\end{cases}$ 的解空间的维数与一组基。",
 "solution": r"两个方程成比例,实际上只有一个独立方程 $x+y+z=0$,系数矩阵秩为 $1$。未知量个数 $n=3$,故解空间维数为 $n-r=3-1=2$。自由未知量取 $y,z$,$x=-y-z$。取 $(y,z)=(1,0)$ 得 $\xi_1=(-1,1,0)$;取 $(y,z)=(0,1)$ 得 $\xi_2=(-1,0,1)$。解空间为 $\mathrm{span}\{\xi_1,\xi_2\}$。",
 "answer": r"维数为 $2$;一组基:$\xi_1=(-1,1,0)$,$\xi_2=(-1,0,1)$。",
 "method": "秩-零度定维数+赋值取基",
 "difficulty": "基础",
 "variant_kind": "解空间维数:成比例方程的秩与维数计算",
 "scene_spec": {
  "objects": [
   "板书:两方程的成比例关系与秩的计算",
   "板书:维数 $=n-r=3-1=2$",
   "板书:两个基向量的赋值构造",
   "高亮框:$\\mathrm{span}\\{(-1,1,0),(-1,0,1)\\}$",
   "标签「解空间=平面」"
  ],
  "steps": [
   "第一步:识别两方程成比例,独立方程数为 $1$。",
   "第二步:由秩-零度得维数 $2$。",
   "第三步:赋值构造两个基向量。",
   "第四步:高亮解空间。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c32-03", "category": "高等代数", "sub_category": "线性方程组",
 "concept": "线性方程组解空间", "concept_id": "C32",
 "parent_training_ids": ["linalg-055", "linalg-056"],
 "problem": r"求非齐次线性方程 $x_1+x_2+x_3-x_4=1$ 的通解(用特解与对应齐次方程基础解系表示)。",
 "solution": r"特解:取 $x_2=x_3=x_4=0$,得 $\eta=(1,0,0,0)$。对应齐次方程 $x_1+x_2+x_3-x_4=0$ 的基础解系:自由未知量 $x_2,x_3,x_4$,$x_1=-x_2-x_3+x_4$,取单位赋值得 $\xi_1=(-1,1,0,0)$,$\xi_2=(-1,0,1,0)$,$\xi_3=(1,0,0,1)$。通解:$x=\eta+c_1\xi_1+c_2\xi_2+c_3\xi_3$,即 $(1-c_1-c_2+c_3,\ c_1,\ c_2,\ c_3)$。",
 "answer": r"通解:$x=(1,0,0,0)+c_1(-1,1,0,0)+c_2(-1,0,1,0)+c_3(1,0,0,1)$。",
 "method": "特解+齐次基础解系",
 "difficulty": "中等",
 "variant_kind": "非齐次结构:通解的特解+基础解系表示",
 "scene_spec": {
  "objects": [
   "板书:特解的取法 $(1,0,0,0)$",
   "板书:齐次基础解系的构造",
   "高亮框:通解 $\\eta+c_1\\xi_1+c_2\\xi_2+c_3\\xi_3$",
   "标签「非齐次通解=特解+齐次解」"
  ],
  "steps": [
   "第一步:取一个特解。",
   "第二步:求对应齐次方程的基础解系。",
   "第三步:拼出通解。",
   "第四步:高亮显示。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c32-04", "category": "高等代数", "sub_category": "线性方程组",
 "concept": "线性方程组解空间", "concept_id": "C32",
 "parent_training_ids": ["linalg-055", "linalg-056"],
 "problem": r"讨论方程组 $\begin{cases}x+y=1\\ 2x+2y=a\end{cases}$ 的解随参数 $a$ 的变化。",
 "solution": r"系数矩阵 $A=\begin{pmatrix}1&1\\2&2\end{pmatrix}$,秩为 $1$;增广矩阵 $\begin{pmatrix}1&1&1\\2&2&a\end{pmatrix}$。当 $a=2$ 时,两方程成比例(同一条直线),增广矩阵秩为 $1=$ 系数矩阵秩,且 $1<2$(未知量个数),方程组有无穷多解:$x+y=1$。当 $a\neq2$ 时,增广矩阵秩为 $2>$ 系数矩阵秩 $1$,方程组无解(两条平行直线)。",
 "answer": r"$a=2$ 时无穷多解($x+y=1$);$a\neq2$ 时无解(平行直线)。",
 "method": "含参相容性(秩比较)",
 "difficulty": "中等",
 "variant_kind": "参数相容性:系数矩阵与增广矩阵秩的含参比较",
 "scene_spec": {
  "objects": [
   "平面坐标系:直线 $x+y=1$ 与直线族 $2x+2y=a$($a$ 滑动动画)",
   "动画:$a=2$ 时两直线重合,$a\\neq2$ 时平行分离",
   "板书:系数矩阵秩与增广矩阵秩的对照",
   "高亮框:两分支结论"
  ],
  "steps": [
   "第一步:计算系数矩阵与增广矩阵的秩。",
   "第二步:动画滑动 $a$,展示两直线重合与平行。",
   "第三步:分析 $a=2$ 分支,无穷多解。",
   "第四步:分析 $a\\neq2$ 分支,无解。",
   "第五步:高亮两分支结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c32-05", "category": "高等代数", "sub_category": "线性方程组",
 "concept": "线性方程组解空间", "concept_id": "C32",
 "parent_training_ids": ["linalg-055", "linalg-056"],
 "problem": r"证明:齐次线性方程组 $Ax=0$ 的解集是 $\mathbb R^n$ 的线性子空间,其维数为 $n-\mathrm{rank}(A)$;非齐次方程组 $Ax=b$($b\neq0$)的解集是 $\eta_0+\ker A$(仿射子空间)而不是线性子空间。",
 "solution": r"子空间:若 $x_1,x_2\in\ker A$,则 $A(x_1+x_2)=0$ 且 $A(cx_1)=0$,对加法与数乘封闭;又 $0\in\ker A$,故 $\ker A$ 是线性子空间。维数:设 $\mathrm{rank}(A)=r$。把 $A$ 通过行变换化为行阶梯形,主元列有 $r$ 个,对应 $r$ 个主变量,其余 $n-r$ 个为自由变量;自由变量任意取值即唯一确定解,解空间与 $\mathbb R^{n-r}$ 同构,故维数为 $n-r$。非齐次:若 $\eta_0$ 是 $Ax=b$ 的一个特解,则 $x$ 是解 ⟺ $x-\eta_0\in\ker A$,故解集为 $\eta_0+\ker A$,是 $\ker A$ 的陪集(仿射子空间)。因 $b\neq0$ 时 $0\notin\eta_0+\ker A$(否则 $b=A0=0$),不含零向量,故不是线性子空间。",
 "answer": r"证明见解法($\\ker A$ 对加法数乘封闭;维数 $n-r$;非齐次解集为陪集且不含零向量)。",
 "method": "解空间结构证明(子空间+秩-零度+陪集)",
 "difficulty": "进阶",
 "variant_kind": "证明型:解空间的结构定理证明与齐次/非齐次的本质区别",
 "scene_spec": {
  "objects": [
   "三维示意图:过原点的平面(齐次解空间)",
   "三维示意图:不过原点的平面(非齐次解集,陪集)与平移向量 $\\eta_0$",
   "板书:封闭性验证($A(x_1+x_2)=0$ 等)",
   "板书:主变量/自由变量计数得维数 $n-r$",
   "高亮框:齐次=子空间,非齐次=陪集"
  ],
  "steps": [
   "第一步:验证 $\\ker A$ 对加法与数乘封闭。",
   "第二步:展示过原点的平面(子空间)。",
   "第三步:由主变量计数推导维数 $n-r$。",
   "第四步:展示非齐次解集为平移后的平面(陪集)。",
   "第五步:说明不含原点故非子空间,高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
]

def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="\n") as f:
        for row in DATA:
            f.write(json.dumps(row, ensure_ascii=False, separators=(",", ":"))
                    + "\n")
    print(f"写入 {len(DATA)} 行 -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
