"""Bound single-record repair: frozen parent preserved; actual native 4K pages."""
from pathlib import Path
import json,sys,copy,difflib,subprocess,time
from fractions import Fraction
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'))
import core_signatures as c, native_render_pilot as n, hd_formula_pages as h
def save(name,v):
 with (O/name).open('xb') as f:f.write(c.encoded(v))
def sha(p):return c.digest(p.read_bytes())
B=R/'reviews/codex-supervision/2026-10-07-deep-isolation-followup/effective-core-v3'
bindings=c.load_record_bindings();by={b['id']:b for b in bindings};rid='eval-calc-030-s3'
old=c.load_record(by,rid);new=copy.deepcopy(old)
bad=r'\pi^2y-2\pi\int_0^1\arcsin y'
good=r'\pi^2-2\pi\int_0^1\arcsin y'
assert new['solution'].count(bad)==1
new['solution']=new['solution'].replace(bad,good).replace('\u6c34\u5e73\u5706\u76d8','\u6c34\u5e73\u5706\u73af').replace('\u5706\u76d8\u5916\u534a\u5f84','\u5706\u73af\u5916\u534a\u5f84')
new['scene_spec']['steps']=[x.replace(bad,good).replace('\u6c34\u5e73\u5706\u76d8','\u6c34\u5e73\u5706\u73af').replace('\u5706\u76d8\u5916\u534a\u5f84','\u5706\u73af\u5916\u534a\u5f84') for x in new['scene_spec']['steps']]
assert new['problem']==old['problem'] and new['answer']==old['answer'] and new['id']==old['id']
assert new['scene_spec']['steps'].count('\u6838\u5bf9\u5b8c\u6574\u8bc1\u660e\uff1a'+new['solution'])==1
assert bad not in json.dumps(new,ensure_ascii=False)
save('record-before.json',old);save('record-after.json',new)
source=R/by[rid]['path'];raw=source.read_bytes();assert sha(source)==by[rid]['source_sha256']
with (O/'source-before.jsonl').open('xb')as f:f.write(raw)
lines=raw.decode('utf-8').splitlines(keepends=True);line=by[rid]['source_line']-1
assert json.loads(lines[line])==old
lines[line]=json.dumps(new,ensure_ascii=False,separators=(',',':'))+'\n'
after=''.join(lines).encode('utf-8');target=O/'dataset_eval-candidate.jsonl'
with target.open('xb')as f:f.write(after)
a=[json.loads(x)for x in raw.decode('utf-8').splitlines()];b=[json.loads(x)for x in after.decode('utf-8').splitlines()]
assert len(a)==len(b)==300 and [r['id']for r in a]==[r['id']for r in b]
assert [x['id']for x,y in zip(a,b)if x!=y]==[rid]
patch=''.join(difflib.unified_diff(json.dumps(old,ensure_ascii=False,indent=2).splitlines(True),json.dumps(new,ensure_ascii=False,indent=2).splitlines(True),fromfile='record-before.json',tofile='record-after.json'))
with (O/'math-changes.patch').open('xb')as f:f.write(patch.encode('utf-8'))
nb=copy.deepcopy(by[rid]);nb.update(path=target.relative_to(R).as_posix(),source_sha256=sha(target),record_sha256=c.dense(new),math_sha256=c.math_digest(new))
nb['parent_binding']=by[rid];nb['repair_review']='THIS_BATCH_PENDING_INDEPENDENT_VERIFICATION'
for i,v in enumerate(bindings):
 if v['id']==rid:bindings[i]=nb
with(O/'current-record-bindings.jsonl').open('xb')as f:
 for v in bindings:f.write((json.dumps(v,ensure_ascii=False,sort_keys=True)+'\n').encode())
save('repair-version-binding.json',{'id':rid,'before':by[rid],'after':nb,'parent_core_manifest_sha256':c.CORE_MANIFEST_SHA256,'changed_records':1,'source_records':300,'core_records':len(bindings),'production':'CLOSED'})
formulas,loc=n.formula_inventory(new);save('formula-inventory-after.json',{'unique_formulas':formulas,'source_occurrences':loc})
work=O/'repair-render';work.mkdir(exist_ok=False)
scene=work/'scene.py';scene.write_text(h.hd_scene(formulas,rid),encoding='utf-8',newline='\n')
(work/'formula-inventory.json').write_bytes(c.encoded({'unique_formulas':formulas,'source_occurrences':loc}))
cmd=h.render_command(scene,work/'media');start=time.monotonic_ns()
p=subprocess.run(cmd,cwd=work,capture_output=True,timeout=600)
(work/'stdout.bin').write_bytes(p.stdout);(work/'stderr.bin').write_bytes(p.stderr)
save('render-execution.json',{'command':cmd,'rc':p.returncode,'elapsed_seconds_exact':str(Fraction(time.monotonic_ns()-start,10**9)),'source_binding':nb,'scene_sha256':sha(scene),'generator_sha256':sha(Path(h.__file__)),'cache_policy':'NEW_CACHE_NO_INHERITED_FORMULA_CLAIMS'})
assert p.returncode==0,p.stderr[-2000:]
videos=list((work/'media').rglob('ConceptScene.mp4'));assert len(videos)==1
g=json.loads((work/'page-geometry.json').read_text('utf-8'))
frames,count=h.decode_pages(videos[0],work/'pages',len(g['pages']))
save('repair-render-result.json',{'id':rid,'status':'PASS_BOUND_NATIVE_4K_RENDER_ONLY','frames':frames,'video_frames':count,'page_count':len(frames),'unique_formulas':len(formulas),'source_formula_occurrences':len(loc),'record_binding':nb,'mp4_path':videos[0].relative_to(R).as_posix(),'mp4_sha256':sha(videos[0]),'geometry_path':(work/'page-geometry.json').relative_to(R).as_posix(),'geometry_sha256':sha(work/'page-geometry.json'),'formula_inventory_path':(work/'formula-inventory.json').relative_to(R).as_posix(),'formula_inventory_sha256':sha(work/'formula-inventory.json'),'production':'CLOSED'})
print(json.dumps({'status':'PASS_BOUND_NATIVE_4K_RENDER_ONLY','pages':len(frames),'source_sha256':nb['source_sha256'],'record_sha256':nb['record_sha256'],'math_sha256':nb['math_sha256']}))
