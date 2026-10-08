"""数据集审阅稿渲染:MD(LaTeX) → HTML(MathJax 保护) → PDF(headless Edge)。

用法:python tools/render_review.py <md文件> [--out-dir outputs/review] [--check]
- $...$ 数学片段在 markdown 渲染前替换为占位符,渲染后再注入(避免
  markdown-it 把公式内 _、* 误当强调符);
- MathJax v3 tex-svg 经 jsdelivr CDN 加载,Edge 打印用 virtual-time-budget
  等待排版完成;
- --check:渲染后 dump DOM,统计残留的 $ 与 MathJax 错误标记(供自查)。
"""
from __future__ import annotations

import argparse
import html as html_module
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

MATHJAX_CDN = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"
# 本地渲染器(阻塞加载,避免 CDN 异步竞态导致打印时公式未排版)
MATHJAX_LOCAL = ROOT / "tools" / "assets" / "mathjax-tex-svg.js"

CSS = """
@page { size: A4; margin: 16mm 14mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: "Microsoft YaHei", "微软雅黑", "Segoe UI", sans-serif;
       font-size: 10pt; line-height: 1.62; color: #1a1a1a; margin: 0; }
h1 { font-size: 19pt; border-bottom: 2.4pt solid #1f4e79; color: #1f4e79;
     padding-bottom: 5pt; }
h2 { font-size: 14pt; border-left: 5pt solid #1f4e79; background: #eef3f9;
     padding: 4pt 8pt; color: #16365c; page-break-after: avoid; }
h3 { font-size: 11.5pt; color: #16365c; border-bottom: 1pt solid #c9d8e8;
     padding-bottom: 2pt; margin-top: 14pt; page-break-after: avoid; }
h3 code { background: none; }
p { margin: 4pt 0; }
strong { color: #14324f; }
blockquote { background: #f5f7fa; border-left: 3pt solid #9db8d2;
             padding: 5pt 9pt; margin: 6pt 0; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0; }
th, td { border: 0.6pt solid #9db8d2; padding: 3.5pt 6pt; text-align: left; }
th { background: #1f4e79; color: #fff; }
code { font-family: Consolas, "Courier New", monospace; font-size: 9pt;
       background: #f0f2f5; padding: 0 2pt; }
hr { border: none; border-top: 1pt solid #dbe4ee; margin: 10pt 0; }
.math-block { text-align: center; margin: 6pt 0; }
"""


def protect_math(text: str) -> tuple[str, list[tuple[str, bool]]]:
    """把 $$..$$ 与 $..$ 片段替换为占位符。

    返回(处理后文本, 片段列表);片段为 (内容, 是否行间公式)。
    定界符在 restore 时重新加上——MathJax 靠 $ 定界符发现公式。
    """
    tokens: list[tuple[str, bool]] = []

    def repl_display(m: re.Match) -> str:
        tokens.append((m.group(1), True))
        return f"@@MATH{len(tokens) - 1}@@"

    def repl_inline(m: re.Match) -> str:
        tokens.append((m.group(1), False))
        return f"@@MATH{len(tokens) - 1}@@"

    # 先保护 $$..$$(跨行),再保护 $..$(单行)
    text = re.sub(r"\$\$(.+?)\$\$", repl_display, text, flags=re.S)
    text = re.sub(r"\$([^$\n]+?)\$", repl_inline, text)
    return text, tokens


def _texify(tok: str) -> str:
    """数学文本中的裸 < > 转 TeX 宏(带空格终止,防与后随字母连写成新命令)。

    & 是 LaTeX 矩阵/分段环境的合法列分隔符,必须原样保留;
    源码中不存在 &xxx; 形式的 HTML 实体序列,原样输出安全。
    """
    return tok.replace("<", r"\lt ").replace(">", r"\gt ")


def restore_math(rendered: str, tokens: list[tuple[str, bool]]) -> str:
    for i, (tok, display) in enumerate(tokens):
        math = _texify(tok)
        if display:
            span = f'<div class="math-block">$${math}$$</div>'
        else:
            span = f'<span class="math">${math}$</span>'
        rendered = rendered.replace(f"@@MATH{i}@@", span)
    return rendered


def build_html(md_text: str, title: str) -> str:
    from markdown_it import MarkdownIt  # noqa: PLC0415

    protected, tokens = protect_math(md_text)
    md = MarkdownIt("commonmark", {"html": True})
    md.enable("table")
    body = md.render(protected)
    body = restore_math(body, tokens)
    # 本地阻塞脚本 + 默认排版完成后在 <title> 写入完成标记(供 check 校验)
    mathjax_cfg = (
        "<script>window.MathJax={tex:{inlineMath:[['$','$']],"
        "displayMath:[['$$','$$']]},svg:{fontCache:'global'},"
        "options:{enableMenu:false},"
        "startup:{ready:function(){MathJax.startup.defaultReady();"
        "MathJax.startup.promise.then(function(){"
        "document.title='MJDONE';});}}};</script>"
    )
    src = MATHJAX_LOCAL.as_uri() if MATHJAX_LOCAL.exists() else MATHJAX_CDN
    return (f"<!DOCTYPE html><html lang='zh'><head><meta charset='utf-8'>"
            f"<title>{html_module.escape(title)}</title>"
            f"<style>{CSS}</style>{mathjax_cfg}"
            f"<script src='{src}'></script>"
            f"</head><body>{body}</body></html>")


def run_edge(args: list[str], timeout: int = 240) -> subprocess.CompletedProcess:
    import tempfile  # noqa: PLC0415
    profile = Path(tempfile.mkdtemp(prefix="edge-headless-"))
    return subprocess.run(
        [EDGE, "--headless=new", "--disable-gpu", "--no-first-run",
         "--allow-file-access-from-files",
         "--user-data-dir=" + str(profile)] + args,
        capture_output=True, timeout=timeout)


