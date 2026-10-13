"""Synthetic review probes. No generated code is executed, no model is loaded."""
import hashlib
import json
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]
from animtrain.manifest import Entry, Manifest, sha256_file
from animtrain.validate import validate_manifest
from animtrain.preflight import run_preflight, check_model_dir
from animtrain.run_record import RunRecord, check_record
from tools.split_data import split
import animtrain.validate as validation

HERE = Path(__file__).resolve().parent
FIX = HERE / "fixtures"
FIX.mkdir(exist_ok=False)
results = {}

def put(name, text):
    p = FIX / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p

def ent(p, role, root=FIX):
    return Entry(path=str(p.relative_to(root)), sha256=sha256_file(p),
                 source="synthetic-review", license="internal-generated",
                 split=role, size=p.stat().st_size)

valid = put("guard/root/valid.jsonl", '{"id":"safe"}\n')
outside = put("guard/outside.jsonl", '{"id":"outside"}\n')
root = valid.parent
m = Manifest(name="probe", entries=[
    ent(valid, "train", root),
    Entry(path="../outside.jsonl", sha256=sha256_file(outside),
          source="synthetic-review", license="internal-generated", split="eval")
])
reads = []
original = validation._load_lines
def track(p):
    reads.append(str(p.resolve()))
    return original(p)
with patch.object(validation, "_load_lines", side_effect=track):
    report = validate_manifest(m, root)
results["rejected_path_read_again"] = {
    "report_ok": report["ok"],
    "outside_read": str(outside.resolve()) in reads,
    "problems": report["problems"]
}

ev = put("bad-eval.jsonl", "not valid json\n")
results["bad_eval_accepted"] = validate_manifest(
    Manifest(name="probe", entries=[ent(ev, "eval")]), FIX)

r = RunRecord(run_id="probe", kind="dry-run", config={"x": 1},
              git_commit="abc1234", manifest_hash="f"*64,
              summary={"command":"probe", "manifest":str(FIX/"absent.json")},
              env={"python":sys.version.split()[0]})
results["missing_manifest_accepted"] = check_record(r, FIX/"absent.json")

with patch("animtrain.preflight.check_gpu", return_value=(True, "mock")), patch(
    "animtrain.preflight.check_model_dir", return_value=(True, "mock")):
    results["unrelated_check_satisfies_strict"] = run_preflight(
        FIX, extra_checks=[("unrelated", (True, "not a data gate"))], strict=True)

for name in ("config.json", "tokenizer_config.json", "tokenizer.json"):
    put("empty-model/"+name, "{}")
put("empty-model/model.safetensors", "")
results["zero_byte_weights_pass_strict"] = check_model_dir(FIX/"empty-model", strict=True)

pool = put("pool.jsonl", '{"id":"a"}\n')
plan = put("plan.json", '{"train":["a"],"eval":[],"test":[]}')
split(pool, plan, FIX/"split-output", False)
manifest = Manifest.load(FIX/"split-output/split_manifest.json")
results["split_assumed_license"] = {e.path:e.license for e in manifest.entries}
results["split_empty_sets_gate"] = validate_manifest(manifest, FIX/"split-output")

plan_alias = put("overwrite-plan/train.jsonl", '{"train":["a"],"eval":[],"test":[]}')
before = plan_alias.read_bytes()
split(pool, plan_alias, plan_alias.parent, False, force=True)
results["force_overwrites_input_plan"] = before != plan_alias.read_bytes()

results["source_snapshot"] = {
    str(p.relative_to(ROOT)):sha256_file(p)
    for folder in ("src", "tools", "tests") for p in sorted((ROOT/folder).rglob("*.py"))
}
(HERE/"probe_results.json").write_text(
    json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({k:v for k,v in results.items() if k!="source_snapshot"},
                 ensure_ascii=False,indent=2))
