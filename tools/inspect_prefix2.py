"""精确统计 scene_spec.steps 前缀:以中文数字「第N步」为准,只报真正缺失的。"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "reviews/2026-10-05-training-diversity-drafts"
CN = "一二三四五六七八九十"
PREFIX = re.compile(r"^第([一二三四五六七八九十]+)步[:、:.]?")


def cn2int(s: str) -> int:
    m = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6,
         "七": 7, "八": 8, "九": 9, "十": 10}
    if len(s) == 1:
        return m[s]
    if s == "十":
        return 10
    if s.startswith("十"):
        return 10 + m[s[1]]
    if s.endswith("十"):
        return m[s[0]] * 10
    return m[s[0]] * 10 + m[s[1]]


def main() -> int:
    files = sorted(DRAFTS.glob("batch-*/draft-codex-repair-v1.jsonl"))
    total, missing, wrong_num, other_fmt = 0, [], [], []
    for p in files:
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            steps = r.get("scene_spec", {}).get("steps", [])
            for i, s in enumerate(steps, 1):
                total += 1
                m = PREFIX.match(s)
                if not m:
                    missing.append((p.parent.name, r["id"], i, s[:60]))
                elif cn2int(m.group(1)) != i:
                    wrong_num.append((p.parent.name, r["id"], i, m.group(1), s[:40]))
    print("总步骤数:", total)
    print("真缺失前缀:", len(missing))
    for b, qid, i, s in missing[:15]:
        print(f"  {b}/{qid} step{i}: {s}")
    print("前缀数字错位:", len(wrong_num))
    for b, qid, i, got, s in wrong_num[:10]:
        print(f"  {b}/{qid} step{i} 前缀为第{got}步: {s}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
