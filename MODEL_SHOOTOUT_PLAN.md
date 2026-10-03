# 底座模型实弹对照方案(MODEL_SHOOTOUT_PLAN)

> 2026-10-03。用户已批准下载三款候选(均在 HF 官方仓库,Apache-2.0,git-lfs):
> Qwen2.5-7B-Instruct、Qwen3-4B、Qwen3-8B。
> 对照目标:数据说话选第一版 baseline;**仅推理对照,不训练**。

## 1. 候选与下载状态

| 候选 | 目录 | 状态 |
|---|---|---|
| Qwen2.5-7B-Instruct | .models/qwen2.5-7b-instruct | 下载中 |
| Qwen3-4B | .models/qwen3-4b | 下载中 |
| Qwen3-8B | .models/qwen3-8b | 下载中 |

下载完成后逐一运行 tools/model_provenance.py 生成 PROVENANCE.json
(来源/许可证/git commit/关键文件与权重 SHA256)。

## 2. 输入样本(20 条)

- 从 63 条 provisional train 按板块分层抽样:数学分析 6、概率论 5、
  解析几何 4、高等代数 5(各覆盖不同 sub_category);
- 输入 = problem + solution(与第一轮训练目标一致),输出 = scene_spec
  (objects/steps 设计稿),**不要求生成 Manim code**;
- 固定 prompt 模板与生成参数(seed=0,temperature 一致),每模型每样本生成 1 次。

## 3. 评测指标(全部实测,不引用外部榜单)

公开评测已覆盖:数学榜单(AIME/MATH500/AMC23/Minerva)、RL 方法(GRPO/PIPO 等)、
token 预算推理、投机解码加速。**以下维度公开未见、且正是我们的配置与任务**:

1. **8GB 上 QLoRA 训练实际峰值显存**(重点:8B;4B 与 2.5-7B 同测作对照)——
   公开数据没有 Windows+8GB+bitsandbytes 4bit 的真实训练显存曲线;
2. **Windows + bitsandbytes 兼容性**:4bit 加载/训练在 Windows 上能否跑通
   本身就是未测维度(加载成功率、警告与回退行为);
3. **中文数学 → scene_spec 结构化 JSON 可解析率**(primary,公开零覆盖):
   按 {objects, steps} 解析成功率、字段类型合规率;
4. **seq_len 显存曲线**:2048/4096 下激活显存增长(我们输出长,必须实测);
5. **batch=1 + 梯度累积的训练吞吐**(8GB 约束下的真实步时);
6. **thinking 模式开销**(Qwen3 特有):思考 token 数、首 token 延迟、
   non-thinking 对比;我们的 pipeline 大概率选 non-thinking,需实测依据;
7. **RTX 5060 Laptop(Blackwell)推理延迟/吞吐**:新卡公开数据少;
8. **4bit 量化在我们任务上的格式/内容退化**:官方指标均满精度,
   量化后 JSON 合规率与数学一致性无公开数据;
9. **训练稳定性**:loss 峰值、checkpoint 体积、断点恢复(小样本 dry-run 实测)。

数学正确率沿用:规则检查 + 人工抽样复核(不把 LLM 判分当唯一真值)。

## 4. 前置条件(需用户批准后执行)

- 安装推理/训练依赖到项目 .venv:transformers、torch、accelerate、peft、
  bitsandbytes(与 R1 时代同栈;工具装 D:\Settings、Python 包装 .venv 的约定);
- 装好后才可执行 §2/§3;在此之前只做 provenance 记录与方案冻结。

## 5. 判定与回滚

- 三模型横向对比表 → 由用户拍板第一版 baseline;
- 落选模型保留在 .models/ 作后续对照,不删除;
- 本方案不启动训练;训练仍按 preflight 八项门禁 + 用户明确批准。

## 6. 边界

- 不把对照结果写成"已验收";candidate/UNVERIFIED 语义保持;
- eval/test 独立制作与冻结、B5 校准不受本方案影响;
- 所有输出产物记录哈希与命令(可重放)。
