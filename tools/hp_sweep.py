"""超参扫参器:门禁开后,候选配置逐个训练+固定子集评测,选胜者写回配置。

设计契约见 docs/TRAINING-LOOP-DESIGN.md。诚实原则:
- 门禁自检前置,未 ready 直接停(不绕过);
- 固定子集(默认 eval 中 20 题,seed 固定可复现)只用于选参,绝不进训练;
- 选优标准:可执行率优先、渲染率次之、数学率参考——不看训练 loss;
- render_executor/judge_script 未接线时对应指标 UNVERIFIED,排序只用可用
  指标并如实标注;executor 接线后重跑本扫参即可;
- 每候选独立 work 目录,训练清单+评测报告+哈希落盘,Codex 可审。

用法:
  <venv>/Scripts/python.exe -X utf8 tools/hp_sweep.py --config <sweep.json>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
import uuid
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from train_loop import gate_ready, STOP_FILE  # noqa: E402
import train_step as ts  # noqa: E402
import eval_step as es  # noqa: E402


def build_subset(manifest: Path, count: int, seed: int) -> list[str]:
    """固定 seed 从 eval 题(按 problem_id)抽子集;只评测用,不进训练。"""
    m = json.loads(manifest.read_text(encoding="utf-8"))
    pids = []
    for e in m["entries"]:
        if e["split"] != "eval":
            continue
        p = (manifest.parent / e["path"]).resolve()
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            pid = json.loads(line).get("problem_id")
            if pid and pid not in pids:
                pids.append(pid)
    rng = random.Random(seed)
    return sorted(rng.sample(pids, min(count, len(pids))))


def _verified_rate(metric, expected_total=None):
    """Return an exact, count-bound rate; unknown metrics are never measurements."""
    from fractions import Fraction
    import re
    if not isinstance(metric, dict) or metric.get("status") != "VERIFIED":
        return None
    passed, total, value = metric.get("passed"), metric.get("total"), metric.get("rate")
    if type(passed) is not int or type(total) is not int or total <= 0 or not 0 <= passed <= total:
        raise ValueError("Verified metric requires integer passed/total counts")
    if expected_total is not None and (type(expected_total) is not int or total != expected_total):
        raise ValueError("Metric total does not match evaluated question count")
    if type(value) not in (str, int) or not re.fullmatch(r"[+-]?\d+(?:/\d+)?", str(value)):
        raise ValueError("Verified metric rate must be an exact integer or fraction")
    try:
        rate = Fraction(str(value))
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError("Invalid exact metric rate") from exc
    if not 0 <= rate <= 1 or rate != Fraction(passed, total):
        raise ValueError("Verified metric count/rate mismatch")
    return rate


def rank_candidates(candidates: list[dict]) -> list[dict]:
    """Rank measured E/R exactly; math is a tiebreaker, never a sole winner basis."""
    eligible = []
    for candidate in candidates:
        if not isinstance(candidate, dict) or not isinstance(candidate.get("metrics"), dict):
            raise ValueError("Invalid candidate metric object")
        metrics = candidate["metrics"]
        rates = tuple(_verified_rate(metrics.get(name), metrics.get("total_questions"))
                      for name in ("executable", "render", "math"))
        if rates[0] is None and rates[1] is None:
            continue
        eligible.append((candidate, rates))
    eligible.sort(key=lambda row: tuple(-(rate if rate is not None else -1) for rate in row[1]))
    return [candidate for candidate, _ in eligible]

def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", type=Path, required=True)
    args = ap.parse_args(argv)
    sweep = json.loads(args.config.read_text(encoding="utf-8"))
    if not sweep.get("candidates"):
        print("[FAIL] 候选配置列表为空")
        return 2
    for candidate in sweep['candidates']:
        approval_error=ts.hyperparameter_approval_error(candidate)
        if approval_error:
            print('[FAIL] Candidate '+str(candidate.get('name','unnamed'))+': '+approval_error)
            return 2
    work = ROOT / "runs" / ("hp-sweep-" + datetime.now().strftime("%Y%m%d-%H%M%S"))
    work.mkdir(parents=True, exist_ok=True)
    manifest = Path(sweep.get("dataset_manifest", "data/manifest.json"))
    model_dir = Path(sweep.get("model_path", ".models/qwen3-4b"))
    subset_ids = build_subset(manifest, int(sweep.get("subset", {}).get("count", 20)),
                              int(sweep.get("subset", {}).get("seed", 20261005)))
    subset_path = work / "subset-ids.json"
    subset_path.write_text(json.dumps(subset_ids, ensure_ascii=False, indent=2),
                           encoding="utf-8")
    (work / "sweep-config-snapshot.json").write_text(
        json.dumps(sweep, ensure_ascii=False, indent=2), encoding="utf-8")

    # 门禁自检一次(前置;任何候选训练前)
    run_id = uuid.uuid4().hex[:12]
    gate_config=dict(sweep);gate_config["_config_path"]=str(args.config.resolve())
    ok, tail = gate_ready(run_id,gate_config)
    if not ok:
        print(f"[FAIL] 门禁未 ready,扫参停止(不绕过): {tail}")
        return 2

    results = []
    for i, cand in enumerate(sweep["candidates"], 1):
        if STOP_FILE.exists():
            print(f"[sweep] stop 文件存在,中止(已完成 {i - 1} 个候选)")
            break
        name = cand.get("name") or f"cand-{i}"
        cdir = work / name
        cdir.mkdir(parents=True, exist_ok=True)
        cfg = {"hyperparameters": cand["hyperparameters"],
               "hyperparameter_approval": cand["hyperparameter_approval"],
               "model_path": str(model_dir),
               "dataset_manifest": str(manifest),
               "render_executor": sweep.get("render_executor"),
               "judge_script": sweep.get("judge_script")}
        cfg_path = cdir / "rounds-config.json"
        cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2),
                            encoding="utf-8")
        cfg["_config_path"]=str(cfg_path.resolve())
        print(f"[sweep] 候选 {i}/{len(sweep['candidates'])}: {name} 训练中…")
        trained = ts.train(cfg, cdir, run_id + "-" + name[:8])
        if trained.get("status") != "TRAINED":
            print(f"[sweep] {name} 训练失败,跳过: {trained.get('reason', '')[:120]}")
            results.append({"name": name, "status": "TRAIN_FAILED",
                            "detail": str(trained)[:200]})
            continue
        print(f"[sweep] {name} 子集评测中({len(subset_ids)} 题)…")
        rc = es.run(cfg_path, cdir, cdir / "adapter",
                    run_id + "-" + name[:8], subset_path)
        report = json.loads((cdir / "eval-report.json").read_text(
            encoding="utf-8")) if (cdir / "eval-report.json").exists() else {}
        results.append({"name": name, "status": "OK" if rc == 0 else "EVAL_FAILED",
                        "hyperparameters": cand["hyperparameters"],
                        "hyperparameter_approval": cand["hyperparameter_approval"],
                        "metrics": {k: v for k, v in report.items()
                                    if k in ("executable", "render", "math",
                                             "fidelity", "total_questions")},
                        "eval_rc": rc})
        (work / "sweep-progress.json").write_text(
            json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    selection_error = None
    try:
        ranked = rank_candidates([r for r in results if r.get("status") == "OK"])
    except (ValueError, TypeError) as exc:
        ranked = []
        selection_error = str(exc)
    winner = ranked[0] if ranked else None
    out = {"sweep_config_sha256": hashlib.sha256(
        args.config.read_bytes()).hexdigest(),
           "subset_ids": subset_ids,
           "results": results, "ranked": ranked,
           "winner": winner["name"] if winner else None,
           "selection_status": "MEASURED_WINNER" if winner else "NO_VERIFIED_WINNER",
           "selection_error": selection_error,
           "note": ("选优标准:可执行率 desc、渲染率 desc、数学率参考;"
                    "UNVERIFIED 指标如实不计入排序;render_executor/"
                    "judge_script 接线后应重跑本扫参")}
    (work / "sweep-report.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    md = ["# 超参扫参报告\n", f"- 候选数:{len(results)},子集:{len(subset_ids)} 题"
          f"(seed 固定,只用于选参)\n",
          "| 候选 | 可执行率 | 渲染率 | 数学率 | 总题数 | 状态 |",
          "|---|---|---|---|---|---|"]
    md.append(f"\nSelection: {out['selection_status']}; winner={out['winner']}")
    if selection_error:
        md.append("Selection rejected: " + selection_error)
    for r in ranked + [x for x in results if not any(x is selected for selected in ranked)]:
        mm = r.get("metrics", {})
        md.append(f"| {r['name']} | {mm.get('executable', {}).get('rate')} "
                  f"| {mm.get('render', {}).get('rate')} "
                  f"| {mm.get('math', {}).get('rate')} "
                  f"| {mm.get('total_questions', '')} | {r.get('status')} |")
    md.append("\n> UNVERIFIED 指标因 render_executor/judge_script 未接线而缺省,"
              "接线后重跑本扫参再定胜者。")
    (work / "sweep-report.md").write_text("\n".join(md), encoding="utf-8")
    if winner:
        winner_cfg = {"hyperparameters": ranked[0]["hyperparameters"],
                      "hyperparameter_approval": ranked[0]["hyperparameter_approval"],
                      "model_path": str(model_dir),
                      "dataset_manifest": str(manifest),
                      "train_script": "tools/train_step.py",
                      "eval_script": "tools/eval_step.py",
                      "render_executor": sweep.get("render_executor"),
                      "judge_script": sweep.get("judge_script"),
                      "targets": {"render": "1", "executable": "19/20"},
                      "max_rounds": 8, "plateau_rounds": 3,
                      "_说明": "扫参胜者配置,正式训练循环使用"}
        winner_path = Path(sweep.get("output_winner",
                                     "configs/train_loop.winner.json"))
        if winner_path.exists():
            print(f"[sweep] 胜者配置已存在,不覆盖: {winner_path}")
        else:
            winner_path.parent.mkdir(parents=True, exist_ok=True)
            winner_path.write_text(json.dumps(winner_cfg, ensure_ascii=False,
                                              indent=2), encoding="utf-8")
            print(f"[sweep] 胜者:{winner['name']} → {winner_path}")
    print(json.dumps({"winner": out["winner"], "selection_status": out["selection_status"], "report": str(work)},
                     ensure_ascii=False, indent=2))
    return 0 if winner else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
