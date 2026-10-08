"""数据校验:按 manifest 逐项检查文件与内容(纯标准库)。

检查项:
  1. 文件存在
  2. SHA256 一致(entry.sha256 非空才查;空 = 如实跳过,不伪造)
  3. 许可证白名单(空许可证 → quarantine)
  4. split 合法性
  5. 评测集/测试集与训练集**精确重叠**(样本级内容哈希,零容忍)
     —— 前项目 20/20 评测污染的教训,此检查是硬门禁

用法:
  from animtrain.validate import validate_manifest
  report = validate_manifest(manifest, root_dir)
  print(report["ok"], report["problems"])
"""
from __future__ import annotations

import json as _json
from fractions import Fraction
from pathlib import Path

from .manifest import (Manifest, canonical_problem_hash, canonical_problem_text,
                       sample_content_hash, schema_issues, sha256_file)
from .near_dup import ShingleIndex, shingles
from .kp_rule import kp_signature

# B5 v3 + 用户裁决(2026-10-04):防泄漏屏文字分量阈值 2/5(签名一致 AND
# J5 ≥ 2/5 才拦);0.7 是旧 5-gram-only 屏的未校准初始值,已废弃
NEAR_DUP_TEXT_THRESHOLD = 2 / 5
NEAR_DUP_RULE = "考点签名一致 AND 5-gram Jaccard达阈值"

from .fields import _is_missing  # noqa: E402  A6:与入场检查同一缺失语义

# 训练/评测数据按行读的样本集合;只对可哈希后缀生效
_DATA_SUFFIXES = {".jsonl", ".json"}


def _load_lines(path: Path) -> list[str]:
    """JSONL 文件的非空行列表;JSON 整文件视作单行;读取失败返回空(由存在检查上报)。"""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return []
    if path.suffix == ".jsonl":
        return [l for l in text.splitlines() if l.strip()]
    return [text] if text.strip() else []


def _load_sample_hashes(path: Path, entry) -> set[str]:
    """A8:样本级防泄漏身份哈希——只取核心正文(problem 优先,缺则 solution),
    规范化后哈希;ID/来源/类别/风格等元数据不参与,同题不同解/不同 id 同哈希。
    非行格式返回空集(如实,不伪造)。"""
    return {canonical_problem_hash(l) for l in _load_lines(path)}


def _find_bad_json_lines(path: Path) -> list[tuple[int, str]]:
    """坏 JSON 检查,按扩展名区分格式(复审第三轮:合法 pretty JSON 不得误报)。

    .jsonl: 逐行解析,报行号;
    .json : 整文件解析一次(pretty JSON 多行是合法的),失败报 line 1。
    """
    import json as _json
    bad: list[tuple[int, str]] = []
    if path.suffix == ".jsonl":
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                _json.loads(line)
            except _json.JSONDecodeError as exc:
                bad.append((i, str(exc)))
    elif path.suffix == ".json":
        try:
            _json.loads(path.read_text(encoding="utf-8"))
        except _json.JSONDecodeError as exc:
            bad.append((1, str(exc)))
    return bad


def _find_non_object_lines(path: Path) -> list[int]:
    """数据行里解析成功但不是 JSON 对象的行号(A1:null/数组/标量结构非法)。"""
    import json as _json
    out: list[int] = []
    if path.suffix != ".jsonl":
        return out  # 整文件 JSON 的非对象结构由调用方语义决定,这里不误判
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = _json.loads(line)
        except _json.JSONDecodeError:
            continue  # 由 _find_bad_json_lines 报
        if not isinstance(obj, dict):
            out.append(i)
    return out


def _record_id(obj: dict):
    """A6/GS3:统一 ID 提取语义——优先 id,缺则 sample_id(legacy 别名),
    再缺则多解复合身份 problem_id::solution_id。所有 ID 流程
    (重叠/去重/定位)必须用同一提取,避免别名冲突漏检。"""
    sid = obj.get("id") if obj.get("id") is not None else obj.get("sample_id")
    if sid is None:
        pid = obj.get("problem_id")
        s2 = obj.get("solution_id")
        if pid is not None and s2 is not None:
            return f"{pid}::{s2}"
    return sid


