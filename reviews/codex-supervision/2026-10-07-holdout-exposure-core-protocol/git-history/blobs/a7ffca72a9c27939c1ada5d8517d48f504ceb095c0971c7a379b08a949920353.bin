# 候选数据集审查报告

> 生成日期: 2026-10-02。工具: tools/dataset_intake.py report。

## 总览

- 样本总数: 64
- 状态: **rejected**(候选数据集,**不是已验收训练集**)
- 含义: candidate = 存在 quarantine 待补齐;rejected = 存在硬伤;clean = 无检查问题,但进正式 manifest 前仍需用户确认(许可证证据/ID 修复/answer 补齐)。

## 分类统计

- 高等代数: 23 条
- 数学分析: 19 条
- 解析几何: 12 条
- 概率论: 10 条

## 硬伤(problems,必须修复)

- **dataset_calc.jsonl: line 6: scene_spec 数学公式内出现中文(TeX 无 CJK,渲染必失败): $S_{\triangle OAB} < S_{扇形 OAB} < S_{\tri$**
- **dataset_geom.jsonl: id=geom-024 在行 5, 6 整条重复(内容完全相同);真实数据由用户确认后去重,不得静默改名**

## 待补齐(quarantine,candidate 语义)

- license=Internal-Research-Use-Only 仅限内部研究使用,不是公开再分发许可证(id=…)(×64)
- scene_spec 疑似漏反斜杠(\arctan 等): $\left[arctan x \right]_0^b = \arctan b$(×1)
- scene_spec 疑似漏反斜杠(\arctan 等): $lim_{b\to +\infty} \arctan b = arctan b = \frac{\pi}{2}$(×1)
- solution 疑似漏反斜杠(\infty(应写作 +\infty)): $\lim_{b\to +infty}\arctan b = \frac{\pi}{2}$(×1)

## 仍需用户确认的项

1. license=Internal-Research-Use-Only 的使用授权证据(非公开再分发许可证)
2. 重复/冲突 ID 的修改方案(以报告硬伤清单为准)
3. LaTeX 问题(公式内中文、疑似漏反斜杠)是否由用户修正(工具只报告,不改写数学语义)
