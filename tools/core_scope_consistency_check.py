"""Source-bound format diagnostics; never a math or leakage acceptance certificate."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = Path("reviews/codex-supervision/2026-10-07-core-evidence-digest")
DEFAULT_OUT = Path("reviews/2026-10-07-gap-materials/core-submission-v1/consistency-report-v2.jsonl")
DECIMAL = re.compile(r"(?<![\w.])(?:\d+\.\d+|\.\d+)(?![\w.])")
APPROXIMATION = re.compile(r"\\(?:approx|simeq)(?![A-Za-z])|≈|≃")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(record: dict) -> bytes:
    return json.dumps(record, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def escaped(text: str, i: int) -> bool:
    n = 0
    while i > 0 and text[i - 1] == "\\":
        n += 1
        i -= 1
    return n % 2 == 1


def latex_issues(text: str) -> list[str]:
    braces = 0
    math_delimiter = None
    issues = []
    i = 0
    pairs = {"$": "$", "$$": "$$", r"\(": r"\)", r"\[": r"\]"}
    closing = {r"\)", r"\]"}
    while i < len(text):
        token = None
        if text[i] == "$" and not escaped(text, i):
            token = "$$" if text[i:i + 2] == "$$" else "$"
        elif (text[i:i + 2] in {r"\(", r"\)", r"\[", r"\]"}
              and not escaped(text, i)):
            token = text[i:i + 2]
        if token:
            if math_delimiter is None:
                if token in closing:
                    issues.append("unexpected_math_close")
                else:
                    math_delimiter = pairs[token]
            elif token == math_delimiter:
                math_delimiter = None
            else:
                issues.append("mixed_math_delimiters")
            i += len(token)
            continue
        if text[i] == "{" and not escaped(text, i):
            braces += 1
        elif text[i] == "}" and not escaped(text, i):
            braces -= 1
            if braces < 0:
                issues.append("unexpected_brace_close")
                braces = 0
        i += 1
    if braces:
        issues.append("unclosed_brace")
    if math_delimiter is not None:
        issues.append("unclosed_math_delimiter")
    env_stack = []
    for match in re.finditer(r"\\(begin|end)\{([^{}]+)\}", text):
        kind, name = match.groups()
        if kind == "begin":
            env_stack.append(name)
        elif not env_stack or env_stack.pop() != name:
            issues.append("environment_mismatch")
    if env_stack:
        issues.append("unclosed_environment")
    return list(dict.fromkeys(issues))


def latex_balanced(text: str) -> bool:
    return not latex_issues(text)


def norm(expr: str) -> str:
    """Display normalization retains structure; it is not mathematical equivalence."""
    t = expr.strip().rstrip(".。;；")
    if t.startswith("$") and t.endswith("$") and "$" not in t[1:-1]:
        t = t[1:-1]
    elif (t.startswith(r"\(") and t.endswith(r"\)")
          or t.startswith(r"\[") and t.endswith(r"\]")):
        t = t[2:-2]
    for command in (r"\left", r"\right", r"\displaystyle", r"\quad"):
        t = t.replace(command, "")
    t = t.replace(r"\dfrac", r"\frac").replace(r"\tfrac", r"\frac")
    return re.sub(r"\s+", "", t)  # Braces carry mathematical argument structure.


def last_math(solution: str) -> str:
    segments = []
    start = None
    i = 0
    while i < len(solution):
        if solution[i] == "$" and not escaped(solution, i):
            if solution[i:i + 2] == "$$":
                return ""
            if start is None:
                start = i + 1
            else:
                segments.append(solution[start:i])
                start = None
        i += 1
    return segments[-1] if start is None and segments else ""


def check_record(rec: dict, source: dict | None = None) -> dict:
    issues = []
    values = {}
    for field in ("problem", "solution", "answer"):
        value = rec.get(field)
        if value is None or isinstance(value, str) and not value.strip():
            issues.append({"field": field, "code": "empty_field"})
            values[field] = ""
            continue
        if isinstance(value, bool) or not isinstance(value, (str, int)):
            issues.append({"field": field, "code": "invalid_field_type"})
            values[field] = ""
            continue
        if field != "answer" and not isinstance(value, str):
            issues.append({"field": field, "code": "invalid_field_type"})
        text = value if isinstance(value, str) else str(value)
        values[field] = text
        for issue in latex_issues(text):
            issues.append({"field": field, "code": issue})
        if DECIMAL.search(text):
            issues.append({"field": field, "code": "decimal_requires_exact_form"})
        if APPROXIMATION.search(text):
            issues.append({"field": field, "code": "approximation_requires_exact_form"})
    tail = last_math(values.get("solution", ""))
    answer = values.get("answer", "")
    relation = "NOT_COMPARABLE"
    if tail and answer:
        relation = ("DISPLAY_TEXT_MATCH_NO_PROOF" if norm(tail) == norm(answer)
                    else "DIFFERENT_TEXT_UNRESOLVED")
    return {
        "id": rec.get("id"), "source": source,
        "record_dense_sha256": digest(canonical(rec)),
        "status": "NEEDS_CORRECTION" if issues else "DIAGNOSTIC_ONLY",
        "issues": issues, "tail_text_relation": relation,
        "mathematical_verdict": "UNREVIEWED",
        "leakage_verdict": "UNREVIEWED", "accepted": False,
    }


def load_bound_rows(root: Path = ROOT) -> tuple[list[tuple[dict, dict]], list[dict]]:
    packet = root / PACKET
    manifest = json.loads((packet / "delivery-manifest.json").read_text(encoding="utf-8-sig"))
    entries = {x["path"]: x for x in manifest["artifacts"]}
    ref_bytes = (packet / "priority-task-references.jsonl").read_bytes()
    expected = entries["priority-task-references.jsonl"]
    if digest(ref_bytes) != expected["raw_sha256"] or len(ref_bytes) != expected["bytes"]:
        raise ValueError("core packet row bindings changed")
    refs = [json.loads(line) for line in ref_bytes.decode("utf-8-sig").splitlines() if line.strip()]
    if Counter(x["group"] for x in refs) != {
            "train": 47, "selected_draft": 264, "eval": 300, "test": 150}:
        raise ValueError("fixed 761-row core scope is incomplete")
    cache = {}
    rows = []
    seen = set()
    for ref in refs:
        relative = Path(ref["source_path"])
        path = (root / relative).resolve()
        if relative.is_absolute() or not path.is_relative_to(root.resolve()):
            raise ValueError("source outside project")
        if ref["source_path"] not in cache:
            data = path.read_bytes()
            cache[ref["source_path"]] = (data, data.splitlines(keepends=True))
        data, lines = cache[ref["source_path"]]
        if digest(data) != ref["source_raw_sha256"]:
            raise ValueError("source version changed: " + ref["source_path"])
        rec = json.loads(lines[ref["source_line"] - 1].decode("utf-8-sig"))
        if digest(canonical(rec)) != ref["record_version_sha256"] or rec.get("id") != ref["id"]:
            raise ValueError("source record changed: " + str(ref["id"]))
        key = (ref["source_path"], ref["source_line"])
        if key in seen:
            raise ValueError("duplicate source row")
        seen.add(key)
        rows.append((ref, rec))
    bindings = [{"path": name, "raw_sha256": digest(data), "bytes": len(data)}
                for name, (data, _) in sorted(cache.items())]
    return rows, bindings


def write_reports(out: Path, rows: list[dict], summary: dict) -> None:
    companion = out.with_suffix(".summary.json")
    if out.exists() or companion.exists():
        raise FileExistsError("preserve previous report")
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("x", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False) + "\n")
    with companion.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(summary, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args(argv)
    out = (ROOT / args.out).resolve()
    if (not out.is_relative_to((ROOT / "reviews").resolve())
            or out.is_relative_to((ROOT / PACKET).resolve())):
        raise ValueError("output must be a new review artifact outside the frozen core packet")
    bound, bindings = load_bound_rows()
    reports = [check_record(rec, ref) for ref, rec in bound]
    counts = dict(Counter(row["status"] for row in reports))
    summary = {
        "schema": "core-scope-format-diagnostics-v2", "total": len(reports),
        "counts": counts, "source_bindings": bindings, "source_identity": "VERIFIED",
        "mathematical_verdict": "UNREVIEWED", "leakage_verdict": "UNREVIEWED",
        "scope_acceptance": "PENDING", "report_is_acceptance_certificate": False,
        "note": "Text agreement and absence of format flags do not prove any mathematical answer.",
    }
    write_reports(out, reports, summary)
    print(json.dumps(summary, ensure_ascii=False))
    return 1 if counts.get("NEEDS_CORRECTION") else 0


if __name__ == "__main__":
    raise SystemExit(main())
