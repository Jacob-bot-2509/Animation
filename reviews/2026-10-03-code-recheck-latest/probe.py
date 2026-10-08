"""Independent synthetic review probes. Never writes production datasets or ACLs."""
import contextlib
import ctypes
import hashlib
import io
import json
import shutil
import sys
import uuid
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))
from animtrain.freeze import check_frozen, freeze_set
from animtrain.metrics import SampleResult, aggregate
from tools import preflight as cli, eval_test_prep as status, make_eval_test as gen


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    results = {}
    paths = ["src/animtrain/appcontainer.py", "src/animtrain/metrics.py",
             "tools/preflight.py", "tools/eval_test_prep.py", "tools/make_eval_test.py",
             "src/animtrain/render_gate.py", "src/animtrain/net_guard.py"]
    results["source_hashes"] = {p: sha(ROOT / p) for p in paths}
    snapshots = HERE / "source-snapshot"
    snapshots.mkdir(exist_ok=True)
    for p in paths:
        shutil.copyfile(ROOT / p, snapshots / p.replace("/", "__"))

    fx = HERE / "probe-fixtures" / uuid.uuid4().hex
    fx.mkdir(parents=True)
    current = fx / "current"
    current.mkdir(exist_ok=True)
    data = current / "eval.jsonl"
    data.write_text('{"id":"synthetic"}\n', encoding="utf-8")
    mp = current / "manifest.json"
    mp.write_text(json.dumps({"name": "synthetic", "version": 1, "entries": [
        {"path": data.name, "sha256": sha(data), "size": data.stat().st_size,
         "source": "synthetic", "license": "Internal-Research-Use-Only", "split": "eval"}
    ]}), encoding="utf-8")
    good_lock = current / "eval.lock.json"
    freeze_set([data], good_lock, {"manifest_sha256": sha(mp)})
    historical = fx / "other-version"
    historical.mkdir(exist_ok=True)
    other = historical / "eval.jsonl"
    other.write_text("old-version\n", encoding="utf-8")
    old_lock = historical / "eval.lock.json"
    freeze_set([other], old_lock, {"manifest_sha256": "a" * 64})

    def freeze_gate(locks):
        captured = {}
        def record(*args, **kwargs):
            captured.update(dict(kwargs["extra_checks"]))
            return {"checks": [], "ok": False, "ready": False, "exit_code": 1}
        with patch.object(cli, "validate_manifest", return_value={
                "ok": True, "n_entries": 1, "problems": [], "quarantines": [],
                "near_dup_calibrated": True}), \
             patch("animtrain.render_gate.render_check", return_value={
                "ok": True, "status": "synthetic", "detail": "mock"}), \
             patch("animtrain.render_gate.math_check", return_value={
                "ok": True, "status": "synthetic", "detail": "mock"}), \
             patch("animtrain.freeze.discover_locks", return_value=(locks, [])), \
             patch.object(cli, "check_asset_evidence", return_value=(False, "mock")), \
             patch.object(cli, "check_exec_isolation", return_value=(False, "mock")), \
             patch.object(cli, "run_preflight", side_effect=record), \
             contextlib.redirect_stdout(io.StringIO()):
            cli.main(["--manifest", str(mp)])
        return captured["freeze_gate"]

    results["current_lock_only"] = freeze_gate([good_lock])
    results["healthy_other_version"] = freeze_gate([good_lock, old_lock])
    other.write_text("modified-old-version\n", encoding="utf-8")
    results["damaged_other_version"] = freeze_gate([good_lock, old_lock])

    candidate = fx / "candidate"
    (candidate / "eval").mkdir(parents=True, exist_ok=True)
    candidate_data = candidate / "eval" / "dataset_eval.jsonl"
    candidate_data.write_text('{"id":"unrelated-synthetic"}\n', encoding="utf-8")
    v1_sha = sha(ROOT / "data/v1/manifest.json")
    candidate_lock = candidate / "eval" / "eval.lock.json"
    freeze_set([candidate_data], candidate_lock, {"manifest_sha256": v1_sha})
    output = io.StringIO()
    with contextlib.redirect_stdout(output):
        status.cmd_status(SimpleNamespace(dir=str(candidate)))
    results["unrelated_manifest_status"] = output.getvalue()

    out = fx / "generator-target"
    (out / "eval").mkdir(parents=True, exist_ok=True)
    target = out / "eval" / "dataset_eval.json"
    target.write_text("[\"frozen-synthetic\"]\n", encoding="utf-8")
    lock = out / "eval" / "eval.lock.json"
    freeze_set([target], lock)
    before = sha(target)
    with patch.object(sys, "argv", ["make_eval_test", "--out", str(out)]), \
         patch.object(gen, "parse_blocks", return_value=[]), \
         patch.object(gen, "build_eval", return_value=[]), \
         patch.object(gen, "build_test", return_value=[]), \
         contextlib.redirect_stdout(io.StringIO()):
        rc = gen.main()
    results["generator_frozen_overwrite"] = {
        "returncode": rc, "changed": before != sha(target), "lock_problems": check_frozen(lock)}
    with patch.object(sys, "argv", ["make_eval_test", "--out", str(ROOT / "data/V1")]), \
         patch.object(gen, "parse_blocks", side_effect=AssertionError("must reject before parsing")), \
         contextlib.redirect_stdout(io.StringIO()):
        results["uppercase_v1_rejected"] = gen.main() == 1
    try:
        aggregate([SampleResult("a", "hash", parsed_strict=2, parsed_lenient=2)])
        results["metrics_nonboolean_rejected"] = False
    except ValueError:
        results["metrics_nonboolean_rejected"] = True

    from animtrain.preflight import check_exec_isolation
    results["execution_isolation_gate"] = check_exec_isolation()
    if sys.platform == "win32":
        from ctypes import wintypes
        userenv = ctypes.WinDLL("userenv", use_last_error=True)
        derive = userenv.DeriveAppContainerSidFromAppContainerName
        derive.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(wintypes.LPVOID)]
        derive.restype = ctypes.c_long
        ptr = wintypes.LPVOID()
        hr = derive("animtrain-render-sandbox", ctypes.byref(ptr))
        results["derive_sid_raw_api"] = {"HRESULT": hr, "has_sid": bool(ptr)}
        canonical_sid = None
        if ptr:
            api = ctypes.WinDLL("advapi32")
            length = api.GetLengthSid
            length.argtypes = [wintypes.LPVOID]
            length.restype = wintypes.DWORD
            canonical_sid = ctypes.string_at(ptr, length(ptr))
            results["derive_sid_raw_api"]["sid_bytes"] = len(canonical_sid)
            free = ctypes.WinDLL("advapi32").FreeSid
            free.argtypes = [wintypes.LPVOID]
            free.restype = wintypes.LPVOID
            free(ptr)
        try:
            from animtrain import appcontainer
            sid = appcontainer.appcontainer_sid()
            results["appcontainer_sid_probe"] = {
                "returned_bytes": len(sid), "matches_system_sid": sid == canonical_sid,
                "declared_restype": str(appcontainer._u32.DeriveAppContainerSidFromAppContainerName.restype)}
        except Exception as exc:
            results["appcontainer_sid_probe"] = {"exception": type(exc).__name__, "detail": str(exc)}
    results["source_unchanged_during_probes"] = all(
        sha(ROOT / p) == digest for p, digest in results["source_hashes"].items())
    (HERE / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=2),
                                        encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
