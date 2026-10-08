# Codex 修改版草稿 · 修复后复检报告（2026-10-05 · 第二轮）

> 对象：**Claude Code 生成、Codex 修改**的 264 题草稿
> `reviews/2026-10-05-training-diversity-drafts/batch-01…18/draft-codex-repair-v1.jsonl`
> 工具：`tools/draft_audit.py`（只读；本轮补充误报复核）
> 复现命令：
> `python tools/draft_audit.py --out dataset_audit_2026-10-05-codex-drafts-v2 --pool data/v2/train/leakage-isolated-v3-2026-10-05 --eval-test data/v2/eval/dataset_eval.jsonl --eval-test data/v2/test/dataset_test.jsonl`
> 上一轮：`dataset_audit_2026-10-05-codex-drafts/`（hard 13、rejected 5）
> 修复提交：`e555173`（「公式内中文 15 处改英文（5 题）、步骤前缀补齐 752 条；从 staged 原件恢复后重跑」）

---

## 0. 结论摘要（修复前后对照）

| 维度 | 上一轮 | **本轮** |
|---|---|---|
| 批次 / 题数 | 18 / 264 | 18 / 264（未增删） |
| 逐条状态 | rejected **5** / quarantine 259 / clean 0 | **rejected 0 / quarantine 264 / clean 0** |
| hard | **13**（`L002`×12 + `L010`×1） | **0** |
| quarantine | 713 | **528** |
| info | 1042 | 1027 |
| 公式内中文（`L002`） | 9 处 / 5 题 | **0** |
| 步骤前缀缺失（`A005`/`V010`） | 180 题 | **0**（1172 步全部带"第N步"） |
| 与训练池泄漏 | 精确 0；max 0.4177 | 精确 0；max **0.4177**（不变） |
| 与冻结 eval/test 泄漏 | 精确 0；max 0.4186 | 精确 0；max **0.4186**（不变） |
| 集内重复 | 精确 0；max 0.4528 | 精确 0；max **0.4528**（不变） |
| 身份 / 清单 | 264 id 保留、清单匹配 | **264 id 保留、清单重绑后仍匹配** |
| 准入声明 | admitted=true 0；render=true 0 | **admitted=true 0；render=true 0**（如实） |

### 裁定：**内容层门禁通过（0 hard）**；剩余 528 条 quarantine 全部为系统级/用户级项

- 上一轮报告的 **5 题公式内中文全部修复**（`\text{其余}`→`\text{otherwise}`、`\text{唯一最近}`→`\text{uniquely nearest}`、`\text{或}`→`\text{or}`、`\text{患病}`→`\text{diseased}`、`\text{两枚皆正}`→`\text{both heads}`/`\text{same face}`）；
- 上一轮 **180 题的步骤前缀全部补齐**（现 1172 步 100% 以"第N步"开头）；
- **修改范围精确**：与 staged 原件逐条比对，仅 182 题有改动，字段分布 `scene_spec` 180、`solution` 2、`answer` 2、`problem` 1 —— 无越权改动、无新增/删除题；
- 剩余 quarantine：`P002`×264（许可证仅内部研究）+ `A008`×264（动画未验证），均与草稿内容无关。

---

## 1. 对象、基准与只读保证

| 项 | 内容 |
|---|---|
| 受检集 | `batch-01…18/draft-codex-repair-v1.jsonl`（264 条） |
| 对照集 | 同批 `draft.jsonl`（Claude 原始草稿，264 条）与 `codex-supervision/*/staged/batch-*.jsonl`（staged 原件，18 份） |
| 训练池基准 | `data/v2/train/leakage-isolated-v3-2026-10-05/dataset_{calc,geom,linalg,prob}.jsonl`（活动清单指向） |
| 评测集基准 | `data/v2/eval/dataset_eval.jsonl`、`data/v2/test/dataset_test.jsonl` |
| 清单基准 | `draft-selection.json`（19:1x 重绑）、两个 `delivery-manifest.json` |
| 板块 | 高等代数 95、数学分析 69、解析几何 55、概率论 45 |
| 只读保证 | 未修改任何草稿/数据/清单；未启动训练、未下载模型、未生成动画 |

