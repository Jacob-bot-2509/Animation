"""Extract the 47 active train records (manifest-bound) for core-family
identification. Read-only; writes a raw work file under
reviews/2026-10-06-core-families/."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/manifest.json"
OUT = ROOT / "reviews/2026-10-06-core-families"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    try:
        m = json.loads(MANIFEST.read_text("utf-8"))
        recs = []
        for e in m["entries"]:
            if e.get("split") != "train" or "leakage-isolated-v3" not in e.get("path", ""):
                continue
            p = ROOT / "data" / e["path"]
            if sha(p) != e["sha256"]:
                raise ValueError("manifest hash mismatch: " + e["path"])
            for i, line in enumerate(p.read_text("utf-8-sig").splitlines(), 1):
                if not line.strip():
                    continue
                r = json.loads(line)
                recs.append({
                    "file": e["path"].replace("\\", "/").split("/")[-1],
                    "line": i,
                    "record_sha256": hashlib.sha256(line.encode("utf-8")).hexdigest(),
                    "id": r["id"], "category": r["category"],
                    "sub_category": r.get("sub_category", ""),
                    "problem": r["problem"],
                    "answer": r.get("answer", ""),
                })
        if len(recs) != 47:
            raise ValueError("expected 47 train records, got " + str(len(recs)))
        if len({r["id"] for r in recs}) != 47:
            raise ValueError("duplicate train ids")
        recs.sort(key=lambda r: r["id"])
        OUT.mkdir(parents=True, exist_ok=True)
        raw = OUT / "train-47-raw.json"
        if raw.exists():
            raise ValueError("raw output exists")
        raw.write_text(json.dumps({
            "schema": "train-47-raw-v1",
            "manifest_sha256": sha(MANIFEST),
            "records": recs,
        }, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
        print("records:", len(recs), "->", raw)
        return 0
    except Exception as exc:
        print("[FAIL]", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
