"""Read-only audit of the named project backup; only new project-local reports are written."""
from __future__ import annotations
import hashlib,json,os,stat,sys,uuid
from pathlib import Path
HERE=Path(__file__).absolute().parent
ROOT=HERE.parents[3]
BACKUP=Path(r"D:\backups\animtrain\2026-10-17-training-data")
PARTS=("data","holdout-sources","configs")
MAX_FILES=30000
MAX_BYTES=4*1024**3
class AuditError(ValueError):pass
def enc(x):return json.dumps(x,ensure_ascii=True,sort_keys=True,separators=(",",":")).encode()
def sha(raw):return hashlib.sha256(raw).hexdigest()
def fingerprint(st):return (st.st_size,st.st_mtime_ns,st.st_ctime_ns,st.st_dev,st.st_ino)
def safe_path(path):
    p=Path(path).absolute()
    if ".." in p.parts or "." in p.parts:raise AuditError("path_alias")
    for q in reversed((p,*p.parents)):
        if q.exists() or q.is_symlink():
            st=q.lstat()
            if q.is_symlink() or getattr(st,"st_file_attributes",0)&0x400:
                raise AuditError("reparse_path")
    return p
def inventory(root,*,max_files=MAX_FILES,max_bytes=MAX_BYTES):
    root=safe_path(root)
    if not root.is_dir():raise AuditError("missing_root")
    files={};directories={};total=0
    def walk(p):
        nonlocal total
        st=p.lstat()
        if p.is_symlink() or getattr(st,"st_file_attributes",0)&0x400:raise AuditError("reparse_entry")
        if not stat.S_ISDIR(st.st_mode):raise AuditError("not_directory")
        directories[p.relative_to(root).as_posix()]=fingerprint(st)
        for child in sorted(p.iterdir()):
            st=child.lstat()
            if child.is_symlink() or getattr(st,"st_file_attributes",0)&0x400:raise AuditError("reparse_entry")
            if stat.S_ISDIR(st.st_mode):walk(child)
            elif stat.S_ISREG(st.st_mode):
                files[child.relative_to(root).as_posix()]=fingerprint(st);total+=st.st_size
                if len(files)>max_files or total>max_bytes:raise AuditError(f"inventory_budget_exceeded: files={len(files)}, bytes={total}")
            else:raise AuditError("special_entry")
    for name in PARTS:walk(root/name)
    return {"files":files,"directories":directories,"bytes":total}
def hash_file(path,expected):
    safe_path(path)
    if fingerprint(path.stat())!=expected:raise AuditError("file_changed_before_hash")
    h=hashlib.sha256()
    with path.open("rb") as f:
        if (lambda st:(st.st_size,st.st_mtime_ns,st.st_dev,st.st_ino))(os.fstat(f.fileno()))!=expected[:2]+expected[3:]:raise AuditError("file_identity_changed")
        for block in iter(lambda:f.read(1024*1024),b""):h.update(block)
        if (lambda st:(st.st_size,st.st_mtime_ns,st.st_dev,st.st_ino))(os.fstat(f.fileno()))!=expected[:2]+expected[3:]:raise AuditError("file_changed_during_hash")
    if fingerprint(path.stat())!=expected:raise AuditError("file_changed_after_hash")
    return h.hexdigest()
