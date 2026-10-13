# -*- coding: utf-8 -*-
"""第六批探针:节对象命名空间隔离决定性测试(会话命名空间 + Global 复验)。

  A 会话空间入站:宿主建非Global节写nonce → 容器打开(读+写)
  B 会话空间出站:容器建非Global节写nonce → 宿主打开(读+写)
  C Global 复验 :宿主建Global节(记录建成功与否)→ 容器打开;容器建 → 宿主打开
所有 API 返回值和错误码逐步记录,不再依赖 GetLastError 推测。
证据写入 probe-ipc6-v1-results.json,绝不覆盖旧文件。
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
OUT = HERE / "probe-ipc6-v1-results.json"
if OUT.exists():
    raise ValueError("preserve previous evidence")

NONCE = uuid.uuid4().hex[:12]
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


def host_create_section(name):
    ctypes.set_last_error(0)
    h = k32.CreateFileMappingW(INVALID, None, 4, 0, 64, name)
    err = ctypes.get_last_error()
    if not h:
        return None, {"created": False, "winerror": err}
    ctypes.set_last_error(0)
    p = k32.MapViewOfFile(h, 2, 0, 0, 64)
    err2 = ctypes.get_last_error()
    if p:
        ctypes.memmove(p, ("HOST-SEC-" + NONCE).encode(), 20)
        k32.UnmapViewOfFile(p)
    return h, {"created": True, "mapped": bool(p), "map_winerror": err2}


def host_open_section(name, access):
    ctypes.set_last_error(0)
    h = k32.OpenFileMappingW(access, False, name)
    err = ctypes.get_last_error()
    if not h:
        return {"opened": False, "winerror": err}
    ctypes.set_last_error(0)
    p = k32.MapViewOfFile(h, 4, 0, 0, 64)
    err2 = ctypes.get_last_error()
    data = ctypes.string_at(p, 32).decode("ascii", "replace") if p else None
    if p:
        k32.UnmapViewOfFile(p)
    k32.CloseHandle(h)
    return {"opened": True, "mapped": bool(p), "data": data, "map_winerror": err2}


def main() -> int:
    report = {"probe": "ipc6-v1", "nonce": NONCE, "production_gate": "CLOSED",
              "host": {}, "sandbox": {}, "after": {}}

    # A:宿主建会话空间节
    h_a, r_a = host_create_section("AnimTrainSesSec-" + NONCE)
    report["host"]["ses_create"] = r_a
    # C:宿主建 Global 节
    h_c, r_c = host_create_section("Global\\AnimTrainSec6-" + NONCE)
    report["host"]["global_create"] = r_c
    time.sleep(0.3)

    probe = r'''
import json,time,ctypes
from ctypes import wintypes
r={}
k32=ctypes.WinDLL("kernel32",use_last_error=True)
_kH=ctypes.c_void_p
k32.CreateFileMappingW.restype=_kH
k32.OpenFileMappingW.restype=_kH
k32.MapViewOfFile.restype=_kH
k32.CloseHandle.argtypes=[_kH]
k32.CreateFileMappingW.argtypes=[_kH,ctypes.c_void_p,wintypes.DWORD,wintypes.DWORD,wintypes.DWORD,wintypes.LPCWSTR]
k32.OpenFileMappingW.argtypes=[wintypes.DWORD,wintypes.BOOL,wintypes.LPCWSTR]
k32.MapViewOfFile.argtypes=[_kH,wintypes.DWORD,wintypes.DWORD,wintypes.DWORD,ctypes.c_size_t]
k32.UnmapViewOfFile.argtypes=[ctypes.c_void_p]
INVALID=ctypes.c_void_p(-1).value
def op(name,access):
 ctypes.set_last_error(0)
 h=k32.OpenFileMappingW(access,False,name)
 e=ctypes.get_last_error()
 if not h:return {"opened":False,"winerror":e}
 ctypes.set_last_error(0)
 p=k32.MapViewOfFile(h,4,0,0,64)
 e2=ctypes.get_last_error()
 data=ctypes.string_at(p,32).decode("ascii","replace") if p else None
 if p:k32.UnmapViewOfFile(p)
 k32.CloseHandle(h)
 return {"opened":True,"mapped":bool(p),"data":data,"map_winerror":e2}
def cre(name):
 ctypes.set_last_error(0)
 h=k32.CreateFileMappingW(INVALID,None,4,0,64,name)
 e=ctypes.get_last_error()
 if not h:return {"created":False,"winerror":e}
 ctypes.set_last_error(0)
 p=k32.MapViewOfFile(h,2,0,0,64)
 e2=ctypes.get_last_error()
 if p:
  ctypes.memmove(p,("SBX-SEC-"+__NONCE__).encode(),20)
  k32.UnmapViewOfFile(p)
 k32.CloseHandle(h)
 return {"created":True,"mapped":bool(p),"map_winerror":e2}
# A 容器打开宿主会话空间节(读 + 写)
r["ses_in_read"]=op("AnimTrainSesSec-"+__NONCE__,4)
r["ses_in_write"]=op("AnimTrainSesSec-"+__NONCE__,2)
# C 容器打开宿主 Global 节
r["global_in_read"]=op("Global\\AnimTrainSec6-"+__NONCE__,4)
# B 容器建会话空间节(宿主稍后打开)
r["ses_out"]=cre("AnimTrainSbxSesSec-"+__NONCE__)
# C 容器建 Global 节
r["global_out"]=cre("Global\\AnimTrainSbxSec6-"+__NONCE__)
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
    # B:宿主打开容器建的会话空间节
    report["after"]["ses_out_host_read"] = host_open_section("AnimTrainSbxSesSec-" + NONCE, 4)
    report["after"]["ses_out_host_write"] = host_open_section("AnimTrainSbxSesSec-" + NONCE, 2)
    # C:宿主打开容器建的 Global 节
    report["after"]["global_out_host_read"] = host_open_section("Global\\AnimTrainSbxSec6-" + NONCE, 4)
    # A/C 收尾:宿主读回自己的节,看容器是否改写(写权限测试的真实效果)
    for tag, h in (("ses", h_a), ("global", h_c)):
        if h:
            ctypes.set_last_error(0)
            p = k32.MapViewOfFile(h, 4, 0, 0, 64)
            err = ctypes.get_last_error()
            report["after"][tag + "_content_after"] = (
                ctypes.string_at(p, 32).decode("ascii", "replace") if p else
                {"mapped": False, "winerror": err})
            if p:
                k32.UnmapViewOfFile(p)
            k32.CloseHandle(h)

    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("host ses_create:", r_a, "| global_create:", r_c)
    print("sandbox rc:", report["sandbox"]["rc"])
    print("sandbox results:", json.dumps(report["sandbox"].get("results"), ensure_ascii=False))
    print("after ses_out host:", report["after"]["ses_out_host_read"])
    print("after global_out host:", report["after"]["global_out_host_read"])
    print("after ses content:", report["after"].get("ses_content_after"))
    print("after global content:", report["after"].get("global_content_after"))
    print("evidence:", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
