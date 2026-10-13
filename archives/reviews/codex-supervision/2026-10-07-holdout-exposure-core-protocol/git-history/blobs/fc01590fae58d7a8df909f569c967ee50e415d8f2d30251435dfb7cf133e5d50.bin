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

from animtrain.dataset_intake import check_intake_file  # noqa: E402
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
    for name in ("eval", "test"):
        d = base / name
        files = _jsonl_files(d)
        locks = sorted(d.rglob("*.lock.json")) if d.is_dir() else []
        if not files:
            print(f"[OK] {name}: 未生成任何样本(如实,非失败)")
        else:
            print(f"[OK] {name}: 已生成 {len(files)} 个 JSONL —— "
                  f"但未冻结(仅占位目录不允许生成;如需检查请用 check)")
        if locks:
            print(f"[OK] {name}: 冻结锁 {len(locks)} 个(冻结状态以锁为准)")
        else:
            print(f"[OK] {name}: 未冻结")
    return 0


def cmd_check(args) -> int:
    d = Path(args.dir)
    files = _jsonl_files(d)
    if not files:
        print(f"[OK] {d}: 未生成任何样本 —— 如实报告,不视为检查通过")
        return 0
    problems: list[str] = []
    for f in files:
        rep = check_intake_file(f)
        for p in rep["problems"]:
            problems.append(f"{f.name}: {p}")
        if rep["status"] == "rejected":
            print(f"[FAIL] {f}: 入场检查 rejected(problems {len(rep['problems'])})")
        elif rep["status"] == "candidate":
            print(f"[WARN] {f}: 入场检查 candidate(quarantine "
                  f"{len(rep['quarantines'])},不阻断隔离检查)")
    # 与 train 的隔离检查(精确重叠 + 近重复)
    train_dir = Path(args.train_dir)
    train_lines: list[str] = []
    for f in _jsonl_files(train_dir):
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
    if problems:
        for p in problems:
            print(f"  [FAIL] {p}")
        print(f"结论: 隔离检查不通过,{len(problems)} 个问题")
        return 1
    print(f"[OK] {d}: 入场检查与 train 隔离检查通过(近重复阈值 "
          f"{NEAR_DUP_THRESHOLD} UNCALIBRATED)")
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
    pc = sub.add_parser("check", help="已生成样本时:入场检查 + 与 train 隔离检查")
    pc.add_argument("dir")
    pc.add_argument("--train-dir", default=str(ROOT / "data/v1/raw"))
    pc.set_defaults(fn=cmd_check)
    pf = sub.add_parser("freeze", help="未授权:一律拒绝")
    pf.add_argument("dir")
    pf.set_defaults(fn=cmd_freeze)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
