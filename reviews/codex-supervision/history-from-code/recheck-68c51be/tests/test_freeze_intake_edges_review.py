"""Regressions for freeze-guard edges discovered in msg_178 review."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pytest

from animtrain.dataset_intake import _assert_not_frozen, convert_array_to_jsonl
from animtrain.freeze import freeze_set
from tests.test_dataset_intake import clean_record

def write_inputs(tmp_path):
    src = tmp_path / "array.json"
    src.write_text(json.dumps([clean_record()]), encoding="utf-8")
    dst = tmp_path / "eval.jsonl"
    dst.write_text(json.dumps(clean_record(id="original")) + "\n", encoding="utf-8")
    return src, dst

def test_convert_cannot_overwrite_lock_itself(tmp_path):
    src, dst = write_inputs(tmp_path)
    lock = tmp_path / "eval.lock.json"
    freeze_set([dst.resolve()], lock)
    before = lock.read_bytes()
    with pytest.raises(ValueError):
        convert_array_to_jsonl(src, lock, force=True)
    assert lock.read_bytes() == before

@pytest.mark.parametrize("marker", [
    {"freeze_lock_version": 1, "locked": True, "n_files": 0, "entries": []},
    {"freeze_lock_version": 999, "locked": True, "n_files": 0, "entries": []},
    {"freeze_lock_version": 1, "locked": False, "n_files": 0, "entries": []},
])
def test_recognized_but_invalid_lock_blocks_write(tmp_path, marker):
    src, dst = write_inputs(tmp_path)
    (tmp_path / "bad.lock.json").write_text(json.dumps(marker), encoding="utf-8")
    before = dst.read_bytes()
    with pytest.raises(ValueError):
        convert_array_to_jsonl(src, dst, force=True)
    assert dst.read_bytes() == before

def test_malformed_entry_blocks_guard_with_value_error(tmp_path):
    _, dst = write_inputs(tmp_path)
    marker = {"freeze_lock_version": 1, "locked": True, "n_files": 1,
              "entries": [{"path": str(dst.resolve()), "size": dst.stat().st_size}]}
    (tmp_path / "bad.lock.json").write_text(json.dumps(marker), encoding="utf-8")
    with pytest.raises(ValueError):
        _assert_not_frozen(tmp_path / "new.jsonl")
    assert not (tmp_path / "new.jsonl").exists()

def test_valid_unrelated_lock_allows_new_output(tmp_path):
    src, dst = write_inputs(tmp_path)
    freeze_set([dst.resolve()], tmp_path / "eval.lock.json")
    before = dst.read_bytes()
    output = tmp_path / "new.jsonl"
    result = convert_array_to_jsonl(src, output)
    assert result["n_records"] == 1
    assert output.exists()
    assert dst.read_bytes() == before
