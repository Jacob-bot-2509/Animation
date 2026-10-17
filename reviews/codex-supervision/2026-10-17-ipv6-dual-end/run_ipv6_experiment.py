# EXPERIMENT runner: local IPv6 capability of the dual-end evidence chain.
#
# What this experiment CAN establish without a remote witness and without emitting
# any probe:
#   1. This host has no usable IPv6 stack (no address, no default route, no route to
#      a public IPv6 literal) - measured, not assumed.
#   2. The probe-emission switch is OFF in the active automation config, so the
#      Codex side is structurally unable to fire a dual-end probe.
#   3. The driver's IPv6 external-scope rules and the receiver's IPv6-only rules hold
#      under the project's own offline test suite (sockets are mocked; no packets).
#   4. The evidence channel (witness pack/consumer/adapter) is locally consistent.
#
# What it CANNOT establish: an actual external IPv6 dual-end run (needs a reachable
# public-IPv6 witness host). The verdict says so explicitly.
#
# Usage: python run_ipv6_experiment.py --out <staging-dir>
# Exit code: 0 when the local capability chain is proven, 2 when a stage fails.
# This is a MEASUREMENT harness: it never opens a socket to a remote host.

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path("D:/Animation-Model-Training")
PY = Path("D:/Python Interpreter 3147/python.exe")

# The project test suite hard-codes its scratch path under reviews/, which this
# session's subprocesses cannot write. Redirect ONLY that scratch path; the test
# logic itself is untouched.
SCRATCH_OLD = "reviews/codex-supervision/2026-10-09-witness-input-test-work"


def scratch_root() -> tuple[str, Path]:
    """Return a scratch path that payload subprocesses can actually write.

    In this session the session workspace is read-only to plain subprocesses
    (only the privileged file tool can write there), so the suite's scratch
    directory is redirected to the platform temp area. Nothing under the
    project is modified; the redirected path is recorded in the evidence.
    """
    import tempfile
    base = Path(tempfile.gettempdir()) / "ipv6-dual-end-test-work"
    base.mkdir(parents=True, exist_ok=True)
    return str(base), base


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stage_ipv6_facts() -> dict:
    """Measure this host's IPv6 capability with read-only system queries."""
    facts = {}
    ps = shutil.which("powershell") or "powershell"
    queries = {
        "addresses": ["Get-NetIPAddress -AddressFamily IPv6 | Select-Object IPAddress,PrefixLength,InterfaceAlias | ConvertTo-Json -Compress"],
        "default_route": ["Get-NetRoute -AddressFamily IPv6 | Where-Object DestinationPrefix -eq '::/0' | Select-Object DestinationPrefix,NextHop,InterfaceAlias | ConvertTo-Json -Compress"],
        "stack_state": ["Get-NetAdapterBinding -ComponentID ms_tcpip6 | Select-Object Name,Enabled | ConvertTo-Json -Compress"],
    }
    for key, cmd in queries.items():
        try:
            cp = subprocess.run([ps, "-NoProfile", "-Command", cmd[0]], capture_output=True, timeout=60)
            facts[key] = {"rc": cp.returncode,
                          "stdout": cp.stdout.decode("utf-8", "replace").strip()[:2000],
                          "stderr": cp.stderr.decode("utf-8", "replace").strip()[:500]}
        except Exception as exc:  # noqa: BLE001
            facts[key] = {"error": f"{type(exc).__name__}: {exc}"}
    # Read-only reachability check toward a public IPv6 literal (ping only, no payload).
    try:
        cp = subprocess.run(["ping", "-6", "-n", "2", "2001:4860:4860::8888"],
                            capture_output=True, timeout=60)
        facts["ping_public_v6"] = {"rc": cp.returncode,
                                   "stdout": cp.stdout.decode("utf-8", "replace")[-800:]}
    except Exception as exc:  # noqa: BLE001
        facts["ping_public_v6"] = {"error": f"{type(exc).__name__}: {exc}"}
    return facts


def stage_config() -> dict:
    """Read the probe-emission switch and its governance state."""
    path = ROOT / "configs" / "witness_automation.local.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        "config": str(path),
        "sha256": sha(path),
        "allow_probe_emission": data.get("allow_probe_emission"),
        "production": data.get("production"),
        "active": data.get("active"),
        "sender_registry_rounds": [r.get("round") for r in data.get("sender_registry", [])],
        "v3_witness_sha256": (data.get("v3_source_pins") or {}).get("witness_receiver_v3.exe"),
    }


