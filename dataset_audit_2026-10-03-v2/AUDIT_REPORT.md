# 候选数据集全量审计报告（第二轮 · 2026-10-03）

> 工具：`tools/dataset_audit.py`（纯标准库，只读；本轮新增 manifest 一致性、来源文档↔交付内容逐条比对）
> 复现命令：
> `python tools/dataset_audit.py --out dataset_audit_2026-10-03-v2 --content-findings dataset_audit_2026-10-03-v2/content_findings.jsonl`
> 契约依据：`DATASET_SCHEMA.md`；证据：`issues.jsonl`、`summary.json`、`record_status.jsonl/.csv`、`file_hashes.*`
> 上一轮（数据版本 2026-10-02，63 条）：`dataset_audit_2026-10-02/AUDIT_REPORT.md`

---

## 0. 结论摘要

| 维度 | 结果 |
|---|---|
| 审计文件 | 9 个（4 个 `dataset_*.json`、4 个 `data/v1/raw/dataset_*.jsonl`、1 个来源手稿 `dataset.md`）+ 新增 `data/v1/manifest.json` 校验 |
| 样本总量 | **62 条**（上一轮 63 条；JSON 容器与 JSONL 镜像 62/62 逐条一致） |
| 逐条状态 | **rejected 3 / candidate 59 / clean 0** |
| 问题计数 | 硬伤 7（结构 4 + 内容 3）、quarantine 153、info 112 |
| JSONL 结构与字段 | 通过（0 解析错误、0 缺字段、0 空值、0 未知字段） |
| ID 唯一性 | 通过（62 个唯一 ID、0 冲突；唯一断档 `calc-series-014`） |
| LaTeX / 中文进公式 | 硬性缺陷 **0**（公式内中文 0、全角 0、`$` 不配对 0、漏反斜杠 0） |
| 精确/近重复 | **精确重复 0**（上一轮 `calc-series-019/020` 已消除）；近重复 ≥0.7 为 0（项目实现口径最高 `linalg-049↔linalg-064`=0.698，多重集口径=0.714，卡在阈值两侧） |
| 来源/许可证 | manifest 已建立且 4/4 哈希匹配、`split=raw`、来源/许可证字段齐全；`Internal-Research-Use-Only` 仍需转正；来源手稿与交付 62/62 逐条一致 |
| 是否误标为已验收训练数据 | **否**（无 train/eval/test、无验收字段、动画 0/62 验证；文档已统一为 62 条且明确 candidate≠已验收） |
| 动画验证状态 | 0/62 |

**一句话结论：数据质量较上一轮显著改善（10 条 rejected → 3 条，重复题与来源缺口全部消除，manifest 与来源手稿已闭环）；但仍是候选数据，3 条含硬伤记录必须修复后才可进入验收流程，全部 62 条仍缺许可证转正证据与动画验证。**

---

## 1. 审计范围与只读保证

| 类别 | 文件 |
|---|---|
| JSON 数组容器（待转换） | `dataset_calc.json`、`dataset_geom.json`、`dataset_linalg.json`、`dataset_prob.json`（各 19/11/23/9） |
| 正式样本入口格式（候选） | `data/v1/raw/dataset_{calc,geom,linalg,prob}.jsonl` |
| 来源手稿 | `dataset.md`（本轮已是逐行 JSON 对象，62 条） |
| 清单 | `data/v1/manifest.json`（4 条 entry） |
| 排除 | `reviews/**`（合成审查证据）、`.venv/**`、`runs/**`、其他 `dataset_audit_*` 审计产物 |

只读保证：本会话未修改任何 `dataset_*.json`、`data/v1/raw/*.jsonl`、`dataset.md` 或 `data/v1/manifest.json`；未自动重命名 ID、未自动改写公式；未启动训练、未下载模型、未生成批量动画。

---

## 2. 原始文件哈希（SHA256，本轮审计快照）

