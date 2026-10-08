from pathlib import Path
from datetime import datetime,timezone,timedelta
import json,sys,copy
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'));import core_signatures as c
def j(p):return json.loads(p.read_text('utf-8'))
def sha(p):return c.digest(p.read_bytes())
def save(n,v):
 with(O/n).open('xb')as f:f.write(c.encoded(v))
now=datetime.now(timezone(timedelta(hours=8))).isoformat()
v=j(O/'final-independent-verification.json')
readmep=R/'reviews/2026-10-08-visual-acceptance/README.md'
statusp=R/'reviews/codex-supervision/2026-10-07-continuous-math-review/CURRENT_STATUS.json'
oldreadme=(O/'visual-readme-before.md').read_bytes()
assert statusp.read_bytes()==(O/'current-status-before.json').read_bytes()
assert readmep.read_bytes()==(O/'readme-header-content.md').read_bytes()+oldreadme[oldreadme.index(b'---'):]
s=j(O/'current-status-before.json');base=O.relative_to(R).as_posix();relative='../'+O.name
s.setdefault('previous_glyph_continuation_history',[]).append(copy.deepcopy(s['latest_glyph_continuation']))
s.setdefault('previous_visual_review_history',[]).append(copy.deepcopy(s['latest_visual_followup']))
s.setdefault('previous_core_source_and_signature_binding_history',[]).append({k:copy.deepcopy(s.get(k))for k in ('authoritative_sources','record_versions','signatures','record_bindings_sha256','signature_sha256','source_bindings_sha256','current_core_overrides','qualification','verification','math_and_scene_text','signature_fidelity')})
follow={'project_path':base,'report':base+'/FIX_REPORT.md','report_sha256':sha(O/'FIX_REPORT.md'),'reviewed_at':now,'task_source':'USER_CONTINUE_REPAIR','delivery_index':v['current_index_path'],'delivery_index_sha256':v['current_index_sha256'],'qualified_record_count':165,'qualified_pages':633,'manual_image_review_pages':296,'unreviewed_current_pages':337,'page_review_evidence':base+'/effective-page-review-queue.json','unreviewed_page_list':base+'/current-unreviewed-pages.json','qualification':'REPAIRED_PASS_LOCAL_TWO_RECORDS_EIGHT_PROOFS_AND_32_PAGES','full_glyph_visual_acceptance':'NOT_ESTABLISHED','native_minimum_glyph_height_certification':'NOT_CERTIFIED','conceptual_animation':'NOT_EVALUATED','semantic_isolation':'NOT_ESTABLISHED','production':'CLOSED','archive_integrity':'PENDING_FINAL_FREEZE','bridge_reply_id':None}
s['latest_visual_followup']=follow
s['latest_glyph_continuation']={**follow,'new_actual_pages':32,'actual_images_viewed':37,'total_current_reviewed_pages':296,'pending_pages':337,'current_queue':base+'/effective-page-review-queue.json','bound_current_index_sha256':v['current_index_sha256'],'readme_sha256':sha(readmep),'minimum_glyph_height':'NOT_CERTIFIED'}
s.update(updated_at=now,current_sources=24,authoritative_sources=relative+'/current-source-bindings.json',record_versions=relative+'/current-record-bindings.jsonl',signatures=relative+'/current-complete-signatures.jsonl',record_bindings_sha256=sha(O/'current-record-bindings.jsonl'),source_bindings_sha256=sha(O/'current-source-bindings.json'),signature_sha256=sha(O/'current-complete-signatures.jsonl'),qualification=relative+'/QUALIFICATION.json',verification=relative+'/final-independent-verification.json',signature_version_binding='PASS_ALL_761_CURRENT_RECORD_VERSION_BINDINGS',signature_fidelity='CURRENT_DESCRIPTORS_UNCHANGED; TWO_RECORD_VERSION_BINDINGS_REBOUND',math_and_scene_text='PASS_LOCAL_TWO_REPAIRS_PLUS_INHERITED_759; 8_CURRENT_BATCH_COMPLETE_PROOFS_REVIEWED',current_core_overrides={'version_binding':base+'/final-version-binding.json','changed_ids_this_batch':v['changed_ids'],'changed_ids_from_frozen_parent':['eval-calc-030-s3','eval-geom-007-s1','eval-geom-007-s2','eval-linalg-002-s3','eval-linalg-004-s3'],'registered_physical_sources':24,'frozen_base_sources':24,'current_eval_consolidated_source_records':300,'selected_current_records':761,'policy':'Current record bindings select all current records; complete eval candidate replaces the old eval source selection; intermediate copies are not extra records.'})
s['typesetting'].update(current_delivery_index=v['current_index_path'],historical_qualified_records_superseded_by_current_index=True,host_complete_formula_compilation='PASS_CURRENT_165_FORMULA_INVENTORIES_AND_BOUND_LAYOUT; ORIGINAL_COUNT_METADATA_IS_HISTORICAL',current_formula_items=sum(x['unique_formulas']for x in map(json.loads,(O/'CURRENT_DELIVERY_INDEX.jsonl').read_text('utf-8').splitlines())),current_source_occurrences=sum(x['source_formula_occurrences']for x in map(json.loads,(O/'CURRENT_DELIVERY_INDEX.jsonl').read_text('utf-8').splitlines())))
s['current_quantitative_full_page_proxy']={**j(O/'current-slot-proxy-summary.json'),'evidence':base+'/current-slot-proxy-summary.json','current_index_sha256':v['current_index_sha256']}
assert s['PASS_CORE_SCOPE_issued']is False and s['production']=='CLOSED'
statusp.write_bytes(c.encoded(s))
save('active-pointer-update.json',{'at':now,'readme_path':readmep.relative_to(R).as_posix(),'readme_before_sha256':c.digest(oldreadme),'readme_after_sha256':sha(readmep),'history_tail_identical':readmep.read_bytes().split(b'---',1)[1]==oldreadme.split(b'---',1)[1],'status_path':statusp.relative_to(R).as_posix(),'status_before_sha256':sha(O/'current-status-before.json'),'status_after_sha256':sha(statusp),'concurrency_checks':'PASS_BYTES_IDENTICAL_TO_CAPTURED_BEFORE_UPDATE','readme_encoding_fix':'PASS_CHINESE_UTF8_CURRENT_HEADER; HISTORY_TAIL_UNCHANGED'})
latest=R/'reviews/codex-supervision/2026-10-04-live-watch/latest.json'
if latest.exists():
 raw=latest.read_bytes();save('observer-read-only-followup.json',{'read_at':now,'source_path':latest.relative_to(R).as_posix(),'source_sha256':c.digest(raw),'source_snapshot':json.loads(raw),'qualification':'SOURCE_HEARTBEAT_SNAPSHOT_ONLY; NO_ASSERTION_OF_CURRENT_EXPERIMENT_OR_LIVE_PROGRESS','read_only':True,'no_restart':True})
print(json.dumps({'status':'PASS_LOCAL_QUALIFICATION_AND_ACTIVE_POINTER_UPDATE','report_sha256':sha(O/'FIX_REPORT.md'),'readme_sha256':sha(readmep),'status_sha256':sha(statusp),'index_sha256':v['current_index_sha256']}))
