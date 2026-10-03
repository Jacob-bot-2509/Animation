"""Windows Job Object 内存隔离测试(B4)。

Windows 下:job 可创建/回读验证/挂入子进程/整树终止/超限进程崩溃。
非 Windows:如实跳过(平台未实施内存隔离)。
"""
from __future__ import annotations

import subprocess
import sys
import unittest

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

try:
    from animtrain.win_job import WindowsJob  # noqa: E402
    JOB_AVAILABLE = sys.platform == "win32"
except ImportError:
    JOB_AVAILABLE = False


@unittest.skipUnless(JOB_AVAILABLE, "仅 Windows 有 job object 内存隔离")
class TestWindowsJob(unittest.TestCase):
    def test_job_create_and_close(self):
        job = WindowsJob(64)
        job.close()

    def test_assign_and_terminate_kills_tree(self):
        job = WindowsJob(64)
        proc = subprocess.Popen(
            [sys.executable, "-c", "import time; time.sleep(30)"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            job.assign(proc)
            job.terminate()
            proc.wait(timeout=10)
        finally:
            proc.kill()
            proc.wait()
            job.close()

    def test_memory_limit_kills_overallocating_process(self):
        """64MB 上限;子进程分配 200MB 必须失败(非零退出),不拖垮宿主。"""
        job = WindowsJob(64)
        proc = subprocess.Popen(
            [sys.executable, "-c",
             "x = [bytearray(1024*1024) for _ in range(200)]; print(len(x))"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        job.assign(proc)
        try:
            proc.wait(timeout=60)
            self.assertNotEqual(proc.returncode, 0,
                                "超限分配竟然成功 —— 内存隔离未生效")
        finally:
            proc.kill()
            proc.wait()
            job.close()

    def test_isolation_state_reports_memory_implemented(self):
        from animtrain.render_gate import _isolation_state
        st = _isolation_state()
        self.assertEqual(st["memory_limit_mb"], 2048)
