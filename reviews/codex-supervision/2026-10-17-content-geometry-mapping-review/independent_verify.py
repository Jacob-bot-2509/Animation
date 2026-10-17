"""Independent output verifier; reads plans and dataset bytes, never imports the generator."""
import hashlib,json,shutil
from pathlib import Path
R=Path(r'D:\Animation-Model-Training');A=R/'archives/reviews/codex-supervision/2026-10-17-content-geometry-mapping-review'
H=R/'reviews/data-prep/2026-10-17-submission/asset-evidence/content-geometry-mapping'
sha=lambda b:hashlib.sha256(b).hexdigest()
enc=lambda x:json.dumps(x,sort_keys=True,ensure_ascii=True,separators=(',',':')).encode()
g=R/(A/'generation-final-path.txt').read_text()
result=json.loads((g/'mapping.json').read_bytes());complete=json.loads((g/'COMPLETE.json').read_bytes())
assert len(result['records'])==10
for name,pin in complete['files'].items():
 raw=(g/name).read_bytes();assert sha(raw)==pin['sha256'] and len(raw)==pin['bytes']
assert complete['input_pins']==result['input_pins']
live={}
for k,pin in result['input_pins'].items():
 p=R/pin['path'];raw=p.read_bytes();assert sha(raw)==pin['sha256'] and len(raw)==pin['bytes']
 live[pin['path']]={'sha256':sha(raw),'bytes':len(raw)}
batch=json.loads((H.parent/'first-batch-10.v2.json').read_bytes())
old=[json.loads(x) for x in (A/'before/content-geometry-mapping.jsonl').read_bytes().splitlines()]
assert [x['sample_id'] for x in result['records']]==[x['sample_id'] for x in batch['records']]
records=[];totalchars=0;source_lines=[]
for row,selected,oldrow in zip(result['records'],batch['records'],old):
 source=row['source'];p=R/source['path'];data=p.read_bytes()
 assert sha(data)==source['file_sha256']
 raw=data.splitlines(keepends=True)[source['line']-1]
 obj=json.loads(raw)
 assert obj['id']==row['sample_id']==selected['sample_id']
 assert sha(raw)==source['raw_line_sha256']
 assert sha(enc(obj))==source['canonical_record_sha256']
 live[source['path']]={'sha256':sha(data),'bytes':len(data)}
 texts=[obj['problem'],*obj['scene_spec']['steps'],obj['answer']]
 assert row['full_content_plan']['sources']==texts
 for key,expected in [('full_content_plan',texts),('steps_plan',obj['scene_spec']['steps'])]:
  plan=row[key];assert plan['sources']==expected
  assert sha(enc(plan))==row[key+'_sha256']
  pieces=[[] for _ in expected]
  for line in plan['rows']:
   i=line['source_index'];assert type(i)is int and 0<=i<len(expected)
   pieces[i].extend(line['fragments'])
  for text,frags in zip(expected,pieces):
   cursor=0;reconstructed=''
   for f in frags:
    assert f['start']==cursor and f['end']>cursor
    rawpart=text[f['start']:f['end']]
    if f['kind']=='math':assert rawpart=='$'+f['content']+'$'
    elif f['kind']=='break':assert rawpart==f['content']
    elif f['kind']=='text':assert rawpart.replace('\\$','$')==f['content']
    else:raise AssertionError('unknown fragment')
    reconstructed+=rawpart;cursor=f['end']
   assert reconstructed==text and cursor==len(text)
  pages=plan['provisional_pages']
  assert [i for page in pages for i in page]==list(range(len(plan['rows'])))
  assert all(0<len(page)<=plan['per_page_lines'] for page in pages)
 assert len(row['steps_plan']['rows'])==oldrow['plan_rows']
 assert len(row['steps_plan']['provisional_pages'])==oldrow['plan_pages_provisional']
 plan=row['steps_plan']
 oldplan={k:plan[k] for k in ['schema','sources','chunk_chars','per_page_lines','rows','provisional_pages','layout','source_sha256']}
 oldplan['rows']=[{'source_index':line['source_index'],'fragments':[{k:f[k] for k in ['kind','content','start','end']} for f in line['fragments']]} for line in plan['rows']]
 oldencoding=json.dumps(oldplan,ensure_ascii=True,separators=(',',':')).encode()
 assert sha(oldencoding)==oldrow['plan_sha256']
 assert row['math_verdict']==row['geometry_verdict']=='PENDING_REVIEW' and row['user_review']is None
 assert all(c['verdict']=='PENDING_REVIEW' and c['record_correspondence']=='NOT_ESTABLISHED' for c in row['legacy_geometry_checklist'])
 for span in row['lexical_occurrences']:
  text=obj['problem'] if span['field']=='problem' else obj['answer'] if span['field']=='answer' else obj['scene_spec']['steps'][span['index']]
  assert text[span['start']:span['end']]==span['keyword']
 totalchars+=sum(map(len,texts))
 records.append({'id':row['sample_id'],'source':source,'template':row['template'],'steps':len(obj['scene_spec']['steps']),
                 'step_rows':row['provisional_step_rows'],'provisional_step_pages':row['provisional_step_pages'],
                 'full_content_rows':len(row['full_content_plan']['rows']),
                 'legacy_geometry_items':len(row['legacy_geometry_checklist']),'exact_span_reconstruction':'PASS'})
 source_lines.append(raw)
