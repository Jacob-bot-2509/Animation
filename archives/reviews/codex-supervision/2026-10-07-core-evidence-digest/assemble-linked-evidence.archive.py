
from pathlib import Path
import json,hashlib,collections,datetime
R=Path(r'D:\Animation-Model-Training');O=R/'reviews/codex-supervision/2026-10-07-core-evidence-digest';BT=chr(96)
def dense(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def jl(n):return [json.loads(s) for s in (O/n).read_text(encoding='utf-8-sig').splitlines()]
def put(n,x,replace=False):
 with (O/n).open('w' if replace else 'x',encoding='utf-8',newline='\n') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
def putjl(n,rows,replace=False):
 with (O/n).open('w' if replace else 'x',encoding='utf-8',newline='\n') as f:
  for x in rows:f.write(dense(x).decode()+'\n')
def md(n,text):
 with (O/n).open('x',encoding='utf-8',newline='\n') as f:f.write(text)
tasks={x['task_sha256']:x for x in jl('historical-task-corpus.jsonl')}
records={x['record_version_sha256']:x for x in jl('record-variants.jsonl')}
origins=jl('source-record-map.jsonl');sources={x['source_raw_sha256']:x for x in jl('source-files.jsonl')}
refs=jl('priority-task-references.jsonl');counts=load((O/'scope-and-counts.json').relative_to(R).as_posix())
idtasks=collections.defaultdict(set);identifier_maps=[]
for rh,x in records.items():
 a=x['additional_fields'];ids={str(a[k]) for k in ['id','problem_id','solution_id'] if a.get(k) is not None}
 for ident in ids:idtasks[ident].add(x['task_sha256'])
 if len(ids)>1:identifier_maps.append({'record_version_sha256':rh,'task_sha256':x['task_sha256'],'original_identifier_fields':{k:a[k] for k in ['id','problem_id','solution_id'] if k in a},'source_of_aliases':'ORIGINAL_RECORD_FIELDS_NO_SUFFIX_INFERENCE'})
putjl('identifier-field-aliases.jsonl',identifier_maps)
w=jl('workflow-296-evidence.jsonl')
for x in w:
 hs=[h for h in idtasks[x['id']] if sha(dense(tasks[h]['problem']))==x['problem_sha256_claim']]
 if not hs:hs=[h for h in idtasks[x['id']] if isinstance(tasks[h]['problem'],str) and sha(tasks[h]['problem'].encode())==x['problem_sha256_claim']]
 x['complete_task_sha256_candidates']=sorted(hs);x['status']='FULL_TASK_VERSION_MATCHED' if hs else 'TASK_VERSION_PENDING';x['identity_alias_source']='ORIGINAL_ID_PROBLEM_ID_SOLUTION_ID_FIELDS'
putjl('workflow-296-evidence.jsonl',w,True)
b=jl('b5-50-evidence.jsonl')
for x in b:
 pair=x['original_pair']
 for side in ['a','b']:
  x['full_task_version_candidates'][side]=sorted(h for h in idtasks[pair[side]] if tasks[h]['problem']==pair['text_'+side])
 x['status']='FULL_TASKS_MATCHED' if all(x['full_task_version_candidates'].values()) else 'TASK_VERSION_PENDING'
 x['identity_alias_source']='ORIGINAL_ID_PROBLEM_ID_SOLUTION_ID_FIELDS'
putjl('b5-50-evidence.jsonl',b,True)
counts['workflow_pairs_full_task_matched']=sum(x['status']=='FULL_TASK_VERSION_MATCHED' for x in w)
counts['b5_pairs_full_tasks_matched']=sum(x['status']=='FULL_TASKS_MATCHED' for x in b)
put('scope-and-counts.json',counts,True)
tarpath='reviews/codex-supervision/2026-10-07-evidence-handoff-requirements/TARGETS.json'
nearpath='reviews/codex-supervision/2026-10-07-equivalent-evidence-policy/NEARBY_MATERIALS.json'
targets=load(tarpath)['rows'];near={x['expected_old_raw_sha256']:x for x in load(nearpath)['rows']};gap=[]
for x in targets:
 combined=' '.join(x['claimed_paths']);group='OLD_BATCH_8' if 'batch-' in combined else 'OLD_SELECTOR_1' if 'draft-selection' in combined else 'SCREENING_27'
 gap.append({**x,'shared_preparation_group':group,'available_bound_materials':near[x['historical_declared_sha256']]['available_nearby_materials'],'known_task_packet':'historical-task-corpus.jsonl','packet_is_proven_upper_bound':False,'old_byte_status':'UNAVAILABLE','decision_scope_status':'PENDING','next_missing_bridge':{
  'SCREENING_27':'Historical run/producer/input-version binding and output/schema content proof. Current 20-input replay or early creation date alone is insufficient.',
  'OLD_BATCH_8':'Complete reversible patch chain with removed fields, or proof that the known full task union covers every missing old version. Existing exact successor content already packed.',
  'OLD_SELECTOR_1':'Old complete membership/version map, or proven full possible-members-and-versions bound. Known recovered draft union is available but its completeness for the missing selector is unproved.'
 }[group]})
putjl('gap-36-priority-evidence.jsonl',gap)
roles=[];sourcebind=[]
for path in ['reviews/2026-10-07-gap-materials/msg105-110-earliest-excerpt.json','reviews/2026-10-07-gap-materials/msg224-225-excerpt.json']:
 raw=(R/path).read_bytes();binding={'path':path,'raw_sha256':sha(raw),'bytes':len(raw)};sourcebind.append(binding)
 for i,m in enumerate(json.loads(raw.decode('utf-8-sig'))):
  roles.append({'source_binding':binding,'source_array_index':i,'original_message':m,'supports':'Named agents participated in the stated historical review/instruction scope; message body records requests/claims.','does_not_support':'Not a complete access ledger, executed run receipt, proof of unseen material, independent B/C signature, or complete mathematical no-leakage proof.','qualification_role_state':'CONTEXTUAL_OR_UNKNOWN_PENDING_ACTUAL_ROLE_AUDIT'})
putjl('role-message-evidence.jsonl',roles)
important=[
 'reviews/codex-supervision/2026-10-07-equivalent-evidence-policy/EQUIVALENT_EVIDENCE_POLICY.md',
 'reviews/codex-supervision/2026-10-07-equivalent-evidence-policy/retained-input-identity-verification.json',
 'reviews/codex-supervision/2026-10-07-equivalent-evidence-policy/origin-anchor-verification.json',
 'reviews/codex-supervision/2026-10-07-equivalent-evidence-policy/INCOMING_MATERIALS_REVIEW.md',
 'reviews/codex-supervision/2026-10-07-gap-accounting-followup/EXPECTED_VERSION_GAPS.current.json',
 'reviews/codex-supervision/2026-10-07-gap-accounting-followup/reconstruction-verification.json',
 tarpath,nearpath,'reviews/2026-10-03-model-screening/screening-cleanup-manifest.json',
 'reviews/2026-10-05-training-diversity-drafts/draft-selection.json',
 'reviews/2026-10-07-gap-materials/screening-input-scope-v1.json',
 'reviews/2026-10-07-gap-materials/batch-selector-scope-v1.json',
 'data/manifest.json','holdout-sources/extracted/kaoyan-triples.jsonl',
 'reviews/codex-supervision/2026-10-07-holdout-v2-review/holdout-design-v3.pending.md']
for path in important:
 f=R/path
 if f.is_file():
  raw=f.read_bytes();sourcebind.append({'path':path,'raw_sha256':sha(raw),'bytes':len(raw)})
put('resume-source-bindings.json',{'schema':'digest-small-resume-bindings-v1','bindings':sourcebind})
first={}
for a in refs:first.setdefault(a['task_sha256'],a)
taskorig=collections.defaultdict(list)
for a in origins:taskorig[a['task_sha256']].append(a)
parts=[
 ('01-train-and-drafts-complete.md',[h for h,t in tasks.items() if any(g in t['groups'] for g in ['train','selected_draft'])],'当前训练 47 题与选中草稿 264 题'),
 ('02-current-eval-test-complete.md',[h for h,t in tasks.items() if any(g in t['groups'] for g in ['eval','test'])],'当前评测 300 题与测试 150 题'),
 ('03-history-only-complete.md',[h for h,t in tasks.items() if not t['groups']],'其他已恢复完整数学版本')]
def as_text(v):return v if isinstance(v,str) else json.dumps(v,ensure_ascii=False,indent=2)
readcounts={}
for name,hs,title in parts:
 hs=sorted(hs,key=lambda h:(0 if 'train' in tasks[h]['groups'] else 1,first.get(h,{}).get('source_path',''),first.get(h,{}).get('source_line',0),h))
 chunks=[f'# {title}\n\n共 {len(hs)} 份题干、过程、答案。原文逐字段保留，历史错误或小数也是原始证据，不代表本轮认可。每项的场景、方法、条件补充字段见 {BT}record-variants.jsonl{BT}；父级上下文及原始字节见 {BT}mathematical-source-bytes.zip{BT}。数学资格审查必须连同这些上下文进行。本轮只装配证据，不新增核心判定或答案验收。\n']
 for i,h in enumerate(hs,1):
  t=tasks[h];a=first.get(h)
  if a:loc=f"{a['source_path']}，第 {a['source_line']} 行；源 SHA256 {BT}{a['source_raw_sha256']}{BT}"
  else:
   z=taskorig[h][0];sf=sources[z['source_raw_sha256']];path=sf.get('verified_physical_path') or ('Git blob '+sf.get('resolved_from_git_object',''))
   loc=f"{path}；源 SHA256 {BT}{z['source_raw_sha256']}{BT}；行 {z.get('line_number','—')}，JSON pointer {BT}{z['json_pointer'] or '/'}{BT}"
  ident=' / '.join(t['ids']) or '原记录无 id'
  chunks.append(f"\n## {i}. {ident}\n\n内容 SHA256：{BT}{h}{BT}。\n\n来源：{loc}。\n\n**题干**\n\n{as_text(t['problem'])}\n\n**过程**\n\n{as_text(t['solution'])}\n\n**答案原文**\n\n{as_text(t['answer'])}\n")
 md(name,''.join(chunks));readcounts[name]=len(hs)
put('reading-order.json',{'full_math_files':readcounts,'all_exact_unique_math_covered':sum(readcounts.values())==len(tasks),'reviewer_must_load_supplementary_context':True})
print(json.dumps({'counts':counts,'reading':readcounts,'gap_groups':dict(collections.Counter(x['shared_preparation_group'] for x in gap)),'roles':len(roles)},ensure_ascii=False))
