"""目录扫描 → 临时 manifest(核心逻辑,CLI 共用,纯标准库)。"""
from __future__ import annotations

import time
from pathlib import Path

from .manifest import Entry, Manifest, sha256_file

_SPLIT_BY_DIR = {"raw": "raw", "train": "train", "eval": "eval", "test": "test"}


def scan_dir(data_dir: Path) -> Manifest:
    """扫描 data/ 子目录,按目录名推断 split,生成临时 manifest(不落盘)。

    entry.path 相对 data_dir 自身 —— manifest 与数据同目录,自包含。
    """
    base = data_dir.resolve()
    m = Manifest(name="scan", generated_at=time.strftime("%Y-%m-%d %H:%M:%S"),
                 policy="扫描临时登记,非正式 manifest")
    for p in sorted(data_dir.resolve().rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(base)
        parts = p.relative_to(data_dir.resolve()).parts
        split = _SPLIT_BY_DIR.get(parts[0], "raw") if parts else "raw"
        m.entries.append(Entry(path=str(rel), sha256=sha256_file(p),
                              size=p.stat().st_size, split=split,
                              notes="scan: 来源/许可证待补(校验会报 quarantine)"))
    return m
