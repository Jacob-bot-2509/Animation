# dataset-eval / data-test 预跑检测报告（第二轮 · 2026-10-03）

> 工具：`tools/eval_test_audit.py`（纯标准库，只读；复用 `tools/dataset_audit.py` 的结构/一致性/LaTeX/scene_spec/来源许可证规则，并新增冻结锁校验、manifest 条目契约、EOL 哈希绑定、元数据卫生检查）
> 复现命令：
> `python tools/eval_test_audit.py --out dataset_audit_2026-10-03-eval-test-v2`
> 项目自带预检（只读）：`python tools/eval_test_prep.py check --eval data/v1/eval --test data/v1/test --train-dir data/v1/raw` → **exit 0**
> 契约依据：`DATASET_SCHEMA.md`、`EVAL_TEST_PREP.md`；证据：`issues.jsonl`、`summary.json`、`record_status.jsonl/.csv`、`file_hashes.*`
> 上一轮（第一轮）：`dataset_audit_2026-10-03-eval-test/`（裁定 NOT READY，hard 3）

---

## 0. 结论摘要与裁定

| 维度 | 本轮（第二轮） | 上一轮 |
|---|---|---|
| 样本总量 | **450 条**（eval 300 = 100 题×3 解；test 150） | 同 |
| 逐条状态 | **rejected 0 / quarantine 450 / clean 0** | rejected 3 / quarantine 447 |
| 问题计数 | **hard 0**、quarantine 1364、info 833（共 2197） | hard 3、quarantine 2267、info 829 |
| 结构 / 字段 / 类型 | 通过 | 通过 |
| 身份唯一性 | 通过（eval 300 唯一 id + 100 组多解；test 150 唯一） | eval 无 id |
| 同题多解组约束 | 通过（100 组×恰 3 解） | 通过 |
| LaTeX 硬性缺陷 | 0（公式内 CJK/全角全量扫描命中 0） | 0 |
| **与 train 隔离** | **通过**：精确重叠 0；最大近重复 **0.5915** < 0.7 | 通过 |
| **eval ↔ test 隔离** | **通过**：精确重叠 0；最大近重复 **0.6667** < 0.7；≥阈值对数 **0** | **不通过**（0.7619，3 条） |
| manifest 登记 | 通过（根 manifest 6 条，含 eval/test） | 未登记 |
| 冻结锁 | **已建立**（2 个锁，绑定根 manifest，条目哈希校验通过） | 无锁 |
| 元数据完备性 | 513/513 齐全（eval/test/train 全部补齐） | 450/450 缺 |
| 文档与数据一致 | 仅剩"未冻结"字样滞后 | 多处不符 |

### 裁定：**硬门禁通过（CONDITIONAL PASS）——可进入用户裁定/补齐阶段，但仍不能直接投入训练或评测**

- 上一轮的 **3 项 hard 全部清零**：跨池近重复题已拆题、eval 已补全局唯一 id、manifest 已顶层登记，隔离与冻结两项硬门禁成立。
- 仍有 **6 类 quarantine（1364 条）**，其中 **4 项建议投用前必须处理**（§9）：哈希/EOL 不可复现（5）、manifest 条目契约（4）、元数据批量残留（450）、文档状态滞后（5）；另 2 项为已知的用户级决策（动画未验证 450、许可证待转正 450）。

---

## 1. 检测范围、快照与只读保证

| 类别 | 文件（本轮快照时间按文件 mtime） |
|---|---|
| 正式入口（检测对象） | `data/v1/eval/dataset_eval.jsonl`(18:53:57)、`data/v1/test/dataset_test.jsonl`(18:53:57) |
| 镜像容器 | `data/v1/eval/dataset_eval.json`、`data/v1/test/dataset_test.json` |
| 来源手稿 | `dataset-eval.md`(18:42:58)、`data-test.md`(18:42:58) |
| 训练参考池（隔离基准） | `data/v1/raw/dataset_{calc,geom,linalg,prob}.jsonl`（63 条，01:23–01:57） |
| 清单 | `data/v1/manifest.json`(18:54:32)、`manifest-train.json`(18:53:57)、`data/v1/{eval,test}/manifest.json`(18:54:32) |
| 冻结锁 | `data/eval-v1.lock.json`、`data/test-v1.lock.json`(18:59:05) |
| 规则文件 | `.gitattributes`(18:41:33) |

