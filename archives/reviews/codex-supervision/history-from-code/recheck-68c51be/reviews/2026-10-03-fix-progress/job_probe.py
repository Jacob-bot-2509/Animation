"""GS5 post-fix probes use mocks; never launch generated code."""
import sys,json,hashlib
from pathlib import Path
from unittest.mock import patch,Mock
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/"src"))
import animtrain.win_job as wj
from animtrain.render_gate import render_check
out=[]
job=wj.WindowsJob(64)
try:
 with patch.object(wj,"_assign_process",return_value=0),patch.object(wj.ctypes,"get_last_error",return_value=5):
  try:job.assign(Mock(_handle=1));raised=False
  except OSError:raised=True
  out.append({"case":"assign_error_5_now_rejected","expected":"raise for every failed assignment","raised":raised,"assigned_count":len(job.assigned)})
finally:job.close()
proc=Mock();proc.returncode=0;proc.communicate.return_value=("","")
fakejob=Mock();fakejob.assign.side_effect=OSError("injected assignment failure")
with patch("animtrain.render_gate.check_manim_available",return_value=(True,"mock")),patch("animtrain.render_gate.subprocess.Popen",return_value=proc),patch("animtrain.render_gate.WindowsJob",return_value=fakejob):
 rep=render_check("# only mocked; never executed",trusted=True)
out.append({"case":"assignment_failure_cleanup_now_kills_waits","status":rep["status"],"kill_called":proc.kill.called,"wait_called":proc.wait.called,"job_assigned":rep["isolation"]["job_assigned"]})
proc=Mock();proc.returncode=0;proc.communicate.return_value=("","")
with patch("animtrain.render_gate.check_manim_available",return_value=(True,"mock")),patch("animtrain.render_gate.subprocess.Popen",return_value=proc),patch("animtrain.render_gate.WindowsJob",side_effect=[OSError("injected creation failure"),Mock()]):
 rep=render_check("# only mocked; never executed",trusted=True)
out.append({"case":"unassigned_render_metadata","expected":"actual render memory limit is absent","status":rep["status"],"memory_limit_mb":rep["isolation"]["memory_limit_mb"],"job_assigned":rep["isolation"]["job_assigned"]})
doc={"source_hashes":{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ["src/animtrain/win_job.py","src/animtrain/render_gate.py"]},"results":out}
(Path(__file__).parent/"job-results.json").write_text(json.dumps(doc,indent=2),encoding="utf-8");print(json.dumps(doc,indent=2))
