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

from pathlib import Path

from .manifest import Manifest, sample_content_hash, schema_issues, sha256_file
from .near_dup import ShingleIndex, THRESHOLD as NEAR_DUP_THRESHOLD

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
    """JSONL/JSON 文件的样本级内容哈希集合。非行格式返回空集(如实,不伪造)。"""
    return {sample_content_hash(l) for l in _load_lines(path)}


def _load_sample_ids(path: Path) -> set[str]:
    """JSONL 样本的 ID 字段(id/sample_id)集合;解析失败的行记 <unparsable>。"""
    import json as _json
    ids: set[str] = set()
    for l in _load_lines(path):
        try:
            obj = _json.loads(l)
        except _json.JSONDecodeError:
            ids.add("<unparsable>")
            continue
        sid = obj.get("id") or obj.get("sample_id")
        ids.add(sid if sid else "<no-id>")
    return ids


def validate_manifest(m: Manifest, root: Path,
                      near_dup_threshold: float = NEAR_DUP_THRESHOLD) -> dict:
    """对 manifest 与磁盘执行全部检查。返回 {ok, n_entries, problems,
    quarantines, exit_code}。near_dup_threshold 可配置(msg_101-2:当前默认
    0.7 只是初始值,真实数据就位后须对照实验校准)。"""
    problems: list[str] = []
    quarantines: list[str] = []
    problems += schema_issues(m)

    train_hashes: set[str] = set()
    train_ids: set[str] = set()
    eval_test_entries = []
    seen_file_hashes: dict[str, str] = {}  # sha256 → 先登记的 path

    for e in m.entries:
        p = (root / e.path).resolve()
        # 1. 文件存在
        if not p.exists():
            problems.append(f"{e.path}: 文件不存在")
            continue
        if not p.is_file():
            problems.append(f"{e.path}: 不是常规文件")
            continue
        # 2. SHA256
        if e.sha256 and p.suffix.lower() in {".jsonl", ".json", ".parquet", ".py",
                                              ".txt", ".md", ".zip", ".html", ".js",
                                              ".css", ".svg"}:
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
        # 3. 许可证(空 → quarantine)
        if not e.license:
            quarantines.append(f"{e.path}: 许可证未标注 → quarantine,禁入训练")
        # 4. 样本集合(供重叠检查)
        if e.split == "train":
            train_hashes |= _load_sample_hashes(p, e)
            train_ids |= _load_sample_ids(p)
        elif e.split in ("eval", "test"):
            eval_test_entries.append((e, p))

    # 5. 精确重叠:评测/测试样本不得出现在训练集(内容哈希 + ID 字段双重)
    for e, p in eval_test_entries:
        if p.suffix not in _DATA_SUFFIXES:
            continue
        overlap = _load_sample_hashes(p, e) & train_hashes
        if overlap:
            problems.append(f"{e.path}: 与训练集精确重叠 {len(overlap)} 个样本"
                            "(零容忍,前项目 20/20 污染教训)")
        id_overlap = _load_sample_ids(p) & train_ids
        if id_overlap:
            problems.append(f"{e.path}: 与训练集 ID 重叠 {len(id_overlap)} 个"
                            f"({sorted(id_overlap)[:5]}) —— 内容不同但 ID 相同也不行")

    # 6. 近重复门禁(5-gram Jaccard ≥ 阈值,可配置):评测/测试样本不得是
    #    训练样本的改措辞/换数字版本。前项目标准;仅精确重叠不够。
    if train_hashes:
        near_idx = ShingleIndex()
        for e in m.entries:
            if e.split != "train":
                continue
            p = (root / e.path).resolve()
            if not p.exists():
                continue
            for i, line in enumerate(_load_lines(p)):
                near_idx.add(line, {"path": e.path, "line": i})
        for e, p in eval_test_entries:
            if p.suffix not in _DATA_SUFFIXES:
                continue
            for i, line in enumerate(_load_lines(p)):
                sim, hit = near_idx.max_sim(line)
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
            "exit_code": 1 if problems else (2 if quarantines else 0)}
