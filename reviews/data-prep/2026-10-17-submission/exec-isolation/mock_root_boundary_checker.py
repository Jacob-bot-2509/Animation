"""Fixture-only root policy model v2. No filesystem authority or native execution."""
from __future__ import annotations
import argparse, copy, datetime as dt, hashlib, json, re
from pathlib import Path

SCHEMA = "exec-native-roots-v2"
PREFIX = "reviews/exec-native/"
HEX = re.compile(r"[0-9a-f]{64}")
ID = re.compile(r"[a-z0-9][a-z0-9_-]{0,63}")
GUID = re.compile(r"[0-9a-f]{32}")
OLD_ROOTS = (
    "reviews/codex-supervision/2026-10-05-three-gates",
    "reviews/codex-supervision/2026-10-06-all43-sandbox-repair",
    "reviews/2026-10-06-exec-isolation-full-surface")
ENTRY_KEYS = {"root_id","root_path","purpose","cohort","bound_paths","status","created_at"}
COHORT_KEYS = {"collector_sha256","verifier_sha256","bound_files_sha256_map"}
TOOLS = {"collector_sha256","verifier_sha256"}

def sha_object(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode()).hexdigest()

def relative(value):
    if type(value) is not str or not value or len(value)>1024:
        raise ValueError("R_PATH:type_or_length")
    parts=value.split("/")
    reserved={"con","prn","aux","nul",*(f"com{i}" for i in range(1,10)),*(f"lpt{i}" for i in range(1,10))}
    if any(not p or p in (".","..") or p.endswith(("."," ")) or not re.fullmatch(r"[A-Za-z0-9_.-]+",p)
           or p.split(".")[0].casefold() in reserved for p in parts):
        raise ValueError("R_PATH:noncanonical_windows_relative")
    return value

def overlaps(a,b):
    a,b=a.casefold(),b.casefold()
    return a==b or a.startswith(b+"/") or b.startswith(a+"/")

def hash_map(value):
    if type(value) is not dict or not value:
        raise ValueError("R3:empty_or_invalid_binding_map")
    names=set()
    for path,sha in value.items():
        normalized=relative(path).casefold()
        if normalized in names or type(sha) is not str or not HEX.fullmatch(sha):
            raise ValueError("R3:binding_path_or_hash")
        names.add(normalized)

def entry(value):
    if type(value) is not dict or set(value)!=ENTRY_KEYS:
        raise ValueError("R_SCHEMA:entry")
    rid=value["root_id"]
    if type(rid) is not str or not ID.fullmatch(rid):
        raise ValueError("R7:root_id")
    path=relative(value["root_path"])
    if path!=PREFIX+"run-"+rid or any(overlaps(path,old) for old in OLD_ROOTS):
        raise ValueError("R2:root_location")
    if value["purpose"] not in ("transport","surface","joint","external"):
        raise ValueError("R_SCHEMA:purpose")
    bp=value["bound_paths"]
    if type(bp) is not list or not bp or any(type(p) is not str for p in bp):
        raise ValueError("R8:bound_paths_type_or_empty")
    if len(bp)!=len(set(bp)) or not set(bp)<={"raw","work","media"}:
        raise ValueError("R8:bound_paths_not_closed")
    if value["status"] not in ("REGISTERED","ACTIVE","FROZEN"):
        raise ValueError("R7:status")
    stamp=value["created_at"]
    if type(stamp) is not str or dt.datetime.fromisoformat(stamp).utcoffset() is None:
        raise ValueError("R_SCHEMA:created_at")
    cohort=value["cohort"]
    if type(cohort) is not dict or set(cohort)!=COHORT_KEYS:
        raise ValueError("R3:cohort_schema")
    for key in TOOLS:
        if type(cohort[key]) is not str or not HEX.fullmatch(cohort[key]):
            raise ValueError("R3:tool_hash")
    hash_map(cohort["bound_files_sha256_map"])

def snapshot(reg, allow_empty=False):
    if type(reg) is not dict or set(reg)!={"schema","entries","previous_registry_sha256"} or reg["schema"]!=SCHEMA:
        raise ValueError("R_SCHEMA:registry")
    previous=reg["previous_registry_sha256"]
    if previous is not None and (type(previous) is not str or not HEX.fullmatch(previous)):
        raise ValueError("R7:previous_hash")
    rows=reg["entries"]
    if type(rows) is not list or (not rows and not allow_empty):
        raise ValueError("R1:empty_or_invalid_entries")
    ids=set();paths=[]
    for row in rows:
        entry(row)
        if row["root_id"] in ids or any(overlaps(row["root_path"],p) for p in paths):
            raise ValueError("R2_R7:duplicate_or_nested_root")
        ids.add(row["root_id"]);paths.append(row["root_path"])

