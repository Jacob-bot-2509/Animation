# -*- coding: utf-8 -*-
"""Registered remote sandbox sender. Default PLAN; explicit native collection.
Receiver reconciliation is separate and cannot issue a production certificate.
"""
from __future__ import annotations
import argparse,hashlib,ipaddress,json,platform,re,socket,subprocess,sys,time,uuid
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REGISTERED_ROOT=ROOT/"reviews/codex-supervision/2026-10-06-all43-sandbox-repair"
INTERFACE_COMMAND="Get-NetIPAddress -AddressFamily IPv6 | Select-Object IPAddress,PrefixLength | ConvertTo-Json -Compress"
SCHEMA="native-remote-sender-v2"
WITNESS_SCHEMA="sandbox-witness-receiver-v2"
APPROVED_WITNESSES={
    "python_source":"571f4ce31465a84147395abd9778845194ac591371234737ccf2abeebc6be75e",
    "frozen_executable":"d6887098ccd3b1c3b9bde1180746558b78d2b2882b3cbee25d791c5f792f1cad"}
sys.path.insert(0,str(ROOT/"src"))

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def registered(path,must_exist=True):
    p=Path(path).absolute()
    if ".." in p.parts or not p.is_relative_to(REGISTERED_ROOT):
        raise ValueError("Output/evidence must stay inside the registered all43 root")
    for part in (p,*p.parents):
        if part.exists():
            st=part.lstat()
            if part.is_symlink() or getattr(st,"st_file_attributes",0)&0x400:
                raise ValueError("Reparse output/evidence path")
        elif must_exist:
            raise FileNotFoundError(part)
        if part==REGISTERED_ROOT:break
    return p

def write_bytes(path,data):
    with Path(path).open("xb") as stream:
        stream.write(data)
    return digest(path)

def write_json(path,data):
    return write_bytes(path,(json.dumps(data,ensure_ascii=False,indent=2)+"\n").encode("utf-8"))

def validate(bind,udp_port,tcp_port,round_name,observe_seconds,scope):
    address=ipaddress.ip_address(bind)
    if address.is_unspecified or address.is_multicast or address.is_loopback:
        raise ValueError("A distinct receiver literal address is required")
    if any(type(p) is not int or not 1024<=p<=65535 for p in (udp_port,tcp_port)):
        raise ValueError("Receiver ports must be integer 1024..65535")
    if udp_port==tcp_port:raise ValueError("Use distinct UDP/TCP receiver ports")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}",round_name):
        raise ValueError("Round must be a simple bounded identifier")
    if type(observe_seconds) is not int or not 21<=observe_seconds<=90:
        raise ValueError("Observation must be an integer 21..90 seconds")
    if scope=="external" and not address.is_global:
        raise ValueError("External scope requires a global literal receiver")
    return address

def send(endpoint,payload,family,protocol):
    started=time.monotonic_ns()
    try:
        with socket.socket(family,socket.SOCK_DGRAM if protocol=="udp" else socket.SOCK_STREAM) as s:
            s.settimeout(4 if protocol=="udp" else 6)
            if protocol=="udp":s.sendto(payload,endpoint)
            else:
                s.connect(endpoint);s.sendall(payload);s.shutdown(socket.SHUT_WR)
        return {"outcome":"sent" if protocol=="udp" else "completed",
                "elapsed_ns":time.monotonic_ns()-started,"receiver_delivery_verified":False}
    except OSError as exc:
        return {"outcome":"error","error_type":type(exc).__name__,
                "winerror":getattr(exc,"winerror",None),"detail":str(exc),
                "elapsed_ns":time.monotonic_ns()-started,"receiver_delivery_verified":False}

