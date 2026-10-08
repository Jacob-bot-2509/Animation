"""Build SHA-bound page review queue; only explicit model verdicts can close pages."""
import json,hashlib,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];OWNER=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"tools"));import core_signatures as core
PARENT=ROOT/"reviews/codex-supervision/2026-10-08-hd-formula-mail-review"
MANIFEST_SHA="12d50e59e50ee53c219be17d080c83a615523c7305ae5c659bec3b7fbacf902b"
INDEX_SHA="6515262a59d7fec20095aacb30a2e0c9dce4cdb26854deaf0690704988d3bfaf"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(cond,msg):
    if not cond:raise ValueError(msg)
def build():
    check(sha(PARENT/"delivery-manifest.json")==MANIFEST_SHA,"Parent changed")
    manifest=json.loads((PARENT/"delivery-manifest.json").read_text("utf-8"))
    for a in manifest["artifacts"]:
        p=core.checked_path(PARENT/a["path"],PARENT);check(sha(p)==a["sha256"]and p.stat().st_size==a["bytes"],"Changed parent artifact")
    check(sha(PARENT/"DELIVERY_INDEX.jsonl")==INDEX_SHA,"Index changed")
    queue=[]
    for record in (json.loads(l)for l in (PARENT/"DELIVERY_INDEX.jsonl").read_text("utf-8").splitlines()):
        inv=json.loads((ROOT/record["formula_inventory_path"]).read_text("utf-8"))
        geometry=json.loads((ROOT/record["geometry_path"]).read_text("utf-8"))
        for page,frame in zip(geometry["pages"],record["canonical_frames"]):
            queue.append({"ordinal":len(queue),"id":record["id"],"page":page["page"],"page_count":record["page_count"],
                          "path":frame["path"],"sha256":frame["sha256"],"kind":page["kind"],"tile":page["tile"],"tile_grid":page["tile_grid"],
                          "record_sha256":record["record_sha256"],"math_sha256":record["math_sha256"],
                          "formulas":[{"index":item["formula_index"]+1,"tex":inv["unique_formulas"][item["formula_index"]]}for item in page["items"]]})
    check(len(queue)==626 and len({(r["id"],r["page"])for r in queue})==626,"Incomplete queue")
    (OWNER/"page-review-queue.json").write_bytes(core.encoded({"parent_manifest_sha256":MANIFEST_SHA,"parent_index_sha256":INDEX_SHA,"pages":queue}))
    print(json.dumps({"pages":len(queue)}))
def load():return json.loads((OWNER/"page-review-queue.json").read_text("utf-8"))["pages"]
def batch(start,count):
    pages=load()[start:start+count]
    for p in pages:check(sha(core.checked_path(ROOT/p["path"],PARENT))==p["sha256"],"Page changed")
    print(json.dumps(pages,ensure_ascii=False))
def record(verdicts):
    queue={p["ordinal"]:p for p in load()}
    log=OWNER/"page-glyph-verdicts.jsonl"
    old=[json.loads(l)for l in log.read_text("utf-8").splitlines()]if log.exists()else[]
    seen={v["ordinal"]for v in old}
    check(verdicts and len({v["ordinal"]for v in verdicts})==len(verdicts),"Empty/duplicate verdicts")
    validated=[]
    for v in verdicts:
        n=v["ordinal"];check(n in queue and n not in seen,"Unknown/already reviewed")
        p=queue[n];check(sha(core.checked_path(ROOT/p["path"],PARENT))==p["sha256"],"Changed reviewed PNG")
        check(v["status"]in ("PASS","FAIL","NEEDS_DETAIL"),"Invalid verdict")
        check(v["symbols_checked"]==[f["index"]for f in p["formulas"]],"Missing formula symbol verdicts")
        check(isinstance(v["notes"],str)and bool(v["notes"].strip()),"Missing actual image observations")
        check(v["segment_judgment"]==("PARTIAL_LABELLED_VIEW"if p["kind"]=="FORMULA_SEGMENT"else"FULL_FORMULAS"),"Wrong segment judgment")
        validated.append({**p,**v,"review_method":"MODEL_ACTUAL_IMAGE_INSPECTION_PLUS_BOUND_TEX_COMPARISON",
                          "display_preview":"2048x1152; original bound PNG is 3840x2160"})
    with log.open("ab")as out:
        for v in validated:out.write((json.dumps(v,ensure_ascii=False,sort_keys=True)+"\n").encode("utf-8"))
    print(json.dumps({"recorded":len(validated),"total":len(old)+len(validated)}))
if __name__=="__main__":
    if sys.argv[1]=="build":build()
    elif sys.argv[1]=="batch":batch(int(sys.argv[2]),int(sys.argv[3]))
    elif sys.argv[1]=="record":record(json.load(sys.stdin))
