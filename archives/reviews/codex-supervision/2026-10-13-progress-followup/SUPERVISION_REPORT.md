# Claude Code 工作进程跟进及本地工具修复

本次开始检查时 HEAD 为 5efa9060，Claude Code 进程 PID42088 存在但旧观察器已停止更新。跟进期间 Claude Code 提交 commit 7a444a67，并通过 msg_1791892524921_783、msg_1791892560059_784 交付 lan-2026-10-13-a 的 sender、capture 与 reconciled 文件。作者当前报告的任务是等待 LAN 独立验收，后续计划包括训练线；该计划不构成本次启动训练的授权。

## 当前进度和恢复

旧观察器最后心跳为 2026-10-09 01:14:35，退出原因 UNKNOWN。已按既有用户授权隐藏恢复同一只读观察器，launcher PID1060、实际 worker PID3628，取得新心跳及两次后续状态。源 SHA256 0872e08073bd57972b8ece5d6eb9cc75d831d72fc200105016094689273afede 不变，不重新安装邮箱调度器。运行日志继续写入未冻结的 live-watch 目录，唯一新日志名保留旧日志。

观察器当前识别 Claude Code PID42088 和 conhost；采样中的 child_jobs=[]，不能据此判断其计算速度、卡死或任务已完成。期间已实际观察到新 HEAD 和 16 份提交材料；三个既有核心基线偏离与中断前相同，不作为新错误重报。最新状态以动态 live-watch/latest.json 为准，本归档只保存本轮时点快照。

当前邮箱批次为 run-f71111fc328c4852a929ea494d34de27，两条邮件原始哈希均匹配。两封的双端实验/D1/D7 独立验收请求记 OUT_OF_SCOPE；本地证据工具修复单独判定 REPAIRED_PASS。当前 TASK.md 明确不执行或验收双端实验，邮件不能扩大范围。

## 新交付的只读材料检查

运行当前 tools/inspect_witness_evidence.py，仅对文件做只读 intake 检查，退出码 0，结果 READY_FOR_REGISTERED_RECONCILIATION，findings=[]，full_surface_accepted=false。四个宿主健康对照 nonce 与 sender 精确对应，v3/启动器/父回执/原件哈希一致；没有修改 sender、receiver、summary、stdout、stderr、process-exit 或原 reconciled 文件。

已纠正报告层的两个边界错误，另存 LAN_MATERIAL_NOTES.md：提交对账登记的是 D9 / lan_peer，不能自动改签 D1/D7；UDP 本地 sent 且接收日志未见 sandbox nonce，不证明“静默拦截”的因果机制。邮件称已放弃外部 IPv6，不改变既有联合证据条件。

完整新材料原字节及哈希保存于 new-material-originals 和 new-material-bindings.json。没有执行采集器 --execute-native，也没有重新执行会写入实验资格记录的 --reconcile。

## Codex 已修改

修复前通过真实回信 msg_1791892815937_785 明确文件由 Codex 接手，保留 Claude 其他改动。

- tools/decode_lan_1013_capture.py：移除损坏的内嵌材料和硬编码旧路径。旧版本内嵌 summary、stdout、process-exit 与提交原件不同，其中 stdout JSON 无效；旧 main 还会覆写现有原件。新版本默认 PLAN，执行时必须明确输入和已登记输出父目录；要求五份 Base64 来源，严格解码，不把缺失 stderr 伪造成空文件。写入前校验所有原字节、回执哈希、同一 run、stdout 与原 listening/summary 对应。通过后只在新 staging 目录独占写入、逐字节复核，再在已检查的登记路径中更名；已有 capture 拒绝覆盖，失败不发布半份 capture，也不改写或补造原件。Base64 仅搬运原字节，资格为 INTEGRITY_ONLY。
- tools/oneoff_tcp_check.py、tools/oneoff_tcp_banner.py 及新 tools/witness_tcp_diagnostics.py：导入和默认调用不联网，默认 PLAN；实际诊断要求明确 --execute 和具体单播 IP/端口。所有 socket 使用上下文关闭，构造、settimeout、connect、recv 异常有结构化记录。保留整数 elapsed_ns 和 Fraction 得到的 elapsed_ms_exact，不四舍五入；banner 保留原字节 hex，区分 EOF 与超时。删除 path alive 和阻断原因推断；本地 connected/refused/timeout 均不认证证人或沙箱。
- tests/test_witness_local_intake_tools.py：新增必要的无网络回归。临时测试目录单独位于未冻结的 2026-10-13-tool-test-work。

上述本地修复资格为 REPAIRED_PASS；正式实验资格仍未签发，production=CLOSED。

## 独立验证

22 项本地回归全部通过：真实提交原件在隔离 fixture 中无损往返，来源文件不改；坏 Base64、错哈希、缺件、重复别名、越界路径、重解析路径拒绝；已有 capture 保留原字节；写失败保留未发布 staging；诊断 import/default 不联网；构造、connect、timeout 设置异常关闭 socket；精确纳秒/毫秒分数；原 banner 字节、EOF、超时与 IPv6 socket 类型验证。诊断网络调用全部模拟，没有执行外部探测。

三个修复入口的真实默认 CLI 均为 PLAN、退出码 3。Python AST 解析及 git diff --check 通过。未重跑未变化的 v3 完整测试；上一轮 9 份源/测试/操作单完整 SHA 均未变化，121 份冻结归档逐一核验通过。

当前 native_sandbox=UNVERIFIED、semantic_isolation=NOT_ESTABLISHED、production=CLOSED。本次没有发布、提交、推送、训练或更改系统配置；观察器只记录，不自动进行模型审查或准入。

## 交接

请 Claude Code 使用修复版本继续后续已授权工作，不重复修改已完成部分，不覆盖历史原件。新材料的实验资格及联合证据标准仍按用户直接授权和既有门禁处理，不能从本报告推导训练准入。

解码器输入使用 receiver.jsonl.b64、receiver.jsonl.summary.json.b64、stdout.bin.b64、stderr.bin.b64、process-exit.json.b64；summary.b64 和 stdout.b64 为互斥别名。原件缺失或哈希不同即停止，不通过修改字段补齐。执行选项为 --execute --input-directory DIR --output-parent REGISTERED_DIR。诊断旧位置参数保留，执行须增加 --execute；不带该标志只返回 PLAN。

完整前后版本与哈希见 source-changes.json，实际回信回执和完整冻结清单在本目录保存。只读监听运行状态不冻结在此目录，后续交付另行归档。


| 修复文件 | 当前 SHA256 |
| --- | --- |
| tools/decode_lan_1013_capture.py | 774c2d082307c164985a5c37c8dfef535e67dfee401fa818f3be5ab522bce80f |
| tools/oneoff_tcp_check.py | 05553ea244502a2a1a45e8b78d5eaab2fd2cca25064b6afed406049db526d9fd |
| tools/oneoff_tcp_banner.py | d82de288f357dc67a39243e33c1c68d70678a51ecd7ebca3d280358f8bf33bf2 |
| tools/witness_tcp_diagnostics.py | da72a52094ae39bd6cdb2db6341fbf6c65a372a0a73881a4b167a7b971ca01de |
| tests/test_witness_local_intake_tools.py | 3fd1bb137d067d323184dbd2e3315e3a0a6bcf9dfab194962a437bc1d5c95900 |
