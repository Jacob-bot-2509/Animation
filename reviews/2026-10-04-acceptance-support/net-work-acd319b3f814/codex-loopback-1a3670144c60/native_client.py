def token_identity() -> dict:
    """Query classes 29/30/31 in the calling process, not its parent."""
    import ctypes
    from ctypes import wintypes
    result = {"api_ok": False, "is_appcontainer": None, "capability_count": None, "sid": None}
    handle = wintypes.HANDLE()
    k = ctypes.WinDLL("kernel32", use_last_error=True)
    a = ctypes.WinDLL("advapi32", use_last_error=True)
    k.GetCurrentProcess.restype = wintypes.HANDLE
    k.CloseHandle.argtypes = [wintypes.HANDLE]
    a.OpenProcessToken.argtypes = [wintypes.HANDLE, wintypes.DWORD, ctypes.POINTER(wintypes.HANDLE)]
    a.OpenProcessToken.restype = wintypes.BOOL
    a.GetTokenInformation.argtypes = [wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID,
                                     wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
    a.GetTokenInformation.restype = wintypes.BOOL
    a.ConvertSidToStringSidW.argtypes = [wintypes.LPVOID, ctypes.POINTER(wintypes.LPWSTR)]
    a.ConvertSidToStringSidW.restype = wintypes.BOOL
    k.LocalFree.argtypes = [wintypes.LPVOID]
    k.LocalFree.restype = wintypes.LPVOID
    try:
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
                k.LocalFree(text)
        result["api_ok"] = True
    except (OSError, ValueError, AttributeError) as exc:
        result["error"] = repr(exc)
    finally:
        if handle.value:
            k.CloseHandle(handle)
    return result

import hashlib, json, os, socket, sys, time
transport, host, port, nonce = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]
record = {'host': host, 'port': port, 'transport': transport, 'nonce': nonce,
          'token': token_identity(), 'outcome': None, 'winerror': None,
          'executable': sys.executable, 'socket_file': socket.__file__,
          'site_absent': 'site' not in sys.modules and 'sitecustomize' not in sys.modules}
record['started'] = time.monotonic()
try:
    with socket.socket(socket.AF_INET6 if ':' in host else socket.AF_INET,
                       socket.SOCK_STREAM if transport == 'tcp' else socket.SOCK_DGRAM) as s:
        s.settimeout(3)
        if transport == 'tcp':
            s.connect((host, port))
            s.sendall(nonce.encode('ascii'))
        else:
            n = s.sendto(nonce.encode('ascii'), (host, port))
            if n != len(nonce): raise OSError('Partial UDP send')
        record['outcome'] = 'sent_ok'
except TimeoutError:
    record['outcome'] = 'net_timeout'
except OSError as exc:
    record.update(outcome='net_error', winerror=getattr(exc, 'winerror', None), error=repr(exc))
record['finished'] = time.monotonic()
for key, file in [('client_sha256', sys.argv[0]), ('exe_sha256', sys.executable)]:
    with open(file, 'rb') as f: record[key] = hashlib.sha256(f.read()).hexdigest()
print(json.dumps(record), flush=True)
