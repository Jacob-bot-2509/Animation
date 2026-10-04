r"""文件读写隔离验收 v3:AppContainer 沙箱对具名工作区的读/写正反对照。

v3 修改清单(应 msg_341 六缺口):
  1. granted_read/denied_read 目标稳定性入判定(hash_before==hash_after==期望,
     测试期间文件被改 → UNVERIFIED,不再仅记录);
  2. granted_write 沙箱目标前置不存在(sb_pre_exists is False)入判定;
  3. 自检(negative_regressions.all_hold)前置于一切副作用之前失败关闭:
     ACL 授予/目录创建/场景执行均不发生,JSON 与退出码同步 UNVERIFIED/2;
  4. 后核验:场景执行后重验 runtime 关键文件/._pth/客户端/本脚本哈希前后
     一致,任一变化 → 不得 PASS(已确证 FAIL 保留);
  5. 逐步骤增量:_case 每类独立 try/except,异常记录为该类 UNVERIFIED,
     不覆盖早先已确证的 FAIL/原始记录;
  6. 错误证据=完整部分结果(非仅 keys),统一 _write_json 原子写入+兜底
     落 SUPPORT;EVIDENCE 目录在 try 外前置就绪。

契约与范围:仅本支持目录内具名工作区 file-work-<run_id>/(授 rw ACE)与
file-denied-<run_id>/(不授);复用既有生产 profile;仅合成数据;不改核心四
文件/门禁/防火墙/C 盘系统文件;标签 PASS_LOCAL_FILE_ACL 仅覆盖本次测试
具名目录与操作,不构成整体文件隔离或生产放行结论。
"""
from __future__ import annotations

import hashlib
import inspect
import json
import os
import subprocess
import sys
import time
import traceback
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from animtrain import appcontainer as ac  # noqa: E402
from animtrain import network_isolation as net  # noqa: E402

SUPPORT = Path(__file__).resolve().parent
NET_RUNTIME = SUPPORT / "net-runtime"
EVIDENCE = SUPPORT / "file-evidence"
CODEX_RUNTIME = Path(
    r"D:\Animation-Model-Training\reviews\codex-supervision\history-from-code"
    r"\fix-2026-10-04\appcontainer-probe-wenbjyjh\runtime")
RUNTIME_KEY_FILES = ["python.exe", "python313.dll", "Lib/socket.py",
                     "DLLs/_socket.pyd"]
ACCESS_DENIED = 5
CONTRACT = "local-file-acl-v1"
KNOWN_KINDS = ("granted_write", "granted_read", "denied_write", "denied_read")


def _named_dir(path: Path, name: str) -> None:
    p = path.resolve()
    if not p.is_relative_to(SUPPORT.resolve()):
        raise ValueError(f"{name} 越出支持目录: {p}")
    if p.exists():
        raise FileExistsError(f"{name} 已存在,拒绝重用: {p}")


def _sha_file(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


def _sha_str(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _pth_ok(content: str | None) -> bool:
    if not content:
        return False
    lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
    return bool(lines) and all(ln in ("Lib", "DLLs", ".")
                               for ln in lines)


def _assert_json_safe(obj, where: str) -> None:
    if isinstance(obj, bytes):
        raise TypeError(f"{where}: 发现未转换的 bytes 字段")
    if isinstance(obj, dict):
        for k, v in obj.items():
            _assert_json_safe(v, f"{where}.{k}")
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            _assert_json_safe(v, f"{where}[{i}]")


def _write_json(path: Path, obj) -> Path:
    """统一原子写入;目标不可写时兜底落 SUPPORT 并返回实际路径。"""
    try:
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2),
                       encoding="utf-8")
        tmp.replace(path)
        return path
    except OSError:
        fb = SUPPORT / ("fallback-" + path.name)
        fb.write_text(json.dumps(obj, ensure_ascii=False, indent=2),
                      encoding="utf-8")
        return fb


