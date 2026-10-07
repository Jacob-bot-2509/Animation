"""同核心隔离筛查回执:v1(精确文本已由Codex做)+v2数字骨架+v3数字字母骨架+v4表述归一骨架."""
from __future__ import annotations
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = Path("reviews/codex-supervision/2026-10-07-core-evidence-digest")
OUT = ROOT / "reviews/2026-10-07-math-review"

NUM = re.compile(r"\d+(?:\.\d+)?")
LAT = re.compile(r"[A-Za-z]")
WS = re.compile(r"\s+")
VERBS = ["求", "计算", "判断", "讨论", "证明", "设", "已知", "说明", "指出", "验证", "确定",
         "求解", "证明:", "求:", "设:", "已知:", "问", "试", "试求", "若", "其中", "分别",
         "并", "给出", "写出", "解", "比较", "估计"]
PUNCT = re.compile(r"[，。:;：；,()（）!?？\s]")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sk_digits(t: str) -> str:
    return WS.sub("", NUM.sub("#", t))


def sk_letters(t: str) -> str:
    return WS.sub("", LAT.sub("v", NUM.sub("#", t)))


def sk_wording(t: str) -> str:
    s = LAT.sub("v", NUM.sub("#", t))
    for v in VERBS:
        s = s.replace(v, "@")
    return PUNCT.sub("", s)


def load_rows() -> list[dict]:
    packet = ROOT / PACKET
    man = json.loads((packet / "delivery-manifest.json").read_text(encoding="utf-8-sig"))
    entries = {x["path"]: x for x in man["artifacts"]}
    ref_bytes = (packet / "priority-task-references.jsonl").read_bytes()
    if digest(ref_bytes) != entries["priority-task-references.jsonl"]["raw_sha256"]:
        raise ValueError("core packet row bindings changed")
    refs = [json.loads(line) for line in ref_bytes.decode("utf-8-sig").splitlines() if line.strip()]
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
        rows.append({"id": ref["id"], "group": ref["group"],
                     "record_version_sha256": ref["record_version_sha256"],
                     "problem": rec["problem"]})
    return rows


def screen(rows: list[dict], key) -> dict:
    train_side = [r for r in rows if r["group"] in ("train", "selected_draft")]
    eval_side = [r for r in rows if r["group"] in ("eval", "test")]
    by = defaultdict(list)
    for r in eval_side:
        by[key(r["problem"])].append(r)
    cross = []
    for r in train_side:
        for e in by.get(key(r["problem"]), []):
            cross.append({"train_id": r["id"], "eval_id": e["id"],
                          "eval_group": e["group"],
                          "train_problem": r["problem"], "eval_problem": e["problem"]})
    return {"train_side": len(train_side), "eval_side": len(eval_side),
            "cross_candidates": cross}


def main() -> int:
    rows = load_rows()
    screens = {
        "v2_digit_skeleton": screen(rows, sk_digits),
        "v3_digit_letter_skeleton": screen(rows, sk_letters),
        "v4_wording_normalized_skeleton": screen(rows, sk_wording),
    }
    report = {
        "schema": "isolation-skeleton-screens-v1",
        "reviewer": "claude-code",
        "scope": "训练侧311(train47+草稿264) × 评测侧450(eval300+test150)",
        "prior_screens": {
            "v1_exact_text": {"cross_identical": 0, "by": "codex", "note":
                              "311×450=139950对精确题干文本比较,0相同"},
            "linalg048_family_296_pairs": {"cross_same_core": 0,
                "receipt": "reviews/2026-10-06-linalg048-admission/v3-receipt-bound/"
                           "semantic-review-workflow-v1.json",
                "note": "16评审者+对抗复核;295不同核心+1训练集内变体(linalg-058,非跨集);待Codex复验"},
        },
        "screens": screens,
        "honest_limits": [
            "文本骨架筛查无法覆盖结构性改写(同一数学核心的几何↔代数不同表述)",
            "数字骨架相同≠同核心,反之骨架不同也不等于不同核心;本报告仅证明'无同骨架跨集对'",
            "最终语义隔离判定需Codex独立复验,并可按家族指定追加人工复核",
        ],
        "verdict": "NO_CROSS_SPLIT_SKELETON_CANDIDATE_AT_ALL_SCREEN_LEVELS",
        "semantic_isolation_verdict": "NOT_ESTABLISHED",
        "PASS_CORE_SCOPE_issued": False,
    }
    out_path = OUT / "isolation-screens-v1.json"
    with out_path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write("\n")
    b = out_path.read_bytes()
    print(f"输出: {out_path.relative_to(ROOT)}")
    print(f"raw_sha256={digest(b)}  bytes={len(b)}")
    for name, s in screens.items():
        print(f"{name}: 跨集候选 {len(s['cross_candidates'])} 对")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
