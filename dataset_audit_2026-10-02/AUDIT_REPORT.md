# 候选数据集全量审计报告（2026-10-02）

> 工具：`tools/dataset_audit.py`（纯标准库，只读）
> 复现命令：
> `python tools/dataset_audit.py --out dataset_audit_2026-10-02 --content-findings dataset_audit_2026-10-02/content_findings.jsonl`
> 契约依据：`DATASET_SCHEMA.md`；配套证据：`issues.jsonl`、`summary.json`、`record_status.jsonl/.csv`、`file_hashes.*`

---

## 0. 结论摘要

| 维度 | 结果 |
|---|---|
| 审计文件 | 9 个（4 个 `dataset_*.json`、4 个 `data/v1/raw/dataset_*.jsonl`、1 个来源手稿 `dataset.md`） |
| 样本总量 | **63 条**（JSON 容器与 JSONL 互为镜像，63/63 逐条一致） |
| 逐条状态 | **rejected 10 / candidate 53 / clean 0** |
| 问题计数 | 硬伤 15、quarantine 160、info 101 |
| JSONL 结构与字段 | 通过（0 解析错误、0 缺字段、0 非法类型、0 未知字段） |
| ID 唯一性 | 通过（63 个唯一 ID，无冲突；唯一编号断档 `calc-series-014`） |
| LaTeX / 中文进公式 | 硬性缺陷 **0**（公式内中文 0、全角 0、`$` 不配对 0、漏反斜杠 0）；公式级硬伤仅 1 处字幕假等式 |
| 数学内容 | **8 处硬伤（8 条记录）**，已逐条独立复核 |
| 精确重复 | problem 逐字重复 1 对（`calc-series-019/020`） |
| 近重复 | ≥0.7 阈值处 0 对；最高 `linalg-049 ↔ linalg-064` = 0.698（紧贴阈值，阈值未校准） |
| 来源 / 许可证 | 全部 `self-authored` + `Internal-Research-Use-Only`（仅内部研究，非公开许可证，无证据文件、无 manifest） |
| 是否误标为已验收训练数据 | **否**。数据位于 `raw/`、无 manifest、无 train/eval/test 拆分、0/63 动画已验证；但文档状态词存在矛盾与陈旧结论 |

**一句话结论：这批 63 条是候选数据（candidate/rejected 混合），不是已验收训练数据；没有任何证据表明它被标成已验收训练数据，但其中 10 条记录含硬伤、全部 63 条缺许可证转正证据与动画验证，不能进入训练。**

---

## 1. 审计范围与只读保证

| 类别 | 文件 |
|---|---|
| JSON 数组容器（待转换） | `dataset_calc.json`、`dataset_geom.json`、`dataset_linalg.json`、`dataset_prob.json` |
| 正式样本入口格式（候选） | `data/v1/raw/dataset_calc.jsonl`、`dataset_geom.jsonl`、`dataset_linalg.jsonl`、`dataset_prob.jsonl` |
| 来源手稿 | `dataset.md` |
| 排除 | `reviews/**`（合成审查夹具，不参与训练）、`.venv/**`、`runs/**`、其余非 `dataset_*` 文件 |

审计约束（已遵守）：
1. **未修改**任何 `dataset_*.json` 或 `data/v1/raw/*.jsonl`（见 §2 哈希：8 个 `dataset_*` 文件审计前后逐字节一致；`dataset.md` 的改动来自外部，见 §2 注）；
2. **未自动重命名 ID、未自动改写任何公式**；所有修复只以文字建议形式给出；
3. **未启动训练、未下载模型、未生成批量动画**；
4. 只读检查 + 新增审计产物；输出逐条问题、汇总统计与原始文件哈希。

---

## 2. 原始文件哈希（SHA256，审计快照 = 当前磁盘内容）

