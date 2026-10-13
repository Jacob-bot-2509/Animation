"""Explicit local TCP diagnostics, exact times; no witness or sandbox qualification."""
from __future__ import annotations
import argparse,ipaddress,json,socket,time
from fractions import Fraction

def validate_target(host,port):
    address=ipaddress.ip_address(host)
    if address.is_unspecified or address.is_multicast:raise ValueError("Specific unicast literal required")
    if type(port) is not int or not 1<=port<=65535:raise ValueError("Port must be integer 1..65535")
    return str(address),socket.AF_INET6 if address.version==6 else socket.AF_INET

def verdict(code):
    return {0:"LOCAL_CONNECT_COMPLETED",10061:"CONNECTION_REFUSED",
            10060:"TIMEOUT_UNCONFIRMED",10013:"OS_ACCESS_DENIED"}.get(code,"SOCKET_ERROR")

def probe(host,port,*,banner=False):
    host,family=validate_target(host,port)
    start=time.monotonic_ns()
    result={"target":[host,port],"receiver_delivery_verified":False,"qualification":"NOT_ESTABLISHED",
            "production":"CLOSED","native_acceptance":False}
    try:
        with socket.socket(family,socket.SOCK_STREAM) as sock:
            sock.settimeout(3 if banner else 5)
            code=sock.connect_ex((host,port));result.update(errno=code,outcome=verdict(code))
            if banner and code==0:
                sock.settimeout(2)
                try:
                    payload=sock.recv(64)
                    result.update(read_outcome="DATA" if payload else "EOF",first_bytes_hex=payload.hex())
                except TimeoutError:
                    result.update(read_outcome="TIMEOUT_UNCONFIRMED",first_bytes_hex=None)
    except OSError as exc:
        result.update(outcome="TIMEOUT_UNCONFIRMED" if isinstance(exc,TimeoutError) else "SOCKET_ERROR",
                      error_type=type(exc).__name__,detail=str(exc),errno=getattr(exc,"errno",None),
                      winerror=getattr(exc,"winerror",None))
    elapsed=time.monotonic_ns()-start
    result.update(elapsed_ns=elapsed,elapsed_ms_exact=str(Fraction(elapsed,1_000_000)))
    return result

def main(argv=None,*,banner=False):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("host",nargs="?")
    parser.add_argument("port",nargs="?",type=int)
    parser.add_argument("--execute",action="store_true")
    args=parser.parse_args(argv)
    if not args.execute:
        print(json.dumps({"status":"PLAN","network_execution":False,
                          "required":"--execute LITERAL_IP PORT","production":"CLOSED"}))
        return 3
    try:
        if args.host is None or args.port is None:raise ValueError("Explicit literal host and port required")
        host,family=validate_target(args.host,args.port)
        attempts=[]
        for number in range(2 if banner else 1):
            row=probe(host,args.port,banner=banner);row["attempt"]=number;attempts.append(row)
            if banner and number==0:time.sleep(3/10)
        print(json.dumps({"status":"DIAGNOSTIC_ONLY","attempts":attempts,
                          "qualification":"NOT_ESTABLISHED","production":"CLOSED","native_acceptance":False},ensure_ascii=False))
        return 2 if any(row["outcome"]=="SOCKET_ERROR" for row in attempts) else 0
    except (ValueError,OSError) as exc:
        print(json.dumps({"status":"FAILED","detail":str(exc),"production":"CLOSED","native_acceptance":False}))
        return 2
