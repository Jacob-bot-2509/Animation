"""Publish fresh, source-bound chunks joined by subject identity."""
from __future__ import annotations
import argparse
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "src")]
from holdout_contract import Snapshot, LABEL_RULE, write_new_json
from finalize_linalg048_review import PACKET_SHA, read_bound_packet, validate_packet, subject_key


def make_chunks(packet, chunk_size=19, expected_size=296):
    if type(chunk_size) is not int or chunk_size < 1:
        raise ValueError("positive integer chunk size required")
    _, material = validate_packet(packet, expected_size)
    pairs = packet["semantic_pairs"]
    return [{"schema": "linalg048-semantic-review-chunk-v2",
             "packet_raw_sha256": PACKET_SHA, "definition": LABEL_RULE,
             "candidate": packet["candidate"], "pairs": pairs[i:i+chunk_size],
             "material": [material[subject_key(s)] for s in pairs[i:i+chunk_size]]}
            for i in range(0, len(pairs), chunk_size)]


def publish_chunks(out, chunk_size=19):
    out = Path(out).resolve()
    if not out.is_relative_to(ROOT) or out.exists():
        raise ValueError("fresh project chunk directory required")
    snapshot = Snapshot(ROOT)
    packet = read_bound_packet(snapshot)
    chunks = make_chunks(packet, chunk_size)
    for rel in ("tools/split_review_packet.py", "tools/finalize_linalg048_review.py"):
        snapshot.read(ROOT / rel)
    snapshot.check_unchanged()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.mkdir(exist_ok=False)
    files = {}
    for i, chunk in enumerate(chunks, 1):
        name = f"chunk-{i:02d}.json"
        files[name] = write_new_json(out / name, chunk, snapshot)
    listing = {"schema": "linalg048-review-chunk-listing-v2",
               "packet_raw_sha256": PACKET_SHA, "chunk_count": len(chunks),
               "subject_count": len(packet["semantic_pairs"]),
               "source_record_count": sum(len(m["source_records"]) for m in packet["review_material"]),
               "files": files, "source_bindings": snapshot.bindings(),
               "accepted": False, "training_admitted": False}
    write_new_json(out / "listing.json", listing, snapshot)
    return listing


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--chunk-size", type=int, default=19)
    args = ap.parse_args(argv)
    try:
        result = publish_chunks(args.out, args.chunk_size)
        print("PENDING chunks:", result["chunk_count"], "subjects:", result["subject_count"])
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print("[FAIL]", exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
