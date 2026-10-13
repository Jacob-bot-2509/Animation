"""Reviewed, bounded joint probes of the exact production transport.
No training starts; certificate issuance requires separate independent recomputation.
"""
import argparse,ctypes,json,sys,time,socket,select,threading,uuid,subprocess,hashlib
from ctypes import wintypes
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from animtrain.sandbox_execution import run_code,render_scene,digest,BOUND_FILES
OUT=ROOT/'reviews/codex-supervision/2026-10-05-three-gates'


def dead(pid):
    k=ctypes.WinDLL('kernel32',use_last_error=True)
    k.OpenProcess.argtypes=[wintypes.DWORD,wintypes.BOOL,wintypes.DWORD];k.OpenProcess.restype=wintypes.HANDLE
    k.GetExitCodeProcess.argtypes=[wintypes.HANDLE,ctypes.POINTER(wintypes.DWORD)];k.GetExitCodeProcess.restype=wintypes.BOOL
    k.CloseHandle.argtypes=[wintypes.HANDLE]
    h=k.OpenProcess(0x1000,False,pid)
    if not h:return {'dead':ctypes.get_last_error()==87,'error':ctypes.get_last_error()}
    try:
        rc=wintypes.DWORD()
        if not k.GetExitCodeProcess(h,ctypes.byref(rc)):raise ctypes.WinError(ctypes.get_last_error())
        return {'dead':rc.value!=259,'exit_code':rc.value}
    finally:k.CloseHandle(h)


