# 训练前代码与环境审查（2026-10-03）

**结论：现有 CUDA 环境正常，当前仍为训练准备阶段。正式训练后端、评测数据和部分证据门禁尚未齐全，不能仅凭模型筛选或单元测试宣布训练 READY。** 保持用户已选的 Qwen3-4B baseline。本轮未加载模型权重、未推理、未训练、未安装或下载。

审查基线：a7b1c34；独立全量测试原为 335 passed + 29 subtests，小修后 **353 passed + 29 subtests**，指标定向 24 passed。被审查代码/配置与环境见 [before.json](before.json)、[after.json](after.json)、[verification.json](verification.json)。与 Claude Code 通过 AI Bridge 231–235 同步；主力负责训练后端、门禁和筛选脚本，Codex 处理指标小修。

## 环境检查

| 项 | 实际结果 | 判断 |
|---|---|---|
| Python | 项目 .venv，3.13.13，Windows 11 | 当前依赖检查无冲突，未发现需要先降级 Python 的证据 |
| GPU / 驱动 | RTX 5060 Laptop，8151 MiB；592.82 | 检查开始时 GPU 空闲；查询不等于已验证真实训练容量 |
| PyTorch | 2.11.0+cu128；CUDA 12.8 可用；含 sm_120；BF16 可用 | CUDA 构建与硬件能力匹配，当前不是 CPU-only torch |
| HF 栈 | transformers 5.18.0 / peft 0.21.2 / accelerate 1.15.0 / bitsandbytes 0.50.2 / tokenizers 0.23.2 | 记录当前版本，不在训练前盲目升级 |
| pip check | 无依赖冲突 | 只证明包的依赖约束，不证明所有 GPU 内核或正式训练路线已验收 |
| datasets / trl | 未安装 | 不是所有后端都必须依赖它们；先确定后端再按需安装，不为准备审查额外装包 |

现有 requirements.txt 主要锁定 Manim 栈，未记录上述训练栈。已另存完整 [安装版本清单](dependency-inventory.json)，它是环境快照，**不是带下载源与 wheel 哈希的可重建锁文件**。正式训练前应分开维护运行/训练依赖锁，保留 torch 的 CUDA 构建及安装来源，完整环境与运行参数入快照；不需要现在重装正常工作的环境。

## 必须补齐的训练能力与门禁

| 项 | 当前证据 | 最迟处理点 |
|---|---|---|
| 正式训练后端 | src/animtrain/backend.py 仍是注册表占位；load/train/save/evaluate 默认抛 BackendNotApproved；无正式数据 collator/训练器 | 正式训练执行前由 Claude Code 接入。筛选 QLoRA 脚本不是该后端的实现 |
| 训练配置与目标 | train_config.template.json 是 TBD 契约；模型名已选 Qwen3-4B，但量化、种子、LoRA、长度、lr、梯度累积等未冻结 | 先出具体可审阅配置与快照，执行时必须消费该配置，不手写另一套参数 |
| 数据与独立评测 | 63 条 provisional train 的 manifest 验证通过、哈希不变；eval/test 目录没有实际 JSONL；near_dup_calibrated=false | 正式评测/训练 READY 前补独立数据、校准、隔离及冻结。不能从筛选用的 train 样本宣布泛化验收 |
| 资产证据和隔离 | asset_evidence.json 缺失；网络执行隔离仍为未验收项，当前合同八项门禁未齐 | 按现有任务/阶段契约补齐真实证据，不能填状态或移除守卫来假装 READY |
| **B2 多解身份漏检** | 2 条合法样本（1 条普通 id，1 条复合身份）通过 manifest；只给普通 id 一条证据，check_asset_evidence 却返回全覆盖 1/1 | 真实多解 eval 接入前统一 record_identity，逐条不得静默丢弃。反例见 [additional.json](additional.json) |
| **模型完整性门禁** | strict check_model_dir 仍接受 131 字节 LFS 指针；provenance 遇 index 分片问题仅 WARN 后返回 0 | 正式模型消费前将完整性结果接入门禁：缺分片/指针/零字节必须拒绝。当前 Qwen3-4B 已有 v2 provenance、3 个权重文件、index_problems=[]；本轮未重算全部权重 SHA |
| **筛选证据未归档** | 归档目录只有 4 个文档，无 evidence/；临时组已不存在，cleanup 清单列出 32 个文件 | 先定位外部归档或备份并验证哈希；找不到则如实标不可独立复核。不要凭 PDF/删除清单补写原始输出，不自动重跑模型 |

筛选 DECISION 中将 9.40/10.12 GB reserved 写为“溢出”，但对照表同时写两模型失败步=0。超过物理显存预算可以表达资源压力，**不足以证明实测发生 OOM**；allocated、reserved、共享内存和失败状态应分别记录。Qwen3-4B 的选择保持不变，原始成绩等待证据复核。

