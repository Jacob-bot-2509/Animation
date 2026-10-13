"""Lossless local witness Base64 intake. Default PLAN; never issues acceptance."""
from __future__ import annotations
import argparse,base64,hashlib,json,re,sys,uuid
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REGISTERED_ROOT=ROOT/"reviews/codex-supervision/2026-10-06-all43-sandbox-repair/external-tests"
NAMES=("receiver.jsonl","receiver.jsonl.summary.json","stdout.bin","stderr.bin","process-exit.json")
ALIASES={"receiver.jsonl.summary.json":"summary.b64","stdout.bin":"stdout.b64"}
def digest(data):
    return hashlib.sha256(data).hexdigest()

def safe_path(path,registered=False):
    path=Path(path).absolute()
    if ".." in path.parts:raise ValueError("Parent traversal is forbidden")
    if registered and not path.is_relative_to(REGISTERED_ROOT.absolute()):
        raise ValueError("Output must stay inside the registered external-tests root")
    for part in (path,*path.parents):
        if part.exists() or part.is_symlink():
            st=part.lstat()
            if part.is_symlink() or getattr(st,"st_file_attributes",0)&0x400:
                raise ValueError("Reparse evidence/output path")
    return path

def read_transport(directory):
    directory=safe_path(directory)
    result={};originals={}
    for name in NAMES:
        candidates=[directory/(name+".b64")]
        if name in ALIASES:candidates.append(directory/ALIASES[name])
        present=[safe_path(p) for p in candidates if p.exists()]
        if len(present)!=1:raise ValueError("Exactly one Base64 source required for "+name)
        source=present[0];encoded=source.read_bytes()
        compact=b"".join(encoded.split())
        raw=base64.b64decode(compact,validate=True)
        if name!="stderr.bin" and not raw:raise ValueError("Empty original: "+name)
        result[name]=raw;originals[name]={"path":source,"encoded":encoded}
    return result,originals

def validate_bytes(raw):
    proof=json.loads(raw["process-exit.json"])
    summary=json.loads(raw["receiver.jsonl.summary.json"])
    rows=[json.loads(line) for line in raw["receiver.jsonl"].splitlines() if line.strip()]
    # Stdout is checked without reserializing or altering the original bytes.
    stdout=[json.loads(line) for line in raw["stdout.bin"].decode("utf-8").splitlines() if line.strip()]
    if proof.get("schema")!="witness-process-exit-v1" or proof.get("mode")!="SERVE":
        raise ValueError("Expected a SERVE parent-process receipt")
    round_name=proof.get("round");capture_id=proof.get("capture_id")
    if not isinstance(round_name,str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}",round_name):
        raise ValueError("Invalid round name")
    if not isinstance(capture_id,str) or not re.fullmatch("[0-9a-f]{32}",capture_id):
        raise ValueError("Invalid capture identifier")
    hashes=proof.get("files",{})
    if not isinstance(hashes,dict) or set(hashes)!=set(NAMES[:-1]):
        raise ValueError("Incomplete parent-process file hash set")
    if any(hashes[name]!=digest(raw[name]) for name in NAMES[:-1]):
        raise ValueError("Original bytes differ from parent-process hashes")
    if summary.get("log_sha256")!=digest(raw["receiver.jsonl"]):
        raise ValueError("Summary/log hash mismatch")
    if proof.get("receiver_run_id")!=summary.get("run_id") or not rows:
        raise ValueError("Receiver run mismatch")
    if any(row.get("run_id")!=summary["run_id"] for row in rows):
        raise ValueError("Mixed receiver runs")
    if len(stdout)!=2 or stdout[0] not in rows or stdout[0].get("kind")!="listening" or stdout[1]!=summary:
        raise ValueError("Stdout differs from original listening event or summary")
    return round_name+"-"+capture_id

def decode_capture(input_directory,output_parent):
    raw,originals=read_transport(input_directory)
    name=validate_bytes(raw)  # Validate every byte before creating any output.
    parent=safe_path(output_parent,registered=True)
    target=safe_path(parent/name,registered=True)
    if target.exists():raise FileExistsError("Capture already exists; never overwrite")
    parent.mkdir(parents=True,exist_ok=True);safe_path(parent,registered=True)
    staging=safe_path(parent/(".decode-stage-"+uuid.uuid4().hex),registered=True)
    staging.mkdir(exist_ok=False)
    try:
        for name in NAMES:
            with (staging/name).open("xb") as stream:stream.write(raw[name])
        for name in NAMES:
            if (staging/name).read_bytes()!=raw[name]:raise ValueError("Output byte verification failed")
            if originals[name]["path"].read_bytes()!=originals[name]["encoded"]:
                raise ValueError("Transport changed during intake")
        receipt={"schema":"witness-lossless-decode-v1","qualification":"INTEGRITY_ONLY",
                 "files":{name:{"bytes":len(raw[name]),"sha256":digest(raw[name]),
                                "transport_sha256":digest(originals[name]["encoded"])} for name in NAMES},
                 "production":"CLOSED","native_acceptance":False,"certificate_written":False}
        with (staging/"decode-receipt.json").open("x",encoding="utf-8",newline="\n") as stream:
            json.dump(receipt,stream,indent=2);stream.write("\n")
        # Both resolved targets are checked before this single-shell local rename.
        safe_path(staging,registered=True);safe_path(target,registered=True)
        if target.exists():raise FileExistsError("Capture appeared during intake")
        if not staging.resolve().is_relative_to(REGISTERED_ROOT.resolve()) or not target.resolve().is_relative_to(REGISTERED_ROOT.resolve()):
            raise ValueError("Resolved publication target escaped the registered root")
        staging.rename(target)
        return {"status":"DECODED_INTEGRITY_ONLY","path":str(target),**receipt}
    except Exception:
        # Retain owned partial staging for diagnosis; never delete or publish it.
        raise

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute",action="store_true")
    parser.add_argument("--input-directory",type=Path)
    parser.add_argument("--output-parent",type=Path)
    args=parser.parse_args(argv)
    if not args.execute:
        print(json.dumps({"status":"PLAN","writes":False,"required":"--execute --input-directory DIR --output-parent REGISTERED_DIR","production":"CLOSED"}))
        return 3
    try:
        if args.input_directory is None or args.output_parent is None:
            raise ValueError("Explicit input and registered output parent are required")
        result=decode_capture(args.input_directory,args.output_parent)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"status":"NOT_DECODED","error_type":type(exc).__name__,"detail":str(exc),
                          "production":"CLOSED","native_acceptance":False},ensure_ascii=False))
        return 2
if __name__=="__main__":
    raise SystemExit(main())
