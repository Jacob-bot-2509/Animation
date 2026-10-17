"""render_templates 修复候选 v1(独立候选,未修改现役 tools/render_templates.py)。

按 Codex 修复报告(2026-10-17-real-root-handler-review FIX_REPORT 878/881 节)
的候选验收条件实现:
- 步骤完整(去 [:28])、全部步骤(去 [:5]);
- 长内容分页:页面映射 + 每步覆盖证明,不缩字冒充可读;
- 题干/答案完整混排(文本+公式保持原顺序),不拿公式段替代全文;
- 混排处理转义 $、未配对 $ 显式失败、换行、中文 Text 与 MathTex 分体;
- 小数→分数仅在接受"已核验为精确有理数"标记时转换,否则保留原样;
- 固定几何不做通用声明:几何模板必须记录级绑定(候选不改此点)。

范围:纯逻辑与代码生成候选;不渲染、不加载 Manim、不动现役模板与资产证据。
"""
from __future__ import annotations

import re
from fractions import Fraction


class TemplateError(ValueError):
    """模板显式失败:不悄悄删段/吞错。"""


def split_mixed(text: str) -> list[tuple[str, str]]:
    """把含 $...$ 的文本切成有序段 [('text'|'math', 内容)]。

    - '\\$' 是字面美元符,留在文本段;
    - 未配对的 $ 显式抛 TemplateError(不吞);
    - 文本中的换行按行切段;
    - 空文本段丢弃(空数学段保留为空串数学,交给调用方决定)。
    """
    if not isinstance(text, str):
        raise TemplateError("non_string_input")
    out: list[tuple[str, str]] = []
    buf: list[str] = []
    i = 0
    n = len(text)
    in_math = False
    math_buf: list[str] = []

    def flush_text():
        nonlocal buf
        if buf:
            joined = "".join(buf)
            for line in joined.split("\n"):
                if line.strip():
                    out.append(("text", line))
            buf = []

    while i < n:
        ch = text[i]
        if ch == "\\" and i + 1 < n and text[i + 1] == "$":
            (math_buf if in_math else buf).append("$")
            i += 2
            continue
        if ch == "$":
            if in_math:
                out.append(("math", "".join(math_buf)))
                math_buf = []
                in_math = False
            else:
                flush_text()
                in_math = True
            i += 1
            continue
        (math_buf if in_math else buf).append(ch)
        i += 1
    if in_math:
        raise TemplateError("unmatched_dollar")
    flush_text()
    if not out:
        raise TemplateError("empty_after_split")
    return out


def estimate_height(lines: list[list[tuple[str, str]]], font_size: int = 22,
                    line_gap: float = 0.6) -> float:
    """纯启发式高度估计(仅分页用,非渲染验收)。每条线按字号+行距。"""
    return len(lines) * (font_size / 64 + line_gap)


def paginate(step_indexes: list[int], per_page_lines: int,
             lines_per_step: dict[int, int]) -> list[list[int]]:
    """把步骤分页;返回每页的步骤索引列表(可重复跨页)。

    coverage 合同:每个 step_index 至少出现在一页;调用方据此出具覆盖证明。
    """
    pages: list[list[int]] = []
    current: list[int] = []
    budget = per_page_lines
    for idx in step_indexes:
        need = lines_per_step.get(idx, 1)
        if budget < need and current:
            pages.append(current)
            current = []
            budget = per_page_lines
        if need > per_page_lines:
            # 单步超一页:该步独占多页(每页记同一步)
            while need > 0:
                pages.append([idx])
                need -= per_page_lines
            continue
        current.append(idx)
        budget -= need
    if current:
        pages.append(current)
    return pages


def coverage_ok(step_indexes: list[int], pages: list[list[int]]) -> bool:
    """覆盖证明:每步至少出现于一页,页内无重复、页间顺序不倒退。"""
    seen: set[int] = set()
    for p in pages:
        if len(p) != len(set(p)):
            return False
        seen |= set(p)
    if set(step_indexes) - seen:
        return False
    last = -1
    for p in pages:
        for idx in p:
            if idx < last:
                return False
            last = idx
    return True


