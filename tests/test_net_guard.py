"""B4 网络隔离测试:shim 封堵 Python socket 出口、死代理环境、
隔离状态如实。不依赖外网(连 127.0.0.1:9 失败快)。"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.net_guard import (  # noqa: E402
    NETWORK_BLOCK_MARKER, network_isolation_env, write_network_shim)
from animtrain.render_gate import _isolation_state  # noqa: E402

_PROBE = (
    "import socket\n"
    "try:\n"
    "    socket.socket().connect(('127.0.0.1', 9))\n"
    "    print('CONNECTED')\n"
    "except Exception as e:\n"
    "    print('ERR:' + str(e))\n"
)
_PROBE_GETADDR = (
    "import socket\n"
    "try:\n"
    "    socket.getaddrinfo('example.com', 80)\n"
    "    print('RESOLVED')\n"
    "except Exception as e:\n"
    "    print('ERR:' + str(e))\n"
)


def _run(probe: str, env_extra: dict | None = None):
    import os
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    if env_extra:
        env.update(env_extra)
    return subprocess.run([sys.executable, "-X", "utf8", "-c", probe],
                          capture_output=True, encoding="utf-8",
                          errors="replace", env=env, timeout=60)


class TestNetShim(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.shim_dir = write_network_shim(Path(self._tmp.name))

    def tearDown(self):
        self._tmp.cleanup()

    def test_shim_blocks_connect(self):
        out = _run(_PROBE, {"PYTHONPATH": str(self.shim_dir)})
        self.assertIn(NETWORK_BLOCK_MARKER, out.stdout)

    def test_shim_blocks_getaddrinfo(self):
        out = _run(_PROBE_GETADDR, {"PYTHONPATH": str(self.shim_dir)})
        self.assertIn(NETWORK_BLOCK_MARKER, out.stdout)

    def test_without_shim_no_marker(self):
        out = _run(_PROBE)
        self.assertNotIn(NETWORK_BLOCK_MARKER, out.stdout)

    def test_env_overrides_proxy_and_pythonpath(self):
        env = network_isolation_env({"PATH": "x"}, self.shim_dir)
        self.assertEqual(env["HTTP_PROXY"], "http://127.0.0.1:9")
        self.assertEqual(env["https_proxy"], "http://127.0.0.1:9")
        self.assertEqual(env["NO_PROXY"], "")
        self.assertIn(str(self.shim_dir), env["PYTHONPATH"])
        self.assertEqual(env["PATH"], "x")  # 原键保留

    def test_isolation_state_network_true(self):
        st = _isolation_state()
        self.assertIs(st["network_isolation"], True)
        self.assertIn("网络隔离", st["note"])


if __name__ == "__main__":
    unittest.main()
