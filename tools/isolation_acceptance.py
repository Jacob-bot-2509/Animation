"""B4 AppContainer 隔离验收套件(执行方 Claude Code,监督方 Codex)。

逐项验收(复查方 RESULT.md 的剩余范围):
  P1 本机 TCP 回环:沙箱内 _socket connect 必须被 OS 拒绝(回归)
  P2 外网 TCP:沙箱内连接外网地址必须被 OS 拒绝
  P3 UDP:沙箱内 sendto 必须被 OS 拒绝
  P4 IPv6:沙箱内 ::1 连接必须被 OS 拒绝
  P5 子进程树:沙箱内 python 派生的子 python 仍受沙箱约束(令牌继承)
  P6 Manim 渲染链:沙箱内真实 manim 渲染(MathTex)必须成功
  P7 超时终止:超时后进程树终止(fail-closed)
每项有普通进程正对照(control)与沙箱进程对照;证据写
reviews/2026-10-04-isolation-acceptance/。

约定:不改 Codex 的 appcontainer.py;profile 用生产名显式创建(幂等,
已获用户允许写 C 盘普通用户目录);ACL 只加 D 盘自有目录。
"""
from __future__ import annotations

import argparse
import ctypes
import json
import socket
import subprocess
import sys
from ctypes import wintypes
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain import appcontainer as ac  # noqa: E402

OUT = ROOT / "reviews" / "2026-10-04-isolation-acceptance"
SANDBOX_PY = Path(r"D:\Python\python.exe")
VENV_PY = ROOT / ".venv" / "Scripts" / "python.exe"
WORK = ROOT / ".render-tmp"
FFMPEG_BIN = Path(r"D:\Settings\ffmpeg\bin")
MIKTEX_BIN = Path(r"D:\Settings\miktex\miktex\bin\x64")

# 带正确原型的令牌探针(GetCurrentProcess/OpenProcessToken 必须 HANDLE 口径,
# 否则 64 位句柄被截断为 32 位 int → STATUS_INVALID_HANDLE 0xc0000008)
TOKEN_PROBE = (
    "import ctypes\n"
    "from ctypes import wintypes\n"
    "k=ctypes.windll.kernel32;a=ctypes.windll.advapi32\n"
    "k.GetCurrentProcess.restype=wintypes.HANDLE\n"
    "k.OpenProcessToken.restype=wintypes.BOOL\n"
    "k.OpenProcessToken.argtypes=[wintypes.HANDLE,wintypes.DWORD,"
    "ctypes.POINTER(wintypes.HANDLE)]\n"
    "a.GetTokenInformation.restype=wintypes.BOOL\n"
    "a.GetTokenInformation.argtypes=[wintypes.HANDLE,ctypes.c_int,"
    "wintypes.LPVOID,wintypes.DWORD,ctypes.POINTER(wintypes.DWORD)]\n"
    "h=wintypes.HANDLE()\n"
    "ok1=k.OpenProcessToken(k.GetCurrentProcess(),0x0008,ctypes.byref(h))\n"
    "val=wintypes.DWORD();dummy=wintypes.DWORD()\n"
    "ok2=a.GetTokenInformation(h,26,ctypes.byref(val),4,ctypes.byref(dummy))\n"
    "print('TOKEN_APPCONTAINER='+str(bool(val.value))"
    "+' ok='+str(ok1)+'/'+str(ok2))\n"
)

_TCP_LOOP = (
    TOKEN_PROBE +
    "import _socket\n"
    "s=_socket.socket(_socket.AF_INET,_socket.SOCK_STREAM)\n"
    "try:\n"
    "    s.connect(('127.0.0.1',{port}))\n"
    "    print('CONNECTED')\n"
    "except OSError as e:\n"
    "    print('BLOCKED:'+str(e))\n"
)
_TCP_EXT = (
    "import _socket\n"
    "s=_socket.socket(_socket.AF_INET,_socket.SOCK_STREAM)\n"
    "s.settimeout(5)\n"
    "try:\n"
    "    s.connect(('8.8.8.8',53))\n"
    "    print('CONNECTED')\n"
    "except OSError as e:\n"
    "    print('BLOCKED:'+str(e))\n"
)
_UDP_EXT = (
    "import _socket\n"
    "s=_socket.socket(_socket.AF_INET,_socket.SOCK_DGRAM)\n"
    "try:\n"
    "    s.sendto(b'probe',('8.8.8.8',53))\n"
    "    print('SENT')\n"
    "except OSError as e:\n"
    "    print('BLOCKED:'+str(e))\n"
)
_UDP = (
    "import _socket\n"
    "s=_socket.socket(_socket.AF_INET,_socket.SOCK_DGRAM)\n"
    "try:\n"
    "    s.sendto(b'probe',('127.0.0.1',{port}))\n"
    "    print('SENT')\n"
    "except OSError as e:\n"
    "    print('BLOCKED:'+str(e))\n"
)
_IPV6 = (
    "import _socket\n"
    "try:\n"
    "    s=_socket.socket(_socket.AF_INET6,_socket.SOCK_STREAM)\n"
    "    s.connect(('::1',{port}))\n"
    "    print('CONNECTED')\n"
    "except OSError as e:\n"
    "    print('BLOCKED:'+str(e))\n"
)
_SUBPROC = (
    "import os,subprocess,sys\n"
    "child_file=os.path.join(os.environ['TEMP'],'child_probe.py')\n"
    "env=dict(os.environ);env['PROBE_PORT']=os.environ['PROBE_PORT']\n"
    "r=subprocess.run([sys.executable,'-X','utf8',child_file],"
    "capture_output=True,text=True,timeout=60,env=env)\n"
    "print('CHILD_RC='+str(r.returncode))\n"
    "print(r.stdout)\n"
    "print(r.stderr[-200:])\n"
)
CHILD_PROBE_FILE = (
    "import os,_socket\n"
    "s=_socket.socket(_socket.AF_INET,_socket.SOCK_STREAM)\n"
    "try:\n"
    "    s.connect(('127.0.0.1',int(os.environ['PROBE_PORT'])))\n"
    "    print('CHILD_CONNECTED')\n"
    "except OSError as e:\n"
    "    print('CHILD_BLOCKED:'+str(e))\n"
)
_SLEEP = "import time\ntime.sleep(60)\n"


