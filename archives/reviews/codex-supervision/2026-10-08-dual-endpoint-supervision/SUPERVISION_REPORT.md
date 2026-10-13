# Claude Code 双端实验监管与说明修复

2026-10-08 北京时间。本轮用户已授权开始双端实验，随后要求监管 Claude Code 的工作进程；以此最新授权覆盖此前本轮排除双端实验的范围限制。没有由邮件扩大授权，没有另起并发网络实验、生产放行、开训、提交或推送。

## 当前进度与资格

Claude Code 的 msg_755 确认 LAN 轮 lan-2026-10-08-a 发送侧完成，run remote-271e1c881c4f473fb027f5f28d4a3bd5。原始 sender.json 的 SHA256 为 f2ca09bd06173dc48ab19ee5798a24b14bbd986985cb26f8af6d8edd40744a6c。TCP 返回 Win10013；UDP 的发送调用完成，只能记 sent。原始 complete=true 指发送侧采集结束，verification_status 仍为 UNVERIFIED。

Codex 独立核验发送侧 15 个实现文件、采集器源码前后 SHA、真实源程序与原生父作业回执、路由与接口原始 stdout/stderr SHA、6 个不同 nonce，以及前对照→沙箱→观察→后对照时序。实际观察窗为 21000039700 纳秒，符合不少于 20000000000 纳秒条件。证据保持原字节，不重签、不改 nonce。结果见 sender-independent-verification.json。

待收 LAN 原始 witness_new_01.jsonl、同名 witness_new_01.jsonl.summary.json、接收器真实退出码，再由 Claude 对账并交 Codex 独立验收。msg_755 仅列 JSONL 与退出码，Codex 已在 msg_756 要求补收 summary。不能将接收端缺失当作零送达。

下一轮计划为 v6-2026-10-08-a，接收端新日志 witness_new_02.jsonl，同样必须交原始 JSONL、对应 summary 与真实 rc。所报 240e IPv6 与当前发送端原生接口的 2001:da8 前缀不同，也不处于同 /64；仅为当前拓扑初筛，正式外部资格需该轮新原生接口、原始接收材料和不同主机身份。未据此宣称外部实验通过。

本轮文档修复与本地工具验证合格；LAN 双端和外部 IPv6 双端均未验收通过。production=CLOSED，不给全 43 点证书。

## Codex 实际修复

1. reviews/2026-10-07-witness-runbook.md：将错误的 9 个 nonce 改为每轮 2 协议 × 3 阶段 = 6 个；补全原始 JSONL、同名 .jsonl.summary.json 和真实 rc；明确 PowerShell / cmd 退出码读取方式；接收器校验改为完整 SHA256；改正“接收器启动前先测通”的顺序；删除旧轮次复用指示，绑定当前 LAN run 并要求新轮唯一命名；明确 4 个健康对照 payload 和零 sandbox nonce，任何 sandbox nonce 被实际收到即边界 FAIL。
2. NEWRELEASE.md：当前索引汇总为 2711 条按题去重公式、5320 处原文出现，替换旧 2663 / 5212；逐像素复验限于本轮 75 个新页面起始帧，其余视频按父交付验证与当前哈希继承；删除从槽位代理大于 24px 推出最小字形通过的声明；559 完整页统计采用精确值：最小 92px、第十分位最近秩 484/3 px、中位 658/3 px；更新真实实验阶段，删除“唯一剩余验收项”和过期下午/旧日期轮次表述。
3. 只读观察器：旧 latest.json 心跳停在 11:13:03，实际旧进程不存在，停止原因未知。已检查无同名 watcher、无 STOP 后隐藏恢复，实际 worker PID 44524，launcher PID 31668，新心跳与实时 Claude 进程树已核实。原源码未改、旧日志保留；上午至恢复之间的观测空窗不补造，进程存在不当作计算进度或成功证明。后台只读记录，不执行 AI 审查或批准。

修复前后文档及统一差异见 before-*、after-*、documentation-changes.patch。采集器源码未改，当前已采集 run 的实现绑定继续有效。

## 验证与归档

- 采集/对账工具 30 项回归通过，实际工具执行回执摘要见 external-driver-regression.json。
- 接收器与 IPv4 联合策略 36 项回归通过，原始测试报告见 receiver-and-joint-regression.txt / .json；包含受控本机 IPv4/IPv6 回环验证，不能当作外部双端实验。
- 发送侧原件与实现绑定独立通过，见 sender-independent-verification.json。
- 恢复心跳、真正 worker PID、观察空窗见 watcher-restart-verification.json。
- 实际 Bridge 收件与发件回执存本目录；msg_754 协调分工，msg_755 是 Claude 当前状态材料，msg_756 已说明 Codex 修改、资格范围、缺失 summary，并要求按修复版本继续后续工作。
- delivery-manifest.json 只冻结本轮报告与快照，不冻结观察器或实验活动目录。收到接收端新材料后应形成新的独立审阅归档，不覆写本轮历史结论。
