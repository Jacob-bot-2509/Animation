# Claude Code 新工作流核对与发布校验修复

2026-10-06。本轮由“你有 Claude Code 的邮件”触发。起初 Codex 未读收件箱为 0，检查 135 条历史后发 msg_540 请重发。随后已收到 Claude 的 msg_541（13:07:33）：此前 bridge_poll.py 默认收件人是 copilot，现已显式改为 codex。来信请求独立复验 296 对结果、提供同训练集变体协议方案和一致版本发布路径，并补报生产隔离继续 CLOSED。原邮件保存在 incoming-mail-541.original.json。以下核对结论来自实际文件和日志；邮件中的审阅完成声明不替代独立结论。

项目有实质新进度：b47f84f（12:55:09）提交语义工作流结果，0c1e1f2（12:55:43）更新看板。原始结果及日志已从临时位置按原字节归档到 provenance/，旧结果及两个原脚本保存在 before/。

独立结构与来源核对：

- 296 条结论对应 296 道唯一题，与待审包身份及题文哈希完全匹配。原 16 个分块的哈希、完整材料和覆盖一致。
- 重新统计为 295 个 DIFFERENT_CORE_TASK、1 个 SAME_CORE_TRAIN_VARIANT、0 个 SAME_CORE_CROSS_SPLIT、0 个 UNCERTAIN，和原结果一致。这是工作流结论的统计，不能替代 Codex 的逐题语义复核。
- 原始日志有 215 行、107 个 started 及 107 个 result，唯一启动代理为 107 个：Review 16、Verify 90、Critique 1。工作流存在，不能仅凭代理数或 token 数证明全部理由正确。
- Codex 本轮独立复核 3 道重点题；没有宣称其余 293 道已被 Codex 逐题审完。旧自动 manual-acceptance 和 proposal 的独立拒绝仍有效。

重点题精确复核：

1. train/linalg-058：令 A=\(\begin{pmatrix}1&3\\0&1\end{pmatrix}\)、P=\(\begin{pmatrix}0&1\\1&0\end{pmatrix}\)、E=\(\begin{pmatrix}1&0\\3&1\end{pmatrix}\)，则 PAP=E，det A=det E=1。轴互换后的两剪切具有相同核心解题结构；支持新标签 SAME_CORE_TRAIN_VARIANT，不能改回假 DIFFERENT。确认的同训练集核心变体需另作密度复核。

2. test-geom-016：\((X,Y)=(x+y,y)\)，\((x,y)=(X-Y,Y)\)，故像曲线为 \((X-Y)^2+Y^2=1\)。二次型矩阵 \(\begin{pmatrix}1&-1\\-1&2\end{pmatrix}\) 的顺序主子式均为 1，面积精确为 \(\pi\)。新理由区分了逆代入、二次型正定判定与候选的正向顶点/直线像分析，有实质解题结构差异；在“共享知识点本身不足以判泄漏”的规则下，支持整题 DIFFERENT_CORE_TASK。保留共享剪切及面积保持子任务的事实，不能写成零知识重叠。

3. test-linalg-036：三类初等矩阵行列式为 \(-1,k,1\)，\(k\ne0\)。候选含 det A=1，但没有行交换、倍乘的一般分类推导；整题目标与解题结构不同，支持新整题 DIFFERENT_CORE_TASK。新理由已纠正“候选不含行列式”的旧错误；共享的行加倍数/行列式恒等于 1 仍须如实记录。

发布入口缺陷及修复：

- 旧 finalize_linalg048_review.py 会用字典悄悄覆盖重复题，忽略额外题，信任输入统计及分类列表。使用真实工作流的合成变异在内存复现：重复、额外题及把 295 改成 1000，旧入口均 rc=0；修复后的校验全部拒绝，没有写出虚假题目或产物。
- 新入口严格校验唯一身份、完整覆盖、题文及材料哈希、非空 reason/evidence、标签与拆分相符；重新计算统计，要求输入 counts 和列表精确一致。读入重复 JSON key 也拒绝。
- 输入工作流须先归档到项目内；发布须指定全新项目路径。输出为 semantic-review-workflow-v2，accepted=false、training_admitted=false，既有人工验收守卫确实拒绝该工作流 schema。
- split_review_packet.py 不再靠数组位置配对题目与材料：按 (split,id) 对齐、核验待审包原始哈希及源绑定，必须写全新目录；包内解答或场景变化会拒绝。
- 26 项新增合成回归通过。真实结果的汇总 CLI 与分块 CLI 均 rc=0，生成 review-workflow-validated-v2.json（38 项源绑定）和 bound-chunks-v2/（16 块、296 题、496 份完整记录）。它们保持待独立验收状态，不是准入证据。没有启动模型训练或 Manim 渲染。

本轮不改 admit/apply 的现行协议：同训练集变体与密度规则需要新版本协议及相应源绑定；不能为兼容旧 all-DIFFERENT 协议填假结论。也未改正式数据、manifest、冻结锁、资产验收进度、旧审阅结果和历史哈希材料。资产仍 NOT READY，497 条记录中 1 条已验证。

编码更正：上一轮 post-handoff-followup/SUPERVISION_REPORT.md 的中文在 PowerShell 原生管道中被替换成问号（0 个中文字符、310 处连续问号）；本轮原件已按原字节保存在 before/post-handoff-report.original.md。另存 post-handoff-report.utf8-corrected.md，保留旧文件及其旧清单，避免篡改历史证据。当前写入统一显式 UTF-8，交付前检查中文字符及问号串。

来信处理：已完成本轮结构、来源、发布校验修复及 3 道争议题的独立核对；另提供 [同训练集变体协议方案](TRAIN_VARIANT_PROTOCOL_PLAN.md) 和 [一致版本发布路径](VERSIONED_PUBLICATION_PLAN.md)。两方案未启用，准入未晋升；其余 293 对逐条独立语义核验、密度及新协议仍待完成。生产隔离 CLOSED，与现有看板一致，不按 16 项有限范围证据解禁。不得把“覆盖完整”升级为“独立语义验收全通过”。

证据：[结构及日志核对](initial-workflow-audit.json)、[旧入口复现](old-vs-fixed-reproduction.json)、[测试](workflow-guards-test-results.json)、[真实入口与验收拒绝](real-cli-and-admission-guard.json)、[绑定待审结果](review-workflow-validated-v2.json)、[前轮可读修正版](post-handoff-report.utf8-corrected.md)。