> **并发说明**：本轮开始时锁文件位于 `data/v1/{eval,test}/dataset_*.lock.json`，检测过程中（18:59:05）被移动到 `data/{eval,test}-v1.lock.json`；随后 19:01:57 根清单 `data/v1/manifest.json` 被重生成（eval/test 条目的备注由"未冻结"改为"已冻结(data/{eval,test}-v1.lock.json 绑定本清单)"），两个锁同步重绑到新清单哈希 `636d4902…`。**本报告以 19:03:35 的最终快照为准**，全部哈希见 `file_hashes.json`。
> **文件名说明**：`dataset-test.md` 在仓库中的实际文件名为 `data-test.md`。
> 只读保证：未修改任何数据/文档/manifest/锁；未自动改 ID 或公式；未启动训练、未下载模型、未生成动画。

---

## 2. 原始文件哈希（SHA256，本轮快照）

| 文件 | 字节 | mtime | SHA256（前 12 位） |
|---|---:|---|---|
| `data/v1/eval/dataset_eval.jsonl` | 465152 | 18:53:57 | `9e5b7355606d` |
| `data/v1/test/dataset_test.jsonl` | 201290 | 18:53:57 | `e1ba1eb49dd7` |
| `data/v1/eval/dataset_eval.json` | 524255 | 18:53:57 | `f75bcf5dabe1` |
| `data/v1/test/dataset_test.json` | 224609 | 18:53:57 | `0e02da48040b` |
| `dataset-eval.md` / `data-test.md` | 182347 / 118654 | 18:42:58 | `6fd913bc89d8` / `342e6d0e4d49` |
| `data/v1/manifest.json` | 2635 | 19:01:57 | `636d4902d001` |
| `data/v1/manifest-train.json` | 2105 | 18:53:57 | `eb630bc1dc3d` |
| `data/v1/eval/manifest.json` / `test/manifest.json` | 1226 / 1226 | 18:54:32 | `cef290f0e32f` / `6a6604d1ce74` |
| `data/eval-v1.lock.json` / `data/test-v1.lock.json` | 485 / 485 | 19:01:57 | `a3f1c17ca6a6` / `c2394c7b4735` |
| `data/v1/raw/dataset_{calc,geom,linalg,prob}.jsonl` | 32927 / 18150 / 31025 / 15471 | 01:23 / 01:23 / 01:57 / 01:57 | `65d9c9255cd6` / `109d993d8dfd` / `2fa2a95de269` / `254626ccd2f1` |
| `.gitattributes` | 92 | 18:41:33 | `a2dc85e2442c` |

> 共 19 个受检文件，完整哈希见 `file_hashes.json` / `file_hashes.sha256`。**最终快照时间 19:03:35**；检测跑完后立即复核，19 个文件全部未再变动。

---

## 3. 与第一轮（NOT READY）的差异

### 3.1 上一轮 3 项 hard：全部清零

| 上一轮 hard | 本轮状态 | 证据 |
|---|---|---|
| `eval-linalg-006`(×3 解) ↔ `test-linalg-003` 近重复 0.7619 | **已修复** | `test-linalg-003` 已换题（现为"求所有满足 $B^2=A$ 的二阶实矩阵"，Lead 手算 $B=\pm\begin{pmatrix}1&1\\0&1\end{pmatrix}$，$B^2=A$ 且由与 $A$ 交换 + $p^2=s^2=1,q(p+s)=2$ 证唯一）；与该题相似度降至阈值以下 |
| eval 无 `id`，与 `DATASET_SCHEMA §2`「id 缺失＝硬伤」冲突 | **已修复** | eval 300 条均有唯一 `id`（`eval-calc-001-s1` … `eval-linalg-035-s3`），与 test/train 无交集 |
| eval/test 未被 manifest 登记、无冻结锁 | **已修复** | 根 manifest 6 条（train×4 + eval + test）；锁 2 个并绑定根 manifest 哈希 |

### 3.2 上一轮 quarantine：已清除 10 类

- `F010` 可选元数据缺/空 **1350 → 0**（eval 300 + test 150 + train 63 全部补齐 function_family / visual_style / efficiency_tags）；
- `S002` CRLF 行尾 **2 → 0**（eval/test JSONL 已 LF 化，`.gitattributes` 声明 `*.jsonl/*.json eol=lf`）；
- `MF006` 未登记 **2 → 0**、`MF007` 无冻结锁 **2 → 0**、`MF004` manifest 哈希不符 **0**；
- `G001` 契约分歧 **1 → 0**（eval 有 id）；`D004`/`D005`/`D010` 文档"未生成/未转 JSON"字样已更新；
- 根清单**（检测期间修复）** 19:01:57 重生成：eval/test 条目备注由"未冻结"改为"已冻结(…lock.json 绑定本清单)"，两个锁同步重绑到 `636d4902…`，锁校验仍通过；
- 镜像一致性保持（eval 300/300、test 150/150 与 JSONL 逐条相同）。

