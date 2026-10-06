"""Verify Codex's scene-repair-takeover claims on disk (read-only)."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUP = ROOT / "reviews/codex-supervision/2026-10-06-scene-repair-takeover"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    try:
        print("== 1. chunks restoration ==")
        listing = json.loads((ROOT / "reviews/2026-10-06-scene-standard-sweep/chunks/listing.json")
                             .read_text("utf-8"))
        bad = [(n, s[:12], sha(ROOT / "reviews/2026-10-06-scene-standard-sweep/chunks" / n)[:12])
               for n, s in listing["chunks"].items()
               if sha(ROOT / "reviews/2026-10-06-scene-standard-sweep/chunks" / n) != s]
        print("  chunks SHA match:", not bad, "| mismatches:", bad)

        print("== 2. inputs-v2 ==")
        d = json.loads((SUP / "inputs-v2/inputs.json").read_text("utf-8"))
        chunks = d.get("chunks", [])
        recs = [r for c in chunks for r in (c.get("records", []) if isinstance(c, dict) else [])]
        ids = [r.get("id") if isinstance(r, dict) else str(r)[:20] for r in recs]
        print("  chunks:", len(chunks), "| records:", len(recs), "| unique ids:", len(set(ids)))

        print("== 3. math-corrected-v1 ==")
        mc = SUP / "math-corrected-v1"
        total = 0
        for p in sorted(mc.glob("*.jsonl")):
            n = sum(1 for l in p.read_text("utf-8").splitlines() if l.strip())
            total += n
            print("  ", p.name, n)
        print("  total records:", total)

        print("== 4. scene-candidates-53-v4 ==")
        sc = SUP / "scene-candidates-53-v4"
        files = sorted(sc.glob("*.json")) if sc.exists() else []
        print("  files:", [f.name for f in files])
        if files:
            cand = json.loads(files[0].read_text("utf-8"))
            print("  sample keys:", list(cand.keys())[:8] if isinstance(cand, dict) else type(cand))

        print("== 5. remaining 90 ==")
        ev = json.loads((SUP / "workflow-evidence-analysis.json").read_text("utf-8"))
        print("  keys:", list(ev.keys())[:8])
        for k in ev:
            v = ev[k]
            if isinstance(v, list) and v and isinstance(v[0], str):
                print("  ", k, ":", len(v), "e.g.", v[:5])
        return 0
    except Exception as exc:
        print("[FAIL]", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
