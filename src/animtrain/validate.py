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


def validate_manifest(m: Manifest, root: Path) -> dict:
    """对 manifest 与磁盘执行全部检查。返回 {ok, n_entries, problems, quarantines}。"""
    problems: list[str] = []
    quarantines: list[str] = []
    problems += schema_issues(m)

    train_hashes: set[str] = set()
    eval_test_entries = []

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
        # 3. 许可证(空 → quarantine)
        if not e.license:
            quarantines.append(f"{e.path}: 许可证未标注 → quarantine,禁入训练")
        # 4. 样本集合(供重叠检查)
        if e.split == "train":
            train_hashes |= _load_sample_hashes(p, e)
        elif e.split in ("eval", "test"):
            eval_test_entries.append((e, p))

    # 5. 精确重叠:评测/测试样本不得出现在训练集
    for e, p in eval_test_entries:
        if p.suffix not in _DATA_SUFFIXES:
            continue
        overlap = _load_sample_hashes(p, e) & train_hashes
        if overlap:
            problems.append(f"{e.path}: 与训练集精确重叠 {len(overlap)} 个样本"
                            "(零容忍,前项目 20/20 污染教训)")

    # 6. 近重复门禁(5-gram Jaccard ≥ 0.7):评测/测试样本不得是训练样本的
    #    改措辞/换数字版本。前项目标准;仅精确重叠不够。
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
                if sim >= NEAR_DUP_THRESHOLD:
                    problems.append(
                        f"{e.path}:{i + 1} 与训练样本近重复(5-gram Jaccard "
                        f"{sim:.3f} ≥ {NEAR_DUP_THRESHOLD},命中 {hit['path']}:"
                        f"{hit['line'] + 1})")

    # msg_101-1 数据合约:quarantine 不默认通过 —— 有任何 quarantine 即不通过,
    # 但 exit code 与 problems 区分(problems=1 硬伤;quarantine=2 待补齐信息)
    return {"ok": not problems and not quarantines,
            "n_entries": len(m.entries),
            "problems": problems, "quarantines": quarantines,
            "exit_code": 1 if problems else (2 if quarantines else 0)}
