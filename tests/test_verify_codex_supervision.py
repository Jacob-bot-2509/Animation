from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("verify_codex", ROOT / "tools/verify_codex_supervision.py")
v = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(v)


def test_old_issue_rows_have_real_counts():
    rows = [
        {"status": "FAIL", "issues": ["tail_mismatch", "decimal_in_answer"]},
        {"status": "FAIL", "issues": ["tail_mismatch"]},
        {"status": "PASS", "issues": []},
    ]
    assert v.consistency_counts(rows) == {
        "total": 3, "status_counts": {"FAIL": 2, "PASS": 1},
        "tail_mismatch_rows": 2, "decimal_answer_rows": 1,
    }


def test_new_issue_rows_are_counted_once_per_record():
    row = {"status": "NEEDS_CORRECTION", "tail_text_relation": "DIFFERENT_TEXT_UNRESOLVED",
           "issues": [{"code": "tail_mismatch"},
                      {"code": "decimal_requires_exact_form", "field": "solution"},
                      {"code": "decimal_requires_exact_form", "field": "answer"},
                      {"code": "decimal_requires_exact_form", "field": "answer"}]}
    got = v.consistency_counts([row])
    assert got["tail_mismatch_rows"] == got["decimal_answer_rows"] == 1


@pytest.mark.parametrize("rows", [
    [], [{"status": "PASS"}], [{"issues": []}],
    [{"status": "FAIL", "issues": [None]}],
    [{"status": "FAIL", "issues": [{"field": "answer"}]}],
])
def test_malformed_report_is_not_zero_issues(rows):
    with pytest.raises(v.VerificationError):
        v.consistency_counts(rows)


def test_real_tuple_identity_and_risky_exclusion():
    result = v.review_index_summary(
        {"ids": [["train", "draft-a"], ["test", "b"]],
         "risky": [["train", "draft-a"], ["test", "unrelated"]]},
        [{"group": "selected_draft", "id": "draft-a"}])
    assert result["review_count"] == 2
    assert result["by_split"] == {"train": 1, "test": 1}
    assert result["draft_id_intersection"] == ["draft-a"]


@pytest.mark.parametrize("index", [
    {}, {"ids": []}, {"ids": ["a"]}, {"ids": [["train"]]},
    {"ids": [["train", ""]]}, {"ids": [["train", 1]]},
    {"ids": [["train", "a"], ["train", "a"]]},
    {"risky": [["train", "a"]]},
])
def test_ambiguous_or_missing_identity_array_fails(index):
    with pytest.raises(v.VerificationError):
        v.review_index_summary(index, [{"group": "selected_draft", "id": "a"}])


def make_patch(rid="a", group="train"):
    before = {"id": rid, "problem": "p", "solution": "s", "answer": "0", "scene": "retained"}
    after = dict(before, answer="1")
    before_sha = v.digest(v.canonical(before))
    return {"id": rid, "source": {"id": rid, "group": group,
            "record_version_sha256": before_sha},
            "before_record_dense_sha256": before_sha,
            "after_record_dense_sha256": v.digest(v.canonical(after)),
            "after_math_fields": {k: after[k] for k in ("problem", "solution", "answer")},
            "corrected_record": after}


def test_correction_split_is_nested_in_source():
    got = v.correction_counts([make_patch("a", "train"), make_patch("b", "test")])
    assert got == {"correction_count": 2, "by_group": {"train": 1, "test": 1}}


@pytest.mark.parametrize("fault", ["group", "identity", "after_sha", "before_sha", "math_fields"])
def test_corrected_record_corruption_is_rejected(fault):
    row = make_patch()
    if fault == "group":
        row["source"].pop("group")
    elif fault == "identity":
        row["corrected_record"]["id"] = "other"
    elif fault == "after_sha":
        row["corrected_record"]["answer"] = "2"
    elif fault == "before_sha":
        row["before_record_dense_sha256"] = "0" * 64
    else:
        row["after_math_fields"]["answer"] = "2"
    with pytest.raises(v.VerificationError):
        v.correction_counts([row])


