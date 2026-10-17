"""diversity 证据只读准备:行 SHA 绑定表 + 结构模板 + 待审列表。

按 Codex FIX_REPORT 定序第 3 步:"Claude 可只读生成 diversity 结构模板、
全量实际 train ID 与原始行 SHA 的绑定表及待审列表。每条数学、变体、泄漏裁决
和 user_review 都必须来自实际审核;无审核保留待审,不能代签 APPROVED。"

行 SHA 口径(协议 §3):绑定原始 JSONL 行字节,**含原始行结束字节**。
本脚本不改任何现役文件,只写本目录新文件。
"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
MANIFEST = ROOT / "data" / "manifest.json"
POLICY = ROOT / "configs" / "training_diversity_policy.json"


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    policy = json.loads(POLICY.read_text(encoding="utf-8"))

    bindings = []
    for entry in manifest["entries"]:
        if entry["split"] != "train":
            continue
        p = (MANIFEST.parent / entry["path"]).resolve()
        data = p.read_bytes()
        # splitlines(keepends=True):保留原始行结束字节(CRLF/LF/无)
        for line_no, raw in enumerate(data.splitlines(keepends=True), 1):
            if not raw.strip():
                continue
            try:
                obj = json.loads(raw.decode("utf-8"))
            except Exception as exc:  # noqa: BLE001
                bindings.append({"sample_id": None, "source_path": str(entry["path"]),
                                 "line_no": line_no,
                                 "raw_line_sha256": sha_bytes(raw),
                                 "parse_error": exc.__class__.__name__})
                continue
            sid = obj.get("sample_id") or obj.get("id")
            bindings.append({"sample_id": sid, "source_path": str(entry["path"]),
                             "line_no": line_no, "raw_line_sha256": sha_bytes(raw),
                             "parse_error": None})

    # 绑定表:纯事实,不含任何审核字段
    (HERE / "row-bindings.jsonl").write_text(
        "\n".join(json.dumps(b, ensure_ascii=False) for b in bindings) + "\n",
        encoding="utf-8")

    # 待审列表:每个 train ID 一条,审核字段全部 null(待审),不代填
    pending = []
    for b in bindings:
        if b["sample_id"] is None:
            continue
        pending.append({
            "sample_id": b["sample_id"],
            "raw_line_sha256": b["raw_line_sha256"],
            "concept_id": None, "variant_kind": None,
            "user_review": None, "math_verdict": None,
            "diversity_verdict": None, "leakage_verdict": None,
            "state": "PENDING_REVIEW",
        })
    (HERE / "pending-review-list.jsonl").write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in pending) + "\n",
        encoding="utf-8")

    # 结构模板:只给形状;status 只标事实,审核字段留 null
    template = {
        "schema": 1,
        "status": "BINDINGS_COLLECTED_REVIEWS_PENDING",
        "manifest_sha256": sha_bytes(MANIFEST.read_bytes()),
        "policy_sha256": sha_bytes(POLICY.read_bytes()),
        "policy_concepts_total": len(policy.get("concepts", [])),
        "actual_train_ids_total": len(pending),
        "record_reviews": [
            {"sample_id": x["sample_id"], "raw_line_sha256": x["raw_line_sha256"],
             "concept_id": None, "variant_kind": None,
             "user_review": None, "math_review": None,
             "diversity_review": None, "leakage_review": None,
             "review_state": "PENDING"}
            for x in pending
        ],
        "note": "每条数学、变体、泄漏裁决与 user_review 必须来自实际审核;"
                "本模板不代签 APPROVED/VERIFIED,未审核项保持 PENDING。",
    }
    (HERE / "template.json").write_text(
        json.dumps(template, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"bindings={len(bindings)} pending={len(pending)} "
          f"policy_concepts={len(policy.get('concepts', []))}")
    print("ids:", [b["sample_id"] for b in bindings][:12], "...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
