"""One temporary per-user profile; run only after consent to C:/HKCU writes."""
import ctypes
import json
import os
import socket
import subprocess
import sys
import uuid
import winreg
from ctypes import wintypes
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
PROJECT = Path(r'D:\Animation-Model-Training')
sys.path.insert(0, str(PROJECT / 'src'))
from animtrain import appcontainer as ac

name = 'codex-elevation-probe-' + uuid.uuid4().hex[:16]
assert len(name) < 64 and name.startswith('codex-elevation-probe-')
result = {'test_profile_name': name, 'requested_capability_count': 0,
          'uac_requested': False, 'stage': 'initializing'}
create = ac._u32.CreateAppContainerProfile
create.argtypes = [wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.LPCWSTR,
                   wintypes.LPVOID, wintypes.DWORD, ctypes.POINTER(wintypes.LPVOID)]
create.restype = ctypes.c_long
delete = ac._u32.DeleteAppContainerProfile
delete.argtypes = [wintypes.LPCWSTR]
delete.restype = ctypes.c_long
get_token = ac._a32.GetTokenInformation
get_token.argtypes = [wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID,
                     wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
get_token.restype = wintypes.BOOL
ac._k32.GetCurrentProcess.restype = wintypes.HANDLE
ac._a32.OpenProcessToken.argtypes = [wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)]
ac._a32.OpenProcessToken.restype = wintypes.BOOL
token = wintypes.HANDLE()
if not ac._a32.OpenProcessToken(ac._k32.GetCurrentProcess(), 8, ctypes.byref(token)):
    raise ctypes.WinError(ctypes.get_last_error())
try:
    value = wintypes.DWORD()
    needed = wintypes.DWORD()
    if not get_token(token, 20, ctypes.byref(value), ctypes.sizeof(value), ctypes.byref(needed)):
        raise ctypes.WinError(ctypes.get_last_error())
    result['parent_token_elevated'] = bool(value.value)
finally:
    ac._k32.CloseHandle(token)
if result['parent_token_elevated']:
    raise SystemExit('Refusing test: parent token is elevated, so result would not answer necessity')

old = json.loads(Path(r'D:\code\output\claude-supervision\fix-2026-10-04\appcontainer-native-probe.json').read_bytes())
scratch = Path(old['scratch']).resolve()
allowed_root = Path(r'D:\code\output\claude-supervision').resolve()
if not scratch.is_relative_to(allowed_root):
    raise SystemExit('Runtime is outside the approved scratch tree')
runtime = scratch / 'runtime'
work = HERE / ('work-' + name)
work.mkdir()
private = HERE / ('private-' + name)
private.mkdir()
sentinel = private / 'synthetic.txt'
sentinel.write_text('synthetic-only', encoding='utf-8')
env = {'SystemRoot': os.environ.get('SystemRoot', r'C:\Windows'),
       'PATH': str(runtime), 'TEMP': str(work), 'TMP': str(work)}
