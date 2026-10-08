r"""网络验收 v1:本机 TCP/UDP/IPv6 真实随机 nonce 收包正反对照(应 msg_306)。

范围与安全约束(复查方 msg_306):
  - 仅本支持目录:本脚本、证据目录 net-evidence/、runtime 独立副本
    net-runtime/(从复查方授权可复用的运行时复制,绝不授权 D:\Python 或
    项目 .venv)、随机工作目录 net-work-<rand>/;
  - 新增 ACL 只落在 net-runtime/(读)与 net-work-<rand>/(读写),全部在
    本支持目录内,不触碰原工具链任何目录;
  - 复用既有生产 AppContainer profile(不新建临时 profile);
  - 仅回环地址 127.0.0.1 / ::1、合成随机 nonce、可定位进程;
  - 不改核心四文件/生产门禁/防火墙/loopback 豁免/C 盘系统文件。

严格判定(纯谓词 _judge_attempt,合成负例 N1-N8 断言):
  - 控制端(普通进程、同一 runtime 解释器、同一客户端代码)必须被服务端
    实际收到精确 nonce;未启动/rc!=0/超时/未送达/nonce 不匹配 → UNVERIFIED;
  - 沙箱端 nonce 送达服务端 → FAIL(隔离击穿);
  - 沙箱端由 AppContainer 运行,必须自带 API 观察:
    TokenIsAppContainer=29(类 29 取值 1 且 OpenProcessToken/GetTokenInformation
    均成功);令牌 Groups 中 S-1-15-3-* 能力 SID 计数=0;无 Python shim
    (运行时副本无 sitecustomize 且 sys.modules 不含 'sitecustomize');
    观察缺失/不符 → UNVERIFIED;
  - 沙箱 TCP 错误 10061(拒连)或其它无法解释的结果/超时 → UNVERIFIED;
    不按异常文字自动 PASS;明确阻断证据 = 10013(WSAEACCES)或
    UDP 已发送但服务端时间界限内未收到(接收端 recvfrom 实录为准,
    sendto 返回不代表投递);
  - IPv6 服务端无法绑定 ::1 → 该场景 UNVERIFIED(环境不可用)。
结论口径:仅"本机回环 TCP/UDP/IPv6 网络隔离"验收;不宣称完整网络隔离,
外网 TCP 与完整沙箱渲染由后续补证。
"""
from __future__ import annotations

import json
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

SERVER_WAIT_S = 5.0          # 服务端每次接收的时间界限
CLIENT_TIMEOUT_S = 3.0       # 客户端 socket 超时
WSAEACCES = 10013            # AppContainer 无网络能力时的预期拒绝
WSAECONNREFUSED = 10061      # 拒连 = rig 问题,不是阻断证据


def _check_paths(work: Path) -> None:
    assert work.is_absolute(), "工作目录必须绝对路径"
    assert str(work).startswith(str(SUPPORT.resolve())), \
        f"工作目录必须在支持目录内: {work}"
    work.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------- 纯判定谓词

def _judge_attempt(control: dict, sandbox: dict) -> dict:
    """单次正反对照严格判定(纯谓词,只吃观测值,无副作用)。
    返回 {"verdict": PASS|FAIL|UNVERIFIED, "reasons": [...]}。"""
    reasons: list[str] = []
    # 控制端:必须真的收到精确 nonce
    if (not control["spawned"] or control["rc"] != 0
            or control["timed_out"] or control["delivered"] is not True
            or control["nonce_match"] is not True):
        reasons.append("控制端异常(未启动/rc!=0/超时/未送达/nonce 不匹配)")
    if reasons:
        return {"verdict": "UNVERIFIED", "reasons": reasons}
    # 沙箱端:送达即击穿
    if sandbox["delivered"] is True:
        return {"verdict": "FAIL", "reasons": ["沙箱 nonce 送达服务端(隔离击穿)"]}
    if sandbox["token29"] is not True:
        reasons.append("TokenIsAppContainer=29 证据缺失或 API 失败")
    if sandbox["cap_count"] != 0:
        reasons.append("能力 SID 计数非 0")
    if sandbox["shim_absent"] is not True:
        reasons.append("存在 Python shim 或运行时非干净副本")
    outcome = sandbox["outcome"]
    werr = sandbox["err_winerror"]
    if outcome == "net_error" and werr == WSAEACCES:
        pass  # 明确拒绝(10013)= 阻断证据
    elif outcome == "sent_ok":
        pass  # UDP 已发送但未送达:以接收端实录为准的阻断证据
    else:
        reasons.append(f"沙箱结果无法解释(outcome={outcome}, winerror={werr})")
    if sandbox["timed_out"] is True:
        reasons.append("run_appcontainer 超时")
    if reasons:
        return {"verdict": "UNVERIFIED", "reasons": reasons}
    return {"verdict": "PASS", "reasons": []}


