"""Recompute the registered 43-point surface; labels alone never open the gate.

GREEN covers only a point's registered fixture/protocol matrix. It is not a
universal claim about every endpoint, every Windows object or future code.
"""
from __future__ import annotations
import hashlib, ipaddress, json, re
from pathlib import Path

POINTS = tuple(f"{prefix}{i}" for prefix,count in (("A",9),("B",5),("C",7),("D",13),("E",3),("F",6)) for i in range(1,count+1))
ROOT=Path(__file__).resolve().parents[2]
WORK_ROOT=ROOT/"reviews/codex-supervision/2026-10-05-three-gates"
REVIEW_ROOT=ROOT/"reviews/codex-supervision/2026-10-06-all43-sandbox-repair"
PERMISSIONS={"C1":"read_outside","C2":"write_outside","C3":"write_toolchain","C4":"cross_run_write",
             "C6":"junction_escape","C7":"delete_outside","F1":"registry_write",
             "F2":"pipe_access","F3":"mailslot_access","F4":"mapping_access"}
NETWORKS={"D1":"external_tcp_v4","D2":"external_tcp_v6","D3":"loopback_tcp_v4","D4":"loopback_tcp_v6",
          "D5":"loopback_udp_v4","D6":"loopback_udp_v6","D7":"external_udp_v4","D8":"external_udp_v6",
          "D9":"lan_peer","D10":"uncached_dns","D11":"native_executables","D12":"icmp","D13":"winhttp_wininet"}

class BoundaryFailure(ValueError): pass

