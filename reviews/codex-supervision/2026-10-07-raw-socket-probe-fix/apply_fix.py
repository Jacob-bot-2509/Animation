import pathlib,hashlib
ROOT=pathlib.Path('.');OUT=ROOT/'reviews/codex-supervision/2026-10-07-raw-socket-probe-fix'
p=ROOT/'tools/sandbox_external_test_driver.py';before=(OUT/'before/tools/sandbox_external_test_driver.py').read_bytes()
assert p.read_bytes()==before,'Driver changed after ownership snapshot'
t=p.read_text(encoding='utf8')
old='''    try:
        with _socket.socket(family,_socket.SOCK_DGRAM if protocol=="udp" else _socket.SOCK_STREAM) as s:
            s.settimeout(4 if protocol=="udp" else 6)
            if protocol=="udp":s.sendto(nonce.encode("ascii"),(host,port))
            else:
                s.connect((host,port));s.sendall(nonce.encode("ascii"));s.shutdown(_socket.SHUT_WR)
        r[protocol]={"outcome":"sent" if protocol=="udp" else "completed"}
    except OSError as exc:
        code=getattr(exc,"winerror",None)
        outcome="os_denied" if code==10013 else "timeout" if isinstance(exc,TimeoutError) else "error"
        r[protocol]={"outcome":outcome,"winerror":code,"error_type":type(exc).__name__,"detail":str(exc)}
    r[protocol]["elapsed_ns"]=time.monotonic_ns()-started'''
new='''    s=None
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
    r[protocol]["elapsed_ns"]=time.monotonic_ns()-started'''