def _load_sample_ids(path: Path) -> set[str]:
    """JSONL 样本的 ID 字段(id/sample_id)集合;异常行用可定位标记。

    ID 合法性(A1):只允许 str/int(排除 bool);None/空串 → <no-id>;
    非标量(list/dict)或 bool → <invalid-id:<type>>;解析失败 → <unparsable>。
    不伪造占位字符串,标记必须能定位类型问题。
    """
    import json as _json
    ids: set[str] = set()
    for l in _load_lines(path):
        try:
            obj = _json.loads(l)
        except _json.JSONDecodeError:
            ids.add("<unparsable>")
            continue
        if not isinstance(obj, dict):  # null / 数组 / 标量 → 非对象,结构化标记
            ids.add("<non-object>")
            continue
        sid = _record_id(obj)
        if sid is None or (isinstance(sid, str) and not sid.strip()):
            ids.add("<no-id>")
        elif isinstance(sid, bool):
            ids.add("<invalid-id:bool>")
        elif isinstance(sid, (str, int)):
            ids.add(str(sid))
        else:  # list/dict/float/… 不可哈希或类型非法,不抛 TypeError
            ids.add(f"<invalid-id:{type(sid).__name__}>")
    return ids


def _find_invalid_id_lines(path: Path) -> list[tuple[int, str]]:
    """数据行 ID 字段非法的行号与原因(A1:空白/非标量/bool ID 可定位报告)。"""
    import json as _json
    out: list[tuple[int, str]] = []
    if path.suffix != ".jsonl":
        return out
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            obj = _json.loads(line)
        except _json.JSONDecodeError:
            continue
        if not isinstance(obj, dict):
            continue
        sid = _record_id(obj)
        if sid is None or (isinstance(sid, str) and not sid.strip()):
            out.append((i, "缺 ID 或仅空白"))
        elif isinstance(sid, bool) or not isinstance(sid, (str, int)):
            out.append((i, f"ID 类型非法({type(sid).__name__})"))
    return out


