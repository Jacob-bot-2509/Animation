import subprocess,json,sys,datetime,hashlib,uuid
from pathlib import Path
p=Path(r'D:\Animation-Model-Training');d=p/'reviews/2026-10-06-exec-isolation-full-surface';o=Path(__file__).parent
results=[]
for mode,script in [('udp','probe_udp_external.py'),('exe','probe_exe_ipc_fs.py'),('ipc','probe_raw_ipc3.py')]:
    cmd=[str(p/'.venv/Scripts/python.exe'),'-X','utf8','-B',str(d/script),'--execute-native']
    print('START',mode,flush=True)
    cp=subprocess.run(cmd,cwd=p,capture_output=True,timeout=120)
    for name,data in [('stdout',cp.stdout),('stderr',cp.stderr)]:
        target=o/('native-'+mode+'.'+name+'.raw.txt')
        if target.exists():(o/(target.name+'.previous-'+uuid.uuid4().hex)).write_bytes(target.read_bytes())
        target.write_bytes(data)
    row={'mode':mode,'command':cmd,'rc':cp.returncode,'stdout_raw_sha256':hashlib.sha256(cp.stdout).hexdigest(),'stderr_raw_sha256':hashlib.sha256(cp.stderr).hexdigest()}
    try:
        summary=json.loads(cp.stdout);f=Path(summary['path']);raw=f.read_bytes();record=json.loads(raw)
        row.update(path=str(f),raw_sha256=hashlib.sha256(raw).hexdigest(),status=record['status'],transport_verified=record['transport_verified'],implementation_unchanged=record['implementation_unchanged'],error=record.get('error'),scoped_results=record['scoped_results'])
        row['expected_unverified_exit']=cp.returncode==3 and record['status']=='UNVERIFIED' and record['transport_verified'] is True and record['implementation_unchanged'] is True and not record.get('error')
    except Exception as exc:row['parse_error']=str(exc);row['expected_unverified_exit']=False
    results.append(row)
    (o/'native-bounded-validation.json').write_text(json.dumps({'checked_at':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'scope':'Only owned loopback, new project fixture/registry leaf, and live owned IPC object access. No clipboard/window/external receiver/render/train operations.','production_gate':'CLOSED','full_surface_accepted':False,'results':results},ensure_ascii=False,indent=2),encoding='utf-8')
    print('DONE',mode,json.dumps({'rc':cp.returncode,'transport_verified':row.get('transport_verified'),'expected_unverified_exit':row['expected_unverified_exit'],'error':row.get('error')},ensure_ascii=False),flush=True)
    if not row['expected_unverified_exit']:break
sys.exit(0 if len(results)==3 and all(x['expected_unverified_exit'] for x in results) else 1)