"""Supplemental anonymous pipe inheritance check using owned live handles."""
import ctypes,hashlib,json,sys,uuid
from ctypes import wintypes
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).parent
sys.path.insert(0,str(ROOT/"src"))
from animtrain import sandbox_execution as se
from animtrain.full_surface_evidence import transport
k=ctypes.WinDLL("kernel32",use_last_error=True)
class SA(ctypes.Structure):_fields_=[("nLength",wintypes.DWORD),("descriptor",wintypes.LPVOID),("inherit",wintypes.BOOL)]
k.CreatePipe.argtypes=[ctypes.POINTER(wintypes.HANDLE),ctypes.POINTER(wintypes.HANDLE),ctypes.POINTER(SA),wintypes.DWORD];k.CreatePipe.restype=wintypes.BOOL
k.ReadFile.argtypes=[wintypes.HANDLE,wintypes.LPVOID,wintypes.DWORD,ctypes.POINTER(wintypes.DWORD),wintypes.LPVOID];k.ReadFile.restype=wintypes.BOOL
k.WriteFile.argtypes=k.ReadFile.argtypes;k.WriteFile.restype=wintypes.BOOL
k.CloseHandle.argtypes=[wintypes.HANDLE];k.CloseHandle.restype=wintypes.BOOL
read=wintypes.HANDLE();write=wintypes.HANDLE();sa=SA(ctypes.sizeof(SA),None,True)
if not k.CreatePipe(ctypes.byref(read),ctypes.byref(write),ctypes.byref(sa),4096):raise ctypes.WinError(ctypes.get_last_error())
def healthy():
    nonce=uuid.uuid4().hex;data=ctypes.create_string_buffer(nonce.encode());count=wintypes.DWORD();got=ctypes.create_string_buffer(32)
    if not k.WriteFile(write,data,32,ctypes.byref(count),None) or count.value!=32:raise ctypes.WinError(ctypes.get_last_error())
    if not k.ReadFile(read,got,32,ctypes.byref(count),None) or count.value!=32 or got.raw!=nonce.encode():raise RuntimeError("Owned anonymous pipe control failed")
    return nonce
code='import ctypes,json\nfrom ctypes import wintypes\nr={}\nhandles='+repr({"read":read.value,"write":write.value})+'\n'+'''
k=ctypes.WinDLL("kernel32",use_last_error=True)
k.GetNamedPipeInfo.argtypes=[wintypes.HANDLE,*([ctypes.POINTER(wintypes.DWORD)]*4)];k.GetNamedPipeInfo.restype=wintypes.BOOL
for name,h in handles.items():
    ctypes.set_last_error(0)
    try:
        ok=k.GetNamedPipeInfo(h,None,None,None,None)
        r[name]={"query":bool(ok),"winerror":None if ok else ctypes.get_last_error()}
    except OSError as e:r[name]={"query":False,"winerror":e.winerror}
print(json.dumps(r),flush=True)
'''
before={n:se.digest(ROOT/n) for n in se.BOUND_FILES}
try:
    controls={"before":healthy()}
    cp=se.run_code(code,mode="probe")
    controls["after"]=healthy()
finally:k.CloseHandle(read);k.CloseHandle(write)
row={"source":code,"transport":cp,"implementation_before":before,"implementation_after":{n:se.digest(ROOT/n) for n in se.BOUND_FILES}}
_,data=transport(row)
passed=cp["rc"]==0 and set(data)=={"read","write"} and all(v["query"] is False and v["winerror"] in (6,-1073741816) for v in data.values())
report={"schema":"anonymous-pipe-supplement-v1","row":row,"controls":controls,"both_host_handles_held_throughout":True,
        "scoped_pass":passed,"F2_complete":False,"remaining":"A distinct Windows user fixture is still required",
        "host_source_sha256":se.digest(Path(__file__)),"production_gate":"CLOSED"}
path=OUT/("anonymous-pipe-"+uuid.uuid4().hex+".json")
with path.open("x",encoding="utf-8") as f:json.dump(report,f,indent=2)
print(json.dumps({"path":str(path),"scoped_pass":passed,"observations":data}),flush=True)
