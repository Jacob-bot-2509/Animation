"""Read-only witness intake diagnostics. Never modifies evidence or issues acceptance."""
from pathlib import Path
import argparse,hashlib,ipaddress,json,re,importlib.util
ROOT=Path(__file__).resolve().parents[3]
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
    expected=driver.APPROVED_WITNESSES.get(summary.get("implementation",{}).get("kind"))
    supplied=summary.get("implementation",{}).get("sha256")
    check("APPROVED_IMPLEMENTATION_HASH_MISMATCH",supplied==expected,{"expected":expected,"actual":supplied,"actual_hex_length":len(supplied)if isinstance(supplied,str)else None})
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
        if r.get("kind")!="created" and valid:
            check("RAW_EVENT_OUTSIDE_SUMMARY_TIME_WINDOW",type(mono)is int and start<=mono<=end,{"row_sequence":r.get("seq"),"kind":r.get("kind"),"monotonic_ns":mono})
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
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sender",type=Path,required=True);ap.add_argument("--receiver-log",type=Path,required=True);ap.add_argument("--receiver-summary",type=Path,required=True);ap.add_argument("--receiver-rc",type=int)
    a=ap.parse_args()
    try:
        result=inspect(a.sender,a.receiver_log,a.receiver_summary,a.receiver_rc)
    except Exception as exc:
        result={"status":"NOT_ACCEPTED","findings":[{"code":"UNREADABLE_OR_INVALID_INPUT","error_type":type(exc).__name__,"detail":str(exc)}],"production":"CLOSED","full_surface_accepted":False}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 2 if result["status"]=="NOT_ACCEPTED"else 0
if __name__=="__main__":raise SystemExit(main())
