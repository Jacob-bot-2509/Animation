"""Trusted project-template pilot in AppContainer. No production gate is enabled.
Full video/image decoding is required. Rendering alone does not verify mathematics.
"""
from __future__ import annotations
import argparse,hashlib,inspect,json,os,re,sys,uuid
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT),str(ROOT/'src')]
from animtrain import appcontainer as ac,network_isolation as net
from tools import render_templates as rt
from tools.render_pilot import _picks

TEX_BOOTSTRAP = """
from manim.utils import tex_file_writing as _tex_writing
_original_tex_command = _tex_writing.make_tex_compilation_command
def _sandbox_tex_command(compiler, output_format, tex_file, tex_dir):
    if compiler != 'latex':
        raise ValueError('Sandbox pilot permits only the reviewed latex compiler')
    command = _original_tex_command(compiler, output_format, tex_file, tex_dir)
    command[1:1] = ['-disable-installer', '-disable-write18']
    print('TEX_COMMAND_EVIDENCE=' + json.dumps(command), flush=True)
    return command
_tex_writing.make_tex_compilation_command = _sandbox_tex_command
"""

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def decode_artifact(path:Path,fmt:str)->dict:
    if fmt=='mp4':
        import av
        count=0;size=None
        with av.open(str(path)) as container:
            if len(container.streams.video)!=1:raise ValueError('Exactly one video stream required')
            stream=container.streams.video[0];rate=str(stream.average_rate)
            for frame in container.decode(video=0):
                count+=1;size=(frame.width,frame.height)
        if not count or not size or min(size)<=0:raise ValueError('No decoded frames')
        detail={'frames':count,'width':size[0],'height':size[1],'frame_rate':rate}
    else:
        from PIL import Image
        with Image.open(path) as im:
            if im.format!='PNG':raise ValueError('Not a PNG')
            im.load();detail={'width':im.width,'height':im.height}
            if min(im.size)<=0:raise ValueError('Empty image')
    return {'path':str(path.resolve()),'sha256':sha(path),'bytes':path.stat().st_size,'decoded':True,**detail}

def load_records(manifest:Path,splits:list[str])->list[dict]:
    data=json.loads(manifest.read_text(encoding='utf-8'));records=[]
    for entry in data['entries']:
        if entry['split'] not in splits:continue
        path=(manifest.parent/entry['path']).resolve()
        if not path.is_relative_to(ROOT) or sha(path)!=entry['sha256']:raise ValueError('Input path/hash mismatch')
        for line in path.read_text(encoding='utf-8').splitlines():
            if not line.strip():continue
            rec=json.loads(line);rec['_input_sha256']=hashlib.sha256(line.strip().encode()).hexdigest();records.append(rec)
    if not records:raise ValueError('No current manifest records selected')
    return records

