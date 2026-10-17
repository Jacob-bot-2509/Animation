from pathlib import Path
import ast, hashlib, json, sys
ROOT=Path(r"D:\Animation-Model-Training")
OUT=ROOT/"archives/reviews/codex-supervision/2026-10-17-executor-isolation-inventory-review"
BASE=ROOT/"reviews/data-prep/2026-10-17-submission"
audit=json.loads((OUT/"readonly-audit.stdout.json").read_text(encoding="utf-8"))
inv=json.loads((BASE/"exec-isolation/exec-isolation-bounded-inventory-v1.json").read_text(encoding="utf-8"))
checked={}
def verify(item):
    p=ROOT/item["path"]
    b=p.read_bytes()
    assert hashlib.sha256(b).hexdigest()==item["sha256"],str(p)
    if "bytes" in item:assert type(item["bytes"]) is int and len(b)==item["bytes"]
    checked[item["path"]]={"bytes":len(b),"sha256":item["sha256"]}
for item in inv["bound_files_current"]+inv["collector_scripts"]:verify(item)
for row in inv["existing_raw_receipts_index"]:
    members=row.get("expanded_members",[row])
    if "*" in row["path"]:
        actual=sorted(p.relative_to(ROOT).as_posix().rstrip("/") for p in ROOT.glob(row["path"]))
        assert actual==sorted(x["path"] for x in members)
        assert row["count"]==len(members)
    for item in members:
        if "files" in item:
            p=ROOT/item["path"]
            assert sorted(x.name for x in p.iterdir() if x.is_file())==sorted(Path(x["path"]).name for x in item["files"])
            for f in item["files"]:verify(f)
        else:verify(item)
for run in audit["historical_runs"]:verify(run["binding"])
for transport in audit["transports"]:
    for f in transport["original_files"]:
        assert f["status"]=="CHECKED"
        verify(f["value"])
for media in audit["media"]:
    b=media["expected"];verify({"path":Path(b["path"]).relative_to(ROOT).as_posix(),"sha256":b["sha256"],"bytes":b["size"]})
assert hashlib.sha256((ROOT/inv["independent_readonly_audit"]["audit_path"]).read_bytes()).hexdigest()==inv["independent_readonly_audit"]["audit_sha256"]
assert len(inv["bound_files_current"])==15 and len(inv["collector_scripts"])==3
assert inv["independent_readonly_audit"]["surface_checkpoint_file_count"]==23
assert inv["independent_readonly_audit"]["surface_final_run_count"]==3
assert inv["independent_readonly_audit"]["current_surface_counts"]=={"GREEN":30,"PARTIAL":2,"GAP":11,"FAIL":0}
assert len(audit["transports"])==40 and audit["summary"]["parent_record_field_checks_pass"]==40
assert audit["summary"]["media_exact_matches"]==4
assert not (ROOT/"data/execution_evidence.json").exists()
assert audit["bound_file_set_exact"] and audit["required_cases_exact"]
# Bind unchanged execution/fixture entry points; no repeated tests of unchanged code.
unchanged={
"eval_protocol.py":"5ca2d82f35daa8a1ebfe31ba971cb0e185bce48cb49d1aeca0b0c1e617a31b73",
"fixture_executor.py":"b0f75a2407b5997d6e92037560d33653d43fd22ad932c194073c90e4a000038c",
"run_fixtures.py":"9c6a88621d48712022df0d321785ff3bfbaa2447b89a2df465c52464f5289a93"}
for name,sha in unchanged.items():
    verify({"path":str((BASE/"eval-wiring"/name).relative_to(ROOT)).replace("\\","/"),"sha256":sha})
result={"schema":"bounded-review-final-verification-v1","verified_unique_source_and_raw_files":len(checked),
        "all_recorded_raw_files_preserved":True,"current_execution_certificate_exists":False,
        "current_transport_binding_count":15,"collector_binding_count":3,
        "static_and_binding_assertions":"PASS","new_native_experiments":0,"generated_code_executions":0,
        "unchanged_fixture_tests_not_repeated":True,"files":checked}
print(json.dumps(result,ensure_ascii=False,indent=2))
