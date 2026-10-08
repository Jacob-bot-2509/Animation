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
import math
import socket
import threading
import time
from ctypes import wintypes

LOCAL_LOOPBACK_CONTRACT = "local-loopback-os-policy-v1"
CONTRACT_HISTORY = (
    "Replaces the WSAEACCES-10013-only contract with read-only OS policy, "
    "actual token identity and same-endpoint before/after controls; rationale: "
    "D:/Animation-Model-Training/reviews/codex-supervision/history-from-code/network-core-fix-2026-10-04/FIX_REPORT.md"
)


def token_identity(process_handle=None) -> dict:
    """Query a real process token; default is the calling process.

    A parent may pass the suspended child handle before any user code runs.
    """
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
        if not a.OpenProcessToken(k.GetCurrentProcess() if process_handle is None else process_handle, 8, ctypes.byref(handle)):
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
                if k.LocalFree(text):
                    raise OSError("LocalFree failed for exemption SID string")
        result.update(api_ok=True, sids=sorted(sids))
    except Exception as exc:
        result["error"] = repr(exc)
    finally:
        if array:
            try:
                heap = k.GetProcessHeap()
                if count.value <= 10000:
                    for index in range(count.value):
                        try:
                            if array[index].Sid and not k.HeapFree(heap, 0, array[index].Sid):
                                result["cleanup_ok"] = False
                        except Exception as exc:
                            result.update(cleanup_ok=False, cleanup_error=repr(exc))
                else:
                    result["cleanup_ok"] = False
                if not k.HeapFree(heap, 0, array):
                    result["cleanup_ok"] = False
            except Exception as exc:
                result.update(cleanup_ok=False, cleanup_error=repr(exc))
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
        try:
            self.thread = threading.Thread(target=self._receive, daemon=True)
            self.thread.start()
        except BaseException:
            self.socket.close()
            raise

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
        except Exception as exc:
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


def _sid_key(value):
    """Compare bounded decimal SID components, preserving the raw evidence text.

    Windows accepts both 's' and 'S' and decimal components with leading zeros.
    Unsupported/malformed encodings are unknown, never a non-exempt SID.
    """
    if not isinstance(value, str):
        raise ValueError("SID must be a string")
    parts = value.split("-")
    if not 3 <= len(parts) <= 18 or parts[0] not in ("s", "S") or any(
        not part.isascii() or not part.isdecimal() for part in parts[1:]
    ):
        raise ValueError("Invalid decimal SID")
    numbers = tuple(int(part, 10) for part in parts[1:])
    if numbers[0] != 1 or numbers[1] >= 1 << 48 or any(n >= 1 << 32 for n in numbers[2:]):
        raise ValueError("SID component out of range")
    return numbers


