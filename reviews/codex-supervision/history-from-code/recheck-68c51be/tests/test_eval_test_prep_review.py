"""Review guards for the read-only eval preparation CLI; synthetic data only."""
import json
import subprocess
import sys
from pathlib import Path
import pytest
ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'tools/eval_test_prep.py'
FIX = ROOT / 'reviews/fixtures-eval-test'

def row(name):
    r = json.loads((FIX / name).read_text(encoding='utf-8'))
    return r

def write(p, r):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(r, ensure_ascii=False) + '\n', encoding='utf-8')

def run(candidate, train):
    return subprocess.run([sys.executable, '-X', 'utf8', str(CLI), 'check', str(candidate), '--train-dir', str(train)], capture_output=True, encoding='utf-8')

@pytest.mark.parametrize('reference', ['missing', 'empty_directory', 'empty_file', 'invalid_json', 'invalid_shape'])
def test_reference_must_be_available_and_valid(tmp_path, reference):
    candidate = tmp_path / 'candidate.jsonl'
    write(candidate, row('eval_ok.jsonl'))
    train = tmp_path / 'train'
    if reference != 'missing':
        train.mkdir()
    if reference == 'empty_file':
        (train / 'train.jsonl').write_text('')
    if reference == 'invalid_json':
        (train / 'train.jsonl').write_text('{broken')
    if reference == 'invalid_shape':
        (train / 'train.jsonl').write_text('null\n')
    result = run(candidate, train)
    assert result.returncode == 1, result.stdout + result.stderr
    assert '[FAIL]' in result.stdout
    assert '[OK]' not in result.stdout

def test_cross_candidate_file_ids_must_be_unique(tmp_path):
    train = tmp_path / 'train.jsonl'
    write(train, row('train_synthetic.jsonl'))
    candidates = tmp_path / 'candidate'
    r = row('eval_ok.jsonl')
    write(candidates / 'a.jsonl', r)
    r['problem'] = 'A separate synthetic geometric task: classify three conic shapes.'
    write(candidates / 'b.jsonl', r)
    result = run(candidates, train)
    assert result.returncode == 1, result.stdout + result.stderr
    assert r['id'] in result.stdout

def test_candidate_ids_cannot_overlap_train_even_with_new_problem(tmp_path):
    r = row('train_synthetic.jsonl')
    train = tmp_path / 'train.jsonl'
    write(train, r)
    candidate_row = row('eval_ok.jsonl')
    candidate_row['id'] = r['id']
    candidate = tmp_path / 'candidate.jsonl'
    write(candidate, candidate_row)
    result = run(candidate, train)
    assert result.returncode == 1, result.stdout + result.stderr
    assert r['id'] in result.stdout

def test_reference_file_ids_must_be_unique(tmp_path):
    train = tmp_path / 'train'
    r = row('train_synthetic.jsonl')
    write(train / 'a.jsonl', r)
    r['problem'] = 'Synthetic calculus reference task: differentiate a cubic monomial.'
    write(train / 'b.jsonl', r)
    candidate = tmp_path / 'candidate.jsonl'
    write(candidate, row('eval_ok.jsonl'))
    result = run(candidate, train)
    assert result.returncode == 1, result.stdout + result.stderr

def test_candidate_quarantine_keeps_isolation_only_check_available(tmp_path):
    train = tmp_path / 'train.jsonl'
    write(train, row('train_synthetic.jsonl'))
    candidate = tmp_path / 'candidate.jsonl'
    write(candidate, row('eval_ok.jsonl'))
    result = run(candidate, train)
    assert result.returncode == 0, result.stdout + result.stderr
    assert '[WARN]' in result.stdout
    assert 'UNCALIBRATED' in result.stdout
