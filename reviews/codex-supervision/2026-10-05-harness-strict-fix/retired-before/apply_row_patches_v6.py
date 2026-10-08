"""发布 v6(Codex msg_505/506 严格校验版):
- 补丁应用前严格校验原记录 SHA == expected_record_sha256
  (sha256(sorted-dump-json of original record)),失败直接拒绝;
- 应用后校验新数学 SHA == new_math_content_sha256
  (sha256(sorted-dump-json of {problem,solution,answer,scene_spec})),失败拒绝;
- 修正 4 批 12 个别名字段(root_path/root_report_path/source_path 统一根相对);
- 绑定 v6 血缘并发布 draft-codex-repair-v6.jsonl(不原地改已发布 v5);
- 生成 v6 逐题 MD;选择器切 v6 并记录双哈希。
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from draft_io import (fingerprint, publish_jsonl, verify_entry,  # noqa: E402
                      write_utf8_lf, NORMALIZED_HASH)

DRAFTS = ROOT / "reviews/2026-10-05-training-diversity-drafts"
PATCHES = ROOT / "reviews/codex-supervision/2026-10-05-draft-hash-compatibility/ready-row-separator-patches.json"
SEL = DRAFTS / "draft-selection.json"
V6 = "codex-repair-v6"
MATH_FIELDS = ("problem", "solution", "answer", "scene_spec")


def sorted_dump_sha(obj) -> str:
    return hashlib.sha256(json.dumps(
        obj, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def md_for_batch(batch: str, rows: list[dict], prev_norm_sha: str) -> str:
    parts = [f"# {batch} 精确数学修订文档", "",
             f"版本：{V6}。{len(rows)}题；原编号、题数和顺序全部保留，删除0题。"
             "题目、推导、答案及场景文本已复验。未正式准入，动画尚未渲染验收。", "",
             f"前身v5 SHA-256：`{prev_norm_sha}`。", ""]
    for r in rows:
        parts += [f"## {r['id']} · {r.get('concept_id', '')}", "",
                  "**题目**", "", r["problem"], "",
                  "**推导**", "", r["solution"], "",
                  "**答案**", "", r["answer"], "",
                  "**场景对象**", ""]
        parts += ["- " + o for o in r["scene_spec"]["objects"]]
        parts += ["", "**场景步骤**", ""]
        parts += ["- " + s for s in r["scene_spec"]["steps"]]
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def main() -> int:
    patches = json.loads(PATCHES.read_text(encoding="utf-8-sig"))
    sel = json.loads(SEL.read_text(encoding="utf-8-sig"))
    if sel.get("schema", 1) < 2:
        print("选择器非 schema2,拒绝")
        return 1
    by_batch: dict[str, list[dict]] = {}
    for p in patches["records"]:
        by_batch.setdefault(p["batch"], []).append(p)

    receipts = {}
    for batch, plist in sorted(by_batch.items()):
        entry = next(e for e in sel["entries"] if e["batch"] == batch)
        v5 = DRAFTS / entry["path"]
        verify_entry(v5, entry, hash_algorithm=NORMALIZED_HASH)
        v5_fp = fingerprint(v5.read_bytes())
        v5_rows = {r["id"]: r for r in (
            json.loads(l) for l in v5.read_text(
                encoding="utf-8-sig").splitlines() if l.strip())}
        # 原记录取自 v4 原件(source),预校验在其上执行
        v4 = DRAFTS / entry["source_path"] if Path(
            entry["source_path"]).is_absolute() else DRAFTS / entry["source_path"]
        if not v4.is_file():
            v4 = DRAFTS / batch / "draft-codex-repair-v4-final.jsonl"
        v4_fp = fingerprint(v4.read_bytes())
        if v4_fp["sha256"] != entry.get("source_sha256"):
            print(f"[REJECT] {batch} source(v4)指纹与选择器不符")
            return 1
        rows = [json.loads(l) for l in v5.read_text(
            encoding="utf-8-sig").splitlines() if l.strip()]
        v4_rows = {r["id"]: r for r in (
            json.loads(l) for l in v4.read_text(
                encoding="utf-8-sig").splitlines() if l.strip())}
        for p in plist:
            orig = v4_rows[p["id"]]
            # 前校验:原记录(补丁应用前)排序 JSON 原始 SHA
            if sorted_dump_sha(orig) != p["expected_record_sha256"]:
                print(f"[REJECT] {batch}/{p['id']} 原记录 SHA 不符")
                return 1
            r = dict(orig)
            for k, v in p["fields"].items():
                r[k] = v
            # 后校验:新数学摘要
            if sorted_dump_sha({k: r[k] for k in MATH_FIELDS}) != \
                    p["new_math_content_sha256"]:
                print(f"[REJECT] {batch}/{p['id']} 新数学 SHA 不符")
                return 1
            # v6 血缘绑定(前身链: v4 原件 -> 已发布 v5 -> 本 v6)
            old_vid = v5_rows[p["id"]].get("versioned_id", "")
            r["versioned_id"] = f"{V6}-20261005-{batch}-{p['id']}"
            lin = r.get("revision_lineage") or {}
            sr = r.get("strict_review") or {}
            lin["version"] = V6
            lin["previous_selected_version"] = {
                "version": "codex-repair-v5",
                "path": (f"reviews/2026-10-05-training-diversity-drafts/"
                         f"{batch}/draft-codex-repair-v5.jsonl"),
                "sha256": v5_fp["sha256"],
                "versioned_id": old_vid}
            notes = list(lin.get("math_correction_notes") or [])
            notes.append("v6: 严格前后哈希校验+路径别名修正(Codex msg505/506)")
            lin["math_correction_notes"] = notes
            r["revision_lineage"] = lin
            sr["math_content_sha256"] = p["new_math_content_sha256"]
            sr["math_review_evidence"] = (
                "reviews/codex-supervision/2026-10-05-draft-hash-compatibility/"
                "ready-row-separator-patches.json")
            r["strict_review"] = sr
            r["draft_status"] = f"CODEX-REPAIR-v6-NOT-ADMITTED"
            for i, x in enumerate(rows):
                if x["id"] == p["id"]:
                    rows[i] = r
                    break
        out = DRAFTS / batch / f"draft-{V6}.jsonl"
        if out.exists():
            print(f"目标已存在,拒绝覆盖: {out}")
            return 1
        result = publish_jsonl(out, rows)
        md = DRAFTS / batch / f"DRAFT_REPORT-{V6}.md"
        write_utf8_lf(md, md_for_batch(batch, rows, v5_fp["sha256"]))
        md_fp = fingerprint(md.read_bytes())
        receipts[batch] = {"v5": dict(v5_fp), "v6": dict(result),
                           "report": dict(md_fp)}
        print(f"{batch}: v6={result['sha256'][:12]} "
              f"patched={[p['id'] for p in plist]}")
    # 选择器切 v6 + 别名修正(根相对)
    for e in sel["entries"]:
        if e["batch"] not in receipts:
            continue
        r = receipts[e["batch"]]
        e["path"] = f"{e['batch']}/draft-{V6}.jsonl"
        e["sha256"] = r["v6"]["sha256"]
        e["raw_sha256"] = r["v6"]["raw_sha256"]
        e["hash_algorithm"] = NORMALIZED_HASH
        e["version"] = V6
        e["root_path"] = (f"reviews/2026-10-05-training-diversity-drafts/"
                          f"{e['batch']}/draft-{V6}.jsonl")
        e["source_path"] = (f"reviews/2026-10-05-training-diversity-drafts/"
                            f"{e['batch']}/draft-codex-repair-v5.jsonl")
        e["source_sha256"] = r["v5"]["sha256"]
        e["source_raw_sha256"] = r["v5"]["raw_sha256"]
        e["source_hash_algorithm"] = NORMALIZED_HASH
        e["report_path"] = f"{e['batch']}/DRAFT_REPORT-{V6}.md"
        e["report_sha256"] = r["report"]["sha256"]
        e["report_raw_sha256"] = r["report"]["raw_sha256"]
        e["report_hash_algorithm"] = NORMALIZED_HASH
        e["root_report_path"] = (f"reviews/2026-10-05-training-diversity-drafts/"
                                 f"{e['batch']}/DRAFT_REPORT-{V6}.md")
    sel["updated_by"] = "claude-row-separator-patches-v6-2026-10-05"
    write_utf8_lf(SEL, json.dumps(sel, ensure_ascii=False, indent=2) + "\n")
    out = DRAFTS / "repair-v6-summary.json"
    write_utf8_lf(out, json.dumps(receipts, ensure_ascii=False, indent=2) + "\n")
    print("选择器已切 v6(4 批,别名已修正)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
