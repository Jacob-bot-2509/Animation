# 三方底座模型对照报告(MODEL_COMPARISON)

> 生成时间:2026-10-03 15:26:27。任务:problem+solution → scene_spec 结构化 JSON(20 条子类分层样本,输入哈希冻结)。仅筛选测量,不构成正式训练;candidate/UNVERIFIED 语义保持。

## 1. 推理对照(20 条,同口径冻结 seed/GenerationConfig)

| 模型/模式 | 严格 JSON 解析率 | 宽松提取率 | 4bit 加载显存 | 热延迟/条 | 总生成 token |
|---|---|---|---|---|---|
| qwen2.5-7b | 35% | 35% | 5.97 GB | 9.8 s | 4261 |
| qwen3-4b | 50% | 50% | 2.89 GB | 20.6 s | 6678 |
| qwen3-4b-thinking | 80% | 80% | 2.89 GB | 44.3 s | 14275 |
| qwen3-8b | 65% | 65% | 6.49 GB | 18.6 s | 6085 |
| qwen3-8b-thinking | 65% | 65% | 6.49 GB | 44.1 s | 15317 |

## 2. QLoRA 训练资源探针(seq=1024 精确 token,3 步)

| 模型 | 训练峰值 allocated | 训练峰值 reserved | 平均步时 | 失败步 | adapter 体积 |
|---|---|---|---|---|---|
| qwen2.5-7b | 8.33 GB | 9.40 GB | [3.83, 2.87, 2.86] | 0 | 20221148 |
| qwen3-4b | 5.33 GB | 6.42 GB | [2.74, 2.36, 2.37] | 0 | 23637595 |
| qwen3-8b | 9.02 GB | 10.12 GB | [6.06, 6.53, 6.52] | 0 | 30715547 |

## 3. 未测维度(NOT_MEASURED,如实)

- FP16-vs-4bit 退化对照:未测
- TTFT 细分:未测
- 梯度累积吞吐:未测
- 断点恢复验证:未测(adapter save ≠ 恢复验证)
- 数学/内容人工复核:未测(仅规则可解析率)
- seq_len 曲线全档(2048/4096):未测
- Windows+bnb 兼容性:已实测通过(三模型 4bit 加载均成功)

## 4. 环境与证据

- GPU: NVIDIA GeForce RTX 5060 Laptop(8GB),torch 2.11.0+cu128;
- 每 run 目录含逐样本完整输出/哈希/命令/env/provenance 哈希;
- 原始 run 数据留存于 outputs/screening-tmp/,撤组前归档。

## 5. 结论建议(待用户拍板)

- 数据为 provisional train 筛选成绩,不当正式 eval/test 验收;
- baseline 选择需综合解析率、显存余量、延迟与训练可行性,由用户决定。
