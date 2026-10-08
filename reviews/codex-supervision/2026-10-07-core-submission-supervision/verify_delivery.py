"""Verify delivered corrections, identities, raw preservation and code binding."""
from pathlib import Path
import importlib.util,json,hashlib,zipfile
from collections import Counter
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("diagnostics",ROOT/"tools/core_scope_consistency_check.py")
cc=importlib.util.module_from_spec(spec);spec.loader.exec_module(cc)
def sha(data):return hashlib.sha256(data).hexdigest()
def readjl(path):return [json.loads(x) for x in path.read_text(encoding="utf-8-sig").splitlines() if x.strip()]
bound,sources=cc.load_bound_rows()
snap=readjl(OUT/"corrected-core-761.jsonl");patches=readjl(OUT/"math-corrections-30.jsonl")
assert len(bound)==len(snap)==761 and len(patches)==30
patch_map={(x["source"]["source_path"],x["source"]["source_line"]):x for x in patches}
changed=0
for (ref,before),row in zip(bound,snap):
 assert ref==row["source"]
 key=(ref["source_path"],ref["source_line"]);after=row["record"]
 assert sha(cc.canonical(after))==row["record_dense_sha256"]
 if key in patch_map:
  p=patch_map[key]
  assert before["id"]==after["id"]==p["id"]
  assert cc.digest(cc.canonical(before))==p["before_record_dense_sha256"]
  assert cc.digest(cc.canonical(after))==p["after_record_dense_sha256"]
  assert {k:v for k,v in before.items() if k not in ("problem","solution","answer")}=={k:v for k,v in after.items() if k not in ("problem","solution","answer")}
  assert after==p["corrected_record"]
  changed+=1
 else:assert before==after
 assert not cc.check_record(after,ref)["issues"]
assert changed==30
candidate_bindings=json.loads((OUT/"candidate-source-bindings.json").read_text(encoding="utf-8"))
assert len(candidate_bindings)==5
for candidate in candidate_bindings:
 before=ROOT/candidate["before"]["path"];after=ROOT/candidate["candidate"]["path"]
 b=before.read_bytes();a=after.read_bytes()
 for raw,expected in ((b,candidate["before"]),(a,candidate["candidate"])):
  assert sha(raw)==expected["raw_sha256"] and len(raw)==expected["bytes"]
 bl=b.splitlines(keepends=True);al=a.splitlines(keepends=True)
 assert len(bl)==len(al)
 source_path=candidate["before"]["path"]
 for line,(lb,la) in enumerate(zip(bl,al),1):
  key=(source_path,line)
  if key in patch_map:assert json.loads(la.decode("utf-8-sig"))==patch_map[key]["corrected_record"]
  else:assert lb==la
packet=ROOT/cc.PACKET
manifest=json.loads((packet/"delivery-manifest.json").read_text(encoding="utf-8"))
for entry in manifest["artifacts"]:
 data=(packet/entry["path"]).read_bytes()
 assert sha(data)==entry["raw_sha256"] and len(data)==entry["bytes"]
with zipfile.ZipFile(packet/"claude-core-evidence.zip") as archive:
 expected={x["path"] for x in manifest["artifacts"]}|{"delivery-manifest.json"}
 assert set(archive.namelist())==expected and len(archive.namelist())==len(expected)==55
 assert archive.read("delivery-manifest.json")==(packet/"delivery-manifest.json").read_bytes()
 for entry in manifest["artifacts"]:assert sha(archive.read(entry["path"]))==entry["raw_sha256"]
 assert archive.testzip() is None
reg=json.loads((OUT/"regression-validation.json").read_text(encoding="utf-8"))
for relative,k in (("tools/core_scope_consistency_check.py","tested_implementation"),("tests/test_core_scope_consistency_check.py","tested_suite")):
 data=(ROOT/relative).read_bytes();expected=reg[k]
 assert sha(data)==expected["raw_sha256"] and len(data)==expected["bytes"]
assert reg["result"]["value"]["exit_code"]==0 and "27 passed" in reg["result"]["value"]["output"]
exact=json.loads((OUT/"exact-math-verification.json").read_text(encoding="utf-8"))
assert exact["distinct_reviewed_records"]==30 and exact["check_count"]==31
assert {x["id"] for x in exact["checks"]}=={x["id"] for x in patches}
for item in exact["checks"]:
 p=next(p for p in patches if p["id"]==item["id"])
 assert item["candidate_record_dense_sha256"]==p["after_record_dense_sha256"]
submission=ROOT/"reviews/2026-10-07-gap-materials/core-submission-v1"
for name in ("core-scope-review.md","review-receipts.jsonl","consistency-report.jsonl","submission-index.json"):
 assert (submission/name).read_bytes()==(OUT/"before"/("submission-final-"+name)).read_bytes()
for item in json.loads((OUT/"retained-support-bindings.json").read_text(encoding="utf-8")):
 data=(ROOT/item["retained_copy"]["path"]).read_bytes()
 assert sha(data)==item["original"]["raw_sha256"] and len(data)==item["original"]["bytes"]
result={"result":"PASS_DELIVERY_INTEGRITY_AND_SCOPED_CORRECTION_VERIFICATION",
 "total_bound_rows":761,"modified_math_rows":30,"other_records_fully_preserved":731,
 "changed_source_files":5,"unchanged_source_line_bytes":"PRESERVED","source_versions_verified":24,
 "packet_originals_unchanged":54,"zip_members_verified":55,"old_submission_preserved":True,
 "regression_tests":27,"exact_math_checks":31,"scoped_math_reviewed_records":30,"after_format_flag_rows":0,
 "full_761_mathematical_verdict":"NOT_ESTABLISHED","semantic_isolation_verdict":"NOT_ESTABLISHED",
 "current_data_admission":"PENDING","PASS_CORE_SCOPE_issued":False,"production":"CLOSED"}
with (OUT/"final-verification.json").open("x",encoding="utf-8",newline="\n") as f:
 json.dump(result,f,ensure_ascii=False,indent=2);f.write("\n")
print(json.dumps(result,ensure_ascii=False))
