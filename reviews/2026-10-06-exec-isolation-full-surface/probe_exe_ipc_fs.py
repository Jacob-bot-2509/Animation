# -*- coding: utf-8 -*-
"""第二批探针:D11 非Python程序出网 / 局域网TCP / F1 注册表 / C6 链接逃逸 /
C7 删除权限 / D12 原始套接字 / F4 全局共享内存节。

机制同 native_transport:宿主机 before/after 健康对照;沙箱内一次性执行;
证据写入 probe-exe-ipc-fs-v1-results.json,绝不覆盖旧文件。
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
OUT = HERE / "probe-exe-ipc-fs-v1-results.json"
if OUT.exists():
    raise ValueError("preserve previous evidence")

SENTINEL = HERE / "host-only-sentinel.txt"
SENTINEL.write_text("host-control-do-not-write", encoding="utf-8")
ESCAPE_MARKER = HERE / "escaped-marker.txt"
if ESCAPE_MARKER.exists():
    ESCAPE_MARKER.unlink()

NONCE = uuid.uuid4().hex[:12]


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


def host_http_control(url):
    try:
        r = subprocess.run(["curl.exe", "-s", "--connect-timeout", "4", "--max-time", "6",
                            "-o", "NUL", url], timeout=10)
        return {"rc": r.returncode}
    except Exception as exc:
        return {"err": repr(exc)}


def host_tcp_control(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(4)
    try:
        s.connect((ip, port))
        return "connected"
    except OSError as exc:
        return repr(exc)
    finally:
        s.close()


def main() -> int:
    ip = lan_ip()
    listener = HttpListener()
    listener.start()
    time.sleep(0.1)
    report = {
        "probe": "exe-ipc-fs-v1",
        "lan_ip": ip,
        "nonce": NONCE,
        "production_gate": "CLOSED",
        "controls": {},
        "sandbox": {},
        "after": {},
    }
    report["controls"]["http_via_lan_ip"] = host_http_control(f"http://{ip}:{listener.port}/")
    report["controls"]["tcp_via_lan_ip"] = host_tcp_control(ip, listener.port)
    report["controls"]["http_via_loopback"] = host_http_control(f"http://127.0.0.1:{listener.port}/")
    hits_before = len(listener.hits)  # 沙箱运行前的对照命中数

    probe = r'''
import json,os,subprocess,time,socket,_socket,winreg,ctypes
r={}
lan_ip,port=%(ip)r,%(port)d
# D11 非 Python 程序出网
for name,cmd in [
 ("curl_exe",["curl.exe","-s","--connect-timeout","4","--max-time","6","-o","NUL","http://%%s:%%d/"%%(lan_ip,port)]),
 ("powershell_exe",["powershell.exe","-NoProfile","-Command","try{Invoke-WebRequest -UseBasicParsing -TimeoutSec 6 http://%%s:%%d/|Out-Null;'HIT'}catch{'DENIED:'+$_.Exception.Message}"%%(lan_ip,port)])]:
 try:
  cp=subprocess.run(cmd,capture_output=True,text=True,timeout=15)
  r[name]={"rc":cp.returncode,"out":(cp.stdout or '')[:120],"err":(cp.stderr or '')[:120]}
 except Exception as e:
  r[name]={"err":e.__class__.__name__+':'+str(e)[:120]}
# 局域网 TCP(python 原生)
s=_socket.socket(_socket.AF_INET,_socket.SOCK_STREAM);s.settimeout(5)
try:
 s.connect((lan_ip,port));r["tcp_lan_v4"]={"outcome":"connected"}
except OSError as e:r["tcp_lan_v4"]={"outcome":"denied","winerror":getattr(e,'winerror',None)}
finally:s.close()
# D12 原始套接字
try:
 _socket.socket(_socket.AF_INET,_socket.SOCK_RAW,_socket.IPPROTO_ICMP);r["raw_icmp"]={"outcome":"created"}
except OSError as e:r["raw_icmp"]={"outcome":"denied","winerror":getattr(e,'winerror',None)}
# F1 注册表:HKLM 必须拒绝;HKCU 落入容器私有 hive
try:
 k=winreg.CreateKeyEx(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\AnimTrainProbe",0,winreg.KEY_SET_VALUE)
 winreg.SetValueEx(k,"t",0,winreg.REG_SZ,"x");winreg.CloseKey(k);r["reg_hklm"]={"outcome":"allowed"}
except OSError as e:r["reg_hklm"]={"outcome":"denied","winerror":getattr(e,'winerror',None)}
try:
 k=winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER,r"Software\AnimTrainProbe",0,winreg.KEY_SET_VALUE)
 winreg.SetValueEx(k,"t",0,winreg.REG_SZ,"x");winreg.CloseKey(k);r["reg_hkcu"]={"outcome":"allowed"}
except OSError as e:r["reg_hkcu"]={"outcome":"denied","winerror":getattr(e,'winerror',None)}
# C6 链接逃逸:work 内建 junction 指向外部目录,再穿它写文件
work=os.getcwd()
try:
 cp=subprocess.run(["cmd.exe","/c","mklink","/J",r"esc",%(sentinel_dir)r],capture_output=True,text=True,timeout=15)
 r["junction_create"]={"rc":cp.returncode,"out":(cp.stdout or '')[:120],"err":(cp.stderr or '')[:120]}
 try:
  with open(os.path.join(work,"esc",%(escape_name)r),"w",encoding="utf-8") as f:
   f.write("escaped")
  r["junction_write"]={"outcome":"allowed"}
 except OSError as e:r["junction_write"]={"outcome":"denied","winerror":getattr(e,'winerror',None)}
except Exception as e:
 r["junction_create"]={"err":e.__class__.__name__+':'+str(e)[:120]}
# C7 删除权限
try:
 os.remove(%(sentinel)r);r["delete_outside"]={"outcome":"deleted"}
except OSError as e:r["delete_outside"]={"outcome":"denied","winerror":getattr(e,'winerror',None)}
# F4 全局命名共享内存节(无 SeCreateGlobalPrivilege 应拒绝)
try:
 h=ctypes.windll.kernel32.CreateFileMappingW(None,None,4,0,4096,"Global\\AnimTrainProbe-"+%(nonce)r)
 if not h:r["global_section"]={"outcome":"denied","winerror":ctypes.get_last_error()}
 else:ctypes.windll.kernel32.CloseHandle(h);r["global_section"]={"outcome":"created"}
except OSError as e:r["global_section"]={"outcome":"denied","winerror":getattr(e,'winerror',None)}
print(json.dumps(r),flush=True)
''' % {
        "ip": ip, "port": listener.port, "sentinel": str(SENTINEL),
        "sentinel_dir": str(HERE), "escape_name": ESCAPE_MARKER.name,
        "nonce": NONCE,
    }

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
    report["after"]["listener_hits"] = listener.hits
    report["after"]["hits_before_sandbox"] = hits_before
    report["after"]["sandbox_hit_listener"] = len(listener.hits) > hits_before
    report["after"]["sentinel_exists"] = SENTINEL.exists()
    report["after"]["escape_marker_exists"] = ESCAPE_MARKER.exists()
    if ESCAPE_MARKER.exists():
        ESCAPE_MARKER.unlink()

    # F4 宿主侧复验:全局节不应存在
    import ctypes as _ct
    h = _ct.windll.kernel32.OpenFileMappingW(4, False, "Global\\AnimTrainProbe-" + NONCE)
    report["after"]["global_section_visible_to_host"] = bool(h)
    if h:
        _ct.windll.kernel32.CloseHandle(h)

    # F1 宿主侧复验:HKCU 不应有容器写入
    import winreg as _wr
    try:
        k = _wr.OpenKey(_wr.HKEY_CURRENT_USER, r"Software\AnimTrainProbe")
        _wr.CloseKey(k)
        report["after"]["hkcu_leaked_to_host"] = True
    except OSError:
        report["after"]["hkcu_leaked_to_host"] = False

    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("sandbox rc:", report["sandbox"]["rc"])
    print("sandbox results:", json.dumps(report["sandbox"].get("results"), ensure_ascii=False))
    print("listener hits:", report["after"]["listener_hits"])
    print("sentinel exists:", report["after"]["sentinel_exists"], "| escape marker:", report["after"]["escape_marker_exists"])
    print("global section visible:", report["after"]["global_section_visible_to_host"], "| hkcu leak:", report["after"]["hkcu_leaked_to_host"])
    print("evidence:", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
