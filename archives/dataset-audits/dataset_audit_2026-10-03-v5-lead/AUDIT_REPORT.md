# 候选数据集全量审计报告（第五轮 · 2026-10-03）

> 工具：`tools/dataset_audit.py`（纯标准库，只读；含 manifest 一致性、来源文档↔交付逐条比对、JSONL 结构/ID/一致性/scene_spec/LaTeX/重复/分布/验收语义九类检查）
> 复现命令：
> `python tools/dataset_audit.py --out dataset_audit_2026-10-03-v5-lead --content-findings dataset_audit_2026-10-03-v5-lead/content_findings.jsonl`
> 契约依据：`DATASET_SCHEMA.md`；证据：`issues.jsonl`、`summary.json`、`record_status.jsonl/.csv`、`file_hashes.*`
> 历史轮次：第一轮 `dataset_audit_2026-10-02`（63 条）、第二轮 `-v2`（62 条）、第三轮 `-v3`（63 条）、第四轮 `-v4`（63 条）
> **目录说明**：本轮开始时 `dataset_audit_2026-10-03-v5/` 与 `-v6/` 已由另一执行方创建并提交（仅机器门禁、`content_review.n=0`）。为避免覆盖他方产物，本报告的审计输出落在 **`dataset_audit_2026-10-03-v5-lead/`**；`-v5/` 已按 git HEAD 原样还原（`git status` 干净），`-v6/` 未改动。

---

## 0. 结论摘要

| 维度 | 结果 |
|---|---|
| 样本总量 | **63 条**（数学分析 19、高等代数 23、解析几何 12、概率论 9） |
| 逐条状态 | **rejected 0 / candidate 63 / clean 0** |
| 问题计数 | 硬伤 4（**全部为 JSON 数组容器 `S005`，记录级硬伤 0**）、quarantine 140、info 143（逐条共 287 条） |
| 内容级硬伤 | **0**（第四轮唯一的内容硬伤 `prob-043` 本轮已修复并复核） |
| 本轮改动范围 | **只有 `dataset_prob.jsonl` / `dataset_prob.json` / `dataset.md` 变化**；`calc`、`geom`、`linalg` 三个板块的 6 个文件与第四轮**逐字节相同** |
| JSONL 结构与字段 | 通过（0 解析错误、0 缺字段、0 空值、0 未知字段） |
| ID 唯一性 | 通过（63 唯一 ID、0 冲突；`geom-020–031` 连续；仅 `calc` 缺 14） |
| LaTeX / 中文进公式 | 硬性缺陷 **0** |
| 精确/近重复 | 精确 0；近重复按项目实现 0 对（`linalg-049/064` = 0.698113，多重集 0.714286） |
| 来源/许可证 | manifest 4/4 哈希匹配、`split=raw`；来源手稿与交付 63/63 逐条一致；**许可证/分发与哈希行尾两项仍未决** |
| 是否误标为已验收训练数据 | **否**（无 train/eval/test、无验收字段、动画 0/63 验证） |
| 动画验证状态 | 0/63 |

**一句话结论：本轮修复了第四轮唯一的内容硬伤（`prob-043` 三角分布），记录级硬伤归零；数据集仍是候选状态——剩余 14 条 quarantine 中 6 条是 `linalg-*` 的 answer 未答题面第二问，另有许可证/分发与哈希行尾两项跨轮未决风险。**

---

## 1. 审计范围与只读保证

| 类别 | 文件 |
|---|---|
| JSON 数组容器（待转换） | `dataset_calc.json`(19)、`dataset_geom.json`(12)、`dataset_linalg.json`(23)、`dataset_prob.json`(9) |
| 正式样本入口格式（候选） | `data/v1/raw/dataset_{calc,geom,linalg,prob}.jsonl`（已入库 git） |
| 来源手稿 | `dataset.md`（63 条） |
| 清单 | `data/v1/manifest.json`（4 条 entry，本轮 01:37:43 重绑） |
| 排除 | `reviews/**`、`.venv/**`、`runs/**`、其他 `dataset_audit_*` 产物 |

只读保证：本会话未修改任何数据文件；未自动重命名 ID、未自动改写公式；未启动训练、未下载模型、未生成批量动画。

---

## 2. 原始文件哈希（SHA256，本轮审计快照）

