"""首批 10 条资产修复批次选择(只读):覆盖全部故障类型矩阵。

类型矩阵(Codex 要求的覆盖):
A spec_step_text_truncated_at_28_characters(全部有)
B spec_steps_after_fifth_omitted
C text_answer_not_displayed
D problem_replaced_by_formula_extraction_failure_placeholder
E tex_in_Text_not_typeset_as_MathTex(高频)
F historical_decimal_literals_need_fraction_display_adapter
G fixed_template_geometry_requires_record_specific_validation(固定几何待逐题核验)
选择规则:每条被选记录尽量覆盖多种类型;纯文字题/答案、混合公式、长步骤、
超五步、固定几何错配各有代表。
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EV = ROOT / "data" / "asset_evidence.json"
OUT = Path(__file__).resolve().parent / "first-batch-10.json"


def main() -> int:
    d = json.loads(EV.read_text(encoding="utf-8"))
    recs = d["records"]
    rows = []
    for k, v in recs.items():
        errs = set(v.get("errors") or [])
        warns = set(v.get("warnings") or [])
        tags = set()
        if "spec_step_text_truncated_at_28_characters" in errs:
            tags.add("A")
        if "spec_steps_after_fifth_omitted" in errs:
            tags.add("B")
        if "text_answer_not_displayed" in errs:
            tags.add("C")
        if "problem_replaced_by_formula_extraction_failure_placeholder" in errs:
            tags.add("D")
        if "tex_in_Text_not_typeset_as_MathTex" in warns:
            tags.add("E")
        if "historical_decimal_literals_need_fraction_display_adapter" in warns:
            tags.add("F")
        if "fixed_template_geometry_requires_record_specific_validation" in warns:
            tags.add("G")
        rows.append({"sample_id": k, "tags": sorted(tags),
                     "errors": sorted(errs), "warnings": sorted(warns)})

    # 贪心覆盖:优先选标签多的,保证每种类型至少一个代表
    picked = []
    covered: set = set()
    for want in (5, 4, 3, 2, 1):
        if len(picked) >= 10:
            break
        for r in sorted(rows, key=lambda x: -len(x["tags"])):
            if r["sample_id"] in {p["sample_id"] for p in picked}:
                continue
            if len(r["tags"]) < want:
                continue
            if not (set(r["tags"]) - covered):
                continue
            picked.append(r)
            covered |= set(r["tags"])
            if len(picked) >= 10 or covered >= {"A", "B", "C", "D", "E", "F", "G"}:
                break
    # 若还有类型没覆盖,补选只含该类型的记录
    missing = {"A", "B", "C", "D", "E", "F", "G"} - covered
    for tag in sorted(missing):
        if len(picked) >= 10:
            break
        for r in sorted(rows, key=lambda x: len(x["tags"]), reverse=True):
            if r["sample_id"] in {p["sample_id"] for p in picked}:
                continue
            if tag in r["tags"]:
                picked.append(r)
                covered.add(tag)
                break
    # 类型全覆盖后,继续按 (标签数,错误数) 补足 10 条;同核心族(去 -sN 后缀)不重复占位
    if len(picked) < 10:
        def core(sid):
            import re as _re
            return _re.sub(r"-s\d+$", "", sid)
        cores_seen = {core(p["sample_id"]) for p in picked}
        for r in sorted(rows, key=lambda x: (len(x["tags"]), len(x["errors"])),
                        reverse=True):
            if len(picked) >= 10:
                break
            if r["sample_id"] in {p["sample_id"] for p in picked}:
                continue
            if core(r["sample_id"]) in cores_seen:
                continue
            cores_seen.add(core(r["sample_id"]))
            picked.append(r)

    out = {
        "batch": "first-batch-10",
        "purpose": "资产模板修复候选的多故障覆盖静态绑定清单;仅是候选准备规模,不是审核吞吐承诺或渲染执行许可",
        "covered_types": sorted(covered),
        "uncovered_types": sorted({"A", "B", "C", "D", "E", "F", "G"} - covered),
        "records": picked,
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if len(picked) == 10 else 1


if __name__ == "__main__":
    raise SystemExit(main())
