"""模型筛选:QLoRA 训练探针(测量,不正式训练)。

4bit 加载 + LoRA 配置 + 若干训练步(固定小样本),实测:
峰值显存(batch=1 前向/反向)、步时、checkpoint 体积、断点恢复可行性。
run_id=screening-*;产物写入 outputs/screening-tmp/qlora-probes/(临时实验组)。

用法:
  python tools/screening_qlora_probe.py --model-dir .models/qwen2.5-7b-instruct \
      --tag qwen2.5-7b [--steps 3] [--seq-len 1024]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--steps", type=int, default=3)
    ap.add_argument("--seq-len", type=int, default=1024)
    args = ap.parse_args(argv)

    import torch  # noqa: PLC0415
    from transformers import (  # noqa: PLC0415
        AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig)
    from peft import LoraConfig, get_peft_model  # noqa: PLC0415

    load_start = time.time()
    quant = BitsAndBytesConfig(load_in_4bit=True,
                               bnb_4bit_compute_dtype=torch.bfloat16,
                               bnb_4bit_quant_type="nf4")
    tok = AutoTokenizer.from_pretrained(args.model_dir, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(
        args.model_dir, quantization_config=quant, device_map="auto",
        torch_dtype=torch.bfloat16, trust_remote_code=False)
    model.gradient_checkpointing_enable()
    model.enable_input_require_grads()
    lora = LoraConfig(r=8, lora_alpha=16, lora_dropout=0.05,
                      bias="none", task_type="CAUSAL_LM",
                      target_modules=["q_proj", "k_proj", "v_proj", "o_proj"])
    peft_model = get_peft_model(model, lora)
    load_sec = time.time() - load_start
    load_vram = torch.cuda.max_memory_allocated() / 1e9
    torch.cuda.reset_peak_memory_stats()

    # 合成输入(固定 token,非真实数据;仅测资源)
    prompt_ids = tok("数学动画规划 " * (args.seq_len // 6),
                     return_tensors="pt").to(model.device)
    labels = prompt_ids["input_ids"].clone()
    optimizer = torch.optim.AdamW(peft_model.parameters(), lr=2e-4)

    step_times = []
    for step in range(args.steps):
        t0 = time.time()
        peft_model.train()
        out = peft_model(input_ids=prompt_ids["input_ids"], labels=labels)
        out.loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        torch.cuda.synchronize()
        step_times.append(time.time() - t0)
        print(f"[step {step + 1}/{args.steps}] {step_times[-1]:.1f}s "
              f"loss={out.loss.item():.3f} "
              f"peak={torch.cuda.max_memory_allocated() / 1e9:.2f}GB")
    peak = torch.cuda.max_memory_allocated() / 1e9

    # checkpoint 体积(只存 adapter)
    out_dir = ROOT / "outputs/screening-tmp/qlora-probes"
    out_dir.mkdir(parents=True, exist_ok=True)
    ckpt_dir = out_dir / f"{args.tag}-ckpt"
    peft_model.save_pretrained(ckpt_dir)
    ckpt_bytes = sum(p.stat().st_size for p in ckpt_dir.rglob("*") if p.is_file())

    summary = {"tag": args.tag, "run_id": f"screening-{args.tag}",
               "steps": args.steps, "seq_len": args.seq_len,
               "load_sec": round(load_sec, 1), "load_vram_gb": round(load_vram, 2),
               "train_peak_vram_gb": round(peak, 2),
               "step_sec_mean": round(sum(step_times) / len(step_times), 2),
               "step_sec_list": [round(x, 2) for x in step_times],
               "adapter_ckpt_bytes": ckpt_bytes,
               "loss_last": round(out.loss.item(), 4),
               "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")}
    (out_dir / f"{args.tag}.summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
