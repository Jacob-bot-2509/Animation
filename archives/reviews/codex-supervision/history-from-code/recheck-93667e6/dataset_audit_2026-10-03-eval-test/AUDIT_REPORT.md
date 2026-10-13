# dataset-eval / data-test 预跑检测报告（2026-10-03）

> 工具：`tools/eval_test_audit.py`（纯标准库，只读；复用 `tools/dataset_audit.py` 的结构/一致性/LaTeX/scene_spec/来源许可证检查规则）
> 复现命令：
> `python tools/eval_test_audit.py --out dataset_audit_2026-10-03-eval-test`
> 契约依据：`DATASET_SCHEMA.md`、`EVAL_TEST_PREP.md`；证据：`issues.jsonl`、`summary.json`、`record_status.jsonl/.csv`、`file_hashes.*`
> 项目自带预检（只读）：`python tools/eval_test_prep.py status` / `check --eval data/v1/eval --test data/v1/test --train-dir data/v1/raw`

---

## 0. 结论摘要与裁定

| 维度 | 结果 |
|---|---|
| 检测对象 | `dataset-eval.md`(182224 B, 100 题×≥2 解)、`data-test.md`(118798 B, 150 题)；转出物 `data/v1/eval/dataset_eval.jsonl`(300 条)、`data/v1/test/dataset_test.jsonl`(150 条) 及同名 `.json` 镜像 |
| 样本总量 | **450 条**（eval 300 = 100 题 × 3 解；test 150） |
| 逐条状态 | **rejected 3 / candidate 447 / clean 0** |
| 问题计数 | hard 3、quarantine 2267、info 829（逐条共 3099 条） |
| 结构和字段 | 通过（0 解析失败、0 缺必需字段、0 类型错误、0 重复身份） |
| ID / 身份唯一性 | 通过（eval 300 复合身份唯一；test 150 id 唯一；镜像 63/63、300/300、150/150 一致） |
| 同题多解组约束 | 通过（100 组，每组恰 3 解；同组题干一致、method 唯一、solution_id 唯一） |
| LaTeX 硬性缺陷 | 0（7 条 `\leftarrow` 与 3 条 `\frac32` 经复核为误报，已降为 info） |
| **隔离（train/eval/test）** | **不通过**：eval 与 test 存在 1 题（3 条解法）**近重复 0.7619 ≥ 0.7**；与 train 精确重叠 0、最大近重复 0.5915 < 0.7 |
| manifest 覆盖 | **未登记**（两个 manifest 都只覆盖 `raw/*`） |
| 冻结锁 | **无**（`data/**/*.lock.json` 为空）→ 未冻结 |
| 许可证 | 450/450 `Internal-Research-Use-Only`（训练/公开前须转正） |
| 动画验证 | 0/450 |
| 内容质量（交叉核对） | 既有独立评审 64 条（A 5 / B 31 / C 28）；**其 5 条 A 级在当前 JSONL 中均已改为正确表述**（Lead 逐条复核） |

### 裁定：**NOT READY（fail-closed）——当前不得作为训练/评测数据使用**

必须至少完成以下 3 项才能进入下一步（详见 §9）：

1. **修隔离硬伤**：`eval-linalg-006`（3 条解法）与 `test-linalg-003` 近重复 0.7619，违反"test 题目族不得来自 eval"；
2. **补冻结与登记**：eval/test 未被 manifest 覆盖、无冻结锁——按 `EVAL_TEST_PREP §2` 必须 make_manifest → freeze 后才能用；
3. **同步契约文本**：eval 无 `id` 依赖复合身份，与 `DATASET_SCHEMA §2`（id 缺失＝硬伤）冲突。

---

## 1. 检测范围与只读保证