| 文件 | 字节 | 与第四轮对比 | 记录数 |
|---|---:|---|---:|
| `data/v1/raw/dataset_calc.jsonl` | 32927 | **SAME**（逐字节相同） | 19 |
| `data/v1/raw/dataset_geom.jsonl` | 18150 | **SAME** | 12 |
| `data/v1/raw/dataset_linalg.jsonl` | 30343 | **SAME** | 23 |
| `data/v1/raw/dataset_prob.jsonl` | 15355 | CHANGED（+52 B，01:37:43） | 9 |
| `dataset_calc.json` / `dataset_geom.json` / `dataset_linalg.json` | 32951 / 18167 / 30371 | SAME | 19/12/23 |
| `dataset_prob.json` | 15369 | CHANGED（+52 B） | 9 |
| `dataset.md` | 96899 | CHANGED（+52 B） | 63 |
| `data/v1/manifest.json` | 1604 | 重绑（4/4 哈希与当前文件匹配） | 4 entries |

> 完整的 SHA256 值见 `file_hashes.json` / `file_hashes.sha256`。审计期间 9 个数据文件哈希与 mtime 未变化。

---

## 3. 与上一轮（第四轮）的差异

### 3.1 变更范围

- **只有概率论板块与来源手稿变化**（3 个文件）；`calc`/`geom`/`linalg` 的 6 个文件哈希与第四轮**完全一致**。
- 因此本轮对后三个板块**沿用第四轮的复核结论**（已由独立评审逐条验算，且文件字节未变——结论仍有效），并对概率论板块**重新逐条复核**。

### 3.2 上一轮内容硬伤：已修复

| 项 | 第四轮 | 第五轮 |
|---|---|---|
| `prob-043` scene_spec.steps[2] | hard：「n=2 直方图呈现出与总体相似的粗糙形态」（与三角分布矛盾） | **已修复**：现为「初始设置 n=2，样本均值的直方图已呈现三角分布（Irwin–Hall 分布），与原始均匀总体明显不同」——与均匀总体下 n=2 样本均值的真实分布一致 |

### 3.3 其余项：状态未变（本轮无新增修复）

| 项 | 状态 |
|---|---|
| `linalg-049/052/054/057/064` answer 未答第二问 | **未修复**（文件字节未变） |
| `linalg-068` answer 未给 Q | **未修复** |
| `linalg-051` 复平面面板、`linalg-067` 元数据 | **未修复**（info） |
| `prob-046` answer 裸数字/口径 | **未修复** |
| `prob-043` steps[1] 重复次数 M | **未修复** |
| `prob-038` 面积等比口径 | **未修复** |
| `calc-series-020`/`calc-green-005` scene 登记 | **未修复**（文件字节未变） |
| 许可证/分发（`K-LICENSE-DIST`）、哈希行尾（`K-HASH-EOL`） | **未修复**：`.gitattributes` 仍不存在、仓库仍无 LICENSE、`data/v1/raw/*.jsonl` 仍在 git 且 `origin/main=61e7922` 已含数据（本地领先 4 个提交） |

> 附注：本轮提交信息提到 `A7 冻结写保护 / A6 统一入口门禁 / A8 防泄漏规范化哈希 / G4 类型契约` 与「全量 200+29 通过」——属**代码与测试**改动，不在本审计（数据集）范围内；其中「规范化哈希」尚未体现在数据侧（manifest 仍绑定 CRLF 字节，见 §6.2 `K-HASH-EOL`）。

---

## 4. 逐项检查结果

### 4.1 JSONL 结构与字段
4 个 JSONL 共 **63 行、全部合法 JSON 对象**：0 解析失败、0 重复键；12 字段齐全、类型正确、无空值、无未知字段。4 个 `dataset_*.json` 仍为 JSON 数组容器，**不能作为样本入口**（`S005`×4），与 JSONL 63/63 一致。

### 4.2 ID 唯一性
63 唯一 ID、0 冲突；镜像 63/63；`geom-020–031`、`linalg-048–070`、`prob-038–046` 连续，仅 `calc` 缺 14（info）。

### 4.3 problem / solution / answer 一致性
**记录级硬伤 0**。机械 `C007` 30 条均为等价表述或纯文字结论差异；`linalg-*` 未答第二问的 6 条见 §6.2。

### 4.4 scene_spec.objects / steps
63/63 非空（objects 2–9/条、steps 4–7/条），步骤编号 0 例外；**动画验证 0/63**。第四轮列出的 scene 问题中，`prob-043` 已修复；其余（`calc-series-020`、`calc-green-005`、`prob-038`）仍开放。

### 4.5 LaTeX 与中文进公式
公式内中文 0、全角 0、`$` 不配对 0、花括号/`\left`-`\right` 不配对 0、漏反斜杠 0、重复等式 0；1 条风格提示（`linalg-070` `u_1v_2`）。

