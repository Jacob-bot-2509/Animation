import os,_socket
s=_socket.socket(_socket.AF_INET,_socket.SOCK_STREAM)
try:
    s.connect(('127.0.0.1',int(os.environ['PROBE_PORT'])))
    print('CHILD_CONNECTED')
except OSError as e:
    print('CHILD_BLOCKED:'+str(e))
