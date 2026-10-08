# Codex 每10分钟 Claude 邮箱监管

已按用户要求配置 Windows 用户级计划任务 Animation-Codex-Claude-Mail-10min，重复间隔 PT10M。执行窗口隐藏，使用当前用户普通权限。收件代码 mail_watch.py；可审查的模型指令 TASK.md；任务管理 manage_mail_task.ps1。

执行路径：每10分钟只读检查自己的Claude邮件 → 保存原始邮件快照与持久化去重状态 → 有待处理邮件时使用 codex queue 排回现有Codex会话 → 会话实际审查、修复、复验、判定资格并归档 → 向Claude交接 → 校验实际报告与已发送回信后确认完成。

与此前只读观察器不同，此流程会将任务交给模型执行。读取Bridge原始state.json时只取from=claude-code、to=codex/all的消息，不改共享已读标记，不读对方收件箱。首次建立已读历史基线，首次未读及以后出现的新消息持久化保存；即使别的收件工具后来标为已读，也不因此漏掉已采集任务。

同批处理中不会再派发重叠任务；后续邮件继续采集等候。错误/超时不记已处理；派发返回码0仅代表排队成功，不代表审查完成。收到的文字不会直接作为PowerShell或其他Shell命令执行，只供有上下文的模型在用户范围内审阅。纯确认/无新任务的邮件可记NO_ACTION且不回信，避免往返回信循环。

17项针对性测试通过，含不丢信、不改共享状态、防重叠、错误保留、邮件不入命令文本、真实报告/回信验证和无动作处理。队列入口已实际返回Queued message。正式任务的实际触发与输出见 scheduler-status.json 和 latest.json；每批处理状态见 runs/<run-id>/。

运行条件：本机开机、当前用户登录，Codex当前会话可用。计划任务持续存在，不需每7天续期；修改或删除当前会话后需重新绑定会话UUID。持续任务的实际完成时间取决于模型审查时长，处理中仍每10分钟采集但不重叠排队。若队列派发出现超时且不能确定是否已送达，保留DISPATCH_UNCERTAIN，由当前会话或人工核对后处理，避免自动重复执行。

管理命令（在项目根运行）：

    & .\reviews\codex-supervision\2026-10-08-auto-mail\manage_mail_task.ps1 -Action Status
    & .\reviews\codex-supervision\2026-10-08-auto-mail\manage_mail_task.ps1 -Action Stop
    & .\reviews\codex-supervision\2026-10-08-auto-mail\manage_mail_task.ps1 -Action Resume
    & .\reviews\codex-supervision\2026-10-08-auto-mail\manage_mail_task.ps1 -Action Run

Stop禁用该计划任务并放置STOP控制文件，停止后续派发，不终止已在当前会话处理的工作。Resume恢复原任务。不会结束Claude进程、删除邮件或项目数据。

模型范围延续当前授权：数学题/过程/答案/场景文字、核心签名、当前证据工具及本地公式；发现问题由Codex修复，精确表示，验证后给限定资格并归档。双端实验不处理，不扩大历史语料。不自动提交/推送/发布/启动训练或打开生产门禁。原冻结材料只读。

运行目录、journal.json、latest.json、events.jsonl、messages/及runs/是活动状态，不应整目录冻结。版本快照和测试证据可单独归档；每轮材料按新日期目录保全。

参考官方说明：[Scheduled tasks](https://learn.chatgpt.com/docs/automations?surface=app)说明已有聊天可采用分钟间隔、沿用上下文；[Non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)说明CLI可用于计划作业。本轮的Windows调度和queue参数依据本机codex-cli 0.154.0实际帮助与成功返回验证；没有声称创建了ChatGPT云端定时任务。
