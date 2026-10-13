"""Synthetic replay contract probes; does not create a real run record."""
import sys,tempfile,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"src"))
from animtrain.run_record import RunRecord,verify_replay
with tempfile.TemporaryDirectory() as td:
 d=Path(td);m=d/"manifest.json";m.write_text("{}");c=d/"config.json";c.write_text("{}")
 r=RunRecord(run_id="synthetic",kind="baseline",config={"file":str(c),"sha256":hashlib.sha256(c.read_bytes()).hexdigest()},git_commit="a"*40,manifest_hash=hashlib.sha256(m.read_bytes()).hexdigest(),summary={"command":"synthetic never executed","manifest":str(m)},metrics={"dummy":1},env={"python":"synthetic"},seed=0,dirty={"clean":False,"changed":["src/a.py"]})
 out=[]
 out.append({"case":"replay_different_dirty_files","expected":"different worktree source must block replay","problems":verify_replay(r,m,"a"*40,{"clean":False,"changed":["src/b.py"]},c)})
 r.config={"learning_rate":0.1}
 out.append({"case":"replay_no_config_binding","expected":"baseline without bound config file must block replay","problems":verify_replay(r,m,"a"*40,{"clean":False,"changed":["src/a.py"]},None)})
 p=Path(__file__).parent/"replay-results.json";p.write_text(json.dumps({"source_hashes":{x:hashlib.sha256((ROOT/x).read_bytes()).hexdigest() for x in ["src/animtrain/run_record.py","tools/run_record.py"]},"results":out},indent=2),encoding="utf-8")
 print(json.dumps(out,indent=2))
