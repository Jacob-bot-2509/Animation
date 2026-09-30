"""文件写入守卫(Codex 审查 R1,纯标准库):默认拒绝覆盖,防路径穿越。

审查发现:split --out 可与 pool 同目录原地覆盖、run_id 可带 ../ 穿越、
各工具输出无存在性保护。统一规则:
  1. 输出文件已存在 → 拒绝(显式 --force 才覆盖)
  2. run_id 等用户可控路径片段只允许 [A-Za-z0-9_-],拒绝分隔符与空白
"""
from __future__ import annotations

import re
from pathlib import Path

RUN_ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


def ensure_not_exists(path: Path, force: bool = False) -> None:
    """输出路径已存在且未 --force → 抛 ValueError(默认拒绝覆盖)。"""
    if path.exists() and not force:
        raise ValueError(f"输出已存在,拒绝覆盖: {path}(确需覆盖请加 --force)")


def valid_run_id(run_id: str) -> bool:
    return bool(RUN_ID_RE.match(run_id))