| 文件 | 字节 | SHA256 | 记录数 |
|---|---:|---|---:|
| `dataset_calc.json` | 32212 | `5b85ce136b224512477d52578afc564172f34f52cd27295a577b242cbf39c2ec` | 19 |
| `dataset_geom.json` | 15853 | `714e49d7a43ab99ef1b90b43868982c4191034d6ecca6e7dbce6c13c83ce51c4` | 11 |
| `dataset_linalg.json` | 29364 | `6636cd366510dcb18e05bd0b384fb588dd5e7bee844f000c48477031a4544e17` | 23 |
| `dataset_prob.json` | 16174 | `8d20d583889c0181c6a441ece2d949496cb73889d30237bf70ebd5a3e3f28c5d` | 10 |
| `data/v1/raw/dataset_calc.jsonl` | 32188 | `78982eaa5ae84e2701afc8d63c5049241557a8eaaeef4825c85e1ee78a3314b6` | 19 |
| `data/v1/raw/dataset_geom.jsonl` | 15837 | `1877282a1f4e5c60c5d2f7c7d4e4714d8d07d8f51763f1c943f734d7e1bc8a0f` | 11 |
| `data/v1/raw/dataset_linalg.jsonl` | 29361 | `93f2abc5d1792bb700ea49670fb62362fca0aadd608d6b9274b695d12c72d9ab` | 23 |
| `data/v1/raw/dataset_prob.jsonl` | 16171 | `42e74007bda4bcf0d02a5fba8560b5b16c74ac975786467ea176aeb7b7061cb7` | 10 |
| `dataset.md` | 101460 | `2e8ac3ddb4132670ba62e41fe14f9ab85d2e9de0650c08d5c2b2d5c11d934068` | 手稿 69 条 |

> 完整的机器可读清单见 `file_hashes.json` / `file_hashes.sha256`。
> **完整性复核说明**：8 个 `dataset_*` 文件在审计前后逐字节一致（本审计未写入任何数据文件）。
> `dataset.md` 在首次审计之后被**外部修改**（mtime 2026-10-02 22:02:36，101824 → 101460 字节，行数 1443 → 1407），本会话未执行任何写入该文件的命令；
> 该变化为格式重排（全角逗号 705 → 698、HTML 实体 59 → 64），**69 个 ID、6 条未交付记录、键名拼写错误与结构缺陷均未改变**。
> 上表 `dataset.md` 哈希与随后的统计已按当前磁盘内容重新审计刷新。

---

## 3. 逐项检查结果

### 3.1 JSONL 结构与字段

- 4 个 JSONL 共 **63 行，全部为合法 JSON 对象**：0 解析失败、0 非对象行、0 重复键（`object_pairs_hook` 检测）。
- **字段 12 个齐全且类型正确**：`id / category / sub_category / problem / solution / answer / scene_spec / source / license / function_family / visual_style / efficiency_tags`；**0 缺字段、0 空值、0 未知字段**（`F001–F008` 全部为 0）。
- `scene_spec` 均为对象且含 `objects/steps` 两个非空列表；`efficiency_tags` 均为非空字符串列表。
- 结构小项（info，不影响判定）：4 个 JSONL 与 2 个 JSON 容器使用 **CRLF 行尾**（共 6 处）；当前 `dataset.md` 末尾无多余空行；无 BOM、无重复键、无解码错误。
- **格式契约**：4 个 `dataset_*.json` 顶层是 JSON 数组，按 `DATASET_SCHEMA.md §1` 属"待转换"格式，**不能作为 train/eval/test 样本入口**（`S005` 硬伤 ×4，仅"样本入口"维度）。它们与对应 JSONL 内容 63/63 完全一致，作为原始容器本身无数据损坏。

### 3.2 ID 唯一性