assert t.count(old)==1;t=t.replace(old,new);p.write_text(t,encoding='utf8')
p=ROOT/'tests/test_sandbox_external_driver.py'
assert p.read_bytes()==(OUT/'before/tests/test_sandbox_external_driver.py').read_bytes(),'Tests changed after snapshot'
t=p.read_text(encoding='utf8')
old='s=mock.MagicMock();s.__enter__.return_value=s;s.sendto.side_effect=error;s.connect.side_effect=error;sockets.append(s)'
new='s=mock.Mock(spec=["settimeout","sendto","connect","sendall","shutdown","close"]);s.sendto.side_effect=error;s.connect.side_effect=error;sockets.append(s)'
assert t.count(old)==1;t=t.replace(old,new)
needle='        return json.loads(output.getvalue())\n    def test_probe_classifies_only_actual_10013_as_os_denied'
replacement='        for raw_socket in sockets:\n            self.assertFalse(hasattr(raw_socket,"__enter__"))\n            raw_socket.close.assert_called_once_with()\n        return json.loads(output.getvalue())\n    def test_probe_classifies_only_actual_10013_as_os_denied'
assert needle in t;t=t.replace(needle,replacement)
newtests=r'''
    def test_probe_real_bare_sockets_ipv4_ipv6_loopback_delivery_and_close(self):
        import _socket
        self.assertFalse(hasattr(_socket.socket,"__enter__"))
        actual_factory=_socket.socket
        for family,host in ((socket.AF_INET,"127.0.0.1"),(socket.AF_INET6,"::1")):
            with self.subTest(family=family):
                with socket.socket(family,socket.SOCK_STREAM) as tcp, socket.socket(family,socket.SOCK_DGRAM) as udp:
                    tcp.bind((host,0));tcp.listen(1);tcp.settimeout(3)
                    udp.bind((host,0));udp.settimeout(3)
                    ports={"tcp":tcp.getsockname()[1],"udp":udp.getsockname()[1]}
                    nonces={p:{"sandbox":uuid.uuid4().hex} for p in ("tcp","udp")}
                    created=[]
                    def bare_factory(*args):
                        s=actual_factory(*args);created.append(s);return s
                    output=io.StringIO()
                    with mock.patch.object(_socket,"socket",side_effect=bare_factory),contextlib.redirect_stdout(output):
                        exec(d.probe_source(host,ports,nonces,["tcp","udp"]),{})
                    result=json.loads(output.getvalue())
                    self.assertEqual(result["tcp"]["outcome"],"completed")
                    self.assertEqual(result["udp"]["outcome"],"sent")
                    packet,_=udp.recvfrom(64)
                    self.assertEqual(packet,nonces["udp"]["sandbox"].encode("ascii"))
                    conn,_=tcp.accept()
                    with conn:
                        conn.settimeout(3);parts=[]
                        while True:
                            part=conn.recv(64)
                            if not part:break
                            parts.append(part)
                    self.assertEqual(b"".join(parts),nonces["tcp"]["sandbox"].encode("ascii"))
                    self.assertEqual(len(created),2)
                    self.assertTrue(all(s.fileno()==-1 for s in created))
    def test_probe_creation_denied_continues_to_next_protocol(self):
        denied=PermissionError("constructor denied");denied.winerror=10013
        raw=mock.Mock(spec=["settimeout","sendto","connect","sendall","shutdown","close"])
        fake=types.SimpleNamespace(AF_INET=2,AF_INET6=23,SOCK_DGRAM=2,SOCK_STREAM=1,SHUT_WR=1,
            socket=mock.Mock(side_effect=[denied,raw]))
        out=io.StringIO()
        with mock.patch.dict(sys.modules,{"_socket":fake}),contextlib.redirect_stdout(out):
            exec(d.probe_source("192.0.2.10",{"tcp":49002,"udp":49001},
                {p:{"sandbox":uuid.uuid4().hex} for p in ("tcp","udp")},["udp","tcp"]),{})
        result=json.loads(out.getvalue())
        self.assertEqual(result["udp"]["outcome"],"os_denied")
        self.assertEqual(result["udp"]["winerror"],10013)
        self.assertEqual(result["tcp"]["outcome"],"completed")
        raw.close.assert_called_once_with()
    def test_probe_timeout_setup_failure_still_closes(self):
        raw=mock.Mock(spec=["settimeout","sendto","connect","sendall","shutdown","close"])
        raw.settimeout.side_effect=OSError("timeout setup failed")
        fake=types.SimpleNamespace(AF_INET=2,AF_INET6=23,SOCK_DGRAM=2,SOCK_STREAM=1,socket=mock.Mock(return_value=raw))
        out=io.StringIO()
        with mock.patch.dict(sys.modules,{"_socket":fake}),contextlib.redirect_stdout(out):
            exec(d.probe_source("192.0.2.10",{"udp":49001},{"udp":{"sandbox":uuid.uuid4().hex}},["udp"]),{})
        self.assertEqual(json.loads(out.getvalue())["udp"]["outcome"],"error")
        raw.sendto.assert_not_called();raw.close.assert_called_once_with()
    def test_probe_close_denied_is_error_not_network_isolation(self):
        raw=mock.Mock(spec=["settimeout","sendto","connect","sendall","shutdown","close"])
        denied=PermissionError("close denied");denied.winerror=10013;raw.close.side_effect=denied
        fake=types.SimpleNamespace(AF_INET=2,AF_INET6=23,SOCK_DGRAM=2,SOCK_STREAM=1,socket=mock.Mock(return_value=raw))
        out=io.StringIO()
        with mock.patch.dict(sys.modules,{"_socket":fake}),contextlib.redirect_stdout(out):
            exec(d.probe_source("192.0.2.10",{"udp":49001},{"udp":{"sandbox":uuid.uuid4().hex}},["udp"]),{})
        result=json.loads(out.getvalue())["udp"]
        self.assertEqual(result["outcome"],"error")
        self.assertEqual(result["close_error"]["winerror"],10013)
        raw.close.assert_called_once_with()
'''
assert '\nif __name__=="__main__":unittest.main()' in t
t=t.replace('\nif __name__=="__main__":unittest.main()',newtests+'\nif __name__=="__main__":unittest.main()')
p.write_text(t,encoding='utf8')
print(hashlib.sha256((ROOT/'tools/sandbox_external_test_driver.py').read_bytes()).hexdigest())
