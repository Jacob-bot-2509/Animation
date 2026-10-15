"""Archive explicit visual verdicts, coverage, corrected metric scope, and packet integrity."""
from pathlib import Path
import json,hashlib,datetime,importlib.util,sys
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'));import core_signatures as core
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def emit(name,value):
 with (O/name).open('xb')as f:f.write(core.encoded(value))
def check(x,s):
 if not x:raise ValueError(s)
run='run-d69a44a629954e66b6fb08ca36ace3b1'
A=R/'reviews/codex-supervision/2026-10-08-auto-mail';work=A/'runs'/run
packet=json.loads((work/'inbox.json').read_text('utf-8'))
check(packet==json.loads((O/'inbox-original.json').read_text('utf-8')),'Packet snapshot changed')
spec=importlib.util.spec_from_file_location('existing_mail_protocol',A/'mail_watch.py');mail=importlib.util.module_from_spec(spec);spec.loader.exec_module(mail)
check(packet['run_id']==run,'Run mismatch')
verified=[]
for m in packet['messages']:
 h=mail.message_hash(m);check(h==packet['message_hashes'][m['id']],'Canonical message changed')
 p=A/'messages'/(m['id']+'.json');check(mail.message_hash(json.loads(p.read_text('utf-8')))==h,'Original captured message changed')
 verified.append(dict(id=m['id'],message_sha256=h,captured_snapshot=p.relative_to(R).as_posix()))
emit('packet-verification.json',dict(run_id=run,status='PASS_EXACT_PACKET_AND_CAPTURED_MESSAGES',messages=verified))
rows=list(map(json.loads,(O/'DELIVERY_INDEX.jsonl').read_text('utf-8').splitlines()))
parents=list(map(json.loads,(R/'reviews/codex-supervision/2026-10-08-hd-formula-mail-review/DELIVERY_INDEX.jsonl').read_text('utf-8').splitlines()))
repaired=set(x['id']for x in map(json.loads,(O/'REPAIRED_INDEX.jsonl').read_text('utf-8').splitlines()))
oldby={x['id']:x for x in parents}
check(len(rows)==165 and len(repaired)==9,'Coverage changed')
for row in rows:
 if row['id']not in repaired:check(row==oldby[row['id']],'Unchanged inheritance changed')
queue=[];metrics=[]
for row in rows:
 for name,hs in [('geometry_path','geometry_sha256'),('formula_inventory_path','formula_inventory_sha256'),('mp4_path','mp4_sha256')]:
  check(sha(core.checked_path(R/row[name],R))==row[hs],'Bound asset changed')
 g=json.loads((R/row['geometry_path']).read_text('utf-8'))
 f=json.loads((R/row['formula_inventory_path']).read_text('utf-8'))['unique_formulas']
 for p,fr,me in zip(g['pages'],row['canonical_frames'],row['page_metrics']):
  check(sha(core.checked_path(R/fr['path'],R))==fr['sha256'],'Bound PNG changed')
  q=dict(ordinal=len(queue),id=row['id'],page=p['page'],path=fr['path'],sha256=fr['sha256'],kind=p['kind'],tile=p['tile'],tile_grid=p['tile_grid'],record_sha256=row['record_sha256'],math_sha256=row['math_sha256'],formulas=[dict(index=i['formula_index']+1,tex=f[i['formula_index']])for i in p['items']])
  queue.append(q)
  metrics.append(dict(id=row['id'],image_path=fr['path'],image_sha256=fr['sha256'],pixel_resolution=[3840,2160],**me))
check(len(queue)==633,'Missing combined pages')
verdicts=[json.loads(s)for name in ['page-glyph-verdicts.jsonl','repair-page-glyph-verdicts.jsonl']for s in (O/name).read_text('utf-8').splitlines()]
check(len(verdicts)==123,'Actual verdict count changed')
vb={(v['id'],v['sha256']):v for v in verdicts}
coverage=[]
for p in queue:
 v=vb.get((p['id'],p['sha256']))
 if v:
  for k in ['record_sha256','math_sha256','formulas','kind','tile','tile_grid']:
   check(v[k]==p[k],'Verdict formula/version mismatch')
  check(v['symbols_checked']==[x['index']for x in p['formulas']],'Incomplete symbol verdict')
  check(v['status']=='PASS','Failed candidate still selected')
 coverage.append(dict(**p,review_status='PASS_ACTUAL_IMAGE_REVIEW'if v else'NEEDS_EVIDENCE_NOT_INSPECTED',verdict_source=('repair-page-glyph-verdicts.jsonl'if p['id']in repaired else'page-glyph-verdicts.jsonl')if v else None))
passed=sum(x['review_status']=='PASS_ACTUAL_IMAGE_REVIEW'for x in coverage)
check(passed==120,'Unexpected current actual review coverage')
emit('current-page-review-queue.json',dict(index_sha256=sha(O/'DELIVERY_INDEX.jsonl'),pages=coverage))
emit('unreviewed-pages.json',dict(index_sha256=sha(O/'DELIVERY_INDEX.jsonl'),status='NEEDS_EVIDENCE',pages=[p for p in coverage if p['review_status']!='PASS_ACTUAL_IMAGE_REVIEW']))
emit('glyph-coverage-summary.json',dict(current_pages=633,current_reviewed_pass=120,current_unreviewed=513,repair_pages_reviewed_pass=45,unchanged_current_reviewed_pass=75,old_actual_verdicts=78,old_pass=77,old_fail=1,old_fail_excluded_from_current=True,old_reviewed_pages_superseded=3,full_glyph_visual_acceptance='NOT_ESTABLISHED',preview='2048x1152 actual display of SHA-bound 3840x2160 PNGs; not native-pixel minimum-size certification',no_automated_glyph_pass=True))
emit('corrected-readable-verification.json',dict(author_report_original='author-verification-original.json',author_report_sha256=sha(O/'author-verification-original.json'),index='DELIVERY_INDEX.jsonl',index_sha256=sha(O/'DELIVERY_INDEX.jsonl'),parent_manifest_sha256='12d50e59e50ee53c219be17d080c83a615523c7305ae5c659bec3b7fbacf902b',records=165,pages=633,metrics=metrics,method='Frozen audit_hd.py formula-only inclusive occupied bbox: native PNG zero-based region rows 271:1889 and columns 136:3704, threshold any RGB channel >32. Exact bbox height divided by displayed item count; 1080p proxy equals one half for native 2160p. This includes layout and is NOT minimum glyph height or an all-symbol visual certificate.',minimum_slot_proxy_at_1080p_exact='46',minimum_glyph_size='NOT_CERTIFIED',full_glyph_visual_acceptance='NOT_ESTABLISHED',qualification='PASS_BOUND_SOURCE_LAYOUT_PAGE_PIXELS_ONLY'))
latest=R/'reviews/codex-supervision/2026-10-04-live-watch/latest.json'
emit('observer-after.json',json.loads(latest.read_text('utf-8')))
emit('final-active-hashes.json',dict(files=[dict(path=str(p.relative_to(R).as_posix()),sha256=sha(p),bytes=p.stat().st_size)for p in [R/'tools/hd_formula_pages.py',R/'tests/test_hd_formula_pages.py',R/'tools/readable_formula_pages.py',R/'tools/native_render_pilot.py',R/'tools/core_signatures.py']],checked_at=datetime.datetime.now().astimezone().isoformat()))
print(json.dumps(dict(pages=633,reviewed=passed,unreviewed=633-passed,index_sha256=sha(O/'DELIVERY_INDEX.jsonl'),packet='PASS')))
