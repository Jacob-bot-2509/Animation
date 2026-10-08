"""Independent evaluation regression cases; no GPU or model dependencies."""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from animtrain.metrics import SampleResult, aggregate, finalize_result


def good(sid="a", **kwargs):
    return SampleResult(sid, "synthetic-input-hash",
                        parsed_strict=True, parsed_lenient=True, **kwargs)


def test_math_failure_survives_json_success():
    result = finalize_result(good(failure_class="math_error", failure_detail="wrong answer"))
    assert result.status == "failed"
    assert result.failure_class == "math_error"
    assert result.failure_detail == "wrong answer"


def test_invalid_failure_class_rejected_even_for_valid_json():
    with pytest.raises(ValueError, match="failure_class"):
        finalize_result(good(failure_class="not-a-class"))


def test_explicit_failed_status_is_not_erased():
    result = finalize_result(good(status="failed"))
    assert result.status == "failed"
    assert result.failure_class == "schema_violation"


def test_semantic_failure_does_not_change_field_compliance():
    summary = aggregate([good(failure_class="math_error", failure_detail="wrong")])
    assert summary["ok_rate"] == 0
    assert summary["strict_parse_rate"] == 1
    assert summary["spec_field_compliance_rate"] == 1
    assert summary["failure_counts"] == {"math_error": 1}


def test_foreign_math_review_cannot_inflate_score():
    with pytest.raises(ValueError, match="outside"):
        aggregate([good()], {"foreign1": True, "foreign2": True})


def test_partial_math_review_remains_unmeasured():
    summary = aggregate([good("a"), good("b")], {"a": True})
    assert summary["math_review_pass_rate"] == "NOT_MEASURED"
    assert summary["math_review_n"] == 1
    assert summary["math_reviewed_n"] == 1


def test_complete_math_review_uses_all_samples():
    summary = aggregate([good("a"), good("b")], {"a": True, "b": False})
    assert summary["math_review_pass_rate"] == 0.5
    assert summary["math_reviewed_n"] == 2


def test_review_truthy_string_is_not_a_verified_boolean():
    with pytest.raises(ValueError, match="bool"):
        aggregate([good()], {"a": "verified"})


def test_duplicate_results_rejected():
    with pytest.raises(ValueError, match="Duplicate"):
        aggregate([good("a"), good("a")])


def test_missing_latency_is_not_zero_or_measured():
    summary = aggregate([good("a"), good("b", metrics={"latency_sec": None})])
    assert summary["median_latency_sec"] is None
    assert summary["p95_latency_sec"] is None
    assert summary["latency_n"] == 0


def test_nearest_rank_p95_boundary_with_twenty_samples():
    summary = aggregate([good(str(i), metrics={"latency_sec": float(i)}) for i in range(1, 21)])
    assert summary["median_latency_sec"] == 10.5
    assert summary["p95_latency_sec"] == 19
    assert summary["latency_n"] == 20


@pytest.mark.parametrize("value", [-1, float("nan"), float("inf"), True, "1.0"])
def test_invalid_latency_cannot_be_published(value):
    with pytest.raises(ValueError, match="latency"):
        aggregate([good(metrics={"latency_sec": value})])


def test_aggregation_finalizes_copies_without_mutating_input():
    result = good(failure_class="math_error", failure_detail="wrong")
    summary = aggregate([result])
    assert result.status == "pending"
    assert summary["ok"] == 0


def test_inconsistent_parse_flags_rejected():
    with pytest.raises(ValueError, match="Strict"):
        finalize_result(SampleResult("a", "h", parsed_strict=True, parsed_lenient=False))
