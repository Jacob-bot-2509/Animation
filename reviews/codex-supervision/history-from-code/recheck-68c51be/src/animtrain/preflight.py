"""preflight 检查(msg_101-6,纯标准库):GPU / 模型文件 / 数据门禁。

任何一项 FAIL → exit 1,禁止后续动作(训练前最后一道门,便于定位)。
不下载模型:只检查已存在文件。
"""
from __future__ import annotations

import subprocess
from pathlib import Path

MODEL_KEY_FILES = ("config.json", "tokenizer_config.json", "tokenizer.json")


def check_gpu() -> tuple[bool, str]:
    """nvidia-smi 可用且至少一块 GPU(C12:查询带超时,挂起即如实失败)。"""
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total",
                              "--format=csv,noheader"], capture_output=True,
                             text=True, encoding="utf-8", timeout=10)
    except FileNotFoundError:
        return False, "nvidia-smi 不存在:未安装 NVIDIA 驱动或不在 PATH"
    except subprocess.TimeoutExpired:
        return False, "nvidia-smi 查询超时(>10s)—— GPU 状态未知,如实失败(C12)"
    if out.returncode != 0:
        return False, f"nvidia-smi 失败: {out.stderr.strip()[:200]}"
    lines = [l for l in out.stdout.splitlines() if l.strip()]
    if not lines:
        return False, "未检测到 GPU"
    return True, "; ".join(lines[:2])


WEIGHT_SUFFIXES = (".safetensors", ".bin", ".gguf", ".pt", ".pth")


def check_model_dir(model_dir: Path, strict: bool = False) -> tuple[bool, str]:
    """模型目录存在且关键文件齐全(不下载,只检查)。

    strict=True: 还必须有实际权重文件 —— 只有空 JSON 无权重的目录
    不得宣称就绪(审查 R5)。
    """
    if not model_dir or not model_dir.is_dir():
        return False, f"模型目录不存在: {model_dir}"
    missing = [f for f in MODEL_KEY_FILES if not (model_dir / f).exists()]
    if missing:
        return False, f"模型目录缺关键文件: {', '.join(missing)}"
    if strict:
        weights = [p for p in model_dir.rglob("*")
                   if p.is_file() and p.suffix in WEIGHT_SUFFIXES and p.stat().st_size > 0]
        if not weights:
            return False, (f"模型目录无**非空**权重文件({WEIGHT_SUFFIXES})——"
                           "仅配置 JSON/0 字节文件不得宣称就绪")
    return True, f"模型目录齐全: {model_dir}"


# B2: ready 模式必需的检查名(缺任一 = 不可生成可执行训练计划)。
# GS2:核心必需门禁统一 —— 库调用方只传部分 extra_checks 也不得绕过
# 资产证据/冻结/校准/执行隔离;缺名即 not ready。
READY_REQUIRED_CHECKS = ("gpu", "model_dir", "data_manifest", "run_snapshot",
                         "asset_evidence", "freeze_gate",
                         "near_dup_calibrated", "exec_isolation")


