"""Independent binding and exact-span checks. Never import correspondence builder or execute records."""
import hashlib,json,re,shutil
from fractions import Fraction
from pathlib import Path
R=Path(r'D:\Animation-Model-Training');A=R/'archives/reviews/codex-supervision/2026-10-17-first-batch-exact-math-review'
H=R/'reviews/data-prep/2026-10-17-submission/asset-evidence/math-correspondence'
sha=lambda b:hashlib.sha256(b).hexdigest()
enc=lambda x:json.dumps(x,ensure_ascii=True,sort_keys=True,separators=(',',':')).encode()
g=R/(A/'generation-path.txt').read_text();done=json.loads((g/'COMPLETE.json').read_bytes())
for item in done['artifacts']:
 raw=(g/item['path']).read_bytes();assert sha(raw)==item['sha256'] and len(raw)==item['bytes']
index=json.loads((g/'input-index.json').read_bytes())
for rel,pin in index['input_pins'].items():
 raw=(R/rel).read_bytes();assert sha(raw)==pin['sha256'] and len(raw)==pin['bytes']
rows=[json.loads(x) for x in (g/'math-correspondence.jsonl').read_bytes().splitlines()]
batch=json.loads((H.parent/'first-batch-10.v2.json').read_bytes())
reviews=json.loads((A/'candidate/record-reviews.json').read_bytes())
candidate_raw=(A/'candidate/records.jsonl').read_bytes();lines=candidate_raw.splitlines(keepends=True)
assert sha(candidate_raw)==reviews['candidate_file_sha256']
assert len(rows)==len(lines)==len(reviews['records'])==10
counts={'fields':0,'items':0,'formula_spans':0,'segments':0,'candidate_sources':0}
bindings={}
for row,selected,review,line in zip(rows,batch['records'],reviews['records'],lines):
 b=selected['source'];p=R/b['path'];data=p.read_bytes();raw=data.splitlines(keepends=True)[b['line']-1];obj=json.loads(raw);new=json.loads(line)
 assert sha(data)==b['file_sha256'] and sha(raw)==b['raw_line_sha256'] and sha(enc(obj))==b['canonical_record_sha256']
 assert row['sample_id']==obj['id']==new['id']==review['sample_id']
 assert row['source']==b
 expected={k:obj[k] for k in ['problem','solution','answer']}
 for key in ['objects','steps']:
  expected.update({f'scene_spec.{key}[{i}]':v for i,v in enumerate(obj['scene_spec'][key])})
 assert set(row['fields'])==set(expected)
 for field,scanned in row['fields'].items():
  text=expected[field];assert text==scanned['text'];counts['fields']+=1
  cursor=0
  for seg in scanned['segments']:
   assert seg['start']==cursor and seg['end']>cursor and text[seg['start']:seg['end']]==seg['text']
   cursor=seg['end'];counts['segments']+=1
  assert cursor==len(text)
  for span in scanned['formula_spans']:
   assert text[span['start']:span['end']]==span['text'];counts['formula_spans']+=1
  for item in scanned['items']:
   assert text[item['start']:item['end']]==item['value'] and item['verdict']=='PENDING_REVIEW'
   if item['kind']=='decimal_literal' and item['literal_fraction_candidate']is not None:
    assert Fraction(item['value'])==Fraction(item['literal_fraction_candidate'])
   counts['items']+=1
 assert row['math_verdict']==row['geometry_verdict']=='PENDING_REVIEW'
 assert sha(line)==review['candidate_raw_line_sha256'] and sha(enc(new))==review['candidate_canonical_record_sha256']
 assert sha(enc({k:obj[k] for k in ['problem','solution','answer','scene_spec']}))==review['original_math_content_sha256']
 assert sha(enc({k:new[k] for k in ['problem','solution','answer','scene_spec']}))==review['candidate_math_content_sha256']
 assert review['math_text_verdict']=='PASS_EXACT_MATH_TEXT_CANDIDATE'
 assert review['native_render']=='PENDING_REVIEW' and review['user_review']is None
 assert len(new['scene_spec']['steps'])==len(obj['scene_spec']['steps'])
 for key in set(obj)-{'problem','solution','answer','scene_spec'}:assert obj[key]==new[key]
 alltext=[new[k] for k in ['problem','solution','answer']]+new['scene_spec']['objects']+new['scene_spec']['steps']
 assert all(not re.search(r'\d+\.\d+|\\approx',text) for text in alltext)
 for text in alltext:
  assert text.count('$')%2==0
  counts['candidate_sources']+=1
 bindings[b['path']]={'sha256':sha(data),'bytes':len(data)}
