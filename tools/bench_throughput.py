"""实测本机训练/生成吞吐:QLoRA 步时 + 生成 tok/s(喂给周期估算)。

只做计时基准,不写任何训练产物,不触碰数据门禁。
"""
from __future__ import annotations
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]


def bench() -> None:
    import torch
    from transformers import (AutoModelForCausalLM, AutoTokenizer,
                              BitsAndBytesConfig)
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

    model_dir = ROOT / ".models/qwen3-4b"
    tok = AutoTokenizer.from_pretrained(str(model_dir))
    tok.pad_token = tok.pad_token or tok.eos_token
    print("加载 4-bit 模型…", flush=True)
    t0 = time.time()
    bnb = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                             bnb_4bit_compute_dtype=torch.bfloat16,
                             bnb_4bit_use_double_quant=True)
    model = AutoModelForCausalLM.from_pretrained(
        str(model_dir), quantization_config=bnb, torch_dtype=torch.bfloat16,
        device_map="auto")
    print(f"模型加载 {time.time()-t0:.0f}s,显存 "
          f"{torch.cuda.max_memory_allocated()/2**30:.2f}GiB", flush=True)

    model.gradient_checkpointing_enable()
    model = prepare_model_for_kbit_training(model)
    model = get_peft_model(model, LoraConfig(
        r=8, lora_alpha=16, lora_dropout=0.05, bias="none",
        task_type="CAUSAL_LM", target_modules="all-linear"))
    model.print_trainable_parameters()

    # 训练步时:batch2 × ~600 token(与真实训练分布一致)
    prompt = ("你是数学动画规划师。" + "题目:求矩阵的特征值。" * 40)
    ids = tok.encode(prompt)[:600]
    batch = {"input_ids": torch.tensor([ids, ids], device="cuda"),
             "attention_mask": torch.ones(2, len(ids), device="cuda",
                                          dtype=torch.long),
             "labels": torch.tensor([ids, ids], device="cuda")}
    opt = torch.optim.AdamW(model.parameters(), lr=2e-4)
    model.train()
    for _ in range(2):  # 预热
        opt.zero_grad()
        loss = model(**batch).loss
        loss.backward()
        opt.step()
    torch.cuda.synchronize()
    t0 = time.time()
    steps = 6
    for _ in range(steps):
        opt.zero_grad()
        loss = model(**batch).loss
        loss.backward()
        opt.step()
    torch.cuda.synchronize()
    s_per_step = (time.time() - t0) / steps
    print(f"训练: {s_per_step:.2f}s/步,峰值显存 "
          f"{torch.cuda.max_memory_allocated()/2**30:.2f}GiB", flush=True)

    # 生成 tok/s:真实分布 prompt + 256 token
    model.eval()
    with torch.no_grad():
        inp = tok.apply_chat_template(
            [{"role": "user", "content": "题目:求级数 ∑1/n² 的和。解法:巴塞尔问题。请输出动画规划 JSON。"}],
            tokenize=True, add_generation_prompt=True,
            enable_thinking=False, return_tensors="pt").to("cuda")
        t0 = time.time()
        out = model.generate(**inp, max_new_tokens=256, do_sample=False)
        torch.cuda.synchronize()
        n_new = out.shape[1] - inp["input_ids"].shape[1]
        print(f"生成: {n_new / (time.time() - t0):.1f} tok/s", flush=True)
    print("BENCH_DONE", flush=True)


if __name__ == "__main__":
    bench()
