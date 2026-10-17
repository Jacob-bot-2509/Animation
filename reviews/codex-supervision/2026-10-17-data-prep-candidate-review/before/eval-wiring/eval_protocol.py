"""逐题隔离证据协议 harness —— 候选实现 v1(无模型,只接固定夹具)。

契约来源: docs/READINESS-EVIDENCE-PROTOCOL.md §6。
本文件是独立候选目录中的父进程侧实现,不改 eval_step.py/真实模型/真实超参。
默认拒绝:任何 executor/judge 的 sha256 未绑定进 request.json 即拒绝启动,
不执行任意脚本、不用 shell=True/字符串命令。

结构:
  build_request()   按 §6.2 生成 request.json(绑定 SHA 与固定题单)
  run_executor()    白名单绑定后以真实子进程启动 executor,采集真实 rc/stdout/stderr
  verify_response() 逐样本核对 §6.2 拒绝清单与真实文件/解码/哈希
  aggregate()       按 §6.3 计算 R/E/M/F,精确分数,分母锁定,未知不删分母
"""
from __future__ import annotations

import base64
import hashlib
import json
import subprocess
import sys
import time
from fractions import Fraction
from pathlib import Path

PROTOCOL_VERSION = "eval-evidence-v1"
REASON = str  # 仅用于类型标注可读性


def _sha(p: Path) -> str | None:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError:
        return None


def _sha_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def build_request(cfg: dict) -> dict:
    """request.json 合同键(§6.2):协议版本、身份、scope、双向 SHA 绑定、固定题单。"""
    req = {
        "protocol_version": PROTOCOL_VERSION,
        "run_id": cfg["run_id"],
        "round_id": cfg.get("round_id"),
        "candidate_id": cfg.get("candidate_id"),
        "scope": cfg.get("scope", "fixture-only-no-model"),
        "bindings": {
            "config_sha256": cfg["config_sha256"],
            "manifest_sha256": cfg["manifest_sha256"],
            "training_manifest_sha256": cfg.get("training_manifest_sha256"),
            "adapter_sha256": cfg.get("adapter_sha256"),
            "generated_specs_sha256": cfg["generated_specs_sha256"],
        },
        "evaluator_sources": cfg["evaluator_sources"],  # {name:{path,sha256,protocol_role}}
        "limits": cfg.get("limits", {"timeout_seconds": 30,
                                     "max_output_bytes": 64 * 1024 * 1024}),
        "fixed_questions": cfg["fixed_questions"],
    }
    return req


def verify_bindings(req: dict, work: Path) -> tuple[bool, str]:
    """启动前:executor 源 SHA 必须与绑定一致;generated_specs 文件 SHA 一致。"""
    for name, src in req["evaluator_sources"].items():
        p = (work / src["path"]).resolve()
        if not p.is_file():
            return False, f"evaluator source missing: {name} {src['path']}"
        if _sha(p) != src["sha256"]:
            return False, f"evaluator source drift: {name}"
    specs = work / "generated-specs.json"
    if _sha(specs) != req["bindings"]["generated_specs_sha256"]:
        return False, "generated_specs_sha256 mismatch"
    return True, ""


def _safe_artifact(work_root: Path, rel: str) -> Path | None:
    """拒绝根外路径/重解析点逃逸(最小实现:resolve 后必须仍在 work_root 内)。

    说明:完整 reparse-point 检测须按 witness_transfer_common.checked 的
    既有实现接入;本候选先用 resolve+前缀判定并如实标注局限。
    """
    if not isinstance(rel, str) or not rel:
        return None
    cand = (work_root / rel).resolve()
    root = work_root.resolve()
    if cand != root and root not in cand.parents:
        return None
    return cand


def _decode_media(p: Path) -> tuple[bool, str]:
    """真实完整解码校验:PNG 用 PIL;其他类型如实 UNVERIFIED(不猜)。"""
    try:
        from PIL import Image  # noqa: PLC0415
    except ImportError:
        return False, "PIL unavailable"
    try:
        with Image.open(p) as im:
            im.load()
            if im.size[0] <= 0 or im.size[1] <= 0:
                return False, "empty dimensions"
        return True, f"png {im.size[0]}x{im.size[1]}"
    except Exception as exc:  # noqa: BLE001 解码失败须如实记为 FAIL
        return False, f"decode failed: {exc.__class__.__name__}"


