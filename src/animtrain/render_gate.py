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
RENDER_MEM_MB = 2048  # 目标值;当前未实施(Windows 下需 job objects,待接入)

# BR6 隔离状态(如实,不宣称):
#   shell=False ✓  超时 ✓  内存限制 ✗  文件系统隔离 ✗  网络隔离 ✗
# 不可信生成代码的执行须等隔离就位;可信固定样例的渲染可先行。


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
                          f"{(proc.stderr or '')[-500:]}", "unverified": [],
                "isolation": _isolation_state()}
    return {"ok": True, "status": "rendered",
            "detail": "渲染成功", "unverified": [], "isolation": _isolation_state()}


# BR2 数学断言契约:
#   verified   化简后布尔值为真(断言成立)
#   disproved  化简后布尔值为假(断言不成立 —— 假命题不得标 verified)
#   unproven   含自由符号无法判定真假(如实,不冒充验证通过)
#   invalid    非法表达式
# 仅"能解析/能化简"不构成验证通过。
MATH_EXPR_MAX_LEN = 200
_MATH_FORBIDDEN = ("import", "__", "exec", "eval", "open", "compile",
                   "globals", "locals", "vars", "getattr", "setattr",
                   "delattr", "breakpoint", "input")


def _isolation_state() -> dict:
    """BR6 隔离状态如实报告(调用方必须检查后再宣称安全执行)。"""
    return {"shell": False, "timeout_sec": RENDER_TIMEOUT_SEC,
            "memory_limit_mb": None,  # 未实施(Windows job objects 待接入)
            "fs_isolation": False,    # 未实施
            "network_isolation": False,  # 未实施
            "note": "当前隔离不完整:仅禁 shell + 超时;不可信生成代码的"
                    "执行须等 fs/network/memory 隔离就位(BR6)"}


def math_check(expr: str) -> dict:
    """数学断言检查(SymPy);环境缺失 → unverified。"""
    ok_sympy, msg = check_sympy_available()
    if not ok_sympy:
        return {"ok": False, "status": "unverified", "detail": msg,
                "unverified": ["math"]}
    # BR6 防护:sympify 内部走 eval,对输入做长度与敏感词限制(不替代完整隔离)
    if len(expr) > MATH_EXPR_MAX_LEN:
        return {"ok": False, "status": "invalid",
                "detail": f"表达式超长(>{MATH_EXPR_MAX_LEN}),拒绝求值(BR6)", "unverified": []}
    lowered = expr.lower()
    if any(bad in lowered for bad in _MATH_FORBIDDEN):
        return {"ok": False, "status": "invalid",
                "detail": "表达式含受限模式,拒绝求值(BR6)", "unverified": []}
    import sympy  # noqa: PLC0415 环境可用才导入
    try:
        result = sympy.simplify(sympy.sympify(expr, rational=True))
    except Exception as exc:  # noqa: BLE001 表达式非法即失败,如实上报
        return {"ok": False, "status": "invalid",
                "detail": f"数学断言非法: {exc}", "unverified": []}
    try:
        truth = bool(result)
    except TypeError:  # 含自由符号无法判定
        return {"ok": False, "status": "unproven",
                "detail": f"无法判定真假(含自由符号): {expr} → {result}", "unverified": []}
    if truth:
        return {"ok": True, "status": "verified",
                "detail": f"断言成立: {expr} → {result}", "unverified": []}
    return {"ok": False, "status": "disproved",
            "detail": f"断言不成立: {expr} → {result}(假命题)", "unverified": []}
