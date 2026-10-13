"""Replay evidence probes; no real run records or source files are modified."""
import json,hashlib,sys,tempfile,subprocess
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/"src"));sys.path.insert(0,str(ROOT))
from animtrain.run_record import RunRecord,verify_replay
import tools.run_record as cli
out=[]
with tempfile.TemporaryDirectory() as td:
 d=Path(td);m=d/"manifest.json";m.write_text("{}");c=d/"config.json";c.write_text("{}")
 r=RunRecord(run_id="synthetic",kind="baseline",config={"file":str(c),"sha256":hashlib.sha256(c.read_bytes()).hexdigest()},git_commit="a"*40,manifest_hash=hashlib.sha256(m.read_bytes()).hexdigest(),summary={"command":"synthetic only","manifest":str(m)},metrics={"dummy":1},env={"python":"synthetic"},seed=0,dirty={"clean":False,"changed":["deleted_a.py"],"hashes":{}})
 out.append({"case":"dirty_different_deletions","expected":"different deleted paths must block replay","problems":verify_replay(r,m,"a"*40,{"clean":False,"changed":["deleted_b.py"],"hashes":{}},c)})
 pkg=d/"new_package";pkg.mkdir();f=pkg/"code.py";f.write_text("original content")
 cp=subprocess.CompletedProcess([],0,stdout="?? new_package/\n",stderr="")
 with patch.object(cli,"ROOT",d),patch.object(cli.subprocess,"run",return_value=cp):
  first=cli.git_dirty();f.write_text("different untracked code");second=cli.git_dirty()
 r.dirty=first
 out.append({"case":"untracked_directory_content_not_hashed","expected":"changed untracked code must block replay","recorded_dirty":first,"current_dirty":second,"problems":verify_replay(r,m,"a"*40,second,c)})
 out.append({"case":"missing_current_code_evidence","expected":"missing current git/dirty evidence cannot prove replay","problems":verify_replay(r,m,"",None,c)})
 r.config={"learning_rate":0.1}
 out.append({"case":"baseline_missing_config_now_blocked","expected":"missing config binding must block baseline","problems":verify_replay(r,m,"a"*40,second,None)})
doc={"source_hashes":{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ["src/animtrain/run_record.py","tools/run_record.py"]},"results":out}
(Path(__file__).parent/"replay-results.json").write_text(json.dumps(doc,indent=2),encoding="utf-8");print(json.dumps(doc,indent=2))