def _negative_regressions() -> dict:
    """合成负例 N1-N8(应 msg_306"加控制失败/探针失败等负例"):
    判定谓词绝不放行无效/击穿输入。"""
    base_control = {"spawned": True, "rc": 0, "timed_out": False,
                    "delivered": True, "nonce_match": True}
    base_sandbox = {"spawned": True, "rc": 0, "timed_out": False,
                    "delivered": False, "token29": True, "cap_count": 0,
                    "shim_absent": True, "outcome": "net_error",
                    "err_winerror": WSAEACCES}
    cases = []

    def _rec(name: str, verdict: str, expect_fail: bool = False) -> None:
        ok = (verdict == "FAIL") if expect_fail else (verdict != "PASS")
        cases.append({"name": name, "verdict": verdict, "holds": ok})

    _rec("N1 控制未送达", _judge_attempt(dict(base_control, delivered=None),
                                        base_sandbox)["verdict"])
    _rec("N2 沙箱送达 nonce(必须 FAIL)", _judge_attempt(
        base_control, dict(base_sandbox, delivered=True))["verdict"],
        expect_fail=True)
    _rec("N3 令牌证据缺失", _judge_attempt(
        base_control, dict(base_sandbox, token29=False))["verdict"])
    _rec("N4 沙箱无结果记录", _judge_attempt(
        base_control, dict(base_sandbox, outcome=None))["verdict"])
    _rec("N5 控制 nonce 不匹配", _judge_attempt(
        dict(base_control, nonce_match=False), base_sandbox)["verdict"])
    _rec("N6 沙箱连接被拒 10061", _judge_attempt(
        base_control, dict(base_sandbox, err_winerror=WSAECONNREFUSED))["verdict"])
    _rec("N7 能力计数非 0", _judge_attempt(
        base_control, dict(base_sandbox, cap_count=1))["verdict"])
    _rec("N8 shim 存在", _judge_attempt(
        base_control, dict(base_sandbox, shim_absent=False))["verdict"])
    return {"cases": cases, "all_hold": all(c["holds"] for c in cases)}


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
    "a.ConvertSidToStringSidW.restype = wintypes.BOOL\n"
    "a.ConvertSidToStringSidW.argtypes = [wintypes.LPVOID, "
    "ctypes.POINTER(wintypes.LPWSTR)]\n"
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
    "cap_count = None\n"
    "if ok2:\n"
    "    need = wintypes.DWORD()\n"
    "    a.GetTokenInformation(h, 2, None, 0, ctypes.byref(need))\n"
    "    buf = ctypes.create_string_buffer(need.value)\n"
    "    if a.GetTokenInformation(h, 2, buf, need.value, ctypes.byref(need)):\n"
    "        tg = ctypes.cast(buf, ctypes.POINTER(_TGROUPS)).contents\n"
    "        arr = ctypes.cast(ctypes.addressof(tg.Groups), "
    "ctypes.POINTER(_SAA))\n"
    "        cnt = 0\n"
    "        for i in range(tg.GroupCount):\n"
    "            s = wintypes.LPWSTR()\n"
    "            if a.ConvertSidToStringSidW(arr[i].Sid, ctypes.byref(s)) "
    "and s.value:\n"
    "                if s.value.startswith('S-1-15-3-'):\n"
    "                    cnt += 1\n"
    "                k.LocalFree(s)\n"
    "        cap_count = cnt\n"
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
    "    print('SOCKET_ERROR winerror=%s' % getattr(e, 'winerror', None), "
    "flush=True)\n"
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
    "print('CAPABILITY_COUNT=%s' % cap_count, flush=True)\n"
    "print('SHIM_ABSENT=%s' % ('sitecustomize' not in sys.modules), "
    "flush=True)\n"
    "print('OUTCOME=%s ERR_WINERROR=%s T_DELTA=%.3f' % (outcome, "
    "err_winerror, time.time() - t0), flush=True)\n"
)


def _parse_client(out: str) -> dict:
    tok = re.search(r"TOKEN_IS_APPCONTAINER=(\S+) ok=(\d)/(\d)", out)
    cap = re.search(r"CAPABILITY_COUNT=(\S+)", out)
    shim = re.search(r"SHIM_ABSENT=(\S+)", out)
    oc = re.search(r"OUTCOME=(\S+) ERR_WINERROR=(\S+)", out)
    return {
        "token29": bool(tok) and tok.group(1) == "1" and tok.group(2) == "1"
        and tok.group(3) == "1",
        "cap_count": int(cap.group(1)) if cap and cap.group(1).isdigit()
        else None,
        "shim_absent": bool(shim) and shim.group(1) == "True",
        "outcome": oc.group(1) if oc else None,
        "err_winerror": int(oc.group(2))
        if oc and oc.group(2).lstrip("-").isdigit() else None,
    }


