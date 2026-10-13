# 候选数据集全量审计报告（第三轮 · 2026-10-03）

> 工具：`tools/dataset_audit.py`（纯标准库，只读；含 manifest 一致性、来源文档↔交付逐条比对、JSONL 结构/ID/一致性/scene_spec/LaTeX/重复/分布/验收语义九类检查）
> 复现命令：
> `python tools/dataset_audit.py --out dataset_audit_2026-10-03-v3 --content-findings dataset_audit_2026-10-03-v3/content_findings.jsonl`
> 契约依据：`DATASET_SCHEMA.md`；证据：`issues.jsonl`、`summary.json`、`record_status.jsonl/.csv`、`file_hashes.*`
> 历史轮次：`dataset_audit_2026-10-02/AUDIT_REPORT.md`（第一轮，63 条）、`dataset_audit_2026-10-03-v2/AUDIT_REPORT.md`（第二轮，62 条）

---

## 0. 结论摘要

| 维度 | 结果 |
|---|---|
| 样本总量 | **63 条**（上一轮 62 条；**新增 `geom-031`**，几何 11 → 12） |
| 逐条状态 | **rejected 0 / candidate 63 / clean 0** |
| 问题计数 | 硬伤 4（**全部为 JSON 数组容器 `S005`，无记录级硬伤**）、quarantine 144、info 131 |
| 内容级硬伤 | **0**（上一轮 3 条硬伤 `calc-area-010`、`prob-040`、`linalg-058` 均已修复并独立复核） |
| JSONL 结构与字段 | 通过（0 解析错误、0 缺字段、0 空值、0 未知字段） |
| ID 唯一性 | 通过（63 唯一 ID、0 冲突；`geom-031` 补入后几何编号 020–031 连续；仅 `calc` 仍缺 14） |
| LaTeX / 中文进公式 | 硬性缺陷 **0**（公式内中文 0、全角 0、`$` 不配对 0、漏反斜杠 0、重复等式 0） |
| 精确/近重复 | 精确 0；近重复按项目实现 0 对（`linalg-049/064` = 0.698113，多重集口径 0.714286，卡在阈值两侧） |
| 来源/许可证 | 63/63 `self-authored` + `Internal-Research-Use-Only`；manifest 4/4 哈希匹配、`split=raw`；来源手稿与交付 **63/63 逐条一致**；**新增待确认项：数据已提交并被推送到 GitHub 远端，与"不公开分发"语义可能冲突** |
| 是否误标为已验收训练数据 | **否**（无 train/eval/test、无验收字段、动画 0/63 验证） |
| 动画验证状态 | 0/63 |

**一句话结论：本轮把上一轮的全部内容级硬伤清零——63 条中没有任何一条含记录级硬伤（唯一 4 条硬伤是 4 个 JSON 数组容器不能作为样本入口）；但仍是候选数据，需处理许可证/分发范围问题并完成动画验证后才可进入验收流程。**

---

## 1. 审计范围与只读保证

| 类别 | 文件 |
|---|---|
| JSON 数组容器（待转换） | `dataset_calc.json`(19)、`dataset_geom.json`(12)、`dataset_linalg.json`(23)、`dataset_prob.json`(9) |
| 正式样本入口格式（候选） | `data/v1/raw/dataset_{calc,geom,linalg,prob}.jsonl`（已入库 git） |
| 来源手稿 | `dataset.md`（63 条，逐行 JSON 对象） |
| 清单 | `data/v1/manifest.json`（4 条 entry） |
| 排除 | `reviews/**`、`.venv/**`、`runs/**`、其他 `dataset_audit_*` 产物 |

只读保证：本会话未修改任何 `dataset_*.json`、`data/v1/raw/*.jsonl`、`dataset.md`、`data/v1/manifest.json`；未自动重命名 ID、未自动改写公式；未启动训练、未下载模型、未生成批量动画。

---

## 2. 原始文件哈希（SHA256，本轮审计快照）

