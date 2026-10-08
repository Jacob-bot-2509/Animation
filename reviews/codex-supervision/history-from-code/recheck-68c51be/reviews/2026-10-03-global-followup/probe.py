"""Read-only global review probes; all mutations use disposable synthetic data."""
import hashlib,json,sys,tempfile,subprocess
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"src"))
from animtrain.publish import publish_files,recover_publish,journal_path,BACKUP_SUFFIX
from animtrain.freeze import freeze_set
from animtrain.preflight import check_asset_evidence,run_preflight
results=[]
def case(name,fn):
    try: result=fn()
    except Exception as e: result={"unexpected_exception":repr(e)}
    results.append({"case":name,**result})
def crash_new():
    with tempfile.TemporaryDirectory() as td:
        d=Path(td); a=d/"new.txt"; a.write_text("partial")
        jp=journal_path(d,"g")
        jp.write_text(json.dumps({"group":"g","items":[{"path":str(a),"backup":str(a)+BACKUP_SUFFIX}]}))
        rep=recover_publish(d,"g")
        return {"expected":"rollback removes newly-created file","target_remains":a.exists(),"journal_remains":jp.exists(),"report":rep}
def cleanup_failure():
    with tempfile.TemporaryDirectory() as td:
        d=Path(td);a=d/"a.txt";b=d/"b.txt"
        a.write_text("oldA");b.write_text("oldB")
        original=Path.unlink; failed=False
        def unlink(p,*args,**kw):
            nonlocal failed
            if p==Path(str(b)+BACKUP_SUFFIX) and not failed:
                failed=True;raise OSError("injected backup cleanup failure")
            return original(p,*args,**kw)
        try:
            with patch.object(Path,"unlink",unlink):
                publish_files(d,"g",[(a,"newA"),(b,"newB")],force=True)
        except OSError: pass
        return {"expected":"both original files preserved or committed together","a":a.read_text() if a.exists() else None,"b":b.read_text() if b.exists() else None,"journal_remains":journal_path(d,"g").exists()}
def backup_collision():
    with tempfile.TemporaryDirectory() as td:
        d=Path(td);a=d/"new.txt";bak=Path(str(a)+BACKUP_SUFFIX);bak.write_text("unrelated retained data")
        publish_files(d,"g",[(a,"new")])
        return {"expected":"existing backup collision rejected without deletion","backup_preserved":bak.exists(),"target_created":a.exists()}
def frozen_recover():
    with tempfile.TemporaryDirectory() as td:
        d=Path(td);a=d/"frozen.jsonl";a.write_text("frozen");freeze_set([a],d/"f.lock.json")
        bak=Path(str(a)+BACKUP_SUFFIX);bak.write_text("different")
        journal_path(d,"g").write_text(json.dumps({"group":"g","items":[{"path":str(a),"backup":str(bak)}]}))
        rep=recover_publish(d,"g")
        return {"expected":"frozen target must not change","target":a.read_text(),"report":rep}
def corrupt_journal():
    with tempfile.TemporaryDirectory() as td:
        d=Path(td);jp=journal_path(d,"g");jp.write_text("{broken")
        rep=recover_publish(d,"g")
        return {"expected":"reject malformed journal and keep recovery evidence","journal_preserved":jp.exists(),"report":rep}
def duplicate_target():
    with tempfile.TemporaryDirectory() as td:
        d=Path(td);a=d/"a.txt";a.write_text("old")
        bad=d/"bad";bad.mkdir()
        try: publish_files(d,"g",[(a,"first"),(a,"second"),(bad,"x")],force=True)
        except OSError: pass
        return {"expected":"reject duplicate target or preserve original on rollback","target":a.read_text() if a.exists() else None}
