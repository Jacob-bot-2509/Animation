"""batch-01 v3 生成器:在 v2 基础上吸收 Codex msg_448 三处修改
(c01-02 有限斜率切线措辞 / c36-01 实对称正定约定 / c52-05 分段目标与
分段逆 CDF 重写,避免与 test-prob-004 的 f=3x² 直接重合)。
三题整体取自 Codex 提案 draft-v3-review-proposal.jsonl,其余 12 题保留 v2。
"""
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
V2 = HERE / "draft-v2.jsonl"
PROP = Path("reviews/codex-supervision/2026-10-05-batch01-v2-mail-review/"
            "draft-v3-review-proposal.jsonl")
OUT = HERE / "draft-v3.jsonl"
ABSORB = {"draft-c01-02", "draft-c36-01", "draft-c52-05"}


def main() -> int:
    prop_path = PROP if PROP.is_file() else (
        HERE.parents[3] / PROP)
    v2 = [json.loads(l) for l in V2.read_text(encoding="utf-8").splitlines()
          if l.strip()]
    props = {}
    for l in prop_path.read_text(encoding="utf-8").splitlines():
        if l.strip():
            row = json.loads(l)
            props[row["id"]] = row
    rows = []
    for r in v2:
        if r["id"] in ABSORB:
            new = props[r["id"]]
            new["draft_status"] = "draft-v3-吸收Codex修订-待用户审阅"
            rows.append(new)
        else:
            r["draft_status"] = "draft-v3-待用户审阅"
            rows.append(r)
    OUT.write_text("\n".join(json.dumps(r, ensure_ascii=False,
                                         separators=(",", ":")) for r in rows)
                   + "\n", encoding="utf-8", newline="\n")
    print(f"写入 {len(rows)} 行 -> {OUT};吸收 {sorted(ABSORB)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
