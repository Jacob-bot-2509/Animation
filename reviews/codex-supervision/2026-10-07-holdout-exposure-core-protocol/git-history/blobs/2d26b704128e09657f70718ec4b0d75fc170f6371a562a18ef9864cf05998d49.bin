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
from pathlib import Path

from .manifest import (Manifest, canonical_problem_hash, canonical_problem_text,
                       sample_content_hash, schema_issues, sha256_file)
from .near_dup import ShingleIndex, THRESHOLD as NEAR_DUP_THRESHOLD

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
        sid = obj.get("id") if obj.get("id") is not None else obj.get("sample_id")
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
        sid = obj.get("id") if obj.get("id") is not None else obj.get("sample_id")
        if sid is None or (isinstance(sid, str) and not sid.strip()):
            out.append((i, "缺 ID 或仅空白"))
        elif isinstance(sid, bool) or not isinstance(sid, (str, int)):
            out.append((i, f"ID 类型非法({type(sid).__name__})"))
    return out


def validate_manifest(m: Manifest, root: Path,
                      near_dup_threshold: float = NEAR_DUP_THRESHOLD) -> dict:
    """对 manifest 与磁盘执行全部检查。返回 {ok, n_entries, problems,
    quarantines, exit_code}。near_dup_threshold 可配置(msg_101-2:当前默认
    0.7 只是初始值,真实数据就位后须对照实验校准)。"""
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
            # 2b. 文件 hash 重叠(msg_101-2):不同路径内容完全相同 → 检出
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
                sid = obj.get("id")
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

    # 6. 近重复门禁(5-gram Jaccard ≥ 阈值,可配置):评测/测试样本不得是
    #    训练样本的改措辞/换数字版本。前项目标准;仅精确重叠不够。
    if train_hashes:
        near_idx = ShingleIndex()
        for e, p in approved:
            if e.split != "train":
                continue
            for i, line in enumerate(_load_lines(p)):
                # A8:对核心正文规范化文本做 shingle,元数据不参与相似度
                near_idx.add(canonical_problem_text(line), {"path": e.path, "line": i})
        for e, p in eval_test_entries:
            if p.suffix not in _DATA_SUFFIXES:
                continue
            for i, line in enumerate(_load_lines(p)):
                sim, hit = near_idx.max_sim(canonical_problem_text(line))
                if sim >= near_dup_threshold:
                    problems.append(
                        f"{e.path}:{i + 1} 与训练样本近重复(5-gram Jaccard "
                        f"{sim:.3f} ≥ {near_dup_threshold},命中 {hit['path']}:"
                        f"{hit['line'] + 1})")

    # msg_101-1 数据合约:quarantine 不默认通过 —— 有任何 quarantine 即不通过,
    # 但 exit code 与 problems 区分(problems=1 硬伤;quarantine=2 待补齐信息)
    return {"ok": not problems and not quarantines,
            "n_entries": len(m.entries),
            "problems": problems, "quarantines": quarantines,
            "near_dup_threshold": near_dup_threshold,
            "near_dup_calibrated": False,  # UNCALIBRATED:0.7 待真实数据对照实验
            "exit_code": 1 if problems else (2 if quarantines else 0)}
