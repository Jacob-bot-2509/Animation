# -*- coding: utf-8 -*-
"""Rewrite scene_spec (objects/steps only) for record idx=226 draft-c43-03.
Verifies all arithmetic against the solution before dumping."""
import json
import io

SRC = r"D:/Animation-Model-Training/reviews/2026-10-06-scene-standard-sweep/chunks/chunk-17.json"
OUT = r"D:/code/.bridge-poll/record_226_rewritten.json"

with io.open(SRC, encoding="utf-8") as f:
    data = json.load(f)

rec = None
for r in data["records"]:
    if r.get("idx") == 226 and r.get("id") == "draft-c43-03":
        rec = r
        break
assert rec is not None

# ---------- arithmetic self-checks ----------
G = [[2, 0, "2/3"], [0, "2/3", 0], ["2/3", 0, "2/5"]]
C = [["9/8", 0, "-15/8"], [0, "3/2", 0], ["-15/8", 0, "45/8"]]

from fractions import Fraction as F

Gf = [[F("2"), F("0"), F(2, 3)], [F("0"), F(2, 3), F("0")], [F(2, 3), F("0"), F(2, 5)]]
Cf = [[F(9, 8), F(0), F(-15, 8)], [F(0), F(3, 2), F(0)], [F(-15, 8), F(0), F(45, 8)]]
CG = [[sum(Cf[i][k] * Gf[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
assert CG == [[F(1), F(0), F(0)], [F(0), F(1), F(0)], [F(0), F(0), F(1)]], CG

# elimination: row ops
A = [
    [F(2), F(0), F(2, 3), F(1), F(0), F(0)],
    [F(0), F(2, 3), F(0), F(0), F(1), F(0)],
    [F(2, 3), F(0), F(2, 5), F(0), F(0), F(1)],
]
A[0] = [x * F(1, 2) for x in A[0]]
assert A[0] == [F(1), F(0), F(1, 3), F(1, 2), F(0), F(0)], A[0]
A[2] = [a - F(2, 3) * b for a, b in zip(A[2], A[0])]
assert A[2] == [F(0), F(0), F(8, 45), F(-1, 3), F(0), F(1)], A[2]
A[1] = [x * F(3, 2) for x in A[1]]
assert A[1] == [F(0), F(1), F(0), F(0), F(3, 2), F(0)], A[1]
A[2] = [x * F(45, 8) for x in A[2]]
assert A[2] == [F(0), F(0), F(1), F(-15, 8), F(0), F(45, 8)], A[2]
A[0] = [a - F(1, 3) * b for a, b in zip(A[0], A[2])]
assert A[0] == [F(1), F(0), F(0), F(9, 8), F(0), F(-15, 8)], A[0]

# nine pairings by integration: moments int x^k = 2/(k+1) even, 0 odd
mom = {0: F(2), 1: F(0), 2: F(2, 3), 3: F(0), 4: F(2, 5)}
gs = {
    "g0": [F(9, 8), F(0), F(-15, 8)],
    "g1": [F(0), F(3, 2), F(0)],
    "g2": [F(-15, 8), F(0), F(45, 8)],
}
table = []
for name in ["g0", "g1", "g2"]:
    row = []
    for j in range(3):
        v = sum(c * mom[k + j] for k, c in enumerate(gs[name]))
        row.append(v)
    table.append(row)
assert table == [[F(1), F(0), F(0)], [F(0), F(1), F(0)], [F(0), F(0), F(1)]], table

print("all arithmetic checks passed")

# ---------- new objects ----------
objects = [
    r"题目卡片:在$V=\mathbb R[x]_{\le2}$中取基$1,x,x^2$。求三个多项式$g_0,g_1,g_2$,使$f_i(p)=\int_{-1}^1g_i(x)p(x)\,dx$为此基的对偶泛函,并证明九个配对值。",
    r"积分基础公式卡片:五个基础矩积分逐步计算——$\int_{-1}^1x^0dx=[x]_{-1}^1=2$,$\int_{-1}^1x^1dx=[\frac{x^2}{2}]_{-1}^1=0$,$\int_{-1}^1x^2dx=[\frac{x^3}{3}]_{-1}^1=2/3$,$\int_{-1}^1x^3dx=[\frac{x^4}{4}]_{-1}^1=0$,$\int_{-1}^1x^4dx=[\frac{x^5}{5}]_{-1}^1=2/5$。",
    r"关键点高亮框(第一步):奇次幂$x,x^3$在对称区间$[-1,1]$上积分为0;偶次幂公式$\int_{-1}^1x^kdx=\frac{2}{k+1}$。",
    r"矩阵对象(Gram矩阵G):$G=\begin{pmatrix}2&0&2/3\\0&2/3&0\\2/3&0&2/5\end{pmatrix}$,逐格高亮$G_{ij}=\int_{-1}^1x^{i+j}dx$的填入过程,标注对称性$G_{ij}=G_{ji}$。",
    r"系数矩阵C占位与定义卡片:第$i$行为$g_i$的系数$(c_{i0},c_{i1},c_{i2})$,即$g_i(x)=c_{i0}\cdot1+c_{i1}x+c_{i2}x^2$,行对应$g_i$、列对应基元$1,x,x^2$。",
    r"行×列展开公式卡片:$(CG)_{ij}=c_{i0}G_{0j}+c_{i1}G_{1j}+c_{i2}G_{2j}$,高亮「$C$的第$i$行×$G$的第$j$列=各分量乘积之和」。",
    r"关键点高亮框(第二步):配对条件$f_i(x^j)=\delta_{ij}$($i,j=0,1,2$)等价于矩阵方程$CG=I$;$G$对称可逆,故$C=G^{-1}$。",
    r"增广矩阵对象$(G\,|\,I)$:$\left(\begin{array}{ccc|ccc}2&0&2/3&1&0&0\\0&2/3&0&0&1&0\\2/3&0&2/5&0&0&1\end{array}\right)$,左块为$G$、右块为单位阵$I$。",
    r"行变换标注箭头(五个):$R_1\gets\frac12R_1$;$R_3\gets R_3-\frac23R_1$;$R_2\gets\frac32R_2$;$R_3\gets\frac{45}{8}R_3$;$R_1\gets R_1-\frac13R_3$;每个标签旁附该行运算的逐项算术展开。",
    r"中间矩阵卡片(四个):每次行变换后的增广矩阵状态,依次为①$\left(\begin{array}{ccc|ccc}1&0&1/3&1/2&0&0\\0&2/3&0&0&1&0\\2/3&0&2/5&0&0&1\end{array}\right)$;②$\left(\begin{array}{ccc|ccc}1&0&1/3&1/2&0&0\\0&2/3&0&0&1&0\\0&0&8/45&-1/3&0&1\end{array}\right)$;③$\left(\begin{array}{ccc|ccc}1&0&1/3&1/2&0&0\\0&1&0&0&3/2&0\\0&0&8/45&-1/3&0&1\end{array}\right)$;④$\left(\begin{array}{ccc|ccc}1&0&1/3&1/2&0&0\\0&1&0&0&3/2&0\\0&0&1&-15/8&0&45/8\end{array}\right)$。",
    r"结果矩阵C:$C=G^{-1}=\begin{pmatrix}9/8&0&-15/8\\0&3/2&0\\-15/8&0&45/8\end{pmatrix}$,与左块化成的单位阵并排对照。",
    r"行×列乘法高亮框(CG=I核验):逐项高亮$C$的第$i$行与$G$的第$j$列,标注「第i行×第j列=各分量乘积之和」并写具体数值,如第1行×第1列:$\frac98\times2+0\times0+(-\frac{15}{8})\times\frac23=\frac94-\frac54=1$。",
    r"多项式读出卡片:按$C$的行读出$g_i$——$g_0=\frac98\cdot1+0\cdot x+(-\frac{15}{8})x^2=\frac{9-15x^2}{8}$;$g_1=0\cdot1+\frac32x+0\cdot x^2=\frac{3x}{2}$;$g_2=(-\frac{15}{8})\cdot1+0\cdot x+\frac{45}{8}x^2=\frac{-15+45x^2}{8}$。",
    r"九个配对值3×3表格:行标$g_0,g_1,g_2$、列标$1,x,x^2$,逐格填入$\int g_i x^j$的展开式与结果,最终呈现单位矩阵$\delta_{ij}$。",
    r"配对积分展开式卡片(九个):逐项展示乘积展开→逐项积分→代入化简,如$\int g_0\cdot1\,dx=\int\frac{9-15x^2}{8}dx=\frac{9\int1\,dx-15\int x^2dx}{8}=\frac{9\times2-15\times\frac23}{8}=\frac{18-10}{8}=1$。",
    r"注释文本卡片(第五步):真正的对偶元素是泛函$f_i$,多项式$g_i$是相对于内积型积分配对$\langle g,p\rangle=\int_{-1}^1gp\,dx$的表示;九个配对值$f_i(x^j)=\delta_{ij}$表明$f_0,f_1,f_2$是基$1,x,x^2$的对偶基。",
    r"结论卡片:$g_0=(9-15x^2)/8,g_1=3x/2,g_2=(-15+45x^2)/8$;$f_i(p)=\int_{-1}^1g_ip$组成对偶基。",
]

steps = [
    r"第一步:计算Gram矩阵。对$i,j=0,1,2$,$G_{ij}=\int_{-1}^1x^{i+j}\,dx$,先逐步算出五个基础矩积分(公式→代入→结果):"
    r"①$\int_{-1}^1x^0dx=\int_{-1}^11\,dx=[x]_{-1}^1=1-(-1)=2$;"
    r"②$\int_{-1}^1x^1dx=[\frac{x^2}{2}]_{-1}^1=\frac12-\frac12=0$;"
    r"③$\int_{-1}^1x^2dx=[\frac{x^3}{3}]_{-1}^1=\frac13-(-\frac13)=\frac23$;"
    r"④$\int_{-1}^1x^3dx=[\frac{x^4}{4}]_{-1}^1=\frac14-\frac14=0$;"
    r"⑤$\int_{-1}^1x^4dx=[\frac{x^5}{5}]_{-1}^1=\frac15-(-\frac15)=\frac25$。"
    r"关键点:奇次幂$x,x^3$在对称区间$[-1,1]$上积分为0;偶次幂$\int_{-1}^1x^kdx=\frac{2}{k+1}$。"
    r"再按$i+j$取值逐项填入:$G_{00}=\int x^0=2$,$G_{01}=G_{10}=\int x^1=0$,$G_{02}=G_{20}=\int x^2=2/3$,$G_{11}=\int x^2=2/3$,$G_{12}=G_{21}=\int x^3=0$,$G_{22}=\int x^4=2/5$。"
    r"得$G=\begin{pmatrix}2&0&2/3\\0&2/3&0\\2/3&0&2/5\end{pmatrix}$(关键点:$G_{ij}=G_{ji}$,矩阵对称)。",

    r"第二步:把配对条件化为矩阵方程。设$g_i(x)=c_{i0}\cdot1+c_{i1}x+c_{i2}x^2$,其系数排成矩阵$C$的第$i$行(关键点:行对应$g_i$,列对应基元$1,x,x^2$)。对每个$j=0,1,2$逐步展开:"
    r"$f_i(x^j)=\int_{-1}^1g_i(x)x^jdx=\int_{-1}^1(c_{i0}+c_{i1}x+c_{i2}x^2)x^jdx=c_{i0}\int_{-1}^1x^{0+j}dx+c_{i1}\int_{-1}^1x^{1+j}dx+c_{i2}\int_{-1}^1x^{2+j}dx=c_{i0}G_{0j}+c_{i1}G_{1j}+c_{i2}G_{2j}=(CG)_{ij}$。"
    r"关键点:上式正是「$C$的第$i$行×$G$的第$j$列=各分量乘积之和」,故配对条件$f_i(x^j)=\delta_{ij}$($i,j=0,1,2$)等价于$CG=I$;又$G$对称可逆,故$C=G^{-1}$。",

    r"第三步:解$CG=I$求$C$(消元求逆,标注每步行变换;再按行×列核验$CG=I$)。关键点:消元目标是把左块化为单位阵,右块即为$G^{-1}$。对增广矩阵$(G\,|\,I)=\left(\begin{array}{ccc|ccc}2&0&2/3&1&0&0\\0&2/3&0&0&1&0\\2/3&0&2/5&0&0&1\end{array}\right)$逐步行变换:"
    r"①$R_1\gets\frac12R_1$:第一行$(2,0,2/3)\times\frac12=(1,0,1/3)$,右端$(1,0,0)\times\frac12=(1/2,0,0)$,得$\left(\begin{array}{ccc|ccc}1&0&1/3&1/2&0&0\\0&2/3&0&0&1&0\\2/3&0&2/5&0&0&1\end{array}\right)$;"
    r"②$R_3\gets R_3-\frac23R_1$:$(\frac23,0,\frac25)-\frac23(1,0,\frac13)=(0,0,\frac25-\frac29)=(0,0,\frac{18}{45}-\frac{10}{45})=(0,0,\frac{8}{45})$,右端$(0,0,1)-\frac23(\frac12,0,0)=(-\frac13,0,1)$,得$\left(\begin{array}{ccc|ccc}1&0&1/3&1/2&0&0\\0&2/3&0&0&1&0\\0&0&8/45&-1/3&0&1\end{array}\right)$;"
    r"③$R_2\gets\frac32R_2$:$(0,\frac23,0)\times\frac32=(0,1,0)$,右端$(0,1,0)\times\frac32=(0,\frac32,0)$,得$\left(\begin{array}{ccc|ccc}1&0&1/3&1/2&0&0\\0&1&0&0&3/2&0\\0&0&8/45&-1/3&0&1\end{array}\right)$;"
    r"④$R_3\gets\frac{45}{8}R_3$:$(0,0,\frac{8}{45})\times\frac{45}{8}=(0,0,1)$,右端$(-\frac13,0,1)\times\frac{45}{8}=(-\frac{45}{24},0,\frac{45}{8})=(-\frac{15}{8},0,\frac{45}{8})$,得$\left(\begin{array}{ccc|ccc}1&0&1/3&1/2&0&0\\0&1&0&0&3/2&0\\0&0&1&-15/8&0&45/8\end{array}\right)$;"
    r"⑤$R_1\gets R_1-\frac13R_3$:左端$(1,0,\frac13)-\frac13(0,0,1)=(1,0,0)$,右端$(\frac12,0,0)-\frac13(-\frac{15}{8},0,\frac{45}{8})=(\frac12+\frac{15}{24},0,-\frac{15}{8})=(\frac{12}{24}+\frac{15}{24},0,-\frac{15}{8})=(\frac{27}{24},0,-\frac{15}{8})=(\frac98,0,-\frac{15}{8})$,得$\left(\begin{array}{ccc|ccc}1&0&0&9/8&0&-15/8\\0&1&0&0&3/2&0\\0&0&1&-15/8&0&45/8\end{array}\right)$。"
    r"故$C=G^{-1}=\begin{pmatrix}9/8&0&-15/8\\0&3/2&0\\-15/8&0&45/8\end{pmatrix}$。"
    r"乘回核验$CG=I$(逐步标明第i行×第j列=各分量乘积之和):"
    r"第1行×第1列:$\frac98\times2+0\times0+(-\frac{15}{8})\times\frac23=\frac94-\frac{30}{24}=\frac94-\frac54=1$;"
    r"第1行×第2列:$\frac98\times0+0\times\frac23+(-\frac{15}{8})\times0=0$;"
    r"第1行×第3列:$\frac98\times\frac23+0\times0+(-\frac{15}{8})\times\frac25=\frac{18}{24}-\frac{30}{40}=\frac34-\frac34=0$;"
    r"第2行×第1列:$0\times2+\frac32\times0+0\times\frac23=0$;"
    r"第2行×第2列:$0\times0+\frac32\times\frac23+0\times0=1$;"
    r"第2行×第3列:$0\times\frac23+\frac32\times0+0\times\frac25=0$;"
    r"第3行×第1列:$(-\frac{15}{8})\times2+0\times0+\frac{45}{8}\times\frac23=-\frac{15}{4}+\frac{90}{24}=-\frac{15}{4}+\frac{15}{4}=0$;"
    r"第3行×第2列:$(-\frac{15}{8})\times0+0\times\frac23+\frac{45}{8}\times0=0$;"
    r"第3行×第3列:$(-\frac{15}{8})\times\frac23+0\times0+\frac{45}{8}\times\frac25=-\frac{30}{24}+\frac{90}{40}=-\frac54+\frac94=1$。"
    r"九个结果恰为$\delta_{ij}$,$CG=I$成立。"
    r"按行读出$g_i$($C$的第$i$行=$g_i$在基$1,x,x^2$下的系数):"
    r"$g_0=\frac98\cdot1+0\cdot x+(-\frac{15}{8})x^2=\frac{9-15x^2}{8}$;"
    r"$g_1=0\cdot1+\frac32x+0\cdot x^2=\frac{3x}{2}$;"
    r"$g_2=(-\frac{15}{8})\cdot1+0\cdot x+\frac{45}{8}x^2=\frac{-15+45x^2}{8}$。",

    r"第四步:直接积分核验九个配对值$\int_{-1}^1g_i(x)x^jdx=\delta_{ij}$(逐项写出乘积展开→逐项积分→代入→化简;所需矩:$\int_{-1}^11\,dx=2$,$\int_{-1}^1x\,dx=0$,$\int_{-1}^1x^2dx=2/3$,$\int_{-1}^1x^3dx=0$,$\int_{-1}^1x^4dx=2/5$;关键点:奇次矩积分为零):"
    r"①$\int_{-1}^1g_0\cdot1\,dx=\int_{-1}^1\frac{9-15x^2}{8}dx=\frac{9\int1\,dx-15\int x^2dx}{8}=\frac{9\times2-15\times\frac23}{8}=\frac{18-10}{8}=1=\delta_{00}$;"
    r"②$\int_{-1}^1g_0\cdot x\,dx=\int_{-1}^1\frac{(9-15x^2)x}{8}dx=\frac{9\int x\,dx-15\int x^3dx}{8}=\frac{9\times0-15\times0}{8}=0=\delta_{01}$;"
    r"③$\int_{-1}^1g_0\cdot x^2dx=\int_{-1}^1\frac{(9-15x^2)x^2}{8}dx=\frac{9\int x^2dx-15\int x^4dx}{8}=\frac{9\times\frac23-15\times\frac25}{8}=\frac{6-6}{8}=0=\delta_{02}$;"
    r"④$\int_{-1}^1g_1\cdot1\,dx=\int_{-1}^1\frac{3x}{2}dx=\frac32\int x\,dx=\frac32\times0=0=\delta_{10}$;"
    r"⑤$\int_{-1}^1g_1\cdot x\,dx=\int_{-1}^1\frac{3x^2}{2}dx=\frac32\int x^2dx=\frac32\times\frac23=1=\delta_{11}$;"
    r"⑥$\int_{-1}^1g_1\cdot x^2dx=\int_{-1}^1\frac{3x^3}{2}dx=\frac32\int x^3dx=\frac32\times0=0=\delta_{12}$;"
    r"⑦$\int_{-1}^1g_2\cdot1\,dx=\int_{-1}^1\frac{-15+45x^2}{8}dx=\frac{-15\int1\,dx+45\int x^2dx}{8}=\frac{-15\times2+45\times\frac23}{8}=\frac{-30+30}{8}=0=\delta_{20}$;"
    r"⑧$\int_{-1}^1g_2\cdot x\,dx=\int_{-1}^1\frac{(-15+45x^2)x}{8}dx=\frac{-15\int x\,dx+45\int x^3dx}{8}=\frac{-15\times0+45\times0}{8}=0=\delta_{21}$;"
    r"⑨$\int_{-1}^1g_2\cdot x^2dx=\int_{-1}^1\frac{(-15+45x^2)x^2}{8}dx=\frac{-15\int x^2dx+45\int x^4dx}{8}=\frac{-15\times\frac23+45\times\frac25}{8}=\frac{-10+18}{8}=1=\delta_{22}$。"
    r"九个值排成3×3表恰为单位矩阵$I$($\delta_{ij}$),与$CG=I$一致。",

    r"第五步:结论与理解。关键点:对偶空间$V^*$中的对偶元素是泛函$f_i$($f_i(p)=\int_{-1}^1g_i(x)p(x)dx$),多项式$g_i$只是泛函相对于内积型积分配对$\langle g,p\rangle=\int_{-1}^1g(x)p(x)dx$的表示;九个配对值$f_i(x^j)=\delta_{ij}$表明$f_0,f_1,f_2$是基$1,x,x^2$的对偶基。"
    r"答案:$g_0=(9-15x^2)/8,g_1=3x/2,g_2=(-15+45x^2)/8$;$f_i(p)=\int_{-1}^1g_ip$组成对偶基。",
]

assert len(steps) == 5
for i, s in enumerate(steps, 1):
    assert s.startswith("\u7b2c" + "\u4e00\u4e8c\u4e09\u56db\u4e94"[i - 1] + "\u6b65:"), s[:10]

new_scene = {"objects": objects, "steps": steps}
assert rec["scene_spec"]["objects"] != objects or rec["scene_spec"]["steps"] != steps

out = {
    "idx": rec["idx"],
    "id": rec["id"],
    "concept_id": rec["concept_id"],
    "category": rec["category"],
    "sub_category": rec["sub_category"],
    "problem": rec["problem"],
    "solution": rec["solution"],
    "answer": rec["answer"],
    "scene_spec": new_scene,
}
assert out["problem"] == rec["problem"]
assert out["solution"] == rec["solution"]
assert out["answer"] == rec["answer"]

with io.open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=2)

# verify escaped round-trip
with io.open(OUT, encoding="utf-8") as f:
    back = json.load(f)
assert back["scene_spec"]["steps"] == steps
assert back["scene_spec"]["objects"] == objects
print("written and round-trip verified:", OUT)
print("objects:", len(objects), "steps:", len(steps))