def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--only-local',action='store_true')
    parser.add_argument('--ipv4-evidence',choices=('joint','direct'),default='joint')
    parser.add_argument('--plan',action='store_true',help='Describe policy without executing probes')
    args=parser.parse_args(argv)
    from animtrain.full_surface_evidence import IPV4_JOINT_POLICY
    if args.plan:
        print(json.dumps({'ipv4_evidence':args.ipv4_evidence,
            'acceptance_basis':IPV4_JOINT_POLICY if args.ipv4_evidence=='joint' else 'direct',
            'public_ipv4_node_required':args.ipv4_evidence=='direct',
            'required_joint_components':['lan_ipv4','external_ipv6','local_ipv4'],
            'production_gate':'CLOSED','evidence_collected':False}))
        return
    ONLY_LOCAL=args.only_local
    REPORT=OUT/('production-joint-v3-'+uuid.uuid4().hex+'.json')
    if REPORT.exists():raise ValueError('Preserve previous raw evidence')
    report={'schema':'production-joint-raw-v1','implementation_sha256':{n:digest(ROOT/n) for n in BOUND_FILES},
            'probe_sha256':digest(Path(__file__)),'records':{},'production_gate':'CLOSED',
            'ipv4_evidence':args.ipv4_evidence,'ipv4_joint_evidence_collected':False}
    def save(name,result):
        report['records'][name]=result
        REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(name,'captured',flush=True)
    for name,body in ([] if ONLY_LOCAL else [('render_formula','self.add(MathTex(r"f\'(x)=2x"))'),('render_chinese','self.add(Text("切线方程",font="Microsoft YaHei",font_size=32))')]):
        save(name,render_scene('from manim import *\nclass ConceptScene(Scene):\n    def construct(self):\n        '+body+'\n        self.wait(1/5)\n'))
    if not ONLY_LOCAL:
        private=OUT/('joint-private-sentinel-'+uuid.uuid4().hex+'.txt');private.write_text(uuid.uuid4().hex,encoding='utf-8')
        prior=Path(report['records']['render_formula']['transport']['work'])
        attempts=[('file_read_outside','read',str(private)),('file_write_outside','write',str(OUT/('joint-outside-write-'+uuid.uuid4().hex+'.txt'))),
                  ('file_write_runtime','write',str(ROOT/'.sandbox-runtime/miktex-real'/('joint-write-'+uuid.uuid4().hex+'.txt'))),
                  ('cross_run_write','write',str(prior/'cross-run-marker.txt')),
                  ('cross_run_cache_write','write',str(prior/'state/config/cross-run-marker.txt'))]
        before=digest(private)
        code='import json,pathlib\nr={}\nfor name,kind,path in '+repr(attempts)+':\n    try:\n        p=pathlib.Path(path)\n        if kind=="read":p.read_bytes()\n        else:p.write_text("bounded-probe",encoding="utf-8")\n        r[name]="allowed"\n    except PermissionError:r[name]="denied"\n    except Exception as e:r[name]=repr(e)\nprint(json.dumps(r),flush=True)\n'
        cp=run_code(code,mode='probe');save('files',{'transport':cp,'attempts':attempts,'private_before_sha256':before,'private_after_sha256':digest(private),'markers_absent':{name:not Path(path).exists() for name,kind,path in attempts if kind=='write'}})
    # Four listeners share one job/window, ordinary controls use exact same sockets.
    sockets={};packets={};stop=threading.Event()
    for name,family,kind,host in [('tcp_loopback_v4',socket.AF_INET,socket.SOCK_STREAM,'127.0.0.1'),('tcp_loopback_v6',socket.AF_INET6,socket.SOCK_STREAM,'::1'),('udp_loopback_v4',socket.AF_INET,socket.SOCK_DGRAM,'127.0.0.1'),('udp_loopback_v6',socket.AF_INET6,socket.SOCK_DGRAM,'::1')]:
        s=socket.socket(family,kind);s.bind((host,0));s.setblocking(False)
        if kind==socket.SOCK_STREAM:s.listen()
        sockets[name]=(s,int(family),int(kind),s.getsockname());packets[name]=[]
    def receive():
        while not stop.is_set():
            readable,_,_=select.select([x[0] for x in sockets.values()],[],[],1/10)
            for ready in readable:
                name=next(n for n,x in sockets.items() if x[0] is ready)
                if sockets[name][2]==int(socket.SOCK_STREAM):
                    conn,_=ready.accept()
                    with conn:
                        conn.settimeout(3)
                        payload=b""
                        while len(payload)<32:
                            part=conn.recv(32-len(payload))
                            if not part:break
                            payload+=part
                else:payload,_=ready.recvfrom(256)
                packets[name].append({'hex':payload.hex(),'at':time.time()})
    thread=threading.Thread(target=receive,daemon=True);thread.start()
    nonces={phase:{n:uuid.uuid4().hex for n in sockets} for phase in ('before','sandbox','after')}
    def ordinary(phase):
        result={}
        for name,(_,fam,kind,ep) in sockets.items():
            with socket.socket(fam,kind) as s:
                s.settimeout(3);s.connect(ep);s.send(nonces[phase][name].encode())
                result[name]={'outcome':'sent','nonce':nonces[phase][name]}
        return result
    before=ordinary('before');time.sleep(1/5)
    spec=[(n,f,k,ep,nonces['sandbox'][n]) for n,(_,f,k,ep) in sockets.items()]
    code='import _socket,json,time\nr={}\nfor name,fam,kind,ep,nonce in '+repr(spec)+':\n    s=_socket.socket(fam,kind);s.settimeout(2);started=time.monotonic()\n    try:\n        s.connect(ep);s.send(nonce.encode());r[name]={"outcome":"sent"}\n    except OSError as e:r[name]={"outcome":"error","winerror":getattr(e,"winerror",None),"error_type":type(e).__name__,"error_detail":str(e),"elapsed_ms":round((time.monotonic()-started)*1000)}\n    finally:s.close()\nprint(json.dumps(r),flush=True)\n'
    cp=run_code(code,mode='probe');time.sleep(20);after=ordinary('after');time.sleep(1/5)
    stop.set();thread.join(timeout=2)
    for s,_,_,_ in sockets.values():s.close()
    save('local_network',{'transport':cp,'before':before,'after':after,'nonces':nonces,'packets':packets,'observation_seconds':20,'receiver_complete':not thread.is_alive()})
    if ONLY_LOCAL:
        report['complete']=True
        report['implementation_unchanged']=report['implementation_sha256']=={n:digest(ROOT/n) for n in BOUND_FILES}
        REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        return
    endpoints=[('tcp_external_v6',int(socket.AF_INET6),('2606:4700:4700::1111',443,0,0))]
    if args.ipv4_evidence=='direct':
        endpoints.insert(0,('tcp_external_v4',int(socket.AF_INET),('1.1.1.1',443)))
    def external_controls():
        result={}
        for name,fam,ep in endpoints:
            with socket.socket(fam,socket.SOCK_STREAM) as s:
                s.settimeout(3)
                try:s.connect(ep);result[name]='connected'
                except OSError as e:result[name]=repr(e)
        return result
    before=external_controls()
    code='import _socket,json\nr={}\nfor name,fam,ep in '+repr(endpoints)+':\n    s=_socket.socket(fam,_socket.SOCK_STREAM);s.settimeout(3)\n    try:s.connect(ep);r[name]={"outcome":"connected"}\n    except OSError as e:r[name]={"outcome":"error","winerror":getattr(e,"winerror",None)}\n    finally:s.close()\nprint(json.dumps(r),flush=True)\n'
    cp=run_code(code,mode='probe');save('external_network',{'transport':cp,'before':before,'after':external_controls(),'endpoints':endpoints})
    for kind in ('root_exit_tree','timeout_tree'):
        source='import subprocess,sys,json,time\np=subprocess.Popen([sys.executable,"-I","-B","-c","import time;time.sleep(60)"])\nprint(json.dumps({"child_pid":p.pid}),flush=True)\n'+('time.sleep(60)\n' if kind=='timeout_tree' else '')
        try:
            cp=run_code(source,mode='probe',timeout_ms=5000)
            child=json.loads(cp['stdout'])['child_pid'];record={'transport':cp,'timed_out':False,'child_state':dead(child)}
        except subprocess.TimeoutExpired as exc:
            child=json.loads(exc.output.decode())['child_pid'];record={'timed_out':True,'parent_evidence':getattr(exc,'parent_evidence',None),'work':getattr(exc,'work',None),'stdout':exc.output.decode(),'child_state':dead(child)}
        save(kind,record)
    memory_source='import json,sys\nchunks=[]\ntry:\n    for i in range(36):chunks.append(bytearray(64*1024*1024))\nexcept MemoryError:\n    print(json.dumps({"memory_denied":True,"allocated_chunks":len(chunks),"chunk_bytes":64*1024*1024}),flush=True)\n    sys.exit(17)\nprint(json.dumps({"memory_denied":False}),flush=True)\n'
    save('memory_limit',{'transport':run_code(memory_source,mode='probe',timeout_ms=30000)})
    report['complete']=True;report['implementation_unchanged']=report['implementation_sha256']=={n:digest(ROOT/n) for n in BOUND_FILES}
    REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print('report',REPORT,flush=True)
if __name__=='__main__':main()
