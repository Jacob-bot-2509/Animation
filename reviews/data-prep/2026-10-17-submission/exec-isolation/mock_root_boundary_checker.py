"""根注册表拒绝矩阵 mock 校验器(fixture-only,不建真实根、不跑原生探针)。

对应 new-work-root-proposal.md §3 的 R1-R8。每场景真实 assert,失败退出非零。
本文件只证明拒绝规则逻辑,不构成任何原生验收证据。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

OLD_ROOTS = {
    "reviews/codex-supervision/2026-10-05-three-gates",
    "reviews/codex-supervision/2026-10-06-all43-sandbox-repair",
    "reviews/2026-10-06-exec-isolation-full-surface",
}
NEW_ROOT_PREFIX = "reviews/exec-native/"


def valid_registry() -> dict:
    return {"schema": "exec-native-roots-v1", "entries": [
        {"root_id": "n001", "root_path": "reviews/exec-native/run-n001",
         "purpose": "surface", "cohort": {"collector_sha256": "a" * 64,
         "verifier_sha256": "b" * 64, "bound_files_sha256_map": {"k": "v"}},
         "bound_paths": ["raw", "work", "media"], "status": "REGISTERED",
         "created_at": None},
    ]}


def check_registry(reg: dict, current_bound_map: dict) -> list[str]:
    """返回拒绝原因列表(空 = 通过)。"""
    rejects: list[str] = []
    if not isinstance(reg, dict) or reg.get("schema") != "exec-native-roots-v1":
        return ["R_BAD_SCHEMA"]
    seen_ids: set = set()
    for e in reg.get("entries", []):
        rid = e.get("root_id")
        path = e.get("root_path", "")
        # R1 根未登记(由调用方决定是否登记;此处校验登记内容合法性)
        # R2 与旧根/既有目录重叠
        norm = Path(path)
        if not str(norm).startswith(NEW_ROOT_PREFIX.replace("/", "\\")) and \
                not str(norm).startswith(NEW_ROOT_PREFIX):
            rejects.append(f"R2:root_outside_new_area:{path}")
        if str(norm).replace("\\", "/") in {r.replace("\\", "/") for r in OLD_ROOTS}:
            rejects.append(f"R2:overlaps_old_root:{path}")
        for old in OLD_ROOTS:
            if norm.is_relative_to(Path(old)) or Path(old).is_relative_to(norm):
                rejects.append(f"R2:nesting_with_old:{path}<->{old}")
        # R7 历史回改:root_id 复用
        if rid in seen_ids:
            rejects.append(f"R7:root_id_reused:{rid}")
        seen_ids.add(rid)
        # R8 放宽 bound_path
        bp = e.get("bound_paths")
        if not isinstance(bp, list) or not bp:
            rejects.append(f"R8:bound_paths_empty:{rid}")
        else:
            for p in bp:
                if p in ("..", "/", "*", "") or p.startswith("/") or ".." in Path(p).parts:
                    rejects.append(f"R8:bound_path_loose:{rid}:{p}")
        # R3 cohort 绑定与当前 BOUND_FILES 不一致
        cohort = e.get("cohort") or {}
        if cohort.get("bound_files_sha256_map") != current_bound_map:
            rejects.append(f"R3:cohort_bound_mismatch:{rid}")
    return rejects


def check_write(reg: dict, root_id: str, write_rel: str) -> bool:
    """R4:写路径必须在 bound_paths 内;返回是否允许。"""
    for e in reg.get("entries", []):
        if e.get("root_id") != root_id:
            continue
        bp = e.get("bound_paths", [])
        parts = Path(write_rel).parts
        return bool(parts) and parts[0] in bp and ".." not in parts
    return False


def check_old_receipt_as_new(reg: dict, claimed_root: str) -> bool:
    """R5:旧回执(旧根路径)不能冒充本轮材料。"""
    norm = claimed_root.replace("\\", "/")
    return not any(norm == r or norm.startswith(r + "/") for r in OLD_ROOTS)


def check_reuse(used_cohorts: set, cohort_id: str) -> bool:
    """R6:同 cohort 不可重复运行/复用产物。"""
    if cohort_id in used_cohorts:
        return False
    used_cohorts.add(cohort_id)
    return True


def main() -> int:
    current_bound = {"k": "v"}
    scenarios: list[tuple[str, bool, str]] = []
    reg = valid_registry()
    # 基线:全合法 → 0 拒绝
    scenarios.append(("baseline-valid", check_registry(reg, current_bound) == [], ""))
    # R2:根与旧根重叠
    bad = valid_registry()
    bad["entries"][0]["root_path"] = "reviews/codex-supervision/2026-10-05-three-gates"
    scenarios.append(("R2-overlap-old-root", any(
        r.startswith("R2") for r in check_registry(bad, current_bound)), ""))
    # R2:根越出新区
    bad = valid_registry()
    bad["entries"][0]["root_path"] = "reviews/elsewhere/run-x"
    scenarios.append(("R2-outside-new-area", any(
        r.startswith("R2") for r in check_registry(bad, current_bound)), ""))
    # R3:cohort 绑定不一致
    bad = valid_registry()
    bad["entries"][0]["cohort"]["bound_files_sha256_map"] = {"k": "DIFFERENT"}
    scenarios.append(("R3-cohort-mismatch", any(
        r.startswith("R3") for r in check_registry(bad, current_bound)), ""))
    # R4:写路径越界
    scenarios.append(("R4-write-in-bounds", check_write(reg, "n001", "raw/x.json") is True, ""))
    scenarios.append(("R4-write-traversal", check_write(reg, "n001", "../evil.json") is False, ""))
    scenarios.append(("R4-write-absolute", check_write(reg, "n001", "/abs/x") is False, ""))
    # R5:旧回执冒充本轮
    scenarios.append(("R5-old-receipt-rejected",
                      check_old_receipt_as_new(reg, "reviews/codex-supervision/2026-10-05-three-gates") is False, ""))
    scenarios.append(("R5-new-root-accepted",
                      check_old_receipt_as_new(reg, "reviews/exec-native/run-n001") is True, ""))
    # R6:同 cohort 复用
    used: set = set()
    scenarios.append(("R6-first-use-ok", check_reuse(used, "cohort-1") is True, ""))
    scenarios.append(("R6-reuse-refused", check_reuse(used, "cohort-1") is False, ""))
    # R7:root_id 复用
    bad = valid_registry()
    bad["entries"].append(dict(bad["entries"][0]))
    scenarios.append(("R7-root-id-reused", any(
        r.startswith("R7") for r in check_registry(bad, current_bound)), ""))
    # R8:放宽 bound_paths
    for label, bp in [("R8-empty", []), ("R8-dotdot", [".."]), ("R8-star", ["*"])]:
        bad = valid_registry()
        bad["entries"][0]["bound_paths"] = bp
        scenarios.append((label, any(
            r.startswith("R8") for r in check_registry(bad, current_bound)), ""))

    fails = 0
    for name, ok, detail in scenarios:
        print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")
        if not ok:
            fails += 1
    print(f"scenarios={len(scenarios)} fails={fails}")
    receipt = {"scenarios": [{"name": n, "ok": o} for n, o, _ in scenarios],
               "note": "mock-only;不构成原生验收证据"}
    Path(__file__).with_name("mock-root-boundary-receipt.json").write_text(
        json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
