r"""文件读写隔离验收 v1:AppContainer 沙箱对具名工作区的读/写正反对照(应 msg_323)。

契约与范围:
  - 仅本支持目录内具名工作区:file-work-<run_id>/(授予 rw ACE)与
    file-denied-<run_id>/(不授 ACE,由普通进程放置合成哨兵文件);
  - 复用既有生产 AppContainer profile;runtime 复用已核验的 net-runtime 副本
    (不新增授权、不授权原 D:\Python/.venv);
  - 仅合成数据(随机 hex nonce 内容);不改核心四文件/门禁/防火墙/C 盘系统文件;
  - 结论标签 PASS_LOCAL_FILE_ACL 仅覆盖本次测试的具名目录与操作,
    不构成整体文件隔离或生产放行结论。

四对照(每例:普通进程控制端必须真实成功,沙箱端判定如下):
  1. granted_write:沙箱写授予目录必须成功且落盘内容哈希一致(证明授权路径可用);
  2. granted_read:沙箱读授予目录内监督端预置文件必须成功且哈希一致;
  3. denied_write:沙箱写未授予目录必须失败(winerror==5 明确拒绝)、
     目标文件必须不存在;控制端写同目录必须成功(证明目录本身可写);
  4. denied_read:沙箱读未授予目录哨兵文件必须失败(winerror==5)且无内容泄漏;
     控制端读必须成功(证明文件本身可读)。
判定(纯谓词 _judge_case):控制端失败/未成功 → UNVERIFIED;沙箱令牌证据
缺失/不符(类29=1、类31 SID 与预期一致) → UNVERIFIED;授予类哈希不一致或
无记录 → UNVERIFIED;拒绝类 winerror 非 5 或无法解释 → UNVERIFIED;
拒绝类目标文件出现/内容泄漏 → FAIL(最高优先级)。
沙箱侧证据一律记录原始输出;文件系统事实由监督端独立复核
(存在性+哈希),不采信客户端单方声称。
"""
from __future__ import annotations

import ctypes
import hashlib
import json
import os
import re
import subprocess
import sys
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from animtrain import appcontainer as ac  # noqa: E402

SUPPORT = Path(__file__).resolve().parent
NET_RUNTIME = SUPPORT / "net-runtime"
EVIDENCE = SUPPORT / "file-evidence"
ACCESS_DENIED = 5  # 明确拒绝类证据

CONTRACT = "local-file-acl-v1"


def _check_paths(path: Path, name: str) -> None:
    assert path.is_absolute(), f"{name} 必须绝对路径"
    assert str(path).startswith(str(SUPPORT.resolve())), \
        f"{name} 必须在支持目录内: {path}"


