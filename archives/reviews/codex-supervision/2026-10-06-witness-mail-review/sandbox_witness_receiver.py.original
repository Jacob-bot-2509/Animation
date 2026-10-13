# -*- coding: utf-8 -*-
"""沙箱外部证人接收器:在另一台机器(校园网电脑/云服务器)上运行,
监听 UDP/TCP,记录每个收到的包(时间戳/来源/内容),退出时写带SHA的证据日志。

用法(纯标准库,Windows/Linux/macOS/Termux 通用):
  python sandbox_witness_receiver.py --udp-port 49001 --tcp-port 49002 --log witness.jsonl
  python sandbox_witness_receiver.py --selftest   # 本机自测收发通路

证据日志每行一个JSON事件,退出后整体SHA绑定,供独立复核。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import socket
import sys
import threading
import time
from pathlib import Path


def log_event(log, kind, **fields):
    event = {"t": time.time(), "kind": kind}
    event.update(fields)
    log.append(event)
    print(json.dumps(event, ensure_ascii=False), flush=True)


def udp_loop(bind, port, log, stop):
    s = socket.socket(socket.AF_INET6 if ":" in bind else socket.AF_INET,
                      socket.SOCK_DGRAM)
    if ":" in bind:
        try:
            s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        except OSError:
            pass
    s.bind((bind, port))
    s.settimeout(0.5)
    log_event(log, "listening", proto="udp", bind=f"{bind}:{port}")
    while not stop.is_set():
        try:
            data, addr = s.recvfrom(4096)
        except socket.timeout:
            continue
        except OSError:
            break
        log_event(log, "udp", src=f"{addr[0]}:{addr[1]}", payload=data.decode("utf-8", "replace"))
    s.close()


def tcp_loop(bind, port, log, stop):
    s = socket.socket(socket.AF_INET6 if ":" in bind else socket.AF_INET,
                      socket.SOCK_STREAM)
    if ":" in bind:
        try:
            s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        except OSError:
            pass
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((bind, port))
    s.listen(8)
    s.settimeout(0.5)
    log_event(log, "listening", proto="tcp", bind=f"{bind}:{port}")
    while not stop.is_set():
        try:
            conn, addr = s.accept()
        except socket.timeout:
            continue
        except OSError:
            break
        try:
            conn.settimeout(3)
            data = conn.recv(4096)
            log_event(log, "tcp", src=f"{addr[0]}:{addr[1]}",
                      payload=data.decode("utf-8", "replace"))
        except OSError:
            pass
        finally:
            conn.close()
    s.close()


def selftest():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.setblocking(False)
    s2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s2.sendto(b"selftest-nonce", ("127.0.0.1", port))
    s2.close()
    got = []
    deadline = time.time() + 1.0
    while time.time() < deadline:
        try:
            data, _addr = s.recvfrom(4096)
            got.append(data.decode())
        except BlockingIOError:
            time.sleep(0.05)
        except OSError:
            break
    s.close()
    ok = "selftest-nonce" in got
    print("selftest:", "OK 收发通路正常" if ok else "FAILED")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--udp-port", type=int, default=49001)
    ap.add_argument("--tcp-port", type=int, default=49002)
    ap.add_argument("--bind", default="0.0.0.0", help="或 :: 双栈监听")
    ap.add_argument("--log", type=Path, default=Path("witness.jsonl"))
    ap.add_argument("--seconds", type=float, default=0.0,
                    help="运行N秒后自动停止并写证据(0=等Ctrl+C)")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    log = []
    stop = threading.Event()
    threads = [
        threading.Thread(target=udp_loop, args=(args.bind, args.udp_port, log, stop), daemon=True),
        threading.Thread(target=tcp_loop, args=(args.bind, args.tcp_port, log, stop), daemon=True),
    ]
    for t in threads:
        t.start()
    log_event(log, "started", udp_port=args.udp_port, tcp_port=args.tcp_port)
    print("按 Ctrl+C 结束,证据将写入", args.log, flush=True)
    try:
        deadline = time.time() + args.seconds if args.seconds > 0 else None
        while deadline is None or time.time() < deadline:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    stop.set()
    for t in threads:
        t.join(timeout=2)
    lines = [json.dumps(e, ensure_ascii=False) for e in log]
    raw = ("\n".join(lines) + "\n").encode("utf-8")
    args.log.write_bytes(raw)
    sha = hashlib.sha256(raw).hexdigest()
    print("events:", len(log))
    print("log:", args.log)
    print("log_sha256:", sha)
    return 0


if __name__ == "__main__":
    sys.exit(main())