created = False
profile = None
created_sid = None
listener = socket.socket()
listener.bind(('127.0.0.1', 0))
listener.listen(4)
listener.settimeout(1)
port = listener.getsockname()[1]
result['acl_scope'] = [str(runtime), str(work)]
code = f'''
import _socket,ctypes,json
from ctypes import wintypes
report={{'python_started':True}}
k=ctypes.WinDLL('kernel32',use_last_error=True);a=ctypes.WinDLL('advapi32',use_last_error=True)
k.GetCurrentProcess.restype=wintypes.HANDLE
k.CloseHandle.argtypes=[wintypes.HANDLE]
a.OpenProcessToken.argtypes=[wintypes.HANDLE,wintypes.DWORD,ctypes.POINTER(wintypes.HANDLE)]
a.OpenProcessToken.restype=wintypes.BOOL
a.GetTokenInformation.argtypes=[wintypes.HANDLE,ctypes.c_int,wintypes.LPVOID,wintypes.DWORD,ctypes.POINTER(wintypes.DWORD)]
a.GetTokenInformation.restype=wintypes.BOOL
t=wintypes.HANDLE();ok=a.OpenProcessToken(k.GetCurrentProcess(),8,ctypes.byref(t))
if ok:
    try:
        for tag,kind in [('token_is_appcontainer',29),('token_is_elevated',20)]:
            value=wintypes.DWORD();needed=wintypes.DWORD()
            if a.GetTokenInformation(t,kind,ctypes.byref(value),ctypes.sizeof(value),ctypes.byref(needed)):
                report[tag]=bool(value.value)
    finally:k.CloseHandle(t)
s=_socket.socket(_socket.AF_INET,_socket.SOCK_STREAM);s.settimeout(3)
try:
    s.connect(('127.0.0.1',{port}));report['socket_connected']=True
except OSError as e:
    report.update(socket_connected=False,socket_errno=e.errno,socket_winerror=getattr(e,'winerror',None))
finally:s.close()
try:
    with open({str(sentinel)!r},encoding='utf-8') as f:report['private_read_allowed']=f.read()=='synthetic-only'
except OSError as e:
    report.update(private_read_allowed=False,private_errno=e.errno)
print(json.dumps(report))
'''
args = [str(runtime / 'python.exe'), '-I', '-X', 'utf8', '-c', code]
try:
    ptr = wintypes.LPVOID()
    hr = create(name, 'Codex elevation test (temporary)', 'Temporary diagnostic; deleted after test', None, 0, ctypes.byref(ptr))
    result['create_profile_hresult'] = hr
    result['create_profile_hresult_hex'] = f'0x{hr & 0xffffffff:08X}'
    if hr < 0:
        result['stage'] = 'profile_creation_failed'
    else:
        created = True
        if not ptr.value:
            raise RuntimeError('Profile API succeeded without SID')
        try:
            created_sid = ctypes.string_at(ptr, ac._a32.GetLengthSid(ptr))
        finally:
            ac._a32.FreeSid(ptr)
        with patch.object(ac, 'APPCONTAINER_NAME', name):
            result['derived_sid_matches_created_sid'] = ac.appcontainer_sid() == created_sid
            result['profile_sid'] = ac._sid_sddl(created_sid)
            profile = ac.appcontainer_profile_path(created_sid)
            result['profile_storage_drive'] = profile.drive
            result['profile_exists_before_cleanup'] = profile.is_dir()
            for key in ('SystemDrive', 'windir', 'USERPROFILE', 'ALLUSERSPROFILE',
                        'ProgramData', 'USERNAME', 'USERDOMAIN', 'HOMEDRIVE', 'HOMEPATH'):
                if key in os.environ:
                    env[key] = os.environ[key]
            env['LOCALAPPDATA'] = str(profile)
            env['APPDATA'] = str(profile)
            result['required_user_environment_supplied'] = True
            control = subprocess.run(args, cwd=work, env=env, capture_output=True, timeout=15)
            result['control'] = {'returncode':control.returncode,
                'stdout':control.stdout.decode('utf-8','replace'), 'stderr':control.stderr.decode('utf-8','replace')}
            if control.returncode != 0:
                raise RuntimeError('Ordinary runtime failed')
            c,_ = listener.accept();c.close()
            sandbox = ac.run_appcontainer(args, cwd=work, env=env,
                allowed_dirs=[(runtime,False),(work,True)], timeout_ms=15_000)
            result['appcontainer'] = {'returncode':sandbox.returncode,
                'stdout':sandbox.stdout.decode('utf-8','replace'), 'stderr':sandbox.stderr.decode('utf-8','replace')}
            try:
                c,_=listener.accept();c.close();result['unexpected_sandbox_connection']=True
            except TimeoutError:
                result['unexpected_sandbox_connection']=False
            result['stage'] = 'completed'
except Exception as exc:
    result.update(stage='exception', exception=type(exc).__name__, error=str(exc),
                  errno=getattr(exc,'errno',None), winerror=getattr(exc,'winerror',None))
finally:
    listener.close()
    if created:
        # Never delete a pre-existing profile. Only a successful fresh UUID create reaches here.
        hr = delete(name)
        result['delete_profile_hresult'] = hr
        result['profile_exists_after_cleanup'] = profile.exists() if profile is not None else None
        if created_sid is not None:
            key = r'Software\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppContainer\Mappings' + '\\' + ac._sid_sddl(created_sid)
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER,key):
                    result['registry_mapping_exists_after_cleanup']=True
            except FileNotFoundError:
                result['registry_mapping_exists_after_cleanup']=False
    result['cleanup_confirmed'] = bool(created and result.get('delete_profile_hresult') == 0
        and result.get('profile_exists_after_cleanup') is False
        and result.get('registry_mapping_exists_after_cleanup') is False)
    (HERE/'new-profile-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
