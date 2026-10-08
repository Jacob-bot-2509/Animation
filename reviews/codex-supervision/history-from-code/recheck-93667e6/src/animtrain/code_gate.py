"""代码门禁(msg_101-4,纯标准库,只读不重写)。

四项检查:
  1. 语法: ast.parse,失败报行号与错误
  2. 危险调用: 黑名单导入/调用(subprocess/os.system/eval/exec/__import__/
     shutil.rmtree 等) —— 安全边界,不是风格检查
  3. 中文-LaTeX: MathTex/Tex/Title 等 LaTeX 家族字符串里含中文 → 报
     (前项目实测教训:TeX 模板无 CJK,编译必失败);Text/MarkupText 走
     Pango 支持中文,不报
  4. API 白名单: 构造调用 Klass(...) 的类名查白名单;未提供白名单 →
     如实跳过(标注 api_skipped,不伪造)

说明:manim 不在本项目环境中,API 真值改由 configs/api_whitelist.json
提供(可配置);前项目"内省运行中的 manim"方式待渲染环境就位后恢复。
"""
from __future__ import annotations

import ast
import json
import re
from pathlib import Path

# 危险黑名单(安全边界;逐项可审计,不搞模糊匹配)
DANGEROUS_IMPORTS = {"subprocess", "socket", "ctypes", "pickle", "marshal"}
DANGEROUS_ATTRS = {"os.system", "os.popen", "os.spawn", "os.remove", "os.rmdir",
                   "os.unlink", "os.rename", "shutil.rmtree", "shutil.copy",
                   "shutil.move"}
DANGEROUS_NAMES = {"eval", "exec", "__import__", "open", "input", "compile",
                   "globals", "locals", "breakpoint"}

# Imported builtins and from-import aliases use the same deny list.
DANGEROUS_QUALIFIED = DANGEROUS_ATTRS | {
    f"builtins.{name}" for name in DANGEROUS_NAMES
}

# LaTeX 家族(中文进这些必失败);Text/MarkupText 走 Pango 支持中文
LATEX_CALLS = {"MathTex", "Tex", "Title", "BulletedList", "DecimalNumber",
               "Integer", "Matrix", "Table"}
CJK_RE = re.compile(r"[一-鿿]")


def check_syntax(code: str) -> list[str]:
    try:
        ast.parse(code)
    except SyntaxError as exc:
        return [f"语法错误 line {exc.lineno or '?'}: {exc.msg}"]
    return []


def check_dangerous(code: str) -> list[str]:
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []  # 语法错误由 check_syntax 报,这里不重复
    out: list[str] = []
    # R6: 收集 import 别名(import os as operating / from os import system as s),
    # 别名调用必须与原名同等检出 —— 只查原名会被别名绕过。
    alias: dict[str, str] = {}  # 局部名 → 完整名
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                root = a.name.split(".")[0]
                local = a.asname or root
                alias[local] = a.name
                if root in DANGEROUS_IMPORTS:
                    out.append(f"危险导入: import {a.name}"
                               f"{' as ' + a.asname if a.asname else ''}"
                               f" (line {node.lineno})")
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            root = mod.split(".")[0]
            for a in node.names:
                local = a.asname or a.name
                alias[local] = f"{mod}.{a.name}"
            if root in DANGEROUS_IMPORTS:
                out.append(f"危险导入: from {mod} import … (line {node.lineno})")
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in DANGEROUS_NAMES:
                    out.append(f"危险调用: {node.func.id}() (line {node.lineno})")
                elif (alias.get(node.func.id, node.func.id) in DANGEROUS_QUALIFIED
                      or alias.get(node.func.id, node.func.id).split(".")[0]
                      in DANGEROUS_IMPORTS):
                    out.append(f"危险调用: 别名 {node.func.id}() → "
                               f"{alias[node.func.id]} (line {node.lineno})")
            elif isinstance(node.func, ast.Attribute):
                chain = _attr_chain(node.func)
                # 别名解析:operating.system → os.system
                first = chain.split(".")[0]
                resolved = alias.get(first, first) + chain[len(first):]
                if resolved in DANGEROUS_QUALIFIED or chain in DANGEROUS_QUALIFIED:
                    out.append(f"危险调用: {chain}"
                               f"{' → ' + resolved if resolved != chain else ''}"
                               f" (line {node.lineno})")
    return out


def _attr_chain(node: ast.AST) -> str:
    parts: list[str] = []
    cur: ast.AST = node
    while isinstance(cur, ast.Attribute):
        parts.append(cur.attr)
        cur = cur.value
    if isinstance(cur, ast.Name):
        parts.append(cur.id)
    return ".".join(reversed(parts))


def check_latex_cjk(code: str) -> list[str]:
    """LaTeX 家族调用里出现中文字符 → 报(前项目教训:编译必失败)。"""
    out: list[str] = []
    for m in re.finditer(r"\b(" + "|".join(sorted(LATEX_CALLS, key=len, reverse=True))
                         + r")\s*\(([^)]*)\)", code):
        call, args = m.group(1), m.group(2)
        if CJK_RE.search(args):
            out.append(f"{call}(…) 参数含中文: LaTeX 无 CJK 支持,编译必失败"
                       f" (line {code[:m.start()].count(chr(10)) + 1});中文请用 Text/MarkupText")
    return out


def check_api(code: str, whitelist: dict | None) -> list[str]:
    """构造调用 Klass(...) 的类名查白名单。whitelist={"allowed":[...]}。

    未提供白名单 → 如实跳过(标注),不伪造。
    """
    if not whitelist or not whitelist.get("allowed"):
        return ["api_skipped: 未提供白名单(如实跳过,不伪造)"]
    allowed = set(whitelist["allowed"])
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []
    out: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in allowed:
                continue
            # 跳过显然是内置/局部变量的名字(白名单只管 manim 类构造)
            if node.func.id in DANGEROUS_NAMES or node.func.id in {"range", "len",
                    "int", "float", "str", "list", "dict", "set", "tuple", "min",
                    "max", "sum", "sorted", "print", "zip", "enumerate", "abs",
                    "round", "isinstance", "getattr", "hasattr", "super"}:
                continue
            out.append(f"API 白名单外构造调用: {node.func.id}() (line {node.lineno})")
    return out


def check_code_all(code: str, whitelist: dict | None = None) -> dict:
    problems = (check_syntax(code) + check_dangerous(code)
                + check_latex_cjk(code) + check_api(code, whitelist))
    # R6: 数学正确性/真实渲染未在本环境验证 —— 如实标注,不得宣称通过
    unverified = ["math_correctness", "render_success"]
    return {"ok": not problems, "problems": problems,
            "unverified": unverified,
            "note": "math/render 未验证(无渲染环境),宣称'通过'仅指语法/安全/白名单层",
            "exit_code": 1 if problems else 0}


def load_whitelist(path: Path | None) -> dict | None:
    if path is None or not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))