- 63 个样本 → **63 个唯一 ID**；JSONL 内部 0 重复、0 冲突。
- 跨 JSON 容器与 JSONL 的"重复"全部是**镜像对**：63 对逐条 canonical JSON 完全一致（`mirror identical = 63/63`），不是真实重复数据。
- `id` 前缀 ↔ `category` ↔ 文件名三者一致：0 例外（`I002/I003` = 0）。
- 编号断档（info）：`calc` 编号 1–20 内缺 **14**（`calc-series-014`）；`geom 020–030`、`prob 038–047`、`linalg 048–070` 连续。
- 工具**只报告定位，未改名、未去重**。

### 3.3 problem / solution / answer 一致性

机械判据（`C007/C008/C009`）：

| 判据 | 结果 |
|---|---|
| `answer` 未逐字出现在 `solution`（等价表述，info） | 23 条 |
| `answer` 的数学式部分未出现在 `solution`（quarantine，需人工核对） | 4 条 |
| `answer` 非自包含终答（"见解答"类，quarantine） | 2 条：`geom-027`、`prob-046` |
| 公式内重复等式（quarantine） | 1 条：`calc-improper-002` |

内容评审（4 个板块逐条人工复核 + Lead 独立复算）：

- **8 处硬伤（8 条记录）**：`calc-area-008`、`calc-area-010`、`calc-improper-002`、`geom-023`、`geom-027`、`linalg-055`、`linalg-058`、`prob-043`（详见 §5）。
- 其中 **answer 与题干/事实矛盾 3 处**：`calc-area-010`（answer=1，正确面积≈1.9491）、`geom-027`（称无交点，实际两交点）、`linalg-055`（称无穷多解，实际唯一解 (1,0,0)）。
- **推导错误但终答碰巧正确 1 条**：`calc-area-008`（积分区间与末步算术错，终答 πa² 正确）。
- **多问题干只答一问**（quarantine）：`geom-024`、`geom-025`、`geom-026`、`linalg-051`、`linalg-053`、`prob-045` 等。
- 其余：`geom-023` 距离正确但投影点错；`linalg-058` det/面积正确但方向写反；`prob-043` 题干/解答正确，仅动画描述写反。

### 3.4 scene_spec.objects / steps

- **63/63 条均含 `objects` 与 `steps` 且非空**（`A001–A004` = 0）：objects 合计 269 个（每条 3–9 个），steps 合计 291 个（每条 4–7 个）。
- **步骤编号全部连续**：`第N步` 序列 0 例外（`A005/A006` = 0）。
- **动画验证状态：0/63**。所有记录都缺 `code / render_status / code_sha256`（`A008` ×63, quarantine）。按 `DATASET_SCHEMA.md §7`，状态只能标 **candidate**，**不得宣称动画已验证**。
- 内容级自洽问题（quarantine，见 §5 与 `issues.jsonl`）：objects 与 steps 描述不一致（`calc-green-005`）、步骤自相矛盾（`calc-series-020`）、动画与数学结论矛盾（`prob-043`）、无法在三维呈现（`linalg-060`）、无可演示内容（`linalg-066`）、步骤公式在数学模式外裸写（`calc-limit-006`、`linalg-061` 等）。

### 3.5 LaTeX 写法与中文进入公式

对 `problem / solution / answer / scene_spec` 全部字符串扫描：

| 检查 | 结果 |
|---|---|
| `$...$` 内中文（CJK） | **0** |
| `$...$` 内全角标点/全角字符（U+3000–303F、U+FF00–FFEF） | **0**（现有 CJK 正则 `[一-鿿]` 检测不到此类字符，本审计补充扫描后仍为 0） |
| `$` 不配对 | **0** |
| 花括号 / `\left`-`\right` 不配对 | **0** |
| 漏反斜杠（`+infty`、裸 `sin/cos/tan/ln/log/lim/arctan`） | **0** |
| 未加花括号的多位数字上下标 | **0** |
| 公式内重复等式 | **1**（`calc-improper-002`：`\lim_{b\to+\infty}\arctan b = \arctan b = \frac{\pi}{2}`） |
| 同一层重复上下标标记（风格提示，info） | 1 |

