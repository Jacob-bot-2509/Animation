"""Read-only audit of named historical receipts. Never launches a collector or scene."""
from pathlib import Path
import ast, collections, datetime as dt, hashlib, json, stat, sys

ROOT = Path(r"D:\Animation-Model-Training")
sys.path.insert(0, str(ROOT / "src"))
from animtrain import sandbox_execution as se, isolation_evidence as ie, full_surface_evidence as fs

def safe(path):
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    if ".." in p.parts or not p.is_relative_to(ROOT):
        raise ValueError("Out-of-project evidence")
    for q in (p, *p.parents):
        info = q.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError("Reparse evidence")
        if q == ROOT: break
    return p

def bound(path):
    p=safe(path);b=p.read_bytes()
    return {"path":p.relative_to(ROOT).as_posix(),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}

def load(path):
    return json.loads(safe(path).read_text(encoding="utf-8-sig"))

def mismatch(old,current):
    return [{"path":k,"recorded":old.get(k),"current":current.get(k)}
            for k in sorted(set(old)|set(current)) if old.get(k)!=current.get(k)]

def attempt(call):
    try: return {"status":"CHECKED","value":call()}
    except Exception as e: return {"status":"UNVERIFIED","reason":type(e).__name__+": "+str(e)}

current={name:se.digest(safe(name)) for name in se.BOUND_FILES}
source_inventory=load(sys.argv[1])
out={"schema":"bounded-readonly-native-evidence-audit-v1","checked_at":dt.datetime.now(dt.timezone(dt.timedelta(hours=8))).isoformat(),
     "scope":"HISTORICAL_BYTES_AND_RECORDED_PARENT_FIELDS_ONLY_NOT_FRESH_OS_EXPERIMENT",
     "production":"CLOSED","certificate_written":False,"current_bindings":current,
     "source_inventory":bound(sys.argv[1]),"inventory_binding_checks":[],"expanded_index":[],
     "additional_surface_raws":[],"additional_checkpoints":[],"historical_runs":[],"transports":[],"media":[],
     "remote_sender_directories":[]}

for key in ("bound_files_current","collector_scripts"):
    for item in source_inventory[key]:
        actual=bound(item["path"])
        out["inventory_binding_checks"].append({**actual,"declared_sha256":item["sha256"],
                                                "matches":actual["sha256"]==item["sha256"]})
out["bound_file_set_exact"]=set(x["path"] for x in source_inventory["bound_files_current"])==set(se.BOUND_FILES)
out["required_cases_exact"]=source_inventory["work_roots_and_test_sets"]["required_cases"]==list(se.REQUIRED_CASES)

raws={}
for row in source_inventory["existing_raw_receipts_index"]:
    paths=sorted(ROOT.glob(row["path"])) if "*" in row["path"] else [ROOT/row["path"]]
    entry={"pattern":row["path"],"declared_count":row.get("count"),"actual_count":len(paths),"members":[]}
    for p in paths:
        safe(p)
        if p.is_dir():
            members=[bound(q) for q in sorted(p.iterdir()) if q.is_file()]
            item={"path":p.relative_to(ROOT).as_posix(),"files":members}
            entry["members"].append(item)
            if p.name.startswith("remote-"):
                sender=load(p/"sender.json")
                item["sender_schema"]=sender.get("schema")
                item["qualification"]="SENDER_BYTES_INDEXED_NOT_NEW_DOUBLE_ENDPOINT_PROOF"
                out["remote_sender_directories"].append(item)
        else:
            b=bound(p)
            if row.get("sha256"):b["declared_hash_matches"]=b["sha256"]==row["sha256"]
            entry["members"].append(b)
            if p.suffix==".json":raws[p]=load(p)
    out["expanded_index"].append(entry)

surface=ROOT/"reviews/codex-supervision/2026-10-06-all43-sandbox-repair"
for p in sorted(surface.glob("surface-raw-*.json")):
    out["additional_surface_raws"].append(bound(p));raws[p]=load(p)
for p in sorted(surface.glob("checkpoint-*.json")):
    if p not in raws:
        out["additional_checkpoints"].append(bound(p));raws[p]=load(p)

