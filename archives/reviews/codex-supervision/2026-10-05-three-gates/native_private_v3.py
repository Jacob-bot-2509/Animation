import sys,json,pathlib,time,socket
ROOT=pathlib.Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT/'src'))
from animtrain.render_gate import render_check
from animtrain.sandbox_execution import run_code
out=pathlib.Path(__file__).parent
report={'production_gate':'CLOSED','records':[]}
def save(name,result):
 report['records'].append({'name':name,'result':result})
 (out/'native-private-v3-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 print(name,result.get('ok',result.get('rc')),result.get('status',''),flush=True)
for name,body in [('render_formula','self.add(MathTex(r"x^2+y^2=1"))'),('render_chinese','self.add(Text("切线方程", font="Microsoft YaHei",font_size=32))')]:
 code='from manim import *\nclass ConceptScene(Scene):\n    def construct(self):\n        '+body+'\n        self.wait(1/5)\n'
 save(name,render_check(code,trusted=True))
sentinel=out/'host-only-sentinel.txt';sentinel.write_text('private-project-control',encoding='utf-8')
cross=out/'host-private-v3-marker.txt'
old=ROOT/'reviews/codex-supervision/2026-10-05-readiness-completion/pilot-83c6d358b0ea/scene-000/cross-run-private-v3-probe.txt'
# Exact fresh marker in an OLD sandbox directory, never overwrite an old artifact.
assert not old.exists()
code='import pathlib,json,_socket\nresults={}\n'
code+='for name,kind,path in '+repr([('file_read_outside','read',str(sentinel)),('file_write_outside','write',str(cross)),('cross_run_write','write',str(old)),('file_write_runtime','write',str(ROOT/'.sandbox-runtime/miktex-real/production-write-private-v3-probe.txt'))])+':\n'
code+='    try:\n        p=pathlib.Path(path)\n        if kind=="read": p.read_text(encoding="utf-8")\n        else: p.write_text("bounded-acceptance-marker",encoding="utf-8")\n        results[name]={"outcome":"allowed"}\n    except OSError as e: results[name]={"outcome":"denied","winerror":getattr(e,"winerror",None)}\n'
code+='for name,fam,ep in '+repr([('tcp_external_v4',int(socket.AF_INET),('1.1.1.1',443)),('tcp_external_v6',int(socket.AF_INET6),('2606:4700:4700::1111',443,0,0))])+':\n    s=_socket.socket(fam,_socket.SOCK_STREAM);s.settimeout(3)\n    try:\n        s.connect(ep);results[name]={"outcome":"connected"}\n    except OSError as e: results[name]={"outcome":"denied","winerror":getattr(e,"winerror",None)}\n    finally:s.close()\nprint(json.dumps(results),flush=True)\n'
controls={}
for phase in ('before',):
 controls[phase]={}
 for name,fam,ep in [('tcp_external_v4',int(socket.AF_INET),('1.1.1.1',443)),('tcp_external_v6',int(socket.AF_INET6),('2606:4700:4700::1111',443,0,0))]:
  s=socket.socket(fam,socket.SOCK_STREAM);s.settimeout(3)
  try:s.connect(ep);controls[phase][name]='connected'
  except OSError as e:controls[phase][name]=repr(e)
  finally:s.close()
cp=run_code(code,mode='probe');save('file_and_external_network',cp)
controls['after']={}
for name,fam,ep in [('tcp_external_v4',int(socket.AF_INET),('1.1.1.1',443)),('tcp_external_v6',int(socket.AF_INET6),('2606:4700:4700::1111',443,0,0))]:
 s=socket.socket(fam,socket.SOCK_STREAM);s.settimeout(3)
 try:s.connect(ep);controls['after'][name]='connected'
 except OSError as e:controls['after'][name]=repr(e)
 finally:s.close()
report['ordinary_network_controls']=controls
report['marker_paths']=[str(sentinel),str(cross),str(old)]
report['marker_exists_after']={str(p):p.exists() for p in [sentinel,cross,old]}
report['scope']='Transport and named tested boundaries only. Shared writable work/profile/cache prohibit joint acceptance; no certificate issued.'
(out/'native-private-v3-results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
