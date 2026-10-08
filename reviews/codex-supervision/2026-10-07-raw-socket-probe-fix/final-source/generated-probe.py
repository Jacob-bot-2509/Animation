SPEC=[('tcp', '127.0.0.1', 49002, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'), ('udp', '127.0.0.1', 49001, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')]

import json,_socket,time
r={}
for protocol,host,port,nonce in SPEC:
    family=_socket.AF_INET6 if ":" in host else _socket.AF_INET
    started=time.monotonic_ns()
    s=None
    try:
        # Bare _socket.socket has no context-manager protocol.
        s=_socket.socket(family,_socket.SOCK_DGRAM if protocol=="udp" else _socket.SOCK_STREAM)
        s.settimeout(4 if protocol=="udp" else 6)
        if protocol=="udp":s.sendto(nonce.encode("ascii"),(host,port))
        else:
            s.connect((host,port));s.sendall(nonce.encode("ascii"));s.shutdown(_socket.SHUT_WR)
        r[protocol]={"outcome":"sent" if protocol=="udp" else "completed"}
    except OSError as exc:
        code=getattr(exc,"winerror",None)
        outcome="os_denied" if code==10013 else "timeout" if isinstance(exc,TimeoutError) else "error"
        r[protocol]={"outcome":outcome,"winerror":code,"error_type":type(exc).__name__,"detail":str(exc)}
    finally:
        if s is not None:
            try:s.close()
            except OSError as exc:
                # Cleanup failure is not evidence of network isolation.
                r[protocol]["outcome"]="error"
                r[protocol]["close_error"]={"error_type":type(exc).__name__,
                    "winerror":getattr(exc,"winerror",None),"detail":str(exc)}
    r[protocol]["elapsed_ns"]=time.monotonic_ns()-started
print(json.dumps(r),flush=True)