# ---------------------------------------------------------------- 纯判定谓词

def _judge_case(kind: str, control: dict, sandbox: dict) -> dict:
    """单例判定(纯谓词,只吃观测值)。FAIL 最高优先级,未知一律 UNVERIFIED,
    所有布尔字段严格 is True / is False。"""
    reasons: list[str] = []
    if kind not in KNOWN_KINDS:
        return {"verdict": "UNVERIFIED", "reasons": [f"未知场景 {kind!r}"],
                "contract": CONTRACT}
    if kind == "denied_write" and sandbox.get("target_created") is True:
        return {"verdict": "FAIL", "reasons": ["沙箱写入未授权目标成功(隔离击穿)"],
                "contract": CONTRACT}
    if kind == "denied_read" and sandbox.get("content_leaked") is True:
        return {"verdict": "FAIL", "reasons": ["沙箱读到未授权哨兵内容(隔离击穿)"],
                "contract": CONTRACT}
    if control.get("spawned") is not True:
        reasons.append("控制端未启动/状态非布尔真")
    if type(control.get("rc")) is not int or control.get("rc") != 0:
        reasons.append("控制端 rc 非 0/非整数")
    if control.get("timed_out") is not False:
        reasons.append("控制端超时/状态未知")
    if control.get("succeeded") is not True:
        reasons.append("控制端未实际成功")
    if sandbox.get("spawned") is not True:
        reasons.append("沙箱未启动/状态非布尔真")
    if type(sandbox.get("rc")) is not int or sandbox.get("rc") != 0:
        reasons.append("沙箱 rc 非 0/非整数")
    if sandbox.get("timed_out") is not False:
        reasons.append("沙箱超时/状态未知")
    if sandbox.get("token29") is not True:
        reasons.append("TokenIsAppContainer=29 证据缺失或 API 失败")
    if sandbox.get("sid_ok") is not True:
        reasons.append("类31 SID 与预期不一致")
    if sandbox.get("client_ok") is not True:
        reasons.append("客户端/解释器自哈希或路径校验失败")
    if kind in ("granted_write", "granted_read"):
        if sandbox.get("succeeded") is not True or sandbox.get("hash_ok") is not True:
            reasons.append("授予类操作未成功或哈希不一致")
    if kind == "granted_write" and sandbox.get("sb_pre_exists") is not False:
        reasons.append("沙箱写入目标前置状态未知/已存在")
    if kind in ("granted_read", "denied_read") and sandbox.get("target_stable") is not True:
        reasons.append("目标文件测试期间被改动(前后哈希不一致)")
    if kind == "denied_write":
        if sandbox.get("outcome") != "denied":
            reasons.append("拒绝写结果无法解释")
        if sandbox.get("winerror") != ACCESS_DENIED:
            reasons.append(f"非明确拒绝 winerror={sandbox.get('winerror')}"
                           f"(仅接受 5=ACCESS_DENIED)")
        if sandbox.get("target_created") is not False:
            reasons.append("拒绝写目标状态未知/非明确未创建")
    if kind == "denied_read":
        if sandbox.get("outcome") != "denied":
            reasons.append("拒绝读结果无法解释")
        if sandbox.get("winerror") != ACCESS_DENIED:
            reasons.append(f"非明确拒绝 winerror={sandbox.get('winerror')}"
                           f"(仅接受 5=ACCESS_DENIED)")
        if sandbox.get("content_leaked") is not False:
            reasons.append("拒绝读泄漏状态未知/非明确未泄漏")
    if reasons:
        return {"verdict": "UNVERIFIED", "reasons": reasons, "contract": CONTRACT}
    return {"verdict": "PASS", "reasons": [], "contract": CONTRACT}


