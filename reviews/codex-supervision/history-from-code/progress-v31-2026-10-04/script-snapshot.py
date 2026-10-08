"""A1/A2 独立重放 v3(应 msg_299/300):严格判定收敛为纯谓词 + 四项失败回归。

v2 判定漏洞(复查方纯 AST 反例,predicate-counterexamples.json/SUPERVISION_REPORT.md):
  1. A1 正对照启动失败或 rc0 无精确哨兵证据,blocked 仍 True;
  2. A1 任意 OSError 都记 INVALID_HANDLE,未保存真实 winerror(v2 实测 lasterr=0
     系读错实例:应读同实例 k.get_last_error(),而非模块级 ctypes.get_last_error());
  3. A2 超时分支兜底清理后重赋值 signaled_at_return → 假通过;
  4. A2 passed 未要求 timed_out=True、正常退出 rc0、令牌成功、线程结束、
     握手身份核验、监督端 ACK。
v3:
  - 判定全部收敛为纯谓词 _judge_a1/_judge_a2(只吃观测值,可 AST 独立复核);
  - 返回瞬间 signaled 只赋值一次,兜底清理单独记录(cleanup),结构上不进判定;
  - 握手=OpenProcess(SYNCHRONIZE|QUERY_LIMITED)+打开时存活+映像路径核验;
  - 正常退出场景根进程须看到监督端 ACK 才退出(ACK_SEEN=True);
  - 四项失败回归 N1-N4(合成输入断言必须 FAIL)随主流程执行;
  - 结果绑定本脚本+appcontainer.py+win_job.py 三份 sha256。
v3.1(应 msg_302):
  - 存活判定只认 WAIT_TIMEOUT;WaitForSingleObject=WAIT_FAILED(0xFFFFFFFF)
    记录错误并 FAIL,新增 N5;
  - _judge_a1 增加 sandbox_rc==0 要求与正对照 Wait=WAIT_OBJECT_0/
    GetExitCodeProcess API 成功要求,新增 N6;
  - 握手时即持有 SYNCHRONIZE|QUERY|PROCESS_TERMINATE 并核验映像,
    cleanup 只用已持有句柄 Terminate/Wait,不按 PID 重开,失败错误如实保存;
  - 更正 v2 last_error 归因:子进程 ReadFile 失败后直接调用 GetLastError
    API 立即捕获(或 WinDLL(use_last_error=True)+ctypes.get_last_error())。
范围:仅支持目录随机子目录,零新增原工具链 ACL,不改四个核心/测试文件。
"""
from __future__ import annotations

import ctypes
import hashlib
import json
import os
import re
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
SENTINEL = "SYNTHETIC-INHERITED-HANDLE-PROBE"

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
k32.CloseHandle.argtypes = [wintypes.HANDLE]
k32.QueryFullProcessImageNameW.argtypes = [wintypes.HANDLE, wintypes.DWORD,
                                           wintypes.LPWSTR,
                                           ctypes.POINTER(wintypes.DWORD)]
k32.QueryFullProcessImageNameW.restype = wintypes.BOOL
k32.TerminateProcess.argtypes = [wintypes.HANDLE, wintypes.UINT]
k32.TerminateProcess.restype = wintypes.BOOL

HANDLE_FLAG_INHERIT = 0x1
SYNCHRONIZE = 0x00100000
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
PROCESS_TERMINATE = 0x0001
WAIT_OBJECT_0 = 0
WAIT_TIMEOUT = 0x102
WAIT_FAILED = 0xFFFFFFFF
CREATE_UNICODE_ENVIRONMENT = 0x400
STARTF_USESTDHANDLES = 0x100

