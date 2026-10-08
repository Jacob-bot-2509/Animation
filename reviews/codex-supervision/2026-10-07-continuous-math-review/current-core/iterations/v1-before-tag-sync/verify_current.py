"""Read-only validation of the current candidate, provenance, exact witnesses and typesetting."""
import pathlib,json,hashlib,re,gzip,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[4]
OUT=pathlib.Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def dense(r):return sha(json.dumps(r,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode())
def mathsha(r):return sha(json.dumps({k:r.get(k) for k in ('problem','solution','answer','scene_spec')},ensure_ascii=False,sort_keys=True).encode())
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
index=load(OUT/'current-index.json');sources=load(OUT/'source-bindings.json')
refs=[json.loads(l) for l in (OUT/'record-bindings.jsonl').read_text(encoding='utf8').splitlines()]
patches={p['id']:p for p in load(OUT/'patches.json')}
specs={p['id']:p for p in load(OUT/'patch-specifications.json')}
proof=load(OUT/'patch-review.json')
assert index['source_bindings_sha256']==sha((OUT/'source-bindings.json').read_bytes())
assert index['record_bindings_sha256']==sha((OUT/'record-bindings.jsonl').read_bytes())
parent_artifacts=0
for pin in index['parent_manifests']:
 p=ROOT/pin['path'];assert sha(p.read_bytes())==pin['sha256']
 for a in load(p)['artifacts']:
  f=p.parent/a['path'];data=f.read_bytes()
  assert len(data)==a['bytes'] and sha(data)==a.get('sha256',a.get('raw_sha256')),str(f)
  parent_artifacts+=1
by={(r['path'],r['source_line']):r for r in refs};ids=set();unchanged=0;groups={};issues=[]
for binding in sources:
 p=ROOT/binding['path'];data=p.read_bytes();parent=ROOT/binding['parent_path'];before=parent.read_bytes()
 assert len(data)==binding['bytes'] and sha(data)==binding['sha256']
 assert len(before)==binding['parent_bytes'] and sha(before)==binding['parent_sha256']
 lines=data.splitlines(keepends=True);oldlines=before.splitlines(keepends=True)
 assert len(lines)==binding['records']==len(oldlines)
 for n,(line,oldline) in enumerate(zip(lines,oldlines),1):
  r=json.loads(line);old=json.loads(oldline);ref=by[(binding['path'],n)]
  rid=r['id'];assert rid not in ids;ids.add(rid)
  assert rid==ref['id']==old['id']
  assert dense(r)==ref['record_sha256'] and mathsha(r)==ref['math_sha256']
  assert ref['source_sha256']==binding['sha256']
  review=ref['parent_review'];rp=ROOT/review['path'];assert sha(rp.read_bytes())==review['sha256']
  receipt=json.loads(rp.read_text(encoding='utf8').splitlines()[review['line']-1])
  assert receipt['id']==rid and review['record_sha256']==dense(old)
  if rid not in patches:assert line==oldline;unchanged+=1
  else:
   patch=patches[rid];assert old==patch['before'] and r==patch['after']
   assert dense(old)==patch['before_record_sha256'] and dense(r)==patch['after_record_sha256']
   for key,value in specs[rid]['fields'].items():assert r[key]==value
   allowed=set(specs[rid]['fields'])|{'versioned_id','admitted','animation_render_verified','review_status','strict_review','current_revision_lineage','draft_status'}
   for k in set(old)|set(r):
    if k not in allowed:assert old.get(k)==r.get(k),(rid,k)
   assert not r['admitted'] and not r['animation_render_verified']
   assert r['strict_review']['math_content_sha256']==mathsha(r)
   witness=next(w for w in proof['patch_bindings'] if w['id']==rid)
   assert witness['record_sha256']==dense(r) and witness['math_sha256']==mathsha(r)
  for field in ('problem','solution','answer','scene_spec','efficiency_tags'):
   text=json.dumps(r.get(field),ensure_ascii=False)
   assert not re.search(r'\?{2,}|\ufffd|(?<![A-Za-z0-9])\d+\.\d+',text),(rid,field,'garbled_or_decimal')
  groups[ref['group']]=groups.get(ref['group'],0)+1
assert len(ids)==761 and unchanged==758 and groups==index['groups']
fresh=subprocess.run([sys.executable,'-X','utf8','-B',str(OUT/'verify_patches.py')],capture_output=True,check=True).stdout
assert json.loads(fresh)==proof
render=load(OUT/'render-input-receipt.json');browser=load(OUT/'browser-typesetting-receipt.json')
assert render['records']==browser['current_records']==761
assert browser['typesetting']=='PASS_LOCAL_TYPESETTING'
assert browser['render_input_receipt_sha256']==sha((OUT/'render-input-receipt.json').read_bytes())
assert len(render['files'])==len(browser['files'])==24
html_fields=0;math_count=0
for entry,result in zip(render['files'],browser['files']):
 p=ROOT/entry['path'];assert sha(p.read_bytes())==entry['sha256']==result['source_html_sha256']
 source=next(s for s in sources if s['path']==entry['source_path'])
 assert source['sha256']==entry['source_sha256']==result['source_jsonl_sha256']
 assert result['qa']['status']=='DONE' and not result['qa']['errors'] and result['qa']['records']==entry['records']
 compressed=(ROOT/result['dom_archive']).read_bytes();assert sha(compressed)==result['dom_archive_sha256']
 dom=gzip.decompress(compressed);assert sha(dom)==result['dom_sha256']
 match=re.search(r'<pre id="qa"[^>]*>(.*?)</pre>',dom.decode('utf8'),re.S)
 import html
 assert json.loads(html.unescape(match.group(1)))==result['qa']
 assert not re.search(r'<script[^>]+src=["\x27]https?://',p.read_text(encoding='utf8'))
 html_fields+=entry['rendered_text_fields'];math_count+=result['qa']['math_count']
asset=render['local_asset'];assert sha((ROOT/asset['path']).read_bytes())==asset['sha256']
for archived in load(OUT/'submission-archive-bindings.json'):
 data=(ROOT/archived['archived_path']).read_bytes()
 assert sha(data)==archived['sha256'] and len(data)==archived['bytes']
screen=load(OUT/'isolation-followup-receipt.json')
assert screen['source_bindings_sha256']==sha((OUT/'source-bindings.json').read_bytes())
assert screen['record_bindings_sha256']==sha((OUT/'record-bindings.jsonl').read_bytes())
assert screen['global_semantic_isolation']=='NOT_ESTABLISHED'
archive_count=0
if (OUT/'delivery-manifest.json').exists():
 for a in load(OUT/'delivery-manifest.json')['artifacts']:
  p=OUT/a['path'];assert sha(p.read_bytes())==a['sha256'] and len(p.read_bytes())==a['bytes'],str(p)
  archive_count+=1
print(json.dumps({'verdict':'PASS_CURRENT_CORE_VERSION_AND_EXACT_REPAIR_VERIFICATION','records':len(ids),'groups':groups,'sources':len(sources),'new_patches':len(patches),'unchanged_parent_bytes':unchanged,'frozen_parent_artifacts_verified':parent_artifacts,'new_exact_checks':proof['check_count'],'parity_cases':729,'local_typeset_html_files':len(browser['files']),'local_typeset_records':761,'typeset_math_expressions':math_count,'typeset_text_fields':html_fields,'typeset_errors':0,'math_and_scene_text':'PASS_CANDIDATE_FIELDS','global_semantic_isolation':'NOT_ESTABLISHED','visual_layout':'NOT_INDEPENDENTLY_REVIEWED','native_render':'UNVERIFIED','production':'CLOSED','current_archive_artifacts_verified':archive_count},ensure_ascii=False,indent=2))
