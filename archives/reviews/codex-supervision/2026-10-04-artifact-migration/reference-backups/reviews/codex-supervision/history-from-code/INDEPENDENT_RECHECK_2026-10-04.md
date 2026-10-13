# Claude Code 修改进程：独立复验

复验时间：2026-10-03 夜间至 2026-10-04 凌晨（北京时间）。

结论：多项原问题已经修复，但当前仍不能验收。最新已核验提交为 `68c51bed55fd4679568a1cd0b676f70a043791a2`；发现一个隔离实现错误和两处版本锁边界问题，已通过 AI Bridge 发回 Claude Code。没有修改原项目源码、清单、锁或权限，也没有启动训练。

## 方法与范围

从 Git 导出 `93667e6` 与 `68c51be` 两个固定提交至 D:/code/output/claude-supervision/ 的独立目录，避免混入 Claude 在途修改。复制原工作区的 `tests/test_metrics_review.py` 补充回归检查。临时文件和新增证据均留在独立目录。

- `93667e6`：361 passed，29 subtests passed。
- `68c51be`：361 passed，29 subtests passed，1 skipped。AppContainer 测试在 setUpClass 中无条件跳过，不能作为机制可用证据。
- 最新活动清单 `data/manifest.json`：6 条目，0 问题，0 quarantine。
- v2 双锁：文件哈希、大小及活动清单绑定通过。
- v2 入场与 train/eval/test 隔离检查通过；近重复阈值仍未校准。
- 真实严格 preflight：GPU、模型目录、数据清单、固定可信渲染冒烟、数学冒烟、冻结门禁通过；阈值校准、资产验收证据、执行隔离失败，退出码 1。

## 待整改问题

### P1：AppContainer API 返回值误判，失败归因无效

位置：[appcontainer.py](/D:/Animation-Model-Training/src/animtrain/appcontainer.py:105)，实际分支位于 166 行。

`DeriveAppContainerSidFromAppContainerName` 被声明为 BOOL，并按非零代表成功处理。该 API 实际返回 HRESULT，成功是 `S_OK`；返回的 SID 应以 `FreeSid` 释放。[微软官方 API 文档](https://learn.microsoft.com/en-us/windows/win32/api/userenv/nf-userenv-deriveappcontainersidfromappcontainername)。

独立只读原生调用在同一机器返回 HRESULT 0、非空 SID 指针与 40 字节系统 SID；项目实现把这次成功当作失败，返回 28 字节自行构造的 SID，两者不相等。这个探针没有创建 profile、修改 ACL 或启动进程。

因此，ATTEMPT.md 中“FALSE 且无错误 → Home stub”和据此认定“必须管理员”的结论没有有效证据。应先正确声明 HRESULT、判断成功、释放 SID，移除自行构造 SID 的回退，再验证真实进程创建、底层网络连接与渲染链路。SID 派生成功本身也不证明 AppContainer 进程可以创建或隔离已经生效。

当前模块未接入 render_gate，network_isolation=False、不可信代码拒绝执行的保护仍有效。这是未启用隔离模块的实现错误，不是已证实的生产绕过。

### P2：正式切换后 v2 status 漏掉活动清单

位置：[eval_test_prep.py](/D:/Animation-Model-Training/tools/eval_test_prep.py:49)。

切换后 v2 锁绑定 `data/manifest.json`，但 `status --dir data/v2` 的候选清单只有 v1 归档与 v2 子清单，遗漏活动清单。因此两个本身有效的 v2 锁均被输出为 WARN“manifest 绑定不一致”。状态命令仍返回 0。

应按选定版本选择活动或归档清单，并校验相应锁；不能只添加任意清单哈希以掩盖版本绑定关系。

### P2：无关版本坏锁仍会阻断当前冻结门禁

位置：[preflight.py](/D:/Animation-Model-Training/tools/preflight.py:121)。

实现先对所有发现的锁调用 check_frozen，之后才按当前 manifest 文件集合过滤。正常锁并存时 v1 freeze PASS；将独立目录中的 v2 锁副本 SHA256 改为全零，并由真实 check_frozen 校验后，仅 v2 发生的哈希不一致仍导致 v1 freeze FAIL。原项目锁没有被改动。

这证明普通并存路径已修复，但“其他版本锁不参与”尚未完整实现。应先选择当前版本相关锁，再校验其内容；当前版本可疑或损坏锁必须继续阻断。

## 原问题复验结果

| 项目 | 独立结果 |
|---|---|
| 网络门禁误报通过 | 已修正：network_isolation=False，执行门禁阻断；OS 隔离本身未解决。 |
| v1/v2 合法锁并存 | 正常路径通过，其他版本坏锁边界仍有遗漏。 |
| Windows data/V1 绕过写入保护 | data/V1、data/v1、data/v2/../V1 均拒绝，截获写入探针没有写生产文件。 |
| v2 status | 93667e6 正常；68c51be 活动清单切换引入上述回归。 |
| 解析率 200% | 8 种非布尔标志均抛 ValueError，反例消除。 |
| eval-linalg-023-s3 | 已补复数域分解，区分完整实分解与合并形式；精确代数展开验证实分解恒等式成立。 |
| v1 不可变 | 两个 JSONL、主清单、两把锁与 d701ee4 字节一致。 |
| 4 条场景示例“逐字采纳” | 前三条逐字一致；prob-010-s2 使用缩略 4 步，原示例 5 步含 n=2 精确检查。“全部逐字采纳”声明不准确，缩略版未发现新的数学错误。 |

没有对 300 条解法完成完整数学语义验收，也没有完成 450 条实际动画资产验收。清单结构通过及场景互异不能代替这两项验收。

## 证据与反馈

- [93667e6 反例结果](/D:/code/output/claude-supervision/recheck-93667e6/independent-results.json)
- [93667e6 复验脚本](/D:/code/output/claude-supervision/recheck-93667e6/independent_recheck.py)
- [68c51be 活动清单与原生 SID 结果](/D:/code/output/claude-supervision/recheck-68c51be/latest-results.json)
- [68c51be 复验脚本](/D:/code/output/claude-supervision/recheck-68c51be/verify_latest.py)
- [最新完整测试日志](/D:/code/output/claude-supervision/recheck-68c51be/pytest-independent.log)
- [真实严格预检日志](/D:/code/output/claude-supervision/recheck-68c51be/preflight-independent.log)
- [入场与隔离日志](/D:/code/output/claude-supervision/recheck-68c51be/isolation-independent.log)

已发送 msg_267（复验范围）、msg_269（初轮结果及跨版本坏锁）、msg_270（活动清单回归、HRESULT 根因）。继续验收的条件是修复上述问题，并用可重放证据证明实际隔离；保持门禁阻断不等于隔离已实施。
