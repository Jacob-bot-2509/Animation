"""Adversarial verification of candidate defect:
_post_verify exception demotes confirmed FAIL -> UNVERIFIED/ERROR/exit 2.

READ-ONLY w.r.t. project files: only creates files under a temp dir.
"""
import sys
import tempfile
import threading
import traceback
from pathlib import Path

SUPPORT = Path(r"D:\Animation-Model-Training\reviews\2026-10-04-acceptance-support")
sys.path.insert(0, str(SUPPORT))
import file_acceptance as fa  # noqa: E402

print("module under test:", fa.__file__)

# ---- 1. Pure judge: FAIL reachable for real breach records -----------------
ctrl_ok = {"spawned": True, "rc": 0, "timed_out": False, "succeeded": True}
sb_ok = {"spawned": True, "rc": 0, "timed_out": False, "token29": True,
         "sid_ok": True, "client_ok": True}
dw = fa._judge_case("denied_write", ctrl_ok,
                    dict(sb_ok, outcome="denied", winerror=5,
                         target_created=True))
dr = fa._judge_case("denied_read", ctrl_ok,
                    dict(sb_ok, outcome="denied", winerror=5,
                         content_leaked=True, target_stable=True))
neg = fa._negative_regressions()
print("judge denied_write target_created=True ->", dw["verdict"])
print("judge denied_read  content_leaked=True ->", dr["verdict"])
print("negative_regressions all_hold:", neg["all_hold"])

# ---- 2. Deterministic _post_verify exception from lines 536-537 -----------
# exists() returns True (Path.exists() is True for a directory), then
# read_text() raises OSError -- the same unguarded call the candidate cites.
tmp = Path(tempfile.mkdtemp(prefix="pvsim-"))
(tmp / "python313._pth").mkdir()
real_nr = fa.NET_RUNTIME
fa.NET_RUNTIME = tmp
cfg = {"client_path": str(tmp / "no-client.py"), "client_sha256": "x"}
try:
    fa._post_verify(cfg, manifest={}, pth_before="Lib\nDLLs\n.",
                    script_sha_before="x")
    print("post_verify: unexpectedly no exception")
except OSError as e:
    print(f"post_verify raised {type(e).__name__}: {e} (from read_text after exists()==True)")

# ---- 3. Replay main() lines 627-649 + exit logic 652-654 verbatim ---------
results = {"overall": "UNVERIFIED", "state": "RUNNING",
           "case": {"overall": "FAIL",   # confirmed breach, e.g. dw above
                    "cases": {"denied_write": dw}}}
exit_code = None
try:
    # line 627-628 (case already computed above); line 629:
    results["post_verify"] = fa._post_verify(cfg, {}, "Lib\nDLLs\n.", "x")
    case_overall = results["case"]["overall"]          # line 632
    if case_overall == "FAIL":                          # lines 633-634
        results["overall"] = "FAIL"
    elif results["post_verify"]["all_unchanged"]:       # line 635
        results["overall"] = case_overall
    else:                                               # lines 637-638
        results["overall"] = "UNVERIFIED"
    results["state"] = "COMPLETE"                       # line 639
    fa._assert_json_safe(results, "results")            # line 640
    exit_code = 1 if results["overall"] == "FAIL" else 0  # line 652-654 shape
except Exception as e:  # lines 644-649 verbatim
    results.update(state="ERROR", overall="UNVERIFIED",
                   error=repr(e), traceback=traceback.format_exc())
    exit_code = 2
fa.NET_RUNTIME = real_nr

print("\n--- after main()-style flow ---")
print("results['case']['overall'] =", results["case"]["overall"])
print("results['overall']          =", results["overall"])
print("results['state']            =", results["state"])
print("exit code                  =", exit_code)
print("error                      =", results.get("error"))
print("FAIL survives only in nested case dict:", "FAIL" == results["case"]["overall"],
      "| top-level signal lost:", results["overall"] != "FAIL")

# ---- 4. Show the real TOCTOU (delete between exists/read_text) can fire ----
pth = tmp / "python313._pth2"
pth.write_text("Lib\nDLLs\n.\n", encoding="ascii")
stop = threading.Event()
hits = {"fne": 0, "perm": 0, "iters": 0}

def writer():
    while not stop.is_set():
        try:
            pth.unlink()
        except OSError:
            pass
        pth.write_text("Lib\nDLLs\n.\n", encoding="ascii")

def reader():
    while not stop.is_set():
        hits["iters"] += 1
        try:
            # exact pattern of lines 536-537
            _ = pth.read_text(encoding="utf-8",
                              errors="replace") if pth.exists() else None
        except FileNotFoundError:
            hits["fne"] += 1
        except OSError:
            hits["perm"] += 1

tw = threading.Thread(target=writer, daemon=True)
tr = threading.Thread(target=reader, daemon=True)
tw.start(); tr.start()
import time
time.sleep(4.0)
stop.set(); tw.join(1); tr.join(1)
print(f"\nTOCTOU race: {hits['iters']} exists/read_text cycles -> "
      f"FileNotFoundError x{hits['fne']}, other OSError x{hits['perm']}")
