# OneDrive 证据搬运与自动消费方案 v1

状态：**设计已交付，用户已选定 OneDrive；工具尚未实现或部署，云盘实际传输尚未验证。**
依据：用户于 2026-10-13 在 Codex 当前会话直接授权两项范围，并直接选择 OneDrive。完整授权见 [AUTHORITY.md](AUTHORITY.md)，当前资格口径见 [POLICY.json](POLICY.json)。

## 一、当前执行口径

D2（外部 IPv6 TCP）与 D8（外部 IPv6 UDP）推迟到有可达公网 IPv6 证人时补做；证据状态保留 GAP，原因和依赖保留。仅此缺口不阻塞训练准备。允许准备数据、配置草案、计划与本地检查；本条不签发训练运行许可，不把全局隔离或生产改成通过。

探针发射、接收器启动和双端实验排期仍由用户授权后 Claude 执行。Codex 负责第二三层材料搬运工具、独立审查和本地证据消费；这些工具没有探针发射入口。

原 IPv4 联合证据条件没有被修改：LAN IPv4 + 外部 IPv6 + 本机 IPv4，TCP/UDP 分别记账。缺外部 IPv6 时，D1/D7 不能被本方案直接标 GREEN；这项依赖明确显示为延期依赖，不借它重复阻塞已授权的准备工作。当前 LAN 对账代码把 LAN TCP/UDP 都记入 D9，保持原映射。任何实际泄漏或其他证据缺失仍单独报告。

数学、公式、视觉、原生与全局资格分别记账；production=CLOSED，full_surface_accepted=false。本设计不改变训练循环或生产证书检查器。

## 二、总体链路

```mermaid
flowchart LR
    A["用户授权＋Claude启动原v3采集"] --> B["证人侧捕获完成的原目录"]
    B --> C["第二层：本地打包／逐文件哈希／不可变发布"]
    C --> D["OneDrive约定同步目录"]
    D --> E["第三层：训练机监视／等待完整／复制本地快照"]
    E --> F["整包与成员哈希核验"]
    F --> G["现有v3预检"]
    G --> H["受限适配器：新目录内注册对账"]
    H --> I["分项报告／归档／幂等日志"]
```

控制链与被测 TCP/UDP 路径分开：自编工具只读写约定本地目录，OneDrive 客户端负责云同步，不实现两台主机直连传输。材料未到时是 WAITING_SYNC，不解释成被测通路失败。

单 worker 顺序消费一个作业；它不启动任何实验，也不操作 Claude 进程。OneDrive 客户端、本地 worker 与每10分钟邮箱任务各自独立，邮箱任务只接收结果和异常报告，不用邮件触发无限重试。

## 三、OneDrive 选型及接入条件

用户已选择 OneDrive，故配置中的 cloud_provider 固定为 OneDrive。两端应只同步专用共享文件夹 AMT-Witness-v1，确认双方账号有该目录权限和网络可达性；禁止把整个项目或 Desktop/Documents 备份当作证据通道。

