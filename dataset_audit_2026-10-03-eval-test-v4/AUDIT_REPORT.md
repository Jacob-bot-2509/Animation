# dataset-eval / data-test 预跑检测报告（第四轮 · 指针切换至 v2 · 2026-10-03）

> 工具：`tools/eval_test_audit.py`（纯标准库，只读；本轮新增 `--manifest`（活动清单）、`--source-dir`、`--train-dir` 与指针一致性检查 PTR001–PTR005）
> 复现命令：
> `python tools/eval_test_audit.py --base data/v2 --manifest data/manifest.json --source-dir data/v2/sources --out dataset_audit_2026-10-03-eval-test-v4`
> 项目自带门禁（只读）：`data_check --manifest data/manifest.json`、`freeze_data --check`、`preflight --manifest … --strict/--ready`、`eval_test_prep status/check`
> 历史轮次：`…-eval-test`（NOT READY, hard 3）→ `…-v2`（hard 0, CONDITIONAL）→ `…-v3`（v1 复核 + v2 候选, hard 0）

---

## 0. 结论摘要与裁定

**指针已切换生效**：活动清单 `data/manifest.json`（6 条目）现引用 `v1/raw/*`（train）+ `v2/eval`、`v2/test`；`data/v1/manifest.json` 还原为 v1 归档；v2 双锁重冻并绑定活动清单。

| 维度 | 结果 |
|---|---|
| 检测基目录 | `data/v2`（活动指针所指版本） |
| 记录 | eval 300（100 题×3 解）+ test 150 = **450** |
| 逐条状态 | **rejected 0 / quarantine 450 / clean 0** |
| **我的检测** | **hard 0**、quarantine **908**、info **858**（共 1766 条） |
| 活动清单 | 6 条目，4 train + 1 eval + 1 test，**哈希 6/6 匹配** |
| 冻结锁 | `data/eval-v2.lock.json`、`data/test-v2.lock.json`，均绑定活动清单 `b11def7be9…`，条目哈希校验通过 |
| 隔离 | 精确重叠 0；≥0.7 近重复 **0**；最大 **0.6667**（未校准阈值） |
| 镜像 `.json`↔JSONL | 450/450 一致 |
| 行尾/哈希可复现 | 全 LF，通过 |
| **项目 `data_check`** | **通过**（6 条目 / 问题 0 / quarantine 0） |
| **项目 `freeze_gate`** | **PASS**（冻结证据绑定当前 manifest，eval/test 全量覆盖） |
| **项目 `preflight --ready`** | **NOT READY**（5 项阻断，见 §5） |

### 裁定

- **数据结构与指针层面：通过**。指针漂移没有留下悬空引用（活动清单哈希 6/6 匹配、v2 双锁校验"冻结完好"、`data_check` 0 问题）。
- **仍不可引用为训练/评测数据**：项目自带 `preflight --ready` 判定 **NOT READY**，阻断项为 `near_dup_calibrated`（近重复阈值 UNCALIBRATED）、`asset_evidence`（无资产验收证据 = 动画未经真实渲染/数学验收）、`exec_isolation`（网络隔离未实施），以及本次探针未提供的 `model_dir`、`run_snapshot`。
- **本轮新增待处理 4 项**：`A005`×4（v2 有 4 条 steps 未以"第N步"开头）、`PTR005`（`eval_test_prep.py` 默认指针仍为 `data/v1`）、`D012`×3（文档仍写"未冻结"）、`PTR003`/`PTR004`（活动清单 name/generated_at 未随切换刷新，info）。

---

## 1. 范围、快照与只读保证

| 类别 | 本轮对象 |
|---|---|
| 活动指针 | `data/manifest.json`（2525 B，23:52:48） |
| 入口 JSONL | `data/v2/eval/dataset_eval.jsonl`(433369, 23:24:31)、`data/v2/test/dataset_test.jsonl`(200390, 23:24:31) |
| 镜像 JSON | `data/v2/eval/dataset_eval.json`(483800)、`data/v2/test/dataset_test.json`(223709) |
| 源手稿 | `data/v2/sources/dataset-eval.md`(205684)、`data/v2/sources/data-test.md`(118713) |
| 子清单 | `data/v2/eval/manifest.json`、`data/v2/test/manifest.json`（各 573 B） |
| 冻结锁 | `data/eval-v2.lock.json`、`data/test-v2.lock.json` |
| 训练参考池 | `data/v1/raw/dataset_{calc,geom,linalg,prob}.jsonl`（63 条，LF） |
| 归档（不再活动） | `data/v1/manifest.json`、`data/v1/manifest-train.json`、`data/v1/{eval,test}/*`、`data/{eval,test}-v1.lock.json` |

