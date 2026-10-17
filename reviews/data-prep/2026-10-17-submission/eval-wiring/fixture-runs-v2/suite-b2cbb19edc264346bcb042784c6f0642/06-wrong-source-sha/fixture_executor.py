"""夹具子进程模拟器(fixture 专用,不是真实渲染/判定器)。

按 work/scenario.json 的 prescribed 规则,对 request.json 的固定题单
逐题发出回执(response-index.jsonl)+ 产物,并用规定 rc 退出。
覆盖 READINESS-EVIDENCE-PROTOCOL §6.4 最小夹具清单。
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import sys
import time
from pathlib import Path

# 内联夹具 PNG(与 eval_protocol.TINY_PNG 同字节),避免跨目录 import
TINY_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGP4z8DwHwAFAAH/q842iQAAAABJRU5ErkJggg==")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def emit(request: dict, work: Path, sc: dict) -> int:
    questions = request["fixed_questions"]
    lines: list[dict] = []
    seen: set = set()
    for q in questions:
        ident = dict(q["identity"])
        key = frozenset(ident.items())
        if key in seen:
            # duplicate_id 场景:同一身份发两行
            pass
        seen.add(key)

        # missing_id 场景:跳过指定身份
        if sc.get("missing_identity") and ident == sc["missing_identity"]:
            continue

        render_fail = None
        if sc.get("fail_render_identity") and ident == sc["fail_render_identity"]:
            render_fail = sc["fail_render_mode"]  # corrupted / empty / no_artifact
        if sc.get("timeout"):
            time.sleep(sc["timeout"])
            return 0

        art_path = f"artifacts/{ident['problem_id']}-{ident['row_index']}.png"
        if render_fail == "corrupted":
            data = b"not-a-png" * 20
            sha = sha_bytes(data)
            (work / art_path).parent.mkdir(parents=True, exist_ok=True)
            (work / art_path).write_bytes(data)
        elif render_fail == "empty":
            data = b""
            sha = sha_bytes(data)
            (work / art_path).parent.mkdir(parents=True, exist_ok=True)
            (work / art_path).write_bytes(data)
        elif render_fail == "no_artifact":
            art_path = None
            sha = None
        elif sc.get("path_escape"):
            art_path = "../escape.png"
            data = TINY_PNG
            sha = sha_bytes(data)
            (work.parent / "escape.png").write_bytes(data)
        else:
            data = TINY_PNG
            sha = sha_bytes(data)
            (work / art_path).parent.mkdir(parents=True, exist_ok=True)
            (work / art_path).write_bytes(data)

        render_decision = "FAIL" if render_fail else "PASS"
        rc = sc.get("rc", 0)
        if sc.get("rc_is_bool"):
            rc = True
        if sc.get("rc_forgery"):
            rc = 0  # 回执自报 0,但进程真实退出 3

        math_decision = sc.get("math_decision", "PASS")
        if sc.get("math_false_identity") and ident == sc["math_false_identity"]:
            math_decision = "FAIL"
        if sc.get("math_undecided_identity") and ident == sc["math_undecided_identity"]:
            math_decision = "UNVERIFIED"
        math_assertions = [
            {**a, "verdict": True if math_decision == "PASS" else
             (None if math_decision == "UNVERIFIED" else False),
             "reason": "fixture-reason" if math_decision != "UNVERIFIED" else ""}
            for a in q.get("assertions", [])
        ]

        line = {
            "identity": ident,
            "input_bindings": {
                "input_record_sha256": q.get("input_record_sha256"),
                "generated_spec_sha256": q["generated_spec_sha256"]
                if not (sc.get("spec_drift") and ident == sc["spec_drift_identity"])
                else "f" * 64,
            },
            "rc": rc,
            "render": {"decision": render_decision,
                       "reason_code": render_fail or "OK"},
            "executable": {"decision": "PASS" if (render_decision == "PASS" and
                           sc.get("exec_fail_identity") != ident) else "FAIL",
                           "reason_code": "FIXTURE_SANDBOX_OK" if render_decision == "PASS" else "NO_ARTIFACT_CHAIN"},
            "artifacts": ([] if art_path is None else
                          [{"path": art_path, "sha256": sha, "media_type": "image/png"}]),
            "math": {"decision": math_decision,
                     "assertions": math_assertions},
        }
        # fidelity 场景:fidelity_missing 时整块缺失
        if not sc.get("fidelity_missing"):
            line["fidelity"] = {"decision": "PASS" if not sc.get("fidelity_fail") else "FAIL",
                                "checklist": q.get("fidelity_checklist", [])}
        lines.append(line)

    if sc.get("extra_identity"):
        lines.append({"identity": sc["extra_identity"],
                      "rc": 0, "render": {"decision": "PASS"}, "artifacts": []})
    if sc.get("duplicate_identity"):
        dup = [x for x in lines if x.get("identity") == sc["duplicate_identity"]]
        if dup:
            lines.append(json.loads(json.dumps(dup[0])))

    (work / "response-index.jsonl").write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in lines) + "\n",
        encoding="utf-8")
    if sc.get("rc_forgery"):
        return 3
    return sc.get("rc", 0)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--request", required=True)
    ap.add_argument("--work", required=True)
    args = ap.parse_args(argv)
    work = Path(args.work)
    request = json.loads(Path(args.request).read_text(encoding="utf-8"))
    sc = json.loads((work / "scenario.json").read_text(encoding="utf-8"))
    return emit(request, work, sc)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
