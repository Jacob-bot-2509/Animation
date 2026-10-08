import importlib.util
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("core_scope_checker", ROOT / "tools/core_scope_consistency_check.py")
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


def record(problem="$2+2$", solution="$2+2=5$", answer="$5$"):
    return {"id": "case", "problem": problem, "solution": solution, "answer": answer}


@pytest.mark.parametrize("a,b", [
    (r"\frac{1}{23}", r"\frac{12}{3}"),
    (r"x^{12}", r"x^{1}2"),
    (r"\frac{1}{2+3}", r"\frac{1+2}{3}"),
])
def test_normalization_retains_mathematical_structure(a, b):
    assert checker.norm(a) != checker.norm(b)


def test_wrapper_normalization_does_not_prove_correctness():
    assert checker.norm(r"$\dfrac{1}{2}$") == checker.norm(r"\frac{1}{2}")
    row = checker.check_record(record(answer="$2+2=5$"))
    assert row["tail_text_relation"] == "DISPLAY_TEXT_MATCH_NO_PROOF"
    assert row["mathematical_verdict"] == "UNREVIEWED"
    assert row["accepted"] is False
    assert row["status"] == "DIAGNOSTIC_ONLY"


def test_cross_field_errors_do_not_cancel():
    row = checker.check_record(record(problem="$" + r"{x$", solution=r"$y}$"))
    assert {(x["field"], x["code"]) for x in row["issues"]} >= {
        ("problem", "unclosed_brace"), ("solution", "unexpected_brace_close")}


@pytest.mark.parametrize("text", [
    r"集合 $\{x:x>0\}$，价格 \$5。", r"\(x^{2}\)", r"\[x+1\]",
    r"$$\frac{1}{2}$$", r"$\begin{pmatrix}1&2\\3&4\end{pmatrix}$",
])
def test_escaped_or_balanced_delimiters(text):
    assert checker.latex_balanced(text)


@pytest.mark.parametrize("text", [
    r"$x", r"\(x\]", r"$$x$", r"$x}$",
    r"$\begin{matrix}1\end{pmatrix}$",
])
def test_malformed_delimiters(text):
    assert not checker.latex_balanced(text)


@pytest.mark.parametrize("field", ["problem", "solution", "answer"])
def test_fraction_policy_checks_every_mathematical_field(field):
    rec = record()
    rec[field] = "$0.5$"
    row = checker.check_record(rec)
    assert {"field": field, "code": "decimal_requires_exact_form"} in row["issues"]
    assert row["status"] == "NEEDS_CORRECTION"


@pytest.mark.parametrize("text", [r"$\pi\approx 22/7$", "$π≈22/7$"])
def test_approximation_without_decimal_is_flagged(text):
    row = checker.check_record(record(answer=text))
    assert any(x["code"] == "approximation_requires_exact_form" for x in row["issues"])


def test_different_tail_is_unresolved_not_a_mathematical_failure():
    row = checker.check_record(record(solution="$y-1=2(x-1)$", answer="$y=2x-1$"))
    assert row["status"] == "DIAGNOSTIC_ONLY"
    assert row["tail_text_relation"] == "DIFFERENT_TEXT_UNRESOLVED"
    assert row["mathematical_verdict"] == "UNREVIEWED"


def test_zero_answer_and_bad_types():
    row = checker.check_record(record(answer=0))
    assert not any(x["code"] == "empty_field" for x in row["issues"])
    for value in [True, {}, 0.5]:
        row = checker.check_record(record(answer=value))
        assert any(x["code"] == "invalid_field_type" for x in row["issues"])


def test_import_has_no_report_side_effect():
    assert callable(checker.main)


def test_existing_report_is_preserved(tmp_path):
    out = tmp_path / "report.jsonl"
    out.write_bytes(b"old evidence")
    with pytest.raises(FileExistsError):
        checker.write_reports(out, [], {})
    assert out.read_bytes() == b"old evidence"


def test_existing_companion_is_preserved(tmp_path):
    out = tmp_path / "report.jsonl"
    companion = out.with_suffix(".summary.json")
    companion.write_bytes(b"old summary")
    with pytest.raises(FileExistsError):
        checker.write_reports(out, [], {})
    assert not out.exists()


def test_frozen_scope_rows_match_all_sources():
    rows, bindings = checker.load_bound_rows()
    assert len(rows) == 761
    assert len(bindings) == 24


def test_incomplete_packet_is_rejected(tmp_path):
    packet = tmp_path / checker.PACKET
    packet.mkdir(parents=True)
    data = b""
    (packet / "priority-task-references.jsonl").write_bytes(data)
    (packet / "delivery-manifest.json").write_text(json.dumps({"artifacts": [
        {"path": "priority-task-references.jsonl", "raw_sha256": checker.digest(data), "bytes": 0}]}))
    with pytest.raises(ValueError, match="scope is incomplete"):
        checker.load_bound_rows(tmp_path)


@pytest.mark.parametrize("text", [r"$\pi\approx4m/n$", r"$x\simeq2$"])
def test_approximation_control_word_ends_before_a_digit(text):
    record = {"id": "adjacent", "problem": "p", "solution": text, "answer": "a"}
    assert {"field": "solution", "code": "approximation_requires_exact_form"} in checker.check_record(record)["issues"]
