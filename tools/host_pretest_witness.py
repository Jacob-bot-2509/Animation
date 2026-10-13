"""Local host socket diagnostics for the named witness.

A local connect completion or refusal does not authenticate the witness.
A timeout leaves reachability unresolved. Receiver nonce evidence is required.
"""
from __future__ import annotations

from fractions import Fraction
import json
import socket
import sys
import time

WITNESS = "172.31.31.250"
TCP_PORT = 49002
UDP_PORT = 49001


def tcp_verdict(code):
    if code == 0:
        return "LOCAL_CONNECT_COMPLETED"
    if code == 10061:
        return "CONNECTION_REFUSED"
    if code == 10060:
        return "TIMEOUT_UNCONFIRMED"
    return "SOCKET_ERROR"


def elapsed_fields(started):
    elapsed = time.monotonic_ns() - started
    return {"elapsed_ns": elapsed, "elapsed_ms_exact": str(Fraction(elapsed, 1_000_000))}


def error_fields(exc):
    return {"error_type": type(exc).__name__, "detail": str(exc),
            "errno": exc.errno, "winerror": getattr(exc, "winerror", None)}


def tcp_probe():
    started = time.monotonic_ns()
    result = {"target": f"{WITNESS}:{TCP_PORT}", "receiver_delivery_verified": False}
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(5)
            code = sock.connect_ex((WITNESS, TCP_PORT))
        result.update(errno=code, outcome=tcp_verdict(code))
    except OSError as exc:
        result.update(error=error_fields(exc), errno=None,
                      outcome="TIMEOUT_UNCONFIRMED" if isinstance(exc, TimeoutError) else "SOCKET_ERROR")
    result.update(elapsed_fields(started))
    return result


def udp_probe():
    started = time.monotonic_ns()
    payload = b"pretest"
    result = {"target": f"{WITNESS}:{UDP_PORT}", "receiver_delivery_verified": False}
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(3)
            count = sock.sendto(payload, (WITNESS, UDP_PORT))
        result.update(sent=count == len(payload), bytes_sent=count,
                      outcome="LOCAL_SEND_COMPLETED" if count == len(payload) else "SHORT_SEND")
    except OSError as exc:
        result.update(sent=False, outcome="SOCKET_ERROR", error=error_fields(exc))
    result.update(elapsed_fields(started))
    return result


def main():
    tcp, udp = tcp_probe(), udp_probe()
    print(json.dumps({"tcp": tcp, "udp": udp, "verdict": tcp["outcome"],
                      "status": "DIAGNOSTIC_ONLY", "qualification": "NOT_ESTABLISHED",
                      "production_gate": "CLOSED", "full_surface_accepted": False}))
    return 2 if tcp["outcome"] == "SOCKET_ERROR" or not udp["sent"] else 0


if __name__ == "__main__":
    sys.exit(main())
