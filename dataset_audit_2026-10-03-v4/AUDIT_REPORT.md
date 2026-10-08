# 候选数据集全量审计报告（第四轮 · 2026-10-03）

> 工具：`tools/dataset_audit.py`（纯标准库，只读；含 manifest 一致性、来源文档↔交付逐条比对、JSONL 结构/ID/一致性/scene_spec/LaTeX/重复/分布/验收语义九类检查）
> 复现命令：
> `python tools/dataset_audit.py --out dataset_audit_2026-10-03-v4 --content-findings dataset_audit_2026-10-03-v4/content_findings.jsonl`
> 契约依据：`DATASET_SCHEMA.md`；证据：`issues.jsonl`、`summary.json`、`record_status.jsonl/.csv`、`file_hashes.*`
> 历史轮次：第一轮 `dataset_audit_2026-10-02`（63 条）、第二轮 `dataset_audit_2026-10-03-v2`（62 条）、第三轮 `dataset_audit_2026-10-03-v3`（63 条）

---

## 0. 结论摘要

| 维度 | 结果 |
|---|---|
| 样本总量 | **63 条**（数学分析 19、高等代数 23、解析几何 12、概率论 9） |
| 逐条状态 | **rejected 1 / candidate 62 / clean 0** |
| 问题计数 | 硬伤 5（结构 4 = JSON 数组容器 `S005`；**内容 1 = `prob-043` 动画与抽样分布矛盾**）、quarantine 140、info 139 |
| 内容级硬伤 | **1**（`prob-043`；其余 62 条无记录级硬伤） |
| JSONL 结构与字段 | 通过（0 解析错误、0 缺字段、0 空值、0 未知字段） |
| ID 唯一性 | 通过（63 唯一 ID、0 冲突；`geom-020–031` 连续；仅 `calc` 缺 14） |
| LaTeX / 中文进公式 | 硬性缺陷 **0** |
| 精确/近重复 | 精确 0；近重复按项目实现 0 对（`linalg-049/064` = 0.698113，多重集口径 0.714286，卡在阈值两侧） |
| 来源/许可证 | manifest 4/4 哈希匹配、`split=raw`；来源手稿与交付 63/63 逐条一致；**数据已推送至 GitHub 远端（license 为"不公开分发"）与哈希行尾不可复现两项仍未决** |
| 是否误标为已验收训练数据 | **否**（无 train/eval/test、无验收字段、动画 0/63 验证） |
| 动画验证状态 | 0/63 |

**一句话结论：第四轮把第三轮列出的 scene_spec 语义冲突（10 处）与元数据口径（7 处）全部修掉；但复核发现 1 条动画描述与数学矛盾（`prob-043` n=2 样本均值应为三角分布，已判 hard→rejected），另有 12 条 quarantine 集中在"answer 未答题面第二问"（5 条）、answer 不完整（2 条）、许可证/分发与哈希行尾（2 条）等。**

### 0.1 评审分歧的裁决（本轮）

| 争议项 | 评审主张 | Lead 裁决 |
|---|---|---|
| `prob-043` steps[2] n=2 形态 | prob 评审：**hard**（会生成错误画面，附 20 万次模拟：两端 3991/4002、中部 36028） | **采纳为 hard**（与历史同类：`prob-040`、`linalg-058` 的动画-数学矛盾均判 hard） |
| `prob-046` answer 缺通式/口径 | prob 评审：**hard** | **定为 quarantine**：`DATASET_SCHEMA §2` 规定 answer 缺失/不完整属"补齐"类；数学本身正确 |
| `linalg-051` 复平面双面板 | linalg 评审：quarantine | **定为 info**：上一轮的"objects 复平面 vs steps 实曲线"矛盾已消除，场景现自洽；仅未画复平面面板 |
| `linalg-067` visual_style"旋转与反射" | linalg 评审：quarantine | **定为 info**：属元数据措辞与演示范围不符（同类元数据项一律 info） |
| `linalg-068` answer 缺 Q | linalg 评审：quarantine | **采纳为 quarantine**：与 5 条"answer 未答第二问"同属 answer 不完整 |

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

