# 第二轮：Claude 新工作审查 + 十题真实渲染试点（Codex）

日期：2026-10-17 21:3x（本地）
审查对象：commit `d2b7b3b3`（把我的管线修复连同 B5/备份工作一起提交）、`a6046174`（archives/harness + archives/codex 分档）、`3eeed869`（geometry-layer-design.md）；消息 msg_908（归档分档）、msg_909（几何层设计）。

## 一、审查结论

- 三个提交都没有改写既有冻结归档；`reports`/`FIX_REPORT`/ACK 绑定路径仍在；我的管线文件被原样提交，SHA 与回执一致（pipeline `7d502a03…` 提交前值）。
- `archives/harness` 与 `archives/codex` 两个新档只含 README，未迁移任何原件；`archives/codex` 是否由我使用属我的归档所有权，**Codex 不启用**，继续按 AGENTS 写入 `archives/reviews/codex-supervision/`。
- 几何层设计结构可用；但缺三件事，已由 Codex 补写（见下）。

## 二、发现并修复的错误

1. **prob-042 公式含中文导致 LaTeX 编译失败（真实失败）**
   `$F_n=\frac{\#\text{正面}}{n}$` 在 Manim 默认模板（english babel、无 CJK）报 `! LaTeX Error: Unicode character 正 (U+6B63)`，AppContainer 试点该题返回 `manim_failed`。
   修复：新建 `candidate-v2/records.jsonl`（只改这一行：`\text{正面}` → `\text{heads}`，并在同一步注明“heads 为正面次数”；其余 9 行逐字节不变），见 `candidate-v2/PATCH.md`。
2. **文字与公式片段紧贴**：`arrange(RIGHT, buff=0)` 使“正向圆周 L”“趋于 0”等边界粘连；480p 试点帧可复现。
   修复：新模板 `render_templates_v4_candidate.py`（`ROW_BUFF=0.12`），v2/v3 字节不动；27 项测试通过。
3. **几何设计缺合成边界与保真约束**
   补：§五 与文字候选的合成边界（`candidate_requires_dedicated_empty_canvas` 决定必须分场或模板 v4，不能拼贴）；§六 等比例、逐题精确值、三维相机锁定。
4. **提交标题与内容不一致（仅记录）**：`3eeed869` 标题写“7 类模板”，正文与表格是 10 类。

## 三、复验

- v4 模板：27 项通过；管线 v2：14 项通过。
- 场景审计（v4 + candidate-v2）：10 题 / 90 行 / 断词 0；模板、场景、计划、记录、覆盖率、几何清单不符全 0；包壳 AST 失败 0。
- 管线重建：`BUILT_PENDING_RENDER`，10 包，render `REFUSED`（`data/execution_evidence.json` 缺失），`--verify` = `REVIEW_INCOMPLETE`（结论单全空）。

## 四、十题真实渲染试点（AppContainer，非生产验收）

传输：`src/animtrain/sandbox_execution.run_code`（Windows AppContainer + JobObject，私有 profile，无宿主 fallback；`network_isolated=false`，未做 43 项联合验收）。
结果：**10/10 渲染成功**，每题 45 帧 / 854×480 / 15fps，合计 1,060,139 字节；工件与抽样帧在 `presentation-pipeline/runs/render-pilot/`，逐题 SHA 见 `manifest.json`（SHA256 `ac262a6d80cbf6329b26b599dfb36ca7755949730ddf297d4324dfe78ac1eb38`），联系表 `contact-sheet.png`。

| 题 | 状态 | 耗时 | 帧 |
|---|---|---|---|
| calc-double-integral-004 | rendered | 42.1s | 45 |
| calc-green-005 | rendered | 42.2s | 45 |
| calc-limit-006 | rendered | 46.8s | 45 |
| calc-series-015 | rendered | 38.3s | 45 |
| calc-series-017 | rendered | 40.1s | 45 |
| calc-vol-012 | rendered | 42.2s | 45 |
| eval-prob-007-s1 | rendered | 37.3s | 45 |
| prob-042 | rendered | 39.5s | 45 |
| prob-043 | rendered | 42.8s | 45 |
| prob-046 | rendered | 42.7s | 45 |

## 五、限定与未解决

- 试点不是 43 项联合验收：`exec_isolation` 仍未验收，`network_isolated=false`；本结果不能记 R/E/F 任一指标，也不解禁生产（production 仍 CLOSED）。
- 场景仍是纯文字/公式幻灯片（0 个几何图元），F 无证据；几何层仅有设计。
- layout 仍 `UNVERIFIED_REQUIRES_NATIVE_MEASUREMENTS`（本次只证明代码可渲染、内容可读）。
- 10 份审核包结论单仍为空；数学结论未代签。

## 六、变更文件

新增：`render_templates_v4_candidate.py`、`test_template_v4_candidate.py`、`candidate-v2/records.jsonl`（+PATCH.md）、`presentation-pipeline/runs/render-pilot/`（10 mp4 + 30 png + manifest + contact-sheet）。
修改：`build_presentation_candidates.py`（v4 + candidate-v2）、`presentation-bindings.jsonl`、`scenes/*.py`（10）、`pipeline.py`（template/records 路径）、`runs/pipeline-receipt.json`、`runs/verdicts.json`、`runs/review-packs/*`（10 包）、`geometry-layer-design.md`（§五/§六）、`test_pipeline.py`（模板指向 v4）。
