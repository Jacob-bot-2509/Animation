"""Trusted probes for inherited file handles and timeout descendants; bounded cleanup."""
import ctypes
import json
import os
import subprocess
import sys
import tempfile
import uuid
from ctypes import wintypes
from pathlib import Path
from unittest.mock import patch

HERE = Path(r'D:\code\output\claude-supervision\acceptance-2026-10-04')
HERE.mkdir(exist_ok=True)
sys.path.insert(0,r'D:\Animation-Model-Training\src')
from animtrain import appcontainer as ac
old = json.loads(Path(r'D:\code\output\claude-supervision\fix-2026-10-04\appcontainer-native-probe.json').read_bytes())
runtime = Path(old['scratch']) / 'runtime'
work = Path(tempfile.mkdtemp(prefix='work-',dir=HERE))
private = Path(tempfile.mkdtemp(prefix='private-',dir=HERE))
sentinel = private / 'sentinel.txt'
sentinel.write_bytes(b'SYNTHETIC-INHERITED-HANDLE-PROBE')
name = 'codex-acceptance-edge-' + uuid.uuid4().hex[:16]
result={'profile_name':name,'scope':'Trusted synthetic files and short-lived processes only',
        'work':str(work),'checks':{}}
create=ac._u32.CreateAppContainerProfile
create.argtypes=[wintypes.LPCWSTR,wintypes.LPCWSTR,wintypes.LPCWSTR,wintypes.LPVOID,wintypes.DWORD,ctypes.POINTER(wintypes.LPVOID)]
create.restype=ctypes.c_long
delete=ac._u32.DeleteAppContainerProfile
delete.argtypes=[wintypes.LPCWSTR];delete.restype=ctypes.c_long
ac._k32.OpenProcess.argtypes=[wintypes.DWORD,wintypes.BOOL,wintypes.DWORD]
ac._k32.OpenProcess.restype=wintypes.HANDLE
ac._k32.QueryFullProcessImageNameW.argtypes=[wintypes.HANDLE,wintypes.DWORD,wintypes.LPWSTR,ctypes.POINTER(wintypes.DWORD)]
ac._k32.QueryFullProcessImageNameW.restype=wintypes.BOOL
created=False;profile=None;child_handle=None;fd=None
try:
    sid=wintypes.LPVOID();hr=create(name,'Temporary acceptance edge probe','Delete after testing',None,0,ctypes.byref(sid))
    result['create_hresult']=hr
    if hr<0:raise OSError(hr,'Cannot create temporary profile')
    created=True
    try: sid_bytes=ctypes.string_at(sid,ac._a32.GetLengthSid(sid))
    finally:ac._a32.FreeSid(sid)
    with patch.object(ac,'APPCONTAINER_NAME',name):
        profile=ac.appcontainer_profile_path(sid_bytes)
        env={key:os.environ[key] for key in ('SystemRoot','SystemDrive','windir','USERPROFILE',
            'ALLUSERSPROFILE','ProgramData','USERNAME','USERDOMAIN','HOMEDRIVE','HOMEPATH') if key in os.environ}
        env.update(PATH=str(runtime),TEMP=str(work),TMP=str(work),LOCALAPPDATA=str(profile),APPDATA=str(profile))
        fd=os.open(sentinel,os.O_RDONLY)
        os.set_inheritable(fd,True)
        import msvcrt
        inherited=msvcrt.get_osfhandle(fd)
        code=f'''
import ctypes,json
from ctypes import wintypes
r={{}}
try:
    with open({str(sentinel)!r},'rb') as f:r['direct_read']=f.read().decode()
except OSError as e:r['direct_read_denied']=True;r['direct_read_errno']=e.errno
k=ctypes.WinDLL('kernel32',use_last_error=True)
k.ReadFile.argtypes=[wintypes.HANDLE,wintypes.LPVOID,wintypes.DWORD,ctypes.POINTER(wintypes.DWORD),wintypes.LPVOID]
k.ReadFile.restype=wintypes.BOOL
b=ctypes.create_string_buffer(128);n=wintypes.DWORD()
r['inherited_read_ok']=bool(k.ReadFile(wintypes.HANDLE({inherited}),b,128,ctypes.byref(n),None))
r['inherited_read_error']=ctypes.get_last_error() if not r['inherited_read_ok'] else 0
r['inherited_bytes']=b.raw[:n.value].decode('ascii','replace')
print(json.dumps(r))
'''
        run=ac.run_appcontainer([str(runtime/'python.exe'),'-I','-c',code],cwd=work,env=env,
            allowed_dirs=[(runtime,False),(work,True)],timeout_ms=10000)
        result['checks']['inherited_handle']={'returncode':run.returncode,'stdout':run.stdout.decode('utf-8','replace'),
            'stderr':run.stderr.decode('utf-8','replace')}
        os.close(fd);fd=None
        code="import subprocess,sys,time,json; p=subprocess.Popen([sys.executable,'-I','-c','import time; time.sleep(8)'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); print(json.dumps({'child_pid':p.pid}),flush=True); time.sleep(10)"
        args=[str(runtime/'python.exe'),'-I','-c',code]
        try:
            ac.run_appcontainer(args,cwd=work,env=env,allowed_dirs=[],timeout_ms=1000)
            result['checks']['timeout_tree']={'unexpected_normal_return':True}
        except subprocess.TimeoutExpired:
            stdout_file=work/f'.ac-out-{id(args)}.tmp'
            lines=stdout_file.read_text(encoding='utf-8').splitlines()
            child_pid=json.loads(lines[0])['child_pid']
            child_handle=ac._k32.OpenProcess(0x100000|0x1000|1,False,child_pid)
            entry={'parent_timed_out':True,'child_pid':child_pid,'child_handle_opened':bool(child_handle)}
            if child_handle:
                image=ctypes.create_unicode_buffer(32768);n=wintypes.DWORD(len(image))
                if not ac._k32.QueryFullProcessImageNameW(child_handle,0,image,ctypes.byref(n)):
                    raise ctypes.WinError(ctypes.get_last_error())
                entry['child_image_matches_runtime']=Path(image.value).resolve()==(runtime/'python.exe').resolve()
                entry['child_alive_after_parent_timeout']=ac._k32.WaitForSingleObject(child_handle,0)==0x102
                if entry['child_image_matches_runtime'] and entry['child_alive_after_parent_timeout']:
                    if not ac._k32.TerminateProcess(child_handle,1):
                        raise ctypes.WinError(ctypes.get_last_error())
                    entry['manual_cleanup_child_exited']=ac._k32.WaitForSingleObject(child_handle,5000)==0
                ac._k32.CloseHandle(child_handle);child_handle=None
            result['checks']['timeout_tree']=entry
except Exception as exc:
    result['error']={'type':type(exc).__name__,'detail':str(exc)}
finally:
    if fd is not None:os.close(fd)
    if child_handle:
        # This handle belongs to the exact child created by our trusted probe.
        ac._k32.TerminateProcess(child_handle,1)
        ac._k32.WaitForSingleObject(child_handle,5000)
        ac._k32.CloseHandle(child_handle)
    if created:
        result['delete_hresult']=delete(name)
        result['profile_exists_after_cleanup']=profile.exists() if profile else None
    (HERE/'edge-results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))
