"""B4 AppContainer mechanism; not yet enabled in the render gate.

The previous attempt misread HRESULT S_OK=0 as failure and used an invalid
fallback SID; it does not establish an OS/admin restriction. Keep the gate
blocked until process, network and render integration are verified.

Mechanism:
  - DeriveAppContainerSidFromAppContainerName supplies the SID;
  - A provisioned AppContainer profile is required; SID derivation does not
    create a profile. This module never creates user profile storage implicitly.
  - SetEntriesInAclW 在自有 D 盘目录追加 ACE(TRUSTEE_IS_SID 需二进制
    SID 指针,实测修正);
  - STARTUPINFOEX + SECURITY_CAPABILITIES 启动,AppContainer 令牌无
    INTERNET_CLIENT 能力 → 出站被网络栈 OS 层拒绝。
"""
from __future__ import annotations

import ctypes
import subprocess
import sys
import uuid
from ctypes import wintypes
from pathlib import Path

from .win_job import WindowsJob

APPCONTAINER_NAME = "animtrain-render-sandbox"

_PROC_THREAD_ATTRIBUTE_SECURITY_CAPABILITIES = 0x00020009
_PROC_THREAD_ATTRIBUTE_HANDLE_LIST = 0x00020002
_EXTENDED_STARTUPINFO_PRESENT = 0x00080000
_CREATE_UNICODE_ENVIRONMENT = 0x00000400
_CREATE_SUSPENDED = 0x00000004
_STARTF_USESTDHANDLES = 0x00000100
_GRANT_ACCESS = 1  # ACCESS_MODE: NOT_USED=0, GRANT=1, SET=2, DENY=3
_SUB_CONTAINERS_AND_OBJECTS_INHERIT = 0x3
_TRUSTEE_IS_SID = 0
_SE_FILE_OBJECT = 1
_DACL_SECURITY_INFORMATION = 0x00000004
_GENERIC_READ = 0x80000000
_GENERIC_WRITE = 0x40000000
_GENERIC_EXECUTE = 0x20000000
_GENERIC_ALL = 0x10000000
_INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value
_WAIT_TIMEOUT = 0x00000102
_WAIT_OBJECT_0 = 0


class _SECURITY_CAPABILITIES(ctypes.Structure):
    _fields_ = [("AppContainerSid", wintypes.LPVOID),
                ("Capabilities", wintypes.LPVOID),
                ("CapabilityCount", wintypes.DWORD),
                ("Reserved", wintypes.DWORD)]


class _TRUSTEE_W(ctypes.Structure):
    _fields_ = [("pMultipleTrustee", wintypes.LPVOID),
                ("MultipleTrusteeOperation", ctypes.c_int),
                ("TrusteeForm", ctypes.c_int),
                ("TrusteeType", ctypes.c_int),
                ("ptstrName", wintypes.LPWSTR)]


class _EXPLICIT_ACCESS_W(ctypes.Structure):
    _fields_ = [("grfAccessPermissions", wintypes.DWORD),
                ("grfAccessMode", ctypes.c_int),
                ("grfInheritance", wintypes.DWORD),
                ("Trustee", _TRUSTEE_W)]


class _STARTUPINFOW(ctypes.Structure):
    _fields_ = [("cb", wintypes.DWORD), ("lpReserved", wintypes.LPWSTR),
                ("lpDesktop", wintypes.LPWSTR), ("lpTitle", wintypes.LPWSTR),
                ("dwX", wintypes.DWORD), ("dwY", wintypes.DWORD),
                ("dwXSize", wintypes.DWORD), ("dwYSize", wintypes.DWORD),
                ("dwXCountChars", wintypes.DWORD), ("dwYCountChars", wintypes.DWORD),
                ("dwFillAttribute", wintypes.DWORD), ("dwFlags", wintypes.DWORD),
                ("wShowWindow", wintypes.WORD), ("cbReserved2", wintypes.WORD),
                ("lpReserved2", wintypes.LPBYTE), ("hStdInput", wintypes.HANDLE),
                ("hStdOutput", wintypes.HANDLE), ("hStdError", wintypes.HANDLE)]


class _STARTUPINFOEXW(ctypes.Structure):
    _fields_ = [("StartupInfo", _STARTUPINFOW),
                ("lpAttributeList", wintypes.LPVOID)]


