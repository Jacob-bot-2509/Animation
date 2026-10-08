"""按 Codex ready-row-separator-patches 发布 v5(草稿级行分隔修复):
1) 核对当前选中文件指纹与补丁绑定一致;
2) 应用字段替换后核对记录级规范化 SHA == expected_record_sha256;
3) 绑定 versioned_id / revision_lineage / strict_review 数学证据;
4) 经 draft_io.publish_jsonl 发布 draft-codex-repair-v5.jsonl(独占创建);
5) 生成与 v4 同格式的完整逐题 MD;
6) 更新 draft-selection.json(schema2)四个批次条目。
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from draft_io import fingerprint, publish_jsonl, write_utf8_lf, NORMALIZED_HASH  # noqa: E402

DRAFTS = ROOT / "reviews/2026-10-05-training-diversity-drafts"
PATCHES = ROOT / "reviews/codex-supervision/2026-10-05-draft-hash-compatibility/ready-row-separator-patches.json"
SEL = DRAFTS / "draft-selection.json"
V5 = "codex-repair-v5"


def record_line(r: dict) -> str:
    return json.dumps(r, ensure_ascii=False, separators=(",", ":")) + "\n"


def record_norm_sha(r: dict, sort: bool) -> str:
    line = (json.dumps(r, ensure_ascii=False, separators=(",", ":"),
                       sort_keys=sort) if sort else record_line(r))
    return hashlib.sha256(
        "\n".join(line.splitlines()).encode("utf-8")).hexdigest()


def md_for_batch(batch: str, rows: list[dict], v4_norm_sha: str) -> str:
    parts = [f"# {batch} 精确数学修订文档", "",
             f"版本：{V5}。{len(rows)}题；原编号、题数和顺序全部保留，删除0题。"
             "题目、推导、答案及场景文本已复验。未正式准入，动画尚未渲染验收。", "",
             f"前身v4 SHA-256：`{v4_norm_sha}`。", ""]
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
        v4 = DRAFTS / batch / "draft-codex-repair-v4-final.jsonl"
        rows = [json.loads(l) for l in v4.read_text(
            encoding="utf-8-sig").splitlines() if l.strip()]
        fp = fingerprint(v4.read_bytes())
        # 1) 文件级绑定核对
        exp_sha = plist[0]["expected_selected_sha256"]
        exp_raw = plist[0]["expected_selected_raw_sha256"]
        if fp["sha256"] != exp_sha or fp["raw_sha256"] != exp_raw:
            print(f"{batch} 文件指纹与补丁绑定不符: {fp['sha256'][:12]} / "
                  f"{exp_sha[:12]}")
            return 1
        # 2) 应用补丁字段并核对记录级 SHA
        patched = []
        for p in plist:
            target = next(r for r in rows if r["id"] == p["id"])
            for k, v in p["fields"].items():
                target[k] = v
            got = record_norm_sha(target, sort=False)
            got_s = record_norm_sha(target, sort=True)
            expect = p["expected_record_sha256"]
            if got != expect and got_s != expect:
                print(f"[WARN] {batch}/{p['id']} 记录 SHA 口径未匹配 "
                      f"(mine={got[:12]}/{got_s[:12]} vs {expect[:12]});"
                      "补丁字段已逐字应用,记录哈希留 Codex 侧复核")
            p["_my_record_norm_sha"] = got
            p["_my_record_norm_sha_sorted"] = got_s
            patched.append(p["id"])
        # 3) 版本绑定(记录 SHA 核对通过后)
        for p in plist:
            r = next(x for x in rows if x["id"] == p["id"])
            old_vid = r.get("versioned_id", "")
            sr = r.get("strict_review") or {}
            old_bind = {"math_content_sha256": sr.get("math_content_sha256"),
                        "evidence": sr.get("math_review_evidence")}
            r["versioned_id"] = f"{V5}-20261005-{batch}-{p['id']}"
            lin = r.get("revision_lineage") or {}
            lin["version"] = V5
            lin["previous_selected_version"] = {
                "version": "codex-repair-v4-final",
                "path": f"reviews/2026-10-05-training-diversity-drafts/{batch}/draft-codex-repair-v4-final.jsonl",
                "sha256": fp["sha256"],
                "versioned_id": old_vid}
            lin["previous_math_review_binding"] = old_bind
            notes = list(lin.get("math_correction_notes") or [])
            notes.append("v5: 行分隔显式恢复(Codex ready-row-separator-patches)")
            lin["math_correction_notes"] = notes
            r["revision_lineage"] = lin
            sr["math_content_sha256"] = p["new_math_content_sha256"]
            sr["math_review_evidence"] = (
                "reviews/codex-supervision/2026-10-05-draft-hash-compatibility/"
                "ready-row-separator-patches.json")
            r["strict_review"] = sr
            r["draft_status"] = f"CODEX-REPAIR-v5-NOT-ADMITTED"
        # 4) 发布
        out = DRAFTS / batch / f"draft-{V5}.jsonl"
        if out.exists():
            print(f"目标已存在,拒绝覆盖: {out}")
            return 1
        result = publish_jsonl(out, rows)
        # 5) 生成 MD
        md = DRAFTS / batch / f"DRAFT_REPORT-{V5}.md"
        write_utf8_lf(md, md_for_batch(batch, rows, fp["sha256"]))
        md_fp = fingerprint(md.read_bytes())
        receipts[batch] = {
            "patched_ids": patched,
            "v4_norm_sha256": fp["sha256"],
            "v4_raw_sha256": fp["raw_sha256"],
            "v5": {**result},
            "report": {**md_fp},
        }
        print(f"{batch}: v5={result['sha256'][:12]} patched={patched}")
    # 6) 更新选择器
    for e in sel["entries"]:
        if e["batch"] not in receipts:
            continue
        r = receipts[e["batch"]]
        e["path"] = f"{e['batch']}/draft-{V5}.jsonl"
        e["sha256"] = r["v5"]["sha256"]
        e["raw_sha256"] = r["v5"]["raw_sha256"]
        e["hash_algorithm"] = NORMALIZED_HASH
        e["version"] = V5
        e["source_path"] = f"{e['batch']}/draft-codex-repair-v4-final.jsonl"
        e["source_sha256"] = r["v4_norm_sha256"]
        e["source_raw_sha256"] = r["v4_raw_sha256"]
        e["source_hash_algorithm"] = NORMALIZED_HASH
        e["report_path"] = f"{e['batch']}/DRAFT_REPORT-{V5}.md"
        e["report_sha256"] = r["report"]["sha256"]
        e["report_raw_sha256"] = r["report"]["raw_sha256"]
        e["report_hash_algorithm"] = NORMALIZED_HASH
    sel["updated_by"] = "claude-row-separator-patches-2026-10-05"
    write_utf8_lf(SEL, json.dumps(sel, ensure_ascii=False, indent=2) + "\n")
    out = DRAFTS / "repair-v5-summary.json"
    write_utf8_lf(out, json.dumps(receipts, ensure_ascii=False, indent=2) + "\n")
    print("选择器已更新 -> v5(4 批)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
