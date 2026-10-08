"""训练执行器(QLoRA SFT):problem + solution → scene_spec。

设计契约见 docs/TRAINING-LOOP-DESIGN.md。超参从轮次配置读取,缺失即拒绝
执行(fail-closed);训练只读当前 manifest 登记的 train 文件,eval/test 绝不
触碰(防过拟合铁律)。产出:LoRA adapter + 训练清单(training-manifest.json,
含配置/数据/权重哈希)。

用法:
  <venv>/Scripts/python.exe -X utf8 tools/train_step.py --config <rounds.json>
      --work <runs/loop-xxx/round-n> --run-id <id>
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

PROMPT_TMPL = (
    "你是数学动画规划师。根据题目与解法,输出动画规划 JSON(scene_spec),"
    "格式:{\"objects\": [\"...\"], \"steps\": [\"...\"]}。\n"
    "要求:objects/steps 均为非空字符串列表;公式用 $...$ 包裹;"
    "steps 覆盖解法全部关键推理步骤;只输出 JSON,不要解释。\n"
    "题目:{problem}\n解法({method}):{solution}\n")


def _sha(p: Path) -> str | None:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()
    except OSError:
        return None


def load_train_rows(manifest: Path) -> list[dict]:
    m = json.loads(manifest.read_text(encoding="utf-8"))
    rows = []
    for e in m["entries"]:
        if e["split"] != "train":
            continue  # eval/test 绝不进入训练
        p = (manifest.parent / e["path"]).resolve()
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows


def check_hyperparameters(config: dict) -> list[str]:
    hp = config.get("hyperparameters") or {}
    required = ("learning_rate", "batch_size", "gradient_accumulation_steps",
                "epochs", "lora_r", "lora_alpha", "max_seq_length",
                "quantization", "seed")
    return [k for k in required if hp.get(k) is None]


def train(config: dict, work: Path, run_id: str) -> dict:
    hp = config["hyperparameters"]
    manifest = Path(config.get("dataset_manifest",
                               str(ROOT / "data/manifest.json")))
    model_dir = Path(config.get("model_path", str(ROOT / ".models/qwen3-4b")))
    if not model_dir.exists():
        return {"status": "REFUSED", "reason": f"模型目录不存在: {model_dir}"}
    rows = load_train_rows(manifest)
    if not rows:
        return {"status": "REFUSED", "reason": "训练集为空,拒绝执行"}
    adapter_out = work / "adapter"
    adapter_out.mkdir(parents=True, exist_ok=True)

    # 惰性导入重依赖(环境缺失时给出明确报错而非裸崩)
    try:
        import torch  # noqa: PLC0415
        from transformers import (  # noqa: PLC0415
            AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer,
            DataCollatorForLanguageModeling)
        from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training  # noqa: PLC0415
        import bitsandbytes as bnb  # noqa: PLC0415
        from transformers import BitsAndBytesConfig  # noqa: PLC0415
    except ImportError as e:
        return {"status": "REFUSED",
                "reason": f"训练依赖缺失: {e}(先装 torch/transformers/peft/bitsandbytes)"}

    tok = AutoTokenizer.from_pretrained(str(model_dir))
    tok.pad_token = tok.pad_token or tok.eos_token
    texts = [PROMPT_TMPL.format(problem=r.get("problem", ""),
                                solution=r.get("solution", ""),
                                method=r.get("method", "常规解法"))
             for r in rows]
    enc = tok(texts, max_length=int(hp["max_seq_length"]), truncation=True,
              padding=True)
    truncated = sum(1 for t in texts
                    if len(tok(t)["input_ids"]) > int(hp["max_seq_length"]))
    if truncated:
        print(f"[train] 注意:{truncated} 条样本被截断到 "
              f"{hp['max_seq_length']} token(如实记录,不伪造)")

    quant = hp["quantization"].lower()
    bnb_cfg = BitsAndBytesConfig(load_in_4bit=quant in ("4bit", "nf4", "4-bit"),
                                 bnb_4bit_quant_type="nf4",
                                 bnb_4bit_compute_dtype=torch.bfloat16,
                                 bnb_4bit_use_double_quant=True) \
        if quant in ("4bit", "nf4", "4-bit") else None
    model = AutoModelForCausalLM.from_pretrained(
        str(model_dir), quantization_config=bnb_cfg,
        torch_dtype=torch.bfloat16, device_map="auto")
    model.gradient_checkpointing_enable()
    model = prepare_model_for_kbit_training(model)
    model = get_peft_model(model, LoraConfig(
        r=int(hp["lora_r"]), lora_alpha=int(hp["lora_alpha"]),
        lora_dropout=0.05, bias="none", task_type="CAUSAL_LM",
        target_modules="all-linear"))
    model.print_trainable_parameters()

    import torch  # noqa: PLC0415
    from torch.utils.data import Dataset  # noqa: PLC0415

    class _LMDataset(Dataset):
        def __init__(self, input_ids, attention_mask):
            self.input_ids = input_ids
            self.attention_mask = attention_mask

        def __len__(self):
            return len(self.input_ids)

        def __getitem__(self, i):
            return {"input_ids": self.input_ids[i],
                    "attention_mask": self.attention_mask[i]}

    ds = _LMDataset(torch.tensor(enc["input_ids"], dtype=torch.long),
                    torch.tensor(enc["attention_mask"], dtype=torch.long))
    args = TrainingArguments(
        output_dir=str(work / "ckpt"),
        num_train_epochs=int(hp["epochs"]),
        per_device_train_batch_size=int(hp["batch_size"]),
        gradient_accumulation_steps=int(hp["gradient_accumulation_steps"]),
        learning_rate=float(hp["learning_rate"]),
        lr_scheduler_type="cosine", warmup_ratio=0.05,
        logging_steps=1, save_strategy="no", bf16=True,
        report_to=[], seed=int(hp["seed"]),
        run_name=f"loop-train-{run_id}")
    trainer = Trainer(model=model, args=args, train_dataset=ds,
                      data_collator=DataCollatorForLanguageModeling(
                          tokenizer=tok, mlm=False))
    t0 = time.time()
    result = trainer.train()
    model.save_pretrained(str(adapter_out))
    tok.save_pretrained(str(adapter_out))
    manifest_out = {
        "status": "TRAINED", "run_id": run_id,
        "train_rows": len(rows), "truncated_rows": truncated,
        "model_path": str(model_dir),
        "model_sha256": _sha(model_dir / "config.json"),
        "adapter_dir": str(adapter_out),
        "hyperparameters": dict(hp),
        "train_loss": getattr(result, "training_loss", None),
        "elapsed_s": round(time.time() - t0, 1)}
    (work / "training-manifest.json").write_text(
        json.dumps(manifest_out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest_out, ensure_ascii=False, indent=2))
    return manifest_out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument("--work", type=Path, required=True)
    ap.add_argument("--run-id", required=True)
    args = ap.parse_args(argv)
    config = json.loads(args.config.read_text(encoding="utf-8"))
    missing = check_hyperparameters(config)
    if missing:
        print(f"[FAIL] 超参未定案({missing}),训练步拒绝执行(fail-closed)")
        return 2
    args.work.mkdir(parents=True, exist_ok=True)
    out = train(config, args.work, args.run_id)
    return 0 if out.get("status") == "TRAINED" else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
