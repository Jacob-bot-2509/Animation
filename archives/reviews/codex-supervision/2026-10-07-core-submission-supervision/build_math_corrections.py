"""Build versioned math corrections without changing active or frozen inputs."""
from __future__ import annotations
import importlib.util,json,hashlib
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location("core_diagnostics",ROOT/"tools/core_scope_consistency_check.py")
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
def bind(path):
 data=path.read_bytes()
 return {"path":path.relative_to(ROOT).as_posix(),"raw_sha256":hashlib.sha256(data).hexdigest(),"bytes":len(data)}
def write(path,obj,jsonl=False):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open("x",encoding="utf-8",newline="\n") as f:
  if jsonl:
   for row in obj:f.write(json.dumps(row,ensure_ascii=False)+"\n")
  else:json.dump(obj,f,ensure_ascii=False,indent=2);f.write("\n")
def main():
 bound,sources=checker.load_bound_rows()
 fixes=json.loads((OUT/"new-math-fields-21.json").read_text(encoding="utf-8"))
 old=ROOT/"reviews/codex-supervision/2026-10-06-scene-repair-takeover/math-corrected-v1"
 old_ids={"calc-series-015","calc-series-020","linalg-050","linalg-070","prob-038","prob-039","prob-042","prob-043","prob-046"}
 origins={}
 for path in sorted(old.glob("*.jsonl")):
  for i,line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(),1):
   rec=json.loads(line)
   if rec["id"] in old_ids:
    fixes[rec["id"]]={k:rec[k] for k in ("problem","solution","answer")}
    fixes[rec["id"]]["reason"]="旧版精确数学修订仍未进入现役；本轮重新绑定原记录并核对证明。"
    origins[rec["id"]]={**bind(path),"line":i,"record_dense_sha256":checker.digest(checker.canonical(rec))}
 assert len(fixes)==30 and set(origins)==old_ids
 fixes["prob-042"]["answer"]=r"$E(F_n)=p$，$\operatorname{Var}(F_n)=\frac{p(1-p)}n$，$F_n\xrightarrow{P}p$；公平硬币附加条件为 $p=\frac12$。"
 fixes["prob-043"]["answer"]=r"$\frac{\sqrt n(\overline X_n-\mu)}\sigma\xrightarrow{d}N(0,1)$；$\overline X_n\xrightarrow{P}\mu$，极限分布为 $\delta_\mu$；总体为 $N(\mu,\sigma^2)$ 时，有限样本精确有 $\overline X_n\sim N(\mu,\sigma^2/n)$。"
 fixes["prob-046"]["answer"]=r"本图例中 $R_k$ 两两不交，$\bigcup_{k=1}^\infty R_k=[0,1)^2$，且 $\sum_{k=1}^\infty\operatorname{area}(R_k)=\sum_{k=1}^\infty2^{-k}=1$。"
 patches=[];after_rows=[];reports=[];source_patches={};md=["# 30 道核心范围数学正文修订","",
 "输入严格绑定冻结包的 761 条现役/入选记录；修订 30 条，保留其余 731 条的全部字段。",
 "本稿是待准入的正文修订覆盖层。原始包、现役绑定和其他字段保持原样；场景、渲染与隔离复验另需绑定修改后的版本。",
 "未宣称全部 761 条数学正确，也未据格式检查认定同核心隔离通过。",""]
 for ref,before in bound:
  after=dict(before);rid=before["id"]
  if rid in fixes:
   for k in ("problem","solution","answer"):
    if k in fixes[rid]:after[k]=fixes[rid][k]
   changed=[k for k in ("problem","solution","answer") if before[k]!=after[k]]
   assert changed and {k:v for k,v in before.items() if k not in changed}=={k:v for k,v in after.items() if k not in changed}
   patch={"id":rid,"source":ref,"before_record_dense_sha256":checker.digest(checker.canonical(before)),
    "after_record_dense_sha256":checker.digest(checker.canonical(after)),"changed_fields":changed,
    "before_math_fields":{k:before[k] for k in ("problem","solution","answer")},
    "after_math_fields":{k:after[k] for k in ("problem","solution","answer")},
    "reason":fixes[rid]["reason"],"prior_candidate_source":origins.get(rid),
    "mathematical_review":"EXACT_REDERIVATION_REVIEWED","active_admission":"PENDING",
    "leakage_review":"UNREVIEWED_FOR_CORRECTED_VERSION","other_fields":"PRESERVED; scene fields may need a version-bound update",
    "corrected_record":after}
   patches.append(patch)
   source_patches.setdefault(ref["source_path"],{})[ref["source_line"]]=after
   md.extend(["## "+rid,"",fixes[rid]["reason"],"",
    "**题目**："+after["problem"],"","**过程**："+after["solution"],"","**答案**："+str(after["answer"]),""])
  after_rows.append({"source":ref,"record":after,"record_dense_sha256":checker.digest(checker.canonical(after)),
    "active_admission":"PENDING" if rid in fixes else "UNCHANGED"})
  reports.append(checker.check_record(after,ref))
 assert len(patches)==30 and all(x["status"]=="DIAGNOSTIC_ONLY" for x in reports)
 candidates=[]
 for name,changes in sorted(source_patches.items()):
  path=ROOT/name;lines=path.read_bytes().splitlines(keepends=True)
  before_count=0
  for i,line in enumerate(lines,1):
   if line.strip():before_count+=1
   if i in changes:
    ending=b"\r\n" if line.endswith(b"\r\n") else b"\n" if line.endswith(b"\n") else b""
    prefix=b"\xef\xbb\xbf" if i==1 and line.startswith(b"\xef\xbb\xbf") else b""
    lines[i-1]=prefix+json.dumps(changes[i],ensure_ascii=False).encode("utf-8")+ending
  dest=OUT/"corrected-sources"/name;dest.parent.mkdir(parents=True,exist_ok=True)
  with dest.open("xb") as f:f.write(b"".join(lines))
  parsed=[json.loads(x.decode("utf-8-sig")) for x in lines if x.strip()]
  assert len(parsed)==before_count
  for i,after in changes.items():
   assert json.loads(lines[i-1].decode("utf-8-sig"))==after
  candidates.append({"before":bind(path),"candidate":bind(dest),"changed_source_lines":sorted(changes),"unchanged_line_bytes":"PRESERVED"})
 write(OUT/"math-corrections-30.jsonl",patches,True)
 write(OUT/"corrected-core-761.jsonl",after_rows,True)
 write(OUT/"diagnostics-corrected-v2.jsonl",reports,True)
 write(OUT/"candidate-source-bindings.json",candidates)
 with (OUT/"MATH_CORRECTIONS.md").open("x",encoding="utf-8",newline="\n") as f:f.write("\n".join(md)+"\n")
 summary={"scope":"CORE_SCOPE_ONLY","fixed_source_rows":30,"unchanged_source_rows":731,"snapshot_rows":761,
  "groups":dict(Counter(ref["group"] for ref,_ in bound)),"changed_source_files":len(candidates),
  "after_format_counts":dict(Counter(x["status"] for x in reports)),
  "math_reviewed_ids":[p["id"] for p in patches],"full_761_math_verdict":"NOT_ESTABLISHED",
  "corrected_version_leakage_verdict":"UNREVIEWED","scope_acceptance":"PENDING",
  "active_data_changed":False,"frozen_packet_changed":False}
 write(OUT/"correction-summary.json",summary)
 print(json.dumps(summary,ensure_ascii=False))
if __name__=="__main__":main()
