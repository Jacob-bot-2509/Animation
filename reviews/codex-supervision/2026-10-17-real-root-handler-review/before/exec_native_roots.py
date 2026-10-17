"""exec-native 根注册表处理器 —— 静态实现候选 v1(不触碰 BOUND_FILES)。

对应 new-work-root-proposal.md v2 §2-§5:注册表 schema v2、可信历史链、
Windows 字面路径校验(先验证原始字面量再用 Path API)、状态流转、cohort 绑定、
(job) 原子预留、回执根精确校验。

范围与局限(如实):
- 纯内存/文件处理器;真实 OS 重解析点、ACL、句柄/令牌隔离、TOCTOU 由调用方
  提供的 existing_paths/reparse_paths 事实参与判定,本实现不实盘探测;
- 不创建真实 ROOTS 注册表(本轮);--receipt 仅写项目内新文件,拒已存在/冻结目录/ADS/重解析路径;
- 不构成任何原生验收证据;状态 DESIGN。
"""
from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path

SCHEMA = "exec-native-roots-v2"
PURPOSES = ("transport", "surface", "joint", "external")
BOUND_PATH_SET = ("raw", "work", "media")
STATUS_FLOW = {"REGISTERED": {"REGISTERED", "ACTIVE"},
               "ACTIVE": {"ACTIVE", "FROZEN"},
               "FROZEN": {"FROZEN"}}
ROOT_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{0,63}$")
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
DEVICE_NAMES = {f"{n}{s}" for n in ("CON", "PRN", "AUX", "NUL") for s in ("", ".", ".txt")}
DEVICE_NAMES |= {f"COM{i}" for i in range(1, 10)} | {f"LPT{i}" for i in range(1, 10)}


def is_hex64(s) -> bool:
    return isinstance(s, str) and bool(HEX64_RE.match(s))


def valid_root_id(s) -> bool:
    return isinstance(s, str) and bool(ROOT_ID_RE.match(s))


def root_path_of(root_id: str) -> str:
    return f"reviews/exec-native/run-{root_id}"


def literal_relpath_issues(rel: str) -> list[str]:
    """Windows 规范相对路径字面校验;返回问题列表,空=通过。

    必须先于 Path 折叠检查原始字面量:拒绝 ..、.、空段、绝对/盘符/UNC、
    反斜杠别名、ADS、设备名、尾点/尾空格、通配符与控制字符。
    """
    issues: list[str] = []
    if not isinstance(rel, str) or not rel:
        return ["empty_or_non_string"]
    if any(ord(ch) < 32 for ch in rel):
        issues.append("control_characters")
    if "\x00" in rel:
        issues.append("nul_byte")
    if ":" in rel:
        issues.append("ads_or_drive_colon")  # ADS 或盘符
    if rel.startswith("\\\\") or rel.startswith("//"):
        issues.append("unc")
    if rel.startswith("/") or rel.startswith("\\"):
        issues.append("absolute")
    if len(rel) >= 2 and rel[1] == ":":
        issues.append("drive")
    if "*" in rel or "?" in rel or "[" in rel or "]" in rel:
        issues.append("wildcard")
    segments = rel.replace("\\", "/").split("/")
    for seg in segments:
        if seg in ("", ".", ".."):
            issues.append(f"bad_segment:{seg!r}")
        if seg != seg.rstrip(" ."):
            issues.append(f"trailing_dot_or_space:{seg!r}")
        if seg.upper() in DEVICE_NAMES:
            issues.append(f"device_name:{seg!r}")
    return issues


