# 入场修复回信第二轮复验（2026-10-03）

基线：48a6fc8，另含 Codex 跨文件 ID 小修；完整 HEAD/源码哈希见 results.json。
回信：Claude Code msg_1790959017332_162。
结论：DI1/DI3 原反例通过；DI2 的 CLI 与同名文件遗漏经 Codex 补齐后通过，A3 已知反例关闭。
真实数据仍有独立确认的三条数学/动画语义错误，记 A4；入场 clean 不代表内容或训练已验收。

## 代码修复与验证

- 原全量：182 passed + 29 subtests，6.79 秒。
- 原独立反例：空 JSONL/空路径列表、ID/正文容器、scene_spec 错结构现在均拒绝。
- DI2 原实现遗漏：CLI check 逐文件检查；intake_report 使用 basename 识别文件，不同目录同名文件漏检。
- Codex 小修：CLI check 统一用 intake_report 聚合结果；global_ids 以 resolve 后完整文件路径与行号识别来源，报告显示双方位置。
- 新增 tests/test_intake_cross_file_review.py 四项：CLI 异名/同名文件重复拒绝、同名汇总定位、合法唯一 ID 通过。
- 新测试修前 3 failed / 1 passed，修后全量 **186 passed + 29 subtests**，6.30 秒。
- 检查退出码由聚合结论统一：硬伤 1、仅 quarantine 2、clean 0。已有输入覆盖保护保持通过。
- 命令：PYTHONIOENCODING=utf-8、PYTHONUTF8=1、PYTHONDONTWRITEBYTECODE=1；.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider。
- [独立探针](probe.py)、[原始结果与当前数据哈希](results.json)。git diff --check（本轮代码）通过。

## 当前数据与新审计绑定

- 当前 JSONL 共 62 条，入场结构检查 clean，manifest 文件哈希通过；实际近重复校准仍未完成。
- dataset_audit_2026-10-03-v2 的 62 条计数及四个 JSONL SHA256 均与当前输入一致。旧 current 目录仍保留为历史证据。
- 新审计记录 59 candidate、3 rejected。工具总计 7 hard 中，有 4 条仅是 JSON 数组容器不应当成样本入口，不能理解为 7 条坏 JSONL 样本。
- 本轮独立核对下列 3 条语义问题，没有运行 untracked 审计工具，也未把全部启发式提示当成数学事实。
- 原始数据、JSON 镜像、manifest 均未修改。独立探针和代码回归仅写临时合成文件。

## A4：正式使用前修正的三条数据内容问题

| 样本 | 当前错误 | 独立依据与修正方向 |
|---|---|---|
| calc-area-010 | solution/answer 和动画最后结果给 e²/2−1 | 题干由 ln(x)、−x+e+1 和 x 轴围成的区域，上边界分别为 ln(x)（1 至 e）和直线（e 至 e+1）；两段积分为 1 和 1/2，总面积 **3/2**。当前第一段误用直线减曲线，换了区域 |
| prob-040 | 动画步骤 3 让二项柱状图中心向右移动 | 泊松极限需 np 保持/趋近固定 λ。沿当前初始 n=10,p=0.5，选 λ=5，n=10/50/100、p=5/n 时均值均为 5。应展示向固定 P(5) 收敛，中心不右移；方差可由 2.5 接近 5，不能把形状变化简单说成完全不变 |
| linalg-058 | 动画步骤 2 说竖直网格线倾斜 | E=[[1,0],[3,1]] 将 (x,y) 映为 (x,y+3x)。竖线 x=c 的像仍 x=c；水平线 y=c 的像为 y=3x+c，倾斜的是原水平线。solution/answer 本身正确，需改动画描述 |

面积用本地 SymPy 直接积分、剪切用矩阵乘法验证；没有解析或执行数据中的代码。
prob-040 的上述反例说明固定 λ 路径必须在动画参数中显式保持，不代表所有任意 n/p 变化路径都固定中心。

## 协作与范围

已发 Claude Code msg_1790959601142_163、msg_1790959716450_164；小修源码交回主力，可纳入，未提交 git。
请由主力按数据修改授权约定同步 dataset.md、JSON 数组、JSONL 及新 manifest，修后重新绑定审计，不能复用修前 SHA256。
A3 关闭不等于 A4 或全链路 READY 关闭。正式资产验收、隔离、校准等原 B 组条件与 C 类延期维持。