| 类别 | 文件 |
|---|---|
| 来源手稿（草稿） | `dataset-eval.md`、`data-test.md` |
| 正式入口（本次检测对象） | `data/v1/eval/dataset_eval.jsonl`、`data/v1/test/dataset_test.jsonl` |
| 镜像容器 | `data/v1/eval/dataset_eval.json`、`data/v1/test/dataset_test.json` |
| 训练参考池（隔离基准） | `data/v1/raw/dataset_{calc,geom,linalg,prob}.jsonl`（63 条） |
| 清单 | `data/v1/manifest.json`、`data/v1/manifest-train.json` |
| 说明文档 | `EVAL_TEST_PREP.md`、`data/v1/eval/README.md`、`data/v1/test/README.md` |
| 既有内容评审（交叉核对，非本次产物） | `reviews/2026-10-03-math-review/review-math.md`、`evidence/findings.json` |

> **文件名说明**：用户提到的 `dataset-test.md` 在仓库中的实际文件名是 **`data-test.md`**（内容为 test 题目族，150 题）；本报告按实际文件检测。

只读保证：未修改/创建/删除任何数据或文档；未自动改 ID、未自动改写公式；未启动训练、未下载模型、未生成批量动画。本次仅新增只读检测工具 `tools/eval_test_audit.py` 与输出目录 `dataset_audit_2026-10-03-eval-test/`。

---

## 2. 原始文件哈希（SHA256，本轮快照）

| 文件 | 字节 | 记录数 |
|---|---:|---:|
| `data/v1/eval/dataset_eval.jsonl` | 390335 | 300 |
| `data/v1/eval/dataset_eval.json` | 445240 | 300 |
| `data/v1/test/dataset_test.jsonl` | 175805 | 150 |
| `data/v1/test/dataset_test.json` | 197746 | 150 |
| `dataset-eval.md` | 182224 | 100 题 |
| `data-test.md` | 118798 | 150 题 |
| `data/v1/raw/dataset_{calc,geom,linalg,prob}.jsonl` | 32927 / 18150 / 31025 / 15471 | 19/12/23/9 |
| `data/v1/manifest.json` / `manifest-train.json` | 1604 / 1761 | 4 / 4 entries |

> 完整 SHA256 见 `file_hashes.json` / `file_hashes.sha256`（含 README 与 manifest）。

---

## 3. 预跑门禁逐项结果

| # | 门禁 | 结果 | 证据 |
|---|---|---|---|
| G1 | JSONL 结构（解析/空行/CRLF/重复键） | **通过**（2 条 CRLF info） | S002×2 |
| G2 | 必需字段与类型 | **通过**（0 缺、0 类型错） | F001/F002/F003 = 0 |
| G3 | 身份唯一性（复合身份口径） | **通过** | eval 300、test 150，0 冲突 |
| G4 | 同题多解组约束 | **通过**（100 组×3 解；题干一致、method 唯一） | I002/I003/I005 = 0；G002 |
| G5 | answer 可判分性 | 通过（0 缺失；273 条纯文字结论 info） | C007=273(info) |
| G6 | LaTeX（公式内中文/漏反斜杠/`$`/括号） | **通过**（0 硬性缺陷） | L006/L009 复核为误报 |
| G7 | scene_spec 结构 | **通过**（450/450 含 objects+steps） | A001-A007 = 0 |
| G8 | 来源与许可证 | **条件通过**：许可证待转正 | P002×450(quarantine) |
| G9 | **与 train 隔离** | **通过**：精确 0；最大近重复 0.5915 < 0.7 | X001=0、X002 |
| G10 | **eval 与 test 隔离** | **不通过**：近重复 0.7619 ≥ 0.7 | X005×3（hard） |
| G11 | manifest 登记 | **不通过**：eval/test 均未被登记 | MF006×2 |
| G12 | 冻结锁 | **不通过**：无 `*.lock.json` | MF007×2 |
| G13 | 拆分标签一致性 | **不通过**：同一 raw 文件被标 `raw` 与 `train` 两种 split | MF005×4、MF008 |
| G14 | 文档与数据一致 | **不通过**：文档称"未生成/未转 JSON/未冻结/草稿"而数据已存在 | D004×2、D005×2、D010×3 |
| G15 | 契约与实现一致 | **不通过**：eval 无 `id`，依赖复合身份 | G001 |
| G16 | 元数据完备性 | 不通过（candidate 语义） | F010×1350 |
| G17 | 动画验证 | 不通过（0/450） | A008×450 |

