"""版本明确的起草协调账本：草稿数量不等于训练验收。只读数据。"""
from __future__ import annotations
import hashlib,json,re,sys
from fractions import Fraction
from pathlib import Path
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'configs/training_diversity_policy.json').is_file())
DRAFTS=ROOT/'reviews/2026-10-05-training-diversity-drafts'
THRESHOLD=Fraction(2,5)

def load_rows(path:Path)->list[dict]:
 return [json.loads(line) for line in path.read_text(encoding='utf-8-sig').splitlines() if line.strip()]

def j5(a:str,b:str)->Fraction:
 def grams(s):
  s=re.sub(r'\s+','',s)
  return {s[i:i+5] for i in range(max(0,len(s)-4))}
 ga,gb=grams(a),grams(b)
 return Fraction(len(ga&gb),len(ga|gb)) if ga and gb else Fraction(0)

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def selected_files(drafts:Path)->list[dict]:
 selection=drafts/'draft-selection.json';explicit={}
 if selection.is_file():
  data=json.loads(selection.read_text(encoding='utf-8'))
  for row in data['entries']:
   batch=row['batch']
   if batch in explicit:raise ValueError(f'duplicate selection: {batch}')
   explicit[batch]=row
 result=[]
 for directory in sorted(drafts.glob('batch-*')):
  if not directory.is_dir():continue
  batch=directory.name
  if batch in explicit:
   e=explicit.pop(batch);path=(drafts/e['path']).resolve()
   if path.parent!=directory.resolve() or path.suffix!='.jsonl':raise ValueError(f'invalid selected path: {batch}')
   if not path.is_file() or digest(path)!=e['sha256']:raise ValueError(f'selected version hash mismatch: {batch}')
   method='EXPLICIT_HASH_BOUND_SELECTION'
  else:
   candidates=[]
   for path in directory.glob('draft*.jsonl'):
    if path.name=='draft.jsonl':candidates.append((1,path))
    else:
     match=re.fullmatch(r'draft-v(\d+)\.jsonl',path.name)
     if match:candidates.append((int(match.group(1)),path))
   if not candidates:continue
   if len({n for n,p in candidates})!=len(candidates):raise ValueError(f'ambiguous version: {batch}')
   path=max(candidates,key=lambda item:item[0])[1];method='LATEST_NUMBERED_AUTHOR_DRAFT_PENDING_REVIEW'
  result.append({'batch':batch,'path':str(path.relative_to(drafts)).replace('\\','/'),'sha256':digest(path),'selection':method,'absolute_path':path})
 if explicit:raise ValueError(f'missing selected batches: {sorted(explicit)}')
 return result

def selected_rows(drafts:Path)->tuple[list[dict],list[dict]]:
 files=selected_files(drafts);rows=[];seen=set()
 for entry in files:
  for row in load_rows(entry['absolute_path']):
   if not isinstance(row.get('id'),str) or row['id'] in seen:raise ValueError(f'duplicate or missing question id: {row.get("id")}')
   seen.add(row['id']);rows.append({**row,'selected_batch':entry['batch'],'selected_sha256':entry['sha256']})
 return rows,files

def planning_counts(concepts:list[dict],active:list[dict],drafts:list[dict],catalog:dict)->list[dict]:
 counts={c['id']:{'concept_id':c['id'],'concept':c['name'],'active':0,'drafted':0,'math_reviewed_drafts':0,'newly_admitted':0} for c in concepts}
 unmapped=[]
 for row in active:
  cid=row.get('concept_id') or catalog.get(row['id'])
  if cid in counts:counts[cid]['active']+=1
  else:unmapped.append(row['id'])
 for row in drafts:
  cid=row.get('concept_id')
  if cid not in counts:raise ValueError(f'unknown concept id: {row["id"]}/{cid}')
  counts[cid]['drafted']+=1
  if row.get('strict_review',{}).get('core_math_verified') is True:counts[cid]['math_reviewed_drafts']+=1
 # A math review or an author's admitted flag cannot admit a draft. This tool does
 # not validate production certificates, so only manifest-active counts are used.
 for v in counts.values():
  v['planning_total']=v['active']+v['drafted']
  v['formal_density_pass']=False
  v['reason']='DRAFTS_ARE_NOT_VERSION_BOUND_ACCEPTANCE_OR_DISTINCT_STRUCTURE_EVIDENCE'
 return list(counts.values()),unmapped

