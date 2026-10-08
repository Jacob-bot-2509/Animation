import ctypes, os, socket, sys, time
from ctypes import wintypes
k = ctypes.windll.kernel32
a = ctypes.windll.advapi32
k.GetCurrentProcess.restype = wintypes.HANDLE
k.OpenProcessToken.restype = wintypes.BOOL
k.OpenProcessToken.argtypes = [wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)]
a.GetTokenInformation.restype = wintypes.BOOL
a.GetTokenInformation.argtypes = [wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
k.LocalFree.argtypes = [wintypes.LPVOID]
k.CloseHandle.argtypes = [wintypes.HANDLE]
class _SAA(ctypes.Structure):
    _fields_ = [('Sid', wintypes.LPVOID), ('Attributes', wintypes.DWORD)]
class _TGROUPS(ctypes.Structure):
    _fields_ = [('GroupCount', wintypes.DWORD), ('Groups', _SAA * 1)]
h = wintypes.HANDLE()
ok1 = k.OpenProcessToken(k.GetCurrentProcess(), 0x0008, ctypes.byref(h))
val = wintypes.DWORD(); need = wintypes.DWORD()
ok2 = a.GetTokenInformation(h, 29, ctypes.byref(val), 4, ctypes.byref(need))
is_ac = int(val.value) if ok2 else None
# 能力计数:TokenCapabilities=30 返回 TOKEN_GROUPS,GroupCount 即能力数;
# API 失败一律 None,绝不填 0
cap_count = None
cap_api_ok = 0
cap_needed = 0
if ok2:
    need2 = wintypes.DWORD()
    a.GetTokenInformation(h, 30, None, 0, ctypes.byref(need2))
    cap_needed = need2.value
    if cap_needed:
        buf = ctypes.create_string_buffer(cap_needed)
        if a.GetTokenInformation(h, 30, buf, cap_needed, ctypes.byref(need2)):
            tg = ctypes.cast(buf, ctypes.POINTER(_TGROUPS)).contents
            cap_count = tg.GroupCount
            cap_api_ok = 1
k.CloseHandle(h)
transport, host, port, nonce = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
t0 = time.time()
outcome = 'no_record'
err_winerror = None
s = None
try:
    fam = socket.AF_INET6 if ':' in host else socket.AF_INET
    s = socket.socket(fam, socket.SOCK_STREAM if transport == 'tcp' else socket.SOCK_DGRAM)
except OSError as e:
    outcome = 'net_error'
    err_winerror = getattr(e, 'winerror', None)
    print('SOCKET_ERROR winerror=%s' % err_winerror, flush=True)
if s is not None:
    try:
        s.settimeout(3.0)
        if transport == 'tcp':
            s.connect((host, port))
            s.sendall(nonce.encode('latin-1'))
            outcome = 'sent_ok'
            print('TCP_SENT_OK', flush=True)
        else:
            s.sendto(nonce.encode('latin-1'), (host, port))
            outcome = 'sent_ok'
            print('UDP_SENT_OK', flush=True)
    except socket.timeout:
        outcome = 'net_timeout'
        print('NET_TIMEOUT', flush=True)
    except OSError as e:
        outcome = 'net_error'
        err_winerror = getattr(e, 'winerror', None)
        print('NET_ERROR winerror=%s errno=%s' % (err_winerror, getattr(e, 'errno', None)), flush=True)
    finally:
        try:
            s.close()
        except Exception:
            pass
print('TOKEN_IS_APPCONTAINER=%s ok=%s/%s' % (is_ac, int(ok1), int(ok2)), flush=True)
print('CAPABILITY_COUNT=%s CAP_API_OK=%s CAP_NEEDED=%s' % (cap_count, cap_api_ok, cap_needed), flush=True)
print('SHIM_ABSENT=%s' % ('sitecustomize' not in sys.modules), flush=True)
print('SITE_ABSENT=%s' % ('site' not in sys.modules), flush=True)
print('SYS_EXECUTABLE=%s' % sys.executable, flush=True)
print('SOCKET_FILE=%s' % socket.__file__, flush=True)
# 自哈希:对实际执行的脚本文件与解释器计算 SHA256,供监督端比对
def _sha(p):
    try:
        import hashlib
        with open(p, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None
print('CLIENT_FILE_SHA256=%s' % _sha(sys.argv[0]), flush=True)
print('RUNTIME_EXE_SHA256=%s' % _sha(sys.executable), flush=True)
print('OUTCOME=%s ERR_WINERROR=%s T_DELTA=%.3f' % (outcome, err_winerror, time.time() - t0), flush=True)
