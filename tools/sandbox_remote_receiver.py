"""Controlled remote TCP/UDP/HTTP nonce receiver; default is plan only."""
import argparse,hashlib,ipaddress,json,os,re,socket,time,uuid
from pathlib import Path
def run(bind,port,protocol,seconds,output):
    address=ipaddress.ip_address(bind);family=socket.AF_INET6 if address.version==6 else socket.AF_INET
    if not 1024<=port<=65535 or not 20<=seconds<=900:raise ValueError("High port and 20..900 second window required")
    output=Path(output).absolute();output.mkdir(parents=True,exist_ok=True)
    tag=uuid.uuid4().hex;log=output/("receiver-"+tag+".jsonl");summary=output/("receiver-"+tag+".summary.json")
    source=Path(__file__);source_hash=hashlib.sha256(source.read_bytes()).hexdigest()
    records=[];errors=[];started=time.monotonic_ns()
    sock=socket.socket(family,socket.SOCK_DGRAM if protocol=="udp" else socket.SOCK_STREAM)
    sock.settimeout(1/5)
    try:
        sock.bind((bind,port))
        if protocol!="udp":sock.listen(16)
        endpoint=sock.getsockname();deadline=started+seconds*1_000_000_000
        print(json.dumps({"status":"LISTENING","endpoint":endpoint,"protocol":protocol,"run_id":tag,"log":str(log),"source_sha256":source_hash}),flush=True)
        with log.open("x",encoding="utf-8",newline="\n") as out:
            while time.monotonic_ns()<deadline:
                try:
                    if protocol=="udp":payload,peer=sock.recvfrom(65535)
                    else:
                        conn,peer=sock.accept()
                        with conn:
                            conn.settimeout(2);payload=b""
                            while len(payload)<8192:
                                block=conn.recv(8192-len(payload))
                                if not block:break
                                payload+=block
                                if protocol=="tcp" and len(payload)>=32:break
                                if protocol=="http" and b"\r\n\r\n" in payload:break
                            if protocol=="http":
                                parts=payload.split(b"\r\n",1)[0].split(b" ")
                                nonce=parts[1].removeprefix(b"/") if len(parts)==3 and parts[0]==b"GET" else b""
                                conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Length: 2\r\nConnection: close\r\n\r\nok")
                            else:nonce=payload
                    if protocol=="udp":nonce=payload
                    valid=bool(re.fullmatch(b"[0-9a-f]{32}",nonce))
                    record={"seq":len(records),"at_monotonic_ns":time.monotonic_ns(),"at_utc_ns":time.time_ns(),"peer":peer,
                            "endpoint":endpoint,"protocol":protocol,"payload_hex":payload.hex(),"nonce":nonce.decode("ascii") if valid else None,"exact_nonce":valid}
                    records.append(record);out.write(json.dumps(record)+"\n");out.flush()
                except TimeoutError:continue
                except Exception as exc:errors.append({"type":type(exc).__name__,"detail":str(exc)});break
    finally:sock.close()
    result={"schema":"controlled-nonce-receiver-v1","run_id":tag,"bind":bind,"port":port,"protocol":protocol,
            "started_monotonic_ns":started,"finished_monotonic_ns":time.monotonic_ns(),"errors":errors,"receiver_complete":not errors,
            "source_sha256":source_hash,"source_unchanged":hashlib.sha256(source.read_bytes()).hexdigest()==source_hash,
            "log":str(log),"log_sha256":hashlib.sha256(log.read_bytes()).hexdigest() if log.exists() else None,"records":len(records),
            "certificate_written":False}
    with summary.open("x",encoding="utf-8",newline="\n") as out:json.dump(result,out,indent=2);out.write("\n")
    print(json.dumps(result),flush=True)
    return 0 if not errors and result["source_unchanged"] else 2
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("--serve",action="store_true")
    p.add_argument("--bind");p.add_argument("--port",type=int,default=39443);p.add_argument("--protocol",choices=("tcp","udp","http"),default="udp")
    p.add_argument("--seconds",type=int,default=300);p.add_argument("--output",default="receiver-evidence")
    a=p.parse_args()
    if not a.serve:print("PLAN ONLY: explicit --serve --bind ADDRESS required; no socket opened");return 3
    if a.bind is None:p.error("--bind literal receiver address is required")
    return run(a.bind,a.port,a.protocol,a.seconds,a.output)
if __name__=="__main__":raise SystemExit(main())
