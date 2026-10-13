"""Frozen output guards for the field-report CLI, disposable fixtures only."""
import json
import subprocess
import sys
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from animtrain.freeze import freeze_set
CLI = ROOT / 'tools/check_fields.py'

def source(tmp_path):
    p = tmp_path / 'input.jsonl'
    p.write_text(json.dumps({'id': 'synthetic', 'problem': 'synthetic task', 'solution': 'synthetic explanation', 'answer': '1'}) + '\n', encoding='utf-8')
    return p

def run(src, dst):
    return subprocess.run([sys.executable, '-X', 'utf8', str(CLI), '--jsonl', str(src), '--report', str(dst), '--force'], capture_output=True, encoding='utf-8')

@pytest.mark.parametrize('mode', ['frozen_data', 'lock_itself', 'malformed_lock', 'new_lock_name'])
def test_report_force_cannot_modify_frozen_or_lock_paths(tmp_path, mode):
    src = source(tmp_path)
    out = tmp_path / 'out'
    out.mkdir()
    target = out / 'retained.jsonl'
    target.write_text('preserve this file\n', encoding='utf-8')
    lock = out / 'frozen.lock.json'
    if mode in ('frozen_data', 'lock_itself'):
        freeze_set([target], lock)
    if mode == 'malformed_lock':
        lock.write_text('{broken', encoding='utf-8')
    report = lock if mode == 'lock_itself' else out / 'new.lock.json' if mode == 'new_lock_name' else target
    before = {p: p.read_bytes() for p in out.iterdir()}
    result = run(src, report)
    assert result.returncode == 1, result.stdout + result.stderr
    assert all((p.exists() and p.read_bytes() == data for p, data in before.items()))
    if mode == 'new_lock_name':
        assert not report.exists()

def test_nonfrozen_report_force_still_supported(tmp_path):
    src = source(tmp_path)
    report = tmp_path / 'report.json'
    report.write_text('old', encoding='utf-8')
    result = run(src, report)
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(report.read_text(encoding='utf-8'))['bad'] == []

@pytest.mark.parametrize('alias_kind', ['data', 'lock'])
def test_report_hardlink_cannot_modify_frozen_bytes(tmp_path, alias_kind):
    import os
    src = source(tmp_path)
    out = tmp_path / 'out'
    out.mkdir()
    frozen = out / 'retained.jsonl'
    frozen.write_text('retained frozen bytes\n', encoding='utf-8')
    freeze_set([frozen], out / 'frozen.lock.json')
    if alias_kind == 'lock':
        frozen = out / 'frozen.lock.json'
    report = out / 'alias.json'
    os.link(frozen, report)
    original = frozen.read_bytes()
    result = run(src, report)
    assert result.returncode == 1, result.stdout + result.stderr
    assert frozen.read_bytes() == original
    assert report.read_bytes() == original
