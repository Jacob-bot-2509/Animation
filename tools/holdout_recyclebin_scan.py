"""Read current Windows $I metadata; this is not proof of historical non-deletion.

Format references:
https://github.com/libyal/dtformats/blob/main/documentation/Windows%20Recycle.Bin%20file%20formats.asciidoc
https://github.com/danielmarschall/recyclebinunit/blob/master/FORMAT.md
No $R payloads are opened, restored, or removed. Importing performs no scan.
"""
import argparse
import hashlib
import json
import os
import stat
import struct
from datetime import datetime, timedelta, timezone
from pathlib import Path, PureWindowsPath

MAX_METADATA_BYTES = 1 << 20
FILETIME_EPOCH = datetime(1601, 1, 1, tzinfo=timezone.utc)


def filetime_utc(ticks):
    seconds, remainder = divmod(ticks, 10_000_000)
    try:
        value = FILETIME_EPOCH + timedelta(seconds=seconds)
    except OverflowError as exc:
        raise ValueError("FILETIME outside supported calendar range") from exc
    return value.strftime("%Y-%m-%dT%H:%M:%S") + f".{remainder:07d}Z"


def parse_i_metadata(raw):
    if len(raw) < 24:
        raise ValueError("truncated 24-byte header")
    if len(raw) > MAX_METADATA_BYTES:
        raise ValueError("metadata exceeds size limit")
    version, original_size, ticks = struct.unpack_from("<QQQ", raw)
    if version == 1:
        if len(raw) != 544:
            raise ValueError("version 1 requires a 520-byte filename field")
        field = raw[24:]
        count = None
    elif version == 2:
        if len(raw) < 28:
            raise ValueError("truncated version 2 filename length")
        count = struct.unpack_from("<I", raw, 24)[0]
        if count < 2 or len(raw) != 28 + 2 * count:
            raise ValueError("version 2 UTF-16 code-unit count does not match bytes")
        field = raw[28:]
    else:
        raise ValueError(f"unsupported metadata version {version}")
    try:
        text = field.decode("utf-16-le", errors="strict")
    except UnicodeDecodeError as exc:
        raise ValueError("invalid UTF-16LE filename") from exc
    path, separator, padding = text.partition("\x00")
    if not separator or not path or any(c != "\x00" for c in padding):
        raise ValueError("missing terminator, empty path, or nonzero trailing data")
    if version == 2 and padding:
        raise ValueError("version 2 filename has an embedded terminator")
    if not PureWindowsPath(path).is_absolute():
        raise ValueError("original filename must be an absolute Windows path")
    return {
        "format_version": version, "original_size_bytes": original_size,
        "deleted_filetime_100ns": ticks, "deleted_at_utc": filetime_utc(ticks),
        "original_path": path, "declared_utf16_code_units": count,
    }


def path_relation(original, target):
    # Lexical Windows comparisons: no access to the original/deleted path.
    left, right = PureWindowsPath(original), PureWindowsPath(target)
    if left == right:
        return "EXACT_PATH"
    if left in right.parents:
        return "DELETED_ANCESTOR_CONTAINS_TARGET"
    if right in left.parents:
        return "DELETED_PATH_WITHIN_TARGET_SCOPE"
    return None


def is_reparse(info):
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0)
        & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    )


def scan_current_metadata(root, targets=()):
    root = Path(root)
    targets = [str(PureWindowsPath(t)) for t in targets]
    if any(not PureWindowsPath(t).is_absolute() for t in targets):
        raise ValueError("target paths must be absolute Windows paths")
    report = {
        "schema": "recycle-bin-current-metadata-v2",
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "root": str(root), "targets": targets, "sid_directories_scanned": [],
        "metadata_files_seen": 0, "records": [], "errors": [],
        "historical_non_deletion_proved": False,
        "delete_actor": "UNKNOWN",
        "scope": "Current readable $I metadata only; no historical completeness claim",
    }

    def error(path, exc):
        report["errors"].append({"path": str(path), "reason": str(exc),
                                 "exception_type": type(exc).__name__})

    def children(path):
        try:
            with os.scandir(path) as iterator:
                return sorted(list(iterator), key=lambda x: x.name.casefold())
        except OSError as exc:
            error(path, exc)
            return []

    try:
        info = root.lstat()
        if is_reparse(info) or not stat.S_ISDIR(info.st_mode):
            raise ValueError("root must be a directory without a reparse point")
    except (OSError, ValueError) as exc:
        error(root, exc)
    else:
        for sid in children(root):
            if not sid.name.upper().startswith("S-"):
                continue
            try:
                info = sid.stat(follow_symlinks=False)
                if is_reparse(info) or not stat.S_ISDIR(info.st_mode):
                    raise ValueError("SID entry is not an ordinary directory")
            except (OSError, ValueError) as exc:
                error(sid.path, exc)
                continue
            report["sid_directories_scanned"].append(sid.path)
            for item in children(sid.path):
                if not item.name.upper().startswith("$I"):
                    continue
                report["metadata_files_seen"] += 1
                try:
                    before = os.stat(item.path, follow_symlinks=False)
                    if is_reparse(before) or not stat.S_ISREG(before.st_mode):
                        raise ValueError("$I entry is not an ordinary file")
                    if before.st_size > MAX_METADATA_BYTES:
                        raise ValueError("$I entry exceeds size limit")
                    with open(item.path, "rb") as stream:
                        raw = stream.read(MAX_METADATA_BYTES + 1)
                    after = os.stat(item.path, follow_symlinks=False)
                    if (before.st_size, before.st_mtime_ns, before.st_ino) != (
                            after.st_size, after.st_mtime_ns, after.st_ino):
                        raise ValueError("$I metadata changed during capture")
                    record = parse_i_metadata(raw)
                    record.update({"metadata_path": item.path,
                                   "metadata_raw_sha256": hashlib.sha256(raw).hexdigest(),
                                   "metadata_size_bytes": len(raw),
                                   "target_matches": []})
                    for target in targets:
                        relation = path_relation(record["original_path"], target)
                        if relation:
                            record["target_matches"].append({"target": target,
                                                             "relation": relation})
                    report["records"].append(record)
                except (OSError, ValueError) as exc:
                    error(item.path, exc)
    report["parsed_records"] = len(report["records"])
    report["matched_records"] = sum(bool(r["target_matches"]) for r in report["records"])
    report["status"] = "SNAPSHOT_INCOMPLETE" if report["errors"] else "SNAPSHOT_COMPLETE"
    report["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("D:/$Recycle.Bin"))
    parser.add_argument("--target", action="append", default=[],
                        help="Absolute original path or scope; repeat as needed")
    args = parser.parse_args(argv)
    try:
        report = scan_current_metadata(args.root, args.target)
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 2 if report["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
