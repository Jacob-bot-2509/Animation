# -*- coding: utf-8 -*-
"""libpku 数学考卷 PDF 可提取性验证:
对 33 个 PDF 提取文本,按文本量分类 文字版/混合/扫描版,
文字版输出前若干字符供质量评估。只读,打印报告。"""
import re
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
DIRS = [ROOT / "holdout-sources/libpku/专业课/高等数学B",
        ROOT / "holdout-sources/libpku/专业课/线性代数",
        ROOT / "holdout-sources/libpku/专业课/数学分析"]

CN_CHAR = re.compile(r"[一-鿿]")
MATH_HINT = re.compile(r"[=∫∑√≤≥≠∞∈∂\\]|\d")


def classify(text, pages):
    n_cn = len(CN_CHAR.findall(text))
    density = n_cn / max(pages, 1)
    if density >= 30:
        return "text" if MATH_HINT.search(text) else "text_plain"
    if density >= 5:
        return "mixed"
    return "scanned"


def main() -> int:
    rows = []
    for d in DIRS:
        for pdf in sorted(d.rglob("*.pdf")):
            try:
                reader = PdfReader(str(pdf))
                pages = len(reader.pages)
                text = "\n".join((p.extract_text() or "") for p in reader.pages)
                kind = classify(text, pages)
                rows.append((d.name, pdf.name, pages, len(CN_CHAR.findall(text)), kind))
            except Exception as exc:
                rows.append((d.name, pdf.name, 0, 0, "error:" + str(exc)[:40]))
    print(f"{'科目':10} {'文件':46} {'页':>3} {'中文字符':>7}  分类")
    for subj, name, pages, cn, kind in rows:
        print(f"{subj:10} {name[:44]:46} {pages:3} {cn:7}  {kind}")
    usable = [r for r in rows if r[4].startswith("text")]
    print("---")
    print("文字版可用:", len(usable), "/", len(rows))
    # 对一个文字版 PDF 打印样本
    for d in DIRS:
        for pdf in sorted(d.glob("*.pdf")):
            try:
                reader = PdfReader(str(pdf))
                text = "\n".join((p.extract_text() or "") for p in reader.pages)
                if classify(text, len(reader.pages)).startswith("text"):
                    print("=== 样本:", pdf.name)
                    print(text[:500])
                    return 0
            except Exception:
                continue
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
