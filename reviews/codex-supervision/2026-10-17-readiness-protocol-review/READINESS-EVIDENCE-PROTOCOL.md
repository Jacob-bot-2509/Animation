# 准备证据、联合验收与评测接线协议 v1

状态：DESIGN_CONTRACT_NOT_CONNECTED。本协议回应 Claude 邮件 851/852，明确准备材料和实现分工；没有运行原生探针、外测或训练，也不生成生产证书。来源和实际检查见 [本轮报告](../archives/reviews/codex-supervision/2026-10-17-readiness-protocol-review/SUPERVISION_REPORT.md)。

## 1. 三类“隔离”分别记账

- 训练与评测的内容隔离：761 条记录签名、12 组具名对照和 4 条改写属于具名版本的有限内容证据。应引用真实源路径、记录 SHA、检查器/人工理由及处置结果，不能只列计数。用户已直接确认接受有限证据口径，不要求事前证明全局语义隔离。全局状态仍如实为 NOT_ESTABLISHED。
- 最终 holdout 的访问隔离：是成员和角色的实际曝光、封存与规则锁定记录。未落实项按真实状态记账；不是恢复对全局语义隔离的事前证明要求。
- exec_isolation：是 Windows AppContainer/JobObject、文件/进程/网络边界的原生运行证据。内容签名与盲标不能代替这个操作系统门禁。OneDrive 回放和 consumer watch 证明的是具名材料传输与监视，不是生产隔离验收。

用户此前决定 D2/D8 公网 IPv6 延后、如实 GAP 且不阻塞准备。当前 check_certificate 的实现仍要求 43 点全 GREEN，IPv4 联合认定仍依赖 LAN IPv4 + 外部 IPv6 + 本机 IPv4。有限内容隔离确认没有把 D1/D7/D2/D8 自动标绿。本协议不新增证明要求，也不把未满足的现有检查改成 PASS。需要改变具体生产隔离准入范围时必须另行明确政策与实现，不能手填证书消除差异。

用户参与以当前会话可追溯的文字授权即可；没有要求实体在场、手签纸件或重复确认既定政策。授权应明确实际动作与边界；它不能代替原始测量和独立复算。

## 2. exec_isolation 联合验收程序与分工

实际链路：preflight.check_exec_isolation → sandbox_execution.check_certificate → full_surface_evidence.require_complete_surface + isolation_evidence.judge。当前没有已核验的自动发证入口。

1. Claude 先交新目录中的清单：当前 transport/runtime 的全套 BOUND_FILES 路径与 SHA，采集脚本 SHA，工作根、测试集合、计划及已存在原始回执的绑定索引。保留旧冻结原件，不用当前 SHA 替旧运行“重新签名”。缺运行就是 GAP。
2. 对现成原件先由 Codex 只读复算：parent token/capability=0、挂 Job 后恢复、进程树终止、临时 ACL 恢复及每次私有 profile 清理、源/日志/媒体 SHA、真实媒体解码；不能只看 rc 或报告中的 PASS。
3. 需要补采时，由 Claude 在用户授权的具名范围内执行，Codex 不发射。旧 production_isolation_acceptance.py 的 OUT 和运行 transport 的 WORK_ROOT、43 点 REVIEW_ROOT 指向具名旧路径；已有冻结目录不能直接重跑。必须先审查独立新工作根及 verifier 的一致绑定改造，保留兼容与测试，不能只复制文件或随意替换常量。该代码改造本轮尚未执行。
4. Claude 交两组原始材料：production-joint-raw-v1（完整 16 个 REQUIRED_CASES）和 sandbox-surface-native-v1（43 点、前后实现一致、error=null）；每个 case 关联实际源、transport、父进程证据、原始 stdout/stderr、事件和产物。外部/LAN case 附发送端登记、接收端原始 JSONL/summary/typed rc、健康前后对照、同轮 nonce/端点/拓扑/观察窗和哈希。
5. Codex 独立复算每个 case，并出具范围、未决项、旧证据可继承条件和当前源码绑定。LAN D9 的 lan-2026-10-13-a 可按已冻结回放归档引用，仅继承具名 D9 窗口，不能替代完整 43 点或当前实现证书；源码变化必须做兼容性核对。761/12/4 放在内容隔离索引，不混入 native case。
6. 仅当范围和全部实际结果满足适用合同，才可另提证书候选。当前 checker 读取的键为 schema=production-appcontainer-v2、fs_isolation=private_per_run、implementation_sha256、raw_path/raw_sha256、surface_raw_path/surface_raw_sha256。文件名是 data/execution_evidence.json，但本协议不创建它；把模板改为 VERIFIED 或 JSON 自报成功均无效。生产安装/放行仍在相应直接授权范围另行执行。