### 3.3 本轮新增发现（上一轮不存在或未检出）

| 代码 | 条数 | 内容 |
|---|---:|---|
| `F011` | 450 | efficiency_tags 条目残留 Markdown 项目符号 `"- "`（批量写入残留） |
| `W001` | 5 | 记录哈希绑定 CRLF，而 `.gitattributes` 声明 `eol=lf` → 全新 clone 后校验失败 |
| `MF005` | 2 | 同一文件在根 manifest（`eval`/`test`）与分目录 manifest（`raw`）中 split 取值冲突 |
| `MF009` | 2 | 分目录 manifest 把 JSON 数组容器 `dataset_{eval,test}.json` 登记为数据条目 |
| `D011` | 2 | 两份手稿仍称"未冻结"，但相应冻结锁已建立 |
| `D012` | 3 | `EVAL_TEST_PREP.md` 与两个 README 仍写"未冻结" |
| `MF010` | 2 | 分目录 manifest 把 `README.md` 登记为数据条目（info） |

---

## 4. 硬门禁逐项结果

| # | 门禁 | 结果 |
|---|---|---|
| G1 | JSONL 结构（解析/空行/BOM/重复键） | **通过**（0 异常） |
| G2 | 必需字段、类型、未知字段 | **通过**（0 缺、0 类型错、0 未知字段） |
| G3 | 身份唯一性 | **通过**（eval 300、test 150；跨池无交集） |
| G4 | 同题多解组约束 | **通过**（100 组，每组恰 3 解，题干一致、method 唯一） |
| G5 | answer 可判分性 | 通过 |
| G6 | LaTeX（公式内 CJK/全角/`$`/括号） | **通过**（0 硬性缺陷） |
| G7 | scene_spec 结构 | **通过**（450/450 含 objects+steps） |
| G8 | 镜像一致性 | **通过**（450/450 逐条相同） |
| G9 | 与 train 隔离 | **通过**（精确 0；max 0.5915） |
| G10 | eval↔test 隔离 | **通过**（精确 0；max 0.6667；≥0.7 对数 0） |
| G11 | manifest 登记 | **通过**（根 manifest 含 eval/test） |
| G12 | 冻结锁与哈希绑定 | **通过**（2 锁，均绑定 `data/v1/manifest.json` `6ce669f2…`；条目哈希/大小校验通过） |
| G13 | 元数据完备性 | **通过**（513/513） |
| G14 | 文档与数据一致 | 不通过（"未冻结"字样滞后，5 条） |
| G15 | 哈希可复现性 | 不通过（`W001`×5） |
| G16 | manifest 条目/拆分语义 | 不通过（`MF005`×2、`MF009`×2） |
| G17 | 动画验证 | 不通过（0/450，scene_spec 仍为设计稿） |
| G18 | 许可证 | 不通过（450/450 `Internal-Research-Use-Only`，训练/公开前须转正） |

---

## 5. 隔离检测

| 池对 | 精确重叠 | 最大 5-gram Jaccard（set） | ≥0.7 对数 |
|---|---:|---:|---:|
| train ↔ eval | 0 | 0.5915（`linalg-067` vs `eval-linalg-007-s1`） | 0 |
| train ↔ test | 0 | 0.3895（`linalg-067` vs `test-linalg-021`） | 0 |
| **eval ↔ test** | 0 | **0.6667**（`eval-calc-023-s1` vs `test-calc-013`） | **0** |

- 三对均低于未校准阈值 0.7，隔离判定通过；跨池 ID 交集为空。
- **边界对研判（Lead 复核）**：`eval-calc-023-s1`「证明级数 $\sum 1/n^2$ 收敛」与 `test-calc-013`「求级数 $\sum 1/(n(n+2))$ 的和」——级数不同、任务不同（证明收敛 vs 求和），0.6667 主要来自共用 LaTeX 脚手架，**属结构性相似而非题面泄漏**；但距阈值仅 0.033，建议纳入阈值校准样本。
- **门禁盲区仍未补**：`tools/eval_test_prep.py check` 的 eval↔test 比较仍只用"核心正文哈希 + ID"（`_group_sets`），**未做组间近重复**。本轮 0 泄漏是数据层面的结论，若后续新增题目，该门禁不会拦住 eval↔test 的近似题。上一轮已提出，本轮仍未关闭。

---

## 6. 逐项检查结果

