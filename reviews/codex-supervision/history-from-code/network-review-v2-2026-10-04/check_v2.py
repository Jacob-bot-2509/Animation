"""Review selected AST functions with fake I/O; no native networking or ACL."""
import ast
import hashlib
import json
import os
import re
import sys
import types
from pathlib import Path

OUT = Path(__file__).resolve().parent
SOURCE = Path(r"D:\Animation-Model-Training\reviews\2026-10-04-acceptance-support\network_acceptance.py")
raw = SOURCE.read_bytes()
tree = ast.parse(raw.decode("utf-8-sig"))
names = {"_judge_attempt", "_negative_regressions", "_recv_evidence",
         "_json_roundtrip_ok", "_parse_client", "_normpath", "_server_snapshot",
         "_attempt", "_server_tcp", "_assert_json_safe"}
ns = dict(json=json, os=os, re=re, Path=Path, WSAEACCES=10013,
          WSAECONNREFUSED=10061, SERVER_WAIT_S=5,
          threading=types.SimpleNamespace(Event=object),
          subprocess=__import__("subprocess"), socket=__import__("socket"))
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n, ast.FunctionDef)
                             and n.name in names], type_ignores=[]), str(SOURCE), "exec"), ns)
baseline_ctrl = dict(spawned=True, rc=0, timed_out=False, delivered=True, nonce_match=True)
baseline_sb = dict(spawned=True, rc=0, timed_out=False, delivered=False,
                   server_ok=True, recv_final=True, token29=True, cap_count=0,
                   cap_api_ok=True, shim_absent=True, client_file_ok=True,
                   outcome="net_error", err_winerror=10013)
cases = []
def add(name, actual, expected):
    cases.append(dict(name=name, actual=actual, expected=expected, holds=actual == expected))

matrix = [
    ("nonzero_exit", {}, {"rc": 7}, "UNVERIFIED"),
    ("not_spawned", {}, {"spawned": False}, "UNVERIFIED"),
    ("receive_unknown", {}, {"delivered": None}, "UNVERIFIED"),
    ("receiver_failure", {}, {"recv_final": False}, "UNVERIFIED"),
    ("tcp_sent_no_receive", {}, {"outcome": "sent_ok", "err_winerror": None}, "UNVERIFIED"),
    ("udp_sent_no_receive", {}, {"outcome": "sent_ok", "err_winerror": None}, "UNVERIFIED"),
    ("delivered_with_failed_control", {"delivered": False}, {"delivered": True}, "FAIL"),
    ("valid_blocked_baseline", {}, {}, "PASS"),
    ("refused", {}, {"err_winerror": 10061}, "UNVERIFIED"),
    ("token_query_failed", {}, {"token29": False}, "UNVERIFIED"),
]
for name, c, s, expected in matrix:
    add(name, ns["_judge_attempt"](dict(baseline_ctrl, **c), dict(baseline_sb, **s))["verdict"], expected)

class Clock:
    def __init__(self): self.value = 0
    def monotonic(self): self.value += 1; return self.value
class Thread:
    def __init__(self, result, expired=False): self.result=result; self.expired=expired
    def join(self, timeout=None):
        self.result["finalized"] = True
        if self.result.get("received") is None: self.result["timeout"] = True
    def is_alive(self): return not self.expired and not self.result.get("finalized", False)

def fake_attempt(mode):
    clock = Clock()
    server_count = 0
    sb_state = {}
    runtime = Path(r"D:\code\output\claude-supervision\network-review-v2-2026-10-04\fake-runtime\python.exe")
    socket_path = str(runtime.parent / "Lib/socket.py")
    if mode == "socket_outside_runtime": socket_path = r"D:\Python\Lib\socket.py"
    def spawn(transport, host, result):
        nonlocal server_count
        server_count += 1
        t0 = clock.monotonic()
        result["listening"] = True
        result["received"] = b"control-nonce" if server_count == 1 else None
        expired = server_count == 2 and mode == "listener_expired_before_launch"
        if expired:
            result.update(finalized=True, timeout=True)
            clock.value += 10
        if server_count == 2: sb_state.update(result)
        return Thread(result, expired), [12345], t0
    client_out = ("TOKEN_IS_APPCONTAINER=1 ok=1/1\n"
                  "CAPABILITY_COUNT=0 CAP_API_OK=1 CAP_NEEDED=8\n"
                  "SHIM_ABSENT=True\nSITE_ABSENT=True\n"
                  f"SYS_EXECUTABLE={runtime}\nSOCKET_FILE={socket_path}\n"
                  "OUTCOME=net_error ERR_WINERROR=10013 T_DELTA=0\n")
    def run_sb(*args, **kw):
        return types.SimpleNamespace(stdout=client_out.encode(), stderr=b"", returncode=0)
    fake_subprocess = types.SimpleNamespace(
        run=lambda *a, **kw: types.SimpleNamespace(stdout=b"control", stderr=b"", returncode=0),
        TimeoutExpired=__import__("subprocess").TimeoutExpired)
    ns.update(time=clock, _spawn_server=spawn, subprocess=fake_subprocess,
              ac=types.SimpleNamespace(run_appcontainer=run_sb))
    return ns["_attempt"]("tcp", "127.0.0.1", OUT / "fake-client.py", runtime,
                          OUT, {}, {"client_file_sha256": "unverified-nonempty",
                                    "runtime_python_sha256": "unverified-nonempty"},
                          "control-nonce", "sandbox-nonce")

attempts = {}
for mode in ["socket_outside_runtime", "listener_expired_before_launch"]:
    record = fake_attempt(mode)
    attempts[mode] = record
    add(mode, record["verdict"]["verdict"], "UNVERIFIED")

# Force the existing TCP receive-error branch without opening a real socket.
class Conn:
    closed = False
    def settimeout(self, value): pass
    def recv(self, size): raise OSError(10054, "synthetic receive failure")
    def close(self): self.closed = True
conn = Conn()
class Server:
    closed = False
    def bind(self, endpoint): pass
    def getsockname(self): return ("127.0.0.1", 12345)
    def listen(self, count): pass
    def settimeout(self, value): pass
    def accept(self): return conn, ("127.0.0.1", 12346)
    def close(self): self.closed = True
srv = Server()
ns["socket"] = types.SimpleNamespace(AF_INET=2, AF_INET6=23, SOCK_STREAM=1,
                                     socket=lambda *a: srv, timeout=TimeoutError)
result = {}
ns["_server_tcp"]("127.0.0.1", [None], result,
                  types.SimpleNamespace(set=lambda: None), 5)
add("tcp_receive_error_closes_both_sockets", conn.closed and srv.closed, True)
ns["_assert_json_safe"]({"server": ns["_server_snapshot"]({"received": b"\x00\xffnonce"})}, "test")
payload = dict(source_sha256=hashlib.sha256(raw).hexdigest(),
               internal_regressions=ns["_negative_regressions"](),
               json_roundtrip=ns["_json_roundtrip_ok"](), independent_cases=cases,
               independent_holds=sum(c["holds"] for c in cases), independent_total=len(cases),
               fake_attempt_evidence=attempts,
               receive_error_cleanup=dict(conn_closed=conn.closed, server_closed=srv.closed, result=result),
               scope="AST functions with fake I/O only; no sockets, profile, native process or ACL created")
(OUT / "source-snapshot.py").write_bytes(raw)
(OUT / "independent-v2-results.json").write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps({k:v for k,v in payload.items() if k != "fake_attempt_evidence"}, indent=2, ensure_ascii=False))
sys.exit(0 if all(c["holds"] for c in cases) else 1)