| 文件 | 字节 | SHA256（前 12 位；完整值见 `file_hashes.json`） | 记录数 |
|---|---:|---|---:|
| `data/v1/raw/dataset_calc.jsonl` | 32927 | 见 `file_hashes.json` | 19 |
| `data/v1/raw/dataset_geom.jsonl` | 18150 | 同上 | 12 |
| `data/v1/raw/dataset_linalg.jsonl` | 30343 | 同上 | 23 |
| `data/v1/raw/dataset_prob.jsonl` | 15303 | 同上 | 9 |
| `dataset_calc.json` / `dataset_geom.json` / `dataset_linalg.json` / `dataset_prob.json` | 32951 / 18167 / 30371 / 15317 | 同上 | 19/12/23/9 |
| `dataset.md` | 96847 | 同上 | 63 |
| `data/v1/manifest.json` | 1604 | 4 条 entry 与文件 4/4 匹配 | 4 entries |

> 审计期间 9 个数据文件哈希与 mtime 未变化（会话内只读）；manifest 由本轮提交 `db8f63b` 重新绑定，校验 4/4 通过。

---

## 3. 与上一轮（第三轮，63 条）的差异

### 3.1 记录级

| 项 | 结果 |
|---|---|
| 记录数 / ID 集合 | 63 条不变；无新增/删除 ID（`geom-031` 保持） |
| 所有 9 个文件 | 哈希全部变化（本轮为 scene_spec 与元数据修补） |
| 上一轮 hard | 无（连续两轮记录级 hard=0） |

### 3.2 第三轮 quarantine：已修复 8 条

| 上一轮项 | 本轮状态 |
|---|---|
| `calc-param-improper-003` objects"三条曲线"vs steps 单曲线 | **已修复**：objects 改为"随参数 α 变化的衰减曲线 y=e^{-αx}"，并补登"曲线下方黄色积分区域高亮" |
| `calc-series-017` objects 要"极限函数曲线"但无表达式 | **已修复**：objects/steps 改为"高项数部分和参考曲线（N=200）"作为极限函数近似 |
| `calc-series-020` objects 仅"前3项"vs steps 前10项 | **已修复**：objects 拆为"逐项正弦波（前3项…，中间项快速带过）"+"前10项叠加的合成波形" |
| `calc-vol-012` objects 无公式项 | **已修复（主体）**：objects 补"右侧分部积分推导公式"；残留 steps 5/6 重复承诺（info） |
| `geom-026` steps"抛物线沿 y 轴平移"与方程不符 | **已修复**：solution/steps 改为"截面抛物线 z=x²+2c² 随 c 变化，顶点沿 y 平移 c 同时沿 z 抬高 2c²" |
| `linalg-048` "剪切和拉伸" | **已修复**：solution 改为"对称矩阵…沿两个正交特征方向的纯拉伸（无剪切）"，scene 改为"沿两个正交特征方向发生纯拉伸变形" |
| `linalg-051` objects"复平面"vs steps 实曲线 | **已修复**：objects 改为"直角坐标系（实轴）"，steps 第四步改为"在数轴上展示三个根" |
| `linalg-064` sub_category 口径交叉 | **已修复**：sub_category 改为"特征值与特征向量"，与 linalg-049 一致 |
| `prob-038` 圆面积/正方形口径 | **已修复**：objects 改为"矩形样本空间（总面积对应概率 1）"并按比例标注 0.6/0.4/0.2 |
| `calc-improper-002` 措辞（钟形曲线、位置） | **已修复**：steps 改为"对称单峰曲线"，objects/steps 位置统一为"右下角" |
| `calc-series-017` 元数据"包络线" | **已修复**：visual_style 改"上下界约束带"、tags 改"上下界直线" |

### 3.3 元数据口径（7 处）：已修复

`linalg-053`（二维 tags → "单位立方体映射/有向体积"）、`linalg-058`（"网格剪切与缩放/行列式值变化" → "网格剪切/面积保持"）、`linalg-060`（"开口方向" → "等值面闭合性与正定性"）、`linalg-066`（tags"相似变换" → "分块高亮"）、`linalg-064`（见上）、`linalg-049`（function_family → "矩阵的特征分解"）、`linalg-068`（→ "主轴旋转与正交对角化"）。

### 3.4 第三轮问题：仍未修复（本轮重复确认）

