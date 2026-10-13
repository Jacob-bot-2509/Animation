# Claude 最新修改独立审查及草稿哈希修复

检查时间：2026-10-05T22:49:45.946680+08:00。最新 Claude 提交为 `1e9f60b`（22:27:01），修改 PDF 两段式渲染及探针。此前 `e990576`（22:07:54）修复账本路径基准不一致导致哈希核对跳过的问题，已用实际提交源码独立复验。

**结论：哈希底层修复已通过；最新 PDF 修改尚不能验收。** 基础草稿审计 hard=0 不等于全部公式已正确渲染。生产隔离告警仍有汇总1项、结构候选2对，新增正式准入0题。

## 最新提交发现的问题

| 等级 | 位置 | 独立发现与修正要求 |
|---|---|---|
| P1 | `tools/render_review.py:177` | 原始脚本已有 `document.title='MJDONE'`，字符串包含判据会把未排版文档判为完成。须核对真实 title、全部 inline/display 公式和实际 SVG 错误节点。 |
| P1 | `tools/render_review.py:188` | 目标旧 PDF 存在时，即使打印失败、没有新输出也返回成功。独立夹具以打印 rc=1、未改变旧无效哨兵文件复现工具 rc=0。须唯一新输出并验证有效 PDF，保全旧版本。 |
| P1 | 7题矩阵/行列式源文及 PDF | 缺少双反斜杠行分隔，未知命令作为红色 SVG `mtext` 输出；容器统计和仅检查 `merror` 都漏报。共14个红色节点、12个公式。须同步修正 JSONL、过程、答案、场景与 MD，并重绑新版证据。 |
| P2 | `tools/build_review_pdf.py:16` | 封面写1172/1172，当前实际1176条；近重复写四舍五入值。应绑定选中版本、核对总数与文档摘要，并直接采用精确分数。 |

受影响题号：draft-c24-03, draft-c31-04, draft-c33-02, draft-c33-04, draft-c33-05, draft-c38-03, draft-c39-01。已生成[7题可执行字段补丁](ready-row-separator-patches.json)，共12个字段，绑定规范化文件摘要、原始字节摘要和完整记录摘要，核对修复后矩阵为预期行列数；没有原地修改 v4-final。Claude 被要求通过统一写入器发布新版本，恢复一致的数学证据，再生成新的 PDF。

[守卫独立复现](pdf-guard-independent-reproduction.json)；[红色未知命令逐式证据](pdf-undefined-command-findings.json)；[当前提交源码快照与完整审查](latest-claude-review.json)。中间 `merror` 字符串计数曾计入CSS选择器，后续节点解析已纠正；此处以实际红色 SVG 节点和视觉检查为准。

## 实际 PDF 与正文核对

现有审阅 PDF 有效，共103页，SHA-256为 `0409dee38f732e3a7c200a9feedf1c3f7d1089f2638880f6d521321897b8e3a2`。实际静态 DOM title=MJDONE，8316个数学容器已产生，全部264题及18份修订正文存在。已渲染103页缩略图并放大1、12、13、14、57、58、103页；第12页等可见红色未知命令，封面仍为旧计数。未修改、重导出或覆盖现有 PDF，不能将容器齐全或缩略图检查称为零格式缺陷证明。

精确相似度：训练池最大33/79，冻结评测测试最大18/43，草稿内最大24/53。仅为候选筛查值，不证明结构隔离。

## 已执行的底层修复

- 统一 `draft_io` 规范化哈希与原始字节摘要；账本 schema 2，`draft_audit`、`coverage_ledger` 和新版交付视图同步使用明确算法。
- 精确定义和旧版兼容规则见 [HASH_CONTRACT.md](HASH_CONTRACT.md)；UTF-8严格解码，去起始BOM、splitlines后LF连接，不估算或改写数学值。
- 新增统一 UTF-8/LF/无BOM写入器及CLI，已存在版本拒绝覆盖；六个旧原地修复/重签脚本在新账本下拒绝运行。
- 草稿 Git 属性为 `-text !eol`；历史数据、旧清单、数学证据和原始日志保持字节不变，通过203项新增摘要目录和三份 normalized交付视图衔接。
- 审计的可精确表示比值改用分数，报告使用实际审查 glob。

活动账本原始字节 SHA-256：`5dc06da3f7aba4fd32e474dfded2ad1b22fa3e2105d9cad6ef726913b5aac535`。只修改活动草稿账本的哈希口径和相关工具，没有修改生产 manifest、冻结训练/评测/测试、旧草稿、旧数学证据或旧交付清单。

## 独立验证

18项回归通过；18批264题真实账本 V007=0、V011=0、hard=0；独立伪造一批摘要时 V007=1、hard=1，核对没有跳过。CLI实际写入保留精确分数，第二次同名发布拒绝。隔离Git真实提交和clone使18份最终草稿原字节一致；18份历史v1现存Git blob与工作区的规范化摘要一致。12219份既有历史及生产文件逐项保持原字节。

仍有528项草稿 quarantine：264项内部研究许可证、264项动画未验证。生产清单当前 `ok=false`，结构告警含 `linalg-048 ↔ eval-linalg-015-s1` 与 `linalg-048 ↔ test-linalg-025`；已有训练改写候选未激活，未自动准入。

[本轮最终验证](final-verification.json)；[18项测试](unit-tests-18.txt)；[实际完整审计](acceptance-real/summary.json)；[Git克隆验证](git-roundtrip-validation.json)；[新版覆盖账本](coverage-ledger-normalized.json)；[生产清单复验](production-validation.json)；[交付清单](delivery-manifest.json)。

只读观察器PID12024继续记录。进程存在和监听记录不证明Claude正在计算；本报告仅覆盖记录的提交和当前文件版本。独立哈希修复为Codex工作区修改，尚未由Codex提交项目仓库；Claude新PDF提交需按上述发现继续修复并返还版本化成果。