原始证据由 Claude/采集工具产生，Codex 的复核报告由 Codex 产生，两者保留各自来源。不要求用户自己写技术验收字段。缺 IPv6 期间可以完成静态数据、工具及本机证据整理，整体生产 exec_isolation 暂不能由当前代码判绿。

## 3. 准备顺序与逐项交付

“8 项”在代码中指 READY_REQUIRED_CHECKS 的八个名称，不是项目全部工作的数量。数据多样性、参数审批、长度处理及指标接线另列，不能漏掉。每份 JSON/JSONL 包附 evidence-index.json：schema_version、scope、真实来源/执行者、生成器 SHA、命令、起止时间、实际 rc、输入/输出相对路径/bytes/SHA、实际状态与问题；文档模板保持 PROPOSED，不预填 PASS/VERIFIED。

| READY 名称 | Claude 应交的真实材料、生成口径 | 时机与 Codex 复核 |
|---|---|---|
| gpu | 当前解释器/库版本、设备可用性及型号、相关 check_gpu 原始输出与 rc；只读查询不分配训练任务 | 可先查；按实际调用核验，不用 PID 或历史截图代替 |
| model_dir | 实际本地模型目录、config/tokenizer/权重分片清单、大小/SHA及 strict 模型检查输出 | 可先整理，不下载/改模型；核验文件完整性与约定配置 |
| data_manifest | 新候选 JSONL、源登记、转换/数学/许可/泄漏审查、make_manifest/data_check 真实输出；每条 entry 路径相对 manifest 所在目录、SHA/数量/split 正确 | 静态候选构建在 READY 前；现役 data/manifest.json 不由本协议替换 |
| run_snapshot | tools/run_record.py 产生真实 run_record.json，绑定配置 SHA、manifest、Git HEAD+未提交状态、模型与命令；不手写 ready | 数据/源码/配置固定后；prepare_snapshot 为 dry-run，不通过启动训练生成它；复算 verify_replay |
| asset_evidence | manifest 同目录的 asset_evidence.json；逐样本完整行 input_sha256、output={path,sha256,size}、math/render/semantic 证据，真实媒体与解码/数学/语义记录；总量逐条覆盖 | 静态人工核对可先做；不可信代码渲染须在 exec_isolation 通过后。可信固定 smoke 不充当全资产验收 |
| freeze_gate | eval/test 全覆盖锁、原始数据及 meta.manifest_sha256；freeze_data --check 同时给 --manifest 的真实输出 | 切分、记录和候选 manifest 固定后；旧锁只读，新版本另存，不能重写旧锁适配新 SHA |
| near_dup_calibrated | 执行规则/源码/阈值、具名独立自然标签和输入版本、混淆计数与精确分数、校准与未见验证范围、盲标/规则冻结记录 | 数据冻结前筛查；校准方案按既定 holdout 设计。当前 validate.py 固定 near_dup_calibrated=False，没有已接通的正式证据消费接口；补材料后还需审查实现，不能改 B5 calibrated 一键开门 |
| exec_isolation | 本协议第 2 节原始材料和独立复算，当前 transport/runtime 完整绑定 | 与静态数据准备并行；必须先于不可信生成代码的资产渲染，整体 READY 最后汇总 |

当前 harness 还要求：

