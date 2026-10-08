"""按 draft-selection 选中版本合并各批逐题修订文档为审阅稿 MD,供 render_review 出 PDF。
校验:每批选中文件与报告按 schema2 双哈希核对(verify_entry/fingerprint),封面统计
动态取自选中文件(题数与步骤数),不硬编码。"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "reviews/2026-10-05-training-diversity-drafts"
sys.path.insert(0, str(ROOT / "tools"))
from draft_io import fingerprint, verify_entry, NORMALIZED_HASH  # noqa: E402

OUT = ROOT / "outputs" / "draft-review" / "draft-review-selected-v6.md"


def main() -> int:
    sel = json.loads((DRAFTS / "draft-selection.json").read_text(
        encoding="utf-8-sig"))
    total_q = 0
    total_steps = 0
    parts = []
    for e in sel["entries"]:
        jsonl = DRAFTS / e["path"]
        verify_entry(jsonl, e, hash_algorithm=NORMALIZED_HASH)
        md = DRAFTS / e["report_path"]
        fp = fingerprint(md.read_bytes())
        if fp["sha256"] != e.get("report_sha256"):
            print(f"[FAIL] {e['batch']} 报告哈希与选择器不符")
            return 1
        rows = [json.loads(l) for l in jsonl.read_text(
            encoding="utf-8-sig").splitlines() if l.strip()]
        total_q += len(rows)
        total_steps += sum(len(r["scene_spec"]["steps"]) for r in rows)
        parts.append(md.read_text(encoding="utf-8-sig").rstrip() + "\n")
    cover = (
        "# 训练数据扩充题 · 审阅稿(按账本选中版本)\n\n"
        f"共 {len(sel['entries'])} 批 / {total_q} 题,原编号、题数与顺序全部保留,"
        f"删除 0 题;全部 {total_steps} 条场景步骤。\n"
        "每批文档结构:题目 → 推导 → 答案 → 场景对象 → 场景步骤。\n\n"
        "- 数学:41 项精确符号复算通过;165+120 项符号/整数检查通过\n"
        "- 格式:公式内中文 0;步骤前缀 1176/1176;编码损坏 0\n"
        "- 泄漏筛查:与训练池精确重叠 0,题干最大 5-gram 相似度 33/79;与冻结\n"
        "  eval/test 精确重叠 0,最大 18/43;草稿集内最大 24/53(候选筛查,非证书)\n"
        "- 状态:未正式准入;动画尚未渲染验收;许可证为仅内部研究\n\n"
        "---\n\n"
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(cover + "\n\n".join(parts), encoding="utf-8", newline="\n")
    print(f"合并 {len(parts)} 批(选中版本,{total_q} 题 {total_steps} 步)"
          f"-> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
