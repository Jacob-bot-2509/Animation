import ctypes,os
from ctypes import wintypes
k=ctypes.windll.kernel32
k.ReadFile.argtypes=[wintypes.HANDLE,wintypes.LPVOID,wintypes.DWORD,ctypes.POINTER(wintypes.DWORD),wintypes.LPVOID]
k.ReadFile.restype=wintypes.BOOL
h=int(os.environ['PROBE_HANDLE'])
buf=ctypes.create_string_buffer(64);n=wintypes.DWORD()
ok=k.ReadFile(wintypes.HANDLE(h),buf,64,ctypes.byref(n),None)
err=k.GetLastError()
if ok:
    print('SENTINEL_READ:'+buf.raw[:n.value].decode('latin-1'),flush=True)
else:
    print('READ_ERROR winerror='+str(err),flush=True)
