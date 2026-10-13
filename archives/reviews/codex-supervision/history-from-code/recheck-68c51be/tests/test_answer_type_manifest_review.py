"""Manifest gate must reject non-string answers just like intake."""
import json
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from animtrain.manifest import Entry, Manifest, sha256_file
from animtrain.validate import validate_manifest
from tests.test_dataset_intake import clean_record

@pytest.mark.parametrize("answer", [["4"], {"value": "4"}])
def test_answer_container_rejected_by_manifest(tmp_path, answer):
    source = tmp_path / "train.jsonl"
    source.write_text(json.dumps(clean_record(answer=answer)) + "\n", encoding="utf-8")
    manifest = Manifest(name="synthetic-review", entries=[
        Entry(path=source.name, sha256=sha256_file(source), size=source.stat().st_size,
              source="synthetic-review", license="internal-generated", split="train")])
    result = validate_manifest(manifest, tmp_path)
    assert result["ok"] is False
    assert result["exit_code"] == 1
    assert result["problems"]
