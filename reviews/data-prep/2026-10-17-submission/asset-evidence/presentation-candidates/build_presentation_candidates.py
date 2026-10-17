"""逐题呈现实现候选:用修正后记录 + 修复版模板生成场景代码(不渲染)。

输入:archives/.../2026-10-17-first-batch-exact-math-review/candidate/records.jsonl
(Codex 修正版,只读)。输出:本目录 scenes/<id>.py + presentation-bindings.jsonl。
绑定按修正记录自身字节 SHA(新源绑定,不套旧哈希);覆盖按修复版 make_plan
重算比对;几何清单取自修正后 objects;全部 PENDING_REVIEW,不渲染不自判。
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(HERE.parent / "template-fix-candidate"))
from render_templates_v2_candidate import scene_blocks_v2, coverage_ok, TemplateError  # noqa: E402

RECORDS = ROOT / "archives/reviews/codex-supervision/2026-10-17-first-batch-exact-math-review/candidate/records.jsonl"
SCENES = HERE / "scenes"


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    SCENES.mkdir(parents=True, exist_ok=True)
    rows = []
    errors = []
    for raw in RECORDS.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        rec = json.loads(raw)
        sid = rec.get("id") or rec.get("sample_id")
        problem = rec.get("problem", "")
        steps = (rec.get("scene_spec") or {}).get("steps", []) or []
        answer = rec.get("answer", "")
        objects = (rec.get("scene_spec") or {}).get("objects", []) or []
        try:
            code, plan = scene_blocks_v2(problem, steps, answer)
            cov = coverage_ok([problem, *steps, answer], plan)
        except TemplateError as exc:
            errors.append({"sample_id": sid, "error": str(exc)})
            continue
        scene_path = SCENES / f"{sid}.py"
        scene_path.write_text(code, encoding="utf-8")
        rows.append({
            "sample_id": sid,
            "corrected_record_sha256": sha_bytes(raw.encode("utf-8")),
            "scene_sha256": sha_bytes(code.encode("utf-8")),
            "plan_rows": len(plan["rows"]),
            "plan_pages_provisional": len(plan["provisional_pages"]),
            "coverage_ok": cov,
            "layout_status": plan["layout"],
            "geometry_objects": objects,
            "render_verdict": "PENDING_REVIEW",
            "visual_verdict": "PENDING_REVIEW",
        })
    out = HERE / "presentation-bindings.jsonl"
    out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
                   encoding="utf-8")
    print(f"scenes={len(rows)} errors={len(errors)}")
    for e in errors:
        print("ERROR", json.dumps(e, ensure_ascii=False))
    for r in rows:
        print(f"  {r['sample_id']:24s} rows={r['plan_rows']:>3} pages={r['plan_pages_provisional']} "
              f"cov={r['coverage_ok']} objs={len(r['geometry_objects'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
