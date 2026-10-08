> 后续：B5已切换用户裁决后的v3规则，本报告保留历史版本结论。最新协助修复见 [B5 v3交接](../2026-10-04-b5-v3-assist/FIX_REPORT.md)。

# 协助修复及独立复验记录

时间：2026-10-04T21:09:56.068757+08:00；修改保存在工作树，未创建提交。原始标签、历史验收JSON保持原字节；核心11项批准基线没有变化。

## 已修复

1. `tools/runpy.py`：目标脚本只收到自己的 argv；finally 恢复调用者 argv。None/整数退出码按原语义返回；字符串 SystemExit 输出原消息、返回1，不再触发二次 ValueError。真实 argparse 目标和包含空格的路径通过。
2. `tools/b5_calibrate.py`：从完整题文重算5-gram交集/并集，以 Fraction 比较，避免舍入数据驱动边界判定。报告 JSON schema2 的 threshold/Jaccard/precision/recall/fpr/fnr 为精确分数字符串；metric_counts 保存原始分子/分母。11行完整网格保留；无选定阈值时 threshold 和未测量计数为 null。未知标签拒绝，2个不确定排除；50个人工标签原文件字节不变。
3. 报告 MD/JSON/HTML/PDF 已同步。所有可表示为分数的展示数值均使用分数，无小数、None或调试标题。零分母指标显示“未定义”。阈值1/2的召回率9/11、误报率3/37；计数与修复前已独立确认的网格一致。结论仍 UNCALIBRATED，这是当前样本不满足目标的结果。
4. 新增 `tools/render_b5_report.py`：复用项目离线MathJax，先验证排版DOM再打印静态SVG，浏览器profile在项目审查目录。MathJax错误判断读取实际错误节点，忽略样式中 merror 的定义。PDF3页、51条数学片段已排版、0实际错误；三页已渲染并目视核对，标签列正常、公式/矩阵完整、跨页重复表头，无截断或重叠。源PDF有备份。
5. 文件验收：Claude 的 ff832da/v3.9 提供真实 CreateFileW错误诊断；我只把 `CORE_MODULES` 从3项补为已批准的11项，AST 对比确认除该名单字面量外无逻辑改动。新源 SHA `1d45f089d80825f0440f1e863af6a3aef24a8d7b60c0920d6fe84b3b5efec4bf`。未改其客户端或判定谓词。

## 验证

- 15项相关测试通过（执行入口、精确分数边界/舍入值污染、可分离/不可分离样本、空指标、标签校验、旧校准框架、MathJax实际错误节点检测）。记录 `regression-tests.txt`。新增12项，既有3项。
- `report-verification.json`：源标签字节不变、11网格计数保持、MD/PDF无小数、静态HTML无脚本、PDF无 MJDONE、未定义显示正确。
- Claude v3.9 纯谓词32项自检独立通过；历史 run1a74d39b87e4 快照及 review 保留，3项清单的历史不足没有被追补或改写。
- 我独立执行一次新具名目录四对照：run `487341961b6c`，parent rc=0，4/4 PASS_LOCAL_FILE_ACL。拒读/拒写均 PermissionError、errno13，独立Win32探针明确返回5=ACCESS_DENIED。源/客户端/运行时、令牌、原始JSON、实际文件、无泄漏、核心11项前后完整清单等70项独立核验全通过。运行前后11项与批准基线一致。
- 原生证据 SHA `2c62e51623b9be462a11914c1042bece14e0f550c499b9099f1cc76d99a4846f`，源文件位于 `../../2026-10-04-acceptance-support/file-evidence/file-accept-results-487341961b6c.json`；原始副本 `native-original-evidence.json`，实际stdout和stderr分别保留在 `native-stdout.json`、`native-stderr.txt`，外部rc及70项核验在 `native-independent-validation.json`。

## 范围与后续状态

文件PASS只覆盖本次合成数据/具名目录和4种操作；生产门禁仍 CLOSED，不构成整个文件系统、外网或正式渲染放行。已有正常监管监听继续记录源码和任务变化。

JSON报告 schema2 的精确值采用字符串/未定义采用 null；已检索当前源码，未发现读取该报告的其他消费者。若新增消费者，应按 schema2 读取分数，不把字符串当浮点数或把未选阈值当零。

复跑代码测试：项目venv执行 tests/test_tools_runpy.py、test_b5_pairwise.py、test_calibrate.py、test_b5_render_check.py。

重新生成报告：`python -B tools/b5_calibrate.py`；PDF：`python -B tools/render_b5_report.py --evidence reviews/codex-supervision/<新审查目录>/pdf-qa`。原生验收会创建新的具名工作目录，必要时单独执行并保存完整运行记录。

修改的前后SHA见 `changes-manifest.json`，源码/原报告备份在 `before/`，已跟踪文件差异在 `tracked-changes.patch`。测试与渲染器新文件在 tools/tests 中；补丁不含未跟踪文件。

收尾格式检查：git diff --check通过。Edge DOM的CRLF在Windows写出时形成重复回车，已规范化HTML换行，并在生成器中防止复发；仅换行发生变化，打印内容、PDF及已核对版面不变。
