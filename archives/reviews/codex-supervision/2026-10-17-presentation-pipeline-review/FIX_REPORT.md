# 呈现管线 v2 审查与修复报告（Codex 独立复验）

日期：2026-10-17 20:0x（本地）
基线：`11c20539`（工作区另有本轮之前已存在的未提交改动，见 §6）
范围：`reviews/data-prep/2026-10-17-submission/asset-evidence/` 下的呈现候选、模板候选与管线 harness
结论：**管线骨架方向正确（fail-closed、字节级 SHA、不代签），但 v1 存在 1 个阻断性缺陷、2 个高危缺陷、若干证据缺口，已修复并独立复验；几何层与真实渲染仍未实现，不在本轮范围。**

## 1. 审查发现（修复前）

| 编号 | 级别 | 发现 | 证据 |
|---|---|---|---|
| F1 | 阻断 | 10/10 场景文件只是 `construct` 方法体片段：无 `from manim import *`、无 `class Candidate(Scene)`、无 `def construct`；第 1 行即 8 空格缩进，`py_compile` 报 `IndentationError`。而 `generate` 阶段只校验文件存在+SHA 就判 `PASS`，等于把不可运行文件判成通过；审核包又把片段当"场景代码"发出，没有任何可运行形态。 | 实测 `IndentationError: unexpected indent (calc-double-integral-004.py, line 1)`；模板测试自身需手工套 `class Candidate:\n def construct(self):` 才能编译。 |
| F2 | 阻断 | 10/10 场景 **0 个几何图元**（无 `Circle/Line/Dot/Polygon/Axes/Arrow`），全部是 `MathTex`/`Text` 行的 `FadeIn/FadeOut`。题干要求的单位圆、三角形、扇形、生日格、圆柱、曲线、向量场、黎曼矩形只出现在**文字描述**里。R/E 可过，画面忠实度(F)结构性无证据；而审核包名为"目视审核"却无图可看。 | 逐场景正则统计：`drawing_primitives = 0`；`content-geometry-mapping/README.md` 第 10 行亦自述"文本候选没有修好旧几何"。 |
| F3 | 高 | 管线不可重跑：`mkdir(..., exist_ok=False)` 第二次运行必崩 `FileExistsError`；旧 `pipeline-receipt.json` 保持上一次 `PASS` 不变，与本次失败无关却看起来有效；中途失败留下半套包（非原子）。 | 实测重跑 exit 1 + traceback，receipt mtime 未变。 |
| F4 | 高 | 渲染门禁是权威合同的弱化副本：只查 `schema` 与 `fs_isolation` 两个字段，而 `check_certificate()` 还要校验 10+ 个 BOUND_FILES 实现 SHA、raw 证据必须在 WORK_ROOT 内、`raw_sha256`、D1–D8 表面、16 项 case。手工放一个两字段 JSON 即可得到 `ALLOWED_BY_EVIDENCE_PRESENT`。 | `src/animtrain/sandbox_execution.py::check_certificate`（L33–59）对比 v1 `stage_render`。 |
| F5 | 中 | 回执无 run_id/时间/git/输入 SHA/逐场景 SHA；`pack_dir` 用 Windows 反斜杠；`render` 被拒仍 exit 0，自动化无法区分"完成"与"被拒"。 | v1 `pipeline.py` L87–99。 |
| F6 | 中 | 结论单无任何机器验收：没有 verify 阶段校验"三选一恰好一项 + 审核人/时间/修改意见"，verdict 永远 PENDING；pack 的 `bindings.json` 还丢了源里的 `render_verdict/visual_verdict`。 | v1 `pipeline.py` L61–78。 |
| F7 | 中 | 审核包缺原题、答案与计划：docstring 声称"场景代码+原题+结论单"，实际只有 `scene.py`/`bindings.json`/`conclusion-sheet.md`；`plan_sha256` 在 content-geometry-mapping 有、到 presentation-bindings 被丢掉，包无法独立复算。 | v1 pack 目录清单；bindings 行字段。 |
| F8 | 低 | 无 schema 校验（缺字段直接 KeyError）、`coverage_ok=false` 不拦、`ROOT=HERE.parents[4]` 脆弱、无 README/测试、`sample_id` 未消毒即拼路径。 | v1 源码。 |
| F9 | 内容缺陷 | 90 行中有 **14 行**在字符预算处硬切，出现断词（如 `…箭长若作统一缩放须说` / `明，不能任意随机方向。`）。 | 复算 v2 计划：`mid_cut = 14/90`。 |

