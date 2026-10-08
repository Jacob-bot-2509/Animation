"""Independent checks for the active v2 switch and AppContainer API contract."""
import contextlib
import ctypes
import hashlib
import importlib.util
import io
import json
import os
import sys
from ctypes import wintypes
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
os.chdir(ROOT)
sys.path.insert(0, str(ROOT / 'src'))
report = {'revision': '68c51be', 'checks': {}, 'findings': []}
def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

from animtrain.freeze import check_frozen
from animtrain.manifest import Manifest
from animtrain.validate import validate_manifest
from animtrain.preflight import check_exec_isolation

active = ROOT / 'data/manifest.json'
report['checks']['active_manifest'] = validate_manifest(Manifest.load(active), active.parent)
report['checks']['v2_lock_binding'] = [{'split': split, 'errors': check_frozen(ROOT / f'data/{split}-v2.lock.json'),
    'binding_ok': json.loads((ROOT / f'data/{split}-v2.lock.json').read_bytes())['meta']['manifest_sha256'] == hashlib.sha256(active.read_bytes()).hexdigest()} for split in ('eval','test')]
report['checks']['network_gate'] = check_exec_isolation()

prep = load('review_latest_prep', 'tools/eval_test_prep.py')
with contextlib.redirect_stdout(io.StringIO()) as out:
    rc = prep.main(['status', '--dir', str(ROOT / 'data/v2')])
report['checks']['v2_status'] = {'exit_code': rc, 'stdout': out.getvalue()}
if '校验未过' in out.getvalue():
    report['findings'].append({'priority': 'P2', 'file': 'tools/eval_test_prep.py:46',
        'issue': 'After the active manifest moved to data/manifest.json, status still omits it from the candidate set and rejects correctly rebound v2 locks.'})

# Read-only native API call: no profile creation, ACL change or process launch.
u = ctypes.WinDLL('userenv', use_last_error=True)
a = ctypes.WinDLL('advapi32', use_last_error=True)
k = ctypes.WinDLL('kernel32', use_last_error=True)
derive = u.DeriveAppContainerSidFromAppContainerName
derive.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(wintypes.LPVOID)]
derive.restype = ctypes.c_long  # HRESULT; success is S_OK == 0
a.GetLengthSid.argtypes = [wintypes.LPVOID]
a.GetLengthSid.restype = wintypes.DWORD
a.FreeSid.argtypes = [wintypes.LPVOID]
a.FreeSid.restype = wintypes.LPVOID
a.ConvertSidToStringSidW.argtypes = [wintypes.LPVOID, ctypes.POINTER(wintypes.LPWSTR)]
a.ConvertSidToStringSidW.restype = wintypes.BOOL
k.LocalFree.argtypes = [wintypes.LPVOID]
k.LocalFree.restype = wintypes.LPVOID
sid_ptr = wintypes.LPVOID()
hr = derive('animtrain-render-sandbox', ctypes.byref(sid_ptr))
sid_info = {'hresult': hr, 'success': hr == 0, 'sid_pointer_nonnull': bool(sid_ptr.value)}
if hr == 0 and sid_ptr.value:
    length = a.GetLengthSid(sid_ptr)
    correct_sid = ctypes.string_at(sid_ptr, length)
    sid_text = wintypes.LPWSTR()
    if a.ConvertSidToStringSidW(sid_ptr, ctypes.byref(sid_text)):
        sid_info.update({'sid': sid_text.value, 'length': length})
        k.LocalFree(ctypes.cast(sid_text, wintypes.LPVOID))
    a.FreeSid(sid_ptr)
    implementation = load('review_latest_appcontainer', 'src/animtrain/appcontainer.py')
    wrong_sid = implementation.appcontainer_sid()
    sid_info.update({'implementation_sid_length': len(wrong_sid),
                     'implementation_matches_system_sid': wrong_sid == correct_sid})
    if wrong_sid != correct_sid:
        report['findings'].append({'priority': 'P1', 'file': 'src/animtrain/appcontainer.py:101',
            'issue': 'DeriveAppContainerSidFromAppContainerName returns HRESULT S_OK=0, but implementation declares BOOL and treats zero as failure, discarding a valid SID and using a different fallback. Home/admin failure conclusion is not established.'})
report['checks']['native_sid_contract'] = sid_info
(ROOT / 'latest-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
