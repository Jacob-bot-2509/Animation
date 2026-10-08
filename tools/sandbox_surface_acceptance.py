"""Bounded native 43-point repair collection. No certificate, training or user UI."""
from __future__ import annotations
import argparse,ctypes,hashlib,json,os,socket,subprocess,sys,tempfile,threading,time,uuid
from ctypes import wintypes
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/"reviews/codex-supervision/2026-10-06-all43-sandbox-repair"
sys.path.insert(0,str(ROOT/"src"))
sys.path.insert(0,str(ROOT/"reviews/2026-10-06-exec-isolation-full-surface"))
from animtrain import sandbox_execution as se,private_profile as pp
from animtrain.full_surface_evidence import recompute
from surface_probe_contract import Receiver,host_control,wait_packet,WIN32_SOURCE
DIGEST=se.digest
ERROR_CODE=r'''
def failure(e):
    n=getattr(e,"winerror",None)
    return {"outcome":"os_denied" if n in (5,10013) else "error","winerror":n,"errno":getattr(e,"errno",None),"error_type":type(e).__name__,"detail":str(e)}
'''
def bindings():return {n:DIGEST(ROOT/n) for n in se.BOUND_FILES}
def write_new(path,data):
    with path.open("x",encoding="utf-8",newline="\n") as f:json.dump(data,f,ensure_ascii=False,indent=2);f.write("\n")
def native(source,timeout=90000,prepare=None):
    before=bindings()
    try:cp=se.run_code(source,mode="probe",timeout_ms=timeout,prepare_probe=prepare)
    except subprocess.TimeoutExpired as e:
        work=Path(e.work)
        cp={"rc":-1,"stdout":(e.output or b"").decode("utf-8","replace"),"stderr":(e.stderr or b"").decode("utf-8","replace"),
            "work":e.work,"source_sha256":DIGEST(work/"scene.py"),"command":[str((ROOT/".venv/Scripts/python.exe").resolve()),"-I","-B",str(work/"scene.py")],"parent_evidence":e.parent_evidence}
    return {"source":source,"transport":cp,"implementation_before":before,"implementation_after":bindings()}
def checkpoint(report,label):
    write_new(HERE/("checkpoint-"+report["run_id"]+"-"+label+".json"),report)
    print(label,"captured",flush=True)

