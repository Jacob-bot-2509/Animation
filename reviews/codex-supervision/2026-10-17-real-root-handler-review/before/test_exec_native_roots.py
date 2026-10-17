"""exec_native_roots 对抗回归测试(真实断言,失败 exit 非零)。

覆盖 v2 R1-R8 + Codex 复现过的 8 类误接受(空注册表/root 逃逸/未知回执根/
FROZEN 写入/ADS 写入/绝对 bound_path/无效 SHA/不同 ID 同根)与历史链七类。
纯内存与临时目录,不建真实 ROOTS、不探测实盘重解析点。
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from exec_native_roots import (  # noqa: E402
    BOUND_PATH_SET, HistoryChain, JobReservation, check_receipt_root,
    check_registry_entries, check_write, literal_relpath_issues, valid_root_id)

OLD_ROOTS = ["reviews/codex-supervision/2026-10-05-three-gates",
             "reviews/codex-supervision/2026-10-06-all43-sandbox-repair",
             "reviews/2026-10-06-exec-isolation-full-surface"]
CURRENT_BOUND = {"src/animtrain/sandbox_execution.py": "a" * 64,
                 "src/animtrain/render_gate.py": "b" * 64}


def entry(root_id="n001", **over):
    base = {
        "root_id": root_id,
        "root_path": f"reviews/exec-native/run-{root_id}",
        "purpose": "surface",
        "cohort": {"collector_sha256": "c" * 64, "verifier_sha256": "d" * 64,
                   "bound_files_sha256_map": dict(CURRENT_BOUND)},
        "bound_paths": ["raw", "work", "media"],
        "status": "ACTIVE",
        "created_at": "2026-10-17T00:00:00+08:00",
    }
    base.update(over)
    return base


def run_scenarios() -> list[tuple[str, bool, str]]:
    rows: list[tuple[str, bool, str]] = []
    base = [entry()]

    # 基线
    ok, probs = check_registry_entries(base, CURRENT_BOUND, OLD_ROOTS, None)
    rows.append(("baseline-valid", ok and not probs, str(probs)))

    # R1 空注册表 / 坏 ID / 未知键 / 坏 purpose / 坏 status
    for label, bad in [
        ("R1-empty-entries", []),
        ("R1-bad-root-id", [entry(root_id="N@x")]),
        ("R1-unexpected-keys", [entry(root_id="n002", extra="x")]),
        ("R1-bad-purpose", [entry(root_id="n003", purpose="joint|surface")]),
        ("R1-bad-status", [entry(root_id="n004", status="BROKEN")]),
    ]:
        ok, probs = check_registry_entries(bad, CURRENT_BOUND, OLD_ROOTS, None)
        rows.append((label, not ok, str(probs)))

    # R2 根路径逃逸/旧根重叠/嵌套/不同 ID 同根
    for label, bad in [
        ("R2-root-escape", [entry(root_id="n005", root_path="reviews/exec-native/../evil")]),
        ("R2-overlap-old-root", [entry(root_id="n006",
                                       root_path="reviews/codex-supervision/2026-10-05-three-gates")]),
        ("R2-nesting", [entry(root_id="n007", root_path="reviews/exec-native/run-n007a"),
                        entry(root_id="n007a", root_path="reviews/exec-native/run-n007a")]),
    ]:
        ok, probs = check_registry_entries(bad, CURRENT_BOUND, OLD_ROOTS, None)
        rows.append((label, not ok, str(probs)))

    # R3 无效 SHA / 绑定不一致
    for label, bad in [
        ("R3-bad-collector-sha", [entry(root_id="n008",
                                        cohort={"collector_sha256": "zz",
                                                "verifier_sha256": "d" * 64,
                                                "bound_files_sha256_map": dict(CURRENT_BOUND)})]),
        ("R3-bound-map-mismatch", [entry(root_id="n009",
                                         cohort={"collector_sha256": "c" * 64,
                                                 "verifier_sha256": "d" * 64,
                                                 "bound_files_sha256_map": {"k": "v"}})]),
        ("R3-empty-bound-map", [entry(root_id="n010",
                                      cohort={"collector_sha256": "c" * 64,
                                              "verifier_sha256": "d" * 64,
                                              "bound_files_sha256_map": {}})]),
    ]:
        ok, probs = check_registry_entries(bad, CURRENT_BOUND, OLD_ROOTS, None)
        rows.append((label, not ok, str(probs)))

    # R4 写权限
    rows.append(("R4-write-ok", check_write(base, "n001", "raw/x.json", "d" * 64)[0], ""))
    rows.append(("R4-not-active", not check_write(
        [entry(status="REGISTERED")], "n001", "raw/x.json", "d" * 64)[0], ""))
    rows.append(("R4-frozen-write", not check_write(
        [entry(status="FROZEN")], "n001", "raw/x.json", "d" * 64)[0], ""))
    rows.append(("R4-outside-bounds", not check_write(base, "n001", "secret/x.json", "d" * 64)[0], ""))
    rows.append(("R4-traversal", not check_write(base, "n001", "../evil.json", "d" * 64)[0], ""))
    rows.append(("R4-ads-write", not check_write(base, "n001", "raw/x:stream", "d" * 64)[0], ""))
    rows.append(("R4-absolute", not check_write(base, "n001", "D:/x.json", "d" * 64)[0], ""))
    rows.append(("R4-reparse-fact", not check_write(base, "n001", "raw/x.json", "d" * 64,
                                                    reparse_paths={"reviews/exec-native/run-n001/raw"})[0], ""))

    # R5 回执根
    rows.append(("R5-unknown-root", not check_receipt_root(base, "n999", "run-x", "d" * 64)[0], ""))
    rows.append(("R5-cohort-mismatch", not check_receipt_root(base, "n001", "run-x", "e" * 64)[0], ""))
    rows.append(("R5-no-run-id", not check_receipt_root(base, "n001", "", "d" * 64)[0], ""))
    rows.append(("R5-ok", check_receipt_root(base, "n001", "run-x", "d" * 64)[0], ""))

    # R6 job 预留
    with tempfile.TemporaryDirectory() as td:
        jr = JobReservation(Path(td))
        rows.append(("R6-first-reserve-ok", jr.reserve("c1", "job-1")[0], ""))
        rows.append(("R6-same-job-refused", not jr.reserve("c1", "job-1")[0], ""))
        rows.append(("R6-other-job-same-cohort-ok", jr.reserve("c1", "job-2")[0], ""))
        rows.append(("R6-finalize-ok", jr.finalize("job-1")[0], ""))

    # R7 历史链
    snap1 = {"schema": "exec-native-roots-v2", "entries": [entry(status="REGISTERED")]}
    snap2 = {"schema": "exec-native-roots-v2",
             "entries": [entry(status="ACTIVE")],
             "previous_registry_sha256": None}
    import hashlib
    snap2["previous_registry_sha256"] = hashlib.sha256(
        json.dumps(snap1, ensure_ascii=False).encode()).hexdigest()
    hc = HistoryChain(json.dumps(snap1, ensure_ascii=False).encode())
    rows.append(("R7-chain-ok", hc.verify_against(snap2)[0], ""))
    rows.append(("R7-no-prev-snapshot", not HistoryChain(None).verify_against(snap2)[0], ""))
    bad2 = dict(snap2); bad2["previous_registry_sha256"] = "f" * 64
    rows.append(("R7-prev-sha-mismatch", not hc.verify_against(bad2)[0], ""))
    deleted = {"schema": "exec-native-roots-v2", "entries": [],
               "previous_registry_sha256": snap2["previous_registry_sha256"]}
    rows.append(("R7-history-deleted", not hc.verify_against(deleted)[0], ""))
    rewritten = {"schema": "exec-native-roots-v2",
                 "entries": [entry(status="FROZEN",
                                   root_path="reviews/exec-native/run-n001x")],
                 "previous_registry_sha256": snap2["previous_registry_sha256"]}
    rows.append(("R7-history-rewrite", not hc.verify_against(rewritten)[0], ""))
    snapF = {"schema": "exec-native-roots-v2", "entries": [entry(status="FROZEN")]}
    snapF_sha = hashlib.sha256(json.dumps(snapF, ensure_ascii=False).encode()).hexdigest()
    hc2 = HistoryChain(json.dumps(snapF, ensure_ascii=False).encode())
    rollback = {"schema": "exec-native-roots-v2",
                "entries": [entry(status="ACTIVE")],
                "previous_registry_sha256": snapF_sha}
    rows.append(("R7-status-rollback", not hc2.verify_against(rollback)[0], ""))

    # R8 白名单
    for label, bad in [
        ("R8-empty", [entry(root_id="n011", bound_paths=[])]),
        ("R8-not-subset", [entry(root_id="n012", bound_paths=["raw", "secret"])]),
        ("R8-duplicate", [entry(root_id="n013", bound_paths=["raw", "raw"])]),
        ("R8-dotdot-in-bounds", [entry(root_id="n014", bound_paths=["raw", ".."])]),
    ]:
        ok, probs = check_registry_entries(bad, CURRENT_BOUND, OLD_ROOTS, None)
        rows.append((label, not ok, str(probs)))

    # 字面路径校验单元
    for label, rel, expect_ok in [
        ("literal-ok", "raw/x.json", True),
        ("literal-dotdot", "raw/../x", False),
        ("literal-dot-segment", "./raw", False),
        ("literal-unc", "\\\\server\\share", False),
        ("literal-drive", "C:/x", False),
        ("literal-ads", "raw/x:stream", False),
        ("literal-device", "raw/CON", False),
        ("literal-trailing-dot", "raw/x.", False),
        ("literal-trailing-space", "raw/x ", False),
        ("literal-wildcard", "raw/*.json", False),
        ("literal-control", "raw/x\x01", False),
        ("literal-backslash-mixed", "raw\\x/y", True),  # 纯分隔混用不算别名
    ]:
        issues = literal_relpath_issues(rel)
        rows.append((label, (not issues) == expect_ok, str(issues)))

    return rows


def main() -> int:
    rows = run_scenarios()
    fails = 0
    for name, ok, detail in rows:
        print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")
        if not ok:
            fails += 1
    print(f"scenarios={len(rows)} fails={fails}")
    receipt = {"scenarios": [{"name": n, "ok": o} for n, o, _ in rows],
               "scope": "SYNTHETIC_MODEL_ONLY_NOT_NATIVE_ACCEPTANCE",
               "source_sha256": None}
    import hashlib
    receipt["source_sha256"] = hashlib.sha256(
        (HERE / "exec_native_roots.py").read_bytes()).hexdigest()
    out = HERE / "exec-native-roots-receipt.json"
    if out.exists():
        print("receipt exists; refusing overwrite")
        return 1
    out.write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
