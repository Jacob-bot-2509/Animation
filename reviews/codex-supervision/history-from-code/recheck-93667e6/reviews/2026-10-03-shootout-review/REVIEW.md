# 三方模型筛选准备审查（2026-10-03）

结论：**准备代码尚不能支撑可信的三方比较结论**。应先修正判分、共同配置、实际长度及证据保存，再跑用于选 baseline 的对比。下载、环境准备及其他基础设施修复可以继续。本轮只审查准备，没有执行模型推理、加载权重、训练、安装或下载。

审查对象：`tools/screening_probe.py`、`tools/screening_qlora_probe.py`、`tools/model_provenance.py`、`MODEL_SHOOTOUT_PLAN.md`。脚本来自 127250b，方案截至 5f4fef6；反例执行时 HEAD 为 9ce2766。执行期间上述四文件哈希未变，详见 [results.json](results.json)。随后主力的 c88c128 改动属于其他模块，未凭其测试数量宣称本轮问题已关闭。

协作：已通过 AI Bridge 消息 224、225 发给 Claude Code。上述四文件由 Claude Code 主导修复；Codex 仅写本次审查材料与备忘录，避开在途修改。

## 需要在正式筛选比较前修正

| ID / 优先级 | 位置 | 独立依据及影响 | 修复验收 |
|---|---|---|---|
| S1 / P1 | screening_probe.py:125–132 | 未设置方案的 seed=0；仅覆盖部分生成参数。本地 Qwen2.5 generation_config 有 repetition_penalty=1.05，Qwen3 没有该项；脚本未覆盖它。三方“同口径”尚未落实，重跑也无法核对有效参数 | 显式冻结共同 GenerationConfig、量化与生成预算，记录所有有效参数和种子；按样本设置可复现 seed，保留环境及确定性边界 |
| S2 / P1 | screening_probe.py:52–77、119–126、134–145 | parser 从整段首个 { 截到最后 }。反例一：思考含另一 JSON + 正确最终 JSON，被判不可解析；反例二：只有 <think> 内的合法 scene_spec、没有最终回答，却 parsed/clean=true。Qwen3 仅收到 /no_think 软指令，未设置模板 enable_thinking | 明确设置 Qwen3 模板硬开关；分离思考 token 与最终答案，未完成思考/截断标为失败。严格 JSON、宽松提取、字段合规分开计，不把思考里的 JSON 当最终答案 |
| S3 / P1 | screening_qlora_probe.py:55–57、82–83 | 实际本地 tokenizer 测量：三款模型的标注 1024/2048/4096 对应 680/1364/2728 token。仅重复文字并未构造目标长度，容易低估目标序列资源开销 | 构造准确 token 数并断言、保存 actual_seq_len。资源曲线按实际长度比较；合成重复串仅用于合成资源探针，不能等同真实任务训练稳定性 |
| S4 / P1 | screening_probe.py:91、143、152–168；screening_qlora_probe.py:76–94 | mock 连续运行同 tag 的 2048 与 4096，仅剩 4096 summary 和一个 ckpt；推理同 tag 亦无条件覆盖。`../escaped` 写出了 inference 子目录。只存输出前 200 字、无完整输出/输入绑定/生成参数快照；异常发生在写文件之前，整轮已完成结果可能丢失 | 复用合法 run_id 守卫、唯一且默认不可覆盖的运行目录，长度/模式/seed 等全部记录。逐样本保存完整输出、输入和输出哈希、命令、代码/模型/环境证据及失败状态；失败不得消失或缩小分母。撤走临时组前归档完整可复核证据，不仅保留 PDF/摘要/删除清单 |
| S5 / P2 | screening_probe.py:36–49 | 当前只是每分类取文件前 n 行。几何 4 条全为“直线与平面”，库中还存在其他 4 个子类，违背方案覆盖不同 sub_category 的要求；不同模型运行期间原始文件可变，没有共同样本锁 | 优先覆盖子类，冻结同一 20 条 ID、输入与源文件哈希，缺额/重复/输入漂移拒绝。标注 provisional train 筛选成绩，不能当正式 eval/test 验收 |
| S6 / P2 | model_provenance.py:45–69 | config-only 无权重目录 rc=0；131 字节 Git LFS 指针被记录为成功的 weight_file。非独立模型 Git 目录会继承项目 HEAD。现有 Qwen2.5 provenance 的 total_bytes=30,478,357,620，实际列出的权重总和=15,231,271,888，递归 .git/LFS 缓存让两种体积混在一起 | 严格验证权重/index 分片与 LFS 未完成状态；核对 Git 顶层与模型来源，不能继承父仓库提交。分开报告模型文件和 clone 存储体积；许可证及来源是声明还是核验须明确 |
| S7 / P2 | screening_probe.py:104–115、128–135、150–159；screening_qlora_probe.py:36–52、61–72 | 推理计时未显式 CUDA 同步，使用 wall clock，未区分预热与首轮；两脚本使用 device_map=auto 却未保存实际分派/CPU offload。显存只有 allocated，没有 reserved 和失败状态 | 同步测量窗口，用单调计时；明确 cold/warm 口径，保存实际设备分派、allocated/reserved 峰值与 OOM/加载失败。未确认的 CPU 回退不能当纯 8GB GPU 成绩 |

Qwen3 的硬/软开关及按结束思考 token 分离内容，核对了 [Qwen 官方模型卡](https://huggingface.co/Qwen/Qwen3-4B)。本轮没有运行真实模型，S2 用显式构造输出验证 parser 行为，不声称任何模型实际出现上述输出。

## 方案与交付边界

- 方案写“仅推理、不训练”，QLoRA 入口实际调用 backward 和 optimizer.step。即使输入是合成文字、kind=dry-run，也包含参数训练操作；应明确资源训练探针的授权范围及执行门禁。本轮没有执行它，mock 仅记录调用。
- 当前代码未测首 token 延迟/思考 token 数、同模型满精度对 4bit 退化、梯度累积、断点恢复、数学内容准确性。保存 adapter 不等于断点恢复成功，loss_last 不等于稳定性曲线。
- 九维 PDF 对未测/不可用项应明确 NOT_MEASURED/FAILED/不适用，不能用其他结果补成“实测”。正式 baseline 结论由用户决定。
- 20 条 provisional train 可以做候选筛选，但不能取代冻结独立 eval/test。小样本结果说明本次样本上的表现，不能扩展成整体数学或动画质量已验收。
- 旧 B1/B2/B4/B6/A9 与本轮新问题分开跟踪。主力并行提交 93d943e、9ce2766、c88c128 的修复尚不在本次独立复验范围；其旧报告反例状态需后续重跑，不能沿用旧状态认定新代码仍失败。

## 验证与复现

```powershell
$env:PYTHONIOENCODING='utf-8'
$env:PYTHONDONTWRITEBYTECODE='1'
.\.venv\Scripts\python.exe reviews/2026-10-03-shootout-review/probe.py
```

[probe.py](probe.py) 用独立临时目录和 torch/transformers/peft 替身验证入口的记录/覆盖/路径行为，使用本地 tokenizer.json 只读计算长度，使用纯标准库验证来源记录边界。结果保存在 [results.json](results.json)，包含被审查源文件 SHA256 与执行时 HEAD。mock 的显存、耗时、loss、adapter 都是合成数据，**不是三模型实测成绩**。

本轮没有修改这三个执行脚本，也没有跑全量回归；全量基础设施测试无法替代这些新增入口的反例。以上问题仍为待修，不凭消息发送或报告落盘自动关闭。
