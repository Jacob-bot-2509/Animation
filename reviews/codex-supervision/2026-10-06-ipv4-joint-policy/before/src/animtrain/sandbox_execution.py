"""AppContainer production transport; acceptance is separate from availability.

No host-process fallback. Parent-owned token evidence is captured before resume.
Each job receives a fresh profile, private writable caches and temporary read grants.
Joint acceptance is still separate from transport availability.
"""
from __future__ import annotations
import hashlib
import json
import subprocess
import sys
import uuid
import shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
WORK_ROOT = ROOT / 'reviews/codex-supervision/2026-10-05-three-gates'
CERTIFICATE = ROOT / 'data/execution_evidence.json'
BOUND_FILES = ('src/animtrain/sandbox_execution.py', 'src/animtrain/render_gate.py',
               'src/animtrain/appcontainer.py', 'src/animtrain/network_isolation.py',
               'src/animtrain/win_job.py', 'src/animtrain/private_profile.py', 'src/animtrain/isolation_evidence.py', 'src/animtrain/full_surface_evidence.py', 'src/animtrain/net_guard.py', 'reviews/2026-10-06-exec-isolation-full-surface/surface_probe_contract.py', 'tools/sandbox_surface_acceptance.py', 'reviews/codex-supervision/2026-10-06-all43-sandbox-repair/host_cases.py', '.sandbox-runtime/miktex-real/miktex/config/miktexstartup.ini', '.sandbox-runtime/miktex-environment.json',
               '.venv/Scripts/python.exe')
REQUIRED_CASES = ('render_formula', 'render_chinese', 'file_read_outside',
                  'file_write_outside', 'file_write_runtime', 'cross_run_write', 'cross_run_cache_write',
                  'tcp_loopback_v4', 'tcp_loopback_v6', 'udp_loopback_v4',
                  'udp_loopback_v6', 'tcp_external_v4', 'tcp_external_v6',
                  'timeout_tree', 'root_exit_tree', 'memory_limit')


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check_certificate(path=None):
    """Recompute every native boundary and bind the exact current transport."""
    try:
        evidence = json.loads(Path(path or CERTIFICATE).read_text(encoding='utf-8'))
        if evidence.get('schema')!='production-appcontainer-v2' or evidence.get('fs_isolation')!='private_per_run':
            raise ValueError('Unsupported/partial acceptance contract')
        current={n:digest(ROOT/n) for n in BOUND_FILES}
        if evidence.get('implementation_sha256')!=current:
            raise ValueError('Backend/runtime bindings changed')
        raw_path=Path(evidence['raw_path']).resolve()
        if not raw_path.is_relative_to(WORK_ROOT) or digest(raw_path)!=evidence['raw_sha256']:
            raise ValueError('Native evidence changed/missing')
        raw=json.loads(raw_path.read_text(encoding='utf-8'))
        if raw.get('implementation_sha256')!=current:
            raise ValueError('Native run does not bind current production transport')
        from .isolation_evidence import judge
        results=judge(raw,digest,decode_video)
        if set(results)!=set(REQUIRED_CASES) or any(v!='PASS' for v in results.values()):
            raise ValueError('Incomplete joint acceptance')
        from .full_surface_evidence import require_complete_surface
        require_complete_surface(evidence)
        return True, '生产 AppContainer 43项及联合验收通过(仅限已登记的端点、文件和进程边界)'
    except Exception as exc:
        return False, '生产隔离尚未联合验收: '+str(exc)


def runtime_env(work):
    env = json.loads((ROOT/'.sandbox-runtime/miktex-environment.json').read_text(encoding='utf-8'))
    allowed = {'PATHEXT','SYSTEMDRIVE','SYSTEMROOT','USERDOMAIN','USERNAME','WINDIR',
               'ANIMTRAIN_MIKTEX_STATE','PATH','APPDATA','LOCALAPPDATA','USERPROFILE','TEMP','TMP'}
    if set(env)-allowed or any(not isinstance(v,str) for v in env.values()):
        raise ValueError('Runtime environment is not the reviewed allowlist')
    env['PATH'] = str(ROOT/'.venv/Scripts')+';D:/Python;'+env['PATH']
    env.update(TEMP=str(work),TMP=str(work),MPLCONFIGDIR=str(work/'mpl'),
               PYTHONDONTWRITEBYTECODE='1')
    from .net_guard import network_isolation_env
    return network_isolation_env(env,work/'shim')


from .net_guard import NETWORK_SHIM

TEX_BOOTSTRAP = NETWORK_SHIM + r"""
import runpy,sys
from manim.utils import tex_file_writing as _tw
_original = _tw.make_tex_compilation_command
def _command(compiler, output_format, tex_file, tex_dir):
    if compiler != 'latex':
        raise ValueError('Only reviewed latex compiler is permitted')
    command = _original(compiler, output_format, tex_file, tex_dir)
    command[1:1] = ['-disable-installer','-disable-write18']
    return command
_tw.make_tex_compilation_command = _command
runpy.run_module('manim', run_name='__main__', alter_sys=True)
"""


