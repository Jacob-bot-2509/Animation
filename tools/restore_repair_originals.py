"""从 Codex 交付目录的 staged 副本恢复全部 18 批 draft-codex-repair-v1.jsonl
(覆盖我此前有 bug 的修复造成的损坏),并按 draft-selection.json 逐批核对 SHA。

只读 staged 原件;目标文件字节级还原;SHA 不匹配即拒绝写入。
"""
from __future__ import annotations
import hashlib
import json
import shutil
import sys
from pathlib import Path
from draft_io import require_legacy_selection

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "reviews/2026-10-05-training-diversity-drafts"
SEL = DRAFTS / "draft-selection.json"
STAGED_08 = ROOT / "reviews/codex-supervision/2026-10-05-batch-repair-execution/staged"
STAGED_18 = ROOT / "reviews/codex-supervision/2026-10-05-remaining-batch-audit/staged"


def main() -> int:
    require_legacy_selection(SEL)
    sel = json.loads(SEL.read_text(encoding="utf-8"))
    ok = True
    for e in sel["entries"]:
        batch = e["batch"]
        staged_dir = STAGED_08 if int(batch.split("-")[1]) <= 8 else STAGED_18
        src = staged_dir / f"{batch}.jsonl"
        dst = DRAFTS / batch / "draft-codex-repair-v1.jsonl"
        if not src.is_file():
            print(f"缺 staged 原件: {src}")
            ok = False
            continue
        h = hashlib.sha256(src.read_bytes()).hexdigest()
        if h != e["sha256"]:
            print(f"SHA 不匹配 {batch}: staged={h[:16]} 期望={e['sha256'][:16]}")
            ok = False
            continue
        shutil.copyfile(src, dst)
        print(f"恢复 {batch} (SHA {h[:16]} 匹配)")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