assert (H/'content-geometry-mapping.jsonl').read_bytes()==(A/'before/content-geometry-mapping.jsonl').read_bytes()
b5=R/'archives/reviews/codex-supervision/2026-10-17-b5-readiness-audit'
manifest=json.loads((b5/'delivery-manifest.json').read_bytes())
for x in manifest['artifacts']:
 raw=(b5/x['path']).read_bytes();assert sha(raw)==x['sha256'] and len(raw)==x['bytes']
b5_live={'tools/b5_annotation_set.py':'0260f887b3e2131c205a9b972da3801625b1c1e9f7000ad6f75ae085d7136365',
'tools/b5_calibrate.py':'55a5cc6c8d2293c67551ab8270dff857809ea328395e8208fb1bb91651b7e29b',
'src/animtrain/b5_output.py':'1892f47a2c0a4ee781bedd0e6557eb9856f1a2121e729c176cdd25cbf4f46953',
'tests/test_b5_output_safety.py':'f0ff0c7c1d356170fb9ba3aa43ee45ac8004823b3c3346dec0a721d53551e433'}
for rel,digest in b5_live.items():assert sha((R/rel).read_bytes())==digest
(A/'independent-verification.json').write_bytes(enc({'status':'PASS_STATIC_SOURCE_COVERAGE_ONLY','records':records,
 'complete_source_characters':totalchars,'old_steps_plan_hashes_unchanged':10,'old_mapping_preserved':True,
 'B5_reuse':{'archive':b5.relative_to(R).as_posix(),'verified_artifacts':len(manifest['artifacts']),'reply_id':'msg_1792234276791_895','live_tools':b5_live},
 'generation':g.relative_to(R).as_posix()})+b'\n')
(A/'current-source-bindings.json').write_bytes(enc(live)+b'\n')
(A/'selected-original-source-lines.jsonl').write_bytes(b''.join(source_lines))
for folder in ['after','generation-final','generation-intermediate']:
 (A/folder).mkdir(exist_ok=True)
for name in ['build_content_mapping.py','test_content_mapping.py']:
 shutil.copyfile(H/name,A/'after'/name)
shutil.copytree(g,A/'generation-final',dirs_exist_ok=True)
oldg=R/(A/'generation-path.txt').read_text()
shutil.copytree(oldg,A/'generation-intermediate',dirs_exist_ok=True)
watch=R/'reviews/codex-supervision/2026-10-04-live-watch/latest.json'
x=json.loads(watch.read_bytes())
(A/'observer-summary.json').write_bytes(enc({k:x.get(k) for k in ['time','head','child_jobs','core_drift']})+b'\n')
print(json.dumps({'records':records,'characters':totalchars,'live_bound_files':len(live),'B5_reused_artifacts':len(manifest['artifacts'])}))
