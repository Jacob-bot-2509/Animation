"""Read-only helper: print file contents by absolute path (bypasses shell quoting limits)."""
import sys
from pathlib import Path

path = Path(sys.argv[1])
offset = int(sys.argv[2]) if len(sys.argv) > 2 else 0
limit = int(sys.argv[3]) if len(sys.argv) > 3 else 200
lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
chunk = lines[offset:offset + limit]
for i, line in enumerate(chunk, start=offset + 1):
    print(f"{i}\t{line}")
print(f"--- total lines: {len(lines)} ---")
