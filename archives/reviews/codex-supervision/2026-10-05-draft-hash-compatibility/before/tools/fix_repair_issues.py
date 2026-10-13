"""修复 codex-repair-v1 的两类问题(用户授权,小心修改):
1) 公式内中文(L002 硬伤):定点把 \\text{中文} 换成 \\text{英文},数学零改动;
2) scene_spec.steps 缺失「第N步:」前缀:按 1-based 序号补齐中文数字前缀,
   与其余 84 题格式一致;已有正确前缀的步骤不动。
只改 draft-codex-repair-v1.jsonl;改完请重跑 draft_audit.py 复核并更新
draft-selection.json 的 sha256。
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "reviews/2026-10-05-training-diversity-drafts"

# (batch, id, 字段, 精确旧串, 新串)
TEXT_FIXES = [
    ("batch-01", "draft-c52-05", "problem",
     r"\text{其余}", r"\text{otherwise}"),
    ("batch-02", "draft-c51-03", "solution",
     r"\text{患病}", r"\text{diseased}"),
    ("batch-06", "draft-c46-03", "answer",
     r"\text{唯一最近}", r"\text{ uniquely nearest}"),
    ("batch-08", "draft-c09-04", "answer",
     r"\text{或}", r"\text{ or }"),
    ("batch-16", "draft-c45-03", "solution",
     r"\text{两枚皆正}", r"\text{both heads}"),
    ("batch-16", "draft-c45-03", "solution",
     r"\text{两枚同面}", r"\text{same face}"),
    ("batch-16", "draft-c45-03", "scene_spec",
     r"\text{两枚皆正}", r"\text{both heads}"),
    ("batch-16", "draft-c45-03", "scene_spec",
     r"\text{两枚同面}", r"\text{same face}"),
]

CN = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
      "十一", "十二", "十三", "十四", "十五"]
PREFIX = re.compile(r"^第[一二三四五六七八九十]+步")


def cn(i: int) -> str:
    if i <= 15:
        return CN[i - 1]
    return str(i)


def fix_field(text: str, old: str, new: str, count: int) -> tuple[str, int]:
    if old not in text:
        return text, count
    n = text.count(old)
    return text.replace(old, new), count + n


def fix_scene(spec: dict, old: str, new: str, count: int) -> tuple[dict, int]:
    for k in ("objects", "steps"):
        items = spec.get(k, [])
        for i, s in enumerate(items):
            if isinstance(s, str) and old in s:
                items[i] = s.replace(old, new)
                count += s.count(old)
    return spec, count


def main() -> int:
    files = sorted(DRAFTS.glob("batch-*/draft-codex-repair-v1.jsonl"))
    text_fixed = 0
    prefix_added = 0
    changed_files = set()
    for p in files:
        batch = p.parent.name
        rows = [json.loads(l) for l in p.read_text(
            encoding="utf-8").splitlines() if l.strip()]
        changed = False
        for r in rows:
            # 1) 定点替换公式内中文
            for tb, tid, field, old, new in TEXT_FIXES:
                if tb != batch or tid != r["id"]:
                    continue
                if field == "scene_spec":
                    spec, n = fix_scene(r["scene_spec"], old, new, 0)
                    r["scene_spec"] = spec
                else:
                    val, n = fix_field(r.get(field, ""), old, new, 0)
                    r[field] = val
                if n:
                    text_fixed += n
                    changed = True
            # 2) 补齐步骤前缀(仅真缺失的)
            steps = r.get("scene_spec", {}).get("steps", [])
            for idx, s in enumerate(steps):
                if not PREFIX.match(s):
                    steps[idx] = f"第{cn(idx + 1)}步:{s}"
                    prefix_added += 1
                    changed = True
        if changed:
            p.write_text("\n".join(json.dumps(r, ensure_ascii=False,
                                               separators=(",", ":"))
                                   for r in rows) + "\n",
                         encoding="utf-8", newline="\n")
            changed_files.add(p.parent.name)
    print("公式内中文替换:", text_fixed, "处")
    print("补齐前缀:", prefix_added, "条")
    print("改动文件:", len(changed_files), "个:", sorted(changed_files))
    return 0


if __name__ == "__main__":
    sys.exit(main())
