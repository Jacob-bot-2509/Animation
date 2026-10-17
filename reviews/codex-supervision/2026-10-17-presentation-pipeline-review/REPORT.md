# 呈现管线 v1 审查结论（供 ACK 绑定）

日期：2026-10-17 20:1x（本地）
被审对象：`presentation-candidates/`（msg_904）与 `presentation-pipeline/`（msg_905）
完整报告：`archives/reviews/codex-supervision/2026-10-17-presentation-pipeline-review/FIX_REPORT.md`

## 结论

管线骨架方向正确（fail-closed、字节级 SHA、不代签），但 v1 有 2 个阻断缺陷、2 个高危缺陷与若干证据缺口。**Codex 已实际修改并独立复验**；几何层与真实渲染不在本轮范围，仍未实现。

## 已修复

1. 场景文件只是 `construct` 片段、无 `class Candidate(Scene)`，`py_compile` 即 `IndentationError`，而 generate 仅凭存在+SHA 判 PASS → 新增 v3 模板与可运行包壳，管线新增"用模板+记录重生成并逐字节比对"的复算校验。
2. 10/10 场景 0 个几何图元（纯文字）→ 未擅自补几何，改为在回执 `limits`、审核包与结论单中明示，F 指标保持无证据。
3. 管线重跑必崩且旧 `PASS` 回执不失效 → 改为暂存目录原子替换；失败写 `pipeline-receipt.FAILED.json`，旧回执不被冒充。
4. render 门禁是权威合同的弱化副本 → 改为直接调用 `check_certificate()`，只允许 `REFUSED` / `CERTIFICATE_VALID_RENDER_NOT_RUN`，恒 `rendered=false`。
5. 回执缺证据元数据、审核包缺原题/答案/计划 SHA、结论单无机器验收 → 全部补齐，并新增 `--verify`。
6. 90 行中 14 行中文断词 → v3 行尾优先断在标点，断词 0、行数不变、覆盖精确。

## 复验

- 模板 v3：26 项通过；管线 v2：14 项通过。
- 真实重建：`BUILT_PENDING_RENDER`，run `de7d09f4ddc64cdf`，10 包。
- 渲染门禁：`REFUSED`（`data/execution_evidence.json` 不存在，真实门禁原因）。
- `--verify`：`REVIEW_INCOMPLETE`（10 份结论单均为空，按设计未代签）。
- 独立审计：绑定/模板/计划/覆盖率/记录/几何清单不符全 0，断词 0，包壳 AST 失败 0；`drawing_primitives=0` 为未解决项。

## 合格范围（限定）

合格：场景字节可由模板+修正记录复现；绑定 SHA 一致；审核包可原子重建、可复核；审核流程有机器可验的未签/已签两态。
不合格：不证明动画可渲染、不证明画面忠实度、不证明数学审核通过、不证明原生分页可读；未有 R/E/M/F 证据。

## 未解决

- 几何层缺失（单位圆/切线/扇形/生日格/圆柱/曲线带/向量场/黎曼矩形）。
- 真实渲染未做（须 AppContainer + 获准入口）。
- layout 仍 `UNVERIFIED_REQUIRES_NATIVE_MEASUREMENTS`。
- 10 份结论单待审核方签署。
