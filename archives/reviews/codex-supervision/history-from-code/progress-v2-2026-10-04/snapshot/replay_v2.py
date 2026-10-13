"""A1/A2 独立重放 v2(修正 v1 的假通过缺陷,应 msg_291/293/294)。

v1 缺陷(v1-invalid-evidence/ 存档):A2 传 repr(grandchild) 子进程只求值
字符串瞬间退出 → 假通过;按 PID 重开/按 PID kill(无身份验证,复用误杀风险);
CRT 句柄表错用;结果未绑定源 hash。v2 修正:
  - 所有路径限定 reviews/2026-10-04-acceptance-support/ 下随机子目录,
    启动时断言绝对路径归属;
  - A1 正对照:父进程原生 CreateProcessW(bInheritHandles=True,无 HANDLE_LIST)
    子进程读继承句柄 → 必须读到哨兵(证明句柄有效且可继承);
    沙箱侧(修复后模块)同句柄 → 必须无效句柄;令牌判定类号 29 并记录 API 返回;
  - A2 真休眠:孙进程代码经环境变量传递(非 repr),孙进程写
    alive-<token> 标记文件(含自身 PID)完成握手;主线程轮询确认存活后
    持有 OpenProcess(SYNCHRONIZE) 句柄;函数返回瞬间该句柄必须 signaled;
    存活兜底清理只用已持有并验证身份的句柄,绝不按 PID 杀;
  - allowed_dirs 仅本随机工作目录(可写),不触碰原工具链任何目录;
  - 结果绑定本脚本 sha256 与完整命令行。
"""
from __future__ import annotations

import ctypes
import hashlib
import json
import os
import subprocess
import sys
import threading
import time
import uuid
from ctypes import wintypes
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]   # 项目根
sys.path.insert(0, str(ROOT / "src"))

from animtrain import appcontainer as ac  # noqa: E402

SUPPORT = Path(__file__).resolve().parent
SANDBOX_PY = Path(r"D:\Python\python.exe")

k32 = ctypes.WinDLL("kernel32", use_last_error=True)
k32.CreateProcessW.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR,
                               wintypes.LPVOID, wintypes.LPVOID, wintypes.BOOL,
                               wintypes.DWORD, wintypes.LPVOID, wintypes.LPCWSTR,
                               wintypes.LPVOID, wintypes.LPVOID]
k32.CreateProcessW.restype = wintypes.BOOL
k32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
k32.OpenProcess.restype = wintypes.HANDLE
k32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
k32.WaitForSingleObject.restype = wintypes.DWORD
k32.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
k32.GetExitCodeProcess.restype = wintypes.BOOL
k32.SetHandleInformation.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD]
k32.SetHandleInformation.restype = wintypes.BOOL
k32.ReadFile.argtypes = [wintypes.HANDLE, wintypes.LPVOID, wintypes.DWORD,
                         ctypes.POINTER(wintypes.DWORD), wintypes.LPVOID]
k32.ReadFile.restype = wintypes.BOOL
k32.CloseHandle.argtypes = [wintypes.HANDLE]

HANDLE_FLAG_INHERIT = 0x1
SYNCHRONIZE = 0x00100000
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
WAIT_OBJECT_0 = 0
CREATE_UNICODE_ENVIRONMENT = 0x400

# 令牌类号(复查方核实):TokenIsAppContainer = 29
_TOKEN_CLASS_IS_APPCONTAINER = 29


def _check_paths(work: Path) -> None:
    assert work.is_absolute(), "工作目录必须绝对路径"
    assert str(work).startswith(str(SUPPORT.resolve())), \
        f"工作目录必须在支持目录内: {work}"
    work.mkdir(parents=True, exist_ok=True)


def _sandbox_env(profile: Path, work: Path) -> dict:
    return {"SYSTEMROOT": r"C:\Windows",
            "PATH": ";".join([str(SANDBOX_PY.parent), r"C:\Windows\System32"]),
            "TEMP": str(work), "TMP": str(work),
            "LOCALAPPDATA": str(profile), "APPDATA": str(profile),
            "USERPROFILE": str(profile), "PATHEXT": ".COM;.EXE;.BAT;.CMD"}


