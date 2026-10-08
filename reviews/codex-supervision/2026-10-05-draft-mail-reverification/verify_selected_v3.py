from pathlib import Path
import json,hashlib,re,sys,collections
ROOT=Path(r'D:/Animation-Model-Training');OUT=Path(__file__).resolve().parent;D=ROOT/'reviews/2026-10-05-training-diversity-drafts'
sys.path.insert(0,str(ROOT/'src'))
from animtrain.manifest import Manifest
from animtrain.validate import validate_manifest
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return [json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
def strings(x,path=''):
 if isinstance(x,str):yield path,x
 elif isinstance(x,list):
  for i,y in enumerate(x):yield from strings(y,path+f'[{i}]')
 elif isinstance(x,dict):
  for k,y in x.items():yield from strings(y,path+'.'+k)
a=ROOT/'reviews/codex-supervision/2026-10-05-batch-repair-execution';b=ROOT/'reviews/codex-supervision/2026-10-05-remaining-batch-audit'
m1=json.loads((a/'delivery-manifest.json').read_text(encoding='utf-8'));m2=json.loads((b/'delivery-manifest.json').read_text(encoding='utf-8'));old={x['batch']:x for x in m1['entries']+m2['files']}
selector=D/'draft-selection.json';sel=json.loads(selector.read_text(encoding='utf-8'));files=[];changes=[];risks=[];counts=collections.Counter();ids=[]
for e in sel['entries']:
 batch=e['batch'];p=D/e['path'];md=D/e['report_path'];base=(a if int(batch[-2:])<9 else b)/'staged'/f'{batch}.jsonl';assert sha(base)==old[batch]['sha256']
 before=load(base);after=load(p);assert [x['id'] for x in before]==[x['id'] for x in after]
 assert sha(p)==e['sha256'];assert sha(md)==e['report_sha256'];counts['records']+=len(after);ids.extend(x['id'] for x in after)
 for oldrow,row in zip(before,after):
  changed={k:{'before':oldrow.get(k),'after':row.get(k)} for k in oldrow.keys()|row.keys() if oldrow.get(k)!=row.get(k)}
  if changed:changes.append({'batch':batch,'id':row['id'],'fields':changed})
  assert row['admitted'] is False and row['animation_render_verified'] is False
  spec=row['scene_spec'];counts['steps']+=len(spec['steps']);pref=re.compile(r'^\s*第[一二三四五六七八九十\d]+步')
  counts['missing_step_prefix']+=sum(not pref.match(s) for s in spec['steps'])
  counts['restored_step_prefix']+=sum(not pref.match(s) for s in oldrow['scene_spec']['steps'])
  for field,text in strings(row):
   if '??' in text or '\ufffd' in text:risks.append({'id':row['id'],'field':field,'code':'ENCODING_REPLACEMENT','text':text})
  for field,text in strings({k:row[k] for k in ('problem','solution','answer','scene_spec')}):
   for formula in re.findall(r'(?<!\\)\$([^$]*)\$',text):
    if re.search(r'[\u4e00-\u9fff]',formula):risks.append({'id':row['id'],'field':field,'code':'CJK_MATH','formula':formula})
    if re.search(r'\d+\.\d+',formula):risks.append({'id':row['id'],'field':field,'code':'DECIMAL_MATH','formula':formula})
    if re.search(r'\^\d{2,}',formula):risks.append({'id':row['id'],'field':field,'code':'UNBRACED_EXPONENT','formula':formula})
    for case in re.findall(r'\\begin\{cases\}(.*?)\\end\{cases\}',formula,re.S):
     parts=case.split('\\\\')
     if any(x.count('&')>1 for x in parts):risks.append({'id':row['id'],'field':field,'code':'CASES_ROW_DELIMITERS','formula':formula})
  expected=row.get('strict_review',{}).get('math_content_sha256')
  if expected:
   counts['legacy_math_binding_present']+=1
   current_math=hashlib.sha256(json.dumps({k:row[k] for k in ('problem','solution','answer','scene_spec')},ensure_ascii=False,sort_keys=True).encode()).hexdigest()
   if current_math!=expected:counts['stale_math_content_sha256']+=1
 files.append({'batch':batch,'count':len(after),'path':str(p.relative_to(ROOT)).replace('\\','/'),'sha256':sha(p),'old_delivered_sha256':old[batch]['sha256'],'old_delivery_matches_current':sha(D/batch/'draft-codex-repair-v1.jsonl')==old[batch]['sha256'],'report_path':str(md.relative_to(ROOT)).replace('\\','/'),'report_sha256':sha(md),'md_contains_current_math':all(all(row[k] in md.read_text(encoding='utf-8') for k in ('problem','solution','answer')) for row in after)})
assert counts['records']==264 and len(set(ids))==264
v=validate_manifest(Manifest.load(ROOT/'data/manifest.json'),ROOT/'data')
result={'selector_sha256':sha(selector),'counts':dict(counts),'changed_rows':len(changes),'changed_math_ids':[x['id'] for x in changes if any(k in x['fields'] for k in ('problem','solution','answer'))],'old_delivery_jsonl_mismatches':sum(not x['old_delivery_matches_current'] for x in files),'md_current_math_mismatches':[x['batch'] for x in files if not x['md_contains_current_math']],'risks':risks,'files':files,'production_manifest_sha256':sha(ROOT/'data/manifest.json'),'production_validation':v,'formal_admission':False,'actual_render_verified':False}
(OUT/'independent-check-v3.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(OUT/'field-delta-v3.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('counts','changed_rows','changed_math_ids','old_delivery_jsonl_mismatches','md_current_math_mismatches','risks')},ensure_ascii=False,indent=2))
