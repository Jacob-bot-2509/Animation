"""Synthetic review probes; never execute generated code or attack payloads."""
from pathlib import Path
from unittest.mock import patch
import contextlib, hashlib, importlib.util, io, json, subprocess, sys, tempfile
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/"src"))
from animtrain.render_gate import math_check, render_check
from animtrain.freeze import freeze_set, check_frozen
from animtrain.run_record import RunRecord
from animtrain.manifest import sha256_file

def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT/path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

def captured(call):
    try:
        return {"returned": call()}
    except (Exception, SystemExit) as exc:
        return {"exception": type(exc).__name__, "detail": str(exc)}

result = {
    "head": subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
    "source_sha256": {f: hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in [
        "src/animtrain/render_gate.py", "src/animtrain/freeze.py", "tools/preflight.py",
        "tools/split_data.py", "src/animtrain/atomic_write.py"]},
    "math": {e: captured(lambda e=e: math_check(e)) for e in
             ["Eq(1, 2)", "False", "Eq(1, 1)", "x", "x + 1", "1", "2", "0", "x**2 >= 0"]}
}
with tempfile.TemporaryDirectory(prefix="codex-br-recheck-") as tmp:
    root = Path(tmp)
    data = root/"data.jsonl"
    data.write_text('{"id":"synthetic"}\n',encoding="utf-8")
    result["locks"] = {}
    cases = {
        "missing_entries":{"freeze_lock_version":1},
        "unlocked_empty":{"freeze_lock_version":1,"locked":False,"n_files":0,"entries":[]},
        "missing_hash":{"freeze_lock_version":1,"locked":True,"n_files":1,
                        "entries":[{"path":str(data),"size":data.stat().st_size}]},
        "null_path":{"freeze_lock_version":1,"locked":True,"n_files":1,
                     "entries":[{"path":None,"sha256":"0"*64,"size":1}]}
    }
    (root/"invalid_cases").mkdir()
    for name,obj in cases.items():
        lock=root/"invalid_cases"/(name+".lock.json")
        lock.write_text(json.dumps(obj),encoding="utf-8")
        result["locks"][name]=captured(lambda: check_frozen(lock))
    result["locks"]["create_empty"]=captured(lambda: freeze_set([],root/"empty.lock.json"))

    cli = module("review_cli", "tools/preflight.py")
    mp = root/"manifest.json"
    mp.write_text('{"name":"synthetic-review","entries":[]}',encoding="utf-8")
    rec=RunRecord(run_id="probe",kind="dry-run",config={"synthetic":True},
        git_commit=result["head"],manifest_hash="0"*64,
        summary={"command":"synthetic","manifest":str(mp)},env={"python":sys.version},
        dirty={"clean":True})
    rec.save(root/"runs/probe/run_record.json")
    result["snapshot"]={}
    for calibrated in [False,True,"matching_hash","unrelated_lock"]:
        if calibrated in ("matching_hash", "unrelated_lock"):
            rec.manifest_hash = sha256_file(mp)
            rec.save(root/"runs/probe/run_record.json")
        if calibrated == "unrelated_lock":
            note = root/"unrelated.txt"
            note.write_text("unrelated synthetic note", encoding="utf-8")
            freeze_set([note], root/"unrelated.lock.json")
        out=io.StringIO()
        with patch.object(cli,"ROOT",root), patch.object(cli,"validate_manifest",return_value={
             "ok":True,"n_entries":1,"problems":[],"quarantines":[],"near_dup_calibrated":calibrated is not False}), \
             patch("animtrain.preflight.check_gpu",return_value=(True,"mock")), \
             patch("animtrain.preflight.check_model_dir",return_value=(True,"mock")), \
             patch("animtrain.render_gate.check_manim_available",return_value=(True,"mock")), \
             patch("animtrain.render_gate.check_sympy_available",return_value=(True,"mock")), \
             patch("animtrain.render_gate.render_check", return_value={"ok":True,"status":"rendered","detail":"mock smoke","unverified":[]}) as render, \
             patch("animtrain.render_gate.math_check", return_value={"ok":True,"status":"verified","detail":"mock smoke","unverified":[]}) as math, \
             contextlib.redirect_stdout(out):
            rc=cli.main(["--ready","--run-id","probe","--manifest",str(mp),"--model",str(root)])
        result["snapshot"][str(calibrated)]={"exit_code":rc,"output":out.getvalue(),
            "actual_hash":sha256_file(mp),"record_hash":rec.manifest_hash,
            "render_check_calls":render.call_count,"math_check_calls":math.call_count, "render_input":render.call_args.args[0], "math_input":math.call_args.args[0]}

split_cli=module("review_split","tools/split_data.py")
result["frozen_write"]={}
for mode in ["valid_lock","omitted_lock","corrupt_lock","missing_lock","omitted_corrupt","omitted_nonstandard"]:
    with tempfile.TemporaryDirectory(prefix="codex-freeze-recheck-") as tmp:
        root=Path(tmp); inp=root/"input"; inp.mkdir()
        pool=inp/"pool.jsonl"; plan=inp/"plan.json"; out=root/"output"
        pool.write_text('{"id":"a"}\n{"id":"b"}\n',encoding="utf-8")
        plan.write_text('{"train":["a"],"eval":["b"],"test":[]}',encoding="utf-8")
        split_cli.split(pool,plan,out,False,license_="internal-generated")
        lock=out/("freeze.json" if mode=="omitted_nonstandard" else "frozen.lock.json")
        freeze_set([out/"eval.jsonl"],lock)
        before={p.name:sha256_file(p) for p in out.iterdir() if p.suffix==".jsonl"}
        plan.write_text('{"train":["b"],"eval":["a"],"test":[]}',encoding="utf-8")
        locks=[lock]
        if mode in ("omitted_lock","omitted_corrupt","omitted_nonstandard"): locks=[]
        if mode=="omitted_corrupt": lock.write_text("{",encoding="utf-8")
        if mode=="corrupt_lock": lock.write_text("{",encoding="utf-8")
        if mode=="missing_lock": locks=[out/"does-not-exist.lock.json"]
        outcome=captured(lambda:split_cli.split(pool,plan,out,False,force=True,
            license_="internal-generated",frozen_locks=locks))
        after={p.name:sha256_file(p) for p in out.iterdir() if p.suffix==".jsonl"}
        result["frozen_write"][mode]={"outcome":outcome,
            "changed_files":[name for name in before if before[name]!=after[name]]}

with patch("animtrain.render_gate.check_manim_available",return_value=(True,"mock")), \
     patch("animtrain.render_gate.subprocess.run") as run:
    run.return_value.returncode=0
    run.return_value.stderr=""
    rendered=render_check("x = 1")
    result["isolation_mock"]={"result":rendered,"subprocess_calls":run.call_count,
        "note":"Mocked subprocess only. No actual code execution or render verification."}

dest=Path(__file__).with_name("results.json")
dest.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(result,ensure_ascii=False,indent=2))