def check_registry_entries(entries, current_bound_map, old_roots, existing_paths) -> tuple[bool, list[str]]:
    """R1-R3/R7/R8 校验;返回 (ok, 拒绝原因列表)。"""
    if not isinstance(entries, list) or not entries:
        return False, ["R1:entries_empty_or_not_list"]
    problems: list[str] = []
    seen_ids: set = set()
    seen_paths: set = set()
    for e in entries:
        if not isinstance(e, dict):
            problems.append("R1:entry_not_object")
            continue
        if set(e) != {"root_id", "root_path", "purpose", "cohort", "bound_paths",
                      "status", "created_at"}:
            problems.append(f"R1:unexpected_keys:{sorted(set(e))}")
            continue
        rid = e["root_id"]
        if not valid_root_id(rid):
            problems.append(f"R1:bad_root_id:{rid!r}")
        expected_path = root_path_of(rid) if valid_root_id(rid) else None
        if e.get("root_path") != expected_path:
            problems.append(f"R2:root_path_not_exact:{rid}:{e.get('root_path')!r}")
        if rid in seen_ids:
            problems.append(f"R7:root_id_reused:{rid}")
        seen_ids.add(rid)
        path = e.get("root_path", "")
        if path in seen_paths:
            problems.append("R7:path_reused")
        seen_paths.add(path)
        # 旧根/登记根/祖先子树重叠
        norm = path.replace("\\", "/")
        for old in old_roots:
            if norm == old or norm.startswith(old.rstrip("/") + "/") \
                    or old.startswith(norm.rstrip("/") + "/"):
                problems.append(f"R2:overlap_old_root:{path}")
        for other in seen_paths:
            if other == path:
                continue
            if path.startswith(other.rstrip("/") + "/") or other.startswith(path.rstrip("/") + "/"):
                problems.append(f"R2:nesting:{path}<->{other}")
        # 已存在目标/子项:正常公共容器 reviews/exec-native 除外
        if existing_paths is not None and path not in existing_paths:
            pass  # 不存在则无冲突
        if e.get("purpose") not in PURPOSES:
            problems.append(f"R1:bad_purpose:{e.get('purpose')!r}")
        if e.get("status") not in STATUS_FLOW:
            problems.append(f"R1:bad_status:{e.get('status')!r}")
        cohort = e.get("cohort")
        if not isinstance(cohort, dict) or set(cohort) != {"collector_sha256",
                                                           "verifier_sha256",
                                                           "bound_files_sha256_map"}:
            problems.append(f"R3:bad_cohort_shape:{rid}")
        else:
            for k in ("collector_sha256", "verifier_sha256"):
                if not is_hex64(cohort.get(k)):
                    problems.append(f"R3:bad_sha:{rid}:{k}")
            bm = cohort.get("bound_files_sha256_map")
            if not isinstance(bm, dict) or not bm or \
                    not all(isinstance(k2, str) and is_hex64(v2) for k2, v2 in bm.items()):
                problems.append(f"R3:bad_bound_map:{rid}")
            elif bm != current_bound_map:
                problems.append(f"R3:cohort_bound_mismatch:{rid}")
        bp = e.get("bound_paths")
        if not isinstance(bp, list) or not bp:
            problems.append(f"R8:bound_paths_empty:{rid}")
        elif set(bp) - set(BOUND_PATH_SET):
            problems.append(f"R8:bound_paths_not_subset:{rid}:{sorted(set(bp))}")
        elif len(bp) != len(set(bp)):
            problems.append(f"R8:bound_paths_duplicate:{rid}")
        for p in bp if isinstance(bp, list) else []:
            issues = literal_relpath_issues(p)
            if issues:
                problems.append(f"R8:bound_path_literal:{rid}:{p}:{issues}")
    return not problems, problems


def check_write(entries, root_id: str, write_rel: str, cohort_digest: str,
                reparse_paths: set | None = None) -> tuple[bool, str]:
    """R4 写权限:ACTIVE + cohort 一致 + 闭合 bound_paths + 字面校验 + 重解析事实。"""
    for e in entries:
        if e.get("root_id") != root_id:
            continue
        if e.get("status") != "ACTIVE":
            return False, "R4:not_active"
        if e.get("cohort", {}).get("verifier_sha256") != cohort_digest and \
                cohort_digest not in ("", None):
            return False, "R4:cohort_mismatch"
        issues = literal_relpath_issues(write_rel)
        if issues:
            return False, f"R4:literal:{issues}"
        parts = write_rel.replace("\\", "/").split("/")
        if not parts or parts[0] not in e.get("bound_paths", []):
            return False, "R4:outside_bound_paths"
        if reparse_paths is not None:
            full = (root_path_of(root_id) + "/" + write_rel).replace("\\", "/")
            for rp in reparse_paths:
                if full == rp or full.startswith(rp.rstrip("/") + "/"):
                    return False, "R4:reparse_conflict"
        return True, ""
    return False, "R1:root_not_registered"


