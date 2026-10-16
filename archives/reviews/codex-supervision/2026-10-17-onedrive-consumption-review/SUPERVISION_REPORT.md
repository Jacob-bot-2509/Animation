# OneDrive 新报告接收、复核与 watch 修复

批次 run-140a171a9d1a4ab6b9cd8c5a6528aee2，接收邮件 msg_1792169552651_833、msg_1792169617421_834。原始快照已核对 packet、journal 与原件 SHA，完整材料纳入本目录。

结论：**本机包到达、消费预检及注册结果已独立通过；完整跨端发布来源链仍 NEEDS_EVIDENCE。watch 生命周期缺陷已由 Codex 修复并通过 35 项相关回归，实际持续服务未由 Codex 启动。**

## 已接受的新材料

新 job：reviews/witness-automation/jobs/job-e652263c33094648a5113e70dfa5adab。
其冻结清单包含 13 件工件，连同清单共 14 个文件，所有字节数、SHA 和文件集合通过。清单 SHA：
44a2a5748f213a5cc6ccfdb6d2fd9e982cd15eaeac6593eaae00fa4a6db3fbcd。

已直接读取指定同步目录的 READY（365 字节）与 ZIP（4844 字节）；两次完整快照、包内六成员及五份原件一致，job 包与同步包字节完全一致。包 SHA：
7d25d860a9cffb497f99e4e016c4228eab5b7aa5144e3c9ffac631b015efca6f。

新注册结果：
reconciled-1340170d2ba84b4fa9f071b521b0c942.json，
SHA 761f4b661fc28035abfecfe48e4dde753908081aa7c585d7cc9b4c28d995451f。
Codex 使用当轮已钉版本函数独立重算预检，并把完整注册输出截留在内存，与该 JSON 全值比较一致；没有重跑消费、写冻结 job 或发射探针。六份原 sender/native 原件及回执全部输入绑定也通过。53 项具名材料核验见 verification.json，不与测试用例数量混计。

本轮仍是 lan-2026-10-13-a、capture e605e0ee3a8b4388aa72271d56f473cd、receiver f801046c47a04deeb89cc442942f0bb6 的旧材料回放；TCP/UDP 仍映射 D9。发送机观察时长为 21000477800 ns，即 105002389/5000000 s。没有新增沙箱实验或 IPv6 实验，也未建立 UDP 拦截机制因果证明。

## 需要收紧的报告结论

邮件 834 把“通道 PASS”作为全链路结论，但同时说明 WJW publish-receipt.json 与实际配置尚待回传。本机消费结果不能单独区分跨端发布、同机复制或旧包重放的来源过程。现阶段只签本机已到达包及注册消费的具名范围；完整 WJW → OneDrive → 训练机链在原始发布回执、当轮配置/工具绑定及真实同步关系补齐前仍缺证据。

这不否定现有 job，也不要求重做 LAN 采集。原件保持；本目录 QUALIFICATION.json 明确限定合格范围，不覆盖作者冻结报告。接收、归档一份报告不等于批准其全部结论。

## Codex 已实际修改并复验

部署审查发现 consumer 只在 scan() 期间持锁，sleep 时释放，两个 --watch 可以交错存活；运行中变更 runtime_root 还可能转移到不受原锁保护的根。新测试先在旧版复现这两项失败，再修复：

1. tools/witness_consumer.py：增加独立 consumer-watch 生命周期锁，覆盖所有等待；每次扫描仍使用原 job 锁。运行根变化拒绝并要求重启；STOP、异常返回和单次消费保持明确行为。
2. tests/test_witness_consumer_service.py：新增 7 项回归，验证等待期间第二实例拒绝、锁与扫描互不冲突、运行根改变拒绝、退出释放、已有 STOP、单次及 PLAN 无服务锁。
3. configs/witness_automation.example.json 与 local.json：只替换 tools/witness_consumer.py 的 source pin。其他字节/字段保留，local 的 active=true、训练机路径、registry 和证人 null 路径均未改。没有未经说明将其改回 inactive。

最终 7 项新增测试与 28 项关联回归全部通过，git diff --check 通过。原 28 项因 consumer 源码改变而重新运行，未将继承结果当本次实测。测试只使用项目隔离夹具，保留生成的冻结测试记录；没有运行真实 consumer watch。一次额外只读检查的自动审批超时，缩小为项目内核验重试后完成；没有据超时推断操作不安全或绕过审批。

修复后 consumer SHA：
5694391fa2414aa0c1fb8f9af49b450230a017602a12c796639094abd58f87a5。
修复后 local SHA：
8cf5f6fd80ca9f521694085e3eed9c7c67c8f36655828e1e1bc43827f3012d5a。
修复前后源码与配置、先失败后通过输出及绑定见 before-repair、after-repair、repair-file-bindings.json、post-repair-verification.json。

旧 job 仍记录其实际使用的旧 cohort（consumer SHA 2ed5a95e...），其全部 14 文件哈希在修复及测试后保持不变。不得回改旧回执的版本。新 cohort 首次处理当前旧 READY 时按既有版本策略可能另生一个新版本复核 job；这是旧材料在新工具版本下复核，不是新实验，之后同版本交付再走幂等复用。

## 给 Claude 的就绪清单

具体见 WATCH_READINESS.json。优先补交 WJW 本轮 staging_root/pack-<context>/publish-receipt.json，及实际使用的非凭据配置：capture/sync/staging 根、active、全部 source pins 与范围开关；核对发布输出、真实执行结果、两端专用同步目录关系和到达记录。缺失输出如实说明，采用现存真实材料交叉验证，不补造历史日志；不交密码/token，不扩大历史语料。

这些材料核验后，再用新的 Python 进程加载修复后的 pin 启动一个隐藏 consumer watch，留独立日志、版本、实际处理和 STOP 退出回执。服务锁在 consumer.runtime_root/consumer-watch/worker.lock；STOP 仍在 consumer.runtime_root/STOP，完成当前工作后于下一轮退出。不可删锁或改 ACL 强行并发，不新增系统计划任务。后续新轮必须有各自身份和审批绑定。

Codex 已向 Claude 通知接手范围，完成后实际回信交付；要求按修复版本继续，不重复修改完成部分。冻结目录和既有用户/Claude 改动均保留。

## 监听和资格边界

上一轮修复的只读观察器仍正常，worker 51704，已捕获新 job 文件事件；源码 SHA bd29b8548f1f9318c0ebb537d68f12862f65180027b52504c7a8edbf4ca484d4 未变。它只记录，不自动放行。

D2/D8 保留延期 GAP，不阻塞训练准备；D1/D7 原依赖保留。全局隔离 NOT_ESTABLISHED、原生沙箱 UNVERIFIED、production=CLOSED，未开训。watch 修复的本机测试通过不等于持续部署或全局准入通过。

归档 archives/reviews/codex-supervision/2026-10-17-onedrive-consumption-review/；同内容兼容副本 reviews/codex-supervision/2026-10-17-onedrive-consumption-review/ 供既有 ACK 使用。真实交接回执和最终清单在封存时纳入。
