"""Bounded native evidence contract. Never issue a production certificate."""
from __future__ import annotations
import ctypes
import hashlib
import json
import socket
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
POINTS = {
    'udp': ('D7', 'D8', 'D9', 'D10'),
    'exe': ('C6', 'C7', 'D9', 'D11', 'D12', 'F1', 'F4'),
    'ipc': ('D12', 'D13', 'F2', 'F3', 'F4', 'F5', 'F6'),
    'ipc4': ('F2', 'F3', 'F4', 'F5'),
}


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def error_record(exc):
    number = getattr(exc, 'winerror', None)
    return {'outcome': 'os_denied' if number == 10013 else 'error',
            'winerror': number, 'errno': getattr(exc, 'errno', None),
            'error_type': type(exc).__name__, 'detail': str(exc)}


def classify_delivery(state, packets, nonces, complete, observation_ns):
    """Exact phase correlation. No substring tests or packet-count subtraction."""
    if nonces['sandbox'] in packets:
        return 'FAIL'
    controls = (packets.count(nonces['before']) == 1
                and packets.count(nonces['after']) == 1)
    if not controls or not complete or observation_ns < 20_000_000_000:
        return 'UNKNOWN'
    if state.get('outcome') == 'os_denied' and state.get('winerror') == 10013:
        return 'SCOPED_PASS'
    if state.get('outcome') in ('sent', 'completed'):
        return 'BOUNDED_NO_DELIVERY'
    return 'UNKNOWN'


def classify_permission(state, healthy):
    if not healthy:
        return 'UNKNOWN'
    if state.get('outcome') == 'allowed':
        return 'FAIL'
    if state.get('outcome') == 'os_denied' and state.get('winerror') == 5:
        return 'SCOPED_PASS'
    return 'UNKNOWN'


def parse_observations(transport):
    if transport.get('rc') != 0:
        raise ValueError('Probe did not finish successfully')
    data = json.loads(transport['stdout'])
    if not isinstance(data, dict):
        raise ValueError('Probe output must be one complete JSON object')
    return data


def validate_transport(transport, code):
    from animtrain.isolation_evidence import _parent
    _parent(transport['parent_evidence'])
    work = Path(transport['work']).resolve()
    allowed = ROOT / 'reviews/codex-supervision/2026-10-05-three-gates'
    if not work.is_relative_to(allowed) or not work.name.startswith('execution-'):
        raise ValueError('Unreviewed transport work directory')
    source = work / 'scene.py'
    if source.read_text(encoding='utf-8') != code:
        raise ValueError('Executed code differs from reviewed generated code')
    if digest(source) != transport['source_sha256']:
        raise ValueError('Source byte binding changed')
    expected = [str((ROOT / '.venv/Scripts/python.exe').resolve()), '-I', '-B', str(source)]
    if transport['command'] != expected:
        raise ValueError('Unreviewed native command')
    for name in ('stdout', 'stderr'):
        actual = (work / (name + '.txt')).read_bytes()
        if actual.decode('utf-8', 'replace') != transport[name]:
            raise ValueError('Saved transport stream differs: ' + name)
    return parse_observations(transport)


def save_exclusive(path, report):
    path = Path(path)
    if path.parent.resolve() != HERE:
        raise ValueError('Evidence must stay in the named probe directory')
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(report, ensure_ascii=False, indent=2) + '\n')


class Receiver:
    """Owned loopback endpoint; bounded I/O, exact payloads, explicit lifecycle."""
    def __init__(self, kind, family=socket.AF_INET):
        self.kind = kind
        self.packets = []
        self.errors = []
        self.stop = threading.Event()
        self.complete = False
        self.sock = socket.socket(family, socket.SOCK_DGRAM if kind == 'udp' else socket.SOCK_STREAM)
        address = '127.0.0.1' if family == socket.AF_INET else '::1'
        self.sock.bind((address, 0))
        self.endpoint = self.sock.getsockname()
        self.sock.settimeout(1/5)
        if kind == 'http':
            self.sock.listen(8)
        self.thread = threading.Thread(target=self._receive, daemon=True)
        self.thread.start()

    def _receive(self):
        try:
            while not self.stop.is_set():
                try:
                    if self.kind == 'udp':
                        data, _ = self.sock.recvfrom(4096)
                        self.packets.append(data.decode('ascii'))
                    else:
                        conn, _ = self.sock.accept()
                        with conn:
                            conn.settimeout(1)
                            data = b''
                            while b'\r\n\r\n' not in data and len(data) <= 4096:
                                block = conn.recv(1024)
                                if not block:
                                    break
                                data += block
                            line = data.split(b'\r\n', 1)[0]
                            parts = line.split(b' ')
                            if len(parts) != 3 or parts[0] != b'GET':
                                raise ValueError('Invalid control HTTP request')
                            self.packets.append(parts[1].decode('ascii').removeprefix('/'))
                            conn.sendall(b'HTTP/1.1 200 OK\r\nContent-Length: 2\r\nConnection: close\r\n\r\nok')
                except socket.timeout:
                    continue
                except OSError as exc:
                    if not self.stop.is_set():
                        self.errors.append(error_record(exc))
                    break
                except Exception as exc:
                    self.errors.append({'error_type': type(exc).__name__, 'detail': str(exc)})
        finally:
            self.complete = True

    def close(self):
        self.stop.set()
        self.sock.close()
        self.thread.join(timeout=3)
        if self.thread.is_alive():
            self.errors.append({'error_type': 'ReceiverNotStopped'})
        self.complete = self.complete and not self.thread.is_alive() and not self.errors