def test_duplicate_correction_identity_fails():
    with pytest.raises(v.VerificationError):
        v.correction_counts([make_patch(), make_patch()])


def artifact(tmp_path):
    path = tmp_path / "one.txt"
    path.write_bytes(b"evidence")
    return {"path": "one.txt", "raw_sha256": v.digest(b"evidence"), "bytes": 8}


def test_valid_manifest_and_file_binding(tmp_path):
    entry = artifact(tmp_path)
    assert v.verify_artifacts(tmp_path, {"artifacts": [entry]}, 1)["verified_artifacts"] == 1


@pytest.mark.parametrize("fault", ["empty", "count", "duplicate", "missing", "bytes", "sha", "boolean_bytes"])
def test_incomplete_or_corrupt_manifest_fails(tmp_path, fault):
    entry = artifact(tmp_path)
    entries = [entry]
    expected = 1
    if fault == "empty":
        entries = []
    elif fault == "count":
        expected = 2
    elif fault == "duplicate":
        entries = [entry, dict(entry)]
        expected = 2
    elif fault == "missing":
        entry["path"] = "absent.txt"
    elif fault == "bytes":
        entry["bytes"] = 9
    elif fault == "sha":
        entry["raw_sha256"] = "0" * 64
    else:
        entry["bytes"] = True
    with pytest.raises((v.VerificationError, OSError)):
        v.verify_artifacts(tmp_path, {"artifacts": entries}, expected)


def test_escape_path_is_rejected_before_reading(tmp_path):
    with pytest.raises(v.VerificationError):
        v.check_binding(tmp_path, {"path": "../outside.txt", "raw_sha256": "0" * 64, "bytes": 0})


def test_ab_failure_cannot_be_masked_by_delivery_success(monkeypatch, tmp_path):
    for name in ("check_delivery", "check_ab", "check_consistency", "check_review_index", "check_corrections"):
        monkeypatch.setattr(v, name, lambda root: {"completed": True})
    def bad_binding(root):
        raise v.VerificationError("A SHA mismatch")
    monkeypatch.setattr(v, "check_ab", bad_binding)
    result = v.verify(tmp_path)
    assert result["overall"] == "FAIL"
    assert result["checks"]["AB"]["status"] == "FAIL"
    assert result["checks"]["delivery"]["status"] == "PASS_SCOPED_EVIDENCE_CHECK"
    monkeypatch.setattr(v, "verify", lambda: result)
    assert v.main([]) == 1


def test_existing_output_is_preserved(tmp_path):
    rel = Path("reviews/new/result.json")
    target = tmp_path / rel
    target.parent.mkdir(parents=True)
    target.write_bytes(b"old raw evidence")
    with pytest.raises(FileExistsError):
        v.write_output(tmp_path, rel, {})
    assert target.read_bytes() == b"old raw evidence"


@pytest.mark.parametrize("relative", [
    "outside.json",
    str(v.SUP / "new.json"),
    str(v.PACKET / "new.json"),
    "../outside.json",
])
def test_output_cannot_change_frozen_or_nonreview_locations(tmp_path, relative):
    with pytest.raises(v.VerificationError):
        v.write_output(tmp_path, Path(relative), {})


def test_live_delivery_bound_counts_and_no_math_acceptance():
    result = v.verify()
    assert result["overall"] == "PASS_SCOPED_EVIDENCE_VERIFICATION"
    assert result["checks"]["original_consistency"]["result"]["tail_mismatch_rows"] == 602
    assert result["checks"]["original_consistency"]["result"]["decimal_answer_rows"] == 11
    assert result["checks"]["review_input_scope"]["result"]["review_count"] == 296
    assert result["checks"]["review_input_scope"]["result"]["draft_id_intersection_count"] == 0
    assert result["checks"]["correction_structure"]["result"]["by_group"] == {"train": 9, "eval": 9, "test": 12}
    assert result["PASS_CORE_SCOPE_issued"] is False
    assert result["full_761_math_verdict"] == result["semantic_isolation_verdict"] == "NOT_ESTABLISHED"
