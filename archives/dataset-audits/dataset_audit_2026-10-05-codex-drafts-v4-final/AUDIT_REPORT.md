# Codex 修改版草稿 · v4-final 复检报告（2026-10-05 · 第三轮）

> 对象：账本 `draft-selection.json` 当前选中的 **`codex-repair-v4-final`**（18 批 / 264 题）
> `reviews/2026-10-05-training-diversity-drafts/batch-01…18/draft-codex-repair-v4-final.jsonl`
> 基准：训练池 `data/v2/train/leakage-isolated-v3-2026-10-05`、冻结 `data/v2/{eval,test}`
> 工具：`tools/draft_audit.py`（只读；本轮同时跑 v1/v2/v3/v4-final 做版本对照）
> 复现命令：
> `python tools/draft_audit.py --out dataset_audit_2026-10-05-codex-drafts-v4-final --drafts "reviews/2026-10-05-training-diversity-drafts/batch-*/draft-codex-repair-v4-final.jsonl" --pool data/v2/train/leakage-isolated-v3-2026-10-05 --eval-test data/v2/eval/dataset_eval.jsonl --eval-test data/v2/test/dataset_test.jsonl`
> 历史：`…-codex-drafts/`（v1 初检, hard 13）、`…-codex-drafts-v2/`（修复后复核, hard 0）

---

## 0. 结论摘要

| 版本 | hard | quarantine | info | rejected | 说明 |
|---|---:|---:|---:|---:|---|
| `codex-repair-v1`（恢复原件） | **13** | 875 | 1063 | 5 | 原件含公式内中文 12 处、步骤前缀缺 180 题、`E002`（`??`）165 处 |
| `codex-repair-v2` | 0 | 693 | 1044 | 0 | 修完 CJK + 步骤前缀；`E002`×165 尚存 |
| `codex-repair-v3` | 0 | 528 | 1044 | 0 | ready-field-patches 81 条 + `??` 串修复 → `E002` 归零 |
| **`codex-repair-v4-final`（账本选中）** | **0** | **528** | 1062 | **0** | 内容与 v3 **逐字段一致**，仅重盖版本/状态字段 |

### 裁定：**v4-final 内容层通过（hard 0）**；剩余 528 条 quarantine 全为系统级/用户级

- 264 题：**公式内中文 0**、**步骤前缀 1172/1172 合规**、**编码损坏（E001/E002/E003）0**、**id 与顺序 100% 保留**、**泄漏 0**。
- 剩余：`P002`×264（许可证仅内部研究）、`A008`×264（动画未验证）——均与题目内容无关。
- **本轮新发现 2 项**（见 §5）：① 审计工具的"账本哈希核对"对 v4-final **恒被判为"非选中版本"而跳过**（我改用人工核对 18/18 通过）；② v4-final 为 **CRLF**，而 `.gitattributes` 声明 `*.jsonl eol=lf`，账本 sha256 绑定 CRLF 字节 → **全新 clone 后账本哈希全部失效**。

---

## 1. 对象、基准与只读保证

| 项 | 内容 |
|---|---|
| 受检集（账本选中） | `batch-01…18/draft-codex-repair-v4-final.jsonl`（264 条，22–23 字段/条） |
| 对照版本 | 同批 `draft-codex-repair-v1/v2/v3.jsonl`；原始草稿 `draft.jsonl` |
| 训练池基准 | `data/v2/train/leakage-isolated-v3-2026-10-05/dataset_{calc,geom,linalg,prob}.jsonl` |
| 评测集基准 | `data/v2/eval/dataset_eval.jsonl`、`data/v2/test/dataset_test.jsonl` |
| 账本 | `draft-selection.json`（`updated_by=codex-mail-repair-final-2026-10-05`，`selected_drafts=264`，`version=codex-repair-v4-final`） |
| 只读保证 | 未修改任何草稿、数据、账本或工具；未启动训练、未下载模型、未生成动画 |

---

## 2. 账本哈希与文件（人工核对，18/18）

| 批次 | 条数 | 账本 sha256 = CRLF 字节 | 账本 sha256 = LF 归一化 |
|---|---:|---|---|
| batch-01…18（全部） | 15/15/…/10（合计 264） | **匹配 18/18** | **不匹配 18/18** |

- 结论：账本绑定的是**当前工作区 CRLF 字节**；由于 `.gitattributes` 声明 `*.jsonl text eol=lf`，全新 clone 得到的 LF 文件 sha256 会变化（见 §5.2）。

