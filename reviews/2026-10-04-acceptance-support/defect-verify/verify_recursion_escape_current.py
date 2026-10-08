"""Definitive demo against the CURRENT file: RecursionError escape past the
facts-first breach checks (denied_write FS check / denied_read _scan_leak),
with all other cases PASS, so overall becomes UNVERIFIED -> exit 2 while a
real breach artifact sits on disk.

Only the executors are mocked (to inject crafted client stdout, as the
defect posits). _parse_client/_run_client/_run_denied_write/_run_denied_read/
_case are the real current functions. Files created only under a temp dir.
"""
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

SUPPORT = Path(r"D:\Animation-Model-Training\reviews\2026-10-04-acceptance-support")
sys.path.insert(0, str(SUPPORT))
import file_acceptance as fa  # noqa: E402

DEEP = "[" * 50000 + "]" * 50000  # json.loads -> RecursionError (verified 3.13.13)

tmp = Path(tempfile.mkdtemp(prefix="fin-"))
work = tmp / "work"; denied = tmp / "denied"
work.mkdir(); denied.mkdir()
cfg = {"client_sha256": "csha", "runtime_python_sha256": "esha",
       "runtime": Path("python.exe")}
RUNTIME = Path("python.exe"); CLIENT = Path("file_client.py"); SID = "S-1-15-2-x"

orig_ac, orig_run = fa.ac.run_appcontainer, fa.subprocess.run


def flat(token=True, outcome="wrote", ch=None, winerror=None):
    d = {"outcome": outcome, "content_hash": ch, "winerror": winerror}
    if token:
        d["token"] = {"api_ok": True, "is_appcontainer": True, "sid": SID}
    d.update(client_sha256=cfg["client_sha256"],
             exe_sha256=cfg["runtime_python_sha256"], site_absent=True,
             executable=str(cfg["runtime"]))
    return json.dumps(d).encode()


def fake_run(cmd, *, cwd, capture_output, timeout):
    mode, target, content = cmd[4], cmd[5], cmd[6]
    tp = Path(target)
    if mode == "write":
        tp.write_bytes(content.encode())
        return subprocess.CompletedProcess(
            cmd, 0, flat(token=False, ch=hashlib.sha256(content.encode()).hexdigest()), b"")
    h = hashlib.sha256(tp.read_bytes()).hexdigest()
    return subprocess.CompletedProcess(cmd, 0,
        flat(token=False, outcome="read", ch=h), b"")


def make_sandbox(craft=None):
    """craft: callable(args) -> bytes | None; None = normal denied behavior."""
    def fake_ac(args, *, cwd, env, allowed_dirs, timeout_ms):
        mode, target, content = args[4], args[5], args[6]
        tp = Path(target)
        if craft is not None:
            out = craft(mode, tp, content)
            if out is not None:
                return subprocess.CompletedProcess(args, 0, out, b"")
        if mode == "write":
            if tp.name.startswith("dw-sb-"):      # denied as it should be
                return subprocess.CompletedProcess(
                    args, 5, flat(outcome="denied", winerror=5), b"")
            tp.write_bytes(content.encode())      # granted writes succeed
            return subprocess.CompletedProcess(
                args, 0, flat(ch=hashlib.sha256(content.encode()).hexdigest()), b"")
        # sandbox read: denied as it should be
        return subprocess.CompletedProcess(
            args, 5, flat(outcome="denied", winerror=5), b"")
    return fake_ac


# ---- baseline: all PASS (sandbox properly denied) -------------------------
fa.subprocess.run = fake_run
fa.ac.run_appcontainer = make_sandbox(None)
base = fa._case(work, denied, RUNTIME, {}, SID, CLIENT, cfg)
print("baseline:", {k: v["verdict"] for k, v in base["cases"].items()},
      "| overall:", base["overall"])

# ---- scenario 1: denied_write BREACH + crafted output (RecursionError) ----
def craft_dw(mode, tp, content):
    if mode == "write" and tp.name.startswith("dw-sb-"):
        tp.write_bytes(content.encode())         # REAL breach write on disk
        return (DEEP + "\n").encode()            # parser-crashing output
    return None

fa.ac.run_appcontainer = make_sandbox(craft_dw)
rec1 = fa._case(work, denied, RUNTIME, {}, SID, CLIENT, cfg)
print("\nscenario1 (dw breach + deep output):",
      {k: v["verdict"] for k, v in rec1["cases"].items()},
      "| overall:", rec1["overall"])
print("  errors:", [(e["kind"], e["error"][:60]) for e in rec1["errors"]])
breach_files = sorted(p for p in denied.iterdir() if p.name.startswith("dw-sb-"))
print("  breach files on disk:", [p.name for p in breach_files],
      "| sizes:", [p.stat().st_size for p in breach_files])
print("  raw[denied_write]:", rec1["raw"]["denied_write"])
ok1 = fa._negative_regressions()["all_hold"] and rec1["overall"] == "PASS_LOCAL_FILE_ACL"
print("  main() exit code:", 1 if rec1["overall"] == "FAIL" else (0 if ok1 else 2),
      "(expected 1=FAIL)")

# ---- scenario 2: denied_read LEAK report + crafted output -----------------
def craft_dr(mode, tp, content):
    if mode == "read":
        h = hashlib.sha256(tp.read_bytes()).hexdigest()   # real sentinel hash
        return (json.dumps({"content_hash": h}) + "\n" + DEEP + "\n").encode()
    return None

fa.ac.run_appcontainer = make_sandbox(craft_dr)
rec2 = fa._case(work, denied, RUNTIME, {}, SID, CLIENT, cfg)
print("\nscenario2 (dr leak + deep output):",
      {k: v["verdict"] for k, v in rec2["cases"].items()},
      "| overall:", rec2["overall"])
print("  errors:", [(e["kind"], e["error"][:60]) for e in rec2["errors"]])
print("  raw[denied_read]:", rec2["raw"]["denied_read"])
ok2 = fa._negative_regressions()["all_hold"] and rec2["overall"] == "PASS_LOCAL_FILE_ACL"
print("  main() exit code:", 1 if rec2["overall"] == "FAIL" else (0 if ok2 else 2),
      "(expected 1=FAIL; sentinel hash WAS reported in raw_out but _scan_leak "
      "never ran)")

# ---- control: breach with NORMAL output -> FAIL detected ------------------
def craft_ok(mode, tp, content):
    if mode == "write" and tp.name.startswith("dw-sb-"):
        tp.write_bytes(content.encode())
        return flat(ch=hashlib.sha256(content.encode()).hexdigest())
    return None

fa.ac.run_appcontainer = make_sandbox(craft_ok)
rec3 = fa._case(work, denied, RUNTIME, {}, SID, CLIENT, cfg)
print("\ncontrol (breach + normal output):",
      {k: v["verdict"] for k, v in rec3["cases"].items()},
      "| overall:", rec3["overall"])

fa.ac.run_appcontainer, fa.subprocess.run = orig_ac, orig_run