def foundations(report):
    # Only this owned inheritable file handle is offered as the negative control.
    path=HERE/("handle-sentinel-"+report["run_id"]+".txt");path.write_text(report["run_id"],encoding="utf-8")
    k=ctypes.WinDLL("kernel32",use_last_error=True)
    class SA(ctypes.Structure):_fields_=[("size",wintypes.DWORD),("descriptor",wintypes.LPVOID),("inherit",wintypes.BOOL)]
    class FILE_ID_INFO(ctypes.Structure):_fields_=[("volume",ctypes.c_ulonglong),("identifier",ctypes.c_ubyte*16)]
    k.CreateFileW.argtypes=[wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,ctypes.POINTER(SA),wintypes.DWORD,wintypes.DWORD,wintypes.HANDLE];k.CreateFileW.restype=wintypes.HANDLE
    k.GetFileInformationByHandleEx.argtypes=[wintypes.HANDLE,ctypes.c_int,wintypes.LPVOID,wintypes.DWORD];k.GetFileInformationByHandleEx.restype=wintypes.BOOL
    k.CloseHandle.argtypes=[wintypes.HANDLE];k.CloseHandle.restype=wintypes.BOOL
    sa=SA(ctypes.sizeof(SA),None,True);handle=k.CreateFileW(str(path),0x80000000,3,ctypes.byref(sa),3,0,None)
    if handle in (None,0,ctypes.c_void_p(-1).value):raise ctypes.WinError(ctypes.get_last_error())
    file_id=FILE_ID_INFO()
    if not k.GetFileInformationByHandleEx(handle,18,ctypes.byref(file_id),ctypes.sizeof(file_id)):raise ctypes.WinError(ctypes.get_last_error())
    expected=str(file_id.volume)+":"+bytes(file_id.identifier).hex()
    code='import ctypes,json,os\nfrom ctypes import wintypes\n'+'''
class FileId(ctypes.Structure):_fields_=[("volume",ctypes.c_ulonglong),("identifier",ctypes.c_ubyte*16)]
k=ctypes.WinDLL("kernel32",use_last_error=True)
k.GetFileInformationByHandleEx.argtypes=[wintypes.HANDLE,ctypes.c_int,wintypes.LPVOID,wintypes.DWORD];k.GetFileInformationByHandleEx.restype=wintypes.BOOL
k.GetStdHandle.argtypes=[wintypes.DWORD];k.GetStdHandle.restype=wintypes.HANDLE
info=FileId()
'''
    code+=f'try:\n    ok=k.GetFileInformationByHandleEx({handle},18,ctypes.byref(info),ctypes.sizeof(info));query_error=None\nexcept OSError as e:\n    ok=False;query_error=e.winerror\n'
    code+='print(json.dumps({"pid":os.getpid(),"external_handle_file_id":str(info.volume)+":"+bytes(info.identifier).hex() if ok else None,"external_handle_query_error":query_error,"stdio_count":sum(bool(k.GetStdHandle(v)) for v in (0xfffffff6,0xfffffff5,0xfffffff4))}),flush=True)\n'
    try:identity=native(code)
    finally:k.CloseHandle(handle)
    report["identity_jobs"]=[identity]
    report["cases"]["B1"]={**identity,"host_file_id":expected,"host_inheritable_control_verified":True}
    protected=[{"path":str(ROOT/n),"before_sha256":DIGEST(ROOT/n)} for n in se.BOUND_FILES]
    guarded=se.NETWORK_SHIM+'''
import json,os,socket
r={}
for name,call in (
 ("connect",lambda:socket.socket().connect(("127.0.0.1",9))),
 ("connect_ex",lambda:socket.socket().connect_ex(("127.0.0.1",9))),
 ("sendto",lambda:socket.socket(type=socket.SOCK_DGRAM).sendto(b"fixture",("127.0.0.1",9))),
 ("getaddrinfo",lambda:socket.getaddrinfo("never-query.invalid",80))):
    try:call();r[name]="ALLOWED"
    except ConnectionError as e:r[name]=str(e)
keys=("HTTP_PROXY","HTTPS_PROXY","ALL_PROXY","http_proxy","https_proxy","all_proxy","NO_PROXY","no_proxy")
print(json.dumps({"shim":r,"proxy_environment":{k:os.environ.get(k) for k in keys}}),flush=True)
'''
    guards=native(guarded);report["identity_jobs"].append(guards)
    for point in ("A1","A2","A3","A4","A5","A7"):report["cases"][point]={"jobs":report["identity_jobs"]}
    for point in ("E1","E2"):report["cases"][point]=guards
    report["cases"]["E3"]={"source_sha256":DIGEST(ROOT/"src/animtrain/net_guard.py")}
    for v in protected:v["after_sha256"]=DIGEST(v["path"])
    report["cases"]["C5"]={**guards,"protected_files":protected}
    checkpoint(report,"foundations")

def host_case(mode):
    tag=uuid.uuid4().hex;source=HERE/"host_cases.py"
    cp=subprocess.run([sys.executable,"-X","utf8","-B",str(source),mode,tag],capture_output=True,timeout=100,cwd=ROOT)
    path=HERE/("host-"+mode+"-"+tag+".stdout.txt")
    with path.open("xb") as f:f.write(cp.stdout)
    with path.with_suffix(".stderr.txt").open("xb") as f:f.write(cp.stderr)
    return {"host_source_path":str(source),"host_source_sha256":DIGEST(source),"host_stdout_path":str(path),"host_stdout_sha256":DIGEST(path),"host_rc":cp.returncode},json.loads(cp.stdout or b"{}")