### 4.6 来源与许可证状态
- 63/63 `source=self-authored`、`license=Internal-Research-Use-Only`。
- `manifest.json`：4/4 哈希匹配、`split=raw`、无验收语义字段。
- 来源手稿与交付池 **63/63 逐条一致**。
- **两项跨轮未决（quarantine）**：数据已推送到 GitHub 远端（与"不公开分发"可能冲突，且无 LICENSE）；哈希绑定 CRLF 字节（跨平台克隆不可复现）。

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
**否**：无 train/eval/test、无锁文件、无逐样本验收字段、动画 0/63；manifest 只登记事实；文档声明 `candidate ≠ 已验收训练集`（`DATASET_REVIEW.md` 头部状态词建议加限定，`M010` info）。

---

## 5. clean / quarantine / rejected 划分

| 状态 | 条数 | 说明 |
|---|---:|---|
| **rejected** | **0** | 记录级硬伤 0（第四轮 1 条已修复） |
| **candidate** | **63** | 每条至少带 A008（动画未验证）+ P002（许可证待转正）两项系统级 quarantine |
| **clean** | **0** | 尚无一条同时满足动画已验证 + 许可证转正 + 元数据完备 |

文件级：4 个 JSONL 均 candidate（0 硬伤）；4 个 `dataset_*.json` 入口维度 rejected（`S005`）；`dataset.md` clean。

---

## 6. 逐条问题清单

### 6.1 硬伤（4 条，均为结构/入口维度）

| # | 文件 | 代码 | 问题 | 建议 |
|---|---|---|---|---|
| 1–4 | `dataset_{calc,geom,linalg,prob}.json` | S005 | JSON 数组不是合法样本入口（`DATASET_SCHEMA §1`） | 按 convert 流程使用 JSONL，原文件保留 |

### 6.2 内容 quarantine（14 条）

| 文件:定位 | ID | 代码 | 问题 | 跨轮 |
|---|---|---|---|---|
| `data/v1/manifest.json` | — | K-LICENSE-DIST | 数据已推送至 GitHub 远端，与 `Internal-Research-Use-Only`（不公开分发）可能冲突；仓库无 LICENSE | 第 4/5 轮 |
| `data/v1/manifest.json` | — | K-HASH-EOL | 哈希绑定 CRLF 字节、git 存 LF，跨平台克隆后校验不可复现 | 第 4/5 轮 |
| `dataset_linalg.jsonl:2` | `linalg-049` | K-ANS-WEAK | answer 未答题面第二问（几何意义） | 第 4/5 轮 |
| `dataset_linalg.jsonl:5` | `linalg-052` | K-ANS-WEAK | answer 未答题面第二问（展开式意义） | 第 4/5 轮 |
| `dataset_linalg.jsonl:7` | `linalg-054` | K-ANS-WEAK | answer 未答题面第二问（行列式为零的几何意义） | 第 4/5 轮 |
| `dataset_linalg.jsonl:10` | `linalg-057` | K-ANS-WEAK | answer 未答题面第二问（可逆性几何意义） | 第 4/5 轮 |
| `dataset_linalg.jsonl:17` | `linalg-064` | K-ANS-WEAK | answer 未答题面第二问（几何意义） | 第 4/5 轮 |
| `dataset_linalg.jsonl:21` | `linalg-068` | K-ANS-WEAK | answer 未给正交矩阵 Q | 第 4/5 轮 |
| `dataset_prob.jsonl:9` | `prob-046` | K-ANS-WEAK | answer 仍为"1，即所有事件概率之和为1"，无 `$` 通式、口径为"事件" | 第 3/4/5 轮 |
| `dataset_prob.jsonl:6` | `prob-043` | K-AMBIG | steps[1]"重复多次"未定独立重复次数 M | 第 3/4/5 轮 |
| `dataset_prob.jsonl:1` | `prob-038` | K-SPEC-CONFLICT | "圆面积表示概率"在单位正方形内不可行，且 objects"矩形样本空间"与 steps"正方形"口径不一 | 第 4/5 轮 |
| `dataset_calc.jsonl:19` | `calc-series-020` | K-SPEC-CONFLICT | objects"目标直线（灰色半透明）" vs steps"灰色虚线"；第一项正弦波颜色归属空档 | 第 4/5 轮 |
| `dataset_calc.jsonl:5` | `calc-green-005` | K-SPEC-CONFLICT | steps"随机绘制向量箭头"无法体现被积场 (P,Q)=(-y,x)；偏导推导文本未登记 | 第 4/5 轮 |
| `dataset_linalg.jsonl:2` | `linalg-049` | K-NEAR-DUP | 与 `linalg-064` 题干模板逐字相同，阈值敏感（set 0.698113 / multiset 0.714286） | 第 3/4/5 轮 |

