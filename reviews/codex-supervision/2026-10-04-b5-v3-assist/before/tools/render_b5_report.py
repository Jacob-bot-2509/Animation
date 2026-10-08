"""离线生成B5数学报告PDF；只在MathJax排版验证成功后打印静态HTML。"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import uuid
from html.parser import HTMLParser
from pathlib import Path

from render_review import EDGE, MATHJAX_LOCAL, build_html, protect_math

ROOT = Path(__file__).resolve().parents[1]
STYLE = """
body { font-size: 9pt; line-height: 1.55; }
h1 { font-size: 17pt; }
table { table-layout: fixed; }
thead { display: table-header-group; }
tr { break-inside: avoid; page-break-inside: avoid; }
.grid th, .grid td { text-align: center; padding: 4pt 2pt; }
.grid th:nth-child(1) { width: 13%; }
.grid th:nth-child(n+2):nth-child(-n+5) { width: 9%; }
.grid th:nth-child(n+6) { width: 17%; }
.pairs th:nth-child(1) { width: 13%; }
.pairs th:nth-child(2) { width: 12%; }
.pairs th:nth-child(n+3) { width: 37.5%; }
.pairs td:nth-child(-n+2) { white-space: nowrap; text-align: center; }
.pairs td { overflow-wrap: anywhere; padding: 5pt 4pt; }
mjx-container { font-size: 100% !important; max-width: 100%; }
"""


class _ErrorNodes(HTMLParser):
    def __init__(self):
        super().__init__()
        self.errors = 0

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "data-mjx-error" in values or values.get("data-mml-node") == "merror":
            self.errors += 1


def math_errors(dom: str) -> int:
    parser = _ErrorNodes()
    parser.feed(dom)
    return parser.errors


def render(md: Path, destination: Path, evidence: Path) -> dict:
    if not MATHJAX_LOCAL.is_file():
        raise RuntimeError("缺少本地MathJax；不使用网络资源回退")
    destination.mkdir(parents=True, exist_ok=True)
    evidence.mkdir(parents=True, exist_ok=True)
    profile = evidence / ("edge-profile-" + uuid.uuid4().hex[:12])
    command = [EDGE, "--headless", "--disable-gpu", "--no-first-run",
               "--no-pdf-header-footer", "--allow-file-access-from-files",
               "--user-data-dir=" + str(profile)]
    text = md.read_text(encoding="utf-8")
    html = build_html(text, "B5 近重复阈值校准报告").replace(
        "document.title='MJDONE';",
        "document.documentElement.dataset.mathjaxReady='true';")
    html = html.replace("</head>", f"<style>{STYLE}</style></head>")
    html = html.replace("<table>", '<table class="grid">', 1)
    html = html.replace("<table>", '<table class="pairs">', 1)
    source = evidence / "b5-mathjax-source.html"
    source.write_text(html, encoding="utf-8")
    cp = subprocess.run(command + ["--dump-dom", "--virtual-time-budget=10000",
                                  source.as_uri()], capture_output=True, timeout=45,
                        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    dom = cp.stdout.decode("utf-8", "replace").replace("\r\n", "\n")
    (evidence / "mathjax-dom.html").write_text(dom, encoding="utf-8")
    (evidence / "mathjax-stderr.txt").write_bytes(cp.stderr)
    spans = re.findall(r'<span class="math">(.*?)</span>', dom, re.S)
    expected = len(protect_math(text)[1])
    rendered = sum("<mjx-container" in span for span in spans)
    errors = math_errors(dom)
    stats = {"dom_rc": cp.returncode, "expected_math": expected,
             "rendered_math": rendered, "math_errors": errors,
             "mathjax_ready": 'data-mathjax-ready="true"' in dom}
    if cp.returncode or not stats["mathjax_ready"] or rendered != expected or errors:
        raise RuntimeError("数学排版验证失败：" + json.dumps(stats))
    static = re.sub(r"<script\b[^>]*>.*?</script>", "", dom, flags=re.S | re.I)
    # SVG已在DOM内，打印时无需再次运行脚本或等待网络。
    html_path = destination / "b5-calibration-report.html"
    html_path.write_text(static, encoding="utf-8", newline="\n")
    candidate = evidence / "b5-calibration-report.candidate.pdf"
    cp = subprocess.run(command + ["--print-to-pdf=" + str(candidate),
                                  "--virtual-time-budget=1000", html_path.as_uri()],
                        capture_output=True, timeout=45,
                        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    (evidence / "print-stderr.txt").write_bytes(cp.stderr)
    stats["print_rc"] = cp.returncode
    if cp.returncode or not candidate.is_file() or candidate.stat().st_size == 0:
        raise RuntimeError("PDF打印失败")
    pdf = destination / "b5-calibration-report.pdf"
    pdf.write_bytes(candidate.read_bytes())
    stats["pdf"] = str(pdf)
    stats["pdf_bytes"] = pdf.stat().st_size
    (evidence / "render-results.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    return stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--md", type=Path,
                        default=ROOT / "data/b5-calibration-report/b5-calibration-report.md")
    parser.add_argument("--out", type=Path,
                        default=ROOT / "data/b5-calibration-report/pdf")
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(render(args.md.resolve(), args.out.resolve(), args.evidence.resolve()),
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
