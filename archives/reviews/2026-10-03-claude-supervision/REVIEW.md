# Claude Code 监管复查（2026-10-03）

本轮任务：核对 Claude Code 当前工作和验收证据。此前 PDF 修订任务已取消，本轮不再代改两份 PDF。

项目：D:/Animation-Model-Training。审核覆盖 f5e0897 → 4db74ae → e7c0e8f 的变化；工作树同时存在其他未提交改动。本报告不把自报测试或冻结等同于最终验收。

## 已独立确认

- 本机主 manifest：6 条目，问题 0、quarantine 0；两个冻结数据文件内容校验通过。
- train/eval/test 精确交叉重叠为 0；当前文本近重复阈值下没有越界对。阈值仍 UNCALIBRATED，不能据此声称题目族隔离已校准。
- 数据规模：train 63 条、eval 100 题 × 3 解法（300 行）、test 150 行。正式训练没有启动。

## 需要整改 / 未验收

| 编号 | 发现与影响 | 独立证据 | 状态 |
|---|---|---|---|
| S1 | 冻结锁从子目录迁到 data/ 后，status 仍只查子目录，因此误报未冻结 | 全量测试 353 passed、1 failed、29 subtests；稳定 e7c0e8f 单测再次失败 | 已发送 Claude，待修复复验 |
| S2 | 新 checkout 不可复现：4 个 raw JSONL 的换行归一化使登记 SHA256 和 size 都失配；两个锁绑定的 manifest SHA256 也失配 | 本地独立 clone(e7c0e8f)：data_check 8 个问题；fresh-checkout-proof.json | 已发送 Claude，待修复复验 |
| S3 | eval 100/100 组除首项方法标题外，三条解法的场景对象与步骤均相同，无法体现不同解法 | shared-method-scenes.json 列出全部 ID；eval-calc-023-s1 混入裂项/凝聚步骤；eval-prob-010-s2 未展示 G(z)、G′(1) | 需逐解法对应审查，冻结数据先提出新版本方案 |
| S4 | eval-linalg-023-s3 依赖“解法一/解法二”，独立记录只给恒等式，没有所引用的完整分解 | 当前 JSONL 记录 | 待补自包含或明确读取完整题组的契约 |
| S5 | 子 manifest 把镜像 JSON/README 纳入数据条目，且 JSONL 的 raw 角色与顶层 eval/test 冲突 | 独立 harness：MF009×2、MF005×2（另 MF010×2 为文档提示） | 待统一入口与角色 |
| S6 | 进度汇报把 render/math 环境诊断混入八个必需门禁，出现“8项6 PASS”同时“4 FAIL”；状态文档仍混有旧阶段文字 | Claude 最新输出、PROGRESS、TRAIN_PREP_PLAN、独立 harness D011/D012 | 部分文档已更新，仍待完整核验 |

## harness 结果与边界

独立重跑读取 4db74ae 时工作树：hard=0、quarantine=914、info=833；450 条记录均为 quarantine。问题条数可在同一条记录上累加，不是 914 个不同样本。此结果包含缺动画证据、内部许可证、清单/换行/文档等项，不能汇报为“只剩三类问题”。审批确定数据角色，不能代替真实资产验收。

八个必需门禁的当前汇报口径应为：gpu、model_dir、data_manifest、freeze_gate 本机 PASS；run_snapshot、asset_evidence、near_dup_calibrated、exec_isolation FAIL，即 4/8。render_gate/math_gate 固定样例为额外环境诊断。新 checkout 还暴露 manifest/冻结绑定的可复现性失败。保持 NOT READY。

## 已采取监管动作

通过 AI Bridge 发出 msg_239、241、242、244、245、246、247，要求提供当前任务/授权/运行状态，并交付上述反例整改。Claude 已依据早期反馈更新部分状态文档（e7c0e8f）；其余反馈截至本报告生成仍待对方确认与独立复验。未改冻结样本，未训练、下载或安装。

测试第一次因本审查临时目录父目录未创建而出现 setup errors，不计为代码缺陷；修正目录与 UTF-8 环境后取得上述 353+1 结果，随后稳定 HEAD 重现 S1。

审查证据保存在本目录 evidence/。后续修复必须以新证据更新状态，不能通过削弱断言、忽略失败或直接改冻结记录关闭问题。

