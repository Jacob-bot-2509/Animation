> 最新协助复验：预检证据绑定和组合屏候选筛选已修正，113 项测试、22 个子测试通过。组合屏仍未校准，5 道题的 15 条候选待继续处理。见 [交接报告](../2026-10-04-preflight-binding-fix/FIX_REPORT.md)。下文为原时点记录。

> 后续：B5已切换用户裁决后的v3规则，本报告保留历史版本结论。最新协助修复见 [B5 v3交接](../2026-10-04-b5-v3-assist/FIX_REPORT.md)。

> 后续修复已完成：执行入口与精确分数报告已修正，11项前后清单补齐；独立文件四对照通过，生产门禁仍CLOSED。详见 [协助修复报告](../2026-10-04-assisted-fix/FIX_REPORT.md)。下文保留20:49历史检查结论。

# Claude 修改独立检查报告

检查时间：2026-10-04T20:49:10.866328+08:00（北京时间）。审查提交 `d718f941e8837df78ecd0d295c3883078f1e05dc`，以及 `7635586` 新增执行入口；验收源仍为 v3.8，SHA `8d8902d92ca8b700cd14182190709314834aeff05b457dea4ced5034ab488a71`。

结论：B5 自匹配污染已修复，新计数与未校准结论成立；执行入口尚有参数缺陷；文件原生验收仍 UNVERIFIED，生产门禁 CLOSED。

## 需要继续修正的内容

1. **P2：执行入口污染目标脚本参数。** `tools/runpy.py:33` 调用 `run_path` 前未移除包装器的位置参数。目标脚本收到 `[目标路径, 目标路径]`。同一 argparse 探针直接执行 rc=0，经包装器 rc=2，错误为 unrecognized arguments。会阻断通过新入口执行的 argparse 工具。另 `:35` 用 int 转换 `SystemExit('文本')` 导致二次 ValueError。应暂存 argv、设 `[目标路径]`、执行后恢复，并正常处理字符串退出。详见 `runpy-argparse-result.json`、`runpy-argv-result.json`、`runpy-exitstr-result.json`。已发 Claude msg_376。
2. **P2：文件拒绝证据仍缺明确错误归因。** run `a41cc68655fd` 的授权读/写均 PASS；拒绝读/写返回 `outcome=denied`，但 `winerror=null`。脚本 `file_acceptance.py:368` 把所有 OSError 归为 denied，仅取 winerror，未记录 errno/异常类型。必须保留 UNVERIFIED；不可用未创建文件/未观察到泄漏替代明确权限错误。已发 msg_375 要求补录异常及同路径、同操作的真实 Win32 诊断，再复验新源码，不凭猜测映射 ERROR_ACCESS_DENIED。
3. **P2：11 项前后哈希的回执与原始证据不一致。** msg_373 声称核心 11 项前后哈希已入证据，但 JSON 的 `core_manifest_before` 与 `post_verify.core_modules_before/after` 只有 3 个核心模块。当前独立核对 11 项均与批准基线相同，不能据此补造运行前的历史证据。已要求回交额外原始清单及父进程 rc=2 运行记录；rc=2 目前依据 Bridge 回执，8 个子进程 rc=0 可在 JSON 直接核对。
4. **P2：报告未按要求使用精确分数。** `b5_calibrate.py:31` 指标舍入；MD/PDF 的网格、目标与 Jaccard 均以小数展示，未含显式精确比值；零预测时 PDF 显示 Python `None`。应从计数及 shingle 交并数输出分数，precision 分母为零时显示“未定义”。当前网格计数正确，表示方式待修。未选阈值的 calibration 对象仍用 threshold=0 和四项计数全0作为占位，建议改 null/明确“无选定阈值”，避免读成48对全零。已发 msg_375/376。

## B5 已确认修复

