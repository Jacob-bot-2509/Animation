"""把修复报告 Markdown 渲染为打印友好 HTML(纯标准库,零依赖)。

只覆盖本报告用到的子集:标题/表格/列表/段落/加粗/行内代码/引用。
用法: python reports/render_repair_html.py <in.md> <out.html>
"""
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

CSS = """
@page { size: A4; margin: 18mm 15mm; }
body { font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
       color: #1a1f2b; line-height: 1.65; max-width: 190mm; margin: 0 auto; }
h1 { font-size: 1.55em; border-bottom: 3px solid #2f6fed; padding-bottom: .35em; }
h2 { font-size: 1.2em; color: #1d4ed8; margin-top: 1.6em;
     border-left: 4px solid #2f6fed; padding-left: .5em; }
table { border-collapse: collapse; width: 100%; margin: .8em 0 1.2em;
        page-break-inside: avoid; }
th, td { border: 1px solid #c9d4e3; padding: .45em .6em; font-size: .9em;
         text-align: left; vertical-align: top; }
th { background: #eef3fc; }
code { background: #f1f4f9; padding: .05em .3em; border-radius: 3px;
       font-family: Consolas, monospace; font-size: .92em; }
blockquote { color: #55627a; border-left: 3px solid #9fb3d1;
             margin: .6em 0; padding: .2em .8em; }
ul, ol { margin: .4em 0 .8em; padding-left: 1.4em; }
"""


def _inline(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    return s


def render(text: str) -> str:
    out: list[str] = ["<!DOCTYPE html><html lang=zh-CN><head><meta charset=utf-8>",
                      f"<style>{CSS}</style></head><body>"]
    in_list: str | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if line.startswith("# "):
            if in_list:
                out.append(f"</{in_list}>")
                in_list = None
            out.append(f"<h1>{_inline(line[2:])}</h1>")
        elif line.startswith("## "):
            if in_list:
                out.append(f"</{in_list}>")
                in_list = None
            out.append(f"<h2>{_inline(line[3:])}</h2>")
        elif line.startswith(">"):
            if in_list:
                out.append(f"</{in_list}>")
                in_list = None
            out.append(f"<blockquote>{_inline(line.lstrip('> '))}</blockquote>")
        elif re.match(r"^\s*\|.*\|\s*$", line) and "---" not in line:
            if in_list:
                out.append(f"</{in_list}>")
                in_list = None
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            out.append("<tr>" + "".join(f"<th>{_inline(c)}</th>" for c in cells)
                       + "</tr>")
        elif re.match(r"^\s*\|[\s:\-|]+\|\s*$", line):
            continue  # 表格分隔行
        elif line.startswith("- "):
            if in_list != "ul":
                if in_list:
                    out.append(f"</{in_list}>")
                out.append("<ul>")
                in_list = "ul"
            out.append(f"<li>{_inline(line[2:])}</li>")
        else:
            if in_list:
                out.append(f"</{in_list}>")
                in_list = None
            out.append(f"<p>{_inline(line)}</p>")
    if in_list:
        out.append(f"</{in_list}>")
    out.append("</body></html>")
    # 把相邻的 <tr> 包进 <table>
    body = "\n".join(out)
    body = re.sub(r"(<tr>.*?</tr>\n)+", lambda m: f"<table>{m.group(0)}</table>",
                  body)
    return body


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("用法: python reports/render_repair_html.py <in.md> <out.html>")
        return 2
    src, dst = Path(argv[0]), Path(argv[1])
    dst.write_text(render(src.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"HTML → {dst}({dst.stat().st_size} 字节)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
