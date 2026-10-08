"""Preserve every current input byte before restoring historical inputs."""
from pathlib import Path
import hashlib,json,copy,sys,datetime
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
P=R/'reviews/codex-supervision/2026-10-06-scene-start-supervision'
sys.path[:0]=[str(R/'tools'),str(R/'src')]
sys.stdout.reconfigure(encoding='utf-8')
from holdout_contract import Snapshot,object_sha
from draft_io import fingerprint
from publish_row_patches import sorted_sha,MATH_FIELDS
raw=lambda b:hashlib.sha256(b).hexdigest()
a=json.loads((P/'input-audit.json').read_text(encoding='utf-8'));s=Snapshot(R)
records={}
for v in a['record_bindings']:
 b=s.read(R/v['source_path']);assert raw(b)==v['source_raw_sha256']
 row=json.loads(b.decode('utf-8-sig').splitlines()[v['source_line']-1])
 assert row['id']==v['id'] and object_sha(row)==v['full_record_canonical_sha256']
 records[v['id']]=(v,row)
assert raw(s.read(R/'reviews/2026-10-05-training-diversity-drafts/draft-selection.json'))==a['selection_raw_sha256']
preserved=[];patches=[];plan=[]
for item in a['chunks']+[{'path':'reviews/2026-10-06-scene-standard-sweep/chunks/listing.json'}]:
 rel=item['path'];path=R/rel;old=s.read(P/'input-snapshot'/rel);current=s.read(path)
 if path.name!='listing.json':
  assert raw(old)==item['raw_sha256']
  before=json.loads(old);after=json.loads(current)
  assert len(before['records'])==len(after['records'])
  for b,n in zip(before['records'],after['records']):
   assert {k:v for k,v in b.items() if k!='scene_spec'}=={k:v for k,v in n.items() if k!='scene_spec'},n['id']
   if b['scene_spec']==n['scene_spec']:continue
   bind,row=records[n['id']];updated=copy.deepcopy(row);updated['scene_spec']=n['scene_spec']
   patches.append({'batch':bind['batch'],'id':n['id'],
    'expected_selected_path':bind['source_path'].split('2026-10-05-training-diversity-drafts/',1)[1],
    'expected_hash_algorithm':'sha256-utf8-sig-splitlines-lf-v1',
    'expected_selected_sha256':bind['source_normalized_sha256'],
    'expected_selected_raw_sha256':bind['source_raw_sha256'],
    'expected_record_sha256':sorted_sha(row),
    'new_math_content_sha256':sorted_sha({k:updated[k] for k in MATH_FIELDS}),
    'fields':{'scene_spec':n['scene_spec']},'semantic_review_status':'PENDING','visual_verified':False})
 plan.append({'path':rel,'original_path':(O/'original-inputs'/path.name).relative_to(R).as_posix(),
       'original_raw_sha256':raw(old),'current_raw_sha256':raw(current),'current_bytes':len(current)})
 preserved.append((path.name,old,current))
s.check_unchanged()
for dirname in ('original-inputs','current-before-restore'):(O/dirname).mkdir(exist_ok=False)
for name,old,current in preserved:
 (O/'original-inputs'/name).write_bytes(old);(O/'current-before-restore'/name).write_bytes(current)
def save(name,v):
 with (O/name).open('x',encoding='utf-8') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
save('restore-plan.json',{'schema':'preserved-input-restore-v1','files':plan,'root':str(R),'capture_at':datetime.datetime.now().astimezone().isoformat()})
save('claude-scene-candidates.captured-v1.json',{'schema':'preserved-scene-candidates-v1','status':'UNSELECTED_UNREVIEWED','records':patches})
save('capture-verification.json',{'selected_records':len(records),'selection_raw_sha256':a['selection_raw_sha256'],
  'live_chunks_changed':sum(v['current_raw_sha256']!=v['original_raw_sha256'] for v in plan),
  'scene_changes_preserved':len(patches),'math_three_fields_unchanged':True,'source_bindings':s.bindings()})
print(json.dumps({'source_records':len(records),'changed_scenes_preserved':len(patches),'files_captured':len(plan)}))
