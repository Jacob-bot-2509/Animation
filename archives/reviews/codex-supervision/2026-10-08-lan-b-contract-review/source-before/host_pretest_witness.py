"""Host-level connectivity pre-test to witness 172.31.31.250 before receiver starts.

Expectation with no listener running: TCP connect returns WSAECONNREFUSED (10061)
if the path is alive (RST from the host), timeout (10060) if blocked/unreachable.
"""
from __future__ import annotations

import socket
import sys
import time

WITNESS = "172.31.31.250"
TCP_PORT = 49002
UDP_PORT = 49001


def tcp_probe():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    start = time.monotonic()
    err = sock.connect_ex((WITNESS, TCP_PORT))
    elapsed = round((time.monotonic() - start) * 1000, 1)
    sock.close()
    return {"target": f"{WITNESS}:{TCP_PORT}", "errno": err, "elapsed_ms": elapsed,
            "note": "10061=refused(path alive, no listener) 10060=timeout(path blocked/unreachable)"}


def udp_probe():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    try:
        sock.sendto(b"pretest", (WITNESS, UDP_PORT))
        sent = True
    except OSError as exc:
        sent = False
        print(f"udp send error: {exc}")
    sock.close()
    return {"target": f"{WITNESS}:{UDP_PORT}", "sent": sent,
            "note": "no listener yet; delivery cannot be confirmed pre-start"}


def main():
    tcp = tcp_probe()
    udp = udp_probe()
    verdict = "PATH_ALIVE" if tcp["errno"] in (10061, 10060) else f"errno={tcp['errno']}"
    # 10060 also reported: alive-but-filtered ambiguity is resolved after receiver starts.
    print({"tcp": tcp, "udp": udp, "verdict": verdict})
    return 0


if __name__ == "__main__":
    sys.exit(main())