def _no_style(dom: str) -> str:
    return re.sub(r"<style\b[^>]*>.*?</style>", "", dom, flags=re.S | re.I)


def check_render(html_path: Path) -> tuple[int, int, int]:
    """dump DOM 检查:未排版公式数、已排版数与 MathJax 错误节点数。"""
    r = run_edge(["--dump-dom", "--virtual-time-budget=240000",
                  html_path.resolve().as_uri()])
    dom = r.stdout.decode("utf-8", "replace") + r.stderr.decode("utf-8", "replace")
    body = _no_style(dom)
    spans = re.findall(r'<span class="math">(.*?)</span>', body, re.S)
    rendered = sum(1 for s in spans if "<mjx-container" in s)
    unrendered = len(spans) - rendered
    done = "MJDONE" in dom
    errors = (body.count('data-mjx-error') + body.count("<mjx-merror")
              + body.count('data-mml-node="merror"'))
    print(f"[check-diag] rc={r.returncode} dom_len={len(dom)} "
          f"raw_spans={dom.count('class=\"math\"')} MJDONE={done} "
          f"errors={errors}")
    return unrendered, rendered, errors


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("md", type=Path)
    ap.add_argument("--out-dir", type=Path, default=ROOT / "outputs" / "review")
    ap.add_argument("--check", action="store_true",
                    help="渲染后 dump DOM 自查公式残留")
    ap.add_argument("--skip-pdf", action="store_true", help="只生成 HTML")
    args = ap.parse_args(argv)

    md_path = args.md.resolve()
    if not md_path.exists():
        print(f"[FAIL] 找不到 {md_path}")
        return 1
    md_text = md_path.read_text(encoding="utf-8")
    tokens = protect_math(md_text)[1]
    expected_inline = sum(1 for _, disp in tokens if not disp)
    expected_display = sum(1 for _, disp in tokens if disp)
    title = f"{md_path.stem} 审阅稿"
    args.out_dir.mkdir(parents=True, exist_ok=True)

    html_path = args.out_dir / f"{md_path.stem}.html"
    html_path.write_text(build_html(md_text, title), encoding="utf-8")
    print(f"HTML → {html_path} 期望 inline={expected_inline} "
          f"display={expected_display}")

    # 唯一新 PDF 目标:已存在则拒绝(不允许旧文件冒充新产物)
    pdf_path = args.out_dir / f"{md_path.stem}.pdf"
    if not args.skip_pdf and pdf_path.exists():
        print(f"[FAIL] PDF 目标已存在,拒绝覆盖: {pdf_path}")
        return 1

    if args.check:
        unrendered, rendered, errors = check_render(html_path)
        print(f"[check] 已排版 {rendered} 条,未排版 {unrendered} 条,"
              f"错误节点 {errors} 个")
        if unrendered or errors:
            print("[FAIL] 存在未排版公式或 MathJax 错误(check 不通过)")
            return 2
    if args.skip_pdf:
        return 0
    # 两段式:先 dump-dom 等 MathJax 排版完成,保存静态 HTML(去掉脚本),
    # 再对静态页打印(避免打印阶段重新运行脚本的竞态)。
    dom_r = run_edge(["--dump-dom", "--virtual-time-budget=240000",
                      html_path.resolve().as_uri()])
    dom = dom_r.stdout.decode("utf-8", "replace")
    tm = re.search(r"<title>(.*?)</title>", dom, re.S)
    if tm is None or html_module.unescape(tm.group(1)).strip() != "MJDONE":
        print("[FAIL] 真实 title 未达到 MJDONE,拒绝打印")
        return 1
    dom_body = _no_style(dom)
    inline_ok = sum(1 for s in re.findall(
        r'<span class="math">(.*?)</span>', dom_body, re.S)
        if "<mjx-container" in s)
    display_ok = sum(1 for s in re.findall(
        r'<div class="math-block">(.*?)</div>', dom_body, re.S)
        if "<mjx-container" in s)
    dom_errors = (dom_body.count('data-mjx-error') + dom_body.count("<mjx-merror")
                  + dom_body.count('data-mml-node="merror"')
                  + dom_body.count("Undefined control sequence"))
    if (inline_ok != expected_inline or display_ok != expected_display
            or dom_errors):
        print(f"[FAIL] 排版不完整或存在错误: inline={inline_ok}/{expected_inline} "
              f"display={display_ok}/{expected_display} errors={dom_errors}")
        return 2
    static = re.sub(r"<script\b[^>]*>.*?</script>", "", dom,
                    flags=re.S | re.I)
    static_path = args.out_dir / f"{md_path.stem}.static.html"
    static_path.write_text(static, encoding="utf-8", newline="\n")
    r = None
    for attempt in (1, 2):
        r = run_edge([f"--print-to-pdf={pdf_path}",
                      "--virtual-time-budget=120000",
                      static_path.resolve().as_uri()])
        if pdf_path.exists() and pdf_path.stat().st_size > 0:
            break
    if (not pdf_path.exists() or pdf_path.stat().st_size == 0):
        print(f"[FAIL] PDF 生成失败 rc={r.returncode} static={static_path.exists()} "
              f"{r.stderr.decode('utf-8', 'replace')[:200]}")
        return 1
    data = pdf_path.read_bytes()
    if data[:4] != b"%PDF" or b"%%EOF" not in data[-2048:]:
        print(f"[FAIL] PDF 结构校验失败(头/尾标记缺失)")
        return 1
    print(f"PDF → {pdf_path} ({pdf_path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
