"""数学核心/任务结构签名:版本绑定(goal/domain/key_conditions/decisive_steps)与跨集匹配."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CORE = ROOT / "reviews/codex-supervision/2026-10-07-continuous-math-review/current-core"
SIG_DIR = ROOT / "reviews/2026-10-07-semantic-core-lists"
NAME_RE = re.compile(r"[a-z][a-z0-9-]{0,79}")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_record_bindings() -> list[dict]:
    rows = [json.loads(line) for line in
            (CORE / "record-bindings.jsonl").read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    if len(rows) != 761 or len({r["id"] for r in rows}) != 761:
        raise ValueError("record bindings incomplete")
    return rows


def load_record(by_id: dict, rid: str) -> dict:
    b = by_id[rid]
    lines = (ROOT / b["path"]).read_bytes().splitlines(keepends=True)
    rec = json.loads(lines[b["source_line"] - 1].decode("utf-8-sig"))
    if digest(json.dumps(rec, ensure_ascii=False, sort_keys=True,
                         separators=(",", ":")).encode("utf-8")) != b["record_sha256"]:
        raise ValueError("record version changed: " + rid)
    return rec


def validate_signature(sig: dict, by_id: dict) -> None:
    rid = sig["id"]
    b = by_id[rid]
    for field in ("goal", "domain", "key_conditions", "decisive_steps"):
        if not isinstance(sig.get(field), (str, list)) or not sig[field]:
            raise ValueError(f"signature field empty: {rid}.{field}")
    if sig.get("group") != b["group"]:
        raise ValueError("group mismatch: " + rid)
    for f in ("record_sha256", "math_sha256"):
        if sig.get(f) != b[f]:
            raise ValueError(f"{f} binding mismatch: " + rid)


def bundle(group_name: str) -> int:
    if not NAME_RE.fullmatch(group_name):
        raise ValueError("invalid group name")
    sig_path = SIG_DIR / f"{group_name}-signatures.jsonl"
    sigs = [json.loads(line) for line in sig_path.read_text(encoding="utf-8-sig").splitlines()
            if line.strip()]
    by_id = {r["id"]: r for r in load_record_bindings()}
    for sig in sigs:
        validate_signature(sig, by_id)
    if len({s["id"] for s in sigs}) != len(sigs):
        raise ValueError("duplicate signature id")
    out_dir = SIG_DIR / group_name
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "signatures.jsonl").write_text(
        "".join(json.dumps(s, ensure_ascii=False) + "\n" for s in sigs),
        encoding="utf-8", newline="\n")
    receipt = {"schema": "semantic-core-signatures-v1", "group": group_name,
               "total": len(sigs),
               "groups": {g: sum(1 for s in sigs if s["group"] == g)
                          for g in sorted({s["group"] for s in sigs})},
               "note": "签名绑定 record_sha256/math_sha256;语义内容由作者逐条撰写,"
                       "同核心判定靠 cross-match 而非本文件"}
    with (out_dir / "receipt.json").open("w", encoding="utf-8", newline="\n") as f:
        json.dump(receipt, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(json.dumps(receipt, ensure_ascii=False))
    return 0


def cross_match() -> int:
    """跨集同核心候选:goal 相等且 decisive_steps 集合相等(去参数后的语义签名)."""
    sigs = []
    for p in sorted(SIG_DIR.glob("*-signatures.jsonl")):
        sigs.extend(json.loads(line) for line in p.read_text(encoding="utf-8-sig").splitlines()
                    if line.strip())
    train_side = [s for s in sigs if s["group"] in ("train", "selected_draft")]
    eval_side = [s for s in sigs if s["group"] in ("eval", "test")]
    key = lambda s: (s["goal"], tuple(sorted(s["decisive_steps"])))  # noqa: E731
    by = defaultdict(list)
    for s in eval_side:
        by[key(s)].append(s)
    candidates = []
    for t in train_side:
        for e in by.get(key(t), []):
            candidates.append({"train_id": t["id"], "eval_id": e["id"],
                               "eval_group": e["group"],
                               "train_goal": t["goal"], "eval_goal": e["goal"],
                               "train_steps": t["decisive_steps"], "eval_steps": e["decisive_steps"],
                               "train_domain": t["domain"], "eval_domain": e["domain"],
                               "disposition": "UNREVIEWED"})
    out = SIG_DIR / "cross-candidates.json"
    out.write_text(json.dumps({"schema": "semantic-cross-candidates-v1",
                               "train_side": len(train_side), "eval_side": len(eval_side),
                               "candidates": candidates},
                              ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"训练侧 {len(train_side)} 签名,评测侧 {len(eval_side)} 签名")
    print(f"跨集同核心候选: {len(candidates)} 对 -> {out.relative_to(ROOT)}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("action", choices=["bundle", "cross-match"])
    ap.add_argument("--group")
    args = ap.parse_args(argv)
    if args.action == "bundle":
        if not args.group:
            raise ValueError("bundle requires --group")
        return bundle(args.group)
    return cross_match()


if __name__ == "__main__":
    raise SystemExit(main())
