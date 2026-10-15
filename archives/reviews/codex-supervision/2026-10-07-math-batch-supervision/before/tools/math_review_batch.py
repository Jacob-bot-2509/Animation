"""剩余题目实际数学复核:批次提取与打包。只读;产出在 reviews/2026-10-07-math-review/."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = Path("reviews/codex-supervision/2026-10-07-core-evidence-digest")
OUT_DIR = ROOT / "reviews/2026-10-07-math-review"
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


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(record: dict) -> bytes:
    return json.dumps(record, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def load_bound_refs() -> list[dict]:
    packet = ROOT / PACKET
    ref_bytes = (packet / "priority-task-references.jsonl").read_bytes()
    man = json.loads((packet / "delivery-manifest.json").read_text(encoding="utf-8-sig"))
    entries = {x["path"]: x for x in man["artifacts"]}
    expected = entries["priority-task-references.jsonl"]
    if digest(ref_bytes) != expected["raw_sha256"]:
        raise ValueError("core packet row bindings changed")
    return [json.loads(line) for line in ref_bytes.decode("utf-8-sig").splitlines() if line.strip()]


def extract(batch: str) -> int:
    spec = json.loads((ROOT / f"tools/review-batches/{batch}.json").read_text(encoding="utf-8-sig"))
    refs = load_bound_refs()
    by_id = {r["id"]: r for r in refs}
    cache = {}
    out = []
    for rid in spec["ids"]:
        ref = by_id.get(rid)
        if ref is None:
            raise ValueError(f"batch id not in frozen bindings: {rid}")
        if rid in CORRECTED:
            raise ValueError(f"batch id already corrected: {rid}")
        src = ref["source_path"]
        if src not in cache:
            data = (ROOT / src).read_bytes()
            if digest(data) != ref["source_raw_sha256"]:
                raise ValueError("source version changed: " + src)
            cache[src] = data.splitlines(keepends=True)
        lines = cache[src]
        rec = json.loads(lines[ref["source_line"] - 1].decode("utf-8-sig"))
        if digest(canonical(rec)) != ref["record_version_sha256"]:
            raise ValueError("record changed: " + rid)
        out.append({
            "id": rid, "group": ref["group"], "source_path": src,
            "source_line": ref["source_line"],
            "record_version_sha256": ref["record_version_sha256"],
            "problem": rec["problem"], "solution": rec["solution"], "answer": rec["answer"],
        })
    print(f"批次 {batch}: {len(out)} 条(绑定校验通过)")
    for i, r in enumerate(out, 1):
        print(f"\n[{i}/{len(out)}] {r['id']} ({r['group']})")
        print(f"题面: {r['problem']}")
        print(f"解析: {r['solution']}")
        print(f"答案: {r['answer']}")
    return 0


def bundle(batch: str) -> int:
    spec = json.loads((ROOT / f"tools/review-batches/{batch}.json").read_text(encoding="utf-8-sig"))
    v_path = ROOT / f"tools/review-batches/{batch}-verdicts.jsonl"
    verdicts = [json.loads(line) for line in v_path.read_text(encoding="utf-8-sig").splitlines()
                if line.strip()]
    if {v["id"] for v in verdicts} != set(spec["ids"]) or len(verdicts) != len(spec["ids"]):
        raise ValueError("verdict id set does not match batch spec")
    refs = load_bound_refs()
    by_id = {r["id"]: r for r in refs}
    rows = []
    for v in verdicts:
        ref = by_id[v["id"]]
        row = dict(v)
        row["source_path"] = ref["source_path"]
        row["source_line"] = ref["source_line"]
        row["record_version_sha256"] = ref["record_version_sha256"]
        if v["verdict"] not in ("MATH_PASS", "MATH_ISSUE", "NEEDS_CODEX"):
            raise ValueError(f"bad verdict: {v['id']}")
        rows.append(row)
    bdir = OUT_DIR / batch
    bdir.mkdir(parents=True, exist_ok=True)
    report = {
        "schema": "math-review-batch-v1", "batch": batch,
        "reviewer": "claude-code", "total": len(rows),
        "pass": sum(1 for r in rows if r["verdict"] == "MATH_PASS"),
        "issue": sum(1 for r in rows if r["verdict"] == "MATH_ISSUE"),
        "needs_codex": sum(1 for r in rows if r["verdict"] == "NEEDS_CODEX"),
        "note": "逐条人工审阅(题面/解析/答案);sympy 辅助核验仅作佐证,不替代审阅结论",
    }
    with (bdir / "batch-report.json").open("w", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write("\n")
    with (bdir / "batch-verdicts.jsonl").open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    files = {}
    for p in sorted(bdir.iterdir()):
        b = p.read_bytes()
        files[p.name] = {"raw_sha256": digest(b), "bytes": len(b)}
    receipt = {
        "schema": "math-review-batch-receipt-v1", "batch": batch,
        "reviewer": "claude-code", "files": files,
        "verdict_counts": {k: report[k] for k in ("total", "pass", "issue", "needs_codex")},
    }
    with (bdir / "batch-receipt.json").open("w", encoding="utf-8", newline="\n") as f:
        json.dump(receipt, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(json.dumps(receipt, ensure_ascii=False, indent=2))
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("action", choices=["extract", "bundle"])
    ap.add_argument("--batch", required=True)
    args = ap.parse_args(argv)
    if args.action == "extract":
        return extract(args.batch)
    return bundle(args.batch)


if __name__ == "__main__":
    raise SystemExit(main())
