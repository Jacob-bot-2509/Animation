"""Adversarial verification of candidate defect:
"Facts-first breach checks bypassed by uncaught exception classes —
 a real isolation breach is masked as UNVERIFIED"

Claims to verify:
 1. _parse_client (lines 334-338) catches only (ValueError, TypeError);
    json.loads CAN raise RecursionError (not a ValueError subclass) on
    deeply nested input -> propagates.
 2. _run_client (341-362) catches only subprocess.TimeoutExpired / OSError;
    a RecursionError from _parse_client (line 354) therefore escapes
    _run_client and skips the FS-facts check at _run_denied_write line 465.
 3. _case (563-574) converts the escape into denied_write=UNVERIFIED ->
    overall UNVERIFIED -> main() returns 2 (lines 764-769) instead of 1.
 4. denied_read: if parsed data is a JSON list, line 511 (s4 data .get) raises
    AttributeError BEFORE the raw_out regex fallback (513-515) runs, losing a
    reported sentinel hash that the fallback would have caught as FAIL.

READ-ONLY w.r.t. project files: only creates files under a temp dir.
Executors (subprocess.run / ac.run_appcontainer) are monkeypatched purely to
inject the crafted client output the defect posits; every function under test
(_parse_client, _run_client, _run_denied_write, _run_denied_read, _case,
_judge_case, _negative_regressions) is the real one.
"""
import hashlib
import json
import subprocess
import sys
import tempfile
import traceback
from pathlib import Path

SUPPORT = Path(r"D:\Animation-Model-Training\reviews\2026-10-04-acceptance-support")
sys.path.insert(0, str(SUPPORT))
import file_acceptance as fa  # noqa: E402

print("module under test:", fa.__file__)
print("python:", sys.version)

# 50k nesting: verified on this interpreter that json.loads raises RecursionError
# (2k depth parses fine; 50k/200k/1M raise -- C scanner depth check)
DEEP = "[" * 50000 + "]" * 50000


def flat_json(token=True, outcome="wrote", content_hash=None, cfg=None):
    d = {"outcome": outcome, "content_hash": content_hash}
    if token:
        d["token"] = {"api_ok": True, "is_appcontainer": True,
                      "sid": "S-1-15-2-x"}
    if cfg is not None:
        d.update(client_sha256=cfg["client_sha256"],
                 exe_sha256=cfg["runtime_python_sha256"],
                 site_absent=True, executable=str(cfg["runtime"]))
    return json.dumps(d).encode("ascii")


# ---- 1. Unit: _parse_client exception-class coverage ----------------------
print("\n== 1. _parse_client coverage ==")
print("valid dict   ->", type(fa._parse_client('{"a": 1}')).__name__)
print("JSON list    ->", fa._parse_client("[1,2,3]"))   # non-dict precondition
print("garbage      ->", fa._parse_client("not json"))  # ValueError -> {}
try:
    fa._parse_client(DEEP)
    print("deep nested  -> no exception (unexpected)")
except RecursionError as e:
    print(f"deep nested  -> RecursionError PROPAGATES (line 337 except is "
          f"(ValueError, TypeError) only): {type(e).__name__}")

# ---- 2. End-to-end denied_write: real breach on disk + RecursionError ----
print("\n== 2. denied_write: breach write + crafted output ==")
tmp = Path(tempfile.mkdtemp(prefix="advsim-"))
work = tmp / "work"; denied = tmp / "denied"
work.mkdir(); denied.mkdir()
cfg = {"client_sha256": "csha", "runtime_python_sha256": "esha",
       "runtime": Path("python.exe")}
RUNTIME = Path("python.exe"); CLIENT = Path("file_client.py"); SID = "S-1-15-2-x"

orig_ac, orig_run = fa.ac.run_appcontainer, fa.subprocess.run


def fake_ac(args, *, cwd, env, allowed_dirs, timeout_ms):
    mode, target, content = args[4], args[5], args[6]
    tp = Path(target)
    if mode == "write":
        tp.write_bytes(content.encode("ascii"))          # sandbox write "succeeds"
        if tp.name.startswith("dw-sb-"):                 # breach + crafted output
            return subprocess.CompletedProcess(args, 0, (DEEP + "\n").encode(), b"")
        return subprocess.CompletedProcess(
            args, 0, flat_json(cfg=cfg, content_hash=hashlib.sha256(
                content.encode()).hexdigest()), b"")
    if tp.exists():
        h = hashlib.sha256(tp.read_bytes()).hexdigest()
    else:
        h = None
    return subprocess.CompletedProcess(args, 0,
        flat_json(outcome="read", content_hash=h, cfg=cfg), b"")


def fake_run(cmd, *, cwd, capture_output, timeout):
    mode, target, content = cmd[4], cmd[5], cmd[6]
    tp = Path(target)
    if mode == "write":
        tp.write_bytes(content.encode("ascii"))
        return subprocess.CompletedProcess(
            cmd, 0, flat_json(token=False, content_hash=hashlib.sha256(
                content.encode()).hexdigest(), cfg=cfg), b"")
    h = hashlib.sha256(tp.read_bytes()).hexdigest() if tp.exists() else None
    return subprocess.CompletedProcess(cmd, 0,
        flat_json(token=False, outcome="read", content_hash=h, cfg=cfg), b"")


fa.ac.run_appcontainer, fa.subprocess.run = fake_ac, fake_run

