"""Read-only candidate reconstruction, coverage, prior revisions and archive verification."""
from pathlib import Path
import json,hashlib,re,subprocess,sys
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[3]
def sha(b):return hashlib.sha256(b).hexdigest()
def canon(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def rows(p):return [json.loads(s) for s in p.read_text(encoding='utf-8-sig').splitlines() if s.strip()]
binding=json.loads((OUT/'eval-candidate-source-bindings.json').read_text(encoding='utf-8'))
source=binding['source_path']
orig=(OUT/'original-submission'/source).read_bytes();parent=(OUT/'parent-candidate'/source).read_bytes();candidate=(OUT/'candidate-sources'/source).read_bytes()
assert sha(orig)==binding['source_raw_sha256']
assert sha(parent)==binding['parent_raw_sha256']
assert sha(candidate)==binding['raw_sha256'] and len(candidate)==binding['bytes']
assert (ROOT/source).read_bytes()==orig and (ROOT/binding['parent_candidate_path']).read_bytes()==parent
before=parent.splitlines(keepends=True);after=candidate.splitlines(keepends=True)
assert len(before)==len(after)==300
specs=json.loads((OUT/'eval-correction-specs.json').read_text(encoding='utf-8'))
patches={r['id']:r for r in rows(OUT/'eval-corrections.jsonl')}
reviews={r['id']:r for r in rows(OUT/'independent-eval-review-291.jsonl')}
assert len(specs)==len(patches)==78 and len(reviews)==291
origrecords={r['id']:r for r in rows(OUT/'original-submission'/source)}
current={r['id']:r for r in rows(OUT/'candidate-sources'/source)}
changed=[];preserved=[]
for pos,(b,a) in enumerate(zip(before,after),1):
 old=json.loads(b);r=json.loads(a);rid=old['id']
 assert r['id']==rid
 if rid not in specs:
  assert a==b
 else:
  assert b!=a;changed.append(pos);patch=patches[rid]
  assert sha(canon(old))==patch['before_record_sha256']
  assert sha(canon(r))==patch['after_record_sha256']
  assert r==patch['corrected_record']
  expected=dict(old)
  expected.update(specs[rid]['fields'])
  expected.update({k:patch['after_fields'][k] for k in ('revision_lineage','versioned_id','strict_review')})
  assert expected==r
  h=sha(json.dumps({k:r[k] for k in ('problem','solution','answer','scene_spec')},ensure_ascii=False,sort_keys=True).encode())
  assert h==r['strict_review']['math_content_sha256']
  assert r['strict_review']['admitted'] is False and r['strict_review']['render_verified'] is False
  assert r['efficiency_tags']==r['scene_spec']['objects']
 if rid in reviews:
  ref=reviews[rid]['source']
  assert ref['source_path']==source and ref['source_line']==pos
  assert ref['source_raw_sha256']==sha(orig)
  assert ref['record_version_sha256']==sha(canon(origrecords[rid]))
  assert reviews[rid]['candidate_record_sha256']==sha(canon(r))
  assert reviews[rid]['post_repair_math']==reviews[rid]['post_repair_scene_text']=='PASS'
  for field in ('problem','solution','answer','scene_spec','efficiency_tags'):
   assert not re.search(r'(?<!\d)\d+\.\d+',str(r[field])),(rid,field)
 else:
  assert a==b;preserved.append(rid)
assert changed==binding['changed_lines'] and preserved==binding['previous_9_preserved'] and len(preserved)==9
w=json.loads((OUT/'eval-exact-witnesses.json').read_text(encoding='utf-8-sig'))
assert w['verdict']=='PASS' and w['candidate_sha256']==sha(candidate)
assert w['review_file_sha256']==sha((OUT/'independent-eval-review-291.jsonl').read_bytes())
for test in w['witnesses']:
 assert test['verdict']=='PASS'
 for row in test['candidate_bindings']:assert row['sha256']==sha(canon(current[row['id']]))
# Fresh exact replay; compare full result, not a mere previously authored PASS.
result=subprocess.run([sys.executable,'-B',str(OUT/'verify_eval_math.py')],check=True,capture_output=True,text=True,encoding='utf-8')
assert json.loads(result.stdout)==w
archive_count=0
manifest=OUT/'eval-delivery-manifest.json'
if manifest.exists():
 m=json.loads(manifest.read_text(encoding='utf-8'))
 for item in m['artifacts']:
  p=OUT/item['path'];data=p.read_bytes()
  assert len(data)==item['bytes'] and sha(data)==item['sha256'],item['path']
 archive_count=len(m['artifacts'])
print(json.dumps({'verdict':'PASS','independent_reviews':291,'repaired_records':78,'candidate_records':300,
 'unmodified_parent_lines':222,'prior_revised_records_preserved':9,'exact_checks_replayed':w['checks'],
 'records_with_exact_witness':w['records_with_witness'],'archived_artifacts_verified':archive_count,
 'semantic_isolation':'NOT_ESTABLISHED','native_render':'UNVERIFIED','production':'CLOSED'},indent=2))
