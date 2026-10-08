"""Preserve workflow results and repair concrete scene defects without changing math text."""
from pathlib import Path
import ast,copy,json,re,sys,collections
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
P=R/'reviews/codex-supervision/2026-10-06-scene-start-supervision'
sys.path[:0]=[str(R/'tools'),str(R/'src')];sys.stdout.reconfigure(encoding='utf-8')
from holdout_contract import Snapshot,object_sha,raw_sha
from scene_sweep_protocol import verify_inputs,sorted_sha,MATH_FIELDS
from dataset_audit import Audit,check_latex
# Only compile the two pure text helpers, not the materialization entry point.
tree=ast.parse((O/'materialize_exact_math.py').read_text(encoding='utf-8'))
helpers=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'walk','frac_braces'}]
exec(compile(ast.Module(body=helpers,type_ignores=[]),'pure_fraction_helpers','exec'))
manifest,items=verify_inputs(O/'inputs-v2',root=R)
byid={i['record']['id']:i for i in items};order=[i['record']['id'] for i in items]
snapshot=Snapshot(R);workflow_path=R/'reviews/2026-10-06-scene-standard-sweep/workflow-run-result.json'
workflow_bytes=snapshot.read(workflow_path);workflow=json.loads(workflow_bytes)
assert raw_sha(workflow_bytes)=='92b4adf7c04659e8ae257ebaad687497bcda0187727b39fe2fe17159e5e5f1aa'
assert set(workflow['audit'])==set(byid)
for pid,entry in workflow['audit'].items():
 assert entry['id']==pid and entry['idx']==order.index(pid)
counts=collections.Counter(x['standard_verdict'] for x in workflow['audit'].values())
assert counts['REVISE']==143 and counts['PASS']==121
assert sum(v['geometric_viewable'] for v in workflow['audit'].values())==104
patches={};provenance={};mathfixes=[]
captured=json.loads((O/'claude-scene-candidates.captured-v1.json').read_text(encoding='utf-8'))
for patch in captured['records']:
 patches[patch['id']]=copy.deepcopy(patch);provenance[patch['id']]='preserved_inplace_output'
def make_patch(pid,spec):
 i=byid[pid];row=i['record'];b=i['binding'];after=copy.deepcopy(row);after['scene_spec']=spec
 return {'batch':b['batch'],'id':pid,'expected_selected_path':b['source_path'].split('2026-10-05-training-diversity-drafts/',1)[1],
  'expected_hash_algorithm':b['hash_algorithm'],'expected_selected_sha256':b['source_normalized_sha256'],
  'expected_selected_raw_sha256':b['source_raw_sha256'],'expected_record_sha256':sorted_sha(row),
  'new_math_content_sha256':sorted_sha({k:after[k] for k in MATH_FIELDS}),'fields':{'scene_spec':spec},
  'mathematics_three_fields_unchanged':True,'semantic_review_status':'PENDING_INDEPENDENT_REVIEW','visual_verified':False}
for pid,v in workflow['revisions'].items():
 assert pid in byid and v['idx']==byid[pid]['idx']
 assert v['still_rejected'] is False and not v['verify_issues']
 spec={'objects':copy.deepcopy(v['objects']),'steps':copy.deepcopy(v['steps'])}
 if pid=='draft-c36-01':
  # AA^-1 A = A, not I. Correct the false intermediate equality in the delivered proof.
  def correct(t):
   return t.replace(r'y^{\mathsf{T}}Iy',r'y^{\mathsf{T}}IAy').replace(r'A^{-1}A=I',r'AA^{-1}=I')
  spec=walk(spec,correct)
  mathfixes.append({'id':pid,'defect':'AA^{-1}A was simplified to I, dropping the final A',
    'correction':'AA^{-1}A=IA=A','workflow_verifier_missed':True})
 patches[pid]=make_patch(pid,spec);provenance[pid]='workflow_returned_revision'
sample=json.loads((P/'scene-sample-codex-corrections-v1.pending.json').read_text(encoding='utf-8'))
for patch in sample['records']:
 patches[patch['id']]=copy.deepcopy(patch);provenance[patch['id']]='codex_three_reviewed_corrections'
qa=[];blockers=[]
for pid,patch in patches.items():
 patch['fields']['scene_spec']=walk(patch['fields']['scene_spec'],
       lambda t:frac_braces(t).replace(r'\int_0^1',r'\int_{0}^{1}'))
 row=copy.deepcopy(byid[pid]['record']);row.update(patch['fields'])
 patch['new_math_content_sha256']=sorted_sha({k:row[k] for k in MATH_FIELDS})
 assert all(row[k]==byid[pid]['record'][k] for k in ('problem','solution','answer'))
 a=Audit();check_latex(a,{'path':'new scene candidates'},{'record':row,'locator':pid},pid)
 sceneissues=[x for x in a.issues if x['field']=='scene_spec' and x['severity'] in ('hard','quarantine')]
 decimals=re.findall(r'\d+\.\d+',json.dumps(row['scene_spec'],ensure_ascii=False))
 if sceneissues or decimals:blockers.append({'id':pid,'issues':sceneissues,'decimal_literals':decimals})
 qa.append({'id':pid,'provenance':provenance[pid],'scene_guard_blocker_count':len(sceneissues),
     'decimal_literals':decimals,'mathematics_three_fields_unchanged':True,
     'independent_math_review':pid in {'draft-c36-01','draft-c37-03','draft-c12-05','draft-c51-02'},
     'visual_verified':False})
revised=set(workflow['revisions']);needed={k for k,v in workflow['audit'].items() if v['standard_verdict']=='REVISE'}
snapshot.check_unchanged()
with (O/'workflow-run-result.original.json').open('xb') as f:f.write(workflow_bytes)
def save(name,v):
 with (O/name).open('x',encoding='utf-8') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
save('workflow-evidence-analysis.json',{'source_raw_sha256':raw_sha(workflow_bytes),'audit_id_and_idx_coverage_verified':264,
 'author_reported_counts':workflow['counts'],'source_revision_count':len(revised),
 'merged_candidate_count':len(patches),'source_revision_ids':sorted(revised),'math_defects_fixed':mathfixes,
 'remaining_without_any_scene_candidate':sorted(needed-set(patches)),
 'remaining_without_workflow_returned_revision':sorted(needed-revised),
 'author_validated_is_not_independent_or_visual_acceptance':True,
 'author_reported_failed_agents':105,'known_internal_task_stop_ack':'msg_1791268112077_560'})
save('scene-candidates-merged-v3.pending.json',{'schema':'source-bound-scene-candidate-patches-v3',
 'status':'UNSELECTED_PARTIAL_INDEPENDENT_REVIEW','records':[patches[k] for k in order if k in patches],
 'precedence':'Codex reviewed three > returned workflow revision > preserved inplace scene',
 'source_workflow_raw_sha256':raw_sha(workflow_bytes),'math_defects_fixed':mathfixes})
save('scene-candidate-latex-qa.json',{'records':qa,'blockers':blockers,'independent_full_math_review':False})
print(json.dumps({'workflow_revisions':len(revised),'merged_candidates':len(patches),'blockers':blockers,
 'remaining_without_candidate':len(needed-set(patches))},ensure_ascii=False))