class _PROCESS_INFORMATION(ctypes.Structure):
    _fields_ = [("hProcess", wintypes.HANDLE), ("hThread", wintypes.HANDLE),
                ("dwProcessId", wintypes.DWORD), ("dwThreadId", wintypes.DWORD)]


class _SECURITY_ATTRIBUTES(ctypes.Structure):
    _fields_ = [("nLength", wintypes.DWORD), ("lpSecurityDescriptor", wintypes.LPVOID),
                ("bInheritHandle", wintypes.BOOL)]


_k32 = ctypes.WinDLL("kernel32", use_last_error=True)
_a32 = ctypes.WinDLL("advapi32", use_last_error=True)
_u32 = ctypes.WinDLL("userenv", use_last_error=True)
_ole32 = ctypes.WinDLL("ole32", use_last_error=True)

# ---- 显式原型声明(宽字符 API 必须 LPCWSTR,否则 str 被 ANSI 转换) ----
_LPV = wintypes.LPVOID
_PV = ctypes.POINTER(_LPV)
_u32.DeriveAppContainerSidFromAppContainerName.argtypes = [wintypes.LPCWSTR, _PV]
_u32.DeriveAppContainerSidFromAppContainerName.restype = ctypes.c_long  # HRESULT
_a32.IsValidSid.argtypes = [_LPV]
_a32.IsValidSid.restype = wintypes.BOOL
_a32.FreeSid.argtypes = [_LPV]
_a32.FreeSid.restype = _LPV
_u32.GetAppContainerFolderPath.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(wintypes.LPWSTR)]
_u32.GetAppContainerFolderPath.restype = ctypes.c_long
_ole32.CoTaskMemFree.argtypes = [_LPV]
_ole32.CoTaskMemFree.restype = None
_a32.ConvertSidToStringSidW.argtypes = [_LPV, ctypes.POINTER(wintypes.LPWSTR)]
_a32.ConvertSidToStringSidW.restype = wintypes.BOOL
_a32.GetLengthSid.argtypes = [_LPV]
_a32.GetLengthSid.restype = wintypes.DWORD
_a32.GetNamedSecurityInfoW.argtypes = [
    wintypes.LPCWSTR, ctypes.c_int, ctypes.c_uint,
    _PV, _PV, _PV, _PV, _PV]
_a32.GetNamedSecurityInfoW.restype = wintypes.DWORD
_a32.SetEntriesInAclW.argtypes = [
    wintypes.ULONG, ctypes.POINTER(_EXPLICIT_ACCESS_W), _LPV, _PV]
_a32.SetEntriesInAclW.restype = wintypes.DWORD
_a32.SetNamedSecurityInfoW.argtypes = [
    wintypes.LPCWSTR, ctypes.c_int, ctypes.c_uint, _LPV, _LPV, _LPV, _LPV]
_a32.SetNamedSecurityInfoW.restype = wintypes.DWORD
_k32.CreateFileW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD,
                             _LPV, wintypes.DWORD, wintypes.DWORD,
                             wintypes.HANDLE]
_k32.CreateFileW.restype = wintypes.HANDLE
_SIZE_T = ctypes.c_size_t  # wintypes 无 SIZE_T 别名
_k32.InitializeProcThreadAttributeList.argtypes = [
    _LPV, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(_SIZE_T)]
_k32.InitializeProcThreadAttributeList.restype = wintypes.BOOL
_k32.UpdateProcThreadAttribute.argtypes = [
    _LPV, wintypes.DWORD, ctypes.c_size_t, _LPV, ctypes.c_size_t, _LPV, _LPV]
_k32.UpdateProcThreadAttribute.restype = wintypes.BOOL
_k32.DeleteProcThreadAttributeList.argtypes = [_LPV]
_k32.DeleteProcThreadAttributeList.restype = None
_k32.CreateProcessW.argtypes = [
    wintypes.LPCWSTR, wintypes.LPWSTR, _LPV, _LPV, wintypes.BOOL,
    wintypes.DWORD, _LPV, wintypes.LPCWSTR, _LPV, _LPV]
