# 训练准备 Runbook：门禁未开

当前只允许准备与审查，不由本文授权开训、评测、原生探针或 production 解锁。OneDrive 传输回放与 consumer watch 部署已按具名范围验收；它们不替代校准、资产、执行隔离或运行快照门禁。

本页修订依据：[只读事实快照](../archives/reviews/codex-supervision/2026-10-17-training-runbook-review/current-read-only-facts.json)、[本轮修复报告](../archives/reviews/codex-supervision/2026-10-17-training-runbook-review/SUPERVISION_REPORT.md)。本轮未运行完整 preflight、渲染 smoke、训练或真实模型评测，不能把本页当作全部门禁的实测 PASS 清单。

## 当前事实与缺口

| 项目 | 已核验事实及限制 |
|---|---|
| 冻结锁 | eval-v2 与 test-v2 两份锁通过当前 manifest 绑定校验，退出码均为 0。仅代表具名冻结检查，不代表整体 READY。 |
| 执行隔离 | check_exec_isolation() 返回未联合验收，当前 data/execution_evidence.json 缺失。D9 的旧 LAN 有限登记窗不能代替生产联合证书。 |
| 数据多样性 | check_training_diversity() 返回 Training diversity review evidence is absent。必须按当前 manifest、政策与逐条审查绑定验收，不能从草稿数量推断满足。 |
| 资产 | 当前 asset_evidence 中 calc-area-007 缺 output 对象。须有真实产物、当前完整样本行 SHA、解码及数学/语义/渲染证据；不能只补字段或改 verified 标记。 |
| 近重复校准 | 必须核验实际执行规则、阈值、标签与输入版本的独立证据；旧 B5 自报 calibrated 不自动覆盖当前规则。UNCALIBRATED 仍阻断 READY。 |
| GPU、模型、运行快照与环境 smoke | 本轮未完整实测，不引用无原始回执的时间占位或历史 PASS 当作当前结果。render/math 固定 smoke 仅诊断环境，不替代资产验收。 |
| 全局隔离 | 保持 NOT_ESTABLISHED，如实记录有限已验收范围。本页不新增“必须事前证明全部全局隔离”的要求，也不擅自批准在有限证据下训练。 |
| 生产状态 | CLOSED；当前未 READY、未开训。 |

当前 [preflight 实现](../src/animtrain/preflight.py) 的 READY 必需项为：
gpu、model_dir、data_manifest、run_snapshot、asset_evidence、freeze_gate、near_dup_calibrated、exec_isolation。
harness 还会检查数据多样性和实际配置绑定，不能只查前四项或把未知项剔除。

不带 --manifest 时无法验收当前 eval/test 冻结绑定，这是缺少输入产生的正确拒绝，不是应忽略的“误报”。

## 当前扫参配置不能直接运行

[configs/hp_sweep.json](../configs/hp_sweep.json) 的 dataset_manifest 仍为 TBD。四个候选的实际参数如下，不是完整的二乘二网格：

| 候选 | 学习率 | LoRA r/alpha | 配置中的审批状态 |
|---|---:|---:|---|
| center-confirmed | 1/5000 | 16/32 | CONFIRMED，但当前执行器仍拒绝：Unreviewed quantization |
| pilot-r8 | 1/5000 | 8/16 | PROPOSED |
| pilot-lr-high | 1/2500 | 16/32 | PROPOSED |
| pilot-lr-low | 1/10000 | 16/32 | PROPOSED |

审批标记不等于执行器接受，参数内容、审批 SHA 与受支持合同都须一致。本轮没有修改任何超参或模型配置，也没有替用户批准其余候选。

subset.pilot_count=78 是配置中的训练侧提案元数据；当前 [hp_sweep.py](../tools/hp_sweep.py) 的 build_subset 实际读取 subset.count（未配置时为 20），从 eval 的 problem_id 抽固定评测子集，不实施按 pilot_count 选取训练子集。不得把两者混为已实现的训练采样。

当前自动选优按可执行率、渲染率、数学率参考排序，不按 eval_loss 排序；“eval_loss + 动画目视”若要成为新选优方法，需另行落实合同、实现与证据，不能只写说明。现有评测实现保持 R/E/M/F 为 UNVERIFIED，schema 诊断不能替代真实执行/数学/忠实度指标。

Codex 本轮已修复选择器：只使用 VERIFIED 且 passed/total 与精确分数一致的指标；无可验证的执行/渲染主指标时不选胜者、不写 winner 配置，返回失败。数学率不能单独支撑执行胜者。未知指标不假绿，分数不转成小数近似。

