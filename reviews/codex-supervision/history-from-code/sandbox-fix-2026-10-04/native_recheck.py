"""Trusted synthetic native checks of handle inheritance and job lifecycle."""
from __future__ import annotations

import ctypes
import hashlib
import json
import msvcrt
import os
import subprocess
import sys
import tempfile
import threading
import time
import uuid
from ctypes import wintypes
from pathlib import Path
from unittest.mock import patch

ROOT = Path(r"D:\Animation-Model-Training")
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
from animtrain import appcontainer as ac

runtime = Path(json.loads((OUT.parent / "fix-2026-10-04/appcontainer-native-probe.json").read_bytes())["scratch"]) / "runtime"
work = Path(tempfile.mkdtemp(prefix="native-work-", dir=OUT))
private = Path(tempfile.mkdtemp(prefix="native-private-", dir=OUT))
sentinel = private / "synthetic.txt"
sentinel.write_bytes(b"SYNTHETIC-INHERITED-HANDLE-PROBE")
profile_name = "codex-fixed-sandbox-" + uuid.uuid4().hex[:16]
result = {"profile": profile_name, "work": str(work), "runtime": str(runtime), "checks": {}}
k = ac._k32
k.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
k.OpenProcess.restype = wintypes.HANDLE
k.QueryFullProcessImageNameW.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.LPWSTR, ctypes.POINTER(wintypes.DWORD)]
k.QueryFullProcessImageNameW.restype = wintypes.BOOL
k.GetCurrentProcess.restype = wintypes.HANDLE
k.GetProcessHandleCount.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
k.GetProcessHandleCount.restype = wintypes.BOOL
create = ac._u32.CreateAppContainerProfile
create.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.LPVOID, wintypes.DWORD, ctypes.POINTER(wintypes.LPVOID)]
create.restype = ctypes.c_long
delete = ac._u32.DeleteAppContainerProfile
delete.argtypes = [wintypes.LPCWSTR]
delete.restype = ctypes.c_long
created = False
profile = None

TOKEN_PROBE = '''
import ctypes
from ctypes import wintypes
k=ctypes.WinDLL('kernel32',use_last_error=True)
a=ctypes.WinDLL('advapi32',use_last_error=True)
k.GetCurrentProcess.restype=wintypes.HANDLE
a.OpenProcessToken.argtypes=[wintypes.HANDLE,wintypes.DWORD,ctypes.POINTER(wintypes.HANDLE)]
a.OpenProcessToken.restype=wintypes.BOOL
a.GetTokenInformation.argtypes=[wintypes.HANDLE,ctypes.c_int,wintypes.LPVOID,wintypes.DWORD,ctypes.POINTER(wintypes.DWORD)]
a.GetTokenInformation.restype=wintypes.BOOL
k.CloseHandle.argtypes=[wintypes.HANDLE]
h=wintypes.HANDLE()
if not a.OpenProcessToken(k.GetCurrentProcess(),8,ctypes.byref(h)):raise ctypes.WinError(ctypes.get_last_error())
try:
    val=wintypes.DWORD();n=wintypes.DWORD()
    if not a.GetTokenInformation(h,29,ctypes.byref(val),4,ctypes.byref(n)):raise ctypes.WinError(ctypes.get_last_error())
    is_appcontainer=bool(val.value)
finally:k.CloseHandle(h)
'''