def digest(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def bound_path(value, allowed):
    path=Path(value).absolute()
    if ".." in path.parts or not path.is_relative_to(allowed):
        raise ValueError("Evidence path outside registered scope")
    for part in (path,*path.parents):
        st=part.lstat()
        if part.is_symlink() or getattr(st,"st_file_attributes",0)&0x400:
            raise ValueError("Reparse evidence path")
        if part==allowed: break
    return path

def transport(row):
    from .sandbox_execution import BOUND_FILES
    from .isolation_evidence import _parent
    cp=row["transport"]
    if type(cp.get("rc")) is not int: raise ValueError("Native exit code must be an integer")
    _parent(cp["parent_evidence"])
    work=bound_path(cp["work"],WORK_ROOT)
    if not re.fullmatch(r"execution-[0-9a-f]{32}",work.name): raise ValueError("Unregistered work")
    source=work/"scene.py"
    if digest(source)!=cp["source_sha256"] or source.read_text(encoding="utf-8")!=row["source"]:
        raise ValueError("Executed source changed")
    expected=[str((ROOT/".venv/Scripts/python.exe").resolve()),"-I","-B",str(source)]
    if cp["command"]!=expected: raise ValueError("Command changed")
    for name in ("stdout","stderr"):
        if (work/(name+".txt")).read_bytes().decode("utf-8","replace")!=cp[name]:
            raise ValueError("Raw stream changed")
    acl=cp["parent_evidence"]["private_profile"]["temporary_acl"]
    expected_paths={str(p.resolve()) for p in (ROOT/".venv",ROOT/".sandbox-runtime/miktex-real",Path(r"D:\Python"),work)}
    if len(acl)!=4 or {str(Path(v["path"]).resolve()) for v in acl}!=expected_paths:
        raise ValueError("ACL grant roots not exact")
    if cp["parent_evidence"].get("inherited_handle_count")!=3:
        raise ValueError("Native stdio handle allowlist not recorded")
    if row["implementation_before"]!={n:digest(ROOT/n) for n in BOUND_FILES} or row["implementation_after"]!=row["implementation_before"]:
        raise ValueError("Implementation bindings changed")
    data=json.loads(cp["stdout"])
    if not isinstance(data,dict): raise ValueError("Non-object output")
    return cp,data

def complete_controls(case):
    for phase in ("before","after"):
        control=case["controls"][phase]
        if control.get("outcome")!="allowed" or control.get("fixture")!=case["fixture"]:
            raise ValueError("Missing same-fixture health control")
    if case.get("fixture_alive_throughout") is not True: raise ValueError("Fixture lifetime incomplete")

def permission(point,case):
    if case["operation"]!=PERMISSIONS[point]: raise ValueError("Wrong operation")
    cp,data=transport(case);complete_controls(case)
    state=data[case["observation_key"]]
    if state.get("outcome")=="allowed": raise BoundaryFailure("Sandbox accessed registered host fixture")
    if cp["rc"]!=0 or state.get("outcome")!="os_denied" or state.get("winerror")!=5:
        raise ValueError("No typed access denial")
    if case.get("host_unchanged") is not True: raise BoundaryFailure("Host mutation/unknown")
    if point=="C6" and (case.get("preexisting_junction_verified") is not True or case.get("target_acl_unchanged") is not True):
        raise ValueError("Existing junction and target DACL not verified")
    if point=="C4" and case.get("cache_denied") is not True: raise ValueError("Cross-run cache not checked")
    if point=="F2" and case.get("matrix")!=["named_local","named_cross_user","anonymous"]:
        raise ValueError("Pipe namespace/cross-user matrix incomplete")
    if point=="F4" and case.get("matrix")!=["Local","Global"]: raise ValueError("Mapping namespace matrix incomplete")
    if point in ("F2","F4"):
        if set(data.get("matrix",{}))!=set(case["matrix"]) or any(v.get("outcome")!="os_denied" or v.get("winerror") not in (5,6) for v in data["matrix"].values()):
            raise ValueError("IPC matrix lacks per-operation native denials")

def network(point,case):
    if case["operation"]!=NETWORKS[point]: raise ValueError("Wrong protocol")
    cp,data=transport(case)
    if cp["rc"]!=0: raise ValueError("Native network probe failed")
    nonces=case["nonces"]
    if set(nonces)!={"before","sandbox","after"} or len(set(nonces.values()))!=3 or any(not re.fullmatch("[0-9a-f]{32}",v) for v in nonces.values()):
        raise ValueError("Ambiguous phase nonces")
    packets=case["packets"]
    if nonces["sandbox"] in packets: raise BoundaryFailure("Sandbox delivery")
    if packets.count(nonces["before"])!=1 or packets.count(nonces["after"])!=1 or any(v not in nonces.values() for v in packets):
        raise ValueError("Missing/unattributed receiver control")
    if case.get("receiver_complete") is not True or case.get("receiver_errors")!=[] or type(case.get("post_attempt_observation_ns")) is not int or case["post_attempt_observation_ns"]<20_000_000_000:
        raise ValueError("Incomplete observation window")
    state=data[case["observation_key"]]
    denied=state.get("outcome")=="os_denied" and state.get("winerror")==10013
    bounded=state.get("outcome") in ("sent","completed","timeout")
    if not denied and not bounded: raise ValueError("Unexplained outcome")
    if state.get("outcome")=="timeout" and state.get("error_type")!="TimeoutError": raise ValueError("Untyped timeout")
    if point in ("D1","D2","D7","D8"):
        addr=ipaddress.ip_address(case["endpoint"][0])
        if not addr.is_global or addr.version!=(6 if point in ("D2","D8") else 4) or case.get("controlled_remote_peer") is not True:
            raise ValueError("Not the registered external receiver")
    if point=="D9" and case.get("independent_lan_peer") is not True: raise ValueError("No distinct LAN host")
    if point=="D10" and case.get("fresh_query_capture_complete") is not True: raise ValueError("DNS cache/egress unknown")
    if point=="D11" and case.get("executable_matrix_complete") is not True: raise ValueError("Native executable matrix missing")
    if point=="D12" and case.get("echo_id_sequence_payload_verified") is not True: raise ValueError("No correlated ICMP capture")
    if point=="D13" and case.get("api_matrix")!=["WinHTTP","WinINET"]: raise ValueError("HTTP stacks incomplete")

def host_capture(case):
    path=bound_path(case["host_stdout_path"],REVIEW_ROOT)
    if digest(path)!=case["host_stdout_sha256"]: raise ValueError("Host native output changed")
    code=bound_path(case["host_source_path"],REVIEW_ROOT)
    if code!=REVIEW_ROOT/"host_cases.py" or digest(code)!=case["host_source_sha256"]: raise ValueError("Host native source changed")
    if case["host_rc"]!=0: raise ValueError("Host fixture failed")
    return json.loads(path.read_text(encoding="utf-8"))

def specialized(point,case):
    if point=="A6":
        cp,_=transport(case);data=host_capture(case)
        if cp["rc"]!=0 or set(data["reparse_cases"])!={"root","ancestor"} or any(v.get("rejected_before_profile") is not True or v.get("create_calls")!=0 or v.get("acl_unchanged") is not True for v in data["reparse_cases"].values()):
            raise ValueError("Literal reparse/ancestor grants not rejected")
    elif point in ("A8","A9","B5"):
        data=host_capture(case)
        if point=="A8":
            if data.get("preexisting_sid_rejected") is not True or data.get("grant_calls")!=0 or data.get("profile_deleted") is not True or data.get("acl_unchanged") is not True:
                raise ValueError("Fresh SID collision abort not verified")
        elif point=="A9":
            if data.get("first_native_profile_acquired") is not True or data.get("second_errno")!=13 or data.get("second_profile_create_calls")!=0 or data.get("first_cleanup_complete") is not True or data.get("same_lock_path") is not True:
                raise ValueError("Cross-process lock proof incomplete")
        elif data.get("assignment_error")!=5 or data.get("resume_calls")!=0 or data.get("created_suspended") is not True or data.get("root_wait_result")!=0 or data.get("profile_cleanup_complete") is not True:
            raise ValueError("Native assignment failure did not close")
    elif point=="B1":
        cp,data=transport(case)
        if data.get("external_handle_file_id")==case["host_file_id"]: raise BoundaryFailure("Unrelated host handle inherited")
        if cp["rc"]!=0 or data.get("external_handle_query_error") not in (None,6,-1073741816) or data.get("stdio_count")!=3 or case.get("host_inheritable_control_verified") is not True:
            raise ValueError("Unrelated inheritable handle not excluded")
    elif point in ("B2","B3"):
        cp,_=transport(case)
        if point=="B2" and cp["rc"]!=0: raise ValueError("Root exit failed")
        if point=="B3" and case.get("timed_out") is not True: raise ValueError("No transport timeout")
        children=case["held_children"]
        if len(children)<2 or any(v.get("opened_while_live") is not True or v.get("same_handle_retained") is not True or v.get("signaled_wait_result")!=0 or type(v.get("creation_filetime")) is not int or v["creation_filetime"]<=0 for v in children):
            raise ValueError("Child/grandchild handles not proven terminated")
    elif point=="B4":
        cp,data=transport(case)
        if cp["rc"]!=17 or data.get("memory_denied") is not True or data.get("chunk_bytes")!=67108864 or type(data.get("allocated_chunks")) is not int or not 0<data["allocated_chunks"]<32:
            raise ValueError("2 GiB memory denial missing")
    elif point=="C5":
        cp,_=transport(case)
        entries=case["protected_files"]
        if cp["rc"]!=0 or len(entries)<4 or any(v["before_sha256"]!=v["after_sha256"] or digest(Path(v["path"]))!=v["after_sha256"] for v in entries):
            raise ValueError("Protected files changed/unknown")
    elif point in ("F5","F6"):
        cp,data=transport(case);complete_controls(case)
        station=case["isolated_window_station"]
        if not re.fullmatch("AnimTrainCodex-[0-9a-f]{32}",station) or data.get("window_station")!=station or case.get("user_clipboard_accessed") is not False:
            raise ValueError("No independently isolated Windows UI fixture")
        keys=("clipboard_read","clipboard_write") if point=="F5" else ("window_message","global_hook")
        if cp["rc"]!=0 or any(data.get(k,{}).get("outcome")!="os_denied" or data[k].get("winerror")!=5 for k in keys):
            raise ValueError("UI primitive matrix incomplete")
        if point=="F5" and case.get("synthetic_clipboard_unchanged") is not True:
            raise ValueError("Synthetic clipboard mutation/unknown")
    else: raise ValueError("Unregistered point")

def recompute(raw):
    results={point:{"status":"GAP","reason":"No current complete evidence"} for point in POINTS}
    if raw.get("schema")!="sandbox-surface-native-v1": raise ValueError("Unrecognized 43-point evidence")
    from .sandbox_execution import BOUND_FILES
    current={n:digest(ROOT/n) for n in BOUND_FILES}
    if raw.get("initial_bindings")!=current:
        return {p:{"status":"PARTIAL","reason":"Whole-run implementation binding changed or absent"} for p in POINTS}
    cases=raw.get("cases",{})
    for point in POINTS:
        try:
            if point not in cases: continue
            case=cases[point]
            if point in PERMISSIONS: permission(point,case)
            elif point in NETWORKS: network(point,case)
            elif point in ("A1","A2","A3","A4","A5","A7"):
                jobs=case["jobs"]
                if len(jobs)<2: raise ValueError("Two fresh native jobs required")
                profiles=[]
                for row in jobs:
                    cp,_=transport(row)
                    if cp["rc"]!=0: raise ValueError("Incomplete identity job")
                    profiles.append(cp["parent_evidence"]["private_profile"]["profile_name"])
                if len(profiles)!=len(set(profiles)): raise ValueError("Profile reused")
            elif point=="E1":
                cp,data=transport(case)
                if cp["rc"]!=0 or set(data.get("shim",{}))!={"connect","connect_ex","sendto","getaddrinfo"} or any(v!="B4-network-isolation: blocked" for v in data["shim"].values()):
                    raise ValueError("Four production shim calls not blocked")
            elif point=="E2":
                cp,data=transport(case)
                expected={k:"http://127.0.0.1:9" for k in ("HTTP_PROXY","HTTPS_PROXY","ALL_PROXY","http_proxy","https_proxy","all_proxy")}
                expected.update(NO_PROXY="",no_proxy="")
                if cp["rc"]!=0 or data.get("proxy_environment")!=expected: raise ValueError("Production proxies not exact")
            elif point=="E3":
                from . import net_guard
                doc=net_guard.__doc__ or ""
                if not all(s in doc for s in ("_socket","sitecustomize","纵深防御")): raise ValueError("Boundary disclaimer missing")
                if case.get("source_sha256")!=digest(ROOT/"src/animtrain/net_guard.py"): raise ValueError("Policy source changed")
            else:
                specialized(point,case)
            results[point]={"status":"GREEN","scope":"Registered fixture matrix only"}
        except BoundaryFailure as exc:
            results[point]={"status":"FAIL","reason":str(exc)}
        except Exception as exc:
            results[point]={"status":"PARTIAL","reason":str(exc)}
    return results

def require_complete_surface(certificate):
    path=bound_path(certificate["surface_raw_path"],REVIEW_ROOT)
    if digest(path)!=certificate["surface_raw_sha256"]: raise ValueError("43-point raw evidence changed")
    raw=json.loads(path.read_text(encoding="utf-8"))
    if raw.get("implementation_unchanged") is not True or raw.get("final_bindings")!=raw.get("initial_bindings") or raw.get("error") is not None:
        raise ValueError("Incomplete or changed full surface run")
    results=recompute(raw)
    missing=[point for point,row in results.items() if row["status"]!="GREEN"]
    if missing: raise ValueError("43-point surface incomplete: "+",".join(missing))
    return results
