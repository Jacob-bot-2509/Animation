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


def render_check(code: str, python: str | None = None,
                 trusted: bool = False) -> dict:
    """执行隔离渲染:独立子进程跑 manim,超时/退出码/stderr 捕获。

    返回 {ok, status, detail, unverified};环境缺失 → unverified。
    不伪造成功:任何失败/超时都是失败。

    BR6 复验:隔离不完整(fs/network/memory 未实施)时,默认拒绝执行
    不可信代码 —— trusted=False 直接阻断;只有可信固定样例
    (项目内审查过的模板)可以 trusted=True 执行。
    """
    if not trusted:
        return {"ok": False, "status": "unverified",
                "detail": "隔离不完整(fs/network/memory 未实施),"
                          "拒绝执行不可信代码;可信模板须显式 trusted=True(BR6)",
                "unverified": ["render_isolation"]}
    ok_manim, msg = check_manim_available()
    if not ok_manim:
        return {"ok": False, "status": "unverified", "detail": msg,
                "unverified": ["render"]}
    py = python or sys.executable
    # ffmpeg 位于项目约定目录 D:\Settings\ffmpeg\bin(用户 2026-09-30 指定)
    ffmpeg_bin = Path(r"D:\Settings\ffmpeg\bin")
    env = _sanitized_env(str(ffmpeg_bin) if ffmpeg_bin.is_dir() else None)
    with tempfile.TemporaryDirectory() as d:
        scene = Path(d) / "scene.py"
        scene.write_text(code, encoding="utf-8")
        try:
            proc = subprocess.run(
                [py, "-m", "manim", "-ql", "--media_dir", str(Path(d) / "out"),
                 str(scene), "ConceptScene"],
                capture_output=True, text=True, encoding="utf-8",
                errors="replace", timeout=RENDER_TIMEOUT_SEC, env=env,
                # 实测定位(2026-10-01):dvisvgm 3.6 在 cwd 路径含空格时
                # 崩溃(Windows API error 87,退出码 0xFFFFFFFC),manim 内部
                # 调 dvisvgm 继承本进程 cwd。项目根路径带空格,故 cwd 必须
                # 设为无空格的临时目录。scene/media 均在此目录内,不受影响。
                cwd=d)
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
    """BR6/B4 隔离状态如实报告(调用方必须检查后再宣称安全执行)。"""
    return {"shell": False, "timeout_sec": RENDER_TIMEOUT_SEC,
            "env_sanitized": True,      # 密钥类变量剔除(尽力,非完整隔离)
            "fs_isolation": "cwd_only",  # cwd=无空格临时目录(基础文件系统隔离)
            "memory_limit_mb": None,    # 未实施(Windows job objects 待接入)
            "network_isolation": False,  # 未实施
            "note": "当前隔离不完整:cwd 基础隔离 + 环境脱敏 + 禁 shell + 超时;"
                    "memory/network 隔离未实施,不可信生成代码的执行仍被拒绝(B4)"}


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
