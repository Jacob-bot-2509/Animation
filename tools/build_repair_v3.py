"""构建 draft-codex-repair-v3(Codex msg_485-489 追加修复):
v3 = v2 + ①81 条 ready-field-patches(80 条 difficulty/variant_kind 元数据恢复
+ c15-05 乱码题完整证明替换)②c01-02 场景 \bx 非法命令补行分隔(msg_486)。
v2 保持已发布不变(不原地改哈希);逐批写 draft-codex-repair-v3.jsonl 与
DRAFT_REPORT-codex-repair-v3.md,并核对补丁 expected sha 与 v2 账本一致。
"""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path
from draft_io import require_legacy_selection

ROOT = Path(__file__).resolve().parents[1]
DRAFTS = ROOT / "reviews/2026-10-05-training-diversity-drafts"
PATCHES = ROOT / "reviews/codex-supervision/2026-10-05-draft-mail-reverification/ready-field-patches.json"
SEL = DRAFTS / "draft-selection.json"

C01_02_FIX = ("batch-01", "draft-c01-02", "scene_spec",
              r"1\bx+1", r"1\\bx+1")


def main() -> int:
    require_legacy_selection(SEL)
    sel = json.loads(SEL.read_text(encoding="utf-8"))
    selmap = {e["batch"]: e for e in sel["entries"]}
    patches = json.loads(PATCHES.read_text(encoding="utf-8"))
    by_batch: dict[str, dict[str, list[dict]]] = {}
    for r in patches["records"]:
        e = selmap.get(r["batch"])
        if e and e.get("source_sha256") != r.get("expected_selected_file_sha256"):
            print(f"补丁 SHA 绑定不符: {r['batch']}/{r['id']}")
            return 1
        by_batch.setdefault(r["batch"], {}).setdefault(r["id"], []).append(r)

    summary = {}
    total_applied = 0
    for batch, e in selmap.items():
        v2 = DRAFTS / batch / "draft-codex-repair-v2.jsonl"
        if not v2.is_file():
            continue
        rows = [json.loads(l) for l in v2.read_text(
            encoding="utf-8").splitlines() if l.strip()]
        applied = 0
        # ① 补丁
        for r in rows:
            for patch in by_batch.get(batch, {}).get(r["id"], []):
                for k, v in patch["fields"].items():
                    r[k] = v
                applied += 1
                total_applied += 1
        # ② c01-02 场景行分隔修复
        tb, tid, field, old, new = C01_02_FIX
        if tb == batch:
            for r in rows:
                if r["id"] != tid:
                    continue
                if field == "scene_spec":
                    spec = r["scene_spec"]
                    for k in ("objects", "steps"):
                        for i, s in enumerate(spec.get(k, [])):
                            if isinstance(s, str) and old in s:
                                spec[k][i] = s.replace(old, new)
                                applied += 1
                                total_applied += 1
        # ③ c15-05 溯源备注字段的编码损坏(问号串,原文不可恢复,写诚实占位)
        for r in rows:
            if r["id"] == "draft-c15-05":
                lin = r.get("revision_lineage") or {}
                if isinstance(lin, dict) and "?" in str(
                        lin.get("math_correction_notes", "")):
                    lin["math_correction_notes"] = (
                        "原备注字段编码损坏(问号串),内容不可恢复;"
                        "2026-10-05 v3 起由 Codex ready-field-patches 的完整"
                        "正交分解证明替换本题数学内容")
                    r["revision_lineage"] = lin
                    applied += 1
                    total_applied += 1
        # 写 v3
        v3 = DRAFTS / batch / "draft-codex-repair-v3.jsonl"
        v3.write_text("\n".join(json.dumps(r, ensure_ascii=False,
                                            separators=(",", ":"))
                                for r in rows) + "\n",
                      encoding="utf-8", newline="\n")
        md = [
            f"# {batch} 修复版 v3 变更说明",
            "",
            f"- 基线:v2 `draft-codex-repair-v2.jsonl`(SHA256 `{e['sha256']}`),v2 已发布不改动",
            f"- 变更:应用 Codex ready-field-patches({applied} 条)+ msg_486 场景行分隔修复",
            "- c15-05(若在本批):乱码段已由 Codex 补丁的完整正交分解证明替换",
            "- 其余:恢复原稿 difficulty、variant_kind 前缀改「结构改写：」",
            "- admitted 与 animation_render_verified 保持 false",
        ]
        rep = DRAFTS / batch / "DRAFT_REPORT-codex-repair-v3.md"
        rep.write_text("\n".join(md) + "\n", encoding="utf-8", newline="\n")
        summary[batch] = {
            "v2_sha256": e["sha256"],
            "v3_sha256": hashlib.sha256(v3.read_bytes()).hexdigest(),
            "report_sha256": hashlib.sha256(rep.read_bytes()).hexdigest(),
            "patches": applied,
        }
        print(f"{batch}: v3={summary[batch]['v3_sha256'][:12]} "
              f"patches={applied}")
    out = DRAFTS / "repair-v3-summary.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2),
                   encoding="utf-8", newline="\n")
    print(f"总应用 {total_applied} 处(应=82: 81 补丁+1 行分隔) -> {out.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