| 文件 | 字节 | SHA256 | 记录数 |
|---|---:|---|---:|
| `data/v1/raw/dataset_calc.jsonl` | 32344 | `f0a8294dcecdc0e91d421cbc3484bb58bbb1c9da2e58652442ca54975b576842` | 19 |
| `data/v1/raw/dataset_geom.jsonl` | 15742 | `0f033af96a29bb01074fb05b9e30e54a2e7c4fec0d2b4b448d7fe19874f80db8` | 11 |
| `data/v1/raw/dataset_linalg.jsonl` | 29570 | `b2895ec152f47f0420302bc3aeccdfa0ea4975894ebe2ed15c7702e8f20e7e0b` | 23 |
| `data/v1/raw/dataset_prob.jsonl` | 14752 | `7c05779a333e0844f9f9cc372a920430f19ad05e11b4a94ed35ca4146ce9bd8c` | 9 |
| `dataset_calc.json` | 32368 | `59114f2c03f848df5c14c7c392d98355bdba8a4da4212575bee6bd08866c5b52` | 19 |
| `dataset_geom.json` | 15758 | `3f6d4dd875028ecfb1347832c61e3ddf0095bdc69552f46f614e70b414030019` | 11 |
| `dataset_linalg.json` | 29598 | `bb848fbac1cfb719ee872c7ee701210e0c02fd6fbce40f899b4c7e7d902ba629` | 23 |
| `dataset_prob.json` | 14766 | `4f61f8e67ad7a9a3c35a3a847eb8414974c6f0547bbf1b707959abbfae36f862` | 9 |
| `dataset.md` | 92530 | `89b8dba6db8d90bca83512a2ee781d27502f57f122180df84f561820d9eabef4` | 62 |
| `data/v1/manifest.json` | 1604 | （逐条 entry 哈希见下 §3.9，4/4 与文件匹配） | 4 entries |

> 完整机器可读清单见 `file_hashes.json` / `file_hashes.sha256`。审计过程只读，9 个文件在本轮审计期间哈希与 mtime 均未变化。

---

## 3. 与上一轮（2026-10-02，63 条）的差异

### 3.1 文件级

| 文件 | 上一轮字节 | 本轮字节 | 变化 | 本轮 SHA256（前 12） |
|---|---:|---:|---:|---|
| `data/v1/raw/dataset_calc.jsonl` | 32188 | 32344 | +156 | `f0a8294dcecd` |
| `data/v1/raw/dataset_geom.jsonl` | 15837 | 15742 | −95 | `0f033af96a29` |
| `data/v1/raw/dataset_linalg.jsonl` | 29361 | 29570 | +209 | `b2895ec152f4` |
| `data/v1/raw/dataset_prob.jsonl` | 16171 | 14752 | −1419 | `7c05779a333e` |
| `dataset_calc.json` | 32212 | 32368 | +156 | `59114f2c03f8` |
| `dataset_geom.json` | 15853 | 15758 | −95 | `3f6d4dd87502` |
| `dataset_linalg.json` | 29364 | 29598 | +234 | `bb848fbac1cf` |
| `dataset_prob.json` | 16174 | 14766 | −1408 | `4f61f8e67ad7` |
| `dataset.md` | 101460 | 92530 | −8930 | `89b8dba6db8d` |

### 3.2 ID 级

| 项 | 结果 |
|---|---|
| 删除 | `prob-047`（1 条；其内容原样递补为当前 `prob-046`，旧 `prob-046`「概率的公理化定义／answer=见解答（面积映射法）」整条删除，该 sub_category 消失） |
| 新增 | 无 |
| 保留 | 62 条；行号全部未变 |
| 元数据变化 | `calc-series-019`（一般级数 → 正项级数，题目整体替换为裂项相消题）、`prob-046`（概率的公理化定义 → 可列可加性） |

### 3.3 上一轮硬伤修复情况：10 条 → 完全修复 8 条、部分修复 1 条、重写后仍有新错 1 条

