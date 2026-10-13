from pathlib import Path
import json,hashlib,copy,re,os
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];D=ROOT/'reviews/2026-10-05-training-diversity-drafts';VERSION='codex-repair-v4-final'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return [json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
def math_sha(r):return hashlib.sha256(json.dumps({k:r[k] for k in ('problem','solution','answer','scene_spec')},ensure_ascii=False,sort_keys=True).encode()).hexdigest()
def canon(r):return hashlib.sha256(json.dumps(r,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
def strings(v):
 if isinstance(v,str):yield v
 elif isinstance(v,list):
  for x in v:yield from strings(x)
 elif isinstance(v,dict):
  for x in v.values():yield from strings(x)
selection=D/'draft-selection.json';before_bytes=selection.read_bytes();before_sha=sha(selection);sel=json.loads(before_bytes);assert len(sel['entries'])==18 and all(e['version']=='codex-repair-v3' for e in sel['entries'])
(OUT/'selector-before-final.json').write_bytes(before_bytes)
check=json.loads((OUT/'independent-check-v3.json').read_text(encoding='utf-8'));assert check['selector_sha256']==before_sha and not check['risks'] and check['counts']['missing_step_prefix']==0
exact=json.loads((OUT/'exact-notation-reverification.json').read_text(encoding='utf-8'));assert exact['exact_checks']==exact['passed']==41
base=json.loads((ROOT/'reviews/codex-supervision/2026-10-05-remaining-batch-audit/baseline.json').read_text(encoding='utf-8'));protected={**base['protected_inputs'],**base['protected_code']};history={}
for e in sel['entries']:
 for version in ('v1','v2','v3'):
  for name in (f'draft-codex-repair-{version}.jsonl',f'DRAFT_REPORT-codex-repair-{version}.md'):
   p=D/e['batch']/name;history[str(p.relative_to(ROOT)).replace('\\','/')]=sha(p)
 for name in ('draft.jsonl',):
  p=D/e['batch']/name;history[str(p.relative_to(ROOT)).replace('\\','/')]=sha(p)
for folder in ('2026-10-05-batch-repair-execution','2026-10-05-remaining-batch-audit'):
 for name in ('delivery-manifest.json','REPAIR_REPORT.md','exact-reverification.json','published-content-check.json'):
  p=ROOT/'reviews/codex-supervision'/folder/name;history[str(p.relative_to(ROOT)).replace('\\','/')]=sha(p)
def guard(check_selector=True):
 assert all(sha(ROOT/p)==h for p,h in {**protected,**history}.items()),'protected/historical source drift'
 if check_selector:assert sha(selection)==before_sha,'selector changed concurrently'
guard();(OUT/'final-baseline.json').write_text(json.dumps({'selector_before_sha256':before_sha,'protected':protected,'historical':history},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
files=[];newentries=[];bindings=[];allids=[]
for e in sel['entries']:
 batch=e['batch'];source=D/e['path'];assert sha(source)==e['sha256'];rows=load(source);original=load(D/batch/'draft.jsonl');assert [x['id'] for x in rows]==[x['id'] for x in original]
 md=[f'# {batch} 精确数学修订文档','',f'版本：{VERSION}。{len(rows)}题；原编号、题数和顺序全部保留，删除0题。题目、推导、答案及场景文本已复验。未正式准入，动画尚未渲染验收。','',f'前身v3 SHA-256：`{e["sha256"]}`。','']
 for row in rows:
  r=copy.deepcopy(row);rid=r['id'];allids.append(rid);prior=copy.deepcopy(r.get('strict_review',{}));lin=r['revision_lineage'];assert lin['original_id']==rid
  lin['previous_selected_version']={'version':e['version'],'path':str(source.relative_to(ROOT)).replace('\\','/'),'sha256':e['sha256'],'versioned_id':r.get('versioned_id')};lin['previous_math_review_binding']={'math_content_sha256':prior.get('math_content_sha256'),'evidence':prior.get('math_review_evidence')};lin['version']=VERSION;lin['historical_risk_not_reset']=True
  r['versioned_id']=f'{VERSION}-20261005-{batch}-{rid}';r['draft_status']='CODEX-REPAIR-v4-final-NOT-ADMITTED';r['review_status']='CODEX_MATH_REVIEW_COMPLETE_PENDING_VERSION_BOUND_ACCEPTANCE';r['admitted']=False;r['animation_render_verified']=False
  mh=math_sha(r);r.setdefault('strict_review',{}).update({'core_math_verified':True,'text_math_fields_reviewed':True,'scene_text_reviewed':True,'exact_expression_required':True,'rational_numbers':'fractions_or_integers','user_review_new_version':'DELEGATED_TO_CODEX_COMPLETED','render_verified':False,'admitted':False,'math_content_sha256':mh,'math_review_evidence':'reviews/codex-supervision/2026-10-05-draft-mail-reverification/selected-math-review-final.json','verification_basis':'HASH_BOUND_PRIOR_MATH_PLUS_EQUIVALENT_NOTATION_AND_SCENE_REVIEW_EXACT_41_CHECKS'})
  for t in strings(r):
   assert '??' not in t and '\ufffd' not in t,(rid,'encoding')
   assert not any(ord(c)<32 or ord(c)==127 for c in t),(rid,'control character')
  for t in strings({k:r[k] for k in ('problem','solution','answer','scene_spec')}):
   for f in re.findall(r'(?<!\\)\$([^$]*)\$',t):
    assert not re.search(r'[\u4e00-\u9fff]|\d+\.\d+',f),(rid,f)
    for case in re.findall(r'\\begin\{cases\}(.*?)\\end\{cases\}',f,re.S):assert all(part.count('&')<=1 for part in case.split('\\\\')),(rid,case)
  assert all(re.match(r'^\s*第[一二三四五六七八九十\d]+步',t) for t in r['scene_spec']['steps'])
  basis='PRIOR_PROOF_WITH_EQUIVALENT_NOTATION_AND_STEP_NUMBERING_RECHECKED'
  if rid=='draft-c15-05':basis='FULL_ORTHOGONAL_DECOMPOSITION_PROOF_REPLACED_ENCODING_LOSS_AND_REVERIFIED'
  bindings.append({'batch':batch,'id':rid,'versioned_id':r['versioned_id'],'math_content_sha256':mh,'record_sha256':canon(r),'basis':basis,'source_v3_record_sha256':canon(row),'admitted':False,'render_verified':False})
  rows[rows.index(row)]=r
  md += [f'## {rid} · {r["concept_id"]}','','**题目**','',r['problem'],'','**推导**','',r['solution'],'','**答案**','',r['answer'],'','**场景对象**','',*['- '+t for t in r['scene_spec']['objects']],'','**场景步骤**','',*['- '+t for t in r['scene_spec']['steps']],'']
 p=D/batch/f'draft-{VERSION}.jsonl';doc=D/batch/f'DRAFT_REPORT-{VERSION}.md';assert not p.exists() and not doc.exists(),'new version already exists'
 p.write_text('\n'.join(json.dumps(r,ensure_ascii=False) for r in rows)+'\n',encoding='utf-8');doc.write_text('\n'.join(md),encoding='utf-8')
 ne={**e,'path':f'{batch}/{p.name}','sha256':sha(p),'version':VERSION,'source_sha256':e['sha256'],'report_path':f'{batch}/{doc.name}','report_sha256':sha(doc)};newentries.append(ne);files.append({**ne,'root_path':str(p.relative_to(ROOT)).replace('\\','/'),'root_report_path':str(doc.relative_to(ROOT)).replace('\\','/')})
 assert all(all(r[k] in doc.read_text(encoding='utf-8') for k in ('problem','solution','answer')) for r in rows)
 assert all(t in doc.read_text(encoding='utf-8') for r in rows for t in r['scene_spec']['steps'])
assert len(allids)==len(set(allids))==264 and len(bindings)==264
review={'version':VERSION,'record_count':264,'basis':'Previous fully reviewed v1 mathematical sources plus all v1-to-v3 deltas independently inspected; six changed main-math records reviewed, scene formatting and numbering reviewed; c15-05 complete proof reconstructed.','exact_checks_path':'reviews/codex-supervision/2026-10-05-draft-mail-reverification/exact-notation-reverification.json','exact_checks_sha256':sha(OUT/'exact-notation-reverification.json'),'passed_exact_checks':41,'prior_math_evidence':[{'path':p,'sha256':h} for p,h in history.items() if p.endswith('/exact-reverification.json')],'no_decimal_math':True,'no_encoding_replacement':True,'actual_render_verified':False,'formal_admission':False,'records':bindings,'selected_files':files}
(OUT/'selected-math-review-final.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
guard();newsel=copy.deepcopy(sel);newsel['entries']=newentries;newsel['updated_by']='codex-mail-repair-final-2026-10-05';newsel['selected_drafts']=264;tmp=selection.with_name('draft-selection.codex-mail-final-next.json');tmp.write_text(json.dumps(newsel,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');assert sha(selection)==before_sha;os.replace(tmp,selection);guard(False)
result={'version':VERSION,'selected_drafts':264,'ids_and_order_preserved':True,'deleted_questions':0,'selector_before_sha256':before_sha,'selector_final_sha256':sha(selection),'files':files,'review_evidence_sha256':sha(OUT/'selected-math-review-final.json'),'protected_and_historical_files_unchanged':True,'production_manifest_modified':False,'admission':False,'render_verified':False}
(OUT/'final-publication.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:v for k,v in result.items() if k!='files'},ensure_ascii=False))
