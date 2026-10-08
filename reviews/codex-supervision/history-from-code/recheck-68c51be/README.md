# Animation Model Training（动画模型训练项目）

**v0.2.0 · 基础设施预发布 · 2026-10-01**

当前交付数据登记/拆分/校验、运行快照、冻结评测保护、数学/渲染检查及 preflight。最新验证为 **144 tests + 29 subtests 通过**；真实数据验收与模型训练尚未开展。

[发布说明](NEWRELEASE.md) · [当前进度](PROGRESS.md) · [审查备忘录](REVIEW_BACKLOG.md) · [下一周期](NEXT_CYCLE_PLAN.md)

本地项目目录为 D:/Animation-Model-Training，与 MathGuide（D:/code）独立。Claude Code 主导实现，Codex 同步审查并处理必要小修。训练、模型下载、依赖安装需另行批准。

## 当前入口

| 入口 | 职责与通过范围 |
|---|---|
| tools/make_manifest.py | 扫描数据根生成清单；输出必须位于该根，已有文件拒绝覆盖 |
| tools/split_data.py | 按 ID 计划拆分；写入前自动发现约定冻结锁，坏锁拒绝，跨目录传显式锁 |
| tools/data_check.py | 校验 manifest/目录；空输入失败；--dry-run 只说明检查项 |
| tools/check_fields.py | 核心字段校验，报告不能覆盖输入 |
| tools/check_code.py | 静态语法/API/中文 TeX 检查，静态通过不等于真实渲染通过 |
| tools/freeze_data.py | 生成 *.lock.json；--manifest 写入绑定哈希，检查冻结文件一致性 |
| tools/run_record.py | 记录配置、seed、环境、git 状态及数据版本 |
| tools/preflight.py | GPU/模型/数据/快照/冻结覆盖聚合及固定样例执行；完整资产验收门禁尚未闭合 |

核心代码在 src/animtrain/，测试在 tests/，审查证据在 reviews/。
标准见 [PIPELINE_PLAN.md](PIPELINE_PLAN.md)，最新复验见 [第四轮报告](reviews/2026-10-01-br-recheck-round4/REVIEW.md)。

## 本地验证

使用已有环境，不自动安装依赖：

```powershell
$env:PYTHONIOENCODING='utf-8'
$env:PYTHONUTF8='1'
$env:PYTHONDONTWRITEBYTECODE='1'
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider
.\.venv\Scripts\python.exe tools/data_check.py --dry-run
```

完整测试包含真实固定 MathTex 渲染，需要已配置的 Manim、SymPy、FFmpeg 和 TeX 工具链。
requirements.txt 记录已有 Python 环境包；不包含外部 FFmpeg/TeX 安装。

--dry-run 的成功不代表数据验收成功。数据检查退出码：0=当前检查通过，1=失败，2=quarantine 或参数错误。
相对输入/输出路径通常相对启动目录；代码检查内置白名单相对项目根。
来源和许可证要求见 [data/README.md](data/README.md)。

## 当前限制

- **正式 READY 尚缺当前资产验收证据缺失时的显式阻断**。固定 MathTex/数学样例是环境诊断，不能替代当前数据或产物验收；不能仅凭 CLI 的 READY 开始训练。
- 近重复候选截断漏检已修；0.7 仍为未校准初值，需要真实分布对照实验。
- 数学断言契约和可信固定样例渲染已验证；API 白名单仍不能代替实际资产验证。
- 不可信渲染默认拒绝；trusted=True 仅供已审查固定样例。完整文件系统/网络/内存隔离尚未实施。
- 冻结写保护限于约定锁发现范围和显式参数；单文件原子写不保证多文件发布事务。
- 正式实验重放、评测指标和逐样本结果契约仍需阶段验收。
- configs/data_check.example.json 是说明示例，CLI 不读取该配置。
- C 类维护问题按 REVIEW_BACKLOG 延期。

## 环境与资产

数据处理核心主要使用标准库，数学/渲染功能依赖 SymPy/Manim 及外部工具链。
当前完整验证使用 Python 3.13；pyproject 的 Python 下限不等同于整套渲染环境的兼容性承诺。
模型、原始数据、检查点、密钥和缓存不默认入库。reviews 中数据和零字节模型文件均为合成审查夹具，不是真实权重。代码许可证尚待确定。

## 重启时的既定结论(来自前项目的全部实测与决策,重启不用重走弯路)

### 目标
可审计、可修复、可交互的数学动画生成系统,质量向 3Blue1Brown 靠拢;
LoRA 是可替换组件,不是终点。从最小可用开始验证。

### 训练环境选项(实测)
| 环境 | 显存 | 说明 |
| --- | --- | --- |
| 本机 Windows + LLaMAFactory | 8GB | 4bit + rsLoRA 实测 36s/步;DoRA 实测慢 11 倍(弃用);paged 优化器收尾卡死(弃用) |
| 本机 WSL2 + Ubuntu + Unsloth | 8GB | WSL2 组件已装;需装 Ubuntu 发行版才可用;官方支持好但显存不变 |
| 云端 Colab + Unsloth | 16GB | 首选验证环境;数据 zip 上传、结果回传 D 盘 |

### 关键教训(前项目踩过的坑)
1. 训练目标退化:数据转换若丢弃 solution/answer,模型只会学"题干→常量 JSON"
2. 评测污染:评测集必须与训练池零精确重叠 + 近重复门禁 + 独立锁
3. 锁守卫:锁存在且内容一致则不可重写;不一致必须大声失败
4. DoRA 在 4bit 上慢 11 倍;模型输出带 markdown 围栏是格式问题不是能力问题
5. 训练须另行批准;R1 资产(前项目)已随目录删除,无恢复可能

### 硬约束(延续)
- 未经明确批准不启动训练
- 不碰系统文件;MathGuide(D:\code)与本项目无关
- 所有新数据带 manifest/来源/许可证/SHA256/门禁结果/限制说明
- 中文进 LaTeX 会编译失败(TeX 无 CJK),中文用 Text()
- API 正确性以运行中的 manim 内省为准,不手抄文档
