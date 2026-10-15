"""Version-bound semantic signature packaging; candidate screening never certifies isolation."""
from __future__ import annotations
import argparse,hashlib,json,re,stat,sys
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CORE=ROOT/"reviews/codex-supervision/2026-10-07-semantic-signature-supervision/effective-core-v2"
SIG_DIR=ROOT/"reviews/2026-10-07-semantic-core-lists"
CORE_MANIFEST_SHA256="78017f740969cd251f6c263bdcb14ef1bb5bd63de939df394fa24e33e57df4b5"
EXPECTED_GROUPS={"train":47,"selected_draft":264,"eval":300,"test":150}
NAME_RE=re.compile(r"[a-z][a-z0-9-]{0,79}")
def digest(data):return hashlib.sha256(data).hexdigest()
def dense(record):return digest(json.dumps(record,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf8"))
def math_digest(record):return digest(json.dumps({k:record.get(k) for k in ("problem","solution","answer","scene_spec")},ensure_ascii=False,sort_keys=True).encode("utf8"))
def checked_path(path,base):
    path=Path(path).absolute();base=Path(base).absolute()
    if ".." in path.parts or not path.is_relative_to(base):raise ValueError("Path outside registered root")
    current=path
    while True:
        if current.exists() or current.is_symlink():
            st=current.lstat()
            if current.is_symlink() or getattr(st,"st_file_attributes",0)&0x400:raise ValueError("Reparse path")
        if current==base:break
        current=current.parent
    return path
def manifest_path(relative):
    if not isinstance(relative,str) or not relative or "\\" in relative or ":" in relative:
        raise ValueError("Invalid manifest path")
    return checked_path(CORE/relative,CORE)
def read_json(data):return json.loads(data.decode("utf-8-sig"))
def read_rows(data):
    return [json.loads(line) for line in data.decode("utf-8-sig").splitlines() if line.strip()]
def load_record_bindings():
    manifest=checked_path(CORE/"delivery-manifest.json",CORE).read_bytes()
    if digest(manifest)!=CORE_MANIFEST_SHA256:raise ValueError("Frozen core manifest changed")
    entries={}
    for item in read_json(manifest)["artifacts"]:
        relative=item["path"];manifest_path(relative)
        if relative in entries:raise ValueError("Duplicate core artifact")
        entries[relative]=item
    def bound_bytes(path):
        path=checked_path(path,CORE);relative=path.relative_to(CORE).as_posix()
        if relative not in entries:raise ValueError("Unmanifested core input")
        data=path.read_bytes();item=entries[relative]
        if digest(data)!=item["sha256"] or len(data)!=item["bytes"]:raise ValueError("Frozen core artifact changed: "+relative)
        return data
    raw=bound_bytes(CORE/"record-bindings.jsonl")
    source_raw=bound_bytes(CORE/"source-bindings.json")
    index=read_json(bound_bytes(CORE/"current-index.json"))
    if index["record_bindings_sha256"]!=digest(raw) or index["source_bindings_sha256"]!=digest(source_raw):
        raise ValueError("Core index binding mismatch")
    rows=read_rows(raw);sources=read_json(source_raw)
    if len(rows)!=761 or len(sources)!=24:raise ValueError("Core population incomplete")
    by_source={};seen=set();positions=set()
    for source in sources:
        path=checked_path(ROOT/source["path"],CORE/"candidate-sources")
        if source["path"] in by_source:raise ValueError("Duplicate core source")
        data=bound_bytes(path)
        if digest(data)!=source["sha256"] or len(data)!=source["bytes"]:raise ValueError("Source binding mismatch")
        records=read_rows(data)
        if len(records)!=source["records"]:raise ValueError("Source record count mismatch")
        by_source[source["path"]]=(source,records)
    counts=Counter()
    for row in rows:
        rid=row.get("id");line=row.get("source_line");path=row.get("path")
        if not isinstance(rid,str) or not rid.strip() or rid in seen:raise ValueError("Duplicate/empty core id")
        seen.add(rid)
        if type(line) is not int or line<=0 or path not in by_source:raise ValueError("Invalid core row reference")
        if (path,line) in positions:raise ValueError("Duplicate core row position")
        positions.add((path,line));source,records=by_source[path]
        if line>len(records):raise ValueError("Source line outside record population")
        record=records[line-1]
        if (record.get("id")!=rid or dense(record)!=row.get("record_sha256")
                or math_digest(record)!=row.get("math_sha256") or row.get("source_sha256")!=source["sha256"]
                or row.get("group")!=source["group"]):
            raise ValueError("Actual record version/identity mismatch: "+rid)
        counts[row["group"]]+=1
    if dict(counts)!=EXPECTED_GROUPS or index["groups"]!=EXPECTED_GROUPS:raise ValueError("Core groups incomplete")
    return rows
def load_record(by_id,rid):
    if rid not in by_id:raise ValueError("Unknown core id")
    row=by_id[rid];path=checked_path(ROOT/row["path"],CORE/"candidate-sources")
    data=path.read_bytes()
    if digest(data)!=row["source_sha256"]:raise ValueError("Actual source changed")
    record=read_rows(data)[row["source_line"]-1]
    if dense(record)!=row["record_sha256"] or math_digest(record)!=row["math_sha256"]:
        raise ValueError("Actual record changed")
    return record
def validate_signature(sig,by_id):
    if not isinstance(sig,dict):raise ValueError("Signature must be an object")
    rid=sig.get("id")
    if not isinstance(rid,str) or rid not in by_id:raise ValueError("Unknown signature id")
    row=by_id[rid]
    for field in ("goal","domain"):
        if not isinstance(sig.get(field),str) or not sig[field].strip():raise ValueError("Nonempty string required: "+rid+"."+field)
    for field in ("key_conditions","decisive_steps"):
        values=sig.get(field)
        if not isinstance(values,list) or not values or any(not isinstance(v,str) or not v.strip() for v in values):
            raise ValueError("Nonempty list of nonempty strings required: "+rid+"."+field)
    if sig.get("group")!=row["group"]:raise ValueError("Signature group mismatch")
    for field in ("record_sha256","math_sha256"):
        if sig.get(field)!=row[field]:raise ValueError("Signature version mismatch: "+rid+"."+field)
def read_signature_inputs(paths,by_id):
    all_sigs=[];bindings=[];seen=set()
    for path in paths:
        path=checked_path(path,ROOT);data=path.read_bytes();sigs=read_rows(data)
        if not sigs:raise ValueError("Empty signature file")
        for sig in sigs:
            validate_signature(sig,by_id)
            if sig["id"] in seen:raise ValueError("Duplicate signature id across inputs: "+sig["id"])
            seen.add(sig["id"])
        all_sigs.extend(sigs)
        bindings.append({"path":path.relative_to(ROOT).as_posix(),"sha256":digest(data),"bytes":len(data),"records":len(sigs)})
    if not all_sigs:raise ValueError("No signatures supplied")
    return all_sigs,bindings
def output_directory(path):
    path=checked_path(path,ROOT/"reviews")
    if path.is_relative_to(CORE) or path.is_relative_to(ROOT/"reviews/codex-supervision/2026-10-07-continuous-math-review/current-core"):raise ValueError("Cannot write into frozen core or its frozen parent")
    return path
def publish(directory,files):
    directory=output_directory(directory)
    if directory.exists():raise FileExistsError("Preserve submitted output; choose a new --out directory")
    directory.parent.mkdir(parents=True,exist_ok=True)
    directory.mkdir(exist_ok=False)
    for name,data in files.items():
        with (directory/name).open("xb") as stream:stream.write(data)
def encoded(obj):return (json.dumps(obj,ensure_ascii=False,indent=2)+"\n").encode("utf8")
def bundle(group_name,input_path=None,out_path=None):
    if not NAME_RE.fullmatch(group_name):raise ValueError("Invalid signature group name")
    rows=load_record_bindings();by_id={r["id"]:r for r in rows}
    sigs,inputs=read_signature_inputs([input_path or SIG_DIR/(group_name+"-signatures.jsonl")],by_id)
    groups=dict(Counter(s["group"] for s in sigs))
    receipt={"schema":"semantic-core-signatures-v2","group":group_name,"total":len(sigs),"groups":groups,
        "core_manifest_sha256":CORE_MANIFEST_SHA256,"input_bindings":inputs,
        "actual_sources_and_records_verified":True,"packaging":"PASS_VERSION_BOUND_SIGNATURE_PACKAGING",
        "semantic_content":"PENDING_INDEPENDENT_REVIEW","semantic_isolation":"NOT_ESTABLISHED",
        "production":"CLOSED","PASS_CORE_SCOPE_issued":False}
    payload=b"".join((json.dumps(s,ensure_ascii=False)+"\n").encode("utf8") for s in sigs)
    receipt["signatures_sha256"]=digest(payload)
    publish(out_path or SIG_DIR/group_name,{"signatures.jsonl":payload,"receipt.json":encoded(receipt)})
    print(json.dumps(receipt,ensure_ascii=False));return 0
def cross_match(input_paths=None,out_path=None,allow_partial=False):
    rows=load_record_bindings();by_id={r["id"]:r for r in rows}
    paths=list(input_paths) if input_paths is not None else sorted(SIG_DIR.glob("*-signatures.jsonl"))
    sigs,inputs=read_signature_inputs(paths,by_id)
    present={s["id"] for s in sigs};missing=sorted(set(by_id)-present)
    if missing and not allow_partial:raise ValueError("Incomplete core signature coverage: "+str(len(missing))+" missing; --allow-partial records an INCOMPLETE result")
    train=[s for s in sigs if s["group"] in ("train","selected_draft")]
    evaluation=[s for s in sigs if s["group"] in ("eval","test")]
    # Literal descriptor equality is ONE non-exhaustive candidate channel, not a semantic decision.
    key=lambda s:(s["goal"].strip(),tuple(sorted(step.strip() for step in s["decisive_steps"])))
    by=defaultdict(list)
    for sig in evaluation:by[key(sig)].append(sig)
    candidates=[]
    for t in train:
        for e in by.get(key(t),[]):
            candidates.append({"train_id":t["id"],"eval_id":e["id"],"eval_group":e["group"],
                "train_record_sha256":t["record_sha256"],"eval_record_sha256":e["record_sha256"],
                "train_goal":t["goal"],"eval_goal":e["goal"],"train_steps":t["decisive_steps"],"eval_steps":e["decisive_steps"],
                "train_domain":t["domain"],"eval_domain":e["domain"],
                "train_conditions":t["key_conditions"],"eval_conditions":e["key_conditions"],
                "disposition":"UNREVIEWED","candidate_basis":"EXACT_GOAL_AND_UNORDERED_STEP_DESCRIPTORS"})
    receipt={"schema":"semantic-cross-candidates-v2","core_manifest_sha256":CORE_MANIFEST_SHA256,
        "input_bindings":inputs,"train_side":len(train),"eval_side":len(evaluation),
        "expected_groups":EXPECTED_GROUPS,"covered_groups":dict(Counter(s["group"] for s in sigs)),
        "missing_ids":missing,"signature_coverage":"INCOMPLETE" if missing else "COMPLETE",
        "candidate_generation":"PARTIAL_CANDIDATE_SCREEN" if missing else "CANDIDATE_SCREEN_ONLY",
        "candidates":candidates,"candidate_generation_exhaustive":False,
        "limits":["Literal descriptor equality misses synonyms and alternative mathematical formulations.",
                  "Goal/step equality does not establish semantic equivalence; domains and conditions require review.",
                  "Zero candidates never establishes train/evaluation isolation."],
        "semantic_content":"PENDING_INDEPENDENT_REVIEW","semantic_isolation":"NOT_ESTABLISHED",
        "production":"CLOSED","PASS_CORE_SCOPE_issued":False}
    publish(out_path or SIG_DIR/"cross-match-v2",{"cross-candidates.json":encoded(receipt)})
    print(json.dumps({"signature_coverage":receipt["signature_coverage"],"train_side":len(train),
        "eval_side":len(evaluation),"candidates":len(candidates),"semantic_isolation":"NOT_ESTABLISHED"},ensure_ascii=False))
    return 3 if missing else 0
def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action",choices=("bundle","cross-match"));parser.add_argument("--group")
    parser.add_argument("--input",type=Path,action="append");parser.add_argument("--out",type=Path)
    parser.add_argument("--allow-partial",action="store_true")
    args=parser.parse_args(argv)
    try:
        if args.action=="bundle":
            if not args.group or args.allow_partial or (args.input is not None and len(args.input)!=1):
                raise ValueError("bundle requires --group, optional one --input; no --allow-partial")
            return bundle(args.group,args.input[0] if args.input else None,args.out)
        if args.group:raise ValueError("cross-match does not accept --group")
        return cross_match(args.input,args.out,args.allow_partial)
    except (ValueError,KeyError,TypeError,IndexError,OSError) as exc:
        print(json.dumps({"status":"FAIL_VERSION_BOUND_SIGNATURE_PACKAGING","error_type":type(exc).__name__,
            "detail":str(exc),"semantic_isolation":"NOT_ESTABLISHED","production":"CLOSED","PASS_CORE_SCOPE_issued":False},ensure_ascii=False))
        return 2
if __name__=="__main__":raise SystemExit(main())