| 文件 | 字节 | SHA256 | 记录数 |
|---|---:|---|---:|
| `data/v1/raw/dataset_calc.jsonl` | 32500 | `17a06617201c…`（完整值见 `file_hashes.json`） | 19 |
| `data/v1/raw/dataset_geom.jsonl` | 17928 | `b29eae9e1f51…` | 12 |
| `data/v1/raw/dataset_linalg.jsonl` | 30191 | `ce3762a82576…` | 23 |
| `data/v1/raw/dataset_prob.jsonl` | 15167 | `144f3b696797…` | 9 |
| `dataset_calc.json` | 32524 | 见 `file_hashes.json` | 19 |
| `dataset_geom.json` | 17945 | 同上 | 12 |
| `dataset_linalg.json` | 30219 | 同上 | 23 |
| `dataset_prob.json` | 15181 | 同上 | 9 |
| `dataset.md` | 95910 | 同上 | 63 |
| `data/v1/manifest.json` | 1604 | 4 条 entry 与文件 4/4 匹配 | 4 entries |

> manifest 生成时间 2026-10-03 01:08:23，已按新文件重新绑定哈希（校验 4/4 通过）。审计期间 9 个数据文件哈希与 mtime 未变化。

---

## 3. 与上一轮（第二轮，62 条）的差异

### 3.1 文件与记录

| 项 | 结果 |
|---|---|
| 记录数 | 62 → **63**（新增 `geom-031`） |
| 新增 | `geom-031`「球面与圆柱面交线（维维安尼曲线）参数方程」，几何 11 → 12 |
| 删除 | 无 |
| 所有 9 个文件 | 哈希全部变化（内容修补 + 新记录 + manifest 重绑） |

### 3.2 上一轮 3 条硬伤：**全部修复**（Lead 独立复核）

| 记录 | 上一轮问题 | 本轮状态 |
|---|---|---|
| `calc-area-010` | 面积算错（`½e²−1`，正确 `3/2`） | **已修复**：解答改为 `∫₁^e ln x dx = 1` + `∫_e^{e+1}L dx = 1/2`，answer=`3/2`；objects 补了分段虚线与垂直微元。与 Lead 的三重独立复算（解析/数值/蒙特卡洛）一致 |
| `prob-040` | 动画"中心右移、越来越平缓"与 λ=np 固定矛盾 | **已修复**：step3 改为"保持 λ=np=5 固定，中心始终位于 5、方差由 2.5 趋近 5，收敛到 P(5)"（`Var(B(n,p))=np(1-p)→λ` 正确） |
| `linalg-058` | 动画称"竖直网格线发生倾斜"（方向写反） | **已修复**：step2 改为"水平网格线发生倾斜（竖直网格线保持竖直）"，step3 补"以仍竖直的边为底" |

### 3.3 上一轮 quarantine 遗留项：绝大多数已修复

