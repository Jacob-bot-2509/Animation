from pathlib import Path
import json,sys,copy,difflib,subprocess,time
from fractions import Fraction
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'))
import core_signatures as c,native_render_pilot as n,hd_formula_pages as h
P=R/'reviews/codex-supervision/2026-10-08-glyph-mail-744-review'
def read(p):return json.loads(p.read_text('utf-8'))
def sha(p):return c.digest(p.read_bytes())
def save(name,v):
 with (O/name).open('xb')as f:f.write(c.encoded(v))
def jl(name,vs):
 with (O/name).open('xb')as f:
  for v in vs:f.write((json.dumps(v,ensure_ascii=False,sort_keys=True)+'\n').encode())
bs=list(map(json.loads,(P/'effective-record-bindings.jsonl').read_text('utf-8').splitlines()));by={b['id']:copy.deepcopy(b) for b in bs}
rid='eval-linalg-004-s3';b=by[rid]
source=P/'dataset_eval-final-candidate.jsonl';assert sha(source)=='af8fdf68b7009aa6c09345911793d9eb663769c2ca0f0b5df9deaa0d85911504'
raw=source.read_bytes();rows=list(map(json.loads,raw.decode().splitlines()));old=rows[b['source_line']-1];assert c.dense(old)==b['record_sha256']
new=copy.deepcopy(old)
bad=r'$ab^2\cdot\det(e_1,e_2,e_j$ \u6362\u4e3a $(1,1,1)^T)=ab^2$'.replace(r'\u6362\u4e3a','\u6362\u4e3a')
good=r'$ab^2\det(e_1,\ldots,e_{j-1},\mathbf1,e_{j+1},\ldots,e_3)=ab^2$'+ '\uff08'+r'$j\in\{1,2,3\}$'+'\uff0c'+r'$\mathbf1=(1,1,1)^T$'+'\uff0c\u5176\u4f59\u5217\u4fdd\u6301\u5bf9\u5e94\u7684\u6807\u51c6\u57fa\u5411\u91cf\uff09'
assert new['solution'].count(bad)==1
new['solution']=new['solution'].replace(bad,good)
new['scene_spec']['steps']=[s.replace(bad,good)for s in new['scene_spec']['steps']]
assert new['scene_spec']['steps'].count('\u6838\u5bf9\u5b8c\u6574\u8bc1\u660e\uff1a'+new['solution'])==1
assert new['problem']==old['problem']and new['answer']==old['answer']and new['id']==old['id']
save('record-before.json',old);save('record-after.json',new)
with (O/'source-before.jsonl').open('xb')as f:f.write(raw)
rows[b['source_line']-1]=new;jl('dataset_eval-candidate.jsonl',rows);target=O/'dataset_eval-candidate.jsonl'
assert len(rows)==300 and [a['id']for a in rows]==[a['id']for a in map(json.loads,raw.decode().splitlines())]
assert [a['id']for a,z in zip(rows,map(json.loads,raw.decode().splitlines()))if a!=z]==[rid]
with (O/'math-changes.patch').open('xb')as f:f.write(''.join(difflib.unified_diff(json.dumps(old,ensure_ascii=False,indent=2).splitlines(True),json.dumps(new,ensure_ascii=False,indent=2).splitlines(True),fromfile='record-before.json',tofile='record-after.json')).encode())
for z in bs:
 if z['group']=='eval':
  z.update(path=target.relative_to(R).as_posix(),source_sha256=sha(target))
  if z['id']==rid:z.update(parent_binding=by[rid],record_sha256=c.dense(new),math_sha256=c.math_digest(new),review='REPAIRED_THIS_BATCH_PENDING_INDEPENDENT_VERIFICATION')
jl('effective-record-bindings.jsonl',bs)
nb=next(x for x in bs if x['id']==rid)
# Consolidate all current eval records into the complete candidate; no extra record or physical overlay duplication.
srcs=read(P/'effective-source-bindings.json')
srcs=[x for x in srcs if x['group']!='eval'];srcs.append({'path':target.relative_to(R).as_posix(),'sha256':sha(target),'bytes':target.stat().st_size,'records':300,'group':'eval','parent_path':source.relative_to(R).as_posix(),'parent_sha256':sha(source),'unchanged_source_bytes':False})
assert len(srcs)==24;save('effective-source-bindings.json',srcs)
sigs=list(map(json.loads,(P/'effective-complete-signatures.jsonl').read_text('utf-8').splitlines()))
for s in sigs:
 if s['id']==rid:s.update(record_sha256=c.dense(new),math_sha256=c.math_digest(new))
jl('effective-complete-signatures.jsonl',sigs)
save('repair-version-binding.json',{'id':rid,'before':b,'after':nb,'parent_delivery_index_sha256':sha(P/'CURRENT_DELIVERY_INDEX.jsonl'),'source_records':300,'selected_core_records':761,'physical_sources':24,'changed_record_ids_this_batch':[rid],'prior_three_repairs_preserved':True,'production':'CLOSED','qualification':'PENDING_INDEPENDENT_VERIFICATION'})
f,loc=n.formula_inventory(new);save('formula-inventory-after.json',{'unique_formulas':f,'source_occurrences':loc})
work=O/'repair-render';work.mkdir(exist_ok=False);scene=work/'scene.py';scene.write_text(h.hd_scene(f,rid),encoding='utf-8',newline='\n');(work/'formula-inventory.json').write_bytes(c.encoded({'unique_formulas':f,'source_occurrences':loc}))
cmd=h.render_command(scene,work/'media');start=time.monotonic_ns();p=subprocess.run(cmd,cwd=work,capture_output=True,timeout=600);(work/'stdout.bin').write_bytes(p.stdout);(work/'stderr.bin').write_bytes(p.stderr)
save('render-execution.json',{'command':cmd,'rc':p.returncode,'elapsed_seconds_exact':str(Fraction(time.monotonic_ns()-start,10**9)),'scene_sha256':sha(scene),'generator_sha256':sha(Path(h.__file__)),'cache_policy':'NEW_CACHE','source_binding':nb})
assert p.returncode==0,p.stderr[-2000:]
vids=list((work/'media').rglob('ConceptScene.mp4'));assert len(vids)==1;g=read(work/'page-geometry.json');frames,count=h.decode_pages(vids[0],work/'pages',len(g['pages']))
save('repair-render-result.json',{'id':rid,'frames':frames,'video_frames':count,'page_count':len(frames),'unique_formulas':len(f),'source_formula_occurrences':len(loc),'record_binding':nb,'mp4_path':vids[0].relative_to(R).as_posix(),'mp4_sha256':sha(vids[0]),'geometry_path':(work/'page-geometry.json').relative_to(R).as_posix(),'geometry_sha256':sha(work/'page-geometry.json'),'formula_inventory_path':(work/'formula-inventory.json').relative_to(R).as_posix(),'formula_inventory_sha256':sha(work/'formula-inventory.json'),'production':'CLOSED'})
print(json.dumps({'status':'RENDERED_NOT_YET_VISUALLY_ACCEPTED','pages':len(frames),'formulas':len(f),'source_sha256':sha(target),'record_sha256':c.dense(new)}))
