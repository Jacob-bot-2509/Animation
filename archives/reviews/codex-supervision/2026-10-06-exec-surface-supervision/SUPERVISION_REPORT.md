# Claude 工作进程监管与独立复验

检查日期：2026-10-06。结论：已捕获 exec_isolation 全安全点测试开工；清单和首个探索探针存在证据口径缺陷，尚不能验收。生产门禁仍为 CLOSED，候选未选中、未准入，没有启动训练。

## 当前实际进度

- msg_1791280302745_575 确认：全量独立数学/语义、视觉与来源绑定、密度及独立校准、沙箱全安全点均尚未完成。
- msg_1791280706685_576 是本次开工记录。提交 `4c54f2e5004fe68e71b4b706ccfa960670f6711d` 增加安全点枚举，后续新增 `probe_udp_external.py` 及 `probe-udp-external-v1-results.json`。开始通知、具体文件和结果共同支持本次工作进度；进程存在本身不作为进度证明。
- 已发 msg_577 询问当前任务，msg_578 纠正枚举口径，msg_579 返回新探针源代码问题。

## 枚举口径问题

清单表格实际为 43 点：28 个 GREEN、14 个 GAP、1 个 PARTIAL。尚未绿色的点合计 15，F6 不能以“价值低”为由排除。旧联合验收只涵盖明确列出的 16 个检查，不能扩张为 43 个点或全表面证明。

A8、A9、B5、E1、E2、E3 的依据分别为代码、单元测试或声明；它们与原生证据必须分列。其余点也需逐点绑定实际测试用例与当前源码，不能由一份 PASS 汇总推断覆盖。当前枚举未获本轮穷尽性认证。

## 首个 UDP/DNS 探针审查

| 点 | 原始观测 | 本轮结论 |
|---|---|---|
| D7 外部 UDP IPv4 | sendto 返回 sent | UNKNOWN：没有外部接收端及健康前后对照 |
| D8 外部 UDP IPv6 | sendto 返回 sent | UNKNOWN：没有对应 IPv6 外部送达证据 |
| D9 局域网 | 向本机接口 28.0.0.1 发送；接收记录仅见两个宿主对照 | UNKNOWN：并非另一台经确认的 LAN 主机，观测窗及线程结束证据不全 |
| D10 原生 DNS | gaierror，errno=11001 | UNKNOWN：没有明确权限拒绝或 DNS 无出网证明；缓存与固定域名未分离 |

`SENT` 不能证明对方收到，也不能证明已封堵；此原则已写在项目 `SANDBOX-DEPS.md`。接收端未见沙箱 nonce 的记录，仅支持当前有限观测，不能推广到所有外部或 LAN 端点。

已用无网络的独立反例重现：

1. `before in payload` 会把 `probe-lan-<before>` 误认为宿主 before 对照。应对不同阶段的完整 nonce 精确比较；本次实际原始记录仍保留，不因反例改写观测。
2. 任意 OSError 都被标作 denied，包括无 winerror 的非权限错误。只有明确的权限拒绝可以标作 OS_DENIED，其余失败应按原因保留为 ERROR/UNKNOWN。

探针还裁剪了 stdout/stderr，丢失 `run_code` 返回的 `parent_evidence`、`command`、`source_sha256`；没有完整绑定令牌、profile、ACL 恢复、接收器结束和观测窗口。程序返回零不能代替安全验收。本轮保存了实际工作目录内的 scene.py 字节，但这不能补造已丢失的父进程/ACL 原始证据。

要求 Claude 保留 v1 为探索证据，修正后另交新版本及新具名原始证据，不覆盖旧记录，不解禁。Codex 本轮未启动新的原生网络、渲染或训练作业。

## 已交付文件与正式来源复核

以下均与对应历史绑定一致：106 项上一轮交付、111 项正式来源、32 项原生渲染来源、10 项旧联合验收实现绑定及旧联合原始回执。两项活跃源码保持原样；观察器源码仅由本轮明确扩展监听范围。看板与上一轮单行澄清回执一致。

这些是字节、来源与范围复核，不能冒充全量独立数学、视觉或全安全点验收。未重复无变化的旧数学测试及渲染作业。

## 只读监听

观察器由旧 worker 45744 正常 STOP，隐藏重启后的实际 worker 为 14724。新增动态范围仅 `reviews/2026-10-06-exec-isolation-full-surface/`；递归发现新证据文件、记录删除、跳过重解析点，未扩大至整个磁盘。

AST 编译及 6 项独立目录发现检查通过，包括新文件、移除记录、目录边界、junction/symlink 拒跟随。新心跳正常，首次覆盖 233 个路径。三项核心基线偏离是此前已记录的历史偏离；本轮旧联合绑定的源码均未变化。

监听只记录事件；会话结束后不会自行执行模型审查或批准。新交付仍需独立审查。

## 复核材料

- `independent-integrity.json`：每项原始/当前 SHA 与长度。
- `enum_original.md`：首次收到枚举的原始字节。
- `probe-udp-external-v1.source.original.py`、`probe-udp-external-v1-results.original.json`、`executed-probe.scene.original.py`：源码与探索结果原始快照。
- `probe-review.json`、`probe-counterexamples.json`：结论与两项独立反例。
- `watcher_before.py`、`watcher-change.json`、`watcher-verification.json`、`watcher-after.original.json`：监听改动与验证。
- `incoming-mail.*.original.json`：Codex 自己收件箱原始记录。未读取 Claude 收件箱。