---

## 3. v4-final 验收结果（0 hard）

| 检查 | 结果 |
|---|---|
| 结构（解析/重复键/空行/BOM） | 通过（18 份文件 CRLF，`S002`×18 info） |
| 必需字段与类型 | 通过（0 缺失、0 类型错） |
| 身份 | 264 个 `id` 唯一、264 个 `versioned_id` 唯一；与原始草稿 id 集合与顺序完全一致 |
| 内容（problem/solution/answer/scene_spec） | **与 v3 逐字段一致（0/264 差异）**；无公式内中文、无编码损坏 |
| 步骤前缀 | 1172 步 **100%** 以"第N步"开头（`A005`/`V010`=0） |
| 编码 | `E001`（U+FFFD）=0、`E002`（`??`）=0、`E003`（控制字符）=0 |
| answer ↔ solution | 通过（`C007`×257 为等价表述/纯文字结论 info） |
| LaTeX 其它 | `L009`×343（`\frac` 单 token，合法）、`L007`×154（双上下标，合法）、`C008`/`L008`（复核为误报，info） |
| 泄漏（训练池） | 精确 0；最大题干近重复 **0.4177**（`draft-c40-02` ↔ `linalg-065`） |
| 泄漏（冻结 eval/test） | 精确 0；最大 **0.4186**（`draft-c13-02` ↔ `test-calc-013`） |
| 集内重复 | 精确 0；最大 **0.4528**（`draft-c03-01` ↔ `draft-c03-05`） |
| 准入声明 | `admitted=true` **0**；`animation_render_verified=true` **0** |
| 状态字段 | `draft_status` 全为 `CODEX-REPAIR-v4-final-NOT-ADMITTED`；`review_status` 全为 `CODEX_MATH_REVIEW_COMPLETE_PENDING_VERSION_BOUND_ACCEPTANCE`；`strict_review.user_review_new_version` 全为 `DELEGATED_TO_CODEX_COMPLETED` |
| 来源/许可证 | `source=self-authored`（`P003`×264 info）；`license=Internal-Research-Use-Only`（`P002`×264 quarantine） |
| 动画 | 264/264 未验证（`A008`） |

---

## 4. 版本演进（本轮四版并跑）

| 项 | v1 | v2 | v3 | **v4-final** |
|---|---:|---:|---:|---:|
| hard | 13 | 0 | 0 | **0** |
| rejected 题数 | 5 | 0 | 0 | **0** |
| 公式内中文（`L002`） | 12 处 | 0 | 0 | **0** |
| 步骤前缀缺失（`A005`） | 180 | 0 | 0 | **0** |
| 编码 `E002`（`??`） | 165 | 165 | **0** | **0** |
| quarantine | 875 | 693 | 528 | **528** |
| 内容字段与前一版差异 | — | CJK 5 题 + 前后缀 180 题 | ready-field-patches 81 条 + `??` 修复 | **内容 0 处**（仅版本/状态字段 264 题） |

> v4-final 相对 v3 的差异字段：`draft_status`/`versioned_id`/`revision_lineage`/`strict_review`（各 264 题）、`review_status`（119 题）；**题目内容零改动**。即：81 条 ready-field-patches 落在 v3，v4-final 是"版本盖戳"。

---

## 5. 本轮新发现（Lead 独立复核）

### 5.1 `V011`×18：审计工具的"账本哈希核对"被跳过（工具缺陷）

- 现象：18 条 `V011` info，内容形如
  「被审文件 `reviews/…/batch-01/draft-codex-repair-v4-final.jsonl` 不是账本选中版本(`batch-01/draft-codex-repair-v4-final.jsonl`)，跳过哈希核对」——两串路径指向**同一个文件**，判断恒为真。
- 后果：本次运行的 `V007`（哈希不符）/`V008`（条数不符）**全部未执行**；若账本哈希或条数有问题，工具会静默放过。
- 补偿措施：我改用人工核对账本 18 条 → **18/18 哈希匹配、条数匹配**（§2），故本次无漏判；但该守卫当前处于**失效状态**，建议修复（用 `path` 归一化后比较，或直接比较被审文件的相对路径与账本 `path`）。

### 5.2 CRLF 与账本哈希绑定（复现性风险）

