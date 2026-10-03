# 答案与训练准备回信复验（2026-10-03）

回信：msg_1790963961389_185、msg_1791000527063_192。
最新基线：602c792；包含主力 A6/B7 修复、Codex 答案类型守卫及训练准备材料。
结论：A6/A7/A8、B7 本轮已知反例复验关闭；七条补全答案与独立公式核对一致。训练准备保持 provisional/candidate，实际 preflight 为 NOT READY，未启动训练。

## 验证结果

- 主力稳定提交 1c9d332：213 passed + 29 subtests（6.49 秒）。
- Codex 发现 answer 非空列表/对象仍被 manifest 放行，新增两项测试修前 2 failed；补字符串类型守卫后 215 passed + 29 subtests（6.70 秒）。
- 守卫及测试已纳入 602c792，最新全量 **223 passed + 29 subtests passed**（6.76 秒）。
- 本轮仅新增审查证据、更新备忘录及类型契约说明；此前源码小修已合入。真实输入哈希在本轮探针前后不变。
- [独立探针](probe.py)、[原始结果及哈希](results.json)。

期间首次测试与主力修改重叠，曾出现两条旧“合格”夹具缺 answer 的失败；主力补全夹具后，稳定提交重跑通过。没有删除新门禁或把失败改成放行。

## A6 / A7 / A8 / B7

| 项目 | 复验结论 |
|---|---|
| A6 错正文类型 | 非空 list/dict 冒充 problem/solution，manifest 返回 1 |
| A6 缺 answer | answer=null 返回 quarantine、exit 2，不再 ok=true |
| A6 错答案类型 | 非空 answer 列表/对象返回 1；与正式入场字符串契约一致 |
| A6 旧 ID 别名 | 两条 sample_id 相同、题干不同，统一 ID 提取后检出同集合重复 |
| A6 空字段 CLI | 空 JSONL 的 check_fields CLI 返回 1 |
| A7 冻结写保护 | 已合入上一轮 Codex 守卫与六项边界回归；原覆盖反例仍拒绝 |
| A8 正文防泄漏 | 同题换 ID/元数据/解法的原反例仍检出 |
| B7 元数据类型 | 非字符串函数族/风格、非列表标签被拒绝；场景文本列表与分类/来源规则保持 |

已补明 DATASET_SCHEMA.md 的具体类型规则及 legacy ID 支持范围。关闭范围为现有已知反例，不等于所有任务格式或 READY 资产证据已经验收。
C10 保留：fields.check_jsonl 核心函数仍以缺失列表表达结果，空文件返回 []；当前 CLI 已显式拦空输入，新调用方必须使用相同规则或改核心接口，不能用空列表声称完成完整样本验收。

## 七条答案补全

读取当前题干、解答、答案逐条核对，没有执行或解析数据中的 Python 代码。

| ID | 独立核对 |
|---|---|
| linalg-049 | A=[[2,1],[1,2]]，特征值 3/1，方向 (1,1)/(1,-1) 的特征方程残差为零；新增方向拉伸说明正确 |
| linalg-052 | 三阶展开 1+3(x−1)+3(x−1)²+(x−1)³ 与 x³ 差为零；精确相等及导数系数说明齐全 |
| linalg-054 | 解为 (2,1)，系数行列式 −3；行列式为零时平行/重合的普通直线几何说明与题意一致 |
| linalg-057 | 给出的逆矩阵与 A 相乘为单位阵，逆变换的几何意义已补 |
| linalg-064 | 特征值 3/2 对应 (1,0)/(1,−1)，两残差为零；拉伸说明齐全，分类与 049 一致 |
| linalg-068 | QᵀQ=I、QᵀAQ=diag(3,1)，正交对角化结果完整 |
| prob-046 | 几何级数 Σ(k≥1)2⁻ᵏ=1，与单位正方形面积一致，终答能够独立理解 |

本地 SymPy 使用审查者手写固定公式做核对，不对数据字符串调用 eval/sympify。
四组 JSON 数组与 JSONL、dataset.md 一致；v7 审计 63 条及四哈希匹配，全部为 candidate。审计工具计数不覆盖答案完整性全部维度，不能从 quarantine 数量未变推断修复无效或从数量变化推断数学已验收。

## 训练前准备材料

- TRAIN_PREP_PLAN.md 和 train_config.template.json 任务一致：problem + solution → scene_spec 动画规划；没有声称已有 Manim code 标签。
- 模型、路线和未知超参数为 TBD，模板为说明契约，不是已接入训练器的可执行配置。
- manifest-train.json 四条目均为 provisional train，路径/哈希/大小与当前原始文件匹配；原 raw manifest 保留。
- 候选训练清单 SHA256：8f1c9b98bfc7c07137645b01555e596f798d750912ab2dd7201290e5569e8353。
- 独立 data_check：4 条目，0 问题、0 quarantine，exit 0。
- 独立 preflight 命令：tools/preflight.py --ready --run-id prep-check-0001 --manifest data/v1/manifest-train.json。
- 实测 exit 1、NOT READY。GPU、数据清单、固定可信渲染/数学环境样例通过；模型目录、运行快照、近重复校准、eval/test 冻结缺失导致阻断。
- 环境样例通过不是当前动画资产验收；63 条仍缺实际 code/render_status/code_sha256。
- 没有执行 split、冻结真实数据、训练、下载、安装或发布。

## 后续阶段

B1 完整运行配置/重放、B2 当前资产验收、B3 独立评测集合与指标、B4 完整隔离、B5 正式校准、B6 多文件恢复继续按验收点补齐。C 类小问题继续备忘，不扩大本轮范围。
