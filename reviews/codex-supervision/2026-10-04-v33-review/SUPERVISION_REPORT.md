# Claude v3.3 持续监管

复核采样：2026-10-04T17:09:41.140414+08:00（北京时间）。HEAD：`76c44a377e8ec9f1b02f73bc7ef9903d40036a2f`。
文件验收 SHA：`953ec77c7347e40e17524ade2b2fe03b07ba7e262e6103ac9adb11382ceb98b2`；渲染工具 SHA：`797218030b0caa78f53761ad1e1aaf068de50548f16c4429547d8e1e1e37c816`。

## 结论

收到 Claude 的 msg_354 / 提交 76c44a3。原坏令牌输入的拒读 FAIL 已修，证据无法落盘时也不再允许 PASS；但**拒读原始泄漏证据的类型/多哈希处理仍未完整修复，终端与持久 JSON 的状态字段不一致**。本轮仍不通过原生文件验收审核，生产门禁 CLOSED。

11 个核心文件均与保存基线一致；进程采样只有两个 claude.exe，未见 Python/TeX/ffmpeg。未启动原生沙箱、修改真实 ACL、复制 MiKTeX 或新渲染。

## 独立复验：已确认进步

24/24 内置自检全持，正常模拟基线通过，前轮后核验异常保 FAIL/退出 1、拒写事实先行、预存目标跳过、自检先于授权、运行时/核心模块后核验关闭均保持。

v3.3 原 `token=['malformed']` 输入已返回 FAIL；结构化 data={} 但原始输出含匹配哨兵哈希时也返回 FAIL。主/兜底证据同时不可写时，模拟 PASS 降为 UNVERIFIED/退出 2、已测 FAIL 保持 FAIL/退出 1。

这些均为源码函数 AST 抽取、全内存文件/进程/ACL 替身，并非 AppContainer 原生验收。

## 待修一：拒读 FAIL 先于类型处理

原始沙箱输出明确含父进程哨兵的期望哈希，读取命令仅收到非秘密占位符。以下情况仍被降为 UNVERIFIED：

- parsed data 是非空 list/int/str：在 `(data or {}).get(...)` 处抛异常，尚未扫描 raw_out。
- content_hash 是 int/list：在 `.lower()` 处抛异常。
- parsed hash 为另一值：不再检查 raw_out 中的正确哨兵哈希。
- raw_out 先有另一个不匹配 hash、后有匹配哨兵 hash：re.search 仅取首项，漏掉后项。

已补 **12 种 parsed data × 是否先出现另一哈希 = 24 组** 完整回归矩阵，每组 raw_out 都含真实哨兵 hash，预期统一 FAIL。当前 **6/24** 保持 FAIL、其余 **18/24** 错误降为 UNVERIFIED。

修正方向：在解析任何数据类型前独立扫描原始输出的所有候选哈希，匹配哨兵即保存 raw/期望哈希并判 FAIL；再做类型明确的辅助解析。没有匹配泄漏而数据异常时，应 UNVERIFIED，不能伪 PASS。

`read-leak-type-sweep.json` 保存矩阵；`reproduce_file_v33.py` 一次可重放前轮输入、证据故障及完整矩阵。msg_356/357 已交付；msg_358 更正此前交接误写的矩阵数字为实际 6/24。

## 待修二：stdout 与持久 JSON 一致性

正常模拟 PASS 时，stdout JSON 有 `evidence_written` 实际路径和 `stdout_only=False`；保存的 JSON **没有这两字段**。原因是 `_write_json` 先序列化/写入，main 才添加字段。自检与错误落盘路径也采用相同顺序。

应在序列化/原子写入前构建状态；fallback 目标也须按实际位置写入一致字段。若所有目标不可写，stdout_only=True/UNVERIFIED（FAIL 仍保留）无需再尝试向不可写位置追写。具体 stdout/内存持久 JSON 都保存在 `file-v33-independent-results.json`。

runtime/core 清单已新增到最终 results，确认此项修订；不重复要求已关闭的核心后核验。

## 渲染与其他进程范围

媒体谓词已排除 partial 与 OtherScene，拒绝无正确文件头的伪媒体；独立 5 类输入均符合其已明确的 **header_only** 契约。仅有正确签名的截断文件仍可能通过，这是文件头检查本身的范围，现源码已如实标明未完整解码；不将其列为本轮新增阻断，也不把 header_only 当完整视频质量验收。

Claude 在 msg_354 说明先前 D:/Python 的 render_review.py 是 B5 Markdown→PDF 文档导出，不是 Manim 或隔离验收，已结束。项目内导出文件存在，未作 PDF 页面视觉验收；本轮未再进行文档导出。B5 题文与竖线格式已在上一轮确认，相关生成器本轮 SHA 未变，不重复测试。

## 材料与下一步

本轮证据：`snapshot/`、`status-snapshot.json`、`process-snapshot.json`、`reproduce_file_v33.py`、`file-v33-independent-results.json`、`read-leak-type-sweep.json`、`render-v33-independent-results.json`。

等待 Claude 按矩阵修正并回交最终 SHA；重点检查 24/24 原始泄漏输入统一保 FAIL、无泄漏异常统一关闭，以及终端/持久 JSON 一致后，再推进限定具名目录的原生文件验收。TeX/整套渲染及生产门禁不在该步骤中放行。
