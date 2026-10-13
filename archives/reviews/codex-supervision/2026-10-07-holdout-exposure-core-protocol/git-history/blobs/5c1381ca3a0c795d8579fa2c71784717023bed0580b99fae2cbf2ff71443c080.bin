"""Repaired v2 probe runner. Scoped observations never open the production gate."""
from __future__ import annotations
import argparse
import ast
import ctypes
import json
import os
import shutil
import socket
import sys
import time
import uuid
from pathlib import Path
from surface_probe_contract import (ROOT, HERE, POINTS, Receiver, WIN32_SOURCE,
    classify_delivery, classify_permission, digest, host_control,
    save_exclusive, validate_transport)

sys.path.insert(0, str(ROOT / 'src'))

ERROR_SOURCE = r'''
def failure(exc):
    number=getattr(exc,'winerror',None)
    return {'outcome':'os_denied' if number in (5,10013) else 'error',
            'winerror':number,'errno':getattr(exc,'errno',None),
            'error_type':type(exc).__name__,'detail':str(exc)}
'''


def build_udp_code(endpoints):
    code = 'import json,_socket,time\nr={}\ntargets=' + repr(endpoints) + '\n'
    code += ERROR_SOURCE + r'''
for name,item in targets.items():
    sock=None;started=time.monotonic_ns()
    try:
        sock=_socket.socket(item['family'],_socket.SOCK_DGRAM)
        sock.sendto(item['nonce'].encode('ascii'),tuple(item['endpoint']))
        r[name]={'outcome':'sent'}
    except OSError as exc:r[name]=failure(exc)
    finally:
        if sock is not None:sock.close()
    r[name]['elapsed_ns']=time.monotonic_ns()-started
print(json.dumps(r),flush=True)
'''
    ast.parse(code)
    return code


def build_exe_code(config):
    code = 'import json,subprocess,_socket,os,pathlib,winreg\nr={}\nconfig=' + repr(config) + '\n'
    code += ERROR_SOURCE + r'''
for name,args in config['commands'].items():
    try:
        cp=subprocess.run(args,capture_output=True,text=True,timeout=10)
        r[name]={'outcome':'completed','rc':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr}
    except Exception as exc:r[name]=failure(exc)
try:
    pathlib.Path(config['victim']).unlink();r['delete_owned_host_fixture']={'outcome':'allowed'}
except OSError as exc:r['delete_owned_host_fixture']=failure(exc)
try:
    cp=subprocess.run([config['cmd'],'/c','mklink','/J','escape',config['fixture']],capture_output=True,text=True,timeout=10)
    r['junction_setup']={'rc':cp.returncode,'stdout':cp.stdout,'stderr':cp.stderr}
    link=pathlib.Path('escape')
    target=os.readlink(link) if cp.returncode==0 and link.is_junction() else None
    normalize=lambda value:os.path.normcase(os.path.abspath(value.removeprefix('\\\\?\\')))
    valid=target is not None and normalize(target)==normalize(config['fixture'])
    r['junction_setup']['verified_target']=valid
    if valid:
        try:
            with (link/'escaped-marker.txt').open('x',encoding='utf-8') as stream:stream.write(config['nonce'])
            r['junction_write']={'outcome':'allowed'}
        except OSError as exc:r['junction_write']=failure(exc)
    else:r['junction_write']={'outcome':'not_tested','reason':'Verified junction fixture absent'}
except Exception as exc:r['junction_setup']=failure(exc);r['junction_write']={'outcome':'not_tested'}
raw=None
try:
    raw=_socket.socket(_socket.AF_INET,_socket.SOCK_RAW,_socket.IPPROTO_ICMP)
    r['raw_socket']={'outcome':'created','reason':'Creation alone does not test ICMP delivery'}
except OSError as exc:r['raw_socket']=failure(exc)
finally:
    if raw is not None:raw.close()
try:
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER,config['registry_key'],0,winreg.KEY_SET_VALUE) as key:
        winreg.SetValueEx(key,'nonce',0,winreg.REG_SZ,config['nonce'])
    r['host_registry_write']={'outcome':'allowed'}
except OSError as exc:r['host_registry_write']=failure(exc)
print(json.dumps(r),flush=True)
'''
    ast.parse(code)
    return code


