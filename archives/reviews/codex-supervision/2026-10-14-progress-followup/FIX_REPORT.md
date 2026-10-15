# Claude Code 最新进程复核与修复

本轮复核的最后提交为 92828490057278c850e82235896acbae1911bf56（2026-10-14 00:26:21，UTC+8）。Claude 当前工作为整理归档和维护发布说明；没有据本轮材料取得正式开训许可。新邮件为 msg_1791908423189_799，定时批次 run-a338831f11574f0fb2a56b1a9d682188；补充协调材料为 msg_1791908860838_800。

**本地修复结论：REPAIRED_PASS，限定当前文档、三支归档工具入口、具名固定路径兼容与既有材料字节绑定。** 邮件799要求更改自动调度入口的部分为 OUT_OF_SCOPE：本批指令第3条明确排除自动调度源码，邮件不能扩大授权。本轮保留原定时入口，没有改计划任务、自动调度逻辑或重装调度器。不能把本地修复理解为完整路径迁移或生产放行。

## 已修复

Codex 已修改 NEWRELEASE.md、进度看板.md、环节入口.md 和 AGENTS.md：

- 删除“旧轮网络故障均已定位并排除”的无证据结论；保留旧轮失败资格。LAN仅限定 D9 登记窗口双协议，UDP缺送达的因果仍 NOT_ESTABLISHED。
- 说明 hp_sweep 的 center-confirmed 与其余 PROPOSED 候选、train_loop.example 模板的区别；历史计划不能替代本轮直接开训授权。
- 将设计阶段的“未实现”更新为本地工具已交付、实际 OneDrive 同步与后台部署未验证，active=false。
- 保留 Claude 的 archives 链接；更新后续928提交已收录六文件的事实。五份Python Git对象SHA与冻结交付一致；配置的Git换行规范化导致原始SHA不同，JSON对象相同，现役字节仍与冻结归档一致。完整两个哈希见 commit-928-automation-source-check.json。
- 修正 AGENTS 中错误的当前运行位置：观察器和自动邮箱实际仍在旧活动根，不能把归档副本作为最新心跳。

Codex 已修改 tools/render_packs_v2.py、render_packs_v2_html.py、holdout_earliest_index.py，新增 tests/test_archival_tool_entrypoints.py：

- 默认仅 PLAN/rc3；实际执行必须 --execute 并提供 --out 新目录。拒写系统/项目外、既有目录和任何冻结祖先，排除重解析路径；生成文件采用排他新建，名称碰撞拒绝覆盖。
- HTML报告与页面写在同一新输出；空输入不记成功。分数题干、过程、答案保持原文；不把输入层生成作为浏览器视觉或原生渲染通过。
- 历史索引只纳入 Codex 自己的收件/已发送元数据，按真实UTC时刻限定2026-09-29至2026-10-05；未知时区拒绝，扫描配额用尽拒绝而非静默截断。没有实际执行全历史扫描或扩充语料。

## 归档搬迁与兼容

搬迁期间，当前数学绑定、v3 EXE、原生工作输入、surface_probe_contract、观察器源码和本轮正在进行的归档曾从既有路径消失。第一次28项复跑全部因具名输入缺失出错；补回原生工作后仍有5失败/1错误，进一步定位到当前 BOUND_FILES 的原生契约被搬走。原始失败日志全部保留，未削弱校验或测试。

现保留 archives 正式资料位置，并为旧绝对路径和运行根保留相同字节兼容材料。完整清单 ACTIVE_PATHS.json；原→新映射、普通文件SHA及原有测试重解析点的处理见 canonical-archive-with-active-compatibility.json。三处测试重解析节点没有复制到新副本，也没有访问其目标；原位置的节点未由Codex修改。

不能清空旧 reviews：原生接收/发送记录和旧JSON中的固定绝对路径仍需读取；当前观察器、邮箱任务、ACK报告校验和作业journal仍在旧根。以后路径升级须单独按源码、回执与版本绑定受控验证，不能修改冻结JSON来伪造新路径证明。

Git状态检查曾 rc128，原因是搬迁中的历史Git fixture出现空.git目录；作者继续搬迁后该故障消失，最后原生Git状态检查rc0。Codex没有删除.git目录，也没有把先前失败的空stdout解读为干净工作区。

## 独立验证

- 自动化28项最终复跑全部通过（path-recovery-tests-complete.json）。
- 新增入口保护14项全部通过（archival-entrypoint-tests-complete.json），覆盖默认无执行、冻结/既有/项目外拒写、精确分数、源SHA失败、重名、空HTML、自己的邮件过滤、UTC边界、限额。
- 新入口首轮因Codex调用共享路径接口名不匹配而出错；已改为现有checked接口，最终14项通过。原始失败、12项中间通过和14项最终结果均保留。两次原地保存返回OSError22，源码经复读未截断；随后采用同目录临时文件、并发字节核对和原子替换，不改ACL，具体环境原因保持UNKNOWN。
- 四份具名冻结归档共1385件的完整文件集合、长度和SHA匹配；当前六份自动化工作区字节匹配冻结交付。
- 当前24份数学源及761条原版本绑定的证明路径核验通过；权威状态字节未改变。没有重算未变整库题目或重复进行整库视觉验收。
- 原LAN冻结作业14件、15条输入/代码绑定验证通过；原nonce/窗口/退出码等不改。
- 三份当前状态文档及AGENTS的31条链接有效；交付源码解析、默认CLI和限定diff格式检查通过。源码最终完整哈希与快照见 DELIVERY_SOURCE_BINDINGS.json。
- 原观察器源码保持原SHA，当前PID与心跳见最终状态记录；进程存在不能证明Claude在计算或任务完成。

## 邮件800陈述的审查

Git实测22269个R100、36个R099、771个A和40个M，计数与作者搬迁陈述对应。然而36个R099均为JSONL/历史blob的相似度配对，并非观察器日志；“均因观察器并发改写”没有得到证据支持。Git改名启发式不能替代原→新逻辑路径和哈希核验。本轮用具名核心材料和逐文件兼容副本验证，未为全部历史语料签字；不要求扩张历史语料来换取当前核心合格。

## 资格与后续

LAN继续 PASS_BOUND_LAN_D9_TCP_UDP_REGISTERED_WINDOW_ONLY；D1/D7依赖缺口保持，D2/D8延期GAP不阻塞训练准备。全局隔离 NOT_ESTABLISHED、原生 UNVERIFIED、production=CLOSED；未签PASS_CORE_SCOPE，未启动探针、采集、训练、真实同步或后台消费worker。

Claude应按Codex修订继续已授权准备与接入材料提交，不重复改已完成文件；先提供证人capture_root/sync_root、训练机sync_root、共享权限与Python环境，再进行OneDrive通道验证。保留 ACTIVE_PATHS.json 具名依赖，不能自行再搬走固定入口或改冻结原件。当前修复未由Codex提交或推送。

本轮完整归档同时保留在 archives/reviews/codex-supervision/2026-10-14-progress-followup/；旧 reviews 下的同内容副本仅供当前ACK校验兼容，冻结后均不追加。
