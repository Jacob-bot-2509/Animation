"""候选数据集入场检查(msg_152 P0/P1,纯标准库)。

入场契约(与 tools/dataset_intake.py、DATASET_SCHEMA.md 配套):
  1. 样本入口只接受 JSONL:一行一个 JSON 对象。JSON 数组整文件是"待转换"
     格式,必须显式 convert 后才能进检查,不得被误当正式样本通过。
  2. 全局 ID 唯一:同 ID 不同内容 = ID 冲突(硬伤);同 ID 同内容 = 整条重复
     (硬伤)。只报告可定位行号,绝不静默改名——真实数据由用户确认后修改。
  3. 关键字段(id/category/sub_category/problem/solution/scene_spec/source/
     license)缺失或空 → problems;answer 缺失、可选元数据(function_family/
     visual_style/efficiency_tags)缺失或空 → quarantine(candidate 语义),
     任何 quarantine 都不得 ok=true。
  4. 正式字段只认契约内字段(category/sub_category/license 等);license 白名单
     外一律 quarantine;Internal-Research-Use-Only 仅限内部研究使用,不是
     公开再分发许可证,证据待用户确认。
  5. LaTeX 规则:$...$ 公式内不得出现中文(TeX 无 CJK,渲染必失败 → problems);
     疑似漏反斜杠(+infty、裸 arctan/lim/sin 等)只报 render_risk 进
     quarantine,绝不自动改写数学语义。
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from .atomic_write import atomic_write_text
from .fields import _is_missing  # noqa: F401  (与字段校验同一缺失语义)
from .freeze import check_frozen, discover_locks, frozen_paths
from .fs_guard import ensure_not_exists

# 许可证白名单(与 manifest/validate 契约一致)。
# Internal-Research-Use-Only:用户确认(2026-10-02)仅内部研究使用、不公开分发、
# 后续转正 —— 见 DATASET_SCHEMA.md §4;不代表满足 Apache/MIT/CC。
LICENSE_WHITELIST = {"apache-2.0", "mit", "internal-generated", "cc-by-sa-4.0",
                     "Internal-Research-Use-Only"}
INTERNAL_LICENSE = "Internal-Research-Use-Only"

# 关键字段(缺失/空 → 硬伤);answer 是判分字段(缺失 → quarantine 候选语义)
REQUIRED_INTAKE = ["id", "category", "sub_category", "problem", "solution",
                   "scene_spec", "source", "license"]
OPTIONAL_META = ["function_family", "visual_style", "efficiency_tags"]

CJK_RE = re.compile(r"[一-鿿]")          # TeX 无 CJK,中文进公式必编译失败
MATH_SPAN_RE = re.compile(r"\$([^$]*)\$")        # $...$ 行内公式(数据无 \$ 转义)

# 疑似漏反斜杠(只报 render_risk,不改写):裸函数名渲染为斜体字母,语义丢失
_RENDER_RISK_PATTERNS = [
    (re.compile(r"\+infty"), "\\infty(应写作 +\\infty)"),
    (re.compile(r"(?<!\\)\b(?:arctan|arcsin|arccos)\b"), "\\arctan 等"),
    (re.compile(r"(?<!\\)\blim(?=\s*[_{])"), "\\lim"),
    (re.compile(r"(?<!\\)\b(?:sin|cos|tan|ln|log)\b"), "\\sin/\\cos/\\ln 等"),
]


def _assert_not_frozen(dst: Path) -> None:
    """写前保护锁本身与冻结目标；坏锁拒绝写入，force 不绕过。"""
    resolved = dst.resolve()
    if any(p.name.lower().endswith(".lock.json") for p in (dst, resolved)):
        raise ValueError("A7 冻结保护:拒绝写入冻结锁路径(*.lock.json)，--force 不能绕过")
    valid, suspicious = discover_locks([dst.parent])
    if suspicious:
        raise ValueError("A7 冻结保护:范围内存在无法识别的 *.lock.json"
                         f"({suspicious[0].name}),fail-closed 拒绝写入")
    target = str(resolved)
    for lock in valid:
        try:
            problems = check_frozen(lock)
            if problems:
                raise ValueError(f"A7 冻结保护:锁 {lock.name} 无效或已变化，"
                                 f"fail-closed 拒绝写入: {problems[0]}")
            covered = frozen_paths(lock)
            # Existing hard links share file bytes despite different resolved paths.
            is_frozen = target in covered or (
                resolved.exists()
                and any(resolved.samefile(p) for p in [lock, *covered]))
        except (OSError, UnicodeError, KeyError, TypeError, AttributeError) as exc:
            raise ValueError(f"A7 冻结保护:锁 {lock.name} 结构无效，"
                             "fail-closed 拒绝写入") from exc
        if is_frozen:
            raise ValueError(f"A7 冻结保护:目标已被冻结锁 {lock.name} 覆盖,"
                             "拒绝写入(--force 不能绕过)")


def detect_json_array(path: Path) -> bool:
    """整文件是否为 JSON 数组(待转换格式)。解析失败/非数组返回 False。"""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    if not text.lstrip().startswith("["):
        return False
    try:
        return isinstance(json.loads(text), list)
    except json.JSONDecodeError:
        return False


def convert_array_to_jsonl(src: Path, dst: Path, force: bool = False) -> dict:
    """JSON 数组 → JSONL(一行一对象,ensure_ascii=False,原子写入)。

    原文件只读不写;dst 已存在且未 --force → 拒绝覆盖。内容不做任何清洗。
    返回 {"n_records": int, "dst": str}。失败抛 ValueError/OSError。
    """
    if src.resolve() == dst.resolve():
        raise ValueError("拒绝覆盖转换输入文件，--force 不能绕过原文件只读保护")
    _assert_not_frozen(dst)
    try:
        records = json.loads(src.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"无法读取 JSON 数组 {src}: {exc}") from exc
    if not isinstance(records, list):
        raise ValueError(f"{src} 顶层不是 JSON 数组({type(records).__name__}),"
                         "无需/无法 convert")
    for i, r in enumerate(records):
        if not isinstance(r, dict):
            raise ValueError(f"{src} 第 {i} 个元素不是 JSON 对象,不能作为样本行")
    ensure_not_exists(dst, force=force)
    lines = [json.dumps(r, ensure_ascii=False) for r in records]
    atomic_write_text(dst, "\n".join(lines) + "\n")
    return {"n_records": len(records), "dst": str(dst)}


def _walk_strings(obj, fn) -> None:
    """递归遍历嵌套结构,对每个字符串调用 fn(用于 scene_spec 内公式检查)。"""
    if isinstance(obj, str):
        fn(obj)
    elif isinstance(obj, list):
        for x in obj:
            _walk_strings(x, fn)
    elif isinstance(obj, dict):
        for v in obj.values():
            _walk_strings(v, fn)


def check_record(record: dict, line: int) -> tuple[list[str], list[str]]:
    """单条样本检查。返回 (problems, quarantines)——两者都非空即不通过。"""
    problems: list[str] = []
    quarantines: list[str] = []
    sid = str(record.get("id") or "<no-id>")

    # 1. 关键字段(硬伤)
    missing = [f for f in REQUIRED_INTAKE if _is_missing(record.get(f))]
    if missing:
        problems.append(f"line {line}: 缺关键字段 {', '.join(missing)}(id={sid})")

    # 1.5 DI3 结构类型(A3 复审):id 只允许 str/int 标量;problem/solution/answer
    #     必须为字符串;scene_spec 必须是含 objects/steps 两列表的对象
    rid = record.get("id")
    if not _is_missing(rid) and (isinstance(rid, bool)
                                 or not isinstance(rid, (str, int))):
        problems.append(f"line {line}: id 类型非法({type(rid).__name__}),"
                        f"仅允许 str/int(id={rid!r})")
    for f in ("problem", "solution"):
        v = record.get(f)
        if not _is_missing(v) and not isinstance(v, str):
            problems.append(f"line {line}: {f} 不是字符串({type(v).__name__})")
    ans = record.get("answer")
    if not _is_missing(ans) and not isinstance(ans, str):
        problems.append(f"line {line}: answer 不是字符串({type(ans).__name__})")
    # G4 类型契约:category/sub_category/source 必须为字符串
    for f in ("category", "sub_category", "source"):
        v = record.get(f)
        if not _is_missing(v) and not isinstance(v, str):
            problems.append(f"line {line}: {f} 不是字符串({type(v).__name__})")
    spec = record.get("scene_spec")
    if not _is_missing(spec):
        if not isinstance(spec, dict):
            problems.append(f"line {line}: scene_spec 结构非法"
                            "(需含 objects/steps 的对象)")
        else:
            # G4:objects/steps 必须为非空字符串列表(空列表/[null]/[false] 不通过)
            bad_keys = []
            for k in ("objects", "steps"):
                v = spec.get(k)
                if (not isinstance(v, list) or not v
                        or any(not isinstance(x, str) or not x.strip() for x in v)):
                    bad_keys.append(k)
            if bad_keys:
                problems.append(f"line {line}: scene_spec.{'/'.join(bad_keys)} "
                                "必须为非空字符串列表(G4 类型契约)")

    # 2. answer(判分字段):缺 → quarantine,不得假绿
    if _is_missing(record.get("answer")):
        quarantines.append(f"line {line}: 缺 answer(id={sid},候选数据:判分字段待补齐)")

    # 3. 可选元数据:缺或空 → quarantine(candidate 语义)
    empty_meta = [f for f in OPTIONAL_META if _is_missing(record.get(f))]
    if empty_meta:
        quarantines.append(f"line {line}: 可选元数据缺/空: {', '.join(empty_meta)}"
                           f"(id={sid},candidate 语义)")
    # 3.5 B7 类型契约:可选元数据存在时必须是正确类型
    for f in ("function_family", "visual_style"):
        v = record.get(f)
        if not _is_missing(v) and not isinstance(v, str):
            problems.append(f"line {line}: {f} 不是字符串({type(v).__name__})")
    et = record.get("efficiency_tags")
    if not _is_missing(et) and (not isinstance(et, list)
                                or any(not isinstance(x, str) or not x.strip()
                                       for x in et)):
        problems.append(f"line {line}: efficiency_tags 必须为非空字符串列表"
                        "(B7 类型契约)")

    # 4. license:白名单外且未声明语义 → 硬伤。白名单含用户已确认的
    #    Internal-Research-Use-Only(见模块头注释与 DATASET_SCHEMA.md §4)。
    lic = record.get("license")
    if not _is_missing(lic) and str(lic).strip() not in LICENSE_WHITELIST:
        problems.append(f"line {line}: license={lic!r} 不在白名单且"
                        f"未声明语义(id={sid})")

    # 5. LaTeX:公式内中文(硬伤)+ 疑似漏反斜杠(quarantine,只报不改)
    def _check_text(text: str, field: str) -> None:
        for span in MATH_SPAN_RE.findall(text):
            if CJK_RE.search(span):
                problems.append(f"line {line}: {field} 数学公式内出现中文"
                                f"(TeX 无 CJK,渲染必失败): ${span[:40]}$")
                continue
            for pat, hint in _RENDER_RISK_PATTERNS:
                if pat.search(span):
                    quarantines.append(f"line {line}: {field} 疑似漏反斜杠"
                                       f"({hint}): ${span[:60]}$")
                    break

    for field in ("problem", "solution", "answer"):
        val = record.get(field)
        if isinstance(val, str):
            _check_text(val, field)
    spec = record.get("scene_spec")
    if isinstance(spec, dict):  # objects/steps 内的公式同样检查
        _walk_strings(spec, lambda s: _check_text(s, "scene_spec"))

    # 6. 正式字段只认契约内字段;出现其他键 → quarantine(提示查 DATASET_SCHEMA)
    formal = set(REQUIRED_INTAKE) | {"answer"} | set(OPTIONAL_META)
    extra = [k for k in record if k not in formal]
    if extra:
        quarantines.append(f"line {line}: 非正式字段 {extra}"
                           f"(id={sid},正式字段见 DATASET_SCHEMA.md)")

    return problems, quarantines


def check_duplicate_ids(records: list[tuple[int, dict]]) -> list[str]:
    """全局 ID 唯一性。同 ID 同内容 = 整条重复;同 ID 不同内容 = ID 冲突。

    均为硬伤;只报告可定位行号,不静默改名(真实数据由用户确认后修改)。
    """
    by_id: dict[str, list[tuple[int, dict]]] = {}
    for line, rec in records:
        sid = rec.get("id")
        if _is_missing(sid):
            continue  # 缺 ID 由 check_record 报
        by_id.setdefault(str(sid), []).append((line, rec))
    problems: list[str] = []
    for sid, items in sorted(by_id.items()):
        if len(items) < 2:
            continue
        lines = ", ".join(str(l) for l, _ in items)
        canon = {json.dumps(r, sort_keys=True, ensure_ascii=False) for _, r in items}
        if len(canon) == 1:
            problems.append(f"id={sid} 在行 {lines} 整条重复(内容完全相同);"
                            "真实数据由用户确认后去重,不得静默改名")
        else:
            problems.append(f"id={sid} 在行 {lines} 冲突:同一 ID 对应不同内容;"
                            "真实数据由用户确认后改 ID,不得静默改名")
    return problems


def check_intake_file(path) -> dict:
    """入场检查。JSON 数组/非 JSONL → 硬伤拒绝;JSONL 逐行检查。

    返回 {file, n_records, categories, problems, quarantines, ok, status,
    exit_code};status ∈ rejected(有硬伤)/candidate(有 quarantine)/clean。
    """
    p = Path(path)
    problems: list[str] = []
    quarantines: list[str] = []
    records: list[tuple[int, dict]] = []
    categories: dict[str, int] = {}
    id_lines: dict[str, list[int]] = {}  # DI2: 合法标量 id → 行号(供跨文件查重)

    def _finish() -> dict:
        ok = not problems and not quarantines
        status = "rejected" if problems else ("candidate" if quarantines else "clean")
        return {"file": str(p), "n_records": len(records),
                "categories": categories, "problems": problems,
                "quarantines": quarantines, "id_lines": id_lines,
                "ok": ok, "status": status,
                "exit_code": 1 if problems else (2 if quarantines else 0)}

    if not p.exists():
        problems.append(f"文件不存在: {p}")
        return _finish()
    if p.suffix != ".jsonl":
        if detect_json_array(p):
            problems.append(f"{p.name}: JSON 数组不是合法样本入口(项目 "
                            "train/eval/test 入口要求 JSONL 一行一对象);请先 "
                            "tools/dataset_intake.py convert 转换,原文件不会被覆盖")
        else:
            problems.append(f"{p.name}: 非 .jsonl 文件不能作为样本入口"
                            "(JSONL 一行一对象);请先 convert 转换")
        return _finish()

    for line_no, raw in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError as exc:
            problems.append(f"line {line_no}: JSON 解析失败: {exc}")
            continue
        if not isinstance(obj, dict):
            problems.append(f"line {line_no}: 样本不是 JSON 对象(null/数组/标量)")
            continue
        records.append((line_no, obj))
        cat = obj.get("category")
        if isinstance(cat, str) and cat.strip():
            categories[cat] = categories.get(cat, 0) + 1
        sid = obj.get("id")
        if (isinstance(sid, (str, int)) and not isinstance(sid, bool)
                and not (isinstance(sid, str) and not sid.strip())):
            id_lines.setdefault(str(sid), []).append(line_no)
        p2, q2 = check_record(obj, line_no)
        problems += p2
        quarantines += q2
    # DI1: 空 JSONL/无有效样本行 → 硬伤(空样本入口不得 ok=true)
    if not records:
        problems.append(f"{p.name}: 没有有效样本行(空 JSONL/空输入不得 ok=true)")
    problems += check_duplicate_ids(records)
    return _finish()


def _group(messages: list[str]) -> dict[str, tuple[int, list[str]]]:
    """按原因聚合:去掉 "文件名: line N: " 前缀、把 (id=…) 归一化为 (id=…)。
    返回 {原因: (次数, 前3条原始消息)}——原始消息保留完整文件/行号可定位。"""
    groups: dict[str, list[str]] = {}
    for m in messages:
        key = re.sub(r"^[^:]+: line \d+: ", "", m)
        key = re.sub(r"\(id=[^)]*\)", "(id=…)", key)
        groups.setdefault(key, []).append(m)
    return {k: (len(v), v[:3]) for k, v in sorted(groups.items())}


def intake_report(paths) -> dict:
    """多文件汇总。返回 {n_records, categories, problems, quarantines,
    problem_groups, quarantine_groups, ok, status, exit_code}。
    DI1: 空输入列表 → 硬伤;DI2: 跨文件同 ID → 硬伤(全局 ID 唯一,零容忍)。"""
    if not paths:
        return {"n_records": 0, "categories": {}, "problems": ["未提供任何输入文件"],
                "quarantines": [], "problem_groups": {},
                "quarantine_groups": {}, "ok": False, "status": "rejected",
                "exit_code": 1}
    reports = [check_intake_file(p) for p in paths]
    cats: dict[str, int] = {}
    for r in reports:
        for c, n in r["categories"].items():
            cats[c] = cats.get(c, 0) + n
    problems = [f"{Path(r['file']).name}: {x}" for r in reports for x in r["problems"]]
    quarantines = [f"{Path(r['file']).name}: {x}" for r in reports for x in r["quarantines"]]
    # DI2: 跨文件同 ID(同文件内的重复/冲突由 check_duplicate_ids 报)
    global_ids: dict[str, list[tuple[str, int]]] = {}
    for r in reports:
        file_id = str(Path(r["file"]).resolve())
        for sid, lines in r.get("id_lines", {}).items():
            for ln in lines:
                global_ids.setdefault(sid, []).append((file_id, ln))
    for sid, locs in sorted(global_ids.items()):
        files = {file_id for file_id, _ in locs}
        if len(files) > 1:
            locations = ", ".join(f"{file_id}:{ln}" for file_id, ln in locs)
            problems.append(f"id={sid} 跨文件重复({locations}):"
                            "全局 ID 唯一性,跨文件零容忍")
    n = sum(r["n_records"] for r in reports)
    ok = not problems and not quarantines
    status = "rejected" if problems else ("candidate" if quarantines else "clean")
    return {"n_records": n, "categories": cats, "problems": problems,
            "quarantines": quarantines, "problem_groups": _group(problems),
            "quarantine_groups": _group(quarantines), "ok": ok,
            "status": status,
            "exit_code": 1 if problems else (2 if quarantines else 0)}