| 上一轮 rejected 记录 | 上一轮问题 | 本轮状态 |
|---|---|---|
| `calc-improper-002` | 字幕假等式 `\arctan b = \arctan b = π/2` | **已修复**（假等式删除；"去线"笔误亦已改） |
| `calc-area-008` | 极坐标积分区间与末步算术错 | **已修复**（区间改为 `[-π/2, π/2]`，推导与 `πa²` 一致） |
| `calc-area-010` | 交点错 + 中途改题 + answer=1 | **题目已重写，但面积算错** → 见 §6（新硬伤） |
| `calc-series-019` | 与 020 题目逐字重复 | **已修复**（改为 `∑1/(n²+n)=1` 裂项题，数学正确） |
| `calc-series-020` | 同上 | **已消除重复** |
| `geom-023` | 投影点错 | **已修复**：`t=-10/9`、`Q=(-2/9,19/9,7/9)`，代入平面为 0、`|PQ|=10/3`（Lead 与 geom 评审双重独立复核） |
| `geom-027` | 称无交点，实际两交点 | **已修复**：`3t²+6t+2=0`、`Δ=12>0`、answer「有两个交点」 |
| `linalg-055` | 秩/解集判断错 | **已修复**：秩 3、唯一解 `(1,0,0)`（Lead sympy 复核） |
| `linalg-058` | 作用方向写反 | **主错误已修复**：solution/answer 为 `x` 不变、`y→y+3x`（Lead sympy 复核）；但动画步骤 2「竖直方向的网格线发生倾斜」方向仍写反 → 本轮新增硬伤（见 §6） |
| `prob-043` | 动画"变矮变宽"与 CLT 矛盾 | **已修复**：改为"变高变窄"，solution/answer/steps 三处口径一致 |

### 3.4 上一轮文档/来源问题：已闭环

| 上一轮问题 | 本轮状态 |
|---|---|
| `dataset.md` 键名拼写错误（`catergory`×3、`sub_catergory`×3、`licence`×2） | **已修复**（0 处） |
| `dataset.md` 中 `"scene_spec"{` 缺冒号、HTML 实体 `&#x20;`×59 | **已修复**（0 处） |
| 来源手稿 69 条 vs 交付 63 条，6 条「高等几何」记录无交代 | **已闭环**：手稿与交付**均为 62 条且逐条内容完全一致**（`content_compared=62, content_diff_ids=[]`） |
| 无 manifest | **已建立** `data/v1/manifest.json`（4 条 entry，哈希 4/4 匹配，`split=raw`） |
| `DATASET_SCHEMA.md` 计数自相矛盾（64/63/rejected…） | **已统一**（§4/§7/§8 均为 62 条，且新增"manifest 只登记事实、不代表验收"表述） |
| `data/v1` 缺 manifest | 已补（同上） |

### 3.5 上一轮 quarantine 仍未修（遗留清单）

`calc-series-017`（"包络线"表述 + `\sum` 无上下限）、`calc-series-020`（Markdown 粗体 + 省略口径矛盾）、`calc-green-005`（objects/steps 位置不一致）、`calc-limit-006`（`<` 在数学模式外）、`linalg-048`（剪切/拉伸表述冲突）、`linalg-050/051/053/059/060/064/065/066`、`geom-024/025/026`（answer 未答全）、`geom-028`（推导省略号）、`prob-043`（n=2 形态、标准正态叠加口径）、`prob-044`（术语）、`prob-045`（支撑区间）、`prob-046`（answer 裸数字、无数学模式、表述冲突）。

---

## 4. 逐项检查结果

### 4.1 JSONL 结构与字段

- 4 个 JSONL 共 **62 行，全部为合法 JSON 对象**：0 解析失败、0 非对象行、0 重复键。
- **12 个字段齐全、类型正确、无空值、无未知字段**（`F001–F008` 全为 0）。
- `scene_spec` 均为对象且含非空 `objects/steps`；`efficiency_tags` 均为非空字符串列表。
- 结构小项（info）：4 个 JSONL 与 2 个 JSON 容器使用 CRLF 行尾（共 6 处）；无 BOM、无解码错误。
- 4 个 `dataset_*.json` 仍为 JSON 数组容器，按 `DATASET_SCHEMA §1` 属"待转换"格式，**不能作为样本入口**（`S005` 硬伤 ×4，仅入口维度）；与 JSONL 内容 62/62 一致。

### 4.2 ID 唯一性

- 62 个唯一 ID，JSONL 内 0 重复、0 冲突；跨 JSON/JSONL 的重复均为镜像（62/62 一致）。
- `id` 前缀 ↔ `category` ↔ 文件名三者一致：0 例外。
- 编号断档（info）：`calc` 1–20 内缺 **14**；`geom 020–030`、`linalg 048–070`、`prob 038–046` 连续。

### 4.3 problem / solution / answer 一致性