def _negative_regressions() -> dict:
    base_control = {"spawned": True, "rc": 0, "timed_out": False, "succeeded": True}
    base_sandbox = {"spawned": True, "rc": 0, "timed_out": False, "token29": True,
                    "sid_ok": True, "client_ok": True, "outcome": None,
                    "winerror": None, "succeeded": None, "hash_ok": None,
                    "sb_pre_exists": None, "target_stable": None,
                    "target_created": None, "content_leaked": None}
    cases = []

    def _rec(name: str, verdict: str, expect: str) -> None:
        cases.append({"name": name, "verdict": verdict, "expect": expect,
                      "holds": verdict == expect})

    def _sb(**kw):
        return dict(base_sandbox, **kw)

    def _ct(**kw):
        return dict(base_control, **kw)

    _rec("N1 denied_write 目标出现", _judge_case(
        "denied_write", base_control, _sb(target_created=True))["verdict"], "FAIL")
    _rec("N2 denied_read 内容泄漏", _judge_case(
        "denied_read", base_control, _sb(content_leaked=True))["verdict"], "FAIL")
    _rec("N3 控制端失败", _judge_case(
        "granted_write", _ct(succeeded=False),
        _sb(succeeded=True, hash_ok=True, sb_pre_exists=False))["verdict"],
        "UNVERIFIED")
    _rec("N4 令牌证据缺失", _judge_case(
        "granted_write", base_control, _sb(
            succeeded=True, hash_ok=True, sb_pre_exists=False,
            token29=False))["verdict"], "UNVERIFIED")
    _rec("N5 SID 不符", _judge_case(
        "granted_write", base_control, _sb(
            succeeded=True, hash_ok=True, sb_pre_exists=False,
            sid_ok=False))["verdict"], "UNVERIFIED")
    _rec("N6 授予类哈希不一致", _judge_case(
        "granted_read", base_control, _sb(
            succeeded=True, hash_ok=False, target_stable=True))["verdict"],
        "UNVERIFIED")
    _rec("N7 授予类无记录", _judge_case(
        "granted_write", base_control, _sb())["verdict"], "UNVERIFIED")
    _rec("N8 拒绝类 winerror 非 5", _judge_case(
        "denied_write", base_control, _sb(
            outcome="denied", winerror=3, target_created=False))["verdict"],
        "UNVERIFIED")
    _rec("N9 拒绝类结果无法解释", _judge_case(
        "denied_read", base_control, _sb(
            outcome="sent", winerror=None, content_leaked=False,
            target_stable=True))["verdict"], "UNVERIFIED")
    _rec("N10 沙箱未启动", _judge_case(
        "granted_write", base_control, _sb(spawned=False))["verdict"], "UNVERIFIED")
    _rec("N11 拒写目标状态未知", _judge_case(
        "denied_write", base_control, _sb(
            outcome="denied", winerror=ACCESS_DENIED,
            target_created=None))["verdict"], "UNVERIFIED")
    _rec("N12 拒读泄漏状态未知", _judge_case(
        "denied_read", base_control, _sb(
            outcome="denied", winerror=ACCESS_DENIED,
            content_leaked=None, target_stable=True))["verdict"], "UNVERIFIED")
    _rec("N13 沙箱超时状态未知", _judge_case(
        "granted_write", base_control, _sb(
            succeeded=True, hash_ok=True, sb_pre_exists=False,
            timed_out=None))["verdict"], "UNVERIFIED")
    _rec("N14 控制超时状态未知", _judge_case(
        "granted_write", _ct(timed_out=None), _sb(
            succeeded=True, hash_ok=True, sb_pre_exists=False))["verdict"],
        "UNVERIFIED")
    _rec("N15 控制 spawned 非布尔", _judge_case(
        "granted_write", _ct(spawned=1), _sb(
            succeeded=True, hash_ok=True, sb_pre_exists=False))["verdict"],
        "UNVERIFIED")
    _rec("N16 未知场景 kind", _judge_case(
        "granted_delete", base_control, _sb())["verdict"], "UNVERIFIED")
    _rec("N17 客户端自哈希缺失", _judge_case(
        "granted_write", base_control, _sb(
            succeeded=True, hash_ok=True, sb_pre_exists=False,
            client_ok=False))["verdict"], "UNVERIFIED")
    _rec("N18 正写目标前置已存在", _judge_case(
        "granted_write", base_control, _sb(
            succeeded=True, hash_ok=True, sb_pre_exists=True))["verdict"],
        "UNVERIFIED")
    _rec("N19 授予读目标被改动", _judge_case(
        "granted_read", base_control, _sb(
            succeeded=True, hash_ok=True, target_stable=False))["verdict"],
        "UNVERIFIED")
    _rec("N20 拒读哨兵被改动", _judge_case(
        "denied_read", base_control, _sb(
            outcome="denied", winerror=ACCESS_DENIED, content_leaked=False,
            target_stable=False))["verdict"], "UNVERIFIED")
    _rec("P1 granted_write 基线", _judge_case(
        "granted_write", base_control, _sb(
            succeeded=True, hash_ok=True, sb_pre_exists=False))["verdict"], "PASS")
    _rec("P2 denied_write 基线", _judge_case(
        "denied_write", base_control, _sb(
            outcome="denied", winerror=ACCESS_DENIED,
            target_created=False))["verdict"], "PASS")
    _rec("P3 granted_read 基线", _judge_case(
        "granted_read", base_control, _sb(
            succeeded=True, hash_ok=True, target_stable=True))["verdict"], "PASS")
    _rec("P4 denied_read 基线", _judge_case(
        "denied_read", base_control, _sb(
            outcome="denied", winerror=ACCESS_DENIED, content_leaked=False,
            target_stable=True))["verdict"], "PASS")
    return {"cases": cases, "all_hold": all(c["holds"] for c in cases)}


