# Claude 开工监听与监管记录

用户要求：Claude 开始作业时立即跟进监管。监听已于 2026-10-04 17:49 启动，实际观察器 PID 50932。

## 监听与审查的区别

后台 Python 观察器约每 5 秒采样 Claude 父子进程树、Git HEAD、具名代码文件 SHA 和 11 个核心基线；启动/结束、提交、文件改变和基线偏离记录到 `events.jsonl`，当前心跳在 `latest.json`。它只读源文件、只向本目录写日志，不执行 Claude 的代码、不读取 Claude 的 inbox、不修改 ACL 或门禁。

**后台记录不等于模型自动审查**。本轮会话即时读取事件并独立复验；会话结束后观察器继续记录，不能自行给出审查结论。采样可能错过两个采样点之间启动又结束的短任务，因此 Claude 也已被要求事前发送 start、事后发送结果。

复验不得仅凭进程存在推断 Claude 正在计算或卡死。开始新的监督回合时先查看心跳、事件及 Codex 自己的 Bridge inbox。

## 控制

- 启动：项目 venv 的 python.exe -B 本目录 watch_claude.py（后台用 Start-Process -WindowStyle Hidden）。实例文件锁避免重复运行。
- 停止：在本目录创建名为 `STOP` 的文件，观察器在下一轮退出，并写 `stopped.json`。这是停止观察器，不结束 Claude 会话。
- 重新启动前只移除本目录的 STOP 控制文件；不删除项目源文件。
- 运行记录：`watcher.json`、`latest.json`、`events.jsonl`、`watcher.stdout.log`、`watcher.stderr.log`。

## 本轮已经触发的监管

1. v3.8 文件验收（SHA 8d8902d92ca8b700cd14182190709314834aeff05b457dea4ced5034ab488a71）：24/24 内置回归、24/24 拒读原始泄漏矩阵、64/64 写入故障组合全部满足预期。证据写入尾项关闭。只有静态/内存模拟通过，**尚无原生文件验收结论**。
2. 已通过 msg_370 放行限定一次具名文件原生验收：复用已有 profile/已核验 net-runtime，仅 runtime read 和本脚本新具名 work rw；四对照、原始 JSON/rc 与前后清单，CLOSED 门禁不变。TeX 复制/新渲染/生产放行未包含在此步骤中；Claude 应先发 start，出现未知/FAIL/源码变更即关闭。
3. 已发现 B5 新标注/校准提交：11 对重复、37 对不重复、2 对不确定。但校准把 pair 两端作为 query 放入含自身的 pool，96/96 query 自身相似度为 1，权衡表受到污染。独立 pairwise 对照证据保存在 `b5-calibration-independent-findings.json`，已发 msg_371 要求按 48 个已标注对重算，保留用户标签、排除不确定对。

当前监听心跳：2026-10-04T17:54:36.994511+08:00；最近 HEAD `7635586159d9c2393dad35c25e063db6fe447e96`；子作业 `[]`；核心基线偏离 `[]`。

## 复验材料

`snapshot/`、`reproduce_file_v38.py`、`file-v38-independent-results.json`、`read-leak-type-sweep.json`、`writer-fault-matrix.json`、`b5-calibration-independent-findings.json`。

## 2026-10-04 20:43 恢复及最新检查

旧监听最后心跳18:14:31，进程已退出且原因未知；20:43恢复，实际观察器PID13204。原始日志保留，空窗已写 events.jsonl。新监听同时观察B5校准脚本/报告/PDF。此前本文17:54状态为历史检查点。最新独立审查见 `../2026-10-04-native-b5-review/SUPERVISION_REPORT.md`：B5污染已修复，runpy入口参数缺陷待修，文件原生仍UNVERIFIED、门禁CLOSED。

## 21:08 协助修复完成

runpy入口和B5分数报告已修正，15项相关测试通过；file_acceptance的核心名单补齐11项。独立原生run487341961b6c的4项local文件ACL对照通过、rc0、70项证据核验通过，生产CLOSED。最新说明 `../2026-10-04-assisted-fix/FIX_REPORT.md`。历史UNVERIFIED证据保持原字节。

## B5 v3协助完成

新规则测试已适配，26项相关测试通过；主规则固定签名相等，缺失记录/字段和陈旧题文关闭，标量方程类型与公式绝对值已修正。7页143公式已视觉核对，48对当前计数17/0/0/31不变，仅同样本一致性结论，门禁CLOSED。最新 `../2026-10-04-b5-v3-assist/FIX_REPORT.md`。


