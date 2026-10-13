"""Local loopback protocol reproduction only; never native sandbox acceptance."""
from pathlib import Path
import concurrent.futures,importlib.util,json,queue,socket,uuid,hashlib,base64
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent

def load(name,file):
    spec=importlib.util.spec_from_file_location(name,ROOT/file)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

driver=load("local_registered_sender","tools/sandbox_external_test_driver.py")
receiver=load("local_registered_receiver","tools/sandbox_witness_receiver.py")
sha=lambda q:hashlib.sha256(q.read_bytes()).hexdigest()
before={str(q.relative_to(ROOT)):sha(q)for q in [ROOT/"tools/sandbox_external_test_driver.py",ROOT/"tools/sandbox_witness_receiver.py"]}
cases=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    futures=[]
    for bind,family,label in [("127.0.0.1",socket.AF_INET,"ipv4"),("::1",socket.AF_INET6,"ipv6")]:
        ready=queue.Queue()
        log=OUT/(label+"-loopback.jsonl")
        future=pool.submit(receiver.run,bind,0,0,20,log,ready=ready.put)
        endpoints=ready.get(timeout=10)
        nonces={protocol:{phase:uuid.uuid4().hex for phase in ("before","after")}for protocol in ("tcp","udp")}
        sends={}
        for phase in ("before","after"):
            for protocol in ("tcp","udp"):
                sends[phase+"_"+protocol]=driver.send(tuple(endpoints[protocol]),nonces[protocol][phase].encode("ascii"),family,protocol)
                assert sends[phase+"_"+protocol]["outcome"]==("completed"if protocol=="tcp"else"sent")
                assert sends[phase+"_"+protocol]["receiver_delivery_verified"]is False
        # A connection without nonce is also recorded; it is invalid for acceptance.
        with socket.socket(family,socket.SOCK_STREAM)as conn:
            conn.settimeout(3);conn.connect(tuple(endpoints["tcp"]));conn.shutdown(socket.SHUT_WR)
        futures.append((label,log,future,nonces,sends))
    for label,log,future,nonces,sends in futures:
        rc=future.result(timeout=30)
        summary=json.loads(log.with_suffix(log.suffix+".summary.json").read_bytes())
        rows=[json.loads(row)for row in log.read_bytes().splitlines()if row.strip()]
        payloads=[row for row in rows if row["kind"]=="payload"]
        expected={protocol:[nonces[protocol][phase]for phase in ("before","after")]for protocol in ("tcp","udp")}
        observed={protocol:[row["nonce"]for row in payloads if row["protocol"]==protocol and row["exact_nonce"]]for protocol in ("tcp","udp")}
        empty=[row for row in payloads if row["protocol"]=="tcp"and row["bytes"]==0]
        assert observed==expected
        assert len(payloads)==5 and len(empty)==1 and empty[0]["exact_nonce"]is False
        assert rc==0 and summary["records"]==5 and summary["receiver_complete"]is True
        assert sha(log)==summary["log_sha256"]
        cases.append({"family":label,"rc":rc,"expected_controls":expected,"observed_controls":observed,"empty_connection_recorded":True,"records":len(payloads),"sends":sends,"log_sha256":sha(log),"scope":"LOCAL_HOST_LOOPBACK_PROTOCOL_ONLY"})
assert before=={name:sha(ROOT/name)for name in before}
result={"status":"PASS_LOCAL_LOOPBACK_PROTOCOL_ONLY","cases":cases,"bindings":before,"original_sources_unchanged":True,"native_sandbox_accepted":False,"full_surface_accepted":False,"production":"CLOSED"}
(OUT/"protocol-loopback-result.json").write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"status":result["status"],"cases":len(cases),"controls_per_family":4,"empty_tcp_rows_per_family":1,"production":"CLOSED"}))
