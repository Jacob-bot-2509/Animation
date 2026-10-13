"""Version-scoped CLI regression tests using isolated synthetic files."""
import contextlib
import hashlib
import importlib.util
import io
import json
import sys
from pathlib import Path
from unittest import mock

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from animtrain.freeze import freeze_set
from animtrain.manifest import Entry, Manifest, sha256_file


def load_cli(name):
    spec = importlib.util.spec_from_file_location('review_' + name, ROOT / 'tools' / (name + '.py'))
    cli = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cli)
    return cli


def fixture(root):
    data = root / 'data'
    manifests, files, locks = {}, {}, {}
    for version in ('v1', 'v2'):
        entries = []
        for split in ('eval', 'test'):
            f = data / version / split / 'records.jsonl'
            f.parent.mkdir(parents=True)
            f.write_text(json.dumps({'id': version + split, 'problem': version + split}) + '\n', encoding='utf-8')
            files[version, split] = f
            entries.append(Entry(path=str(f.relative_to(data if version == 'v2' else data / version)),
                split=split, sha256=sha256_file(f), size=f.stat().st_size,
                source='synthetic', license='internal-generated'))
        mp = data / 'manifest.json' if version == 'v2' else data / version / 'manifest.json'
        Manifest(name='synthetic-' + version, entries=entries).save(mp)
        manifests[version] = mp
        for split in ('eval', 'test'):
            lock = data / f'{split}-{version}.lock.json'
            freeze_set([files[version, split]], lock, meta={'manifest_sha256': sha256_file(mp)})
            locks[version, split] = lock
    return manifests, files, locks


@pytest.mark.parametrize('case, expected', [('valid', True), ('other_bad_hash', True),
    ('current_bad_hash', False), ('current_missing_hash', False), ('unscopable', False)])
def test_preflight_filters_versions_before_hash_validation(tmp_path, case, expected):
    manifests, files, locks = fixture(tmp_path)
    if case == 'unscopable':
        (tmp_path / 'data/unknown.lock.json').write_text('{', encoding='utf-8')
    elif case != 'valid':
        version = 'v1' if case == 'other_bad_hash' else 'v2'
        lock = locks[version, 'eval']
        payload = json.loads(lock.read_bytes())
        if case == 'current_missing_hash':
            del payload['entries'][0]['sha256']
        else:
            payload['entries'][0]['sha256'] = '0' * 64
        lock.write_text(json.dumps(payload), encoding='utf-8')
    cli = load_cli('preflight')
    captured = []
    def capture(*args, **kwargs):
        captured.extend(kwargs['extra_checks'])
        return {'checks': [], 'ok': False, 'ready': False, 'exit_code': 1}
    with mock.patch.object(cli, 'ROOT', tmp_path), \
         mock.patch.object(cli, 'run_preflight', side_effect=capture), \
         mock.patch.object(cli, 'validate_manifest', return_value={'ok': True, 'n_entries': 2,
             'problems': [], 'quarantines': [], 'near_dup_calibrated': False}), \
         mock.patch('animtrain.render_gate.render_check', return_value={'ok': True, 'status': 'synthetic', 'detail': 'mock'}), \
         mock.patch('animtrain.render_gate.math_check', return_value={'ok': True, 'status': 'synthetic', 'detail': 'mock'}), \
         contextlib.redirect_stdout(io.StringIO()):
        cli.main(['--manifest', str(manifests['v2'])])
    gate = next(payload for name, payload in captured if name == 'freeze_gate')
    assert gate[0] is expected, gate


@pytest.mark.parametrize('version', ['v1', 'v2'])
def test_status_accepts_selected_active_or_archive_manifest(tmp_path, version):
    fixture(tmp_path)
    cli = load_cli('eval_test_prep')
    with mock.patch.object(cli, 'ROOT', tmp_path), contextlib.redirect_stdout(io.StringIO()) as out:
        assert cli.main(['status', '--dir', str(tmp_path / 'data' / version)]) == 0
    assert '[WARN]' not in out.getvalue(), out.getvalue()
    assert out.getvalue().count('校验通过') == 2


def test_status_cannot_bind_v2_files_to_an_unrelated_archive(tmp_path):
    manifests, files, locks = fixture(tmp_path)
    lock = locks['v2', 'eval']
    payload = json.loads(lock.read_bytes())
    payload['meta']['manifest_sha256'] = sha256_file(manifests['v1'])
    lock.write_text(json.dumps(payload), encoding='utf-8')
    cli = load_cli('eval_test_prep')
    with mock.patch.object(cli, 'ROOT', tmp_path), contextlib.redirect_stdout(io.StringIO()) as out:
        cli.main(['status', '--dir', str(tmp_path / 'data/v2')])
    assert '[WARN] eval' in out.getvalue(), out.getvalue()
    assert 'manifest 绑定不一致' in out.getvalue()