建议两端将专用目录设为“始终保留在此设备上”。OneDrive 支持本地同步及该离线保留方式；新远端文件可能先以在线文件出现，不能仅凭目录项存在就消费。[微软同步说明](https://support.microsoft.com/en-us/onedrive/sync-your-computer-s-files-and-folders-with-onedrive)、[按需文件说明](https://support.microsoft.com/en-gb/onedrive/save-disk-space-with-onedrive-files-on-demand-for-windows)

使用短文件名、浅目录，只同步 ZIP 与 READY 描述符。微软文档分别列出云端和 Windows 路径限制，本方案主动采用短路径，不依赖机器开启长路径系统设置。[路径限制](https://support.microsoft.com/en-us/onedrive/what-are-file-path-length-limits)

当前只读检查发现训练机 OneDrive.exe PID29028；这只证明客户端进程存在。账号、共享目录、证人侧安装情况和两端可达性均未验收。本轮没有登录账号、改同步配置或上传材料。配置模板中三项实际路径仍为 null：证人 capture_root、证人 sync_root、训练机 sync_root，待实际接入时由操作者填写并核对。

同步目录可以在用户既有位置，工具不迁移 OneDrive、不改系统文件。原始材料和生产项目均保留在原位置。

## 四、第二层：证人侧完成检测与发布

拟新增 tools/witness_pack.py，支持 plan、once、watch 三种模式；默认 plan 不写同步目录。watch 仅扫描原 start_witness_capture.ps1 的 OutputRoot，不修改该脚本，因此保留 wrapper SHA 与 v3 EXE 绑定。

完成条件是：process-exit.json 已落盘、SERVE 模式、round/capture_id 合法、文件集合完整、原件前后两次内容哈希一致。目录名严格保持 round-capture_id。失败的真实退出码保留；非零码或错误不被改成成功，也不会人为补 stderr、summary、JSONL。文件不齐则产出 INCOMPLETE_CAPTURE 本地诊断，不产出可消费的标准包。

每个标准包精确包含六个 ZIP 成员：

```text
PACKAGE_MANIFEST.json
capture/<round>-<capture_id>/receiver.jsonl
capture/<round>-<capture_id>/receiver.jsonl.summary.json
capture/<round>-<capture_id>/stdout.bin
capture/<round>-<capture_id>/stderr.bin
capture/<round>-<capture_id>/process-exit.json
```

空 stderr 是合法的零字节原件，必须存在并带哈希；不传递重复 .b64、EXE、凭据或整个历史目录。manifest 精确列五项路径、长度与 SHA256，包含 round/capture_id/receiver_run_id、原 wrapper/exe SHA 和用途。schema 见 package-manifest.schema.json。

先在非同步本地暂存目录流式写 ZIP，关闭并逐成员校验，再复制到同步目录中的唯一 .partial 文件；关闭并复核后在该卷以排他方式发布 <ZIP_SHA256>.zip，最后发布 <ZIP_SHA256>.ready.json。描述符绑定整包字节数、整包 SHA 和包内 manifest SHA。已有最终对象若哈希相同则重复跳过；不同则 CONFLICT，绝不覆盖。

“最后发布 READY”只是生产端本地顺序，不承诺云端传输顺序。消费者必须独立验证；READY 先到也不能开始对账。生产端发布日志最多证明本地发布成功，直到消费端具名回执才记到达。

## 五、第三层：本地快照、预检和注册对账

拟新增 tools/witness_consumer.py 与 tools/witness_registered_adapter.py；先交付 once，必要验证完成后再启用 watch。默认 plan。工具只使用固定 argv 列表，不运行包内脚本、邮件命令或云端提供的 shell 参数。

按以下步骤单线程执行：

1. 启动时全量扫描约定目录，后续定时扫描；发现事件只是加速提示，避免进程重启漏包。只识别严格 SHA 文件名的 ready/zip 配对；未到齐或无法取得完整本地字节记 WAITING_SYNC。
2. READY 本身限制大小并严格验证 schema。采样稳定后把 ZIP 复制到项目内新作业目录；对本地快照验证整包长度与 SHA，源文件若变化则重新等待，稳定采样不能替代 SHA。
3. 验证 ZIP 仅六个允许成员、无重复名、无大小写碰撞、路径穿越、盘符、UNC、ADS、链接和异常压缩体量。默认整包上限 1 GiB、解压总量上限 256 MiB，manifest/READY 上限 64 KiB；这些是配置限额，超限拒绝并保留原因，不拆坏原件。
4. 流式解出五份普通本地文件，逐项长度/SHA 与 manifest 和 process-exit.json 核对；保持原 round-capture_id 目录名。写入均排他；输入或已冻结作业禁止覆盖。
5. 在操作者维护的 sender_registry 中以 round **及 receiver_capture_id** 选择唯一已批准本机 sender.json。核对 sender SHA、发送端 run_id、指定接收端 run_id、驱动与依赖文件绑定。包不能指定发送端绝对路径，也不能靠“最新文件”或时间戳猜配对；缺少批准项记 WAITING_SENDER_BINDING。
6. 调用现有 inspect_witness_evidence.py 的 inspect_capture 对普通本地快照做预检。必须是 READY_FOR_REGISTERED_RECONCILIATION 且无 findings，并记录实际输出、退出状态和工具 SHA；预检通过仅代表可进入对账。
7. 经新受限适配器调用现有已绑定版本的 driver.reconcile 做注册对账。它只读取既有原件，所有新产物必须写入新作业目录。禁止调用 collect、--execute-native、start_witness_capture.ps1 或任何探针。输入 SHA 在调用前后再次核对；输出需同时核验实际文件、JSON 契约、source/run/nonce/协议绑定及 CLOSED 标志，不能只看 rc0。
8. 输出 SUMMARY.json、REPORT.md 和实际工具记录。记录传输、预检、对账的分别结论；保留实际 D 点映射，不签全43点证书。写最终归档清单后冻结该作业；幂等 journal 在独立 runtime 目录更新。

### 现有入口的冻结目录兼容约束

实际检查发现原 REGISTERED_ROOT（reviews/codex-supervision/2026-10-06-all43-sandbox-repair）有 delivery-manifest.json。现有 driver.reconcile 既把该根用于输入路径检查，又向 sender.json 的父目录写新 reconciled-UUID.json。本方案不能直接从冻结原 sender 路径运行原 CLI，也不能向该旧根追加新作业。

新 namespace 固定为项目内 reviews/witness-automation/jobs/<job_id>；活动日志为 reviews/witness-automation/runtime。这两个落点不位于任何冻结归档下。

适配器设计约束：

- 把唯一批准的 sender.json 原字节复制到新 job 内；不重写 JSON 内的原路径、driver_source_path、接口采集引用或数学/证据内容。
- 加载现有哈希固定的 driver 模块，保持其真实 __file__ 与源码 SHA；仅在本次隔离模块实例内提供受限路径读写回调。**不是改 driver 源码或重新签旧 sender。**
- 读回调仅允许 registry 列明的旧原件路径及当前 job 输入；旧冻结路径只读。写回调仅允许当前 job 中预定新文件。拒绝源目录写入、重解析点和越界。
- 该方式尚需实现、代码审查与回归后才能部署；若发现现有验证存在隐含单根假设，应暂停交付可执行工具并修订适配器设计，不用临时改全局 REGISTERED_ROOT 绕过验证。
- 适配器 SHA、被复用的验证源码 SHA、路径策略版本和逐项回执一起归档。与原已提交 reconcile 结果比较时，只有派生作业的路径字段可按具名映射解释；原内容哈希、nonce、协议、case 判定与身份不能改变。

这样保持原 v3 证据契约，同时避开冻结原件追加问题。方案中的接口为拟新增，当前没有可运行的新工具命令。

### OneDrive 重解析点边界

OneDrive 云文件可能具有 CLOUD 类重解析标签，不能把所有 ReparsePoint 都当作目录链接，也不能把所有重解析点都放行。[微软标签定义](https://learn.microsoft.com/en-us/windows/win32/fileio/reparse-point-tags)

接入实现需检查实际标签和文件句柄最终路径：仅约定同步边界内的已知 CLOUD 类型可读取完整字节；名称替代型链接、junction、未知标签和越界路径拒绝。不更改云文件属性或清除标签。下载/复制后写入独立普通本地文件，再交给现有严格拒绝重解析点的 inspector；不修改 inspector 的证据路径规则。若该 Windows 接入实现不能证明边界，记 CLOUD_PATH_UNSUPPORTED，不能跳过检查。

## 六、幂等、恢复与隔离

逻辑唯一键使用原 round、capture_id、receiver_run_id 与批准 sender SHA；同逻辑身份对应不同内容 SHA 记 CONFLICT。ZIP SHA 可用于下载去重，但不同压缩元数据可能产生不同 ZIP SHA，不能作为唯一实验身份。所有时间和时长记录整数 ns；显示秒时使用分数，不做小数近似。两台主机的 monotonic_ns 不互相比大小。

每个消费 root 只有一个系统文件锁；第二个 worker 退出，不能并发创建相同作业。新 job_id 为 UUID，排他创建且不复用失败目录。写 journal 用同卷临时文件、flush 与原子替换。

重启时先查每个未完成作业的实际文件和具名回执。若对账已写结果但 journal 未提交，核验该结果完整绑定后恢复记录；不得盲目再调用生成一个随机 reconciled 文件。模糊结果记 RECOVERY_REQUIRED，保留原件；后续新版本另建 job，旧文件不删。

同步故障可按 5/15/45/120 秒间隔等待，达到限次后保持 WAITING_SYNC 并报告。坏 schema、版本漂移、nonce 不符、缺失原件、预检失败或真实泄漏不自动“修成功”，分别隔离；缺证据是 NEEDS_EVIDENCE，不是 PASS。临时目录不做跨 shell 删除，所有清理限于已核验的本任务路径且冻结作业不可清理。

每个 job 最终报告至少包含：

| 维度 | 状态示例 |
|---|---|
| 材料传输完整性 | HASH_VERIFIED / WAITING_SYNC / CONFLICT |
| v3 预检 | READY_FOR_REGISTERED_RECONCILIATION / NOT_ACCEPTED |
| 注册对账 | REGISTERED_RECONCILIATION_COMPLETE / FAILED / NEEDS_EVIDENCE |
| D2/D8 | GAP，用户允许延期，不阻塞准备 |
| LAN 与 IPv4 联合依赖 | 实际 D9 / 仍待联合材料 |
| 全局/生产 | NOT_ESTABLISHED / CLOSED |
| 训练准备权限 | AUTHORIZED；其他准备检查单独列明 |

哈希链证明内容一致性，不宣称远程来源认证；当前父进程回执仍是有哈希绑定的生产端记录。共享目录权限和批准 sender registry 是本方案的来源接入边界。

## 七、验收及实施顺序

本地候选工具实现后，按实际故障验证，不以“文件存在”或状态字符串代替验证：

| 用例 | 必须得到的行为 |
|---|---|
| 合法五原件、空 stderr | 字节往返一致；保持原目录名与身份 |
| 非零真实 rc、缺文件、截断原件 | 实际失败/缺口保留，无成功假回执 |
| READY 先到、ZIP 半份、客户端断网 | 等待，不能预检或对账 |
| 错 SHA、重复 ZIP 名、Zip Slip、ADS、大小写碰撞、zip bomb | 拒绝且无越界文件写入 |
| 本地链接/junction/云标签未知/复制中更改 | 拒绝或等待；已知 CLOUD 类型经受限读取验证 |
| sender 不匹配、旧源码 SHA、缺 native 依赖 | NEEDS_EVIDENCE / VERSION_DRIFT，不运行探针补证 |
| 同包重复、同身份不同包、进程崩溃和双 worker | 单次具名消费、冲突不覆盖、可核验恢复 |
| 现有 LAN 材料的本地导入与对账 | 逐字节原件不变；按代码记 D9，不改成 D1/D7 |
| 脚本调用与注册适配器 | 网络发送/collect/start_witness 调用为零；旧冻结目录新增项为零 |
| 完成归档 | 清单集合/长度/SHA完整；production与证书标志保持CLOSED/false |

顺序：当前方案与授权落地 → 实现一次性 pack/consume/adapter 并本地验收 → 确认两端三项实际路径及共享权限 → 操作者完成 OneDrive 到达试验（仅材料传递）→ 启用隐藏 watch 包装 → 用户授权、Claude 执行下一轮采集后自动消费。探针排期不由本工具安排。

当前交付附带 provider=OneDrive、active=false 的配置模板、两个 JSON schema、一个只供设计验证的字节无损样包与本地契约检查记录。样包 purpose=DESIGN_FIXTURE_ONLY，运行工具必须拒绝将它注册成新实验。它是现有材料的派生载体，不是新采集或新沙箱证据。
