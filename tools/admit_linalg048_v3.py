"""Produce a bound isolated-render receipt; visual/semantic acceptance is separate."""
from __future__ import annotations
import argparse
import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'src')]
from holdout_contract import Snapshot, json_object, raw_sha, object_sha, required_text, write_new_json
import prepare_linalg048_rewrite as rewrite
from animtrain import sandbox_execution as sandbox

CANDIDATE_PATH = ROOT / 'reviews/codex-supervision/2026-10-06-holdout-strict-fix/linalg048-v3/candidate.json'
CANDIDATE_SHA = '8d30d09d5f1dd5b7c72f429ee5670680f2a84a953fbebd57d8372bfbca56e169'
SCENE_PATH = ROOT / 'reviews/codex-supervision/2026-10-06-repair-progress-followup/shear-scene-v2.py'
SCENE_SHA = 'e21c9ff372911a46a8538025f6e1f4f4f4cb36371fbef7740fe47fd71c65149e'
SCHEMA = 'linalg048-bound-render-v2'
CODE_FILES = [
    'tools/admit_linalg048_v3.py', 'tools/apply_linalg048_admission.py',
    'tools/prepare_linalg048_rewrite.py', 'tools/holdout_contract.py',
    'tools/build_holdout_pairs.py', 'tools/draft_io.py',
    'src/animtrain/kp_rule.py', 'src/animtrain/near_dup.py',
    'src/animtrain/structural_leakage.py', 'src/animtrain/validate.py',
    'src/animtrain/sandbox_execution.py', 'src/animtrain/appcontainer.py',
    'src/animtrain/win_job.py', 'src/animtrain/private_profile.py',
    'src/animtrain/isolation_evidence.py', 'src/animtrain/network_isolation.py',
]
math_checks = rewrite.math_checks


def load_candidate(snapshot, path=CANDIDATE_PATH):
    raw = snapshot.read(path)
    if raw_sha(raw) != CANDIDATE_SHA:
        raise ValueError('candidate raw hash differs from reviewed v3')
    return json_object(raw)


def prepare(snapshot, candidate_path, scene_path):
    candidate = load_candidate(snapshot, candidate_path)
    scene_raw = snapshot.read(scene_path)
    if raw_sha(scene_raw) != SCENE_SHA:
        raise ValueError('scene is not the reviewed revision')
    scene = scene_raw.decode('utf-8-sig').replace('\r\n', '\n')
    compile(ast.parse(scene), str(scene_path), 'exec')
    active, others, aliases, population = rewrite.load_population(snapshot)
    checks = rewrite.check_candidate(candidate, active, others, aliases)
    for rel in CODE_FILES:
        snapshot.read(ROOT / rel)
    subjects = [{'split':split, 'id':qid,
                 'problem_sha256':raw_sha(row['problem'].encode('utf-8'))}
                for split, qid, row in others]
    return candidate, scene, checks, population, subjects


def verify_result(result, scene, snapshot, decoder=None):
    if not isinstance(result, dict) or result.get('ok') is not True or result.get('status') != 'rendered':
        raise ValueError('actual render did not succeed')
    transport = result.get('transport')
    isolation = result.get('isolation')
    if not isinstance(transport, dict) or type(transport.get('rc')) is not int or transport['rc'] != 0:
        raise ValueError('explicit zero transport return code required')
    if not isinstance(isolation, dict):
        raise ValueError('isolation evidence required')
    for k,v in {'backend':'windows_appcontainer', 'shell':False,
                'job_assigned':True, 'network_isolated':True,
                'fs_isolation':'private_per_run', 'memory_limit_mb':2048}.items():
        if isolation.get(k) != v or type(isolation.get(k)) is not type(v):
            raise ValueError('isolation field mismatch: '+k)
    parent = transport.get('parent_evidence')
    if not isinstance(parent, dict) or parent != isolation.get('parent_evidence'):
        raise ValueError('parent evidence mismatch')
    for key in ('created_suspended', 'job_assigned_before_resume', 'tree_stopped'):
        if parent.get(key) is not True:
            raise ValueError('parent guard missing: '+key)
    if type(parent.get('memory_limit_mb')) is not int or parent['memory_limit_mb'] != 2048:
        raise ValueError('parent memory guard mismatch')
    token = parent.get('token', {})
    if (token.get('api_ok') is not True or token.get('is_appcontainer') is not True or
            type(token.get('capability_count')) is not int or token['capability_count'] != 0):
        raise ValueError('verified zero-capability AppContainer token required')
    if not isinstance(token.get('sid'), str) or not token['sid'].startswith('S-1-15-2-'):
        raise ValueError('AppContainer SID required')
    profile = parent.get('private_profile', {})
    if profile.get('cleanup_complete') is not True or token.get('sid') != profile.get('sid'):
        raise ValueError('private profile cleanup/identity mismatch')
    grants = profile.get('temporary_acl')
    if not isinstance(grants, list) or not grants:
        raise ValueError('restored ACL evidence required')
    for grant in grants:
        if (not isinstance(grant, dict) or grant.get('restored') is not True or
                not isinstance(grant.get('before_sha256'), str) or
                len(grant['before_sha256']) != 64 or
                grant['before_sha256'] != grant.get('after_sha256')):
            raise ValueError('ACL restoration failed')
    work = Path(required_text(transport, 'work')).resolve()
    if not work.is_relative_to(sandbox.WORK_ROOT.resolve()):
        raise ValueError('render work outside controlled transport root')
    scene_path = work / 'scene.py'
    actual_source = snapshot.read(scene_path)
    if (raw_sha(actual_source) != transport.get('source_sha256') or
            actual_source.decode('utf-8-sig').replace('\r\n', '\n') != scene):
        raise ValueError('executed scene/source binding mismatch')
    expected_command = [str((ROOT/'.venv/Scripts/python.exe').resolve()), '-I', '-B',
                        str(work/'bootstrap.py'), 'render', '-ql', '--format=mp4',
                        '--media_dir', str(work/'media'), str(scene_path), 'ConceptScene']
    if transport.get('command') != expected_command:
        raise ValueError('render command differs from controlled command')
    snapshot.read(work/'bootstrap.py')
    for key in ('stdout', 'stderr'):
        raw = snapshot.read(work/(key+'.txt'))
        if raw.decode('utf-8', 'replace') != transport.get(key):
            raise ValueError('raw transport log mismatch: '+key)
    output = result.get('output')
    if not isinstance(output, dict):
        raise ValueError('media binding required')
    if any(type(output.get(k)) is not int or output[k] <= 0 for k in ('size','frames','width','height')):
        raise ValueError('positive integer media metadata required')
    media = Path(required_text(output, 'path')).resolve()
    if not media.is_relative_to(work/'media') or 'partial_movie_files' in media.parts:
        raise ValueError('media is not a final artifact of this run')
    media_raw = snapshot.read(media)
    if raw_sha(media_raw) != output.get('sha256') or len(media_raw) != output.get('size'):
        raise ValueError('media raw binding mismatch')
    decoded = (decoder or sandbox.decode_video)(media)
    if decoded != output:
        raise ValueError('full decoded media metadata mismatch')
    snapshot.check_unchanged()
    return output


