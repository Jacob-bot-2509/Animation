"""A report must never truncate the JSONL input through an NTFS hard link."""
import json
import os
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def test_intake_report_cannot_overwrite_input_hardlink(tmp_path):
    src = tmp_path / 'candidate.jsonl'
    src.write_text((ROOT / 'reviews/fixtures-eval-test/eval_ok.jsonl').read_text(encoding='utf-8'), encoding='utf-8')
    original = src.read_bytes()
    report = tmp_path / 'alias.md'
    os.link(src, report)
    result = subprocess.run([sys.executable, '-X', 'utf8', str(ROOT / 'tools/dataset_intake.py'), 'report', str(src), '--out', str(report), '--force'], capture_output=True, encoding='utf-8')
    assert result.returncode == 2, result.stdout + result.stderr
    assert src.read_bytes() == original
    assert report.read_bytes() == original
