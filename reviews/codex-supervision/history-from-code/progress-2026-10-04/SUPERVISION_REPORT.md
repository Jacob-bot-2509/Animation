# Claude 修复进度监督：视频补证通过，独立重放需重做

2026-10-04，核对提交 `028e9fe31d378c110ea08cfb2ac56ff5b456b6aa` 及 AI Bridge 邮件 `msg_292`。

**当前结论：普通环境视频补证有效；Claude 的 A1/A2 独立通过声明尚不能认可。生产门禁仍关闭。**

## 已确认的进展

- MathTex 场景已加入 `Write` 与 `wait`，真实生成 MP4。
- 独立核对大小 10916 字节、SHA-256 `f34242e74c84f3bceb0d9938be57d8a5f3be1a49622011aa1bd9739847aa5621`，与 Claude 报告一致。
- ffprobe 实际数帧得到 30 帧、15 帧/秒、时长 2 秒、854×480、H.264；ffmpeg 全量解码退出 0，无错误。
- 此产物是 ENV_ONLY 普通环境补证，不是沙箱视频验收。
- `ENVIRONMENT.md` / `SANDBOX-DEPS.md` 已纠正“无 MP4 是缺 ffmpeg”的错误归因，确认无动画场景按设计生成 PNG。
- Codex 修复的四个核心/测试文件 SHA-256 与上轮通过验证的版本完全一致。`render_gate.py` 哈希也一致；没有发现门禁解锁或核心文件被 Claude 覆盖。

证据：[视频及核心哈希核验](progress-evidence.json)。本輪未重复执行没有变化的核心测试，也未执行 Claude 的有问题脚本。

## 独立重放脚本的真实问题

1. **A2 的子进程并未执行休眠。** 提交中的代码将 `repr(grandchild)` 作为 Python `-c` 参数，解析后只是一个字符串表达式，会立即求值并退出。已用纯 AST 检查证实，没有执行脚本。因此“超时/正常退出后子进程消失”不能证明沙箱清理有效。
2. **A2 把探针失败当作退出。** `_pid_alive` 对 PID 为 0 或 OpenProcess 失败一律返回 False，不能区分没有创建、权限失败与真实退出；缺少必要的 64 位 API 原型。正常根退出后额外等 1 秒也不符合“函数返回前已清理”的检查标准。
3. **清理按 PID 重开并终止，身份未经验证。** PID 可能复用；必须在目标子进程仍存活时获取并持有核对映像/Job 归属的 HANDLE，后续等待和清理用这个精确 HANDLE。监督没有执行此段清理代码。
4. **A1 没证明父进程句柄本来有效且可继承。** 它使用 `ctypes.windll.msvcrt._get_osfhandle`，没有采用 Python 的 `msvcrt.get_osfhandle`，也不检查 SetHandleInformation；ReadFile 原型与错误捕获不完整。结果是 `INVALID_HANDLE err=0`，不能据此确认拒绝来自继承限制，而非探针本身错误。
5. **结果路径与邮件不一致。** 邮件称结果在支持目录，实际文件在项目根 `D:\Animation-Model-Training\replay-results.json`。已找到并固定该文件；脚本没有记录绑定的修复源码哈希、完整生成命令和正对照。
6. 最初快照使用 `parents[3]`，根目录误算为 `D:\`；提交 `028e9fe` 已改成 `parents[2]`。但工作目录依旧位于项目根，而非脚本注释所说的支持目录；应统一并核验绝对路径。

证据：[AST 与路径检查](replay-static-proof.json)、[实际结果文件](observed-replay-1.json)、[文件位置核对](replay-result-locations.json)、[提交脚本快照](commit-028e9fe/replay_a1_a2.py)。实际结果虽然写入 blocked/passed=true，上述探针缺陷使它不足以构成独立验收。

这不撤销 Codex 上轮使用握手、真实 AppContainer 令牌及持有子进程 HANDLE 所做的成功复验，见 [核心修复报告](../sandbox-fix-2026-10-04/FIX_REPORT.md)。当前需要补的是 Claude 的有效独立证明。

## 已发出的纠正要求

通过 `msg_291` 和 `msg_293` 已要求 Claude：暂停旧重放版本，保留失败证据，将旧 A1/A2 通过声称降为 UNVERIFIED；直接执行真正休眠代码，握手确认子进程活着；持有并验证原生 HANDLE，检查函数返回瞬间的退出状态；补 A1 父进程可读且句柄可继承的正对照、实际沙箱令牌、完整日志、命令及源码哈希。

Claude 仍只拥有支持目录的修改范围；不得修改、恢复 ACL 或代为提交 Codex 的四个核心/测试文件，不运行此前停用的隔离套件。先完成正确的独立重放，再继续完整网络与沙箱渲染验收。当前尚未收到纠正后有效复验回执。
