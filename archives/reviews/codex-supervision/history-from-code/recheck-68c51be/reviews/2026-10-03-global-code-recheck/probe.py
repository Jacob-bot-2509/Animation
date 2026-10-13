"""Recheck of msg_178 plus synthetic residual gate/freeze edges."""
import importlib.util, json, pathlib, sys, tempfile
ROOT=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/"src"))
from animtrain.dataset_intake import convert_array_to_jsonl,check_intake_file,check_record
from animtrain.freeze import freeze_set
from animtrain.manifest import Manifest,Entry,sha256_file
from animtrain.validate import validate_manifest
from tests.test_dataset_intake import clean_record
spec=importlib.util.spec_from_file_location("global_review_base",ROOT/"reviews/2026-10-03-global-code-review/probe.py")
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
r=base.run()
r["baseline_tests"]={"before_codex_patch":200,"after_codex_patch":206,"subtests":29,"seconds":6.67}
r["edge_test_before"]={"failed":5,"passed":1}
r["residual_A6"]={}
r["edge_A7"]={}
with tempfile.TemporaryDirectory(prefix="codex-global-recheck-") as tmp:
 root=pathlib.Path(tmp)
 for case in ["target_lock","empty_marker","wrong_version","unlocked_marker"]:
  d=root/case;d.mkdir()
  src=d/"source.json";src.write_text(json.dumps([clean_record()]),encoding="utf-8")
  dst=d/"eval.jsonl";dst.write_text(json.dumps(clean_record(id="old"))+"\n",encoding="utf-8")
  lk=d/"eval.lock.json"
  if case=="target_lock":freeze_set([dst.resolve()],lk);dst=lk
  else:
   marker={"freeze_lock_version":999 if case=="wrong_version" else 1,
           "locked":case!="unlocked_marker","n_files":0,"entries":[]}
   lk.write_text(json.dumps(marker),encoding="utf-8")
  before=dst.read_bytes()
  try:outcome=convert_array_to_jsonl(src,dst,force=True)
  except Exception as ex:outcome={"exception":type(ex).__name__,"detail":str(ex)}
  r["edge_A7"][case]={"outcome":outcome,"target_changed":dst.read_bytes()!=before}
 for case,changes in [
  ("body_containers",{"problem":["p"],"solution":{"s":1}}),
  ("missing_answer",{"answer":None}),
  ("sample_id_duplicate",{}),
 ]:
  d=root/case;d.mkdir();p=d/"train.jsonl"
  if case=="sample_id_duplicate":
   recs=[clean_record(id="a",problem="first"),clean_record(id="b",problem="second")]
   for row in recs:row.pop("id");row["sample_id"]="dup"
  else:recs=[clean_record(**changes)]
  p.write_text("\n".join(json.dumps(x) for x in recs)+"\n",encoding="utf-8")
  m=Manifest(name="probe",entries=[Entry(path=p.name,sha256=sha256_file(p),size=p.stat().st_size,source="synthetic",license="internal-generated",split="train")])
  r["residual_A6"][case]={"manifest":validate_manifest(m,d),"intake":check_intake_file(p)}
r["optional_meta_type"]={}
for key,value in {"function_family":True,"visual_style":17,"efficiency_tags":"not-a-list"}.items():
 p,q=check_record(clean_record(**{key:value}),1)
 r["optional_meta_type"][key]={"problems":p,"quarantines":q}
old=json.loads((ROOT/"dataset_audit_2026-10-03-v6/summary.json").read_text(encoding="utf-8"))
r["v6_binding"]={"count":old["totals"]["pool_records_jsonl"],
 "status":old["record_status_counts"],
 "hash_mismatches":[e["file"] for e in old["per_file"] if e["format"]=="jsonl" and r["real_input_hashes"].get(e["file"])!=e["sha256"]]}
rows=[]
r["mirror_arrays"]={}
for p in sorted((ROOT/"data/v1/raw").glob("*.jsonl")):
 parsed=[json.loads(s) for s in p.read_text(encoding="utf-8").splitlines() if s.strip()]
 rows+=parsed
 r["mirror_arrays"][p.name]=parsed==json.loads((ROOT/p.name.replace(".jsonl",".json")).read_text(encoding="utf-8"))
doc=[json.loads(s) for s in (ROOT/"dataset.md").read_text(encoding="utf-8").splitlines() if s.strip()]
r["doc_matches"]= {x["id"]:x for x in doc}=={x["id"]:x for x in rows}
r["record_snapshot"]={x["id"]:x for x in rows if x["id"] in ["linalg-060","linalg-066","prob-043","geom-031","linalg-058","geom-026"]}
r["source_consistent"]={name:sha256_file(ROOT/name)==digest for name,digest in r["source_hashes"].items()}
r["real_still_unchanged"]={name:sha256_file(ROOT/name)==digest for name,digest in r["real_input_hashes"].items()}
out=pathlib.Path(__file__).with_name("results.json")
out.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"head":r["head"],"A7_target_changed":{k:v["target_changed"] for k,v in r["edge_A7"].items()},
 "A6_manifest_passes":{k:v["manifest"]["ok"] for k,v in r["residual_A6"].items()},
 "v6_binding":r["v6_binding"],"mirror_arrays":r["mirror_arrays"],"doc_matches":r["doc_matches"],
 "source_consistent":all(r["source_consistent"].values()),"real_unchanged":all(r["real_still_unchanged"].values())},ensure_ascii=False,indent=2))
