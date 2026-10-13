# 下一周期准备:真实数据集进入前的可执行骨架(msg_146 第二部分)

> 2026-10-01。基线 a4eb3b9。仅准备,不训练、不下载模型、不安装依赖。

## 1. 选定任务的 JSONL schema(最小必需字段)

reasoning 数据(problem → solution → answer):

```json
{
  "id": "稳定唯一 ID(str/int)",
  "problem": "完整题干",
  "solution": "完整解答过程",
  "answer": "可判分终答",
  "source": "真实来源",
  "license": "已确认许可证(apache-2.0|mit|internal-generated|cc-by-sa-4.0)",
  "sha256": "该行内容哈希(登记时实测)",
  "size": 0
}
```

animation 数据(加 scene_spec):

```json
{
  "id": "...", "problem": "...", "scene_spec": "AnimationSpec v2 结构",
  "code": "可执行 manim 代码(过 render_gate)",
  "source": "...", "license": "...", "sha256": "...", "size": 0
}
```

分区:raw(原始只读)/ normalized(清洗后)/ train / eval / test。
**禁止原地覆盖**:所有清洗/拆分写新文件,原文件只读。

## 2. 数据验收入口/报告契约

- 入口:make_manifest → data_check(--manifest 校验:
  文件存在/SHA256/size/source/license/坏 JSON/非对象行/非法 ID/
  精确重叠/近重复)
- 报告契约:exit_code 0=通过 1=硬伤 2=quarantine;报告含
  problems/quarantines 清单与 near_dup_calibrated 状态
- **近重复未校准(UNCALIBRATED)必须阻断 ready**,不得假绿
- 目录约定:data/v1/{raw,normalized,train,eval,test}/
  (manifest 与数据同目录自包含)

## 3. eval/test 冻结与 READY 证据目录规范

- 冻结锁:*.lock.json(强制命名),freeze_data CLI
  --manifest 绑定 manifest_sha256
- 锁内每文件记录 sha256/size;冻结后哈希变化大声失败
- READY(freeze_gate)要求:当前 manifest 的 eval/test **全量**被锁
  覆盖、无坏锁、绑定 manifest_sha256 与当前一致;
  无锁/部分覆盖/无关锁/坏锁/绑定不一致 → NOT READY
- 环境 smoke(固定 MathTex/数学样例)保留为**环境诊断**,
  在 READY 输出中明确标识非资产验收证据

## 4. 最小 synthetic fixture/验收脚本

- fixtures:archives/reviews/ 下合成样例(现有)+ 新增 data/v1 骨架目录
  (README + 空分区占位)
- 验收脚本:一条命令链(make_manifest → freeze_data → data_check
  → preflight --ready),全部 dry-run 可重放
- **synthetic 结果不得写成真实数据通过**,报告注明 synthetic

## 5. 下一周期开始条件与用户确认清单

开始真实数据验收前,用户需确认:
1. 数据来源与许可证(逐来源证据,不填假值)
2. 数据规模(条数/体积)与分区计划
3. 模型路线(底座选择:7B 级候选/训练方式)与显存预算(本机 8GB
   / 云端 16GB)
4. 是否允许真实数据入 D 盘统一目录与上传云端(如需要)

## 6. 文档同步

REVIEW_BACKLOG 的 B 组状态已在 23c3432 后更新至 a4eb3b9 水平;
本文件为计划补充。RESTART_LOG 由协作方维护,不覆盖。
