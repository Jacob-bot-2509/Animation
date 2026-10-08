# dataset-eval / data-test 预跑检测报告（第三轮 · 2026-10-03）

> 工具：`tools/eval_test_audit.py`（纯标准库，只读；本轮新增 `--base` 支持对 v1/v2 两版候选分别检测，并新增同题多解场景互异性、基目录清单/锁归属检查）
> 复现命令：
> `python tools/eval_test_audit.py --base data/v1 --out dataset_audit_2026-10-03-eval-test-v3-v1`
> `python tools/eval_test_audit.py --base data/v2 --out dataset_audit_2026-10-03-eval-test-v3-v2`
> 项目自带预检（只读）：`python tools/eval_test_prep.py check --eval data/v1/eval --test data/v1/test --train-dir data/v1/raw` → exit 0
> 契约依据：`DATASET_SCHEMA.md`、`EVAL_TEST_PREP.md`；证据：两个输出目录的 `issues.jsonl` / `summary.json` / `record_status.*` / `file_hashes.*`
> 历史轮次：第一轮 `dataset_audit_2026-10-03-eval-test/`（NOT READY, hard 3）、第二轮 `…-v2/`（CONDITIONAL PASS, hard 0）

---

## 0. 结论摘要与裁定

本轮出现两个候选版本，**分别检测**：

| 维度 | **v1**（已冻结 19:25，不可变） | **v2**（22:09 新候选，待用户批准切换） |
|---|---|---|
| 入口 | `data/v1/{eval,test}/dataset_{eval,test}.jsonl` | `data/v2/{eval,test}/dataset_{eval,test}.jsonl` |
| 记录数 | 300 + 150 = **450** | 300 + 150 = **450** |
| 逐条状态 | rejected 0 / quarantine 450 / clean 0 | rejected 0 / quarantine 450 / clean 0 |
| **hard** | **0** | **0** |
| quarantine | **1353** | **904** |
| info | 833 | 855 |
| 隔离（精确/近重复） | 0 / max 0.6667 | 0 / max 0.6667 |
| 冻结锁 | 2 个，绑定 `data/v1/manifest.json`（校验通过） | 2 个，绑定 v2 子清单（校验通过） |
| 行尾/哈希可复现 | **已修**（全 LF） | **已修**（全 LF） |
| 清单条目契约 | **已修**（子清单仅登记 JSONL，split=eval/test） | 子清单合规，但**无顶层清单** |
| 元数据 tag 卫生 | **未修**（450 条 `"- "` 前缀残留） | **已修**（0 条） |
| scene_spec | v1 通用场景（objects 1200 / steps 1500） | **逐解法重写**（objects 612 / steps 1212，同题 3 解法场景互异 100/100） |

### 裁定

- **v1：复核通过，四项必清中三项已清**（W001 行尾/哈希、MF005+MF009 清单条目、D011 手稿状态）。`F011`（450 条 tag 前缀残留）未清，但 v1 已冻结不可变，**由 v2 取代**；`D012`（文档仍写"未冻结"）为仓库级待办。
- **v2：硬门禁全部通过，可作为替代候选**；切换引用前仍需：① **顶层 manifest 登记**（`MF011`）+ 用户批准切换；② `A008` 动画验证（0/450）；③ `P002` 许可证转正（450）；④ `D012` 文档状态更新（3）。

---

## 1. 范围、快照与只读保证

| 类别 | v1 | v2 |
|---|---|---|
| 入口 JSONL | `data/v1/eval/dataset_eval.jsonl`(465152)、`data/v1/test/dataset_test.jsonl`(201290) | `data/v2/eval/dataset_eval.jsonl`(432636)、`data/v2/test/dataset_test.jsonl`(200390) |
| 镜像 JSON | `…/dataset_eval.json`(524255)、`…/dataset_test.json`(224609) | `…/dataset_eval.json`(483003)、`…/dataset_test.json`(223709) |
| 子清单 | `data/v1/{eval,test}/manifest.json`(563×2) | `data/v2/{eval,test}/manifest.json`(573×2) |
| 顶层清单 | `data/v1/manifest.json`(2573)、`manifest-train.json`(2105) | **不存在**（MF011） |
| 冻结锁 | `data/{eval,test}-v1.lock.json` | `data/{eval,test}-v2.lock.json` |
| 来源手稿（共用） | `dataset-eval.md`(205335)、`data-test.md`(118713) | 同左 |
| 训练参考池 | `data/v1/raw/dataset_{calc,geom,linalg,prob}.jsonl`（63 条，已 LF） | 同左 |

- 快照时间：v1 运行 `2026-10-03T14:14:18Z`、v2 运行 `2026-10-03T14:14:19Z`（= 北京时间 22:14）；两个输出目录在运行后立即复核，受检文件哈希无变化。
- 只读保证：未修改任何数据、文档、清单或锁；未自动改 ID/公式；未启动训练、未下载模型、未生成动画。

