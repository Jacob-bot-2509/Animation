# Claude Code 新回执与语义验收复验

已跟进 `cca27bab5d3bfada53562be1735cd05ca8e244c7`（2026-10-06 12:12:14）。Claude Code 完成新的真实 AppContainer 渲染、标准 v2 绑定回执及一个**未激活提案**。回执通过独立核验；所谓全量人工语义验收没有通过本次独立审阅。

## 实际完成与未完成

- 12:06–12:07 新执行目录 `execution-64ba8747d92b41e384b9f125ad6167c9`。视频为248帧、15帧每秒，时长 \(\frac{248}{15}\) 秒；raw SHA仍为 `da928b2d6d48185f3627b7c8e14549092cd530dd14a6bda870530c8b5e7d2f98`，与前轮已审阅视频相同。
- `v3-receipt-bound/receipt.json` raw SHA `4e81d921f2fb3ad5e90ab8e7372fa898203441bf8011008774f2d1b45cfbee25`。复验候选、完整输入、296唯一题人口、32项源码/媒体/日志绑定和实际隔离字段全部通过，accepted仍为false。这部分已补齐，不必继续说“缺绑定回执”。
- 当前 `manual-acceptance.json` raw SHA为 `96aadcf6d1bffc492ab222bd6434429b668eb6e3be9a4a3eb66af25a620386ca`。239条理由来自关键词/默认规则，其中94条使用同一句兜底文字。57条硬编码逐题理由的存在，不能证明另外239条真实完成审阅。
- `proposal.json` raw SHA `4e7c585bdbd84adda86b5d4e708d7dcef31e6da088eb527d22a8b2ae8b4a9355`。它仅通过现有协议的格式/绑定检查；协议不能证明字符串理由是真的。其“MANUAL_REVIEW_VERIFIED”不能替代本次独立语义结论，**不得据此做正式版本切换**。原件已保留，拒绝记录另见 `acceptance-rejection.json`。

## 可复现的问题及数学理由

旧生成器在不比较核心结构的情况下总填 `DIFFERENT_CORE_TASK`。合成的同剪切题“横坐标改为x+3y，纵坐标不动，说明单位正方形的像和面积”也被判为不同核心（仅为反例，未写入任何真实数据）。

训练内的 `linalg-058` 使用
\[
E=\begin{pmatrix}1&0\\3&1\end{pmatrix},\quad
A=\begin{pmatrix}1&3\\0&1\end{pmatrix},\quad
P=\begin{pmatrix}0&1\\1&0\end{pmatrix},\quad E=PAP.
\]
换横纵坐标即可把水平剪切变成竖直剪切。逐点映射、单位正方形的像、\(\det=1\)和面积保持的解法结构相同，不能因为方向或矩阵不同就标“不同核心”。同训练 split 的变体可以保留，但必须诚实标注，另作密度检查；这本身不构成跨训练—评测/测试泄漏。

`test-geom-016` 的单位圆像通过反代得到 \((X-Y)^2+Y^2=1\)，它与候选的单位正方形像确有对象/计算步骤差异，但两题共享水平剪切及 \(|\det A|=1\) 的面积子任务。不能只凭换系数/换图形自动放行，仍需按严格核心任务规则裁决。此处记录未决风险，没有假装已经证明全题泄漏或无泄漏。

`test-linalg-036` 含初等行加法矩阵行列式为1的子情况；候选也明确计算 \(\det A=1\)。写“候选没有行列式内容”不符合实际内容，即使最后能证明任务不同，也需要正确的逐题依据。

## 直接修复

- `tools/review_linalg048_pairs.py` 现在只生成 `linalg048-semantic-review-packet-v1` 待审包：先完整核验真实绑定回执，附候选和296个唯一题的**496份完整来源记录**，包含推导、答案和所有场景变体。reviewer、视觉判定、语义verdict/reason均留空，accepted与training_admitted为false。没有关键词自动通过分支，也不再自动写manual-acceptance-v2。
- `tools/render_shear_scene_v2.py` 原来声称“fully bound”但仍发布旧自定义回执。现在作为当前admit入口的兼容委托，必须指定新的`--out`，使用同一完整绑定协议，不覆盖历史v1回执。
- 新增 `tests/test_linalg048_review_packet.py`，14项实质回归通过，覆盖同核心反例保持待审、全场景覆盖、错绑/缺失/重复/人口变化、已有/外部输出路径、兼容入口及协议拒绝。真实CLI构建待审包rc=0；将待审包交给apply得到rc=2且无提案输出。
- 未修改admit/apply或已绑定的32项核心来源，修复后再次独立核验新回执仍有效。没有重新运行Manim或模型训练，没有改正式数据、两锁及资产状态。

原始代码和证据保存在 `before/`，后续旧文件不会由本轮覆盖。当前活动资产仍1/497、NOT READY。下一步是真实逐题语义审查与诚实处理同split变体/跨split风险，随后才能谈一致版本发布；独立校准和其余训练门禁仍未完成。

监听保持记录模式，不自动审查或放行。已通过AI Bridge向Claude交接拒绝依据与修复结果；是否有回信以最终收件箱记录为准。

## 收尾状态

新增六项代码与证据路径已纳入观察器并通过新心跳确认。98个上轮固定命名产物保持原字节；本轮六个修改文件diff检查及导航链接检查通过。源码改动未提交；收尾HEAD及当前文件哈希见 `final-verification.json`，不能用提交号替代工作区哈希。
