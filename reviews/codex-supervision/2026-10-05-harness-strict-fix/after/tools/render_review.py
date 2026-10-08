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
     padding-bottom: 5pt; page-break-after: avoid; }
h2 { font-size: 14pt; border-left: 5pt solid #1f4e79; background: #eef3f9;
     padding: 4pt 8pt; color: #16365c; page-break-after: avoid; }
h3 { font-size: 11.5pt; color: #16365c; border-bottom: 1pt solid #c9d8e8;
     padding-bottom: 2pt; margin-top: 14pt; page-break-after: avoid; }
h3 code { background: none; }
p { margin: 4pt 0; }
p:has(> strong:only-child) { page-break-after: avoid; break-after: avoid-page; }
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
.math { display: inline-block; max-width: 100%; vertical-align: middle; }
mjx-container[jax="SVG"] { max-width: 100%; }
mjx-container[jax="SVG"] > svg { max-width: 100%; height: auto; }
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
    import tempfile
    with tempfile.TemporaryDirectory(prefix='edge-headless-',ignore_cleanup_errors=True) as profile:
        return subprocess.run([EDGE,'--headless=new','--disable-gpu','--no-first-run',
            '--disable-extensions','--allow-file-access-from-files','--user-data-dir='+profile]+args,
            capture_output=True,timeout=timeout,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))

sys.path.insert(0,str(ROOT/'tools'))
from review_guard import verify_dom, validate_pdf


def checked_dom(html_path,expected_inline,expected_display):
    cp=run_edge(['--dump-dom','--virtual-time-budget=240000',html_path.resolve().as_uri()])
    dom=cp.stdout.decode('utf-8','strict')
    verify_dom(dom,expected_inline,expected_display)
    return dom


def check_render(html_path):
    from review_guard import MathDom
    source=MathDom(); source.feed(html_path.read_text(encoding='utf-8'))
    inline=sum(w['kind']=='inline' for w in source.wrappers); display=len(source.wrappers)-inline
    dom=checked_dom(html_path,inline,display)
    return verify_dom(dom,inline,display)


def main(argv):
    import uuid,hashlib,json,tempfile
    ap=argparse.ArgumentParser()
    ap.add_argument('md',type=Path); ap.add_argument('--out-dir',type=Path,default=ROOT/'outputs/review')
    ap.add_argument('--check',action='store_true'); ap.add_argument('--skip-pdf',action='store_true')
    args=ap.parse_args(argv)
    try:
        source=args.md.resolve().read_bytes(); md=source.decode('utf-8-sig'); tokens=protect_math(md)[1]
        inline=sum(not display for _,display in tokens); display=len(tokens)-inline
        args.out_dir.mkdir(parents=True,exist_ok=True)
        html_path=args.out_dir/f'{args.md.stem}.html'; static_path=args.out_dir/f'{args.md.stem}.static.html'
        pdf_path=args.out_dir/f'{args.md.stem}.pdf'; receipt=args.out_dir/f'{args.md.stem}.render.json'
        if any(p.exists() for p in (html_path,static_path,pdf_path,receipt)): raise ValueError('output exists: use a new directory/version')
        with html_path.open('x',encoding='utf-8',newline='\n') as f: f.write(build_html(md,args.md.stem+' 审阅稿'))
        print(f'HTML → {html_path}')
        dom=checked_dom(html_path,inline,display) if args.check or not args.skip_pdf else None
        if dom is None: return 0  # HTML only, no validation or PDF claim.
        print(f'[check] verified inline={inline}, display={display}')
        if args.skip_pdf: return 0
        static=re.sub(r'<script\b[^>]*>.*?</script>','',dom,flags=re.S|re.I)
        with static_path.open('x',encoding='utf-8',newline='\n') as f: f.write(static)
        last=''
        for attempt in (1,2):
            # 本机 Edge 无头打印拒绝写 D: 盘目标(实测),先在 C: 临时目录打印再拷贝
            fresh=Path(tempfile.gettempdir())/f'.{args.md.stem}-{uuid.uuid4().hex}.pdf'
            try:
                if attempt==1:
                    cp=run_edge([f'--print-to-pdf={fresh}','--no-pdf-header-footer','--virtual-time-budget=1000',static_path.resolve().as_uri()],timeout=60)
                    backend='edge-cli'
                else:
                    from edge_print import print_static_to_pdf
                    print_static_to_pdf(static_path,fresh,EDGE,inline,display)
                    cp=subprocess.CompletedProcess([],0,b'',b'');backend='edge-cdp-stream'
                pages=validate_pdf(fresh)
                with pdf_path.open('xb') as f: f.write(fresh.read_bytes())
                payload={'renderer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'guard_sha256':hashlib.sha256((ROOT/'tools/review_guard.py').read_bytes()).hexdigest(),'source_md_sha256':hashlib.sha256(source).hexdigest(),'static_html_sha256':hashlib.sha256(static_path.read_bytes()).hexdigest(),
                    'pdf_sha256':hashlib.sha256(pdf_path.read_bytes()).hexdigest(),'formula_count':len(tokens),'pages':pages,
                    'print_returncode':cp.returncode,'fresh_target':fresh.name,'backend':backend}
                with receipt.open('x',encoding='utf-8',newline='\n') as f: f.write(json.dumps(payload,ensure_ascii=False,indent=2)+'\n')
                print(f'PDF → {pdf_path} ({pages} pages)'); return 0
            except (OSError,ValueError,subprocess.SubprocessError) as exc: last=str(exc)
            finally:
                if fresh.exists(): fresh.unlink()
        raise ValueError('no validated new PDF: '+last)
    except (OSError,ValueError,UnicodeError,subprocess.SubprocessError) as exc:
        print('[FAIL] '+str(exc)); return 1


if __name__=='__main__': sys.exit(main(sys.argv[1:]))
