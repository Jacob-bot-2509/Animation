"""batch-17 生成器:三个单条考点各 5 题
(C47 二项到泊松近似 / C48 正态分布与参数 / C49 大数定律)。
全部数学结论由作者逐题手工验算(见 DRAFT_REPORT.md 核算说明);
起草过程未读 eval/test 题文或答案作提示;凡有理数一律分数。
"""
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "draft.jsonl"

DATA = [
# ===================== C47 二项到泊松近似 =====================
{
 "id": "draft-c47-01", "category": "概率论", "sub_category": "极限定理",
 "concept": "二项到泊松近似", "concept_id": "C47",
 "parent_training_ids": ["prob-040"],
 "problem": r"某彩票单张中奖率为 $\frac{1}{1000}$。某人购买 $2000$ 张(设各张彩票是否中奖相互独立)，用泊松近似求他恰中 $3$ 次奖的概率。",
 "solution": r"中奖次数 $X\sim B(2000,\frac{1}{1000})$,$n$ 大 $p$ 小,$\lambda=np=2000\times\frac{1}{1000}=2$。泊松近似:$P(X=3)\approx e^{-2}\frac{2^3}{3!}=e^{-2}\times\frac{8}{6}=e^{-2}\times\frac{4}{3}\approx0.1353\times\frac{4}{3}\approx0.1804$。",
 "answer": r"$P(X=3)\approx e^{-2}\frac{2^3}{3!}=\frac{4}{3}e^{-2}\approx0.180$。",
 "method": "泊松近似(λ=np 代入)",
 "difficulty": "基础",
 "variant_kind": "数值应用:泊松近似的具体数值计算(与定性说明父题不同)",
 "scene_spec": {
  "objects": [
   "板书:$n=2000,p=\\frac{1}{1000},\\lambda=2$",
   "板书:泊松公式代入 $e^{-2}\\frac{2^3}{3!}$",
   "高亮框:$\\approx0.180$",
   "标签「$n$ 大 $p$ 小」"
  ],
  "steps": [
   "第一步:识别二项分布参数。",
   "第二步:计算 $\\lambda=np=2$。",
   "第三步:代入泊松公式。",
   "第四步:计算数值。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c47-02", "category": "概率论", "sub_category": "极限定理",
 "concept": "二项到泊松近似", "concept_id": "C47",
 "parent_training_ids": ["prob-040"],
 "problem": r"设 $X\sim B(100,\frac{1}{100})$。分别用精确公式与泊松近似计算 $P(X=0)$，并比较两者。",
 "solution": r"精确值:$P(X=0)=(1-\frac{1}{100})^{100}=0.99^{100}\approx0.3660$。泊松近似:$\lambda=np=1$,$P(X=0)\approx e^{-1}\approx0.3679$。比较:两者相差约 $0.0018$,相对误差约 $0.5\%$。",
 "answer": r"精确值 $0.99^{100}\approx0.3660$;泊松近似 $e^{-1}\approx0.3679$;相对误差约 $0.5\%$。",
 "method": "精确与近似对照",
 "difficulty": "基础",
 "variant_kind": "精确概率对照:同参数的精确值与近似值比较",
 "scene_spec": {
  "objects": [
   "板书:精确公式 $0.99^{100}$ 与泊松 $e^{-1}$",
   "数轴:两个数值的并排标注",
   "高亮框:相对误差约 $0.5\\%$",
   "标签「近似良好」"
  ],
  "steps": [
   "第一步:写精确公式并计算。",
   "第二步:写泊松近似并计算。",
   "第三步:在数轴上并排标注。",
   "第四步:计算相对误差。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c47-03", "category": "概率论", "sub_category": "极限定理",
 "concept": "二项到泊松近似", "concept_id": "C47",
 "parent_training_ids": ["prob-040"],
 "problem": r"证明:当 $n\to\infty$、$p\to0$ 且 $np\to\lambda>0$ 时，对固定的 $k$，$B(n,p)$ 在 $k$ 处的概率趋于 $\frac{\lambda^k}{k!}e^{-\lambda}$。",
 "solution": r"记 $p_n$ 满足 $np_n\to\lambda$。$P(X=k)=\binom{n}{k}p_n^k(1-p_n)^{n-k}=\frac{n(n-1)\cdots(n-k+1)}{k!}\cdot p_n^k\cdot(1-p_n)^{n-k}$。改写为 $\frac{(np_n)^k}{k!}\cdot\frac{n(n-1)\cdots(n-k+1)}{n^k}\cdot(1-p_n)^{n-k}$。第一因子 $(np_n)^k\to\lambda^k$;第二因子 $\frac{n}{n}\cdot\frac{n-1}{n}\cdots\frac{n-k+1}{n}\to1$($k$ 固定);第三因子 $(1-p_n)^{n-k}=(1-p_n)^{n}/(1-p_n)^k$,其中 $(1-p_n)^n=(1-\frac{np_n}{n})^n\to e^{-\lambda}$ 且 $(1-p_n)^k\to1$。故极限为 $\frac{\lambda^k}{k!}e^{-\lambda}$。",
 "answer": r"证明见解法(三因子分别取极限:$\lambda^k/k!$、$1$、$e^{-\lambda}$)。",
 "method": "极限推导(泊松定理证明)",
 "difficulty": "中等",
 "variant_kind": "稀有事件极限条件:泊松定理的极限推导证明",
 "scene_spec": {
  "objects": [
   "板书:概率公式的三因子分解",
   "板书:各因子的极限分析(高亮三部分)",
   "高亮框:$\\frac{\\lambda^k}{k!}e^{-\\lambda}$",
   "标签「泊松定理」"
  ],
  "steps": [
   "第一步:写出二项概率并分解为三因子。",
   "第二步:分析第一、二因子的极限。",
   "第三步:分析第三因子的极限(含 $e^{-\\lambda}$ 的来源)。",
   "第四步:合并得泊松公式。",
   "第五步:高亮结论,完成证明。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c47-04", "category": "概率论", "sub_category": "极限定理",
 "concept": "二项到泊松近似", "concept_id": "C47",
 "parent_training_ids": ["prob-040"],
 "problem": r"设 $X\sim B(100,\frac12)$。说明为什么不能用泊松分布近似 $X$，并用 $P(X=50)$ 的精确值与泊松近似值对比说明。",
 "solution": r"泊松近似要求 $n$ 大、$p$ 小(稀有事件)且 $\lambda=np$ 适中;此处 $p=\frac12$ 不满足「$p$ 小」,$\lambda=50$ 过大,泊松近似失效。数值对比:精确值 $P(X=50)=\binom{100}{50}(\frac12)^{100}\approx0.0796$(直接计算 $\binom{100}{50}=100891344545564193334812497256$,除以 $2^{100}$ 得 $0.07959$);泊松近似值 $e^{-50}\frac{50^{50}}{50!}\approx0.0563$。两者相差约 $0.023$,相对误差约 $30\%$,近似不可接受。",
 "answer": r"不适用:$p=\frac12$ 不小、$\lambda=50$ 过大;精确值 $\approx0.0796$ 与泊松近似 $\approx0.0563$ 相对误差约 $30\%$。",
 "method": "不适用情形的判定与数值对比",
 "difficulty": "中等",
 "variant_kind": "不适用情形:p 不小/λ 过大时泊松近似失效的判定与对照",
 "scene_spec": {
  "objects": [
   "板书:泊松近似的适用条件清单(n 大、p 小、λ 适中)",
   "板书:$p=\\frac12,\\lambda=50$ 与条件的对照(红色叉号)",
   "数轴:精确值 $0.0796$ 与近似值 $0.0563$ 的差距标注",
   "高亮框:「不适用」"
  ],
  "steps": [
   "第一步:列出泊松近似的适用条件。",
   "第二步:逐条对照题设参数,标出违反项。",
   "第三步:计算精确值。",
   "第四步:计算泊松近似值并对照差距。",
   "第五步:高亮「不适用」结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c47-05", "category": "概率论", "sub_category": "极限定理",
 "concept": "二项到泊松近似", "concept_id": "C47",
 "parent_training_ids": ["prob-040"],
 "problem": r"设 $X\sim B(50,\frac{1}{50})$。分别用精确公式与泊松近似计算 $P(X\le2)$，并比较两者。",
 "solution": r"精确值:$P(X\le2)=p_0+p_1+p_2$,其中 $p_0=0.98^{50}\approx0.3642$;$p_1=50\times\frac{1}{50}\times0.98^{49}=0.98^{49}\approx0.3716$;$p_2=\binom{50}{2}(\frac{1}{50})^2 0.98^{48}=1225\times\frac{1}{2500}\times0.98^{48}\approx0.1858$。故精确值 $\approx0.3642+0.3716+0.1858=0.9216$。泊松近似:$\lambda=1$,$P(X\le2)\approx e^{-1}(1+1+\frac12)=2.5e^{-1}\approx2.5\times0.3679=0.9197$。两者相差约 $0.002$,相对误差约 $0.2\%$。",
 "answer": r"精确值 $\approx0.922$;泊松近似 $\approx0.920$;相对误差约 $0.2\%$。",
 "method": "分布函数近似对照(三项和)",
 "difficulty": "进阶",
 "variant_kind": "分布函数对照:前若干项和的精确值与泊松近似对比",
 "scene_spec": {
  "objects": [
   "板书:精确三项 $p_0+p_1+p_2$ 的逐项计算",
   "板书:泊松近似 $e^{-1}(1+1+\\frac12)$",
   "数轴:两值并排标注",
   "高亮框:相对误差约 $0.2\\%$"
  ],
  "steps": [
   "第一步:逐项计算精确概率。",
   "第二步:求和得精确值。",
   "第三步:计算泊松近似。",
   "第四步:对照两值并计算误差。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
# ===================== C48 正态分布与参数 =====================
{
 "id": "draft-c48-01", "category": "概率论", "sub_category": "正态分布",
 "concept": "正态分布与参数", "concept_id": "C48",
 "parent_training_ids": ["prob-041"],
 "problem": r"设 $X\sim N(2,9)$。求 $P(X\le5)$。",
 "solution": r"标准化:$Z=\frac{X-2}{3}\sim N(0,1)$。$P(X\le5)=P\left(Z\le\frac{5-2}{3}\right)=P(Z\le1)=\Phi(1)\approx0.8413$。",
 "answer": r"$P(X\le5)=\Phi(1)\approx0.8413$。",
 "method": "标准化查表",
 "difficulty": "基础",
 "variant_kind": "标准化:非标准正态的概率计算(与形状分析父题不同)",
 "scene_spec": {
  "objects": [
   "坐标图:$N(2,9)$ 的钟形曲线与 $x=5$ 的阴影面积",
   "板书:标准化 $Z=\\frac{X-2}{3}$",
   "高亮框:$\\Phi(1)\\approx0.8413$"
  ],
  "steps": [
   "第一步:画出钟形曲线。",
   "第二步:标准化并标出对应 $z$ 值。",
   "第三步:查表得概率。",
   "第四步:高亮结果。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c48-02", "category": "概率论", "sub_category": "正态分布",
 "concept": "正态分布与参数", "concept_id": "C48",
 "parent_training_ids": ["prob-041"],
 "problem": r"设 $X\sim N(0,1)$。求 $P(-1\le X\le1)$、$P(-2\le X\le2)$、$P(-3\le X\le3)$(即 $3\sigma$ 规则)。",
 "solution": r"由对称性,$P(-k\le X\le k)=2\Phi(k)-1$。$k=1$:$2\Phi(1)-1\approx2\times0.8413-1=0.6826$。$k=2$:$2\Phi(2)-1\approx2\times0.9772-1=0.9544$。$k=3$:$2\Phi(3)-1\approx2\times0.9987-1=0.9974$。即正态变量落在均值附近 $1,2,3$ 个标准差内的概率分别约为 $68\%$、$95\%$、$99.7\%$。",
 "answer": r"$0.6826$、$0.9544$、$0.9974$($3\sigma$ 规则)。",
 "method": "对称性+标准正态表",
 "difficulty": "基础",
 "variant_kind": "区间概率与对称性:3σ 规则的数值验证",
 "scene_spec": {
  "objects": [
   "坐标图:标准正态曲线与三组对称区间阴影",
   "板书:$2\\Phi(k)-1$ 的公式",
   "高亮框:三组概率 $68\\%$、$95\\%$、$99.7\\%$"
  ],
  "steps": [
   "第一步:画出标准正态曲线。",
   "第二步:依次阴影标注三组对称区间。",
   "第三步:计算三组概率。",
   "第四步:高亮 3σ 规则。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c48-03", "category": "概率论", "sub_category": "正态分布",
 "concept": "正态分布与参数", "concept_id": "C48",
 "parent_training_ids": ["prob-041"],
 "problem": r"设 $X\sim N(\mu,4)$。求使 $P(X\le a)=0.95$ 的 $a$(用 $\mu$ 表示)。",
 "solution": r"标准化:$P\left(Z\le\frac{a-\mu}{2}\right)=0.95$,即 $\Phi\left(\frac{a-\mu}{2}\right)=0.95$。查表 $\Phi(1.645)\approx0.95$,故 $\frac{a-\mu}{2}=1.645$,$a=\mu+2\times1.645=\mu+3.29$。",
 "answer": r"$a=\mu+3.29$(即 $\mu+2\times1.645$)。",
 "method": "分位数反求",
 "difficulty": "中等",
 "variant_kind": "参数区间:分位数反求与参数表示",
 "scene_spec": {
  "objects": [
   "坐标图:钟形曲线与 $0.95$ 分位数的阴影面积",
   "板书:标准化与查表 $1.645$",
   "高亮框:$a=\\mu+3.29$"
  ],
  "steps": [
   "第一步:标出 $0.95$ 的分位点。",
   "第二步:标准化并查表。",
   "第三步:反解 $a$。",
   "第四步:高亮结果。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c48-04", "category": "概率论", "sub_category": "正态分布",
 "concept": "正态分布与参数", "concept_id": "C48",
 "parent_training_ids": ["prob-041"],
 "problem": r"设 $X\sim N(1,4)$ 与 $Y\sim N(2,9)$ 相互独立。求 $X+Y$ 与 $2X-Y$ 的分布，并求 $P(2X-Y>0)$。",
 "solution": r"正态分布的可加性:$X+Y\sim N(1+2,\,4+9)=N(3,13)$。线性组合:$2X-Y\sim N(2\times1-2,\,4\times4+1\times9)=N(0,25)$。由对称性($N(0,25)$ 关于 $0$ 对称),$P(2X-Y>0)=\frac12$。",
 "answer": r"$X+Y\sim N(3,13)$;$2X-Y\sim N(0,25)$;$P(2X-Y>0)=\frac12$。",
 "method": "正态线性组合+对称性",
 "difficulty": "中等",
 "variant_kind": "线性组合:独立正态变量的和与线性组合分布",
 "scene_spec": {
  "objects": [
   "板书:两个分布及其参数",
   "板书:和的均值方差计算",
   "板书:线性组合的均值方差计算",
   "高亮框:$N(0,25)$ 对称,$P(>0)=\\frac12$"
  ],
  "steps": [
   "第一步:写出两个正态分布。",
   "第二步:计算 $X+Y$ 的分布。",
   "第三步:计算 $2X-Y$ 的分布。",
   "第四步:由对称性得概率。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c48-05", "category": "概率论", "sub_category": "正态分布",
 "concept": "正态分布与参数", "concept_id": "C48",
 "parent_training_ids": ["prob-041"],
 "problem": r"用特征函数证明:若 $X\sim N(\mu_1,\sigma_1^2)$ 与 $Y\sim N(\mu_2,\sigma_2^2)$ 相互独立，则 $X+Y\sim N(\mu_1+\mu_2,\sigma_1^2+\sigma_2^2)$。",
 "solution": r"正态分布的特征函数为 $\varphi_X(t)=e^{i\mu_1t-\frac{\sigma_1^2t^2}{2}}$。由独立性,和的特征函数为乘积:$\varphi_{X+Y}(t)=\varphi_X(t)\varphi_Y(t)=e^{i\mu_1t-\frac{\sigma_1^2t^2}{2}}\cdot e^{i\mu_2t-\frac{\sigma_2^2t^2}{2}}=e^{i(\mu_1+\mu_2)t-\frac{(\sigma_1^2+\sigma_2^2)t^2}{2}}$。这正是 $N(\mu_1+\mu_2,\sigma_1^2+\sigma_2^2)$ 的特征函数,而特征函数唯一决定分布,故 $X+Y\sim N(\mu_1+\mu_2,\sigma_1^2+\sigma_2^2)$。",
 "answer": r"证明见解法(特征函数乘积:$e^{i(\mu_1+\mu_2)t-(\sigma_1^2+\sigma_2^2)t^2/2}$)。",
 "method": "特征函数证明可加性",
 "difficulty": "进阶",
 "variant_kind": "证明型:正态可加性的特征函数证明",
 "scene_spec": {
  "objects": [
   "板书:两个正态的特征函数",
   "板书:独立性下的乘积",
   "板书:合并指数得和分布的特征函数",
   "高亮框:$N(\\mu_1+\\mu_2,\\sigma_1^2+\\sigma_2^2)$"
  ],
  "steps": [
   "第一步:写出特征函数公式。",
   "第二步:由独立性相乘。",
   "第三步:合并指数。",
   "第四步:识别为和分布的特征函数。",
   "第五步:由唯一性得结论,完成证明。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
# ===================== C49 大数定律 =====================
{
 "id": "draft-c49-01", "category": "概率论", "sub_category": "极限定理",
 "concept": "大数定律", "concept_id": "C49",
 "parent_training_ids": ["prob-042"],
 "problem": r"设随机变量 $X$ 的均值为 $5$、方差为 $1$。用切比雪夫不等式估计 $P(|X-5|\ge3)$ 的上界。",
 "solution": r"切比雪夫不等式:$P(|X-EX|\ge\varepsilon)\le\frac{Var(X)}{\varepsilon^2}$。取 $\varepsilon=3$:$P(|X-5|\ge3)\le\frac{1}{3^2}=\frac19$。",
 "answer": r"$P(|X-5|\ge3)\le\frac19$。",
 "method": "切比雪夫不等式",
 "difficulty": "基础",
 "variant_kind": "不等式应用:切比雪夫上界的数值计算",
 "scene_spec": {
  "objects": [
   "板书:切比雪夫不等式公式",
   "板书:代入 $\\varepsilon=3$",
   "高亮框:$\\frac19$"
  ],
  "steps": [
   "第一步:写出不等式。",
   "第二步:代入数值。",
   "第三步:得上界 $\\frac19$。",
   "第四步:高亮结论。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c49-02", "category": "概率论", "sub_category": "极限定理",
 "concept": "大数定律", "concept_id": "C49",
 "parent_training_ids": ["prob-042"],
 "problem": r"说明依概率收敛与几乎必然收敛的区别，并说明大数定律(频率趋于概率)属于哪一种收敛。",
 "solution": r"定义:几乎必然收敛($X_n\xrightarrow{a.s.}X$)指 $P(\{\omega:\lim X_n(\omega)=X(\omega)\})=1$,即几乎每个样本路径最终都收敛;依概率收敛($X_n\xrightarrow{P}X$)指对任意 $\varepsilon>0$,$\lim_{n}P(|X_n-X|>\varepsilon)=0$,只要求偏差大的概率趋于零,不要求逐点路径最终稳定。关系:几乎必然收敛蕴含依概率收敛,反之不成立(可构造 $X_n$ 为「越来越窄但不断游走的脉冲」序列,依概率收敛于 $0$ 但几乎必然不收敛)。大数定律:频率 $\frac{S_n}{n}$ 依概率收敛于概率 $p$(弱大数定律);加强形式(强大数定律)给出几乎必然收敛。",
 "answer": r"区别与蕴含关系见解法(几乎必然⟹依概率,反之不然);(弱)大数定律给的是依概率收敛。",
 "method": "收敛方式辨析(定义对照)",
 "difficulty": "基础",
 "variant_kind": "收敛方式:依概率与几乎必然收敛的辨析与大数定律定位",
 "scene_spec": {
  "objects": [
   "板书:两种收敛的定义对照",
   "动画:几乎必然收敛(路径最终稳定)与依概率收敛(偏差概率趋于零)的示意",
   "高亮框:几乎必然⟹依概率,反之不然",
   "标签「大数定律:依概率收敛」"
  ],
  "steps": [
   "第一步:写出两种收敛的定义。",
   "第二步:动画对照两种收敛行为。",
   "第三步:说明蕴含关系与反例思想。",
   "第四步:指出大数定律的收敛类型。",
   "第五步:高亮总结。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c49-03", "category": "概率论", "sub_category": "极限定理",
 "concept": "大数定律", "concept_id": "C49",
 "parent_training_ids": ["prob-042"],
 "problem": r"设 $X_1,\dots,X_{100}$ 独立同分布于 $U(0,1)$。用切比雪夫不等式估计 $P(|\bar X-\frac12|>0.1)$ 的上界。",
 "solution": r"$E\bar X=\frac12$。$Var(X_1)=\frac{1}{12}$,$Var(\bar X)=\frac{1/12}{100}=\frac{1}{1200}$。切比雪夫:$P(|\bar X-\frac12|>0.1)\le\frac{Var(\bar X)}{0.1^2}=\frac{1/1200}{1/100}=\frac{1}{12}$。",
 "answer": r"上界为 $\frac{1}{12}\approx0.083$。",
 "method": "切比雪夫+样本均值方差",
 "difficulty": "中等",
 "variant_kind": "大数定律定量:样本均值偏离概率的切比雪夫上界",
 "scene_spec": {
  "objects": [
   "板书:$Var(\\bar X)=\\frac{1}{1200}$ 的计算",
   "板书:切比雪夫代入",
   "高亮框:$\\frac{1}{12}$",
   "标签「大数定律的定量版本」"
  ],
  "steps": [
   "第一步:计算样本均值的方差。",
   "第二步:代入切比雪夫不等式。",
   "第三步:得上界 $\\frac{1}{12}$。",
   "第四步:高亮结论。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c49-04", "category": "概率论", "sub_category": "极限定理",
 "concept": "大数定律", "concept_id": "C49",
 "parent_training_ids": ["prob-042"],
 "problem": r"证明切比雪夫大数定律:若随机变量序列 $X_1,X_2,\dots$ 两两不相关，且存在常数 $C$ 使 $Var(X_i)\le C$ 对一切 $i$ 成立，则 $\frac{1}{n}\sum_{i=1}^{n}(X_i-EX_i)\xrightarrow{P}0$。",
 "solution": r"令 $S_n=\frac1n\sum_{i=1}^{n}(X_i-EX_i)$。$ES_n=0$。由两两不相关,$Var(S_n)=\frac{1}{n^2}\sum_{i=1}^{n}Var(X_i)\le\frac{nC}{n^2}=\frac{C}{n}$(协方差项全为零)。由切比雪夫不等式,对任意 $\varepsilon>0$,$P(|S_n|\ge\varepsilon)\le\frac{Var(S_n)}{\varepsilon^2}\le\frac{C}{n\varepsilon^2}\to0$。故 $S_n\xrightarrow{P}0$。",
 "answer": r"证明见解法(两两不相关使方差无交叉项:$Var(S_n)\le C/n\to0$,切比雪夫得依概率收敛)。",
 "method": "不相关条件下的证明",
 "difficulty": "中等",
 "variant_kind": "相关样本的适用条件:两两不相关(无需独立)下的切比雪夫大数定律证明",
 "scene_spec": {
  "objects": [
   "板书:样本均值的方差展开(交叉项为零)",
   "板书:$Var(S_n)\\le\\frac{C}{n}$",
   "板书:切比雪夫代入取极限",
   "高亮框:$S_n\\xrightarrow{P}0$"
  ],
  "steps": [
   "第一步:写出样本均值。",
   "第二步:展开方差,说明协方差项为零。",
   "第三步:得方差上界 $C/n$。",
   "第四步:切比雪夫不等式取极限。",
   "第五步:高亮结论,完成证明。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c49-05", "category": "概率论", "sub_category": "极限定理",
 "concept": "大数定律", "concept_id": "C49",
 "parent_training_ids": ["prob-042"],
 "problem": r"证明(切比雪夫)大数定律:若 $X_1,X_2,\dots$ 独立同分布,均值 $\mu$ 与方差 $\sigma^2$ 均有限,则样本均值 $\bar X_n=\frac1n\sum_{i=1}^{n}X_i$ 依概率收敛于 $\mu$。",
 "solution": r"$E\bar X_n=\mu$。由独立性,$Var(\bar X_n)=\frac{1}{n^2}\sum_{i=1}^{n}Var(X_i)=\frac{\sigma^2}{n}$。对任意 $\varepsilon>0$,由切比雪夫不等式,$P(|\bar X_n-\mu|\ge\varepsilon)\le\frac{Var(\bar X_n)}{\varepsilon^2}=\frac{\sigma^2}{n\varepsilon^2}\to0$($n\to\infty$)。这正是依概率收敛的定义,故 $\bar X_n\xrightarrow{P}\mu$。",
 "answer": r"证明见解法(独立同分布使 $Var(\bar X_n)=\sigma^2/n$,切比雪夫得收敛)。",
 "method": "大数定律的完整证明",
 "difficulty": "进阶",
 "variant_kind": "证明型:切比雪夫大数定律的完整证明",
 "scene_spec": {
  "objects": [
   "板书:样本均值的期望与方差",
   "板书:切比雪夫不等式代入",
   "板书:取极限得零",
   "高亮框:$\\bar X_n\\xrightarrow{P}\\mu$"
  ],
  "steps": [
   "第一步:计算样本均值的期望。",
   "第二步:计算方差($\\sigma^2/n$)。",
   "第三步:切比雪夫不等式给出上界。",
   "第四步:取极限。",
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
