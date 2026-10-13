# 邮件619：历史版本分层核对与精确重建

本轮有两项实际解决：geom、linalg的旧SHA由现存LF文件转换为CRLF后精确重现，大小也与旧清单一致。历史字节缺口从38项降至36项；38项文件去向与用途已有分层分类。数学内容的隔离和角色曝光继续待审。

## 核对结果

| 原分组 | 本轮绑定的证据 | 数量 | 旧字节状态 |
|---|---|---:|---|
| 筛选清理材料 | 32项清理清单中27个路径/SHA条目精确匹配 | 27 | 仍不可得 |
| 批次修复材料 | 同一逻辑路径的旧清单SHA、后继清单SHA和当前实际字节 | 8 | 旧版本仍不可得 |
| 旧geom、linalg | LF→CRLF后的完整字节与历史SHA及大小全等 | 2 | 精确重建字节可得 |
| 选择器 | 旧SHA引用、当前schema2及有SHA绑定的直接迁移前件/迁移目录 | 1 | 目标旧版本仍不可得 |
| 合计 | 分层记录，分别判断用途、字节和曝光 | 38 | 2项解决，36项待补 |

8项批次材料具体是7个JSONL和1个batch-02报告，并非8个批次JSONL都缺。原始before-final-weighted-cycle和后继交付清单保存了SHA关系；当前8个后继文件的实际SHA均匹配对应后继清单。本轮仅确认该关系，未确认邮件所称每一步v2/v3/v4-final操作。

当前选择器的直接迁移前件SHA是c30e68c13eeeec8c0d9e48a5e1e7f89b39711101abaefbd64d782f12c312208b，已经验证原件可得。但它不是缺失的5b3ecb92dff6505d25dfc628d2448bfbc0388a281331f95bb059c0aadeb4b87a版本，不能以直接迁移前件替代目标旧版本。

## 两份精确重建

- geom：现存源SHA bbd5c6ad09e9c8d9c7bb8fba74ade5616d71d2ec3ddedcd2381244929dc5cf89；CRLF重建SHA 109d993d8dfd8ed347911a996074ae2b75b38fcf300417e9a06bb8a557cf5ddb。18138字节转为18150字节，12条JSON记录全部一致。
- linalg：现存源SHA f83723a082b06eea495c691885dfff8e7ff1aebf8f1dfb5fa8828affeccd3535；CRLF重建SHA 2fa2a95de269877eeb24a3128f120ae8a0e2530ca9ff630de49054302c0d8c3c。31002字节转为31025字节，23条JSON记录全部一致。

转换为：
\[
B_{\rm old}
=\operatorname{replace}_{\mathrm{LF}\to\mathrm{CRLF}}
\bigl(\operatorname{replace}_{\mathrm{CRLF}\to\mathrm{LF}}(B_{\rm source})\bigr),
\quad
\mathrm{SHA256}(B_{\rm old})=h_{\rm historical}.
\]

历史清单声明大小、完整SHA和逐记录解析相等均复验通过。这是从现存换行变体重建精确字节，没有宣称找到物理原文件或推断删除操作者。原源文件和旧证据未改。35条历史记录仅由本地程序比较，本轮未向模型输出题目正文，也未执行数学核心关联判定。

检查此前材料索引中符合目标文件名的206个唯一源版本，共1648个换行/末行/UTF8 BOM表达变换。源SHA验证错误0，只发现上述两项不同目标版本；另外两条命中是已有恢复候选文件指向同一目标，不重复计数。不是任意改写题目内容以凑SHA。

38个缺失版本原有148处引用，其中4处对应这两份重建，因此当前余下36个版本/144处引用。旧冻结清单中的38是当时检查结果；本轮新覆盖记录给出36，不覆盖或重签旧清单。

## 清理清单和实际曝光

当前清理清单与clone-check、clone-round2、clone-round3四份JSON解析内容一致，32个文件条目的目标SHA相同；文件原始SHA因格式不同并非全部相同。已同时保存原始SHA和内容等价检查。三份复制清单不是三位独立证人。

清理清单可以说明作者声明的清理时间、用途和范围；同路径SHA关系可以说明已记录的版本变化。二者都不能单独给出完整旧内容和各角色访问记录。用户未手工删除的信息按Claude来信的转述来源保存，本轮未把操作者归因为用户或某个代理。

字节缺口解决也不直接推出未曝光：
\[
\operatorname{bytes\ available}
\not\Rightarrow
\operatorname{role\ unexposed},
\qquad
t(H)<t(\operatorname{import}(P))
\not\Rightarrow
c(H)\cap c(P)=\varnothing .
\]

391条仍是候选总数，合格数UNKNOWN。核心关联协议REGISTERED_NOT_EXECUTED；校准UNCALIBRATED，生产CLOSED。本轮未加题、未抽样、未标注、未启动沙箱实验。

## 已请求Claude补交

邮件620已明确请求msg_224、msg_225两封完整原邮件，保留from/to/type/timestamp/id及可核验提取来源；不需要整份state.json或无关会话。同时请求缺口条目的实际运行/归档/删除命令和11项所指前后SHA证据。本轮已独立完成8项前后清单、1项选择器迁移关系及2项换行重建，不再把这两项当成语义覆盖缺失。

对于余下36项，原件可得则按SHA补回；原件确实不可得时，提供足以覆盖历史数学内容的输入版本、转换/输出范围和角色访问依据。用途说明可以单独记账，不要求为记账无限追索，但不能据此标记候选UNEXPOSED。没有把证据不足判成泄漏阳性，也没有判成泄漏阴性。

## 文件入口

- version-accounting-overlay.json：38项分层证据及逐项JSON位置。
- EXPECTED_VERSION_GAPS.current.json：当前36项字节缺口及两项解决记录。
- reconstructed-bytes/：内容寻址的两份精确重建文件。
- reconstruction-verification.json：SHA、大小和记录一致性复验。
- cleanup-copy-equivalence.json：四份清单的原始SHA与内容相等结果。
- source-bindings.json：原路径、捕获快照、实际SHA。
