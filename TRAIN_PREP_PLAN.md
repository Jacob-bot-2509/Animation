# 训练前准备计划(TRAIN_PREP_PLAN)

> 2026-10-03,msg_190/191。**仅准备:不启动训练、不下载模型、不安装依赖、不生成批量动画。**
> 本文件是训练前准备的契约与状态说明,不是可执行训练计划。

## 1. 任务目标与输入输出字段(第一轮固定)

- 目标:**problem + solution → scene_spec(动画规划)**。
- 明确声明:当前数据**没有 Manim code 标签**,训练目标**不是**直接生成代码;
  不默认声称已有 code/render_status/code_sha256。
- 输入字段:problem、solution(核心正文)。
- 输出字段:scene_spec(objects/steps 设计稿)。
- 同题多解预留:problem_id/solution_id/method(见 DATASET_SCHEMA.md §6),
  当前数据未启用,接口保留。

## 2. 当前数据状态:63 条 provisional train

| 板块 | 条数 |
|---|---|
| 数学分析 | 19 |
| 概率论 | 9 |
| 解析几何 | 12 |
| 高等代数 | 23 |

- 正式入口:`data/v1/raw/*.jsonl`(原始 JSON 数组保留,不做样本入口)。
- train-only 清单:`data/v1/manifest-train.json`(4 条目,用户拍板 2026-10-03:
  63 条候选按角色标 split=train,manifest.json 同口径;provisional/candidate
  语义在 notes 与 policy 注明,未验收、动画未验证,不得视为已验收训练集)。
- **candidate/UNVERIFIED 语义保留**:63 条是候选训练数据,不是已验收训练集;
  动画未验证(缺 code/render_status/code_sha256)。
- 许可证:`Internal-Research-Use-Only`(用户确认:仅内部研究、不公开分发、公开前转正)。

## 3. 训练配置契约

模板:`train_config.template.json`。要点:

- 字段:task / dataset_manifest / split=train / seed / model(name, quantization) /
  method(lora/qlora 候选) / lora(r, alpha, dropout, target_modules) /
  max_seq_length / learning_rate / batch_size / gradient_accumulation_steps /
  epochs / eval_strategy / output_dir。
- **未知超参数一律 TBD,不伪造已验证数值**;模板不含真实模型名/凭据。
- 静态校验:JSON 合法、必填字段齐全、TBD 标记存在、无凭据键(见 tests/test_train_prep.py)。

## 4. B1 运行快照字段清单(训练启动时必填)

模型名称/版本、tokenizer 版本、量化配置、LoRA 参数(r/alpha/dropout/target_modules)、
seed、Python 版本、GPU 型号与显存、git commit 与 dirty 状态、
数据 manifest SHA256、完整训练命令。
(与项目 run_record v3 的 seed/dirty/env 快照约定一致。)

## 5. 8GB 显存路线说明(仅路线,不验证模型可用性)

- **小样本过拟合先行**:先在极小样本上验证管线能学、资源峰值可控。
- **LoRA/QLoRA 作为候选**:适配器训练,量化候选待批准。
- 模型已下载并经用户批准(2026-10-03 筛选完成);具体量化方案由用户批准后确定。
- **后端适配器契约**:src/animtrain/backend.py(load_model/train/save_checkpoint/
  evaluate 四入口;未批准阶段一律 NOT_APPROVED 抛 BackendNotApproved;
  LLaMAFactory/Unsloth 等未来后端经注册表接入,当前不绑定实现)。
- **底座模型**:BASE_MODEL_SHORTLIST.md。**baseline = Qwen3-4B
  (2026-10-03 用户拍板,Apache-2.0,权重在本机 .models/qwen3-4b,provenance 已记录)**;
  Qwen3-8B / Qwen2.5-7B-Instruct 保留对照;DeepSeek-R1-Distill-Qwen-7B 为后续候选。
- **eval/test**:EVAL_TEST_PREP.md(eval=同题多解 problem_id/
  solution_id/method;test=综合泛化;题目族/近重复/train 严格隔离;
  **已生成已冻结(2026-10-03)**:300/150 条,锁 data/{eval,test}-v1.lock.json)。

## 6. 后续 eval/test 接口与隔离规则(现在不生成、不冻结)

- 评测题目族**独立制作**,不得复用 provisional train 样本;
- 同题多解用 problem_id/solution_id/method 区分;
- 近重复校准(B5)与冻结锁(*.lock.json)入口保留;
- eval/test 生成与冻结是 READY 的前置条件,现在一律不执行。

## 7. 训练前门禁(READY 前置条件)

1. eval/test 独立生成并通过 data_check + 冻结(锁绑定当前 manifest);
2. 数据/许可证/manifest/快照齐全;
3. B2 资产验收证据(真实渲染验证)、B4 执行隔离、B5 阈值校准完成;
4. `preflight --ready` 通过且无 UNVERIFIED;
5. **用户明确批准模型/训练路线**。

当前 train-only 状态下,preflight 输出必须为 **PREPARED/NOT READY**,
不得生成可执行训练计划,不得绕过任何缺失门禁。

实测(2026-10-03,`preflight --ready --run-id prep-check-0001
--manifest data/v1/manifest-train.json`,exit=1):

- PASS:gpu(RTX 5060 Laptop,8151 MiB)/ data_manifest(4 条目,0 问题)/
  render_gate/math_gate(环境诊断证据,非资产验收)
- FAIL:model_dir(未提供模型)/ run_snapshot(无快照)/
  near_dup_calibrated(UNCALIBRATED)/ freeze_gate(manifest 无 eval/test)
- 结论:**NOT READY —— 禁止生成训练计划,先定位缺失项** ✓ 语义正确,
  训练前门禁生效。

## 8. 不覆盖声明

不覆盖任何既有审计证据(dataset_audit_*)、archives/reviews/ 文档、原始数据;
本文件为计划补充。
