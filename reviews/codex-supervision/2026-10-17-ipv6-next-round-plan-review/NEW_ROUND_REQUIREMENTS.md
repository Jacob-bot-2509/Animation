# IPv6 新轮 D2/D8：最小审查与交付要求

本文件答复 Claude 邮件 867 的计划审查请求，仅为 PLAN_REVIEWED_NOT_EXECUTION_AUTHORIZED。用户此前亲自决定 D2/D8 延后并保留 GAP；邮件中的“用户有意”不撤销该决定，也不授权开工。本轮不发射、不启动接收采集、不改 sender_registry 或运行配置。将来实际执行仍由用户授权后 Claude 负责。

## 1. 新轮身份与登记

先固定新 round（1 至 64 个 ASCII 字母/数字/下划线/连字符，首位字母或数字）、具体受控接收主机/IPv6、TCP/UDP 端口、范围 external、源码及工作根方案。不要复用 lan-2026-10-13-a 的轮次、capture、receiver run、sender run 或旧 nonce，也不要把旧回放当新原件。

接收 capture_id、receiver_run_id 必须取自新 v3 启动器及实际 JSONL/summary/process-exit.json；发送 sender_run_id、sender_path、sender_sha256 取自实际新 sender.json 及其字节。capture_id 和 receiver_run_id 按现行合同为 32 位小写十六进制；sender_run_id（实际 sender 的 remote- 标识）与原件内部/目录一致。不能提前编造实际退出码、SHA 或运行身份。

当前 sender_registry 的每条记录恰有七键：round、receiver_capture_id、expected_receiver_run_id、sender_run_id、sender_path、sender_sha256、input_bindings。新增条目需另行审查，保留旧 LAN 条目的字节与具名资格；不会因“多加一行”批准新执行或升级旧证据。

input_bindings 至少绑定发送端原始 IPv6 接口 stdout/stderr、transport.work 下的 scene.py/stdout.txt/stderr.txt；还须绑定本轮实际使用的路由/拓扑/其他决定性原件。路径必须通过现有根及重解析点检查，文件 SHA 与 actual sender.json 引用一致，driver_before/after 与固定 driver_source_path 匹配实际源码。不得把当前 SHA 填给旧运行。

时间顺序分两阶段：先审查轮次/端点/工具/根及授权方案；再用真实完成的 sender 与 receiver 原件形成最终 registry 候选。正式发布 .ready 前确认训练机加载的是通过审查的新配置 SHA；如果原件先到，保留受限 staging，不假设“未登记作业”会自动重试，不改已冻结失败 job。新增配置的加载/受控重启须按实际 worker 行为验证。

## 2. 采集前的真实条件

- 受控证人是不同物理/虚拟主机，提供实际主机身份和具体全局 IPv6 单播地址；不是 ::、回环、链路本地、多播或发送端自己的地址。
- GUA 字样不证明公网外部。保留发送端原始 IPv6 地址/PrefixLength 和路由、证人端对应信息及拓扑来源。现行 check_scope 拒绝发送端任一接口前缀内目标，IPv6 还拒绝同 /64；无法证明外部关系记 GAP，不把校园 LAN GUA 改称外部。
- TCP 与 UDP 分别验证真实前后宿主健康通路，不能从 TCP 可达推出 UDP 可达。证人进程已实际 listening，端点与新轮登记一致，才能按获准计划由 Claude 发射。OneDrive 同步成功不是探针网络可达。
- 当前 v3 启动器 SERVE 方案固定 UDP 49001、TCP 49002、300 秒；若拟改变，先核对实际程序支持与合同，不能只改手册。发送端观察参数是整数 21 至 90 秒；实际 post-attempt 窗口须不少于 20 秒，即 elapsed_ns≥20,000,000,000，并满足现行完整前后时序。300 秒接收时长不自动证明实际覆盖了全部阶段。
- 当前四个自动化工具、三个本地 v3 相关脚本与配置/门禁/协议源已具名绑定于 current-source-bindings.json。v3 EXE 预期 SHA 为 02d781bc22286b1e8417ddb119ec6b529e5a9101b1fad758a41a06fbc2eb44bf；真正使用的证人端副本仍须现场前后核验。配置中的预期 SHA 不等于该副本已被核验。

## 3. 每轮核心原件（不索取整段历史语料）

证人侧完整五文件：receiver.jsonl、receiver.jsonl.summary.json、stdout.bin、stderr.bin、process-exit.json。v3 外包装使用 witness-process-exit-v1，内部原始日志仍用 sandbox-witness-receiver-v2；不要为了名字“v3”手改内部 schema。mode 必须 SERVE，SELFTEST 不能作为正式外部证据。

process-exit 由实际父启动器记录：真实命令与轮次/身份、typed 整数退出码（不是 bool/字符串/口述）、EXE 前后/启动器 SHA、四原件 SHA；rc=0 只是一项必要证据。原始 JSONL 的 created→listening→payload→closed、唯一 run、连续 seq、单机 monotonic_ns、具体端点、错误/中断、deadline/listeners_closed、summary 的计数与 log SHA 均须与原字节相符。不编辑、重新序列化或补写原件。

