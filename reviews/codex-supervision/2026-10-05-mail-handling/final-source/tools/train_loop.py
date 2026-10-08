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
sys.path[:0]=[str(ROOT),str(ROOT/"src")]
RUNS = ROOT / "runs"
STOP_FILE = RUNS / "loop.stop"
MAX_ROUNDS = 8
PLATEAU_ROUNDS = 3
# 分层目标(用户 2026-10-05 拍板)
TARGET_RENDER = 1      # 渲染成功率 100%
TARGET_EXECUTABLE = "19/20"  # 可执行率 ≥95%
METRICS = ("render", "executable", "math", "fidelity")


def _sha(p: Path) -> str | None:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError:
        return None



def prepare_snapshot(run_id,config,manifest):
    """Create a real readiness snapshot before requiring it; never invent metrics."""
    import re
    if not isinstance(run_id,str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}',run_id):return False,'Invalid run_id'
    config_path=Path(config.get('_config_path',''))
    if not config_path.is_file():return False,'Actual config file is required for a readiness snapshot'
    stored=json.loads(config_path.read_text(encoding='utf-8'))
    if stored!={k:v for k,v in config.items() if k!='_config_path'}:
        return False,'In-memory config differs from bound config file'
    snapshot=ROOT/'runs'/run_id/'run_record.json'
    if not snapshot.exists():
        command=[sys.executable,'-X','utf8',str(ROOT/'tools/run_record.py'),'init',
                 '--run-id',run_id,'--kind','dry-run','--config',str(config_path.resolve()),
                 '--manifest',str(manifest),'--command','readiness check; training has not started']
        cp=subprocess.run(command,capture_output=True,timeout=120,cwd=ROOT,
                          creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        if cp.returncode!=0:return False,'Readiness snapshot failed: '+(cp.stdout or b'').decode('utf-8','replace')[-200:]
    try:
        record=json.loads(snapshot.read_text(encoding='utf-8'))
        if record['config']['sha256']!=_sha(config_path) or record['manifest_hash']!=_sha(manifest):
            return False,'Readiness snapshot config or manifest is stale'
        if record.get('dirty',{}).get('truncated'):return False,'Readiness code snapshot is incomplete (truncated)'
    except (OSError,ValueError,KeyError,TypeError):return False,'Readiness snapshot is missing or invalid'
    from animtrain.run_record import RunRecord,verify_replay
    from tools.run_record import git_head,git_dirty
    problems=verify_replay(RunRecord.from_dict(record),manifest_path=manifest,
                           git_commit_now=git_head(),dirty_now=git_dirty(),config_path=config_path)
    if problems:return False,'Readiness snapshot cannot be replayed: '+ '; '.join(problems[:2])
    return True,'Readiness snapshot bound; training has not started'


def gate_ready(run_id: str, config: dict | None = None) -> tuple[bool, str]:
    """门禁自检:preflight --ready 未通过即停,不绕过。"""
    cfg=config or {}
    manifest=Path(cfg.get('dataset_manifest',ROOT/'data/manifest.json')).resolve()
    if manifest!=(ROOT/'data/manifest.json').resolve():
        return False,'Configured manifest is not the currently reviewed dataset'
    from tools.training_data_policy import check_training_diversity
    ok,detail=check_training_diversity(manifest,ROOT/'configs/training_diversity_policy.json',ROOT/'data/training_diversity_evidence.json')
    if not ok:return False,detail
    model=Path(cfg.get('model_path',ROOT/'.models/qwen3-4b')).resolve()
    if config is not None:
        ok,detail=prepare_snapshot(run_id,cfg,manifest)
        if not ok:return False,detail
    cp = subprocess.run(
        [sys.executable, "-X", "utf8", str(ROOT / "tools/preflight.py"),
         "--manifest", str(manifest), "--model",str(model),
         "--ready", "--run-id", run_id],
        capture_output=True, timeout=600,cwd=ROOT,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    out = (cp.stdout or b"").decode("utf-8", "replace")
    return cp.returncode == 0, out.strip()[-200:]


def train_step(config: dict, work: Path, run_id: str) -> dict:
    """训练步:执行 tools/train_step.py;超参未定案由该脚本 fail-closed。"""
    script = config.get("train_script") or "tools/train_step.py"
    if script!="tools/train_step.py":return {"status":"FAILED","rc":2,"detail":"Unreviewed training executor refused"}
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
    if script!="tools/eval_step.py":return {"status":"FAILED","rc":2,"detail":"Unreviewed evaluation executor refused"}
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


def exact_rate(value):
    from fractions import Fraction
    import math
    if isinstance(value,bool) or value is None:return None
    try:
        if isinstance(value,float) and not math.isfinite(value):return None
        rate=Fraction(str(value))
        return rate if 0<=rate<=1 else None
    except (ValueError,ZeroDivisionError,TypeError):return None


def metrics_met(m: dict) -> bool:
    r=exact_rate(m.get('render'));e=exact_rate(m.get('executable'))
    return r==1 and e is not None and e>=exact_rate(TARGET_EXECUTABLE)


def plateau(history: list[dict]) -> bool:
    if len(history)<PLATEAU_ROUNDS+1:return False
    rounds=history[-(PLATEAU_ROUNDS+1):]
    # Three consecutive rounds with no improvement require four checkpoints.
    # Unknown metrics never count as plateau evidence.
    known=[k for k in METRICS if all(exact_rate(r['metrics'].get(k)) is not None for r in rounds)]
    if not {'render','executable'}.issubset(known):return False
    return all(exact_rate(rounds[i+1]['metrics'][k])<=max(exact_rate(r['metrics'][k])
               for r in rounds[:i+1]) for i in range(PLATEAU_ROUNDS) for k in known)


def decide(round_no: int, m: dict, history: list[dict]) -> str:
    if metrics_met(m):
        return "stop_target_met"
    if round_no >= MAX_ROUNDS:
        return "stop_max_rounds"
    if plateau(history):
        return "stop_plateau"
    return "continue"


def run_loop(config: dict) -> int:
    from tools.train_step import hyperparameter_approval_error
    approval_error=hyperparameter_approval_error(config)
    if approval_error:
        print('[FAIL] '+approval_error)
        return 2
    loop_id = datetime.now().strftime("%Y%m%d-%H%M%S")+"-"+uuid.uuid4().hex[:8]
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
        ok, tail = gate_ready(run_id,config)
        if not ok:
            rec.update(event="gate_blocked", gate_out=tail)
            (work / f"round-{round_no}.json").write_text(
                json.dumps(rec, ensure_ascii=False, indent=2), encoding="utf-8")
            print(f"[loop] 轮次 {round_no}:门禁未 ready,循环停止(不绕过)")
            return 2
        # Missing R/E evidence is blocked before retraining or deciding success.
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
        if any(exact_rate(m.get(k)) is None for k in ('render','executable')):
            rec.update(event='metrics_unverified',metrics=m)
            (work/f'round-{round_no}.json').write_text(json.dumps(rec,ensure_ascii=False,indent=2),encoding='utf-8')
            return 2
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
