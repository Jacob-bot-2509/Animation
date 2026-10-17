# 新邮件审查、准备协议与文档修复

批次 run-a8135009f6b64c198c0f3a01d36dc55b，邮件 851/852。

结论：851 的程序/分工/顺序请求已交付（PASS，仅限协议）；852 引用的两份文档存在真实矛盾，Codex 已修订并交付逐项协议（REPAIRED_PASS，仅限文档与设计合同）。这不等于数据已导入、holdout 已获资格、评测已接通或训练 READY。

## 实际修改

- docs/DATA-CANDIDATES-HF.md：消除 TheoremQA 同时当训练题源与外测集的冲突；按邮件所述外测方向，保持整集 EXTERNAL_QA_ONLY，参考答案不进入模型提示。区分 NuminaMath 中文来源与实际语言；将 5062×3 精确写为 15186 并保留基础题/版本相关性；撤除 GPL“传染性”及风格研读“无需许可”的泛化判断；ManiBench/四个 manim 来源缺具体版本许可时保持候选。修正把完整训练 READY 当作静态准备前提的循环依赖。外部短答案评测与动画四指标分账。
- docs/TRAINING-LOOP-DESIGN.md：移除旧题数和百分数表述，保留精确 R=1、E≥19/20、3 轮平台和 8 轮上限；规定固定分母/按题汇总/未知状态。修正“先要求快照通过、再创建快照”的说明顺序；明确持续监测 test 与最终 holdout 的区别；将已定义合同与尚未实现接线分开。
- docs/READINESS-EVIDENCE-PROTOCOL.md：新增可交付的程序，逐一回应 851/852 的全部请求：操作系统联合验收、用户参与、八项 READY 与附加检查、候选导入/切分/冻结/许可/泄漏核查、外测登记、391 成员及最终资格、A/B/D 会话与封存包、逐题 render/judge 及 R/E/M/F 接线合同、分工/依赖和最小夹具。

当前规范入口：
[准备证据与接线协议](D:/Animation-Model-Training/docs/READINESS-EVIDENCE-PROTOCOL.md)、
[修订的数据清单](D:/Animation-Model-Training/docs/DATA-CANDIDATES-HF.md)、
[修订的循环设计](D:/Animation-Model-Training/docs/TRAINING-LOOP-DESIGN.md)。

进入修改前已发送 ownership msg_1792175898259_853，锁定三份文档归 Codex 负责；写入前核对原文 SHA，未覆盖他人并行版本。修改前后字节和源绑定保存在本目录。

## 代码核验发现的实际限制

exec_isolation 当前读取 data/execution_evidence.json，不凭证书字样或用户在场自动通过；它复算 16 个联合 case 与 43 点，并绑定当前后端/运行时。签名/数学泄漏证据不属于操作系统边界证据。D9 旧 LAN 窗口和 OneDrive 回放各自有范围，不能替代整套原生证据。

D2/D8 延期不阻塞静态准备，但当前 require_complete_surface 仍要求全 GREEN；用户刚确认的是有限内容隔离政策，没有自动改变这套 native checker。旧采集器/transport/verifier 的写入根仍指具名旧路径，冻结根禁止重跑；新独立工作根的代码与一致绑定改造尚待实现。本轮只给修正后的执行次序，没有执行原生采集或放行。

validate.py 仍固定 near_dup_calibrated=False；旧 B5 自报不能解除它。近重复证据消费接口还需实现和审查，不能叫 Claude 仅补一个 JSON 来假装通过。eval_step 的 render_check/judge 当前拒绝启动任意外部脚本，aggregate 四指标未知，run 返回 2。新协议不是现成插件能力。

协议逐项区分资产完整行 strip 后哈希与多样性原始行（含行末）哈希；保留真实参数审批、配置 TBD/量化拒绝、逐条多样性、token 长度及快照重建事项。没有修改这些检查结果或模型配置。

## 授权与材料范围

用户有限隔离政策的直接确认保持有效，无需重新确认；不新增事前全局证明要求。邮件里的新数据额度、其他角色或“用户拍板”只按其来源登记，未转成 Codex 自动下载、开训、外测或改模型的权限。用户无需实体在场或补纸质签名；原有政策文字不重复索取，实际新动作只按相应已授权范围执行。

391 候选原池和冻结角色登记未改。成员资格、检测器校准、最终验证分阶段给具名结论；没有开封题文、启动独立会话、创建标签、填 GRANTED 或重新抽样。

## 复验与证据

两封邮件的 packet/原件/账本内容哈希一致。独立静态核验源码合同、三份活动文档与快照、八项名称及相关字段、精确分数、所有活动文档本地链接；具体具名检查和结果见 independent-verification.json。检查不是训练或原生实验，不把数量称作回归测试。

本轮只改文档；未重跑已通过且源未变的 hp_sweep 或自动化测试。源码、配置、数据、数学 CURRENT_STATUS、旧角色/holdout 原件均保持所绑定字节。后台服务与调度器未改，未提交/推送 Git。

许可/规模/字段的事实以官方页面核对，引用与查询结果摘要见 PRIMARY_SOURCES.json；来源有 NuminaMath、TheoremQA 官方卡片，UGMathBench 官方卡片/仓库与许可证。本轮只读这些页面，没有下载数据集、接触凭据或上传项目。

后续：Claude 按协议先做静态来源/候选登记与无模型接口夹具，保留新目录原件和 SHA，提交实际进展。Codex 独立审查修复；未接线、缺证据或现行 checker 不满足的部分据实保留，不产生虚假 winner/证书。

最终具名静态检查 25 项、活动文档本地链接 10 处均通过；不是 25 项原生或训练测试。审查脚本自身的假设/转义/历史清单路径修正见 verification-attempts.json，不计作项目源代码缺陷。
