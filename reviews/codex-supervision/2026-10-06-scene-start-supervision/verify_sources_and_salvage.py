"""Final source verification and immutable preservation of currently changed scenes."""
from pathlib import Path
import hashlib,json,sys,copy,datetime
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sys.path[:0]=[str(R/'tools'),str(R/'src')]
sys.stdout.reconfigure(encoding='utf-8')
from holdout_contract import Snapshot,object_sha
from draft_io import fingerprint
from publish_row_patches import sorted_sha,MATH_FIELDS
raw=lambda b:hashlib.sha256(b).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
audit=read(O/'input-audit.json')
s=Snapshot(R)
active=[]
for item in audit['active_and_old_core_checks']:
 digest=raw(s.read(R/item['path']))
 assert digest==item['raw_sha256'],item['path']
 active.append({'path':item['path'],'raw_sha256':digest,'unchanged':True})
receiptpath=R/'reviews/2026-10-06-linalg048-admission/v3-receipt-bound/receipt.json'
receiptdata=s.read(receiptpath);receipt=json.loads(receiptdata)
assert raw(receiptdata)=='4e81d921f2fb3ad5e90ab8e7372fa898203441bf8011008774f2d1b45cfbee25'
for path,item in receipt['source_bindings'].items():
 b=s.read(R/path);assert raw(b)==item['raw_sha256'] and len(b)==item['bytes'],path
for path,digest in read(R/'reviews/codex-supervision/2026-10-06-protocol-v3-mail-followup/delivery-manifest.json')['live_source_hashes'].items():
 if path.endswith('watch_claude.py'):continue
 assert raw(s.read(R/path))==digest,path
assert raw(s.read(R/'reviews/2026-10-05-training-diversity-drafts/draft-selection.json'))==audit['selection_raw_sha256']
selected={}
for item in audit['record_bindings']:
 path=R/item['source_path'];data=s.read(path)
 assert raw(data)==item['source_raw_sha256']
 assert fingerprint(data)['sha256']==item['source_normalized_sha256']
 row=json.loads(data.decode('utf-8-sig').splitlines()[item['source_line']-1])
 assert object_sha(row)==item['full_record_canonical_sha256']
 selected[item['id']]=(item,row)
arch=read(O/'chunks-listing-archived-v3.json')
for path,item in arch['archived_source_bindings'].items():
 b=s.read(R/path);assert raw(b)==item['raw_sha256'] and len(b)==item['bytes'],path
changes=[];patches=[];changed_bytes={}
for item in audit['chunks']:
 path=R/item['path'];b=s.read(path)
 original=s.read(O/'input-snapshot'/item['path']);assert raw(original)==item['raw_sha256']
 old=json.loads(original);current=json.loads(b)
 assert list(old.keys())==list(current.keys())
 assert len(old['records'])==len(current['records'])
 diffs=[]
 for before,after in zip(old['records'],current['records']):
  assert {k:v for k,v in before.items() if k!='scene_spec'}=={k:v for k,v in after.items() if k!='scene_spec'},after['id']
  if before['scene_spec']==after['scene_spec']:continue
  pid=after['id'];bind,row=selected[pid];dif=copy.deepcopy(row);dif['scene_spec']=after['scene_spec']
  assert all(row[k]==after[k] for k in ('problem','solution','answer'))
  batch=bind['batch']
  patches.append({'batch':batch,'id':pid,
   'expected_selected_path':bind['source_path'].split('2026-10-05-training-diversity-drafts/',1)[1],
   'expected_hash_algorithm':'sha256-utf8-sig-splitlines-lf-v1',
   'expected_selected_sha256':bind['source_normalized_sha256'],
   'expected_selected_raw_sha256':bind['source_raw_sha256'],
   'expected_record_sha256':sorted_sha(row),
   'new_math_content_sha256':sorted_sha({k:dif[k] for k in MATH_FIELDS}),
   'fields':{'scene_spec':after['scene_spec']},
   'before_scene_canonical_sha256':object_sha(before['scene_spec']),
   'after_scene_canonical_sha256':object_sha(after['scene_spec']),
   'math_three_fields_unchanged':True,'semantic_review_status':'PENDING','visual_verified':False})
  diffs.append(pid)
 if raw(b)!=raw(original):
  changed_bytes[path.name]=b;changes.append({'path':item['path'],'original_raw_sha256':raw(original),
          'current_raw_sha256':raw(b),'changed_scene_ids':diffs})
for p in read(O/'scene-sample-codex-corrections-v1.pending.json')['records']:
 bind,row=selected[p['id']]
 assert set(p['fields'])=={'scene_spec'} and sorted_sha(row)==p['expected_record_sha256']
 after=copy.deepcopy(row);after.update(p['fields'])
 assert sorted_sha({k:after[k] for k in MATH_FIELDS})==p['new_math_content_sha256']
 assert all(after[k]==row[k] for k in ('problem','solution','answer'))
 assert object_sha(after['scene_spec'])==p['after_scene_canonical_sha256']
latex=read(O/'latex-guard-fix.json')
assert raw(s.read(R/latex['source']))==latex['after_raw_sha256']
board=read(O/'progress-board-fix.json')
assert raw(s.read(R/board['path']))==board['after_raw_sha256']
watchpath=R/'reviews/codex-supervision/2026-10-04-live-watch/watch_claude.py'
watchdata=s.read(watchpath)
s.check_unchanged()
sal=O/'live-scenes-salvage-v2';sal.mkdir(exist_ok=False)
for name,b in changed_bytes.items():(sal/name).write_bytes(b)
with (O/'live-scene-candidates.salvaged-v2.json').open('x',encoding='utf-8') as f:
 json.dump({'schema':'scene-salvage-patches-v2','status':'UNSELECTED_UNREVIEWED_SNAPSHOT',
           'records':patches,'override_notice':'Three reviewed correction candidates are in scene-sample-codex-corrections-v1.pending.json. Do not combine duplicate targets.'},f,ensure_ascii=False,indent=2);f.write('\n')
result={'checked_at':datetime.datetime.now().astimezone().isoformat(),'scope':'finite snapshot, not complete scene audit',
 'old_receipt_raw_sha256':raw(receiptdata),'old_receipt_source_bindings_verified':len(receipt['source_bindings']),
 'active_and_core_checks':active,'previous_v3_tools_and_test_unchanged':True,
 'selector_unchanged':True,'selected_records_verified':len(selected),'selected_batches':18,
 'archived_source_bindings_verified':len(arch['archived_source_bindings']),'archived_nonempty_chunks':len(arch['nonempty_chunks']),
 'live_changed_chunk_count':len(changes),'live_changed_scene_count':len(patches),'live_drift':changes,
 'original_live_chunks_restored':not changes,'old_listing_now_stale':bool(changes),
 'small_sample_corrections_source_bound':True,'math_three_fields_unchanged_for_all_captured_scenes':True,
 'latex_guard_live_raw_sha256':raw(s.data[R/latex['source']]),'watcher_live_raw_sha256':raw(watchdata),
 'progress_board_live_raw_sha256':board['after_raw_sha256'],
 'new_training_or_native_render':False,'publication_executed':False,
 'asset_status':'1/497 NOT READY','production_isolation':'CLOSED'}
with (O/'final-source-verification.json').open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
(O/'watch_claude.current.py').write_bytes(watchdata)
print(json.dumps({k:v for k,v in result.items() if k not in ('live_drift','active_and_core_checks')},ensure_ascii=False))