- training_diversity_evidence.json：schema=1、status=VERIFIED、manifest_sha256、policy_sha256、record_reviews 全覆盖实际 train ID。每条绑定原始 JSONL 行 SHA（含原始行结束字节），concept_id、variant_kind、真实 user_review、独立数学/多样性与泄漏裁决。当前政策每概念至少 5 道、至少 3 类形式，全部 53 个概念按实际核对；不能拿 300 条或 47+311 的总量代替。人工认可与证据必须真实，不能代填 APPROVED。
- 资产 input_sha256 当前算法是 line.strip().encode('utf-8')，与多样性原始行哈希不同。两类字段分别生成，不把一个 SHA 套到所有表。
- 参数与长度：真实配置、参数对象规范 SHA、确认来源、执行器接受结果、tokenizer 版本/长度逐条清单和超长处置。PROPOSED 候选不得冒充 CONFIRMED；当前量化描述拒绝与 TBD 必须解决，不能只换标记。所有超参和模型配置本轮未改。
- R/E/M/F 接线：见第 6 节；在真实候选训练前先用固定人工夹具验证协议，不能试训完才发现没有可用指标。

顺序为：来源/额度/用途登记 → 静态候选与泄漏/数学审查 → 切分与新版本冻结 → 完整源/模型/参数固定 → 真实快照；执行隔离复核并行，合格后才做不可信资产渲染 → 资产与校准等材料验收/接线核验 → 最终配置和快照再次一致性检查 → 完整 preflight --ready 与 harness 前置检查 → 已授权的实际运行。快照绑定的输入改变后必须重新生成新记录。GPU/模型检查可提前，整体 READY 无需成为构建静态数据的前置条件。

当前 gate_ready 还只接受现役 data/manifest.json；新候选路径通过审查后仍需受控接入与快照重建，不得只改 dataset_manifest 指向来绕过。

## 4. 外部数据导入与短答案外测登记

[来源与用途表](DATA-CANDIDATES-HF.md)以 TheoremQA/UGMathBench 外测互斥为本轮修订口径；NuminaMath 上限/首批计划为邮件报告方案，未自动执行或更改用户额度。既有用户要求“不加题”的 holdout 当前池约束继续适用于 391 候选池，不能用外部数据扩充它。

### 4.1 独立候选交付

每来源交 source-register.json：dataset_id、official_url、固定 revision、文件列表/SHA、license_id、许可证/版权原件路径及 SHA、上游 source、拟用途、许可未决项。不要用 main 分支名充当固定 revision。卡片许可是来源声明，不是对每条上游来源的全量核验。

records.jsonl 保留 source_record_id、raw_record_sha256、problem/solution/answer 原始来源、语言、学科/难度、转换器 SHA、勘误版本与独立数学理由。图片记原始 SHA 和引用关系，不能静默 OCR 丢图；有理数转写为精确分数但保留原字段，不用浮点近似冒充精确答案。NuminaMath 的 CoT 须逐题核验，不能当权威解答或当 scene_spec 标签。

sampling-plan.json 先锁候选范围、每层整数配额、seed/算法版本、group/core 规则及上限；抽样后记录实际选中和每条排除理由。只按固定方案选择，不从全部外测得分倒选题。真实随机版本、翻译和同核心题整体分组后分配用途，不逐行随机切开。没有足够合格题时报告不足，不造数值变体凑满 300 或 2000。

leakage-review.jsonl 应绑定 train/eval/test、外测和适用 holdout 的各版本 SHA、双方记录稳定身份、文字/核心候选、独立理由、CLEAR/CONFLICT/UNKNOWN 及处置。只用现成有限证据的适用范围，未命中不自动代表全局安全。存在冲突时保留原题及题号，另版重写题干、完整过程、答案和核心解法并重新核验；主要换数字/符号仍算泄漏。冻结外测、holdout 原件不改；无法保持隔离则候选隔离存放，不在原池删除历史来假装解决。

不得将完整封存 holdout 明文给调参者；K 的受限工具应只向其返回稳定 ID/SHA 和风险裁决。新候选训练资料不能作为最终盲标会话的背景。当前 dataset_intake convert 只转 JSON 数组到 JSONL，不是 Hugging Face 下载/许可/核心隔离或自动标签工具；需要新适配器时作为候选源码单独审查。

