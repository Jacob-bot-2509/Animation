from pathlib import Path
import json,sys,subprocess,time
from fractions import Fraction
R=Path(__file__).resolve().parents[3];O=Path(__file__).resolve().parent
sys.path.insert(0,str(R/'tools'))
import core_signatures as c,native_render_pilot as n,hd_formula_pages as h
def read(p):return json.loads(p.read_text('utf-8'))
def sha(p):return c.digest(p.read_bytes())
def save(p,v):p.write_bytes(c.encoded(v))
qs={q['id']:q for q in read(O/'repaired-records-after.json')};bs={b['id']:b for b in map(json.loads,(O/'current-record-bindings.jsonl').read_text('utf-8').splitlines())}
results=[]
for rid in read(O/'render-plan.json')['rerender_ids']:
 work=O/'repair-render'/rid
 if (work/'receipt.json').exists():
  receipt=read(work/'receipt.json');assert receipt['rc']==0;results.append(receipt);continue
 work.mkdir(parents=True,exist_ok=False);q=qs[rid];f,loc=n.formula_inventory(q);save(work/'formula-inventory.json',{'unique_formulas':f,'source_occurrences':loc})
 scene=work/'scene.py';scene.write_text(h.hd_scene(f,rid),encoding='utf-8',newline='\n');cmd=h.render_command(scene,work/'media')
 start=time.monotonic_ns();p=subprocess.run(cmd,cwd=work,capture_output=True,timeout=600);(work/'stdout.bin').write_bytes(p.stdout);(work/'stderr.bin').write_bytes(p.stderr)
 assert p.returncode==0,(rid,p.stderr[-2500:])
 vids=list((work/'media').rglob('ConceptScene.mp4'));assert len(vids)==1;g=read(work/'page-geometry.json');frames,count=h.decode_pages(vids[0],work/'pages',len(g['pages']))
 receipt={'id':rid,'rc':p.returncode,'elapsed_seconds_exact':str(Fraction(time.monotonic_ns()-start,10**9)),'command':cmd,'generator_sha256':sha(Path(h.__file__)),'scene_sha256':sha(scene),'record_binding':bs[rid],'unique_formulas':len(f),'source_formula_occurrences':len(loc),'frames':frames,'page_count':len(frames),'video_frames':count,'mp4_path':vids[0].relative_to(R).as_posix(),'mp4_sha256':sha(vids[0]),'geometry_path':(work/'page-geometry.json').relative_to(R).as_posix(),'geometry_sha256':sha(work/'page-geometry.json'),'formula_inventory_path':(work/'formula-inventory.json').relative_to(R).as_posix(),'formula_inventory_sha256':sha(work/'formula-inventory.json'),'visual_acceptance':'PENDING_ACTUAL_IMAGE_REVIEW','production':'CLOSED'}
 save(work/'receipt.json',receipt);results.append(receipt);save(O/'render-execution.json',results);print(json.dumps({'id':rid,'pages':len(frames),'done':len(results)}),flush=True)
save(O/'render-execution.json',results)
print(json.dumps({'rendered_records':len(results),'pages':sum(z['page_count']for z in results)}),flush=True)
