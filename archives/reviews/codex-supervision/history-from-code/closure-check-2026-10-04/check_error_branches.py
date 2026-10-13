"""Run captured handshake/cleanup against fake APIs; never launch processes.

Only three reviewed function definitions are loaded via AST. Module-level
profile, ACL, process, and main code is not executed. All API calls are fake.
"""
from __future__ import annotations

import ast
import ctypes
import hashlib
import json
import sys
from ctypes import wintypes
from pathlib import Path
from types import SimpleNamespace

SOURCE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    r"D:\Animation-Model-Training\reviews\2026-10-04-acceptance-support\replay_v2.py")
OUT = Path(__file__).resolve().parent
source_bytes = SOURCE.read_bytes()
functions = {n.name: n for n in ast.parse(source_bytes.decode('utf-8')).body
             if isinstance(n, ast.FunctionDef)}
required = ['_is_alive_wait', '_handshake', '_cleanup']
captured = ast.Module(body=[functions[n] for n in required], type_ignores=[])


class FakeKernel:
    def __init__(self, *, handshake=False, before_wait=0x102,
                 after_wait=0, terminate_ok=True):
        self.handshake = handshake
        self.before_wait = before_wait
        self.after_wait = after_wait
        self.terminate_ok = terminate_ok
        self.terminated = False
        self.last_error = 5
        self.calls = []

    def OpenProcess(self, access, inherit, pid):
        self.calls.append(('open', access, pid))
        return 101

    def WaitForSingleObject(self, handle, milliseconds):
        self.calls.append(('wait', handle, milliseconds, self.terminated))
        self.last_error = 5
        return self.after_wait if self.terminated else self.before_wait

    def TerminateProcess(self, handle, exit_code):
        self.calls.append(('terminate', handle))
        self.terminated = True
        self.last_error = 5
        return self.terminate_ok

    def CloseHandle(self, handle):
        self.calls.append(('close', handle))
        self.last_error = 0  # verifies errors are cached BEFORE cleanup
        return True


def namespace(fake):
    clock = {'value': 0}
    def now():
        clock['value'] += 1
        return clock['value']
    ns = {'wintypes': wintypes, 'Path': Path,
          'ctypes': SimpleNamespace(get_last_error=lambda: fake.last_error),
          'time': SimpleNamespace(time=now, monotonic=now, sleep=lambda _: None),
          'k32': fake, 'WAIT_OBJECT_0': 0, 'WAIT_TIMEOUT': 0x102,
          'WAIT_FAILED': 0xffffffff, '_HANDSHAKE_ACCESS': 0x101001,
          'SANDBOX_PY': Path(r'D:\Python\python.exe'),
          '_image_path': lambda _: str(Path(r'D:\Python\python.exe').resolve())}
    exec(compile(captured, str(SOURCE) + ' [isolated fake APIs]', 'exec'), ns)
    return ns


cases = []
def check(name, fake, invoke, validate):
    result = None
    try:
        result = invoke(namespace(fake))
        validate(result, fake)
        passed, error = True, None
    except Exception as exc:
        passed, error = False, f'{type(exc).__name__}: {exc}'
    cases.append({'name': name, 'passed': passed, 'error': error,
                  'observations': result, 'fake_api_calls': fake.calls})


def require(condition, message):
    if not condition:
        raise AssertionError(message)


marker = SimpleNamespace(exists=lambda: True, read_text=lambda: '12345')
handshake = lambda ns: ns['_handshake'](marker, Path(r'D:\synthetic'), 'token', False)
cleanup = lambda ns: ns['_cleanup'](101)
error_value = lambda r: r.get('wait_lasterr', r.get('wait_error'))

check('handshake WAIT_FAILED rejects and closes handle',
      FakeKernel(before_wait=0xffffffff), handshake,
      lambda r, k: (require(r['verified'] is False, 'must reject WAIT_FAILED'),
                    require(r['wait_error'] == 5, 'must preserve native error'),
                    require(k.calls.count(('close', 101)) == 1, 'must close handle once')))
check('handshake WAIT_TIMEOUT accepts verified live handle',
      FakeKernel(), handshake,
      lambda r, k: (require(r['verified'] is True, 'valid live handshake rejected'),
                    require(r['held'] == 101, 'must retain exact handle'),
                    require(k.calls[0][1] & 1, 'must request terminate rights')))
check('cleanup already exited is confirmed without termination',
      FakeKernel(before_wait=0), cleanup,
      lambda r, k: (require(r.get('exit_confirmed') is True or r.get('alive_before_cleanup') is False, 'exit not observed'),
                    require(not k.terminated, 'must not terminate exited process')))
check('cleanup initial WAIT_FAILED records error without termination',
      FakeKernel(before_wait=0xffffffff), cleanup,
      lambda r, k: (require(error_value(r) == 5, 'must preserve wait error'),
                    require(r.get('exit_confirmed') is not True, 'error is not success'),
                    require(not k.terminated, 'must not terminate on wait error')))
check('cleanup termination success awaits exact held handle',
      FakeKernel(), cleanup,
      lambda r, k: (require(r.get('exit_confirmed') is True, 'missing exit confirmation'),
                    require(any(c[0] == 'wait' and c[3] for c in k.calls), 'no wait after terminate'),
                    require(not any(c[0] == 'open' for c in k.calls), 'PID reopened')))
check('cleanup termination failure preserves native error',
      FakeKernel(terminate_ok=False), cleanup,
      lambda r, k: (require(r.get('terminate_ok') is False, 'termination failure missing'),
                    require(r.get('terminate_lasterr') == 5, 'native error missing'),
                    require(r.get('exit_confirmed') is not True, 'failure claimed success')))
check('cleanup post-termination WAIT_TIMEOUT is not confirmed',
      FakeKernel(after_wait=0x102), cleanup,
      lambda r, k: (require(any(c[0] == 'wait' and c[3] for c in k.calls), 'no wait after terminate'),
                    require(r.get('exit_confirmed') is False, 'timeout must not confirm exit')))
check('cleanup post-termination WAIT_FAILED preserves error',
      FakeKernel(after_wait=0xffffffff), cleanup,
      lambda r, k: (require(any(c[0] == 'wait' and c[3] for c in k.calls), 'no wait after terminate'),
                    require(error_value(r) == 5, 'post-termination wait error missing'),
                    require(r.get('exit_confirmed') is not True, 'error must not confirm exit')))

record = {'scope': 'AST-isolated functions; fake APIs only, no process/profile/ACL changes',
          'source': str(SOURCE), 'source_sha256': hashlib.sha256(source_bytes).hexdigest(),
          'cases': cases, 'all_passed': all(c['passed'] for c in cases)}
(OUT / 'latest-fault-results.json').write_text(
    json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'tests': len(cases), 'passed': sum(c['passed'] for c in cases),
                  'all_passed': record['all_passed'],
                  'failures': [{'name': c['name'], 'error': c['error']} for c in cases if not c['passed']]},
                 ensure_ascii=False, indent=2))
sys.exit(0 if record['all_passed'] else 1)
