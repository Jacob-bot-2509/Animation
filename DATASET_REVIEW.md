# 候选数据集审查报告

> 生成日期: 2026-10-02。工具: tools/dataset_intake.py report。

## 总览

- 样本总数: 63
- 状态: **clean**(候选数据集,**不是已验收训练集**)
- 含义: candidate = 存在 quarantine 待补齐;rejected = 存在硬伤;clean = 入场检查通过(正式验收仍需全链路,见报告下一步)。

## 分类统计

- 高等代数: 23 条
- 数学分析: 19 条
- 解析几何: 11 条
- 概率论: 10 条

## 下一步

- 入场检查已通过;进正式验收仍需全链路:make_manifest → data_check → split → freeze → preflight --ready。
- clean 不代表训练就绪;真实数据验收以全链路结果为准。
