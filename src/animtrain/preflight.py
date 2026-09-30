"""preflight 检查(msg_101-6,纯标准库):GPU / 模型文件 / 数据门禁。

任何一项 FAIL → exit 1,禁止后续动作(训练前最后一道门,便于定位)。
不下载模型:只检查已存在文件。
"""
from __future__ import annotations

import subprocess
from pathlib import Path

MODEL_KEY_FILES = ("config.json", "tokenizer_config.json", "tokenizer.json")


def check_gpu() -> tuple[bool, str]:
    """nvidia-smi 可用且至少一块 GPU。"""
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total",
                              "--format=csv,noheader"], capture_output=True,
                             text=True, encoding="utf-8")
    except FileNotFoundError:
        return False, "nvidia-smi 不存在:未安装 NVIDIA 驱动或不在 PATH"
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


# B2: ready 模式必需的检查名(缺任一 = 不可生成可执行训练计划)
READY_REQUIRED_CHECKS = ("gpu", "model_dir", "data_manifest", "run_snapshot")


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
        unverified = [n for n, c in by_name.items()
                      if c.get("unverified")]
        if missing:
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
