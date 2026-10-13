# 全量数据渲染检查报告（2026-10-05）

> 目的：快速看清**所有数据**的公式排版/渲染情况
> 方式：把每个数据集的**全部字段**（problem / solution / answer / scene_spec.objects / scene_spec.steps）打成渲染包 MD，用项目自带 `tools/render_review.py --check`（本地 MathJax tex-svg + headless Edge，`--dump-dom` 统计未排版公式）逐集核对
> 复现：
> `python tools/render_review.py <render-pack>.md --out-dir <dir> --check --skip-pdf`
> 产物：`render-packs/*.md`（输入）、`render/*/`（HTML 证据）、`render-results.json`（机读结果）

---

## 0. 结论

**全部 824 条记录、16,539 条公式，未排版 0 条 —— 公式排版层面全部通过。**

| 数据集 | 记录 | 公式（已排版） | 未排版 | 耗时 |
|---|---:|---:|---:|---:|
| `data/v1/raw`（原训练池 63） | 63 | 884 | **0** | 1.7s |
| `data/v2/train/leakage-isolated-v3`（现行训练池） | 47 | 693 | **0** | 1.5s |
| `data/v2/eval`（冻结 eval） | 300 | 4540 | **0** | 6.3s |
| `data/v2/test`（冻结 test） | 150 | 2106 | **0** | 3.3s |
| `reviews/…/draft-codex-repair-v4-final`（264 题草稿） | 264 | 8316 | **0** | 9.5s |
| **合计** | **824** | **16,539** | **0** | ~22s |

> 另用项目自有审阅稿 MD 复核一次（`dataset.md` 884、`data-test.md` 2025、`dataset-eval.md` 3469、`outputs/draft-review/draft-review-v4-final.md` 8316），同样**全部 0 未排版**。

---

## 1. 静态渲染风险扫描（同一批数据的文本层）

| 数据集 | 公式 span | `$` 奇偶异常 | 花括号不平衡 | `\left/\right` 不配对 | 公式内中文 | 公式内全角 |
|---|---:|---:|---:|---:|---:|---:|
| v1 raw 63 | 884 | 0 | 0 | 0 | 0 | 0 |
| v2 train 池 | 693 | 0 | 0 | 0 | 0 | 0 |
| v2 eval | 4548 | 0 | 0 | 0 | 0 | 0 |
| v2 test | 2106 | 0 | 0 | 0 | 0 | 0 |
| drafts v4-final | 8316 | 0 | 0 | 0 | 0 | 0 |
| **合计** | **16,547** | **0** | **0** | **0** | **0** | **0** |

- 静态计数比渲染计数多 8 条：来自 eval 中 3 条记录使用 `$$…$$` **显示公式**（`eval-linalg-019-s3`、`eval-linalg-021-s2`、`eval-linalg-032-s3`）。渲染器的 MathJax 配置含 `displayMath:[['$$','$$']]`，这 8 处**均正常排版**，属**写法不统一**（其余 800+ 条一律单 `$` 行内），不是渲染缺陷。
- 无 `$$` 之外的空公式、无未闭合定界符。

---

## 2. 与"资产渲染验证"的区别（重要）

上表是**公式排版**（MathJax→SVG）层面。项目另有**逐资产渲染/数学验收**（manim 出图 + 语义校验），其证据在 `data/asset_evidence.json`：

| 指标 | 值 |
|---|---|
| schema | `asset-evidence-progress-v1` |
| 记录总数 | **497** |
| 已语义验证 | **1** |
| 语义未通过/未验证 | **496** |
| 状态 | **NOT READY** |
| scope 原文 | "One individually reviewed asset; 496 assets remain unverified. This is incomplete progress evidence." |

→ 也就是说：**公式排版全绿，但逐资产渲染验收仍是 1/497**；`preflight --ready` 仍会因 `asset_evidence` 阻断。

---

## 3. 检查口径与环境

- **渲染链路**：`tools/render_review.py` → `protect_math` 把 `$…$`/`$$…$$` 包进 `<span class="math">` → 本地 `tools/assets/mathjax-tex-svg.js`（2.1 MB，**无需联网**）+ headless Edge（`--dump-dom --virtual-time-budget=240000`）→ 统计含 `<mjx-container>` 的 span 数；未排版 = span 总数 − 已排版。
- **覆盖面**：每个数据集**全部记录的全部字段**（含 `scene_spec.objects` / `scene_spec.steps`），非抽样。
- **只读**：源数据未改动；渲染包与 HTML 写入 `dataset_audit_2026-10-05-render-check/`。

---

## 4. 产物

| 路径 | 内容 |
|---|---|
| `RENDER_REPORT.md` / `.pdf` | 本报告 |
| `render-results.json` | 逐数据集"已排版/未排版"机读结果 |
| `render-packs/*.md` | 5 个渲染包（824 条记录全字段） |
| `render/<dataset>/*.html` | 渲染后的 HTML 证据（含 MJDONE 标记） |
| `_scan.py` / `_dollar.py` / `_packs.py` | 只读检查脚本 |

**声明**：本轮为只读渲染检查，未修改任何数据；未启动训练、未下载模型、未生成动画（未执行 manim 渲染，仅公式排版与静态扫描）。