### 4.2 短答案外测

external-eval-register.json 绑定：用途（开发或一次最终）、数据 revision/文件 SHA、基础 core_id 与 variant_id、模型/adapter SHA、prompt/图片策略、允许输入字段、生成参数、答案类型/判分器与版本、先锁规则时间、执行者与回执、缺失和排除原因。参考答案仅提供给判分端；不输出推理训练标签。

每实例结果交 identity、input_sha256、output_sha256、expected_answer_sha256、answer_type、原始输出、受限解析结果、PASS/FAIL/UNVERIFIED、理由及回执路径。先锁定分母；未知、缺图、解析失败不删除以提高得分。适用范围不完整则完整集指标 UNVERIFIED，另报已覆盖子集而非冒充全集。

有理/代数/集合/区间/矩阵等按答案类型做数学等价判定，保留定义域和分支；不把所有答案粗暴做字符串相等。源数据若规定容差，用精确有理数明确记录判据及单位，不另加未申明的小数近似。UGMathBench 分别报告基础题数 5062 和版本实例 15186 的覆盖与结果，三版本相关，不按独立样本扩张置信度。

只有短答案的任务不能直接进入 scene_spec 的指标接口或 hp_sweep 选优。不同任务若需比较，另列结果，不混成一个成功率。该外测若持续用于调参就记录为开发用途，不能再宣称一次未见最终测验。

## 5. 391 候选的资格与最终验证程序

既定 [holdout 设计 v3](../archives/reviews/codex-supervision/2026-10-07-holdout-v2-review/holdout-design-v3.pending.md)及[角色候选 v3](../archives/reviews/codex-supervision/2026-10-17-holdout-custody-mail-review/ROLE_REGISTER.v3.pending.json)保持原始冻结版本。以下是执行交付顺序，不宣称本轮已启动会话或开封。

1. 身份用 (pool_raw_sha256,record_sha256)，保留全 391 条；原 ID 有复用，不能按 ID 去掉记录。metadata-manifest.json 仅列别名、来源/记录 SHA、资格裁决、已知/未知曝光、角色可见范围和核心族 ID。未知资格不直接计入 M。
2. A_FINAL/B_FINAL/D_FINAL 的实际隔离会话，应在任何任务内容、标签和检测分值交付给它们之前建立并记录真实 session_id、历史接触声明、角色独立性与工具/访问范围。不能继承当前 Claude/Codex 的项目上下文充当未见会话；本协议不启动多代理。K 仍按受限机械保管落实，不能参与判分或调参，实际控制待回执。
3. 独立资格审核完成后列逐成员 IN/OUT/UNKNOWN 与依据，报告真实 M；保持全池历史，不补题。成员资格通过与检测器 CALIBRATED 是两个结论，不能用同一个 GRANTED 盖住所有阶段。
4. 依设计做整核心族 C/F 阶段隔离、辅助角色/题对总体、各层 N_h/m_h、预算与抽样器源码冻结，再产生真实随机位/秩并封存。上限 B_C=540、B_F=360 对每个总体独立计算，不保证自然正负例数量，不把 391 当已获资格数量。
5. 密封交付分两层：外层 package-manifest.json（package_id/phase、字节数/SHA、角色收件目标、权限/访问日志、封存/转移时间）；内层 input-index.jsonl + 绑定完整题干/过程/答案/必要上下文的材料。标注包隐藏检测分值、预测、旧结论与核心分组。metadata 只能交获准角色，不让调参者由映射读取最终题文。加密是可用手段但不是唯一方案；应交真实控制证据，不把“zip+SHA”当内容访问控制。
6. A/B 各自独立封存 labels.jsonl（pair_id、两端稳定身份、POSITIVE/NEGATIVE/UNCERTAIN、完整数学理由、输入包SHA/标签SHA/会话身份），双方封存前互不可见。冲突由独立 C 角色按既定实际曝光范围裁决，单人不能冒充双审。错误题解保留原字节，另出勘误并说明影响。
7. 只用 C 校准阶段锁定 rule-lock.json（执行规则/源码、精确阈值、参数、输入版本、锁定时间、最终封存包SHA）。之后 D 在独立会话按固定规则做一次 F 验证和精确复算，报告 P1/P2 各层 TP/FP/TN/FN 与未确定项。现有有限证据政策不要求额外全局证明，但也不把未实际生成的标签/资格填为通过。
8. 按设计的有限总体超几何界及前提判断：两个总体分别要求 FPR_U≤1/100、Recall_L≥19/20，分母须可定义；假设不成立、自然正例不足或界不能达标保持 UNCALIBRATED。不得重抽到通过，不把共享成员题对当独立 Bernoulli。
9. Codex 复核绑定与实际交付后，按具名版本给出 MEMBER_ELIGIBILITY_VERIFIED 或仍待证据；只有全部最终设计要求满足才给 FINAL_HOLDOUT_VERIFIED。二者必须写 scope，不给“全池自动 GRANTED”。此项不直接解除操作系统 exec_isolation。

