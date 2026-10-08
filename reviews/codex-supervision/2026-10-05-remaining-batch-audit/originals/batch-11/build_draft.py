"""batch-11 生成器:三个单条考点各 5 题
(C20 二次曲面分类与截面 / C22 直纹性与母线 / C23 等距变换)。
全部数学结论由作者逐题手工验算(见 DRAFT_REPORT.md 核算说明);
起草过程未读 eval/test 题文或答案作提示;凡有理数一律分数。
"""
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "draft.jsonl"

DATA = [
# ===================== C20 二次曲面分类与截面 =====================
{
 "id": "draft-c20-01", "category": "解析几何", "sub_category": "二次曲面",
 "concept": "二次曲面分类与截面", "concept_id": "C20",
 "parent_training_ids": ["geom-025", "geom-026"],
 "problem": r"指出方程 $z=x^2-y^2$ 表示的二次曲面类型，并分别说明其与平面 $z=0$、$z=1$、$z=-1$ 的交线形状。",
 "solution": r"类型:双曲抛物面(马鞍面)。截面 $z=0$:$x^2-y^2=0$,即 $y=\pm x$,是两条相交直线。截面 $z=1$:$x^2-y^2=1$,是双曲线(实轴沿 $x$ 方向)。截面 $z=-1$:$y^2-x^2=1$,也是双曲线(实轴沿 $y$ 方向)。",
 "answer": r"双曲抛物面;$z=0$ 截面为两条相交直线 $y=\pm x$,$z=1$ 与 $z=-1$ 截面为实轴方向不同的双曲线。",
 "method": "曲面判型+水平截面分析",
 "difficulty": "基础",
 "variant_kind": "曲面类型变化:马鞍面的水平截面分支(与椭圆抛物面父题不同)",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "马鞍面 $z=x^2-y^2$(半透明)",
   "三个水平截面平面 $z=0,1,-1$(半透明)",
   "截线高亮:两条相交直线、两条双曲线",
   "标签「双曲抛物面」"
  ],
  "steps": [
   "第一步:画出马鞍面,标注方程。",
   "第二步:展示 $z=0$ 截面,得两相交直线。",
   "第三步:展示 $z=1$ 截面,得双曲线。",
   "第四步:展示 $z=-1$ 截面,得另一支双曲线。",
   "第五步:汇总截面分支与曲面类型。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c20-02", "category": "解析几何", "sub_category": "二次曲面",
 "concept": "二次曲面分类与截面", "concept_id": "C20",
 "parent_training_ids": ["geom-025", "geom-026"],
 "problem": r"用配方法判断方程 $x^2+y^2+z^2-2x-4y+1=0$ 表示什么曲面，并求其中心(球心)与半径。",
 "solution": r"配方:$(x^2-2x)+(y^2-4y)+z^2+1=0$,即 $(x-1)^2-1+(y-2)^2-4+z^2+1=0$,整理得 $(x-1)^2+(y-2)^2+z^2=4$。这是球面,球心为 $(1,2,0)$,半径为 $2$。",
 "answer": r"球面,球心 $(1,2,0)$,半径 $2$。",
 "method": "配方法(平移项判型)",
 "difficulty": "基础",
 "variant_kind": "含一次项的配方判型(平移后识别)",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "球面(半透明),球心 $(1,2,0)$ 高亮",
   "板书:配方过程 $(x-1)^2+(y-2)^2+z^2=4$",
   "半径标注(球心到球面的线段)",
   "标签「球面」"
  ],
  "steps": [
   "第一步:写出原方程,展示对 $x,y$ 的配方。",
   "第二步:整理得标准形式。",
   "第三步:识别为球面,标出球心。",
   "第四步:画出球面与半径线段。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c20-03", "category": "解析几何", "sub_category": "二次曲面",
 "concept": "二次曲面分类与截面", "concept_id": "C20",
 "parent_training_ids": ["geom-025", "geom-026"],
 "problem": r"讨论方程 $x^2+y^2-z^2=a$ 随参数 $a$ 变化所表示的曲面类型。",
 "solution": r"当 $a>0$ 时,化为 $\frac{x^2}{a}+\frac{y^2}{a}-\frac{z^2}{a}=1$,是单叶双曲面。当 $a=0$ 时,$x^2+y^2-z^2=0$,即 $z^2=x^2+y^2$,是圆锥面(退化情形)。当 $a<0$ 时,令 $b=-a>0$,$\frac{z^2}{b}-\frac{x^2}{b}-\frac{y^2}{b}=1$,是双叶双曲面。",
 "answer": r"$a>0$:单叶双曲面;$a=0$:圆锥面(退化);$a<0$:双叶双曲面。",
 "method": "含参判型(退化分支)",
 "difficulty": "中等",
 "variant_kind": "参数退化:同一方程族的三种曲面类型与退化边界 a=0",
 "scene_spec": {
  "objects": [
   "三个并排三维图:单叶双曲面、圆锥面、双叶双曲面",
   "数轴:参数 $a$ 的三个区间与退化点 $a=0$",
   "动画:曲面随 $a$ 连续变化(在 $a=0$ 处收缩为圆锥面)",
   "高亮框:三分支结论"
  ],
  "steps": [
   "第一步:写出方程族,分 $a>0,a=0,a<0$ 讨论。",
   "第二步:展示 $a>0$ 的单叶双曲面。",
   "第三步:展示 $a=0$ 的退化圆锥面,动画过渡。",
   "第四步:展示 $a<0$ 的双叶双曲面。",
   "第五步:数轴汇总三分支,高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c20-04", "category": "解析几何", "sub_category": "二次曲面",
 "concept": "二次曲面分类与截面", "concept_id": "C20",
 "parent_training_ids": ["geom-025", "geom-026"],
 "problem": r"讨论椭球面 $\frac{x^2}{4}+\frac{y^2}{9}+z^2=1$ 与平面 $z=k$ 的交线:对不同的 $k$ 说明交线是椭圆、一个点还是空集。",
 "solution": r"代入 $z=k$:$\frac{x^2}{4}+\frac{y^2}{9}=1-k^2$。当 $|k|<1$ 时,右端为正,交线是椭圆,半轴为 $2\sqrt{1-k^2}$ 与 $3\sqrt{1-k^2}$。当 $|k|=1$ 时,右端为 $0$,交线退化为一个点 $(0,0,\pm1)$(与椭球相切的截面)。当 $|k|>1$ 时,右端为负,无实解,交线为空集。",
 "answer": r"$|k|<1$:椭圆(半轴 $2\sqrt{1-k^2}$、$3\sqrt{1-k^2}$);$|k|=1$:点 $(0,0,\pm1)$;$|k|>1$:空集。",
 "method": "截面分支分析(椭圆/点/空集)",
 "difficulty": "中等",
 "variant_kind": "截面分支:切截、割截与不相交三种截线的完整讨论",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "椭球面(半透明)",
   "动画:截面平面 $z=k$ 上下滑动",
   "截线高亮:椭圆(收缩)、点、消失",
   "数轴:$k$ 的三个区间标注"
  ],
  "steps": [
   "第一步:画出椭球面,写出截面方程。",
   "第二步:动画滑动截面,展示 $|k|<1$ 的椭圆并收缩。",
   "第三步:在 $k=\\pm1$ 处展示退化为点。",
   "第四步:继续滑动展示 $|k|>1$ 时无交线。",
   "第五步:数轴汇总三个分支。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c20-05", "category": "解析几何", "sub_category": "二次曲面",
 "concept": "二次曲面分类与截面", "concept_id": "C20",
 "parent_training_ids": ["geom-025", "geom-026"],
 "problem": r"用正交变换(旋转)判断方程 $x^2+2xy+y^2+z=0$ 表示的曲面类型。",
 "solution": r"交叉项部分 $x^2+2xy+y^2=(x+y)^2$。作正交变换 $u=\frac{x+y}{\sqrt2}$,$v=\frac{-x+y}{\sqrt2}$,$w=z$(变换矩阵 $\begin{pmatrix}\frac1{\sqrt2}&\frac1{\sqrt2}&0\\-\frac1{\sqrt2}&\frac1{\sqrt2}&0\\0&0&1\end{pmatrix}$ 为正交矩阵且行列式为 $1$,是绕 $z$ 轴的真旋转),则 $x^2+2xy+y^2=2u^2$,方程化为 $2u^2+w=0$,即 $w=-2u^2$。这是母线沿 $v$ 方向的抛物柱面。",
 "answer": r"抛物柱面(旋转变换后 $w=-2u^2$,母线沿 $v=\frac{-x+y}{\sqrt2}$ 方向)。",
 "method": "正交变换消交叉项",
 "difficulty": "进阶",
 "variant_kind": "交叉项处理:正交变换旋转后判型(抛物柱面)",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "原曲面与旋转后的抛物柱面对照",
   "板书:$x^2+2xy+y^2=(x+y)^2$ 与正交变换矩阵",
   "板书:$2u^2+w=0$ 的简化形式",
   "标签「抛物柱面」"
  ],
  "steps": [
   "第一步:写出交叉项并配方为 $(x+y)^2$。",
   "第二步:构造正交变换矩阵。",
   "第三步:在新坐标下化简方程。",
   "第四步:对照展示旋转前后的曲面。",
   "第五步:识别为抛物柱面,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
# ===================== C22 直纹性与母线 =====================
{
 "id": "draft-c22-01", "category": "解析几何", "sub_category": "二次曲面",
 "concept": "直纹性与母线", "concept_id": "C22",
 "parent_training_ids": ["geom-028"],
 "problem": r"验证单叶双曲面 $x^2+y^2-z^2=1$ 是直纹面，并写出其两族直母线。",
 "solution": r"由 $(x+z)(x-z)=(1+y)(1-y)$ 可得两族直线。第一族:$\begin{cases}x+z=\lambda(1+y)\\ \lambda(x-z)=1-y\end{cases}$($\lambda$ 取扩充实数,含 $\lambda=\infty$ 对应的极限直线 $y=-1,x=z$);第二族:$\begin{cases}x+z=\mu(1-y)\\ \mu(x-z)=1+y\end{cases}$($\mu$ 取扩充实数,含 $\mu=\infty$ 对应的极限直线 $y=1,x=z$)。验证第一族:直线上任一点满足 $(x+z)(x-z)=\lambda(1+y)\cdot\frac{1-y}{\lambda}=1-y^2$,即 $x^2-z^2=1-y^2$,故 $x^2+y^2-z^2=1$,整条直线在曲面上。第二族同理。补充极限直线后,曲面上每一点恰有每族各一条母线经过。",
 "answer": r"两族母线:$\begin{cases}x+z=\lambda(1+y)\\ \lambda(x-z)=1-y\end{cases}$ 与 $\begin{cases}x+z=\mu(1-y)\\ \mu(x-z)=1+y\end{cases}$($\lambda,\mu$ 取扩充实数,含 $\infty$ 对应极限直线 $y=\mp1,x=z$);单叶双曲面是直纹面。",
 "method": "因式分解构造母线族",
 "difficulty": "基础",
 "variant_kind": "构造母线:单叶双曲面的两族直母线(因式分解法)",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "单叶双曲面(半透明)",
   "第一族母线(若干条直线,一色)与第二族母线(另一色)叠加显示",
   "板书:因式分解 $(x+z)(x-z)=(1+y)(1-y)$",
   "标签「直纹面:每点两条母线」"
  ],
  "steps": [
   "第一步:写出曲面方程并因式分解。",
   "第二步:由分解构造第一族直线,验证整条在曲面上。",
   "第三步:构造第二族直线。",
   "第四步:在曲面上画出两族母线。",
   "第五步:说明每点恰有两条母线,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c22-02", "category": "解析几何", "sub_category": "二次曲面",
 "concept": "直纹性与母线", "concept_id": "C22",
 "parent_training_ids": ["geom-028"],
 "problem": r"证明球面 $x^2+y^2+z^2=1$ 不是直纹面。",
 "solution": r"任一直线与球面至多有两个交点:设直线 $l(t)=p+td$($d\neq0$),代入球面方程得 $(p_1+td_1)^2+(p_2+td_2)^2+(p_3+td_3)^2=1$,即 $|d|^2t^2+2(p\cdot d)t+(|p|^2-1)=0$。因二次项系数 $|d|^2>0$,这是真正的二次方程,至多有两个实根;该二次多项式不可能恒为零(二次项系数非零)。故球面不含任何整条直线,即球面上不存在母线,球面不是直纹面。",
 "answer": r"球面不是直纹面:任一直线与球面至多交于两点,球面不含整条直线。",
 "method": "交点个数论证(反证)",
 "difficulty": "基础",
 "variant_kind": "证否:球面非直纹的二次方程交点论证",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "球面(半透明)与若干条穿过或相切的直线",
   "动画:直线穿过球面至多两交点,相切时一个交点",
   "板书:代入得二次方程 $|d|^2t^2+2(p\\cdot d)t+|p|^2-1=0$",
   "红色标签「非直纹面」"
  ],
  "steps": [
   "第一步:设任意直线参数式,代入球面方程。",
   "第二步:展示所得二次方程至多两个实根。",
   "第三步:动画展示直线与球面至多两交点。",
   "第四步:说明球面不含整条直线。",
   "第五步:结论:球面不是直纹面。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c22-03", "category": "解析几何", "sub_category": "二次曲面",
 "concept": "直纹性与母线", "concept_id": "C22",
 "parent_training_ids": ["geom-028"],
 "problem": r"求双曲抛物面 $z=xy$ 的两族直母线，并说明过曲面上每一点恰有两条母线。",
 "solution": r"对每个实数 $t$,直线 $\{(x,t,tx)\}$ 在曲面上(因为 $z=tx=xy$ 当 $y=t$);同样 $\{(t,y,ty)\}$ 也在曲面上(当 $x=t$)。故两族母线为 $l_1(t):\{(x,t,tx)\}$ 与 $l_2(t):\{(t,y,ty)\}$。过点 $(a,b,ab)$:取 $t=b$ 得第一族母线,取 $t=a$ 得第二族母线。完备性:设过 $(a,b,ab)$、方向为 $(u,v,w)$ 的直线在曲面上,则 $ab+tw=(a+tu)(b+tv)$ 对一切 $t$ 成立,即 $tw=(av+bu)t+uvt^2$,比较系数得 $uv=0$ 且 $w=av+bu$:$u=0$ 时是第二族($x\equiv a$),$v=0$ 时是第一族($y\equiv b$)。故过该点恰有两条母线。",
 "answer": r"两族母线:$\{(x,t,tx)\}$ 与 $\{(t,y,ty)\}$($t$ 为参数);过每点恰有两条母线(完备性由比较系数 $uv=0$ 保证)。",
 "method": "参数构造母线族",
 "difficulty": "中等",
 "variant_kind": "曲面类型变化:马鞍面的两族母线构造",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "马鞍面 $z=xy$(半透明)",
   "两族母线(不同颜色)叠加显示",
   "曲面上一点与过它的两条母线高亮",
   "标签「双曲抛物面是直纹面」"
  ],
  "steps": [
   "第一步:画出马鞍面。",
   "第二步:构造第一族直线并验证在曲面上。",
   "第三步:构造第二族直线。",
   "第四步:高亮曲面上一点与过它的两条母线。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c22-04", "category": "解析几何", "sub_category": "二次曲面",
 "concept": "直纹性与母线", "concept_id": "C22",
 "parent_training_ids": ["geom-028"],
 "problem": r"判断下列曲面哪些是直纹面，并各给理由:圆柱面 $x^2+y^2=1$;圆锥面 $x^2+y^2-z^2=0$;椭球面 $\frac{x^2}{4}+\frac{y^2}{9}+z^2=1$;抛物柱面 $y=x^2$。",
 "solution": r"圆柱面:直纹面——对每个 $(x_0,y_0)$ 在圆 $x^2+y^2=1$ 上,直线 $\{(x_0,y_0,t)\}$ 整条在曲面上(母线平行于 $z$ 轴)。圆锥面:直纹面——对每个满足 $u^2+v^2-w^2=0$ 的方向 $(u,v,w)$,过原点的直线 $\{(tu,tv,tw)\}$ 满足 $t^2(u^2+v^2-w^2)=0$,整条在曲面上(所有母线都经过顶点,互不平行)。椭球面:不是直纹面——与球面同理(有界曲面不含整条直线,任一直线与椭球面至多两交点)。抛物柱面 $y=x^2$:直纹面——对每个 $x_0$,直线 $\{(x_0,x_0^2,t)\}$ 整条在曲面上($x=x_0,y=x_0^2$ 满足 $y=x^2$,母线平行于 $z$ 轴)。",
 "answer": r"圆柱面、圆锥面、抛物柱面是直纹面(圆柱面/抛物柱面含整族平行直线;圆锥面的母线均过顶点);椭球面不是直纹面(有界曲面与直线至多两交点)。",
 "method": "分类判定(各曲面含直线与否)",
 "difficulty": "中等",
 "variant_kind": "分类任务:四类曲面的直纹性判定与理由",
 "scene_spec": {
  "objects": [
   "四个并排三维图:圆柱面、圆锥面、椭球面、抛物柱面",
   "直纹面上画出母线族,椭球面上红色叉号",
   "标签:各自「直纹面/非直纹面」判定",
   "高亮框:分类结果"
  ],
  "steps": [
   "第一步:依次展示四个曲面。",
   "第二步:在圆柱面上画母线族,说明整条在曲面上。",
   "第三步:在圆锥面、抛物柱面上同样处理。",
   "第四步:对椭球面说明直线至多两交点,红色标记非直纹。",
   "第五步:高亮分类结果。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c22-05", "category": "解析几何", "sub_category": "二次曲面",
 "concept": "直纹性与母线", "concept_id": "C22",
 "parent_training_ids": ["geom-028"],
 "problem": r"证明双叶双曲面 $x^2+y^2-z^2=-1$ 不是直纹面。",
 "solution": r"反证:设存在直线 $l(t)=p+td$ 整条在曲面上,则对一切 $t$ 有 $(p_1+td_1)^2+(p_2+td_2)^2-(p_3+td_3)^2+1=0$。这是 $t$ 的二次多项式恒为零,故三个系数全为零:常数项 $p_1^2+p_2^2-p_3^2+1=0$,一次项 $p_1d_1+p_2d_2-p_3d_3=0$,二次项 $d_1^2+d_2^2-d_3^2=0$。由第三式 $|d_3|=\sqrt{d_1^2+d_2^2}$;由第一式 $p_3^2=p_1^2+p_2^2+1$,即 $|p_3|>\sqrt{p_1^2+p_2^2}$。但由第二式与柯西不等式,$|p_3d_3|=|p_1d_1+p_2d_2|\le\sqrt{p_1^2+p_2^2}\sqrt{d_1^2+d_2^2}<\sqrt{p_3^2}\sqrt{d_3^2}=|p_3d_3|$,矛盾。故不存在整条直线在双叶双曲面上,它不是直纹面。",
 "answer": r"双叶双曲面不是直纹面:假设整条直线在曲面上,多项式恒零给出三个系数方程,由柯西不等式导出 $|p_3d_3|<|p_3d_3|$ 的矛盾(证明见解法)。",
 "method": "多项式系数分析+柯西不等式(反证)",
 "difficulty": "进阶",
 "variant_kind": "证明型:非直纹面的严格反证证明(多项式恒零+不等式矛盾)",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "双叶双曲面(两叶,半透明)",
   "动画:任意直线穿入两叶之间,无法整条落在曲面上",
   "板书:三个系数方程(常数/一次/二次项为零)",
   "板书:柯西不等式的矛盾推导"
  ],
  "steps": [
   "第一步:画出双叶双曲面,假设存在整条直线在其上。",
   "第二步:代入参数式,得多项式恒零的三个系数方程。",
   "第三步:由二次项与常数项得出 $|d_3|$ 与 $|p_3|$ 的关系。",
   "第四步:用柯西不等式导出矛盾。",
   "第五步:结论:双叶双曲面非直纹面。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
# ===================== C23 等距变换 =====================
{
 "id": "draft-c23-01", "category": "解析几何", "sub_category": "空间变换",
 "concept": "等距变换", "concept_id": "C23",
 "parent_training_ids": ["geom-029"],
 "problem": r"求等距变换 $T(x)=Ax+b$ 的逆变换，其中 $A=\begin{pmatrix}0&1&0\\-1&0&0\\0&0&1\end{pmatrix}$，$b=(1,2,3)$。",
 "solution": r"$A$ 为正交矩阵,逆变换为 $T^{-1}(x)=A^{\mathsf T}x-A^{\mathsf T}b$。$A^{\mathsf T}=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix}$,$A^{\mathsf T}b=(0-2,\ 1+0,\ 0+3)=(-2,1,3)$。故 $T^{-1}(x)=A^{\mathsf T}x-(-2,1,3)=A^{\mathsf T}x+(2,-1,-3)$。验证:$T(T^{-1}(x))=A(A^{\mathsf T}x-A^{\mathsf T}b)+b=x-b+b=x$ ✓。",
 "answer": r"$T^{-1}(x)=A^{\mathsf T}x+(2,-1,-3)$,即 $T^{-1}(x,y,z)=(-y+2,\,x-1,\,z-3)$。",
 "method": "正交矩阵的逆变换公式",
 "difficulty": "基础",
 "variant_kind": "逆变换:等距变换的逆公式推导与验证",
 "scene_spec": {
  "objects": [
   "三维示意图:点 $x$ 经 $T$ 映到 $Tx$ 再经 $T^{-1}$ 返回(往返箭头动画)",
   "板书:$T^{-1}(x)=A^{\\mathsf T}x-A^{\\mathsf T}b$ 的推导",
   "板书:$A^{\\mathsf T}b=(-2,1,3)$ 的计算",
   "高亮框:$T^{-1}(x,y,z)=(-y+2,x-1,z-3)$",
   "标签「等距变换可逆」"
  ],
  "steps": [
   "第一步:写出逆变换的一般公式。",
   "第二步:计算 $A^{\\mathsf T}$ 与 $A^{\\mathsf T}b$。",
   "第三步:写出逆变换的坐标形式。",
   "第四步:动画展示点往返回到自身。",
   "第五步:验证 $T\\circ T^{-1}=I$,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c23-02", "category": "解析几何", "sub_category": "空间变换",
 "concept": "等距变换", "concept_id": "C23",
 "parent_training_ids": ["geom-029"],
 "problem": r"证明:若 $A$ 为正交矩阵,则等距变换 $T(x)=Ax+b$ 保持任意两点间的距离,即 $\|T(x)-T(y)\|=\|x-y\|$。",
 "solution": r"$\|T(x)-T(y)\|=\|(Ax+b)-(Ay+b)\|=\|A(x-y)\|$。由正交矩阵的性质 $\|Au\|^2=(Au)^{\mathsf T}(Au)=u^{\mathsf T}A^{\mathsf T}Au=u^{\mathsf T}u=\|u\|^2$,故 $\|A(x-y)\|=\|x-y\|$,距离保持不变。",
 "answer": r"证明见解法(核心:$\|Au\|^2=u^{\mathsf T}A^{\mathsf T}Au=u^{\mathsf T}u$)。",
 "method": "正交矩阵保范数证明",
 "difficulty": "基础",
 "variant_kind": "保持量:等距变换保距离的证明",
 "scene_spec": {
  "objects": [
   "三维示意图:两点与其像,连线长度标注不变",
   "板书:$\\|A(x-y)\\|^2=(x-y)^{\\mathsf T}A^{\\mathsf T}A(x-y)$ 的推导",
   "板书:$A^{\\mathsf T}A=I$ 的代入",
   "高亮框:$\\|T(x)-T(y)\\|=\\|x-y\\|$",
   "标签「等距变换保距离」"
  ],
  "steps": [
   "第一步:画出两点及其在 $T$ 下的像,标注连线。",
   "第二步:写出范数平方并展开。",
   "第三步:用 $A^{\\mathsf T}A=I$ 化简。",
   "第四步:得距离不变。",
   "第五步:高亮结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c23-03", "category": "解析几何", "sub_category": "空间变换",
 "concept": "等距变换", "concept_id": "C23",
 "parent_training_ids": ["geom-029"],
 "problem": r"求旋转矩阵 $A=\begin{pmatrix}0&0&1\\0&1&0\\-1&0&0\end{pmatrix}$ 的旋转轴与旋转角。",
 "solution": r"旋转轴是特征值 $1$ 的特征向量方向:解 $(A-I)v=0$,即 $\begin{pmatrix}-1&0&1\\0&0&0\\-1&0&-1\end{pmatrix}v=0$:由第一行 $-v_1+v_3=0$ 与第三行 $-v_1-v_3=0$ 得 $v_1=v_3=0$,$v_2$ 任意,故轴为 $y$ 轴(方向 $(0,1,0)$)。旋转角:由迹公式 $\mathrm{tr}(A)=1+2\cos\theta$,这里 $\mathrm{tr}(A)=0+1+0=1$,故 $\cos\theta=0$,$\theta=\pm90^\circ$;再由 $A(1,0,0)=(0,0,-1)$,按右手定则绕 $y$ 轴正方向旋转 $90^\circ$ 恰把 $x$ 轴正方向转到 $z$ 轴负方向,故 $\theta=90^\circ$。",
 "answer": r"旋转轴为 $y$ 轴(方向 $(0,1,0)$),旋转角 $90^\circ$(绕 $y$ 轴正向)。",
 "method": "特征值定轴+迹定角",
 "difficulty": "中等",
 "variant_kind": "旋转轴/角求解:由旋转矩阵反求轴与角(迹公式+方向核对)",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "旋转轴 $y$ 轴高亮(虚线)",
   "动画:坐标架绕 $y$ 轴旋转 $90^\\circ$($x$ 轴转向 $-z$)",
   "板书:特征方程 $(A-I)v=0$ 的求解",
   "板书:$\\mathrm{tr}(A)=1+2\\cos\\theta$ 与方向核对"
  ],
  "steps": [
   "第一步:解特征方程求不动方向,得 $y$ 轴。",
   "第二步:用迹公式求旋转角大小。",
   "第三步:动画展示坐标架旋转过程。",
   "第四步:由 $x$ 轴像的方向定旋转方向。",
   "第五步:汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c23-04", "category": "解析几何", "sub_category": "空间变换",
 "concept": "等距变换", "concept_id": "C23",
 "parent_training_ids": ["geom-029"],
 "problem": r"求关于平面 $\pi:x+y+z=0$ 的反射矩阵，并验证平面上的点不动、法向量反向。",
 "solution": r"平面单位法向量 $n=\frac{1}{\sqrt3}(1,1,1)$。反射矩阵 $S=I-2nn^{\mathsf T}=I-\frac{2}{3}\begin{pmatrix}1&1&1\\1&1&1\\1&1&1\end{pmatrix}=\begin{pmatrix}\frac13&-\frac23&-\frac23\\-\frac23&\frac13&-\frac23\\-\frac23&-\frac23&\frac13\end{pmatrix}$。验证:对平面上点 $(x,y,z)$($x+y+z=0$),$S(x,y,z)=(x,y,z)-\frac{2}{3}(x+y+z)(1,1,1)=(x,y,z)$,不动 ✓;对法向量 $(1,1,1)$,$S(1,1,1)=(1,1,1)-\frac23\cdot3\cdot(1,1,1)=-(1,1,1)$,反向 ✓。另 $\det S=-1$,为反射的特征。",
 "answer": r"$S=\begin{pmatrix}\frac13&-\frac23&-\frac23\\-\frac23&\frac13&-\frac23\\-\frac23&-\frac23&\frac13\end{pmatrix}$;平面点不动、法向量反向,已验证。",
 "method": "Householder 反射矩阵构造",
 "difficulty": "中等",
 "variant_kind": "反射:过原点平面的反射矩阵构造与双验证",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "平面 $x+y+z=0$(半透明)与法向量",
   "动画:点关于平面的镜像反射",
   "板书:$S=I-2nn^{\\mathsf T}$ 的构造",
   "验证板书:平面点不动与法向反向"
  ],
  "steps": [
   "第一步:画出平面与单位法向量。",
   "第二步:构造反射矩阵 $I-2nn^{\\mathsf T}$。",
   "第三步:动画展示反射的镜像效果。",
   "第四步:验证平面上的点不动。",
   "第五步:验证法向量反向,汇总结论。"
  ]
 },
 "source": "self-authored", "license": "Internal-Research-Use-Only",
 "draft_status": "draft-v1-待用户审阅",
},
{
 "id": "draft-c23-05", "category": "解析几何", "sub_category": "空间变换",
 "concept": "等距变换", "concept_id": "C23",
 "parent_training_ids": ["geom-029"],
 "problem": r"把等距变换 $T(x)=Ax+b$ 分解为绕某轴的旋转与沿该轴平移的复合(螺旋运动),其中 $A=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix}$(绕 $z$ 轴旋转 $90^\circ$),$b=(1,2,3)$。",
 "solution": r"旋转轴方向 $v=(0,0,1)$。把 $b$ 分解为沿轴分量与垂直分量:$b_\parallel=(b\cdot v)v=(0,0,3)$,$b_\perp=b-b_\parallel=(1,2,0)$。在 $v^\perp$ 上解 $(I-A)p=b_\perp$:$I-A=\begin{pmatrix}1&1&0\\-1&1&0\\0&0&0\end{pmatrix}$,方程 $p_1+p_2=1$,$-p_1+p_2=2$,解得 $p_1=-\frac12,p_2=\frac32$;取 $p=(-\frac12,\frac32,0)$。则 $T(x)=A(x-p)+p+b_\parallel$:验证右端 $=Ax+(I-A)p+(0,0,3)=Ax+(1,2,0)+(0,0,3)=Ax+b=T(x)$ ✓。故 $T$ 是「绕过点 $p$、平行于 $z$ 轴的直线旋转 $90^\circ$」与「沿 $z$ 轴平移 $(0,0,3)$」的复合(螺旋运动)。",
 "answer": r"$T=$ 绕过 $p=(-\frac12,\frac32,0)$ 且平行于 $z$ 轴的直线旋转 $90^\circ$,复合沿 $z$ 轴平移 $(0,0,3)$。",
 "method": "螺旋运动分解(轴向/垂直分量分离)",
 "difficulty": "进阶",
 "variant_kind": "分解型:等距变换的螺旋运动分解与验证",
 "scene_spec": {
  "objects": [
   "三维坐标系(带刻度)",
   "旋转轴(过 $p$ 平行 $z$ 轴,虚线)",
   "动画:先绕轴旋转 $90^\\circ$ 再沿轴平移的复合运动",
   "板书:$b$ 的轴向/垂直分解与 $(I-A)p=b_\\perp$ 的求解",
   "高亮框:螺旋分解式 $T(x)=A(x-p)+p+b_\\parallel$"
  ],
  "steps": [
   "第一步:确定旋转轴方向并分解平移向量。",
   "第二步:解 $(I-A)p=b_\\perp$ 求轴上参考点。",
   "第三步:写出螺旋分解式。",
   "第四步:动画展示旋转+沿轴平移的复合效果。",
   "第五步:验证复合恰为 $T$,高亮结论。"
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
