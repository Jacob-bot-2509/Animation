
import json,_socket,time
r={}
ep_udp=('192.168.1.83',49001)
ep_tcp=('192.168.1.83',49002)
nonce_udp=b'd3279f64cf2846919782cd3188c4f494'
nonce_tcp=b'0fcea69992c549daab64034d0452a910'
fam=_socket.AF_INET6 if ":" in '192.168.1.83' else _socket.AF_INET
s=_socket.socket(fam,_socket.SOCK_DGRAM);s.settimeout(3)
try:
 s.sendto(nonce_udp,ep_udp);r["udp"]={"outcome":"sent"}
except OSError as e:r["udp"]={"outcome":"denied","winerror":getattr(e,"winerror",None),"err":type(e).__name__}
finally:s.close()
s=_socket.socket(fam,_socket.SOCK_STREAM);s.settimeout(6)
try:
 s.connect(ep_tcp);s.sendall(nonce_tcp);r["tcp"]={"outcome":"connected"}
except OSError as e:r["tcp"]={"outcome":"denied","winerror":getattr(e,"winerror",None),"err":type(e).__name__}
finally:s.close()
print(json.dumps(r),flush=True)