**结论：中文进公式的问题在这批数据中已不存在，LaTeX 硬性缺陷为 0**；唯一公式级硬伤是上述字幕假等式，已由内容评审与机械检查（`C008`）双重命中。

### 3.6 来源与许可证状态

- `source` 全部 = `self-authored`（63/63）；`license` 全部 = `Internal-Research-Use-Only`（63/63）。
- 许可证在项目白名单内（用户 2026-10-02 确认的语义），但它是**仅限内部研究使用、不公开分发、后续转正**的语义，**不等于 Apache/MIT/CC**；公开或转正前必须换为真实许可证 → `P002` ×63（quarantine）。
- `self-authored` **没有配套来源证据文件**（`P003` ×63, info）；`data/README.md` 要求 manifest 登记 `path/sha256/size/source/license/split/notes`，而 `data/v1` 下**无 manifest.json**（`M001`）。
- 来源手稿 `dataset.md` 质量（`SRC001–SRC005`）：键名拼写错误 `catergory`×3、`sub_catergory`×3、`licence`×2；全角逗号 698 处、中文弯引号 33 处、HTML 实体 `&#x20;`×64；`"scene_spec"{` 缺冒号 1 处；**整份文件不是合法 JSON**，属未结构化手稿。
- **覆盖缺口（重要）**：`dataset.md` 实含 **69 条**记录（多出类别"高等几何"6 条：`geom-032`–`geom-037`），而交付数据集只有 63 条。这 6 条**没有任何删除/拒绝记录或理由**，来源与交付之间不可追溯 → `SRC005`（quarantine）。另：手稿中 `geom-033` 的解答公式 `$\sin B = \frac{\sqrt{6}}{2}` 未闭合、文本被截断。

### 3.7 精确重复与近重复

| 检查 | 结果 |
|---|---|
| 整条记录完全重复（排除 JSON/JSONL 镜像） | **0** |
| `problem` 逐字重复 | **1 对**：`calc-series-019` ↔ `calc-series-020`（`D001`×2，硬伤；answer 也逐字相同，solution 仅删减中间步骤） |
| `scene_spec` 完全重复 | 0 |
| 近重复（problem 5-gram Jaccard ≥ 0.7，项目阈值） | **0 对**（上述精确重复对已单独计为 `D001`，不再重复计） |
| 最接近阈值 | `linalg-049 ↔ linalg-064`：Jaccard **0.698**、SequenceMatcher 0.962（题干模板逐字相同，仅矩阵不同） |
| 次高 | `linalg-049↔linalg-068` 0.455、`linalg-048↔linalg-068` 0.410、`linalg-048↔linalg-049` 0.352 |

- `calc-series-019/020` 没有 `problem_id / solution_id / method` 字段，**不构成 `DATASET_SCHEMA.md §6` 预留的"同题多解"**，应人工决定去留（工具未自动去重）。
- 0.7 阈值按 `PROGRESS.md` B5 仍是**未校准初值**；`linalg-049/064` 距阈值仅 0.002，建议用真实分布做校准对照。

### 3.8 四个板块的数量与分布

| 板块（category） | 文件 | 条数 | 占比 | ID 区间 | 子类数 |
|---|---|---:|---:|---|---:|
| 数学分析 | `dataset_calc.jsonl` | 19 | 30.2% | `calc-*-001…020`（缺 14） | 10 |
| 高等代数 | `dataset_linalg.jsonl` | 23 | 36.5% | `linalg-048…070` | 11 |
| 解析几何 | `dataset_geom.jsonl` | 11 | 17.5% | `geom-020…030` | 5 |
| 概率论 | `dataset_prob.jsonl` | 10 | 15.9% | `prob-038…047` | 9 |
| **合计** | 4 个 JSONL | **63** | 100% | — | **35 个子类** |

