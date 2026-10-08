# Claude v3.2 监督与独立复验

采样时间：2026-10-04T17:01:54.323837+08:00（北京时间）。HEAD：`2a93ab2294b2f98756c36483e5d1c82033019f7e`。
文件验收脚本 SHA：`769045a97ab4f2160bb8cee1e282dcfea2017439b2af2a404cec1502bc260f8e`。本轮主要回执：AI Bridge msg_348、349、350。

## 当前结论

Claude 已回交 v3.2。前轮异常路径缺陷大多已得到独立确认，**尚有一个主要阻断：拒读已返回匹配哨兵的哈希时，坏令牌字段仍会抹掉 FAIL**。尚不批准原生文件验收；生产门禁保持 CLOSED。

本轮未启动 AppContainer、修改真实 ACL、复制工具链或执行新 Manim 渲染。11 个核心/门禁文件均与迁移后受监控基线一致。已只读独立保存四文件运行时源/副本 SHA，全部匹配，见 `independent-runtime-manifest.json`。

## 已独立确认修好

同一源码快照的内存替身复验中，24/24 内置回归自检持有预期，正常场景模拟通过。以下前轮问题已关闭：

- case 已判 FAIL，随后后核验抛 PermissionError：保留 FAIL，退出 1。
- 拒写目标已被创建，客户端返回 data=[]：仍依文件事实判 FAIL。
- 正写目标已存在：返回 skipped，不运行该步骤控制或沙箱客户端。
- 证据目录不可写：结构化 stdout 报 ERROR/UNVERIFIED，受控退出 2。
- 主/兜底证据同时不可写：不再裸异常；已判 FAIL 的退出码仍为 1。
- 核心模块在 case 期间变更：后核验 UNVERIFIED，退出 2。
- 读目标变更、自检失败无 ACL/case、运行时变更失败关闭、后续场景异常不覆盖早先 FAIL，均保持前轮修复。

这些是函数的纯 AST 抽取与全内存故障注入，**不是原生沙箱验收**。可重放 `reproduce_file_v32.py`，原始记录见 `file-v32-independent-results.json`。

## 主要阻断：拒读 FAIL 优先级

模拟拒读沙箱确实读取哨兵文件并输出：`outcome='read'`、`content_hash` 等于父进程生成哨兵的期望 SHA；读取命令仅收到非秘密占位符。随后返回的 `token=['malformed']` 导致 `_run_denied_read` 在 `tok4.get(...)` 处抛异常。

现有 `_case` 只保存 exception，把该场景及整体标为 UNVERIFIED。已匹配哨兵的泄漏证据没有被先行保存和判为 FAIL；它应像 v3.2 拒写文件事实一样先处理，再验证令牌。新增 `read-leak-priority-proof.json` 保留期望哈希和模拟沙箱完整观测，明确该输入的预期为 FAIL。

已发 msg_352 要求 Claude 对称修复。此项不能由 24 项内置自检通过替代。

## 证据持久化状态

模拟场景 PASS 且主/兜底均不可写时，当前仍 JSON PASS、退出 0；stdout 含观测，stderr 说明写入失败。脚本没有在 JSON 中给出实际 evidence_path / stdout_only / 写入状态。因此应明确契约：若允许 stdout 作证据，明确状态；若必须持久证据，写入失败应 UNVERIFIED/退出 2。不要把未保存状态描述为已落盘。此项已随 msg_352 反馈，不将 stdout 本身视为无证据。

四文件 runtime manifest 尚未由该脚本直接保存。本轮监督方补存了独立清单，供稳定版本复验与之后的原生运行记录绑定。

## 渲染与标注

渲染 `e355c96068b68d8e66ef395c680d37c75ea29dcfc710c49fb1aea0a24a62ad02`：已独立确认拒绝 `partial_movie_files` 和没有正确文件头的伪 PNG/MP4。既有 PNG10/MP48 报告产物按新文件头谓词均正常。

现实现仅验证文件头：8 字节 PNG 签名、12 字节 ftyp 截断文件及其他场景目录的 MP4 仍可通过谓词。它不能证明文件完整可解码，也未严格限定 PilotScene 最终路径。这是**能力边界/改进项**，不推翻此前真实产物 SHA 核对；可显式标记 header_only，或进一步实现精确路径及完整性检查。已发 msg_353。

B5：50/50 完整题文及相似度与源数据一致；第 45/49 对竖线已在 Markdown 中转义，表格无列错位；JSON 保留 2 对原始竖线。此前表格缺陷已关闭，不添加人工标签。

Claude 在 msg_349/350 说明普通环境试点来自用户“先数据线和渲染线开工”的授权，使用项目 venv 与 C 盘用户 MiKTeX，报告输出在项目 `.render-pilot`；记录为 Claude 提供的交接说明，未把它当成沙箱验收。Claude 已承诺暂停新原生/复制/ACL/渲染等待边界收口。

首采样另外见 `D:/Python/python.exe tools/render_review.py ...` 的 B5 PDF 导出，后采样已无 Python/TeX/ffmpeg。项目内 HTML/PDF 文件存在；尚未对 PDF 页面作视觉验收。该进程是文档导出，不作为先前 Manim 残留。msg_351 已询问 Claude 说明。

## 本轮证据与交接

稳定源码在 `snapshot/`；`status-snapshot.json`、`process-snapshot.json` 保留采样；`read-leak-priority-proof.json`、`file-v32-independent-results.json`、`render-v32-independent-results.json`、`b5-v32-independent-results.json`、`independent-runtime-manifest.json` 提供复验。

msg_351 确认回交并询问文档导出；msg_352 交付拒读 FAIL 复现与持久状态反馈；msg_353 关闭标注表和中间片段缺陷，澄清文件头判定边界。待回交新稳定 SHA，重点重放拒读 FAIL 输入。
