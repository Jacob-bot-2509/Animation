"""训练自动化循环编排器(harness 后台长跑)。

设计契约见 docs/TRAINING-LOOP-DESIGN.md:分层目标(R=100% 且 E≥95% 停)、
连续 3 轮平台停、上限 8 轮;每轮 7 步,门禁自检前置,证据链完整。

当前状态:编排/决策/证据机制可用;训练步与评测步在超参/评测协议未定案
前**拒绝执行**(fail-closed,不伪造)。用法:
  <venv>/Scripts/python.exe -X utf8 tools/train_loop.py --config <rounds.json>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import uuid
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNS = ROOT / "runs"
STOP_FILE = RUNS / "loop.stop"
MAX_ROUNDS = 8
PLATEAU_ROUNDS = 3
# 分层目标(用户 2026-10-05 拍板)
TARGET_RENDER = 1.0      # 渲染成功率 100%
TARGET_EXECUTABLE = 0.95  # 可执行率 ≥95%
METRICS = ("render", "executable", "math", "fidelity")


def _sha(p: Path) -> str | None:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError:
        return None


def gate_ready(run_id: str) -> tuple[bool, str]:
    """门禁自检:preflight --ready 未通过即停,不绕过。"""
    cp = subprocess.run(
        [sys.executable, "-X", "utf8", str(ROOT / "tools/preflight.py"),
         "--manifest", str(ROOT / "data/manifest.json"),
         "--ready", "--run-id", run_id],
        capture_output=True, timeout=600,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    out = (cp.stdout or b"").decode("utf-8", "replace")
    return cp.returncode == 0, out.strip()[-200:]


def train_step(config: dict, work: Path, run_id: str) -> dict:
    """训练步:执行 tools/train_step.py;超参未定案由该脚本 fail-closed。"""
    script = config.get("train_script") or "tools/train_step.py"
    cp = subprocess.run(
        [sys.executable, "-X", "utf8", str(ROOT / script),
         "--config", config["_config_path"], "--work", str(work),
         "--run-id", run_id],
        capture_output=True, timeout=3600 * 8,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    return {"status": "TRAINED" if cp.returncode == 0 else "FAILED",
            "rc": cp.returncode,
            "detail": ((cp.stdout or b"") + (cp.stderr or b"")).decode(
                "utf-8", "replace")[-400:]}


def eval_step(config: dict, work: Path, adapter: Path, run_id: str) -> dict:
    """评测步:执行 tools/eval_step.py;四指标中未接线的判定器如实 UNVERIFIED。"""
    script = config.get("eval_script") or "tools/eval_step.py"
    cp = subprocess.run(
        [sys.executable, "-X", "utf8", str(ROOT / script),
         "--config", config["_config_path"], "--work", str(work),
         "--adapter", str(adapter), "--run-id", run_id],
        capture_output=True, timeout=3600 * 8,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    return {"status": "OK" if cp.returncode == 0 else "FAILED",
            "rc": cp.returncode,
            "detail": ((cp.stdout or b"") + (cp.stderr or b"")).decode(
                "utf-8", "replace")[-400:]}


def metrics_met(m: dict) -> bool:
    return (m.get("render") == TARGET_RENDER
            and m.get("executable", 0) >= TARGET_EXECUTABLE)


def plateau(history: list[dict]) -> bool:
    if len(history) < PLATEAU_ROUNDS:
        return False
    recent = history[-PLATEAU_ROUNDS:]
    keys = set()
    for r in recent:
        keys.update(r["metrics"].keys())
    for k in keys:
        vals = [r["metrics"].get(k) for r in recent if r["metrics"].get(k) is not None]
        if len(vals) == PLATEAU_ROUNDS and len(set(vals)) == 1 and vals[0] != 1.0:
            continue
        return False
    return True


def decide(round_no: int, m: dict, history: list[dict]) -> str:
    if metrics_met(m):
        return "stop_target_met"
    if round_no >= MAX_ROUNDS:
        return "stop_max_rounds"
    if plateau(history):
        return "stop_plateau"
    return "continue"


def run_loop(config: dict) -> int:
    loop_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    work = RUNS / f"loop-{loop_id}"
    work.mkdir(parents=True, exist_ok=True)
    history: list[dict] = []
    for round_no in range(1, MAX_ROUNDS + 1):
        if STOP_FILE.exists():
            (work / "log.jsonl").open("a", encoding="utf-8").write(
                json.dumps({"round": round_no, "event": "stop_file"},
                           ensure_ascii=False) + "\n")
            print(f"[loop] 轮次 {round_no}:stop 文件存在,中止")
            return 0
        run_id = uuid.uuid4().hex[:12]
        rec = {"loop": loop_id, "round": round_no, "run_id": run_id,
               "started": datetime.now().isoformat(timespec="seconds"),
               "config_sha256": _sha(Path(config.get("_config_path", "")))
               if config.get("_config_path") else None}
        # 1. 门禁自检(前置,不绕过)
        ok, tail = gate_ready(run_id)
        if not ok:
            rec.update(event="gate_blocked", gate_out=tail)
            (work / f"round-{round_no}.json").write_text(
                json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"[loop] 轮次 {round_no}:门禁未 ready,循环停止(不绕过)")
            return 2
        # 3. 训练步(超参未定案 → 由 train_step.py fail-closed)
        train = train_step(config, work / f"round-{round_no}", run_id)
        if train["status"] != "TRAINED":
            rec.update(event="train_blocked", detail=train)
            (work / f"round-{round_no}.json").write_text(
                json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"[loop] 轮次 {round_no}:训练步未完成({train['detail'][-120:]})")
            return 2
        adapter = work / f"round-{round_no}" / "adapter"
        # 4-5. 生成+验收(四指标;未接线判定器如实 UNVERIFIED)
        ev = eval_step(config, work / f"round-{round_no}", adapter, run_id)
        if ev["status"] != "OK":
            rec.update(event="eval_blocked", detail=ev)
            (work / f"round-{round_no}.json").write_text(
                json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"[loop] 轮次 {round_no}:评测步未完成({ev['detail'][-120:]})")
            return 2
        report_path = work / f"round-{round_no}" / "eval-report.json"
        try:
            report = json.loads(report_path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            report = {}
        m = {k: report.get(k, {}).get("rate") if isinstance(
            report.get(k), dict) else None for k in METRICS}
        rec.update(event="round_complete", metrics=m,
                   report=report_path.name)
        (work / f"round-{round_no}.json").write_text(
            json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
        history.append({"round": round_no, "metrics": m})
        print(f"[loop] 轮次 {round_no} 完成,指标: {m}")
        verdict = decide(round_no, m, history)
        if verdict != "continue":
            rec.update(final_verdict=verdict)
            (work / f"round-{round_no}.json").write_text(
                json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"[loop] 决策:{verdict},循环结束")
            return 0
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", type=Path, required=True,
                    help="轮次配置 JSON(超参/脚本路径/目标覆盖)")
    args = ap.parse_args(argv)
    config = json.loads(args.config.read_text(encoding="utf-8"))
    config["_config_path"] = str(args.config.resolve())
    return run_loop(config)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
