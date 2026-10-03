"""Independent recheck for msgs 185/192; no training or dataset mutation."""
import importlib.util,json,pathlib,sys,tempfile
import sympy as sp
ROOT=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/"src"))
from animtrain.dataset_intake import check_intake_file,check_record
from animtrain.manifest import Entry,Manifest,sha256_file
from animtrain.validate import validate_manifest
from tests.test_dataset_intake import clean_record
spec=importlib.util.spec_from_file_location("base_review",ROOT/"reviews/2026-10-03-global-code-review/probe.py")
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
r=base.run()
r["baseline_tests"]={"stable_1c9d332":213,"codex_answer_guard":215,"stable_602c792":223,"subtests":29,"latest_seconds":6.76}
r["answer_container_tests_before"]={"failed":2}
r["A6_remaining_recheck"]={}
with tempfile.TemporaryDirectory(prefix="codex-final-gate-") as tmp:
 root=pathlib.Path(tmp)
 for case,changes in [("body_containers",{"problem":["p"],"solution":{"s":1}}),
   ("missing_answer",{"answer":None}),("answer_list",{"answer":["4"]}),
   ("answer_dict",{"answer":{"value":"4"}}),("sample_id_duplicate",{})]:
  d=root/case;d.mkdir();p=d/"train.jsonl"
  if case=="sample_id_duplicate":
   rows=[clean_record(id="a",problem="first"),clean_record(id="b",problem="second")]
   for row in rows:row.pop("id");row["sample_id"]="dup"
  else:rows=[clean_record(**changes)]
  p.write_text("\n".join(json.dumps(x) for x in rows)+"\n",encoding="utf-8")
  manifest=Manifest(name="synthetic-review",entries=[Entry(path=p.name,sha256=sha256_file(p),size=p.stat().st_size,source="synthetic-review",license="internal-generated",split="train")])
  r["A6_remaining_recheck"][case]={"manifest":validate_manifest(manifest,d),"intake":check_intake_file(p)}
r["B7_metadata_types"]={}
for key,val in {"function_family":True,"visual_style":17,"efficiency_tags":"not-a-list"}.items():
 p,q=check_record(clean_record(**{key:val}),1)
 r["B7_metadata_types"][key]={"problems":p,"quarantines":q}
rows=[]
r["mirror_arrays"]={}
for p in sorted((ROOT/"data/v1/raw").glob("*.jsonl")):
 parsed=[json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
 rows+=parsed
 r["mirror_arrays"][p.name]=parsed==json.loads((ROOT/p.name.replace(".jsonl",".json")).read_text(encoding="utf-8"))
doc=[json.loads(x) for x in (ROOT/"dataset.md").read_text(encoding="utf-8").splitlines() if x.strip()]
r["doc_matches"]={x["id"]:x for x in doc}=={x["id"]:x for x in rows}
summary=json.loads((ROOT/"dataset_audit_2026-10-03-v7/summary.json").read_text(encoding="utf-8"))
r["v7_binding"]={"count":summary["totals"]["pool_records_jsonl"],"record_status":summary["record_status_counts"],
 "hash_mismatches":[e["file"] for e in summary["per_file"] if e["format"]=="jsonl" and r["real_input_hashes"].get(e["file"])!=e["sha256"]]}
wanted=["linalg-049","linalg-052","linalg-054","linalg-057","linalg-064","linalg-068","prob-046"]
r["answer_record_snapshot"]={x["id"]:x for x in rows if x["id"] in wanted}
a=sp.Matrix([[2,1],[1,2]]);v1=sp.Matrix([1,1]);v2=sp.Matrix([1,-1])
b=sp.Matrix([[3,1],[0,2]]);inv=sp.Matrix([[1,-1],[-1,2]])
q=sp.Matrix([[1,1],[1,-1]])/sp.sqrt(2)
x=sp.Symbol("x");k=sp.Symbol("k",integer=True,positive=True)
r["independent_math"]={
 "linalg-049_eigen_residuals":[str(a*v1-3*v1),str(a*v2-v2)],
 "linalg-052_taylor_difference":str(sp.expand(x**3-(1+3*(x-1)+3*(x-1)**2+(x-1)**3))),
 "linalg-054_solution":str(sp.Matrix([[2,1],[1,-1]]).inv()*sp.Matrix([5,1])),
 "linalg-057_inverse_product":str(sp.Matrix([[2,1],[1,1]])*inv),
 "linalg-064_eigen_residuals":[str(b*sp.Matrix([1,0])-3*sp.Matrix([1,0])),str(b*v2-2*v2)],
 "linalg-068_orthogonal":str(sp.simplify(q.T*q)),
 "linalg-068_diagonal":str(sp.simplify(q.T*a*q)),
 "prob-046_geometric_series":str(sp.summation(sp.Rational(1,2)**k,(k,1,sp.oo)))}
mp=ROOT/"data/v1/manifest-train.json"
r["train_manifest"]={"sha256":sha256_file(mp),"report":validate_manifest(Manifest.load(mp),mp.parent),
 "splits":[e.split for e in Manifest.load(mp).entries]}
r["raw_manifest_sha256"]=sha256_file(ROOT/"data/v1/manifest.json")
r["prep_template_sha256"]=sha256_file(ROOT/"train_config.template.json")
r["prep_plan_sha256"]=sha256_file(ROOT/"TRAIN_PREP_PLAN.md")
r["preflight_observation"]={"command":"tools/preflight.py --ready --run-id prep-check-0001 --manifest data/v1/manifest-train.json",
 "exit_code":1,"ready":False,"passed":["gpu","data_manifest","render_gate","math_gate"],
 "failed":["model_dir","run_snapshot","near_dup_calibrated","freeze_gate"],
 "scope":"Fixed trusted environmental smoke only; no training"}
r["source_consistent"]={name:sha256_file(ROOT/name)==digest for name,digest in r["source_hashes"].items()}
r["real_inputs_consistent"]={name:sha256_file(ROOT/name)==digest for name,digest in r["real_input_hashes"].items()}
out=pathlib.Path(__file__).with_name("results.json")
out.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"head":r["head"],"A6_exits":{k:v["manifest"]["exit_code"] for k,v in r["A6_remaining_recheck"].items()},
 "empty_fields_cli":r["G1_entry_disagreement"]["empty.jsonl"]["fields_cli"]["exit_code"],
 "B7_rejected":{k:bool(v["problems"]) for k,v in r["B7_metadata_types"].items()},
 "v7_binding":r["v7_binding"],"train_manifest_ok":r["train_manifest"]["report"]["ok"],
 "mirror_arrays":r["mirror_arrays"],"doc_matches":r["doc_matches"],
 "source_consistent":all(r["source_consistent"].values()),"real_unchanged":all(r["real_inputs_consistent"].values())},ensure_ascii=False,indent=2))
