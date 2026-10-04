import ctypes,os
from ctypes import wintypes
k=ctypes.WinDLL('kernel32', use_last_error=True)
k.ReadFile.argtypes=[wintypes.HANDLE,wintypes.LPVOID,wintypes.DWORD,ctypes.POINTER(wintypes.DWORD),wintypes.LPVOID]
k.ReadFile.restype=wintypes.BOOL
h=int(os.environ['PROBE_HANDLE'])
buf=ctypes.create_string_buffer(64);n=wintypes.DWORD()
try:
    ok=k.ReadFile(wintypes.HANDLE(h),buf,64,ctypes.byref(n),None)
except OSError as e:
    ok=False
if ok:
    print('SENTINEL_READ:'+buf.raw[:n.value].decode('latin-1'))
else:
    print('INVALID_HANDLE lasterr='+str(ctypes.get_last_error()))
