# -*- coding: utf-8 -*-
"""解析 D 盘回收站的 $I 元数据文件,列出被删除文件的原始路径与删除时间。只读。"""
import struct
from pathlib import Path

RB = Path("D:/$Recycle.Bin")
OUT = []
for sid_dir in RB.iterdir():
    if not sid_dir.is_dir():
        continue
    for item in sid_dir.iterdir():
        if not item.name.startswith("$I"):
            continue
        raw = item.read_bytes()
        if len(raw) < 24:
            continue
        # 结构:头8字节(版本2+文件大小) + UTF-16LE 原始路径 + 8字节 FILETIME
        size = struct.unpack("<Q", raw[8:16])[0]
        rest = raw[24:]  # 跳过 24 字节头? 实际 $I: 8(ver) + 8(size) + 8(del time) + utf16 path
        # 标准 $I 结构: 8字节 header(version=2), 8字节 原文件大小, 8字节 FILETIME, UTF-16LE 路径
        try:
            fsize = struct.unpack("<Q", raw[8:16])[0]
            ft = struct.unpack("<Q", raw[16:24])[0]
            path = raw[24:].decode("utf-16-le", errors="replace").rstrip("\x00")
        except Exception as exc:
            path = "<decode error %s>" % exc
        OUT.append((item.name, path, fsize, ft))
for name, path, fsize, ft in OUT:
    print(f"{name} | {path} | {fsize}B")
print("total:", len(OUT))