# ---------------------------------------------------------------- 客户端代码

_CLIENT = inspect.getsource(net.token_identity) + '''
import hashlib, json, sys, time
mode, target, content = sys.argv[1], sys.argv[2], sys.argv[3]
t0 = time.time()
outcome = None
winerror = None
content_hash = None
try:
    if mode == 'write':
        with open(target, 'wb') as f:
            f.write(content.encode('ascii'))
        outcome = 'wrote'
        content_hash = hashlib.sha256(content.encode('ascii')).hexdigest()
    else:
        with open(target, 'rb') as f:
            data = f.read()
        outcome = 'read'
        content_hash = hashlib.sha256(data).hexdigest()
except OSError as e:
    outcome = 'denied'
    winerror = getattr(e, 'winerror', None)

def _sha(p):
    try:
        with open(p, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None

print(json.dumps({'token': token_identity(), 'mode': mode, 'outcome': outcome,
                  'winerror': winerror, 'content_hash': content_hash,
                  'client_sha256': _sha(sys.argv[0]), 'exe_sha256': _sha(sys.executable),
                  'site_absent': 'site' not in sys.modules and 'sitecustomize' not in sys.modules,
                  'executable': sys.executable,
                  'elapsed_s': round(time.time() - t0, 3)}), flush=True)
'''


def _parse_client(out: str) -> dict:
    try:
        return json.loads(out.strip().splitlines()[-1]) if out.strip() else {}
    except (ValueError, TypeError):
        return {}


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


def _client_ok(data: dict, cfg: dict) -> bool:
    return (data.get("client_sha256") == cfg["client_sha256"]
            and data.get("exe_sha256") == cfg["runtime_python_sha256"]
            and data.get("site_absent") is True
            and os.path.normcase(str(data.get("executable", "")))
            == os.path.normcase(str(cfg["runtime"])))


