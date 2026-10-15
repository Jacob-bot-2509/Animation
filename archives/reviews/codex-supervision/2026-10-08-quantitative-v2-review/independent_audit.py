"""Independent v2 binding audit and comparison to named frozen native-pixel metrics."""
from pathlib import Path
from fractions import Fraction as F
import json,hashlib,importlib.util
from PIL import Image
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
P=R/'reviews/codex-supervision/2026-10-08-4k-quantitative-followup'
G=R/'reviews/codex-supervision/2026-10-08-glyph-review-followup'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(x,msg):
 if not x:raise ValueError(msg)
def save(name,data):
 with(O/name).open('xb')as f:f.write((json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
check(sha(P/'delivery-manifest.json')=='b22609e85eaca58644f9951ecc1a41947f5ac11e5b62e7ef76438bb409f2bccb','Changed named parent')
manifest=json.loads((P/'delivery-manifest.json').read_text('utf-8'))
for a in manifest['artifacts']:
 p=(P/a['path']).resolve();check(p.is_relative_to(P.resolve())and sha(p)==a['sha256']and p.stat().st_size==a['bytes'],'Changed parent artifact')
check(sha(G/'DELIVERY_INDEX.jsonl')=='07b4543d38599e1c30d2b515e0c2a8761e5611f771c46c75ee23b357c58b6331','Changed current index')
previous=json.loads((P/'current-quantitative-corrected.json').read_text('utf-8'));old={(p['id'],p['page']):p for p in previous['pages']}
v3=json.loads((O/'verification-v3.json').read_text('utf-8'));now={(r['id'],p['page']):p for r in v3['records']for p in r['page_rows']}
author=json.loads((O/'author-v2-original.json').read_text('utf-8'));authors={r['id']:r for r in author['records']}
check(len(authors)==len(author['records'])==165,'Duplicate/missing author records')
rows=list(map(json.loads,(G/'DELIVERY_INDEX.jsonl').read_text('utf-8').splitlines()));pages=full=segments=0;bindings=[]
for r in rows:
 gpath=R/r['geometry_path'];check(sha(gpath)==r['geometry_sha256'],'Changed geometry')
 geo=json.loads(gpath.read_text('utf-8'));ar=authors[r['id']]
 check(ar['pages']==len(ar['page_rows'])==len(geo['pages'])==len(r['canonical_frames'])==r['page_count'],'Author page coverage mismatch')
 for i,(gp,fr,ap)in enumerate(zip(geo['pages'],r['canonical_frames'],ar['page_rows'])):
  check(ap['page_order_index']==i and ap['path']==fr['path']and ap['frame_sha256']==fr['sha256']and ap['kind']==gp['kind']and ap['formulas_on_page']==len(gp['items']),'Author ordered binding mismatch')
  path=R/fr['path'];check(sha(path)==fr['sha256'],'Actual PNG SHA mismatch')
  with Image.open(path)as im:check(list(im.size)==ap['size']==[3840,2160],'Actual image resolution mismatch')
  native=now[(r['id'],gp['page'])];prior=old[(r['id'],gp['page'])]
  check(native['path']==prior['path']==fr['path']and native['frame_sha256']==prior['sha256']==fr['sha256'],'Native candidate page mismatch')
  for a,b in [('formula_ink','ink_pixels'),('bbox_height','bbox_height'),('bbox_width','bbox_width'),('formulas_on_page','displayed_formula_items')]:check(native[a]==prior[b],'Recomputed native metric disagrees with independent frozen metric')
  if gp['kind']=='FULL_FORMULAS':
   full+=1;check(F(native['slot_px_proxy_exact'])==F(prior['bbox_height_per_displayed_item_px_exact']),'Exact full slot mismatch')
   check(ap['slot_px_proxy']is not None,'Missing author full slot')
  else:
   segments+=1;check(ap['slot_px_proxy']is None and native['slot_px_proxy_exact']is None,'Segment improperly counted in slot stats')
  pages+=1;bindings.append(dict(id=r['id'],page=gp['page'],path=fr['path'],sha256=fr['sha256'],kind=gp['kind'],status='PASS_BOUND_CURRENT_VERSION'))
check((pages,full,segments)==(633,552,81),'Population mismatch')
slots=sorted(F(p['slot_px_proxy_exact'])for p in now.values()if p['kind']=='FULL_FORMULAS');stats=dict(min=str(slots[0]),p10_nearest_rank=str(slots[(len(slots)+9)//10-1]),median=str((slots[len(slots)//2-1]+slots[len(slots)//2])/2))
check(stats==v3['summary']['full_page_slot_proxy_exact'],'Native summary mismatch')
astats=sorted(F(str(p['slot_px_proxy']))for r in author['records']for p in r['page_rows']if p['kind']=='FULL_FORMULAS')
astat=dict(min=str(astats[0]),p10_nearest_rank=str(astats[(len(astats)+9)//10-1]),median_arithmetic=str((astats[275]+astats[276])/2),median_upper=str(astats[276]),published_median_as_fraction=str(F(str(author['summary']['full_page_slot_proxy_median']))))
ledger_cache={};q=json.loads((O/'current-page-review-queue.json').read_text('utf-8'));inherit=0
for p in q['pages']:
 if p['review_status']=='PASS_ACTUAL_IMAGE_REVIEW' and p['verdict_source']!=(O/'page-glyph-verdicts.jsonl').relative_to(R).as_posix():
  src=R/p['verdict_source']
  if str(src)not in ledger_cache:ledger_cache[str(src)]=list(map(json.loads,src.read_text('utf-8').splitlines()))
  candidates=[v for v in ledger_cache[str(src)]if v['status']=='PASS'and all(v[k]==p[k]for k in ('id','sha256','record_sha256','math_sha256','formulas','kind','tile','tile_grid'))]
  check(len(candidates)==1,'Inherited glyph binding mismatch');inherit+=1
check(inherit==144,'Inherited coverage mismatch')
spec=importlib.util.spec_from_file_location('original_author_metric',O/'visual_acceptance_verify_pages.before.py');original=importlib.util.module_from_spec(spec);spec.loader.exec_module(original)
counter=[]
for key in [('eval-calc-022-s2',6),('calc-area-009',1)]:
 prior=old[key];met=original.metrics(R/prior['path']);n=prior['displayed_formula_items'];proxy=F(str(round((met['bbox'][3]-met['bbox'][1])/n,1)))
 ap=next(p for p in authors[key[0]]['page_rows']if p['page_order_index']==key[1]-1)
 check(proxy==F(str(ap['slot_px_proxy'])),'Original algorithm not reproducible on counterexample')
 counter.append(dict(id=key[0],page=key[1],path=prior['path'],sha256=prior['sha256'],formula_region_inclusive_height=prior['bbox_height'],formula_region_slot_exact=prior['bbox_height_per_displayed_item_px_exact'],original_downsampled_canvas_bbox=met['bbox'],author_rounded_canvas_slot_as_fraction=str(proxy),author_ink_count_half_resolution=met['ink'],explanation='Original metrics scans full downsampled canvas including title, whereas the native formula metric excludes title and does not resize.'))
for row in json.loads((G/'final-active-hashes.json').read_text('utf-8'))['files']:check(sha(R/row['path'])==row['sha256'],'Unrelated renderer/math code changed')
check(sha(R/'tools/visual_acceptance_verify_pages.py')==v3['verifier_sha256']==sha(O/'visual_acceptance_verify_pages.after.py'),'Active tool changed since run')
check(sha(R/'reviews/2026-10-08-visual-acceptance/readable-pages-verification-4k-v2.json')==sha(O/'author-v2-original.json'),'Author original changed')
save('author-reproduction-counterexamples.json',dict(original_tool_sha256=sha(O/'visual_acceptance_verify_pages.before.py'),examples=counter))
save('independent-v2-review.json',dict(status='PASS_CURRENT_BINDINGS_AND_REPAIRED_NATIVE_FORMULA_METRICS_ONLY',parent_artifacts_verified=len(manifest['artifacts']),author_original_sha256=sha(O/'author-v2-original.json'),author_original_tool_sha256=sha(O/'visual_acceptance_verify_pages.before.py'),pages=pages,full_pages=full,segment_pages=segments,author_summary_from_rounded_rows_exact=astat,repaired_summary_exact=stats,actual_png_SHA_and_size_checked=633,native_metrics_equal_independent_frozen_method=633,inherited_actual_glyph_bindings=144,page_bindings=bindings,full_glyph_visual_acceptance='NOT_ESTABLISHED'))
print(json.dumps(dict(status='PASS_CURRENT_BINDINGS_AND_REPAIRED_NATIVE_METRICS',pages=pages,full=full,segments=segments,author_summary=astat,repaired_stats=stats,counterexamples=counter)))
