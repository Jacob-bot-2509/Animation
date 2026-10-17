"""把审核包 plan.json 渲染成可读行,便于逐题核对文字/公式。"""
import json
from pathlib import Path

PACKS = Path(r"D:\Animation-Model-Training\reviews\data-prep\2026-10-17-submission"
             r"\asset-evidence\presentation-pipeline\runs\review-packs")

for pack in sorted(PACKS.iterdir()):
    if not pack.is_dir():
        continue
    plan = json.loads((pack / "plan.json").read_text(encoding="utf-8"))
    print("=" * 70)
    print(pack.name, "rows:", len(plan["rows"]), "pages:", len(plan["provisional_pages"]))
    for ri, row in enumerate(plan["rows"]):
        parts = []
        for f in row["fragments"]:
            if f["kind"] == "break":
                continue
            parts.append(f["content"] if f["kind"] == "text" else f"${f['content']}$")
        print(f"  {ri:2d} [{row['source_index']}] " + "".join(parts))
