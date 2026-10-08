"""Publish a new draft through the shared LF/no-BOM writer; does not select/admit."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
from draft_io import publish_jsonl


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = [json.loads(s) for s in args.source.read_text(encoding="utf-8-sig").splitlines()
            if s.strip()]
    result = publish_jsonl(args.output, rows)
    print(json.dumps({"path": args.output.as_posix(), **result}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