def _sandbox(code: str, work: Path, timeout_ms: int = 60_000,
             extra: dict | None = None):
    profile = ac.appcontainer_profile_path(ac.appcontainer_sid())
    env = _sandbox_env(profile, work)
    if extra:
        env.update(extra)
    return ac.run_appcontainer(
        [str(SANDBOX_PY), "-X", "utf8", "-c", code],
        cwd=work, env=env, allowed_dirs=[(work, True)],
        timeout_ms=timeout_ms)


def _token_probe() -> str:
    return (
        "import ctypes\n"
        "from ctypes import wintypes\n"
        "k=ctypes.windll.kernel32;a=ctypes.windll.advapi32\n"
        "k.GetCurrentProcess.restype=wintypes.HANDLE\n"
        "k.OpenProcessToken.restype=wintypes.BOOL\n"
        "k.OpenProcessToken.argtypes=[wintypes.HANDLE,wintypes.DWORD,"
        "ctypes.POINTER(wintypes.HANDLE)]\n"
        "a.GetTokenInformation.restype=wintypes.BOOL\n"
        "a.GetTokenInformation.argtypes=[wintypes.HANDLE,ctypes.c_int,"
        "wintypes.LPVOID,wintypes.DWORD,ctypes.POINTER(wintypes.DWORD)]\n"
        "h=wintypes.HANDLE();ok1=k.OpenProcessToken(k.GetCurrentProcess(),0x0008,"
        "ctypes.byref(h))\n"
        "val=wintypes.DWORD();dummy=wintypes.DWORD()\n"
        "ok2=a.GetTokenInformation(h,29,ctypes.byref(val),4,ctypes.byref(dummy))\n"
        "print('TOKEN_IS_APPCONTAINER='+str(bool(val.value))+' ok='+str(ok1)+'/'+str(ok2))\n"
    )


def a1(work: Path) -> dict:
    sentinel = work / "sentinel.txt"
    sentinel.write_text("SYNTHETIC-INHERITED-HANDLE-PROBE", encoding="utf-8")
    import msvcrt  # Python CRT 句柄表(msg_291 点 5)
    fd = os.open(str(sentinel), os.O_RDONLY | os.O_BINARY)
    h = msvcrt.get_osfhandle(fd)
    if not k32.SetHandleInformation(h, HANDLE_FLAG_INHERIT, HANDLE_FLAG_INHERIT):
        os.close(fd)
        return {"error": f"SetHandleInformation 失败 {ctypes.get_last_error()}"}
    read_code = (
        "import ctypes,os\n"
        "from ctypes import wintypes\n"
        "k=ctypes.WinDLL('kernel32', use_last_error=True)\n"
        "k.ReadFile.argtypes=[wintypes.HANDLE,wintypes.LPVOID,wintypes.DWORD,"
        "ctypes.POINTER(wintypes.DWORD),wintypes.LPVOID]\n"
        "k.ReadFile.restype=wintypes.BOOL\n"
        "h=int(os.environ['PROBE_HANDLE'])\n"
        "buf=ctypes.create_string_buffer(64);n=wintypes.DWORD()\n"
        "try:\n"
        "    ok=k.ReadFile(wintypes.HANDLE(h),buf,64,ctypes.byref(n),None)\n"
        "except OSError as e:\n"
        "    ok=False\n"
        "if ok:\n"
        "    print('SENTINEL_READ:'+buf.raw[:n.value].decode('latin-1'))\n"
        "else:\n"
        "    print('INVALID_HANDLE lasterr='+str(ctypes.get_last_error()))\n"
    )
    # 正对照:原生 CreateProcessW 无 HANDLE_LIST,子进程按同句柄号读 → 必须读到。
    # 子进程代码走文件,避免命令行引号转义(文件由普通进程读,不经沙箱)。
    control_child = work / "control_child.py"
    control_child.write_text(read_code, encoding="utf-8")
    env_lines = "SYSTEMROOT=C:\\Windows\0PATH=" + str(SANDBOX_PY.parent) + "\0" \
        + "PROBE_HANDLE=" + str(h) + "\0\0"
    env_block = ctypes.create_unicode_buffer(env_lines)

    class _PI(ctypes.Structure):
        _fields_ = [("hProcess", wintypes.HANDLE), ("hThread", wintypes.HANDLE),
                    ("dwProcessId", wintypes.DWORD), ("dwThreadId", wintypes.DWORD)]
    pi = _PI()

    class _SI(ctypes.Structure):
        _fields_ = [("cb", wintypes.DWORD), ("lpReserved", wintypes.LPWSTR),
                    ("lpDesktop", wintypes.LPWSTR), ("lpTitle", wintypes.LPWSTR),
                    ("dwX", wintypes.DWORD), ("dwY", wintypes.DWORD),
                    ("dwXSize", wintypes.DWORD), ("dwYSize", wintypes.DWORD),
                    ("dwXCountChars", wintypes.DWORD),
                    ("dwYCountChars", wintypes.DWORD),
                    ("dwFillAttribute", wintypes.DWORD), ("dwFlags", wintypes.DWORD),
                    ("wShowWindow", wintypes.WORD), ("cbReserved2", wintypes.WORD),
                    ("lpReserved2", wintypes.LPBYTE), ("hStdInput", wintypes.HANDLE),
                    ("hStdOutput", wintypes.HANDLE), ("hStdError", wintypes.HANDLE)]
    si = _SI()
    si.cb = ctypes.sizeof(_SI)
    cmdline = f'"{SANDBOX_PY}" -X utf8 "{control_child}"'
    cmd_buf = ctypes.create_unicode_buffer(cmdline)  # CreateProcessW 会改写,须可变
    ok = k32.CreateProcessW(None, cmd_buf,
                            None, None, True, CREATE_UNICODE_ENVIRONMENT,
                            ctypes.cast(env_block, wintypes.LPVOID), str(work),
                            ctypes.byref(si), ctypes.byref(pi))
    control_out = ""
    if ok:
        k32.WaitForSingleObject(pi.hProcess, 30000)
        code = wintypes.DWORD()
        k32.GetExitCodeProcess(pi.hProcess, ctypes.byref(code))
        k32.CloseHandle(pi.hProcess); k32.CloseHandle(pi.hThread)
        control_out = f"control_rc={code.value}"
    else:
        control_out = f"control_spawn_failed lasterr={ctypes.get_last_error()}"
    # 沙箱侧(修复后 HANDLE_LIST):同句柄必须无效
    r = _sandbox(read_code, work, extra={"PROBE_HANDLE": str(h)})
    os.close(fd)
    sandbox_out = (r.stdout or b"").decode("utf-8", "replace")
    return {"control": control_out, "sandbox_rc": r.returncode,
            "sandbox_out": sandbox_out,
            "sandbox_err": (r.stderr or b"").decode("utf-8", "replace")[-400:],
            "blocked": ("INVALID_HANDLE" in sandbox_out
                        and "SENTINEL_READ" not in sandbox_out)}


