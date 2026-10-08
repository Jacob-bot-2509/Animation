# Claude Code 验收监督与独立复验

更新：用户随后授权修复，A1/A2 已修改并通过本机原生复验，见 [修复报告](../sandbox-fix-2026-10-04/FIX_REPORT.md)。下文保留修复前审查记录；完整隔离验收及生产门禁仍未放行。

2026-10-04，项目 HEAD：`03eb5f203fa641d0a6ecf532006a436d860664cb`。

**结论：隔离验收不通过，生产不可信代码执行门禁必须继续关闭。** 普通权限下能创建 AppContainer 并启动进程已经有实测证据；这不能替代完整隔离验收。本轮没有修改项目核心代码，也没有解锁生产门禁。

## 独立复验发现的两个真实阻塞

| 编号 | 反例及实测结果 | 代码位置 | 验收结论 |
|---|---|---|---|
| A1 | 沙箱直接打开未授权合成文件被拒绝，errno 13；通过父进程继承的原生文件句柄却成功读到完全相同的合成标记 | `src/animtrain/appcontainer.py:294`，`bInheritHandles=True`，仅设置 SECURITY_CAPABILITIES，没有 HANDLE_LIST | 文件隔离被继承句柄绕过，FAIL |
| A2 | 沙箱父进程启动受控短时子进程；父进程超时被终止后，子进程仍存活。已核对其可执行映像为本轮专用 runtime，然后人工终止并等待退出 | `src/animtrain/appcontainer.py:305`，超时分支只调用 `TerminateProcess(pi.hProcess, 1)` | 超时未终止整棵进程树，FAIL |

证据：[edge-results.json](edge-results.json)。复现脚本：[probe_acceptance_edges.py](../elevation-test-2026-10-04/probe_acceptance_edges.py)。测试只使用合成文件和短时受控进程，没有读取用户秘密。临时 profile 使用系统 API 删除成功，检查对应目录不存在；本轮发现的残留子进程已经清理。结果中的历史 PID 不应用于后续清理，因为 PID 会复用。

建议修复：限定允许继承的标准输入、输出、错误句柄，使用 `PROC_THREAD_ATTRIBUTE_HANDLE_LIST`；用 JobObject 管理所有后代，挂起创建后先绑定 Job 再恢复执行，绑定失败时关闭执行；超时或异常应终止整棵进程树并确认退出。修复完成后必须重放上面两个反例。

Microsoft 对 [CreateProcessW](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw) 的说明明确指出，启用句柄继承会继承父进程中所有可继承句柄；[Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects) 提供进程组管理。这里的 FAIL 来自本机反例，不只是静态代码推测。

## Claude 新验收证据的审查

已保存正在变化的脚本、结果和核心代码快照，见 [快照及 SHA-256](claude-snapshot/manifest.json)。以下针对捕获版本，不代表后续修订已经复验。

| 项目 | 捕获证据/脚本问题 | 判定与补证要求 |
|---|---|---|
| P1 本机 TCP | sandbox 输出 `TOKEN_APPCONTAINER=False`，连接错误 10061 | UNVERIFIED。令牌 API 必须检查返回值和错误；不能把“目标拒绝连接”当作隔离成功 |
| P2 外网 TCP | 普通对照 CONNECTED，sandbox 返回 10013 | 有拒绝访问证据，但该项没有独立确认实际 AppContainer 令牌，尚不能整体验收 |
| P3 UDP | 对照与 sandbox 均输出 SENT，没有接收端收包证据 | UNVERIFIED。sendto 返回不能证明包已投递，也不能证明被隔离；必须记录接收端正反对照 |
| P4 IPv6 | 对照 CONNECTED，sandbox 返回 10061 | UNVERIFIED。需排除监听状态等影响，并确认令牌 |
| P5 子进程 | 捕获结果出现 SyntaxError；对照未保存 rc/stderr | 探针未成功，不能 PASS。修复后记录父子令牌、退出码、完整错误及实际访问结果 |
| P6 MathTex | 捕获结果没有此项；脚本主要记录 rc 和日志尾部 | 尚未验收。需真实产物、哈希、尺寸、媒体验证，并区分普通环境成功与沙箱成功 |
| P7 超时 | 只记录 TIMEOUT_EXPIRED，没有创建、核对并验证后代退出 | 无法证明进程树终止；独立反例 A2 已证明现有实现失败 |
| profile | `--skip-profile` 写入 hresult 0、already_exists true | 跳过应标明未执行，不应记录为实际 API 成功；新创建 SID 也需正确释放 |

