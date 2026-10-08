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
RENDER_MEM_MB = 2048  # 目标值;Windows job objects 实现,不可用则如实 None

try:
    from .win_job import WindowsJob  # noqa: F401 B4 内存隔离
except (ImportError, OSError):  # 非 Windows/接口不可用 → 如实不可用
    WindowsJob = None  # type: ignore[assignment]

from . import net_guard  # B4 网络隔离(socket shim + 死代理环境)

# BR6 隔离状态(如实,不宣称):
#   shell=False ✓  超时 ✓  内存限制(job)✓  网络隔离(shim)✓
#   文件系统隔离:cwd_only 基础隔离(非完整,如实标注)
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


def render_check(code: str, python: str | None = None,
                 trusted: bool = False) -> dict:
    """Production transport: AppContainer only, no host-process fallback.

    Generated code remains closed until the exact transport passes joint acceptance.
    Trusted fixed probes use the same transport without pretending to certify it.
    """
    from .sandbox_execution import check_certificate, render_scene
    if not trusted:
        accepted, detail = check_certificate()
        if not accepted:
            return {"ok": False, "status": "unverified", "detail": detail,
                    "unverified": ["render_isolation"]}
    available, detail = check_manim_available()
    if not available:
        return {"ok": False, "status": "unverified", "detail": detail,
                "unverified": ["render"]}
    return render_scene(code, python=python)


# BR2 数学断言契约(复验收紧):
#   verified   化简结果为显式布尔真(Eq/Ne/Lt/.../True 化简成立)
#   disproved  化简结果为显式布尔假(假命题不得标 verified)
#   unproven   化简结果为含自由符号的布尔(无法判定真假,如实)
#   invalid    非布尔断言 —— 数字/符号/裸表达式都不是数学断言
#             (bool(result) 是 Python 真值,不是数学证明,禁止当判定依据)
MATH_EXPR_MAX_LEN = 200
_MATH_FORBIDDEN = ("import", "__", "exec", "eval", "open", "compile",
                   "globals", "locals", "vars", "getattr", "setattr",
                   "delattr", "breakpoint", "input")

# B4:不可信数学输入的白名单命名空间(解析时 __builtins__ 置空,只放
# SymPy 数学对象与关系符;任何属性访问/import/下标在 ast 预检即拒绝)
_MATH_WHITELIST = ("sin", "cos", "tan", "asin", "acos", "atan",
                   "sinh", "cosh", "tanh", "ln", "log", "exp", "sqrt",
                   "Abs", "Rational", "Integer", "Symbol", "pi", "E", "I", "oo",
                   "Eq", "Ne", "Lt", "Le", "Gt", "Ge")


def _safe_parse(expr: str):
    """B4:不可信数学输入的受限解析(防 sympify eval 逃逸)。

    三层防护:敏感模式预检(调用方)→ ast 语法预检(禁 import/属性/下标/
    非白名单调用形式)→ parse_expr 用 __builtins__ 置空 + SymPy 白名单。
    """
    import ast

    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"非合法表达式语法: {exc}") from exc
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            raise ValueError("禁止 import")
        if isinstance(node, ast.Attribute):
            raise ValueError("禁止属性访问(白名单外对象不可用)")
        if isinstance(node, ast.Subscript):
            raise ValueError("禁止下标访问")
        if isinstance(node, ast.Call) and not isinstance(node.func, ast.Name):
            raise ValueError("禁止非白名单调用形式")
    import sympy  # noqa: PLC0415 环境可用才导入
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations  # noqa: PLC0415
    ns = {"__builtins__": {}}
    for name in _MATH_WHITELIST:
        if hasattr(sympy, name):
            ns[name] = getattr(sympy, name)
    return parse_expr(expr, global_dict=ns, local_dict={},
                      transformations=standard_transformations)


def _sanitized_env(extra_path: str | None = None) -> dict:
    """B4:子进程环境脱敏(尽力而为,不是完整隔离)——剔除疑似密钥/凭据的
    变量(含 KEY/TOKEN/SECRET/PASSWORD/CREDENTIAL),保留 PATH/SYSTEMROOT 等
    执行必需项。"""
    import os
    env = dict(os.environ)
    for k in list(env):
        ku = k.upper()
        if any(bad in ku for bad in ("TOKEN", "SECRET", "PASSWORD", "CREDENTIAL",
                                     "APIKEY", "API_KEY", "PRIVATE_KEY")):
            env.pop(k, None)
    if extra_path:
        env["PATH"] = extra_path + os.pathsep + env.get("PATH", "")
    return env


def _isolation_state() -> dict:
    """Report joint acceptance separately from OS transport availability."""
    from .sandbox_execution import check_certificate
    accepted, detail = check_certificate()
    mem = None
    if sys.platform == "win32" and WindowsJob is not None:
        try:
            probe = WindowsJob(16)
            probe.close()
            mem = RENDER_MEM_MB
        except OSError:
            pass
    return {"backend": "windows_appcontainer", "shell": False,
            "timeout_sec": RENDER_TIMEOUT_SEC, "env_sanitized": True,
            "fs_isolation": "private_per_run" if accepted else "shared_explicit_acl",
            "memory_limit_mb": mem, "network_isolation": accepted,
            "python_socket_guard": False, "joint_accepted": accepted,
            "note": detail}


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
        # B4:不可信输入用受限解析(__builtins__ 置空 + 白名单),不用裸 sympify
        parsed = _safe_parse(expr)
        result = sympy.simplify(parsed)
    except Exception as exc:  # noqa: BLE001 表达式非法即失败,如实上报
        return {"ok": False, "status": "invalid",
                "detail": f"数学断言非法或受限: {exc}", "unverified": []}
    # 只有 sympy 布尔类型才是断言;数字/符号/裸表达式一律拒绝。
    # 注意:含自由符号的 relational(如 x>y)的 .is_Boolean 是 None(未知),
    # 不能用 not is_Boolean 判非布尔 —— 用类型判断。
    from sympy.core.relational import Relational  # noqa: PLC0415
    from sympy.logic.boolalg import Boolean as SymBoolean  # noqa: PLC0415
    if result is sympy.S.true:
        return {"ok": True, "status": "verified",
                "detail": f"断言成立: {expr}", "unverified": []}
    if result is sympy.S.false:
        return {"ok": False, "status": "disproved",
                "detail": f"断言不成立: {expr} → False(假命题)", "unverified": []}
    if isinstance(result, (Relational, SymBoolean))             and not isinstance(result, sympy.Symbol):
        # 化简后仍是含自由符号的布尔(如 x > y)。
        # 注意:SymPy 的 Symbol 继承 Boolean(逻辑变量),但裸符号不是
        # 数学断言,排除 —— 否则 'x' 会被当 unproven 而不是 invalid。
        return {"ok": False, "status": "unproven",
                "detail": f"无法判定真假(含自由符号): {expr} → {result}", "unverified": []}
    return {"ok": False, "status": "invalid",
            "detail": f"非布尔断言: {expr} → {result}"
                      "(只接受 Eq/Ne/不等式/布尔表达式;数字不是断言)", "unverified": []}
