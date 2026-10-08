"""Read-only preparation audit; tokenization and synthetic records only, no model load."""
import ast
import hashlib
import importlib.util
import importlib.metadata as md
import json
import platform
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"src"))
from animtrain.manifest import Manifest
from animtrain.validate import validate_manifest
from animtrain.preflight import check_model_dir, check_asset_evidence
from animtrain.metrics import SampleResult,aggregate,finalize_result
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths=["src/animtrain/metrics.py","src/animtrain/backend.py","tools/screening_probe.py",
       "tools/screening_qlora_probe.py","tools/model_provenance.py","src/animtrain/preflight.py",
       "requirements.txt","train_config.template.json"]
r={"head":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip(),
   "source_hashes":{p:sha(ROOT/p) for p in paths},"no_model_execution":True}
r["environment"]={"python":sys.version,"executable":sys.executable,"platform":platform.platform()}
r["environment"]["packages"]={}
for p in ["torch","transformers","peft","accelerate","bitsandbytes","tokenizers","datasets","trl","safetensors","numpy","pytest"]:
    try:r["environment"]["packages"][p]=md.version(p)
    except md.PackageNotFoundError:r["environment"]["packages"][p]="NOT_INSTALLED"
import torch
r["environment"]["torch"]={"version":torch.__version__,"cuda_build":torch.version.cuda,
                          "cuda_available":torch.cuda.is_available(),"arch_list":torch.cuda.get_arch_list()}
if torch.cuda.is_available():
    g=torch.cuda.get_device_properties(0)
    r["environment"]["gpu"]={"name":g.name,"compute_capability":[g.major,g.minor],
                           "total_memory":g.total_memory,"bf16_supported":torch.cuda.is_bf16_supported()}
pc=subprocess.run([sys.executable,"-m","pip","check"],capture_output=True,text=True,timeout=30)
r["environment"]["pip_check"]={"exit":pc.returncode,"stdout":pc.stdout.strip(),"stderr":pc.stderr.strip()}
mp=ROOT/"data/v1/manifest-train.json"
r["data"]={"manifest_sha256":sha(mp),"validation":validate_manifest(Manifest.load(mp),mp.parent),
           "asset_evidence":check_asset_evidence(mp),
           "eval_files":[p.name for p in (ROOT/"data/v1/eval").glob("*.jsonl")],
           "test_files":[p.name for p in (ROOT/"data/v1/test").glob("*.jsonl")]}
r["baseline_model"]={"strict_file_check":check_model_dir(ROOT/".models/qwen3-4b",strict=True)}
prov=ROOT/".models/qwen3-4b/PROVENANCE.json"
if prov.exists():
    p=json.loads(prov.read_text(encoding="utf-8"))
    r["baseline_model"]["provenance"]={"sha256":sha(prov),"version":p.get("provenance_version"),
                                    "source":p.get("source"),"index_problems":p.get("index_problems"),
                                    "weight_files":len(p.get("weight_files",[]))}
archive=ROOT/"reviews/2026-10-03-model-screening"
cleanup=json.loads((archive/"screening-cleanup-manifest.json").read_text(encoding="utf-8"))
evidence=archive/"evidence"
r["screening_archive"]={"evidence_exists":evidence.exists(),"tmp_exists":(ROOT/"outputs/screening-tmp").exists(),
                       "archive_files":[p.name for p in archive.iterdir()],
                       "n_cleanup_files":len(cleanup["files"]),
                       "archived_matches":sum((evidence/f["path"]).is_file() for f in cleanup["files"])}
def observe(fn):
    try:return fn()
    except ValueError as exc:return {"rejected":True,"reason":str(exc)}
r["metrics_observed"]={
    "missing_latency":aggregate([SampleResult("a","h",status="failed")]),
    "foreign_math_review":observe(lambda:aggregate([SampleResult("a","h")],{"foreign1":True,"foreign2":True})),
    "math_failure_with_valid_json":finalize_result(SampleResult("a","h",parsed_strict=True,
                              parsed_lenient=True,failure_class="math_error",failure_detail="wrong")).to_dict(),
}
spec=importlib.util.spec_from_file_location("screening_probe",ROOT/"tools/screening_probe.py")
probe=importlib.util.module_from_spec(spec);spec.loader.exec_module(probe)
valid=json.dumps({"scene_spec":{"objects":["axis"],"steps":["draw"]}})
r["thinking_parser"]={}
for case,text in [("missing_open_tag","scratch {\"x\":1}</think>\n"+valid),
                  ("unclosed_think_with_json","<think>"+valid),
                  ("closed_think","<think>{\"x\":1}</think>"+valid)]:
    think,final,truncated=probe.split_think_final(text)
    parsed,strict=probe.extract_scene_spec(final)
    r["thinking_parser"][case]={"truncated":truncated,"parsed":parsed is not None,"strict":strict,
                              "final_is_empty":not final.strip()}
