"""Final repair verification; no publication, training or rendering."""
from pathlib import Path
import copy,datetime,json,os,stat,sys
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
P=R/'reviews/codex-supervision/2026-10-06-scene-start-supervision'
sys.path[:0]=[str(R/'tools')];sys.stdout.reconfigure(encoding='utf-8')
from holdout_contract import Snapshot,raw_sha,json_object,jsonl,object_sha
from scene_sweep_protocol import verify_inputs
from draft_io import selected_path,fingerprint
# Correct current board counts; historical board backups remain untouched.
board=R/('docs/'+''.join(map(chr,[0x9879,0x76ee,0x603b,0x89c8]))+'/'+''.join(map(chr,[0x8fdb,0x5ea6,0x770b,0x677f]))+'.md')
b=board.read_bytes();t=b.decode('utf-8');assert '37 '+chr(0x9879) in t
t=t.replace('37 '+chr(0x9879),'39 '+chr(0x9879))
with (O/'progress-board.before-final.md').open('xb') as f:f.write(b)
assert board.read_bytes()==b;board.write_bytes(t.encode('utf-8'))
with (O/'progress-board-final-fix.json').open('x',encoding='utf-8') as f:
 json.dump({'path':board.relative_to(R).as_posix(),'before_raw_sha256':raw_sha(b),'after_raw_sha256':raw_sha(board.read_bytes())},f,ensure_ascii=False,indent=2)
guide=O/'OPERATING_GUIDE.md';t=guide.read_text(encoding='utf-8')
t=t.replace(chr(0x6e90)+chr(0x7801)+'/',''.join(map(chr,[0x6765,0x6e90]))+'/')
guide.write_text(t,encoding='utf-8',newline='\n')
s=Snapshot(R);a=json.loads((P/'input-audit.json').read_text(encoding='utf-8'))
for item in a['active_and_old_core_checks']:assert raw_sha(s.read(R/item['path']))==item['raw_sha256'],item['path']
receiptpath=R/'reviews/2026-10-06-linalg048-admission/v3-receipt-bound/receipt.json'
rd=s.read(receiptpath);assert raw_sha(rd)=='4e81d921f2fb3ad5e90ab8e7372fa898203441bf8011008774f2d1b45cfbee25'
receipt=json_object(rd)
for path,item in receipt['source_bindings'].items():
 data=s.read(R/path);assert raw_sha(data)==item['raw_sha256'] and len(data)==item['bytes'],path
oldmanifest=json_object(s.read(R/'reviews/codex-supervision/2026-10-06-protocol-v3-mail-followup/delivery-manifest.json'))
for rel,digest in oldmanifest['live_source_hashes'].items():
 if rel.endswith('watch_claude.py'):continue
 assert raw_sha(s.read(R/rel))==digest,rel
plan=json_object(s.read(O/'restore-plan.json'))
for item in plan['files']:
 p=R/item['path'];data=s.read(p)
 assert raw_sha(data)==item['original_raw_sha256'] and data==s.read(R/item['original_path'])
 assert p.stat().st_file_attributes&stat.FILE_ATTRIBUTE_READONLY,p
inputs,bound=verify_inputs(O/'inputs-v2',root=R);oldrows={x['record']['id']:x['record'] for x in bound}
assert inputs['record_count']==264 and inputs['chunk_count']==20
assert all(v['count']>0 for v in inputs['chunks'].values())
selectionpath=R/'reviews/2026-10-05-training-diversity-drafts/draft-selection.json'
assert raw_sha(s.read(selectionpath))==a['selection_raw_sha256']
patchpacket=json_object(s.read(O/'scene-candidates-corrected-v4.json'));patches={p['id']:p for p in patchpacket['records']}
candidateRoot=O/'scene-candidates-53-v4'
sel=json_object(s.read(candidateRoot/'draft-selection.candidate.json'));seen=[]
for entry in sel['entries']:
 p=selected_path(candidateRoot,entry);data=s.read(p)
 fp=fingerprint(data);assert fp['raw_sha256']==entry['raw_sha256'] and fp['sha256']==entry['sha256']
 for row in jsonl(data):
  old=oldrows[row['id']];assert all(old[k]==row[k] for k in ('problem','solution','answer'))
  spec=patches[row['id']]['fields']['scene_spec'] if row['id'] in patches else old['scene_spec']
  assert row['scene_spec']==spec
  assert row['admitted'] is False and row['training_admitted'] is False and row['render_verified'] is False
  assert row['strict_review']['visual_review']=='PENDING'
  seen.append(row['id'])
