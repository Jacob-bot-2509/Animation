"""扫描场景代码里 MathTex 公式中的 CJK 字符(LaTeX 默认模板不支持)。"""
import re
from pathlib import Path

SCENES = Path(r"D:\Animation-Model-Training\reviews\data-prep\2026-10-17-submission"
              r"\asset-evidence\presentation-candidates\scenes")
CJK = re.compile("[\u4e00-\u9fff]")

for p in sorted(SCENES.glob("*.py")):
    text = p.read_text(encoding="utf-8")
    for m in re.finditer(r"MathTex\('([^']*)'", text):
        if CJK.search(m.group(1)):
            print(p.name, "->", m.group(1)[:90])