def render_one(rec:dict,work:Path,env:dict,fmt:str,timeout_ms:int)->dict:
    result={'id':rec['id'],'input_sha256':rec['_input_sha256'],'template':rt.route(rec),'math':'UNVERIFIED','ok':False}
    try:
        # Dataset strings only enter reviewed templates. Reject TeX file/shell primitives.
        if re.search(r'\\(?:write|read|openin|openout|input|include|immediate|catcode|csname)\b',rec['problem']+' '+rec['answer']):raise ValueError('Unsafe TeX primitive')
        work.mkdir(parents=True,exist_ok=False);scene=work/'scene.py';source=rt.build_scene(rec)
        # The identity helper is fixed reviewed code, separate from the dataset/template.
        scene.write_text(inspect.getsource(net.token_identity)+"\nimport json\nprint('TOKEN_EVIDENCE='+json.dumps(token_identity()),flush=True)\n"+TEX_BOOTSTRAP+source,encoding='utf-8')
        cmd=[str(ROOT/'.venv/Scripts/python.exe'),'-X','utf8','-B','-m','manim','render','-ql',f'--format={fmt}','--media_dir',str(work/'media'),str(scene),'PilotScene']
        result.update(command=cmd,scene_sha256=sha(scene))
        child_env=dict(env);child_env.update(TEMP=str(work),TMP=str(work),MPLCONFIGDIR=str(work/'mpl'))
        cp=ac.run_appcontainer(cmd,cwd=work,env=child_env,allowed_dirs=[(work,True)],timeout_ms=timeout_ms)
        stdout=cp.stdout.decode('utf-8','replace');stderr=cp.stderr.decode('utf-8','replace');(work/'stdout.txt').write_text(stdout,encoding='utf-8');(work/'stderr.txt').write_text(stderr,encoding='utf-8');result['rc']=cp.returncode
        token=json.loads(next(line.split('=',1)[1] for line in stdout.splitlines() if line.startswith('TOKEN_EVIDENCE=')));result['token']=token
        sid=ac._sid_sddl(ac.appcontainer_sid())
        if cp.returncode!=0:raise ValueError('Manim failed; see stdout/stderr')
        if not(token.get('api_ok') is True and token.get('is_appcontainer') is True and token.get('capability_count')==0 and token.get('sid')==sid):raise ValueError('Invalid AppContainer identity')
        files=[p for p in (work/'media').rglob('*') if p.is_file() and 'partial_movie_files' not in p.parts and ((fmt=='mp4' and p.name=='PilotScene.mp4') or (fmt=='png' and p.suffix=='.png' and p.name.startswith('PilotScene')))]
        if len(files)!=1:raise ValueError('Exactly one final artifact required')
        result.update(output=decode_artifact(files[0],fmt),ok=True)
    except Exception as ex:result['error']=repr(ex)
    return result

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--manifest',type=Path,default=ROOT/'data/manifest.json');parser.add_argument('--splits',nargs='+',choices=['train','eval','test'],default=['eval','test']);parser.add_argument('--limit',type=int,default=8);parser.add_argument('--ids',nargs='+');parser.add_argument('--format',choices=['mp4','png'],default='mp4');parser.add_argument('--timeout-ms',type=int,default=120000);args=parser.parse_args(argv)
    if not 1<=args.limit<=513 or not 1<=args.timeout_ms<=300000:parser.error('limit/timeout out of range')
    manifest=args.manifest.resolve()
    if not manifest.is_relative_to(ROOT):parser.error('Manifest must be in this project')
    records=load_records(manifest,args.splits)
    if args.ids:
        wanted=set(args.ids);records=[r for r in records if r['id'] in wanted]
        if {r['id'] for r in records}!=wanted:parser.error('Requested IDs missing from selected active splits')
    picks=_picks(records,args.limit)
    out=ROOT/'reviews/codex-supervision/2026-10-05-readiness-completion'/('pilot-'+uuid.uuid4().hex[:12]);out.mkdir(parents=True)
    runtime=ROOT/'.sandbox-runtime/miktex-real';state=ROOT/'.sandbox-runtime/miktex-state';env=json.loads((ROOT/'.sandbox-runtime/miktex-environment.json').read_text(encoding='utf-8'));env.update(PATH=str(ROOT/'.venv/Scripts')+';D:/Python;'+env['PATH'],PYTHONDONTWRITEBYTECODE='1')
    ac.grant_dir_access(runtime,ac.appcontainer_sid(),write=False);ac.grant_dir_access(state,ac.appcontainer_sid(),write=True)
    report={'manifest_sha256':sha(manifest),'tool_sha256':sha(Path(__file__)),'template_sha256':sha(Path(rt.__file__)),'format':args.format,'scope':'Actual reviewed templates in AppContainer; no math/semantic/whole-dataset acceptance claim','production_gate':'CLOSED','records':[]}
    for i,rec in enumerate(picks):
        result=render_one(rec,out/f'scene-{i:03d}',env,args.format,args.timeout_ms);report['records'].append(result);(out/'pilot-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({k:result.get(k) for k in ('id','template','ok','rc','error')},ensure_ascii=False),flush=True)
    print('report:',out/'pilot-report.json');return 0 if all(r['ok'] for r in report['records']) else 1
if __name__=='__main__':raise SystemExit(main())
