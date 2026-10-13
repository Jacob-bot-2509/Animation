"""把 draft-selection.json 各批 sha256 更新为当前实际文件哈希
(修复公式内中文+步骤前缀后);只改 sha256 字段,其余保留。"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "reviews/2026-10-05-training-diversity-drafts"
SEL = DRAFTS / "draft-selection.json"


def main() -> int:
    sel = json.loads(SEL.read_text(encoding="utf-8"))
    changed = 0
    for e in sel["entries"]:
        p = DRAFTS / e["path"]
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        if h != e["sha256"]:
            print(f"{e['batch']}: {e['sha256'][:12]} -> {h[:12]}")
            e["sha256"] = h
            changed += 1
    if changed:
        SEL.write_text(json.dumps(sel, ensure_ascii=False, indent=2),
                       encoding="utf-8", newline="\n")
        print(f"更新 {changed} 批哈希")
    else:
        print("无变化")
    return 0


if __name__ == "__main__":
    sys.exit(main())
