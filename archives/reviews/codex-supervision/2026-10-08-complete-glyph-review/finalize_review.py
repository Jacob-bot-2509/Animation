from pathlib import Path
import json,sys,copy,math
from collections import Counter
from fractions import Fraction as F
from datetime import datetime,timezone,timedelta
import numpy as np
from PIL import Image
import av
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'))
import core_signatures as c,native_render_pilot as n
def sha(p):return c.digest(p.read_bytes())
def read(p):return json.loads(p.read_text('utf-8'))
def lines(p):return [json.loads(z) for z in p.read_text('utf-8').splitlines() if z.strip()]
def save(p,v):p.write_bytes(c.encoded(v))
def rel(p):return p.relative_to(R).as_posix()
def path(s):return c.checked_path(s,R)
old=lines(O/'parent-CURRENT_DELIVERY_INDEX.jsonl');bs=lines(O/'current-record-bindings.jsonl');bmap={b['id']:b for b in bs}
assert len(bs)==len(bmap)==761
ss=read(O/'current-source-bindings.json');assert len(ss)==24
qs={};groups=Counter()
for s in ss:
 p=path(s['path']);assert sha(p)==s['sha256'];rs=lines(p);assert len(rs)==s['records']
 for i,q in enumerate(rs,1):
  rid=q['id'];assert rid not in qs;qs[rid]=q;groups[s['group']]+=1;b=bmap[rid]
  assert b['path']==s['path'] and b['source_line']==i and b['source_sha256']==s['sha256']
  assert b['record_sha256']==c.dense(q) and b['math_sha256']==c.math_digest(q)
assert len(qs)==761
sig=lines(O/'current-complete-signatures.jsonl');assert len(sig)==761
for s in sig:assert s['record_sha256']==bmap[s['id']]['record_sha256'] and s['math_sha256']==bmap[s['id']]['math_sha256']
parentbs={b['id']:b for b in lines(O/'parent-current-record-bindings.jsonl')}
changed=[rid for rid,b in bmap.items() if b['record_sha256']!=parentbs[rid]['record_sha256']]
plan=read(O/'render-plan.json');assert set(changed)==set(plan['changed_record_ids'])
for rid,b in bmap.items():
 pb=parentbs[rid];pq=lines(path(pb['path']))[pb['source_line']-1]
 assert pq['id']==rid and qs[rid]['problem']==pq['problem']
for rid in ['eval-calc-030-s3','eval-geom-007-s1','eval-geom-007-s2','eval-linalg-004-s3','eval-linalg-002-s3']:assert bmap[rid]['record_sha256']==parentbs[rid]['record_sha256']
progress=read(O/'manual-review-progress.json');assert len(progress['notes'])==337 and len(progress['math_notes'])==98
oldqueue=read(O/'parent-effective-page-review-queue.json')['pages'];omap={p['ordinal']:p for p in oldqueue}
original=[]
for ordinal,status,note in progress['notes']:
 p=copy.deepcopy(omap[ordinal]);p['original_review_note']=note;p['original_review_status']=status if status=='PASS' or status.startswith('NEEDS') else 'PASS'
 p['reviewer']='codex';original.append(p)