- 48 个有效标注对：重复11、不重复37；2个不确定排除；与 f5e4271 用户标签语义一致。字节差异仅 Git LF 与工作树 CRLF。
- 从完整题文独立规范化并生成5字符集合，以交集/并集的 Fraction 重算50个 Jaccard，保存值全部与其四位舍入一致。11行 TP/FP/FN/TN 与独立精确评估全部相符。
- 在审查目录输出重新执行快照脚本，rc=0，JSON 与待审报告逐字段一致；没有覆盖原报告或标签。
- 遍历[0,1]所有相似度分界及相邻区间分类：该48对样本上没有阈值同时满足召回率≥19/20、误报率≤1/100。结论仅针对该样本；其分层抽样不能直接推断总体性能。

| 阈值 | TP | FP | FN | TN | 精确率 | 召回率 | 误报率 |
|---|---|---|---|---|---|---|---|
| 3/10 | 11 | 15 | 0 | 22 | 11/26 | 1 | 15/37 |
| 9/20 | 11 | 14 | 0 | 23 | 11/25 | 1 | 14/37 |
| 1/2 | 9 | 3 | 2 | 34 | 3/4 | 9/11 | 3/37 |
| 7/10 | 1 | 0 | 10 | 37 | 1 | 1/11 | 0 |

PDF 为3页。已逐页渲染并目视检查：完整题文及数学公式恢复，未见截断导致的公式残缺；网格与JSON一致。标签列过窄逐字换行，页眉仍为 MJDONE，属于版面收尾项；小数和 None 是明确待修项。检查未编辑或重导出源 PDF。

## 原生文件证据复核

- 原始 JSON SHA `6d017f7fac2a728d516eddfbcac84195d9aff394aa0764c32bdc36bdece0b432`。源脚本是获准的 v3.8，证据位置与 evidence_written 一致，stdout_only=false；24项内置回归 holds=true。
- 4场景的8条控制/沙箱原始 JSON 均与已解析字段一致，spawned=true、无超时、rc=0。沙箱令牌 AppContainer=true、SID匹配、capability=0；控制端非 AppContainer。实际客户端和 exe 哈希一致，site_absent=true。
- 当前授权写目标文件字节哈希正确，授权读目标/拒读哨兵哈希与运行前后记录一致；拒写沙箱目标不存在。拒读 raw_out 未包含哨兵内容哈希。上述事实不能单独证明整个文件系统隔离。
- 当前ACL：具名 work 含该 AppContainer SID读写ACE；runtime含读/执行ACE；denied目录未授予该SID。当前4项runtime文件与记录相符，核心11项与批准基线均一致。原始 JSON 的3项运行前后核心哈希均相同。
- 未重新运行原生验收；未扩大ACL、修改核心/门禁/防火墙或启动TeX/渲染。

## 监管监听恢复与边界

旧监听 PID50932 已不存在，最后心跳18:14:31；没有正常停止记录或错误日志，退出原因未知。20:43:13恢复隐藏后台监听，实际观察器 PID13204（启动器PID42116）。停顿证据与旧日志已保留，不能声称空窗内持续监控。新观察器加入 B5 脚本、报告和PDF哈希监测。

收尾心跳：2026-10-04T20:49:10.723328+08:00；核心偏离为空。监听只记录，不会在会话结束后自动做模型审查或放行；进程存在不能证明任务正在计算或卡死。

## 复验材料

`snapshot-manifest.json` 与 `snapshot/`：源代码、标注、JSON、MD、PDF、原生验收原始证据快照。

`b5-independent-results.json`：精确 Jaccard、全部网格、完整阈值分类及标签完整性；`b5-v2-rerun/`：隔离复跑。

`native-independent-results.json`：原始输出、文件哈希、令牌、runtime与核心11项独立核对；`current-acl.json`：只读ACL记录。

`runpy-*-result.json` 与 `probe-*.py`：执行入口实际回归；`before-restart-*`、`watcher-recovery.json`：监听空窗/恢复证据。

`closing-status.json`：收尾HEAD、心跳和相对审查快照的变更。若随后源码变化，本报告仅覆盖上述快照版本，需要再次复验。
