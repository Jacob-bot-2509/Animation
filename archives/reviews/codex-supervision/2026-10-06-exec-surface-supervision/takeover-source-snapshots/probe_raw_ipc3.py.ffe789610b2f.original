# -*- coding: utf-8 -*-
"""第三批探针:D12 原始ICMP收发实测 / F2 命名管道双向 / F3 邮件槽 /
F5 剪贴板双向 / D13 WinHTTP(certutil+全路径powershell) / F6 窗口消息 /
F4 反向:宿主建命名事件→容器打开并置位。

证据写入 probe-raw-ipc3-v1-results.json,绝不覆盖旧文件。
"""
from __future__ import annotations

import json
import socket
import subprocess
import threading
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
import sys
sys.path.insert(0, str(ROOT / "src"))

from animtrain.sandbox_execution import run_code

HERE = Path(__file__).parent
OUT = HERE / "probe-raw-ipc3-v1-results.json"
if OUT.exists():
    raise ValueError("preserve previous evidence")

NONCE = uuid.uuid4().hex[:12]
import ctypes
from ctypes import wintypes

k32 = ctypes.WinDLL("kernel32", use_last_error=True)
u32 = ctypes.WinDLL("user32", use_last_error=True)


def lan_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 53))
        return s.getsockname()[0]
    except OSError:
        return socket.gethostbyname(socket.gethostname())
    finally:
        s.close()


class HttpListener(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("0.0.0.0", 0))
        self.sock.listen(4)
        self.sock.settimeout(0.2)
        self.port = self.sock.getsockname()[1]
        self.hits = []

    def run(self):
        while True:
            try:
                conn, addr = self.sock.accept()
            except socket.timeout:
                continue
            except OSError:
                return
            with conn:
                try:
                    conn.recv(1024)
                    conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nok")
                except OSError:
                    pass
                self.hits.append(str(addr))

    def close(self):
        try:
            self.sock.close()
        except OSError:
            pass


class PipeServer(threading.Thread):
    """宿主命名管道服务:收到容器 nonce 即泄漏通道。"""
    def __init__(self, name):
        super().__init__(daemon=True)
        self.name = name
        self.received = []

    def run(self):
        h = k32.CreateNamedPipeW(
            self.name, 2 | 4 | 1, 0, 1, 0, 0, 0, None)  # PIPE_ACCESS_DUPLEX|overlapped
        if h == wintypes.HANDLE(-1).value:
            self.received.append(("pipe_create_failed", ctypes.get_last_error()))
            return
        k32.ConnectNamedPipe(h, None)
        buf = ctypes.create_string_buffer(256)
        n = wintypes.DWORD(0)
        if k32.ReadFile(h, buf, 256, ctypes.byref(n), None):
            self.received.append(buf.raw[: n.value].decode("ascii", "replace"))
        k32.CloseHandle(h)


class Mailslot(threading.Thread):
    """宿主邮件槽:收到容器 nonce 即泄漏通道。"""
    def __init__(self, name):
        super().__init__(daemon=True)
        self.name = name
        self.received = []

    def run(self):
        h = k32.CreateMailslotW(self.name, 0, 0, None)
        if h == wintypes.HANDLE(-1).value:
            self.received.append(("mailslot_create_failed", ctypes.get_last_error()))
            return
        buf = ctypes.create_string_buffer(256)
        n = wintypes.DWORD(0)
        ok = k32.ReadFile(h, buf, 256, ctypes.byref(n), None)
        k32.CloseHandle(h)
        self.received.append(buf.raw[: n.value].decode("ascii", "replace") if ok else ("read_rc", not ok))


