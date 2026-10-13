# Claude Code 最新修改检查

检查时间：2026-10-05T22:11:38.091163+08:00。

最新修改已通过本轮独立复验。审阅期间Claude Code新增提交e990576（2026-10-05 22:07），只修改tools/draft_audit.py，修复18批清单SHA核对被路径基准差异跳过的问题。当前264题最终修订文档与题库仍为codex-repair-v4-final，未被这次提交改变。

## 最新修复与复验证据

检查开始时HEAD为34ec138，收件箱无新邮件。独立审阅发现P2问题：清单path相对草稿目录，而被审文件path相对项目根，直接比较导致18批均V011跳过SHA。隔离样例将batch-01 SHA改为全零，旧工具仍hard=0、V007=0、V011=18。

问题回传后，Claude Code在e990576统一路径基准。对实际已提交代码分别用错误SHA清单与当前正式清单复验：

| 场景 | V007哈希错误 | V011跳过 | 全局hard |
|---|---:|---:|---:|
| 故意错误SHA | 1 | 0 | 1 |
| 当前正式清单 | 0 | 0 | 0 |

这次修复已确认能检出错误，并正确校验现有18批。实际题库和正式清单未用于造错；造错只发生在独立审阅目录的隔离清单内。工具的导出返回码仍为0，清单级hard也不计入每个题号的rejected数量，本次判断读取全局severity_counts。

[修复前复现](binding-probe-result.json)；[实际提交正反例验证](committed-fix-validation.json)；[错误清单审计](committed-fix-bad-audit/summary.json)；[正式清单审计](committed-fix-real-audit/summary.json)。

## 题库与历史保护

36个最终题库/文档、26个保护输入/代码、134个历史版本/证据文件共196个文件的SHA全部与上一轮交付一致；selector SHA也一致。当前264题未发现内容回归、题目删减、文档失配或旧证据覆盖。

此前v3完成的公式中文、752步骤编号、81条字段补丁、正交分解证明等修复均保留；完整文档和264数学哈希绑定由Codex在v4-final补齐。v5/v6/v7是此前审计运行目录名称，不是新的题库选择版本。

## 当前仍未解除的训练隔离

生产数据检查仍不通过（exit_code=2）：隔离告警1项，包含linalg-048与eval-linalg-015-s1、test-linalg-025两对确认结构泄漏。保留原ID的实质改写候选已交付，但尚未替换活动版本或完成准入。此次审计工具修复没有取消该告警，没有启动训练。

用户打开的[final-cli-1.txt](../2026-10-05-readiness-completion/final-cli-1.txt)记录498条目、quarantine=0、clean，是历史结果，不能代表当前状态。以[本轮生产验证](current-production-validation.json)为准。

## 只读监听恢复

旧观察器PID40476已退出，最后成功心跳20:32:51，错误记录到20:33:37。CIM查询恢复后，按用户持续监管要求重启已有只读脚本，旧状态保存、旧日志未覆盖。

实际观察器PID12024；新心跳2026-10-05T22:09:56.337683+08:00。监听已记录本轮新增提交e990576。Claude进程存在仅表示会话进程存在，不能据此认定正在计算或卡住。

[重启前状态](observer-before-restart/latest.json)；[恢复及新提交状态](observer-after-fix-state.json)；[启动记录](watcher-restart.json)。

## 本轮边界

Codex未修改Claude Code的工具源文件、题库、生产清单、冻结eval/test、门禁或旧交付证据；只执行隔离复验、保存本轮报告及恢复已有只读观察器。修复由Claude Code提交，最终结论依据实际提交代码的正反例复验。
