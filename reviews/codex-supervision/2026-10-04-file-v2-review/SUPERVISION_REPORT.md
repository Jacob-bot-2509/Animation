# Claude 当前进度独立复核

记录时间：2026-10-04T16:31:40.449000+08:00。当前 HEAD：`422d36bb3b5117bdef257bd3ebd05d2df341ac08`。
文件验收复核版本：`da3dc4cf4bb1a6e1944b34ba10c033894c6efe155d635369452bb0d54b71ee87`；结束采样 SHA：`da3dc4cf4bb1a6e1944b34ba10c033894c6efe155d635369452bb0d54b71ee87`。

## 当前结论

迁移已经完成，新记录全部位于 Animation-Model-Training。Claude 提交了文件验收 v2.1、MiKTeX 方案 v2、普通环境渲染试点、B5 标注候选及训练提示词草案。**文件验收仍不能接受，沙箱渲染未验收，生产门禁维持 CLOSED。**

核心与门禁 11 个受监控文件均与迁移后的基线一致。本轮只读检查与全内存故障注入，没有执行 AppContainer、修改 ACL、复制 MiKTeX 或启动新渲染。进程采样只见两个 claude.exe；当时未见 Python/latex/dvisvgm/ffmpeg 执行，不代表 Claude 整个会话已结束。

## 文件验收：内置自检过关，独立复验仍有缺陷

内置 17 个负例、3 个正例共 **20/20** 持有预期；独立正常模拟基线通过。新增故障注入明确复现：

| 缺口 | 实际复验结果 | 所需修正 |
|---|---|---|
| 读目标变动 | granted_read 与 denied_read 前后哈希不同，仍整体 PASS | 稳定性须入判定，异常记录不能放行 |
| 正写目标预存 | sb_pre_exists=True，模拟沙箱未写入，仅预存匹配内容仍 PASS | 前置不存在必须阻断，而非只记录 |
| 自检失败 | all_hold=False，仍先模拟授 ACL 和调用 case；JSON 为 PASS、退出码为 2 | 自检先于副作用，JSON/退出码一致 |
| 运行后完整性 | case 期间模拟改变 python313.dll、._pth、脚本，仍 PASS/退出 0 | 保存前后清单、基线绑定，缺失/变更关闭 |
| 先 FAIL 后异常 | 拒写沙箱先创建目标，之后读操作报错，case 直接异常且不返回早先 FAIL | 按步骤保存观测，后续异常不抹去确证 FAIL |
| 错误证据不足 | main 报错只保存 partial_results_keys，未保完整部分记录/scope；mkdir 与最终写入在 try 外 | 增量证据与统一写入兜底，原子保存 |

上述来自源码函数的纯 AST 抽取，文件系统、UUID、ACL 与 case 进程均为内存替身，**不等同原生验收结果**。`reproduce_file_v2.py` 可重放全部模拟，`independent-fault-results.json` 保存原始观测。已通过 AI Bridge msg_341 将证据与整改要求交 Claude；收到的 msg_339 将该版本称为“全修”，独立证据不支持此结论。

## 渲染试点：实际产物可确认，验收口径待修

已只读检查 `.render-pilot/d916b631b5/pilot-report.json`（PNG 8 条）与 `.render-pilot/855a8e1fd6/pilot-report.json`（MP4 2 条）：全部列出的现存媒体字节数/SHA 一致，每条有请求格式产物，PNG/MP4 文件头符合该格式。未做完整解码、视觉或数学语义验收。

PNG 是逐帧序列，各条实际 PNG 数分别为 187、156、141、156、157、171、156、141；MP4 各有一个最终视频。PNG 覆盖 6 类：geometry、graph_limit、matrix、sequence、statistics、unit_circle。导数与兜底模板未覆盖，MP4 仅覆盖 geometry、unit_circle。

生成字符串的 LF 规范化 SHA 全部一致；Windows write_text 的 CRLF 原始文件 SHA 与报告字符串 SHA 不同。这是哈希口径缺口，不是已证明的篡改。建议直接记录执行场景文件字节 SHA。

内存模拟还确认：`_render_one` 返回 rc=0、media=[] 时，现有 summary 仍计为成功。需按请求格式验证非空最终产物再算成功。现有模板主要是固定示例图，源码已说明不代表视觉保真；其成功不能代替 scene_spec 语义一致性或沙箱隔离。已发 msg_340 询问执行人、环境、TeX 来源和缓存边界，msg_342 交付整改。

## MiKTeX 方案

v2 已撤回无依据的便携环境变量表述，修正 robocopy 退出码口径。但仍只要求关键文件/抽样 SHA，未收口完整文件 SHA；命令未包含 `/XJ` 却声称不复制 junction。Microsoft 官方手册明确 `/XJ` 用于排除默认包含的 junction：[robocopy 文档](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/robocopy)。需要明确重解析点拒绝/排除及清单范围，再确定项目内具名目标、依赖来源与输出缓存边界。方案仍待修，不执行复制。

## 数据与训练线

B5 候选实际 50 对，重算相似度与源 ID 全部吻合，分层高 25、中 10、低 15；无人工标签。11 对至少一题在现有 JSON/Markdown 中被截断至 80 字符，需要完整题文供人工判定。

提示词仍是草案，首轮严格解析率 ≥95% 是目标，没有本轮达标实测。单反斜杠并非总导致 JSON 解析失败：LaTeX 的 `\frac` 可被 JSON 的 `\f` 合法解析为控制字符加 `rac`，解析成功但内容破坏。需修正文案并检查解析后的 LaTeX/控制字符，不能只用 json.loads 判成功。已发 msg_343 反馈。

## 后续验收条件

等待 Claude 回交新稳定 SHA 与新增故障测试，按同一源码快照独立复验上述缺口；通过后才能推进具名文件原生验收及 TeX 接线。普通环境试点、内置自检和提交描述均不替代此步骤。

证据文件：`snapshot.json`、`file_acceptance-snapshot.py`、`reproduce_file_v2.py`、`independent-fault-results.json`、`render-artifact-verification.json`、`render-predicate-fault.json`、`b5-readonly-verification.json`、`MIKTEX-INVENTORY.md`。