---

## 2. 原始文件哈希（SHA256，本轮快照）

| 文件 | 字节 | SHA256（前 12 位） |
|---|---:|---|
| `data/v1/eval/dataset_eval.jsonl` | 465152 | `9e5b7355606d` |
| `data/v1/test/dataset_test.jsonl` | 201290 | `e1ba1eb49dd7` |
| `data/v1/eval/manifest.json` / `test/manifest.json` | 563 / 563 | `81a3e052ab06` / `1a15e8ca525b` |
| `data/eval-v1.lock.json` / `test-v1.lock.json` | 469 / 469 | `597f5f5b0f4b` / `01767d21555d` |
| `data/v2/eval/dataset_eval.jsonl` | 432636 | `8ff7044a0c48` |
| `data/v2/test/dataset_test.jsonl` | 200390 | `d4de0bb6a86f` |
| `data/v2/eval/manifest.json` / `test/manifest.json` | 573 / 573 | `a92d80727398` / `cd681f55f7d4` |
| `data/eval-v2.lock.json` / `test-v2.lock.json` | 469 / 469 | `e8d3fafc62fd` / `fa98d15f7db3` |
| `data/v1/raw/dataset_{calc,geom,linalg,prob}.jsonl` | 32908 / 18138 / 31002 / 15462 | 见 `file_hashes.json` |
| `dataset-eval.md` / `data-test.md` | 205335 / 118713 | 见 `file_hashes.json` |

> 完整清单：v1 运行 19 个文件、v2 运行 17 个文件（v2 无顶层清单/无 v2 README）。见各自 `file_hashes.json`。

---

## 3. 上一轮（第二轮）四项建议必清的验收

| 上一轮项 | 本轮状态 | 证据 |
|---|---|---|
| `W001` 记录哈希绑定 CRLF 而 `.gitattributes` 声明 `eol=lf` | **已修复** | 提交 `a8f5071`「全量数据/清单/锁 LF 落盘 + 索引重规范化，两个 manifest 哈希按 LF 字节重算」；本轮实测：raw JSONL、v1/v2 JSONL、各级 manifest、锁**CRLF 计数全为 0**；fresh clone 复现见提交 `738d175` |
| `MF005` split 语义冲突（子清单标 `raw`） | **已修复** | `data/v1/{eval,test}/manifest.json` 现只登记 JSONL 且 `split=eval`/`test` |
| `MF009` 子清单把 `.json` 数组容器登记为数据条目 | **已修复** | 子清单条目从 3 条（含 `.json` 与 README）降为 1 条（仅 JSONL）；`M002` 仅剩"镜像"info |
| `F011` efficiency_tags 残留 `"- "` 前缀 | **v1 未清 / v2 已清** | v1：450 条仍带前缀（数据冻结不可变）；v2：0 条（提交 `c599006` 修生成器、`4fe0152` 清理数据） |
| `D011`/`D012` 文档仍写"未冻结" | **部分修复** | `dataset-eval.md`/`data-test.md` 已去除"未冻结/草稿"字样；`EVAL_TEST_PREP.md`（6 处）与 `data/v1/{eval,test}/README.md`（标题）仍写"未冻结" → 本轮 `D012`×3 |

---

## 4. v2 候选专项核验（Lead 独立复核）

### 4.1 v1 → v2 差异范围（逐字段比对 450 条）

| 池 | 记录数 | 差异字段命中 |
|---|---:|---|
| eval | 300 | `scene_spec` 300、`efficiency_tags` 300、`solution` **1** |
| test | 150 | `scene_spec` 150、`efficiency_tags` 150 |

→ v2 是**纯 scene_spec/元数据修订**（外加 1 条解法补全）；`id`、`problem`、`answer`、`category`、`source`、`license` 与 v1 逐条相同，**未引入新题目**，故隔离结论与 v1 一致。

### 4.2 逐解法 scene_spec（用户批准的 v2 核心改动）

- eval：100 个 problem_id、每组 3 个解法，**scene_spec 完全相同的组数 = 0**；首步文本完全相同的组数 = 0 → "逐解法场景"落实（`G003` info 通过）。
- 规模：eval objects 总计 **612**（每条 1–3）、steps 总计 **1212**（每条 3–5）；test objects 303 / steps 603。相比 v1（1200/1500）明显精简，符合"解法专属动画要点"的定位。
- 无空 objects/steps；450/450 均含两列表。

### 4.3 v2 对既有内容问题的处理

