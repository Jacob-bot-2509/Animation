"""Measure the actual training-side corpus size for hyperparameter derivation.

Reads the frozen current-core bindings, loads the 311 training-side records
(train + selected_draft), and reports character/length statistics per field
so batch size, sequence length, steps/epoch and epochs can be derived from
the real data instead of defaults.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
import core_signatures as core

ROOT = core.ROOT
CORE = ROOT / "reviews/codex-supervision/2026-10-07-deep-isolation-followup/effective-core-v3"

def main():
    bindings = core.load_record_bindings()
    by_id = {b["id"]: b for b in bindings}
    print(json.dumps({"total_bindings": len(bindings)}, ensure_ascii=False))
    train_side = [b for b in bindings if b.get("group") in ("train", "selected_draft")]
    other = [b for b in bindings if b.get("group") not in ("train", "selected_draft")]
    print(json.dumps({"train_side": len(train_side),
                      "other_groups": sorted({b.get("group", "") for b in other})}, ensure_ascii=False))

    lengths = {"problem": [], "solution": [], "answer": [], "scene_spec": [], "total": []}
    missing = []
    for b in train_side:
        try:
            rec = core.load_record(by_id, b["id"])
        except Exception as exc:  # noqa: BLE001 统计脚本要能报出所有载入失败
            missing.append({"id": b["id"], "error": str(exc)[:120]})
            continue
        total = 0
        for field in ("problem", "solution", "answer"):
            text = rec.get(field, "")
            n = len(text) if isinstance(text, str) else 0
            lengths[field].append(n)
            total += n
        scene = rec.get("scene_spec")
        scene_text = ""
        if isinstance(scene, dict):
            for key in ("objects", "steps"):
                values = scene.get(key, [])
                if isinstance(values, list):
                    scene_text += "\n".join(v for v in values if isinstance(v, str))
        lengths["scene_spec"].append(len(scene_text))
        total += len(scene_text)
        lengths["total"].append(total)

    def stat(vals):
        vals = sorted(vals)
        if not vals:
            return None
        n = len(vals)
        return {"n": n, "min": vals[0], "p50": vals[n // 2], "p90": vals[int(n * 0.9)],
                "p95": vals[int(n * 0.95)], "max": vals[-1], "sum": sum(vals)}

    out = {"loaded_train_side_records": len(lengths["total"]),
           "missing": missing,
           "chars_per_field": {k: stat(v) for k, v in lengths.items()}}
    (ROOT / "reviews/2026-10-08-hyperparam-derivation" ).mkdir(exist_ok=True)
    (ROOT / "reviews/2026-10-08-hyperparam-derivation/corpus-stats.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main())
