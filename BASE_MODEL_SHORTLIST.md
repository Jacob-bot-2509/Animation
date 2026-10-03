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

| 候选 | 规模 | 许可证 | 入选理由(定性,待实测) | 待确认项 |
|---|---|---|---|---|
| **Qwen2.5-7B-Instruct(第一版 baseline,用户已确认 2026-10-03)** | 7B | Apache-2.0 | 中文/数学基础好,JSON 输出与工具调用生态成熟,QLoRA 生态支持广,8GB 显存可 QLoRA | 下载/实测/批准后启用;中文数学实测、scene_spec JSON 可解析率实测、量化方案批准 |
| DeepSeek-R1-Distill-Qwen-7B(后续对照候选) | 7B | MIT | 数学推理蒸馏强化,同为 Qwen 底座便于工具链复用 | 指令跟随/JSON 输出实测、与 baseline 对比后决定 |

> **决策(2026-10-03,用户拍板):baseline = Qwen3-4B** —— 三方实弹对照结论:
> 4B 思考模式严格 JSON 解析率 80%(最高)、QLoRA 训练峰值 5.33G(8G 显存无溢出);
> Qwen2.5-7B(35%/9.4G 溢出)与 Qwen3-8B(65%/10.12G 溢出)保留作对照,不删除。
> 证据:reviews/2026-10-03-model-screening/。八维评估中未测项保持待实测标注。

## 明确不做

- 不下载模型、不安装依赖、不启动训练;
- 不写真实模型路径/凭据进任何配置(模板内模型名为 TBD);
- 不把候选表当成已验证结论——训练路线批准前一切保持 candidate/UNVERIFIED。

## 决策入口

- 训练配置契约:train_config.template.json
- 后端适配器契约:src/animtrain/backend.py(未批准一律 NOT_APPROVED)
- 训练前门禁与 READY 前置条件:TRAIN_PREP_PLAN.md §7
