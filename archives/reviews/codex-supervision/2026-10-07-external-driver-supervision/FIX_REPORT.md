# 外部/LAN 采集入口修复与监管

2026-10-07，北京时间。Claude 的外部/LAN 采集入口已由 Codex 接管并修复。用户随后调整优先级为 holdout 草案，双端沙箱检测实验推迟至 2026-10-08；本次不新增该类实验。

## 结果

当前 tools/sandbox_external_test_driver.py 默认只输出 PLAN，原生采集必须显式提供参数；采集和接收端对账分开。新增 \(26\) 项针对性回归，与 IPv4 联合策略及全表门禁回归合计 \(64\) 项通过。范围是模拟证据与本地文件 I/O，不能当作外部或 LAN 双端原生验收。

只读 Get-NetIPAddress 元数据捕获的 IPv4/IPv6 子命令均 rc=0，原始 stdout/stderr 文件按实际最终字节绑定。它没有启动 AppContainer 作业，也没有发送正式接收端验收探针。当前校园 IPv6 证人与宿主同 /64，仍归 LAN；不能据此填写真正外部 IPv6 实锤。

主矩阵最后有效绑定仍为 \(30\) GREEN、\(0\) FAIL、\(2\) PARTIAL、\(11\) GAP。RoundA 不满足新双端证据契约，D9 仍为 GAP。生产 CLOSED，未写放行证书。

## 已修问题

- 所有原始输出按实际字节保存；修复计算 SHA 后另加换行导致文件不匹配的问题。
- 保留完整 stdout/stderr、真实 rc、超时类型及超时残余输出；不 strip、不截断、不伪造成功。
- TCP 完整发送并结束写方向；宿主 UDP sent 仅证明调用完成，不证明接收端收到。
- 沙箱网络拒绝严格识别 Win10013；超时和其他错误独立记账。
- 限定注册根、拒绝重解析路径、唯一目录和排他写入；部分失败保留真实材料。
- 记录整次运行的当前底层绑定、采集器源码 SHA、父作业/原生回执和高精度时间字段。
- 宿主前对照先成功；沙箱结束后观察不少于 \(20\) 秒，后对照完成在显式窗口内。
- 接收端必须有原始 v2 JSONL、summary、实际 rc、完整监听/关闭生命周期、准确包数、序列和不同主机身份。
- 双端 endpoint、协议、地址族、逐阶段 nonce、全 payload 及前后对照逐项对账。
- 任何实际接收的 sandbox nonce 立即作边界 FAIL；不把“未提供日志”误判为零送达。
- 外部层级结合发送端原生接口/前缀判断，拒绝同宿主、同 LAN 前缀及同 IPv6 /64。
- 对账只形成注册协议的限定证据，full_surface_accepted 始终为 False；不直接放行全 43 点。
- 旧 RoundA 原 JSON、route/interfaces 文件及工作目录输出保留，不能重签或修改旧字段来适配新契约。

旧接口文件实际 SHA 为 48b4dd4437a01829015a2d9810718feeac8c7bdfbdfa02332037529103851c67，旧报告声称的 SHA 不符；证据缺陷另记，原字节不改。RoundA 宿主 TCP connected、UDP sent，沙箱 UDP sent 和 TCP Win10013 只能证明具名调用结果；没有接收端原始回执，不能推出沙箱 UDP 已到达或未到达。

## 监管与交付

只读观察器旧 worker 44260 经 STOP 正常退出，隐藏重启后的 worker 为 37180，新增监听采集入口、测试、外部实验目录和 holdout 修订目录。后台只记录变化，不执行 AI 审查或准入；进程存在不能证明正在计算。

当前源码和测试的精确快照见 final-source/；sandbox_external_test_driver.repaired.py 是较早的暂存版本，不是最终交付源码。before-manifest.json 保留旧字节身份。unit-receipt.json 记录 \(64\) 项回归；host-interface-capture.json 仅为实际宿主接口/哈希检查。USAGE.md 说明明天实验时需收集的双端材料。

实验尚待：独立主机实际原始 JSONL/summary/rc、完整健康对照、真实外部 IPv6 双协议材料及全 43 点重新核验。不能以修复代码或单元测试替代这些证据。用户 IPv4 联合策略保持不变，不再单独要求公网 IPv4 节点。
