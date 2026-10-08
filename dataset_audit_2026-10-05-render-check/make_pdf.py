"""AUDIT_REPORT.md → HTML(自包含, 中文字体) → 供 headless Edge 打印 PDF。

只读报告文件; 只写 dataset_audit_2026-10-02/ 下的 html 产物。
"""
from __future__ import annotations

import pathlib

from markdown_it import MarkdownIt

BASE = pathlib.Path(__file__).resolve().parent
SRC = BASE / "RENDER_REPORT.md"
DST = BASE / "RENDER_REPORT.html"

md = MarkdownIt("commonmark", {"html": True, "typographer": False})
md.enable("table")

text = SRC.read_text(encoding="utf-8")
body = md.render(text)

CSS = """
@page { size: A4; margin: 15mm 13mm 15mm 13mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body {
  font-family: "Microsoft YaHei", "微软雅黑", "Segoe UI", "SimSun", sans-serif;
  font-size: 10pt; line-height: 1.62; color: #1a1a1a; margin: 0;
}
h1 { font-size: 19pt; margin: 0 0 4pt 0; padding-bottom: 5pt;
     border-bottom: 2.4pt solid #1f4e79; color: #1f4e79; }
h2 { font-size: 13.5pt; margin: 15pt 0 6pt 0; padding: 3pt 0 3pt 7pt;
     border-left: 4pt solid #1f4e79; background: #eef3f9; color: #16365c;
     page-break-after: avoid; }
h3 { font-size: 11.5pt; margin: 11pt 0 4pt 0; color: #1f4e79;
     page-break-after: avoid; }
p { margin: 4pt 0; }
ul, ol { margin: 4pt 0 4pt 0; padding-left: 18pt; }
li { margin: 2pt 0; }
blockquote { margin: 7pt 0; padding: 5pt 9pt; background: #f5f7fa;
             border-left: 3pt solid #9db8d2; color: #333; font-size: 9.2pt; }
blockquote p { margin: 2pt 0; }
code { font-family: Consolas, "Courier New", "Microsoft YaHei", monospace;
       background: #f2f2f2; padding: 0.5pt 2.5pt; border-radius: 2pt;
       font-size: 8.8pt; }
pre { background: #f6f8fa; border: 0.5pt solid #d6dde5; border-radius: 3pt;
      padding: 6pt 8pt; overflow-wrap: anywhere; page-break-inside: avoid; }
pre code { background: none; font-size: 8.6pt; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0 9pt 0;
        font-size: 8.6pt; }
th, td { border: 0.5pt solid #b7c3d0; padding: 3pt 4.5pt;
         vertical-align: top; text-align: left; overflow-wrap: anywhere; }
th { background: #dfe8f2; color: #16365c; font-weight: 600; }
tr { page-break-inside: avoid; }
thead { display: table-header-group; }
tbody tr:nth-child(even) { background: #f7fafd; }
hr { border: none; border-top: 0.8pt solid #c9d3de; margin: 12pt 0; }
a { color: #1f4e79; text-decoration: none; overflow-wrap: anywhere; }
strong { color: #000; }
h1 + blockquote { margin-top: 8pt; }
"""

doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>候选数据集全量审计报告（2026-10-02）</title>
<style>{CSS}</style>
</head>
<body>
{body}
</body>
</html>
"""

DST.write_text(doc, encoding="utf-8")
print(f"html written: {DST}")
print(f"source md: {SRC.stat().st_size} bytes -> html: {DST.stat().st_size} bytes")
