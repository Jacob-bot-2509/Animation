# Codex 修改版草稿独立检测报告（2026-10-05）

> 对象：**Claude Code 生成、Codex 修改**的 264 道题草稿
> `reviews/2026-10-05-training-diversity-drafts/batch-01…18/draft-codex-repair-v1.jsonl`
> 工具：`tools/draft_audit.py`（本轮新建，只读；复用 `tools/dataset_audit.py` 的结构/一致性/LaTeX/scene_spec/来源许可证规则）
> 复现命令：
> `python tools/draft_audit.py --out dataset_audit_2026-10-05-codex-drafts --pool data/v2/train/leakage-isolated-v3-2026-10-05 --eval-test data/v2/eval/dataset_eval.jsonl --eval-test data/v2/test/dataset_test.jsonl`
> 基准：当前活动清单 `data/manifest.json`（train = `v2/train/leakage-isolated-v3-2026-10-05`；eval/test = `v2/{eval,test}`）

---

## 0. 结论摘要

| 维度 | 结果 |
|---|---|
| 批次 / 题数 | **18 批 / 264 题**（batch-07 14 题、batch-18 10 题，其余各 15 题） |
| 逐条状态 | **rejected 5 / quarantine 259 / clean 0** |
| 问题计数 | **hard 13**、quarantine 713、info 1042（共 1768 条） |
| **与当前训练池泄漏** | **无**：精确重叠 0；最大题干近重复 **0.4177** < 0.7 |
| **与冻结 eval/test 泄漏** | **无**：精确重叠 0；最大 0.4186 < 0.7 |
| 草稿集内重复 | 精确 0；最大近重复 0.4528 < 0.7 |
| 身份 | 264 个 id 唯一；与原始草稿 **id 与顺序 100% 保留** |
| 准入声明 | `admitted=true` **0** 条、`animation_render_verified=true` **0** 条（如实） |
| 清单核对 | `draft-selection.json` / 两个 delivery-manifest 的 sha256 与条数 **全部匹配** |
| 改动幅度 | 与原始草稿逐条比对：**264/264 都有内容改动**（Codex 确已修改） |

### 裁定：**不可准入（5 题须修）**，但泄漏门禁干净

- **硬伤 5 题**：`$...$` 公式内出现中文（TeX 无 CJK，渲染必失败）。
  - **其中 3 题是本次 Codex 修改新引入的**（原始草稿没有）：`draft-c52-05`（problem 的 `\text{其余}`）、`draft-c46-03`（answer 的 `\text{唯一最近}` ×2）、`draft-c09-04`（answer 的 `\text{或}`）；
  - 另 2 题原始草稿已有、本次未清：`draft-c51-03`（solution `\text{患病}` ×2）、`draft-c45-03`（solution + scene_spec `\text{两枚皆正}` 等 ×6）。
- **系统性格式回归 180 题**：本次修改把 `scene_spec.steps` 的"第N步"前缀全部去掉（原始草稿 264/264 都带前缀，修改后 180 题缺失；批次 09–18 全量、批次 02–08 部分）。
- **系统级 quarantine**：`P002`×264（许可证仍为仅内部研究）、`A008`×264（动画未验证）——与草稿状态一致，非新问题。
- **泄漏门禁干净**：264 题与当前训练池、冻结 eval/test 均无精确重叠、无 ≥0.7 近重复。

---

## 1. 范围与基准

| 项 | 内容 |
|---|---|
| 受检集 | `batch-01…18/draft-codex-repair-v1.jsonl`（264 条，23–24 字段/条） |
| 对照集 | 同批 `draft.jsonl`（Claude 原始草稿，264 条） |
| 训练池基准 | `data/v2/train/leakage-isolated-v3-2026-10-05/dataset_{calc,geom,linalg,prob}.jsonl` |
| 评测集基准 | `data/v2/eval/dataset_eval.jsonl`、`data/v2/test/dataset_test.jsonl` |
| 清单基准 | `draft-selection.json`、两个 `delivery-manifest.json`（batch-repair-execution / remaining-batch-audit） |
| 板块分布 | 高等代数 95、数学分析 69、解析几何 55、概率论 45 |
| 只读保证 | 未修改任何草稿、数据与清单；未启动训练、未下载模型、未生成动画 |

---

## 2. 原始文件哈希（SHA256 前 12 位，完整见 `file_hashes.json`）

| 文件 | 字节 | SHA256 前 12 位 |
|---|---:|---|
| `batch-01/draft-codex-repair-v1.jsonl` | — | `5103259cb6bd` |
| `batch-02/draft-codex-repair-v1.jsonl` | — | `24548fa6bd5a` |
| `batch-03` … `batch-18` | — | 见 `file_hashes.json`（18 份草稿 + 18 份原始 + 3 份清单全部登记） |
| 训练池 `leakage-isolated-v3-2026-10-05/dataset_{calc,geom,linalg,prob}.jsonl` | 28056 / 12050 / 21097 / 11845 | 见 `file_hashes.json` |
| 评测集 `v2/{eval,test}/dataset_{eval,test}.jsonl` | 442378 / 200390 | 见 `file_hashes.json` |

