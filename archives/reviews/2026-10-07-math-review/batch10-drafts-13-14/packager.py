"""Package version-bound authored math reviews; packaging never proves mathematics."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = Path("reviews/codex-supervision/2026-10-07-core-evidence-digest")
OUT_DIR = ROOT / "reviews/2026-10-07-math-review"
MANIFEST_SHA = "792ea93f97a9897e95e91658c5506a40c753c96ef47fb28912383d10a8a93df3"
MANIFEST_BYTES = 10732
CORRECTED = {
    "calc-series-015", "calc-series-020", "linalg-050", "linalg-070",
    "prob-038", "prob-039", "prob-042", "prob-043", "prob-046",
    "eval-calc-015-s3", "eval-calc-026-s3", "eval-calc-027-s3",
    "eval-prob-007-s1", "eval-prob-007-s2", "eval-prob-007-s3",
    "eval-prob-008-s1", "eval-prob-008-s2", "eval-prob-008-s3",
    "test-calc-027", "test-prob-001", "test-prob-002", "test-prob-005",
    "test-prob-007", "test-prob-008", "test-prob-016", "test-prob-020",
    "test-prob-021", "test-linalg-012", "test-x-004", "test-x-015",
}
FILES = {"batch-report.json", "batch-verdicts.jsonl", "batch-spec.json",
         "review-input-verdicts.jsonl", "input-bindings.json", "packager.py"}
STATUSES = {"MATH_PASS": "pass", "MATH_ISSUE": "issue", "NEEDS_CODEX": "needs_codex"}
SHA_RE = re.compile(r"[0-9a-f]{64}\Z")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(record) -> bytes:
    return json.dumps(record, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def inside(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative.strip():
        raise ValueError("missing relative path")
    rel = Path(relative)
    path = (root / rel).resolve()
    if rel.is_absolute() or ".." in rel.parts or not path.is_relative_to(root.resolve()):
        raise ValueError("path outside project: " + relative)
    return path


def json_bytes(data: bytes):
    return json.loads(data.decode("utf-8-sig"))


def jsonl_bytes(data: bytes) -> list[dict]:
    rows = [json.loads(line) for line in data.decode("utf-8-sig").splitlines() if line.strip()]
    if not rows or any(not isinstance(x, dict) for x in rows):
        raise ValueError("empty or malformed review rows")
    return rows


def binding(relative: str, data: bytes) -> dict:
    return {"path": relative, "raw_sha256": digest(data), "bytes": len(data)}


def load_bound_refs(root: Path | None = None) -> list[dict]:
    root = ROOT if root is None else root
    base = root / PACKET
    data = (base / "delivery-manifest.json").read_bytes()
    if digest(data) != MANIFEST_SHA or len(data) != MANIFEST_BYTES:
        raise ValueError("frozen core manifest changed")
    manifest = json_bytes(data)
    entries = [x for x in manifest["artifacts"] if x.get("path") == "priority-task-references.jsonl"]
    if len(entries) != 1:
        raise ValueError("missing or duplicate core references binding")
    expected = entries[0]
    refs_bytes = (base / "priority-task-references.jsonl").read_bytes()
    if digest(refs_bytes) != expected["raw_sha256"] or len(refs_bytes) != expected["bytes"]:
        raise ValueError("core references SHA/size changed")
    refs = jsonl_bytes(refs_bytes)
    if Counter(r.get("group") for r in refs) != {
            "train": 47, "selected_draft": 264, "eval": 300, "test": 150}:
        raise ValueError("incomplete frozen 761-row scope")
    if len({r["id"] for r in refs}) != len(refs) or len({
            (r["source_path"], r["source_line"]) for r in refs}) != len(refs):
        raise ValueError("duplicate frozen identity")
    return refs


def batch_name(batch: str) -> str:
    if not isinstance(batch, str) or not re.fullmatch(r"[a-z][a-z0-9-]{0,79}", batch):
        raise ValueError("invalid batch name")
    return batch


def validate_spec(spec: dict, batch: str) -> list[str]:
    batch_name(batch)
    if not isinstance(spec, dict) or spec.get("batch") != batch:
        raise ValueError("batch identity mismatch")
    ids = spec.get("ids")
    if (not isinstance(ids, list) or not ids or
            any(not isinstance(rid, str) or not rid.strip() for rid in ids)):
        raise ValueError("missing nonempty batch IDs")
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate batch IDs")
    if set(ids) & CORRECTED:
        raise ValueError("previously corrected IDs require their candidate-version workflow")
    return ids


def bound_records(root: Path, spec: dict, batch: str) -> tuple[list[dict], list[dict]]:
    ids = validate_spec(spec, batch)
    refs = load_bound_refs(root)
    by_id = {r["id"]: r for r in refs}
    cache = {}
    out, sources = [], {}
    for rid in ids:
        if rid not in by_id:
            raise ValueError("batch ID outside frozen scope: " + rid)
        ref = by_id[rid]
        src = ref["source_path"]
        if src not in cache:
            data = inside(root, src).read_bytes()
            cache[src] = (data, data.splitlines())
        data, lines = cache[src]
        if digest(data) != ref["source_raw_sha256"]:
            raise ValueError("source version changed: " + src)
        line = ref["source_line"]
        if type(line) is not int or not 1 <= line <= len(lines):
            raise ValueError("source line out of range: " + rid)
        record = json_bytes(lines[line - 1])
        if not isinstance(record, dict) or record.get("id") != rid:
            raise ValueError("record identity mismatch: " + rid)
        if digest(canonical(record)) != ref["record_version_sha256"]:
            raise ValueError("record version changed: " + rid)
        fields = {k: record.get(k) for k in ("problem", "solution", "answer")}
        if any(not isinstance(x, str) or not x.strip() for x in fields.values()):
            raise ValueError("missing mathematical fields: " + rid)
        out.append({"id": rid, "group": ref["group"], "source_path": src,
                    "source_line": line, "source_raw_sha256": ref["source_raw_sha256"],
                    "record_version_sha256": ref["record_version_sha256"], **fields})
        sources[src] = binding(src, data)
    return out, sorted(sources.values(), key=lambda x: x["path"])


def validate_verdicts(verdicts: list[dict], records: list[dict]) -> list[dict]:
    ids = [v.get("id") for v in verdicts]
    if any(not isinstance(x, str) for x in ids) or len(set(ids)) != len(ids):
        raise ValueError("missing or duplicate verdict ID")
    if set(ids) != {r["id"] for r in records}:
        raise ValueError("verdict IDs differ from batch")
    by_id = {v["id"]: v for v in verdicts}
    rows = []
    for record in records:
        v = by_id[record["id"]]
        if v.get("verdict") not in STATUSES:
            raise ValueError("invalid authored verdict")
        if not isinstance(v.get("findings"), str) or not v["findings"].strip():
            raise ValueError("authored verdict needs a nonempty rationale")
        row = dict(v)
        for key in ("group", "source_path", "source_line",
                    "source_raw_sha256", "record_version_sha256"):
            if key in row and row[key] != record[key]:
                raise ValueError("authored input binding disagrees: " + key)
            row[key] = record[key]
        rows.append(row)
    return rows


def report_for(batch: str, rows: list[dict]) -> dict:
    counts = Counter(STATUSES[x["verdict"]] for x in rows)
    return {"schema": "math-review-batch-v3", "batch": batch, "reviewer": "claude-code",
            "status": "PACKAGED_AUTHORED_REVIEWS", "total": len(rows),
            **{key: counts[key] for key in STATUSES.values()},
            "note": "Source bindings verified; authored math verdicts require independent review.",
            "semantic_isolation_verdict": "NOT_ESTABLISHED",
            "native_render_verdict": "UNVERIFIED", "active_data_admission": "PENDING",
            "production": "CLOSED", "PASS_CORE_SCOPE_issued": False}


def output_path(root: Path, batch: str, destination: Path | None = None) -> Path:
    path = root / "reviews/2026-10-07-math-review" / batch if destination is None else root / destination
    path = path.resolve()
    protected = [PACKET,
        Path("reviews/codex-supervision/2026-10-07-core-submission-supervision"),
        Path("reviews/codex-supervision/2026-10-07-core-verifier-followup")]
    if (not path.is_relative_to((root / "reviews").resolve()) or
            path == (root / "reviews").resolve() or
            any(path.is_relative_to((root / d).resolve()) for d in protected)):
        raise ValueError("output must be a new project review directory outside frozen deliveries")
    if path.exists():
        raise FileExistsError("preserve existing batch; use a new --out")
    return path


def encode(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def encode_rows(rows) -> bytes:
    return b"".join(canonical(row) + b"\n" for row in rows)


def extract(batch: str, root: Path | None = None) -> int:
    root = ROOT if root is None else root
    batch_name(batch)
    spec = json_bytes((root / f"tools/review-batches/{batch}.json").read_bytes())
    records, _ = bound_records(root, spec, batch)
    for record in records:
        print(json.dumps(record, ensure_ascii=False))
    return 0


def build_bundle(batch: str, destination: Path | None = None, root: Path | None = None) -> dict:
    root = ROOT if root is None else root
    batch_name(batch)
    dest = output_path(root, batch, destination)
    spec_path = f"tools/review-batches/{batch}.json"
    verdict_path = f"tools/review-batches/{batch}-verdicts.jsonl"
    spec_bytes = (root / spec_path).read_bytes()
    verdict_bytes = (root / verdict_path).read_bytes()
    records, sources = bound_records(root, json_bytes(spec_bytes), batch)
    rows = validate_verdicts(jsonl_bytes(verdict_bytes), records)
    report = report_for(batch, rows)
    inputs = {
        "schema": "math-review-input-bindings-v3",
        "core_manifest": {"path": (PACKET / "delivery-manifest.json").as_posix(),
                          "raw_sha256": MANIFEST_SHA, "bytes": MANIFEST_BYTES},
        "spec": {**binding(spec_path, spec_bytes), "snapshot": "batch-spec.json"},
        "authored_verdicts": {**binding(verdict_path, verdict_bytes),
                             "snapshot": "review-input-verdicts.jsonl"},
        "sources": sources,
        "packager": {**binding("tools/math_review_batch.py", Path(__file__).read_bytes()), "snapshot": "packager.py"}}
    artifacts = {"batch-report.json": encode(report), "batch-verdicts.jsonl": encode_rows(rows),
                 "batch-spec.json": spec_bytes, "review-input-verdicts.jsonl": verdict_bytes,
                 "input-bindings.json": encode(inputs), "packager.py": Path(__file__).read_bytes()}
    receipt = {"schema": "math-review-batch-receipt-v3", "batch": batch,
               "reviewer": "claude-code", "files": {k: binding(k, data) for k, data in sorted(artifacts.items())},
               "verdict_counts": {k: report[k] for k in ("total", "pass", "issue", "needs_codex")},
               "mathematical_acceptance_claimed": False, "PASS_CORE_SCOPE_issued": False}
    dest.mkdir(parents=True, exist_ok=False)
    for name, data in {**artifacts, "batch-receipt.json": encode(receipt)}.items():
        with (dest / name).open("xb") as stream:
            stream.write(data)
    return {"status": "PACKAGED_AUTHORED_REVIEWS", "output": str(dest), "receipt": receipt}


def bundle(batch: str, destination: Path | None = None) -> int:
    print(json.dumps(build_bundle(batch, destination), ensure_ascii=False, indent=2))
    return 0


def verify_bundle(destination: Path, root: Path | None = None) -> dict:
    root = ROOT if root is None else root
    dest = (root / destination).resolve()
    if not dest.is_relative_to((root / "reviews").resolve()):
        raise ValueError("input outside project reviews")
    receipt = json_bytes((dest / "batch-receipt.json").read_bytes())
    if receipt.get("schema") != "math-review-batch-receipt-v3":
        raise ValueError("unsupported historical receipt schema; preserve original")
    if (set(receipt.get("files", {})) != FILES or
            {p.name for p in dest.iterdir()} != FILES | {"batch-receipt.json"}):
        raise ValueError("incomplete or extra batch artifact")
    artifacts = {}
    for name in sorted(FILES):
        b = receipt["files"][name]
        data = (dest / name).read_bytes()
        if b != binding(name, data):
            raise ValueError("artifact binding mismatch: " + name)
        artifacts[name] = data
    batch = batch_name(receipt.get("batch"))
    records, sources = bound_records(root, json_bytes(artifacts["batch-spec.json"]), batch)
    expected_rows = validate_verdicts(jsonl_bytes(artifacts["review-input-verdicts.jsonl"]), records)
    if jsonl_bytes(artifacts["batch-verdicts.jsonl"]) != expected_rows:
        raise ValueError("packaged rows disagree with authored reviews and frozen sources")
    report = report_for(batch, expected_rows)
    if json_bytes(artifacts["batch-report.json"]) != report:
        raise ValueError("report counts/scope disagree")
    inputs = json_bytes(artifacts["input-bindings.json"])
    expected_core = {"path": (PACKET / "delivery-manifest.json").as_posix(),
                     "raw_sha256": MANIFEST_SHA, "bytes": MANIFEST_BYTES}
    expected_spec = {**binding(f"tools/review-batches/{batch}.json", artifacts["batch-spec.json"]),
                     "snapshot": "batch-spec.json"}
    expected_verdicts = {**binding(f"tools/review-batches/{batch}-verdicts.jsonl",
                                 artifacts["review-input-verdicts.jsonl"]),
                        "snapshot": "review-input-verdicts.jsonl"}
    if (inputs.get("schema") != "math-review-input-bindings-v3" or
            inputs.get("core_manifest") != expected_core or inputs.get("spec") != expected_spec or
            inputs.get("authored_verdicts") != expected_verdicts or inputs.get("sources") != sources):
        raise ValueError("input bindings disagree")
    expected_packager = {**binding("tools/math_review_batch.py", artifacts["packager.py"]),
                         "snapshot": "packager.py"}
    if inputs.get("packager") != expected_packager:
        raise ValueError("packager source snapshot binding mismatch")
    if (receipt.get("reviewer") != "claude-code" or
            receipt.get("verdict_counts") != {k: report[k] for k in ("total", "pass", "issue", "needs_codex")} or
            receipt.get("mathematical_acceptance_claimed") is not False or
            receipt.get("PASS_CORE_SCOPE_issued") is not False):
        raise ValueError("receipt counts/scope disagree")
    return {"status": "PASS_VERSION_BOUND_REVIEW_PACKAGING", "batch": batch,
            "total": len(expected_rows), "artifacts_verified": len(FILES),
            "independent_math_verdict": "NOT_ESTABLISHED",
            "semantic_isolation_verdict": "NOT_ESTABLISHED", "production": "CLOSED"}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("action", choices=["extract", "bundle", "verify"])
    ap.add_argument("--batch")
    ap.add_argument("--out", type=Path)
    ap.add_argument("--input", type=Path)
    args = ap.parse_args(argv)
    try:
        if args.action == "verify":
            if args.input is None or args.batch is not None or args.out is not None:
                raise ValueError("verify requires only --input")
            print(json.dumps(verify_bundle(args.input), ensure_ascii=False, indent=2))
            return 0
        if args.batch is None or args.input is not None or (args.action == "extract" and args.out is not None):
            raise ValueError("extract/bundle require --batch; only bundle accepts --out")
        return extract(args.batch) if args.action == "extract" else bundle(args.batch, args.out)
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        print(json.dumps({"status": "FAIL", "error": type(exc).__name__ + ": " + str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
