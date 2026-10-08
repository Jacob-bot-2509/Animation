# 三项验收处理与 Claude 新代码复验

本轮已修复私有作业隔离、结构候选筛查、验收门禁、具名切线动画及 Claude 新训练代码的确定性缺陷。最终 475 项回归全部通过，16 项具名原生边界测试经独立重算通过。整体仍为 **NOT READY**：结构规则未完成独立留出校准，资产仅 1/497 条完成数学/语义/真实媒体验收，生产隔离证据尚未获准写入。没有启动训练、扫参或生成代码执行。

| 三项任务 | 本轮结果 | 未完成部分 |
|---|---|---|
| 结构泄漏检测与独立校准 | 增加 problem-only 结构候选筛查；补发现并隔离一条直接代值训练题 | 候选筛查不是已校准分类器；新增漏检原始失败保留，需要新的独立留出集 |
| 全量资产验收 | 497 条逐条源码审计；修复导数撇号被删问题；切线题真实验收 1/497 | 其余 496 条数学/语义/渲染未全部验收，通用模板仍有步骤截断、替代图形等缺口 |
| 生产隔离传输与联合验收 | 主渲染入口切换为独立 AppContainer、私有缓存、临时权限回收；16 个具名原生测试通过 | 有限测试范围不等于所有协议/端点安全；写入生产证据被自动审批拒绝，当前 CLOSED |

## 活动数据与泄漏定义

当前 train 47 条、eval 300 条、test 150 条，共 497 条；活动训练目录为 `data/v2/train/leakage-isolated-v3-2026-10-05/`。累计隔离 16 条训练记录，涉及已识别 18 对题文。原始训练记录和旧清单/冻结锁原字节保留，eval/test JSONL 与 B5 标注/报告/PDF 未改变。两个冻结锁均有效且绑定当前清单。

新隔离 `calc-series-018`：训练已求出和函数 $S(x)=-\ln(1-x)$，评测 `eval-calc-011-s1` 是代入 $x=1/2$ 即得 $\ln 2$。旧结构筛查没有命中这一对；该独立失败保存在 `new-independent-leakage.json`。修正后能作为候选检出，但这个案例已进入开发过程，不能回头当作独立校准成功。

原 228 对开发诊断为 TP=17、FN=0、FP=3、TN=208；召回 1、候选假阳性率 3/211 仅适用于这份已知开发材料。当前全量候选筛查没有命中，不代表 UNKNOWN 对均不泄漏。`near_dup_calibrated` 仍为 false。

Claude 的 msg_422–423 转述了“难度升级变体可以保留”的用户说明。本会话已向用户请求确认边界；尚未据邮件转述修改定义或恢复隔离记录。确认前沿用本会话已明确的直接套解结构隔离口径。

当前 manifest SHA256：`801f7036cf14b9d44e3a84874878ad176b19124fbfe74154cd5e95c8cbcfc448`。

## 原生隔离修复与实际测试范围

初次边界复验发现共享 AppContainer 身份能写旧作业目录；新传输对每个作业新建唯一 profile，安装/venv/Python 只读，仅本作业 work 与缓存可写。父进程在 resume 前核验真实 AppContainer 令牌、SID 和零能力数，确认已加入 2 GiB JobObject。结束时停止整棵进程树，撤回本次唯一 SID 的临时权限，核对四个根目录 ACL 前后哈希一致，并删除本次用户 AppContainer 配置。无 host-process fallback。

原始 v2 联合测试与独立重算覆盖：中文/公式两项真实渲染；项目外读取/写入、工具链写入、跨作业目录/缓存写入五项拒绝；TCP/UDP 的 IPv4/IPv6 loopback 四项；公网 TCP IPv4/IPv6 两项；超时/根进程退出的子树清理两项；内存限制一项。所有实际媒体均完整解码，产物、探针和执行实现哈希匹配。

loopback TCP 明确记录 `TimeoutError`，耗时分别为 2007/1000 秒与 503/250 秒，不能声称立即返回 WinError 10013。UDP 的 send 返回成功，但接收端没有收到沙箱 nonce。四个接收端在同一窗口收到了普通进程前后对照的 nonce，持续观察 20 秒；结论为本次指定端点和窗口中无沙箱数据送达。公网仅连接 `1.1.1.1:443` 与 `[2606:4700:4700::1111]:443`，前后普通进程可连，沙箱均返回 10013，不发送应用数据。

`production-joint-raw-v2.json` 和 `production-joint-independent-review-v2.json` 保留完整证据。此前未记录 TCP 错误类型的结果没有改成通过。以上为有限范围验证，未宣称覆盖所有协议、端点或未知攻击。