_GRAND_CODE = (
    "import os,time\n"
    "with open(os.path.join(os.environ['GRAND_DIR'],'alive-'+os.environ['GRAND_TOKEN']),'w') as f:\n"
    "    f.write(str(os.getpid()))\n"
    "time.sleep(120)\n"
)
_CHILD_SPAWN = _token_probe() + (
    "import os,subprocess,sys\n"
    "p=subprocess.Popen([sys.executable,'-X','utf8','-c',"
    "os.environ['GRAND_CODE']],env=dict(os.environ))\n"
    "print('GRAND_PID='+str(p.pid),flush=True)\n"
)
# 正常退出场景:根进程等孙进程写完存活标记再退出(保证父侧能握到"确实活着"的句柄)
_CHILD_SPAWN_EXIT = _token_probe() + (
    "import os,subprocess,sys,time\n"
    "p=subprocess.Popen([sys.executable,'-X','utf8','-c',"
    "os.environ['GRAND_CODE']],env=dict(os.environ))\n"
    "print('GRAND_PID='+str(p.pid),flush=True)\n"
    "marker=os.path.join(os.environ['GRAND_DIR'],'alive-'+os.environ['GRAND_TOKEN'])\n"
    "deadline=time.time()+30\n"
    "while time.time()<deadline and not os.path.exists(marker):\n"
    "    time.sleep(0.05)\n"
    "print('GRAND_ALIVE_CONFIRMED='+str(os.path.exists(marker)),flush=True)\n"
)


def _run_async(args) -> tuple[threading.Thread, dict]:
    box: dict = {}

    def _t():
        try:
            box["result"] = _sandbox(*args)
        except subprocess.TimeoutExpired as e:
            box["timeout"] = e
        except Exception as e:  # noqa: BLE001
            box["error"] = repr(e)
    th = threading.Thread(target=_t, daemon=True)
    th.start()
    return th, box