- 检测快照：`2026-10-03T16:05:44Z`（= 北京时间 00:05）；18 个受检文件在检测后立即复核，哈希无变化。
- **环境说明（重要）**：项目 `.venv` 的解释器位于工作区外（`D:\Python\python.exe`）。在我的沙箱（workspace-write）下该路径被拒绝访问，`python` 回退到系统解释器 3.14.7（无 manim/sympy/markdown_it）——这会让 `preflight` 的 `render_gate`/`math_gate` 出现**假 FAIL**。改用项目 venv（一次性放宽权限）后两项均 **PASS**，故 §5 采用 venv 下的权威结论。venv 本身**并未损坏**。
- 只读保证：未修改任何数据、文档、清单或锁；未自动改 ID/公式；未启动训练、未下载模型、未生成动画。

---

## 2. 原始文件哈希（SHA256，本轮快照）

| 文件 | 字节 | SHA256（前 12 位） |
|---|---:|---|
| `data/manifest.json`（活动） | 2525 | `b11def7be902` |
| `data/v2/eval/dataset_eval.jsonl` | 433369 | `8f18123fcb3f` |
| `data/v2/test/dataset_test.jsonl` | 200390 | `d4de0bb6a86f` |
| `data/v2/eval/dataset_eval.json` / `test…json` | 483800 / 223709 | `1de2df62edd0` / `15a524ceeb1b` |
| `data/v2/eval/manifest.json` / `test/manifest.json` | 573 / 573 | `8830f1d266d4` / `cd681f55f7d4` |
| `data/eval-v2.lock.json` / `test-v2.lock.json` | 469 / 469 | `1a84b5b3c723` / `24c55a096fd1` |
| `data/v2/sources/dataset-eval.md` / `data-test.md` | 205684 / 118713 | `d681996dcf54` / `d36cab40f199` |
| `data/v1/raw/dataset_{calc,geom,linalg,prob}.jsonl` | 32908 / 18138 / 31002 / 15462 | `9f862c7c6876` / `bbd5c6ad09e9` / `f83723a082b0` / `5ddd3a1c25b9` |
| `data/v1/{eval,test}/README.md` | 282 / 258 | `31012b92e42e` / `80bb3754595a` |
| `.gitattributes` | 92 | `a2dc85e2442c` |

> 完整清单见 `file_hashes.json` / `file_hashes.sha256`（18 个文件）。

---

## 3. 指针一致性检查

| 检查 | 结果 |
|---|---|
| `PTR002` 活动清单是否覆盖本轮基目录 | **通过**（清单含 `v2/eval`、`v2/test`） |
| 活动清单条目哈希 vs 文件 | **6/6 匹配**（train 4 + eval + test） |
| 锁 ↔ 活动清单绑定 | **通过**：两把 v2 锁 `manifest_sha256 = b11def7be9…` 与活动清单一致；`freeze_data --check` 均报"冻结完好" |
| `PTR003` 清单 name | info：`animation-data-v1` 仍含 v1 字样，而 eval/test 已指向 v2 |
| `PTR004` 清单 generated_at | info：`2026-10-03 18:42:00` 早于其指向文件最新 mtime `23:24:31`（时间戳未随重写刷新） |
| `PTR005` 工具默认指针 | **quarantine**：`tools/eval_test_prep.py` 默认 `--dir` 仍为 `data/v1`。实测 `status` 报"eval-v1 锁校验通过、eval-v2 锁覆盖其他版本文件,不参与本次判定"——**不带参数运行时会判定归档版本**，与活动指针相反 |

> 说明：`data/v1/manifest.json` 归档化本身正常（提交 `68c51be` 声明"data/v1/manifest.json 还原为 v1 归档"）；问题只在**工具默认参数**未随指针切换。

---

## 4. 独立检测结果（基目录 data/v2 + 活动清单）

- **hard 0**、quarantine 908、info 858（共 1766 条）。
- 结构/字段/身份/多解组/镜像/LaTeX/隔离/冻结/清单登记：全部通过（逐项见 §6）。
- 逐条状态：450 条全部 `quarantine`（无 rejected、无 clean）——quarantine 来自系统级项（许可证待转正、动画未验证）与少量新发现问题。

### 4.1 本轮新增发现

| 代码 | 条数 | 内容 |
|---|---:|---|
| `A005` | **4** | v2 有 4 条记录的 `steps` 未以"第N步"开头（`eval-calc-023-s1/s2/s3`、`eval-prob-010-s2`）——v2 逐解法重写时的格式不一致 |
| `PTR005` | 1 | `eval_test_prep.py` 默认指针仍为 `data/v1`（见 §3） |
| `PTR003`/`PTR004` | 各 1 | 活动清单 name / generated_at 未随切换刷新（info） |

