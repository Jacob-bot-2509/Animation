from pathlib import Path
import sys,json,hashlib,importlib.util
from fractions import Fraction
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
sys.path.insert(0,str(ROOT/'src'))
from animtrain.structural_leakage import compare,implementation_sha256
spec=importlib.util.spec_from_file_location('ledger',ROOT/'reviews/2026-10-05-training-diversity-drafts/coverage_ledger.py');L=importlib.util.module_from_spec(spec);spec.loader.exec_module(L)
rows=[r for p in sorted((OUT/'staged').glob('*.jsonl')) for r in L.load_rows(p)]
held=[];active=[];manifest=json.loads((ROOT/'data/manifest.json').read_text(encoding='utf-8'))
for e in manifest['entries']:
 p=ROOT/'data'/e['path'];items=L.load_rows(p)
 for r in items:(active if e['split']=='train' else held).append({**r,'source':str(p.relative_to(ROOT))})
first8=[r for b in range(1,9) for r in L.load_rows(ROOT/f'reviews/2026-10-05-training-diversity-drafts/batch-{b:02d}/draft-codex-repair-v1.jsonl')]
assert len(held)==450 and len(active)==47 and len(first8)==119
pairs=[];draft_pairs=[];top=[]
for r in rows:
 scores={}
 for q in held:
  pred=compare(r['problem'],q['problem']);score=L.j5(r['problem'],q['problem'])
  if pred['candidate'] or score>=Fraction(2,5):pairs.append({'train_id':r['id'],'query_id':q['id'],'query_problem':q['problem'],'query_solution':q['solution'],'query_method':q.get('method'),'score':str(score),'prediction':pred,'query_source':q['source']})
  key=q.get('problem_id',q['id']);prev=scores.get(key)
  if prev is None or score>prev[0]:scores[key]=(score,q)
 top.append({'id':r['id'],'top':[{'score':str(v[0]),'id':v[1]['id'],'problem':v[1]['problem'],'method':v[1].get('method')} for v in sorted(scores.values(),key=lambda v:v[0],reverse=True)[:3]]})
for j,r in enumerate(rows):
 for q in rows[j+1:]+first8+active:
  score=L.j5(r['problem'],q['problem']);pred=compare(r['problem'],q['problem'])
  if score>=Fraction(2,5) or 'numeric-normalized-object-and-task' in pred['reasons']:
   draft_pairs.append({'left':r['id'],'right':q['id'],'left_problem':r['problem'],'right_problem':q['problem'],'score':str(score),'prediction':pred})
result={'total':145,'heldout_method_records':450,'heldout_comparisons':65250,'first8_rows':119,'active_train':47,'within_and_prior_comparisons':sum(144-j+119+47 for j in range(145)),'calibrated':False,'UNKNOWN_is_not_no_leakage':True,'detector_sha256':implementation_sha256(),'candidate_pairs':pairs,'draft_and_active_candidates':draft_pairs,'top_text_candidates':top,'record_bindings':[{ 'id':r['id'],'sha256':hashlib.sha256(json.dumps(r,ensure_ascii=False,sort_keys=True).encode()).hexdigest()} for r in rows]}
(OUT/'structural-screen.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'heldout_candidates':len(pairs),'heldout_unique':len(set((p['train_id'],p['query_problem']) for p in pairs)),'draft_candidates':len(draft_pairs),'comparison_count':65250},ensure_ascii=False))
