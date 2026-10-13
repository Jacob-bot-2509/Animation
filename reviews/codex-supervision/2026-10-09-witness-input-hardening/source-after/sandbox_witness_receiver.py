# -*- coding: utf-8 -*-
"""Controlled dual-protocol nonce witness. Default is PLAN; --serve is explicit.

Use separate IPv4/IPv6 runs; an IPv6 listener is IPv6-only. Logs and summaries
are exclusive new files, never an overwrite of historical evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import os
import platform
import queue
import re
import selectors
import socket
import sys
import threading
import time
import uuid
from pathlib import Path

SCHEMA = "sandbox-witness-receiver-v2"
MAX_PAYLOAD = 65535
MAX_CONNECTIONS = 64


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def implementation_identity():
    frozen = bool(getattr(sys, "frozen", False))
    path = Path(sys.executable if frozen else __file__).resolve()
    return {"kind": "frozen_executable" if frozen else "python_source",
            "path": str(path), "sha256": digest(path)}


def validate(bind, udp_port, tcp_port, seconds):
    address = ipaddress.ip_address(bind)
    for port in (udp_port, tcp_port):
        if type(port) is not int or (port != 0 and not 1024 <= port <= 65535):
            raise ValueError("Ports must be 0 (ephemeral) or 1024..65535")
    if type(seconds) is not int or not 20 <= seconds <= 900:
        raise ValueError("A bounded integer 20..900 second window is required")
    return socket.AF_INET6 if address.version == 6 else socket.AF_INET


def run(bind, udp_port, tcp_port, seconds, log_path, *, ready=None, stop=None):
    family = validate(bind, udp_port, tcp_port, seconds)
    log_path = Path(log_path).absolute()
    summary_path = log_path.with_suffix(log_path.suffix + ".summary.json")
    log_path.parent.mkdir(parents=True, exist_ok=True)
    # Reserve BOTH output names before opening any listener.
    with log_path.open("x", encoding="utf-8", newline="\n") as log:
        with summary_path.open("x", encoding="utf-8", newline="\n") as summary_file:
            return _collect(family, bind, udp_port, tcp_port, seconds, log,
                            summary_file, log_path, summary_path, ready, stop)


def _collect(family, bind, udp_port, tcp_port, seconds, log, summary_file,
             log_path, summary_path, ready, stop):
    selector = selectors.DefaultSelector()
    listeners = []
    pending = {}
    errors = []
    endpoints = {}
    tag = uuid.uuid4().hex
    identity = implementation_identity()
    seq = 0
    received = 0
    started = None
    deadline_reached = False
    interrupted = False

    def event(kind, **fields):
        nonlocal seq
        seq += 1
        row = {"schema": SCHEMA, "run_id": tag, "seq": seq,
               "utc_ns": time.time_ns(), "monotonic_ns": time.monotonic_ns(),
               "kind": kind, **fields}
        log.write(json.dumps(row, ensure_ascii=False) + "\n")
        log.flush()
        return row

    def fail(kind, exc=None, **fields):
        row = {"error_kind": kind, **fields}
        if exc is not None:
            row.update(error_type=type(exc).__name__, detail=str(exc),
                       errno=getattr(exc, "errno", None),
                       winerror=getattr(exc, "winerror", None))
        errors.append(row)
        event("error", **row)

    def payload(proto, peer, data, complete=True, **fields):
        nonlocal received
        received += 1
        valid = complete and bool(re.fullmatch(b"[0-9a-f]{32}", data))
        event("payload", protocol=proto, peer=list(peer),
              endpoint=endpoints[proto], bytes=len(data), payload_hex=data.hex(),
              capture_complete=complete, exact_nonce=valid,
              nonce=data.decode("ascii") if valid else None, **fields)

    def finish(conn, complete=True, **fields):
        state = pending.pop(conn)
        try:
            payload("tcp", state["peer"], bytes(state["data"]), complete, **fields)
        finally:
            selector.unregister(conn)
            conn.close()

    event("created", bind=bind, address_family=6 if family == socket.AF_INET6 else 4,
          ipv6_only=family == socket.AF_INET6, implementation=identity,
          argv=sys.argv, pid=os.getpid(), host=platform.node(),
          requested_seconds=seconds, log=str(log_path), summary=str(summary_path))
    try:
        for proto, port, kind in (("udp", udp_port, socket.SOCK_DGRAM),
                                  ("tcp", tcp_port, socket.SOCK_STREAM)):
            listener = socket.socket(family, kind)
            listeners.append(listener)
            if family == socket.AF_INET6:
                # No silent fallback to an unverified dual-stack setup.
                listener.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 1)
            listener.bind((bind, port))
            if proto == "tcp":
                listener.listen(16)
            listener.setblocking(False)
            endpoints[proto] = list(listener.getsockname())
            selector.register(listener, selectors.EVENT_READ, proto)
        started = time.monotonic_ns()
        deadline = started + seconds * 1_000_000_000
        row = event("listening", endpoints=endpoints, implementation=identity)
        print(json.dumps(row), flush=True)
        if ready is not None:
            ready(endpoints)
        while True:
            now = time.monotonic_ns()
            if now >= deadline:
                deadline_reached = True
                break
            if stop is not None and stop.is_set():
                fail("early_stop")
                break
            for key, _ in selector.select(min(1/5, (deadline - now)/1_000_000_000)):
                sock = key.fileobj
                try:
                    if key.data == "udp":
                        data, peer = sock.recvfrom(MAX_PAYLOAD)
                        payload("udp", peer, data)
                    elif key.data == "tcp":
                        conn, peer = sock.accept()
                        if len(pending) >= MAX_CONNECTIONS:
                            conn.close()
                            fail("connection_limit", max_connections=MAX_CONNECTIONS)
                            continue
                        conn.setblocking(False)
                        pending[conn] = {"peer": peer, "data": bytearray(),
                                         "deadline": time.monotonic_ns() + 3_000_000_000}
                        selector.register(conn, selectors.EVENT_READ, "client")
                    else:
                        state = pending[sock]
                        block = sock.recv(MAX_PAYLOAD + 1 - len(state["data"]))
                        if not block:
                            finish(sock)
                        else:
                            state["data"].extend(block)
                            if len(state["data"]) > MAX_PAYLOAD:
                                fail("tcp_payload_over_limit", peer=list(state["peer"]))
                                finish(sock, False, reason="payload_over_limit")
                except BlockingIOError:
                    continue
                except OSError as exc:
                    fail("socket_error", exc)
                    if sock in pending:
                        finish(sock, False, reason="socket_error")
                    else:
                        raise
            now = time.monotonic_ns()
            for conn, state in list(pending.items()):
                if now >= state["deadline"]:
                    fail("tcp_read_timeout", peer=list(state["peer"]))
                    finish(conn, False, reason="read_timeout")
    except KeyboardInterrupt:
        interrupted = True
        fail("interrupted")
    except Exception as exc:
        fail("collection_failure", exc)
    finally:
        for conn in list(pending):
            fail("pending_tcp_at_close", peer=list(pending[conn]["peer"]))
            finish(conn, False, reason="observation_closed")
        for listener in listeners:
            listener.close()
        selector.close()
    finished = time.monotonic_ns()
    try:
        unchanged = digest(identity["path"]) == identity["sha256"]
    except OSError as exc:
        unchanged = False
        fail("implementation_unreadable", exc)
    if not unchanged:
        fail("implementation_changed")
    complete = deadline_reached and not errors and unchanged
    event("closed", listeners_closed=all(s.fileno() == -1 for s in listeners),
          deadline_reached=deadline_reached, receiver_complete=complete)
    log.flush()
    os.fsync(log.fileno())
    result = {"schema": SCHEMA, "run_id": tag, "bind": bind,
              "address_family": 6 if family == socket.AF_INET6 else 4,
              "ipv6_only": family == socket.AF_INET6, "endpoints": endpoints,
              "implementation": identity, "implementation_unchanged": unchanged,
              "started_monotonic_ns": started, "finished_monotonic_ns": finished,
              "requested_seconds": seconds, "deadline_reached": deadline_reached,
              "interrupted": interrupted, "errors": errors, "records": received,
              "listeners_closed": all(s.fileno() == -1 for s in listeners),
              "receiver_complete": complete, "log": str(log_path),
              "log_sha256": digest(log_path), "summary": str(summary_path),
              "certificate_written": False, "production_gate": "CLOSED"}
    json.dump(result, summary_file, ensure_ascii=False, indent=2)
    summary_file.write("\n")
    summary_file.flush()
    os.fsync(summary_file.fileno())
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return 0 if complete else 2


def selftest(output):
    """Host-only TCP/UDP x IPv4/IPv6 health test, never sandbox acceptance."""
    output = Path(output).absolute()
    output.mkdir(parents=True, exist_ok=True)
    cases = []
    threads = []
    failures = []
    for bind in ("127.0.0.1", "::1"):
        ready = queue.Queue()
        log = output / ("selftest-" + uuid.uuid4().hex + ".jsonl")
        case = {"bind": bind, "log": str(log)}
        cases.append(case)

        def worker(bind=bind, log=log, ready=ready, case=case):
            try:
                case["rc"] = run(bind, 0, 0, 20, log, ready=ready.put)
            except Exception as exc:
                case["exception"] = repr(exc)
                ready.put(None)
        thread = threading.Thread(target=worker)
        thread.start()
        threads.append(thread)
        endpoints = ready.get(timeout=10)
        if endpoints is None:
            failures.append(bind)
            continue
        family = socket.AF_INET6 if ":" in bind else socket.AF_INET
        case["nonces"] = {}
        for proto in ("udp", "tcp"):
            nonce = uuid.uuid4().hex
            case["nonces"][proto] = nonce
            with socket.socket(family, socket.SOCK_DGRAM if proto == "udp" else socket.SOCK_STREAM) as sender:
                sender.settimeout(3)
                endpoint = tuple(endpoints[proto])
                if proto == "udp":
                    sender.sendto(nonce.encode("ascii"), endpoint)
                else:
                    sender.connect(endpoint)
                    sender.sendall(nonce[:7].encode("ascii"))
                    sender.sendall(nonce[7:].encode("ascii"))
                    sender.shutdown(socket.SHUT_WR)
    for thread in threads:
        thread.join(timeout=30)
        if thread.is_alive():
            failures.append("collector_did_not_stop")
    for case in cases:
        if case.get("rc") != 0:
            failures.append(case["bind"])
            continue
        rows = [json.loads(line) for line in Path(case["log"]).read_text("utf-8").splitlines()]
        observed = {r["protocol"]: r["nonce"] for r in rows if r["kind"] == "payload" and r["exact_nonce"]}
        if observed != case["nonces"]:
            failures.append(case["bind"])
    result = {"scope": "Host loopback self-test only; no sandbox/external evidence",
              "cases": cases, "failures": failures, "full_surface_accepted": False}
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return 0 if not failures else 2


def validate_serving_bind(bind):
    address = ipaddress.ip_address(bind)
    if (address.is_unspecified or address.is_multicast or address.is_loopback
            or address.is_link_local or address.is_reserved):
        raise ValueError("--serve requires a specific unicast witness address")
    return str(address)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--serve", action="store_true")
    parser.add_argument("--bind", help="Explicit local literal address; IPv6 is IPv6-only")
    parser.add_argument("--udp-port", type=int, default=49001)
    parser.add_argument("--tcp-port", type=int, default=49002)
    parser.add_argument("--seconds", type=int, default=300)
    parser.add_argument("--log", type=Path)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--output", type=Path, default=Path("witness-selftest"))
    args = parser.parse_args(argv)
    if args.selftest and args.serve:
        parser.error("--selftest and --serve are mutually exclusive")
    if args.selftest:
        return selftest(args.output)
    if not args.serve:
        print("PLAN ONLY: no listener opened; use --serve --bind ADDRESS --log NEW_LOG")
        return 3
    if args.bind is None or args.log is None:
        parser.error("--serve requires --bind and a new --log path")
    try:
        bind = validate_serving_bind(args.bind)
        if args.udp_port == 0 or args.tcp_port == 0 or args.udp_port == args.tcp_port:
            raise ValueError("--serve requires distinct nonzero UDP/TCP ports")
        return run(bind, args.udp_port, args.tcp_port, args.seconds, args.log)
    except (OSError, ValueError) as exc:
        print(json.dumps({"status": "FAILED", "error_type": type(exc).__name__,
                          "detail": str(exc), "certificate_written": False}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
