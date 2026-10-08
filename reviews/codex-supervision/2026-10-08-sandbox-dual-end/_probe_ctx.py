"""Read-only probe: dump every context window around a term in a DSH session transcript."""
import sys, json, re
from pathlib import Path
from compression import zstd

path = Path(sys.argv[1])
term = sys.argv[2]
width = int(sys.argv[3]) if len(sys.argv) > 3 else 500
with zstd.open(path, "rb") as fh:
    text = fh.read().decode("utf-8", "replace")
idxs = [m.start() for m in re.finditer(re.escape(term), text)]
print(f"# {path.name} term={term!r} hits={len(idxs)} plaintext={len(text)}")
for i, ix in enumerate(idxs, 1):
    lo, hi = max(0, ix - width), min(len(text), ix + width)
    print(f"\n===== hit {i}/{len(idxs)} @{ix} =====")
    print(text[lo:hi])