# 令牌类号(复查方核实):TokenIsAppContainer = 29
_TOKEN_CLASS_IS_APPCONTAINER = 29
# "已确认的无效句柄错误"类:6=ERROR_INVALID_HANDLE / 5=ERROR_ACCESS_DENIED /
# 0xC0000008=STATUS_INVALID_HANDLE(本机沙箱实测以 OSError 抛出,
# winerror 为负数形式 -1073741816,须 & 0xFFFFFFFF 归一)。
# 三者均证明该句柄在沙箱内不可读;0 或其它值一律不构成阻断证据。
_CONFIRMED_HANDLE_ERRORS = {5, 6, 0xC0000008}
_TOKEN_RE = re.compile(r"TOKEN_IS_APPCONTAINER=1 ok=1/1")


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
        "k.CloseHandle.argtypes=[wintypes.HANDLE]\n"
        "a.GetTokenInformation.restype=wintypes.BOOL\n"
        "a.GetTokenInformation.argtypes=[wintypes.HANDLE,ctypes.c_int,"
        "wintypes.LPVOID,wintypes.DWORD,ctypes.POINTER(wintypes.DWORD)]\n"
        "h=wintypes.HANDLE();ok1=k.OpenProcessToken(k.GetCurrentProcess(),0x0008,"
        "ctypes.byref(h))\n"
        "val=wintypes.DWORD();dummy=wintypes.DWORD()\n"
        "ok2=a.GetTokenInformation(h,29,ctypes.byref(val),4,ctypes.byref(dummy))\n"
        "print('TOKEN_IS_APPCONTAINER='+str(int(val.value))+' ok='"
        "+str(int(ok1))+'/'+str(int(ok2)),flush=True)\n"
        "k.CloseHandle(h)\n"
    )


# 读句柄子进程代码(正对照与沙箱共用):ReadFile 失败后立即直接调用
# GetLastError API 捕获真实 winerror(v2 得 0 系错误来源读错;正确做法即
# 直接调 GetLastError,或 WinDLL(use_last_error=True)+ctypes.get_last_error() 立即捕获)。
_READ_CODE = (
    "import ctypes,os\n"
    "from ctypes import wintypes\n"
    "k=ctypes.windll.kernel32\n"
    "k.ReadFile.argtypes=[wintypes.HANDLE,wintypes.LPVOID,wintypes.DWORD,"
    "ctypes.POINTER(wintypes.DWORD),wintypes.LPVOID]\n"
    "k.ReadFile.restype=wintypes.BOOL\n"
    "h=int(os.environ['PROBE_HANDLE'])\n"
    "buf=ctypes.create_string_buffer(64);n=wintypes.DWORD()\n"
    "try:\n"
    "    ok=k.ReadFile(wintypes.HANDLE(h),buf,64,ctypes.byref(n),None)\n"
    "    err=k.GetLastError()\n"
    "except OSError as e:\n"
    "    ok=False;err=(e.winerror & 0xFFFFFFFF)\n"
    "if ok:\n"
    "    print('SENTINEL_READ:'+buf.raw[:n.value].decode('latin-1'),flush=True)\n"
    "else:\n"
    "    print('READ_ERROR winerror='+str(err),flush=True)\n"
)


# ---------------------------------------------------------------- 纯判定谓词

def _is_alive_wait(wait_result: int) -> bool:
    """存活判定(应 msg_302):只有 WAIT_TIMEOUT(0x102)表示存活;
    WAIT_OBJECT_0=已结束;WAIT_FAILED(0xFFFFFFFF)是错误,绝不判活。"""
    return wait_result == WAIT_TIMEOUT


def _judge_a1(*, control_spawned: bool, control_waited: bool,
              control_rc_read: bool, control_rc: int | None,
              control_read: str | None, sandbox_rc: int | None,
              sandbox_winerror: int | None, token_ok: bool,
              sandbox_out: str) -> dict:
    """A1 通过条件:正对照 Wait=WAIT_OBJECT_0、GetExitCodeProcess API 成功、
    rc0 且读到精确哨兵;沙箱必须 rc0、令牌确认、确认类句柄错误,
    且绝无哨兵内容。所有输入为观测值,无副作用。"""
    control_good = bool(control_spawned and control_waited and control_rc_read
                        and control_rc == 0 and control_read == SENTINEL)
    sandbox_blocked = bool("SENTINEL_READ" not in sandbox_out
                           and token_ok
                           and sandbox_rc == 0
                           and sandbox_winerror in _CONFIRMED_HANDLE_ERRORS)
    return {"blocked": control_good and sandbox_blocked,
            "control_good": control_good,
            "sandbox_blocked": sandbox_blocked}