## 本轮组合屏复验交接

已完成预检证据、候选遮挡、报告指标与夹具修复，113 项测试和 22 个子测试通过；7 页报告、143 条公式复验完成。实际入口还有 5 道题/15 条候选，组合屏 UNCALIBRATED，11 核心基线无漂移，执行门禁 CLOSED。详见 ../2026-10-04-preflight-binding-fix/FIX_REPORT.md。


## 2026-10-06 全安全点测试监管

收到 Claude msg_576 开工记录后，将 `reviews/2026-10-06-exec-isolation-full-surface/` 纳入动态只读监听；新文件和移除均记录，拒跟随 junction/symlink。旧 worker 45744 用 STOP 正常退出，隐藏重启后的实际 worker 为 14724。AST 及 6 项独立目录发现验证通过。首次已捕获新枚举和 UDP/DNS 探针，完整审查与字节绑定见 `../2026-10-06-exec-surface-supervision/SUPERVISION_REPORT.md`。枚举口径和探针证据存在问题，未给出全安全点通过结论，production CLOSED；后台观察器继续记录，不执行模型审查或准入。


## 2026-10-06 严格修复及资产监管

用户要求发现错误由Codex直接修复。本轮已修六支探针、只读记账、授权根重解析点顺序和面积候选/非旁路渲染入口；57项回归通过，三次有限原生作业保持UNVERIFIED，不接受全绿。监听扩展到两个具名目录：exec-isolation-full-surface、asset-acceptance；隐藏重启后实际worker PID28164，新日志采用唯一名称，不覆盖旧日志。最新结论见 `../2026-10-06-exec-surface-supervision/FIX_REPORT.md`。旧底层绑定因private_profile变更而失效，生产CLOSED、未准入；后台只记录，不自动AI验收。


## 2026-10-06 本机43点修复及资源待补

用户安排“暂无资源，先完成本机部分”。本机注册矩阵重算30 GREEN、0 FAIL、2 PARTIAL、11 GAP；46项相关回归与8主原生作业复验，匿名管道另有补测，6个接收器自测仅验证脚本。生产CLOSED，全43点未通过。监听新增all43-sandbox-repair目录和具名核心工具；旧worker28164用STOP正常退出，新隐藏worker15492已确认心跳，重解析点拒跟随。详见 [本机修复报告](../2026-10-06-all43-sandbox-repair/FIX_REPORT.md)。后台只记录，不能自动进行AI审查或准入。


## 2026-10-06 证人邮件及接收器修复

新邮件600/601报告校园LAN证人就位，尚无正式双端验收。Codex修复witness接收器的截断、异常成功、覆写与身份绑定问题；10项针对性测试通过，新EXE四条宿主回环自测通过，仅为工具验证。当前43点仍30 GREEN/2 PARTIAL/11 GAP，生产CLOSED。监听新增witness-mail-review目录及两个源码文件，STOP正常结束旧worker15492，新隐藏worker35160有心跳。详情见 [邮件审阅](../2026-10-06-witness-mail-review/MAIL_REVIEW.md)。后台只记录，不自动AI验收。

## 2026-10-06 IPv4联合认定

用户授权LAN IPv4受控证人 + 真实外部IPv6 + 本机IPv4联合认定，不再独立要求公网IPv4节点；TCP/UDP逐项重算。82项回归通过，新原生主回执独立重算30 GREEN、0 FAIL、2 PARTIAL、11 GAP，生产CLOSED。监听新增ipv4-joint-policy目录、联合测试和生产采集入口；35160正常STOP，新隐藏worker44260有心跳。详情见 [新策略及修复](../2026-10-06-ipv4-joint-policy/FIX_REPORT.md)。后台仍只记录，不自动AI验收。

## 2026-10-07 外部采集入口与 holdout 草案

外部/LAN采集入口已由Codex修复，26项新增回归及合计64项相关回归通过，仅为模拟/本地I/O证据。旧RoundA缺完整双端日志，不能用于准入。用户安排双端沙箱检测实验在2026-10-08，当前未启动该实验。只读监听已扩展到采集器、测试、外部实验及holdout修订目录；44260正常STOP，新隐藏worker37180有心跳，后台仍只记录。