def capture(command,directory,tag,timeout):
    start=time.monotonic_ns();timed_out=False
    try:
        cp=subprocess.run(command,capture_output=True,timeout=timeout,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform=="win32" else 0)
        stdout,stderr,rc=cp.stdout,cp.stderr,cp.returncode
    except subprocess.TimeoutExpired as exc:
        stdout,stderr,rc=exc.stdout or b"",exc.stderr or b"",None;timed_out=True
    except OSError as exc:
        stdout,stderr,rc=b"",str(exc).encode("utf-8"),None
    out=directory/(tag+".stdout.bin");err=directory/(tag+".stderr.bin")
    return {"command_argv":command,"rc":rc,"timed_out":timed_out,
        "elapsed_ns":time.monotonic_ns()-start,
        "path":str(out),"sha256":write_bytes(out,stdout),
        "stderr_path":str(err),"stderr_sha256":write_bytes(err,stderr),
        "stderr":stderr.decode("utf-8","replace")}

def interface_rows(proof):
    p=registered(proof["path"])
    if (digest(p)!=proof["sha256"] or proof.get("rc")!=0
            or type(proof.get("rc")) is not int or proof.get("stderr")!=""):
        raise ValueError("Native interface capture incomplete/changed")
    err=registered(proof["stderr_path"])
    if digest(err)!=proof["stderr_sha256"] or err.read_bytes()!=b"":
        raise ValueError("Native interface stderr changed/nonempty")
    data=json.loads(p.read_text(encoding="utf-8-sig"))
    if isinstance(data,dict):data=[data]
    if not isinstance(data,list) or not data:raise ValueError("Empty native interfaces")
    return data

def check_scope(address,scope,interfaces):
    rows=interface_rows(interfaces)
    for row in rows:
        local=ipaddress.ip_address(row["IPAddress"].split("%")[0])
        prefix=row["PrefixLength"]
        if type(prefix) is not int or not 0<=prefix<=local.max_prefixlen:
            raise ValueError("Invalid interface prefix")
        if address==local:raise ValueError("Receiver is on the sender itself")
        if scope=="external" and (address in ipaddress.ip_network((local,prefix),strict=False)
            or address.version==6 and address in ipaddress.ip_network((local,64),strict=False)):
            raise ValueError("Receiver is inside the sender LAN, not external")

def probe_source(bind,ports,nonces,protocols):
    spec=[(p,bind,ports[p],nonces[p]["sandbox"]) for p in protocols]
    return "SPEC="+repr(spec)+"\n"+r'''
import json,_socket,time
r={}
for protocol,host,port,nonce in SPEC:
    family=_socket.AF_INET6 if ":" in host else _socket.AF_INET
    started=time.monotonic_ns()
    try:
        with _socket.socket(family,_socket.SOCK_DGRAM if protocol=="udp" else _socket.SOCK_STREAM) as s:
            s.settimeout(4 if protocol=="udp" else 6)
            if protocol=="udp":s.sendto(nonce.encode("ascii"),(host,port))
            else:
                s.connect((host,port));s.sendall(nonce.encode("ascii"));s.shutdown(_socket.SHUT_WR)
        r[protocol]={"outcome":"sent" if protocol=="udp" else "completed"}
    except OSError as exc:
        code=getattr(exc,"winerror",None)
        outcome="os_denied" if code==10013 else "timeout" if isinstance(exc,TimeoutError) else "error"
        r[protocol]={"outcome":outcome,"winerror":code,"error_type":type(exc).__name__,"detail":str(exc)}
    r[protocol]["elapsed_ns"]=time.monotonic_ns()-started
print(json.dumps(r),flush=True)
'''

def wait_until(deadline):
    while True:
        remaining=deadline-time.monotonic_ns()
        if remaining<=0:return
        time.sleep(min(1/5,remaining/1_000_000_000))