不要求现在把封存题文发给 Codex；先交外层元数据、真实角色/访问回执及原件绑定索引即可规划下一步。

## 6. render_executor / judge_script 与 R/E/M/F 接线合同

这是待实现的逐题证据协议；当前 eval_step.render_check/judge 仍在启动外部进程前返回 UNVERIFIED，aggregate 不产出正式 R/E/M/F，run 返回 2。设置两个配置字段为脚本路径不会接通。本轮没有改这一行为。

### 6.1 分工与调用边界

Claude 提交一个独立候选 PR/工作目录中的适配器实现与固定夹具，不改真实模型超参、不训练。实现应明确 render_executor/judge_script 的受审查源码 SHA、依赖、协议版本、批准入口和权限。Codex 在同一版本上独立做对抗验证并修复问题。未完成接线验收前不安排真实试训来“补指标”。

harness 只生成数据请求，不以 shell=True、eval/exec、任意命令串、宿主 fallback 或任意 judge 回调执行模型输出。生成内容是数据，不是工具指令。由父进程执行白名单编译器/渲染器，遵循现有 AppContainer + JobObject 实际证据与超时/内存/输出根约束；生成代码只有在 exec_isolation 合格后才能运行。数学解析继续受限，不得把字符串直接送 SymPy 的任意求值入口。语义判定若需要 AI/API 只在实际获准的调用范围内使用，不自动出网、上传题库或读密钥。

### 6.2 请求与逐样本回执

request.json 的合同键为 protocol_version、run_id、round_id/candidate_id、scope、config/manifest/training_manifest/adapter/generated_specs 的 SHA、evaluator/compiler/renderer/judge 源 SHA、固定题单及其 SHA。每条 identity=(split,problem_id,sample_id,row_index)，绑定完整输入记录 SHA、实际生成 spec SHA、所需场景、断言/语义基准 SHA。生成日志与转换后的 scene.py 各有独立 SHA。当前 generated-specs.json 尚不导出 row_index，接线实现须补齐并重新绑定，不可用数组位置在不同阶段隐式猜测身份。

response-index.jsonl 逐样本含同一 identity/输入绑定、各阶段 decision=PASS|FAIL|UNVERIFIED、理由码、证据路径与 SHA；原始 stdout/stderr、真实 rc/timeout、父进程 token/job/profile/ACL 清理证据、产物列表与解码结果、数学断言/人工或判定器理由均可追溯。实际数值用整数或精确分数字符串。

父进程拒绝根外路径、重解析点逃逸、旧回执、重复/缺失/额外样本、错误 round/run/candidate、源码或输入漂移、字符串伪造 rc、无产物 rc0 以及响应里自报的 VERIFIED。回执必须读实际文件和独立验签/哈希，不能只信子进程输出。输出只写新轮次目录；已冻结证据不重写。

### 6.3 指标定义、分母和未知

对每个 split 先由冻结输入确定问题集合 Q_s；同一问题的全部必需样本/场景集合 S_q 也先锁定。不能只计成功生成的题。任意一条必需样本失败使该题对应指标失败；有缺证据则该题该指标 UNVERIFIED，不能因失败或未知删除分母。