def tree_check(env, normal_exit):
    label = "normal_root_exit" if normal_exit else "timeout"
    marker = work / (label + "-child.json")
    ack = work / (label + "-ack")
    child = {}

    def monitor():
        try:
            deadline = time.monotonic() + 5
            while not marker.exists() and time.monotonic() < deadline:
                time.sleep(0.01)
            data = json.loads(marker.read_text(encoding="utf-8"))
            h = k.OpenProcess(0x100000 | 0x1000 | 1, False, data["child_pid"])
            if not h:
                raise ctypes.WinError(ctypes.get_last_error())
            child["handle"] = h
            image = ctypes.create_unicode_buffer(32768)
            n = wintypes.DWORD(len(image))
            if not k.QueryFullProcessImageNameW(h, 0, image, ctypes.byref(n)):
                raise ctypes.WinError(ctypes.get_last_error())
            child.update(child_pid=data["child_pid"], image_matches=Path(image.value).resolve() == (runtime / "python.exe").resolve(), was_alive=k.WaitForSingleObject(h, 0) == ac._WAIT_TIMEOUT)
            if not child["image_matches"] or not child["was_alive"]:
                raise AssertionError("Controlled child not observed alive")
            ack.write_text("observed", encoding="utf-8")
        except Exception as exc:
            child["monitor_error"] = repr(exc)

    code = f'''
import subprocess,sys,time,json
from pathlib import Path
p=subprocess.Popen([sys.executable,'-I','-c','import time;time.sleep(12)'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
Path({str(marker)!r}).write_text(json.dumps({{'child_pid':p.pid}}),encoding='utf-8')
deadline=time.monotonic()+2
while not Path({str(ack)!r}).exists() and time.monotonic()<deadline:time.sleep(0.01)
print(json.dumps({{'child_pid':p.pid}}),flush=True)
{'pass' if normal_exit else 'time.sleep(10)'}
'''
    t = threading.Thread(target=monitor)
    t.start()
    try:
        try:
            run = ac.run_appcontainer([str(runtime / "python.exe"), "-I", "-c", code], cwd=work, env=env, allowed_dirs=[], timeout_ms=8000 if normal_exit else 3000)
            parent = {"returncode": run.returncode, "stdout": run.stdout.decode()}
            assert normal_exit and run.returncode == 0
        except subprocess.TimeoutExpired as exc:
            parent = {"timed_out": True, "stdout": exc.output.decode(), "stderr": exc.stderr.decode()}
            assert not normal_exit
        t.join(6)
        assert not t.is_alive() and "monitor_error" not in child, child
        assert child["image_matches"] and child["was_alive"]
        assert json.loads(parent["stdout"])["child_pid"] == child["child_pid"]
        exited = k.WaitForSingleObject(child["handle"], 0) == 0
        assert exited, "Child survived helper return"
        return {**parent, "child_pid": child["child_pid"], "child_image_matches": True, "child_observed_alive_before_cleanup": True, "held_child_handle_signaled_after_return": exited}
    finally:
        t.join(6)
        h = child.get("handle")
        if h:
            if child.get("image_matches") and k.WaitForSingleObject(h, 0) == ac._WAIT_TIMEOUT:
                k.TerminateProcess(h, 1)
                k.WaitForSingleObject(h, 5000)
                result.setdefault("emergency_cleanup", []).append(label)
            k.CloseHandle(h)


