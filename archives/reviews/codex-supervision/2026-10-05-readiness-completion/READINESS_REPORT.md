# 训练前准备：隔离、网络验收与沙箱渲染修复

本轮已完成独立题文初审、已识别结构泄漏隔离、四个公网 TCP 端点验收和可信模板沙箱渲染试点。整体训练状态仍为 NOT READY：现行文字检测规则未通过新的结构定义校准，全量资产未验收，生产生成代码执行链尚未切换并通过联合验收。没有启动训练或放开生成代码门禁。

## 泄漏复核与数据隔离

用户已确认：核心解题结构相同、主要只换数字/符号/表述的题按泄漏处理，训练与评测之间需要隔离。标签来源为 Codex 独立题文审阅；用户确认的是定义，新增逐对判断不冒充用户亲自标注。原 B5 用户标签和裁决保留。

先对 63 条训练与 250 个评测/测试独立题文做同签名普查，219 对候选初审发现 8 对明确结构复用。进一步补读原候选未覆盖的 153 个题文并对照活动训练，发现 9 对跨签名复用：参数和函数直接代值、裂项求和、异面直线距离、直线与二次曲面相交、二次型标准化、贝叶斯后验及均匀变量幂函数变换。合计 17 对，涉及 15 条训练记录；没有把共享知识点本身判作泄漏。

对应训练记录已从活动版本移出，原记录与每次清单/锁原字节归档。当前训练 48 条、eval 300 条、test 150 条，共 498 条。活动训练路径为 `data/v2/train/leakage-isolated-v2-2026-10-05/`。原 v1 文件、冻结评测/测试 JSONL 与 raw JSON、B5 用户标注均未改动；双锁通过 `freeze_set` 重建新清单绑定，前任锁原字节保留在 `before-isolation/` 与 `before-isolation-v2/`。

新增 `tools/leakage_population.py` 默认纳入不同签名，不自动赋标签或校准。对最终数据生成 12,000 对全量跨集合候选（同签名 155 对），按题文哈希去重并保留全部来源。**这份普查不是 12,000 对均已取得人工泄漏标签的证明。** 标签版本 v2 共 228 对独立 AI 审阅记录（17 对泄漏、211 对不泄漏），用于记录已知失败和隔离。

现行“签名一致 AND J5≥2/5”对已发现的 17 个结构复用例均漏检，不能据此宣布达到召回目标 19/20。保持 UNCALIBRATED；不降阈值制造校准通过，也不凭清理后没有正例宣称召回率为 1。后续结构检测器需按新定义设计、独立留出验证并绑定输入与实现。旧 B5 考点标签不能替代该验证。

## MiKTeX 与网络验收

源安装只读复制到项目 `.sandbox-runtime/miktex-real/`。实际 23,560 个文件，共 1,092,826,980 字节，源/目标全量 SHA256 一致，无重解析点。运行配置经 `initexmf --report` 证实为 Portable，安装、配置和数据目录均指向项目 D 盘目录；禁自动装包。最小公式 `x^2+y^2=1` 实际编译到 DVI/SVG，沙箱 Manim 中使用明确的 `-disable-installer` 和 `-disable-write18` 参数。

