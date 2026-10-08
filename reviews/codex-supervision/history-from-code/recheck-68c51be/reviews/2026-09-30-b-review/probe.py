"""Independent, synthetic negative probes; no generated code execution."""
from pathlib import Path
from unittest.mock import patch
import contextlib, hashlib, importlib.util, io, json, subprocess, sys, tempfile
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from animtrain.preflight import run_preflight
from animtrain.render_gate import math_check
from animtrain.freeze import check_frozen, freeze_set
from animtrain.manifest import Manifest, Entry, sha256_file
from animtrain.validate import validate_manifest
from animtrain.run_record import RunRecord

result = {"head": subprocess.check_output(["git","rev-parse","HEAD"], cwd=ROOT, text=True).strip(),
          "source_sha256": {f: hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in
          ["src/animtrain/preflight.py","src/animtrain/render_gate.py","src/animtrain/freeze.py",
           "tools/preflight.py","tools/split_data.py","src/animtrain/atomic_write.py"]}}
base = [("data_manifest",(True,"synthetic")),("run_snapshot",(True,"synthetic"))]
with patch("animtrain.preflight.check_gpu", return_value=(True,"mock")), patch(
        "animtrain.preflight.check_model_dir", return_value=(True,"mock")):
    result["ready_cases"] = {
        "extra_failure": run_preflight(ROOT, base+[("render_gate",(False,"render failed"))],ready=True),
        "duplicate_failure": run_preflight(ROOT, base+[("data_manifest",(False,"bad")),("data_manifest",(True,"later"))],ready=True),
        "duplicate_unverified": run_preflight(ROOT,base+[("math_gate",(True,"pending",{"unverified":["math"]})),("math_gate",(True,"later"))],ready=True),
        "all_pass": run_preflight(ROOT,base,ready=True)}
result["math"] = {e: math_check(e) for e in ["Eq(1, 2)","False","1","Eq(1, 1)"]}
with tempfile.TemporaryDirectory(prefix="codex-b-review-") as tmp:
    root = Path(tmp)
    lock = root/"lock.json"
    result["freeze"] = {}
    for key,obj in {"missing_entries":{"freeze_lock_version":1},
                    "unlocked_empty":{"freeze_lock_version":1,"locked":False,"n_files":0,"entries":[]}}.items():
        lock.write_text(json.dumps(obj),encoding="utf-8")
        result["freeze"][key] = check_frozen(lock)
    fresh = root/"empty.lock.json"
    freeze_set([],fresh)
    result["freeze"]["empty_created"] = check_frozen(fresh)
    p = root/"sample.json"
    p.write_text('{"id":"synthetic","problem":"1+1","solution":"2"}',encoding="utf-8")
    result["a1_json"] = {}
    for split in ["train","eval","test"]:
        m = Manifest(name="synthetic-review",entries=[Entry(path=p.name,sha256=sha256_file(p),
            size=p.stat().st_size,source="codex synthetic review",license="internal-generated",split=split)])
        result["a1_json"][split] = validate_manifest(m,root)

    # Run real preflight CLI plumbing with mocked hardware and unrelated data validation.
    # Deliberately isolate snapshot hash validation from other gates.
    spec = importlib.util.spec_from_file_location("review_preflight_cli",ROOT/"tools/preflight.py")
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    mp = root/"manifest.json"
    mp.write_text('{"name":"synthetic-review","entries":[]}',encoding="utf-8")
    rec = RunRecord(run_id="probe",kind="dry-run",config={"synthetic":True},
        git_commit=result["head"],manifest_hash="0"*64,summary={"command":"synthetic","manifest":str(mp)},
        env={"python":sys.version},dirty={"clean":True})
    rec.save(root/"runs/probe/run_record.json")
    output = io.StringIO()
    with patch.object(cli,"ROOT",root), patch.object(cli,"validate_manifest",
          return_value={"ok":True,"n_entries":1,"problems":[],"quarantines":[]}), patch(
          "animtrain.preflight.check_gpu",return_value=(True,"mock")), patch(
          "animtrain.preflight.check_model_dir",return_value=(True,"mock")), contextlib.redirect_stdout(output):
        rc = cli.main(["--ready","--run-id","probe","--manifest",str(mp),"--model",str(root)])
    result["stale_snapshot_with_mocked_other_gates"] = {"exit_code":rc,"output":output.getvalue(),
        "record_hash":"0"*64,"actual_hash":sha256_file(mp)}

# Frozen output overwrite probe, entirely within a synthetic temporary directory.
with tempfile.TemporaryDirectory(prefix="codex-frozen-split-") as tmp:
    root = Path(tmp)
    spec = importlib.util.spec_from_file_location("review_split_cli", ROOT/"tools/split_data.py")
    split_cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(split_cli)
    pool = root/"input/pool.jsonl"
    pool.parent.mkdir()
    pool.write_text('{"id":"a","problem":"synthetic a"}\n{"id":"b","problem":"synthetic b"}\n',encoding="utf-8")
    plan = root/"input/plan.json"
    plan.write_text('{"train":["a"],"eval":["b"],"test":[]}',encoding="utf-8")
    output = root/"output"
    split_cli.split(pool,plan,output,False,license_="internal-generated")
    lock = output/"frozen.lock.json"
    freeze_set([output/"eval.jsonl"],lock)
    before_hash = sha256_file(output/"eval.jsonl")
    plan.write_text('{"train":["b"],"eval":["a"],"test":[]}',encoding="utf-8")
    split_cli.split(pool,plan,output,False,force=True,license_="internal-generated")
    result["frozen_split_force"] = {
        "changed": sha256_file(output/"eval.jsonl") != before_hash,
        "post_write_check": check_frozen(lock),
        "note":"Write succeeded; only a later explicit lock check detected the damage."}

out = Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name("before.json")
out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"output":str(out),"ready":{k:(v["ready"],v["exit_code"]) for k,v in result["ready_cases"].items()},
                  "math":result["math"],"freeze":result["freeze"],
                  "a1_json":{k:v["ok"] for k,v in result["a1_json"].items()},
                  "stale_snapshot_exit":rc},ensure_ascii=False,indent=2))