class HostWindow(threading.Thread):
    """宿主窗口:容器 PostMessage 若送达即 UI 注入通道。"""
    def __init__(self, class_name):
        super().__init__(daemon=True)
        self.class_name = class_name
        self.messages = []

    def run(self):
        WNDPROC = ctypes.WINFUNCTYPE(ctypes.c_longlong, wintypes.HWND, wintypes.UINT,
                                     wintypes.WPARAM, wintypes.LPARAM)
        def proc(hwnd, msg, wp, lp):
            self.messages.append(msg)
            return u32.DefWindowProcW(hwnd, msg, wp, lp)
        wc = wintypes.WNDCLASSW()
        wc.lpfnWndProc = WNDPROC(proc)
        wc.lpszClassName = self.class_name
        wc.hInstance = k32.GetModuleHandleW(None)
        u32.RegisterClassW(ctypes.byref(wc))
        hwnd = u32.CreateWindowExW(0, self.class_name, self.class_name, 0,
                                   0, 0, 0, 0, None, None, wc.hInstance, None)
        msg = wintypes.MSG()
        deadline = time.time() + 12
        while time.time() < deadline:
            if u32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 1):
                u32.TranslateMessage(ctypes.byref(msg))
                u32.DispatchMessageW(ctypes.byref(msg))
            time.sleep(0.05)
        u32.DestroyWindow(hwnd)


def host_http_control(url):
    try:
        r = subprocess.run(["curl.exe", "-s", "--connect-timeout", "4", "--max-time", "6",
                            "-o", "NUL", url], timeout=10)
        return {"rc": r.returncode}
    except Exception as exc:
        return {"err": repr(exc)}


def set_clipboard_text(text):
    k32.GlobalAlloc.restype = ctypes.c_void_p
    k32.GlobalLock.restype = ctypes.c_void_p
    k32.GlobalLock.argtypes = [ctypes.c_void_p]
    k32.GlobalUnlock.argtypes = [ctypes.c_void_p]
    u32.SetClipboardData.argtypes = [wintypes.UINT, ctypes.c_void_p]
    u32.OpenClipboard(None)
    u32.EmptyClipboard()
    buf = ctypes.create_unicode_buffer(text)
    gmh = k32.GlobalAlloc(0x42, (len(text) + 1) * 2)
    dst = k32.GlobalLock(gmh)
    ctypes.memmove(dst, ctypes.addressof(buf), (len(text) + 1) * 2)
    k32.GlobalUnlock(gmh)
    u32.SetClipboardData(13, gmh)  # CF_UNICODE
    u32.CloseClipboard()


def get_clipboard_text():
    k32.GlobalAlloc.restype = ctypes.c_void_p
    k32.GlobalLock.restype = ctypes.c_void_p
    k32.GlobalLock.argtypes = [ctypes.c_void_p]
    k32.GlobalUnlock.argtypes = [ctypes.c_void_p]
    u32.GetClipboardData.restype = ctypes.c_void_p
    try:
        u32.OpenClipboard(None)
        h = u32.GetClipboardData(13)
        if not h:
            u32.CloseClipboard()
            return None
        p = k32.GlobalLock(h)
        text = ctypes.wstring_at(p) if p else None
        k32.GlobalUnlock(h)
        u32.CloseClipboard()
        return text
    except Exception as exc:
        return "clipboard_error:" + repr(exc)