- **硬伤 3 条**：`calc-area-010` 面积算错（数学错误）、`prob-040`（动画与泊松近似矛盾）、`linalg-058`（动画网格线方向与矩阵作用矛盾）。
- 多问题干只答一问（quarantine）：`geom-024`、`geom-025`、`geom-026`。
- `answer` 非自包含（quarantine）：`prob-045`（缺支撑区间）、`prob-046`（裸数字"1"且题干无求值问法）。
- 机械 `C007` 提示的 25 条 answer 未逐字出现中，**已人工逐条确认 3 条为等价表述**（`calc-series-016`、`linalg-061`、`prob-040`，见 §6 的 `K-VERIFIED-OK`），其余为纯文字结论的正常差异。
- **Lead 独立复算全部 62 条**：除 `calc-area-010` 外，其余 61 条的题干↔解答↔答案在数学上一致（含上一轮修复的 6 处与全部计算题）。

### 4.4 scene_spec.objects / steps

- 62/62 条 objects 与 steps 均非空：objects 合计 264（3–9/条），steps 合计 286（4–7/条）；步骤编号 0 例外。
- **动画验证 0/62**：全部缺 `code / render_status / code_sha256`（`A008` quarantine；按 §7 只能标 candidate）。
- 内容级：`prob-040`、`linalg-058`（动画与数学矛盾，hard）、`prob-043`×2、`prob-046`、`linalg-048/050/060/064/065/066`、`calc-area-010/derivative-001/vol-012/series-020/green-005/limit-006` 等（quarantine/info，见 §6）。

### 4.5 LaTeX 写法与中文进公式

| 检查 | 结果 |
|---|---|
| `$...$` 内中文 | **0** |
| `$...$` 内全角标点/全角字符 | **0** |
| `$` 不配对 | **0** |
| 花括号 / `\left`-`\right` 不配对 | **0** |
| 漏反斜杠（`+infty`、裸 `sin/cos/lim/arctan/ln/log`） | **0** |
| 未加花括号的多位数字上下标 | **0** |
| 重复等式笔误 | **0**（上一轮 `calc-improper-002` 已修） |
| 同一层重复上下标标记（风格提示） | 1（`linalg-070`：`u_1v_2`，合法写法，info） |

**结论：LaTeX 硬性缺陷为 0；中文进公式问题不存在。** 仍有少量"数学模式外裸写"的口径问题（`prob-041`、`prob-042`、`prob-046`，info/quarantine）。

### 4.6 来源与许可证状态（含 manifest）

- 62/62 条 `source=self-authored`、`license=Internal-Research-Use-Only`；`P002`（非公开许可证，需转正）×62、`P003`（无来源证据文件，info）×62。
- **manifest 校验通过**：`data/v1/manifest.json` 4 条 entry，覆盖全部 4 个样本文件，**sha256/size 4/4 与文件匹配**，`split` 全部 `raw`，`source/license` 字段齐全，notes 明示"来源/许可证待补（校验会报 quarantine）"；未出现 `train/eval/test` 或 `accepted/verified/ready` 等验收语义。
- 来源手稿 `dataset.md`：现为逐行 JSON 对象（62 条），与交付池 **62/62 逐条内容完全一致**（`SRC008`）；仍有中文全角逗号 615 处、中文引号 28 处（正文标点，属正常）。

### 4.7 精确重复与近重复

| 检查 | 结果 |
|---|---|
| 整条重复 / 同 ID 冲突 | **0** |
| `problem` 逐字重复 | **0**（上一轮 `calc-series-019/020` 已消除） |
| `scene_spec` 完全重复 | **0** |
| 近重复（5-gram Jaccard ≥ 0.7） | **项目实现口径 0 对** |
| 最接近阈值 | `linalg-049 ↔ linalg-064`：**项目实现 `shingles()`（set，重复 5-gram 去重）= 0.698113（<0.7，未触发）**；改用多重集口径 = 40/56 = **0.714286（≥0.7，会触发 D002）**；原始字符集口径 = 0.698113。两题干仅矩阵不同，归一化长度均 52、仅第 [17]/[20] 位不同 |

> **阈值敏感性（需人工决断）**：该对是否构成近重复完全取决于 5-gram 去重口径，正好卡在 0.7 两侧；项目 `PROGRESS.md` B5 明确 0.7 是**未校准初值**。建议按真实分布校准后重新判定 `linalg-049/064`，并在契约中写明用 set 还是 multiset。