seen_cp=set();seen_media=set()
def walk(obj, path, location="$"):
    if isinstance(obj,dict):
        if "parent_evidence" in obj and "work" in obj:
            key=(obj["work"],obj.get("source_sha256"))
            if key not in seen_cp:
                seen_cp.add(key)
                work=safe(obj["work"])
                parent=attempt(lambda:ie._parent(obj["parent_evidence"]))
                rec={"work":str(work.relative_to(ROOT)).replace("\\","/"),"first_receipt":path.relative_to(ROOT).as_posix(),
                     "location":location,"recorded_parent_fields_and_storage_absence":parent,
                     "current_os_acl_retested":False,"original_files":[]}
                for name in ("scene.py","stdout.txt","stderr.txt"):
                    p=work/name
                    rec["original_files"].append(attempt(lambda p=p:bound(p)))
                if "source_sha256" in obj:
                    rec["source_hash_matches"]=attempt(lambda:se.digest(safe(work/"scene.py"))==obj["source_sha256"])
                for name in ("stdout","stderr"):
                    if isinstance(obj.get(name),str):
                        rec[name+"_matches_raw_file"]=attempt(lambda name=name: safe(work/(name+".txt")).read_bytes().decode("utf-8","replace")==obj[name])
                rec["recorded_rc"]=obj.get("rc")
                out["transports"].append(rec)
        if set(("path","sha256","size","frames","width","height","frame_rate"))<=set(obj):
            key=obj["path"]
            if key not in seen_media:
                seen_media.add(key)
                p=safe(key)
                # PyAV decodes existing local media only, never scene Python.
                actual=attempt(lambda:se.decode_video(p))
                out["media"].append({"expected":obj,"actual_decode":actual,
                                     "exact_receipt_match":actual.get("value")==obj})
        for k,v in obj.items():walk(v,path,location+"."+str(k))
    elif isinstance(obj,list):
        for i,v in enumerate(obj):walk(v,path,location+"["+str(i)+"]")

for path,raw in sorted(raws.items()):
    schema=raw.get("schema")
    if schema not in ("production-joint-raw-v1","sandbox-surface-native-v1"):
        continue
    old=raw.get("implementation_sha256",raw.get("initial_bindings",{}))
    run={"binding":bound(path),"schema":schema,"recorded_case_count":len(raw.get("cases",raw.get("records",{}))),
         "implementation_differences":mismatch(old,current),"has_final_bindings":"final_bindings" in raw,
         "final_equals_initial":raw.get("final_bindings")==raw.get("initial_bindings") if "final_bindings" in raw else None,
         "implementation_unchanged_recorded":raw.get("implementation_unchanged"),
         "error_key_present":"error" in raw,"recorded_error":raw.get("error"),
         "current_transport_acceptance":"NOT_ESTABLISHED"}
    if schema=="sandbox-surface-native-v1":
        result=attempt(lambda:fs.recompute(raw))
        run["current_recompute"]=result
        if result["status"]=="CHECKED":
            run["current_counts"]=dict(collections.Counter(v["status"] for v in result["value"].values()))
    else:
        # Original strict judge is read-only, may stop at first invalid/missing record.
        run["strict_original_judge"]=attempt(lambda:ie.judge(raw,lambda p:se.digest(safe(p)),lambda p:se.decode_video(safe(p))))
    out["historical_runs"].append(run)
    walk(raw,path)

out["summary"]={"inventory_bindings_match":all(x["matches"] for x in out["inventory_binding_checks"]),
    "joint_raw_count":sum(x["schema"]=="production-joint-raw-v1" for x in out["historical_runs"]),
    "surface_raw_and_checkpoints":sum(x["schema"]=="sandbox-surface-native-v1" for x in out["historical_runs"]),
    "unique_recorded_transports":len(out["transports"]),"decoded_media":len(out["media"]),
    "media_exact_matches":sum(x["exact_receipt_match"] for x in out["media"]),
    "parent_record_field_checks_pass":sum(x["recorded_parent_fields_and_storage_absence"]["status"]=="CHECKED" for x in out["transports"]),
    "transport_source_hash_mismatch_or_missing":sum(x.get("source_hash_matches",{}).get("value") is not True for x in out["transports"]),
    "remote_sender_count":len(out["remote_sender_directories"]),
    "execution_certificate_exists":(ROOT/"data/execution_evidence.json").exists()}
print(json.dumps(out,ensure_ascii=False,indent=2))
