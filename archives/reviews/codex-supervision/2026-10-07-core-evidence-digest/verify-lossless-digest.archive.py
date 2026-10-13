
from pathlib import Path
import json,hashlib,collections,zipfile,datetime
R=Path(r'D:\Animation-Model-Training');O=R/'reviews/codex-supervision/2026-10-07-core-evidence-digest'
def dense(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def jl(n):return [json.loads(l) for l in (O/n).read_text(encoding='utf-8-sig').splitlines()]
def load(n):return json.loads((O/n).read_text(encoding='utf-8-sig'))
T={x['task_sha256']:x for x in jl('historical-task-corpus.jsonl')};V={x['record_version_sha256']:x for x in jl('record-variants.jsonl')};A=jl('source-record-map.jsonl');S={x['source_raw_sha256']:x for x in jl('source-files.jsonl')}
error=[]
for h,t in T.items():
 if sha(dense({k:t[k] for k in ['problem','solution','answer']}))!=h:error.append(['task_hash',h])
for h,v in V.items():
 rec={k:T[v['task_sha256']][k] for k in ['problem','solution','answer']};rec.update(v['additional_fields'])
 if sha(dense(rec))!=h:error.append(['reconstructed_record',h])
with zipfile.ZipFile(O/'mathematical-source-bytes.zip') as z:
 archive={n[:-4]:z.read(n) for n in z.namelist()}
 for h,b in archive.items():
  if sha(b)!=h:error.append(['archive_member',h])
 parsed={};parsedlines={}
 def node(h,line,pointer):
  if line is None:
   if h not in parsed:parsed[h]=json.loads(archive[h].decode('utf-8-sig'))
   q=parsed[h]
  else:
   if h not in parsedlines:parsedlines[h]=archive[h].splitlines(keepends=True)
   raw=parsedlines[h][line-1];q=json.loads(raw.decode('utf-8-sig'))
  if pointer:
   for token in pointer.split('/')[1:]:
    token=token.replace('~1','/').replace('~0','~')
    q=q[int(token)] if isinstance(q,list) else q[token]
  return q
 for a in A:
  rec=node(a['source_raw_sha256'],a.get('line_number'),a['json_pointer'])
  if sha(dense(rec))!=a['record_version_sha256']:error.append(['source_record',a])
  if a.get('line_number') is not None:
   raw=parsedlines[a['source_raw_sha256']][a['line_number']-1]
   if sha(raw)!=a['raw_line_with_terminator_sha256']:error.append(['source_line',a])
# Old protocol bindings are checked through the new origin map, preserving every alias.
keys={(a['source_raw_sha256'],a.get('line_number'),a['record_version_sha256']) for a in A}
B=jl('bound-row-coverage.jsonl')
for b in B:
 if (b['source_raw_sha256'],b['source_line'],b['record_version_sha256']) not in keys:error.append(['binding_not_in_aliases',b])
refs=jl('priority-task-references.jsonl')
assert len(refs)==761
groups=collections.Counter(a['group'] for a in refs)
assert groups=={'train':47,'eval':300,'test':150,'selected_draft':264}
assert len(jl('gap-36-priority-evidence.jsonl'))==36
assert len(set(a['historical_declared_sha256'] for a in jl('gap-36-priority-evidence.jsonl')))==36
assert all(x['status']=='FULL_TASK_VERSION_MATCHED' for x in jl('workflow-296-evidence.jsonl'))
assert all(x['status']=='FULL_TASKS_MATCHED' for x in jl('b5-50-evidence.jsonl'))
# Known pool / frozen policy bytes unchanged. Other historical raw bytes were read only.
checks=[]
protected={
 'holdout-sources/extracted/kaoyan-triples.jsonl':'39d0f1a1f16ef5ffc026ae58da887cc44ce8a8b4225bcd4f4da751e41c8e663d',
 'reviews/codex-supervision/2026-10-07-holdout-v2-review/holdout-design-v3.pending.md':'33d999ff963f37dfd6931e44205e8e702a682dfdc222c6e28abc4d6d9db5c4dd',
 'reviews/codex-supervision/2026-10-07-equivalent-evidence-policy/EQUIVALENT_EVIDENCE_POLICY.md':'aca80959d797a03c42ac7c8515ea8ce9f1801cc24824fff53d9e27422e0ab0a1',
 'reviews/codex-supervision/2026-10-07-gap-accounting-followup/EXPECTED_VERSION_GAPS.current.json':'61f65b3fab23145d65c6b911b51ed50d38ab13b2ea88330535fa84ce3d353ee2'}
for p,h in protected.items():
 actual=sha((R/p).read_bytes());checks.append({'path':p,'expected_raw_sha256':h,'actual_raw_sha256':actual,'matches':actual==h})
 if actual!=h:error.append(['protected_source_changed',p])
scans=jl('structured-scan-report.jsonl')
scanerrors=[x for x in scans if x.get('parse_errors') or x['status']!='SCANNED']
out={'schema':'lossless-digest-validation-v1','time':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'result':'PASS' if not error else 'FAIL','task_hash_checks':len(T),'full_record_reconstructions_checked':len(V),'source_record_locations_checked':len(A),'archive_raw_sha_checks':len(archive),'mandatory_previous_bindings_checked':len(B),'priority_groups':dict(groups),'workflow_pairs_bound':296,'b5_pairs_bound':50,'protected_sources':checks,'errors':error,'structured_source_parse_error_versions':len(scanerrors),'parse_errors_remain_scope_limits_not_silently_closed':True,'candidate_qualification_verified':False,'mathematical_correctness_verified':False,'native_experiments':0}
with (O/'validation.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(out,f,ensure_ascii=False,indent=2);f.write('\n')
with (O/'structured-parse-scope-limits.json').open('x',encoding='utf-8',newline='\n') as f:json.dump({'versions':scanerrors,'not_claiming_missing_content_is_non_task':True},f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps(out,ensure_ascii=False))
if error:raise SystemExit(1)
