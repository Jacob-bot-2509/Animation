from pathlib import Path
import json,hashlib,datetime
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,text):
 p=OUT/name;assert not p.exists();p.write_bytes(text.encode('utf-8'));return p
review=json.loads((OUT/'latest-claude-review.json').read_text('utf-8'));verification=json.loads((OUT/'final-verification.json').read_text('utf-8'));selector=ROOT/'reviews/2026-10-05-training-diversity-drafts/draft-selection.json'
contract=r'''# 草稿哈希与写入约定 v1

仅适用于草稿及其新版交付视图。生产训练/评测/测试 manifest、锁文件、旧证据和记录数学内容摘要的既有算法不迁移。

## 精确定义

`hash_algorithm = sha256-utf8-sig-splitlines-lf-v1`

```python
sha256('\n'.join(data.decode('utf-8-sig').splitlines()).encode('utf-8'))
```

以上示意代码中的 `\n` 是 LF 分隔符；实际实现为 [draft_io.py](../../../tools/draft_io.py) 中的 `normalized_bytes` 和 `fingerprint`。UTF-8 严格解码，忽略一个起始 BOM，使用 Python `str.splitlines()` 识别行界，再以 LF 连接。一个终末行分隔符不计入摘要，内部空行和多余终末空行仍显著；JSON 空白、键顺序、数值与数学记号均不另做归一化。Python splitlines 识别的其他 Unicode 行分隔符也按同一明确算法处理，不能把规范化当作 JSON 语义校验。

- `sha256`：当前规范化内容摘要，草稿选择和核对按此字段进行。
- `raw_sha256`：发布时归档字节摘要，用于追溯原件。当前内容摘要匹配而字节摘要不同，记录等价换行/BOM差异；不能据此增加准入数。
- `source_sha256/source_raw_sha256/source_hash_algorithm` 和 `report_sha256/report_raw_sha256/report_hash_algorithm` 同样显式标明各自口径。
- 无算法声明的旧 schema 1 仍按 `sha256-raw-bytes-v1` 校验，绝不以尝试多个算法的方式放过哈希失配。未知算法、算法冲突、缺失/格式错误摘要、非法路径均拒绝。
- `strict_review.math_content_sha256` 和逐记录排序 JSON 摘要仍用原有独立算法；旧记录和历史证据不被重写。

## 新版本发布

```powershell
.venv/Scripts/python.exe -B tools/publish_draft.py --source NEW_SOURCE.jsonl --output reviews/2026-10-05-training-diversity-drafts/batch-XX/draft-NEW_VERSION.jsonl
```

统一使用 `draft_io.publish_jsonl`：UTF-8、LF、无 BOM、终末 LF，保留输入顺序和数学字符串；重复/缺失 ID 与非有限 JSON 数值拒绝。目标使用独占创建，已存在文件拒绝覆盖。调用者须另行核对 ID/总数/顺序、版本血缘、数学内容证据和 Markdown；写入器不自动选中或准入任何记录。

草稿路径在 `.gitattributes` 中为 `-text !eol`；Git 后续新增时不改字节。已存在 Git 历史 blob 不会被属性追溯改写：18份 v1 历史 blob 是 LF，而工作区原件为 CRLF，新规范化视图验证二者一致。项目仓库尚未由 Codex提交或重写索引，本轮真实 clone 验证发生于隔离夹具仓库。

六个旧原地修复、切回 v2 和裸 SHA 重签工具在 schema 2 下提前拒绝执行。历史交付清单保持原字节，新增三份 normalized manifest 和 [203项历史摘要映射](historical-hash-catalog.json) 供迁移使用。执行旧报告核验时必须按其原算法及归档原件解释，不能直接把旧 raw SHA 改称新内容 SHA。

审计的 `file_hashes.json` 对草稿提供两种摘要与算法；传统 `file_hashes.sha256` 保持原始字节摘要，可用于普通文件校验。

`draft_audit.py` 是报告导出器，出现全局 hard 时返回码仍可能为0；消费者必须读取全局 `severity_counts` 和 `V007/V010`，不能仅凭退出码或逐记录状态放行。
'''
# Write the executable definition literally with a single LF escape in the document.
contract=contract.replace("sha256('\\\\n'.join", "sha256('\\n'.join")
save('HASH_CONTRACT.md',contract)
report=f'''# Claude 最新修改独立审查及草稿哈希修复

检查时间：{review['reviewed_at']}。最新 Claude 提交为 `1e9f60b`（22:27:01），修改 PDF 两段式渲染及探针。此前 `e990576`（22:07:54）修复账本路径基准不一致导致哈希核对跳过的问题，已用实际提交源码独立复验。

**结论：哈希底层修复已通过；最新 PDF 修改尚不能验收。** 基础草稿审计 hard=0 不等于全部公式已正确渲染。生产隔离告警仍有汇总1项、结构候选2对，新增正式准入0题。

## 最新提交发现的问题

| 等级 | 位置 | 独立发现与修正要求 |
|---|---|---|
| P1 | `tools/render_review.py:177` | 原始脚本已有 `document.title='MJDONE'`，字符串包含判据会把未排版文档判为完成。须核对真实 title、全部 inline/display 公式和实际 SVG 错误节点。 |
| P1 | `tools/render_review.py:188` | 目标旧 PDF 存在时，即使打印失败、没有新输出也返回成功。独立夹具以打印 rc=1、未改变旧无效哨兵文件复现工具 rc=0。须唯一新输出并验证有效 PDF，保全旧版本。 |
| P1 | 7题矩阵/行列式源文及 PDF | 缺少双反斜杠行分隔，未知命令作为红色 SVG `mtext` 输出；容器统计和仅检查 `merror` 都漏报。共14个红色节点、12个公式。须同步修正 JSONL、过程、答案、场景与 MD，并重绑新版证据。 |
| P2 | `tools/build_review_pdf.py:16` | 封面写1172/1172，当前实际1176条；近重复写四舍五入值。应绑定选中版本、核对总数与文档摘要，并直接采用精确分数。 |

受影响题号：{', '.join(review['affected_ids'])}。已生成[7题可执行字段补丁](ready-row-separator-patches.json)，共12个字段，绑定规范化文件摘要、原始字节摘要和完整记录摘要，核对修复后矩阵为预期行列数；没有原地修改 v4-final。Claude 被要求通过统一写入器发布新版本，恢复一致的数学证据，再生成新的 PDF。

[守卫独立复现](pdf-guard-independent-reproduction.json)；[红色未知命令逐式证据](pdf-undefined-command-findings.json)；[当前提交源码快照与完整审查](latest-claude-review.json)。中间 `merror` 字符串计数曾计入CSS选择器，后续节点解析已纠正；此处以实际红色 SVG 节点和视觉检查为准。

## 实际 PDF 与正文核对

现有审阅 PDF 有效，共103页，SHA-256为 `{review['pdf_raw_sha256']}`。实际静态 DOM title=MJDONE，8316个数学容器已产生，全部264题及18份修订正文存在。已渲染103页缩略图并放大1、12、13、14、57、58、103页；第12页等可见红色未知命令，封面仍为旧计数。未修改、重导出或覆盖现有 PDF，不能将容器齐全或缩略图检查称为零格式缺陷证明。

精确相似度：训练池最大33/79，冻结评测测试最大18/43，草稿内最大24/53。仅为候选筛查值，不证明结构隔离。

## 已执行的底层修复

- 统一 `draft_io` 规范化哈希与原始字节摘要；账本 schema 2，`draft_audit`、`coverage_ledger` 和新版交付视图同步使用明确算法。
- 精确定义和旧版兼容规则见 [HASH_CONTRACT.md](HASH_CONTRACT.md)；UTF-8严格解码，去起始BOM、splitlines后LF连接，不估算或改写数学值。
- 新增统一 UTF-8/LF/无BOM写入器及CLI，已存在版本拒绝覆盖；六个旧原地修复/重签脚本在新账本下拒绝运行。
- 草稿 Git 属性为 `-text !eol`；历史数据、旧清单、数学证据和原始日志保持字节不变，通过203项新增摘要目录和三份 normalized交付视图衔接。
- 审计的可精确表示比值改用分数，报告使用实际审查 glob。

活动账本原始字节 SHA-256：`{verification['selector_raw_sha256']}`。只修改活动草稿账本的哈希口径和相关工具，没有修改生产 manifest、冻结训练/评测/测试、旧草稿、旧数学证据或旧交付清单。

## 独立验证

18项回归通过；18批264题真实账本 V007=0、V011=0、hard=0；独立伪造一批摘要时 V007=1、hard=1，核对没有跳过。CLI实际写入保留精确分数，第二次同名发布拒绝。隔离Git真实提交和clone使18份最终草稿原字节一致；18份历史v1现存Git blob与工作区的规范化摘要一致。12219份既有历史及生产文件逐项保持原字节。

仍有528项草稿 quarantine：264项内部研究许可证、264项动画未验证。生产清单当前 `ok=false`，结构告警含 `linalg-048 ↔ eval-linalg-015-s1` 与 `linalg-048 ↔ test-linalg-025`；已有训练改写候选未激活，未自动准入。

[本轮最终验证](final-verification.json)；[18项测试](unit-tests-18.txt)；[实际完整审计](acceptance-real/summary.json)；[Git克隆验证](git-roundtrip-validation.json)；[新版覆盖账本](coverage-ledger-normalized.json)；[生产清单复验](production-validation.json)；[交付清单](delivery-manifest.json)。

只读观察器PID12024继续记录。进程存在和监听记录不证明Claude正在计算；本报告仅覆盖记录的提交和当前文件版本。独立哈希修复为Codex工作区修改，尚未由Codex提交项目仓库；Claude新PDF提交需按上述发现继续修复并返还版本化成果。
'''
report_path=save('SUPERVISION_REPORT.md',report)
artifacts=['SUPERVISION_REPORT.md','HASH_CONTRACT.md','final-verification.json','migration-result.json','historical-hash-catalog.json','delivery-batch01-08-normalized.json','delivery-batch09-18-normalized.json','delivery-v4-final-normalized.json','coverage-ledger-normalized.json','git-roundtrip-validation.json','writer-cli-validation.json','latest-claude-review.json','pdf-guard-independent-reproduction.json','pdf-undefined-command-findings.json','ready-row-separator-patches.json','acceptance-real/summary.json','production-validation.json','unit-tests-18.txt']
manifest={'schema':2,'scope':'DRAFT_HASH_COMPATIBILITY_AND_LATEST_CLAUDE_REVIEW','generated_at':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'latest_claude_commit':review['latest_claude_commit'],'hash_algorithm':verification['hash_algorithm'],'draft_entries':json.loads(selector.read_text('utf-8'))['entries'],'selector':{'path':selector.relative_to(ROOT).as_posix(),'raw_sha256':sha(selector)},'artifact_hash_algorithm':'sha256-raw-bytes-v1','artifacts':[{'path':(OUT/n).relative_to(ROOT).as_posix(),'raw_sha256':sha(OUT/n)} for n in artifacts],'code_changes':verification['code_changes'],'hash_fix_verified':True,'latest_pdf_accepted':False,'latest_pdf_affected_ids':review['affected_ids'],'new_draft_admissions':0,'historical_bytes_preserved':True,'project_commit_or_index_modified_by_codex':False}
save('delivery-manifest.json',json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'report_raw_sha256':sha(report_path),'delivery_raw_sha256':sha(OUT/'delivery-manifest.json'),'patch_raw_sha256':sha(OUT/'ready-row-separator-patches.json'),'selector_raw_sha256':sha(selector)},ensure_ascii=False))
