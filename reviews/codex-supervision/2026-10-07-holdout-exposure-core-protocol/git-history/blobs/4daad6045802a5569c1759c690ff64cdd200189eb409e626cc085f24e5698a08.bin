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


def check_model_dir(model_dir: Path) -> tuple[bool, str]:
    """模型目录存在且关键文件齐全(不下载,只检查)。"""
    if not model_dir or not model_dir.is_dir():
        return False, f"模型目录不存在: {model_dir}"
    missing = [f for f in MODEL_KEY_FILES if not (model_dir / f).exists()]
    if missing:
        return False, f"模型目录缺关键文件: {', '.join(missing)}"
    return True, f"模型目录齐全: {model_dir}"


def run_preflight(model_dir: Path | None,
                  extra_checks: list[tuple[str, tuple[bool, str]]] | None = None) -> dict:
    """执行全部检查。返回 {ok, exit_code, checks}。"""
    checks: list[dict] = []
    ok, detail = check_gpu()
    checks.append({"check": "gpu", "ok": ok, "detail": detail})
    if model_dir is not None:
        ok2, detail2 = check_model_dir(model_dir)
        checks.append({"check": "model_dir", "ok": ok2, "detail": detail2})
    for name, (ok3, detail3) in (extra_checks or []):
        checks.append({"check": name, "ok": ok3, "detail": detail3})
    ok_all = all(c["ok"] for c in checks)
    return {"ok": ok_all, "exit_code": 0 if ok_all else 1, "checks": checks}
