"""模板修复候选纯逻辑自测(真实断言;不导入 Manim、不渲染)。"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from render_templates_v2_candidate import (  # noqa: E402
    TemplateError, answer_block_v2, coverage_ok, estimate_height,
    exact_fraction_text, paginate, split_mixed, steps_block_v2, title_block_v2)


def main() -> int:
    rows: list[tuple[str, bool, str]] = []

    def t(name, ok, detail=""):
        rows.append((name, ok, detail))

    # split_mixed:正常混排
    segs = split_mixed("第一步：抛物线 $y=x^2$ 与直线 $y=x+2$")
    t("split-mixed-order", [k for k, _ in segs] == ["text", "math", "text", "math"]
      and segs[1][1] == "y=x^2", str(segs))
    # 转义美元符
    segs = split_mixed("价格 \\$5 与 $x$")
    t("split-escaped-dollar", ("text", "价格 $5 与 ") in [(k, c) for k, c in segs]
      and ("math", "x") in [(k, c) for k, c in segs], str(segs))
    # 未配对 $ 显式失败
    try:
        split_mixed("第一步 $x")
        t("split-unmatched-raises", False, "no exception")
    except TemplateError:
        t("split-unmatched-raises", True, "")
    # 换行切段
    segs = split_mixed("第一行\n第二行")
    t("split-newline", [c for k, c in segs if k == "text"] == ["第一行", "第二行"], str(segs))
    # 空输入显式失败
    try:
        split_mixed("   ")
        t("split-empty-raises", False, "no exception")
    except TemplateError:
        t("split-empty-raises", True, "")

    # 分页覆盖:10 步、每步 2 行、每页 5 行 → 每页 2 步、5 页;每步至少一页
    lines = {i: 2 for i in range(10)}
    pages = paginate(list(range(10)), per_page_lines=5, lines_per_step=lines)
    t("paginate-all-covered", coverage_ok(list(range(10)), pages), str(pages))
    t("paginate-page-count", len(pages) == 5, str(len(pages)))
    # 单步超页:一步 12 行、每页 5 → 独占 3 页
    pages = paginate([0], per_page_lines=5, lines_per_step={0: 12})
    t("paginate-oversized-step", pages == [[0], [0], [0]], str(pages))
    # 覆盖证明:漏步 → False
    t("coverage-missing-step", not coverage_ok([0, 1, 2], [[0], [1]]), "")
    # 覆盖证明:页内重复 → False
    t("coverage-dup-in-page", not coverage_ok([0], [[0, 0]]), "")
    # 覆盖证明:顺序倒退 → False
    t("coverage-order-regression", not coverage_ok([0, 1], [[1], [0]]), "")

    # 精确分数:已核验才转换
    t("frac-verified", exact_fraction_text("0.5", True) == "\\frac{1}{2}",
      exact_fraction_text("0.5", True))
    t("frac-unverified-kept", exact_fraction_text("0.333", False) == "0.333", "")
    t("frac-negative", exact_fraction_text("-0.25", True) == "-\\frac{1}{4}",
      exact_fraction_text("-0.25", True))
    try:
        exact_fraction_text("x", True)
        t("frac-nondecimal-raises", False, "no exception")
    except TemplateError:
        t("frac-nondecimal-raises", True, "")

    # 步骤块:完整内容(不再 28 字符截断)、全部步骤(不再 5 步)
    steps = ["第一步：绘制直角坐标系，用蓝色绘制抛物线 $y=x^2$",
             "第二步：标出两曲线的交点 $(-1,1)$ 和 $(2,4)$"] + \
            [f"第{i}步：继续演示" for i in range(3, 8)]
    code, pages = steps_block_v2(steps)
    t("steps-all-six", "第7步：继续演示" in code, "")
    # 无截断:混排后内容分成 Text/MathTex 多段,逐段核对完整性
    t("steps-no-28-truncation", all(x in code for x in
        ["标出两曲线的交点", "(-1,1)", "(2,4)"]), "")
    t("steps-mathtex-mixed", "MathTex(" in code and "Text(" in code, "")

    # 题干/答案:完整混排,纯文字也显示
    tc = title_block_v2("计算 $y=x^2$ 与 $y=x+2$ 围成区域面积")
    t("title-mixed", "MathTex('y=x^2')" in tc and "围成区域面积" in tc, "")
    ac = answer_block_v2("9/2")
    t("answer-text-fallback", "Text('9/2'" in ac, "")

    fails = 0
    for name, ok, detail in rows:
        print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")
        if not ok:
            fails += 1
    print(f"scenarios={len(rows)} fails={fails}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
