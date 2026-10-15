from pathlib import Path
import json,sys,copy
from datetime import datetime,timezone,timedelta
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'));import core_signatures as c
def sha(p):return c.digest(p.read_bytes())
def read(p):return json.loads(p.read_text('utf-8'))
def rel(p):return p.relative_to(R).as_posix()
def save(p,v):p.write_bytes(c.encoded(v))
status=R/'reviews/codex-supervision/2026-10-07-continuous-math-review/CURRENT_STATUS.json'
readme=R/'reviews/2026-10-08-visual-acceptance/README.md'
assert sha(status)=='4d70732f9847163aa56dacddb92b4bae4471fc89b88fd5febf46db792523644d'
assert sha(readme)=='bed34222c6bad8b24ea5374eae57b6fc9fee0744cff6aec3488394dce8d0d646'
v=read(O/'final-independent-verification.json');s=read(status);now=datetime.now(timezone(timedelta(hours=8))).isoformat()
fields=['authoritative_sources','record_versions','signatures','record_bindings_sha256','signature_sha256','source_bindings_sha256','current_core_overrides','math_and_scene_text','signature_fidelity','signature_version_binding']
s.setdefault('previous_core_source_and_signature_binding_history',[]).append({k:copy.deepcopy(s[k])for k in fields if k in s})
for key,hist in [('latest_visual_followup','previous_visual_review_history'),('latest_glyph_continuation','previous_glyph_continuation_history')]:
 if key in s:s.setdefault(hist,[]).append(copy.deepcopy(s[key]))
s.update({'authoritative_sources':'../2026-10-08-complete-glyph-review/current-source-bindings.json','record_versions':'../2026-10-08-complete-glyph-review/current-record-bindings.jsonl','signatures':'../2026-10-08-complete-glyph-review/current-complete-signatures.jsonl','source_bindings_sha256':v['source_bindings_sha256'],'record_bindings_sha256':v['record_bindings_sha256'],'signature_sha256':v['signature_sha256'],'signature_version_binding':'PASS_ALL_761_CURRENT_RECORD_VERSION_BINDINGS','signature_fidelity':'PASS_LOCAL_THREE_DESCRIPTOR_REPAIRS_PLUS_INHERITED_DESCRIPTORS','math_and_scene_text':'PASS_LOCAL_98_COMPLETE_PROOFS_AND_23_REPAIRS_PLUS_UNCHANGED_PARENT_RECORDS','full_glyph_visual_acceptance':'PASS_LOCAL_CURRENT_165_BOUND_RECORDS_ALL_638_FORMULA_PAGES','native_minimum_glyph_height_certification':'NOT_CERTIFIED'})
s['current_core_overrides']={'project_path':rel(O),'version_binding':rel(O/'final-independent-verification.json'),'selected_current_records':761,'registered_physical_sources':24,'changed_this_round':23,'prior_five_repairs_preserved':True,'policy':'Only current-record-bindings selects records. Candidate copies are not additional records. Frozen base remains historical; current source list is authoritative.'}
entry={'project_path':rel(O),'report':rel(O/'FIX_REPORT.md'),'report_sha256':sha(O/'FIX_REPORT.md'),'reviewed_at':now,'task_source':'USER_CONTINUE_UNTIL_ALL_SCOPED_REPAIRS_COMPLETE','delivery_index':rel(O/'CURRENT_DELIVERY_INDEX.jsonl'),'delivery_index_sha256':v['index_sha256'],'qualified_record_count':165,'qualified_pages':638,'manual_image_review_pages':638,'unreviewed_current_pages':0,'new_actual_pages':75,'original_pending_pages_actually_viewed':337,'current_batch_complete_proofs':98,'exact_symbolic_checks':96,'page_review_evidence':rel(O/'effective-page-review-queue.json'),'unreviewed_page_list':rel(O/'current-unreviewed-pages.json'),'qualification':rel(O/'QUALIFICATION.json'),'full_glyph_visual_acceptance':s['full_glyph_visual_acceptance'],'minimum_glyph_height':'NOT_CERTIFIED','conceptual_animation':'NOT_EVALUATED','semantic_isolation':'NOT_ESTABLISHED','native_sandbox':'UNVERIFIED','production':'CLOSED','archive_integrity':'AWAITING_FINAL_FREEZE'}
s['latest_visual_followup']=copy.deepcopy(entry);s['latest_glyph_continuation']=copy.deepcopy(entry)
assert s['production']=='CLOSED' and not s['PASS_CORE_SCOPE_issued'] and s['semantic_isolation']=='NOT_ESTABLISHED'
tail=readme.read_bytes().split(b'---',1)[1];before_tail=c.digest(tail)
header='# 当前公式页审阅交付\n\n当前修复归档：[FIX_REPORT.md](../codex-supervision/2026-10-08-complete-glyph-review/FIX_REPORT.md)。\n\n165 条当前交付记录、638 页全部完成实际图片审阅，待审 0 页。本轮复核 98 条完整数学记录，修复 23 条记录和 3 条签名描述；96 项精确符号检查通过。19 道重新原生渲染的 75 页全部逐页复审，视频起始帧与 PNG 逐像素一致。\n\n当前来源：[current-source-bindings.json](../codex-supervision/2026-10-08-complete-glyph-review/current-source-bindings.json)；交付索引：[CURRENT_DELIVERY_INDEX.jsonl](../codex-supervision/2026-10-08-complete-glyph-review/CURRENT_DELIVERY_INDEX.jsonl)；资格结论：[QUALIFICATION.json](../codex-supervision/2026-10-08-complete-glyph-review/QUALIFICATION.json)。\n\n仅认定当前绑定公式页的本地审阅合格。最小字形高度未认证，概念动画未验收，整体语义隔离未建立，原生沙箱未核实，生产关闭；双端实验按用户要求不在本轮范围。\n\n'
readme.write_bytes(header.encode('utf-8')+b'---'+tail)
assert c.digest(readme.read_bytes().split(b'---',1)[1])==before_tail
save(status,s)
save(O/'active-pointer-update.json',{'status':'PASS_CURRENT_POINTERS_UPDATED','updated_at':now,'current_status_before_sha256':sha(O/'current-status-before.json'),'current_status_after_sha256':sha(status),'readme_before_sha256':sha(O/'visual-readme-before.md'),'readme_after_sha256':sha(readme),'historical_readme_tail_preserved_exact':True,'historical_tail_sha256':before_tail,'parent_archive_unchanged':True})
(O/'current-status-after-pre-freeze.json').write_bytes(status.read_bytes());(O/'visual-readme-after.md').write_bytes(readme.read_bytes())
print(json.dumps({'status':'PASS','pages':638,'pending':0,'readme_sha256':sha(readme)}))