| 指标 | 单题 PASS 所需证据 |
|---|---|
| R render | S_q 每条均产出协议约定的最终 PNG/MP4、大小/SHA 匹配，真实完整解码；媒体非空且对应正确生成样本。只有文件存在或 rc0 不够 |
| E executable | S_q 每条 schema、受审查转换、完整沙箱执行/边界与树清理检查全部通过，并满足 R 的产物条件。E 的 PASS 集是 R 的子集 |
| M math | 每条必需数学结论、适用条件和题解/动画对象对应有独立可核对的精确断言或完整审查理由。schema、题解复制、CAS 未定结果或短答案正确均不自动算动画数学正确 |
| F fidelity | 根据事先锁定的逐题语义清单，对实际完整画面核对对象、坐标/曲线、步骤顺序、视觉关系和叙述；每项有时间/帧定位与判定理由。抽几帧或固定公式编译不能宣称全动画忠实 |

每项已全部完成真实 PASS/FAIL 判定才可汇总为 status=VERIFIED、passed=p、total=N=|Q_s|、rate=str(Fraction(p,N))；N=0 或任一题未知时该完整指标 status=UNVERIFIED、rate=null，另报已审覆盖和失败/未知清单。观测到的真实失败仍可构成已验证指标的一部分，不能把“VERIFIED”理解为全对。M/F 若只完成子集，仅给具名子集结果，完整指标仍未知。

全量报告含 total_questions、total_samples、by_split.eval/test 各自四指标及原始分子分母，全量 passed/total 等于各 split 加和，不求简单平均。R=1、E≥19/20 的停止目标不变，M/F 不另造硬线；M/F 未验证不得用于改善、排名或达标声明。选优仍用当前已核验的 E→R→M 精确比较，F 不擅自加入排序或改变目标；不能只凭 M 胜出。

当前完整循环要 R/E 全量 eval/test 双列；hp_sweep 固定子集只有被该子集实际覆盖的题，分母与固定子集绑定，不能伪装完整结果。沿用循环监视的 test 应如实称持续监测集，不能再声称未见最终 holdout。试训候选的固定子集、输入和评测器版本一致后才可比较，不按不同覆盖数或混合 QA 任务强选胜者。eval_loss 尚未实现选优，不在本合同补写成已支持。

### 6.4 接线验收最小夹具

先以固定人工夹具和 Mock 传输验证：有效逐题回执、真实 FAIL 分母、缺/重复/额外 ID、错 run/config/adapter/spec/源码 SHA、损坏/空媒体、rc0 无产物、超时/异常、路径逃逸/重解析点、数学假命题及未定、F 清单缺失、同问题多场景中一条失败、分数/计数矛盾与 bool 冒充整数。无真实执行协议时始终拒绝启动任意脚本。

随后在具体获准的隔离范围做最小集成复验，保存真实媒体与 token/job 回执。只有该版本完成可复算的 R/E 逐题合同，eval_step 才能把当前无条件返回 2 改成“正式评测完成且绑定有效时返回 0”；真实 metric 的 FAIL 进入精确计数，未知、协议错误、缺证据返回非零。harness 与 hp_sweep 消费同一经过核验的报告，不能为了产生 winner 提前放行。

M/F 接口可以先留未知，独立审查机制落实后再扩；不因此伪造 M/F。题量与实验范围保持已授权边界。

## 7. 下一次提交的最小目录

新目录交：evidence-index.json、readiness-items.json（八项及附加项逐条实际状态）、对应原件与日志/哈希索引、source-register/sampling-plan（若涉及新来源）、holdout 外层登记（若有实际进展）、评测接线候选源码与夹具回执（若已实现）。

各文件注明 DESIGN / COLLECTED / INDEPENDENTLY_VERIFIED / GAP，未知字段用 null 并说明，不填想要达到的结果。Claude 先完成静态来源/候选登记和无模型夹具实现；Codex 审查、修复、复验并给出具名资格；用户既有政策不重复索取。实际模型配置变更、原生补采、训练或生产开放仍分别按真实授权和门禁执行。