### 4.2 与第三轮相比的变化（v2 数据在 23:24 又改过一次）

- `data/v2/eval/dataset_eval.jsonl` 432636 → **433369 B**（objects 612 → 617，L007 100 → 101），新增 `A005`×4；
- `eval-linalg-023-s3` 已按复查意见修正：现明确区分"形式一（完整实不可约分解）"与"形式二（合并书写,尚未完全分解）"，并给出连接恒等式证明——**Lead 复核正确**；
- 其余结构与隔离结论不变。

### 4.3 仍未关闭（跨轮）

| 代码 | 条数 | 内容 |
|---|---:|---|
| `P002` | 450 | `license=Internal-Research-Use-Only`（仅内部研究、不公开分发），训练/公开前须转正 |
| `A008` | 450 | 动画未验证（无 `code`/`render_status`/`code_sha256`），scene_spec 仍是设计稿 |
| `D012` | 3 | `EVAL_TEST_PREP.md` 与 `data/v1/{eval,test}/README.md` 仍写"未冻结" |

---

## 5. 项目自带门禁（在项目 venv 下运行，权威结论）

| 门禁 | 结果 | 说明 |
|---|---|---|
| `data_check --manifest data/manifest.json` | **通过** | 6 条目 / 问题 0 / quarantine 0 |
| `freeze_data --check data/{eval,test}-v2.lock.json` | **冻结完好** ×2 | 锁结构与文件哈希一致 |
| `preflight --strict` → gpu | PASS | RTX 5060 Laptop 8151 MiB |
| → data_manifest | PASS | 6 条目,问题 0 |
| → render_gate | PASS | 固定 smoke 渲染成功（**非资产验收证据**） |
| → math_gate | PASS | 固定数学 smoke 断言成立（**非资产验收证据**） |
| → freeze_gate | **PASS** | 冻结证据绑定当前 manifest，eval/test 全量覆盖 |
| → model_dir | FAIL | 本次探针未提供 `--model`（非数据缺陷） |
| → run_snapshot | FAIL | 本次无 `runs/<id>/run_record.json`（非数据缺陷） |
| → near_dup_calibrated | **FAIL** | 近重复阈值仍 UNCALIBRATED（真实数据对照实验未完成） |
| → asset_evidence | **FAIL** | `asset_evidence.json` 不存在：资产未经真实渲染/数学验收 → UNVERIFIED |
| → exec_isolation | **FAIL** | 网络隔离未实施（现有：cwd 隔离+环境脱敏+禁 shell+超时+内存上限） |
| `preflight --ready` | **NOT READY** | 阻断：`model_dir`、`run_snapshot`、`near_dup_calibrated`、`asset_evidence`、`exec_isolation` |

> `render_gate`/`math_gate` 在系统 Python 下会假 FAIL（缺 manim/sympy），在项目 venv 下为 PASS——**不要**把沙箱/解释器差异当成数据缺陷。

---

## 6. 逐项检查结果

| 检查 | 结果 |
|---|---|
| JSONL 结构（解析/空行/BOM/重复键） | 通过（0 异常） |
| 字段与类型（id 唯一、12/15 字段、无未知字段） | 通过 |
| 身份唯一性（eval 300 + test 150，跨池无交集） | 通过 |
| 同题多解组（100 组×3 解、题干一致、method 唯一） | 通过 |
| 同题多解场景互异（`G003`） | 通过（0 组完全相同） |
| LaTeX（公式内 CJK/全角/`$`/括号） | 通过（0 硬性缺陷；`L006`×11、`L009`×7 经复核为误报降级 info） |
| scene_spec 结构 | 通过（450/450 含 objects+steps；`A005`×4 为步骤前缀格式，见 §4.1） |
| 镜像 `.json` ↔ JSONL | 通过（450/450） |
| 源手稿 ↔ 交付身份覆盖 | 通过（100/100、150/150） |
| 与 train 隔离 | 通过（精确 0；max 0.5915） |
| eval ↔ test 隔离 | 通过（精确 0；max 0.6667；≥0.7 对数 0） |
| 活动清单登记 | 通过（6/6 哈希匹配） |
| 冻结锁 | 通过（绑定活动清单，条目校验通过） |
| 文档状态 | 不通过（`D012`×3：仍写"未冻结"） |
| 动画验证 | 不通过（0/450） |
| 许可证 | 不通过（450/450 内部研究许可） |

---

## 7. quarantine 清单（908 条）