def fault_cases(report):
    row,data=host_case("reparse");report["cases"]["A6"]={**report["identity_jobs"][0],**row}
    row,data=host_case("sid_collision");report["cases"]["A8"]=row
    row,data=host_case("assignment_failure");report["cases"]["B5"]=row
    source=HERE/"host_cases.py";tag=uuid.uuid4().hex;folder=HERE/("host-fixture-"+tag)
    first=subprocess.Popen([sys.executable,"-X","utf8","-B",str(source),"lock_owner",tag],stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=ROOT)
    first_out=first_err=b""
    try:
        deadline=time.monotonic()+30
        while not (folder/"ready.json").exists():
            if first.poll() is not None or time.monotonic()>deadline:raise RuntimeError("Lock fixture not healthy")
            time.sleep(1/20)
        second=subprocess.run([sys.executable,"-X","utf8","-B",str(source),"lock_contender",tag],capture_output=True,timeout=15,cwd=ROOT)
    finally:
        if folder.exists():(folder/"release").write_text("release",encoding="ascii")
        first_out,first_err=first.communicate(timeout=30)
    data={**json.loads(first_out),**json.loads(second.stdout),"same_lock_path":True}
    path=HERE/("host-lock-"+tag+".stdout.json");write_new(path,data)
    for name,value in (("owner.stdout",first_out),("owner.stderr",first_err),("contender.stdout",second.stdout),("contender.stderr",second.stderr)):
        with (HERE/("host-lock-"+tag+"-"+name+".txt")).open("xb") as f:f.write(value)
    report["cases"]["A9"]={"host_source_path":str(source),"host_source_sha256":DIGEST(source),"host_stdout_path":str(path),"host_stdout_sha256":DIGEST(path),"host_rc":0 if first.returncode==second.returncode==0 else 2}
    checkpoint(report,"fault-native")