- 分布不均衡：最大板块（高等代数 36.5%）是最小板块（概率论 15.9%）的 **2.3 倍**。
- 来源手稿还包含**第 5 个板块"高等几何" 6 条**（`geom-032`–`geom-037`），未进入交付数据集。
- 拆分角色分布：`raw = 63`，`train = 0`，`eval = 0`，`test = 0`，`rejected = 0` —— `data/v1` 下只有 `raw/`。

### 3.9 是否误把候选数据标成已验收训练数据

**结论：没有发现"候选数据被标为已验收训练数据"的情况；但存在可能误导的状态词与陈旧文档。**

支持"未误标"的证据：
- 样本位于 `data/v1/raw/`（raw 角色），`data/v1` 下**无 train/eval/test 目录、无 manifest.json、无 `*.lock.json`**；
- `.gitignore` 明确忽略 `/data/**/*.jsonl`，数据未入库；
- 样本内没有任何 `split/status/verified` 之类验收字段；`scene_spec` 的 `code/render_status/code_sha256` **0/63 存在**（动画未验证）；
- `data/README.md` 明写"当前没有已批准进入训练的数据集"；`README.md`/`PROGRESS.md` 明写真实数据验收与训练尚未开展。

需要人工统一的**文档风险**（`M011` 硬伤 / `M012` quarantine）：
- `DATASET_REVIEW.md` 头部状态写 **clean**（入场检查语义），正文虽注明"不是已验收训练集"，但标题词易被误读；
- `DATASET_SCHEMA.md` 自相矛盾：§7 写"当前 **64** 条均齐备"、§4 写"当前 **63** 条全部如此"、§8 引用"状态：**rejected**，3 硬伤 + 87 待补齐"，三者与当前 `clean/63` 状态冲突，属陈旧结论。

---

## 4. clean / quarantine / rejected 划分

### 4.1 记录级（63 条）

| 状态 | 条数 | 含义 |
|---|---:|---|
| **rejected** | **10** | 含硬伤（数学错误、答案矛盾、结构硬伤），必须修复后重审 |
| **candidate** | **53** | 无硬伤，但存在 quarantine（动画未验证、许可证待转正、答案待补齐等） |
| **clean** | **0** | 无任何问题（当前无一条达到） |

**rejected 的 10 条（定位到行）**

| 文件 | 定位 | ID | 硬伤代码 |
|---|---|---|---|
| `data/v1/raw/dataset_calc.jsonl` | line 2 | `calc-improper-002` | K-ANIM-ERR（字幕假等式） |
| 同上 | line 8 | `calc-area-008` | K-DERIV-ERR（积分区间+算术错） |
| 同上 | line 10 | `calc-area-010` | K-MATH-ERR（题干-答案矛盾） |
| 同上 | line 18 | `calc-series-019` | D001（problem 逐字重复） |
| 同上 | line 19 | `calc-series-020` | D001（problem 逐字重复） |
| `data/v1/raw/dataset_geom.jsonl` | line 4 | `geom-023` | K-MATH-ERR（投影点错误） |
| 同上 | line 8 | `geom-027` | K-MATH-ERR（结论与事实相反） |
| `data/v1/raw/dataset_linalg.jsonl` | line 8 | `linalg-055` | K-MATH-ERR（解集判断错误） |
| 同上 | line 11 | `linalg-058` | K-MATH-ERR（作用方向写反） |
| `data/v1/raw/dataset_prob.jsonl` | line 6 | `prob-043` | K-ANIM-ERR（动画与 CLT 矛盾） |

### 4.2 文件级

