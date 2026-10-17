# 训练自动化循环设计（harness）

状态：接口预留，正式逐题执行/判定尚未接通，门禁关闭。本设计与实际差异、证据格式及分工统一见 [准备证据与接线协议](READINESS-EVIDENCE-PROTOCOL.md)，实际操作见 [Runbook](TRAINING-START-RUNBOOK.md)。

## 1. 任务与四指标

训练任务为 problem + solution → scene_spec，不直接训练 Manim code。按问题计数，具体题数从当前 manifest 和固定子集推导，不从记录行数或旧文档硬编码。eval/test 分列报告，同一问题全部必需场景绑定同一身份并合并判断。

| 指标 | 定义 | 目标 |
|---|---|---|
| R 渲染成功率 | 必需场景均产出对应的真实可解码 PNG/MP4，并有源/产物/运行绑定 | R=1 |
| E 可执行率 | schema、受审查转换与沙箱执行/清理全过程通过，并满足 R 的真实产物条件 | E≥19/20 |
| M 数学正确率 | 逐题数学条件、结论与动画对应有独立精确断言或审查理由 | 不另设硬线，未解决项入队 |
| F 画面忠实度 | 实际完整动画满足事前锁定的对象、关系、步骤和叙述语义清单 | 不另设硬线，未解决项入队 |

指标分母在生成前固定，未知不得作失败或成功伪填，也不得删题提高率。正式汇总的 status=VERIFIED 要求具名总体中每题已真实判为 PASS/FAIL，rate 使用 Fraction(passed,total) 的精确字符串；有未知则完整指标仍 UNVERIFIED，另列实际覆盖。schema 诊断、退出码、公式编译或短答案外测均不能替代 R/E/M/F。

停止规则保留用户既定目标：R=1 且 E≥19/20 达标停；或已验证可比较指标连续 3 轮无改善；或达到 8 轮上限。未知指标不能作为改善或达标依据。任何评测协议错误、缺证据、异常或超时停止并留存回执。

## 2. 执行顺序与实际实现

静态数据准备在 READY 前完成；不可信代码执行先通过 exec_isolation，再完成真实资产验收。全部配置、数据与源码固定后由 prepare_snapshot/run_record 生成真实快照，再完整检查 READY 与 harness 前置项。不能先开训来生成“准备就绪”的证据。

每轮：检查 stop 文件 → 真实配置/数据/代码绑定与准备快照 → 门禁自检 → 已获审批的训练 → 固定评测题单生成 → 受限逐题渲染/数学/语义审查 → 双列报告与哈希 → 目标/平台/上限决定。

当前工具读取的八项 READY 名称是 gpu、model_dir、data_manifest、run_snapshot、asset_evidence、freeze_gate、near_dup_calibrated、exec_isolation。另有训练多样性、真实超参审批/支持合同、长度处理和配置/数据绑定。详情按协议逐项交付，缺项不得手造通过。

## 3. 访问与执行边界

eval/test 题文、答案和生成结果不进入训练或提示示例，人工硬题队列只保存 ID/原因。持续每轮监测的 test 不再宣称未见最终验证；391 候选来源池的最终资格与独立封存另按既定 holdout 设计执行。

生成代码只通过受审查的 AppContainer + JobObject 运行，无宿主 fallback；固定可信 smoke 不充当新生成资产验收。用户已直接确认有限内容隔离政策，不要求事前全局语义隔离证明；该政策与操作系统边界、真实资产和访问记录分别记账。

循环只写新轮次目录，不自行更改门禁、冻结锁、标注或数据。runs/loop.stop 与证据 consumer 的 runtime/STOP 各自独立。自动流程不授予模型配置变更、探针发射或生产解锁权限。

## 4. 报告与选优

eval-report.json 绑定 run_id、config/manifest/training_manifest/generated_specs/adapter SHA，逐题证据还须绑定 evaluator 版本、样本身份、实际代码/媒体和判定理由。报告含 eval/test 四指标、原始分子分母、失败/未知 ID、证据索引及轮次 JSON/MD/日志。硬题队列不回灌题文。

hp_sweep 只有真实 VERIFIED 的执行/渲染主指标才能选择 winner，使用精确 E→R→M 比较；全部未知或仅数学指标可用时不产生 winner。eval_loss 排名与按 pilot_count 选训练子集均不能写成已实现；当前 build_subset 读取 subset.count 选择评测问题。

## 5. 接线待办与分工

已确定的合同详见协议第 6 节：请求绑定、逐样本回执、R/E/M/F 数学定义、未知/分母、路径与进程边界、最小对抗夹具。它是待实现合同，不是现有任意脚本插件的调用许可。

Claude 先提交受限 render_executor/judge_script 适配器候选及固定夹具、源 SHA、真实接口和权限边界；Codex 独立审查、修复和验证。未通过前 eval_step 维持拒绝任意外部脚本、四指标 UNVERIFIED 和非零退出。M/F 可分阶段接通，未知就保留未知。

当前还需落实：真实参数合同与审批、训练构建期 tokenizer/超长处置、校准证据消费接口、独立工作根上的原生采集与证书生成流程。协议文件不会自动实现这些功能；也不把配置中的描述或作者声明作为回执。

用户决定政策和授权；Claude 完成已授权工作并交付原件；Codex 依具名版本独立核验和修复、限定资格、归档与回信。当前未开训。
