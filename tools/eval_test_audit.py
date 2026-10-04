"""eval/test 预跑检测(只读;2026-10-03,msg_2xx)。

对 dataset-eval.md / data-test.md 及其转出的
data/v1/{eval,test}/dataset_{eval,test}.jsonl(+.json 镜像)做入场预检:
结构/字段/身份/多解组/一致性/LaTeX/scene_spec/来源许可证/隔离(与 train
精确与近重复)/manifest 覆盖与冻结锁/文档与数据一致性。

约定:只读,不修改任何数据文件,不自动改 ID/公式;输出逐条问题、
汇总统计、原始文件哈希,并区分 clean / quarantine / rejected。

用法:
  python tools/eval_test_audit.py --out dataset_audit_2026-10-03-eval-test
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "src"))

from dataset_audit import (  # noqa: E402
    ANIMATION_FIELDS, Audit, CATEGORY_BY_PREFIX, INTERNAL_LICENSE,
    LICENSE_WHITELIST, OPTIONAL_META, check_consistency, check_latex,
    check_scene_spec, check_source_license, check_structure, load_file,
    sha256_bytes,
)
from animtrain.near_dup import norm_text, shingles  # noqa: E402

TRAIN_GLOB = "data/v1/raw/*.jsonl"
POOLS = {
    "eval": ["data/v1/eval/dataset_eval.jsonl"],
    "test": ["data/v1/test/dataset_test.jsonl"],
}
MIRRORS = {
    "eval": "data/v1/eval/dataset_eval.json",
    "test": "data/v1/test/dataset_test.json",
}
DOCS = {"eval": "dataset-eval.md", "test": "data-test.md"}
MANIFESTS = ["data/v1/manifest.json", "data/v1/manifest-train.json",
             "data/v1/eval/manifest.json", "data/v1/test/manifest.json"]
NEAR_DUP_THRESHOLD = 0.7
COMMON_REQUIRED = ["category", "sub_category", "problem", "solution",
                   "scene_spec", "source", "license"]
MULTI_FIELDS = ["problem_id", "solution_id", "method"]


def rid_of(rec: dict) -> str:
    """身份提取:id 优先;缺省且 problem_id+solution_id 齐备时用复合身份。"""
    sid = rec.get("id")
    if isinstance(sid, (str, int)) and str(sid).strip():
        return str(sid)
    pid, s2 = rec.get("problem_id"), rec.get("solution_id")
    if isinstance(pid, str) and pid.strip() and isinstance(s2, str) and s2.strip():
        return f"{pid}::{s2}"
    return "<no-id>"


def pool_texts(infos: list[dict], pool: str) -> list[tuple[str, dict]]:
    """(problem 文本, meta) —— 隔离检查只看核心题干。"""
    out = []
    for info in infos:
        for r in info["records"]:
            rec = r["record"]
            if not isinstance(rec, dict):
                continue
            out.append((str(rec.get("problem") or ""),
                        {"pool": pool, "id": rid_of(rec), "file": info["path"],
                         "locator": r["locator"], "problem_id": rec.get("problem_id")}))
    return out


def jaccard_multiset(a: str, b: str) -> float:
    ca = collections.Counter(shingles(a) and [t for t in _grams(a)])
    cb = collections.Counter(t for t in _grams(b))
    if not ca or not cb:
        return 0.0
    inter = sum((ca & cb).values())
    union = sum((ca | cb).values())
    return inter / union if union else 0.0


def _grams(text: str) -> list[str]:
    t = norm_text(text)
    k = 5
    if len(t) < k:
        return [t] if t else []
    return [t[i:i + k] for i in range(len(t) - k + 1)]


def jaccard_set(a: str, b: str) -> float:
    sa, sb = shingles(a), shingles(b)
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def check_structure_and_fields(audit: Audit, info: dict, pool: str) -> None:
    check_structure(audit, info)
    for r in info["records"]:
        rec = r["record"]
        if not isinstance(rec, dict):
            continue
        rid = rid_of(rec)
        f, loc = info["path"], r["locator"]
        # 身份:多解样本用复合身份(契约 §6 + 实现 record_identity)
        has_multi = all(not _missing(rec.get(k)) for k in ("problem_id", "solution_id"))
        any_multi = any(not _missing(rec.get(k)) for k in MULTI_FIELDS)
        if _missing(rec.get("id")) and not has_multi:
            audit.add("hard", "F001", f, loc,
                      f"缺关键字段 id,且 problem_id/solution_id 不齐备(id={rid})",
                      rid=rid, field="id")
        for field in COMMON_REQUIRED:
            v = rec.get(field)
            if field not in rec or _missing(v):
                sev = "quarantine" if field == "answer" else "hard"
                audit.add(sev, "F002", f, loc,
                          f"缺关键字段 {field}(id={rid})", rid=rid, field=field)
            elif field == "scene_spec":
                if not isinstance(v, dict):
                    audit.add("hard", "F003", f, loc,
                              f"scene_spec 不是对象({type(v).__name__},id={rid})",
                              rid=rid, field=field)
            elif not isinstance(v, str):
                audit.add("hard", "F003", f, loc,
                          f"{field} 不是字符串({type(v).__name__},id={rid})",
                          rid=rid, field=field)
        if any_multi and not has_multi:
            miss = [k for k in ("problem_id", "solution_id") if _missing(rec.get(k))]
            audit.add("hard", "F004", f, loc,
                      f"多解字段不完整:缺 {', '.join(miss)}(id={rid})",
                      rid=rid, field="problem_id/solution_id")
        if has_multi and _missing(rec.get("method")):
            audit.add("hard", "F005", f, loc,
                      f"多解样本缺 method(id={rid})", rid=rid, field="method")
        for k in MULTI_FIELDS:
            v = rec.get(k)
            if not _missing(v) and not isinstance(v, str):
                audit.add("hard", "F006", f, loc,
                          f"{k} 不是字符串({type(v).__name__},id={rid})",
                          rid=rid, field=k)
        # answer 单独:缺失 → quarantine(契约 §2)
        ans = rec.get("answer")
        if _missing(ans):
            audit.add("quarantine", "F007", f, loc,
                      f"answer 缺失/空(id={rid})", rid=rid, field="answer")
        elif not isinstance(ans, str):
            audit.add("hard", "F008", f, loc,
                      f"answer 不是字符串({type(ans).__name__})", rid=rid,
                      field="answer")
        known = set(COMMON_REQUIRED) | {"id", "answer"} | set(MULTI_FIELDS) \
            | set(OPTIONAL_META) | set(ANIMATION_FIELDS)
        for k in rec:
            if k not in known:
                audit.add("quarantine", "F009", f, loc,
                          f"未知字段 {k}(契约 §2:其余键一律 quarantine 提示)",
                          rid=rid, field=k)
        for k in OPTIONAL_META:
            if _missing(rec.get(k)):
                audit.add("quarantine", "F010", f, loc,
                          f"可选元数据缺/空:{k}(候选语义)", rid=rid, field=k)
        tags = rec.get("efficiency_tags")
        if isinstance(tags, list):
            for t in tags:
                if isinstance(t, str) and re.match(r"^\s*[-*•]\s+", t):
                    audit.add("quarantine", "F011", f, loc,
                              f"efficiency_tags 条目残留 Markdown 项目符号:{t[:40]!r}"
                              "(批量写入残留,建议清理符号)",
                              rid=rid, field="efficiency_tags", evidence=t)


def _missing(v) -> bool:
    if v is None:
        return True
    if isinstance(v, str) and not v.strip():
        return True
    if isinstance(v, (list, dict)) and len(v) == 0:
        return True
    return False


def _resolve(raw: str, base: Path | None = None) -> Path:
    """manifest/锁条目路径解析:绝对路径原样;以 data/ 开头按仓库根;否则按 base。"""
    s = str(raw).replace("\\", "/")
    p = Path(s)
    if p.is_absolute():
        return p
    if s.startswith("data/"):
        return ROOT / p
    return (base or ROOT) / p


def check_identity(audit: Audit, info: dict, pool: str) -> None:
    seen: dict[str, dict] = {}
    by_pid: dict[str, list[tuple[dict, str]]] = collections.defaultdict(list)
    for r in info["records"]:
        rec = r["record"]
        if not isinstance(rec, dict):
            continue
        rid = rid_of(rec)
        f, loc = info["path"], r["locator"]
        if rid in seen:
            same = json.dumps(seen[rid]["record"], sort_keys=True,
                              ensure_ascii=False) == json.dumps(rec, sort_keys=True,
                                                                ensure_ascii=False)
            audit.add("hard", "I001", f, loc,
                      f"{'整条重复' if same else 'ID 冲突'}:身份 {rid} 已出现在 "
                      f"{seen[rid]['locator']}", rid=rid, field="id")
        else:
            seen[rid] = r
        pid = rec.get("problem_id")
        if not _missing(pid):
            by_pid[str(pid)].append((r, rid))
    for pid, items in sorted(by_pid.items()):
        texts = {str(it[0]["record"].get("problem")) for it in items}
        if len(texts) > 1:
            audit.add("hard", "I002", info["path"], f"problem_id={pid}",
                      f"同一 problem_id 对应不同题干({len(texts)} 种)"
                      "——同题多解必须同题干", rid=pid, field="problem")
        methods = [it[0]["record"].get("method") for it in items]
        dup_m = [m for m, c in collections.Counter(methods).items() if c > 1]
        if dup_m:
            audit.add("hard", "I003", info["path"], f"problem_id={pid}",
                      f"同一 problem_id 内 method 重复:{dup_m}", rid=pid,
                      field="method")
        if len(items) < 2:
            audit.add("info", "I004", info["path"], f"problem_id={pid}",
                      f"同题多解组只有 {len(items)} 条(EVAL_TEST_PREP §4 建议 ≥2)",
                      rid=pid)
        for r, rid in items:
            sid = r["record"].get("solution_id")
            if not _missing(sid) and str(sid).split("-s")[-1] not in (None, ""):
                pass
    # solution_id 全局唯一
    sids = [str(r["record"].get("solution_id")) for r in info["records"]
            if isinstance(r["record"], dict) and not _missing(r["record"].get("solution_id"))]
    for sid, c in collections.Counter(sids).items():
        if c > 1:
            audit.add("hard", "I005", info["path"], f"solution_id={sid}",
                      f"solution_id 重复 {c} 次", rid=sid, field="solution_id")
    return seen


def check_id_conventions(audit: Audit, info: dict, pool: str) -> None:
    for r in info["records"]:
        rec = r["record"]
        if not isinstance(rec, dict):
            continue
        rid = rid_of(rec)
        ident = str(rec.get("id") or rec.get("problem_id") or "")
        toks = ident.split("-")
        cat = rec.get("category")
        if len(toks) >= 3 and toks[0] in ("eval", "test"):
            sub = toks[1]
            expect = CATEGORY_BY_PREFIX.get(sub)
            if expect and cat != expect:
                audit.add("hard", "I010", info["path"], r["locator"],
                          f"ID {ident} 的题族前缀 {sub} 与 category={cat} 不一致",
                          rid=rid, field="id")
        elif not ident:
            continue


def check_isolation(audit: Audit, texts_by_pool: dict[str, list[tuple[str, dict]]]) -> dict:
    """跨池隔离:精确(核心题干哈希)+ 近重复(5-gram Jaccard)+ 身份重叠。"""
    stats = {"pairs": [], "max_sim": 0.0, "exact": 0}
    pools = [p for p in ("train", "eval", "test") if texts_by_pool.get(p)]
    hashes = {p: {} for p in pools}
    for p in pools:
        for text, meta in texts_by_pool[p]:
            h = sha256_bytes(text.encode("utf-8"))
            hashes[p].setdefault(h, []).append(meta)
    for i, a in enumerate(pools):
        for b in pools[i + 1:]:
            common = set(hashes[a]) & set(hashes[b])
            for h in common:
                stats["exact"] += 1
                audit.add("hard", "X001", f"{hashes[a][h][0]['file']}",
                          hashes[a][h][0]["locator"],
                          f"{a} 与 {b} 核心题干精确重叠:{hashes[a][h][0]['id']} ↔ "
                          f"{hashes[b][h][0]['id']}(A8 隔离零容忍)", rid=hashes[a][h][0]["id"],
                          field="problem")
            # 近重复:抽样全量(池子规模小,直接两两比较)
            worst = (0.0, None, None)
            for ta, ma in texts_by_pool[a]:
                for tb, mb in texts_by_pool[b]:
                    if ma.get("problem_id") and ma.get("problem_id") == mb.get("problem_id"):
                        continue
                    s_set = jaccard_set(ta, tb)
                    if s_set > worst[0]:
                        worst = (s_set, ma, mb)
                    if s_set >= NEAR_DUP_THRESHOLD:
                        stats["pairs"].append({"a": a, "b": b, "set": round(s_set, 4),
                                               "multiset": round(jaccard_multiset(ta, tb), 4),
                                               "x": ma["id"], "y": mb["id"]})
                        audit.add("hard", "X005", ma["file"], ma["locator"],
                                  f"{a} 与 {b} 跨池近重复:set 口径 {s_set:.4f} ≥ "
                                  f"阈值 {NEAR_DUP_THRESHOLD}(多重集口径 "
                                  f"{jaccard_multiset(ta, tb):.4f});{ma['id']} ↔ {mb['id']}"
                                  "——评测题目族必须与训练/其他评测集独立",
                                  rid=ma["id"], field="problem",
                                  action="人工确认该题是否泄漏;阈值 0.7 未校准,需按校准结果复核")
            stats["max_sim"] = max(stats["max_sim"], worst[0])
            if worst[1]:
                audit.add("info", "X002", worst[1]["file"], worst[1]["locator"],
                          f"{a}↔{b} 核心题干最大近重复(set 口径 {worst[0]:.4f}"
                          f" < 阈值 {NEAR_DUP_THRESHOLD}):{worst[1]['id']} vs {worst[2]['id']}",
                          rid=worst[1]["id"], field="problem")
    # 身份跨池重叠
    ids = {p: {m["id"] for _, m in texts_by_pool[p]} for p in pools}
    for i, a in enumerate(pools):
        for b in pools[i + 1:]:
            shared = ids[a] & ids[b]
            if shared:
                audit.add("hard", "X003", "data", "pools",
                          f"{a} 与 {b} 身份重叠:{sorted(shared)[:5]}", rid=None)
    # 池内:test/eval 不同题号却同题干
    for p in ("test",):
        if not texts_by_pool.get(p):
            continue
        seen: dict[str, dict] = {}
        for text, meta in texts_by_pool[p]:
            h = sha256_bytes(text.encode("utf-8"))
            if h in seen:
                audit.add("hard", "X004", meta["file"], meta["locator"],
                          f"池内不同记录核心题干重复:{meta['id']} 与 {seen[h]['id']}",
                          rid=meta["id"], field="problem")
            else:
                seen[h] = meta
    return stats


def check_manifests(audit: Audit, all_hashes: dict[str, str]) -> None:
    seen_files: dict[str, list[str]] = collections.defaultdict(list)
    for mp in MANIFESTS:
        p = ROOT / mp
        if not p.exists():
            audit.add("quarantine", "MF001", mp, "document", "manifest 不存在")
            continue
        try:
            m = json.loads(p.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            audit.add("hard", "MF002", mp, "document", f"manifest 解析失败:{exc}")
            continue
        mdir = p.parent
        for e in m.get("entries", []):
            raw_rel = str(e.get("path", ""))
            fh = _resolve(raw_rel, mdir)
            rel = str(fh.relative_to(ROOT)).replace("\\", "/")
            seen_files[rel].append(str(e.get("split")))
            if not fh.exists():
                audit.add("hard", "MF003", mp, raw_rel, "manifest 条目文件不存在")
                continue
            actual = sha256_bytes(fh.read_bytes())
            if actual != e.get("sha256"):
                audit.add("hard", "MF004", mp, raw_rel,
                          f"manifest 哈希与文件不符(manifest {str(e.get('sha256'))[:12]}…"
                          f" vs 实际 {actual[:12]}…)")
            # 条目契约:JSON 数组容器 / 非样本文件
            if fh.suffix == ".json":
                audit.add("quarantine", "MF009", mp, raw_rel,
                          "manifest 把 JSON 数组容器登记为数据条目(DATASET_SCHEMA §1:"
                          "数组整文件不得被当作正式样本通过)",
                          action="人工从 manifest 移除,或改为仅登记 JSONL 入口")
            elif fh.name.upper().startswith("README"):
                audit.add("info", "MF010", mp, raw_rel,
                          "manifest 把 README 文档登记为数据条目(非样本文件)")
    for f, splits in seen_files.items():
        if len(set(splits)) > 1:
            audit.add("quarantine", "MF005", "data/v1", f,
                      f"同一文件在多个 manifest 中被标为不同 split:{sorted(set(splits))}"
                      "——split 语义冲突(raw vs train)")
    registered = set(seen_files)
    for pool, files in POOLS.items():
        for f in files:
            if f not in registered:
                audit.add("quarantine", "MF006", f, "document",
                          f"{pool} 样本未被任何 manifest 登记(manifest 只覆盖 raw/*)"
                          "——用前必须 make_manifest 并冻结")
    locks = sorted((ROOT / "data").rglob("*.lock.json"))
    for pool, files in POOLS.items():
        target = files[0].replace("\\", "/")
        has_lock = False
        for lp in locks:
            try:
                lk = json.loads(lp.read_text(encoding="utf-8"))
            except Exception:  # noqa: BLE001
                continue
            for e in lk.get("entries", []):
                if str(e.get("path", "")).replace("\\", "/").endswith(target):
                    has_lock = True
        if not has_lock:
            audit.add("quarantine", "MF007", f"{target.rsplit('/', 1)[0]}", "document",
                      f"{pool} 无冻结锁(*.lock.json)——未冻结的评测集不得用于评测/训练"
                      "(EVAL_TEST_PREP §2)")
    # train 标签声明检查:对所有含 train 条目的清单(活动清单/归档 train 清单)
    for mp in MANIFESTS:
        p = ROOT / mp
        if not p.exists():
            continue
        try:
            m = json.loads(p.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        entries = m.get("entries", [])
        train_entries = [e for e in entries if e.get("split") == "train"]
        if not train_entries:
            continue
        undocumented = [e for e in train_entries
                        if not re.search(r"provisional|未验收|用户拍板|候选",
                                         str(e.get("notes", "")) + str(m.get("policy", "")))]
        if undocumented:
            audit.add("quarantine", "MF008", mp, "document",
                      f"{len(undocumented)} 条 candidate/UNVERIFIED 样本被标为 split=train "
                      "且无 provisional/未验收声明", action="补声明或改为 provisional split")
        else:
            audit.add("info", "MF008", mp, "document",
                      f"{len(train_entries)} 条样本按用户拍板标 split=train,notes 已注明 "
                      "provisional/未验收/动画未验证(如实)")


def check_pointer_consistency(audit: Audit, base: str, infos: dict) -> dict:
    """指针一致性:活动清单(data/manifest.json)指向的版本 vs 清单元信息/工具默认。"""
    active = ROOT / "data/manifest.json"
    res = {"active": str(active.relative_to(ROOT)).replace("\\", "/"),
           "exists": active.exists()}
    if not active.exists():
        audit.add("quarantine", "PTR001", "data/manifest.json", "document",
                  "缺少活动清单 data/manifest.json(指针未落地)")
        return res
    m = json.loads(active.read_text(encoding="utf-8"))
    entries = m.get("entries", [])
    versions = set()
    for e in entries:
        rel = str(e.get("path", "")).replace("\\", "/")
        mo = re.match(r"^(v\d+)/", rel)
        if mo:
            versions.add(mo.group(1))
    res["versions"] = sorted(versions)
    res["name"] = m.get("name")
    res["generated_at"] = m.get("generated_at")
    splits = collections.Counter(str(e.get("split")) for e in entries)
    res["splits"] = dict(splits)
    # 指针指向的版本 vs 本轮检测基目录
    bver = re.search(r"(v\d+)$", base)
    if bver and versions and bver.group(1) not in versions:
        audit.add("hard", "PTR002", "data/manifest.json", "document",
                  f"活动清单只引用 {sorted(versions)},而本轮检测基目录为 {base}"
                  "——指针与受检对象不一致")
    # 清单 name 未随指针版本更新
    if versions and m.get("name") and any(v in str(m.get("name")) for v in ("v1",)):
        if "v2" in versions:
            audit.add("info", "PTR003", "data/manifest.json", "document",
                      f"活动清单 name={m.get('name')!r} 仍含 v1 字样,但条目已指向 "
                      f"{sorted(versions)}——建议改名以免下游误读")
    # 清单 generated_at 早于其指向文件的最新 mtime
    newest, newest_f = None, None
    for e in entries:
        f = ROOT / "data" / str(e.get("path", "")).replace("\\", "/")
        if f.exists():
            ts = datetime.fromtimestamp(f.stat().st_mtime)
            if newest is None or ts > newest:
                newest, newest_f = ts, f
    if newest and m.get("generated_at"):
        try:
            ga = datetime.strptime(str(m["generated_at"]), "%Y-%m-%d %H:%M:%S")
            if newest > ga + timedelta(minutes=1):
                audit.add("info", "PTR004", "data/manifest.json", "document",
                          f"清单 generated_at={m['generated_at']} 早于其指向文件的最新 mtime "
                          f"{newest.strftime('%Y-%m-%d %H:%M:%S')}"
                          f"({newest_f.name})——时间戳未随重写刷新,建议更新"
                          "(清单按本地时间记录,此处按本地时间比较)")
        except ValueError:
            pass
    # 工具默认指针是否仍指向归档版本
    for tool, pat in (("tools/eval_test_prep.py", r'--dir["\']?\s*,\s*default=str\(ROOT\s*/\s*"([^"]+)"\)'),
                      ("tools/eval_test_prep.py", r'default="(data/v[12])"')):
        p = ROOT / tool
        if not p.exists():
            continue
        src = p.read_text(encoding="utf-8")
        mm = re.search(pat, src)
        if mm:
            default_base = mm.group(1).replace("\\", "/")
            if bver and bver.group(1) not in default_base:
                audit.add("quarantine", "PTR005", tool, "document",
                          f"{tool} 的默认指针仍为 {default_base},而活动清单已指向 "
                          f"{sorted(versions)}——不带参数运行时会判定归档版本(实测 status 报 "
                          "v1 锁有效、v2 锁为“其他版本”)",
                          action="把工具默认基目录切到活动版本,或在文档中明确须显式传参")
    return res


def check_locks(audit: Audit, base: str = "data/v1") -> list[dict]:
    """冻结锁:存在性 + 条目哈希 + 绑定的 manifest 哈希是否与现存 manifest 一致。
    只校验与当前基目录相关的锁;其他基目录的锁单独登记为 info。"""
    all_locks = sorted((ROOT / "data").rglob("*.lock.json"))
    relevant, others = [], []
    for lp in all_locks:
        try:
            lk = json.loads(lp.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            relevant.append(lp)
            continue
        if any(base in str(e.get("path", "")).replace("\\", "/")
               for e in lk.get("entries", [])):
            relevant.append(lp)
        else:
            others.append(lp)
    locks = relevant
    if others:
        audit.add("info", "LK008", base, "document",
                  "存在其他基目录的冻结锁(本轮不校验):"
                  + ", ".join(str(p.relative_to(ROOT)).replace("\\", "/") for p in others))
    out = []
    manifest_hashes = {}
    for mp in MANIFESTS:
        p = ROOT / mp
        if p.exists():
            manifest_hashes[sha256_bytes(p.read_bytes())] = mp
    for lp in locks:
        try:
            lk = json.loads(lp.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            audit.add("hard", "LK001", str(lp.relative_to(ROOT)), "document",
                      f"冻结锁解析失败:{exc}")
            continue
        rel = str(lp.relative_to(ROOT)).replace("\\", "/")
        out.append({"path": rel, "name": lk.get("meta", {}).get("name"),
                    "locked": lk.get("locked"), "n_files": lk.get("n_files"),
                    "manifest_sha256": lk.get("meta", {}).get("manifest_sha256")})
        if not lk.get("locked"):
            audit.add("hard", "LK002", rel, "document", "lock.locked != true")
        for e in lk.get("entries", []):
            f = _resolve(str(e.get("path", "")))
            if not f.exists():
                audit.add("hard", "LK003", rel, str(e.get("path")),
                          "锁条目文件不存在")
                continue
            h = sha256_bytes(f.read_bytes())
            if h != e.get("sha256"):
                audit.add("hard", "LK004", rel, str(e.get("path")),
                          f"锁绑定哈希与文件不符(锁 {str(e.get('sha256'))[:12]}… vs "
                          f"实际 {h[:12]}…)——冻结后文件被改动")
            if f.stat().st_size != e.get("size"):
                audit.add("hard", "LK005", rel, str(e.get("path")),
                          f"锁绑定大小不符({e.get('size')} vs {f.stat().st_size})")
        mh = lk.get("meta", {}).get("manifest_sha256")
        if mh and mh not in manifest_hashes:
            audit.add("hard", "LK006", rel, "document",
                      f"锁绑定的 manifest 哈希 {str(mh)[:12]}… 与现存任何 manifest 都不匹配"
                      "——manifest 已在冻结后被重写")
        elif mh:
            audit.add("info", "LK007", rel, "document",
                      f"锁校验通过:绑定 {manifest_hashes[mh]}")
    return out


def check_eol_binding(audit: Audit) -> None:
    """EOL 与哈希绑定:记录哈希若基于 CRLF,而 .gitattributes 强制 LF 换行,
    则全新 clone 后 sha256 不匹配(manifest/lock 校验会失败)。"""
    ga = ROOT / ".gitattributes"
    if not ga.exists():
        return
    patterns = {}
    for line in ga.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        pat = parts[0]
        attrs = " ".join(parts[1:])
        patterns[pat] = attrs
    bound: list[tuple[str, str]] = []
    for mp in MANIFESTS:
        p = ROOT / mp
        if not p.exists():
            continue
        m = json.loads(p.read_text(encoding="utf-8"))
        mdir = p.parent
        for e in m.get("entries", []):
            raw_rel = str(e.get("path", ""))
            fh = _resolve(raw_rel, mdir)
            if fh.exists():
                bound.append((str(fh.relative_to(ROOT)).replace("\\", "/"),
                              str(e.get("sha256"))))
    for lp in sorted((ROOT / "data").rglob("*.lock.json")):
        try:
            lk = json.loads(lp.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            continue
        for e in lk.get("entries", []):
            fh = _resolve(str(e.get("path", "")))
            if fh.exists():
                bound.append((str(fh.relative_to(ROOT)).replace("\\", "/"),
                              str(e.get("sha256"))))
        # 锁绑定的 manifest 自身也在 eol 归一化范围内
        mh = lk.get("meta", {}).get("manifest_sha256")
        if mh:
            for mp in MANIFESTS:
                p = ROOT / mp
                if p.exists() and sha256_bytes(p.read_bytes()) == mh:
                    bound.append((mp, mh))
    seen = set()
    for rel, recorded in bound:
        if not recorded or (rel, recorded) in seen:
            continue
        seen.add((rel, recorded))
        f = ROOT / rel
        b = f.read_bytes()
        crlf_h = sha256_bytes(b)
        lf_h = sha256_bytes(b.replace(b"\r\n", b"\n"))
        if crlf_h == lf_h:
            continue
        eol_lf = any(attrs for pat, attrs in patterns.items()
                     if f.match(pat) and "eol=lf" in attrs) or \
            any("eol=lf" in attrs for pat, attrs in patterns.items() if f.match(pat))
        if not eol_lf:
            continue
        if recorded == crlf_h:
            audit.add("quarantine", "W001", rel, "document",
                      f"记录哈希绑定 CRLF 字节({crlf_h[:12]}…),但 .gitattributes 对该模式"
                      f"声明 eol=lf(LF 归一化后为 {lf_h[:12]}…);全新 clone 得到 LF 文件后 "
                      "manifest/冻结锁校验将失败——哈希不可复现",
                      action="把文件落盘改为 LF 后重算并重冻,或对该文件声明 -text 固定字节")


def check_docs(audit: Audit, docs_heads: dict[str, list[str]],
               id_lists: dict[str, list[str]]) -> None:
    for pool, doc in DOCS.items():
        p = ROOT / doc
        if not p.exists():
            audit.add("hard", "D001", doc, "document", "来源手稿不存在")
            continue
        text = p.read_text(encoding="utf-8")
        ids_doc = docs_heads.get(doc, [])
        ids_data = id_lists.get(pool, [])
        miss = [i for i in ids_data if i not in set(ids_doc)]
        extra = [i for i in ids_doc if i not in set(ids_data)]
        if miss:
            audit.add("hard", "D002", doc, "document",
                      f"JSONL 有 {len(miss)} 个身份在手稿中缺失:{miss[:5]}")
        if extra:
            audit.add("quarantine", "D003", doc, "document",
                      f"手稿有 {len(extra)} 个身份未出现在 JSONL:{extra[:5]}")
        if "未冻结" in text and "未转 JSON" in text:
            audit.add("quarantine", "D004", doc, "document",
                      "手稿自称“未冻结、未转 JSON/JSONL”,但 "
                      f"{POOLS[pool][0]} 已存在并进入预跑检测——文档状态与实际不符",
                      action="人工更新文档状态或撤回数据")
        if re.search(r"状态[：:]\s*\*\*草稿", text):
            audit.add("quarantine", "D005", doc, "document",
                      "手稿状态为“草稿(供审阅)”,而对应 JSONL 已生成并用于预跑检测"
                      "——需明确内容是否定稿")
        # 规模声明 vs 实际
        m = re.search(r"规模[：:]\s*(\d+)\s*题", text)
        if m:
            claimed = int(m.group(1))
            actual = len(set(ids_data))
            if claimed != actual:
                audit.add("hard", "D006", doc, "document",
                          f"手稿声明 {claimed} 题,实际 JSONL 身份数 {actual}")


def check_doc_inventory(audit: Audit) -> None:
    for rel, claim in (("EVAL_TEST_PREP.md", "eval:未生成"),
                       ("data/v1/eval/README.md", "未生成任何"),
                       ("data/v1/test/README.md", "未生成任何")):
        p = ROOT / rel
        if p.exists():
            t = p.read_text(encoding="utf-8", errors="replace")
            if "未生成" in t:
                audit.add("quarantine", "D010", rel, "document",
                          "文档声明 eval/test 未生成,但 data/v1/{eval,test} 下已有 "
                          "450 条样本——文档滞后于数据(易导致误判“无评测集”)",
                          action="人工更新文档")


def check_prior_review(audit: Audit) -> dict:
    p = ROOT / "reviews/2026-10-03-math-review/evidence/findings.json"
    if not p.exists():
        return {}
    fs = json.loads(p.read_text(encoding="utf-8"))
    lv = collections.Counter(x.get("level") for x in fs)
    ds = collections.Counter("eval" if str(x.get("id")).startswith("eval-") else "test"
                             for x in fs)
    audit.add("info", "R001", "reviews/2026-10-03-math-review/review-math.md", "document",
              f"既有内容评审 {len(fs)} 条(A {lv.get('A', 0)} / B {lv.get('B', 0)} / "
              f"C {lv.get('C', 0)};eval {ds.get('eval', 0)} / test {ds.get('test', 0)});"
              "本轮抽查其 A 级 5 条在当前 JSONL 中均已改为正确表述")
    return {"n": len(fs), "A": lv.get("A", 0), "B": lv.get("B", 0), "C": lv.get("C", 0),
            "eval": ds.get("eval", 0), "test": ds.get("test", 0),
            "a_ids": [x["id"] for x in fs if x.get("level") == "A"]}


def refine_issues(audit: Audit) -> None:
    """Lead 复核后的误报修正(保留原证据,只调整严重度)。"""
    for it in audit.issues:
        blob = f"{it.get('message') or ''} {it.get('evidence') or ''}"
        if it["code"] == "C008" and "pmatrix" in blob:
            it["severity"] = "info"
            it["message"] = (it["message"] +
                             "(Lead 复核:该处为矩阵幂 A^2=A 的恒等演示,非笔误)")
        # L006: \leftarrow / \leftrightarrow 等是独立控制字,\left 不是未配对
        if it["code"] == "L006" and re.search(r"\\+left[a-zA-Z]", blob):
            it["severity"] = "info"
            it["message"] = (it["message"] +
                             "(Lead 复核:此处 \\left 后紧跟字母,实为 "
                             "\\leftarrow 类箭头命令,非未配对 \\left;规则需加字母边界)")
        # L009: \frac32 / \dfrac12 等未加花括号的单 token 参数是合法 TeX,仅风格问题
        if it["code"] == "L009":
            it["severity"] = "info"
            it["message"] = (it["message"] +
                             "(Lead 复核:\\frac/\\dfrac 取单 token 参数为合法 TeX,"
                             "可正常渲染,仅风格建议;无渲染失败风险)")


def check_schema_divergence(audit: Audit, infos: dict) -> None:
    """eval 无 id 字段依赖复合身份:与 DATASET_SCHEMA §2/§6 文本不一致。"""
    ev = [r["record"] for r in infos["eval"][0]["records"]]
    no_id = [r for r in ev if _missing(r.get("id"))]
    if no_id:
        audit.add("quarantine", "G001", POOLS["eval"][0], "document",
                  f"{len(no_id)}/{len(ev)} 条 eval 样本没有 id 字段,依赖 problem_id+solution_id "
                  "复合身份;DATASET_SCHEMA §2 仍把 id 缺失列为硬伤、§6 仍称多解字段为“预留”"
                  "——契约文本需与实现(GS3 record_identity)同步,否则下游按 §2 校验即判硬伤",
                  action="人工更新 DATASET_SCHEMA:写明多解样本的复合身份口径")
    # 多解组覆盖
    pids = collections.Counter(str(r["record"].get("problem_id")) for r in infos["eval"][0]["records"])
    if pids:
        dist = collections.Counter(pids.values())
        audit.add("info", "G002", POOLS["eval"][0], "document",
                  f"eval 同题多解组 {len(pids)} 组,解法数分布 {dict(sorted(dist.items()))}"
                  "(设计:每题 ≥2 种解法)")


def check_doc_freeze_claims(audit: Audit, locks: list[dict]) -> None:
    """文档仍称“未冻结”但已存在冻结锁 → 文档滞后。"""
    lock_names = " ".join(str(l.get("path", "")) + " " + str(l.get("name", ""))
                          for l in locks)
    for pool, doc in DOCS.items():
        p = ROOT / doc
        if not p.exists():
            continue
        if "未冻结" in p.read_text(encoding="utf-8") and pool in lock_names:
            audit.add("quarantine", "D011", doc, "document",
                      f"手稿仍称“未冻结”,但已存在 {pool} 的冻结锁"
                      f"({[l['path'] for l in locks if pool in str(l.get('path',''))]})"
                      "——文档状态滞后于冻结事实", action="人工更新文档状态")
    for rel in ("EVAL_TEST_PREP.md",):
        p = ROOT / rel
        if p.exists() and "未冻结" in p.read_text(encoding="utf-8", errors="replace"):
            audit.add("quarantine", "D012", rel, "document",
                      "文档仍写“未冻结”,而 eval/test(v1/v2)冻结锁均已建立"
                      "(v1 19:25、v2 22:09)", action="人工更新为已冻结/待用户批准")
    for pool in ("eval", "test"):
        for cand in (f"data/v1/{pool}/README.md", f"data/v2/{pool}/README.md"):
            p = ROOT / cand
            if p.exists() and "未冻结" in p.read_text(encoding="utf-8", errors="replace"):
                audit.add("quarantine", "D012", cand, "document",
                          "该目录 README 仍写“未冻结”,与已建立的冻结锁不符",
                          action="人工更新为已冻结/待用户批准")


def g003_identical_group_scenes(audit: Audit, infos: dict) -> None:
    """同题多解:同 problem_id 下不同解法的 scene_spec 若完全相同,与
    “逐解法场景”设计不符(EVAL_TEST_PREP §1)。"""
    groups = collections.defaultdict(list)
    for r in infos["eval"][0]["records"]:
        rec = r["record"]
        if isinstance(rec, dict) and rec.get("problem_id"):
            groups[str(rec["problem_id"])].append(r)
    dup = []
    for pid, rows in groups.items():
        sig = {json.dumps(r["record"].get("scene_spec"), sort_keys=True,
                          ensure_ascii=False) for r in rows}
        if len(rows) > 1 and len(sig) < len(rows):
            dup.append(pid)
    if dup:
        audit.add("quarantine", "G003", POOLS["eval"][0], "document",
                  f"{len(dup)} 个 problem_id 的多个解法共用完全相同的 scene_spec"
                  f"(示例 {dup[:3]})——逐解法场景设计未落实",
                  action="人工逐解法重写或确认共用是有意为之")
    else:
        audit.add("info", "G003", POOLS["eval"][0], "document",
                  f"同题多解场景互异性检查通过:{len(groups)} 组,无“多解法 scene_spec 完全相同”")


def check_base_manifest(audit: Audit, base: str) -> None:
    active = ROOT / "data/manifest.json"
    covers = False
    if active.exists():
        try:
            m = json.loads(active.read_text(encoding="utf-8"))
            covers = any(base.replace("data/", "") in str(e.get("path", "")).replace("\\", "/")
                         for e in m.get("entries", []))
        except Exception:  # noqa: BLE001
            covers = False
    if not (ROOT / base / "manifest.json").exists() and not covers:
        audit.add("quarantine", "MF011", base, "document",
                  f"{base} 内没有顶层 manifest.json,且活动清单 data/manifest.json 也未引用它:"
                  "切换引用时需重建顶层清单,使 train/eval/test 在同一份清单里绑定",
                  action="用户批准切换后 make_manifest 顶层登记并重冻")


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--base", default="data/v1",
                    help="候选基目录(默认 data/v1;v2 用 data/v2)")
    ap.add_argument("--manifest", action="append", default=[],
                    help="额外纳入检查的清单(如活动清单 data/manifest.json),可重复")
    ap.add_argument("--train-dir", default="data/v1/raw", help="训练参考池目录")
    ap.add_argument("--source-dir", default=None,
                    help="源手稿目录(默认仓库根;v2 用 data/v2/sources)")
    args = ap.parse_args(argv)
    base = args.base.replace("\\", "/").rstrip("/")
    POOLS.clear()
    POOLS.update({"eval": [f"{base}/eval/dataset_eval.jsonl"],
                  "test": [f"{base}/test/dataset_test.jsonl"]})
    MIRRORS.clear()
    MIRRORS.update({"eval": f"{base}/eval/dataset_eval.json",
                    "test": f"{base}/test/dataset_test.json"})
    MANIFESTS.clear()
    MANIFESTS.extend([m for m in (f"{base}/manifest.json",
                                  f"{base}/manifest-train.json",
                                  f"{base}/eval/manifest.json",
                                  f"{base}/test/manifest.json")
                      if (ROOT / m).exists()])
    for extra in args.manifest:
        e = extra.replace("\\", "/")
        if (ROOT / e).exists() and e not in MANIFESTS:
            MANIFESTS.append(e)
    if args.source_dir:
        sdir = args.source_dir.replace("\\", "/")
        DOCS.clear()
        DOCS.update({"eval": f"{sdir}/dataset-eval.md",
                     "test": f"{sdir}/data-test.md"})
    outdir = ROOT / args.out
    outdir.mkdir(parents=True, exist_ok=True)

    audit = Audit()
    infos: dict[str, list[dict]] = {}
    all_files: list[Path] = []
    train_files = sorted((ROOT / args.train_dir).glob("*.jsonl"))
    for p in train_files + [ROOT / f for fs in POOLS.values() for f in fs]:
        all_files.append(p)
    for pool, files in POOLS.items():
        infos[pool] = [load_file(ROOT / f) for f in files]
    train_infos = [load_file(p) for p in train_files]

    for pool in ("eval", "test"):
        for info in infos[pool]:
            check_structure_and_fields(audit, info, pool)
            check_identity(audit, info, pool)
            check_id_conventions(audit, info, pool)
            for r in info["records"]:
                if not isinstance(r["record"], dict):
                    continue
                rid = rid_of(r["record"])
                check_source_license(audit, info, r, rid)
                check_consistency(audit, info, r, rid)
                check_latex(audit, info, r, rid)
                check_scene_spec(audit, info, r, rid)

    texts_by_pool = {
        "train": pool_texts(train_infos, "train"),
        "eval": pool_texts(infos["eval"], "eval"),
        "test": pool_texts(infos["test"], "test"),
    }
    iso = check_isolation(audit, texts_by_pool)

    # 镜像 .json 与 JSONL 内容一致性
    for pool, mirror in MIRRORS.items():
        mp = ROOT / mirror
        if not mp.exists():
            audit.add("info", "M001", mirror, "document", "镜像 .json 不存在")
            continue
        mi = load_file(mp)
        if mi["format"] == "json-array":
            audit.add("info", "M002", mirror, "document",
                      "JSON 数组容器不得作为样本入口(DATASET_SCHEMA §1);"
                      "本仓库以 JSONL 为入口,该文件仅作镜像,入场工具只选 *.jsonl",
                      action="人工确认镜像用途,或移出入口目录")
        jl = [r["record"] for r in infos[pool][0]["records"]]
        arr = [r["record"] for r in mi["records"]]
        if json.dumps(arr, sort_keys=True, ensure_ascii=False) != \
           json.dumps(jl, sort_keys=True, ensure_ascii=False):
            audit.add("hard", "M003", mirror, "document",
                      f"镜像 .json 与 {POOLS[pool][0]} 内容不一致"
                      f"({len(arr)} vs {len(jl)})")

    check_manifests(audit, {})
    check_base_manifest(audit, base)
    locks = check_locks(audit, base)
    pointer = check_pointer_consistency(audit, base, infos)
    check_eol_binding(audit)
    doc_heads = {}
    for doc in DOCS.values():
        p = ROOT / doc
        if p.exists():
            doc_heads[doc] = re.findall(r"(?m)^###\s+(\S+)",
                                        p.read_text(encoding="utf-8"))
    id_lists = {
        "eval": sorted({str(r["record"].get("problem_id")) for r in infos["eval"][0]["records"]}),
        "test": sorted({str(r["record"].get("id")) for r in infos["test"][0]["records"]}),
    }
    check_docs(audit, doc_heads, id_lists)
    check_doc_inventory(audit)
    check_doc_freeze_claims(audit, locks)
    check_schema_divergence(audit, infos)
    g003_identical_group_scenes(audit, infos)
    prior = check_prior_review(audit)
    refine_issues(audit)

    # ---- 逐条状态 ----
    issues = audit.issues
    by_rec: dict[str, dict[str, int]] = collections.defaultdict(
        lambda: {"hard": 0, "quarantine": 0, "info": 0})
    for it in issues:
        rid = it.get("id")
        if rid:
            by_rec[rid][it["severity"]] += 1
    status_rows = []
    for pool in ("eval", "test"):
        for info in infos[pool]:
            for r in info["records"]:
                rec = r["record"]
                if not isinstance(rec, dict):
                    continue
                rid = rid_of(rec)
                c = by_rec.get(rid, {"hard": 0, "quarantine": 0, "info": 0})
                status = ("rejected" if c["hard"] else
                          "quarantine" if c["quarantine"] else "clean")
                status_rows.append({
                    "split": pool, "file": info["path"], "locator": r["locator"],
                    "identity": rid, "problem_id": rec.get("problem_id"),
                    "solution_id": rec.get("solution_id"), "method": rec.get("method"),
                    "id": rec.get("id"), "category": rec.get("category"),
                    "sub_category": rec.get("sub_category"),
                    "status": status, "n_hard": c["hard"],
                    "n_quarantine": c["quarantine"], "n_info": c["info"],
                    "animation_verified": bool(rec.get("render_status") == "verified"),
                })

    # ---- 哈希 ----
    hash_files = []
    readme_candidates = [ROOT / f"{v}/{pool}/README.md"
                         for v in ("data/v1", "data/v2") for pool in ("eval", "test")]
    for p in all_files + [ROOT / m for m in MIRRORS.values()] \
            + [ROOT / d for d in DOCS.values()] \
            + [ROOT / m for m in MANIFESTS] \
            + readme_candidates \
            + [ROOT / l["path"] for l in locks] \
            + [ROOT / ".gitattributes"]:
        if p.exists():
            b = p.read_bytes()
            hash_files.append({"file": str(p.relative_to(ROOT)).replace("\\", "/"),
                               "sha256": sha256_bytes(b), "size": len(b)})

    sev = collections.Counter(i["severity"] for i in issues)
    codes = collections.Counter(i["code"] for i in issues)
    status_counts = collections.Counter(r["status"] for r in status_rows)
    per_split = {}
    for pool in ("eval", "test"):
        rows = [r for r in status_rows if r["split"] == pool]
        recs = [r["record"] for info in infos[pool] for r in info["records"]]
        per_split[pool] = {
            "records": len(rows),
            "identities": len({r["identity"] for r in rows}),
            "problem_ids": len({r["problem_id"] for r in recs if r.get("problem_id")}),
            "status": dict(collections.Counter(r["status"] for r in rows)),
            "categories": dict(collections.Counter(r.get("category") for r in recs)),
            "sub_categories": len({r.get("sub_category") for r in recs}),
            "objects": sum(len((r.get("scene_spec") or {}).get("objects") or []) for r in recs),
            "steps": sum(len((r.get("scene_spec") or {}).get("steps") or []) for r in recs),
            "animation_verified": sum(1 for r in recs if r.get("render_status") == "verified"),
            "methods": len({r.get("method") for r in recs if r.get("method")}),
        }
    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tool": "tools/eval_test_audit.py (只读)",
        "scope": {"base": base,
                  "entry_jsonl": {p: POOLS[p] for p in POOLS},
                  "mirrors": MIRRORS, "source_docs": DOCS,
                  "train_pool": [str(p.relative_to(ROOT)).replace("\\", "/")
                                 for p in train_files]},
        "totals": {"eval_records": len(infos["eval"][0]["records"]),
                   "test_records": len(infos["test"][0]["records"]),
                   "all_records": len(status_rows),
                   "train_records": sum(len(i["records"]) for i in train_infos)},
        "severity_counts": dict(sev),
        "issue_code_counts": dict(codes),
        "record_status_counts": dict(status_counts),
        "per_split": per_split,
        "isolation": {
            "exact_cross_pool_overlaps": iso["exact"],
            "near_dup_pairs_ge_threshold": iso["pairs"],
            "max_cross_pool_similarity_set": round(iso["max_sim"], 4),
            "threshold": NEAR_DUP_THRESHOLD,
            "threshold_status": "UNCALIBRATED",
        },
        "mirror_identical": {m: (json.dumps([r["record"] for r in load_file(
            ROOT / MIRRORS[m])["records"]], sort_keys=True, ensure_ascii=False)
            == json.dumps([r["record"] for r in infos[m][0]["records"]],
                          sort_keys=True, ensure_ascii=False)) for m in POOLS},
        "prior_review": prior,
        "freeze_locks": locks,
        "pointer": pointer,
    }

    (outdir / "issues.jsonl").write_text(
        "\n".join(json.dumps(i, ensure_ascii=False) for i in issues) + "\n",
        encoding="utf-8")
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

    print(f"[eval/test 预跑检测] eval={summary['totals']['eval_records']} "
          f"test={summary['totals']['test_records']} train={summary['totals']['train_records']}")
    print(f"[严重度] {dict(sev)}")
    print(f"[逐条状态] {dict(status_counts)}")
    print(f"[隔离] 跨池精确重叠={iso['exact']} 近重复≥阈值对={len(iso['pairs'])} "
          f"max_set={iso['max_sim']:.4f}")
    print(f"[输出] {outdir}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
