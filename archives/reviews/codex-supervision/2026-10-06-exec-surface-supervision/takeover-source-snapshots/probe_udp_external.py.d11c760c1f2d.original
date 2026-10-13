# -*- coding: utf-8 -*-
"""D7/D8/D9/D10 探针:外部 UDP(v4/v6)、局域网 UDP、OS 层 DNS 解析。

机制(与 native_transport.py 同款):
  - 宿主机起 UDP 接收器(before/after 健康对照,证明通路可用)
  - 沙箱内 _socket 原生发 nonce(绕过一切 Python 层 shim)
  - 接收器若收到沙箱 nonce => 送达缺口坐实;OS 拒绝(winerror 10013)=> 绿
证据写入本目录 probe-udp-external-v1-results.json,绝不覆盖旧文件。
"""
from __future__ import annotations

import json
import socket
import threading
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
import sys
sys.path.insert(0, str(ROOT / "src"))

from animtrain.sandbox_execution import run_code

OUT = Path(__file__).with_name("probe-udp-external-v1-results.json")
if OUT.exists():
    raise ValueError("preserve previous evidence")


def lan_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 53))
        return s.getsockname()[0]
    except OSError:
        return socket.gethostbyname(socket.gethostname())
    finally:
        s.close()


class UdpReceiver(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", 0))
        self.sock.settimeout(0.2)
        self.port = self.sock.getsockname()[1]
        self.received = []  # (payload, addr)

    def run(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(4096)
            except socket.timeout:
                continue
            except OSError:
                return
            self.received.append((data.decode("ascii", "replace"), addr))

    def close(self):
        try:
            self.sock.close()
        except OSError:
            pass


def udp_control(ip, port, nonce):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.sendto(nonce.encode("ascii"), (ip, port))
        return "sent"
    except OSError as exc:
        return repr(exc)
    finally:
        s.close()


def dns_control():
    try:
        socket.getaddrinfo("example.com", 80)
        return "resolved"
    except OSError as exc:
        return repr(exc)


def main() -> int:
    ip = lan_ip()
    report = {
        "probe": "external-udp-v1",
        "lan_ip": ip,
        "production_gate": "CLOSED",
        "controls": {},
        "sandbox": {},
        "receiver": {},
    }
    receiver = UdpReceiver()
    receiver.start()
    time.sleep(0.1)

    before = str(uuid.uuid4())[:16]
    report["controls"]["before_udp"] = udp_control(ip, receiver.port, before)
    report["controls"]["before_dns"] = dns_control()

    # 沙箱探针代码:_socket 原生路径,不经 shim
    probe = (
        "import json,_socket\n"
        "r={}\n"
        "for name,fam,ep in [\n"
        " ('udp_lan_v4',_socket.AF_INET,(%r,%d)),\n"
        " ('udp_external_v4',_socket.AF_INET,('8.8.8.8',53)),\n"
        " ('udp_external_v6',_socket.AF_INET6,('2606:4700:4700::1111',53,0,0))]:\n"
        " s=_socket.socket(fam,_socket.SOCK_DGRAM)\n"
        " try:\n"
        "  s.sendto(b%s,fam==_socket.AF_INET and ep or ep[:2]);r[name]={'outcome':'sent'}\n"
        " except OSError as e:r[name]={'outcome':'denied','winerror':getattr(e,'winerror',None),'err':e.__class__.__name__}\n"
        " finally:s.close()\n"
        "try:\n"
        " _socket.getaddrinfo('example.com',80);r['dns_os']={'outcome':'resolved'}\n"
        "except OSError as e:r['dns_os']={'outcome':'failed','errno':getattr(e,'errno',None),'err':e.__class__.__name__}\n"
        "print(json.dumps(r),flush=True)\n"
    ) % (ip, receiver.port, repr("probe-lan-" + before))

    cp = run_code(probe, mode="probe", timeout_ms=90000)
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

    # 收口:接收器应只收到 before/after 对照 nonce,不得收到沙箱 nonce
    time.sleep(1.5)
    after = str(uuid.uuid4())[:16]
    report["controls"]["after_udp"] = udp_control(ip, receiver.port, after)
    report["controls"]["after_dns"] = dns_control()
    time.sleep(1.0)
    receiver.close()
    got = [(payload, str(addr)) for payload, addr in receiver.received]
    report["receiver"]["all"] = got
    report["receiver"]["before_nonrecv"] = any(before in p for p, _ in got)
    report["receiver"]["after_received"] = any(after in p for p, _ in got)
    report["receiver"]["sandbox_nonce_received"] = any("probe-lan-" in p for p, _ in got)

    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("sandbox rc:", report["sandbox"]["rc"])
    print("sandbox results:", report["sandbox"].get("results"))
    print("receiver got:", got)
    print("sandbox nonce delivered to host:", report["receiver"]["sandbox_nonce_received"])
    print("evidence:", OUT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