| 上一轮遗留 | 本轮状态 |
|---|---|
| `geom-024/025/026` answer 未答全 | **已修复**（024 补母线/准线、025 补"截面为圆"、026 补两条交线）；025 仍缺半径 √(1+k²)（降为 info） |
| `geom-028` 推导省略号+缺关键步 | **已修复**：补全 `t` 的一次项并给出 `l=m=0 ⇒ n=0` 的关键论证 |
| `linalg-050` 有向面积口径 | **已修复**（step4 改为"绝对值与几何面积一致，负值对应定向反转"） |
| `linalg-051` 只答第一问 | **已修复**（answer 补"三个实根均在实轴上"） |
| `linalg-053` 缺几何结论 | **已修复**（answer 补"绝对值=平行六面体体积"） |
| `linalg-059` 缺负惯性指数 / 配方说成旋转 | **已修复**（answer 补"负惯性指数为 0"；step3 改为"非正交线性替换"） |
| `linalg-060` 三元二次型画三维曲面 | **已修复**（改为 `f=1` 等值面 + 主轴截面口径） |
| `linalg-066` 相似变换无可演示 | **已修复**（改为高亮分块结构与超对角线） |
| `linalg-065` visual_style 名不符实 | **已修复**（改为"矩阵对角化与因子分解"） |
| `prob-043` CLT 口径 | **已修复**（answer 改 `X̄→N(μ,σ²/n)`；step6 改叠 `N(μ,σ²/n)`）；残留 step3 的 n=2 形态表述（info） |
| `prob-044` 术语 | **已修复**（改为"未患病者…99%，相应地假阳性率为 1%"） |
| `prob-045` 缺支撑区间 | **已修复**（answer 补 `0<y<1`） |
| `prob-046` 无数学模式/表述冲突/裸答案 | **已修复**（solution/steps 全面补 `$`，补 `Σ1/2^k=1`，answer 改"1，即所有事件概率之和为 1"） |
| `calc-limit-006` 单侧证明 + `<` 在数学模式外 | **已修复**（补偶函数说明；`$<$` 纳入数学模式） |
| `calc-series-017` "包络线" | **已修复**（步骤改为"界直线 y=±π²/6"且 `\sum` 补上下限）；元数据仍写"包络线"（info） |
| `calc-series-020` Markdown 粗体+省略矛盾 | **已修复**（`**` 移除，step3 改为"中间项数（n=4 到 9）快速带过"） |
| `calc-green-005` objects/steps 位置不一致 | **已修复**（objects 改为"圆内区域的向量场箭头"） |
| `calc-param-improper-003` 错字/引号 | **已修复** |
| `calc-derivative-001` visual_style 与场景不符 | **已修复**（改为"导数几何意义动态演示"） |
| `linalg-048` 剪切 vs 拉伸 | **部分修复**（solution 已写"沿 (1,1) 方向拉伸"，但仍接"其余方向发生剪切形变"，scene 第二步仍"剪切变形"）→ 仍为 quarantine |

### 3.4 新增观察

- **数据入库与远端**：`data/v1/raw/*.jsonl` 已由提交 `61e7922` 纳入 git（`.gitignore` 以"用户授权 2026-10-03"加例外），且该提交**已在 `origin/main`**（`github.com/Jacob-bot-2509/Animation`）；本地另有 2 个提交未推送。由于数据 license 为 `Internal-Research-Use-Only`（不公开分发），若远端仓库为公开则冲突 → 新增 quarantine（见 §6）。
- **行尾与哈希**：工作区为 CRLF、git 存储为 LF（`core.autocrlf=true`、无 `.gitattributes`），manifest/`file_hashes` 的 sha256 绑定 CRLF 字节 → 跨平台克隆后哈希不可复现（`K-HASH-EOL`）。
- **编号连续**：`geom-020…031` 已连续（补齐 `geom-031`）；`calc` 仍缺 `calc-series-014`（info）。

### 3.5 本轮内容评审（四板块独立复审 + Lead 复核）

| 板块 | 复审结论 | hard | quarantine | info |
|---|---|---:|---:|---:|
| 数学分析（19） | 数学与 LaTeX 全部通过；问题集中在 scene_spec 登记一致性 | 0 | 4 | 12 |
| 解析几何（12，含新记录） | 12/12 数学复算通过；`geom-031` 的"分支"指控经 Lead 复核**不成立** | 0 | 1 | 4 |
| 高等代数（23） | 23/23 结论经 sympy 复算通过；最接近 hard 的是 `linalg-048` 措辞 | 0 | 9 | 15 |
| 概率论（9） | 无算术/推导错误；Poisson/CLT/贝叶斯等数值全部复核通过 | 0 | 4 | 10 |

> 合并去重后共 **40 条内容发现（quarantine 18 / info 22）**，已并入 `issues.jsonl` 的 K- 系列；四板块**均无 hard 级内容问题**。

---

## 4. 逐项检查结果

### 4.1 JSONL 结构与字段
4 个 JSONL 共 **63 行、全部合法 JSON 对象**：0 解析失败、0 重复键；12 字段齐全、类型正确、无空值、无未知字段。结构小项（info）：4 个 JSONL 与 2 个 JSON 容器为 CRLF 行尾；无 BOM。4 个 `dataset_*.json` 仍为 JSON 数组容器，按契约**不能作为样本入口**（`S005`×4）；与 JSONL 内容 63/63 一致。

