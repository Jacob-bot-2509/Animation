"""Portable draft hashes and exclusive UTF-8/LF publication; no admission rules."""
from __future__ import annotations
import hashlib
import json
import re
from pathlib import Path
from typing import Iterable

NORMALIZED_HASH = "sha256-utf8-sig-splitlines-lf-v1"
RAW_HASH = "sha256-raw-bytes-v1"
_SHA = re.compile(r"[0-9a-f]{64}\Z")


def normalized_bytes(data: bytes) -> bytes:
    """Exact v1 contract: UTF-8-sig decode, splitlines, LF join, UTF-8 encode.

    Only the leading BOM and splitlines-recognized line separators are folded.
    One terminal line separator is omitted; internal/trailing empty lines and
    other whitespace remain significant. No JSON sorting or number conversion.
    Invalid UTF-8 is rejected, never replaced.
    """
    return "\n".join(data.decode("utf-8-sig").splitlines()).encode("utf-8")


def fingerprint(data: bytes) -> dict:
    return {"sha256": hashlib.sha256(normalized_bytes(data)).hexdigest(),
            "raw_sha256": hashlib.sha256(data).hexdigest(),
            "hash_algorithm": NORMALIZED_HASH}


def selected_path(drafts: Path, entry: dict) -> Path:
    batch, rel = entry.get("batch"), entry.get("path")
    if not isinstance(batch, str) or not re.fullmatch(r"batch-\d{2}", batch):
        raise ValueError("invalid draft batch")
    if not isinstance(rel, str) or not rel or Path(rel).is_absolute():
        raise ValueError(f"invalid selected path: {batch}")
    root = drafts.resolve()
    path = (root / rel).resolve()
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"selected path outside draft root: {batch}") from exc
    if path.parent != (root / batch).resolve() or path.suffix != ".jsonl":
        raise ValueError(f"invalid selected path: {batch}")
    return path


def verify_entry(path: Path, entry: dict, hash_algorithm: str | None = None) -> dict:
    algorithm = entry.get("hash_algorithm", hash_algorithm or RAW_HASH)
    if hash_algorithm is not None and algorithm != hash_algorithm:
        raise ValueError("entry/manifest hash algorithm conflict")
    if algorithm not in (NORMALIZED_HASH, RAW_HASH):
        raise ValueError(f"unsupported draft hash algorithm: {algorithm}")
    expected = entry.get("sha256")
    if not isinstance(expected, str) or not _SHA.fullmatch(expected):
        raise ValueError("missing or malformed selected SHA-256")
    data = path.read_bytes()
    raw = hashlib.sha256(data).hexdigest()
    if algorithm == NORMALIZED_HASH:
        expected_raw = entry.get("raw_sha256")
        if not isinstance(expected_raw, str) or not _SHA.fullmatch(expected_raw):
            raise ValueError("normalized draft entry requires archival raw_sha256")
        actual = fingerprint(data)["sha256"]
    else:
        actual = raw
    if actual != expected:
        raise ValueError(f"selected version hash mismatch: {entry.get('batch')} ({algorithm})")
    return {"sha256": actual, "raw_sha256": raw, "hash_algorithm": algorithm,
            "raw_bytes_match_manifest": raw == entry.get("raw_sha256", expected)}


def write_utf8_lf(path: Path, text: str, *, exclusive: bool = False) -> None:
    """Write without platform newline translation; reject BOM, normalize CR/LF."""
    if text.startswith("\ufeff"):
        raise ValueError("publisher text must not start with a BOM")
    data = text.replace("\r\n", "\n").replace("\r", "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb" if exclusive else "wb") as stream:
        stream.write(data)


def publish_jsonl(path: Path, records: Iterable[dict]) -> dict:
    """Publish a NEW version only. Existing versions can never be overwritten."""
    rows = list(records)
    ids = [r.get("id") if isinstance(r, dict) else None for r in rows]
    if not rows or any(not isinstance(i, str) or not i for i in ids) or len(set(ids)) != len(ids):
        raise ValueError("draft records require nonempty unique string IDs")
    text = "\n".join(json.dumps(r, ensure_ascii=False, separators=(",", ":"),
                              allow_nan=False) for r in rows) + "\n"
    write_utf8_lf(path, text, exclusive=True)
    return {**fingerprint(path.read_bytes()), "count": len(rows)}


def require_legacy_selection(path: Path) -> None:
    """Retired repair scripts must not downgrade a migrated selector or evidence."""
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if data.get("schema", 1) >= 2 or data.get("hash_algorithm") not in (None, RAW_HASH):
        raise ValueError("Retired raw-hash repair tool: publish a new version with draft_io; "
                         "do not rewrite signed history or the normalized selector")
