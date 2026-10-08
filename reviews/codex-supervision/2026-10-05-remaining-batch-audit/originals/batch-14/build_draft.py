"""batch-14 生成器:三个单条考点各 5 题
(C34 初等矩阵与操作 / C38 子空间和与交 / C39 线性映射核与像)。
全部数学结论由作者逐题手工验算(见 DRAFT_REPORT.md 核算说明);
起草过程未读 eval/test 题文或答案作提示;凡有理数一律分数。
"""
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "draft.jsonl"

DATA = [
# ===================== C34 初等矩阵与操作 =====================
{
 "id": "draft-c34-01", "category": "高等代数", "sub_category": "矩阵",
 "concept": "初等矩阵与操作", "concept_id": "C34",
 "parent_training_ids": ["linalg-058"],
 "problem": r"设 $E=\begin{pmatrix}1&0&0\\0&1&0\\0&0&5\end{pmatrix}$。说明用 $E$ 左乘与右乘一个 $3$ 阶矩阵 $A$ 分别对 $A$ 做了什么操作。",
 "solution": r"左乘 $EA$:把 $A$ 的第三行乘以 $5$(其余行不变)。右乘 $AE$:把 $A$ 的第三列乘以 $5$(其余列不变)。$E$ 是由单位矩阵把第三行(列)乘以 $5$ 得到的倍乘型初等矩阵。",
 "answer": r"左乘:第三行乘 $5$;右乘:第三列乘 $5$。",
 "method": "初等矩阵的左乘右乘作用辨析",
 "difficulty": "基础",
 "variant_kind": "左乘与右乘:同一初等矩阵两侧作用的区分(与几何意义父题不同)",
 "scene_spec": {
  "objects": [
   "板书:$A$(示意 3x3 矩阵)与 $E=\\mathrm{diag}(1,1,5)$",
   "动画:$EA$ 的第三行整体乘 $5$(行高亮)",
   "动画:$AE$ 的第三列整体乘 $5$(列高亮)",
   "对照框:「左乘改行,右乘改列」"
  ],
  "steps": [
   "第一步:写出 $E$ 与示意矩阵 $A$。",
   "第二步:动画展示左乘对第三行的作用。",
   "第三步:动画展示右乘对第三列的作用。",
   "第四步:对照总结左乘改行、右乘改列。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c34-02", "category": "高等代数", "sub_category": "矩阵",
 "concept": "初等矩阵与操作", "concept_id": "C34",
 "parent_training_ids": ["linalg-058"],
 "problem": r"构造把 $3$ 阶矩阵的第二行加到第一行的初等矩阵 $E$，并求 $E^{-1}$ 与 $E^{-1}$ 对应的操作。",
 "solution": r"把第二行加到第一行的初等矩阵为 $E=\begin{pmatrix}1&1&0\\0&1&0\\0&0&1\end{pmatrix}$(左乘 $EA$ 即第一行加第二行)。其逆为把第一行减去第二行:$E^{-1}=\begin{pmatrix}1&-1&0\\0&1&0\\0&0&1\end{pmatrix}$。验证:$EE^{-1}=I$(第一行:$(1,1,0)$ 减第二行 $(0,1,0)$ 得 $(1,0,0)$)。",
 "answer": r"$E=\begin{pmatrix}1&1&0\\0&1&0\\0&0&1\end{pmatrix}$;$E^{-1}=\begin{pmatrix}1&-1&0\\0&1&0\\0&0&1\end{pmatrix}$,对应「第一行减第二行」。",
 "method": "倍加型初等矩阵构造与求逆",
 "difficulty": "基础",
 "variant_kind": "构造+逆操作:倍加型初等矩阵的构造与逆操作对应",
 "scene_spec": {
  "objects": [
   "板书:单位矩阵与目标操作「第一行加第二行」",
   "板书:$E$ 的构造过程",
   "板书:$E^{-1}$ 与逆操作「第一行减第二行」",
   "验证板书:$EE^{-1}=I$"
  ],
  "steps": [
   "第一步:写出目标行操作。",
   "第二步:由单位矩阵构造 $E$。",
   "第三步:推导逆矩阵 $E^{-1}$。",
   "第四步:说明逆操作。",
   "第五步:验证乘积为单位矩阵。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c34-03", "category": "高等代数", "sub_category": "矩阵",
 "concept": "初等矩阵与操作", "concept_id": "C34",
 "parent_training_ids": ["linalg-058"],
 "problem": r"设 $P_1$ 是交换第一、二行的初等矩阵，$P_2$ 是把第一行乘以 $2$ 的初等矩阵。求先交换第一、二行、再把新第一行乘以 $2$ 的复合初等矩阵。",
 "solution": r"$P_1=\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}$,$P_2=\begin{pmatrix}2&0&0\\0&1&0\\0&0&1\end{pmatrix}$。先做 $P_1$ 后做 $P_2$ 对应左乘 $P_2P_1$(先作用的矩阵写在右边):$P_2P_1=\begin{pmatrix}2&0&0\\0&1&0\\0&0&1\end{pmatrix}\begin{pmatrix}0&1&0\\1&0&0\\0&0&1\end{pmatrix}=\begin{pmatrix}0&2&0\\1&0&0\\0&0&1\end{pmatrix}$。复合矩阵把第二行换到第一行并乘以 $2$。",
 "answer": r"复合初等矩阵为 $\begin{pmatrix}0&2&0\\1&0&0\\0&0&1\end{pmatrix}$。",
 "method": "操作顺序与矩阵乘积次序",
 "difficulty": "中等",
 "variant_kind": "操作顺序:复合初等矩阵的乘积次序(先作用者居右)",
 "scene_spec": {
  "objects": [
   "板书:$P_1$ 与 $P_2$ 的矩阵",
   "动画:先交换第一二行,再把新第一行乘 $2$",
   "板书:矩阵乘法 $P_2P_1$ 的计算",
   "高亮框:复合矩阵"
  ],
  "steps": [
   "第一步:写出两个初等矩阵。",
   "第二步:动画展示两步操作的先后顺序。",
   "第三步:说明先作用者写在右边。",
   "第四步:完成矩阵乘法。",
   "第五步:高亮复合矩阵,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c34-04", "category": "高等代数", "sub_category": "矩阵",
 "concept": "初等矩阵与操作", "concept_id": "C34",
 "parent_training_ids": ["linalg-058"],
 "problem": r"把矩阵 $A=\begin{pmatrix}2&2\\0&1\end{pmatrix}$ 分解为初等矩阵的乘积。",
 "solution": r"对 $A$ 作行变换化单位阵:第一步第一行乘以 $\frac12$,对应初等矩阵 $E_1'=\begin{pmatrix}\frac12&0\\0&1\end{pmatrix}$,$E_1'A=\begin{pmatrix}1&1\\0&1\end{pmatrix}$;第二步第一行减去第二行,对应 $E_2'=\begin{pmatrix}1&-1\\0&1\end{pmatrix}$,$E_2'E_1'A=I$。故 $A=E_1'^{-1}E_2'^{-1}$。求逆:$E_1'^{-1}=\begin{pmatrix}2&0\\0&1\end{pmatrix}$(第一行乘 $2$),$E_2'^{-1}=\begin{pmatrix}1&1\\0&1\end{pmatrix}$(第一行加第二行)。故 $A=\begin{pmatrix}2&0\\0&1\end{pmatrix}\begin{pmatrix}1&1\\0&1\end{pmatrix}$。验证:乘积 $=\begin{pmatrix}2&2\\0&1\end{pmatrix}=A$ ✓。",
 "answer": r"$A=\begin{pmatrix}2&0\\0&1\end{pmatrix}\begin{pmatrix}1&1\\0&1\end{pmatrix}$,两个初等矩阵之积。",
 "method": "消元步骤反推分解",
 "difficulty": "中等",
 "variant_kind": "矩阵分解:可逆矩阵的初等矩阵乘积分解",
 "scene_spec": {
  "objects": [
   "板书:$A$ 与目标分解",
   "动画:第一步行变换(第一行加第二行)",
   "动画:第二步行变换(第一行乘 2)",
   "板书:两步初等矩阵的乘积验证"
  ],
  "steps": [
   "第一步:写出 $A$,规划行变换步骤。",
   "第二步:动画展示第一步变换与对应初等矩阵。",
   "第三步:动画展示第二步变换。",
   "第四步:验证两个初等矩阵的乘积等于 $A$。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c34-05", "category": "高等代数", "sub_category": "矩阵",
 "concept": "初等矩阵与操作", "concept_id": "C34",
 "parent_training_ids": ["linalg-058"],
 "problem": r"证明三类初等矩阵都可逆，并分别求其行列式；由此说明任意可逆矩阵可以表示为初等矩阵的乘积。",
 "solution": r"三类初等矩阵及其逆:交换型 $P_{ij}$($P_{ij}^{-1}=P_{ij}$,行列式 $-1$);倍乘型 $D_i(k)$($k\neq0$,$D_i(k)^{-1}=D_i(\frac1k)$,行列式 $k$);倍加型 $E_{ij}(k)$(第 $j$ 行乘 $k$ 加到第 $i$ 行,$E_{ij}(k)^{-1}=E_{ij}(-k)$,行列式 $1$)。均可逆。任意可逆矩阵:$A$ 可逆 ⟺ $A$ 的行阶梯形经行变换可化为单位矩阵(主元均非零),即存在初等矩阵 $E_1,\dots,E_m$ 使 $E_m\cdots E_1A=I$,故 $A=E_1^{-1}\cdots E_m^{-1}$,而初等矩阵的逆仍是初等矩阵,故 $A$ 是初等矩阵的乘积。",
 "answer": r"交换型:$P_{ij}^{-1}=P_{ij}$,$\det=-1$;倍乘型:$D_i(k)^{-1}=D_i(\frac1k)$,$\det=k$;倍加型:$E_{ij}(k)^{-1}=E_{ij}(-k)$,$\det=1$;可逆矩阵可化为 $I$ 故可表为初等矩阵之积(证明见解法)。",
 "method": "分类证明(三类初等矩阵的性质)",
 "difficulty": "进阶",
 "variant_kind": "证明型:初等矩阵可逆性、行列式与可逆矩阵分解的系统证明",
 "scene_spec": {
  "objects": [
   "三列表格:三类初等矩阵、逆矩阵、行列式",
   "板书:消元过程 $E_m\\cdots E_1A=I$ 的推导",
   "高亮框:$A=E_1^{-1}\\cdots E_m^{-1}$",
   "标签「可逆 ⟺ 可化为单位矩阵」"
  ],
  "steps": [
   "第一步:列出三类初等矩阵并分别求逆。",
   "第二步:分别计算三类矩阵的行列式。",
   "第三步:展示可逆矩阵消元化为单位矩阵的过程。",
   "第四步:两边左乘逆矩阵得分解式。",
   "第五步:高亮结论,完成证明。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
# ===================== C38 子空间和与交 =====================
{
 "id": "draft-c38-01", "category": "高等代数", "sub_category": "线性空间",
 "concept": "子空间和与交", "concept_id": "C38",
 "parent_training_ids": ["linalg-062"],
 "problem": r"设 $W_1=\mathrm{span}\{(1,0,0),(0,1,0)\}$，$W_2=\mathrm{span}\{(0,0,1)\}$。求 $\dim(W_1+W_2)$ 与 $\dim(W_1\cap W_2)$，并判断该和是否为直和。",
 "solution": r"$W_1\cap W_2=\{0\}$(两子空间的生成元合在一起为 $(1,0,0),(0,1,0),(0,0,1)$,线性无关)。故 $\dim(W_1\cap W_2)=0$,$\dim(W_1+W_2)=2+1-0=3$,且 $W_1+W_2=\mathbb R^3$。由于 $W_1\cap W_2=\{0\}$,该和为直和:$W_1\oplus W_2=\mathbb R^3$。",
 "answer": r"$\dim(W_1+W_2)=3$,$\dim(W_1\cap W_2)=0$,是直和。",
 "method": "维数公式+直和判定",
 "difficulty": "基础",
 "variant_kind": "直和情形:交为零的子空间和与直和判定(与相交父题不同)",
 "scene_spec": {
  "objects": [
   "三维示意图:xy 平面与 z 轴(两子空间)",
   "标注:交为原点,和为全空间",
   "板书:维数公式 $3=2+1-0$",
   "高亮框:「直和」"
  ],
  "steps": [
   "第一步:画出两个子空间。",
   "第二步:说明交仅含零向量。",
   "第三步:由维数公式得和的维数。",
   "第四步:判断直和。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c38-02", "category": "高等代数", "sub_category": "线性空间",
 "concept": "子空间和与交", "concept_id": "C38",
 "parent_training_ids": ["linalg-062"],
 "problem": r"设 $W_1=\mathrm{span}\{(1,1,0),(0,1,1)\}$，$W_2=\mathrm{span}\{(1,0,1),(0,1,1)\}$。求 $W_1\cap W_2$ 的一组基与 $\dim(W_1+W_2)$。",
 "solution": r"设 $v\in W_1\cap W_2$:$v=a(1,1,0)+b(0,1,1)=c(1,0,1)+d(0,1,1)$。按分量比较:$a=c$,$a+b=d$,$b=c+d$。由 $a=c$ 与 $b=c+d$ 得 $b=a+d$;与 $a+b=d$ 联立得 $2a=0$,即 $a=c=0$,$b=d$。故 $v=b(0,1,1)$,$W_1\cap W_2=\mathrm{span}\{(0,1,1)\}$,$\dim=1$。维数公式:$\dim(W_1+W_2)=2+2-1=3$。",
 "answer": r"$W_1\cap W_2=\mathrm{span}\{(0,1,1)\}$(维数 $1$);$\dim(W_1+W_2)=3$。",
 "method": "交集基求解+维数公式",
 "difficulty": "基础",
 "variant_kind": "交集基构造:两平面子空间交线的基求解",
 "scene_spec": {
  "objects": [
   "三维示意图:两个过原点的平面相交于一条直线",
   "交集直线高亮(方向 $(0,1,1)$)",
   "板书:线性组合相等与分量比较",
   "高亮框:$\\dim(W_1\\cap W_2)=1$,$\\dim(W_1+W_2)=3$"
  ],
  "steps": [
   "第一步:画出两个平面子空间。",
   "第二步:设交向量为两边的线性组合并比较分量。",
   "第三步:解出交为一条直线。",
   "第四步:高亮交线,由维数公式求和维数。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c38-03", "category": "高等代数", "sub_category": "线性空间",
 "concept": "子空间和与交", "concept_id": "C38",
 "parent_training_ids": ["linalg-062"],
 "problem": r"设 $U=\mathrm{span}\{(1,2,3),(0,1,1)\}$，$V=\mathrm{span}\{(1,0,1),(0,1,0),(1,1,1)\}$。求 $\dim U$、$\dim V$、$\dim(U\cap V)$ 与 $\dim(U+V)$。",
 "solution": r"$\dim U=2$($(1,2,3)$ 与 $(0,1,1)$ 线性无关)。$V$ 的生成元中 $(1,1,1)=(1,0,1)+(0,1,0)$,故 $V=\mathrm{span}\{(1,0,1),(0,1,0)\}=\{(p,q,p)\}$,$\dim V=2$。求 $U\cap V$:设 $v\in U$,$v=a(1,2,3)+b(0,1,1)=(a,2a+b,3a+b)$。$v\in V$ 当且仅当第一分量等于第三分量:$a=3a+b$,即 $2a+b=0$,$b=-2a$。此时 $v=(a,0,a)=a(1,0,1)$。故 $U\cap V=\mathrm{span}\{(1,0,1)\}$,$\dim(U\cap V)=1$。验证:$(1,0,1)=1\cdot(1,2,3)+(-2)\cdot(0,1,1)\in U$ ✓。维数公式:$\dim(U+V)=2+2-1=3$。",
 "answer": r"$\dim U=2$,$\dim V=2$,$\dim(U\cap V)=1$($U\cap V=\mathrm{span}\{(1,0,1)\}$),$\dim(U+V)=3$。",
 "method": "生成元化简+交集基+维数公式",
 "difficulty": "中等",
 "variant_kind": "不同维数组合:含冗余生成元的子空间化简与交集求解",
 "scene_spec": {
  "objects": [
   "板书:$V$ 的生成元线性关系((1,1,1) 为前两者之和)",
   "板书:交集方程的求解过程",
   "高亮框:四问的维数结果",
   "三维示意图:两平面子空间的交线"
  ],
  "steps": [
   "第一步:化简 $V$ 的生成元,得各子空间维数。",
   "第二步:写出 $U$ 中向量的一般形式。",
   "第三步:代入 $V$ 的成员条件,解交集。",
   "第四步:由维数公式求和维数。",
   "第五步:高亮四个维数结果。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c38-04", "category": "高等代数", "sub_category": "线性空间",
 "concept": "子空间和与交", "concept_id": "C38",
 "parent_training_ids": ["linalg-062"],
 "problem": r"设 $U,V$ 是 $\mathbb R^5$ 的子空间，$\dim U=3$，$\dim V=2$。求 $\dim(U\cap V)$ 的可能取值范围，并说明每种取值对应的 $\dim(U+V)$。",
 "solution": r"由维数公式 $\dim(U+V)=\dim U+\dim V-\dim(U\cap V)=5-\dim(U\cap V)$。而 $U+V\subseteq\mathbb R^5$,故 $\dim(U+V)\le5$,即 $\dim(U\cap V)\ge0$;又 $\dim(U\cap V)\le\min(\dim U,\dim V)=2$。故 $\dim(U\cap V)$ 的可能取值为 $0,1,2$,对应的 $\dim(U+V)$ 分别为 $5,4,3$。三种情形均可实现:直和(交为 $0$)、交一条直线、$V\subseteq U$(交为 $V$)。",
 "answer": r"$\dim(U\cap V)\in\{0,1,2\}$,对应 $\dim(U+V)=5,4,3$。",
 "method": "维数公式的约束范围分析",
 "difficulty": "中等",
 "variant_kind": "约束变化:维数公式导出的交集维数取值范围讨论",
 "scene_spec": {
  "objects": [
   "板书:维数公式 $\\dim(U+V)=5-\\dim(U\\cap V)$",
   "数轴:$\\dim(U\\cap V)$ 的取值 $0,1,2$ 标注",
   "三种情形示意:直和、交线、包含",
   "高亮框:取值与对应和维数"
  ],
  "steps": [
   "第一步:写出维数公式。",
   "第二步:由和的维数上界与交的上界确定范围。",
   "第三步:展示三种可实现情形。",
   "第四步:列出每种取值对应的和维数。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c38-05", "category": "高等代数", "sub_category": "线性空间",
 "concept": "子空间和与交", "concept_id": "C38",
 "parent_training_ids": ["linalg-062"],
 "problem": r"证明维数公式:若 $U,V$ 是有限维线性空间 $W$ 的子空间，则 $\dim(U+V)=\dim U+\dim V-\dim(U\cap V)$。",
 "solution": r"取 $U\cap V$ 的一组基 $u_1,\dots,u_k$($k=\dim(U\cap V)$)。把它分别延拓为 $U$ 的基 $u_1,\dots,u_k,p_1,\dots,p_r$ 与 $V$ 的基 $u_1,\dots,u_k,q_1,\dots,q_s$(其中 $r=\dim U-k$,$s=\dim V-k$)。下证向量组 $u_1,\dots,u_k,p_1,\dots,p_r,q_1,\dots,q_s$ 是 $U+V$ 的一组基。张成:任意 $w\in U+V$ 可写为 $w=u+v$($u\in U,v\in V$),两者均可由上述向量组线性表出,故整个组张成 $U+V$。线性无关:设 $(\sum\alpha_iu_i+\sum\beta_jp_j)+(\sum\alpha_i'u_i+\sum\gamma_lq_l)=0$,令 $x=\sum\alpha_iu_i+\sum\beta_jp_j\in U$,则 $x=-\sum\alpha_i'u_i-\sum\gamma_lq_l\in V$,故 $x\in U\cap V$。于是 $x$ 可仅由 $u_1,\dots,u_k$ 表出,但 $x$ 作为 $U$ 中元素用 $U$ 的基表示唯一,故 $\beta_j=0$;同理 $\gamma_l=0$,回代得 $\sum(\alpha_i+\alpha_i')u_i=0$,由线性无关得 $\alpha_i+\alpha_i'=0$。于是该向量组线性无关。故 $\dim(U+V)=k+r+s=(k+r)+(k+s)-k=\dim U+\dim V-\dim(U\cap V)$。",
 "answer": r"证明见解法(交的基延拓为两子空间的基,拼接组构成 $U+V$ 的基)。",
 "method": "基延拓法证明维数公式",
 "difficulty": "进阶",
 "variant_kind": "证明型:维数公式的基延拓严格证明",
 "scene_spec": {
  "objects": [
   "板书:$U\\cap V$ 的基与分别延拓示意图",
   "板书:拼接向量组张成 $U+V$ 的论证",
   "板书:线性无关性(交向量双重表示唯一)的论证",
   "高亮框:$\\dim(U+V)=\\dim U+\\dim V-\\dim(U\\cap V)$"
  ],
  "steps": [
   "第一步:取交的基并延拓到两子空间。",
   "第二步:证明拼接组张成 $U+V$。",
   "第三步:证明拼接组线性无关。",
   "第四步:计数得维数公式。",
   "第五步:高亮结论,完成证明。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
# ===================== C39 线性映射核与像 =====================
{
 "id": "draft-c39-01", "category": "高等代数", "sub_category": "线性映射",
 "concept": "线性映射核与像", "concept_id": "C39",
 "parent_training_ids": ["linalg-063"],
 "problem": r"设线性变换 $T:\mathbb R^3\to\mathbb R^3$ 由 $T(x,y,z)=(x-y,\,y-z,\,z-x)$ 定义。求 $T$ 的核、像与各自的维数。",
 "solution": r"核:解 $x-y=0,y-z=0,z-x=0$,得 $x=y=z$,故 $\ker T=\mathrm{span}\{(1,1,1)\}$,$\dim\ker T=1$。像:由秩-零度定理 $\dim\mathrm{im}\,T=3-1=2$。像的方程:三个分量之和 $(x-y)+(y-z)+(z-x)=0$,故像包含于平面 $u+v+w=0$;两者维数均为 $2$,故 $\mathrm{im}\,T=\{u+v+w=0\}$。",
 "answer": r"$\\ker T=\\mathrm{span}\\{(1,1,1)\\}$(维数 $1$);$\\mathrm{im}\\,T=\\{u+v+w=0\\}$(维数 $2$)。",
 "method": "解核方程+秩零度定像",
 "difficulty": "基础",
 "variant_kind": "数值结构变化:三变量循环差的核与像(与 R³→R² 父题不同)",
 "scene_spec": {
  "objects": [
   "三维示意图:直线 $x=y=z$(核,红色)与平面 $u+v+w=0$(像,蓝色)",
   "板书:核方程的求解",
   "板书:像的方程与维数推导",
   "高亮框:核维数 $1$,像维数 $2$"
  ],
  "steps": [
   "第一步:解核方程,得对角线直线。",
   "第二步:高亮核。",
   "第三步:推导像的方程与维数。",
   "第四步:高亮像平面。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c39-02", "category": "高等代数", "sub_category": "线性映射",
 "concept": "线性映射核与像", "concept_id": "C39",
 "parent_training_ids": ["linalg-063"],
 "problem": r"设 $T:\mathbb R^2\to\mathbb R^3$ 由 $T(x,y)=(x+y,\,x-y,\,2x)$ 定义。判断 $T$ 是否单射、是否满射，并求核与像的维数。",
 "solution": r"核:解 $x+y=0,x-y=0,2x=0$,得 $x=y=0$,故 $\ker T=\{0\}$,$\dim\ker T=0$,由秩-零度定理 $\dim\mathrm{im}\,T=2-0=2$。单射:核为 $\{0\}$ ⟺ 单射,故 $T$ 单射。满射:像的维数 $2<3$,故 $T$ 非满射(像是 $\mathbb R^3$ 中由 $T(1,0)=(1,1,2)$ 与 $T(0,1)=(1,-1,0)$ 张成的平面)。",
 "answer": r"单射但非满射;$\\ker T=\\{0\\}$(维数 $0$),$\\dim\\mathrm{im}\\,T=2$。",
 "method": "单射满射判定(核与秩零度)",
 "difficulty": "基础",
 "variant_kind": "单射/非满射:低维到高维映射的单射性与非满射性判定",
 "scene_spec": {
  "objects": [
   "三维示意图:平面像(由两个像向量张成)与原点",
   "板书:核方程求解(仅零解)",
   "板书:秩零度 $\\dim\\mathrm{im}=2$",
   "高亮框:「单射,非满射」"
  ],
  "steps": [
   "第一步:解核方程,得核为零。",
   "第二步:由秩零度得像维数 $2$。",
   "第三步:画出像平面。",
   "第四步:判断单射(核零)与非满射(像维数<3)。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c39-03", "category": "高等代数", "sub_category": "线性映射",
 "concept": "线性映射核与像", "concept_id": "C39",
 "parent_training_ids": ["linalg-063"],
 "problem": r"在实数域上次数不超过 $2$ 的多项式空间 $V$ 上定义微分映射 $D(p)=p'$。求 $D$ 的核、像与各自的维数，并验证秩-零度定理。",
 "solution": r"$V=\{a_0+a_1x+a_2x^2\}$,$\dim V=3$。核:$p'=0\iff p$ 为常数多项式,故 $\ker D=\mathrm{span}\{1\}$,$\dim\ker D=1$。像:$D(a_0+a_1x+a_2x^2)=a_1+2a_2x$,像为次数不超过 $1$ 的多项式全体,$\dim\mathrm{im}\,D=2$。秩-零度:$1+2=3=\dim V$ ✓。",
 "answer": r"$\\ker D=\\mathrm{span}\\{1\\}$(常数多项式,维数 $1$);$\\mathrm{im}\\,D=$ 次数不超过 $1$ 的多项式全体(维数 $2$);$1+2=3$ 满足秩-零度。",
 "method": "抽象空间微分映射的核与像",
 "difficulty": "中等",
 "variant_kind": "多项式微分映射:抽象空间上的核与像及秩零度验证",
 "scene_spec": {
  "objects": [
   "板书:$V$ 的基 $\\{1,x,x^2\\}$ 与微分作用",
   "动画:各基向量经微分后的像(1→0,x→1,x²→2x)",
   "板书:核(常数)与像(一次多项式)的维数",
   "高亮框:秩-零度 $1+2=3$"
  ],
  "steps": [
   "第一步:写出空间与基。",
   "第二步:动画展示基向量的微分像。",
   "第三步:确定核为常数多项式。",
   "第四步:确定像为一次多项式全体。",
   "第五步:验证秩-零度,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c39-04", "category": "高等代数", "sub_category": "线性映射",
 "concept": "线性映射核与像", "concept_id": "C39",
 "parent_training_ids": ["linalg-063"],
 "problem": r"设 $T:\mathbb R^3\to\mathbb R^3$ 由 $T(x,y,z)=(x+y,\,y+z,\,0)$ 定义。求 $T^2$ 的表达式，并比较 $T$ 与 $T^2$ 的核与像。",
 "solution": r"$T^2(x,y,z)=T(x+y,\,y+z,\,0)=((x+y)+(y+z),\,(y+z)+0,\,0)=(x+2y+z,\,y+z,\,0)$。核:$T$ 的核:$x+y=0,y+z=0$,得 $(x,-x,x)$,$\ker T=\mathrm{span}\{(1,-1,1)\}$。$T^2$ 的核:$x+2y+z=0,y+z=0$。由第二式 $z=-y$,代入第一式得 $x+2y-y=x+y=0$,故与 $\ker T$ 相同的条件,$\ker T^2=\ker T=\mathrm{span}\{(1,-1,1)\}$。像:$T$ 的像由 $T(1,0,0)=(1,0,0)$,$T(0,1,0)=(1,1,0)$,$T(0,0,1)=(0,1,0)$ 张成,即 $\{(a,b,0)\}$,维数 $2$。$T^2$ 的像由 $T^2(1,0,0)=(1,0,0)$,$T^2(0,0,1)=(1,1,0)$ 张成($T^2(0,1,0)=(2,1,0)=(1,0,0)+(1,1,0)$),也是 $\{(a,b,0)\}$,维数 $2$。故 $\ker T^2=\ker T$ 且 $\mathrm{im}\,T^2=\mathrm{im}\,T$(本例中复合映射的核与像均不变)。",
 "answer": r"$T^2(x,y,z)=(x+2y+z,\\,y+z,\\,0)$;$\\ker T^2=\\ker T=\\mathrm{span}\\{(1,-1,1)\\}$,$\\mathrm{im}\\,T^2=\\mathrm{im}\\,T=\\{(a,b,0)\\}$。",
 "method": "复合映射的核与像比较",
 "difficulty": "中等",
 "variant_kind": "复合映射:T² 与 T 的核像比较(本例均不变)",
 "scene_spec": {
  "objects": [
   "板书:$T$ 与 $T^2$ 的表达式",
   "板书:两个核的求解对照",
   "板书:两个像的生成元化简对照",
   "高亮框:核与像均不变的结论"
  ],
  "steps": [
   "第一步:计算 $T^2$ 的表达式。",
   "第二步:分别解 $T$ 与 $T^2$ 的核。",
   "第三步:对照两个核。",
   "第四步:化简两个像的生成元并对照。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c39-05", "category": "高等代数", "sub_category": "线性映射",
 "concept": "线性映射核与像", "concept_id": "C39",
 "parent_training_ids": ["linalg-063"],
 "problem": r"证明秩-零度定理:若 $T:V\to W$ 是有限维线性空间之间的线性映射，则 $\dim V=\dim\ker T+\dim\mathrm{im}\,T$。",
 "solution": r"取 $\ker T$ 的一组基 $v_1,\dots,v_k$,延拓为 $V$ 的基 $v_1,\dots,v_k,v_{k+1},\dots,v_n$(故 $\dim V=n$)。下证 $T(v_{k+1}),\dots,T(v_n)$ 是 $\mathrm{im}\,T$ 的一组基。张成:任意 $y\in\mathrm{im}\,T$,存在 $x=\sum_{i=1}^{n}c_iv_i$ 使 $y=T(x)=\sum_{i=1}^{n}c_iT(v_i)=\sum_{i=k+1}^{n}c_iT(v_i)$(前 $k$ 项为零,因 $v_i\in\ker T$)。线性无关:若 $\sum_{i=k+1}^{n}d_iT(v_i)=0$,则 $T\left(\sum_{i=k+1}^{n}d_iv_i\right)=0$,即 $\sum_{i=k+1}^{n}d_iv_i\in\ker T$,它可仅由 $v_1,\dots,v_k$ 表出;但 $V$ 的基表示唯一,故 $d_{k+1}=\cdots=d_n=0$。于是 $\dim\mathrm{im}\,T=n-k$,即 $\dim V=n=k+(n-k)=\dim\ker T+\dim\mathrm{im}\,T$。",
 "answer": r"证明见解法(核的基延拓到全空间,核外基向量的像构成像的基)。",
 "method": "基延拓法证明秩-零度定理",
 "difficulty": "进阶",
 "variant_kind": "证明型:秩-零度定理的严格证明",
 "scene_spec": {
  "objects": [
   "板书:核的基延拓为 $V$ 的基的示意图",
   "板书:核外基向量的像张成像的论证",
   "板书:线性无关性(落入核则系数为零)的论证",
   "高亮框:$\\dim V=\\dim\\ker T+\\dim\\mathrm{im}\\,T$"
  ],
  "steps": [
   "第一步:取核的基并延拓到全空间。",
   "第二步:证明核外基向量的像张成像。",
   "第三步:证明这些像线性无关。",
   "第四步:计数得定理。",
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
