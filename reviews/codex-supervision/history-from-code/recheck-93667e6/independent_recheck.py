"""Read-only replay of reviewer counterexamples against a pinned source snapshot."""
import contextlib
import copy
import hashlib
import importlib.util
import io
import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
SOURCE = Path(r'D:\Animation-Model-Training')
sys.path.insert(0, str(ROOT / 'src'))
os.chdir(ROOT)
report = {'revision': '93667e6', 'checks': {}, 'findings': []}

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

from animtrain.metrics import SampleResult, aggregate
from animtrain.render_gate import _isolation_state, render_check
from animtrain.preflight import check_exec_isolation
from animtrain.freeze import check_frozen, frozen_paths
from animtrain.manifest import Manifest
from animtrain.validate import validate_manifest

bad_flags = []
for flag in ('parsed_strict', 'parsed_lenient'):
    for value in (2, 1, None, 'true'):
        kwargs = {'parsed_strict': True, 'parsed_lenient': True, flag: value}
        try:
            aggregate([SampleResult('probe', 'probe-hash', **kwargs)])
            bad_flags.append({'flag': flag, 'value': value, 'rejected': False})
        except ValueError as exc:
            bad_flags.append({'flag': flag, 'value': value, 'rejected': True, 'error': str(exc)})
report['checks']['metrics_flags'] = bad_flags
report['checks']['isolation'] = {'state': _isolation_state(), 'gate': check_exec_isolation(),
                                'untrusted_render': render_check('raise RuntimeError("must not run")', trusted=False)}

generator = load('review_generator', 'tools/make_eval_test.py')
guards = []
for alias in ('data/V1', 'data/v1', 'data/v2/../V1'):
    with patch.object(sys, 'argv', ['make_eval_test.py', '--out', str(ROOT / alias)]), \
         patch.object(Path, 'write_text', side_effect=AssertionError('write attempt prohibited')), \
         contextlib.redirect_stdout(io.StringIO()) as out:
        try:
            rc = generator.main()
            guards.append({'alias': alias, 'returncode': rc, 'stdout': out.getvalue()})
        except AssertionError as exc:
            guards.append({'alias': alias, 'error': str(exc)})
report['checks']['v1_alias_guard'] = guards

data_checks = []
for version in ('v1', 'v2'):
    for split in ('eval', 'test'):
        manifest_path = ROOT / 'data' / version / split / 'manifest.json'
        lock_path = ROOT / 'data' / f'{split}-{version}.lock.json'
        binding_path = ROOT / 'data/v1/manifest.json' if version == 'v1' else manifest_path
        lock = json.loads(lock_path.read_bytes())
        checked = validate_manifest(Manifest.load(manifest_path), manifest_path.parent)
        data_checks.append({'version': version, 'split': split,
            'manifest_ok': checked['ok'], 'problems': checked['problems'],
            'quarantines': checked['quarantines'], 'lock_problems': check_frozen(lock_path),
            'binding_ok': lock['meta']['manifest_sha256'] == hashlib.sha256(binding_path.read_bytes()).hexdigest()})
report['checks']['manifests_locks'] = data_checks

prep = load('review_prep', 'tools/eval_test_prep.py')
statuses = []
for version in ('v1', 'v2'):
    with contextlib.redirect_stdout(io.StringIO()) as out:
        rc = prep.main(['status', '--dir', str(ROOT / 'data' / version)])
    statuses.append({'version': version, 'returncode': rc, 'stdout': out.getvalue()})
report['checks']['status'] = statuses

eval_records = [json.loads(line) for line in (ROOT / 'data/v2/eval/dataset_eval.jsonl').read_text(encoding='utf-8').splitlines() if line.strip()]
by_id = {r['id']: r for r in eval_records}
examples = json.loads((SOURCE / 'reviews/2026-10-03-claude-supervision/evidence/scene-spec-review-examples.json').read_bytes())['examples']
report['checks']['scene_examples'] = [{'id': r['sample_id'], 'exact_match': by_id[r['sample_id']]['scene_spec'] == r['proposed_changes']['scene_spec']} for r in examples]
report['checks']['linalg_solution'] = by_id['eval-linalg-023-s3']['solution']
import sympy as sp
x = sp.Symbol('x')
real_product = (x-1)*(x+1)*(x*x+1)*(x*x-sp.sqrt(2)*x+1)*(x*x+sp.sqrt(2)*x+1)
report['checks']['linalg_factor_identity'] = sp.expand(real_product - (x**8-1)) == 0

v1_files = [str(next((ROOT / 'data/v1' / split).glob('*.jsonl')).relative_to(ROOT)).replace('\\', '/') for split in ('eval', 'test')]
v1_files += ['data/v1/manifest.json', 'data/eval-v1.lock.json', 'data/test-v1.lock.json']
report['checks']['v1_immutable'] = []
for name in v1_files:
    before = subprocess.check_output(['git', '-C', str(SOURCE), 'show', 'd701ee4:'+name])
    report['checks']['v1_immutable'].append({'path': name, 'identical': (ROOT / name).read_bytes() == before})

# Only the final gate evaluation is intercepted: no render/model or production data is changed.
pf = load('review_preflight', 'tools/preflight.py')
bad_v2 = json.loads((ROOT / 'data/eval-v2.lock.json').read_bytes())
bad_v2['entries'][0]['sha256'] = '0' * 64
bad_v2_path = ROOT / 'evidence/synthetic-v2-corrupt.lock.json'
bad_v2_path.parent.mkdir(exist_ok=True)
bad_v2_path.write_text(json.dumps(bad_v2), encoding='utf-8')
captured = []
def capture(*args, **kwargs):
    extra = kwargs.get('extra_checks', [])
    captured.extend(extra)
    return {'checks': [], 'ok': False, 'ready': False, 'unverified': [], 'exit_code': 1}

def gate_probe(inject_other_version_failure):
    captured.clear()
    original = check_frozen
    def validate(lock):
        if inject_other_version_failure and Path(lock).name == 'eval-v2.lock.json':
            return original(bad_v2_path)
        return original(lock)
    with patch('animtrain.render_gate.render_check', return_value={'ok': True, 'status': 'review_stub', 'detail': 'No render performed'}), \
         patch('animtrain.render_gate.math_check', return_value={'ok': True, 'status': 'review_stub', 'detail': 'No subprocess performed'}), \
         patch('animtrain.freeze.check_frozen', side_effect=validate), \
         patch.object(pf, 'run_preflight', side_effect=capture), \
         contextlib.redirect_stdout(io.StringIO()) as out:
        try:
            pf.main(['--manifest', str(ROOT / 'data/v1/manifest.json')])
        except (KeyError, TypeError) as exc:
            # The real gate has already been calculated; reporting schema may differ.
            out.write(str(exc))
    return {'freeze_gate': next((value for key, value in captured if key == 'freeze_gate'), None),
            'captured': copy.deepcopy(captured), 'stdout': out.getvalue()}

report['checks']['preflight_normal'] = gate_probe(False)
report['checks']['preflight_other_version_bad_lock'] = gate_probe(True)
if report['checks']['preflight_other_version_bad_lock']['freeze_gate'] and not report['checks']['preflight_other_version_bad_lock']['freeze_gate'][0]:
    report['findings'].append({'priority': 'P2', 'file': 'tools/preflight.py',
        'issue': 'check_frozen validates all discovered version locks before the version filter; a damaged v2 lock still blocks v1.'})

path = ROOT / 'independent-results.json'
path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
