# Codex 当前协助所有权和验收条件

Codex 正在接手 `src/animtrain/validate.py`、`tools/preflight.py`、`tests/test_validate.py` 和 `tests/test_b5_preflight_binding.py`。请本轮暂不修改这些文件，等本目录 FIX_REPORT.md 的完成说明后再接续；保留双方修改，不整文件回退。

B5 签名规则校准只证明当前 48 对考点标注的一致性，不能给新增签名 AND J5≥2/5 的组合屏背书。组合屏在这些原标注上 TP=16、FN=1、FP=0、TN=31，召回率 16/17 < 19/20。按检测阈值排除漏检正例，再声称“作用域召回=1”，没有验证独立定义的正例。

最新 leakage_screen_calibration 可作为诊断保留。仅匹配 rule、threshold、calibrated 自报字段不足以解除 ready 阻断；还缺独立定义的泄漏标注、输入/实现/目标绑定及真实复算。Codex 会保存该自报信息，但保持近重复校准为 UNCALIBRATED，核心执行门禁 CLOSED。

已经修好按签名分组检索，防止不同签名的全池最高相似候选遮挡真实漏题；JSON 测试题干必须 json.dumps 转义 TeX。完成记录会包含独立回归结果与源码哈希。

## 已完成交接

113 项相关测试、22 个子测试全部通过；最终完整说明及源码/产物 SHA256 见本目录 FIX_REPORT.md、changes-manifest.json。本轮所有权处理完成，后续请在此实现基础上继续，不恢复自报字段放行。换题题目明细见 near-duplicate-candidates.json；原标注需按新的实际题文重新核对。
