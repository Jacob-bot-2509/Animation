"""AppContainer 沙箱机制测试(本机被系统拒绝时如实 SKIP,证据见
reviews/2026-10-03-sandbox-attempt/ATTEMPT.md)。"""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.appcontainer import (  # noqa: E402
    APPCONTAINER_NAME, appcontainer_sid)

SANDBOX_PY = Path(r"D:\Python\python.exe")
WORK_DIR = ROOT / ".render-tmp"


class TestAppContainer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if sys.platform != "win32" or not SANDBOX_PY.exists():
            raise unittest.SkipTest("需要 Windows + D:\\Python")
        # 本机 CreateProcess+AppContainer 被系统拒绝(4250),机制不可用:
        # 诚实 SKIP,而不是断言可用(不假绿)
        raise unittest.SkipTest(
            "AppContainer 进程创建在本机被系统拒绝(错误 4250,无管理员);"
            "机制保留待管理员路线,见 reviews/2026-10-03-sandbox-attempt/ATTEMPT.md")

    def test_sid_deterministic(self):
        self.assertEqual(appcontainer_sid(), appcontainer_sid())


if __name__ == "__main__":
    unittest.main()
