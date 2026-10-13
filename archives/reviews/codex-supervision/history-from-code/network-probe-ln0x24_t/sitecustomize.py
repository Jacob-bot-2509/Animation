"""B4 网络隔离 shim(自动注入渲染子进程):封堵 Python socket 出口。"""
import socket

_MARKER = 'B4-network-isolation: blocked'

def _blocked(*args, **kwargs):
    raise ConnectionError(_MARKER)

socket.socket.connect = _blocked
socket.socket.connect_ex = _blocked
socket.socket.sendto = _blocked
socket.getaddrinfo = _blocked
