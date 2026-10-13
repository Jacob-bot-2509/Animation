# Animation Model Training(动画模型训练项目)

> 创建:2026-09-16;骨架:2026-09-30。用途:前动画模型项目(D:\manim-agent-lab)
> 删除后,重启项目时的**新工作目录**。当前为最小可运行骨架(数据 manifest
> 与校验管线),未实现模型训练,未下载大模型。
> **与 MathGuide(D:\code)完全独立**:本项目的代码/数据/环境/Git/权重/记录
> 全部独立维护,不读取、不引用、不复用 D:\code 的任何内容。

## 项目结构

```
src/animtrain/        核心包(纯标准库,零依赖)
  manifest.py         manifest schema(v1):Entry/Manifest/白名单/内容哈希
  validate.py         校验:文件存在/SHA256/许可证/split/训练-评测精确重叠
  scan.py             目录扫描 → 临时 manifest(按子目录推断 split)
tools/
  make_manifest.py    生成 manifest(扫目录、算 SHA256、登记)
  data_check.py       校验 CLI(--manifest / --scan / --dry-run)
configs/
  data_check.example.json  检查约定与命令示例
tests/
  test_validate.py    校验器测试(unittest,8 项,含重叠检出)
data/README.md        数据目录与 manifest 规范
```

## 快速验证

```bash
python tools/data_check.py --dry-run            # 骨架自检(无数据时)
python -m unittest discover tests               # 测试(8/8)
python tools/make_manifest.py --dir data --out data/manifest.json \
    --name animation-data-v1 --source <来源> --license <许可证>
python tools/data_check.py --manifest data/manifest.json
```

manifest 与数据同目录自包含:entry.path 相对 manifest 所在目录。

## 未实现/遗留(如实)

- 未实现任何模型训练(等待规划文件与批准)
- 未下载大模型
- source/license 扫描时只能统一登记,须人工逐条复核真实性
- 数据格式(JSONL 字段)待训练方案确定
- **近重复阈值待校准(如实)**:5-gram Jaccard ≥0.7 是前项目在英文长题
  (几百字符)上实测校准的;中文题面更短(几十字符),实测尾部改措辞的
  同题 sim 可低至 0.585(漏报)或 0.706(检出)——阈值对短题不稳定。
  待真实数据就位后做对照实验重校准,当前不拍脑袋改阈值;
  tests/test_near_dup.py::test_short_text_limitation_documented 钉住了此局限

## 环境

- venv: `.venv/`(仅 dev 依赖 pytest;运行代码纯标准库)
- 测试: `.venv/Scripts/python.exe -m pytest tests/`(15 项)
- Python ≥ 3.10

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