> 全部 18 份 Codex 修改版草稿的行尾为 **CRLF**（`S002`×18，info）；其余结构检查无异常（0 解析失败、0 重复键、0 空行）。

---

## 3. 硬伤明细（13 条，涉及 5 题）

| # | 题号（批次） | 代码 | 字段 | 问题 | 归因 |
|---|---|---|---|---|---|
| 1 | `draft-c52-05`（batch-01） | L002 | problem | `\begin{cases}…&\text{其余}\end{cases}` 公式内中文 | **本次修改新引入** |
| 2–3 | `draft-c46-03`（batch-06） | L002 | answer ×2 | `P(A\text{唯一最近})=1/4` 等 | **本次修改新引入** |
| 4 | `draft-c09-04`（batch-08） | L002 | answer | `0\le h\le2,\\4\pi\|h-1\|,&h<0\text{或}h…` | **本次修改新引入** |
| 5–6 | `draft-c51-03`（batch-02） | L002 | solution ×2 | `P(\text{患病}\mid+_1)=…` | 原始已有，未清 |
| 7–12 | `draft-c45-03`（batch-16） | L002 | solution ×3 + scene_spec ×3 | `P(\text{两枚皆正})` 等 | 原始已有，未清 |
| 13 | 集合级 | L010 | — | 汇总：`['draft-c52-05','draft-c46-03','draft-c09-04']` 为修改新引入 | — |

> 按 `DATASET_SCHEMA §5`：`$...$` 内出现中文属**硬伤**（TeX 无 CJK，渲染必失败）；项目在 2026-10-03 也曾以"修复 `\text{中文}` 硬伤隐患"处理同类问题。修法：把中文移到公式外的 Text()，或引入 CJK 字体方案（需与渲染门禁一致）。

---

## 4. 泄漏检测（本次重点）

| 对比对象 | 精确题干重叠 | 最大题干近重复（5-gram Jaccard，set） | ≥0.7 命中 |
|---|---:|---:|---:|
| 当前训练池（leakage-isolated-v3） | **0** | **0.4177**（`draft-c40-02` ↔ `linalg-065`） | 0 |
| 冻结 eval/test | **0** | **0.4186**（`draft-c13-02` ↔ `test-calc-013`） | 0 |
| 草稿集内（264×264） | **0** | **0.4528**（`draft-c03-01` ↔ `draft-c03-05`） | 0 |

- 三张表的最大相似度均显著低于未校准阈值 0.7，**未发现题目泄漏**；轨迹与 Codex 报告"未保留同核心数值变体"的结论一致。
- 说明：阈值 0.7 仍标 UNCALIBRATED（项目 `preflight` 亦以 `near_dup_calibrated` 阻断）；本轮最大 0.4528 可作为校准的负样本参考。

---

## 5. 声明与清单核查

| 检查 | 结果 |
|---|---|
| `admitted=true` 条数 | **0**（264 条全为 false）—— 草稿未冒充已准入 |
| `animation_render_verified=true` 条数 | **0** —— 未冒充动画已验证 |
| `draft_status` | 全为 `CODEX-REPAIR-v1-NOT-ADMITTED`（如实） |
| id 保留 | 与原始草稿 **id 集合与顺序完全一致**（264/264，`V004`） |
| `versioned_id` | 264 个唯一，且均包含原 id |
| `revision_lineage.original_id` | 与 `id` 逐条一致 |
| 内容改动 | **264/264** 条与原始草稿不同（`V005`）——证实"Codex 修改"覆盖全部题目 |
| `draft-selection.json` | 声明总数 264 = 实际 264；`deleted_questions=0`；状态 `DRAFT_ONLY_NOT_TRAINING_ADMISSION`；18 批 sha256 与条数**全部匹配**（无 `V007`/`V008`） |
| 未入库核对 | 264 题的题干与训练池/评测集**无精确重复**，且 `admitted=false` → 未混入当前训练清单 |

---

## 6. 其它检查结果

| 检查 | 结果 |
|---|---|
| 结构（解析/重复键/空行/BOM） | 通过（18 份文件仅 CRLF info） |
| 必需字段与类型 | 通过（0 缺失、0 类型错） |
| 身份唯一性 | 通过（id / versioned_id 均唯一） |
| answer ↔ solution 一致性 | 通过（`C007`×257 为"等价表述/纯文字结论"info，无矛盾型硬伤） |
| LaTeX 其它项 | 公式内全角 0；`L009`×343（`\frac` 单 token，**合法 TeX**，已复核降为 info）、`L007`×154（双上下标，合法 info）、`L008`×1（`^23` 建议加花括号，quarantine） |
| scene_spec 结构 | 通过（264/264 含 objects+steps 非空）；`A005`×180（步骤前缀，见 §3 归因）、`C008`×2（`1/2,y = 1/2,y` 疑似笔误，quarantine，属 `draft-c46-03`） |
| 来源/许可证 | `source=self-authored`（`P003`×264 info）；`license=Internal-Research-Use-Only`（`P002`×264 quarantine，训练/公开前须转正） |
| 动画验证 | 264/264 未验证（`A008`，scene_spec 缺 code/render_status/code_sha256） |

