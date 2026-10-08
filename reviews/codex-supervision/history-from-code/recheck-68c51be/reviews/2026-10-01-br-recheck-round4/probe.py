"""Capture CLI integration outcomes and independent frozen-write checks."""
from pathlib import Path
from unittest.mock import patch
import hashlib, importlib.util, json, subprocess, sys, tempfile
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/"src"))
from animtrain.freeze import freeze_set
from animtrain.manifest import sha256_file

def module(name, file):
    spec=importlib.util.spec_from_file_location(name, ROOT/file)
    obj=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

review=module("review_tests","tests/test_preflight_evidence_review.py")
actual=review.run_preflight
observed=[]
def capture(*args,**kwargs):
    result=actual(*args,**kwargs)
    observed.append(result)
    return result
with patch.object(review,"run_preflight",side_effect=capture):
    review.TestFreezeEvidenceCLI().test_freeze_gate_checks_coverage_and_mandatory_binding()
cases=("matching","missing_binding","wrong_binding","unrelated","partial","corrupt","no_lock")
result={"head":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
        "cli_cases":dict(zip(cases,observed)),
        "source_sha256":{f:hashlib.sha256((ROOT/f).read_bytes()).hexdigest() for f in
            ["src/animtrain/freeze.py","tools/preflight.py","tools/split_data.py",
             "tests/test_preflight_evidence_review.py"]}}
split=module("review_split","tools/split_data.py")
result["frozen_write"]={}
for case in ("omitted_valid","omitted_corrupt","nonstandard_name"):
    with tempfile.TemporaryDirectory(prefix="codex-freeze-r4-") as tmp:
        root=Path(tmp); inp=root/"input"; inp.mkdir()
        pool=inp/"pool.jsonl"; plan=inp/"plan.json"; out=root/"output"
        pool.write_text('{"id":"a"}\n{"id":"b"}\n',encoding="utf-8")
        plan.write_text('{"train":["a"],"eval":["b"],"test":[]}',encoding="utf-8")
        split.split(pool,plan,out,False,license_="internal-generated")
        before={p.name:sha256_file(p) for p in out.iterdir()}
        lock=out/("freeze.json" if case=="nonstandard_name" else "frozen.lock.json")
        try:
            freeze_set([out/"eval.jsonl"],lock)
            if case=="omitted_corrupt":
                lock.write_text("{",encoding="utf-8")
            plan.write_text('{"train":["b"],"eval":["a"],"test":[]}',encoding="utf-8")
            split.split(pool,plan,out,False,force=True,license_="internal-generated")
            outcome={"returned":"write succeeded"}
        except (Exception,SystemExit) as exc:
            outcome={"exception":type(exc).__name__,"detail":str(exc)}
        outcome["changed_outputs"]=[name for name,h in before.items() if sha256_file(out/name)!=h]
        result["frozen_write"][case]=outcome
dest=Path(__file__).with_name("results.json")
dest.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"cli_cases":{k:{"ready":v["ready"],"exit_code":v["exit_code"],
    "freeze_gate":next(c for c in v["checks"] if c["check"]=="freeze_gate")} for k,v in result["cli_cases"].items()},
    "frozen_write":result["frozen_write"]},ensure_ascii=False,indent=2))