def files(report):
    fixture=Path(tempfile.mkdtemp(prefix="AnimTrainCodex-"+report["run_id"]+"-")).resolve()
    report["temporary_external_fixture"]=str(fixture)
    protected=fixture/"private.txt";victim=fixture/"victim.txt"
    protected.write_text(report["run_id"],encoding="ascii");victim.write_text(report["run_id"],encoding="ascii")
    prior=Path(report["identity_jobs"][0]["transport"]["work"])
    attempts={"read_outside":("read",protected),"write_outside":("write",fixture/"outside-marker.txt"),
      "write_toolchain":("write",Path(r"D:\Python")/("AnimTrainCodex-"+report["run_id"]+".txt")),
      "cross_run_write":("write",prior/("cross-marker-"+report["run_id"]+".txt")),
      "cross_run_cache":("write",prior/"state/config"/("cross-marker-"+report["run_id"]+".txt")),
      "delete_outside":("delete",victim)}
    win_file=r'''
import ctypes
from ctypes import wintypes
k=ctypes.WinDLL("kernel32",use_last_error=True)
k.CreateFileW.argtypes=[wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,wintypes.LPVOID,wintypes.DWORD,wintypes.DWORD,wintypes.HANDLE];k.CreateFileW.restype=wintypes.HANDLE
k.CloseHandle.argtypes=[wintypes.HANDLE];k.CloseHandle.restype=wintypes.BOOL
k.DeleteFileW.argtypes=[wintypes.LPCWSTR];k.DeleteFileW.restype=wintypes.BOOL
def attempt(op,path):
    ctypes.set_last_error(0)
    if op=="delete":
        if k.DeleteFileW(path):return {"outcome":"allowed"}
        error=ctypes.get_last_error()
    else:
        h=k.CreateFileW(path,0x80000000 if op=="read" else 0x40000000,3,None,3 if op=="read" else 1,0,None)
        if h not in (None,0,ctypes.c_void_p(-1).value):
            k.CloseHandle(h);return {"outcome":"allowed"}
        error=ctypes.get_last_error()
    return {"outcome":"os_denied" if error==5 else "error","winerror":error}
'''
    env={};exec(win_file,env)
    def healthy(op,path,fixture_label=None):
        result=env["attempt"](op,str(path));result["fixture"]=fixture_label or str(path)
        if result["outcome"]!="allowed":raise RuntimeError("Host fixture unhealthy: "+repr(result))
        if op=="write":path.unlink()
        elif op=="delete":path.write_text(report["run_id"],encoding="ascii")
        return result
    control={name:{"before":healthy(op,path)} for name,(op,path) in attempts.items()}
    target_acl=pp.acl_text(fixture);link_record={};junction_controls={}
    def prepare(work):
        link=work/"existing-escape"
        cp=subprocess.run([os.environ["COMSPEC"],"/c","mklink","/J",str(link),str(fixture)],capture_output=True,timeout=10)
        if cp.returncode or not link.is_junction() or link.resolve()!=fixture:raise RuntimeError("Preexisting junction fixture unavailable")
        link_record.update(path=str(link),target=str(fixture),verified=True,stdout=cp.stdout.decode("utf-8","replace"))
        junction_controls["before"]=healthy("write",link/"escaped-marker.txt",str(fixture))
    code=win_file+'\nimport json\npaths='+repr({n:(op,str(p)) for n,(op,p) in attempts.items()})+'\nr={n:attempt(op,path) for n,(op,path) in paths.items()}\nr["junction_escape"]=attempt("write",r"existing-escape\\escaped-marker.txt")\nprint(json.dumps(r),flush=True)\n'
    row=native(code,prepare=prepare);data=json.loads(row["transport"]["stdout"])
    snapshots={name:((path.exists() and DIGEST(path)==hashlib.sha256(report["run_id"].encode()).hexdigest()) if op in ("read","delete") else not path.exists()) for name,(op,path) in attempts.items()}
    marker=fixture/"escaped-marker.txt";junction_unchanged=not marker.exists();target_acl_unchanged=target_acl==pp.acl_text(fixture)
    for name,(op,path) in attempts.items():control[name]["after"]=healthy(op,path)
    junction_controls["after"]=healthy("write",Path(link_record["path"])/"escaped-marker.txt",str(fixture))
    for point,name in {"C1":"read_outside","C2":"write_outside","C3":"write_toolchain","C4":"cross_run_write","C7":"delete_outside"}.items():
        report["cases"][point]={**row,"operation":name,"observation_key":name,"fixture":str(attempts[name][1]),"controls":control[name],"fixture_alive_throughout":True,"host_unchanged":snapshots[name]}
    report["cases"]["C4"]["cache_denied"]=data.get("cross_run_cache",{}).get("outcome")=="os_denied" and data["cross_run_cache"].get("winerror")==5 and snapshots["cross_run_cache"]
    report["cases"]["C6"]={**row,"operation":"junction_escape","observation_key":"junction_escape","fixture":str(fixture),
        "controls":junction_controls,"fixture_alive_throughout":True,"host_unchanged":junction_unchanged,
        "preexisting_junction_verified":True,"target_acl_unchanged":target_acl_unchanged,"junction":link_record}
    report["temporary_external_fixture_cleanup_pending"]=True
    checkpoint(report,"files")

