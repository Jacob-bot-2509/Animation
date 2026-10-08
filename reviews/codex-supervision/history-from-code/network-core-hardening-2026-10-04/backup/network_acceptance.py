"""Bounded local loopback acceptance using an already provisioned test runtime.

This command does not grant ACLs or create a profile. See --baseline-evidence.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
import traceback
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from animtrain import appcontainer as ac
from animtrain import network_isolation as net

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def run_client(command, sandbox, work, env):
    record = {"command": command, "rc": None, "timed_out": False, "data": None}
    try:
        if sandbox:
            cp = ac.run_appcontainer(command, cwd=work, env=env, allowed_dirs=[], timeout_ms=15000)
        else:
            cp = subprocess.run(command, cwd=work, capture_output=True, timeout=15)
        record.update(rc=cp.returncode, stdout=cp.stdout.decode("utf-8", "replace"),
                      stderr=cp.stderr.decode("utf-8", "replace"))
        try: record["data"] = json.loads(record["stdout"])
        except (ValueError, TypeError): pass
    except subprocess.TimeoutExpired as exc:
        record.update(timed_out=True, error=repr(exc))
    except OSError as exc:
        record["error"] = repr(exc)
    return record

def run_case(transport, host, runtime, client, work, env, expected_sid, manifest, client_sha, window):
    nonce = {side: uuid.uuid4().hex for side in ("before", "sandbox", "after")}
    record = {"host": host, "transport": transport, "expected_sid": expected_sid,
              "nonces": nonce, "clients": {}, "packets": [], "server_complete": False,
              "server_errors": [], "runtime_integrity": False,
              "contract": net.LOCAL_LOOPBACK_CONTRACT,
              "policy_before": {"api_ok": False}, "policy_after": {"api_ok": False}}
    receiver = None
    try:
        record["policy_before"] = net.read_loopback_exemptions()
        receiver = net.LoopbackReceiver(transport, host)
        record.update(port=receiver.port, server_started=receiver.started)
        for side in ("before", "sandbox", "after"):
            print("RUN " + transport + " " + host + " " + side, flush=True)
            cmd = [str(runtime), "-X", "utf8", str(client), transport, host, str(receiver.port), nonce[side]]
            record["clients"][side] = run_client(cmd, side == "sandbox", work, env)
            if side == "sandbox":
                # Keep the same receiver alive for a full bounded observation window.
                deadline = time.monotonic() + window
                while time.monotonic() < deadline:
                    time.sleep(min(0.1, max(0, deadline - time.monotonic())))
            else:
                deadline = time.monotonic() + 2
                target = nonce[side].encode("ascii").hex()
                while time.monotonic() < deadline and not any(p["hex"] == target for p in receiver.snapshot()):
                    time.sleep(0.01)
    except Exception as exc:
        record["server_errors"].append(repr(exc))
    finally:
        if receiver:
            try:
                receiver.close()
                record.update(packets=receiver.snapshot(), server_closed=receiver.closed,
                              server_complete=not receiver.thread.is_alive())
                record["server_errors"].extend(receiver.errors)
            except Exception as exc:
                record["server_errors"].append(repr(exc))
        try:
            record["policy_after"] = net.read_loopback_exemptions()
        except Exception as exc:
            record["policy_after"] = {"api_ok": False, "error": repr(exc)}
    try:
        runtime_ok = all(digest(runtime.parent / rel) == sha for rel, sha in manifest.items())
        pth = (runtime.parent / "python313._pth").read_text(encoding="utf-8").splitlines()
        pth_ok = bool(pth) and all(line.strip() in ("Lib", "DLLs", ".") for line in pth if line.strip())
        clients_ok = all(
            (c.get("data") or {}).get("client_sha256") == client_sha
            and c["data"].get("exe_sha256") == manifest["python.exe"]
            and c["data"].get("site_absent") is True
            and os.path.normcase(c["data"].get("executable", "")) == os.path.normcase(str(runtime))
            and os.path.normcase(c["data"].get("socket_file", "")) == os.path.normcase(str(runtime.parent / "Lib/socket.py"))
            for c in record["clients"].values())
        record["runtime_integrity"] = runtime_ok and pth_ok and clients_ok and digest(client) == client_sha
    except Exception as exc:
        record["integrity_error"] = repr(exc)
    record["judgment"] = net.judge_loopback_evidence(record)
    return record

CASES = (("tcp", "127.0.0.1"), ("udp", "127.0.0.1"), ("tcp", "::1"), ("udp", "::1"))


def overall_verdict(result):
    """A partial/error run cannot pass; affirmative delivery always remains FAIL."""
    if not isinstance(result, dict):
        return "UNVERIFIED"
    attempts = result.get("attempts", [])
    if not isinstance(attempts, list):
        return "UNVERIFIED"
    verdicts = [a["judgment"].get("verdict") if isinstance(a, dict) and isinstance(a.get("judgment"), dict) else None for a in attempts]
    if "FAIL" in verdicts:
        return "FAIL"
    endpoints = [(a.get("transport"), a.get("host")) if isinstance(a, dict) else None for a in attempts]
    if (result.get("state") == "COMPLETE" and endpoints == list(CASES)
            and result.get("runtime_unchanged") is True
            and all(v == "PASS_LOCAL_LOOPBACK" for v in verdicts)):
        return "PASS_LOCAL_LOOPBACK"
    return "UNVERIFIED"


def write_evidence(target, result):
    """Replace a unique run's snapshot atomically, so readers never see half JSON."""
    pending = target.with_suffix(".json.tmp")
    pending.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    pending.replace(target)