def provision_profile() -> dict:
    """创建生产 profile(幂等):已存在(HRESULT 0x800700B7)→ 视为成功。"""
    if not getattr(ac._u32.CreateAppContainerProfile, "argtypes", None):
        ac._u32.CreateAppContainerProfile.argtypes = [
            wintypes.LPCWSTR, wintypes.LPCWSTR, wintypes.LPCWSTR,
            ctypes.POINTER(ctypes.c_void_p), wintypes.DWORD,
            ctypes.POINTER(wintypes.LPVOID)]
        ac._u32.CreateAppContainerProfile.restype = ctypes.c_long
    sid = ac.appcontainer_sid()
    caps = ctypes.POINTER(ctypes.c_void_p)()
    out_sid = wintypes.LPVOID()
    hr = ac._u32.CreateAppContainerProfile(
        ac.APPCONTAINER_NAME, ac.APPCONTAINER_NAME, ac.APPCONTAINER_NAME,
        caps, 0, ctypes.byref(out_sid))
    if hr != 0 and (hr & 0xFFFFFFFF) != 0x800700B7:
        raise OSError(hr, f"CreateAppContainerProfile HRESULT 0x{hr & 0xffffffff:08X}")
    profile = ac.appcontainer_profile_path(sid)
    return {"hresult": hr, "profile": str(profile), "already_exists": bool(hr)}


def sandbox_env(profile: Path) -> dict:
    return {
        "SYSTEMROOT": r"C:\Windows",
        "PATH": ";".join([str(SANDBOX_PY.parent), str(FFMPEG_BIN), str(MIKTEX_BIN),
                          str(VENV_PY.parent), r"C:\Windows\System32"]),
        "TEMP": str(WORK), "TMP": str(WORK),
        "LOCALAPPDATA": str(profile), "APPDATA": str(profile),
        "USERPROFILE": str(profile),
        "MPLCONFIGDIR": str(WORK / "mpl"), "HOME": str(WORK),
        "USERNAME": "sandbox", "COMPUTERNAME": "SANDBOX",
        "PATHEXT": ".COM;.EXE;.BAT;.CMD",
    }


def run_sandbox(code: str, profile: Path, timeout_ms: int = 60_000,
                extra_env: dict | None = None):
    env = sandbox_env(profile)
    if extra_env:
        env.update(extra_env)
    return ac.run_appcontainer(
        [str(SANDBOX_PY), "-X", "utf8", "-c", code],
        cwd=WORK, env=env,
        allowed_dirs=[(SANDBOX_PY.parent, False), (WORK, True),
                      (FFMPEG_BIN, False), (MIKTEX_BIN.parent, False),
                      (VENV_PY.parent.parent, False)],
        timeout_ms=timeout_ms)


def run_control(code: str):
    import os
    env = dict(os.environ)
    env["TEMP"] = str(WORK); env["TMP"] = str(WORK)
    return subprocess.run([str(SANDBOX_PY), "-X", "utf8", "-c", code],
                          capture_output=True, timeout=60, env=env, cwd=str(WORK))


