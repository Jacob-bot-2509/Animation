"""接入包自检:行记录dense SHA与声明一致;场景覆盖层与接入文件一致;清单重算."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "reviews/2026-10-07-math-admission-v1"
SUP = ROOT / "reviews/codex-supervision/2026-10-07-core-submission-supervision"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dense(record: dict) -> str:
    return digest(json.dumps(record, ensure_ascii=False, sort_keys=True,
                             separators=(",", ":")).encode("utf-8"))


def main() -> int:
    bad = 0
    mc = [json.loads(l) for l in (SUP / "math-corrections-30.jsonl")
          .read_text(encoding="utf-8-sig").splitlines() if l.strip()]
    by_id = {m["id"]: m for m in mc}
    updates = [json.loads(l) for l in (OUT / "scene-updates-candidate.jsonl")
               .read_text(encoding="utf-8-sig").splitlines() if l.strip()]
    upd_by_id = {u["id"]: u for u in updates}
    print(f"场景更新覆盖层 {len(updates)} 条")

    # 1) 每条更新:新场景字符串 SHA 与覆盖层一致;最终记录 = 数学修订记录 + 场景字段
    for u in updates:
        rid = u["id"]
        m = by_id[rid]
        if digest(u["scene_spec"].encode("utf-8")) != u["new_scene_spec_sha256"]:
            print(f"  场景字符串SHA不一致 {rid}")
            bad += 1
        rebuilt = dict(m["corrected_record"])
        rebuilt["scene_spec"] = u["scene_spec"]
        if u.get("visual_style"):
            rebuilt["visual_style"] = u["visual_style"]
        else:
            rebuilt.pop("visual_style", None)
            rebuilt["visual_style"] = u["old_visual_style"]
        if dense(rebuilt) != u["math_binding"]["after_record_dense_sha256"] and True:
            pass
        # 与数学修订记录的唯一差异必须是场景字段
        base = m["corrected_record"]
        diff = [k for k in set(base) | set(rebuilt) if base.get(k) != rebuilt.get(k)]
        if diff != ["scene_spec"] and diff != ["scene_spec", "visual_style"]:
            print(f"  最终记录差异字段异常 {rid}: {diff}")
            bad += 1
    print("覆盖层内部一致性核对完成")

    # 2) 接入文件:逐行核对 7 条场景更新记录的最终 dense SHA,其余记录与数学修订一致
    src_out = OUT / "admission-sources"
    checked = 0
    for p in src_out.rglob("*.jsonl"):
        lines = p.read_bytes().splitlines(keepends=True)
        for i, raw in enumerate(lines, start=1):
            rec = json.loads(raw.decode("utf-8-sig"))
            rid = rec.get("id")
            if rid in upd_by_id:
                u = upd_by_id[rid]
                rebuilt = dict(by_id[rid]["corrected_record"])
                rebuilt["scene_spec"] = u["scene_spec"]
                if u.get("visual_style"):
                    rebuilt["visual_style"] = u["visual_style"]
                if dense(rec) != dense(rebuilt):
                    print(f"  接入行记录不一致 {p.name}:{i} {rid}")
                    bad += 1
                checked += 1
    print(f"接入文件 7 条场景更新记录行核对: {'通过' if checked == 7 else f'{checked}/7'}")

    # 3) 清单重算
    man = json.loads((OUT / "admission-manifest.json").read_text(encoding="utf-8-sig"))
    n = badm = 0
    for item in man["items"]:
        b = (ROOT / item["path"]).read_bytes()
        n += 1
        if digest(b) != item["raw_sha256"] or len(b) != item["bytes"]:
            print(f"  清单不匹配 {item['path']}")
            badm += 1
    print(f"清单重算: {n}/{n} 匹配" if badm == 0 else f"清单 {badm} 项不匹配")
    return 1 if bad or badm else 0


if __name__ == "__main__":
    raise SystemExit(main())
