"""scene_spec v2 → Manim 场景模板库(渲染试点用,正常环境)。

每个模板生成独立、自包含的 Manim 场景代码(仅 import manim,不依赖项目)。
中文标签用 Text(font='Microsoft YaHei'),公式用 MathTex。
模板仅证明"spec→场景代码→媒体产物"管线可用,不代表视觉保真度。
"""
from __future__ import annotations

_PREAMBLE = (
    "from manim import *\n"
    "import numpy as np\n\n\n"
    "class PilotScene(Scene):\n"
    "    def construct(self):\n"
)


def _math_segments(text: str) -> str | None:
    """提取 $...$ 数学段并拼接(中文与标点不进 MathTex);无数学段返回 None。
    以 Python 字符串字面量安全转义；保留导数撇号与引号的数学意义。"""
    import re
    parts = re.findall(r"\$([^$]+)\$", text)
    if not parts:
        return None
    segs = []
    for p in parts:
        s = p.strip()
        if s.endswith("\\"):
            s += " "
        if s:
            segs.append(s)
    return " \\quad ".join(segs) if segs else None


def _title_block(problem: str, answer: str) -> str:
    """标题=问题公式段,超宽自动缩放;无公式段时用中文占位。"""
    # LaTeX child processes must run before Pango/Text accumulates in the
    # 2 GiB job. Prebuild the answer, display it only after the solution steps.
    answer_math = _math_segments(answer)
    prefix = (f"        answer_math = MathTex({answer_math!r}, color=YELLOW)\n"
              if answer_math is not None else "")
    math = _math_segments(problem)
    if math is not None:
        return prefix + (
            f"        title = MathTex({math!r}).scale_to_fit_width("
            f"config.frame_width - 1.2)\n"
            "        title.to_edge(UP)\n"
            "        self.play(Write(title))\n"
        )
    return prefix + (
        "        title = Text('(公式段提取失败)', font='Microsoft YaHei', "
        "font_size=24).to_edge(UP)\n"
        "        self.play(Write(title))\n"
    )


def _steps_block(steps: list[str]) -> str:
    """步骤逐条显示(中文 Text + 公式段用 MathTex 混合省略,试点保持简单)。"""
    lines = []
    for i, step in enumerate(steps[:5]):
        lines.append(
            f"        s{i} = Text({step[:28]!r}, font='Microsoft YaHei', "
            f"font_size=22).shift(DOWN * (1.2 + 0.6 * {i}))\n"
            f"        self.play(FadeIn(s{i}))\n"
            f"        self.wait(0.15)\n"
        )
    return "".join(lines)


def _answer_block(answer: str) -> str:
    math = _math_segments(answer)
    if math is None:
        return "        self.wait(0.3)\n"
    return (
        "        ans = answer_math.scale_to_fit_width("
        f"config.frame_width - 2)\n"
        "        ans.to_edge(DOWN)\n"
        "        self.play(FadeIn(ans))\n"
        "        self.wait(0.6)\n"
    )


def _scene_body(body: str) -> str:
    return _PREAMBLE + body + "\n\n\nif __name__ == '__main__':\n    pass\n"


def unit_circle(rec: dict) -> str:
    body = _title_block(rec["problem"], rec["answer"])
    body += (
        "        circle = Circle(radius=2, color=BLUE)\n"
        "        self.play(Create(circle))\n"
        "        radius = Line(ORIGIN, 2 * RIGHT, color=WHITE)\n"
        "        arc = Arc(radius=2, angle=PI / 4, color=YELLOW)\n"
        "        self.play(Create(radius), Create(arc))\n"
        "        tri = Polygon(ORIGIN, 2 * RIGHT,\n"
        "                       2 * np.array([np.cos(PI / 4), np.sin(PI / 4), 0]),\n"
        "                       color=GREEN, fill_opacity=0.15)\n"
        "        self.play(FadeIn(tri))\n"
        "        lbl = MathTex(r'\\frac{\\sin(x/2)}{x/2}\\to 1').shift(DOWN * 1.6)\n"
        "        self.play(Write(lbl))\n"
        "        self.wait(0.4)\n"
    )
    body += _steps_block(rec["scene_spec"]["steps"])
    body += _answer_block(rec["answer"])
    return _scene_body(body)


