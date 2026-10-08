"""Write the user-confirmed hyperparameter config (2026-10-08) into configs/.

Builds configs/hp_sweep.json with the confirmed center combo (sha256-bound,
status CONFIRMED) plus the planned pilot grid (PROPOSED, not run yet).
Writing a config only -- no training is triggered.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(r"D:\Animation-Model-Training")
OUT = ROOT / "configs" / "hp_sweep.json"

def canon(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))

def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def main():
    base = {
        "learning_rate": "1/5000",
        "batch_size": 2,
        "gradient_accumulation_steps": 4,
        "epochs": 6,
        "max_seq_length": 2048,
        "quantization": "4bit NF4 + 双量化",
        "optimizer": "paged_adamw_8bit",
        "lr_schedule": "cosine + 5% warmup",
        "early_stop": "eval_loss 连续 2 轮变差即停",
        "seq_guard": "构建期逐条 tokenize 校验,超长记录拆分",
        "checkpoint": "每 epoch 保存,冻结 seed/命令/SHA 快照",
        "seed": 42,
    }
    center = {**base, "lora_r": 16, "lora_alpha": 32}
    center_sha = sha256(canon(center))
    candidates = [
        {
            "name": "center-confirmed",
            "hyperparameters": center,
            "hyperparameter_approval": {
                "status": "CONFIRMED",
                "confirmed_by": "用户 2026-10-08(效率重算 reviews/2026-10-08-hyperparam-derivation/hyperparams-v2.md)",
                "sha256": center_sha,
                "run": "NOT_RUN_YET",
            },
        },
    ]
    # Pilot grid: first-round empirical validation on ~1/4 data; not yet run.
    for name, patch in (
        ("pilot-r8", {"lora_r": 8, "lora_alpha": 16}),
        ("pilot-lr-high", {"learning_rate": "1/2500"}),
        ("pilot-lr-low", {"learning_rate": "1/10000"}),
    ):
        params = {**center, **patch}
        candidates.append({
            "name": name,
            "hyperparameters": params,
            "hyperparameter_approval": {
                "status": "PROPOSED",
                "confirmed_by": None,
                "sha256": sha256(canon(params)),
                "run": "NOT_RUN_YET",
            },
        })
    doc = {
        "_说明": (
            "用户 2026-10-08 确认的效率最优组合(基于实测语料 311 条/0.3M tokens 推导),"
            "先落配置不运行。正式训练前须跑首轮 pilot_grid(1/4 数据,4 组),"
            "按验收集损失+生成动画样本双指标选优后放大;center-confirmed 为默认起点。"
            "底座模型=Qwen3-4B(.models/qwen3-4b,用户 2026-10-03 拍板)。"
        ),
        "subset": {"pilot_count": 78, "note": "首轮试训用约 1/4 训练侧数据", "seed": 20261005},
        "model_path": ".models/qwen3-4b",
        "dataset_manifest": "TBD(训练启动时绑定 current-core 清单,冻结 SHA)",
        "render_executor": None,
        "judge_script": None,
        "output_winner": "configs/train_loop.winner.json",
        "pilot_grid": {
            "plan": "2 LR(1/5000、1/2500)× 2 r(16/32、8/16)= 4 组,每组约 5-15 分钟",
            "metrics": ["eval_loss", "生成动画样本(渲染后结构/密度指标+用户目视)"],
            "status": "PLANNED_NOT_RUN",
        },
        "candidates": candidates,
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"written": OUT.relative_to(ROOT).as_posix(),
                      "center_sha256": center_sha,
                      "candidates": [c["name"] for c in candidates]}, ensure_ascii=False))
    return 0

if __name__ == "__main__":
    sys.exit(main())
