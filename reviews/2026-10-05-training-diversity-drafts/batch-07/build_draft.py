"""batch-07 生成器:C02 无穷限反常积分 5 题、C04 格林公式 5 题、
C06 直角坐标面积与分段 4 题(活动已 4 条,补 4 封顶 8,密度协调)。
全部数学结论由作者逐题手工验算(见 DRAFT_REPORT.md 核算说明);
起草过程未读 eval/test 题文或答案作提示;凡有理数一律分数。
"""
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "draft.jsonl"

DATA = [
# ===================== C02 无穷限反常积分 =====================
{
 "id": "draft-c02-01", "category": "数学分析", "sub_category": "反常积分",
 "concept": "无穷限反常积分", "concept_id": "C02",
 "parent_training_ids": ["calc-improper-002", "calc-param-improper-003"],
 "problem": r"计算反常积分 $\int_1^{+\infty}\frac{1}{x^2}\,dx$。",
 "solution": r"先算有限区间上的积分再取极限:$\int_1^R\frac{1}{x^2}\,dx=\left.-\frac1x\right|_1^R=1-\frac1R$。令 $R\to+\infty$,得 $\int_1^{+\infty}\frac{1}{x^2}\,dx=\lim_{R\to+\infty}\left(1-\frac1R\right)=1$。",
 "answer": r"积分值为 $1$。",
 "method": "极限定义直接计算",
 "difficulty": "基础",
 "variant_kind": "数值结构变化:p 积分的直接极限计算(与 arctan/指数父题不同)",
 "scene_spec": {
  "objects": [
   "坐标图:曲线 $y=\\frac{1}{x^2}$($x\\ge1$)与 $x$ 轴之间的阴影区域",
   "动画:上限 $R$ 向右滑动,阴影面积逐渐接近极限",
   "板书:$\\int_1^R\\frac{1}{x^2}dx=1-\\frac1R$",
   "高亮框:极限 $1$",
   "标签「$p=2>1$ 收敛」"
  ],
  "steps": [
   "第一步:画出曲线与阴影区域,标出积分下限 $1$。",
   "第二步:写出有限区间积分 $\\int_1^R=1-\\frac1R$。",
   "第三步:动画滑动上限 $R$,展示面积趋近稳定值。",
   "第四步:取极限得 $1$。",
   "第五步:标注 $p=2>1$ 收敛,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c02-02", "category": "数学分析", "sub_category": "反常积分",
 "concept": "无穷限反常积分", "concept_id": "C02",
 "parent_training_ids": ["calc-improper-002", "calc-param-improper-003"],
 "problem": r"判断反常积分 $\int_1^{+\infty}\frac{1}{\sqrt{x}}\,dx$ 的敛散性，并说明理由。",
 "solution": r"$\int_1^R\frac{1}{\sqrt x}\,dx=\left.2\sqrt x\right|_1^R=2\sqrt R-2$。当 $R\to+\infty$ 时,$2\sqrt R-2\to+\infty$,故积分发散。理由:这是 $p=\frac12$ 的 $p$ 积分,而 $p$ 积分 $\int_1^{+\infty}\frac1{x^p}\,dx$ 当且仅当 $p>1$ 时收敛;此处 $p=\frac12\le1$,发散。",
 "answer": r"发散($p=\frac12\le1$)。",
 "method": "极限计算+p 积分判据",
 "difficulty": "基础",
 "variant_kind": "敛散判定:发散情形的 p 积分判据应用",
 "scene_spec": {
  "objects": [
   "坐标图:曲线 $y=\\frac{1}{\\sqrt{x}}$($x\\ge1$)与阴影区域",
   "动画:上限 $R$ 滑动,面积持续增长不封顶",
   "板书:$\\int_1^R=2\\sqrt R-2\\to+\\infty$",
   "红色标签「发散」",
   "板书:$p$ 积分判据:$p=\\frac12\\le1$"
  ],
  "steps": [
   "第一步:画出曲线与阴影区域。",
   "第二步:计算有限区间积分 $2\\sqrt R-2$。",
   "第三步:动画展示面积随 $R$ 持续增长。",
   "第四步:取极限为 $+\\infty$,红色标注发散。",
   "第五步:对照 $p$ 积分判据($p\\le1$ 发散),汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c02-03", "category": "数学分析", "sub_category": "反常积分",
 "concept": "无穷限反常积分", "concept_id": "C02",
 "parent_training_ids": ["calc-improper-002", "calc-param-improper-003"],
 "problem": r"判断 $\int_2^{+\infty}\frac{1}{x\ln x}\,dx$ 与 $\int_2^{+\infty}\frac{1}{x\ln^2 x}\,dx$ 的敛散性，并求收敛者的值。",
 "solution": r"换元 $u=\ln x$,$du=\frac{dx}{x}$。第一个:$\int_2^R\frac{1}{x\ln x}dx=\int_{\ln2}^{\ln R}\frac{du}{u}=\ln(\ln R)-\ln(\ln2)\to+\infty$,发散。第二个:$\int_2^R\frac{1}{x\ln^2x}dx=\int_{\ln2}^{\ln R}\frac{du}{u^2}=\frac{1}{\ln2}-\frac{1}{\ln R}\to\frac{1}{\ln2}$,收敛且值为 $\frac{1}{\ln2}$。",
 "answer": r"$\int_2^{+\infty}\frac{1}{x\ln x}dx$ 发散;$\int_2^{+\infty}\frac{1}{x\ln^2x}dx$ 收敛,值为 $\frac{1}{\ln2}$。",
 "method": "换元化为 p 积分",
 "difficulty": "中等",
 "variant_kind": "边界对比:对数因子一阶与二阶的敛散分界(换元后 p 积分)",
 "scene_spec": {
  "objects": [
   "板书:两个被积函数 $\\frac{1}{x\\ln x}$ 与 $\\frac{1}{x\\ln^2x}$ 并排",
   "板书:换元 $u=\\ln x$ 的推导",
   "坐标图:两条曲线衰减速度对比(一快一慢)",
   "红色标签「发散」与绿色标签「收敛 $=\\frac{1}{\\ln2}$」",
   "板书:极限过程 $\\ln(\\ln R)\\to+\\infty$ 与 $\\frac{1}{\\ln R}\\to0$"
  ],
  "steps": [
   "第一步:并列写出两个积分,说明差别只在 $\\ln x$ 的幂次。",
   "第二步:换元 $u=\\ln x$,分别化为 $\\int du/u$ 与 $\\int du/u^2$。",
   "第三步:计算第一个的极限,$\\ln(\\ln R)\\to+\\infty$,发散。",
   "第四步:计算第二个的极限,得 $\\frac{1}{\\ln2}$,收敛。",
   "第五步:对照两条曲线的衰减速度,总结对数因子的敛散分界。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c02-04", "category": "数学分析", "sub_category": "反常积分",
 "concept": "无穷限反常积分", "concept_id": "C02",
 "parent_training_ids": ["calc-improper-002", "calc-param-improper-003"],
 "problem": r"用分部积分法计算 $\int_0^{+\infty}xe^{-x}\,dx$。",
 "solution": r"先对有限区间分部积分:取 $u=x,dv=e^{-x}dx$,则 $\int_0^R xe^{-x}dx=\left.-xe^{-x}\right|_0^R+\int_0^R e^{-x}dx=-Re^{-R}+(1-e^{-R})$。令 $R\to+\infty$:$Re^{-R}\to0$(指数衰减快于线性增长),$e^{-R}\to0$,故 $\int_0^{+\infty}xe^{-x}dx=1$。",
 "answer": r"积分值为 $1$。",
 "method": "分部积分+极限处理",
 "difficulty": "中等",
 "variant_kind": "方法变化:分部积分法(含 $Re^{-R}\\to0$ 的极限论证)",
 "scene_spec": {
  "objects": [
   "坐标图:曲线 $y=xe^{-x}$($x\\ge0$)与阴影区域(单峰形状)",
   "板书:分部积分 $\\int xe^{-x}dx=-xe^{-x}+\\int e^{-x}dx$",
   "板书:边界项 $-Re^{-R}\\to0$ 的极限标注",
   "高亮框:结果 $1$",
   "标签「指数衰减快于线性增长」"
  ],
  "steps": [
   "第一步:画出单峰曲线与阴影区域。",
   "第二步:展示分部积分过程,得 $-xe^{-x}+(1-e^{-x})$。",
   "第三步:讨论边界项 $-Re^{-R}\\to0$。",
   "第四步:取极限得 $1$。",
   "第五步:标注指数衰减快于线性增长,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c02-05", "category": "数学分析", "sub_category": "反常积分",
 "concept": "无穷限反常积分", "concept_id": "C02",
 "parent_training_ids": ["calc-improper-002", "calc-param-improper-003"],
 "problem": r"证明 $p$ 积分 $\int_1^{+\infty}\frac{1}{x^p}\,dx$ 当且仅当 $p>1$ 时收敛。",
 "solution": r"当 $p\neq1$ 时,$\int_1^R x^{-p}dx=\left.\frac{x^{1-p}}{1-p}\right|_1^R=\frac{R^{1-p}-1}{1-p}$。若 $p>1$,则 $1-p<0$,$R^{1-p}\to0$,故极限为 $\frac{1}{p-1}$,收敛。若 $p<1$,则 $1-p>0$,$R^{1-p}\to+\infty$,发散。当 $p=1$ 时,$\int_1^R\frac{dx}{x}=\ln R\to+\infty$,发散。综上,收敛当且仅当 $p>1$(且收敛值为 $\frac{1}{p-1}$)。",
 "answer": r"收敛当且仅当 $p>1$,此时值为 $\frac{1}{p-1}$;证明见解法。",
 "method": "极限直接计算(全参数分支证明)",
 "difficulty": "进阶",
 "variant_kind": "证明型:p 积分敛散性的完整参数分支证明,非单一数值计算",
 "scene_spec": {
  "objects": [
   "板书:$\\int_1^R x^{-p}dx=\\frac{R^{1-p}-1}{1-p}$($p\\neq1$)",
   "数轴:参数 $p$ 的三个区间($p<1$ 发散、$p=1$ 发散、$p>1$ 收敛)",
   "板书:$p>1$ 时 $R^{1-p}\\to0$ 与 $p<1$ 时 $R^{1-p}\\to+\\infty$ 的对照",
   "板书:$p=1$ 时 $\\ln R\\to+\\infty$",
   "高亮框:收敛当且仅当 $p>1$,值为 $\\frac{1}{p-1}$"
  ],
  "steps": [
   "第一步:写出 $p\\neq1$ 时的有限积分公式。",
   "第二步:分析 $p>1$ 分支,得收敛且值为 $\\frac{1}{p-1}$。",
   "第三步:分析 $p<1$ 分支,发散。",
   "第四步:单独处理 $p=1$ 分支,$\\ln R\\to+\\infty$,发散。",
   "第五步:在数轴上汇总三个分支,高亮充要条件结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
# ===================== C04 格林公式 =====================
{
 "id": "draft-c04-01", "category": "数学分析", "sub_category": "曲线积分",
 "concept": "格林公式", "concept_id": "C04",
 "parent_training_ids": ["calc-green-005"],
 "problem": r"用格林公式求 $\oint_L x^2\,dy$，其中 $L$ 为以 $(0,0),(1,0),(0,1)$ 为顶点的三角形正向边界，并直接计算验证。",
 "solution": r"格林公式:$\oint_L x^2\,dy=\iint_D 2x\,dxdy$。区域 $D$:$0\le y\le1$,$0\le x\le1-y$。$\iint_D 2x\,dxdy=\int_0^1\int_0^{1-y}2x\,dx\,dy=\int_0^1(1-y)^2\,dy=\frac13$。直接验证:底边 $y=0$ 上 $dy=0$ 贡献为 $0$;竖边 $x=0$ 上 $x^2=0$ 贡献为 $0$;斜边 $x=1-y$($y$ 从 $0$ 到 $1$):$\int_0^1(1-y)^2\,dy=\frac13$。两法一致。",
 "answer": r"积分值为 $\frac13$(格林公式与直接计算一致)。",
 "method": "格林公式(非对称区域)+直接验证",
 "difficulty": "基础",
 "variant_kind": "区域变化:三角形非对称区域的格林公式应用与双算法互验",
 "scene_spec": {
  "objects": [
   "平面坐标系:三角形区域(阴影)与正向边界箭头",
   "板书:格林公式 $\\oint x^2\\,dy=\\iint 2x\\,dxdy$",
   "板书:$\\int_0^1(1-y)^2dy=\\frac13$",
   "动画:沿三边的直接积分贡献分解(两零一非零)",
   "高亮框:$\\frac13$(两法一致)"
  ],
  "steps": [
   "第一步:画出三角形与逆时针边界箭头。",
   "第二步:应用格林公式化为二重积分并计算。",
   "第三步:直接积分:展示底边与竖边贡献为零。",
   "第四步:展示斜边积分 $(1-y)^2$ 的贡献为 $\\frac13$。",
   "第五步:对照两法结果,高亮一致。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c04-02", "category": "数学分析", "sub_category": "曲线积分",
 "concept": "格林公式", "concept_id": "C04",
 "parent_training_ids": ["calc-green-005"],
 "problem": r"求 $\oint_L y\,dx$，其中 $L$ 为逆时针单位圆周；并说明若沿顺时针方向积分，结果如何变化。",
 "solution": r"格林公式:$\oint_L y\,dx=\iint_D(0-1)\,dxdy=-\iint_D 1\,dxdy=-A$,其中 $A$ 为区域面积。单位圆面积 $A=\pi$,故逆时针积分为 $-\pi$。若改为顺时针,格林公式需取负号(或等价地区域定向反转),结果为 $+\pi$。",
 "answer": r"逆时针为 $-\pi$;顺时针为 $+\pi$(符号随定向反转)。",
 "method": "格林公式+方向反转",
 "difficulty": "基础",
 "variant_kind": "方向反转:边界定向对曲线积分符号的影响",
 "scene_spec": {
  "objects": [
   "平面坐标系:单位圆盘(阴影)与逆时针箭头",
   "板书:$\\oint y\\,dx=\\iint(0-1)dxdy=-A$",
   "高亮框:逆时针 $=-\\pi$",
   "动画:箭头切换为顺时针,符号翻转为 $+\\pi$",
   "标签「定向决定符号」"
  ],
  "steps": [
   "第一步:画出单位圆与逆时针定向箭头。",
   "第二步:应用格林公式得 $-A=-\\pi$。",
   "第三步:高亮逆时针结果。",
   "第四步:动画切换为顺时针定向,说明格林公式取负。",
   "第五步:汇总:定向反转则符号反转。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c04-03", "category": "数学分析", "sub_category": "曲线积分",
 "concept": "格林公式", "concept_id": "C04",
 "parent_training_ids": ["calc-green-005"],
 "problem": r"用格林公式求 $\oint_L -y^3\,dx+x^3\,dy$，其中 $L$ 为圆环 $1\le x^2+y^2\le4$ 的边界(外圆逆时针、内圆顺时针)，并说明内外圆方向相反的原因。",
 "solution": r"格林公式(区域 $D$ 为圆环):$\oint_L -y^3dx+x^3dy=\iint_D\left(\frac{\partial}{\partial x}x^3-\frac{\partial}{\partial y}(-y^3)\right)dxdy=\iint_D(3x^2+3y^2)\,dxdy=3\iint_D r^2\cdot r\,dr\,d\theta=3\int_0^{2\pi}d\theta\int_1^2r^3\,dr=3\times2\pi\times\frac{2^4-1^4}{4}=\frac{45\pi}{2}$。方向:为使区域 $D$ 总在边界的左侧(正向),外边界须逆时针、内边界须顺时针。",
 "answer": r"积分值为 $\frac{45\pi}{2}$;外逆内顺保证区域在边界左侧(正向)。",
 "method": "格林公式(有洞区域)",
 "difficulty": "中等",
 "variant_kind": "有洞区域:圆环的格林公式应用与多连通区域定向规则",
 "scene_spec": {
  "objects": [
   "平面坐标系:圆环区域(阴影)与外逆内顺的边界箭头",
   "板书:被积函数偏导差 $3x^2+3y^2$",
   "板书:极坐标计算 $3\\times2\\pi\\times\\frac{15}{4}$",
   "高亮框:$\\frac{45\\pi}{2}$",
   "标签「多连通区域:外逆内顺」"
  ],
  "steps": [
   "第一步:画出圆环与两条边界曲线,标注外逆内顺箭头。",
   "第二步:写出偏导差 $3x^2+3y^2$ 的二重积分。",
   "第三步:极坐标化并计算径向积分。",
   "第四步:高亮结果 $\\frac{45\\pi}{2}$。",
   "第五步:说明多连通区域正向规则(区域在边界左侧)。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c04-04", "category": "数学分析", "sub_category": "曲线积分",
 "concept": "格林公式", "concept_id": "C04",
 "parent_training_ids": ["calc-green-005"],
 "problem": r"用格林公式(补边闭合)计算曲线积分 $\int_L (x+y)\,dx+x\,dy$，其中 $L$ 为抛物线 $y=x^2$ 上从 $(0,0)$ 到 $(1,1)$ 的弧段。",
 "solution": r"补直线段 $L'$:从 $(1,1)$ 沿直线回到 $(0,0)$,$L+L'$ 为闭合曲线。区域 $D$ 内,$\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}=\frac{\partial x}{\partial x}-\frac{\partial(x+y)}{\partial y}=1-1=0$,故 $\oint_{L+L'}=0$,于是 $\int_L=-\int_{L'}$。参数化 $L'$:$(1-t,1-t)$,$t\in[0,1]$,$dx=dy=-dt$:$\int_{L'}(x+y)dx+x\,dy=\int_0^1\left[(2-2t)(-1)+(1-t)(-1)\right]dt=\int_0^1(3t-3)\,dt=-\frac32$。故 $\int_L=\frac32$。",
 "answer": r"积分值为 $\frac32$(补边闭合,格林公式得闭合积分为零)。",
 "method": "补边法(非闭合曲线+格林公式)",
 "difficulty": "中等",
 "variant_kind": "适用条件:非闭合曲线补边闭合后应用格林公式",
 "scene_spec": {
  "objects": [
   "平面坐标系:抛物线弧段 $L$(从 $(0,0)$ 到 $(1,1)$)与补边直线段(虚线)",
   "区域 $D$(阴影)与闭合定向箭头",
   "板书:$\\frac{\\partial Q}{\\partial x}-\\frac{\\partial P}{\\partial y}=1-1=0$",
   "板书:补边积分 $\\int_{L'}(3t-3)dt=-\\frac32$",
   "高亮框:$\\int_L=\\frac32$"
  ],
  "steps": [
   "第一步:画出抛物线弧段,并用虚线补上直线段形成闭合回路。",
   "第二步:计算区域内的偏导差,得零。",
   "第三步:由格林公式得闭合积分为零,故 $\\int_L=-\\int_{L'}$。",
   "第四步:参数化补边线段并计算 $-\\frac32$。",
   "第五步:取负得 $\\frac32$,高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c04-05", "category": "数学分析", "sub_category": "曲线积分",
 "concept": "格林公式", "concept_id": "C04",
 "parent_training_ids": ["calc-green-005"],
 "problem": r"由格林公式推导面积公式 $A=\frac12\oint_L x\,dy-y\,dx$，并求椭圆 $\frac{x^2}{a^2}+\frac{y^2}{b^2}=1$ 的面积。",
 "solution": r"在格林公式 $\oint_L P\,dx+Q\,dy=\iint_D\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)dxdy$ 中取 $P=-y,Q=x$,得 $\oint_L x\,dy-y\,dx=\iint_D(1+1)dxdy=2A$,故 $A=\frac12\oint_L x\,dy-y\,dx$。椭圆参数化:$x=a\cos t,y=b\sin t$($t:0\to2\pi$),则 $\oint x\,dy-y\,dx=\int_0^{2\pi}\left[(a\cos t)(b\cos t)-(b\sin t)(-a\sin t)\right]dt=ab\int_0^{2\pi}(\cos^2t+\sin^2t)\,dt=2\pi ab$。故 $A=\frac12\cdot2\pi ab=\pi ab$。",
 "answer": r"面积公式 $A=\frac12\oint_L x\,dy-y\,dx$;椭圆面积为 $\pi ab$。",
 "method": "格林公式面积公式推导+参数化应用",
 "difficulty": "进阶",
 "variant_kind": "推导+应用:面积公式的推导与椭圆面积计算",
 "scene_spec": {
  "objects": [
   "板书:格林公式取 $P=-y,Q=x$ 的推导",
   "高亮框:$A=\\frac12\\oint x\\,dy-y\\,dx$",
   "平面坐标系:椭圆与参数化标注",
   "板书:$ab\\int_0^{2\\pi}(\\cos^2t+\\sin^2t)dt=2\\pi ab$",
   "高亮框:$A=\\pi ab$"
  ],
  "steps": [
   "第一步:由格林公式取 $P=-y,Q=x$,推导面积公式。",
   "第二步:高亮面积公式。",
   "第三步:参数化椭圆,写出 $x\\,dy-y\\,dx$ 的表达式。",
   "第四步:计算积分得 $2\\pi ab$。",
   "第五步:代入公式得 $A=\\pi ab$,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
# ===================== C06 直角坐标面积与分段 =====================
{
 "id": "draft-c06-01", "category": "数学分析", "sub_category": "定积分应用",
 "concept": "直角坐标面积与分段", "concept_id": "C06",
 "parent_training_ids": ["calc-area-007", "calc-area-010", "calc-area-011", "calc-area-013"],
 "problem": r"求由抛物线 $y=x^2$ 与 $y=2-x^2$ 围成的封闭图形的面积。",
 "solution": r"交点:$x^2=2-x^2$ 得 $x=\pm1$。利用对称性,$A=\int_{-1}^{1}\left[(2-x^2)-x^2\right]dx=2\int_0^1(2-2x^2)\,dx=2\left.\left(2x-\frac{2x^3}{3}\right)\right|_0^1=2\times\frac43=\frac83$。",
 "answer": r"面积为 $\frac83$。",
 "method": "上下曲线相减(对称简化)",
 "difficulty": "基础",
 "variant_kind": "曲线组合变化:两条抛物线围成的对称区域",
 "scene_spec": {
  "objects": [
   "平面坐标系:两条抛物线 $y=x^2$ 与 $y=2-x^2$",
   "两抛物线围成的封闭区域(阴影)",
   "两个交点 $(-1,1)$ 与 $(1,1)$ 高亮",
   "板书:$A=2\\int_0^1(2-2x^2)dx$",
   "高亮框:$\\frac83$"
  ],
  "steps": [
   "第一步:画出两条抛物线,高亮两个交点。",
   "第二步:阴影标出围成区域,说明上下曲线的位置。",
   "第三步:写出积分并利用对称性简化。",
   "第四步:计算得 $\\frac83$。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c06-02", "category": "数学分析", "sub_category": "定积分应用",
 "concept": "直角坐标面积与分段", "concept_id": "C06",
 "parent_training_ids": ["calc-area-007", "calc-area-010", "calc-area-011", "calc-area-013"],
 "problem": r"求由 $y=|x|$ 与 $y=1$ 围成的封闭图形的面积。",
 "solution": r"交点:$|x|=1$ 得 $x=\pm1$。区域关于 $y$ 轴对称,右半部分为 $0\le x\le1$,$|x|\le y\le1$。$A=2\int_0^1(1-x)\,dx=2\left.\left(x-\frac{x^2}{2}\right)\right|_0^1=2\times\frac12=1$。",
 "answer": r"面积为 $1$。",
 "method": "绝对值分段+对称性",
 "difficulty": "基础",
 "variant_kind": "绝对值函数与水平线的围成区域(分段后对称简化)",
 "scene_spec": {
  "objects": [
   "平面坐标系:折线 $y=|x|$ 与水平线 $y=1$",
   "围成的三角形区域(阴影)",
   "两个交点 $(-1,1)$ 与 $(1,1)$ 高亮",
   "板书:$A=2\\int_0^1(1-x)dx$",
   "高亮框:$1$"
  ],
  "steps": [
   "第一步:画出折线 $y=|x|$ 与水平线,高亮交点。",
   "第二步:阴影标出围成的等腰三角形。",
   "第三步:利用对称性写出一半区域积分。",
   "第四步:计算得 $1$。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c06-03", "category": "数学分析", "sub_category": "定积分应用",
 "concept": "直角坐标面积与分段", "concept_id": "C06",
 "parent_training_ids": ["calc-area-007", "calc-area-010", "calc-area-011", "calc-area-013"],
 "problem": r"求由抛物线 $x=y^2$ 与直线 $y=x-2$ 围成的封闭图形的面积(按 $y$ 积分)。",
 "solution": r"交点:$y^2=y+2$,即 $y^2-y-2=0$,得 $y=-1$ 与 $y=2$。区域在 $y$ 方向的范围为 $[-1,2]$,右边界为直线 $x=y+2$,左边界为抛物线 $x=y^2$。$A=\int_{-1}^{2}\left[(y+2)-y^2\right]dy=\left.\left(\frac{y^2}{2}+2y-\frac{y^3}{3}\right)\right|_{-1}^{2}=\left(2+4-\frac83\right)-\left(\frac12-2+\frac13\right)=\frac{10}{3}+\frac76=\frac92$。",
 "answer": r"面积为 $\frac92$。",
 "method": "按 y 积分(左右曲线相减)",
 "difficulty": "中等",
 "variant_kind": "积分方向变化:横向区域的按 y 积分路径",
 "scene_spec": {
  "objects": [
   "平面坐标系:抛物线 $x=y^2$ 与直线 $y=x-2$",
   "围成的封闭区域(阴影)",
   "两个交点 $(1,-1)$ 与 $(4,2)$ 高亮",
   "板书:$A=\\int_{-1}^2[(y+2)-y^2]dy$",
   "高亮框:$\\frac92$"
  ],
  "steps": [
   "第一步:画出抛物线与直线,解出交点对应的 $y$ 值。",
   "第二步:阴影标出区域,说明按 $y$ 方向积分的原因(区域横向)。",
   "第三步:写出左右曲线相减的积分。",
   "第四步:计算得 $\\frac92$。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c06-04", "category": "数学分析", "sub_category": "定积分应用",
 "concept": "直角坐标面积与分段", "concept_id": "C06",
 "parent_training_ids": ["calc-area-007", "calc-area-010", "calc-area-011", "calc-area-013"],
 "problem": r"求由抛物线 $y=x^2$ 与直线 $y=kx$($k>0$)围成的封闭图形的面积(用 $k$ 表示)，并求 $k=2$ 时的面积。",
 "solution": r"交点:$x^2=kx$ 得 $x=0$ 与 $x=k$。在 $[0,k]$ 上,$kx\ge x^2$。$A(k)=\int_0^k(kx-x^2)\,dx=\left.\left(\frac{kx^2}{2}-\frac{x^3}{3}\right)\right|_0^k=\frac{k^3}{2}-\frac{k^3}{3}=\frac{k^3}{6}$。当 $k=2$ 时,$A=\frac{2^3}{6}=\frac43$。",
 "answer": r"$A(k)=\frac{k^3}{6}$;$k=2$ 时面积为 $\frac43$。",
 "method": "含参面积(交点随参数变化)",
 "difficulty": "中等",
 "variant_kind": "参数依赖:交点与面积均随参数变化的含参面积公式",
 "scene_spec": {
  "objects": [
   "平面坐标系:抛物线 $y=x^2$ 与直线族 $y=kx$(动画:$k$ 滑动)",
   "围成的区域(阴影随 $k$ 变化)",
   "两个交点 $(0,0)$ 与 $(k,k^2)$ 高亮",
   "板书:$A(k)=\\frac{k^3}{6}$",
   "高亮框:$k=2$ 时 $\\frac43$"
  ],
  "steps": [
   "第一步:动画滑动直线 $y=kx$,展示交点随 $k$ 移动。",
   "第二步:写出积分 $\\int_0^k(kx-x^2)dx$。",
   "第三步:计算得 $A(k)=\\frac{k^3}{6}$。",
   "第四步:代入 $k=2$,得 $\\frac43$。",
   "第五步:高亮结论。"
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
