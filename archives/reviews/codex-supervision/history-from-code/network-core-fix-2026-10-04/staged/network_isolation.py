"""Read-only Windows network policy evidence and bounded loopback acceptance.

No firewall, exemption, capability, profile or ACL is changed by this module.
PASS_LOCAL_LOOPBACK proves only the tested local endpoints and observation window.
It must never enable a production render gate or imply external isolation.
"""
from __future__ import annotations

import ctypes
import inspect
import ipaddress
import json
import socket
import threading
import time
from ctypes import wintypes


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


def read_loopback_exemptions() -> dict:
    """Copy API-owned SIDs then HeapFree each SID and the array, per Microsoft."""
    result = {"api_ok": False, "return_code": None, "sids": None, "cleanup_ok": True}
    class SidAndAttributes(ctypes.Structure):
        _fields_ = [("Sid", wintypes.LPVOID), ("Attributes", wintypes.DWORD)]
    array = ctypes.POINTER(SidAndAttributes)()
    count = wintypes.DWORD()
    try:
        k = ctypes.WinDLL("kernel32", use_last_error=True)
        a = ctypes.WinDLL("advapi32", use_last_error=True)
        f = ctypes.WinDLL("Firewallapi", use_last_error=True)
        k.GetProcessHeap.restype = wintypes.HANDLE
        k.HeapFree.argtypes = [wintypes.HANDLE, wintypes.DWORD, wintypes.LPVOID]
        k.HeapFree.restype = wintypes.BOOL
        k.LocalFree.argtypes = [wintypes.LPVOID]
        k.LocalFree.restype = wintypes.LPVOID
        a.ConvertSidToStringSidW.argtypes = [wintypes.LPVOID, ctypes.POINTER(wintypes.LPWSTR)]
        a.ConvertSidToStringSidW.restype = wintypes.BOOL
        fn = f.NetworkIsolationGetAppContainerConfig
        fn.argtypes = [ctypes.POINTER(wintypes.DWORD), ctypes.POINTER(ctypes.POINTER(SidAndAttributes))]
        fn.restype = wintypes.DWORD
        result["return_code"] = int(fn(ctypes.byref(count), ctypes.byref(array)))
        if result["return_code"] != 0:
            return result
        if count.value > 10000 or (count.value and not array):
            raise ValueError("Invalid exemption array")
        sids = []
        for index in range(count.value):
            text = wintypes.LPWSTR()
            if not a.ConvertSidToStringSidW(array[index].Sid, ctypes.byref(text)):
                raise ctypes.WinError(ctypes.get_last_error())
            try:
                if not text.value:
                    raise ValueError("Empty exemption SID")
                sids.append(text.value)
            finally:
                k.LocalFree(text)
        result.update(api_ok=True, sids=sorted(sids))
    except (OSError, ValueError, AttributeError) as exc:
        result["error"] = repr(exc)
    finally:
        if array:
            heap = k.GetProcessHeap()
            if count.value <= 10000:
                for index in range(count.value):
                    if array[index].Sid and not k.HeapFree(heap, 0, array[index].Sid):
                        result["cleanup_ok"] = False
            if not k.HeapFree(heap, 0, array):
                result["cleanup_ok"] = False
    result["api_ok"] = result["api_ok"] and result["cleanup_ok"]
    return result


def client_source() -> str:
    """Embed the canonical token query in a standalone client; no socket shim."""
    return inspect.getsource(token_identity) + '''
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
'''


class LoopbackReceiver:
    """One bound endpoint kept alive for control-before, sandbox, control-after."""
    def __init__(self, transport: str, host: str):
        self.transport, self.host = transport, host
        self.records, self.errors = [], []
        self.stop = threading.Event()
        self.lock = threading.Lock()
        self.socket = socket.socket(socket.AF_INET6 if ":" in host else socket.AF_INET,
                                    socket.SOCK_STREAM if transport == "tcp" else socket.SOCK_DGRAM)
        try:
            self.socket.bind((host, 0))
            self.port = self.socket.getsockname()[1]
            if transport == "tcp": self.socket.listen(8)
            self.socket.settimeout(0.1)
        except BaseException:
            self.socket.close()
            raise
        self.started = time.monotonic()
        self.closed = None
        self.thread = threading.Thread(target=self._receive, daemon=True)
        self.thread.start()

    def _receive(self):
        try:
            while not self.stop.is_set():
                try:
                    if self.transport == "tcp":
                        conn, peer = self.socket.accept()
                        with conn:
                            conn.settimeout(2)
                            chunks = []
                            size = 0
                            try:
                                while size < 32:
                                    data = conn.recv(32 - size)
                                    if not data: break
                                    chunks.append(data)
                                    size += len(data)
                            except TimeoutError:
                                self.errors.append("Accepted connection timed out before a full nonce")
                            data = b"".join(chunks)
                    else:
                        data, peer = self.socket.recvfrom(4096)
                    with self.lock:
                        self.records.append({"hex": data.hex(), "peer": repr(peer), "at": time.monotonic()})
                except TimeoutError:
                    continue
        except OSError as exc:
            self.errors.append(repr(exc))
        finally:
            self.socket.close()
            self.closed = time.monotonic()

    def snapshot(self):
        with self.lock:
            return list(self.records)

    def close(self):
        self.stop.set()
        self.thread.join(3)
        if self.thread.is_alive():
            self.errors.append("Receiver thread did not exit")
            raise RuntimeError(self.errors[-1])


