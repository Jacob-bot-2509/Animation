"""新版渲染包 md → 自包含 MathJax HTML(渲染输入层第二步);PDF 需 headless 浏览器另行."""  # noqa: E501
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKS = ROOT / "archives/dataset-audits/dataset_audit_2026-10-07-render-check-v2/render-packs-v2"
OUT = ROOT / "archives/dataset-audits/dataset_audit_2026-10-07-render-check-v2/render-html-v2"

MATHJAX = (
    "<script>window.MathJax={tex:{inlineMath:[['$','$'],['\\\\(','\\\\)']],"
    "displayMath:[['$$','$$'],['\\\\[','\\\\]']]},svg:{fontCache:'none'}};</script>\n"
    "<script src=\"https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js\" "
    "id=\"MathJax-script\" async></script>\n"
)
CSS = """body{font-family:'Microsoft YaHei','Segoe UI',sans-serif;font-size:11pt;
line-height:1.65;color:#1a1a1a;margin:24px auto;max-width:900px;padding:0 16px;}
h1{color:#1f4e79;border-bottom:2px solid #1f4e79;padding-bottom:4pt;}
h3{color:#1f4e79;margin-top:16pt;}"""


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    try:
        from markdown_it import MarkdownIt  # noqa: PLC0415
    except ImportError:
        print("FAIL: markdown_it 未安装 → HTML 层 UNVERIFIED(需 pip install markdown-it-py)")
        return 1
    md = MarkdownIt("commonmark", {"html": True, "typographer": False})
    summary = {}
    for p in sorted(PACKS.glob("*.md")):
        text = p.read_text(encoding="utf-8")
        body = md.render(text)
        html = ("<!DOCTYPE html><html lang='zh'><head><meta charset='utf-8'>"
                f"<title>{p.stem} 新版渲染</title>{MATHJAX}<style>{CSS}</style></head>"
                f"<body>{body}</body></html>")
        out = OUT / f"{p.stem}.html"
        out.write_text(html, encoding="utf-8", newline="\n")
        b = out.read_bytes()
        summary[p.stem] = {"md_sha256": digest(p.read_bytes()),
                           "html_sha256": digest(b), "html_bytes": len(b)}
        print(f"{p.stem:44s} html={len(b):>9d} B  sha={digest(b)[:16]}")
    report = {
        "schema": "render-html-v2-v1",
        "note": "自包含MathJax HTML(渲染输入层);浏览器视觉确认与PDF层未执行,"
                "Manim场景渲染UNVERIFIED(生产门CLOSED)",
        "html_files": summary,
    }
    rp = ROOT / "archives/dataset-audits/dataset_audit_2026-10-07-render-check-v2/render-html-v2-report.json"
    with rp.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write("\n")
    b = rp.read_bytes()
    print(f"报告: {rp.relative_to(ROOT)}  sha256={digest(b)}  bytes={len(b)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
