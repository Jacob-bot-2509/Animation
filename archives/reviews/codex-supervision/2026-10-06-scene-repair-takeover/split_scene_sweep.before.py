"""Split the 264 selected draft records into self-contained scene-sweep
chunks (full problem/solution/answer/scene_spec per record) for the
scene-presentation-standard workflow agents."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from draft_io import selected_path, verify_entry  # noqa: E402

DRAFTS = ROOT / "reviews/2026-10-05-training-diversity-drafts"
OUT = ROOT / "reviews/2026-10-06-scene-standard-sweep/chunks"
NCHUNKS = 20

STANDARD = (
    "场景呈现标准(2026-10-06 用户审阅后新增,长期执行):"
    "①不能用集合/几何视角动画表示的题,必须给出清晰细致的运算动画;"
    "②矩阵运算不能只展现过程和结果,要标明哪一行乘哪一列;"
    "③证明收敛要标注重点和细节;"
    "④所有无法用几何视角表示的计算题必须列出详细运算方法和操作过程,"
    "学生看动画就能跟着算。")


def main() -> int:
    try:
        sel_path = DRAFTS / "draft-selection.json"
        sel_bytes = sel_path.read_bytes()
        sel = json.loads(sel_bytes.decode("utf-8-sig"))
        if sel.get("schema") != 2:
            raise ValueError("schema2 selector required")
        rows = []
        for entry in sel["entries"]:
            path = selected_path(DRAFTS, entry)
            verify_entry(path, entry, hash_algorithm=sel["hash_algorithm"])
            for line in path.read_text("utf-8-sig").splitlines():
                if line.strip():
                    rows.append(json.loads(line))
        if sel_path.read_bytes() != sel_bytes:
            raise ValueError("selection changed during load")
        if len(rows) != 264:
            raise ValueError("unexpected record count: " + str(len(rows)))
        if OUT.exists() and any(OUT.glob("*.json")):
            raise ValueError("chunks exist; use a fresh directory")
        OUT.mkdir(parents=True, exist_ok=True)
        per = (len(rows) + NCHUNKS - 1) // NCHUNKS
        for ci in range(NCHUNKS):
            slice_rows = rows[ci * per:(ci + 1) * per]
            records = []
            for i, r in enumerate(slice_rows):
                records.append({
                    "idx": ci * per + i,
                    "id": r["id"],
                    "concept_id": r.get("concept_id"),
                    "category": r.get("category"),
                    "sub_category": r.get("sub_category"),
                    "problem": r["problem"],
                    "solution": r["solution"],
                    "answer": r["answer"],
                    "scene_spec": r["scene_spec"],
                })
            (OUT / f"chunk-{ci + 1:02d}.json").write_text(
                json.dumps({"standard": STANDARD, "records": records},
                           ensure_ascii=False, indent=1) + "\n",
                encoding="utf-8", newline="\n")
        listing = {f.name: hashlib.sha256(f.read_bytes()).hexdigest()
                   for f in sorted(OUT.glob("*.json"))}
        (OUT / "listing.json").write_text(
            json.dumps({"selection_sha256": hashlib.sha256(sel_bytes).hexdigest(),
                        "chunks": listing, "records": len(rows)},
                       indent=2) + "\n", encoding="utf-8", newline="\n")
        print("chunks:", NCHUNKS, "| records:", len(rows))
        return 0
    except Exception as exc:
        print("[FAIL]", exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
