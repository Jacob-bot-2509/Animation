# Animation Model Training（动画模型训练项目）

当前为数学动画生成系统的实验基础设施：数据登记、分割、字段与静态代码检查、运行记录和 preflight。未实现真实模型训练。整体门禁仍在修补，测试通过不等于训练就绪。

本项目仅使用 D:/Animation Model Training，与 MathGuide（D:/code）独立。Claude Code 主导实现；Codex 同步审查并处理必要的小问题。训练、模型下载、依赖安装需用户另行批准。

## 当前入口

| 入口 | 职责与通过范围 |
|---|---|
| tools/make_manifest.py | 扫描数据根并生成清单；输出必须位于该根目录，已有文件拒绝覆盖 |
| tools/split_data.py | 按显式 ID 计划拆分；用它生成的 split_manifest.json 校验，不重新扫描猜测角色 |
| tools/data_check.py | 检查清单/扫描目录；空输入失败；--dry-run 仅显示骨架说明 |
| tools/check_fields.py | 校验指定核心字段；报告不得覆盖输入，即使 --force |
| tools/check_code.py | 静态检查；默认白名单相对项目根；数学/渲染显示 UNVERIFIED |
| tools/run_record.py | 运行记录创建/检查；完整可复现契约仍待补齐 |
| tools/preflight.py | 模型/GPU/数据诊断；完整 L1–L5 聚合仍待实现，不能独立授权训练 |

核心实现在 src/animtrain/；测试在 tests/；审查证据在 reviews/。验收标准见 [PIPELINE_PLAN.md](PIPELINE_PLAN.md)，最新整体复查见 [协调性报告](reviews/2026-09-30-coherence/REVIEW.md)。

## 本地验证

在项目根使用已有环境，不安装新依赖：

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q -p no:cacheprovider
.\.venv\Scripts\python.exe tools/data_check.py --dry-run
```

--dry-run 仅打印当前 schema/检查项说明，没有执行数据验收。实际数据准备和许可要求见 [data/README.md](data/README.md)。命令传入的相对输入/输出路径默认相对启动目录；代码检查的内置白名单固定相对项目根，显式 --whitelist 仍相对启动目录。

数据检查退出码：0=当前检查通过；1=失败；2=quarantine 待补齐或参数错误。调用方必须同时记录命令、模式和输出，不能把 --dry-run 的 0 当数据验收通过。代码检查的 0 仅表示已实现的静态检查通过。

## 当前限制

- 近重复阈值 0.7 为待重新校准的初值；候选截断、字段归一化和报告完整性仍需验证。
- API 白名单为示例快照，不能替代运行环境内省；真实数学/渲染未验证。
- 数据 schema/解析、快照、严格门禁聚合和冻结评测集锁仍有审查阻塞，详见 reviews。
- configs/data_check.example.json 是说明示例，CLI 不读取其中配置；修改它不会改变实际门禁。
- 扫描暂会登记根目录下全部文件，包括文档和历史清单；应使用专用数据版本目录，生成后人工核对条目与来源/许可。
- 本机显存规划预算 8GB。环境选项与历史测量保留在下方，未在本轮重新验证。

## 环境与资产

核心代码使用标准库，Python >= 3.10；当前测试使用已有 .venv 中的 pytest。模型、原始数据、检查点、密钥和缓存不应默认入库；.gitignore 只影响未跟踪文件。已有审查目录中的零字节模型文件是合成反例，不是真实权重。项目许可证尚待用户确认。

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