def _run_granted_write(work: Path, runtime: Path, env: dict, expected_sid: str,
                       client: Path, cfg: dict):
    n_ctrl, n_sb = uuid.uuid4().hex, uuid.uuid4().hex
    tgt_c, tgt_s = work / f"gw-ctrl-{n_ctrl}.bin", work / f"gw-sb-{n_sb}.bin"
    sb_pre_exists = tgt_s.exists()
    c1 = _run_client([str(runtime), "-X", "utf8", str(client), "write",
                      str(tgt_c), n_ctrl], False, work, env)
    s1 = _run_client([str(runtime), "-X", "utf8", str(client), "write",
                      str(tgt_s), n_sb], True, work, env)
    h_c, h_s = _sha_file(tgt_c), _sha_file(tgt_s)
    h_ctrl_exp, h_sb_exp = (hashlib.sha256(n_ctrl.encode("ascii")).hexdigest(),
                            hashlib.sha256(n_sb.encode("ascii")).hexdigest())
    tok1 = s1["data"].get("token") or {}
    verdict = _judge_case(
        "granted_write",
        {"spawned": c1["spawned"], "rc": c1["rc"], "timed_out": c1["timed_out"],
         "succeeded": c1["data"].get("outcome") == "wrote" and h_c == h_ctrl_exp},
        {"spawned": s1["spawned"], "rc": s1["rc"], "timed_out": s1["timed_out"],
         "token29": tok1.get("api_ok") is True
         and tok1.get("is_appcontainer") is True,
         "sid_ok": tok1.get("sid") == expected_sid,
         "client_ok": _client_ok(s1["data"], cfg),
         "succeeded": s1["data"].get("outcome") == "wrote",
         "hash_ok": s1["data"].get("content_hash") == h_sb_exp
         and h_s == h_sb_exp,
         "sb_pre_exists": sb_pre_exists,
         "target_created": None, "content_leaked": None,
         "outcome": s1["data"].get("outcome"),
         "winerror": s1["data"].get("winerror")})
    raw = {"control": c1, "sandbox": s1, "ctrl_target": str(tgt_c),
           "sb_target": str(tgt_s), "sb_pre_exists": sb_pre_exists,
           "ctrl_sha256": h_c, "ctrl_expected_sha256": h_ctrl_exp,
           "sb_sha256": h_s, "sb_expected_sha256": h_sb_exp}
    return verdict, raw


def _run_granted_read(work: Path, runtime: Path, env: dict, expected_sid: str,
                      client: Path, cfg: dict):
    n2 = uuid.uuid4().hex
    src2 = work / "granted-read.bin"
    src2.write_text(n2, encoding="ascii")
    h2 = hashlib.sha256(n2.encode("ascii")).hexdigest()
    h2_before = _sha_file(src2)
    c2 = _run_client([str(runtime), "-X", "utf8", str(client), "read",
                      str(src2), "x" * 32], False, work, env)
    s2 = _run_client([str(runtime), "-X", "utf8", str(client), "read",
                      str(src2), "x" * 32], True, work, env)
    h2_after = _sha_file(src2)
    tok2 = s2["data"].get("token") or {}
    verdict = _judge_case(
        "granted_read",
        {"spawned": c2["spawned"], "rc": c2["rc"], "timed_out": c2["timed_out"],
         "succeeded": c2["data"].get("outcome") == "read"
         and c2["data"].get("content_hash") == h2},
        {"spawned": s2["spawned"], "rc": s2["rc"], "timed_out": s2["timed_out"],
         "token29": tok2.get("api_ok") is True
         and tok2.get("is_appcontainer") is True,
         "sid_ok": tok2.get("sid") == expected_sid,
         "client_ok": _client_ok(s2["data"], cfg),
         "succeeded": s2["data"].get("outcome") == "read",
         "hash_ok": s2["data"].get("content_hash") == h2,
         "target_stable": h2_before == h2 and h2_after == h2,
         "target_created": None, "content_leaked": None,
         "outcome": s2["data"].get("outcome"),
         "winerror": s2["data"].get("winerror")})
    raw = {"control": c2, "sandbox": s2, "target": str(src2),
           "expected_sha256": h2, "hash_before": h2_before,
           "hash_after": h2_after}
    return verdict, raw