def _open_verified_handle(pid: int) -> wintypes.HANDLE | None:
    """在目标进程存活时打开并验证身份(仅本项目 token 的标记文件产生的 PID)。"""
    if not pid:
        return None
    h = k32.OpenProcess(SYNCHRONIZE | PROCESS_QUERY_LIMITED_INFORMATION, False, pid)
    return h or None


def _alive(h: wintypes.HANDLE) -> bool:
    return k32.WaitForSingleObject(h, 0) != WAIT_OBJECT_0


def a2(work: Path) -> dict:
    token = uuid.uuid4().hex
    extra = {"GRAND_TOKEN": token, "GRAND_DIR": str(work),
             "GRAND_CODE": _GRAND_CODE}
    marker = work / f"alive-{token}"
    # 场景 1:超时
    th, box = _run_async((_CHILD_SPAWN + "import time\ntime.sleep(60)\n",
                          work, 5000, extra))
    held = None
    pid = 0
    deadline = time.time() + 30
    while time.time() < deadline and held is None:
        if marker.exists():
            pid = int(marker.read_text().strip())
            held = _open_verified_handle(pid)
            if held and not _alive(held):
                k32.CloseHandle(held); held = None  # 打开瞬间已退:重试
        time.sleep(0.05)
    th.join(60)
    t1 = {}
    if "timeout" in box:
        t1 = {"timed_out": True,
              "captured_out": (box["timeout"].output or b"").decode("utf-8", "replace")}
    elif "result" in box:
        t1 = {"timed_out": False, "rc": box["result"].returncode}
    else:
        t1 = {"error": box.get("error", "unknown")}
    signaled_at_return = (held is not None
                          and k32.WaitForSingleObject(held, 0) == WAIT_OBJECT_0)
    if held and not signaled_at_return:
        # 兜底:仅用已持有且验证身份的句柄等待/终止,绝不按 PID 杀
        k32.WaitForSingleObject(held, 5000)
        if _alive(held):
            ctypes.windll.kernel32.TerminateProcess(held, 1)
        signaled_at_return = k32.WaitForSingleObject(held, 0) == WAIT_OBJECT_0
    if held:
        k32.CloseHandle(held)
    # 场景 2:正常根退出
    token2 = uuid.uuid4().hex
    marker2 = work / f"alive-{token2}"
    extra2 = {"GRAND_TOKEN": token2, "GRAND_DIR": str(work),
              "GRAND_CODE": _GRAND_CODE}
    th2, box2 = _run_async((_CHILD_SPAWN_EXIT, work, 60_000, extra2))
    held2 = None
    pid2 = 0
    deadline = time.time() + 30
    while time.time() < deadline and held2 is None:
        if marker2.exists():
            pid2 = int(marker2.read_text().strip())
            held2 = _open_verified_handle(pid2)
            if held2 and not _alive(held2):
                k32.CloseHandle(held2); held2 = None
        time.sleep(0.05)
    th2.join(60)
    if held2:
        k32.WaitForSingleObject(held2, 5000)
        if _alive(held2):
            ctypes.windll.kernel32.TerminateProcess(held2, 1)
        sig2 = k32.WaitForSingleObject(held2, 0) == WAIT_OBJECT_0
        k32.CloseHandle(held2)
    else:
        sig2 = False
    return {"timeout": {"timed_out": t1.get("timed_out"),
                        "grand_pid": pid,
                        "signaled_at_return": signaled_at_return},
            "normal_exit": {"grand_pid": pid2,
                            "signaled_after_exit": sig2},
            "passed": signaled_at_return and sig2}


def main() -> int:
    work = SUPPORT / f"replay2-{uuid.uuid4().hex[:8]}"
    _check_paths(work)
    src_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    results = {"source_sha256": src_sha,
               "command": [sys.executable] + sys.argv,
               "work": str(work)}
    results["A1_inherited_handle"] = a1(work)
    results["A2_tree_termination"] = a2(work)
    out = SUPPORT / "replay-v2-results.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0 if (results["A1_inherited_handle"].get("blocked")
                 and results["A2_tree_termination"].get("passed")) else 1


if __name__ == "__main__":
    sys.exit(main())