---

## 7. 逐条问题清单

### 7.1 hard（13 条，5 题）：见 §3

### 7.2 quarantine（713 条）

| 代码 | 条数 | 内容 | 处置 |
|---|---:|---|---|
| `P002` | 264 | 许可证仅内部研究 | 用户级：转正后方可用于训练/公开 |
| `A008` | 264 | 动画未验证 | 过 `render_gate` 后登记 |
| `A005` | 180 | steps 缺"第N步"前缀（本次修改引入） | 统一编号后重出批次 |
| `C008` | 2 | `draft-c46-03` 出现重复等式 `1/2,y = 1/2,y` | 人工核对笔误 |
| `L008` | 1 | `draft-c07-01` scene_spec `^23` 多位数字上标未加花括号 | 建议 `^{23}` |
| `L011` | 1 | 2 题的公式内中文原始已有、本次未清 | 与 §3 一并修 |
| `V010` | 1 | 180 题步骤前缀丢失（集合级登记） | 同 `A005` |

### 7.3 info（1042 条）

| 代码 | 条数 | 内容 |
|---|---:|---|
| `P003` | 264 | `source=self-authored` |
| `C007` | 257 | answer 与 solution 为等价表述/纯文字结论（正常） |
| `L009` | 343 | `\frac` 单 token 参数（合法 TeX，复核降级） |
| `L007` | 154 | 双上下标（合法） |
| `S002` | 18 | 草稿文件为 CRLF 行尾 |
| `X003` | 2 | 与训练池/评测集最大近重复（0.4177 / 0.4186） |
| `X005` | 1 | 草稿集内最大近重复 0.4528 |
| `V004`/`V005`/`V009` | 各 1 | id 全保留 264 / 264 条均有改动 / 清单状态与总数一致 |

---

## 8. 汇总统计

| 项 | 值 |
|---|---|
| 批次 / 记录 | 18 / 264（原始对照 264） |
| 状态 | rejected 5、quarantine 259、clean 0 |
| 严重度 | hard 13、quarantine 713、info 1042 |
| 泄漏 | 训练池 0/0；eval-test 0/0；集内精确 0 |
| 最大近重复 | 训练池 0.4177、评测集 0.4186、集内 0.4528（阈值 0.7，UNCALIBRATED） |
| 板块 | 高等代数 95、数学分析 69、解析几何 55、概率论 45 |
| 准入声明 | admitted=true 0、render_verified=true 0 |

---

## 9. 结论与建议

1. **可以进入下一轮修改**：264 题在结构、身份、清单一致性、**泄漏隔离**四项上全部通过；Codex 的修改确实覆盖了全部题目（264/264 均有改动）且未删除题目（0 删除、id 全保留）。
2. **必须修（阻塞准入）**：
   - 5 题的公式内中文（`draft-c52-05`、`draft-c46-03`、`draft-c09-04` 为**本次新引入**，须回退/移出公式；`draft-c51-03`、`draft-c45-03` 为历史遗留）；
   - 180 题的 `steps` 前缀统一（本次修改丢前缀，原始草稿 264/264 均带前缀）。
3. **建议核对**：`draft-c46-03` 的重复等式、`draft-c07-01` 的 `^23` 上标。
4. **用户级前置**：许可证转正（264 条）与动画验证（264 条）仍为 quarantine；这两项与草稿是否准入无关的既有约束。
5. **门禁建议**：本轮最大近重复 0.4528/0.4177/0.4186 均远低于 0.7，可作为阈值校准的负样本；`preflight` 的 `near_dup_calibrated` 仍是整体 NOT READY 的阻断项之一。

---

## 10. 产物清单

| 路径 | 内容 |
|---|---|
| `dataset_audit_2026-10-05-codex-drafts/AUDIT_REPORT.md` / `.pdf` | 本报告 |
| `dataset_audit_2026-10-05-codex-drafts/issues.jsonl` | 逐条问题（1768 条） |
| `dataset_audit_2026-10-05-codex-drafts/record_status.jsonl` / `.csv` | 264 题逐条状态（批/类别/准入声明/状态） |
| `dataset_audit_2026-10-05-codex-drafts/summary.json` | 汇总（含泄漏、归因、按批统计） |
| `dataset_audit_2026-10-05-codex-drafts/file_hashes.json` / `.sha256` | 受检文件哈希（18 草稿 + 18 原始 + 清单 + 基准池） |
| `tools/draft_audit.py` | 本轮只读检测工具（可复现） |

**声明**：本轮为只读检测，未修改任何草稿、数据、清单或锁；未自动改写公式或 ID；未启动训练、未下载模型、未生成动画。
