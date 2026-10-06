# -*- coding: utf-8 -*-
"""沙箱外部/LAN 隔离正式测试驱动(训练机侧)。
严格按 Codex 协议:
  - 每个协议/地址族三个不同 32 位十六进制 nonce:before / sandbox / after
  - 宿主 before/after 在相同协议端点精确送达(健康对照)
  - 沙箱尝试经 AppContainer 生产传输(run_code mode=probe),保留完整 parent 证据
  - 沙箱尝试后至少 20 秒完整观察,after 在该窗口内
  - 证据 JSON 独立新建,绝不覆盖
用法:
  python tools/sandbox_external_test_driver.py --bind <证人地址> --round <名字> --out <目录>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import socket
import subprocess
import sys
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def send_udp(ep, payload, family, timeout=4):
    s = socket.socket(family, socket.SOCK_DGRAM)
    s.settimeout(timeout)
    try:
        s.sendto(payload, ep)
        return {"outcome": "sent"}
    except OSError as exc:
        return {"outcome": "error", "err": type(exc).__name__,
                "winerror": getattr(exc, "winerror", None)}
    finally:
        s.close()


def send_tcp(ep, payload, family, timeout=6):
    s = socket.socket(family, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect(ep)
        s.sendall(payload)
        s.shutdown(socket.SHUT_WR)  # 发完正常关闭发送端
        return {"outcome": "connected"}
    except OSError as exc:
        return {"outcome": "error", "err": type(exc).__name__,
                "winerror": getattr(exc, "winerror", None)}
    finally:
        s.close()


def tracert(ip, family, out_dir=None, tag="route"):
    args = ["tracert", "-d", "-h", "4", "-w", "500", ip]
    if family == socket.AF_INET6:
        args.insert(1, "-6")
    try:
        cp = subprocess.run(args, capture_output=True, timeout=30)  # bytes,防GBK解码炸
        raw = cp.stdout or b""
        record = {"rc": cp.returncode, "stderr": (cp.stderr or b"")[:200].decode("gbk", "replace")}
        if out_dir is not None:
            f = out_dir / f"{tag}-{uuid.uuid4().hex}.txt"
            f.write_bytes(raw + b"\n")
            record["path"] = str(f)
            record["sha256"] = hashlib.sha256(raw).hexdigest()
        record["out"] = raw[:800].decode("gbk", "replace")
        return record
    except subprocess.TimeoutExpired:
        return {"rc": "timeout", "out": ""}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bind", required=True, help="证人地址(本轮绑定字面值)")
    ap.add_argument("--udp-port", type=int, default=49001)
    ap.add_argument("--tcp-port", type=int, default=49002)
    ap.add_argument("--round", required=True, help="具名轮次,如 d9-lan-v4 / ext-v6")
    ap.add_argument("--out", type=Path, default=ROOT / "reviews/2026-10-06-sandbox-external-tests")
    args = ap.parse_args(argv)

    family = socket.AF_INET6 if ":" in args.bind else socket.AF_INET
    ep_udp = (args.bind, args.udp_port)
    ep_tcp = (args.bind, args.tcp_port)
    out_dir = args.out
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"driver-{args.round}-{uuid.uuid4().hex}.json"
    if out_file.exists():
        raise ValueError("preserve previous evidence")

    nonces = {proto: {phase: uuid.uuid4().hex for phase in ("before", "sandbox", "after")}
              for proto in ("udp", "tcp")}
    report = {
        "round": args.round,
        "endpoint": {"bind": args.bind, "udp_port": args.udp_port,
                     "tcp_port": args.tcp_port, "family": str(family)},
        "host_identity": {"hostname": socket.gethostname(), "os": platform.platform(),
                          "python": sys.version},
        "nonces": nonces,
        "started_utc": time.time(),
        "phases": {},
    }
    report["route"] = tracert(args.bind, family, out_dir=out_dir, tag=f"route-{args.round}")

    # 拓扑证据:发送侧 IPv6 接口清单(Get-NetIPAddress 原始输出,供 ipv4-joint topology.json)
    try:
        cp_if = subprocess.run(
            ["powershell", "-NoProfile", "-Command",
             "Get-NetIPAddress -AddressFamily IPv6 | Select-Object IPAddress,PrefixLength | ConvertTo-Json -Compress"],
            capture_output=True, timeout=60)  # bytes,防GBK解码炸
        iface_raw = cp_if.stdout or b""
        iface_file = out_dir / f"interfaces-{args.round}-{uuid.uuid4().hex}.txt"
        iface_file.write_bytes(iface_raw + b"\n")
        report["sender_interfaces"] = {"path": str(iface_file),
                                       "sha256": hashlib.sha256(iface_raw).hexdigest(),
                                       "rc": cp_if.returncode,
                                       "stderr": (cp_if.stderr or b"")[:200].decode("gbk", "replace"),
                                       "command": "Get-NetIPAddress -AddressFamily IPv6 | Select-Object IPAddress,PrefixLength | ConvertTo-Json -Compress"}
    except Exception as exc:
        report["sender_interfaces"] = {"error": repr(exc)}

    def phase(name, fn):
        t0 = time.time()
        result = fn()
        report["phases"][name] = {"result": result,
                                  "started_utc": t0, "finished_utc": time.time()}

    # BEFORE:宿主健康对照(精确 nonce 送达)
    phase("before_udp", lambda: send_udp(ep_udp, nonces["udp"]["before"].encode(), family))
    phase("before_tcp", lambda: send_tcp(ep_tcp, nonces["tcp"]["before"].encode(), family))

    # SANDBOX:AppContainer 生产传输内的尝试
    from animtrain.sandbox_execution import run_code
    probe = r'''
import json,_socket,time
r={}
ep_udp=(__BIND__,__UDP_PORT__)
ep_tcp=(__BIND__,__TCP_PORT__)
nonce_udp=__NONCE_UDP__
nonce_tcp=__NONCE_TCP__
fam=_socket.AF_INET6 if ":" in __BIND__ else _socket.AF_INET
s=_socket.socket(fam,_socket.SOCK_DGRAM);s.settimeout(3)
try:
 s.sendto(nonce_udp,ep_udp);r["udp"]={"outcome":"sent"}
except OSError as e:r["udp"]={"outcome":"denied","winerror":getattr(e,"winerror",None),"err":type(e).__name__}
finally:s.close()
s=_socket.socket(fam,_socket.SOCK_STREAM);s.settimeout(6)
try:
 s.connect(ep_tcp);s.sendall(nonce_tcp);r["tcp"]={"outcome":"connected"}
except OSError as e:r["tcp"]={"outcome":"denied","winerror":getattr(e,"winerror",None),"err":type(e).__name__}
finally:s.close()
print(json.dumps(r),flush=True)
'''.replace("__BIND__", repr(args.bind)) \
   .replace("__UDP_PORT__", str(args.udp_port)) \
   .replace("__TCP_PORT__", str(args.tcp_port)) \
   .replace("__NONCE_UDP__", repr(nonces["udp"]["sandbox"].encode())) \
   .replace("__NONCE_TCP__", repr(nonces["tcp"]["sandbox"].encode()))
    t0 = time.time()
    cp = run_code(probe, mode="probe", timeout_ms=120000)
    report["sandbox"] = {
        "rc": cp["rc"],
        "stdout": cp["stdout"].strip(),
        "stderr": cp["stderr"].strip()[:1000],
        "work": cp["work"],
        "source_sha256": cp["source_sha256"],
        "command": cp["command"],
        "parent_evidence": cp["parent_evidence"],
        "started_utc": t0, "finished_utc": time.time(),
    }
    try:
        report["sandbox"]["results"] = json.loads(cp["stdout"].strip().splitlines()[-1])
    except Exception:
        pass

    # 沙箱尝试后 ≥20 秒完整观察
    observe_seconds = 21
    time.sleep(observe_seconds)
    report["observation_seconds"] = observe_seconds

    # AFTER:宿主健康对照(在观察窗内)
    phase("after_udp", lambda: send_udp(ep_udp, nonces["udp"]["after"].encode(), family))
    phase("after_tcp", lambda: send_tcp(ep_tcp, nonces["tcp"]["after"].encode(), family))

    report["finished_utc"] = time.time()
    raw = json.dumps(report, ensure_ascii=False, indent=2).encode("utf-8")
    out_file.write_bytes(raw + b"\n")
    print("round:", args.round)
    print("before_udp:", report["phases"]["before_udp"]["result"])
    print("before_tcp:", report["phases"]["before_tcp"]["result"])
    print("sandbox rc:", cp["rc"], "| results:", report["sandbox"].get("results"))
    print("after_udp:", report["phases"]["after_udp"]["result"])
    print("after_tcp:", report["phases"]["after_tcp"]["result"])
    print("driver evidence:", out_file)
    print("driver sha256:", hashlib.sha256(raw).hexdigest())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