def _run_denied_write(denied_dir: Path, work: Path, runtime: Path, env: dict,
                      expected_sid: str, client: Path, cfg: dict):
    n3 = uuid.uuid4().hex
    tgt3c = denied_dir / f"dw-ctrl-{n3}.bin"
    tgt3s = denied_dir / f"dw-sb-{n3}.bin"
    c3 = _run_client([str(runtime), "-X", "utf8", str(client), "write",
                      str(tgt3c), n3], False, work, env)
    h3 = _sha_file(tgt3c)
    h3_exp = hashlib.sha256(n3.encode("ascii")).hexdigest()
    ctrl3_ok = c3["data"].get("outcome") == "wrote" and h3 == h3_exp
    tgt3c.unlink(missing_ok=True)
    s3 = _run_client([str(runtime), "-X", "utf8", str(client), "write",
                      str(tgt3s), n3], True, work, env)
    tok3 = s3["data"].get("token") or {}
    verdict = _judge_case(
        "denied_write",
        {"spawned": c3["spawned"], "rc": c3["rc"], "timed_out": c3["timed_out"],
         "succeeded": ctrl3_ok},
        {"spawned": s3["spawned"], "rc": s3["rc"], "timed_out": s3["timed_out"],
         "token29": tok3.get("api_ok") is True
         and tok3.get("is_appcontainer") is True,
         "sid_ok": tok3.get("sid") == expected_sid,
         "client_ok": _client_ok(s3["data"], cfg),
         "outcome": s3["data"].get("outcome"),
         "winerror": s3["data"].get("winerror"),
         "succeeded": None, "hash_ok": None,
         "target_created": tgt3s.exists(), "content_leaked": None})
    raw = {"control": c3, "sandbox": s3, "ctrl_target": str(tgt3c),
           "ctrl_sha256": h3, "ctrl_expected_sha256": h3_exp,
           "sb_target": str(tgt3s)}
    return verdict, raw


def _run_denied_read(denied_dir: Path, work: Path, runtime: Path, env: dict,
                     expected_sid: str, client: Path, cfg: dict):
    n4 = uuid.uuid4().hex
    sentinel = denied_dir / "sentinel.bin"
    sentinel.write_text(n4, encoding="ascii")
    h4 = hashlib.sha256(n4.encode("ascii")).hexdigest()
    h4_before = _sha_file(sentinel)
    c4 = _run_client([str(runtime), "-X", "utf8", str(client), "read",
                      str(sentinel), "x" * 32], False, work, env)
    s4 = _run_client([str(runtime), "-X", "utf8", str(client), "read",
                      str(sentinel), "x" * 32], True, work, env)
    h4_after = _sha_file(sentinel)
    tok4 = s4["data"].get("token") or {}
    verdict = _judge_case(
        "denied_read",
        {"spawned": c4["spawned"], "rc": c4["rc"], "timed_out": c4["timed_out"],
         "succeeded": c4["data"].get("outcome") == "read"
         and c4["data"].get("content_hash") == h4},
        {"spawned": s4["spawned"], "rc": s4["rc"], "timed_out": s4["timed_out"],
         "token29": tok4.get("api_ok") is True
         and tok4.get("is_appcontainer") is True,
         "sid_ok": tok4.get("sid") == expected_sid,
         "client_ok": _client_ok(s4["data"], cfg),
         "outcome": s4["data"].get("outcome"),
         "winerror": s4["data"].get("winerror"),
         "succeeded": None, "hash_ok": None,
         "target_created": None,
         "content_leaked": s4["data"].get("content_hash") == h4,
         "target_stable": h4_before == h4 and h4_after == h4})
    raw = {"control": c4, "sandbox": s4, "target": str(sentinel),
           "expected_sha256": h4, "hash_before": h4_before,
           "hash_after": h4_after}
    return verdict, raw


