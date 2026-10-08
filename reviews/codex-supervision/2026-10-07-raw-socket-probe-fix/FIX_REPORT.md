# 裸 socket 探针模板修复

Claude 的 msg_689 提交两轮失败：lan-2026-10-07-a、v6-2026-10-07-a。宿主健康对照有结果，但沙箱探针在发包前因裸 _socket.socket 缺少上下文管理协议而退出，rc=1。Codex 在本机原模板中独立复现同一 TypeError。该模板属于我此前的代码；现已直接修复。

生成的探针使用显式创建与 try/finally 关闭，保留原来的裸 _socket 路径。构造失败时不访问未初始化句柄；settimeout、连接、发送、超时和拒绝路径均关闭已创建的 socket。关闭本身失败会单独保留 close_error 并将 outcome 设为 error，不能把清理失败当作网络隔离拒绝证据。原判定、接收器归因和生产门未放宽。

旧测试的 MagicMock 错误地提供 __enter__，掩盖了实际运行缺陷。替身现按裸 socket 接口约束，无上下文协议，并检查 close 被调用。新增真实 IPv4 与 IPv6 回环中 TCP/UDP 的准确 nonce 送达、真实裸 socket 句柄关闭，以及构造失败后下一协议继续、设置超时失败清理和关闭拒绝不能通过等回归。

| 验证 | 结果 |
|---|---|
| 原模板本机复现 | TypeError，发包前失败 |
| 驱动对应回归 | 30 PASS |
| 完整表面证据 / IPv4 联合策略 / 接收器相关回归 | 48 PASS，无跳过 |
| 合计 | 78 项本机回归通过 |
| 原两轮失败原件 | 2 件 sender.json 哈希不变 |
| 外部 / LAN 新沙箱双端结果 | 本轮未执行，待提交原件 |
| 修复后工具资格 | PASS_LOCAL_DRIVER_REPAIR |
| 原生隔离资格 | UNVERIFIED |
| 生产 | CLOSED |

当前驱动 tools/sandbox_external_test_driver.py 原始 SHA-256：

99324c8a5343ab1379f290f1c9b2b46f70ae13e3a3f346e23249f6c1bc236292

对应测试 SHA-256：

89af7528c188b17c191a4950e94a9cf501ba6d49f3796ba1aa52c50f26f41723

源码变更前后哈希在 source-change-bindings.json；before/ 和 final-source/ 分别保留完整源码，source-changes.diff 仅展示本轮差异。reproduction.json 与 failed-originals/ 保留两轮失败回执及本机复现。driver-regression.json、regression.txt、related-regression.json 和 related-regression.txt 保存实际回归依据。

已通过 msg_692 将修复和最终源码 SHA 交回 Claude Code。后续重跑需新轮次与重新生成的 scene.py，并提交独立完整 receiver JSONL、summary 和实际 rc；保留旧失败文件。旧监听日志若含旧 nonce，会被现有严格归因规则拒绝，不能裁剪历史日志冒充新完整接收会话。重跑依用户最新实验安排，本轮没有连接外部节点或启动沙箱实验。

本机代码修复通过不构成原生双端隔离通过。收到新材料后仍需按实际版本、四个健康对照、沙箱尝试、接收器观察窗、源哈希与原始退出码独立核验，再判定并归档。核心题库的 761 条数学/场景文字通过、完整语义隔离尚未建立等状态仍以 continuous-math-review/current-core/FIX_REPORT.md 为准；本次驱动修复不改变其冻结归档。

最终交付原件由本目录 delivery-manifest.json 绑定。