_k32.CreateProcessW.restype = wintypes.BOOL
_k32.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
_k32.WaitForSingleObject.restype = wintypes.DWORD
_k32.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
_k32.GetExitCodeProcess.restype = wintypes.BOOL
_k32.TerminateProcess.argtypes = [wintypes.HANDLE, wintypes.UINT]
_k32.TerminateProcess.restype = wintypes.BOOL
_k32.ResumeThread.argtypes = [wintypes.HANDLE]
_k32.ResumeThread.restype = wintypes.DWORD
_k32.CloseHandle.argtypes = [wintypes.HANDLE]
_k32.CloseHandle.restype = wintypes.BOOL
_k32.LocalFree.argtypes = [_LPV]


def _sid_sddl(sid: bytes) -> str:
    pstr = wintypes.LPWSTR()
    if not _a32.ConvertSidToStringSidW(
            ctypes.cast(ctypes.create_string_buffer(sid), _LPV),
            ctypes.byref(pstr)):
        raise OSError(ctypes.get_last_error(), "ConvertSidToStringSid 失败")
    out = pstr.value
    _k32.LocalFree(pstr)
    return out


def appcontainer_sid() -> bytes:
    """Copy the system-derived SID and release its allocation with FreeSid."""
    sid = wintypes.LPVOID()
    hr = _u32.DeriveAppContainerSidFromAppContainerName(
        APPCONTAINER_NAME, ctypes.byref(sid))
    if hr < 0:
        raise OSError(hr, f"DeriveAppContainerSid failed: HRESULT 0x{hr & 0xffffffff:08X}")
    if not sid.value:
        raise OSError("DeriveAppContainerSid succeeded without a SID")
    try:
        if not _a32.IsValidSid(sid):
            raise OSError("DeriveAppContainerSid returned an invalid SID")
        length = _a32.GetLengthSid(sid)
        if not length:
            raise ctypes.WinError(ctypes.get_last_error())
        return ctypes.string_at(sid, length)
    finally:
        _a32.FreeSid(sid)


def grant_dir_access(path: Path, sid: bytes, write: bool = False) -> None:
    """为 AppContainer SID 在目录上追加 ACE(继承传播,幂等追加不删旧)。"""
    path.mkdir(parents=True, exist_ok=True)
    mask = _GENERIC_READ | _GENERIC_EXECUTE
    if write:
        mask |= _GENERIC_WRITE | _GENERIC_ALL
    ea = _EXPLICIT_ACCESS_W()
    ea.grfAccessPermissions = mask
    ea.grfAccessMode = _GRANT_ACCESS
    ea.grfInheritance = _SUB_CONTAINERS_AND_OBJECTS_INHERIT
    ea.Trustee.TrusteeForm = _TRUSTEE_IS_SID
    ea.Trustee.TrusteeType = 0  # TRUSTEE_IS_UNKNOWN
    # TRUSTEE_IS_SID:ptstrName 必须是二进制 SID 指针(不是 SDDL 字符串)
    ea.Trustee.ptstrName = ctypes.cast(
        ctypes.create_string_buffer(sid), wintypes.LPWSTR)
    old_acl = wintypes.LPVOID()
    sd = wintypes.LPVOID()
    rc = _a32.GetNamedSecurityInfoW(str(path), _SE_FILE_OBJECT,
                                    _DACL_SECURITY_INFORMATION, None, None,
                                    ctypes.byref(old_acl), None, ctypes.byref(sd))
    if rc != 0:
        raise OSError(rc, f"GetNamedSecurityInfo 失败: {path}")
    new_acl = wintypes.LPVOID()
    rc = _a32.SetEntriesInAclW(1, ctypes.byref(ea), old_acl, ctypes.byref(new_acl))
    if rc != 0:
        _k32.LocalFree(sd)
        raise OSError(rc, f"SetEntriesInAcl 失败: {path}")
    rc = _a32.SetNamedSecurityInfoW(str(path), _SE_FILE_OBJECT,
                                    _DACL_SECURITY_INFORMATION, None, None,
                                    new_acl, None)
    _k32.LocalFree(new_acl)
    _k32.LocalFree(sd)
    if rc != 0:
        raise OSError(rc, f"SetNamedSecurityInfo 失败: {path}")


