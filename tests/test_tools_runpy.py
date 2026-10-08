"""执行入口回归：真实参数解析、退出消息和调用者argv恢复。"""
import importlib.util
import io
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("code_entry", ROOT / "tools/runpy.py")
entry = importlib.util.module_from_spec(spec)
spec.loader.exec_module(entry)


class TestCodeEntry(unittest.TestCase):
    def test_argparse_target_has_no_wrapper_argument(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "script with spaces.py"
            target.write_text("import argparse\nargparse.ArgumentParser().parse_args()\n",
                              encoding="utf-8")
            result = subprocess.run([sys.executable, str(ROOT / "tools/runpy.py"),
                                     str(target)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_exit_semantics_and_argv_restoration(self):
        original = sys.argv
        for expression, expected, message in (
                ("None", 0, ""), ("7", 7, ""), ("'explanation'", 1, "explanation\n")):
            with self.subTest(expression=expression), tempfile.TemporaryDirectory() as directory:
                target = Path(directory) / "exit.py"
                target.write_text(f"raise SystemExit({expression})\n", encoding="utf-8")
                stream = io.StringIO()
                with redirect_stderr(stream):
                    self.assertEqual(entry.main([str(target)]), expected)
                self.assertEqual(stream.getvalue(), message)
                self.assertIs(sys.argv, original)

    def test_exception_restores_argv(self):
        original = sys.argv
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "error.py"
            target.write_text("raise RuntimeError('probe')\n", encoding="utf-8")
            with redirect_stderr(io.StringIO()):
                self.assertEqual(entry.main([str(target)]), 1)
        self.assertIs(sys.argv, original)
