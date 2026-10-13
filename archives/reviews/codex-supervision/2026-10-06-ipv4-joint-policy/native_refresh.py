import hashlib,json,subprocess,time
from pathlib import Path
from datetime import datetime,timezone,timedelta
root=Path(r'D:\Animation-Model-Training');out=root/'reviews/codex-supervision/2026-10-06-ipv4-joint-policy'
command=[str(root/'.venv/Scripts/python.exe'),'-X','utf8','-B',str(root/'tools/sandbox_surface_acceptance.py'),'--execute-native']
started=time.monotonic_ns()
with (out/'native.stdout.txt').open('xb') as stdout,(out/'native.stderr.txt').open('xb') as stderr:
    cp=subprocess.run(command,cwd=root,stdout=stdout,stderr=stderr)
receipt={'captured_at':datetime.now(timezone(timedelta(hours=8))).isoformat(),'command':command,
    'rc':cp.returncode,'elapsed_ns':time.monotonic_ns()-started,
    'scope':'Fresh registered local fixtures only; no external/LAN joint evidence synthesized'}
with (out/'native-driver-receipt.json').open('x',encoding='utf-8') as f:json.dump(receipt,f,indent=2)
print(json.dumps(receipt));print((out/'native.stdout.txt').read_text(encoding='utf-8'));print((out/'native.stderr.txt').read_text(encoding='utf-8'))