def build_ipc_code(targets):
    code = WIN32_SOURCE + '\nimport json\nr={}\ntargets=' + repr(targets) + '\n'
    code += r'''
kernel=bind_kernel32()
for kind,name in targets.items():
    ctypes.set_last_error(0)
    if kind=='mapping':handle=kernel.OpenFileMappingW(6,False,name)
    else:handle=kernel.CreateFileW(name,0xC0000000 if kind=='pipe' else 0x40000000,0,None,3,0,None)
    number=ctypes.get_last_error()
    if invalid_handle(handle):
        r[kind]={'outcome':'os_denied' if number==5 else 'error','winerror':number}
    else:
        r[kind]={'outcome':'allowed','winerror':None};kernel.CloseHandle(handle)
r['clipboard']={'outcome':'not_tested','reason':'Dedicated isolated clipboard fixture required; user clipboard untouched'}
r['window_messages_and_hooks']={'outcome':'not_tested','reason':'ABI declared, but independently healthy isolated UI fixture required'}
print(json.dumps(r),flush=True)
'''
    ast.parse(code)
    return code


def source_bindings():
    from animtrain.sandbox_execution import BOUND_FILES
    relative = tuple(BOUND_FILES) + tuple(str(f.relative_to(ROOT)).replace('\\','/') for f in HERE.glob('*.py'))
    return {name:digest(ROOT/name) for name in relative}


def capture(report, code):
    from animtrain.sandbox_execution import run_code
    report['generated_source'] = code
    report['generated_source_canonical_sha256'] = __import__('hashlib').sha256(code.encode('utf-8')).hexdigest()
    transport = run_code(code, mode='probe', timeout_ms=90000)
    report['transport'] = transport  # Full, unmodified return; no stripping or truncation.
    work = Path(transport['work'])
    report['raw_streams'] = {name:{'path':str(work/(name+'.txt')),
        'raw_sha256':digest(work/(name+'.txt')),'bytes':(work/(name+'.txt')).stat().st_size}
        for name in ('stdout','stderr')}
    observations = validate_transport(transport, code)
    report['observations'] = observations
    report['transport_verified'] = True
    return observations


def phases():
    return {phase:uuid.uuid4().hex for phase in ('before','sandbox','after')}


def receive_summary(receiver, nonces, started, state):
    return {'endpoint':receiver.endpoint,'nonces':nonces,'packets':receiver.packets,
        'complete':receiver.complete,'errors':receiver.errors,
        'observation_ns':time.monotonic_ns()-started,
        'verdict':classify_delivery(state,receiver.packets,nonces,receiver.complete,time.monotonic_ns()-started)}


def observe_until(started):
    deadline=started+20_000_000_000
    while time.monotonic_ns()<deadline:time.sleep(min(1,(deadline-time.monotonic_ns())/1_000_000_000))


def run_udp(report):
    receivers={};targets={};nonces={};started=time.monotonic_ns()
    try:
        for name,family in (('owned_loopback_udp_v4',socket.AF_INET),('owned_loopback_udp_v6',socket.AF_INET6)):
            try:
                receiver=Receiver('udp',family);receivers[name]=receiver;nonces[name]=phases()
                report['controls'][name]={'before':host_control(receiver,nonces[name]['before'])}
                targets[name]={'family':family,'endpoint':receiver.endpoint,'nonce':nonces[name]['sandbox']}
            except OSError as exc:report['fixture_errors'][name]={'error_type':type(exc).__name__,'detail':str(exc)}
        if not targets:raise ValueError('No healthy native endpoint fixture')
        observations=capture(report,build_udp_code(targets))
        for name,receiver in receivers.items():report['controls'][name]['after']=host_control(receiver,nonces[name]['after'])
        observe_until(started)
    finally:
        for receiver in receivers.values():receiver.close()
    for name,receiver in receivers.items():report['scoped_results'][name]=receive_summary(receiver,nonces[name],started,observations.get(name,{}))
    # These are intentionally untested; a host-local NIC is not a separate LAN peer.
    report['required_fixtures']=['controlled external IPv4/IPv6 receiver with exact nonce controls','independent LAN peer','controlled uncached DNS endpoint/capture']


