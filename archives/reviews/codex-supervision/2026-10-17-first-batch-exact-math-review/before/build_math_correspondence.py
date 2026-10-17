"""首批 10 条逐题数学/计算/符号对应材料(只读,审核支撑,不自判)。

按 Codex 895/898 下一步:"首批10条逐题数学与实际计算/符号材料"。
对每条记录抽取:
- 小数字面量(须核验是否精确有理数 → 分数显示;默认保留原样)
- 文本分数与 LaTeX \\frac(记录为精确)
- 符号常量/根式(\\pi \\sqrt e ln sin cos 等,保留符号显示)
- 解答计算步骤(逐句)
全部 verdict=PENDING_REVIEW;真实判定由审核方(Codex+用户)给出。
"""
import hashlib
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
BATCH = HERE.parent / "first-batch-10.v2.json"
EV = ROOT / "data" / "asset_evidence.json"

DEC_RE = re.compile(r"-?\d+\.\d+")
FRAC_TEXT_RE = re.compile(r"-?\d+/\d+")
FRAC_TEX_RE = re.compile(r"\\frac\{[^{}]+\}\{[^{}]+\}")
SYM_RE = re.compile(r"\\pi|\\sqrt\{[^{}]+\}|\be\b|\\ln|\\sin|\\cos|\\tan|\\infty")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def read_record(rec, ev):
    sid = rec.get("sample_id") or rec.get("id")
    src_path = rec.get("source_path") or ev["records"].get(sid, {}).get("source", {}).get("path")
    line_no = rec.get("line_no") or ev["records"].get(sid, {}).get("source", {}).get("line")
    src = Path(str(src_path))
    if not src.is_absolute():
        src = ROOT / str(src_path)
    data = src.read_bytes()
    raw = data.splitlines(keepends=True)[line_no - 1]
    return sid, json.loads(raw.decode("utf-8")), raw


def main() -> int:
    batch = json.loads(BATCH.read_text(encoding="utf-8"))
    ev = json.loads(EV.read_text(encoding="utf-8"))
    records = batch.get("records") or batch.get("entries") or []
    rows = []
    for rec in records:
        sid, obj, raw = read_record(rec, ev)
        problem = obj.get("problem", "")
        solution = obj.get("solution", "")
        answer = obj.get("answer", "")
        steps = (obj.get("scene_spec") or {}).get("steps", []) or []

        items = []
        for label, text in [("problem", problem), ("solution", solution),
                            ("answer", answer)]:
            for m in DEC_RE.finditer(text):
                items.append({"kind": "decimal_literal", "value": m.group(),
                              "source": label, "position": m.start(),
                              "check": "须核验是否精确有理数;是→分数显示,否→原样",
                              "verdict": "PENDING_REVIEW"})
            for m in FRAC_TEXT_RE.finditer(text):
                items.append({"kind": "text_fraction", "value": m.group(),
                              "source": label, "position": m.start(),
                              "check": "文本分数,按精确值显示",
                              "verdict": "PENDING_REVIEW"})
            for m in FRAC_TEX_RE.finditer(text):
                items.append({"kind": "latex_frac", "value": m.group(),
                              "source": label, "position": m.start(),
                              "check": "LaTeX 分数,保留符号显示",
                              "verdict": "PENDING_REVIEW"})
            for m in SYM_RE.finditer(text):
                items.append({"kind": "symbolic", "value": m.group(),
                              "source": label, "position": m.start(),
                              "check": "符号/根式保留符号,不用近似值",
                              "verdict": "PENDING_REVIEW"})

        # 解答计算步骤:按句切分(仅作审核定位,不做数学断言)
        sent = [s.strip() for s in re.split(r"[。;；]", solution) if s.strip()]

        rows.append({
            "sample_id": sid,
            "raw_line_sha256": sha_bytes(raw),
            "decimal_literals": [i for i in items if i["kind"] == "decimal_literal"],
            "fractions": [i for i in items if i["kind"] in ("text_fraction", "latex_frac")],
            "symbolics": [i for i in items if i["kind"] == "symbolic"],
            "solution_steps": sent,
            "scene_steps_count": len(steps),
            "math_verdict": "PENDING_REVIEW",
            "note": "抽取为审核定位材料;精确性/几何/计算逐项判定由审核方给出,不自判",
        })

    out = HERE / "math-correspondence.jsonl"
    out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
                   encoding="utf-8")
    for r in rows:
        print(f"{r['sample_id']:24s} dec={len(r['decimal_literals'])} "
              f"frac={len(r['fractions'])} sym={len(r['symbolics'])} "
              f"sol_steps={len(r['solution_steps'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