def _judge_a2(timeout_sc: dict, exit_sc: dict) -> dict:
    """A2 通过条件:超时场景 timed_out=True;退出场景 rc==0;两场景均要求
    返回瞬间 signaled、握手身份核验、令牌 1/1、线程确实结束;退出场景
    还要求根进程看到监督端 ACK。cleanup 字段不参与判定(结构上无法掩盖)。"""
    t_ok = (timeout_sc["timed_out"] is True
            and timeout_sc["signaled_at_return"] is True
            and timeout_sc["handshake"]["verified"] is True
            and timeout_sc["token_ok"] is True
            and timeout_sc["thread_finished"] is True)
    e_ok = (exit_sc["rc"] == 0
            and exit_sc["signaled_at_return"] is True
            and exit_sc["handshake"]["verified"] is True
            and exit_sc["token_ok"] is True
            and exit_sc["thread_finished"] is True
            and exit_sc["ack_received"] is True)
    return {"passed": t_ok and e_ok, "timeout_ok": t_ok, "exit_ok": e_ok}


def _negative_regressions() -> dict:
    """四项失败回归(应 msg_296/297):合成输入断言必须 FAIL。"""
    cases = []

    def _rec(name: str, actual: bool) -> None:
        cases.append({"name": name, "expect_pass": False,
                      "actual_pass": actual, "holds": actual is False})

    # N1 正对照启动失败:沙箱侧哪怕输出确认类错误也必须 FAIL
    r = _judge_a1(control_spawned=False, control_waited=True,
                  control_rc_read=True, control_rc=0, control_read=SENTINEL,
                  sandbox_rc=0, sandbox_winerror=6, token_ok=True,
                  sandbox_out="READ_ERROR winerror=6")
    _rec("N1 正对照启动失败", r["blocked"])
    # N2 正对照 rc0 但哨兵不匹配/缺失
    r = _judge_a1(control_spawned=True, control_waited=True,
                  control_rc_read=True, control_rc=0, control_read="WRONG-BYTES",
                  sandbox_rc=0, sandbox_winerror=6, token_ok=True,
                  sandbox_out="READ_ERROR winerror=6")
    _rec("N2 哨兵不匹配", r["blocked"])
    # N3 未真正超时(正常 rc 返回)但两状态 True → 必须 FAIL
    t = {"timed_out": False, "signaled_at_return": True,
         "handshake": {"verified": True}, "token_ok": True,
         "thread_finished": True}
    e = {"rc": 0, "signaled_at_return": True,
         "handshake": {"verified": True}, "token_ok": True,
         "thread_finished": True, "ack_received": True}
    _rec("N3 未真正超时", _judge_a2(t, e)["passed"])
    # N4 返回时未退出、人工清理后才退出(清理结果完整但不得进判定)→ 必须 FAIL
    t = {"timed_out": True, "signaled_at_return": False,
         "handshake": {"verified": True}, "token_ok": True,
         "thread_finished": True,
         "cleanup": {"terminate_attempted": True, "terminate_ok": True}}
    e = {"rc": 0, "signaled_at_return": False,
         "handshake": {"verified": True}, "token_ok": True,
         "thread_finished": True, "ack_received": True,
         "cleanup": {"terminate_attempted": True, "terminate_ok": True}}
    _rec("N4 返回时未清理(人工清理后退出)", _judge_a2(t, e)["passed"])
    # N5(应 msg_302):WaitForSingleObject=WAIT_FAILED 是错误,不得判活;
    # WAIT_OBJECT_0 也不得判活;WAIT_TIMEOUT 才判活
    _rec("N5 WAIT_FAILED 不得判活(仅 WAIT_TIMEOUT 判活)",
         _is_alive_wait(WAIT_FAILED) or _is_alive_wait(WAIT_OBJECT_0)
         or not _is_alive_wait(WAIT_TIMEOUT))
    # N6(应 msg_302):令牌+拒绝输出齐但沙箱子进程异常退出(rc!=0)→ 必须 FAIL
    r = _judge_a1(control_spawned=True, control_waited=True,
                  control_rc_read=True, control_rc=0, control_read=SENTINEL,
                  sandbox_rc=1, sandbox_winerror=6, token_ok=True,
                  sandbox_out="READ_ERROR winerror=6")
    _rec("N6 沙箱子进程异常退出(rc!=0)", r["blocked"])
    return {"cases": cases, "all_hold": all(c["holds"] for c in cases)}


