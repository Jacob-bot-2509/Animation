"""batch-06 生成器:三个单条考点各 5 题
(C03 二重积分与区域 / C05 函数极限 / C46 几何概型)。
全部数学结论由作者逐题手工验算(见 DRAFT_REPORT.md 核算说明);
起草过程未读 eval/test 题文或答案作提示;凡有理数一律分数。
"""
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "draft.jsonl"

DATA = [
# ===================== C03 二重积分与区域 =====================
{
 "id": "draft-c03-01", "category": "数学分析", "sub_category": "二重积分",
 "concept": "二重积分与区域", "concept_id": "C03",
 "parent_training_ids": ["calc-double-integral-004"],
 "problem": r"求二重积分 $\iint_D xy\,dxdy$，其中 $D=[0,1]\times[0,2]$。",
 "solution": r"矩形区域上被积函数可分离：$\iint_D xy\,dxdy=\left(\int_0^1x\,dx\right)\left(\int_0^2y\,dy\right)=\frac12\times\frac{2^2}{2}=\frac12\times2=1$。",
 "answer": r"积分值为 $1$。",
 "method": "矩形区域分离变量积分",
 "difficulty": "基础",
 "variant_kind": "区域类型变化:矩形区域的分离变量计算(与圆盘几何意义父题不同)",
 "scene_spec": {
  "objects": [
   "平面坐标系:矩形区域 $D=[0,1]\\times[0,2]$(阴影)",
   "曲面 $z=xy$ 在区域上方的示意",
   "板书:$\\iint_D xy\\,dxdy=(\\int_0^1x\\,dx)(\\int_0^2y\\,dy)$",
   "高亮框:结果 $1$",
   "标签「可分离变量」"
  ],
  "steps": [
   "第一步:画出矩形区域 $D$,阴影标注。",
   "第二步:展示曲面 $z=xy$ 在区域上方。",
   "第三步:把二重积分拆成两个一元积分之积。",
   "第四步:分别计算两个一元积分。",
   "第五步:高亮结果 $1$。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c03-02", "category": "数学分析", "sub_category": "二重积分",
 "concept": "二重积分与区域", "concept_id": "C03",
 "parent_training_ids": ["calc-double-integral-004"],
 "problem": r"求二重积分 $\iint_D x^2\,dxdy$，其中 $D$ 由 $y=x$、$y=0$、$x=1$ 围成；并换一种积分次序重算验证。",
 "solution": r"先对 $y$ 积分：$\iint_D x^2\,dxdy=\int_0^1\int_0^x x^2\,dy\,dx=\int_0^1 x^3\,dx=\frac14$。换序(先对 $x$)：区域改写为 $0\le y\le1$，$y\le x\le1$，故 $\iint_D x^2\,dxdy=\int_0^1\int_y^1 x^2\,dx\,dy=\int_0^1\frac{1-y^3}{3}\,dy=\frac{1-\frac14}{3}=\frac14$。两种次序结果一致。",
 "answer": r"积分值为 $\frac14$(两种积分次序结果一致)。",
 "method": "三角形区域积分(两种次序对照)",
 "difficulty": "基础",
 "variant_kind": "换积分次序:三角形区域两种次序的对照验证",
 "scene_spec": {
  "objects": [
   "平面坐标系:三角形区域 $D$(由 $y=x,y=0,x=1$ 围成,阴影)",
   "板书:先对 $y$ 积分的累次积分 $\\int_0^1\\int_0^x x^2\\,dy\\,dx$",
   "板书:换序后的累次积分 $\\int_0^1\\int_y^1 x^2\\,dx\\,dy$",
   "高亮框:两者均得 $\\frac14$",
   "标签「积分次序可交换」"
  ],
  "steps": [
   "第一步:画出三角形区域并写出边界方程。",
   "第二步:展示先对 $y$ 积分的累次积分并计算。",
   "第三步:改写区域为 $0\\le y\\le1,y\\le x\\le1$,展示换序后的积分。",
   "第四步:计算换序结果,两法均为 $\\frac14$。",
   "第五步:标注积分次序可交换,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c03-03", "category": "数学分析", "sub_category": "二重积分",
 "concept": "二重积分与区域", "concept_id": "C03",
 "parent_training_ids": ["calc-double-integral-004"],
 "problem": r"用极坐标求二重积分 $\iint_D (x^2+y^2)\,dxdy$，其中 $D$ 为圆盘 $x^2+y^2\le4$ 在第一象限的部分。",
 "solution": r"极坐标:$x=r\cos\theta,y=r\sin\theta$,雅可比为 $r$。区域:$0\le r\le2$,$0\le\theta\le\frac{\pi}{2}$。$\iint_D (x^2+y^2)\,dxdy=\int_0^{\frac{\pi}{2}}\int_0^2 r^2\cdot r\,dr\,d\theta=\int_0^{\frac{\pi}{2}}d\theta\cdot\int_0^2 r^3\,dr=\frac{\pi}{2}\times\frac{2^4}{4}=\frac{\pi}{2}\times4=2\pi$。",
 "answer": r"积分值为 $2\pi$。",
 "method": "极坐标变换(雅可比 $r$)",
 "difficulty": "中等",
 "variant_kind": "坐标变换:极坐标与雅可比因子的应用(圆域上径向积)",
 "scene_spec": {
  "objects": [
   "平面坐标系:第一象限四分之一圆盘(阴影)",
   "板书:极坐标替换 $x=r\\cos\\theta,y=r\\sin\\theta$,雅可比 $r$",
   "板书:$\\int_0^{\\pi/2}\\int_0^2 r^3\\,dr\\,d\\theta$",
   "高亮框:结果 $2\\pi$",
   "标签「极坐标雅可比 $r$」"
  ],
  "steps": [
   "第一步:画出四分之一圆盘,标注极坐标范围。",
   "第二步:写出极坐标替换与雅可比因子 $r$。",
   "第三步:把被积函数化为 $r^2$,积分化为 $\\int\\int r^3\\,dr\\,d\\theta$。",
   "第四步:分离变量计算,得 $2\\pi$。",
   "第五步:标注极坐标雅可比的来源,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c03-04", "category": "数学分析", "sub_category": "二重积分",
 "concept": "二重积分与区域", "concept_id": "C03",
 "parent_training_ids": ["calc-double-integral-004"],
 "problem": r"求二重积分 $\iint_D y\,dxdy$，其中 $D$ 为上半圆盘 $x^2+y^2\le1$，$y\ge0$；并说明在全圆盘上的积分值及其理由。",
 "solution": r"极坐标:$0\le r\le1$,$0\le\theta\le\pi$。$\iint_D y\,dxdy=\int_0^{\pi}\int_0^1 (r\sin\theta)\,r\,dr\,d\theta=\int_0^{\pi}\sin\theta\,d\theta\cdot\int_0^1 r^2\,dr=2\times\frac13=\frac23$。(直角坐标验证:$\int_{-1}^{1}\int_0^{\sqrt{1-x^2}}y\,dy\,dx=\int_{-1}^{1}\frac{1-x^2}{2}\,dx=\frac23$。)全圆盘上被积函数 $y$ 关于 $x$ 轴为奇函数,区域关于 $x$ 轴对称,故积分为 $0$。",
 "answer": r"上半圆盘上积分为 $\frac23$;全圆盘上积分为 $0$(奇对称性)。",
 "method": "极坐标+对称性(奇函数抵消)",
 "difficulty": "中等",
 "variant_kind": "对称性与符号:上半圆盘积分与全圆盘奇对称抵消的对照",
 "scene_spec": {
  "objects": [
   "平面坐标系:上半圆盘(阴影)与全圆盘(虚线轮廓)",
   "板书:极坐标积分 $\\int_0^{\\pi}\\int_0^1 r^2\\sin\\theta\\,dr\\,d\\theta$",
   "高亮框:$\\frac23$",
   "动画:全圆盘上下两半关于 $x$ 轴对称的抵消示意",
   "标签「奇函数+对称区域 ⟹ 积分 0」"
  ],
  "steps": [
   "第一步:画出上半圆盘,写极坐标范围。",
   "第二步:化为累次积分并分离变量,得 $\\frac23$。",
   "第三步:用直角坐标重算验证,结果一致。",
   "第四步:动画展示全圆盘上下两半的对称抵消。",
   "第五步:总结奇对称性结论:全圆盘积分为 $0$。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c03-05", "category": "数学分析", "sub_category": "二重积分",
 "concept": "二重积分与区域", "concept_id": "C03",
 "parent_training_ids": ["calc-double-integral-004"],
 "problem": r"用变量替换 $u=x+y$，$v=x-y$ 求二重积分 $\iint_D (x+y)\,dxdy$，其中 $D=[0,1]\times[0,1]$。",
 "solution": r"雅可比:$\frac{\partial(u,v)}{\partial(x,y)}=\begin{vmatrix}1&1\\1&-1\end{vmatrix}=-2$,故 $dxdy=\frac12\,du\,dv$。区域变换:由 $x=\frac{u+v}{2},y=\frac{u-v}{2}$ 与 $0\le x,y\le1$ 得 $0\le u\le2$,且当 $0\le u\le1$ 时 $-u\le v\le u$;当 $1\le u\le2$ 时 $u-2\le v\le2-u$(菱形)。于是 $\iint_D(x+y)\,dxdy=\int_0^1\int_{-u}^{u}\frac{u}{2}\,dv\,du+\int_1^2\int_{u-2}^{2-u}\frac{u}{2}\,dv\,du=\int_0^1u^2\,du+\int_1^2(2u-u^2)\,du=\frac13+\left(\left.u^2-\frac{u^3}{3}\right|_1^2\right)=\frac13+\left[(4-\frac83)-(1-\frac13)\right]=\frac13+\frac23=1$。直角坐标直算验证:$\int_0^1\int_0^1(x+y)\,dx\,dy=\int_0^1(\frac12+y)\,dy=1$。",
 "answer": r"积分值为 $1$(雅可比 $\frac12$,菱形区域分两段)。",
 "method": "一般变量替换(雅可比+区域变换)",
 "difficulty": "进阶",
 "variant_kind": "结构升级:线性变量替换的雅可比与菱形区域分段,与直角坐标直算互验",
 "scene_spec": {
  "objects": [
   "平面坐标系:正方形区域 $D$ 与 $(u,v)$ 平面的菱形区域(变换示意箭头)",
   "板书:雅可比 $\\begin{vmatrix}1&1\\\\1&-1\\end{vmatrix}=-2$,故 $dxdy=\\frac12\\,dudv$",
   "板书:菱形区域的两段积分(按 $u$ 分 $[0,1]$ 与 $[1,2]$)",
   "高亮框:结果 $1$",
   "验证板书:直角坐标直算 $\\int_0^1(\\frac12+y)dy=1$"
  ],
  "steps": [
   "第一步:画出正方形区域与线性变换的几何示意。",
   "第二步:计算雅可比行列式,得 $dxdy=\\frac12\\,dudv$。",
   "第三步:推导 $(u,v)$ 平面的菱形区域,说明需按 $u$ 分两段。",
   "第四步:分段积分得 $\\frac13+\\frac23=1$。",
   "第五步:直角坐标直算验证,两法一致。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
# ===================== C05 函数极限 =====================
{
 "id": "draft-c05-01", "category": "数学分析", "sub_category": "函数极限",
 "concept": "函数极限", "concept_id": "C05",
 "parent_training_ids": ["calc-limit-006"],
 "problem": r"求极限 $\lim_{x\to\infty}\frac{x^2+3x+1}{2x^2-x+5}$。",
 "solution": r"分子分母同除以最高次项 $x^2$:$\frac{x^2+3x+1}{2x^2-x+5}=\frac{1+\frac3x+\frac1{x^2}}{2-\frac1x+\frac5{x^2}}$。当 $x\to\infty$ 时,$\frac3x,\frac1x,\frac1{x^2},\frac5{x^2}$ 均趋于 $0$,故极限为 $\frac{1}{2}$。",
 "answer": r"极限为 $\frac12$。",
 "method": "最高次项主导法",
 "difficulty": "基础",
 "variant_kind": "增长类型:多项式比值的主导项分析(与三角函数极限父题不同)",
 "scene_spec": {
  "objects": [
   "板书:分式 $\\frac{x^2+3x+1}{2x^2-x+5}$",
   "板书:分子分母同除 $x^2$ 的变形",
   "动画:低阶项系数随 $x$ 增大逐渐「缩水」的示意",
   "高亮框:$\\frac12$",
   "标签「最高次项主导」"
  ],
  "steps": [
   "第一步:写出分式,标出分子分母的最高次项。",
   "第二步:同除以 $x^2$,展示各项变形。",
   "第三步:说明低阶项趋于 $0$。",
   "第四步:高亮极限 $\\frac12$。",
   "第五步:总结最高次项主导的原则。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c05-02", "category": "数学分析", "sub_category": "函数极限",
 "concept": "函数极限", "concept_id": "C05",
 "parent_training_ids": ["calc-limit-006"],
 "problem": r"求 $\lim_{x\to0^+}\frac{|x|}{x}$ 与 $\lim_{x\to0^-}\frac{|x|}{x}$，并判断 $\lim_{x\to0}\frac{|x|}{x}$ 是否存在。",
 "solution": r"当 $x>0$ 时,$|x|=x$,故 $\frac{|x|}{x}=1$,右极限为 $1$。当 $x<0$ 时,$|x|=-x$,故 $\frac{|x|}{x}=-1$,左极限为 $-1$。左右极限不相等,故 $\lim_{x\to0}\frac{|x|}{x}$ 不存在。",
 "answer": r"右极限 $1$,左极限 $-1$;$\lim_{x\to0}\frac{|x|}{x}$ 不存在。",
 "method": "单侧极限对比",
 "difficulty": "基础",
 "variant_kind": "单侧极限:左右极限不等导致极限不存在(含绝对值分支)",
 "scene_spec": {
  "objects": [
   "平面坐标系:函数 $\\frac{|x|}{x}$ 的图像(右半直线 $y=1$,左半直线 $y=-1$)",
   "两个空心圆点:$(0,1)$ 与 $(0,-1)$",
   "动画:从右侧与左侧分别趋近 $x=0$ 的箭头",
   "板书:右极限 $1$,左极限 $-1$",
   "红色标签「极限不存在」"
  ],
  "steps": [
   "第一步:画出函数图像,两段水平线在原点处断开。",
   "第二步:从右侧趋近,展示右极限为 $1$。",
   "第三步:从左侧趋近,展示左极限为 $-1$。",
   "第四步:对比左右极限,不相等。",
   "第五步:红色标注极限不存在,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c05-03", "category": "数学分析", "sub_category": "函数极限",
 "concept": "函数极限", "concept_id": "C05",
 "parent_training_ids": ["calc-limit-006"],
 "problem": r"求极限 $\lim_{x\to+\infty}\left(\sqrt{x^2+2x}-x\right)$。",
 "solution": r"分子有理化(当 $x>0$ 时):$\sqrt{x^2+2x}-x=\frac{(x^2+2x)-x^2}{\sqrt{x^2+2x}+x}=\frac{2x}{\sqrt{x^2+2x}+x}=\frac{2}{\sqrt{1+\frac2x}+1}$(分子分母同除以 $x$,$x>0$ 时 $\sqrt{x^2+2x}=x\sqrt{1+\frac2x}$)。当 $x\to+\infty$ 时,$\frac2x\to0$,极限为 $\frac{2}{\sqrt1+1}=1$。",
 "answer": r"极限为 $1$。",
 "method": "分子有理化(无穷减无穷消主项)",
 "difficulty": "中等",
 "variant_kind": "消去主项:无穷减无穷型的有理化处理",
 "scene_spec": {
  "objects": [
   "板书:$\\sqrt{x^2+2x}-x$(标出两个无穷大项)",
   "板书:有理化变形 $\\frac{2x}{\\sqrt{x^2+2x}+x}$",
   "板书:同除 $x$ 得 $\\frac{2}{\\sqrt{1+\\frac2x}+1}$",
   "高亮框:$1$",
   "标签「有理化消主项」"
  ],
  "steps": [
   "第一步:写出表达式,标注两无穷大项相减。",
   "第二步:分子有理化,展示平方差变形。",
   "第三步:分子分母同除 $x$。",
   "第四步:令 $\\frac2x\\to0$,得极限 $1$。",
   "第五步:总结有理化消主项的方法。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c05-04", "category": "数学分析", "sub_category": "函数极限",
 "concept": "函数极限", "concept_id": "C05",
 "parent_training_ids": ["calc-limit-006"],
 "problem": r"求 $\lim_{x\to+\infty}\frac{x^3}{e^x}$ 与 $\lim_{x\to+\infty}\frac{\ln x}{\sqrt{x}}$，并说明它们反映的增长等级关系。",
 "solution": r"对 $\frac{x^3}{e^x}$ 连续三次使用洛必达法则:$\lim_{x\to+\infty}\frac{x^3}{e^x}=\lim\frac{3x^2}{e^x}=\lim\frac{6x}{e^x}=\lim\frac{6}{e^x}=0$。对 $\frac{\ln x}{\sqrt{x}}$:$\lim_{x\to+\infty}\frac{\ln x}{\sqrt{x}}=\lim\frac{1/x}{1/(2\sqrt{x})}=\lim\frac{2}{\sqrt{x}}=0$。两者均为 $0$,反映增长等级:$e^x$ 远快于多项式 $x^3$,而 $x^3$(进而 $\sqrt{x}$)远快于 $\ln x$,即 $e^x\gg x^3\gg\sqrt{x}\gg\ln x$。",
 "answer": r"两者均为 $0$;反映增长等级 $e^x\gg x^3\gg\sqrt{x}\gg\ln x$。",
 "method": "洛必达法则(跨类型增长对比)",
 "difficulty": "中等",
 "variant_kind": "增长类型对比:指数/多项式/对数三类增长的极限与等级排序",
 "scene_spec": {
  "objects": [
   "板书:$\\lim\\frac{x^3}{e^x}$ 的三次洛必达链条",
   "板书:$\\lim\\frac{\\ln x}{\\sqrt{x}}$ 的洛必达过程",
   "坐标图:四条增长曲线 $e^x$、$x^3$、$\\sqrt{x}$、$\\ln x$ 的对比(斜率拉开动画)",
   "高亮框:两个极限均为 $0$",
   "标签「$e^x\\gg x^3\\gg\\sqrt{x}\\gg\\ln x$」"
  ],
  "steps": [
   "第一步:展示 $\\frac{x^3}{e^x}$ 的三次洛必达,得 $0$。",
   "第二步:展示 $\\frac{\\ln x}{\\sqrt{x}}$ 的洛必达,得 $0$。",
   "第三步:画出四条增长曲线,动画展示增长差距拉开。",
   "第四步:高亮两个极限值。",
   "第五步:标注增长等级排序,总结指数快于多项式快于对数。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c05-05", "category": "数学分析", "sub_category": "函数极限",
 "concept": "函数极限", "concept_id": "C05",
 "parent_training_ids": ["calc-limit-006"],
 "problem": r"证明 $\lim_{x\to0}\sin\frac{1}{x}$ 不存在。",
 "solution": r"取两个趋于 $0$ 的数列:$x_n=\frac{1}{2n\pi}$,则 $x_n\to0$ 且 $\sin\frac{1}{x_n}=\sin(2n\pi)=0\to0$。再取 $y_n=\frac{1}{2n\pi+\frac{\pi}{2}}$,则 $y_n\to0$ 且 $\sin\frac{1}{y_n}=\sin(2n\pi+\frac{\pi}{2})=1\to1$。两个数列都趋于 $0$,但函数值分别趋于 $0$ 与 $1$。由海涅定理(归结原则),若 $\lim_{x\to0}\sin\frac1x$ 存在,则沿任何趋于 $0$ 的数列函数值应收敛到同一极限,矛盾。故极限不存在。",
 "answer": r"极限不存在(取 $x_n=\frac{1}{2n\pi}$ 与 $y_n=\frac{1}{2n\pi+\frac\pi2}$ 两列,函数值分别趋于 $0$ 与 $1$,由海涅定理得矛盾)。",
 "method": "海涅定理反证(两列逼近不同值)",
 "difficulty": "进阶",
 "variant_kind": "证明型:极限不存在性的严格证明(归结原则+双数列),非计算",
 "scene_spec": {
  "objects": [
   "平面坐标系:函数 $\\sin\\frac1x$ 在原点附近的振荡图像(振荡加密动画)",
   "红色数列点:$x_n=\\frac{1}{2n\\pi}$ 处的函数值 $0$(沿 $x$ 轴)",
   "蓝色数列点:$y_n=\\frac{1}{2n\\pi+\\frac\\pi2}$ 处的函数值 $1$(上沿)",
   "板书:海涅定理的表述",
   "红色标签「极限不存在」"
  ],
  "steps": [
   "第一步:画出 $\\sin\\frac1x$ 的振荡图像,展示原点附近振荡无限加密。",
   "第二步:取红色数列 $x_n=\\frac{1}{2n\\pi}$,函数值恒为 $0$。",
   "第三步:取蓝色数列 $y_n$,函数值恒为 $1$。",
   "第四步:引用海涅定理:若极限存在则两列函数值应同敛,矛盾。",
   "第五步:红色标注极限不存在,完成证明。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
# ===================== C46 几何概型 =====================
{
 "id": "draft-c46-01", "category": "概率论", "sub_category": "几何概型",
 "concept": "几何概型", "concept_id": "C46",
 "parent_training_ids": ["prob-039"],
 "problem": r"甲、乙两人约定在 $12$ 点到 $13$ 点之间随机到达某地,先到者等待 $15$ 分钟后离开。求两人能相遇的概率。",
 "solution": r"设甲到达时刻为 $x$,乙为 $y$,均服从 $[0,1]$ 上的均匀分布($1$ 小时归一化),样本空间为单位正方形。相遇当且仅当 $|x-y|\le\frac14$。在正方形中,$|x-y|\le\frac14$ 的区域为对角线带,其面积为总面积减去两个直角边长 $\frac34$ 的等腰直角三角形:相遇概率 $P=1-2\times\frac12\times\left(\frac34\right)^2=1-\frac{9}{16}=\frac{7}{16}$。",
 "answer": r"相遇概率为 $\frac{7}{16}$。",
 "method": "面积比(对角线带区域)",
 "difficulty": "基础",
 "variant_kind": "经典相遇问题:单位正方形与对角线带的面积比",
 "scene_spec": {
  "objects": [
   "平面坐标系:单位正方形(样本空间)",
   "两条斜线 $y=x+\\frac14$ 与 $y=x-\\frac14$(对角线带边界)",
   "蓝色对角线带(相遇区域)与两个灰色角落三角形(不相遇)",
   "板书:$1-2\\times\\frac12\\times(\\frac34)^2=\\frac{7}{16}$",
   "高亮框:$\\frac{7}{16}$"
  ],
  "steps": [
   "第一步:画出单位正方形,标注两轴为到达时刻。",
   "第二步:画出对角线带 $|x-y|\\le\\frac14$。",
   "第三步:高亮相遇区域,灰色标出两个角落三角形。",
   "第四步:计算面积比,得 $\\frac{7}{16}$。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c46-02", "category": "概率论", "sub_category": "几何概型",
 "concept": "几何概型", "concept_id": "C46",
 "parent_training_ids": ["prob-039"],
 "problem": r"在单位圆盘 $x^2+y^2\le1$ 内随机取一点(均匀分布),求该点落入内接正方形 $|x|\le\frac{1}{\sqrt2}$，$|y|\le\frac{1}{\sqrt2}$ 的概率。",
 "solution": r"均匀分布下,概率等于面积比。内接正方形的边长为 $\sqrt2$($\frac{1}{\sqrt2}\times2$),面积为 $(\sqrt2)^2=2$。单位圆盘面积为 $\pi$。故所求概率为 $\frac{2}{\pi}$。",
 "answer": r"概率为 $\frac{2}{\pi}$。",
 "method": "面积比(圆盘内接正方形)",
 "difficulty": "基础",
 "variant_kind": "区域切割:圆盘内正方形子区域的面积比",
 "scene_spec": {
  "objects": [
   "平面坐标系:单位圆盘(样本空间)",
   "蓝色内接正方形 $|x|\\le\\frac{1}{\\sqrt2},|y|\\le\\frac{1}{\\sqrt2}$",
   "正方形四个顶点落在圆周上的位置高亮(边长为 $\\sqrt2$)",
   "板书:$\\frac{(\\sqrt2)^2}{\\pi}=\\frac{2}{\\pi}$",
   "高亮框:$\\frac{2}{\\pi}$"
  ],
  "steps": [
   "第一步:画出单位圆盘。",
   "第二步:画出内接正方形,标出顶点。",
   "第三步:说明正方形边长为 $\\sqrt2$,面积为 $2$。",
   "第四步:圆盘面积为 $\\pi$,计算面积比。",
   "第五步:高亮结论 $\\frac{2}{\\pi}$。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c46-03", "category": "概率论", "sub_category": "几何概型",
 "concept": "几何概型", "concept_id": "C46",
 "parent_training_ids": ["prob-039"],
 "problem": r"设 $X,Y$ 独立且均服从 $[0,1]$ 上的均匀分布。求 $P(|X-Y|>\frac12)$,并分别用几何面积法与二重积分法计算验证。",
 "solution": r"几何法:样本空间为单位正方形,$|x-y|>\frac12$ 为对角线带之外的区域,即两个直角边长为 $\frac12$ 的等腰直角三角形,总面积 $2\times\frac12\times\left(\frac12\right)^2=\frac14$,故 $P=\frac14$。积分法:$P=\iint_{|x-y|>\frac12}1\,dx\,dy=2\int_0^{\frac12}\int_{y+\frac12}^{1}dx\,dy=2\int_0^{\frac12}\left(\frac12-y\right)dy=2\times\frac18=\frac14$。两法一致。",
 "answer": r"概率为 $\frac14$(几何法与积分法一致)。",
 "method": "面积比+二重积分双算法",
 "difficulty": "中等",
 "variant_kind": "双算法对照:同一概率的几何面积与二重积分两种路径互验",
 "scene_spec": {
  "objects": [
   "平面坐标系:单位正方形与对角线带 $|x-y|\\le\\frac12$",
   "两个灰色角落三角形(所求区域)高亮",
   "板书:面积法 $2\\times\\frac12\\times(\\frac12)^2=\\frac14$",
   "板书:积分法 $2\\int_0^{\\frac12}(\\frac12-y)dy=\\frac14$",
   "高亮框:两法一致 $\\frac14$"
  ],
  "steps": [
   "第一步:画出单位正方形与对角线带。",
   "第二步:高亮带外的两个角落三角形。",
   "第三步:用面积法计算,得 $\\frac14$。",
   "第四步:写出二重积分并计算,同样得 $\\frac14$。",
   "第五步:对照两法结果,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c46-04", "category": "概率论", "sub_category": "几何概型",
 "concept": "几何概型", "concept_id": "C46",
 "parent_training_ids": ["prob-039"],
 "problem": r"判断如下取点法是否在单位圆盘 $x^2+y^2\le1$ 内均匀分布:取独立随机变量 $U,V\sim U(0,1)$,令 $R=U$,$\Theta=2\pi V$,取点 $(R\cos\Theta,R\sin\Theta)$。若不均匀,说明原因并给出修正。",
 "solution": r"不均匀。此时 $R$ 在 $[0,1]$ 上均匀,$P(R\le r)=r$,而圆盘内半径为 $r$ 的圆面积占总面积的比例为 $r^2$。例如 $P(R\le\frac12)=\frac12$,但半径为 $\frac12$ 的圆只占总面积的 $\frac14$——点过多地集中在圆心附近(径向密度 $f_R(r)=1$,面积密度 $\propto\frac1r$)。修正:取 $R=\sqrt{U}$。此时 $P(R\le r)=P(\sqrt U\le r)=P(U\le r^2)=r^2$,恰为面积比例,故 $(R\cos\Theta,R\sin\Theta)$ 在圆盘内均匀分布。",
 "answer": r"不均匀(径向密度 $f_R(r)=1$ 导致中心过密,$P(R\le\frac12)=\frac12\neq\frac14$);修正:取 $R=\sqrt U$。",
 "method": "均匀性检验(径向分布核对)+修正",
 "difficulty": "中等",
 "variant_kind": "陷阱辨析:朴素极坐标取点的不均匀性及其修正(非均匀抽样不适用)",
 "scene_spec": {
  "objects": [
   "平面坐标系:单位圆盘(目标区域)",
   "动画:用 $R=U$ 取点,散点明显向圆心聚集",
   "动画:改用 $R=\\sqrt U$ 取点,散点均匀铺满圆盘",
   "板书:$P(R\\le r)=r$ 与面积比例 $r^2$ 的对比曲线",
   "高亮框:修正 $R=\\sqrt U$"
  ],
  "steps": [
   "第一步:动画展示 $R=U$ 取点,观察散点向圆心聚集。",
   "第二步:计算 $P(R\\le r)=r$,与面积比例 $r^2$ 对比。",
   "第三步:以 $r=\\frac12$ 为例说明不均匀(概率 $\\frac12$ vs 面积 $\\frac14$)。",
   "第四步:提出修正 $R=\\sqrt U$,验证 $P(R\\le r)=r^2$。",
   "第五步:动画展示修正后散点均匀铺满,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c46-05", "category": "概率论", "sub_category": "几何概型",
 "concept": "几何概型", "concept_id": "C46",
 "parent_training_ids": ["prob-039"],
 "problem": r"平面上画有间距为 $d$ 的平行直线族。将一根长为 $l$($l\le d$)的针随机投掷到平面上(针中点位置与针的方向均随机)。求针与某条直线相交的概率。",
 "solution": r"设针中点到最近直线的距离为 $y$($0\le y\le\frac d2$,均匀),针与直线的夹角为 $\theta$($0\le\theta\le\frac\pi2$,均匀)。针与直线相交当且仅当 $y\le\frac l2\sin\theta$。样本空间面积为 $\frac d2\times\frac\pi2$,相交区域面积为 $\int_0^{\frac\pi2}\frac l2\sin\theta\,d\theta=\frac l2$。故 $P=\frac{\frac l2}{\frac{d\pi}{4}}=\frac{2l}{\pi d}$。",
 "answer": r"相交概率为 $\frac{2l}{\pi d}$。",
 "method": "积分型几何概型(Buffon 投针)",
 "difficulty": "进阶",
 "variant_kind": "结构升级:二维连续参数的积分型几何概型推导(相交条件的区域积分)",
 "scene_spec": {
  "objects": [
   "平面示意图:平行直线族(间距 $d$)与一根随机针",
   "标注:针中点距离 $y$ 与夹角 $\\theta$",
   "参数平面图:$0\\le y\\le\\frac d2$,$0\\le\\theta\\le\\frac\\pi2$,相交区域 $y\\le\\frac l2\\sin\\theta$(阴影)",
   "板书:$P=\\frac{\\int_0^{\\pi/2}\\frac l2\\sin\\theta\\,d\\theta}{\\frac d2\\cdot\\frac\\pi2}=\\frac{2l}{\\pi d}$",
   "高亮框:$\\frac{2l}{\\pi d}$"
  ],
  "steps": [
   "第一步:画出平行直线族与随机针,标注 $y$ 与 $\\theta$。",
   "第二步:推导相交条件 $y\\le\\frac l2\\sin\\theta$。",
   "第三步:在参数平面上画出样本空间与相交区域。",
   "第四步:分别计算两区域面积并求比值。",
   "第五步:高亮结论 $\\frac{2l}{\\pi d}$。"
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
