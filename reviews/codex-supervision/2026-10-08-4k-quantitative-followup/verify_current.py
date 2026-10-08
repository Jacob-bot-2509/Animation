from pathlib import Path
import json,hashlib
from PIL import Image
from fractions import Fraction
R=Path('.');O=R/'reviews/codex-supervision/2026-10-08-4k-quantitative-followup';P=R/'reviews/codex-supervision/2026-10-08-glyph-review-followup'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
q=json.loads((O/'current-page-review-queue.json').read_text('utf-8'));quant=json.loads((O/'current-quantitative-corrected.json').read_text('utf-8'));index=list(map(json.loads,(P/'DELIVERY_INDEX.jsonl').read_text('utf-8').splitlines()))
lookup={(r['id'],m['page']):dict(f,record_sha256=r['record_sha256'],math_sha256=r['math_sha256'])for r in index for f,m in zip(r['canonical_frames'],r['page_metrics'])}
assert len(q['pages'])==len(quant['pages'])==len(lookup)==633
for p,me in zip(q['pages'],quant['pages']):
 assert all(p[k]==me[k]for k in ('id','page','path','sha256','kind'))
 bound=lookup[(p['id'],p['page'])]
 assert all(p[k]==bound[k]for k in ('path','sha256','record_sha256','math_sha256'))
 assert sha(R/p['path'])==p['sha256']
 with Image.open(R/p['path'])as im:assert im.size==(3840,2160)
 Fraction(me['bbox_height_per_displayed_item_px_exact'])
 assert me['displayed_formula_items']==len(p['formulas'])
assert sum(p['review_status']=='PASS_ACTUAL_IMAGE_REVIEW'for p in q['pages'])==144
new=list(map(json.loads,(O/'page-glyph-verdicts.jsonl').read_text('utf-8').splitlines()))
assert len(new)==24 and len({(v['id'],v['page'])for v in new})==24
for v in new:
 p=q['pages'][v['ordinal']]
 assert v['status']=='PASS' and all(v[k]==p[k]for k in ('id','page','sha256','record_sha256','math_sha256','formulas','kind'))
 assert v['symbols_checked']==[f['index']for f in v['formulas']] and v['notes']
repair=json.loads((O/'README-repair-verification.json').read_text('utf-8'))
assert sha(R/repair['path'])==repair['after_sha256']
rawauthor=R/'reviews/2026-10-08-visual-acceptance/readable-pages-verification-4k.json'
assert sha(rawauthor)==repair['raw_author_report_unchanged_sha256']
receipt=dict(status='PASS_BOUND_CURRENT_QUANTITATIVE_AND_ACTUAL_VERDICT_ARCHIVE',actual_pngs_sha_and_resolution_checked=633,actual_png_size=[3840,2160],actual_new_manual_verdicts=24,actual_total_same_version_manual_verdicts=144,unreviewed_pages=489,index_sha256=sha(P/'DELIVERY_INDEX.jsonl'),current_quantitative_sha256=sha(O/'current-quantitative-corrected.json'),active_readme_sha256=sha(R/repair['path']),report_sha256=sha(O/'FIX_REPORT.md'),full_glyph_visual_acceptance='NOT_ESTABLISHED')
with(O/'final-independent-verification.json').open('xb')as f:f.write((json.dumps(receipt,indent=2)+'\n').encode('utf-8'))
print(json.dumps(receipt))