holdout仅修当前391条候选，不加题、不生成数值变体。v3纠正资格声明、容量矛盾、成员/核心隔离和统计界；9项精确公式测试通过，实际资格/盲标/校准/最终验证仍PENDING / UNCALIBRATED。生产CLOSED。

[草案修订报告](../2026-10-07-holdout-v2-review/REVIEW_REPORT.md) · [当前设计v3](../2026-10-07-holdout-v2-review/holdout-design-v3.pending.md) · [采集入口修复](../2026-10-07-external-driver-supervision/FIX_REPORT.md)


## 2026-10-07 核心提交监管恢复

旧 worker37180 最后心跳05:08:27，当前已退出，原因UNKNOWN；历史日志保留。已隐藏恢复，launcher29596、实际worker31260；观察范围加入core-submission-v1、核心检查器、测试及冻结政策/清单。恢复时心跳见 ../2026-10-07-core-submission-supervision/observer-recovery.json。观察器只记录，不能自动执行数学审查或准入。

当前 A/B 原SHA复验匹配；C 的统计和审核范围有错，检查器由Codex修复、27回归通过；交30题精确正文候选，31具名精确检查通过，现役与冻结包未替换。数学/同核心隔离仍待实际全范围复核，生产CLOSED；详见 ../2026-10-07-core-submission-supervision/FIX_REPORT.md。


## 2026-10-07 后续核验与接入层监管

原 verify_codex_supervision 统计/身份/退出码错误已修，39回归通过；接入与格式相关51回归通过，共90具名检查。30题正文保持上一轮精确修订，17场景修正后生成独立 admission-v2，5源文件489记录原身份保留，现役与v1原件未覆盖；全核心数学/同核心隔离和新渲染仍未完成，生产CLOSED。

监听扩展到后续4核验/构建工具、相关测试、v1及Codex新版本材料；31260与41804均正常STOP，当前worker见 ../2026-10-07-core-verifier-followup/observer-restart.json。后台只记录，不自动AI审查或放行。详情 ../2026-10-07-core-verifier-followup/FIX_REPORT.md。


## 2026-10-07 数学批审链修复与独立复核

批审工具最终契约 v3：冻结源/记录版本核验、非空唯一题号、具名理由、源码快照、六项产物回执与禁止覆盖旧目录。独立复核本轮38题，10条补严谨条件/精确场景，保留上一轮30条修订。其他已收草稿批次仅重新绑定，不等同独立数学通过。监听纳入 math_review_batch.py、测试、规格、批次目录及本轮 Codex 材料；旧20432正常STOP，新 worker见 ../2026-10-07-math-batch-supervision/observer-restart.json。后台只记录，不自动数学审查或准入；production CLOSED。


## 2026-10-08 深层数学与真实公式复核

4个训练ID另版修订，61项工具回归、46项精确检查和6项一般性证明通过。原162空MathTex回执不合格，7条实际公式样例通过，156条交Claude Code重渲；全局隔离与视觉仍未验收，生产CLOSED。监听新增数学源码／回执，略过媒体缓存；40700正常STOP，新worker 24760，后台只记录，不自动AI审查。详见 [本轮报告](../2026-10-07-deep-isolation-followup/FIX_REPORT.md)。


## 2026-10-08 当前公式重渲复验

已完成163条当前目标，另2条补验；165条完整公式资格限定本地MathTex编译，2663公式/5212原文出现。修复双美元解析与中文XeLaTeX/ctex，19项相关回归和9项复验器对抗检查通过，数学正文保持。全局隔离/视觉/原生沙箱未标绿，production CLOSED。

只读监听新增 native-real-render 与 real-formula-followup 两个目录，略过媒体缓存。旧worker24760正常STOP，新隐藏worker52952有心跳，后台只记录，不自动AI审查或放行。双端实验不由Codex执行或验收。[当前修复报告](../2026-10-08-real-formula-followup/FIX_REPORT.md)。


## 2026-10-08 ????????

????? 11:13:03?? worker ?????????????????? worker PID 44524????? Claude ?????????????????????????LAN ? remote-271e1c881c4f473fb027f5f28d4a3bd5 ???????????????? JSONL?summary ??? rc???? UNVERIFIED??? CLOSED?Codex ???????????66 ????????? [????](../2026-10-08-dual-endpoint-supervision/SUPERVISION_REPORT.md)???????????AI???
