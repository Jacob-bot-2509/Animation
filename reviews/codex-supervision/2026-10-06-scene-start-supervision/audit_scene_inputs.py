"""Independent read-only scene workflow input audit; no semantic/visual approval."""
from pathlib import Path
import collections
import datetime
import hashlib
import json
import sys
ROOT=Path(__file__).resolve().parents[3]
sys.path[:0]=[str(ROOT/"tools"),str(ROOT/"src")]
from holdout_contract import Snapshot,json_object,strict_json,object_sha,raw_sha
from draft_io import selected_path,fingerprint,NORMALIZED_HASH
OUT=Path(__file__).resolve().parent
DRAFTS=ROOT/"reviews/2026-10-05-training-diversity-drafts"
CHUNKS=ROOT/"reviews/2026-10-06-scene-standard-sweep/chunks"
s=Snapshot(ROOT)
selection_raw=s.read(DRAFTS/"draft-selection.json")
selection=json_object(selection_raw)
assert selection["schema"]==2 and selection["hash_algorithm"]==NORMALIZED_HASH
records={}
ordered=[]
for entry in selection["entries"]:
    path=selected_path(DRAFTS,entry)
    data=s.read(path);fp=fingerprint(data)
    assert fp["raw_sha256"]==entry["raw_sha256"] and fp["sha256"]==entry["sha256"],entry["batch"]
    rows=[json_object(line.encode("utf-8")) for line in data.decode("utf-8-sig").splitlines() if line.strip()]
    assert len(rows)==entry["count"]
    for index,row in enumerate(rows):
        assert row["id"] not in records
        records[row["id"]]=(entry,path,index,row)
        ordered.append(row["id"])
listing=json_object(s.read(CHUNKS/"listing.json"))
assert listing["selection_sha256"]==raw_sha(selection_raw)
assert listing["records"]==len(records)==264
assert set(listing["chunks"])=={p.name for p in CHUNKS.glob("chunk-*.json")}
checked=[]
seen=set()
chunks=[]
standards=set()
for name,digest in sorted(listing["chunks"].items()):
    path=(CHUNKS/name).resolve();assert path.parent==CHUNKS.resolve()
    data=s.read(path);assert raw_sha(data)==digest,name
    packet=json_object(data);standards.add(packet["standard"])
    items=packet["records"];assert isinstance(items,list)
    chunks.append({"path":path.relative_to(ROOT).as_posix(),"raw_sha256":digest,"record_count":len(items)})
    for item in items:
        pid=item["id"];assert pid in records and pid not in seen,pid
        seen.add(pid)
        assert type(item["idx"]) is int and item["idx"]==len(checked),pid
        assert ordered[item["idx"]]==pid
        entry,source,index,row=records[pid]
        assert set(item)=={"idx","id","concept_id","category","sub_category","problem","solution","answer","scene_spec"}
        assert all(item[k]==row[k] for k in item if k!="idx"),pid
        checked.append({"id":pid,"idx":item["idx"],"chunk":name,"batch":entry["batch"],"version":entry["version"],
                        "source_path":source.relative_to(ROOT).as_posix(),"source_line":index+1,
                        "source_raw_sha256":entry["raw_sha256"],"source_normalized_sha256":entry["sha256"],
                        "full_record_canonical_sha256":object_sha(row),
                        "mathematics_three_fields_canonical_sha256":object_sha({k:row[k] for k in ("problem","solution","answer")}),
                        "scene_spec_canonical_sha256":object_sha(row["scene_spec"])})
assert seen==set(records) and len(standards)==1
baseline=json_object(s.read(ROOT/"reviews/codex-supervision/2026-10-06-protocol-v3-mail-followup/real-verification.json"))
unchanged=[]
for item in baseline["active_and_core_checks"]:
    digest=raw_sha(s.read(ROOT/item["path"]))
    unchanged.append({"path":item["path"],"raw_sha256":digest,"unchanged":digest==item["raw_sha256"]})
assert all(x["unchanged"] for x in unchanged)
v3=json_object(s.read(ROOT/"reviews/codex-supervision/2026-10-06-protocol-v3-mail-followup/delivery-manifest.json"))
for rel,digest in v3["live_source_hashes"].items():
    assert raw_sha(s.read(ROOT/rel))==digest,rel
s.check_unchanged()
snap=OUT/"input-snapshot";snap.mkdir(exist_ok=False)
for path,data in s.data.items():
    target=snap/path.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True)
    with target.open("xb") as f:f.write(data)
result={"checked_at":datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),
        "status":"INPUT_CONTENT_AND_COVERAGE_MATCH_WITH_EMPTY_CHUNK",
        "selection_raw_sha256":raw_sha(selection_raw),"selected_batches":len(selection["entries"]),
        "selected_records":len(records),"chunk_records_verified":len(checked),"chunk_file_count":len(chunks),
        "nonempty_chunks":sum(c["record_count"]>0 for c in chunks),"empty_chunks":[c["path"] for c in chunks if c["record_count"]==0],
        "identity_order_math_scene_equal":True,"semantic_approval":False,"visual_approval":False,
        "active_and_old_core_checks":unchanged,"previous_v3_sources_unchanged":True,
        "chunks":chunks,"record_bindings":checked,"source_bindings":s.bindings(),
        "new_native_render_or_training":False}
with (OUT/"input-audit.json").open("x",encoding="utf-8") as f:f.write(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k not in ["record_bindings","source_bindings","active_and_old_core_checks","chunks"]},indent=2))