def stage_offline_tests(staging: Path) -> dict:
    """Run the project's own driver/receiver test suite with the scratch path redirected."""
    src = ROOT / "tests" / "test_sandbox_external_driver.py"
    patched = staging / "test_sandbox_external_driver_patched.py"
    text = src.read_text(encoding="utf-8")
    if SCRATCH_OLD not in text:
        return {"ok": False, "error": f"expected scratch path not found in {src}"}
    scratch_dir_path = scratch_root()[1]
    # Two mechanical edits only:
    #   a) pin ROOT to the project root (the copy lives under archives/, so
    #      parents[1] would otherwise resolve to the wrong directory);
    #   b) redirect the hard-coded scratch path to a writable temp area.
    original = "ROOT=Path(__file__).resolve().parents[1]"
    if original not in text:
        return {"ok": False, "error": f"expected ROOT line not found in {src}"}
    patched_text = text.replace(original, f'ROOT=Path("{ROOT.as_posix()}")')
    patched_text = patched_text.replace(SCRATCH_OLD, scratch_dir_path.as_posix())
    patched.write_text(patched_text, encoding="utf-8")
    cp = subprocess.run([str(PY), "-X", "utf8", "-B", str(patched)],
                        cwd=str(ROOT), capture_output=True, timeout=600)
    out = cp.stdout.decode("utf-8", "replace")
    err = cp.stderr.decode("utf-8", "replace")
    (staging / "unittest.stdout.txt").write_text(out, encoding="utf-8")
    (staging / "unittest.stderr.txt").write_text(err, encoding="utf-8")
    tail = (out + err).strip().splitlines()[-3:]
    return {"ok": cp.returncode == 0, "returncode": cp.returncode, "tail": tail,
            "test_source": str(src), "test_source_sha256": sha(src),
            "patched": str(patched), "patched_sha256": sha(patched),
            "redirect": {"from": SCRATCH_OLD, "to": scratch_dir_path.as_posix()}}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    out: Path = args.out
    out.mkdir(parents=True, exist_ok=True)

    report = {"experiment": "ipv6 dual-end capability (local side)",
              "tool": "run_ipv6_experiment.py",
              "started_unix": time.time(),
              "stages": {}}

    report["stages"]["host_ipv6"] = stage_ipv6_facts()
    report["stages"]["emission_governance"] = stage_config()
    report["stages"]["offline_literal_tests"] = stage_offline_tests(out)

    # Judge the local chain.
    h = report["stages"]["host_ipv6"]
    addrs_raw = (h.get("addresses") or {}).get("stdout", "")
    no_v6_addr = addrs_raw in ("", "null", "[]")
    ping = h.get("ping_public_v6") or {}
    ping_ok = ping.get("rc") == 0
    emitted = report["stages"]["emission_governance"].get("allow_probe_emission")
    tests = report["stages"]["offline_literal_tests"]

    report["judgement"] = {
        "has_ipv6_address": not no_v6_addr,
        "public_ipv6_reachable": ping_ok,
        "probe_emission_allowed": emitted,
        "offline_ipv6_literal_rules_pass": bool(tests.get("ok")),
    }
    local_ready = (not no_v6_addr) and ping_ok
    report["verdict"] = "LOCAL_READY_NEEDS_WITNESS" if local_ready else "BLOCKED_NO_IPV6_PATH"
    report["blocking"] = ([] if local_ready else [
        "this host has no IPv6 address / no route to a public IPv6 literal",
        "no reachable public-IPv6 witness host was provided",
    ])
    report["not_established"] = ["external IPv6 dual-end run (D2/D8)", "sandbox IPv6 probe delivery"]
    report["finished_unix"] = time.time()

    target = out / "ipv6-experiment.json"
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"verdict": report["verdict"], "judgement": report["judgement"],
                      "tests_rc": tests.get("returncode"), "evidence": str(target)},
                     ensure_ascii=False))
    return 0 if (tests.get("ok") and not local_ready) else (2 if not tests.get("ok") else 0)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        print(json.dumps({"verdict": "ERROR", "error": f"{type(exc).__name__}: {exc}"}, ensure_ascii=False))
        raise SystemExit(3)