| 文件 | 条目 | 硬伤 | quarantine | 入口状态 | 内容状态 |
|---|---:|---:|---:|---|---|
| `data/v1/raw/dataset_calc.jsonl` | 19 | 5 | 46 | **rejected** | rejected（5 条硬伤） |
| `data/v1/raw/dataset_geom.jsonl` | 11 | 2 | 26 | **rejected** | rejected（2 条硬伤） |
| `data/v1/raw/dataset_linalg.jsonl` | 23 | 2 | 56 | **rejected** | rejected（2 条硬伤） |
| `data/v1/raw/dataset_prob.jsonl` | 10 | 1 | 25 | **rejected** | rejected（1 条硬伤） |
| `dataset_calc.json` | 19 | 1 | 0 | rejected（JSON 数组不作样本入口） | 与 JSONL 一致 |
| `dataset_geom.json` | 11 | 1 | 0 | rejected（同上） | 与 JSONL 一致 |
| `dataset_linalg.json` | 23 | 1 | 0 | rejected（同上） | 与 JSONL 一致 |
| `dataset_prob.json` | 10 | 1 | 0 | rejected（同上） | 与 JSONL 一致 |
| `dataset.md` | 手稿 69 | 0 | 6 | candidate（非样本入口） | 未结构化手稿，6 条未交付 |

> 两套状态是两个维度：**入口状态**回答"能不能作为样本入口"（JSON 数组一律 rejected）；**内容状态**回答"数据本身有没有硬伤"。两者都不等于"验收通过"。

### 4.3 为什么没有 clean

每条记录至少带 2 条系统级 quarantine：**A008（动画未验证，63/63）**、**P002（许可证仅内部研究，63/63）**。因此即使数学全对的记录也只能是 candidate。

---

## 5. 逐条问题清单（硬伤实际 15 条，下表按类合并为 12 行）

| # | 文件:定位 | ID | 代码 | 问题（证据） | 建议 |
|---|---|---|---|---|---|
| 1 | `dataset_calc.jsonl:10` | `calc-area-010` | K-MATH-ERR | 题干求 `y=ln x` 与 `y=x-2` 围成面积，解答给出错误交点 (1,-1)、(e,e-2) 后**把题目改成** ∫₁^e ln x dx=1，answer=1；真实交点 x≈0.158594、3.146193，面积≈**1.9491** | 人工决定改题干还是改解答；勿自动改写 |
| 2 | `dataset_calc.jsonl:8` | `calc-area-008` | K-DERIV-ERR | `r=2a cosθ` 在 `[0,2π]` 上积分把圆算了两遍（应为 2πa²），末步 `2a²π = πa²` 是错误等式；终答 πa² 正确 | 修正积分区间与末步算术 |
| 3 | `dataset_calc.jsonl:2` | `calc-improper-002` | K-ANIM-ERR | scene_spec 字幕 `\lim_{b\to+\infty}\arctan b = \arctan b = \frac{\pi}{2}` 含假中间等式 | 删除中间等式 |
| 4 | `dataset_calc.jsonl:18` | `calc-series-019` | D001 | problem 与 line 19 逐字相同（answer 也相同） | 人工决定去留 |
| 5 | `dataset_calc.jsonl:19` | `calc-series-020` | D001 | 同 #4 | 人工决定去留 |
| 6 | `dataset_geom.jsonl:4` | `geom-023` | K-MATH-ERR | 投影点 (8/9,14/9,17/9) 不在平面 `2x-y+2z+1=0` 上（代入=5），`|PQ|=5/3≠10/3`；正确 t=-10/9、Q=**(-2/9,19/9,7/9)** | 人工改正 t、Q 与 answer |
| 7 | `dataset_geom.jsonl:8` | `geom-027` | K-MATH-ERR | 称"无实数解/无交点"；实际 `3t²+6t+2=0`，Δ=12>0，**有两个交点**；answer 又是"见解答"式非自包含 | 人工改写解答与 answer |
| 8 | `dataset_linalg.jsonl:8` | `linalg-055` | K-MATH-ERR | det=2、秩=3，**唯一解 (1,0,0)**；数据称"秩为2/无穷多解/解集是直线"，scene_spec 称"两平面重合"均不成立 | 人工重算并同步 answer 与动画 |
| 9 | `dataset_linalg.jsonl:11` | `linalg-058` | K-MATH-ERR | `E=[[1,0],[3,1]]` 作用为 `(x,y)→(x,3x+y)`（x 不变、y→y+3x），数据写成"y 不变、x→x+3y" | 人工改正方向表述 |
| 10 | `dataset_prob.jsonl:6` | `prob-043` | K-ANIM-ERR | 动画写"直方图变矮变宽"；CLT 下 Var(X̄)=σ²/n 递减，应**变高变窄** | 人工改正动画描述 |
| 11 | `dataset_*.json` ×4 | — | S005 | JSON 数组不是合法样本入口（`DATASET_SCHEMA §1`） | 保留原文件；按 convert 流程使用 JSONL |
| 12 | `DATASET_SCHEMA.md` | — | M011 | 文档计数自相矛盾（64 / 63 / "rejected,3 硬伤+87 待补齐"） | 统一权威计数后再作验收依据 |