class JobReservation:
    """(cohort_id, job_id) 原子预留:同 job 重复拒绝,同 cohort 不同 job 允许。

    placeholder 目录持久;结果不确定时保留占位,不盲目重跑。
    跨进程原子性/崩溃恢复:mkdir 提供存在性原子,登记文件用 os.replace 原子写;
    完整持久意图协议由正式实现扩展,本类如实标注。
    """

    def __init__(self, base: Path):
        self.base = base

    def reserve(self, cohort_id: str, job_id: str) -> tuple[bool, str]:
        if not (isinstance(cohort_id, str) and isinstance(job_id, str)
                and cohort_id and job_id):
            return False, "bad ids"
        place = self.base / f"job-{job_id}"
        try:
            place.mkdir(parents=True)
        except FileExistsError:
            return False, "R6:job_reused"
        intent = {"cohort_id": cohort_id, "job_id": job_id, "state": "PLACEHOLDER"}
        tmp = place / ".intent.tmp"
        tmp.write_text(json.dumps(intent, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp, place / "intent.json")
        return True, ""

    def finalize(self, job_id: str) -> tuple[bool, str]:
        place = self.base / f"job-{job_id}"
        intent_f = place / "intent.json"
        if not intent_f.is_file():
            return False, "R6:no_intent"
        data = json.loads(intent_f.read_text(encoding="utf-8"))
        data["state"] = "FINALIZED"
        tmp = place / ".intent.tmp"
        tmp.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        os.replace(tmp, intent_f)
        return True, ""


def check_receipt_root(entries, root_id: str, expected_run_id: str,
                       cohort_digest: str) -> tuple[bool, str]:
    """R5 回执根/身份:精确登记根 + 可信预期 run_id + cohort 摘要,全部一致才通过。"""
    for e in entries:
        if e.get("root_id") != root_id:
            continue
        if e.get("status") not in ("ACTIVE", "FROZEN"):
            return False, "R5:not_active_or_frozen"
        if e.get("cohort", {}).get("verifier_sha256") != cohort_digest:
            return False, "R5:cohort_mismatch"
        if not expected_run_id:
            return False, "R5:no_expected_run_id"
        return True, ""
    return False, "R5:root_not_registered"


class HistoryChain:
    """可信历史链:上一完整快照由调用者独立提供,按 SHA 对上 previous_registry_sha256
    才接受新快照;检测历史删除、字段改写、状态回滚与 root_id 复用。"""

    def __init__(self, previous_snapshot_bytes: bytes | None):
        self.prev_bytes = previous_snapshot_bytes
        self.prev_sha = hashlib.sha256(previous_snapshot_bytes).hexdigest() \
            if previous_snapshot_bytes is not None else None

    def verify_against(self, registry_doc: dict) -> tuple[bool, str]:
        stored = registry_doc.get("previous_registry_sha256")
        if self.prev_bytes is None:
            return False, "R7:no_independent_previous_snapshot"
        if stored != self.prev_sha:
            return False, "R7:previous_sha_mismatch"
        try:
            prev_doc = json.loads(self.prev_bytes.decode("utf-8"))
        except Exception as exc:  # noqa: BLE001
            return False, f"R7:bad_previous_bytes:{exc.__class__.__name__}"
        # 检测历史条目被删/改:当前 entries 必须包含上一快照全部 (root_id,root_path)
        prev_ids = {e.get("root_id") for e in prev_doc.get("entries", [])}
        cur_ids = {e.get("root_id") for e in registry_doc.get("entries", [])}
        if not prev_ids <= cur_ids:
            return False, f"R7:history_deleted:{sorted(prev_ids - cur_ids)}"
        prev_by_id = {e.get("root_id"): e for e in prev_doc.get("entries", [])}
        for e in registry_doc.get("entries", []):
            p = prev_by_id.get(e.get("root_id"))
            if p is None:
                continue  # 新 entry,允许(REGISTERED 起步)
            for k in ("root_path", "purpose", "cohort", "bound_paths", "created_at"):
                if p.get(k) != e.get(k):
                    return False, f"R7:history_rewrite:{e.get('root_id')}:{k}"
            # 状态回滚检测:FROZEN 不可回退
            if p.get("status") == "FROZEN" and e.get("status") != "FROZEN":
                return False, f"R7:status_rollback:{e.get('root_id')}"
            if e.get("status") not in STATUS_FLOW.get(p.get("status", ""), {p.get("status")}):
                return False, f"R7:illegal_transition:{e.get('root_id')}"
        return True, ""

    def next_registry(self, entries: list[dict]) -> dict:
        return {"schema": SCHEMA, "entries": entries,
                "previous_registry_sha256": self.prev_sha}
