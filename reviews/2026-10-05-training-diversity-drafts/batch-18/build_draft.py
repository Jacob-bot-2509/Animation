"""batch-18 生成器:最后两个单条考点各 5 题
(C50 中心极限定理 / C53 可列可加性)。
全部数学结论由作者逐题手工验算(见 DRAFT_REPORT.md 核算说明);
起草过程未读 eval/test 题文或答案作提示;凡有理数一律分数。
"""
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "draft.jsonl"

DATA = [
# ===================== C50 中心极限定理 =====================
{
 "id": "draft-c50-01", "category": "概率论", "sub_category": "极限定理",
 "concept": "中心极限定理", "concept_id": "C50",
 "parent_training_ids": ["prob-043"],
 "problem": r"设 $X_1,\dots,X_{100}$ 独立同分布于 $U(0,1)$，$S=\sum_{i=1}^{100}X_i$。用中心极限定理近似求 $P(S>55)$。",
 "solution": r"$EX_i=\frac12$,$Var(X_i)=\frac{1}{12}$,故 $ES=100\times\frac12=50$,$Var(S)=100\times\frac{1}{12}=\frac{25}{3}$。由中心极限定理,$\frac{S-50}{\sqrt{25/3}}$ 近似服从 $N(0,1)$。$P(S>55)\approx P\left(Z>\frac{55-50}{\sqrt{25/3}}\right)=P\left(Z>\frac{5}{5/\sqrt3}\right)=P(Z>\sqrt3)\approx P(Z>1.732)=1-\Phi(1.732)\approx0.0416$。",
 "answer": r"$P(S>55)\approx0.042$。",
 "method": "CLT 标准化近似",
 "difficulty": "基础",
 "variant_kind": "数值应用:CLT 的标准化近似计算(与定性解释父题不同)",
 "scene_spec": {
  "objects": [
   "板书:$ES=50$、$Var(S)=\\frac{25}{3}$ 的计算",
   "板书:标准化 $Z=\\frac{S-50}{\\sqrt{25/3}}$",
   "坐标图:标准正态曲线与 $z=\\sqrt3$ 的尾部阴影",
   "高亮框:$\\approx0.042$"
  ],
  "steps": [
   "第一步:计算和的期望与方差。",
   "第二步:标准化。",
   "第三步:查表得尾部概率。",
   "第四步:在正态曲线上标出尾部。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c50-02", "category": "概率论", "sub_category": "极限定理",
 "concept": "中心极限定理", "concept_id": "C50",
 "parent_training_ids": ["prob-043"],
 "problem": r"掷一颗均匀骰子 $36$ 次，$S$ 为点数之和。用中心极限定理近似求 $P(S>140)$。",
 "solution": r"单次点数 $X$:$\mu=\frac{1+2+3+4+5+6}{6}=\frac72$;$\sigma^2=\frac{1^2+2^2+3^2+4^2+5^2+6^2}{6}-\left(\frac72\right)^2=\frac{91}{6}-\frac{49}{4}=\frac{35}{12}$。故 $ES=36\times\frac72=126$,$Var(S)=36\times\frac{35}{12}=105$。$P(S>140)\approx P\left(Z>\frac{140-126}{\sqrt{105}}\right)=P(Z>1.366)=1-\Phi(1.366)\approx0.086$。",
 "answer": r"$P(S>140)\approx0.086$。",
 "method": "CLT 标准化近似(骰子)",
 "difficulty": "基础",
 "variant_kind": "中心化缩放:离散均匀总体的 CLT 标准化",
 "scene_spec": {
  "objects": [
   "板书:$\\mu=\\frac72$、$\\sigma^2=\\frac{35}{12}$ 的计算",
   "板书:标准化与查表",
   "坐标图:正态曲线与尾部阴影",
   "高亮框:$\\approx0.086$"
  ],
  "steps": [
   "第一步:计算单次点数的期望与方差。",
   "第二步:计算和的期望与方差。",
   "第三步:标准化并查表。",
   "第四步:标出尾部区域。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c50-03", "category": "概率论", "sub_category": "极限定理",
 "concept": "中心极限定理", "concept_id": "C50",
 "parent_training_ids": ["prob-043"],
 "problem": r"设 $X_1,\dots,X_{100}$ 独立同分布于指数分布 $Exp(1)$，$S=\sum_{i=1}^{100}X_i$。用中心极限定理近似求 $P(S>110)$，并与精确值(伽马分布)比较。",
 "solution": r"$Exp(1)$ 的均值为 $1$、方差为 $1$。$ES=100$,$Var(S)=100$。CLT 近似:$P(S>110)\approx P(Z>\frac{110-100}{10})=P(Z>1)=1-\Phi(1)\approx0.1587$。精确值:$S$ 服从 $\Gamma(100,1)$ 分布(形状参数 $100$)。由精确恒等式 $P(\Gamma(100,1)>110)=P(\mathrm{Pois}(110)\le99)$(伽马与泊松的互补分布关系),对泊松分布求和得 $P(S>110)\approx0.1583$。两者之差仅约 $0.0004$,说明即使总体远非正态(指数分布严重右偏),CLT 近似在 $n=100$ 时已极准确。",
 "answer": r"CLT 近似 $\approx0.159$;精确值(伽马/泊松互补)$\approx0.158$;两者差约 $0.0004$,近似极佳。",
 "method": "非正态总体的 CLT+精确对照",
 "difficulty": "中等",
 "variant_kind": "非正态总体:指数(严重右偏)总体的 CLT 近似与伽马精确值对照",
 "scene_spec": {
  "objects": [
   "坐标图:指数密度(右偏)与正态近似曲线的叠加",
   "板书:CLT 标准化计算",
   "板书:伽马分布精确值的说明",
   "高亮框:两值对照(0.159 vs 0.158)"
  ],
  "steps": [
   "第一步:计算和的期望与方差。",
   "第二步:CLT 标准化得近似值。",
   "第三步:说明精确分布为伽马。",
   "第四步:对照两值。",
   "第五步:说明非正态总体下 CLT 仍有效的结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c50-04", "category": "概率论", "sub_category": "极限定理",
 "concept": "中心极限定理", "concept_id": "C50",
 "parent_training_ids": ["prob-043"],
 "problem": r"设 $X\sim B(100,\frac12)$。分别用不带与带连续性修正的中心极限定理近似计算 $P(X\le55)$，并与精确值比较。",
 "solution": r"$\mu=50$,$\sigma=\sqrt{100\times\frac12\times\frac12}=5$。不带修正:$P(X\le55)\approx P(Z\le\frac{55-50}{5})=P(Z\le1)=\Phi(1)\approx0.8413$。带连续性修正:$P(X\le55)=P(X\le55.5)\approx P(Z\le\frac{55.5-50}{5})=P(Z\le1.1)=\Phi(1.1)\approx0.8643$。精确值:$\sum_{k=0}^{55}\binom{100}{k}(\frac12)^{100}\approx0.8644$。可见连续性修正显著改善了近似(不带修正误差约 $0.023$,带修正误差约 $0.0001$)。",
 "answer": r"不带修正 $\approx0.841$;带修正 $\approx0.864$;精确值 $\approx0.864$。连续性修正显著改善。",
 "method": "连续性修正对比",
 "difficulty": "中等",
 "variant_kind": "连续性修正:离散分布 CLT 近似的连续性修正与精确值对照",
 "scene_spec": {
  "objects": [
   "坐标图:二项分布直方图与正态曲线叠加",
   "板书:不带修正的近似计算",
   "板书:带修正的近似计算",
   "高亮框:三个数值对照表"
  ],
  "steps": [
   "第一步:计算二项分布的均值与标准差。",
   "第二步:不带修正的近似。",
   "第三步:带连续性修正的近似。",
   "第四步:给出精确值并对照。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c50-05", "category": "概率论", "sub_category": "极限定理",
 "concept": "中心极限定理", "concept_id": "C50",
 "parent_training_ids": ["prob-043"],
 "problem": r"说明中心极限定理要求方差有限的条件，并用柯西分布的例子说明：若方差无限，样本均值不必近似正态。",
 "solution": r"中心极限定理的标准条件:独立同分布、均值 $\mu$ 与方差 $\sigma^2$ 均有限;此时 $\frac{\sum X_i-n\mu}{\sigma\sqrt n}$ 依分布收敛于 $N(0,1)$。柯西分布 $Cauchy(0,1)$:均值与方差均不存在。其特征函数为 $\varphi(t)=e^{-|t|}$。若 $X_1,\dots,X_n$ 独立同分布于柯西分布,则样本均值 $\bar X_n=\frac1n\sum X_i$ 的特征函数为 $\varphi(t/n)^n=(e^{-|t|/n})^n=e^{-|t|}$,仍是 $Cauchy(0,1)$ 的特征函数!即样本均值与单个观测同分布,完全不随 $n$ 增大而向正态靠拢(也不向任何常数集中)。这从反面说明方差有限(或类似的矩条件)对 CLT 必不可少。",
 "answer": r"柯西分布样本均值的特征函数 $(e^{-|t|/n})^n=e^{-|t|}$ 仍为柯西,不近似正态;说明方差有限条件是 CLT 的必要条件(论证见解法)。",
 "method": "退化限制(特征函数反例)",
 "difficulty": "进阶",
 "variant_kind": "退化或无限方差时的限制:柯西分布反例的特征函数论证",
 "scene_spec": {
  "objects": [
   "坐标图:柯西密度(重尾)与正态密度(轻尾)的对照",
   "板书:CLT 的矩条件(方差有限)",
   "板书:柯西特征函数与样本均值特征函数的推导",
   "高亮框:$\\bar X_n\\sim Cauchy(0,1)$,不趋正态"
  ],
  "steps": [
   "第一步:写出 CLT 的标准条件。",
   "第二步:画出柯西与正态的尾部对照。",
   "第三步:推导柯西样本均值的特征函数。",
   "第四步:说明分布不变、不趋正态。",
   "第五步:总结方差有限条件的必要性。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
# ===================== C53 可列可加性 =====================
{
 "id": "draft-c53-01", "category": "概率论", "sub_category": "概率公理",
 "concept": "可列可加性", "concept_id": "C53",
 "parent_training_ids": ["prob-046"],
 "problem": r"设 $X$ 服从参数为 $p$ 的几何分布($P(X=k)=p(1-p)^{k-1}$,$k=1,2,\dots$)。用可列可加性求 $P(X\ge k)$。",
 "solution": r"事件 $\{X\ge k\}$ 可拆分为可列个互斥事件 $\{X=i\}$($i=k,k+1,\dots$)的并。由可列可加性,$P(X\ge k)=\sum_{i=k}^{\infty}P(X=i)=\sum_{i=k}^{\infty}p(1-p)^{i-1}=p(1-p)^{k-1}\sum_{j=0}^{\infty}(1-p)^j=p(1-p)^{k-1}\cdot\frac{1}{1-(1-p)}=(1-p)^{k-1}$。",
 "answer": r"$P(X\ge k)=(1-p)^{k-1}$。",
 "method": "可列拆分(几何分布尾概率)",
 "difficulty": "基础",
 "variant_kind": "计算应用:尾事件的可列拆分求和(与几何分割父题不同)",
 "scene_spec": {
  "objects": [
   "数轴:整数点 $k,k+1,\\dots$ 与尾事件的并集高亮",
   "板书:可列可加性的拆分",
   "板书:几何级数求和",
   "高亮框:$(1-p)^{k-1}$"
  ],
  "steps": [
   "第一步:把尾事件拆为可列个单点事件。",
   "第二步:由可列可加性求和。",
   "第三步:提取公因子并求几何级数。",
   "第四步:得尾概率公式。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c53-02", "category": "概率论", "sub_category": "概率公理",
 "concept": "可列可加性", "concept_id": "C53",
 "parent_training_ids": ["prob-046"],
 "problem": r"抛两枚均匀硬币。用互斥事件的拆分与可加性求「至少一枚正面朝上」的概率。",
 "solution": r"样本空间 $\Omega=\{HH,HT,TH,TT\}$,四个基本事件互斥且概率各为 $\frac14$。事件 $A=$「至少一枚正面」$=\{HH,HT,TH\}$,由(有限)可加性,$P(A)=P(HH)+P(HT)+P(TH)=\frac14+\frac14+\frac14=\frac34$。",
 "answer": r"$P(A)=\frac34$。",
 "method": "互斥拆分求和",
 "difficulty": "基础",
 "variant_kind": "重叠先拆分:复杂事件拆为互斥基本事件再求和",
 "scene_spec": {
  "objects": [
   "两枚硬币的四种结果表(正正/正反/反正/反反)",
   "三种含正面的结果高亮",
   "板书:$P(A)=\\frac14+\\frac14+\\frac14$",
   "高亮框:$\\frac34$"
  ],
  "steps": [
   "第一步:列出样本空间。",
   "第二步:高亮目标事件所含结果。",
   "第三步:由可加性求和。",
   "第四步:高亮结果。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c53-03", "category": "概率论", "sub_category": "概率公理",
 "concept": "可列可加性", "concept_id": "C53",
 "parent_training_ids": ["prob-046"],
 "problem": r"说明为什么概率公理中的可加性只要求「可列」而不要求「不可列」:以 $[0,1]$ 上的均匀分布为例。",
 "solution": r"在 $[0,1]$ 的均匀分布下,每个单点 $\{x\}$ 的概率为 $0$。若把可加性不加限制地推广到不可列求和,则 $P([0,1])=P\left(\bigcup_{x\in[0,1]}\{x\}\right)=\sum_{x\in[0,1]}P(\{x\})=0$,与 $P([0,1])=1$ 矛盾。原因:不可列多个数(即使是零)的「和」本身没有良好的定义(不可列正数集中必有可列子集和发散),概率论只对可列并集建立求和理论。因此公理限定为可列可加性,既足以处理极限运算,又避免上述矛盾。",
 "answer": r"若允许不可列可加,$[0,1]$ 的概率会是不可列多个零之和 $=0$,与 $P([0,1])=1$ 矛盾;故可加性只定义在可列并集上。",
 "method": "可列与不可列区别(反例论证)",
 "difficulty": "中等",
 "variant_kind": "可列与不可列区别:不可列可加性的矛盾反例",
 "scene_spec": {
  "objects": [
   "数轴:区间 $[0,1]$ 与稠密的单点标注",
   "板书:$P(\\{x\\})=0$ 与不可列求和为零的矛盾推导",
   "红色标签「不可列可加不可行」",
   "高亮框:公理限定可列的原因"
  ],
  "steps": [
   "第一步:说明均匀分布下每个单点概率为零。",
   "第二步:假设不可列可加并求和。",
   "第三步:得到 $0=1$ 的矛盾。",
   "第四步:说明不可列求和本身无良定义。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c53-04", "category": "概率论", "sub_category": "概率公理",
 "concept": "可列可加性", "concept_id": "C53",
 "parent_training_ids": ["prob-046"],
 "problem": r"设 $X\sim U(0,1)$，$A_n=\{X\ge\frac1n\}$。求 $P(A_n)$ 与 $P\left(\bigcup_{n=1}^{\infty}A_n\right)$，并说明与概率的单调连续性(下连续性)的关系。",
 "solution": r"$P(A_n)=P(X\ge\frac1n)=1-\frac1n$。$\bigcup_{n=1}^{\infty}A_n=\{X>0\}$(对 $X\in(0,1)$ 的样本点,存在 $n$ 使 $X\ge\frac1n$),故 $P\left(\bigcup_nA_n\right)=P(X>0)=1$。另一方面 $A_n$ 单调递增($A_1\subseteq A_2\subseteq\cdots$),由下连续性(可由可列可加性导出),$P(\bigcup_nA_n)=\lim_{n}P(A_n)=\lim(1-\frac1n)=1$。两者一致。",
 "answer": r"$P(A_n)=1-\frac1n$;$P(\bigcup_n A_n)=1=\lim P(A_n)$(下连续性,与可列可加性一致)。",
 "method": "单调事件序列的连续性应用",
 "difficulty": "中等",
 "variant_kind": "极限事件与单调连续性:递增事件列的极限概率",
 "scene_spec": {
  "objects": [
   "数轴:区间 $[\\frac1n,1)$ 随 $n$ 增大而扩张的动画",
   "板书:$P(A_n)=1-\\frac1n$",
   "板书:并集为 $\\{X>0\\}$ 与极限一致",
   "高亮框:下连续性 $P(\\cup A_n)=\\lim P(A_n)=1$"
  ],
  "steps": [
   "第一步:计算每个 $A_n$ 的概率。",
   "第二步:动画展示区间随 $n$ 扩张。",
   "第三步:求并集与并集概率。",
   "第四步:与极限对照。",
   "第五步:高亮下连续性结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c53-05", "category": "概率论", "sub_category": "概率公理",
 "concept": "可列可加性", "concept_id": "C53",
 "parent_training_ids": ["prob-046"],
 "problem": r"证明:在有限可加性的前提下,可列可加性等价于下连续性(即对 $A_1\subseteq A_2\subseteq\cdots$,$P(\bigcup_nA_n)=\lim_nP(A_n)$)。",
 "solution": r"(可列可加⟹下连续)设 $A_n\uparrow A=\bigcup_nA_n$。令 $B_1=A_1$,$B_n=A_n\setminus A_{n-1}$($n\ge2$),则 $B_n$ 两两互斥且 $A=\bigcup_nB_n$,$A_n=\bigcup_{i\le n}B_i$。由可列可加性,$P(A)=\sum_nP(B_n)=\lim_n\sum_{i\le n}P(B_i)=\lim_nP(A_n)$(最后一步用有限可加性)。(下连续⟹可列可加)设 $A_1,A_2,\dots$ 两两互斥,$A=\bigcup_nA_n$。令 $C_n=\bigcup_{i\le n}A_i$,则 $C_n\uparrow A$。由下连续性与有限可加性,$P(A)=\lim_nP(C_n)=\lim_n\sum_{i\le n}P(A_i)=\sum_nP(A_n)$。故在有限可加性下两者等价。",
 "answer": r"证明见解法(可列可加⟹下连续:互斥拆分 $B_n=A_n\setminus A_{n-1}$;下连续⟹可列可加:部分并 $C_n\uparrow A$)。",
 "method": "可列可加性与连续性的等价证明",
 "difficulty": "进阶",
 "variant_kind": "证明型:可列可加性与下连续性的等价性证明",
 "scene_spec": {
  "objects": [
   "板书:两个方向的推导链",
   "韦恩图:$B_n$ 的互斥拆分与 $C_n$ 的递增并",
   "高亮框:有限可加性下两者等价",
   "标签「概率公理的结构」"
  ],
  "steps": [
   "第一步:证明可列可加蕴含下连续(互斥拆分)。",
   "第二步:展示 $B_n$ 拆分图。",
   "第三步:证明下连续蕴含可列可加(部分并)。",
   "第四步:展示 $C_n$ 递增图。",
   "第五步:高亮等价性结论。"
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