## 准备与后续执行顺序

1. 核对用户实际授权的训练策略与适用范围。Claude 邮件 846 转述其侧用户确认了有限隔离策略，但这仍是邮件来源材料，不等于当前会话收到的用户直接指令；在确认前不据此扩权。即使后续确认，也不自动免除现行代码门禁。Codex 职责是独立审查、修复和限定资格，不是单独改变用户政策或自行 production 解锁。
2. 在授权范围整理新的、独立的数据/证据候选，保留题号、数量与原件；绑定当前训练 manifest，补齐数据多样性、已知泄漏处理、资产和校准证据。不得把同核心换数当隔离，或回写冻结样本/旧锁。需要新冻结版本时另存，旧版本只读。
3. 核对构建期 token 长度检查和超长记录处理的实际实现及回执；配置中的 seq_guard 描述不是执行证明。落实参数合同、候选审批及各自精确 SHA；解决 TBD 和当前量化描述拒绝，不能仅改审批标志。
4. 由已审查的运行快照流程产生真实、绑定配置/manifest/源码状态的 run_record；不能手造 READY。只有 preflight --ready 的全部必需项与 harness 前置检查实际通过，且任务本身得到用户授权，才进入对应执行阶段。
5. 训练/扫参/评测在其实际授权与门禁范围内由 Claude 执行；产物、输入、模型和配置都须绑定版本。当前操作单不能作为立即运行的许可，也不承诺试训耗时。
6. holdout 方案必须先完成资格、隔离访问、独立标签、冲突裁决、规则锁定与独立复算等已约定材料，才能把真实最终验证结果作后续判定；不能训完才临时选规则或回看最终样本调参。
7. 后续审片、参数或数据修订遵循用户裁定；每轮保留完整记录。当前 harness 的分层目标为 R=1 且 E≥19/20、平台窗口 3 轮、上限 8 轮；UNVERIFIED 指标不能用于宣告达标。

## Holdout 的实际状态

391 是冻结来源池的候选数量，不是 391 条已获资格、已独立盲标的最终 holdout。
[当前角色登记](../archives/reviews/codex-supervision/2026-10-15-holdout-role-followup/ROLE_REGISTER.v2.pending.json) 仍为 PENDING_REAL_ROLE_AND_ISOLATION_EVIDENCE，eligible_count=null、qualification=NOT_GRANTED。独立 A/B/D 真实会话、封存输入/标签、裁决及最终规则/复算回执尚待交付。

用户后续若确认采用有限隔离启动策略，须明确该策略的适用范围与真实 holdout 设计如何对应；不能据“来源池冻结”替代上述资格事实。当前不加题、不扩大历史语料、不以重写数字构造伪独立评测。

## 命令速查

以下帮助和冻结校验不启动训练：

~~~powershell
& .\.venv\Scripts\python.exe -X utf8 -B tools\preflight.py --help
& .\.venv\Scripts\python.exe -X utf8 -B tools\freeze_data.py --check data\eval-v2.lock.json --manifest data\manifest.json
& .\.venv\Scripts\python.exe -X utf8 -B tools\freeze_data.py --check data\test-v2.lock.json --manifest data\manifest.json
~~~

完整 preflight 会执行可信环境渲染/数学 smoke，并非纯文件只读检查；需要模型路径、当前 manifest 和真实 run_id。仅在相应检查范围获准并完成真实快照后使用以下模板；本轮未运行：

~~~text
.venv/Scripts/python.exe -X utf8 -B tools/preflight.py --manifest data/manifest.json --model .models/qwen3-4b --ready --run-id <真实已登记run_id>
~~~

扫参和 train_loop 命令仅在前述准备、授权与全部门禁完成后执行，不能为生成快照或试探状态而先启动训练。runs/loop.stop 是训练循环的控制文件，与证据 consumer 的 runtime/STOP 不同；不要误删其他工作者控制文件。

## 职责和边界

用户决定政策与授权；Codex 独立核验、直接修复发现的问题、明确合格范围并归档回 Claude；Claude 按核验版本完成已授权的构建/运行并提交真实回执。新脚本或文档中的角色、时间和结论不能自行升级为用户指令。

D2/D8 外部 IPv6 延期 GAP 不阻塞训练准备；不等于已经完成训练、执行隔离或 production 解锁。其他真实缺证据、失败、准备检查分别记账。