## 已直接修复：B3 指标可信度

独立反例确认：合法 JSON + 明确 math_error 会被 finalize_result 改为 ok；与当前样本无关的数学复核项可让 1 条结果产生 200% 通过率。

本轮改动：
- 显式 math/render/truncated 等失败不因字段合规而消失，失败类始终校验。
- 字段合规率与语义/执行成功率独立计量。
- 数学复核绑定当前结果 ID；部分未复核保持 NOT_MEASURED 并报告已复核量。
- 重复结果 ID、无效状态/解析标志、负数/NaN/inf/非数延迟拒绝。
- p95 明确为 nearest-rank，指标契约版本为 1；汇总对副本定稿，不修改调用者记录。
- 旧延迟测试使用相同 ID 重复十次，改为唯一 ID，原中位数/p95 断言不变。

改动文件：src/animtrain/metrics.py、tests/test_metrics_review.py（18 项回归）、tests/test_metrics.py（仅 fixture ID）。结果见 verification.json。没有改训练入口或门禁。

“未测 latency 会补 0”的初读判断经反例未复现，已撤回：原过滤逻辑会排除缺失延迟。没有把这一项算作漏洞；新测试保留未测语义。

## 建议的首轮资源方案（候选，不是执行批准）

本地 Qwen3 tokenizer 只读测量：按当前 screening SYSTEM/USER 模板、完整 problem+solution 和纯 scene_spec JSON 标签，enable_thinking=False，63 条的长度 **381–876，中位数 530**；全部低于 1024。具体逐样本长度在 before/after.json。实际训练模板变化、新评测样本、附加思考或更长标签需要重新测量，不能直接套用这组长度。

因此可先准备 **1024 长度、microbatch=1、4bit NF4 + BF16、梯度检查点** 的首轮小样本方案；无需默认上 4096。LoRA r=8/alpha=16/q-k-v-o 投影和梯度累积是待实测候选，不据合成探针固定为已验证参数。建议在正式后端落实：

1. 对量化模型调用 prepare_model_for_kbit_training，再加 LoRA；use_cache=False，检查基础参数冻结、优化器仅接收可训练参数。标准准备会改变非量化参数精度，可能增加某些内存占用，须重新测量，不承诺一定降低峰值。
2. 双重量化可作为降低显存的候选，保留独立配置与比较结果。NF4/BF16/训练准备函数与双重量化的用法核对了 [PEFT 官方指南](https://huggingface.co/docs/peft/developer_guides/quantization) 和 [Transformers 量化文档](https://huggingface.co/docs/transformers/main/quantization/bitsandbytes)。
3. 第一轮目标是 scene_spec，真实 collator 应对 prompt/PAD 使用 -100，仅监督 assistant 标签；保留目标终止 token，尤其 pad 与 eos 共用 ID 时按 attention mask 遮罩。必须有可人工核对的一条编码/标签边界样例，不把合成探针 labels=input_ids 搬到正式 SFT。
4. 固定 Qwen3 chat template 的 thinking 模式。当前标签没有思考正文，不能无说明地将 thinking 的 80% 筛选率用于 non-thinking 正式 baseline。官方明确在模板中设置 enable_thinking，当前脚本却将其传给 generate 后回退软指令，仍需修改。参见 [Qwen 官方模型卡](https://huggingface.co/Qwen/Qwen3-4B)。
5. 用同一正式准备流程验证一个完整 optimizer step 的显存及有限 loss/gradient，记录 allocated/reserved 和实际设备；8GB 必须留资源余量。当前 QLoRA 探针没有重置加载后的峰值，且未用标准 kbit 准备，不能把其 5.33 GB 直接当正式训练保证。
6. checkpoint 保存 adapter 之外还需保存 optimizer/scheduler/RNG/全局步数、tokenizer 和配置，并按已批准范围验证恢复。当前仅 adapter save 不等于可恢复训练。

上述真实 step/恢复测量仍需执行阶段授权；本轮没有做。不给未测 lr/epoch 等参数编造最优值。

## A10 修复效果及延期项

已确认 seed 和显式生成配置、子类覆盖、实际长度裁剪、增量保存结果等改善。仍有残余：thinking 模板开关接错入口、思考解析仅按字符串标签、秒级时间戳加 exist_ok=True 可碰撞覆盖、来源完整性异常不阻断，以及完整归档缺失。A10 不整体关闭。

PROGRESS/TRAIN_PREP_PLAN 仍有旧 baseline 和“未下载/未安装”声明，与实际状态矛盾。Claude Code 应在下一个可执行训练方案里同步；命名/排版、版本号等既有低影响维护项继续后置，不借本次审查扩展重构。

本报告及包版本清单为准备证据。训练后端可继续实现，真正执行以具体配置、适用门禁及用户授权为准。