def verify_response(req: dict, work: Path, resp: list[dict],
                    real_rc: int, timed_out: bool) -> dict:
    """逐样本核对:身份/绑定/产物/解码/rc 真实性;父进程重算,不信自报 VERIFIED。"""
    fixed = {frozenset(q["identity"].items()): q for q in req["fixed_questions"]}
    seen: set = set()
    lines: list[dict] = []
    problems: list[dict] = []

    def prob(identity, code, detail):
        problems.append({"identity": identity, "code": code, "detail": detail})

    for line in resp:
        ident = line.get("identity")
        if not isinstance(ident, dict) or frozenset(ident.items()) not in fixed:
            prob(ident, "EXTRA_OR_UNKNOWN_IDENTITY", "identity not in fixed question list")
            continue
        key = frozenset(ident.items())
        if key in seen:
            prob(ident, "DUPLICATE_IDENTITY", "duplicate receipt line")
            # 协议违例:首个有效行一并作废,该题按缺证据处理
            for prev in lines:
                if frozenset((prev.get("identity") or {}).items()) == key \
                        and not prev.get("_rejected"):
                    prev["_rejected"] = True
            line = {**line, "_rejected": True}
            lines.append(line)
            continue
        seen.add(key)
        q = fixed[key]

        # rc 真实性:子进程自报 rc 与真实 returncode 不一致 → 拒绝该行(字符串伪造 rc 同样拒绝)
        rc = line.get("rc")
        if not isinstance(rc, int) or isinstance(rc, bool):
            prob(ident, "RC_NOT_INT_OR_BOOL_IMPERSONATION", f"rc={rc!r}")
            line = {**line, "_rejected": True}
            lines.append(line)
            continue
        if rc != real_rc:
            prob(ident, "RC_MISMATCH_REAL_PROCESS", f"claimed={rc} real={real_rc}")
            line = {**line, "_rejected": True}
            lines.append(line)
            continue

        # 输入绑定:回执引用的输入/生成 spec SHA 必须与 request 一致(输入漂移拒绝)
        ib = line.get("input_bindings") or {}
        if ib.get("generated_spec_sha256") != q.get("generated_spec_sha256"):
            prob(ident, "SPEC_DRIFT", "generated spec sha mismatch")
            line = {**line, "_rejected": True}
            lines.append(line)
            continue

        # 产物核验:路径在根内、文件存在、SHA 一致、解码真实。
        # 空产物/解码失败 = 产物不合格 → 强制 render FAIL(不拒行);
        # 路径逃逸/SHA 不一致 = 完整性违例 → 拒行。
        artifacts = line.get("artifacts") or []
        checked: list[dict] = []
        render_force_fail = False
        for art in artifacts:
            p = _safe_artifact(work, art.get("path"))
            if p is None or not p.is_file():
                prob(ident, "ARTIFACT_PATH_ESCAPE_OR_MISSING", str(art.get("path")))
                line = {**line, "_rejected": True}
                break
            if _sha(p) != art.get("sha256"):
                prob(ident, "ARTIFACT_SHA_MISMATCH", str(art.get("path")))
                line = {**line, "_rejected": True}
                break
            if p.stat().st_size == 0:
                prob(ident, "ARTIFACT_EMPTY", str(art.get("path")))
                render_force_fail = True
                checked.append({"path": art["path"], "sha256": art["sha256"],
                                "decode_ok": False, "decode_detail": "empty file"})
                continue
            ok, msg = _decode_media(p)
            if not ok:
                prob(ident, "ARTIFACT_DECODE_FAIL", str(art.get("path")))
                render_force_fail = True
            checked.append({"path": art["path"], "sha256": art["sha256"],
                            "decode_ok": ok, "decode_detail": msg})
        if line.get("_rejected"):
            lines.append(line)
            continue
        line = {**line, "_artifacts_checked": checked}
        if render_force_fail and (line.get("render") or {}).get("decision") == "PASS":
            line["render"] = {**line.get("render", {}), "decision": "FAIL",
                              "reason_code": "ARTIFACT_EMPTY_OR_UNDECODABLE"}

        # 数学断言覆盖:回执须逐条覆盖题单全部必需断言(id+布尔 verdict+理由),PASS 须全真
        required_asserts = q.get("assertions") or []
        math = line.get("math") or {}
        if math.get("decision") == "PASS":
            got = {a.get("id"): a for a in (math.get("assertions") or [])}
            missing = [a["id"] for a in required_asserts
                       if a["id"] not in got or not isinstance(got[a["id"]].get("verdict"), bool)
                       or not str(got[a["id"]].get("reason", "")).strip()]
            false_verdicts = [a["id"] for a in required_asserts
                              if a["id"] in got and got[a["id"]].get("verdict") is False]
            if missing or false_verdicts:
                prob(ident, "MATH_ASSERTION_UNVERIFIED_OR_FALSE",
                     f"missing/undecided={missing} false={false_verdicts}")
                math = {**math, "decision": "UNVERIFIED" if missing else "FAIL"}

        # rc0 无产物:任何 stage 自报 PASS 但无对应产物 → 该 stage 强制 FAIL
        render = line.get("render") or {}
        if rc == 0 and not checked and render.get("decision") == "PASS":
            prob(ident, "RC0_NO_ARTIFACT", "PASS claimed with no artifacts")
            render = {**render, "decision": "FAIL", "reason_code": "RC0_NO_ARTIFACT"}

        line = {**line, "render": render, "_parent_note":
                "parent re-verified artifacts; self-reported VERIFIED is never trusted"}
        lines.append(line)

    for key, q in fixed.items():
        if key not in seen:
            prob(dict(q["identity"]), "MISSING_IDENTITY", "no receipt line for fixed question")
            lines.append({"identity": dict(q["identity"]), "_missing": True})
    return {"lines": lines, "problems": problems,
            "real_rc": real_rc, "timed_out": timed_out}