tree=ast.parse((ROOT/"tools/screening_probe.py").read_text(encoding="utf-8"))
def calls_with_keyword(method,key):
    return any(isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)
               and n.func.attr==method and any(k.arg==key for k in n.keywords) for n in ast.walk(tree))
r["static_checks"]={
    "template_enable_thinking_wired": calls_with_keyword("apply_chat_template","enable_thinking"),
    "enable_thinking_is_generate_kwarg": calls_with_keyword("generate","enable_thinking"),
    "qlora_reset_peak_call": "reset_peak_memory_stats(" in (ROOT/"tools/screening_qlora_probe.py").read_text(encoding="utf-8"),
    "qlora_prepare_kbit_call":"prepare_model_for_kbit_training(" in (ROOT/"tools/screening_qlora_probe.py").read_text(encoding="utf-8"),
}
with tempfile.TemporaryDirectory(prefix="prep-file-audit-") as td:
    fake=Path(td)
    for name in ("config.json","tokenizer_config.json","tokenizer.json"):(fake/name).write_text("{}")
    (fake/"model.safetensors").write_text("version https://git-lfs.github.com/spec/v1\noid sha256:"+"0"*64+"\nsize 999\n")
    r["strict_preflight_lfs_pointer"]=check_model_dir(fake,strict=True)
# Tokenizer only: never AutoModel, never forward/generate/backward.
from transformers import AutoTokenizer
tok=AutoTokenizer.from_pretrained(str(ROOT/".models/qwen3-4b"),local_files_only=True,trust_remote_code=False)
records=[]
for path in sorted((ROOT/"data/v1/raw").glob("dataset_*.jsonl")):
    records.extend(json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
lengths=[]
for sample in records:
    user=probe.USER_TMPL.format(problem=sample["problem"],solution=sample["solution"])
    messages=[{"role":"system","content":probe.SYSTEM},{"role":"user","content":user},
              {"role":"assistant","content":json.dumps({"scene_spec":sample["scene_spec"]},ensure_ascii=False)}]
    tokens=tok.apply_chat_template(messages,tokenize=True,enable_thinking=False)
    ids=tokens["input_ids"] if isinstance(tokens,dict) or hasattr(tokens,"keys") else tokens
    lengths.append({"id":sample["id"],"total_tokens":len(ids)})
ordered=sorted(x["total_tokens"] for x in lengths)
r["token_budget"]={"task":"problem+solution->scene_spec; canonical JSON target; enable_thinking=False; tokenizer only",
                   "n":len(lengths),"min":ordered[0],"median":ordered[len(ordered)//2],"max":ordered[-1],
                   "over_1024":sum(x>1024 for x in ordered),"over_2048":sum(x>2048 for x in ordered),
                   "over_4096":sum(x>4096 for x in ordered),"per_sample":lengths}
prompt_messages=[{"role":"system","content":probe.SYSTEM},{"role":"user","content":"/no_think\nexample"}]
default_prompt=tok.apply_chat_template(prompt_messages,tokenize=False,add_generation_prompt=True)
disabled_prompt=tok.apply_chat_template(prompt_messages,tokenize=False,add_generation_prompt=True,enable_thinking=False)
r["tokenizer_think_template"]={"default_tail":default_prompt[-100:],"disabled_tail":disabled_prompt[-100:],
                             "different":default_prompt!=disabled_prompt}
r["source_unchanged_during_probe"]={p:sha(ROOT/p) for p in paths}==r["source_hashes"]
output=HERE/((sys.argv[1] if len(sys.argv)>1 else "current")+".json")
with output.open("x",encoding="utf-8") as dest:dest.write(json.dumps(r,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({k:v for k,v in r.items() if k not in ("token_budget","source_hashes")},ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in r["token_budget"].items() if k!="per_sample"},ensure_ascii=False,indent=2))