def check_asset_evidence(manifest_path: Path) -> tuple[bool, str]:
    """B2(GS2 复修):资产验收证据检查 —— 以当前 manifest 的实际样本为准
    逐条验证,自报数字不可作为验收依据。

    证据 asset_evidence.json 必须与 manifest 同目录,含:
      manifest_sha256(绑定当前文件)、n_total_records/n_verified_assets、
      records: {sample_id: {input_sha256(该行核心正文哈希),
                            output_sha256(产物哈希),
                            math: "verified", render: "rendered"}}
    每个实际样本必须有逐条匹配证据;缺失/损坏/未绑定/自报不符 → (False, 原因)。
    """
    import hashlib as _h
    import json as _j

    mp = Path(manifest_path)
    manifest_sha = _h.sha256(mp.read_bytes()).hexdigest()
    ep = mp.parent / "asset_evidence.json"
    if not ep.exists():
        return False, ("资产验收证据缺失(asset_evidence.json 不存在)——"
                       "当前资产未经真实渲染/数学验收,UNVERIFIED 阻断 ready")
    try:
        ev = _j.loads(ep.read_text(encoding="utf-8"))
    except (OSError, _j.JSONDecodeError):
        return False, "资产验收证据文件损坏(非合法 JSON)—— 不得作为验收依据"
    if not isinstance(ev, dict):
        return False, "资产验收证据结构非法(非对象)—— 不得作为验收依据"
    bound = ev.get("manifest_sha256")
    if not isinstance(bound, str) or bound != manifest_sha:
        return False, ("资产验收证据未绑定当前 manifest(哈希不一致)—— "
                       "不得作为验收依据")
    records = ev.get("records")
    if not isinstance(records, dict) or not records:
        return False, ("资产验收证据无逐条记录(records 缺失/空)—— "
                       "自报数字不可作为验收依据(GS2)")
    # 以当前 manifest 的实际样本为准(msg_216:资产输入绑定完整样本行,
    # 不只是题目哈希;产物必须绑定真实 artifact 文件 path/hash/size)
    from .manifest import Manifest  # noqa: PLC0415
    try:
        m = Manifest.load(mp)
    except Exception as exc:  # noqa: BLE001
        return False, f"manifest 无法解析: {exc}"
    actual: dict[str, str] = {}
    for e in m.entries:
        p = mp.parent / e.path
        if p.suffix != ".jsonl" or not p.exists():
            continue
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                obj = _j.loads(line)
            except _j.JSONDecodeError:
                continue
            sid = obj.get("id") if isinstance(obj, dict) else None
            if sid is not None:
                actual[str(sid)] = _h.sha256(
                    line.strip().encode("utf-8")).hexdigest()
    n_total = ev.get("n_total_records")
    if not isinstance(n_total, int) or n_total != len(actual):
        return False, (f"自报总量 {n_total!r} 与实际样本数 {len(actual)} 不符"
                       "—— 不得作为验收依据(GS2)")
    for sid, full_hash in sorted(actual.items()):
        rec = records.get(sid)
        if not isinstance(rec, dict):
            return False, f"样本 {sid} 缺逐条验收证据(GS2)"
        if rec.get("input_sha256") != full_hash:
            return False, f"样本 {sid} 输入哈希与证据不一致(须绑定完整样本行)(GS2)"
        out = rec.get("output")
        if not isinstance(out, dict):
            return False, f"样本 {sid} 缺产物记录(output 对象)(GS2)"
        opath = out.get("path")
        osha = out.get("sha256")
        osize = out.get("size")
        if not isinstance(opath, str) or not opath.strip() \
                or not isinstance(osha, str) or len(osha) != 64 \
                or not isinstance(osize, int) or osize < 0:
            return False, f"样本 {sid} 产物记录非法(需真实 path/64位 sha256/size)(GS2)"
        fp = mp.parent / opath
        if not fp.exists() or not fp.is_file():
            return False, f"样本 {sid} 产物文件不存在: {opath}(GS2)"
        try:
            fsha = _h.sha256(fp.read_bytes()).hexdigest()
        except OSError as exc:
            return False, f"样本 {sid} 产物文件不可读: {exc}(GS2)"
        if fsha != osha or fp.stat().st_size != osize:
            return False, f"样本 {sid} 产物文件哈希/大小与证据不一致(GS2)"
        if rec.get("math") != "verified" or rec.get("render") != "rendered":
            return False, f"样本 {sid} 数学/渲染证据未验证(GS2)"
    if len(records) != len(actual):
        return False, f"证据条数 {len(records)} 与实际样本数 {len(actual)} 不符(GS2)"
    n_verified = ev.get("n_verified_assets")
    if not isinstance(n_verified, int) or n_verified != len(actual):
        return False, f"自报验收数 {n_verified!r} 与实际 {len(actual)} 不符(GS2)"
    return True, f"资产验收证据绑定当前 manifest,逐条覆盖 {len(actual)}/{len(actual)} 条"