### 6.1 结构与字段
4 个入口/镜像文件全部可解析；0 空行、0 重复键、0 BOM；eval 15 字段（比上一轮多 `id` + 3 项元数据）、test 12 字段；无未知字段。

### 6.2 身份与同题多解
eval：300 条 = 100 个 problem_id × 恰 3 解；`id` 全局唯一（`eval-*-NNN-sM`），`solution_id` 唯一，method 名共 263 个；同组题干一致。test：150 条 `test-*-NNN`（含跨学科 `test-x-*`）唯一。train：63 条不变。三池 ID 两两无交集。

### 6.3 手稿↔交付
`dataset-eval.md` 100 个题号 ↔ eval 100 个 problem_id 完全对应；`data-test.md` 150 个题号 ↔ test 150 个 id 完全对应；规模声明（100/150 题）与实际一致。

### 6.4 LaTeX
全量扫描 450 条 problem/solution/answer 与 scene_spec 的 `$...$` 片段：**公式内中文/全角命中 0**。7 条 `\leftarrow` 误报（`\left` 规则需字母边界）、3 条 `\frac32`（合法单 token）、1 条 `A^2=A` 恒等演示（C008）经复核为误报，均已降为 info。

### 6.5 scene_spec 与动画
450/450 含非空 objects（1203）与 steps（1503），步骤编号连续；**动画验证 0/450**（无 code/render_status/code_sha256）→ 状态只能是 candidate/UNVERIFIED。

### 6.6 来源与许可证
450/450 `source=self-authored`、`license=Internal-Research-Use-Only`；该许可仅限内部研究、不公开分发，训练/公开前必须转正（与 train 池一致）。

### 6.7 manifest 与冻结
- 根 `manifest.json`：6 条（train×4、eval、test），4/4 train 条目标 `train` 且 notes 注明"用户拍板 provisional：candidate 未验收、动画未验证"。
- `manifest-train.json`：4 条（同哈希、同 split），notes 同样注明 provisional → **如实**（本轮降为 info）。
- `data/v1/{eval,test}/manifest.json`：各 3 条，**split 全为 `raw`**，且把 `.json` 数组容器与 `README.md` 登记为数据条目 → 语义/条目契约问题（§7）。
- 冻结锁：`data/eval-v1.lock.json`、`data/test-v1.lock.json`，均 `locked=true`、绑定根 manifest `6ce669f2…`、条目哈希与大小校验通过 → **冻结有效**。

### 6.8 文档状态
`EVAL_TEST_PREP.md`、`data/v1/{eval,test}/README.md`、`dataset-eval.md`、`data-test.md` 仍含"未冻结"字样，而锁已于 18:59 建立 → 5 条 quarantine。

---

## 7. 逐条问题清单

### 7.1 硬伤：**0 条**

### 7.2 quarantine（1364 条，按代码）

| 代码 | 条数 | 内容 | 级别 |
|---|---:|---|---|
| `A008` | 450 | 动画未验证（scene_spec 无 code/render_status/code_sha256） | 已知，需 render_gate |
| `P002` | 450 | `license=Internal-Research-Use-Only`，训练/公开前须转正 | 已知，用户级 |
| `F011` | 450 | efficiency_tags 首条残留 `"- "` 项目符号（批量写入残留） | 建议清理 |
| `W001` | 5 | 记录哈希绑定 CRLF 而 `.gitattributes` 声明 `eol=lf`：4 个 raw JSONL + 根 manifest.json → 全新 clone 后校验失败 | **建议投用前修** |
| `D012` | 3 | `EVAL_TEST_PREP.md`、两个 README 仍写"未冻结" | 文档滞后 |
| `MF005` | 2 | `dataset_eval/test.jsonl` 在根 manifest 标 `eval`/`test`、在分目录 manifest 标 `raw` | **建议投用前修** |
| `MF009` | 2 | 分目录 manifest 把 `.json` 数组容器登记为数据条目（`DATASET_SCHEMA §1`） | **建议投用前修** |
| `D011` | 2 | 两份手稿仍称"未冻结" | 文档滞后 |

### 7.3 info（833 条，按代码）

