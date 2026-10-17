# IPv6 双端实验 D2/D8：工具与分阶段操作单 v2

状态：PLAN_PREPARED_NOT_EXECUTION_AUTHORIZED。本单是待实施方案，不是已可直接运行的发布包。Codex 已修正文书中的部署依赖、同步权限和身份/发布时序；本轮不启动接收采集或探针、不改变配置/登记/门禁。用户此前 D2/D8 延期 GAP 的决定继续有效；已明确覆盖具体范围的真实授权可引用，不重复索取，邮件转述不能替代新授权。

## 一、两端工具和路径

### 1. 证人端接收器：最小两文件

在操作者控制、非 OneDrive 的独立目录中，同目录放 witness_receiver_v3.exe 与 start_witness_capture.ps1。EXE 预期 SHA256 为 02d781bc22286b1e8417ddb119ec6b529e5a9101b1fad758a41a06fbc2eb44bf；启动器预期 SHA256 为 39032c5e3b14d699715047cf9f6acbd2bef1c9265916d574ae9f90ca0f3e3545。这只是当前受审版本，现场副本仍要在运行前后核验。

该最小接收器不要求 Python；不能因此声称 Python 自动打包工具也已部署。接收器 mode=SERVE，当前启动器固定 UDP 49001、TCP 49002、300 秒；SELFTEST 仅本机自检，不当正式外部证据。

### 2. 证人端自动打包：另需完整闭包

witness_pack.py 直接 import witness_transfer_common。公共模块在导入时计算四个 automation_source_pins，load_config 执行模式还核验三个 v3 相关脚本；只带原稿所列几份文件不能满足该检查。

若使用现行代码，候选部署布局为 <部署根>/tools/ 下至少存在以下七份同版本原字节：
- witness_transfer_common.py、witness_pack.py、witness_consumer.py、witness_registered_adapter.py；
- start_witness_capture.ps1、inspect_witness_evidence.py、sandbox_external_test_driver.py。

后两类文件即使在证人端不执行，也属于当前 pin 核验闭包。ROOT 按 __file__.parents[1] 推导，因此不能把 tools 文件平铺到任意目录后仍套用旧根配置。可将 EXE 与 tools/start_witness_capture.ps1 同目录；或者保留独立两文件接收目录，capture_root 指向实际原件位置。inspect 和发送 driver 的正式调用仍在训练机受审环境，不在证人端为验证依赖而执行。

证人端还须有实际核验可用的 Windows Python/标准库环境、witness 角色独立配置以及实际 capture_root、staging_root、sync_root。现行 load_config 要求 staging 位于该部署根的 reviews/witness-automation/ 内，三根不得相互包含。七份源码的字节清单见 WITNESS-KIT.plan.json；该清单不是运行配置，未部署、未激活、未声明证人端 Python 已验证。

训练机现行配置的 witness.capture_root/sync_root 为 null，不能照抄其 active=true 配置作为证人端就绪证明；证人角色要经独立路径/权限/版本核验后接入。

### 3. 训练机与同步通道

训练机沿用已审四工具及完整本地依赖、具体新根/driver/verifier 合同和实际配置/加载版本。常驻 consumer 只说明在等待包，不证明新 receiver 可达。

OneDrive 使用用户已授权的同步/共享通道；不要求在不同机器登录某个硬编码个人账号。是否同一账号或经授权共享，由实际接入方式决定，不要求交出密码/令牌。两端各自的绝对 sync_root、可见性和权限必须用真实材料核验；不要假定证人端也叫 OneDrive\witness，或用训练机路径替代证人路径。只有指定证据包进入此通道，不上传整个项目。

## 二、采集前的四类检查

1. **授权和范围**：独立受控证人主机身份、具体 IPv6/协议/端口、新 round、固定探针、执行者、原始产物范围及已有真实授权来源。Codex 不启动接收器、不发射；证人端实际操作者与获授权 Claude 负责采集/发送。
2. **外部拓扑与端点**：两端实际 IPv6 地址、PrefixLength、路由和控制来源。GUA 本身不证明外部；非 ::、回环、链路本地、多播或发送端自己。现行 check_scope 还拒绝发送端任一接口网段及 IPv6 同 /64。TCP/UDP 的真实健康通路要在获准采集中分别实测，不能用 TCP 代 UDP 或旧 LAN 成功代公网可达。
3. **新根与工具版本**：当前 driver/transport/verifier 固定旧根；仅设计层的 REPAIRED_PASS 不代表真实新根已接线。统一根/源码/pins/cohort 与拒绝夹具方案实施并独立复核前，不直接向旧脚本传新路径或放宽 bound_path。
4. **部署与轮次计划**：角色工具/运行环境/配置路径真实可用，新的 round 及身份生成规则经审查；round 为 1 至 64 个允许的 ASCII 字符。此时 capture_id/receiver_run_id 和 sender SHA 等实际运行字段可仍为 null/PENDING，不能要求尚未运行的材料先有“真实 SHA”。它们在真实产生后进入最终 registry 审查，而不是作为自报执行许可。

本轮没有替用户验证公网可达、启动这些检查命令或更改系统策略、防火墙、ACL、账号设置。只读本机接口/路由材料可以由受控操作者按具名范围准备；不要为了准备材料先发射未获准的外部探针。

