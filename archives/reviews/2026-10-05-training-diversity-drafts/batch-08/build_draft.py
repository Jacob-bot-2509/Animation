"""batch-08 生成器:三个单条考点各 5 题
(C07 极坐标面积 / C08 参数曲线面积 / C09 旋转体体积)。
全部数学结论由作者逐题手工验算(见 DRAFT_REPORT.md 核算说明);
起草过程未读 eval/test 题文或答案作提示;凡有理数一律分数。
"""
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "draft.jsonl"

DATA = [
# ===================== C07 极坐标面积 =====================
{
 "id": "draft-c07-01", "category": "数学分析", "sub_category": "定积分应用",
 "concept": "极坐标面积", "concept_id": "C07",
 "parent_training_ids": ["calc-area-008"],
 "problem": r"求三叶玫瑰线 $r=2\sin 3\theta$ 的一叶所围成的面积。",
 "solution": r"一叶对应角域 $0\le\theta\le\frac{\pi}{3}$(当 $\theta$ 从 $0$ 到 $\frac{\pi}{3}$ 时,$r$ 从 $0$ 增大到 $2$ 再回到 $0$)。面积 $A=\frac12\int_0^{\frac{\pi}{3}}r^2\,d\theta=\frac12\int_0^{\frac{\pi}{3}}4\sin^2 3\theta\,d\theta=2\int_0^{\frac{\pi}{3}}\sin^2 3\theta\,d\theta$。换元 $u=3\theta$:$\int_0^{\frac{\pi}{3}}\sin^2 3\theta\,d\theta=\frac13\int_0^{\pi}\sin^2u\,du=\frac13\cdot\frac{\pi}{2}=\frac{\pi}{6}$。故 $A=2\times\frac{\pi}{6}=\frac{\pi}{3}$。",
 "answer": r"一叶面积为 $\frac{\pi}{3}$。",
 "method": "极坐标面积公式(单瓣角域)",
 "difficulty": "基础",
 "variant_kind": "多瓣区域:玫瑰线单叶面积(角域确定)",
 "scene_spec": {
  "objects": [
   "极坐标网格",
   "三叶玫瑰线 $r=2\\sin3\\theta$(三叶完整图)",
   "一叶高亮(其余两叶淡化)与角域扇形示意",
   "板书:$A=\\frac12\\int_0^{\\pi/3}4\\sin^23\\theta\\,d\\theta$",
   "高亮框:$\\frac{\\pi}{3}$"
  ],
  "steps": [
   "第一步:画出三叶玫瑰线,高亮其中一叶。",
   "第二步:说明该叶对应角域 $0\\le\\theta\\le\\frac\\pi3$。",
   "第三步:写出面积公式并换元计算。",
   "第四步:得 $\\frac{\\pi}{6}\\times2=\\frac{\\pi}{3}$。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c07-02", "category": "数学分析", "sub_category": "定积分应用",
 "concept": "极坐标面积", "concept_id": "C07",
 "parent_training_ids": ["calc-area-008"],
 "problem": r"求心形线 $r=1+\cos\theta$ 所围成的面积。",
 "solution": r"心形线在 $0\le\theta\le2\pi$ 上完整描绘一遍。$A=\frac12\int_0^{2\pi}(1+\cos\theta)^2\,d\theta=\frac12\int_0^{2\pi}(1+2\cos\theta+\cos^2\theta)\,d\theta=\frac12\left(2\pi+0+\pi\right)=\frac{3\pi}{2}$(用到 $\int_0^{2\pi}\cos\theta\,d\theta=0$ 与 $\int_0^{2\pi}\cos^2\theta\,d\theta=\pi$)。",
 "answer": r"面积为 $\frac{3\pi}{2}$。",
 "method": "极坐标面积公式(完整周期)",
 "difficulty": "基础",
 "variant_kind": "曲线类型变化:心形线的完整周期积分",
 "scene_spec": {
  "objects": [
   "极坐标网格",
   "心形线 $r=1+\\cos\\theta$(阴影内部区域)",
   "动画:极径随 $\\theta$ 扫过 $0\\to2\\pi$",
   "板书:$\\frac12\\int_0^{2\\pi}(1+\\cos\\theta)^2d\\theta$",
   "高亮框:$\\frac{3\\pi}{2}$"
  ],
  "steps": [
   "第一步:画出心形线,阴影标出内部区域。",
   "第二步:动画展示极径扫过完整周期。",
   "第三步:展开被积函数并逐项积分。",
   "第四步:得 $\\frac{3\\pi}{2}$。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c07-03", "category": "数学分析", "sub_category": "定积分应用",
 "concept": "极坐标面积", "concept_id": "C07",
 "parent_training_ids": ["calc-area-008"],
 "problem": r"求四叶玫瑰线 $r=\cos 2\theta$ 所围成的总面积，并说明为什么只需计算一叶再乘 $4$。",
 "solution": r"一叶对应角域 $-\frac{\pi}{4}\le\theta\le\frac{\pi}{4}$(其间 $r\ge0$ 且极径从 $0$ 出发回到 $0$)。一叶面积 $A_1=\frac12\int_{-\frac{\pi}{4}}^{\frac{\pi}{4}}\cos^2 2\theta\,d\theta$。换元 $u=2\theta$:$\int_{-\frac{\pi}{4}}^{\frac{\pi}{4}}\cos^2 2\theta\,d\theta=\frac12\int_{-\frac{\pi}{2}}^{\frac{\pi}{2}}\cos^2u\,du=\frac12\cdot\frac{\pi}{2}=\frac{\pi}{4}$。故 $A_1=\frac12\cdot\frac{\pi}{4}=\frac{\pi}{8}$。四叶互不重叠且完全对称,总面积为 $4A_1=\frac{\pi}{2}$。",
 "answer": r"总面积为 $\frac{\pi}{2}$(一叶 $\frac{\pi}{8}$ 乘 $4$)。",
 "method": "极坐标面积公式(多瓣对称)",
 "difficulty": "中等",
 "variant_kind": "多瓣区域:四叶玫瑰的对称简化与覆盖次数说明",
 "scene_spec": {
  "objects": [
   "极坐标网格",
   "四叶玫瑰线 $r=\\cos2\\theta$(四叶对称图)",
   "一叶高亮(其余淡化)与角域 $[-\\frac\\pi4,\\frac\\pi4]$ 标注",
   "板书:一叶面积计算与乘以 $4$ 的理由",
   "高亮框:$\\frac{\\pi}{2}$"
  ],
  "steps": [
   "第一步:画出四叶玫瑰线,说明四叶对称。",
   "第二步:高亮一叶,标出角域 $[-\\frac\\pi4,\\frac\\pi4]$。",
   "第三步:计算一叶面积 $\\frac\\pi8$。",
   "第四步:说明四叶互不重叠,总面积乘 $4$。",
   "第五步:高亮结论 $\\frac\\pi2$。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c07-04", "category": "数学分析", "sub_category": "定积分应用",
 "concept": "极坐标面积", "concept_id": "C07",
 "parent_training_ids": ["calc-area-008"],
 "problem": r"求圆 $r=4\cos\theta$ 内部位于圆 $r=2$ 外部的区域(月牙形)的面积。",
 "solution": r"两圆交点:$4\cos\theta=2$ 得 $\cos\theta=\frac12$,即 $\theta=\pm\frac{\pi}{3}$。所求区域由 $-\frac{\pi}{3}\le\theta\le\frac{\pi}{3}$ 且 $2\le r\le4\cos\theta$ 描述。$A=\frac12\int_{-\frac{\pi}{3}}^{\frac{\pi}{3}}\left[(4\cos\theta)^2-2^2\right]d\theta=\frac12\int_{-\frac{\pi}{3}}^{\frac{\pi}{3}}(16\cos^2\theta-4)\,d\theta=\int_{-\frac{\pi}{3}}^{\frac{\pi}{3}}(8\cos^2\theta-2)\,d\theta=\int_{-\frac{\pi}{3}}^{\frac{\pi}{3}}(2+4\cos2\theta)\,d\theta=\left.2\theta+2\sin2\theta\right|_{-\frac{\pi}{3}}^{\frac{\pi}{3}}=\frac{4\pi}{3}+2\sqrt3$。",
 "answer": r"面积为 $\frac{4\pi}{3}+2\sqrt3$。",
 "method": "内外曲线相减(交叠区域)",
 "difficulty": "中等",
 "variant_kind": "内外曲线交叠:两圆交叠的月牙形区域(平方差被积函数)",
 "scene_spec": {
  "objects": [
   "极坐标网格",
   "圆 $r=4\\cos\\theta$(中心在 $(2,0)$)与圆 $r=2$(原点)",
   "月牙形区域(阴影)",
   "两个交点对应的角 $\\pm\\frac\\pi3$ 高亮",
   "板书:$\\frac12\\int_{-\\pi/3}^{\\pi/3}[(4\\cos\\theta)^2-4]d\\theta$"
  ],
  "steps": [
   "第一步:画出两个圆,标出交点对应的角 $\\pm\\frac\\pi3$。",
   "第二步:阴影标出月牙形区域。",
   "第三步:写出平方差被积函数并化简。",
   "第四步:积分得 $\\frac{4\\pi}{3}+2\\sqrt3$。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c07-05", "category": "数学分析", "sub_category": "定积分应用",
 "concept": "极坐标面积", "concept_id": "C07",
 "parent_training_ids": ["calc-area-008"],
 "problem": r"求双纽线 $r^2=\cos 2\theta$ 所围成的总面积，并说明角域的确定方式。",
 "solution": r"需 $r^2\ge0$,即 $\cos2\theta\ge0$,故角域为 $[-\frac{\pi}{4},\frac{\pi}{4}]\cup[\frac{3\pi}{4},\frac{5\pi}{4}]$(按模 $2\pi$ 理解,等价于 $[0,\frac{\pi}{4}]\cup[\frac{3\pi}{4},\frac{5\pi}{4}]\cup[\frac{7\pi}{4},2\pi]$),两段对应两个对称的叶。右叶面积 $A_1=\frac12\int_{-\frac{\pi}{4}}^{\frac{\pi}{4}}\cos2\theta\,d\theta=\frac12\left.\frac{\sin2\theta}{2}\right|_{-\frac{\pi}{4}}^{\frac{\pi}{4}}=\frac12\times1=\frac12$。总面积 $=2A_1=1$。",
 "answer": r"总面积为 $1$(每叶 $\frac12$,共两叶)。",
 "method": "极坐标面积公式($r^2$ 形式+角域约束)",
 "difficulty": "进阶",
 "variant_kind": "结构升级:r² 形式的双纽线,角域由非负性约束确定",
 "scene_spec": {
  "objects": [
   "极坐标网格",
   "双纽线 $r^2=\\cos2\\theta$(两叶对称图)",
   "角域约束示意:$\\cos2\\theta\\ge0$ 的区间高亮",
   "板书:$A_1=\\frac12\\int_{-\\pi/4}^{\\pi/4}\\cos2\\theta\\,d\\theta=\\frac12$",
   "高亮框:总面积 $1$"
  ],
  "steps": [
   "第一步:画出双纽线两叶。",
   "第二步:由 $r^2\\ge0$ 确定角域,高亮两个有效区间。",
   "第三步:计算右叶面积 $\\frac12$。",
   "第四步:由对称性得总面积 $1$。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
# ===================== C08 参数曲线面积 =====================
{
 "id": "draft-c08-01", "category": "数学分析", "sub_category": "定积分应用",
 "concept": "参数曲线面积", "concept_id": "C08",
 "parent_training_ids": ["calc-area-009"],
 "problem": r"用参数方程求椭圆 $\begin{cases}x=a\cos t\\ y=b\sin t\end{cases}$($a,b>0$,$0\le t\le2\pi$)围成的面积。",
 "solution": r"面积公式 $A=\left|\int_0^{2\pi}y\,x'\,dt\right|$。$x'=-a\sin t$,故 $\int_0^{2\pi}y\,x'\,dt=\int_0^{2\pi}(b\sin t)(-a\sin t)\,dt=-ab\int_0^{2\pi}\sin^2t\,dt=-ab\cdot\pi=-\pi ab$。取绝对值得 $A=\pi ab$。",
 "answer": r"面积为 $\pi ab$。",
 "method": "参数方程面积公式(有向积分取绝对值)",
 "difficulty": "基础",
 "variant_kind": "曲线类型变化:椭圆参数方程的面积公式应用",
 "scene_spec": {
  "objects": [
   "平面坐标系:椭圆与内部阴影区域",
   "参数化标注:$(a\\cos t,b\\sin t)$ 的动点动画",
   "板书:$A=|\\int_0^{2\\pi}y\\,x'\\,dt|$",
   "板书:积分计算 $-ab\\pi$ 与取绝对值",
   "高亮框:$\\pi ab$"
  ],
  "steps": [
   "第一步:画出椭圆,动画展示参数化动点。",
   "第二步:写出面积公式与 $x'$。",
   "第三步:计算有向积分得 $-\\pi ab$。",
   "第四步:取绝对值得面积。",
   "第五步:高亮结论 $\\pi ab$。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c08-02", "category": "数学分析", "sub_category": "定积分应用",
 "concept": "参数曲线面积", "concept_id": "C08",
 "parent_training_ids": ["calc-area-009"],
 "problem": r"求星形线 $\begin{cases}x=a\cos^3 t\\ y=a\sin^3 t\end{cases}$($a>0$)围成的面积。",
 "solution": r"星形线在第一象限的部分对应 $t$ 从 $\frac{\pi}{2}$ 到 $0$。第一象限面积 $A_1=\int_{\frac{\pi}{2}}^{0}y\,x'\,dt$ 的绝对值,$x'=-3a\cos^2t\sin t$:$\int_{\frac{\pi}{2}}^{0}(a\sin^3t)(-3a\cos^2t\sin t)\,dt=3a^2\int_0^{\frac{\pi}{2}}\sin^4t\cos^2t\,dt=3a^2\cdot\frac{(3!!\cdot1!!)\pi}{6!!\cdot2}=3a^2\cdot\frac{3\pi}{96}=\frac{3\pi a^2}{32}$。总面积为 $4A_1=\frac{3\pi a^2}{8}$。",
 "answer": r"面积为 $\frac{3\pi a^2}{8}$。",
 "method": "参数方程面积公式(对称简化)",
 "difficulty": "基础",
 "variant_kind": "曲线类型变化:星形线的四象限对称面积",
 "scene_spec": {
  "objects": [
   "平面坐标系:星形线(四角星形状)与内部阴影",
   "第一象限部分高亮,其余淡化",
   "板书:$3a^2\\int_0^{\\pi/2}\\sin^4t\\cos^2t\\,dt$",
   "高亮框:$\\frac{3\\pi a^2}{8}$",
   "标签「四象限对称乘 4」"
  ],
  "steps": [
   "第一步:画出星形线,阴影标出内部。",
   "第二步:高亮第一象限部分,说明对称性。",
   "第三步:写出第一象限的面积积分并计算。",
   "第四步:乘以 $4$ 得总面积。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c08-03", "category": "数学分析", "sub_category": "定积分应用",
 "concept": "参数曲线面积", "concept_id": "C08",
 "parent_training_ids": ["calc-area-009"],
 "problem": r"求笛卡尔叶形线 $x=\frac{3t}{1+t^3}$，$y=\frac{3t^2}{1+t^3}$($t\ge0$)的环所围成的面积。",
 "solution": r"叶形线的环对应 $t$ 从 $0$ 到 $+\infty$(曲线从原点出发,经第一象限后回到原点)。用面积公式 $A=\frac12\int_0^{+\infty}(x\,y'-y\,x')\,dt$。计算:$x'=\frac{3(1-2t^3)}{(1+t^3)^2}$,$y'=\frac{3t(2-t^3)}{(1+t^3)^2}$,故 $x\,y'-y\,x'=\frac{9t^2(2-t^3)-9t^2(1-2t^3)}{(1+t^3)^3}=\frac{9t^2(1+t^3)}{(1+t^3)^3}=\frac{9t^2}{(1+t^3)^2}$。$A=\frac12\int_0^{+\infty}\frac{9t^2}{(1+t^3)^2}\,dt=\frac12\left.\left(-\frac{3}{1+t^3}\right)\right|_0^{+\infty}=\frac12\times3=\frac32$。",
 "answer": r"环的面积为 $\frac32$。",
 "method": "参数曲线面积公式(闭环+广义积分)",
 "difficulty": "中等",
 "variant_kind": "参数非单调:叶形线闭环的广义积分面积计算",
 "scene_spec": {
  "objects": [
   "平面坐标系:笛卡尔叶形线(环+渐近支),环内阴影",
   "动画:参数 $t$ 从 $0$ 增大,动点沿环行进",
   "板书:$xy'-yx'=\\frac{9t^2}{(1+t^3)^2}$ 的推导",
   "板书:广义积分 $\\frac12\\int_0^{+\\infty}$ 的计算",
   "高亮框:$\\frac32$"
  ],
  "steps": [
   "第一步:画出叶形线,阴影标出环部。",
   "第二步:动画展示动点从原点出发画环又回到原点。",
   "第三步:推导 $xy'-yx'$ 的化简结果。",
   "第四步:计算广义积分得 $\\frac32$。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c08-04", "category": "数学分析", "sub_category": "定积分应用",
 "concept": "参数曲线面积", "concept_id": "C08",
 "parent_training_ids": ["calc-area-009"],
 "problem": r"求李萨如曲线 $\begin{cases}x=\cos t\\ y=\sin 2t\end{cases}$ 的两个环各自的面积与总面积，并说明沿全周期 $[0,2\pi]$ 的有向积分为何为零。",
 "solution": r"曲线在 $t=\frac{\pi}{2}$ 与 $t=\frac{3\pi}{2}$ 处经过原点;在 $t=0$ 与 $t=\pi$ 处分别经过两环的顶点 $(1,0)$ 与 $(-1,0)$。两个环分别对应 $t\in[-\frac{\pi}{2},\frac{\pi}{2}]$ 与 $t\in[\frac{\pi}{2},\frac{3\pi}{2}]$。$x\,y'-y\,x'=\cos t\cdot2\cos2t-\sin2t\cdot(-\sin t)=2\cos t\cos2t+\sin t\sin2t$。第一环:$\int_{-\frac{\pi}{2}}^{\frac{\pi}{2}}(2\cos t\cos2t+\sin t\sin2t)\,dt=\int_{-\frac{\pi}{2}}^{\frac{\pi}{2}}\left(\frac32\cos t+\frac12\cos3t\right)dt=\left.\frac32\sin t+\frac16\sin3t\right|_{-\frac{\pi}{2}}^{\frac{\pi}{2}}=3-\frac13=\frac83$,故第一环面积 $\frac12\cdot\frac83=\frac43$。由对称性第二环面积也是 $\frac43$,总面积 $\frac83$。全周期有向积分:$\int_0^{2\pi}\cos t\cos2t\,dt=0$ 且 $\int_0^{2\pi}\sin t\sin2t\,dt=0$(正交性),两个环定向相反、有向值相消,故为零——有向面积为零而实际面积为 $\frac83$。",
 "answer": r"每环面积 $\frac43$,总面积 $\frac83$;全周期有向积分为 $0$(两环定向相反,相互抵消)。",
 "method": "参数曲线有向面积(闭环定向分析)",
 "difficulty": "中等",
 "variant_kind": "有向面积与实际面积:双环曲线的定向抵消辨析",
 "scene_spec": {
  "objects": [
   "平面坐标系:李萨如 8 字形曲线,两环阴影",
   "动画:动点沿 8 字行进,箭头标出两环的相反定向",
   "板书:$xy'-yx'=\\frac32\\cos t+\\frac12\\cos3t$ 的化简",
   "板书:第一环积分 $\\frac83$ 与乘 $\\frac12$",
   "高亮框:每环 $\\frac43$、总面积 $\\frac83$、有向和 $0$"
  ],
  "steps": [
   "第一步:画出 8 字形曲线,动画展示两环的相反定向。",
   "第二步:推导被积函数的三角化简。",
   "第三步:计算第一环的有向积分 $\\frac83$。",
   "第四步:由对称性得总面积,并展示两环定向相反。",
   "第五步:说明全周期正交性使有向积分为零,高亮对照结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c08-05", "category": "数学分析", "sub_category": "定积分应用",
 "concept": "参数曲线面积", "concept_id": "C08",
 "parent_training_ids": ["calc-area-009"],
 "problem": r"推导参数曲线 $\begin{cases}x=x(t)\\ y=y(t)\end{cases}$ 的面积公式,并分别说明简单闭曲线、$y$ 变号的图线、自交曲线三种情形下绝对值应放在哪里;再举一反例说明简单闭曲线为何不能分段取绝对值。",
 "solution": r"微元:沿曲线切片,面积微元为 $|y|\,dx=|y(t)x'(t)|\,dt$,带符号量 $y(t)x'(t)\,dt$ 的符号由曲线走向与 $y$ 的符号共同决定。情形一(简单闭曲线,不自交):两半支的带符号积分必须相加——它们的部分抵消恰好「剩出」内部面积,整圈积分后取一次绝对值即得面积:$A=\left|\int_{\alpha}^{\beta}y(t)x'(t)\,dt\right|$(格林公式:正向时 $\oint_L y\,dx=-\text{面积}$)。情形二(曲线为 $x$ 的图线且 $y$ 变号):在被积函数上取绝对值,$A=\int_{\alpha}^{\beta}\left|y(t)x'(t)\right|dt$,等价于在 $y=0$ 处分段分别取绝对值。情形三(自交曲线,如 $8$ 字形):先拆成若干简单圈,逐圈按情形一取绝对值后相加:$A=\sum_k\left|\oint_{L_k}y\,x'\,dt\right|$。反例(简单闭曲线不能分段取绝对值):圆 $x=\cos t$,$y=2+\sin t$($t\in[0,2\pi]$,圆心 $(0,2)$ 半径 $1$)。整圈积分 $\int_0^{2\pi}(2+\sin t)(-\sin t)\,dt=\int_0^{2\pi}(-2\sin t-\sin^2t)\,dt=0-\pi=-\pi$,面积 $|-\pi|=\pi$ ✓。若错误地在 $x'=0$(即 $t=0,\pi$)处拆成两段分别取绝对值:第一段 $\int_0^{\pi}y\,x'\,dt=-4-\frac{\pi}{2}$,第二段 $\int_{\pi}^{2\pi}y\,x'\,dt=4-\frac{\pi}{2}$,错误结果 $|-4-\frac{\pi}{2}|+|4-\frac{\pi}{2}|=8\neq\pi$。",
 "answer": r"规则:$A=\left|\int_{\alpha}^{\beta}yx'\,dt\right|$(简单闭曲线,整圈一次绝对值);$A=\int_{\alpha}^{\beta}|yx'|\,dt$($y$ 变号图线);$A=\sum_k\left|\oint_{L_k}yx'\,dt\right|$(自交曲线逐圈)。反例:$x=\cos t,y=2+\sin t$ 的圆,分段取绝对值得 $8\neq\pi$,证明简单闭曲线不可分段取绝对值。",
 "method": "面积公式推导(三种情形的绝对值规则+反例)",
 "difficulty": "进阶",
 "variant_kind": "推导型:面积公式推导与三种情形的绝对值位置规则,含分段取绝对值失效的反例",
 "scene_spec": {
  "objects": [
   "平面坐标系:圆 $x=\\cos t,y=2+\\sin t$(两半支异色)与内部阴影",
   "动画:整圈积分两半支的带符号贡献相加,部分抵消后剩出面积",
   "板书:情形一公式 $A=|\\int yx'\\,dt|$(整圈一次绝对值)",
   "板书:情形二 $A=\\int|yx'|\\,dt$ 与情形三 $\\sum_k|\\oint_{L_k}yx'\\,dt|$",
   "红色警示:分段取绝对值得 $8\\neq\\pi$ 的反例计算"
  ],
  "steps": [
   "第一步:写出面积微元 $|y|dx=|yx'|dt$,说明带符号量的来源。",
   "第二步:情形一:动画展示两半支带符号积分相加、部分抵消剩出内部面积。",
   "第三步:写出整圈一次绝对值的公式,并说明情形二、三的规则。",
   "第四步:展示反例圆:整圈积分为 $-\\pi$,面积 $\\pi$。",
   "第五步:红色警示分段取绝对值的错误结果 $8\\neq\\pi$,总结三种情形的正确规则。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
# ===================== C09 旋转体体积 =====================
{
 "id": "draft-c09-01", "category": "数学分析", "sub_category": "定积分应用",
 "concept": "旋转体体积", "concept_id": "C09",
 "parent_training_ids": ["calc-vol-012"],
 "problem": r"求由曲线 $y=\sqrt{x}$、直线 $x=4$ 与 $x$ 轴围成的图形绕 $x$ 轴旋转所得旋转体的体积。",
 "solution": r"圆盘法:旋转半径为 $R(x)=\sqrt{x}$,$0\le x\le4$。$V=\pi\int_0^4R(x)^2\,dx=\pi\int_0^4x\,dx=\pi\left.\frac{x^2}{2}\right|_0^4=8\pi$。",
 "answer": r"体积为 $8\pi$。",
 "method": "圆盘法(绕 x 轴)",
 "difficulty": "基础",
 "variant_kind": "曲线类型变化:根式函数的圆盘法(与反三角父题不同)",
 "scene_spec": {
  "objects": [
   "平面坐标系:曲线 $y=\\sqrt{x}$、直线 $x=4$ 与 $x$ 轴围成的区域(阴影)",
   "旋转体(碗状旋转抛物面)的三维示意",
   "圆盘微元动画:在 $x$ 处半径为 $\\sqrt{x}$ 的圆盘",
   "板书:$V=\\pi\\int_0^4x\\,dx$",
   "高亮框:$8\\pi$"
  ],
  "steps": [
   "第一步:画出平面区域,阴影标注。",
   "第二步:三维示意旋转体,动画展示圆盘微元。",
   "第三步:写出圆盘法积分。",
   "第四步:计算得 $8\\pi$。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c09-02", "category": "数学分析", "sub_category": "定积分应用",
 "concept": "旋转体体积", "concept_id": "C09",
 "parent_training_ids": ["calc-vol-012"],
 "problem": r"用柱壳法求由曲线 $y=x^2$、直线 $x=1$ 与 $x$ 轴围成的图形绕 $y$ 轴旋转所得旋转体的体积。",
 "solution": r"柱壳法:在 $x$ 处取厚度 $dx$ 的竖直薄片,绕 $y$ 轴旋转形成半径为 $x$、高为 $x^2$ 的柱壳,体积微元 $dV=2\pi x\cdot x^2\,dx$。$V=2\pi\int_0^1x\cdot x^2\,dx=2\pi\int_0^1x^3\,dx=2\pi\cdot\frac14=\frac{\pi}{2}$。",
 "answer": r"体积为 $\frac{\pi}{2}$。",
 "method": "柱壳法(绕 y 轴)",
 "difficulty": "基础",
 "variant_kind": "方法变化:绕 y 轴的柱壳法(与绕 x 轴圆盘法对照)",
 "scene_spec": {
  "objects": [
   "平面坐标系:曲线 $y=x^2$ 与直线 $x=1$、$x$ 轴围成的区域(阴影)",
   "旋转体三维示意(绕 $y$ 轴)",
   "柱壳微元动画:在 $x$ 处半径 $x$、高 $x^2$ 的薄壳",
   "板书:$V=2\\pi\\int_0^1x\\cdot x^2\\,dx$",
   "高亮框:$\\frac{\\pi}{2}$"
  ],
  "steps": [
   "第一步:画出平面区域,阴影标注。",
   "第二步:三维示意绕 $y$ 轴的旋转体。",
   "第三步:动画展示柱壳微元(半径 $x$,高 $x^2$)。",
   "第四步:写出柱壳积分并计算。",
   "第五步:高亮结论 $\\frac{\\pi}{2}$。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c09-03", "category": "数学分析", "sub_category": "定积分应用",
 "concept": "旋转体体积", "concept_id": "C09",
 "parent_training_ids": ["calc-vol-012"],
 "problem": r"求由曲线 $y=x$ 与 $y=x^2$ 围成的区域绕 $x$ 轴旋转所得旋转体的体积。",
 "solution": r"两曲线交点:$x=0,1$。区域绕 $x$ 轴旋转形成中空的旋转体,用垫圈法:外半径 $R(x)=x$,内半径 $r(x)=x^2$。$V=\pi\int_0^1\left[R(x)^2-r(x)^2\right]dx=\pi\int_0^1(x^2-x^4)\,dx=\pi\left(\frac13-\frac15\right)=\frac{2\pi}{15}$。",
 "answer": r"体积为 $\frac{2\pi}{15}$。",
 "method": "垫圈法(空腔旋转体)",
 "difficulty": "中等",
 "variant_kind": "空腔:两曲线围成区域的垫圈法(内外半径相减)",
 "scene_spec": {
  "objects": [
   "平面坐标系:曲线 $y=x$ 与 $y=x^2$ 围成的区域(阴影)",
   "旋转体三维示意(中空,剖面可见空腔)",
   "垫圈微元动画:外半径 $x$、内半径 $x^2$ 的圆环",
   "板书:$V=\\pi\\int_0^1(x^2-x^4)dx$",
   "高亮框:$\\frac{2\\pi}{15}$"
  ],
  "steps": [
   "第一步:画出两条曲线与围成区域,标出交点。",
   "第二步:三维示意中空旋转体,动画展示垫圈微元。",
   "第三步:写出内外半径平方差的积分。",
   "第四步:计算得 $\\frac{2\\pi}{15}$。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c09-04", "category": "数学分析", "sub_category": "定积分应用",
 "concept": "旋转体体积", "concept_id": "C09",
 "parent_training_ids": ["calc-vol-012"],
 "problem": r"求由曲线 $y=x^2$、$x$ 轴与直线 $x=1$ 所围成的区域绕直线 $x=-1$ 旋转所得旋转体的体积。",
 "solution": r"旋转轴为 $x=-1$,用柱壳法:在 $x$ 处柱壳到轴的距离为 $x-(-1)=x+1$,高为 $x^2$。$V=2\pi\int_0^1(x+1)x^2\,dx=2\pi\int_0^1(x^3+x^2)\,dx=2\pi\left(\frac14+\frac13\right)=\frac{7\pi}{6}$。",
 "answer": r"体积为 $\frac{7\pi}{6}$。",
 "method": "柱壳法(旋转轴平移)",
 "difficulty": "中等",
 "variant_kind": "旋转轴平移:轴不在坐标轴上时柱壳半径的平移修正",
 "scene_spec": {
  "objects": [
   "平面坐标系:曲线 $y=x^2$、直线 $x=1$、$x$ 轴围成的区域(阴影)与旋转轴直线 $x=-1$(虚线)",
   "柱壳微元动画:半径为 $x+1$ 的薄壳",
   "板书:$V=2\\pi\\int_0^1(x+1)x^2\\,dx$",
   "高亮框:$\\frac{7\\pi}{6}$",
   "标签「轴平移:半径 $x+1$」"
  ],
  "steps": [
   "第一步:画出区域(曲线 $y=x^2$、$x$ 轴与直线 $x=1$ 围成)与旋转轴 $x=-1$,标出轴与区域的距离。",
   "第二步:动画展示柱壳微元,说明半径为 $x+1$。",
   "第三步:写出含平移修正的积分。",
   "第四步:计算得 $\\frac{7\\pi}{6}$。",
   "第五步:高亮结论,强调轴平移的半径修正。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c09-05", "category": "数学分析", "sub_category": "定积分应用",
 "concept": "旋转体体积", "concept_id": "C09",
 "parent_training_ids": ["calc-vol-012"],
 "problem": r"求由曲线 $y=\sin x$($0\le x\le\pi$)与 $x$ 轴围成的区域分别绕 $x$ 轴与 $y$ 轴旋转所得旋转体的体积，并说明两种情况下所用方法的适用性。",
 "solution": r"绕 $x$ 轴(圆盘法):$V_x=\pi\int_0^{\pi}\sin^2x\,dx=\pi\cdot\frac{\pi}{2}=\frac{\pi^2}{2}$。绕 $y$ 轴(柱壳法):区域到 $y$ 轴的距离为 $x$,高为 $\sin x$,$V_y=2\pi\int_0^{\pi}x\sin x\,dx$。分部积分:$\int_0^{\pi}x\sin x\,dx=\left.\sin x-x\cos x\right|_0^{\pi}=\pi$,故 $V_y=2\pi\cdot\pi=2\pi^2$。方法适用性:绕 $x$ 轴时截面为圆盘,圆盘法直接;绕 $y$ 轴时按 $y$ 切片需要把曲线分成两支反解 $x$,柱壳法(对 $x$ 积分)更自然。",
 "answer": r"绕 $x$ 轴:$\frac{\pi^2}{2}$;绕 $y$ 轴:$2\pi^2$。",
 "method": "圆盘法与柱壳法对照(同一区域绕两轴)",
 "difficulty": "进阶",
 "variant_kind": "双轴对照:同一区域绕两轴的方法选择与适用性辨析",
 "scene_spec": {
  "objects": [
   "平面坐标系:曲线 $y=\\sin x$ 与 $x$ 轴围成的区域(阴影)",
   "两个三维示意:绕 $x$ 轴的橄榄形与绕 $y$ 轴的喇叭形",
   "板书:圆盘法 $V_x=\\pi\\int_0^\\pi\\sin^2x\\,dx$",
   "板书:柱壳法 $V_y=2\\pi\\int_0^\\pi x\\sin x\\,dx$ 与分部积分",
   "高亮框:$\\frac{\\pi^2}{2}$ 与 $2\\pi^2$"
  ],
  "steps": [
   "第一步:画出平面区域。",
   "第二步:三维示意绕 $x$ 轴的旋转体,圆盘法直接计算。",
   "第三步:三维示意绕 $y$ 轴的旋转体,说明按 $y$ 切片需分两支。",
   "第四步:柱壳法对 $x$ 积分,分部积分计算。",
   "第五步:对照两法结果与适用性,高亮结论。"
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