# ------------------------------------------------------------------ A1 场景

def a1(work: Path) -> dict:
    sentinel = work / "sentinel.txt"
    sentinel.write_text(SENTINEL, encoding="utf-8")
    import msvcrt  # Python CRT 句柄表(msg_291 点 5)
    fd = os.open(str(sentinel), os.O_RDONLY | os.O_BINARY)
    h = msvcrt.get_osfhandle(fd)
    if not k32.SetHandleInformation(h, HANDLE_FLAG_INHERIT, HANDLE_FLAG_INHERIT):
        os.close(fd)
        return {"error": f"SetHandleInformation 失败 {k32.get_last_error()}"}
    # 正对照:原生 CreateProcessW(bInheritHandles=True,无 HANDLE_LIST),
    # 子进程按同句柄号读 → 必须读到精确哨兵;stdout/stderr 落盘供逐字节核验。
    control_child = work / "control_child.py"
    control_child.write_text(_READ_CODE, encoding="utf-8")
    control_out_path = work / "control_out.txt"
    out_fd = os.open(str(control_out_path),
                     os.O_WRONLY | os.O_CREAT | os.O_TRUNC | os.O_BINARY)
    out_h = msvcrt.get_osfhandle(out_fd)
    k32.SetHandleInformation(out_h, HANDLE_FLAG_INHERIT, HANDLE_FLAG_INHERIT)
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
    si.dwFlags = STARTF_USESTDHANDLES
    si.hStdOutput = wintypes.HANDLE(out_h)
    si.hStdError = wintypes.HANDLE(out_h)
    cmdline = f'"{SANDBOX_PY}" -X utf8 "{control_child}"'
    cmd_buf = ctypes.create_unicode_buffer(cmdline)  # CreateProcessW 会改写,须可变
    spawned = bool(k32.CreateProcessW(None, cmd_buf,
                                      None, None, True, CREATE_UNICODE_ENVIRONMENT,
                                      ctypes.cast(env_block, wintypes.LPVOID),
                                      str(work), ctypes.byref(si), ctypes.byref(pi)))
    control_rc = None
    control_waited = False
    control_rc_read = False
    if spawned:
        control_waited = (k32.WaitForSingleObject(pi.hProcess, 30000)
                          == WAIT_OBJECT_0)
        code = wintypes.DWORD()
        control_rc_read = bool(k32.GetExitCodeProcess(pi.hProcess,
                                                      ctypes.byref(code)))
        control_rc = code.value if control_rc_read else None
        k32.CloseHandle(pi.hProcess)
        k32.CloseHandle(pi.hThread)
    else:
        control_lasterr = k32.get_last_error()
    os.close(out_fd)
    control_out = control_out_path.read_text(encoding="utf-8", errors="replace") \
        if control_out_path.exists() else ""
    m_ctl = re.search(r"SENTINEL_READ:(.*)", control_out)
    control_read = m_ctl.group(1) if m_ctl else None
    # 沙箱侧(修复后 HANDLE_LIST):同句柄必须确认类错误 + 真实令牌
    r = _sandbox(_token_probe() + _READ_CODE, work,
                 extra={"PROBE_HANDLE": str(h)})
    os.close(fd)
    sandbox_out = ((r.stdout or b"") + (r.stderr or b"")).decode(
        "utf-8", "replace")
    m_err = re.search(r"READ_ERROR winerror=(\d+)", sandbox_out)
    sandbox_winerror = int(m_err.group(1)) if m_err else None
    token_ok = bool(_TOKEN_RE.search(sandbox_out))
    verdict = _judge_a1(control_spawned=spawned, control_waited=control_waited,
                        control_rc_read=control_rc_read, control_rc=control_rc,
                        control_read=control_read, sandbox_rc=r.returncode,
                        sandbox_winerror=sandbox_winerror,
                        token_ok=token_ok, sandbox_out=sandbox_out)
    return {**verdict,
            "control": {"spawned": spawned, "waited": control_waited,
                        "rc_read": control_rc_read, "rc": control_rc,
                        "lasterr": control_lasterr if not spawned else None,
                        "out": control_out},
            "sandbox": {"rc": r.returncode, "winerror": sandbox_winerror,
                        "token_ok": token_ok, "out": sandbox_out[-400:]}}