> 硬伤合计 15 = S005×4 + D001×2 + K-MATH-ERR×5 + K-ANIM-ERR×2 + K-DERIV-ERR×1 + M011×1。

### 内容级 quarantine（20 条，摘要）

| 类别 | 条数 | 记录 |
|---|---:|---|
| K-ANS-WEAK（answer 不完整/非自包含） | 7 | `geom-024`、`geom-025`、`geom-026`、`linalg-051`、`linalg-053`、`prob-045`、`prob-047` |
| K-AMBIG（口径/术语/表述歧义） | 4 quarantine + 2 info | quarantine：`calc-series-017`、`prob-046`、`linalg-050`、`linalg-065`；info：`prob-042`、`prob-044` |
| K-SPEC-CONFLICT / K-CONFLICT（动画脚本或图文冲突） | 5 | `calc-series-020`、`calc-green-005`、`linalg-048`(K-CONFLICT)、`linalg-060`、`linalg-066` |
| K-CLASS / K-FORMAT / K-TEXT / K-EDIT-RESIDUE / K-NEAR-DUP | 4 quarantine + 1 info | `linalg-064`、`calc-limit-006`、`calc-improper-002`、`calc-area-010`、`linalg-049`(info) |
| C009（answer 指向"见解答"） | 2 | `geom-027`、`prob-046` |
| C008（公式重复等式） | 1 | `calc-improper-002` |
| SRC001–SRC005（来源手稿质量与覆盖缺口） | 7 | `dataset.md`（含 `geom-032`–`geom-037` 未交付） |
| M012（陈旧审查结论） | 1 | `DATASET_SCHEMA.md` |
| **内容评审发现合计** | **31**（hard 8 / quarantine 20 / info 3） | 见 `content_findings.jsonl` |

完整逐条明细（含完整证据片段与推荐动作）见 **`issues.jsonl`**（共 276 条）与 **`content_findings.jsonl`**（31 条内容评审发现）。

---

## 6. 汇总统计

**严重度**：hard 15 / quarantine 160 / info 101。

**问题代码分布**

| 代码 | 严重度 | 次数 | 含义 |
|---|---|---|---|
| A008 | quarantine | 63 | 动画未验证（缺 code/render_status/code_sha256） |
| P002 | quarantine | 63 | license 仅内部研究，非公开许可证 |
| P003 | info | 63 | source=self-authored，无来源证据文件 |
| C007 | info/quarantine | 23/4 | answer 未逐字出现 / 数学式部分缺失 |
| K-ANS-WEAK | quarantine | 7 | answer 不完整或非自包含 |
| K-AMBIG | info/quarantine | 2/4 | 口径、术语、表述歧义 |
| K-MATH-ERR | hard | 5 | 数学结果/解集错误 |
| K-SPEC-CONFLICT | quarantine | 4 | 动画脚本自洽性问题 |
| S005 | hard | 4 | JSON 数组不作样本入口 |
| SRC001–003 | quarantine | 5 | 来源手稿键名拼写/结构/实体 |
| D001 | hard | 2 | problem 逐字重复 |
| K-ANIM-ERR | hard | 2 | 动画与数学矛盾 |
| C009 | quarantine | 2 | answer 非自包含终答 |
| 其余（C008/L007/I020/K-CLASS/K-CONFLICT/K-DERIV-ERR/K-EDIT-RESIDUE/K-FORMAT/K-NEAR-DUP/K-TEXT/M001/M002/M010/M011/M012/S002/SRC004/SRC005） | 混合 | 各 1–7 | 见 `summary.json` |

