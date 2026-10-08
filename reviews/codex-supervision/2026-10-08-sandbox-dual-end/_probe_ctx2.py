"""Read-only extractor: find user-turn and assistant text blocks that mention a term.

Prints the human-facing text (stripping harness boilerplate) rather than raw JSON,
and de-duplicates repeated prompt echoes so the output stays readable.
"""
import sys, json, re
from pathlib import Path
from compression import zstd

path = Path(sys.argv[1])
term = sys.argv[2]
with zstd.open(path, "rb") as fh:
    lines = fh.read().decode("utf-8", "replace").splitlines()

seen = set()
out = []
for ln in lines:
    if term not in ln:
        continue
    try:
        rec = json.loads(ln)
    except Exception:
        continue
    data = rec.get("data") or {}
    msg = data.get("message") or {}
    if not isinstance(msg, dict):
        continue
    role = msg.get("role")
    if role not in ("user", "assistant"):
        continue
    texts = []
    for blk in msg.get("content") or []:
        if isinstance(blk, dict) and blk.get("type") == "text" and blk.get("text"):
            texts.append(blk["text"])
    for t in texts:
        if term not in t:
            continue
        key = t[:200]
        if key in seen:
            continue
        seen.add(key)
        out.append((rec.get("seq"), role, t))

print(f"# {path.name} term={term!r} distinct-text-blocks={len(out)}")
for seq, role, t in out:
    print(f"\n########## seq={seq} role={role} len={len(t)} ##########")
    print(t[:1500])
