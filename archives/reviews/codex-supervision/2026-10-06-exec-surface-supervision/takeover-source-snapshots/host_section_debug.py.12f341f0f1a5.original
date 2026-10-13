# -*- coding: utf-8 -*-
"""宿主侧节对象 API 干净调试:创建/映射/写读,逐步报返回值和错误码。"""
import ctypes
import json
from ctypes import wintypes

k32 = ctypes.WinDLL("kernel32", use_last_error=True)
_kH = ctypes.c_void_p
k32.CreateFileMappingW.restype = _kH
k32.OpenFileMappingW.restype = _kH
k32.MapViewOfFile.restype = _kH
k32.CloseHandle.argtypes = [_kH]
k32.CreateFileMappingW.argtypes = [_kH, ctypes.c_void_p, wintypes.DWORD,
                                   wintypes.DWORD, wintypes.DWORD, wintypes.LPCWSTR]
k32.OpenFileMappingW.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.LPCWSTR]
k32.MapViewOfFile.argtypes = [_kH, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, ctypes.c_size_t]
k32.UnmapViewOfFile.argtypes = [ctypes.c_void_p]
INVALID = ctypes.c_void_p(-1).value

r = {}
ctypes.set_last_error(0)
h = k32.CreateFileMappingW(INVALID, None, 4, 0, 64, "Global\\AnimTrainDbg-TestSec")
r["create"] = {"handle": hex(h) if h else 0, "winerror": ctypes.get_last_error()}
if h:
    ctypes.set_last_error(0)
    p = k32.MapViewOfFile(h, 2, 0, 0, 64)
    r["map_write"] = {"ptr": hex(p) if p else 0, "winerror": ctypes.get_last_error()}
    if p:
        ctypes.memmove(p, b"DBG-HOST-SECTION-DATA", 20)
        r["map_write"]["wrote"] = True
        k32.UnmapViewOfFile(p)
    ctypes.set_last_error(0)
    p2 = k32.MapViewOfFile(h, 4, 0, 0, 64)
    r["map_read"] = {"ptr": hex(p2) if p2 else 0, "winerror": ctypes.get_last_error(),
                     "data": ctypes.string_at(p2, 20).decode() if p2 else None}
    if p2:
        k32.UnmapViewOfFile(p2)
    k32.CloseHandle(h)
print(json.dumps(r, ensure_ascii=False, indent=2))
