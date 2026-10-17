"""鐙珛瀹¤(淇鍚?:澶嶇畻 10 鏉″満鏅笌缁戝畾,鍙,涓嶆敼浠讳綍浜х墿銆?
鐢ㄦ硶:python -B -X utf8 scene_audit.py [--json out.json]
"""
import argparse
import ast
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CAND = ROOT / "reviews/data-prep/2026-10-17-submission/asset-evidence/presentation-candidates"
TPL_DIR = ROOT / "reviews/data-prep/2026-10-17-submission/asset-evidence/template-fix-candidate"
TEMPLATE = TPL_DIR / "render_templates_v4_candidate.py"
RECORDS = ROOT / "archives/reviews/codex-supervision/2026-10-17-first-batch-exact-math-review/candidate-v2/records.jsonl"

sys.path.insert(0, str(TPL_DIR))
import render_templates_v4_candidate as tpl  # noqa: E402

WRAPPER_HEAD = (
    '"""Auto-generated runnable shell for a text-only presentation candidate.\n\n'
    "The fragment below is authored; this shell only adds the Manim import and the\n"
    "Scene subclass so `manim -ql scene_runnable.py Candidate` can import it.\n"
    "This file has never been executed by the pipeline.\n"
    '"""\n'
    "from manim import *  # noqa: F401,F403\n\n\n"
    "class Candidate(Scene):\n"
    "    def construct(self):\n"
)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", default="")
    args = ap.parse_args()

    lines = [x for x in RECORDS.read_text(encoding="utf-8").splitlines() if x.strip()]
    recs = {}
    raw = {}
    for line in lines:
        rec = json.loads(line)
        sid = rec.get("id") or rec.get("sample_id")
        recs[sid] = rec
        raw[sid] = line

    bind = {}
    for line in (CAND / "presentation-bindings.jsonl").read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            bind[row["sample_id"]] = row

    template_sha = sha(TEMPLATE.read_bytes())
    samples = []
    for sid, rec in recs.items():
        row = bind.get(sid, {})
        spec = rec.get("scene_spec") or {}
        sources = [rec.get("problem", ""), *(spec.get("steps") or []), rec.get("answer", "")]
        code, plan = tpl.scene_blocks_v2(sources[0], sources[1:-1], sources[-1])
        plan_bytes = json.dumps(plan, ensure_ascii=False, sort_keys=True,
                                separators=(",", ":")).encode("utf-8")
        scene_path = CAND / "scenes" / f"{sid}.py"
        scene_text = scene_path.read_text(encoding="utf-8") if scene_path.is_file() else ""
        try:
            compile(scene_text, str(scene_path), "exec")
            standalone = "OK"
        except SyntaxError as exc:
            standalone = f"{type(exc).__name__}: {exc.msg} (line {exc.lineno})"
        try:
            ast.parse(WRAPPER_HEAD + scene_text)
            wrapped = "OK"
        except SyntaxError as exc:
            wrapped = f"{type(exc).__name__}: {exc.msg}"

        mid = []
        for idx, r in enumerate(plan["rows"]):
            frags = [f for f in r["fragments"] if f["kind"] in ("text", "math")]
            if not frags:
                mid.append({"row": idx, "reason": "empty_row"})
                continue
            last = frags[-1]
            if last["kind"] == "text":
                tail = last["content"].rstrip()
                if tail and tail[-1] not in tpl.ROW_END_PUNCT:
                    mid.append({"row": idx, "tail": tail[-16:]})

        samples.append({
            "sample_id": sid,
            "scene_exists": scene_path.is_file(),
            "scene_sha256": sha(scene_path.read_bytes()) if scene_path.is_file() else None,
            "bind_scene_sha_ok": row.get("scene_sha256") == (sha(scene_path.read_bytes()) if scene_path.is_file() else None),
            "scene_is_template_output": scene_text == code,
            "template_sha_ok": row.get("template_sha256") == template_sha,
            "plan_sha_ok": row.get("plan_sha256") == sha(plan_bytes),
            "plan_rows_ok": row.get("plan_rows") == len(plan["rows"]),
            "plan_pages_ok": row.get("plan_pages_provisional") == len(plan["provisional_pages"]),
            "coverage_ok": tpl.coverage_ok(sources, plan),
            "record_sha_ok": row.get("corrected_record_sha256") == sha(raw[sid].encode("utf-8")),
            "geometry_objects_ok": row.get("geometry_objects") == (spec.get("objects") or []),
            "standalone_syntax": standalone,
            "wrapped_syntax": wrapped,
            "drawing_primitives": sum(scene_text.count(p + "(") for p in (
                "Circle", "Dot", "Line", "Polygon", "Axes", "Arrow", "Arc", "Sector", "Triangle")),
            "rows": len(plan["rows"]),
            "provisional_pages": len(plan["provisional_pages"]),
            "mid_cut_rows": mid,
        })

    def fails(key):
        return sum(1 for s in samples if s[key] is False)

    result = {
        "template": {"path": str(TEMPLATE), "sha256": template_sha,
                     "version": tpl.TEMPLATE_VERSION},
        "samples": samples,
        "totals": {
            "samples": len(samples),
            "rows": sum(s["rows"] for s in samples),
            "mid_cut_rows": sum(len(s["mid_cut_rows"]) for s in samples),
            "standalone_syntax_fail": sum(1 for s in samples if s["standalone_syntax"] != "OK"),
            "wrapped_syntax_fail": sum(1 for s in samples if s["wrapped_syntax"] != "OK"),
            "drawing_primitives": sum(s["drawing_primitives"] for s in samples),
            "scene_sha_fail": fails("bind_scene_sha_ok"),
            "scene_reproduce_fail": fails("scene_is_template_output"),
            "template_sha_fail": fails("template_sha_ok"),
            "plan_sha_fail": fails("plan_sha_ok"),
            "plan_rows_fail": fails("plan_rows_ok"),
            "plan_pages_fail": fails("plan_pages_ok"),
            "coverage_fail": fails("coverage_ok"),
            "record_sha_fail": fails("record_sha_ok"),
            "geometry_objects_fail": fails("geometry_objects_ok"),
        },
    }
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.json:
        Path(args.json).write_text(text + "\n", encoding="utf-8")
        print(json.dumps(result["totals"], ensure_ascii=False))
    else:
        print(text)
    checks = ["scene_sha_fail", "scene_reproduce_fail", "template_sha_fail", "plan_sha_fail",
              "plan_rows_fail", "plan_pages_fail", "coverage_fail", "record_sha_fail",
              "geometry_objects_fail", "wrapped_syntax_fail", "mid_cut_rows"]
    ok = all(result["totals"][k] == 0 for k in checks)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

