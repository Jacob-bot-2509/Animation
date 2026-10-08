from __future__ import annotations
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("math_batch", ROOT / "tools/math_review_batch.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


@pytest.fixture
def fixture(tmp_path, monkeypatch):
    root = tmp_path
    data = m.canonical({"id": "r", "problem": "1+1", "solution": "1+1=2", "answer": "2"}) + b"\n"
    (root / "source.jsonl").write_bytes(data)
    ref = {"id": "r", "group": "train", "source_path": "source.jsonl", "source_line": 1,
           "source_raw_sha256": m.digest(data),
           "record_version_sha256": m.digest(m.canonical(m.json_bytes(data)))}
    # Use the same canonical algorithm for record version hashes.
    ref["record_version_sha256"] = m.digest(m.canonical(m.json_bytes(data)))
    monkeypatch.setattr(m, "load_bound_refs", lambda root=None: [ref])
    inputs = root / "tools/review-batches"
    inputs.mkdir(parents=True)
    (inputs / "sample.json").write_text(json.dumps({"batch": "sample", "ids": ["r"]}), encoding="utf-8")
    (inputs / "sample-verdicts.jsonl").write_text(
        json.dumps({"id": "r", "verdict": "MATH_PASS", "findings": "Exact identity 1+1=2."}) + "\n",
        encoding="utf-8")
    return root, ref


def build(root):
    return m.build_bundle("sample", Path("reviews/new"), root)


def refresh(dest, name):
    receipt = m.json_bytes((dest / "batch-receipt.json").read_bytes())
    receipt["files"][name] = m.binding(name, (dest / name).read_bytes())
    (dest / "batch-receipt.json").write_bytes(m.encode(receipt))


def test_version_bound_packaging_is_not_math_acceptance(fixture):
    root, _ = fixture
    result = build(root)
    dest = root / "reviews/new"
    receipt = result["receipt"]
    assert "batch-receipt.json" not in receipt["files"]
    assert receipt["mathematical_acceptance_claimed"] is False
    assert m.verify_bundle(dest, root)["independent_math_verdict"] == "NOT_ESTABLISHED"


@pytest.mark.parametrize("ids", [[], ["r", "r"], [None], [""], ["unknown"], ["calc-series-015"]])
def test_bad_specs_rejected_before_writes(fixture, ids):
    root, _ = fixture
    (root / "tools/review-batches/sample.json").write_bytes(m.encode({"batch": "sample", "ids": ids}))
    with pytest.raises((ValueError, KeyError)):
        build(root)
    assert not (root / "reviews/new").exists()


def test_wrong_batch_identity(fixture):
    root, _ = fixture
    (root / "tools/review-batches/sample.json").write_bytes(m.encode({"batch": "other", "ids": ["r"]}))
    with pytest.raises(ValueError, match="identity"):
        build(root)


@pytest.mark.parametrize("change", ["source", "dense", "identity", "line", "path"])
def test_source_bindings_checked_on_bundle(fixture, change):
    root, ref = fixture
    if change == "source":
        (root / "source.jsonl").write_bytes(b'{"id":"r","answer":"3"}\n')
    elif change == "dense":
        ref["record_version_sha256"] = "0" * 64
    elif change == "identity":
        ref["id"] = "different"
    elif change == "line":
        ref["source_line"] = 0
    elif change == "path":
        ref["source_path"] = "../outside.jsonl"
    with pytest.raises((ValueError, KeyError)):
        build(root)
    assert not (root / "reviews/new").exists()


@pytest.mark.parametrize("row", [
    {}, {"id": "r", "verdict": "PASS", "findings": "x"},
    {"id": "r", "verdict": "MATH_PASS", "findings": ""},
    {"id": "r", "verdict": "MATH_PASS", "findings": "x", "record_version_sha256": "0" * 64},
])
def test_missing_rationale_or_false_binding_rejected(fixture, row):
    root, _ = fixture
    (root / "tools/review-batches/sample-verdicts.jsonl").write_bytes(m.encode_rows([row]))
    with pytest.raises(ValueError):
        build(root)


def test_duplicate_verdicts_rejected(fixture):
    root, _ = fixture
    p = root / "tools/review-batches/sample-verdicts.jsonl"
    p.write_bytes(p.read_bytes() * 2)
    with pytest.raises(ValueError, match="duplicate"):
        build(root)


def test_empty_verdicts_rejected(fixture):
    root, _ = fixture
    (root / "tools/review-batches/sample-verdicts.jsonl").write_bytes(b"")
    with pytest.raises(ValueError):
        build(root)


def test_existing_bundle_preserved_byte_for_byte(fixture):
    root, _ = fixture
    build(root)
    dest = root / "reviews/new"
    before = {p.name: p.read_bytes() for p in dest.iterdir()}
    with pytest.raises(FileExistsError):
        build(root)
    assert {p.name: p.read_bytes() for p in dest.iterdir()} == before


@pytest.mark.parametrize("path", [
    Path("../outside"), Path("tools/new"),
    m.PACKET / "new",
    Path("reviews/codex-supervision/2026-10-07-core-verifier-followup/new"),
])
def test_output_escape_and_frozen_package_rejected(fixture, path):
    root, _ = fixture
    with pytest.raises(ValueError):
        m.build_bundle("sample", path, root)


@pytest.mark.parametrize("batch", ["../sample", "sample/../other", "", "SAMPLE", "sample.json"])
def test_batch_path_injection_rejected(batch):
    with pytest.raises(ValueError):
        m.batch_name(batch)


@pytest.mark.parametrize("mutation", ["count", "binding", "scope", "empty", "self", "extra", "duplicate", "packager"])
def test_rehashed_internally_invalid_bundle_rejected(fixture, mutation):
    root, _ = fixture
    build(root)
    dest = root / "reviews/new"
    if mutation in {"count", "scope"}:
        p = dest / "batch-report.json"
        value = m.json_bytes(p.read_bytes())
        value["pass" if mutation == "count" else "PASS_CORE_SCOPE_issued"] = 99 if mutation == "count" else True
        p.write_bytes(m.encode(value))
        refresh(dest, p.name)
    elif mutation == "binding":
        p = dest / "batch-verdicts.jsonl"
        rows = m.jsonl_bytes(p.read_bytes())
        rows[0]["record_version_sha256"] = "0" * 64
        p.write_bytes(m.encode_rows(rows))
        refresh(dest, p.name)
    elif mutation == "empty":
        p = dest / "batch-verdicts.jsonl"
        p.write_bytes(b"")
        refresh(dest, p.name)
    elif mutation == "duplicate":
        p = dest / "batch-verdicts.jsonl"
        p.write_bytes(p.read_bytes() * 2)
        refresh(dest, p.name)
    elif mutation == "packager":
        p = dest / "packager.py"
        p.write_bytes(p.read_bytes() + b"\n# changed source\n")
        refresh(dest, p.name)
    elif mutation == "self":
        p = dest / "batch-receipt.json"
        receipt = m.json_bytes(p.read_bytes())
        receipt["files"][p.name] = m.binding(p.name, p.read_bytes())
        p.write_bytes(m.encode(receipt))
    else:
        (dest / "extra.txt").write_bytes(b"hidden")
    with pytest.raises(ValueError):
        m.verify_bundle(dest, root)


def test_changed_source_after_bundle_rejected(fixture):
    root, _ = fixture
    build(root)
    (root / "source.jsonl").write_bytes(b"modified")
    with pytest.raises(ValueError, match="source"):
        m.verify_bundle(root / "reviews/new", root)


def test_issue_packaging_retains_authored_verdict_without_acceptance(fixture):
    root, _ = fixture
    (root / "tools/review-batches/sample-verdicts.jsonl").write_bytes(m.encode_rows([
        {"id": "r", "verdict": "MATH_ISSUE", "findings": "Needs a stated hypothesis."}]))
    result = build(root)
    assert result["receipt"]["verdict_counts"]["issue"] == 1
    assert result["receipt"]["mathematical_acceptance_claimed"] is False


def test_cli_binding_failure_returns_nonzero(fixture, monkeypatch, capsys):
    root, _ = fixture
    monkeypatch.setattr(m, "ROOT", root)
    (root / "source.jsonl").write_bytes(b"modified")
    assert m.main(["bundle", "--batch", "sample", "--out", "reviews/new"]) == 1
    assert json.loads(capsys.readouterr().out)["status"] == "FAIL"


def test_live_frozen_scope_integrity():
    # Independent imports avoid the fixture's replaced reference loader.
    live_spec = importlib.util.spec_from_file_location("batch_live", ROOT / "tools/math_review_batch.py")
    live = importlib.util.module_from_spec(live_spec)
    live_spec.loader.exec_module(live)
    refs = live.load_bound_refs(ROOT)
    assert len(refs) == 761
    for name in ("batch1-train-calc", "batch2-train-linalg-prob", "batch3-train-geom"):
        spec = live.json_bytes((ROOT / f"tools/review-batches/{name}.json").read_bytes())
        records, _ = live.bound_records(ROOT, spec, name)
        assert records


def test_frozen_manifest_not_replaceable(tmp_path):
    packet = tmp_path / m.PACKET
    packet.mkdir(parents=True)
    (packet / "delivery-manifest.json").write_bytes(b'{"artifacts":[]}')
    with pytest.raises(ValueError, match="manifest"):
        m.load_bound_refs(tmp_path)
