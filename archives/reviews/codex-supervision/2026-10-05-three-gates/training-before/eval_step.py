"""四指标评测器(按题计):渲染成功率 / 可执行率 / 数学正确率 / 画面忠实度。

设计契约见 docs/TRAINING-LOOP-DESIGN.md。诚实原则:
- schema(可执行率)与渲染(渲染成功率)有真实验收器;
- 数学正确率/画面忠实度依赖独立判定器(judge_script),未接线时如实
  UNVERIFIED,不伪造指标;
- eval/test 题文只用于评测,绝不写入训练。

用法:
  <venv>/Scripts/python.exe -X utf8 tools/eval_step.py --config <rounds.json>
      --work <runs/loop-xxx/round-n> --adapter <adapter-dir> --run-id <id>
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

GEN_PROMPT = (
    "你是数学动画规划师。根据题目与解法,输出动画规划 JSON(scene_spec),"
    "格式:{\"objects\": [\"...\"], \"steps\": [\"...\"]}。\n"
    "要求:objects/steps 均为非空字符串列表;公式用 $...$ 包裹;"
    "steps 覆盖解法全部关键推理步骤;只输出 JSON,不要解释。\n"
    "题目:{problem}\n解法({method}):{solution}\n")


def load_eval_rows(manifest: Path) -> list[dict]:
    m = json.loads(manifest.read_text(encoding="utf-8"))
    rows = []
    for e in m["entries"]:
        if e["split"] not in ("eval", "test"):
            continue
        p = (manifest.parent / e["path"]).resolve()
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows


def schema_ok(spec: dict) -> bool:
    """可执行率分量:scene_spec 满足入场契约的 objects/steps 要求。"""
    if not isinstance(spec, dict):
        return False
    for key in ("objects", "steps"):
        v = spec.get(key)
        if not isinstance(v, list) or not v:
            return False
        if any(not isinstance(x, str) or not x.strip() for x in v):
            return False
    return True


def generate(adapter: Path, model_dir: Path, rows: list[dict],
             work: Path, hp: dict) -> list[dict]:
    """逐题生成 scene_spec(本地 4-bit 推理)。"""
    import torch  # noqa: PLC0415
    from transformers import AutoModelForCausalLM, AutoTokenizer  # noqa: PLC0415
    from transformers import BitsAndBytesConfig  # noqa: PLC0415
    from peft import PeftModel  # noqa: PLC0415

    tok = AutoTokenizer.from_pretrained(str(adapter))
    tok.pad_token = tok.pad_token or tok.eos_token
    quant = hp.get("quantization", "4bit").lower()
    bnb_cfg = BitsAndBytesConfig(load_in_4bit=quant in ("4bit", "nf4", "4-bit"),
                                 bnb_4bit_quant_type="nf4",
                                 bnb_4bit_compute_dtype=torch.bfloat16,
                                 bnb_4bit_use_double_quant=True)
    model = AutoModelForCausalLM.from_pretrained(
        str(model_dir), quantization_config=bnb_cfg,
        torch_dtype=torch.bfloat16, device_map="auto")
    model = PeftModel.from_pretrained(model, str(adapter))
    model.eval()
    results = []
    for i, r in enumerate(rows):
        prompt = GEN_PROMPT.format(problem=r.get("problem", ""),
                                   solution=r.get("solution", ""),
                                   method=r.get("method", "常规解法"))
        inputs = tok(prompt, return_tensors="pt").to(model.device)
        with torch.no_grad():
            out = model.generate(**inputs, max_new_tokens=1024,
                                 do_sample=False)
        text = tok.decode(out[0][inputs["input_ids"].shape[1]:],
                          skip_special_tokens=True).strip()
        try:
            spec = json.loads(text)
        except json.JSONDecodeError:
            spec = {"_raw": text[:200]}
        results.append({"row_index": i,
                        "problem_id": r.get("problem_id") or r.get("id"),
                        "split": "eval" if "problem_id" in r else "test",
                        "spec": spec, "schema_ok": schema_ok(spec),
                        "raw_len": len(text)})
        if (i + 1) % 50 == 0:
            print(f"[eval] 已生成 {i + 1}/{len(rows)}")
    return results


def render_check(config: dict, work: Path, results: list[dict]) -> dict:
    """渲染成功率:render_executor 未接线时如实 UNVERIFIED。"""
    exe = config.get("render_executor")
    if not exe:
        return {"status": "UNVERIFIED",
                "reason": "渲染执行器未接线(生产渲染链验收后配置 render_executor),"
                          "渲染成功率如实 UNVERIFIED,不伪造"}
    cp = subprocess.run([sys.executable, "-X", "utf8", str(ROOT / exe),
                         "--specs", str(work / "generated-specs.json")],
                        capture_output=True, timeout=3600 * 4)
    return {"status": "OK" if cp.returncode == 0 else "FAILED",
            "rc": cp.returncode,
            "detail": (cp.stdout or b"").decode("utf-8", "replace")[:200]}


def judge(config: dict, work: Path, results: list[dict]) -> dict:
    """数学正确率/画面忠实度:judge_script 未接线时如实 UNVERIFIED。"""
    j = config.get("judge_script")
    if not j:
        return {"status": "UNVERIFIED",
                "reason": "独立判定器未接线(judge_script),"
                          "数学/忠实度如实 UNVERIFIED,不伪造"}
    cp = subprocess.run([sys.executable, "-X", "utf8", str(ROOT / j),
                         "--specs", str(work / "generated-specs.json")],
                        capture_output=True, timeout=3600 * 4)
    return {"status": "OK" if cp.returncode == 0 else "FAILED",
            "rc": cp.returncode,
            "detail": (cp.stdout or b"").decode("utf-8", "replace")[:200]}


def aggregate(results: list[dict], render: dict, judge: dict) -> dict:
    n = len(results)
    total = n or 1
    return {
        "total_questions": n,
        "render": {"rate": None, "detail": render["reason"]}
        if render["status"] == "UNVERIFIED" else render,
        "executable": {"rate": round(sum(1 for r in results
                                         if r["schema_ok"]) / total, 4),
                       "passed": sum(1 for r in results if r["schema_ok"]),
                       "total": n},
        "math": {"rate": None, "detail": judge["reason"]}
        if judge["status"] == "UNVERIFIED" else judge,
        "fidelity": {"rate": None, "detail": judge["reason"]}
        if judge["status"] == "UNVERIFIED" else judge,
        "failures": [{"problem_id": r["problem_id"], "row_index": r["row_index"],
                      "raw": r["spec"].get("_raw", "")[:120]}
                     for r in results if not r["schema_ok"]][:20]}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--adapter", type=Path, required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--subset", type=Path, default=None,
                    help="可选:只评测 JSON 列表中的 problem_id(扫参用固定子集)")
    args = ap.parse_args(argv)
    return run(args.config, args.work, args.adapter, args.run_id, args.subset)


def run(config_path: Path, work: Path, adapter: Path, run_id: str,
        subset: Path | None = None) -> int:
    """可复用入口:扫参器直接调用;subset 只过滤评测行,不进入训练。"""
    config = json.loads(config_path.read_text(encoding="utf-8"))
    hp = config.get("hyperparameters") or {}
    if hp.get("quantization") is None:
        print("[FAIL] 量化方案未定案,评测步拒绝执行(fail-closed)")
        return 2
    work.mkdir(parents=True, exist_ok=True)
    manifest = Path(config.get("dataset_manifest",
                               str(ROOT / "data/manifest.json")))
    model_dir = Path(config.get("model_path", str(ROOT / ".models/qwen3-4b")))
    rows = load_eval_rows(manifest)
    if subset is not None:
        keep = json.loads(subset.read_text(encoding="utf-8"))
        if not isinstance(keep, list):
            print("[FAIL] --subset 必须为 problem_id 列表")
            return 2
        rows = [r for r in rows
                if (r.get("problem_id") or r.get("id")) in set(keep)]
        if not rows:
            print("[FAIL] 子集过滤后为空")
            return 2
    results = generate(adapter, model_dir, rows, work, hp)
    (work / "generated-specs.json").write_text(
        json.dumps([{"problem_id": r["problem_id"], "split": r["split"],
                     "spec": r["spec"], "schema_ok": r["schema_ok"],
                     "raw_len": r["raw_len"]} for r in results],
                   ensure_ascii=False, indent=2), encoding="utf-8")
    render = render_check(config, work, results)
    judge = judge(config, work, results)
    summary = aggregate(results, render, judge)
    summary["run_id"] = run_id
    (work / "eval-report.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