---

## 2. 原始文件哈希（SHA256 前 12 位，完整见 `file_hashes.json`）

| 文件 | 上一轮 | 本轮 |
|---|---|---|
| `batch-01/draft-codex-repair-v1.jsonl` | `5103259cb6bd` | 见 `file_hashes.json` |
| `batch-02` … `batch-18` | 各见上轮报告 | 18 份全部变化 |
| `draft-selection.json` | `b852700ade80`* | 已重绑 |

> 本轮快照：18 份草稿 + 18 份原始草稿 + 18 份 staged 原件 + 3 份清单 + 训练池/评测集基准，全部登记在 `file_hashes.json` / `.sha256`；检测跑完后复核无变化。

---

## 3. 修复验收（逐项）

### 3.1 公式内中文（上轮 hard 13 → 0）

| 题号 | 上轮命中 | 本轮文本 |
|---|---|---|
| `draft-c52-05` | problem `\text{其余}` | `&\text{otherwise}\end{cases}` ✅ |
| `draft-c46-03` | answer `\text{唯一最近}`×2 | `P(A\text{ uniquely nearest})=1/4` ✅ |
| `draft-c09-04` | answer `\text{或}` | `h<0\text{ or }h>2.` ✅ |
| `draft-c51-03` | solution `\text{患病}`×2 | `P(\text{diseased}\mid+_1)=…` ✅ |
| `draft-c45-03` | solution×3 + scene×3 `\text{两枚皆正}` | `P(\text{both heads})=\frac14` / `\text{same face}` ✅ |

- 全量扫描：264 题的 problem/solution/answer 与 scene_spec 中，`$...$` 内 CJK/全角 **命中 0**。
- 归因复核：`introduced_cjk = []`、`preexisting_cjk = []` → 既无新增，也无遗留。

### 3.2 步骤前缀（上轮 180 题 → 0）

- 264 题共 **1172 步**，全部以"第N步"开头；`A005`/`V010` = 0。

### 3.3 修改范围核对（staged 原件 → 当前）

| 字段 | 改动题数 |
|---|---:|
| `scene_spec` | 180 |
| `solution` | 2 |
| `answer` | 2 |
| `problem` | 1 |
| **合计（有改动的题）** | **182 / 264** |
| 其它字段（id/category/…） | **0** |

→ 改动**精确落在修复范围内**（步骤前缀 180 + 公式内中文 5 题中的 5 个字段），未触碰身份、分类、来源、许可证等字段；未新增或删除题目。

---

## 4. 泄漏检测（与上轮一致，仍干净）

| 对比对象 | 精确题干重叠 | 最大题干近重复（5-gram，set） | ≥0.7 |
|---|---:|---:|---:|
| 当前训练池（leakage-isolated-v3） | **0** | 0.4177（`draft-c40-02` ↔ `linalg-065`） | 0 |
| 冻结 eval/test | **0** | 0.4186（`draft-c13-02` ↔ `test-calc-013`） | 0 |
| 草稿集内 | **0** | 0.4528（`draft-c03-01` ↔ `draft-c03-05`） | 0 |

---

## 5. 声明与清单核查

| 检查 | 结果 |
|---|---|
| `admitted=true` | **0**（264 条全 false） |
| `animation_render_verified=true` | **0** |
| `draft_status` | 全为 `CODEX-REPAIR-v1-NOT-ADMITTED` |
| id 保留 | 与原始草稿 id 集合与顺序 **完全一致**（264/264） |
| 与原始草稿差异 | 264/264 均有改动（修复后仍成立） |
| `draft-selection.json` | 声明 264 = 实际 264、`deleted_questions=0`、状态 `DRAFT_ONLY_NOT_TRAINING_ADMISSION`；18 批 **sha256 与条数全部匹配**（重绑成功） |
| 未入库 | 264 题与训练池无精确重叠且 `admitted=false` → 未混入训练清单 |

---

## 6. 剩余问题与误报说明

### 6.1 quarantine（528 条，全部系统级/用户级）