| 代码 | 条数 | 处置 |
|---|---:|---|
| `P002` | 450 | 用户级：许可证转正（训练/公开前） |
| `A008` | 450 | 用户级：过 `render_gate` 并登记 `code`/`render_status`/`code_sha256` |
| `A005` | 4 | **工程级（本轮新增）**：统一 v2 steps 的"第N步"前缀 |
| `D012` | 3 | 文档：更新 `EVAL_TEST_PREP.md` 与两个 v1 README 的冻结状态 |
| `PTR005` | 1 | **指针（本轮新增）**：把 `eval_test_prep.py` 默认基目录切到活动版本 |

## 8. info 亮点（858 条）

| 代码 | 条数 | 内容 |
|---|---:|---|
| `P003` | 450 | `source=self-authored`（如实） |
| `C007` | 274 | answer 与 solution 无文本重合（纯文字结论，正常） |
| `L007` | 101 | 双上下标（合法） |
| `L006`/`L009` | 11 / 7 | `\leftarrow`、`\dfrac12` 误报（已复核为合法） |
| `X002` | 3 | 三对池最大近重复（0.5915 / 0.3895 / 0.6667） |
| `PTR003`/`PTR004` | 各 1 | 活动清单 name / generated_at 未刷新 |
| `LK007`/`LK008` | 2 / 1 | 本版本锁校验通过 / 他版本锁未参与校验 |
| `G002`/`G003` | 各 1 | 多解组 {3:100} / 场景互异通过 |
| `MF008` | 1 | train 标签为"用户拍板 provisional"（如实） |
| `R001` | 1 | 既有内容评审 64 条（A5/B31/C28）纳入交叉核对 |

---

## 9. 汇总统计

| 项 | eval | test |
|---|---:|---:|
| 记录 / 唯一身份 | 300 / 300 | 150 / 150 |
| 题目数 | 100（每组 3 解） | 150 |
| 子类数 | 41 | 144 |
| objects / steps | 617 / 1212 | 303 / 603 |
| method 数 | 263 | — |
| 状态 | quarantine 300 | quarantine 150 |

- 板块：eval（高代 105 / 数分 90 / 几何 60 / 概率 45，按解法计）；test（数分 45 / 高代 40 / 几何 25 / 概率 25 / 跨学科 15）。
- 严重度：hard 0、quarantine 908、info 858（共 1766）。
- 隔离：精确重叠 0；≥0.7 近重复 0；最大 0.6667（阈值 UNCALIBRATED）。

---

## 10. 裁定与建议

**指针切换本身成功**：活动清单、锁、哈希、`data_check`、`freeze_gate` 全部一致，独立性（train/eval/test 隔离）保持通过。

**引用前需完成（按优先级）**：

1. **工程级收尾（本轮新增，易修）**：① `A005`×4 统一 steps 前缀；② `PTR005` 把 `eval_test_prep.py` 默认基目录切到活动版本（否则默认运行会判定归档 v1）；③ `PTR003`/`PTR004` 刷新活动清单 name 与 generated_at；④ `D012` 更新文档冻结状态。
2. **项目级门禁（`preflight --ready` 阻断项）**：`near_dup_calibrated`（完成 0.7 阈值校准，本轮边界对 0.6667 可作样本）、`asset_evidence`（生成真实渲染/数学验收证据，替代环境 smoke）、`exec_isolation`（网络隔离）；`model_dir`/`run_snapshot` 在正式 `--ready` 需一并提供。
3. **用户级决策**：`P002` 许可证转正；`A008` 动画验证（450 条 scene_spec 仍为设计稿，v2 的逐解法重写尚未过 `render_gate`）。

**结论**：指针指向 v2 后，数据与清单/锁层面**已自洽**（hard 0、`data_check` 通过、`freeze_gate` PASS），但**整体仍为 NOT READY**——阻断来自"阈值未校准 + 无资产验收证据 + 无网络隔离 + 无模型/运行快照"，而非数据本身。

---

## 11. 产物清单

| 路径 | 内容 |
|---|---|
| `dataset_audit_2026-10-03-eval-test-v4/AUDIT_REPORT.md` / `.pdf` | 本报告 |
| `dataset_audit_2026-10-03-eval-test-v4/issues.jsonl` | 逐条问题（1766 条） |
| `dataset_audit_2026-10-03-eval-test-v4/record_status.jsonl` / `.csv` | 450 条逐条状态 |
| `dataset_audit_2026-10-03-eval-test-v4/summary.json` | 汇总（含 pointer / locks / isolation / per_split） |
| `dataset_audit_2026-10-03-eval-test-v4/file_hashes.json` / `.sha256` | 18 个受检文件哈希 |
| `tools/eval_test_audit.py` | 只读检测工具（支持 `--base` / `--manifest` / `--source-dir` / `--train-dir`） |

**声明**：本轮为只读检测，未修改任何数据、文档、清单或锁；未自动改 ID/公式；未启动训练、未下载模型、未生成动画。