- 18 份 v4-final 均为 **CRLF**；账本 sha256 = CRLF 字节；`.gitattributes` 为 `*.jsonl text eol=lf`。
- 后果：全新 clone/checkout 后文件变 LF → 账本 sha256 **全部失效**，"版本绑定"门禁（`PENDING_VERSION_BOUND_ACCEPTANCE` 依赖的哈希）无法复现。这与 2026-10-03 在 `data/` 侧修复过的同类问题（`W001`）一致。
- 建议：把草稿落盘改为 LF 并重绑账本哈希，或对草稿模式声明 `-text` 固定字节。

### 5.3 其它

- `S002`×18（CRLF）已在上条覆盖；`X003`/`X005` 三张相似度表数值与上一轮完全一致（题目内容未变）。

---

## 6. 逐条问题清单

### 6.1 hard：**0**

### 6.2 quarantine（528 条）

| 代码 | 条数 | 内容 | 处置 |
|---|---:|---|---|
| `P002` | 264 | `license=Internal-Research-Use-Only` | 用户级：训练/公开前转正 |
| `A008` | 264 | 动画未验证（无 `code`/`render_status`/`code_sha256`） | 用户级：过 `render_gate` 后登记 |

### 6.3 info（1062 条）

| 代码 | 条数 | 内容 |
|---|---:|---|
| `L009` | 343 | `\frac` 单 token（合法 TeX） |
| `P003` | 264 | `source=self-authored` |
| `C007` | 257 | answer 与 solution 等价表述/纯文字结论 |
| `L007` | 154 | 双上下标（合法） |
| `S002` | 18 | CRLF 行尾（见 §5.2） |
| `V011` | 18 | 账本核对被跳过（见 §5.1） |
| `X003`/`X005` | 2/1 | 与训练池 0.4177 / eval-test 0.4186 / 集内 0.4528 |
| `C008`/`L008` | 2/1 | 复核为误报（三条直线枚举 / `\sin^23\theta`） |
| `V004`/`V005`/`V009` | 各 1 | id 全保留 264 / 264 条均有改动 / 账本状态与总数一致 |

---

## 7. 汇总统计

| 项 | 值 |
|---|---|
| 版本 / 批次 / 记录 | `codex-repair-v4-final` / 18 / 264 |
| 状态 | rejected **0**、quarantine 264、clean 0 |
| 严重度 | hard **0**、quarantine 528、info 1062 |
| 泄漏 | 训练池 0；eval-test 0；集内精确 0（最大 0.4177 / 0.4186 / 0.4528） |
| 内容改动（相对 v3） | 0 处 |
| 声明 | admitted=true 0、render_verified=true 0 |
| 账本 | 18/18 哈希与条数匹配（CRLF 字节口径） |

---

## 8. 裁定与建议

1. **v4-final 内容层通过**：0 hard、0 编码损坏、0 泄漏、id 全保留、声明如实；相比 v1（13 hard）与 v2（165 处 `??`）是当前最优版本。
2. **采纳前建议先修两处工程问题**：
   - **§5.1 工具守卫**：`V011` 使账本哈希核对失效——修复后再跑一次，让 `V007/V008` 真正生效；
   - **§5.2 行尾/哈希**：把 18 份草稿改为 LF 并重绑账本 SHA（或声明 `-text`），否则 clone 后"版本绑定"不可复现。
3. **仍然的用户级前置**：`P002` 许可证转正、`A008` 动画验证（`preflight --ready` 另有 `asset_evidence`/`near_dup_calibrated`/`exec_isolation` 阻断）。
4. **准入口径提示**：v4-final 的 `review_status` 为 `…PENDING_VERSION_BOUND_ACCEPTANCE`，即**待用户批准版本绑定**——与本裁定一致。

---

## 9. 产物清单

| 路径 | 内容 |
|---|---|
| `dataset_audit_2026-10-05-codex-drafts-v4-final/AUDIT_REPORT.md` / `.pdf` | 本报告 |
| `dataset_audit_2026-10-05-codex-drafts-v4-final/issues.jsonl` | 逐条问题（1590 条） |
| `dataset_audit_2026-10-05-codex-drafts-v4-final/record_status.jsonl` / `.csv` | 264 题逐条状态 |
| `dataset_audit_2026-10-05-codex-drafts-v4-final/summary.json` | 汇总 |
| `dataset_audit_2026-10-05-codex-drafts-v{1,2,3}/` | 三个对照版本的检测输出 |
| `tools/draft_audit.py` | 只读检测工具 |

**声明**：本轮为只读复检，未修改任何草稿、数据、账本或工具；未自动改写公式或 ID；未启动训练、未下载模型、未生成动画。
