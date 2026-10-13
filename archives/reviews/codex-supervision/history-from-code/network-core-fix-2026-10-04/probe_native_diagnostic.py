"""Native diagnostic prototype using an existing granted runtime and profile."""
import hashlib
import importlib.util
import json
import sys
import uuid
from pathlib import Path

OUT = Path(__file__).resolve().parent
PROJECT = Path(r"D:\Animation-Model-Training")
SUPPORT = PROJECT / "reviews/2026-10-04-acceptance-support"
SCRIPT = SUPPORT / "network_acceptance.py"
EXPECTED = "4559e077d9a0d06ddb012e912866fb026dc1cbd19d65b76f239b9cc5a24414b7"
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
if sha(SCRIPT) != EXPECTED: raise RuntimeError("Reviewed script changed")
baseline = json.loads((SUPPORT / "net-evidence/network-accept-results-acd319b3f814.json").read_text(encoding="utf-8"))
work = Path(baseline["work"])
runtime = Path(baseline["runtime"])
manifest = baseline["runtime_copy"]["src_manifest"]
before = {rel: sha(runtime.parent / rel) for rel in manifest}
if before != manifest: raise RuntimeError("Runtime integrity failed")
spec = importlib.util.spec_from_file_location("reviewed_network_probe", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
diagnostic_code = '''
import json
diag = {'server': host, 'return_code': None, 'netiso_error': None}
try:
    fw = ctypes.WinDLL('Firewallapi.dll', use_last_error=True)
    fn = fw.NetworkIsolationDiagnoseConnectFailureAndGetInfo
    fn.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(ctypes.c_int)]
    fn.restype = wintypes.DWORD
    error_type = ctypes.c_int(-1)
    rc = int(fn(host, ctypes.byref(error_type)))
    diag.update(return_code=rc, netiso_error=int(error_type.value))
except (OSError, AttributeError) as exc:
    diag['exception'] = repr(exc)
print('NETISO_DIAGNOSTIC=' + json.dumps(diag), flush=True)
'''
client = work / ("codex-netiso-" + uuid.uuid4().hex[:12] + ".py")
client.write_text(module._CLIENT + diagnostic_code, encoding="utf-8")
cfg = dict(pth_ok=module._pth_ok((runtime.parent / "python313._pth").read_text(encoding="utf-8")),
           client_file_sha256=sha(client), runtime_python_sha256=sha(runtime))
results = dict(command=[sys.executable] + sys.argv, script_sha256=EXPECTED,
               client=str(client), config=cfg, runtime_before=before,
               scope="Native diagnostic prototype; existing runtime/work/profile; no grants/profile/firewall/exemption changes",
               attempts=[])
target = OUT / "native-diagnostic-prototype.json"
for transport in ["tcp", "udp"]:
    print("START " + transport, flush=True)
    a = module._attempt(transport, "127.0.0.1", client, runtime, work,
                        baseline["sandbox_env"], cfg, uuid.uuid4().hex, uuid.uuid4().hex)
    for side in ["control", "sandbox"]:
        line = next((s for s in a[side]["client_out"].splitlines() if s.startswith("NETISO_DIAGNOSTIC=")), None)
        a[side]["native_diagnostic"] = json.loads(line.split("=", 1)[1]) if line else None
    results["attempts"].append(a)
    target.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(dict(transport=transport, control_delivered=a['control']['delivered'], sandbox_delivered=a['sandbox']['delivered'],
                          outcome=a['sandbox']['outcome'], control_diag=a['control']['native_diagnostic'],
                          sandbox_diag=a['sandbox']['native_diagnostic']), ensure_ascii=False), flush=True)
results['runtime_after'] = {rel: sha(runtime.parent / rel) for rel in manifest}
results['runtime_unchanged'] = results['runtime_after'] == before
results['script_unchanged'] = sha(SCRIPT) == EXPECTED
target.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print('DONE', flush=True)
