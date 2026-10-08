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
from datetime import datetime, timezone, timedelta
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
    try: stored=json.loads(config_path.read_text(encoding='utf-8'))
    except (OSError,ValueError): return False,'Invalid actual config file'
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
    manifest=project_path(cfg.get('dataset_manifest','data/manifest.json'))
    if manifest!=(ROOT/'data/manifest.json').resolve():
        return False,'Configured manifest is not the currently reviewed dataset'
    from tools.training_data_policy import check_training_diversity
    ok,detail=check_training_diversity(manifest,ROOT/'configs/training_diversity_policy.json',ROOT/'data/training_diversity_evidence.json')
    if not ok:return False,detail
    model=project_path(cfg.get('model_path','.models/qwen3-4b'))
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


def project_path(value):
    p=Path(value)
    return (p if p.is_absolute() else ROOT/p).resolve()


def adapter_hash(adapter):
    files=sorted(p for p in adapter.rglob('*') if p.is_file())
    if not files or any(p.is_symlink() for p in files):raise ValueError('adapter is missing or contains links')
    payload=[(p.relative_to(adapter).as_posix(),_sha(p)) for p in files]
    if any(sha is None for _,sha in payload):raise ValueError('adapter contains unreadable files')
    return hashlib.sha256(json.dumps(payload,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()


def report_metrics(report,run_id,config,round_work):
    """Reject stale/unverified metrics and mathematically inconsistent counts."""
    from fractions import Fraction
    if not isinstance(report,dict) or report.get('run_id')!=run_id:raise ValueError('evaluation run_id mismatch')
    expected={'config_sha256':_sha(Path(config['_config_path'])),
        'manifest_sha256':_sha(project_path(config.get('dataset_manifest','data/manifest.json'))),
        'training_manifest_sha256':_sha(round_work/'training-manifest.json'),
        'generated_specs_sha256':_sha(round_work/'generated-specs.json'),
        'adapter_sha256':adapter_hash(round_work/'adapter')}
    if any(v is None for v in expected.values()) or report.get('bindings')!=expected:raise ValueError('evaluation input/adapter binding missing or stale')
    manifest=project_path(config.get('dataset_manifest','data/manifest.json'))
    wanted={sp:set() for sp in ('eval','test')}
    for entry in json.loads(manifest.read_text('utf-8'))['entries']:
        if entry['split'] in wanted:
            for line in (manifest.parent/entry['path']).read_text('utf-8').splitlines():
                if line.strip():
                    row=json.loads(line);wanted[entry['split']].add(row.get('problem_id') or row['id'])
    if not all(wanted.values()):raise ValueError('empty evaluation split')
    def verified(metric,total):
        if not isinstance(metric,dict) or metric.get('status')!='VERIFIED':raise ValueError('metric is unverified')
        passed=metric.get('passed');n=metric.get('total');rate=exact_rate(metric.get('rate'))
        if type(passed) is not int or type(n) is not int or n!=total or not 0<=passed<=n or rate!=Fraction(passed,n):raise ValueError('metric count/rate mismatch')
        return rate
    m={k:None for k in METRICS}
    for key in ('render','executable'):
        total=sum(len(v) for v in wanted.values());splits=report.get('by_split',{})
        for sp in wanted:verified(splits.get(sp,{}).get(key),len(wanted[sp]))
        if report[key].get('passed')!=sum(splits[sp][key]['passed'] for sp in wanted):raise ValueError('aggregate/split metric mismatch')
        m[key]=str(verified(report[key],total))
    for key in ('math','fidelity'):
        value=report.get(key,{})
        if isinstance(value,dict) and value.get('status')=='VERIFIED':m[key]=str(verified(value,total))
    return m


def persist_round(work,rec,report=None):
    payload=json.dumps(rec,ensure_ascii=False,indent=2,allow_nan=False)+'\n'
    with (work/f'round-{rec["round"]}.json').open('x',encoding='utf-8',newline='\n') as stream:stream.write(payload)
    with (work/'log.jsonl').open('a',encoding='utf-8',newline='\n') as stream:stream.write(json.dumps(rec,ensure_ascii=False,allow_nan=False)+'\n')
    md=f'# Round {rec["round"]}\n\nRun: `{rec["run_id"]}`\n\nStatus: `{rec["event"]}`\n\n'
    md+='```json\n'+payload+'```\n'
    with (work/f'round-{rec["round"]}.md').open('x',encoding='utf-8',newline='\n') as stream:stream.write(md)
    queue_path=work/'hard-queue.json'
    queue=json.loads(queue_path.read_text('utf-8')) if queue_path.exists() else []
    # IDs and reasons only. Frozen eval/test text is never fed into training.
    if report:
        for failure in report.get('failures',[]):
            if isinstance(failure,dict):queue.append({'round':rec['round'],'run_id':rec['run_id'],'problem_id':failure.get('problem_id'),'sample_id':failure.get('sample_id'),'reason':'evaluation failure; manual review only'})
        if any(report.get(k,{}).get('status')!='VERIFIED' for k in ('math','fidelity')):
            queue.append({'round':rec['round'],'run_id':rec['run_id'],'reason':'mathematics or fidelity unverified; manual review required'})
    queue_path.write_text(json.dumps(queue,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def run_loop(config):
    from tools.train_step import hyperparameter_approval_error
    error=hyperparameter_approval_error(config)
    if error:print('[FAIL] '+error);return 2
    if config.get('max_rounds',MAX_ROUNDS)!=MAX_ROUNDS or config.get('plateau_rounds',PLATEAU_ROUNDS)!=PLATEAU_ROUNDS or any(exact_rate(config.get('targets',{}).get(k,v))!=exact_rate(v) for k,v in (('render',TARGET_RENDER),('executable',TARGET_EXECUTABLE))):
        print('[FAIL] unsupported loop target/round contract');return 2
    loop_id=datetime.now(timezone(timedelta(hours=8))).strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:8]
    work=RUNS/f'loop-{loop_id}';work.mkdir(parents=True,exist_ok=False);history=[]
    for round_no in range(1,MAX_ROUNDS+1):
        run_id=uuid.uuid4().hex[:12];rec={'loop':loop_id,'round':round_no,'run_id':run_id,'started':datetime.now(timezone(timedelta(hours=8))).isoformat(),'config_sha256':_sha(Path(config.get('_config_path','')))}
        report=None
        try:
            if STOP_FILE.exists():rec['event']='stop_file';persist_round(work,rec);return 0
            ok,detail=gate_ready(run_id,config)
            if not ok:rec.update(event='gate_blocked',detail=detail);persist_round(work,rec);return 2
            rw=work/f'round-{round_no}';rw.mkdir(exist_ok=False)
            if STOP_FILE.exists():rec['event']='stop_file';persist_round(work,rec);return 0
            train=train_step(config,rw,run_id)
            if train['status']!='TRAINED':rec.update(event='train_blocked',detail=train);persist_round(work,rec);return 2
            training_path=rw/'training-manifest.json';training=json.loads(training_path.read_text('utf-8'))
            if training.get('status')!='TRAINED' or training.get('run_id')!=run_id or training.get('config_sha256')!=rec['config_sha256'] or training.get('manifest_sha256')!=_sha(project_path(config.get('dataset_manifest','data/manifest.json'))) or training.get('adapter_sha256')!=adapter_hash(rw/'adapter'):raise ValueError('training manifest/adapter binding missing or stale')
            rec['training_manifest_sha256']=_sha(training_path)
            if STOP_FILE.exists():rec['event']='stop_file';persist_round(work,rec);return 0
            ev=eval_step(config,rw,rw/'adapter',run_id)
            report_path=rw/'eval-report.json'
            if report_path.is_file():report=json.loads(report_path.read_text('utf-8'))
            if ev['status']!='OK':rec.update(event='eval_blocked',detail=ev);persist_round(work,rec,report if isinstance(report,dict) else None);return 2
            m=report_metrics(report,run_id,config,rw);history.append({'round':round_no,'metrics':m})
            verdict=decide(round_no,m,history);rec.update(event='round_complete',metrics=m,report=report_path.relative_to(work).as_posix(),report_sha256=_sha(report_path),final_verdict=verdict)
            persist_round(work,rec,report)
            print(f'[loop] round={round_no}, metrics={m}, decision={verdict}')
            if verdict!='continue':return 0
        except (OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError) as exc:
            rec.update(event='round_failed',detail=type(exc).__name__+': '+str(exc))
            try:persist_round(work,rec,report if isinstance(report,dict) else None)
            except (OSError,ValueError,TypeError) as evidence_error:print('[FAIL] evidence could not be completely persisted: '+str(evidence_error))
            print('[FAIL] '+rec['detail']);return 2
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