assert (H/'math-correspondence.jsonl').read_bytes()==(A/'before/math-correspondence.jsonl').read_bytes()
proof=json.loads((A/'exact-proof-results.json').read_bytes())
assert proof['check_count']==len(proof['checks'])==35 and all(x['result']=='PASS' for x in proof['checks'])
W=R/'reviews/codex-supervision/2026-10-17-auto-start/runs/start-5726318d1c4544318e0fb76498098ae3'
packet=json.loads((W/'signals.json').read_bytes());wanted={x['detail']['tool_id'] for x in packet['signals'] if x['kind']=='PROJECT_TOOL_USE'}
log=Path(r'C:\Users\Jacap\.claude\projects\d--code\ee005e1f-71f1-4697-a746-054f6399acd6.jsonl')
with log.open('rb') as f:f.seek(max(0,log.stat().st_size-2*1024*1024));f.readline();records=f.readlines()
mapped=[]
for raw in records:
 try:obj=json.loads(raw)
 except Exception:continue
 content=obj.get('message',{}).get('content',[])
 if not isinstance(content,list):continue
 for tool in content:
  if isinstance(tool,dict) and tool.get('id') in wanted:
   inp=tool.get('input',{});d={'id':tool['id'],'name':tool.get('name'),'file_path':inp.get('file_path'),'input_sha256':sha(enc(inp)),'command_prefix':str(inp.get('command',''))[:240]}
   if tool.get('name')=='Write':
    assert inp['content'].encode().replace(b'\r\n',b'\n')==(A/'before/build_math_correspondence.py').read_bytes().replace(b'\r\n',b'\n')
    d['matches_original_snapshot']=True
   mapped.append(d)
assert {x['id'] for x in mapped}==wanted
(A/'activity-mapping.json').write_bytes(enc({'tools':mapped,'process_signals':[x for x in packet['signals'] if x['kind']!='PROJECT_TOOL_USE'],'scope':'PROCESS_OBSERVATION_IS_NOT_EXECUTION_PROOF'})+b'\n')
for rel,pin in index['input_pins'].items():bindings[rel]=pin
for name in ['build_math_correspondence.py','test_math_correspondence.py']:
 raw=(H/name).read_bytes();bindings[(H/name).relative_to(R).as_posix()]={'sha256':sha(raw),'bytes':len(raw)}
(A/'current-source-bindings.json').write_bytes(enc(bindings)+b'\n')
(A/'independent-verification.json').write_bytes(enc({'status':'PASS_NAMED_EXACT_MATH_TEXT_CANDIDATES_AND_LEXICAL_BINDING_ONLY',
 'records':10,'counts':counts,'mapped_tool_ids':len(wanted),'mapped_log_records':len(mapped),
 'process_signals_not_execution_proof':len(packet['signals'])-len(wanted),'exact_math_checks':35,
 'original_correspondence_preserved':True,'formal_data_unchanged':True,
 'candidate_file_sha256':sha(candidate_raw),'generation':g.relative_to(R).as_posix(),
 'native_geometry_and_render':'PENDING_REVIEW','production':'CLOSED','global_isolation':'NOT_ESTABLISHED'})+b'\n')
for d in ['after','generation']:
 (A/d).mkdir(exist_ok=True)
for name in ['build_math_correspondence.py','test_math_correspondence.py']:shutil.copyfile(H/name,A/'after'/name)
shutil.copytree(g,A/'generation',dirs_exist_ok=True)
watch=json.loads((R/'reviews/codex-supervision/2026-10-04-live-watch/latest.json').read_bytes())
(A/'observer-summary.json').write_bytes(enc({k:watch.get(k) for k in ['time','head','child_jobs','core_drift']})+b'\n')
print(json.dumps({'records':10,'counts':counts,'checks':35,'mapped_tools':len(wanted),'mapped_records':len(mapped),'current_pins':len(bindings)}))