def exact_fraction_text(dec_str: str, verified_exact: bool) -> str:
    """小数→分数显示。仅在 verified_exact=True(经逐条核实为精确有理数)时转换;
    否则返回原串(不盲目转换,保留原始日志/帧/测量值)。"""
    if not verified_exact:
        return dec_str
    s = dec_str.strip()
    if not re.fullmatch(r"-?\d+\.\d+", s):
        raise TemplateError(f"not_decimal_literal:{dec_str!r}")
    f = Fraction(s)
    if f.denominator == 1:
        return str(f.numerator)
    sign = "-" if f.numerator < 0 else ""
    num, den = abs(f.numerator), f.denominator
    return f"{sign}\\frac{{{num}}}{{{den}}}"


def _code_for_line(segments: list[tuple[str, str]], var: str,
                   font_size: int) -> list[str]:
    """生成一行混排代码:Text/MathTex 交替,arrange(RIGHT),返回行列表。"""
    parts = []
    exprs = []
    for kind, content in segments:
        if kind == "text":
            exprs.append(f"Text({content!r}, font='Microsoft YaHei', font_size={font_size})")
        else:
            exprs.append(f"MathTex({content!r})")
    joined = ",\n                ".join(exprs)
    return [
        f"        {var} = VGroup({joined}).arrange(RIGHT, buff=0.15)"
    ]


def steps_block_v2(steps: list[str], font_size: int = 22,
                   per_page_lines: int = 5) -> tuple[str, list[list[int]]]:
    """生成分页混排步骤块;返回 (代码文本, 页面映射)。

    不截断、不限五步;每步先 split_mixed(未配对 $ 显式失败)。
    """
    lines_per_step: dict[int, int] = {}
    mixed_steps: dict[int, list[tuple[str, str]]] = {}
    for i, step in enumerate(steps):
        segs = split_mixed(step)
        mixed_steps[i] = segs
        text_lines = sum(1 for k, _ in segs if k == "text")
        lines_per_step[i] = max(1, text_lines)
    pages = paginate(list(range(len(steps))), per_page_lines, lines_per_step)
    assert coverage_ok(list(range(len(steps))), pages), "coverage contract violated"
    code: list[str] = []
    for pi, page in enumerate(pages):
        g = f"page{pi}"
        code.append(f"        {g} = VGroup()")
        for li, idx in enumerate(page):
            segs = mixed_steps[idx]
            for kind, content in segs:
                if kind == "text":
                    code.append(f"        {g}.add(Text({content!r}, "
                                f"font='Microsoft YaHei', font_size={font_size}))")
                else:
                    code.append(f"        {g}.add(MathTex({content!r}))")
        code.append(f"        {g}.arrange(DOWN, buff=0.25).shift(DOWN * 0.5)")
        code.append(f"        self.play(FadeIn({g}))")
        if pi < len(pages) - 1:
            code.append(f"        self.play(FadeOut({g}))")
        code.append("        self.wait(0.15)")
    return "\n".join(code) + "\n", pages


def title_block_v2(problem: str) -> str:
    """题干完整混排标题(不再只取公式段);未配对 $ 显式失败。"""
    segs = split_mixed(problem)
    parts = []
    for kind, content in segs:
        if kind == "text":
            parts.append(f"Text({content!r}, font='Microsoft YaHei', font_size=24)")
        else:
            parts.append(f"MathTex({content!r})")
    return (
        "        title = VGroup(" + ",\n                ".join(parts) + ")\n"
        "        title.arrange(RIGHT, buff=0.15).scale_to_fit_width("
        "config.frame_width - 1.2).to_edge(UP)\n"
        "        self.play(Write(title))\n"
    )


def answer_block_v2(answer: str) -> str:
    """答案完整混排;无公式段也用 Text 显示(不再静默 wait)。"""
    segs = split_mixed(answer)
    parts = []
    for kind, content in segs:
        if kind == "text":
            parts.append(f"Text({content!r}, font='Microsoft YaHei', font_size=24)")
        else:
            parts.append(f"MathTex({content!r})")
    return (
        "        ans = VGroup(" + ",\n                ".join(parts) + ")\n"
        "        ans.arrange(RIGHT, buff=0.15).scale_to_fit_width("
        "config.frame_width - 2).to_edge(DOWN)\n"
        "        self.play(FadeIn(ans))\n"
        "        self.wait(0.6)\n"
    )