def audit(source=ROOT,destination=BACKUP):
    source=safe_path(source);destination=safe_path(destination)
    if source==destination or source.is_relative_to(destination) or destination.is_relative_to(source):
        raise AuditError("overlapping_roots")
    left=inventory(source);right=inventory(destination)
    if left["bytes"]+right["bytes"]>MAX_BYTES:raise AuditError("combined_budget_exceeded")
    source_files={};target_files={}
    for rel,pin in left["files"].items():source_files[rel]={"size":pin[0],"sha256":hash_file(source/rel,pin)}
    for rel,pin in right["files"].items():target_files[rel]={"size":pin[0],"sha256":hash_file(destination/rel,pin)}
    if inventory(source)!=left or inventory(destination)!=right:raise AuditError("tree_changed_during_audit")
    common=set(source_files)&set(target_files)
    mismatched=sorted(rel for rel in common if source_files[rel]!=target_files[rel])
    missing=sorted(set(source_files)-set(target_files));extra=sorted(set(target_files)-set(source_files))
    shared=sorted(rel for rel in common if left["files"][rel][3:]==right["files"][rel][3:])
    missing_dirs=sorted(set(left["directories"])-set(right["directories"]))
    extra_dirs=sorted(set(right["directories"])-set(left["directories"]))
    status="PASS_CURRENT_CONTENT_EQUALITY_ONLY" if not (mismatched or missing or extra or shared or missing_dirs or extra_dirs) else "FAIL"
    return {"schema":"bounded-project-backup-audit-v1","status":status,
        "scope":"CURRENT_FILE_BYTES_AND_DIRECTORY_COVERAGE_ONLY_NOT_ORIGINAL_COPY_RC_ACL_RESTORE_OR_SEPARATE_DISK_PROOF",
        "source":str(source),"destination":str(destination),"parts":list(PARTS),
        "source_files":source_files,"destination_files":target_files,
        "source_bytes":left["bytes"],"destination_bytes":right["bytes"],
        "matched_files":len(common)-len(mismatched),
        "missing_files":missing,"extra_files":extra,"mismatched_files":mismatched,
        "shared_file_identity":shared,"missing_directories":missing_dirs,"extra_directories":extra_dirs,
        "source_content_tree_sha256":sha(enc(source_files)),"destination_content_tree_sha256":sha(enc(target_files)),
        "original_robocopy_returncodes":None,
        "observation":"metadata stability checked before/during/after hashing; not an atomic snapshot or hostile-peer boundary",
        "backup_action":"NOT_PERFORMED","production":"CLOSED","global_isolation":"NOT_ESTABLISHED"}
def write_report(result,base=HERE):
    base=safe_path(base)
    if not base.is_relative_to(ROOT) or not base.is_dir():raise AuditError("output_outside_project")
    for p in (base,*base.parents):
        if (p/"delivery-manifest.json").exists():raise AuditError("frozen_output")
        if p==ROOT:break
    d=base/("audit-"+uuid.uuid4().hex);d.mkdir(exist_ok=False)
    result={**result,"verifier_sha256":sha(Path(__file__).read_bytes())}
    raw=enc(result)+b"\n"
    with (d/"audit.json").open("xb") as f:f.write(raw)
    complete={"schema":"backup-audit-output-v1","status":result["status"],"artifact":{"path":"audit.json","bytes":len(raw),"sha256":sha(raw)}}
    with (d/"COMPLETE.json").open("xb") as f:f.write(enc(complete)+b"\n")
    return d

