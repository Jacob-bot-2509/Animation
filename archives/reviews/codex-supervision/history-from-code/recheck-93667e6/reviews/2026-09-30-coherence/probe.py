"""Read-only core contract probes with project-local synthetic files."""
import hashlib
import json
from pathlib import Path
import random
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/"src"),str(ROOT)]
from animtrain.manifest import Manifest,Entry,sha256_file
from animtrain.validate import validate_manifest
from animtrain.near_dup import ShingleIndex
from animtrain.fields import check_fields
from animtrain.fs_guard import valid_run_id
HERE=Path(__file__).resolve().parent
FIX=HERE/"fixtures"
FIX.mkdir(exist_ok=False)
p=FIX/"one.jsonl"
p.write_text('{"id":"one"}\n',encoding="utf-8")
entry=Entry(path=p.name,sha256=sha256_file(p),size=999999,source=" ",
            license="internal-generated",split="train")
results={
 "empty_core_manifest":validate_manifest(Manifest(name="empty"),FIX),
 "wrong_size_and_blank_source":validate_manifest(Manifest(name="probe",entries=[entry]),FIX),
 "empty_containers_in_core_fields":check_fields([{"problem":[],"solution":{},"answer":0}]),
 "run_id_trailing_newline":valid_run_id("run\n")
}
query="abcdefghijklmnopqrstuvwxyz"
idx=ShingleIndex()
for i in range(20):
 rng=random.Random(i)
 idx.add(query+"".join(rng.choices("abcdefghijklmnopqrstuvwxyz",k=500)),{"id":i})
idx.add(query,{"id":"exact"})
results["top20_hides_exact_match"]={"similarity":idx.max_sim(query)[0],
                                  "hit":idx.max_sim(query)[1],"expected":1.0}
results["source_snapshot"]={str(p.relative_to(ROOT)):sha256_file(p)
 for folder in ("src","tools","tests") for p in sorted((ROOT/folder).rglob("*.py"))}
(HERE/"probe_results.json").write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps({k:v for k,v in results.items() if k!="source_snapshot"},
                 ensure_ascii=False,indent=2))