def validate_manifest(m: Manifest, root: Path,
                      near_dup_threshold: float = NEAR_DUP_TEXT_THRESHOLD) -> dict:
    """对 manifest 与磁盘执行全部检查。返回 {ok, n_entries, problems,
    quarantines, exit_code}。near_dup_threshold 为防泄漏屏的文字分量阈值
    (仅在与训练样本考点签名一致时生效,默认 2/5,应 B5 v3)。"""
    problems: list[str] = []
    quarantines: list[str] = []
    problems += schema_issues(m)
    # A1: 空 manifest 无效(函数级直调也要拦住,不靠 CLI)
    if not m.entries:
        problems.append("manifest 没有任何条目,无法验收(空清单不得 ok=true)")

    train_hashes: set[str] = set()
    train_ids: set[str] = set()
    eval_test_entries = []
    seen_file_hashes: dict[str, str] = {}  # sha256 → 先登记的 path
    split_id_locs: dict[str, dict[str, list[str]]] = {}  # A6: split → id → 位置
    approved: list[tuple] = []  # (entry, path) —— 只有通过全部前置检查的
                                # 才进入后续阶段;被拒路径绝不二次读取(复审 R3)

    for e in m.entries:
        # R3: entry.path 不得越出根目录(防 ../ 逃逸);resolve 后必须仍在 root 内
        p = (root / e.path).resolve()
        try:
            p.relative_to(root.resolve())
        except ValueError:
            problems.append(f"{e.path}: 路径越出根目录(../ 逃逸),拒绝读取")
            continue
        # 1. 文件存在
        if not p.exists():
            problems.append(f"{e.path}: 文件不存在")
            continue
        if not p.is_file():
            problems.append(f"{e.path}: 不是常规文件")
            continue
        is_data = e.split in ("train", "eval", "test")
        # 1.5 A1 格式边界:数据 split 只允许 JSONL —— .json 整文件注册为
        #     train/eval/test 一律拒绝(可定位问题);manifest/config 的 JSON
        #     不是数据 split,不受影响。理由:.json 整文件无行级样本语义,
        #     结构/ID 检查无法逐样本定位。
        if is_data and p.suffix != ".jsonl":
            problems.append(f"{e.path}: 数据格式仅支持 JSONL(.jsonl);"
                            f"{p.suffix or '(无扩展名)'} 注册为 {e.split} 不被接受"
                            " —— 请转 JSONL 或改 split 为 raw(A1 格式边界)")
            continue
        # 2. SHA256(数据文件必填;空 = 未校验,不得默认通过)
        if not e.sha256:
            if is_data:
                quarantines.append(f"{e.path}: 数据文件缺少 SHA256 → quarantine,"
                                   "不得默认通过")
        else:
            actual = sha256_file(p)
            if actual != e.sha256:
                problems.append(f"{e.path}: SHA256 不一致(登记 {e.sha256[:12]}…,"
                                f"实际 {actual[:12]}…)")
            # 2b. 文件 hash 重叠(msg_101-2):不同路径内容完全相同 → 检出。
            #     C2:空文件(size=0)不参与重叠判定 —— 两个空文件同哈希是
            #     空集合误报,不是内容重复;空文件本身由"数据文件为空"硬伤拦住。
            if p.stat().st_size > 0:
                if actual in seen_file_hashes:
                    problems.append(f"{e.path}: 与 {seen_file_hashes[actual]} "
                                    "文件内容完全相同(文件 hash 重叠=0 要求)")
                else:
                    seen_file_hashes[actual] = e.path
        # 3. 许可证与来源(空/None/仅空白 → quarantine,数据文件不得默认通过)
        # 注意 None(JSON null)不能 str() 成 "None" 蒙混 —— not x 短路先判
        if not e.license or not str(e.license).strip():
            quarantines.append(f"{e.path}: 许可证未标注 → quarantine,禁入训练")
        if not e.source or not str(e.source).strip():
            quarantines.append(f"{e.path}: 来源未标注(或仅空白) → quarantine,"
                               "不得默认通过")
        # 3b. A1: size 与实际不符(登记值必须与真实文件一致)
        if is_data and e.size and e.size != p.stat().st_size:
            problems.append(f"{e.path}: size 与实际不符(登记 {e.size},"
                            f"实际 {p.stat().st_size})")
        # 4. 坏 JSON/非对象结构/非法 ID 检查覆盖全部数据 split
        if is_data and p.suffix in _DATA_SUFFIXES:
            for ln, exc in _find_bad_json_lines(p):
                problems.append(f"{e.path}:{ln} JSON 解析失败: {exc}")
            for ln in _find_non_object_lines(p):
                problems.append(f"{e.path}:{ln} 样本不是 JSON 对象(null/数组/"
                                "标量),结构非法(A1)")
            for ln, why in _find_invalid_id_lines(p):
                problems.append(f"{e.path}:{ln} ID 非法: {why}(A1)")
            # A6:统一入口门禁——空样本入口、仅{id}缺核心正文、同 split 内重复 ID
            lines = _load_lines(p)
            if not lines:
                problems.append(f"{e.path}: 数据文件为空(空样本入口不得 ok=true)")
            for i, line in enumerate(lines, 1):
                try:
                    obj = _json.loads(line)
                except _json.JSONDecodeError:
                    continue
                if not isinstance(obj, dict):
                    continue
                if _is_missing(obj.get("problem")) or _is_missing(obj.get("solution")):
                    problems.append(f"{e.path}:{i} 样本缺核心正文字段 problem/solution"
                                    "(A6:仅 id 的样本不得通过)")
                elif not isinstance(obj.get("problem"), str) \
                        or not isinstance(obj.get("solution"), str):
                    problems.append(f"{e.path}:{i} 核心正文字段类型非法"
                                    "(A6:problem/solution 必须为字符串)")
                if _is_missing(obj.get("answer")):
                    quarantines.append(f"{e.path}:{i} 缺 answer"
                                       "(A6:与入场检查同口径,候选数据待补齐)")
                elif not isinstance(obj.get("answer"), str):
                    problems.append(f"{e.path}:{i} answer 类型非法"
                                    "(A6:answer 必须为字符串，与入场检查一致)")
                sid = _record_id(obj)
                if (isinstance(sid, (str, int)) and not isinstance(sid, bool)
                        and not (isinstance(sid, str) and not sid.strip())):
                    split_id_locs.setdefault(e.split, {}).setdefault(
                        str(sid), []).append(f"{e.path}:{i}")
        # 5. 样本集合(供重叠检查);仅通过以上全部检查的 entry 进入
        if e.split == "train":
            train_hashes |= _load_sample_hashes(p, e)
            train_ids |= _load_sample_ids(p)
            approved.append((e, p))
        elif e.split in ("eval", "test"):
            eval_test_entries.append((e, p))
            approved.append((e, p))

    # 4.5 A6:同一 split 内 ID 必须唯一(同文件/跨文件都查,入口门禁统一)
    for sp, by_id in split_id_locs.items():
        for sid, locs in sorted(by_id.items()):
            if len(locs) > 1:
                problems.append(f"{sp} 内 ID 重复: id={sid}({', '.join(locs)})"
                                "(A6:同集合样本 ID 必须唯一)")

    # 5. 精确重叠:三个集合两两检查(R4:不能只与 train 比,eval 与 test 之间
    #    同 ID/同内容同样必须检出)。内容哈希(A8 核心正文身份) + ID 字段双重。
    split_sets: dict[str, tuple[set[str], set[str]]] = {}  # split → (hashes, ids)
    for e, p in approved:
        if e.split not in ("train", "eval", "test"):
            continue
        if p.suffix not in _DATA_SUFFIXES:
            continue
        h, ids = split_sets.setdefault(e.split, (set(), set()))
        h |= _load_sample_hashes(p, e)
        ids |= _load_sample_ids(p)
    for a, b in (("train", "eval"), ("train", "test"), ("eval", "test")):
        ha, ia = split_sets.get(a, (set(), set()))
        hb, ib = split_sets.get(b, (set(), set()))
        if ha & hb:
            problems.append(f"{a} 与 {b} 精确重叠 {len(ha & hb)} 个样本"
                            "(零容忍,前项目 20/20 污染教训)")
        if ia & ib:
            problems.append(f"{a} 与 {b} ID 重叠 {len(ia & ib)} 个"
                            f"({sorted(ia & ib)[:5]}) —— 内容不同但 ID 相同也不行")

    # 6. 近重复门禁(应 B5 v3 + 用户裁决"保留变体,防泄漏屏拦同考点+文字
    #    高度相似"):评测/测试样本与训练样本**考点签名一致** AND
    #    5-gram Jaccard ≥ 阈值 → 视为换数字/换系数版本的泄漏候选,拦;
    #    同考点但文字差异大(不同函数族/任务要求的变体)按用户裁决保留。
    #    文字分量阈值默认 2/5:实测同考点 train-vs-eval/test 的 J5 在 0.4
    #    处有自然断档(0.4 以下为不同任务要求,0.4~0.6 为换数字版本)。
    #    无法提取考点签名(缺 category/problem 或不可归类)→ 不参与屏,
    #    不得把缺失值当成共同考点(与入场契约的硬伤语义一致)。
    if train_hashes:
        near_indexes: dict[tuple[str, str], ShingleIndex] = {}
        for e, p in approved:
            if e.split != "train":
                continue
            for i, line in enumerate(_load_lines(p)):
                # A8:对核心正文规范化文本做 shingle,元数据不参与相似度;
                # 签名随命中记录携带,判定时无需回查行内容
                try:
                    sig = kp_signature(_json.loads(line))
                except (ValueError, TypeError, KeyError, _json.JSONDecodeError):
                    sig = None
                if sig is None:
                    continue
                # 先按签名筛选候选,避免全池最大命中来自其他签名,
                # 遮住相似度略低但真正满足组合规则的训练题。
                near_idx = near_indexes.setdefault(sig, ShingleIndex())
                text = canonical_problem_text(line)
                near_idx.add(text, {"path": e.path, "line": i, "text": text})
        for e, p in eval_test_entries:
            if p.suffix not in _DATA_SUFFIXES:
                continue
            for i, line in enumerate(_load_lines(p)):
                try:
                    sig = kp_signature(_json.loads(line))
                except (ValueError, TypeError, KeyError, _json.JSONDecodeError):
                    sig = None
                if sig is None or sig not in near_indexes:
                    continue
                text = canonical_problem_text(line)
                sim, hit = near_indexes[sig].max_sim(text)
                if hit is not None and sim >= near_dup_threshold:
                    # 显示精确集合比值,不把浮点近似误写成数学结论。
                    a, b = shingles(text), shingles(hit["text"])
                    ratio = Fraction(len(a & b), len(a | b))
                    problems.append(
                        f"{e.path}:{i + 1} 与训练样本近重复(考点 {sig[0]}/"
                        f"{sig[1]} 一致,5-gram Jaccard {ratio} ≥ "
                        f"{Fraction(str(near_dup_threshold))},命中 {hit['path']}:"
                        f"{hit['line'] + 1})")

    # 6.5 B5 签名规则和组合屏诊断均不自动解除 ready。
    # 组合屏尚缺独立定义的泄漏标签及与输入/实现/目标绑定的复算证据。
    # 按检测条件筛掉 FN 后的 domain_recall 不能替代原标注召回率。
    near_dup_calibrated = False
    near_dup_calibration = {
        "rule": NEAR_DUP_RULE,
        "threshold": str(Fraction(str(near_dup_threshold))),
        "note": "组合规则缺少独立标签和匹配校准证据(UNCALIBRATED)"}
    b5_signature_calibration: dict = {}
    leakage_screen_report: dict = {}
    b5_path = root / "b5-calibration-report" / "b5-calibration-report.json"
    try:
        b5 = _json.loads(b5_path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        b5 = {}
    b5_cal = b5.get("calibration", {}) if isinstance(b5, dict) else {}
    if (isinstance(b5_cal, dict) and b5_cal.get("calibrated") is True
            and b5_cal.get("threshold") == "1"):
        # 仅记录报告自报状态供审查,不是门禁校准证明。
        b5_signature_calibration = {
            "reported_calibrated": True,
            "rule": "考点签名一致(模块+题型)", "threshold": b5_cal["threshold"],
            "tp": b5_cal.get("tp"), "fp": b5_cal.get("fp"),
            "fn": b5_cal.get("fn"), "tn": b5_cal.get("tn"),
            "note": str(b5_cal.get("note", ""))[:120]}
        near_dup_calibration["note"] += (
            ";B5 模块+题型签名与执行规则不同,不能解除 ready 阻断")
    lk = b5.get("leakage_screen_calibration", {}) if isinstance(b5, dict) else {}
    if isinstance(lk, dict) and lk:
        leakage_screen_report = {
            "reported_calibrated": lk.get("calibrated") is True,
            "rule": lk.get("rule"), "threshold": lk.get("threshold"),
            "tp": lk.get("tp"), "fp": lk.get("fp"),
            "fn": lk.get("fn"), "tn": lk.get("tn"),
            "recall_all_labels": lk.get("recall_all_labels"),
            "domain_recall": lk.get("domain_recall"),
            "note": "报告自报诊断未验证;不得作为 ready 校准证明"}
        near_dup_calibration["note"] += (
            ";组合屏报告自报 calibrated 不能替代独立验收")

    # msg_101-1 数据合约:quarantine 不默认通过 —— 有任何 quarantine 即不通过,
    # 但 exit code 与 problems 区分(problems=1 硬伤;quarantine=2 待补齐信息)
    return {"ok": not problems and not quarantines,
            "n_entries": len(m.entries),
            "problems": problems, "quarantines": quarantines,
            "near_dup_rule": NEAR_DUP_RULE,
            "near_dup_threshold": near_dup_threshold,
            "near_dup_calibrated": near_dup_calibrated,
            "near_dup_calibration": near_dup_calibration,
            "b5_signature_calibration": b5_signature_calibration,
            "leakage_screen_report": leakage_screen_report,
            "exit_code": 1 if problems else (2 if quarantines else 0)}
