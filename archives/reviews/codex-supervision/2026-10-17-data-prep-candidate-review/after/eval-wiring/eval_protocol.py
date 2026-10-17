"""Fixed-fixture evidence diagnostics. Never a production evaluator or judge."""
from __future__ import annotations
import base64, hashlib, json, os, re, stat, subprocess, sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURE_ROOT = HERE / "fixture-runs-v2"
PROTOCOL_VERSION = "eval-fixture-diagnostics-v2"
# Pin the independently read executor, not a hash chosen by a request.
APPROVED_FIXTURE_SHA256 = "b0f75a2407b5997d6e92037560d33653d43fd22ad932c194073c90e4a000038c"
IDENTITY_KEYS = ("split", "problem_id", "sample_id", "row_index")
METRICS = ("render", "executable", "math", "fidelity")
MAX_BYTES = 1048576

def _sha(p):
    try:
        with Path(p).open("rb") as f:
            return hashlib.file_digest(f, "sha256").hexdigest()
    except OSError:
        return None

def _sha_text(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def _identity(value):
    if not isinstance(value, dict) or set(value) != set(IDENTITY_KEYS):
        raise ValueError("INVALID_IDENTITY")
    if value["split"] not in ("eval", "test") or type(value["row_index"]) is not int or value["row_index"] < 0:
        raise ValueError("INVALID_IDENTITY")
    if any(not isinstance(value[k], str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}", value[k])
           for k in ("problem_id", "sample_id")):
        raise ValueError("INVALID_IDENTITY")
    return tuple(value[k] for k in IDENTITY_KEYS)

def _no_reparse(p):
    p = Path(os.path.abspath(p))
    for part in list(reversed(p.parents)) + [p]:
        try:
            info = os.lstat(part)
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 1024:
            raise ValueError("REPARSE_POINT")
    return p

def _safe_artifact(root, rel):
    try:
        if not isinstance(rel, str) or not rel or ":" in rel or "\\" in rel:
            return None
        q = Path(rel)
        if q.is_absolute() or any(x in ("..", ".") for x in q.parts):
            return None
        base = _no_reparse(root)
        p = _no_reparse(base / q)
        if p == base or not p.is_relative_to(base):
            return None
        return p
    except (ValueError, OSError):
        return None

def _read_json(p):
    p = _no_reparse(p)
    if not p.is_file() or p.stat().st_size > MAX_BYTES:
        raise ValueError("JSON_SIZE_OR_MISSING")
    return json.loads(p.read_text(encoding="utf-8"))

def _check_work(work):
    root = _no_reparse(FIXTURE_ROOT)
    work = _no_reparse(work)
    if work == root or not work.is_relative_to(root):
        raise ValueError("FIXTURE_WORK_ROOT_ONLY")
    for parent in [work] + list(work.parents):
        if (parent / "delivery-manifest.json").exists():
            raise ValueError("FROZEN_DIRECTORY")
    return work

def build_request(cfg):
    if cfg.get("scope") != "fixture-only-no-model":
        raise ValueError("FIXTURE_SCOPE_ONLY")
    return {"protocol_version": PROTOCOL_VERSION, "scope": cfg["scope"],
            "run_id": cfg["run_id"], "round_id": cfg.get("round_id"),
            "candidate_id": cfg.get("candidate_id"), "bindings": {
                k: cfg.get(k) for k in ("config_sha256", "manifest_sha256",
                "training_manifest_sha256", "adapter_sha256", "generated_specs_sha256")},
            "evaluator_sources": cfg["evaluator_sources"],
            "limits": cfg.get("limits", {"timeout_seconds": 2, "max_output_bytes": MAX_BYTES}),
            "fixed_questions": cfg["fixed_questions"]}

def verify_bindings(req, work):
    try:
        work = _check_work(work)
        if req.get("scope") != "fixture-only-no-model" or req.get("protocol_version") != PROTOCOL_VERSION:
            raise ValueError("FIXTURE_SCOPE_ONLY")
        if not isinstance(req.get("run_id"), str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,128}", req["run_id"]):
            raise ValueError("INVALID_RUN_ID")
        if any(not isinstance(v, str) or not re.fullmatch("[0-9a-f]{64}", v)
               for v in req["bindings"].values()) or len(req["bindings"]) != 5:
            raise ValueError("INVALID_BINDING")
        sources = req["evaluator_sources"]
        if set(sources) != {"render_executor"}:
            raise ValueError("FIXTURE_EXECUTOR_ONLY")
        src = sources["render_executor"]
        if src.get("path") != "fixture_executor.py" or src.get("protocol_role") != "fixture-child":
            raise ValueError("FIXTURE_EXECUTOR_ONLY")
        exe = _safe_artifact(work, src["path"])
        if exe is None or src.get("sha256") != APPROVED_FIXTURE_SHA256 or _sha(exe) != APPROVED_FIXTURE_SHA256:
            raise ValueError("EXECUTOR_NOT_INDEPENDENTLY_PINNED")
        limits = req["limits"]
        if type(limits.get("timeout_seconds")) is not int or not 1 <= limits["timeout_seconds"] <= 30:
            raise ValueError("INVALID_TIMEOUT")
        if type(limits.get("max_output_bytes")) is not int or not 1 <= limits["max_output_bytes"] <= MAX_BYTES:
            raise ValueError("INVALID_OUTPUT_LIMIT")
        qs = req["fixed_questions"]
        if not isinstance(qs, list) or not 1 <= len(qs) <= 128:
            raise ValueError("INVALID_FIXED_QUESTIONS")
        ids = [_identity(q["identity"]) for q in qs]
        if len(set(ids)) != len(ids):
            raise ValueError("DUPLICATE_FIXED_IDENTITY")
        for q in qs:
            for key in ("input_record_sha256", "generated_spec_sha256"):
                if not isinstance(q.get(key), str) or not re.fullmatch("[0-9a-f]{64}", q[key]):
                    raise ValueError("INVALID_SAMPLE_HASH")
        specs = _read_json(work / "generated-specs.json")
        if _sha(work / "generated-specs.json") != req["bindings"]["generated_specs_sha256"]:
            raise ValueError("GENERATED_SPECS_DRIFT")
        if not isinstance(specs, list):
            raise ValueError("INVALID_GENERATED_SPECS")
        spec_ids = [_identity({k: s[k] for k in IDENTITY_KEYS}) for s in specs]
        if len(spec_ids) != len(set(spec_ids)) or set(spec_ids) != set(ids):
            raise ValueError("GENERATED_IDENTITY_COVERAGE")
        by_id = dict(zip(spec_ids, specs))
        if any(_sha_text(json.dumps(by_id[key]["spec"], ensure_ascii=False)) != q["generated_spec_sha256"]
               for key, q in zip(ids, qs)):
            raise ValueError("SPEC_CONTENT_DRIFT")
        if (work / "scenario.json").stat().st_size > 16384:
            raise ValueError("SCENARIO_TOO_LARGE")
        return True, ""
    except (OSError, ValueError, TypeError, KeyError, AttributeError) as exc:
        return False, str(exc)

def _decode_media(p):
    if p.suffix.lower() != ".png":
        return None, "UNSUPPORTED_MEDIA"
    try:
        from PIL import Image
        with Image.open(p) as im:
            if im.format != "PNG":
                return False, "NOT_PNG"
            im.load()
            return min(im.size) > 0, "PNG_DECODED"
    except ImportError:
        return None, "PIL_UNAVAILABLE"
    except Exception as exc:
        return False, type(exc).__name__

def verify_response(req, work, resp, real_rc, timed_out):
    fixed = {_identity(q["identity"]): q for q in req["fixed_questions"]}
    seen = set(); lines = []; problems = []; fatal = False
    def problem(identity, code):
        problems.append({"identity": identity, "code": code})
    if type(real_rc) is not int or type(timed_out) is not bool or timed_out:
        resp = []
        problem(None, "TIMEOUT_OR_INVALID_PROCESS_RESULT")
        fatal = True
    if not isinstance(resp, list) or len(resp) > 256:
        resp = []; fatal = True; problem(None, "INVALID_RESPONSE")
    for raw in resp:
        try:
            if not isinstance(raw, dict) or any(str(k).startswith("_") for k in raw):
                raise ValueError("MALFORMED_RECEIPT")
            ident = raw.get("identity"); key = _identity(ident)
            if key not in fixed:
                raise ValueError("EXTRA_OR_UNKNOWN_IDENTITY")
        except (ValueError, TypeError, KeyError):
            fatal = True; problem(None, "EXTRA_OR_MALFORMED_IDENTITY"); continue
        line = json.loads(json.dumps(raw))
        if key in seen:
            problem(ident, "DUPLICATE_IDENTITY")
            for previous in lines:
                if previous.get("identity") == ident:
                    previous["_rejected"] = True
            line["_rejected"] = True; lines.append(line); continue
        seen.add(key); q = fixed[key]
        if type(line.get("rc")) is not int or line["rc"] != real_rc:
            line["_rejected"] = True; problem(ident, "RC_MISMATCH_OR_INVALID_TYPE")
        ib = line.get("input_bindings")
        if not isinstance(ib, dict) or any(ib.get(k) != q[k] for k in ("input_record_sha256", "generated_spec_sha256")):
            line["_rejected"] = True; problem(ident, "INPUT_OR_SPEC_DRIFT")
        if line.get("_rejected"):
            lines.append(line); continue
        artifacts = line.get("artifacts", [])
        if not isinstance(artifacts, list) or len(artifacts) > 16:
            line["_rejected"] = True; problem(ident, "INVALID_ARTIFACTS"); lines.append(line); continue
        checked = []; render_override = None
        for art in artifacts:
            if not isinstance(art, dict):
                line["_rejected"] = True; problem(ident, "INVALID_ARTIFACT"); break
            p = _safe_artifact(work, art.get("path"))
            if p is None or not p.is_file() or p.stat().st_size > MAX_BYTES or _sha(p) != art.get("sha256"):
                line["_rejected"] = True; problem(ident, "ARTIFACT_PATH_SIZE_OR_HASH"); break
            result, detail = _decode_media(p) if p.stat().st_size else (False, "EMPTY_MEDIA")
            checked.append({"path": art["path"], "sha256": art["sha256"], "decode_ok": result, "detail": detail})
            if result is False:
                render_override = "FAIL"; problem(ident, "ARTIFACT_UNDECODABLE")
            elif result is None and render_override != "FAIL":
                render_override = "UNVERIFIED"
        if line.get("_rejected"):
            lines.append(line); continue
        if not checked:
            render_override = "FAIL"; problem(ident, "NO_ARTIFACT")
        line["_artifacts_checked"] = checked
        if render_override is not None:
            line["render"] = {"decision": render_override}
        if real_rc != 0:
            line["executable"] = {"decision": "FAIL"}
        math = line.get("math")
        if isinstance(math, dict) and math.get("decision") == "PASS":
            req_as = q.get("assertions", [])
            got_as = math.get("assertions", [])
            if not isinstance(got_as, list) or any(not isinstance(x, dict) for x in got_as):
                got_as = []
            got = {x.get("id"): x for x in got_as if isinstance(x.get("id"), str)}
            wanted = {x["id"] for x in req_as}
            if not wanted or len(got) != len(got_as) or set(got) != wanted or any(
                    type(got[k].get("verdict")) is not bool or not isinstance(got[k].get("reason"), str)
                    or not got[k]["reason"].strip() for k in wanted):
                line["math"] = {"decision": "UNVERIFIED"}; problem(ident, "MATH_COVERAGE_OR_UNDECIDED")
            elif any(got[k]["verdict"] is False for k in wanted):
                line["math"] = {"decision": "FAIL"}; problem(ident, "MATH_FALSE_VERDICT")
        fid = line.get("fidelity")
        if isinstance(fid, dict) and fid.get("decision") == "PASS":
            if not q.get("fidelity_checklist") or fid.get("checklist") != q["fidelity_checklist"]:
                line["fidelity"] = {"decision": "UNVERIFIED"}; problem(ident, "FIDELITY_COVERAGE")
        lines.append(line)
    for key, q in fixed.items():
        if key not in seen:
            problem(q["identity"], "MISSING_IDENTITY")
            lines.append({"identity": q["identity"], "_missing": True})
    if fatal:
        for line in lines:
            line["_rejected"] = True
    return {"lines": lines, "problems": problems, "real_rc": real_rc, "timed_out": timed_out, "protocol_rejected": fatal}

def schema_ok(spec):
    return isinstance(spec, dict) and all(isinstance(spec.get(k), list) and bool(spec[k]) and
        all(isinstance(x, str) and x.strip() for x in spec[k]) for k in ("objects", "steps"))

def _combine(values):
    if not values or any(x not in ("PASS", "FAIL") for x in values):
        return "UNVERIFIED"
    return "FAIL" if "FAIL" in values else "PASS"

def question_metrics(req, verified, specs_by_identity):
    groups = {}; by_id = {}
    for line in verified["lines"]:
        by_id.setdefault(_identity(line["identity"]), []).append(line)
    for q in req["fixed_questions"]:
        groups.setdefault((q["identity"]["split"], q["identity"]["problem_id"]), []).append(q)
    out = []
    for (split, pid), members in groups.items():
        rows = []; invalid = False; schemas = []
        for q in members:
            key = _identity(q["identity"]); found = by_id.get(key, [])
            if len(found) != 1 or any(x.get("_missing") or x.get("_rejected") for x in found):
                invalid = True
            rows.extend(found)
            s = specs_by_identity.get(key, [])
            if len(s) != 1:
                invalid = True
            schemas.extend(schema_ok(x) for x in s)
        values = {}
        for name in METRICS:
            decisions = [(x.get(name) or {}).get("decision") if isinstance(x.get(name), dict) else None for x in rows]
            values[name] = "UNVERIFIED" if invalid else _combine(decisions)
        values["executable"] = "UNVERIFIED" if invalid else _combine(
            [values["executable"], values["render"], "PASS" if schemas and all(schemas) else "FAIL"])
        out.append({"question": {"split": split, "problem_id": pid}, **values})
    return out

def _metric(rows, name):
    passed = sum(x[name] == "PASS" for x in rows)
    unknown = sum(x[name] == "UNVERIFIED" for x in rows)
    n = len(rows)
    return {"status": "UNVERIFIED" if unknown or not n else "FIXTURE_CHECKED",
            "passed": passed, "total": n, "rate": None if unknown or not n else str(Fraction(passed, n)),
            "unknown": unknown, "scope": "SIMULATED_DIAGNOSTIC_NOT_ACTUAL_METRIC"}

def aggregate(req, verified, specs_by_identity=None):
    rows = question_metrics(req, verified, specs_by_identity or {})
    splits = sorted({x["question"]["split"] for x in rows})
    diag = {name: _metric(rows, name) for name in METRICS}
    diag["by_split"] = {sp: {name: _metric([x for x in rows if x["question"]["split"] == sp], name) for name in METRICS} for sp in splits}
    diag["e_subset_of_r"] = all(x["render"] == "PASS" for x in rows if x["executable"] == "PASS")
    diag["questions"] = rows
    def unknown(n):
        return {"status": "UNVERIFIED", "passed": None, "total": n, "rate": None,
                "reason": "Fixed fixture only; no actual sandbox renderer or independent math/visual judge."}
    return {"protocol_version": PROTOCOL_VERSION, "status": "REFUSED" if verified.get("protocol_rejected") else "FIXTURE_ONLY",
            "scope": "fixture-only-no-model", "production": "CLOSED", "total_questions": len(rows),
            "total_samples": len(req["fixed_questions"]), **{name: unknown(len(rows)) for name in METRICS},
            "by_split": {sp: {"total_questions": sum(x["question"]["split"] == sp for x in rows),
                **{name: unknown(sum(x["question"]["split"] == sp for x in rows)) for name in METRICS}} for sp in splits},
            "fixture_diagnostics": diag, "problems": verified["problems"],
            "rejected_receipts": len(verified["problems"]), "actual_execution_metrics_valid": False}

def run_executor(req, work, exe_name):
    ok, reason = verify_bindings(req, work)
    if not ok or exe_name != "render_executor":
        raise ValueError(reason or "FIXTURE_EXECUTOR_ONLY")
    response = work / "response-index.jsonl"
    if response.exists():
        raise ValueError("STALE_RESPONSE")
    exe = _safe_artifact(work, req["evaluator_sources"][exe_name]["path"])
    try:
        cp = subprocess.run([sys.executable, "-I", "-B", "-X", "utf8", str(exe),
            "--request", str(work / "request.json"), "--work", str(work)],
            capture_output=True, cwd=work, timeout=req["limits"]["timeout_seconds"],
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        limit = req["limits"]["max_output_bytes"]
        if len(cp.stdout) > limit or len(cp.stderr) > limit:
            raise ValueError("EXECUTOR_OUTPUT_LIMIT")
        if response.exists() and response.stat().st_size > limit:
            raise ValueError("RESPONSE_OUTPUT_LIMIT")
        rows = [json.loads(x) for x in response.read_text(encoding="utf-8").splitlines() if x.strip()] if response.exists() else []
        return rows, cp.returncode, False, cp.stdout.decode("utf-8", "replace"), cp.stderr.decode("utf-8", "replace")
    except subprocess.TimeoutExpired as exc:
        return [], -1, True, (exc.stdout or b"").decode("utf-8", "replace"), (exc.stderr or b"").decode("utf-8", "replace")

def run_harness(cfg, work):
    try:
        work = _check_work(work)
        if any((work / x).exists() for x in ("request.json", "response-index.jsonl", "eval-report.json", "executor.stdout.txt", "executor.stderr.txt", "artifacts")):
            raise ValueError("FRESH_WORK_REQUIRED")
        req = build_request(cfg)
        ok, reason = verify_bindings(req, work)
        if not ok:
            raise ValueError(reason)
        request_bytes = (json.dumps(req, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        if len(request_bytes) > MAX_BYTES:
            raise ValueError("REQUEST_TOO_LARGE")
        (work / "request.json").write_bytes(request_bytes)
        request_sha = _sha(work / "request.json")
        rows, rc, timed_out, stdout, stderr = run_executor(req, work, "render_executor")
        (work / "executor.stdout.txt").write_text(stdout, encoding="utf-8")
        (work / "executor.stderr.txt").write_text(stderr, encoding="utf-8")
        ok, reason = verify_bindings(req, work)
        if not ok or _sha(work / "request.json") != request_sha:
            raise ValueError(reason or "REQUEST_DRIFT")
        verified = verify_response(req, work, rows, rc, timed_out)
        specs = _read_json(work / "generated-specs.json")
        by_id = {_identity({k: s[k] for k in IDENTITY_KEYS}): [s["spec"]] for s in specs}
        report = aggregate(req, verified, by_id)
        report.update(run_id=req["run_id"], real_rc=rc, timed_out=timed_out,
            request_sha256=request_sha, executor_stdout_sha256=_sha(work / "executor.stdout.txt"),
            executor_stderr_sha256=_sha(work / "executor.stderr.txt"))
        (work / "eval-report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return report
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        return {"status": "REFUSED", "scope": "fixture-only-no-model", "reason": str(exc), "production": "CLOSED", "actual_execution_metrics_valid": False}