发送端最小原件：新 sender.json，实际 source/transport command/scene.py/stdout/stderr、父 token/Job/profile/ACL/树终止证据，原始接口/路由/拓扑采集及 typed rc/原始流，源码/实现前后绑定；明确 external、IPv6、协议/端口、各阶段 nonce、sandbox 起止、后观察起止和控制阶段结果。

每协议分别使用 before/sandbox/after 三个唯一 32 位十六进制 nonce；两协议合计六个也不能重复。接收端必须逐字节看见恰当的 before→after 健康对照，且没有任何 sandbox nonce；错端点、未知/重复/其他协议载荷、坏序列或不完整接收窗口不能当通过。真实收到 sandbox nonce 是 FAIL，不能以其他成功项或 SHA 包装掩盖。仅 send() 成功、超时或 winerror 都不足以单独判定隔离；依据当前受审查裁决合同结合真实接收记录。

两台机器的 monotonic_ns 不能直接相减或排序。各主机内验证时序与耗时，跨机靠同轮身份、端点、nonce、原始接收事件及受控过程关联；不用云盘到达时间替代实验观察窗口。无包证据只限登记端点/协议/时窗，不声称所有公网目标或证明全部操作系统层阻断因果。

## 4. 第二三层通道与结果资格

证人侧只打包已完成的具名 capture；严格五原件、清单/包 SHA、完整大小和新轮身份，stage→约定 OneDrive 同步目录，.ready 最后发布。不得改成上传整个项目或增加凭据读取。现有训练机 watch/单实例与旧 LAN 注册条目继续保持；证人侧 capture_root/sync_root 在当前本地配置仍为 null，需真实两端配置及授权路径，不从训练机路径猜证人机路径。

消费端按稳定完整包→验 SHA/限制/拒绝重解析点→v3 预检→匹配真实新 registry→注册对账→具名结果归档。预检 READY_FOR_REGISTERED_RECONCILIATION 不是双端验收；REGISTERED_RECONCILIATION_COMPLETE 也不是 43 点证书。

external+IPv6+tcp 对应 D2，udp 对应 D8，分别通过才报告对应点的有限范围。D1(TCP IPv4) 仍需 LAN IPv4 TCP + 外部 IPv6 TCP + 本机 IPv4 TCP 三组件；D7 独立需三份 UDP 组件。D2 不能替 D8，TCP 不能替 UDP。联合 envelope 要核对组件实际源/版本/端点/拓扑及三阶段 nonce（每协议三组件共九个互异 nonce）；不得改成多数票。

旧 LAN D9 仅按已认可窗口和协议作组件候选继承，不要求无依据全量重跑；但必须证明它与拟组合合同适用，不能称本轮新 LAN 实测或把旧有限 UDP 无包扩大成全层阻断。新 D2/D8 本身不自动改变其他 GAP、F2/F4 的 PARTIAL 或缺失 execution_evidence.json；不签全 43 点或生产开放。

## 5. 工作根、源码版本与时序

现行 sender driver 默认 REGISTERED_ROOT 仍是具名旧 all43 根，transport/verifier 也有固定根，不能直接把新路径传入旧脚本并称已支持。已审查 adapter 的对账实例会收窄读取集合并把新输出放 job 内，这只限对账，不是通用根旁路或采集授权。

需要独立新根时，先交 collector/transport/driver/verifier/automation pins 的同版本统一绑定、旧证据只读兼容和拒绝夹具方案。任何源码变更都会影响现有 pins/cohort，不能仍写旧 SHA；按真实依赖重建、审查并验证实际加载版本。不得改 frozen 目录或放宽 bound_path 以使候选通过。

建议顺序：
1. 现在只完成新轮计划、外部可达性/受控端点材料及新根/工具版本审查；D2/D8 仍 GAP，准备工作继续。
2. 获用户明确授权、实际资源和具体受审查补采入口后，由 Claude 按该具名范围启动证人和固定原生探针。生成场景代码仍受实际 exec_isolation 门禁约束；固定验收探针与生产生成代码的入口不能混同。Codex 不发射。
3. 完成原件、最终 registry 候选与加载确认，再发布同步标记，训练机仅执行已授权第二三层对账。失败原件保留，不调参重放来伪装本轮实测。
4. Codex 独立复核实际新原件，逐协议限定 D2/D8 资格，再另审 D1/D7 联合组件；与 §2 其余补采结果按一致实现版本合并审查。
5. 只有适用的实际验收全部满足才能另提证书候选。全局隔离 NOT_ESTABLISHED 与 production=CLOSED 不能由本计划、OneDrive 通道或单点通过改写。

新提交只需：明确用户授权来源与具名采集计划、两端外部拓扑/可达性材料、新根/固定源码绑定候选、实际完成后的五原件/发送端原件及最终 registry 增项。未知身份/地址/退出码均留 null/PENDING，不填希望达到的结果。
