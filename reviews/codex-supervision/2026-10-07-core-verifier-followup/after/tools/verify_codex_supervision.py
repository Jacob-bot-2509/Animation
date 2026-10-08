"""Independently verify scoped evidence bindings and counts, never mathematical acceptance."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUP = Path("reviews/codex-supervision/2026-10-07-core-submission-supervision")
PACKET = Path("reviews/codex-supervision/2026-10-07-core-evidence-digest")
SUBMISSION = Path("reviews/2026-10-07-gap-materials/core-submission-v1")
MANIFEST_SHA = "1b92fa5d8c65fc57ff5d978921c80b95de3be2cf4631b635cbf3fa48af7160d5"
SHA_PATTERN = re.compile(r"[0-9a-f]{64}\Z")


class VerificationError(ValueError):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: dict) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def inside(base: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative.strip():
        raise VerificationError("missing relative path")
    rel = Path(relative)
    path = (base / rel).resolve()
    if rel.is_absolute() or ".." in rel.parts or not path.is_relative_to(base.resolve()):
        raise VerificationError("path outside binding root: " + relative)
    return path


def check_binding(base: Path, binding: dict) -> dict:
    if not isinstance(binding, dict):
        raise VerificationError("binding must be an object")
    expected_sha = binding.get("raw_sha256")
    size = binding.get("bytes")
    if not isinstance(expected_sha, str) or not SHA_PATTERN.fullmatch(expected_sha):
        raise VerificationError("invalid raw SHA256")
    if type(size) is not int or size < 0:
        raise VerificationError("invalid byte count")
    path = inside(base, binding.get("path"))
    data = path.read_bytes()
    if digest(data) != expected_sha or len(data) != size:
        raise VerificationError("SHA/size mismatch: " + str(binding["path"]))
    return dict(binding)


def verify_artifacts(base: Path, manifest: dict, expected_count: int = 58) -> dict:
    artifacts = manifest.get("artifacts") if isinstance(manifest, dict) else None
    if not isinstance(artifacts, list) or len(artifacts) != expected_count or not artifacts:
        raise VerificationError("incomplete artifact manifest")
    seen = set()
    for binding in artifacts:
        if not isinstance(binding, dict):
            raise VerificationError("invalid artifact entry")
        path = inside(base, binding.get("path"))
        if path in seen:
            raise VerificationError("duplicate artifact path")
        seen.add(path)
        check_binding(base, binding)
    return {"artifact_count": len(artifacts), "verified_artifacts": len(seen)}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_jsonl(path: Path) -> list[dict]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines()
            if line.strip()]
    if not rows or any(not isinstance(x, dict) for x in rows):
        raise VerificationError("empty or malformed JSONL")
    return rows


def consistency_counts(rows: list[dict]) -> dict:
    if not rows:
        raise VerificationError("empty report")
    statuses = Counter()
    tail = decimal = 0
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("status"), str):
            raise VerificationError("missing report status")
        issues = row.get("issues")
        if not isinstance(issues, list):
            raise VerificationError("issues must be an array")
        codes = set()
        decimal_answer = False
        for issue in issues:
            if isinstance(issue, str):
                codes.add(issue)
                decimal_answer |= issue == "decimal_in_answer"
            elif isinstance(issue, dict) and isinstance(issue.get("code"), str):
                codes.add(issue["code"])
                decimal_answer |= (issue["code"] == "decimal_requires_exact_form"
                                   and issue.get("field") == "answer")
            else:
                raise VerificationError("unsupported issue shape")
        statuses[row["status"]] += 1
        tail += ("tail_mismatch" in codes
                 or row.get("tail_text_relation") == "DIFFERENT_TEXT_UNRESOLVED")
        decimal += decimal_answer
    return {"total": len(rows), "status_counts": dict(statuses),
            "tail_mismatch_rows": tail, "decimal_answer_rows": decimal}


def review_index_summary(index: dict, refs: list[dict]) -> dict:
    ids = index.get("ids") if isinstance(index, dict) else None
    if not isinstance(ids, list) or not ids:
        raise VerificationError("missing explicit ids array")
    pairs = []
    for entry in ids:
        if (not isinstance(entry, list) or len(entry) != 2
                or any(not isinstance(x, str) or not x.strip() for x in entry)):
            raise VerificationError("review ID must be [split,id]")
        pairs.append(tuple(entry))
    if len(set(pairs)) != len(pairs):
        raise VerificationError("duplicate review identity")
    draft_ids = {r["id"] for r in refs if r.get("group") == "selected_draft"}
    if not draft_ids or any(not isinstance(x, str) or not x for x in draft_ids):
        raise VerificationError("missing draft IDs")
    intersection = sorted({rid for _, rid in pairs} & draft_ids)
    return {"review_count": len(pairs), "by_split": dict(Counter(split for split, _ in pairs)),
            "draft_count": len(draft_ids), "draft_id_intersection_count": len(intersection),
            "draft_id_intersection": intersection,
            "risky_is_not_an_additional_identity_list": True}


def correction_counts(rows: list[dict]) -> dict:
    if not rows:
        raise VerificationError("empty corrections")
    seen = set()
    groups = Counter()
    for row in rows:
        source = row.get("source")
        record = row.get("corrected_record")
        if not isinstance(source, dict) or not isinstance(source.get("group"), str):
            raise VerificationError("missing source.group")
        rid = row.get("id")
        if not isinstance(rid, str) or not rid or rid in seen:
            raise VerificationError("missing or duplicate corrected ID")
        seen.add(rid)
        if not isinstance(record, dict) or record.get("id") != rid or source.get("id") != rid:
            raise VerificationError("corrected identity mismatch")
        if digest(canonical(record)) != row.get("after_record_dense_sha256"):
            raise VerificationError("corrected record SHA mismatch")
        if row.get("before_record_dense_sha256") != source.get("record_version_sha256"):
            raise VerificationError("input record SHA mismatch")
        fields = {k: record.get(k) for k in ("problem", "solution", "answer")}
        if fields != row.get("after_math_fields"):
            raise VerificationError("corrected mathematical fields mismatch")
        groups[source["group"]] += 1
    return {"correction_count": len(rows), "by_group": dict(groups)}


def check_delivery(root: Path) -> dict:
    base = root / SUP
    data = (base / "delivery-manifest.json").read_bytes()
    if digest(data) != MANIFEST_SHA or len(data) != 11347:
        raise VerificationError("delivery manifest differs from msg644 fixed binding")
    return verify_artifacts(base, json.loads(data.decode("utf-8-sig")))


def check_ab(root: Path) -> dict:
    index = read_json(root / SUP / "submission-index.corrected-v2.json")
    return {"A": check_binding(root, index["A"]), "B": check_binding(root, index["B"])}


def check_consistency(root: Path) -> dict:
    binding = {
        "path": (SUBMISSION / "consistency-report.jsonl").as_posix(),
        "raw_sha256": "25013b85c95501ebd010defeb1fef5e353726f0598d692a1ea58d8f43bf61fab",
        "bytes": 139100,
    }
    check_binding(root, binding)
    result = consistency_counts(read_jsonl(root / binding["path"]))
    expected = {"total": 761, "status_counts": {"PASS": 158, "FAIL": 603},
                "tail_mismatch_rows": 602, "decimal_answer_rows": 11}
    if result != expected:
        raise VerificationError("original report counts disagree: " + str(result))
    return result


def read_bound_refs(root: Path) -> list[dict]:
    check_binding(root / PACKET, {"path": "delivery-manifest.json",
        "raw_sha256": "792ea93f97a9897e95e91658c5506a40c753c96ef47fb28912383d10a8a93df3",
        "bytes": 10732})
    manifest = read_json(root / PACKET / "delivery-manifest.json")
    binding = next(x for x in manifest["artifacts"] if x["path"] == "priority-task-references.jsonl")
    check_binding(root / PACKET, binding)
    refs = read_jsonl(root / PACKET / binding["path"])
    if Counter(x.get("group") for x in refs) != {
            "train": 47, "selected_draft": 264, "eval": 300, "test": 150}:
        raise VerificationError("incomplete 761-row priority scope")
    if len({(x["source_path"], x["source_line"]) for x in refs}) != 761:
        raise VerificationError("duplicate priority identity")
    return refs


def check_review_index(root: Path) -> dict:
    check_binding(root, {"path": "outputs/review-ids.json",
        "raw_sha256": "178a1bb409cb67f6211bfbb1ffa3520e5986bd5a77432264ba250f029729ade7",
        "bytes": 10929})
    result = review_index_summary(read_json(root / "outputs/review-ids.json"), read_bound_refs(root))
    if (result["review_count"] != 296 or result["by_split"] != {"train": 46, "eval": 100, "test": 150}
            or result["draft_count"] != 264 or result["draft_id_intersection_count"] != 0):
        raise VerificationError("review input scope disagrees: " + str(result))
    return result


def check_corrections(root: Path) -> dict:
    rows = read_jsonl(root / SUP / "math-corrections-30.jsonl")
    result = correction_counts(rows)
    if result != {"correction_count": 30, "by_group": {"train": 9, "eval": 9, "test": 12}}:
        raise VerificationError("correction scope disagrees: " + str(result))
    refs = {(x["source_path"], x["source_line"]): x for x in read_bound_refs(root)}
    cache = {}
    for patch in rows:
        source = patch["source"]
        key = (source["source_path"], source["source_line"])
        if refs.get(key) != source:
            raise VerificationError("correction source not in bound scope")
        if source["source_path"] not in cache:
            data = inside(root, source["source_path"]).read_bytes()
            cache[source["source_path"]] = (data, data.splitlines())
        data, lines = cache[source["source_path"]]
        if digest(data) != source["source_raw_sha256"]:
            raise VerificationError("current source bytes changed")
        before = json.loads(lines[source["source_line"] - 1].decode("utf-8-sig"))
        after = patch["corrected_record"]
        if digest(canonical(before)) != patch["before_record_dense_sha256"]:
            raise VerificationError("before record SHA mismatch")
        if {k: before[k] for k in ("problem", "solution", "answer")} != patch["before_math_fields"]:
            raise VerificationError("before mathematical fields mismatch")
        if ({k: v for k, v in before.items() if k not in ("problem", "solution", "answer")}
                != {k: v for k, v in after.items() if k not in ("problem", "solution", "answer")}):
            raise VerificationError("non-mathematical fields changed")
        changed = [k for k in ("problem", "solution", "answer") if before[k] != after[k]]
        if not changed or patch.get("changed_fields") != changed:
            raise VerificationError("changed field declaration mismatch")
    result["input_and_corrected_dense_record_sha_verified"] = True
    return result


def verify(root: Path = ROOT) -> dict:
    checks = {}
    for name, function in (("delivery", check_delivery), ("AB", check_ab),
                           ("original_consistency", check_consistency),
                           ("review_input_scope", check_review_index),
                           ("correction_structure", check_corrections)):
        try:
            checks[name] = {"status": "PASS_SCOPED_EVIDENCE_CHECK", "result": function(root)}
        except (OSError, ValueError, KeyError, TypeError, IndexError, StopIteration) as exc:
            checks[name] = {"status": "FAIL", "error": type(exc).__name__ + ": " + str(exc)}
    passed = all(x["status"] == "PASS_SCOPED_EVIDENCE_CHECK" for x in checks.values())
    return {"schema": "codex-supervision-independent-verification-v2",
            "overall": "PASS_SCOPED_EVIDENCE_VERIFICATION" if passed else "FAIL",
            "checks": checks, "full_761_math_verdict": "NOT_ESTABLISHED",
            "semantic_isolation_verdict": "NOT_ESTABLISHED",
            "active_data_admission": "PENDING", "PASS_CORE_SCOPE_issued": False}


def write_output(root: Path, relative: Path, result: dict) -> None:
    path = (root / relative).resolve()
    if (not path.is_relative_to((root / "reviews").resolve())
            or path.is_relative_to((root / SUP).resolve())
            or path.is_relative_to((root / PACKET).resolve())):
        raise VerificationError("output must be a new review outside prior frozen deliveries")
    if path.exists():
        raise FileExistsError("preserve previous verification output")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    result = verify()
    if args.out is not None:
        try:
            write_output(ROOT, args.out, result)
        except (OSError, ValueError) as exc:
            result["overall"] = "FAIL_OUTPUT"
            result["output_error"] = type(exc).__name__ + ": " + str(exc)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["overall"] == "PASS_SCOPED_EVIDENCE_VERIFICATION" else 1


if __name__ == "__main__":
    raise SystemExit(main())
