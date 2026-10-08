import copy,hashlib,json,re,sys
from collections import Counter
from pathlib import Path
ROOT=Path(r'D:\Animation-Model-Training');OUT=Path(__file__).resolve().parent;SWEEP=ROOT/'reviews/2026-10-06-scene-standard-sweep';OLD=ROOT/'reviews/codex-supervision/2026-10-06-scene-repair-takeover'
sys.path.insert(0,str(ROOT/'tools'))
from scene_sweep_protocol import verify_inputs,sorted_sha,MATH_FIELDS
from draft_io import fingerprint,selected_path
from dataset_audit import Audit,check_latex,walk_strings
from holdout_contract import object_sha
sha=lambda b:hashlib.sha256(b).hexdigest()
def save(name,v): (OUT/name).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
inputs,rows=verify_inputs(OLD/'inputs-v2');byid={r['record']['id']:r for r in rows}
prev=json.loads((OLD/'scene-candidates-corrected-v4.json').read_text('utf-8'));prev={r['id']:r for r in prev['records']}
remaining=json.loads((OLD/'workflow-evidence-analysis.json').read_text('utf-8'))['remaining_without_any_scene_candidate']
allpatch=[];batches=[];bindings={};control=[];latex=[];errors=[]
def bind(p):
 b=p.read_bytes();bindings[p.relative_to(ROOT).as_posix()]={'raw_sha256':sha(b),'bytes':len(b)};return b
for n in range(1,11):
 p=SWEEP/f'batch{n}-patches.json';raw=bind(p);(OUT/f'batch{n}-patches.original.json').write_bytes(raw);patches=json.loads(raw)['records'];staged=SWEEP/f'batch{n}-staged-v1'
 selpath=staged/'draft-selection.candidate.json';receiptpath=staged/'stage-receipt.json';sel=json.loads(bind(selpath));receipt=json.loads(bind(receiptpath));(OUT/f'batch{n}-receipt.original.json').write_bytes(receiptpath.read_bytes())
 assert receipt['patches_raw_sha256']==sha(raw) and receipt['patch_count']==len(patches)
 assert receipt['record_count']==264 and receipt['production_selector_updated'] is False and receipt['training_admitted'] is False and receipt['visual_verified'] is False
 assert sel['status']=='UNSELECTED_NOT_ADMITTED' and sel['original_selection_raw_sha256']==inputs['selection_raw_sha256']
 for rel,meta in receipt['source_bindings'].items():
  b=bind(ROOT/rel);assert sha(b)==meta['raw_sha256'] and len(b)==meta['bytes'],rel
 pm={x['id']:x for x in patches};assert len(pm)==len(patches)
 md=[f'# Batch {n} independent review material\n'];rr=[]
 for patch in patches:
  pid=patch['id'];item=byid[pid];record=item['record'];binding=item['binding'];assert patch['batch']==binding['batch'] and set(patch['fields'])=={'scene_spec'}
  assert patch['expected_record_sha256']==sorted_sha(record)
  assert patch['expected_selected_raw_sha256']==binding['source_raw_sha256'] and patch['expected_selected_sha256']==binding['source_normalized_sha256']
  assert selected_path(ROOT/'reviews/2026-10-05-training-diversity-drafts',{'batch':patch['batch'],'path':patch['expected_selected_path']})==ROOT/binding['source_path']
  after={**record,**patch['fields']};assert patch['new_math_content_sha256']==sorted_sha({k:after[k] for k in MATH_FIELDS})
  scene=patch['fields']['scene_spec'];audit=Audit();check_latex(audit,{'path':str(p)},{'record':{'scene_spec':scene},'locator':pid},pid);latex+=audit.issues
  for text in walk_strings(scene):
   bad=[f'U+{ord(c):04X}' for c in text if ord(c)<32 or 127<=ord(c)<=159 or c=='\ufffd']
   if bad: control.append({'batch':n,'id':pid,'bad':bad,'text':text})
  md += ['## '+pid,'P: '+record['problem'],'S: '+record['solution'],'A: '+record['answer'],'Objects: '+' | '.join(scene['objects']),'Steps:\n'+'\n'.join(scene['steps'])+'\n']
  rr.append(pid);allpatch.append({'batch_number':n,'patch':patch})
 stagedrows=[]
 for e in sel['entries']:
  f=selected_path(staged,e);b=bind(f);fp=fingerprint(b);assert all(e[k]==fp[k] for k in fp)
  records=[json.loads(line) for line in b.decode('utf-8').splitlines() if line.strip()];assert len(records)==e['count'];stagedrows+=records
  for rec in records:
   original=byid[rec['id']]['record'];assert all(rec[k]==original[k] for k in ('problem','solution','answer'))
   assert rec['scene_spec']==pm.get(rec['id'],{'fields':original})['fields']['scene_spec']
   assert all(rec.get(k) is False for k in ('admitted','training_admitted','render_verified','animation_verified'))
 assert len(stagedrows)==264 and len({r['id'] for r in stagedrows})==264
 batches.append({'batch':n,'patch_count':len(patches),'ids':rr,'staged_records':264,'source_and_content_binding_valid':True})
 (OUT/f'review-material-batch{n:02d}.md').write_text('\n\n'.join(md),encoding='utf-8',newline='\n')
ids=[x['patch']['id'] for x in allpatch];counts=Counter(ids);unique=set(ids);oldset=set(prev)
summary={'batches':batches,'patch_count':len(ids),'unique_patch_count':len(unique),'duplicates':{k:v for k,v in counts.items() if v>1},'remaining_90_covered':sorted(set(remaining)&unique),'missing_from_remaining_90':sorted(set(remaining)-unique),'patches_outside_remaining_90':sorted(unique-set(remaining)),'overlap_prior_53':sorted(unique&oldset),'merged_unique_count':len(unique|oldset),'control_corruption':control,'latex_issues':latex,'latex_blockers':[x for x in latex if x['severity'] in ('hard','quarantine')],'scope':'source bindings/full staged coverage and math-three-field equality; not mathematical or visual acceptance','production_approved':False}
save('preflight-results.json',summary);save('source-bindings.before.json',bindings);save('patches-with-batch.json',allpatch)
print(json.dumps({k:v for k,v in summary.items() if k not in ('batches','remaining_90_covered','latex_issues')},ensure_ascii=False,indent=2))