# ------------------------------------------------------------------ A2 场景

_GRAND_CODE = (
    "import os,time\n"
    "with open(os.path.join(os.environ['GRAND_DIR'],'alive-'+os.environ['GRAND_TOKEN']),'w') as f:\n"
    "    f.write(str(os.getpid()))\n"
    "time.sleep(120)\n"
)
_CHILD_SPAWN_TIMEOUT = _token_probe() + (
    "import os,subprocess,sys,time\n"
    "p=subprocess.Popen([sys.executable,'-X','utf8','-c',"
    "os.environ['GRAND_CODE']],env=dict(os.environ))\n"
    "print('GRAND_PID='+str(p.pid),flush=True)\n"
    "time.sleep(60)\n"
)
# 正常退出场景:根进程等监督端 ACK(监督端核验握手后才写)再退出
_CHILD_SPAWN_EXIT = _token_probe() + (
    "import os,subprocess,sys,time\n"
    "p=subprocess.Popen([sys.executable,'-X','utf8','-c',"
    "os.environ['GRAND_CODE']],env=dict(os.environ))\n"
    "print('GRAND_PID='+str(p.pid),flush=True)\n"
    "ack=os.path.join(os.environ['GRAND_DIR'],'ack-'+os.environ['GRAND_TOKEN'])\n"
    "deadline=time.time()+30\n"
    "while time.time()<deadline and not os.path.exists(ack):\n"
    "    time.sleep(0.05)\n"
    "print('ACK_SEEN='+str(os.path.exists(ack)),flush=True)\n"
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


def _image_path(h: wintypes.HANDLE) -> str | None:
    buf = ctypes.create_unicode_buffer(1024)
    n = wintypes.DWORD(1024)
    if k32.QueryFullProcessImageNameW(h, 0, buf, ctypes.byref(n)):
        return buf.value
    return None


_HANDSHAKE_ACCESS = (SYNCHRONIZE | PROCESS_QUERY_LIMITED_INFORMATION
                     | PROCESS_TERMINATE)


def _handshake(marker: Path, work: Path, token: str, need_ack: bool) -> dict:
    """握手:打开进程句柄(含 PROCESS_TERMINATE,cleanup 只用此句柄,
    不按 PID 重开);存活判定只认 WAIT_TIMEOUT,WAIT_FAILED 记录错误并失败;
    并核验映像路径=SANDBOX_PY。核验通过(且需要时)写监督端 ACK。"""
    deadline = time.time() + 30
    while time.time() < deadline:
        if marker.exists():
            try:
                pid = int(marker.read_text().strip())
            except ValueError:
                pid = 0
            if pid:
                h = k32.OpenProcess(_HANDSHAKE_ACCESS, False, pid)
                if h:
                    w = k32.WaitForSingleObject(h, 0)
                    if _is_alive_wait(w):  # 仅 WAIT_TIMEOUT=打开时存活
                        img = _image_path(h)
                        if img and img.lower() == str(SANDBOX_PY.resolve()).lower():
                            if need_ack:
                                (work / f"ack-{token}").write_text("1")
                            return {"held": h, "pid": pid, "image": img,
                                    "verified": True, "wait_error": None}
                        k32.CloseHandle(h)
                        return {"held": None, "pid": pid, "image": img,
                                "verified": False, "wait_error": None}  # 映像不符
                    if w == WAIT_FAILED:
                        err = k32.get_last_error()
                        k32.CloseHandle(h)
                        return {"held": None, "pid": pid, "image": None,
                                "verified": False, "wait_error": err}
                    k32.CloseHandle(h)  # WAIT_OBJECT_0:打开瞬间已死,重试
        time.sleep(0.05)
    return {"held": None, "pid": 0, "image": None, "verified": False,
            "wait_error": None}


def _cleanup(held: wintypes.HANDLE | None) -> dict:
    """兜底清理(绝不进判定):只用握手时已持有并核验身份的句柄
    Terminate/Wait,不按 PID 重开;失败错误如实保存。"""
    out = {"terminate_attempted": False, "terminate_ok": None,
           "terminate_lasterr": None, "wait_lasterr": None,
           "alive_before_cleanup": None}
    if held is None:
        return out
    w0 = k32.WaitForSingleObject(held, 0)
    if w0 == WAIT_TIMEOUT:
        out["alive_before_cleanup"] = True
    elif w0 == WAIT_OBJECT_0:
        out["alive_before_cleanup"] = False
        return out
    else:  # WAIT_FAILED:错误,记录并停止
        out["wait_lasterr"] = k32.get_last_error()
        return out
    k32.WaitForSingleObject(held, 5000)
    if k32.WaitForSingleObject(held, 0) == WAIT_OBJECT_0:
        return out
    out["terminate_attempted"] = True
    out["terminate_ok"] = bool(k32.TerminateProcess(held, 1))
    if not out["terminate_ok"]:
        out["terminate_lasterr"] = k32.get_last_error()
    return out


def _run_scenario(code: str, work: Path, timeout_ms: int, token: str,
                  need_ack: bool) -> dict:
    marker = work / f"alive-{token}"
    extra = {"GRAND_TOKEN": token, "GRAND_DIR": str(work),
             "GRAND_CODE": _GRAND_CODE}
    th, box = _run_async((code, work, timeout_ms, extra))
    hs = _handshake(marker, work, token, need_ack)
    held, pid, img, verified = hs["held"], hs["pid"], hs["image"], hs["verified"]
    th.join(60)
    thread_finished = not th.is_alive()
    out = ""
    timed_out: bool | None = None
    rc: int | None = None
    if "timeout" in box:
        timed_out = True
        out = (box["timeout"].output or b"").decode("utf-8", "replace")
    elif "result" in box:
        timed_out = False
        rc = box["result"].returncode
        out = ((box["result"].stdout or b"") + (box["result"].stderr or b"")).decode(
            "utf-8", "replace")
    else:
        out = "ERROR:" + box.get("error", "unknown")
    # 返回瞬间观测:只赋值一次;兜底清理只记录,绝不改写(防假通过)
    signaled_at_return = (held is not None
                          and k32.WaitForSingleObject(held, 0) == WAIT_OBJECT_0)
    cleanup = _cleanup(held)
    if held:
        k32.CloseHandle(held)
    return {"timed_out": timed_out, "rc": rc,
            "signaled_at_return": signaled_at_return,
            "handshake": {"verified": verified, "pid": pid, "image": img,
                          "wait_error": hs["wait_error"]},
            "token_ok": bool(_TOKEN_RE.search(out)),
            "thread_finished": thread_finished,
            "ack_received": "ACK_SEEN=True" in out,
            "cleanup": cleanup, "out": out[-600:]}


def a2(work: Path) -> dict:
    sc1 = _run_scenario(_CHILD_SPAWN_TIMEOUT, work, 5000,
                        uuid.uuid4().hex, need_ack=False)
    sc2 = _run_scenario(_CHILD_SPAWN_EXIT, work, 60_000,
                        uuid.uuid4().hex, need_ack=True)
    verdict = _judge_a2(sc1, sc2)
    return {"timeout": sc1, "normal_exit": sc2, **verdict}


def main() -> int:
    work = SUPPORT / f"replay3-{uuid.uuid4().hex[:8]}"
    _check_paths(work)
    hashes = {
        "replay_script_sha256": hashlib.sha256(
            Path(__file__).read_bytes()).hexdigest(),
        "appcontainer_sha256": hashlib.sha256(
            (ROOT / "src/animtrain/appcontainer.py").read_bytes()).hexdigest(),
        "win_job_sha256": hashlib.sha256(
            (ROOT / "src/animtrain/win_job.py").read_bytes()).hexdigest(),
    }
    results = {"source_hashes": hashes,
               "command": [sys.executable] + sys.argv,
               "work": str(work)}
    results["negative_regressions"] = _negative_regressions()
    results["A1_inherited_handle"] = a1(work)
    results["A2_tree_termination"] = a2(work)
    out = SUPPORT / "replay-v3-results.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False, indent=2))
    ok = (results["negative_regressions"]["all_hold"]
          and results["A1_inherited_handle"]["blocked"]
          and results["A2_tree_termination"]["passed"])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
