# A1 剩余修复复验：6aa4589

范围：检查来源空值与样本 ID 边界；未改实现。基线：6aa4589c8c9d82fa19a2403846f9c318a0c57a05。

## 通过项
- 全套测试 96 passed, 22 subtests passed in 2.39s。
- 独立构造 train/eval/test 三集合的 27 条坏 JSONL 路径全部被结构化拦截：source=null、缺失/空白/null/list/dict/float/bool ID，以及 null 样本行。
- 12 条合法路径全部通过：字符串 ID、整数 ID、ID=0、sample_id。
- 样本实际大小与 SHA256 均匹配，未通过其他错误造成假阳性；探测期间源码哈希未变化。
- A2 的 top20 漏检此前已验证关闭，本提交没有相关变化。

结论：A1 此前列出的 JSONL 反例已修复并验证通过，可以继续基于该路径推进主线。

## 尚未覆盖的格式边界
.json 作为 train/eval/test 样本时，{}、null、{"id":["x"]} 均仍返回 ok=true，因为非对象/非法 ID 检查仅对 .jsonl 生效。
这不是要求提前扩展通用格式：当前可继续使用已验证的 JSONL 路径；正式使用 .json 样本前，必须沿用同一校验或明确拒绝该样本格式。此限制针对样本文件，不影响 manifest/config 本身使用 JSON。
A1 不能无条件标为所有格式已关闭；B/C 排期不变，不阻止无关开发。

证据：results.json（完整返回值、HEAD、源码 SHA256）。已通过 AI Bridge 发 Claude Code，要求处理这一范围边界或限制入口；未训练/下载/安装。

本轮同时修复 REVIEW_BACKLOG 表格状态标签的乱码，只更新审查文档，不修改源码。
