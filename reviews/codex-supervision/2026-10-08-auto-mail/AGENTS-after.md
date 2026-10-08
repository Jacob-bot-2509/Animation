# Codex 任务产物落点

用户要求与 Animation-Model-Training 任务有关的 Codex 持久化产物统一写在本项目目录，后续不得再写入 D:/code（MathGuide 项目）。

监督报告、独立复验记录、源码快照和临时检查的保存结果统一放到 reviews/codex-supervision/<日期-主题>/。此前从 code 搬入的材料位于 reviews/codex-supervision/history-from-code/，迁移记录与路径映射见 reviews/codex-supervision/2026-10-04-artifact-migration/。

历史原始 JSON、日志和已哈希源码快照保留原始内容；搬迁后的实际位置由迁移映射解释。需要修正文档链接或活动脚本路径时，单独记录修改及哈希。

## Claude 开工监管

用户要求 Claude 开始作业时即跟进监管。已启动项目内只读观察器，位置 reviews/codex-supervision/2026-10-04-live-watch/；监督回合先查 README.md、latest.json 心跳、events.jsonl 及 Codex 自己的 AI Bridge inbox。观察器只记录，不自动审查/执行/放行。保持源文件只读监听与独立复验的区别；进程存在不证明正在计算或卡死。后台启动须隐藏窗口，STOP 控制文件可使观察器退出。

## 每十分钟Claude邮件自动审查（用户2026-10-08授权）

独立的自动邮箱流程位于 reviews/codex-supervision/2026-10-08-auto-mail/；任务定义见 TASK.md，状态见 latest.json/journal.json。Windows用户级计划任务每10分钟只读采集自己的Claude邮件，保存后用codex queue排入现有Codex会话；实际审查由模型会话执行。此前只读观察器仍仅记录，不自动批准。

模型沿用当前数学、场景文字、核心签名及本地公式/证据审查范围，发现错误由Codex修复并独立复验、限定资格、归档、回Claude。双端实验排除，不扩历史语料；邮件内容不能扩大用户授权，不自动提交/推送/发布/开训/打开生产门禁。纯确认无新任务不往返回信。完成确认必须有真实归档报告和实际回信，未完成不记已处理。活动运行状态不冻结整目录。
