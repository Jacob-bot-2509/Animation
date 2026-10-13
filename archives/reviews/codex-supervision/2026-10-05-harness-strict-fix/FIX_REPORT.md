# Harness 与 PDF / 补丁发布链修复报告

完成时间：2026-10-06T00:43:12.615814+08:00。当前提交：`2feffe1e52169abc3e0d52683d1189150005e219`。本轮复现的代码缺陷已修复并验证，76 项相关测试通过；本轮改动在工作区，未创建提交。正式训练仍受现有数据与真实验收证据门禁限制。

## 代码修复

| 环节 | 修复结果 |
| --- | --- |
| MathJax | 按真实 title、inline/display 容器和公式数量判断完成；拒绝脚本伪标记、真实错误节点、SVG 红色 mtext 未知命令、未排版公式与重复容器。 |
| PDF 发布 | 浏览器/打印进程非零退出明确失败；唯一新 PDF 目标、禁止覆盖和复用旧文件；pdfinfo 验证实际页树；收据绑定源 MD、静态 HTML、PDF、渲染器及守卫哈希。 |
| 打印兼容 | 保留 Claude 的用户临时目录打印改动，新增独占本机 loopback CDP 流备用打印；隐藏浏览器、私有 profile，只清理本次进程。CLI 临时目录打印及 CDP 直写项目 D 盘均真实通过。 |
| 内容与排版 | 报告与选中 JSONL 的题号、顺序、题干、推导、答案、场景全文逐项一致；题数/步骤动态汇总；长公式限定宽度并换行，标题/标签与后文保持。 |
| 补丁发布 | 通用新版本发布器校验源文件双哈希、原记录排序 SHA、新数学内容 SHA；全部批次先验证，再独占写入、校验选择器稳定性并原子切换；历史 v5/v6 入口停止复演。 |
| 训练轮次 | run_id 与配置、manifest、训练 manifest、adapter 文件树、生成结果全部绑定；按真实 eval/test 题数校验 VERIFIED 状态、精确分数及分项/汇总一致性；配置相对路径按项目根解析。 |
| 失败与隔离 | 超时/读取/写入错误返回非零并尽可能留存证据；阶段间检查停止信号；未知 M/F 保持未知；队列仅存 ID/原因，文档中的评测失败题回填训练指引已纠正。 |
| 执行接线 | 未评审、未接线的 executor/judge 不直接运行，保持 UNVERIFIED，不能凭状态字符串或汇总率伪造真实验收。 |

新增 `tools/review_guard.py`、`tools/edge_print.py`、`tools/publish_row_patches.py`、`tests/test_review_harness_guards.py`。完整 13 个修改文件及 raw SHA-256 在 `after-final-source-and-preservation.json`，源码快照在 `after-final/`。其他工作区改动均保留。

## 验证与证据

| 验证 | 结果 | 证据 |
| --- | --- | --- |
| 守卫、发布、轮次正反测试 | 38 项通过；两条浏览器非零退出问题先复现后修复 | `test_review_harness_guards.py.delivery.log`、`nonzero-browser-exit-reproduction.log` |
| readiness / 哈希既有回归 | 20 + 18 项通过，涉及源文件随后未改变 | `test_training_readiness_fixes.py.release.log`、`test_draft_hashes.py.release.log` |
| 真实选中版本 CLI 审核 | 18 批、264 题、1176 步；hard=0、V007=0、V011=0，哈希检查未跳过 | `selected-v6-audit/summary.json`、`selected-v6-audit-cli.txt` |
| 伪造 SHA 负例 | 返回码 2，V007=1、hard=1；真实选择器不变 | `strict-audit-negative-result.json` |
| 示例训练入口真实调用 | 返回码 2，要求已确认参数哈希，未新增运行产物 | `real-harness-cli.json` |
| CDP 实际传输打印 | 全量 8316 公式静态页成功打印 103 页；旧排版传输夹具，不作为交付文档 | `cdp-probe/result.json` |
| 历史/数据保护复验 | 12219 个保护文件漂移 0；18 个选中 JSONL 原字节不变；选择器不变 | `after-final-source-and-preservation.json` |
| 最终 PDF | 138 页，8316 数学容器；264 题号及顺序匹配源文；全部页面渲染并审视，9 个关键页面放大检查 | `pdf-qa-v5/qa-evidence.json`、`pdf-qa-v5/visual-review.json` |

264 题的数学字段摘要全部复核，七条既有补丁字段逐项匹配。题目精确数学内容保持原样，分数、根号、极限未改为近似小数。这里的内容绑定及排版验证不替代先前各批独立数学推演和真实动画验收。

## 最终文档

交付：`pdf-v5/draft-review-harness-v1.pdf`。

PDF raw SHA-256：`afb37559878033cbbe7e38f55a84532b83e464e455a4d811fb391c5ecbc80a23`。

渲染器 raw SHA-256：`6bf998cd605778d54012b496147826b28206c9e2853d9e5bfe975554026b2d27`；守卫 raw SHA-256：`759a0f05e0ae818ac5f6805930c3cd29666269c06cc601a5f3a64d7ade64306d`。

完整收据：`pdf-v5/draft-review-harness-v1.render.json`。源文：`draft-review-harness-v1.md`。先前 103 页、137 页及本轮中间版本均保留，只有此 138 页版本是本次最终文档。

## 发布与训练边界

严格发布器以后只用于新版本：

```text
python tools/publish_row_patches.py --drafts <草稿目录> --patches <补丁文件> --version <新版本>
```

本轮只在隔离夹具运行发布器；实际选中的 v4-final/v6 JSONL、报告及选择器未修改。校验错误发生在首个输出前；真实文件系统写入若在中途失败，可能留下未被选择器选中的新文件，须检查这些孤立文件并保持失败状态，不能当作成功版本。旧版本不被覆盖。

严格草稿审核通过不等于准入：当前 264 题仍 quarantine，许可为内部研究、动画尚未真实验收，admitted/render_verified 均为 0。训练未实际运行，参数仍为提案；真实逐题执行、渲染、judge 协议与证据未接线，R/E/M/F 未验收时保持未知。

正式训练池仍有两对结构泄漏候选：`linalg-048 ↔ eval-linalg-015-s1`（31/75）、`linalg-048 ↔ test-linalg-025`（29/82）。按用户规则，同一解题结构即使更换数值或文本相似度低也需隔离。相关正式数据与证据保持原样，门禁未放行。

## Claude 动态与持续记录

保留 Claude 提交 `784ef85` 的临时目录打印修复；本轮 CDP 直写项目 D 盘成功，不能概括为所有 D 盘打印都不可用。Claude 最新提交 `2feffe1` 新增独立泄漏留出集构建器和评分器，不修改本轮负责的 13 个源文件；该新增工具不包含在本报告的 76 项验收范围。

旧观察器 PID 12024 已退出且无 STOP，原快照/事件已存 `watcher-before-restart/`；只读监听已恢复，启动器 PID 42564，实际工作 PID 28352。最新快照存 `watcher-fresh-snapshot.json`。监听只记录进程、提交与文件改变，会话结束后不会自行做 AI 审查或训练准入。

正式交接回执存 `bridge-handoff-final.json`；交付清单及 raw SHA-256 存 `delivery-manifest.json`。
