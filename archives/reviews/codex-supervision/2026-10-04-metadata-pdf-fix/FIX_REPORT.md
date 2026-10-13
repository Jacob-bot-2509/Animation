# 新题元数据与 B5 PDF 越界修复

两项问题已修复并写入正式原路径：新题动画元数据不再沿用旧题，B5 第 5 页二次型公式不再越过列边界。141 项相关回归全部通过，正式数据检查为 0 问题、0 quarantine，双冻结锁有效且绑定当前 manifest。

## 具体修改

### 新题元数据

修改 tools/meta_eval_test.py 的五题源映射，再用现有 make_eval_test 和 dataset_intake 生成候选，核验后原子更新 data/v2/raw/dataset_eval.json 与 data/v2/eval/dataset_eval.jsonl。

|题号|新的语义|
|---|---|
|014|三阶含参对称矩阵正交对角化；特征方向、正交主轴和参数曲面|
|019|三元含参二次型标准形与正定性；配方、合同和三维参数曲面分类|
|021|含参三元二次型正定范围；参数正区间及椭球/椭圆柱/单叶双曲面|
|031|最小多项式与迹约束的若尔当分块；四阶块拼图、主分解和二阶幂零链|
|032|三阶含参 λ-矩阵不变/初等因子；Smith 等价变换、因子合并及若尔当块结构|

正式 eval 的 15 条记录仅 function_family 与 visual_style 两字段改变。300 条记录的题目、答案、解法、method、scene_spec 等其余字段完全不变，其余 285 条记录完全不变。raw 与 JSONL 对象相等；测试集 JSONL/raw 原字节不变。源映射已同步，后续正常生成不会把旧反射/J3(2)元数据写回。

manifest 的 eval 哈希与大小已同步。旧 eval-v2/test-v2 锁原字节保存于 archived-locks/ 和 before/，新锁绑定当前 manifest，并记录 supersedes_sha256 与修订原因。test 数据未改，test-v2 锁仅同步新的 manifest 绑定与修订来源。

### B5 PDF 表格公式

保留 tools/render_b5_report.py 中已有的表格分类和裁决表样式改动；新增表格内 MathJax 容器的 inline-block/最大宽度规则，并对实际内部 SVG 设置最大宽度及自动高度。原先只限制外层容器，长 SVG 不缩放；现在完整公式在列宽内按比例适配，不删公式末项。

使用本地 MathJax 和隐藏 Edge 重渲，经候选复验后更新原路径：

- data/b5-calibration-report/pdf/b5-calibration-report.html
- data/b5-calibration-report/pdf/b5-calibration-report.pdf

原 PDF 字节保存在 before/。新 PDF 共 7 页，148 条公式逐条与 Markdown 源等价，148 个 MathJax 渲染节点，0 实际公式错误；按 A4 内容宽度检查表格内 158 个 SVG 边界，0 越界，已查看全部 7 页。第 5 页新二次型公式的末项完整保留并落在右单元格内。最终原路径 PDF 与已查看候选逐字节一致。

B5 annotation JSON、校准 JSON 和 Markdown 均保持修复前原字节，用户标签、8 项既有裁决、2 个不确定项及全部统计和分数未改。

## 验证

- 141 项相关 unittest 通过，覆盖数据校验、字段、入场、冻结、锁版本筛选、近重复、B5、预检、PDF检查与评测生成器。
- 正式 dataset_intake check 为 clean；data_check 为 0 问题、0 quarantine。
- eval-v2 与 test-v2 freeze --check --manifest 均通过，哈希绑定正确。
- 测试前后源码及产物哈希稳定；git diff --check 通过。11 个核心基线文件无漂移。
- 修复前原字节、生成候选、逐记录字段差异、最终输入及 PDF 检查材料完整保存；没有覆盖此前监督回合的历史 JSON/日志/快照。

## 当前范围与交接

用户明确要求 Codex 接手两项修复，已通过 msg_410 告知 Claude 文件责任范围。本文对应的两个问题均已闭环，后续结果已发 Bridge 供 Claude 继续。未替他人提交工作区的其他历史修改。

项目整体训练就绪仍有原先三项未完成：实际组合屏保持 UNCALIBRATED（原标注上的召回率仍 16/17），资产验收证据缺失，network 执行隔离未验收。本轮修复未修改这些规则或门禁，也未启动训练或生成代码。

## 证据

before-manifest.json / before/：修复前字节与哈希；metadata-updates.json / record-diff.json：五题映射与 15 行仅两个字段变化；generated/：确定性生成候选；archived-locks/：旧锁原字节；after-manifest.json / after/：最终状态；verification-results.json：141 测试、CLI与基线结果；pdf-qa/verification.json / final-width-check.json：数学等价、全部页面与实际边界；related-regression.stderr.txt：实跑回归日志。