def asset_count():
    with tempfile.TemporaryDirectory() as td:
        d=Path(td); data=d/"train.jsonl"
        record=json.loads((ROOT/"reviews/fixtures-eval-test/eval_ok.jsonl").read_text(encoding="utf-8"))
        rows=[{**record,"id":sid,"problem":"Synthetic independent algebra task "+sid} for sid in ("a","b","c")]
        data.write_text("\n".join(json.dumps(row,ensure_ascii=False) for row in rows)+"\n",encoding="utf-8")
        mp=d/"manifest.json";mp.write_text(json.dumps({"name":"synthetic","entries":[{"path":data.name,"split":"train","sha256":hashlib.sha256(data.read_bytes()).hexdigest(),"size":data.stat().st_size,"source":"synthetic","license":"internal-generated"}]}))
        ep=d/"asset_evidence.json";ep.write_text(json.dumps({"manifest_sha256":hashlib.sha256(mp.read_bytes()).hexdigest(),"n_verified_assets":1,"n_total_records":1}))
        from animtrain.manifest import Manifest
        from animtrain.validate import validate_manifest
        data_result=validate_manifest(Manifest.load(mp),d)
        ok,detail=check_asset_evidence(mp)
        return {"data_gate_exit":data_result["exit_code"],"expected":"3 records without per-asset evidence must not pass as 1/1","accepted":ok,"detail":detail}
def ready_missing():
    with patch("animtrain.preflight.check_gpu",return_value=(True,"mock")),patch("animtrain.preflight.check_model_dir",return_value=(True,"mock")):
        rep=run_preflight(Path("."),[("data_manifest",(True,"mock")),("run_snapshot",(True,"mock"))],ready=True)
    return {"expected":"missing asset/freeze/calibration/isolation checks block READY","ready":rep["ready"],"checks":[c["check"] for c in rep["checks"]]}
def eval_run(name):
    with tempfile.TemporaryDirectory() as td:
        d=Path(td);candidate=d/"candidate";candidate.mkdir();train=d/"train";train.mkdir()
        record=json.loads((ROOT/"reviews/fixtures-eval-test/eval_ok.jsonl").read_text(encoding="utf-8"))
        (train/"train.jsonl").write_text((ROOT/"reviews/fixtures-eval-test/train_synthetic.jsonl").read_text(encoding="utf-8"),encoding="utf-8")
        if name=="schema":
            record.pop("id"); record.update(problem_id="ep1",solution_id="ep1-s1",method="m1")
        (candidate/"a.jsonl").write_text(json.dumps(record,ensure_ascii=False)+"\n",encoding="utf-8")
        if name=="duplicates":
            another={**record,"problem":"Entirely new geometry problem: classify conic sections."}
            (candidate/"b.jsonl").write_text(json.dumps(another)+"\n",encoding="utf-8")
        tr=train if name!="missing_train" else d/"does-not-exist"
        cp=subprocess.run([sys.executable,"-X","utf8",str(ROOT/"tools/eval_test_prep.py"),"check",str(candidate),"--train-dir",str(tr)],capture_output=True,encoding="utf-8")
        return {"expected":{"schema":"documented eval schema accepted","duplicates":"cross-file duplicate IDs rejected","missing_train":"missing reference train blocks isolation PASS"}[name],"exit_code":cp.returncode,"stdout":cp.stdout,"stderr":cp.stderr}
for n,fn in [("publish_crash_new_file",crash_new),("publish_cleanup_failure",cleanup_failure),("publish_backup_collision",backup_collision),("publish_recover_frozen",frozen_recover),("publish_corrupt_journal",corrupt_journal),("publish_duplicate_target",duplicate_target),("asset_self_reported_coverage",asset_count),("ready_missing_required_gates",ready_missing)]:
    case(n,fn)
for n in ("schema","duplicates","missing_train"):case("eval_"+n,lambda n=n:eval_run(n))
paths=["src/animtrain/publish.py","src/animtrain/preflight.py","src/animtrain/render_gate.py","tools/eval_test_prep.py","tools/preflight.py"]
out={"source_hashes":{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},"results":results}
(Path(__file__).parent/"results.json").write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(out,ensure_ascii=False,indent=2))
