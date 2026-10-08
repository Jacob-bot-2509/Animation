# 修复后复检报告（草稿 v4-final + 全量渲染链 · 2026-10-05 第三轮）

> 本轮修复内容（依提交）：
> - `e990576` 修 `tools/draft_audit.py` 的 **V011 守卫失效**（账本 path 与项目根相对路径基准不一致 → 哈希核对恒被跳过）
> - `1e9f60b` 修**审阅稿 PDF 渲染链**（Edge 改 `as_uri` + 独立临时 profile、两段式打印、放宽 rc 判据），并新增**错误节点**统计
> - 账本 `draft-selection.json` 升级为 **schema 2**：声明 `hash_algorithm=sha256-utf8-sig-splitlines-lf-v1`，每条附 `raw_sha256`；`.gitattributes` 对草稿声明 `-text !eol`（保留原始字节）
> 复现：
> `python tools/draft_audit.py --out <dir> --drafts "reviews/2026-10-05-training-diversity-drafts/batch-*/draft-codex-repair-v4-final.jsonl" --pool data/v2/train/leakage-isolated-v3-2026-10-05 --eval-test data/v2/eval/dataset_eval.jsonl --eval-test data/v2/test/dataset_test.jsonl`
> `python tools/render_review.py <render-pack>.md --out-dir <dir> --check --skip-pdf`

---

## 0. 结论

| 检查 | 结果 |
|---|---|
| 草稿 v4-final（264 题） | **hard 0**、quarantine 528、info 1044；rejected 0 |
| 上一轮的 2 项发现 | **均已修复并复核通过**（V011 守卫、账本哈希口径） |
| 账本 schema 2 独立核对 | **18/18 全项通过**（规范化哈希 / 原始哈希 / 上游来源 / 报告 / 计数 / 路径） |
| 全量公式渲染（新渲染链） | 824 条记录、**16,539 条公式、未排版 0**（`MJDONE=True`） |
| 新「错误节点」指标 | **恒定 2 → 页面基线，不是公式错误**（探针验证，见 §3） |

---

## 1. 上一轮 2 项发现的复核

### 1.1 V011 守卫失效 → 已修复

- 上一轮：18 条 `V011` info 称"被审文件不是账本选中版本…跳过哈希核对"（两条路径其实指向同一文件），导致 `V007`（哈希不符）/`V008`（条数不符）**从未执行**。
- 本轮：`V011` **0 条**；`V007`/`V008` **0 条** → 账本核对**真正执行且通过**。
- 工具修复方式（`e990576`）：把账本 `path`（相对草稿目录）统一折算为**相对项目根**的 posix 路径再比较。

### 1.2 账本哈希与行尾（复现性）→ 已修复

- 上一轮：账本 sha256 绑定 **CRLF 字节**，而 `.gitattributes` 声明 `*.jsonl eol=lf` → clone 后账本哈希失效。
- 本轮：
  - 账本升级 **schema 2**，顶层与每条均声明 `hash_algorithm = sha256-utf8-sig-splitlines-lf-v1`，即 **UTF-8(BOM 去除) → `splitlines()` → LF 连接**（无末换行）的规范化哈希；原始字节哈希另存 `raw_sha256` 供归档；
  - `.gitattributes` 对 `reviews/.../batch-*/draft*.jsonl` 与 `staged/*.jsonl` 声明 **`-text !eol`**（提交/检出都不做换行转换 → 字节稳定）；
  - 另有 `migration` 段指向历史哈希目录证据（`2026-10-05-draft-hash-compatibility/historical-hash-catalog.json`）。
- **Lead 独立核对（不依赖其工具）**：我用 `sha256("\n".join(raw.decode("utf-8-sig").splitlines()).encode())` 重算，**18/18 与账本 `sha256` 完全一致**；同时逐条核对：

| 核对项 | 通过 |
|---|---|
| 规范化哈希（草稿） | **18/18** |
| 原始字节哈希 `raw_sha256` | **18/18** |
| 上游来源 `source_sha256`（v3） | **18/18** |
| 报告 `report_sha256`（`DRAFT_REPORT-…md`） | **18/18** |
| 条数 `count` | **18/18** |
| 路径存在（`root_path`/`source_path`/`root_report_path`） | **18/18** |

- 明细口径示例（batch-01）：账本 `df5893421e6a…` = LF+去末换行的规范化哈希；`raw_sha256 = e52c6ac7de59…` = 当前 CRLF 字节。二者**同时登记**，因此既保证 clone 后可复现，也保留归档字节可追溯。

> 说明：草稿文件本身**仍是 CRLF**（`.gitattributes` 现明确 `-text !eol` 保留字节），故 `S002`×18（"含 CR"）保留为 info，**属既定策略，不是缺陷**。

