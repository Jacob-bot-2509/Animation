"""合并 18 批 v4-final 逐题修订文档为一份审阅稿 MD,供 render_review.py 出 PDF。"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "reviews/2026-10-05-training-diversity-drafts"
OUT = ROOT / "outputs" / "draft-review" / "draft-review-v4-final.md"

COVER = """# 训练数据扩充题 · 审阅稿(v4-final)

版本:codex-repair-v4-final。18 批 / 264 题;原编号、题数与顺序全部保留,删除 0 题。
每批文档结构:题目 → 推导 → 答案 → 场景对象 → 场景步骤。

- 数学:41 项精确符号复算通过;165+120 项符号/整数检查通过
- 格式:公式内中文 0;步骤前缀 1172/1172;编码损坏 0
- 泄漏筛查:与训练池/冻结 eval/test 精确重叠 0,近重复最高 0.45(候选筛查,非证书)
- 状态:未正式准入;动画尚未渲染验收;许可证为仅内部研究

---

"""


def main() -> int:
    parts = [COVER]
    for batch in sorted(DRAFTS.glob("batch-*/")):
        md = batch / "DRAFT_REPORT-codex-repair-v4-final.md"
        if not md.is_file():
            print(f"缺 {md}")
            return 1
        parts.append(md.read_text(encoding="utf-8").rstrip() + "\n")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n\n".join(parts), encoding="utf-8", newline="\n")
    print(f"合并 {len(parts) - 1} 批 -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