使用的临时用户配置生命周期参考 Microsoft 官方 [CreateAppContainerProfile](https://learn.microsoft.com/en-us/windows/win32/api/userenv/nf-userenv-createappcontainerprofile) 与 [DeleteAppContainerProfile](https://learn.microsoft.com/en-us/windows/win32/api/userenv/nf-userenv-deleteappcontainerprofile)；实测以父进程证据和清理记录为准。没有改动 C 盘系统文件或源 MiKTeX 安装。

## 逐题资产与分数显示

原通用模板会删除导数公式的撇号，已改为保留数学文字并用安全字符串字面量生成源码。497 条原模板源码均可编译，但静态检查发现步骤截断等语义缺口；编译成功没有被当作数学或视觉正确。

`calc-derivative-001` 使用完整输入行哈希绑定的专用场景。独立符号核对确认 $f(1)=1$、$f'(1)=2$、切线 $y=2x-1$；63 帧完整解码，八帧时序图及末帧已人工核对。黑色轴与整数刻度、蓝色抛物线、黄色闪烁切点、从切点向两侧延伸的橙线、右下角两项白色公式均符合五条原始步骤。可见小数刻度已改成整数。

证据见 `asset-admission-v3.json`、`tangent-contact-sheet-v3.png` 和 `tangent-final-frame-v3.png`。`data/asset_evidence.json` 明确记录仅 1 条已验收、其余 496 条未完成；更新前文件原字节归档，整体资产门禁仍失败。历史 v1/v2 画面与 native JSON 未覆盖。

## Claude 新训练代码的修复及限制

已接收 msg_421 的训练循环设计，并独立读取最新提交。修复 `train_step.py`、`eval_step.py`、`train_loop.py`，同步调整 `hp_sweep.py` 两处配置绑定：

- JSON 提示词花括号转义，消除实际可复现的 `KeyError`。
- 训练包含完整 assistant scene_spec 目标，对 prompt/padding 使用忽略标签，保留真实目标/EOS；不允许截断掉监督目标。训练与生成使用匹配的 chat 边界。模板边界不匹配则拒绝，不冒充兼容。
- 修正 `judge=judge(...)` 的变量遮蔽。
- 未知、非法、越界指标不能触发达标停止；目标可执行率以 19/20 表示。连续三轮没有改善需要四个检查点；未知指标不能证明平台。
- eval/test 明确由 manifest split 标记，方法行按题分组并分别报告；schema 合格率不再冒充可执行率。执行器仅返回 rc=0 不得伪造渲染/数学/语义率。
- 真实配置/manifest/源码重放快照先准备再检查，缺文件、配置漂移、源码快照截断、非法 run_id 都拒绝；直接训练/评测入口也先检查门禁，只调用具名已审阅训练/评测脚本。

监督目标及 chat 模板用法参考 [Transformers chat templates](https://huggingface.co/docs/transformers/main/chat_templating)。本轮没有加载模型或实跑 GPU 训练，因此没有声明训练效果、Qwen 模板实机兼容性或完整评测协议已验收。外接逐题渲染/判定协议仍未接线，四指标如实 UNVERIFIED，评测步返回阻断，扫参不能因此选出假胜者。

## 最终复验和需要的授权

最终全套 **475/475** 测试通过，0 失败、0 错误、0 跳过；`data_check` 0 问题、0 quarantine，双冻结锁通过，`git diff --check` 通过（仍有既存换行转换提示）。源文件及前后 SHA 位于 `final-source/`、`final-file-manifest.json`。执行核心有用户授权的实际修改，监听基线保留，没有宣称旧 11 核心全部无漂移。

最新监听仍运行，Claude 进程存在但子作业为空；这只能说明采样时没有子作业，不能据此断言卡死或正在计算。当前 HEAD 为 `9ba021f01a836e284c941c5f3a38699a5b95bfe0`，本轮 Codex 没有创建提交。阶段结果已通过 AI Bridge msg_424–426 交接，要求避免覆盖本轮四个训练工具和绕过 CLOSED 门禁。

自动审批拒绝了“写入 `data/execution_evidence.json` 并使生产生成代码门禁通过”：理由为有限边界测试不足以代表全面生产验收，且此前授权没有明确包含按该有限范围放行。被拒写入未执行，也未改用其他工具或让 Claude 代写绕过。若用户明确接受已登记 16 项测试的有限范围并授权该具体写入，才可再次走审批；此举会允许生成代码进入 AppContainer，但其他就绪门禁仍失败，不会启动训练。当前建议保持 CLOSED，继续完成独立校准与其余资产验收。

最终机器复验：`final-independent-verification.json`；全量日志：`regression-all-v2.log`。历史 `2026-10-05-readiness-completion/READINESS_REPORT.md` 描述的是旧 48 条训练/498 条记录检查点，保留作历史资料，本报告为当前状态。
