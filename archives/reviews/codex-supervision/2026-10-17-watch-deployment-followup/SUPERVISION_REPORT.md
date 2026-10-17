# 持续消费服务部署跟进与验收

批次 run-ad3ade732a8e47a3967d8369d8498119；新报告 msg_1792171618506_841。

结论：**PASS_CURRENT_BOUND_CONSUMER_WATCH_LOCAL_DEPLOYMENT。** 本机具名 consumer watch 已实际运行，版本正确，等待期间持续持有独立锁；真实重复实例拒绝、一次包装记录的 STOP 退出码 0、后续唯一居民实例和同版本幂等均有证据。通过范围是本次、本机、既定 runtime 和版本的部署就绪，不承诺无限期可用性或全局沙箱准入。

本批无源码/配置修复。Codex 未启动第二 consumer、未创建 STOP、未重启或停止现有服务、未执行清理或发射探针。

## 当前进展

Claude 已按上一批交接部署 --execute --watch。当前常驻包装进程 cmd PID 46264、Python PID 33416，实际解释器 D:\Python Interpreter 3147\python.exe；父子关系与部署记录一致。只读观察器 PID 51704 仍正常。

新版本首次处理旧包形成 job-dde04273a99e42ebadc7d5237a792209，cohort：
e6ec6487a38b42791417c099fdc4ac3647682b52539d5a08089b4354604f8359。
它仍对应 lan-2026-10-13-a 和包 7d25d860a9cffb497f99e4e016c4228eab5b7aa5144e3c9ffac631b015efca6f。
后续日志出现 duplicate=true，符合新版本第一次复核、随后同版本幂等的策略，不算新实验。

## 独立核验

verification.json 保存 46 项具名材料/运行检查，全部通过；没有重跑源码及配置完全相同的前轮 35 项回归。主要证据为：

- 新 job 冻结集合、字节/SHA、全部回执输入、注册结果摘要通过。完整新注册 JSON 与上一批已独立重算结果，在仅替换 job 路径后全值一致；原始包一致，TCP/UDP 均为 D9，证书和生产标志未打开。
- 三个既有 job（9f6d800…、e652263…、dde0427…）的冻结清单和工件均通过；原 e652 清单 SHA 44a2a5748f213a5cc6ccfdb6d2fd9e982cd15eaeac6593eaae00fa4a6db3fbcd 保持。WJW 配置/发布回执原 SHA 也保持。
- 实际第二实例原始输出为 NOT_ACCEPTED / WORKER_BUSY / production=CLOSED。旧首启动 PID 41244 和第二实例 PID 37752 当前已不在，居民 PID 33416 存活，父进程为 46264。
- res-2-exit-code.txt 原始值为 0，批处理 w.cmd 在 Python 命令后立即捕获 ERRORLEVEL。结合 --watch 参数、处理日志与 STOP 记录，支持一次真实受控退出。首启动进程没有另附独立退出码文件，因此不虚构“两份原始 rc0”。
- 对实际 consumer-watch/worker.lock 做两次非阻塞探测，均被现存持锁实例拒绝；不读取或写入受锁字节。最初试图读取该锁字节遇到 Windows 强制锁的 PermissionError，已保留说明，改用无字节 I/O 的探测，不改变服务。
- 两次观察之间 res-3 stdout 字节数持续增长，后一次快照有 90 行，含真实重复处理和后续空扫描；stderr 为 0 字节，当前 STOP 不存在。锁在空扫描等待阶段仍持有，验证了上一轮修复所针对的实际运行场景。
- 四个当前修复文件与先前通过测试的冻结副本完全一致；实际加载的 consumer 配置源绑定通过。

关键版本：
consumer SHA 5694391fa2414aa0c1fb8f9af49b450230a017602a12c796639094abd58f87a5；
local SHA 8cf5f6fd80ca9f521694085e3eed9c7c67c8f36655828e1e1bc43827f3012d5a。

## 启动记录的正确解释

deploy-record.json 保存的是首次启动（PID 41244），不是当前居民 PID。记录链按以下方式解释，不覆盖原件：

| 阶段 | 证据 | 可判定范围 |
|---|---|---|
| 首启动 | deploy-record.json、pid.txt、stdout/stderr、作者 STOP 说明 | 当时版本/命令和已运行；现在进程已退出，未补造独立原始退出码 |
| 重启包装实例 | w.cmd、res-2 stdout/stderr、exit-code=0 | 一次可核验的处理与 STOP 退出，锁随后能重新取得 |
| 最终居民实例 | resident-pids.txt、res-3 stdout/stderr、实际进程与两次锁探测 | 当前同 runtime 常驻、幂等和空队列等待正常 |

部署日志仍属活动运行时，不能冻结其原目录。本目录保存时点快照，服务继续写原 runtime 日志，不把归档快照误当持续更新的当前状态。

## 同步目录为空与清理说明

本次实际看到 C:\Users\Jacap\OneDrive\witness 为空，因此 results=[] 是正常无待处理材料的等待状态。不是仅凭进程存在判断服务成功，而是结合此前实际处理、新 job、日志增长和真实锁验证。

作者在 841 报告称按用户指示清理了本机 10 项实验传输件，包括同步目录、OneDrive 根传递件及 D:\tmp 暂存。此为作者动作/授权转述，不是本会话新增权限。Codex 没有执行这些删除，也没有扩查个人云盘根或 D:\tmp 的其他数据，不能独立认证每一项删除清单和授权来源。

已独立确认本轮发布证据目录和三个冻结 job 保留且完整，故已验收证据链不因临时投递目录清空而丢失。不得由此推广为自动删包政策；后续清理仍按用户实际指示和具名材料范围执行，禁止改动冻结原件。

## 交接与边界

已接收正式报告，完成原始邮件/批次哈希核对并准备回信限定合格范围。Claude 可以按现有版本继续等待、处理批准的后续材料，不必重复修改已完成部分或重复同版本 35 项回归。新 round/capture/sender/native 绑定仍需实际提交；异常、源码/配置漂移和服务重启应保留新原始记录。

本次通过不等于新 LAN/IPv6 实验、全 43 点通过或生产解禁。D2/D8 保持延期 GAP，不阻塞训练准备；D1/D7 原依赖保留。全局隔离 NOT_ESTABLISHED、原生沙箱 UNVERIFIED、production=CLOSED，未开训。

归档 archives/reviews/codex-supervision/2026-10-17-watch-deployment-followup/；同内容兼容副本 reviews/codex-supervision/2026-10-17-watch-deployment-followup/ 供既有 ACK 校验。真实回信回执和最终清单在封存时纳入。