def run_code(code, *, mode='render', timeout_ms=300000, python=None, prepare_probe=None):
    """Internal transport for reviewed fixed probes and scenes, never host exec.

    External generated scenes must enter through render_gate.render_check.
    run_appcontainer verifies the suspended child's token from the parent.
    """
    from . import appcontainer as ac
    if sys.platform != 'win32':
        raise OSError('No reviewed OS backend on this platform; host fallback disabled')
    if not isinstance(code,str) or not code.strip() or len(code)>1000000:
        raise ValueError('Invalid scene source')
    if mode not in ('render','probe') or type(timeout_ms) is not int or not 1<=timeout_ms<=300000:
        raise ValueError('Invalid transport mode/timeout')
    if prepare_probe is not None and (mode!='probe' or not callable(prepare_probe)):
        raise ValueError('Fixture setup is allowed only for reviewed fixed probes')
    py = (ROOT/'.venv/Scripts/python.exe').resolve()
    if python is not None and Path(python).resolve()!=py:
        raise ValueError('Unreviewed Python executable')
    work = WORK_ROOT/('execution-'+uuid.uuid4().hex)
    work.mkdir(parents=True,exist_ok=False)
    scene = work/'scene.py';scene.write_text(code,encoding='utf-8')
    env = runtime_env(work)
    runtime = ROOT/'.sandbox-runtime/miktex-real'
    state = ROOT/'.sandbox-runtime/miktex-state'
    if not runtime.is_dir() or not state.is_dir():
        raise FileNotFoundError('Reviewed local MiKTeX copy/configuration absent')
    if mode == 'render':
        bootstrap=work/'bootstrap.py';bootstrap.write_text(TEX_BOOTSTRAP,encoding='utf-8')
        command=[str(py),'-I','-B',str(bootstrap),'render','-ql','--format=mp4',
                 '--media_dir',str(work/'media'),str(scene),'ConceptScene']
    else:
        command=[str(py),'-I','-B',str(scene)]
    from .private_profile import isolated_profile
    private_state=work/'state'
    shutil.copytree(state/'config',private_state/'config')
    shutil.copytree(state/'data',private_state/'data')
    (private_state/'profile').mkdir()
    env.update(ANIMTRAIN_MIKTEX_STATE=str(private_state.relative_to(Path('D:/'))),APPDATA=str(private_state/'profile'),LOCALAPPDATA=str(private_state/'profile'),USERPROFILE=str(private_state/'profile'))
    grants=[(Path(r'D:\Python'),False),(ROOT/'.venv',False),(runtime,False),(work,True)]
    if prepare_probe is not None:
        prepare_probe(work)
        if scene.read_text(encoding='utf-8')!=code:
            raise ValueError('Probe fixture setup changed executable source')
    try:
        with isolated_profile(grants) as (profile_name,profile_evidence):
            cp=ac.run_appcontainer(command,cwd=work,env=env,allowed_dirs=[],
                                  timeout_ms=timeout_ms,verify_identity=True,profile_name=profile_name)
    except subprocess.TimeoutExpired as exc:
        if hasattr(exc,'parent_evidence'):
            exc.parent_evidence['private_profile']=profile_evidence
        exc.work=str(work)
        (work/'stdout.txt').write_bytes(exc.output or b'')
        (work/'stderr.txt').write_bytes(exc.stderr or b'')
        raise
    cp.parent_evidence['private_profile']=profile_evidence
    (work/'stdout.txt').write_bytes(cp.stdout);(work/'stderr.txt').write_bytes(cp.stderr)
    evidence=getattr(cp,'parent_evidence',None)
    if not isinstance(evidence,dict) or evidence.get('job_assigned_before_resume') is not True or evidence.get('tree_stopped') is not True:
        raise OSError('Parent process/job evidence missing; refusing success')
    return {'rc':cp.returncode,'stdout':cp.stdout.decode('utf-8','replace'),
            'stderr':cp.stderr.decode('utf-8','replace'),'work':str(work),
            'source_sha256':digest(scene),'command':command,'parent_evidence':evidence}


def decode_video(path):
    import av
    count=0;size=None
    with av.open(str(path)) as container:
        if len(container.streams.video)!=1:
            raise ValueError('Exactly one video stream required')
        rate=str(container.streams.video[0].average_rate)
        for frame in container.decode(video=0):
            count+=1;size=(frame.width,frame.height)
    if not count or not size or min(size)<=0:
        raise ValueError('No decoded video frames')
    return {'path':str(path),'sha256':digest(path),'size':path.stat().st_size,
            'frames':count,'width':size[0],'height':size[1],'frame_rate':rate}


def render_scene(code, python=None):
    try:
        result=run_code(code,python=python)
        isolation={'backend':'windows_appcontainer','shell':False,
                   'memory_limit_mb':2048,'job_assigned':True,
                   'network_isolated':False,'network_evidence':'43-point acceptance required','fs_isolation':'private_per_run',
                   'parent_evidence':result['parent_evidence']}
        if result['rc']!=0:
            return {'ok':False,'status':'failed','detail':result['stderr'][-1500:],
                    'unverified':[],'transport':result,'isolation':isolation}
        outputs=[p for p in Path(result['work']).rglob('ConceptScene.mp4')
                 if 'partial_movie_files' not in p.parts]
        if len(outputs)!=1:
            raise ValueError('Exactly one final ConceptScene.mp4 required; exit 0 alone is not a render')
        artifact=decode_video(outputs[0])
        return {'ok':True,'status':'rendered','detail':'AppContainer 真实渲染并完整解码',
                'unverified':[],'output':artifact,'transport':result,'isolation':isolation}
    except subprocess.TimeoutExpired as exc:
        return {'ok':False,'status':'timeout','detail':str(exc),'unverified':[]}
    except Exception as exc:
        return {'ok':False,'status':'exec_error','detail':str(exc),
                'unverified':['render_isolation']}
