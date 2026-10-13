"""A zero job process count must not hide incomplete process termination."""
from __future__ import annotations

import ctypes
import sys
import unittest
from contextlib import ExitStack
from ctypes import wintypes
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
if sys.platform == 'win32':
    from animtrain import win_job as wj


@unittest.skipUnless(sys.platform == 'win32', 'Windows JobObject API required')
class TestJobTerminationCompletion(unittest.TestCase):
    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.job = object.__new__(wj.WindowsJob)
        self.job._handle = 999

        def query(job, kind, data, length, returned):
            if kind == 3:
                class Ids(ctypes.Structure):
                    _fields_ = [('Assigned', wintypes.DWORD), ('Count', wintypes.DWORD),
                                ('Ids', ctypes.c_size_t * 16)]
                value = ctypes.cast(data, ctypes.POINTER(Ids)).contents
                value.Assigned = value.Count = 1
                value.Ids[0] = 12345
            else:
                value = ctypes.cast(data, ctypes.POINTER(wj._JOBOBJECT_BASIC_ACCOUNTING_INFORMATION)).contents
                value.ActiveProcesses = 0
            return 1

        def member(process, job, out):
            ctypes.cast(out, ctypes.POINTER(wintypes.BOOL))[0] = True
            return 1

        self.stack.enter_context(mock.patch.object(wj._kernel32, 'QueryInformationJobObject', side_effect=query))
        self.stack.enter_context(mock.patch.object(wj._kernel32, 'OpenProcess', return_value=101))
        self.member = self.stack.enter_context(mock.patch.object(wj._kernel32, 'IsProcessInJob', side_effect=member))
        self.terminate = self.stack.enter_context(mock.patch.object(wj._kernel32, 'TerminateJobObject', return_value=1))
        self.wait = self.stack.enter_context(mock.patch.object(wj._kernel32, 'WaitForSingleObject', return_value=0))
        self.close = self.stack.enter_context(mock.patch.object(wj._kernel32, 'CloseHandle', return_value=1))

    def test_zero_accounting_count_still_waits_member_handle(self):
        self.job.terminate_and_wait()
        self.wait.assert_called_once()
        self.assertEqual(self.wait.call_args.args[0], 101)
        self.close.assert_called_once_with(101)

    def test_unsignaled_member_is_not_reported_as_complete(self):
        self.wait.return_value = 0x102
        with self.assertRaisesRegex(OSError, 'termination wait failed'):
            self.job.terminate_and_wait()
        self.close.assert_called_once_with(101)

    def test_recycled_pid_outside_job_is_never_waited(self):
        def outside(process, job, out):
            ctypes.cast(out, ctypes.POINTER(wintypes.BOOL))[0] = False
            return 1
        self.member.side_effect = outside
        self.job.terminate_and_wait()
        self.wait.assert_not_called()
        self.close.assert_called_once_with(101)


if __name__ == '__main__':
    unittest.main()