- `eval-linalg-023-s3`（上一轮内容评审 A 级关联项）已改为**自包含**：先给出实数域分解的两种形式，再用平方差恒等式连接并证明，`Lead 复核`式子正确（$(x^2+1)^2-(\sqrt2x)^2=x^4+1$）。
- 上一轮 5 条 A 级（`test-prob-002`、`eval-calc-006`、`eval-linalg-023`、`test-linalg-021`、`test-x-011`）在 v2 中仍保持已修正状态（v2 未改动 problem/solution/answer，除上述 1 条）。

### 4.4 仍需补齐（v2）

| 项 | 说明 |
|---|---|
| `MF011` | v2 只有子清单+锁，**无顶层 `data/v2/manifest.json`** → 切换引用时需顶层登记，把 train/eval/test 绑到同一份清单并重冻 |
| `A008`×450 | 动画仍未验证：v2 同样无 `code`/`render_status`/`code_sha256`，scene_spec 仍是设计稿 |
| `P002`×450 | `license=Internal-Research-Use-Only`（仅内部研究、不公开分发），训练/公开前须转正 |
| `D012`×3 | `EVAL_TEST_PREP.md` 与 `data/v1/{eval,test}/README.md` 仍写"未冻结" |

---

## 5. 硬门禁逐项结果（v1 / v2）

| # | 门禁 | v1 | v2 |
|---|---|---|---|
| G1 | JSONL 结构（解析/空行/BOM/重复键） | 通过 | 通过 |
| G2 | 必需字段/类型/未知字段 | 通过 | 通过 |
| G3 | 身份唯一性（eval 300 + test 150，跨池无交集） | 通过 | 通过 |
| G4 | 同题多解组约束（100 组×3 解、题干一致、method 唯一） | 通过 | 通过 |
| G5 | answer 可判分性 | 通过 | 通过 |
| G6 | LaTeX（公式内 CJK/全角/`$`/括号） | 通过（0 硬性） | 通过（0 硬性） |
| G7 | scene_spec 结构 | 通过 | 通过 |
| G8 | 镜像 `.json` ↔ JSONL 一致 | 通过（450/450） | 通过（450/450） |
| G9 | 与 train 隔离 | 通过（精确 0；max 0.5915） | 通过（同左） |
| G10 | eval ↔ test 隔离 | 通过（精确 0；max **0.6667**；≥0.7 对数 0） | 通过（同左） |
| G11 | manifest 登记 | 通过（顶层+子清单） | **子清单通过，顶层缺失（MF011）** |
| G12 | 冻结锁校验（结构/条目哈希/manifest 绑定） | 通过 | 通过 |
| G13 | 元数据完备性 | 通过（513/513 齐全） | 通过 |
| G14 | 元数据卫生（tag 前缀） | **不通过**（F011×450） | 通过 |
| G15 | 行尾/哈希可复现 | **通过** | 通过 |
| G16 | 文档状态一致 | 不通过（D012×3） | 不通过（D012×3） |
| G17 | 动画验证 | 不通过（0/450） | 不通过（0/450） |
| G18 | 许可证 | 不通过（内部研究） | 不通过（内部研究） |

---

## 6. 隔离检测

| 池对 | 精确重叠 | 最大 5-gram Jaccard（set） | ≥0.7 对数 |
|---|---:|---:|---:|
| train ↔ eval | 0 | 0.5915（`linalg-067` vs `eval-linalg-007-s1`） | 0 |
| train ↔ test | 0 | 0.3895（`linalg-067` vs `test-linalg-021`） | 0 |
| eval ↔ test | 0 | 0.6667（`eval-calc-023-s1` vs `test-calc-013`） | 0 |

- v1 与 v2 的题目文本完全相同，故两张表的数值一致。
- 边界对（0.6667）经 Lead 复核为**结构性相似**（共用 LaTeX 脚手架；一题"证明 Σ1/n² 收敛"、一题"求 Σ1/(n(n+2)) 的和"，任务与级数均不同），非题面泄漏；阈值 0.7 仍标 UNCALIBRATED，建议纳入校准。
- **门禁盲区仍未关闭**：`tools/eval_test_prep.py check` 的 eval↔test 比较仍只用"核心正文哈希 + ID"，不做组间近重复（第三轮仍无变化）。

---

## 7. 逐条问题清单

### 7.1 硬伤：**v1 0 条、v2 0 条**

### 7.2 quarantine

| 代码 | v1 | v2 | 内容 | 处置建议 |
|---|---:|---:|---|---|
| `P002` | 450 | 450 | `license=Internal-Research-Use-Only` | 训练/公开前转正（用户级） |
| `A008` | 450 | 450 | 动画未验证（无 code/render_status/code_sha256） | 过 `render_gate` 后登记（用户级） |
| `F011` | **450** | 0 | efficiency_tags 残留 `"- "` 前缀 | v2 已清；v1 不再改（被取代） |
| `D012` | 3 | 3 | `EVAL_TEST_PREP.md` + `data/v1/{eval,test}/README.md` 写"未冻结" | 更新文档（仓库级） |
| `MF011` | 0 | **1** | v2 无顶层 manifest | 批准切换后顶层登记并重冻 |
| 合计 | **1353** | **904** | | |

