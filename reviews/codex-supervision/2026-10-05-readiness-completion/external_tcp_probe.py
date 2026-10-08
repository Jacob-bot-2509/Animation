from pathlib import Path
import sys,json,hashlib,inspect,subprocess,uuid,os
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'src'))
from animtrain import appcontainer as ac,network_isolation as net
OUT=Path(__file__).resolve().parent
BASE=ROOT/'reviews/2026-10-04-acceptance-support/file-evidence/file-accept-results-487341961b6c.json'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run():
 b=json.loads(BASE.read_text(encoding='utf-8'));runtime=Path(b['runtime']);work=Path(b['work'])/('external-'+uuid.uuid4().hex[:12]);work.mkdir()
 pth=runtime.parent/'python313._pth';before={str(p):digest(p) for p in [runtime,runtime.parent/'python313.dll',runtime.parent/'Lib/socket.py',runtime.parent/'DLLs/_socket.pyd',pth]}
 assert set(pth.read_text().splitlines()) <= {'Lib','DLLs','.'}
 source=inspect.getsource(net.token_identity)+r"""
import json,socket,sys,hashlib
host=sys.argv[1];port=int(sys.argv[2]);af=socket.AF_INET6 if ':' in host else socket.AF_INET
r={'host':host,'port':port,'token':token_identity(),'connected':False,'winerror':None,'site_absent':'site' not in sys.modules and 'sitecustomize' not in sys.modules,'socket_file':socket.__file__,'executable':sys.executable,'script_sha256':hashlib.sha256(open(__file__,'rb').read()).hexdigest(),'runtime_sha256':hashlib.sha256(open(sys.executable,'rb').read()).hexdigest()}
try:
 with socket.socket(af,socket.SOCK_STREAM) as s:
  s.settimeout(6);s.connect((host,port));r['connected']=True
except OSError as ex:r.update(winerror=getattr(ex,'winerror',None),error=repr(ex))
print(json.dumps(r))
"""
 client=work/'external_client.py';client.write_text(source,encoding='utf-8');sha=digest(client);env=dict(b['sandbox_env']);env.update(TEMP=str(work),TMP=str(work));sid=ac._sid_sddl(ac.appcontainer_sid())
 report={'scope':'Only TCP connect to listed public endpoints during this run; no payload sent, no UDP/DNS/complete production isolation claim','production_gate':'CLOSED','source_sha256':digest(Path(__file__)),'runtime_manifest':before,'cases':[],'state':'RUNNING'}
 for host in ['1.1.1.1','1.0.0.1','2606:4700:4700::1111','2606:4700:4700::1001']:
  row={'host':host,'port':443,'clients':{},'policy_before':net.read_loopback_exemptions()}
  for side in ['before','sandbox','after']:
   cmd=[str(runtime),'-X','utf8',str(client),host,'443']
   try:
    cp=ac.run_appcontainer(cmd,cwd=work,env=env,allowed_dirs=[],timeout_ms=12000) if side=='sandbox' else subprocess.run(cmd,cwd=work,env=env,capture_output=True,timeout=12)
    row['clients'][side]={'rc':cp.returncode,'command':cmd,'data':json.loads(cp.stdout),'stderr':cp.stderr.decode('utf-8','replace')}
   except Exception as ex:row['clients'][side]={'error':repr(ex)}
  row['policy_after']=net.read_loopback_exemptions();cs=row['clients'];sb=cs['sandbox'].get('data',{});token=sb.get('token',{});integrity=all(c.get('rc')==0 and c.get('data',{}).get('script_sha256')==sha and c.get('data',{}).get('runtime_sha256')==before[str(runtime)] and c.get('data',{}).get('site_absent') is True and os.path.normcase(c.get('data',{}).get('socket_file',''))==os.path.normcase(str(runtime.parent/'Lib/socket.py')) for c in cs.values())
  controls=all(cs[s].get('data',{}).get('connected') is True for s in ['before','after']);identity=token.get('api_ok') is True and token.get('is_appcontainer') is True and token.get('capability_count')==0 and token.get('sid')==sid
  row.update(integrity=integrity,controls_connected=controls,identity_valid=identity,verdict='FAIL' if sb.get('connected') is True else ('PASS_TESTED_EXTERNAL_TCP' if integrity and controls and identity and sb.get('winerror')==10013 else 'UNVERIFIED'))
  report['cases'].append(row);(OUT/'external-tcp-results.json').write_text(json.dumps(report,indent=2),encoding='utf-8');print(host,row['verdict'],flush=True)
 report.update(state='COMPLETE',runtime_unchanged=all(digest(Path(p))==h for p,h in before.items()));report['overall']='FAIL' if any(r['verdict']=='FAIL' for r in report['cases']) else ('PASS_TESTED_EXTERNAL_TCP' if all(r['verdict']=='PASS_TESTED_EXTERNAL_TCP' for r in report['cases']) and report['runtime_unchanged'] else 'UNVERIFIED')
 (OUT/'external-tcp-results.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
if __name__=='__main__':run()
