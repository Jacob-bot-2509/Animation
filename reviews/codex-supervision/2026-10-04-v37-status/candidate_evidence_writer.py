# Review-only reference. Not installed in live Claude code.
def _write_evidence_record(results: dict, path: Path) -> None:
    """Serialize each explicit candidate path once; each commit is atomic."""
    candidates = (path, SUPPORT / ("fallback-" + path.name))
    for candidate in candidates:
        record = dict(results, evidence_written=str(candidate), stdout_only=False)
        temporary = candidate.with_suffix(candidate.suffix + ".tmp")
        try:
            serialized = json.dumps(record, ensure_ascii=False, indent=2)
            temporary.write_text(serialized, encoding="utf-8")
            temporary.replace(candidate)
        except (OSError, TypeError, ValueError) as error:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass
            print("Evidence candidate failed: " + repr(error), file=sys.stderr,
                  flush=True)
            continue
        results["evidence_written"] = str(candidate)
        results["stdout_only"] = False
        return
    results["evidence_written"] = None
    results["stdout_only"] = True
