"""Verify the new author report against its named old 4K parent and current 633-page delivery."""
from pathlib import Path
import json,hashlib,importlib.util,math
from fractions import Fraction as F
from statistics import median
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(x,msg):
 if not x:raise ValueError(msg)
def save(name,x):
 with(O/name).open('xb')as f:f.write((json.dumps(x,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
old=R/'reviews/codex-supervision/2026-10-08-hd-formula-mail-review'
current=R/'reviews/codex-supervision/2026-10-08-glyph-review-followup'
for folder,expected in [(old,'12d50e59e50ee53c219be17d080c83a615523c7305ae5c659bec3b7fbacf902b'),(current,'57a94b01c8c26ac7e898901a4b6f9bd5006b972b84266b9212272c388a139491')]:
 check(sha(folder/'delivery-manifest.json')==expected,'Parent manifest changed')
 m=json.loads((folder/'delivery-manifest.json').read_text('utf-8'))
 check(len({a['path']for a in m['artifacts']})==len(m['artifacts']),'Duplicate bound artifact')
 for a in m['artifacts']:
  p=(folder/a['path']).resolve();check(p.is_relative_to(folder.resolve())and sha(p)==a['sha256']and p.stat().st_size==a['bytes'],'Parent artifact changed')
 print('Verified frozen '+folder.name,flush=True)
spec=importlib.util.spec_from_file_location('named_auditor',old/'audit_hd.py');audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)
author=json.loads((O/'author-4k-original.json').read_text('utf-8'))
authorrows={(r['id'],p['page']):p for r in author['records']for p in r['page_rows']}
check(len(author['records'])==165 and len(authorrows)==626,'Author coverage duplicates/missing')
cache={};versions={};diff=[]
for tag,folder in [('submitted_old_626',old),('current_repaired_633',current)]:
 rows=list(map(json.loads,(folder/'DELIVERY_INDEX.jsonl').read_text('utf-8').splitlines()));pages=[]
 for row in rows:
  g=json.loads((R/row['geometry_path']).read_text('utf-8'))
  check(len(g['pages'])==len(row['canonical_frames'])==len(row['page_metrics']),'Bound page coverage')
  for p,fr,bound in zip(g['pages'],row['canonical_frames'],row['page_metrics']):
   path=R/fr['path'];check(sha(path)==fr['sha256'],'Page SHA changed')
   n=len(p['items']);key=(fr['sha256'],n)
   if key not in cache:cache[key]=audit.page_density(path,n)
   me=cache[key];check(me=={k:bound[k]for k in me},'Frozen metric not reproducible')
   got=dict(id=row['id'],page=p['page'],path=fr['path'],sha256=fr['sha256'],pixel_resolution=[3840,2160],kind=p['kind'],**me);pages.append(got)
   if tag=='submitted_old_626':
    ar=authorrows[(row['id'],p['page'])]
    check(ar['size']==[3840,2160]and ar['formulas_on_page']==n,'Author size/item mismatch')
    if F(str(ar['slot_px']))!=F(me['bbox_height_per_displayed_item_px_exact']):
     diff.append(dict(id=row['id'],page=p['page'],path=fr['path'],sha256=fr['sha256'],author_slot_exact=str(F(str(ar['slot_px']))),formula_only_slot_exact=me['bbox_height_per_displayed_item_px_exact']))
 slots=sorted(F(p['bbox_height_per_displayed_item_px_exact'])for p in pages)
 summary=dict(records=len(rows),pages=len(pages),geometry_items_total=sum(p['displayed_formula_items']for p in pages),slot_native_2160p_min_exact=str(slots[0]),slot_native_2160p_p10_nearest_rank_exact=str(slots[math.ceil(len(slots)/10)-1]),slot_native_2160p_median_exact=str(median(slots)),slot_1080p_min_exact=str(slots[0]/2),pixel_resolution=[3840,2160],minimum_glyph_height='NOT_CERTIFIED',full_glyph_visual_acceptance='NOT_ESTABLISHED')
 versions[tag]=dict(index_path=(folder/'DELIVERY_INDEX.jsonl').relative_to(R).as_posix(),index_sha256=sha(folder/'DELIVERY_INDEX.jsonl'),summary=summary,pages=pages)
 print(json.dumps(dict(version=tag,**summary)),flush=True)
save('independent-quantitative-review.json',dict(author_report_sha256=sha(O/'author-4k-original.json'),author_algorithm='NOT_SUBMITTED',author_page_sha_fields='NOT_PRESENT_IN_SUBMITTED_JSON',method='Named frozen audit_hd.py page_density: native 3840x2160 PNG rows 271:1889, columns 136:3704, any RGB>32, inclusive occupied bbox height / displayed items. Quantiles: p10 nearest rank ceil(N/10); median exact arithmetic mean if even. Occupied bbox slot is not minimum glyph height.',author_slot_disagreement_count=len(diff),author_slot_disagreements=diff,versions=versions))
save('current-quantitative-corrected.json',dict(schema='bound-formula-slot-proxy-v2',index_path=versions['current_repaired_633']['index_path'],index_sha256=versions['current_repaired_633']['index_sha256'],summary=versions['current_repaired_633']['summary'],pages=versions['current_repaired_633']['pages'],all_rational_metrics='EXACT_FRACTIONS',minimum_glyph_height='NOT_CERTIFIED_BY_SLOT_PROXY',global_visual_acceptance='NEEDS_EVIDENCE_ACTUAL_PAGE_VERDICTS'))
save('old-current-version-delta.json',dict(old_pages=626,current_pages=633,math_record_count=165,changed_render_record_ids=[n['id']for n in map(json.loads,(current/'REPAIRED_INDEX.jsonl').read_text('utf-8').splitlines())],known_old_actual_fail=dict(id='draft-c33-03',page=3,formula_index=12,verdict_source='reviews/codex-supervision/2026-10-08-glyph-review-followup/page-glyph-verdicts.jsonl',defect='STACKED_MATRIX_FRACTIONS_ROW_COLLISION',current_fix='NEW_RENDER_DRAFT_C33_03_PAGE_5_PASS_ACTUAL_IMAGE_REVIEW'),author_claim_limit='Its 626-page quantitative report does not bind or close the current 633-page visual qualification.'))
print(json.dumps({'status':'PASS_BOUND_QUANTITATIVE_REVIEW_ONLY','author_slot_disagreements':len(diff),'cache_pages':len(cache)}),flush=True)