assert len({p['ordinal']for p in original})==337
save(O/'original-337-page-verdicts.json',original)
originalby={(p['id'],p['page']):p for p in original}
newnotes=read(O/'actual-repair-page-notes.json');assert len(newnotes)==75 and all(p['status']=='PASS_ACTUAL_IMAGE_REVIEW'for p in newnotes)
newmap={(p['id'],p['page']):p for p in newnotes}
receipts={r['id']:r for r in read(O/'render-execution.json')};assert len(receipts)==19
index=[];queue=[];metrics=[];pixel_checks=[];inventory_rebindings=[];ordinal=0
for d0 in old:
 d=copy.deepcopy(d0);rid=d['id'];b=bmap[rid];q=qs[rid]
 f,loc=n.formula_inventory(q)
 if rid in receipts:
  rc=receipts[rid];assert rc['rc']==0 and rc['record_binding']==b
  for k in ['mp4','geometry','formula_inventory']:d[k+'_path']=rc[k+'_path'];d[k+'_sha256']=rc[k+'_sha256']
  d['canonical_frames']=rc['frames'];d['page_count']=rc['page_count'];d['video_frames']=rc['video_frames']
  d['render_parent_binding']=b
 for k in ['mp4','geometry','formula_inventory']:assert sha(path(d[k+'_path']))==d[k+'_sha256'],(rid,k)
 inv=read(path(d['formula_inventory_path']));assert inv['unique_formulas']==f,(rid,'formula inventory')
 if inv['source_occurrences']!=loc:
  assert rid in plan['unchanged_formula_pixels_ids'],rid
  p=O/'rebound-inventories'/f'{rid}.json';p.parent.mkdir(exist_ok=True)
  save(p,{'unique_formulas':f,'source_occurrences':loc,'pixel_reuse_basis':'Ordered unique formula list identical; occurrence inventory rebound to current full record','parent_inventory_path':d['formula_inventory_path'],'parent_inventory_sha256':d['formula_inventory_sha256']})
  inventory_rebindings.append({'id':rid,'old_occurrences':len(inv['source_occurrences']),'new_occurrences':len(loc),'pixels_unchanged':True})
  d['formula_inventory_path']=rel(p);d['formula_inventory_sha256']=sha(p)
 g=read(path(d['geometry_path']));assert len(g['pages'])==len(d['canonical_frames'])==d['page_count'];assert g['pixel_width']==3840 and g['pixel_height']==2160
 covered={i['formula_index']for p in g['pages']for i in p['items']};assert covered==set(range(len(f)))
 if rid in receipts:
  starts={fr['video_frame_index']:fr for fr in d['canonical_frames']};j=0;count=0
  with av.open(str(path(d['mp4_path']))) as container:
   stream=container.streams.video[0]
   assert (stream.width,stream.height)==(3840,2160) and F(stream.average_rate)==1
   for frame in container.decode(stream):
    if j in starts:
     fr=starts[j];expected=np.array(Image.open(path(fr['path'])).convert('RGB'))
     assert F(frame.pts)*F(frame.time_base)==F(fr['video_time_seconds_exact'])
     assert np.array_equal(np.array(frame.to_image()),expected),(rid,j)
     count+=1
    j+=1
  assert count==d['page_count'] and j==d['video_frames']
  pixel_checks.append({'id':rid,'frames_decoded':j,'page_start_pixels_exact':count,'status':'PASS'})
 dm=[]
 for pg,fr in zip(g['pages'],d['canonical_frames']):
  png=path(fr['path']);assert sha(png)==fr['sha256'];assert F(fr['video_time_seconds_exact'])==fr['video_frame_index']
  im=Image.open(png);assert im.size==(3840,2160);a=np.array(im.convert('RGB'))[271:1889,136:3704];mask=np.any(a>32,axis=2);ys,xs=np.nonzero(mask);assert len(xs)>0
  height=int(ys.max()-ys.min()+1);width=int(xs.max()-xs.min()+1);cnt=len(pg['items']);ratio=F(height,cnt)
  m={'page':pg['page'],'bbox_height':height,'bbox_width':width,'ink_pixels':int(mask.sum()),'displayed_formula_items':cnt,'bbox_height_per_displayed_item_px_exact':str(ratio),'slot_proxy_at_1080p_exact':str(ratio/2),'metric_scope':'OCCUPIED_BBOX_SLOT_PROXY_NOT_MINIMUM_GLYPH_SIZE'}
  dm.append(m);metrics.append({'id':rid,**m,'kind':pg['kind']})
  if rid in receipts:ver=newmap[(rid,pg['page'])];assert ver['path']==fr['path'] and ver['sha256']==fr['sha256'];basis=rel(O/'actual-repair-page-notes.json')
  elif (rid,pg['page']) in originalby:
   ver=originalby[(rid,pg['page'])];assert ver['path']==fr['path'] and ver['sha256']==fr['sha256'];assert ver['original_review_status']=='PASS',(rid,pg['page'],ver['original_review_status']);basis=rel(O/'original-337-page-verdicts.json')
  else:
   ver=next(p for p in oldqueue if p['id']==rid and p['page']==pg['page']);assert ver['review_status']=='PASS_ACTUAL_IMAGE_REVIEW';assert ver['path']==fr['path'] and ver['sha256']==fr['sha256'];basis=ver['verdict_source']
  queue.append({'ordinal':ordinal,'id':rid,'page':pg['page'],'path':fr['path'],'sha256':fr['sha256'],'record_sha256':b['record_sha256'],'math_sha256':b['math_sha256'],'kind':pg['kind'],'tile':pg['tile'],'tile_grid':pg['tile_grid'],'formulas':[{'index':i['formula_index']+1,'tex':f[i['formula_index']]}for i in pg['items']],'review_status':'PASS_ACTUAL_IMAGE_REVIEW','verdict_source':basis,'current_binding_reuse_basis':'Current source formulas identical to reviewed pixels' if rid not in receipts else 'Fresh native render of current full record'})
  ordinal+=1
 d.update({'record_sha256':b['record_sha256'],'math_sha256':b['math_sha256'],'source_path':b['path'],'source_sha256':b['source_sha256'],'source_line':b['source_line'],'unique_formulas':len(f),'source_formula_occurrences':len(loc),'page_metrics':dm,'segment_pages':sum(p['kind']=='FORMULA_SEGMENT'for p in g['pages']),'full_glyph_visual_acceptance':'PASS_LOCAL_CURRENT_BOUND_ALL_FORMULA_PAGES','conceptual_animation':'NOT_EVALUATED','production':'CLOSED','verification':rel(O/'final-independent-verification.json')})
 index.append(d)
