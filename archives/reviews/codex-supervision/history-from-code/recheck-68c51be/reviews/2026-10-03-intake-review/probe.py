"""Synthetic negatives and read-only current dataset snapshot."""
from pathlib import Path
import hashlib, importlib.util, json, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
sys.path.insert(0,str(ROOT/"src"))
from animtrain.dataset_intake import check_intake_file,intake_report,convert_array_to_jsonl
from animtrain.manifest import Manifest
from animtrain.validate import validate_manifest
from tests.test_dataset_intake import clean_record, write_jsonl
r={"head":subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()}
actual=sorted((ROOT/"data/v1/raw").glob("*.jsonl"))
r["input_hashes"]={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in actual}
r["current_intake"]=intake_report(actual)
mp=ROOT/"data/v1/manifest.json"
r["current_manifest"]=validate_manifest(Manifest.load(mp),mp.parent)
summary=json.loads((ROOT/"dataset_audit_2026-10-03-current/summary.json").read_text(encoding="utf-8"))
r["previous_audit_binding"]={"reported_count":summary["totals"]["pool_records_jsonl"],
  "hash_mismatches":[e["file"] for e in summary["per_file"] if e["format"]=="jsonl"
    and e["sha256"]!=r["input_hashes"].get(e["file"])]}
spec=importlib.util.spec_from_file_location("intake_cli",ROOT/"tools/dataset_intake.py")
cli=importlib.util.module_from_spec(spec); spec.loader.exec_module(cli)
with tempfile.TemporaryDirectory(prefix="codex-intake-probe-") as td:
 p=Path(td)
 empty=p/"empty.jsonl";empty.write_text("",encoding="utf-8")
 r["empty"]=check_intake_file(empty)
 r["empty_list"]=intake_report([])
 a,b=p/"a.jsonl",p/"b.jsonl"
 write_jsonl(a,[clean_record(id="same")]);write_jsonl(b,[clean_record(id="same",problem="different problem")])
 r["cross_file_duplicate"]=intake_report([a,b])
 r["invalid_values"]={}
 for key,val in {"id":["bad"],"problem":["bad"],"scene_spec":{"wrong":"shape"}}.items():
  f=p/(key+".jsonl");write_jsonl(f,[clean_record(**{key:val})])
  r["invalid_values"][key]=check_intake_file(f)
 src=p/"source.json";src.write_text(json.dumps([clean_record()],ensure_ascii=False),encoding="utf-8")
 before=src.read_bytes()
 try: outcome=convert_array_to_jsonl(src,src,force=True)
 except (Exception,SystemExit) as exc:outcome={"exception":type(exc).__name__,"detail":str(exc)}
 r["convert_same_input"]={"outcome":outcome,"input_changed":src.read_bytes()!=before}
 report=p/"report_input.jsonl";write_jsonl(report,[clean_record()])
 before=report.read_bytes()
 rc=cli.main(["report",str(report),"--out",str(report),"--force"])
 r["report_same_input"]={"exit_code":rc,"input_changed":report.read_bytes()!=before}
r["inputs_unchanged"]={p.relative_to(ROOT).as_posix():hashlib.sha256(p.read_bytes()).hexdigest()==r["input_hashes"][p.relative_to(ROOT).as_posix()] for p in actual}
out=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name("before.json")
out.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({"current_n":r["current_intake"]["n_records"],"manifest_ok":r["current_manifest"]["ok"],
  "manifest_uncalibrated":not r["current_manifest"].get("near_dup_calibrated",False),
  "stale_audit":r["previous_audit_binding"],
  "negatives":{k:r[k]["ok"] for k in ["empty","empty_list","cross_file_duplicate"]},
  "invalid_values":{k:v["ok"] for k,v in r["invalid_values"].items()},
  "convert_changed":r["convert_same_input"]["input_changed"],"report_changed":r["report_same_input"]["input_changed"]},ensure_ascii=False,indent=2))