def _bound_port(family: int, socktype: int, listeners: list) -> int:
    s = socket.socket(family, socktype)
    s.bind(("127.0.0.1" if family == socket.AF_INET else "::1", 0))
    if socktype == socket.SOCK_STREAM:
        s.listen(1)
    listeners.append(s)
    return s.getsockname()[1]


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-render", action="store_true")
    ap.add_argument("--skip-profile", action="store_true")
    args = ap.parse_args(argv)
    OUT.mkdir(parents=True, exist_ok=True)
    WORK.mkdir(parents=True, exist_ok=True)
    (WORK / "mpl").mkdir(parents=True, exist_ok=True)
    results: dict[str, dict] = {}
    if args.skip_profile:
        prov = {"hresult": 0, "profile": "skipped", "already_exists": True}
        profile = ac.appcontainer_profile_path(ac.appcontainer_sid())
    else:
        prov = provision_profile()
        profile = Path(prov["profile"])
    results["profile"] = prov
    print(f"profile: {profile}")
    listeners: list = []

    def probe(pid: str, desc: str, code: str, port: int | None = None,
              timeout_ms: int = 60_000, control: bool = True,
              extra_env: dict | None = None):
        if port is not None:
            code = code.format(port=port)
        c = run_control(code) if control else None
        try:
            s = run_sandbox(code, profile, timeout_ms=timeout_ms,
                            extra_env=extra_env)
        except subprocess.TimeoutExpired:
            s = subprocess.CompletedProcess(["sandbox"], -9, b"", b"TIMEOUT_EXPIRED")
        results[pid] = {
            "desc": desc,
            "control_out": ((c.stdout if c else b"") or b"").decode("utf-8", "replace"),
            "sandbox_out": (s.stdout or b"").decode("utf-8", "replace"),
            "sandbox_err": (s.stderr or b"").decode("utf-8", "replace")[-800:],
            "sandbox_rc": s.returncode,
        }
        print(f"=== {pid}: {desc}")
        print(json.dumps(results[pid], ensure_ascii=False))

    try:
        probe("P1_tcp_loopback", "本机 TCP 回环(回归)", _TCP_LOOP,
              port=_bound_port(socket.AF_INET, socket.SOCK_STREAM, listeners))
        probe("P2_tcp_external", "外网 TCP(8.8.8.8:53)", _TCP_EXT)
        probe("P3_udp_sendto", "UDP sendto(本机回环监听)", _UDP,
              port=_bound_port(socket.AF_INET, socket.SOCK_DGRAM, listeners))
        probe("P3b_udp_external", "UDP sendto(外网 8.8.8.8:53)", _UDP_EXT)
        probe("P4_ipv6", "IPv6 ::1 连接", _IPV6,
              port=_bound_port(socket.AF_INET6, socket.SOCK_STREAM, listeners))
        (WORK / "child_probe.py").write_text(CHILD_PROBE_FILE, encoding="utf-8")
        _p5 = _bound_port(socket.AF_INET, socket.SOCK_STREAM, listeners)
        import os as _os
        _saved = _os.environ.get("PROBE_PORT")
        _os.environ["PROBE_PORT"] = str(_p5)
        try:
            probe("P5_subprocess_inherit", "子进程树令牌继承", _SUBPROC,
                  extra_env={"PROBE_PORT": str(_p5)})
        finally:
            if _saved is None:
                _os.environ.pop("PROBE_PORT", None)
            else:
                _os.environ["PROBE_PORT"] = _saved
        if not args.skip_render:
            probe("P6_manim_render", "Manim 渲染链", "", control=False)
            # P6 特殊:渲染实现见下,这里单独处理
        probe("P7_timeout_terminate", "超时终止(5s vs sleep 60)", _SLEEP,
              timeout_ms=5_000, control=False)
    finally:
        for s in listeners:
            try:
                s.close()
            except OSError:
                pass
    if not args.skip_render:
        results["P6_manim_render"] = probe_manim(profile)
        print(json.dumps(results["P6_manim_render"], ensure_ascii=False))
    (OUT / "results.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"证据 → {OUT / 'results.json'}")
    return 0


def probe_manim(profile: Path) -> dict:
    scene = WORK / "AcceptScene.py"
    scene.write_text(
        "from manim import *\n"
        "class AcceptScene(Scene):\n"
        "    def construct(self):\n"
        "        self.add(MathTex(r'x^2 + y^2 = 1'))\n",
        encoding="utf-8")
    media = WORK / "media"
    try:
        r = ac.run_appcontainer(
            [str(VENV_PY), "-X", "utf8", "-m", "manim", "-ql",
             "--media_dir", str(media), str(scene), "AcceptScene"],
            cwd=WORK, env=sandbox_env(profile),
            allowed_dirs=[(SANDBOX_PY.parent, False), (VENV_PY.parent.parent, False),
                          (FFMPEG_BIN, False), (MIKTEX_BIN.parent, False),
                          (WORK, True)],
            timeout_ms=300_000)
        return {"desc": "Manim 渲染链(沙箱内真实渲染 MathTex)",
                "rc": r.returncode,
                "stdout_tail": r.stdout.decode("utf-8", "replace")[-600:],
                "stderr_tail": r.stderr.decode("utf-8", "replace")[-600:]}
    except subprocess.TimeoutExpired:
        return {"desc": "Manim 渲染链", "rc": -9, "stderr_tail": "TIMEOUT_EXPIRED(300s)"}


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