def run_executor(req: dict, work: Path, exe_name: str) -> tuple[list[dict], int, bool, str, str]:
    """白名单绑定后真实子进程启动;返回(回执行, 真实 rc, 是否超时, stdout, stderr)。"""
    src = req["evaluator_sources"][exe_name]
    exe = (work / src["path"]).resolve()
    limits = req["limits"]
    try:
        cp = subprocess.run(
            [sys.executable, "-X", "utf8", str(exe),
             "--request", str(work / "request.json"), "--work", str(work)],
            capture_output=True, cwd=work,
            timeout=limits.get("timeout_seconds", 30))
        stdout, stderr = cp.stdout.decode("utf-8", "replace"), cp.stderr.decode("utf-8", "replace")
        resp_path = work / "response-index.jsonl"
        rows = ([json.loads(x) for x in resp_path.read_text(encoding="utf-8").splitlines()
                 if x.strip()] if resp_path.is_file() else [])
        return rows, cp.returncode, False, stdout, stderr
    except subprocess.TimeoutExpired as exc:
        return [], -1, True, exc.stdout.decode("utf-8", "replace") if exc.stdout else "", \
            (exc.stderr.decode("utf-8", "replace") if exc.stderr else "timeout")


def schema_ok(spec: dict) -> bool:
    """可执行率分量:scene_spec 满足入场契约(objects/steps 非空字符串列表)。"""
    if not isinstance(spec, dict):
        return False
    for key in ("objects", "steps"):
        v = spec.get(key)
        if not isinstance(v, list) or not v:
            return False
        if any(not isinstance(x, str) or not x.strip() for x in v):
            return False
    return True


def question_metrics(req: dict, verified: dict, specs_by_identity: dict) -> dict:
    """按 §6.3:Q_s 分母锁定(按 split+problem_id 计题),S_q=题内全部必需样本;
    任意必需样本失败→该题失败,缺证据→该题 UNVERIFIED。"""
    qs = req["fixed_questions"]
    by_q = {}
    for line in verified["lines"]:
        ident = line.get("identity")
        if not isinstance(ident, dict):
            continue
        key = frozenset(ident.items())
        by_q.setdefault(key, []).append(line)
    q_groups: dict = {}
    for q in qs:
        gkey = (q["identity"]["split"], q["identity"]["problem_id"])
        q_groups.setdefault(gkey, []).append(q)

    q_rows = []
    for gkey, members in q_groups.items():
        lines: list[dict] = []
        missing = False
        for q in members:
            key = frozenset(q["identity"].items())
            ls = by_q.get(key, [])
            if not ls or any(x.get("_missing") or x.get("_rejected") for x in ls):
                missing = True
                continue
            lines.extend(ls)
        specs = []
        for q in members:
            key = frozenset(q["identity"].items())
            specs.extend(specs_by_identity.get(key, []))
        schema_all_ok = bool(specs) and all(schema_ok(s) for s in specs)
        question = {"split": gkey[0], "problem_id": gkey[1]}
        if missing or not lines:
            q_rows.append({"question": question, "status": "UNVERIFIED",
                           "reason": "missing or rejected receipt",
                           "render": "UNVERIFIED", "executable": "UNVERIFIED",
                           "math": "UNVERIFIED", "fidelity": "UNVERIFIED"})
            continue
        render_ok = all((x.get("render") or {}).get("decision") == "PASS" for x in lines)
        exec_ok = all((x.get("executable") or {}).get("decision") == "PASS" for x in lines)

        def stage_value(name):
            """缺失块/UNVERIFIED → 该题 UNVERIFIED;全 PASS → PASS;否则 FAIL。"""
            decs = [(x.get(name) or {}).get("decision") for x in lines]
            if any(d is None or d == "UNVERIFIED" for d in decs):
                return "UNVERIFIED"
            return "PASS" if all(d == "PASS" for d in decs) else "FAIL"

        math_v = stage_value("math")
        fid_v = stage_value("fidelity")
        executable = "PASS" if (schema_all_ok and exec_ok and render_ok) else "FAIL"
        q_rows.append({"question": question, "status": "PASS" if render_ok else "FAIL",
                       "render": "PASS" if render_ok else "FAIL",
                       "executable": executable,
                       "math": math_v,
                       "fidelity": fid_v})
    return q_rows


