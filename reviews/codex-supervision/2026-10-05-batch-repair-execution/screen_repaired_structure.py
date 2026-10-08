from pathlib import Path
import sys,json,hashlib,importlib.util
from fractions import Fraction
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(OUT))
from animtrain.structural_leakage import compare,implementation_sha256
import build_repaired_batches as B
spec=importlib.util.spec_from_file_location('L',OUT/'coverage_ledger.repaired.py');L=importlib.util.module_from_spec(spec);spec.loader.exec_module(L)
rows=[r for p in sorted((OUT/'staged').glob('*.jsonl')) for r in L.load_rows(p)]
manifest_path=ROOT/'data/manifest.json';manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
held=[];active=[]
for e in manifest['entries']:
 p=manifest_path.parent/e['path'];dest=active if e['split']=='train' else held
 for r in L.load_rows(p):dest.append({**r,'source_path':str(p.relative_to(ROOT)).replace('\\','/'),'row_sha256':hashlib.sha256(json.dumps(r,ensure_ascii=False,sort_keys=True).encode()).hexdigest()})
assert len(held)==450 and len(active)==47
pairs=[];top=[]
for row in rows:
 scores={}
 for query in held:
  pred=compare(row['problem'],query['problem'])
  if pred['candidate']:pairs.append({'train_id':row['id'],'query_id':query['id'],'query_problem':B.normalize_math(query['problem']),'query_method':query.get('method'),'prediction':pred,'query_row_sha256':query['row_sha256'],'source':query['source_path']})
  key=query.get('problem_id',query['id'])
  score=L.j5(row['problem'],B.normalize_math(query['problem']))
  if key not in scores or score>scores[key]['score_fraction']:scores[key]={'score_fraction':score,'query_id':query['id'],'query_problem':B.normalize_math(query['problem']),'query_method':query.get('method'),'query_solution':B.normalize_math(query['solution']),'query_row_sha256':query['row_sha256']}
 if row['id'] in B.NEW:
  top.append({'id':row['id'],'top':[{'score':str(q['score_fraction']),**{k:v for k,v in q.items() if k!='score_fraction'}} for q in sorted(scores.values(),key=lambda v:v['score_fraction'],reverse=True)[:3]]})
draft_pairs=[]
for i,row in enumerate(rows):
 for other in rows[i+1:]+active:
  score=L.j5(row['problem'],B.normalize_math(other['problem']));pred=compare(row['problem'],B.normalize_math(other['problem']))
  if score>=Fraction(2,5) or 'numeric-normalized-object-and-task' in pred['reasons']:
   draft_pairs.append({'left':row['id'],'right':other['id'],'score':str(score),'prediction':pred,'left_problem':row['problem'],'right_problem':B.normalize_math(other['problem'])})
result={'problems':119,'revised':33,'heldout_method_records':450,'comparisons':len(rows)*len(held),'detector_sha256':implementation_sha256(),'rule':'structure-candidates-v4','calibrated':False,'UNKNOWN_is_not_no_leakage':True,'candidate_pairs':pairs,'top_text_similarity_not_semantic_evidence':top,'draft_and_active_candidates':draft_pairs}
(OUT/'structural-screen-repaired.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'candidate_pairs':len(pairs),'new_candidate_pairs':[(p['train_id'],p['query_id'],p['prediction']['reasons']) for p in pairs if p['train_id'] in B.NEW],'draft_and_active_candidates':draft_pairs,'top':[{ 'id':v['id'],'top':[{k:q[k] for k in ('score','query_id','query_problem','query_method')} for q in v['top']]} for v in top]},ensure_ascii=False))