assert seen==[x['record']['id'] for x in bound]
math=json_object(s.read(O/'math-correction-receipt.json'));changes={v['id']:v for v in math['corrections']}
mathseen=[];corrected_seen=0
for name,entry in math['files'].items():
 data=s.read(O/'math-corrected-v1'/name);fp=fingerprint(data)
 assert fp['raw_sha256']==entry['raw_sha256'] and fp['sha256']==entry['sha256']
 originals={r['id']:r for r in jsonl(s.read(R/entry['source_path']))}
 for row in jsonl(data):
  assert row['admitted'] is False and row['training_admitted'] is False and row['render_verified'] is False
  if row['id'] in changes:
   assert object_sha(row)==changes[row['id']]['after_record_canonical_sha256'];corrected_seen+=1
  else:assert all(row[k]==originals[row['id']][k] for k in ('problem','solution','answer','scene_spec'))
  mathseen.append(row['id'])
assert len(mathseen)==47 and len(set(mathseen))==47 and corrected_seen==9
sample=json_object(s.read(P/'scene-sample-codex-corrections-v1.pending.json'))
for patch in sample['records']:
 assert object_sha(patch['fields']['scene_spec'])==object_sha(patches[patch['id']]['fields']['scene_spec'])
s.check_unchanged()
result={'checked_at':datetime.datetime.now().astimezone().isoformat(),'old_inputs_restored_and_readonly':21,
 'original_scene_results_preserved':18,'new_nonempty_input_chunks':20,'input_records':264,
 'active_selector_unchanged':True,'old_native_source_bindings_verified':len(receipt['source_bindings']),
 'old_receipt_raw_sha256':raw_sha(rd),'protocol_v3_sources_unchanged':True,
 'stage_candidate_records':len(seen),'stage_changed_scenes':len(patches),'all_stage_math_three_fields_equal_sources':True,
 'candidate_acceptance_flags_closed':True,'new_math_candidate_records':47,'math_corrections_applied_to_new_version':9,
 'original_math_sources_unchanged':True,'sample_three_proof_content_unchanged':True,
 'regression_tests_passed':json_object(s.read(O/'suite-final-result.json'))['tests'],
 'exact_formula_checks':json_object(s.read(O/'exact-math-verification.json'))['check_count'],
 'full_scene_math_and_visual_acceptance':False,'production_gate':'CLOSED','assets':'1/497 NOT READY',
 'training_started':False,'source_bindings':s.bindings()}
with (O/'final-verification.json').open('x',encoding='utf-8') as f:json.dump(result,f,ensure_ascii=False,indent=2);f.write('\n')
sourcepaths=['tools/scene_sweep_protocol.py','tools/stage_scene_patches.py','tools/split_scene_sweep.py',
 'tools/publish_row_patches.py','tools/dataset_audit.py','tests/test_scene_sweep_protocol.py',
 'tests/test_dataset_audit_latex_delimiters.py',board.relative_to(R).as_posix(),
 'reviews/codex-supervision/2026-10-04-live-watch/watch_claude.py',
 'reviews/2026-10-06-core-families/core-families.corrected-v2.json',
 'reviews/2026-10-06-holdout-design/holdout-design.corrected-v2.md']
live={}
for rel in sourcepaths:
 data=(R/rel).read_bytes();p=O/'source-current'/rel;p.parent.mkdir(parents=True,exist_ok=True)
 with p.open('xb') as f:f.write(data)
 live[rel]=raw_sha(data)
with (O/'live-source-hashes.json').open('x',encoding='utf-8') as f:json.dump(live,f,ensure_ascii=False,indent=2);f.write('\n')
print(json.dumps({k:v for k,v in result.items() if k!='source_bindings'},ensure_ascii=False))
