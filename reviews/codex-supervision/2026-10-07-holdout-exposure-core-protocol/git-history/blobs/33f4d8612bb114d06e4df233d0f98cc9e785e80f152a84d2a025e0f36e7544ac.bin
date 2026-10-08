# 当前任务进度

更新日期：2026-10-03。**协作角色：Claude Code 同时承担统筹(copilot 职责)与执行职责;
Codex 独立复审。** 未训练、未下载模型、未安装依赖。

## 当前阶段

- 数据：63 条自撰候选数据(数学分析 19 / 概率论 9 / 解析几何 12 / 高等代数 23),
  dataset.md / JSON 数组 / data/v1/raw/*.jsonl 三处一致,入场检查 clean;
  审计记录级 hard=0,63 条全部 **candidate**(code/render_status 缺失,不假绿)。
- 训练前准备就绪：manifest-train(provisional)、train_config.template(TBD 契约)、
  backend 适配器契约、BASE_MODEL_SHORTLIST(baseline=Qwen2.5-7B-Instruct 待批准)、
  eval/test 接口与目录占位(未生成未冻结)。
- preflight --ready 实测 **NOT READY**(model_dir/run_snapshot/near_dup_calibrated/
  freeze_gate/asset_evidence 阻断),fail-closed 生效。

## 审查台账状态

| 项 | 状态 |
|---|---|
| A1-A8 数据与入场可信度 | 全部关闭(JSONL 口径、近重复实现、入场边界、A4/A5 语义、A6 类型/别名、A7 冻结写保护、A8 防泄漏哈希) |
| B1 运行快照 | GS4 反例已修(dirty 内容哈希绑定、config fail-closed、CLI verify);待 Codex 独立复验 |
| B2 严格 preflight | GS2 反例已修(逐条资产证据 + 8 项核心门禁);待 Codex 独立复验 |
| B3 冻结评测与指标 | 空锁/覆盖/绑定已过;固定指标、逐样本结果与失败分类待 eval/test 冻结后验收 |
| B4 执行隔离 | GS5 反例已修(assign fail-closed、kill+wait、job_assigned 如实);memory 已实施、network 仍 UNVERIFIED;待独立复验 |
| B5 阈值校准 | UNCALIBRATED 传播并阻断;分语言/长度校准待真实标注数据(用户侧) |
| B6 产物写入 | GS1 反例已修(碰撞拒绝/阶段持久化/清理失败不回滚/恢复冻结保护);待独立复验 |
| B7 类型契约 | 已关闭(分类/来源/正文/答案/场景元素/可选元数据类型) |
| C1-C12 | 延期清理,主线收尾集中处理 |

## 最新验证

- **301 passed + 29 subtests**(2026-10-03);真实 63 条入场 clean、data_check 通过;
  审计 v7 记录级 hard=0;GS1-GS6 反例已修待 Codex 复验。
- manifest sha256: data/v1/manifest.json `297c0373…`(raw 口径);
  data/v1/manifest-train.json `8f1c9b98…`(provisional train,4 条目 split=train)。

## 下一步顺序(统筹视角)

代码侧可继续推进(不需用户批准)：
1. **B4 完整执行隔离**(fs/network/memory)与不可信数学输入保护;
2. **B1 快照补全**(训练配置参数入快照、完整重放);
3. C 类清理(C2 空 split 误报、C5 配置示例、C12 效率整理)。

需要用户批准/提供的门：
1. eval/test 样本制作(数量/来源/许可证,EVAL_TEST_PREP.md §4);
2. Qwen2.5-7B-Instruct 下载与量化方案批准;
3. B5 校准的真实标注数据;
4. 训练超参数(base 选择后的实测值)。

完整规划见 [PIPELINE_PLAN](PIPELINE_PLAN.md)、[训练前准备](TRAIN_PREP_PLAN.md)、
[eval/test 接口](EVAL_TEST_PREP.md)、[审查备忘录](REVIEW_BACKLOG.md)。