> 项目自带 `tools/eval_test_prep.py check` 报告 **exit 0 通过**（仅 450 项 quarantine 警告）。该结论与 G10 的差异原因见 §4.2。

---

## 4. 隔离检测（本次核心发现）

### 4.1 跨池重叠矩阵

| 池对 | 核心题干精确重叠 | 最大 5-gram Jaccard（set / multiset） | ≥0.7 对数 |
|---|---:|---|---:|
| train ↔ eval | 0 | 0.5915（`linalg-067` vs `eval-linalg-007-s1`） | 0 |
| train ↔ test | 0 | 0.3895（`linalg-067` vs `test-linalg-021`） | 0 |
| **eval ↔ test** | 0 | **0.7619 / 0.7778**（`eval-linalg-006` vs `test-linalg-003`） | **3** |

### 4.2 硬伤明细（3 条，同一题目的 3 个解法）

| eval 记录 | test 记录 | set 口径 | multiset 口径 |
|---|---|---:|---:|
| `eval-linalg-006`-s1/s2/s3 | `test-linalg-003` | 0.7619 | 0.7778 |

- eval 题干：`设 A=[[1,1],[0,1]]，求 A^n`；test 题干：`设 A=[[1,2],[0,1]]，求 A^n` —— **同一模板仅改常数**，属"改数字的同一题"，违反 `EVAL_TEST_PREP §1`"test 题目不得来自 train 或 eval"。
- 3 条记录分别对应 eval 的三种解法（数学归纳法 / 二项式展开 / 若尔当形观点），故 3 行全部命中。
- 阈值 0.7 仍标 **UNCALIBRATED**，但两种口径均 ≥0.76，结论对口径不敏感。

### 4.3 项目自带预检的盲区（需补）

`tools/eval_test_prep.py check` 只在 **候选 vs train** 之间做近重复，**eval 与 test 之间仅比较精确哈希与 ID**（`_group_sets` 只取 `canonical_problem_hash` 与 `record_identity`），因此本次 0.7619 的跨角色近重复**不会被它拦下**。建议把 `ShingleIndex` 也用于 eval↔test 组间比较。

---

## 5. 逐项检查结果

### 5.1 结构与字段
- 4 个文件（2 JSONL + 2 JSON）全部合法；2 条 CRLF 行尾提示（`data-test.md` 及其转出物）。
- eval 11 字段：`problem_id/solution_id/method/category/sub_category/problem/solution/answer/scene_spec/source/license`；test 9 字段：`id/category/sub_category/problem/solution/answer/scene_spec/source/license`。
- 必需字段 0 缺失、0 类型错误；**eval 全部缺 `id`**（见 5.3）。

### 5.2 身份与同题多解
- eval：300 条 = **100 个 problem_id × 恰 3 个解法**；solution_id 全局唯一；同组题干一致、method 唯一（`数学归纳法/二项式展开/若尔当形观点` 等，共 263 个 method 名）。
- test：150 条 id 唯一（`test-calc-001` … `test-x-015`），5 个板块。
- 镜像 `.json` 与 `.jsonl` 内容**逐条一致**（eval 300/300、test 150/150）。
- 与手稿覆盖：`dataset-eval.md` 的 100 个 `### <problem_id>` 与 eval 的 100 个 problem_id 完全对应；`data-test.md` 的 150 个 `### <id>` 与 test 的 150 个 id 完全对应；规模声明与实际一致。