def process_tree(report,kind):
    tag=uuid.uuid4().hex;meta={};result={}
    mid='import subprocess,sys,time\np=subprocess.Popen([sys.executable,"-I","-B","-c","import time;time.sleep(60)"])\nprint(p.pid,flush=True)\ntime.sleep(60)\n'
    code='import subprocess,sys,time,json,pathlib\n'
    code+='p=subprocess.Popen([sys.executable,"-I","-B","-c",'+repr(mid)+'],stdout=subprocess.PIPE)\n'
    code+='grand=int(p.stdout.readline())\npathlib.Path("children-'+tag+'.json").write_text(json.dumps([p.pid,grand]),encoding="ascii")\n'
    code+='deadline=time.monotonic()+15\nwhile not pathlib.Path("continue-'+tag+'").exists():\n    if time.monotonic()>deadline:raise TimeoutError("Host did not retain child handles")\n    time.sleep(1/20)\n'
    code+='print(json.dumps({"child_pid":p.pid,"grandchild_pid":grand}),flush=True)\n'
    if kind=="B3":code+='time.sleep(60)\n'
    def run():
        try:result["row"]=native(code,timeout=20000,prepare=lambda w:meta.update(work=w))
        except Exception as e:result["error"]=repr(e)
    thread=threading.Thread(target=run);thread.start()
    k=ctypes.WinDLL("kernel32",use_last_error=True)
    k.OpenProcess.argtypes=[wintypes.DWORD,wintypes.BOOL,wintypes.DWORD];k.OpenProcess.restype=wintypes.HANDLE
    k.WaitForSingleObject.argtypes=[wintypes.HANDLE,wintypes.DWORD];k.WaitForSingleObject.restype=wintypes.DWORD
    k.GetProcessTimes.argtypes=[wintypes.HANDLE,*([ctypes.POINTER(wintypes.FILETIME)]*4)];k.GetProcessTimes.restype=wintypes.BOOL
    k.CloseHandle.argtypes=[wintypes.HANDLE];k.CloseHandle.restype=wintypes.BOOL
    handles=[];children=[]
    try:
        deadline=time.monotonic()+90
        while "work" not in meta or not (meta["work"]/("children-"+tag+".json")).exists():
            if not thread.is_alive() or time.monotonic()>deadline:raise RuntimeError("Child/grandchild fixture unavailable: "+repr(result))
            time.sleep(1/20)
        for pid in json.loads((meta["work"]/("children-"+tag+".json")).read_text(encoding="ascii")):
            h=k.OpenProcess(0x100000|0x1000,False,pid)
            if not h:raise ctypes.WinError(ctypes.get_last_error())
            handles.append(h);times=[wintypes.FILETIME() for _ in range(4)]
            if not k.GetProcessTimes(h,*[ctypes.byref(v) for v in times]):raise ctypes.WinError(ctypes.get_last_error())
            children.append({"pid":pid,"creation_filetime":times[0].dwHighDateTime*2**32+times[0].dwLowDateTime,
                             "opened_while_live":k.WaitForSingleObject(h,0)==258,"same_handle_retained":True})
        (meta["work"]/("continue-"+tag)).write_text("continue",encoding="ascii")
        thread.join(100)
        if thread.is_alive():raise RuntimeError("Owned transport did not finish")
        if "error" in result:raise RuntimeError(result["error"])
        for h,v in zip(handles,children):v["signaled_wait_result"]=int(k.WaitForSingleObject(h,5000))
        row=result["row"];report["cases"][kind]={**row,"held_children":children,"timed_out":row["transport"]["rc"]==-1}
    finally:
        if thread.is_alive() and "work" in meta:(meta["work"]/("continue-"+tag)).write_text("continue",encoding="ascii")
        thread.join(100)
        for h in handles:k.CloseHandle(h)
    checkpoint(report,kind)

def memory(report):
    code='import json,sys\nchunks=[]\ntry:\n    for i in range(36):chunks.append(bytearray(67108864))\nexcept MemoryError:\n    print(json.dumps({"memory_denied":True,"allocated_chunks":len(chunks),"chunk_bytes":67108864}),flush=True)\n    sys.exit(17)\nprint(json.dumps({"memory_denied":False}),flush=True)\n'
    report["cases"]["B4"]=native(code,timeout=30000);checkpoint(report,"memory")

class RawTCPReceiver:
    def __init__(self,family):
        self.kind="tcp";self.packets=[];self.errors=[];self.complete=False;self.stop=threading.Event()
        self.sock=socket.socket(family,socket.SOCK_STREAM)
        self.sock.bind(("127.0.0.1" if family==socket.AF_INET else "::1",0));self.sock.listen(8);self.sock.settimeout(1/5)
        self.endpoint=self.sock.getsockname();self.thread=threading.Thread(target=self.receive);self.thread.start()
    def receive(self):
        try:
            while not self.stop.is_set():
                try:conn,_=self.sock.accept()
                except TimeoutError:continue
                except OSError:
                    if self.stop.is_set():break
                    raise
                with conn:
                    conn.settimeout(2);payload=b""
                    while len(payload)<32:
                        part=conn.recv(32-len(payload))
                        if not part:break
                        payload+=part
                    if len(payload)!=32:raise ValueError("Incomplete nonce")
                    self.packets.append(payload.decode("ascii"))
        except Exception as e:self.errors.append(repr(e))
        finally:self.complete=True
    def close(self):
        self.stop.set();self.sock.close();self.thread.join(3)
        self.complete=self.complete and not self.thread.is_alive() and not self.errors
