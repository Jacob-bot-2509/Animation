"""batch-09 生成器:三个单条考点各 5 题
(C10 交错级数与绝对收敛 / C12 函数项级数一致收敛 / C14 傅立叶展开)。
全部数学结论由作者逐题手工验算(见 DRAFT_REPORT.md 核算说明);
起草过程未读 eval/test 题文或答案作提示;凡有理数一律分数。
"""
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "draft.jsonl"

DATA = [
# ===================== C10 交错级数与绝对收敛 =====================
{
 "id": "draft-c10-01", "category": "数学分析", "sub_category": "级数",
 "concept": "交错级数与绝对收敛", "concept_id": "C10",
 "parent_training_ids": ["calc-series-015"],
 "problem": r"判断级数 $\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n}$ 的敛散性，并指出是绝对收敛还是条件收敛。",
 "solution": r"绝对收敛性:$\left|\frac{(-1)^{n+1}}{n}\right|=\frac1n$,$\sum\frac1n$ 为调和级数,发散,故非绝对收敛。条件收敛性:$a_n=\frac1n$ 单调递减趋于 $0$,由莱布尼茨判别法,$\sum\frac{(-1)^{n+1}}{n}$ 收敛。故为条件收敛(其和为 $\ln2$)。",
 "answer": r"条件收敛(和为 $\ln2$)。",
 "method": "莱布尼茨判别法+绝对收敛检验",
 "difficulty": "基础",
 "variant_kind": "绝对与条件边界:调和型交错级数的条件收敛判定",
 "scene_spec": {
  "objects": [
   "板书:级数 $\\sum(-1)^{n+1}/n$",
   "板书:绝对值的调和级数发散(红色)",
   "板书:莱布尼茨条件核对($\\frac1n$ 单调递减趋于 $0$)",
   "高亮框:「条件收敛,和 $=\\ln2$」",
   "数轴:部分和的摆动收敛示意(两侧夹逼动画)"
  ],
  "steps": [
   "第一步:写出级数,先检验绝对收敛:调和级数发散。",
   "第二步:核对莱布尼茨条件:通项绝对值单调递减趋于零。",
   "第三步:结论:交错级数收敛。",
   "第四步:动画展示部分和在 $\\ln2$ 两侧摆动收敛。",
   "第五步:高亮「条件收敛」结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c10-02", "category": "数学分析", "sub_category": "级数",
 "concept": "交错级数与绝对收敛", "concept_id": "C10",
 "parent_training_ids": ["calc-series-015"],
 "problem": r"判断级数 $\sum_{n=1}^{\infty}\frac{(-1)^n n}{n^2+1}$ 的敛散性，并指出是绝对收敛还是条件收敛。",
 "solution": r"绝对收敛性:$\frac{n}{n^2+1}\ge\frac{n}{2n^2}=\frac{1}{2n}$($n\ge1$ 时 $n^2+1\le2n^2$),而 $\sum\frac{1}{2n}$ 发散,故 $\sum\frac{n}{n^2+1}$ 发散,非绝对收敛。条件收敛性:令 $f(x)=\frac{x}{x^2+1}$,$f'(x)=\frac{1-x^2}{(x^2+1)^2}<0$($x>1$),故 $a_n=\frac{n}{n^2+1}$ 单调递减;又 $\lim_{n\to\infty}\frac{n}{n^2+1}=0$。由莱布尼茨判别法,$\sum\frac{(-1)^n n}{n^2+1}$ 收敛,故为条件收敛。",
 "answer": r"条件收敛(绝对值级数发散,交错级数本身收敛)。",
 "method": "比较判别+莱布尼茨判别法",
 "difficulty": "基础",
 "variant_kind": "数值结构变化:含 n 的分子分母型的条件收敛判定(比较+单调性论证)",
 "scene_spec": {
  "objects": [
   "板书:级数 $\\sum(-1)^n n/(n^2+1)$",
   "板书:比较判别 $\\frac{n}{n^2+1}\\ge\\frac{1}{2n}$(绝对值级数发散)",
   "板书:$f'(x)=\\frac{1-x^2}{(x^2+1)^2}<0$ 的单调性论证",
   "高亮框:「条件收敛」",
   "标签「绝对值发散但自身收敛」"
  ],
  "steps": [
   "第一步:写出级数,展示绝对值级数的比较判别。",
   "第二步:说明绝对值级数发散,非绝对收敛。",
   "第三步:求导论证通项绝对值单调递减并趋于零。",
   "第四步:由莱布尼茨判别法得收敛。",
   "第五步:高亮「条件收敛」结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c10-03", "category": "数学分析", "sub_category": "级数",
 "concept": "交错级数与绝对收敛", "concept_id": "C10",
 "parent_training_ids": ["calc-series-015"],
 "problem": r"说明级数 $\sum_{n=1}^{\infty}\frac{(-1)^n(2+(-1)^n)}{n}$ 发散，并解释莱布尼茨判别法为何不能使用。",
 "solution": r"拆项:$\frac{(-1)^n(2+(-1)^n)}{n}=\frac{2(-1)^n+1}{n}=\frac{2(-1)^n}{n}+\frac1n$。于是原级数 $=2\sum\frac{(-1)^n}{n}+\sum\frac1n$:第一项由莱布尼茨判别法收敛,第二项调和级数发散,收敛级数与发散级数之和必发散,故原级数发散。莱布尼茨判别法不能使用的原因:通项绝对值 $a_n=\frac{2+(-1)^n}{n}$ 虽趋于 $0$,但不单调($a_n$ 在 $\frac3n$ 与 $\frac1n$ 之间跳动),不满足判别法的单调条件——可见「通项趋于零」加「交错」并不足以保证收敛。",
 "answer": r"级数发散(拆成 $2\sum(-1)^n/n+\sum1/n$,收敛+发散);莱布尼茨判别法因通项绝对值不单调而不可用。",
 "method": "拆项分析(单调性条件的必要性)",
 "difficulty": "中等",
 "variant_kind": "单调性不满足:莱布尼茨条件失效的反例辨析",
 "scene_spec": {
  "objects": [
   "板书:级数 $\\sum(-1)^n(2+(-1)^n)/n$ 的拆项过程",
   "板书:$2\\sum(-1)^n/n$(收敛,绿色)与 $\\sum1/n$(发散,红色)",
   "坐标图:通项绝对值 $a_n$ 在 $\\frac3n$ 与 $\\frac1n$ 之间跳动的散点动画",
   "高亮框:「发散」",
   "标签「通项趋于零+交错 ≠ 收敛」"
  ],
  "steps": [
   "第一步:展示拆项:$\\frac{2(-1)^n}{n}+\\frac1n$。",
   "第二步:说明收敛级数与发散级数之和发散。",
   "第三步:动画展示通项绝对值在两曲线间跳动,不单调。",
   "第四步:指出莱布尼茨判别法的单调条件不满足。",
   "第五步:高亮结论:交错+通项趋于零不足以保证收敛。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c10-04", "category": "数学分析", "sub_category": "级数",
 "concept": "交错级数与绝对收敛", "concept_id": "C10",
 "parent_training_ids": ["calc-series-015"],
 "problem": r"用交错级数余项估计,求级数 $\sum_{n=1}^{\infty}\frac{(-1)^{n+1}}{n}$ 的和的近似值,使误差小于 $\frac{1}{10}$。",
 "solution": r"莱布尼茨型交错级数的余项估计:$|R_N|=|S-S_N|\le a_{N+1}=\frac{1}{N+1}$。要求 $\frac{1}{N+1}<\frac{1}{10}$,即 $N+1>10$,$N\ge10$,故取前 $10$ 项。$S_{10}=1-\frac12+\frac13-\frac14+\frac15-\frac16+\frac17-\frac18+\frac19-\frac{1}{10}$。通分(公分母 $2520$):分子 $=2520-1260+840-630+504-420+360-315+280-252=1627$,故 $S_{10}=\frac{1627}{2520}\approx0.6456$。所以 $S\approx0.646$,误差小于 $0.1$(实际 $S=\ln2\approx0.6931$,实际误差 $\approx0.05$ 满足要求)。",
 "answer": r"取前 $10$ 项,$S_{10}=\frac{1627}{2520}\approx0.646$,误差小于 $\frac{1}{10}$。",
 "method": "交错级数余项估计",
 "difficulty": "中等",
 "variant_kind": "余项界:由 |R_N|≤a_{N+1} 确定项数并计算近似值",
 "scene_spec": {
  "objects": [
   "板书:余项估计 $|R_N|\\le\\frac{1}{N+1}<\\frac{1}{10}\\Rightarrow N\\ge10$",
   "动画:部分和 $S_1,S_2,\\dots,S_{10}$ 的摆动逼近过程",
   "板书:逐项累加的过程与 $S_{10}=\\frac{1627}{2520}\\approx0.646$",
   "数轴:真实值 $\\ln2$ 与 $S_{10}$ 的位置及误差区间",
   "高亮框:$S_{10}\\approx0.646$(误差 $<0.1$)"
  ],
  "steps": [
   "第一步:写出余项估计,由误差要求解出 $N\\ge10$。",
   "第二步:动画展示部分和逐项摆动逼近。",
   "第三步:逐项累加得 $S_{10}\\approx0.646$。",
   "第四步:在数轴上标出真实值与误差区间。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c10-05", "category": "数学分析", "sub_category": "级数",
 "concept": "交错级数与绝对收敛", "concept_id": "C10",
 "parent_training_ids": ["calc-series-015"],
 "problem": r"证明莱布尼茨判别法:若 $a_n$ 单调递减趋于 $0$,则交错级数 $\sum_{n=1}^{\infty}(-1)^{n+1}a_n$ 收敛,且其和 $S$ 满足 $|S-S_N|\le a_{N+1}$。",
 "solution": r"考察偶子列部分和:$S_{2N}=(a_1-a_2)+(a_3-a_4)+\cdots+(a_{2N-1}-a_{2N})$。因 $a_n$ 单调递减,每个括号非负,故 $S_{2N}$ 单调递增;又 $S_{2N}=a_1-(a_2-a_3)-\cdots-(a_{2N-2}-a_{2N-1})-a_{2N}\le a_1$,故 $S_{2N}$ 有上界。单调有界定理:$\lim S_{2N}=S$ 存在。奇子列 $S_{2N+1}=S_{2N}+a_{2N+1}\to S+0=S$,故两子列收敛于同一极限,原级数收敛于 $S$。余项估计:$|S-S_N|\le a_{N+1}$。证明:当 $N$ 为偶数时,$S-S_N=(a_{N+1}-a_{N+2})+(a_{N+3}-a_{N+4})+\cdots\ge0$ 且 $S-S_N\le a_{N+1}$(首个括号之后各项括号非负,逐对减去);当 $N$ 为奇数时,$|S-S_N|=S_N-S=a_{N+1}-(a_{N+2}-a_{N+3})-(a_{N+4}-a_{N+5})-\cdots\le a_{N+1}$(每个括号均非负,从 $a_{N+1}$ 起逐对减去)。故一般地 $|S-S_N|\le a_{N+1}$。",
 "answer": r"证明见解法(偶子列单调有界、奇子列同极限;余项 $|S-S_N|\le a_{N+1}$)。",
 "method": "单调有界定理(收敛性与余项界证明)",
 "difficulty": "进阶",
 "variant_kind": "证明型:莱布尼茨判别法的严格证明与余项估计推导",
 "scene_spec": {
  "objects": [
   "板书:偶子列 $S_{2N}$ 的配对分组与单调递增展示",
   "板书:$S_{2N}=a_1-(a_2-a_3)-\\cdots-a_{2N}\\le a_1$ 的上界论证",
   "板书:奇子列 $S_{2N+1}=S_{2N}+a_{2N+1}$ 的同极限论证",
   "板书:余项 $|S-S_N|\\le a_{N+1}$ 的奇偶分支推导",
   "高亮框:莱布尼茨判别法成立"
  ],
  "steps": [
   "第一步:把偶子列部分和配对分组,展示括号均非负。",
   "第二步:给出偶子列的上界 $a_1$,由单调有界定理得收敛。",
   "第三步:说明奇子列与偶子列收敛于同一极限。",
   "第四步:分奇偶推导余项估计 $|S-S_N|\\le a_{N+1}$。",
   "第五步:高亮结论,完成证明。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
# ===================== C12 函数项级数一致收敛 =====================
{
 "id": "draft-c12-01", "category": "数学分析", "sub_category": "函数项级数",
 "concept": "函数项级数一致收敛", "concept_id": "C12",
 "parent_training_ids": ["calc-series-017"],
 "problem": r"证明函数项级数 $\sum_{n=1}^{\infty}\frac{\sin nx}{n^2}$ 在 $\mathbb R$ 上一致收敛。",
 "solution": r"用魏尔斯特拉斯 $M$ 判别法:对一切 $x\in\mathbb R$,$\left|\frac{\sin nx}{n^2}\right|\le\frac{1}{n^2}=M_n$,而 $\sum_{n=1}^{\infty}M_n=\sum\frac{1}{n^2}$ 收敛。故级数在 $\mathbb R$ 上一致收敛(且绝对一致收敛)。",
 "answer": r"在 $\mathbb R$ 上一致收敛($M$ 判别法,$M_n=\frac{1}{n^2}$)。",
 "method": "魏尔斯特拉斯 M 判别法",
 "difficulty": "基础",
 "variant_kind": "方法变化:三角函数的 M 判别法(与幂级数父题不同)",
 "scene_spec": {
  "objects": [
   "板书:级数 $\\sum\\sin(nx)/n^2$ 与不等式 $|\\sin nx|/n^2\\le1/n^2$",
   "板书:$M_n=1/n^2$ 与 $\\sum M_n$ 收敛(p 级数)",
   "高亮框:「全实轴一致收敛」",
   "标签「魏尔斯特拉斯 M 判别法」"
  ],
  "steps": [
   "第一步:写出级数,构造上界 $|\\sin nx|/n^2\\le1/n^2$。",
   "第二步:取 $M_n=1/n^2$,说明 $\\sum M_n$ 收敛。",
   "第三步:由 M 判别法得一致收敛。",
   "第四步:强调一致收敛区间为全实轴。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c12-02", "category": "数学分析", "sub_category": "函数项级数",
 "concept": "函数项级数一致收敛", "concept_id": "C12",
 "parent_training_ids": ["calc-series-017"],
 "problem": r"证明 $\sum_{n=0}^{\infty}x^n$ 在 $[-\frac12,\frac12]$ 上一致收敛，并说明在 $(-1,1)$ 上不一致收敛。",
 "solution": r"在 $[-\frac12,\frac12]$ 上,$|x|^n\le\left(\frac12\right)^n$,而 $\sum\left(\frac12\right)^n$ 收敛,由 $M$ 判别法一致收敛。在 $(-1,1)$ 上,部分和 $S_N(x)=\frac{1-x^{N+1}}{1-x}$,和函数 $S(x)=\frac{1}{1-x}$,尾项 $|S_N(x)-S(x)|=\frac{|x|^{N+1}}{1-x}$。取 $x_N=1-\frac1N\in(-1,1)$:$\frac{x_N^{N+1}}{1-x_N}=N\left(1-\frac1N\right)^{N+1}\to\infty$(因 $\left(1-\frac1N\right)^{N+1}\to e^{-1}$),故 $\sup_{x\in(-1,1)}|S_N-S|$ 不趋于 $0$,不一致收敛。",
 "answer": r"在 $[-\frac12,\frac12]$ 上一致收敛($M$ 判别法);在 $(-1,1)$ 上不一致收敛($\sup|S_N-S|$ 不趋于 $0$)。",
 "method": "M 判别法+上确界判别(一致与不一致对照)",
 "difficulty": "基础",
 "variant_kind": "一致与逐点区别:同一级数在缩小区间与开区间上的收敛性对照",
 "scene_spec": {
  "objects": [
   "板书:在 $[-\\frac12,\\frac12]$ 上 $|x|^n\\le(\\frac12)^n$ 的 M 判别",
   "板书:尾项 $|S_N-S|=\\frac{|x|^{N+1}}{1-x}$ 的表达式",
   "动画:$x_N=1-\\frac1N$ 处尾项随 $N$ 增长发散的示意",
   "高亮框:「缩小区间一致,开区间不一致」",
   "标签「收敛性依赖区间」"
  ],
  "steps": [
   "第一步:展示缩小区间上的 M 判别法证明。",
   "第二步:写出开区间上的尾项表达式。",
   "第三步:取 $x_N=1-\\frac1N$,展示尾项不趋于零。",
   "第四步:说明上确界不趋于零,不一致收敛。",
   "第五步:高亮两区间的对照结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c12-03", "category": "数学分析", "sub_category": "函数项级数",
 "concept": "函数项级数一致收敛", "concept_id": "C12",
 "parent_training_ids": ["calc-series-017"],
 "problem": r"讨论函数项级数 $\sum_{n=1}^{\infty}\frac{x^n}{n}$ 在 $[0,r]$($0<r<1$)上的一致收敛性，并说明其在 $[0,1)$ 上不一致收敛。",
 "solution": r"在 $[0,r]$ 上,$\left|\frac{x^n}{n}\right|\le\frac{r^n}{n}\le r^n$,而 $\sum r^n$ 收敛($0<r<1$),由 $M$ 判别法一致收敛。在 $[0,1)$ 上,尾项 $\sum_{k=N+1}^{\infty}\frac{x^k}{k}$ 关于 $x$ 递增(各项系数为正),其关于 $x$ 的上确界为 $\sup_{x\in[0,1)}\sum_{k=N+1}^{\infty}\frac{x^k}{k}=\lim_{x\to1^-}\sum_{k=N+1}^{\infty}\frac{x^k}{k}=\sum_{k=N+1}^{\infty}\frac1k$(在 $[0,1)$ 内不被任何点取到,由极限给出)。调和级数尾部发散,故 $\sup$ 为 $+\infty$ 不趋于 $0$,不一致收敛。",
 "answer": r"在 $[0,r]$($0<r<1$)上一致收敛;在 $[0,1)$ 上不一致收敛。",
 "method": "M 判别法+尾部上确界分析",
 "difficulty": "中等",
 "variant_kind": "区间改变:端点邻域使一致收敛性丧失的尾部上确界分析",
 "scene_spec": {
  "objects": [
   "板书:$[0,r]$ 上的 M 判别($x^n/n\\le r^n$)",
   "板书:尾项 $\\sum_{k>N}x^k/k$ 的上确界为调和尾部",
   "动画:$x\\to1^-$ 时尾部部分和不断增大发散的示意",
   "高亮框:「$[0,r]$ 一致,$[0,1)$ 不一致」",
   "标签「端点邻域导致不一致」"
  ],
  "steps": [
   "第一步:展示 $[0,r]$ 上的 M 判别法。",
   "第二步:在 $[0,1)$ 上分析尾部上确界。",
   "第三步:说明上确界恰为调和级数尾部,发散。",
   "第四步:动画展示 $x\\to1^-$ 时尾部不收敛于零。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c12-04", "category": "数学分析", "sub_category": "函数项级数",
 "concept": "函数项级数一致收敛", "concept_id": "C12",
 "parent_training_ids": ["calc-series-017"],
 "problem": r"设 $0<r<1$。利用 $\sum_{n=0}^{\infty}x^n$ 在 $[0,r]$ 上的一致收敛性,将 $\int_0^r\frac{1}{1-x}\,dx$ 展开为级数并验证。",
 "solution": r"在 $[0,r]$ 上 $\sum x^n$ 一致收敛,故可逐项积分:$\int_0^r\frac{1}{1-x}\,dx=\int_0^r\sum_{n=0}^{\infty}x^n\,dx=\sum_{n=0}^{\infty}\int_0^rx^n\,dx=\sum_{n=0}^{\infty}\frac{r^{n+1}}{n+1}$。直接积分验证:$-\ln(1-r)$ 的级数展开为 $\sum_{n=0}^{\infty}\frac{r^{n+1}}{n+1}$($\ln(1-u)=-u-\frac{u^2}{2}-\frac{u^3}{3}-\cdots$,即 $-\ln(1-r)=r+\frac{r^2}{2}+\frac{r^3}{3}+\cdots$),两者一致。",
 "answer": r"$\int_0^r\frac{1}{1-x}dx=\sum_{n=0}^{\infty}\frac{r^{n+1}}{n+1}=-\ln(1-r)$。",
 "method": "一致收敛下的逐项积分",
 "difficulty": "中等",
 "variant_kind": "逐项积分:一致收敛保证下的积分与求和交换",
 "scene_spec": {
  "objects": [
   "板书:一致收敛(已证)⇒ 可逐项积分",
   "板书:$\\int_0^r\\sum x^n\\,dx=\\sum\\int_0^rx^n\\,dx=\\sum\\frac{r^{n+1}}{n+1}$",
   "板书:对数展开 $r+r^2/2+r^3/3+\\cdots$ 的对照",
   "高亮框:$=-\\ln(1-r)$",
   "标签「一致收敛保证逐项积分」"
  ],
  "steps": [
   "第一步:引用 $[0,r]$ 上的一致收敛性。",
   "第二步:展示逐项积分的交换过程。",
   "第三步:写出级数和 $\\sum r^{n+1}/(n+1)$。",
   "第四步:与对数函数的幂级数展开对照。",
   "第五步:高亮结论 $-\\ln(1-r)$。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c12-05", "category": "数学分析", "sub_category": "函数项级数",
 "concept": "函数项级数一致收敛", "concept_id": "C12",
 "parent_training_ids": ["calc-series-017"],
 "problem": r"证明函数列 $f_n(x)=n^2x(1-x^2)^n$($0\le x\le1$)逐点收敛于 $0$，但 $\int_0^1f_n(x)\,dx$ 不趋于 $0$；由此说明逐点收敛不足以保证极限与积分交换，并指出一致收敛为何是充分条件。",
 "solution": r"逐点收敛:当 $x=0$ 时 $f_n(0)=0$;当 $0<x\le1$ 时,$f_n(x)=n^2x(1-x^2)^n$,$0\le1-x^2<1$,指数衰减快于多项式增长,故 $f_n(x)\to0$。积分:换元 $u=1-x^2$,$du=-2x\,dx$,$\int_0^1f_n(x)\,dx=\frac{n^2}{2}\int_0^1u^n\,du=\frac{n^2}{2(n+1)}\to+\infty$。而 $\int_0^1\lim f_n\,dx=0$,故极限与积分不能交换。原因:该函数列不一致收敛(若一致收敛于 $0$,则 $\sup|f_n|$ 应趋于 $0$;计算 $f_n$ 在 $x=\frac{1}{\sqrt{2n+1}}$ 处取值约为 $\frac{n^2}{\sqrt{2n+1}}e^{-\frac12}\to\infty$,故 $\sup|f_n|\to\infty$,不一致)。一致收敛是逐项积分/交换极限的充分条件:一致收敛保证 $\left|\int f_n-\int f\right|\le\int|f_n-f|\le\sup|f_n-f|\cdot(b-a)\to0$。",
 "answer": r"$f_n\to0$ 逐点,但 $\int_0^1f_n=n^2/(2(n+1))\to+\infty\neq0$;该函数列不一致收敛($\sup|f_n|\to\infty$),一致收敛是交换的充分条件(证明见解法)。",
 "method": "反例构造(逐点收敛+积分不可交换)",
 "difficulty": "进阶",
 "variant_kind": "反例型:逐点收敛不足以保证积分交换的经典反例与充分条件说明",
 "scene_spec": {
  "objects": [
   "坐标图:函数列 $f_n$ 的图像(尖峰不断升高变窄的动画)",
   "板书:$f_n(x)=n^2x(1-x^2)^n$ 的逐点收敛说明",
   "板书:积分 $\\frac{n^2}{2(n+1)}\\to+\\infty$ 的计算",
   "板书:$\\sup|f_n|\\to\\infty$(取 $x=1/\\sqrt{2n+1}$)的不一致收敛证明",
   "高亮框:「逐点收敛≠可交换积分」"
  ],
  "steps": [
   "第一步:动画展示尖峰不断升高变窄的函数列图像。",
   "第二步:说明逐点收敛于零。",
   "第三步:计算积分序列发散到正无穷。",
   "第四步:由上确界发散证明不一致收敛。",
   "第五步:给出不一致性使交换失效、一致性保证交换的总结。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
# ===================== C14 傅立叶展开 =====================
{
 "id": "draft-c14-01", "category": "数学分析", "sub_category": "傅立叶级数",
 "concept": "傅立叶展开", "concept_id": "C14",
 "parent_training_ids": ["calc-series-020"],
 "problem": r"将 $f(x)=x^2$($-\pi\le x\le\pi$)展开为傅立叶级数，并由此推导 $\sum_{n=1}^{\infty}\frac{1}{n^2}=\frac{\pi^2}{6}$。",
 "solution": r"$f$ 为偶函数,故 $b_n=0$。$a_0=\frac1\pi\int_{-\pi}^{\pi}x^2\,dx=\frac1\pi\cdot\frac{2\pi^3}{3}=\frac{2\pi^2}{3}$。$a_n=\frac1\pi\int_{-\pi}^{\pi}x^2\cos nx\,dx$。两次分部积分:$\int x^2\cos nx\,dx=\frac{x^2\sin nx}{n}+\frac{2x\cos nx}{n^2}-\frac{2\sin nx}{n^3}$,代入上下限得 $\int_{-\pi}^{\pi}x^2\cos nx\,dx=\frac{4\pi(-1)^n}{n^2}$($\sin n\pi=0$,$\cos n\pi=(-1)^n$),故 $a_n=\frac{4(-1)^n}{n^2}$。于是 $x^2=\frac{\pi^2}{3}+4\sum_{n=1}^{\infty}\frac{(-1)^n\cos nx}{n^2}$。取 $x=\pi$:$\pi^2=\frac{\pi^2}{3}+4\sum_{n=1}^{\infty}\frac{1}{n^2}$,解得 $\sum_{n=1}^{\infty}\frac{1}{n^2}=\frac{\pi^2}{6}$。",
 "answer": r"$x^2=\frac{\pi^2}{3}+4\sum_{n=1}^{\infty}\frac{(-1)^n\cos nx}{n^2}$;$\sum_{n=1}^{\infty}\frac{1}{n^2}=\frac{\pi^2}{6}$。",
 "method": "偶函数余弦展开+端点取值",
 "difficulty": "基础",
 "variant_kind": "偶函数展开:余弦级数并推导巴塞尔和(与奇函数父题不同)",
 "scene_spec": {
  "objects": [
   "坐标图:$y=x^2$($-\\pi\\le x\\le\\pi$)与周期延拓",
   "板书:分部积分计算 $a_n$ 的过程",
   "板书:展开式 $\\frac{\\pi^2}{3}+4\\sum(-1)^n\\cos nx/n^2$",
   "高亮框:取 $x=\\pi$ 得 $\\sum1/n^2=\\pi^2/6$",
   "标签「偶函数⇒纯余弦级数」"
  ],
  "steps": [
   "第一步:画出 $x^2$ 及其周期延拓,说明偶性。",
   "第二步:计算 $a_0$ 与两次分部积分的 $a_n$。",
   "第三步:写出余弦展开式。",
   "第四步:代入 $x=\\pi$,解出巴塞尔和。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c14-02", "category": "数学分析", "sub_category": "傅立叶级数",
 "concept": "傅立叶展开", "concept_id": "C14",
 "parent_training_ids": ["calc-series-020"],
 "problem": r"将 $f(x)=x$($0\le x\le\pi$)展开为正弦级数(作奇延拓)。",
 "solution": r"作奇延拓后在 $[-\pi,\pi]$ 上 $f$ 为奇函数,故 $a_n=0$。$b_n=\frac2\pi\int_0^{\pi}x\sin nx\,dx$。分部积分:$\int_0^{\pi}x\sin nx\,dx=\left.-\frac{x\cos nx}{n}\right|_0^{\pi}+\frac1n\int_0^{\pi}\cos nx\,dx=-\frac{\pi\cos n\pi}{n}+0=\frac{\pi(-1)^{n+1}}{n}$。故 $b_n=\frac{2(-1)^{n+1}}{n}$。正弦展开:$x=\sum_{n=1}^{\infty}\frac{2(-1)^{n+1}}{n}\sin nx$($0<x<\pi$;在端点 $x=0,\pi$ 处级数和为 $0$)。",
 "answer": r"$x=\sum_{n=1}^{\infty}\frac{2(-1)^{n+1}}{n}\sin nx$($0<x<\pi$)。",
 "method": "奇延拓正弦展开(半区间)",
 "difficulty": "基础",
 "variant_kind": "奇延拓:半区间上的正弦级数展开(与全区间父题不同)",
 "scene_spec": {
  "objects": [
   "坐标图:$y=x$ 的奇延拓(贯穿 $[-\\pi,\\pi]$ 的直线段)及其 $2\\pi$ 周期延拓形成的锯齿折线",
   "板书:分部积分计算 $b_n$",
   "板书:展开式 $\\sum 2(-1)^{n+1}\\sin(nx)/n$",
   "动画:部分和逐渐逼近锯齿折线(在跳跃点 $\\pm\\pi$ 处收敛于 $0$)",
   "高亮框:展开式"
  ],
  "steps": [
   "第一步:画出 $x$ 的奇延拓直线段,并展示 $2\\pi$ 周期延拓的锯齿折线。",
   "第二步:由奇性得 $a_n=0$,计算 $b_n$。",
   "第三步:写出正弦展开式。",
   "第四步:动画展示部分和逼近锯齿折线,指出跳跃点处级数和为 $0$(左右极限 $\\pi$ 与 $-\\pi$ 的中点)。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c14-03", "category": "数学分析", "sub_category": "傅立叶级数",
 "concept": "傅立叶展开", "concept_id": "C14",
 "parent_training_ids": ["calc-series-020"],
 "problem": r"将方波 $f(x)=\begin{cases}0,&-\pi<x<0\\1,&0<x<\pi\end{cases}$ 展开为傅立叶级数，并说明在间断点处级数的取值。",
 "solution": r"$a_0=\frac1\pi\int_{-\pi}^{\pi}f(x)\,dx=\frac1\pi\int_0^{\pi}1\,dx=1$。$a_n=\frac1\pi\int_0^{\pi}\cos nx\,dx=\frac{\sin n\pi}{n\pi}=0$($n\ge1$)。$b_n=\frac1\pi\int_0^{\pi}\sin nx\,dx=\frac{1-\cos n\pi}{n\pi}=\frac{1-(-1)^n}{n\pi}$,即奇数项 $b_{2k-1}=\frac{2}{(2k-1)\pi}$,偶数项为 $0$。故 $f(x)=\frac12+\frac{2}{\pi}\sum_{k=1}^{\infty}\frac{\sin(2k-1)x}{2k-1}$。在间断点 $x=0,\pm\pi$ 处,由狄利克雷定理,级数和为左右极限的平均值 $\frac{0+1}{2}=\frac12$。",
 "answer": r"$f=\frac12+\frac{2}{\pi}\sum_{k=1}^{\infty}\frac{\sin(2k-1)x}{2k-1}$;间断点处级数取 $\frac12$(左右极限平均)。",
 "method": "分段函数展开+间断点取值",
 "difficulty": "中等",
 "variant_kind": "分段函数:方波展开与间断点中点取值的狄利克雷定理",
 "scene_spec": {
  "objects": [
   "坐标图:方波(0/1 两段)与周期延拓",
   "板书:$a_0=1$、$a_n=0$、$b_n=(1-(-1)^n)/(n\\pi)$ 的计算",
   "动画:部分和逼近方波,间断点处过冲与中点收敛示意",
   "高亮框:$\\frac12+\\frac{2}{\\pi}\\sum\\frac{\\sin(2k-1)x}{2k-1}$",
   "标签「间断点取左右极限平均」"
  ],
  "steps": [
   "第一步:画出方波及其周期延拓。",
   "第二步:计算各系数,展示 $b_n$ 的奇偶分支。",
   "第三步:写出展开式。",
   "第四步:动画展示部分和逼近与间断点行为。",
   "第五步:高亮间断点取值 $\\frac12$,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c14-04", "category": "数学分析", "sub_category": "傅立叶级数",
 "concept": "傅立叶展开", "concept_id": "C14",
 "parent_training_ids": ["calc-series-020"],
 "problem": r"将 $f(x)=x$($0\le x<2\pi$)作周期 $2\pi$ 延拓,展开为傅立叶级数,并求级数在 $x=0$ 处的和,与狄利克雷定理核对。",
 "solution": r"$a_0=\frac1\pi\int_0^{2\pi}x\,dx=\frac1\pi\cdot\frac{4\pi^2}{2}=2\pi$。$a_n=\frac1\pi\int_0^{2\pi}x\cos nx\,dx=\frac1\pi\left.\left(\frac{x\sin nx}{n}+\frac{\cos nx}{n^2}\right)\right|_0^{2\pi}=0$。$b_n=\frac1\pi\int_0^{2\pi}x\sin nx\,dx=\frac1\pi\left.\left(-\frac{x\cos nx}{n}+\frac{\sin nx}{n^2}\right)\right|_0^{2\pi}=\frac1\pi\left(-\frac{2\pi}{n}\right)=-\frac2n$。故 $f(x)=\pi-\sum_{n=1}^{\infty}\frac{2}{n}\sin nx$。在 $x=0$ 处,周期延拓后的函数有跳跃:$f(0^+)=0$,$f(0^-)=2\pi$,由狄利克雷定理,级数和为 $\frac{0+2\pi}{2}=\pi$;级数在该点各正弦项 $\sin(n\cdot0)=0$,级数和即常数项 $\pi$,两者一致。",
 "answer": r"$f=\pi-\sum_{n=1}^{\infty}\frac{2}{n}\sin nx$;$x=0$ 处级数和为 $\pi$((0+2π)/2,与狄利克雷定理一致)。",
 "method": "周期延拓展开+跳跃点取值核对",
 "difficulty": "中等",
 "variant_kind": "区间变化:0 到 2π 区间的展开与跳跃点狄利克雷核对",
 "scene_spec": {
  "objects": [
   "坐标图:锯齿波($[0,2\\pi)$ 上的 $y=x$ 周期延拓)",
   "板书:$a_0=2\\pi$、$a_n=0$、$b_n=-2/n$ 的计算",
   "板书:展开式 $\\pi-\\sum2\\sin(nx)/n$",
   "高亮框:$x=0$ 处级数和 $=\\pi=(0+2\\pi)/2$",
   "标签「跳跃点取两侧极限平均」"
  ],
  "steps": [
   "第一步:画出锯齿波。",
   "第二步:计算系数,展示 $b_n=-2/n$。",
   "第三步:写出展开式。",
   "第四步:分析 $x=0$ 的跳跃,由狄利克雷定理得和 $\\pi$。",
   "第五步:与级数在该点的值核对,高亮一致。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c14-05", "category": "数学分析", "sub_category": "傅立叶级数",
 "concept": "傅立叶展开", "concept_id": "C14",
 "parent_training_ids": ["calc-series-020"],
 "problem": r"将 $f(x)=1$($0<x<\pi$)分别作正弦展开(奇延拓)与余弦展开(偶延拓),并比较两种展开在区间内部与端点处的收敛行为。",
 "solution": r"正弦展开(奇延拓):奇延拓后为方波($-1,1$ 交替),$b_n=\frac2\pi\int_0^{\pi}\sin nx\,dx=\frac{2(1-(-1)^n)}{n\pi}$,即 $f=1=\frac{4}{\pi}\sum_{k=1}^{\infty}\frac{\sin(2k-1)x}{2k-1}$($0<x<\pi$)。在端点 $x=0,\pi$ 处,奇延拓函数跳跃($1$ 到 $-1$),级数和为左右极限平均 $\frac{1+(-1)}{2}=0$。余弦展开(偶延拓):偶延拓后 $f\equiv1$ 处处连续,$a_0=2$,$a_n=0$($n\ge1$),即 $f=1$ 恰为单项展开,在闭区间 $[0,\pi]$ 上处处成立(包括端点)。比较:同一函数在内部两种展开都收敛到 $1$,但正弦展开在端点收敛到 $0$(由奇延拓的跳跃决定),余弦展开在端点也收敛到 $1$(延拓连续)——延拓方式决定端点行为。",
 "answer": r"正弦展开:$1=\frac{4}{\pi}\sum_{k=1}^{\infty}\frac{\sin(2k-1)x}{2k-1}$($0<x<\pi$),端点取 $0$;余弦展开:$1$ 的单项展开,含端点处处为 $1$。",
 "method": "奇偶延拓对照(端点行为比较)",
 "difficulty": "进阶",
 "variant_kind": "奇偶延拓:同一函数的两种延拓展开与端点收敛行为对照",
 "scene_spec": {
  "objects": [
   "坐标图:奇延拓(方波)与偶延拓(常值 1)的对照图",
   "板书:正弦展开 $\\frac{4}{\\pi}\\sum\\frac{\\sin(2k-1)x}{2k-1}$ 与余弦展开 $1$",
   "动画:正弦部分和逼近,端点处趋于 $0$ 的示意",
   "动画:余弦展开恒为 $1$,端点亦然",
   "高亮框:两法对照表(内部均 1;端点 0 vs 1)"
  ],
  "steps": [
   "第一步:画出奇延拓方波与偶延拓常值的对照。",
   "第二步:计算正弦展开的系数并写出级数。",
   "第三步:动画展示正弦级数在端点收敛到零。",
   "第四步:说明余弦展开恰为单项,端点也成立。",
   "第五步:高亮对照表,总结延拓方式决定端点行为。"
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
