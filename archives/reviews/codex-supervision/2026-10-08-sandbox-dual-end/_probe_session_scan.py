"""Read-only probe: decompress DSH session transcript and search for dual-end experiment terms."""
import sys, json, re
from pathlib import Path

try:
    from compression.zstd import ZstdDecompressor  # py3.14+
    have = "compression.zstd"
except Exception:
    try:
        import zstandard
        have = "zstandard"
    except Exception as exc:
        print(json.dumps({"ok": False, "error": f"no zstd: {exc}"}, ensure_ascii=False))
        sys.exit(0)

TARGETS = sys.argv[1:]
KEYS = ["\u53cc\u7aef", "DSH", "dsh", "Render \u4fa7", "\u6c99\u7bb1\u53cc\u7aef"]
out = {"zstd_backend": have, "files": {}}
for t in TARGETS:
    p = Path(t)
    rec = {"exists": p.exists()}
    if p.exists():
        raw = p.read_bytes()
        rec["compressed_bytes"] = len(raw)
        try:
            if have == "compression.zstd":
                with __import__("compression.zstd", fromlist=["open"]).open(p, "rb") as fh:
                    data = fh.read()
            else:
                data = zstandard.ZstdDecompressor().stream_reader(__import__("io").BytesIO(raw)).read()
            text = data.decode("utf-8", "replace")
            rec["plaintext_bytes"] = len(data)
            rec["hits"] = {}
            for k in KEYS:
                idxs = [m.start() for m in re.finditer(re.escape(k), text)]
                rec["hits"][k] = len(idxs)
                if idxs:
                    lo = max(0, idxs[0] - 400)
                    hi = min(len(text), idxs[0] + 400)
                    rec["first_context_" + k] = text[lo:hi]
        except Exception as exc:
            rec["error"] = repr(exc)
    out["files"][str(p)] = rec
print(json.dumps(out, ensure_ascii=False, indent=2))
