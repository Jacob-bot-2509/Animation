# eval 换题清单(防泄漏屏拦截 5 题,用户裁决:换掉)

> 2026-10-04。防泄漏屏(考点签名一致 AND 5-gram≥2/5)拦截 5 道 eval 题:
> 与 train 题"同考点+句式几乎相同+只换数字/矩阵"。用户裁决:出 5 道新题替换。

## 待替换的 5 题与出题约束

| problem_id | 考点签名 | 被拦原因(与 train 的 J5) | 新题约束 |
|---|---|---|---|
| eval-linalg-014 | 高等代数/特征值对角化 | 与 linalg-049/064 句式全同仅换矩阵(J5=1/2) | 保留"特征值+对角化"考点;任务形式/矩阵构造要不同(如:含参数的矩阵、给定特征值反求矩阵、证明题) |
| eval-linalg-019 | 高等代数/其他[二次型] | 与 linalg-059 仅差一个系数(J5=20/47) | 保留"二次型化标准形"考点;系数/问法不同(如:三元二次型、含参二次型分类) |
| eval-linalg-021 | 高等代数/其他[二次型] | 与 linalg-060 仅差一个 4yz 项(J5=22/45) | 保留"二次型正定判定"考点;如:含参数 a 的正定讨论、半正定判定 |
| eval-linalg-031 | 高等代数/其他[λ-矩阵] | 与 linalg-066 仅差一个矩阵元(J5=29/63) | 保留"最小多项式/若尔当形"考点;如:不同若尔当块组合、由若尔当形反推矩阵性质 |
| eval-linalg-032 | 高等代数/其他[λ-矩阵] | 与 linalg-065 同为 λ-矩阵不变/初等因子(J5=19/35) | 保留"λ-矩阵标准形"考点;如:含参数的 λ-矩阵、给定初等因子构造 λ-矩阵 |

**硬约束**:新题题文与任意同考点 train 题的 5-gram Jaccard 必须 < 2/5
(任务形式/结构差异足够大;写好后我逐题核验)。

## 每题需要的完整字段(入场契约)

- category(高等代数)/ sub_category(同原题)
- problem:题干(含 $...$ LaTeX;公式内不得有中文)
- solution ×3(同题多解:同一 problem_id 题干相同、method 唯一,
  如 特征方程/几何反射/对合性 这类命名)
- answer:可判分终答
- scene_spec:objects/steps 动画规格
- function_family / visual_style / efficiency_tags
- source=self-authored / license=Internal-Research-Use-Only

## 连带更新(换题后我执行)

1. data/v2/eval/dataset_eval.jsonl 更新 15 行(5 题 × 3 解法)+ raw 数组重生成
2. eval-v2 冻结锁重签(哈希绑定)
3. B5 标注集 2 对同步:annotation 中 (eval-geom-001×eval-linalg-031) 与
   (eval-calc-014×eval-linalg-021) 的 text_b 更新为新题文、jaccard 重算
   (均为跨科目负例,标签"不重复"不变)→ b5 校准报告重生成
4. data_check + preflight 复跑,门禁转绿

## 交付方式

你写 5 道新题的**题干+考点意图**(一句话即可,如"含参数 a 的二次型正定讨论"),
我来按同题多解格式补全 solution/answer/scene_spec 等字段草案,你审后落库。