def check_registry(reg,current_bound_map,*,current_tool_hashes=None,history=None,
                   existing_paths=(),reparse_paths=()):
    """Only validates supplied model facts. Caller must supply independently trusted context."""
    try:
        snapshot(reg);hash_map(current_bound_map)
        if type(current_tool_hashes) is not dict or set(current_tool_hashes)!=TOOLS:
            raise ValueError("R3:trusted_tool_pins_missing")
        if any(type(v) is not str or not HEX.fullmatch(v) for v in current_tool_hashes.values()):
            raise ValueError("R3:trusted_tool_pins_invalid")
        if history is None:
            raise ValueError("R7:trusted_history_missing")
        snapshot(history,True)
        if reg["previous_registry_sha256"]!=sha_object(history):
            raise ValueError("R7:history_hash")
        old={e["root_id"]:e for e in history["entries"]}
        new={e["root_id"]:e for e in reg["entries"]}
        if not old.keys()<=new.keys():
            raise ValueError("R7:history_deleted")
        existing=[relative(p) for p in existing_paths]
        reparses=[relative(p) for p in reparse_paths]
        transitions={("REGISTERED","REGISTERED"),("REGISTERED","ACTIVE"),("ACTIVE","ACTIVE"),
                     ("ACTIVE","FROZEN"),("FROZEN","FROZEN")}
        for rid,e in new.items():
            path=e["root_path"]
            if rid in old:
                if any(e[k]!=old[rid][k] for k in ENTRY_KEYS-{"status"}):
                    raise ValueError("R7:historical_fields_changed")
                if (old[rid]["status"],e["status"]) not in transitions:
                    raise ValueError("R7:status_transition")
            else:
                if e["status"]!="REGISTERED":
                    raise ValueError("R7:new_root_must_be_registered")
                # Existing containers are permitted; a new target itself or its descendants are not.
                if any(p.casefold()==path or p.casefold().startswith(path+"/") for p in existing):
                    raise ValueError("R2:existing_target_or_descendant")
            if any(path.casefold()==p.casefold() or path.casefold().startswith(p.casefold()+"/") for p in reparses):
                raise ValueError("R_PATH:reparse_ancestor")
            # Frozen historical cohorts keep their exact old hashes, never re-sign them as current.
            if e["status"]!="FROZEN":
                c=e["cohort"]
                if c["bound_files_sha256_map"]!=current_bound_map or any(c[k]!=current_tool_hashes[k] for k in TOOLS):
                    raise ValueError("R3:current_cohort_mismatch")
        return []
    except (ValueError,TypeError,KeyError,AttributeError) as exc:
        return [str(exc) or "R_BAD_INPUT"]

def selected(reg,root_id,current_bound_map,context):
    if check_registry(reg,current_bound_map,**context):
        return None
    return next((e for e in reg["entries"] if e["root_id"]==root_id and e["status"]=="ACTIVE"),None)

def check_write(reg,root_id,write_rel,*,current_bound_map,writer="parent",**context):
    e=selected(reg,root_id,current_bound_map,context)
    if e is None or writer not in ("parent","child"):
        return False
    try:
        parts=relative(write_rel).split("/")
        if len(parts)<2 or parts[0] not in e["bound_paths"] or writer=="child" and parts[0]=="raw":
            return False
        full=e["root_path"]+"/"+write_rel
        return not any(full.casefold()==relative(p).casefold() or full.casefold().startswith(relative(p).casefold()+"/")
                       for p in context.get("reparse_paths",()))
    except (ValueError,TypeError):
        return False

def check_old_receipt_as_new(reg,claimed_root,*,root_id,expected_run_id,receipt,current_bound_map,**context):
    e=selected(reg,root_id,current_bound_map,context)
    if e is None:
        return False
    try:
        return (relative(claimed_root)==e["root_path"] and type(expected_run_id) is str
                and GUID.fullmatch(expected_run_id) is not None
                and type(receipt) is dict and set(receipt)=={"root_id","root_path","run_id","cohort_sha256"}
                and receipt=={"root_id":root_id,"root_path":e["root_path"],"run_id":expected_run_id,
                              "cohort_sha256":sha_object(e["cohort"])})
    except (ValueError,TypeError):
        return False

