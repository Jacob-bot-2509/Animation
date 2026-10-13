"""模型筛选:推理对照探针(msg_225 口径修正,仅推理不训练)。

同口径要点:显式 set_seed;显式冻结 GenerationConfig(三模型一致,
含 repetition_penalty=1.0);thinking 与 final 按 token 分离解析,
截断/未闭合不计成功;严格 JSON 合规与宽松提取分开计;样本按子类分层
并冻结 20 条 ID+输入哈希(不足/变更拒绝);CUDA 同步计时、冷/热分计、
allocated/reserved 与 device_map 如实记录、CPU 回退不冒充 GPU 结果;
每样本失败单独留记录;产物按 tag/run-时间戳 唯一目录,不可覆盖。

用法:
  python tools/screening_probe.py --model-dir .models/qwen2.5-7b-instruct \
      --tag qwen2.5-7b [--max-new-tokens 1024] [--thinking]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.fs_guard import valid_run_id  # noqa: E402

SAMPLES = {"数学分析": 6, "概率论": 5, "解析几何": 4, "高等代数": 5}
SAMPLE_MANIFEST = ROOT / "outputs/screening-tmp/sample_manifest.json"

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


def input_hash(sample: dict) -> str:
    return hashlib.sha256(
        json.dumps({"problem": sample["problem"],
                    "solution": sample["solution"]},
                   ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()


def select_samples() -> list[dict]:
    """子类分层抽样:每 category 按 distinct sub_category 轮转取,不足配额拒绝;
    选样冻结到 sample_manifest(20 条 ID+输入哈希),复跑必须一致。"""
    by_cat: dict[str, dict[str, dict]] = {}
    for f in sorted((ROOT / "data/v1/raw").glob("dataset_*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            obj = json.loads(line)
            cat = obj.get("category")
            if cat in SAMPLES:
                sub = obj.get("sub_category") or "未分类"
                by_cat.setdefault(cat, {}).setdefault(sub, obj)
    picked: list[dict] = []
    for cat, quota in SAMPLES.items():
        subs = list(by_cat.get(cat, {}).values())
        if len(subs) < quota:
            raise SystemExit(f"[FAIL] {cat} 子类覆盖不足({len(subs)}<{quota})"
                             "—— 抽样必须覆盖子类,不足拒绝")
        picked += subs[:quota]
    manifest = {"n": len(picked),
                "items": [{"id": s.get("id"), "category": s.get("category"),
                           "sub_category": s.get("sub_category"),
                           "input_sha256": input_hash(s)} for s in picked]}
    if SAMPLE_MANIFEST.exists():
        old = json.loads(SAMPLE_MANIFEST.read_text(encoding="utf-8"))
        if old.get("items") != manifest["items"]:
            raise SystemExit("[FAIL] 样本清单与已冻结的 sample_manifest 不一致"
                             "—— 对照口径已冻结,变更须先更新清单(勿静默换样本)")
    else:
        SAMPLE_MANIFEST.parent.mkdir(parents=True, exist_ok=True)
        SAMPLE_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False,
                                              indent=2), encoding="utf-8")
    return picked


def split_think_final(text: str) -> tuple[str, str, bool]:
    """按 <think>…</think> 分离;未闭合 think → (think, final, truncated=True)。"""
    start = text.find("<think>")
    if start < 0:
        return "", text, False
    end = text.find("</think>", start)
    if end < 0:
        return text[start + len("<think>"):], "", True  # 未闭合:截断
    return text[start + len("<think>"):end], text[end + len("</think>"):], False


def extract_scene_spec(final: str) -> tuple[dict | None, bool]:
    """严格:final 去掉空白后整体是一个 JSON 对象;宽松:从 { 到 } 提取。
    返回 (spec, strict)。"""
    t = final.strip()
    try:
        obj = json.loads(t)
        spec = obj.get("scene_spec", obj) if isinstance(obj, dict) else None
        return (spec if isinstance(spec, dict) else None), True
    except json.JSONDecodeError:
        pass
    s, e = t.find("{"), t.rfind("}")
    if s < 0 or e <= s:
        return None, False
    try:
        obj = json.loads(t[s:e + 1])
    except json.JSONDecodeError:
        return None, False
    spec = obj.get("scene_spec", obj) if isinstance(obj, dict) else None
    return (spec if isinstance(spec, dict) else None), False


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
    ap.add_argument("--tag", required=True, help="结果标记(仅 [A-Za-z0-9_-])")
    ap.add_argument("--max-new-tokens", type=int, default=1024)
    ap.add_argument("--thinking", action="store_true")
    args = ap.parse_args(argv)
    if not valid_run_id(args.tag):
        print(f"[FAIL] tag 非法: {args.tag!r}(只允许 [A-Za-z0-9_-] 1-64)")
        return 1

    samples = select_samples()
    print(f"样本 {len(samples)} 条(子类分层,清单已冻结)")

    import torch  # noqa: PLC0415
    from transformers import (  # noqa: PLC0415
        AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig,
        GenerationConfig, set_seed)

    torch.manual_seed(0)
    set_seed(0)
    gpu_ok = torch.cuda.is_available()
    quant = BitsAndBytesConfig(load_in_4bit=True,
                               bnb_4bit_compute_dtype=torch.bfloat16,
                               bnb_4bit_quant_type="nf4")
    load_start = time.time()
    tok = AutoTokenizer.from_pretrained(args.model_dir, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(
        args.model_dir, quantization_config=quant, device_map="auto",
        torch_dtype=torch.bfloat16, trust_remote_code=False)
    load_sec = time.time() - load_start
    device_map = getattr(model, "hf_device_map", None) or {}
    on_gpu = gpu_ok and any("cuda" in str(v) for v in device_map.values())
    load_vram = (torch.cuda.max_memory_allocated() / 1e9) if gpu_ok else 0.0
    # 显式冻结生成口径:三模型一致(覆盖各自本地 generation_config 差异)
    gen_cfg = GenerationConfig(max_new_tokens=args.max_new_tokens,
                               do_sample=True, temperature=0.7, top_p=0.9,
                               repetition_penalty=1.0,
                               pad_token_id=tok.eos_token_id)
    gen_cfg_dict = gen_cfg.to_dict()

    run_dir = (ROOT / "outputs/screening-tmp/inference" / args.tag
               / f"run-{time.strftime('%Y%m%d-%H%M%S')}")
    run_dir.mkdir(parents=True, exist_ok=True)
    results = []
    for i, s in enumerate(samples):
        rec = {"id": s.get("id"), "category": s.get("category"),
               "sub_category": s.get("sub_category"),
               "input_sha256": input_hash(s),
               "prompt_problem": s["problem"], "prompt_solution": s["solution"]}
        try:
            user = USER_TMPL.format(problem=s["problem"], solution=s["solution"])
            if not args.thinking:
                user = "/no_think\n" + user
            msgs = [{"role": "system", "content": SYSTEM},
                    {"role": "user", "content": user}]
            prompt = tok.apply_chat_template(msgs, tokenize=False,
                                             add_generation_prompt=True)
            rec["prompt"] = prompt
            inputs = tok(prompt, return_tensors="pt").to(model.device)
            if gpu_ok:
                torch.cuda.synchronize()
            t0 = time.time()
            with torch.no_grad():
                try:
                    gen = model.generate(**inputs, generation_config=gen_cfg,
                                         enable_thinking=args.thinking)
                    thinking_mode = "kwarg"
                except TypeError:
                    # 模型不支持 enable_thinking 参数 → 回退软开关并如实记录
                    gen = model.generate(**inputs, generation_config=gen_cfg)
                    thinking_mode = "soft_switch_only"
            if gpu_ok:
                torch.cuda.synchronize()
            gen_sec = time.time() - t0
            text = tok.decode(gen[0][inputs["input_ids"].shape[1]:],
                              skip_special_tokens=True)
            think, final, truncated = split_think_final(text)
            spec, strict = extract_scene_spec(final)
            spec_problems = check_spec(spec) if spec else ["不可解析"]
            rec.update({"thinking_mode": thinking_mode,
                        "cold_start": i == 0, "gen_sec": round(gen_sec, 2),
                        "n_gen_tokens": int(gen.shape[1]
                                            - inputs["input_ids"].shape[1]),
                        "truncated_think": truncated,
                        "parsed_strict": strict and spec is not None,
                        "parsed_lenient": spec is not None,
                        "spec_problems": spec_problems,
                        "think_text": think[:2000], "final_text": final,
                        "full_output_sha256": hashlib.sha256(
                            text.encode("utf-8")).hexdigest(),
                        "allocated_gb": round(
                            torch.cuda.memory_allocated() / 1e9, 3) if gpu_ok else None,
                        "reserved_gb": round(
                            torch.cuda.memory_reserved() / 1e9, 3) if gpu_ok else None})
        except Exception as exc:  # noqa: BLE001 单样本失败留记录,不丢整轮
            rec.update({"error": repr(exc)[:500], "parsed_strict": False,
                        "parsed_lenient": False})
        results.append(rec)
        print(f"[{i + 1}/{len(samples)}] {s['id']} "
              f"strict={rec.get('parsed_strict')} "
              f"lenient={rec.get('parsed_lenient')} "
              f"{rec.get('gen_sec', 'err')}s")
        (run_dir / "results.jsonl").write_text(
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in results),
            encoding="utf-8")

    strict_n = sum(1 for r in results if r.get("parsed_strict"))
    lenient_n = sum(1 for r in results if r.get("parsed_lenient"))
    clean_n = sum(1 for r in results if r.get("parsed_lenient")
                  and not r.get("spec_problems"))
    err_n = sum(1 for r in results if "error" in r)
    warm = [r["gen_sec"] for r in results if "gen_sec" in r and not r["cold_start"]]
    summary = {"tag": args.tag, "model_dir": args.model_dir,
               "thinking": args.thinking, "n_samples": len(samples),
               "strict_rate": round(strict_n / len(samples), 4),
               "lenient_rate": round(lenient_n / len(samples), 4),
               "clean_lenient_rate": round(clean_n / len(samples), 4),
               "errors": err_n, "gpu_ok": gpu_ok, "on_gpu": on_gpu,
               "device_map_summary": {k: str(v)[:40] for k, v
                                      in list(device_map.items())[:4]},
               "load_sec": round(load_sec, 1), "load_vram_gb": round(load_vram, 2),
               "warm_gen_sec_mean": round(sum(warm) / len(warm), 2) if warm else 0,
               "cold_gen_sec": results[0].get("gen_sec") if results else None,
               "total_gen_tokens": sum(r.get("n_gen_tokens", 0) for r in results),
               "gen_config": gen_cfg_dict,
               "env": {"python": sys.version.split()[0],
                       "platform": platform.platform()},
               "command": " ".join(sys.argv),
               "provenance_sha256": hashlib.sha256(
                   Path(args.model_dir, "PROVENANCE.json").read_bytes()).hexdigest()
               if Path(args.model_dir, "PROVENANCE.json").exists() else "",
               "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")}
    (run_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