def report()->dict:
 policy=json.loads((ROOT/'configs/training_diversity_policy.json').read_text(encoding='utf-8'))
 drafts,files=selected_rows(DRAFTS)
 manifest_path=ROOT/'data/manifest.json';manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
 active=[]
 for e in manifest['entries']:
  if e['split']!='train':continue
  path=(manifest_path.parent/e['path']).resolve()
  if digest(path)!=e['sha256']:raise ValueError('active manifest hash mismatch')
  active.extend(load_rows(path))
 if len({r['id'] for r in active})!=len(active):raise ValueError('duplicate active id')
 catalog_path=ROOT/'reviews/codex-supervision/2026-10-05-mail-handling/candidate-recovery/candidate_catalog.json'
 catalog={r['id']:r['concept_id'] for r in json.loads(catalog_path.read_text(encoding='utf-8'))['records']}
 counts,unmapped=planning_counts(policy['concepts'],active,drafts,catalog)
 pairs=[]
 for i,left in enumerate(drafts):
  for right in drafts[i+1:]+active:
   score=j5(left['problem'],right['problem'])
   if score>=THRESHOLD:pairs.append({'left':left['id'],'right':right['id'],'J5':str(score),'same_concept':left.get('concept_id')==right.get('concept_id',catalog.get(right['id'])),'status':'PENDING_MANUAL_STRUCTURAL_REVIEW','text_similarity_is_not_semantic_verdict':True})
 return {'selected_files':[{k:v for k,v in f.items() if k!='absolute_path'} for f in files],'selected_drafts':len(drafts),'active_train':len(active),'threshold':str(THRESHOLD),'concepts':counts,'unmapped_active_ids':unmapped,'candidate_pairs':pairs,'new_draft_admissions':0,'formal_density_certified':False,'missing_version_bound_acceptance':True,'requirements':{'min_reviewed_samples_per_concept':policy['min_reviewed_samples_per_concept'],'target_max_per_concept':policy['target_max_per_concept'],'min_distinct_variant_kinds_per_concept':policy['min_distinct_variant_kinds_per_concept']},'structural_detector_negative_not_proof':True}

def main()->int:
 try:data=report()
 except (OSError,ValueError,KeyError) as error:
  print(f'账本停止：{error}',file=sys.stderr);return 2
 if '--json' in sys.argv:print(json.dumps(data,ensure_ascii=False,indent=2));return 0
 print(f"选中草稿 {data['selected_drafts']} 题；活动训练 {data['active_train']} 题；本账本新增验收数 0。")
 print('起草数量仅用于安排生产，不作为训练密度或结构多样性验收。')
 print('考点 | 活动 | 草稿 | 草稿数学复核 | 生产规划合计')
 for c in sorted(data['concepts'],key=lambda c:(c['planning_total'],c['concept_id'])):
  print(f"{c['concept_id']} {c['concept']} | {c['active']} | {c['drafted']} | {c['math_reviewed_drafts']} | {c['planning_total']}")
 print(f"文字相似候选阈值 {data['threshold']}；全部候选须人工结构复核：")
 for p in data['candidate_pairs']:print(f"J5={p['J5']} {p['left']} <-> {p['right']}；同考点={p['same_concept']}；待复核")
 print('形式验收未认证；数学复核、文字相似度和原始变体标签均不能代替版本绑定的准入证据。')
 return 0
if __name__=='__main__':raise SystemExit(main())
