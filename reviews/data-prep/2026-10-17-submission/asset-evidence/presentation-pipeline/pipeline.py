"""动画呈现管线 harness(候选 v1,阶段机,fail-closed)。

阶段:
  generate   呈现候选生成(输入 presentation-candidates/,校验存在+SHA)
  render     真实渲染 —— 默认 REFUSE;仅当 exec 证据文件存在且绑定一致才允许
             (exec_isolation 未验收前一律拒绝,不绕过)
  review-pack 审核包组装:场景代码+原题+三选一结论单(过/不过/要改),供
             Codex 数学/质量复核与用户全量目视
  receipt    管线运行回执(每阶段实际状态,不伪造)

真实渲染与审核判定不在本管线内自证;结论单为空表,等审核方填写。
"""
import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
CAND = HERE.parent / "presentation-candidates"
BIND = CAND / "presentation-bindings.jsonl"
EXEC_EVIDENCE = ROOT / "data" / "execution_evidence.json"
OUT = HERE / "runs"


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def stage_generate() -> list[dict]:
    if not BIND.is_file():
        raise RuntimeError("presentation-bindings.jsonl missing")
    rows = [json.loads(x) for x in BIND.read_text(encoding="utf-8").splitlines() if x.strip()]
    for r in rows:
        p = CAND / "scenes" / f"{r['sample_id']}.py"
        if not p.is_file():
            raise RuntimeError(f"scene missing: {r['sample_id']}")
        if sha_bytes(p.read_bytes()) != r["scene_sha256"]:
            raise RuntimeError(f"scene sha mismatch: {r['sample_id']}")
    return rows


def stage_render(rows: list[dict]) -> str:
    """渲染阶段:exec 证据缺失即 REFUSE;不伪造、不旁路。"""
    if not EXEC_EVIDENCE.is_file():
        return "REFUSED_EXEC_EVIDENCE_MISSING"
    ev = json.loads(EXEC_EVIDENCE.read_text(encoding="utf-8"))
    if ev.get("schema") != "production-appcontainer-v2" or \
            ev.get("fs_isolation") != "private_per_run":
        return "REFUSED_UNSUPPORTED_CONTRACT"
    return "ALLOWED_BY_EVIDENCE_PRESENT"  # 真实渲染执行仍另需获准入口


def stage_review_pack(rows: list[dict], render_state: str) -> list[dict]:
    packs = []
    for r in rows:
        d = OUT / "review-packs" / r["sample_id"]
        d.mkdir(parents=True, exist_ok=False)
        shutil.copyfile(CAND / "scenes" / f"{r['sample_id']}.py", d / "scene.py")
        (d / "conclusion-sheet.md").write_text(
            "# 目视审核结论单\n\n"
            f"- sample_id: {r['sample_id']}\n"
            "- 渲染状态: " + render_state + "\n"
            "- 审核结论(三选一,待审核方填写):\n"
            "  - [ ] 过\n"
            "  - [ ] 不过\n"
            "  - [ ] 要改\n"
            "- 修改意见(若要改,必填):\n\n"
            "- 审核人:\n"
            "- 时间:\n", encoding="utf-8")
        (d / "bindings.json").write_text(json.dumps(
            {"sample_id": r["sample_id"],
             "corrected_record_sha256": r["corrected_record_sha256"],
             "scene_sha256": r["scene_sha256"],
             "coverage_ok": r["coverage_ok"],
             "render_state": render_state}, ensure_ascii=False, indent=2),
            encoding="utf-8")
        packs.append({"sample_id": r["sample_id"], "pack_dir": str(d.relative_to(HERE))})
    return packs


def main() -> int:
    rows = stage_generate()
    render_state = stage_render(rows)
    packs = stage_review_pack(rows, render_state)
    receipt = {
        "stages": {
            "generate": {"state": "PASS", "records": len(rows)},
            "render": {"state": render_state},
            "review_pack": {"state": "PASS", "packs": len(packs)},
        },
        "packs": packs,
        "note": "结论单为空表待审核方填写;渲染状态如实记录,不伪造",
    }
    (OUT / "pipeline-receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
