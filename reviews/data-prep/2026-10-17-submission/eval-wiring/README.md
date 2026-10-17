# 评测接线候选 v2：仅固定夹具诊断

本目录已由 Codex 独立复验并修复。它尚未接入 tools/eval_step.py，不是真实生成代码执行器、数学判定器或画面判定器；不加载模型、不调用原生探针、不开放生产。

## 修正后的边界

- 父进程只接受 fixture-only-no-model scope、固定 fixture-runs-v2 工作根和独立硬编码批准的 fixture_executor.py SHA。请求自己提供一个 SHA 不构成执行批准；不接受其他脚本、根外路径、重解析点或已有回执。
- 固定模拟执行器以 -I -B 隔离导入环境启动；这是已审查的可信模拟程序在宿主运行，不是 AppContainer 集成或“不可信生成代码宿主 fallback”。它不发射探针、不生成模型代码、不创建子进程树；正式执行隔离仍未接通。
- 同时核对完整输入记录 SHA、每条生成 spec 的实际内容 SHA、生成文件 SHA、唯一身份和固定题单覆盖；输入和源码执行前后都核对。额外/畸形身份使整响应拒绝；缺失或重复保留未知。
- 正式顶层及 eval/test 的 R/E/M/F 始终为 UNVERIFIED、rate=null、passed=null；fixture_diagnostics 只是模拟结构/分母/解码诊断，确定者标 FIXTURE_CHECKED，不能交给 hp_sweep 选 winner、不能用于真实 R/E/M/F 达标。
- 缺 stage、未知状态、超时及完整性错误不会被当成已验证失败率或通过率。数学 PASS 搭配 false 断言、断言缺失和 F 清单缺失都会在模拟诊断中正确降格；结构检查不证明数学为真或画面忠实。
- 路径逐层 lstat 拒绝 reparse/symlink；媒体只实际解码 PNG 并核对格式，其他媒体明确未知。固定小图只是解码夹具，不能代表动画质量。
- 请求/回执有大小和条数限制、超时及旧输出拒绝；该受限可信模拟程序不代表正式不可信程序的进程树/内存/持续输出隔离已经实现。后者仍需 AppContainer/JobObject 集成和独立原生证据。

## 实际复验

原 fixture-runs/、fixture-receipt.json 和 run.log 是修复前历史原件，保持不变。原运行器只打印预期、未自动断言且 fails 列表不更新；不能用 rc0 证明 20 项通过。

新 run_fixtures.py 每场景有实际断言，失败返回非零。它使用新唯一目录 fixture-runs-v2/suite-<UUID>/，保存新请求/回执/产物/日志与 fixture-receipt.v2.json，不覆盖旧回执。本轮 20 场景自动断言通过；test_eval_protocol_v2.py 的 18 项独立对抗回归通过。正式四指标仍全部未知。

新场景 05 明确额外身份拒绝整响应，不再接受“丢弃额外行但其余全绿”；场景 19 将坏 schema 的实际 spec SHA 正确绑定，单独验证模拟 E 失败。所有精确分数仅在 fixture_diagnostics 中使用，分母仍为 6 道/7 样本中的固定问题集合。

当前源码、回执与测试记录的具体路径/bytes/SHA 见上一级 evidence-index.json 的 eval_wiring 部分。没有新增真实模型、原生渲染、独立数学或视觉证据，readiness 的接线项仍为 DESIGN/GAP。

后续正式接线须提交独立批准的实现和真实逐题 sandbox/token/job/媒体/数学/语义原件，由 Codex 复验后另行判定；不能将本候选的 fixture scope 改成 production 来运行。
