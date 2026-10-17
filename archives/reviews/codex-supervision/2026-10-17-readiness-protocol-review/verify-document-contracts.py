from pathlib import Path
from datetime import datetime
import ast,json,hashlib,re
r=Path(r'D:\Animation-Model-Training');a=r/'archives/reviews/codex-supervision/2026-10-17-readiness-protocol-review'
assert not (a/'delivery-manifest.json').exists(), 'Frozen archive: refuse to overwrite verification output'
before=json.loads((a/'source-bindings.before.json').read_text());checks={}
def check(name,value):
 checks[name]=bool(value)
 assert checks[name],name
def source(n): return (r/n).read_text(encoding='utf-8')
def literal_assignment(n,key):
 tree=ast.parse(source(n))
 for node in tree.body:
  if isinstance(node,ast.Assign) and any(isinstance(x,ast.Name) and x.id==key for x in node.targets):return ast.literal_eval(node.value)
 raise ValueError(key)
docs=['docs/DATA-CANDIDATES-HF.md','docs/TRAINING-LOOP-DESIGN.md','docs/READINESS-EVIDENCE-PROTOCOL.md']
after={n:hashlib.sha256((r/n).read_bytes()).hexdigest() for n in docs}
check('two_original_documents_changed',all(after[n]!=before[n] for n in docs[:2]))
check('all_eighteen_other_bound_inputs_unchanged',all(hashlib.sha256((r/n).read_bytes()).hexdigest()==h for n,h in before.items() if n not in docs[:2]))
for name,copyname in [(docs[0],'DATA-CANDIDATES-HF.md.after'),(docs[1],'TRAINING-LOOP-DESIGN.md.after'),(docs[2],'READINESS-EVIDENCE-PROTOCOL.md')]:
 check('snapshot_identical_'+Path(name).stem,(r/name).read_bytes()==(a/copyname).read_bytes())
required=literal_assignment('src/animtrain/preflight.py','READY_REQUIRED_CHECKS')
check('eight_ready_names_actual',len(required)==8 and set(required)=={'gpu','model_dir','data_manifest','run_snapshot','asset_evidence','freeze_gate','near_dup_calibrated','exec_isolation'})
protocol=source(docs[2]); data=source(docs[0]); design=source(docs[1])
check('all_eight_ready_rows_covered',all(any(line.startswith('| '+k+' |') for line in protocol.splitlines()) for k in required))
check('native_required_cases_count_actual',len(literal_assignment('src/animtrain/sandbox_execution.py','REQUIRED_CASES'))==16)
check('certificate_keys_source_bound',all(x in (source('src/animtrain/sandbox_execution.py')+source('src/animtrain/full_surface_evidence.py')) and x in protocol for x in ['production-appcontainer-v2','private_per_run','implementation_sha256','raw_path','raw_sha256','surface_raw_path','surface_raw_sha256']))
v=ast.parse(source('src/animtrain/validate.py'))
assigns=[n for n in ast.walk(v) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='near_dup_calibrated' for t in n.targets)]
check('near_dup_not_connected_fact',len(assigns)>0 and all(isinstance(n.value,ast.Constant) and n.value.value is False for n in assigns))
e=ast.parse(source('tools/eval_step.py'))
for f in [n for n in e.body if isinstance(n,ast.FunctionDef) and n.name in ('render_check','judge')]:
 val=ast.literal_eval(f.body[0].value)
 check('evaluator_'+f.name+'_unverified_actual',val['status']=='UNVERIFIED')
run=next(n for n in e.body if isinstance(n,ast.FunctionDef) and n.name=='run')
check('evaluator_final_return_two_actual',isinstance(run.body[-1],ast.Return) and ast.literal_eval(run.body[-1].value)==2)
check('no_percentage_or_approx_targets_in_revised_docs',all(x not in '\n'.join([protocol,data,design]) for x in ['100%','95%','\u2248','~300']))
check('precise_target_contract_present',all(x in design for x in ['R=1','E\u226519/20','UNVERIFIED']))
check('external_instance_count_exact',5062*3==15186 and '15186' in data)
check('external_reference_answer_separation_documented','\u4e0d\u628a\u53c2\u8003\u7b54\u6848\u653e\u5165\u6a21\u578b\u63d0\u793a' in data and 'EXTERNAL_QA_ONLY' in data)
check('finite_policy_and_native_gap_separate',all(x in protocol for x in ['\u4e0d\u8981\u6c42\u4e8b\u524d\u8bc1\u660e\u5168\u5c40\u8bed\u4e49\u9694\u79bb','D2/D8','NOT_ESTABLISHED','require_complete_surface']))
check('no_claim_protocol_already_connected','DESIGN_CONTRACT_NOT_CONNECTED' in protocol and '\u5c1a\u672a\u63a5\u901a' in design)
check('holdout_stage_thresholds_preserved',all(x in protocol for x in ['MEMBER_ELIGIBILITY_VERIFIED','FINAL_HOLDOUT_VERIFIED','FPR_U\u22641/100','Recall_L\u226519/20']))
check('question_identity_and_unknown_contract',all(x in protocol for x in ['row_index','rate=null','UNVERIFIED','Fraction(p,N)']))
links=[]
for p in [r/n for n in docs]+[a/'SUPERVISION_REPORT.md']:
 for target in re.findall(r'\]\(([^)]+)\)',p.read_text(encoding='utf-8')):
  if target.startswith(('https://','http://','#')):continue
  dest=Path(target) if re.match(r'^[A-Za-z]:/',target) else p.parent/target.split('#')[0]
  links.append({'file':p.relative_to(r).as_posix(),'target':target,'exists':dest.exists()})
check('all_active_document_and_report_local_links_resolve',all(x['exists'] for x in links) and len(links)>0)
for rel,name in [('2026-10-07-holdout-v2-review','holdout-design-v3.pending.md'),('2026-10-17-holdout-custody-mail-review','ROLE_REGISTER.v3.pending.json')]:
 d=r/'archives/reviews/codex-supervision'/rel;m=json.loads((d/'delivery-manifest.json').read_text());item=next(x for x in m['artifacts'] if x['path'] in (name,'reviews/codex-supervision/'+rel+'/'+name));p=d/name
 check('frozen_'+name+'_still_bound',hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'] and p.stat().st_size==item['bytes'])
o=r/'reviews/codex-supervision/2026-10-08-auto-mail';rid='run-a8135009f6b64c198c0f3a01d36dc55b'
check('batch_still_unacknowledged',not(o/'runs'/rid/'ACK.json').exists())
latest=json.loads((r/'reviews/codex-supervision/2026-10-04-live-watch/latest.json').read_text(encoding='utf-8'))
out={'verified_at':datetime.now().astimezone().isoformat(),'checks':checks,'named_checks':len(checks),'local_links':links,'current_document_sha256':after,'tests_run':0,'scope':'STATIC_DOCUMENT_SOURCE_CONTRACT_AND_BINDING_REVIEW_ONLY','observer':{x:latest.get(x) for x in ['time','watcher_pid','head','process_observation','core_drift']}}
(a/'independent-verification.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(a/'source-bindings.after.json').write_text(json.dumps({n:hashlib.sha256((r/n).read_bytes()).hexdigest() for n in list(before)+[docs[2]]},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'named_checks':len(checks),'links':len(links),'checks':checks,'current_document_sha256':after},ensure_ascii=False))