def run_exe(report):
    import winreg
    fixture=HERE/('owned-fixture-'+report['run_id']);fixture.mkdir(exist_ok=False)
    victim=fixture/'victim.txt';victim.write_text(report['run_id'],encoding='utf-8')
    before_hash=digest(victim)
    receiver=Receiver('http');nonce=phases();started=time.monotonic_ns()
    registry_key='Software\\AnimationModelTraining\\CodexProbes\\'+report['run_id']
    curl=shutil.which('curl.exe');cmd=str(Path(os.environ['SYSTEMROOT'])/'System32/cmd.exe')
    commands={}
    if curl:commands['curl_native']=[curl,'--noproxy','*','-sS','--connect-timeout','3','--max-time','5','-o','NUL',f'http://127.0.0.1:{receiver.endpoint[1]}/{nonce["sandbox"]}']
    else:report['fixture_errors']['curl_native']={'reason':'Executable unavailable; no network inference'}
    if curl:report['executable_bindings']={curl:digest(curl)}
    registry_created=False
    try:
        with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER,registry_key,0,winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key,'nonce',0,winreg.REG_SZ,'before-'+report['run_id'])
        registry_created=True
        report['controls']['owned_http']={'before':host_control(receiver,nonce['before'])}
        observations=capture(report,build_exe_code({'commands':commands,'fixture':str(fixture),'victim':str(victim),'nonce':report['run_id'],'cmd':cmd,'registry_key':registry_key}))
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,registry_key) as key:registry_after=winreg.QueryValueEx(key,'nonce')[0]
        report['controls']['owned_http']['after']=host_control(receiver,nonce['after'])
        observe_until(started)
        report['scoped_results']['host_registry_fixture']={'host_value_unchanged':registry_after=='before-'+report['run_id'],
            'verdict':'FAIL' if registry_after==report['run_id'] else classify_permission(observations.get('host_registry_write',{}),True)}
    finally:
        receiver.close()
        if registry_created:winreg.DeleteKey(winreg.HKEY_CURRENT_USER,registry_key)  # Only this newly owned leaf.
    report['scoped_results']['curl_owned_http']=receive_summary(receiver,nonce,started,observations.get('curl_native',{}))
    exists=victim.exists()
    report['scoped_results']['delete_owned_host_fixture']={'exists':exists,'unchanged':exists and digest(victim)==before_hash,
        'verdict':classify_permission(observations.get('delete_owned_host_fixture',{}),exists and digest(victim)==before_hash)}
    marker=fixture/'escaped-marker.txt'
    setup=observations.get('junction_setup',{})
    report['scoped_results']['junction_write']={'verified_junction':setup.get('verified_target') is True,'marker_exists':marker.exists(),
        'verdict':'FAIL' if marker.exists() else classify_permission(observations.get('junction_write',{}),setup.get('verified_target') is True)}
    report['scoped_results']['raw_socket']={'observation':observations.get('raw_socket',{}),'verdict':'UNKNOWN','reason':'ICMP transmit/receive not verified by creating a socket'}
    report['required_fixtures']=['independent LAN and external non-Python receivers','healthy ICMP receive controls','bidirectional shared-memory fixture']


