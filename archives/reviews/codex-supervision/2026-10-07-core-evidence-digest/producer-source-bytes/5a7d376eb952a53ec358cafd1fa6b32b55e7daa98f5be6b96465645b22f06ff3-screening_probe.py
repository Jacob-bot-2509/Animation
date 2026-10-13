"""模型筛选:推理对照探针(仅推理,不训练)。

三款候选同口径实测:20 条分层抽样(problem+solution → scene_spec JSON),
指标:JSON 可解析率、字段合规、延迟、加载/推理峰值显存、生成 token 数。
产物写入 outputs/screening-tmp/inference/(临时实验组,筛选后撤走)。

用法:
  python tools/screening_probe.py --model-dir .models/qwen2.5-7b-instruct \
      --tag qwen2.5-7b [--max-new-tokens 1024] [--thinking]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

SAMPLES = {"数学分析": 6, "概率论": 5, "解析几何": 4, "高等代数": 5}

SYSTEM = ("你是数学动画教学规划助手。根据数学题目与解答,输出动画规划 JSON。"
          "只输出 JSON 本身,不要任何解释或代码块标记。")
USER_TMPL = ("请为下面的题目规划动画场景。输出格式:\n"
             '{{"scene_spec": {{"objects": ["视觉元素1", "..."], '
             '"steps": ["第一步：...", "..."]}}}}\n'
             "要求:objects 列出动画需要的全部视觉元素(坐标轴、曲线、标注等);"
             "steps 用 第一步/第二步… 分步描述动画过程;全部中文,"
             "数学公式用 $...$ 包起来。\n"
             "题目: {problem}\n"
             "解答: {solution}\n")


def load_samples() -> list[dict]:
    out: list[dict] = []
    by_cat: dict[str, list[dict]] = {}
    for f in sorted((ROOT / "data/v1/raw").glob("dataset_*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            obj = json.loads(line)
            if obj.get("category") in SAMPLES:
                by_cat.setdefault(obj["category"], []).append(obj)
    for cat, n in SAMPLES.items():
        picks = by_cat.get(cat, [])[:n]
        out += picks
    return out


def extract_scene_spec(text: str) -> dict | None:
    """从生成文本中提取 scene_spec JSON(容忍围栏与前后杂讯)。"""
    t = text.strip()
    start, end = t.find("{"), t.rfind("}")
    if start < 0 or end <= start:
        return None
    try:
        obj = json.loads(t[start:end + 1])
    except json.JSONDecodeError:
        # 去掉 markdown 围栏再试
        for marker in ("```json", "```"):
            t2 = t.replace(marker, "")
        s2, e2 = t2.find("{"), t2.rfind("}")
        if s2 < 0 or e2 <= s2:
            return None
        try:
            obj = json.loads(t2[s2:e2 + 1])
        except json.JSONDecodeError:
            return None
    spec = obj.get("scene_spec", obj) if isinstance(obj, dict) else None
    if not isinstance(spec, dict):
        return None
    return spec


def check_spec(spec: dict) -> list[str]:
    problems = []
    for key in ("objects", "steps"):
        v = spec.get(key)
        if not isinstance(v, list) or not v:
            problems.append(f"{key} 缺失/空/非列表")
        elif any(not isinstance(x, str) or not x.strip() for x in v):
            problems.append(f"{key} 含非字符串元素")
    return problems


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", required=True)
    ap.add_argument("--tag", required=True, help="结果标记(如 qwen3-4b)")
    ap.add_argument("--max-new-tokens", type=int, default=1024)
    ap.add_argument("--thinking", action="store_true",
                    help="Qwen3 启用 thinking 模式(默认非 thinking)")
    args = ap.parse_args(argv)

    samples = load_samples()
    print(f"样本 {len(samples)} 条(分层抽样)")

    import torch  # noqa: PLC0415 依赖安装后可用
    from transformers import (  # noqa: PLC0415
        AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig)

    load_start = time.time()
    quant = BitsAndBytesConfig(load_in_4bit=True,
                               bnb_4bit_compute_dtype=torch.bfloat16,
                               bnb_4bit_quant_type="nf4")
    tok = AutoTokenizer.from_pretrained(args.model_dir, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(
        args.model_dir, quantization_config=quant, device_map="auto",
        torch_dtype=torch.bfloat16, trust_remote_code=False)
    load_sec = time.time() - load_start
    vram = torch.cuda.max_memory_allocated() / 1e9
    torch.cuda.reset_peak_memory_stats()

    results = []
    for i, s in enumerate(samples):
        user = USER_TMPL.format(problem=s["problem"], solution=s["solution"])
        if args.thinking:
            user = "/think\n" + user
        else:
            user = "/no_think\n" + user
        msgs = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": user}]
        prompt = tok.apply_chat_template(msgs, tokenize=False,
                                         add_generation_prompt=True)
        inputs = tok(prompt, return_tensors="pt").to(model.device)
        t0 = time.time()
        with torch.no_grad():
            gen = model.generate(**inputs, max_new_tokens=args.max_new_tokens,
                                 do_sample=True, temperature=0.7,
                                 top_p=0.9, pad_token_id=tok.eos_token_id)
        gen_sec = time.time() - t0
        text = tok.decode(gen[0][inputs["input_ids"].shape[1]:],
                          skip_special_tokens=True)
        spec = extract_scene_spec(text)
        spec_problems = check_spec(spec) if spec else ["不可解析"]
        results.append({"id": s.get("id"), "category": s.get("category"),
                        "parsed": spec is not None,
                        "spec_problems": spec_problems,
                        "gen_sec": round(gen_sec, 2),
                        "n_gen_tokens": int(gen.shape[1] - inputs["input_ids"].shape[1]),
                        "output_preview": text[:200]})
        print(f"[{i + 1}/{len(samples)}] {s['id']} parsed={spec is not None} "
              f"{gen_sec:.1f}s tokens={results[-1]['n_gen_tokens']}")

    parsed_n = sum(1 for r in results if r["parsed"])
    clean_n = sum(1 for r in results if r["parsed"] and not r["spec_problems"])
    total_tok = sum(r["n_gen_tokens"] for r in results)
    total_sec = sum(r["gen_sec"] for r in results)
    peak = torch.cuda.max_memory_allocated() / 1e9
    summary = {"tag": args.tag, "model_dir": args.model_dir,
               "thinking": args.thinking, "n_samples": len(samples),
               "parsed": parsed_n, "parsed_rate": round(parsed_n / len(samples), 4),
               "clean": clean_n, "clean_rate": round(clean_n / len(samples), 4),
               "load_sec": round(load_sec, 1), "total_gen_sec": round(total_sec, 1),
               "total_gen_tokens": total_tok,
               "tok_per_sec": round(total_tok / total_sec, 2) if total_sec else 0,
               "load_vram_gb": round(vram, 2), "infer_peak_vram_gb": round(peak, 2),
               "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")}
    out_dir = ROOT / "outputs/screening-tmp/inference"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{args.tag}{'-thinking' if args.thinking else ''}.jsonl").write_text(
        "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in results),
        encoding="utf-8")
    (out_dir / f"{args.tag}{'-thinking' if args.thinking else ''}.summary.json") \
        .write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
