# 草稿批次独立复核回执

本轮完成 Claude 的 batch4–12，共 264 条草稿。修订 10 条记录，全部保留题目 ID 和条数；254 条未修改记录逐行保留原始字节，18 份来源文件保留完整原件和完整候选副本。

**判定：修订后 264 条数学内容合格，264 条场景文字合格，材料版本绑定通过。** 原稿有 8 条正文问题和 8 条场景条件或记号问题，二者合计涉及 10 条记录。该判定只适用于本次归档的候选版本，不构成实际动画渲染、训练与评测语义隔离或生产开放的通过证明。

| ID | 问题及修复 |
| --- | --- |
| draft-c33-03 | 块逆列向量缺行分隔符；改成 $(-\frac12,\frac12)^{\mathsf T}$，复验完整逆矩阵。 |
| draft-c37-04 | 过程与答案中的 $Q$ 缺行分隔符；改成 $\begin{pmatrix}\frac32&\frac32\\\frac12&-\frac12\end{pmatrix}$，复验 $PQ$。 |
| draft-c12-05 | 补齐题干要求的一致收敛与积分换极限充分性：积分误差不超过区间长度乘一致误差；同步补场景。 |
| draft-c19-03 | 显式定义截面坐标 $\xi,\eta$，统一为 $\xi^2+\eta^2/5=1$，同步改场景。 |
| draft-c32-05 | 非齐次陪集断言补“相容”条件，并明确无解分支；同步改场景题干。 |
| draft-c27-04 | 夹角定义包含 $k=0$ 的直角边界，取消仅称“锐角”的不完整用词。 |
| draft-c38-02 | 交空间明确写成 $\operatorname{span}\{(x^2-1)^2\}$；同步改场景。 |
| draft-c41-05 | 区分尺寸至少为 $k$ 的块数 $r_k-r_{k-1}$ 与恰为 $k$ 的块数 $2r_k-r_{k-1}-r_{k+1}$。 |
| draft-c35-03 | 场景标签统一使用 $(n_+,n_-,n_0)$ 三元惯性。 |
| draft-c01-03 | 场景参数斜率公式补 $t\ne0$ 条件，保留 $t=0$ 竖直切线独立分支。 |

逐题推导核验依据见 independent-draft-review-264.jsonl；其中每条均绑定原始来源、原始记录指纹、候选记录指纹及独立核验说明。verify_draft_math.py 使用精确符号运算完成 165 项恒等式检查，覆盖 142 条记录；其余论证和收敛、唯一性、适用条件由逐题人工推导审阅覆盖，不将计算机代数通过等同于全部证明自动通过。

verify_draft_delivery.py 只读重建 18 份来源及全部 264 条记录，检查明确补丁、行号、逐行原件保留、修订的数学指纹、两处矩阵实际维数及回执版本。检查结果见 draft-verification.json。

修订正文详见 DRAFT_CORRECTIONS.md；完整修订数据在 candidate-sources/，完整原件在 source-originals/，逐字段前后值在 draft-corrections-10.jsonl。归档边界与全部文件 SHA-256 见 draft-delivery-manifest.json。原始 Claude 提交在 received/，未覆盖其报告或冻结材料。

后续评测及测试材料在 REVIEW_LEDGER.json 中排队，独立复核未完成的条目仍标 PENDING。原生渲染 UNVERIFIED，语义隔离 NOT_ESTABLISHED，数据准入 PENDING，生产 CLOSED。
