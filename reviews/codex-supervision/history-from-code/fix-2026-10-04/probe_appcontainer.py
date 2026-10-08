"""Trusted native AppContainer probe; ACL changes stay inside this scratch tree."""
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = Path(r'D:\Animation-Model-Training')
sys.path.insert(0, str(PROJECT / 'src'))
from animtrain.appcontainer import appcontainer_sid, run_appcontainer

scratch = Path(tempfile.mkdtemp(prefix='appcontainer-probe-', dir=HERE)).resolve()
if not scratch.is_relative_to(HERE.resolve()):
    raise RuntimeError('Scratch directory escaped the review workspace')
runtime = scratch / 'runtime'
runtime.mkdir()
work = scratch / 'work'
work.mkdir()
private = scratch / 'private'
private.mkdir()
sentinel = private / 'synthetic-sentinel.txt'
sentinel.write_text('synthetic-private-probe', encoding='utf-8')
for name in ('python.exe', 'python3.dll', 'python313.dll', 'vcruntime140.dll', 'vcruntime140_1.dll'):
    shutil.copy2(Path(r'D:\Python') / name, runtime / name)
shutil.copytree(Path(r'D:\Python\DLLs'), runtime / 'DLLs', ignore=shutil.ignore_patterns('__pycache__'))
shutil.copytree(Path(r'D:\Python\Lib'), runtime / 'Lib',
    ignore=shutil.ignore_patterns('site-packages', '__pycache__', 'test', 'tests', 'idlelib', 'tkinter', 'turtledemo', 'ensurepip'))
(runtime / 'python313._pth').write_text('Lib\nDLLs\n.\n', encoding='utf-8')
env = {'SystemRoot': os.environ.get('SystemRoot', r'C:\Windows'), 'PATH': str(runtime),
       'TEMP': str(work), 'TMP': str(work)}
result = {'scratch': str(scratch), 'system_sid_length': len(appcontainer_sid()),
          'acl_scope': [str(runtime), str(work)], 'network_guard_shim': False}
listener = socket.socket()
listener.bind(('127.0.0.1', 0))
listener.listen(5)
listener.settimeout(1)
port = listener.getsockname()[1]
code = f'''
import _socket,json,os
report={{'python_started':True}}
s=_socket.socket(_socket.AF_INET,_socket.SOCK_STREAM)
s.settimeout(3)
try:
    s.connect(('127.0.0.1',{port}))
    report['socket_connected']=True
except OSError as e:
    report.update(socket_connected=False,socket_errno=e.errno,socket_winerror=getattr(e,'winerror',None),socket_error=str(e))
finally:
    s.close()
try:
    with open({str(sentinel)!r},encoding='utf-8') as f:
        report['private_read_allowed']=f.read()=='synthetic-private-probe'
except OSError as e:
    report.update(private_read_allowed=False,private_errno=e.errno,private_error=str(e))
print(json.dumps(report))
'''
args = [str(runtime / 'python.exe'), '-I', '-X', 'utf8', '-c', code]
control = subprocess.run(args, cwd=work, env=env, capture_output=True, timeout=15)
result['control'] = {'returncode': control.returncode, 'stdout': control.stdout.decode('utf-8','replace'),
                     'stderr': control.stderr.decode('utf-8','replace')}
if control.returncode != 0:
    raise RuntimeError('Trusted control runtime failed: ' + str(result['control']))
connection, address = listener.accept()
connection.close()
try:
    sandbox = run_appcontainer(args, cwd=work, env=env,
        allowed_dirs=[(runtime, False), (work, True)], timeout_ms=15_000)
    result['appcontainer'] = {'returncode': sandbox.returncode,
        'stdout': sandbox.stdout.decode('utf-8','replace'), 'stderr': sandbox.stderr.decode('utf-8','replace')}
    try:
        connection, address = listener.accept()
        connection.close()
        result['unexpected_sandbox_connection'] = True
    except TimeoutError:
        result['unexpected_sandbox_connection'] = False
except Exception as exc:
    result['appcontainer'] = {'exception': type(exc).__name__, 'error': str(exc),
        'errno': getattr(exc,'errno',None), 'winerror': getattr(exc,'winerror',None)}
finally:
    listener.close()
(HERE / 'appcontainer-native-probe.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
