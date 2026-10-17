"""Static candidate preparation only. Never renders, executes scenes or approves assets.
Family uniqueness uses explicit problem_id / ID suffix, NOT semantic leakage proof.
All selected records bind exact current JSONL bytes and unchanged upstream evidence.
"""
from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path

ROOT=Path(__file__).absolute().parents[4]
HERE=Path(__file__).absolute().parent
LABELS={
 "A":"spec_step_text_truncated_at_28_characters",
 "B":"spec_steps_after_fifth_omitted",
 "C":"text_answer_not_displayed",
 "D":"problem_replaced_by_formula_extraction_failure_placeholder",
 "E":"tex_in_Text_not_typeset_as_MathTex",
 "F":"historical_decimal_literals_need_fraction_display_adapter",
 "G":"fixed_template_geometry_requires_record_specific_validation",
}
REQUIRED=set(LABELS)
HEX=re.compile(r"[0-9a-f]{64}")
SAFE_ID=re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}")

def sha(data):return hashlib.sha256(data).hexdigest()
def encoded(value):return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=True).encode()

def checked_path(value,*,root=ROOT):
    if type(value) is not str or not value or any(x in (".","..") for x in value.replace("\\","/").split("/")):
        raise ValueError("noncanonical_input_path")
    p=Path(value)
    if not p.is_absolute() or not p.is_relative_to(root):
        raise ValueError("input_outside_project")
    rel=p.relative_to(root).as_posix()
    if not re.fullmatch(r"[A-Za-z0-9_./-]+",rel) or ":" in rel:
        raise ValueError("input_path_alias")
    for q in (p,*p.parents):
        if q.exists() or q.is_symlink():
            st=q.lstat()
            if q.is_symlink() or getattr(st,"st_file_attributes",0)&0x400:
                raise ValueError("input_reparse")
        if q==root:break
    return p

def bind_record(sid,evidence,*,root=ROOT,cache=None):
    if type(sid) is not str or not SAFE_ID.fullmatch(sid) or type(evidence) is not dict:
        raise ValueError("record_identity")
    cache={} if cache is None else cache
    source=evidence["source"];p=checked_path(source["path"],root=root)
    if not p.is_relative_to(root/"data") or p.suffix!=".jsonl":
        raise ValueError("not_dataset_jsonl")
    if p not in cache:
        data=p.read_bytes()
        if len(data)>32*1024*1024:raise ValueError("dataset_too_large")
        cache[p]=(data,data.splitlines(keepends=True),sha(data))
    data,lines,file_sha=cache[p]
    if source.get("sha256")!=file_sha:raise ValueError("source_file_sha_mismatch")
    n=source.get("line")
    if type(n) is not int or not 1<=n<=len(lines):raise ValueError("source_line_invalid")
    line=lines[n-1];record=json.loads(line)
    if type(record) is not dict or record.get("id")!=sid:raise ValueError("source_record_id_mismatch")
    family=record.get("problem_id") or re.sub(r"-s\d+$","",sid)
    if type(family) is not str or not SAFE_ID.fullmatch(family):raise ValueError("family_identity")
    errors=evidence.get("errors",[]);warnings=evidence.get("warnings",[])
    if type(errors) is not list or type(warnings) is not list or any(type(x) is not str for x in errors+warnings):
        raise ValueError("label_shape")
    tags=sorted(k for k,v in LABELS.items() if v in (errors if k in "ABCD" else warnings))
    claims=evidence.get("input_sha256")
    if type(claims) is not str or not HEX.fullmatch(claims):raise ValueError("upstream_claim_sha")
    return {
        "sample_id":sid,"family_key":family,
        "family_key_source":"explicit_problem_id" if record.get("problem_id") else "id_suffix_rule",
        "tags":tags,"errors":sorted(set(errors)),"warnings":sorted(set(warnings)),
        "source":{"path":p.relative_to(root).as_posix(),"line":n,"file_sha256":file_sha,
                  "raw_line_sha256":sha(line),"raw_line_includes_terminator":True,
                  "canonical_record_sha256":sha(encoded(record))},
        "upstream_input_sha256_claim":claims,
        "math_review":"PENDING","semantic_review":"PENDING","render_review":"PENDING",
    }

