"""B4 网络 best-effort guard(纯标准库,无需管理员权限):不可信渲染子进程的
Python 层网络出口封堵。**不是不可绕过的网络边界**:底层 _socket、不经
sitecustomize 的子 Python 均可绕过(msg_259 已实测)——network_isolation
必须保持 False/UNVERIFIED,本 guard 仅作纵深防御。

机制(两层,如实文档化,不宣称超出能力):
  1. sitecustomize shim(经 PYTHONPATH 注入子进程):封堵 Python 层 socket
     出口 —— socket.connect / connect_ex / sendto / getaddrinfo 一律抛
     ConnectionError(带标记串)。封住不可信生成代码的主要出网通道,
     同时封住 DNS 外带(getaddrinfo 也被禁)。
  2. 死代理环境:HTTP(S)_PROXY/ALL_PROXY(含小写)指向 127.0.0.1:9、
     NO_PROXY 置空 —— 代理感知的 HTTP 客户端快速失败。

如实边界(不假绿):
  - 只约束本进程族内的 Python 层网络出口;
  - 固定工具链子进程(latex/dvisvgm/ffmpeg,项目可信组件)不经 shim,
    其自身无网络行为;
  - OS 级沙箱(AppContainer/防火墙)需管理员权限,不在本机制范围。
"""
from __future__ import annotations

from pathlib import Path

NETWORK_BLOCK_MARKER = "B4-network-isolation: blocked"

NETWORK_SHIM = f'''\
"""B4 网络隔离 shim(自动注入渲染子进程):封堵 Python socket 出口。"""
import socket

_MARKER = {NETWORK_BLOCK_MARKER!r}

def _blocked(*args, **kwargs):
    raise ConnectionError(_MARKER)

socket.socket.connect = _blocked
socket.socket.connect_ex = _blocked
socket.socket.sendto = _blocked
socket.getaddrinfo = _blocked
'''

_DEAD_PROXY = "http://127.0.0.1:9"


def write_network_shim(directory: Path) -> Path:
    """在指定目录写入 sitecustomize.py(网络出口封堵),返回该目录。

    目录须由调用方保证唯一;写入失败抛 OSError(调用方 fail-closed)。
    """
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "sitecustomize.py").write_text(
        NETWORK_SHIM, encoding="utf-8")
    return directory


def network_isolation_env(env: dict, shim_dir: Path) -> dict:
    """在子进程环境上叠加网络隔离:PYTHONPATH 注入 shim + 死代理环境。

    返回新 dict,不修改调用方 env。
    """
    out = dict(env)
    existing = out.get("PYTHONPATH")
    out["PYTHONPATH"] = (str(shim_dir) + ";" + existing) if existing \
        else str(shim_dir)
    for key in ("HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
                "http_proxy", "https_proxy", "all_proxy"):
        out[key] = _DEAD_PROXY
    out["NO_PROXY"] = ""
    out["no_proxy"] = ""
    return out
