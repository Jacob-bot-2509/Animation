"""Validate the final active pointers, qualification and each inherited/current verdict."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import json,sys,hashlib
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'));import core_signatures as c
def j(p):return json.loads(p.read_text('utf-8'))
def jl(p):return list(map(json.loads,p.read_text('utf-8').splitlines()))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
bs=jl(O/'current-record-bindings.jsonl');bm={x['id']:x for x in bs};src=j(O/'current-source-bindings.json');srcmap={x['path']:x for x in src};cache={}
assert len(bs)==len(bm)==761 and len(src)==len(srcmap)==24
for s in src:
 p=c.checked_path(R/s['path'],R);assert sha(p)==s['sha256']and p.stat().st_size==s['bytes'];cache[s['path']]=jl(p);assert len(cache[s['path']])==s['records']
for b in bs:
 assert b['source_sha256']==srcmap[b['path']]['sha256']
 rec=cache[b['path']][b['source_line']-1];assert rec['id']==b['id']and c.dense(rec)==b['record_sha256']and c.math_digest(rec)==b['math_sha256']
sigs=jl(O/'current-complete-signatures.jsonl');assert len(sigs)==761
for s in sigs:assert all(s[k]==bm[s['id']][k]for k in ('record_sha256','math_sha256'))
q=j(O/'effective-page-review-queue.json');idx=O/'CURRENT_DELIVERY_INDEX.jsonl';rows=jl(idx)
assert q['index_sha256']==sha(idx)and q['index_path']==idx.relative_to(R).as_posix()
fields=('id','page','path','sha256','record_sha256','math_sha256','formulas','kind','tile','tile_grid')
queue=q['pages'];verdictcache={};count=0;passcount=0
for row in rows:
 b=bm[row['id']];assert all(row[k]==b[k]for k in ('source_sha256','record_sha256','math_sha256'))
 g=j(R/row['geometry_path']);f=j(R/row['formula_inventory_path'])['unique_formulas']
 for gp,fr in zip(g['pages'],row['canonical_frames']):
  p=queue[count];assert p['ordinal']==count and p['id']==row['id']and p['page']==gp['page']
  assert all(p[k]==fr[k]for k in ('path','sha256'))and all(p[k]==b[k]for k in ('record_sha256','math_sha256'))
  assert p['formulas']==[{'index':v['formula_index']+1,'tex':f[v['formula_index']]}for v in gp['items']]
  if p['review_status']=='PASS_ACTUAL_IMAGE_REVIEW':
   vs=p['verdict_source']
   if vs not in verdictcache:verdictcache[vs]=jl(R/vs)
   assert sum(v['status']=='PASS'and all(v[k]==p[k]for k in fields)for v in verdictcache[vs])==1;passcount+=1
  count+=1
assert len(rows)==165 and count==len(queue)==633 and passcount==296
assert j(O/'current-unreviewed-pages.json')==[p for p in queue if p['review_status']!='PASS_ACTUAL_IMAGE_REVIEW']
qual=j(O/'QUALIFICATION.json');ver=j(O/'final-independent-verification.json')
assert qual['verification_sha256']==sha(O/'final-independent-verification.json')
assert qual['status']=='REPAIRED_PASS_LOCAL_TWO_RECORDS_EIGHT_PROOFS_AND_32_PAGES'
assert all(b==bm[b['id']]for b in qual['current_record_versions'])
assert len(j(O/'complete-proof-review.json'))==8 and len(j(O/'exact-symbolic-checks.json'))==36
notes=j(O/'actual-page-notes.json');assert len(notes['notes'])==32 and len(notes['repair_notes'])==5
assert all('?'not in note and any(ord(ch)>127 for ch in note)for _,note in notes['notes'])
st=j(R/'reviews/codex-supervision/2026-10-07-continuous-math-review/CURRENT_STATUS.json')
for k,filename in [('record_bindings_sha256','current-record-bindings.jsonl'),('signature_sha256','current-complete-signatures.jsonl'),('source_bindings_sha256','current-source-bindings.json')]:assert st[k]==sha(O/filename)
for follow in (st['latest_visual_followup'],st['latest_glyph_continuation']):
 assert follow['delivery_index_sha256']==sha(idx)and follow['report_sha256']==sha(O/'FIX_REPORT.md')and follow['manual_image_review_pages']==296 and follow['unreviewed_current_pages']==337
assert st['current_sources']==24 and st['total_reviewed_core']==761 and st['PASS_CORE_SCOPE_issued']is False
assert st['full_glyph_visual_acceptance']=='NOT_ESTABLISHED'and st['semantic_isolation']=='NOT_ESTABLISHED'and st['production']=='CLOSED'
readme=R/'reviews/2026-10-08-visual-acceptance/README.md'
assert st['latest_glyph_continuation']['readme_sha256']==sha(readme)
oldreadme=(O/'visual-readme-before.md').read_bytes()
assert readme.read_bytes()==(O/'readme-header-content.md').read_bytes()+oldreadme[oldreadme.index(b'---'):]
assert readme.read_bytes().split(b'---',1)[1]==(O/'visual-readme-before.md').read_bytes().split(b'---',1)[1]
assert any(ord(x)>127 for x in readme.read_text('utf-8').split('---',1)[0])and'?'not in readme.read_text('utf-8').split('---',1)[0]
for path,h in ver['protected_code_hashes'].items():assert sha(R/path)==h
result={'status':'PASS_FINAL_CURRENT_SOURCE_BINDINGS_LEDGER_QUALIFICATION_AND_ACTIVE_POINTERS','at':datetime.now(timezone(timedelta(hours=8))).isoformat(),'core_records':761,'physical_sources':24,'signature_versions':761,'index_records':165,'index_pages':633,'qualified_current_pages':296,'pending_pages':337,'proofs':8,'symbolic_checks':36,'new_pages':32,'report_sha256':sha(O/'FIX_REPORT.md'),'readme_sha256':sha(readme),'current_status_sha256_at_validation':sha(R/'reviews/codex-supervision/2026-10-07-continuous-math-review/CURRENT_STATUS.json'),'index_sha256':sha(idx),'production':'CLOSED'}
(O/'final-delivery-validation.json').open('xb').write(c.encoded(result));print(json.dumps(result))
