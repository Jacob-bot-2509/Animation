# Claude Code 验收进程监督

2026-10-04，UTC+8。复核范围为 Claude 的最新回信、活动进程、提交 8cb3f9e 和新文件验收支持脚本。**本机回环已获第三轮独立复核认可；新文件验收脚本 v1 尚不具备原生执行条件，已发具名整改清单。MiKTeX 方案仍待补证，生产门禁 CLOSED。**

## 当前进程与交付

- 两次直接进程检查均见 Claude Code 的 PID 45116、27720。它们是 VS Code 扩展启动的进程；仅凭进程存在不能判定忙闲，但 15:52 的新提交及最新回信证明近期有交付。
- 最后一次直接检查未见 Python 文件/网络原生验收、TeX 或 FFmpeg 渲染进程。15:58:24 的保存快照里两个 Python 进程是本轮监督检查自身的 venv/base 父子进程，检查结束后已不在后续列表中。未结束任何进程。
- Claude 已提交 8cb3f9e，只包含 file_acceptance.py 与 MIKTEX-INVENTORY.md 两份支持材料。没有据此接受文件隔离或渲染通过。
- 11 份本人网络模块/测试和既有底层、门禁及支持文件哈希全部匹配上轮已验收基线。见 [状态及哈希](status-snapshot.json)、[进程快照](process-snapshot.json)。
- Claude 在 msg_325 逐项确认第三轮六项修复、独立 392/392 测试（网络 53/53）及原生记录一致，本机四个回环场景可以限定范围收口。外网及完整沙箱渲染仍未验收。

## 新文件验收脚本的实质问题

审查快照 SHA256：1589780eab7c8d7274f2b6528417aa9b3e5689e9001648820b44da40b93f6a4a。源码原文见 [快照](file_acceptance-snapshot.py)。这份 v1 的问题已反馈，后续必须以新 SHA 重新审查，不将本报告套用到未核实的新版本。

| 项目 | 独立结果 | 要求修订 |
|---|---|---|
| 令牌真假接线 | 客户端输出 is_appcontainer 为 int(1)，接线却要求 is True，真实有效 AC 令牌也会被拒绝 | 复用已回归的规范 token_identity 并绑定源码哈希，检查完整实际令牌身份 |
| 未知状态误通过 | target_created=None、content_leaked=None、两端 timed_out=None、未知操作 kind、spawned=1 共 6 类输入均得到 PASS | 明确类型及操作枚举，未知不通过，拒绝类必须有明确 False 的监督端事实 |
| 正写控制污染 | 全内存接线模拟中，沙箱完全不写但谎报正确 outcome/hash；控制预先写了同一目标和同一内容，最终仍 PASS_LOCAL_FILE_ACL | 控制与沙箱用不同目标/随机内容，执行前检查目标不存在，分别保存真实落盘哈希 |
| 自检失败不阻断 | 全模拟 main 的 all_hold=False，仍 PASS_LOCAL_FILE_ACL 并返回 0 | 自检作为前置门禁，失败只能 UNVERIFIED/错误；保留已有 FAIL 的优先级 |
| 错误证据不完整 | 全模拟 main 出错后 JSON 仅有 error/traceback/command/run_id/partial_results_keys | 写完整 state/overall/范围/门禁和已完成原始记录；原子落盘，写入失败显式报告 |
| 路径边界 | startswith 接受 support-other 同前缀兄弟目录 | resolve 后验证目录归属，拒绝重用和重解析点逃逸；仅新建具名工作区 |
| 独立观测与完整性 | 拒写控制文件未先独立核验哈希就删除；读对照缺文件前后快照；runtime 仅存在性、单 exe 哈希 | 保存控制和监督端事实；复用审定 manifest/_pth，核验实际 client/executable 自哈希与路径、前后不变性 |
| 读哨兵输入 | denied_read 命令直接传入秘密哨兵 nonce | 不把应由实际读取才能得知的秘密内容提供给沙箱参数，保存实际读取证据 |
| 自检计数表述 | 代码实际 13 条总案例：10 负例、3 正例；邮件称 13 负例+3 正例 | 更正计数并补上述独立负例 |

复现仅抽取纯函数并对所有文件、ACL、profile、客户端及 subprocess 接线做内存模拟；没有调用该脚本的原生主流程或执行实际授权。

见 [独立判定/接线复现](draft-independent-reproductions.json)、[主入口故障复现](draft-main-fault-reproductions.json)、[原内置自检](draft-builtin-regressions.json)。原自检全持并不覆盖上述缺口。已通过 msg_327、msg_328 将具名复现和修改要求交给 Claude，由他负责自己的支持脚本；没有覆盖他的文件。

## MiKTeX 方案

D 盘当时可用 109618438144 字节，空间不是当前卡点；源目录 565 MB 是 Claude 的盘点值，本轮没有重新递归统计，也没有复制。

方案将 MIKTEX_PORTABLE=1 标成“官方便携模式”，尚无该版本的支持依据。官方说明采用便携安装器及启动脚本；官方环境变量页也没有列出 MIKTEX_PORTABLE 或 MIKTEX_USERDATA。因此不能仅凭这两个变量认定普通安装目录的副本已自持。[便携版说明](https://miktex.org/howto/portable-edition)、[环境变量文档](https://docs.miktex.org/manual/envvars.html)。这里是待证结论，并非宣称变量在所有版本绝对无效。

robocopy 小于 8 表示没有报告复制失败，但某些返回值仍代表存在不匹配或额外文件，不能替代完整副本验证。[Microsoft 返回码说明](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy/)。已要求补完整源/目标相对路径、文件数、字节数、SHA 清单，以及安装/用户配置/用户数据/包根、格式/字体/动态库和重解析点处理方案。普通环境输出和缓存应限定到具名 D 盘目录，自动拉包策略也需明确。

已通过 msg_330 要求更正方案并补依据；当前没有批准复制、工具链 ACL 或渲染。

## 后续与证据落点

下一步由 Claude 修订自己的文件支持脚本及 MiKTeX 方案，交回新 SHA、合成正反测试和修改清单；我再独立复核接线、证据与原生执行条件。生产门禁持续关闭，不因本机回环通过自动放行其它验收。

按 msg_329/331 的落点建议，已在 msg_332 确认：后续新监督材料归入训练项目 reviews/codex-supervision。历史 D:/code/output/claude-supervision 材料保留原位，既有链接不破坏；本轮早期已写的 7 个具名记录只复制了副本，来源与 SHA 见 [证据来源](evidence-provenance.json)。不再向旧 output 目录写后续增量。


## 迁移更新（2026-10-04）

用户随后明确要求将 Codex 此前在 D:/code 写的任务产物全部搬入本项目。原“历史材料保留原位”的落点安排已被替代：历史文件现在位于 [history-from-code](../history-from-code/)。原始 JSON 的来源路径保留历史观测值，实际位置使用 [迁移记录](../2026-10-04-artifact-migration/MIGRATION_REPORT.md) 中的映射。
