"""逐题呈现实现候选:用修正后记录 + 修复版模板生成场景代码(不渲染)。

输入:archives/.../2026-10-17-first-batch-exact-math-review/candidate/records.jsonl
(Codex 修正版,只读)。输出:本目录 scenes/<id>.py + presentation-bindings.jsonl。
绑定按修正记录自身字节 SHA(新源绑定,不套旧哈希);覆盖按修复版 make_plan
重算比对;几何清单取自修正后 objects;全部 PENDING_REVIEW,不渲染不自判。

2026-10-17 改用 text-candidate-v4(行内片段间距 buff=0.12;v2/v3 字节不动)。
记录改用 candidate-v2(仅改 prob-042 公式里的 CJK:默认 LaTeX 模板无法编译 \text{正面})。
每题额外绑定 template_sha256 / plan_sha256,供管线端独立复算场景与分页计划。
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(HERE.parent / "template-fix-candidate"))
from render_templates_v4_candidate import (  # noqa: E402
    TEMPLATE_VERSION, TemplateError, coverage_ok, scene_blocks_v2,
)

TEMPLATE_PATH = HERE.parent / "template-fix-candidate/render_templates_v4_candidate.py"

RECORDS = ROOT / "archives/reviews/codex-supervision/2026-10-17-first-batch-exact-math-review/candidate-v2/records.jsonl"
SCENES = HERE / "scenes"


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def canonical_plan_bytes(plan: dict) -> bytes:
    """管线端复算用的规范字节;plan_sha256 即此字节的 SHA。"""
    return json.dumps(plan, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def main() -> int:
    SCENES.mkdir(parents=True, exist_ok=True)
    template_sha = sha_bytes(TEMPLATE_PATH.read_bytes())
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
        scene_path.write_text(code, encoding="utf-8", newline="\n")
        # 绑定磁盘真实字节 SHA(Windows write_text 会换行翻译,回读再算)
        scene_disk_sha = sha_bytes(scene_path.read_bytes())
        rows.append({
            "sample_id": sid,
            "corrected_record_sha256": sha_bytes(raw.encode("utf-8")),
            "scene_sha256": scene_disk_sha,
            "template_version": TEMPLATE_VERSION,
            "template_sha256": template_sha,
            "plan_sha256": sha_bytes(canonical_plan_bytes(plan)),
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
                   encoding="utf-8", newline="\n")
    print(f"scenes={len(rows)} errors={len(errors)}")
    for e in errors:
        print("ERROR", json.dumps(e, ensure_ascii=False))
    for r in rows:
        print(f"  {r['sample_id']:24s} rows={r['plan_rows']:>3} pages={r['plan_pages_provisional']} "
              f"cov={r['coverage_ok']} objs={len(r['geometry_objects'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