def audit_current_inputs(source=ROOT,destination=BACKUP):
    source=safe_path(source);destination=safe_path(destination)
    if source==destination or source.is_relative_to(destination) or destination.is_relative_to(source):raise AuditError("overlapping_roots")
    manifest_path=safe_path(source/"data/manifest.json")
    manifest_raw=manifest_path.read_bytes()
    if len(manifest_raw)>1024*1024:raise AuditError("manifest_budget")
    manifest=json.loads(manifest_raw)
    entries=manifest.get("entries")
    if type(entries)is not list or not entries or len(entries)>100:raise AuditError("manifest_entries")
    names={"data/manifest.json":(None,None),"data/asset_evidence.json":(None,None),
           "configs/training_diversity_policy.json":(None,None),"configs/train_loop.example.json":(None,None)}
    for entry in entries:
        rel=entry.get("path")
        if type(rel)is not str:raise AuditError("manifest_path")
        rel=rel.replace("\\","/")
        if rel.startswith("/") or ":" in rel or any(x in ("",".","..") for x in rel.split("/")):raise AuditError("manifest_path_alias")
        rel="data/"+rel
        if rel in names:raise AuditError("duplicate_manifest_path")
        expected=entry.get("sha256")
        if type(expected)is not str or len(expected)!=64 or any(c not in "0123456789abcdef" for c in expected):raise AuditError("manifest_sha")
        expected_size=entry.get("size")
        if type(expected_size)is not int or expected_size<0:raise AuditError("manifest_size")
        names[rel]=(expected,expected_size)
    records=[];total=0
    for rel,(expected,expected_size) in sorted(names.items()):
        p=safe_path(source/rel);st=p.stat()
        if not stat.S_ISREG(st.st_mode):raise AuditError("not_regular_input")
        if expected_size is not None and st.st_size!=expected_size:raise AuditError("manifest_input_size_mismatch")
        total+=st.st_size
        if st.st_size>32*1024*1024 or total>128*1024*1024:raise AuditError("current_inputs_budget")
        srcsha=hash_file(p,fingerprint(st))
        if expected is not None and srcsha!=expected:raise AuditError("manifest_input_sha_mismatch")
        q=safe_path(destination/rel)
        row={"path":rel,"source_sha256":srcsha,"source_bytes":st.st_size,"manifest_sha256":expected,
             "destination_sha256":None,"destination_bytes":None,"status":"MISSING"}
        if q.is_file():
            qt=q.stat();row["destination_bytes"]=qt.st_size
            if qt.st_size>32*1024*1024:raise AuditError("destination_file_budget")
            row["destination_sha256"]=hash_file(q,fingerprint(qt))
            row["status"]="PASS" if qt.st_size==st.st_size and row["destination_sha256"]==srcsha else "FAIL"
            if os.path.samefile(p,q):row["status"]="SHARED_FILE_IDENTITY"
        records.append(row)
    if manifest_path.read_bytes()!=manifest_raw:raise AuditError("manifest_changed")
    for row in records:
        p=source/row["path"]
        if hash_file(p,fingerprint(p.stat()))!=row["source_sha256"]:raise AuditError("input_changed")
        q=destination/row["path"]
        if row["destination_sha256"] is not None:
            if hash_file(q,fingerprint(q.stat()))!=row["destination_sha256"]:raise AuditError("backup_input_changed")
        elif q.exists():raise AuditError("backup_input_appeared")
    return {"schema":"bounded-project-backup-current-inputs-v1",
        "status":"PASS_CURRENT_MANIFEST_INPUTS_ONLY" if all(x["status"]=="PASS" for x in records) else "FAIL",
        "scope":"ONLY_NAMED_CURRENT_MANIFEST_FILES_AND_FOUR_CONTROL_FILES_NOT_WHOLE_BACKUP",
        "source":str(source),"destination":str(destination),"records":records,"source_bytes":total,
        "matched_files":sum(x["status"]=="PASS" for x in records),
        "manifest_sha256":sha(manifest_raw),"original_robocopy_returncodes":None,
        "whole_backup":"UNVERIFIED_RESOURCE_LIMIT","holdout_sources":"NOT_AUDITED",
        "backup_action":"NOT_PERFORMED","production":"CLOSED","global_isolation":"NOT_ESTABLISHED"}

def main():
    if sys.argv[1:] not in ([],["--current-inputs-only"]):raise AuditError("unsupported_arguments")
    try:result=audit_current_inputs() if sys.argv[1:] else audit()
    except (OSError,ValueError) as exc:
        result={"schema":"bounded-project-backup-audit-v1","status":"ERROR","error":type(exc).__name__+": "+str(exc),
                "backup_action":"NOT_PERFORMED","production":"CLOSED"}
    d=write_report(result)
    print(json.dumps({"output":str(d),"status":result["status"],"source_files":len(result.get("source_files",result.get("records",{}))),
                     "source_bytes":result.get("source_bytes"),"matched_files":result.get("matched_files")}))
    return 0 if result["status"] in {"PASS_CURRENT_CONTENT_EQUALITY_ONLY","PASS_CURRENT_MANIFEST_INPUTS_ONLY"} else 2
if __name__=="__main__":raise SystemExit(main())