---

## 2. 草稿 v4-final 复检结果（264 题）

| 项 | 数值 |
|---|---|
| 状态 | rejected **0** / quarantine 264 / clean 0 |
| 严重度 | **hard 0** / quarantine **528** / info **1044**（共 1572） |
| quarantine 构成 | `P002`×264（license=Internal-Research-Use-Only）、`A008`×264（动画未验证） |
| info 主要项 | `L009`×343（`\frac` 单 token，合法）、`P003`×264、`C007`×257、`L007`×154、`S002`×18（CRLF，既定策略）、`X003`×2、`X005`×1、`C008`×2、`V004`/`V005`/`V009` 各 1 |
| 与上一轮差异 | **仅少 `V011`×18**；其余代码分布完全一致（题目内容未变） |
| 泄漏 | 训练池精确 0 / 最大 0.4177；eval-test 精确 0 / 0.4186；集内精确 0 / 0.4528 |
| 声明 | `admitted=true` 0、`animation_render_verified=true` 0 |
| 身份 | 264 id 唯一、264 versioned_id 唯一、与原始草稿 id+顺序 100% 保留 |

---

## 3. 全量渲染复核（使用**修复后的**渲染链）

| 数据集 | 记录 | 已排版 | 未排版 | 错误节点 | 耗时 |
|---|---:|---:|---:|---:|---:|
| v1 raw | 63 | 884 | **0** | 2 | 1.9s |
| v2 train 池 | 47 | 693 | **0** | 2 | 1.6s |
| v2 eval | 300 | 4540 | **0** | 2 | 6.3s |
| v2 test | 150 | 2106 | **0** | 2 | 3.3s |
| 草稿 v4-final | 264 | 8316 | **0** | 2 | 10s |
| **合计** | **824** | **16,539** | **0** | 2 | ~23s |

所有页面 `MJDONE=True`（MathJax 完成排版）。

### 3.1 新增「错误节点」指标：恒定 2，属页面基线（Lead 探针验证）

新 `check_render` 统计 `data-mjx-error` + `<mjx-merror` + `data-mml-node="merror"` 的出现次数。我用两个最小探针复核其灵敏度：

| 探针 | 内容 | 已排版 | 未排版 | 错误节点 |
|---|---|---:|---:|---:|
| `ok.md` | 2 条正常公式 | 1（同段合并） | 0 | **2** |
| `broken.md` | 含故意写坏的 `$\frac{1}{$` | 2 | **1** | **2** |

结论：
1. **「错误节点」有恒定基线 2**（单公式页面也是 2），来自页面/注入样式中的 MathJax 错误选择器文本，**不能反映真实公式错误**；
2. **「未排版」指标是灵敏的**：故意写坏的公式被准确计为 1 条未排版，而正常公式不计；
3. 因此本轮全量数据的有效结论是 **未排版 0**；建议把错误节点改为"仅统计 `<mjx-container>` 内的 `mjx-merror` 元素"或扣除基线，否则该数字会长期显示 2 而被误读。

---

## 4. 裁定与建议

1. **上一轮两项发现均已闭环**：V011 守卫生效（账本校验真跑且通过）、账本哈希口径改为 EOL 无关的规范化哈希 + 原始字节归档，clone 后可复现。
2. **草稿内容层无新增问题**：hard 0、无泄漏、id 全保留、声明如实；剩余 528 条 quarantine 仍全是**用户级**项（`P002` 许可证转正、`A008` 动画验证）。
3. **公式排版全量通过**：824 条记录 / 16,539 条公式 / 未排版 0（用修复后的渲染链复测）。
4. **建议修一处指标口径**：`check_render` 的"错误节点"含恒定基线 2，宜改为容器内计数或扣除基线（本轮已用探针证明其当前不具判别力）。
5. 另一层"渲染验收"仍待推进：`data/asset_evidence.json` 为 497 条中 **1 条**已验证、状态 **NOT READY**（与公式排版无关）。

---

## 5. 产物

| 路径 | 内容 |
|---|---|
| `dataset_audit_2026-10-05-codex-drafts-v4-final-r2/` | 草稿复检输出（`issues.jsonl`、`summary.json`、`record_status.*`、`file_hashes.*`） |
| `dataset_audit_2026-10-05-render-check-r2/` | 渲染复检（`render-results.json`、`render/`、`probe/` 探针） |
| `_ledger2.py` / `_ledger3.py` / `_ident.py` | 账本规范化口径识别与 18 项独立核对脚本 |
| 本报告 `RECHECK_REPORT.md` / `.pdf` | — |

**声明**：只读检查；未修改草稿、数据、账本或工具；所有写入均在本工作区目录内；未启动训练、未下载模型、未生成动画。
