"""独立核验 Codex 严格修复交付:我的原始报告计数、264回执绑定、交付清单58项."""
from __future__ import annotations
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUP = ROOT / "reviews/codex-supervision/2026-10-07-core-submission-supervision"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    # 1) 我的 v1 文件 SHA 是否与 Codex 索引引用一致
    print("== 1. 我的 v1 提交文件(Codex 索引引用值) ==")
    for rel, sha, size in [
        ("reviews/2026-10-07-gap-materials/core-submission-v1/package-reference.json",
         "99eff04df56c9d26fc329f2f57d918f81552910ad71005a5db042aee35d89d9e", 1135),
        ("reviews/2026-10-07-gap-materials/core-submission-v1/submission-manifest.json",
         "6081b95f1945d912abb6fe80792e9ef6299bb12fd31d8a623cdee6db2b25d2f8", 1982),
    ]:
        b = (ROOT / rel).read_bytes()
        print(f"{'MATCH' if digest(b) == sha and len(b) == size else 'MISMATCH'}  {rel}  {len(b)}B")

    # 2) 我的原始 consistency-report.jsonl 实际计数(Codex 称 158 PASS/603 FAIL,602 tail_mismatch,11 decimal_in_answer)
    print("\n== 2. 我的原始 consistency-report.jsonl 实际计数 ==")
    rep_path = ROOT / "reviews/2026-10-07-gap-materials/core-submission-v1/consistency-report.jsonl"
    b = rep_path.read_bytes()
    print(f"raw_sha256={digest(b)}  bytes={len(b)}")
    rows = [json.loads(l) for l in b.decode("utf-8-sig").splitlines() if l.strip()]
    status = {}
    tail = 0
    decimal_ans = 0
    for r in rows:
        status[r.get("status", "?")] = status.get(r.get("status", "?"), 0) + 1
        if r.get("tail_text_relation") == "DIFFERENT_TEXT_UNRESOLVED":
            tail += 1
        for i in r.get("issues", []):
            code = i.get("code") if isinstance(i, dict) else (str(i) if "decimal" in str(i) else "")
            field = i.get("field") if isinstance(i, dict) else ""
            if code == "decimal_requires_exact_form" and field == "answer":
                decimal_ans += 1
    print(f"total={len(rows)}  status={status}  tail_mismatch={tail}  decimal_in_answer={decimal_ans}")

    # 3) review-ids.json 实际条数与 264 草稿 ID 交集(Codex 称 296 条,交集 0)
    print("\n== 3. review-ids.json 与 264 草稿交集 ==")
    rid_path = ROOT / "outputs/review-ids.json"
    rb = rid_path.read_bytes()
    print(f"raw_sha256={digest(rb)}  bytes={len(rb)}")
    rid = json.loads(rb.decode("utf-8-sig"))
    ids = [x if isinstance(x, str) else str(x) for x in rid] if isinstance(rid, list) else []
    if not ids and isinstance(rid, dict):
        for v in rid.values():
            ids.extend([x if isinstance(x, str) else str(x) for x in v] if isinstance(v, list) else [])
    from collections import Counter
    print(f"review-ids 条数={len(ids)}")
    # 264 草稿 ID:经核心包 priority-task-references 或 draft-selection
    draft_ids = set()
    for src in [
        "data/v2/train/draft-selection.json",
        "data/v2/train/draft-selection-v3-2026-10-05.json",
    ]:
        p = ROOT / src
        if p.exists():
            try:
                d = json.loads(p.read_text(encoding="utf-8-sig"))
                for entry in (d if isinstance(d, list) else d.get("entries", [])):
                    if isinstance(entry, dict) and entry.get("id"):
                        draft_ids.add(str(entry["id"]))
            except Exception as e:  # noqa: BLE001
                print(f"  ({src} 读取失败: {e})")
    # 也可从核心包 refs 取 selected_draft 组
    pkt = ROOT / "reviews/codex-supervision/2026-10-07-core-evidence-digest/priority-task-references.jsonl"
    if pkt.exists():
        for line in pkt.read_text(encoding="utf-8-sig").splitlines():
            if not line.strip():
                continue
            ref = json.loads(line)
            if ref.get("group") == "selected_draft":
                draft_ids.add(str(ref["id"]))
    inter = set(ids) & draft_ids
    print(f"264 草稿 ID 数={len(draft_ids)}  交集={len(inter)}  {sorted(inter)[:8]}")

    # 4) 交付清单 58 项全量重算
    print("\n== 4. delivery-manifest.json 全量重算 ==")
    man = json.loads((SUP / "delivery-manifest.json").read_text(encoding="utf-8-sig"))
    arts = man["artifacts"] if isinstance(man.get("artifacts"), list) else man.get("items", [])
    n = bad = 0
    for a in arts:
        p = (SUP / a["path"]).resolve() if "path" in a else (SUP / a.get("name", "")).resolve()
        if not p.exists():
            bad += 1
            print(f"  MISSING {p.name}")
            continue
        b = p.read_bytes()
        n += 1
        if digest(b) != a.get("raw_sha256", "") or len(b) != a.get("bytes", -1):
            bad += 1
            print(f"  MISMATCH {p.name}")
    print(f"清单项={len(arts)}  已核={n}  不匹配/缺失={bad}")

    # 5) math-corrections-30 结构:30 条,分布
    print("\n== 5. math-corrections-30.jsonl 结构与分布 ==")
    from collections import Counter
    mc = [json.loads(l) for l in (SUP / "math-corrections-30.jsonl").read_text(encoding="utf-8-sig").splitlines() if l.strip()]
    print(f"条数={len(mc)}  分布={dict(Counter(m.get('split', m.get('group', '?')) for m in mc))}")
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
