r"""文件读写隔离验收 v3:AppContainer 沙箱对具名工作区的读/写正反对照。

v3 修改清单(应 msg_341 六缺口):
  1. granted_read/denied_read 目标稳定性入判定(hash_before==hash_after==期望,
     测试期间文件被改 → UNVERIFIED,不再仅记录);
  2. granted_write 沙箱目标前置不存在(sb_pre_exists is False)入判定;
  3. 自检(negative_regressions.all_hold)前置于一切验收副作用之前失败关闭
     (除 EVIDENCE 证据目录前置就绪外,ACL 授予/具名工作目录创建/场景执行
     均不发生),JSON 与退出码同步 UNVERIFIED/2;
  4. 后核验:场景执行后重验 runtime 关键文件/._pth/客户端/本脚本哈希前后
     一致,任一变化 → 不得 PASS(已确证 FAIL 保留);
  5. 逐步骤增量:_case 每类独立 try/except,异常记录为该类 UNVERIFIED,
     不覆盖早先已确证的 FAIL/原始记录;
  6. 错误证据=完整部分结果(非仅 keys),统一 _write_json 原子写入+兜底
     落 SUPPORT;EVIDENCE 目录在 try 外前置就绪。
v3.2(应 msg_347 B/C/D/E):
  7. 文件系统事实先收集:denied_write 目标存在→FAIL 判定独立于客户端解析
     (解析崩溃不丢击穿);
  8. granted_write 沙箱目标前置已存在→直接拒绝执行该操作(不跑任何客户端);
  9. EVIDENCE.mkdir 不可写→stdout 结构化证据+受控退出 2,不裸崩;
  10. 后核验覆盖三个核心模块(appcontainer/win_job/network_isolation),
      前后哈希快照双双落证据供与已验收基线绑定。
v3.3(应 msg_352/353):
  11. denied_read 泄漏事实先行:原始输出中与哨兵一致的哈希即 FAIL,
      不等待令牌/解析成功(坏 token 不掩盖击穿);
  12. 证据写入状态显式化 evidence_written/stdout_only,持久证据不可写时
      PASS 降 UNK、已确证 FAIL 保留;
  13. runtime_manifest/core_manifest_before 直接落证据。
v3.4(应 msg_356/357/358):
  14. 泄漏扫描类型无关化:re.findall 全量扫描原始输出所有 64 位 hex 哈希
      (坏 data 非 dict/content_hash 非 str/前导非匹配哈希均不掩盖);
      _parse_client 非 dict 一律空 dict;
  15. 证据落盘与 stdout 字段一致:_write_evidence_record 先占位落盘、
      成功后设真实路径并重序列化。
v3.5(应对抗复核确认项):
  16. denied_write 判定与 raw 统一使用一次采样的事实快照(修判定输入处
      重复采样 tgt3s.exists() 的 TOCTOU),raw 另记 target_created_resample
      作观察补充。
v3.6(应对抗复核 major):
  17. 异常类逃逸封堵:_parse_client 捕获 Exception(含 RecursionError),
      denied_write/denied_read 沙箱执行包兜底 try/except,任何异常不得
      跳过击穿事实收集与泄漏扫描。
v3.7(应 msg_362):
  18. _write_evidence_record 改单次原子写:每候选路径先预设一致字段再写,
      主失败降级 fallback 时以 fallback 路径字段重建内容,二次写入失败/
      路径漂移不再造成落盘与 stdout 不一致,残余不一致保守回退
      stdout_only=True。
v3.9(应 msg_375,拒绝类明确错误归因):
  19. 客户端 OSError 补录 errno/异常类型/异常消息,并做独立 Win32
      CreateFileW 探针(同路径同操作,ctypes use_last_error=True)确认拒绝、
      取真实 GetLastError;判定不再接受 outcome=denied+无写入/未泄漏
      作明确归因:须探针确认拒绝、Python 层或 Win32 层出现
      5=ACCESS_DENIED 且互不矛盾、errno/类型/消息齐全。

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
import re
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


def _write_evidence_record(results: dict, path: Path) -> None:
    """逐候选显式原子写(采纳复查方参考实现,64 组故障矩阵 0 缺陷):
    每个候选路径先声明该候选的字段再 tmp+replace 单次提交,无隐藏
    fallback 嵌套;失败清 tmp 并仅再试显式 fallback;全部失败才
    stdout_only=True。落盘内容与实际位置/字段始终一致。"""
    candidates = (path, SUPPORT / ("fallback-" + path.name))
    for candidate in candidates:
        record = dict(results, evidence_written=str(candidate),
                      stdout_only=False)
        temporary = candidate.with_suffix(candidate.suffix + ".tmp")
        try:
            serialized = json.dumps(record, ensure_ascii=False, indent=2)
            temporary.write_text(serialized, encoding="utf-8")
            temporary.replace(candidate)
        except (OSError, TypeError, ValueError) as error:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass
            print("Evidence candidate failed: " + repr(error),
                  file=sys.stderr, flush=True)
            continue
        results["evidence_written"] = str(candidate)
        results["stdout_only"] = False
        return
    results["evidence_written"] = None
    results["stdout_only"] = True


def _write_json(path: Path, obj) -> Path | None:
    """统一原子写入;失败逐级兜底(SUPPORT fallback → stderr),返回实际路径;
    任何失败都不得吞掉调用方的退出码语义(证据缺失由调用方如实处理)。"""
    try:
        text = json.dumps(obj, ensure_ascii=False, indent=2)
    except (TypeError, ValueError) as e:
        print("Evidence serialization failed: " + repr(e),
              file=sys.stderr, flush=True)
        return None
    try:
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(text, encoding="utf-8")
        tmp.replace(path)
        return path
    except OSError:
        try:
            fb = SUPPORT / ("fallback-" + path.name)
            fb.write_text(text, encoding="utf-8")
            return fb
        except OSError as e2:
            print("Evidence write failed (primary+fallback): " + repr(e2),
                  file=sys.stderr, flush=True)
            return None


# ---------------------------------------------------------------- 纯判定谓词

def _denied_attribution_reasons(sb: dict, reasons: list[str]) -> None:
    """拒绝类明确归因(应 msg_375):独立 CreateFileW 探针须确认拒绝,
    Python 层或 Win32 层须出现 5=ACCESS_DENIED 且互不矛盾,
    errno/异常类型/消息须齐全;任一缺失或矛盾追加 UNVERIFIED 理由。"""
    if sb.get("probe_denied") is not True:
        reasons.append("独立 CreateFileW 探针(同路径同操作)未确认拒绝")
    if sb.get("probe_denied") is True and type(sb.get("gle")) is not int:
        reasons.append("探针确认拒绝但 GetLastError 缺失/非整数")
    py, gle = sb.get("winerror"), sb.get("gle")
    if py is None and gle is None:
        reasons.append("无 5=ACCESS_DENIED 归因(Python winerror 与 "
                       "Win32 GetLastError 均缺失)")
    if py is not None and py != ACCESS_DENIED:
        reasons.append(f"Python winerror={py} 非 5=ACCESS_DENIED")
    if gle is not None and gle != ACCESS_DENIED:
        reasons.append(f"Win32 GetLastError={gle} 非 5=ACCESS_DENIED")
    if py is not None and gle is not None and py != gle:
        reasons.append(f"归因矛盾:winerror={py} vs GetLastError={gle}")
    if type(sb.get("errno")) is not int:
        reasons.append("缺少 Python errno 记录(非整数)")
    if not (isinstance(sb.get("exc_type"), str) and sb.get("exc_type")):
        reasons.append("缺少异常类型记录(非字符串/为空)")
    if not (isinstance(sb.get("exc_msg"), str) and sb.get("exc_msg")):
        reasons.append("缺少异常消息记录(非字符串/为空)")


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
        _denied_attribution_reasons(sandbox, reasons)
        if sandbox.get("target_created") is not False:
            reasons.append("拒绝写目标状态未知/非明确未创建")
    if kind == "denied_read":
        if sandbox.get("outcome") != "denied":
            reasons.append("拒绝读结果无法解释")
        _denied_attribution_reasons(sandbox, reasons)
        if sandbox.get("content_leaked") is not False:
            reasons.append("拒绝读泄漏状态未知/非明确未泄漏")
    if reasons:
        return {"verdict": "UNVERIFIED", "reasons": reasons, "contract": CONTRACT}
    return {"verdict": "PASS", "reasons": [], "contract": CONTRACT}


def _negative_regressions() -> dict:
    base_control = {"spawned": True, "rc": 0, "timed_out": False, "succeeded": True}
    base_sandbox = {"spawned": True, "rc": 0, "timed_out": False, "token29": True,
                    "sid_ok": True, "client_ok": True, "outcome": None,
                    "winerror": None, "errno": None, "exc_type": None,
                    "exc_msg": None, "probe_denied": None, "gle": None,
                    "succeeded": None, "hash_ok": None,
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
    _rec("N8 拒绝类归因非 5", _judge_case(
        "denied_write", base_control, _sb(
            outcome="denied", winerror=3, gle=3, probe_denied=True,
            errno=13, exc_type="PermissionError", exc_msg="[Errno 13]",
            target_created=False))["verdict"], "UNVERIFIED")
    _rec("N9 拒绝类结果无法解释", _judge_case(
        "denied_read", base_control, _sb(
            outcome="sent", winerror=None, content_leaked=False,
            target_stable=True))["verdict"], "UNVERIFIED")
    _rec("N10 沙箱未启动", _judge_case(
        "granted_write", base_control, _sb(spawned=False))["verdict"], "UNVERIFIED")
    _rec("N11 拒写目标状态未知", _judge_case(
        "denied_write", base_control, _sb(
            outcome="denied", winerror=ACCESS_DENIED, gle=ACCESS_DENIED,
            probe_denied=True, errno=13, exc_type="PermissionError",
            exc_msg="[Errno 13]", target_created=None))["verdict"], "UNVERIFIED")
    _rec("N12 拒读泄漏状态未知", _judge_case(
        "denied_read", base_control, _sb(
            outcome="denied", winerror=ACCESS_DENIED, gle=ACCESS_DENIED,
            probe_denied=True, errno=13, exc_type="PermissionError",
            exc_msg="[Errno 13]", content_leaked=None,
            target_stable=True))["verdict"], "UNVERIFIED")
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
            outcome="denied", winerror=ACCESS_DENIED, gle=ACCESS_DENIED,
            probe_denied=True, errno=13, exc_type="PermissionError",
            exc_msg="[Errno 13]", content_leaked=False,
            target_stable=False))["verdict"], "UNVERIFIED")
    _rec("N21 拒写探针未确认拒绝", _judge_case(
        "denied_write", base_control, _sb(
            outcome="denied", winerror=ACCESS_DENIED, probe_denied=False,
            gle=None, errno=13, exc_type="PermissionError",
            exc_msg="[Errno 13]", target_created=False))["verdict"], "UNVERIFIED")
    _rec("N22 拒读 GetLastError 缺失", _judge_case(
        "denied_read", base_control, _sb(
            outcome="denied", winerror=ACCESS_DENIED, probe_denied=True,
            gle=None, errno=13, exc_type="PermissionError",
            exc_msg="[Errno 13]", content_leaked=False,
            target_stable=True))["verdict"], "UNVERIFIED")
    _rec("N23 拒写缺 errno 记录", _judge_case(
        "denied_write", base_control, _sb(
            outcome="denied", winerror=None, gle=ACCESS_DENIED,
            probe_denied=True, errno=None, exc_type="PermissionError",
            exc_msg="[Errno 13]", target_created=False))["verdict"], "UNVERIFIED")
    _rec("N24 拒读缺异常类型/消息", _judge_case(
        "denied_read", base_control, _sb(
            outcome="denied", winerror=ACCESS_DENIED, gle=ACCESS_DENIED,
            probe_denied=True, errno=13, exc_type="", exc_msg="",
            content_leaked=False, target_stable=True))["verdict"], "UNVERIFIED")
    _rec("N25 归因矛盾", _judge_case(
        "denied_write", base_control, _sb(
            outcome="denied", winerror=ACCESS_DENIED, gle=3,
            probe_denied=True, errno=13, exc_type="PermissionError",
            exc_msg="[Errno 13]", target_created=False))["verdict"], "UNVERIFIED")
    _rec("N26 无任何 5 归因", _judge_case(
        "denied_write", base_control, _sb(
            outcome="denied", winerror=None, gle=None, probe_denied=False,
            errno=13, exc_type="PermissionError", exc_msg="[Errno 13]",
            target_created=False))["verdict"], "UNVERIFIED")
    _rec("P1 granted_write 基线", _judge_case(
        "granted_write", base_control, _sb(
            succeeded=True, hash_ok=True, sb_pre_exists=False))["verdict"], "PASS")
    _rec("P2 denied_write 基线", _judge_case(
        "denied_write", base_control, _sb(
            outcome="denied", winerror=None, gle=ACCESS_DENIED,
            probe_denied=True, errno=13, exc_type="PermissionError",
            exc_msg="[Errno 13]", target_created=False))["verdict"], "PASS")
    _rec("P3 granted_read 基线", _judge_case(
        "granted_read", base_control, _sb(
            succeeded=True, hash_ok=True, target_stable=True))["verdict"], "PASS")
    _rec("P4 denied_read 基线", _judge_case(
        "denied_read", base_control, _sb(
            outcome="denied", winerror=None, gle=ACCESS_DENIED,
            probe_denied=True, errno=13, exc_type="PermissionError",
            exc_msg="[Errno 13]", content_leaked=False,
            target_stable=True))["verdict"], "PASS")
    _rec("P5 denied_write winerror=5 归因", _judge_case(
        "denied_write", base_control, _sb(
            outcome="denied", winerror=ACCESS_DENIED, gle=ACCESS_DENIED,
            probe_denied=True, errno=13, exc_type="PermissionError",
            exc_msg="[Errno 13]", target_created=False))["verdict"], "PASS")
    _rec("P6 denied_read winerror=5 归因", _judge_case(
        "denied_read", base_control, _sb(
            outcome="denied", winerror=ACCESS_DENIED, gle=ACCESS_DENIED,
            probe_denied=True, errno=13, exc_type="PermissionError",
            exc_msg="[Errno 13]", content_leaked=False,
            target_stable=True))["verdict"], "PASS")
    return {"cases": cases, "all_hold": all(c["holds"] for c in cases)}


# ---------------------------------------------------------------- 客户端代码

_CLIENT = inspect.getsource(net.token_identity) + '''
import ctypes, hashlib, json, sys, time
mode, target, content = sys.argv[1], sys.argv[2], sys.argv[3]
t0 = time.time()
outcome = None
winerror = None
errno_rec = None
exc_type = None
exc_msg = None
probe_denied = None
gle = None
content_hash = None

GENERIC_WRITE = 0x40000000
GENERIC_READ = 0x80000000
CREATE_ALWAYS = 2
OPEN_EXISTING = 3
FILE_ATTRIBUTE_NORMAL = 0x80


def _probe(mode, target):
    """独立 Win32 诊断(应 msg_375):同路径同操作 CreateFileW,
    不依赖 Python 异常映射,拒绝时取真实 GetLastError。"""
    try:
        k32 = ctypes.WinDLL('kernel32', use_last_error=True)
        k32.CreateFileW.argtypes = [ctypes.c_wchar_p, ctypes.c_uint32,
                                    ctypes.c_uint32, ctypes.c_void_p,
                                    ctypes.c_uint32, ctypes.c_uint32,
                                    ctypes.c_void_p]
        k32.CreateFileW.restype = ctypes.c_void_p
        want = GENERIC_WRITE if mode == 'write' else GENERIC_READ
        creation = CREATE_ALWAYS if mode == 'write' else OPEN_EXISTING
        h = k32.CreateFileW(target, want, 0, None, creation,
                            FILE_ATTRIBUTE_NORMAL, None)
        # restype c_void_p 把 INVALID_HANDLE_VALUE(-1) 回包为 2**64-1,
        # NULL(0) 回来是 None;两者都是失败,其余才是有效句柄
        if h is not None and h != ctypes.c_void_p(-1).value:
            k32.CloseHandle(ctypes.c_void_p(h))
            return (False, None)
        return (True, ctypes.get_last_error())
    except Exception:
        return (None, None)

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
    errno_rec = getattr(e, 'errno', None)
    exc_type = type(e).__name__
    exc_msg = str(e)
    probe_denied, gle = _probe(mode, target)

def _sha(p):
    try:
        with open(p, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None

print(json.dumps({'token': token_identity(), 'mode': mode, 'outcome': outcome,
                  'winerror': winerror, 'errno': errno_rec,
                  'exc_type': exc_type, 'exc_msg': exc_msg,
                  'probe_denied': probe_denied, 'gle': gle,
                  'content_hash': content_hash,
                  'client_sha256': _sha(sys.argv[0]), 'exe_sha256': _sha(sys.executable),
                  'site_absent': 'site' not in sys.modules and 'sitecustomize' not in sys.modules,
                  'executable': sys.executable,
                  'elapsed_s': round(time.time() - t0, 3)}), flush=True)
'''


def _parse_client(out: str) -> dict:
    try:
        parsed = json.loads(out.strip().splitlines()[-1]) if out.strip() else {}
    except Exception:  # noqa: BLE001 任何解析异常类(含 RecursionError)都不得
        # 逃逸并跳过击穿事实收集;解析失败一律视为无结构化数据
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _scan_leak(raw_out: str, expected_sha: str) -> bool:
    """泄漏扫描(类型无关):扫描原始输出中**所有** 64 位 hex 哈希,
    任一与哨兵哈希一致即泄漏。不依赖结构化解析(坏 data/坏 token 不掩盖),
    也不被前面出现的非匹配哈希骗过(re.findall 全量扫描)。"""
    if not isinstance(raw_out, str):
        raw_out = repr(raw_out)
    expected = expected_sha.lower()
    return any(c.lower() == expected
               for c in re.findall(r"[0-9a-fA-F]{64}", raw_out))


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
    if sb_pre_exists:
        # 前置状态失败即阻止该操作(不执行任何客户端)
        return ({"verdict": "UNVERIFIED",
                 "reasons": ["沙箱写入目标前置已存在,拒绝执行该操作"],
                 "contract": CONTRACT},
                {"sb_pre_exists": sb_pre_exists, "sb_target": str(tgt_s),
                 "skipped": True})
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
    cmd3 = [str(runtime), "-X", "utf8", str(client), "write", str(tgt3s), n3]
    try:
        s3 = _run_client(cmd3, True, work, env)
    except Exception as e:  # noqa: BLE001 任何异常都不得跳过击穿事实收集
        s3 = {"command": cmd3, "spawned": False, "rc": None, "timed_out": False,
              "data": {}, "raw_out": "", "error": repr(e)}
    # 文件系统事实先收集:击穿判定独立于客户端解析(解析崩溃也不丢 FAIL)
    target_created = tgt3s.exists()
    sb_target_sha = _sha_file(tgt3s)
    if target_created:
        return ({"verdict": "FAIL",
                 "reasons": ["沙箱写入未授权目标成功(隔离击穿)"],
                 "contract": CONTRACT},
                {"control": c3, "sandbox": s3, "ctrl_target": str(tgt3c),
                 "ctrl_sha256": h3, "ctrl_expected_sha256": h3_exp,
                 "sb_target": str(tgt3s), "target_created": True,
                 "sb_target_sha256": sb_target_sha})
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
         "errno": s3["data"].get("errno"),
         "exc_type": s3["data"].get("exc_type"),
         "exc_msg": s3["data"].get("exc_msg"),
         "probe_denied": s3["data"].get("probe_denied"),
         "gle": s3["data"].get("gle"),
         "succeeded": None, "hash_ok": None,
         "target_created": target_created, "content_leaked": None})
    raw = {"control": c3, "sandbox": s3, "ctrl_target": str(tgt3c),
           "ctrl_sha256": h3, "ctrl_expected_sha256": h3_exp,
           "sb_target": str(tgt3s), "target_created": target_created,
           "sb_target_sha256": sb_target_sha,
           "target_created_resample": tgt3s.exists()}
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
    cmd4 = [str(runtime), "-X", "utf8", str(client), "read", str(sentinel),
            "x" * 32]
    try:
        s4 = _run_client(cmd4, True, work, env)
    except Exception as e:  # noqa: BLE001 任何异常都不得跳过泄漏扫描
        s4 = {"command": cmd4, "spawned": False, "rc": None, "timed_out": False,
              "data": {}, "raw_out": "", "error": repr(e)}
    h4_after = _sha_file(sentinel)
    # 泄漏事实先行(FAIL 最高优先,不等待令牌/解析全部成功):
    # 哨兵内容不进沙箱命令行,原始输出中出现与哨兵一致的哈希即泄漏证据;
    # 全量扫描所有 hex 哈希,坏 data/坏 token/前导非匹配哈希均不掩盖
    if _scan_leak(s4.get("raw_out", ""), h4):
        return ({"verdict": "FAIL",
                 "reasons": ["沙箱读到未授权哨兵内容(隔离击穿)"],
                 "contract": CONTRACT},
                {"control": c4, "sandbox": s4, "target": str(sentinel),
                 "expected_sha256": h4, "hash_before": h4_before,
                 "hash_after": h4_after, "content_leaked": True,
                 "leak_source": "client_reported_hash_match"})
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
         "errno": s4["data"].get("errno"),
         "exc_type": s4["data"].get("exc_type"),
         "exc_msg": s4["data"].get("exc_msg"),
         "probe_denied": s4["data"].get("probe_denied"),
         "gle": s4["data"].get("gle"),
         "succeeded": None, "hash_ok": None,
         "target_created": None,
         "content_leaked": s4["data"].get("content_hash") == h4,
         "target_stable": h4_before == h4 and h4_after == h4})
    raw = {"control": c4, "sandbox": s4, "target": str(sentinel),
           "expected_sha256": h4, "hash_before": h4_before,
           "hash_after": h4_after, "content_leaked": False}
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


CORE_MODULES = [
    "src/animtrain/network_isolation.py",
    "tools/network_acceptance.py",
    "tests/test_network_isolation.py",
    "tests/test_network_acceptance.py",
    "src/animtrain/appcontainer.py",
    "src/animtrain/win_job.py",
    "tests/test_appcontainer_lifecycle.py",
    "tests/test_win_job_cleanup.py",
    "src/animtrain/render_gate.py",
    "tools/isolation_acceptance.py",
    "reviews/2026-10-04-acceptance-support/network_acceptance.py"
]


def _post_verify(cfg: dict, manifest: dict, pth_before: str,
                 script_sha_before: str, core_before: dict) -> dict:
    """场景执行后重验:runtime 关键文件/._pth/客户端/本脚本/三个核心模块
    前后一致(核心模块基线快照同时落证据,供与已验收基线绑定)。"""
    checks: dict = {}
    for rel, sha in manifest.items():
        cur = _sha_file(NET_RUNTIME / rel)
        checks[rel] = cur == sha
    pth_now = (NET_RUNTIME / "python313._pth").read_text(
        encoding="utf-8", errors="replace") if (NET_RUNTIME / "python313._pth").exists() else None
    checks["pth"] = pth_now == pth_before
    client = Path(cfg["client_path"])
    checks["client_file"] = _sha_file(client) == cfg["client_sha256"]
    _script_now = _sha_file(Path(__file__))
    checks["script"] = (_script_now is not None
                        and script_sha_before is not None
                        and _script_now == script_sha_before)
    core_now = {}
    for rel, sha_before in core_before.items():
        cur = _sha_file(ROOT / rel)
        core_now[rel] = cur
        checks["core:" + rel] = (sha_before is not None and cur == sha_before)
    return {"all_unchanged": all(checks.values()), "checks": checks,
            "core_modules_before": core_before, "core_modules_after": core_now}


def main() -> int:
    run_id = uuid.uuid4().hex[:12]
    work = SUPPORT / f"file-work-{run_id}"
    denied_dir = SUPPORT / f"file-denied-{run_id}"
    try:
        EVIDENCE.mkdir(exist_ok=True)  # 错误路径依赖,置于 try 外
    except OSError as e:
        # 证据目录不可写:stdout 结构化原始证据 + 受控退出 2,不裸崩
        print(json.dumps({"state": "ERROR", "overall": "UNVERIFIED",
                          "production_gate": "CLOSED", "contract": CONTRACT,
                          "run_id": run_id, "error": repr(e),
                          "note": "证据目录不可写,仅 stdout 输出,无落盘证据"},
                         ensure_ascii=False, indent=2))
        return 2
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
        _write_evidence_record(
            results, EVIDENCE / f"file-accept-error-{run_id}.json")
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
        if script_sha_before is None:
            raise OSError("无法读取本脚本哈希,失败关闭(后核验基线不可为 None)")
        core_before = {rel: _sha_file(ROOT / rel) for rel in CORE_MODULES}
        if any(v is None for v in core_before.values()):
            raise OSError("无法读取核心模块哈希,失败关闭(基线不可为 None)")
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
            runtime_manifest=dict(manifest),  # 关键文件清单直接落证据
            core_manifest_before=dict(core_before),  # 核心模块基线直接落证据
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
                                              script_sha_before, core_before)
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
        # 已确证 FAIL(隔离击穿)不得被任何后置异常降级为 UNVERIFIED
        if results.get("case", {}).get("overall") == "FAIL":
            results.update(state="ERROR", overall="FAIL",
                           error=repr(e), traceback=traceback.format_exc())
            _write_evidence_record(
                results, EVIDENCE / f"file-accept-error-{run_id}.json")
            print(json.dumps(results, ensure_ascii=False, indent=2))
            return 1
        results.update(state="ERROR", overall="UNVERIFIED",
                       error=repr(e), traceback=traceback.format_exc())
        _write_evidence_record(
            results, EVIDENCE / f"file-accept-error-{run_id}.json")
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 2
    _write_evidence_record(
        results, EVIDENCE / f"file-accept-results-{run_id}.json")
    if results["stdout_only"]:
        # 持久证据不可写:契约要求持久证据,PASS 降 UNK;
        # 已确证 FAIL 保留(击穿信号不得被落盘失败掩盖)
        if results["overall"] == "PASS_LOCAL_FILE_ACL":
            results["overall"] = "UNVERIFIED"
        print(json.dumps(results, ensure_ascii=False, indent=2))
        return 1 if results["overall"] == "FAIL" else 2
    print(json.dumps(results, ensure_ascii=False, indent=2))
    all_hold = results["negative_regressions"]["all_hold"]
    ok = (all_hold and results["overall"] == "PASS_LOCAL_FILE_ACL"
          and results["state"] == "COMPLETE")
    if results["overall"] == "FAIL":
        return 1
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main())
