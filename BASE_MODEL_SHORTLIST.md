# 底座模型候选短名单(BASE_MODEL_SHORTLIST)

> 2026-10-03,msg_195。**未下载、未验证任何模型**;本表为候选评估框架,
> 各维度结论均以"待实测/待验证"标注,最终选择由用户确认。
> 许可证、量化生态、显存适配在批准后逐项实测。

## 评估维度(候选按以下 8 项打分,当前全部待实测)

| 维度 | 说明 | 当前状态 |
|---|---|---|
| 中文能力 | 中文题干/解答理解与生成 | 待实测 |
| 数学推理 | problem→solution 推理质量 | 待实测 |
| LaTeX 生成 | 公式语法正确率(过 render_gate 口径) | 待实测 |
| JSON 结构化输出 | scene_spec(objects/steps)可解析率 | 待实测 |
| Python/Manim 基础 | 是否具备 Manim 代码基础(本轮不训练 code) | 待实测 |
| 4bit+LoRA/QLoRA 支持 | 量化/适配器生态成熟度 | 待实测 |
| 许可证 | 可商用/可内部训练的许可条款 | 见下表,需最终确认 |
| 8GB 显存适配 | QLoRA 下本机可训练性(本机 RTX 5060 Laptop 8GB) | 待实测 |

## 候选(保留 2 个,全部待用户确认)

| 候选 | 规模 | 许可证 | 状态(2026-10-03 实弹对照后) | 待确认项 |
|---|---|---|---|---|
| **Qwen3-4B(baseline,用户拍板)** | 4B | Apache-2.0 | 思考模式严格解析率 80%(最高)、QLoRA 峰值 5.33G 无溢出 | 训练超参数、eval/test 冻结后启动 |
| Qwen3-8B(对照保留) | 8B | Apache-2.0 | 65% 解析率、训练峰值 10.12G 溢出 8G | 若启用需短序列+显存优化 |
| Qwen2.5-7B-Instruct(对照保留) | 7B | Apache-2.0 | 35% 解析率、训练峰值 9.4G 溢出 | 出局候选,保留 .models/ |
| DeepSeek-R1-Distill-Qwen-7B(后续候选) | 7B | MIT | 数学推理蒸馏强化 | 与 baseline 对比后决定 |

> **决策(2026-10-03,用户拍板):baseline = Qwen3-4B** —— 三方实弹对照结论:
> 4B 思考模式严格 JSON 解析率 80%(最高)、QLoRA 训练峰值 5.33G(8G 显存无溢出);
> Qwen2.5-7B(35%/9.4G 溢出)与 Qwen3-8B(65%/10.12G 溢出)保留作对照,不删除。
> 证据:reviews/2026-10-03-model-screening/。八维评估中未测项保持待实测标注。

## 明确不做

- 不再下载新模型(现有三款经用户批准);不启动训练;
- 不写凭据进任何配置;模板内模型名已置为 baseline Qwen3-4B;
- 不把候选表当成已验证结论——训练路线批准前一切保持 candidate/UNVERIFIED。

## 决策入口

- 训练配置契约:train_config.template.json
- 后端适配器契约:src/animtrain/backend.py(未批准一律 NOT_APPROVED)
- 训练前门禁与 READY 前置条件:TRAIN_PREP_PLAN.md §7
