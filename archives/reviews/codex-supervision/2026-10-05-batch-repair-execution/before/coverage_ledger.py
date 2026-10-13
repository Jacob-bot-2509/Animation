"""批次生产账本 + 跨批重复检测器。

1) 密度协调:对照 DATA_DIVERSITY_PLAN.json 的 53 考点,统计各批次已起草数,
   列出未覆盖/未满 5 条的考点(供后续批次选题);
2) 重复检测:对全部 batch-*/draft.jsonl 的题目做 5-gram Jaccard 相似度,
   两两对比并对照活动 train 行,高相似对(>=0.5)人工复核,防跨批重复出题。

用法: <venv>/Scripts/python.exe -X utf8 tools/runpy.py
      reviews/2026-10-05-training-diversity-drafts/coverage_ledger.py
"""
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DRAFTS = Path(__file__).resolve().parent
PLAN = ROOT / "reviews/codex-supervision/2026-10-05-mail-handling/DATA_DIVERSITY_PLAN.json"
MANIFEST = ROOT / "data/manifest.json"
THRESHOLD = 0.5  # 题目文字 5-gram Jaccard 阈值(草稿间从严,与 B5 的 2/5 一致)


def j5(a: str, b: str) -> float:
    def grams(s: str) -> set:
        t = re.sub(r"\s+", "", s)
        return {t[i:i + 5] for i in range(len(t) - 4)}
    ga, gb = grams(a), grams(b)
    if not ga or not gb:
        return 0.0
    return len(ga & gb) / len(ga | gb)


def load_rows(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines()
            if l.strip()]


def main() -> int:
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    groups = plan.get("concept_groups") or []
    concepts = {g["concept_id"]: g for g in groups if isinstance(g, dict)
                and g.get("concept_id")}
    if not concepts:  # 结构兜底
        recs = json.loads((PLAN.parent / "candidate-recovery"
                           / "candidate_catalog.json").read_text(
            encoding="utf-8"))["records"]
        concepts = {r["concept_id"]: {"concept_id": r["concept_id"],
                                      "concept": r["concept_id"],
                                      "active_count": 0,
                                      "candidate_count": 0} for r in recs}
    # 活动计数
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    active = {}
    for e in m["entries"]:
        if e["split"] != "train":
            continue
        p = (MANIFEST.parent / e["path"]).resolve()
        for r in load_rows(p):
            active[r["id"]] = r

    drafts = {}
    for d in sorted(DRAFTS.glob("batch-*/draft.jsonl")):
        for r in load_rows(d):
            drafts[r["id"]] = r

    # 1) 密度账本
    by_concept = {}
    for cid, c in concepts.items():
        by_concept[cid] = {"cid": cid,
                           "title": c.get("concept", cid),
                           "active": int(c.get("active_count", 0) or 0),
                           "drafted": 0}
    for r in drafts.values():
        cid = r.get("concept_id")
        if cid in by_concept:
            by_concept[cid]["drafted"] += 1
    short = sorted((v for v in by_concept.values()
                    if v["active"] + v["drafted"] < 5),
                   key=lambda v: v["active"] + v["drafted"])
    done = sorted((v for v in by_concept.values()
                   if v["active"] + v["drafted"] >= 5),
                  key=lambda v: v["cid"])
    print("== 密度账本 ==")
    print(f"考点总数 {len(by_concept)},已起草 {len(drafts)} 题,"
          f"达标(活动+起草>=5) {len(done)} 个")
    print("-- 未达标考点(活动+起草,按缺口排序) --")
    for v in short:
        print(f"  {v['cid']} {v['title']}: 活动{v['active']} + 起草{v['drafted']}"
              f" = {v['active']+v['drafted']} (缺 {5-v['active']-v['drafted']})")

    # 2) 跨批重复检测(草稿之间 + 草稿 vs 活动 train)
    print("== 重复检测 ==")
    pairs, same_concept = [], []
    dlist = sorted(drafts.values(), key=lambda r: r["id"])
    for i in range(len(dlist)):
        for j in range(i + 1, len(dlist)):
            s = j5(dlist[i]["problem"], dlist[j]["problem"])
            if s >= THRESHOLD:
                same = dlist[i].get("concept_id") == dlist[j].get("concept_id")
                (same_concept if same else pairs).append(
                    (s, dlist[i]["id"], dlist[j]["id"]))
    for r in dlist:
        for tid, tr in active.items():
            s = j5(r["problem"], tr.get("problem", ""))
            if s >= THRESHOLD:
                pairs.append((s, r["id"], tid))
    if pairs:
        print("  [!] 跨考点/对训练的高相似对(需人工复核是否实质重复):")
        for s, a, b in sorted(pairs, reverse=True):
            print(f"      J5={s:.3f}  {a} <-> {b}")
    else:
        print("  无跨考点高相似对")
    if same_concept:
        print("  [i] 同考点内相近对(预期:变体设计使然,已人工确认差异实质):")
        for s, a, b in sorted(same_concept, reverse=True):
            print(f"      J5={s:.3f}  {a} <-> {b}")
    else:
        print("  无同考点高相似对")

    # 3) 待覆盖考点(供下一批选题)
    print("== 建议下一批(取未达标前 3) ==")
    for v in short[:3]:
        print(f"  {v['cid']} {v['title']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
