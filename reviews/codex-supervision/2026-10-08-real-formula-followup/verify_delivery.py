"""Verify the frozen formula review archive and its immutable mathematical parents."""
import argparse, hashlib, json
from pathlib import Path
from collections import Counter
PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[2]
CORE = ROOT/"reviews/codex-supervision/2026-10-07-deep-isolation-followup/effective-core-v3"
CORE_SHA = "e66ca4f1835667801cc20502818dbf3398308634e8dc2b9a7f1b182ba3805eda"
PARENTS = [
    ("reviews/codex-supervision/2026-10-07-deep-isolation-followup", "f6cab02af67fdde59987323f74db43081c921c418bee1862e464d7348f1693ac"),
    ("reviews/codex-supervision/2026-10-07-semantic-signature-supervision", "4e2ae6741592386d93be6cf01cbe8cabb13e3fd002d99b0617675d37a4ea24a5"),
    ("reviews/codex-supervision/2026-10-07-continuous-math-review/current-core", "972bd216b713bec7c48896e8f144d999dd6385b8c0e3e00a4c0116dfd1bbca22")
]
def read(p): return json.loads(p.read_text(encoding="utf-8-sig"))
def digest(raw): return hashlib.sha256(raw).hexdigest()
def sha(p): return digest(p.read_bytes())
def require(ok, message):
    if not ok: raise ValueError(message)
def inside(base, relative):
    p=(base/relative).resolve()
    require(p.is_relative_to(base.resolve()), "Path escaped archive")
    return p
def manifest(base, expected, strict=False):
    p=base/"delivery-manifest.json"
    require(sha(p)==expected, "Manifest hash changed: "+str(base))
    x=read(p); seen=set()
    for b in x["artifacts"]:
        require(b["path"] not in seen, "Duplicate artifact")
        seen.add(b["path"])
        f=inside(base,b["path"])
        require(f.is_file() and sha(f)==b["sha256"] and f.stat().st_size==b["bytes"], "Artifact changed: "+str(f))
    if strict:
        actual={p.relative_to(base).as_posix() for p in base.rglob("*") if p.is_file()}
        require(actual==seen|{"delivery-manifest.json"}, "Unexpected or omitted archive files")
    return len(seen)
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--expected-sha256", required=True)
    p.add_argument("--check-live-sources", action="store_true")
    a=p.parse_args()
    require(ROOT.name=="Animation-Model-Training", "Wrong project")
    count=manifest(PACKAGE,a.expected_sha256,True)
    parents={rel:manifest(ROOT/rel,expected) for rel,expected in PARENTS}
    core_count=manifest(CORE,CORE_SHA)
    bs=[json.loads(l) for l in (CORE/"record-bindings.jsonl").read_text(encoding="utf-8-sig").splitlines() if l.strip()]
    by={b["id"]:b for b in bs}
    require(len(bs)==len(by)==761,"Core identity count")
    sources={}
    groups=Counter()
    for b in bs:
        source=inside(ROOT,b["path"])
        if b["path"] not in sources:
            raw=source.read_bytes();require(digest(raw)==b["source_sha256"],"Actual source changed")
            sources[b["path"]]=[json.loads(l) for l in raw.decode("utf-8-sig").splitlines() if l.strip()]
        record=sources[b["path"]][b["source_line"]-1]
        require(record["id"]==b["id"],"Actual record identity")
        require(digest(json.dumps(record,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8"))==b["record_sha256"],"Actual record hash")
        math={k:record.get(k) for k in ("problem","solution","answer","scene_spec")}
        require(digest(json.dumps(math,ensure_ascii=False,sort_keys=True).encode("utf-8"))==b["math_sha256"],"Actual math hash")
        groups[b["group"]]+=1
    require(len(sources)==24 and dict(groups)=={"train":47,"selected_draft":264,"eval":300,"test":150},"Core coverage/groups")
    qualified=[json.loads(l) for l in (PACKAGE/"qualified-records.jsonl").read_text(encoding="utf-8-sig").splitlines() if l.strip()]
    require(len(qualified)==len({x["id"] for x in qualified})==165,"Qualified identities")
    for x in qualified:
        b=by[x["id"]]
        for key in ("record_sha256","math_sha256","source_sha256"):
            require(x[key]==b[key],"Qualified actual version mismatch")
        require(x["status"]=="PASS_LOCAL_COMPLETE_FORMULA_COMPILATION" and x["scope"]=="TRUSTED_LOCAL_MATHTEX_ONLY","Qualified scope")
        v=inside(ROOT,x["mp4_path"]);require(v.is_relative_to(PACKAGE) and v.stat().st_size>0 and sha(v)==x["mp4_sha256"],"Archived video mismatch")
    qual=read(PACKAGE/"QUALIFICATION.json")
    audit=read(PACKAGE/"independent-audit-archived.json")
    require(sha(PACKAGE/"independent-audit-archived.json")==qual["evidence"]["independent_audit_sha256"],"Audit changed")
    require(sha(PACKAGE/"qualified-records.jsonl")==qual["evidence"]["qualified_records_sha256"],"Qualified inventory changed")
    summary=audit["summary"]
    require(summary["target_qualified"]==summary["required_current_target_count"]==163 and summary["claude_qualified"]==156 and not summary["target_pending_ids"],"Target coverage")
    require(sum(x["unique_formulas"] for x in qualified)==2663 and sum(x["source_formula_occurrences"] for x in qualified)==5212,"Formula coverage")
    require(qual["visual_acceptance"]=="NOT_REVIEWED" and qual["native_sandbox"]=="UNVERIFIED" and qual["semantic_isolation"]=="NOT_ESTABLISHED" and qual["production"]=="CLOSED" and qual["PASS_CORE_SCOPE_issued"] is False,"Qualification overclaim")
    tests=read(PACKAGE/"native-cjk-tests.json")
    adv=read(PACKAGE/"adversarial-verification-final.json")
    proof=read(PACKAGE/"probability-exact-witness.json")
    require(tests["tests"]==19 and tests["rc"]==0 and adv["checks"]==adv["passed"]==9,"Test results")
    require(len(proof["checks"])==2 and all(x["pass"] is True for x in proof["checks"]),"Exact witnesses")
    source_live={}
    for b in read(PACKAGE/"final-source-bindings.json"):
        require(sha(PACKAGE/"final-source-snapshot"/b["path"])==b["sha256"],"Snapshot changed")
        if a.check_live_sources:
            source_live[b["path"]]=sha(ROOT/b["path"])==b["sha256"]
    require(all(source_live.values()),"Live reviewed source changed")
    print(json.dumps({"archive_integrity":"PASS","archive_manifest_sha256":a.expected_sha256,
        "archive_artifacts":count,"parent_artifacts":parents,"current_core_artifacts":core_count,
        "current_records":761,"sources":24,"target_records":163,"qualified_records":165,
        "unique_formula_items":2663,"source_formula_occurrences":5212,"pending_target_records":0,
        "renderer_tests":19,"verifier_adversarial_checks":9,"exact_probability_checks":2,
        "live_source_checks":source_live,"scope":"TRUSTED_LOCAL_MATHTEX_ONLY",
        "semantic_isolation":"NOT_ESTABLISHED","production":"CLOSED","PASS_CORE_SCOPE_issued":False}))
if __name__=="__main__": main()
