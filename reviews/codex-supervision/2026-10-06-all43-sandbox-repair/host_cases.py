"""Owned native fixtures for SID collision, cross-process lock and startup failure."""
from __future__ import annotations
import ctypes,json,os,subprocess,sys,time,uuid
from contextlib import contextmanager
from ctypes import wintypes
from pathlib import Path
from unittest import mock
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/"src"))
from animtrain import private_profile as pp,appcontainer as ac,sandbox_execution as se
HERE=Path(__file__).parent
def emit(data):print(json.dumps(data),flush=True)
def main():
    mode,tag=sys.argv[1:3]
    if not tag.isalnum() or len(tag)!=32:raise ValueError("Bad fixture tag")
    work=HERE/("host-fixture-"+tag);work.mkdir(exist_ok=True)
    if mode in ("lock_owner","lock_contender"):
        grants=[(Path(r"D:\Python"),False),(ROOT/".venv",False),(ROOT/".sandbox-runtime/miktex-real",False),(work,True)]
        count=[0];original=ac._u32.CreateAppContainerProfile
        def create(*args):count[0]+=1;return original(*args)
        try:
            with mock.patch.object(ac._u32,"CreateAppContainerProfile",side_effect=create):
                with pp.isolated_profile(grants) as (name,evidence):
                    if mode=="lock_contender":emit({"unexpected_lock_acquired":True});return 2
                    (work/"ready.json").write_text(json.dumps({"profile":name}),encoding="utf-8")
                    deadline=time.monotonic()+20
                    while not (work/"release").exists():
                        if time.monotonic()>deadline:raise TimeoutError("Fixture release missing")
                        time.sleep(1/20)
            emit({"first_native_profile_acquired":True,"first_cleanup_complete":evidence["cleanup_complete"],
                  "second_profile_create_calls":count[0],"profile":evidence})
        except OSError as e:
            if mode!="lock_contender":raise
            emit({"second_errno":e.errno,"second_profile_create_calls":count[0]})
        return 0
    if mode=="sid_collision":
        before=pp.acl_text(work);state={};original_create=ac._u32.CreateAppContainerProfile
        original_grant=ac.grant_dir_access;grant_calls=[0]
        def create(*args):
            hr=original_create(*args)
            if hr==0:
                ptr=ctypes.cast(args[-1],ctypes.POINTER(wintypes.LPVOID)).contents
                sid=ctypes.string_at(ptr,ac._a32.GetLengthSid(ptr))
                state.update(sid=sid,storage=str(ac.appcontainer_profile_path(sid)))
                original_grant(work,sid,write=False) # ONLY the newly created SID on our new fixture.
            return hr
        def grant(*args,**kwargs):grant_calls[0]+=1;return original_grant(*args,**kwargs)
        caught=False
        try:
            with mock.patch.object(ac._u32,"CreateAppContainerProfile",side_effect=create),mock.patch.object(ac,"grant_dir_access",side_effect=grant):
                try:
                    with pp.isolated_profile([(work,False)]):raise AssertionError("Collision accepted")
                except OSError as e:
                    caught="Fresh UUID SID already granted" in str(e)
        finally:
            if state.get("sid"):pp.revoke_new_sid(work,state["sid"])
        emit({"preexisting_sid_rejected":caught,"grant_calls":grant_calls[0],
              "profile_deleted":bool(state.get("storage")) and not Path(state["storage"]).exists(),
              "acl_unchanged":before==pp.acl_text(work)})
        return 0
    if mode=="reparse":
        import os
        target=HERE/("reparse-target-"+tag);target.mkdir();(target/"child").mkdir()
        link=HERE/("reparse-link-"+tag)
        cp=subprocess.run([os.environ["COMSPEC"],"/c","mklink","/J",str(link),str(target)],capture_output=True,timeout=10)
        if cp.returncode or not link.is_junction():raise RuntimeError("Healthy junction creation unavailable")
        before=pp.acl_text(target);cases={}
        for name,path in (("root",link),("ancestor",link/"child")):
            count=[0];original=ac._u32.CreateAppContainerProfile
            def create(*args):count[0]+=1;return original(*args)
            rejected=False
            with mock.patch.object(ac._u32,"CreateAppContainerProfile",side_effect=create):
                try:
                    with pp._profile_grants([(path,True)]):pass
                except ValueError as e:rejected="Reparse" in str(e)
            cases[name]={"rejected_before_profile":rejected,"create_calls":count[0],"acl_unchanged":before==pp.acl_text(target)}
        emit({"reparse_cases":cases});return 0
    if mode=="assignment_failure":
        state={"resume_calls":0};k=ac._k32;held=[None]
        k.GetCurrentProcess.restype=wintypes.HANDLE
        k.DuplicateHandle.argtypes=[wintypes.HANDLE,wintypes.HANDLE,wintypes.HANDLE,ctypes.POINTER(wintypes.HANDLE),wintypes.DWORD,wintypes.BOOL,wintypes.DWORD];k.DuplicateHandle.restype=wintypes.BOOL
        original_create=k.CreateProcessW;original_resume=k.ResumeThread;original_profile=pp.isolated_profile
        def create(*args):
            state["created_suspended"]=bool(args[5]&4)
            return original_create(*args)
        def assign(job,handle):
            copy=wintypes.HANDLE()
            if not k.DuplicateHandle(k.GetCurrentProcess(),handle,k.GetCurrentProcess(),ctypes.byref(copy),0,False,2):raise ctypes.WinError(ctypes.get_last_error())
            held[0]=copy
            raise ctypes.WinError(5)
        def resume(*args):state["resume_calls"]+=1;return original_resume(*args)
        @contextmanager
        def profile(grants):
            evidence=None
            try:
                with original_profile(grants) as item:evidence=item[1];yield item
            finally:
                if evidence is not None:state["profile_cleanup_complete"]=evidence.get("cleanup_complete")
        try:
            with mock.patch.object(k,"CreateProcessW",side_effect=create),mock.patch.object(k,"ResumeThread",side_effect=resume),mock.patch.object(ac.WindowsJob,"assign_handle",assign),mock.patch.object(pp,"isolated_profile",profile):
                try:se.run_code('raise RuntimeError("Child must never resume")',mode="probe")
                except OSError as e:state["assignment_error"]=e.winerror
            state["root_wait_result"]=int(k.WaitForSingleObject(held[0],5000)) if held[0] else None
        finally:
            if held[0]:k.CloseHandle(held[0])
        emit(state);return 0
    raise ValueError("Unknown mode")
if __name__=="__main__":raise SystemExit(main())
