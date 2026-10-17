"""重建预演:在 .pipeline-tests/v3-preview 下生成 v3 场景 + 跑管线 v2,不碰 reviews/。

用法:python -B -X utf8 stage_check.py
"""
import importlib.util
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SUB = ROOT / "reviews/data-prep/2026-10-17-submission/asset-evidence"
CAND = SUB / "presentation-candidates"
TEMPLATE = SUB / "template-fix-candidate/render_templates_v3_candidate.py"
RECORDS = ROOT / "archives/reviews/codex-supervision/2026-10-17-first-batch-exact-math-review/candidate/records.jsonl"
SCRATCH = ROOT / ".pipeline-tests/v3-preview"

sys.path.insert(0, str(CAND))
import build_presentation_candidates as builder  # noqa: E402

if SCRATCH.exists():
    shutil.rmtree(SCRATCH, ignore_errors=True)
SCRATCH.mkdir(parents=True)

builder.HERE = SCRATCH
builder.SCENES = SCRATCH / "scenes"
builder.TEMPLATE_PATH = TEMPLATE
rc = builder.main()
print("builder rc =", rc)

# 管线参数化预演
spec = importlib.util.spec_from_file_location(
    "pp", SUB / "presentation-pipeline/pipeline.py")
pp = importlib.util.module_from_spec(spec)
sys.modules["pp"] = pp
spec.loader.exec_module(pp)

paths = pp.Paths(root=ROOT, cand=SCRATCH, bind=SCRATCH / "presentation-bindings.jsonl",
                 template=TEMPLATE, records=RECORDS, out=SCRATCH / "runs")
receipt = pp.build(paths, gate=lambda: (False, "preview: certificate not checked"))
print("status =", receipt["status"])
print("render =", receipt["stages"]["render"]["state"])
print("packs  =", receipt["stages"]["review_pack"]["packs"])
verdicts = pp.stage_verify(paths)
print("verify overall =", verdicts["overall"])

# 行尾断词复核
import render_templates_v3_candidate as tpl3  # noqa: E402
END = tpl3.ROW_END_PUNCT
mid = 0
rows_total = 0
for line in (SCRATCH / "presentation-bindings.jsonl").read_text(encoding="utf-8").splitlines():
    if not line.strip():
        continue
    row = json.loads(line)
    scene = (SCRATCH / "scenes" / f"{row['sample_id']}.py").read_text(encoding="utf-8")
    print(f"  {row['sample_id']:<26} sha={row['scene_sha256'][:12]} plan={row['plan_sha256'][:12]} "
          f"rows={row['plan_rows']} pages={row['plan_pages_provisional']} cov={row['coverage_ok']}")
print("preview dir =", SCRATCH)
