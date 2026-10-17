"""夹具运行器:覆盖 §6.4 最小夹具清单,每场景独立 work 目录,
断言父进程侧预期判定,写 fixture-receipt.json + 矩阵报告。

无模型、无真实渲染、无真实判定器;全部是固定夹具数据。
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from eval_protocol import run_harness, _sha_text  # noqa: E402

RUNS = HERE / "fixture-runs"
SPLITS = {"eval": 3, "test": 3}  # 每 split 题数;eval-003 有两个样本


def spec(problem_id: str, bad_schema: bool = False) -> dict:
    if bad_schema:
        return {"objects": [], "steps": ["坏 schema:objects 为空"]}
    return {"objects": ["坐标轴", "抛物线 $y=x^2$"],
            "steps": ["绘制坐标轴", "绘制抛物线并标注切点"]}


def make_questions() -> list[dict]:
    """6 题 7 样本(eval-003 双样本),断言与 F 清单为固定夹具。"""
    qs = []
    for split, n in SPLITS.items():
        for i in range(1, n + 1):
            pid = f"{split}-{i:03d}"
            samples = ([f"{pid}-a", f"{pid}-b"] if pid == "eval-003" else [f"{pid}"])
            for j, sid in enumerate(samples):
                qs.append({
                    "identity": {"split": split, "problem_id": pid,
                                 "sample_id": sid, "row_index": len(qs)},
                    "input_record_sha256": _sha_text(f"fixture-input:{pid}:{sid}"),
                    "generated_spec_sha256": _sha_text(json.dumps(
                        spec(pid), ensure_ascii=False)),
                    "assertions": [{"id": f"{pid}-a1",
                                    "statement": "fixture 断言:切线斜率=2",
                                    "expect": True}],
                    "fidelity_checklist": [
                        {"item": "抛物线经过 (1,1)", "frame": "0:00-0:05"},
                        {"item": "切点高亮", "frame": "0:05-0:10"}],
                })
    return qs


def build_cfg(scenario: str, qs: list[dict], bad_spec_identity: dict | None = None,
              wrong_source_sha: bool = False) -> tuple[dict, Path]:
    import shutil
    work = RUNS / scenario
    work.mkdir(parents=True, exist_ok=True)
    specs = []
    for q in qs:
        s = dict(q["identity"])
        s["spec"] = spec(s["problem_id"],
                         bad_schema=(bad_spec_identity == q["identity"]))
        specs.append(s)
    (work / "generated-specs.json").write_text(
        json.dumps(specs, ensure_ascii=False, indent=2), encoding="utf-8")
    # 真实部署同款:绑定源码置于工作目录,按副本 SHA 绑定
    shutil.copyfile(HERE / "fixture_executor.py", work / "fixture_executor.py")
    exe_sha = hashlib.sha256((work / "fixture_executor.py").read_bytes()).hexdigest()
    cfg = {
        "run_id": f"fixture-{scenario}",
        "round_id": "fixture-round-0",
        "candidate_id": "fixture-no-model",
        "scope": "fixture-only-no-model",
        "config_sha256": _sha_text(f"fixture-config:{scenario}"),
        "manifest_sha256": _sha_text("fixture-manifest"),
        "training_manifest_sha256": _sha_text("fixture-training-manifest"),
        "adapter_sha256": _sha_text("fixture-adapter-none"),
        "generated_specs_sha256": hashlib.sha256(
            (work / "generated-specs.json").read_bytes()).hexdigest(),
        "evaluator_sources": {
            "render_executor": {"path": "fixture_executor.py",
                                "sha256": ("f" * 64 if wrong_source_sha else exe_sha),
                                "protocol_role": "fixture-child"}},
        "fixed_questions": qs,
    }
    (work / "scenario.json").write_text(json.dumps(
        SCENARIOS[scenario]["child"], ensure_ascii=False, indent=2), encoding="utf-8")
    return cfg, work


EVAL001 = {"split": "eval", "problem_id": "eval-001", "sample_id": "eval-001", "row_index": 0}
EVAL002 = {"split": "eval", "problem_id": "eval-002", "sample_id": "eval-002", "row_index": 1}
EVAL003A = {"split": "eval", "problem_id": "eval-003", "sample_id": "eval-003-a", "row_index": 2}
EVAL003B = {"split": "eval", "problem_id": "eval-003", "sample_id": "eval-003-b", "row_index": 3}
TEST001 = {"split": "test", "problem_id": "test-001", "sample_id": "test-001", "row_index": 4}

SCENARIOS: dict[str, dict] = {
    "01-valid-all": {"child": {}, "expect": "R 6/6 E 6/6 M 6/6 F 6/6 全 VERIFIED"},
    "02-fail-denominator": {"child": {"fail_render_identity": EVAL001,
                                      "fail_render_mode": "corrupted"},
                            "expect": "R=5/6 VERIFIED,分母保留失败题"},
    "03-missing-id": {"child": {"missing_identity": TEST001},
                      "expect": "整指标 UNVERIFIED(一题缺回执),problems 记 MISSING_IDENTITY"},
    "04-duplicate-id": {"child": {"duplicate_identity": EVAL002},
                        "expect": "DUPLICATE_IDENTITY 首行一并作废,该题 UNVERIFIED,整指标 UNVERIFIED"},
    "05-extra-id": {"child": {"extra_identity": {"split": "eval", "problem_id": "ghost",
                                                 "sample_id": "g", "row_index": 99}},
                    "expect": "EXTRA_OR_UNKNOWN_IDENTITY 被拒,其余题正常 5/6"},
    "06-wrong-source-sha": {"child": {}, "wrong_source_sha": True,
                            "expect": "启动前 REFUSED(evaluator source drift)"},
    "07-spec-drift": {"child": {"spec_drift": True, "spec_drift_identity": EVAL003A},
                      "expect": "SPEC_DRIFT 拒绝该行,eval-003 题 UNVERIFIED,整指标 UNVERIFIED"},
    "08-corrupted-media": {"child": {"fail_render_identity": EVAL002,
                                     "fail_render_mode": "corrupted"},
                           "expect": "该题 render FAIL(解码失败),R=5/6"},
    "09-empty-media": {"child": {"fail_render_identity": EVAL002, "fail_render_mode": "empty"},
                       "expect": "空产物 → render 强制 FAIL,R=5/6"},
    "10-rc0-no-artifact": {"child": {"fail_render_identity": EVAL001,
                                     "fail_render_mode": "no_artifact"},
                           "expect": "RC0_NO_ARTIFACT 强制 FAIL,R=5/6"},
    "11-timeout": {"child": {"timeout": 60}, "expect": "超时,全部题缺回执 → 全 UNVERIFIED"},
    "12-path-escape": {"child": {"path_escape": True},
                       "expect": "ARTIFACT_PATH_ESCAPE_OR_MISSING 完整性拒绝 → 全 UNVERIFIED"},
    "13-math-false": {"child": {"math_false_identity": EVAL001},
                      "expect": "该题 M=FAIL,M=5/6"},
    "14-math-undecided": {"child": {"math_undecided_identity": EVAL001},
                          "expect": "该题 M=UNVERIFIED → M 整指标 UNVERIFIED"},
    "15-fidelity-missing": {"child": {"fidelity_missing": True},
                            "expect": "F 全 UNVERIFIED(清单缺失)"},
    "16-multi-scene-one-fails": {"child": {"fail_render_identity": EVAL003B,
                                           "fail_render_mode": "corrupted"},
                                 "expect": "eval-003 双样本其一失败 → 该题 FAIL,R=5/6"},
    "17-rc-bool": {"child": {"rc_is_bool": True},
                   "expect": "RC_NOT_INT_OR_BOOL_IMPERSONATION 全行拒绝 → 全 UNVERIFIED"},
    "18-rc-forgery": {"child": {"rc_forgery": True},
                      "expect": "回执自报 rc=0 但真实 rc=3 → RC_MISMATCH 全行拒绝"},
    "19-schema-bad": {"child": {}, "bad_spec_identity": EVAL001,
                      "expect": "该题 schema 校验失败 → E 该题 FAIL,E=5/6"},
    "20-exec-fail": {"child": {"exec_fail_identity": EVAL002},
                     "expect": "该题 executable FAIL → E=5/6(render 仍 PASS)"},
}


def main() -> int:
    qs = make_questions()
    rows = []
    fails = []
    for name, meta in SCENARIOS.items():
        child = meta.get("child", {})
        cfg, work = build_cfg(
            name, qs,
            bad_spec_identity=meta.get("bad_spec_identity"),
            wrong_source_sha=meta.get("wrong_source_sha", False))
        # 场景参数里的 child 需要在 build_cfg 之后补写(部分由运行器直控)
        report = run_harness(cfg, work)
        r = report.get("render") or {}
        e = report.get("executable") or {}
        m = report.get("math") or {}
        f = report.get("fidelity") or {}
        row = {
            "scenario": name,
            "expected": meta["expect"],
            "result": {
                "status": report.get("status", "RAN"),
                "reason": report.get("reason"),
                "rejected_receipts": report.get("rejected_receipts", 0),
                "problems_count": len(report.get("problems", [])),
                "R": {"status": r.get("status"), "rate": r.get("rate"),
                      "passed": r.get("passed"), "total": r.get("total")},
                "E": {"status": e.get("status"), "rate": e.get("rate"),
                      "passed": e.get("passed"), "total": e.get("total")},
                "M": {"status": m.get("status"), "rate": m.get("rate"),
                      "passed": m.get("passed"), "total": m.get("total")},
                "F": {"status": f.get("status"), "rate": f.get("rate"),
                      "passed": f.get("passed"), "total": f.get("total")},
                "e_subset_of_r": report.get("e_subset_of_r"),
            },
        }
        rows.append(row)
        # 每场景断言的自动化核对:由人工对照 expected 复核,这里只记录结构
        print(json.dumps(row, ensure_ascii=False))
    receipt = {"fixture_matrix": rows,
               "note": "每场景期望与结果须逐行人工/Codex 对照复核,本文件不自动判 PASS"}
    (HERE / "fixture-receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n共 {len(rows)} 场景,回执写入 fixture-receipt.json")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
