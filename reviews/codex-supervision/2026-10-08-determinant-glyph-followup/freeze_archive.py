from pathlib import Path
from datetime import datetime,timezone,timedelta
import json,sys,hashlib
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'));import core_signatures as c
def j(p):return json.loads(p.read_text('utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
actual=json.loads(j(O/'bridge-final-reply.json')['content'][0]['text'])
assert actual['status']=='sent'and actual['message']['id']=='msg_1791438252391_751'
assert actual['message']['from']=='codex'and actual['message']['to']=='claude-code'
assert actual['message']['metadata']['report_sha256']==sha(O/'FIX_REPORT.md')
v=j(O/'final-delivery-validation.json')
statusp=R/'reviews/codex-supervision/2026-10-07-continuous-math-review/CURRENT_STATUS.json'
assert sha(statusp)==v['current_status_sha256_at_validation']
s=j(statusp);now=datetime.now(timezone(timedelta(hours=8))).isoformat()
mp=O/'delivery-manifest.json';assert not mp.exists()
artifacts=[]
for p in sorted(O.rglob('*')):
 if p.is_file():
  p=c.checked_path(p,O)
  artifacts.append({'path':p.relative_to(O).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size})
manifest={'schema':'codex-frozen-local-review-manifest-v1','created_at':now,'scope':'TWO_REPAIRED_RECORDS_EIGHT_COMPLETE_PROOFS_32_CURRENT_PAGES','status':'PASS_LOCAL_REVIEW_FROZEN_ARTIFACTS','qualification':'QUALIFICATION.json','report':'FIX_REPORT.md','actual_bridge_reply_id':actual['message']['id'],'self_manifest_excluded':True,'artifacts':artifacts,'production':'CLOSED'}
mp.open('xb').write(c.encoded(manifest))
for a in artifacts:
 p=c.checked_path(O/a['path'],O);assert sha(p)==a['sha256']and p.stat().st_size==a['bytes']
assert {p.relative_to(O).as_posix()for p in O.rglob('*')if p.is_file()}=={a['path']for a in artifacts}|{'delivery-manifest.json'}
for k in ('latest_glyph_continuation','latest_visual_followup'):
 s[k].update(archive_integrity='PASS',manifest_sha256=sha(mp),archive_artifacts=len(artifacts),bridge_reply_id=actual['message']['id'],archive_verified_at=now)
s['updated_at']=now
assert s['PASS_CORE_SCOPE_issued']is False and s['production']=='CLOSED'
statusp.write_bytes(c.encoded(s))
print(json.dumps({'status':'PASS_FROZEN_ARCHIVE_AND_ACTUAL_CLAUDE_REPLY','artifacts':len(artifacts),'manifest_sha256':sha(mp),'report_sha256':sha(O/'FIX_REPORT.md'),'bridge_reply_id':actual['message']['id'],'current_status_sha256':sha(statusp),'current_pass_pages':296,'pending_pages':337}))