def collect(args):
    from animtrain import sandbox_execution as se
    address=validate(args.bind,args.udp_port,args.tcp_port,args.round,args.observe_seconds,args.scope)
    base=registered(args.out,False);base.mkdir(parents=True,exist_ok=True);registered(base)
    directory=base/("remote-"+uuid.uuid4().hex);directory.mkdir(exist_ok=False)
    file=directory/"sender.json"
    protocols=["tcp","udp"] if args.protocol=="both" else [args.protocol]
    ports={"tcp":args.tcp_port,"udp":args.udp_port}
    before={n:se.digest(ROOT/n) for n in se.BOUND_FILES}
    driver_before=digest(__file__)
    report={"schema":SCHEMA,"run_id":directory.name,"round":args.round,
        "scope":args.scope,"bind":str(address),"ports":ports,"protocols":protocols,
        "sender_identity":{"hostname":socket.gethostname(),"os":platform.platform(),"python":sys.version},
        "driver_source_path":str(Path(__file__).resolve()),"driver_before_sha256":driver_before,
        "implementation_before":before,"started_utc_ns":time.time_ns(),
        "started_monotonic_ns":time.monotonic_ns(),
        "nonces":{p:{phase:uuid.uuid4().hex for phase in ("before","sandbox","after")} for p in protocols},
        "phases":{},"complete":False,"verification_status":"UNVERIFIED",
        "production_gate":"CLOSED","certificate_written":False}
    try:
        family=socket.AF_INET6 if address.version==6 else socket.AF_INET
        command=["tracert","-6" if address.version==6 else "-4","-d","-h","4","-w","500",str(address)]
        report["route"]=capture(command,directory,"route",30)
        interface_command=INTERFACE_COMMAND if address.version==6 else INTERFACE_COMMAND.replace("IPv6","IPv4")
        report["sender_interfaces"]=capture(["powershell","-NoProfile","-Command",interface_command],
            directory,"interfaces-"+str(address.version),30)
        report["sender_interfaces"]["command"]=interface_command
        # Always retain IPv6 topology for the user-authorized joint envelope.
        if address.version==4:
            report["sender_ipv6_interfaces"]=capture(["powershell","-NoProfile","-Command",INTERFACE_COMMAND],
                directory,"interfaces-6",30)
            report["sender_ipv6_interfaces"]["command"]=INTERFACE_COMMAND
        check_scope(address,args.scope,report["sender_interfaces"])
        def controls(phase):
            for p in protocols:
                t0=time.monotonic_ns()
                result=send((str(address),ports[p]),report["nonces"][p][phase].encode("ascii"),family,p)
                report["phases"][phase+"_"+p]={"started_monotonic_ns":t0,
                    "finished_monotonic_ns":time.monotonic_ns(),"result":result}
        controls("before")
        if any(report["phases"]["before_"+p]["result"]["outcome"]=="error" for p in protocols):
            raise ValueError("Host before-send failed; no healthy fixture for this run")
        if before!={n:se.digest(ROOT/n) for n in se.BOUND_FILES} or digest(__file__)!=driver_before:
            raise ValueError("Implementation changed before native launch")
        source=probe_source(str(address),ports,report["nonces"],protocols)
        report["source"]=source;report["sandbox_started_monotonic_ns"]=time.monotonic_ns()
        cp=se.run_code(source,mode="probe",timeout_ms=120000)
        # Keep every original field and byte-equivalent stream; never strip/truncate.
        report["transport"]=cp
        report["sandbox_finished_monotonic_ns"]=time.monotonic_ns()
        start=time.monotonic_ns()
        report["observation"]={"started_monotonic_ns":start,"requested_seconds":args.observe_seconds}
        # AFTER reaches the receiver >=20 s after the sandbox returned and is within the recorded window.
        wait_until(start+(args.observe_seconds-1)*1_000_000_000)
        controls("after")
        wait_until(max(start+args.observe_seconds*1_000_000_000,time.monotonic_ns()+200_000_000))
        report["observation"]["finished_monotonic_ns"]=time.monotonic_ns()
        report["observation"]["elapsed_ns"]=report["observation"]["finished_monotonic_ns"]-start
        report["complete"]=True
    except Exception as exc:
        report["error"]={"error_type":type(exc).__name__,"detail":str(exc)}
        if isinstance(exc,subprocess.TimeoutExpired):
            report["timeout_evidence"]={"parent_evidence":getattr(exc,"parent_evidence",None),
                "work":str(getattr(exc,"work",""))}
    finally:
        report["finished_utc_ns"]=time.time_ns();report["finished_monotonic_ns"]=time.monotonic_ns()
        report["implementation_after"]={n:se.digest(ROOT/n) for n in se.BOUND_FILES}
        report["driver_after_sha256"]=digest(__file__)
        report["implementation_unchanged"]=(before==report["implementation_after"] and driver_before==report["driver_after_sha256"])
        checksum=write_json(file,report)
    result={"path":str(file),"sha256":checksum,"complete":report["complete"],
        "implementation_unchanged":report["implementation_unchanged"],"verification_status":"UNVERIFIED",
        "receiver_receipt_required":True,"production_gate":"CLOSED","error":report.get("error")}
    print(json.dumps(result,ensure_ascii=False))
    return 0 if report["complete"] and report["implementation_unchanged"] and report["transport"]["rc"]==0 else 2