脚本把原 `D:\Python`、项目 `.venv`、ffmpeg 与 MiKTeX 路径加入 `allowed_dirs`，会调用 ACL 授权。已要求 Claude 停止扩大原工具链权限、盘点实际修改并提出精确恢复方案。监督任务要求测试使用独立副本；不要在没有原始 ACL 基线的情况下盲目“恢复默认”。

已只读保存当前 [工具链 ACL](toolchain-acl-observation.json)。其中存在 AppContainer SID 授权，也有旧的 28 字节 SID 记录；没有本轮前的完整基线，不能把所有现存授权都归因于本次 Claude 执行。此次监督没有修改这些 ACL。

## 当前门禁及工作边界

- `render_gate.py:62` 仍拒绝 `trusted=False`，`network_isolation=False`；本轮反例位于尚未启用为完整生产隔离的辅助实现。
- 原修复的测试通过，不足以覆盖本轮两个新发现；普通权限启动成功也不足以解锁门禁。
- 20 条数据探针重试后结构解析为 20/20、首次为 3/4，只证明该样本的结构解析，不等于数学正确或全部数据验收。数据线不在本轮隔离放行范围内。

已通过 AI Bridge 向 Claude 发出：`msg_283` 支持任务、`msg_284` 两个独立反例、`msg_285` 验收脚本审查。支持任务只负责独立支持目录、环境盘点、固定可信 MathTex 普通环境烟测（必须标 ENV_ONLY）、最小依赖副本和清理方案，避免与核心修改冲突。

## 放行前必须复验

1. A1 继承句柄反例不能再读到合成文件，同时标准输出、错误捕获正常。
2. A2 在超时、父进程退出和启动异常时均无后代残留；绑定 Job 失败应拒绝执行。
3. 所有网络探针检查实际 AppContainer 令牌和 API 返回值，保留成功的普通对照及服务端收包记录；无法解释的超时、连接拒绝、跳过不能算 PASS。
4. 未授权文件读取与写入均被拒绝，允许范围内的读写正常；完整 Manim/LaTeX/ffmpeg 链产生可核验产物。
5. 同一提交上的回归检查通过，profile、进程、句柄和临时授权清理有证据；然后才审查是否具备生产接入条件。

## 新邮件 msg_287 复核（2026-10-04 01:46 北京时间）

Claude 提交 `78ed7d4d3878cdd5f10d1b9dfb391f1bfdf3b849`，新增环境、依赖、ACL 盘点及普通环境 MathTex 产物，并将此前隔离结果降为 UNVERIFIED/FAIL。它承认令牌信息类号用错、D 盘 MiKTeX 副本为空，以及对原工具链追加过 AppContainer 授权；邮件称已停止旧验收脚本。

独立核对 PNG、SVG、TeX 三项大小和 SHA-256 均吻合，ffprobe 验证 PNG 为 854×480。证据见 [邮件产物复核](mail-287-recheck.json) 与 [邮件支持文档快照](mail-287-support-snapshot/ENVIRONMENT.md)。这只是普通环境的静态公式产物；核心 `appcontainer.py`、`render_gate.py`、`preflight.py` 相对 `03eb5f2` 无修改，A1/A2 仍未修复。

发现新归因错误：邮件及支持文档把“无 MP4”归因于 PATH 缺 ffmpeg，但场景仅 `self.add(MathTex(...))`，没有动画或等待。已安装 Manim 的 `renderer/cairo_renderer.py:269` 明确规定无动画场景转为图片；`scene_file_writer.py:673` 的视频写入使用 PyAV。当前证据无法证明独立 ffmpeg.exe 缺失导致无视频。另，支持 `result.json` 的 ffprobe 字符串被截断，不能作为完整可解析的媒体验收记录。

已通过 `msg_288` 要求 Claude 在支持目录用含 `wait(1)` 或 `play` 的固定可信场景补普通环境 MP4 烟测，保留完整命令、环境差异、退出码、日志及完整 ffprobe JSON，并纠正归因。仍明确禁止运行旧隔离脚本、修改核心源文件或扩大原工具链 ACL。

没有批准整 SID 的 REVOKE 恢复方案：缺少变更前 ACL 基线，整 SID 移除可能影响既有授权。要求先证明哪些 ACE 是本次新增，无法精确回滚时应明确记录。当前只保存观察证据，没有执行权限恢复或删除生产 profile。**隔离验收结论仍不通过。**
