from pathlib import Path
import json,copy,sys,difflib
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'))
import core_signatures as c,native_render_pilot as n
P=R/'reviews/codex-supervision/2026-10-08-glyph-mail-744-review'
def j(p):return json.loads(p.read_text('utf-8'))
def jl(p):return list(map(json.loads,p.read_text('utf-8').splitlines()))
def sha(p):return c.digest(p.read_bytes())
def save(name,v):
 with(O/name).open('xb')as f:f.write(c.encoded(v))
def lines(name,vs):
 with(O/name).open('xb')as f:
  for v in vs:f.write((json.dumps(v,ensure_ascii=False,sort_keys=True)+'\n').encode())
rows=jl(O/'dataset_eval-candidate.jsonl');oldrows=jl(O/'source-before.jsonl')
rid='eval-linalg-002-s3';i=next(i for i,x in enumerate(rows)if x['id']==rid)
old=copy.deepcopy(rows[i]);new=copy.deepcopy(old)
bad='??????????????';good='??????????????'
assert new['efficiency_tags'].count(bad)==1 and new['scene_spec']['objects'].count(bad)==1
assert new['scene_spec']['steps'].count('?????'+bad)==1
new['efficiency_tags']=[x.replace(bad,good)for x in new['efficiency_tags']]
new['scene_spec']['objects']=[x.replace(bad,good)for x in new['scene_spec']['objects']]
new['scene_spec']['steps']=[x.replace(bad,good)for x in new['scene_spec']['steps']]
assert all(new[k]==old[k]for k in ('problem','solution','answer','id'))
assert n.formula_inventory(old)==n.formula_inventory(new)
save('scene-record-before.json',old);save('scene-record-after.json',new)
with(O/'scene-label-changes.patch').open('xb')as f:f.write(''.join(difflib.unified_diff(json.dumps(old,ensure_ascii=False,indent=2).splitlines(True),json.dumps(new,ensure_ascii=False,indent=2).splitlines(True),fromfile='scene-record-before.json',tofile='scene-record-after.json')).encode())
rows[i]=new;lines('dataset_eval-final-candidate.jsonl',rows);target=O/'dataset_eval-final-candidate.jsonl'
changed=[x['id']for x,y in zip(rows,oldrows)if x!=y];assert changed==['eval-linalg-002-s3','eval-linalg-004-s3']
bs=jl(P/'effective-record-bindings.jsonl');parent={x['id']:copy.deepcopy(x)for x in bs}
for b in bs:
 if b['group']=='eval':
  row=rows[b['source_line']-1];assert row['id']==b['id']
  b.update(path=target.relative_to(R).as_posix(),source_sha256=sha(target))
  if b['id']in changed:b.update(parent_binding=parent[b['id']],record_sha256=c.dense(row),math_sha256=c.math_digest(row),review='CURRENT_REPAIR_PENDING_INDEPENDENT_VERIFICATION')
lines('current-record-bindings.jsonl',bs)
sigs=jl(P/'effective-complete-signatures.jsonl');bmap={b['id']:b for b in bs}
for s in sigs:
 if s['id']in changed:s.update(record_sha256=bmap[s['id']]['record_sha256'],math_sha256=bmap[s['id']]['math_sha256'])
lines('current-complete-signatures.jsonl',sigs)
sources=[x for x in j(P/'effective-source-bindings.json')if x['group']!='eval']
sources.append({'path':target.relative_to(R).as_posix(),'sha256':sha(target),'bytes':target.stat().st_size,'records':300,'group':'eval','parent_path':(P/'dataset_eval-final-candidate.jsonl').relative_to(R).as_posix(),'parent_sha256':sha(P/'dataset_eval-final-candidate.jsonl'),'unchanged_source_bytes':False})
assert len(sources)==24 and sum(x['records']for x in sources)==761
save('current-source-bindings.json',sources)
save('final-version-binding.json',{'changed_ids_this_batch':changed,'source_records':300,'core_records':761,'physical_sources':24,'render_phase_source':'dataset_eval-candidate.jsonl','final_candidate_source':'dataset_eval-final-candidate.jsonl','render_phase_source_sha256':sha(O/'dataset_eval-candidate.jsonl'),'final_candidate_source_sha256':sha(target),'render_phase_record_004_s3_unchanged_in_final':c.dense(rows[206])==c.dense(j(O/'record-after.json')),'two_repairs':[{'before':parent[k],'after':bmap[k]}for k in changed],'prior_three_repaired_ids_preserved':['eval-calc-030-s3','eval-geom-007-s1','eval-geom-007-s2'],'qualification':'PENDING_INDEPENDENT_VERIFICATION','production':'CLOSED'})
print(json.dumps({'status':'TWO_REPAIRS_READY_FOR_INDEPENDENT_VERIFICATION','source_sha256':sha(target),'changed_ids':changed}))
