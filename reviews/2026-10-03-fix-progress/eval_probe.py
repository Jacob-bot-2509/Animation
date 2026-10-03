"""GS3 candidate split consistency, synthetic data only."""
import json,sys,tempfile,subprocess,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/"src"))
from animtrain.dataset_intake import intake_report
from animtrain.manifest import Manifest
from animtrain.validate import validate_manifest
out=[]
with tempfile.TemporaryDirectory() as td:
 d=Path(td);train=d/"train.jsonl";train.write_text((ROOT/"reviews/fixtures-eval-test/train_synthetic.jsonl").read_text(encoding="utf-8"),encoding="utf-8")
 r=json.loads((ROOT/"reviews/fixtures-eval-test/eval_ok.jsonl").read_text(encoding="utf-8"));r.pop("id");r.update(problem_id="p1",solution_id="s1",method="method1")
 def write(p,rows):p.parent.mkdir(parents=True,exist_ok=True);p.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in rows)+"\n",encoding="utf-8")
 def run(p):
  cp=subprocess.run([sys.executable,"-X","utf8",str(ROOT/"tools/eval_test_prep.py"),"check",str(p),"--train-dir",str(train)],capture_output=True,encoding="utf-8")
  return {"exit_code":cp.returncode,"stdout":cp.stdout,"stderr":cp.stderr}
 group=d/"eval";write(group/"a.jsonl",[r]);write(group/"b.jsonl",[{**r,"solution_id":"s2","method":"method2"}])
 out.append({"case":"same_eval_problem_two_files","expected":"same split multi-method rows accepted regardless of storage sharding",**run(group)})
 single=d/"single.jsonl";write(single,[r,{**r,"solution_id":"s2","method":"method2"}])
 out.append({"case":"same_eval_problem_one_file","expected":"same logical data should give same outcome as two files",**run(single)})
 write(single,[r,{**r,"solution_id":"s2"}]);out.append({"case":"duplicate_method","expected":"same problem must use distinct methods",**run(single)})
 write(single,[r,{**r,"solution_id":"s2","method":"method2","problem":"An entirely independent synthetic vector geometry problem."}]);out.append({"case":"same_problem_id_different_problem","expected":"problem identity must bind one stable problem body",**run(single)})
 r.pop("method");write(single,[r]);out.append({"case":"missing_method","expected":"multi-solution identity requires method",**run(single)})
 intake=intake_report([single]);mp=d/"manifest.json";mp.write_text(json.dumps({"name":"synthetic","version":1,"entries":[{"path":single.name,"split":"eval","sha256":hashlib.sha256(single.read_bytes()).hexdigest(),"size":single.stat().st_size,"source":"synthetic","license":"internal-generated"}]}),encoding="utf-8")
 result=validate_manifest(Manifest.load(mp),d)
 out.append({"case":"multi_solution_intake_manifest_identity_mismatch","intake_status":intake["status"],"intake_problems":intake["problems"],"manifest_exit":result["exit_code"],"manifest_problems":result["problems"]})
doc={"source_hashes":{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ["src/animtrain/dataset_intake.py","tools/eval_test_prep.py","src/animtrain/validate.py"]},"results":out}
(Path(__file__).parent/"eval-results.json").write_text(json.dumps(doc,ensure_ascii=False,indent=2),encoding="utf-8");print(json.dumps(doc,ensure_ascii=False,indent=2))
