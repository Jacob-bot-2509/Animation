"""Read-only evidence inventory. Does not judge core associations or expose question text."""
from pathlib import Path
import os, sys, json, hashlib, stat, subprocess, collections, datetime, re
R = Path(r"D:\Animation-Model-Training")
O = R / "reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol"
ROOTS = ("data","reviews","docs","holdout-sources","configs","assets","src","tools","tests")
SKIP_NAMES = {".git",".venv","node_modules","__pycache__",".sandbox-runtime",".pytest_cache"}
SKIP_PREFIXES = ("edge-profile","chrome-profile","browser-profile")
GIT_CONTENT_EXTENSIONS = {".json",".jsonl",".md",".txt",".py",".tex",".pdf",".csv",".tsv",".yaml",".yml",".toml",".ini"}
def canonical(obj): return json.dumps(obj, ensure_ascii=False, sort_keys=True).encode("utf-8")
def digest_bytes(b): return hashlib.sha256(b).hexdigest()
def read_json(p): return json.loads(p.read_text(encoding="utf-8-sig"))
def output_json(name,obj):
    with (O/name).open("x",encoding="utf-8",newline="\n") as f:
        f.write(json.dumps(obj,ensure_ascii=False,indent=2)+"\n")
def line_writer(name):
    return (O/name).open("x",encoding="utf-8",newline="\n")
def emit(f,obj): f.write(json.dumps(obj,ensure_ascii=False,separators=(",",":"))+"\n")
def rel(p): return p.relative_to(R).as_posix()
def reparse(p): return bool(p.stat(follow_symlinks=False).st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
def skip(d): return d in SKIP_NAMES or d.lower().startswith(SKIP_PREFIXES)
def run(args):
    cp=subprocess.run(["git","-c","core.quotepath=false",*args],cwd=R,capture_output=True,timeout=120)
    if cp.returncode:raise RuntimeError("Git metadata read failed: "+str(args[0])+" rc "+str(cp.returncode))
    return cp.stdout
def hash_file(p):
    before=p.stat()
    h=hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda:f.read(1<<20),b""):h.update(chunk)
    after=p.stat()
    if (before.st_size,before.st_mtime_ns)!=(after.st_size,after.st_mtime_ns):
        raise RuntimeError("FILE_CHANGED_DURING_CAPTURE")
    return h.hexdigest(),after.st_size
def store_raw(b):
    checksum=digest_bytes(b)
    dest=O/"git-history"/"blobs"/(checksum+".bin")
    dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists():
        with dest.open("xb") as f:f.write(b)
    assert digest_bytes(dest.read_bytes())==checksum
    return dest

