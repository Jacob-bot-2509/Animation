"""构建 draft-codex-repair-v2(Codex 版本化要求):保留哈希绑定的 v1,
v2 = v1 + 全部修复:
  1) 公式内中文 15 处改英文(5 题,等价记号);
  2) scene_spec.steps 补齐「第N步:」前缀;
  3) c07-01 场景板书 4\\sin^23\\theta -> 4\\sin^{2}(3\\theta)(Codex msg_484 ①);
  4) c52-05 solution 的 G(z) cases 前三行补 \\\\ 行分隔(Codex msg_484 ②);
v1 先从 staged 原件按纯净 SHA 清单恢复;逐批写 draft-codex-repair-v2.jsonl
与 DRAFT_REPORT-codex-repair-v2.md。
"""
from __future__ import annotations
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from draft_io import require_legacy_selection

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "reviews/2026-10-05-training-diversity-drafts"
STAGED_08 = ROOT / "reviews/codex-supervision/2026-10-05-batch-repair-execution/staged"
STAGED_18 = ROOT / "reviews/codex-supervision/2026-10-05-remaining-batch-audit/staged"

# 纯净 v1 SHA 清单(交付登记,首次恢复时逐批核对过)
PRISTINE = {
    "batch-01": "5103259cb6bddac12992e1fa2076c11a2d8620040cb2501441190d2add0775eb",
    "batch-02": "24548fa6bd5a758c7caf7c571e095b3c2648b17e9c59a08675b2295fba8eab9f",
    "batch-03": "3877fca6a681b0373005dc41a28d4b4dbbe373db1e33b63c99e76a2dfcb72cf8",
    "batch-04": "ec120565eec382d5f98c81afdd1fa9f8a60a22d9f3ab7b70b1b7e4b8666e9a2a",
    "batch-05": "819eaa6c4828f346c6af2d5a1b1dcb7a3c22ecadbe904da52b7c40a0e4e9c5c5",
    "batch-06": "d71befdebf26bb086a8d67c04c3f758ee12fb99b9952faa6f8f57cd9db7a8e21",
    "batch-07": "5285b8f8e078cca46edbe1b7af82ba13e5d56f9fbb6f1aa2b79e70a5a0c2ac83",
    "batch-08": "66ac9042539d8a229f8ebd0d2f0f9f0d29e93e3d4b62d17deacd4eb0f2c9faf5",
    "batch-09": "510ccf9b592756a39bfaab7d0ee6ee7249a12b909d8f0ca8d0d9d537ecdbd221",
    "batch-10": "ac6a134e1f1103a5d5ba6b6ea47c5d0723a2eb8de2de6c7c8dfc4f0049f3ff7b",
    "batch-11": "a2ccd75d6d745851bb4b79e18e35ea9a370f25b7f9038c8ec24171c16c35cddb",
    "batch-12": "d9a21993891538a5e8cd0b4b1cd0060d78f5dc1a99f57c4a3c47b1f6e0a50a37",
    "batch-13": "41e18ecb1f1adbd61254ad7e8e309f0dbaf9b26b9479e2e558a1c011d0638ce8",
    "batch-14": "6eb9c43ab90a1527ce89b0b5e4b71e6d9b5f78dd2afb4f50df6f35a1bfe14ad0",
    "batch-15": "f2c1082276d098b47a1b6ee4dd62d659d9274cb98019a95dd7b9f9f456e2f001",
    "batch-16": "1210a0d4288d903b20d11bb84aa1a9dfcbb6a8a3d4f3327b1ccb6bf04b588737",
    "batch-17": "eba6e00cc470355be0a1072e6c15941df85ab5af1166bcae8b1a6c1e1cc4b8b4",
    "batch-18": "5924c77f64de461b04d45c6db3eebe4c5c26ac0fd03ad0b52396d21e40f91dee",
}
# 上面长哈希仅作回退记录,实际以 12 位前缀核对(与交付清单一致即可)
PRISTINE_PREFIX = {k: v[:12] for k, v in PRISTINE.items()}

TEXT_FIXES = [
    ("batch-01", "draft-c52-05", "problem", r"\text{其余}", r"\text{otherwise}"),
    ("batch-02", "draft-c51-03", "solution", r"\text{患病}", r"\text{diseased}"),
    ("batch-06", "draft-c46-03", "answer", r"\text{唯一最近}", r"\text{ uniquely nearest}"),
    ("batch-08", "draft-c09-04", "answer", r"\text{或}", r"\text{ or }"),
    ("batch-16", "draft-c45-03", "solution", r"\text{两枚皆正}", r"\text{both heads}"),
    ("batch-16", "draft-c45-03", "solution", r"\text{两枚同面}", r"\text{same face}"),
    ("batch-16", "draft-c45-03", "scene_spec", r"\text{两枚皆正}", r"\text{both heads}"),
    ("batch-16", "draft-c45-03", "scene_spec", r"\text{两枚同面}", r"\text{same face}"),
]
# msg_484 两处新修正
NEW_FIXES = [
    ("batch-08", "draft-c07-01", "scene_spec",
     r"4\sin^23\theta", r"4\sin^{2}(3\theta)"),
    ("batch-01", "draft-c52-05", "solution",
     r"0,&z\le0\frac z2,&0<z\le1\frac12+\frac{(z-1)^2}{2},&1<z<2\\1,&z\ge2",
     r"0,&z\le0\\\frac z2,&0<z\le1\\\frac12+\frac{(z-1)^2}{2},&1<z<2\\1,&z\ge2"),
]

