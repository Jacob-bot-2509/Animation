"""对比 v2/v3 在 10 条真实样本上的行尾断词与覆盖,只读。"""
import importlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
TPL = ROOT / "reviews/data-prep/2026-10-17-submission/asset-evidence/template-fix-candidate"
RECORDS = ROOT / "archives/reviews/codex-supervision/2026-10-17-first-batch-exact-math-review/candidate/records.jsonl"
sys.path.insert(0, str(TPL))

END = "。，；：、！？）》」』”’，,.;:!?)]}"


def stats(mod):
    rows_total = 0
    mid = []
    cov_fail = []
    chars = 0
    for line in RECORDS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        sid = rec.get("id")
        spec = rec.get("scene_spec") or {}
        sources = [rec.get("problem", ""), *(spec.get("steps") or []), rec.get("answer", "")]
        code, plan = mod.scene_blocks_v2(*sources[:1], sources[1:-1], sources[-1])
        if not mod.coverage_ok(sources, plan):
            cov_fail.append(sid)
        for idx, row in enumerate(plan["rows"]):
            rows_total += 1
            frags = [f for f in row["fragments"] if f["kind"] in ("text", "math")]
            last = frags[-1] if frags else None
            if last and last["kind"] == "text":
                tail = last["content"].rstrip()
                if tail and tail[-1] not in END:
                    mid.append({"sample": sid, "row": idx, "tail": tail[-16:]})
    return {"rows": rows_total, "mid_cut": len(mid), "coverage_fail": cov_fail, "mid_cut_examples": mid[:6]}


v2 = importlib.import_module("render_templates_v2_candidate")
v3 = importlib.import_module("render_templates_v3_candidate")
out = {"v2": stats(v2), "v3": stats(v3)}
print(json.dumps(out, ensure_ascii=False, indent=2))
(HERE / "v2-v3-compare.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
