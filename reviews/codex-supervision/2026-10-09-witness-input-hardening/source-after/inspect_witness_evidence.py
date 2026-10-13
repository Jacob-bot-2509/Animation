"""Read-only witness intake diagnostics. Never modifies evidence or issues acceptance."""
from pathlib import Path
import argparse,hashlib,ipaddress,json,re,importlib.util
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("registered_driver_for_intake",ROOT/"tools/sandbox_external_test_driver.py")
driver=importlib.util.module_from_spec(spec);spec.loader.exec_module(driver)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def inspect(sender_path,log_path,summary_path,receiver_rc):
    sender_path,log_path,summary_path=map(Path,(sender_path,log_path,summary_path))
    before={str(p):sha(p) for p in (sender_path,log_path,summary_path)}
    sender=json.loads(sender_path.read_bytes());summary=json.loads(summary_path.read_bytes())
    rows=[json.loads(z)for z in log_path.read_bytes().splitlines() if z.strip()]
    findings=[]
    def check(code,passed,detail):
        if not passed:findings.append({"code":code,**detail})
    check("ORIGINAL_LOG_SHA_MISMATCH",summary.get("log_sha256")==before[str(log_path)],{"claimed":summary.get("log_sha256"),"actual":before[str(log_path)]})
    expected=driver.approved_witness_hashes(summary.get("implementation",{}).get("kind"))
    supplied=summary.get("implementation",{}).get("sha256")
    check("APPROVED_IMPLEMENTATION_HASH_MISMATCH",supplied in expected,{"expected":sorted(expected),"actual":supplied,"actual_hex_length":len(supplied)if isinstance(supplied,str)else None})
    target=ipaddress.ip_address(sender["bind"]);bind=ipaddress.ip_address(summary["bind"])
    check("EXACT_ENDPOINT_BIND_MISMATCH",bind==target,{"sender_target":str(target),"receiver_bind":str(bind),"receiver_unspecified":bind.is_unspecified})
    start,end,seconds=(summary.get(k)for k in ("started_monotonic_ns","finished_monotonic_ns","requested_seconds"))
    valid=all(type(x)is int for x in (start,end,seconds))
    check("RECEIVER_MONOTONIC_DURATION_INVALID",valid and end-start>=seconds*1_000_000_000,{"started":start,"finished":end,"claimed_seconds":seconds,"elapsed_ns_exact":end-start if valid else None})
    nonces=sender["nonces"];payloads=[r for r in rows if r.get("kind")=="payload"]
    expectedcontrols={p:[nonces[p]["before"],nonces[p]["after"]]for p in sender["protocols"]}
    observed={p:[r.get("nonce")for r in payloads if r.get("protocol")==p]for p in sender["protocols"]}
    check("HEALTH_CONTROLS_MISSING_OR_INVALID",observed==expectedcontrols,{"expected_controls":expectedcontrols,"observed_controls":observed,"payload_count":len(payloads)})
    for r in payloads:
        payload=bytes.fromhex(r.get("payload_hex",""))
        for p in sender["protocols"]:
            if nonces[p]["sandbox"].encode("ascii")in payload:
                findings.append({"code":"ACTUAL_SANDBOX_PAYLOAD_BOUNDARY_FAILURE","protocol":p,"row_sequence":r.get("seq")})
    for r in rows:
        mono=r.get("monotonic_ns")
        kind=r.get("kind")
        if kind in ("listening","payload") and valid:
            check("RAW_EVENT_OUTSIDE_SUMMARY_TIME_WINDOW",type(mono)is int and start<=mono<=end,{"row_sequence":r.get("seq"),"kind":kind,"monotonic_ns":mono})
        elif kind=="closed" and valid:
            # Receiver records finished before implementation hashing and the closed event.
            check("CLOSED_EVENT_BEFORE_COLLECTION_FINISHED",type(mono)is int and mono>=end,{"row_sequence":r.get("seq"),"monotonic_ns":mono,"finished_monotonic_ns":end})
    check("ACTUAL_RECEIVER_RC_MISSING_OR_NONZERO",type(receiver_rc)is int and receiver_rc==0,{"received_rc":receiver_rc,"note":"The caller must provide actual native exit status; never infer from JSON."})
    lifecycle=all(summary.get(k)is True for k in ("receiver_complete","implementation_unchanged","deadline_reached","listeners_closed"))
    check("RECEIVER_LIFECYCLE_INCOMPLETE",lifecycle and summary.get("errors")==[] and summary.get("interrupted")is False,{"flags":[summary.get(k)for k in ("receiver_complete","implementation_unchanged","deadline_reached","listeners_closed")],"errors":summary.get("errors")})
    controlled=None
    if not findings:
        try:
            driver.receiver_packets(sender,log_path,summary_path,receiver_rc)
            controlled="PASS_CURRENT_REGISTERED_RECEIVER_VALIDATOR_ONLY"
        except Exception as exc:
            findings.append({"code":"REGISTERED_VALIDATOR_REJECTED","error_type":type(exc).__name__,"detail":str(exc)})
    assert before=={str(p):sha(p)for p in(sender_path,log_path,summary_path)}
    return {"status":"NOT_ACCEPTED"if findings else"READY_FOR_REGISTERED_RECONCILIATION","run_id":sender["run_id"],"findings":findings,"files":before,"read_only_inputs_unchanged":True,"registered_receiver_check":controlled,"production":"CLOSED","full_surface_accepted":False}