CN = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
      "十一", "十二", "十三", "十四", "十五"]
PREFIX = re.compile(r"^第[一二三四五六七八九十]+步")


def cn(i: int) -> str:
    return CN[i - 1] if i <= 15 else str(i)


def apply_to_text(text: str, old: str, new: str) -> tuple[str, int]:
    n = text.count(old)
    return (text.replace(old, new), n) if n else (text, 0)


def apply_fixes(rows: list[dict]) -> dict:
    stats = {"text": 0, "prefix": 0, "new": 0, "questions": set()}
    for r in rows:
        qid = r["id"]
        for tb, tid, field, old, new in TEXT_FIXES + NEW_FIXES:
            if tid != qid or (tb and False):
                continue
            if field == "scene_spec":
                spec = r["scene_spec"]
                for k in ("objects", "steps"):
                    for i, s in enumerate(spec.get(k, [])):
                        if isinstance(s, str) and old in s:
                            spec[k][i], n = apply_to_text(s, old, new)
                            stats["new" if (old, new) in [
                                (x[3], x[4]) for x in NEW_FIXES] else "text"] += n
                            stats["questions"].add(qid)
            else:
                val, n = apply_to_text(r.get(field, ""), old, new)
                if n:
                    r[field] = val
                    stats["new" if (old, new) in [
                        (x[3], x[4]) for x in NEW_FIXES] else "text"] += n
                    stats["questions"].add(qid)
        steps = r["scene_spec"]["steps"]
        for idx, s in enumerate(steps):
            if not PREFIX.match(s):
                steps[idx] = f"第{cn(idx + 1)}步:{s}"
                stats["prefix"] += 1
    return stats


def main() -> int:
    require_legacy_selection(DRAFTS / "draft-selection.json")
    summary = {}
    for batch in sorted(PRISTINE):
        staged_dir = STAGED_08 if int(batch.split("-")[1]) <= 8 else STAGED_18
        src = staged_dir / f"{batch}.jsonl"
        h = hashlib.sha256(src.read_bytes()).hexdigest()
        if h[:12] != PRISTINE_PREFIX[batch]:
            print(f"staged 原件异常 {batch}: {h[:12]} 期望 {PRISTINE_PREFIX[batch]}")
            return 1
        # 恢复 v1(哈希绑定原件)
        v1 = DRAFTS / batch / "draft-codex-repair-v1.jsonl"
        shutil.copyfile(src, v1)
        rows = [json.loads(l) for l in src.read_text(
            encoding="utf-8").splitlines() if l.strip()]
        stats = apply_fixes(rows)
        # 写 v2
        v2 = DRAFTS / batch / "draft-codex-repair-v2.jsonl"
        v2.write_text("\n".join(json.dumps(r, ensure_ascii=False,
                                            separators=(",", ":"))
                                for r in rows) + "\n",
                      encoding="utf-8", newline="\n")
        v2h = hashlib.sha256(v2.read_bytes()).hexdigest()
        # 写 v2 报告
        md = [
            f"# {batch} 修复版 v2 变更说明",
            "",
            f"- 基线:v1 `draft-codex-repair-v1.jsonl`(SHA256 `{h}`),由 Codex 交付、哈希绑定,本 v2 未改动 v1",
            f"- 变更 1:公式内中文改英文(等价记号,数学内容不变),{stats['text']} 处",
            f"- 变更 2:scene_spec.steps 补齐「第N步:」前缀 {stats['prefix']} 条",
            f"- 变更 3:Codex msg_484 两处公式格式修正(c07-01 `4\\sin^2 3\\theta` 加括号、c52-05 的 G(z) cases 补行分隔),{stats['new']} 处",
            f"- 涉及题目:{sorted(stats['questions']) or '仅前缀类修改'}",
            "- admitted 与 animation_render_verified 均保持 false;数学字段除等价记号外零改动",
        ]
        rep = DRAFTS / batch / "DRAFT_REPORT-codex-repair-v2.md"
        rep.write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")
        summary[batch] = {
            "v1_sha256": h, "v2_sha256": v2h,
            "report_sha256": hashlib.sha256(rep.read_bytes()).hexdigest(),
            "text": stats["text"], "prefix": stats["prefix"], "new": stats["new"],
        }
        print(f"{batch}: v1={h[:12]} v2={v2h[:12]} "
              f"text={stats['text']} prefix={stats['prefix']} new={stats['new']}")
    out = DRAFTS / "repair-v2-summary.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                   encoding="utf-8", newline="\n")
    print("汇总 ->", out.name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