# ---------------------------------------------------------------- 服务端与场景

def _server_tcp(host: str, port_holder: list, result: dict, bound: threading.Event,
                wait_s: float) -> None:
    srv = socket.socket(socket.AF_INET6 if ":" in host else socket.AF_INET,
                        socket.SOCK_STREAM)
    try:
        srv.bind((host, 0))
    except OSError as e:
        result["bind_error"] = getattr(e, "winerror", None) or e.errno
        bound.set()
        return
    port_holder[0] = srv.getsockname()[1]
    srv.listen(1)
    srv.settimeout(wait_s)
    bound.set()
    try:
        conn, peer = srv.accept()
        conn.settimeout(2.0)
        data = conn.recv(256)
        result["received"] = data
        result["peer"] = repr(peer)
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
        try:
            srv.close()
        except OSError:
            pass


def _server_udp(host: str, port_holder: list, result: dict, bound: threading.Event,
                wait_s: float) -> None:
    srv = socket.socket(socket.AF_INET6 if ":" in host else socket.AF_INET,
                        socket.SOCK_DGRAM)
    try:
        srv.bind((host, 0))
    except OSError as e:
        result["bind_error"] = getattr(e, "winerror", None) or e.errno
        bound.set()
        return
    port_holder[0] = srv.getsockname()[1]
    srv.settimeout(wait_s)
    bound.set()
    try:
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
        try:
            srv.close()
        except OSError:
            pass


def _spawn_server(transport: str, host: str, result: dict) -> tuple[threading.Thread, list, threading.Event, float]:
    port_holder: list = [None]
    bound = threading.Event()
    t0 = time.time()
    fn = _server_tcp if transport == "tcp" else _server_udp
    th = threading.Thread(target=fn, args=(host, port_holder, result, bound,
                                           SERVER_WAIT_S), daemon=True)
    th.start()
    bound.wait(5.0)
    return th, port_holder, bound, t0


def _attempt(transport: str, host: str, client_file: Path, rt_py: Path,
             work: Path, sandbox_env: dict, nonce_ctrl: str,
             nonce_sb: str) -> dict:
    rec = {"transport": transport, "host": host,
           "nonce_control": nonce_ctrl, "nonce_sandbox": nonce_sb}
    # ---- 控制端(普通进程,同一 runtime 解释器/客户端代码) ----
    ctrl_res: dict = {}
    th, port_holder, bound, t0 = _spawn_server(transport, host, ctrl_res)
    rec["control_server"] = {"port": port_holder[0],
                             "bind_error": ctrl_res.get("bind_error"),
                             "t_bind_s": round(time.time() - t0, 3)}
    if port_holder[0] is None:
        rec["control"] = {"spawned": False, "rc": None, "timed_out": False,
                          "delivered": None, "nonce_match": False,
                          "client_out": "", "server": dict(ctrl_res),
                          "bind_unavailable": True}
        rec["verdict"] = {"verdict": "UNVERIFIED",
                          "reasons": ["服务端绑定失败/环境不可用"]}
        return rec
    try:
        cp = subprocess.run([str(rt_py), "-X", "utf8", str(client_file),
                             transport, host, str(port_holder[0]), nonce_ctrl],
                            capture_output=True, timeout=15, cwd=work)
        ctrl_out = (cp.stdout + cp.stderr).decode("utf-8", "replace")
        ctrl = {"spawned": True, "rc": cp.returncode, "timed_out": False,
                "client_out": ctrl_out}
    except subprocess.TimeoutExpired as e:
        ctrl_out = (e.output or b"").decode("utf-8", "replace")
        ctrl = {"spawned": True, "rc": None, "timed_out": True,
                "client_out": ctrl_out}
    th.join(timeout=SERVER_WAIT_S + 2)
    received = ctrl_res.get("received")
    ctrl_delivered = received == nonce_ctrl.encode("latin-1")
    ctrl.update({"delivered": ctrl_delivered, "nonce_match": ctrl_delivered,
                 "server": dict(ctrl_res),
                 "t_total_s": round(time.time() - t0, 3)})
    rec["control"] = ctrl
    # ---- 沙箱端(AppContainer) ----
    sb_res: dict = {}
    th2, port2, bound2, t1 = _spawn_server(transport, host, sb_res)
    rec["sandbox_server"] = {"port": port2[0],
                             "bind_error": sb_res.get("bind_error"),
                             "t_bind_s": round(time.time() - t1, 3)}
    if port2[0] is None:
        rec["sandbox"] = {"spawned": False, "rc": None, "timed_out": False,
                          "delivered": None, "token29": None, "cap_count": None,
                          "shim_absent": None, "outcome": None,
                          "err_winerror": None, "client_out": "",
                          "server": dict(sb_res), "bind_unavailable": True}
        rec["verdict"] = {"verdict": "UNVERIFIED",
                          "reasons": ["服务端绑定失败/环境不可用"]}
        return rec
    try:
        r = ac.run_appcontainer(
            [str(rt_py), "-X", "utf8", str(client_file), transport, host,
             str(port2[0]), nonce_sb],
            cwd=work, env=sandbox_env,
            allowed_dirs=[],  # ACL 已在 main 一次性显式授予,避免逐场景重复追加
            timeout_ms=15_000)
        sb_out = ((r.stdout or b"") + (r.stderr or b"")).decode("utf-8",
                                                                "replace")
        sb = {"spawned": True, "rc": r.returncode, "timed_out": False,
              "client_out": sb_out}
    except subprocess.TimeoutExpired as e:
        sb_out = (e.output or b"").decode("utf-8", "replace")
        sb = {"spawned": True, "rc": None, "timed_out": True,
              "client_out": sb_out}
    except OSError as e:
        sb = {"spawned": False, "rc": None, "timed_out": False,
              "client_out": repr(e)}
    th2.join(timeout=SERVER_WAIT_S + 2)
    received2 = sb_res.get("received")
    parsed = _parse_client(sb.get("client_out", ""))
    sb.update({"delivered": received2 == nonce_sb.encode("latin-1"),
               "token29": parsed["token29"], "cap_count": parsed["cap_count"],
               "shim_absent": parsed["shim_absent"],
               "outcome": parsed["outcome"],
               "err_winerror": parsed["err_winerror"],
               "server": dict(sb_res),
               "t_total_s": round(time.time() - t1, 3)})
    rec["sandbox"] = sb
    rec["verdict"] = _judge_attempt(rec["control"], rec["sandbox"])
    return rec