def receiver_packets(report,log_path,summary_path,receiver_rc):
    """Full original v2 witness logs, not send() success, establish every control."""
    from animtrain.full_surface_evidence import BoundaryFailure
    if type(receiver_rc) is not int or receiver_rc!=0:raise ValueError("Actual receiver rc0 required")
    log=registered(log_path);summary_file=registered(summary_path)
    raw=log.read_bytes();summary=json.loads(summary_file.read_bytes())
    if summary.get("schema")!=WITNESS_SCHEMA or summary.get("log_sha256")!=hashlib.sha256(raw).hexdigest():
        raise ValueError("Witness schema/log hash changed")
    required=("receiver_complete","implementation_unchanged","deadline_reached","listeners_closed")
    if any(summary.get(k) is not True for k in required) or summary.get("errors")!=[] or summary.get("interrupted") is not False:
        raise ValueError("Witness lifecycle incomplete")
    identity=summary["implementation"]
    if identity.get("sha256")!=APPROVED_WITNESSES.get(identity.get("kind")):
        raise ValueError("Witness executable/source is not the approved version")
    started=summary["started_monotonic_ns"];finished=summary["finished_monotonic_ns"]
    seconds=summary["requested_seconds"]
    if (type(started) is not int or type(finished) is not int or type(seconds) is not int
            or not 20<=seconds<=900 or finished-started<seconds*1_000_000_000):
        raise ValueError("Witness duration incomplete")
    rows=[json.loads(line) for line in raw.splitlines()]
    if not rows or rows[0].get("kind")!="created" or rows[-1].get("kind")!="closed":
        raise ValueError("Witness start/close records missing")
    if rows[0].get("implementation")!=identity or rows[0].get("bind")!=summary["bind"]:
        raise ValueError("Witness identity changed")
    if rows[-1].get("receiver_complete") is not True or rows[-1].get("listeners_closed") is not True or rows[-1].get("deadline_reached") is not True:
        raise ValueError("Witness close not complete")
    host=rows[0].get("host")
    if not host or host.casefold()==report["sender_identity"]["hostname"].casefold():
        raise ValueError("Witness is not a distinct host")
    addr=ipaddress.ip_address(report["bind"])
    if ipaddress.ip_address(summary["bind"])!=addr or summary["address_family"]!=addr.version:
        raise ValueError("Witness endpoint family/address differs")
    if addr.version==6 and summary.get("ipv6_only") is not True:
        raise ValueError("IPv6-only receiver not proven")
    previous=-1;listening=0;packets={p:[] for p in report["protocols"]}
    all_payloads=0;phase_order={p:[] for p in report["protocols"]}
    for seq,row in enumerate(rows,1):
        mono=row.get("monotonic_ns")
        if (row.get("schema")!=WITNESS_SCHEMA or row.get("run_id")!=summary["run_id"]
                or type(row.get("seq")) is not int or row["seq"]!=seq
                or type(mono) is not int or mono<previous):
            raise ValueError("Witness sequence/run/time corrupted")
        previous=mono
        if row["kind"]=="error":raise ValueError("Witness raw error")
        if row["kind"]=="listening":
            listening+=1
            if row.get("endpoints")!=summary["endpoints"] or row.get("implementation")!=identity:
                raise ValueError("Witness listening endpoint/identity mismatch")
        if row["kind"]!="payload":continue
        all_payloads+=1
        payload=bytes.fromhex(row["payload_hex"])
        for values in report["nonces"].values():
            if values["sandbox"].encode("ascii") in payload:raise BoundaryFailure("Actual sandbox payload received")
        proto=row.get("protocol")
        if proto not in packets:raise ValueError("Unattributed other-protocol payload")
        endpoint=summary["endpoints"][proto]
        if (row.get("endpoint")!=endpoint or ipaddress.ip_address(endpoint[0])!=addr
                or endpoint[1]!=report["ports"][proto] or row.get("capture_complete") is not True
                or row.get("exact_nonce") is not True or len(payload)!=32
                or row.get("bytes")!=32 or payload.decode("ascii")!=row.get("nonce")):
            raise ValueError("Incomplete/unattributed receiver payload")
        if not started<=mono<=finished:raise ValueError("Payload outside live receiver window")
        nonce=row["nonce"];values=report["nonces"][proto]
        phase=next((p for p,n in values.items() if n==nonce),None)
        if phase not in ("before","after"):raise ValueError("Unknown/duplicate attribution")
        phase_order[proto].append(phase);packets[proto].append(nonce)
    if listening!=1 or summary["records"]!=all_payloads:
        raise ValueError("Receiver event/count mismatch")
    for p in packets:
        if phase_order[p]!=["before","after"]:raise ValueError("Missing/repeated/out-of-order health controls")
    return packets,{"log_path":str(log),"log_sha256":digest(log),
        "summary_path":str(summary_file),"summary_sha256":digest(summary_file),
        "rc":receiver_rc,"host":host,"implementation":identity,"receiver_run_id":summary["run_id"]}

