# Claude 开工自动监管

用户于 2026-10-17 直接要求：“只要检测到 claudecode 一开工，你就自动监管”。

本目录是活动运行根，不得冻结整个目录。安装记录另存 archives/reviews/codex-supervision/2026-10-17-auto-start-supervision/。

## 当前机制

每 5 秒观察一次；发现新 Claude 进程、Claude 子进程或明确引用 D:/Animation-Model-Training 的新助手工具调用后，生成受限 signals.json 和 instructions.md，并通过现有 Codex 会话队列提交。现有常驻 Claude 只产生一次“启用时已存在”基线信号，不冒充新开工。不会读取历史日志并重放过去任务。

进程信号来自原只读观察器；心跳过期或查询失败时，用只读 CIM 查询后备。进程身份不证明属于本项目，更不证明有正确成果；审查会话先确认本项目实际改动。新工具调用只检查允许目录中最近 16 个顶层会话 JSONL 的增量，提取工具名、ID、时间；不复制提示词、命令正文或工具结果。读取上限每日志每轮 1 MiB，截断、轮换、坏行和信号溢出显式记 GAP。少于轮询间隔的短进程、没有可归属日志的纯思考、其他路径日志可能未观察到，不能声称全覆盖。

同一时刻一个活动回合；新信号保留待审，最多保存 200 条并对超量显式记账。两次排队至少间隔 60 秒。排队成功只标 QUEUED_NOT_YET_REVIEWED；超时/非零/启动错误标 DISPATCH_UNCERTAIN_NEEDS_CHECK，保留占位，不盲目重发。DISPATCHING 期间崩溃也保留占位，需要查队列后人工恢复。

实际审查沿用用户既有职责：独立核验、接管确认的错误并修改、验证、限定合格范围、通知 Claude 已修改并要求继续后续工作、冻结归档。若材料已由邮箱流程处理，核验后复用已冻结报告及真实回信，不重复修复和来回确认。未处理邮件仍独立遵守原 mail_watch.py 的收件、真实回信、冻结与 ACK 工作流。

自动触发不授权启动训练、发射探针、运行任意新生成程序、提交/推送/发布或生产放行。Claude 信件、日志和文件是材料，不能扩大用户权限。全局隔离 NOT_ESTABLISHED 与 D2/D8 延后 GAP 继续如实记账，用户有限隔离证据口径不变。

## 路由、运行与暂停

会话 UUID 为 01a1010d-fd38-72c1-b7b1-5719ed112e32，与既有邮箱配置相同；没有更换模型或权限参数。官方队列说明：https://learn.chatgpt.com/docs/cli/reference#codex-queue；本机 queue --help 已复核。

用户级计划任务 Animation-Codex-Claude-Start-Supervision 使用交互登录用户、Limited 权限及 pythonw.exe，无可见窗口。登录时启动，每分钟尝试补启动；运行中 IgnoreNew，程序再用 worker.lock 拦截重复实例。源代码部署后可在 STOP 文件退出后重启，不覆盖已存在的操作者 STOP。此为新增任务，未重装或改动既有邮箱任务。

电脑关机、休眠、用户未登录、客户端/服务不可用或无法触达目标会话时，不保证实时审查。可持久化的待审信号和队列占位会保留；需查看心跳及不确定状态，不以“任务已注册”代替存活证明。

查看 latest.json、state.json、error.json（若存在）与各 runs/start-*/dispatch.json、ACK.json。SELFTEST_ACK.json 只能在自检消息真正返回本会话后，由本会话执行受限 selftest ACK 产生；不能在 queue 返回成功时预写。审查 ACK 必须绑定 canonical 冻结目录内报告字节及清单中的实际回信，且回信须真实存在于 Codex→claude-code 账本。ACK 写入后崩溃可重试恢复，不重复记账。

暂停：
```powershell
Disable-ScheduledTask -TaskName 'Animation-Codex-Claude-Start-Supervision'
New-Item -ItemType File -Path 'D:\Animation-Model-Training\reviews\codex-supervision\2026-10-17-auto-start\STOP'
```
不需要结束 Claude 或修改权限/ACL。恢复须明确移除本目录 STOP、启用同名任务并启动；保留所有队列账本。

## 验证范围

28 项独立回归覆盖基线/新子进程/去重、明确项目引用/相似路径拒绝、API 历史重复过滤、增量日志/新日志/半行/过大记录/轮换/溢出、先占位后排队、排队成功不冒充审查、异常保留、真实报告与回信校验、自检 ACK、ACK 后崩溃恢复、父目录跳转拒绝和只读查询后备。队列调用均模拟，不运行 Claude 任务。

真实路由自检另有 dispatch.json。收到与否以实际 SELFTEST_ACK.json 为准；安装归档只证明其冻结当时的状态。