### 6.3 内容 info（34 条，按类聚合）

| 类别 | 条数 | 记录 |
|---|---:|---|
| 元数据与内容不符 | 3 | `linalg-067`（"旋转与反射"但只演示旋转）、`linalg-054`（sub_category vs Cramer 法则）、`linalg-058`（"底和高均为 1"仅对本矩阵成立） |
| objects ↔ steps 登记缺口 | 9 | `linalg-055/058/065/066/067/070`、`calc-green-005`、`calc-limit-006`、`calc-param-improper-003`、`calc-series-019`、`calc-series-015` |
| answer 粒度/记法/风格 | 9 | `geom-024`/`geom-025`（缺半径）、`prob-039`（缺频率口径）、`prob-041`（缺密度式）、`prob-045`（缺 0 值说明）、`linalg-061`（矩阵与坐标并列）、`calc-answer-style`、`prob-046`（steps 表述） |
| 表述精度 | 8 | `geom-026/030/031`、`linalg-050/059/060`、`calc-series-017`（尾项带）、`calc-area-009`（被积函数替换） |
| 概率/统计表述 | 4 | `prob-042`（轨道收敛）、`prob-040`（`P(λ)` 记法）、`prob-044`（缺"特异度"）、`prob-038`（`P(A|B)` 宜作 `P(A\mid B)`） |
| 其他 | 1 | `calc-series-018`（收敛域偏窄）、`linalg-051`（未画复平面面板）、`M010`（状态词）、`prob-043`（`K-VERIFIED-OK`：三角分布已修复） |

> 完整逐条明细见 **`issues.jsonl`**（共 287 条）与 **`content_findings.jsonl`**（48 条：quarantine 14 / info 34）。

---

## 7. 汇总统计

- **严重度**：hard 4（全部 S005）/ quarantine 140 / info 143。
- **逐条状态**：rejected 0 / candidate 63 / clean 0。
- **系统级 quarantine**：`A008`×63、`P002`×63。
- **结构化数据**：63 条、63 唯一 ID、35 子类、镜像 63/63、来源镜像 63/63、manifest 4/4。
- **重复**：精确 0；近重复按项目实现 0 对。
- **LaTeX**：公式内中文/全角/`$` 不配对/漏反斜杠/重复等式 全为 0。

---

## 8. 建议的下一步

1. **补 answer 第二问（6 条，最易收尾）**：`linalg-049/052/054/057/064`、`linalg-068`（补 Q）；`prob-046` answer 补通式与"矩形面积"口径。
2. **许可证/分发与哈希（最高风险，建议优先）**：确认 `origin` 可见性；若公开则撤下数据或完成许可证转正；补 LICENSE；加 `.gitattributes` 固定行尾并为 manifest 绑定规范化哈希（提交信息中的 "A8 规范化哈希" 需落到数据侧）。
3. **收尾表述**：`prob-043` 重复次数 M、`prob-038` 面积口径、`linalg-049/064` 同模板题与 5-gram 口径、`calc-series-020`/`calc-green-005` scene 登记。
4. **元数据/登记一致性（info）**：`calc-*` 与 `linalg-*`、`geom-024/025/026/030/031`、`prob-039/040/041/042/044/045/046` 的具体条目见 §6.3。
5. **动画验证**：逐条过 `render_gate` 后登记 `code/render_status=verified/code_sha256`，在此之前保持 candidate。
6. **补齐编号**：确认 `calc-series-014` 是否应有记录。
7. **修复完成后重跑本审计**，再走 `make_manifest → data_check → split → freeze → preflight` 全链路。
8. 保留五轮审计目录以便追溯（`dataset_audit_2026-10-02`、`-v2`、`-v3`、`-v4`、`-v5`（他方机械运行）、`-v5-lead`（本报告）、`-v6`）。

---

## 9. 产物清单

| 文件 | 内容 |
|---|---|
| `AUDIT_REPORT.md` / `AUDIT_REPORT.pdf` | 本报告 |
| `issues.jsonl` | 逐条问题（287 条） |
| `content_findings.jsonl` | 内容评审发现（48 条） |
| `record_status.jsonl` / `.csv` | 逐条状态与问题代码 |
| `summary.json` | 汇总统计 |
| `file_hashes.json` / `.sha256` | 9 个原始文件哈希 |

**声明**：本轮审计未修改任何数据集文件、未自动重命名 ID、未自动改写公式，未启动训练、未下载模型、未生成批量动画。
