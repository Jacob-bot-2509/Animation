"""Independent current-text and exact-set audit; does not create new labels."""
import json,hashlib,re,sys
from pathlib import Path
from fractions import Fraction
from collections import defaultdict,Counter
P=Path(r"D:\Animation-Model-Training")
A=P/"archives/reviews/codex-supervision/2026-10-17-b5-readiness-audit"
sys.path.insert(0,str(P/"src"))
from animtrain.kp_rule import kp_signature
from animtrain.validate import NEAR_DUP_TEXT_THRESHOLD,NEAR_DUP_RULE
def sha(b):return hashlib.sha256(b).hexdigest()
def gram(t):
    t=re.sub(r"[\s$\\_{}\[\]()]","",t).lower()
    return ({t} if t else set()) if len(t)<5 else {t[i:i+5] for i in range(len(t)-4)}
def ratio(a,b):return Fraction(len(a&b),len(a|b)) if a and b else Fraction(0)
ann_path=P/"data/b5-annotation-set/b5-annotation-set.json"
report_path=P/"data/b5-calibration-report/b5-calibration-report.json"
ann=json.loads(ann_path.read_text(encoding="utf-8"));report=json.loads(report_path.read_text(encoding="utf-8"))
assert report["annotation_sha256"]==sha(ann_path.read_bytes())
current=defaultdict(list)
for name in ("data/v2/eval/dataset_eval.jsonl","data/v2/test/dataset_test.jsonl"):
    raw=(P/name).read_bytes()
    for no,line in enumerate(raw.splitlines(keepends=True),1):
        if not line.strip():continue
        record=json.loads(line)
        for key in {record.get("id"),record.get("problem_id")}-{None}:
            current[key].append((record,{"path":name,"line":no,"file_sha256":sha(raw),"raw_line_sha256":sha(line)}))
seen=set();prepared=[];bindings=[]
for pair in ann["pairs"]:
    identity=tuple(sorted((pair["a"],pair["b"])))
    assert pair["a"]!=pair["b"] and identity not in seen
    seen.add(identity);sig={}
    for side in ("a","b"):
        matches=[(r,b) for r,b in current[pair[side]] if r.get("problem")==pair["text_"+side]]
        assert matches
        signatures={kp_signature(r) for r,b in matches};assert len(signatures)==1
        sig[side]=next(iter(signatures))
        bindings.append({"pair":list(identity),"side":side,"id":pair[side],"current_exact_sources":[b for r,b in matches]})
    ga,gb=gram(pair["text_a"]),gram(pair["text_b"])
    score=ratio(ga,gb)
    ta={("category",sig["a"][0]),("kind",sig["a"][1])}
    tb={("category",sig["b"][0]),("kind",sig["b"][1])}
    prepared.append({"a":pair["a"],"b":pair["b"],"label":pair["label"],
                     "j5":str(score),"kp_j":str(ratio(ta,tb)),
                     "intersection":len(ga&gb),"union":len(ga|gb),
                     "kp_a":" ".join(sig["a"]),"kp_b":" ".join(sig["b"])})
labeled=[r for r in prepared if r["label"]!="不确定"]
def evaluate(predicate):
    tp=fp=fn=tn=0
    for row in labeled:
        pred=predicate(row);positive=row["label"]=="重复"
        if positive:tp+=pred;fn+=not pred
        else:fp+=pred;tn+=not pred
    return {"tp":tp,"fp":fp,"fn":fn,"tn":tn,
            "precision":str(Fraction(tp,tp+fp)) if tp+fp else None,
            "recall":str(Fraction(tp,tp+fn)) if tp+fn else None,
            "fpr":str(Fraction(fp,fp+tn)) if fp+tn else None,
            "fnr":str(Fraction(fn,fn+tp)) if fn+tp else None}
threshold=Fraction(str(NEAR_DUP_TEXT_THRESHOLD))
signature=evaluate(lambda r:Fraction(r["kp_j"])==1)
combined=evaluate(lambda r:Fraction(r["kp_j"])==1 and Fraction(r["j5"])>=threshold)
for key,value in signature.items():assert report["calibration"][key]==value
for key,value in combined.items():
    assert report["leakage_screen_calibration"]["recall_all_labels" if key=="recall" else key]==value
by_pair={(r["a"],r["b"]):r for r in report["pairs"]}
for row in labeled:
    old=by_pair[(row["a"],row["b"])]
    for key in ("j5","kp_j","kp_a","kp_b","label"):assert old[key]==row[key]
    assert old["similarity_counts"]=={"intersection":row["intersection"],"union":row["union"]}
for table,key in (("grid_kp","kp_j"),("grid_5gram_contrast","j5")):
    for old in report[table]:
        t=Fraction(old["threshold"]);counts=evaluate(lambda r:Fraction(r[key])>=t)
        for field,value in counts.items():assert old[field]==value
false_negatives=[r for r in labeled if r["label"]=="重复" and not(Fraction(r["kp_j"])==1 and Fraction(r["j5"])>=threshold)]
result={"annotation_pairs":len(prepared),"unique_pairs":len(seen),"labels":dict(Counter(r["label"] for r in prepared)),
        "current_exact_text_references":len(bindings),"signature_diagnostic":signature,
        "executed_b5_rule":NEAR_DUP_RULE,"threshold":str(threshold),"combined_diagnostic":combined,
        "all_stored_report_counts_and_grids_match":True,"missed_positive_pairs":false_negatives,
        "recall_goal":"19/20","recall_shortfall":str(Fraction(19,20)-Fraction(combined["recall"])),
        "formal_calibration":"NOT_ESTABLISHED","independent_label_evidence":"MISSING",
        "near_dup_calibrated":False,"production":"CLOSED"}
(A/"independent-exact-audit.json").write_text(json.dumps(result,ensure_ascii=True,indent=2))
(A/"current-exact-source-bindings.json").write_text(json.dumps(bindings,ensure_ascii=True,indent=2))
print(json.dumps(result,ensure_ascii=True,indent=2))