### 4.2 ID 唯一性
63 个唯一 ID、0 冲突；JSON/JSONL 镜像 63/63 一致；前缀↔category↔文件名一致 0 例外；`geom` 编号补齐后连续；仅 `calc` 缺 14（info）。工具未改名、未去重。

### 4.3 problem / solution / answer 一致性
**记录级硬伤 0**。机械 `C007` 30 条提示经人工抽查均为等价表述或纯文字结论差异（前两轮已逐条复核同类项）；多问句 answer 完整性在上一轮基础上已补齐。

### 4.4 scene_spec.objects / steps
63/63 非空：objects 合计 270（2–9/条）、steps 合计 291（4–7/条），步骤编号 0 例外。**动画验证 0/63**（缺 `code/render_status/code_sha256`，只能标 candidate）。内容级问题见 §6（`linalg-048` 等）。

### 4.5 LaTeX 与中文进公式
公式内中文 **0**、全角 **0**、`$` 不配对 **0**、花括号/`\left`-`\right` 不配对 **0**、漏反斜杠 **0**、重复等式 **0**；1 条风格提示（`linalg-070` `u_1v_2`，合法写法）。

### 4.6 来源与许可证状态
- 63/63 `source=self-authored`、`license=Internal-Research-Use-Only`（`P002`×63、`P003`×63）。
- `manifest.json`：4 条 entry、哈希/大小 **4/4 匹配**、`split=raw`、来源/许可证字段齐全、无验收语义字段（`MF000`）。
- 来源手稿 `dataset.md` 与交付池 **63/63 逐条内容完全一致**（`SRC008`）。
- **新增待确认（quarantine）**：数据已入库并被推送到 GitHub 远端，与 `Internal-Research-Use-Only` 的"不公开分发"语义存在冲突风险；同时仓库无 LICENSE 文件（`README.md` 亦称"代码许可证尚待确定"）。

### 4.7 精确重复与近重复
整条重复 0、`problem` 逐字重复 0、`scene_spec` 重复 0；近重复按项目实现 0 对；`linalg-049/064` 阈值敏感项见 §6。

### 4.8 四个板块的数量与分布

| 板块 | 条数 | 占比 | ID 区间 |
|---|---:|---:|---|
| 高等代数 | 23 | 36.5% | `linalg-048…070` |
| 数学分析 | 19 | 30.2% | `calc-*-001…020`（缺 14） |
| 解析几何 | 12 | 19.0% | `geom-020…031`（已连续） |
| 概率论 | 9 | 14.3% | `prob-038…046` |
| **合计** | **63** | 100% | 35 个子类 |

拆分角色：`raw=63`，`train/eval/test/rejected=0`。

### 4.9 是否误把候选数据标成已验收训练数据
**否**：无 train/eval/test 目录、无锁文件、无逐样本验收字段、动画 0/63 已验证；manifest 明确"只登记事实"；文档（`DATASET_SCHEMA.md`/`DATASET_REVIEW.md` 63 条）均声明 `candidate ≠ 已验收训练集`。仅 `DATASET_REVIEW.md` 头部"状态: clean"建议加"入场检查语义"限定（`M010`，info）。

---

## 5. clean / quarantine / rejected 划分

| 状态 | 条数 | 说明 |
|---|---:|---|
| **rejected** | **0** | 无记录级硬伤 |
| **candidate** | **63** | 每条至少带 A008（动画未验证）+ P002（许可证待转正）两项系统级 quarantine |
| **clean** | **0** | 尚无一条同时满足"动画已验证 + 许可证转正 + 元数据完备" |

文件级：4 个 JSONL 均为 candidate（0 硬伤）；4 个 `dataset_*.json` 入口维度 rejected（JSON 数组，`S005`）；`dataset.md` clean（来源镜像，非样本入口）。

---

## 6. 逐条问题清单

### 6.1 硬伤（4 条，均非记录内容问题）

| # | 文件 | 代码 | 问题 | 建议 |
|---|---|---|---|---|
| 1–4 | `dataset_calc.json`、`dataset_geom.json`、`dataset_linalg.json`、`dataset_prob.json` | S005 | JSON 数组不是合法样本入口（`DATASET_SCHEMA §1`），须 convert 为 JSONL | 保留原文件，按 convert 流程使用 JSONL |