def _case(work: Path, denied_dir: Path, runtime: Path, env: dict,
          expected_sid: str, client: Path, cfg: dict) -> dict:
    """逐步骤增量:每类独立 try/except,异常不覆盖早先已确证的 FAIL/原始记录。"""
    rec: dict = {"cases": {}, "raw": {}, "errors": []}
    steps = [
        ("granted_write", lambda: _run_granted_write(
            work, runtime, env, expected_sid, client, cfg)),
        ("granted_read", lambda: _run_granted_read(
            work, runtime, env, expected_sid, client, cfg)),
        ("denied_write", lambda: _run_denied_write(
            denied_dir, work, runtime, env, expected_sid, client, cfg)),
        ("denied_read", lambda: _run_denied_read(
            denied_dir, work, runtime, env, expected_sid, client, cfg)),
    ]
    for kind, fn in steps:
        try:
            verdict, raw = fn()
            rec["cases"][kind] = verdict
            rec["raw"][kind] = raw
        except Exception as e:  # noqa: BLE001 单类异常不影响已确证结果
            rec["errors"].append({"kind": kind, "error": repr(e),
                                  "traceback": traceback.format_exc()})
            rec["cases"][kind] = {"verdict": "UNVERIFIED",
                                  "reasons": [f"执行异常: {e!r}"],
                                  "contract": CONTRACT}
            rec["raw"][kind] = {"exception": repr(e)}
    verdicts = [v["verdict"] for v in rec["cases"].values()]
    if "FAIL" in verdicts:
        rec["overall"] = "FAIL"
    elif "UNVERIFIED" in verdicts or rec["errors"]:
        rec["overall"] = "UNVERIFIED"
    else:
        rec["overall"] = "PASS_LOCAL_FILE_ACL"
    return rec


def _post_verify(cfg: dict, manifest: dict, pth_before: str,
                 script_sha_before: str) -> dict:
    """场景执行后重验:runtime 关键文件/._pth/客户端/本脚本前后一致。"""
    checks: dict = {}
    for rel, sha in manifest.items():
        cur = _sha_file(NET_RUNTIME / rel)
        checks[rel] = cur == sha
    pth_now = (NET_RUNTIME / "python313._pth").read_text(
        encoding="utf-8", errors="replace") if (NET_RUNTIME / "python313._pth").exists() else None
    checks["pth"] = pth_now == pth_before
    client = Path(cfg["client_path"])
    checks["client_file"] = _sha_file(client) == cfg["client_sha256"]
    checks["script"] = _sha_file(Path(__file__)) == script_sha_before
    return {"all_unchanged": all(checks.values()), "checks": checks}


