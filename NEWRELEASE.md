# Animation Model Training v0.6.0

发布日期：2026-10-17  
本地说明修订：2026-10-18  
发布类型：证据通道与训练准备候选阶段（Pre-release）

本周期交付了具名 OneDrive 旧材料回放与本机 watch 部署证据、首批十题精确数学文本候选、呈现管线候选和几何设计。各项资格分别按实际证据判断，准备工作尚未全部完成。production=CLOSED，训练未启动，全局隔离 NOT_ESTABLISHED。

本次只修正工作区中的发布说明；既有 Git 提交、标签和远端 Release 未由本次审查修改。版本依据为具名输入/源码 SHA 和相应冻结报告，不能将不同提交、候选与历史运行合并为同一次验收。[本次说明审查](archives/reviews/codex-supervision/2026-10-18-release-claims-review/FIX_REPORT.md)。

## 已有证据及适用范围

- **OneDrive 回放通道**：已有 WJW 发布配置/回执、包、训练机到达与注册对账的独立核验，结论为 PASS_BOUND_ONEDRIVE_REPLAY_CHANNEL。89 项是具名材料/归档检查，包含旧归档核验，不是 89 次新实验。只证明该轮旧 LAN 材料在声明端点间的一次传输回放，不证明远程身份认证、持续可用性或新沙箱实验通过。[通道报告](archives/reviews/codex-supervision/2026-10-17-publisher-chain-review/SUPERVISION_REPORT.md)。
- **watch 部署**：历史具名部署的 46 项检查支持 PASS_CURRENT_BOUND_CONSUMER_WATCH_LOCAL_DEPLOYMENT，包括等待期间持锁、第二实例拒绝、一次真实 STOP 退出码 0 和同版本幂等。这是当时、本机、具名版本的证据；本说明不据此宣称服务此刻在线，也不重启服务。[部署报告](archives/reviews/codex-supervision/2026-10-17-watch-deployment-followup/SUPERVISION_REPORT.md)。
- **原始材料与作者操作**：保留既有回执及原始字节。传输件清理等作者记录不改写为 Codex 执行或新增用户授权，历史运行身份不因当前源码变化而重签。

## 门禁前静态准备

下列材料按各自范围交付，不合并为“全部准备通过”。现行分工及具名交付要求见[准备证据协议](docs/READINESS-EVIDENCE-PROTOCOL.md)。

| 项目 | 当前可认定范围 | 尚待完成 |
|---|---|---|
| 外部来源与抽样 | 来源登记、固定 revision、六层配额及 7 学科×3 难度整数配额设计；既有可行性核验器 17 项回归 | execution_ready=false，尚未下载/抽样；NuminaMath 上限 2000、首批 300 属邮件报告方案，不由本说明确认为新增用户额度 |
| 来源用途 | TheoremQA 800、UGMathBench 5062 道基础题/15186 个版本实例按方案列为外测，不进训练；manim 类资料仅作风格参考候选 | 逐来源许可、上游权利、用途及转换资格按具名材料核验，不以来源卡片替所有条目背书 |
| 评测接线 | 已有固定夹具与绑定/对抗检查 | 正式 R/E/M/F 全为 UNVERIFIED，诊断仍单列 fixture_diagnostics；设计和夹具不等于真实执行器已接通 |
| 执行隔离 | 已有 BOUND_FILES、采集脚本绑定、新根设计和纯元数据处理器候选（39 项既有测试） | 上一具名 43 点汇总为 30 GREEN / 2 PARTIAL（F2/F4）/ 11 GAP；data/execution_evidence.json 缺失，联合验收 NEEDS_EVIDENCE，不能以纯模拟替代原生证据 |
| 资产呈现 | 原 step[:28]、steps[:5]、公式/答案呈现缺陷已有模板修复候选与首批十题材料 | 497 条资产中仍有 496 条待验；其中 15 条旧源绑定失配，独立隔离候选处理，不直接改签合格 |
| diversity | 47 条当前 train 原始行 SHA 绑定材料与结构化待审清单 | 概念、变体、数学、泄漏及真实用户意见仍待审；47 条的数量不自动满足 53 概念各至少 5 题、至少 3 种形式 |
| B5 | 现有 50 对开发诊断已精确复算 | 组合屏召回率 16/17＜19/20，差 3/340，存在 1 对漏检；现有标签不属于独立最终校准，near_dup_calibrated=False 继续保持 |

B5 组合屏为“签名一致且 Jaccard≥2/5”；漏检对 eval-calc-010 与 test-calc-007 的相似度为 19/62。没有调整真实标签、分母或目标来标通过。[B5 独立报告](archives/reviews/codex-supervision/2026-10-17-b5-readiness-audit/FIX_REPORT.md)。

