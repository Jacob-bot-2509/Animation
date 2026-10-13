# linalg-048 改写候选 · 独立复核报告（2026-10-06）

> 复核对象：提交 `889027d`（10-06 01:07）新增的
> `reviews/2026-10-06-linalg048-rewrite/linalg-048-rewrite-candidate.json`
> 背景：`data_check` 因 **2 对结构泄漏候选**（`eval-linalg-015-s1`、`test-linalg-025` 各自 vs 训练池 `linalg-048`）不通过；本候选把 `linalg-048` 从**对称矩阵 `[[2,1],[1,2]]` 的几何意义**改写为**水平剪切 `[[1,3],[0,1]]` 的几何意义**。
> 复现：`python dataset_audit_2026-10-06-linalg048/_verify.py`（只读）

---

## 0. 结论

| 检查 | 结果 |
|---|---|
| 数学正确性（Lead 独立自算） | **通过**——det、基向量像、正方形像、斜率、面积全部与候选一致 |
| 结构泄漏（替换后全量再筛 21,090 对） | **候选对 0**（旧题：2 对） |
| 与两条查询题的近重复（5-gram） | 0.2568 / 0.1910，全池最大 0.2985 ≪ 0.7 |
| 字段 / LaTeX / scene_spec / answer↔solution | **无 hard**；仅仓库既有 `P002`（许可证）、`A008`（动画未验证）两条系统级 quarantine |
| **是否已生效** | **否——目前仍是候选，数据集未改动** |

---

## 1. 数学自算（不依赖其脚本）

对 $A=\begin{pmatrix}1&3\\0&1\end{pmatrix}$：

| 断言（候选） | 我的自算 |
|---|---|
| $A(x,y)=(x+3y,\;y)$ | ✓ 取 $(x,y)=(7,2)$ 得 $(13,2)$ |
| $\vec e_1=(1,0)$ 不动、$\vec e_2=(0,1)\mapsto(3,1)$ | ✓ |
| $\det A=1\cdot1-3\cdot0=1$ | ✓ |
| 单位正方形 $[0,1]^2$ 顶点像 $(0,0),(1,0),(3,1),(4,1)$ | ✓（逐个代入一致） |
| 底边长 $1$、高 $1$、面积仍为 $1$ | ✓（面积因子 $\lvert\det\rvert=1$） |
| 水平线 $y=c$ 仍水平、整体右移 $3c$ | ✓ $(x,c)\mapsto(x+3c,c)$ |
| 竖直线 $x=c$ 变为过 $(c,0)$、斜率 $1/3$ 的直线 | ✓ $(c,y)\mapsto(c+3y,y)$ |
| 该变换为水平剪切（$x$ 轴上点不动，越远平移越多） | ✓ 特征多项式 $(1-\lambda)^2$、$A\ne I$ 且不可对角化，正是剪切 |

> 改写后的解答**只讲几何、不再给出谱数据**，因此不再包含 `eval-linalg-015`（求特征值/特征向量并对角化）与 `test-linalg-025`（求谱分解）的答案信息。

---

## 2. 结构泄漏复筛（关键验证）

用项目自带 `animgtrain.structural_leakage.compare`（规则 `structure-candidates-v4`）：

| 对比 | 旧题 `[[2,1],[1,2]]` | **候选题 `[[1,3],[0,1]]`** |
|---|---|---|
| vs `eval-linalg-015-s1` | candidate=**True**（31/75） | candidate=**False**（31/74，reasons 空） |
| vs `test-linalg-025` | candidate=**True**（29/82） | candidate=**False**（29/81，reasons 空） |

**全量再筛**：以候选题替换 `linalg-048` 后，对 eval 300 条 × train 47 条、test 150 条 × train 47 条共 **21,090 对**逐对调用 `compare()` → **候选对 0**。与其提交自述"全量筛查全过"一致。

**近重复**：候选 vs 两条查询题 J=0.2568 / 0.1910；与全池最大 **0.2985**（`eval-linalg-006-s1`）≪ 0.7 阈值。

---

## 3. 记录级检查

- 必需字段齐全（id/category/sub_category/problem/solution/answer/scene_spec/source/license + 3 项可选元数据），键集合与现行记录一致；
- LaTeX：公式内无中文/全角，`$` 配对、花括号平衡，`\begin{pmatrix}` 等用法正常；
- scene_spec：objects 5 项 / steps 5 步（编号连续），**objects 与 steps 一一对应**（坐标轴→步1、单位正方形→步1/4、平行四边形→步4、两条水平线→步3、右下角文本→步2）；
- answer 与 solution 一致（`C007` info：等价表述）；
- 仅 `P002`（许可证）与 `A008`（动画未验证）两条**仓库级** quarantine，非本次改写引入。

---

## 4. ⚠️ 关键状态：候选**尚未应用**

- 候选只写入了 `reviews/2026-10-06-linalg048-rewrite/linalg-048-rewrite-candidate.json`；
- **三个训练池目录**（`data/v2/train/leakage-isolated-2026-10-05`、`-v2`、`-v3`）中的 `linalg-048` **仍是旧的对称矩阵版本**；
- 因此 `python tools/data_check.py --manifest data/manifest.json` **仍为不通过（exit 2）**，2 对结构泄漏候选仍在；
- `tools/prepare_linalg048_rewrite.py` 是"只准备 + 自检"脚本（输出已存在时 fail-closed），**不会自动改数据**。

### 应用时需同步完成（建议顺序）

1. 用候选内容替换现行训练池（活动池为 `v2/train/leakage-isolated-v3-2026-10-05`）中的 `linalg-048`，并落 UTF-8/LF；
2. 重跑 `data_check --manifest data/manifest.json` → 预期 2 对候选清零、exit 0；
3. **重绑哈希**：`data/manifest.json` 中该 train 条目的 sha256 + 重冻 `data/{eval,test}-v2.lock.json`（train 文件哈希变化会让冻结证据失效）；
4. 重跑隔离/近重复门禁与（若已接入）渲染门禁。

### 两点提醒

- 候选同时改动了**元数据取值**：`function_family` 矩阵变换→线性变换、`visual_style` 空间网格形变→空间几何图形、`efficiency_tags` 基向量追踪/网格拉伸→几何意义/剪切变换。准备脚本的 E 项只比较**键集合**、不校验元数据取值漂移，请确认这是有意为之。
- 旧 scene 含 NumberPlane 网格与基向量箭头，新版 scene 改为单位正方形+水平线（无基向量）——与 `A008`（动画未验证）一致：若后续要出动画，需按新版 scene 重写。

---

## 5. 产物

| 路径 | 内容 |
|---|---|
| `dataset_audit_2026-10-06-linalg048/_verify.py` | 本次只读复核脚本（数学自算 + 结构复筛 + 近重复 + 记录级检查） |
| `dataset_audit_2026-10-06-linalg048/LINALG048_REVIEW.md` / `.pdf` | 本报告 |
| `reviews/2026-10-06-linalg048-rewrite/linalg-048-rewrite-candidate.json` | 被复核的候选题（未改动） |

**声明**：本轮为只读复核；未修改任何数据、清单、锁或工具；所有写入均在本工作区复核目录内。
