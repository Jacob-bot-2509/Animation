"""Post-fix supervision probes. All effects confined to disposable directories."""
import json,hashlib,sys,tempfile
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"src"))
from animtrain.publish import publish_files,recover_publish,journal_path,BACKUP_SUFFIX,PublishCleanupError
from animtrain.freeze import freeze_set
from animtrain.manifest import Manifest,canonical_problem_hash
from animtrain.validate import validate_manifest
from animtrain.preflight import check_asset_evidence
results=[]
def case(name,fn):
    try:r=fn()
    except Exception as exc:r={"exception":repr(exc)}
    results.append({"case":name,**r})
def interrupted_cleanup():
    with tempfile.TemporaryDirectory() as td:
        d=Path(td);a=d/"a.txt";b=d/"b.txt";a.write_text("oldA");b.write_text("oldB")
        real=Path.unlink;hit=False
        def unlink(p,*args,**kw):
            nonlocal hit
            if p==Path(str(b)+BACKUP_SUFFIX) and not hit:
                hit=True;raise OSError("injected cleanup failure after first backup deletion")
            return real(p,*args,**kw)
        with patch.object(Path,"unlink",unlink):
            try:publish_files(d,"g",[(a,"newA"),(b,"newB")],force=True)
            except PublishCleanupError:pass
        before=[a.read_text(),b.read_text()]
        rep=recover_publish(d,"g")
        return {"expected":"cleanup recovery keeps committed group intact","before":before,"after":[a.read_text(),b.read_text()],"report":rep}
def partial_backup():
    with tempfile.TemporaryDirectory() as td:
        d=Path(td);a=d/"a.txt";a.write_text("COMPLETE ORIGINAL")
        real=Path.write_bytes
        def write(p,data):
            if p==Path(str(a)+BACKUP_SUFFIX):
                real(p,b"PARTIAL")
                raise OSError("injected interrupted backup write")
            return real(p,data)
        with patch.object(Path,"write_bytes",write):
            try:publish_files(d,"g",[(a,"new")],force=True)
            except OSError:pass
        return {"expected":"failed backup creation cannot damage intact original","after":a.read_text(),"journal_remains":journal_path(d,"g").exists()}
def crossing_backup():
    with tempfile.TemporaryDirectory() as td:
        d=Path(td);a=d/"a.txt";a.write_text("oldA");b=Path(str(a)+BACKUP_SUFFIX)
        rep=publish_files(d,"g",[(a,"newA"),(b,"newB")],force=True)
        return {"expected":"target cannot equal another target's backup","returned_count":len(rep),"a":a.read_text(),"b_exists":b.exists()}
def crossing_journal():
    with tempfile.TemporaryDirectory() as td:
        d=Path(td);a=journal_path(d,"g")
        rep=publish_files(d,"g",[(a,"requested artifact")],force=True)
        return {"expected":"target cannot equal transaction journal","returned_count":len(rep),"target_exists":a.exists()}
def frozen_new_file():
    with tempfile.TemporaryDirectory() as td:
        d=Path(td);a=d/"new.jsonl";a.write_text("frozen now");freeze_set([a],d/"f.lock.json")
        jp=journal_path(d,"g");jp.write_text(json.dumps({"group":"g","stage":"writing","committed":[str(a)],"items":[{"path":str(a),"backup":str(a)+BACKUP_SUFFIX,"existed_before":False}]}))
        rep=recover_publish(d,"g")
        return {"expected":"all recovery mutations respect current freeze protection","target_exists":a.exists(),"journal_remains":jp.exists(),"report":rep}
def malformed_empty():
    with tempfile.TemporaryDirectory() as td:
        d=Path(td);jp=journal_path(d,"g");jp.write_text("{}")
        rep=recover_publish(d,"g")
        return {"expected":"empty/missing-schema journal rejected and preserved","journal_remains":jp.exists(),"report":rep}
def interrupted_recovery():
    with tempfile.TemporaryDirectory() as td:
        d=Path(td);a=d/"a.txt";b=d/"b.txt";a.write_text("newA");b.write_text("newB")
        ba=Path(str(a)+BACKUP_SUFFIX);bb=Path(str(b)+BACKUP_SUFFIX);ba.write_text("oldA");bb.write_text("oldB")
        jp=journal_path(d,"g");jp.write_text(json.dumps({"group":"g","stage":"writing","committed":[str(a),str(b)],"items":[{"path":str(t),"backup":str(t)+BACKUP_SUFFIX,"existed_before":True} for t in [a,b]]}))
        real=Path.replace
        def replace(p,target):
            if p==bb:raise OSError("injected recovery interruption after first restore")
            return real(p,target)
        with patch.object(Path,"replace",replace):
            try:recover_publish(d,"g")
            except OSError:pass
        rep=recover_publish(d,"g")
        return {"expected":"recovery retry completes and removes valid journal","after":[a.read_text(),b.read_text()],"journal_remains":jp.exists(),"report":rep}
def asset_binding(change):
    with tempfile.TemporaryDirectory() as td:
        d=Path(td);r=json.loads((ROOT/"reviews/fixtures-eval-test/eval_ok.jsonl").read_text(encoding="utf-8"));line=json.dumps(r,ensure_ascii=False);proof=canonical_problem_hash(line)
        if change:r["solution"]="Changed solution";r["scene_spec"]["steps"]=["Changed animation plan"]
        data=d/"train.jsonl";data.write_text(json.dumps(r,ensure_ascii=False)+"\n",encoding="utf-8")
        mp=d/"manifest.json";mp.write_text(json.dumps({"name":"synthetic","version":1,"entries":[{"path":data.name,"split":"train","sha256":hashlib.sha256(data.read_bytes()).hexdigest(),"size":data.stat().st_size,"source":"synthetic","license":"internal-generated"}]}),encoding="utf-8")
        evidence={"manifest_sha256":hashlib.sha256(mp.read_bytes()).hexdigest(),"n_total_records":1,"n_verified_assets":1,"records":{r["id"]:{"input_sha256":proof,"output_sha256":"no-artifact-exists","math":"verified","render":"rendered"}}}
        (d/"asset_evidence.json").write_text(json.dumps(evidence),encoding="utf-8")
        gate=validate_manifest(Manifest.load(mp),d);ok,detail=check_asset_evidence(mp)
        return {"expected":"evidence requires full record input binding and real output verification","data_gate_exit":gate["exit_code"],"asset_gate_ok":ok,"detail":detail}
for name,fn in [("cleanup_recovery_mixes_versions",interrupted_cleanup),("partial_backup_overwrites_original",partial_backup),("target_backup_cross_collision",crossing_backup),("target_journal_collision",crossing_journal),("new_file_recovery_deletes_frozen",frozen_new_file),("empty_journal_false_recovered",malformed_empty),("interrupted_recovery_not_idempotent",interrupted_recovery),("asset_nonexistent_artifact",lambda:asset_binding(False)),("asset_changed_solution_and_scene",lambda:asset_binding(True))]:case(name,fn)
paths=["src/animtrain/publish.py","src/animtrain/preflight.py","src/animtrain/run_record.py","src/animtrain/win_job.py"]
doc={"source_hashes":{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths},"results":results}
(Path(__file__).parent/"results.json").write_text(json.dumps(doc,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(doc,ensure_ascii=False,indent=2))