## 三、真实采集顺序（未来获准后）

1. 证人端现场核验 EXE/启动器，按批准端点、新 round 和 SERVE 计划启动，取得实际 capture_id、receiver_run_id 与 listening 端点。与旧 lan-2026-10-13-a 的所有实际身份区分，不补造、不重命名旧回放。
2. 训练机在已审入口按 external IPv6、both 协议的单个 sender 运行。现行 driver 实际顺序是：TCP/UDP 两项 before 控制 → 一个沙箱 probe 内分别尝试两协议 → 共同 post-attempt 观察窗口 → TCP/UDP 两项 after 控制。不是先做完一轮 TCP、再把另一轮 UDP 填进同一 sender/capture 身份。
3. 两协议各有 before/sandbox/after 三个新 32 位小写十六进制 nonce，六个互异。观察参数为整数 21 至 90 秒，实际后窗口 elapsed_ns≥20,000,000,000。after 控制必须按现行核验处于窗口中并在接收器仍存活时抵达。
4. 300 秒接收时长不自动保证覆盖接口/路由准备、原生运行、观察及控制；须依据实际起止/原件核验。若窗口或健康控制不足，保留失败/未知，不在同轮补日志或重放来伪造成功。
5. 两机 monotonic_ns 不能直接相减/比较。各机内核对顺序/耗时，跨机以同轮身份、端点、nonce、接收事件和受控过程关联；云盘同步时刻不当观察窗口。

若计划拆为独立 TCP/UDP sender/capture，必须另交对应身份、registry 匹配和完整窗口方案，不能将多个 sender 填进同一个未审绑定。

## 四、完成原件→真实登记→发布→消费

1. 等接收器和 sender 实际结束，保留所有失败原件。证人侧五份原件：receiver.jsonl、receiver.jsonl.summary.json、stdout.bin、stderr.bin、process-exit.json；外层 v3 的内部日志仍为 sandbox-witness-receiver-v2，父回执为 witness-process-exit-v1，不手改 schema。
2. 新 sender.json 及 source/transport/命令、scene.py/stdout/stderr、真实父 token/Job/profile/ACL/树终止、接口/路由/拓扑、typed rc/nonce/窗口、前后实现 SHA 全部绑定。发送成功、超时、rc0 或某个 winerror 都不是单独的双端通过。
3. 用实际完成原件构成 registry 候选七键：round、receiver_capture_id、expected_receiver_run_id、sender_run_id、sender_path、sender_sha256、input_bindings。至少绑定 IPv6 接口 stdout/stderr、transport.work 下三文件及本轮决定性路由/拓扑原件，保留旧登记，不先填期望 SHA。
4. Codex 审查候选；确认训练机按实际加载机制采用新配置 SHA 后，才允许对本 capture 调用已审 pack 的发布执行模式。此前原件保留在非同步区，publisher 不启用、不扫描它。
5. 当前 witness_pack.publish 会连续执行本地 staging、写同步 ZIP、最后写 .ready，没有独立的“只 stage、不发布”执行开关。不要先运行 --execute 再手工扣留 .ready；本单也不提供手写/修改 marker 的替代流程。默认 PLAN 不发布，但也不预先打包。
6. 发布仅限已完成的具名 capture，按已授权两端路径自动写包/标记；.ready 是工具最后写入，不是操作者可伪造的成功证明。本地 LOCAL_PUBLISHED 的 remote_arrival_verified=false，仍须训练机实际接收核验。
7. consumer 按稳定完整包→哈希/资源/路径检查→v3 预检→精确新 registry→注册对账→具名归档。包过早到达/未登记不假定会自动恢复；保留原件和失败状态，按现有策略另审，不改冻结 job。

## 五、判定与交付

接收原始日志应逐字节看到各协议恰当的 before→after 控制且没有 sandbox nonce，连续 seq、正确 run、端点/字节数、完整结束与原始流/summary/父回执相符。实际 sandbox 载荷收到为 FAIL；缺控制/窗口/原件为未验收，不能把它改称隔离通过。

D2 是 external IPv6 TCP，D8 是 UDP，分别裁决。D1 的 TCP IPv4 联合仍需对应 LAN IPv4 TCP、外部 IPv6 TCP、本机 IPv4 TCP；D7 独立需三份 UDP。九个 nonce 是**每个协议的三个组件各三阶段**，不能理解为 TCP+UDP 合计九个。旧 LAN D9 仅按已认可具名窗口继承，不冒充本轮 LAN 实测。

只交本轮核心原件、外部拓扑/授权/源码与新根说明、最终 registry 候选、发布/消费/对账回执，不索取全部历史语料。预检就绪、通道合格、注册对账、D2/D8 分项通过、43 点证书分别记账。当前其他 GAP、F2/F4 PARTIAL 和证书缺失不因本单改变；production=CLOSED、全局 NOT_ESTABLISHED、D2/D8 延后 GAP 保持。

相关上位审查：archives/reviews/codex-supervision/2026-10-17-ipv6-next-round-plan-review/NEW_ROUND_REQUIREMENTS.md 及 2026-10-17-root-boundary-mock-review/FIX_REPORT.md。后者仅设计/Mock 合格，真实路径/ACL/持久预留及原生接线仍待实现。