### 7.3 info（v1 833 / v2 855）

| 代码 | v1 | v2 | 内容 |
|---|---:|---:|---|
| `P003` | 450 | 450 | `source=self-authored`（如实） |
| `C007` | 274 | 274 | answer 与 solution 无文本重合（纯文字结论，正常） |
| `L007` | 86 | 100 | 双上下标（`x_1^2` 类，合法） |
| `L006` | 7 | 11 | `\leftarrow` 被 `\left` 规则误报（复核为误报） |
| `L009` | 3 | 7 | `\frac32`/`\dfrac12` 单 token 参数（合法 TeX，复核为误报） |
| `X002` | 3 | 3 | 三对池最大近重复（0.5915 / 0.3895 / 0.6667） |
| `M002` | 2 | 2 | `.json` 仅作镜像（入场工具只选 `*.jsonl`） |
| `LK007`/`LK008` | 2/1 | 2/1 | 本基目录锁校验通过 / 其他基目录锁未校验 |
| `G002`/`G003` | 1/1 | 1/1 | 多解组 {3:100} / 场景互异性通过 |
| `C008` | 1 | 1 | `A^2=A` 恒等演示（复核为误报） |
| `MF008` | 1 | 1 | train 标签为"用户拍板 provisional"（如实） |
| `R001` | 1 | 1 | 既有内容评审 64 条（A5/B31/C28）纳入交叉核对 |

---

## 8. 汇总统计

| 项 | v1 | v2 |
|---|---:|---:|
| eval / test 记录 | 300 / 150 | 300 / 150 |
| 唯一身份 | 300 / 150 | 300 / 150 |
| 题目数 | 100（每组 3 解）/ 150 | 100（每组 3 解）/ 150 |
| 子类数 | 41 / 144 | 41 / 144 |
| objects / steps | 1200 / 1500（eval）、303 / 603（test） | **612 / 1212**（eval）、303 / 603（test） |
| method 数 | 263 | 263 |
| 状态 | rejected 0 / quarantine 450 / clean 0 | rejected 0 / quarantine 450 / clean 0 |
| 动画验证 | 0/450 | 0/450 |

- 板块：eval（高代 105 / 数分 90 / 几何 60 / 概率 45，按解法计）；test（数分 45 / 高代 40 / 几何 25 / 概率 25 / 跨学科 15）。

---

## 9. 裁定与建议

1. **v1 完成使命**：第二轮所列 W001/MF005/MF009/D011 均已修复并复核；剩下的 F011 属数据内容问题，v1 已冻结不可变，**不再回改**（保留其历史版本价值）。文档 `D012` 建议在最终切换时一并更新。
2. **v2 可进入"批准切换"流程**：结构与字段、身份、多解组、LaTeX、镜像、隔离、冻结锁、元数据卫生全部通过（hard 0）。切换前需完成：
   - ① **顶层 manifest 登记**：在 `data/v2/manifest.json` 里把 train（raw 63）+ eval + test 绑成同一份清单，重建双锁（当前锁只绑子清单）；
   - ② **用户批准**引用切换（v2 notes 已注明"切换引用需用户批准"）；
   - ③ 动画验证（`A008` 450）：过 `render_gate` → 登记 `code`/`render_status=verified`/`code_sha256`；
   - ④ 许可证转正（`P002` 450）。
3. **门禁能力建议**：给 `eval_test_prep.py check` 补 eval↔test 近重复比较；并对 0.7 阈值做一次校准（0.6667 边界对可作校准样本）。
4. **不建议**在完成 ①–④ 前把 v2（或 v1）当作正式训练/评测数据引用；`manifest-train.json` 的 `split=train` 仍为 provisional（notes 如实注明未验收）。

---

## 10. 产物清单

| 路径 | 内容 |
|---|---|
| `dataset_audit_2026-10-03-eval-test-v3/AUDIT_REPORT.md` / `.pdf` | 本报告（合并 v1 复核 + v2 候选裁定） |
| `dataset_audit_2026-10-03-eval-test-v3-v1/` | v1 检测输出：`issues.jsonl`(2186)、`summary.json`、`record_status.*`、`file_hashes.*` |
| `dataset_audit_2026-10-03-eval-test-v3-v2/` | v2 检测输出：`issues.jsonl`(1759)、`summary.json`、`record_status.*`、`file_hashes.*` |
| `tools/eval_test_audit.py` | 只读检测工具（支持 `--base`，可复现） |

**声明**：本轮为只读预跑检测，未修改任何数据、文档、清单或锁；未自动改 ID/公式；未启动训练、未下载模型、未生成动画。
