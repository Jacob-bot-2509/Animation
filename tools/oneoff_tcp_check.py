"""One-off TCP reachability check to a candidate witness (diagnostic only)."""
import socket, sys, time
host, port = sys.argv[1], int(sys.argv[2])
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
t = time.monotonic()
code = s.connect_ex((host, port))
el = (time.monotonic() - t) * 1000
s.close()
print({"target": f"{host}:{port}", "errno": code, "elapsed_ms": round(el, 1),
       "note": "0=connected 10061=refused(path alive) 10060=timeout(blocked/unreachable)"})