def reconcile(args):
    from animtrain import full_surface_evidence as fe,sandbox_execution as se
    path=registered(args.reconcile);raw=json.loads(path.read_bytes())
    if raw.get("schema")!=SCHEMA or raw.get("complete") is not True or raw.get("error"):
        raise ValueError("Sender run incomplete/unsupported; do not re-sign legacy evidence")
    if raw.get("implementation_unchanged") is not True or raw["driver_before_sha256"]!=raw["driver_after_sha256"]:
        raise ValueError("Whole sender implementation changed")
    if (raw["driver_source_path"]!=str(Path(__file__).resolve()) or digest(__file__)!=raw["driver_before_sha256"]):
        raise ValueError("Sender collector source changed")
    protocols=raw["protocols"]
    if not protocols or len(set(protocols))!=len(protocols) or set(protocols)-{"tcp","udp"}:
        raise ValueError("Unregistered sender protocols")
    nonces=[n for p in protocols for n in raw["nonces"][p].values()]
    if (len(set(nonces))!=3*len(protocols) or any(not re.fullmatch("[0-9a-f]{32}",n) for n in nonces)
            or any(set(raw["nonces"][p])!={"before","sandbox","after"} for p in protocols)):
        raise ValueError("Ambiguous sender phase nonces")
    row={"source":raw["source"],"transport":raw["transport"],
        "implementation_before":raw["implementation_before"],"implementation_after":raw["implementation_after"]}
    cp,data=fe.transport(row)
    if cp["rc"]!=0 or set(data)!=set(protocols):raise ValueError("Native sender output incomplete")
    address=ipaddress.ip_address(raw["bind"]);check_scope(address,raw["scope"],raw["sender_interfaces"])
    obs=raw["observation"];start,end=obs["started_monotonic_ns"],obs["finished_monotonic_ns"]
    measured=(start,end,obs["elapsed_ns"],raw["sandbox_started_monotonic_ns"],raw["sandbox_finished_monotonic_ns"])
    if (any(type(v) is not int or v<=0 for v in measured) or start<raw["sandbox_finished_monotonic_ns"]
            or raw["sandbox_started_monotonic_ns"]>raw["sandbox_finished_monotonic_ns"]
            or obs["elapsed_ns"]!=end-start or end-start<20_000_000_000):
        raise ValueError("Measured post-attempt observation incomplete")
    for p in protocols:
        before=raw["phases"]["before_"+p];after=raw["phases"]["after_"+p]
        times=[phase[key] for phase in (before,after) for key in ("started_monotonic_ns","finished_monotonic_ns")]
        if (any(type(v) is not int or v<=0 for v in times)
                or before["started_monotonic_ns"]>before["finished_monotonic_ns"]
                or before["finished_monotonic_ns"]>raw["sandbox_started_monotonic_ns"]
                or not start+20_000_000_000<=after["started_monotonic_ns"]<=after["finished_monotonic_ns"]<=end
                or before["result"]["outcome"] not in ("sent","completed")
                or after["result"]["outcome"] not in ("sent","completed")):
            raise ValueError("Sender controls not within the required live window")
    packets,receipt=receiver_packets(raw,args.receiver_log,args.receiver_summary,args.receiver_rc)
    cases={}
    for p in protocols:
        point="D9" if raw["scope"]=="lan" else ("D2" if p=="tcp" else "D8") if address.version==6 else ("D1" if p=="tcp" else "D7")
        case={**row,"operation":fe.NETWORKS[point],"wire_protocol":p,
            "endpoint":[str(address),raw["ports"][p]],"nonces":raw["nonces"][p],"packets":packets[p],
            "receiver_complete":True,"receiver_errors":[],"post_attempt_observation_ns":end-start,
            "observation_key":p,"receiver_evidence":receipt,"sender_raw_path":str(path),"sender_raw_sha256":digest(path)}
        if raw["scope"]=="lan":case["independent_lan_peer"]=True
        else:case["controlled_remote_peer"]=True
        fe.network(point,case);cases[p]={"point":point,"case":case}
    result={"schema":"registered-remote-reconciliation-v1","cases":cases,
        "scope":"Only the registered native receiver protocols; not a whole-43 certificate",
        "production_gate":"CLOSED","certificate_written":False,"full_surface_accepted":False}
    target=path.parent/("reconciled-"+uuid.uuid4().hex+".json")
    checksum=write_json(target,result)
    print(json.dumps({"path":str(target),"sha256":checksum,"verified_protocols":list(cases),
        "production_gate":"CLOSED","full_surface_accepted":False}))
    return 0