def judge_loopback_evidence(record: dict) -> dict:
    """Require OS configuration + token identity + same-endpoint bracketing.

    Silent drop alone, an API error, unknown state or an absent control never passes.
    This uses a different, explicit evidence contract from WSAEACCES-only acceptance.
    """
    nonce = record.get("nonces", {})
    packets = record.get("packets", [])
    if not isinstance(nonce, dict) or not isinstance(packets, list) or any(not isinstance(p, dict) for p in packets):
        return {"verdict": "UNVERIFIED", "reasons": ["Malformed nonce/packet evidence"]}
    probe_hex = str(nonce.get("sandbox", "")).encode("ascii", "ignore").hex()
    if probe_hex and any(p.get("hex") == probe_hex for p in packets):
        return {"verdict": "FAIL", "reasons": ["Sandbox nonce received"]}
    reasons = []
    try:
        if not ipaddress.ip_address(record["host"]).is_loopback or record["transport"] not in ("tcp", "udp"):
            reasons.append("Only literal loopback TCP/UDP is covered")
        expected = record["expected_sid"]
        if not expected.startswith("S-1-15-2-"): reasons.append("Invalid expected AppContainer SID")
        configs = [record["policy_before"], record["policy_after"]]
        for config in configs:
            if config.get("api_ok") is not True or config.get("return_code") != 0 or config.get("cleanup_ok") is not True:
                reasons.append("Loopback policy query failed")
            if not isinstance(config.get("sids"), list) or expected in config["sids"]:
                reasons.append("Exemption list unknown or tested SID exempt")
        if configs[0].get("sids") != configs[1].get("sids"): reasons.append("Policy changed during test")
        if record["runtime_integrity"] is not True: reasons.append("Runtime/client integrity not confirmed")
        if record["server_errors"] or record["server_complete"] is not True: reasons.append("Receiver failed or unfinished")
        if len(nonce) != 3 or len(set(nonce.values())) != 3 or any(len(v) != 32 for v in nonce.values()):
            reasons.append("Invalid/ambiguous nonces")
        expected_hex = {n.encode("ascii").hex() for n in nonce.values()}
        if any(p.get("hex") not in expected_hex for p in packets): reasons.append("Unattributed network data")
        for side in ("before", "sandbox", "after"):
            client = record["clients"][side]
            data = client.get("data") or {}
            token = data.get("token") or {}
            if client.get("rc") != 0 or client.get("timed_out") is not False or token.get("api_ok") is not True:
                reasons.append(side + " client/token incomplete")
            if (data.get("host"), data.get("port"), data.get("transport"), data.get("nonce")) != (record["host"], record["port"], record["transport"], nonce[side]):
                reasons.append(side + " endpoint/nonce mismatch")
            if not record["server_started"] <= data.get("started", -1) <= data.get("finished", -1) <= record["server_closed"]:
                reasons.append(side + " attempt outside listener lifetime")
            if side == "sandbox":
                if token.get("is_appcontainer") is not True or token.get("sid") != expected or token.get("capability_count") != 0:
                    reasons.append("AppContainer identity/capabilities mismatch")
                if data.get("outcome") not in ("net_timeout", "sent_ok", "net_error"):
                    reasons.append("Unexplained sandbox outcome")
                if record["transport"] == "tcp" and data.get("outcome") == "sent_ok":
                    reasons.append("TCP reported successful delivery but receiver did not confirm it")
                if data.get("outcome") == "net_error" and data.get("winerror") != 10013:
                    reasons.append("Unexplained sandbox error")
            else:
                if token.get("is_appcontainer") is not False or data.get("outcome") != "sent_ok":
                    reasons.append(side + " ordinary control invalid")
                matches = [p for p in packets if p.get("hex") == nonce[side].encode("ascii").hex()]
                if len(matches) != 1: reasons.append(side + " nonce not uniquely received")
        before, sb, after = [record["clients"][side]["data"] for side in ("before", "sandbox", "after")]
        if not before["finished"] <= sb["started"] <= sb["finished"] <= after["started"]:
            reasons.append("Control/sandbox ordering invalid")
        if after["started"] - sb["finished"] < 20:
            reasons.append("Observation window shorter than 20 seconds")
    except (KeyError, TypeError, ValueError) as exc:
        reasons.append("Missing/invalid evidence: " + str(exc))
    return {"verdict": "UNVERIFIED" if reasons else "PASS_LOCAL_LOOPBACK", "reasons": reasons,
            "scope": "Only tested local endpoints/window; not external networking or production isolation"}
