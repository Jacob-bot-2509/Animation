"""batch-10 生成器:三个单条考点各 5 题
(C15 直线与平面夹角 / C17 平面方程与构造 / C19 柱面与方程的空间意义)。
全部数学结论由作者逐题手工验算(见 DRAFT_REPORT.md 核算说明);
起草过程未读 eval/test 题文或答案作提示;凡有理数一律分数。
"""
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "draft.jsonl"

DATA = [
# ===================== C15 直线与平面夹角 =====================
{
 "id": "draft-c15-01", "category": "解析几何", "sub_category": "空间直线与平面",
 "concept": "直线与平面夹角", "concept_id": "C15",
 "parent_training_ids": ["geom-020"],
 "problem": r"求直线 $l:\frac{x-1}{1}=\frac{y+2}{0}=\frac{z}{1}$ 与平面 $\pi:x+y=1$ 的夹角。",
 "solution": r"直线方向 $d=(1,0,1)$,平面法向量 $n=(1,1,0)$。夹角公式 $\sin\varphi=\frac{|d\cdot n|}{|d|\,|n|}=\frac{|1\times1+0\times1+1\times0|}{\sqrt{2}\times\sqrt{2}}=\frac{1}{2}$,故 $\varphi=\arcsin\frac12=\frac{\pi}{6}$,即 $30^\circ$。",
 "answer": r"夹角为 $\frac{\pi}{6}$(即 $30^\circ$)。",
 "method": "方向向量与法向量夹角公式",
 "difficulty": "基础",
 "variant_kind": "数值结构变化:方向含零分量的夹角计算(与父题不同直线/平面)",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "半透明平面 $\\pi:x+y=1$ 与其法向量箭头 $n=(1,1,0)$",
   "直线 $l$(方向 $(1,0,1)$)与方向向量箭头",
   "夹角标记弧线(标注 $30^\\circ$)",
   "板书:$\\sin\\varphi=\\frac{|d\\cdot n|}{|d||n|}=\\frac12$"
  ],
  "steps": [
   "第一步:画出平面与直线,标出法向量与方向向量。",
   "第二步:写出夹角公式并代入计算。",
   "第三步:得 $\\sin\\varphi=\\frac12$。",
   "第四步:在图中画出夹角弧线,标注 $30^\\circ$。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c15-02", "category": "解析几何", "sub_category": "空间直线与平面",
 "concept": "直线与平面夹角", "concept_id": "C15",
 "parent_training_ids": ["geom-020"],
 "problem": r"判断直线 $l:\frac{x-1}{1}=\frac{y-2}{2}=\frac{z-3}{-1}$ 与平面 $\pi:x+2y-z=0$ 的位置关系；再判断过点 $(1,1,2)$、方向为 $(1,-1,1)$ 的直线 $l'$ 与平面 $\pi':x+y=0$ 的位置关系。",
 "solution": r"$l$ 的方向 $d=(1,2,-1)$ 与 $\pi$ 的法向量 $n=(1,2,-1)$ 平行($d=n$),故 $l\perp\pi$(直线垂直于平面)。$l'$ 的方向 $d'=(1,-1,1)$ 与 $\pi'$ 的法向量 $n'=(1,1,0)$ 的内积为 $1-1+0=0$,故 $d'\perp n'$,即 $l'\parallel\pi'$;又点 $(1,1,2)$ 代入 $x+y=2\neq0$,不在平面内,故 $l'$ 与 $\pi'$ 平行且不重合。",
 "answer": r"$l\perp\pi$(方向平行于法向);$l'\parallel\pi'$ 且不重合($d'\perp n'$ 且所过点不在平面内)。",
 "method": "方向与法向关系判定(退化分支)",
 "difficulty": "基础",
 "variant_kind": "退化分支:垂直(方向∥法向)与平行(方向⊥法向+点不在面内)的判定",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "平面 $\\pi$ 与直线 $l$ 的垂直关系示意(直角标记)",
   "平面 $\\pi'$ 与直线 $l'$ 的平行关系示意(平行箭头)",
   "板书:$d=(1,2,-1)=n$ 与 $d'\\cdot n'=1-1+0=0$",
   "高亮框:「垂直」与「平行不重合」"
  ],
  "steps": [
   "第一步:画出 $l$ 与 $\\pi$,展示方向与法向平行的垂直关系。",
   "第二步:画出 $l'$ 与 $\\pi'$,展示方向与法向正交。",
   "第三步:代入 $l'$ 所过点验证其不在平面内。",
   "第四步:得出平行且不重合的结论。",
   "第五步:高亮两个退化分支的判定结果。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c15-03", "category": "解析几何", "sub_category": "空间直线与平面",
 "concept": "直线与平面夹角", "concept_id": "C15",
 "parent_training_ids": ["geom-020"],
 "problem": r"求过点 $P(1,2,3)$、法向量位于 $xz$ 平面内、且与方向为 $(1,1,0)$ 的直线成 $30^\circ$ 角的平面方程。",
 "solution": r"设法向量 $n=(a,0,c)$($a,c$ 不同时为零)。夹角条件:$\sin30^\circ=\frac{|(a,0,c)\cdot(1,1,0)|}{|n|\cdot\sqrt2}=\frac{|a|}{\sqrt{a^2+c^2}\cdot\sqrt2}=\frac12$,平方得 $2a^2=a^2+c^2$,即 $c=\pm a$。取 $a=1$:$n=(1,0,1)$ 或 $(1,0,-1)$。过 $P(1,2,3)$:平面 $1(x-1)+0(y-2)+1(z-3)=0$ 即 $x+z=4$;或 $1(x-1)+0(y-2)-1(z-3)=0$ 即 $x-z=-2$。验证:$n=(1,0,1)$ 与 $(1,1,0)$ 的夹角余弦 $\frac{1}{\sqrt2\sqrt2}=\frac12$,直线与平面夹角确为 $30^\circ$ ✓。",
 "answer": r"两个平面:$x+z=4$ 与 $x-z=-2$。",
 "method": "逆向构造(夹角条件反求法向量)",
 "difficulty": "中等",
 "variant_kind": "逆向构造:由夹角与法向约束反求平面(两解)",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "点 $P(1,2,3)$ 与方向 $(1,1,0)$ 的参考直线",
   "两个平面 $x+z=4$ 与 $x-z=-2$(半透明)",
   "夹角弧线:$30^\\circ$ 标注",
   "板书:$c=\\pm a$ 的推导"
  ],
  "steps": [
   "第一步:标出点 $P$ 与参考方向。",
   "第二步:设法向量 $(a,0,c)$,由夹角条件得 $c=\\pm a$。",
   "第三步:取两个法向量,写出两个平面方程。",
   "第四步:画出两平面与参考直线,标出夹角。",
   "第五步:验证两平面均满足条件,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c15-04", "category": "解析几何", "sub_category": "空间直线与平面",
 "concept": "直线与平面夹角", "concept_id": "C15",
 "parent_training_ids": ["geom-020"],
 "problem": r"求直线 $l$：过原点、方向为 $(1,1,1)$ 与平面 $\pi:x+y=0$ 的夹角 $\varphi$；再求 $l$ 在 $\pi$ 上的投影直线的方向，并求 $l$ 与其投影线的夹角 $\theta$，说明 $\theta$ 与 $\varphi$ 的关系。",
 "solution": r"平面法向量 $n=(1,1,0)$。$\sin\varphi=\frac{|(1,1,1)\cdot(1,1,0)|}{\sqrt3\cdot\sqrt2}=\frac{2}{\sqrt6}=\sqrt{\frac23}$,故 $\varphi=\arcsin\sqrt{\frac23}$。投影方向:$d'=d-\frac{d\cdot n}{|n|^2}n=(1,1,1)-\frac{2}{2}(1,1,0)=(0,0,1)$。$l$ 与投影线的夹角 $\theta$:$\cos\theta=\frac{d\cdot d'}{|d||d'|}=\frac{1}{\sqrt3\cdot1}=\frac{1}{\sqrt3}$,故 $\theta=\arccos\frac{1}{\sqrt3}$。数值核对:$\sin^2\varphi=\frac23$,而 $1-\cos^2\theta=1-\frac13=\frac23$;事实上线面夹角的定义就是直线与其投影线的夹角,故 $\theta=\varphi$(两者都等于 $90^\circ-\angle(d,n)$,即都与 $d$ 与 $n$ 的夹角互余)。",
 "answer": r"$\varphi=\arcsin\sqrt{\frac23}$;投影方向 $(0,0,1)$;$\theta=\arccos\frac{1}{\sqrt3}$,且 $\theta=\varphi$(两者均为 $90^\circ-\angle(d,n)$,数值约 $54.7^\circ$)。",
 "method": "投影重建(正交分解)",
 "difficulty": "中等",
 "variant_kind": "从投影重建:直线在平面上的投影方向与夹角的三角关系",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "平面 $\\pi:x+y=0$ 与直线 $l$(方向 $(1,1,1)$)",
   "投影直线(方向 $(0,0,1)$,虚线高亮)与正交分解示意",
   "板书:$d'=d-\\frac{d\\cdot n}{|n|^2}n=(0,0,1)$",
   "高亮框:$\\theta=\\varphi\\approx54.7^\\circ$($\\sin^2\\varphi=1-\\cos^2\\theta=\\frac23$)"
  ],
  "steps": [
   "第一步:画出平面与直线,计算夹角 $\\varphi$。",
   "第二步:正交分解方向向量,得投影方向 $(0,0,1)$。",
   "第三步:在图中画出投影直线,标注正交分解。",
   "第四步:计算 $\\theta$ 并推导两者的三角关系。",
   "第五步:高亮关系式,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c15-05", "category": "解析几何", "sub_category": "空间直线与平面",
 "concept": "直线与平面夹角", "concept_id": "C15",
 "parent_training_ids": ["geom-020"],
 "problem": r"证明直线与平面夹角公式 $\sin\varphi=\frac{|d\cdot n|}{|d|\,|n|}$，并讨论 $d\cdot n=0$ 与 $d\times n=0$ 两个退化分支对应的位置关系及判定方法。",
 "solution": r"记 $\psi$ 为直线方向 $d$ 与平面法向量 $n$ 的夹角(取 $[0,\frac{\pi}{2}]$ 内的值)。正交分解:$d=d'+\frac{d\cdot n}{|n|^2}n$,其中 $d'$ 位于平面的方向子空间内且 $d'\perp n$。当 $d'$ 非零时,直线与其投影线(方向 $d'$)的夹角 $\varphi$ 满足:在由 $d,d'$ 与法向分量张成的直角三角形中,$d$ 与 $d'$ 的夹角为 $\varphi$,$d$ 与 $n$ 的夹角为 $\psi$,故 $\varphi+\psi=\frac{\pi}{2}$,即 $\sin\varphi=\cos\psi=\frac{|d\cdot n|}{|d|\,|n|}$;当 $d'=0$(即 $d\parallel n$)时,直线垂直于平面,投影退化为一个点,约定夹角 $\varphi=\frac{\pi}{2}$,此时公式右端 $\frac{|d\cdot n|}{|d||n|}=1$,仍成立。退化分支一:$d\cdot n=0\iff d\perp n\iff l\parallel\pi$;此时若 $l$ 上某点在 $\pi$ 上,则 $l\subset\pi$(直线完全落在平面内),否则 $l$ 与 $\pi$ 平行无公共点——判定需代入直线上一点。退化分支二:$d\times n=0\iff d\parallel n\iff l\perp\pi$,此时直线与平面恰有一个交点(垂足)。非退化情形($d\cdot n\neq0$ 且 $d\times n\neq0$):直线与平面斜交于一点。",
 "answer": r"公式由 $\varphi+\psi=\frac{\pi}{2}$ 与 $\cos\psi=\frac{|d\cdot n|}{|d||n|}$ 得;退化分支:$d\cdot n=0\iff l\parallel\pi$(再以点是否在面内区分含于面内/平行),$d\times n=0\iff l\perp\pi$(证明见解法)。",
 "method": "公式推导+退化分支完整讨论",
 "difficulty": "进阶",
 "variant_kind": "证明型:夹角公式推导与两种退化位置关系的判定准则",
 "scene_spec": {
  "objects": [
   "三维示意图:直线与平面及夹角 $\\varphi$、法向夹角 $\\psi$ 的标注",
   "板书:$\\varphi+\\psi=\\frac\\pi2$ 与 $\\sin\\varphi=\\cos\\psi$ 的推导",
   "三种情形对照图:斜交、平行(含面内)、垂直",
   "板书:退化判定 $d\\cdot n=0$ 与 $d\\times n=0$",
   "高亮框:判定方法汇总表"
  ],
  "steps": [
   "第一步:画出夹角示意图,标注 $\\varphi$ 与 $\\psi$。",
   "第二步:推导互余关系与公式。",
   "第三步:对照展示斜交、平行、垂直三种情形。",
   "第四步:推导两个退化条件的判定准则。",
   "第五步:高亮汇总表,完成证明。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
# ===================== C17 平面方程与构造 =====================
{
 "id": "draft-c17-01", "category": "解析几何", "sub_category": "平面",
 "concept": "平面方程与构造", "concept_id": "C17",
 "parent_training_ids": ["geom-022"],
 "problem": r"求过点 $P(1,-2,3)$ 且以 $n=(2,1,-2)$ 为法向量的平面方程。",
 "solution": r"点法式:$2(x-1)+1(y+2)-2(z-3)=0$,展开得 $2x+y-2z+6=0$。验证:代入 $P$:$2-2-6+6=0$ ✓。",
 "answer": r"平面方程为 $2x+y-2z+6=0$。",
 "method": "点法式",
 "difficulty": "基础",
 "variant_kind": "构造路径变化:点法式(与三点式父题不同)",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "点 $P(1,-2,3)$ 与法向量箭头 $n=(2,1,-2)$",
   "半透明平面 $2x+y-2z+6=0$",
   "板书:点法式代入过程",
   "验证板书:代入 $P$ 得 $0$"
  ],
  "steps": [
   "第一步:标出点 $P$ 与法向量。",
   "第二步:写出点法式并展开。",
   "第三步:画出平面。",
   "第四步:验证点满足方程。",
   "第五步:高亮方程。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c17-02", "category": "解析几何", "sub_category": "平面",
 "concept": "平面方程与构造", "concept_id": "C17",
 "parent_training_ids": ["geom-022"],
 "problem": r"求过点 $P(1,1,1)$ 且平行于向量 $a=(1,0,1)$ 与 $b=(0,1,1)$ 的平面方程。",
 "solution": r"平面的法向量可取 $n=a\times b=(1,0,1)\times(0,1,1)=(0\times1-1\times1,\,1\times0-1\times1,\,1\times1-0\times0)=(-1,-1,1)$。由点法式:$-(x-1)-(y-1)+(z-1)=0$,即 $x+y-z=1$。验证:$P$ 满足 $1+1-1=1$ ✓;$a\cdot n=-1+0+1=0$,$b\cdot n=0-1+1=0$,两个方向均在平面内 ✓。",
 "answer": r"平面方程为 $x+y-z=1$。",
 "method": "叉积求法向量+点法式",
 "difficulty": "基础",
 "variant_kind": "构造条件变化:一点+两平行方向(叉积定法向)",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "点 $P(1,1,1)$ 与两个方向向量 $a,b$ 的箭头",
   "半透明平面 $x+y-z=1$",
   "板书:叉积 $a\\times b=(-1,-1,1)$ 的计算",
   "验证板书:两方向与法向均正交"
  ],
  "steps": [
   "第一步:标出点 $P$ 与两个方向向量。",
   "第二步:叉积得法向量。",
   "第三步:点法式写出平面方程。",
   "第四步:画出平面。",
   "第五步:验证两方向均在平面内。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c17-03", "category": "解析几何", "sub_category": "平面",
 "concept": "平面方程与构造", "concept_id": "C17",
 "parent_training_ids": ["geom-022"],
 "problem": r"求过 $A(1,1,1)$、$B(2,2,2)$ 且平行于 $x$ 轴的平面方程，并说明为什么只用两个共线的点不能确定平面。",
 "solution": r"$\overrightarrow{AB}=(1,1,1)$,$x$ 轴方向 $e=(1,0,0)$。$AB$ 与 $e$ 不平行,两者张成所求平面的方向子空间,法向量 $n=\overrightarrow{AB}\times e=(1,1,1)\times(1,0,0)=(1\times0-1\times0,\,1\times1-1\times0,\,1\times0-1\times1)=(0,1,-1)$。点法式:$0(x-1)+(y-1)-(z-1)=0$,即 $y=z$。验证:$A,B$ 均满足 $y=z$ ✓;方向 $e$ 与 $n$ 正交 ✓。说明:$A,B$ 共线时,两个点只给出一个方向,而空间中过一条定直线的平面有无穷多个(绕该直线旋转),必须再给一个与 $AB$ 不共线的方向或条件才能唯一确定平面。",
 "answer": r"平面方程为 $y=z$;共线两点只确定一个方向,过该直线的平面有无穷多个,故不能唯一确定平面。",
 "method": "叉积定法向(共线两点的不可决定性说明)",
 "difficulty": "中等",
 "variant_kind": "共线导致不唯一:两点共线时的条件补全与可决定性说明",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "两点 $A,B$ 与直线 $AB$",
   "动画:过直线 $AB$ 的平面族绕其旋转(说明不唯一)",
   "半透明平面 $y=z$ 与 $x$ 轴方向箭头",
   "板书:$n=AB\\times e=(0,1,-1)$"
  ],
  "steps": [
   "第一步:标出 $A,B$,连线。",
   "第二步:动画展示绕 $AB$ 旋转的平面族,说明不唯一。",
   "第三步:加入与 $x$ 轴平行的条件,叉积定法向。",
   "第四步:写出平面 $y=z$ 并画出。",
   "第五步:总结共线两点不可唯一确定平面的理由。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c17-04", "category": "解析几何", "sub_category": "平面",
 "concept": "平面方程与构造", "concept_id": "C17",
 "parent_training_ids": ["geom-022"],
 "problem": r"写出过直线 $l:\begin{cases}x+y+z=1\\ x-y+2z=0\end{cases}$ 的平面束方程，并求其中过点 $P(1,1,1)$ 的平面。",
 "solution": r"过交线的平面束:$(x+y+z-1)+\lambda(x-y+2z)=0$($\lambda$ 为参数;注意 $\lambda$ 取遍实数时给出过 $l$ 的除 $x-y+2z=0$ 外的一切平面)。代入 $P(1,1,1)$:$(1+1+1-1)+\lambda(1-1+2)=0$,即 $2+2\lambda=0$,$\lambda=-1$。故所求平面为 $(x+y+z-1)-(x-y+2z)=0$,即 $2y-z-1=0$。验证:$P$ 满足 $2-1-1=0$ ✓;直线 $l$ 上点满足两原方程,故也满足其线性组合,平面过 $l$ ✓。",
 "answer": r"平面束:$(x+y+z-1)+\lambda(x-y+2z)=0$;过 $P$ 的平面为 $2y-z-1=0$(对应 $\lambda=-1$)。",
 "method": "平面束参数化+定点定参",
 "difficulty": "中等",
 "variant_kind": "平面族参数:过定直线的平面束与过定点条件定参",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "两个基础平面的交线 $l$(高亮)",
   "动画:平面束绕 $l$ 旋转(参数 $\\lambda$ 滑动)",
   "半透明平面 $2y-z-1=0$ 与点 $P(1,1,1)$",
   "板书:代入 $P$ 解出 $\\lambda=-1$"
  ],
  "steps": [
   "第一步:画出两平面与交线 $l$。",
   "第二步:写出平面束的一般式。",
   "第三步:动画展示束绕 $l$ 旋转。",
   "第四步:代入 $P$ 解出 $\\lambda=-1$,得所求平面。",
   "第五步:验证平面过 $l$ 与 $P$,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c17-05", "category": "解析几何", "sub_category": "平面",
 "concept": "平面方程与构造", "concept_id": "C17",
 "parent_training_ids": ["geom-022"],
 "problem": r"推导平面的截距式方程，并求过点 $P(1,2,3)$ 且在三坐标轴上的截距都相等且不为零(即平面不过原点)的平面方程。",
 "solution": r"设平面在 $x,y,z$ 轴上的截距分别为 $a,b,c$($abc\neq0$),即平面过 $(a,0,0),(0,b,0),(0,0,c)$。三点确定平面:设一般式 $Ax+By+Cz+D=0$($D\neq0$),代入三点得 $Aa+D=0,Bb+D=0,Cc+D=0$,即 $A=-\frac Da,B=-\frac Db,C=-\frac Dc$,代入并除以 $-D$:$\frac{x}{a}+\frac{y}{b}+\frac{z}{c}=1$,即截距式。截距相等:设 $a=b=c=t\neq0$,方程为 $\frac{x+y+z}{t}=1$,即 $x+y+z=t$。过 $P(1,2,3)$:$1+2+3=t$,$t=6$。故所求平面为 $x+y+z=6$。(若允许零截距,则过原点且过 $P$ 的平面有无穷多个,条件不足以唯一确定,故本题约定截距非零。)",
 "answer": r"截距式:$\frac{x}{a}+\frac{y}{b}+\frac{z}{c}=1$($abc\neq0$);$x+y+z=6$。",
 "method": "截距式推导+含截距条件构造",
 "difficulty": "进阶",
 "variant_kind": "推导+构造:截距式的推导与等截距条件下的平面构造",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "平面与三坐标轴的交点(截距 $a,b,c$ 标注)",
   "板书:一般式代入三点的推导",
   "高亮框:截距式 $\\frac xa+\\frac yb+\\frac zc=1$",
   "板书:等截距代入 $P$ 得 $t=6$,平面 $x+y+z=6$"
  ],
  "steps": [
   "第一步:画出平面与坐标轴交点,标注截距。",
   "第二步:由一般式代入三点推导截距式。",
   "第三步:高亮截距式公式。",
   "第四步:令三截距相等,用 $P$ 定出 $t=6$。",
   "第五步:画出平面 $x+y+z=6$,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
# ===================== C19 柱面与方程的空间意义 =====================
{
 "id": "draft-c19-01", "category": "解析几何", "sub_category": "二次曲面",
 "concept": "柱面与方程的空间意义", "concept_id": "C19",
 "parent_training_ids": ["geom-024"],
 "problem": r"说明方程 $y^2=2x$ 在空间直角坐标系中表示什么曲面，并指出它与 $xy$ 平面内的曲线 $y^2=2x$ 的区别。",
 "solution": r"方程不含 $z$:若 $(x,y,z)$ 满足 $y^2=2x$,则对任意 $z'$,$(x,y,z')$ 也满足。故该方程表示母线平行于 $z$ 轴的抛物柱面——准线是 $xy$ 平面内的抛物线 $y^2=2x$,过准线上每一点作平行于 $z$ 轴的直线,这些直线的并集即曲面。区别:平面内方程 $y^2=2x$ 表示一条曲线(一维),空间同一方程表示一张曲面(二维,沿 $z$ 方向无限延伸)。",
 "answer": r"母线平行于 $z$ 轴的抛物柱面(准线 $y^2=2x$);平面内同方程为曲线,空间中为曲面。",
 "method": "缺变量方程的柱面识别",
 "difficulty": "基础",
 "variant_kind": "曲线与曲面辨析:缺变量方程在平面与空间中的不同含义",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "抛物柱面 $y^2=2x$(沿 $z$ 轴无限延伸)",
   "$xy$ 平面内的准线抛物线高亮",
   "母线动画:沿 $z$ 方向平移抛物线扫出柱面",
   "标签「母线∥z 轴」"
  ],
  "steps": [
   "第一步:在 $xy$ 平面画出准线抛物线。",
   "第二步:动画沿 $z$ 轴平移抛物线,扫出柱面。",
   "第三步:说明方程不含 $z$ 的几何含义。",
   "第四步:指出平面内曲线与空间曲面的维数区别。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c19-02", "category": "解析几何", "sub_category": "二次曲面",
 "concept": "柱面与方程的空间意义", "concept_id": "C19",
 "parent_training_ids": ["geom-024"],
 "problem": r"求以 $xy$ 平面内的圆 $x^2+y^2=1$($z=0$)为准线、母线平行于直线 $l$:方向 $(1,1,1)$ 的柱面方程。",
 "solution": r"柱面上点 $(x,y,z)$ 沿母线方向 $(1,1,1)$ 平移后可落到准线上:存在 $s$ 使 $(x-s,y-s,z-s)$ 满足 $z-s=0$ 且 $x^2+y^2$ 条件,即取 $s=z$,得 $(x-z)^2+(y-z)^2=1$。故柱面方程为 $(x-z)^2+(y-z)^2=1$。验证:准线上点 $(x_0,y_0,0)$($x_0^2+y_0^2=1$)满足 $(x_0-0)^2+(y_0-0)^2=1$ ✓;过准线上点沿 $(1,1,1)$ 的直线 $(x_0+s,y_0+s,s)$:$(x_0+s-s)^2+(y_0+s-s)^2=x_0^2+y_0^2=1$ ✓,整条母线在曲面上。",
 "answer": r"柱面方程为 $(x-z)^2+(y-z)^2=1$。",
 "method": "斜母线柱面构造(变量替换)",
 "difficulty": "基础",
 "variant_kind": "非坐标方向母线:斜母线的圆柱面方程构造",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "$xy$ 平面内的圆(准线)高亮",
   "斜圆柱面 $(x-z)^2+(y-z)^2=1$",
   "母线方向箭头 $(1,1,1)$",
   "板书:$(x-z)^2+(y-z)^2=1$ 的推导"
  ],
  "steps": [
   "第一步:画出 $xy$ 平面内的准线圆。",
   "第二步:标出斜母线方向 $(1,1,1)$。",
   "第三步:推导沿母线平移的坐标条件。",
   "第四步:画出斜圆柱面。",
   "第五步:验证准线与母线都在曲面上。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c19-03", "category": "解析几何", "sub_category": "二次曲面",
 "concept": "柱面与方程的空间意义", "concept_id": "C19",
 "parent_training_ids": ["geom-024"],
 "problem": r"求柱面 $x^2+y^2=1$ 与平面 $z=2x$ 的交线方程及其在 $xy$ 平面上的投影，并说明该交线是什么曲线。",
 "solution": r"交线为方程组 $\begin{cases}x^2+y^2=1\\ z=2x\end{cases}$。投影到 $xy$ 平面:消去 $z$ 得 $x^2+y^2=1$ 且 $-1\le x\le1$——投影是 $xy$ 平面内的单位圆周。交线本身是圆柱面 $x^2+y^2=1$ 被平面 $z=2x$ 截出的截线,位于该平面内,是椭圆。轴长分析:参数化 $(\cos t,\sin t,2\cos t)$,在平面 $z=2x$ 内取正交基 $e_1=(0,1,0)$ 与 $e_2=\frac{(1,0,2)}{\sqrt5}$(均垂直于法向 $(2,0,-1)$ 且互相正交),则交线坐标为 $(\sin t,\sqrt5\cos t)$,即 $\eta^2+\frac{\xi^2}{5}=1$:沿 $y$ 方向($e_1$)为短轴,半轴长 $1$,全长 $2$;沿 $(1,0,2)$ 方向($e_2$)为长轴,半轴长 $\sqrt5$,全长 $2\sqrt5$。",
 "answer": r"交线:$\begin{cases}x^2+y^2=1\\ z=2x\end{cases}$;$xy$ 平面投影为单位圆周;交线为平面 $z=2x$ 内的椭圆(短半轴 $1$ 沿 $y$ 方向,长半轴 $\sqrt5$ 沿 $(1,0,2)$ 方向)。",
 "method": "平面截线(柱面与斜平面)",
 "difficulty": "中等",
 "variant_kind": "平面截线:斜平面截柱面的交线与投影分析",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "圆柱面 $x^2+y^2=1$",
   "斜平面 $z=2x$(半透明)",
   "交线椭圆(高亮,平面内)",
   "$xy$ 平面上的投影圆(虚线高亮)"
  ],
  "steps": [
   "第一步:画出圆柱面与斜平面。",
   "第二步:标出两者的交线,说明其位于斜平面内。",
   "第三步:高亮交线为椭圆(圆被斜截)。",
   "第四步:消去 $z$ 得投影圆,在 $xy$ 平面画出。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c19-04", "category": "解析几何", "sub_category": "二次曲面",
 "concept": "柱面与方程的空间意义", "concept_id": "C19",
 "parent_training_ids": ["geom-024"],
 "problem": r"判断下列方程在空间直角坐标系中表示曲线还是曲面，并说明理由:(1) $x^2+y^2=1$;(2) $\begin{cases}x^2+y^2=1\\ z=0\end{cases}$;(3) $x+y+z=1$;(4) $\begin{cases}x^2+y^2=1\\ z=x\end{cases}$。",
 "solution": r"(1) 曲面:一个方程只约束一个自由度,留下两个自由度($z$ 可任取),是母线平行 $z$ 轴的圆柱面。(2) 曲线:两个方程联立,自由度为 $3-2=1$,是 $xy$ 平面内的单位圆周。(3) 曲面:一个方程,是平面。(4) 曲线:两个独立方程联立(平面 $z=x$ 截圆柱面),是空间中的椭圆。一般地:空间维数为 $3$,一个独立方程给出一张曲面(维数 $2$),两个独立方程联立一般给出一条曲线(维数 $1$),即图形维数 $=$ $3$ $-$ 独立方程数。",
 "answer": r"(1) 曲面(圆柱面);(2) 曲线(圆周);(3) 曲面(平面);(4) 曲线(椭圆);理由:方程个数与自由度(3 减方程数)。",
 "method": "曲线与曲面方程辨析(自由度计数)",
 "difficulty": "中等",
 "variant_kind": "辨析:方程个数与图形维数的对应关系",
 "scene_spec": {
  "objects": [
   "四个并排示意图:(1) 圆柱面、(2) 圆周、(3) 平面、(4) 椭圆曲线",
   "每个图下方标注方程与「曲面/曲线」标签",
   "板书:自由度计数「维数=3−独立方程数」",
   "高亮框:分类结果"
  ],
  "steps": [
   "第一步:依次画出四个方程的图形。",
   "第二步:对每个图形标注曲面或曲线。",
   "第三步:引入自由度计数规则。",
   "第四步:用规则解释四个例子。",
   "第五步:高亮分类结果汇总。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c19-05", "category": "解析几何", "sub_category": "二次曲面",
 "concept": "柱面与方程的空间意义", "concept_id": "C19",
 "parent_training_ids": ["geom-024"],
 "problem": r"证明:若曲面方程 $F(x,y,z)=0$ 不含变量 $z$(即 $F(x,y)=0$),则它表示母线平行于 $z$ 轴的柱面;并说明如何识别母线沿一般方向的柱面(以 $(x-z)^2+(y-z)^2=1$ 为例)。",
 "solution": r"设 $(x_0,y_0)$ 满足 $F(x_0,y_0)=0$。对任意 $t$,点 $(x_0,y_0,t)$ 也满足 $F(x_0,y_0)=0$($F$ 不含 $z$),故过 $(x_0,y_0,0)$ 且平行于 $z$ 轴的整条直线都在曲面上;反之曲面上任一点 $(x,y,z)$ 的 $(x,y)$ 满足 $F(x,y)=0$,其所在的沿 $z$ 方向直线由准线点 $(x,y,0)$ 给出。故曲面是母线平行于 $z$ 轴的柱面(准线为 $xy$ 平面内曲线 $F(x,y)=0$)。一般方向:对方向 $v=(v_1,v_2,v_3)$($v_3\neq0$)的柱面,作变量替换 $u=x-\frac{v_1}{v_3}z$,$w=y-\frac{v_2}{v_3}z$($u,w$ 沿母线方向不变:方向导数 $\nabla_{(v_1,v_2,v_3)}(u)=v_1-\frac{v_1}{v_3}v_3=0$),若方程可写成 $G(u,w)=0$,则是母线沿 $v$ 的柱面。例:$(x-z)^2+(y-z)^2=1$ 中 $v=(1,1,1)$,$u=x-z$,$w=y-z$,方程即 $u^2+w^2=1$,故是母线沿 $(1,1,1)$ 的圆柱面。",
 "answer": r"证明见解法(沿 $z$ 方向的整条直线在曲面上);一般方向用 $u=x-\frac{v_1}{v_3}z$,$w=y-\frac{v_2}{v_3}z$ 的替换识别。",
 "method": "柱面判定证明+一般方向识别",
 "difficulty": "进阶",
 "variant_kind": "证明型:缺变量方程是柱面的严格证明与一般方向柱面的识别方法",
 "scene_spec": {
  "objects": [
   "三维示意图:曲线 $F(x,y)=0$ 沿 $z$ 方向平移扫出柱面的动画",
   "板书:任意 $t$,$(x_0,y_0,t)$ 满足方程的论证",
   "板书:变量替换 $u=x-\\frac{v_1}{v_3}z$ 的方向不变性",
   "高亮框:$(x-z)^2+(y-z)^2=1$ 即 $u^2+w^2=1$",
   "标签「母线方向=替换方向」"
  ],
  "steps": [
   "第一步:动画展示准线沿 $z$ 轴平移扫出柱面。",
   "第二步:论证沿 $z$ 的整条直线都在曲面上。",
   "第三步:引入一般方向的变量替换。",
   "第四步:验证替换沿母线方向不变。",
   "第五步:以斜圆柱面为例展示识别方法,完成证明。"
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