def run_ipc(report):
    env={};exec(WIN32_SOURCE,env);kernel=env['bind_kernel32']();invalid=env['invalid_handle'];sentinel=env['INVALID_HANDLE_VALUE']
    handles={};targets={};health={}
    names={'pipe':'\\\\.\\pipe\\AnimTrainCodex-'+report['run_id'],
           'mailslot':'\\\\.\\mailslot\\AnimTrainCodex-'+report['run_id'],
           'mapping':'Global\\AnimTrainCodex-'+report['run_id']}
    def open_control(kind,name):
        ctypes.set_last_error(0)
        handle=kernel.OpenFileMappingW(6,False,name) if kind=='mapping' else kernel.CreateFileW(name,0xC0000000 if kind=='pipe' else 0x40000000,0,None,3,0,None)
        number=ctypes.get_last_error();ok=not invalid(handle)
        if ok:kernel.CloseHandle(handle)
        if kind=='pipe':kernel.DisconnectNamedPipe(handles[kind]);kernel.ConnectNamedPipe(handles[kind],None)
        return {'opened':ok,'winerror':None if ok else number}
    try:
        for kind,name in names.items():
            ctypes.set_last_error(0)
            if kind=='pipe':handle=kernel.CreateNamedPipeW(name,3,7,1,4096,4096,100,None)
            elif kind=='mailslot':handle=kernel.CreateMailslotW(name,4096,100,None)
            else:handle=kernel.CreateFileMappingW(sentinel,None,4,0,4096,name)
            number=ctypes.get_last_error()
            if invalid(handle):report['fixture_errors'][kind]={'winerror':number,'reason':'Host fixture creation failed; UNKNOWN'};continue
            handles[kind]=handle;targets[kind]=name
            if kind=='pipe':kernel.ConnectNamedPipe(handle,None)
            health[kind]={'before':open_control(kind,name)}
        if not targets:raise ValueError('No live, owned IPC fixtures')
        observations=capture(report,build_ipc_code(targets))
        for kind,name in targets.items():
            health[kind]['after']=open_control(kind,name)
            healthy=health[kind]['before']['opened'] and health[kind]['after']['opened']
            report['scoped_results'][kind]={'controls':health[kind],'lifetime':'host handle held throughout child operation',
                'verdict':classify_permission(observations.get(kind,{}),healthy)}
    finally:
        for handle in handles.values():kernel.CloseHandle(handle)
    report['required_fixtures']=['bidirectional data nonce/receiver controls for all IPC namespaces','dedicated isolated clipboard session','independently healthy hidden-window and global-hook fixture','WinHTTP/WinINET controlled receiver','ICMP transmit/receive controls']


def main(mode, argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute-native',action='store_true',help='Run only the explicitly owned, bounded fixtures; never accept the full surface')
    args=parser.parse_args(argv)
    run_id=uuid.uuid4().hex
    report={'schema':'exec-surface-bounded-probe-v2','probe':mode,'run_id':run_id,
        'status':'UNVERIFIED','production_gate':'CLOSED','certificate_written':False,
        'full_surface_accepted':False,'native_executed':False,'transport_verified':False,
        'safety_points':{point:'UNKNOWN' for point in POINTS[mode]},'controls':{},
        'fixture_errors':{},'scoped_results':{},'clipboard_accessed':False}
    if not args.execute_native:
        report['reason']='Plan only. Native fixtures require explicit --execute-native; no original evidence overwritten.'
        print(json.dumps(report,ensure_ascii=False,indent=2));return 3
    before=source_bindings();report['implementation_before']=before
    try:
        report['native_executed']=True
        {'udp':run_udp,'exe':run_exe,'ipc':run_ipc,'ipc4':run_ipc}[mode](report)
    except BaseException as exc:
        report['error']={'error_type':type(exc).__name__,'detail':str(exc)}
        # Preserve full timeout/parent data if native transport raises.
        parent=getattr(exc,'parent_evidence',None)
        if parent is not None:report['exception_parent_evidence']=parent
        for name in ('output','stderr'):
            value=getattr(exc,name,None)
            if value is not None:report['exception_'+name+'_hex']=value.hex() if isinstance(value,bytes) else value
    finally:
        after=source_bindings();report['implementation_after']=after
        report['implementation_unchanged']=before==after
        if any(row.get('verdict')=='FAIL' for row in report['scoped_results'].values()):report['status']='SCOPED_FAILURE'
        if before!=after:report['status']='INVALID_SOURCE_CHANGED'
        out=HERE/(f'probe-{mode}-v2-{run_id}-results.json');save_exclusive(out,report)
    print(json.dumps({'path':str(out),'status':report['status'],'production_gate':'CLOSED'},ensure_ascii=False))
    return 2 if report['status'] in ('SCOPED_FAILURE','INVALID_SOURCE_CHANGED') else 3