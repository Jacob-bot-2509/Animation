"""模型筛选:QLoRA 训练资源探针(msg_225 口径修正)。

注意:本工具执行 backward+optimizer.step —— 属**用户已批准的筛选期资源探针**
(临时实验组,固定合成输入,不构成正式训练;dry-run 标签不等于训练授权)。

口径修正:精确 token 长度(裁剪到目标 token 数并记录 actual_seq_len,
不用文本重复估算);tag 校验;每 (tag, seq_len) 唯一 run 目录不可覆盖;
allocated/reserved 峰值与 device_map 如实记录;失败留记录;
结论注明"合成资源探针,不等于真实任务训练稳定性"。
"""
from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from animtrain.fs_guard import valid_run_id  # noqa: E402  (保留供 run_id)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--steps", type=int, default=3)
    ap.add_argument("--seq-len", type=int, default=1024)
    args = ap.parse_args(argv)
    if (not args.tag or len(args.tag) > 64 or args.tag in (".", "..")
            or "/" in args.tag or "\\" in args.tag or ":" in args.tag
            or any(ord(c) < 32 for c in args.tag)):
        print(f"[FAIL] tag 非法: {args.tag!r}(禁止路径分隔/.. /控制字符,≤64 字符)")
        return 1

    import torch  # noqa: PLC0415
    from transformers import (  # noqa: PLC0415
        AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig)
    from peft import LoraConfig, get_peft_model  # noqa: PLC0415

    torch.manual_seed(0)
    gpu_ok = torch.cuda.is_available()
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
    load_vram = (torch.cuda.max_memory_allocated() / 1e9) if gpu_ok else 0.0
    device_map = getattr(model, "hf_device_map", None) or {}

    # 精确 token 长度:编码长文本后裁剪到目标 token 数(msg_225:文本估算虚标)
    filler = tok("数学动画规划教学示例 " * 2000, return_tensors="pt")
    ids = filler["input_ids"][0][:args.seq_len]
    if ids.shape[0] < args.seq_len:
        print(f"[FAIL] 无法构造 {args.seq_len} token 的输入"
              f"(仅 {ids.shape[0]})")
        return 1
    actual_seq_len = int(ids.shape[0])
    prompt_ids = ids.unsqueeze(0).to(model.device)
    labels = prompt_ids.clone()
    optimizer = torch.optim.AdamW(peft_model.parameters(), lr=2e-4)

    run_dir = (ROOT / "outputs/screening-tmp/qlora-probes" / args.tag
               / f"seq-{args.seq_len}" / f"run-{time.strftime('%Y%m%d-%H%M%S')}")
    run_dir.mkdir(parents=True, exist_ok=True)
    step_records = []
    for step in range(args.steps):
        rec = {"step": step + 1}
        try:
            if gpu_ok:
                torch.cuda.synchronize()
            t0 = time.time()
            peft_model.train()
            out = peft_model(input_ids=prompt_ids, labels=labels)
            out.loss.backward()
            optimizer.step()
            optimizer.zero_grad()
            if gpu_ok:
                torch.cuda.synchronize()
            rec.update({"sec": round(time.time() - t0, 2),
                        "loss": round(float(out.loss.item()), 4),
                        "allocated_gb": round(
                            torch.cuda.memory_allocated() / 1e9, 3) if gpu_ok else None,
                        "reserved_gb": round(
                            torch.cuda.memory_reserved() / 1e9, 3) if gpu_ok else None})
            print(f"[step {step + 1}/{args.steps}] {rec['sec']}s "
                  f"loss={rec['loss']}")
        except Exception as exc:  # noqa: BLE001 失败留记录
            rec["error"] = repr(exc)[:500]
            print(f"[step {step + 1}/{args.steps}] 失败: {exc}")
        step_records.append(rec)
        (run_dir / "steps.jsonl").write_text(
            "".join(json.dumps(r, ensure_ascii=False) + "\n"
                    for r in step_records), encoding="utf-8")

    ok_steps = [r for r in step_records if "error" not in r]
    peak_alloc = (torch.cuda.max_memory_allocated() / 1e9) if gpu_ok else 0.0
    peak_reserved = (torch.cuda.max_memory_reserved() / 1e9) if gpu_ok else 0.0
    ckpt_dir = run_dir / "adapter-ckpt"
    peft_model.save_pretrained(ckpt_dir)
    ckpt_bytes = sum(p.stat().st_size for p in ckpt_dir.rglob("*") if p.is_file())

    summary = {"tag": args.tag, "run_id": f"screening-{args.tag}-seq{args.seq_len}",
               "steps": args.steps, "seq_len_target": args.seq_len,
               "actual_seq_len": actual_seq_len,
               "gpu_ok": gpu_ok, "device_map_summary":
                   {k: str(v)[:40] for k, v in list(device_map.items())[:4]},
               "load_sec": round(load_sec, 1),
               "load_vram_gb": round(load_vram, 2),
               "train_peak_allocated_gb": round(peak_alloc, 2),
               "train_peak_reserved_gb": round(peak_reserved, 2),
               "step_sec_list": [r.get("sec") for r in ok_steps],
               "failed_steps": len(step_records) - len(ok_steps),
               "adapter_ckpt_bytes": ckpt_bytes,
               "note": "合成资源探针(重复文本输入),不等于真实任务训练稳定性;"
                       "执行了 backward+optimizer.step(用户批准的筛选期测量)",
               "env": {"python": sys.version.split()[0],
                       "platform": platform.platform()},
               "command": " ".join(sys.argv),
               "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")}
    (run_dir / "summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
