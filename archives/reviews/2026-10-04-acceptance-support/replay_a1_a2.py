"""A1/A2 独立重放(修复后模块,只读使用;零新增 ACL)。

A1:父进程持可继承文件句柄 → 沙箱子进程按句柄号读取,必须无效句柄(修复前可读)。
A2:超时/正常根退出后,受控孙进程必须全部退出(修复前残留)。
独立运行目录 reviews/2026-10-04-acceptance-support/replay-work;
allowed_dirs=[] 不再追加任何 ACL;profile 为已存在生产 profile。
"""
from __future__ import annotations

import ctypes
import json
import subprocess
import sys
import time
from ctypes import wintypes
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]   # 项目根(reviews/…/文件 → [2]=项目根)
sys.path.insert(0, str(ROOT / "src"))

from animtrain import appcontainer as ac  # noqa: E402

WORK = ROOT / "replay-work"
SANDBOX_PY = Path(r"D:\Python\python.exe")

k32 = ctypes.WinDLL("kernel32", use_last_error=True)
k32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
k32.OpenProcess.restype = wintypes.HANDLE
k32.SetHandleInformation.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.DWORD]
k32.SetHandleInformation.restype = wintypes.BOOL
k32.CloseHandle.argtypes = [wintypes.HANDLE]
HANDLE_FLAG_INHERIT = 0x00000001
SYNCHRONIZE = 0x00100000
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000


def base_env() -> dict:
    profile = ac.appcontainer_profile_path(ac.appcontainer_sid())
    return {
        "SYSTEMROOT": r"C:\Windows",
        "PATH": ";".join([r"D:\Python", r"D:\Settings\ffmpeg\bin",
                          r"D:\Settings\miktex\miktex\bin\x64",
                          r"C:\Windows\System32"]),
        "TEMP": str(WORK), "TMP": str(WORK),
        "LOCALAPPDATA": str(profile), "APPDATA": str(profile),
        "USERPROFILE": str(profile),
        "PATHEXT": ".COM;.EXE;.BAT;.CMD",
    }


def sandbox(code: str, timeout_ms: int = 60_000, extra: dict | None = None):
    env = base_env()
    if extra:
        env.update(extra)
    return ac.run_appcontainer(
        [str(SANDBOX_PY), "-X", "utf8", "-c", code],
        cwd=WORK, env=env, allowed_dirs=[], timeout_ms=timeout_ms)


def a1_inherited_handle() -> dict:
    """父进程可继承句柄不得被子进程读取。"""
    sentinel = WORK / "sentinel.txt"
    sentinel.write_text("SYNTHETIC-INHERITED-HANDLE-PROBE", encoding="utf-8")
    import os
    fd = os.open(str(sentinel), os.O_RDONLY | os.O_BINARY)
    h = ctypes.windll.msvcrt._get_osfhandle(fd)  # type: ignore[attr-defined]
    k32.SetHandleInformation(h, HANDLE_FLAG_INHERIT, HANDLE_FLAG_INHERIT)
    code = (
        "import ctypes,os\n"
        "from ctypes import wintypes\n"
        "k=ctypes.windll.kernel32\n"
        "h=int(os.environ['PROBE_HANDLE'])\n"
        "buf=ctypes.create_string_buffer(64);n=wintypes.DWORD()\n"
        "ok=k.ReadFile(wintypes.HANDLE(h),buf,64,ctypes.byref(n),None)\n"
        "if ok:\n"
        "    print('SENTINEL_READ:'+buf.raw[:n.value].decode('latin-1'))\n"
        "else:\n"
        "    print('INVALID_HANDLE err='+str(ctypes.get_last_error()))\n"
    )
    r = sandbox(code, extra={"PROBE_HANDLE": str(h)})
    os.close(fd)
    out = (r.stdout or b"").decode("utf-8", "replace")
    return {"rc": r.returncode, "out": out,
            "blocked": "INVALID_HANDLE" in out and "SENTINEL_READ" not in out}


def a2_tree_termination() -> dict:
    """超时与正常根退出后孙进程必须消失。"""
    grandchild = ("import time\ntime.sleep(120)\n")
    spawn = (
        "import subprocess,sys,time\n"
        "p=subprocess.Popen([sys.executable,'-X','utf8','-c',"
        "repr(%r)],creationflags=0)\n" % grandchild +
        "print('GRANDCHILD_PID='+str(p.pid),flush=True)\n"
        "time.sleep(60)\n"
    )
    # 场景 1:超时
    t0 = time.time()
    try:
        sandbox(spawn, timeout_ms=5_000)
        timeout_result = {"timed_out": False, "out": ""}
    except subprocess.TimeoutExpired as e:
        timeout_result = {"timed_out": True,
                          "out": (e.output or b"").decode("utf-8", "replace")}
    pid_line = [l for l in timeout_result["out"].splitlines()
                if l.startswith("GRANDCHILD_PID=")]
    pid = int(pid_line[0].split("=")[1]) if pid_line else 0
    alive_after_timeout = _pid_alive(pid)
    if alive_after_timeout:
        _kill(pid)
    # 场景 2:正常根退出(根立即退出,孙 sleep)
    spawn_exit = (
        "import subprocess,sys\n"
        "p=subprocess.Popen([sys.executable,'-X','utf8','-c',"
        "repr(%r)],creationflags=0)\n" % grandchild +
        "print('GRANDCHILD_PID='+str(p.pid),flush=True)\n"
    )
    r = sandbox(spawn_exit, timeout_ms=30_000)
    out2 = (r.stdout or b"").decode("utf-8", "replace")
    pid2 = int([l for l in out2.splitlines()
                if l.startswith("GRANDCHILD_PID=")][0].split("=")[1])
    time.sleep(1.0)  # 留出树清理窗口
    alive_after_exit = _pid_alive(pid2)
    if alive_after_exit:
        _kill(pid2)
    return {"timeout": {"timed_out": timeout_result["timed_out"],
                        "grandchild_pid": pid,
                        "alive_after_timeout": alive_after_timeout},
            "normal_exit": {"grandchild_pid": pid2,
                            "alive_after_exit": alive_after_exit},
            "passed": (not alive_after_timeout) and (not alive_after_exit)}


def _pid_alive(pid: int) -> bool:
    if not pid:
        return False
    h = k32.OpenProcess(SYNCHRONIZE | PROCESS_QUERY_LIMITED_INFORMATION,
                        False, pid)
    if not h:
        return False  # 打不开 = 已退出
    alive = k32.WaitForSingleObject(h, 0) != 0
    k32.CloseHandle(h)
    return alive


def _kill(pid: int) -> None:
    h = k32.OpenProcess(0x0001, False, pid)
    if h:
        ctypes.windll.kernel32.TerminateProcess(h, 1)
        k32.CloseHandle(h)


def main() -> int:
    WORK.mkdir(parents=True, exist_ok=True)
    r1 = a1_inherited_handle()
    r2 = a2_tree_termination()
    results = {"A1_inherited_handle": r1, "A2_tree_termination": r2}
    (WORK.parent / "replay-results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0 if (r1["blocked"] and r2["passed"]) else 1


if __name__ == "__main__":
    sys.exit(main())
