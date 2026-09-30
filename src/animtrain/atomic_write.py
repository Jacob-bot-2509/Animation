"""原子写入(B6,纯标准库):临时文件 + rename,失败不半写、不留半成品。

用途:split 输出、run_record、冻结锁等正式产物的最小可靠写入机制。
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path


def atomic_write_text(path: Path, text: str, encoding: str = "utf-8") -> None:
    """写文本:同目录临时文件 → os.replace 原子落位;任何失败清理临时文件。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp",
                                    dir=str(path.parent))
    os.close(fd)  # Windows:句柄不关会导致 rename 失败且临时文件删不掉
    tmp = Path(tmp_name)
    try:
        tmp.write_text(text, encoding=encoding)
        os.replace(tmp, path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise


def atomic_write_bytes(path: Path, data: bytes) -> None:
    """写字节:同目录临时文件 → os.replace 原子落位。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp",
                                    dir=str(path.parent))
    os.close(fd)  # Windows:句柄不关会导致 rename 失败且临时文件删不掉
    tmp = Path(tmp_name)
    try:
        tmp.write_bytes(data)
        os.replace(tmp, path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
