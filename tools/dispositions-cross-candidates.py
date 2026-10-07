"""跨集同核心候选逐对裁决:确认同核心(SAME_CORE)或给出数学区别(DIFFERENT_CORE)."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LISTS = ROOT / "reviews/2026-10-07-semantic-core-lists"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


DISPOSITIONS = {
    ("draft-c18-02", "test-geom-024"): {
        "verdict": "SAME_CORE_CONFIRMED",
        "evidence": {
            "train_problem": "求两平行平面 π1:2x-y+2z=1 与 π2:2x-y+2z=5 之间的距离(答案4/3)",
            "eval_problem": "求两平行平面 2x-y+2z=1 与 2x-y+2z=7 之间的距离(答案2)",
            "shared_structure": "相同法向量(2,-1,2)、相同第一平面常数1、相同解法"
                              "点面距离公式|d1-d2|/|n|,仅第二平面常数不同(5 vs 7)",
            "train_side": "selected_draft(draft-c18-02)", "eval_side": "test(test-geom-024)",
        },
        "action": "训练侧draft-c18-02需修订(同ID不增删题,由Codex修),"
                  "与c31-01/c31-03同规;不得靠换数字排除泄漏",
    },
}


def main() -> int:
    cand = json.loads((LISTS / "cross-candidates.json").read_text(encoding="utf-8-sig"))
    rows = []
    for c in cand["candidates"]:
        key = (c["train_id"], c["eval_id"])
        d = DISPOSITIONS.get(key)
        if d is None:
            raise ValueError("candidate without authored disposition: " + str(key))
        rows.append({**c, **d})
    out = LISTS / "cross-candidates-disposed.json"
    with out.open("w", encoding="utf-8", newline="\n") as f:
        json.dump({"schema": "cross-candidates-disposed-v1",
                   "total_candidates": len(rows),
                   "same_core": sum(1 for r in rows if r["verdict"] == "SAME_CORE_CONFIRMED"),
                   "rows": rows}, f, ensure_ascii=False, indent=2)
        f.write("\n")
    b = out.read_bytes()
    print(f"逐对裁决完成: {len(rows)} 对")
    for r in rows:
        print(f"  {r['train_id']} <-> {r['eval_id']}: {r['verdict']}")
    print(f"回执: {out.relative_to(ROOT)}  sha256={digest(b)}  bytes={len(b)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
