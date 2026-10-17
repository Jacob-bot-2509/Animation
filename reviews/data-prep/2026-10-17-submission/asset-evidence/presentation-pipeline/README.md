# 呈现管线 harness v2（候选，未接训练）

本目录只做三件事：**独立复算校验**候选场景、**按权威合同拒绝渲染**、**原子组装审核包并复核签署**。
它不渲染、不执行场景、不判定数学、不代签、不产生 R/E/M/F 任何指标证据。

## 输入与输出

| 角色 | 路径 |
|---|---|
| 候选场景 + 绑定 | `../presentation-candidates/scenes/<id>.py`、`../presentation-candidates/presentation-bindings.jsonl` |
| 模板（v3） | `../template-fix-candidate/render_templates_v3_candidate.py` |
| 修正记录（只读） | `archives/reviews/codex-supervision/2026-10-17-first-batch-exact-math-review/candidate/records.jsonl` |
| 渲染门禁（权威） | `src/animtrain/sandbox_execution.py::check_certificate` |
| 输出 | `runs/review-packs/<id>/`、`runs/pipeline-receipt.json`、`runs/verdicts.json`、失败时 `runs/pipeline-receipt.FAILED.json` |

## 阶段

1. **generate**：逐题独立重算，不信任 bindings 自述。
   校验记录行 SHA、模板 SHA/版本、场景文件字节 SHA、**用模板+记录重生成场景并逐字节比对**、
   分页计划规范字节 SHA、行/页计数、`coverage_ok` 重算、几何清单与记录一致、verdict 仍为 PENDING。
   任一项不符 → 拒收（退出码 3），不产出也不替换任何包。
2. **render**：直接调用 `check_certificate()`（校验 BOUND_FILES 实现 SHA、raw 证据路径/哈希、
   D1–D8 表面与 16 项 case）。证书缺失即 `REFUSED`；通过也只记
   `CERTIFICATE_VALID_RENDER_NOT_RUN` 且 `rendered=false`——**本管线从不声称渲染成功**。
3. **review-pack**：在 `runs/.stage-<run_id>/` 组装，成功后整体替换 `runs/review-packs/`；
   每包含 `scene.py`（片段）、`scene_runnable.py`（补 `from manim import *` 与
   `class Candidate(Scene)` 的包壳，经 AST/compile 检查）、`problem.md`、`answer.md`、
   `plan.json`（规范字节）、`bindings.json`、`conclusion-sheet.md`（三选一空表）。
   构建失败保留上一份包与上一份回执，另写 `pipeline-receipt.FAILED.json`，旧 `PASS` 不会被冒充成本次结果。
4. **receipt**：含 run_id、时间、git HEAD、管线/模板/输入 SHA、逐场景 SHA、`limits` 明示限制。
5. **verify（`--verify`）**：重算包内三个 SHA、复核包壳 AST、解析结论单（恰好勾一项、
   `审核人`/`时间` 非空、`要改` 必填修改意见），写 `runs/verdicts.json`。
   未签署完整 → `REVIEW_INCOMPLETE` 且退出码 1。**只证明已签署，不证明审核正确或渲染通过。**

## 命令

```text
<venv-python> -X utf8 pipeline.py            # 构建:0 成功(渲染被拒是正常状态) 3 拒收/失败
<venv-python> -X utf8 pipeline.py --verify   # 复核:0 已全部签署 1 未完成 3 错误
```

## 明确不提供

- 真实渲染、PNG/MP4 产物、渲染/可执行率证据（须走 appcontainer 与获准入口）。
- 几何绘制：当前场景是纯文字/公式候选（0 个图元），`画面忠实度` 无任何证据。
- 原生分页测量：`layout` 仍为 `UNVERIFIED_REQUIRES_NATIVE_MEASUREMENTS`。
- 数学/画面结论：一律 PENDING_REVIEW，由审核方填写。
