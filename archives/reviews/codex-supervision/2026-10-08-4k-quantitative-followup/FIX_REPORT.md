# 4K量化邮件的独立复核与说明修复

时间：2026-10-08。邮件批次：run-809f6577b44e4dbe8dc52d566d43e6a4。
对象：msg_1791420026567_732；规范邮件哈希：`853fc964860c938bbc2d9cf9cab733b2a2ca89401970c15da4ef7340e94026df`。

**本轮说明及量化候选修复合格；全量字形资格仍为NEEDS_EVIDENCE。** Codex已修改作者侧README，另出当前版本绑定的精确量化候选；新增24页实际图像审阅均PASS。当前144/633页有同版本具名实际目视证据，剩余489页不得自动标绿。

## 版本与实际问题

邮件引用的 `reviews/2026-10-08-visual-acceptance/readable-pages-verification-4k.json` SHA256为
`b86454cf8d8c632c502bd32068afdf929ee18d0a0a10386582b7741d1f630f11`。
其165条、626页属于旧4K索引：
`6515262a59d7fec20095aacb30a2e0c9dce4cdb26854deaf0690704988d3bfaf`。

当前165条、633页索引位于 `../2026-10-08-glyph-review-followup/DELIVERY_INDEX.jsonl`，
SHA256为 `07b4543d38599e1c30d2b515e0c2a8761e5611f771c46c75ee23b357c58b6331`。
当前父清单SHA256为 `57a94b01c8c26ac7e898901a4b6f9bd5006b972b84266b9212272c388a139491`；
旧4K父清单SHA256为 `12d50e59e50ee53c219be17d080c83a615523c7305ae5c659bec3b7fbacf902b`。
本轮独立校验两份冻结清单所绑定的每项文件的实际SHA和字节，原件均未修改。

9条记录上轮已修复分数数组行间碰撞，造成页数变化；题号、数学过程、答案与题量未变。旧 draft-c33-03 第3页公式12有实际分数矩阵碰撞，新候选第5页通过；不能拿旧626页量化结论覆盖当前版本。
完整前后关系见 `old-current-version-delta.json` 和上轮冻结报告。

作者JSON没有逐页路径和SHA字段，也未交可复现槽位算法；因此不能仅凭其中自述认定SHA绑定和字号成立。本轮自行通过具名索引找到真实PNG并校验，并不把自己的补验改写成作者已经提交的证据。

## 独立量化结果与精确数学定义

本轮 `audit_quantitative.py` 实际执行完成：
逐页重算旧626页和当前633页的公式区域占用指标，并与具名冻结索引指标逐项相等；按图像SHA与项目数缓存，共计算655个不同键。结果为 `independent-quantitative-review.json`。

采用冻结的 `../2026-10-08-hd-formula-mail-review/audit_hd.py` 中 `page_density`：
3840×2160图像的零基行区间[271,1889)、列区间[136,3704)，任一RGB通道大于32为墨迹。若占用包围盒含端点高度为h、显示项目数为n，则槽位代理
\[
s=\frac{h}{n},\qquad s_{1080}=\frac{h}{2n}.
\]
排序为 \(s_{(1)}\le\cdots\le s_{(N)}\)，第十分位数使用最近秩 \(s_{(\lceil N/10\rceil)}\)，偶数页数的中位数取中间两项算术平均。所有有理数使用精确分数。

| 版本 | 记录/页数 | 显示项目总数 | 最小s | 第十分位数 | 中位数 | 最小s1080 |
|---|---|---|---|---|---|---|
| 旧4K | 165/626 | 2703 | 92 | 160 | 224 | 46 |
| 当前修复4K | 165/633 | 2704 | 92 | 160 | 677/3 | 46 |

作者报告最小238、第十分位数2517/10、中位数1578/5；其626页槽位值全部与上述具名公式区域指标不相等。因为未得到作者算法，只能确认**指标不等价且不可复现作者定义**，不能断言作者具体怎样计算。作者原JSON完整保留。
新的 `current-quantitative-corrected.json` 对633页逐页给出真实路径、SHA、精确指标及当前索引哈希。

**占用包围盒槽位不是最小字形高度。** 它可能包含空白，不能证明上标、下标、分数内部和矩阵内部合格；已确认的旧矩阵碰撞就是反例。4K分辨率、源布局和页面绑定通过的资格继承具名同版本证据，全量字形不得由外框数字推导。

## 本轮实际修改及复验

修改 `reviews/2026-10-08-visual-acceptance/README.md`：
更新当前633页入口，列出精确指标、实际审阅进度、未完成页清单和资格限制；早期首帧包改为历史说明，原内容保留。
修改前后完整副本为 `author-README-before.md`、`author-README-after.md`；差异为 `README-repair.patch`。
修改后实际SHA256为 `120ac8ee5200b42fe92f70a5f84389b623b72d7622cab8ffb18a9913403581ed`，检查见 `README-repair-verification.json`。修改前已发接手回信msg_1791421731990_735，避免同时改同一文件。

当前120页旧证据逐页匹配图像、记录、数学哈希及可见TeX/分片字段：75页来自上轮 `page-glyph-verdicts.jsonl`，45页来自 `repair-page-glyph-verdicts.jsonl`，见 `inherited-glyph-binding-verification.json`。新队列明确引用实际对应账本。
生成器及相关5个文件实际SHA与上轮相同，继承上轮11项具名回归结果，本轮未重复跑无变化测试，见 `unchanged-active-version-verification.json`。

本轮实际新增观察：

- draft-c35-03：第1至6页。
- draft-c36-03：第1至5页。
- draft-c37-05：第1至3页。
- draft-c38-02：第1至3页。
- draft-c41-05：第1至6页。
- eval-calc-003-s1：第1页。

24页均实际查看并逐项对照绑定TeX，符号、指数、上下标、求和与极限边界、矩阵行列和分数在所见图像中清楚，无新增问题。具名逐页理由、SHA、记录/数学哈希和所检公式索引保存在 `page-glyph-verdicts.jsonl`。
显示预览为2048×1152，原PNG为3840×2160；不将预览检查冒称原生最小字形测量证书。

当前覆盖144/633，剩489页列于 `unreviewed-pages.json`；全633页绑定队列为 `current-page-review-queue.json`。未观察页仍为NEEDS_EVIDENCE_NOT_INSPECTED。

## 裁决、后续证据与归档

msg_1791420026567_732：**NEEDS_EVIDENCE**。
本轮当前索引绑定、精确量化候选、README修正与新增24页观察合格；全量视觉资格尚缺其余489页的真实逐页观察。后续提交必须绑定当前索引SHA、具体页PNG SHA、实际所检符号/分片及理由；若宣称最小字形尺寸达标，需给字形自身可复现测量定义与证据，槽位代理不能替代。

只读观察器记录HEAD e2ecd94a925c674bf95d14aec5b164451138b03d、Claude进程29536和观察器37212；进程存在不证明正在执行或验收合格，原始小范围观察见 `observer.json`。

请Claude Code按修复版本继续后续工作，不重复修改Codex已完成部分。保持当前633页交付入口，提交新证据时只处理明确未闭合项，不再将旧626页报告当作当前验收证书。
归档清单在实际交接回执落盘后冻结；冻结后不追加。
本轮production=CLOSED、全局隔离NOT_ESTABLISHED、原生沙箱UNVERIFIED、概念动画NOT_EVALUATED，未签PASS_CORE_SCOPE；双端实验不在范围。未重装调度器，未提交、推送或发布项目。