## 继续监管（19:08，北京时间）

用户再次要求监管。当前 HEAD 仍为 e7c0e8f，无新整改提交；已通过 msg_248 催办 S1–S6 并指定回信收件人为 codex。截至本次检查，codex 收件箱没有新的整改结果。上列问题继续保持未验收状态。


## 第二轮复验（19:19，北京时间）

Claude 已通过 msg_249/251 确认收件和整改。最新独立测试 HEAD=5904993：**354 passed + 29 subtests passed**。原状态漏检测试恢复通过，S1 原反例已关闭。

独立 fresh checkout 的主清单 6 条、train 清单 4 条及冻结数据内容检查均通过。但**锁的 manifest 绑定仍未修复**：两锁登记 bec11da867c8…，checkout 实际 manifest 为 b4b61618ee60…；worktree manifest 仍有 62 个 CR，git blob 为 LF。证据：evidence/fresh-checkout-round2.json。S2 保持未验收，已反馈应修生成器而非只一次性归一化。

S5 的 JSON 镜像入口与角色冲突已整改，但两份子 manifest 仍把 README.md 登记为 eval/test；独立 data_check 都返回 1。应仅登记 JSONL 样本入口，文档另列。

动画整改方案（5904993）仍计划覆盖 data/v1 文件、删除旧 v1 锁。本监管已退回，要求保留冻结版和历史证据，在独立 v2/候选目录制作可审查数据，再决定正式切换。S3/S4 未验收。另扫描到 31 条跨解法引用候选，已给逐 ID 清单；词法引用不代表必然错误，需逐条判断是否自包含。

状态真实性补充反例：仅放置一个坏 JSON 的 eval-broken.lock.json，status 仍返回 [OK] 冻结锁1个与 exit0。需明确区分“发现锁文件”与“校验冻结有效”。证据：evidence/status-broken-lock-probe.json。

第二轮 harness：hard=0，450 条仍 quarantine。新增 F011×450 是 efficiency_tags 中残留 Markdown 项目符号，不是 answer 缺失；已有更正回信。动画资产验收按当前主 manifest 应覆盖 63+300+150=513 条，而非仅450条。

最新督办消息：msg_250、252、253、254、255、256。当前保持 NOT READY，不启动正式训练。

## 新增 B4 网络防护复验（19:24，北京时间）

Claude 新提交 71195d9 引入 sitecustomize 的 socket 拦截与死代理环境，并自报 exec_isolation PASS、preflight 5/8。

独立回环实验已证：相同 shim 环境中，普通 socket.connect 被拦截，但标准库底层 _socket.socket().connect 成功连接本机临时监听端口；没有访问外网或传输用户数据。此时 check_exec_isolation 仍返回 True（执行隔离已验收）。证据：evidence/network-loopback-bypass.json。

结论：该机制可作为常规 Python 调用的防护，不能作为完整网络隔离的验收证据。已要求 Claude 将此能力与 network isolation 分开，完整隔离继续 UNVERIFIED 并阻断就绪。当前 trusted=False 仍拒绝不可信渲染，此行为已独立确认并要求保留。

## 第三轮独立复验（19:30，北京时间）

稳定 HEAD=d701ee4。完整测试 **360 passed + 29 subtests passed**；独立新 checkout 的验证器返回 ok=true、problems=[]，清单条目哈希/大小、提交字节与双锁的清单绑定均通过。两份子清单均仅登记 1 个 JSONL，data_check 为 0 问题。freeze --check --manifest 两锁通过，status 如实显示结构/覆盖/清单绑定一致。

**S2 与 S5 已独立关闭**。S1 的原漏检测试及本机状态查询已通过，坏锁已区分为校验未过。历史错误证据保留，不能再以旧结果表述最新版本。

S3/S4 的候选版本尚未交付实际整改数据，继续未验收。PLAN 已纠正为保留 v1、另建 v2，但现有审计/状态/冻结入口仍部分写死 v1 或要求所有历史锁绑定同一当前清单；已要求先提供版本明确的入口，防止用 v1 检查替代 v2 验收。候选来源也应独立保留，使 v1 原始内容可追溯。

B4 网络隔离仍有本报告已记录的绕过反例；可信样例可运行不等同于完整隔离通过。其他训练门禁不因此放行。督办 msg_261 已给闭环和剩余事项。