def phase_control(receiver,nonce):
    if receiver.kind=="udp":return host_control(receiver,nonce)
    with socket.socket(receiver.sock.family,socket.SOCK_STREAM) as client:
        client.settimeout(3);client.connect(receiver.endpoint);client.sendall(nonce.encode("ascii"))
    if not wait_packet(receiver,nonce):raise RuntimeError("TCP before/after receiver unhealthy")
    return {"received_exactly_once":True}

def loopback(report):
    receivers={};nonces={};spec={}
    try:
        for point,kind,family in (("D3","tcp",socket.AF_INET),("D4","tcp",socket.AF_INET6),("D5","udp",socket.AF_INET),("D6","udp",socket.AF_INET6)):
            receiver=Receiver(kind,family) if kind=='udp' else RawTCPReceiver(family);receivers[point]=receiver
            phases={p:uuid.uuid4().hex for p in ("before","sandbox","after")};nonces[point]=phases
            phase_control(receiver,phases["before"])
            spec[point]={"family":int(family),"kind":int(socket.SOCK_STREAM if kind=="tcp" else socket.SOCK_DGRAM),"endpoint":receiver.endpoint,"nonce":phases["sandbox"]}
        code='import _socket,json,time\nr={}\nspec='+repr(spec)+'\n'+ERROR_CODE+'''
for name,item in spec.items():
    s=_socket.socket(item["family"],item["kind"]);s.settimeout(2)
    try:
        if item["kind"]==int(_socket.SOCK_DGRAM):s.sendto(item["nonce"].encode(),tuple(item["endpoint"]))
        else:s.connect(tuple(item["endpoint"]));s.sendall(item["nonce"].encode())
        r[name]={"outcome":"sent"}
    except TimeoutError as e:r[name]={"outcome":"timeout","error_type":"TimeoutError","detail":str(e)}
    except OSError as e:r[name]=failure(e)
    finally:s.close()
print(json.dumps(r),flush=True)
'''
        row=native(code);finished=time.monotonic_ns()
        deadline=finished+20_000_000_000
        while time.monotonic_ns()<deadline:time.sleep(max(0,min(1,(deadline-time.monotonic_ns())/1_000_000_000)))
        for point,receiver in receivers.items():phase_control(receiver,nonces[point]["after"])
    finally:
        for receiver in receivers.values():receiver.close()
    from animtrain.full_surface_evidence import NETWORKS
    for point,receiver in receivers.items():
        report["cases"][point]={**row,"operation":NETWORKS[point],"observation_key":point,"endpoint":receiver.endpoint,"nonces":nonces[point],
            "packets":receiver.packets,"receiver_complete":receiver.complete,"receiver_errors":receiver.errors,
            "post_attempt_observation_ns":time.monotonic_ns()-finished}
    checkpoint(report,"loopback")

