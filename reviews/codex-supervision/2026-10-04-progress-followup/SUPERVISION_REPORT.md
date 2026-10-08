# 持续监督与独立复验

采样：2026-10-04T16:41:48.079778+08:00（北京时间）。最新提交：`2671938c8ad0f08553d64029ab0253e5ccbebb12`。
本轮文件验收 v3 字节 SHA：`d569e0829ce916c0ceaf54cdf265bc185b220f7a5dee2ea2790f0e612980beae`。

## 结论

Claude 已从 v2.1 推进到 v3，修订已提交；多项前轮缺陷得到独立复验确认，但**仍不通过原生文件验收审核，生产门禁维持 CLOSED**。本轮没有运行原生沙箱、修改真实 ACL、复制 MiKTeX 或启动新渲染。

核心/门禁 11 文件均与迁移后的保存基线一致。16:36 首次采样观察到普通环境 MP4 渲染进程；后续采样已只见两个 claude.exe。已询问 Claude 该流程授权来源、环境/TeX 来源与缓存边界，尚未收到书面回应，不推断其是否另有用户授权。

## 文件验收 v3：已修与未修

独立抽取稳定源码函数，使用全内存文件系统、模拟 UUID、ACL 和进程。自带 **20 个负例 + 4 个正例，共 24/24** 满足预期；正常模拟基线通过。这是代码判定复验，不是 AppContainer 原生验收。

| 上轮缺陷 | v3 独立结果 |
|---|---|
| 读文件前后变更仍通过 | 已改为 UNVERIFIED |
| 预存写目标被当成新写入 | 不再通过；但仍执行写操作，尚须前置阻止 |
| 自检失败仍授权和执行，JSON/退出码冲突 | 已修：无模拟 grant/case，UNVERIFIED/退出 2 |
| runtime/._pth/脚本变更仍通过 | 已修：检测变更，退出 2 |
| 已判拒写 FAIL 后另一场景报错 | 已修：保留先前 FAIL 与对应原始记录 |
| 证据初始化/错误处理完整性 | 部分修订，仍有异常路径缺口 |

新增故障注入确认：

1. **确证 FAIL 被 main 覆盖**：case 已 FAIL，后核验模拟 `python313._pth` 读取 PermissionError，main 将 overall 改为 UNVERIFIED、退出 2。应保留 FAIL、退出 1，并附 ERROR 原因。
2. **同一场景内文件事实丢失**：拒写场景已模拟创建未授权文件，但返回 `data=[]`；后续 `.get` 解析报错，仅存 exception，整体 UNVERIFIED。需要先保存独立文件事实与原始输出，再解析；不能依赖成功解析才能判击穿。
3. **证据路径错误未闭合**：EVIDENCE.mkdir 不可写时仍在 try 外抛异常；主证据与 fallback 同时不可写时同样裸异常。两项模拟均无结构化 stdout/JSON 完整输出。若确实无可写位置，至少保留结构化 stdout 与受控退出，不能要求物理上不可能的落盘。
4. **前置条件未阻止操作**：sb_pre_exists=True 已参与判定，但 `_run_granted_write` 仍无条件调用 control/sandbox 写入；应先拒绝该步骤。
5. **完整性证据仍有边界**：后核验未包含三个核心模块；四个 runtime 文件比较清单没有落入最终证据，也未绑定已有复验基线。需保存完整前/后清单及依据。

可重放脚本：`reproduce_file_v3.py`；原始结果：`file-v3-independent-results.json`。不需启动真实验收。以上已发 AI Bridge msg_347，要求回交稳定 SHA 后重验。

## 渲染：覆盖进步已核实，判定仍有遗漏

已只读逐项核验新报告：

- `.render-pilot/0f77391281`：PNG **10/10**，覆盖 8 类模板。
- `.render-pilot/9658702839`：MP4 **8/8**，每条一个最终 MP4，覆盖 8 类模板。

所列媒体实际字节数和 SHA 全吻合，场景源码实际文件字节 SHA 也吻合，已消除旧版字符串/LF 与实际 CRLF 文件的哈希口径差异。未做完整解码、画面质量或数学/scene_spec 语义验收；以上为普通环境产物核验，不能替代沙箱验收。

新逻辑已拒绝 rc=0 且 media=[]、零字节、错误格式、只有 TeX 缓存四类输入。但模拟仅有 `partial_movie_files/PilotScene/123.mp4` 时，`_has_artifact` 仍返回 True，将中间片段当作最终产物。须限定最终路径，并建立与“可验证”表述相称的格式验证。真实新报告恰有最终文件，不能据此忽略该判定缺口。已发 msg_345。

## B5 标注集与文档

50 对候选的 **完整题文 50/50、重算相似度 50/50** 均与源数据吻合；11 对长题截断缺陷已修。仍无人工标签，不自动填入。

Markdown 第 45、49 对的概率公式含未转义的 `|`，会把表格拆成额外列（文件第 52、56 行各含 8 个管线分隔，结构应为 6 个）。已要求 Claude 在生成器中只对 Markdown 单元格转义竖线，JSON 原文保持完整。

训练提示词已修正“单反斜杠总导致 JSON 解析失败”的表述，要求解析后语义检查；≥95% 明确为目标，尚无新达标测量。文档计划不等于验证器已实现。

MiKTeX 方案已到 v3：目标改为项目内 `.sandbox-runtime/miktex-real`、全量文件 SHA、显式 `/XJ`。这三项反馈已落实；依赖根、禁自动安装参数、输出/缓存边界、自持性仍未实测。未执行复制。

## 交接与材料

msg_344：询问新渲染的授权/环境边界；msg_345：交付中间片段及标注表格缺陷；msg_346：确认新提交和真实八模板覆盖；msg_347：交付 v3 异常路径复现。目前未收到这些交接的正式回执。

证据：`snapshot/`、`status-snapshot.json`、`final-status.json`、`process-snapshot.json`、`file_acceptance-v3-snapshot.py`、`reproduce_file_v3.py`、`file-v3-independent-results.json`、`render-independent-checks.json`、`latest-render-verification.json`、`b5-independent-checks.json`。