def main() -> int:
    run_id = uuid.uuid4().hex[:12]
    work = SUPPORT / f"file-work-{run_id}"
    denied_dir = SUPPORT / f"file-denied-{run_id}"
    EVIDENCE.mkdir(exist_ok=True)  # 错误路径依赖,置于 try 外
    results: dict = {"schema": 3, "run_id": run_id, "contract": CONTRACT,
                     "scope": "仅本次具名目录/操作的本地文件读写隔离;"
                              "不构成整体文件隔离或生产放行结论",
                     "state": "RUNNING", "overall": "UNVERIFIED",
                     "production_gate": "CLOSED",
                     "command": [sys.executable] + sys.argv,
                     "work": str(work), "denied_dir": str(denied_dir)}
    # 自检前置:失败关闭——ACL/目录/场景执行均不发生
    neg = _negative_regressions()
    results["negative_regressions"] = neg
    if not neg["all_hold"]:
        results.update(state="ERROR", overall="UNVERIFIED",
                       error="内置负例自检未全持,拒绝执行")
        _write_json(EVIDENCE / f"file-accept-error-{run_id}.json", results)
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 2
    try:
        _named_dir(work, "work")
        _named_dir(denied_dir, "denied_dir")
        manifest = {}
        for rel in RUNTIME_KEY_FILES:
            src = CODEX_RUNTIME / rel
            if not src.exists():
                raise FileNotFoundError(f"授权运行时源缺失: {src}")
            manifest[rel] = hashlib.sha256(src.read_bytes()).hexdigest()
        runtime = NET_RUNTIME / "python.exe"
        for rel, sha in manifest.items():
            dst = NET_RUNTIME / rel
            if not dst.exists() or hashlib.sha256(dst.read_bytes()).hexdigest() != sha:
                raise OSError(f"net-runtime 副本与授权源不一致: {rel}")
        pth = (NET_RUNTIME / "python313._pth").read_text(
            encoding="utf-8", errors="replace")
        if not _pth_ok(pth):
            raise OSError("net-runtime ._pth 隔离配置核验失败")
        script_sha_before = _sha_file(Path(__file__))
        work.mkdir()
        denied_dir.mkdir()
        profile = ac.appcontainer_profile_path(ac.appcontainer_sid())
        sid = ac.appcontainer_sid()
        expected_sid = ac._sid_sddl(sid)
        ac.grant_dir_access(NET_RUNTIME, sid, write=False)
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
        cfg = {"client_sha256": hashlib.sha256(client.read_bytes()).hexdigest(),
               "runtime_python_sha256": hashlib.sha256(runtime.read_bytes()).hexdigest(),
               "runtime": runtime, "client_path": str(client)}
        results.update(
            runtime=str(runtime), profile=str(profile),
            expected_sid=expected_sid,
            pre_granted_acl=[[str(NET_RUNTIME), "read"],
                             [str(work), "read_write"]],
            allowed_dirs=[], sandbox_env=dict(env),
            runtime_pth=pth, runtime_pth_ok=True,
            source_hashes={
                "script_sha256": script_sha_before,
                "appcontainer_sha256": hashlib.sha256(
                    (ROOT / "src/animtrain/appcontainer.py").read_bytes()
                ).hexdigest(),
                "win_job_sha256": hashlib.sha256(
                    (ROOT / "src/animtrain/win_job.py").read_bytes()
                ).hexdigest(),
                "network_isolation_sha256": hashlib.sha256(
                    (ROOT / "src/animtrain/network_isolation.py").read_bytes()
                ).hexdigest(),
                "runtime_python_sha256": cfg["runtime_python_sha256"],
                "client_file_sha256": cfg["client_sha256"]})
        results["case"] = _case(work, denied_dir, runtime, env, expected_sid,
                                client, cfg)
        results["post_verify"] = _post_verify(cfg, manifest, pth,
                                              script_sha_before)
        # 总体:已确证 FAIL 不被后核验覆盖;后核验失败只降 PASS/UNVERIFIED
        case_overall = results["case"]["overall"]
        if case_overall == "FAIL":
            results["overall"] = "FAIL"
        elif results["post_verify"]["all_unchanged"]:
            results["overall"] = case_overall
        else:
            results["overall"] = "UNVERIFIED"
        results["state"] = "COMPLETE"
        _assert_json_safe(results, "results")
        all_hold = neg["all_hold"]
        ok = (all_hold and results["overall"] == "PASS_LOCAL_FILE_ACL"
              and results["state"] == "COMPLETE")
    except Exception as e:  # noqa: BLE001 完整部分证据,不裸崩溃
        results.update(state="ERROR", overall="UNVERIFIED",
                       error=repr(e), traceback=traceback.format_exc())
        _write_json(EVIDENCE / f"file-accept-error-{run_id}.json", results)
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 2
    out = _write_json(EVIDENCE / f"file-accept-results-{run_id}.json", results)
    print(json.dumps(results, ensure_ascii=False, indent=2))
    if results["overall"] == "FAIL":
        return 1
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