**结构与分布**

- 样本 63 条；唯一 ID 63；JSON/JSONL 镜像 63/63 一致；35 个子类；objects 269、steps 291；动画已验证 0/63。
- 拆分角色：raw 63，train/eval/test/rejected 各 0。

---

## 7. 建议的下一步（全部需人工确认）

1. **修数学硬伤（优先级最高）**：`calc-area-010`（题干/答案二选一）、`calc-area-008`（区间与算术）、`linalg-055`（改唯一解）、`linalg-058`（改正方向）、`geom-023`（改正投影点）、`geom-027`（改为两交点）。
2. **修动画字幕/脚本**：`calc-improper-002` 假等式、`prob-043` 变高变窄、`linalg-048` 剪切→拉伸、`linalg-060/066` 换表现方式、`prob-046` 可列可加性口径。
3. **处理重复**：`calc-series-019/020` 去留决定（若保留同题多解，需补 `problem_id/solution_id/method`）。
4. **补 answer 完整性**：7 条 K-ANS-WEAK + 2 条 C009。
5. **来源与许可证转正**：补齐 `self-authored` 证据；`Internal-Research-Use-Only` 在公开/训练前换成真实许可证；建立 `data/v1/manifest.json`（含 sha256、来源、许可证、split、notes）。
6. **动画验证**：逐条过 `render_gate` 后才可登记 `code/render_status=verified/code_sha256`，在此之前保持 candidate。
7. **文档统一**：`DATASET_REVIEW.md` 状态词加"入场检查语义"限定；`DATASET_SCHEMA.md` 的 64/63/rejected 陈旧结论更新。
8. **手稿决策**：`dataset.md` 中未交付的 `geom-032`–`geom-037`（高等几何）确认是"有意剔除"还是"遗漏"，并补 rejected 记录与理由。
9. **阈值校准**：0.7 近重复阈值用真实分布校准；关注 `linalg-049/064`（0.698）。
10. **确认 `dataset.md` 的外部改动**：该手稿在首次审计后被外部修改（22:02:36），请确认修改者与意图（本次已按新内容重审，结论不变）；若后续还要改动，需在改动后重新审计哈希。
11. 上述修复完成后**重跑本审计**，再走 `make_manifest → data_check → split → freeze → preflight` 全链路。

---

## 8. 产物清单

| 文件 | 内容 |
|---|---|
| `AUDIT_REPORT.md` | 本报告（人读） |
| `issues.jsonl` | 逐条问题（276 条，含 severity/code/文件/行号/id/字段/证据/建议） |
| `content_findings.jsonl` | 内容评审发现（31 条，含独立复核状态与复核人） |
| `record_status.jsonl` / `record_status.csv` | 逐条状态（clean/candidate/rejected）与所属问题代码 |
| `summary.json` | 汇总统计（分布、重复、覆盖、验收判定、代码计数） |
| `file_hashes.json` / `file_hashes.sha256` | 9 个原始文件 SHA256/大小/格式/条数 |
| `tools/dataset_audit.py` | 只读审计工具（可复现） |

**声明**：本次审计未修改任何数据集文件，未自动重命名 ID，未自动改写公式，未启动训练、未下载模型、未生成批量动画。