def publish_render(out, *, scene_path=SCENE_PATH, candidate_path=CANDIDATE_PATH, renderer=None):
    snapshot = Snapshot(ROOT)
    out = Path(out).resolve()
    if not out.is_relative_to(ROOT) or out.exists():
        raise ValueError('render receipt must use a new project path')
    candidate, scene, checks, population, subjects = prepare(snapshot, candidate_path, scene_path)
    snapshot.check_unchanged()
    result = (renderer or sandbox.render_scene)(scene)
    verify_result(result, scene, snapshot)
    data = {'schema':SCHEMA, 'status':'RENDERED_PENDING_MANUAL_ACCEPTANCE',
            'accepted':False, 'candidate_raw_sha256':CANDIDATE_SHA,
            'candidate_record_sha256':object_sha(candidate),
            'scene':{'path':Path(scene_path).resolve().relative_to(ROOT).as_posix(),
                     'raw_sha256':SCENE_SHA},
            'math':checks['math'], 'screening':checks, 'population':population,
            'semantic_subjects':subjects, 'render_result':result,
            'source_bindings':snapshot.bindings(),
            'visual_review':None, 'global_leakage_free_certified':False,
            'calibration_eligible':False}
    write_new_json(out, data, snapshot)
    return data


def verify_evidence(snapshot, evidence_path, candidate_path=CANDIDATE_PATH):
    data = json_object(snapshot.read(evidence_path))
    if data.get('schema') != SCHEMA or data.get('accepted') is not False:
        raise ValueError('bound v2 render receipt required; old/unbound receipt rejected')
    if data.get('status') != 'RENDERED_PENDING_MANUAL_ACCEPTANCE':
        raise ValueError('render receipt status mismatch')
    scene_info = data.get('scene', {})
    if scene_info.get('raw_sha256') != SCENE_SHA:
        raise ValueError('reviewed scene binding mismatch')
    candidate, scene, checks, population, subjects = prepare(
        snapshot, candidate_path, ROOT / required_text(scene_info, 'path'))
    if (data.get('candidate_raw_sha256') != CANDIDATE_SHA or
            data.get('candidate_record_sha256') != object_sha(candidate) or
            data.get('math') != checks['math'] or data.get('screening') != checks or
            data.get('population') != population or data.get('semantic_subjects') != subjects):
        raise ValueError('candidate/input/population evidence is stale or mismatched')
    verify_result(data.get('render_result'), scene, snapshot)
    bindings = data.get('source_bindings')
    expected = snapshot.bindings()
    receipt_rel = Path(evidence_path).resolve().relative_to(ROOT).as_posix()
    expected.pop(receipt_rel, None)
    if bindings != expected:
        raise ValueError('receipt source bindings incomplete, extra or stale')
    snapshot.check_unchanged()
    return candidate, data


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--scene', type=Path, default=SCENE_PATH)
    parser.add_argument('--candidate', type=Path, default=CANDIDATE_PATH)
    args = parser.parse_args(argv)
    try:
        data = publish_render(args.out, scene_path=args.scene, candidate_path=args.candidate)
        print('render receipt published; manual acceptance PENDING; frames:',
              data['render_result']['output']['frames'])
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print('[FAIL]', exc)
        return 2


if __name__ == '__main__':
    sys.exit(main())
