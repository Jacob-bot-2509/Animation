def token_identity() -> dict:
    """Query classes 29/30/31 in the calling process, not its parent."""
    import ctypes
    from ctypes import wintypes
    result = {"api_ok": False, "is_appcontainer": None, "capability_count": None, "sid": None}
    handle = wintypes.HANDLE()
    try:
        k = ctypes.WinDLL("kernel32", use_last_error=True)
        a = ctypes.WinDLL("advapi32", use_last_error=True)
        k.GetCurrentProcess.restype = wintypes.HANDLE
        k.CloseHandle.argtypes = [wintypes.HANDLE]
        k.CloseHandle.restype = wintypes.BOOL
        a.OpenProcessToken.argtypes = [wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)]
        a.OpenProcessToken.restype = wintypes.BOOL
        a.GetTokenInformation.argtypes = [wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID,
                                         wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
        a.GetTokenInformation.restype = wintypes.BOOL
        a.ConvertSidToStringSidW.argtypes = [wintypes.LPVOID, ctypes.POINTER(wintypes.LPWSTR)]
        a.ConvertSidToStringSidW.restype = wintypes.BOOL
        k.LocalFree.argtypes = [wintypes.LPVOID]
        k.LocalFree.restype = wintypes.LPVOID
        if not a.OpenProcessToken(k.GetCurrentProcess(), 8, ctypes.byref(handle)):
            raise ctypes.WinError(ctypes.get_last_error())
        needed = wintypes.DWORD()
        value = wintypes.DWORD()
        if not a.GetTokenInformation(handle, 29, ctypes.byref(value), ctypes.sizeof(value), ctypes.byref(needed)):
            raise ctypes.WinError(ctypes.get_last_error())
        result["is_appcontainer"] = bool(value.value)
        if not a.GetTokenInformation(handle, 30, None, 0, ctypes.byref(needed)):
            error = ctypes.get_last_error()
            if error != 122:  # ERROR_INSUFFICIENT_BUFFER is expected for the size query.
                raise ctypes.WinError(error)
        if needed.value < ctypes.sizeof(wintypes.DWORD):
            raise ValueError("Invalid TokenCapabilities size")
        buffer = ctypes.create_string_buffer(needed.value)
        if not a.GetTokenInformation(handle, 30, buffer, len(buffer), ctypes.byref(needed)):
            raise ctypes.WinError(ctypes.get_last_error())
        result["capability_count"] = ctypes.cast(buffer, ctypes.POINTER(wintypes.DWORD)).contents.value
        if not a.GetTokenInformation(handle, 31, None, 0, ctypes.byref(needed)):
            error = ctypes.get_last_error()
            if error != 122:
                raise ctypes.WinError(error)
        # TokenAppContainerSid contains a pointer into the supplied information buffer.
        # Allocate the entire returned buffer and convert while it is alive.
        if needed.value < ctypes.sizeof(wintypes.LPVOID):
            raise ValueError("Invalid TokenAppContainerSid size")
        buffer31 = ctypes.create_string_buffer(needed.value)
        if not a.GetTokenInformation(handle, 31, buffer31, len(buffer31), ctypes.byref(needed)):
            raise ctypes.WinError(ctypes.get_last_error())
        sidptr = ctypes.cast(buffer31, ctypes.POINTER(wintypes.LPVOID)).contents
        if sidptr.value:
            text = wintypes.LPWSTR()
            if not a.ConvertSidToStringSidW(sidptr, ctypes.byref(text)):
                raise ctypes.WinError(ctypes.get_last_error())
            try:
                result["sid"] = text.value
            finally:
                if k.LocalFree(text):
                    raise OSError("LocalFree failed for token SID string")
            if not result["sid"]:
                raise ValueError("Empty token SID string")
        elif result["is_appcontainer"]:
            raise ValueError("AppContainer token has a null SID")
        result["api_ok"] = True
    except Exception as exc:
        result["error"] = repr(exc)
    finally:
        if handle.value:
            try:
                if not k.CloseHandle(handle):
                    raise ctypes.WinError(ctypes.get_last_error())
            except Exception as exc:
                result.update(api_ok=False, cleanup_error=repr(exc))
    return result

import ctypes, hashlib, json, sys, time
mode, target, content = sys.argv[1], sys.argv[2], sys.argv[3]
t0 = time.time()
outcome = None
winerror = None
errno_rec = None
exc_type = None
exc_msg = None
probe_denied = None
gle = None
content_hash = None

GENERIC_WRITE = 0x40000000
GENERIC_READ = 0x80000000
CREATE_ALWAYS = 2
OPEN_EXISTING = 3
FILE_ATTRIBUTE_NORMAL = 0x80


def _probe(mode, target):
    """独立 Win32 诊断(应 msg_375):同路径同操作 CreateFileW,
    不依赖 Python 异常映射,拒绝时取真实 GetLastError。"""
    try:
        k32 = ctypes.WinDLL('kernel32', use_last_error=True)
        k32.CreateFileW.argtypes = [ctypes.c_wchar_p, ctypes.c_uint32,
                                    ctypes.c_uint32, ctypes.c_void_p,
                                    ctypes.c_uint32, ctypes.c_uint32,
                                    ctypes.c_void_p]
        k32.CreateFileW.restype = ctypes.c_void_p
        want = GENERIC_WRITE if mode == 'write' else GENERIC_READ
        creation = CREATE_ALWAYS if mode == 'write' else OPEN_EXISTING
        h = k32.CreateFileW(target, want, 0, None, creation,
                            FILE_ATTRIBUTE_NORMAL, None)
        # restype c_void_p 把 INVALID_HANDLE_VALUE(-1) 回包为 2**64-1,
        # NULL(0) 回来是 None;两者都是失败,其余才是有效句柄
        if h is not None and h != ctypes.c_void_p(-1).value:
            k32.CloseHandle(ctypes.c_void_p(h))
            return (False, None)
        return (True, ctypes.get_last_error())
    except Exception:
        return (None, None)

try:
    if mode == 'write':
        with open(target, 'wb') as f:
            f.write(content.encode('ascii'))
        outcome = 'wrote'
        content_hash = hashlib.sha256(content.encode('ascii')).hexdigest()
    else:
        with open(target, 'rb') as f:
            data = f.read()
        outcome = 'read'
        content_hash = hashlib.sha256(data).hexdigest()
except OSError as e:
    outcome = 'denied'
    winerror = getattr(e, 'winerror', None)
    errno_rec = getattr(e, 'errno', None)
    exc_type = type(e).__name__
    exc_msg = str(e)
    probe_denied, gle = _probe(mode, target)

def _sha(p):
    try:
        with open(p, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()
    except OSError:
        return None

print(json.dumps({'token': token_identity(), 'mode': mode, 'outcome': outcome,
                  'winerror': winerror, 'errno': errno_rec,
                  'exc_type': exc_type, 'exc_msg': exc_msg,
                  'probe_denied': probe_denied, 'gle': gle,
                  'content_hash': content_hash,
                  'client_sha256': _sha(sys.argv[0]), 'exe_sha256': _sha(sys.executable),
                  'site_absent': 'site' not in sys.modules and 'sitecustomize' not in sys.modules,
                  'executable': sys.executable,
                  'elapsed_s': round(time.time() - t0, 3)}), flush=True)