try:
    fa._run_denied_write(denied, work, RUNTIME, {}, SID, CLIENT, cfg)
    print("denied_write returned normally (unexpected)")
except RecursionError:
    print("RecursionError escapes _run_client (catches only TimeoutExpired/"
          "OSError, lines 355/360) and _run_denied_write -> line 465 "
          "tgt3s.exists() NEVER runs")
breach = sorted(denied.iterdir())
print("breach file on disk in denied_dir:", [str(p.name) for p in breach],
      "| sizes:", [p.stat().st_size for p in breach])

rec = fa._case(work, denied, RUNTIME, {}, SID, CLIENT, cfg)
print("\n_case() with real breach on disk:")
print("  cases:",
      {k: v["verdict"] for k, v in rec["cases"].items()})
print("  denied_write reasons:", rec["cases"]["denied_write"]["reasons"])
print("  errors:", [(e["kind"], e["error"][:80]) for e in rec["errors"]])
print("  raw[denied_write] keys:", list(rec["raw"]["denied_write"].keys()))
print("  overall:", rec["overall"])

# main() tail (lines 764-769) applied to this outcome:
all_hold = fa._negative_regressions()["all_hold"]
ok = (all_hold and rec["overall"] == "PASS_LOCAL_FILE_ACL" and True)
exit_code = 1 if rec["overall"] == "FAIL" else (0 if ok else 2)
print(f"  -> main() exit code: {exit_code}  (breach present, expected 1=FAIL)")
print("  -> breach evidence lost: target_created never evaluated; raw entry is "
      f"{rec['raw']['denied_write']}")

# ---- 3. denied_read: data-as-list AttributeError before regex fallback -----
print("\n== 3. denied_read: leak reported in raw_out, last line parses to list ==")

def fake_ac_list(args, *, cwd, env, allowed_dirs, timeout_ms):
    mode, target, content = args[4], args[5], args[6]
    tp = Path(target)
    if mode == "read":
        h = hashlib.sha256(tp.read_bytes()).hexdigest()
        # leak evidence in raw_out + last line parses to a JSON list
        stdout = (json.dumps({"content_hash": h}) + "\n[1, 2, 3]\n").encode()
        return subprocess.CompletedProcess(args, 0, stdout, b"")
    tp.write_bytes(content.encode("ascii"))
    return subprocess.CompletedProcess(args, 0, flat_json(cfg=cfg), b"")

fa.ac.run_appcontainer = fake_ac_list
try:
    fa._run_denied_read(denied, work, RUNTIME, {}, SID, CLIENT, cfg)
    print("denied_read returned normally (unexpected)")
except AttributeError as e:
    print(f"AttributeError at line 511 (data is a list, .get fails) BEFORE the "
          f"regex fallback (513-515) could find the sentinel hash in raw_out: {e}")

rec2 = fa._case(work, denied, RUNTIME, {}, SID, CLIENT, cfg)
print("  denied_read verdict:", rec2["cases"]["denied_read"]["verdict"],
      "| overall:", rec2["overall"])

# contrast: same leak report, but last line is garbage (ValueError -> {})
def fake_ac_v(cls, *, cwd, env, allowed_dirs, timeout_ms):
    return fake_ac_list(cls, cwd=cwd, env=env, allowed_dirs=allowed_dirs,
                        timeout_ms=timeout_ms)

def fake_ac_garbage(args, *, cwd, env, allowed_dirs, timeout_ms):
    mode, target, content = args[4], args[5], args[6]
    tp = Path(target)
    if mode == "read":
        h = hashlib.sha256(tp.read_bytes()).hexdigest()
        stdout = (json.dumps({"content_hash": h}) + "\nnot json\n").encode()
        return subprocess.CompletedProcess(args, 0, stdout, b"")
    tp.write_bytes(content.encode("ascii"))
    return subprocess.CompletedProcess(args, 0, flat_json(cfg=cfg), b"")

fa.ac.run_appcontainer = fake_ac_garbage
v3, raw3 = fa._run_denied_read(denied, work, RUNTIME, {}, SID, CLIENT, cfg)
print("contrast (ValueError crash -> data={} -> regex fallback runs): verdict =",
      v3["verdict"], "| leak_source =", raw3.get("leak_source"))
print("-> same leak report: list-parse yields UNVERIFIED (masked), "
      "ValueError-parse yields FAIL (detected)")

fa.ac.run_appcontainer, fa.subprocess.run = orig_ac, orig_run

# ---- 4. Sanity: pure judge + regressions --------------------------------
print("\n== 4. sanity ==")
neg = fa._negative_regressions()
print("negative_regressions all_hold:", neg["all_hold"],
      "| n cases:", len(neg["cases"]))
ctrl = {"spawned": True, "rc": 0, "timed_out": False, "succeeded": True}
sb = {"spawned": True, "rc": 0, "timed_out": False, "token29": True,
      "sid_ok": True, "client_ok": True, "outcome": "denied", "winerror": 5}
print("judge target_created=1 (truthy non-True) ->",
      fa._judge_case("denied_write", ctrl, dict(sb, target_created=1))["verdict"])
print("judge sb_pre_exists=1 for granted_write ->",
      fa._judge_case("granted_write", ctrl,
                     dict(sb, succeeded=True, hash_ok=True,
                          sb_pre_exists=1))["verdict"])
