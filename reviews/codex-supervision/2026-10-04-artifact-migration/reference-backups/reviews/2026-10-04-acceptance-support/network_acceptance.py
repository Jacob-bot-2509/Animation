r"""网络验收 v2:本机 TCP/UDP/IPv6 真实随机 nonce 收包正反对照(应 msg_306/308)。

v1 静态复核未通过(msg_308,复查方 10 场景仅 3/10 达标),v2 修复:
  1. 能力读取改用 TokenCapabilities=30(TOKEN_GROUPS.GroupCount),
     记录 Open/Get API 成功与返回大小;API/转换失败不得填 0;
  2. _judge_attempt 要求沙箱 spawned=True/rc==0/服务端已证明正常监听
     (bind+listen 成功、无 bind_error)/接收观察已完结且无 server_error;
     服务端 socket 创建/bind/listen/accept/recv 异常完整捕获,
     finally 关闭 socket/conn(修复 bind 失败漏关 socket);
  3. 严格 PASS 仅 = 明确拒绝(winerror=10013)+服务端正常监听+有效令牌;
     sent_ok 无收包一律 UNVERIFIED(保留为观测),不归因 OS 隔离;
     沙箱 nonce 送达 = FAIL(最高优先级,控制端异常也不掩盖击穿);
  4. 服务端 received 以 hex+长度+latin-1 显式编码存储,原始字节可回放,
     JSON roundtrip 自检 + 写入前断言无 bytes(绝不 default=str);
  5. no-shim 证据:记录并核对副本 ._pth 隔离配置、sys.executable/
     socket.__file__/SITE_ABSENT(无 import site 注入)/关键运行时与
     客户端哈希;不需授权原工具链;
  6. 完整记录逐次命令、nonce、单调时间监听/收发/结束界限;
     负例对齐复查方 10 场景(N1-N10+P8 干净基线判 PASS)。

范围与安全约束(不变):仅本支持目录(net-evidence/、net-runtime/ 独立副本、
net-work-<rand>/);ACL 只落本支持目录副本与工作目录;复用既有生产
AppContainer profile;仅回环地址、合成 nonce、可定位进程;不改核心四文件/
门禁/防火墙/loopback 豁免/C 盘系统文件;不宣称完整网络隔离。

v2.1(应内部对抗复核 12 项确认发现):
  - 判定补 delivered=None → UNVERIFIED(送达状态必须明确 False 才可能 PASS);
  - 客户端自哈希:子进程对自身脚本文件与 sys.executable 计算 SHA256 上报,
    监督端与记录值比对,client_file_ok 不再是恒真死门;
  - ._pth 隔离配置真正核验(只允许 Lib/DLLs/. 相对条目、无 import site),
    socket.__file__ 与运行时副本路径比对,均入判定(pth_ok/socket_ok);
  - 服务端接收窗口改为客户端启动后才开始计时,窗口=客户端最长尝试
    (15s)+socket 超时 3s+余量,超时前全覆盖;TCP accept 后 conn 全路径
    finally 关闭(修 conn 泄漏);
  - 控制端 subprocess 补 OSError 捕获;TimeoutExpired 同时保留 stderr
    (沙箱/控制);main 整体异常兜底写错误证据 JSON,不再裸崩溃;
  - 重跑时 net-runtime 副本与授权源比对 python.exe 哈希+._pth 内容,
    不一致即刷新副本并记录两侧哈希。
v2.2(应 msg_312,授权受限原生执行前的收尾):
  - 运行时副本核验扩为关键文件哈希清单:python.exe/python313.dll/
    Lib/socket.py/DLLs/_socket.pyd + ._pth 内容,源与副本逐项比对,
    任何不一致即刷新副本并记录完整清单;
  - 沙箱 env 补普通 Windows 变量(SystemDrive/windir/USERNAME/USERDOMAIN)
    防 203 错误;TEMP/TMP/profile/PATH 仍绑定副本,不授权源工具链;
  - 每次运行证据写入带 run_id 后缀的新文件,绝不覆盖旧证据。
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import threading
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from animtrain import appcontainer as ac  # noqa: E402

SUPPORT = Path(__file__).resolve().parent
# 复查方授权可复用的独立运行时(msg_306);只读复制,不授权原 D:\Python/.venv
CODEX_RUNTIME = Path(
    r"D:\code\output\claude-supervision\fix-2026-10-04"
    r"\appcontainer-probe-wenbjyjh\runtime")
NET_RUNTIME = SUPPORT / "net-runtime"
EVIDENCE = SUPPORT / "net-evidence"

# 服务端接收窗口(自客户端启动事件起算):须覆盖客户端最长尝试窗口
# (run_appcontainer/subprocess 15s)+ 客户端 socket 超时 3s + 余量 2s
SERVER_WAIT_S = 20.0
WSAEACCES = 10013            # AppContainer 无网络能力时的预期拒绝
WSAECONNREFUSED = 10061      # 拒连 = rig 问题,不是阻断证据
TOKEN_IS_APPCONTAINER = 29
TOKEN_CAPABILITIES = 30


def _check_paths(work: Path) -> None:
    assert work.is_absolute(), "工作目录必须绝对路径"
    assert str(work).startswith(str(SUPPORT.resolve())), \
        f"工作目录必须在支持目录内: {work}"
    work.mkdir(parents=True, exist_ok=True)


def _normpath(p: str) -> str:
    return os.path.normcase(os.path.abspath(p))


def _assert_json_safe(obj, where: str) -> None:
    """写入前断言无 bytes(防 v1 的 json.dumps TypeError 复发)。"""
    if isinstance(obj, bytes):
        raise TypeError(f"{where}: 发现未转换的 bytes 字段")
    if isinstance(obj, dict):
        for k, v in obj.items():
            _assert_json_safe(v, f"{where}.{k}")
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            _assert_json_safe(v, f"{where}[{i}]")


def _recv_evidence(data: bytes | None) -> dict:
    """服务端收到的字节 → JSON 安全证据(hex+长度+latin-1,可回放)。"""
    if data is None:
        return {"received_hex": None, "received_len": 0,
                "received_latin1": None}
    return {"received_hex": data.hex(), "received_len": len(data),
            "received_latin1": data.decode("latin-1", "replace")}


def _pth_ok(content: str | None) -> bool:
    """核验运行时副本 ._pth 隔离配置:非空、只允许 Lib/DLLs/. 相对条目、
    无 import site 注入。"""
    if not content:
        return False
    lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
    if not lines:
        return False
    for ln in lines:
        if "import site" in ln:
            return False
        if ln not in ("Lib", "DLLs", "."):
            return False
    return True


# ---------------------------------------------------------------- 纯判定谓词

def _judge_attempt(control: dict, sandbox: dict) -> dict:
    """单次正反对照严格判定(纯谓词,只吃观测值,无副作用)。
    返回 {"verdict": PASS|FAIL|UNVERIFIED, "reasons": [...]}。

    规则(应 msg_308):
      - 沙箱 nonce 送达服务端 → FAIL,最高优先级(控制端异常不掩盖击穿);
      - 沙箱必须 spawned=True、rc==0、未超时、服务端已证明正常监听
        (listening=True 且无 bind_error)、接收观察已完结(finalized=True
        且无 server_error)、TokenIsAppContainer=29 证据齐全、能力计数==0
        (TokenCapabilities=30,API 成功,失败不得填 0)、无 Python shim
        (无 sitecustomize/site 注入+executable 匹配+运行时/客户端哈希核验);
      - 明确阻断证据仅 = outcome==net_error 且 winerror==10013;
        sent_ok 无收包一律 UNVERIFIED(不归因 OS 隔离);
      - 控制端必须实际收到精确 nonce;否则 UNVERIFIED(在 FAIL 判定之后)。
    """
    reasons: list[str] = []
    # FAIL 优先:沙箱 nonce 确实到达 = 击穿
    if sandbox["delivered"] is True:
        return {"verdict": "FAIL", "reasons": ["沙箱 nonce 送达服务端(隔离击穿)"]}
    if sandbox["delivered"] is not False:
        reasons.append("沙箱送达状态未知(必须明确未送达)")
    if sandbox["spawned"] is not True:
        reasons.append("沙箱未启动")
    if sandbox["rc"] != 0:
        reasons.append(f"沙箱 rc={sandbox['rc']}")
    if sandbox["timed_out"] is True:
        reasons.append("run_appcontainer 超时")
    if sandbox["server_ok"] is not True:
        reasons.append("沙箱侧服务端未证明正常监听(就绪/监听/无绑定错误)")
    if sandbox["recv_final"] is not True:
        reasons.append("沙箱侧接收观察未完结或接收线程存在错误/未知状态")
    if sandbox["token29"] is not True:
        reasons.append("TokenIsAppContainer=29 证据缺失或 API 失败")
    if sandbox["cap_count"] != 0:
        reasons.append("能力 SID 计数非 0(TokenCapabilities=30)")
    if sandbox["cap_api_ok"] is not True:
        reasons.append("TokenCapabilities API 失败(计数不可信)")
    if sandbox["shim_absent"] is not True:
        reasons.append("存在 Python shim/site 注入或可执行路径不符")
    if sandbox["pth_ok"] is not True:
        reasons.append("._pth 隔离配置核验失败")
    if sandbox["socket_ok"] is not True:
        reasons.append("socket.__file__ 与运行时副本不符")
    if sandbox["client_file_ok"] is not True:
        reasons.append("客户端自哈希与记录值不符/缺失")
    outcome = sandbox["outcome"]
    werr = sandbox["err_winerror"]
    if outcome == "net_error" and werr == WSAEACCES:
        pass  # 明确拒绝(10013)= 唯一可 PASS 的阻断证据
    else:
        reasons.append(f"非明确拒绝(outcome={outcome}, winerror={werr});"
                       f"无收包不归因 OS 隔离")
    if reasons:
        return {"verdict": "UNVERIFIED", "reasons": reasons}
    # 控制端(最后,不影响 FAIL 判定)
    if (not control["spawned"] or control["rc"] != 0 or control["timed_out"]
            or control["delivered"] is not True
            or control["nonce_match"] is not True):
        return {"verdict": "UNVERIFIED",
                "reasons": ["控制端异常(未启动/rc!=0/超时/未送达/nonce 不匹配)"]}
    return {"verdict": "PASS", "reasons": []}


def _negative_regressions() -> dict:
    """负例对齐复查方 10 场景(msg_308)+ 补充;P8 为干净基线正例(判 PASS)。"""
    base_control = {"spawned": True, "rc": 0, "timed_out": False,
                    "delivered": True, "nonce_match": True}
    base_sandbox = {"spawned": True, "rc": 0, "timed_out": False,
                    "delivered": False, "server_ok": True, "recv_final": True,
                    "token29": True, "cap_count": 0, "cap_api_ok": True,
                    "shim_absent": True, "pth_ok": True, "socket_ok": True,
                    "client_file_ok": True,
                    "outcome": "net_error", "err_winerror": WSAEACCES}
    cases = []

    def _rec(name: str, verdict: str, expect: str) -> None:
        cases.append({"name": name, "verdict": verdict,
                      "expect": expect, "holds": verdict == expect})

    def _sb(**kw):
        return dict(base_sandbox, **kw)

    def _ct(**kw):
        return dict(base_control, **kw)

    _rec("N1 沙箱 rc!=0", _judge_attempt(base_control, _sb(rc=1))["verdict"],
         "UNVERIFIED")
    _rec("N2 沙箱未启动", _judge_attempt(base_control, _sb(spawned=False))["verdict"],
         "UNVERIFIED")
    _rec("N3 接收观察未完结", _judge_attempt(base_control,
                                            _sb(recv_final=False))["verdict"],
         "UNVERIFIED")
    _rec("N4 接收线程错误", _judge_attempt(base_control,
                                          _sb(server_ok=False))["verdict"],
         "UNVERIFIED")
    _rec("N5 TCP 发送成功但无收包", _judge_attempt(
        base_control, _sb(outcome="sent_ok", err_winerror=None))["verdict"],
        "UNVERIFIED")
    _rec("N6 UDP 已发送无明确阻断", _judge_attempt(
        base_control, _sb(outcome="sent_ok", err_winerror=None))["verdict"],
        "UNVERIFIED")
    _rec("N7 控制异常但沙箱送达(必须 FAIL)", _judge_attempt(
        _ct(delivered=None), _sb(delivered=True))["verdict"], "FAIL")
    _rec("N8 连接被拒 10061", _judge_attempt(
        base_control, _sb(err_winerror=WSAECONNREFUSED))["verdict"],
        "UNVERIFIED")
    _rec("N9 令牌证据失败", _judge_attempt(base_control,
                                          _sb(token29=False))["verdict"],
         "UNVERIFIED")
    _rec("N10 能力 API 失败", _judge_attempt(base_control, _sb(
        cap_count=None, cap_api_ok=False))["verdict"], "UNVERIFIED")
    _rec("N11 控制未送达", _judge_attempt(
        _ct(delivered=None), base_sandbox)["verdict"], "UNVERIFIED")
    _rec("N12 shim 存在", _judge_attempt(base_control,
                                        _sb(shim_absent=False))["verdict"],
         "UNVERIFIED")
    _rec("N13 客户端哈希核验缺失", _judge_attempt(
        base_control, _sb(client_file_ok=False))["verdict"], "UNVERIFIED")
    _rec("N14 沙箱超时", _judge_attempt(base_control, _sb(
        timed_out=True))["verdict"], "UNVERIFIED")
    _rec("N15 沙箱送达状态未知", _judge_attempt(base_control, _sb(
        delivered=None))["verdict"], "UNVERIFIED")
    _rec("N16 ._pth 核验失败", _judge_attempt(base_control, _sb(
        pth_ok=False))["verdict"], "UNVERIFIED")
    _rec("N17 socket.__file__ 不符", _judge_attempt(base_control, _sb(
        socket_ok=False))["verdict"], "UNVERIFIED")
    _rec("P8 干净阻断基线(10013+全证据)", _judge_attempt(
        base_control, base_sandbox)["verdict"], "PASS")
    return {"cases": cases, "all_hold": all(c["holds"] for c in cases)}


def _json_roundtrip_ok() -> dict:
    """JSON roundtrip 自检:含 hex 证据的样例必须可无损序列化/反序列化。"""
    sample = {"recv": _recv_evidence(b"\x00\xffSYN"),
              "nonce": "abc123", "nested": [{"hex": "00ff", "n": 7}]}
    try:
        back = json.loads(json.dumps(sample))
        ok = back == sample
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": repr(e)}
    return {"ok": ok, "error": None}


# ---------------------------------------------------------------- 客户端代码

_CLIENT = (
    "import ctypes, os, socket, sys, time\n"
    "from ctypes import wintypes\n"
    "k = ctypes.windll.kernel32\n"
    "a = ctypes.windll.advapi32\n"
    "k.GetCurrentProcess.restype = wintypes.HANDLE\n"
    "k.OpenProcessToken.restype = wintypes.BOOL\n"
    "k.OpenProcessToken.argtypes = [wintypes.HANDLE, wintypes.DWORD, "
    "ctypes.POINTER(wintypes.HANDLE)]\n"
    "a.GetTokenInformation.restype = wintypes.BOOL\n"
    "a.GetTokenInformation.argtypes = [wintypes.HANDLE, ctypes.c_int, "
    "wintypes.LPVOID, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]\n"
    "k.LocalFree.argtypes = [wintypes.LPVOID]\n"
    "k.CloseHandle.argtypes = [wintypes.HANDLE]\n"
    "class _SAA(ctypes.Structure):\n"
    "    _fields_ = [('Sid', wintypes.LPVOID), ('Attributes', wintypes.DWORD)]\n"
    "class _TGROUPS(ctypes.Structure):\n"
    "    _fields_ = [('GroupCount', wintypes.DWORD), ('Groups', _SAA * 1)]\n"
    "h = wintypes.HANDLE()\n"
    "ok1 = k.OpenProcessToken(k.GetCurrentProcess(), 0x0008, ctypes.byref(h))\n"
    "val = wintypes.DWORD(); need = wintypes.DWORD()\n"
    "ok2 = a.GetTokenInformation(h, 29, ctypes.byref(val), 4, ctypes.byref(need))\n"
    "is_ac = int(val.value) if ok2 else None\n"
    "# 能力计数:TokenCapabilities=30 返回 TOKEN_GROUPS,GroupCount 即能力数;\n"
    "# API 失败一律 None,绝不填 0\n"
    "cap_count = None\n"
    "cap_api_ok = 0\n"
    "cap_needed = 0\n"
    "if ok2:\n"
    "    need2 = wintypes.DWORD()\n"
    "    a.GetTokenInformation(h, 30, None, 0, ctypes.byref(need2))\n"
    "    cap_needed = need2.value\n"
    "    if cap_needed:\n"
    "        buf = ctypes.create_string_buffer(cap_needed)\n"
    "        if a.GetTokenInformation(h, 30, buf, cap_needed, "
    "ctypes.byref(need2)):\n"
    "            tg = ctypes.cast(buf, ctypes.POINTER(_TGROUPS)).contents\n"
    "            cap_count = tg.GroupCount\n"
    "            cap_api_ok = 1\n"
    "k.CloseHandle(h)\n"
    "transport, host, port, nonce = sys.argv[1], sys.argv[2], "
    "int(sys.argv[3]), sys.argv[4]\n"
    "t0 = time.time()\n"
    "outcome = 'no_record'\n"
    "err_winerror = None\n"
    "s = None\n"
    "try:\n"
    "    fam = socket.AF_INET6 if ':' in host else socket.AF_INET\n"
    "    s = socket.socket(fam, socket.SOCK_STREAM if transport == 'tcp' "
    "else socket.SOCK_DGRAM)\n"
    "except OSError as e:\n"
    "    outcome = 'net_error'\n"
    "    err_winerror = getattr(e, 'winerror', None)\n"
    "    print('SOCKET_ERROR winerror=%s' % err_winerror, flush=True)\n"
    "if s is not None:\n"
    "    try:\n"
    "        s.settimeout(3.0)\n"
    "        if transport == 'tcp':\n"
    "            s.connect((host, port))\n"
    "            s.sendall(nonce.encode('latin-1'))\n"
    "            outcome = 'sent_ok'\n"
    "            print('TCP_SENT_OK', flush=True)\n"
    "        else:\n"
    "            s.sendto(nonce.encode('latin-1'), (host, port))\n"
    "            outcome = 'sent_ok'\n"
    "            print('UDP_SENT_OK', flush=True)\n"
    "    except socket.timeout:\n"
    "        outcome = 'net_timeout'\n"
    "        print('NET_TIMEOUT', flush=True)\n"
    "    except OSError as e:\n"
    "        outcome = 'net_error'\n"
    "        err_winerror = getattr(e, 'winerror', None)\n"
    "        print('NET_ERROR winerror=%s errno=%s' % (err_winerror, "
    "getattr(e, 'errno', None)), flush=True)\n"
    "    finally:\n"
    "        try:\n"
    "            s.close()\n"
    "        except Exception:\n"
    "            pass\n"
    "print('TOKEN_IS_APPCONTAINER=%s ok=%s/%s' % (is_ac, int(ok1), int(ok2)), "
    "flush=True)\n"
    "print('CAPABILITY_COUNT=%s CAP_API_OK=%s CAP_NEEDED=%s' % (cap_count, "
    "cap_api_ok, cap_needed), flush=True)\n"
    "print('SHIM_ABSENT=%s' % ('sitecustomize' not in sys.modules), flush=True)\n"
    "print('SITE_ABSENT=%s' % ('site' not in sys.modules), flush=True)\n"
    "print('SYS_EXECUTABLE=%s' % sys.executable, flush=True)\n"
    "print('SOCKET_FILE=%s' % socket.__file__, flush=True)\n"
    "# 自哈希:对实际执行的脚本文件与解释器计算 SHA256,供监督端比对\n"
    "def _sha(p):\n"
    "    try:\n"
    "        import hashlib\n"
    "        with open(p, 'rb') as f:\n"
    "            return hashlib.sha256(f.read()).hexdigest()\n"
    "    except OSError:\n"
    "        return None\n"
    "print('CLIENT_FILE_SHA256=%s' % _sha(sys.argv[0]), flush=True)\n"
    "print('RUNTIME_EXE_SHA256=%s' % _sha(sys.executable), flush=True)\n"
    "print('OUTCOME=%s ERR_WINERROR=%s T_DELTA=%.3f' % (outcome, "
    "err_winerror, time.time() - t0), flush=True)\n"
)


def _parse_client(out: str) -> dict:
    tok = re.search(r"TOKEN_IS_APPCONTAINER=(\S+) ok=(\d)/(\d)", out)
    cap = re.search(r"CAPABILITY_COUNT=(\S+) CAP_API_OK=(\d) CAP_NEEDED=(\d+)",
                    out)
    shim = re.search(r"SHIM_ABSENT=(\S+)", out)
    site = re.search(r"SITE_ABSENT=(\S+)", out)
    exe = re.search(r"SYS_EXECUTABLE=(.+)$", out, re.MULTILINE)
    sock = re.search(r"SOCKET_FILE=(.+)$", out, re.MULTILINE)
    csha = re.search(r"CLIENT_FILE_SHA256=(\S+)", out)
    esha = re.search(r"RUNTIME_EXE_SHA256=(\S+)", out)
    oc = re.search(r"OUTCOME=(\S+) ERR_WINERROR=(\S+)", out)
    return {
        "token29": bool(tok) and tok.group(1) == "1" and tok.group(2) == "1"
        and tok.group(3) == "1",
        "cap_count": int(cap.group(1)) if cap and cap.group(1).isdigit()
        else None,
        "cap_api_ok": cap.group(2) == "1" if cap else False,
        "cap_needed": int(cap.group(3)) if cap else None,
        "shim_absent": bool(shim) and shim.group(1) == "True",
        "site_absent": bool(site) and site.group(1) == "True",
        "sys_executable": exe.group(1).strip() if exe else None,
        "socket_file": sock.group(1).strip() if sock else None,
        "client_file_sha": csha.group(1) if csha else None,
        "runtime_exe_sha": esha.group(1) if esha else None,
        "outcome": oc.group(1) if oc else None,
        "err_winerror": int(oc.group(2))
        if oc and oc.group(2).lstrip("-").isdigit() else None,
    }


# ---------------------------------------------------------------- 服务端与场景

def _server_tcp(host: str, port_holder: list, result: dict, bound: threading.Event,
                start: threading.Event, wait_s: float) -> None:
    try:
        srv = socket.socket(socket.AF_INET6 if ":" in host else socket.AF_INET,
                            socket.SOCK_STREAM)
    except OSError as e:
        result["bind_error"] = getattr(e, "winerror", None) or e.errno
        bound.set()
        return
    try:
        srv.bind((host, 0))
        port_holder[0] = srv.getsockname()[1]
        srv.listen(1)
        result["listening"] = True
        bound.set()
    except OSError as e:
        result["bind_error"] = getattr(e, "winerror", None) or e.errno
        try:
            srv.close()
        except OSError:
            pass
        bound.set()
        return
    try:
        # 接收窗口自客户端启动事件起算,覆盖客户端最长尝试窗口
        if not start.wait(30):
            result["server_error"] = "start event 未触发"
            return
        srv.settimeout(wait_s)
        conn, peer = srv.accept()
        try:
            conn.settimeout(2.0)
            data = conn.recv(256)
            result["received"] = data
            result["peer"] = repr(peer)
        except socket.timeout:
            result["received"] = None
            result["timeout"] = True
        except OSError as e:
            result["received"] = None
            result["server_error"] = getattr(e, "winerror", None) or e.errno
        finally:
            try:
                conn.close()
            except OSError:
                pass
    except socket.timeout:
        result["received"] = None
        result["timeout"] = True
    except OSError as e:
        result["received"] = None
        result["server_error"] = getattr(e, "winerror", None) or e.errno
    finally:
        result["finalized"] = True
        try:
            srv.close()
        except OSError:
            pass


def _server_udp(host: str, port_holder: list, result: dict, bound: threading.Event,
                start: threading.Event, wait_s: float) -> None:
    try:
        srv = socket.socket(socket.AF_INET6 if ":" in host else socket.AF_INET,
                            socket.SOCK_DGRAM)
    except OSError as e:
        result["bind_error"] = getattr(e, "winerror", None) or e.errno
        bound.set()
        return
    try:
        srv.bind((host, 0))
        port_holder[0] = srv.getsockname()[1]
        result["listening"] = True
        bound.set()
    except OSError as e:
        result["bind_error"] = getattr(e, "winerror", None) or e.errno
        try:
            srv.close()
        except OSError:
            pass
        bound.set()
        return
    try:
        if not start.wait(30):
            result["server_error"] = "start event 未触发"
            return
        srv.settimeout(wait_s)
        data, peer = srv.recvfrom(256)
        result["received"] = data
        result["peer"] = repr(peer)
    except socket.timeout:
        result["received"] = None
        result["timeout"] = True
    except OSError as e:
        result["received"] = None
        result["server_error"] = getattr(e, "winerror", None) or e.errno
    finally:
        result["finalized"] = True
        try:
            srv.close()
        except OSError:
            pass


def _spawn_server(transport: str, host: str, result: dict):
    port_holder: list = [None]
    bound = threading.Event()
    start = threading.Event()
    t0 = time.monotonic()
    fn = _server_tcp if transport == "tcp" else _server_udp
    th = threading.Thread(target=fn, args=(host, port_holder, result, bound,
                                           start, SERVER_WAIT_S), daemon=True)
    th.start()
    bound.wait(5.0)
    return th, port_holder, t0, start


def _server_snapshot(result: dict) -> dict:
    """服务端结果 → JSON 安全快照(received 字节转 hex+长度+latin-1)。"""
    snap = {k: v for k, v in result.items() if k != "received"}
    snap.update(_recv_evidence(result.get("received")))
    return snap


def _attempt(transport: str, host: str, client_file: Path, rt_py: Path,
             work: Path, sandbox_env: dict, cfg: dict,
             nonce_ctrl: str, nonce_sb: str) -> dict:
    rt_expect = _normpath(str(rt_py.resolve()))
    sock_expect = _normpath(str((NET_RUNTIME / "Lib" / "socket.py").resolve()))
    rec = {"transport": transport, "host": host,
           "nonce_control": nonce_ctrl, "nonce_sandbox": nonce_sb}
    # ---- 控制端(普通进程,同一 runtime 解释器/客户端代码) ----
    ctrl_res: dict = {}
    th, port_holder, t0, start = _spawn_server(transport, host, ctrl_res)
    rec["control_server"] = {"port": port_holder[0],
                             "t_bind_mono_s": round(time.monotonic() - t0, 3)}
    if port_holder[0] is None:
        rec["control"] = {"spawned": False, "rc": None, "timed_out": False,
                          "delivered": None, "nonce_match": False,
                          "client_out": "",
                          "server": _server_snapshot(ctrl_res),
                          "bind_unavailable": True}
        rec["verdict"] = {"verdict": "UNVERIFIED",
                          "reasons": ["服务端绑定失败/环境不可用"]}
        return rec
    ctrl_cmd = [str(rt_py), "-X", "utf8", str(client_file), transport, host,
                str(port_holder[0]), nonce_ctrl]
    t_launch = time.monotonic()
    start.set()  # 接收窗口自此刻起算
    try:
        cp = subprocess.run(ctrl_cmd, capture_output=True, timeout=15, cwd=work)
        ctrl_out = (cp.stdout + cp.stderr).decode("utf-8", "replace")
        ctrl = {"spawned": True, "rc": cp.returncode, "timed_out": False,
                "client_out": ctrl_out}
    except subprocess.TimeoutExpired as e:
        ctrl_out = ((e.output or b"") + (getattr(e, "stderr", None) or b"")
                    ).decode("utf-8", "replace")
        ctrl = {"spawned": True, "rc": None, "timed_out": True,
                "client_out": ctrl_out}
    except OSError as e:
        ctrl = {"spawned": False, "rc": None, "timed_out": False,
                "client_out": repr(e), "launch_error": repr(e)}
    t_ret = time.monotonic()
    th.join(timeout=SERVER_WAIT_S + 2)
    t_recv_end = time.monotonic()
    received = ctrl_res.get("received")
    ctrl_delivered = received == nonce_ctrl.encode("latin-1")
    ctrl.update({"delivered": ctrl_delivered, "nonce_match": ctrl_delivered,
                 "server": _server_snapshot(ctrl_res),
                 "command": ctrl_cmd,
                 "t_launch_mono_s": round(t_launch - t0, 3),
                 "t_return_mono_s": round(t_ret - t0, 3),
                 "t_recv_end_mono_s": round(t_recv_end - t0, 3)})
    rec["control"] = ctrl
    # ---- 沙箱端(AppContainer) ----
    sb_res: dict = {}
    th2, port2, t1, start2 = _spawn_server(transport, host, sb_res)
    rec["sandbox_server"] = {"port": port2[0],
                             "t_bind_mono_s": round(time.monotonic() - t1, 3)}
    if port2[0] is None:
        rec["sandbox"] = {"spawned": False, "rc": None, "timed_out": False,
                          "delivered": None, "server_ok": False,
                          "recv_final": False, "token29": None,
                          "cap_count": None, "cap_api_ok": False,
                          "shim_absent": False, "pth_ok": False,
                          "socket_ok": False, "client_file_ok": False,
                          "outcome": None, "err_winerror": None,
                          "client_out": "",
                          "server": _server_snapshot(sb_res),
                          "bind_unavailable": True}
        rec["verdict"] = {"verdict": "UNVERIFIED",
                          "reasons": ["服务端绑定失败/环境不可用"]}
        return rec
    sb_cmd = [str(rt_py), "-X", "utf8", str(client_file), transport, host,
              str(port2[0]), nonce_sb]
    t_launch2 = time.monotonic()
    start2.set()  # 接收窗口自此刻起算
    try:
        r = ac.run_appcontainer(sb_cmd, cwd=work, env=sandbox_env,
                                allowed_dirs=[],  # ACL 已一次性显式授予
                                timeout_ms=15_000)
        sb_out = ((r.stdout or b"") + (r.stderr or b"")).decode("utf-8",
                                                                "replace")
        sb = {"spawned": True, "rc": r.returncode, "timed_out": False,
              "client_out": sb_out}
    except subprocess.TimeoutExpired as e:
        sb_out = ((e.output or b"") + (getattr(e, "stderr", None) or b"")
                  ).decode("utf-8", "replace")
        sb = {"spawned": True, "rc": None, "timed_out": True,
              "client_out": sb_out}
    except OSError as e:
        sb = {"spawned": False, "rc": None, "timed_out": False,
              "client_out": repr(e)}
    t_ret2 = time.monotonic()
    th2.join(timeout=SERVER_WAIT_S + 2)
    t_recv_end2 = time.monotonic()
    received2 = sb_res.get("received")
    parsed = _parse_client(sb.get("client_out", ""))
    server_snap = _server_snapshot(sb_res)
    sb.update({
        "delivered": received2 == nonce_sb.encode("latin-1"),
        "server_ok": (sb_res.get("listening") is True
                      and sb_res.get("bind_error") is None),
        "recv_final": (sb_res.get("finalized") is True
                       and sb_res.get("server_error") is None),
        "token29": parsed["token29"], "cap_count": parsed["cap_count"],
        "cap_api_ok": parsed["cap_api_ok"],
        "shim_absent": (parsed["shim_absent"] and parsed["site_absent"]
                        and parsed["sys_executable"] is not None
                        and _normpath(parsed["sys_executable"]) == rt_expect),
        "pth_ok": bool(cfg.get("pth_ok")),
        "socket_ok": (parsed["socket_file"] is not None
                      and _normpath(parsed["socket_file"]) == sock_expect),
        # 客户端自哈希必须与监督端记录值一致(防死门)
        "client_file_ok": (parsed["client_file_sha"] is not None
                           and parsed["client_file_sha"]
                           == cfg.get("client_file_sha256")
                           and parsed["runtime_exe_sha"] is not None
                           and parsed["runtime_exe_sha"]
                           == cfg.get("runtime_python_sha256")),
        "site_absent": parsed["site_absent"],
        "sys_executable": parsed["sys_executable"],
        "socket_file": parsed["socket_file"],
        "client_file_sha": parsed["client_file_sha"],
        "runtime_exe_sha": parsed["runtime_exe_sha"],
        "outcome": parsed["outcome"],
        "err_winerror": parsed["err_winerror"],
        "server": server_snap,
        "command": sb_cmd,
        "t_launch_mono_s": round(t_launch2 - t1, 3),
        "t_return_mono_s": round(t_ret2 - t1, 3),
        "t_recv_end_mono_s": round(t_recv_end2 - t1, 3)})
    rec["sandbox"] = sb
    rec["verdict"] = _judge_attempt(rec["control"], rec["sandbox"])
    return rec


def main() -> int:
    run_id = uuid.uuid4().hex[:12]
    work = SUPPORT / f"net-work-{run_id}"
    _check_paths(work)
    EVIDENCE.mkdir(exist_ok=True)
    results: dict = {}
    try:
        # runtime 独立副本(只读复制复查方授权运行时;不授权原 D:\Python/.venv);
        # 核验=关键文件哈希清单,源与副本逐项比对,任何不一致即刷新副本
        RUNTIME_KEY_FILES = ["python.exe", "python313.dll", "Lib/socket.py",
                             "DLLs/_socket.pyd"]
        src_manifest = {}
        for rel in RUNTIME_KEY_FILES:
            f = CODEX_RUNTIME / rel
            if not f.exists():
                raise FileNotFoundError(f"授权运行时源缺失文件: {f}")
            src_manifest[rel] = hashlib.sha256(f.read_bytes()).hexdigest()
        src_pth_file = CODEX_RUNTIME / "python313._pth"
        if not src_pth_file.exists():
            raise FileNotFoundError(f"授权运行时源缺失: {src_pth_file}")
        src_pth = src_pth_file.read_text(encoding="utf-8", errors="replace")
        need_copy = False
        dst_manifest = {}
        for rel in RUNTIME_KEY_FILES:
            f = NET_RUNTIME / rel
            if not f.exists():
                need_copy = True
                break
            dst_manifest[rel] = hashlib.sha256(f.read_bytes()).hexdigest()
            if dst_manifest[rel] != src_manifest[rel]:
                need_copy = True
                break
        dst_pth_file = NET_RUNTIME / "python313._pth"
        if not need_copy and dst_pth_file.exists():
            dst_pth = dst_pth_file.read_text(encoding="utf-8",
                                             errors="replace")
            if dst_pth != src_pth:
                need_copy = True
        elif not dst_pth_file.exists():
            need_copy = True
        if need_copy:
            shutil.copytree(CODEX_RUNTIME, NET_RUNTIME, dirs_exist_ok=True)
            dst_manifest = {rel: hashlib.sha256(
                (NET_RUNTIME / rel).read_bytes()).hexdigest()
                for rel in RUNTIME_KEY_FILES}
        rt_py = NET_RUNTIME / "python.exe"
        runtime_pth = (NET_RUNTIME / "python313._pth").read_text(
            encoding="utf-8", errors="replace")
        runtime_pth_ok = _pth_ok(runtime_pth)
        # 刷新后逐项复核,确保前后一致(不放过旧副本模块改动)
        for rel in RUNTIME_KEY_FILES:
            if hashlib.sha256((NET_RUNTIME / rel).read_bytes()).hexdigest() \
                    != src_manifest[rel]:
                raise OSError(f"运行时副本核验失败(刷新后仍不一致): {rel}")
        client_file = work / "net_client.py"
        client_file.write_text(_CLIENT, encoding="utf-8")
        hashes = {
            "script_sha256": hashlib.sha256(
                Path(__file__).read_bytes()).hexdigest(),
            "appcontainer_sha256": hashlib.sha256(
                (ROOT / "src/animtrain/appcontainer.py").read_bytes()).hexdigest(),
            "win_job_sha256": hashlib.sha256(
                (ROOT / "src/animtrain/win_job.py").read_bytes()).hexdigest(),
            "runtime_python_sha256": hashlib.sha256(
                rt_py.read_bytes()).hexdigest(),
            "client_file_sha256": hashlib.sha256(
                client_file.read_bytes()).hexdigest(),
        }
        cfg = {"pth_ok": runtime_pth_ok,
               "client_file_sha256": hashes["client_file_sha256"],
               "runtime_python_sha256": hashes["runtime_python_sha256"]}
        profile = ac.appcontainer_profile_path(ac.appcontainer_sid())
        # 一次性显式授予 ACL(均在本支持目录内):net-runtime 只读、work 读写
        sid = ac.appcontainer_sid()
        ac.grant_dir_access(NET_RUNTIME, sid, write=False)
        ac.grant_dir_access(work, sid, write=True)
        sandbox_env = {"SYSTEMROOT": r"C:\Windows",
                       "SystemDrive": os.environ.get("SystemDrive", "C:"),
                       "windir": os.environ.get("windir", r"C:\Windows"),
                       "USERNAME": os.environ.get("USERNAME", ""),
                       "USERDOMAIN": os.environ.get("USERDOMAIN", ""),
                       "PATH": ";".join([str(NET_RUNTIME),
                                         r"C:\Windows\System32"]),
                       "TEMP": str(work), "TMP": str(work),
                       "LOCALAPPDATA": str(profile), "APPDATA": str(profile),
                       "USERPROFILE": str(profile),
                       "PATHEXT": ".COM;.EXE;.BAT;.CMD"}
        results = {"source_hashes": hashes,
                   "runtime_pth": runtime_pth,
                   "runtime_pth_ok": runtime_pth_ok,
                   "runtime_copy": {"src_manifest": dict(src_manifest),
                                    "dst_manifest": dict(dst_manifest),
                                    "src_pth": src_pth,
                                    "refreshed": need_copy},
                   "command": [sys.executable] + sys.argv,
                   "sandbox_env": dict(sandbox_env),
                   "work": str(work), "runtime": str(rt_py),
                   "profile": str(profile),
                   "pre_granted_acl": [[str(NET_RUNTIME), "read"],
                                       [str(work), "read_write"]],
                   "allowed_dirs": [],
                   "server_wait_s": SERVER_WAIT_S,
                   "json_roundtrip": _json_roundtrip_ok()}
        results["negative_regressions"] = _negative_regressions()
        attempts = []
        for transport, host in (("tcp", "127.0.0.1"), ("udp", "127.0.0.1"),
                                ("tcp", "::1"), ("udp", "::1")):
            attempts.append(_attempt(transport, host, client_file, rt_py, work,
                                     sandbox_env, cfg, uuid.uuid4().hex,
                                     uuid.uuid4().hex))
        results["attempts"] = attempts
        verdicts = [a.get("verdict", {}).get("verdict") for a in attempts]
        if "FAIL" in verdicts:
            overall = "FAIL"
        elif "UNVERIFIED" in verdicts or None in verdicts:
            overall = "UNVERIFIED"
        else:
            overall = "PASS"
        results["overall"] = {"verdict": overall, "per_attempt": verdicts,
                              "scope_note": "仅本机回环 TCP/UDP/IPv6 网络隔离;"
                                            "不构成完整网络隔离结论,"
                                            "外网 TCP 待补证",
                              "run_id": run_id}
        _assert_json_safe(results, "results")
        ok = (results["negative_regressions"]["all_hold"]
              and results["json_roundtrip"]["ok"] and overall == "PASS")
    except Exception as e:  # noqa: BLE001 兜底:任何异常都落错误证据,不裸崩溃
        import traceback
        err_rec = {"error": repr(e), "traceback": traceback.format_exc(),
                   "command": [sys.executable] + sys.argv,
                   "partial_results_keys": list(results.keys()),
                   "run_id": run_id}
        (EVIDENCE / f"network-accept-error-{run_id}.json").write_text(
            json.dumps(err_rec, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(err_rec, ensure_ascii=False, indent=2))
        return 1
    # 每次运行独立证据文件,绝不覆盖旧证据
    out = EVIDENCE / f"network-accept-results-{run_id}.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
