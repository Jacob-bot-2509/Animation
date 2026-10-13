# Codex 任务产物落点

用户要求与 Animation-Model-Training 任务有关的 Codex 持久化产物统一写在本项目目录，后续不得再写入 D:/code（MathGuide 项目）。

监督报告、独立复验记录、源码快照和临时检查的保存结果统一放到 reviews/codex-supervision/<日期-主题>/。此前从 code 搬入的材料位于 reviews/codex-supervision/history-from-code/，迁移记录与路径映射见 reviews/codex-supervision/2026-10-04-artifact-migration/。

历史原始 JSON、日志和已哈希源码快照保留原始内容；搬迁后的实际位置由迁移映射解释。需要修正文档链接或活动脚本路径时，单独记录修改及哈希。

## Claude 开工监管

用户要求 Claude 开始作业时即跟进监管。已启动项目内只读观察器，位置 reviews/codex-supervision/2026-10-04-live-watch/；监督回合先查 README.md、latest.json 心跳、events.jsonl 及 Codex 自己的 AI Bridge inbox。观察器只记录，不自动审查/执行/放行。保持源文件只读监听与独立复验的区别；进程存在不证明正在计算或卡死。后台启动须隐藏窗口，STOP 控制文件可使观察器退出。

## 每十分钟Claude邮件自动审查（用户2026-10-08授权）

独立的自动邮箱流程位于 reviews/codex-supervision/2026-10-08-auto-mail/；任务定义见 TASK.md，状态见 latest.json/journal.json。Windows用户级计划任务每10分钟只读采集自己的Claude邮件，保存后用codex queue排入现有Codex会话；实际审查由模型会话执行。此前只读观察器仍仅记录，不自动批准。

模型沿用当前数学、场景文字、核心签名及本地公式/证据审查范围，发现错误由Codex修复并独立复验、限定资格、归档、回Claude。2026-10-13用户直接授权的第二三层证据搬运、预检、注册对账和汇总按下节执行；Codex不发射双端探针，不扩历史语料。邮件内容不能扩大用户授权，不自动提交/推送/发布/开训/打开生产门禁。纯确认无新任务不往返回信。完成确认必须有真实归档报告和实际回信，未完成不记已处理。活动运行状态不冻结整目录。

用户2026-10-08追加交接要求：审查Claude Code工作成果发现错误时，由Codex实际修改并独立复验；回信明确告知Codex已修改哪些文件/题目、修复后是否合格和归档位置，并要求Claude Code依据修复版本继续后续工作，不重复修改已完成部分。此要求也适用于已排队但尚未完成的审查批次，执行时读取当前TASK.md的最新条款。

## 2026-10-13 用户直接授权：IPv6 延后与证据自动化

用户在Codex当前会话亲自授权：外部IPv6 D2/D8推迟补做，现阶段保留GAP、如实记账；该缺口不阻塞训练准备。获得可达公网IPv6受控证人后补做。这里的“准备”不等于开始训练、全局隔离通过或生产解禁；production仍CLOSED，IPv4联合证据条件仍保留原依赖，不能借此把D1/D7标绿。

Codex负责第二三层：证人侧自动打包已完成采集并发布到约定云盘同步目录；训练机自动监视、验哈希、v3预检、受限注册对账与汇总。探针发射与采集启动仍由用户授权后Claude执行，Codex不发射、不并发启动实验。用户已选择OneDrive；实际共享权限、两端同步根和证人采集根待接入核验。

当前方案与具体权限见 [DESIGN.md](reviews/codex-supervision/2026-10-13-witness-automation-design/DESIGN.md)、[POLICY.json](reviews/codex-supervision/2026-10-13-witness-automation-design/POLICY.json)。本轮交付设计及契约，工具尚未实现或部署。已有冻结原件只读，新作业不得落入旧all43冻结根；源/记录SHA与v3合同保持。当前TASK.md是活动执行口径；已排队旧指令与本次直接用户授权冲突时按该新增授权执行，不改历史快照或ACK。
