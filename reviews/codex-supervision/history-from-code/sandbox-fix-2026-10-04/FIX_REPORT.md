# AppContainer 继承句柄与进程树清理修复

2026-10-04。根据用户“由你来开始修”的授权，直接修改项目四个文件；尚未提交 Git。生产不可信代码执行门禁没有解锁。

**结果：两个已复现缺陷已修复，并通过真实 Windows AppContainer 反例复验。完整隔离验收仍未完成。**

## 修改内容

| 文件 | 修改及作用 |
|---|---|
| `src/animtrain/appcontainer.py` | HANDLE_LIST 仅包含显式 NUL 标准输入及标准输出/错误句柄，阻止继承父进程其他可继承句柄；进程挂起创建、绑定 Job 后才恢复；失败拒绝执行；超时、异常和正常根进程退出均清理后代 |
| `src/animtrain/win_job.py` | 新增原生句柄绑定和整树终止等待；核对 Job 内存及 kill-on-close 标志；枚举成员、验证 Job 归属并持有进程句柄等待退出，避免仅看进程计数或复用 PID；补齐 API 原型及初始化失败资源释放 |
| `tests/test_appcontainer_lifecycle.py` | 新增 11 项启动与清理故障回归，覆盖绑定失败不恢复线程、恢复失败、超时输出保留、等待失败、部分文件创建失败及捕获句柄只关闭一次 |
| `tests/test_win_job_cleanup.py` | 新增 3 项 Job 清理回归，验证计数为零仍等待成员句柄、未确认退出不能返回成功、复用到其他 Job 外的 PID 不被等待 |

捕获文件使用随机名称并以 CREATE_NEW 打开，避免旧名称碰撞和截断已有文件；超时通过 `TimeoutExpired.output/stderr` 返回已捕获日志，同时清理临时捕获文件。调用者不应再依赖旧的 `.ac-out-{id(args)}.tmp` 遗留文件。

Windows 启动保留可修改的命令行缓冲区及属性值的生命周期；环境块按变量名排序。AppContainer 启动 Job 使用 2048 MB 内存上限，绑定失败不运行子进程。

## 真实反例复验

见 [完整原生结果](native-results.json) 和 [复现脚本](native_recheck.py)。脚本只使用可信合成数据、D 盘独立 runtime/work 和随机临时用户 profile，不修改 C 盘系统文件或原工具链 ACL。

| 检查 | 修复前 | 修复后实测 |
|---|---|---|
| 实际 AppContainer 令牌 | 既有原生启动实测为 True | 再次正确查询 TokenIsAppContainer（信息类 29）及 API 返回值，为 True |
| 未授权文件直接读取 | errno 13 | errno 13 |
| 继承句柄读取同一合成文件 | 成功读到合成标记 | Windows 报无效句柄，读取失败，无字节泄漏 |
| 标准输入、输出、错误 | 未全面检查 | stdin 为 EOF；stdout/stderr 捕获正确 |
| 超时后的子进程 | 仍存活 | 测试先持有确认存活的目标子进程句柄；函数返回后该句柄已 signaled |
| 正常根进程退出后的后台子进程 | 未覆盖 | 同样确认目标子进程退出后才返回 |
| Job 绑定失败 | 无绑定流程 | 注入失败时受控子进程代码未执行 |
| 宿主原生句柄数 | 未覆盖 | 一次完整调用前后均为 179，没有增加 |
| 捕获临时文件 | 超时遗留 | 0 个残留 |

原生复验额外发现 Job 的 ActiveProcesses 可以归零而进程句柄尚未 signaled，已补充成员句柄等待后重测通过。首次探针对无效句柄的异常未捕获，以及清理时序失败的原始记录均保留，没有删除失败证据：[首轮记录](native-results-first-invalid-handle.json)、[清理时序记录](native-results-accounting-race.json)。清理时序失败时出现的本轮受控子进程已按持有的精确句柄清理。

三次测试的 profile 均使用系统删除 API 成功删除，目录和 HKCU 映射不存在，见 [清理复核](cleanup-verification.json)。D 盘合成工作文件与测试证据保留用于重放；独立 runtime 上的测试 SID ACL 不等于原工具链 ACL 的恢复。

## 回归与交付证据

- 完整项目 unittest：336 项通过，0 失败、0 错误、0 跳过。见 [结果](unittest-full.json)、[完整日志](unittest-full.log)。
- 随后新增的 3 项 Job 清理回归已单独通过；生产核心代码没有在完整测试后再修改。
- 原生结果状态为 `PASS_TWO_FIXES_ONLY`，仅表示本轮修复通过。
- 四个文件的 `git diff --check` 通过；写回前核对原始文件 SHA-256，未覆盖他人并发修改。
- [可审查补丁](fix.patch)、[原始哈希](baseline-hashes.json)、[最终文件哈希](fixed-file-hashes.json)。没有打包、恢复或提交项目其他已有改动。

本方案依据 Microsoft 的 [HANDLE_LIST 属性说明](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute)、[Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects) 和 [TerminateJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-terminatejobobject)；修复结论来自上面的本机正反例及回归证据。

## 尚未放行的范围

生产 `trusted=False` 仍拒绝执行。外网、UDP、IPv6、完整沙箱 MathTex/视频渲染、依赖副本与授权范围仍须完成验收，本轮不将其标为通过。当前子进程原生探针覆盖受控父子进程，更多层级与并发派生边界应纳入后续完整验收。

已通过 AI Bridge `msg_290` 通知 Claude 修复结果并要求独立复验；它仍负责支持目录下的普通环境视频补证，不应改动或代为提交本轮四个核心/测试文件。