### 5.3 契约分歧（G001）
`DATASET_SCHEMA §2` 把 `id` 缺失列为**硬伤**、§6 称 `problem_id/solution_id/method` 为"预留"；而实现（`record_identity`/`check_record`）已允许"缺 id 但 problem_id+solution_id 齐备"的复合身份。当前 eval 300 条全部走复合身份；若下游按 §2 文本校验会直接判 450 条中 300 条硬伤。**须同步契约文本**。

### 5.4 LaTeX
- 公式内中文/全角 0；`$` 配对 0 异常；`\left/\right`、花括号、重复等式硬性缺陷 0。
- 7 条 `\left`"未配对"**经 Lead 复核为误报**：实为 `\leftarrow`（`$R_k\leftarrow R_k-x_1R_{k-1}$` 等），规则需加字母边界。
- 3 条 `\frac32`/`\dfrac12`**经 Lead 复核为合法 TeX**（单 token 参数可正常渲染），仅为风格建议。
- 86 条 `x_1^2` 类双上下标为 info（合法）。

### 5.5 scene_spec 与动画
- 450/450 均含非空 `objects`（eval 1200 / test 302）与 `steps`（eval 1500 / test 602），步骤编号连续。
- **动画验证 0/450**：无 `code/render_status/code_sha256` → 只能标 candidate/UNVERIFIED（`DATASET_SCHEMA §7`）。

### 5.6 来源与许可证
- 450/450 `source=self-authored`、`license=Internal-Research-Use-Only`；后者仅限内部研究、不公开分发，训练/公开前须转正（与 train 池同）。
- 可选元数据 `function_family/visual_style/efficiency_tags` **450/450 全缺**（1350 条 quarantine）——与 `reports/2026-10-03-eval-test-intake.md` 的记录一致。

### 5.7 manifest / 冻结 / 拆分标签
- `manifest.json`（4 条，`split=raw`）与 `manifest-train.json`（4 条，`split=train`）**都只覆盖 `raw/*.jsonl`**；eval/test 未登记。
- 同一 4 个文件在两个 manifest 中 split 取值不同（`raw` vs `train`）→ 语义冲突。
- `manifest-train.json` 把 63 条仍为 candidate/UNVERIFIED 的数据标为 `split=train`（notes 自称 provisional）→ 训练语义先于验收，需人工确认。
- **无任何 `*.lock.json`** → eval/test 未冻结；`preflight --ready` 在无冻结时必然 NOT READY（fail-closed）。

### 5.8 文档与数据一致性
| 文档 | 声明 | 实际 | 判定 |
|---|---|---|---|
| `EVAL_TEST_PREP.md §5` | "eval:未生成、未冻结;test:未生成、未冻结" | 300 + 150 条已生成 | quarantine（文档滞后） |
| `data/v1/eval/README.md`、`test/README.md` | "未生成任何 eval/test 样本" | 目录内已有 390 KB / 176 KB JSONL | quarantine |
| `dataset-eval.md`、`data-test.md` | "草稿,供用户审阅""未冻结、未转 JSON/JSONL" | JSONL 已生成并进入预跑检测 | quarantine（需明确内容是否定稿） |

---

## 6. 内容质量交叉核对

- 既有独立评审 `reviews/2026-10-03-math-review/`：**64 条**（A 级 5 / B 级 31 / C 级 28；test 34、eval 30），覆盖 250 个题号。
- **Lead 独立复核 5 条 A 级在当前 JSONL 中的状态：全部已修正**：

