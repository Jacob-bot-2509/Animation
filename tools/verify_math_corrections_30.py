"""Reconstruct and bind the 30 corrected records; this is not a new mathematical proof."""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("scoped_verifier", ROOT / "tools/verify_codex_supervision.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)
SUP = v.SUP


def load_verified_math(root: Path = ROOT):
    verified = v.verify(root)
    if verified["overall"] != "PASS_SCOPED_EVIDENCE_VERIFICATION":
        raise v.VerificationError("input delivery verification failed: " + str(verified["checks"]))
    patches = v.read_jsonl(root / SUP / "math-corrections-30.jsonl")
    by_source = {(p["source"]["source_path"], p["source"]["source_line"]): p for p in patches}
    bindings = v.read_json(root / SUP / "candidate-source-bindings.json")
    if not isinstance(bindings, list) or len(bindings) != 5:
        raise v.VerificationError("five candidate source bindings required")
    seen = set()
    for b in bindings:
        before_path = b["before"]["path"]
        if before_path in seen:
            raise v.VerificationError("duplicate candidate source")
        seen.add(before_path)
        v.check_binding(root, b["before"])
        v.check_binding(root, b["candidate"])
        cp = v.inside(root, b["candidate"]["path"])
        if cp.relative_to((root / SUP / "corrected-sources").resolve()).as_posix() != before_path:
            raise v.VerificationError("candidate path/source mismatch")
        before = v.inside(root, before_path).read_bytes().splitlines(keepends=True)
        after = cp.read_bytes().splitlines(keepends=True)
        expected_lines = sorted(line for path, line in by_source if path == before_path)
        if b["changed_source_lines"] != expected_lines or len(before) != len(after):
            raise v.VerificationError("source coverage or line count mismatch")
        for line, (old, new) in enumerate(zip(before, after), 1):
            patch = by_source.get((before_path, line))
            if patch:
                if json.loads(new.decode("utf-8-sig")) != patch["corrected_record"]:
                    raise v.VerificationError("candidate corrected record mismatch")
            elif old != new:
                raise v.VerificationError("unchanged candidate line drift")
    if seen != {p["source"]["source_path"] for p in patches}:
        raise v.VerificationError("candidate sources incomplete")
    return patches, bindings


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args(argv)
    try:
        rows, bindings = load_verified_math()
        result = {"result": "PASS_SOURCE_AND_RECORD_RECONSTRUCTION",
                  "corrected_records": len(rows), "source_files": len(bindings),
                  "by_group": v.correction_counts(rows)["by_group"],
                  "new_math_proof_claimed": False, "active_admission": "PENDING"}
        if args.out: v.write_output(ROOT, args.out, result)
        rc = 0
    except (OSError, ValueError, KeyError, TypeError, IndexError) as exc:
        result = {"result": "FAIL", "error": type(exc).__name__ + ": " + str(exc)}
        rc = 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