def main() -> int:
    ip = lan_ip()
    report = {
        "probe": "raw-ipc3-v1",
        "lan_ip": ip,
        "nonce": NONCE,
        "production_gate": "CLOSED",
        "controls": {},
        "sandbox": {},
        "after": {},
    }
    listener = HttpListener()
    listener.start()
    time.sleep(0.1)
    report["controls"]["http_via_lan_ip"] = host_http_control(f"http://{ip}:{listener.port}/")
    hits_before = len(listener.hits)

    # ICMP 控制:宿主机自己 ping 自己,确认该地址应答 echo
    try:
        r = subprocess.run(["ping.exe", "-n", "1", "-w", "3000", ip],
                           capture_output=True, text=True, timeout=10)
        report["controls"]["ping_self"] = {"rc": r.returncode,
                                           "out": (r.stdout or "")[:200]}
    except Exception as exc:
        report["controls"]["ping_self"] = {"err": repr(exc)}

    pipe_srv = PipeServer(r"\\.\pipe\AnimTrainPipe-" + NONCE)
    pipe_srv.start()
    slot = Mailslot(r"\\.\mailslot\AnimTrainSlot-" + NONCE)
    slot.start()
    evt = k32.CreateEventW(None, True, False, "Global\\AnimTrainEvt-" + NONCE)
    win = HostWindow("AnimTrainWnd-" + NONCE)
    win.start()
    time.sleep(0.3)
    set_clipboard_text("host-to-sandbox-" + NONCE)

    probe = r'''
import json,struct,time,socket,_socket,subprocess,ctypes
from ctypes import wintypes
r={}
lan_ip=__IP__
k32=ctypes.WinDLL("kernel32",use_last_error=True)
# D12 原始ICMP:发带nonce的echo请求,等宿主回显
def cksum(p):
 if len(p)%2:p+=b"\x00"
 s=sum(struct.unpack("!%dH"%(len(p)//2),p))
 s=(s>>16)+(s&0xffff);s+=s>>16
 return (~s)&0xffff
nonce=__NONCE__.encode()
pkt=struct.pack("!BBHHH",8,0,0,0x1234,1)+nonce
pkt=struct.pack("!BBHHH",8,0,cksum(pkt),0x1234,1)+nonce
try:
 s=_socket.socket(_socket.AF_INET,_socket.SOCK_RAW,_socket.IPPROTO_ICMP)
 s.settimeout(4)
 try:
  s.sendto(pkt,(lan_ip,0));r["icmp_send"]={"outcome":"sent"}
 except OSError as e:r["icmp_send"]={"outcome":"denied","winerror":getattr(e,"winerror",None)}
 got=None;deadline=time.time()+4
 while time.time()<deadline:
  try:
   data,addr=s.recvfrom(4096)
   if nonce in data:got={"reply_from":str(addr),"payload_match":True};break
  except OSError:break
 r["icmp_reply"]=got or {"reply":None}
except OSError as e:r["icmp_socket"]={"outcome":"denied","winerror":getattr(e,"winerror",None)}
# F4 反向:宿主建的命名事件,容器能否打开并置位
h=k32.OpenEventW(0x100000,False,"Global\\AnimTrainEvt-"+__NONCE__)
r["open_host_event"]={"opened":bool(h),"winerror":ctypes.get_last_error()}
if h:
 try:k32.SetEvent(h);r["open_host_event"]["set"]="ok"
 except OSError as e:r["open_host_event"]["set"]="denied:"+str(getattr(e,'winerror',None))
# F2 命名管道:容器连宿主管道写nonce
h=k32.CreateFileW(r"\\.\pipe\AnimTrainPipe-"+__NONCE__,0xC0000000,0,None,3,0,None)
r["pipe_open"]={"opened":h!=wintypes.HANDLE(-1).value,"winerror":ctypes.get_last_error()}
if h!=wintypes.HANDLE(-1).value:
 n=wintypes.DWORD(0)
 ok=k32.WriteFile(h,ctypes.create_string_buffer(b"pipe-nonce-"+nonce),20,ctypes.byref(n),None)
 r["pipe_open"]["write"]=bool(ok)
 k32.CloseHandle(h)
# F2 反向:容器自建管道,供宿主连接检测
h=k32.CreateNamedPipeW(r"\\.\pipe\AnimTrainSbx-"+__NONCE__,2|4|1,0,1,0,0,0,None)
r["pipe_create"]={"created":h!=wintypes.HANDLE(-1).value,"winerror":ctypes.get_last_error()}
if h!=wintypes.HANDLE(-1).value:k32.CloseHandle(h)
# F3 邮件槽:容器写宿主邮件槽
h=k32.CreateFileW(r"\\.\mailslot\AnimTrainSlot-"+__NONCE__,0x40000000,0,None,3,0,None)
r["mailslot_open"]={"opened":h!=wintypes.HANDLE(-1).value,"winerror":ctypes.get_last_error()}
if h!=wintypes.HANDLE(-1).value:
 n=wintypes.DWORD(0)
 ok=k32.WriteFile(h,ctypes.create_string_buffer(b"slot-nonce-"+nonce),19,ctypes.byref(n),None)
 r["mailslot_open"]["write"]=bool(ok)
 k32.CloseHandle(h)
# F5 剪贴板:读宿主写入的内容
try:
 u32=ctypes.WinDLL("user32",use_last_error=True)
 u32.OpenClipboard(None)
 hc=u32.GetClipboardData(13)
 if hc:
  p=k32.GlobalLock(hc);r["clip_read"]=ctypes.wstring_at(p) if p else None;k32.GlobalUnlock(hc)
 else:r["clip_read"]=None
 u32.CloseClipboard()
except OSError as e:r["clip_read"]="denied:"+str(getattr(e,'winerror',None))
# D13 WinHTTP/WinINET:certutil + 全路径 powershell
try:
 cp=subprocess.run(["certutil.exe","-urlcache","-split","-f","http://%s:%d/x"%(lan_ip,__PORT__),"NUL"],
  capture_output=True,text=True,timeout=20)
 r["certutil"]={"rc":cp.returncode,"out":(cp.stdout or '')[:150]}
except Exception as e:r["certutil"]={"err":e.__class__.__name__+':'+str(e)[:100]}
try:
 cp=subprocess.run([r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe","-NoProfile","-Command",
  "try{Invoke-WebRequest -UseBasicParsing -TimeoutSec 6 http://%s:%d/|Out-Null;'HIT'}catch{'DENIED'}"%(lan_ip,__PORT__)],
  capture_output=True,text=True,timeout=20)
 r["powershell_fullpath"]={"rc":cp.returncode,"out":(cp.stdout or '')[:100],"err":(cp.stderr or '')[:120]}
except Exception as e:r["powershell_fullpath"]={"err":e.__class__.__name__+':'+str(e)[:100]}
# F6 窗口消息:容器向宿主窗口 PostMessage
try:
 u32=ctypes.WinDLL("user32",use_last_error=True)
 hwnd=u32.FindWindowW(None,"AnimTrainWnd-"+__NONCE__)
 if hwnd:
  rc=u32.PostMessageW(hwnd,0x0401,0x5EED,0)
  r["postmessage"]={"found":True,"posted":bool(rc),"winerror":ctypes.get_last_error()}
 else:r["postmessage"]={"found":False}
except OSError as e:r["postmessage"]={"err":str(e)}
print(json.dumps(r),flush=True)
'''.replace("__IP__", repr(ip)).replace("__NONCE__", repr(NONCE)).replace("__PORT__", str(listener.port))

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
    report["controls"]["after_http_via_lan_ip"] = host_http_control(f"http://{ip}:{listener.port}/")
    time.sleep(0.5)
    listener.close()
    pipe_srv.join(timeout=3)
    slot.join(timeout=3)
    win.join(timeout=3)
    report["after"]["listener_hits"] = listener.hits
    report["after"]["hits_before_sandbox"] = hits_before
    report["after"]["sandbox_hit_listener"] = len(listener.hits) > hits_before
    report["after"]["pipe_server_received"] = pipe_srv.received
    report["after"]["mailslot_received"] = slot.received
    report["after"]["window_messages"] = win.messages
    report["after"]["host_event_signaled"] = bool(k32.WaitForSingleObject(evt, 0) == 0)
    report["after"]["clipboard_after"] = get_clipboard_text()
    k32.CloseHandle(evt)

    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("sandbox rc:", report["sandbox"]["rc"])
    print("sandbox results:", json.dumps(report["sandbox"].get("results"), ensure_ascii=False))
    print("pipe got:", report["after"]["pipe_server_received"], "| mailslot got:", report["after"]["mailslot_received"])
    print("window msgs:", report["after"]["window_messages"], "| event signaled:", report["after"]["host_event_signaled"])
    print("clipboard after:", report["after"]["clipboard_after"])
    print("listener sandbox hits:", report["after"]["sandbox_hit_listener"])
    print("evidence:", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
