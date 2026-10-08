"""Explicit disposable per-job profile and temporary project/toolchain grants.

Only Create/DeleteAppContainerProfile touch the current user's own app storage.
No system file, source MiKTeX installation, firewall or exemption is modified.
Directory revocation removes ONLY this newly created UUID SID; old ACEs remain.
"""
from __future__ import annotations
import ctypes
import hashlib
import re
import uuid
from contextlib import contextmanager
from ctypes import wintypes
from pathlib import Path
from . import appcontainer as ac
ROOT=Path(__file__).resolve().parents[2]


def acl_text(path):
    sd=wintypes.LPVOID();text=wintypes.LPWSTR()
    rc=ac._a32.GetNamedSecurityInfoW(str(path),1,4,None,None,None,None,ctypes.byref(sd))
    if rc:raise OSError(rc,'Cannot read DACL: '+str(path))
    convert=ac._a32.ConvertSecurityDescriptorToStringSecurityDescriptorW
    convert.argtypes=[wintypes.LPVOID,wintypes.DWORD,wintypes.DWORD,ctypes.POINTER(wintypes.LPWSTR),wintypes.LPVOID]
    convert.restype=wintypes.BOOL
    try:
        if not convert(sd,1,4,ctypes.byref(text),None):raise ctypes.WinError(ctypes.get_last_error())
        return text.value
    finally:
        if text:ac._k32.LocalFree(text)
        if sd:ac._k32.LocalFree(sd)


def revoke_new_sid(path,sid):
    """REVOKE_ACCESS for the unique profile SID, including inherited propagation."""
    ea=ac._EXPLICIT_ACCESS_W();ea.grfAccessMode=4;ea.grfInheritance=3
    ea.Trustee.TrusteeForm=0;ea.Trustee.TrusteeType=0
    buffer=ctypes.create_string_buffer(sid)
    ea.Trustee.ptstrName=ctypes.cast(buffer,wintypes.LPWSTR)
    old=wintypes.LPVOID();sd=wintypes.LPVOID();new=wintypes.LPVOID()
    rc=ac._a32.GetNamedSecurityInfoW(str(path),1,4,None,None,ctypes.byref(old),None,ctypes.byref(sd))
    if rc:raise OSError(rc,'Cannot read temporary grant')
    try:
        rc=ac._a32.SetEntriesInAclW(1,ctypes.byref(ea),old,ctypes.byref(new))
        if rc:raise OSError(rc,'Cannot revoke temporary SID')
        rc=ac._a32.SetNamedSecurityInfoW(str(path),1,4,None,None,new,None)
        if rc:raise OSError(rc,'Cannot apply SID revocation')
    finally:
        if new:ac._k32.LocalFree(new)
        if sd:ac._k32.LocalFree(sd)


def _validated_grant_path(path):
    """Reject literal reparse roots/ancestors before resolving their targets."""
    import stat
    literal=Path(path).absolute()
    if '..' in literal.parts:
        raise ValueError('Noncanonical grant root')
    if not literal.is_dir():
        raise FileNotFoundError(literal)
    for ancestor in (literal,*literal.parents):
        details=ancestor.lstat()
        if stat.S_ISLNK(details.st_mode) or getattr(details,'st_file_attributes',0)&0x400:
            raise ValueError('Reparse grant root or ancestor')
    resolved=literal.resolve()
    if not resolved.is_relative_to(ROOT) and resolved!=Path(r'D:\Python'):
        raise ValueError('Grant outside reviewed project/runtime')
    return resolved


@contextmanager
def _profile_grants(grants):
    """Provision a never-reused profile. Revoke grants and delete after tree exit.

    Grant roots are restricted to the D: Python runtime and this project.
    A cleanup error prevents a successful result/certificate.
    """
    name='animtrain-job-'+uuid.uuid4().hex
    if not re.fullmatch(r'animtrain-job-[0-9a-f]{32}',name):raise ValueError('Bad profile name')
    paths=[]
    for path,write in grants:
        path=_validated_grant_path(path)
        paths.append((path,write))
    create=ac._u32.CreateAppContainerProfile
    create.argtypes=[wintypes.LPCWSTR,wintypes.LPCWSTR,wintypes.LPCWSTR,wintypes.LPVOID,wintypes.DWORD,ctypes.POINTER(wintypes.LPVOID)]
    create.restype=ctypes.c_long
    delete=ac._u32.DeleteAppContainerProfile;delete.argtypes=[wintypes.LPCWSTR];delete.restype=ctypes.c_long
    ptr=wintypes.LPVOID()
    hr=create(name,name,'Disposable animtrain render job',None,0,ctypes.byref(ptr))
    if hr!=0:raise OSError(hr,'Fresh AppContainer profile creation failed')
    sid=None;applied=[];cleanup=[]
    try:
        if not ptr.value or not ac._a32.IsValidSid(ptr):raise OSError('Invalid provisioned SID')
        sid=ctypes.string_at(ptr,ac._a32.GetLengthSid(ptr))
        storage=ac.appcontainer_profile_path(sid).resolve()
        # Native API owns this newly named CURRENT USER profile only.
        evidence={'profile_name':name,'sid':ac._sid_sddl(sid),'storage':str(storage),
                  'temporary_acl':[],'cleanup_complete':False}
        for path,write in paths:
            before=acl_text(path)
            if evidence['sid'] in before:raise OSError('Fresh UUID SID already granted')
            applied.append((path,before))
            ac.grant_dir_access(path,sid,write=write)
        yield name,evidence
    finally:
        if ptr.value:ac._a32.FreeSid(ptr)
        for path,before in reversed(applied):
            try:
                revoke_new_sid(path,sid)
                after=acl_text(path)
                same=before==after
                evidence['temporary_acl'].append({'path':str(path),'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest(),'restored':same})
                if not same:cleanup.append('DACL changed during job: '+str(path))
            except Exception as exc:cleanup.append(str(exc))
        hr=delete(name)
        if hr!=0:cleanup.append('DeleteAppContainerProfile failed: '+str(hr))
        if 'evidence' in locals():evidence['cleanup_complete']=not cleanup
        if cleanup:raise OSError('Private profile cleanup failed: '+'; '.join(cleanup))


@contextmanager
def isolated_profile(grants):
    """Serialize temporary shared-runtime ACL edits across host processes."""
    import msvcrt
    lock=ROOT/'reviews/codex-supervision/2026-10-05-three-gates/transport.lock'
    lock.parent.mkdir(parents=True,exist_ok=True)
    with lock.open('a+b') as handle:
        if handle.tell()==0:
            handle.write(b"0");handle.flush()
        handle.seek(0)
        msvcrt.locking(handle.fileno(),msvcrt.LK_NBLCK,1)
        try:
            with _profile_grants(grants) as profile:
                yield profile
        finally:
            handle.seek(0);msvcrt.locking(handle.fileno(),msvcrt.LK_UNLCK,1)