def execute(args, result, target):
    baseline = json.loads(args.baseline_evidence.read_text(encoding="utf-8"))
    runtime = Path(baseline["runtime"]).resolve()
    work_parent = Path(baseline["work"]).resolve()
    manifest = baseline["runtime_copy"]["src_manifest"]
    required = {"python.exe", "python313.dll", "Lib/socket.py", "DLLs/_socket.pyd"}
    if set(manifest) != required or not all(digest(runtime.parent / rel) == sha for rel, sha in manifest.items()):
        raise RuntimeError("Preflight runtime manifest failed; no ACL/profile changes attempted")
    pth_before = (runtime.parent / "python313._pth").read_bytes()
    if not pth_before.strip() or any(line.strip() not in (b"Lib", b"DLLs", b".") for line in pth_before.splitlines() if line.strip()):
        raise RuntimeError("Runtime is not isolated by a safe ._pth")
    work = work_parent / ("codex-loopback-" + result["run_id"][:12])
    work.mkdir()
    client = work / "native_client.py"
    client.write_text(net.client_source(), encoding="utf-8")
    client_sha = digest(client)
    env = dict(baseline["sandbox_env"])
    env.update(TEMP=str(work), TMP=str(work))
    sid = ac._sid_sddl(ac.appcontainer_sid())
    result.update(sandbox_env=env, work=str(work), runtime=str(runtime), client_sha256=client_sha,
                  expected_sid=sid, runtime_manifest=manifest,
                  module_sha256=digest(Path(net.__file__)), tool_sha256=digest(Path(__file__)))
    write_evidence(target, result)
    for transport, host in CASES:
        record = run_case(transport, host, runtime, client, work, env, sid, manifest, client_sha, 20)
        result["attempts"].append(record)
        result["overall"] = overall_verdict(result)
        write_evidence(target, result)
        print(json.dumps(record["judgment"], ensure_ascii=False), flush=True)
    result["runtime_unchanged"] = all(digest(runtime.parent / rel) == sha for rel, sha in manifest.items()) and (runtime.parent / "python313._pth").read_bytes() == pth_before
    result["state"] = "COMPLETE"


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-evidence", type=Path, required=True,
                        help="Previously reviewed native JSON with granted runtime/work, hashes and sandbox_env")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    run_id = uuid.uuid4().hex
    result = {"schema": 2, "run_id": run_id, "scope": "Local loopback only",
              "contract": net.LOCAL_LOOPBACK_CONTRACT, "contract_history": net.CONTRACT_HISTORY,
              "baseline_evidence": str(args.baseline_evidence.resolve()),
              "command": [sys.executable, str(Path(__file__))] + list(argv if argv is not None else sys.argv[1:]),
              "observation_seconds_after_client_return": 20, "attempts": [],
              "state": "RUNNING", "overall": "UNVERIFIED", "runtime_unchanged": False,
              "production_gate": "CLOSED", "external_network": "UNVERIFIED"}
    target = args.output / ("loopback-" + run_id + ".json")
    try:
        args.output.mkdir(parents=True, exist_ok=True)
        write_evidence(target, result)
        execute(args, result, target)
    except (Exception, KeyboardInterrupt) as exc:
        result.update(state="ERROR", error=repr(exc), traceback=traceback.format_exc())
    result["overall"] = overall_verdict(result)
    try:
        write_evidence(target, result)
        print(str(target), flush=True)
    except Exception as exc:
        print("Evidence write failed: " + repr(exc), file=sys.stderr, flush=True)
        # Without durable evidence no acceptance result may be reported as success.
        return 2
    return {"PASS_LOCAL_LOOPBACK": 0, "FAIL": 1, "UNVERIFIED": 2}[result["overall"]]

if __name__ == "__main__":
    raise SystemExit(main())
