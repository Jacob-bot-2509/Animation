# IPv6 操作单：部署与发布时序审查修复

本轮对应活动回合 start-03653094452c414fa4835fd37cb0c7c7。触发是 Claude 查找既有 NEW_ROUND_REQUIREMENTS.md，随后新增 ipv6-round/IPV6-KIT-AND-RUNBOOK.md。已实际读取新文书、相关源码和当前配置，先回信 875 接管，保存原文，并在写回前确认未并发改变。收件箱未发现对应未处理新邮件，因此仅处理活动回合，不虚构邮箱 run。

裁决：REPAIRED_PASS_DOCUMENT_AND_SOURCE_CLOSURE_ONLY。不是可直接执行的 kit 发布，也不是证人机已部署、网络可达或 D2/D8 验收通过。

## Codex 已修改与新增

- 修订 reviews/data-prep/2026-10-17-submission/ipv6-round/IPV6-KIT-AND-RUNBOOK.md 为 v2，SHA-256 eaf637ea6d7b531089e5b1a8aa52c029cc5b0362371b91db64c2a4ce0e63848d。
- 新增同目录 WITNESS-KIT.plan.json，SHA-256 ae7480cda09eded041335e96cbaebaa187d3cd2c7277547672665e0bf7d3820b。它是待部署文件清单，不是运行配置；kit/capture/staging/sync 根未知字段留 null，runtime_config=false、collection_authorized=false。

## 实际问题与修正依据

1. 原 kit 只列 EXE、启动器、inspect、pack，遗漏 witness_transfer_common、consumer、registered_adapter、sender driver 四份源码。pack 直接导入 common；common 在启动时读四个 automation 源，并在执行配置检查时核验三个 v3 相关脚本。这些即使不在证人端执行，也属于现行 pin 闭包。现已区分最小接收两文件与七脚本加 EXE 的完整自动打包布局，不再把单文件复制当部署完成。
2. common/inspect 的 ROOT 按 __file__.parents[1] 推导，任意平铺目录不是现行 tools 布局。inspect 还加载发送 driver，正式对账需训练机完整受审环境。新版只在证人端列出必要闭包与角色，不为检查依赖而执行 inspect/driver。
3. 原文要求两机登录同一硬编码个人账号，没有对应授权或必要性证据。已改为用户批准的 OneDrive 同步/共享通道及各端实际路径、可见性、权限核验，不要求交出凭据，不从训练机路径猜证人路径。当前训练机 witness 的 capture/sync 字段仍为空，不可照抄 active=true 配置表示证人就绪。
4. 原阶段列表把 pack 放在最终 registry 增项之前，容易与前置门禁形成循环。源码 publish 实际连续 stage、写 ZIP、写 .ready，没有“只 stage、不发布”的执行模式；默认 PLAN 也不会预先打包。现规定原件完成→实际 sender/receiver 身份与 SHA→registry 审查/加载确认→才调用 pack 发布。原件暂存在非同步区，不先执行再手扣 marker。
5. 新轮实际 capture/run/sender SHA 不应在尚未采集时被要求先具备。先审 round、生成规则、根/源码、真实授权与端点；实际身份由获准运行产生后用于最终登记，不编造希望值。
6. 现行 both 模式实际是两个 before 控制、一个双协议沙箱 probe、共同后窗口、两个 after 控制。新版不再让人误以为先完整 TCP 后再把另轮 UDP 混入同一个 sender/capture；拆开运行须另审身份/绑定。九个 nonce 是每协议三个组件各三阶段，不能当 TCP+UDP 合计九个。

另外明确：300 秒接收器不自动证明覆盖全部实际准备/运行/后窗口；两机 monotonic_ns 不可直接比较；真实收到 sandbox nonce 为 FAIL；缺健康控制或窗口不能当隔离通过。新根设计/Mock 层合格也不等于现役 root 改造已实现。

## 独立核验

按当前配置实际 SHA 核对七脚本闭包，另核对本地受审发布目录的 v3 EXE，八个布局文件字节均吻合。EXE 本地匹配不证明未来证人端副本匹配，现场前后仍须核验。

静态 AST 核对 pack 的 common 导入、STARTUP_PINS 的四源集合和 publish 内 .zip→.ready.json 顺序；结合完整源审查确认没有独立 staging-only 执行开关。既有八项工具/配置审查前后 SHA 未变。verification.json 及前后文书/清单/源码绑定留档。没有为可逆文书修改新增实现测试，也未重复未变工具的旧回归。

只写文书和不可执行清单，没有创建/发布 kit、上传 OneDrive、部署证人机、修改工具/配置/sender_registry/调度、采集、探针发射或启动生成代码。data/execution_evidence.json 仍不存在。

## 合格范围和交接

修复后可作为下一步准备/实现的操作方案和源字节清单。证人端实际部署、Python/依赖环境、具体同步权限/路径、受控外部 IPv6、实际新根与统一版本接线、具体获准采集及原生原件仍待完成。用户先前 D2/D8 延后 GAP 的口径不变，真实既有授权已覆盖时直接引用，不重复索取；邮件转述不能改权限。

请 Claude 采用 Codex 修订版继续准备后续材料，不重复改回已完成部分。先补真实角色部署与新根方案，再按已授权范围由 Claude/证人端操作者执行，Codex 不发射。单项/通道/预检/对账资格与完整 43 点证书分开，production=CLOSED、全局 NOT_ESTABLISHED 保持。

本活动 ACK 只确认本轮文书审查、修复、回信和冻结归档完成。