运行后再次全量检查：C 盘源安装不变；副本中的旧更新程序备份被运行时清理，发现后从源恢复。恢复前后记录分别保留，其他原安装文件一致；新增配置/日志/数据库单列。关闭自动装包参数参考 [MiKTeX 官方文档](https://docs.miktex.org/manual/initexmf.html)，实际配置以本机报告和命令日志为准。

外网仅 TCP connect，不发送应用数据。端点为 `1.1.1.1:443`、`1.0.0.1:443`、`[2606:4700:4700::1111]:443`、`[2606:4700:4700::1001]:443`。每个普通进程前后对照均能连接，同一运行时的 AppContainer 客户端均明确返回 WinError 10013，真实 SID 匹配、能力数为 0，无 site/shim 注入，运行时/客户端哈希一致。4/4 PASS_TESTED_EXTERNAL_TCP。这个结果仅证明所测 TCP 端点和窗口，不扩大为所有协议/端点或生产门禁已验收。

## 沙箱渲染接线与内存故障修复

新增 `tools/sandbox_render_pilot.py`，只从已登记当前数据构建项目可信模板，复用 AppContainer 的 suspended→JobObject→resume 机制、2 GiB 内存限制和进程树清理。授权限于项目 MiKTeX 副本、配置缓存与具名工作目录；复用原有 Python/venv 读取权限，不扩大 C 盘源安装权限，不修改注册表/防火墙/网络豁免。

固定中文/公式冒烟实际生成 MP4，完整解码 30 帧、854×480、时长 2 秒；画面检查通过。八种当前数据模板首轮 7/8，graph_limit 最后公式编译失败。诊断证实 JobObject 内存峰值 2,153,242,624 字节，触及 2,147,483,648 字节限制；同一公式单独沙箱编译通过。

修复 `tools/render_templates.py`：先编译答案公式，再构建中文 Text；答案仍在最后显示。相同内存限制下原失败场景通过，修复后峰值为 1,980,157,952 字节。完整八模板复跑 8/8，每个最终 MP4 都完整解码、验证真实令牌及文件哈希。八条输入未因训练隔离而改变，最终按当前清单逐条核对输入行/产物哈希，保留原生报告原字节。

这些模板证明运行管线，不证明动画内容忠实于每道题。部分模板仍是通用图形；例如 graph_limit 的示意曲线与选中题的具体函数未必一致。每条数学状态仍为 UNVERIFIED，没有伪造 `asset_evidence.json`。

## 复验与后续边界

全套 438 项测试通过，其中新增沙箱工具的 9 个失败边界测试；之后新增普查工具的 5 项测试也全部通过。日志保留既有 ResourceWarning，没有把警告当作零告警。最终 498 条数据入口 clean，data_check 0 问题/0 quarantine，双锁有效并绑定当前 manifest，git diff --check 通过。11 个核心执行文件未偏离既有基线。

当前 manifest SHA256：`c1f18378ca2b28df5629c908070cc68498dea00977c62c196d6946734954f500`。

剩余项目验收：结构规则的独立校准、全部 498 条资产的逐条数学/语义/渲染验收、生产生成代码执行路径的接线与联合边界验收。本轮没有将八模板试点或四个 TCP 端点对照扩大成完整训练放行。

## 证据与复跑

- `independent-leakage-labels-v2.json`、`cross-signature-leakage-findings.json`：审阅依据和题文哈希。
- `isolated-training-records*.json`、`isolation-update-v2.json`：隔离原记录及版本切换。
- `current-cross-split-population.json`：当前 12,000 对普查及精确分数。
- `miktex-copy-manifest.json`、`miktex-post-run-restored-verification.json`、`miktex-config-report-paths.txt`：全量复制、配置与复验。
- `external-tcp-results.json`、`external_tcp_probe.py`：原生外网对照。
- `pilot-83c6d358b0ea/pilot-report.json`：八模板全通过及真实媒体。
- `graph-limit-job-memory*.json`、`template-order-verification.json`：内存峰值与显示顺序验证。
- `regression-cli-results.json`、`final-cli-results.json`、`final-independent-verification.json`：测试、最终数据与绑定验收。
- `final-file-manifest.json`、`final-source/`：修改文件最终哈希和源码快照。

```powershell
.venv/Scripts/python.exe -X utf8 -B tools/sandbox_render_pilot.py --limit 8 --format mp4
.venv/Scripts/python.exe -X utf8 -B tools/leakage_population.py --output reviews/codex-supervision/新目录/population.json
.venv/Scripts/python.exe -X utf8 -B tools/data_check.py --manifest data/manifest.json
```

重新渲染会建立新的具名工作目录并使用既有项目副本/缓存；媒体属于可信模板试点，不自动写正式资产验收证据。普查拒绝覆盖历史输出。

Git跟踪边界已补齐：仅放行两个具名隔离版本的 JSONL，防止后续提交清单时遗漏活动数据；.sandbox-runtime/ 仍作为本地工具链副本忽略。本轮未创建提交。
