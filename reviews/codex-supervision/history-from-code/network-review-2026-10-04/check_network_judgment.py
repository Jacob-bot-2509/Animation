"""Read-only AST review of Claude's network judgment; never run its main."""
import ast
import hashlib
import json
import sys
from pathlib import Path

SOURCE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    r"D:\Animation-Model-Training\reviews\2026-10-04-acceptance-support\network_acceptance.py")
OUT = Path(__file__).resolve().parent
raw = SOURCE.read_bytes()
tree = ast.parse(raw.decode("utf-8-sig"))
judge = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_judge_attempt")
ns = {"WSAEACCES": 10013, "WSAECONNREFUSED": 10061}
exec(compile(ast.Module(body=[judge], type_ignores=[]), str(SOURCE), "exec"), ns)
fn = ns["_judge_attempt"]
control = dict(spawned=True, rc=0, timed_out=False, delivered=True, nonce_match=True)
sandbox = dict(spawned=True, rc=0, timed_out=False, delivered=False,
               token29=True, cap_count=0, shim_absent=True,
               outcome="net_error", err_winerror=10013,
               server={"received": None, "timeout": True})
cases = [
    ("sandbox_nonzero_exit", control, dict(sandbox, rc=7), "UNVERIFIED"),
    ("sandbox_not_spawned", control, dict(sandbox, spawned=False), "UNVERIFIED"),
    ("receiver_unknown", control, dict(sandbox, delivered=None), "UNVERIFIED"),
    ("receiver_failure", control, dict(sandbox, server={"server_error": 10038}), "UNVERIFIED"),
    ("tcp_sent_without_receive", control,
     dict(sandbox, outcome="sent_ok", err_winerror=None, transport="tcp"), "UNVERIFIED"),
    ("udp_send_no_explicit_block", control,
     dict(sandbox, outcome="sent_ok", err_winerror=None, transport="udp"), "UNVERIFIED"),
    ("delivered_despite_invalid_control", dict(control, delivered=False),
     dict(sandbox, delivered=True), "FAIL"),
    ("blocked_baseline", control, sandbox, "PASS"),
    ("refused_connection", control, dict(sandbox, err_winerror=10061), "UNVERIFIED"),
    ("probe_token_failure", control, dict(sandbox, token29=False), "UNVERIFIED"),
]
results = []
for name, c, s, expected in cases:
    try:
        actual = fn(c, s)
        holds = actual.get("verdict") == expected
    except Exception as exc:
        actual = {"exception": repr(exc)}
        holds = False
    results.append(dict(name=name, expected=expected, actual=actual, holds=holds))

client_node = next(n for n in tree.body if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == "_CLIENT" for t in n.targets))
client = ast.literal_eval(client_node.value)
compile(client, "<client-read-only>", "exec")
try:
    json.dumps({"control": {"server": {"received": b"random-control-nonce"}}})
    serialization = {"supported": True}
except TypeError as exc:
    serialization = {"supported": False, "error": str(exc)}

hashes = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in [
    SOURCE,
    Path(r"D:\Animation-Model-Training\src\animtrain\appcontainer.py"),
    Path(r"D:\Animation-Model-Training\src\animtrain\win_job.py"),
    Path(r"D:\Animation-Model-Training\tests\test_appcontainer_lifecycle.py"),
    Path(r"D:\Animation-Model-Training\tests\test_win_job_cleanup.py"),
    Path(r"D:\Animation-Model-Training\src\animtrain\render_gate.py"),
]}
payload = {"reviewed_source_sha256": hashlib.sha256(raw).hexdigest(),
           "cases": results, "holds": sum(r["holds"] for r in results),
           "total": len(results), "raw_bytes_serialization": serialization,
           "client_compiles": True, "token_groups_class2_used": "GetTokenInformation(h, 2," in client,
           "source_hashes": hashes,
           "scope": "AST-only; no client/server, profile, ACL or child process created"}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "reviewed-network-source.py").write_bytes(raw)
(OUT / "independent-judgment-results.json").write_text(
    json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(payload, indent=2, ensure_ascii=False))
sys.exit(0 if all(r["holds"] for r in results) else 1)
