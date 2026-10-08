"""Adapt the independent v2 tests to the reviewed v2.1 start-event protocol."""
import hashlib
from pathlib import Path

old = Path(r"D:\code\output\claude-supervision\network-review-v2-2026-10-04\check_v2.py")
source = old.read_text(encoding="utf-8")
def replace_once(before, after):
    global source
    if source.count(before) != 1:
        raise RuntimeError("Review harness shape changed: " + before[:70])
    source = source.replace(before, after, 1)

replace_once('"_attempt", "_server_tcp", "_assert_json_safe"}',
             '"_attempt", "_server_tcp", "_server_udp", "_pth_ok", "_assert_json_safe"}')
replace_once('SERVER_WAIT_S=5,', 'SERVER_WAIT_S=20,')
replace_once('cap_api_ok=True, shim_absent=True, client_file_ok=True,',
             'cap_api_ok=True, shim_absent=True, client_file_ok=True, pth_ok=True, socket_ok=True,')
replace_once('class Clock:', '''class StartEvent:
    def set(self): pass
    def wait(self, timeout=None): return True
class Clock:''')
replace_once('if expired:\n            result.update(finalized=True, timeout=True)\n            clock.value += 10',
             'if expired:\n            result.update(finalized=True, server_error="start event not triggered")\n            clock.value += 31')
replace_once('return Thread(result, expired), [12345], t0',
             'return Thread(result, expired), [12345], t0, StartEvent()')
replace_once('"OUTCOME=net_error ERR_WINERROR=10013 T_DELTA=0\\n")',
             '"CLIENT_FILE_SHA256=abc123\\nRUNTIME_EXE_SHA256=def456\\n"\n                  "OUTCOME=net_error ERR_WINERROR=10013 T_DELTA=0\\n")')
replace_once('ns.update(time=clock, _spawn_server=spawn, subprocess=fake_subprocess,',
             'ns.update(time=clock, NET_RUNTIME=runtime.parent, _spawn_server=spawn, subprocess=fake_subprocess,')
replace_once('{"client_file_sha256": "unverified-nonempty",\n                                    "runtime_python_sha256": "unverified-nonempty"}',
             '{"client_file_sha256": "abc123", "runtime_python_sha256": "def456", "pth_ok": True}')
replace_once('types.SimpleNamespace(set=lambda: None), 5)',
             'types.SimpleNamespace(set=lambda: None), StartEvent(), 20)')
replace_once('payload = dict(source_sha256=', '''# Additional protocol checks exercise the actual server functions, not just flags.
for name, content, expected in [
    ("pth_clean", "Lib\\nDLLs\\n.\\n", True),
    ("pth_site_injection", "Lib\\nimport site\\n", False),
    ("pth_external_path", "Lib\\nD:\\\\Python\\n", False),
    ("pth_missing", None, False),
]:
    add(name, ns["_pth_ok"](content), expected)

for fn_name in ["_server_tcp", "_server_udp"]:
    srv.closed = False
    timeout_result = {}
    ns["socket"].SOCK_DGRAM = 2
    ns[fn_name]("127.0.0.1", [None], timeout_result,
                types.SimpleNamespace(set=lambda: None),
                types.SimpleNamespace(wait=lambda timeout: False), 20)
    add(fn_name + "_start_event_timeout_fails_and_closes",
        bool(timeout_result.get("server_error")) and timeout_result.get("finalized") is True
        and srv.closed, True)

# Hash mismatch must make the orchestration reject the client.
record = fake_attempt("hash_mismatch")
attempts["hash_mismatch_baseline"] = record
add("orchestration_valid_blocked_baseline", record["verdict"]["verdict"], "PASS")
original_parse = ns["_parse_client"]
def mismatched_parse(out):
    parsed = original_parse(out)
    parsed["client_file_sha"] = "different"
    return parsed
ns["_parse_client"] = mismatched_parse
record = fake_attempt("hash_mismatch")
attempts["hash_mismatch"] = record
add("orchestration_client_hash_mismatch", record["verdict"]["verdict"], "UNVERIFIED")
ns["_parse_client"] = original_parse

payload = dict(source_sha256=''')
replace_once('"independent-v2-results.json"', '"independent-v21-results.json"')
exec(compile(source, str(Path(__file__)), "exec"))
