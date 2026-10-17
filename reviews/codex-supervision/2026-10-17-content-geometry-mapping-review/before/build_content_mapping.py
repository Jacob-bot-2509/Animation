"""首批 10 条内容/几何映射构建(只读;使用 Codex 修复版模板 API)。

产出 content-geometry-mapping.jsonl:每条记录 = 源行绑定 + 完整片段计划
(make_plan,coverage 重算比对)+ 几何核对清单(PENDING_REVIEW,不自判)。
布局/数学/几何结论留待真实渲染与审核;本脚本不渲染、不改现役文件。
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(HERE.parent / "template-fix-candidate"))
from render_templates_v2_candidate import make_plan, coverage_ok, TemplateError  # noqa: E402

BATCH = HERE.parent / "first-batch-10.v2.json"
EV = ROOT / "data" / "asset_evidence.json"

GEO_KEYWORDS = [
    "抛物线", "直线", "圆", "椭圆", "双曲线", "曲线", "切点", "切线", "坐标轴",
    "点", "面积", "矩形", "区域", "积分", "微元", "极限", "平面", "向量", "三角形",
    "正方形", "圆点", "刻度", "边界", "端点", "区间", "交点", "原点",
]
TPL_GEOMETRY = {
    "derivative": ["坐标轴", "函数曲线", "切点", "切线"],
    "integral": ["坐标轴", "上下曲线", "微元矩形", "积分区域"],
    "area": ["坐标轴", "曲线", "边界线", "面积区域"],
}


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    records = batch.get("records") or batch.get("entries") or []
    ev = json.loads(EV.read_text(encoding="utf-8"))
    out_rows = []
    errors = []

    for rec in records:
        sid = rec.get("sample_id") or rec.get("id")
        if not sid:
            errors.append({"problem": "no_sample_id", "record": rec})
            continue
        # 源行绑定:优先用清单里的 path/line/SHA,否则从 asset_evidence 的 source 取
        src_path = rec.get("source_path") or (ev["records"].get(sid) or {}).get("source", {}).get("path")
        line_no = rec.get("line_no") or (ev["records"].get(sid) or {}).get("source", {}).get("line")
        try:
            src = Path(str(src_path).replace("D:\\Animation-Model-Training\\", str(ROOT) + "\\"))
            if not src.is_absolute():
                src = ROOT / str(src_path)
            data = src.read_bytes()
            raw = data.splitlines(keepends=True)[line_no - 1]
            obj = json.loads(raw.decode("utf-8"))
        except Exception as exc:  # noqa: BLE001
            errors.append({"problem": "source_read_failed", "sample_id": sid,
                           "error": f"{exc.__class__.__name__}: {exc}"})
            continue

        problem = obj.get("problem", "")
        steps = (obj.get("scene_spec") or {}).get("steps", []) or []
        answer = obj.get("answer", "")
        try:
            plan = make_plan(steps)
            cov = coverage_ok(steps, plan)
        except TemplateError as exc:
            errors.append({"problem": "plan_failed", "sample_id": sid, "error": str(exc)})
            continue

        # 几何核对清单:从题干/步骤中扫出的几何要素 + 模板几何,全部待审
        text = problem + " " + " ".join(steps)
        found = [k for k in GEO_KEYWORDS if k in text]
        tpl = (ev["records"].get(sid) or {}).get("scene_source", {}).get("template")
        checklist = []
        for item in TPL_GEOMETRY.get(tpl, []):
            checklist.append({"element": item, "found_in_text": item in text,
                              "verdict": "PENDING_REVIEW"})
        for item in found:
            if item not in [c["element"] for c in checklist]:
                checklist.append({"element": item, "found_in_text": True,
                                  "verdict": "PENDING_REVIEW"})

        out_rows.append({
            "sample_id": sid,
            "template": tpl,
            "raw_line_sha256": sha_bytes(raw),
            "plan_sha256": hashlib.sha256(json.dumps(
                plan, ensure_ascii=True, separators=(",", ":")).encode()).hexdigest(),
            "plan_rows": len(plan["rows"]),
            "plan_pages_provisional": len(plan["provisional_pages"]),
            "layout_status": plan["layout"],
            "coverage_ok": cov,
            "problem_chars": len(problem),
            "steps_count": len(steps),
            "answer_chars": len(answer),
            "geometry_checklist": checklist,
            "math_verdict": "PENDING_REVIEW",
            "geometry_verdict": "PENDING_REVIEW",
        })

    out = HERE / "content-geometry-mapping.jsonl"
    out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in out_rows) + "\n",
                   encoding="utf-8")
    print(f"mapped={len(out_rows)} errors={len(errors)}")
    for e in errors:
        print("ERROR", json.dumps(e, ensure_ascii=False)[:200])
    for r in out_rows:
        print(f"  {r['sample_id']:24s} tpl={r['template']} rows={r['plan_rows']} "
              f"pages={r['plan_pages_provisional']} cov={r['coverage_ok']} "
              f"geom_items={len(r['geometry_checklist'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
