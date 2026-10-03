"""Windows Job Object 内存限制(B4,纯标准库 ctypes)。

把子进程挂入带 ProcessMemoryLimit/JobMemoryLimit 的 job:
- 超限分配失败 → 子进程崩溃(非零退出),不会拖垮宿主机;
- 超时/异常时 TerminateJobObject 整树清理(含 manim 派生的 latex/dvisvgm);
- 非 Windows 平台返回 None(如实:该平台未实施内存隔离)。

kernel32 语义:job 创建 → SetInformationJobObject(ExtendedLimit) →
Query 回读验证生效 → AssignProcessToJobObject(proc._handle)。
"""
from __future__ import annotations

import ctypes
import subprocess
import sys
from ctypes import wintypes

if sys.platform != "win32":
    class WindowsJob:  # 非 Windows 占位:不可用(如实)
        def __init__(self, memory_mb: int):
            raise OSError("WindowsJob 仅在 Windows 可用")
else:
    _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

    class _IO_COUNTERS(ctypes.Structure):
        _fields_ = [("ReadOperationCount", ctypes.c_ulonglong),
                    ("WriteOperationCount", ctypes.c_ulonglong),
                    ("OtherOperationCount", ctypes.c_ulonglong),
                    ("ReadTransferCount", ctypes.c_ulonglong),
                    ("WriteTransferCount", ctypes.c_ulonglong),
                    ("OtherTransferCount", ctypes.c_ulonglong)]

    class _JOBOBJECT_BASIC_LIMIT_INFORMATION(ctypes.Structure):
        _fields_ = [("PerProcessUserTimeLimit", ctypes.c_longlong),
                    ("PerJobUserTimeLimit", ctypes.c_longlong),
                    ("LimitFlags", ctypes.c_ulong),
                    ("MinimumWorkingSetSize", ctypes.c_size_t),
                    ("MaximumWorkingSetSize", ctypes.c_size_t),
                    ("ActiveProcessLimit", ctypes.c_ulong),
                    ("Affinity", ctypes.c_size_t),
                    ("PriorityClass", ctypes.c_ulong),
                    ("SchedulingClass", ctypes.c_ulong)]

    class _JOBOBJECT_EXTENDED_LIMIT_INFORMATION(ctypes.Structure):
        _fields_ = [("BasicLimitInformation",
                     _JOBOBJECT_BASIC_LIMIT_INFORMATION),
                    ("IoInfo", _IO_COUNTERS),
                    ("ProcessMemoryLimit", ctypes.c_size_t),
                    ("JobMemoryLimit", ctypes.c_size_t),
                    ("PeakProcessMemoryUsed", ctypes.c_size_t),
                    ("PeakJobMemoryUsed", ctypes.c_size_t)]

    _JOB_OBJECT_LIMIT_PROCESS_MEMORY = 0x00000100
    _JOB_OBJECT_LIMIT_JOB_MEMORY = 0x00000200
    _JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE = 0x00002000
    _JobObjectExtendedLimitInformation = 9

    def _assign_process(job_handle: int, proc_handle: int) -> int:
        """模块级间接调用(便于测试注入失败);返回 0 = 失败。"""
        return _kernel32.AssignProcessToJobObject(
            wintypes.HANDLE(job_handle), wintypes.HANDLE(proc_handle))

    class WindowsJob:
        """带内存上限的 Windows job;子进程挂入后整树受控。"""

        def __init__(self, memory_mb: int):
            self.memory_mb = int(memory_mb)
            self._handle = _kernel32.CreateJobObjectW(None, None)
            if not self._handle:
                raise OSError("CreateJobObject 失败: "
                              f"{ctypes.get_last_error()}")
            info = _JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
            limit = memory_mb * 1024 * 1024
            info.ProcessMemoryLimit = limit
            info.JobMemoryLimit = limit
            info.BasicLimitInformation.LimitFlags = (
                _JOB_OBJECT_LIMIT_PROCESS_MEMORY
                | _JOB_OBJECT_LIMIT_JOB_MEMORY
                | _JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE)
            ok = _kernel32.SetInformationJobObject(
                wintypes.HANDLE(self._handle),
                _JobObjectExtendedLimitInformation,
                ctypes.byref(info), ctypes.sizeof(info))
            if not ok:
                raise OSError("SetInformationJobObject 失败: "
                              f"{ctypes.get_last_error()}")
            # 回读验证:限制确实生效才敢宣称内存隔离
            readback = _JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
            ok2 = _kernel32.QueryInformationJobObject(
                wintypes.HANDLE(self._handle),
                _JobObjectExtendedLimitInformation,
                ctypes.byref(readback), ctypes.sizeof(readback), None)
            if not ok2 or readback.ProcessMemoryLimit != limit:
                raise OSError("Job 内存限制回读验证失败 —— 不宣称内存隔离")
            self.assigned: list[int] = []

        def assign(self, popen: subprocess.Popen) -> None:
            """把子进程挂入 job(其后续派生的 latex/dvisvgm 同受限制)。

            GS5:任何失败(含 ERROR_ACCESS_DENIED=5)一律抛 OSError——
            错误码 5 绝不意味着"新 job 已接管",吞错即假隔离。
            """
            handle = getattr(popen, "_handle", None)
            if not handle:
                raise OSError("无法取得子进程句柄,不能挂入 job")
            ok = _assign_process(self._handle, handle)
            if not ok:
                raise OSError("AssignProcessToJobObject 失败: "
                              f"{ctypes.get_last_error()}(fail-closed)")
            self.assigned.append(handle)

        def terminate(self) -> None:
            """终止 job 内全部进程(超时/异常清理,含子进程树)。"""
            _kernel32.TerminateJobObject(wintypes.HANDLE(self._handle), 1)

        def close(self) -> None:
            if getattr(self, "_handle", None):
                _kernel32.CloseHandle(wintypes.HANDLE(self._handle))
                self._handle = None