def main():
    O.mkdir(exist_ok=False)
    started=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
    head=run(["rev-parse","HEAD"]).decode("ascii").strip()
    refs=run(["for-each-ref","--format=%(refname) %(objectname)"])
    excluded=[];errors=[];files={};by_sha=collections.defaultdict(list)
    with line_writer("filesystem-inventory.jsonl") as ledger:
        for root in ROOTS:
            base=R/root
            if not base.exists():continue
            for directory,dirs,names in os.walk(base,followlinks=False):
                kept=[]
                for d in sorted(dirs):
                    p=Path(directory)/d
                    if p==O:excluded.append({"path":rel(p),"reason":"new output: avoid recursive self-inclusion"})
                    elif skip(d):excluded.append({"path":rel(p),"reason":"runtime, browser profile/cache, or VCS metadata"})
                    elif p.is_symlink() or reparse(p):excluded.append({"path":rel(p),"reason":"reparse point: not followed"})
                    else:kept.append(d)
                dirs[:]=kept
                for name in sorted(names):
                    p=Path(directory)/name
                    if rel(p)=="reviews/codex-supervision/2026-10-04-live-watch/watch.lock":
                        excluded.append({"path":rel(p),"reason":"active observer exclusive process mutex; not question material"})
                        continue
                    if p.is_symlink() or reparse(p):
                        excluded.append({"path":rel(p),"reason":"reparse file: not followed"});continue
                    if root=="reviews" and rel(p).startswith("reviews/codex-supervision/2026-10-04-live-watch/") and name in {"latest.json","events.jsonl","watcher.stdout.log","watcher.stderr.log","watcher.lock","watch.lock"}:
                        b=p.read_bytes();dst=O/"observer-snapshot"/name
                        dst.parent.mkdir(exist_ok=True)
                        with dst.open("xb") as f:f.write(b)
                        row={"path":rel(p),"sha256":digest_bytes(b),"bytes":len(b),"actual_bound_path":rel(dst),"category":"activity_snapshot","exposure_state":"ROLE_EXPOSURE_UNKNOWN","content_emitted_to_model":False}
                    else:
                        try:checksum,n=hash_file(p)
                        except (OSError,RuntimeError) as exc:
                            errors.append({"path":rel(p),"error":type(exc).__name__,"reason":str(exc)});continue
                        row={"path":rel(p),"sha256":checksum,"bytes":n,"actual_bound_path":rel(p),
                             "category":"candidate_source_metadata" if root=="holdout-sources" else "available_potential_exposure_material",
                             "exposure_state":"CANDIDATE_QUALIFICATION_UNREVIEWED" if root=="holdout-sources" else "ROLE_EXPOSURE_UNKNOWN",
                             "content_emitted_to_model":False}
                    files[row["path"]]=row;by_sha[row["sha256"]].append(row["actual_bound_path"]);emit(ledger,row)
            print("hashed scope",root,"files so far",len(files),flush=True)
        for p in sorted(R.glob("*")):
            if p.is_file() and p.suffix.lower() in GIT_CONTENT_EXTENSIONS:
                checksum,n=hash_file(p)
                row={"path":rel(p),"sha256":checksum,"bytes":n,"actual_bound_path":rel(p),"category":"root_project_material","exposure_state":"ROLE_EXPOSURE_UNKNOWN","content_emitted_to_model":False}
                files[row["path"]]=row;by_sha[checksum].append(rel(p));emit(ledger,row)
    output_json("filesystem-scope.json",{"schema":"project-history-evidence-filesystem-scope-v1","started_at":started,"head":head,
        "roots":list(ROOTS),"root_project_text_files_included":True,"available_files_bound":len(files),
        "excluded":excluded,"capture_errors":errors,"scope_complete":not errors,
        "scope_completeness_means":"all readable ordinary files in the declared roots at capture; not all human/model exposure proven",
        "question_text_emitted_to_model":False,"qualified_count":None})
    (O/"git-refs.raw.txt").write_bytes(refs)
    commits=run(["rev-list","--all"]).decode("ascii").splitlines()
    (O/"git-commits.raw.txt").write_text("\n".join(commits)+"\n",encoding="ascii")
    occurrences=collections.defaultdict(list)
    with line_writer("git-path-versions.jsonl") as versions:
        for index,commit in enumerate(commits):
            raw=run(["ls-tree","-r","-z",commit,"--",*ROOTS])
            for entry in raw.split(b"\0"):
                if not entry:continue
                meta,pathraw=entry.split(b"\t",1)
                mode,kind,oid=meta.decode("ascii").split()
                path=pathraw.decode("utf-8")
                parts=Path(path).parts
                if any(skip(x) for x in parts) or path.startswith(rel(O)+"/"):continue
                if kind!="blob" or Path(path).suffix.lower() not in GIT_CONTENT_EXTENSIONS:continue
                row={"commit":commit,"logical_path":path,"git_object_id":oid,"mode":mode}
                emit(versions,row)
                occurrences[oid].append(row)
            if index%25==0:print("git trees",index+1,"of",len(commits),flush=True)
    proc=subprocess.Popen(["git","cat-file","--batch"],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    def blob(oid):
        proc.stdin.write((oid+"\n").encode("ascii"));proc.stdin.flush()
        header=proc.stdout.readline().decode("ascii").strip().split()
        if len(header)!=3 or header[1]!="blob":raise RuntimeError("invalid Git blob header")
        n=int(header[2]);b=proc.stdout.read(n)
        if len(b)!=n or proc.stdout.read(1)!=b"\n":raise RuntimeError("incomplete Git blob read")
        assert hashlib.sha1(b"blob "+str(n).encode("ascii")+b"\0"+b).hexdigest()==oid
        return b
    git_rows=[];recovered=0
    with line_writer("git-history-inventory.jsonl") as ledger:
        for oid,versions in sorted(occurrences.items()):
            b=blob(oid);checksum=digest_bytes(b)
            candidates=by_sha.get(checksum)
            if candidates:
                actual=sorted(candidates)[0];storage="existing_exact_bytes"
            else:
                actual=rel(store_raw(b));storage="materialized_original_git_blob";recovered+=1
            row={"git_object_id":oid,"sha256":checksum,"bytes":len(b),"actual_bound_path":actual,"storage":storage,
                "logical_paths":sorted({v["logical_path"] for v in versions}),"commit_count":len({v["commit"] for v in versions}),
                "exposure_state":"ROLE_EXPOSURE_UNKNOWN","content_emitted_to_model":False}
            git_rows.append(row);emit(ledger,row);by_sha[checksum].append(actual)
    proc.stdin.close()
    assert proc.wait(timeout=30)==0
    assert run(["rev-parse","HEAD"]).decode("ascii").strip()==head
    assert run(["for-each-ref","--format=%(refname) %(objectname)"])==refs
    output_json("git-history-scope.json",{"schema":"reachable-project-history-scope-v1","head":head,"reachable_commits":len(commits),"unique_relevant_blobs":len(git_rows),
        "materialized_missing_versions":recovered,"extensions":sorted(GIT_CONTENT_EXTENSIONS),"roots":list(ROOTS),
        "all_selected_path_versions_enumerated":True,"refs_unchanged_during_capture":True,
        "not_covered":["unreachable/deleted Git objects","unrecorded external chats and unavailable external files","non-text/media binary Git versions beyond the selected extensions"],
        "qualified_count":None})
    # Concrete anchors plus their selected sources and row identities.
    anchors=["data/manifest.json","reviews/2026-10-06-core-families/core-families.corrected-v2.json",
        "reviews/2026-10-06-linalg048-admission/v3-receipt-bound/semantic-review-workflow-v1.json",
        "data/b5-annotation-set/b5-annotation-set.json","data/b5-calibration-report/b5-calibration-report.json",
        "data/b5-calibration-report/pdf/b5-calibration-report.pdf",
        "reviews/2026-10-05-training-diversity-drafts/draft-selection.json",
        "reviews/codex-supervision/2026-10-04-artifact-migration/path-mapping.json",
        "reviews/codex-supervision/2026-10-07-holdout-v2-review/delivery-manifest.json",
        "holdout-sources/extracted/kaoyan-pool-v1-manifest.json","holdout-sources/extracted/kaoyan-triples.jsonl"]
    manifest_paths=[p for p in files if "manifest" in Path(p).name.lower() and p.endswith(".json") and p.startswith("reviews/codex-supervision/")]
    anchor_rows=[files[p] for p in anchors]
    output_json("anchor-bindings.json",{"schema":"holdout-exposure-anchor-bindings-v1","anchors":anchor_rows,
        "supervision_manifest_paths":sorted(manifest_paths),"supervision_manifest_count":len(manifest_paths)})
    def field_digest(value):
        b=value.encode("utf-8") if isinstance(value,str) else canonical(value)
        return digest_bytes(b)
    def row_ledger(source,f,role):
        p=R/source;raw=p.read_bytes();source_sha=digest_bytes(raw);count=0
        for number,b in enumerate(raw.splitlines(keepends=True),1):
            if not b.strip():continue
            rec=json.loads(b.decode("utf-8-sig"));count+=1
            row={"source_path":source,"source_raw_sha256":source_sha,"line_number":number,
                "raw_line_with_terminator_sha256":digest_bytes(b),"record_canonical_sha256":digest_bytes(canonical(rec)),
                "id":rec.get("id"),"problem_id":rec.get("problem_id"),"solution_id":rec.get("solution_id"),
                "role":role,"exposure_state":"ROLE_EXPOSURE_UNKNOWN",
                "exact_field_sha256":{k:field_digest(rec[k]) for k in ("problem","solution","answer") if k in rec}}
            emit(f,row)
        return count
    active=read_json(R/"data/manifest.json")
    active_counts=collections.Counter();source_rows=[]
    with line_writer("active-497-row-bindings.jsonl") as rows:
        for entry in active["entries"]:
            source=(Path("data")/entry["path"]).as_posix()
            checksum,n=hash_file(R/source)
            assert checksum==entry["sha256"] and n==entry["size"]
            count=row_ledger(source,rows,entry["split"]);active_counts[entry["split"]]+=count
            source_rows.append({"path":source,"sha256":checksum,"count":count,"split":entry["split"]})
    assert dict(active_counts)=={"train":47,"eval":300,"test":150}
    selector=read_json(R/"reviews/2026-10-05-training-diversity-drafts/draft-selection.json")
    selected_counts=[];seen_paths=set()
    with line_writer("selected-264-row-bindings.jsonl") as rows:
        for entry in selector["entries"]:
            source=entry["root_path"].replace("\\","/")
            assert source not in seen_paths;seen_paths.add(source)
            checksum,n=hash_file(R/source)
            assert checksum==entry["raw_sha256"]
            count=row_ledger(source,rows,"selected_draft")
            assert count==entry["count"]
            selected_counts.append({"path":source,"sha256":checksum,"count":count})
    assert sum(r["count"] for r in selected_counts)==264
    # Natural sources in archived JSONL, without doing equality or mathematical matching.
    historical_row_files=[];historical_row_errors=[]
    with line_writer("historical-triple-row-bindings.jsonl") as rows:
        for source,file in sorted(files.items()):
            if not source.endswith(".jsonl") or source.startswith("holdout-sources/"):continue
            p=R/file["actual_bound_path"]
            try:
                raw=p.read_bytes();linecount=0
                for number,b in enumerate(raw.splitlines(keepends=True),1):
                    if not b.strip():continue
                    rec=json.loads(b.decode("utf-8-sig"))
                    if not isinstance(rec,dict) or not all(k in rec for k in ("problem","solution","answer")):continue
                    linecount+=1
                    emit(rows,{"source_path":source,"source_raw_sha256":file["sha256"],"line_number":number,"raw_line_with_terminator_sha256":digest_bytes(b),
                        "record_canonical_sha256":digest_bytes(canonical(rec)),"id":rec.get("id"),"exact_field_sha256":{k:field_digest(rec[k]) for k in ("problem","solution","answer")},
                        "exposure_state":"ROLE_EXPOSURE_UNKNOWN"})
                if linecount:historical_row_files.append({"path":source,"triple_rows_bound":linecount})
            except (UnicodeError,json.JSONDecodeError) as exc:
                historical_row_errors.append({"path":source,"error":type(exc).__name__})
    # Reference closure preserves claimed hashes and resolves exact bytes where available.
    refs_out=[];unresolved=[]
    migration=read_json(R/"reviews/codex-supervision/2026-10-04-artifact-migration/path-mapping.json")
    def references(obj,location="$"):
        if isinstance(obj,dict):
            for key,val in obj.items():
                if isinstance(val,str) and (key=="path" or key.endswith("_path")):
                    suffix="" if key=="path" else key[:-5]
                    candidates=([suffix+"_raw_sha256",suffix+"_sha256"] if suffix else ["raw_sha256","sha256"])
                    expected=next((obj[k] for k in candidates if isinstance(obj.get(k),str) and re.fullmatch("[a-f0-9]{64}",obj[k])),None)
                    if expected:yield location+"."+key,val,expected
                if isinstance(val,(dict,list)):yield from references(val,location+"."+key)
        elif isinstance(obj,list):
            for i,val in enumerate(obj):yield from references(val,location+"["+str(i)+"]")
    for source in sorted(set(manifest_paths+anchors)):
        p=R/source
        if not p.suffix.lower()==".json":continue
        try:obj=read_json(p)
        except (UnicodeError,json.JSONDecodeError):continue
        for location,logical,expected in references(obj):
            matches=by_sha.get(expected,[])
            row={"referring_path":source,"json_pointer_label":location,"claimed_path":logical,"claimed_sha256":expected,
                 "actual_matching_paths":sorted(set(matches)),"status":"EXACT_BYTES_AVAILABLE" if matches else "UNRESOLVED_EXPECTED_VERSION"}
            refs_out.append(row)
            if not matches:unresolved.append(row)
    with line_writer("reference-closure.jsonl") as ledger:
        for row in refs_out:emit(ledger,row)
    output_json("row-binding-summary.json",{"canonical_serialization":"json.dumps(record,ensure_ascii=False,sort_keys=True), UTF-8, default separators",
        "line_sha_convention":"exact source line bytes INCLUDING original line terminator",
        "active_counts":dict(active_counts),"active_rows":497,"active_sources":source_rows,
        "selected_draft_rows":264,"selected_draft_sources":selected_counts,
        "historical_jsonl_sources_with_triples":historical_row_files,"historical_triple_rows_bound":sum(x["triple_rows_bound"] for x in historical_row_files),
        "historical_jsonl_parse_errors":historical_row_errors,"reference_count":len(refs_out),"unresolved_expected_versions":unresolved,
        "qualified_count":None,"core_associations_decided":0})
    core=read_json(R/"reviews/2026-10-06-core-families/core-families.corrected-v2.json")
    groups=collections.defaultdict(list)
    for r in core["record_core_reviews"]:groups[r["core_family_id"]].append(r)
    assert len(groups)==46 and len(core["record_core_reviews"])==47
    families=[]
    for family,members in sorted(groups.items()):
        families.append({"core_family_id":family,"family_identity_sha256":digest_bytes(canonical({"catalog_sha256":files["reviews/2026-10-06-core-families/core-families.corrected-v2.json"]["sha256"],"core_family_id":family,"member_record_hashes":sorted(r["record_canonical_sha256"] for r in members)})),
            "members":[{k:r[k] for k in ("id","source_path","source_raw_sha256","source_line","raw_line_sha256","record_canonical_sha256")} for r in members],
            "profile_sha256":[digest_bytes(canonical(r["core_profile"])) for r in members],
            "core_profile_fields":["object","conditions","goal","solution_structure"],"not_a_current_math_acceptance_certificate":True})
    pooloverlay=read_json(R/"reviews/codex-supervision/2026-10-07-holdout-v2-review/candidate-metadata-overlay.json")
    assert pooloverlay["candidate_count"]==391
    output_json("core-association-plan.json",{"schema":"holdout-core-association-preregistration-v1","status":"PROTOCOL_REGISTERED_NOT_EXECUTED",
        "catalog_path":"reviews/2026-10-06-core-families/core-families.corrected-v2.json","catalog_sha256":files["reviews/2026-10-06-core-families/core-families.corrected-v2.json"]["sha256"],
        "families":families,"candidate_pool_raw_sha256":pooloverlay["pool_raw_sha256"],
        "candidates":[{k:r[k] for k in ("candidate_id","original_id","record_sha256","pool_raw_sha256")} for r in pooloverlay["records"]],
        "family_count":46,"candidate_count":391,"planned_cells":46*391,
        "default_cell_verdict":"UNREVIEWED","default_member_qualification":"QUARANTINED_NOT_ELIGIBLE",
        "decided_cells":0,"positive_cells":None,"negative_cells":None,"qualified_count":None,
        "roles":{"protocol_and_evidence_owner":"codex","qualification_review_execution_owner":"codex",
                 "second_independent_qualification_reviewer":"PENDING","independent_conflict_adjudicator":"PENDING"},
        "scope_warning":"46 tasks represent bound original-47 census only; all other historical task versions and per-role exposure require additional review."})
    output_json("inventory-summary.json",{"schema":"holdout-history-evidence-summary-v1","captured_at":started,"head":head,
        "file_inventory_records":len(files),"reachable_commits":len(commits),"unique_relevant_git_blobs":len(git_rows),"recovered_git_versions":recovered,
        "active_rows_bound":497,"active_train_rows_bound":47,"selected_draft_rows_bound":264,"workflow_pairs":296,"core_families":46,"candidate_members":391,
        "planned_association_cells":17986,"associations_decided":0,"known_positive_cells":None,"known_negative_cells":None,
        "reference_count":len(refs_out),"unresolved_expected_versions_count":len(unresolved),"filesystem_capture_errors":errors,
        "scope_binding_complete":not errors,"human_and_model_exposure_complete":False,"qualification_complete":False,"qualified_count":None,
        "role_exposure_default":"UNKNOWN; no member cleared by file hashing",
        "new_questions":0,"deleted_questions":0,"experiments_started":0,"calibration_status":"UNCALIBRATED","production_gate":"CLOSED"})
    print(json.dumps({"files":len(files),"reachable_commits":len(commits),"git_blobs":len(git_rows),"recovered":recovered,
        "active":dict(active_counts),"selected_draft_rows":264,"planned_core_cells":17986,"decided_core_cells":0,
        "references":len(refs_out),"unresolved_versions":len(unresolved),"capture_errors":len(errors)},ensure_ascii=False),flush=True)
if __name__=="__main__":main()
