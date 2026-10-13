"""Recompute production joint results, never trust a JSON PASS flag."""
from __future__ import annotations
import json,re
from pathlib import Path


def _parent(evidence):
    if not isinstance(evidence,dict):raise ValueError('Missing parent evidence')
    token=evidence['token'];profile=evidence['private_profile']
    if not (token['api_ok'] is True and token['is_appcontainer'] is True
            and type(token['capability_count']) is int and token['capability_count']==0
            and token['sid']==profile['sid']
            and re.fullmatch(r'animtrain-job-[0-9a-f]{32}',profile['profile_name'])
            and evidence['memory_limit_mb']==2048
            and evidence['created_suspended'] is True
            and evidence['job_assigned_before_resume'] is True
            and evidence['tree_stopped'] is True and profile['cleanup_complete'] is True):
        raise ValueError('Invalid parent token/job/profile evidence')
    acl=profile['temporary_acl']
    if len(acl)!=4 or any(x['restored'] is not True or x['before_sha256']!=x['after_sha256'] for x in acl):
        raise ValueError('Temporary runtime grants not restored')
    if Path(profile['storage']).exists():raise ValueError('Disposable profile storage still exists')


def _transport(cp,digest):
    _parent(cp['parent_evidence'])
    work=Path(cp['work']);source=work/'scene.py'
    if digest(source)!=cp['source_sha256']:raise ValueError('Probe source changed')
    if '-I' not in cp['command'] or '-B' not in cp['command']:
        raise ValueError('Unreviewed Python flags')


def judge(raw,digest,decode_video):
    """Raw fields and actual file/token/media binding determine every result."""
    if raw.get('complete') is not True or raw.get('implementation_unchanged') is not True:
        raise ValueError('Incomplete/changed native run')
    records=raw['records'];results={}
    for name in ('render_formula','render_chinese'):
        row=records[name];cp=row['transport'];_transport(cp,digest)
        output=row['output'];path=Path(output['path'])
        decoded=decode_video(path)
        if row['ok'] is not True or cp['rc']!=0 or decoded!=output:
            raise ValueError('Render artifact invalid: '+name)
        results[name]='PASS'
    files=records['files'];cp=files['transport'];_transport(cp,digest)
    observed=json.loads(cp['stdout'])
    if cp['rc']!=0 or files['private_before_sha256']!=files['private_after_sha256']:
        raise ValueError('File probe failed')
    for name,kind,path in files['attempts']:
        if observed.get(name)!='denied':raise ValueError('File boundary not denied: '+name)
        if kind=='write' and (files['markers_absent'].get(name) is not True or Path(path).exists()):
            raise ValueError('Outside write marker exists: '+name)
        results[name]='PASS'
    local=records['local_network'];cp=local['transport'];_transport(cp,digest)
    observed=json.loads(cp['stdout'])
    if cp['rc']!=0 or local['receiver_complete'] is not True or local['observation_seconds']<20:
        raise ValueError('Incomplete network receiver/window')
    for name,packets in local['packets'].items():
        values=[bytes.fromhex(p['hex']).decode('ascii') for p in packets]
        expected=[local['nonces'][p][name] for p in ('before','after')]
        if sorted(values)!=sorted(expected) or local['nonces']['sandbox'][name] in values:
            raise ValueError('Missing controls or sandbox delivery: '+name)
        state=observed[name]
        _local_outcome(name,state)
        results[name]='PASS'
    external=records['external_network'];cp=external['transport'];_transport(cp,digest)
    observed=json.loads(cp['stdout'])
    if cp['rc']!=0:raise ValueError('External probe failed')
    for name,_,_ in external['endpoints']:
        if external['before'][name]!='connected' or external['after'][name]!='connected' or observed[name].get('winerror')!=10013:
            raise ValueError('External before/after denial not demonstrated')
        results[name]='PASS'
    for name in ('root_exit_tree','timeout_tree'):
        row=records[name]
        if row['child_state']['dead'] is not True or row['timed_out']!=(name=='timeout_tree'):
            raise ValueError('Child tree cleanup not confirmed')
        if name=='timeout_tree':_parent(row['parent_evidence'])
        else:
            _transport(row['transport'],digest)
            if row['transport']['rc']!=0:raise ValueError('Root exit probe failed')
        results[name]='PASS'
    cp=records['memory_limit']['transport'];_transport(cp,digest);data=json.loads(cp['stdout'])
    if cp['rc']!=17 or data.get('memory_denied') is not True or data['chunk_bytes']!=67108864 or not 0<data['allocated_chunks']<32:
        raise ValueError('2 GiB memory denial not confirmed')
    results['memory_limit']='PASS'
    return results


def _local_outcome(name,state):
    """Bounded no-delivery proof: TCP may be denied or explicitly time out.
    Caller must separately require healthy before/after receivers and no sandbox nonce.
    Never reinterpret old missing error types as timeout.
    """
    denial=state.get('outcome')=='error' and state.get('winerror')==10013
    timeout=(state.get('outcome')=='error' and state.get('error_type')=='TimeoutError'
             and state.get('winerror') is None and type(state.get('elapsed_ms')) is int
             and state['elapsed_ms']>=1900)
    if name.startswith('tcp'):
        if not (denial or timeout):raise ValueError('TCP failure is neither OS denial nor measured timeout')
    elif name.startswith('udp'):
        if not (state.get('outcome')=='sent' or denial):raise ValueError('Unexplained UDP outcome')
    else:raise ValueError('Unknown local protocol')
