"""Fail-closed startup and cleanup contracts; native edge probes are separate."""
from __future__ import annotations

import ctypes
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from contextlib import ExitStack
from ctypes import wintypes
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
if sys.platform == "win32":
    from animtrain import appcontainer as ac


@unittest.skipUnless(sys.platform == "win32", "Windows process API required")
class TestAppContainerLifecycle(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.work = Path(self.stack.enter_context(tempfile.TemporaryDirectory()))
        self.events = []
        self.created_files = []
        self.handles = []
        self.attributes = {}
        self.flags = None
        self.patch(ac, "appcontainer_sid", return_value=b"synthetic sid")
        self.patch(ac, "appcontainer_profile_path", return_value=self.work)
        self.patch(ac, "grant_dir_access")
        self.job = mock.MagicMock()
        self.job.assign_handle.side_effect = lambda h: self.events.append("assign")
        self.job.terminate.side_effect = lambda: self.events.append("terminate_job")
        self.job.wait_empty.side_effect = lambda: self.events.append("wait_empty")
        self.job.close.side_effect = lambda: self.events.append("close_job")
        self.job.terminate_and_wait.side_effect = lambda: (self.job.terminate(), self.job.wait_empty())
        self.job_cls = self.patch(ac, "WindowsJob", return_value=self.job)

        def create_file(path, access, share, sa, disposition, flags, template):
            handle = 101 + len(self.handles)
            self.handles.append(handle)
            if path != "NUL":
                p = Path(path)
                self.created_files.append(p)
                p.write_bytes(b"captured stdout" if len(self.created_files) == 1 else b"captured stderr")
                self.assertEqual(disposition, 1)  # no truncating existing paths
            return handle

        def initialize(attributes, count, flags, size):
            self.assertEqual(count, 2)
            ctypes.cast(size, ctypes.POINTER(ctypes.c_size_t))[0] = 256
            return bool(attributes)

        def update(attributes, flags, key, value, size, previous, returned):
            if key == ac._PROC_THREAD_ATTRIBUTE_HANDLE_LIST:
                self.attributes[key] = list(ctypes.cast(
                    value, ctypes.POINTER(wintypes.HANDLE * 3)).contents)
            else:
                self.attributes[key] = True
            return 1

        def create_process(executable, command, psa, tsa, inherit, flags, env, cwd, si, pi):
            self.events.append("create_suspended")
            self.flags = flags
            self.assertTrue(inherit)
            self.assertTrue(flags & ac._CREATE_SUSPENDED)
            info = ctypes.cast(pi, ctypes.POINTER(ac._PROCESS_INFORMATION)).contents
            info.hProcess = 201
            info.hThread = 202
            return 1

        def resume(handle):
            self.events.append("resume")
            return 1

        def exit_code(handle, code):
            ctypes.cast(code, ctypes.POINTER(wintypes.DWORD))[0] = 0
            return 1

        self.create_file = self.patch(ac._k32, "CreateFileW", side_effect=create_file)
        self.patch(ac._k32, "InitializeProcThreadAttributeList", side_effect=initialize)
        self.update = self.patch(ac._k32, "UpdateProcThreadAttribute", side_effect=update)
        self.delete_attributes = self.patch(ac._k32, "DeleteProcThreadAttributeList")
        self.create_process = self.patch(ac._k32, "CreateProcessW", side_effect=create_process)
        self.resume = self.patch(ac._k32, "ResumeThread", side_effect=resume)
        self.wait = self.patch(ac._k32, "WaitForSingleObject", return_value=0)
        self.get_exit = self.patch(ac._k32, "GetExitCodeProcess", side_effect=exit_code)
        self.terminate_process = self.patch(ac._k32, "TerminateProcess", return_value=1)
        self.close = self.patch(ac._k32, "CloseHandle", return_value=1)

    def patch(self, target, name, **kwargs):
        return self.stack.enter_context(mock.patch.object(target, name, **kwargs))

    def run_sandbox(self):
        return ac.run_appcontainer(["synthetic.exe"], cwd=self.work,
            env={"Z": "last", "A": "first"}, allowed_dirs=[], timeout_ms=1000)

    def assert_cleanup(self, process=True):
        for p in self.created_files:
            self.assertFalse(p.exists())
        expected = self.handles + ([201, 202] if process else [])
        closed = [call.args[0] for call in self.close.call_args_list]
        self.assertEqual(Counter(closed), Counter(expected))

    def test_only_stdio_inherited_and_assigned_before_resume(self):
        r = self.run_sandbox()
        self.assertEqual(r.stdout, b"captured stdout")
        self.assertEqual(r.stderr, b"captured stderr")
        self.assertEqual(self.attributes[ac._PROC_THREAD_ATTRIBUTE_HANDLE_LIST], [101, 102, 103])
        self.assertEqual(self.events[:3], ["create_suspended", "assign", "resume"])
        self.assertIn("terminate_job", self.events)  # root exit kills background workers
        self.assertIn("wait_empty", self.events)
        self.assert_cleanup()

    def test_timeout_waits_entire_job_and_preserves_output(self):
        self.wait.side_effect = [ac._WAIT_TIMEOUT, 0]
        with self.assertRaises(subprocess.TimeoutExpired) as caught:
            self.run_sandbox()
        self.assertEqual(caught.exception.output, b"captured stdout")
        self.assertEqual(caught.exception.stderr, b"captured stderr")
        self.job.terminate.assert_called_once()
        self.job.wait_empty.assert_called_once()
        self.assert_cleanup()

    def test_assignment_failure_never_resumes_child(self):
        self.job.assign_handle.side_effect = OSError("assign denied")
        with self.assertRaisesRegex(OSError, "assign denied"):
            self.run_sandbox()
        self.resume.assert_not_called()
        self.terminate_process.assert_called_once_with(201, 1)
        self.assert_cleanup()

    def test_resume_failure_terminates_job(self):
        self.resume.side_effect = None
        self.resume.return_value = 0xffffffff
        with self.assertRaises(OSError):
            self.run_sandbox()
        self.job.terminate.assert_called_once()
        self.job.wait_empty.assert_called_once()
        self.assert_cleanup()

    def test_create_error_survives_cleanup(self):
        self.create_process.side_effect = None
        self.create_process.return_value = 0
        self.patch(ctypes, "get_last_error", return_value=5)
        self.delete_attributes.side_effect = lambda *a: ctypes.set_last_error(87)
        with self.assertRaises(OSError) as caught:
            self.run_sandbox()
        self.assertEqual(caught.exception.winerror, 5)
        self.resume.assert_not_called()
        self.assert_cleanup(process=False)

    def test_wait_failure_does_not_return_success(self):
        self.wait.side_effect = [0xffffffff, 0]
        with self.assertRaisesRegex(OSError, "wait failed"):
            self.run_sandbox()
        self.job.wait_empty.assert_called_once()
        self.assert_cleanup()

    def test_exit_code_failure_still_kills_tree(self):
        self.get_exit.side_effect = None
        self.get_exit.return_value = 0
        with self.assertRaises(OSError):
            self.run_sandbox()
        self.job.wait_empty.assert_called_once()
        self.assert_cleanup()

    def test_partial_file_creation_releases_previous_handle(self):
        self.create_file.side_effect = [101, ac._INVALID_HANDLE_VALUE]
        with self.assertRaises(OSError):
            self.run_sandbox()
        self.create_process.assert_not_called()
        self.close.assert_called_once_with(101)

    def test_handle_list_setup_failure_does_not_start_child(self):
        self.update.side_effect = [1, 0]
        with self.assertRaises(OSError):
            self.run_sandbox()
        self.create_process.assert_not_called()
        self.delete_attributes.assert_called_once()
        self.assert_cleanup(process=False)

    def test_job_creation_failure_does_not_start_child(self):
        self.job_cls.side_effect = OSError("job unavailable")
        with self.assertRaisesRegex(OSError, "job unavailable"):
            self.run_sandbox()
        self.create_process.assert_not_called()
        self.assert_cleanup(process=False)

    def test_tree_cleanup_failure_cannot_be_success(self):
        self.job.wait_empty.side_effect = TimeoutError("descendant remains")
        with self.assertRaisesRegex(TimeoutError, "descendant remains"):
            self.run_sandbox()
        self.job.close.assert_called_once()
        self.assert_cleanup()


if __name__ == "__main__":
    unittest.main()
