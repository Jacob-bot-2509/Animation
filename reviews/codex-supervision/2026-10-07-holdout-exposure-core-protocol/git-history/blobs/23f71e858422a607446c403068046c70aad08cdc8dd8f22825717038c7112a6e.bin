"""Dump batch-1 material: the 90 remaining REVISE ids + audit deficiencies,
then the full records for the chosen batch from inputs-v2 (read-only)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUP = ROOT / "reviews/codex-supervision/2026-10-06-scene-repair-takeover"
AUDIT = ROOT / "reviews/2026-10-06-scene-standard-sweep/workflow-run-result.json"
INPUTS = SUP / "inputs-v2/inputs.json"
OUT = ROOT / "reviews/2026-10-06-scene-standard-sweep/batch1-material.json"

# 90 remaining REVISE ids (from workflow-evidence-analysis.json)
REMAINING = json.loads((SUP / "workflow-evidence-analysis.json").read_text("utf-8"))[
    "remaining_without_any_scene_candidate"]
# 候选优先:矩阵/收敛/纯计算混合,取前 10
CHOSEN = [
    "draft-c02-01", "draft-c04-04", "draft-c06-01", "draft-c11-01", "draft-c11-04",
    "draft-c12-01", "draft-c23-01", "draft-c24-03", "draft-c26-03", "draft-c27-04",
]


def main() -> int:
    try:
        audit = json.loads(AUDIT.read_text("utf-8"))["audit"]
        missing = [c for c in CHOSEN if c not in audit]
        if missing:
            raise ValueError("chosen ids missing from audit: " + str(missing))
        inputs = json.loads(INPUTS.read_text("utf-8"))
        assert inputs["record_count"] == 264
        records = {}
        for name in inputs["chunks"]:
            chunk = json.loads((INPUTS.parent / name).read_text("utf-8"))
            for rec in chunk.get("records", []):
                row = rec.get("record", {})
                records[row["id"]] = row
        if len(records) != 264:
            raise ValueError("inputs record count mismatch: " + str(len(records)))
        out = {"remaining_90": REMAINING,
               "chosen": []}
        for cid in CHOSEN:
            a = audit[cid]
            out["chosen"].append({
                "id": cid,
                "deficiencies": a["deficiencies"],
                "record": records[cid],
            })
        OUT.parent.mkdir(parents=True, exist_ok=True)
        if OUT.exists():
            raise ValueError("output exists")
        OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8", newline="\n")
        print("remaining_90:", len(REMAINING), "| chosen:", len(out["chosen"]))
        for c in out["chosen"]:
            print(" -", c["id"], "| deficits:", len(c["deficiencies"]))
        return 0
    except Exception as exc:
        print("[FAIL]", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
