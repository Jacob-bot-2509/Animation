# -*- coding: utf-8 -*-
"""预留题池冻结:对 kaoyan-triples.jsonl 生成 SHA256 绑定清单。
清单只含 id/年份/节/题号/记录哈希(不含题面内容),可入版本库;
池数据本体留在 gitignored 目录,加锁冻结后不再修改。"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POOL = ROOT / "holdout-sources/extracted/kaoyan-triples.jsonl"
MANIFEST = ROOT / "holdout-sources/extracted/kaoyan-pool-v1-manifest.json"


def record_sha(rec):
    return hashlib.sha256(
        json.dumps(rec, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def main() -> int:
    raw = POOL.read_bytes()
    recs = [json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()]
    manifest = {
        "schema": "holdout-pool-manifest-v1",
        "pool_path": str(POOL.relative_to(ROOT)),
        "pool_raw_sha256": hashlib.sha256(raw).hexdigest(),
        "n_records": len(recs),
        "status": "FROZEN_UNEXPOSED",  # 任何人不得审阅/开发,仅作裁判
        "records": [
            {"id": r["id"], "year": r["year"], "section": r["section"],
             "number": r["number"], "record_sha256": record_sha(r)}
            for r in recs
        ],
    }
    if MANIFEST.exists():
        raise ValueError("manifest exists; pool is frozen, no re-freeze without new version")
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8", newline="\n")
    print("pool records:", len(recs))
    print("pool raw sha256:", manifest["pool_raw_sha256"])
    print("manifest:", MANIFEST)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
