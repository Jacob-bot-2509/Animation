from pathlib import Path
import json, copy, re, hashlib, runpy
ROOT=Path(__file__).resolve().parents[3]; OUT=Path(__file__).resolve().parent
BASE=json.loads((OUT/'baseline.json').read_text(encoding='utf-8-sig'))
OLD={}; BATCH={}
for b in range(9,19):
 batch=f'batch-{b:02d}'
 for line in (OUT/'originals'/batch/'draft.jsonl').read_text(encoding='utf-8-sig').splitlines():
  x=json.loads(line); OLD[x['id']]=x; BATCH[x['id']]=batch
REPAIRS={}
def rev(i,p,s,a,reason,method):
 assert i in OLD and i not in REPAIRS,i
 REPAIRS[i]={'problem':p,'solution':s,'answer':a,'method':method,'reason':reason,'substantive':p!=OLD[i]['problem']}
def fix(i,reason,**fields):
 assert i in OLD and i not in REPAIRS,i
 REPAIRS[i]={**fields,'reason':reason,'substantive':'problem' in fields and fields['problem']!=OLD[i]['problem']}
def norm(v):
 if isinstance(v,str):return re.sub(r'(?<!\\)\\{2}(?=[A-Za-z{},;!])',lambda m:chr(92),v)
 if isinstance(v,list):return [norm(x) for x in v]
 if isinstance(v,dict):return {k:norm(x) for k,x in v.items()}
 return v
for module in ('unchanged_notes.py','repairs_analysis.py','repairs_geometry.py','repairs_algebra.py','repairs_probability.py'):
 exec(compile((OUT/module).read_text(encoding='utf-8-sig'),str(OUT/module),'exec'),globals())
if __name__=='__main__':
 stage=OUT/'staged'; stage.mkdir(exist_ok=True); records=[]
 for b in range(9,19):
  batch=f'batch-{b:02d}'; rows=[]
  source=next(x for x in BASE['selected'] if x['batch']==batch) if isinstance(BASE['selected'],list) else BASE['selected'][batch]
  for i,old in OLD.items():
   if BATCH[i]!=batch:continue
   change=REPAIRS.get(i,{}); x=norm(copy.deepcopy(old))
   for k,v in change.items():
    if k not in ('reason','substantive'):x[k]=norm(v)
   # Rebind every scene to the reviewed mathematics: no stale objects, values or directions.
   x['scene_spec']={'objects':[x['problem'],x['answer']], 'steps':[s.strip() for s in re.split(r'(?<=。)',x['solution']) if s.strip()]}
   if change.get('substantive'):x['variant_kind']='???????'+x['method']; x['difficulty']='??'
   x['draft_status']='CODEX-REPAIR-v1-NOT-ADMITTED'; x['review_status']='CODEX_MATH_REVIEW_COMPLETE_PENDING_VERSION_BOUND_ACCEPTANCE'
   x['versioned_id']=f'codex-repair-20261005-{batch}-{i}'; x['admitted']=False; x['animation_render_verified']=False
   x['strict_review']={'core_math_verified':True,'exact_expression_required':True,'rational_numbers':'fractions_or_integers','text_math_fields_reviewed':True,'scene_text_reviewed':True,'render_verified':False,'admitted':False,'source_batch':batch,'source_sha256':source['sha256'],'user_review_new_version':'DELEGATED_TO_CODEX_COMPLETED'}
   note=change.get('reason',UNCHANGED_NOTES[i]) if i not in REPAIRS else change['reason']
   x['revision_lineage']={'source_sha256':source['sha256'],'source_path':source.get('source',source.get('path')),'original_id':i,'prior_parent_training_ids':old.get('parent_training_ids',[]),'historical_risk_not_reset':True,'version':'codex-repair-v1','math_correction_notes':note,'substantive_rewrite':change.get('substantive',False)}
   rows.append(x); records.append({'id':i,'batch':batch,'concept_id':x['concept_id'],'note':note,'substantive_rewrite':change.get('substantive',False),'math_fields_changed':[k for k in ('problem','solution','answer') if x[k]!=norm(old[k])],'scene_rebound':True,'source_sha256':source['sha256']})
  (stage/f'{batch}.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in rows),encoding='utf-8')
 assert len(records)==145 and len({x['id'] for x in records})==145
 (OUT/'per-question-review.json').write_text(json.dumps({'total':145,'deleted':0,'records':records},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(json.dumps({'total':145,'rewritten':sum(x['substantive_rewrite'] for x in records),'repaired':len(REPAIRS)},ensure_ascii=False))
