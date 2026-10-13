#!/usr/bin/env python
"""dataset_audit.py — 候选数据集只读审计(msg: 全量检查)。

审计范围(本次):
  - dataset.md                     手写来源文档(未纳入 git)
  - dataset_{calc,geom,linalg,prob}.json     JSON 数组容器(待转换格式)
  - data/v1/raw/dataset_*.jsonl              正式样本入口格式(候选)

硬约束(审计工具自身):
  - 只读:绝不写入/重命名/去重任何 dataset_*.json 或 data/v1/raw/*.jsonl
  - 不自动改 ID、不自动改写公式内容;所有修复均只作为建议输出
  - 输出:逐条问题(issues.jsonl)、逐条状态(record_status.jsonl)、
          汇总(summary.json)、原始文件哈希(file_hashes.json)

严重度语义(与 DATASET_SCHEMA.md §8 对齐):
  hard       → 硬伤,该条/该文件判 rejected
  quarantine → 候选语义待补齐,判 candidate(≠ 已验收)
  info       → 结构性观察,不影响 clean/candidate/rejected

用法:
  python tools/dataset_audit.py --out reports/dataset_audit_<date>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.near_dup import jaccard, norm_text, shingles  # noqa: E402

# ---------------------------------------------------------------- 契约常量
LICENSE_WHITELIST = {"apache-2.0", "mit", "internal-generated", "cc-by-sa-4.0",
                     "Internal-Research-Use-Only"}
INTERNAL_LICENSE = "Internal-Research-Use-Only"
REQUIRED_INTAKE = ["id", "category", "sub_category", "problem", "solution",
                   "scene_spec", "source", "license"]
OPTIONAL_META = ["function_family", "visual_style", "efficiency_tags"]
FORMAL_FIELDS = set(REQUIRED_INTAKE) | {"answer"} | set(OPTIONAL_META)
ANIMATION_FIELDS = ["code", "render_status", "code_sha256"]

CATEGORY_BY_PREFIX = {
    "calc": "数学分析",
    "geom": "解析几何",
    "linalg": "高等代数",
    "prob": "概率论",
}

CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
FULLWIDTH_RE = re.compile(r"[\u3000-\u303f\uff01-\uff5e\ufe30-\ufe4f]")
MATH_SPAN_RE = re.compile(r"(?<!\\)\$([^$]*)(?<!\\)\$")
PLACEHOLDER_RE = re.compile(r"\b(?:TODO|TBD|FIXME|XXX|待补|待定|略|占位)\b", re.I)
EXPECTED_TRAIN_MARKERS = ["已验收", "验收通过", "训练就绪", "READY", "training-ready",
                          "approved for training", "已批准训练", "verified"]

RENDER_RISK_PATTERNS = [
    (re.compile(r"\+infty"), r"缺少反斜杠:应写作 +\infty"),
    (re.compile(r"(?<!\\)\b(?:arctan|arcsin|arccos)\b"), r"裸函数名:应写作 \arctan/\arcsin/\arccos"),
    (re.compile(r"(?<!\\)\blim(?=\s*[_{])"), r"裸函数名:应写作 \lim"),
    (re.compile(r"(?<!\\)\b(?:sin|cos|tan|ln|log)(?![a-zA-Z])"), r"裸函数名:应写作 \sin/\cos/\tan/\ln/\log"),
    (re.compile(r"(?<!\\)\binfty\b"), r"应写作 \infty"),
]
# 未加花括号的多位数字上下标(如 x^12 会渲染成 x^1 2);单字母后接字母
# (A^TAQ、u_1v_2)是 TeX 正常写法,不算风险,故只查多位数字。
UNBRACED_MULTIDIGIT_RE = re.compile(r"[_^]\d{2,}")
# 同一层重复出现同类上下标(如 x_i_j、e^x^2);先去掉 {...} 分组再判断,
# 避免把合法的 x_0^b(先下标后上标)误判为双重上下标。
WEAK_ANSWER_RE = re.compile(r"见(?:上述)?解答|详见解答|见解答过程|见下文|同上|略$")
# `A = X = X = B` 型重复等式(实测: \lim...\arctan b = \arctan b = \pi/2)
DUP_EQ_RE = re.compile(r"([^=]{2,40}?)\s*=\s*\1\s*=")
CJK_NUM = {"一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7,
           "八": 8, "九": 9, "十": 10}


# ---------------------------------------------------------------- 基础工具
def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _dup_key_hook(pairs):
    """记录重复键(JSON 规范允许但会静默丢数据)。"""
    seen, dup = set(), []
    out = {}
    for k, v in pairs:
        if k in seen:
            dup.append(k)
        seen.add(k)
        out[k] = v
    if dup:
        out["__dup_keys__"] = dup
    return out


def norm_latex(s: str) -> str:
    return re.sub(r"[\s$\\{}]", "", (s or "")).lower()


def math_spans(text: str) -> list[str]:
    return MATH_SPAN_RE.findall(text or "")


def _trunc(s, n=200):
    s = "" if s is None else str(s)
    s = s.replace("\n", "\\n")
    return s if len(s) <= n else s[: n - 1] + "…"


def walk_strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, list):
        for x in obj:
            yield from walk_strings(x)
    elif isinstance(obj, dict):
        for v in obj.values():
            yield from walk_strings(v)


def find_double_subsup(span: str) -> str | None:
    """检测同一层重复上/下标(如 x_i_j、e^x^2)。

    去掉 {...} 分组后,只允许两个标记之间是纯字母数字(排除 1-x^2-y^2 这类
    分属不同项的 ^);注意 u_1v_2 在 TeX 中合法,故此检查定位为风格/消歧提示。
    """
    s = span
    for _ in range(8):
        s2 = re.sub(r"\{[^{}]*\}", "", s)
        if s2 == s:
            break
        s = s2
    m = re.search(r"_[A-Za-z0-9]*_", s) or re.search(r"\^[A-Za-z0-9]*\^", s)
    return m.group(0) if m else None


def math_atoms(text: str) -> list[str]:
    """取文本中的数学式并归一化(去空白/$/反斜杠/花括号),用于一致性比对。"""
    return [norm_latex(x) for x in math_spans(text) if norm_latex(x)]


# ---------------------------------------------------------------- 文件加载
def load_file(path: Path, *, allow_utf8_bom: bool = False) -> dict:
    """只读加载,保留源行号/索引。返回记录与结构诊断。"""
    raw = path.read_bytes()
    info = {
        "path": str(path.relative_to(ROOT)).replace("\\", "/"),
        "abs_path": str(path),
        "sha256": sha256_bytes(raw),
        "size": len(raw),
        "mtime": datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
                          .isoformat(timespec="seconds"),
        "format": "unknown",
        "records": [],
        "structure_issues": [],
        "dup_keys": [],
        "blank_lines": [],
        "decode_error": None,
        "line_count": 0,
    }
    if raw.startswith(b"\xef\xbb\xbf"):
        info["structure_issues"].append("BOM:文件带 UTF-8 BOM")
    try:
        text = raw.decode("utf-8-sig" if allow_utf8_bom else "utf-8")
    except UnicodeDecodeError as exc:
        info["decode_error"] = str(exc)
        info["structure_issues"].append(f"非 UTF-8 可解码:{exc}")
        return info
    lines = text.splitlines()
    info["line_count"] = len(lines)
    if not text.endswith("\n"):
        info["structure_issues"].append("末尾缺少换行符(final newline)")
    if text.endswith("\n\n"):
        info["structure_issues"].append("文件末尾存在多余空行")
    if "\r" in text:
        info["structure_issues"].append("含 CR(CRLF 行尾)")

    stripped = text.lstrip()
    is_array = path.suffix == ".json" and stripped.startswith("[")
    if is_array:
        info["format"] = "json-array"
        try:
            data = json.loads(text, object_pairs_hook=_dup_key_hook)
        except json.JSONDecodeError as exc:
            info["structure_issues"].append(f"JSON 解析失败:{exc}")
            return info
        if not isinstance(data, list):
            info["structure_issues"].append(f"顶层不是数组({type(data).__name__})")
            return info
        for i, rec in enumerate(data):
            if isinstance(rec, dict) and "__dup_keys__" in rec:
                info["dup_keys"].append({"index": i + 1, "keys": rec.pop("__dup_keys__")})
            info["records"].append({"locator": f"record[{i + 1}]", "line": None,
                                    "index": i + 1, "record": rec, "raw": None})
        return info

    info["format"] = "jsonl" if path.suffix == ".jsonl" else "text"
    if path.suffix != ".jsonl":
        # 非 .jsonl 的文件:先看是否逐行 JSON 对象(来源手稿可能已是 JSONL 文本);
        # 是则按样本解析(便于与交付池做逐条内容比对),否则只做正则体检。
        objs = []
        linewise = True
        for i, ln in enumerate(lines, 1):
            if not ln.strip():
                info["blank_lines"].append(i)
                continue
            try:
                o = json.loads(ln, object_pairs_hook=_dup_key_hook)
            except json.JSONDecodeError:
                linewise = False
                break
            if not isinstance(o, dict):
                linewise = False
                break
            if "__dup_keys__" in o:
                info["dup_keys"].append({"line": i, "keys": o.pop("__dup_keys__")})
            objs.append({"locator": f"line {i}", "line": i, "index": None,
                         "record": o, "raw": ln})
        if linewise and objs:
            info["format"] = "jsonl-text(doc)"
            info["records"] = objs
            return info
        info["format"] = "source-doc"
        info["records"] = [{"locator": f"line {i}", "line": i, "index": i,
                            "record": None, "raw": ln}
                           for i, ln in enumerate(lines, 1)]
        return info

    for i, ln in enumerate(lines, 1):
        if not ln.strip():
            info["blank_lines"].append(i)
            continue
        try:
            rec = json.loads(ln, object_pairs_hook=_dup_key_hook)
        except json.JSONDecodeError as exc:
            info["records"].append({"locator": f"line {i}", "line": i, "index": None,
                                    "record": None, "raw": ln,
                                    "parse_error": str(exc)})
            continue
        if isinstance(rec, dict) and "__dup_keys__" in rec:
            info["dup_keys"].append({"line": i, "keys": rec.pop("__dup_keys__")})
        info["records"].append({"locator": f"line {i}", "line": i, "index": None,
                                "record": rec, "raw": ln})
    return info


# ---------------------------------------------------------------- 记录检查
class Audit:
    def __init__(self):
        self.issues = []
        self._n = 0

    def add(self, severity, code, file, locator, message, *, rid=None, field=None,
            evidence=None, action=None):
        self._n += 1
        self.issues.append({
            "issue_id": f"{self._n:04d}",
            "severity": severity,
            "code": code,
            "file": file,
            "locator": locator,
            "id": rid,
            "field": field,
            "message": message,
            "evidence": _trunc(evidence),
            "suggested_action": action or "仅报告:由用户确认后人工修改,工具不改写",
        })


def check_structure(audit: Audit, info: dict) -> None:
    f = info["path"]
    for msg in info["structure_issues"]:
        sev = "hard" if ("解析失败" in msg or "非 UTF-8" in msg) else "info"
        audit.add(sev, "S001" if sev == "hard" else "S002", f, "document", msg)
    for b in info["blank_lines"]:
        if info["format"] == "jsonl":
            audit.add("info", "S003", f, f"line {b}",
                      "空行(JSONL 允许,但样本行计数需注意)")
    for d in info["dup_keys"]:
        loc = d.get("line") and f"line {d['line']}" or f"record[{d['index']}]"
        audit.add("hard", "S004", f, loc,
                  f"JSON 对象内重复键 {d['keys']}:解析时后者覆盖前者,数据静默丢失",
                  evidence=d["keys"])
    if info["format"] == "json-array":
        audit.add("hard", "S005", f, "document",
                  "整文件 JSON 数组不是合法样本入口(DATASET_SCHEMA §1,硬伤);"
                  "须 convert 为 JSONL 后才能作为 train/eval/test 样本",
                  action="按契约拒绝作为样本入口;原文件保留,不改写")

    records = info["records"]
    ids = [r["record"].get("id") for r in records
           if isinstance(r.get("record"), dict)]
    for r in records:
        if r.get("parse_error"):
            audit.add("hard", "S006", f, r["locator"],
                      f"JSON 解析失败:{r['parse_error']}", evidence=r.get("raw"))
        elif r.get("record") is not None and not isinstance(r["record"], dict):
            audit.add("hard", "S007", f, r["locator"],
                      f"样本不是 JSON 对象({type(r['record']).__name__})",
                      evidence=r.get("raw"))


def check_fields(audit: Audit, info: dict, r: dict, rid: str) -> dict:
    rec = r["record"]
    f, loc = info["path"], r["locator"]
    out = {"missing_required": [], "quarantine": []}
    for field in REQUIRED_INTAKE:
        if field not in rec:
            out["missing_required"].append(field)
            audit.add("hard", "F001", f, loc, f"缺关键字段 {field}(id={rid})",
                      rid=rid, field=field)
        elif rec[field] is None or (isinstance(rec[field], str) and not rec[field].strip()) \
                or (isinstance(rec[field], (list, dict)) and len(rec[field]) == 0):
            out["missing_required"].append(field)
            audit.add("hard", "F002", f, loc,
                      f"关键字段 {field} 为空(id={rid})", rid=rid, field=field)
    if "answer" not in rec or rec.get("answer") in (None, ""):
        out["quarantine"].append("answer")
        audit.add("quarantine", "F003", f, loc,
                  f"缺 answer:判分字段待补齐(id={rid})", rid=rid, field="answer")
    for field in OPTIONAL_META:
        v = rec.get(field)
        if v is None or (isinstance(v, str) and not v.strip()) or \
                (isinstance(v, (list, dict)) and len(v) == 0):
            out["quarantine"].append(field)
            audit.add("quarantine", "F004", f, loc,
                      f"可选元数据 {field} 缺失/为空(candidate 语义,id={rid})",
                      rid=rid, field=field)
    for field in ("id", "category", "sub_category", "problem", "solution", "source",
                  "license"):
        v = rec.get(field)
        if v is not None and not isinstance(v, (str, int)):
            audit.add("hard", "F005", f, loc,
                      f"字段 {field} 类型异常:{type(v).__name__}(id={rid})",
                      rid=rid, field=field, evidence=v)
    if isinstance(rec.get("id"), bool):
        audit.add("hard", "F006", f, loc,
                  f"id 是 bool 而非 str/int(id={rid})", rid=rid, field="id")
    spec = rec.get("scene_spec")
    if spec is not None and not isinstance(spec, dict):
        audit.add("hard", "F007", f, loc,
                  f"scene_spec 不是对象({type(spec).__name__},id={rid})",
                  rid=rid, field="scene_spec")
    extra = [k for k in rec if k not in FORMAL_FIELDS]
    if extra:
        audit.add("quarantine", "F008", f, loc,
                  f"非正式字段 {extra}(id={rid},正式字段见 DATASET_SCHEMA §2)",
                  rid=rid, evidence=extra)
    return out


def check_id(audit: Audit, info: dict, r: dict, rid: str) -> None:
    rec = r["record"]
    f, loc = info["path"], r["locator"]
    m = re.match(r"^([a-z]+)-", str(rid))
    if not m:
        audit.add("info", "I001", f, loc, f"id 不符合 <prefix>-<name>-<num> 约定:{rid}",
                  rid=rid, field="id")
        return
    prefix = m.group(1)
    expected = CATEGORY_BY_PREFIX.get(prefix)
    cat = rec.get("category")
    if expected and cat and cat != expected:
        audit.add("hard", "I002", f, loc,
                  f"id 前缀 {prefix} 与 category={cat} 不一致(id={rid})",
                  rid=rid, field="id")
        return
    filename_prefix = Path(info["path"]).stem.replace("dataset_", "")
    if prefix != filename_prefix:
        audit.add("hard", "I003", f, loc,
                  f"id 前缀 {prefix} 与文件名前缀 {filename_prefix} 不一致(id={rid})",
                  rid=rid, field="id")


def check_consistency(audit: Audit, info: dict, r: dict, rid: str) -> None:
    rec = r["record"]
    f, loc = info["path"], r["locator"]
    problem = str(rec.get("problem") or "")
    solution = str(rec.get("solution") or "")
    answer = str(rec.get("answer") or "")

    for field, val in (("problem", problem), ("solution", solution), ("answer", answer)):
        if PLACEHOLDER_RE.search(val):
            audit.add("hard", "C001", f, loc,
                      f"{field} 含占位符文本(id={rid})", rid=rid, field=field,
                      evidence=val)
    if problem and problem == answer:
        audit.add("hard", "C002", f, loc, f"answer 与 problem 完全相同(id={rid})",
                  rid=rid, field="answer")
    if solution and answer and norm_latex(solution) == norm_latex(answer):
        audit.add("quarantine", "C003", f, loc,
                  f"solution 与 answer 完全相同(无推导过程,id={rid})",
                  rid=rid, field="solution")
    if problem and len(norm_text(problem)) < 8:
        audit.add("quarantine", "C004", f, loc,
                  f"problem 过短({len(norm_text(problem))} 字符,id={rid})",
                  rid=rid, field="problem")
    if solution and len(norm_text(solution)) < 12:
        audit.add("quarantine", "C005", f, loc,
                  f"solution 过短({len(norm_text(solution))} 字符,id={rid})",
                  rid=rid, field="solution")
    if problem and not re.search(r"[?？。.]\s*$", problem):
        audit.add("info", "C006", f, loc,
                  f"problem 结尾无问句/句号标记(id={rid})", rid=rid, field="problem")

    if answer and WEAK_ANSWER_RE.search(answer):
        audit.add("quarantine", "C009", f, loc,
                  f"answer 非自包含终答(指向解答,无法独立判分,id={rid})",
                  rid=rid, field="answer", evidence=answer,
                  action="补齐可判分终答后再进入验收")

    # answer 与 solution 的一致性(两层判据):
    #  a) answer 里的数学式应出现在 solution 中 → 一致
    #  b) answer 无数学式或数学式缺失时,回退到 5-gram 相似度,仅低相似度才提示人工
    if answer and solution:
        a_norm, s_norm = norm_latex(answer), norm_latex(solution)
        atoms = math_atoms(answer)
        atoms_in_sol = [a for a in atoms if a in s_norm]
        if a_norm and a_norm in s_norm:
            pass                                    # 逐字一致,无问题
        elif atoms and len(atoms_in_sol) == len(atoms):
            audit.add("info", "C007", f, loc,
                      f"answer 未逐字出现在 solution,但其数学式全部可在 solution 中"
                      f"找到(等价表述,id={rid})", rid=rid, field="answer")
        elif atoms and atoms_in_sol:
            missing = [a for a in atoms if a not in s_norm]
            audit.add("info", "C007", f, loc,
                      f"answer 的部分数学式未逐字出现在 solution:{missing}"
                      f"(字符串启发式,通常为等价表述;需人工核对,id={rid})",
                      rid=rid, field="answer",
                      evidence=f"answer={_trunc(answer,70)}")
        elif not atoms and jaccard(shingles(answer), shingles(solution)) >= 0.1:
            pass                                    # 纯文字结论,与解答用词相符
        else:
            sim = jaccard(shingles(answer), shingles(solution))
            audit.add("info", "C007", f, loc,
                      f"answer 与 solution 无明显文本/数学式重合"
                      f"(5-gram 相似度 {sim:.2f},纯文字结论属正常,id={rid})",
                      rid=rid, field="answer",
                      evidence=f"answer={_trunc(answer,60)} | solution 结尾="
                               f"{_trunc(solution[-80:],80)}")

    # 数学式内部重复等号(P0 实测: \lim ... \arctan b = \arctan b = \pi/2)
    def _dup_equal(field: str, val: str) -> None:
        for span in math_spans(val):
            m = DUP_EQ_RE.search(span)
            if m:
                audit.add("quarantine", "C008", f, loc,
                          f"{field} 公式出现重复等式 '{m.group(1).strip()} = "
                          f"{m.group(1).strip()}'(疑似笔误,id={rid})",
                          rid=rid, field=field, evidence=f"${_trunc(span,80)}$")

    for field, val in (("problem", problem), ("solution", solution), ("answer", answer)):
        _dup_equal(field, val)
    spec = rec.get("scene_spec")
    if isinstance(spec, dict):
        for s in walk_strings(spec):
            _dup_equal("scene_spec", s)


def check_latex(audit: Audit, info: dict, r: dict, rid: str) -> None:
    rec = r["record"]
    f, loc = info["path"], r["locator"]
    texts = [("problem", rec.get("problem")), ("solution", rec.get("solution")),
             ("answer", rec.get("answer"))]
    spec = rec.get("scene_spec")
    if isinstance(spec, dict):
        texts.append(("scene_spec", json.dumps(spec, ensure_ascii=False)))
    for field, val in texts:
        if not isinstance(val, str) or not val:
            continue
        if "$$" in val:
            audit.add("quarantine", "L000", f, loc,
                      f"{field} 使用 $$ 显示公式(数据契约按行内 $...$ 设计,id={rid})",
                      rid=rid, field=field)
        n_dollar = len(re.findall(r"(?<!\\)\$", val))
        if n_dollar % 2:
            audit.add("hard", "L001", f, loc,
                      f"{field} 美元符号不配对({n_dollar} 个,id={rid}):公式未闭合",
                      rid=rid, field=field, evidence=val)
        for span in math_spans(val):
            ev = f"${_trunc(span, 90)}$"
            if CJK_RE.search(span):
                audit.add("hard", "L002", f, loc,
                          f"{field} 数学公式内出现中文(TeX 无 CJK,渲染必失败,id={rid})",
                          rid=rid, field=field, evidence=ev)
            if FULLWIDTH_RE.search(span):
                audit.add("hard", "L003", f, loc,
                          f"{field} 公式内含全角标点/全角字符(id={rid});"
                          f"现有 CJK 正则 [一-鿿] 检测不到此类字符",
                          rid=rid, field=field, evidence=ev)
            for pat, hint in RENDER_RISK_PATTERNS:
                if pat.search(span):
                    audit.add("quarantine", "L004", f, loc,
                              f"{field} 疑似漏反斜杠({hint},id={rid});只报不改",
                              rid=rid, field=field, evidence=ev)
                    break
            if span.count("{") != span.count("}"):
                audit.add("hard", "L005", f, loc,
                          f"{field} 公式花括号不配对(id={rid})",
                          rid=rid, field=field, evidence=ev)
            if len(re.findall(r"\\left(?![A-Za-z])", span)) != len(re.findall(r"\\right(?![A-Za-z])", span)):
                audit.add("quarantine", "L006", f, loc,
                          f"{field} \\left/\\right 不配对(id={rid})",
                          rid=rid, field=field, evidence=ev)
            dbl = find_double_subsup(span)
            if dbl:
                audit.add("info", "L007", f, loc,
                          f"{field} 同一层重复上下标标记 '{dbl}':若属同一原子的双重"
                          f"上下标会报错,若为相邻原子(如 u_1v_2)合法;建议加花括号消歧"
                          f"(id={rid})", rid=rid, field=field, evidence=ev)
            for m in UNBRACED_MULTIDIGIT_RE.finditer(span):
                audit.add("quarantine", "L008", f, loc,
                          f"{field} 未加花括号的多位数字上下标 '{m.group(0)}'"
                          f"(渲染为单字符+残余数字,id={rid})", rid=rid, field=field,
                          evidence=ev)
                break
            if re.search(r"\\(?:frac|dfrac|tfrac)\s*[^{]", span):
                audit.add("quarantine", "L009", f, loc,
                          f"{field} \\frac 未使用花括号参数(id={rid})",
                          rid=rid, field=field, evidence=ev)
        # 公式外的裸下划线/花括号(文本模式 TeX 会报错风险);scene_spec 是
        # 自然语言规格(y=x^3 之类),不计入
        if field != "scene_spec":
            outside = MATH_SPAN_RE.sub("", val)
            outside = re.sub(r"\\[a-zA-Z]+|\\.", "", outside)
            if re.search(r"[_^]", outside):
                audit.add("info", "L010", f, loc,
                          f"{field} 公式外出现 _ 或 ^(若作为 MathTex 渲染会报错,"
                          f"作为纯文本无害,id={rid})",
                          rid=rid, field=field, evidence=_trunc(outside, 80))


def check_scene_spec(audit: Audit, info: dict, r: dict, rid: str) -> dict:
    rec = r["record"]
    f, loc = info["path"], r["locator"]
    spec = rec.get("scene_spec")
    res = {"objects": 0, "steps": 0, "verified": False}
    if not isinstance(spec, dict):
        return res
    objs, steps = spec.get("objects"), spec.get("steps")
    if not isinstance(objs, list) or not objs:
        audit.add("hard", "A001", f, loc,
                  f"scene_spec.objects 缺失或非非空列表(id={rid})",
                  rid=rid, field="scene_spec.objects", evidence=objs)
    if not isinstance(steps, list) or not steps:
        audit.add("hard", "A002", f, loc,
                  f"scene_spec.steps 缺失或非非空列表(id={rid})",
                  rid=rid, field="scene_spec.steps", evidence=steps)
    if isinstance(objs, list):
        res["objects"] = len(objs)
        for i, o in enumerate(objs, 1):
            if not isinstance(o, str) or not o.strip():
                audit.add("hard", "A003", f, loc,
                          f"objects[{i}] 不是非空字符串(类型 {type(o).__name__},id={rid})",
                          rid=rid, field="scene_spec.objects", evidence=o)
    if isinstance(steps, list):
        res["steps"] = len(steps)
        for i, s in enumerate(steps, 1):
            if not isinstance(s, str) or not s.strip():
                audit.add("hard", "A004", f, loc,
                          f"steps[{i}] 不是非空字符串(类型 {type(s).__name__},id={rid})",
                          rid=rid, field="scene_spec.steps", evidence=s)
        # 步序编号一致性
        nums = []
        for s in steps:
            if not isinstance(s, str):
                continue
            m = re.match(r"^\s*第\s*([一二三四五六七八九十\d]+)\s*步", s)
            nums.append(CJK_NUM.get(m.group(1), int(m.group(1)) if m and
                        m.group(1).isdigit() else None) if m else None)
        if any(n is None for n in nums):
            audit.add("quarantine", "A005", f, loc,
                      f"steps 存在未以“第N步”开头的步骤(id={rid})",
                      rid=rid, field="scene_spec.steps",
                      evidence=[s for s, n in zip(steps, nums) if n is None][:2])
        elif nums != list(range(1, len(nums) + 1)):
            audit.add("quarantine", "A006", f, loc,
                      f"steps 步序编号不连续/乱序:{nums}(id={rid})",
                      rid=rid, field="scene_spec.steps")
    extra_spec = [k for k in spec if k not in
                  ("objects", "steps", "code", "render_status", "code_sha256")]
    if extra_spec:
        audit.add("quarantine", "A007", f, loc,
                  f"scene_spec 含非契约键 {extra_spec}(id={rid})",
                  rid=rid, field="scene_spec")
    present = [k for k in ANIMATION_FIELDS if k in spec and spec[k] not in (None, "")]
    missing = [k for k in ANIMATION_FIELDS if k not in present]
    if missing:
        audit.add("quarantine", "A008", f, loc,
                  f"动画未验证:scene_spec 缺 {missing}(DATASET_SCHEMA §7:"
                  f"状态只能标 candidate,不得宣称动画已验证,id={rid})",
                  rid=rid, field="scene_spec",
                  action="保持 candidate;通过 render_gate 后再登记 code/render_status/code_sha256")
    else:
        res["verified"] = True
        if str(spec.get("render_status")) != "verified":
            audit.add("quarantine", "A009", f, loc,
                      f"render_status={spec.get('render_status')!r} 非 verified(id={rid})",
                      rid=rid, field="scene_spec.render_status")
    return res


def check_source_license(audit: Audit, info: dict, r: dict, rid: str) -> dict:
    rec = r["record"]
    f, loc = info["path"], r["locator"]
    lic, src = rec.get("license"), rec.get("source")
    out = {"license": lic, "source": src}
    if isinstance(lic, str):
        if lic.strip() not in LICENSE_WHITELIST:
            audit.add("hard", "P001", f, loc,
                      f"license={lic!r} 不在白名单(白名单:{sorted(LICENSE_WHITELIST)},id={rid})",
                      rid=rid, field="license")
        elif lic.strip() == INTERNAL_LICENSE:
            audit.add("quarantine", "P002", f, loc,
                      f"license={lic}:仅限内部研究使用,不是公开再分发许可证;"
                      f"公开/训练转正前必须换为真实许可证(id={rid})",
                      rid=rid, field="license",
                      action="保留候选状态;补充真实授权证据后再转正")
    if src == "self-authored":
        audit.add("info", "P003", f, loc,
                  f"source=self-authored(无外部来源证据文件,id={rid})",
                  rid=rid, field="source")
    return out


# ---------------------------------------------------------------- 汇总检查
def check_pool_ids(audit: Audit, pool: list[tuple[dict, dict]]) -> dict:
    by_id = defaultdict(list)
    by_canon = defaultdict(list)
    result = {"duplicate_id_same_content": [], "duplicate_id_conflict": []}
    for info, r in pool:
        rec = r["record"]
        rid = str(rec.get("id"))
        by_id[rid].append((info, r))
        by_canon[json.dumps(rec, sort_keys=True, ensure_ascii=False)].append((info, r))
    for rid, items in sorted(by_id.items()):
        if len(items) < 2:
            continue
        canon = {json.dumps(x[1]["record"], sort_keys=True, ensure_ascii=False)
                 for x in items}
        locs = ", ".join(f"{x[0]['path']}:{x[1]['locator']}" for x in items)
        if len(canon) == 1:
            result["duplicate_id_same_content"].append({"id": rid, "locs": locs})
            for x in items:
                audit.add("hard", "I010", x[0]["path"], x[1]["locator"],
                          f"全局同 ID 同内容整条重复:{locs};只报告,不静默去重/改名",
                          rid=rid, action="由用户确认后人工去重")
        else:
            result["duplicate_id_conflict"].append({"id": rid, "locs": locs})
            for x in items:
                audit.add("hard", "I011", x[0]["path"], x[1]["locator"],
                          f"全局同 ID 不同内容冲突:{locs};只报告,不静默改名",
                          rid=rid, action="由用户确认后人工改 ID")
    for canon, items in by_canon.items():
        if len(items) > 1:
            locs = ", ".join(f"{x[0]['path']}:{x[1]['locator']}" for x in items)
            idd = str(items[0][1]["record"].get("id"))
            audit.add("hard", "I012", Path(items[0][0]["path"]).name,
                      items[0][1]["locator"],
                      f"整条内容完全重复(不同 ID 或不同文件):{locs}",
                      rid=idd, action="由用户确认后人工处理")
    return result


def check_exact_and_near_dups(audit: Audit, pool: list[tuple[dict, dict]]) -> dict:
    out = {"exact_problem_dups": [], "near_dups": [], "scene_spec_dups": [],
           "top_pairs": []}
    recs = [(info, r, r["record"]) for info, r in pool
            if isinstance(r.get("record"), dict)]
    # 精确重复:problem / scene_spec
    for key, bucket in (("problem", "exact_problem_dups"),
                        ("scene_spec", "scene_spec_dups")):
        seen = defaultdict(list)
        for info, r, rec in recs:
            v = rec.get(key)
            if isinstance(v, (str, dict)) and v:
                seen[json.dumps(v, sort_keys=True, ensure_ascii=False)].append((info, r))
        for _, items in seen.items():
            if len(items) > 1:
                locs = ", ".join(f"{x[0]['path']}:{x[1]['locator']}" for x in items)
                ids = [str(x[1]["record"].get("id")) for x in items]
                out[bucket].append({"ids": ids, "locs": locs})
                for x in items:
                    audit.add("hard" if key == "problem" else "quarantine", "D001",
                              x[0]["path"], x[1]["locator"],
                              f"{key} 完全重复:{locs}(ids={ids})",
                              rid=str(x[1]["record"].get("id")), field=key,
                              action="由用户确认后人工处理,不自动删除")
    # 近重复:problem 5-gram Jaccard(项目阈值 0.7,PROGRESS B5 标注未校准)
    n = len(recs)
    for i in range(n):
        for j in range(i + 1, n):
            ti, tj = recs[i][2].get("problem") or "", recs[j][2].get("problem") or ""
            if not ti or not tj:
                continue
            sim = jaccard(shingles(ti), shingles(tj))
            ratio = SequenceMatcher(None, norm_text(ti), norm_text(tj)).ratio()
            pair = {"a": str(recs[i][2].get("id")), "b": str(recs[j][2].get("id")),
                    "jaccard": round(sim, 4), "ratio": round(ratio, 4)}
            out["top_pairs"].append(pair)
            if sim >= 0.7 and ti != tj:
                out["near_dups"].append(pair)
                for x, other in ((recs[i], recs[j]), (recs[j], recs[i])):
                    audit.add("hard", "D002", x[0]["path"], x[1]["locator"],
                              f"近重复(problem 5-gram Jaccard={sim:.3f} ≥ 0.7):"
                              f"{pair['a']} ↔ {pair['b']}",
                              rid=str(x[2].get("id")), field="problem",
                              action="用户确认后人工合并/改写;不自动删除")
    out["top_pairs"].sort(key=lambda p: -p["jaccard"])
    out["top_pairs"] = out["top_pairs"][:15]
    return out


def check_mirror(audit: Audit, jsonl_infos: list[dict], json_infos: list[dict]) -> list[dict]:
    """JSON 数组容器 ↔ JSONL 镜像逐条比对。"""
    out = []
    jl = {}
    for info in jsonl_infos:
        for r in info["records"]:
            if isinstance(r.get("record"), dict):
                jl[str(r["record"].get("id"))] = (info, r)
    js = {}
    for info in json_infos:
        for r in info["records"]:
            if isinstance(r.get("record"), dict):
                js[str(r["record"].get("id"))] = (info, r)
    for rid in sorted(set(jl) | set(js)):
        a, b = jl.get(rid), js.get(rid)
        if a and b:
            same = json.dumps(a[1]["record"], sort_keys=True, ensure_ascii=False) == \
                   json.dumps(b[1]["record"], sort_keys=True, ensure_ascii=False)
            out.append({"id": rid, "jsonl": f"{a[0]['path']}:{a[1]['locator']}",
                        "json": f"{b[0]['path']}:{b[1]['locator']}", "identical": same})
            if not same:
                audit.add("hard", "D010", b[0]["path"], b[1]["locator"],
                          f"JSON 容器与 JSONL 镜像内容不一致(id={rid})",
                          rid=rid, action="以用户确认为准重建镜像,本次不改写")
        elif a:
            audit.add("hard", "D011", a[0]["path"], a[1]["locator"],
                      f"JSONL 中的 id={rid} 在 JSON 容器中缺失", rid=rid)
        else:
            audit.add("info", "D012", b[0]["path"], b[1]["locator"],
                      f"JSON 容器中的 id={rid} 未进入 JSONL", rid=rid)
    return out


def check_id_numbering(audit: Audit, pool: list[tuple[dict, dict]]) -> dict:
    """ID 编号连续性(结构观察,非硬伤)。"""
    out = {}
    for prefix in CATEGORY_BY_PREFIX:
        nums = []
        for info, r in pool:
            rid = str(r["record"].get("id"))
            m = re.match(rf"^{prefix}-[a-z-]+-(\d+)$", rid)
            if m:
                nums.append(int(m.group(1)))
        if not nums:
            continue
        lo, hi = min(nums), max(nums)
        missing = sorted(set(range(lo, hi + 1)) - set(nums))
        out[prefix] = {"count": len(nums), "min": lo, "max": hi,
                       "missing_numbers": missing}
        if missing:
            audit.add("info", "I020", "pool", "document",
                      f"{prefix} 编号 {lo}–{hi} 内缺号 {missing}"
                      f"(说明:可能为已删除/未生成条目,非硬伤)",
                      action="确认编号留空是有意为之")
    return out


def check_source_doc(audit: Audit, info: dict) -> dict:
    """dataset.md 手写来源文档体检。"""
    text = Path(info["abs_path"]).read_text(encoding="utf-8")
    out = {"n_id_fields": len(re.findall(r'"id"\s*:', text)),
           "n_typo_keys": {}, "n_fullwidth_comma": text.count("，"),
           "n_curly_quotes": text.count("“") + text.count("”"),
           "n_html_entities": len(re.findall(r"&#x?[0-9a-fA-F]+;", text)),
           "n_records_brace": text.count("&#x20;}")}
    typos = Counter()
    for k in ("catergory", "sub_catergory", "licence"):
        c = len(re.findall(rf'"{k}"', text))
        if c:
            typos[k] = c
            audit.add("quarantine", "SRC001", info["path"], "document",
                      f"来源文档键名拼写错误 \"{k}\"(×{c}):JSON 化时会被丢弃或改名",
                      field=k, evidence=k)
    out["n_typo_keys"] = dict(typos)
    for pat, code, msg in (
            (r"scene_spec\"\s*\{", "SRC002", "scene_spec 后缺冒号(非合法 JSON)"),
            (r"&#x20;", "SRC003", "残留在文本中的 HTML 实体 &#x20;"),
    ):
        c = len(re.findall(pat, text))
        if c:
            audit.add("quarantine", code, info["path"], "document", f"{msg}(×{c})")
    audit.add("info", "SRC004", info["path"], "document",
              f"来源文档为未结构化手稿:全角逗号 ×{out['n_fullwidth_comma']}、"
              f"中文引号 ×{out['n_curly_quotes']}、HTML 实体 ×{out['n_html_entities']};"
              f"\"id\" 字段 ×{out['n_id_fields']}")
    return out


def check_source_doc_coverage(audit: Audit, doc_infos: list[dict],
                              pool: list[tuple[dict, dict]]) -> dict:
    """来源手稿(dataset.md) ↔ 交付数据集 的覆盖/可追溯性。"""
    out = {"source_doc": [i["path"] for i in doc_infos], "source_records": 0,
           "source_unique_ids": 0, "pool_ids": 0, "dropped_ids": [],
           "dropped_categories": {}, "unmatched_pool_ids": []}
    if not doc_infos:
        return out
    text = Path(doc_infos[0]["abs_path"]).read_text(encoding="utf-8")
    matches = list(re.finditer(r'"id"\s*:\s*"([^"]+)"', text))
    cats = {}
    for k, m in enumerate(matches):
        seg = text[m.end(): matches[k + 1].start() if k + 1 < len(matches) else len(text)]
        cm = re.search(r'"(?:category|catergory)"\s*[:：]\s*"([^"]+)"', seg)
        cats[m.group(1)] = cm.group(1) if cm else None
    md_ids = [m.group(1) for m in matches]
    pool_ids = {str(r["record"].get("id")) for _, r in pool}
    missing = [i for i in md_ids if i not in pool_ids]
    out.update({
        "source_records": len(md_ids), "source_unique_ids": len(set(md_ids)),
        "pool_ids": len(pool_ids), "dropped_ids": missing,
        "dropped_categories": {i: cats.get(i) for i in missing},
        "unmatched_pool_ids": sorted(pool_ids - set(md_ids)),
        "source_category_counts": dict(Counter(cats.values())),
    })
    doc = doc_infos[0]["path"]
    if missing:
        audit.add("quarantine", "SRC005", doc, "document",
                  f"来源手稿有 {len(missing)} 条记录未进入交付数据集:{missing}"
                  f"(类别 {sorted(set(cats.get(i) for i in missing))});"
                  f"无删除/拒绝记录,来源与交付之间不可追溯",
                  evidence=missing,
                  action="确认是有意剔除还是遗漏;若为剔除,须补 rejected 记录与理由")
    if out["unmatched_pool_ids"]:
        audit.add("hard", "SRC006", doc, "document",
                  f"交付数据集有 id 在来源手稿中找不到:"
                  f"{out['unmatched_pool_ids']}", evidence=out["unmatched_pool_ids"])
    dups = [k for k, v in Counter(md_ids).items() if v > 1]
    if dups:
        audit.add("hard", "SRC007", doc, "document",
                  f"来源手稿内部 ID 重复:{dups}", evidence=dups)

    # 若来源文档本身是逐行 JSON 对象(JSONL 文本),做逐条内容比对
    doc_records = {}
    for rec in doc_infos[0]["records"]:
        if isinstance(rec.get("record"), dict) and rec["record"].get("id"):
            doc_records[str(rec["record"]["id"])] = rec["record"]
    if doc_records:
        pool_rec = {str(r["record"].get("id")): r["record"] for _, r in pool}
        common = sorted(set(doc_records) & set(pool_rec))
        diff = [rid for rid in common
                if json.dumps(doc_records[rid], sort_keys=True, ensure_ascii=False)
                != json.dumps(pool_rec[rid], sort_keys=True, ensure_ascii=False)]
        out["content_compared"] = len(common)
        out["content_diff_ids"] = diff
        if diff:
            audit.add("hard", "SRC008", doc, "document",
                      f"来源文档与交付数据逐条内容不一致的 id:{diff}",
                      evidence=diff, action="以用户确认为准同步;本次不改写")
        else:
            audit.add("info", "SRC008", doc, "document",
                      f"来源文档逐条内容与交付数据完全一致({len(common)}/{len(common)} 条)")
    return out


def check_manifest(audit: Audit, pool: list[tuple[dict, dict]]) -> dict:
    """data/v1 manifest 与交付文件的一致性、来源/许可证字段与验收语义。"""
    out = {"path": None, "n_entries": 0, "hash_ok": 0, "hash_bad": [],
           "missing_pool_files": [], "splits": {}, "acceptance_claim": False,
           "policy": None}
    man_dir = ROOT / "data" / "v1"
    if not man_dir.exists():
        return out
    manifests = sorted(p for p in man_dir.glob("*.json") if "manifest" in p.name.lower())
    if not manifests:
        return out
    p = manifests[0]
    out["path"] = str(p.relative_to(ROOT)).replace("\\", "/")
    try:
        m = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        audit.add("hard", "MF001", out["path"], "document", f"manifest 解析失败:{exc}")
        return out
    entries = m.get("entries") or []
    out["n_entries"] = len(entries)
    out["policy"] = m.get("policy")
    covered = set()
    for e in entries:
        rel = str(e.get("path", "")).replace("\\", "/")
        shown = f"data/v1/{rel}"
        covered.add(shown)
        ep = p.parent / rel
        if not ep.exists():
            out["hash_bad"].append({"path": shown, "reason": "文件不存在"})
            audit.add("hard", "MF002", out["path"], "document",
                      f"manifest 条目指向不存在的文件:{shown}", evidence=rel)
            continue
        data = ep.read_bytes()
        if sha256_bytes(data) == e.get("sha256") and len(data) == e.get("size"):
            out["hash_ok"] += 1
        else:
            out["hash_bad"].append({"path": shown, "reason": "sha256/size 不匹配"})
            audit.add("hard", "MF003", out["path"], "document",
                      f"manifest 条目的 sha256/size 与文件不符:{shown}",
                      evidence=e.get("sha256"))
        for k in ("source", "license", "split"):
            if not e.get(k):
                audit.add("quarantine", "MF004", out["path"], "document",
                          f"manifest 条目缺 {k}:{shown}", evidence=e)
        split = str(e.get("split") or "")
        out["splits"][split] = out["splits"].get(split, 0) + 1
        if split in ("train", "eval", "test"):
            out["acceptance_claim"] = True
    missing = sorted({i["path"] for i, _ in pool} - covered)
    out["missing_pool_files"] = missing
    if missing:
        audit.add("quarantine", "MF005", out["path"], "document",
                  f"交付样本未全部登记进 manifest:{missing}", evidence=missing)
    for k in ("accepted", "verified", "approved", "ready", "training_ready"):
        if k in m:
            out["acceptance_claim"] = True
            audit.add("hard", "MF006", out["path"], "document",
                      f"manifest 含验收/就绪语义字段 {k}={m[k]!r}")
    audit.add("info", "MF000", out["path"], "document",
              f"manifest 存在:条目 {len(entries)} 条,哈希/大小匹配 {out['hash_ok']} 条,"
              f"split={out['splits']},条目含来源/许可证字段;"
              f"{'含 train/eval/test 声明' if out['acceptance_claim'] else '未声明验收/训练就绪'}")
    return out


def check_acceptance_claims(audit: Audit, jsonl_infos: list[dict]) -> dict:
    """是否误把候选数据标成已验收训练数据。"""
    out = {"data_dir": "data/v1", "manifests": [], "formal_splits": [],
           "doc_claims": [], "record_level_claims": []}
    data_dir = ROOT / "data" / "v1"
    if data_dir.exists():
        for p in data_dir.rglob("*"):
            if p.is_file() and p.suffix == ".json" and "manifest" in p.name:
                out["manifests"].append(str(p.relative_to(ROOT)))
        for split in ("train", "eval", "test"):
            d = data_dir / split
            if d.exists():
                out["formal_splits"].append(str(d.relative_to(ROOT)))
    if not out["manifests"]:
        audit.add("info", "M001", "data/v1", "document",
                  "data/v1 下无 manifest.json:按 README/PROGRESS,数据未经验收登记")
    if not out["formal_splits"]:
        audit.add("info", "M002", "data/v1", "document",
                  "data/v1 下无 train/eval/test 目录:样本仍位于 raw/,属候选数据")
    # 记录级:是否有任何样本字段自称已验收
    for info in jsonl_infos:
        for r in info["records"]:
            rec = r.get("record")
            if not isinstance(rec, dict):
                continue
            blob = json.dumps(rec, ensure_ascii=False)
            for marker in EXPECTED_TRAIN_MARKERS:
                if marker in blob:
                    out["record_level_claims"].append(
                        {"file": info["path"], "locator": r["locator"],
                         "id": rec.get("id"), "marker": marker})
                    audit.add("hard", "M003", info["path"], r["locator"],
                              f"样本内容出现验收/训练就绪字样 {marker!r}(候选数据不得如此标注)",
                              rid=rec.get("id"))
    # 文档级声明扫描
    docs = ["README.md", "PROGRESS.md", "DATASET_REVIEW.md", "DATASET_SCHEMA.md",
            "data/README.md", "PIPELINE_PLAN.md", "NEXT_CYCLE_PLAN.md",
            "REVIEW_BACKLOG.md"]
    for name in docs:
        p = ROOT / name
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        for i, line in enumerate(text.splitlines(), 1):
            for marker in EXPECTED_TRAIN_MARKERS:
                if marker in line:
                    out["doc_claims"].append(
                        {"file": name, "line": i, "marker": marker,
                         "text": _trunc(line.strip(), 160)})
    return out


def check_doc_contradictions(audit: Audit, acceptance: dict) -> list[str]:
    """文档自相矛盾 / 状态语义混用。"""
    notes = []
    review = (ROOT / "DATASET_REVIEW.md")
    schema = (ROOT / "DATASET_SCHEMA.md")
    if review.exists():
        t = review.read_text(encoding="utf-8")
        m = re.search(r"状态:\s*\*\*([a-z]+)\*\*", t)
        if m:
            notes.append(f"DATASET_REVIEW.md 声明总状态 = {m.group(1)}")
            audit.add("info", "M010", "DATASET_REVIEW.md", "document",
                      f"报告头声明状态 **{m.group(1)}**;该状态是入场检查语义,"
                      f"不等于训练验收(报告正文已注明,但标题易被误读为已验收)",
                      evidence=_trunc(t.splitlines()[8] if len(t.splitlines()) > 8 else "", 140))
        for pat, msg in ((r"样本总数:\s*(\d+)", "样本总数"),
                         (r"高等代数:\s*(\d+)", None), (r"数学分析:\s*(\d+)", None),
                         (r"解析几何:\s*(\d+)", None), (r"概率论:\s*(\d+)", None)):
            mm = re.search(pat, t)
            if mm and msg:
                notes.append(f"DATASET_REVIEW.md {msg} = {mm.group(1)}")
    if schema.exists():
        t = schema.read_text(encoding="utf-8")
        for pat, label in ((r"当前\s*(\d+)\s*条均齐备", "scene_spec 齐备条数"),
                           (r"当前\s*(\d+)\s*条全部如此", "license 条数"),
                           (r"状态:\s*([a-z]+),\s*(\d+)\s*硬伤\s*\+\s*(\d+)\s*待补齐",
                            "schema 引用的审查结论")):
            mm = re.search(pat, t)
            if mm:
                notes.append(f"DATASET_SCHEMA.md {label} = {'/'.join(mm.groups())}")
    counts = Counter()
    for n in notes:
        m = re.search(r"=\s*(\d+)", n)
        if m and ("条" in n):
            counts[n.split()[1]] = int(m.group(1))
    vals = [v for v in counts.values() if v]
    if vals and (max(vals) != min(vals)):
        audit.add("hard", "M011", "DATASET_SCHEMA.md", "document",
                  f"文档间样本数量自相矛盾:{notes};须统一后再作为验收依据",
                  action="由用户确认权威计数并更新文档")
    if re.search(r"状态:\s*rejected", schema.read_text(encoding="utf-8")) if schema.exists() else False:
        audit.add("quarantine", "M012", "DATASET_SCHEMA.md", "document",
                  "DATASET_SCHEMA.md 引用的审查结论(rejected,3 硬伤 + 87 待补齐)"
                  "与当前 DATASET_REVIEW.md(clean)矛盾,属陈旧结论",
                  action="更新文档或重跑 report,避免以陈旧状态做验收")
    return notes


# ---------------------------------------------------------------- 主流程
def discover() -> tuple[list[Path], list[Path], list[Path]]:
    json_files = sorted(ROOT.glob("dataset_*.json"))
    jsonl_files = sorted((ROOT / "data" / "v1" / "raw").glob("dataset_*.jsonl"))
    docs = [p for p in (ROOT / "dataset.md",) if p.exists()]
    return json_files, jsonl_files, docs


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="候选数据集只读全量审计")
    ap.add_argument("--out", required=True, help="输出目录")
    ap.add_argument("--content-findings", default=None,
                    help="人工/评审内容发现 JSONL(可选),合并进逐条问题与状态")
    args = ap.parse_args(argv)
    out_dir = Path(args.out)
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    json_files, jsonl_files, docs = discover()
    audit = Audit()

    jsonl_infos = [load_file(p) for p in jsonl_files]
    json_infos = [load_file(p) for p in json_files]
    doc_infos = [load_file(p) for p in docs]

    for info in jsonl_infos + json_infos + doc_infos:
        check_structure(audit, info)

    pool: list[tuple[dict, dict]] = []
    for info in jsonl_infos:
        for r in info["records"]:
            if isinstance(r.get("record"), dict):
                pool.append((info, r))

    record_status = []
    scene_stats = {}
    lic_counter, src_counter, cat_counter = Counter(), Counter(), Counter()
    sub_counter, file_cat = Counter(), defaultdict(Counter)
    for info, r in pool:
        rec = r["record"]
        rid = str(rec.get("id"))
        check_fields(audit, info, r, rid)
        check_id(audit, info, r, rid)
        check_consistency(audit, info, r, rid)
        check_latex(audit, info, r, rid)
        scene = check_scene_spec(audit, info, r, rid)
        check_source_license(audit, info, r, rid)
        scene_stats[rid] = scene
        lic_counter[str(rec.get("license"))] += 1
        src_counter[str(rec.get("source"))] += 1
        cat_counter[str(rec.get("category"))] += 1
        sub_counter[(str(rec.get("category")), str(rec.get("sub_category")))] += 1
        file_cat[info["path"]][str(rec.get("category"))] += 1
        record_status.append({
            "file": info["path"], "locator": r["locator"], "id": rid,
            "category": rec.get("category"), "sub_category": rec.get("sub_category"),
            "status": None, "issue_codes": [], "severity_counts":
                {"hard": 0, "quarantine": 0, "info": 0},
            "animation_fields_present": scene["verified"],
            "n_objects": scene["objects"], "n_steps": scene["steps"],
        })

    id_result = check_pool_ids(audit, pool)
    dup_result = check_exact_and_near_dups(audit, pool)
    mirror = check_mirror(audit, jsonl_infos, json_infos)
    numbering = check_id_numbering(audit, pool)
    for info in doc_infos:
        check_source_doc(audit, info)
    src_cov = check_source_doc_coverage(audit, doc_infos, pool)
    manifest = check_manifest(audit, pool)
    acceptance = check_acceptance_claims(audit, jsonl_infos)
    doc_notes = check_doc_contradictions(audit, acceptance)

    # 评审内容发现(人工/评审产出,可追溯 verification 状态)合并
    content_findings = []
    cf_path = Path(args.content_findings) if args.content_findings else None
    if cf_path and not cf_path.is_absolute():
        cf_path = ROOT / cf_path
    if cf_path and cf_path.exists():
        for ln, raw in enumerate(cf_path.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            cf = json.loads(raw)
            content_findings.append(cf)
            audit.add(cf.get("severity", "quarantine"), cf.get("code", "K001"),
                      cf.get("file", "content-review"), cf.get("locator", "document"),
                      cf.get("message", ""), rid=cf.get("id"), field=cf.get("field"),
                      evidence=cf.get("evidence"),
                      action=cf.get("suggested_action") or "仅报告:人工确认后修改")
            for k in ("verification", "verified_by", "reviewer", "source"):
                if k in cf:
                    audit.issues[-1][k] = cf[k]

    # 回填每条记录的状态
    idx = {(x["file"], x["locator"]): x for x in record_status}
    for iss in audit.issues:
        key = (iss["file"], iss["locator"])
        if key in idx:
            e = idx[key]
            e["issue_codes"].append(iss["code"])
            e["severity_counts"][iss["severity"]] += 1
    for e in record_status:
        sc = e["severity_counts"]
        e["status"] = "rejected" if sc["hard"] else ("candidate" if sc["quarantine"]
                                                     else "clean")

    # 文件级状态
    per_file = []
    for info in jsonl_infos + json_infos + doc_infos:
        iss = [x for x in audit.issues if x["file"] == info["path"]]
        hard = [x for x in iss if x["severity"] == "hard"]
        quar = [x for x in iss if x["severity"] == "quarantine"]
        per_file.append({
            "file": info["path"], "format": info["format"],
            "n_records": sum(1 for r in info["records"] if isinstance(r.get("record"), dict)),
            "sha256": info["sha256"], "size": info["size"],
            "entry_status": "rejected" if hard else ("candidate" if quar else "clean"),
            "hard": len(hard), "quarantine": len(quar),
            "info": len([x for x in iss if x["severity"] == "info"]),
            "hard_codes": sorted({x["code"] for x in hard}),
            "quarantine_codes": sorted({x["code"] for x in quar}),
        })

    sev = Counter(x["severity"] for x in audit.issues)
    code_counts = Counter(x["code"] for x in audit.issues)
    status_counts = Counter(e["status"] for e in record_status)

    man_claim = bool(manifest.get("acceptance_claim"))
    man_path = manifest.get("path")
    suspicious = bool(acceptance["record_level_claims"] or acceptance["formal_splits"]
                      or man_claim)
    if suspicious:
        verdict = ("存在需要人工确认的验收/拆分声明:"
                   + (f"manifest={man_path} 含验收语义;" if man_claim else "")
                   + (f"train/eval/test 目录={acceptance['formal_splits']};"
                      if acceptance["formal_splits"] else "")
                   + (f"样本级验收字样={len(acceptance['record_level_claims'])} 条"
                      if acceptance["record_level_claims"] else ""))
    else:
        verdict = ("未发现候选数据被标注为已验收训练数据:样本位于 data/v1/raw/(raw 角色)、"
                   "无 train/eval/test 拆分;"
                   + (f"manifest({man_path})已登记且 split=raw、未声明验收/训练就绪"
                      if man_path else "无 manifest")
                   + "。文档中出现的 READY/验收字样均为'尚未就绪'的否定式表述")
    acceptance["verdict"] = verdict
    acceptance["manifest_acceptance_claim"] = man_claim
    acceptance["animation_verified_over_total"] = \
        f"{sum(1 for s in scene_stats.values() if s['verified'])}/{len(scene_stats)}"
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tool": "tools/dataset_audit.py (只读)",
        "contract": "DATASET_SCHEMA.md",
        "scope": {
            "jsonl": [i["path"] for i in jsonl_infos],
            "json": [i["path"] for i in json_infos],
            "source_docs": [i["path"] for i in doc_infos],
            "excluded": ["reviews/** fixtures(合成审查夹具,不参与训练)",
                         ".venv/**, runs/**, data 下其他非 dataset_* 文件"],
        },
        "totals": {
            "pool_records_jsonl": len(pool),
            "unique_ids_jsonl": len({str(r["record"].get("id")) for _, r in pool}),
            "json_container_records": sum(p["n_records"] for p in per_file
                                          if p["format"] == "json-array"),
            "all_records_incl_mirrors": sum(p["n_records"] for p in per_file
                                            if p["format"] in ("jsonl", "json-array")),
        },
        "severity_counts": dict(sev),
        "issue_code_counts": dict(sorted(code_counts.items())),
        "record_status_counts": dict(status_counts),
        "per_file": per_file,
        "distribution": {
            "category": dict(cat_counter),
            "category_share": {k: round(v / max(1, sum(cat_counter.values())), 4)
                               for k, v in cat_counter.items()},
            "sub_category": {f"{k[0]}/{k[1]}": v for k, v in sorted(sub_counter.items())},
            "per_file_category": {k: dict(v) for k, v in file_cat.items()},
            "split_roles": {
                "raw": len(pool), "train": 0, "eval": 0, "test": 0, "rejected": 0,
                "note": "data/v1 下只有 raw/,无 train/eval/test/rejected 目录;"
                        "样本角色=候选(raw)",
            },
            "license": dict(lic_counter),
            "source": dict(src_counter),
            "scene_spec": {
                "records": len(scene_stats),
                "objects_total": sum(s["objects"] for s in scene_stats.values()),
                "steps_total": sum(s["steps"] for s in scene_stats.values()),
                "objects_min": min((s["objects"] for s in scene_stats.values()), default=0),
                "objects_max": max((s["objects"] for s in scene_stats.values()), default=0),
                "steps_min": min((s["steps"] for s in scene_stats.values()), default=0),
                "steps_max": max((s["steps"] for s in scene_stats.values()), default=0),
                "animation_verified": sum(1 for s in scene_stats.values() if s["verified"]),
            },
        },
        "duplicates": {
            "ids": id_result,
            "exact": {"problem": dup_result["exact_problem_dups"],
                      "scene_spec": dup_result["scene_spec_dups"]},
            "near_dups_threshold_0.7": dup_result["near_dups"],
            "top_pairs": dup_result["top_pairs"],
        },
        "mirror_json_vs_jsonl": {
            "pairs": len(mirror),
            "identical": sum(1 for m in mirror if m["identical"]),
            "mismatched": [m for m in mirror if not m["identical"]],
        },
        "id_numbering": numbering,
        "source_doc_coverage": src_cov,
        "manifest": manifest,
        "content_review": {
            "file": str(cf_path.relative_to(ROOT)).replace("\\", "/")
                    if cf_path and cf_path.exists() else None,
            "n": len(content_findings),
            "by_severity": dict(Counter(c.get("severity") for c in content_findings)),
            "items": content_findings,
        },
        "acceptance": {**acceptance, "doc_notes": doc_notes},
    }

    # ---------------------------------------------------------------- 输出
    hashes = {
        "algorithm": "sha256",
        "generated_at": summary["generated_at"],
        "files": [{
            "path": p["file"], "sha256": p["sha256"], "size": p["size"],
            "format": p["format"], "n_records": p["n_records"],
        } for p in per_file],
    }
    (out_dir / "file_hashes.json").write_text(
        json.dumps(hashes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out_dir / "file_hashes.sha256").write_text(
        "".join(f"{p['sha256']}  {p['file']}\n" for p in per_file), encoding="utf-8")
    (out_dir / "issues.jsonl").write_text(
        "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in audit.issues),
        encoding="utf-8")
    (out_dir / "record_status.jsonl").write_text(
        "".join(json.dumps(x, ensure_ascii=False) + "\n" for x in record_status),
        encoding="utf-8")
    csv_cols = ["file", "locator", "id", "category", "sub_category", "status",
                "n_objects", "n_steps", "animation_fields_present"]
    csv_lines = [",".join(csv_cols)]
    for e in record_status:
        csv_lines.append(",".join(
            f'"{str(e.get(c, "")).replace(chr(34), chr(34) * 2)}"' for c in csv_cols))
    (out_dir / "record_status.csv").write_text("\n".join(csv_lines) + "\n",
                                               encoding="utf-8")
    (out_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # 控制台摘要
    print(f"[审计] 样本池(JSONL) {len(pool)} 条,唯一 ID "
          f"{summary['totals']['unique_ids_jsonl']} 个")
    print(f"[审计] 逐条状态:{dict(status_counts)}")
    print(f"[审计] 问题计数:{dict(sev)}")
    print(f"[审计] 输出目录:{out_dir.relative_to(ROOT)}")
    for p in per_file:
        print(f"  - {p['file']}: n={p['n_records']} hard={p['hard']} "
              f"quarantine={p['quarantine']} entry_status={p['entry_status']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
