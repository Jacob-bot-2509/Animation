# 草稿哈希与写入约定 v1

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
