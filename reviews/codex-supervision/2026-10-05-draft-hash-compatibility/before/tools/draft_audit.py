"""Codex 修改版草稿的独立检测(只读;2026-10-05)。

对象:reviews/2026-10-05-training-diversity-drafts/batch-*/draft-codex-repair-v1.jsonl
(Claude Code 生成、Codex 修改的 264 题草稿)

检查:结构/字段/身份(含 id 保留与 versioned_id)/answer-solution 一致性/
LaTeX/scene_spec/来源许可证/准入声明如实性/与训练池及冻结 eval-test 的
精确与近重复泄漏/批次间重复/清单哈希交叉核对。

约定:只读,不修改任何数据;输出逐条问题、汇总、逐条状态与原始文件哈希。

用法:
  python tools/draft_audit.py --out <dir> [--pool <jsonl/dir>]... [--eval-test <dir>]...
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "src"))

from dataset_audit import (  # noqa: E402
    Audit, check_consistency, check_latex, check_scene_spec,
    check_source_license, load_file, sha256_bytes,
)
from animtrain.near_dup import norm_text, shingles  # noqa: E402

DRAFT_GLOB = "reviews/2026-10-05-training-diversity-drafts/batch-*/draft-codex-repair-v1.jsonl"
ORIG_GLOB = "reviews/2026-10-05-training-diversity-drafts/batch-*/draft.jsonl"
SELECTION = "reviews/2026-10-05-training-diversity-drafts/draft-selection.json"
DELIVERY = ["reviews/codex-supervision/2026-10-05-batch-repair-execution/delivery-manifest.json",
            "reviews/codex-supervision/2026-10-05-remaining-batch-audit/delivery-manifest.json"]
NEAR_DUP_THRESHOLD = 0.7
REQUIRED = ["id", "category", "sub_category", "problem", "solution", "answer",
            "scene_spec", "source", "license", "method", "concept_id",
            "parent_training_ids", "draft_status", "versioned_id", "revision_lineage"]


def rid_of(rec: dict) -> str:
    return str(rec.get("id") or "<no-id>")


def jaccard_set(a: str, b: str) -> float:
    sa, sb = shingles(a), shingles(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def load_records(paths: list[Path]) -> list[dict]:
    out = []
    for p in paths:
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if line.strip():
                out.append({"file": str(p.relative_to(ROOT)).replace("\\", "/"),
                            "line": i, "record": json.loads(line)})
    return out


def check_structure(audit: Audit, paths: list[Path]) -> None:
    for p in paths:
        info = load_file(p)
        rel = info["path"]
        for msg in info["structure_issues"]:
            sev = "hard" if ("解析失败" in msg or "非 UTF-8" in msg) else "info"
            audit.add(sev, "S001" if sev == "hard" else "S002", rel, "document", msg)
        for d in info["dup_keys"]:
            audit.add("hard", "S003", rel, f"record[{d['index']}]",
                      f"重复键 {d['keys']}(后者覆盖前者)")


def check_record(audit: Audit, row: dict) -> None:
    rec, f, loc = row["record"], row["file"], f"line {row['line']}"
    rid = rid_of(rec)
    for field in REQUIRED:
        v = rec.get(field)
        missing = v is None or (isinstance(v, str) and not v.strip()) \
            or (isinstance(v, (list, dict)) and not v)
        if missing:
            audit.add("hard", "F001", f, loc, f"缺关键字段 {field}(id={rid})",
                      rid=rid, field=field)
        elif field in ("category", "sub_category", "problem", "solution", "answer",
                       "source", "license", "method", "concept_id", "draft_status",
                       "versioned_id") and not isinstance(v, str):
            audit.add("hard", "F002", f, loc,
                      f"{field} 不是字符串({type(v).__name__},id={rid})", rid=rid, field=field)
    if not isinstance(rec.get("scene_spec"), dict):
        audit.add("hard", "F003", f, loc, f"scene_spec 非对象(id={rid})", rid=rid)
    if not isinstance(rec.get("parent_training_ids"), list):
        audit.add("quarantine", "F004", f, loc,
                  f"parent_training_ids 非列表(id={rid})", rid=rid)
    # 准入声明如实性
    if rec.get("admitted") is not False:
        audit.add("hard", "F005", f, loc,
                  f"admitted={rec.get('admitted')!r} 非 False:草稿不得声称已准入(id={rid})",
                  rid=rid, field="admitted")
    if rec.get("animation_render_verified") not in (False, None):
        audit.add("hard", "F006", f, loc,
                  f"animation_render_verified={rec.get('animation_render_verified')!r} "
                  f"非 False:动画未验证不得声称已验证(id={rid})", rid=rid)
    if "NOT-ADMITTED" not in str(rec.get("draft_status", "")) and \
       str(rec.get("draft_status", "")) not in ("", "None"):
        audit.add("info", "F007", f, loc,
                  f"draft_status={rec.get('draft_status')!r} 未含 NOT-ADMITTED(id={rid})",
                  rid=rid, field="draft_status")
    # 身份保留
    lin = rec.get("revision_lineage") or {}
    if isinstance(lin, dict) and lin.get("original_id") not in (None, "", rid):
        audit.add("hard", "I001", f, loc,
                  f"id 与 revision_lineage.original_id 不一致({rid} vs "
                  f"{lin.get('original_id')})", rid=rid, field="revision_lineage")
    vid = rec.get("versioned_id")
    if isinstance(vid, str) and rid not in vid:
        audit.add("info", "I002", f, loc,
                  f"versioned_id 未包含原 id({vid} vs {rid})", rid=rid, field="versioned_id")


def check_encoding(audit: Audit, info: dict, r: dict, rid: str) -> None:
    """递归检测编码损坏:U+FFFD、连续问号、控制字符(Codex msg_487 要求)。"""
    def walk(v, path):
        if isinstance(v, str):
            if "�" in v:
                audit.add("quarantine", "E001", info["path"], r["locator"],
                          f"{path} 含替换字符 U+FFFD(id={rid})", rid=rid)
            if "??" in v:
                audit.add("quarantine", "E002", info["path"], r["locator"],
                          f"{path} 含连续问号(id={rid})", rid=rid)
            for ch in v:
                if ord(ch) < 0x20 or ord(ch) == 0x7f:
                    audit.add("quarantine", "E003", info["path"], r["locator"],
                              f"{path} 含控制字符 U+{ord(ch):04X}(id={rid})",
                              rid=rid)
                    break
        elif isinstance(v, dict):
            for k, vv in v.items():
                walk(vv, f"{path}.{k}")
        elif isinstance(v, list):
            for i, vv in enumerate(v):
                walk(vv, f"{path}[{i}]")
    walk(r["record"], "record")


def refine_issues(audit: Audit) -> None:
    """误报修正(与 eval_test_audit 同口径):\\frac 单 token、\\leftarrow 均合法。"""
    for it in audit.issues:
        blob = f"{it.get('message') or ''} {it.get('evidence') or ''}"
        if it["code"] == "L009":
            it["severity"] = "info"
            it["message"] += "(Lead 复核:\\frac/\\dfrac 单 token 参数为合法 TeX,仅风格建议)"
        if it["code"] == "L006" and re.search(r"\\+left[a-zA-Z]", blob):
            it["severity"] = "info"
            it["message"] += "(Lead 复核:实为 \\leftarrow 类命令,非未配对 \\left)"
        if it["code"] == "C008" and "pmatrix" in blob:
            it["severity"] = "info"
            it["message"] += "(Lead 复核:矩阵幂恒等演示,非笔误)"
        # C008 误报:逗号并列的多条直线/点(x=1/2,y=1/2,y=x)被读成“重复等式”
        if it["code"] == "C008" and re.search(r"[0-9]/[0-9],\s*[a-zA-Z]=|[0-9],\s*[a-zA-Z]=", blob):
            it["severity"] = "info"
            it["message"] += "(Lead 复核:该处为逗号并列的多条直线/点枚举,非重复等式)"
        # L008 误报(仅限确认的 sin 函数参数写法):\sin^23\theta 单字符上标后接系数合法
        if it["code"] == "L008" and re.search(r"\\sin\^2\d", blob):
            it["severity"] = "info"
            it["message"] += "(Lead 复核:\\sin^2 后接系数为 sin 函数参数写法,合法 TeX;"
            "其余 \\^2\\d 不自动降级)"


def attribute_to_repair(audit: Audit, rows: list[dict], orig_rows: list[dict]) -> dict:
    """把问题归因到“Codex 修改引入”还是“原始草稿已有”。"""
    orig = {rid_of(r["record"]): r["record"] for r in orig_rows}
    cjk = re.compile(r"[\u4e00-\u9fff]")
    ms = re.compile(r"\$([^$]*)\$")
    step_pref = re.compile(r"^\s*第[一二三四五六七八九十\d]+步")
    introduced_cjk = []
    preexisting_cjk = []
    introduced_steps = []
    for row in rows:
        rid = rid_of(row["record"])
        o = orig.get(rid)
        new_cjk = any(cjk.search(m.group(1))
                      for fld in ("problem", "solution", "answer")
                      for m in ms.finditer(str(row["record"].get(fld) or "")))
        old_cjk = bool(o) and any(cjk.search(m.group(1))
                                  for fld in ("problem", "solution", "answer")
                                  for m in ms.finditer(str(o.get(fld) or "")))
        if new_cjk and not old_cjk:
            introduced_cjk.append(rid)
        elif new_cjk and old_cjk:
            preexisting_cjk.append(rid)
        new_steps = row["record"]["scene_spec"]["steps"]
        old_steps = (o or {}).get("scene_spec", {}).get("steps") or []
        if old_steps and all(step_pref.match(s) for s in old_steps) and \
           not all(step_pref.match(s) for s in new_steps):
            introduced_steps.append(rid)
    if introduced_cjk:
        audit.add("hard", "L010", DRAFT_GLOB, "document",
                  f"{len(introduced_cjk)} 题的“公式内中文”是本次修改新引入的(原始草稿无):"
                  f"{introduced_cjk}——修复动作引入的新硬伤,须回退或改为公式外文本",
                  action="把这 3-5 题的中文移出 $...$ 或加 CJK 字体方案")
    if preexisting_cjk:
        audit.add("quarantine", "L011", DRAFT_GLOB, "document",
                  f"{len(preexisting_cjk)} 题的公式内中文在原始草稿中已存在,本次未清:"
                  f"{preexisting_cjk}")
    if introduced_steps:
        audit.add("quarantine", "V010", DRAFT_GLOB, "document",
                  f"{len(introduced_steps)} 题的 scene_spec.steps 在本次修改中丢失了"
                  "“第N步”前缀(原始草稿全部带前缀)", action="还原统一编号或确认新写法")
    return {"introduced_cjk": introduced_cjk, "preexisting_cjk": preexisting_cjk,
            "introduced_step_prefix_loss": len(introduced_steps),
            "step_prefix_loss_ids": introduced_steps[:20]}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--pool", action="append", default=[],
                    help="训练池 JSONL 或目录(可重复)")
    ap.add_argument("--eval-test", action="append", default=[],
                    help="冻结 eval/test 目录或文件(可重复)")
    ap.add_argument("--drafts", default="",
                    help="草稿 glob(可选;缺省审计 codex-repair-v1)")
    args = ap.parse_args(argv)
    outdir = ROOT / args.out
    outdir.mkdir(parents=True, exist_ok=True)

    audit = Audit()
    draft_glob = args.drafts or DRAFT_GLOB
    draft_paths = sorted(ROOT.glob(draft_glob))
    orig_paths = sorted(ROOT.glob(ORIG_GLOB))
    rows = load_records(draft_paths)

    check_structure(audit, draft_paths)
    for row in rows:
        rid = rid_of(row["record"])
        info = {"path": row["file"], "format": "jsonl"}
        r = {"locator": f"line {row['line']}", "record": row["record"]}
        check_record(audit, row)
        check_encoding(audit, info, r, rid)
        check_source_license(audit, info, r, rid)
        check_consistency(audit, info, r, rid)
        check_latex(audit, info, r, rid)
        check_scene_spec(audit, info, r, rid)

    # ---- 身份唯一性 ----
    ids = [rid_of(r["record"]) for r in rows]
    for i, c in collections.Counter(ids).items():
        if c > 1:
            audit.add("hard", "I003", DRAFT_GLOB, "document",
                      f"id 在草稿集内重复 {c} 次:{i}", rid=i)
    vids = [str(r["record"].get("versioned_id")) for r in rows]
    for i, c in collections.Counter(vids).items():
        if c > 1:
            audit.add("hard", "I004", DRAFT_GLOB, "document",
                      f"versioned_id 重复 {c} 次:{i}")

    # ---- 泄漏:与训练池 / 冻结 eval-test / 批次间 ----
    def expand(paths: list[str]) -> list[Path]:
        out: list[Path] = []
        for s in paths:
            p = ROOT / s
            if p.is_dir():
                out += sorted(p.rglob("*.jsonl"))
            elif p.exists():
                out.append(p)
        return out

    pool_paths = expand(args.pool)
    ev_paths = expand(args.eval_test)
    pool_recs = load_records(pool_paths) if pool_paths else []
    ev_recs = load_records(ev_paths) if ev_paths else []
    for name, ref in (("训练池", pool_recs), ("冻结 eval/test", ev_recs)):
        if not ref:
            continue
        idx = {}
        for rr in ref:
            idx.setdefault(sha256_bytes(str(rr["record"].get("problem") or "").encode()),
                           rr)
        for row in rows:
            h = sha256_bytes(str(row["record"].get("problem") or "").encode())
            if h in idx:
                hit = idx[h]
                audit.add("hard", "X001", row["file"], f"line {row['line']}",
                          f"{name}核心题干精确重叠:{rid_of(row['record'])} ↔ "
                          f"{rid_of(hit['record'])}({hit['file']})",
                          rid=rid_of(row["record"]), field="problem")
        worst = (0.0, None, None)
        for row in rows:
            ps = str(row["record"].get("problem") or "")
            for rr in ref:
                sim = jaccard_set(ps, str(rr["record"].get("problem") or ""))
                if sim > worst[0]:
                    worst = (sim, row, rr)
                if sim >= NEAR_DUP_THRESHOLD:
                    audit.add("hard", "X002", row["file"], f"line {row['line']}",
                              f"与{name}近重复 {sim:.4f} ≥ {NEAR_DUP_THRESHOLD}:"
                              f"{rid_of(row['record'])} ↔ {rid_of(rr['record'])}"
                              f"({rr['file']})", rid=rid_of(row["record"]), field="problem")
        audit.add("info", "X003", DRAFT_GLOB, "document",
                  f"与{name}的最大题干近重复:set 口径 {worst[0]:.4f}"
                  + (f"(草稿 {rid_of(worst[1]['record'])} ↔ {rid_of(worst[2]['record'])})"
                     if worst[1] else ""))
    # 批次间重复
    seen: dict[str, dict] = {}
    for row in rows:
        h = sha256_bytes(str(row["record"].get("problem") or "").encode())
        if h in seen:
            audit.add("hard", "X004", row["file"], f"line {row['line']}",
                      f"草稿集内题干重复:{rid_of(row['record'])} ↔ "
                      f"{rid_of(seen[h]['record'])}({seen[h]['file']})",
                      rid=rid_of(row["record"]), field="problem")
        else:
            seen[h] = row
    intra = (0.0, None, None)
    texts = [(str(r["record"].get("problem") or ""), r) for r in rows]
    for i in range(len(texts)):
        for j in range(i + 1, len(texts)):
            sim = jaccard_set(texts[i][0], texts[j][0])
            if sim > intra[0]:
                intra = (sim, texts[i][1], texts[j][1])
    audit.add("info", "X005", DRAFT_GLOB, "document",
              f"草稿集内最大题干近重复:{intra[0]:.4f}"
              + (f"({rid_of(intra[1]['record'])} ↔ {rid_of(intra[2]['record'])})"
                 if intra[1] else ""))

    # ---- 与原始草稿对比:id 保留/条数 ----
    orig_rows = load_records(orig_paths)
    attribution = {}
    if orig_rows:
        attribution = attribute_to_repair(audit, rows, orig_rows)
        o_ids = [rid_of(r["record"]) for r in orig_rows]
        n_ids = [rid_of(r["record"]) for r in rows]
        if len(o_ids) != len(n_ids):
            audit.add("quarantine", "V001", DRAFT_GLOB, "document",
                      f"条数变化:原始 {len(o_ids)} → Codex 修改 {len(n_ids)}")
        missing = [i for i in o_ids if i not in set(n_ids)]
        added = [i for i in n_ids if i not in set(o_ids)]
        if missing:
            audit.add("hard", "V002", DRAFT_GLOB, "document",
                      f"原始 id 在修改版中缺失 {len(missing)} 个:{missing[:5]}")
        if added:
            audit.add("quarantine", "V003", DRAFT_GLOB, "document",
                      f"修改版新增 id {len(added)} 个:{added[:5]}")
        if not missing and not added and o_ids == n_ids:
            audit.add("info", "V004", DRAFT_GLOB, "document",
                      f"原始 id 与顺序完整保留({len(o_ids)} 条)")
        n_changed = 0
        # 按 id 对齐比较内容
        omap = {rid_of(r["record"]): r["record"] for r in orig_rows}
        for r in rows:
            o = omap.get(rid_of(r["record"]))
            if o is not None and json.dumps(o, sort_keys=True, ensure_ascii=False) != \
               json.dumps(r["record"], sort_keys=True, ensure_ascii=False):
                n_changed += 1
        audit.add("info", "V005", DRAFT_GLOB, "document",
                  f"与原始草稿内容不同的记录:{n_changed}/{len(rows)}")

    # ---- 清单哈希交叉核对 ----
    sel = ROOT / SELECTION
    if sel.exists():
        d = json.loads(sel.read_text(encoding="utf-8"))
        entries = {e.get("batch"): e for e in d.get("entries", [])}
        for p in draft_paths:
            batch = p.parent.name
            e = entries.get(batch)
            if not e:
                audit.add("quarantine", "V006", SELECTION, "document",
                          f"draft-selection.json 未登记 {batch}")
                continue
            # 账本 path 相对草稿目录;统一转成相对项目根的 posix 再比较
            rel = p.relative_to(ROOT).as_posix()
            expected = (Path(DRAFT_GLOB.split("/batch-")[0])
                        / e.get("path", "")).as_posix()
            if e.get("path") and expected != rel:
                audit.add("info", "V011", SELECTION, batch,
                          f"被审文件 {rel} 不是账本选中版本({e.get('path')}),跳过哈希核对")
                continue
            actual = sha256_bytes(p.read_bytes())
            if actual != e.get("sha256"):
                audit.add("hard", "V007", SELECTION, batch,
                          f"{batch} 哈希与 draft-selection.json 不符"
                          f"(清单 {str(e.get('sha256'))[:12]}… vs 实际 {actual[:12]}…)")
            n = len([l for l in p.read_text(encoding="utf-8").splitlines() if l.strip()])
            if e.get("count") != n:
                audit.add("hard", "V008", SELECTION, batch,
                          f"{batch} 条数与清单不符({e.get('count')} vs {n})")
        sel_total = sum(e.get("count", 0) for e in d.get("entries", []))
        audit.add("info", "V009", SELECTION, "document",
                  f"draft-selection.json:状态={d.get('status')} 声明总数={sel_total} "
                  f"实际={len(rows)} 删除题={d.get('deleted_questions')}")

    # ---- 输出 ----
    refine_issues(audit)
    issues = audit.issues
    by_rec: dict[str, dict[str, int]] = collections.defaultdict(
        lambda: {"hard": 0, "quarantine": 0, "info": 0})
    for it in issues:
        if it.get("id"):
            by_rec[it["id"]][it["severity"]] += 1
    status_rows = []
    for row in rows:
        rid = rid_of(row["record"])
        c = by_rec.get(rid, {"hard": 0, "quarantine": 0, "info": 0})
        status_rows.append({
            "batch": Path(row["file"]).parent.name, "file": row["file"],
            "line": row["line"], "id": rid,
            "versioned_id": row["record"].get("versioned_id"),
            "category": row["record"].get("category"),
            "sub_category": row["record"].get("sub_category"),
            "draft_status": row["record"].get("draft_status"),
            "review_disposition": row["record"].get("review_disposition"),
            "admitted": row["record"].get("admitted"),
            "animation_render_verified": row["record"].get("animation_render_verified"),
            "status": ("rejected" if c["hard"] else
                       "quarantine" if c["quarantine"] else "clean"),
            "n_hard": c["hard"], "n_quarantine": c["quarantine"], "n_info": c["info"],
        })
    hash_files = []
    for p in draft_paths + orig_paths + [sel] + [ROOT / d for d in DELIVERY] \
            + pool_paths + ev_paths:
        if p.exists():
            b = p.read_bytes()
            hash_files.append({"file": str(p.relative_to(ROOT)).replace("\\", "/"),
                               "sha256": sha256_bytes(b), "size": len(b)})
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tool": "tools/draft_audit.py (只读)",
        "scope": {"drafts": [str(p.relative_to(ROOT)).replace("\\", "/") for p in draft_paths],
                  "originals": [str(p.relative_to(ROOT)).replace("\\", "/") for p in orig_paths],
                  "pool": [str(p.relative_to(ROOT)).replace("\\", "/") for p in pool_paths],
                  "eval_test": [str(p.relative_to(ROOT)).replace("\\", "/") for p in ev_paths]},
        "totals": {"draft_records": len(rows), "batches": len(draft_paths),
                   "original_records": len(orig_rows)},
        "severity_counts": dict(collections.Counter(i["severity"] for i in issues)),
        "issue_code_counts": dict(collections.Counter(i["code"] for i in issues)),
        "record_status_counts": dict(collections.Counter(r["status"] for r in status_rows)),
        "categories": dict(collections.Counter(r["category"] for r in rows
                                               for r in [r["record"]])),
        "admitted_true": sum(1 for r in rows if r["record"].get("admitted") is True),
        "render_verified_true": sum(
            1 for r in rows if r["record"].get("animation_render_verified") is True),
        "per_batch": {Path(r["file"]).parent.name: sum(
            1 for x in status_rows if x["batch"] == Path(r["file"]).parent.name)
            for r in rows},
        "attribution": attribution,
    }
    (outdir / "issues.jsonl").write_text(
        "\n".join(json.dumps(i, ensure_ascii=False) for i in issues) + "\n", encoding="utf-8")
    (outdir / "record_status.jsonl").write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in status_rows) + "\n",
        encoding="utf-8")
    import csv
    with (outdir / "record_status.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(status_rows[0].keys()))
        w.writeheader()
        w.writerows(status_rows)
    (outdir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    (outdir / "file_hashes.json").write_text(
        json.dumps({"generated_at": summary["generated_at"], "files": hash_files},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    (outdir / "file_hashes.sha256").write_text(
        "\n".join(f"{h['sha256']}  {h['file']}" for h in hash_files) + "\n",
        encoding="utf-8")

    print(f"[草稿检测] 批次={len(draft_paths)} 记录={len(rows)} 原始={len(orig_rows)}")
    print(f"[严重度] {summary['severity_counts']}")
    print(f"[逐条状态] {summary['record_status_counts']}")
    print(f"[声明核查] admitted=true: {summary['admitted_true']} | "
          f"render_verified=true: {summary['render_verified_true']}")
    print(f"[输出] {outdir}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
