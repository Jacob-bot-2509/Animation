# 新训练操作单与扫参选择器监督修复

对应用户“继续跟进”及提交 7b895433；并接收邮件 844、846，批次 run-17a1d8b08693485e8792734e0a625892。

结论：**REPAIRED_PASS_LOCAL_SELECTION_AND_RUNBOOK。** Codex 已实际修正新 Runbook 的准入/来源/能力表述，并修复扫参选择器的精确分数异常和无验证指标仍选胜者问题。最终 10 项相关回归通过；本次不签训练 READY 或 production 解锁。

## 已修改文件

- docs/TRAINING-START-RUNBOOK.md：删除无绑定回执的“01:4x 实测”及不完整 PASS/FAIL 清单；区分 watch 部署和训练门禁、用户政策和邮件转述、391 候选池和最终 holdout；改为当前真实只读事实、8 项 READY 必需项与额外数据多样性检查。
- tools/hp_sweep.py：使用精确分数、VERIFIED 状态及整数 passed/total 交叉验证；拒绝布尔/浮点/非法分数/计数矛盾，分母须匹配实际总题数；没有可验证执行/渲染主指标时不选胜者、不开 winner 配置，返回失败。数学指标不能单独决定执行胜者。
- tests/test_hp_sweep_selection.py：新增 10 项回归；包含极接近 1 的有理数精确比较，以及整个 main 在模拟评测全未知时不输出 winner 的行为。Markdown 报告仍显示未入选的未知指标候选及明确的 NO_VERIFIED_WINNER，避免空表误导。

保留所有超参/模型配置、旧原件、冻结锁和已部署服务。没有替用户批准参数、改 calibration 标记、补造资产或执行证书；没有 Git 提交、推送、训练、模型加载、真实模型评测、渲染 smoke 或原生探针。本次 main 路径测试的训练/评测均由隔离 Mock 替代，未导入执行模型的路径。

## 实际发现与复验

旧版先复现：
1. 对当前精确分数字符串直接取负导致 TypeError。
2. 全部 UNVERIFIED 时按候选顺序产生 winner，模拟 CLI 返回成功。
3. 对计数/状态/非法数值没有当前合同要求的验证，无法区分未知指标和可用于选择的测量。

修复后最终 10 项测试全通过；原始先失败、修复后及最终输出均归档。只对改动相关逻辑测试，不重跑未变化的 consumer 35 项回归。此通过限于选择/报告的合同与新文档，不是对真实训练或所有未来扫参步骤的端到端认证。

## 当前准备缺口：只读事实

本轮只读事实时间 2026-10-17T01:44:55.810221+08:00，详见 current-read-only-facts.json：
- 两份当前 eval/test 冻结锁均通过 --check 与 manifest 绑定，退出码为 0。
- check_exec_isolation 返回未联合验收，data/execution_evidence.json 缺失。
- check_training_diversity 返回审查证据缺失。
- calc-area-007 的资产记录缺 output 对象；这里只核验结构，未代为渲染或补产物。
- hp_sweep dataset_manifest=TBD；实际候选并非二乘二网格。center-confirmed 虽记录 CONFIRMED，真实参数校验仍返回 Unreviewed quantization；其余 3 项为 PROPOSED。
- pilot_count=78 是配置元数据，当前实现实际用 subset.count（缺省 20）抽 eval 子集，不是已实现 78 条训练子集。
- 当前选择器不是 eval_loss 选优；评测代码的 R/E/M/F 仍为 UNVERIFIED。不能把配置愿景、schema 诊断或进程成功当真实动画质量。
- 391 是冻结来源候选数，当前角色登记 eligible_count=null、qualification=NOT_GRANTED，真实独立隔离/标注/最终验证仍待落实。

完整 preflight 会运行环境 smoke，本轮未执行，所以不宣称“仅三个 FAIL”或给 GPU/模型/环境项补写 PASS。Runbook 已改成真实范围与可核验链接。

## 两封新邮件的分别裁决

844：部署记录补充已接收，首启动/STOP 包装/最终居民实例的身份对应与上一轮已验收结论一致；本轮归档作者提供的 10 项清理对象和动作说明，不执行清理、不扩查个人云盘或 D:\tmp，也不把作者授权转述当 Codex 新权限。该项 PASS，范围仅补充记录与既有版本继承。

846：它仍是 claude-code 发来的“用户在其会话确认方案 A”的来源材料，不是当前 Codex 会话中的用户直接消息。已登记为 MAIL_REPORTED_POLICY，尚不作为新增启动权限，NEEDS_EVIDENCE 仅针对当前口径的授权来源/适用范围。没有要求其反复转发同一断言，也没有新增“事前证明全部全局隔离”的技术门禁。

若用户后续直接明确有限隔离策略，按其真实范围更新；仍需区分执行证书、数据多样性、资产、校准、参数合同和 run_snapshot 等当前实际检查，不把 391 来源池自动升级为已独立验收 holdout。即使暂不讨论策略问题，上述具体执行条件也尚未满足，当前不能启动。

## 后续交接

要求 Claude 按 Codex 修复版本继续，不重复修改本轮完成部分，不依据旧 Runbook 启动训练/评测/探针。下一步先提交有真实绑定的准备材料或具体已授权修订，不生成假 READY，不擅自修改参数审批/hash 或已有冻结材料。

consumer/watch 与只读监听继续原样运行。production=CLOSED、全局隔离 NOT_ESTABLISHED、原生沙箱 UNVERIFIED；D2/D8 延期 GAP 只不阻塞训练准备，不等于开训。

本目录保存完整前后版本、只读事实、回归输出、来源消息及真实交接回执；新文件/合同核验见 verification.json。归档 archives/reviews/codex-supervision/2026-10-17-training-runbook-review/；兼容副本 reviews/codex-supervision/2026-10-17-training-runbook-review/ 用于原 ACK。