def judge_loopback_evidence(record: dict) -> dict:
    """Require OS configuration + token identity + same-endpoint bracketing.

    Silent drop alone, an API error, unknown state or an absent control never passes.
    This uses a different, explicit evidence contract from WSAEACCES-only acceptance.
    """
    if not isinstance(record, dict):
        return {"verdict": "UNVERIFIED", "reasons": ["Evidence must be an object"],
                "contract": LOCAL_LOOPBACK_CONTRACT}
    nonce = record.get("nonces", {})
    packets = record.get("packets", [])
    if not isinstance(nonce, dict) or not isinstance(packets, list):
        return {"verdict": "UNVERIFIED", "reasons": ["Malformed nonce/packet evidence"]}
    payloads = []
    for packet in packets:
        try:
            payloads.append(bytes.fromhex(packet["hex"]) if isinstance(packet, dict) else None)
        except (KeyError, TypeError, ValueError):
            payloads.append(None)
    probe = nonce.get("sandbox")
    if isinstance(probe, str) and len(probe) == 32 and probe.isascii() and any(
        payload is not None and probe.encode("ascii") in payload for payload in payloads
    ):
        # Case/spacing in hex and extra wire bytes cannot erase known delivery.
        return {"verdict": "FAIL", "reasons": ["Sandbox nonce received in packet payload"],
                "contract": LOCAL_LOOPBACK_CONTRACT}
    if any(payload is None for payload in payloads):
        return {"verdict": "UNVERIFIED", "reasons": ["Malformed packet evidence"]}
    if set(nonce) != {"before", "sandbox", "after"} or any(
        not isinstance(n, str) or len(n) != 32 or not n.isascii() for n in nonce.values()
    ) or len(set(nonce.values())) != 3:
        return {"verdict": "UNVERIFIED", "reasons": ["Invalid/ambiguous nonces"],
                "contract": LOCAL_LOOPBACK_CONTRACT}
    reasons = []
    def timestamp(value):
        return type(value) in (int, float) and math.isfinite(value) and value >= 0
    try:
        if not isinstance(record["host"], str) or not ipaddress.ip_address(record["host"]).is_loopback or record["transport"] not in ("tcp", "udp"):
            reasons.append("Only literal loopback TCP/UDP is covered")
        expected = record["expected_sid"]
        expected_key = _sid_key(expected)
        if len(expected_key) < 4 or expected_key[:3] != (1, 15, 2):
            raise ValueError("Invalid expected AppContainer SID")
        if type(record["port"]) is not int or not 0 < record["port"] < 65536:
            raise ValueError("Invalid endpoint port")
        configs = [record["policy_before"], record["policy_after"]]
        policy_keys = []
        for config in configs:
            if not isinstance(config, dict): raise ValueError("Policy query is not an object")
            if config.get("api_ok") is not True or type(config.get("return_code")) is not int or config.get("return_code") != 0 or config.get("cleanup_ok") is not True:
                reasons.append("Loopback policy query failed")
            if not isinstance(config.get("sids"), list):
                raise ValueError("Exemption list unknown")
            keys = [_sid_key(sid) for sid in config["sids"]]
            policy_keys.append(sorted(keys))
            if expected_key in keys or len(keys) != len(set(keys)):
                reasons.append("Exemption list unknown or tested SID exempt")
        if policy_keys[0] != policy_keys[1]: reasons.append("Policy changed during test")
        if record["runtime_integrity"] is not True: reasons.append("Runtime/client integrity not confirmed")
        if not isinstance(record["server_errors"], list) or record["server_errors"] or record["server_complete"] is not True:
            reasons.append("Receiver failed, unknown or unfinished")
        if not timestamp(record["server_started"]) or not timestamp(record["server_closed"]) or record["server_started"] > record["server_closed"]:
            raise ValueError("Invalid listener timestamps")
        if any(not timestamp(p.get("at")) or not record["server_started"] <= p["at"] <= record["server_closed"] for p in packets):
            reasons.append("Packet outside listener lifetime or invalid timestamp")
        expected_payloads = {n.encode("ascii") for n in nonce.values()}
        if any(payload not in expected_payloads for payload in payloads): reasons.append("Unattributed network data")
        for side in ("before", "sandbox", "after"):
            client = record["clients"][side]
            if not isinstance(client, dict): raise ValueError(side + " client is not an object")
            data = client.get("data")
            if not isinstance(data, dict): raise ValueError(side + " client data is not an object")
            token = data.get("token")
            if not isinstance(token, dict): raise ValueError(side + " token is not an object")
            if type(client.get("rc")) is not int or client.get("rc") != 0 or client.get("timed_out") is not False or token.get("api_ok") is not True:
                reasons.append(side + " client/token incomplete")
            if (data.get("host"), data.get("port"), data.get("transport"), data.get("nonce")) != (record["host"], record["port"], record["transport"], nonce[side]):
                reasons.append(side + " endpoint/nonce mismatch")
            if not timestamp(data.get("started")) or not timestamp(data.get("finished")):
                raise ValueError(side + " invalid client timestamps")
            if not record["server_started"] <= data["started"] < data["finished"] <= record["server_closed"]:
                reasons.append(side + " attempt outside listener lifetime")
            if side == "sandbox":
                if token.get("is_appcontainer") is not True or _sid_key(token.get("sid")) != expected_key or type(token.get("capability_count")) is not int or token.get("capability_count") != 0:
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
                matches = [p for p, payload in zip(packets, payloads) if payload == nonce[side].encode("ascii")]
                if len(matches) != 1: reasons.append(side + " nonce not uniquely received")
                elif not timestamp(matches[0].get("at")) or matches[0]["at"] < data["started"]:
                    reasons.append(side + " packet predates its client")
                if side == "before" and any(p["at"] > record["clients"]["sandbox"]["data"]["started"] for p in matches):
                    reasons.append("Before control packet received after sandbox start")
                if side == "after" and any(p["at"] < record["clients"]["sandbox"]["data"]["finished"] for p in matches):
                    reasons.append("After control packet received before sandbox completion")
        before, sb, after = [record["clients"][side]["data"] for side in ("before", "sandbox", "after")]
        if not before["finished"] <= sb["started"] <= sb["finished"] <= after["started"]:
            reasons.append("Control/sandbox ordering invalid")
        if after["started"] - sb["finished"] < 20:
            reasons.append("Observation window shorter than 20 seconds")
    except (KeyError, TypeError, ValueError, AttributeError, OverflowError) as exc:
        reasons.append("Missing/invalid evidence: " + str(exc))
    return {"verdict": "UNVERIFIED" if reasons else "PASS_LOCAL_LOOPBACK", "reasons": reasons,
            "scope": "Only tested local endpoints/window; not external networking or production isolation",
            "contract": LOCAL_LOOPBACK_CONTRACT}
