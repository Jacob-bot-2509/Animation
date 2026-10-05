"""枚举记录序列化变体,定位 Codex expected_record_sha256 的计算口径。"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCHES = ROOT / "reviews/codex-supervision/2026-10-05-draft-hash-compatibility/ready-row-separator-patches.json"
V4 = ROOT / "reviews/2026-10-05-training-diversity-drafts/batch-02/draft-codex-repair-v4-final.jsonl"


def main() -> int:
    patches = json.loads(PATCHES.read_text(encoding="utf-8-sig"))
    p = next(x for x in patches["records"]
             if x["id"] == "draft-c33-02")
    rows = [json.loads(l) for l in V4.read_text(encoding="utf-8-sig").splitlines()
            if l.strip()]
    r = next(x for x in rows if x["id"] == "draft-c33-02")
    for k, v in p["fields"].items():
        r[k] = v
    expect = p["expected_record_sha256"]
    variants = []
    for ensure in (False, True):
        for sort in (False, True):
            for sep in ((",", ":"), (", ", ": "), None):
                kw = {"ensure_ascii": ensure, "sort_keys": sort}
                if sep is not None:
                    kw["separators"] = sep
                s = json.dumps(r, **kw)
                variants.append((ensure, sort, sep, s))
    for ensure, sort, sep, s in variants:
        h_norm = hashlib.sha256(
            "\n".join(s.splitlines()).encode("utf-8")).hexdigest()
        h_raw = hashlib.sha256(s.encode("utf-8")).hexdigest()
        for tag, h in (("norm", h_norm), ("raw", h_raw)):
            if h == expect:
                print(f"命中: ensure={ensure} sort={sort} sep={sep} {tag}")
                return 0
    print("无一命中,前 3 个变体哈希:")
    for ensure, sort, sep, s in variants[:3]:
        print(" ", ensure, sort, sep,
              hashlib.sha256("\n".join(s.splitlines()).encode("utf-8")).hexdigest()[:16])
    return 1


if __name__ == "__main__":
    sys.exit(main())