def inspect_capture(sender_path, capture_directory):
    """Validate a bound launcher receipt; this is intake, never sandbox acceptance.

    The receipt is a local producer record, not an authenticated remote attestation.
    Registered reconciliation still must validate the sender and sandbox transport.
    """
    from pathlib import PureWindowsPath
    directory=Path(capture_directory).absolute()
    sender_path=Path(sender_path).absolute()
    raw_names=("receiver.jsonl","receiver.jsonl.summary.json","stdout.bin","stderr.bin")
    paths=[sender_path,*[directory/n for n in (*raw_names,"process-exit.json")]]
    for path in paths:
        for part in (path,*path.parents):
            if part.exists():
                st=part.lstat()
                if part.is_symlink() or getattr(st,"st_file_attributes",0)&0x400:
                    raise ValueError("Reparse evidence path")
        if not path.is_file():raise ValueError("Missing original capture file: "+path.name)
    before={str(path):sha(path) for path in paths}
    sender=json.loads(sender_path.read_bytes())
    summary=json.loads((directory/raw_names[1]).read_bytes())
    rows=[json.loads(line) for line in (directory/raw_names[0]).read_bytes().splitlines() if line.strip()]
    proof=json.loads((directory/"process-exit.json").read_bytes())
    findings=[]
    def check(code,passed):
        if not passed:findings.append({"code":code})
    check("PROCESS_RECEIPT_SCHEMA_OR_MODE",proof.get("schema")=="witness-process-exit-v1" and proof.get("mode")=="SERVE")
    check("PROCESS_EXIT_NOT_ACTUAL_ZERO",type(proof.get("exit_code")) is int and proof["exit_code"]==0 and proof.get("spawn_error") is None)
    capture_id=proof.get("capture_id")
    valid_id=isinstance(capture_id,str) and bool(re.fullmatch("[0-9a-f]{32}",capture_id))
    round_name=proof.get("round")
    check("ROUND_OR_CAPTURE_DIRECTORY_BINDING",
          isinstance(round_name,str) and bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}",round_name))
          and round_name==sender.get("round") and valid_id and directory.name==round_name+"-"+capture_id)
    check("PROCESS_RECEIVER_RUN_MISMATCH",proof.get("receiver_run_id")==summary.get("run_id") and isinstance(summary.get("run_id"),str))
    start,end=proof.get("started_utc_ns"),proof.get("finished_utc_ns")
    valid_time=type(start) is int and type(end) is int and 0<start<end
    check("PROCESS_TIME_INVALID",valid_time)
    if valid_time:
        check("RAW_UTC_OUTSIDE_PARENT_PROCESS",all(type(row.get("utc_ns")) is int and start<=row["utc_ns"]<=end for row in rows))
    check("PROCESS_PID_INVALID",type(proof.get("launched_pid")) is int and proof["launched_pid"]>0)
    # A PyInstaller one-file bootloader starts a child receiver; these PIDs can differ.
    check("WRAPPER_IMPLEMENTATION_MISMATCH",proof.get("wrapper_sha256")==sha(ROOT/"tools/start_witness_capture.ps1"))
    identity=summary.get("implementation",{})
    check("EXE_IMPLEMENTATION_MISMATCH",
          identity.get("kind")=="frozen_executable"
          and identity.get("sha256") in driver.ADDITIONAL_APPROVED_WITNESSES["frozen_executable"]
          and proof.get("exe_before_sha256")==identity.get("sha256")==proof.get("exe_after_sha256"))
    hashes=proof.get("files",{})
    check("RAW_FILE_HASH_BINDING",isinstance(hashes,dict) and set(hashes)==set(raw_names)
          and all(hashes.get(n)==before[str(directory/n)] for n in raw_names))
    check("UNEXPECTED_RECEIVER_STDERR",(directory/"stderr.bin").read_bytes()==b"")
    argv=proof.get("command_argv")
    valid_argv=False
    # Do not normalize supplied paths or accept a manual exit-code override.
    if isinstance(argv,list) and len(argv)==12 and all(isinstance(x,str) for x in argv):
        exe,log=PureWindowsPath(argv[0]),PureWindowsPath(argv[-1])
        expected_args=["--serve","--bind",summary.get("bind"),"--udp-port","49001",
                       "--tcp-port","49002","--seconds","300","--log",argv[-1]]
        valid_argv=(argv[1:]==expected_args and exe.is_absolute() and log.is_absolute()
                    and ".." not in exe.parts and ".." not in log.parts
                    and exe.name=="witness_receiver_v3.exe" and log.name=="receiver.jsonl"
                    and log.parent.name==directory.name and summary.get("requested_seconds")==300
                    and PureWindowsPath(identity.get("path",""))==exe
                    and summary.get("log")==str(log)
                    and summary.get("summary")==str(log)+".summary.json"
                    and sender.get("ports")=={"udp":49001,"tcp":49002})
    check("PROCESS_ARGUMENT_BINDING",valid_argv)
    created=[row for row in rows if row.get("kind")=="created"]
    check("RAW_CREATED_PROCESS_BINDING",len(created)==1 and created[0].get("argv")==argv
          and type(created[0].get("pid")) is int and created[0]["pid"]>0
          and created[0].get("log")==summary.get("log")
          and created[0].get("summary")==summary.get("summary"))
    check("PRODUCTION_GATE_OR_CERTIFICATE_CHANGED",proof.get("production_gate")=="CLOSED" and proof.get("certificate_written") is False
          and summary.get("production_gate")=="CLOSED" and summary.get("certificate_written") is False)
    result=inspect(sender_path,directory/raw_names[0],directory/raw_names[1],0 if not findings else None)
    result["findings"]=findings+result["findings"]
    if result["findings"]:result["status"]="NOT_ACCEPTED"
    result["process_receipt"]={"path":str(directory/"process-exit.json"),"sha256":before[str(directory/"process-exit.json")],
                               "scope":"Hash-bound local producer receipt; not remote authentication or sandbox acceptance"}
    after={str(path):sha(path) for path in paths}
    if before!=after:raise ValueError("Evidence changed during read-only inspection")
    result["files"]=before
    return result

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sender",required=True,type=Path)
    parser.add_argument("--capture-directory",required=True,type=Path)
    args=parser.parse_args(argv)
    try:
        result=inspect_capture(args.sender,args.capture_directory)
    except Exception as exc:
        result={"status":"NOT_ACCEPTED","findings":[{"code":"INVALID_OR_MISSING_CAPTURE","error_type":type(exc).__name__,"detail":str(exc)}],
                "production":"CLOSED","full_surface_accepted":False}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result["status"]=="READY_FOR_REGISTERED_RECONCILIATION" else 2

if __name__=="__main__":
    raise SystemExit(main())
