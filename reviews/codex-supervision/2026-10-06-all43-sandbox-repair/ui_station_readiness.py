"""Readiness only: create/bind/close an owned noninteractive station and desktop.
No clipboard, window, message or hook API is called.
"""
import ctypes,hashlib,json,uuid
from ctypes import wintypes
from pathlib import Path
u=ctypes.WinDLL("user32",use_last_error=True);k=ctypes.WinDLL("kernel32",use_last_error=True)
signatures={
 "CreateWindowStationW":([wintypes.LPCWSTR,wintypes.DWORD,wintypes.DWORD,wintypes.LPVOID],wintypes.HANDLE),
 "GetProcessWindowStation":([],wintypes.HANDLE),
 "SetProcessWindowStation":([wintypes.HANDLE],wintypes.BOOL),
 "CloseWindowStation":([wintypes.HANDLE],wintypes.BOOL),
 "CreateDesktopW":([wintypes.LPCWSTR,wintypes.LPCWSTR,wintypes.LPVOID,wintypes.DWORD,wintypes.DWORD,wintypes.LPVOID],wintypes.HANDLE),
 "GetThreadDesktop":([wintypes.DWORD],wintypes.HANDLE),
 "SetThreadDesktop":([wintypes.HANDLE],wintypes.BOOL),
 "CloseDesktop":([wintypes.HANDLE],wintypes.BOOL),
 "GetUserObjectInformationW":([wintypes.HANDLE,ctypes.c_int,wintypes.LPVOID,wintypes.DWORD,ctypes.POINTER(wintypes.DWORD)],wintypes.BOOL)}
for name,(args,ret) in signatures.items():fn=getattr(u,name);fn.argtypes=args;fn.restype=ret
k.GetCurrentThreadId.restype=wintypes.DWORD
def name(handle):
    data=ctypes.create_unicode_buffer(256);needed=wintypes.DWORD()
    if not u.GetUserObjectInformationW(handle,2,data,ctypes.sizeof(data),ctypes.byref(needed)):raise ctypes.WinError(ctypes.get_last_error())
    return data.value
tag=uuid.uuid4().hex;station_name="AnimTrainCodex-"+tag;desk_name="Synthetic-"+tag
original_station=u.GetProcessWindowStation();original_desktop=u.GetThreadDesktop(k.GetCurrentThreadId())
station=desktop=None;report={"run_id":tag,"clipboard_api_calls":0,"user_desktop_data_accessed":False,"acceptance":False,"production_gate":"CLOSED"}
try:
    station=u.CreateWindowStationW(station_name,0,0x37f,None)
    if not station:raise ctypes.WinError(ctypes.get_last_error())
    if not u.SetProcessWindowStation(station):raise ctypes.WinError(ctypes.get_last_error())
    if name(u.GetProcessWindowStation())!=station_name:raise ValueError("Private station binding mismatch")
    desktop=u.CreateDesktopW(desk_name,None,None,0,0x1ff,None)
    if not desktop:raise ctypes.WinError(ctypes.get_last_error())
    if not u.SetThreadDesktop(desktop):raise ctypes.WinError(ctypes.get_last_error())
    bound_station=name(u.GetProcessWindowStation());bound_desktop=name(u.GetThreadDesktop(k.GetCurrentThreadId()))
    if bound_station.lower()=="winsta0" or bound_station!=station_name or bound_desktop!=desk_name:raise ValueError("Isolation assertion failed")
    report.update(noninteractive_station_created=True,private_station_verified=True,private_desktop_verified=True,station=bound_station,desktop=bound_desktop)
except Exception as e:report["error"]={"type":type(e).__name__,"detail":str(e)}
finally:
    if original_station:report["original_station_restored"]=bool(u.SetProcessWindowStation(original_station))
    if original_desktop:report["original_desktop_restored"]=bool(u.SetThreadDesktop(original_desktop))
    if desktop:report["owned_desktop_closed"]=bool(u.CloseDesktop(desktop))
    if station:report["owned_station_closed"]=bool(u.CloseWindowStation(station))
report["source_sha256"]=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
path=Path(__file__).with_name("ui-station-readiness-"+tag+".json")
with path.open("x",encoding="utf-8") as f:json.dump(report,f,indent=2)
print(json.dumps({"path":str(path),"result":report}),flush=True)