def graph_limit(rec: dict) -> str:
    body = _title_block(rec["problem"], rec["answer"])
    body += (
        "        ax = Axes(x_range=[-3, 3, 1], y_range=[-1, 3, 1],\n"
        "                  x_length=7, y_length=4).shift(DOWN * 0.6)\n"
        "        self.play(Create(ax))\n"
        "        curve = ax.plot(lambda x: np.sin(x) / x if abs(x) > 1e-6 else 1.0,\n"
        "                        x_range=[-3, 3, 0.01], color=BLUE)\n"
        "        self.play(Create(curve))\n"
        "        lim = ax.get_vertical_line(ax.c2p(0, 1), color=YELLOW)\n"
        "        dot = Dot(ax.c2p(0, 1), color=RED)\n"
        "        self.play(Create(lim), FadeIn(dot))\n"
        "        lbl = MathTex(r'x\\to 0').next_to(lim, RIGHT)\n"
        "        self.play(Write(lbl))\n"
        "        self.wait(0.4)\n"
    )
    body += _steps_block(rec["scene_spec"]["steps"])
    body += _answer_block(rec["answer"])
    return _scene_body(body)


def sequence(rec: dict) -> str:
    body = _title_block(rec["problem"], rec["answer"])
    body += (
        "        line = NumberLine(x_range=[0, 12, 1], length=9).shift(DOWN * 1.2)\n"
        "        self.play(Create(line))\n"
        "        dots = VGroup(*[Dot(line.n2p(n), color=TEAL)\n"
        "                        for n in range(1, 9)])\n"
        "        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.15))\n"
        "        lbl = MathTex(r'a_n', color=YELLOW).shift(UP * 1.5)\n"
        "        self.play(Write(lbl))\n"
        "        self.wait(0.4)\n"
    )
    body += _steps_block(rec["scene_spec"]["steps"])
    body += _answer_block(rec["answer"])
    return _scene_body(body)


def matrix(rec: dict) -> str:
    body = _title_block(rec["problem"], rec["answer"])
    body += (
        "        m = Matrix([[1, 2], [0, 1]], h_buff=0.9)\n"
        "        self.play(Write(m))\n"
        "        brace = Brace(m, DOWN)\n"
        "        lbl = MathTex(r'B^2=A').next_to(brace, DOWN)\n"
        "        self.play(GrowFromCenter(brace), FadeIn(lbl))\n"
        "        arrow = Arrow(LEFT * 3, LEFT * 1.5, color=YELLOW)\n"
        "        self.play(Create(arrow))\n"
        "        self.wait(0.4)\n"
    )
    body += _steps_block(rec["scene_spec"]["steps"])
    body += _answer_block(rec["answer"])
    return _scene_body(body)


def derivative(rec: dict) -> str:
    body = _title_block(rec["problem"], rec["answer"])
    body += (
        "        ax = Axes(x_range=[-2, 4, 1], y_range=[-2, 6, 1],\n"
        "                  x_length=7, y_length=4).shift(DOWN * 0.6)\n"
        "        self.play(Create(ax))\n"
        "        curve = ax.plot(lambda x: x ** 2, x_range=[-2, 3, 0.01], color=BLUE)\n"
        "        self.play(Create(curve))\n"
        "        p = ax.c2p(1, 1)\n"
        "        tangent = ax.plot(lambda x: 2 * x - 1, x_range=[-1, 2.2, 0.01],\n"
        "                          color=YELLOW)\n"
        "        dot = Dot(p, color=RED)\n"
        "        self.play(Create(tangent), FadeIn(dot))\n"
        "        lbl = MathTex(r\"f'(x)=2x\").next_to(p, UR)\n"
        "        self.play(Write(lbl))\n"
        "        self.wait(0.4)\n"
    )
    body += _steps_block(rec["scene_spec"]["steps"])
    body += _answer_block(rec["answer"])
    return _scene_body(body)