def appcontainer_profile_path(sid: bytes) -> Path:
    """Read the provisioned profile location without creating storage or ACLs."""
    folder = wintypes.LPWSTR()
    hr = _u32.GetAppContainerFolderPath(_sid_sddl(sid), ctypes.byref(folder))
    if hr < 0:
        raise OSError(hr, f"AppContainer profile unavailable: HRESULT 0x{hr & 0xffffffff:08X}; "
                      "provision the profile explicitly before sandbox startup")
    if not folder.value:
        raise OSError("AppContainer profile lookup succeeded without a folder")
    try:
        path = Path(folder.value)
    finally:
        _ole32.CoTaskMemFree(ctypes.cast(folder, _LPV))
    if not path.is_dir():
        raise FileNotFoundError("AppContainer profile directory is missing; provision the profile explicitly")
    return path


def run_appcontainer(args: list[str], *, cwd: Path, env: dict,
                     allowed_dirs: list[tuple[Path, bool]],
                     timeout_ms: int = 300_000) -> subprocess.CompletedProcess:
    """在 AppContainer 中启动子进程并同步等待,捕获 stdout/stderr。

    allowed_dirs: [(目录, 是否可写)] —— 逐目录追加 ACE。
    Only explicit standard handles are inherited. Create suspended, assign to
    a kill-on-close JobObject, then resume. Kill and await all descendants on
    timeout, failure, and root exit. TimeoutExpired includes captured output.
    """
    if sys.platform != "win32":
        raise OSError("AppContainer 仅 Windows 可用")
    if not args:
        raise ValueError("args must not be empty")
    if not isinstance(timeout_ms, int) or not 0 <= timeout_ms < 0xffffffff:
        raise ValueError("timeout_ms must be a finite nonnegative DWORD")
    sid = appcontainer_sid()
    appcontainer_profile_path(sid)  # Fail before modifying any directory ACLs.
    cwd.mkdir(parents=True, exist_ok=True)
    for path, write in allowed_dirs:
        grant_dir_access(path, sid, write)
    # 输出重定向文件(可继承句柄)
    tag = uuid.uuid4().hex
    out_f = cwd / f".ac-out-{tag}.tmp"
    err_f = cwd / f".ac-err-{tag}.tmp"
    sa = _SECURITY_ATTRIBUTES()
    sa.nLength = ctypes.sizeof(_SECURITY_ATTRIBUTES)
    sa.bInheritHandle = True

    def _mk_handle(p: str, access: int, disposition: int) -> wintypes.HANDLE:
        h = _k32.CreateFileW(p, access, 3,  # FILE_SHARE_READ|WRITE
                             ctypes.byref(sa), disposition,
                             0x80,  # FILE_ATTRIBUTE_NORMAL
                             None)
        if h == _INVALID_HANDLE_VALUE:
            raise OSError(ctypes.get_last_error(), f"CreateFile 失败: {p}")
        return h

    handles = []
    owned_files = []
    attr_list = None
    attr_initialized = False
    job = None
    pi = _PROCESS_INFORMATION()
    assigned = False
    tree_stopped = False

    def _close_stdio() -> None:
        while handles:
            h = handles.pop()
            if not _k32.CloseHandle(h):
                raise ctypes.WinError(ctypes.get_last_error())

    def _stop_tree() -> None:
        nonlocal tree_stopped
        if assigned:
            job.terminate_and_wait()
        else:
            # Assignment failed: the root is still suspended and cannot spawn.
            if not _k32.TerminateProcess(pi.hProcess, 1):
                raise ctypes.WinError(ctypes.get_last_error())
        wait = _k32.WaitForSingleObject(pi.hProcess, 5000)
        if wait != _WAIT_OBJECT_0:
            raise OSError(f"AppContainer cleanup wait failed: {wait}")
        tree_stopped = True

    try:
        h_in = _mk_handle("NUL", _GENERIC_READ, 3)  # OPEN_EXISTING
        handles.append(h_in)
        h_out = _mk_handle(str(out_f), _GENERIC_WRITE, 1)  # CREATE_NEW
        handles.append(h_out)
        owned_files.append(out_f)
        h_err = _mk_handle(str(err_f), _GENERIC_WRITE, 1)
        handles.append(h_err)
        owned_files.append(err_f)
        si = _STARTUPINFOEXW()
        si.StartupInfo.cb = ctypes.sizeof(_STARTUPINFOEXW)
        si.StartupInfo.dwFlags = _STARTF_USESTDHANDLES
        si.StartupInfo.hStdInput = h_in
        si.StartupInfo.hStdOutput = h_out
        si.StartupInfo.hStdError = h_err
        attr_size = ctypes.c_size_t()
        _k32.InitializeProcThreadAttributeList(None, 2, 0, ctypes.byref(attr_size))
        if not attr_size.value:
            raise ctypes.WinError(ctypes.get_last_error())
        attr_list = ctypes.create_string_buffer(attr_size.value)
        if not _k32.InitializeProcThreadAttributeList(attr_list, 2, 0,
                                                      ctypes.byref(attr_size)):
            raise OSError(ctypes.get_last_error(),
                          "InitializeProcThreadAttributeList 失败")
        attr_initialized = True
        sid_buffer = ctypes.create_string_buffer(sid)
        caps = _SECURITY_CAPABILITIES()
        caps.AppContainerSid = ctypes.cast(sid_buffer, wintypes.LPVOID)
        if not _k32.UpdateProcThreadAttribute(
                attr_list, 0, _PROC_THREAD_ATTRIBUTE_SECURITY_CAPABILITIES,
                ctypes.byref(caps), ctypes.sizeof(caps), None, None):
            raise OSError(ctypes.get_last_error(), "UpdateProcThreadAttribute 失败")
        inherited_handles = (wintypes.HANDLE * 3)(h_in, h_out, h_err)
        if not _k32.UpdateProcThreadAttribute(
                attr_list, 0, _PROC_THREAD_ATTRIBUTE_HANDLE_LIST,
                ctypes.cast(inherited_handles, _LPV), ctypes.sizeof(inherited_handles),
                None, None):
            raise ctypes.WinError(ctypes.get_last_error())
        si.lpAttributeList = ctypes.cast(attr_list, wintypes.LPVOID)
        env_lines = "".join(f"{k}={v}\0" for k, v in sorted(
            env.items(), key=lambda item: item[0].upper())) + "\0"
        env_block = ctypes.create_unicode_buffer(env_lines)
        cmdline = ctypes.create_unicode_buffer(subprocess.list2cmdline(args))
        job = WindowsJob(2048)
        ok = _k32.CreateProcessW(
            None, cmdline, None, None, True,
            _EXTENDED_STARTUPINFO_PRESENT | _CREATE_UNICODE_ENVIRONMENT | _CREATE_SUSPENDED,
            ctypes.cast(env_block, wintypes.LPVOID), str(cwd),
            ctypes.byref(si), ctypes.byref(pi))
        create_error = ctypes.get_last_error() if not ok else 0
        if not ok:
            raise ctypes.WinError(create_error)
        job.assign_handle(pi.hProcess)
        assigned = True
        if _k32.ResumeThread(pi.hThread) == 0xffffffff:
            raise ctypes.WinError(ctypes.get_last_error())
        _close_stdio()
        rc_wait = _k32.WaitForSingleObject(pi.hProcess, timeout_ms)
        if rc_wait == _WAIT_TIMEOUT:
            _stop_tree()
            raise subprocess.TimeoutExpired(args, timeout_ms / 1000,
                output=out_f.read_bytes(), stderr=err_f.read_bytes())
        if rc_wait != _WAIT_OBJECT_0:
            raise OSError(ctypes.get_last_error(), f"AppContainer wait failed: {rc_wait}")
        exit_code = wintypes.DWORD()
        if not _k32.GetExitCodeProcess(pi.hProcess, ctypes.byref(exit_code)):
            raise ctypes.WinError(ctypes.get_last_error())
        _stop_tree()  # A root that exited must not leave background workers.
        out = out_f.read_bytes()
        err = err_f.read_bytes()
        return subprocess.CompletedProcess(args, exit_code.value, out, err)
    finally:
        try:
            if pi.hProcess and not tree_stopped:
                _stop_tree()
        finally:
            try:
                if job is not None:
                    job.close()  # KILL_ON_JOB_CLOSE is a final cleanup fallback.
            finally:
                if attr_initialized:
                    _k32.DeleteProcThreadAttributeList(attr_list)
                for h in (pi.hThread, pi.hProcess):
                    if h:
                        _k32.CloseHandle(h)
                try:
                    _close_stdio()
                finally:
                    for p in owned_files:
                        p.unlink(missing_ok=True)