## 2. 修复内容

1. **新增模板 `render_templates_v3_candidate.py`**（v2 字节不动，v3 仅改 `_rows`）：文本超预算时优先在 `。，；：、！？）》」』”’，,.;:!?)]}` 之后断行，预算内无标点才硬切；字符跨度不变，`coverage_ok` 仍可精确复算。复算结果：**14 → 0 行断词，行数仍为 90**。
2. **新增 `test_template_v3_candidate.py`**：v2 全部 22 项回归 + 4 项新增（标点优先、无标点回退、混排顺序与覆盖、公式不被切开），共 **26 项通过**。
3. **重建候选**：`build_presentation_candidates.py` 改用 v3，并给每行新增 `template_version`、`template_sha256`、`plan_sha256`（规范字节：`json.dumps(sort_keys=True,separators=(",",":"),ensure_ascii=False)`），场景与绑定按 LF 写出。
4. **管线重写为 v2**（`pipeline.py`，578 行）：
   - `generate` 独立重算而不信任 bindings：记录行 SHA、模板 SHA/版本、场景字节 SHA、**用模板+记录重生成并逐字节比对**、计划规范 SHA、行/页计数、`coverage_ok`、几何清单、verdict 必须 PENDING；任一不符拒收（exit 3）。
   - `render` 直接调用 `check_certificate()`，状态只可能是 `REFUSED` / `CERTIFICATE_VALID_RENDER_NOT_RUN`，恒 `rendered=false`。
   - `review-pack` 原子化：暂存 `.stage-<run_id>` → 整体替换；失败保留旧包旧回执并写 `pipeline-receipt.FAILED.json`。
   - 包内新增 `scene_runnable.py`（补 import 与 `class Candidate(Scene)`，AST/compile 双检）、`problem.md`、`answer.md`、`plan.json`（规范字节，SHA 与绑定一致）；`bindings.json` 保留 verdict 来源与 layout/geometry 字段。
   - 回执新增 run_id、时间、git HEAD、管线/模板/输入 SHA、逐场景 SHA、`limits` 明示"text-only / rendered=false / layout 未测量 / 结论单待签"。
   - 新增 `--verify`：重算三个包内 SHA、复核包壳、解析结论单（恰好一项、签署完整、要改必填意见），写 `runs/verdicts.json`，未完成 exit 1。
5. **新增 `README.md`**（阶段、命令、退出码、明确不提供的证据）。
6. **新增 `test_pipeline.py`**：**14 项通过**，覆盖：构建成功、重复构建幂等且无残留、篡改场景拒收且旧回执不变、模板 SHA 过期、coverage=false、非法 sample_id、场景不可复现、门禁 callable 合同与拒绝态、verify 未签/已签/包被篡改/要改无意见/缺包。

## 3. 复验（独立执行，非自述）

| 项目 | 命令 | 结果 |
|---|---|---|
| 模板 v3 测试 | `python -B test_template_v3_candidate.py` | 26 passed, exit 0 |
| 管线 v2 测试 | `python -B test_pipeline.py` | 14 passed, exit 0 |
| 真实构建 | `python -B pipeline.py` | `BUILT_PENDING_RENDER`，run_id `de7d09f4ddc64cdf`，10 packs，exit 0 |
| 渲染门禁 | 同上（真实 import） | `REFUSED`：`生产隔离尚未联合验收: [Errno 2] No such file or directory: data/execution_evidence.json` |
| 审核复核 | `python -B pipeline.py --verify` | `REVIEW_INCOMPLETE`，10 packs，exit 1（预期） |
| 场景审计 | `python -B scene_audit.py --json ...` | 见下表，exit 0 |

