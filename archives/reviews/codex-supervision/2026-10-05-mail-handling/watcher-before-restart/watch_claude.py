"""Read-only Claude start/change observer; records events, never reviews or executes code."""
from pathlib import Path
import os,json,hashlib,subprocess,time,datetime,msvcrt
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
if ROOT.name!='Animation-Model-Training' or not OUT.is_relative_to(ROOT):raise RuntimeError('Unexpected project path')
lock=(OUT/'watch.lock').open('a+b');lock.seek(0);lock.write(b'1');lock.flush();lock.seek(0)
try:msvcrt.locking(lock.fileno(),msvcrt.LK_NBLCK,1)
except OSError:raise SystemExit('Watcher already running')
def now():return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
def write(name,obj):
 p=OUT/name;tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8');tmp.replace(p)
def event(kind,detail):
 with (OUT/'events.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps({'time':now(),'kind':kind,'detail':detail},ensure_ascii=False)+'\n')
PS=r"""$OutputEncoding=[System.Text.UTF8Encoding]::new($false);[Console]::OutputEncoding=[System.Text.UTF8Encoding]::new($false);$items=Get-CimInstance Win32_Process;$ids=[System.Collections.Generic.HashSet[uint32]]::new();foreach($p in @($items | Where-Object {$_.Name -eq 'claude.exe'})){[void]$ids.Add([uint32]$p.ProcessId)};do{$added=$false;foreach($p in $items){if($ids.Contains([uint32]$p.ParentProcessId) -and -not $ids.Contains([uint32]$p.ProcessId)){[void]$ids.Add([uint32]$p.ProcessId);$added=$true}}}while($added);$items | Where-Object {$ids.Contains([uint32]$_.ProcessId)} | Select-Object ProcessId,ParentProcessId,Name | ConvertTo-Json -Compress"""
manifest=json.loads((ROOT/'reviews/codex-supervision/latest-live-file-hashes.json').read_text(encoding='utf-8'))['files']
watched=sorted(set(manifest)|{'reviews/2026-10-04-acceptance-support/file_acceptance.py','tools/render_pilot.py','tools/b5_annotation_set.py','data/b5-annotation-set/b5-annotation-set.json','data/b5-annotation-set/b5-annotation-set.md','tools/runpy.py','tools/b5_calibrate.py','data/b5-calibration-report/b5-calibration-report.json','data/b5-calibration-report/b5-calibration-report.md','data/b5-calibration-report/pdf/b5-calibration-report.pdf'})
write('watcher.json',{'pid':os.getpid(),'started_at':now(),'interval_seconds':5,'scope':'read-only process/file/head observer; no autonomous AI review or approval','stop_file':str(OUT/'STOP')})
prior=None;event('watch_started',{'pid':os.getpid()})
while not (OUT/'STOP').exists():
 try:
  cp=subprocess.run(['powershell.exe','-NoLogo','-NoProfile','-Command',PS],capture_output=True,timeout=15)
  if cp.returncode:raise RuntimeError('CIM failed: '+cp.stderr.decode('utf-8','replace')[-300:])
  v=cp.stdout.decode('utf-8-sig').strip();procs=json.loads(v) if v else [];procs=[procs] if isinstance(procs,dict) else procs
  procs=sorted(procs,key=lambda p:p['ProcessId']);jobs=[p for p in procs if p['Name'].lower() not in ('claude.exe','conhost.exe')]
  sha={}
  for rel in watched:
   p=ROOT/rel
   try:sha[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
   except OSError:sha[rel]=None
  git=subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,capture_output=True,text=True,timeout=5)
  head=git.stdout.strip() if git.returncode==0 else None
  state={'time':now(),'watcher_pid':os.getpid(),'head':head,'claude_tree':procs,'child_jobs':jobs,'hashes':sha,'core_drift':[rel for rel,expected in manifest.items() if sha[rel]!=expected]}
  if prior is None:event('baseline',{'head':head,'tree':procs,'core_drift':state['core_drift']})
  else:
   old={p['ProcessId']:p for p in prior['claude_tree']};new={p['ProcessId']:p for p in procs}
   for pid in sorted(new.keys()-old.keys()):event('process_started',new[pid])
   for pid in sorted(old.keys()-new.keys()):event('process_ended',old[pid])
   if head!=prior['head']:event('commit_changed',{'before':prior['head'],'after':head})
   for rel,value in sha.items():
    if value!=prior['hashes'].get(rel):event('file_changed',{'path':rel,'before':prior['hashes'].get(rel),'after':value})
   if state['core_drift']!=prior['core_drift']:event('core_drift_changed',state['core_drift'])
  write('latest.json',state);prior=state
 except Exception as e:event('observer_error',{'error':repr(e)})
 time.sleep(5)
event('watch_stopped',{'pid':os.getpid()})
write('stopped.json',{'pid':os.getpid(),'time':now()})