| A 级项 | 原问题 | 当前数据 |
|---|---|---|
| `test-prob-002` | 精确值少一位（0.149308346） | 现为 `0.1493083459`（=1493083459/10¹⁰，且解答给出分数形式） |
| `eval-calc-006` | 反函数写成 `x=a\sinh y`（仅 a=1 成立） | 现为 `x=a\sinh(y-\ln a)=(e^y-a^2e^{-y})/2`，Lead 用 `e^{2y}-2xe^y=a^2` 复算一致 |
| `eval-linalg-023` | 声称 `x^4+1` 在 ℝ 不可约 | 现给出 `(x^2-\sqrt2x+1)(x^2+\sqrt2x+1)=x^4+1`，并用平方差连接两解法 |
| `test-linalg-021` | 反射轴 `y=x\tan(\theta/2)` 漏竖直情形 | 现明确 `θ=(2k+1)π` 时为竖直轴，并说明 tan 不存在 |
| `test-x-011` | "两反射复合是旋转"未限定 | 题面已限定"过原点的线性反射"，解法补"平行轴→平移"的边界说明 |

- Lead 另按 34 个关键标记扫描 B/C 级问题（如 `0^0`、`左端点`、`16/4`、`A=J'⊗`、`291.67` 等）：当前 JSONL 中对应错误文本**已不存在或已被正确表述取代**（`test-linalg-018` 的幂等最小多项式已限定为"本题给定矩阵"）。
- 残余风险：既有评审针对的是早期 PDF 稿，当前 JSONL 晚于该稿；本轮为机械/门禁预检 + 抽样复核，**未对 250 题的当前文本做逐题重审**。建议在冻结前做一次回归评审。

---

## 7. 逐条问题清单

### 7.1 硬伤（3 条）

| # | 文件:定位 | 身份 | 代码 | 问题 |
|---|---|---|---|---|
| 1 | `data/v1/eval/dataset_eval.jsonl:211` | `eval-linalg-006::eval-linalg-006-s1` | X005 | 与 `test-linalg-003` 跨池近重复 0.7619（多重集 0.7778）≥0.7 |
| 2 | `data/v1/eval/dataset_eval.jsonl:212` | `…-s2` | X005 | 同上 |
| 3 | `data/v1/eval/dataset_eval.jsonl:213` | `…-s3` | X005 | 同上 |

### 7.2 quarantine（2267 条，按代码）

| 代码 | 条数 | 内容 |
|---|---:|---|
| F010 | 1350 | 可选元数据缺/空（function_family/visual_style/efficiency_tags × 450） |
| A008 | 450 | 动画未验证（scene_spec 无 code/render_status/code_sha256） |
| P002 | 450 | license=Internal-Research-Use-Only，训练/公开前须转正 |
| MF005 | 4 | 同一文件在 manifest 中 split 取值冲突（raw vs train） |
| D010 | 3 | 文档声明 eval/test 未生成，实际已有 450 条 |
| MF006 | 2 | eval/test 未被任何 manifest 登记 |
| MF007 | 2 | eval/test 无冻结锁 |
| D004 | 2 | 手稿自称"未冻结、未转 JSON/JSONL"，实际已生成 |
| D005 | 2 | 手稿状态为"草稿"，数据已用于预跑检测 |
| MF008 | 1 | 63 条 candidate/UNVERIFIED 被标为 split=train |
| G001 | 1 | eval 无 id 依赖复合身份，与 DATASET_SCHEMA §2/§6 文本冲突 |

### 7.3 info（829 条，按代码）

| 代码 | 条数 | 内容 |
|---|---:|---|
| C007 | 273 | answer 与 solution 无文本重合（纯文字结论，正常） |
| P003 | 450 | source=self-authored（如实） |
| L007 | 86 | 双上下标（`x_1^2`，合法） |
| L006 | 7 | `\leftarrow` 误判为未配对（Lead 复核：误报） |
| L009 | 3 | `\frac32` 单 token 参数（Lead 复核：合法 TeX） |
| X002 | 3 | 各池对最大近重复（train↔eval 0.5915、train↔test 0.3895、eval↔test 0.7619） |
| C008 | 1 | `A^2=A` 恒等演示被疑似重复等式（Lead 复核：误报） |
| M002 | 2 | `.json` 数组容器不得作入口（本仓库仅作镜像；入场工具只选 `*.jsonl`） |
| S002 | 2 | CRLF 行尾 |
| G002 | 1 | eval 同题多解组 100 组，解法数分布 {3: 100} |
| R001 | 1 | 既有内容评审 64 条（A5/B31/C28）已纳入交叉核对 |

