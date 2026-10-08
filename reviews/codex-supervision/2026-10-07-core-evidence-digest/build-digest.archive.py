
from pathlib import Path
import json, hashlib, collections, subprocess, zipfile, datetime
R=Path(r'D:\Animation-Model-Training')
O=R/'reviews/codex-supervision/2026-10-07-core-evidence-digest'
O.mkdir(exist_ok=False)
P=R/'reviews/codex-supervision/2026-10-07-holdout-exposure-core-protocol'
def sha(b):return hashlib.sha256(b).hexdigest()
def dense(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
def objsha(x):return sha(dense(x))
def load(n):return json.loads((R/n).read_text(encoding='utf-8-sig'))
def lines(p):return [json.loads(l) for l in p.read_text(encoding='utf-8-sig').splitlines() if l.strip()]
def write(n,x):
 with (O/n).open('x',encoding='utf-8',newline='\n') as f:json.dump(x,f,ensure_ascii=False,indent=2);f.write('\n')
def writejl(n,rows):
 with (O/n).open('x',encoding='utf-8',newline='\n') as f:
  for x in rows:f.write(dense(x).decode()+'\n')
now=datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
source_refs={}
def bind(p,expected=None):
 f=R/p;b=f.read_bytes();h=sha(b)
 if expected and h!=expected:raise ValueError(('SOURCE_DRIFT',p,expected,h))
 source_refs[p]={'path':p,'raw_sha256':h,'bytes':len(b)}
 return b
inputs=['filesystem-inventory.jsonl','extra-filesystem-inventory.jsonl','git-history-inventory.jsonl','git-all-material-supplement.jsonl','git-path-versions.jsonl','historical-triple-row-bindings.jsonl','active-497-row-bindings.jsonl','selected-264-row-bindings.jsonl','workflow-296-row-bindings.json','b5-50-row-bindings.json']
for n in inputs:bind((P/n).relative_to(R).as_posix())
fs=lines(P/'filesystem-inventory.jsonl')+lines(P/'extra-filesystem-inventory.jsonl')
git=lines(P/'git-history-inventory.jsonl')+lines(P/'git-all-material-supplement.jsonl')
sources={};warnings=[];excluded=[];scan_reports=[];records={};tasks={};origins=[];origin_keys=set();partial=[]
def source_row(h,n):
 return sources.setdefault(h,{'source_raw_sha256':h,'bytes':n,'available_physical_paths':set(),'logical_git_paths':set(),'git_object_ids':set(),'structured_modes':set(),'indexed_filesystem_aliases':[],'git_inventory_rows':[],'content_collected':False})
for x in fs:
 name=x['path'];suf=Path(name).suffix.lower()
 if suf not in ('.json','.jsonl'):continue
 if name.startswith('holdout-sources/') or any(t in name for t in ['.venv/','node_modules/']):
  excluded.append({'path':name,'raw_sha256':x['sha256'],'reason':'CANDIDATE_SOURCE_OR_DEPENDENCY_EXCLUDED'});continue
 q=source_row(x['sha256'],x['bytes']);q['available_physical_paths'].add(x.get('actual_bound_path',name));q['structured_modes'].add(suf)
 q['indexed_filesystem_aliases'].append({'path':name,'raw_sha256':x['sha256']})
for ix,x in enumerate(git):
 paths=x['logical_paths'];modes={Path(n).suffix.lower() for n in paths}
 if not modes.intersection({'.json','.jsonl'}):continue
 if all(n.startswith('holdout-sources/') for n in paths):continue
 q=source_row(x['sha256'],x['bytes']);q['available_physical_paths'].add(x['actual_bound_path']);q['logical_git_paths'].update(paths);q['git_object_ids'].add(x['git_object_id']);q['structured_modes'].update(modes.intersection({'.json','.jsonl'}))
 q['git_inventory_rows'].append({'inventory':inputs[2 if ix<len(lines(P/'git-history-inventory.jsonl')) else 3],'git_object_id':x['git_object_id']})
extra=['reviews/codex-supervision/2026-10-07-gap-accounting-followup/reconstructed-bytes/109d993d8dfd8ed347911a996074ae2b75b38fcf300417e9a06bb8a557cf5ddb.bin','reviews/codex-supervision/2026-10-07-gap-accounting-followup/reconstructed-bytes/2fa2a95de269877eeb24a3128f120ae8a0e2530ca9ff630de49054302c0d8c3c.bin']
for name in extra:
 b=bind(name);q=source_row(sha(b),len(b));q['available_physical_paths'].add(name);q['structured_modes'].add('.jsonl')
def add_record(rec,h,pointer,line=None,raw_line=None):
 math={k:rec[k] for k in ['problem','solution','answer']};th=objsha(math);rh=objsha(rec)
 t=tasks.setdefault(th,{'task_sha256':th,**math,'record_version_sha256s':set(),'source_raw_sha256s':set(),'ids':set(),'groups':set()})
 t['record_version_sha256s'].add(rh);t['source_raw_sha256s'].add(h)
 if rec.get('id') is not None:t['ids'].add(str(rec['id']))
 records.setdefault(rh,{'record_version_sha256':rh,'task_sha256':th,'additional_fields':{k:v for k,v in rec.items() if k not in math}})
 key=(h,pointer,line,rh)
 if key not in origin_keys:
  origin_keys.add(key);z={'source_raw_sha256':h,'json_pointer':pointer,'record_version_sha256':rh,'task_sha256':th,'id':rec.get('id')}
  if line is not None:z['line_number']=line;z['raw_line_with_terminator_sha256']=sha(raw_line)
  origins.append(z)
def walk(v,h,pointer='',line=None,raw_line=None):
 if isinstance(v,dict):
  if all(k in v for k in ['problem','solution','answer']):add_record(v,h,pointer,line,raw_line)
  elif ('problem' in v or 'solution' in v) and not any(k.endswith('sha256') for k in ['problem','solution'] if k in v) and ('problem' in v and 'solution' in v):
   partial.append({'source_raw_sha256':h,'json_pointer':pointer,'line_number':line,'present_fields':[k for k in ['problem','solution','answer'] if k in v],'node_sha256':objsha(v),'status':'INCOMPLETE_TRIPLE_REQUIRES_SOURCE_CONTEXT'})
  for k,u in v.items():
   if isinstance(u,(dict,list)):walk(u,h,pointer+'/'+str(k).replace('~','~0').replace('/','~1'),line,raw_line)
 elif isinstance(v,list):
  for i,u in enumerate(v):
   if isinstance(u,(dict,list)):walk(u,h,pointer+'/'+str(i),line,raw_line)
source_bytes={}
with zipfile.ZipFile(O/'mathematical-source-bytes.zip','x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for h,q in sorted(sources.items()):
  b=None
  for name in sorted(q['available_physical_paths']):
   f=R/name
   if f.is_file():
    raw=f.read_bytes()
    if sha(raw)==h:b=raw;q['verified_physical_path']=name;break
  if b is None and q['git_object_ids']:
   oid=sorted(q['git_object_ids'])[0]
   cp=subprocess.run(['git','cat-file','blob',oid],cwd=R,capture_output=True)
   if cp.returncode==0 and sha(cp.stdout)==h:b=cp.stdout;q['resolved_from_git_object']=oid
  if b is None:
   warnings.append({'source_raw_sha256':h,'reason':'BOUND_BYTES_NOT_CURRENTLY_AVAILABLE','paths':sorted(q['available_physical_paths'])});continue
  q['content_collected']=True
  before=len(origins);err=[]
  try:text=b.decode('utf-8-sig')
  except UnicodeDecodeError as e:scan_reports.append({'source_raw_sha256':h,'status':'DECODE_FAILED','reason':str(e)});continue
  if '.json' in q['structured_modes']:
   try:walk(json.loads(text),h)
   except (json.JSONDecodeError,RecursionError) as e:err.append({'mode':'json','reason':type(e).__name__})
  if '.jsonl' in q['structured_modes'] and (len(origins)==before or '.json' not in q['structured_modes']):
   for i,raw in enumerate(b.splitlines(keepends=True),1):
    if not raw.strip():continue
    try:walk(json.loads(raw.decode('utf-8-sig')),h,'',i,raw)
    except (json.JSONDecodeError,UnicodeDecodeError,RecursionError) as e:err.append({'mode':'jsonl','line':i,'reason':type(e).__name__})
  count=len(origins)-before
  q['full_record_occurrences']=count
  scan_reports.append({'source_raw_sha256':h,'status':'SCANNED','full_record_occurrences':count,'parse_errors':err})
  if count:
   z.writestr(h+'.bin',b);source_bytes[h]=b;q['archived_member']=h+'.bin'
# Mandatory row-binding verification, kept independently of extraction aliases.
bind_checks=[];priority_refs=[]
for name,group in [('historical-triple-row-bindings.jsonl','INDEXED_HISTORY'),('active-497-row-bindings.jsonl','ACTIVE'),('selected-264-row-bindings.jsonl','SELECTED_DRAFT')]:
 for idx,b in enumerate(lines(P/name),1):
  raw=source_bytes.get(b['source_raw_sha256'])
  if raw is None:raise ValueError(('MISSING_BOUND_MATH_SOURCE',b))
  line=raw.splitlines(keepends=True)[b['line_number']-1]
  rec=json.loads(line.decode('utf-8-sig'))
  if sha(line)!=b['raw_line_with_terminator_sha256']:raise ValueError(('BOUND_LINE_SHA_MISMATCH',b))
  if sha(json.dumps(rec,ensure_ascii=False,sort_keys=True).encode())!=b['record_canonical_sha256']:raise ValueError(('BOUND_RECORD_SHA_MISMATCH',b))
  rh=objsha(rec);th=objsha({k:rec[k] for k in ['problem','solution','answer']})
  add_record(rec,b['source_raw_sha256'],'',b['line_number'],line)
  subgroup=b.get('role',group)
  if group in ['ACTIVE','SELECTED_DRAFT']:tasks[th]['groups'].add(subgroup)
  row={'input_binding':name,'input_binding_line':idx,'source_path':b['source_path'],'source_raw_sha256':b['source_raw_sha256'],'source_line':b['line_number'],'record_version_sha256':rh,'task_sha256':th,'id':rec.get('id'),'group':subgroup,'identity_verified':True}
  bind_checks.append(row)
  if group in ['ACTIVE','SELECTED_DRAFT']:priority_refs.append(row)
def freeze_source(x):
 y=dict(x)
 for k in ['available_physical_paths','logical_git_paths','git_object_ids','structured_modes']:y[k]=sorted(y[k])
 return y
frozen_sources=[freeze_source(x) for x in sources.values()]
# Exact triples are reuse units, never SAME_CORE labels; supplementary fields are lossless.
ordered=sorted(tasks,key=lambda h:(0 if 'train' in tasks[h]['groups'] else 1 if 'selected_draft' in tasks[h]['groups'] else 2 if tasks[h]['groups'] else 3,h))
def taskrow(h):
 t=tasks[h];return {k:sorted(v) if isinstance(v,set) else v for k,v in t.items()}
writejl('historical-task-corpus.jsonl',[taskrow(h) for h in ordered])
writejl('record-variants.jsonl',[records[h] for h in sorted(records)])
writejl('source-record-map.jsonl',origins)
writejl('source-files.jsonl',sorted(frozen_sources,key=lambda x:x['source_raw_sha256']))
writejl('bound-row-coverage.jsonl',bind_checks)
writejl('priority-task-references.jsonl',priority_refs)
writejl('partial-task-locators.jsonl',partial)
writejl('structured-scan-report.jsonl',scan_reports)
# Retained 20 known 10-04 inputs get complete mathematical content.
name='outputs/data-probe/run-20261004-004728/sample_manifest.json';m=load(name);bind(name)
test=[x for x in priority_refs if x['group']=='test']
known20=[]
for item in m['items']:
 choices=[]
 for a in test:
  if a['id']!=item['id']:continue
  t=tasks[a['task_sha256']]
  ih=sha(json.dumps({k:t[k] for k in ['problem','solution']},ensure_ascii=False,sort_keys=True).encode())
  if ih==item['input_sha256']:choices.append(a)
 if len(choices)!=1:raise ValueError(('INPUT20_BINDING',item,choices))
 a=choices[0];known20.append({**item,**a,**{k:tasks[a['task_sha256']][k] for k in ['problem','solution','answer']},'input_hash_omits_answer':True,'does_not_bind_deleted_10_03_run':True})
writejl('retained-20-complete-tasks.jsonl',known20)
# Existing 47/46 catalog is historical context; unchanged claims, no fresh judgment.
name='reviews/2026-10-06-core-families/core-families.corrected-v2.json';c=load(name);bind(name)
train={a['id']:a for a in priority_refs if a['group']=='train'}
core=[]
for x in c['record_core_reviews']:
 a=train[x['id']];rec={**tasks[a['task_sha256']],**records[a['record_version_sha256']]['additional_fields']}
 # compare dense full record, ignoring our index-only fields
 body={k:rec[k] for k in list(tasks[a['task_sha256']]) if k in ['problem','solution','answer']}
 body.update(records[a['record_version_sha256']]['additional_fields'])
 if objsha(body)!=x['record_canonical_sha256']:raise ValueError(('CORE_BIND',x['id']))
 core.append({'id':x['id'],'task_sha256':a['task_sha256'],'record_version_sha256':a['record_version_sha256'],'historical_core_family_id':x['core_family_id'],'historical_core_profile':x['core_profile'],'historical_catalog_source':source_refs[name],'new_core_judgment':False,'independent_math_acceptance':None})
writejl('train-47-core-content-map.jsonl',core)
# Workflow and B5 proof bodies bound; resolve full task versions when identity claims match.
for name in ['reviews/2026-10-06-linalg048-admission/v3-receipt-bound/semantic-review-workflow-v1.json','data/b5-annotation-set/b5-annotation-set.json']:
 bind(name)
wf=load('reviews/2026-10-06-linalg048-admission/v3-receipt-bound/semantic-review-workflow-v1.json')
idtasks=collections.defaultdict(set)
for h,t in tasks.items():
 for ident in t['ids']:idtasks[ident].add(h)
wp=[]
for i,x in enumerate(wf['pairs']):
 matches=[h for h in idtasks[x['id']] if sha(dense(tasks[h]['problem']))==x['problem_sha256']]
 # old field algorithm might hash str bytes rather than JSON string; retain both only with named alg
 if not matches:matches=[h for h in idtasks[x['id']] if isinstance(tasks[h]['problem'],str) and sha(tasks[h]['problem'].encode())==x['problem_sha256']]
 wp.append({'source_pair_index':i,'id':x['id'],'split':x['split'],'problem_sha256_claim':x['problem_sha256'],'complete_task_sha256_candidates':sorted(matches),'historical_verdict':x.get('verdict'),'historical_reason':x.get('reason'),'historical_evidence':x.get('evidence'),'status':'FULL_TASK_VERSION_MATCHED' if matches else 'TASK_VERSION_PENDING','new_independent_judgment':False})
writejl('workflow-296-evidence.jsonl',wp)
b5=load('data/b5-annotation-set/b5-annotation-set.json')
bp=[]
for i,x in enumerate(b5['pairs']):
 refs={}
 for side in ['a','b']:
  refs[side]=sorted(h for h in idtasks[x[side]] if tasks[h]['problem']==x['text_'+side])
 bp.append({'source_pair_index':i,'original_pair':x,'full_task_version_candidates':refs,'status':'FULL_TASKS_MATCHED' if all(refs.values()) else 'TASK_VERSION_PENDING','historical_label_not_new_acceptance':True})
writejl('b5-50-evidence.jsonl',bp)
# Same ID exact content variants and all origin links; do not infer semantic equivalence.
deltas=[{'id':i,'task_sha256_versions':sorted(hs),'known_version_count':len(hs),'relation':'EXACT_MATH_FIELDS_DIFFER','core_relation':'UNREVIEWED','does_not_prove_complete_old_version_chain':True} for i,hs in sorted(idtasks.items()) if len(hs)>1]
writejl('historical-math-deltas.jsonl',deltas)
write('scope-and-counts.json',{
 'schema':'core-evidence-digest-v1','time':now,
 'raw_candidate_pool_untouched':True,'qualification':'UNKNOWN','calibration':'UNCALIBRATED','production':'CLOSED',
 'exact_math_triples':len(tasks),'full_record_versions':len(records),'unique_source_record_occurrences':len(origins),
 'structured_file_versions_considered':len(sources),'structured_file_versions_scanned':sum(x['content_collected'] for x in sources.values()),
 'mathematical_source_byte_members':len(source_bytes),'bound_history_rows_verified':sum(x['input_binding']=='historical-triple-row-bindings.jsonl' for x in bind_checks),
 'active_rows_verified':len([x for x in priority_refs if x['group']!='selected_draft']),'selected_draft_rows_verified':len([x for x in priority_refs if x['group']=='selected_draft']),
 'workflow_pairs':len(wp),'workflow_pairs_full_task_matched':sum(x['status']=='FULL_TASK_VERSION_MATCHED' for x in wp),
 'b5_pairs':len(bp),'b5_pairs_full_tasks_matched':sum(x['status']=='FULL_TASKS_MATCHED' for x in bp),
 'retained20':len(known20),'historical_ids_with_math_field_deltas':len(deltas),
 'partial_record_locators':len(partial),'scan_warning_count':len(warnings),
 'warnings':warnings,'excluded_candidate_or_dependency_files':len(excluded),
 'limits':['Indexed available structured bytes plus captured reachable Git materials only. Missing old versions, prose/string-embedded mathematics, PDF/HTML-only task content and later unindexed materials are not certified covered.','Exact triple dedup does not merge supplementary contexts; original full record reconstructs by merging triple with record-variants additional_fields. Complete parent context remains in SHA-bound ZIP members.','All 36 historical byte gaps and their mathematical scope closure remain PENDING; no missing version gets silently replaced by its successor.','No new SAME_CORE/DIFFERENT_CORE judgments, candidate qualification labels, role signatures or model/native experiments.']
})
write('input-bindings.json',{'schema':'digest-input-bindings-v1','inputs':list(source_refs.values())})
write('excluded-source-scope.json',{'rows':excluded,'partial_math_requires_review':True,'other_formats_in_original_inventory_not_certified_excluded_from_decision':True})
print(json.dumps(load((O/'scope-and-counts.json').relative_to(R).as_posix()),ensure_ascii=False))