### 6.2 内容 quarantine（18 条）

| 类别 | 条数 | 记录 |
|---|---:|---|
| **许可证 / 分发** | 2 | `K-LICENSE-DIST`（数据已推送至 GitHub 远端，与"不公开分发"可能冲突）、`K-HASH-EOL`（哈希绑定 CRLF 字节，跨平台克隆不可复现） |
| **answer 未答题面第二问** | 5 | `linalg-049`、`linalg-052`、`linalg-054`、`linalg-057`、`linalg-064`（与上一轮已修的 051/053/059 同类，本轮新发现） |
| **scene_spec.objects ↔ steps 不一致 / 不可执行** | 7 | `calc-param-improper-003`（objects 三条曲线 vs steps 单曲线）、`calc-vol-012`（承诺推导未展示、objects 无公式项）、`calc-series-017`（objects 要求"极限函数曲线"但全文无表达式）、`calc-series-020`（objects 前 3 项 vs steps 前 10 项）、`linalg-051`（objects 复平面 vs steps 实曲线）、`geom-026`（"抛物线沿 y 轴平移"生成叙述与方程不符）、`prob-046`（answer 裸数字/口径） |
| **几何/动画表述** | 2 | `linalg-048`（"剪切形变"未改纯拉伸）、`prob-043`（步 1 未定重复次数 M） |
| **重复 / 分类** | 2 | `linalg-049`（近重复卡阈值：set 0.698113 / multiset 0.714286）、`linalg-064`（sub_category 口径交叉） |

> 内容 quarantine 合计 18 条；`linalg-048`、`linalg-064`、`linalg-049` 为上一轮登记仍未关闭项。

### 6.3 内容 info（22 条）

| 类别 | 条数 | 记录 |
|---|---:|---|
| 元数据与正文口径不一致 | 5 | `calc-series-017`（仍写"包络线"）、`linalg-058`（"剪切与缩放"/"行列式值变化"）、`linalg-066`（tags"相似变换"）、`linalg-053`（二维 tags）、`linalg-060`（visual_style"开口方向"） |
| answer 粒度/记法 | 5 | `geom-025`（缺半径）、`prob-041`、`linalg-068`（未给 Q）、`prob-046`（问法）、`geom-031`（`sin(t/2)` 记法） |
| 术语/表述精度 | 6 | `prob-044`（特异度）、`prob-045`（开闭区间）、`prob-043`（n=2 三角分布）、`geom-030`（方向歧义）、`linalg-050`（秩 0 退化）、`prob-038`（面积等比口径） |
| LaTeX/排版风格 | 3 | `calc-series-017`（`p=2>1` 在数学模式外）、`linalg-051`（`y=x^3…` 裸写）、`calc-improper-002`（右下角/右侧） |
| 用字与其他 | 3 | `calc-series-015`（"震荡"→"振荡"）、`linalg-048`（题材复用观察）、`geom-031`（`K-VERIFIED-OK`：已驳回评审的 hard 指控） |

> 完整逐条明细见 **`issues.jsonl`**（共 279 条）与 **`content_findings.jsonl`**（40 条内容发现：quarantine 18 / info 22）。

### 6.4 评审分歧的处理（Lead 复核结论）