| 项 | 状态 |
|---|---|
| `linalg-049/052/054/057/064` answer 未答题面第二问 | **未修复**（answer 内容与上一轮逐字相同） |
| `prob-046` answer 仍为"1，即所有事件概率之和为1"（无 `$`、口径为"事件"） | **未修复** |
| `prob-043` steps[1]"重复多次"未定 M、steps[2] n=2 形态表述 | **未修复** |
| 许可证/分发（数据已推送、无 LICENSE）、哈希行尾（CRLF/LF） | **未修复**（见 §6） |
| 各类 info（objects 未登记公式、退化口径、answer 粒度等） | 多数未修（见 §6.3） |

---

## 4. 逐项检查结果

### 4.1 JSONL 结构与字段
4 个 JSONL 共 **63 行、全部合法 JSON 对象**：0 解析失败、0 重复键；12 字段齐全、类型正确、无空值、无未知字段。4 个 `dataset_*.json` 仍为 JSON 数组容器，**不能作为样本入口**（`S005`×4），与 JSONL 63/63 一致。

### 4.2 ID 唯一性
63 个唯一 ID、0 冲突；JSON/JSONL 镜像 63/63；`geom-020–031`、`linalg-048–070`、`prob-038–046` 连续，仅 `calc` 缺 14（info）。未改名、未去重。

### 4.3 problem / solution / answer 一致性
**记录级硬伤 0**。机械 `C007` 30 条提示经复核均为等价表述或纯文字结论差异；未答第二问的 5 条 `linalg-*` 见 §6.2。

### 4.4 scene_spec.objects / steps
63/63 非空（objects 2–9/条、steps 4–7/条），步骤编号 0 例外；**动画验证 0/63**。本轮第三轮列出的 10 处 scene_spec 语义冲突已全部修复；剩余为 objects 未登记既有公式文本等 info。

### 4.5 LaTeX 与中文进公式
公式内中文 0、全角 0、`$` 不配对 0、花括号/`\left`-`\right` 不配对 0、漏反斜杠 0、重复等式 0；1 条风格提示（`linalg-070` `u_1v_2`，合法）。

### 4.6 来源与许可证状态
- 63/63 `source=self-authored`、`license=Internal-Research-Use-Only`（`P002`/`P003`）。
- `manifest.json`：4/4 哈希匹配、`split=raw`、无验收语义（`MF000`）。
- 来源手稿 `dataset.md` 与交付池 **63/63 逐条一致**（`SRC008`）。
- **两项未决（quarantine）**：① 数据已入库并推送至 GitHub 远端（`origin/main=61e7922`），与"不公开分发"可能冲突，且仓库无 LICENSE；② 哈希绑定 CRLF 字节而 git 存 LF，跨平台克隆后不可复现。

### 4.7 精确重复与近重复
整条/`problem`/`scene_spec` 精确重复 0；近重复按项目实现 0 对；`linalg-049/064` 阈值敏感项见 §6.2。

### 4.8 四个板块的数量与分布

| 板块 | 条数 | 占比 | ID 区间 |
|---|---:|---:|---|
| 高等代数 | 23 | 36.5% | `linalg-048…070` |
| 数学分析 | 19 | 30.2% | `calc-*-001…020`（缺 14） |
| 解析几何 | 12 | 19.0% | `geom-020…031` |
| 概率论 | 9 | 14.3% | `prob-038…046` |
| **合计** | **63** | 100% | 35 个子类 |

拆分角色：`raw=63`，`train/eval/test/rejected=0`。

### 4.9 是否误把候选数据标成已验收训练数据
**否**：无 train/eval/test、无锁文件、无逐样本验收字段、动画 0/63；manifest 只登记事实；文档均声明 `candidate ≠ 已验收训练集`。仅 `DATASET_REVIEW.md` 头部"状态: clean"建议加限定词（`M010`，info）。

---

## 5. clean / quarantine / rejected 划分

| 状态 | 条数 | 说明 |
|---|---:|---|
| **rejected** | **1** | `prob-043`（scene_spec 动画与抽样分布矛盾） |
| **candidate** | **62** | 无硬伤，但存在 quarantine（answer 待补、动画未验证、许可证待转正等） |
| **clean** | **0** | 尚无一条同时满足动画已验证 + 许可证转正 + 元数据完备 |

文件级：4 个 JSONL 均 candidate（0 硬伤）；4 个 `dataset_*.json` 入口维度 rejected（`S005`）；`dataset.md` clean（来源镜像）。