### 4.8 四个板块的数量与分布

| 板块 | 文件 | 条数 | 占比 | ID 区间 | 子类数 |
|---|---|---:|---:|---|---:|
| 数学分析 | `dataset_calc.jsonl` | 19 | 30.6% | `calc-*-001…020`（缺 14） | 11 |
| 高等代数 | `dataset_linalg.jsonl` | 23 | 37.1% | `linalg-048…070` | 11 |
| 解析几何 | `dataset_geom.jsonl` | 11 | 17.7% | `geom-020…030` | 5 |
| 概率论 | `dataset_prob.jsonl` | 9 | 14.5% | `prob-038…046` | 8 |
| **合计** | 4 个 JSONL | **62** | 100% | — | **35** |

- 拆分角色：`raw = 62`，`train/eval/test/rejected = 0`（`data/v1` 下只有 `raw/`）。
- 分布不均衡度略降（最大/最小 = 37.1%/14.5% ≈ 2.6）；概率论由 10 → 9 条。

### 4.9 是否误把候选数据标成已验收训练数据

**结论：未发现误标。** 依据：
1. 样本位于 `data/v1/raw/`，无 `train/eval/test` 目录、无 `*.lock.json`、无逐样本验收字段；
2. `scene_spec` 的 `code/render_status/code_sha256` **0/62 存在**（动画未验证，不得声明已验证）；
3. `manifest.json` 仅登记事实（`split=raw`、notes 标注待补），**不含** `accepted/verified/ready` 字段；
4. 文档已统一：`DATASET_REVIEW.md` 62 条、状态 clean（入场检查语义，正文注明"不是已验收训练集"）；`DATASET_SCHEMA.md` 新增"candidate ≠ 已验收训练集""manifest 生成只登记事实，均不代表数据已验收"；`data/README.md` 仍写"当前没有已批准进入训练的数据集"。
5. 仅存提示：`DATASET_REVIEW.md` 头部"状态: clean"易被误读为验收通过，建议加限定词（`M010`，info）。

---

## 5. clean / quarantine / rejected 划分

### 5.1 记录级（62 条）

| 状态 | 条数 | 记录 |
|---|---:|---|
| **rejected** | **3** | `calc-area-010`（面积算错）、`prob-040`（动画与泊松近似矛盾）、`linalg-058`（动画网格线方向写反） |
| **candidate** | **59** | 无硬伤，但存在 quarantine（动画未验证、许可证待转正、answer 待补齐等） |
| **clean** | **0** | 每条至少带 A008（动画未验证）+ P002（许可证待转正）两项系统级 quarantine |

### 5.2 文件级

| 文件 | 条目 | 硬伤 | quarantine | 入口状态 |
|---|---:|---:|---:|---|
| `data/v1/raw/dataset_calc.jsonl` | 19 | 1 | 46 | **rejected**（1 条硬伤） |
| `data/v1/raw/dataset_linalg.jsonl` | 23 | 1 | 57 | **rejected**（1 条硬伤） |
| `data/v1/raw/dataset_prob.jsonl` | 9 | 1 | 24 | **rejected**（1 条硬伤） |
| `data/v1/raw/dataset_geom.jsonl` | 11 | 0 | 26 | candidate |
| `dataset_{calc,geom,linalg,prob}.json` | 19/11/23/9 | 各 1 | 0 | rejected（JSON 数组不作样本入口） |
| `dataset.md` | 62 | 0 | 0 | clean（来源镜像，非样本入口） |

> 两个维度：**入口状态**回答"能否作为样本入口"；**内容状态**回答"数据本身有无硬伤"。二者均不等于验收通过。

---

## 6. 逐条问题清单

### 6.1 硬伤（实际 7 条）