try:
    sid = wintypes.LPVOID()
    hr = create(profile_name, "Synthetic lifecycle test", "Delete after test", None, 0, ctypes.byref(sid))
    result["create_hresult"] = hr
    if hr < 0:
        raise OSError(hr, "Profile creation failed")
    created = True
    try:
        sid_bytes = ctypes.string_at(sid, ac._a32.GetLengthSid(sid))
    finally:
        ac._a32.FreeSid(sid)
    with patch.object(ac, "APPCONTAINER_NAME", profile_name):
        profile = ac.appcontainer_profile_path(sid_bytes)
        env = {key: os.environ[key] for key in ("SystemRoot", "SystemDrive", "windir", "USERPROFILE", "ALLUSERSPROFILE", "ProgramData", "USERNAME", "USERDOMAIN", "HOMEDRIVE", "HOMEPATH") if key in os.environ}
        env.update(PATH=str(runtime), TEMP=str(work), TMP=str(work), LOCALAPPDATA=str(profile), APPDATA=str(profile))
        fd = os.open(sentinel, os.O_RDONLY)
        try:
            os.set_inheritable(fd, True)
            handle = msvcrt.get_osfhandle(fd)
            code = TOKEN_PROBE + f'''
import json,sys
r={{'token_is_appcontainer':is_appcontainer,'stdin_eof':sys.stdin.read()==''}}
try:
    with open({str(sentinel)!r},'rb') as f:r['direct_bytes']=f.read().decode()
except OSError as e:r['direct_errno']=e.errno
k.ReadFile.argtypes=[wintypes.HANDLE,wintypes.LPVOID,wintypes.DWORD,ctypes.POINTER(wintypes.DWORD),wintypes.LPVOID]
k.ReadFile.restype=wintypes.BOOL
b=ctypes.create_string_buffer(128);n=wintypes.DWORD()
try:
    r['inherited_read_ok']=bool(k.ReadFile(wintypes.HANDLE({handle}),b,128,ctypes.byref(n),None))
    r['inherited_error']=ctypes.get_last_error() if not r['inherited_read_ok'] else 0
except OSError as e:
    r['inherited_read_ok']=False
    r['inherited_error']=e.winerror
r['inherited_invalid_handle']=r['inherited_error'] in (6,-1073741816)
r['inherited_bytes']=b.raw[:n.value].decode('ascii','replace')
print(json.dumps(r))
print('stderr-capture-ok',file=sys.stderr)
'''
            run = ac.run_appcontainer([str(runtime / "python.exe"), "-I", "-c", code], cwd=work, env=env, allowed_dirs=[(runtime, False), (work, True)], timeout_ms=10000)
            assert run.returncode == 0, (run.returncode, run.stderr)
            data = json.loads(run.stdout)
            assert data["token_is_appcontainer"] and data["stdin_eof"]
            assert data["direct_errno"] == 13 and not data["inherited_read_ok"] and not data["inherited_bytes"] and data["inherited_invalid_handle"]
            assert run.stderr.strip() == b"stderr-capture-ok"
            result["checks"]["inherited_handle"] = {**data, "returncode": run.returncode, "stderr_capture": True}
        finally:
            os.close(fd)
        result["checks"]["timeout_tree"] = tree_check(env, False)
        result["checks"]["normal_root_exit_tree"] = tree_check(env, True)
        marker = work / "must-not-run.txt"
        with patch.object(ac.WindowsJob, "assign_handle", side_effect=OSError("synthetic assignment failure")):
            try:
                ac.run_appcontainer([str(runtime / "python.exe"), "-I", "-c", f"from pathlib import Path;Path({str(marker)!r}).write_text('ran')"], cwd=work, env=env, allowed_dirs=[], timeout_ms=10000)
                raise AssertionError("Assignment failure was swallowed")
            except OSError as exc:
                assert "synthetic assignment failure" in str(exc)
        assert not marker.exists()
        result["checks"]["assignment_fail_closed"] = {"child_code_executed": False}
        before = wintypes.DWORD()
        after = wintypes.DWORD()
        assert k.GetProcessHandleCount(k.GetCurrentProcess(), ctypes.byref(before))
        ac.run_appcontainer([str(runtime / "python.exe"), "-I", "-c", "print('handle-count-check')"], cwd=work, env=env, allowed_dirs=[], timeout_ms=10000)
        assert k.GetProcessHandleCount(k.GetCurrentProcess(), ctypes.byref(after))
        result["checks"]["parent_handle_count"] = {"before": before.value, "after": after.value, "delta": after.value - before.value}
        assert after.value == before.value
        leftovers = list(work.glob(".ac-*.tmp"))
        result["checks"]["capture_temp_files_left"] = [str(p) for p in leftovers]
        assert not leftovers
        result["status"] = "PASS_TWO_FIXES_ONLY"
except Exception as exc:
    result["status"] = "FAIL"
    result["error"] = {"type": type(exc).__name__, "detail": str(exc)}
finally:
    if created:
        result["delete_hresult"] = delete(profile_name)
        result["profile_exists_after_cleanup"] = profile.exists() if profile else None
        if result["delete_hresult"] != 0 or result["profile_exists_after_cleanup"]:
            result["status"] = "FAIL"
    result["source_sha256"] = {rel: hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() for rel in ("src/animtrain/appcontainer.py", "src/animtrain/win_job.py")}
    (OUT / "native-results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
sys.exit(0 if result.get("status") == "PASS_TWO_FIXES_ONLY" else 1)
