import json,_socket
r={}
for name,fam,ep in [
 ('udp_lan_v4',_socket.AF_INET,('28.0.0.1',59649)),
 ('udp_external_v4',_socket.AF_INET,('8.8.8.8',53)),
 ('udp_external_v6',_socket.AF_INET6,('2606:4700:4700::1111',53,0,0))]:
 s=_socket.socket(fam,_socket.SOCK_DGRAM)
 try:
  s.sendto(b'probe-lan-c4d979f5-f8be-48',fam==_socket.AF_INET and ep or ep[:2]);r[name]={'outcome':'sent'}
 except OSError as e:r[name]={'outcome':'denied','winerror':getattr(e,'winerror',None),'err':e.__class__.__name__}
 finally:s.close()
try:
 _socket.getaddrinfo('example.com',80);r['dns_os']={'outcome':'resolved'}
except OSError as e:r['dns_os']={'outcome':'failed','errno':getattr(e,'errno',None),'err':e.__class__.__name__}
print(json.dumps(r),flush=True)
