【呈现管线 v1 审查结束：Codex 已修改并复验】

对象：presentation-candidates/（msg_904）与 presentation-pipeline/（msg_905）。方向正确（fail-closed、字节级 SHA、不代签），但 v1 有 2 个阻断缺陷、2 个高危缺陷，Codex 已实际修改，不是只给建议。

一、已修问题
1. 10/10 场景只是 construct 片段（无 class Candidate(Scene)），py_compile 第 1 行即 IndentationError；generate 只查存在+SHA 就判 PASS。→ 新增 v3 模板与可运行包壳 scene_runnable.py（AST+compile 双检），管线改为用模板+修正记录重生成场景并逐字节比对。
2. 10/10 场景 0 个几何图元，纯文字/公式，画面忠实度(F)结构性无证据。→ 没有代造几何；改为在回执 limits、审核包与结论单明示，F 保持无证据。
3. 管线不能重跑：mkdir(exist_ok=False) 第二次必崩 FileExistsError，旧 PASS 回执不失效。→ 暂存目录 + 原子替换；失败写 pipeline-receipt.FAILED.json，旧回执不被冒充。
4. 渲染门禁是权威合同的弱化副本（只查 2 字段）。→ 直接调用 src/animtrain/sandbox_execution.check_certificate()，只允许 REFUSED / CERTIFICATE_VALID_RENDER_NOT_RUN，恒 rendered=false。
5. 回执缺 run_id/时间/git/输入 SHA、审包缺原题/答案/计划 SHA、结论单无机器验收。→ 全部补齐，新增 --verify（恰好一项、签署完整、要改必填意见）。
6. 90 行中 14 行硬切中文断词。→ v3 行尾优先断在标点：断词 14→0，行数仍 90，覆盖精确。

二、修改文件
新增：template-fix-candidate/render_templates_v3_candidate.py、test_template_v3_candidate.py、presentation-pipeline/README.md、test_pipeline.py；每包新增 scene_runnable.py、problem.md、answer.md、plan.json。
修改：presentation-candidates/build_presentation_candidates.py、presentation-bindings.jsonl、scenes/*.py（10 题：calc-limit-006、eval-prob-007-s1、prob-046、prob-042、prob-043、calc-double-integral-004、calc-green-005、calc-series-015、calc-series-017、calc-vol-012）、presentation-pipeline/pipeline.py、runs/pipeline-receipt.json、10 包 scene.py/bindings.json/conclusion-sheet.md。
v2 模板一个字节未动（content-geometry-mapping 钉了它的 SHA）。

三、复验（实跑）
模板 v3 26 项、管线 v2 14 项测试通过；真实重建 BUILT_PENDING_RENDER，run de7d09f4ddc64cdf，10 包；渲染门禁 REFUSED（data/execution_evidence.json 不存在，真实门禁原因）；--verify = REVIEW_INCOMPLETE（10 份结论单全空，未代签）；独立审计：绑定/模板/计划/覆盖率/记录/几何清单不符全 0，断词 0，包壳 AST 失败 0。

四、合格范围
合格：场景可由模板+修正记录复现、绑定 SHA 一致、审包可原子重建、审核有机器可验的未签/已签两态。
不合格：不证明可渲染、不证明画面忠实度、不证明数学审核通过、不证明原生分页可读；无 R/E/M/F 证据。

五、仍未解决
几何层缺失（单位圆/切线/扇形/生日格/圆柱/曲线带/向量场/黎曼矩形）；真实渲染须走 AppContainer + 获准入口；layout 仍 UNVERIFIED_REQUIRES_NATIVE_MEASUREMENTS；10 份结论单待签。

六、交接要求
请按本修复版本继续：不要重复修改 Codex 已完成的 pipeline v2、v3 模板、审包与测试；几何层请先出设计（哪些题、哪类模板、F 指标如何取证）再实现；渲染不得绕开 check_certificate；不要用"存在/进程/退出码"当渲染或数学证据。本轮 Codex 未提交 git，改动都在工作区。

归档：archives/reviews/codex-supervision/2026-10-17-presentation-pipeline-review/FIX_REPORT.md（SHA 见 metadata.report_sha256）；ACK 绑定报告 reviews/codex-supervision/2026-10-17-presentation-pipeline-review/REPORT.md。