def choose(rows,count=10):
    if type(count) is not int or count<1:raise ValueError("invalid_count")
    if type(rows) is not list:raise ValueError("rows_type")
    seen_ids=set()
    for row in rows:
        if row["sample_id"] in seen_ids:raise ValueError("duplicate_sample_id")
        seen_ids.add(row["sample_id"])
        if not set(row["tags"])<=REQUIRED:raise ValueError("unknown_tag")
    pending=[r for r in rows if r["tags"]]
    picked=[];covered=set();families=set()
    while len(picked)<count:
        possible=[r for r in pending if r["family_key"] not in families]
        if not possible:break
        # Stable tie-breaking; gain is recomputed after every selection.
        possible.sort(key=lambda r:(-len(set(r["tags"])-covered),-len(r["tags"]),
                                    -len(r["errors"]),r["sample_id"]))
        row=possible[0];picked.append(row);families.add(row["family_key"])
        covered.update(row["tags"])
    # Recompute from actual final rows, never maintain a partial coverage counter.
    covered=set().union(*(set(r["tags"]) for r in picked)) if picked else set()
    if len(picked)!=count or covered!=REQUIRED:
        raise ValueError("insufficient_distinct_families_or_fault_coverage")
    return picked,sorted(covered)

def bind_candidates(records, *, root=ROOT):
    rows=[]; rejected=[]; cache={}
    for sid,value in sorted(records.items()):
        try:
            rows.append(bind_record(sid,value,root=root,cache=cache))
        except (ValueError,KeyError,TypeError,OSError) as exc:
            rejected.append({"sample_id":sid,"reason":str(exc),"status":"QUARANTINED_NOT_ELIGIBLE"})
    return rows,rejected,cache

def build(evidence_path=None):
    evidence_path=ROOT/"data/asset_evidence.json" if evidence_path is None else evidence_path
    raw=evidence_path.read_bytes();ev=json.loads(raw);records=ev["records"]
    if type(records) is not dict or ev.get("n_total_records")!=len(records):
        raise ValueError("evidence_count")
    template=(ROOT/"tools/render_templates.py").read_bytes()
    if ev.get("template_sha256")!=sha(template):raise ValueError("stale_template")
    rows,rejected,cache=bind_candidates(records,root=ROOT)
    selected,covered=choose(rows)
    # Changes observed during the preparation window reject output.
    if evidence_path.read_bytes()!=raw or (ROOT/"tools/render_templates.py").read_bytes()!=template:
        raise ValueError("inputs_changed")
    for path,(data,_,_) in cache.items():
        if path.read_bytes()!=data:raise ValueError("dataset_changed")
    return {"schema":"asset-first-batch-v2","batch":"first-batch-10",
            "purpose":"STATIC_CANDIDATE_PREPARATION_NOT_RENDER_AUTHORIZATION",
            "evidence_sha256":sha(raw),"template_sha256":sha(template),
            "selector_sha256":sha(Path(__file__).read_bytes()),
            "covered_types":covered,"uncovered_types":[],
            "family_dedup_scope":"EXPLICIT_PROBLEM_ID_OR_ID_SUFFIX_ONLY",
            "semantic_core_uniqueness":"NOT_ESTABLISHED",
            "records":selected,"quarantined_records":rejected,
            "source_bound_records":len(rows),"fault_candidate_records":sum(bool(r["tags"]) for r in rows),
            "production":"CLOSED"}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output-name",default="first-batch-10.v2.json")
    args=parser.parse_args()
    if not re.fullmatch(r"first-batch-10(?:[a-zA-Z0-9_.-]*)\.json",args.output_name):
        raise ValueError("unsafe_output_name")
    out=HERE/args.output_name
    for q in (HERE,*HERE.parents):
        if (q/"delivery-manifest.json").exists():raise ValueError("frozen_output")
        if q==ROOT:break
    checked_path(str(out))
    result=build()
    with out.open("x",encoding="utf-8",newline="\n") as f:
        json.dump(result,f,ensure_ascii=False,indent=2)
    print(json.dumps({"output":str(out),"records":len(result["records"]),
                      "covered_types":result["covered_types"],"status":"PREPARATION_ONLY"}))
    return 0

if __name__=="__main__":raise SystemExit(main())
