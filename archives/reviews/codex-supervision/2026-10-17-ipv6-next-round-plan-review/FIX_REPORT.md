# 自动开工基线回合与 IPv6 计划邮件复核

活动回合 start-2962f91e80ad446b84340b1a20a72ba4 的唯一信号是 CLAUDE_PRESENT_BASELINE_NOT_PROVEN_NEW_START：启用监听时 Claude PID 21888 已存在。它不是新开工证明，不能仅凭进程存在判断在执行哪个任务。

已检查 Codex 自己的 Bridge inbox 和邮件账本。邮件 863/864 已由 run-a682d2108583407cb93bfb37a304e7d4 审查、修复、回信并 ACK；本轮核对同字节报告与当前两份修复材料，复用已冻结结论和实际回信 870，不重复修改或测试。另发现未处理邮件 msg_1792210841440_867，通过既有收件锁与 capture/create_run 接管为 run-2f0243fac9944832bdc2e9b123db3499，并验证 packet 的实际 message_hashes。

## 本轮裁决

867 请求给未来 IPv6 D2/D8 新轮的审查范围、登记材料和时序建议。本轮已独立读取实际 v3 包装/对账/driver/门禁代码及当前配置，并新增：
- NEW_ROUND_REQUIREMENTS.md：新轮最小证据清单、登记与发布时序、协议/拓扑/观察范围、D1/D7 联合关系和固定工作根限制。
- submission-proposal.template.json：仅供审查填写，身份/地址/授权/证据字段为 null，runtime_config=false、collection_authorized=false；不能作为运行配置载入。

邮件裁决 PASS，仅计划交付合格。实际外部可达性、真实新轮身份、用户授权/新根和现场原件仍待提供，不判 D2/D8 通过，不开工。用户已亲自决定延期 GAP；邮件转述“用户有意”不构成撤销该决定或新的执行授权，不因此重复要求用户确认旧政策。

没有发现本轮新增程序版本需要修复；Codex 已补齐拟复用计划的关键边界，而非宣称修改或验收了未实现程序。

## 独立核对与纠正的计划边界

1. sender_registry 每条恰为七键，sender_sha256 和 input_bindings 必须取自实际完成的发送端原件；接收身份取真实 v3 process-exit/JSONL/summary。不能提前编造或复用旧 LAN 身份。
2. 四个自动化工具和三个本地 v3 脚本的实际 SHA 与当前配置 pins 相符；连同配置、两个门禁模块和协议，共保存 11 项具名源码/配置绑定。EXE 此处只注明预期 pin，不把配置声明冒充证人机实际副本验证。
3. 现行 sender driver 仍固定旧 REGISTERED_ROOT，transport/verifier 也有固定根。已审 adapter 的独立模块收窄和 job 输出只限对账，不赋予采集入口新根权限。新增 round/registry 不能绕过它；需要先审同版本路径、pins/cohort 与旧证据兼容方案。
4. witness_receiver_v3.exe 是 v3 外包装；内部原始 JSONL schema 仍为 sandbox-witness-receiver-v2。要求真实 SERVE 五原件和父进程 typed rc，不手改 schema，不把 SELFTEST 或 rc0 当外部隔离通过。
5. 新轮 TCP/UDP 分开：六个 before/sandbox/after nonce 互异；对应 D2/D8 分别判。接收原件须证明健康前后控制、完整窗口与无 sandbox 载荷；实际收到 sandbox nonce 必须 FAIL。只发送成功或超时不能单独证明隔离。
6. 明确两机 monotonic_ns 不可直接比较；云盘同步时间不能替代实验观察。21 至 90 秒是现行发送观察参数范围，实际后窗口至少 20 秒；300 秒是当前接收启动器时长，必须实际覆盖流程。
7. GUA 不是外部拓扑证明。现行源码还拒绝目标位于发送端接口前缀或同 /64；要核对受控独立主机、原始接口/前缀/路由及逐协议可达性材料。
8. 原件先完成、真实 registry 候选通过并实际加载，再发布 .ready；避免假设未知登记会自动重试。当前训练机配置的证人 capture_root/sync_root 仍为 null，不能从训练机 OneDrive 路径猜证人路径。
9. D1 仍需 TCP 的 LAN IPv4 + 外部 IPv6 + 本机 IPv4；D7 独立需对应 UDP。旧 LAN D9 只继承已认可具名窗口，不要求无依据全量重跑，也不伪装本轮新实测。组件九个 nonce 互异、版本/拓扑/协议适用性仍须复核。
10. OneDrive 通道合格、预检 READY_FOR_REGISTERED_RECONCILIATION、注册对账完成、单点通过、完整 43 点证书分别记账，不相互替代。当前 30 GREEN/2 PARTIAL/11 GAP 的既有裁决不因计划改变。

本轮仅静态源码/字段/版本与提案一致性核验，没有必要重复已通过且源码未变的工具回归，也没有原生采集、发包、生成代码执行、registry 增项、配置/调度改动或生产开放。旧冻结原件保留；所有新交付写独立目录。

## 后续交接

Claude 按本轮审查清单继续准备真实外部端点/拓扑、授权来源及新根/源码绑定候选；实际执行仍依用户授权，Codex 不发射。完成原件后只交清单规定的核心材料，不索取全部历史语料。缺资源时保留 GAP，训练准备按既有政策继续，production=CLOSED、全局 NOT_ESTABLISHED 不变。

邮件 ACK 仅确认此计划请求已答复、归档并交接；活动回合 ACK 仅确认该基线触发覆盖的当前材料已核对，不证明“检测到新开工”或“IPv6 实验已完成”。