def _sha_file(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def _assert_json_safe(obj, where: str) -> None:
    if isinstance(obj, bytes):
        raise TypeError(f"{where}: 发现未转换的 bytes 字段")
    if isinstance(obj, dict):
        for k, v in obj.items():
            _assert_json_safe(v, f"{where}.{k}")
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            _assert_json_safe(v, f"{where}[{i}]")


# ---------------------------------------------------------------- 纯判定谓词

def _judge_case(kind: str, control: dict, sandbox: dict) -> dict:
    """单例判定(纯谓词,只吃观测值)。kind ∈ granted_write/granted_read/
    denied_write/denied_read。FAIL 最高优先级,未知一律 UNVERIFIED。"""
    reasons: list[str] = []
    # 拒绝类:目标出现/内容泄漏 = 击穿,任何情况下 FAIL
    if kind == "denied_write" and sandbox.get("target_created") is True:
        return {"verdict": "FAIL", "reasons": ["沙箱写入未授权目标成功(隔离击穿)"],
                "contract": CONTRACT}
    if kind == "denied_read" and sandbox.get("content_leaked") is True:
        return {"verdict": "FAIL", "reasons": ["沙箱读到未授权哨兵内容(隔离击穿)"],
                "contract": CONTRACT}
    # 控制端:必须真实成功
    if (not control.get("spawned") or control.get("rc") != 0
            or control.get("timed_out") or control.get("succeeded") is not True):
        reasons.append("控制端异常(未启动/rc!=0/超时/未实际成功)")
    # 沙箱完整性
    if sandbox.get("spawned") is not True:
        reasons.append("沙箱未启动")
    if sandbox.get("rc") != 0:
        reasons.append(f"沙箱 rc={sandbox.get('rc')}")
    if sandbox.get("timed_out") is True:
        reasons.append("run_appcontainer 超时")
    if sandbox.get("token29") is not True:
        reasons.append("TokenIsAppContainer=29 证据缺失或 API 失败")
    if sandbox.get("sid_ok") is not True:
        reasons.append("类31 SID 与预期不一致")
    outcome = sandbox.get("outcome")
    werr = sandbox.get("winerror")
    if kind in ("granted_write", "granted_read"):
        if sandbox.get("succeeded") is not True or sandbox.get("hash_ok") is not True:
            reasons.append("授予类操作未成功或哈希不一致")
    else:
        if outcome not in ("denied",):
            reasons.append(f"拒绝类结果无法解释(outcome={outcome}, winerror={werr})")
        if werr != ACCESS_DENIED:
            reasons.append(f"非明确拒绝 winerror={werr}(仅接受 5=ACCESS_DENIED)")
    if reasons:
        return {"verdict": "UNVERIFIED", "reasons": reasons, "contract": CONTRACT}
    return {"verdict": "PASS", "reasons": [], "contract": CONTRACT}


def _negative_regressions() -> dict:
    """合成负例:缺陷存在时相应输入必须 FAIL/UNVERIFIED,不得 PASS。"""
    base_control = {"spawned": True, "rc": 0, "timed_out": False, "succeeded": True}
    base_sandbox = {"spawned": True, "rc": 0, "timed_out": False, "token29": True,
                    "sid_ok": True, "outcome": None, "winerror": None,
                    "succeeded": None, "hash_ok": None,
                    "target_created": None, "content_leaked": None}
    cases = []

    def _rec(name: str, verdict: str, expect: str) -> None:
        cases.append({"name": name, "verdict": verdict, "expect": expect,
                      "holds": verdict == expect})

    def _sb(**kw):
        return dict(base_sandbox, **kw)

    def _ct(**kw):
        return dict(base_control, **kw)

    # 拒绝类击穿
    _rec("N1 denied_write 目标出现", _judge_case(
        "denied_write", base_control, _sb(target_created=True))["verdict"], "FAIL")
    _rec("N2 denied_read 内容泄漏", _judge_case(
        "denied_read", base_control, _sb(content_leaked=True))["verdict"], "FAIL")
    # 控制端异常
    _rec("N3 控制端失败", _judge_case(
        "granted_write", _ct(succeeded=False),
        _sb(succeeded=True, hash_ok=True))["verdict"], "UNVERIFIED")
    # 沙箱令牌/身份
    _rec("N4 令牌证据缺失", _judge_case(
        "granted_write", base_control, _sb(
            succeeded=True, hash_ok=True, token29=False))["verdict"], "UNVERIFIED")
    _rec("N5 SID 不符", _judge_case(
        "granted_write", base_control, _sb(
            succeeded=True, hash_ok=True, sid_ok=False))["verdict"], "UNVERIFIED")
    # 授予类证据缺失
    _rec("N6 授予类哈希不一致", _judge_case(
        "granted_read", base_control, _sb(
            succeeded=True, hash_ok=False))["verdict"], "UNVERIFIED")
    _rec("N7 授予类无记录", _judge_case(
        "granted_write", base_control, _sb())["verdict"], "UNVERIFIED")
    # 拒绝类非明确拒绝/无法解释
    _rec("N8 拒绝类 winerror 非 5", _judge_case(
        "denied_write", base_control, _sb(
            outcome="denied", winerror=3))["verdict"], "UNVERIFIED")
    _rec("N9 拒绝类结果无法解释", _judge_case(
        "denied_read", base_control, _sb(
            outcome="sent", winerror=None))["verdict"], "UNVERIFIED")
    _rec("N10 沙箱未启动", _judge_case(
        "granted_write", base_control, _sb(spawned=False))["verdict"], "UNVERIFIED")
    # 干净基线正例
    _rec("P1 granted_write 基线", _judge_case(
        "granted_write", base_control, _sb(
            succeeded=True, hash_ok=True))["verdict"], "PASS")
    _rec("P2 denied_write 基线", _judge_case(
        "denied_write", base_control, _sb(
            outcome="denied", winerror=ACCESS_DENIED,
            target_created=False))["verdict"], "PASS")
    _rec("P3 denied_read 基线", _judge_case(
        "denied_read", base_control, _sb(
            outcome="denied", winerror=ACCESS_DENIED,
            content_leaked=False))["verdict"], "PASS")
    return {"cases": cases, "all_hold": all(c["holds"] for c in cases)}


# ---------------------------------------------------------------- 客户端代码

_CLIENT = (
    "import ctypes, hashlib, json, os, sys, time\n"
    "from ctypes import wintypes\n"
    "def token_probe():\n"
    "    k = ctypes.WinDLL('kernel32', use_last_error=True)\n"
    "    a = ctypes.WinDLL('advapi32', use_last_error=True)\n"
    "    k.GetCurrentProcess.restype = wintypes.HANDLE\n"
    "    a.OpenProcessToken.argtypes = [wintypes.HANDLE, wintypes.DWORD, "
    "ctypes.POINTER(wintypes.HANDLE)]\n"
    "    a.OpenProcessToken.restype = wintypes.BOOL\n"
    "    a.GetTokenInformation.argtypes = [wintypes.HANDLE, ctypes.c_int, "
    "wintypes.LPVOID, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]\n"
    "    a.GetTokenInformation.restype = wintypes.BOOL\n"
    "    a.ConvertSidToStringSidW.argtypes = [wintypes.LPVOID, "
    "ctypes.POINTER(wintypes.LPWSTR)]\n"
    "    a.ConvertSidToStringSidW.restype = wintypes.BOOL\n"
    "    k.LocalFree.argtypes = [wintypes.LPVOID]\n"
    "    h = wintypes.HANDLE()\n"
    "    try:\n"
    "        ok1 = a.OpenProcessToken(k.GetCurrentProcess(), 8, ctypes.byref(h))\n"
    "        val = wintypes.DWORD(); need = wintypes.DWORD()\n"
    "        ok2 = a.GetTokenInformation(h, 29, ctypes.byref(val), 4, "
    "ctypes.byref(need))\n"
    "        is_ac = int(val.value) if ok2 else None\n"
    "        sid = None\n"
    "        if ok2:\n"
    "            need2 = wintypes.DWORD()\n"
    "            a.GetTokenInformation(h, 31, None, 0, ctypes.byref(need2))\n"
    "            if need2.value:\n"
    "                buf = ctypes.create_string_buffer(need2.value)\n"
    "                if a.GetTokenInformation(h, 31, buf, need2.value, "
    "ctypes.byref(need2)):\n"
    "                    p = ctypes.cast(buf, ctypes.POINTER(wintypes.LPVOID)).contents\n"
    "                    if p.value:\n"
    "                        s = wintypes.LPWSTR()\n"
    "                        if a.ConvertSidToStringSidW(p, ctypes.byref(s)) "
    "and s.value:\n"
    "                            sid = s.value\n"
    "                            k.LocalFree(s)\n"
    "        return {'api_ok': bool(ok1 and ok2), 'is_appcontainer': is_ac, "
    "'sid': sid}\n"
    "    finally:\n"
    "        if h.value:\n"
    "            k.CloseHandle(h)\n"
    "mode, target, content = sys.argv[1], sys.argv[2], sys.argv[3]\n"
    "t0 = time.time()\n"
    "outcome = None\n"
    "winerror = None\n"
    "content_hash = None\n"
    "try:\n"
    "    if mode == 'write':\n"
    "        with open(target, 'wb') as f:\n"
    "            f.write(content.encode('ascii'))\n"
    "        outcome = 'wrote'\n"
    "        content_hash = hashlib.sha256(content.encode('ascii')).hexdigest()\n"
    "    else:\n"
    "        with open(target, 'rb') as f:\n"
    "            data = f.read()\n"
    "        outcome = 'read'\n"
    "        content_hash = hashlib.sha256(data).hexdigest()\n"
    "except OSError as e:\n"
    "    outcome = 'denied'\n"
    "    winerror = getattr(e, 'winerror', None)\n"
    "print(json.dumps({'token': token_probe(), 'mode': mode, 'outcome': outcome,\n"
    "                  'winerror': winerror, 'content_hash': content_hash,\n"
    "                  'elapsed_s': round(time.time() - t0, 3)}), flush=True)\n"
)


def _parse_client(out: str) -> dict:
    try:
        data = json.loads(out.strip().splitlines()[-1]) \
            if out.strip() else {}
    except (ValueError, TypeError):
        return {}
    return data


# ---------------------------------------------------------------- 场景执行

def _run_client(cmd: list[str], sandbox: bool, work: Path, env: dict) -> dict:
    rec = {"command": cmd, "spawned": False, "rc": None, "timed_out": False,
           "data": {}, "raw_out": ""}
    try:
        if sandbox:
            cp = ac.run_appcontainer(cmd, cwd=work, env=env, allowed_dirs=[],
                                     timeout_ms=15_000)
        else:
            cp = subprocess.run(cmd, cwd=work, capture_output=True, timeout=15)
        rec["spawned"] = True
        rec["rc"] = cp.returncode
        rec["raw_out"] = ((cp.stdout or b"") + (cp.stderr or b"")).decode(
            "utf-8", "replace")
        rec["data"] = _parse_client(rec["raw_out"])
    except subprocess.TimeoutExpired as e:
        rec["timed_out"] = True
        rec["raw_out"] = ((e.output or b"") + (getattr(e, "stderr", None) or b"")
                          ).decode("utf-8", "replace")
        rec["data"] = _parse_client(rec["raw_out"])
    except OSError as e:
        rec["error"] = repr(e)
    return rec


def _case(work: Path, denied_dir: Path, runtime: Path, env: dict,
          expected_sid: str, client: Path) -> dict:
    rec = {"client_sha256": _sha_file(client)}
    # ---- 1. granted_write ----
    nonce1 = uuid.uuid4().hex
    tgt1 = work / f"granted-write-{nonce1}.bin"
    c1 = _run_client([str(runtime), "-X", "utf8", str(client), "write",
                      str(tgt1), nonce1], False, work, env)
    s1 = _run_client([str(runtime), "-X", "utf8", str(client), "write",
                      str(tgt1), nonce1], True, work, env)
    expected_h = hashlib.sha256(nonce1.encode("ascii")).hexdigest()
    # ---- 2. granted_read ----
    nonce2 = uuid.uuid4().hex
    src2 = work / "granted-read.bin"
    src2.write_text(nonce2, encoding="ascii")
    c2 = _run_client([str(runtime), "-X", "utf8", str(client), "read",
                      str(src2), nonce2], False, work, env)
    s2 = _run_client([str(runtime), "-X", "utf8", str(client), "read",
                      str(src2), nonce2], True, work, env)
    h2 = hashlib.sha256(nonce2.encode("ascii")).hexdigest()
    # ---- 3. denied_write ----
    nonce3 = uuid.uuid4().hex
    tgt3c = denied_dir / f"denied-write-ctrl-{nonce3}.bin"
    tgt3s = denied_dir / f"denied-write-sb-{nonce3}.bin"
    c3 = _run_client([str(runtime), "-X", "utf8", str(client), "write",
                      str(tgt3c), nonce3], False, work, env)
    tgt3c.unlink(missing_ok=True)  # 控制端清理,仅验证"普通进程可写该目录"
    s3 = _run_client([str(runtime), "-X", "utf8", str(client), "write",
                      str(tgt3s), nonce3], True, work, env)
    # ---- 4. denied_read ----
    nonce4 = uuid.uuid4().hex
    sentinel = denied_dir / "sentinel.bin"
    sentinel.write_text(nonce4, encoding="ascii")
    c4 = _run_client([str(runtime), "-X", "utf8", str(client), "read",
                      str(sentinel), nonce4], False, work, env)
    s4 = _run_client([str(runtime), "-X", "utf8", str(client), "read",
                      str(sentinel), nonce4], True, work, env)
    h4 = hashlib.sha256(nonce4.encode("ascii")).hexdigest()
    # 组装判定输入(监督端文件系统事实复核)
    rec["cases"] = {}
    tok1 = s1["data"].get("token") or {}
    rec["cases"]["granted_write"] = _judge_case(
        "granted_write",
        {"spawned": c1["spawned"], "rc": c1["rc"], "timed_out": c1["timed_out"],
         "succeeded": c1["data"].get("outcome") == "wrote"},
        {"spawned": s1["spawned"], "rc": s1["rc"], "timed_out": s1["timed_out"],
         "token29": tok1.get("is_appcontainer") is True and tok1.get("api_ok") is True,
         "sid_ok": tok1.get("sid") == expected_sid,
         "outcome": s1["data"].get("outcome"),
         "winerror": s1["data"].get("winerror"),
         "succeeded": s1["data"].get("outcome") == "wrote",
         "hash_ok": s1["data"].get("content_hash") == expected_h
         and _sha_file(tgt1) == expected_h,
         "target_created": tgt1.exists(), "content_leaked": None})
    tok2 = s2["data"].get("token") or {}
    rec["cases"]["granted_read"] = _judge_case(
        "granted_read",
        {"spawned": c2["spawned"], "rc": c2["rc"], "timed_out": c2["timed_out"],
         "succeeded": c2["data"].get("outcome") == "read"
         and c2["data"].get("content_hash") == h2},
        {"spawned": s2["spawned"], "rc": s2["rc"], "timed_out": s2["timed_out"],
         "token29": tok2.get("is_appcontainer") is True and tok2.get("api_ok") is True,
         "sid_ok": tok2.get("sid") == expected_sid,
         "outcome": s2["data"].get("outcome"),
         "winerror": s2["data"].get("winerror"),
         "succeeded": s2["data"].get("outcome") == "read",
         "hash_ok": s2["data"].get("content_hash") == h2,
         "target_created": None, "content_leaked": None})
    tok3 = s3["data"].get("token") or {}
    rec["cases"]["denied_write"] = _judge_case(
        "denied_write",
        {"spawned": c3["spawned"], "rc": c3["rc"], "timed_out": c3["timed_out"],
         "succeeded": c3["data"].get("outcome") == "wrote"},
        {"spawned": s3["spawned"], "rc": s3["rc"], "timed_out": s3["timed_out"],
         "token29": tok3.get("is_appcontainer") is True and tok3.get("api_ok") is True,
         "sid_ok": tok3.get("sid") == expected_sid,
         "outcome": s3["data"].get("outcome"),
         "winerror": s3["data"].get("winerror"),
         "succeeded": None, "hash_ok": None,
         "target_created": tgt3s.exists(), "content_leaked": None})
    tok4 = s4["data"].get("token") or {}
    rec["cases"]["denied_read"] = _judge_case(
        "denied_read",
        {"spawned": c4["spawned"], "rc": c4["rc"], "timed_out": c4["timed_out"],
         "succeeded": c4["data"].get("outcome") == "read"
         and c4["data"].get("content_hash") == h4},
        {"spawned": s4["spawned"], "rc": s4["rc"], "timed_out": s4["timed_out"],
         "token29": tok4.get("is_appcontainer") is True and tok4.get("api_ok") is True,
         "sid_ok": tok4.get("sid") == expected_sid,
         "outcome": s4["data"].get("outcome"),
         "winerror": s4["data"].get("winerror"),
         "succeeded": None, "hash_ok": None,
         "target_created": None,
         "content_leaked": s4["data"].get("content_hash") == h4})
    rec["raw"] = {"granted_write": {"control": c1, "sandbox": s1,
                                    "target": str(tgt1), "expected_sha256": expected_h},
                  "granted_read": {"control": c2, "sandbox": s2,
                                   "target": str(src2), "expected_sha256": h2},
                  "denied_write": {"control": c3, "sandbox": s3,
                                   "target": str(tgt3s)},
                  "denied_read": {"control": c4, "sandbox": s4,
                                  "target": str(sentinel), "expected_sha256": h4}}
    verdicts = [v["verdict"] for v in rec["cases"].values()]
    if "FAIL" in verdicts:
        rec["overall"] = "FAIL"
    elif "UNVERIFIED" in verdicts:
        rec["overall"] = "UNVERIFIED"
    else:
        rec["overall"] = "PASS_LOCAL_FILE_ACL"
    return rec


def main() -> int:
    run_id = uuid.uuid4().hex[:12]
    work = SUPPORT / f"file-work-{run_id}"
    denied_dir = SUPPORT / f"file-denied-{run_id}"
    _check_paths(work, "work")
    _check_paths(denied_dir, "denied_dir")
    EVIDENCE.mkdir(exist_ok=True)
    results: dict = {}
    try:
        runtime = NET_RUNTIME / "python.exe"
        if not runtime.exists():
            raise FileNotFoundError("net-runtime 副本缺失,请先运行网络验收生成")
        denied_dir.mkdir()
        profile = ac.appcontainer_profile_path(ac.appcontainer_sid())
        sid = ac.appcontainer_sid()
        expected_sid = ac._sid_sddl(sid)
        # ACL 仅授予具名工作区(work rw);denied_dir 不授予
        ac.grant_dir_access(work, sid, write=True)
        env = {"SYSTEMROOT": r"C:\Windows",
               "SystemDrive": os.environ.get("SystemDrive", "C:"),
               "windir": os.environ.get("windir", r"C:\Windows"),
               "USERNAME": os.environ.get("USERNAME", ""),
               "USERDOMAIN": os.environ.get("USERDOMAIN", ""),
               "PATH": ";".join([str(NET_RUNTIME), r"C:\Windows\System32"]),
               "TEMP": str(work), "TMP": str(work),
               "LOCALAPPDATA": str(profile), "APPDATA": str(profile),
               "USERPROFILE": str(profile),
               "PATHEXT": ".COM;.EXE;.BAT;.CMD"}
        client = work / "file_client.py"
        client.write_text(_CLIENT, encoding="utf-8")
        results = {"schema": 1, "run_id": run_id, "contract": CONTRACT,
                   "scope": "仅本次具名目录/操作的本地文件读写隔离;"
                            "不构成整体文件隔离或生产放行结论",
                   "state": "RUNNING", "overall": "UNVERIFIED",
                   "command": [sys.executable] + sys.argv,
                   "work": str(work), "denied_dir": str(denied_dir),
                   "runtime": str(runtime), "profile": str(profile),
                   "expected_sid": expected_sid,
                   "pre_granted_acl": [[str(work), "read_write"]],
                   "allowed_dirs": [], "sandbox_env": dict(env),
                   "negative_regressions": _negative_regressions(),
                   "source_hashes": {
                       "script_sha256": hashlib.sha256(
                           Path(__file__).read_bytes()).hexdigest(),
                       "appcontainer_sha256": hashlib.sha256(
                           (ROOT / "src/animtrain/appcontainer.py").read_bytes()
                       ).hexdigest(),
                       "win_job_sha256": hashlib.sha256(
                           (ROOT / "src/animtrain/win_job.py").read_bytes()
                       ).hexdigest(),
                       "runtime_python_sha256": hashlib.sha256(
                           runtime.read_bytes()).hexdigest(),
                       "client_file_sha256": hashlib.sha256(
                           client.read_bytes()).hexdigest()}}
        results["case"] = _case(work, denied_dir, runtime, env, expected_sid,
                                client)
        results["overall"] = results["case"]["overall"]
        results["state"] = "COMPLETE"
        _assert_json_safe(results, "results")
        ok = (results["negative_regressions"]["all_hold"]
              and results["overall"] == "PASS_LOCAL_FILE_ACL")
    except Exception as e:  # noqa: BLE001 兜底:任何异常落错误证据,不裸崩溃
        import traceback
        err_rec = {"error": repr(e), "traceback": traceback.format_exc(),
                   "command": [sys.executable] + sys.argv, "run_id": run_id,
                   "partial_results_keys": list(results.keys())}
        (EVIDENCE / f"file-accept-error-{run_id}.json").write_text(
            json.dumps(err_rec, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps(err_rec, ensure_ascii=False, indent=2))
        return 2
    out = EVIDENCE / f"file-accept-results-{run_id}.json"
    tmp = out.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(results, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    tmp.replace(out)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    return {"PASS_LOCAL_FILE_ACL": 0, "FAIL": 1, "UNVERIFIED": 2}[results["overall"]]


if __name__ == "__main__":
    sys.exit(main())
