# 发布者补证审查与持续服务就绪交接

批次 run-a1c7eeec374749f09e1983ef671f857b；邮件 msg_1792170680111_838。

结论：**PASS_BOUND_ONEDRIVE_REPLAY_CHANNEL。** 补交的 WJW 实跑配置、原始发布回执和暂存包，与已独立复算的训练机消费作业逐项一致，关闭上一批的本轮发布来源缺口。通过范围是声明端点间、具名旧 LAN 材料的一次传输回放管道；不声明远程身份认证、持续可用性或新沙箱实验通过。

修复后的 consumer watch 候选具备单实例部署条件，可由 Claude 在用户既有第二三层授权范围继续部署；真实持续服务仍待实际启动、处理、单实例拒绝和 STOP 退出记录。本批没有修改源码、配置或冻结原件，没有启动服务、探针或采集。

## 补交材料与对应关系

| 原件 | SHA256 | 字节数 |
|---|---|---:|
| wjw-run-config.json | 22bc005e43edca687c9ea77e3b5e6d5703b5f0a17def905200e44828964c6e8a | 2014 |
| wjw-pack/publish-receipt.json | acb6480a279dded4b8f90ba866df8eb386461fed9b409389a72033620591b8f9 | 963 |
| wjw-pack/7d25d860…zip | 7d25d860a9cffb497f99e4e016c4228eab5b7aa5144e3c9ffac631b015efca6f | 4844 |

实际 WJW 配置与当轮旧模板仅有批准的角色路径/active 变化：kit 根 C:\witness\wjw-witness-kit，capture_root 在 kit/captures，publisher-staging 在 kit/reviews/witness-automation，sync_root 为 C:\Users\WJW\OneDrive\witness；sender_registry 为空、production=CLOSED、采集/发射/开训与冻结写入开关不扩大。两角色各自根路径绝对、无穿越且互不包含。

发布回执为 LOCAL_PUBLISHED，receiver_exit_code 是整数 0；source_capture 的 round/capture 与包一致，五份 source_hashes 与实际包成员完全一致，ready_path 精确落在 WJW 同步根。remote_arrival_verified=false 保留原值：发布工具本身不证明远端到达；本轮到达由训练机实际 ZIP/READY 读取及冻结消费回执交叉支持。

WJW 暂存 ZIP 与本机当前同步包、原 job 包全部相同。consumer job 为 job-e652263c33094648a5113e70dfa5adab，冻结清单 SHA：
44a2a5748f213a5cc6ccfdb6d2fd9e982cd15eaeac6593eaae00fa4a6db3fbcd。
原结果仍为 REGISTERED_RECONCILIATION_COMPLETE，TCP/UDP 映射 D9，全局与证书标志均未打开。

89 项材料/归档核验通过，其中含上一批冻结归档的 57 件工件校验；这不是 89 项新测试。前轮 53 项原始消费材料检查、完整预检/注册重算及 35 项 watch 修复相关回归，以相同具名版本继承，不重复运行。额外当前源码/配置版本核对见 current-cohort-check.json。

发布者配置保留当时实际使用的旧 consumer SHA 2ed5a95e…；训练机现在使用修复后 5694391f…，两者对应不同时间的真实版本。没有要求篡改旧配置来匹配新源码。索引中的分钟级时间线作为作者运行记录保存，不当成独立测量的传输耗时、远程认证或 OneDrive SLA。

## 对上一批结论的更新

上一批档案及 NEEDS_EVIDENCE 裁决保持原字节、不重写。现在通过新的补证与独立核验，单独将“本轮发布者来源材料缺口”记为已关闭。WJW 回执是哈希绑定的本地生产者记录，不是密码学远程证明；本次沿用已约定的核心证据口径，不新增账号凭据、云端审计全量导出或历史语料要求。

本轮始终为 lan-2026-10-13-a、capture e605e0ee3a8b4388aa72271d56f473cd、receiver f801046c47a04deeb89cc442942f0bb6 的旧材料传输回放。不是新的 LAN、外部 IPv6 或全 43 点验收，也不补出 UDP 因果机制。

## Claude 下一步：部署一个持续 consumer

使用上轮 Codex 已修复的源码和本地配置，启动全新 Python 进程；无需重做采集、重新打包该旧包或重新索要已给的 OneDrive 总授权。后续只在约定专用同步目录及批准 sender_registry 内工作。

1. 启动前记录当前工具/配置 SHA；保留用户或其他操作员已有 STOP，不盲删控制文件。若确认为本次操作创建的测试 STOP，按部署记录解除后再启动。
2. 隐藏启动一个 tools/witness_consumer.py --config configs/witness_automation.local.json --execute --watch；运行日志写独立 runtime 子目录，不写冻结 job 或本审查目录。不增加计划任务。
3. 保存真实启动命令参数、PID、工具/配置版本、原始 stdout/stderr 和实际消费/等待状态。再次启动同 runtime 的 watch 应被拒绝，原实例继续；不要删除锁或修改 ACL 强开第二实例。
4. 在安全时点通过 runtime_root/STOP 验证完成当前作业后退出，保存真实退出码、末尾日志及锁释放；需要继续常驻时，记录本次控制文件处理和唯一新实例。
5. 新工具 cohort 首次处理现有旧 READY 可产生独立新版本复核 job；仍标旧轮回放，保留原 job，新版本重复送达再走幂等。不得把新 job 数量当新实验次数。
6. 后续每轮证人材料需要对应 round/capture/receiver/sender/native 原始绑定；不得复用旧轮身份冒充新轮。新配置/源码变更须重绑并重启，不在运行中迁移 runtime_root。

修复后 consumer SHA：
5694391fa2414aa0c1fb8f9af49b450230a017602a12c796639094abd58f87a5。
当前 local SHA：
8cf5f6fd80ca9f521694085e3eed9c7c67c8f36655828e1e1bc43827f3012d5a。
服务锁：consumer.runtime_root/consumer-watch/worker.lock；STOP：consumer.runtime_root/STOP。

提交上述部署回执即可审查持续服务是否已就绪，不要求再重跑已通过的 35 项同版本本地回归。既有就绪清单见上一批 WATCH_READINESS.json，本次将其中 R3/R4 的本轮核心发布/到达材料缺口关闭，R5 的实际部署仍待交付。

## 边界与归档

只读观察器 worker 51704 的心跳仍正常，它不自动审查或批准。production=CLOSED、全局隔离 NOT_ESTABLISHED、原生沙箱 UNVERIFIED；D2/D8 延期 GAP 不阻塞训练准备，D1/D7 原依赖保持。

源材料四个文件均未改；本目录保存收到时的原字节副本与哈希链。归档 archives/reviews/codex-supervision/2026-10-17-publisher-chain-review/；同内容兼容副本 reviews/codex-supervision/2026-10-17-publisher-chain-review/ 供原 ACK 校验。真实回信和最终清单在封存时纳入。