def wait_packet(receiver, nonce, seconds=3):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if nonce in receiver.packets or receiver.errors:
            break
        time.sleep(1/50)
    return receiver.packets.count(nonce) == 1


def host_control(receiver, nonce):
    try:
        family = receiver.sock.family
        with socket.socket(family, socket.SOCK_DGRAM if receiver.kind == 'udp' else socket.SOCK_STREAM) as client:
            client.settimeout(3)
            if receiver.kind == 'udp':
                client.sendto(nonce.encode('ascii'), receiver.endpoint)
            else:
                client.connect(receiver.endpoint)
                client.sendall(('GET /' + nonce + ' HTTP/1.1\r\nHost: fixture\r\nConnection: close\r\n\r\n').encode('ascii'))
                response = client.recv(1024)
                if not response.startswith(b'HTTP/1.1 200 OK'):
                    raise ValueError('Control response missing')
        return {'received_exactly_once': wait_packet(receiver, nonce)}
    except Exception as exc:
        return {'received_exactly_once': False, 'error_type': type(exc).__name__, 'detail': str(exc)}


# These declarations are embedded verbatim into the AppContainer source.
# No clipboard API is exposed. All HANDLE results are pointer-sized.
WIN32_SOURCE = r'''
import ctypes
from ctypes import wintypes
INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
def bind_kernel32():
    dll=ctypes.WinDLL('kernel32',use_last_error=True)
    signatures={
      'CloseHandle':([wintypes.HANDLE],wintypes.BOOL),
      'CreateFileW':([wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,ctypes.c_void_p,wintypes.DWORD,wintypes.DWORD,wintypes.HANDLE],wintypes.HANDLE),
      'CreateNamedPipeW':([wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,wintypes.DWORD,wintypes.DWORD,wintypes.DWORD,wintypes.DWORD,ctypes.c_void_p],wintypes.HANDLE),
      'DisconnectNamedPipe':([wintypes.HANDLE],wintypes.BOOL),
      'ConnectNamedPipe':([wintypes.HANDLE,ctypes.c_void_p],wintypes.BOOL),
      'CreateMailslotW':([wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,ctypes.c_void_p],wintypes.HANDLE),
      'CreateFileMappingW':([wintypes.HANDLE,ctypes.c_void_p,wintypes.DWORD,wintypes.DWORD,wintypes.DWORD,wintypes.LPCWSTR],wintypes.HANDLE),
      'OpenFileMappingW':([wintypes.DWORD,wintypes.BOOL,wintypes.LPCWSTR],wintypes.HANDLE),
    }
    for name,(args,result) in signatures.items():
        fn=getattr(dll,name);fn.argtypes=args;fn.restype=result
    return dll
def invalid_handle(handle):
    return handle in (None,0,-1,INVALID_HANDLE_VALUE)
LRESULT=ctypes.c_ssize_t
WNDPROC=ctypes.WINFUNCTYPE(LRESULT,wintypes.HWND,wintypes.UINT,wintypes.WPARAM,wintypes.LPARAM)
class WNDCLASSW(ctypes.Structure):
    _fields_=[('style',wintypes.UINT),('lpfnWndProc',WNDPROC),('cbClsExtra',ctypes.c_int),('cbWndExtra',ctypes.c_int),('hInstance',wintypes.HINSTANCE),('hIcon',wintypes.HICON),('hCursor',wintypes.HANDLE),('hbrBackground',wintypes.HANDLE),('lpszMenuName',wintypes.LPCWSTR),('lpszClassName',wintypes.LPCWSTR)]
'''