"""同核心隔离骨架筛查:问题文本去数字后的 LaTeX 结构跨集比对,只生成候选,不判定."""
from __future__ import annotations
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = Path("reviews/codex-supervision/2026-10-07-core-evidence-digest")
OUT = ROOT / "reviews/2026-10-07-math-review"

NUM = re.compile(r"\d+(?:\.\d+)?")
WS = re.compile(r"\s+")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def skeleton(text: str) -> str:
    """去数字、压空白,保留 LaTeX 结构(变量/函数/指数结构中的数字一并去除,交由人工复核)."""
    t = NUM.sub("#", text)
    t = WS.sub("", t)
    return t


def load_refs() -> list[dict]:
    packet = ROOT / PACKET
    man = json.loads((packet / "delivery-manifest.json").read_text(encoding="utf-8-sig"))
    entries = {x["path"]: x for x in man["artifacts"]}
    ref_bytes = (packet / "priority-task-references.jsonl").read_bytes()
    if digest(ref_bytes) != entries["priority-task-references.jsonl"]["raw_sha256"]:
        raise ValueError("core packet row bindings changed")
    return [json.loads(line) for line in ref_bytes.decode("utf-8-sig").splitlines() if line.strip()]


def main() -> int:
    refs = load_refs()
    cache = {}
    rows = []
    for ref in refs:
        src = ref["source_path"]
        if src not in cache:
            data = (ROOT / src).read_bytes()
            if digest(data) != ref["source_raw_sha256"]:
                raise ValueError("source version changed: " + src)
            cache[src] = data.splitlines(keepends=True)
        rec = json.loads(cache[src][ref["source_line"] - 1].decode("utf-8-sig"))
        problem = rec["problem"]
        if not isinstance(problem, str) or not problem.strip():
            raise ValueError("missing problem text: " + rec.get("id"))
        rows.append({
            "id": ref["id"], "group": ref["group"], "source_path": src,
            "source_line": ref["source_line"],
            "record_version_sha256": ref["record_version_sha256"],
            "problem": problem, "skeleton": skeleton(problem),
            "digit_count": len(NUM.findall(problem)),
        })
    train_side = [r for r in rows if r["group"] in ("train", "selected_draft")]
    eval_side = [r for r in rows if r["group"] in ("eval", "test")]
    print(f"训练侧 {len(train_side)} 条,评测侧 {len(eval_side)} 条,合计 {len(rows)}")

    # 骨架碰撞
    eval_by_skel = defaultdict(list)
    for r in eval_side:
        if r["digit_count"] > 0:  # 无数字的题不可能是数值变体,但保留全部以报告
            eval_by_skel[r["skeleton"]].append(r)
    cross = []
    for r in train_side:
        for e in eval_by_skel.get(r["skeleton"], []):
            cross.append({"train": r, "eval": e, "skeleton": r["skeleton"]})
    print(f"跨集骨架碰撞: {len(cross)} 对")

    # 训练集内碰撞(单独报告)
    train_by_skel = defaultdict(list)
    for r in train_side:
        train_by_skel[r["skeleton"]].append(r)
    intra = {s: vs for s, vs in train_by_skel.items() if len(vs) > 1}
    print(f"训练集内骨架碰撞: {len(intra)} 组")

    # 骨架长度直方图(短骨架碰撞噪声高,人工复核时注意)
    skel_len = Counter(len(r["skeleton"]) for r in rows)
    short = sum(v for k, v in skel_len.items() if k < 60)
    print(f"骨架长度<60的记录数: {short}(短题去数字后易误撞,候选须人工甄别)")

    out_path = OUT / "isolation-skeleton-screen-v1.json"
    with out_path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump({
            "schema": "isolation-skeleton-screen-v1",
            "note": "仅候选生成:去数字LaTeX骨架相同不代表同核心,需逐对人工对抗复核;"
                    "数字含指数等结构位置,骨架相同可能只是短题巧合",
            "counts": {"train_side": len(train_side), "eval_side": len(eval_side),
                       "cross_candidates": len(cross), "intra_train_groups": len(intra)},
            "cross_candidates": [
                {"train_id": c["train"]["id"], "train_problem": c["train"]["problem"],
                 "eval_id": c["eval"]["id"], "eval_group": c["eval"]["group"],
                 "eval_problem": c["eval"]["problem"], "skeleton": c["skeleton"],
                 "reviewed": False} for c in cross],
            "intra_train_groups": [
                {"skeleton": s, "ids": [x["id"] for x in vs]} for s, vs in intra.items()],
        }, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"输出: {out_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
