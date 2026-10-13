"""Split the pending review packet into self-contained per-chunk files for
the workflow review agents (each agent reads one small file)."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKET = (ROOT / "reviews/codex-supervision/2026-10-06-bound-receipt-semantic-review"
          / "pending-review-packet.json")
OUT = ROOT / "reviews/2026-10-06-linalg048-admission/v3-receipt-bound/review-chunks"
CHUNK = 19
NCHUNKS = 16
LABEL_RULE = ("核心数学对象、条件、目标及求解结构保持不变，仅更换数值、符号或表述"
              "即为泄漏；训练与评测/测试需要隔离。共享知识点本身不足以判泄漏。")


def main() -> int:
    try:
        d = json.loads(PACKET.read_text("utf-8"))
        if len(d["semantic_pairs"]) != 296 or len(d["review_material"]) != 296:
            raise ValueError("unexpected packet size")
        if OUT.exists() and any(OUT.glob("*.json")):
            raise ValueError("chunks exist; use a fresh directory")
        OUT.mkdir(parents=True, exist_ok=True)
        idx = 0
        for ci in range(NCHUNKS):
            pairs = d["semantic_pairs"][idx:idx + CHUNK]
            mat = d["review_material"][idx:idx + CHUNK]
            idx += CHUNK
            (OUT / f"chunk-{ci + 1:02d}.json").write_text(
                json.dumps({"candidate": d["candidate"],
                            "definition": LABEL_RULE,
                            "pairs": pairs, "material": mat},
                           ensure_ascii=False, indent=1) + "\n",
                encoding="utf-8", newline="\n")
        listing = {f.name: hashlib.sha256(f.read_bytes()).hexdigest()
                   for f in sorted(OUT.glob("*.json"))}
        (OUT / "listing.json").write_text(
            json.dumps(listing, indent=2) + "\n", encoding="utf-8", newline="\n")
        print("chunks:", len(listing), "| pairs covered:",
              sum(len(json.loads((OUT / f).read_text("utf-8"))["pairs"])
                  for f in listing))
        return 0
    except Exception as exc:
        print("[FAIL]", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