场景审计（`scene-audit-post-fix.json`）：10 样本 / 90 行 / 断词 0 / 绑定 SHA 不符 0 / 模板输出不可复现 0 / 模板 SHA 不符 0 / 计划 SHA 不符 0 / 行页计数不符 0 / 覆盖失败 0 / 记录 SHA 不符 0 / 几何清单不符 0 / 包壳 AST 失败 0；`standalone_syntax_fail = 10`（片段本身不可独立运行，**属预期**，由 `scene_runnable.py` 补齐）、`drawing_primitives = 0`（**未解决的几何缺口**）。

## 4. 仍未解决（需决策，未擅自处理）

1. **几何层缺失**：要让"动画"成立，必须为 `scene_spec.objects` 实现逐类几何模板（单位圆/切线/扇形/生日格/圆柱/曲线带/向量场/黎曼矩形），并重新走资产证据与 F 指标。当前文本候选只能证明"文字与公式完整"。
2. **真实渲染未做**：按项目规则，生成代码只能经受审查的 AppContainer + JobObject 执行，无宿主 fallback；本报告不提供任何 R/E 证据。`scene_runnable.py` 仅为可运行包壳，**从未执行**。
3. **原生测量未做**：`layout` 仍 `UNVERIFIED_REQUIRES_NATIVE_MEASUREMENTS`；分页是字符预算的临时方案。
4. **结论单全部为空**：`verify` 会一直 `REVIEW_INCOMPLETE`，直到审核方逐包签署。签署只证明"已审核"，不证明审核正确。
5. **v2 模板未改动**：`content-geometry-mapping/COMPLETE.json` 绑定的 v2 SHA `55b18a1e…` 与当前工作区一致（该生成晚于 v2 改动）；但注意 **HEAD 中的 v2 是更早版本**（见 §6）。

## 5. 变更清单

新增：`template-fix-candidate/render_templates_v3_candidate.py`、`test_template_v3_candidate.py`、`presentation-pipeline/README.md`、`test_pipeline.py`；包内新增 `scene_runnable.py`、`problem.md`、`answer.md`、`plan.json`（10 包）。
修改：`presentation-candidates/build_presentation_candidates.py`、`presentation-bindings.jsonl`、`scenes/*.py`（10 个）、`presentation-pipeline/pipeline.py`、`runs/pipeline-receipt.json`、`runs/review-packs/*/{scene.py,bindings.json,conclusion-sheet.md}`（10 包）、`runs/verdicts.json`。
源绑定：`source-bindings.json`（10 个文件 SHA + 逐场景修复前后 SHA）。

关键 SHA：管线 `7d502a039d95bd964fa95ef639e27256fa89654acb900fe64df20d793bf954a5`；模板 v3 `81ddd639efb9e443a46617349869ecaf03f207bfcf8e372ff00359377a7f740b`；绑定 `6d5f928ef970e0004ca19db03591df4e55beabd2c3025cfffe0f14911cc55016`。

## 6. 工作区状态与边界

- 本轮**未提交**任何 git commit；改动全部留在工作区，便于复核后再决定提交。
- 工作区在本轮之前已有未提交改动：`render_templates_v2_candidate.py`（18:35，HEAD 版本为更早的中文 docstring 版）、`build_content_mapping.py`、`build_math_correspondence.py`、`pick_first_batch_10.py`、`first-batch-10.json`。它们不是本轮修改，未纳入本报告结论。
- 另有 **2092 个已跟踪文件处于"已删除未提交"**（`reviews/` 2073、`archives/` 1361，多为 `pytest-*` 临时产物，另有 19 个 `.render-tmp`）。与本次修复无关，但会淹没真实 diff，建议单独处置（提交清理或 `git checkout` 还原）。
- 本会话沙箱对 `reviews/` 树只读，重建/复核经一次性扩权执行；`python -m py_compile` 会尝试写 `__pycache__`，复验统一用 `-B` 且以 `ast`/`compile()` 内存校验代替。
