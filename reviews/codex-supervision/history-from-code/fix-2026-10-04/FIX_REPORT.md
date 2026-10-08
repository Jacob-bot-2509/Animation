# Codex 协助修复结果（2026-10-04）

基线：68c51bed55fd4679568a1cd0b676f70a043791a2。以下修复已直接应用到 D:/Animation-Model-Training 工作树，尚未提交。

## 已修复

1. [appcontainer.py](/D:/Animation-Model-Training/src/animtrain/appcontainer.py:161)：用 HRESULT 正确判定系统 SID 派生结果；取消自行构造 SID 的回退；复制系统 SID 后 FreeSid 释放；使用 use_last_error=True 及即时保存的 Win32 错误；增加配置目录前置检查，在 mkdir 和 ACL 修改前拒绝未配置的容器。
2. [preflight.py](/D:/Animation-Model-Training/tools/preflight.py:121)：先按当前清单实际文件选择相关锁，再校验哈希。其他版本的损坏锁不再误阻断当前版本；当前版本坏锁、部分覆盖、错误绑定及无法归属的损坏锁仍阻断。结构错误转为可定位失败，避免直接异常退出。
3. [eval_test_prep.py](/D:/Animation-Model-Training/tools/eval_test_prep.py:47)：候选清单包含新活动 data/manifest.json；绑定清单必须实际覆盖所选文件，防止用无关归档清单哈希冒充有效绑定。

替换了 test_appcontainer.py 的恒定 SKIP，增加真实系统 SID 比较、HRESULT 零成功、错误 HRESULT、空 SID、内存释放和配置前置检查回归；新增 [test_version_lock_review.py](/D:/Animation-Model-Training/tests/test_version_lock_review.py) 的 8 条版本锁边界回归。

## 验证

- 最终完整测试：376 passed，29 subtests passed，无 skipped。
- git diff --check 对本轮源码与测试通过。
- 真实 status --dir data/v2：eval/test 两把活动锁均通过；v1 锁 INFO 其他版本，不参与判定。
- 原文件 SHA256 在应用每批修改前检查，避免覆写 Claude Code 的并发修改。Claude 已确认暂不编辑本轮负责的文件。
- 没有修改冻结数据、活动清单、版本锁、原 Python/工具链目录权限，也没有执行训练。

## 已定位的进一步启动卡点

合法 SID 已能稳定取得（40 字节），原“Home stub／需要管理员”的判断已撤回。独立副本中的实际启动实验显示：

- 复制到 D:/code 临时目录的 Python 正常执行，普通模式能连接本机监听端口并读取合成哨兵文件。
- 相同可执行文件、cwd、env 去掉 SECURITY_CAPABILITIES 后正常启动；加上 AppContainer 属性时得到 WinError 2。
- 即便显式提供可执行路径与可写命令行缓冲，沙箱启动仍 WinError 2。
- GetAppContainerFolderPath 对同一合法 SID 返回 HRESULT 0x80070002；该容器配置尚不存在。

微软的[启动流程](https://learn.microsoft.com/en-us/windows/win32/secauthz/implementing-an-appcontainer)要求新容器先创建 profile；单独派生 SID 不会完成这个步骤。SID API 返回 HRESULT、系统分配的 SID 需要 FreeSid，见[官方 API 文档](https://learn.microsoft.com/en-us/windows/win32/api/userenv/nf-userenv-deriveappcontainersidfromappcontainername)。

本轮已加清晰的配置前置检查，不隐式创建用户 profile 存储。进一步启用需要准备实际容器配置，并验证网络、文件访问、进程树及完整渲染链路；当前 network_isolation=False、拒绝不可信执行的门禁保持有效。SID 契约测试通过不等于实际隔离通过。

所有本轮探针的 ACL 变更仅在独立副本 runtime/work 两个目录；本机监听端口有普通进程的连接对照，不访问外部网络。本轮没有创建 AppContainer profile、修改用户注册表或 C 盘配置。

## 证据

- [最终测试日志](/D:/Animation-Model-Training/reviews/codex-supervision/history-from-code/fix-2026-10-04/pytest-final.log)
- [真实 v2 状态输出](/D:/Animation-Model-Training/reviews/codex-supervision/history-from-code/fix-2026-10-04/status-v2.log)
- [原生启动探针](/D:/Animation-Model-Training/reviews/codex-supervision/history-from-code/fix-2026-10-04/appcontainer-native-probe.json)
- [普通／沙箱启动与配置查询对照](/D:/Animation-Model-Training/reviews/codex-supervision/history-from-code/fix-2026-10-04/appcontainer-launch-comparison.json)
- [探针脚本](/D:/Animation-Model-Training/reviews/codex-supervision/history-from-code/fix-2026-10-04/probe_appcontainer.py)

已通过 msg_272/274/275 向 Claude Code 协调范围和同步验证；本报告附最终结果供接续复验。