---

## 6. 逐条问题清单

### 6.1 硬伤（5 条）

| # | 文件:定位 | ID | 代码 | 问题 | 建议 |
|---|---|---|---|---|---|
| 1 | `dataset_prob.jsonl:6` | `prob-043` | K-ANIM-ERR | scene_spec.steps[2]「初始设置 n=2，右侧直方图呈现出与总体相似的粗糙形态」与抽样分布矛盾：均匀总体下 n=2 的样本均值服从三角分布（Irwin–Hall，峰值 0.5、f(0.5)=2、方差 σ²/2=1/24），与高 1 矩形形态明显不同，会生成错误画面 | 人工改为"n=2 时样本均值呈三角分布，已明显不同于总体形态" |
| 2–5 | `dataset_{calc,geom,linalg,prob}.json` | — | S005 | JSON 数组不是合法样本入口（`DATASET_SCHEMA §1`） | 按 convert 流程使用 JSONL，原文件保留 |

> `prob-043` 的 hard 判定依据：prob 评审 20 万次模拟（直方图两端 3991/4002、中部 36028 的单峰）；Lead 复核该分布为标准 Irwin–Hall（n=2 均匀样本均值），与数据描述不符。

### 6.2 内容 quarantine（14 条）

| 文件:定位 | ID | 代码 | 问题 |
|---|---|---|---|
| `data/v1/manifest.json` | — | K-LICENSE-DIST | 数据已推送至 GitHub 远端，与 `Internal-Research-Use-Only`（不公开分发）可能冲突；仓库无 LICENSE |
| `data/v1/manifest.json` | — | K-HASH-EOL | 哈希绑定 CRLF 字节、git 存 LF，跨平台克隆后校验不可复现 |
| `dataset_linalg.jsonl:2` | `linalg-049` | K-ANS-WEAK | answer 未答题面第二问（几何意义） |
| `dataset_linalg.jsonl:5` | `linalg-052` | K-ANS-WEAK | answer 未答题面第二问（展开式意义） |
| `dataset_linalg.jsonl:7` | `linalg-054` | K-ANS-WEAK | answer 未答题面第二问（行列式为零的几何意义） |
| `dataset_linalg.jsonl:10` | `linalg-057` | K-ANS-WEAK | answer 未答题面第二问（可逆性几何意义） |
| `dataset_linalg.jsonl:17` | `linalg-064` | K-ANS-WEAK | answer 未答题面第二问（几何意义） |
| `dataset_linalg.jsonl:21` | `linalg-068` | K-ANS-WEAK | answer 未给正交矩阵 Q（题面要求"正交对角化"） |
| `dataset_prob.jsonl:9` | `prob-046` | K-ANS-WEAK | answer 仍为"1，即所有事件概率之和为1"，无 `$` 通式、口径为"事件" |
| `dataset_prob.jsonl:6` | `prob-043` | K-AMBIG | steps[1]"重复多次"未定独立重复次数 M |
| `dataset_prob.jsonl:1` | `prob-038` | K-SPEC-CONFLICT | "圆面积表示概率"在单位正方形内不可行（两圆并集 0.8 超出等周/面积约束），且 objects"矩形样本空间"与 steps"正方形"口径不一 |
| `dataset_calc.jsonl:19` | `calc-series-020` | K-SPEC-CONFLICT | objects"目标直线（灰色半透明）" vs steps"灰色虚线"；第一项正弦波颜色归属空档 |
| `dataset_calc.jsonl:5` | `calc-green-005` | K-SPEC-CONFLICT | steps"随机绘制向量箭头"无法体现被积场 (P,Q)=(-y,x)；偏导推导文本未登记进 objects |
| `dataset_linalg.jsonl:2` | `linalg-049` | K-NEAR-DUP | 与 `linalg-064` 题干模板逐字相同，阈值敏感（set 0.698113 / multiset 0.714286） |

### 6.3 内容 info（30 条，按类聚合）

