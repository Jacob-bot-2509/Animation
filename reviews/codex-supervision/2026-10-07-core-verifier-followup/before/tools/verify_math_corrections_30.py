"""独立重推导 Codex 30 题修订:现役源绑定→修订前SHA→构造修订版→对照其交付."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SUP = ROOT / "reviews/codex-supervision/2026-10-07-core-submission-supervision"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def dense(record: dict) -> str:
    return digest(json.dumps(record, ensure_ascii=False, sort_keys=True,
                             separators=(",", ":")).encode("utf-8"))


def main() -> int:
    mc = [json.loads(l) for l in (SUP / "math-corrections-30.jsonl")
          .read_text(encoding="utf-8-sig").splitlines() if l.strip()]
    print(f"修订条数={len(mc)}")
    from collections import Counter
    print("分布:", dict(Counter(m["source"]["group"] for m in mc)))

    # 1) 现役源文件 SHA 与修订包绑定一致
    print("\n== 1. 现役源文件与 before 绑定 ==")
    srcs = {}
    for m in mc:
        s = m["source"]
        srcs.setdefault(s["source_path"], s["source_raw_sha256"])
    for path, sha in sorted(srcs.items()):
        b = (ROOT / path).read_bytes()
        print(f"{'MATCH' if digest(b) == sha else 'MISMATCH'}  {path}  {len(b)}B")

    # 2) 逐条:现役记录 == 修订前;构造修订版 == corrected_record == 修订后SHA
    print("\n== 2. 逐条重推导 ==")
    bad = 0
    for m in mc:
        s = m["source"]
        lines = (ROOT / s["source_path"]).read_bytes().splitlines(keepends=True)
        before = json.loads(lines[s["source_line"] - 1].decode("utf-8-sig"))
        if dense(before) != m["before_record_dense_sha256"]:
            print(f"  BEFORE-MISMATCH {m['id']}")
            bad += 1
            continue
        if before.get("id") != m["id"]:
            print(f"  ID-MISMATCH {m['id']} -> {before.get('id')}")
            bad += 1
            continue
        # 构造:复制原记录,仅替换 changed_fields 为 after_math_fields 对应值
        rebuilt = dict(before)
        for f in m["changed_fields"]:
            if f not in m["after_math_fields"]:
                print(f"  FIELD-MISSING {m['id']}.{f}")
                bad += 1
                continue
            rebuilt[f] = m["after_math_fields"][f]
        # 其他字段必须原样
        for k, v in before.items():
            if k not in m["changed_fields"] and k in ("problem", "solution", "answer"):
                if rebuilt[k] != v:
                    print(f"  EXTRA-CHANGE {m['id']}.{k}")
                    bad += 1
        if dense(rebuilt) != m["after_record_dense_sha256"]:
            print(f"  AFTER-MISMATCH {m['id']} rebuilt={dense(rebuilt)[:12]} want={m['after_record_dense_sha256'][:12]}")
            bad += 1
            continue
        if m.get("corrected_record"):
            cr = m["corrected_record"]
            if dense(cr) != m["after_record_dense_sha256"]:
                print(f"  CORRECTED-RECORD-SHA-MISMATCH {m['id']}")
                bad += 1
            if cr != rebuilt:
                diff = [k for k in set(cr) | set(rebuilt) if cr.get(k) != rebuilt.get(k)]
                print(f"  CORRECTED-RECORD-DIFF {m['id']}: {diff}")
                bad += 1
    print(f"逐条重推导: {'全部通过' if bad == 0 else f'{bad} 条异常'}")

    # 3) corrected-sources 候选版:变更行=修订后记录,其余行逐字节保留
    print("\n== 3. corrected-sources 候选版逐行核对 ==")
    b2 = json.loads((SUP / "candidate-source-bindings.json").read_text(encoding="utf-8-sig"))
    bad2 = 0
    for binding in b2:
        bp = ROOT / binding["before"]["path"]
        cp = ROOT / binding["candidate"]["path"]
        before_bytes = bp.read_bytes()
        cand_bytes = cp.read_bytes()
        if digest(before_bytes) != binding["before"]["raw_sha256"]:
            print(f"  BEFORE-SHA-MISMATCH {binding['before']['path']}")
            bad2 += 1
        if digest(cand_bytes) != binding["candidate"]["raw_sha256"] or len(cand_bytes) != binding["candidate"]["bytes"]:
            print(f"  CANDIDATE-SHA-MISMATCH {binding['candidate']['path']}")
            bad2 += 1
            continue
        bl = before_bytes.splitlines(keepends=True)
        cl = cand_bytes.splitlines(keepends=True)
        if len(bl) != len(cl):
            print(f"  LINE-COUNT-DIFF {binding['before']['path']}: {len(bl)} vs {len(cl)}")
            bad2 += 1
            continue
        changed = set(binding["changed_source_lines"])
        for i, (a, b) in enumerate(zip(bl, cl), start=1):
            if i in changed:
                rec = json.loads(b.decode("utf-8-sig"))
                # 该行应是某条的修订后记录
                exp = [m for m in mc if m["source"]["source_path"] == binding["before"]["path"]
                       and m["source"]["source_line"] == i]
                if not exp or dense(rec) != exp[0]["after_record_dense_sha256"]:
                    print(f"  CHANGED-LINE-MISMATCH {binding['before']['path']}:{i}")
                    bad2 += 1
            elif a != b:
                print(f"  UNCHANGED-LINE-DRIFT {binding['before']['path']}:{i}")
                bad2 += 1
    print(f"候选版逐行核对: {'全部通过' if bad2 == 0 else f'{bad2} 处异常'}")
    return 0 if bad == 0 and bad2 == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
