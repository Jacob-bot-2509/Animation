# -*- coding: utf-8 -*-
"""第五批探针:节对象双向通道决定性测试 + 管道修正(标志=3)重测。

  节出站:容器建 Global 节并写入 nonce → 宿主 OpenFileMappingW(读+写)并读回
  节入站:宿主建 Global 节写 nonce → 容器打开(读+写)、读 nonce、改内容 → 宿主验证被改
  管道  :标志修正后容器连宿主管道 / 宿主连容器管道(双向)
证据写入 probe-ipc5-v1-results.json,绝不覆盖旧文件。
"""
from __future__ import annotations

import ctypes
import json
import threading
import time
import uuid
from ctypes import wintypes
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
import sys
sys.path.insert(0, str(ROOT / "src"))

from animtrain.sandbox_execution import run_code

HERE = Path(__file__).parent
OUT = HERE / "probe-ipc5-v1-results.json"
if OUT.exists():
    raise ValueError("preserve previous evidence")

NONCE = uuid.uuid4().hex[:12]
k32 = ctypes.WinDLL("kernel32", use_last_error=True)

_kH = ctypes.c_void_p
k32.CreateFileW.restype = _kH
k32.CreateNamedPipeW.restype = _kH
k32.CreateFileMappingW.restype = _kH
k32.OpenFileMappingW.restype = _kH
k32.MapViewOfFile.restype = _kH
k32.CloseHandle.argtypes = [_kH]
k32.ConnectNamedPipe.argtypes = [_kH, ctypes.c_void_p]
k32.ReadFile.argtypes = [_kH, ctypes.c_void_p, wintypes.DWORD,
                         ctypes.POINTER(wintypes.DWORD), ctypes.c_void_p]
k32.WriteFile.argtypes = [_kH, ctypes.c_void_p, wintypes.DWORD,
                          ctypes.POINTER(wintypes.DWORD), ctypes.c_void_p]
k32.CreateFileMappingW.argtypes = [_kH, ctypes.c_void_p, wintypes.DWORD,
                                   wintypes.DWORD, wintypes.DWORD, wintypes.LPCWSTR]
k32.OpenFileMappingW.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.LPCWSTR]
k32.MapViewOfFile.argtypes = [_kH, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, ctypes.c_size_t]
k32.UnmapViewOfFile.argtypes = [ctypes.c_void_p]
INVALID = ctypes.c_void_p(-1).value


class PipeSrv3(threading.Thread):
    def __init__(self, name, nonce):
        super().__init__(daemon=True)
        self.name, self.nonce = name, nonce
        self.result = {}

    def run(self):
        h = k32.CreateNamedPipeW(self.name, 3, 0, 1, 0, 0, 0, None)
        if h == INVALID:
            self.result = {"create": False, "winerror": ctypes.get_last_error()}
            return
        ok = k32.ConnectNamedPipe(h, None)
        buf = ctypes.create_string_buffer(self.nonce.encode())
        n = wintypes.DWORD(0)
        wrote = k32.WriteFile(h, buf, len(self.nonce), ctypes.byref(n), None)
        self.result = {"create": True, "connect": bool(ok), "write": bool(wrote),
                       "winerror": ctypes.get_last_error()}
        k32.CloseHandle(h)


class HostConnect3(threading.Thread):
    def __init__(self, name, nonce):
        super().__init__(daemon=True)
        self.name, self.nonce = name, nonce
        self.result = {}

    def run(self):
        time.sleep(8)
        h = k32.CreateFileW(self.name, 0xC0000000, 0, None, 3, 0, None)
        if h == INVALID:
            self.result = {"open": False, "winerror": ctypes.get_last_error()}
            return
        buf = ctypes.create_string_buffer(self.nonce.encode())
        n = wintypes.DWORD(0)
        wrote = k32.WriteFile(h, buf, len(self.nonce), ctypes.byref(n), None)
        self.result = {"open": True, "write": bool(wrote),
                       "winerror": ctypes.get_last_error()}
        k32.CloseHandle(h)


def host_section_open(name, access):
    """宿主打开容器建的节并读内容。返回 dict。"""
    h = k32.OpenFileMappingW(access, False, name)
    if not h:
        return {"opened": False, "winerror": ctypes.get_last_error()}
    p = k32.MapViewOfFile(h, access & 0xF000F, 0, 0, 64)
    if not p:
        err = ctypes.get_last_error()
        k32.CloseHandle(h)
        return {"opened": True, "mapped": False, "winerror": err}
    data = ctypes.string_at(p, 32).decode("ascii", "replace")
    k32.UnmapViewOfFile(p)
    k32.CloseHandle(h)
    return {"opened": True, "mapped": True, "data": data}


