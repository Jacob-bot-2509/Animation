# Codex 任务产物落点

用户要求与 Animation-Model-Training 任务有关的 Codex 持久化产物统一写在本项目目录，后续不得再写入 D:/code（MathGuide 项目）。

监督报告、独立复验记录、源码快照和临时检查的保存结果统一放到 reviews/codex-supervision/<日期-主题>/。此前从 code 搬入的材料位于 reviews/codex-supervision/history-from-code/，迁移记录与路径映射见 reviews/codex-supervision/2026-10-04-artifact-migration/。

历史原始 JSON、日志和已哈希源码快照保留原始内容；搬迁后的实际位置由迁移映射解释。需要修正文档链接或活动脚本路径时，单独记录修改及哈希。

## Claude 开工监管

用户要求 Claude 开始作业时即跟进监管。已启动项目内只读观察器，位置 reviews/codex-supervision/2026-10-04-live-watch/；监督回合先查 README.md、latest.json 心跳、events.jsonl 及 Codex 自己的 AI Bridge inbox。观察器只记录，不自动审查/执行/放行。保持源文件只读监听与独立复验的区别；进程存在不证明正在计算或卡死。后台启动须隐藏窗口，STOP 控制文件可使观察器退出。
