"""任务可学性闭环探针:Qwen3-4B 对 v2/test 抽样生成 scene_spec。

目的(数据前置第 0 步):scene_spec schema 是我们设计的,从未被模型消费过。
本探针回答:模型能否稳定输出该 JSON 格式、objects/steps 粒度是否合理、
常见失败模式是什么 —— 人工评审产物 outputs/data-probe/<run>/review.md。

只读探针:不训练、不改数据;样本冻结 sample_manifest;复用 screening_probe
的解析口径(think/final 分离、严格/宽松解析、spec 结构检查)。
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))

from screening_probe import (  # noqa: E402  复用筛选口径
    SYSTEM, USER_TMPL, check_spec, extract_scene_spec, input_hash,
    split_think_final)

TEST_JSONL = ROOT / "data" / "v2" / "test" / "dataset_test.jsonl"
OUT_BASE = ROOT / "outputs" / "data-probe"
QUOTA = {"数学分析": 4, "解析几何": 4, "概率论": 4, "高等代数": 4,
         "跨学科": 4}          # 5 类 × 4 = 20 条
MODEL_DIR = ROOT / ".models" / "qwen3-4b"


def select_samples() -> list[dict]:
    by_cat: dict[str, dict[str, dict]] = {}
    for line in TEST_JSONL.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        cat = obj.get("category")
        if cat in QUOTA:
            sub = obj.get("sub_category") or "未分类"
            by_cat.setdefault(cat, {}).setdefault(sub, obj)
    picked: list[dict] = []
    for cat, quota in QUOTA.items():
        subs = list(by_cat.get(cat, {}).values())
        if len(subs) < quota:
            raise SystemExit(f"[FAIL] {cat} 子类覆盖不足({len(subs)}<{quota})")
        picked += subs[:quota]
    return picked


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-new-tokens", type=int, default=1024)
    ap.add_argument("--max-retries", type=int, default=6,
                    help="严格解析失败时带修正指令+温度采样的重试上限(目标 100% 严格)")
    ap.add_argument("--thinking", type=bool, default=True,
                    help="思考模式(筛选最佳口径 80% 严格解析率)")
    args = ap.parse_args(argv)

    import torch  # noqa: PLC0415
    from transformers import (  # noqa: PLC0415
        AutoModelForCausalLM, AutoTokenizer, GenerationConfig, set_seed)

    run_dir = OUT_BASE / time.strftime("run-%Y%m%d-%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)
    samples = select_samples()
    manifest = {"n": len(samples),
                "items": [{"id": s["id"], "category": s["category"],
                           "sub_category": s["sub_category"],
                           "input_sha256": input_hash(s)} for s in samples]}
    (run_dir / "sample_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    tok = AutoTokenizer.from_pretrained(str(MODEL_DIR))
    model = AutoModelForCausalLM.from_pretrained(
        str(MODEL_DIR), torch_dtype=torch.bfloat16,
        quantization_config={"load_in_4bit": True,
                             "bnb_4bit_compute_dtype": torch.bfloat16,
                             "bnb_4bit_quant_type": "nf4"},
        device_map="auto")
    set_seed(42)
    gen_cfg = GenerationConfig(max_new_tokens=args.max_new_tokens,
                               do_sample=False)
    gen_cfg_retry = GenerationConfig(max_new_tokens=args.max_new_tokens,
                                     do_sample=True, temperature=0.7,
                                     top_p=0.9)
    _FIXUP = ("注意:输出必须是完整合法的 JSON 对象;JSON 字符串内的 LaTeX "
              "命令必须用双反斜杠转义(如 \\\\frac、\\\\int),不得出现单个 "
              "反斜杠加字母;不要提前结束,必须输出完整闭合的 JSON。")

    def _generate(msgs: list[dict], retry: bool) -> tuple[str, str, bool]:
        try:
            prompt = tok.apply_chat_template(
                msgs, tokenize=False, add_generation_prompt=True,
                enable_thinking=args.thinking)
        except TypeError:
            prompt = tok.apply_chat_template(msgs, tokenize=False,
                                             add_generation_prompt=True)
        inputs = tok(prompt, return_tensors="pt").to(model.device)
        cfg = gen_cfg_retry if retry else gen_cfg
        out = model.generate(**inputs, generation_config=cfg)
        text = tok.decode(out[0][inputs["input_ids"].shape[1]:],
                          skip_special_tokens=True)
        return split_think_final(text)

    results = []
    for s in samples:
        base = [{"role": "system", "content": SYSTEM},
                {"role": "user", "content": USER_TMPL.format(
                    problem=s["problem"], solution=s["solution"])}]
        attempts = 0
        rec = None
        for attempt in range(1 + args.max_retries):
            attempts = attempt + 1
            msgs = base if attempt == 0 else base + [
                {"role": "user", "content": _FIXUP}]
            think, final, truncated = _generate(msgs, retry=attempt > 0)
            spec, strict = extract_scene_spec(final)
            problems = check_spec(spec) if spec else ["spec 缺失"]
            if strict and not problems:
                rec = {"id": s["id"], "category": s["category"],
                       "sub_category": s["sub_category"],
                       "problem": s["problem"], "solution": s["solution"],
                       "raw_output": final, "think": think, "final": final,
                       "truncated": truncated, "strict": True,
                       "lenient": True, "scene_spec": spec,
                       "spec_problems": [], "attempts": attempts}
                break
            rec = {"id": s["id"], "category": s["category"],
                   "sub_category": s["sub_category"],
                   "problem": s["problem"], "solution": s["solution"],
                   "raw_output": final, "think": think, "final": final,
                   "truncated": truncated, "strict": strict,
                   "lenient": spec is not None,
                   "scene_spec": spec, "spec_problems": problems,
                   "attempts": attempts}
        results.append(rec)
        (run_dir / "samples.json").write_text(
            json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[{len(results)}/{len(samples)}] {s['id']} "
              f"strict={rec['strict']} attempts={rec['attempts']}")
    n = len(results)
    strict = sum(r["strict"] for r in results)
    first_try = sum(r["attempts"] == 1 and r["strict"] for r in results)
    summary = {"run_dir": str(run_dir), "n": n, "strict_rate": strict / n,
               "first_try_strict_rate": first_try / n,
               "attempts_total": sum(r["attempts"] for r in results),
               "max_attempts": max(r["attempts"] for r in results),
               "truncated": sum(r["truncated"] for r in results)}
    (run_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    # 人工评审产物
    lines = ["# scene_spec 任务可学性探针 · 人工评审稿", "",
             f"> run: {run_dir.name};样本 20 条(v2/test 分层,输入哈希冻结);"
             f"模型 Qwen3-4B 4bit 思考模式;严格解析率 "
             f"{summary['strict_rate']:.0%},宽松 {summary['lenient_rate']:.0%}。",
             "", "评审问题:格式是否稳定?objects/steps 粒度是否合理?"
             "生成内容与题目/解答是否对应?", ""]
    for r in results:
        lines += [f"## {r['id']} · {r['category']}/{r['sub_category']}",
                  f"**题目** {r['problem']}", f"**解答** {r['solution']}",
                  f"**模型 scene_spec**(strict={r['strict']},问题={r['spec_problems'] or '无'}):",
                  "```json", json.dumps(r["scene_spec"], ensure_ascii=False,
                                        indent=1) if r["scene_spec"] else "(null)",
                  "```", ""]
    (run_dir / "review.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"评审稿 → {run_dir / 'review.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