def main() -> int:
    report = {
        "probe": "ipc5-v1",
        "nonce": NONCE,
        "production_gate": "CLOSED",
        "sandbox": {},
        "after": {},
    }
    pipe_srv = PipeSrv3(r"\\.\pipe\AnimTrainIn5-" + NONCE, "host-pipe-in5-" + NONCE)
    pipe_srv.start()
    host_connect = HostConnect3(r"\\.\pipe\AnimTrainSbx5-" + NONCE, "host-pipe-out5-" + NONCE)
    host_connect.start()

    # 宿主建入站节并写 nonce
    sec_in = k32.CreateFileMappingW(INVALID, None, 4, 0, 64, "Global\\AnimTrainInSec5-" + NONCE)
    sec_in_err = ctypes.get_last_error()
    p_in = k32.MapViewOfFile(sec_in, 2, 0, 0, 64)
    if p_in:
        ctypes.memmove(p_in, ("host-sec-in-" + NONCE).encode(), 24)
        k32.UnmapViewOfFile(p_in)
    time.sleep(0.3)

    probe = r'''
import json,time,ctypes
from ctypes import wintypes
r={}
k32=ctypes.WinDLL("kernel32",use_last_error=True)
_kH=ctypes.c_void_p
k32.CreateFileW.restype=_kH
k32.CreateNamedPipeW.restype=_kH
k32.CreateFileMappingW.restype=_kH
k32.OpenFileMappingW.restype=_kH
k32.MapViewOfFile.restype=_kH
k32.CloseHandle.argtypes=[_kH]
k32.ConnectNamedPipe.argtypes=[_kH,ctypes.c_void_p]
k32.ReadFile.argtypes=[_kH,ctypes.c_void_p,wintypes.DWORD,ctypes.POINTER(wintypes.DWORD),ctypes.c_void_p]
k32.WriteFile.argtypes=[_kH,ctypes.c_void_p,wintypes.DWORD,ctypes.POINTER(wintypes.DWORD),ctypes.c_void_p]
k32.CreateFileMappingW.argtypes=[_kH,ctypes.c_void_p,wintypes.DWORD,wintypes.DWORD,wintypes.DWORD,wintypes.LPCWSTR]
k32.OpenFileMappingW.argtypes=[wintypes.DWORD,wintypes.BOOL,wintypes.LPCWSTR]
k32.MapViewOfFile.argtypes=[_kH,wintypes.DWORD,wintypes.DWORD,wintypes.DWORD,ctypes.c_size_t]
k32.UnmapViewOfFile.argtypes=[ctypes.c_void_p]
INVALID=ctypes.c_void_p(-1).value
# 管道:连宿主管道(标志3修正版)
ctypes.set_last_error(0)
h=k32.CreateFileW(r"\\.\pipe\AnimTrainIn5-"+__NONCE__,0xC0000000,0,None,3,0,None)
if h==INVALID:
 r["pipe_open"]={"opened":False,"winerror":ctypes.get_last_error()}
else:
 n=wintypes.DWORD(0)
 w=k32.WriteFile(h,ctypes.create_string_buffer(b"sbx5"),4,ctypes.byref(n),None)
 we=ctypes.get_last_error()
 buf=ctypes.create_string_buffer(64);n=wintypes.DWORD(0)
 rd=k32.ReadFile(h,buf,64,ctypes.byref(n),None)
 r["pipe_open"]={"opened":True,"write":bool(w),"write_err":we,
  "read":bool(rd),"data":buf.raw[:n.value].decode("ascii","replace")}
 k32.CloseHandle(h)
# 管道:容器自建(标志3)等宿主连
ctypes.set_last_error(0)
h=k32.CreateNamedPipeW(r"\\.\pipe\AnimTrainSbx5-"+__NONCE__,3,0,1,0,0,0,None)
if h==INVALID:
 r["pipe_create"]={"created":False,"winerror":ctypes.get_last_error()}
else:
 ok=k32.ConnectNamedPipe(h,None)
 buf=ctypes.create_string_buffer(64);n=wintypes.DWORD(0)
 rd=k32.ReadFile(h,buf,64,ctypes.byref(n),None)
 r["pipe_create"]={"created":True,"connect":bool(ok),"read":bool(rd),
  "data":buf.raw[:n.value].decode("ascii","replace")}
 k32.CloseHandle(h)
# 节入站:打开宿主节(读)并读内容
ctypes.set_last_error(0)
h=k32.OpenFileMappingW(4,False,"Global\\AnimTrainInSec5-"+__NONCE__)
if not h:
 r["sec_in_read"]={"opened":False,"winerror":ctypes.get_last_error()}
else:
 p=k32.MapViewOfFile(h,4,0,0,64)
 data=ctypes.string_at(p,32).decode("ascii","replace") if p else None
 r["sec_in_read"]={"opened":True,"data":data,"winerror":ctypes.get_last_error()}
 if p:k32.UnmapViewOfFile(p)
 k32.CloseHandle(h)
# 节入站:以写权限打开宿主节并改内容(宿主将验证是否被改)
ctypes.set_last_error(0)
h=k32.OpenFileMappingW(2,False,"Global\\AnimTrainInSec5-"+__NONCE__)
if not h:
 r["sec_in_write"]={"opened":False,"winerror":ctypes.get_last_error()}
else:
 p=k32.MapViewOfFile(h,2,0,0,64)
 if p:
  ctypes.memmove(p,b"SBX-MODIFIED-"+__NONCE__.encode(),18)
  r["sec_in_write"]={"opened":True,"mapped":True,"wrote":True}
  k32.UnmapViewOfFile(p)
 else:r["sec_in_write"]={"opened":True,"mapped":False,"winerror":ctypes.get_last_error()}
 k32.CloseHandle(h)
# 节出站:容器自建节写 nonce(宿主将尝试打开)
ctypes.set_last_error(0)
h=k32.CreateFileMappingW(INVALID,None,4,0,64,"Global\\AnimTrainOutSec5-"+__NONCE__)
if not h:
 r["sec_out"]={"created":False,"winerror":ctypes.get_last_error()}
else:
 p=k32.MapViewOfFile(h,2,0,0,64)
 if p:
  ctypes.memmove(p,("sbx-sec-out-"+__NONCE__).encode(),24)
  k32.UnmapViewOfFile(p)
 r["sec_out"]={"created":True,"written":True}
 k32.CloseHandle(h)
print(json.dumps(r),flush=True)
'''.replace("__NONCE__", repr(NONCE))

    cp = run_code(probe, mode="probe", timeout_ms=120000)
    report["sandbox"] = {
        "rc": cp["rc"],
        "stdout": cp["stdout"].strip(),
        "stderr": cp["stderr"].strip()[:500],
        "work": cp["work"],
    }
    try:
        report["sandbox"]["results"] = json.loads(cp["stdout"].strip().splitlines()[-1])
    except Exception:
        pass

    time.sleep(1.0)
    pipe_srv.join(timeout=4)
    host_connect.join(timeout=4)
    report["after"]["pipe_host_side"] = pipe_srv.result
    report["after"]["host_connect_pipe"] = host_connect.result
    # 宿主读回入站节,验证容器是否改写了内容
    p_in2 = k32.MapViewOfFile(sec_in, 4, 0, 0, 64)
    report["after"]["in_sec_content_after"] = (
        ctypes.string_at(p_in2, 32).decode("ascii", "replace") if p_in2 else None)
    if p_in2:
        k32.UnmapViewOfFile(p_in2)
    if sec_in:
        k32.CloseHandle(sec_in)
    # 宿主打开容器建的出站节(读 + 写)
    report["after"]["out_sec_host_read"] = host_section_open(
        "Global\\AnimTrainOutSec5-" + NONCE, 4)
    report["after"]["out_sec_host_write"] = host_section_open(
        "Global\\AnimTrainOutSec5-" + NONCE, 2)

    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("sandbox rc:", report["sandbox"]["rc"])
    print("sandbox results:", json.dumps(report["sandbox"].get("results"), ensure_ascii=False))
    print("pipe host side:", report["after"]["pipe_host_side"])
    print("host connect sbx pipe:", report["after"]["host_connect_pipe"])
    print("in sec content after:", report["after"]["in_sec_content_after"])
    print("out sec host read:", report["after"]["out_sec_host_read"])
    print("out sec host write:", report["after"]["out_sec_host_write"])
    print("evidence:", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