| 类别 | 条数 | 记录 |
|---|---:|---|
| 元数据与内容不符 | 3 | `linalg-067`（"旋转与反射"但只演示旋转）、`linalg-054`（sub_category"行列式" vs Cramer 法则）、`linalg-058`（"底和高均为 1"仅对本矩阵成立） |
| objects ↔ steps 登记缺口 | 9 | `linalg-055/058/065/066/067/070`（缺秩/单位正方形/公式/块标注）、`calc-green-005`、`calc-limit-006`、`calc-param-improper-003`（登记式与展示式不同）、`calc-series-019`（名称/颜色）、`calc-series-015`（颜色/参考线） |
| answer 粒度/记法/风格 | 6 | `geom-024`/`geom-025`（缺半径）、`prob-041`（缺密度式）、`linalg-061`（矩阵与坐标并列）、`calc-answer-style`（4 条裸文本）、`prob-046`（steps 表述） |
| 表述精度 | 8 | `geom-026`（"平移 c"）、`geom-031`（"参数平移 2π"）、`geom-030`（方向歧义）、`linalg-050`（秩 0 退化/无具体矩阵）、`linalg-059`（非正交替换）、`linalg-060`（主轴口径）、`calc-series-017`（尾项带）、`calc-area-009`（被积函数替换） |
| 概率/统计表述 | 5 | `prob-042`（轨道收敛）、`prob-039`（"频数 m"）、`prob-040`（`P(λ)` 记法）、`prob-044`（缺"特异度"）、`prob-045`（开闭区间/支撑/坐标轴） |
| 其他 | 2 | `calc-series-018`（收敛域偏窄）、`linalg-051`（未画复平面面板）、`M010`（`DATASET_REVIEW.md` 状态词） |

> 完整逐条明细见 **`issues.jsonl`**（共 284 条）与 **`content_findings.jsonl`**（45 条：hard 1 / quarantine 14 / info 30）。

---

## 7. 汇总统计

- **严重度**：hard 5（S005×4 + `prob-043`）/ quarantine 140 / info 139（逐条问题共 284 条）。
- **逐条状态**：rejected 1 / candidate 62 / clean 0。
- **系统级 quarantine**：`A008`×63、`P002`×63。
- **结构化数据**：63 条、63 唯一 ID、35 子类、镜像 63/63、来源镜像 63/63、manifest 4/4。
- **重复**：精确 0；近重复按项目实现 0 对。
- **LaTeX**：公式内中文/全角/`$` 不配对/漏反斜杠/重复等式 全为 0。

---

## 8. 建议的下一步

1. **修 1 条硬伤**：`prob-043` steps[2] 改为"n=2 时样本均值呈三角分布"。
2. **补 answer 第二问（6 条，最易收尾）**：`linalg-049/052/054/057/064`、`linalg-068`（补 Q）；另 `prob-046` answer 补通式与"矩形面积"口径。
3. **许可证/分发与哈希（最高风险）**：确认 `origin` 可见性；若公开则撤下或转正许可证；补 LICENSE；加 `.gitattributes` 固定行尾并重绑 manifest 哈希。
4. **收尾表述**：`prob-043` 重复次数 M、`prob-038` 面积口径、`linalg-049/064` 同模板题与 5-gram 口径。
5. **元数据/登记一致性（info）**：`calc-green-005/limit-006/series-015/series-019/vol-012`、`linalg-050/051/054/055/058/059/060/061/065/066/067/070`、`geom-024/025/026/030/031`、`prob-039/040/041/042/044/045/046`。
6. **动画验证**：逐条过 `render_gate` 后登记 `code/render_status=verified/code_sha256`，在此之前保持 candidate。
7. **补齐编号**：确认 `calc-series-014` 是否应有记录。
8. **修复完成后重跑本审计**，再走 `make_manifest → data_check → split → freeze → preflight` 全链路。
9. 保留四轮审计目录以便追溯（`-v2`、`-v3`、`-v4` 及首轮 `dataset_audit_2026-10-02`）。

---

## 9. 产物清单

| 文件 | 内容 |
|---|---|
| `AUDIT_REPORT.md` / `AUDIT_REPORT.pdf` | 本报告 |
| `issues.jsonl` | 逐条问题（260 条） |
| `content_findings.jsonl` | 内容评审发现（21 条） |
| `record_status.jsonl` / `.csv` | 逐条状态与问题代码 |
| `summary.json` | 汇总统计 |
| `file_hashes.json` / `.sha256` | 9 个原始文件哈希 |

**声明**：本轮审计未修改任何数据集文件、未自动重命名 ID、未自动改写公式，未启动训练、未下载模型、未生成批量动画。
