"""draft-selection.json 切换到 codex-repair-v2:path/version/sha256 更新,
source_sha256 记 v1 哈希,report 指向 v2 报告并记录其 SHA。"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path
from draft_io import require_legacy_selection

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "reviews/2026-10-05-training-diversity-drafts"
SEL = DRAFTS / "draft-selection.json"
SUMMARY = DRAFTS / "repair-v2-summary.json"


def main() -> int:
    require_legacy_selection(SEL)
    sel = json.loads(SEL.read_text(encoding="utf-8"))
    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    for e in sel["entries"]:
        batch = e["batch"]
        s = summary[batch]
        v2 = DRAFTS / batch / "draft-codex-repair-v2.jsonl"
        rep = DRAFTS / batch / "DRAFT_REPORT-codex-repair-v2.md"
        h2 = hashlib.sha256(v2.read_bytes()).hexdigest()
        rh = hashlib.sha256(rep.read_bytes()).hexdigest()
        assert h2 == s["v2_sha256"], f"{batch} v2 SHA 不符"
        e["path"] = f"{batch}/draft-codex-repair-v2.jsonl"
        e["version"] = "codex-repair-v2"
        e["source_sha256"] = s["v1_sha256"]
        e["sha256"] = h2
        e["report_path"] = f"{batch}/DRAFT_REPORT-codex-repair-v2.md"
        e["report_sha256"] = rh
        print(f"{batch}: v2={h2[:12]} src={s['v1_sha256'][:12]} "
              f"rep={rh[:12]}")
    SEL.write_text(json.dumps(sel, ensure_ascii=False, indent=2),
                   encoding="utf-8", newline="\n")
    print("selection 已切换到 v2")
    return 0


if __name__ == "__main__":
    sys.exit(main())
