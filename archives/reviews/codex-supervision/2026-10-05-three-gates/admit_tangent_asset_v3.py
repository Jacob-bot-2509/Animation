"""Admit one reviewed tangent asset with real media and independent symbolic proof."""
import sys,json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];sys.path[:0]=[str(ROOT),str(ROOT/'src')]
from tools.verified_scene_registry import build_scene
from animtrain.sandbox_execution import render_scene
import sympy as sp
m=ROOT/'data/manifest.json';data=json.loads(m.read_text(encoding='utf-8'));record=None
for e in data['entries']:
 for line in (ROOT/'data'/e['path']).read_text(encoding='utf-8').splitlines():
  row=json.loads(line)
  if row['id']=='calc-derivative-001':record=row;input_hash=hashlib.sha256(line.strip().encode()).hexdigest()
assert record is not None
x=sp.symbols('x');f=x*x;slope=sp.diff(f,x).subs(x,1);tangent=sp.expand(f.subs(x,1)+slope*(x-1))
assert slope==2 and tangent==2*x-1 and sp.diff(f-tangent,x).subs(x,1)==0
assert record['answer']=='$y=2x-1$'
result=render_scene(build_scene(record,input_hash))
report={'id':record['id'],'input_sha256':input_hash,'manifest_sha256':hashlib.sha256(m.read_bytes()).hexdigest(),
 'core_math_checks':{'point':str(f.subs(x,1)),'slope':str(slope),'tangent':str(tangent),'tangency':True},
 'semantic_review':'Reviewed all five scene_spec steps: black marked axes on a light panel; blue parabola; flashing yellow point at (1,1); orange tangent y=2x-1; full white derivative and answer labels stacked at the lower right; tangent extends outwards from the highlighted point; integer axis ticks. No generic geometry.',
 'math':'verified','semantic':'pending_visual_review','render_result':result}
out=Path(__file__).with_name('tangent-asset-native-v3.json');out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('render',result['ok'],result.get('detail'),flush=True)
if result['ok']:
 import av
 with av.open(result['output']['path']) as c:
  frames=list(c.decode(video=0))
  frames[-1].to_image().save(out.with_name('tangent-final-frame-v3.png'))
else:sys.exit(1)
