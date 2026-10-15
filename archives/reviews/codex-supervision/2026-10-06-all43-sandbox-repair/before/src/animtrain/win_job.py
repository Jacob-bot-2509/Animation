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
import time
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
    _JobObjectBasicAccountingInformation = 1
    _JobObjectBasicProcessIdList = 3

    class _JOBOBJECT_BASIC_ACCOUNTING_INFORMATION(ctypes.Structure):
        _fields_ = [("TotalUserTime", ctypes.c_longlong),
                    ("TotalKernelTime", ctypes.c_longlong),
                    ("ThisPeriodTotalUserTime", ctypes.c_longlong),
                    ("ThisPeriodTotalKernelTime", ctypes.c_longlong),
                    ("TotalPageFaultCount", wintypes.DWORD),
                    ("TotalProcesses", wintypes.DWORD),
                    ("ActiveProcesses", wintypes.DWORD),
                    ("TotalTerminatedProcesses", wintypes.DWORD)]

    _kernel32.CreateJobObjectW.argtypes = [wintypes.LPVOID, wintypes.LPCWSTR]
    _kernel32.CreateJobObjectW.restype = wintypes.HANDLE
    _kernel32.SetInformationJobObject.argtypes = [
        wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD]
    _kernel32.SetInformationJobObject.restype = wintypes.BOOL
    _kernel32.QueryInformationJobObject.argtypes = [
        wintypes.HANDLE, ctypes.c_int, wintypes.LPVOID, wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD)]
    _kernel32.QueryInformationJobObject.restype = wintypes.BOOL
    _kernel32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    _kernel32.AssignProcessToJobObject.restype = wintypes.BOOL
    _kernel32.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
    _kernel32.TerminateJobObject.restype = wintypes.BOOL
    _kernel32.CloseHandle.argtypes = [wintypes.HANDLE]
    _kernel32.CloseHandle.restype = wintypes.BOOL
    _kernel32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    _kernel32.OpenProcess.restype = wintypes.HANDLE
    _kernel32.IsProcessInJob.argtypes = [wintypes.HANDLE, wintypes.HANDLE, ctypes.POINTER(wintypes.BOOL)]
    _kernel32.IsProcessInJob.restype = wintypes.BOOL
    _kernel32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    _kernel32.WaitForSingleObject.restype = wintypes.DWORD

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
                error = ctypes.get_last_error()
                self.close()
                raise ctypes.WinError(error)
            # 回读验证:限制确实生效才敢宣称内存隔离
            readback = _JOBOBJECT_EXTENDED_LIMIT_INFORMATION()
            ok2 = _kernel32.QueryInformationJobObject(
                wintypes.HANDLE(self._handle),
                _JobObjectExtendedLimitInformation,
                ctypes.byref(readback), ctypes.sizeof(readback), None)
            if (not ok2 or readback.ProcessMemoryLimit != limit
                    or readback.JobMemoryLimit != limit
                    or readback.BasicLimitInformation.LimitFlags != info.BasicLimitInformation.LimitFlags):
                self.close()
                raise OSError("Job 内存限制回读验证失败 —— 不宣称内存隔离")
            self.assigned: list[int] = []

        def assign(self, popen: subprocess.Popen) -> None:
            """把子进程挂入 job(其后续派生的 latex/dvisvgm 同受限制)。

            GS5:任何失败(含 ERROR_ACCESS_DENIED=5)一律抛 OSError——
            错误码 5 绝不意味着"新 job 已接管",吞错即假隔离。
            """
            handle = getattr(popen, "_handle", None)
            self.assign_handle(handle)

        def assign_handle(self, handle: int) -> None:
            """Assign a native process handle before its suspended thread resumes."""
            if not handle:
                raise OSError("无法取得子进程句柄,不能挂入 job")
            ok = _assign_process(self._handle, handle)
            if not ok:
                raise OSError("AssignProcessToJobObject 失败: "
                              f"{ctypes.get_last_error()}(fail-closed)")
            self.assigned.append(handle)

        def terminate(self) -> None:
            """终止 job 内全部进程(超时/异常清理,含子进程树)。"""
            if not _kernel32.TerminateJobObject(wintypes.HANDLE(self._handle), 1):
                raise ctypes.WinError(ctypes.get_last_error())

        def wait_empty(self, timeout_ms: int = 5000) -> None:
            """Wait for the job's entire process tree, not just its root, to exit."""
            deadline = time.monotonic() + timeout_ms / 1000
            while True:
                info = _JOBOBJECT_BASIC_ACCOUNTING_INFORMATION()
                if not _kernel32.QueryInformationJobObject(
                        wintypes.HANDLE(self._handle), _JobObjectBasicAccountingInformation,
                        ctypes.byref(info), ctypes.sizeof(info), None):
                    raise ctypes.WinError(ctypes.get_last_error())
                if info.ActiveProcesses == 0:
                    return
                if time.monotonic() >= deadline:
                    raise TimeoutError("Job process tree did not exit during cleanup")
                time.sleep(0.01)

        def terminate_and_wait(self, timeout_ms: int = 5000) -> None:
            """Keep member handles to await termination beyond job accounting.

            ActiveProcesses can reach zero before a member's process handle is
            signaled. Holding verified member handles also avoids PID reuse.
            TerminateJobObject stops the whole job, including racing children.
            """
            handles = []
            deadline = time.monotonic() + timeout_ms / 1000
            try:
                capacity = 16
                while True:
                    class ProcessIds(ctypes.Structure):
                        _fields_ = [("Assigned", wintypes.DWORD), ("Count", wintypes.DWORD),
                                    ("Ids", ctypes.c_size_t * capacity)]
                    info = ProcessIds()
                    if _kernel32.QueryInformationJobObject(
                            wintypes.HANDLE(self._handle), _JobObjectBasicProcessIdList,
                            ctypes.byref(info), ctypes.sizeof(info), None):
                        break
                    error = ctypes.get_last_error()
                    if error != 234:  # ERROR_MORE_DATA
                        raise ctypes.WinError(error)
                    if time.monotonic() >= deadline:
                        raise TimeoutError("Job member enumeration exceeded cleanup deadline")
                    capacity = max(capacity * 2, info.Assigned)
                for pid in info.Ids[:info.Count]:
                    handle = _kernel32.OpenProcess(0x100000 | 0x1000, False, pid)
                    if not handle:
                        error = ctypes.get_last_error()
                        if error == 87:  # Member already exited; no live PID.
                            continue
                        raise ctypes.WinError(error)
                    member = wintypes.BOOL()
                    try:
                        if not _kernel32.IsProcessInJob(
                                handle, wintypes.HANDLE(self._handle), ctypes.byref(member)):
                            raise ctypes.WinError(ctypes.get_last_error())
                        if member.value:
                            handles.append(handle)
                            handle = None
                    finally:
                        if handle:
                            _kernel32.CloseHandle(handle)
                self.terminate()
                self.wait_empty(max(0, int((deadline - time.monotonic()) * 1000)))
                for handle in handles:
                    remaining = max(0, int((deadline - time.monotonic()) * 1000))
                    wait = _kernel32.WaitForSingleObject(handle, remaining)
                    if wait != 0:
                        raise OSError(f"Job member termination wait failed: {wait}")
            finally:
                for handle in handles:
                    _kernel32.CloseHandle(handle)

        def close(self) -> None:
            if getattr(self, "_handle", None):
                handle = self._handle
                self._handle = None
                if not _kernel32.CloseHandle(wintypes.HANDLE(handle)):
                    raise ctypes.WinError(ctypes.get_last_error())