| # | 文件:定位 | ID | 代码 | 问题 | 建议 |
|---|---|---|---|---|---|
| 1 | `dataset_calc.jsonl:10` | `calc-area-010` | K-MATH-ERR | 题干：`y=ln x`、`y=-x+e+1` 与 x 轴围成的封闭图形，正确面积 = `∫₁^e ln x dx + ∫_e^{e+1}(-x+e+1)dx = 1 + 1/2 = 3/2`；数据把第一段写成"直线−曲线"之差（那是被竖线 `x=1` 封口的另一区域，不属于三曲线围成的图形），得 `½e²−1 ≈ 2.6945` | 人工把第一段改为 `∫₁^e ln x dx` 并同步 answer |
| 2 | `dataset_prob.jsonl:3` | `prob-040` | K-ANIM-ERR | 题设 λ=np 且 n↑、p↓（λ 固定），柱状图中心应固定在 λ、形态收敛到泊松 P(λ)；步骤却写"中心向右移动，且分布形状越来越趋于平缓" | 人工改为"中心固定在 λ=np 处，柱形逐步逼近 P(λ)" |
| 3 | `dataset_linalg.jsonl:11` | `linalg-058` | K-ANIM-ERR | 动画与矩阵作用矛盾：`E=[[1,0],[3,1]]` 把 `(x,y)` 映为 `(x, y+3x)`，竖直网格线 `x=c` 保持不变，倾斜的是水平网格线；步骤 2 却写"网格沿 y 轴方向被剪切，即竖直方向的网格线发生倾斜" | 人工改为"水平网格线被抬斜，点在竖直方向偏移 3x" |
| 4–7 | `dataset_{calc,geom,linalg,prob}.json` | — | S005 | JSON 数组不是合法样本入口（`DATASET_SCHEMA §1`），须 convert 为 JSONL | 保留原文件，按 convert 流程使用 JSONL |

> **`calc-area-010` 的独立复核与分歧处理（重要）**：本轮 calc 评审子代理曾独立复算并给出"answer `½e²−1` 正确"的结论，与本报告相反。Lead 用三种互相独立的方法复算后确认**本报告结论成立**：
> ① 解析积分 `∫₁^e ln x dx + ∫_e^{e+1}(-x+e+1)dx = 1 + 0.5 = 1.5`；
> ② 数值积分 400001 点 = `1.4999999999990277`；
> ③ 蒙特卡洛 6×10⁶ 点（区域 `{1≤x≤e+1, 0<y<min(ln x, L(x))}`）= `1.50034`。
> 且已证明在 `[1,e]` 上恒有 `ln x ≤ L(x)`（仅在 `x=e` 取等），故三曲线所围区域在 `[1,e]` 的**上边界是曲线 `ln x` 而非直线**；`2.6945 = [L−C on [1,e]] + [L on [e,e+1]]` 是"两曲线间区域 + 三角形"的拼接，其边界包含竖直线段 `x=1`，并非"由曲线、直线与 x 轴围成"的图形。

### 6.2 内容 quarantine（29 条，摘要）

| 类别 | 条数 | 记录 |
|---|---:|---|
| 答案未答全 / 缺要素 | 5 | `geom-024`、`geom-025`、`geom-026`、`linalg-051`、`linalg-053`、`linalg-059`（负惯性指数）、`prob-045`（支撑区间）、`prob-046`（裸数字"1"） |
| 动画/脚本与数学或自身冲突 | 9 | `prob-040`（hard）、`linalg-058`（hard）、`prob-043`（n=2 形态、标准正态叠加口径）、`prob-046`（"无限趋近"vs"和为 1"、objects 未落地）、`linalg-048`（剪切 vs 拉伸）、`linalg-059`（配方切变 vs 坐标旋转）、`linalg-060`（三元二次型画三维曲面）、`linalg-066`（相似变换 P=I）、`calc-vol-012`（承诺的推导未展示）、`calc-area-010`（objects 缺步骤元素） |
| 推导/表述不严谨 | 4 | `geom-028`（省略号+缺关键步）、`calc-limit-006`（单侧证明未补偶函数）、`calc-series-017`（"包络线"）、`linalg-050`（有向面积口径） |
| 格式/口径 | 4 | `calc-series-020`（Markdown 粗体+省略矛盾）、`calc-limit-006`（`<` 在数学模式外）、`prob-046`（整条无 `$`）、`calc-derivative-001`（visual_style "割线逼近切线" 与场景不符） |
| 分类/元数据 | 3 | `linalg-064`（sub_category 口径）、`linalg-065`（visual_style "Smith 标准形" 名不符实）、`linalg-049`（近重复卡在 0.7 两侧，口径敏感） |
| 其他 | 1 | `calc-green-005`（objects/steps 位置不一致） |