目视批次当前是提案，不代签真实用户意见。Claude 邮件转述的“全量目视拍板”不在本说明中扩展为用户在当前会话的新承诺；实际 user_review 保持空，收到可追溯反馈后再登记。[批次提案审查](archives/reviews/codex-supervision/2026-10-17-visual-review-batch-plan/FIX_REPORT.md)。

## 首批十题与呈现管线

- **数学文本候选**：十题逐题核对，35 项手写精确表达式检查通过，资格为 REPAIRED_PASS_EXACT_MATH_TEXT_CANDIDATES_ONLY。修订包含生日补事件精确式、LLN/CLT 条件、半开分割、单位圆夹逼、Green 规格、级数界与旋转体推导；原已正确的积分答案保留。不是“十题原答案全部有误”。[数学报告](archives/reviews/codex-supervision/2026-10-17-first-batch-exact-math-review/FIX_REPORT.md)。
- **现用输入**：当前呈现入口指向新冻结的 current-candidate-v2/records.jsonl，SHA256 为 e686ce7e8ac9c8c313d70cffdbecf6c140f044b27ab5f5966321ff61acd45246。相对最初数学候选，仅 prob-042 的一个公式内中文标签改为 heads 并在公式外解释，数学含义未变；其余九条原始记录行一致。旧归档清单之后追加的文件不追认为旧认证。
- **管线候选**：generate、render、review-pack、verify 分阶段记录资格；render 仍依实际 check_certificate 与获准入口，不能靠字段自述或夹具放行。最新修订的 14 项既有管线回归通过，十条实际输入的纯静态生成与十份已有场景逐字节一致；本轮没有运行场景或渲染。不同模板版本的测试数不合计冒充一次测试。
- **历史文字试点**：先前记录为十题文字层短视频，每个 45 帧、无几何图元，network_isolated=false。它仅是历史文字试点，不证明全部过程/答案在全动画中完整可读，也不构成 F、原生隔离或生产验收。
- **几何设计已修订**：十题、十类模板、32 项精确关系与绑定合同已静态核验。黎曼柱高度 h_i=1−ξ_i²−η_i²，体积 v_i=h_iΔA_i；S200±E200 夹住和函数 f；A_N≥2(√(N+1)−1) 是下界，不是恒等式。渲染前期望与渲染后实际媒体/帧证据分开绑定。几何实现、实际媒体、F 和用户意见尚未完成。[几何设计与入口修复报告](archives/reviews/codex-supervision/2026-10-18-geometry-design-review/FIX_REPORT.md)。

## 备份与归档

作者扩展备份目录为 D:/backups/animtrain/2026-10-17-training-data，涉及 data、holdout-sources、configs、archives 和 reviews-data-prep。作者清单含 113594 行，登记大小之和为 7557121960 字节；这是清单元数据统计，不是 Codex 已逐文件核对全集源/副本的结果。

本次只读复核发现两个限制：archives 复制汇总含 1 个失败目录；清单中的 BACKUP-SUMMARY.json 登记为 144 字节，当前文件为 371 字节且 SHA 不同。不能声称所有目录复制成功或清单已完整自洽，原始日志与清单保留。此前 Codex 独立确认的范围仍是十个具名当前输入文件、共 1283186 字节的源/副本一致；备份全集为 UNVERIFIED，原复制退出码不能由事后计数补造。[备份审查](archives/reviews/codex-supervision/2026-10-17-backup-integrity-review/FIX_REPORT.md)。

holdout-sources 对应 391 条候选池，保持原池、不加题；391 不是已获资格的最终测验数量。成员资格、曝光与角色访问控制、独立标签和最终校准分别待实际证据。[保管安排审查](archives/reviews/codex-supervision/2026-10-17-holdout-custody-mail-review/FIX_REPORT.md)。

Codex 产物继续遵循 AGENTS.md，落在 archives/reviews/codex-supervision/；archives/harness 可保留作者分档，archives/codex 的目录说明不代表 Codex 已采用新的落点约定。旧冻结目录与原始字节不回写。

## 后续顺序与边界

1. 先继续数学/几何静态候选、来源许可与抽样准备、B5 独立材料、diversity 实际审核及 holdout 外层元数据/角色控制；这些准备不必等待全部原生点位完成。
2. 后续几何实现交具名源码与纯逻辑检查；真实运行生成代码、渲染及训练须满足适用的执行门禁与动作授权。首批验收完成前不将模板候选直接批量改签为合格。
3. 新增采集与探针由用户授权后 Claude 执行，Codex 不发射。D2/D8 外部 IPv6 按用户决定延期、如实 GAP，不阻塞准备；不据此把 D1/D7 或其他点位改绿。
4. 原生证据、数据/评测资格与实际训练参数按各自合同收口后，再按获准范围进入试训、正式 holdout 执行与训练产物审片。生产门禁仍 CLOSED；本版本没有宣告训练完成或生产就绪。
