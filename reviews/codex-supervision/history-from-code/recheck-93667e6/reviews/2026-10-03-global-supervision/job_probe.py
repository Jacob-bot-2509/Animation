"""Job failure probes use mocks only; never launch generated code."""
import sys,json,hashlib
from pathlib import Path
from unittest.mock import patch,Mock
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/"src"))
import animtrain.win_job as wj
from animtrain.render_gate import render_check
out=[]
job=wj.WindowsJob(64)
try:
    with patch.object(wj._kernel32,"AssignProcessToJobObject",return_value=0),patch.object(wj.ctypes,"get_last_error",return_value=5):
        job.assign(Mock(_handle=1))
        out.append({"case":"assign_error_5","expected":"any job assignment failure must raise","raised":False,"assigned_count":len(job.assigned)})
except OSError:
    out.append({"case":"assign_error_5","raised":True})
finally:job.close()
proc=Mock();proc.returncode=0;proc.communicate.return_value=("","")
fakejob=Mock();fakejob.assign.side_effect=OSError("injected assignment failure")
with patch("animtrain.render_gate.check_manim_available",return_value=(True,"mock")),patch("animtrain.render_gate.subprocess.Popen",return_value=proc),patch("animtrain.win_job.WindowsJob",return_value=fakejob):
    rep=render_check("# mock only; never launched",trusted=True)
out.append({"case":"render_assignment_failure_cleanup","expected":"launched process terminated and waited before returning","status":rep["status"],"kill_called":proc.kill.called,"wait_called":proc.wait.called,"communicate_called":proc.communicate.called,"job_terminate_called":fakejob.terminate.called,"job_close_called":fakejob.close.called})
proc=Mock();proc.returncode=0;proc.communicate.return_value=("","")
with patch("animtrain.render_gate.check_manim_available",return_value=(True,"mock")),patch("animtrain.render_gate.subprocess.Popen",return_value=proc),patch("animtrain.win_job.WindowsJob",side_effect=[OSError("injected per-render creation failure"),Mock()]):
    rep=render_check("# mock only; never launched",trusted=True)
out.append({"case":"render_without_job_reports_memory","expected":"this render must report no actual memory limit","status":rep["status"],"memory_limit_mb":rep["isolation"]["memory_limit_mb"]})
doc={"source_hashes":{x:hashlib.sha256((ROOT/x).read_bytes()).hexdigest() for x in ["src/animtrain/win_job.py","src/animtrain/render_gate.py","src/animtrain/preflight.py"]},"results":out}
(Path(__file__).parent/"job-results.json").write_text(json.dumps(doc,indent=2),encoding="utf-8")
print(json.dumps(doc,indent=2))
