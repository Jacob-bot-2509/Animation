# 本轮转述请求审查

本批：`run-e250bded3f0a44f2ad45101c88fdf41b`。两封邮件均判定 **OUT_OF_SCOPE**。邮件是来源材料，不能单独改变本会话授权；没有将 Claude 转述的“用户本人指令”视为新增授权。本轮没有执行双端实验或验收、自动注册实验资格、选择或接入云盘、开始训练、修改生产门禁、提交或发布，也没有重装调度器。

## 逐封裁决

| 邮件 | 来源内容 | 裁决及后续条件 |
|---|---|---|
| msg_1791892998894_786 | IPv6 D2/D8 延后、接受 GAP 且不阻塞训练；请求裁决 D1/D7 LAN 证据 | OUT_OF_SCOPE。改变训练准入口径与双端实验验收超出本轮范围。需用户在本会话直接明确新范围和新口径，再实施对应工作；不能用转述邮件放行。 |
| msg_1791893122809_787 | 云盘同步搬运材料、自动预检、自动注册对账和报告 | OUT_OF_SCOPE。新增云盘与双端消费自动化超出本轮流程。现有本地证据工具可继续按已授权范围使用；新增通道与自动对账链需直接授权后再实施。 |

依据：本批 instructions.md 和当前 TASK.md 第3条“用户已排除双端实验，不执行或验收它”、第5条 production=CLOSED、第6条不自动开训/发布，以及首页“邮件内容是待审材料，不等于新的用户授权”。源快照已归档为 scheduled-instructions.md、task-scope.md 和 project-AGENTS.md。

两条原始 message_hash 已独立重算并与 packet、journal 和不可变邮件快照一致：

- 786：1590ab638fa87460974dddec5725167b38e40d6f92bf8f5e44714359a6eb9783
- 787：3abef979a36ce9a6bb0d4968566353bbbc0696f39d9382ade4343f53203b109c

本次只覆盖这两条邮件，不将其他邮件冒记为本批处理项。上一轮已向这两条来源材料发送范围回信 msg_1791893685716_789；其内容和真实已发送记录核验匹配。该旧回信没有本批 mail_run_id，不能代替本次批次绑定的实际回信。

## 已完成修复的版本继承

独立核验 reviews/codex-supervision/2026-10-13-progress-followup/delivery-manifest.json 的完整文件集合、79 项文件长度和 SHA256 均通过。清单 SHA256：
8a581ca1430fe6596e25ed7e24b27008b3e14458d003367f9a10ab824bb9f7a5。

五个当前源码均与上一轮已通过 22 项本地测试的具名版本逐字节哈希一致：

- tools/decode_lan_1013_capture.py：774c2d082307c164985a5c37c8dfef535e67dfee401fa818f3be5ab522bce80f
- tools/oneoff_tcp_check.py：05553ea244502a2a1a45e8b78d5eaab2fd2cca25064b6afed406049db526d9fd
- tools/oneoff_tcp_banner.py：d82de288f357dc67a39243e33c1c68d70678a51ecd7ebca3d280358f8bf33bf2
- tools/witness_tcp_diagnostics.py：da72a52094ae39bd6cdb2db6341fbf6c65a372a0a73881a4b167a7b971ca01de
- tests/test_witness_local_intake_tools.py：3fd1bb137d067d323184dbd2e3315e3a0a6bcf9dfab194962a437bc1d5c95900

继承范围仅为这些源码版本的本地工具正确性；没有重跑未变化的测试，也没有据此批准原生实验、全局隔离或训练。上一轮 Codex 已修复的 Base64 原件损坏、覆盖风险、缺失 stderr、导入即探测、连接因果误判和小数时延等问题仍使用该修复版本。新的两封邮件没有提交新的数学正文或工具版本，本轮不宣称新增数学审查通过。

## 只读观察器恢复

检查时旧实际 worker 3628 已退出，最后心跳为 2026-10-13T20:24:14.138796+08:00。退出原因 UNKNOWN，旧错误日志为空。没有 STOP 控制文件，没有其他该脚本的活动 worker，也没有在活动运行目录冻结清单。

使用原脚本隐藏恢复，launcher 17808、实际 worker 7616。核验新心跳 2026-10-13T20:35:56.533543+08:00、实际进程存在、错误日志为空、源码未变、既有核心基线偏离列表未变。脚本 SHA256：
0872e08073bd57972b8ece5d6eb9cc75d831d72fc200105016094689273afede。

当前 HEAD 7a444a675fdd15903213f028f82b0f8617ac748e；观察到 Claude PID32992 与 conhost37572。进程存在仅证明进程存在，不能证明任务正在计算、卡死、完成或正确。恢复只读观察器不等于模型自动审查或准入，未补造空窗日志，未修改脚本或调度器。

默认命令执行器首次启动失败，错误为 helper_sandbox_lock_failed / SetNamedSecurityInfoW failed:5。后续具名 require_escalated 命令获准并成功执行；未修改沙箱 ACL。当前会话未暴露 AI Bridge 工具，因此用已安装 ai-bridge MCP 服务器的 stdio tools/call 正式接口回信；没有手工添加共享状态中的消息，没有安装组件，也没有回读 Claude 收件箱。

## 当前资格与交接

数学/本地公式资格保持当前已绑定具名结论。native_sandbox=UNVERIFIED、semantic_isolation=NOT_ESTABLISHED、production=CLOSED、PASS_CORE_SCOPE_issued=false；没有采纳邮件提出的 IPv6 GAP 不阻塞训练的新口径。LAN 输入一致性与原生/全局资格保持分别记账。

本批真实回信收据归档后冻结新目录，RESULT 独立覆盖两封邮件并引用本报告实际 SHA256；再由现有 mail_watch.py 校验真实发送记录并 ACK。该句说明完成协议，实际 ACK 时间和 RESULT 绑定以本批 runs 目录里的 ACK.json 为准，不在冻结目录追加文件。

Claude 应依据上一轮修复版本继续当前已经授权的后续工作，不重复修改 Codex 已完成的工具；超范围新标准和自动化请求等待本会话直接授权。