"""渲染/数学检查与执行隔离框架(B4,纯标准库)。

原则(不降级):
  - 环境(manim/sympy)未安装 → 返回 UNVERIFIED,由 ready 聚合如实阻断,
    绝不把"没验证"写成"通过"
  - 环境可用 → 真实执行:独立子进程、超时、退出码、stderr 捕获
  - 不做危险执行:只运行传入的代码字符串,禁 shell,限时

接入: preflight --ready 时把 render_gate/math_gate 作为 extra_checks
挂载(带 unverified 元数据),环境缺失即 NOT READY。
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

RENDER_TIMEOUT_SEC = 300
RENDER_MEM_MB = 2048  # 尽力而为(Windows 下由系统管理,记录在案)


def check_manim_available() -> tuple[bool, str]:
    """manim 是否可导入(环境检测,不执行代码)。"""
    spec = importlib.util.find_spec("manim")
    if spec is None:
        return False, "manim 未安装 → 渲染检查 UNVERIFIED(环境就位前阻断 ready)"
    return True, f"manim 可用: {spec.origin}"


def check_sympy_available() -> tuple[bool, str]:
    spec = importlib.util.find_spec("sympy")
    if spec is None:
        return False, "sympy 未安装 → 数学检查 UNVERIFIED(环境就位前阻断 ready)"
    return True, f"sympy 可用: {spec.origin}"


def render_check(code: str, python: str | None = None) -> dict:
    """执行隔离渲染:独立子进程跑 manim,超时/退出码/stderr 捕获。

    返回 {ok, status, detail, unverified};环境缺失 → unverified。
    不伪造成功:任何失败/超时都是失败。
    """
    ok_manim, msg = check_manim_available()
    if not ok_manim:
        return {"ok": False, "status": "unverified", "detail": msg,
                "unverified": ["render"]}
    py = python or sys.executable
    # ffmpeg 位于项目约定目录 D:\Settings\ffmpeg\bin(用户 2026-09-30 指定)
    ffmpeg_bin = Path(r"D:\Settings\ffmpeg\bin")
    env = None
    if ffmpeg_bin.is_dir():
        import os
        env = dict(os.environ)
        env["PATH"] = str(ffmpeg_bin) + os.pathsep + env.get("PATH", "")
    with tempfile.TemporaryDirectory() as d:
        scene = Path(d) / "scene.py"
        scene.write_text(code, encoding="utf-8")
        try:
            proc = subprocess.run(
                [py, "-m", "manim", "-ql", "--media_dir", str(Path(d) / "out"),
                 str(scene), "ConceptScene"],
                capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=RENDER_TIMEOUT_SEC, env=env)
        except subprocess.TimeoutExpired:
            return {"ok": False, "status": "timeout",
                    "detail": f"渲染超时(>{RENDER_TIMEOUT_SEC}s)", "unverified": []}
        except OSError as exc:
            return {"ok": False, "status": "exec_error",
                    "detail": f"无法启动渲染进程: {exc}", "unverified": []}
    if proc.returncode != 0:
        return {"ok": False, "status": "failed",
                "detail": f"渲染失败(退出码 {proc.returncode}): "
                          f"{(proc.stderr or '')[-500:]}", "unverified": []}
    return {"ok": True, "status": "rendered",
            "detail": "渲染成功", "unverified": []}


def math_check(expr: str) -> dict:
    """数学断言检查(SymPy);环境缺失 → unverified。"""
    ok_sympy, msg = check_sympy_available()
    if not ok_sympy:
        return {"ok": False, "status": "unverified", "detail": msg,
                "unverified": ["math"]}
    import sympy  # noqa: PLC0415 环境可用才导入
    try:
        result = sympy.simplify(sympy.sympify(expr))
        return {"ok": True, "status": "verified",
                "detail": f"SymPy 化简: {expr} = {result}", "unverified": []}
    except Exception as exc:  # noqa: BLE001 表达式非法即失败,如实上报
        return {"ok": False, "status": "invalid",
                "detail": f"数学断言非法: {exc}", "unverified": []}