def geometry(rec: dict) -> str:
    body = _title_block(rec["problem"], rec["answer"])
    body += (
        "        tri = Polygon(ORIGIN + DOWN * 0.8, 2 * RIGHT + DOWN * 0.8,\n"
        "                       1.2 * UP + 0.3 * RIGHT,\n"
        "                       color=BLUE, fill_opacity=0.1)\n"
        "        self.play(Create(tri))\n"
        "        circ = Circle(radius=0.7, color=GREEN).move_to(0.8 * RIGHT)\n"
        "        self.play(Create(circ))\n"
        "        right = RightAngle(Line(tri.get_vertices()[0], tri.get_vertices()[1]),\n"
        "                           Line(tri.get_vertices()[1], tri.get_vertices()[2]),\n"
        "                           length=0.25, color=YELLOW)\n"
        "        self.play(Create(right))\n"
        "        self.wait(0.4)\n"
    )
    body += _steps_block(rec["scene_spec"]["steps"])
    body += _answer_block(rec["answer"])
    return _scene_body(body)


def statistics(rec: dict) -> str:
    body = _title_block(rec["problem"], rec["answer"])
    body += (
        "        ax = Axes(x_range=[0, 6, 1], y_range=[0, 4, 1],\n"
        "                  x_length=7, y_length=4).shift(DOWN * 0.6)\n"
        "        self.play(Create(ax))\n"
        "        bars = VGroup(*[\n"
        "            Rectangle(width=0.7, height=h, color=TEAL, fill_opacity=0.6)\n"
        "            .move_to(ax.c2p(x, 0), aligned_edge=DOWN).shift(UP * h / 2)\n"
        "            for x, h in zip([1, 2, 3, 4, 5], [1, 3, 2, 3, 1])])\n"
        "        self.play(FadeIn(bars))\n"
        "        curve = ax.plot(lambda x: 2.2 * np.exp(-((x - 2.5) ** 2) / 1.2),\n"
        "                        x_range=[0, 5.5, 0.01], color=YELLOW)\n"
        "        self.play(Create(curve))\n"
        "        self.wait(0.4)\n"
    )
    body += _steps_block(rec["scene_spec"]["steps"])
    body += _answer_block(rec["answer"])
    return _scene_body(body)


def fallback(rec: dict) -> str:
    body = _title_block(rec["problem"], rec["answer"])
    body += _steps_block(rec["scene_spec"]["steps"])
    body += _answer_block(rec["answer"])
    return _scene_body(body)


# 关键词路由(命中加权,先到先得;顺序=优先级)
_ROUTES: list[tuple[str, list[str]]] = [
    ("unit_circle", ["单位圆", "扇形", "半角", "三角恒等", "sin", "cos", "tan",
                     "正弦", "余弦"]),
    ("matrix", ["矩阵", "行列式", "特征值", "特征向量", "线性变换", "逆矩阵",
                "二次型"]),
    ("sequence", ["数列", "级数", "递推", "a_n", "a_{n", "求和", "通项"]),
    ("derivative", ["导数", "微分", "切线", "积分", "面积", "极值", "单调"]),
    ("statistics", ["概率", "统计", "分布", "期望", "方差", "随机"]),
    ("geometry", ["几何", "三角形", "四边形", "圆", "平行", "垂直", "相似"]),
    ("graph_limit", ["极限", "lim", "趋近", "逼近", "无穷"]),
]

_TEMPLATES = {
    "unit_circle": unit_circle,
    "matrix": matrix,
    "sequence": sequence,
    "derivative": derivative,
    "statistics": statistics,
    "geometry": geometry,
    "graph_limit": graph_limit,
    "fallback": fallback,
}


def route(rec: dict) -> str:
    """按 category/sub_category/problem/solution/scene_spec/function_family/
    visual_style 关键词命中加权选择模板,无命中→fallback。"""
    text = " ".join([
        str(rec.get("category", "")), str(rec.get("sub_category", "")),
        str(rec.get("problem", "")), str(rec.get("solution", "")),
        str(rec.get("function_family", "")), str(rec.get("visual_style", "")),
        str(rec.get("scene_spec", "")),
    ])
    scores = []
    for name, kws in _ROUTES:
        score = sum(1 for kw in kws if kw in text)
        scores.append((name, score))
    best = max(scores, key=lambda t: t[1])
    return best[0] if best[1] > 0 else "fallback"


def build_scene(rec: dict) -> str:
    return _TEMPLATES[route(rec)](rec)