def main() -> int:
    work = SUPPORT / f"net-work-{uuid.uuid4().hex[:8]}"
    _check_paths(work)
    EVIDENCE.mkdir(exist_ok=True)
    # runtime 独立副本(只读复制复查方授权运行时;不授权原 D:\Python/.venv)
    if not (NET_RUNTIME / "python.exe").exists():
        shutil.copytree(CODEX_RUNTIME, NET_RUNTIME)
    rt_py = NET_RUNTIME / "python.exe"
    client_file = work / "net_client.py"
    client_file.write_text(_CLIENT, encoding="utf-8")
    profile = ac.appcontainer_profile_path(ac.appcontainer_sid())
    # 一次性显式授予 ACL(均在本支持目录内):net-runtime 只读、work 读写
    sid = ac.appcontainer_sid()
    ac.grant_dir_access(NET_RUNTIME, sid, write=False)
    ac.grant_dir_access(work, sid, write=True)
    sandbox_env = {"SYSTEMROOT": r"C:\Windows",
                   "PATH": ";".join([str(NET_RUNTIME),
                                     r"C:\Windows\System32"]),
                   "TEMP": str(work), "TMP": str(work),
                   "LOCALAPPDATA": str(profile), "APPDATA": str(profile),
                   "USERPROFILE": str(profile),
                   "PATHEXT": ".COM;.EXE;.BAT;.CMD"}
    results = {
        "source_hashes": {
            "script_sha256": __import__("hashlib").sha256(
                Path(__file__).read_bytes()).hexdigest(),
            "appcontainer_sha256": __import__("hashlib").sha256(
                (ROOT / "src/animtrain/appcontainer.py").read_bytes()).hexdigest(),
            "win_job_sha256": __import__("hashlib").sha256(
                (ROOT / "src/animtrain/win_job.py").read_bytes()).hexdigest(),
            "runtime_python_sha256": __import__("hashlib").sha256(
                rt_py.read_bytes()).hexdigest(),
        },
        "command": [sys.executable] + sys.argv,
        "work": str(work),
        "runtime": str(rt_py),
        "profile": str(profile),
        "pre_granted_acl": [[str(NET_RUNTIME), "read"],
                            [str(work), "read_write"]],
        "allowed_dirs": [],
    }
    results["negative_regressions"] = _negative_regressions()
    attempts = []
    for transport, host in (("tcp", "127.0.0.1"), ("udp", "127.0.0.1"),
                            ("tcp", "::1"), ("udp", "::1")):
        attempts.append(_attempt(transport, host, client_file, rt_py, work,
                                 sandbox_env, uuid.uuid4().hex,
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
                                        "不构成完整网络隔离结论,外网 TCP 待补证"}
    out = EVIDENCE / "network-accept-results.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(json.dumps(results, ensure_ascii=False, indent=2))
    ok = (results["negative_regressions"]["all_hold"] and overall == "PASS")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