def aggregate(req: dict, verified: dict, specs_by_identity: dict | None = None) -> dict:
    """§6.3 汇总:精确分数;N=0 或任一题未知 → 该指标整体 UNVERIFIED、rate=null;E⊆R 校验。"""
    qs = req["fixed_questions"]
    q_rows = question_metrics(req, verified, specs_by_identity or {})
    splits = sorted({q["identity"]["split"] for q in qs})

    def metric(name):
        rows = [r for r in q_rows if r.get(name) == "PASS"]
        unknown = [r for r in q_rows if r.get(name) == "UNVERIFIED"]
        n = len(q_rows)
        if n == 0 or unknown:
            return {"status": "UNVERIFIED", "passed": len(rows), "total": n,
                    "rate": None, "unknown": len(unknown),
                    "covered_total": n - len(unknown), "covered_passed": len(rows)}
        return {"status": "VERIFIED", "passed": len(rows), "total": n,
                "rate": str(Fraction(len(rows), n)), "unknown": 0}

    # E 的 PASS 集必须是 R 的子集(§6.3)
    r_ids = {frozenset(r["question"].items()) for r in q_rows if r["render"] == "PASS"}
    e_ids = {frozenset(r["question"].items()) for r in q_rows if r.get("executable") == "PASS"}
    e_subset_ok = e_ids <= r_ids

    by_split = {}
    for sp in splits:
        sp_rows = [r for r in q_rows if r["question"]["split"] == sp]
        by_split[sp] = {
            "total_questions": len(sp_rows),
            "render": _split_metric(sp_rows, "render"),
            "executable": _split_metric(sp_rows, "executable"),
            "math": _split_metric(sp_rows, "math"),
            "fidelity": _split_metric(sp_rows, "fidelity"),
        }
    return {
        "protocol_version": PROTOCOL_VERSION,
        "total_questions": len(q_rows),
        "by_split": by_split,
        "render": metric("render"),
        "executable": metric("executable"),
        "math": metric("math"),
        "fidelity": metric("fidelity"),
        "e_subset_of_r": e_subset_ok,
        "rejected_receipts": len(verified["problems"]),
        "problems": verified["problems"],
    }


def _split_metric(rows: list[dict], name: str) -> dict:
    passed = sum(1 for r in rows if r.get(name) == "PASS")
    unknown = sum(1 for r in rows if r.get(name) == "UNVERIFIED")
    n = len(rows)
    if n == 0 or unknown:
        return {"status": "UNVERIFIED", "passed": passed, "total": n,
                "rate": None, "unknown": unknown}
    return {"status": "VERIFIED", "passed": passed, "total": n,
            "rate": str(Fraction(passed, n)), "unknown": 0}


def run_harness(cfg: dict, work: Path) -> dict:
    """主入口:绑定校验 → 写 request → 启动子进程 → 逐样本核验 → 汇总。"""
    work.mkdir(parents=True, exist_ok=True)
    req = build_request(cfg)
    (work / "request.json").write_text(
        json.dumps(req, ensure_ascii=False, indent=2), encoding="utf-8")
    ok, why = verify_bindings(req, work)
    if not ok:
        return {"status": "REFUSED", "reason": why, "request": str(work / "request.json")}
    rows, rc, timed_out, stdout, stderr = run_executor(req, work, "render_executor")
    (work / "executor.stdout.txt").write_text(stdout, encoding="utf-8")
    (work / "executor.stderr.txt").write_text(stderr, encoding="utf-8")
    verified = verify_response(req, work, rows, rc, timed_out)
    specs_file = work / "generated-specs.json"
    specs_by_identity: dict = {}
    if specs_file.is_file():
        for s in json.loads(specs_file.read_text(encoding="utf-8")):
            ident = {k: s[k] for k in ("split", "problem_id", "sample_id", "row_index")
                     if k in s}
            specs_by_identity.setdefault(frozenset(ident.items()), []).append(s.get("spec"))
    report = aggregate(req, verified, specs_by_identity)
    report.update({
        "run_id": req["run_id"],
        "real_rc": rc,
        "timed_out": timed_out,
        "executor_stdout_sha256": _sha(work / "executor.stdout.txt"),
        "executor_stderr_sha256": _sha(work / "executor.stderr.txt"),
        "request_sha256": _sha(work / "request.json"),
    })
    (work / "eval-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


# ---- 夹具用工具(仅 fixture 场景使用,不参与正式协议路径) ----

TINY_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGP4z8DwHwAFAAH/q842iQAAAABJRU5ErkJggg==")


def write_artifact(work: Path, rel: str, data: bytes) -> str:
    p = work / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
    return hashlib.sha256(data).hexdigest()
