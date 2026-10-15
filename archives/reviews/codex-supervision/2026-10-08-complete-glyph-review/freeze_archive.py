from pathlib import Path
import json,sys,hashlib
from datetime import datetime,timezone,timedelta
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'))
import core_signatures as c
def read(p):return json.loads(p.read_text('utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,v):p.write_bytes(c.encoded(v))
def path(s):return c.checked_path(s,R)
def rel(p):return p.relative_to(R).as_posix()
def lines(p):return [json.loads(z) for z in p.read_text('utf-8').splitlines() if z.strip()]
def now():return datetime.now(timezone(timedelta(hours=8))).isoformat()
P=R/'reviews/codex-supervision/2026-10-08-determinant-glyph-followup'
statuspath=R/'reviews/codex-supervision/2026-10-07-continuous-math-review/CURRENT_STATUS.json'
readmepath=R/'reviews/2026-10-08-visual-acceptance/README.md'
manifest=O/'delivery-manifest.json'
def parentcheck():
 assert sha(P/'delivery-manifest.json')=='72ca0b030a47d225add18e7d04d61feef81554038c7b5f1a3da5e382e6ecc3a3'
 pm=read(P/'delivery-manifest.json');assert len(pm['artifacts'])==136
 for a in pm['artifacts']:
  p=path(rel(P/a['path']));assert p.stat().st_size==a['bytes'] and sha(p)==a['sha256'],a['path']
 return 136
def validate():
 parentcount=parentcheck()
 qual=read(O/'QUALIFICATION.json')
 assert qual==read(O/'final-independent-verification.json')
 assert (qual['records'],qual['pages'],qual['pending_pages'])==(165,638,0)
 for fn,k in [('CURRENT_DELIVERY_INDEX.jsonl','index_sha256'),('current-record-bindings.jsonl','record_bindings_sha256'),('current-source-bindings.json','source_bindings_sha256'),('current-complete-signatures.jsonl','signature_sha256')]:
  assert sha(O/fn)==qual[k],fn
 bs=lines(O/'current-record-bindings.jsonl');bm={b['id']:b for b in bs};assert len(bs)==len(bm)==761
 ss=read(O/'current-source-bindings.json');assert len(ss)==24
 for s in ss:
  p=path(s['path']);assert sha(p)==s['sha256'] and p.stat().st_size==s['bytes']
  rs=lines(p);assert len(rs)==s['records']
  for i,q in enumerate(rs,1):
   b=bm[q['id']];assert b['path']==s['path'] and b['source_line']==i and b['source_sha256']==s['sha256']
   assert b['record_sha256']==c.dense(q) and b['math_sha256']==c.math_digest(q)
 sg=lines(O/'current-complete-signatures.jsonl');assert len(sg)==len({s['id']for s in sg})==761
 for s in sg:assert s['record_sha256']==bm[s['id']]['record_sha256'] and s['math_sha256']==bm[s['id']]['math_sha256']
 idx=lines(O/'CURRENT_DELIVERY_INDEX.jsonl');assert len(idx)==len({d['id']for d in idx})==165
 queue=read(O/'effective-page-review-queue.json');assert queue['index_sha256']==qual['index_sha256'] and queue['pending_pages']==0
 qm={(p['id'],p['page']):p for p in queue['pages']};assert len(qm)==638
 for d in idx:
  b=bm[d['id']];assert d['record_sha256']==b['record_sha256'] and d['math_sha256']==b['math_sha256']
  assert d['source_path']==b['path'] and d['source_sha256']==b['source_sha256'] and d['source_line']==b['source_line']
  assert len(d['canonical_frames'])==d['page_count']
  for key in ['mp4','geometry','formula_inventory']:assert sha(path(d[key+'_path']))==d[key+'_sha256']
  for pg,fr in zip(read(path(d['geometry_path']))['pages'],d['canonical_frames']):
   p=qm[d['id'],pg['page']];assert p['review_status']=='PASS_ACTUAL_IMAGE_REVIEW'
   assert p['path']==fr['path'] and p['sha256']==fr['sha256']==sha(path(fr['path']))
   assert p['record_sha256']==b['record_sha256'] and p['math_sha256']==b['math_sha256']
   path(p['verdict_source'])
 assert read(O/'current-unreviewed-pages.json')['count']==0
 proofs=read(O/'complete-proof-review.json');assert len(proofs)==98
 for p in proofs:
  assert p['status'] in ['PASS_LOCAL_COMPLETE_PROOF','PASS_LOCAL_COMPLETE_PROOF_AFTER_REPAIR']
  b=bm[p['id']];assert p['binding']['record_sha256']==b['record_sha256'] and p['binding']['math_sha256']==b['math_sha256']
 checks=read(O/'exact-symbolic-checks.json');assert len(checks)==96 and all(c['status']=='PASS'for c in checks)
 fresh=read(O/'actual-repair-page-notes.json');assert len(fresh)==75 and all(p['status']=='PASS_ACTUAL_IMAGE_REVIEW'for p in fresh)
 for p in fresh:
  q=qm[p['id'],p['page']];assert p['path']==q['path'] and p['sha256']==q['sha256']
 v=read(O/'native-video-pixel-verification.json');assert v['status']=='PASS' and len(v['checks'])==19 and sum(z['page_start_pixels_exact']for z in v['checks'])==75
 s=read(statuspath)
 for key in ['latest_visual_followup','latest_glyph_continuation']:
  p=s[key];assert p['project_path']==rel(O) and p['report_sha256']==sha(O/'FIX_REPORT.md') and p['delivery_index_sha256']==qual['index_sha256']
  assert p['qualified_pages']==638 and p['unreviewed_current_pages']==0
 assert s['authoritative_sources']=='../2026-10-08-complete-glyph-review/current-source-bindings.json'
 before=(O/'visual-readme-before.md').read_bytes();after=readmepath.read_bytes()
 assert before[before.index(b'---'):]==after[after.index(b'---'):]
 assert sha(readmepath)==read(O/'active-pointer-update.json')['readme_after_sha256']
 assert qual['production']=='CLOSED' and qual['PASS_CORE_SCOPE_issued'] is False
 return {'status':'PASS_FINAL_DELIVERY_BINDINGS','validated_at':now(),'parent_frozen_artifacts_checked':parentcount,'current_records':165,'current_pages':638,'pending_pages':0,'bound_source_records':761,'source_files':24,'complete_proofs':98,'exact_symbolic_checks':96,'fresh_actual_images':75,'fresh_video_page_pixel_checks':75,'historical_readme_tail_preserved_exact':True,'current_status_pre_freeze_sha256':sha(statuspath),'report_sha256':sha(O/'FIX_REPORT.md'),'index_sha256':qual['index_sha256'],'production':'CLOSED'}
def frozencheck():
 m=read(manifest)
 expected={a['path']for a in m['artifacts']}
 actual={p.relative_to(O).as_posix()for p in O.rglob('*')if p.is_file() and p!=manifest}
 assert actual==expected,{'extra':list(actual-expected),'missing':list(expected-actual)}
 for a in m['artifacts']:
  p=path(rel(O/a['path']));assert p.stat().st_size==a['bytes'] and sha(p)==a['sha256'],a['path']
 return m
mode=sys.argv[1]
if mode=='validate':
 assert not manifest.exists()
 v=validate();save(O/'final-delivery-validation.json',v);print(json.dumps(v))
elif mode=='freeze':
 assert not manifest.exists()
 v=read(O/'final-delivery-validation.json');assert sha(statuspath)==v['current_status_pre_freeze_sha256']
 reply=read(O/'bridge-final-reply.json');rid=reply['message_id'];assert rid.startswith('msg_') and reply['actual_tool_receipt']
 arts=[]
 for p in sorted(O.rglob('*')):
  if not p.is_file() or p==manifest:continue
  checked=path(rel(p));arts.append({'path':p.relative_to(O).as_posix(),'sha256':sha(checked),'bytes':checked.stat().st_size})
 m={'schema':'codex-frozen-local-review-manifest-v1','created_at':now(),'scope':'CURRENT_165_RECORDS_638_FORMULA_PAGES_AND_98_COMPLETE_MATH_PROOFS','status':'PASS_LOCAL_REVIEW_FROZEN_ARTIFACTS','qualification':'QUALIFICATION.json','report':'FIX_REPORT.md','actual_bridge_reply_id':rid,'self_manifest_excluded':True,'production':'CLOSED','artifacts':arts}
 save(manifest,m);frozencheck();parentcheck()
 assert sha(statuspath)==v['current_status_pre_freeze_sha256']
 s=read(statuspath)
 for key in ['latest_visual_followup','latest_glyph_continuation']:
  s[key].update({'archive_integrity':'PASS_FROZEN_ALL_ARTIFACT_HASHES','delivery_manifest':rel(manifest),'delivery_manifest_sha256':sha(manifest),'archive_artifacts':len(arts),'bridge_reply_id':rid,'archive_completed_at':now()})
 save(statuspath,s)
 print(json.dumps({'status':'PASS_ARCHIVE_FROZEN_AND_POINTERS_FINALIZED','artifacts':len(arts),'manifest_sha256':sha(manifest),'actual_bridge_reply_id':rid,'current_status_sha256':sha(statuspath)}))
elif mode=='verify':
 m=frozencheck();v=validate();s=read(statuspath)
 for key in ['latest_visual_followup','latest_glyph_continuation']:
  p=s[key];assert p['delivery_manifest']==rel(manifest) and p['delivery_manifest_sha256']==sha(manifest) and p['bridge_reply_id']==m['actual_bridge_reply_id']
  assert p['archive_integrity']=='PASS_FROZEN_ALL_ARTIFACT_HASHES' and p['archive_artifacts']==len(m['artifacts'])
 print(json.dumps({'status':'PASS_FRESH_PROCESS_FINAL_ARCHIVE_AND_CURRENT_BINDINGS','artifacts':len(m['artifacts']),'manifest_sha256':sha(manifest),'actual_bridge_reply_id':m['actual_bridge_reply_id'],'pages':638,'pending_pages':0,'production':'CLOSED'}))
else:raise AssertionError(mode)