> 其中 `linalg-048/050/051/053/059/060/064/065/066`、`calc-series-017/020/green-005`、`geom-024/025/026`、`prob-043/045/046` 均为上一轮已列出但**本轮仍未修复**的遗留项。

### 6.3 已人工复核为"非缺陷"（info，3 条）

`calc-series-016`、`linalg-061`、`prob-040` 的机械 `C007` 提示均为等价表述（answer 的数学式与 solution 推导结果一致），已在 `content_findings.jsonl` 中标记 `K-VERIFIED-OK`。

> 另有两处评审提出的"硬伤"经 Lead 复核后**不成立**，已按实际情况归类：`calc-area-010` 的"answer 正确"结论被推翻（维持硬伤）；`linalg-049/064` 的"Jaccard=0.7143 必触发阈值"结论受 5-gram 去重口径影响（项目实现为 0.6981，未触发），已按"阈值敏感项"记录为 quarantine。

> 完整逐条明细（含证据原文、复核人、建议动作）见 **`issues.jsonl`**（共 272 条）与 **`content_findings.jsonl`**（41 条内容发现：hard 3 / quarantine 29 / info 9）。

---

## 7. 汇总统计

- **严重度**：hard 7 / quarantine 153 / info 112。
- **逐条状态**：rejected 3 / candidate 59 / clean 0。
- **系统级 quarantine**：`A008`（动画未验证）×62、`P002`（许可证仅内部研究）×62。
- **结构与分布**：62 条、62 唯一 ID、35 子类、objects 264、steps 286、镜像 62/62、来源镜像 62/62、manifest 4/4 匹配。
- **重复**：精确 0；近重复按项目实现 0 对（`linalg-049/064`=0.698113；多重集口径 0.714286，卡在阈值两侧）。
- **LaTeX**：公式内中文 0、全角 0、`$` 不配对 0、漏反斜杠 0、重复等式 0。

---

## 8. 建议的下一步

1. **修 3 条硬伤**：`calc-area-010`（面积 `3/2`）、`prob-040`（动画口径）、`linalg-058`（网格线方向）。
2. **补答案完整性**：`geom-024/025/026`、`linalg-051`、`linalg-053`、`linalg-059`、`prob-045`、`prob-046`。
3. **动画脚本复核**：`prob-043`、`prob-046`、`linalg-048/059/060/066`、`calc-series-020`、`calc-green-005`、`calc-limit-006`、`calc-series-017`、`calc-vol-012`、`calc-area-010`、`calc-derivative-001`。
4. **许可证转正**：`Internal-Research-Use-Only` → 真实许可证；补齐 `self-authored` 的证据；manifest 更新来源/许可证后重新绑定哈希。
5. **动画验证**：逐条过 `render_gate` 后登记 `code/render_status=verified/code_sha256`，在此之前保持 candidate。
6. **阈值与口径校准**：0.7 近重复阈值用真实分布校准，并在契约中写明 5-gram 用 set 还是 multiset（`linalg-049/064` 正好卡在两侧）。
7. **修复完成后重跑本审计**，再走 `make_manifest → data_check → split → freeze → preflight` 全链路。
8. 建议把本轮与上一轮审计目录一并保留（`dataset_audit_2026-10-02`、`dataset_audit_2026-10-03-v2`），便于追溯数据版本演进。

---

## 9. 产物清单

| 文件 | 内容 |
|---|---|
| `AUDIT_REPORT.md` / `AUDIT_REPORT.pdf` | 本报告（人读） |
| `issues.jsonl` | 逐条问题（含 severity/code/文件/行号/id/字段/证据/建议） |
| `content_findings.jsonl` | 内容评审发现（含独立复核状态与复核人） |
| `record_status.jsonl` / `record_status.csv` | 逐条状态（clean/candidate/rejected）与问题代码 |
| `summary.json` | 汇总统计（分布、重复、来源覆盖、manifest、验收判定） |
| `file_hashes.json` / `file_hashes.sha256` | 9 个原始文件 SHA256/大小/格式/条数 |

**声明**：本轮审计未修改任何数据集文件、未自动重命名 ID、未自动改写公式，未启动训练、未下载模型、未生成批量动画。
