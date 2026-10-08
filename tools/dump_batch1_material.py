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
OUT2 = ROOT / "reviews/2026-10-06-scene-standard-sweep/batch2-material.json"
OUT3 = ROOT / "reviews/2026-10-06-scene-standard-sweep/batch3-material.json"
OUT4 = ROOT / "reviews/2026-10-06-scene-standard-sweep/batch4-material.json"

# 90 remaining REVISE ids (from workflow-evidence-analysis.json)
REMAINING = json.loads((SUP / "workflow-evidence-analysis.json").read_text("utf-8"))[
    "remaining_without_any_scene_candidate"]
# 候选优先:矩阵/收敛/纯计算混合,取前 10
CHOSEN = [
    "draft-c02-01", "draft-c04-04", "draft-c06-01", "draft-c11-01", "draft-c11-04",
    "draft-c12-01", "draft-c23-01", "draft-c24-03", "draft-c26-03", "draft-c27-04",
]
# 批次二(用户指示继续改)
CHOSEN_BATCH2 = [
    "draft-c10-01", "draft-c10-03", "draft-c12-03", "draft-c14-01",
    "draft-c26-04", "draft-c27-01", "draft-c41-02", "draft-c42-04",
    "draft-c07-01", "draft-c49-03",
]
CHOSEN_BATCH3 = [
    "draft-c02-04", "draft-c07-03", "draft-c07-04", "draft-c10-04",
    "draft-c10-05", "draft-c14-02", "draft-c25-04", "draft-c25-05",
    "draft-c41-01", "draft-c41-04",
]
CHOSEN_BATCH4 = [
    "draft-c07-05", "draft-c08-01", "draft-c08-02", "draft-c08-03",
    "draft-c14-04", "draft-c17-04", "draft-c26-01", "draft-c26-05",
    "draft-c29-02", "draft-c29-03",
]


def main() -> int:
    try:
        audit = json.loads(AUDIT.read_text("utf-8"))["audit"]
        missing = [c for c in CHOSEN + CHOSEN_BATCH2 + CHOSEN_BATCH3 + CHOSEN_BATCH4 if c not in audit]
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

        def build(chosen, out_path):
            out = {"remaining_90": REMAINING, "chosen": []}
            for cid in chosen:
                a = audit[cid]
                out["chosen"].append({
                    "id": cid,
                    "deficiencies": a["deficiencies"],
                    "record": records[cid],
                })
            if out_path.exists():
                raise ValueError("output exists: " + str(out_path))
            out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8", newline="\n")
            print("chosen:", len(out["chosen"]), "->", out_path.name)
            for c in out["chosen"]:
                print(" -", c["id"], "| deficits:", len(c["deficiencies"]))

        build(CHOSEN, OUT) if not OUT.exists() else print("batch1 material exists (skip)")
        build(CHOSEN_BATCH2, OUT2) if not OUT2.exists() else print("batch2 material exists (skip)")
        build(CHOSEN_BATCH3, OUT3) if not OUT3.exists() else print("batch3 material exists (skip)")
        build(CHOSEN_BATCH4, OUT4)
        return 0
    except Exception as exc:
        print("[FAIL]", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