---

## 8. 汇总统计

| 项 | eval | test | 合计 |
|---|---:|---:|---:|
| 记录数 | 300 | 150 | **450** |
| 唯一身份 | 300 | 150 | 450 |
| 题目数 / 组 | 100（每题 3 解） | 150 | 250 |
| 子类数 | 41 | 144 | — |
| objects / steps | 1200 / 1500 | 302 / 602 | 1502 / 2102 |
| 状态 | rejected 3 / quarantine 297 | quarantine 150 | **rejected 3 / quarantine 447 / clean 0** |
| 动画验证 | 0 | 0 | **0** |

- 板块分布：eval（高代 105 / 数分 90 / 几何 60 / 概率 45，按解法计）；test（数分 45 / 高代 40 / 几何 25 / 概率 25 / 跨学科 15）。
- 严重度：hard 3、quarantine 2267、info 829。
- 来源手稿↔交付：eval 100/100、test 150/150 身份完全对应；镜像 450/450 一致。

---

## 9. 能否成为训练（评测）数据的裁定

**结论：NOT READY（fail-closed）。** 450 条在结构、字段、身份、多解组、LaTeX、scene_spec 层面已达标，但以下 6 类阻断项必须先解决：

| # | 阻断项 | 级别 | 处理 |
|---|---|---|---|
| 1 | eval↔test 近重复 0.7619（`eval-linalg-006` ↔ `test-linalg-003`） | **hard** | 人工改题或改 test 题目族；并给 `eval_test_prep.py check` 补 eval↔test 近重复检查 |
| 2 | eval/test 未冻结、未登记 manifest | quarantine | make_manifest → freeze（用户批准后经 freeze_data）；否则 preflight 恒 NOT READY |
| 3 | DATASET_SCHEMA 与实现的身份口径分歧 | quarantine | 更新契约：写明多解样本复合身份 |
| 4 | 文档滞后（"未生成/未转 JSON/未冻结/草稿"） | quarantine | 更新 `EVAL_TEST_PREP.md`、两个 README、两份手稿状态 |
| 5 | 450/450 缺可选元数据、0/450 动画验证、许可证待转正 | quarantine | 补齐元数据 → render_gate 验证 → 许可证转正 |
| 6 | 既有 64 条内容评审的回归复核 | 建议 | 冻结前对当前 JSONL 逐题复核（本轮已完成 A 级 5 条 + 抽样） |

**可以直接使用的部分**：本轮检测产物（`issues.jsonl` 等）可作为修复清单；`tools/eval_test_prep.py status` 的"未冻结"结论与本次一致。

**不建议**：在修掉第 1 项并把 eval/test 冻结前，把这两份数据当作评测集或训练数据使用；也不要把 `manifest-train.json` 的 `split=train` 当作验收通过。

---

## 10. 产物清单

| 文件 | 内容 |
|---|---|
| `AUDIT_REPORT.md` / `AUDIT_REPORT.pdf` | 本报告 |
| `issues.jsonl` | 逐条问题（3099 条） |
| `record_status.jsonl` / `.csv` | 450 条逐条状态（含 split/身份/状态/计数） |
| `summary.json` | 汇总统计（含隔离矩阵、镜像一致性、既有评审计数、冻结锁） |
| `file_hashes.json` / `.sha256` | 12 个受检文件哈希 |
| `tools/eval_test_audit.py` | 本次只读检测工具（可复现） |

**声明**：本报告为只读预跑检测，未修改任何数据集、文档或 manifest；未自动改 ID、未自动改写公式；未启动训练、未下载模型、未生成动画。