def check_exec_isolation() -> tuple[bool, str]:
    """B4:执行隔离验收——network 隔离未实施前,不可执行生成代码,
    ready 必须阻断(与 render_gate._isolation_state 同一口径,不假绿)。"""
    from .render_gate import _isolation_state  # noqa: PLC0415

    st = _isolation_state()
    missing = []
    if st["memory_limit_mb"] is None:
        missing.append("memory")
    if st["network_isolation"] is False:
        missing.append("network")
    if missing:
        return False, ("执行隔离未验收:{} 隔离未实施(现有:cwd 基础隔离+"
                       "环境脱敏+禁 shell+超时+内存上限)——B4 验收前不得"
                       "执行生成代码,UNVERIFIED 阻断 ready"
                       ).format("/".join(missing))
    return True, f"执行隔离已验收: {st}"


def run_preflight(model_dir: Path | None,
                  extra_checks: list[tuple[str, tuple[bool, str]]] | None = None,
                  strict: bool = False,
                  ready: bool = False) -> dict:
    """执行全部检查。返回 {ok, ready, exit_code, checks}。

    strict=True(R5):模型目录与数据门禁必填,缺失即 FAIL —— 区分"诊断"与
    "训练就绪前严格门禁";任何 SKIPPED/缺失在严格模式下阻断。

    ready=True(B2):训练就绪聚合 —— 只有 READY_REQUIRED_CHECKS 全部存在且
    通过、无 UNVERIFIED 项才 ready;任一 FAIL/SKIPPED/缺失/UNVERIFIED
    都阻止生成可执行训练计划。诊断/静态通过不等于 ready。
    """
    checks: list[dict] = []
    ok, detail = check_gpu()
    checks.append({"check": "gpu", "ok": ok, "detail": detail})
    if model_dir is not None:
        ok2, detail2 = check_model_dir(model_dir, strict=strict or ready)
        checks.append({"check": "model_dir", "ok": ok2, "detail": detail2})
    elif strict or ready:
        checks.append({"check": "model_dir", "ok": False,
                       "detail": "严格/ready 模式必须提供 --model 模型目录"})
    for item in (extra_checks or []):
        name, payload = item[0], item[1]
        ok3, detail3 = payload[0], payload[1]
        meta = payload[2] if len(payload) > 2 else {}
        c = {"check": name, "ok": ok3, "detail": detail3}
        if meta.get("unverified"):
            c["unverified"] = meta["unverified"]
        checks.append(c)
    # 复审 R5:data_manifest 必须真实 —— 只有名为 data_manifest 且通过的检查
    # 才算数,任何其他 extra_checks 不得冒充
    dm = [c for c in checks if c["check"] == "data_manifest" and c["ok"]]
    if strict and not dm:
        checks.append({"check": "data_manifest", "ok": False,
                       "detail": "严格模式必须提供真实的数据门禁"
                                 "(extra_checks 中名为 data_manifest 且通过)"})
    ok_all = all(c["ok"] for c in checks)

    ready_ok = False
    if ready:
        by_name = {c["check"]: c for c in checks}
        missing = [n for n in READY_REQUIRED_CHECKS
                   if n not in by_name or not by_name[n]["ok"]]
        # Inspect every result: duplicate names must not hide an earlier failure.
        failed = [c["check"] for c in checks if not c["ok"]]
        unverified = [c["check"] for c in checks if c.get("unverified")]
        if failed:
            checks.append({"check": "ready", "ok": False,
                           "detail": f"FAIL checks block ready: {failed}"})
        elif missing:
            checks.append({"check": "ready", "ok": False,
                           "detail": f"ready 必需检查缺失或未过: {missing}"})
        elif unverified:
            checks.append({"check": "ready", "ok": False,
                           "detail": f"UNVERIFIED 项阻止 ready: {unverified}"
                                     "(渲染/数学未验证不得装 PASS)"})
        else:
            checks.append({"check": "ready", "ok": True,
                           "detail": "全部必需门禁通过,可生成可执行训练计划"})
        ready_ok = checks[-1]["ok"]

    return {"ok": ok_all, "ready": ready_ok, "exit_code":
            0 if (ready_ok if ready else ok_all) else 1, "checks": checks}