| 代码 | 条数 | 内容 | 处置 |
|---|---:|---|---|
| `P002` | 264 | `license=Internal-Research-Use-Only`（仅内部研究、不公开分发） | 用户级：训练/公开前转正 |
| `A008` | 264 | 动画未验证（scene_spec 缺 `code`/`render_status`/`code_sha256`） | 用户级：过 `render_gate` 后登记 |

### 6.2 上轮 quarantine 中已消除的项

`A005`×180（步骤前缀）、`V010`×1、`L011`×1 → 本轮 **0**。

### 6.3 本轮复核为**误报**并降为 info 的 3 条

| 代码 | 位置 | 原判 | Lead 复核结论 |
|---|---|---|---|
| `C008`×2 | `draft-c46-03` | 重复等式 `1/2,y = 1/2,y` | 实为逗号并列的三条直线枚举 `$x=1/2,y=1/2,y=x$`，**非笔误** |
| `L008`×1 | `draft-c07-01` scene_spec | 多位数字上标 `^23` | 实为 `4\sin^23\theta`（单字符上标 2 + 系数 3），**合法 TeX** |

### 6.4 info 概览（1027 条）

`P003`×264（self-authored）、`C007`×257（answer 与 solution 等价表述/纯文字结论）、`L009`×343（`\frac` 单 token，合法）、`L007`×154（双上下标，合法）、`C008`×2 / `L008`×1（本轮误报降级）、`X003`×2、`X005`×1、`V004`/`V005`/`V009` 各 1。

---

## 7. 汇总统计

| 项 | 值 |
|---|---|
| 批次 / 记录 | 18 / 264（原始对照 264，staged 原件 264） |
| 状态 | rejected **0**、quarantine 264、clean 0 |
| 严重度 | hard **0**、quarantine 528、info 1027（共 1555） |
| 泄漏 | 训练池 0 / eval-test 0 / 集内精确 0；最大近重复 0.4177 / 0.4186 / 0.4528 |
| 公式内中文 | 0（修复前 9 处 / 5 题） |
| 步骤前缀 | 1172/1172 合规（修复前 180 题缺失） |
| 改动范围 | 182 题（scene_spec 180、solution 2、answer 2、problem 1） |
| 准入声明 | admitted=true 0、render_verified=true 0 |

---

## 8. 裁定与建议

1. **内容层门禁通过**：本轮 0 hard，上一轮的全部内容问题（5 题公式内中文、180 题步骤前缀）已修复并复核；修改范围精确、身份与清单一致。
2. **可以进入准入流程的下一环**：若计划把这 264 题纳入训练池，需由用户批准并按项目流程执行（新版本号 → 重跑多样性/泄漏门禁 → make_manifest → freeze → preflight）。
3. **仍需完成的用户级前置**：
   - `P002`：`license` 由 `Internal-Research-Use-Only` 转正；
   - `A008`：264 条 scene_spec 过 `render_gate` 并登记 `code`/`render_status=verified`/`code_sha256`；项目 `preflight --ready` 仍以 `asset_evidence`、`near_dup_calibrated`、`exec_isolation` 等阻断。
4. **门禁建议**：本轮最大近重复 0.4528/0.4177/0.4186 均远低于 0.7，可纳入阈值校准的负样本。

---

## 9. 产物清单

| 路径 | 内容 |
|---|---|
| `dataset_audit_2026-10-05-codex-drafts-v2/AUDIT_REPORT.md` / `.pdf` | 本报告 |
| `dataset_audit_2026-10-05-codex-drafts-v2/issues.jsonl` | 逐条问题（1555 条） |
| `dataset_audit_2026-10-05-codex-drafts-v2/record_status.jsonl` / `.csv` | 264 题逐条状态 |
| `dataset_audit_2026-10-05-codex-drafts-v2/summary.json` | 汇总（含泄漏、归因、按批统计） |
| `dataset_audit_2026-10-05-codex-drafts-v2/file_hashes.json` / `.sha256` | 受检文件哈希 |
| `tools/draft_audit.py` | 只读检测工具（含本轮误报复核） |

**声明**：本轮为只读复检，未修改任何草稿、数据、清单或锁；未自动改写公式或 ID；未启动训练、未下载模型、未生成动画。