| 代码 | 条数 | 内容 |
|---|---:|---|
| `P003` | 450 | `source=self-authored`（如实） |
| `C007` | 274 | answer 与 solution 无文本重合（纯文字结论，正常） |
| `L007` | 86 | 双上下标（`x_1^2`，合法） |
| `L006` | 7 | `\leftarrow` 经复核为误报 |
| `L009` | 3 | `\frac32` 合法单 token |
| `X002` | 3 | 三对池的最大近重复（0.5915 / 0.3895 / 0.6667） |
| `M002` | 2 | `.json` 仅作镜像（入场工具只选 `*.jsonl`） |
| `MF010` | 2 | 分目录 manifest 登记 README |
| `LK007` | 2 | 冻结锁校验通过（绑定根 manifest） |
| `C008` | 1 | `A^2=A` 恒等演示经复核为误报 |
| `G002` | 1 | eval 多解组 100 组、解法数分布 {3: 100} |
| `MF008` | 1 | train 标签为"用户拍板 provisional"，notes 已注明未验收（如实） |
| `R001` | 1 | 既有内容评审 64 条（A5/B31/C28）已纳入交叉核对 |

---

## 8. 汇总统计

| 项 | eval | test | 合计 |
|---|---:|---:|---:|
| 记录数 | 300 | 150 | **450** |
| 唯一身份 | 300 | 150 | 450 |
| 题目数 | 100（每题 3 解） | 150 | 250 |
| 子类数 | 41 | 144 | — |
| objects / steps | 1200 / 1500 | 303 / 603 | 1503 / 2103 |
| 状态 | quarantine 300 | quarantine 150 | **rejected 0 / quarantine 450 / clean 0** |
| 动画验证 | 0 | 0 | **0** |

- 板块：eval（高代 105 / 数分 90 / 几何 60 / 概率 45，按解法计）；test（数分 45 / 高代 40 / 几何 25 / 概率 25 / 跨学科 15）。
- 严重度：hard 0、quarantine 1364、info 833（共 2197 条）。
- 隔离：精确重叠 0；≥0.7 近重复 0；最大 0.6667。
- 冻结：2 锁、绑定根 manifest、条目校验通过。

---

## 9. 裁定与建议

### 判定：**硬门禁通过；投用前仍需清 4 项 + 2 项用户级决策**

必须处理（本轮新增，建议优先）：
1. **`W001`（5）哈希可复现性**：raw 4 个 JSONL 与根 `manifest.json` 的记录哈希基于 CRLF，而 `.gitattributes` 声明 `*.jsonl/*.json eol=lf` → 全新 clone 得到 LF 文件后 sha256 变化，`data_check`/冻结锁校验会失败。建议：把落盘改为 LF 后重算并重冻，或对这些文件声明 `-text` 固定字节（eval/test 已是 LF，可作为参照）。
2. **`MF005`+`MF009`（4）manifest 条目与拆分语义**：分目录 manifest 把 eval/test 标成 `raw`、并把 `.json` 数组容器登记为数据条目；建议修正 split 或删除重复清单，只保留根 manifest 作为唯一权威。
3. **`F011`（450）元数据残留**：efficiency_tags 首条以 `"- "` 开头（Markdown 项目符号混入数据），建议清理。
4. **`D011`+`D012`（5）文档状态**：`EVAL_TEST_PREP.md`、两个 README、两份手稿仍写"未冻结"，与 18:59 的冻结事实不符。

用户级决策（已知，非本轮新增）：
5. **动画验证 0/450**：scene_spec 仍为设计稿；进入训练/评测前需过 `render_gate` 并登记 `code/render_status=verified`/`code_sha256`。
6. **许可证**：450/450 为 `Internal-Research-Use-Only`，训练与公开前须转正。

另建议（门禁能力，非数据缺陷）：
7. 给 `tools/eval_test_prep.py check` 补 **eval↔test 近重复比较**（当前只用精确哈希+ID）；并把 5-gram 阈值 0.7 做一次校准（本轮边界对 0.6667 已被判定为结构性相似，可作为校准样本）。

**结论**：本轮相比上一轮的 NOT READY 有实质进展——**隔离、冻结、登记、元数据四项硬门禁全部成立，hard 归零**；剩 4 项属于可机械修复的工程/卫生问题 + 2 项用户级决策。清理完第 1–4 项后，可再次预跑复核并进入冻结批准流程。

---

## 10. 产物清单

| 文件 | 内容 |
|---|---|
| `AUDIT_REPORT.md` / `AUDIT_REPORT.pdf` | 本报告 |
| `issues.jsonl` | 逐条问题（2197 条） |
| `record_status.jsonl` / `.csv` | 450 条逐条状态 |
| `summary.json` | 汇总统计（含隔离矩阵、冻结锁、镜像一致性、既有评审计数） |
| `file_hashes.json` / `.sha256` | 19 个受检文件哈希 |
| `tools/eval_test_audit.py` | 本轮只读检测工具（可复现） |

**声明**：本轮为只读预跑检测，未修改任何数据、文档、manifest 或锁；未自动改 ID/公式；未启动训练、未下载模型、未生成动画。