def main(argv=None):
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--execute-native",action="store_true")
    ap.add_argument("--bind");ap.add_argument("--udp-port",type=int,default=49001)
    ap.add_argument("--tcp-port",type=int,default=49002)
    ap.add_argument("--round");ap.add_argument("--scope",choices=("lan","external"),default="lan")
    ap.add_argument("--protocol",choices=("both","tcp","udp"),default="both")
    ap.add_argument("--observe-seconds",type=int,default=21)
    ap.add_argument("--out",type=Path,default=REGISTERED_ROOT/"external-tests")
    ap.add_argument("--reconcile",type=Path)
    ap.add_argument("--receiver-log",type=Path);ap.add_argument("--receiver-summary",type=Path)
    ap.add_argument("--receiver-rc",type=int)
    args=ap.parse_args(argv)
    try:
        if args.reconcile:
            if args.execute_native:raise ValueError("Collection and reconciliation are separate actions")
            if args.receiver_log is None or args.receiver_summary is None or args.receiver_rc is None:
                raise ValueError("Reconciliation requires actual original receiver log, summary and rc")
            return reconcile(args)
        if not args.execute_native:
            print(json.dumps({"status":"PLAN","native_execution":False,
                "required":["--execute-native --bind LITERAL --round NAME --scope lan|external",
                            "Complete original receiver v2 JSONL, summary and actual rc"],
                "public_ipv4_node_required":False,"production_gate":"CLOSED"}))
            return 3
        if not args.bind or not args.round:raise ValueError("Native collection requires bind and round")
        return collect(args)
    except Exception as exc:
        from animtrain.full_surface_evidence import BoundaryFailure
        print(json.dumps({"status":"FAIL" if isinstance(exc,BoundaryFailure) else "PARTIAL",
            "error_type":type(exc).__name__,"detail":str(exc),"production_gate":"CLOSED",
            "certificate_written":False},ensure_ascii=False))
        return 2

if __name__=="__main__":
    raise SystemExit(main())
