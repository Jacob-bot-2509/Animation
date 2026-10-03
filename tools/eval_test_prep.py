"""eval/test 准备接口 CLI(msg_199,只读;正式 split/freeze/READY 未授权)。

用法:
  python tools/eval_test_prep.py status [--dir data/v1]
      报告 eval/test 是否已生成/已冻结(当前应恒为"未生成/未冻结")
  python tools/eval_test_prep.py check <dir> [--train-dir data/v1/raw]
      已生成样本时:入场检查 + 与 train 的精确重叠/近重复隔离检查
  python tools/eval_test_prep.py freeze <dir>
      未授权:一律拒绝(正式 freeze 在用户批准后经 freeze_data 执行)

退出码: 0 = 未生成(如实)或检查通过;1 = 硬伤(泄漏/坏样本);2 = 未授权/参数错误。

报告契约:输出行 [OK]/[FAIL]/[拒绝];status 永不说"已冻结"除非 *.lock.json 真实存在。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.dataset_intake import intake_report  # noqa: E402
from animtrain.manifest import canonical_problem_hash, canonical_problem_text  # noqa: E402
from animtrain.near_dup import ShingleIndex  # noqa: E402

NEAR_DUP_THRESHOLD = 0.7  # UNCALIBRATED 占位阈值(与 validate 一致)


def _jsonl_files(d: Path) -> list[Path]:
    if d.is_file():
        return [d] if d.suffix == ".jsonl" else []
    return sorted(d.rglob("*.jsonl")) if d.is_dir() else []


def _load_lines(p: Path) -> list[str]:
    return [l for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def cmd_status(args) -> int:
    base = Path(args.dir)
    import hashlib  # noqa: PLC0415
    from animtrain.freeze import check_frozen, frozen_paths  # noqa: PLC0415
    from animtrain.manifest import Manifest  # noqa: PLC0415
    # Accept active/archive bindings only when they cover the selected files.
    manifests: list[Path] = []
    for top_manifest in (ROOT / "data" / "manifest.json",
                         ROOT / "data" / "v1" / "manifest.json",
                         base.parent / "manifest.json"):
        if top_manifest.exists() and top_manifest not in manifests:
            manifests.append(top_manifest)
    for name in ("eval", "test"):
        for cand in ((base / name / "manifest.json"),
                     (base / "manifest.json"),
                     (base / "manifest-v1.json")):   # v1 归档清单(v2 切换后)
            if cand.exists() and cand not in manifests:
                manifests.append(cand)
    manifest_shas: dict[str, tuple[Path, set[str]]] = {}
    for mp in manifests:
        try:
            manifest = Manifest.load(mp)
            paths = {str((mp.parent / entry.path).resolve())
                     for entry in manifest.entries}
            manifest_shas[hashlib.sha256(mp.read_bytes()).hexdigest()] = (mp, paths)
        except (OSError, ValueError, TypeError, KeyError, AttributeError):
            continue  # A damaged manifest cannot validate a binding.
    for name in ("eval", "test"):
        d = base / name
        files = _jsonl_files(d)
        locks = sorted(d.rglob("*.lock.json")) if d.is_dir() else []
        # 锁亦可位于 data/ 层(preflight discover_locks 口径:向上扫描到 data/)
        locks += sorted(base.parent.glob(f"{name}*.lock.json"))
        locks = sorted({p.resolve(): p for p in locks}.values())
        if not files:
            print(f"[OK] {name}: 未生成任何样本(如实,非失败)")
        else:
            print(f"[OK] {name}: 已生成 {len(files)} 个 JSONL")
        if not locks:
            print(f"[OK] {name}: 未冻结(已生成未冻结;正式 freeze 需用户批准)")
            continue
        # msg_256:发现锁 ≠ 冻结有效 —— 逐锁校验结构/覆盖/manifest 绑定,
        # 坏锁/无关锁不得冒充有效冻结
        for lk in locks:
            problems = check_frozen(lk)   # 结构/数据哈希:坏锁必须 WARN
            frozen = frozen_paths(lk)
            if not problems and frozen and not any(
                    str(f.resolve()) in frozen for f in files):
                # 结构完好但只覆盖其他版本文件(v1/v2 并存):如实 INFO,不参与判定
                print(f"[INFO] {name}: 锁 {lk.name} 覆盖其他版本文件,不参与本次判定")
                continue
            uncovered = [str(f.resolve()) for f in files
                         if str(f.resolve()) not in frozen]
            if uncovered:
                problems.append(f"锁未覆盖当前 JSONL: {uncovered}")
            bound = None
            try:
                bound = json.loads(lk.read_text(encoding="utf-8")) \
                    .get("meta", {}).get("manifest_sha256")
            except (OSError, ValueError):
                bound = None
            current_paths = {str(f.resolve()) for f in files}
            binding = manifest_shas.get(bound) if isinstance(bound, str) else None
            if binding is None or not current_paths.issubset(binding[1]):
                problems.append(f"manifest 绑定不一致(锁绑定 {str(bound)[:12]}…,"
                                f"候选清单 {[m.name for m in manifests]})")
            if problems:
                print(f"[WARN] {name}: 冻结锁 {lk.name} 校验未过"
                      f"({len(problems)} 项,不视为已冻结):")
                for p in problems[:3]:
                    print(f"       - {p}")
            else:
                print(f"[OK] {name}: 冻结锁 {lk.name} 校验通过"
                      f"(结构/覆盖/manifest 绑定一致)")
    return 0


def cmd_check(args) -> int:
    # GS3(msg_221):按逻辑角色聚合 —— eval 组 / test 组;物理文件不是逻辑 split。
    # 未给角色时位置参数整体视为单一候选组(向后兼容)。
    eval_dirs = [Path(x) for x in (args.eval or [])]
    test_dirs = [Path(x) for x in (args.test or [])]
    if not eval_dirs and not test_dirs and getattr(args, "dirs", None):
        eval_dirs = [Path(x) for x in args.dirs]
    eval_files = sorted({f for d in eval_dirs for f in _jsonl_files(d)})
    test_files = sorted({f for d in test_dirs for f in _jsonl_files(d)})
    files = sorted(set(eval_files + test_files))
    if not files:
        print(f"[OK] {args.dirs}: 未生成任何样本 —— 如实报告,不视为检查通过")
        return 0
    # A9: reference availability and schema are part of isolation evidence.
    train_dir = Path(args.train_dir)
    train_files = _jsonl_files(train_dir)
    if not train_files:
        print(f"[FAIL] train {train_dir}: 训练参考集不存在或没有 JSONL，"
              "无法验证隔离；不得报告通过")
        return 1
    # One aggregate preserves intake rules across candidate/reference files:
    # malformed/empty references and global duplicate IDs are hard failures.
    rep = intake_report(files + train_files)
    problems: list[str] = list(rep["problems"])
    if rep["quarantines"]:
        print(f"[WARN] 候选/训练参考集存在 {len(rep['quarantines'])} 项 quarantine；"
              "仅继续隔离预检，不表示入场完整验收")
    if problems:
        for p in problems:
            print(f"  [FAIL] {p}")
        print(f"结论: 入场或参考集检查不通过,{len(problems)} 个问题")
        return 1
    # 与 train 的隔离检查(精确重叠 + 近重复)
    train_lines: list[str] = []
    for f in train_files:
        train_lines += _load_lines(f)
    train_hashes = {canonical_problem_hash(l) for l in train_lines}
    near_idx = ShingleIndex()
    for i, l in enumerate(train_lines):
        near_idx.add(canonical_problem_text(l), {"path": "train", "line": i})
    for f in files:
        for i, l in enumerate(_load_lines(f), 1):
            ch = canonical_problem_hash(l)
            if ch in train_hashes:
                problems.append(f"{f.name}:{i} 与 train 精确重叠(核心正文哈希相同)"
                                "——评测题目族必须独立")
                continue
            sim, hit = near_idx.max_sim(canonical_problem_text(l))
            if sim >= NEAR_DUP_THRESHOLD:
                problems.append(f"{f.name}:{i} 与 train 近重复(5-gram Jaccard "
                                f"{sim:.3f} ≥ {NEAR_DUP_THRESHOLD},"
                                f"命中 train 行 {hit['line'] + 1})")
    # GS3:多解组约束(候选组内,跨文件聚合)——同 problem_id 同题干/method 唯一/必填
    from animtrain.dataset_intake import (  # noqa: PLC0415
        check_multi_solution_groups, record_identity)
    group_records: list[tuple[int, dict]] = []
    for f in files:
        for i, l in enumerate(_load_lines(f), 1):
            try:
                group_records.append((i, json.loads(l)))
            except json.JSONDecodeError:
                continue
    for gp in check_multi_solution_groups(group_records):
        problems.append(f"多解组约束: {gp}")

    def _group_sets(flist: list[Path]) -> tuple[set, set]:
        hs: set[str] = set()
        ids: set[str] = set()
        for f in flist:
            for l in _load_lines(f):
                hs.add(canonical_problem_hash(l))
                try:
                    ids.add(record_identity(json.loads(l)))
                except json.JSONDecodeError:
                    continue
        return hs, ids

    # GS3(msg_221):跨角色隔离 —— 只按逻辑角色(eval 组 vs test 组)隔离,
    # 同组内多文件/多解不算跨集合
    if eval_files and test_files:
        he, ie = _group_sets(eval_files)
        ht, it = _group_sets(test_files)
        overlap = he & ht
        if overlap:
            problems.append(f"eval 组与 test 组跨集合同题重叠 {len(overlap)} 条"
                            "(核心正文哈希)—— 评测题目族必须独立(GS3)")
        shared = {x for x in ie & it if x}
        if shared:
            problems.append(f"eval 组与 test 组跨集合 ID 重叠: "
                            f"{sorted(shared)[:5]}(GS3)")
    if problems:
        for p in problems:
            print(f"  [FAIL] {p}")
        print(f"结论: 隔离检查不通过,{len(problems)} 个问题")
        return 1
    print(f"[OK] {args.dirs}: 入场检查、train 隔离与候选集间隔离检查通过"
          f"(近重复阈值 {NEAR_DUP_THRESHOLD} UNCALIBRATED)")
    return 0


def cmd_freeze(args) -> int:
    print(f"[拒绝] {args.dir}: 正式 freeze 未授权"
          "(msg_199:不执行正式 split/freeze/READY;用户批准后经 freeze_data 执行)")
    return 2


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="eval/test 准备接口(只读;freeze 未授权)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    ps = sub.add_parser("status", help="报告 eval/test 生成/冻结状态")
    ps.add_argument("--dir", default=str(ROOT / "data/v1"))
    ps.set_defaults(fn=cmd_status)
    pc = sub.add_parser("check", help="已生成样本时:入场检查 + 与 train 隔离 + 组约束/跨角色隔离")
    pc.add_argument("dirs", nargs="*", help="候选文件/目录(未给 --eval/--test 时整体视为一组)")
    pc.add_argument("--eval", nargs="*", default=None, help="eval 组(逻辑角色)")
    pc.add_argument("--test", nargs="*", default=None, help="test 组(逻辑角色)")
    pc.add_argument("--train-dir", default=str(ROOT / "data/v1/raw"))
    pc.set_defaults(fn=cmd_check)
    pf = sub.add_parser("freeze", help="未授权:一律拒绝")
    pf.add_argument("dir")
    pf.set_defaults(fn=cmd_freeze)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