| 分歧 | 评审方主张 | Lead 复核 | 结论 |
|---|---|---|---|
| `geom-031` 区间/分支说明 | geom 评审判为 **hard**：称「`0≤t≤2π` 仅覆盖上半部分」是假命题、`[0,2π]` 已覆盖整条曲线 | 参数式 `(a(1+cos t), a sin t, 2a sin(t/2))` 满足两曲面方程；`[0,2π]` 上 `z=2a sin(t/2)∈[0,2a]`（仅上半支）；而 `(0,0,-2a)`（t=3π）确实在两曲面上、却不属于 `[0,2π]` 的像；`[0,4π]` 的 z 范围才是 `[-2a,2a]` | **驳回评审的 hard**：数据表述正确，无需修改；已登记 `K-VERIFIED-OK` |
| `geom-026` steps[3] | geom 评审判为 **hard**：纯沿 y 平移只生成抛物柱面 | 数学判断成立（`z=x²` 沿 y 平移得柱面），但 answer/solution 的类型与两条交线均正确，仅动画生成句表述不精确 | **降为 quarantine**（表述问题，非答案/结论错误） |
| `linalg-049/064` 近重复 | linalg 评审按多重集算得 0.7143 ≥ 0.7，主张触发近重复 | 项目实现 `shingles()` 返回 set → 0.698113 < 0.7；多重集口径 → 0.714286 | **列为阈值敏感项**（quarantine），需先统一/校准口径 |
| `calc-area-010`（第二轮） | calc 评审曾结论"answer `½e²−1` 正确" | 解析积分 + 40 万点数值积分 + 600 万点蒙特卡洛三重验证 = **3/2** | **驳回评审**，该条按硬伤处理；本轮数据已改为 `3/2` |

---

## 7. 汇总统计

- **严重度**：hard 4（全部 S005）/ quarantine 144 / info 131（逐条问题共 279 条）。
- **逐条状态**：rejected 0 / candidate 63 / clean 0。
- **系统级 quarantine**：`A008`×63、`P002`×63。
- **结构化数据**：63 条、63 唯一 ID、35 子类、objects 270、steps 291、镜像 63/63、来源镜像 63/63、manifest 4/4。
- **重复**：精确 0；近重复按项目实现 0 对。
- **LaTeX**：公式内中文/全角/`$` 不配对/漏反斜杠/重复等式 全为 0。

---

## 8. 建议的下一步

1. **许可证与分发（最高优先级）**：确认 `origin` 仓库可见性；若公开，需撤下 `Internal-Research-Use-Only` 数据或先完成许可证转正；为仓库补 LICENSE；增加 `.gitattributes` 固定行尾（解决 `K-HASH-EOL` 哈希不可复现问题）。
2. **补 answer 第二问（5 条）**：`linalg-049`、`linalg-052`、`linalg-054`、`linalg-057`、`linalg-064`（与已修的 051/053/059 同类）。
3. **scene_spec.objects ↔ steps 对齐（7 条）**：`calc-param-improper-003`、`calc-vol-012`、`calc-series-017`、`calc-series-020`、`linalg-051`、`geom-026`、`prob-046`。
4. **收尾表述与阈值**：`linalg-048`（剪切→纯拉伸）、`prob-043`（重复次数 M）、`linalg-049/064` 同模板题决策与近重复 5-gram 口径；`linalg-064` 分类口径。
5. **元数据同步（info）**：`calc-series-017`、`linalg-053/058/060/066` 的 visual_style/tags 与正文对齐。
6. **动画验证**：逐条过 `render_gate` 后登记 `code/render_status=verified/code_sha256`，在此之前保持 candidate。
7. **补齐编号**：确认 `calc-series-014` 是否应有记录。
8. **修复完成后重跑本审计**，再走 `make_manifest → data_check → split → freeze → preflight` 全链路。
9. 保留三轮审计目录以便追溯：`dataset_audit_2026-10-02`、`dataset_audit_2026-10-03-v2`、`dataset_audit_2026-10-03-v3`。

---

## 9. 产物清单

| 文件 | 内容 |
|---|---|
| `AUDIT_REPORT.md` / `AUDIT_REPORT.pdf` | 本报告 |
| `issues.jsonl` | 逐条问题（severity/code/文件/行号/id/字段/证据/建议） |
| `content_findings.jsonl` | 内容评审发现（含复核人/复核方式） |
| `record_status.jsonl` / `.csv` | 逐条状态与问题代码 |
| `summary.json` | 汇总统计（分布、重复、来源覆盖、manifest、验收判定） |
| `file_hashes.json` / `.sha256` | 9 个原始文件哈希 |

**声明**：本轮审计未修改任何数据集文件、未自动重命名 ID、未自动改写公式，未启动训练、未下载模型、未生成批量动画。