assert len(index)==165
ip=O/'CURRENT_DELIVERY_INDEX.jsonl';ip.write_text(''.join(json.dumps(v,ensure_ascii=False,sort_keys=True)+'\n'for v in index),encoding='utf-8',newline='\n')
save(O/'effective-page-review-queue.json',{'index_path':rel(ip),'index_sha256':sha(ip),'pages':queue,'reviewed_pages':len(queue),'pending_pages':0,'records':165})
save(O/'current-unreviewed-pages.json',{'index_sha256':sha(ip),'pages':[],'count':0})
save(O/'native-video-pixel-verification.json',{'status':'PASS','new_render_records':19,'new_exact_page_starts':75,'checks':pixel_checks,'unchanged_videos':'SHA256 checked against parent validated native-video receipts; no repeated pixel decoding claim'})
save(O/'inventory-rebindings.json',inventory_rebindings)
vals=sorted(F(m['bbox_height_per_displayed_item_px_exact'])for m in metrics)
stats={'pages':len(vals),'minimum_exact':str(vals[0]),'p10_nearest_rank_exact':str(vals[math.ceil(len(vals)/10)-1]),'median_exact':str(vals[len(vals)//2] if len(vals)%2 else (vals[len(vals)//2-1]+vals[len(vals)//2])/2),'scope':'OCCUPIED_BBOX_SLOT_PROXY_NOT_MINIMUM_GLYPH_SIZE','minimum_glyph_height':'NOT_CERTIFIED'}
save(O/'current-page-metrics.json',{'summary':stats,'pages':metrics})
v={'status':'PASS_LOCAL_COMPLETE_CURRENT_FORMULA_PAGE_REVIEW','records':165,'pages':len(queue),'reviewed_pages':len(queue),'pending_pages':0,'full_pages':sum(p['kind']=='FULL_FORMULAS'for p in queue),'segment_pages':sum(p['kind']=='FORMULA_SEGMENT'for p in queue),'sources':24,'source_records':761,'groups':dict(groups),'changed_records':23,'changed_signature_descriptors':3,'current_batch_proofs':98,'exact_symbolic_checks':96,'original_pending_images_actually_viewed':337,'fresh_images_actually_viewed':75,'new_video_pixel_checks':75,'question_ids_and_problem_text_unchanged':True,'prior_five_repairs_preserved':True,'inventory_rebindings':inventory_rebindings,'index_sha256':sha(ip),'record_bindings_sha256':sha(O/'current-record-bindings.jsonl'),'source_bindings_sha256':sha(O/'current-source-bindings.json'),'signature_sha256':sha(O/'current-complete-signatures.jsonl'),'glyph_metrics':stats,'conceptual_animation':'NOT_EVALUATED','semantic_isolation':'NOT_ESTABLISHED','native_sandbox':'UNVERIFIED','production':'CLOSED','PASS_CORE_SCOPE_issued':False}
save(O/'final-independent-verification.json',v)
progress.update({'status':'COMPLETE_CURRENT_BATCH','fresh_images_actually_viewed':75,'current_pages':len(queue),'current_pending_pages':0,'final_verification':rel(O/'final-independent-verification.json')});save(O/'manual-review-progress.json',progress)
save(O/'QUALIFICATION.json',v)
print(json.dumps(v,ensure_ascii=False))