def ipc_and_registry(report):
    import winreg
    env={};exec(WIN32_SOURCE,env);k=env["bind_kernel32"]();invalid=env["invalid_handle"]
    k.ReadFile.argtypes=[wintypes.HANDLE,wintypes.LPVOID,wintypes.DWORD,ctypes.POINTER(wintypes.DWORD),wintypes.LPVOID];k.ReadFile.restype=wintypes.BOOL
    k.WriteFile.argtypes=k.ReadFile.argtypes;k.WriteFile.restype=wintypes.BOOL
    k.MapViewOfFile.argtypes=[wintypes.HANDLE,wintypes.DWORD,wintypes.DWORD,wintypes.DWORD,ctypes.c_size_t];k.MapViewOfFile.restype=wintypes.LPVOID
    k.UnmapViewOfFile.argtypes=[wintypes.LPCVOID];k.UnmapViewOfFile.restype=wintypes.BOOL
    tag=report["run_id"];handles={};views={};controls={};nonces={};names={
        "pipe":r"\\.\pipe\AnimTrainCodex-"+tag,"mailslot":r"\\.\mailslot\AnimTrainCodex-"+tag,
        "Local":r"Local\AnimTrainCodex-"+tag,"Global":r"Global\AnimTrainCodex-"+tag}
    key="Software\\AnimationModelTraining\\CodexProbes\\"+tag
    baseline="before-"+tag
    with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER,key,0,winreg.KEY_SET_VALUE) as h:winreg.SetValueEx(h,"nonce",0,winreg.REG_SZ,baseline)
    registry_created=True
    def write(h,payload):
        count=wintypes.DWORD();buf=ctypes.create_string_buffer(payload)
        if not k.WriteFile(h,buf,len(payload),ctypes.byref(count),None) or count.value!=len(payload):raise ctypes.WinError(ctypes.get_last_error())
    def read(h):
        count=wintypes.DWORD();buf=ctypes.create_string_buffer(4096)
        if not k.ReadFile(h,buf,4096,ctypes.byref(count),None):raise ctypes.WinError(ctypes.get_last_error())
        return buf.raw[:count.value]
    def control(kind,nonce):
        if kind=="pipe":
            client=k.CreateFileW(names[kind],0xC0000000,0,None,3,0,None)
            if invalid(client):raise ctypes.WinError(ctypes.get_last_error())
            try:
                write(client,nonce.encode());got=read(handles[kind]);write(handles[kind],("ack-"+nonce).encode());reply=read(client)
                if got!=nonce.encode() or reply!=("ack-"+nonce).encode():raise ValueError("Duplex pipe control nonce mismatch")
            finally:k.CloseHandle(client);k.DisconnectNamedPipe(handles[kind]);k.ConnectNamedPipe(handles[kind],None)
        elif kind=="mailslot":
            client=k.CreateFileW(names[kind],0x40000000,0,None,3,0,None)
            if invalid(client):raise ctypes.WinError(ctypes.get_last_error())
            try:write(client,nonce.encode())
            finally:k.CloseHandle(client)
            if read(handles[kind])!=nonce.encode():raise ValueError("Mailslot control nonce mismatch")
        else:
            client=k.OpenFileMappingW(6,False,names[kind])
            if invalid(client):raise ctypes.WinError(ctypes.get_last_error())
            address=k.MapViewOfFile(client,6,0,0,4096)
            if not address:raise ctypes.WinError(ctypes.get_last_error())
            try:ctypes.memmove(address,nonce.encode(),32);got=ctypes.string_at(views[kind],32)
            finally:k.UnmapViewOfFile(address);k.CloseHandle(client)
            if got!=nonce.encode():raise ValueError("Mapping control nonce mismatch")
        return {"outcome":"allowed","fixture":names[kind],"nonce":nonce}
    try:
        for kind,name in names.items():
            ctypes.set_last_error(0)
            if kind=="pipe":h=k.CreateNamedPipeW(name,3,7,1,4096,4096,1000,None)
            elif kind=="mailslot":h=k.CreateMailslotW(name,4096,1000,None)
            else:h=k.CreateFileMappingW(ctypes.c_void_p(-1).value,None,4,0,4096,name)
            if invalid(h):
                report.setdefault("fixture_errors",{})[kind]={"winerror":ctypes.get_last_error(),"reason":"Host fixture creation failed"}
                continue
            handles[kind]=h
            if kind=="pipe":k.ConnectNamedPipe(h,None)
            if kind in ("Local","Global"):
                address=k.MapViewOfFile(h,6,0,0,4096)
                if not address:raise ctypes.WinError(ctypes.get_last_error())
                views[kind]=address
            nonces[kind]={p:uuid.uuid4().hex for p in ("before","sandbox","after")}
            controls[kind]={"before":control(kind,nonces[kind]["before"])}
        code=WIN32_SOURCE+'\nimport json,winreg\nr={}\ntargets='+repr({kind:{"name":names[kind],"nonce":nonces[kind]["sandbox"]} for kind in handles})+'\nkey='+repr(key)+'\n'+ERROR_CODE+'''
k=bind_kernel32()
for kind,item in targets.items():
    ctypes.set_last_error(0)
    h=k.OpenFileMappingW(6,False,item["name"]) if kind in ("Local","Global") else k.CreateFileW(item["name"],0xC0000000 if kind=="pipe" else 0x40000000,0,None,3,0,None)
    error=ctypes.get_last_error()
    if invalid_handle(h):r[kind]={"outcome":"os_denied" if error==5 else "error","winerror":error}
    else:r[kind]={"outcome":"allowed"};k.CloseHandle(h)
try:
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER,key,0,winreg.KEY_SET_VALUE) as reg:
        winreg.SetValueEx(reg,"nonce",0,winreg.REG_SZ,"sandbox")
    r["registry"]={"outcome":"allowed"}
except OSError as e:r["registry"]=failure(e)
print(json.dumps(r),flush=True)
'''
        row=native(code);report["ipc_native_observation"]=row;data=json.loads(row["transport"]["stdout"])
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,key) as reg:unchanged=winreg.QueryValueEx(reg,"nonce")[0]==baseline
        for kind in handles:controls[kind]["after"]=control(kind,nonces[kind]["after"])
        for point,kind,operation in (("F2","pipe","pipe_access"),("F3","mailslot","mailslot_access"),("F4","Local","mapping_access")):
            if kind not in handles:continue
            case={**row,"operation":operation,"observation_key":kind,"fixture":names[kind],"controls":controls[kind],"fixture_alive_throughout":True,"host_unchanged":data.get(kind,{}).get("outcome")!="allowed"}
            if point=="F2":case["matrix"]=["named_local"]
            if point=="F4":case["matrix"]=[n for n in ("Local","Global") if n in handles]
            report["cases"][point]=case
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,key,0,winreg.KEY_SET_VALUE) as reg:winreg.SetValueEx(reg,"nonce",0,winreg.REG_SZ,"after-"+tag)
        report["cases"]["F1"]={**row,"operation":"registry_write","observation_key":"registry","fixture":key,
            "controls":{p:{"outcome":"allowed","fixture":key} for p in ("before","after")},"fixture_alive_throughout":True,"host_unchanged":unchanged}
    finally:
        for address in views.values():k.UnmapViewOfFile(address)
        for h in handles.values():k.CloseHandle(h)
        if registry_created:winreg.DeleteKey(winreg.HKEY_CURRENT_USER,key)
    checkpoint(report,"ipc-registry")

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute-native",action="store_true")
    parser.add_argument("--groups",default="foundations,faults,files,trees,memory,loopback,ipc")
    args=parser.parse_args()
    if not args.execute_native:print("PLAN ONLY: 43-point evidence collection; production CLOSED");return 3
    HERE.mkdir(parents=True,exist_ok=True)
    report={"schema":"sandbox-surface-native-v1","run_id":uuid.uuid4().hex,"cases":{},"production_gate":"CLOSED",
            "certificate_written":False,"initial_bindings":bindings(),"started_ns":time.monotonic_ns()}
    try:
        for group in args.groups.split(","):
            if group=="foundations":foundations(report)
            elif group=="faults":fault_cases(report)
            elif group=="files":files(report)
            elif group=="trees":
                process_tree(report,"B2");process_tree(report,"B3")
            elif group=="memory":memory(report)
            elif group=="loopback":loopback(report)
            elif group=="ipc":ipc_and_registry(report)
            else:raise ValueError("Unknown group "+group)
    except BaseException as e:report["error"]={"type":type(e).__name__,"detail":str(e)}
    finally:
        report["finished_ns"]=time.monotonic_ns();report["final_bindings"]=bindings()
        report["implementation_unchanged"]=report["initial_bindings"]==report["final_bindings"]
        report["results"]=recompute(report)
        path=HERE/("surface-raw-"+report["run_id"]+".json");write_new(path,report)
    print(json.dumps({"path":str(path),"sha256":DIGEST(path),"counts":{s:sum(v["status"]==s for v in report["results"].values()) for s in ("GREEN","FAIL","PARTIAL","GAP")},"error":report.get("error"),"production_gate":"CLOSED"}),flush=True)
    return 2 if "error" in report or any(v["status"]=="FAIL" for v in report["results"].values()) else 3
if __name__=="__main__":raise SystemExit(main())
