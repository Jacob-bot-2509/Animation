"""batch-16 生成器:三个单条考点各 5 题
(C43 对偶基与线性泛函 / C44 辛形式与保持变换 / C45 条件概率与独立性)。
全部数学结论由作者逐题手工验算(见 DRAFT_REPORT.md 核算说明);
起草过程未读 eval/test 题文或答案作提示;凡有理数一律分数。
"""
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "draft.jsonl"

DATA = [
# ===================== C43 对偶基与线性泛函 =====================
{
 "id": "draft-c43-01", "category": "高等代数", "sub_category": "对偶空间",
 "concept": "对偶基与线性泛函", "concept_id": "C43",
 "parent_training_ids": ["linalg-069"],
 "problem": r"设 $\mathbb R^2$ 的基为 $\eta_1=(1,1)$，$\eta_2=(1,-1)$。求对偶基 $f_1,f_2$，使 $f_i(\eta_j)=\delta_{ij}$。",
 "solution": r"设 $f_1(x,y)=ax+by$。条件:$f_1(\eta_1)=a+b=1$,$f_1(\eta_2)=a-b=0$,解得 $a=b=\frac12$,故 $f_1(x,y)=\frac{x+y}{2}$。设 $f_2(x,y)=cx+dy$。条件:$f_2(\eta_1)=c+d=0$,$f_2(\eta_2)=c-d=1$,解得 $c=\frac12,d=-\frac12$,故 $f_2(x,y)=\frac{x-y}{2}$。验证:$f_1(\eta_1)=\frac{1+1}{2}=1$,$f_1(\eta_2)=0$;$f_2(\eta_1)=0$,$f_2(\eta_2)=1$ ✓。",
 "answer": r"$f_1(x,y)=\frac{x+y}{2}$,$f_2(x,y)=\frac{x-y}{2}$。",
 "method": "解方程组求对偶基",
 "difficulty": "基础",
 "variant_kind": "非标准基:非正交基的对偶基求解(与标准基父题不同)",
 "scene_spec": {
  "objects": [
   "平面坐标系:基向量 $\\eta_1,\\eta_2$ 的箭头",
   "板书:两个泛函的待定系数与方程组",
   "高亮框:$f_1=\\frac{x+y}{2}$,$f_2=\\frac{x-y}{2}$",
   "验证板书:$f_i(\\eta_j)=\\delta_{ij}$"
  ],
  "steps": [
   "第一步:画出两个基向量。",
   "第二步:设泛函为一般线性形式。",
   "第三步:由配对条件解方程组。",
   "第四步:高亮两个泛函。",
   "第五步:逐项验证配对关系。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c43-02", "category": "高等代数", "sub_category": "对偶空间",
 "concept": "对偶基与线性泛函", "concept_id": "C43",
 "parent_training_ids": ["linalg-069"],
 "problem": r"求 $\mathbb R^3$ 上满足 $f(1,1,0)=2$，$f(0,1,1)=-1$，$f(1,0,1)=3$ 的线性泛函 $f(x,y,z)=ax+by+cz$。",
 "solution": r"代入三个条件:$a+b=2$,$b+c=-1$,$a+c=3$。第一式减第二式:$a-c=3$;与第三式 $a+c=3$ 相加得 $2a=6$,$a=3$;代入第三式 $c=0$;代入第一式 $b=-1$。故 $f(x,y,z)=3x-y$。验证:$f(1,1,0)=3-1=2$ ✓;$f(0,1,1)=-1$ ✓;$f(1,0,1)=3$ ✓。",
 "answer": r"$f(x,y,z)=3x-y$。",
 "method": "由取值反求泛函(解系数方程组)",
 "difficulty": "基础",
 "variant_kind": "逆向构造:由泛函在指定向量上的取值反求表达式",
 "scene_spec": {
  "objects": [
   "板书:三个条件方程 $a+b=2,b+c=-1,a+c=3$",
   "板书:消元求解过程",
   "高亮框:$f(x,y,z)=3x-y$",
   "验证板书:三组取值逐项核对"
  ],
  "steps": [
   "第一步:设一般形式并代入三个条件。",
   "第二步:展示消元求解。",
   "第三步:得系数 $a=3,b=-1,c=0$。",
   "第四步:高亮泛函表达式。",
   "第五步:逐项验证。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c43-03", "category": "高等代数", "sub_category": "对偶空间",
 "concept": "对偶基与线性泛函", "concept_id": "C43",
 "parent_training_ids": ["linalg-069"],
 "problem": r"设 $\mathbb R^3$ 的标准基为 $\varepsilon_1,\varepsilon_2,\varepsilon_3$，新基为 $\eta_1=(1,1,0)$，$\eta_2=(0,1,1)$，$\eta_3=(1,0,1)$。求新基的对偶基 $\{f_1,f_2,f_3\}$ 在标准对偶基 $\{\varepsilon^1,\varepsilon^2,\varepsilon^3\}$ 下的坐标。",
 "solution": r"从标准基到新基的过渡矩阵(新基向量按列)$P=\begin{pmatrix}1&0&1\\1&1&0\\0&1&1\end{pmatrix}$。设新对偶基在标准对偶基下的坐标矩阵为 $C$(第 $i$ 行是 $f_i$ 的坐标),则配对条件 $f_i(\eta_j)=\delta_{ij}$ 等价于 $CP=I$,故 $C=P^{-1}$。求 $P^{-1}$:$\det P=2$,$P^{-1}=\frac12\begin{pmatrix}1&1&-1\\-1&1&1\\1&-1&1\end{pmatrix}$。故新对偶基为 $f_1=\frac12(\varepsilon^1+\varepsilon^2-\varepsilon^3)$,$f_2=\frac12(-\varepsilon^1+\varepsilon^2+\varepsilon^3)$,$f_3=\frac12(\varepsilon^1-\varepsilon^2+\varepsilon^3)$。验证(全部九个配对值):$f_1(\eta_1)=\frac12(1+1-0)=1$,$f_1(\eta_2)=\frac12(0+1-1)=0$,$f_1(\eta_3)=\frac12(1+0-1)=0$;$f_2(\eta_1)=\frac12(-1+1+0)=0$,$f_2(\eta_2)=\frac12(0+1+1)=1$,$f_2(\eta_3)=\frac12(-1+0+1)=0$;$f_3(\eta_1)=\frac12(1-1+0)=0$,$f_3(\eta_2)=\frac12(0-1+1)=0$,$f_3(\eta_3)=\frac12(1+0+1)=1$。全部满足 $f_i(\eta_j)=\delta_{ij}$ ✓。",
 "answer": r"$f_1=\frac12(\varepsilon^1+\varepsilon^2-\varepsilon^3)$,$f_2=\frac12(-\varepsilon^1+\varepsilon^2+\varepsilon^3)$,$f_3=\frac12(\varepsilon^1-\varepsilon^2+\varepsilon^3)$(坐标取 $P^{-1}$ 的行)。",
 "method": "对偶基的过渡矩阵((P⁻¹)ᵀ)",
 "difficulty": "中等",
 "variant_kind": "维数变化:三维基变换下对偶基的坐标转换",
 "scene_spec": {
  "objects": [
   "板书:过渡矩阵 $P$ 与 $P^{-1}$",
   "板书:转置得对偶过渡矩阵",
   "高亮框:三个新对偶基泛函",
   "验证板书:配对 $f_i(\\eta_j)=\\delta_{ij}$"
  ],
  "steps": [
   "第一步:写出过渡矩阵 $P$。",
   "第二步:求 $P^{-1}$。",
   "第三步:转置得对偶基过渡矩阵。",
   "第四步:写出新对偶基。",
   "第五步:逐项验证配对关系。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c43-04", "category": "高等代数", "sub_category": "对偶空间",
 "concept": "对偶基与线性泛函", "concept_id": "C43",
 "parent_training_ids": ["linalg-069"],
 "problem": r"证明对偶配对 $\langle v,f\rangle=f(v)$ 在基变换下不变:设向量 $v$ 与泛函 $f$ 在旧基下的坐标分别为 $x$ 与 $y$，在新基下的坐标分别为 $\tilde x$ 与 $\tilde y$，则 $y^{\mathsf T}x=\tilde y^{\mathsf T}\tilde x$。",
 "solution": r"设新旧基的过渡矩阵为 $P$(新基向量为旧基向量的 $P$ 线性组合),则向量坐标变换为 $x=P\tilde x$(新坐标经 $P$ 得旧坐标)。对偶基的过渡矩阵为 $(P^{-1})^{\mathsf T}$,故泛函坐标变换为 $y=(P^{-1})^{\mathsf T}\tilde y$。于是 $y^{\mathsf T}x=((P^{-1})^{\mathsf T}\tilde y)^{\mathsf T}(P\tilde x)=\tilde y^{\mathsf T}P^{-1}P\tilde x=\tilde y^{\mathsf T}\tilde x$。故配对值与基的选择无关。",
 "answer": r"证明见解法(坐标变换 $x=P\tilde x$、$y=(P^{-1})^{\mathsf T}\tilde y$ 代入相消)。",
 "method": "配对不变性证明",
 "difficulty": "中等",
 "variant_kind": "泛函坐标与配对不变性:坐标变换下配对的抵消证明",
 "scene_spec": {
  "objects": [
   "板书:向量坐标变换 $x=P\\tilde x$",
   "板书:泛函坐标变换 $y=(P^{-1})^{\\mathsf T}\\tilde y$",
   "板书:代入配对并相消",
   "高亮框:$y^{\\mathsf T}x=\\tilde y^{\\mathsf T}\\tilde x$"
  ],
  "steps": [
   "第一步:写出两类坐标的变换公式。",
   "第二步:说明对偶基过渡矩阵为何是 $(P^{-1})^{\\mathsf T}$。",
   "第三步:代入配对表达式。",
   "第四步:$P^{-1}P$ 相消。",
   "第五步:高亮结论,完成证明。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c43-05", "category": "高等代数", "sub_category": "对偶空间",
 "concept": "对偶基与线性泛函", "concept_id": "C43",
 "parent_training_ids": ["linalg-069"],
 "problem": r"设 $V$ 是有限维线性空间。证明 $\dim V^*=\dim V$，并构造自然同构 $\Phi:V\to V^{**}$($\Phi(v)(f)=f(v)$)。",
 "solution": r"取 $V$ 的基 $e_1,\dots,e_n$ 与其对偶基 $e^1,\dots,e^n$($e^i(e_j)=\delta_{ij}$)。任何 $f\in V^*$ 由它在基上的取值唯一确定,且 $f=\sum_i f(e_i)e^i$($e^1,\dots,e^n$ 张成 $V^*$);又 $e^1,\dots,e^n$ 线性无关(若 $\sum c_ie^i=0$,作用于 $e_j$ 得 $c_j=0$)。故 $e^1,\dots,e^n$ 是 $V^*$ 的基,$\dim V^*=n=\dim V$。自然同构:定义 $\Phi(v)(f)=f(v)$。先验证 $\Phi(v)\in V^{**}$:对任意 $f,g\in V^*$ 与 $c$,$\Phi(v)(f+g)=(f+g)(v)=f(v)+g(v)=\Phi(v)(f)+\Phi(v)(g)$,$\Phi(v)(cf)=(cf)(v)=cf(v)=c\Phi(v)(f)$,故 $\Phi(v)$ 是 $V^*$ 上的线性泛函。再验证 $\Phi$ 线性:$\Phi(v_1+v_2)(f)=f(v_1+v_2)=f(v_1)+f(v_2)=\Phi(v_1)(f)+\Phi(v_2)(f)$;$\Phi(cv)(f)=f(cv)=cf(v)=c\Phi(v)(f)$。单射:若 $\Phi(v)=0$,则对一切 $f$,$f(v)=0$。若 $v\neq0$,把它延拓为基 $v=e_1,e_2,\dots,e_n$,取 $f=e^1$,则 $f(v)=1\neq0$,矛盾,故 $v=0$。于是 $\Phi$ 单射,而 $\dim V^{**}=\dim V^*=\dim V$,故 $\Phi$ 为同构。",
 "answer": r"证明见解法(对偶基为基、维数相等;$\Phi$ 对 $f$ 与对 $v$ 均线性、单射,维数相同故同构)。",
 "method": "维数与双重对偶自然同构证明",
 "difficulty": "进阶",
 "variant_kind": "证明型:对偶空间维数与自然同构 V≅V** 的完整证明",
 "scene_spec": {
  "objects": [
   "板书:对偶基的张成与线性无关论证",
   "板书:$\\Phi$ 的线性与单射验证",
   "三维示意图:$V$、$V^*$、$V^{**}$ 的同构箭头",
   "高亮框:$V\\cong V^{**}$(自然同构)"
  ],
  "steps": [
   "第一步:证明对偶基是 $V^*$ 的基。",
   "第二步:得维数相等。",
   "第三步:构造 $\\Phi$ 并验证线性。",
   "第四步:验证单射。",
   "第五步:由维数相同得同构,高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
# ===================== C44 辛形式与保持变换 =====================
{
 "id": "draft-c44-01", "category": "高等代数", "sub_category": "辛空间",
 "concept": "辛形式与保持变换", "concept_id": "C44",
 "parent_training_ids": ["linalg-070"],
 "problem": r"设 $\mathbb R^2$ 上的辛形式为 $\omega(u,v)=u_1v_2-u_2v_1$。验证剪切矩阵 $A=\begin{pmatrix}1&2\\0&1\end{pmatrix}$ 保持 $\omega$。",
 "solution": r"对任意 $u,v$,$\omega(Au,Av)=\det(Au,Av)$(二维情形 $\omega$ 就是行列式)。由行列式乘法性质,$\det(Au,Av)=\det A\cdot\det(u,v)=\det A\cdot\omega(u,v)$。而 $\det A=1\times1-2\times0=1$,故 $\omega(Au,Av)=\omega(u,v)$。即剪切矩阵保持辛形式——二维辛变换恰为保面积(行列式为 $1$)的线性变换。",
 "answer": r"剪切矩阵保持 $\omega$(二维辛 = 保面积,$\det A=1$)。",
 "method": "行列式乘法性质验证",
 "difficulty": "基础",
 "variant_kind": "保持条件验证:二维剪切保持辛形式(det=1 即辛)",
 "scene_spec": {
  "objects": [
   "平面坐标系:平行四边形(两向量张成)与剪切后的像",
   "动画:剪切作用下面积保持不变",
   "板书:$\\omega(Au,Av)=\\det A\\cdot\\omega(u,v)$",
   "高亮框:「保持辛形式」"
  ],
  "steps": [
   "第一步:说明二维辛形式即行列式。",
   "第二步:用行列式乘法性质推导。",
   "第三步:计算 $\\det A=1$。",
   "第四步:动画展示面积不变。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c44-02", "category": "高等代数", "sub_category": "辛空间",
 "concept": "辛形式与保持变换", "concept_id": "C44",
 "parent_training_ids": ["linalg-070"],
 "problem": r"验证矩阵 $A=\begin{pmatrix}2&0\\0&1\end{pmatrix}$ 不保持 $\mathbb R^2$ 上的辛形式 $\omega(u,v)=u_1v_2-u_2v_1$。",
 "solution": r"取 $u=e_1=(1,0)$,$v=e_2=(0,1)$。$Au=2e_1=(2,0)$,$Av=e_2=(0,1)$。$\omega(Au,Av)=\det\begin{pmatrix}2&0\\0&1\end{pmatrix}=2\times1-0\times0=2$。而 $\omega(u,v)=\det\begin{pmatrix}1&0\\0&1\end{pmatrix}=1$。$2\neq1$,故 $A$ 不保持 $\omega$。(一般地,$\omega(Au,Av)=\det A\cdot\omega(u,v)$,$\det A=2\neq1$,故不保持。)",
 "answer": r"不保持:$\omega(Ae_1,Ae_2)=2\neq1=\omega(e_1,e_2)$。",
 "method": "反例验证(取基向量对)",
 "difficulty": "基础",
 "variant_kind": "反例:非保面积变换不保持辛形式",
 "scene_spec": {
  "objects": [
   "平面坐标系:单位正方形与拉伸后的矩形(面积变为 2 倍)",
   "板书:$\\omega(Ae_1,Ae_2)=2$ 与 $\\omega(e_1,e_2)=1$ 的对照",
   "红色标签「不保持」"
  ],
  "steps": [
   "第一步:取基向量对。",
   "第二步:计算两边的辛形式值。",
   "第三步:对照得 $2\\neq1$。",
   "第四步:动画展示面积被拉伸。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c44-03", "category": "高等代数", "sub_category": "辛空间",
 "concept": "辛形式与保持变换", "concept_id": "C44",
 "parent_training_ids": ["linalg-070"],
 "problem": r"在 $\mathbb R^4$ 上定义标准辛形式 $\omega((p_1,p_2,q_1,q_2),(r_1,r_2,s_1,s_2))=p_1s_1+p_2s_2-q_1r_1-q_2r_2$。验证 $A=\mathrm{diag}(2,2,\frac12,\frac12)$ 保持 $\omega$。",
 "solution": r"对任意 $x=(p_1,p_2,q_1,q_2)$,$y=(r_1,r_2,s_1,s_2)$,$Ax=(2p_1,2p_2,\frac12q_1,\frac12q_2)$,$Ay=(2r_1,2r_2,\frac12s_1,\frac12s_2)$。于是 $\omega(Ax,Ay)=(2p_1)(\frac12s_1)+(2p_2)(\frac12s_2)-(\frac12q_1)(2r_1)-(\frac12q_2)(2r_2)=p_1s_1+p_2s_2-q_1r_1-q_2r_2=\omega(x,y)$。故 $A$ 保持 $\omega$,是辛变换。",
 "answer": r"$A$ 保持 $\omega$(逐项核对:p 方向放大 2 倍、q 方向收缩为 1/2,配对恰好抵消)。",
 "method": "四维辛变换验证(逐项配对)",
 "difficulty": "中等",
 "variant_kind": "四维形式:高维辛变换的配对验证(p 放大 q 收缩)",
 "scene_spec": {
  "objects": [
   "板书:标准辛形式与 $A$ 的作用",
   "板书:$\\omega(Ax,Ay)$ 的逐项计算",
   "板书:放大与收缩因子的配对抵消",
   "高亮框:$\\omega(Ax,Ay)=\\omega(x,y)$"
  ],
  "steps": [
   "第一步:写出四维辛形式。",
   "第二步:写出 $A$ 对坐标的作用。",
   "第三步:逐项计算变换后的配对。",
   "第四步:展示因子抵消。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c44-04", "category": "高等代数", "sub_category": "辛空间",
 "concept": "辛形式与保持变换", "concept_id": "C44",
 "parent_training_ids": ["linalg-070"],
 "problem": r"在 $\mathbb R^3$ 上定义 $\omega(u,v)=(u\times v)\cdot e_1$($e_1=(1,0,0)$)。验证 $\omega$ 是交替的，并说明它不是辛形式(退化)。",
 "solution": r"交替性:$\omega(v,u)=(v\times u)\cdot e_1=-(u\times v)\cdot e_1=-\omega(u,v)$(叉积反交换),故交替。退化性:$\omega$ 的核为 $\{u:\omega(u,v)=0,\ \forall v\}$。对 $u=e_1$,$\omega(e_1,v)=(e_1\times v)\cdot e_1=0$(叉积垂直于 $e_1$),对一切 $v$ 成立,故 $e_1$ 在核中,核非零,即 $\omega$ 退化。因此 $\omega$ 只是交替双线性形式,不是辛形式(辛形式要求非退化,且只能存在于偶数维空间)。",
 "answer": r"$\omega$ 交替(叉积反交换)但退化($e_1$ 在核中),不是辛形式。",
 "method": "交替性验证+退化判定",
 "difficulty": "中等",
 "variant_kind": "退化交替形式与反例:三维交叉分量的退化性分析",
 "scene_spec": {
  "objects": [
   "三维坐标系:$e_1$ 与叉积 $e_1\\times v$ 的垂直关系示意",
   "板书:交替性的反交换验证",
   "板书:核含 $e_1$ 的验证",
   "红色标签「退化,非辛形式」"
  ],
  "steps": [
   "第一步:验证交替性。",
   "第二步:检验 $e_1$ 与所有向量的配对。",
   "第三步:展示 $e_1\\times v\\perp e_1$。",
   "第四步:得核非零、形式退化。",
   "第五步:说明辛形式须非退化,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c44-05", "category": "高等代数", "sub_category": "辛空间",
 "concept": "辛形式与保持变换", "concept_id": "C44",
 "parent_training_ids": ["linalg-070"],
 "problem": r"证明:在数域(特征不为 $2$)上的奇数维线性空间中,不存在非退化的交替双线性形式。",
 "solution": r"设 $V$ 为 $n$ 维空间,$\omega$ 为交替双线性形式,在取定一组基后由斜对称矩阵 $A$ 表示($A^{\mathsf T}=-A$)。$\omega$ 非退化当且仅当 $A$ 可逆。但若 $n$ 为奇数,$\det A=\det(A^{\mathsf T})=\det(-A)=(-1)^n\det A=-\det A$,故 $\det A=0$,$A$ 奇异,即 $\omega$ 必退化。故奇数维空间不存在非退化的交替双线性形式(辛形式只存在于偶数维空间)。",
 "answer": r"证明见解法(斜对称矩阵:$\det A=(-1)^n\det A$,奇数维时行列式为零)。",
 "method": "奇数维退化性证明(斜对称行列式)",
 "difficulty": "进阶",
 "variant_kind": "证明型:奇数维无非退化交替形式的行列式论证",
 "scene_spec": {
  "objects": [
   "板书:斜对称矩阵 $A^{\\mathsf T}=-A$",
   "板书:$\\det A=\\det(-A)=(-1)^n\\det A$ 的推导",
   "高亮框:奇数维时 $\\det A=0$",
   "标签「辛空间必为偶数维」"
  ],
  "steps": [
   "第一步:写出交替形式的矩阵表示。",
   "第二步:由斜对称性推导行列式关系。",
   "第三步:奇数维时得行列式为零。",
   "第四步:说明非退化要求行列式非零。",
   "第五步:高亮结论,完成证明。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
# ===================== C45 条件概率与独立性 =====================
{
 "id": "draft-c45-01", "category": "概率论", "sub_category": "条件概率",
 "concept": "条件概率与独立性", "concept_id": "C45",
 "parent_training_ids": ["prob-038"],
 "problem": r"证明:若 $A,B$ 相互独立且 $P(A)>0,P(B)>0$，则 $A,B$ 不互斥；若 $A,B$ 互斥且概率均为正，则 $A,B$ 不独立。",
 "solution": r"第一部分:独立给出 $P(A\cap B)=P(A)P(B)>0$(两正数之积),故 $A\cap B\neq\varnothing$,不互斥。第二部分:互斥给出 $P(A\cap B)=0$,而 $P(A)P(B)>0$,故 $P(A\cap B)\neq P(A)P(B)$,不独立(等价地 $P(A|B)=0\neq P(A)$)。结论:独立与互斥是两个不同的概念——独立是概率乘积关系,互斥是集合不相交关系;除退化情形(零概率事件)外两者互斥。",
 "answer": r"证明见解法(独立⟹交概率为正⟹不互斥;互斥⟹交概率为零⟹不独立)。",
 "method": "定义对照证明(独立与互斥辨析)",
 "difficulty": "基础",
 "variant_kind": "独立与互斥辨析:两概念的严格互斥性论证",
 "scene_spec": {
  "objects": [
   "两个韦恩图:相交(独立,阴影交区域)与相离(互斥)",
   "板书:$P(A\\cap B)=P(A)P(B)>0$ 与 $P(A\\cap B)=0$ 的对照",
   "高亮框:「独立≠互斥」"
  ],
  "steps": [
   "第一步:画出相交与相离两种韦恩图。",
   "第二步:由独立推交概率为正。",
   "第三步:由互斥推交概率为零。",
   "第四步:对照两个结论。",
   "第五步:高亮总结。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c45-02", "category": "概率论", "sub_category": "条件概率",
 "concept": "条件概率与独立性", "concept_id": "C45",
 "parent_training_ids": ["prob-038"],
 "problem": r"用乘法公式(链式法则)求 $P(A\cap B\cap C)$，其中 $P(A)=\frac12$，$P(B|A)=\frac35$，$P(C|A\cap B)=\frac45$。",
 "solution": r"链式法则:$P(A\cap B\cap C)=P(A)\cdot P(B|A)\cdot P(C|A\cap B)=\frac12\times\frac35\times\frac45=\frac{6}{25}$。",
 "answer": r"$P(A\cap B\cap C)=\frac{6}{25}$。",
 "method": "链式法则(乘法公式)",
 "difficulty": "基础",
 "variant_kind": "三事件条件化:链式法则的分数计算",
 "scene_spec": {
  "objects": [
   "三层概率树:A → B|A → C|A∩B",
   "板书:链式法则公式与代入",
   "高亮框:$\\frac{6}{25}$"
  ],
  "steps": [
   "第一步:画出三层概率树。",
   "第二步:写出链式法则。",
   "第三步:代入分数并相乘。",
   "第四步:高亮结果。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c45-03", "category": "概率论", "sub_category": "条件概率",
 "concept": "条件概率与独立性", "concept_id": "C45",
 "parent_training_ids": ["prob-038"],
 "problem": r"抛两枚均匀硬币。记 $A=${第一枚正面},$B=${第二枚正面},$C=${两枚同面}。证明 $A,B,C$ 两两独立但整体不独立。",
 "solution": r"$P(A)=P(B)=P(C)=\frac12$。$P(A\cap B)=P(\text{两枚皆正})=\frac14=P(A)P(B)$ ✓。$P(A\cap C)=P(A\cap\text{两枚同面})=P(\text{两枚皆正})=\frac14=P(A)P(C)$ ✓。$P(B\cap C)=\frac14=P(B)P(C)$ ✓。故两两独立。但 $P(A\cap B\cap C)=P(\text{两枚皆正})=\frac14\neq\frac18=P(A)P(B)P(C)$,故整体不独立。",
 "answer": r"两两独立($P(A\cap B)=P(A\cap C)=P(B\cap C)=\frac14$),但 $P(A\cap B\cap C)=\frac14\neq\frac18$,整体不独立。",
 "method": "两两独立与整体独立的对照验证",
 "difficulty": "中等",
 "variant_kind": "三事件条件化:两两独立但不整体独立的经典反例",
 "scene_spec": {
  "objects": [
   "两枚硬币的四种结果表(正正/正反/反正/反反)",
   "三个事件的集合高亮",
   "板书:三个两两交的概率核对",
   "高亮框:交 $\\frac14\\neq\\frac18$ 的整体独立失败"
  ],
  "steps": [
   "第一步:列出四种等可能结果。",
   "第二步:核对三个两两交的概率。",
   "第三步:得两两独立。",
   "第四步:计算三事件交并对照乘积。",
   "第五步:高亮整体独立失败的结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c45-04", "category": "概率论", "sub_category": "条件概率",
 "concept": "条件概率与独立性", "concept_id": "C45",
 "parent_training_ids": ["prob-038"],
 "problem": r"说明是否存在满足 $P(A|B)=\frac{9}{10}$，$P(A|\bar B)=\frac45$，且 $P(A)=\frac{1}{10}$ 的事件 $A,B$($0<P(B)<1$)；并说明一般情形下 $P(A)$ 必须满足什么约束。",
 "solution": r"由全概率公式,$P(A)=P(A|B)P(B)+P(A|\bar B)P(\bar B)$,是 $\frac{9}{10}$ 与 $\frac45$ 的凸组合,故必满足 $\frac45\le P(A)\le\frac{9}{10}$。题设 $P(A)=\frac{1}{10}$ 落在此区间之外,故不存在这样的事件。一般约束:给定 $P(A|B)$ 与 $P(A|\bar B)$ 时,$P(A)$ 必须是两者的凸组合,即介于两者之间;数据不满足此约束时自相矛盾,不可实现。",
 "answer": r"不存在:全概率公式要求 $P(A)$ 为 $\frac45$ 与 $\frac{9}{10}$ 的凸组合(介于两者之间),而 $\frac{1}{10}$ 不在其中。",
 "method": "全概率公式的自洽性约束",
 "difficulty": "中等",
 "variant_kind": "不相容数据的可行性:条件概率数据的自洽性检验",
 "scene_spec": {
  "objects": [
   "数轴:区间 $[\\frac45,\\frac{9}{10}]$(凸组合范围)高亮",
   "数轴:题设值 $\\frac{1}{10}$ 在区间之外(红色叉号)",
   "板书:全概率公式与凸组合解释",
   "高亮框:「数据自相矛盾,不可实现」"
  ],
  "steps": [
   "第一步:写出全概率公式。",
   "第二步:说明 $P(A)$ 是两条件概率的凸组合。",
   "第三步:在数轴上标出可行区间。",
   "第四步:标出题设值在区间外。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c45-05", "category": "概率论", "sub_category": "条件概率",
 "concept": "条件概率与独立性", "concept_id": "C45",
 "parent_training_ids": ["prob-038"],
 "problem": r"证明:给定事件 $B$($P(B)>0$)，条件概率 $P(\cdot|B)$ 是样本空间上的概率测度，并推导全概率公式。",
 "solution": r"验证概率公理:非负性:对任意 $A$,$P(A|B)=\frac{P(A\cap B)}{P(B)}\ge0$。归一性:$P(\Omega|B)=\frac{P(\Omega\cap B)}{P(B)}=\frac{P(B)}{P(B)}=1$。可列可加性:设 $A_1,A_2,\dots$ 两两互斥,则 $P\left(\bigcup_i A_i\,\middle|\,B\right)=\frac{P(\bigcup_i(A_i\cap B))}{P(B)}=\frac{\sum_i P(A_i\cap B)}{P(B)}=\sum_i P(A_i|B)$(用到 $P$ 的可列可加性)。故 $P(\cdot|B)$ 是概率测度。全概率公式:设 $B_1,\dots,B_n$ 构成完备事件组(两两互斥且并为 $\Omega$,$P(B_i)>0$),则 $P(A)=\sum_i P(A\cap B_i)=\sum_i P(A|B_i)P(B_i)$。",
 "answer": r"证明见解法(非负/归一/可列可加三公理验证;全概率公式由完备事件组分解得)。",
 "method": "条件概率的测度性质证明",
 "difficulty": "进阶",
 "variant_kind": "证明型:条件概率构成概率测度的公理验证与全概率公式推导",
 "scene_spec": {
  "objects": [
   "板书:三条公理的逐项验证",
   "韦恩图:完备事件组对 $A$ 的划分",
   "板书:全概率公式的推导",
   "高亮框:$P(A)=\\sum_i P(A|B_i)P(B_i)$"
  ],
  "steps": [
   "第一步:验证非负性与归一性。",
   "第二步:验证可列可加性。",
   "第三步:画出完备事件组划分。",
   "第四步:推导全概率公式。",
   "第五步:高亮结论,完成证明。"
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
