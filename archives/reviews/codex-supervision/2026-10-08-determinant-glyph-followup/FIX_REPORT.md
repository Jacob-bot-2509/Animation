# 本轮修复与复验

本批8题的答案与完整证明已核对。发现并修复2条记录的公式记号和场景说明错误，修复后在本轮范围内合格。已逐一查看32张原页和5张重渲页，当前32页通过；累计296/633页完成实际审阅，337页仍待审。

## 实际修复

1. **eval-linalg-004-s3**：原拆列贡献的数学环境在行列式中途结束，后接的替换列文字与另一段公式不能组成完整表达式。solution与scene_spec.steps中的完整证明同步改为
   \[
   ab^2\det(e_1,\ldots,e_{j-1},\mathbf1,e_{j+1},\ldots,e_3)=ab^2,
   \quad j\in\{1,2,3\},\quad \mathbf1=(1,1,1)^T.
   \]
   其余列保持对应标准基向量。题干和正确答案 \(b^2(3a+b)\) 保持。新缓存真实重渲5页，27个去重公式、64个源码公式出现位置；独立解码15帧视频，5个页面起始帧的RGB像素与PNG完全一致。

2. **eval-linalg-002-s3**：四阶按第一列展开正确；接下来的三阶余子式在显示等式中按第一行展开。efficiency_tags、scene_spec.objects与steps的三处“三阶余子式按第一列”改成“按第一行”。保留题干、完整计算和答案 \(6\)。公式清单、全部出现位置、页面几何与4张原PNG不变，按修复后的记录版本重新绑定。

另修复活动README最新说明中的中文编码损坏。旧说明原字节存于visual-readme-before.md；分隔线后的历史说明保留，冻结历史材料不修改。一次候选脚本的Unicode传输失败发生在任何候选修改之前，已改用ASCII转义传输；失败快照和真实原因见encoding-failure.json。

## 数学核验

本批全部完整证明见 [complete-proof-review.json](complete-proof-review.json)，当前完整记录及精确版本见 [bound-current-math-records.json](bound-current-math-records.json)。36项独立符号校验使用整数、有理数、根式与符号恒等式，见 [exact-symbolic-checks.json](exact-symbolic-checks.json)。

- eval-geom-012-s3：\(a,b>0\)，螺线 \(\kappa=a/(a^2+b^2)\)、\(\tau=b/(a^2+b^2)\)，\(\kappa:\tau=a:b\)；Frenet向量的方向、叉积和负号一致。
- eval-geom-016-s3：三条相关向量模平方为 \(19,13,7\)，对角线点积 \(-5\)，余弦 \(-5/\sqrt{133}\)。
- eval-geom-017-s2：正交投影 \((-8/9,4/9,8/9)\)，长度 \(4/3\)，夹角余弦 \(4/9\)，残差与被投影方向正交。
- eval-geom-019-s3：交线 \((t-4,5-2t,t)\)，两个平面回代分别为 \(1,6\)，法向量秩为2，参数式覆盖完整交线。
- eval-linalg-002-s3：第四行保留；三阶余子式 \(-6\)，四阶展开符号为 \((-1)^5\)，所以 \(D=6\)。
- eval-linalg-004-s1/s2/s3：三种完整证明都给出 \(b^{n-1}(na+b)\)。行列变换和拆列证明均不除以 \(b\)，覆盖 \(b=0\)；\(n=1\) 单独为 \(a+b\)。谱分解证明在 \(a=0\) 两因子重合时仍成立。有限阶符号计算是补充检验，一般 \(n\) 阶结论由归档的完整证明支撑。

## 当前交付与证据

完整300条eval候选是 [dataset_eval-final-candidate.jsonl](dataset_eval-final-candidate.jsonl)，保留上批3条修复，本轮仅再改上述2条；不增加题目、不删除题目、不更改答案。

当前唯一选择记录版本的文件是 [current-record-bindings.jsonl](current-record-bindings.jsonl)：总计761条，24个物理来源（23个保留来源和1份完整300条eval候选）。初始渲染阶段的candidate/effective绑定与PENDING标记保留为过程证据，当前资格由本报告、final-independent-verification.json和QUALIFICATION.json给出，不把过程文件中的阶段状态当作最终结论。

[CURRENT_DELIVERY_INDEX.jsonl](CURRENT_DELIVERY_INDEX.jsonl) 覆盖165条记录、633页，SHA256：
667278f661c3a0ca3f72b415a914d2cfc73845dad8f3987d31a38e82b32af715

完整候选SHA256：
9326f3a044ed6b5a7fe2e370e2240fe2f45eb74b86bfee31801fe62dcf3c804e

所有761条记录/数学内容摘要和761条核心签名的版本绑定均核对；签名描述语义未改，只重绑本轮2条。165条公式清单均与当前源码出现位置核对，633张PNG尺寸与SHA、视频SHA、几何SHA重新核对。新视频独立验像素5页；其余628页像素证据按同一公式、几何和PNG继承，不宣称重新解码全部旧视频。父归档109项的原SHA和字节数再次全部通过，渲染器和验证器源码未改。

实际检查范围是原ordinal240–271，32页、8题。初始31页选择漏了最后一题的第5页，现已补齐并实际查看；初始选择保留为历史。原第268页为FAIL_FORMULA_NOTATION，其记录的5页全被新渲染版本替代。当前合格32页包含27张公式/像素不变的原页和5张新页，不把旧失败页计入合格。

逐页证据见 [current-batch-page-glyph-verdicts.jsonl](current-batch-page-glyph-verdicts.jsonl)；累计264页继承同版本证据，加本批32页为296页。待审337页见 [current-unreviewed-pages.json](current-unreviewed-pages.json)。当前队列见 [effective-page-review-queue.json](effective-page-review-queue.json)。

重新计算当前552张完整公式页的占用包围框/展示公式数代理：最小 \(92\)，第10百分位（最近秩）\(484/3\)，中位数 \(219\)；换算1080高的最小代理 \(46\)。81张分片页排除于该统计。此值不能认证最小字形高度；结论见 [current-slot-proxy-summary.json](current-slot-proxy-summary.json)。

## 合格边界与交接

**REPAIRED_PASS_LOCAL_TWO_RECORDS_EIGHT_PROOFS_AND_32_PAGES**。全部字形审阅尚未完成，最小字形高度未认证；概念动画、全局语义隔离、原生沙箱不因本轮局部证明或页面证据放行。生产门禁保持CLOSED，未执行双端实验、重新安装定时器、历史语料扩展、Git提交、发布或开训。

本轮来自用户“继续修”，不重复处理已确认的run-31邮件，也不生成该旧运行的新ACK。归档后的实际Claude回信见bridge-final-reply.json。Claude须依据当前索引和完整候选继续后续工作，保留Codex已完成修复，剩余337页仍需逐页审阅；发现新错误继续修复并提交明确的记录/页面版本证据。
