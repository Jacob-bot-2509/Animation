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
                   if p.is_file() and p.suffix in WEIGHT_SUFFIXES]
        if not weights:
            return False, (f"模型目录无权重文件({WEIGHT_SUFFIXES})——"
                           "仅配置 JSON 不得宣称就绪")
    return True, f"模型目录齐全: {model_dir}"


def run_preflight(model_dir: Path | None,
                  extra_checks: list[tuple[str, tuple[bool, str]]] | None = None,
                  strict: bool = False) -> dict:
    """执行全部检查。返回 {ok, exit_code, checks}。

    strict=True(R5):模型目录与数据门禁必填,缺失即 FAIL —— 区分"诊断"与
    "训练就绪前严格门禁";任何 SKIPPED/缺失在严格模式下阻断。
    """
    checks: list[dict] = []
    ok, detail = check_gpu()
    checks.append({"check": "gpu", "ok": ok, "detail": detail})
    if model_dir is not None:
        ok2, detail2 = check_model_dir(model_dir, strict=strict)
        checks.append({"check": "model_dir", "ok": ok2, "detail": detail2})
    elif strict:
        checks.append({"check": "model_dir", "ok": False,
                       "detail": "严格模式必须提供 --model 模型目录"})
    for name, (ok3, detail3) in (extra_checks or []):
        checks.append({"check": name, "ok": ok3, "detail": detail3})
    if strict and not extra_checks:
        checks.append({"check": "data_manifest", "ok": False,
                       "detail": "严格模式必须提供 --manifest 数据门禁"})
    ok_all = all(c["ok"] for c in checks)
    return {"ok": ok_all, "exit_code": 0 if ok_all else 1, "checks": checks}