def check_reuse(used_jobs,cohort_id,job_id=None):
    """Single-process model reservation only; not durable or concurrent native protection."""
    if type(used_jobs) is not set or type(cohort_id) is not str or not HEX.fullmatch(cohort_id):
        return False
    if type(job_id) is not str or not GUID.fullmatch(job_id):
        return False
    if any(type(k) is not tuple or len(k)!=2 or type(k[0]) is not str or not HEX.fullmatch(k[0])
           or type(k[1]) is not str or not GUID.fullmatch(k[1]) for k in used_jobs):
        return False
    key=(cohort_id,job_id)
    if key in used_jobs:
        return False
    used_jobs.add(key)
    return True

def fixture(active=False):
    """Synthetic pins and timestamps, never actual production authorization."""
    bounds={"src/mock.py":"c"*64};tools={"collector_sha256":"a"*64,"verifier_sha256":"b"*64}
    genesis={"schema":SCHEMA,"entries":[],"previous_registry_sha256":None}
    reg={"schema":SCHEMA,"previous_registry_sha256":sha_object(genesis),"entries":[{
        "root_id":"n001","root_path":PREFIX+"run-n001","purpose":"surface","cohort":{**tools,"bound_files_sha256_map":bounds},
        "bound_paths":["raw","work","media"],"status":"REGISTERED","created_at":"2026-01-01T00:00:00+00:00"}]}
    history=genesis
    if active:
        history=copy.deepcopy(reg);reg["previous_registry_sha256"]=sha_object(history);reg["entries"][0]["status"]="ACTIVE"
    return reg,bounds,{"current_tool_hashes":tools,"history":history,"existing_paths":(),"reparse_paths":()}

def fixture_matrix():
    reg,bounds,ctx=fixture(True);checks=[]
    def check(name,value):checks.append({"name":name,"ok":value is True})
    check("valid-active",check_registry(reg,bounds,**ctx)==[])
    check("unregistered-id",not check_write(reg,"missing","raw/x.json",current_bound_map=bounds,**ctx))
    for name,path in (("traversal","../x"),("absolute","/x"),("drive","C:/x"),("ads","raw/x:ads"),("backslash",r"raw\..\x"),("device","raw/NUL.txt")):
        check("R4-"+name,not check_write(reg,"n001",path,current_bound_map=bounds,**ctx))
    bad=copy.deepcopy(reg);bad["entries"][0]["status"]="FROZEN"
    check("frozen-write",not check_write(bad,"n001","raw/x",current_bound_map=bounds,**ctx))
    check("child-cannot-write-parent-evidence",not check_write(reg,"n001","raw/proof.json",current_bound_map=bounds,writer="child",**ctx))
    used=set();cohort=sha_object(reg["entries"][0]["cohort"])
    check("first-job",check_reuse(used,cohort,"1"*32))
    check("duplicate-job",not check_reuse(used,cohort,"1"*32))
    check("second-job-same-cohort",check_reuse(used,cohort,"2"*32))
    return checks

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--receipt",type=Path);args=parser.parse_args()
    checks=fixture_matrix();failed=[c["name"] for c in checks if not c["ok"]]
    result={"schema":"root-boundary-mock-receipt-v2","scope":"SYNTHETIC_MODEL_ONLY_NOT_NATIVE_ACCEPTANCE",
            "source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "created_at":dt.datetime.now(dt.timezone.utc).isoformat(),"scenarios":checks,
            "failed":failed,"native_execution":False,"production":"CLOSED"}
    if args.receipt:
        p=args.receipt.absolute();project=Path(r"D:\Animation-Model-Training")
        if ".." in p.parts or not p.is_relative_to(project):
            raise ValueError("Receipt must stay in project")
        relative(p.relative_to(project).as_posix())
        for q in (p,*p.parents):
            if q.exists():
                s=q.lstat()
                if q.is_symlink() or getattr(s,"st_file_attributes",0)&0x400:raise ValueError("Reparse receipt")
            if q.is_dir() and (q/"delivery-manifest.json").exists():raise ValueError("Frozen output")
            if q==project:break
        with p.open("x",encoding="utf-8") as f:json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 1 if failed else 0

if __name__=="__main__":
    raise SystemExit(main())
